from seal.topic_modeling import LDATopicModel
from seal.preprocessing import SimpleTMPreprocessor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import logging
import os
from pathlib import Path
import sys
import warnings
import multiprocessing as mp
from functools import lru_cache
from huggingface_hub import hf_hub_download  # type: ignore
from scipy import sparse
import ast
import matplotlib
matplotlib.use("Agg")

warnings.filterwarnings("ignore")

###############################################################
# CONFIGURATION
###############################################################
# we use the complete dtset for training
HF_REPO_ID = "MilaNLProc/survey-language-technologies"
HF_FILENAME = "survey-language-technologies.csv"
SES_DATA_PATH = "data_Elisa/sampled_dataset.csv"        # plots only use this
OUTPUT_DIR = "data/output/ses_plots"
MODELS_DIR = "data/output/models"
K_MIN, K_MAX, K_STEP = 5, 51, 5
NUM_ITERS = 1500
TOPN_WORDS = 15
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-5.4-nano-2026-03-17"
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
EXPORT_DPI = 320
TOP_N_COMMON = 2
TOP_N_REPRESENTATIVE = 5
TOP_N_SHORTLIST = 20

SES_CLASS_ORDER = ["low", "middle", "upper"]
SES_CLASS_LABELS = {"low": "Lower class",
                    "middle": "Middle class", "upper": "Upper class"}
TAB20 = plt.colormaps["tab20"].colors

plt.rcParams.update({
    "font.size": 22,
    "axes.titlesize": 26,
    "axes.labelsize": 24,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "legend.fontsize": 20,
    "legend.title_fontsize": 22,
})

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(
            OUTPUT_DIR, "pipeline.log"), mode="w"),
    ],
)
logger = logging.getLogger("ses_topic_pipeline")


def _plot_output_dir_for_model(best_model_path: str) -> Path:
    out_dir = Path(OUTPUT_DIR) / Path(best_model_path).name
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


###############################################################
# DATA LOADING
###############################################################
@lru_cache(maxsize=1)
def load_full_dataset() -> pd.DataFrame:
    """Download dataset from hugging face and reshape it into the long form used by the rest of the pipeline: one row per prompt, with user_id + prompt columns."""
    logger.info(
        f"Downloading {HF_REPO_ID}/{HF_FILENAME} from the Hugging Face Hub ...")
    local_path = hf_hub_download(
        repo_id=HF_REPO_ID, filename=HF_FILENAME, repo_type="dataset"
    )
    df_wide = pd.read_csv(local_path)

    prompt_cols = [f"prompt{i}" for i in range(1, 11)]
    id_vars = [c for c in df_wide.columns if c not in prompt_cols]
    df = df_wide.melt(
        id_vars=id_vars, value_vars=prompt_cols, var_name="_prompt_col", value_name="prompt"
    )
    df = df.dropna(subset=["prompt"]).reset_index(drop=True)
    df = df.drop_duplicates(
        subset=["prompt"], keep="first").reset_index(drop=True)
    prompt_num = df["_prompt_col"].str.removeprefix("prompt").astype(int)
    df = df.drop(columns=["_prompt_col"]).rename(columns={"id": "user_id"})
    # use as id the same one used in the sample: uXXXpY where XXX = user_id and Y = prompt number
    df["id"] = "u" + df["user_id"].astype(str) + "p" + prompt_num.astype(str)
    logger.info(
        f"Loaded {len(df):,} prompts from {df['user_id'].nunique():,} respondents.")
    return df


###############################################################
# STEP 1: TRAIN (OR REUSE) THE BEST MODEL
###############################################################
def get_or_train_model() -> tuple[int, str]:
    """Return (best_k, best_model_path), training only if no optimization
    results exist yet in MODELS_DIR."""
    opt_results_path = Path(MODELS_DIR) / "optimization_results.json"

    if opt_results_path.exists():
        import json
        opt_results = json.loads(opt_results_path.read_text(encoding="utf-8"))
        selected = opt_results["selected"]
        best_k = selected[0]["k"]
        best_model_path = selected[0]["model_path"]
        logger.info(
            f"Found existing optimization_results.json -> reusing best model "
            f"K={best_k} ({best_model_path}). Skipping training."
        )
        return best_k, best_model_path

    logger.info("No optimization_results.json found; training from scratch ...")
    df = load_full_dataset().copy()
    df["text"] = df["prompt"].fillna("").astype(str)

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
    selected = opt_results["selected"]
    best_k = selected[0]["k"]
    best_model_path = selected[0]["model_path"]
    logger.info(
        f"Optimal K = {best_k}  (mean coherence = {selected[0]['mean_coherence']:.4f})")
    return best_k, best_model_path


