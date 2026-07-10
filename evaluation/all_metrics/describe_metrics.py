"""Produce an overview of the score columns in ``all_metrics_per_user.csv``.

Writes two files next to the input:

  * ``metrics_overview.md``  -- human-readable, grouped by evaluation family
  * ``metrics_overview.csv`` -- one row per numeric column with summary stats
"""

from __future__ import annotations

import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "all_metrics_per_user.csv")
MD_PATH = os.path.join(HERE, "metrics_overview.md")
CSV_PATH = os.path.join(HERE, "metrics_overview.csv")

MODELS = ["qwen-3.5-27B", "llama-3.3-70B", "gemma-4-31B", "gpt-5.5"]

# (label, predicate on column name). First match wins.
FAMILIES = [
    ("Helpfulness (raw)", lambda c: c.startswith("helpfulness_score_")),
    ("Helpfulness (normalized)", lambda c: c.startswith("normalized_helpfulness_")),
    ("Human-likeness", lambda c: c.startswith(("humt_", "std_humt_", "sociot_", "std_sociot_"))),
    ("Sycophancy", lambda c: c.startswith("syco_")),
    ("Linguistic (elfen)", lambda c: c.startswith("ling_")),
    ("Complexity", lambda c: c.startswith("cplx_")),
]


def split_model(col: str):
    """Return (base_metric, model) splitting a trailing ``_<model>`` suffix."""
    for m in MODELS:
        if col.endswith("_" + m):
            return col[: -(len(m) + 1)], m
    return col, None


def family_of(col: str) -> str:
    for label, pred in FAMILIES:
        if pred(col):
            return label
    return "Identifier / demographics"


def build():
    df = pd.read_csv(IN_PATH)

    rows = []
    for col in df.columns:
        fam = family_of(col)
        base, model = split_model(col)
        s = df[col]
        rec = {"column": col, "family": fam, "base_metric": base, "model": model or ""}
        if pd.api.types.is_numeric_dtype(s):
            rec.update(
                n_nonnull=int(s.notna().sum()),
                mean=round(float(s.mean()), 4),
                std=round(float(s.std()), 4),
                min=round(float(s.min()), 4),
                max=round(float(s.max()), 4),
            )
        else:
            rec.update(n_nonnull=int(s.notna().sum()), mean="", std="", min="", max="")
        rows.append(rec)

    stats = pd.DataFrame(rows)
    return df, stats


def write_csv(stats: pd.DataFrame) -> None:
    stats.to_csv(CSV_PATH, index=False)


def write_md(df: pd.DataFrame, stats: pd.DataFrame) -> None:
    numeric = stats[stats["mean"] != ""]
    lines = []
    lines.append("# Metrics overview — `all_metrics_per_user.csv`\n")
    lines.append(
        f"Aggregated to **{df.shape[0]} users** × **{df.shape[1]} columns** "
        f"({len(numeric)} numeric score columns). "
        "Each score is the mean across a user's prompts; the four models are "
        "`qwen-3.5-27B`, `llama-3.3-70B`, `gemma-4-31B`, `gpt-5.5`.\n"
    )

    # Summary table by family.
    lines.append("## Families\n")
    lines.append("| Family | # cols | # base metrics | Per model? |")
    lines.append("|---|---|---|---|")
    order = [
        "Helpfulness (raw)",
        "Helpfulness (normalized)",
        "Human-likeness",
        "Sycophancy",
        "Linguistic (elfen)",
        "Complexity",
        "Identifier / demographics",
    ]
    for fam in order:
        sub = stats[stats["family"] == fam]
        if sub.empty:
            continue
        n_base = sub["base_metric"].nunique()
        per_model = "yes" if sub["model"].replace("", pd.NA).notna().any() else "no"
        lines.append(f"| {fam} | {len(sub)} | {n_base} | {per_model} |")
    lines.append("")

    # Detailed per-family sections.
    def stat_table(sub: pd.DataFrame) -> list[str]:
        out = ["| column | n | mean | std | min | max |", "|---|---|---|---|---|---|"]
        for _, r in sub.iterrows():
            out.append(
                f"| `{r.column}` | {r.n_nonnull} | {r.mean} | {r.std} | {r.min} | {r.max} |"
            )
        return out

    # Small families: list every column with stats.
    for fam in ["Helpfulness (raw)", "Helpfulness (normalized)", "Human-likeness", "Sycophancy"]:
        sub = numeric[numeric["family"] == fam]
        if sub.empty:
            continue
        lines.append(f"## {fam} ({len(sub)} columns)\n")
        lines += stat_table(sub)
        lines.append("")

    # Large families: list base metrics once (they repeat ×4 models).
    for fam in ["Linguistic (elfen)", "Complexity"]:
        sub = numeric[numeric["family"] == fam]
        if sub.empty:
            continue
        bases = sorted(sub["base_metric"].unique())
        lines.append(
            f"## {fam} ({len(sub)} columns = {len(bases)} metrics × 4 models)\n"
        )
        lines.append(
            "Column pattern: `"
            + bases[0]
            + "_<model>`. Per-column stats are in `metrics_overview.csv`. "
            "Base metrics:\n"
        )
        lines += [f"- `{b}`" for b in bases]
        lines.append("")

    # Demographic / identifier columns (names only).
    demo = stats[stats["family"] == "Identifier / demographics"]
    if not demo.empty:
        lines.append(f"## Identifier / demographics ({len(demo)} columns)\n")
        lines.append(", ".join(f"`{c}`" for c in demo["column"]))
        lines.append("")

    with open(MD_PATH, "w") as f:
        f.write("\n".join(lines))


def main() -> None:
    df, stats = build()
    write_csv(stats)
    write_md(df, stats)
    print(f"Wrote {MD_PATH}")
    print(f"Wrote {CSV_PATH}  ({len(stats)} columns described)")


if __name__ == "__main__":
    main()
