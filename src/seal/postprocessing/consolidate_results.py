"""Consolidate all evaluation metric CSVs into a single wide table.

Every evaluation CSV under ``seal/evaluation`` is keyed by ``id`` (a
respondent+prompt identifier such as ``u487p5``), which is unique within each
file. The consolidated output therefore has one row per ``id`` and one column
per (metric, model), joined with an outer merge on ``id``.

Only the richest version of each evaluation is used (supersets win); redundant
subset files are skipped:

    helpfulness  -> sampled_data_responses_with_normalized_helpfulness.csv
    human_likeness -> human_likeness_all_models.csv (humt / sociot metrics)
    linguistic   -> elfen_features_<model>.csv           (one per model)
    complexity   -> responses_<model>_complexity.csv     (one per model)
    sycophancy   -> sampled_dataset_responses_clean_<variant>.csv (0/1 flags)

Result is written to ``seal/evaluation/all_metrics/all_metrics.csv``.
"""

from __future__ import annotations

import glob
import os
import re

import pandas as pd

EVAL_DIR = "/mount/arbeitsdaten53/projekte/simtech/doenmeea/SEAL/seal/evaluation"
OUT_PATH = os.path.join(EVAL_DIR, "all_metrics", "all_metrics.csv")

# Canonical model labels. Note: the complexity files use "llama-3.5-70B" in
# their filename, which is the same model everything else calls "llama-3.3-70B".
CANONICAL_MODELS = ["qwen-3.5-27B", "llama-3.3-70B", "gemma-4-31B", "gpt-5.5"]

# Complexity columns that are not metrics (bookkeeping / redundant response text).
COMPLEXITY_DROP = {"source_column", "row_index", "input"}

# Sycophancy: three per-dimension files, each holding binary 0/1 flags in
# columns named ``responses_<model>_<variant>``.
SYCOPHANCY_VARIANTS = {
    "framing": "sampled_dataset_responses_clean_framing.csv",
    "validation": "sampled_dataset_responses_clean_validation.csv",
    "indirectness": "sampled_dataset_responses_clean_indirectness.csv",
}


def canonical_model(filename: str) -> str:
    """Map any per-model filename to a single canonical model label."""
    name = filename.lower()
    if "qwen" in name:
        return "qwen-3.5-27B"
    if "llama" in name:
        return "llama-3.3-70B"
    if "gemma" in name:
        return "gemma-4-31B"
    if "gpt" in name:
        return "gpt-5.5"
    raise ValueError(f"Cannot determine model from filename: {filename}")


def _merge_per_model(base: pd.DataFrame, pattern: str, prefix: str,
                     drop: set[str] | None = None) -> pd.DataFrame:
    """Merge a set of per-model CSVs, suffixing each metric with the model."""
    drop = drop or set()
    for path in sorted(glob.glob(pattern)):
        model = canonical_model(os.path.basename(path))
        df = pd.read_csv(path)
        keep = [c for c in df.columns if c == "id" or c not in drop]
        df = df[keep]
        rename = {c: f"{prefix}_{c}_{model}" for c in df.columns if c != "id"}
        df = df.rename(columns=rename)
        base = base.merge(df, on="id", how="outer")
    return base


def _merge_sycophancy(base: pd.DataFrame) -> pd.DataFrame:
    """Merge the three sycophancy dimensions as ``syco_<variant>_<model>``."""
    for variant, fname in SYCOPHANCY_VARIANTS.items():
        df = pd.read_csv(os.path.join(EVAL_DIR, "sycophancy", fname))
        flag_cols = [c for c in df.columns if c.endswith(f"_{variant}")]
        sub = df[["id"] + flag_cols].copy()
        rename = {}
        for c in flag_cols:  # c == responses_<model>_<variant>
            model = canonical_model(c)
            # Coerce stray non-numeric values (e.g. "Question:") to NaN.
            sub[c] = pd.to_numeric(sub[c], errors="coerce")
            rename[c] = f"syco_{variant}_{model}"
        sub = sub.rename(columns=rename)
        base = base.merge(sub, on="id", how="outer")
    return base


def consolidate() -> pd.DataFrame:
    # Base: normalized helpfulness carries the shared demographics/prompt/response
    # columns plus per-model helpfulness_score_* and normalized_helpfulness_*.
    base = pd.read_csv(
        os.path.join(
            EVAL_DIR,
            "helpfulness",
            "sampled_data_responses_with_normalized_helpfulness.csv",
        )
    )

    # Human-likeness: take only the humt / sociot metric columns (incl. std_*),
    # since the demographics/response columns already live in the base.
    hl = pd.read_csv(
        os.path.join(EVAL_DIR, "human_likeness", "human_likeness_all_models.csv")
    )
    hl_cols = [c for c in hl.columns if c == "id" or re.search(r"humt|sociot", c)]
    base = base.merge(hl[hl_cols], on="id", how="outer")

    # Linguistic (elfen features) and complexity: one file per model.
    base = _merge_per_model(
        base, os.path.join(EVAL_DIR, "linguistic", "elfen_features_*.csv"), "ling"
    )
    base = _merge_per_model(
        base,
        os.path.join(EVAL_DIR, "complexity", "responses_*_complexity.csv"),
        "cplx",
        drop=COMPLEXITY_DROP,
    )

    # Sycophancy (binary 0/1 flags per dimension).
    base = _merge_sycophancy(base)
    return base


def main() -> None:
    df = consolidate()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {df.shape[0]} rows x {df.shape[1]} columns -> {OUT_PATH}")


if __name__ == "__main__":
    main()
