"""Build a prompt-level, SES-balanced sample from the language technologies survey.

Reads data_Elisa/survey-language-technologies.csv (one row per user, prompt1..prompt10
columns) and writes data_Elisa/sampled_dataset.csv (one row per prompt), with:
  - social_class derived from ses (1-3 low, 4-7 middle, 8-10 upper)
  - id formatted as "u{user_id}p{prompt_number}"
  - classes balanced by randomly downsampling to the smallest class size
"""

import csv
import random

INPUT_PATH = "data_Elisa/survey-language-technologies.csv"
OUTPUT_PATH = "data_Elisa/sampled_dataset.csv"
NUM_PROMPTS = 10
RANDOM_SEED = 42

SES_METADATA_COLUMNS = {"prompt1", "prompt2", "prompt3", "prompt4", "prompt5",
                         "prompt6", "prompt7", "prompt8", "prompt9", "prompt10"}


def social_class(ses: str):
    try:
        value = int(ses)
    except ValueError:
        return None
    if 1 <= value <= 3:
        return "low"
    if 4 <= value <= 7:
        return "middle"
    if 8 <= value <= 10:
        return "upper"
    return None


def main():
    with open(INPUT_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        base_columns = [c for c in reader.fieldnames if c not in SES_METADATA_COLUMNS and c != "id"]
        rows = list(reader)

    disaggregated = {"low": [], "middle": [], "upper": []}
    for row in rows:
        sclass = social_class(row["ses"])
        if sclass is None:
            continue
        for i in range(1, NUM_PROMPTS + 1):
            prompt_text = row[f"prompt{i}"].strip()
            if not prompt_text:
                continue
            new_row = {"id": f"u{row['id']}p{i}", "prompt": prompt_text, "social_class": sclass}
            for col in base_columns:
                new_row[col] = row[col]
            disaggregated[sclass].append(new_row)

    balanced_n = min(len(v) for v in disaggregated.values())
    print(f"Class sizes before balancing: { {k: len(v) for k, v in disaggregated.items()} }")
    print(f"Sampling {balanced_n} instances per class")

    rng = random.Random(RANDOM_SEED)
    sampled = []
    for sclass, sclass_rows in disaggregated.items():
        sampled.extend(rng.sample(sclass_rows, balanced_n))
    rng.shuffle(sampled)

    output_columns = ["id", "prompt", "ses", "social_class"] + \
        [c for c in base_columns if c != "ses"]

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_columns)
        writer.writeheader()
        writer.writerows(sampled)

    print(f"Wrote {len(sampled)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