def get_or_generate_labels(
    lda_best: LDATopicModel,
    best_model_path: str,
    force: bool = False,
) -> list[str]:
    """Return topic labels, generating them via LLM only if not already on disk
    (or unconditionally when force=True)."""
    labels_file = Path(best_model_path) / "TMmodel" / "tpc_labels.txt"
    if labels_file.exists() and not force:
        labels = labels_file.read_text(encoding="utf-8").splitlines()
        logger.info(
            f"Found existing tpc_labels.txt ({len(labels)} labels) - skipping labeling.")
        return labels

    logger.info(f"  [{LLM_PROVIDER}] Generating topic labels ...")
    lda_best.llm_provider = LLM_PROVIDER
    lda_best.llm_model_type = LLM_MODEL
    lda_best.llm_api_key = LLM_API_KEY
    results = lda_best.tm.generate_topic_outputs(task="label", topn=TOPN_WORDS)
    labels = [lbl for _, lbl in sorted(results)]
    labels_file.write_text("\n".join(labels), encoding="utf-8")
    return labels


###############################################################
# STEP 2: ALIGN FULL-DATASET THETAS TO DOMINANT TOPICS
###############################################################
def _align_df_to_thetas(
    df: pd.DataFrame,
    thetas: np.ndarray,
    doc_ids,
) -> tuple[pd.DataFrame, np.ndarray]:
    """Align raw dataframe rows to the theta order stored by the model."""
    if doc_ids is not None and len(doc_ids) == len(thetas):
        doc_id_strs = [str(d) for d in doc_ids]
        order_df = pd.DataFrame(
            {"id": doc_id_strs, "_theta_pos": range(len(doc_id_strs))})
        df_merged = order_df.merge(df, on="id", how="inner")
        theta_positions = df_merged["_theta_pos"].values
        df_ordered = df_merged.drop(
            columns=["_theta_pos"]).reset_index(drop=True)
        thetas_ordered = thetas[theta_positions]
    else:
        n = min(len(df), len(thetas))
        df_ordered = df.iloc[:n].copy().reset_index(drop=True)
        thetas_ordered = thetas[:n]
    return df_ordered, thetas_ordered


def load_topic_assignments(
    best_model_path: str, regen_labels: bool = False
) -> tuple[pd.DataFrame, list[str], list[list[str]]]:
    """Load the trained model, compute per-prompt dominant topic assignments
    for the full training dataset, and return them keyed by row id.

    Prompt dominant topic = argmax(theta) for each prompt, after filtering out any prompts whose max(theta) is below the uniform-fallback threshold (1/K + 1e-4). The returned dataframe has columns ["id", "dominant_topic"].
    """
    logger.info(
        "Loading full dataset & model to compute topic assignments ...")
    df = load_full_dataset().copy()

    df_prompts = df[["id"]].copy()
    df_prompts["text"] = df["prompt"].fillna("").astype(str)

    lda = LDATopicModel.load(best_model_path, corpus=df_prompts)
    labels = get_or_generate_labels(lda, best_model_path, force=regen_labels)
    topic_words = lda.get_topic_keys()

    thetas = lda.get_thetas()
    lda.tm._load_doc_ids()

    lda.tm.get_most_representative_per_tpc(
        sparse.csr_matrix(thetas), topn=thetas.shape[0], get_text=False
    )
    s3_theta_rank_by_id: dict[tuple[str, int], int] = {
        (str(doc_id), k): rank
        for k, docs in enumerate(lda.tm._most_representative_docs)
        for rank, (doc_id, _text, _theta) in enumerate(docs)
    }

    df_ordered, thetas = _align_df_to_thetas(df, thetas, lda.tm._doc_ids)

    # drop uniform-fallback docs
    K = thetas.shape[1]
    uniform_threshold = (1.0 / K) + 1e-4
    confident_mask = thetas.max(axis=1) > uniform_threshold
    n_uniform = int((~confident_mask).sum())
    logger.info(
        f"  Uniform-fallback filter: dropping {n_uniform:,} docs "
        f"(max_theta <= {uniform_threshold:.4f})"
    )
    df_ordered = df_ordered[confident_mask].reset_index(drop=True)
    thetas = thetas[confident_mask]

    df_ordered["dominant_topic"] = np.argmax(thetas, axis=1)
    df_ordered["topic_prob"] = thetas.max(axis=1)
    df_ordered["topic_composition"] = [
        {i: round(float(p), 4) for i, p in enumerate(row)} for row in thetas
    ]
    # Lower rank = more representative of its dominant topic per S3+theta scoring; if None, the query didn't pass the candidate filters.
    df_ordered["s3_theta_rank"] = [
        s3_theta_rank_by_id.get((doc_id, topic))
        for doc_id, topic in zip(df_ordered["id"], df_ordered["dominant_topic"])
    ]
    return df_ordered[
        ["id", "user_id", "prompt", "dominant_topic", "topic_prob",
         "topic_composition", "s3_theta_rank"]
    ], labels, topic_words


