import pandas as pd
import argparse
from vllm import LLM
import os
import random

DATA_PATH = "data_Elisa"
RES_PATH = "results"

def create_prompts(questions):
    prompts = [
        [
            {"role": "user", "content": question}
        ] 
        for question in questions] 
    return prompts


def run_model(args):
    # set seed for reproducibility
    random.seed(args.seed)

    # get prompts

    question_df = pd.read_csv(f"{DATA_PATH}/{args.data_id}.csv")
    prompt_col="prompt"
    questions = question_df[prompt_col].tolist()

    prompts = create_prompts(questions)
    max_mlen = 19900
    # set up LLM
    llm = LLM(
        model=args.model_id, 
        max_model_len=max_mlen, 
        max_num_seqs=256,
        generation_config='auto',
        tensor_parallel_size=args.tensor_parallel_size,
        )

    sampling_params = llm.get_default_sampling_params()
    sampling_params.temperature = 0 
    sampling_params.n = 1 
    sampling_params.max_tokens = 600 
    sampling_params.seed = args.seed

    chat_template_kwargs={"enable_thinking": False} if args.model_id.startswith("Qwen") else {}

    print(sampling_params)

    # set output path
    out_path = f"{RES_PATH}/{args.model_id.split('/')[-1]}"
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # generate responses
    outputs = llm.chat(prompts, sampling_params, use_tqdm=False, chat_template_kwargs=chat_template_kwargs)

    responses = []

    for out in outputs:
        responses.append(out.outputs[0].text.strip())

    # add responses as a new column
    response_col = f"responses_{args.model_id.split()[-1]}"
    question_df[response_col] = responses

    # save
    question_df.to_csv(f"{out_path}/{args.data_id}_responses_{sampling_params.max_tokens}.csv", index=False)
    return
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", help="huggingface checkpoint id of the model to run", type=str)
    parser.add_argument("--data_id", help="name of the dataset to run", type=str)
    parser.add_argument("--seed", help="random seed for reproducibility", type=int, default=87)
    parser.add_argument("--tensor_parallel_size", default=1, help="number of GPUs to use for distributed setup (tensor parallelism)", type=int)
    
    args = parser.parse_args()
    print(args)

    run_model(args)

