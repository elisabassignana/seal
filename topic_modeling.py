from seal.topic_modeling import LDATopicModel
from seal.preprocessing import SimpleTMPreprocessor
from scipy.stats import chi2_contingency, entropy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse
import logging
import os
from pathlib import Path
import sys
import textwrap
import warnings
import multiprocessing as mp

import matplotlib
matplotlib.use("Agg")

warnings.filterwarnings("ignore")

###############################################################
# CONFIGURATION
###############################################################
DATA_PATH = "data/Elisa_prompts_all.csv"
OUTPUT_DIR = "data/output/plots"
MODELS_DIR = "data/output/models"
K_MIN, K_MAX, K_STEP = 15, 51, 5
NUM_ITERS = 1500
TOPN_WORDS = 15
RANDOM_SEED = 42
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-5.4-nano-2026-03-17"
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
TAB20 = plt.colormaps["Paired"].colors
EXPORT_DPI = 320

DEMO_COLS = [
    "gender", "age", "nationality", "ethnicity", "marital", "language",
    "religion", "education", "mum_education", "dad_education", "ses",
    "home", "employment", "occupation", "mother_occupation", "father_occupation",
    "hobbies", "tech", "know_nlp", "use_nlp", "would_nlp",
    "frequency_llm", "llm_use", "usecases",
]

# Semicolon-separated columns: keep only the first value for plots
MULTI_VALUE_COLS = {
    "nationality", "ethnicity", "language", "occupation",
    "mother_occupation", "father_occupation", "hobbies", "tech",
    "know_nlp", "use_nlp", "would_nlp", "llm_use", "usecases",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(
            OUTPUT_DIR, "pipeline.log"), mode="w"),
    ],
)
logger = logging.getLogger("topic_pipeline")


def _plot_output_dir_for_k(k: int) -> Path:
    out_dir = Path(OUTPUT_DIR) / f"k_{k}_topics"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


###############################################################
# STATISTICS
###############################################################
def compute_chi2_stats(df_plot: pd.DataFrame, col: str) -> dict:
    """ Chi-squared test of independence between topic assignment and a demographic column."""
    ct = pd.crosstab(df_plot["dominant_topic"], df_plot[col])
    # Drop columns that are all-zero to avoid degenerate tables
    ct = ct.loc[:, ct.sum() > 0]
    if ct.shape[1] < 2:
        return {"col": col, "chi2": np.nan, "p_value": np.nan, "dof": np.nan,
                "n": len(df_plot), "cramers_v": np.nan}
    chi2, p, dof, _ = chi2_contingency(ct)
    v = cramers_v_from_chi2(chi2, len(df_plot), ct.shape)
    return {"col": col, "chi2": round(chi2, 4), "p_value": round(p, 6),
            "dof": dof, "n": len(df_plot), "cramers_v": round(v, 4)}


def cramers_v_from_chi2(chi2: float, n: int, shape: tuple) -> float:
    """Cramér's V effect size from a chi2 statistic. O is no association and 1 is perfect association. V < 0.1 weak, 0.1-0.3 moderate, > 0.3 strong.
    """
    k = min(shape) - 1
    if n * k == 0:
        return 0.0
    return float(np.sqrt(chi2 / (n * k)))


def cramers_v(df_plot: pd.DataFrame, col: str) -> float:
    """Cramér's V directly from a dataframe and column."""
    ct = pd.crosstab(df_plot["dominant_topic"], df_plot[col])
    ct = ct.loc[:, ct.sum() > 0]
    if ct.shape[1] < 2:
        return 0.0
    chi2, _, _, _ = chi2_contingency(ct)
    return cramers_v_from_chi2(chi2, len(df_plot), ct.shape)


def topic_demographic_entropy(df_plot: pd.DataFrame, tpc_labels: list, col: str) -> pd.DataFrame:
    """
    For each topic, compute the Shannon entropy of the demographic distribution. If the entropy is low, it means the topic is dominated by one group, while a high entropy (weak signal) means there is a uniform mix across groups.
    """
    rows = []
    for i, lbl in enumerate(tpc_labels):
        mask = df_plot["dominant_topic"] == i
        n_docs = int(mask.sum())
        if n_docs == 0:
            continue
        counts = df_plot.loc[mask, col].value_counts(normalize=True)
        h = float(entropy(counts))
        rows.append({
            "topic_id": i,
            "topic_label": f"T{i}: {lbl}",
            "n_docs": n_docs,
            "entropy": round(h, 4),
            "majority_val": counts.index[0],
            "majority_pct": round(float(counts.iloc[0]), 4),
            "variable": col,
        })
    return pd.DataFrame(rows).sort_values("entropy")


def export_topic_profiles(df_plot: pd.DataFrame, tpc_labels: list,
                          col: str, output_dir: Path) -> None:
    """Export the full proportion breakdown per topic for a demographic column. Each row is a topic; each column is a demographic category. """
    ct = pd.crosstab(df_plot["dominant_topic"],
                     df_plot[col], normalize="index")
    ct.index = [f"T{i}: {tpc_labels[i]}" for i in ct.index]
    ct.to_csv(output_dir / f"profile_{col}.csv")


def aggregate_to_user_level(
    df_ordered: pd.DataFrame,
    tpc_labels: list,
) -> pd.DataFrame | None:
    """Collapse prompt-level data to one row per user."""
    if "user_id" not in df_ordered.columns:
        logger.warning(
            "  [user-level] no user_id column - skipping aggregation")
        return None
    n_before = len(df_ordered)
    df_valid = df_ordered.dropna(subset=["user_id"]).copy()
    n_dropped = n_before - len(df_valid)
    if n_dropped > 0:
        logger.warning(
            "  [user-level] %d rows had NaN user_id and were dropped before aggregation. ",
            n_dropped,
        )
    if df_valid.empty:
        logger.warning(
            "  [user-level] no valid user_ids after dropping NaN - skipping aggregation")
        return None

    demo_cols_present = [c for c in DEMO_COLS if c in df_valid.columns]

    topic_mode = (
        df_valid.groupby("user_id")["dominant_topic"]
        .agg(lambda x: x.mode().iloc[0])
        .rename("dominant_topic")
    )
    topic_diversity = (
        df_valid.groupby("user_id")["dominant_topic"]
        .nunique()
        .rename("topic_diversity")
    )
    n_prompts = (
        df_valid.groupby("user_id")["dominant_topic"]
        .count()
        .rename("n_prompts")
    )
    demo = df_valid.groupby("user_id")[demo_cols_present].first()

    user_df = (
        pd.concat([topic_mode, topic_diversity, n_prompts, demo], axis=1)
        .reset_index()
    )
    user_df["topic_label"] = [
        f"T{t}: {tpc_labels[t]}" for t in user_df["dominant_topic"]
    ]

    n_users = len(user_df)
    n_prompts_total = len(df_valid)
    logger.info(
        f"  [user-level] {n_prompts_total:,} prompts → {n_users:,} users  "
        f"(mean {n_prompts_total/n_users:.1f} prompts/user)"
    )
    return user_df


