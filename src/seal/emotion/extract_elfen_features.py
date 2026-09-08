#!/usr/bin/env python3
"""Extract ELFeN linguistic features for generated LLM responses.

Two input shapes are supported:

1. A wide "sampled dataset" CSV where every model gets its own response column,
   e.g. ``responses_qwen-3.5-27B``, ``responses_llama-3.3-70B``, ... .  ELFeN
   features are extracted independently for each model column and written to one
   CSV per model, each containing the ``id`` column plus the ELFeN feature
   columns (e.g. ``elfen_features_qwen-3.5-27B.csv``).

2. The legacy per-run results file (JSON/JSONL/CSV) with a single ``response``
   column produced by ``query_api_LLM_batch.py``.

Use ``--response-prefix`` (default ``responses_``) to control which wide columns
are treated as model responses.  If no such columns are found the script falls
back to the single-response behaviour.
"""

import argparse
import copy
import json
import pathlib
from typing import Any, Dict, Iterable, List, Optional

import polars as pl
from elfen.extractor import Extractor
from elfen.configs.extractor_config import CONFIG_ALL

# Feature selection: extract the full ``emotion`` area
FULL_AREAS = ("emotion",)


def build_feature_config() -> Dict[str, Any]:
    """Return an ELFeN config restricted to the emotion area and selected norms.

    Starts from ELFeN's ``CONFIG_ALL`` (so feature names always match the
    installed version) and keeps only the ``emotion`` area in full.
    """
    config = copy.deepcopy(CONFIG_ALL)
    all_features = config["features"]

    selected: Dict[str, List[str]] = {}
    for area in FULL_AREAS:
        if area in all_features:
            selected[area] = list(all_features[area])

    config["features"] = selected
    return config


def _records_from_mapping(mapping: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for prompt_id, payload in mapping.items():
        if isinstance(payload, dict):
            response = payload.get(
                "response", payload.get("answer", payload.get("text", ""))
            )
            attempts = payload.get("attempts")
        else:
            response = payload
            attempts = None
        yield {
            "prompt_id": str(prompt_id),
            "response": "" if response is None else str(response),
            "attempts": attempts,
        }


def load_generated_responses(results_file: pathlib.Path) -> pl.DataFrame:
    """Load generated responses from JSON/JSONL/CSV into prompt_id/response rows.

    Supported JSON shapes:
    - [{"prompt_id": "answer"}]
    - [{"prompt_id": {"response": "answer", "attempts": 2}}]
    - {"prompt_id": "answer"}
    - {"prompt_id": {"response": "answer", "attempts": 2}}
    - [{"prompt_id": "...", "response": "...", "attempts": 1}]
    """
    suffix = results_file.suffix.lower()
    records: List[Dict[str, Any]] = []

    if suffix == ".csv":
        df = pl.read_csv(results_file)
        if "response" not in df.columns:
            for candidate in (
                "generated_response",
                "answer",
                "text",
                "output",
            ):
                if candidate in df.columns:
                    df = df.rename({candidate: "response"})
                    break
        if "prompt_id" not in df.columns:
            df = df.with_row_index("prompt_id")
        return df.with_columns(
            pl.col("response").cast(pl.Utf8, strict=False).fill_null("")
        )

    text = results_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"No content found in {results_file}")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = [
            json.loads(line) for line in text.splitlines() if line.strip()
        ]

    if isinstance(parsed, dict):
        records.extend(_records_from_mapping(parsed))
    elif isinstance(parsed, list):
        for item in parsed:
            if not isinstance(item, dict):
                continue
            if "prompt_id" in item and "response" in item:
                records.append(
                    {
                        "prompt_id": str(item["prompt_id"]),
                        "response": (
                            ""
                            if item.get("response") is None
                            else str(item.get("response"))
                        ),
                        "attempts": item.get("attempts"),
                    }
                )
            elif len(item) == 1:
                records.extend(_records_from_mapping(item))
            else:
                prompt_id = (
                    item.get("id") or item.get("custom_id") or item.get("key")
                )
                response = (
                    item.get("response")
                    or item.get("answer")
                    or item.get("text")
                    or item.get("output")
                )
                if prompt_id is not None:
                    records.append(
                        {
                            "prompt_id": str(prompt_id),
                            "response": (
                                "" if response is None else str(response)
                            ),
                            "attempts": item.get("attempts"),
                        }
                    )
    else:
        raise ValueError(
            f"Unsupported generated-response format in {results_file}"
        )

    if not records:
        raise ValueError(
            f"No generated responses could be parsed from {results_file}"
        )

    df = pl.DataFrame(records)
    if "attempts" not in df.columns:
        df = df.with_columns(pl.lit(None).alias("attempts"))
    return df.with_columns(
        pl.col("response").cast(pl.Utf8, strict=False).fill_null("")
    )


