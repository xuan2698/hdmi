# Dual-oracle 五题试运行

计划 35 个配置，6 个生成失败。7 个配置因停止规则封存。Vote-think 的 N 未完成标定。CVDP golden 自回放在 50 份冻结输入上通过。

[预注册](../PREREG.md) · [逐次结果](pilot_by_run.csv) · [逐题结果](pilot_by_task.csv)

## 主指标和追加场景评测

误报率基于可评分检查器。生成失败保留在 H 的计划分母并计零检出。所有单元均在门槛处封存的配置显示为空。部分封存时 H 为已观测的计划分母下界。追加评测沿同一场景输入顺序接到 A0 之后。

| 组 | 配置 | 激励 | 可评分/计划 | 误报 macro | 误报 pooled | H macro | H pooled | 新增 Token | Go USD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | Base-think | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 0 | 0.00000 |
| A | Base-think | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 0 | 0.00000 |
| A | Vote-think | primary | 0/3 | — | — | — | — | 6433 | 0.00414 |
| A | Vote-think | secondary | 0/3 | — | — | — | — | 6433 | 0.00414 |
| A | Ours | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| A | Ours | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| A | Ours-noReview | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 87312 | 0.06077 |
| A | Ours-noReview | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 87312 | 0.06077 |
| A | Ours-noTB | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 23090 | 0.01568 |
| A | Ours-noTB | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 23090 | 0.01568 |
| A | Ours-R1 | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| A | Ours-R1 | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| A | Ours-noArbiter | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| A | Ours-noArbiter | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 96703 | 0.06697 |
| B | Base-think | primary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 136825 | 0.09367 |
| B | Base-think | secondary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 136825 | 0.09367 |
| B | Vote-think | primary | 0/2 | — | — | — | — | 0 | 0.00000 |
| B | Vote-think | secondary | 0/2 | — | — | — | — | 0 | 0.00000 |
| B | Ours | primary | 0/2 | — | — | 0.00% | 0.00% | 286319 | 0.18981 |
| B | Ours | secondary | 0/2 | — | — | 0.00% | 0.00% | 286319 | 0.18981 |
| B | Ours-noReview | primary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 260031 | 0.17438 |
| B | Ours-noReview | secondary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 260031 | 0.17438 |
| B | Ours-noTB | primary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 162718 | 0.10984 |
| B | Ours-noTB | secondary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 162718 | 0.10984 |
| B | Ours-R1 | primary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 276995 | 0.18413 |
| B | Ours-R1 | secondary | 1/2 | 100.00% | 100.00% | 0.00% | 0.00% | 276995 | 0.18413 |
| B | Ours-noArbiter | primary | 0/2 | — | — | 0.00% | 0.00% | 280123 | 0.18726 |
| B | Ours-noArbiter | secondary | 0/2 | — | — | 0.00% | 0.00% | 280123 | 0.18726 |

## 题级配对

误报的主比较使用双方均可评分的题，H 主比较使用全部计划题。计划分母误报下界和共同可评分 H 另列在 CSV。正差意味着 Ours 较高。A/B 分别做主比较 Holm 校正。

| 组 | 对照 | 指标 | 题对 | 差值 pp | 95% CI pp | Wilcoxon p | Holm p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Base-think | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Base-think | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noTB | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noTB | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noArbiter | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noArbiter | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Base-think | H | 1 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noTB | H | 1 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noArbiter | H | 1 | +0.00 | [+0.00, +0.00] | 1 | 1 |

[全部配对](pilot_paired.csv)

## 共模错误和裁决

共模错误分母为至少一个已知 golden 位的采样点。裁决表中的 ambiguous 表示 golden 已知位无法区分候选。此标签只衡量观测值。两边都错误时单列。

| 组 | 配置 | 阶段 | 分歧拍率 | 共模错误 | TB 准确率 | 已知采样 |
| --- | --- | --- | --- | --- | --- | --- |
| A | Ours | final | 0.00% | 0.00% | 100.00% | 122 |
| A | Ours-noReview | final | 0.00% | 0.00% | 100.00% | 122 |
| A | Ours-R1 | final | 0.00% | 0.00% | 100.00% | 122 |
| A | Ours-noArbiter | final | 0.00% | 0.00% | 100.00% | 122 |
| A | RM-stages | initial | 0.00% | 0.00% | 100.00% | 122 |
| A | RM-stages | reviewed | 0.00% | 0.00% | 100.00% | 122 |
| A | RM-stages | final | 0.00% | 0.00% | 100.00% | 122 |
| B | Ours-noReview | final | 0.00% | 20.00% | 80.00% | 60 |
| B | Ours-R1 | final | 3.33% | 20.00% | 80.00% | 60 |
| B | RM-stages | initial | 3.33% | 20.00% | 80.00% | 60 |
| B | RM-stages | reviewed | 3.33% | 20.00% | 80.00% | 60 |

| 组 | 核对分组 | 类别 | 点数 | 可追溯 | 核对率 | 修正可评分 | 修正成功率 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | verdict | RM | 0 | 0 | — | 0 | — |
| A | verdict | TB | 0 | 0 | — | 0 | — |
| A | verdict | ambiguous | 0 | 0 | — | 0 | — |
| A | verdict | both_wrong | 0 | 0 | — | 0 | — |
| A | verdict | untraceable | 0 | 0 | — | 0 | — |
| A | actual | RM | 0 | 0 | — | 0 | — |
| A | actual | TB | 0 | 0 | — | 0 | — |
| A | actual | ambiguous | 0 | 0 | — | 0 | — |
| A | actual | both_wrong | 0 | 0 | — | 0 | — |
| A | actual | untraceable | 0 | 0 | — | 0 | — |
| B | verdict | RM | 1 | 1 | 100.00% | 0 | — |
| B | verdict | TB | 1 | 1 | 0.00% | 0 | — |
| B | verdict | ambiguous | 0 | 0 | — | 0 | — |
| B | verdict | both_wrong | 0 | 0 | — | 0 | — |
| B | verdict | untraceable | 0 | 0 | — | 0 | — |
| B | actual | RM | 2 | 2 | 50.00% | 0 | — |
| B | actual | TB | 0 | 0 | — | 0 | — |
| B | actual | ambiguous | 0 | 0 | — | 0 | — |
| B | actual | both_wrong | 0 | 0 | — | 0 | — |
| B | actual | untraceable | 0 | 0 | — | 0 | — |

| 组 | RM 阶段 | 可评分 | 误报率 |
| --- | --- | --- | --- |
| A | initial | 3 | 0.00% |
| A | reviewed | 3 | 0.00% |
| A | final | 3 | 0.00% |
| B | initial | 1 | 100.00% |
| B | reviewed | 1 | 100.00% |
| B | final | 0 | — |

## 用量和案例

收据去重后共 51 次逻辑调用、88 次传输、941,333 token，Go 用量 USD 0.634986，额外扣费 USD 0.000000。历史 Base-think 用量在原始结果中单列。共享节点在配置归属用量中可重复出现。

可归档完整 Ours 单元 3 个，共模错误场景 12 个，裁决与观测不符 1 个点。

[试运行各阶段样例](pilot_examples.json) · [共模错误](pilot_common_mode_examples.json) · [裁决错误](pilot_arbiter_error_examples.json) · [门槛](pilot_gate.json)

停止前的场景归档发现了 ID 碰撞。配对按输入历史和原 TB 值追溯，不能唯一定位的点单列。碰撞路径上的 TB 定点修正不计成功率。原始生成产物保持归档。
