# Metrics overview — `all_metrics_per_user.csv`

Aggregated to **732 users** × **946 columns** (905 numeric score columns). Each score is the mean across a user's prompts; the four models are `qwen-3.5-27B`, `llama-3.3-70B`, `gemma-4-31B`, `gpt-5.5`.

## Families

| Family | # cols | # base metrics | Per model? |
|---|---|---|---|
| Helpfulness (raw) | 4 | 1 | yes |
| Helpfulness (normalized) | 4 | 1 | yes |
| Human-likeness | 40 | 10 | yes |
| Sycophancy | 12 | 3 | yes |
| Linguistic (elfen) | 532 | 133 | yes |
| Complexity | 312 | 78 | yes |
| Identifier / demographics | 42 | 42 | no |

## Helpfulness (raw) (4 columns)

| column | n | mean | std | min | max |
|---|---|---|---|---|---|
| `helpfulness_score_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         helpfulness_score_responses_qwen-3.5-27B
family                                Helpfulness (raw)
base_metric                 helpfulness_score_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             5.5836
std                                              2.2774
min                                             -3.7344
max                                             14.0938
Name: 42, dtype: object> | <bound method Series.std of column         helpfulness_score_responses_qwen-3.5-27B
family                                Helpfulness (raw)
base_metric                 helpfulness_score_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             5.5836
std                                              2.2774
min                                             -3.7344
max                                             14.0938
Name: 42, dtype: object> | <bound method Series.min of column         helpfulness_score_responses_qwen-3.5-27B
family                                Helpfulness (raw)
base_metric                 helpfulness_score_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             5.5836
std                                              2.2774
min                                             -3.7344
max                                             14.0938
Name: 42, dtype: object> | <bound method Series.max of column         helpfulness_score_responses_qwen-3.5-27B
family                                Helpfulness (raw)
base_metric                 helpfulness_score_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             5.5836
std                                              2.2774
min                                             -3.7344
max                                             14.0938
Name: 42, dtype: object> |
| `helpfulness_score_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         helpfulness_score_responses_llama-3.3-70B
family                                 Helpfulness (raw)
base_metric                  helpfulness_score_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              5.0964
std                                               2.8169
min                                              -5.0312
max                                               19.125
Name: 43, dtype: object> | <bound method Series.std of column         helpfulness_score_responses_llama-3.3-70B
family                                 Helpfulness (raw)
base_metric                  helpfulness_score_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              5.0964
std                                               2.8169
min                                              -5.0312
max                                               19.125
Name: 43, dtype: object> | <bound method Series.min of column         helpfulness_score_responses_llama-3.3-70B
family                                 Helpfulness (raw)
base_metric                  helpfulness_score_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              5.0964
std                                               2.8169
min                                              -5.0312
max                                               19.125
Name: 43, dtype: object> | <bound method Series.max of column         helpfulness_score_responses_llama-3.3-70B
family                                 Helpfulness (raw)
base_metric                  helpfulness_score_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              5.0964
std                                               2.8169
min                                              -5.0312
max                                               19.125
Name: 43, dtype: object> |
| `helpfulness_score_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         helpfulness_score_responses_gemma-4-31B
family                               Helpfulness (raw)
base_metric                helpfulness_score_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                             4.412
std                                             2.0175
min                                            -5.0312
max                                               12.0
Name: 44, dtype: object> | <bound method Series.std of column         helpfulness_score_responses_gemma-4-31B
family                               Helpfulness (raw)
base_metric                helpfulness_score_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                             4.412
std                                             2.0175
min                                            -5.0312
max                                               12.0
Name: 44, dtype: object> | <bound method Series.min of column         helpfulness_score_responses_gemma-4-31B
family                               Helpfulness (raw)
base_metric                helpfulness_score_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                             4.412
std                                             2.0175
min                                            -5.0312
max                                               12.0
Name: 44, dtype: object> | <bound method Series.max of column         helpfulness_score_responses_gemma-4-31B
family                               Helpfulness (raw)
base_metric                helpfulness_score_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                             4.412
std                                             2.0175
min                                            -5.0312
max                                               12.0
Name: 44, dtype: object> |
| `helpfulness_score_responses_gpt-5.5` | 732 | <bound method Series.mean of column         helpfulness_score_responses_gpt-5.5
family                           Helpfulness (raw)
base_metric            helpfulness_score_responses
model                                      gpt-5.5
n_nonnull                                      732
mean                                        4.0504
std                                         3.0757
min                                          -9.25
max                                        15.0625
Name: 45, dtype: object> | <bound method Series.std of column         helpfulness_score_responses_gpt-5.5
family                           Helpfulness (raw)
base_metric            helpfulness_score_responses
model                                      gpt-5.5
n_nonnull                                      732
mean                                        4.0504
std                                         3.0757
min                                          -9.25
max                                        15.0625
Name: 45, dtype: object> | <bound method Series.min of column         helpfulness_score_responses_gpt-5.5
family                           Helpfulness (raw)
base_metric            helpfulness_score_responses
model                                      gpt-5.5
n_nonnull                                      732
mean                                        4.0504
std                                         3.0757
min                                          -9.25
max                                        15.0625
Name: 45, dtype: object> | <bound method Series.max of column         helpfulness_score_responses_gpt-5.5
family                           Helpfulness (raw)
base_metric            helpfulness_score_responses
model                                      gpt-5.5
n_nonnull                                      732
mean                                        4.0504
std                                         3.0757
min                                          -9.25
max                                        15.0625
Name: 45, dtype: object> |

## Helpfulness (normalized) (4 columns)

| column | n | mean | std | min | max |
|---|---|---|---|---|---|
| `normalized_helpfulness_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         normalized_helpfulness_responses_qwen-3.5-27B
family                              Helpfulness (normalized)
base_metric                 normalized_helpfulness_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  -0.044
std                                                   0.7358
min                                                  -3.0544
max                                                   2.7054
Name: 46, dtype: object> | <bound method Series.std of column         normalized_helpfulness_responses_qwen-3.5-27B
family                              Helpfulness (normalized)
base_metric                 normalized_helpfulness_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  -0.044
std                                                   0.7358
min                                                  -3.0544
max                                                   2.7054
Name: 46, dtype: object> | <bound method Series.min of column         normalized_helpfulness_responses_qwen-3.5-27B
family                              Helpfulness (normalized)
base_metric                 normalized_helpfulness_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  -0.044
std                                                   0.7358
min                                                  -3.0544
max                                                   2.7054
Name: 46, dtype: object> | <bound method Series.max of column         normalized_helpfulness_responses_qwen-3.5-27B
family                              Helpfulness (normalized)
base_metric                 normalized_helpfulness_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  -0.044
std                                                   0.7358
min                                                  -3.0544
max                                                   2.7054
Name: 46, dtype: object> |
| `normalized_helpfulness_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         normalized_helpfulness_responses_llama-3.3-70B
family                               Helpfulness (normalized)
base_metric                  normalized_helpfulness_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                  -0.0424
std                                                    0.7408
min                                                   -2.7057
max                                                    3.6467
Name: 47, dtype: object> | <bound method Series.std of column         normalized_helpfulness_responses_llama-3.3-70B
family                               Helpfulness (normalized)
base_metric                  normalized_helpfulness_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                  -0.0424
std                                                    0.7408
min                                                   -2.7057
max                                                    3.6467
Name: 47, dtype: object> | <bound method Series.min of column         normalized_helpfulness_responses_llama-3.3-70B
family                               Helpfulness (normalized)
base_metric                  normalized_helpfulness_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                  -0.0424
std                                                    0.7408
min                                                   -2.7057
max                                                    3.6467
Name: 47, dtype: object> | <bound method Series.max of column         normalized_helpfulness_responses_llama-3.3-70B
family                               Helpfulness (normalized)
base_metric                  normalized_helpfulness_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                  -0.0424
std                                                    0.7408
min                                                   -2.7057
max                                                    3.6467
Name: 47, dtype: object> |
| `normalized_helpfulness_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         normalized_helpfulness_responses_gemma-4-31B
family                             Helpfulness (normalized)
base_metric                normalized_helpfulness_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                -0.0491
std                                                  0.7325
min                                                 -3.4775
max                                                  2.7057
Name: 48, dtype: object> | <bound method Series.std of column         normalized_helpfulness_responses_gemma-4-31B
family                             Helpfulness (normalized)
base_metric                normalized_helpfulness_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                -0.0491
std                                                  0.7325
min                                                 -3.4775
max                                                  2.7057
Name: 48, dtype: object> | <bound method Series.min of column         normalized_helpfulness_responses_gemma-4-31B
family                             Helpfulness (normalized)
base_metric                normalized_helpfulness_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                -0.0491
std                                                  0.7325
min                                                 -3.4775
max                                                  2.7057
Name: 48, dtype: object> | <bound method Series.max of column         normalized_helpfulness_responses_gemma-4-31B
family                             Helpfulness (normalized)
base_metric                normalized_helpfulness_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                -0.0491
std                                                  0.7325
min                                                 -3.4775
max                                                  2.7057
Name: 48, dtype: object> |
| `normalized_helpfulness_responses_gpt-5.5` | 732 | <bound method Series.mean of column         normalized_helpfulness_responses_gpt-5.5
family                         Helpfulness (normalized)
base_metric            normalized_helpfulness_responses
model                                           gpt-5.5
n_nonnull                                           732
mean                                            -0.0072
std                                              0.7223
min                                             -3.1305
max                                              2.5787
Name: 49, dtype: object> | <bound method Series.std of column         normalized_helpfulness_responses_gpt-5.5
family                         Helpfulness (normalized)
base_metric            normalized_helpfulness_responses
model                                           gpt-5.5
n_nonnull                                           732
mean                                            -0.0072
std                                              0.7223
min                                             -3.1305
max                                              2.5787
Name: 49, dtype: object> | <bound method Series.min of column         normalized_helpfulness_responses_gpt-5.5
family                         Helpfulness (normalized)
base_metric            normalized_helpfulness_responses
model                                           gpt-5.5
n_nonnull                                           732
mean                                            -0.0072
std                                              0.7223
min                                             -3.1305
max                                              2.5787
Name: 49, dtype: object> | <bound method Series.max of column         normalized_helpfulness_responses_gpt-5.5
family                         Helpfulness (normalized)
base_metric            normalized_helpfulness_responses
model                                           gpt-5.5
n_nonnull                                           732
mean                                            -0.0072
std                                              0.7223
min                                             -3.1305
max                                              2.5787
Name: 49, dtype: object> |

