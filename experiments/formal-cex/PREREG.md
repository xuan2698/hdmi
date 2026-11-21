# Formal-cex 主比较预注册

基线为 `pilot` 的 `cfa9b5905b3961840f57b9c5dca04d06e8d36311`。沿用 stimulus-v2 的 10 道 CVDP 开发题、可覆盖参数、hard H 和 `deepseek-v4.1-flash` 锁定推理参数。取该协议固定种子列表的前 5 个，每题每配置 5 次。最终测试集继续封存。[题目及参数](../../stimulus-v1/split.json) · [stimulus-v2 协议](../../stimulus-v2/README.md)

## 数据边界和阶段 0

生成端的输入为指定开发题的 spec、CorrectBench 为同题发布的代理 RTL，以及从这些代理用规则生成的 G。沿用之前的代理取法，按 GPT-4o、GPT-4o-mini、Claude 3.5 Sonnet 三个发布来源各取前 3 份。沿用既有规则和排序，每份代理至多保留 24 个 G 候选。按正式数据源中的题号和有据可查的对应关系确定代理归属。API 凭据只从 `OPENCODE_GO_API_KEY` 读取，所有模型生成经 API 脚本。禁止手写设计 RTL、激励及检查器。反例转换和预算对齐使用确定性脚本。Golden RTL、golden TB 与 H 的执行和读取集中在 eval 端。

每个代理和 G 对用 Yosys 构造共享输入的 miter，SymbiYosys 依次在 20、40 周期做 BMC，时序题再到 80 周期。按 spec 或公开的通用 TB 惯例固定起始 N 拍复位，并记录 N、极性和依据。先尝试 Boolector，必要时换 Z3，一对的各深度和求解器共享 120 秒超时。报告每对最终状态及解析/elab 失败、不支持的语法、k 内等价、超时、转换失败、复位语义不匹配、其他的明细。有效反例和完成所要求深度的有界一致均计入形式化成功率。反例的转换、去重、复放及保留数量另行记录。

阶段 0 成功率至少 70% 才开始主比较。对有输入且低于门槛的运行，最多修复并重测三轮，记录每轮变更和结果。缺少合规代理时记录输入阻塞，空分母的成功率记为未定义。阶段 0 未通过时不启动主比较或 Oracle-F。

## 主比较

| 配置 | 激励 |
| --- | --- |
| A0 | 用指定模型根据 spec 和授权代理一次生成原始激励，沿用 4,000 周期起始预算 |
| A0-long | 同一题和种子共用 A0。用固定种子生成随机后缀填满 20,000 周期 |
| F-tool | 同一份 A0。反例按代理、G、最浅成功深度和确定性 trace 哈希排序，转换成含复位的完整输入向量片段。按全序列去重并依序追加可容纳的完整片段，再用与 A0-long 同源的随机序列补齐至 20,000 周期 |
| Oracle-F | 仅在 eval 端对 golden 与每个 hard H 做同深度、同复位及超时规则下的 BMC，并按正式仿真口径复放反例。记录确认可暴露、有界无差异及求解未定的数量。同步报告确认可暴露下界及将未定项计入的有界上界 |

阶段 1 沿用正、负沿即时观察及 golden X 掩码，只评价激励。报告 hard H 的逐题、宏平均和 pooled 暴露率，G 杀伤率、G 到 H 的迁移差值、形式化成功率、反例实际贡献的额外周期数及耗时。宏平均先对同题 5 次取平均，再对十题等权。Pooled 用全部运行中暴露的 H 数除以相应 H 总数之和。迁移差以 G 杀伤率增量减 hard H 暴露率增量定义，两个增量都以 A0 为基线，并一并报告原值。

主要比较为 F-tool 相对 A0-long。以题为配对单位，采用双侧 Wilcoxon 符号秩检验，bootstrap 用 stimulus-v2 的固定种子 441720，在题对上进行 20,000 次重采样，取双侧 95% 百分位区间。Oracle-F 单列。

## 固定停止规则

F-tool 相对 A0-long 的 hard H 宏平均暴露率提升至少 3 个百分点且 Wilcoxon p < 0.05 时判为有效。已完成的比较未满足任一条件时，方向一在本项目结束并停止追加变体。所有观察结果照实报告。阶段 0 输入阻塞或未达到门槛时，主比较的效果判定保持未测。

## Amendment 1

日期为 **2026-11-21**，按用户所在时区记录。CorrectBench 的公开代理仅覆盖 HDLBits，原协议将其误用于 CVDP。修订前，本 formal-cex 实验累计 **0 次模型调用、0 对形式化求解、0 次 H 评测**，未观察任何本实验结果。已发表的 stimulus-v2 结果仍仅作为历史对照。[原输入审查](reports/stage0_gate.csv) · [stimulus-v2 溯源](reports/V2_PROVENANCE.md)

本段更新 CVDP 数据输入规则。

- **(a) 若有现成的 stimulus-v2 CVDP proxy**，原样复用同一批文件，核验 SHA-256，并复用同批 G。溯源已确定十题均无独立代理，实际走 (b)。既有 v2 G 来自发布参考 RTL。
- **(b) 从 spec 生成代理**。每题固定 N=10 个代理槽位。每个槽位用 stimulus-v2 的 `deepseek-v4.1-flash` 与锁定参数经 API 生成。API 仅接收该题 spec 和通用输出要求。凭据只从 `OPENCODE_GO_API_KEY` 读取。每次收到 RTL 当即记录 UTF-8 SHA-256，100 个槽位及状态冻结并提交后再生成 G。失败槽位保留在报告中。G 使用原规则在每个代理上生成，原协议的每代理至多 24 个 G 上限继续适用。生成端仅做语法、端口和可运行性检查。以 golden/TB 测量的正确性不给生成端或筛选阶段。
- **评测端补充指标**。最终报告按题列出通过官方 golden TB 的代理数、可评分数、总槽位数、未定原因及两种分母下的通过率。该结果只在独立 eval 端计算。反例是否在对应 proxy/G 上复放与代理是否通过官方 TB 分别记录，便于解释反例迁移失败。
- **主比较**。A0、A0-long、F-tool、Oracle-F，指标、70% 阶段 0 门槛和正式停止规则保持原样。只有 F-tool 对 A0-long 提升至少 3 个百分点且 p < 0.05 才判为有效。
- **次要实验**。本仓库的 CVDP stimulus-v2 没有 HDLBits 题。将这里的 HDLBits 旧批次解释为 AutoBench v2 的六题正式二次试运行 `selection.json:selected`，依次为 `review2015_fsmseq`、`edgecapture`、`ece241_2014_q5a`、`2014_q3c`、`circuit10`、`count_clock`。固定用官方 CorrectBench `a2dcd36097b9416fd48dece8c2801401425dfcd1` 的代理，按原约定每模型取前三份。对这六题做相同的 A0-long 与 F-tool 对照，使用其 AutoBench v2 冻结评测组，独立报告，排除在主停止规则之外。此批次在主阶段 0 门槛核验之后执行。[AutoBench v2 固定选题](https://github.com/xuan2698/hdmi/blob/cfa9b5905b3961840f57b9c5dca04d06e8d36311/experiments/autobench-pilot/v2/reports/selection.json) · [CorrectBench 固定数据](https://github.com/AutoBench/CorrectBench/tree/a2dcd36097b9416fd48dece8c2801401425dfcd1/data/HDLBits)
