import argparse
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification


DEFAULT_MODEL = "Skywork/Skywork-Reward-V2-Qwen3-0.6B"


def load_model(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
    )

    model.eval()
    return tokenizer, model


def format_prompt_response(tokenizer, prompt: str, response: str) -> str:
    messages = [
        {"role": "user", "content": str(prompt)},
        {"role": "assistant", "content": str(response)},
    ]

    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )

    return f"User: {prompt}\nAssistant: {response}"


@torch.no_grad()
def helpfulness_score(
    tokenizer,
    model,
    prompt: str,
    response: str,
    max_length: int = 4096,
) -> float:
    text = format_prompt_response(tokenizer, prompt, response)

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
    )

    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model(**inputs)
    return outputs.logits.squeeze().float().item()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="Input CSV with id, prompt, response columns")
    parser.add_argument("output_csv", help="Output CSV path")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Hugging Face model name. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=4096,
        help="Maximum tokenized input length",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    required_columns = {
        "id",
        "prompt",
        "responses_qwen-3.5-27B",
        "responses_llama-3.3-70B",
        "responses_gemma-4-31B",
        "responses_gpt-5.5",
    }
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    tokenizer, model = load_model(args.model)

    scores = []
    # calculate helpfulness scores for each column in the ["responses_qwen-3.5-27B", 
    # "responses_llama-3.3-70B", "responses_gemma-4-31B", "responses_gpt-5.5","] in the CSV
    response_columns = [
        "responses_qwen-3.5-27B",
        "responses_llama-3.3-70B",
        "responses_gemma-4-31B",
        "responses_gpt-5.5",
    ]

    for response_column in response_columns:
        df[f"helpfulness_score_{response_column}"] = df.apply(
            lambda row: helpfulness_score(
                tokenizer=tokenizer,
                model=model,
                prompt=row["prompt"],
                response=row[response_column],
                max_length=args.max_length,
            ),
            axis=1,
        )

    df.to_csv(args.output_csv, index=False)
    print(f"Saved scored CSV to {args.output_csv}")


if __name__ == "__main__":
    main()