###############################################################
# STEP 2b: REPRESENTATIVE USERS/QUERIES + COUNTS PER TOPIC
###############################################################
def _assign_user_primary_topics(df_assignments: pd.DataFrame) -> pd.DataFrame:
    """Assign each user to its primary topic (their majority dominant_topic across queries; ties broken by mean topic_prob).
    """
    def _pick(g: pd.DataFrame) -> pd.Series:
        counts = g["dominant_topic"].value_counts()
        candidates = counts[counts == counts.max()].index
        if len(candidates) == 1:
            topic = candidates[0]
        else:
            topic = (
                g[g["dominant_topic"].isin(candidates)]
                .groupby("dominant_topic")["topic_prob"].mean()
                .idxmax()
            )
        topic_rows = g[g["dominant_topic"] == topic]
        return pd.Series({
            "primary_topic": topic,
            "primary_share": len(topic_rows) / len(g),
            "primary_conf": topic_rows["topic_prob"].mean(),
        })

    return (
        df_assignments.groupby("user_id", as_index=False)
        .apply(_pick, include_groups=False)
    )


def extract_topic_representatives(
    df_assignments: pd.DataFrame,
    tpc_labels: list[str],
    top_n: int = TOP_N_REPRESENTATIVE,
) -> pd.DataFrame:
    """For each topic, return the number of distinct users and queries assigned
    to it, plus its most representative queries and users. Queries are ranked by s3_theta_rank, falling back to raw theta for docs that lack a rank .
    """
    user_topics = _assign_user_primary_topics(df_assignments)

    records = []
    for t in sorted(df_assignments["dominant_topic"].unique()):
        sub = df_assignments[df_assignments["dominant_topic"] == t]
        sub_users = user_topics[user_topics["primary_topic"] == t]

        top_queries = sub.sort_values(
            ["s3_theta_rank", "topic_prob"], ascending=[True, False], na_position="last"
        ).head(top_n)
        top_users = sub_users.sort_values(
            ["primary_share", "primary_conf"], ascending=False
        ).head(top_n)

        records.append({
            "topic_id": t,
            "topic_label": tpc_labels[t] if t < len(tpc_labels) else "",
            "n_queries": len(sub),
            "n_users": len(sub_users),
            "representative_queries": " ||| ".join(top_queries["prompt"].astype(str)),
            "representative_users": ", ".join(top_users["user_id"].astype(str)),
        })

    df_repr = pd.DataFrame(records).sort_values(
        "topic_id").reset_index(drop=True)
    logger.info(
        f"Computed representative users/queries for {len(df_repr)} topics.")
    return df_repr


