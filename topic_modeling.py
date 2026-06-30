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
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from seal.preprocessing import SimpleTMPreprocessor
from seal.topic_modeling import LDATopicModel

warnings.filterwarnings("ignore")

###############################################################
# CONFGIGURATION
###############################################################
DATA_PATH  = "data/Elisa_prompts_sample_open_models_clean.csv"
OUTPUT_DIR = "data/output/plots"
MODELS_DIR = "data/output/models"
K_MIN, K_MAX, K_STEP = 15, 51, 5
NUM_ITERS   = 1500
TOPN_WORDS  = 15
RANDOM_SEED = 42
LLM_PROVIDER = "openai"
LLM_MODEL    = "gpt-5.4-nano-2026-03-17"
LLM_API_KEY  = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
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
        logging.FileHandler(os.path.join(OUTPUT_DIR, "pipeline.log"), mode="w"),
    ],
)
logger = logging.getLogger("topic_pipeline")


def _plot_output_dir_for_k(k: int) -> Path:
    out_dir = Path(OUTPUT_DIR) / f"k_{k}_topics"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def main() -> None:
    
    # load data
    logger.info("Loading data ...")
    df = pd.read_csv(DATA_PATH)
    df["id"] = df.index.astype(str)
    if "user_id" in df.columns:
        df["user_id"] = df["user_id"].astype(str)
        
    # concatante prompt and llm responses into a single text column for tm 
    text_cols = ["prompt", "gemma_4_31B_response", "qwen_3.5_27B_response", "llama_3.3_70B_response"]
    df["text"] = df[text_cols].fillna("").astype(str).apply(" ".join, axis=1)
    logger.info(f"  {len(df)} rows loaded")

    # preprocess text for tm
    logger.info("Preprocessing with SimpleTMPreprocessor ...")
    preprocessor = SimpleTMPreprocessor(
        spacy_model="en_core_web_lg",
        spacy_disable=["parser", "ner"],
        valid_pos=["NOUN", "VERB", "ADJ"],
        min_df=1,  # small corpus: accept all terms
        max_df=0.6,
        logger=logger,
        stopword_files=[str(Path(__file__).parent / "static/stops/prompt_stops.txt")]
    )
    data = df[["id", "text"]].to_dict(orient="records")

    # optimize (try) K
    logger.info(f"Searching K in [{K_MIN}, {K_MAX}] ...")
    opt_results = LDATopicModel.optimize_num_topics(
        data=data,
        base_path=MODELS_DIR,
        topic_range=range(K_MIN, K_MAX + 1, K_STEP),
        num_iters=NUM_ITERS,
        topn=TOPN_WORDS,
        smoothing_window=3,
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
    
    # for the generation of the labels we only use the prompts (not the concatenated text with LLM responses)
    df_prompts = df[["id"]].copy()
    df_prompts["text"] = df["prompt"].fillna("").astype(str)
    lda_best = LDATopicModel.load(best_model_path, corpus=df_prompts)
    lda_best.llm_provider   = LLM_PROVIDER
    lda_best.llm_model_type = LLM_MODEL
    lda_best.llm_api_key    = LLM_API_KEY
    logger.info(f"  [{LLM_PROVIDER}] Generating topic labels for best model (k={best_k})...")
    
    tm_opt = lda_best.tm
    results = tm_opt.generate_topic_outputs(task="label", topn=10)  
    
    # results = [f"Topic {tpc}" for tpc in range(best_k)]  # placeholder labels
    # tm_opt._tpc_labels = results
    # (Path(best_model_path) / "TMmodel" / "tpc_labels.txt").write_text(
    #     "\n".join(tm_opt._tpc_labels), encoding="utf-8"
    #         )    
    tm_opt._tpc_labels = [lbl for _, lbl in sorted(results)]
    (Path(best_model_path) / "TMmodel" / "tpc_labels.txt").write_text(
       "\n".join(tm_opt._tpc_labels), encoding="utf-8"
           )    

    thetas = lda_best.get_thetas()  # (n_docs, best_k)

    # align df rows to the theta order stored in doc_ids.json
    lda_best.tm._load_doc_ids()
    doc_ids = lda_best.tm._doc_ids
    if doc_ids is not None and len(doc_ids) == len(thetas):
        df_ordered = df.set_index("id").reindex([str(i) for i in doc_ids]).reset_index()
    else:
        n = min(len(df), len(thetas))
        if len(df) != len(thetas):
            logger.warning(
                "Length mismatch between corpus rows (%d) and thetas (%d); trimming both to %d rows.",
                len(df), len(thetas), n,
            )
        df_ordered = df.iloc[:n].copy().reset_index(drop=True)
        thetas = thetas[:n]

    dominant_topic = np.argmax(thetas, axis=1)
    df_ordered["dominant_topic"] = dominant_topic
    df_ordered["topic_label"] = [f"T{t}: {tm_opt._tpc_labels[t]}" for t in dominant_topic]

    # save outputs
    pd.DataFrame([
        {"topic_id": i, "keywords": tm_opt._tpc_labels[i]} for i in range(best_k)
    ]).to_csv(os.path.join(MODELS_DIR, "topic_labels.csv"), index=False)

    df_ordered[["id", "prompt", "dominant_topic", "topic_label"]].to_csv(
        os.path.join(MODELS_DIR, "topic_assignments.csv"), index=False
    )

    logger.info("Topic labels:")
    for i, lbl in enumerate(tm_opt._tpc_labels):
        logger.info(f"  T{i}: {lbl}")

    # Place each document at the theta-weighted centroid of the pyLDAvis topic coords
    logger.info("Loading pyLDAvis topic coordinates ...")
    tm_opt.load_tpc_coords()
    tpc_coords = np.array(tm_opt._coords)
    alphas = tm_opt.get_alphas()

    # weighted centroid per document: pos_d = sum_k theta[d,k] * coord[k]
    doc_positions = thetas @ tpc_coords
    df_ordered["doc_x"] = doc_positions[:, 0]
    df_ordered["doc_y"] = doc_positions[:, 1]

    # generate plots
    logger.info("Generating plots ...")

    for col in DEMO_COLS:
        if col not in df_ordered.columns:
            logger.warning(f"  [skip] column '{col}' not found")
            continue
        tmp = df_ordered.copy()
        tmp[col] = simplify_col(tmp[col], col)

        # stacked bars: topic by demographic value
        fname_bar = f"bar_{col}.png"
        make_stacked_bar(
            tmp, tm_opt._tpc_labels,
            col, f"Topic composition by {col}",
            (plot_output_dir / fname_bar).as_posix(),
        )
        logger.info(f"  {fname_bar}")

        # bubble summary: one bubble per topic, coloured by majority value
        fname_bub = f"bubble_{col}.png"
        make_bubble_summary(
            tpc_coords, alphas, tm_opt._tpc_labels,
            tmp, col,
            f"Topic map - majority {col} (K={best_k})",
            (plot_output_dir / fname_bub).as_posix(),
        )
        logger.info(f"  {fname_bub}")

    logger.info(f"\nDone. All plots saved to '{plot_output_dir.as_posix()}/'")


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


def make_stacked_bar(
    df_plot: pd.DataFrame,
    tpc_labels: list,
    col: str,
    title: str,
    path: str,
) -> None:
    """Stacked bar chart: for each topic, we show the proportion of user prompts belonging to each demographic value."""
    n_topics = len(tpc_labels)
    values   = df_plot[col].astype(str)
    unique_vals = sorted(values.unique())
    color_map   = _palette(unique_vals)

    # proportion matrix: rows = topics, cols = demographic values
    counts = np.zeros((n_topics, len(unique_vals)))
    for _, (tpc, val) in enumerate(zip(df_plot["dominant_topic"], values)):
        if 0 <= tpc < n_topics:
            counts[tpc, unique_vals.index(val)] += 1
    totals = counts.sum(axis=1, keepdims=True)
    props  = np.divide(counts, totals, where=totals > 0)

    short_labels = [f"T{i}: {lbl[:18]}" for i, lbl in enumerate(tpc_labels)]

    fig, ax = plt.subplots(figsize=(max(10, n_topics * 0.7), 7))
    bottoms = np.zeros(n_topics)
    for j, val in enumerate(unique_vals):
        ax.bar(
            range(n_topics), props[:, j],
            bottom=bottoms, color=color_map[val], label=val, width=0.7,
        )
        bottoms += props[:, j]

    # annotate doc counts per topic
    for i, total in enumerate(totals.ravel()):
        ax.text(i, 1.01, f"n={int(total)}", ha="center", va="bottom", fontsize=7)

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
) -> None:
    """Bubble chart with a separate label panel to keep all labels readable."""
    values = df_plot[col].astype(str)
    unique_vals = sorted(values.unique())
    color_map = _palette(unique_vals)

    # majority value per topic
    majority = {}
    for tpc_i in range(len(tpc_labels)):
        mask = df_plot["dominant_topic"] == tpc_i
        if mask.any():
            majority[tpc_i] = values[mask].mode().iloc[0]
        else:
            majority[tpc_i] = "Unknown"

    n_topics = len(tpc_labels)
    bubble_scale = 5000

    # Two-row layout: map on top + full label catalog below.
    if n_topics <= 24:
        n_label_cols = 2
    elif n_topics <= 54:
        n_label_cols = 3
    else:
        n_label_cols = 4

    wrap_width = {2: 36, 3: 28, 4: 23}[n_label_cols]
    label_font_size = {2: 9.0, 3: 8.1, 4: 7.3}[n_label_cols]
    marker_size = {2: 24, 3: 22, 4: 20}[n_label_cols]
    wrapped_labels = [textwrap.fill(f"T{i}: {lbl}", width=wrap_width) for i, lbl in enumerate(tpc_labels)]
    line_counts = [w.count("\n") + 1 for w in wrapped_labels]

    # Build column packing using true label heights (in abstract units).
    line_gap_units = 0.9
    entry_units = [lc + line_gap_units for lc in line_counts]
    col_items = [[] for _ in range(n_label_cols)]
    col_used_units = [0.0] * n_label_cols
    for i, units in enumerate(entry_units):
        # Greedy balancing: place each label in the currently shortest column.
        col_i = int(np.argmin(col_used_units))
        start_units = col_used_units[col_i]
        col_items[col_i].append((i, start_units, units))
        col_used_units[col_i] += units

    max_col_units = max(col_used_units) if col_used_units else 1.0

    fig_w = {2: 18, 3: 20, 4: 22}[n_label_cols]
    label_block_h = max(3.2, min(15.0, 1.2 + max_col_units * 0.16))
    fig_h = 9.0 + label_block_h

    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(2, 1, height_ratios=[9.0, label_block_h], hspace=0.24)
    ax = fig.add_subplot(gs[0, 0])
    ax_labels = fig.add_subplot(gs[1, 0])
    ax_labels.axis("off")

    for i, (x, y) in enumerate(tpc_coords):
        maj = majority[i]
        ax.scatter(
            x, y,
            s=alphas[i] * bubble_scale,
            color=color_map.get(maj, "lightgray"),
            edgecolors="dimgray", linewidths=1.2,
            alpha=0.75, zorder=2,
        )
        # topic index centred inside bubble
        ax.text(x, y, f"T{i}", ha="center", va="center",
                fontsize=8, fontweight="bold", color="black", zorder=4)

    handles = [
        mpatches.Patch(color=color_map[v], label=v)
        for v in unique_vals if v in color_map
    ]
    ax.legend(
        handles=handles,
        title=f"{col}\n(majority per topic)",
        loc="upper right",
        fontsize=6.5,
        title_fontsize=7.5,
        framealpha=0.9,
    )
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("pyLDAvis dim 1", labelpad=10)
    ax.set_ylabel("pyLDAvis dim 2")
    ax.grid(True, alpha=0.2)

    # Keep margins around bubbles.
    x_span = max(1e-6, float(np.ptp(tpc_coords[:, 0])))
    y_span = max(1e-6, float(np.ptp(tpc_coords[:, 1])))
    ax.set_xlim(float(np.min(tpc_coords[:, 0])) - 0.18 * x_span, float(np.max(tpc_coords[:, 0])) + 0.18 * x_span)
    ax.set_ylim(float(np.min(tpc_coords[:, 1])) - 0.18 * y_span, float(np.max(tpc_coords[:, 1])) + 0.18 * y_span)

    # Label catalog panel: all labels below the map, split into columns.
    ax_labels.set_title("Topic Labels", fontsize=12, pad=12, color="black")
    border = mpatches.Rectangle(
        (0.006, 0.04), 0.988, 0.91,
        fill=False,
        edgecolor="gray",
        linewidth=0.9,
        transform=ax_labels.transAxes,
        clip_on=False,
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

            ax_labels.scatter([x0], [y0], s=marker_size, color=color, edgecolors="dimgray", linewidths=0.6,
                              transform=ax_labels.transAxes, clip_on=False)
            ax_labels.text(
                x0 + 0.018,
                y0,
                wrapped_labels[i],
                transform=ax_labels.transAxes,
                va="center",
                ha="left",
                fontsize=label_font_size,
                color="black",
            )

    fig.subplots_adjust(top=0.96, bottom=0.04)
    fig.savefig(path, dpi=EXPORT_DPI, bbox_inches="tight")
    #fig.savefig(Path(path).with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


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
            "Run the full pipeline first to generate labels or use --regen-labels."
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
        logger.info(f"  [{LLM_PROVIDER}] Recalculating topic labels before regenerating plots ...")
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

    lda.tm._load_doc_ids()
    doc_ids = lda.tm._doc_ids
    if doc_ids is not None and len(doc_ids) == len(thetas):
        df_ordered = df.set_index("id").reindex([str(i) for i in doc_ids]).reset_index()
    else:
        n = min(len(df), len(thetas))
        if len(df) != len(thetas):
            logger.warning(
                "Length mismatch between corpus rows (%d) and thetas (%d); trimming to %d.",
                len(df), len(thetas), n,
            )
        df_ordered = df.iloc[:n].copy().reset_index(drop=True)
        thetas = thetas[:n]

    dominant_topic = np.argmax(thetas, axis=1)
    df_ordered["dominant_topic"] = dominant_topic
    df_ordered["topic_label"] = [f"T{t}: {tpc_labels[t]}" for t in dominant_topic]

    logger.info("Loading pyLDAvis topic coordinates ...")
    tm.load_tpc_coords()
    tpc_coords = np.array(tm._coords)
    alphas = tm.get_alphas()

    logger.info("Generating plots ...")
    for col in DEMO_COLS:
        if col not in df_ordered.columns:
            logger.warning(f"  [skip] column '{col}' not found")
            continue
        tmp = df_ordered.copy()
        tmp[col] = simplify_col(tmp[col], col)

        fname_bar = f"bar_{col}.png"
        make_stacked_bar(
            tmp, tpc_labels, col, f"Topic composition by {col}",
            (plot_output_dir / fname_bar).as_posix(),
        )
        logger.info(f"  {fname_bar}")

        fname_bub = f"bubble_{col}.png"
        make_bubble_summary(
            tpc_coords, alphas, tpc_labels, tmp, col,
            f"Topic map – majority {col} (K={best_k})",
            (plot_output_dir / fname_bub).as_posix(),
        )
        logger.info(f"  {fname_bub}")

    logger.info(f"\nDone. Plots regenerated in '{plot_output_dir.as_posix()}/'")


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
