import ast

import pandas as pd

df_metrics = pd.read_csv("evaluation/all_metrics/all_metrics.csv")
df_topics = pd.read_csv("/Users/lbartolome/seal/data/output/ses_plots/model_15_topics/query_topic_composition.csv")
threshold = 0.4
print(len(df_metrics), len(df_topics))

df_metrics_topics = pd.merge(df_metrics, df_topics, how="left", on="id")
print(len(df_metrics_topics))

df_metrics_topics["topic_composition"] = df_metrics_topics["topic_composition"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else {}
)

# keep all
all_topics = df_metrics_topics[df_metrics_topics.dominant_topic.isin([0.0,3.0])]
all_topics.to_csv("evaluation/all_metrics/all_metrics_topic_0_3.csv", index=False)

# keep all larger than threshold
larger_than_threshold = \
    df_metrics_topics[
        df_metrics_topics.dominant_topic.isin([0.0,3.0]) & (
            (df_metrics_topics.topic_composition.apply(lambda d: d.get(0, 0)) > threshold) |
            (df_metrics_topics.topic_composition.apply(lambda d: d.get(1, 0)) > threshold)
        )
    ]
larger_than_threshold.to_csv("evaluation/all_metrics/all_metrics_topic_0_3_larger_than_threshold.csv", index=False)