###############################################################
# STEP 3: MAP THE SAMPLED SES DATASET ONTO THOSE ASSIGNMENTS
###############################################################
def load_ses_sample_with_topics(df_assignments: pd.DataFrame) -> pd.DataFrame:
    """Load sample and attach each sampled prompt's dominant_topic + SES bucket."""
    logger.info(f"Loading SES sample from {SES_DATA_PATH} ...")
    df_sample = pd.read_csv(SES_DATA_PATH)

    n_before = len(df_sample)
    df_sample = df_sample[df_sample["social_class"].isin(
        SES_CLASS_ORDER)].copy()

    df_merged = df_sample.merge(
        df_assignments[["id", "dominant_topic",
                        "topic_composition", "s3_theta_rank"]],
        on="id", how="inner",
    )
    logger.info(
        f"  {len(df_merged):,} / {n_before} sampled prompts matched to a topic assignment."
    )

    df_merged["social_class_label"] = df_merged["social_class"].map(
        SES_CLASS_LABELS)
    return df_merged[
        ["id", "prompt", "social_class", "social_class_label", "dominant_topic",
         "topic_composition", "s3_theta_rank"]
    ]


###############################################################
# STEP 4: SELECT THE TOPICS MOST COMMON ACROSS ALL 3 SES CLASSES
###############################################################
def select_common_topics(
    df_merged: pd.DataFrame, n_topics: int, top_n: int = TOP_N_COMMON
) -> tuple[list[int], pd.DataFrame]:
    """Return the top_n topics shared by all three SES classes. Each topic gets a score: out of its share in the working, middle, and upper class prompts, we keep only the smallest of the three numbers. A topic that is big in one class but almost not present in another will score low, even if it looks big on average, so ranking topics by this score (instead of by their average share) picks out topics that show up in all three classes, not ones popular in just one. Also returns the full class x topic proportion table.
    """
    class_topic = pd.crosstab(
        df_merged["social_class"], df_merged["dominant_topic"], normalize="index"
    ).reindex(index=SES_CLASS_ORDER, columns=range(n_topics), fill_value=0.0)

    min_share = class_topic.min(axis=0)
    common_topic_ids = min_share.sort_values(
        ascending=False).head(top_n).index.tolist()

    logger.info(f"Top {top_n} topics common across all 3 SES classes:")
    for t in common_topic_ids:
        shares = "  ".join(
            f"{SES_CLASS_LABELS[c]}={class_topic.loc[c, t]:.1%}" for c in SES_CLASS_ORDER)
        logger.info(f"    T{t}:  {shares}  (min share={min_share[t]:.1%})")

    return common_topic_ids, class_topic


###############################################################
# STEP 4b: REPRESENTATIVE QUERIES PER TOPIC, BROKEN DOWN BY SES CLASS
###############################################################
_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _latex_escape(text: str) -> str:
    return "".join(_LATEX_ESCAPES.get(ch, ch) for ch in text)


def _rank_candidates(
    df_merged: pd.DataFrame, topic_id: int, social_class: str, top_n: int
) -> pd.DataFrame:
    """Rank a (topic, SES class) cell's queries by s3_theta_rank, falling back to that topic's raw theta for docs that lack a rank."""
    sub = df_merged[
        (df_merged["dominant_topic"] == topic_id) & (
            df_merged["social_class"] == social_class)
    ].copy()
    sub["_theta_t"] = sub["topic_composition"].apply(
        lambda comp: comp.get(topic_id, 0.0))
    return sub.sort_values(
        ["s3_theta_rank", "_theta_t"], ascending=[True, False], na_position="last"
    ).head(top_n)


def get_representative_queries_by_class(
    df_merged: pd.DataFrame, topic_ids: list[int], top_n: int = 3
) -> dict[int, dict[str, list[str]]]:
    """For each topic in topic_ids, return its top_n most representative
    queries within each SES class. See _rank_candidates for the ranking."""
    return {
        t: {
            cls: _rank_candidates(df_merged, t, cls, top_n)["prompt"].tolist()
            for cls in SES_CLASS_ORDER
        }
        for t in topic_ids
    }