def compute_user_level_stats(
    df_ordered: pd.DataFrame,
    tpc_labels: list,
    plot_output_dir: Path,
) -> pd.DataFrame | None:
    """Run chi-squared + Cramér's V + proportion profiles at user level."""
    logger.info("Computing user-level statistics ...")

    user_df = aggregate_to_user_level(df_ordered, tpc_labels)
    if user_df is None:
        return None

    # topic size (users)
    topic_sizes = (
        user_df.groupby("dominant_topic")
        .agg(n_users=("user_id", "count"), n_prompts_total=("n_prompts", "sum"))
        .reset_index()
    )
    topic_sizes["topic_label"] = [
        f"T{t}: {tpc_labels[t]}" for t in topic_sizes["dominant_topic"]
    ]
    topic_sizes.to_csv(plot_output_dir /
                       "user_level_topic_sizes.csv", index=False)

    # tests
    stats_rows = []
    for col in DEMO_COLS:
        if col not in user_df.columns:
            continue
        tmp = user_df.copy()
        tmp[col] = simplify_col(tmp[col], col)
        row = compute_chi2_stats(tmp, col)
        stats_rows.append(row)

    stats_df = pd.DataFrame(stats_rows)
    n_tests = stats_df["p_value"].notna().sum()
    stats_df["p_bonferroni"] = (
        stats_df["p_value"] * n_tests).clip(upper=1.0).round(6)
    stats_df["significant_bonferroni"] = stats_df["p_bonferroni"] < 0.05
    stats_df = stats_df.sort_values("cramers_v", ascending=False)
    stats_df.to_csv(plot_output_dir / "user_level_chi2_stats.csv", index=False)

    # proportion
    for col in DEMO_COLS:
        if col not in user_df.columns:
            continue
        tmp = user_df.copy()
        tmp[col] = simplify_col(tmp[col], col)
        ct = pd.crosstab(tmp["dominant_topic"], tmp[col], normalize="index")
        ct.index = [f"T{i}: {tpc_labels[i]}" for i in ct.index]
        ct.to_csv(plot_output_dir / f"user_level_profile_{col}.csv")

    user_df.to_csv(plot_output_dir / "user_level_assignments.csv", index=False)

    logger.info("  User-level Cramér's V (corrected for pseudoreplication):")
    for _, r in stats_df.head(8).iterrows():
        sig = "[SIG]" if r.get("significant_bonferroni") else " "
        v_str = f"{r['cramers_v']:.3f}" if not np.isnan(
            r["cramers_v"]) else "N/A"
        p_str = f"{r['p_bonferroni']:.4f}" if not np.isnan(
            r["p_bonferroni"]) else "N/A"
        logger.info(
            f"    [{sig}] {r['col']:<22}  V={v_str}  p_bonf={p_str}  n={r['n']}")

    logger.info(f"  user_level_assignments.csv → {len(user_df):,} users")
    return user_df


def compare_prompt_vs_user_stats(
    prompt_stats_path: Path,
    user_stats_path: Path,
) -> None:
    """Log a side-by-side comparison of Cramér's V at prompt level vs user level."""
    if not prompt_stats_path.exists() or not user_stats_path.exists():
        logger.warning(
            "  [compare] one or both stats files missing - skipping comparison")
        return

    p = pd.read_csv(prompt_stats_path).set_index("col")
    u = pd.read_csv(user_stats_path).set_index("col")
    common = p.index.intersection(u.index)

    logger.info("  ** Prompt-level vs user-level Cramér's V **")
    logger.info(
        f"    {'Variable':<22}  {'V prompts':>9}  {'V users':>8}  {'Δ':>7}  Verdict")
    logger.info("    " + "─" * 68)

    for col in sorted(common, key=lambda c: -p.loc[c, "cramers_v"]):
        vp = p.loc[col, "cramers_v"]
        vu = u.loc[col, "cramers_v"]
        if pd.isna(vp) or pd.isna(vu):
            continue
        delta = vu - vp
        sig_u = bool(u.loc[col, "significant_bonferroni"])
        sig_p = bool(p.loc[col, "significant_bonferroni"])

        if delta < -0.02 and sig_p and not sig_u:
            verdict = "[!]  inflated at prompt level - not robust"
        elif delta < -0.02 and not sig_p and not sig_u:
            verdict = "[NOISE]  not significant at either level"
        elif delta < -0.02 and sig_u:
            verdict = "[LOW]  smaller but still significant"
        elif abs(delta) <= 0.02 and sig_u:
            verdict = "[OK]  stable & significant"
        elif abs(delta) <= 0.02 and not sig_u and not sig_p:
            verdict = "[STABLE-NOT-SIG]  stable (not significant at either level)"
        elif abs(delta) <= 0.02 and not sig_u and sig_p:
            verdict = "[STABLE-MIXED]  stable but significant at prompt level only"
        else:
            verdict = "[HIGH]  stronger at user level"

        logger.info(
            f"    {col:<22}  {vp:>9.3f}  {vu:>8.3f}  {delta:>+7.3f}  {verdict}"
        )


def compute_and_export_stats(df_ordered: pd.DataFrame, tpc_labels: list, plot_output_dir: Path) -> None:
    """Run all statistical analyses and export results."""

    logger.info("Computing demographic statistics ...")
    stats_rows = []
    entropy_dfs = []

    for col in DEMO_COLS:
        if col not in df_ordered.columns:
            continue

        tmp = df_ordered.copy()
        tmp[col] = simplify_col(tmp[col], col)

        # chi2 + Cramér's V
        row = compute_chi2_stats(tmp, col)
        stats_rows.append(row)

        # full proportion profiles
        export_topic_profiles(tmp, tpc_labels, col, plot_output_dir)

        # per-topic entropy
        entropy_df = topic_demographic_entropy(tmp, tpc_labels, col)
        entropy_dfs.append(entropy_df)

    # chi2
    stats_df = pd.DataFrame(stats_rows)
    n_tests = stats_df["p_value"].notna().sum()
    stats_df["p_bonferroni"] = (
        stats_df["p_value"] * n_tests).clip(upper=1.0).round(6)
    stats_df["significant_bonferroni"] = stats_df["p_bonferroni"] < 0.05
    stats_df = stats_df.sort_values("cramers_v", ascending=False)

    chi2_path = plot_output_dir / "chi2_stats.csv"
    stats_df.to_csv(chi2_path, index=False)
    logger.info(f"  Chi2 stats saved → {chi2_path}")

    # log a quick summary to console
    logger.info("  Top variables by Cramér's V (effect size):")
    for _, r in stats_df.head(8).iterrows():
        sig = "✓" if r.get("significant_bonferroni") else " "
        v_str = f"{r['cramers_v']:.3f}" if not np.isnan(
            r["cramers_v"]) else "  N/A"
        p_str = f"{r['p_bonferroni']:.4f}" if not np.isnan(
            r["p_bonferroni"]) else "  N/A"
        logger.info(f"    [{sig}] {r['col']:<22}  V={v_str}  p_bonf={p_str}")

    # entropy summary
    if entropy_dfs:
        entropy_all = pd.concat(entropy_dfs, ignore_index=True)
        entropy_path = plot_output_dir / "topic_entropy.csv"
        entropy_all.to_csv(entropy_path, index=False)
        logger.info(f"  Entropy table saved  → {entropy_path}")

        # flag topics+variables where the majority_pct is actually substantial
        strong = entropy_all[entropy_all["majority_pct"] >= 0.50].sort_values(
            "majority_pct", ascending=False
        )
        if not strong.empty:
            logger.info(
                "  Topics with ≥50% majority in at least one variable:")
            for _, r in strong.head(10).iterrows():
                logger.info(
                    f"    {r['topic_label'][:35]:<35}  {r['variable']:<20}"
                    f"  {r['majority_val'][:25]:<25}  {r['majority_pct']*100:.1f}%"
                )
        else:
            logger.info(
                "  No topic/variable pair reached ≥50% majority - signals are weak.")

    logger.info("  Done with prompt-level statistics.")

    # user-level reanalysis
    compute_user_level_stats(df_ordered, tpc_labels, plot_output_dir)
    compare_prompt_vs_user_stats(
        plot_output_dir / "chi2_stats.csv",
        plot_output_dir / "user_level_chi2_stats.csv",
    )

    logger.info("  Done with statistics.")
    
    # stacked bar plots at user level
    # Bar charts using the user-level dataframe so that
    # the n shown above each bar and the proportions in the bars
    # match the user-level profiles used in the statistical analysis.
    user_assignments_path = plot_output_dir / "user_level_assignments.csv"
    if user_assignments_path.exists():
        logger.info("Generating user-level stacked bar plots ...")
        user_df = pd.read_csv(user_assignments_path)
        # user_df has dominant_topic as int; reconstruct topic_label
        user_df["dominant_topic"] = user_df["dominant_topic"].astype(int)
        user_df["topic_label"] = [
            f"T{t}: {tpc_labels[t]}" for t in user_df["dominant_topic"]
        ]
        ul_bar_dir = plot_output_dir / "user_level_bars"
        ul_bar_dir.mkdir(exist_ok=True)
        for col in DEMO_COLS:
            if col not in user_df.columns:
                continue
            tmp = user_df.copy()
            tmp[col] = simplify_col(tmp[col], col)
            make_stacked_bar(
                tmp, tpc_labels, col,
                f"Topic composition by {col} (user level)",
                (ul_bar_dir / f"bar_{col}.png").as_posix(),
            )
        logger.info(f"  User-level bar plots saved → {ul_bar_dir}/")
    else:
        logger.warning(
            "  user_level_assignments.csv not found — "
            "skipping user-level bar plots. Run compute_user_level_stats first."
        )


