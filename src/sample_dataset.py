"""Build a prompt-level, SES-balanced sample from the language technologies survey.

Reads data/survey-language-technologies.csv (one row per user, prompt1..prompt10
columns) and writes data/sampled_dataset.csv (one row per prompt), with:
  - the survey disaggregated so each prompt gets its own row
  - duplicate prompts (repeated across users) dropped, keeping the first occurrence
  - social_class derived from ses (1-3 low, 4-7 middle, 8-10 upper)
  - id formatted as "u{user_id}p{prompt_number}"
  - classes balanced by randomly downsampling to the smallest class size
"""

import pandas as pd

INPUT_PATH = "data/survey-language-technologies.csv"
OUTPUT_PATH = "data/sampled_dataset.csv"
NUM_PROMPTS = 10
RANDOM_SEED = 42

PROMPT_COLUMNS = [f"prompt{i}" for i in range(1, NUM_PROMPTS + 1)]


def social_class(ses):
    try:
        value = int(ses)
    except (TypeError, ValueError):
        return None
    if 1 <= value <= 3:
        return "low"
    if 4 <= value <= 7:
        return "middle"
    if 8 <= value <= 10:
        return "upper"
    return None


def main():
    df = pd.read_csv(INPUT_PATH, dtype=str, keep_default_na=False)
    base_columns = [c for c in df.columns if c not in PROMPT_COLUMNS and c != "id"]

    # Preserve the survey's row order so that, after disaggregating and
    # dropping duplicate prompts, the kept occurrence is the first one.
    df = df.reset_index(names="_orig_order")

    disaggregated = df.melt(
        id_vars=["id", "_orig_order"] + base_columns,
        value_vars=PROMPT_COLUMNS,
        var_name="prompt_num",
        value_name="prompt",
    )
    disaggregated["prompt"] = disaggregated["prompt"].str.strip()
    disaggregated["prompt_num"] = disaggregated["prompt_num"].str.replace("prompt", "").astype(int)
    disaggregated = disaggregated[disaggregated["prompt"] != ""]
    disaggregated = disaggregated.sort_values(["_orig_order", "prompt_num"])

    disaggregated = disaggregated.drop_duplicates(subset="prompt", keep="first")

    disaggregated["id"] = "u" + disaggregated["id"] + "p" + disaggregated["prompt_num"].astype(str)
    disaggregated["social_class"] = disaggregated["ses"].apply(social_class)
    disaggregated = disaggregated.dropna(subset=["social_class"])

    class_sizes = disaggregated["social_class"].value_counts()
    balanced_n = class_sizes.min()
    print(f"Class sizes before balancing: {class_sizes.to_dict()}")
    print(f"Sampling {balanced_n} instances per class")

    sampled = (
        disaggregated.groupby("social_class", group_keys=False)
        .sample(n=balanced_n, random_state=RANDOM_SEED)
        .sample(frac=1, random_state=RANDOM_SEED)
        .reset_index(drop=True)
    )

    output_columns = ["id", "prompt", "ses", "social_class"] + \
        [c for c in base_columns if c != "ses"]
    sampled = sampled[output_columns]

    sampled.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(sampled)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
