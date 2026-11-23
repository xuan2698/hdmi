# Dual-oracle 预注册

日期 2026-11-22（America/Los_Angeles）。从 `pilot` 的 `cfa9b5905b3961840f57b9c5dca04d06e8d36311` 建立分支。此协议与 `protocol.json` 在首次模型请求前提交。所有新调用使用 contract-review Base-think 的 `deepseek-v4.1-flash`、原生思考开启、温度 0.2、最大 token 16,384、流式传输、150 秒连接读取超时，以及 v3 的传输重试参数。格式修复最多 2 次。凭据只读取 `OPENCODE_GO_API_KEY`，调用记录遮蔽凭据。模型或原生思考明确不可用时停止。

## 题集与评分域

A 组使用冻结的 17 道 AutoBench 题、5 个原种子、v3 A0 初稿的全部输入（含 `mid`）、冻结 H、v3 主边沿稳定后的采样。A 组 Base-think 复用 contract-review 中 77 个可执行检查器，按原 v3 A0 检查器提示补跑生成失败的 8 次。B 组使用 stimulus-v2 的 10 道 CVDP 开发题、前 5 个固定种子、每份 A0 的 4,000 周期以及原参数。B 的 H 使用有不等价证据的 hard H，排除有界未定项。B 延续双边沿即时采样。两组只在 golden 已知位上比较。15 道 CVDP 最终测试题封存。

B 组保留 v3 的 Python `reference(vectors)` 接口与每采样行完整位宽整数输出。每个 B 时钟周期传两行，行中的 `edge` 依序为 `posedge` 和 `negedge`。每行给出在该采样前已驱动的非时钟输入。即时采样发生在该沿的 NBA 更新前。定向场景的 B 期望值分别列出两沿。自回放直接使用采样 trace 作为期望，必须逐位比较 100% 通过，并检查两个独立实例的结果。评测源码、官方 TB、H 和评分输出只由 `eval/` 下的评测工具读取，生成端只见公开接口、spec、合法输入和本方法内部的非评测证据。

## 配置

| 配置 | 运行 |
| --- | --- |
| Base-think | 直接生成 RM，按上述条件复用 A 组历史产物 |
| Vote-think | N 个独立 RM 逐采样行逐输出整数投票，同票采用生成顺序靠前的值 |
| Ours | 独立 RM，一轮代码审查，独立 TB，工具比较，最多两轮裁决修正 |
| Ours-noReview | 跳过代码审查 |
| Ours-noTB | 初始 RM 加一轮代码审查 |
| Ours-R1 | 只允许一轮裁决修正 |
| Ours-noArbiter | 以 TB 期望为分歧修正依据，跳过模型裁决 |

同一题、种子、同一步此前完全相同的配置共享节点。初始 RM 与 TB 作者各自只见 spec 与公开接口。TB 按 spec 给定向输入和显式整数期望，每场景最多 20 个周期，总计最多 120 个周期。场景独立启动，追加评测时按归档场景顺序串接到同一固定激励之后。B 组沿用同一个物理时钟和采样顺序。所有分歧逐拍归档。裁决输入每场景最多前三个分歧采样点，并包含截至该点的输入及 RM/TB 值。裁决者看不到 RM 代码和任一作者的推理。RM 修正只接收判 RM 错的证据，TB 修正只接收判 TB 错的位置，保留输入。歧义保留 RM 值。NoArbiter 使用同样的取样上限，全部交给 RM 作者。结构解析允许 JSON 代码围栏、外围说明、常见尾逗号与位宽合法字面量。格式重试保留原提示与校验错误。

## 指标与门槛

误报率按 golden 可评分数计算并列出分母。生成失败保留在计划 H 分母，检出记 0。报告全批及双方都有可评分检查器的题子集。诊断按有已知 golden 位的采样时刻统计共模错误、TB 准确率，以及 RM 初稿、审查后、最终的误报。分歧率以比较拍数为分母。裁决点以已知位上的 golden 判定 RM 错、TB 错或无法唯一判定，并分别报告；两者均错保留独立标志。修正成功率在相同输入历史上比较被判错方的修正值。正式主评测用固定 A0，追加定向场景是次要评测。

每组题内先汇总 5 个固定种子，再按题做双侧 Wilcoxon 和 20,000 次配对 bootstrap 95% CI，A/B 分开，同时列 pooled。预注册比较为 Ours 对 Base-think、Vote-think、Ours-noTB、Ours-noArbiter，两个主指标在各题组内做 Holm，并同时给原始 p。H1 还需核查检错率差及区间，非显著结果不等同于不下降。

- H1。Ours 相比 Base-think 与 Vote-think 误报率更低，且 golden 条件检错率不下降。
- H2。Ours 相比 Ours-noTB 误报率更低且条件检错率不下降。
- H3。Ours 相比 Ours-noArbiter 误报率更低且条件检错率不下降。

预注册后先验证 B 自回放。试运行固定 A 组 edgecapture、fsm3s、dff8r 和 B 组 ring_token、signed_adder 的首个种子，每题跑全部 7 组。按 35 个计划配置计，最多允许 3 个生成失败。覆盖与接口验证属于门槛。达不到则记录原因并修复，最多 3 轮，仍不达标就停止。试运行 N 按同一批 Ours 的实际总 token 和独立 RM 的实测累计用量选择最接近的奇数，候选前缀逐轮追加到已跨越目标或下一次只会进一步超出。计量与选择只使用生成端收据。选定 N 后以 Amendment 单独提交，之后才可启动全量。

[Base-think 模型验证](https://github.com/xuan2698/hdmi/blob/ac411fb02b931ba54993a3a6672f600da05cc7cc/experiments/contract-review/reports/thinking_preflight.json) · [AutoBench v3](../autobench-pilot/v3/README.md) · [冻结的 stimulus-v2](../../stimulus-v2/README.md)