###############################################################
# SUMMARY DASHBOARD
###############################################################
AGE_MIDPOINTS = {
    "18-24": 21, "25-34": 29.5, "35-44": 39.5,
    "45-54": 49.5, "55-60": 57.5, "60+": 65,
}

DASHBOARD_METRICS = [
    # (col,            label,              type,        target)
    ("age",            "Mean age",         "mean_age",  None),
    ("ses",            "Mean SES (1-10)",  "mean_ses",  None),
    ("gender",         "% Female",         "pct",       "Female"),
    ("education",      "% Postgrad",       "pct_high",
     ["Graduate degree", "Doctorate or above"]),
    ("nationality",    "% UK",             "pct",       "United Kingdom"),
    ("nationality",    "% US",             "pct",       "United States"),
    ("frequency_llm",  "% Daily LLM use",  "pct",       "Every day"),
    ("religion",       "% No religion",    "pct",       "Nothing"),
    ("marital",        "% Married",        "pct",       "Married"),
    ("employment",     "% Employed FT",    "pct",       "Employed full time"),
]


def _compute_metric(profile_df: pd.DataFrame, metric_type: str, target) -> pd.Series:
    """Compute a single metric column from a proportion profile DataFrame."""
    if metric_type == "mean_age":
        cols = [c for c in AGE_MIDPOINTS if c in profile_df.columns]
        return sum(profile_df[c] * AGE_MIDPOINTS[c] for c in cols)

    if metric_type == "mean_ses":
        num_cols = [c for c in profile_df.columns if c.isdigit()]
        return sum(profile_df[c] * int(c) for c in num_cols)

    if metric_type == "pct":
        return profile_df[target] if target in profile_df.columns else pd.Series(
            0.0, index=profile_df.index)

    if metric_type == "pct_high":
        present = [c for c in target if c in profile_df.columns]
        return sum(profile_df[c] for c in present) if present else pd.Series(
            0.0, index=profile_df.index)

    raise ValueError(f"Unknown metric_type: {metric_type!r}")


def _build_summary_table(
    df_ordered: pd.DataFrame,
    tpc_labels: list,
    plot_output_dir: Path,
    use_user_level: bool = True,
) -> pd.DataFrame:
    """
    Build a (n_topics x n_metrics) summary DataFrame based on user level profiles."""
    n_topics = len(tpc_labels)
    topic_index = [f"T{i}: {lbl}" for i, lbl in enumerate(tpc_labels)]

    n_docs_series = (
        df_ordered["dominant_topic"]
        .value_counts()
        .reindex(range(n_topics), fill_value=0)
    )
    rows = {t: {"n_docs": int(n_docs_series.iloc[i])}
            for i, t in enumerate(topic_index)}

    # add user counts when available
    ul_sizes_path = plot_output_dir / "user_level_topic_sizes.csv"
    if ul_sizes_path.exists():
        ul_sizes = pd.read_csv(ul_sizes_path)
        ul_map = dict(zip(ul_sizes["topic_label"], ul_sizes["n_users"]))
        for t in topic_index:
            rows[t]["n_users"] = int(ul_map.get(t, 0))

    for col, label, mtype, target in DASHBOARD_METRICS:
        ul_path = plot_output_dir / f"user_level_profile_{col}.csv"
        prompt_path = plot_output_dir / f"profile_{col}.csv"

        if use_user_level and ul_path.exists():
            profile_path = ul_path
        elif prompt_path.exists():
            profile_path = prompt_path
        else:
            logger.warning(
                f"  [summary] no profile found for '{col}' - skipping '{label}'")
            continue

        profile = pd.read_csv(profile_path, index_col=0)
        metric = _compute_metric(profile, mtype, target)
        if not isinstance(metric, pd.Series):
            metric = pd.Series(metric, index=profile.index)
        for t in topic_index:
            rows[t][label] = float(
                metric.loc[t]) if t in metric.index else float("nan")

    summary = pd.DataFrame.from_dict(rows, orient="index")
    summary.index.name = "topic"
    return summary