def _run_elfen(
    df: pl.DataFrame,
    text_column: str,
    model: str,
) -> pl.DataFrame:
    """Run the ELFeN pipeline on ``text_column`` and return the enriched frame.

    Only the features in :func:`build_feature_config` are extracted (emotion
    area).
    """
    extractor = Extractor(
        data=df,
        config=build_feature_config(),
        model=model,
        text_column=text_column,
    )
    extractor.extract_features()
    extractor.token_normalize("all")
    extractor.rescale("all")
    return extractor.data


def _feature_columns(
    result: pl.DataFrame, input_columns: Iterable[str]
) -> List[str]:
    """Columns produced by ELFeN = result columns not present in the input."""
    input_set = set(input_columns)
    return [c for c in result.columns if c not in input_set]


def _csv_writable(dtype: pl.DataType) -> bool:
    """Whether a polars dtype can be serialised by ``write_csv``.

    ELFeN keeps non-scalar columns in ``extractor.data`` (e.g. the spaCy ``Doc``
    objects it processes, stored as ``Object`` dtype, and any list/struct-valued
    intermediate).  The CSV writer rejects those, so they are dropped from the
    feature output.
    """
    if dtype == pl.Object:
        return False
    if isinstance(dtype, (pl.List, pl.Array, pl.Struct)):
        return False
    return True


def _writable_columns(
    result: pl.DataFrame, feature_cols: Iterable[str]
) -> List[str]:
    """Keep only feature columns whose dtype ``write_csv`` supports; log the rest."""
    keep, dropped = [], []
    schema = result.schema
    for col in feature_cols:
        (keep if _csv_writable(schema[col]) else dropped).append(col)
    if dropped:
        print(
            f"       dropping {len(dropped)} non-serialisable column(s): {', '.join(dropped)}"
        )
    return keep


_FLOAT_DTYPES = (pl.Float32, pl.Float64)


def fill_feature_nulls(
    df: pl.DataFrame,
    feature_cols: Iterable[str],
    strategy: str = "zero",
) -> pl.DataFrame:
    """Fill null/NaN feature values.

    ELFeN leaves the aggregate rating features (``avg_*``/``min_*``/``max_*``/
    ``sd_*``) as null/NaN for texts that contain no words from the relevant
    lexicon (count features are already 0).  This replaces those gaps:

    - ``zero``   -> 0, matching ELFeN's own "no lexicon words = 0" convention.
    - ``mean`` / ``median`` -> per-column mean/median over the present values
      (falling back to 0 for an all-null column).

    Float columns have their NaNs normalised to null first so both are filled.
    """
    if strategy not in ("zero", "mean", "median"):
        raise ValueError(
            f"Unknown fill strategy: {strategy!r} (use zero|mean|median)"
        )

    schema = df.schema
    exprs = []
    for col in feature_cols:
        expr = pl.col(col)
        series = df[col]
        if schema[col] in _FLOAT_DTYPES:
            expr = expr.fill_nan(
                None
            )  # treat NaN like null so it gets filled too
            series = series.fill_nan(None)

        if strategy == "zero":
            fill_value: Any = 0
        else:
            stat = series.mean() if strategy == "mean" else series.median()
            fill_value = stat if stat is not None else 0

        exprs.append(expr.fill_null(fill_value).alias(col))

    return df.with_columns(exprs) if exprs else df


