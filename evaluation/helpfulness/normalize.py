import argparse
import os

import pandas as pd


DEFAULT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(DEFAULT_DIR, "sampled_data_responses_with_helpfulness.csv")
DEFAULT_OUTPUT = os.path.join(DEFAULT_DIR, "sampled_data_responses_with_normalized_helpfulness.csv")

RESPONSE_COLUMNS = [
    "responses_qwen-3.5-27B",
    "responses_llama-3.3-70B",
    "responses_gemma-4-31B",
    "responses_gpt-5.5",
]

def zscore(series: pd.Series) -> pd.Series:
    """Standardize a column to mean 0, std 1 across the dataset.

    Uses the sample standard deviation (ddof=1), matching pandas' default.
    If the column has zero variance, returns all zeros to avoid division by NaN.
    """
    std = series.std()
    if std == 0 or pd.isna(std):
        return series - series.mean()
    return (series - series.mean()) / std


def main():
    parser = argparse.ArgumentParser(
        description="Add per-column z-score normalized helpfulness scores to the CSV."
    )
    parser.add_argument(
        "input_csv",
        nargs="?",
        default=DEFAULT_INPUT,
        help=f"Input CSV with helpfulness_score_* columns. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "output_csv",
        nargs="?",
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path. Default: {DEFAULT_OUTPUT}",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    score_columns = [f"helpfulness_score_{col}" for col in RESPONSE_COLUMNS]
    missing = [col for col in score_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required helpfulness score columns: {missing}")

    for response_column in RESPONSE_COLUMNS:
        score_column = f"helpfulness_score_{response_column}"
        df[f"normalized_helpfulness_{response_column}"] = zscore(df[score_column])

    df.to_csv(args.output_csv, index=False)
    print(f"Saved normalized CSV to {args.output_csv}")


if __name__ == "__main__":
    main()