## Human-likeness (40 columns)

| column | n | mean | std | min | max |
|---|---|---|---|---|---|
| `humt_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         humt_responses_qwen-3.5-27B
family                      Human-likeness
base_metric                 humt_responses
model                         qwen-3.5-27B
n_nonnull                              732
mean                                0.0155
std                                 0.0175
min                                -0.0433
max                                 0.1628
Name: 50, dtype: object> | <bound method Series.std of column         humt_responses_qwen-3.5-27B
family                      Human-likeness
base_metric                 humt_responses
model                         qwen-3.5-27B
n_nonnull                              732
mean                                0.0155
std                                 0.0175
min                                -0.0433
max                                 0.1628
Name: 50, dtype: object> | <bound method Series.min of column         humt_responses_qwen-3.5-27B
family                      Human-likeness
base_metric                 humt_responses
model                         qwen-3.5-27B
n_nonnull                              732
mean                                0.0155
std                                 0.0175
min                                -0.0433
max                                 0.1628
Name: 50, dtype: object> | <bound method Series.max of column         humt_responses_qwen-3.5-27B
family                      Human-likeness
base_metric                 humt_responses
model                         qwen-3.5-27B
n_nonnull                              732
mean                                0.0155
std                                 0.0175
min                                -0.0433
max                                 0.1628
Name: 50, dtype: object> |
| `std_humt_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         std_humt_responses_qwen-3.5-27B
family                          Human-likeness
base_metric                 std_humt_responses
model                             qwen-3.5-27B
n_nonnull                                  732
mean                                    0.0141
std                                     0.0016
min                                     0.0102
max                                     0.0268
Name: 51, dtype: object> | <bound method Series.std of column         std_humt_responses_qwen-3.5-27B
family                          Human-likeness
base_metric                 std_humt_responses
model                             qwen-3.5-27B
n_nonnull                                  732
mean                                    0.0141
std                                     0.0016
min                                     0.0102
max                                     0.0268
Name: 51, dtype: object> | <bound method Series.min of column         std_humt_responses_qwen-3.5-27B
family                          Human-likeness
base_metric                 std_humt_responses
model                             qwen-3.5-27B
n_nonnull                                  732
mean                                    0.0141
std                                     0.0016
min                                     0.0102
max                                     0.0268
Name: 51, dtype: object> | <bound method Series.max of column         std_humt_responses_qwen-3.5-27B
family                          Human-likeness
base_metric                 std_humt_responses
model                             qwen-3.5-27B
n_nonnull                                  732
mean                                    0.0141
std                                     0.0016
min                                     0.0102
max                                     0.0268
Name: 51, dtype: object> |
| `sociot_status_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         sociot_status_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_status_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                        -0.0522
std                                          0.0189
min                                         -0.1855
max                                          0.0188
Name: 52, dtype: object> | <bound method Series.std of column         sociot_status_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_status_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                        -0.0522
std                                          0.0189
min                                         -0.1855
max                                          0.0188
Name: 52, dtype: object> | <bound method Series.min of column         sociot_status_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_status_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                        -0.0522
std                                          0.0189
min                                         -0.1855
max                                          0.0188
Name: 52, dtype: object> | <bound method Series.max of column         sociot_status_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_status_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                        -0.0522
std                                          0.0189
min                                         -0.1855
max                                          0.0188
Name: 52, dtype: object> |
| `std_sociot_status_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         std_sociot_status_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_status_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0096
std                                               0.001
min                                              0.0069
max                                              0.0151
Name: 53, dtype: object> | <bound method Series.std of column         std_sociot_status_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_status_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0096
std                                               0.001
min                                              0.0069
max                                              0.0151
Name: 53, dtype: object> | <bound method Series.min of column         std_sociot_status_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_status_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0096
std                                               0.001
min                                              0.0069
max                                              0.0151
Name: 53, dtype: object> | <bound method Series.max of column         std_sociot_status_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_status_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0096
std                                               0.001
min                                              0.0069
max                                              0.0151
Name: 53, dtype: object> |
| `sociot_social_distance_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         sociot_social_distance_responses_qwen-3.5-27B
family                                        Human-likeness
base_metric                 sociot_social_distance_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  0.0368
std                                                   0.0224
min                                                  -0.0341
max                                                   0.2028
Name: 54, dtype: object> | <bound method Series.std of column         sociot_social_distance_responses_qwen-3.5-27B
family                                        Human-likeness
base_metric                 sociot_social_distance_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  0.0368
std                                                   0.0224
min                                                  -0.0341
max                                                   0.2028
Name: 54, dtype: object> | <bound method Series.min of column         sociot_social_distance_responses_qwen-3.5-27B
family                                        Human-likeness
base_metric                 sociot_social_distance_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  0.0368
std                                                   0.0224
min                                                  -0.0341
max                                                   0.2028
Name: 54, dtype: object> | <bound method Series.max of column         sociot_social_distance_responses_qwen-3.5-27B
family                                        Human-likeness
base_metric                 sociot_social_distance_responses
model                                           qwen-3.5-27B
n_nonnull                                                732
mean                                                  0.0368
std                                                   0.0224
min                                                  -0.0341
max                                                   0.2028
Name: 54, dtype: object> |
| `std_sociot_social_distance_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         std_sociot_social_distance_responses_qwen-3.5-27B
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                               qwen-3.5-27B
n_nonnull                                                    732
mean                                                      0.0124
std                                                       0.0015
min                                                       0.0082
max                                                       0.0266
Name: 55, dtype: object> | <bound method Series.std of column         std_sociot_social_distance_responses_qwen-3.5-27B
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                               qwen-3.5-27B
n_nonnull                                                    732
mean                                                      0.0124
std                                                       0.0015
min                                                       0.0082
max                                                       0.0266
Name: 55, dtype: object> | <bound method Series.min of column         std_sociot_social_distance_responses_qwen-3.5-27B
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                               qwen-3.5-27B
n_nonnull                                                    732
mean                                                      0.0124
std                                                       0.0015
min                                                       0.0082
max                                                       0.0266
Name: 55, dtype: object> | <bound method Series.max of column         std_sociot_social_distance_responses_qwen-3.5-27B
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                               qwen-3.5-27B
n_nonnull                                                    732
mean                                                      0.0124
std                                                       0.0015
min                                                       0.0082
max                                                       0.0266
Name: 55, dtype: object> |
| `sociot_gender_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         sociot_gender_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_gender_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0042
std                                          0.0143
min                                         -0.0504
max                                          0.0819
Name: 56, dtype: object> | <bound method Series.std of column         sociot_gender_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_gender_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0042
std                                          0.0143
min                                         -0.0504
max                                          0.0819
Name: 56, dtype: object> | <bound method Series.min of column         sociot_gender_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_gender_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0042
std                                          0.0143
min                                         -0.0504
max                                          0.0819
Name: 56, dtype: object> | <bound method Series.max of column         sociot_gender_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_gender_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0042
std                                          0.0143
min                                         -0.0504
max                                          0.0819
Name: 56, dtype: object> |
| `std_sociot_gender_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         std_sociot_gender_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_gender_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0162
std                                              0.0018
min                                               0.012
max                                              0.0281
Name: 57, dtype: object> | <bound method Series.std of column         std_sociot_gender_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_gender_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0162
std                                              0.0018
min                                               0.012
max                                              0.0281
Name: 57, dtype: object> | <bound method Series.min of column         std_sociot_gender_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_gender_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0162
std                                              0.0018
min                                               0.012
max                                              0.0281
Name: 57, dtype: object> | <bound method Series.max of column         std_sociot_gender_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_gender_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0162
std                                              0.0018
min                                               0.012
max                                              0.0281
Name: 57, dtype: object> |
| `sociot_warmth_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         sociot_warmth_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_warmth_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0155
std                                          0.0182
min                                         -0.0453
max                                          0.0794
Name: 58, dtype: object> | <bound method Series.std of column         sociot_warmth_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_warmth_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0155
std                                          0.0182
min                                         -0.0453
max                                          0.0794
Name: 58, dtype: object> | <bound method Series.min of column         sociot_warmth_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_warmth_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0155
std                                          0.0182
min                                         -0.0453
max                                          0.0794
Name: 58, dtype: object> | <bound method Series.max of column         sociot_warmth_responses_qwen-3.5-27B
family                               Human-likeness
base_metric                 sociot_warmth_responses
model                                  qwen-3.5-27B
n_nonnull                                       732
mean                                         0.0155
std                                          0.0182
min                                         -0.0453
max                                          0.0794
Name: 58, dtype: object> |
| `std_sociot_warmth_responses_qwen-3.5-27B` | 732 | <bound method Series.mean of column         std_sociot_warmth_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_warmth_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0081
std                                              0.0009
min                                              0.0062
max                                              0.0142
Name: 59, dtype: object> | <bound method Series.std of column         std_sociot_warmth_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_warmth_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0081
std                                              0.0009
min                                              0.0062
max                                              0.0142
Name: 59, dtype: object> | <bound method Series.min of column         std_sociot_warmth_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_warmth_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0081
std                                              0.0009
min                                              0.0062
max                                              0.0142
Name: 59, dtype: object> | <bound method Series.max of column         std_sociot_warmth_responses_qwen-3.5-27B
family                                   Human-likeness
base_metric                 std_sociot_warmth_responses
model                                      qwen-3.5-27B
n_nonnull                                           732
mean                                             0.0081
std                                              0.0009
min                                              0.0062
max                                              0.0142
Name: 59, dtype: object> |
| `humt_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         humt_responses_llama-3.3-70B
family                       Human-likeness
base_metric                  humt_responses
model                         llama-3.3-70B
n_nonnull                               732
mean                                 0.0188
std                                  0.0254
min                                 -0.0637
max                                  0.2389
Name: 60, dtype: object> | <bound method Series.std of column         humt_responses_llama-3.3-70B
family                       Human-likeness
base_metric                  humt_responses
model                         llama-3.3-70B
n_nonnull                               732
mean                                 0.0188
std                                  0.0254
min                                 -0.0637
max                                  0.2389
Name: 60, dtype: object> | <bound method Series.min of column         humt_responses_llama-3.3-70B
family                       Human-likeness
base_metric                  humt_responses
model                         llama-3.3-70B
n_nonnull                               732
mean                                 0.0188
std                                  0.0254
min                                 -0.0637
max                                  0.2389
Name: 60, dtype: object> | <bound method Series.max of column         humt_responses_llama-3.3-70B
family                       Human-likeness
base_metric                  humt_responses
model                         llama-3.3-70B
n_nonnull                               732
mean                                 0.0188
std                                  0.0254
min                                 -0.0637
max                                  0.2389
Name: 60, dtype: object> |
| `std_humt_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         std_humt_responses_llama-3.3-70B
family                           Human-likeness
base_metric                  std_humt_responses
model                             llama-3.3-70B
n_nonnull                                   732
mean                                     0.0148
std                                      0.0043
min                                      0.0072
max                                      0.0699
Name: 61, dtype: object> | <bound method Series.std of column         std_humt_responses_llama-3.3-70B
family                           Human-likeness
base_metric                  std_humt_responses
model                             llama-3.3-70B
n_nonnull                                   732
mean                                     0.0148
std                                      0.0043
min                                      0.0072
max                                      0.0699
Name: 61, dtype: object> | <bound method Series.min of column         std_humt_responses_llama-3.3-70B
family                           Human-likeness
base_metric                  std_humt_responses
model                             llama-3.3-70B
n_nonnull                                   732
mean                                     0.0148
std                                      0.0043
min                                      0.0072
max                                      0.0699
Name: 61, dtype: object> | <bound method Series.max of column         std_humt_responses_llama-3.3-70B
family                           Human-likeness
base_metric                  std_humt_responses
model                             llama-3.3-70B
n_nonnull                                   732
mean                                     0.0148
std                                      0.0043
min                                      0.0072
max                                      0.0699
Name: 61, dtype: object> |
| `sociot_status_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         sociot_status_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_status_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                         -0.0563
std                                           0.0226
min                                          -0.2268
max                                           0.0072
Name: 62, dtype: object> | <bound method Series.std of column         sociot_status_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_status_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                         -0.0563
std                                           0.0226
min                                          -0.2268
max                                           0.0072
Name: 62, dtype: object> | <bound method Series.min of column         sociot_status_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_status_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                         -0.0563
std                                           0.0226
min                                          -0.2268
max                                           0.0072
Name: 62, dtype: object> | <bound method Series.max of column         sociot_status_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_status_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                         -0.0563
std                                           0.0226
min                                          -0.2268
max                                           0.0072
Name: 62, dtype: object> |
| `std_sociot_status_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         std_sociot_status_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_status_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0101
std                                               0.0027
min                                               0.0057
max                                               0.0452
Name: 63, dtype: object> | <bound method Series.std of column         std_sociot_status_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_status_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0101
std                                               0.0027
min                                               0.0057
max                                               0.0452
Name: 63, dtype: object> | <bound method Series.min of column         std_sociot_status_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_status_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0101
std                                               0.0027
min                                               0.0057
max                                               0.0452
Name: 63, dtype: object> | <bound method Series.max of column         std_sociot_status_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_status_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0101
std                                               0.0027
min                                               0.0057
max                                               0.0452
Name: 63, dtype: object> |
| `sociot_social_distance_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         sociot_social_distance_responses_llama-3.3-70B
family                                         Human-likeness
base_metric                  sociot_social_distance_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                   0.0401
std                                                    0.0301
min                                                   -0.0357
max                                                    0.3458
Name: 64, dtype: object> | <bound method Series.std of column         sociot_social_distance_responses_llama-3.3-70B
family                                         Human-likeness
base_metric                  sociot_social_distance_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                   0.0401
std                                                    0.0301
min                                                   -0.0357
max                                                    0.3458
Name: 64, dtype: object> | <bound method Series.min of column         sociot_social_distance_responses_llama-3.3-70B
family                                         Human-likeness
base_metric                  sociot_social_distance_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                   0.0401
std                                                    0.0301
min                                                   -0.0357
max                                                    0.3458
Name: 64, dtype: object> | <bound method Series.max of column         sociot_social_distance_responses_llama-3.3-70B
family                                         Human-likeness
base_metric                  sociot_social_distance_responses
model                                           llama-3.3-70B
n_nonnull                                                 732
mean                                                   0.0401
std                                                    0.0301
min                                                   -0.0357
max                                                    0.3458
Name: 64, dtype: object> |
| `std_sociot_social_distance_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         std_sociot_social_distance_responses_llama-3.3...
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                              llama-3.3-70B
n_nonnull                                                    732
mean                                                       0.013
std                                                       0.0035
min                                                       0.0067
max                                                       0.0557
Name: 65, dtype: object> | <bound method Series.std of column         std_sociot_social_distance_responses_llama-3.3...
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                              llama-3.3-70B
n_nonnull                                                    732
mean                                                       0.013
std                                                       0.0035
min                                                       0.0067
max                                                       0.0557
Name: 65, dtype: object> | <bound method Series.min of column         std_sociot_social_distance_responses_llama-3.3...
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                              llama-3.3-70B
n_nonnull                                                    732
mean                                                       0.013
std                                                       0.0035
min                                                       0.0067
max                                                       0.0557
Name: 65, dtype: object> | <bound method Series.max of column         std_sociot_social_distance_responses_llama-3.3...
family                                            Human-likeness
base_metric                 std_sociot_social_distance_responses
model                                              llama-3.3-70B
n_nonnull                                                    732
mean                                                       0.013
std                                                       0.0035
min                                                       0.0067
max                                                       0.0557
Name: 65, dtype: object> |
| `sociot_gender_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         sociot_gender_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_gender_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0065
std                                           0.0167
min                                          -0.0519
max                                           0.1333
Name: 66, dtype: object> | <bound method Series.std of column         sociot_gender_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_gender_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0065
std                                           0.0167
min                                          -0.0519
max                                           0.1333
Name: 66, dtype: object> | <bound method Series.min of column         sociot_gender_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_gender_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0065
std                                           0.0167
min                                          -0.0519
max                                           0.1333
Name: 66, dtype: object> | <bound method Series.max of column         sociot_gender_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_gender_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0065
std                                           0.0167
min                                          -0.0519
max                                           0.1333
Name: 66, dtype: object> |
| `std_sociot_gender_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         std_sociot_gender_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_gender_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0171
std                                               0.0048
min                                               0.0091
max                                               0.0764
Name: 67, dtype: object> | <bound method Series.std of column         std_sociot_gender_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_gender_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0171
std                                               0.0048
min                                               0.0091
max                                               0.0764
Name: 67, dtype: object> | <bound method Series.min of column         std_sociot_gender_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_gender_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0171
std                                               0.0048
min                                               0.0091
max                                               0.0764
Name: 67, dtype: object> | <bound method Series.max of column         std_sociot_gender_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_gender_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0171
std                                               0.0048
min                                               0.0091
max                                               0.0764
Name: 67, dtype: object> |
| `sociot_warmth_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         sociot_warmth_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_warmth_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0126
std                                           0.0168
min                                          -0.0433
max                                           0.0755
Name: 68, dtype: object> | <bound method Series.std of column         sociot_warmth_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_warmth_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0126
std                                           0.0168
min                                          -0.0433
max                                           0.0755
Name: 68, dtype: object> | <bound method Series.min of column         sociot_warmth_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_warmth_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0126
std                                           0.0168
min                                          -0.0433
max                                           0.0755
Name: 68, dtype: object> | <bound method Series.max of column         sociot_warmth_responses_llama-3.3-70B
family                                Human-likeness
base_metric                  sociot_warmth_responses
model                                  llama-3.3-70B
n_nonnull                                        732
mean                                          0.0126
std                                           0.0168
min                                          -0.0433
max                                           0.0755
Name: 68, dtype: object> |
| `std_sociot_warmth_responses_llama-3.3-70B` | 732 | <bound method Series.mean of column         std_sociot_warmth_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_warmth_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0086
std                                               0.0024
min                                               0.0046
max                                                0.038
Name: 69, dtype: object> | <bound method Series.std of column         std_sociot_warmth_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_warmth_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0086
std                                               0.0024
min                                               0.0046
max                                                0.038
Name: 69, dtype: object> | <bound method Series.min of column         std_sociot_warmth_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_warmth_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0086
std                                               0.0024
min                                               0.0046
max                                                0.038
Name: 69, dtype: object> | <bound method Series.max of column         std_sociot_warmth_responses_llama-3.3-70B
family                                    Human-likeness
base_metric                  std_sociot_warmth_responses
model                                      llama-3.3-70B
n_nonnull                                            732
mean                                              0.0086
std                                               0.0024
min                                               0.0046
max                                                0.038
Name: 69, dtype: object> |
| `humt_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         humt_responses_gemma-4-31B
family                     Human-likeness
base_metric                humt_responses
model                         gemma-4-31B
n_nonnull                             732
mean                               0.0177
std                                 0.024
min                               -0.0612
max                                0.2575
Name: 70, dtype: object> | <bound method Series.std of column         humt_responses_gemma-4-31B
family                     Human-likeness
base_metric                humt_responses
model                         gemma-4-31B
n_nonnull                             732
mean                               0.0177
std                                 0.024
min                               -0.0612
max                                0.2575
Name: 70, dtype: object> | <bound method Series.min of column         humt_responses_gemma-4-31B
family                     Human-likeness
base_metric                humt_responses
model                         gemma-4-31B
n_nonnull                             732
mean                               0.0177
std                                 0.024
min                               -0.0612
max                                0.2575
Name: 70, dtype: object> | <bound method Series.max of column         humt_responses_gemma-4-31B
family                     Human-likeness
base_metric                humt_responses
model                         gemma-4-31B
n_nonnull                             732
mean                               0.0177
std                                 0.024
min                               -0.0612
max                                0.2575
Name: 70, dtype: object> |
| `std_humt_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         std_humt_responses_gemma-4-31B
family                         Human-likeness
base_metric                std_humt_responses
model                             gemma-4-31B
n_nonnull                                 732
mean                                   0.0141
std                                    0.0023
min                                    0.0088
max                                    0.0347
Name: 71, dtype: object> | <bound method Series.std of column         std_humt_responses_gemma-4-31B
family                         Human-likeness
base_metric                std_humt_responses
model                             gemma-4-31B
n_nonnull                                 732
mean                                   0.0141
std                                    0.0023
min                                    0.0088
max                                    0.0347
Name: 71, dtype: object> | <bound method Series.min of column         std_humt_responses_gemma-4-31B
family                         Human-likeness
base_metric                std_humt_responses
model                             gemma-4-31B
n_nonnull                                 732
mean                                   0.0141
std                                    0.0023
min                                    0.0088
max                                    0.0347
Name: 71, dtype: object> | <bound method Series.max of column         std_humt_responses_gemma-4-31B
family                         Human-likeness
base_metric                std_humt_responses
model                             gemma-4-31B
n_nonnull                                 732
mean                                   0.0141
std                                    0.0023
min                                    0.0088
max                                    0.0347
Name: 71, dtype: object> |
| `sociot_status_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         sociot_status_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_status_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                       -0.0533
std                                         0.0231
min                                        -0.2943
max                                         0.0316
Name: 72, dtype: object> | <bound method Series.std of column         sociot_status_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_status_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                       -0.0533
std                                         0.0231
min                                        -0.2943
max                                         0.0316
Name: 72, dtype: object> | <bound method Series.min of column         sociot_status_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_status_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                       -0.0533
std                                         0.0231
min                                        -0.2943
max                                         0.0316
Name: 72, dtype: object> | <bound method Series.max of column         sociot_status_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_status_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                       -0.0533
std                                         0.0231
min                                        -0.2943
max                                         0.0316
Name: 72, dtype: object> |
| `std_sociot_status_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         std_sociot_status_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_status_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0097
std                                             0.0016
min                                             0.0062
max                                             0.0243
Name: 73, dtype: object> | <bound method Series.std of column         std_sociot_status_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_status_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0097
std                                             0.0016
min                                             0.0062
max                                             0.0243
Name: 73, dtype: object> | <bound method Series.min of column         std_sociot_status_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_status_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0097
std                                             0.0016
min                                             0.0062
max                                             0.0243
Name: 73, dtype: object> | <bound method Series.max of column         std_sociot_status_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_status_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0097
std                                             0.0016
min                                             0.0062
max                                             0.0243
Name: 73, dtype: object> |
| `sociot_social_distance_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         sociot_social_distance_responses_gemma-4-31B
family                                       Human-likeness
base_metric                sociot_social_distance_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                 0.0407
std                                                  0.0302
min                                                 -0.0377
max                                                  0.4064
Name: 74, dtype: object> | <bound method Series.std of column         sociot_social_distance_responses_gemma-4-31B
family                                       Human-likeness
base_metric                sociot_social_distance_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                 0.0407
std                                                  0.0302
min                                                 -0.0377
max                                                  0.4064
Name: 74, dtype: object> | <bound method Series.min of column         sociot_social_distance_responses_gemma-4-31B
family                                       Human-likeness
base_metric                sociot_social_distance_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                 0.0407
std                                                  0.0302
min                                                 -0.0377
max                                                  0.4064
Name: 74, dtype: object> | <bound method Series.max of column         sociot_social_distance_responses_gemma-4-31B
family                                       Human-likeness
base_metric                sociot_social_distance_responses
model                                           gemma-4-31B
n_nonnull                                               732
mean                                                 0.0407
std                                                  0.0302
min                                                 -0.0377
max                                                  0.4064
Name: 74, dtype: object> |
| `std_sociot_social_distance_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         std_sociot_social_distance_responses_gemma-4-31B
family                                           Human-likeness
base_metric                std_sociot_social_distance_responses
model                                               gemma-4-31B
n_nonnull                                                   732
mean                                                     0.0124
std                                                       0.002
min                                                      0.0082
max                                                       0.029
Name: 75, dtype: object> | <bound method Series.std of column         std_sociot_social_distance_responses_gemma-4-31B
family                                           Human-likeness
base_metric                std_sociot_social_distance_responses
model                                               gemma-4-31B
n_nonnull                                                   732
mean                                                     0.0124
std                                                       0.002
min                                                      0.0082
max                                                       0.029
Name: 75, dtype: object> | <bound method Series.min of column         std_sociot_social_distance_responses_gemma-4-31B
family                                           Human-likeness
base_metric                std_sociot_social_distance_responses
model                                               gemma-4-31B
n_nonnull                                                   732
mean                                                     0.0124
std                                                       0.002
min                                                      0.0082
max                                                       0.029
Name: 75, dtype: object> | <bound method Series.max of column         std_sociot_social_distance_responses_gemma-4-31B
family                                           Human-likeness
base_metric                std_sociot_social_distance_responses
model                                               gemma-4-31B
n_nonnull                                                   732
mean                                                     0.0124
std                                                       0.002
min                                                      0.0082
max                                                       0.029
Name: 75, dtype: object> |
| `sociot_gender_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         sociot_gender_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_gender_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0048
std                                         0.0142
min                                         -0.044
max                                         0.0782
Name: 76, dtype: object> | <bound method Series.std of column         sociot_gender_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_gender_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0048
std                                         0.0142
min                                         -0.044
max                                         0.0782
Name: 76, dtype: object> | <bound method Series.min of column         sociot_gender_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_gender_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0048
std                                         0.0142
min                                         -0.044
max                                         0.0782
Name: 76, dtype: object> | <bound method Series.max of column         sociot_gender_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_gender_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0048
std                                         0.0142
min                                         -0.044
max                                         0.0782
Name: 76, dtype: object> |
| `std_sociot_gender_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         std_sociot_gender_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_gender_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0162
std                                             0.0027
min                                             0.0106
max                                             0.0398
Name: 77, dtype: object> | <bound method Series.std of column         std_sociot_gender_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_gender_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0162
std                                             0.0027
min                                             0.0106
max                                             0.0398
Name: 77, dtype: object> | <bound method Series.min of column         std_sociot_gender_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_gender_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0162
std                                             0.0027
min                                             0.0106
max                                             0.0398
Name: 77, dtype: object> | <bound method Series.max of column         std_sociot_gender_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_gender_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0162
std                                             0.0027
min                                             0.0106
max                                             0.0398
Name: 77, dtype: object> |
| `sociot_warmth_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         sociot_warmth_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_warmth_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0147
std                                         0.0173
min                                        -0.1276
max                                         0.0758
Name: 78, dtype: object> | <bound method Series.std of column         sociot_warmth_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_warmth_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0147
std                                         0.0173
min                                        -0.1276
max                                         0.0758
Name: 78, dtype: object> | <bound method Series.min of column         sociot_warmth_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_warmth_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0147
std                                         0.0173
min                                        -0.1276
max                                         0.0758
Name: 78, dtype: object> | <bound method Series.max of column         sociot_warmth_responses_gemma-4-31B
family                              Human-likeness
base_metric                sociot_warmth_responses
model                                  gemma-4-31B
n_nonnull                                      732
mean                                        0.0147
std                                         0.0173
min                                        -0.1276
max                                         0.0758
Name: 78, dtype: object> |
| `std_sociot_warmth_responses_gemma-4-31B` | 732 | <bound method Series.mean of column         std_sociot_warmth_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_warmth_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0081
std                                             0.0013
min                                             0.0053
max                                             0.0189
Name: 79, dtype: object> | <bound method Series.std of column         std_sociot_warmth_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_warmth_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0081
std                                             0.0013
min                                             0.0053
max                                             0.0189
Name: 79, dtype: object> | <bound method Series.min of column         std_sociot_warmth_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_warmth_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0081
std                                             0.0013
min                                             0.0053
max                                             0.0189
Name: 79, dtype: object> | <bound method Series.max of column         std_sociot_warmth_responses_gemma-4-31B
family                                  Human-likeness
base_metric                std_sociot_warmth_responses
model                                      gemma-4-31B
n_nonnull                                          732
mean                                            0.0081
std                                             0.0013
min                                             0.0053
max                                             0.0189
Name: 79, dtype: object> |
| `humt_responses_gpt-5.5` | 728 | <bound method Series.mean of column         humt_responses_gpt-5.5
family                 Human-likeness
base_metric            humt_responses
model                         gpt-5.5
n_nonnull                         728
mean                           0.0228
std                            0.0315
min                           -0.0433
max                            0.2927
Name: 80, dtype: object> | <bound method Series.std of column         humt_responses_gpt-5.5
family                 Human-likeness
base_metric            humt_responses
model                         gpt-5.5
n_nonnull                         728
mean                           0.0228
std                            0.0315
min                           -0.0433
max                            0.2927
Name: 80, dtype: object> | <bound method Series.min of column         humt_responses_gpt-5.5
family                 Human-likeness
base_metric            humt_responses
model                         gpt-5.5
n_nonnull                         728
mean                           0.0228
std                            0.0315
min                           -0.0433
max                            0.2927
Name: 80, dtype: object> | <bound method Series.max of column         humt_responses_gpt-5.5
family                 Human-likeness
base_metric            humt_responses
model                         gpt-5.5
n_nonnull                         728
mean                           0.0228
std                            0.0315
min                           -0.0433
max                            0.2927
Name: 80, dtype: object> |
| `std_humt_responses_gpt-5.5` | 728 | <bound method Series.mean of column         std_humt_responses_gpt-5.5
family                     Human-likeness
base_metric            std_humt_responses
model                             gpt-5.5
n_nonnull                             728
mean                               0.0168
std                                0.0032
min                                0.0114
max                                0.0333
Name: 81, dtype: object> | <bound method Series.std of column         std_humt_responses_gpt-5.5
family                     Human-likeness
base_metric            std_humt_responses
model                             gpt-5.5
n_nonnull                             728
mean                               0.0168
std                                0.0032
min                                0.0114
max                                0.0333
Name: 81, dtype: object> | <bound method Series.min of column         std_humt_responses_gpt-5.5
family                     Human-likeness
base_metric            std_humt_responses
model                             gpt-5.5
n_nonnull                             728
mean                               0.0168
std                                0.0032
min                                0.0114
max                                0.0333
Name: 81, dtype: object> | <bound method Series.max of column         std_humt_responses_gpt-5.5
family                     Human-likeness
base_metric            std_humt_responses
model                             gpt-5.5
n_nonnull                             728
mean                               0.0168
std                                0.0032
min                                0.0114
max                                0.0333
Name: 81, dtype: object> |
| `sociot_status_responses_gpt-5.5` | 728 | <bound method Series.mean of column         sociot_status_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_status_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                   -0.0616
std                                     0.0363
min                                    -0.2877
max                                     0.0293
Name: 82, dtype: object> | <bound method Series.std of column         sociot_status_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_status_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                   -0.0616
std                                     0.0363
min                                    -0.2877
max                                     0.0293
Name: 82, dtype: object> | <bound method Series.min of column         sociot_status_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_status_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                   -0.0616
std                                     0.0363
min                                    -0.2877
max                                     0.0293
Name: 82, dtype: object> | <bound method Series.max of column         sociot_status_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_status_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                   -0.0616
std                                     0.0363
min                                    -0.2877
max                                     0.0293
Name: 82, dtype: object> |
| `std_sociot_status_responses_gpt-5.5` | 728 | <bound method Series.mean of column         std_sociot_status_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_status_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0114
std                                         0.0022
min                                         0.0075
max                                         0.0267
Name: 83, dtype: object> | <bound method Series.std of column         std_sociot_status_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_status_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0114
std                                         0.0022
min                                         0.0075
max                                         0.0267
Name: 83, dtype: object> | <bound method Series.min of column         std_sociot_status_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_status_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0114
std                                         0.0022
min                                         0.0075
max                                         0.0267
Name: 83, dtype: object> | <bound method Series.max of column         std_sociot_status_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_status_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0114
std                                         0.0022
min                                         0.0075
max                                         0.0267
Name: 83, dtype: object> |
| `sociot_social_distance_responses_gpt-5.5` | 728 | <bound method Series.mean of column         sociot_social_distance_responses_gpt-5.5
family                                   Human-likeness
base_metric            sociot_social_distance_responses
model                                           gpt-5.5
n_nonnull                                           728
mean                                             0.0469
std                                              0.0423
min                                             -0.0401
max                                              0.3908
Name: 84, dtype: object> | <bound method Series.std of column         sociot_social_distance_responses_gpt-5.5
family                                   Human-likeness
base_metric            sociot_social_distance_responses
model                                           gpt-5.5
n_nonnull                                           728
mean                                             0.0469
std                                              0.0423
min                                             -0.0401
max                                              0.3908
Name: 84, dtype: object> | <bound method Series.min of column         sociot_social_distance_responses_gpt-5.5
family                                   Human-likeness
base_metric            sociot_social_distance_responses
model                                           gpt-5.5
n_nonnull                                           728
mean                                             0.0469
std                                              0.0423
min                                             -0.0401
max                                              0.3908
Name: 84, dtype: object> | <bound method Series.max of column         sociot_social_distance_responses_gpt-5.5
family                                   Human-likeness
base_metric            sociot_social_distance_responses
model                                           gpt-5.5
n_nonnull                                           728
mean                                             0.0469
std                                              0.0423
min                                             -0.0401
max                                              0.3908
Name: 84, dtype: object> |
| `std_sociot_social_distance_responses_gpt-5.5` | 728 | <bound method Series.mean of column         std_sociot_social_distance_responses_gpt-5.5
family                                       Human-likeness
base_metric            std_sociot_social_distance_responses
model                                               gpt-5.5
n_nonnull                                               728
mean                                                 0.0148
std                                                  0.0029
min                                                  0.0096
max                                                  0.0338
Name: 85, dtype: object> | <bound method Series.std of column         std_sociot_social_distance_responses_gpt-5.5
family                                       Human-likeness
base_metric            std_sociot_social_distance_responses
model                                               gpt-5.5
n_nonnull                                               728
mean                                                 0.0148
std                                                  0.0029
min                                                  0.0096
max                                                  0.0338
Name: 85, dtype: object> | <bound method Series.min of column         std_sociot_social_distance_responses_gpt-5.5
family                                       Human-likeness
base_metric            std_sociot_social_distance_responses
model                                               gpt-5.5
n_nonnull                                               728
mean                                                 0.0148
std                                                  0.0029
min                                                  0.0096
max                                                  0.0338
Name: 85, dtype: object> | <bound method Series.max of column         std_sociot_social_distance_responses_gpt-5.5
family                                       Human-likeness
base_metric            std_sociot_social_distance_responses
model                                               gpt-5.5
n_nonnull                                               728
mean                                                 0.0148
std                                                  0.0029
min                                                  0.0096
max                                                  0.0338
Name: 85, dtype: object> |
| `sociot_gender_responses_gpt-5.5` | 728 | <bound method Series.mean of column         sociot_gender_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_gender_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0052
std                                     0.0182
min                                    -0.0685
max                                     0.1208
Name: 86, dtype: object> | <bound method Series.std of column         sociot_gender_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_gender_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0052
std                                     0.0182
min                                    -0.0685
max                                     0.1208
Name: 86, dtype: object> | <bound method Series.min of column         sociot_gender_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_gender_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0052
std                                     0.0182
min                                    -0.0685
max                                     0.1208
Name: 86, dtype: object> | <bound method Series.max of column         sociot_gender_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_gender_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0052
std                                     0.0182
min                                    -0.0685
max                                     0.1208
Name: 86, dtype: object> |
| `std_sociot_gender_responses_gpt-5.5` | 728 | <bound method Series.mean of column         std_sociot_gender_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_gender_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0195
std                                         0.0039
min                                         0.0123
max                                         0.0452
Name: 87, dtype: object> | <bound method Series.std of column         std_sociot_gender_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_gender_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0195
std                                         0.0039
min                                         0.0123
max                                         0.0452
Name: 87, dtype: object> | <bound method Series.min of column         std_sociot_gender_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_gender_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0195
std                                         0.0039
min                                         0.0123
max                                         0.0452
Name: 87, dtype: object> | <bound method Series.max of column         std_sociot_gender_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_gender_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0195
std                                         0.0039
min                                         0.0123
max                                         0.0452
Name: 87, dtype: object> |
| `sociot_warmth_responses_gpt-5.5` | 728 | <bound method Series.mean of column         sociot_warmth_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_warmth_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0172
std                                     0.0181
min                                    -0.0634
max                                     0.1109
Name: 88, dtype: object> | <bound method Series.std of column         sociot_warmth_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_warmth_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0172
std                                     0.0181
min                                    -0.0634
max                                     0.1109
Name: 88, dtype: object> | <bound method Series.min of column         sociot_warmth_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_warmth_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0172
std                                     0.0181
min                                    -0.0634
max                                     0.1109
Name: 88, dtype: object> | <bound method Series.max of column         sociot_warmth_responses_gpt-5.5
family                          Human-likeness
base_metric            sociot_warmth_responses
model                                  gpt-5.5
n_nonnull                                  728
mean                                    0.0172
std                                     0.0181
min                                    -0.0634
max                                     0.1109
Name: 88, dtype: object> |
| `std_sociot_warmth_responses_gpt-5.5` | 728 | <bound method Series.mean of column         std_sociot_warmth_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_warmth_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0096
std                                         0.0017
min                                         0.0064
max                                         0.0187
Name: 89, dtype: object> | <bound method Series.std of column         std_sociot_warmth_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_warmth_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0096
std                                         0.0017
min                                         0.0064
max                                         0.0187
Name: 89, dtype: object> | <bound method Series.min of column         std_sociot_warmth_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_warmth_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0096
std                                         0.0017
min                                         0.0064
max                                         0.0187
Name: 89, dtype: object> | <bound method Series.max of column         std_sociot_warmth_responses_gpt-5.5
family                              Human-likeness
base_metric            std_sociot_warmth_responses
model                                      gpt-5.5
n_nonnull                                      728
mean                                        0.0096
std                                         0.0017
min                                         0.0064
max                                         0.0187
Name: 89, dtype: object> |

## Sycophancy (12 columns)

| column | n | mean | std | min | max |
|---|---|---|---|---|---|
| `syco_framing_qwen-3.5-27B` | 732 | <bound method Series.mean of column         syco_framing_qwen-3.5-27B
family                        Sycophancy
base_metric                 syco_framing
model                       qwen-3.5-27B
n_nonnull                            732
mean                               0.935
std                                 0.17
min                                  0.0
max                                  1.0
Name: 934, dtype: object> | <bound method Series.std of column         syco_framing_qwen-3.5-27B
family                        Sycophancy
base_metric                 syco_framing
model                       qwen-3.5-27B
n_nonnull                            732
mean                               0.935
std                                 0.17
min                                  0.0
max                                  1.0
Name: 934, dtype: object> | <bound method Series.min of column         syco_framing_qwen-3.5-27B
family                        Sycophancy
base_metric                 syco_framing
model                       qwen-3.5-27B
n_nonnull                            732
mean                               0.935
std                                 0.17
min                                  0.0
max                                  1.0
Name: 934, dtype: object> | <bound method Series.max of column         syco_framing_qwen-3.5-27B
family                        Sycophancy
base_metric                 syco_framing
model                       qwen-3.5-27B
n_nonnull                            732
mean                               0.935
std                                 0.17
min                                  0.0
max                                  1.0
Name: 934, dtype: object> |
| `syco_framing_llama-3.3-70B` | 732 | <bound method Series.mean of column         syco_framing_llama-3.3-70B
family                         Sycophancy
base_metric                  syco_framing
model                       llama-3.3-70B
n_nonnull                             732
mean                               0.9597
std                                0.1342
min                                   0.0
max                                   1.0
Name: 935, dtype: object> | <bound method Series.std of column         syco_framing_llama-3.3-70B
family                         Sycophancy
base_metric                  syco_framing
model                       llama-3.3-70B
n_nonnull                             732
mean                               0.9597
std                                0.1342
min                                   0.0
max                                   1.0
Name: 935, dtype: object> | <bound method Series.min of column         syco_framing_llama-3.3-70B
family                         Sycophancy
base_metric                  syco_framing
model                       llama-3.3-70B
n_nonnull                             732
mean                               0.9597
std                                0.1342
min                                   0.0
max                                   1.0
Name: 935, dtype: object> | <bound method Series.max of column         syco_framing_llama-3.3-70B
family                         Sycophancy
base_metric                  syco_framing
model                       llama-3.3-70B
n_nonnull                             732
mean                               0.9597
std                                0.1342
min                                   0.0
max                                   1.0
Name: 935, dtype: object> |
| `syco_framing_gemma-4-31B` | 732 | <bound method Series.mean of column         syco_framing_gemma-4-31B
family                       Sycophancy
base_metric                syco_framing
model                       gemma-4-31B
n_nonnull                           732
mean                             0.9501
std                              0.1514
min                                 0.0
max                                 1.0
Name: 936, dtype: object> | <bound method Series.std of column         syco_framing_gemma-4-31B
family                       Sycophancy
base_metric                syco_framing
model                       gemma-4-31B
n_nonnull                           732
mean                             0.9501
std                              0.1514
min                                 0.0
max                                 1.0
Name: 936, dtype: object> | <bound method Series.min of column         syco_framing_gemma-4-31B
family                       Sycophancy
base_metric                syco_framing
model                       gemma-4-31B
n_nonnull                           732
mean                             0.9501
std                              0.1514
min                                 0.0
max                                 1.0
Name: 936, dtype: object> | <bound method Series.max of column         syco_framing_gemma-4-31B
family                       Sycophancy
base_metric                syco_framing
model                       gemma-4-31B
n_nonnull                           732
mean                             0.9501
std                              0.1514
min                                 0.0
max                                 1.0
Name: 936, dtype: object> |
| `syco_framing_gpt-5.5` | 732 | <bound method Series.mean of column         syco_framing_gpt-5.5
family                   Sycophancy
base_metric            syco_framing
model                       gpt-5.5
n_nonnull                       732
mean                         0.9483
std                          0.1605
min                             0.0
max                             1.0
Name: 937, dtype: object> | <bound method Series.std of column         syco_framing_gpt-5.5
family                   Sycophancy
base_metric            syco_framing
model                       gpt-5.5
n_nonnull                       732
mean                         0.9483
std                          0.1605
min                             0.0
max                             1.0
Name: 937, dtype: object> | <bound method Series.min of column         syco_framing_gpt-5.5
family                   Sycophancy
base_metric            syco_framing
model                       gpt-5.5
n_nonnull                       732
mean                         0.9483
std                          0.1605
min                             0.0
max                             1.0
Name: 937, dtype: object> | <bound method Series.max of column         syco_framing_gpt-5.5
family                   Sycophancy
base_metric            syco_framing
model                       gpt-5.5
n_nonnull                       732
mean                         0.9483
std                          0.1605
min                             0.0
max                             1.0
Name: 937, dtype: object> |
| `syco_validation_qwen-3.5-27B` | 732 | <bound method Series.mean of column         syco_validation_qwen-3.5-27B
family                           Sycophancy
base_metric                 syco_validation
model                          qwen-3.5-27B
n_nonnull                               732
mean                                 0.0255
std                                  0.1107
min                                     0.0
max                                     1.0
Name: 938, dtype: object> | <bound method Series.std of column         syco_validation_qwen-3.5-27B
family                           Sycophancy
base_metric                 syco_validation
model                          qwen-3.5-27B
n_nonnull                               732
mean                                 0.0255
std                                  0.1107
min                                     0.0
max                                     1.0
Name: 938, dtype: object> | <bound method Series.min of column         syco_validation_qwen-3.5-27B
family                           Sycophancy
base_metric                 syco_validation
model                          qwen-3.5-27B
n_nonnull                               732
mean                                 0.0255
std                                  0.1107
min                                     0.0
max                                     1.0
Name: 938, dtype: object> | <bound method Series.max of column         syco_validation_qwen-3.5-27B
family                           Sycophancy
base_metric                 syco_validation
model                          qwen-3.5-27B
n_nonnull                               732
mean                                 0.0255
std                                  0.1107
min                                     0.0
max                                     1.0
Name: 938, dtype: object> |
| `syco_validation_llama-3.3-70B` | 732 | <bound method Series.mean of column         syco_validation_llama-3.3-70B
family                            Sycophancy
base_metric                  syco_validation
model                          llama-3.3-70B
n_nonnull                                732
mean                                  0.0199
std                                   0.1051
min                                      0.0
max                                      1.0
Name: 939, dtype: object> | <bound method Series.std of column         syco_validation_llama-3.3-70B
family                            Sycophancy
base_metric                  syco_validation
model                          llama-3.3-70B
n_nonnull                                732
mean                                  0.0199
std                                   0.1051
min                                      0.0
max                                      1.0
Name: 939, dtype: object> | <bound method Series.min of column         syco_validation_llama-3.3-70B
family                            Sycophancy
base_metric                  syco_validation
model                          llama-3.3-70B
n_nonnull                                732
mean                                  0.0199
std                                   0.1051
min                                      0.0
max                                      1.0
Name: 939, dtype: object> | <bound method Series.max of column         syco_validation_llama-3.3-70B
family                            Sycophancy
base_metric                  syco_validation
model                          llama-3.3-70B
n_nonnull                                732
mean                                  0.0199
std                                   0.1051
min                                      0.0
max                                      1.0
Name: 939, dtype: object> |
| `syco_validation_gemma-4-31B` | 732 | <bound method Series.mean of column         syco_validation_gemma-4-31B
family                          Sycophancy
base_metric                syco_validation
model                          gemma-4-31B
n_nonnull                              732
mean                                0.0142
std                                 0.0829
min                                    0.0
max                                    1.0
Name: 940, dtype: object> | <bound method Series.std of column         syco_validation_gemma-4-31B
family                          Sycophancy
base_metric                syco_validation
model                          gemma-4-31B
n_nonnull                              732
mean                                0.0142
std                                 0.0829
min                                    0.0
max                                    1.0
Name: 940, dtype: object> | <bound method Series.min of column         syco_validation_gemma-4-31B
family                          Sycophancy
base_metric                syco_validation
model                          gemma-4-31B
n_nonnull                              732
mean                                0.0142
std                                 0.0829
min                                    0.0
max                                    1.0
Name: 940, dtype: object> | <bound method Series.max of column         syco_validation_gemma-4-31B
family                          Sycophancy
base_metric                syco_validation
model                          gemma-4-31B
n_nonnull                              732
mean                                0.0142
std                                 0.0829
min                                    0.0
max                                    1.0
Name: 940, dtype: object> |
| `syco_validation_gpt-5.5` | 732 | <bound method Series.mean of column         syco_validation_gpt-5.5
family                      Sycophancy
base_metric            syco_validation
model                          gpt-5.5
n_nonnull                          732
mean                            0.0222
std                             0.1091
min                                0.0
max                                1.0
Name: 941, dtype: object> | <bound method Series.std of column         syco_validation_gpt-5.5
family                      Sycophancy
base_metric            syco_validation
model                          gpt-5.5
n_nonnull                          732
mean                            0.0222
std                             0.1091
min                                0.0
max                                1.0
Name: 941, dtype: object> | <bound method Series.min of column         syco_validation_gpt-5.5
family                      Sycophancy
base_metric            syco_validation
model                          gpt-5.5
n_nonnull                          732
mean                            0.0222
std                             0.1091
min                                0.0
max                                1.0
Name: 941, dtype: object> | <bound method Series.max of column         syco_validation_gpt-5.5
family                      Sycophancy
base_metric            syco_validation
model                          gpt-5.5
n_nonnull                          732
mean                            0.0222
std                             0.1091
min                                0.0
max                                1.0
Name: 941, dtype: object> |
| `syco_indirectness_qwen-3.5-27B` | 732 | <bound method Series.mean of column         syco_indirectness_qwen-3.5-27B
family                             Sycophancy
base_metric                 syco_indirectness
model                            qwen-3.5-27B
n_nonnull                                 732
mean                                   0.2878
std                                    0.3322
min                                       0.0
max                                       1.0
Name: 942, dtype: object> | <bound method Series.std of column         syco_indirectness_qwen-3.5-27B
family                             Sycophancy
base_metric                 syco_indirectness
model                            qwen-3.5-27B
n_nonnull                                 732
mean                                   0.2878
std                                    0.3322
min                                       0.0
max                                       1.0
Name: 942, dtype: object> | <bound method Series.min of column         syco_indirectness_qwen-3.5-27B
family                             Sycophancy
base_metric                 syco_indirectness
model                            qwen-3.5-27B
n_nonnull                                 732
mean                                   0.2878
std                                    0.3322
min                                       0.0
max                                       1.0
Name: 942, dtype: object> | <bound method Series.max of column         syco_indirectness_qwen-3.5-27B
family                             Sycophancy
base_metric                 syco_indirectness
model                            qwen-3.5-27B
n_nonnull                                 732
mean                                   0.2878
std                                    0.3322
min                                       0.0
max                                       1.0
Name: 942, dtype: object> |
| `syco_indirectness_llama-3.3-70B` | 732 | <bound method Series.mean of column         syco_indirectness_llama-3.3-70B
family                              Sycophancy
base_metric                  syco_indirectness
model                            llama-3.3-70B
n_nonnull                                  732
mean                                    0.4213
std                                     0.3545
min                                        0.0
max                                        1.0
Name: 943, dtype: object> | <bound method Series.std of column         syco_indirectness_llama-3.3-70B
family                              Sycophancy
base_metric                  syco_indirectness
model                            llama-3.3-70B
n_nonnull                                  732
mean                                    0.4213
std                                     0.3545
min                                        0.0
max                                        1.0
Name: 943, dtype: object> | <bound method Series.min of column         syco_indirectness_llama-3.3-70B
family                              Sycophancy
base_metric                  syco_indirectness
model                            llama-3.3-70B
n_nonnull                                  732
mean                                    0.4213
std                                     0.3545
min                                        0.0
max                                        1.0
Name: 943, dtype: object> | <bound method Series.max of column         syco_indirectness_llama-3.3-70B
family                              Sycophancy
base_metric                  syco_indirectness
model                            llama-3.3-70B
n_nonnull                                  732
mean                                    0.4213
std                                     0.3545
min                                        0.0
max                                        1.0
Name: 943, dtype: object> |
| `syco_indirectness_gemma-4-31B` | 732 | <bound method Series.mean of column         syco_indirectness_gemma-4-31B
family                            Sycophancy
base_metric                syco_indirectness
model                            gemma-4-31B
n_nonnull                                732
mean                                  0.2659
std                                   0.3164
min                                      0.0
max                                      1.0
Name: 944, dtype: object> | <bound method Series.std of column         syco_indirectness_gemma-4-31B
family                            Sycophancy
base_metric                syco_indirectness
model                            gemma-4-31B
n_nonnull                                732
mean                                  0.2659
std                                   0.3164
min                                      0.0
max                                      1.0
Name: 944, dtype: object> | <bound method Series.min of column         syco_indirectness_gemma-4-31B
family                            Sycophancy
base_metric                syco_indirectness
model                            gemma-4-31B
n_nonnull                                732
mean                                  0.2659
std                                   0.3164
min                                      0.0
max                                      1.0
Name: 944, dtype: object> | <bound method Series.max of column         syco_indirectness_gemma-4-31B
family                            Sycophancy
base_metric                syco_indirectness
model                            gemma-4-31B
n_nonnull                                732
mean                                  0.2659
std                                   0.3164
min                                      0.0
max                                      1.0
Name: 944, dtype: object> |
| `syco_indirectness_gpt-5.5` | 732 | <bound method Series.mean of column         syco_indirectness_gpt-5.5
family                        Sycophancy
base_metric            syco_indirectness
model                            gpt-5.5
n_nonnull                            732
mean                              0.2671
std                               0.3061
min                                  0.0
max                                  1.0
Name: 945, dtype: object> | <bound method Series.std of column         syco_indirectness_gpt-5.5
family                        Sycophancy
base_metric            syco_indirectness
model                            gpt-5.5
n_nonnull                            732
mean                              0.2671
std                               0.3061
min                                  0.0
max                                  1.0
Name: 945, dtype: object> | <bound method Series.min of column         syco_indirectness_gpt-5.5
family                        Sycophancy
base_metric            syco_indirectness
model                            gpt-5.5
n_nonnull                            732
mean                              0.2671
std                               0.3061
min                                  0.0
max                                  1.0
Name: 945, dtype: object> | <bound method Series.max of column         syco_indirectness_gpt-5.5
family                        Sycophancy
base_metric            syco_indirectness
model                            gpt-5.5
n_nonnull                            732
mean                              0.2671
std                               0.3061
min                                  0.0
max                                  1.0
Name: 945, dtype: object> |

## Linguistic (elfen) (532 columns = 133 metrics × 4 models)

Column pattern: `ling_avg_Auditory_sensorimotor_<model>`. Per-column stats are in `metrics_overview.csv`. Base metrics:

- `ling_avg_Auditory_sensorimotor`
- `ling_avg_Foot_leg_sensorimotor`
- `ling_avg_Gustatory_sensorimotor`
- `ling_avg_Hand_arm_sensorimotor`
- `ling_avg_Haptic_sensorimotor`
- `ling_avg_Head_sensorimotor`
- `ling_avg_Interoceptive_sensorimotor`
- `ling_avg_Mouth_sensorimotor`
- `ling_avg_Olfactory_sensorimotor`
- `ling_avg_Torso_sensorimotor`
- `ling_avg_Visual_sensorimotor`
- `ling_avg_arousal`
- `ling_avg_dominance`
- `ling_avg_iconicity`
- `ling_avg_intensity_anger`
- `ling_avg_intensity_anticipation`
- `ling_avg_intensity_disgust`
- `ling_avg_intensity_fear`
- `ling_avg_intensity_joy`
- `ling_avg_intensity_sadness`
- `ling_avg_intensity_surprise`
- `ling_avg_intensity_trust`
- `ling_avg_prevalence`
- `ling_avg_sd_Auditory_sensorimotor`
- `ling_avg_sd_Foot_leg_sensorimotor`
- `ling_avg_sd_Gustatory_sensorimotor`
- `ling_avg_sd_Hand_arm_sensorimotor`
- `ling_avg_sd_Haptic_sensorimotor`
- `ling_avg_sd_Head_sensorimotor`
- `ling_avg_sd_Interoceptive_sensorimotor`
- `ling_avg_sd_Mouth_sensorimotor`
- `ling_avg_sd_Olfactory_sensorimotor`
- `ling_avg_sd_Torso_sensorimotor`
- `ling_avg_sd_Visual_sensorimotor`
- `ling_avg_sd_iconicity`
- `ling_avg_sd_socialness`
- `ling_avg_socialness`
- `ling_avg_valence`
- `ling_max_Auditory_sensorimotor`
- `ling_max_Foot_leg_sensorimotor`
- `ling_max_Gustatory_sensorimotor`
- `ling_max_Hand_arm_sensorimotor`
- `ling_max_Haptic_sensorimotor`
- `ling_max_Head_sensorimotor`
- `ling_max_Interoceptive_sensorimotor`
- `ling_max_Mouth_sensorimotor`
- `ling_max_Olfactory_sensorimotor`
- `ling_max_Torso_sensorimotor`
- `ling_max_Visual_sensorimotor`
- `ling_max_iconicity`
- `ling_max_prevalence`
- `ling_max_socialness`
- `ling_min_Auditory_sensorimotor`
- `ling_min_Foot_leg_sensorimotor`
- `ling_min_Gustatory_sensorimotor`
- `ling_min_Hand_arm_sensorimotor`
- `ling_min_Haptic_sensorimotor`
- `ling_min_Head_sensorimotor`
- `ling_min_Interoceptive_sensorimotor`
- `ling_min_Mouth_sensorimotor`
- `ling_min_Olfactory_sensorimotor`
- `ling_min_Torso_sensorimotor`
- `ling_min_Visual_sensorimotor`
- `ling_min_iconicity`
- `ling_min_prevalence`
- `ling_min_socialness`
- `ling_n_controversial_Auditory_sensorimotor`
- `ling_n_controversial_Foot_leg_sensorimotor`
- `ling_n_controversial_Gustatory_sensorimotor`
- `ling_n_controversial_Hand_arm_sensorimotor`
- `ling_n_controversial_Haptic_sensorimotor`
- `ling_n_controversial_Head_sensorimotor`
- `ling_n_controversial_Interoceptive_sensorimotor`
- `ling_n_controversial_Mouth_sensorimotor`
- `ling_n_controversial_Olfactory_sensorimotor`
- `ling_n_controversial_Torso_sensorimotor`
- `ling_n_controversial_Visual_sensorimotor`
- `ling_n_controversial_iconicity`
- `ling_n_controversial_socialness`
- `ling_n_high_Auditory_sensorimotor`
- `ling_n_high_Foot_leg_sensorimotor`
- `ling_n_high_Gustatory_sensorimotor`
- `ling_n_high_Hand_arm_sensorimotor`
- `ling_n_high_Haptic_sensorimotor`
- `ling_n_high_Head_sensorimotor`
- `ling_n_high_Interoceptive_sensorimotor`
- `ling_n_high_Mouth_sensorimotor`
- `ling_n_high_Olfactory_sensorimotor`
- `ling_n_high_Torso_sensorimotor`
- `ling_n_high_Visual_sensorimotor`
- `ling_n_high_arousal`
- `ling_n_high_dominance`
- `ling_n_high_iconicity`
- `ling_n_high_intensity_anger`
- `ling_n_high_intensity_anticipation`
- `ling_n_high_intensity_disgust`
- `ling_n_high_intensity_fear`
- `ling_n_high_intensity_joy`
- `ling_n_high_intensity_sadness`
- `ling_n_high_intensity_surprise`
- `ling_n_high_intensity_trust`
- `ling_n_high_prevalence`
- `ling_n_high_socialness`
- `ling_n_high_valence`
- `ling_n_low_Auditory_sensorimotor`
- `ling_n_low_Foot_leg_sensorimotor`
- `ling_n_low_Gustatory_sensorimotor`
- `ling_n_low_Hand_arm_sensorimotor`
- `ling_n_low_Haptic_sensorimotor`
- `ling_n_low_Head_sensorimotor`
- `ling_n_low_Interoceptive_sensorimotor`
- `ling_n_low_Mouth_sensorimotor`
- `ling_n_low_Olfactory_sensorimotor`
- `ling_n_low_Torso_sensorimotor`
- `ling_n_low_Visual_sensorimotor`
- `ling_n_low_arousal`
- `ling_n_low_dominance`
- `ling_n_low_iconicity`
- `ling_n_low_intensity_anger`
- `ling_n_low_intensity_anticipation`
- `ling_n_low_intensity_disgust`
- `ling_n_low_intensity_fear`
- `ling_n_low_intensity_joy`
- `ling_n_low_intensity_sadness`
- `ling_n_low_intensity_surprise`
- `ling_n_low_intensity_trust`
- `ling_n_low_prevalence`
- `ling_n_low_socialness`
- `ling_n_low_valence`
- `ling_n_negative_sentiment`
- `ling_n_positive_sentiment`
- `ling_n_tokens`
- `ling_sentiment_score`

## Complexity (312 columns = 78 metrics × 4 models)

Column pattern: `cplx_additive_connectives_<model>`. Per-column stats are in `metrics_overview.csv`. Base metrics:

- `cplx_additive_connectives`
- `cplx_adjectives_density`
- `cplx_adverbs_density`
- `cplx_adversative_connectives`
- `cplx_argument_overlap_adjacent`
- `cplx_argument_overlap_all`
- `cplx_average_age_of_acquisition`
- `cplx_average_cefr_level`
- `cplx_average_concreteness`
- `cplx_average_familiarity`
- `cplx_average_imagery`
- `cplx_average_meaningfulness`
- `cplx_average_number_of_clauses_per_sentence`
- `cplx_average_number_of_commas_per_sentence`
- `cplx_average_number_of_meaning_per_word`
- `cplx_average_sentence_length`
- `cplx_causal_connectives`
- `cplx_coca_academic_range`
- `cplx_coleman_liau_index`
- `cplx_concept_density_concepts_per_sentence`
- `cplx_conceptual_graph_ontology_number_of_concpets`
- `cplx_conceptual_graph_ontology_number_of_distinct_concepts`
- `cplx_connectives`
- `cplx_content_word_frequency_log`
- `cplx_content_word_overlap_adjacent`
- `cplx_content_word_overlap_all`
- `cplx_dale_chall_readability_score`
- `cplx_dependency_parser_branching`
- `cplx_dependency_parser_dependency_distance`
- `cplx_dependency_parser_tree_depth`
- `cplx_dissimilarity_of_words_between_sentences`
- `cplx_first_person_pronouns_density`
- `cplx_flesch_kincaid_grade_level`
- `cplx_gunning_fog_index`
- `cplx_knowledge_graph_average_node_pagerank`
- `cplx_knowledge_graph_number_of_connected_components`
- `cplx_linsear_write_formula`
- `cplx_logical_connectives`
- `cplx_mattr`
- `cplx_max_kuperman_age_of_acquisition`
- `cplx_max_number_of_clauses_per_sentence`
- `cplx_max_number_of_if_per_sentence`
- `cplx_max_number_of_wh_clauses_per_sentence`
- `cplx_mean_word_length`
- `cplx_median_kuperman_age_of_acquisition`
- `cplx_modifiers_per_noun_phrase`
- `cplx_negations_density`
- `cplx_noun_overlap_adjacent`
- `cplx_nouns_density`
- `cplx_number_of_connectives`
- `cplx_number_of_connectives_per_3_sentence_sliding_window`
- `cplx_number_of_wordnet_hypernyms_per_word`
- `cplx_number_of_wordnet_hyponyms_per_word`
- `cplx_overlap_between_adjacent_sents_based_on_argument_bearing_words`
- `cplx_passive_constructions_density`
- `cplx_percentage_of_words_above_b1_level`
- `cplx_percentage_of_words_with_more_than_5_meanings`
- `cplx_polysemy`
- `cplx_pos_dissimilarity_between_sentences`
- `cplx_pronouns_density`
- `cplx_reading_time`
- `cplx_stem_overlap_sent`
- `cplx_syllables_per_word`
- `cplx_te_score`
- `cplx_temporal_cohesions`
- `cplx_temporal_connectives`
- `cplx_text_length`
- `cplx_third_person_pronouns_density`
- `cplx_type_token_ratio`
- `cplx_verb_aspect_repetition`
- `cplx_verb_overlap_adjacent`
- `cplx_verb_tense_repetition`
- `cplx_verb_tense_repetition_nltk`
- `cplx_verb_ttr`
- `cplx_verb_ttr_adj`
- `cplx_verbs_density`
- `cplx_word_concreteness`
- `cplx_word_frequency_log`

## Identifier / demographics (42 columns)

`user`, `social_class`, `gender`, `gender_other`, `age`, `nationality`, `ethnicity`, `ethnicity_other`, `marital`, `marital_other`, `language`, `language_other`, `religion`, `religion_other`, `education`, `mum_education`, `dad_education`, `home`, `home_other`, `employment`, `occupation`, `mother_occupation`, `father_occupation`, `hobbies`, `hobbies_other`, `tech`, `tech_other`, `know_nlp`, `know_nlp_other`, `use_nlp`, `use_nlp_other`, `would_nlp`, `would_nlp_other`, `frequency_llm`, `llm_use`, `llm_other`, `usecases`, `usecases_other`, `contexts`, `contexts_other`, `comments`, `ses`