def export_representative_shortlist(
    df_merged: pd.DataFrame,
    topic_ids: list[int],
    tpc_labels: list[str],
    shortlist_n: int = TOP_N_SHORTLIST,
) -> pd.DataFrame:
    """Build a wider ranked shortlist of candidate queries per topic x SES."""
    records = []
    for t in topic_ids:
        label = tpc_labels[t] if t < len(tpc_labels) else ""
        for cls in SES_CLASS_ORDER:
            top = _rank_candidates(df_merged, t, cls, shortlist_n)
            for rank, (_, row) in enumerate(top.iterrows(), start=1):
                records.append({
                    "topic_id": t,
                    "topic_label": label,
                    "social_class": SES_CLASS_LABELS[cls],
                    "rank": rank,
                    "s3_theta_rank": row["s3_theta_rank"],
                    "theta": round(row["_theta_t"], 4),
                    "query": row["prompt"],
                })
    return pd.DataFrame(records)


def make_representative_queries_latex(
    df_merged: pd.DataFrame,
    topic_ids: list[int],
    tpc_labels: list[str],
    topic_words: list[list[str]] | None = None,
    top_n: int = 3,
    n_words: int = 10,
) -> str:
    """Build one LaTeX table per topic: columns = SES classes, rows = that class's top_n most representative queries for the topic."""
    reps = get_representative_queries_by_class(
        df_merged, topic_ids, top_n=top_n)
    n_cols = len(SES_CLASS_ORDER)

    blocks = []
    for t in topic_ids:
        label = tpc_labels[t] if t < len(tpc_labels) else ""
        per_class = reps[t]

        lines = [
            r"\begin{table}[ht]",
            r"\centering",
            r"\small",
            r"\begin{tabular}{" + "p{4.3cm}" * n_cols + "}",
            r"\toprule",
        ]
        if topic_words is not None and t < len(topic_words):
            words = ", ".join(topic_words[t][:n_words])
            header_text = _latex_escape(f"{label}: {words}")
            lines.append(
                rf"\multicolumn{{{n_cols}}}{{c}}{{\textbf{{{header_text}}}}} \\")
            lines.append(r"\midrule")
        lines.append(" & ".join(SES_CLASS_LABELS[c]
                     for c in SES_CLASS_ORDER) + r" \\")
        lines.append(r"\midrule")
        for i in range(top_n):
            row = []
            for c in SES_CLASS_ORDER:
                queries = per_class[c]
                row.append(_latex_escape(
                    queries[i]) if i < len(queries) else "")
            lines.append(" & ".join(row) + r" \\[4pt]")
        lines += [
            r"\bottomrule",
            r"\end{tabular}",
            rf"\caption{{Representative queries for Topic {t} ({_latex_escape(label)}) by SES class.}}",
            rf"\label{{tab:repr_queries_topic{t}}}",
            r"\end{table}",
        ]
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + "\n"


###############################################################
# PLOTS
###############################################################
def make_topic_level_bar(
    df_merged: pd.DataFrame,
    tpc_labels: list[str],
    common_topic_ids: list[int],
    path: str,
) -> None:
    """x-axis = topics, each bar stacked by the proportion of prompts from
    each of the 3 SES classes (proportions normalized within topic)."""
    n_topics = len(tpc_labels)
    color_map = {c: TAB20[i % len(TAB20)]
                 for i, c in enumerate(SES_CLASS_ORDER)}

    counts = np.zeros((n_topics, len(SES_CLASS_ORDER)))
    for tpc, cls in zip(df_merged["dominant_topic"], df_merged["social_class"]):
        if 0 <= tpc < n_topics:
            counts[tpc, SES_CLASS_ORDER.index(cls)] += 1
    totals = counts.sum(axis=1, keepdims=True)
    props = np.divide(counts, totals, where=totals > 0)

    short_labels = [f"T{i}: {lbl}" for i, lbl in enumerate(tpc_labels)]

    fig, ax = plt.subplots(figsize=(max(14, n_topics * 1.2), 9))
    bottoms = np.zeros(n_topics)
    for j, cls in enumerate(SES_CLASS_ORDER):
        ax.bar(
            range(n_topics), props[:, j],
            bottom=bottoms, color=color_map[cls], label=SES_CLASS_LABELS[cls], width=0.7,
        )
        bottoms += props[:, j]

    for i, total in enumerate(totals.ravel()):
        ax.text(i, 1.01, f"{int(total)}",
                ha="center", va="bottom", fontsize=16)

    ax.set_xticks(range(n_topics))
    ax.set_xticklabels(short_labels, fontsize=18, rotation=45, ha="right")
    for i, tick in enumerate(ax.get_xticklabels()):
        if i in common_topic_ids:
            tick.set_color("crimson")
            tick.set_fontweight("bold")

    ax.set_ylabel("Proportion of prompts")
    ax.set_ylim(0, 1.12)
    ax.set_title(
        "Topic composition by SES class",
        fontsize=26,
    )
    ax.legend(title="SES class", bbox_to_anchor=(
        1.02, 1), loc="upper left", fontsize=20)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)