def extract_model_features(
    df: pl.DataFrame,
    response_columns: List[str],
    id_column: str,
    model: str,
    keep_empty: bool,
    output_dir: pathlib.Path,
    response_prefix: str,
    fill_strategy: str = "zero",
) -> List[pathlib.Path]:
    """Extract ELFeN features for each model response column into its own CSV.

    For every model response column, writes ``<output_dir>/elfen_features_<model>.csv``
    containing the ``id_column`` plus the ELFeN feature columns.  Returns the list
    of written file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    written: List[pathlib.Path] = []

    for response_column in response_columns:
        model_name = (
            response_column.split(response_prefix, 1)[-1]
            if response_prefix in response_column
            else response_column
        )
        work = df.select([id_column, response_column]).rename(
            {response_column: "response"}
        )
        work = work.with_columns(
            pl.col("response").cast(pl.Utf8, strict=False).fill_null("")
        )
        if not keep_empty:
            work = work.filter(
                pl.col("response").str.strip_chars().str.len_chars() > 0
            )
        if work.is_empty():
            print(f"[skip] {response_column}: no non-empty responses")
            continue

        result = _run_elfen(work, text_column="response", model=model)
        feature_cols = _feature_columns(
            result, input_columns=(id_column, "response")
        )
        feature_cols = _writable_columns(result, feature_cols)
        result = result.select([id_column, *feature_cols])
        result = fill_feature_nulls(
            result, feature_cols, strategy=fill_strategy
        )

        out_path = output_dir / f"elfen_features_{model_name}.csv"
        result.write_csv(str(out_path))
        written.append(out_path)
        print(
            f"[ok]   {response_column}: {len(feature_cols)} features for {result.height} responses -> {out_path}"
        )

    return written


def extract_elfen_features(
    results_file: pathlib.Path,
    output: pathlib.Path,
    model: str = "en_core_web_trf",
    keep_empty: bool = False,
    response_prefix: str = "responses_",
    id_column: str = "id",
    fill_strategy: str = "zero",
) -> None:
    # Wide multi-model CSV path: one response column per model -> one CSV per model.
    if results_file.suffix.lower() == ".csv":
        df = pl.read_csv(results_file, infer_schema_length=0)
        response_columns = [
            c for c in df.columns if c.startswith(response_prefix)
        ]
        if response_columns:
            if id_column not in df.columns:
                df = df.with_row_index(id_column)
            models = ", ".join(
                c.split(response_prefix, 1)[-1] for c in response_columns
            )
            print(
                f"Detected {len(response_columns)} model response columns: {models}"
            )
            written = extract_model_features(
                df=df,
                response_columns=response_columns,
                id_column=id_column,
                model=model,
                keep_empty=keep_empty,
                output_dir=output,
                response_prefix=response_prefix,
                fill_strategy=fill_strategy,
            )
            print(
                f"Wrote {len(written)} per-model ELFeN feature files to {output}"
            )
            return

    # Legacy single-response path: write one CSV. If `output` is a directory
    # (no .csv suffix) put the file inside it, otherwise treat it as the file.
    df = load_generated_responses(results_file)
    if not keep_empty:
        df = df.filter(
            pl.col("response").str.strip_chars().str.len_chars() > 0
        )
    if df.is_empty():
        raise ValueError(
            "No non-empty generated responses available for ELFeN extraction."
        )

    output_file = (
        output
        if output.suffix.lower() == ".csv"
        else output / f"{results_file.stem}_elfen.csv"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    result = _run_elfen(df, text_column="response", model=model)
    writable = [c for c in result.columns if _csv_writable(result.schema[c])]
    result = result.select(writable)
    feature_cols = _feature_columns(
        result, input_columns=("prompt_id", "response", "attempts")
    )
    result = fill_feature_nulls(result, feature_cols, strategy=fill_strategy)
    result.write_csv(str(output_file))
    print(f"Wrote ELFeN features for {df.height} responses to {output_file}")


def _default_output_dir(results_file: pathlib.Path) -> pathlib.Path:
    """results/emotion/ relative to a results/ tree if present, else alongside input."""
    for parent in results_file.parents:
        if parent.name == "results":
            return parent / "emotion"
    return results_file.parent / "emotion"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract ELFeN features for generated LLM responses."
    )
    parser.add_argument(
        "--results-file",
        type=pathlib.Path,
        required=True,
        help="Path to generated results.json/csv/jsonl",
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=None,
        help="Output directory for per-model feature CSVs (default: results/emotion/)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="en_core_web_trf",
        help="spaCy model used by ELFeN",
    )
    parser.add_argument(
        "--keep-empty",
        action="store_true",
        help="Keep empty responses instead of filtering them out",
    )
    parser.add_argument(
        "--response-prefix",
        type=str,
        default="responses_",
        help="Column prefix identifying per-model response columns",
    )
    parser.add_argument(
        "--id-column",
        type=str,
        default="id",
        help="Column used as the id/join key written into each output CSV",
    )
    parser.add_argument(
        "--fill-strategy",
        type=str,
        default="zero",
        choices=("zero", "mean", "median"),
        help="How to fill null/NaN feature values (aggregate ratings with no lexicon words). Default: zero",
    )
    args = parser.parse_args()

    output: Optional[pathlib.Path] = args.out or _default_output_dir(
        args.results_file
    )
    extract_elfen_features(
        args.results_file,
        output,
        model=args.model,
        keep_empty=args.keep_empty,
        response_prefix=args.response_prefix,
        id_column=args.id_column,
        fill_strategy=args.fill_strategy,
    )


if __name__ == "__main__":
    main()
