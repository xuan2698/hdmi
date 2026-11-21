# Formal-cex Amendment 1 执行记录

[来源和 SHA-256](V2_PROVENANCE.md) · [独立预注册修订](https://github.com/xuan2698/hdmi/commit/de8bd6eab3cf54339da71f563d20ead732153d5e) · [100 份代理冻结提交](https://github.com/xuan2698/hdmi/commit/8a77baf26bca1fc06a576033d4d6b536602209c8)

修订推送后，才用锁定的 `deepseek-v4.1-flash` 推理参数生成 CVDP 代理。100 个有效槽位及 SHA-256 已提交。Copilot 的九道题使用发布的 `instruction` 中的规格说明，去掉其中围栏内的 TB 片段。Agentic RAM 使用独立发布的规格 Markdown。首次抽取只看了 `spec_files`，使部分 Copilot 请求缺少题面，相关响应全部在冻结前剔除。留下 21 次 HTTP 尝试的回执，因中止而无回执的在途请求用量未核实。首次已收到完整 Markdown 的 RAM P01 保留，后续通用提示额外说明如何解释 Copilot 的 TB 题面。[有效代理清单](../generation/proxy_inventory.csv) · [抽取修正记录](../archive/discarded_empty_spec/incident.json)

## 工具链门槛

冻结的代理里，99 份通过接口与基础运行检查并生成各 24 个规则型 G，形成 **2,376 对**。秒表有一份代理未提供有效输出，保留在代理槽位和 eval 报告的分母内。本阶段用 Boolector 再用 Z3，20、40、80 周期用同一递增搜索覆盖。先做快速求解，未定的对继续运行完整 BMC，阶段内保持每对 120 秒上限。计入确认 BMC 反例与满足 80 周期目标的有界结果，额外单列经仿真复放的反例。只有在矩阵齐备后才输出对照门槛判断。[门槛与上下界](stage0_amended_gate.csv) · [逐题汇总](stage0_amended_by_task.csv) · [逐对原始数据](stage0_amended_pairs.csv)

1. 最初运行逐子步进行断言检查，又在每步重查输入假设。在短样本后中止，保留已完成的结果。IIR 的十份代理在允许的 16 位固定宽度上已实现接口，额外绑不存在的 WIDTH 参数使其被误拒。修复只识别六个 16 位数据端口齐备的代理，保留原始拒绝原因、原文件和 SHA-256。
2. 第一轮改进使用已有比较模型，按四个子步成组检查断言，减少重复假设检查，并尝试 k 归纳。归纳成功的结果同时证实三个有限深度。RAM 先以八地址搜索候选反例，只有完整参数下复放通过才纳入；该切片的有界通过不计入完整 RAM 的证明。中止前归档已完成的样本。
3. 第二轮把可从 Yosys 直接暴露的共同内部信号加入充分性证明，成功才采用。证明不了时以原输出属性继续 BMC。排查还发现 SBY 超时后会遗留合成进程，已回收本实验目录所属的孤儿子进程，并为后续超时处理加了限域回收。

hard H、Oracle-F、主比较和 HDLBits 次要比较的结果未作为阶段 0 的输入。

## 代理 RTL 独立 eval

CVDP 原发行条目在十题上只给出待生成 TB 文件名，没有可执行的官方正确性 TB 源码。官测通过率记为未定义。独立评测另报告有限差分回放结果。评测脚本取 stimulus-v2 前五个固定种子的归档 A0-long 向量，每个 20,000 周期。相同输入下在两个时钟沿比较 proxy 与发布参考 RTL 的输出，并屏蔽参考 X。通过表示在这些向量及当前评分域内一致。两种分母均列出，评测结果不参与 G 选择与形式化门槛。[评测入口](../eval/proxy_quality.py) · [逐个代理](proxy_eval.csv) · [逐题分母和比例](proxy_eval_by_task.csv)

| CVDP 开发题 | 回放通过 / 可评分 | 回放通过 / 全部槽位 |
| --- | ---: | ---: |
| byte_enable_ram_0004 | 10/10 | 10/10 |
| asyc_reset_0004 | 10/10 | 10/10 |
| digital_stopwatch_0017 | 0/9 | 0/10 |
| ring_token_0004 | 0/10 | 0/10 |
| manchester_enc_0009 | 0/10 | 0/10 |
| signed_adder_0003 | 0/10 | 0/10 |
| IIR_filter_0012 | 0/10 | 0/10 |
| hill_cipher_0012 | 0/10 | 0/10 |
| simple_spi_0003 | 0/10 | 0/10 |
| word_change_detector_0012 | 0/10 | 0/10 |
| 合计 | 20/99 | 20/100 |

79 份代理在参考输出上出现差异，另 1 份秒表代理的接口不匹配。proxy/G 的反例只能说明相应的代理和规则变异体在那段输入下不同。是否迁移到目标 RTL 与 hard H 需要单独的冻结评测。

## 可恢复的求解记录

2,376 个槽位对应 1,673 个不同配对。复用键包括题号、端口和参数、源代理 token、源 G token。含编译指令、工具注释或解析诊断的文件按原始字节识别。每个槽位保留单独的结果行，复用行注明其源槽位。工具的短尝试与后续 BMC 共用单对预算。短尝试的未定结果沿用为未决，直到完整求解确认状态。计入归纳证明时记录三个已覆盖的深度。

现有复位惯例为对有复位端口的设计强制第一拍复位，方向由代理敏感边沿或清晰的低有效命名推断，并记录在 G 清单及逐对结果中。求解进程另由限时子进程回收器包裹。合成进程异常遗留时，仅清理本实验的作业目录。

已有 100 个有效生成调用，对应 101 次 HTTP 尝试和 192,317 token。计量回执显示 Go 额度消耗 USD 0.03672963，早期剔除批次的回执单列。修订提交时间早于本实验的所有已归档回执。

冻结代理已包含在仓库分支中。从仓库根目录复查阶段 0。执行环境需提供 Yosys、SymbiYosys、Boolector、Z3、Icarus 和 Python 的 pyarrow、pyslang。先前的作业记录可用于断点恢复。

```sh
python3 experiments/formal-cex/stage0.py --repair 2 --quick --workers 6
python3 experiments/formal-cex/stage0.py --repair 2 --workers 6
python3 experiments/formal-cex/report_stage0.py
```

## 已发布的阶段 0 检查点

快速检查已结束，仍未定的配对已进入完整 BMC。发布时的已完成数、成功数和未决数见门槛 CSV。已完成子集的比例用于显示进度，门槛仍以冻结矩阵全体为分母。主比较、Oracle-F 和 HDLBits 次要比较尚未启动。[完整 BMC 检查点](stage0_amended_gate.csv)

独立 eval 还按代理回放结果汇总了各类代理贡献的已复放反例和有界证明。输出不一致的代理仍会产生可复放的 proxy/G 反例。这项统计区分代理层面的反例证据和目标评测效果，未用来筛选 G。[eval 侧交叉汇总](proxy_eval_formal_join.csv)
