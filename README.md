# SEAL: SocioEconomic Alignment in LLMs

This is the repository for SEAL: SocioEconomic Alignment in LLMs.

Authors: Elisa Bassignana, Lorena Calvo-Bartolomé, Esra Dönmez, Marlene Lutz, Arianna Muti, Vera Neplenbroek, Donya Rooein.

![Introduction](figure.png)

## Paper abstract
According to the United Nations Sustainable Development Goals, socioeconomic inequality is one of the defining challenges of the 21st century, as it shapes access to resources and opportunities across societies worldwide. As large language models (LLMs) become widely used for everyday tasks, they have the potential to create positive social impact by expanding access to information, writing support, education, employment guidance, and administrative assistance. However, this potential depends on whether such systems provide equitable quality of service to users from different socioeconomic backgrounds. In this paper, we evaluate LLM-generated responses to quantify disparities in quality of service across users from different socioeconomic backgrounds. We examine whether model responses to prompts written by users with lower, middle, and upper socioeconomic status (SES) differ by measuring helpfulness, sycophancy, human likeness, emotion and text complexity features. We find differences in quality of service across SES: lower-SES groups receive responses that are less helpful, less complex, less assertive, more negative in sentiment, less trust-oriented and more sycophantically validating.

## Requirements
In order to run the (topic modeling) code included in this project, install the requirements in your virtual environment by running:
```bash
uv pip install -e ".[viz]"
```

## Using this repository
- `data` contains a file with all the prompts in the dataset (`prompts_all.csv`) and the corresponding survey responses (`survey-language-technologies.csv`; both from [The AI Gap: How Socioeconomic Status Affects Language Technology Interactions](https://aclanthology.org/2025.acl-long.914/) (Bassignana et al., ACL 2025)). It also contains a file with the sample from these prompts that we use in our experiments (`sampled_dataset.csv`).
- `evaluation` contains all files of evaluated results with metric scores per LLM and per prompt-response pair.
- `results` contains all files of results with prompt-response pairs for each LLM.
- `src` contains the `seal` directory which contains the code for computing all the metrics and `src/sample_dataset.py` which is used to select the prompts sample we user in our experiments.
- `static/stops` contains `prompt_stops.txt` which consists of stopwords used in the topic modeling.
- `get_open_LLM_responses.py` is used to generate responses from the open-weights LLMs.
    Example usage:
  ```
  python get_open_LLM_responses.py --model_id meta-llama/Llama-3.3-70B-Instruct --data_id sampled_dataset
  ```
- `ses_topic_modeling.py` is used to conduct topic modeling
    Example usage:
  ```
  python ses_topic_modeling.py
  ```