def make_summary_dashboard(
    df_ordered: pd.DataFrame,
    tpc_labels: list,
    plot_output_dir: Path,
    best_k: int,
    min_n: int = 10,
) -> None:
    """
    Generate table showing  key demographic metrics for every topic, plus a colour-coded bar chart ranking each metric.
    * Top panel : heatmap table (topics x metrics). Each column is normalised 0-1 so colours are comparable across metrics with different scales. Raw values are printed inside each cell. Topics with n < min_n are greyed out.
    * Bottom panel: horizontal bar chart of n_docs per topic (log scale), so the dominant-topic imbalance is immediately visible.

    Parameters
    ----------
    min_n : topics with fewer docs than this are still shown but dimmed.
    """
    logger.info("Generating summary dashboard ...")

    summary = _build_summary_table(
        df_ordered, tpc_labels, plot_output_dir, use_user_level=True)
    summary.to_csv(plot_output_dir / "summary_dashboard.csv")
    logger.info(
        f"  summary_dashboard.csv saved → {plot_output_dir / 'summary_dashboard.csv'}")

    metric_cols = [label for _, label, _, _ in DASHBOARD_METRICS
                   if label in summary.columns]
    if not metric_cols:
        logger.warning(
            "  No metric columns available - skipping dashboard plot.")
        return

    has_user_level = "n_users" in summary.columns
    data_source = "user-level profiles" if has_user_level else "prompt-level profiles"

    n_topics = len(tpc_labels)
    n_metrics = len(metric_cols)

    fig_w = max(14, 1.2 * n_metrics + 3)
    fig_h = max(10, 0.45 * n_topics + 5)

    fig = plt.figure(figsize=(fig_w, fig_h))
    # top 75%: heatmap;  bottom 25%: bar chart
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.24)
    ax_heat = fig.add_subplot(gs[0])
    ax_bar = fig.add_subplot(gs[1])

    n_users_total = summary["n_users"].sum() if has_user_level else None
    title_line2 = (
        f"Proportions from {data_source}  "
        + (f"({n_users_total:,} unique users)" if n_users_total else "")
    )
    # fig.suptitle(
    #    f"Topic demographic summary  (K={best_k}, {len(df_ordered):,} prompts)#\n{title_line2}",
    #    fontsize=12, fontweight="bold", y=0.99,
    # )

    heat_data = summary[metric_cols].copy()

    # normalise each column to [0, 1] for colour mapping
    col_min = heat_data.min()
    col_max = heat_data.max()
    col_range = (col_max - col_min).replace(0, 1)
    heat_norm = (heat_data - col_min) / col_range  # 0-1 per column

    # mask low-n topics
    low_n_mask = summary["n_docs"] < min_n

    cmap = plt.colormaps["RdYlGn"]
    img_data = heat_norm.values  # shape (n_topics, n_metrics)

    for row_i, topic in enumerate(heat_data.index):
        for col_i, metric in enumerate(metric_cols):
            raw = heat_data.loc[topic, metric]
            norm = heat_norm.loc[topic, metric]
            is_nan = np.isnan(raw)
            is_low = low_n_mask.loc[topic]

            if is_nan:
                face_color = "#e0e0e0"
                text_color = "#999999"
                cell_text = "-"
            elif is_low:
                face_color = "#f5f5f5"
                text_color = "#aaaaaa"
                # format raw value
                if metric in ("Mean age", "Mean SES (1-10)"):
                    cell_text = f"{raw:.1f}"
                else:
                    cell_text = f"{raw*100:.0f}%"
            else:
                face_color = cmap(norm)
                # pick readable text colour based on luminance
                r, g, b, _ = face_color
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                text_color = "black" if lum > 0.5 else "white"
                if metric in ("Mean age", "Mean SES (1-10)"):
                    cell_text = f"{raw:.1f}"
                else:
                    cell_text = f"{raw*100:.0f}%"

            rect = plt.Rectangle(
                [col_i, row_i], 1, 1,
                facecolor=face_color, edgecolor="white", linewidth=0.8,
            )
            ax_heat.add_patch(rect)
            ax_heat.text(
                col_i + 0.5, row_i + 0.5, cell_text,
                ha="center", va="center",
                fontsize=max(6, min(9, 110 // n_topics)),
                color=text_color,
            )

    # axis labels
    ax_heat.set_xlim(0, n_metrics)
    ax_heat.set_ylim(0, n_topics)
    ax_heat.set_xticks([i + 0.5 for i in range(n_metrics)])
    ax_heat.set_xticklabels(metric_cols, rotation=40, ha="right", fontsize=8)
    ax_heat.set_yticks([i + 0.5 for i in range(n_topics)])

    # topic labels
    ytick_labels = []
    ytick_colors = []
    for topic in heat_data.index:
        n_d = summary.loc[topic, "n_docs"]
        short = topic[:35] + ("…" if len(topic) > 35 else "")
        if has_user_level:
            n_u = summary.loc[topic, "n_users"]
            ytick_labels.append(f"{short}  ({n_u:,}u / {n_d:,}p)")
        else:
            ytick_labels.append(f"{short}  (n={n_d:,})")
        ytick_colors.append("#aaaaaa" if n_d < min_n else "black")

    ax_heat.set_yticklabels(
        ytick_labels, fontsize=max(6, min(8, 100 // n_topics)))
    for lbl, col in zip(ax_heat.get_yticklabels(), ytick_colors):
        lbl.set_color(col)

    ax_heat.tick_params(axis="both", length=0)
    ax_heat.set_title(
        f"Colour scale: per-column min→max (green = high, red = low)   "
        f"Grey = n < {min_n}",
        fontsize=8, pad=6, color="#555555",
    )

    # bar chart as a f. of size per topic
    topic_names = [f"T{i}" for i in range(n_topics)]
    n_docs_vals = [
        summary.loc[f"T{i}: {tpc_labels[i]}", "n_docs"] for i in range(n_topics)]
    bar_colors = ["#b0b0b0" if v < min_n else "#4c8cbf" for v in n_docs_vals]

    bars = ax_bar.barh(topic_names, n_docs_vals, color=bar_colors, edgecolor="none",
                       height=0.7, label="Prompts")

    if has_user_level:
        n_users_vals = [
            summary.loc[f"T{i}: {tpc_labels[i]}", "n_users"] for i in range(n_topics)]
        user_colors = ["#b0c8e8" if v <
                       min_n else "#1a5c9c" for v in n_users_vals]
        ax_bar.barh(topic_names, n_users_vals, color=user_colors, edgecolor="none",
                    height=0.4, label="Unique users")

    ax_bar.set_xscale("log")
    ax_bar.set_xlabel("Count per topic  (log scale)", fontsize=8)
    ax_bar.tick_params(axis="y", labelsize=7)
    ax_bar.tick_params(axis="x", labelsize=7)
    ax_bar.set_title(
        "Topic size  (wide bar = prompts, narrow bar = unique users)" if has_user_level
        else "Topic size distribution",
        fontsize=9,
    )
    ax_bar.grid(axis="x", alpha=0.3, which="both")
    if has_user_level:
        ax_bar.legend(fontsize=7, loc="lower right")

    for bar, val in zip(bars, n_docs_vals):
        ax_bar.text(
            max(val * 1.05, 1.1), bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", fontsize=6, color="#444444",
        )

    legend_patches = [
        mpatches.Patch(color="#4c8cbf", label=f"n ≥ {min_n}  (prompts)"),
        mpatches.Patch(color="#b0b0b0", label=f"n < {min_n}  (dimmed)"),
    ]
    if has_user_level:
        legend_patches.insert(1, mpatches.Patch(
            color="#1a5c9c", label=f"n ≥ {min_n}  (users)"))
    ax_bar.legend(handles=legend_patches, fontsize=7, loc="lower right")

    fig.savefig(
        (plot_output_dir / "summary_dashboard.png").as_posix(),
        dpi=EXPORT_DPI, bbox_inches="tight",
    )
    plt.close(fig)
    logger.info(
        f"  summary_dashboard.png saved → {plot_output_dir / 'summary_dashboard.png'}")


###############################################################
# HELPERS
###############################################################
def simplify_col(series: pd.Series, col: str) -> pd.Series:
    if col in MULTI_VALUE_COLS:
        series = series.apply(
            lambda x: x.split(";")[0].strip() if isinstance(x, str) else x
        )
    series = series.apply(
        lambda x: (x[:45] + "...") if isinstance(x, str) and len(x) > 45 else x
    )
    return series.fillna("Unknown")


def _palette(unique_vals: list) -> dict:
    base = list(TAB20)
    if not base:
        return {v: "lightgray" for v in unique_vals}
    n_base = len(base)
    return {v: base[i % n_base] for i, v in enumerate(unique_vals)}


###############################################################
# PLOTS
###############################################################

def make_stacked_bar(
    df_plot: pd.DataFrame,
    tpc_labels: list,
    col: str,
    title: str,
    path: str,
) -> None:
    """Stacked bar chart: for each topic, show the proportion of user prompts
    belonging to each demographic value."""
    n_topics = len(tpc_labels)
    values = df_plot[col].astype(str)
    unique_vals = sorted(values.unique())
    color_map = _palette(unique_vals)

    counts = np.zeros((n_topics, len(unique_vals)))
    for _, (tpc, val) in enumerate(zip(df_plot["dominant_topic"], values)):
        if 0 <= tpc < n_topics:
            counts[tpc, unique_vals.index(val)] += 1
    totals = counts.sum(axis=1, keepdims=True)
    props = np.divide(counts, totals, where=totals > 0)

    short_labels = [f"T{i}: {lbl[:18]}" for i, lbl in enumerate(tpc_labels)]

    fig, ax = plt.subplots(figsize=(max(10, n_topics * 0.7), 7))
    bottoms = np.zeros(n_topics)
    for j, val in enumerate(unique_vals):
        ax.bar(
            range(n_topics), props[:, j],
            bottom=bottoms, color=color_map[val], label=val, width=0.7,
        )
        bottoms += props[:, j]

    for i, total in enumerate(totals.ravel()):
        ax.text(i, 1.01, f"n={int(total)}",
                ha="center", va="bottom", fontsize=7)

    ax.set_xticks(range(n_topics))
    ax.set_xticklabels(short_labels, fontsize=7, rotation=45, ha="right")
    ax.set_ylabel("Proportion")
    ax.set_ylim(0, 1.12)
    ax.set_title(title, fontsize=11)
    ax.legend(title=col, bbox_to_anchor=(1.02, 1), loc="upper left",
              fontsize=7, title_fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)


def make_bubble_summary(
    tpc_coords: np.ndarray,
    alphas: np.ndarray,
    tpc_labels: list,
    df_plot: pd.DataFrame,
    col: str,
    title: str,
    path: str,
    cramers_v_val: float = None,
    p_bonf: float = None,
) -> None:
    """Bubble chart with a separate label panel to keep all labels readable. Annotates Cramér's V and Bonferroni-corrected p in the subtitle.
    """
    values = df_plot[col].astype(str)
    unique_vals = sorted(values.unique())
    color_map = _palette(unique_vals)

    majority = {}
    majority_pct = {}
    for tpc_i in range(len(tpc_labels)):
        mask = df_plot["dominant_topic"] == tpc_i
        if mask.any():
            vc = values[mask].value_counts(normalize=True)
            majority[tpc_i] = vc.index[0]
            majority_pct[tpc_i] = vc.iloc[0]
        else:
            majority[tpc_i] = "Unknown"
            majority_pct[tpc_i] = 0.0

    n_topics = len(tpc_labels)
    bubble_scale = 5000

    if n_topics <= 24:
        n_label_cols = 2
    elif n_topics <= 54:
        n_label_cols = 3
    else:
        n_label_cols = 4

    wrap_width = {2: 36, 3: 28, 4: 23}[n_label_cols]
    label_font_size = {2: 9.0, 3: 8.1, 4: 7.3}[n_label_cols]
    marker_size = {2: 24, 3: 22, 4: 20}[n_label_cols]
    wrapped_labels = [textwrap.fill(f"T{i}: {lbl}", width=wrap_width)
                      for i, lbl in enumerate(tpc_labels)]
    line_counts = [w.count("\n") + 1 for w in wrapped_labels]

    line_gap_units = 0.9
    entry_units = [lc + line_gap_units for lc in line_counts]
    col_items = [[] for _ in range(n_label_cols)]
    col_used_units = [0.0] * n_label_cols
    for i, units in enumerate(entry_units):
        col_i = int(np.argmin(col_used_units))
        start_units = col_used_units[col_i]
        col_items[col_i].append((i, start_units, units))
        col_used_units[col_i] += units

    max_col_units = max(col_used_units) if col_used_units else 1.0

    fig_w = {2: 18, 3: 20, 4: 22}[n_label_cols]
    label_block_h = max(3.2, min(15.0, 1.2 + max_col_units * 0.16))
    fig_h = 9.0 + label_block_h

    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(2, 1, height_ratios=[
                          9.0, label_block_h], hspace=0.24)
    ax = fig.add_subplot(gs[0, 0])
    ax_labels = fig.add_subplot(gs[1, 0])
    ax_labels.axis("off")

    for i, (x, y) in enumerate(tpc_coords):
        maj = majority[i]
        pct = majority_pct[i]
        # Edge width encodes how dominant the majority is:
        # thin edge = weak majority (<40%), thick = strong (>60%)
        lw = 0.8 + 2.0 * max(0.0, pct - 0.40) / 0.60
        ax.scatter(
            x, y,
            s=alphas[i] * bubble_scale,
            color=color_map.get(maj, "lightgray"),
            edgecolors="dimgray", linewidths=lw,
            alpha=0.75, zorder=2,
        )
        ax.text(x, y, f"T{i}", ha="center", va="center",
                fontsize=8, fontweight="bold", color="black", zorder=4)

    # Build subtitle with stats if available
    subtitle_parts = []
    if cramers_v_val is not None and not np.isnan(cramers_v_val):
        subtitle_parts.append(f"Cramér's V = {cramers_v_val:.3f}")
    if p_bonf is not None and not np.isnan(p_bonf):
        sig_marker = " ✓" if p_bonf < 0.05 else ""
        subtitle_parts.append(f"p (Bonf.) = {p_bonf:.4f}{sig_marker}")
    if subtitle_parts:
        ax.set_title(title + "\n" + "   ".join(subtitle_parts), fontsize=10)
    else:
        ax.set_title(title, fontsize=11)

    handles = [
        mpatches.Patch(color=color_map[v], label=v)
        for v in unique_vals if v in color_map
    ]
    ax.legend(
        handles=handles,
        title=f"{col}\n(majority per topic)",
        loc="upper right",
        fontsize=6.5, title_fontsize=7.5,
        framealpha=0.9,
    )
    ax.set_xlabel("pyLDAvis dim 1", labelpad=10)
    ax.set_ylabel("pyLDAvis dim 2")
    ax.grid(True, alpha=0.2)

    x_span = max(1e-6, float(np.ptp(tpc_coords[:, 0])))
    y_span = max(1e-6, float(np.ptp(tpc_coords[:, 1])))
    ax.set_xlim(float(np.min(tpc_coords[:, 0])) - 0.18 * x_span,
                float(np.max(tpc_coords[:, 0])) + 0.18 * x_span)
    ax.set_ylim(float(np.min(tpc_coords[:, 1])) - 0.18 * y_span,
                float(np.max(tpc_coords[:, 1])) + 0.18 * y_span)

    ax_labels.set_title("Topic Labels", fontsize=12, pad=12, color="black")
    border = mpatches.Rectangle(
        (0.006, 0.04), 0.988, 0.91,
        fill=False, edgecolor="gray", linewidth=0.9,
        transform=ax_labels.transAxes, clip_on=False,
    )
    ax_labels.add_patch(border)

    top_y = 0.88
    bottom_y = 0.08
    usable_h = max(1e-6, top_y - bottom_y)
    y_scale = usable_h / max(max_col_units, 1e-6)
    col_w = 0.96 / n_label_cols

    for col_i, items in enumerate(col_items):
        x0 = 0.02 + col_i * col_w
        for i, start_units, units in items:
            y0 = top_y - (start_units + units / 2.0) * y_scale
            maj = majority.get(i, "Unknown")
            color = color_map.get(maj, "lightgray")
            ax_labels.scatter(
                [x0], [y0], s=marker_size, color=color,
                edgecolors="dimgray", linewidths=0.6,
                transform=ax_labels.transAxes, clip_on=False,
            )
            ax_labels.text(
                x0 + 0.018, y0, wrapped_labels[i],
                transform=ax_labels.transAxes,
                va="center", ha="left",
                fontsize=label_font_size, color="black",
            )

    fig.subplots_adjust(top=0.96, bottom=0.04)
    fig.savefig(path, dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)


###############################################################
# DOMINANT TOPIC DIAGNOSIS
###############################################################

def diagnose_dominant_topic(
    df_ordered: pd.DataFrame,
    thetas: np.ndarray,
    tpc_labels: list,
    plot_output_dir: Path,
    top_n_examples: int = 10,
    dominant_topic_id: int = 0,
) -> None:
    """
    For each topic, we compute:

    1. prompt_length_stats.csv
       Mean / median / std of prompt length (chars and words) per topic.

    2. theta_confidence_stats.csv
       Mean / median max-theta (= confidence of dominant-topic assignment) per topic. Also records the % of docs where max_theta < 0.20 (very low confidence).

    3. dominant_topic_diagnosis.png
       Four-panel figure:
         A) Prompt length distribution: T0 vs all others (overlapping histograms)
         B) Max-theta (assignment confidence) distribution: T0 vs others
         C) Scatter: prompt length vs max-theta, coloured by topic (T0 highlighted)
         D) Bar chart: mean max-theta per topic, sorted - T0 expected to rank lowest

    4. dominant_topic_examples.csv
       top_n_examples prompts from T0 sorted by LOWEST max-theta (= the most ambiguous documents that ended up there).
    """
    logger.info(f"Diagnosing dominant topic (T{dominant_topic_id}: "
                f"{tpc_labels[dominant_topic_id]}) ...")

    n_docs, n_topics = thetas.shape
    max_theta = thetas.max(axis=1)          # confidence of assignment
    dom_topic = np.argmax(thetas, axis=1)   # same as dominant_topic col

    # prompt length
    prompt_col = "prompt" if "prompt" in df_ordered.columns else None
    if prompt_col:
        df_ordered = df_ordered.copy()
        df_ordered["_prompt_chars"] = df_ordered[prompt_col].fillna(
            "").str.len()
        df_ordered["_prompt_words"] = df_ordered[prompt_col].fillna(
            "").str.split().str.len()

    # per-topic stats
    rows = []
    for t in range(n_topics):
        mask = dom_topic == t
        n = int(mask.sum())
        if n == 0:
            continue
        th = max_theta[mask]
        row = {
            "topic_id": t,
            "topic_label": f"T{t}: {tpc_labels[t]}",
            "n_docs": n,
            "pct_corpus": round(n / n_docs, 4),
            "theta_mean": round(float(th.mean()), 4),
            "theta_median": round(float(np.median(th)), 4),
            "theta_std": round(float(th.std()), 4),
            "theta_lt020_pct": round(float((th < 0.20).mean()), 4),
            "theta_lt033_pct": round(float((th < 0.33).mean()), 4),
        }
        if prompt_col:
            chars = df_ordered.loc[mask, "_prompt_chars"]
            words = df_ordered.loc[mask, "_prompt_words"]
            row.update({
                "prompt_chars_mean": round(float(chars.mean()), 1),
                "prompt_chars_median": round(float(chars.median()), 1),
                "prompt_chars_std": round(float(chars.std()), 1),
                "prompt_words_mean": round(float(words.mean()), 1),
                "prompt_words_median": round(float(words.median()), 1),
            })
        rows.append(row)

    diag_df = pd.DataFrame(rows).sort_values("n_docs", ascending=False)
    diag_path = plot_output_dir / "theta_confidence_stats.csv"
    diag_df.to_csv(diag_path, index=False)
    logger.info(f"  theta_confidence_stats.csv → {diag_path}")

    # log summary
    logger.info("  Assignment confidence (mean max-theta) per topic:")
    for _, r in diag_df.iterrows():
        flag = " ← DOMINANT" if r["topic_id"] == dominant_topic_id else ""
        wlen = f"  words_med={r['prompt_words_median']:.0f}" if prompt_col else ""
        logger.info(
            f"    T{int(r['topic_id']):<3} {r['topic_label'][:35]:<35}  "
            f"n={r['n_docs']:>5}  θ_mean={r['theta_mean']:.3f}  "
            f"<0.20={r['theta_lt020_pct']:.1%}{wlen}{flag}"
        )

    # save low-confidence examples from dominant topic
    if prompt_col:
        df_reset = df_ordered.reset_index(drop=True)

        dom_mask = dom_topic == dominant_topic_id
        dom_idx = np.where(dom_mask)[0]
        dom_theta = max_theta[dom_mask]

        # exclude empty / whitespace-only prompts before sorting
        non_empty = df_reset.loc[dom_idx, prompt_col].fillna(
            "").str.strip() != ""
        non_empty_idx = dom_idx[non_empty.values]
        non_empty_theta = max_theta[non_empty_idx]

        if len(non_empty_idx) == 0:
            logger.warning(
                "  No non-empty prompts in dominant topic - skipping examples export.")
        else:
            # sort ascending theta → most ambiguous first
            order = np.argsort(non_empty_theta)
            sorted_idx = non_empty_idx[order][:top_n_examples]

            examples = df_reset.iloc[sorted_idx][[
                prompt_col, "_prompt_words"]].copy()
            examples["max_theta"] = max_theta[sorted_idx].round(4)
            examples["topic_label"] = f"T{dominant_topic_id}: {tpc_labels[dominant_topic_id]}"
            ex_path = plot_output_dir / "dominant_topic_examples.csv"
            examples[["topic_label", "max_theta", "_prompt_words", prompt_col]].to_csv(
                ex_path, index=False
            )
            logger.info(
                f"  dominant_topic_examples.csv ({min(top_n_examples, len(sorted_idx))} "
                f"most ambiguous non-empty prompts) → {ex_path}"
            )

    # sum figure
    df_plot = df_ordered.reset_index(drop=True)
    if prompt_col and "_prompt_chars" not in df_plot.columns:
        df_plot["_prompt_chars"] = df_plot[prompt_col].fillna("").str.len()
        df_plot["_prompt_words"] = df_plot[prompt_col].fillna(
            "").str.split().str.len()

    dom_mask = dom_topic == dominant_topic_id
    other_mask = ~dom_mask

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Dominant-topic diagnosis - T{dominant_topic_id}: {tpc_labels[dominant_topic_id]}"
        f"  ({dom_mask.sum():,} docs = {dom_mask.mean():.1%} of corpus)",
        fontsize=12, fontweight="bold",
    )

    # Panel A - prompt length distribution
    ax = axes[0, 0]
    if prompt_col:
        chars_dom = df_plot.loc[dom_mask,   "_prompt_chars"].dropna()
        chars_other = df_plot.loc[other_mask, "_prompt_chars"].dropna()
        clip = np.percentile(df_ordered["_prompt_chars"].dropna(), 98)
        bins = np.linspace(0, clip, 50)
        ax.hist(chars_other.clip(upper=clip), bins=bins, alpha=0.55,
                color="#4c8cbf", label=f"Other topics (n={other_mask.sum():,})",
                density=True)
        ax.hist(chars_dom.clip(upper=clip),   bins=bins, alpha=0.65,
                color="#e05c5c", label=f"T{dominant_topic_id} (n={dom_mask.sum():,})",
                density=True)
        ax.axvline(chars_dom.median(),   color="#b03030", lw=1.5, ls="--",
                   label=f"T{dominant_topic_id} median={chars_dom.median():.0f}")
        ax.axvline(chars_other.median(), color="#2a5a8c", lw=1.5, ls=":",
                   label=f"Others median={chars_other.median():.0f}")
        ax.set_xlabel("Prompt length (chars)")
        ax.set_ylabel("Density")
        ax.set_title("A) Prompt length distribution")
        ax.legend(fontsize=7)
    else:
        ax.text(0.5, 0.5, "No 'prompt' column available",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_title("A) Prompt length  [unavailable]")

    # Panel B - max-theta (assignment confidence) distribution
    ax = axes[0, 1]
    theta_dom = max_theta[dom_mask]
    theta_other = max_theta[other_mask]
    bins_th = np.linspace(0, 1, 40)
    ax.hist(theta_other, bins=bins_th, alpha=0.55, color="#4c8cbf",
            label=f"Other topics", density=True)
    ax.hist(theta_dom,   bins=bins_th, alpha=0.65, color="#e05c5c",
            label=f"T{dominant_topic_id}", density=True)
    ax.axvline(np.median(theta_dom),   color="#b03030", lw=1.5, ls="--",
               label=f"T{dominant_topic_id} median={np.median(theta_dom):.2f}")
    ax.axvline(np.median(theta_other), color="#2a5a8c", lw=1.5, ls=":",
               label=f"Others median={np.median(theta_other):.2f}")
    ax.axvline(0.33, color="gray", lw=1.0, ls=":", alpha=0.6,
               label="θ=0.33 (random for 3-topic)")
    ax.set_xlabel("Max theta (assignment confidence)")
    ax.set_ylabel("Density")
    ax.set_title("B) Assignment confidence distribution")
    ax.legend(fontsize=7)

    # Panel C - scatter: prompt length vs max-theta
    ax = axes[1, 0]
    if prompt_col:
        sample_size = min(2000, n_docs)
        idx_sample = np.random.choice(n_docs, sample_size, replace=False)
        chars_all = df_plot["_prompt_chars"].values
        is_dom = dom_mask[idx_sample]
        ax.scatter(
            chars_all[idx_sample][~is_dom],
            max_theta[idx_sample][~is_dom],
            alpha=0.25, s=8, color="#4c8cbf", label="Other topics",
        )
        ax.scatter(
            chars_all[idx_sample][is_dom],
            max_theta[idx_sample][is_dom],
            alpha=0.35, s=8, color="#e05c5c", label=f"T{dominant_topic_id}",
        )
        clip = np.percentile(chars_all, 98)
        ax.set_xlim(0, clip)
        ax.set_ylim(0, 1)
        ax.axhline(0.33, color="gray", lw=0.8, ls=":", alpha=0.6)
        ax.set_xlabel("Prompt length (chars)")
        ax.set_ylabel("Max theta")
        ax.set_title("C) Prompt length vs assignment confidence")
        ax.legend(fontsize=7)
    else:
        ax.text(0.5, 0.5, "No 'prompt' column available",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_title("C) Prompt length vs θ  [unavailable]")

    # Panel D - mean max-theta per topic (bar chart, sorted)
    ax = axes[1, 1]
    diag_sorted = diag_df.sort_values("theta_mean")
    colors = [
        "#e05c5c" if int(r["topic_id"]) == dominant_topic_id else "#4c8cbf"
        for _, r in diag_sorted.iterrows()
    ]
    short_labels = [f"T{int(r['topic_id'])}" for _,
                    r in diag_sorted.iterrows()]
    ax.barh(short_labels, diag_sorted["theta_mean"],
            color=colors, edgecolor="none")
    ax.axvline(diag_sorted["theta_mean"].mean(), color="gray", lw=1.0, ls="--",
               label=f"Mean={diag_sorted['theta_mean'].mean():.3f}")
    ax.set_xlabel("Mean max-theta (assignment confidence)")
    ax.set_title("D) Confidence per topic  (red = dominant topic)")
    ax.legend(fontsize=7)
    ax.tick_params(axis="y", labelsize=7)

    fig.tight_layout()
    fig_path = plot_output_dir / "dominant_topic_diagnosis.png"
    fig.savefig(fig_path.as_posix(), dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"  dominant_topic_diagnosis.png → {fig_path}")
    logger.info("  Diagnosis complete.")


def run_plot_and_stats_loop(
    df_ordered: pd.DataFrame,
    tpc_labels: list,
    tpc_coords: np.ndarray,
    alphas: np.ndarray,
    best_k: int,
    plot_output_dir: Path,
    thetas: np.ndarray = None,
) -> None:
    """Generate all bubble + bar plots and then compute & export all statistics."""

    # filter out uniform-fallback documents (those for which we infer (keyword-based inference) a uniform topic distribution, i.e, max_theta == 1/K)
    logger.info("Filtering out uniform-fallback documents (max_theta ≤ 1/K) ...")
    orig_len = len(df_ordered)
    if thetas is not None:
        K = thetas.shape[1]
        uniform_threshold = (1.0 / K) + 1e-4
        confident_mask = thetas.max(axis=1) > uniform_threshold
        n_uniform = int((~confident_mask).sum())
        n_confident = int(confident_mask.sum())
        logger.info(
            f"  Uniform-fallback filter: {n_uniform:,} docs removed "
            f"(max_theta ≤ {uniform_threshold:.4f}), "
            f"{n_confident:,} docs retained for analysis."
        )
        df_ordered = df_ordered[confident_mask].reset_index(drop=True)
        thetas = thetas[confident_mask]
        # Re-assign dominant_topic on the filtered subset
        dominant_topic = np.argmax(thetas, axis=1)
        df_ordered["dominant_topic"] = dominant_topic
        df_ordered["topic_label"]    = [
            f"T{t}: {tpc_labels[t]}" for t in dominant_topic
        ]
    logger.info("Filtered dataframe has %d rows (vs %d) after uniform-fallback removal.", len(df_ordered), orig_len)
    
    logger.info("Pre-computing Cramér's V for all demographic columns ...")
    stats_lookup: dict[str, dict] = {}
    for col in DEMO_COLS:
        if col not in df_ordered.columns:
            continue
        tmp = df_ordered.copy()
        tmp[col] = simplify_col(tmp[col], col)
        stats_lookup[col] = compute_chi2_stats(tmp, col)

    # Bonferroni denominator = number of valid (non-NaN) tests
    n_tests = sum(1 for r in stats_lookup.values()
                  if not np.isnan(r.get("p_value", np.nan)))

    logger.info("Generating plots ...")
    for col in DEMO_COLS:
        if col not in df_ordered.columns:
            logger.warning(f"  [skip] column '{col}' not found")
            continue

        tmp = df_ordered.copy()
        tmp[col] = simplify_col(tmp[col], col)

        # stacked bar
        fname_bar = f"bar_{col}.png"
        make_stacked_bar(
            tmp, tpc_labels, col,
            f"Topic composition by {col}",
            (plot_output_dir / fname_bar).as_posix(),
        )

        # bubble - pass stats for subtitle annotation
        r = stats_lookup.get(col, {})
        p_raw = r.get("p_value")
        p_bonf = (
            p_raw * n_tests) if (p_raw is not None and not np.isnan(p_raw)) else None
        if p_bonf is not None:
            p_bonf = min(p_bonf, 1.0)

        fname_bub = f"bubble_{col}.png"
        make_bubble_summary(
            tpc_coords, alphas, tpc_labels, tmp, col,
            f"Topic map - majority {col} (K={best_k})",
            (plot_output_dir / fname_bub).as_posix(),
            cramers_v_val=r.get("cramers_v"),
            p_bonf=p_bonf,
        )
        logger.info(f"  {fname_bar}  |  {fname_bub}")

    # full statistical export
    compute_and_export_stats(df_ordered, tpc_labels, plot_output_dir)

    # summary dashboard
    make_summary_dashboard(df_ordered, tpc_labels, plot_output_dir, best_k)

    # dominant-topic diagnosis (only when thetas are available)
    if thetas is not None:
        dominant_id = int(
            pd.Series(np.argmax(thetas, axis=1)).value_counts().idxmax()
        )
        diagnose_dominant_topic(
            df_ordered, thetas, tpc_labels, plot_output_dir,
            dominant_topic_id=dominant_id,
        )


def _align_df_to_thetas(
    df: pd.DataFrame,
    thetas: np.ndarray,
    doc_ids,
) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Align the raw dataframe rows to the order of thetas as stored by the model.
    """
    if doc_ids is not None and len(doc_ids) == len(thetas):
        # Build a lookup: doc_id string → theta row index
        doc_id_strs = [str(d) for d in doc_ids]
        order_df = pd.DataFrame({"id": doc_id_strs,
                                 "_theta_pos": range(len(doc_id_strs))})

        # Merge preserves all columns including user_id
        df_merged = order_df.merge(df, on="id", how="inner")

        n_missing = len(doc_id_strs) - len(df_merged)
        if n_missing > 0:
            logger.warning(
                "  %d doc_ids from the model were not found in the dataframe "
                "(possible ID mismatch). Proceeding with %d matched rows.",
                n_missing, len(df_merged),
            )

        # Reorder thetas to match the merged df order
        theta_positions = df_merged["_theta_pos"].values
        df_ordered = df_merged.drop(
            columns=["_theta_pos"]).reset_index(drop=True)
        thetas_ordered = thetas[theta_positions]

    else:
        # Fallback: no doc_ids available, use positional alignment
        n = min(len(df), len(thetas))
        if len(df) != len(thetas):
            logger.warning(
                "  Length mismatch: dataframe has %d rows, thetas has %d rows. "
                "Trimming both to %d.",
                len(df), len(thetas), n,
            )
        df_ordered = df.iloc[:n].copy().reset_index(drop=True)
        thetas_ordered = thetas[:n]

    # Sanity checks
    n_rows = len(df_ordered)
    n_nan_id = df_ordered["user_id"].isna().sum(
    ) if "user_id" in df_ordered.columns else 0
    logger.info(
        f"  Alignment: {n_rows:,} rows matched  "
        + (f"({n_nan_id:,} NaN user_ids - check for ID type mismatch)" if n_nan_id > 0 else
           f"(user_id intact for all rows)" if "user_id" in df_ordered.columns else
           "(no user_id column)")
    )
    return df_ordered, thetas_ordered


###############################################################
# MAIN PIPELINE
###############################################################

def main() -> None:
    # load data
    logger.info("Loading data ...")
    df = pd.read_csv(DATA_PATH)
    df["id"] = df.index.astype(str)
    if "user_id" in df.columns:
        df["user_id"] = df["user_id"].astype(str)

    # concatenate prompt and llm responses into a single text column for tm
    # , "gemma_4_31B_response", "qwen_3.5_27B_response", "llama_3.3_70B_response"]
    text_cols = ["prompt"]
    df["text"] = df[text_cols].fillna("").astype(str).apply(" ".join, axis=1)
    logger.info(f"  {len(df)} rows loaded")

    # preprocess text for tm
    logger.info("Preprocessing with SimpleTMPreprocessor ...")
    preprocessor = SimpleTMPreprocessor(
        spacy_model="en_core_web_lg",
        spacy_disable=["parser", "ner"],
        valid_pos=["NOUN", "VERB", "ADJ"],
        min_df=1,
        max_df=0.6,
        logger=logger,
        stopword_files=[
            str(Path(__file__).parent / "static/stops/prompt_stops.txt")]
    )
    data = df[["id", "text"]].to_dict(orient="records")

    # optimize K
    logger.info(f"Searching K in [{K_MIN}, {K_MAX}] ...")
    opt_results = LDATopicModel.optimize_num_topics(
        data=data,
        base_path=MODELS_DIR,
        topic_range=range(K_MIN, K_MAX + 1, K_STEP),
        num_iters=NUM_ITERS,
        topn=TOPN_WORDS,
        smoothing_window=3,
        min_doc_words=2,
        n_best=1,
        logger=logger,
        preprocessor=preprocessor,
    )

    logger.info("Coherence scores per K:")
    for k, score in opt_results["scores"]:
        logger.info(f"  K={int(k):2d}  coherence={score:.4f}")

    selected = opt_results["selected"]
    best_k = selected[0]["k"]
    best_coh = selected[0]["mean_coherence"]
    best_model_path = selected[0]["model_path"]
    plot_output_dir = _plot_output_dir_for_k(best_k)
    logger.info(f"Optimal K = {best_k}  (mean coherence = {best_coh:.4f})")

    # load best model and generate topic labels
    logger.info(f"Loading best model from {best_model_path} ...")
    df_prompts = df[["id"]].copy()
    df_prompts["text"] = df["prompt"].fillna("").astype(str)
    lda_best = LDATopicModel.load(best_model_path, corpus=df_prompts)
    lda_best.llm_provider = LLM_PROVIDER
    lda_best.llm_model_type = LLM_MODEL
    lda_best.llm_api_key = LLM_API_KEY
    logger.info(
        f"  [{LLM_PROVIDER}] Generating topic labels for best model (k={best_k})...")

    tm_opt = lda_best.tm
    # results = tm_opt.generate_topic_outputs(task="label", topn=15)
    # tm_opt._tpc_labels = [lbl for _, lbl in sorted(results)]
    tm_opt._tpc_labels = [f"Topic {tpc}" for tpc in range(best_k)]
    (Path(best_model_path) / "TMmodel" / "tpc_labels.txt").write_text(
        "\n".join(tm_opt._tpc_labels), encoding="utf-8"
    )

    thetas = lda_best.get_thetas()  # (n_docs, best_k)

    # align df rows to the theta order stored in doc_ids.json
    # Uses merge (not reindex) so user_id and all columns are preserved
    lda_best.tm._load_doc_ids()
    df_ordered, thetas = _align_df_to_thetas(df, thetas, lda_best.tm._doc_ids)

    dominant_topic = np.argmax(thetas, axis=1)
    df_ordered["dominant_topic"] = dominant_topic
    df_ordered["topic_label"] = [
        f"T{t}: {tm_opt._tpc_labels[t]}" for t in dominant_topic]

    # save topic assignments
    pd.DataFrame([
        {"topic_id": i, "keywords": tm_opt._tpc_labels[i]} for i in range(best_k)
    ]).to_csv(os.path.join(MODELS_DIR, "topic_labels.csv"), index=False)

    df_ordered[["id", "prompt", "dominant_topic", "topic_label"]].to_csv(
        os.path.join(MODELS_DIR, "topic_assignments.csv"), index=False
    )

    logger.info("Topic labels:")
    for i, lbl in enumerate(tm_opt._tpc_labels):
        logger.info(f"  T{i}: {lbl}")

    # pyLDAvis coordinates
    logger.info("Loading pyLDAvis topic coordinates ...")
    tm_opt.load_tpc_coords()
    tpc_coords = np.array(tm_opt._coords)
    alphas = tm_opt.get_alphas()

    # plots + stats + diagnosis
    run_plot_and_stats_loop(
        df_ordered, tm_opt._tpc_labels, tpc_coords, alphas, best_k, plot_output_dir,
        thetas=thetas,
    )

    logger.info(
        f"\nDone. All outputs saved to '{plot_output_dir.as_posix()}/'")


###############################################################
# REGEN PLOTS (re-use existing trained model)
###############################################################
def regen_plots(model_path: str, regen_labels: bool = False) -> None:
    """Regenerate all plots for an already-trained model without re-running the pipeline."""
    model_path = Path(model_path).resolve()
    if not model_path.exists():
        logger.error(f"Model path not found: {model_path}")
        sys.exit(1)

    labels_file = model_path / "TMmodel" / "tpc_labels.txt"
    if not labels_file.exists() and not regen_labels:
        logger.error(
            f"tpc_labels.txt not found in {model_path / 'TMmodel'}. "
            "Run the full pipeline first or use --regen-labels."
        )
        sys.exit(1)

    logger.info(f"Regenerating plots for model: {model_path}")

    logger.info("Loading data ...")
    df = pd.read_csv(DATA_PATH)
    df["id"] = df.index.astype(str)
    if "user_id" in df.columns:
        df["user_id"] = df["user_id"].astype(str)

    df_prompts = df[["id"]].copy()
    df_prompts["text"] = df["prompt"].fillna("").astype(str)

    logger.info("Loading model ...")
    lda = LDATopicModel.load(str(model_path), corpus=df_prompts)

    if regen_labels:
        logger.info(f"  [{LLM_PROVIDER}] Recalculating topic labels ...")
        lda.llm_provider = LLM_PROVIDER
        lda.llm_model_type = LLM_MODEL
        lda.llm_api_key = LLM_API_KEY
        tm = lda.tm
        results = tm.generate_topic_outputs(task="label", topn=10)
        tpc_labels = [lbl for _, lbl in sorted(results)]
        labels_file.write_text("\n".join(tpc_labels), encoding="utf-8")
        logger.info("  Topic labels regenerated and saved")
    else:
        tpc_labels = labels_file.read_text(encoding="utf-8").splitlines()
        tm = lda.tm

    tm._tpc_labels = tpc_labels
    best_k = len(tpc_labels)
    plot_output_dir = _plot_output_dir_for_k(best_k)
    logger.info(f"  K={best_k}, {best_k} topic labels loaded")

    thetas = lda.get_thetas()

    # align df rows to the theta order stored in doc_ids.json
    lda.tm._load_doc_ids()
    df_ordered, thetas = _align_df_to_thetas(df, thetas, lda.tm._doc_ids)

    dominant_topic = np.argmax(thetas, axis=1)
    df_ordered["dominant_topic"] = dominant_topic
    df_ordered["topic_label"] = [
        f"T{t}: {tpc_labels[t]}" for t in dominant_topic]

    logger.info("Loading pyLDAvis topic coordinates ...")
    tm.load_tpc_coords()
    tpc_coords = np.array(tm._coords)
    alphas = tm.get_alphas()

    run_plot_and_stats_loop(
        df_ordered, tpc_labels, tpc_coords, alphas, best_k, plot_output_dir,
        thetas=thetas,
    )

    logger.info(
        f"\nDone. Plots regenerated in '{plot_output_dir.as_posix()}/'")


###############################################################
# ENTRY POINT
###############################################################
if __name__ == "__main__":
    mp.freeze_support()

    parser = argparse.ArgumentParser(description="Topic modeling pipeline")
    parser.add_argument(
        "--regen-plots",
        metavar="MODEL_PATH",
        default=None,
        help="Regenerate plots for an existing model (skips preprocessing and optimisation).",
    )
    parser.add_argument(
        "--regen-labels",
        action="store_true",
        help="With --regen-plots, recompute topic labels before generating plots.",
    )
    args = parser.parse_args()

    if args.regen_plots:
        regen_plots(args.regen_plots, regen_labels=args.regen_labels)
    else:
        main()
