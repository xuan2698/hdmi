# Dual-oracle 五题试运行

计划 35 个配置，0 个生成失败（0.00%，门槛用此口径）。Vote-think 使用 3 个独立成员。CVDP golden 自回放在 50 份冻结输入上通过。

独立生成路径有 0/44 条失败（0.00%），另有 0 条未达终态。按独立产物目录统计，重试只计一路。[逐路径数据](pilot_generation_paths.csv) · [接口核对](../TOKEN_LIMIT.md)

[预注册](../../PREREG.md) · [逐次结果](pilot_by_run.csv) · [逐题结果](pilot_by_task.csv)

## 主指标和追加场景评测

误报率基于可评分检查器。生成失败保留在 H 的计划分母并计零检出。所有单元均在门槛处封存的配置显示为空。部分封存时 H 为已观测的计划分母下界。追加评测沿同一场景输入顺序接到 A0 之后。

| 组 | 配置 | 激励 | 可评分/计划 | 误报 macro | 误报 pooled | H macro | H pooled | 新增 Token | Go USD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | Base-think | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 13884 | 0.00945 |
| A | Base-think | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 13884 | 0.00945 |
| A | Vote-think | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 34981 | 0.02370 |
| A | Vote-think | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 34981 | 0.02370 |
| A | Ours | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| A | Ours | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| A | Ours-noReview | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 43047 | 0.02960 |
| A | Ours-noReview | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 43047 | 0.02960 |
| A | Ours-noTB | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 19532 | 0.01289 |
| A | Ours-noTB | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 19532 | 0.01289 |
| A | Ours-R1 | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| A | Ours-R1 | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| A | Ours-noArbiter | primary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| A | Ours-noArbiter | secondary | 3/3 | 0.00% | 0.00% | 96.30% | 96.55% | 54708 | 0.03731 |
| B | Base-think | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 50968 | 0.03551 |
| B | Base-think | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 50968 | 0.03551 |
| B | Vote-think | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 125575 | 0.08646 |
| B | Vote-think | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 125575 | 0.08646 |
| B | Ours | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 267749 | 0.17720 |
| B | Ours | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 267749 | 0.17720 |
| B | Ours-noReview | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 129987 | 0.08289 |
| B | Ours-noReview | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 129987 | 0.08289 |
| B | Ours-noTB | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 137305 | 0.09517 |
| B | Ours-noTB | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 137305 | 0.09517 |
| B | Ours-R1 | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 204331 | 0.13799 |
| B | Ours-R1 | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 204331 | 0.13799 |
| B | Ours-noArbiter | primary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 186279 | 0.12685 |
| B | Ours-noArbiter | secondary | 2/2 | 100.00% | 100.00% | 0.00% | 0.00% | 186279 | 0.12685 |

## 题级配对

误报的主比较使用双方均可评分的题，H 主比较使用全部计划题。计划分母误报下界和共同可评分 H 另列在 CSV。正差意味着 Ours 较高。A/B 分别做主比较 Holm 校正。

| 组 | 对照 | 指标 | 题对 | 差值 pp | 95% CI pp | Wilcoxon p | Holm p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Base-think | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Base-think | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Vote-think | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Vote-think | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noTB | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noTB | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noArbiter | FP | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| A | Ours-noArbiter | H | 3 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Base-think | FP | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Base-think | H | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Vote-think | FP | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Vote-think | H | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noTB | FP | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noTB | H | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noArbiter | FP | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |
| B | Ours-noArbiter | H | 2 | +0.00 | [+0.00, +0.00] | 1 | 1 |

[全部配对](pilot_paired.csv)

## 共模错误和裁决

共模错误分母为至少一个已知 golden 位的采样点。裁决表中的 ambiguous 表示 golden 已知位无法区分候选。此标签只衡量观测值。两边都错误时单列。

| 组 | 配置 | 阶段 | 分歧拍率 | 共模错误 | TB 准确率 | 已知采样 |
| --- | --- | --- | --- | --- | --- | --- |
| A | Ours | final | 0.00% | 0.00% | 100.00% | 95 |
| A | Ours-noReview | final | 0.00% | 0.00% | 100.00% | 95 |
| A | Ours-R1 | final | 0.00% | 0.00% | 100.00% | 95 |
| A | Ours-noArbiter | final | 0.00% | 0.00% | 100.00% | 95 |
| A | RM-stages | initial | 0.00% | 0.00% | 100.00% | 95 |
| A | RM-stages | reviewed | 0.00% | 0.00% | 100.00% | 95 |
| A | RM-stages | final | 0.00% | 0.00% | 100.00% | 95 |
| B | Ours | final | 0.00% | 68.03% | 31.97% | 122 |
| B | Ours-noReview | final | 44.26% | 23.77% | 31.97% | 122 |
| B | Ours-R1 | final | 44.26% | 23.77% | 31.97% | 122 |
| B | Ours-noArbiter | final | 0.00% | 68.03% | 31.97% | 122 |
| B | RM-stages | initial | 44.26% | 23.77% | 31.97% | 122 |
| B | RM-stages | reviewed | 44.26% | 23.77% | 31.97% | 122 |
| B | RM-stages | final | 0.00% | 68.03% | 31.97% | 122 |

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
| B | verdict | RM | 36 | 36 | 0.00% | 36 | 8.33% |
| B | verdict | TB | 0 | 0 | — | 0 | — |
| B | verdict | ambiguous | 0 | 0 | — | 0 | — |
| B | verdict | both_wrong | 0 | 0 | — | 0 | — |
| B | verdict | untraceable | 0 | 0 | — | 0 | — |
| B | actual | RM | 0 | 0 | — | 0 | — |
| B | actual | TB | 6 | 6 | 0.00% | 6 | 50.00% |
| B | actual | ambiguous | 0 | 0 | — | 0 | — |
| B | actual | both_wrong | 30 | 30 | 0.00% | 30 | 0.00% |
| B | actual | untraceable | 0 | 0 | — | 0 | — |

| 组 | RM 阶段 | 可评分 | 误报率 |
| --- | --- | --- | --- |
| A | initial | 3 | 0.00% |
| A | reviewed | 3 | 0.00% |
| A | final | 3 | 0.00% |
| B | initial | 2 | 100.00% |
| B | reviewed | 2 | 100.00% |
| B | final | 2 | 100.00% |

## 用量和案例

收据去重后共 45 次逻辑调用、47 次传输、611,692 token，Go 用量 USD 0.405160，额外扣费 USD 0.000000。历史 Base-think 用量在原始结果中单列。共享节点在配置归属用量中可重复出现。

可归档完整 Ours 单元 5 个，共模错误场景 40 个，裁决与观测不符 36 个点。

[试运行各阶段样例](pilot_examples.json) · [共模错误](pilot_common_mode_examples.json) · [裁决错误](pilot_arbiter_error_examples.json) · [门槛](pilot_gate.json)