def make_reverse_bar(
    class_topic: pd.DataFrame,
    tpc_labels: list[str],
    common_topic_ids: list[int],
    path: str,
    top_n_per_class: int = 8,
) -> None:
    """x-axis = SES class, each bar stacked by the top-N topics within that
    class (proportions normalized within class), plus an 'other' bucket.
    Common topics are hatched so they're easy to spot across all 3 bars."""
    top_topics_per_class = set()
    for cls in SES_CLASS_ORDER:
        top_topics_per_class.update(class_topic.loc[cls].sort_values(
            ascending=False).head(top_n_per_class).index)
    shown_topics = sorted(top_topics_per_class)

    color_map = {t: TAB20[i % len(TAB20)] for i, t in enumerate(shown_topics)}

    fig, ax = plt.subplots(figsize=(16, 10))
    x = np.arange(len(SES_CLASS_ORDER))
    bottoms = np.zeros(len(SES_CLASS_ORDER))

    for t in shown_topics:
        vals = class_topic[t].reindex(SES_CLASS_ORDER).values
        hatch = "//" if t in common_topic_ids else None
        edge = "crimson" if t in common_topic_ids else "white"
        lw = 2.0 if t in common_topic_ids else 0.6
        ax.bar(
            x, vals, bottom=bottoms, color=color_map[t],
            label=f"T{t}: {tpc_labels[t]}", width=0.6,
            hatch=hatch, edgecolor=edge, linewidth=lw,
        )
        bottoms += vals

    other = 1.0 - bottoms
    ax.bar(x, other, bottom=bottoms, color="lightgray",
           label="All other topics", width=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels([SES_CLASS_LABELS[c]
                       for c in SES_CLASS_ORDER], fontsize=20)
    ax.set_ylabel("Proportion of prompts")
    ax.set_ylim(0, 1.02)
    ax.set_title(
        f"Topic composition by SES class",
        fontsize=26,
    )
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=16)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=EXPORT_DPI, bbox_inches="tight")
    plt.close(fig)


###############################################################
# MAIN PIPELINE
###############################################################
def main(model_path: str | None = None, regen_labels: bool = False) -> None:
    if model_path:
        logger.info(
            f"Using explicitly provided model path: {model_path} (skipping training/optimization).")
        best_model_path = model_path
    else:
        _, best_model_path = get_or_train_model()

    df_assignments, tpc_labels, tpc_words = load_topic_assignments(
        best_model_path, regen_labels=regen_labels)
    best_k = len(tpc_labels)
    df_merged = load_ses_sample_with_topics(df_assignments)

    common_topic_ids, class_topic = select_common_topics(
        df_merged, n_topics=best_k)

    plot_output_dir = _plot_output_dir_for_model(best_model_path)

    df_merged["topic_label"] = df_merged["dominant_topic"].map(
        lambda t: tpc_labels[t] if t < len(tpc_labels) else ""
    )
    df_merged[["id", "prompt", "topic_composition", "dominant_topic", "topic_label"]].to_csv(
        plot_output_dir / "query_topic_composition.csv", index=False
    )

    df_repr = extract_topic_representatives(df_assignments, tpc_labels)
    print(df_repr)
    df_repr.to_csv(plot_output_dir / "topic_representatives.csv", index=False)

    common_df = pd.DataFrame({
        "topic_id": common_topic_ids,
        "topic_label": [tpc_labels[t] for t in common_topic_ids],
        **{SES_CLASS_LABELS[c]: [class_topic.loc[c, t] for t in common_topic_ids] for c in SES_CLASS_ORDER},
    })
    common_df.to_csv(plot_output_dir / "common_topics_ses.csv", index=False)

    repr_queries_latex = make_representative_queries_latex(
        df_merged, common_topic_ids, tpc_labels, topic_words=tpc_words, top_n=TOP_N_SHORTLIST
    )
    (plot_output_dir / "representative_queries_by_ses.tex").write_text(repr_queries_latex, encoding="utf-8")

    shortlist_df = export_representative_shortlist(
        df_merged, common_topic_ids, tpc_labels)
    shortlist_df.to_csv(
        plot_output_dir / "representative_queries_shortlist.csv", index=False)

    make_topic_level_bar(
        df_merged, tpc_labels, common_topic_ids,
        (plot_output_dir / "bar_ses_topic_level.png").as_posix(),
    )
    make_reverse_bar(
        class_topic, tpc_labels, common_topic_ids,
        (plot_output_dir / "bar_ses_reverse_class_level.png").as_posix(),
    )

    labels_str = ", ".join(f"T{t}: {tpc_labels[t]}" for t in common_topic_ids)
    logger.info(
        f"\nDone. Topics most common across all 3 SES classes: {labels_str}")
    logger.info(f"All outputs saved to '{plot_output_dir.as_posix()}/'")


