"""Aggregate the consolidated metrics per user.

Prompt ids look like ``u110p1`` where the number between ``u`` and ``p`` is the
user id. This collapses all prompts belonging to a user into a single row:

  * numeric score/metric columns   -> mean across the user's prompts
  * per-user demographic columns   -> first value (constant within a user)
  * per-prompt text (prompt / responses / input) -> dropped

Result is written next to the input as ``all_metrics_per_user.csv``.
"""

from __future__ import annotations

import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(HERE, "all_metrics.csv")
OUT_PATH = os.path.join(HERE, "all_metrics_per_user.csv")


def extract_user(prompt_id: str) -> str:
    """u110p1 -> u110 (the part before the prompt number)."""
    m = re.match(r"(u\d+)p\d+", str(prompt_id))
    if not m:
        raise ValueError(f"Unexpected id format: {prompt_id!r}")
    return m.group(1)


def aggregate() -> pd.DataFrame:
    df = pd.read_csv(IN_PATH)
    df.insert(0, "user", df["id"].map(extract_user))

    # Drop per-prompt text columns that cannot be meaningfully aggregated.
    # Only the *raw* model output columns start with ``responses_``; score
    # columns like ``helpfulness_score_responses_<model>`` merely contain the
    # word and must be kept.
    text_cols = [
        c
        for c in df.columns
        if c in {"id", "prompt", "input"}
        or c.startswith("responses_")
        or c.endswith("_trunc")
    ]
    df = df.drop(columns=text_cols)

    numeric_cols = df.select_dtypes("number").columns.tolist()
    meta_cols = [c for c in df.columns if c not in numeric_cols and c != "user"]

    agg = {c: "mean" for c in numeric_cols}
    agg.update({c: "first" for c in meta_cols})  # demographics: constant per user

    out = df.groupby("user", as_index=False).agg(agg)
    # Keep user + demographics first, metrics after.
    out = out[["user"] + meta_cols + numeric_cols]
    return out


def main() -> None:
    out = aggregate()
    out.to_csv(OUT_PATH, index=False)
    print(f"Wrote {out.shape[0]} users x {out.shape[1]} columns -> {OUT_PATH}")


if __name__ == "__main__":
    main()