if __name__ == "__main__":
    mp.freeze_support()

    parser = argparse.ArgumentParser(description="SES topic modeling pipeline")
    parser.add_argument(
        "--regen-plots",
        metavar="MODEL_PATH",
        default=None,
        help="Regenerate outputs for an existing model (skips training/optimisation).",
    )
    parser.add_argument(
        "--regen-labels",
        action="store_true",
        help="Recompute topic labels via LLM even if tpc_labels.txt already exists.",
    )
    parser.add_argument(
        "--add_topic_info",
        action="store_true",
        default=False,
        help="Add topic info.",
    )
    parser.add_argument(
        "--path_metrics",
        type=str,
        default="evaluation/all_metrics/all_metrics.csv",
        help="Path to the metrics CSV file.",
    )
    parser.add_argument(
        "--path_topics",
        type=str,
        default="evaluation/topic_modeling/ses_plots/model_15_topics",
        help="Path to the topics CSV file.",
    )
    parser.add_argument(
        "--topic-ids",
        type=int,
        nargs="+",
        default=[0, 3],
        help="Dominant topic ids to keep when adding topic info to the metrics CSV.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.4,
        help="Minimum topic_composition score (for any of --topic-ids) required to keep a row in the thresholded export.",
    )
    args = parser.parse_args()

    if args.add_topic_info:

        df_metrics = pd.read_csv(args.path_metrics)
        df_topics = pd.read_csv(args.path_topics)
        topic_ids = args.topic_ids
        threshold = args.threshold
        suffix = "_".join(str(int(t)) for t in topic_ids)
        print(len(df_metrics), len(df_topics))

        df_metrics_topics = pd.merge(
            df_metrics, df_topics, how="left", on="id")
        print(len(df_metrics_topics))

        df_metrics_topics["topic_composition"] = df_metrics_topics["topic_composition"].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else {}
        )

        # keep all
        all_topics = \
            df_metrics_topics[df_metrics_topics.dominant_topic.isin(
                topic_ids)]
        all_topics.to_csv(
            f"evaluation/all_metrics/all_metrics_topic_{suffix}.csv", index=False)
        print(len(all_topics))

        # keep all larger than threshold
        above_threshold = pd.Series(False, index=df_metrics_topics.index)
        for tid in topic_ids:
            above_threshold |= df_metrics_topics.topic_composition.apply(
                lambda d, tid=int(tid): d.get(tid, 0)
            ) > threshold
        larger_than_threshold = \
            df_metrics_topics[
                df_metrics_topics.dominant_topic.isin(
                    topic_ids) & above_threshold
            ]
        larger_than_threshold.to_csv(
            f"evaluation/all_metrics/all_metrics_topic_{suffix}_larger_than_threshold.csv", index=False)
        print(len(larger_than_threshold))

    main(model_path=args.regen_plots, regen_labels=args.regen_labels)
