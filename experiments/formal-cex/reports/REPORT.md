# Formal-cex 阶段 0 报告

**状态为输入阻塞。** 基于 `pilot` 提交 `cfa9b5905b3961840f57b9c5dca04d06e8d36311` 创建 `pilot-formal-cex`，先提交预注册，再核验输入和工具。冻结的 10 道 CVDP 开发题中，公开的 CorrectBench 代理目录匹配 **0 道**。实际可构造的 `(proxy, G)` 对为 **0**，形式化成功率未定义，70% 门槛无法评估。阶段 1 和 Oracle-F 均未启动，方向一的效果判定保持未测。[预注册](../PREREG.md) · [阶段 0 门槛记录](stage0_gate.csv)

## 数据来源与逐题结果

CorrectBench 的论文和仓库说明均将实验数据限定为 156 道 HDLBits 题。核验时，官方远端只有 `master`，头提交与先前锁定的 `a2dcd36097b9416fd48dece8c2801401425dfcd1` 一致。它发布了 GPT-4o、GPT-4o-mini 和 Claude 3.5 Sonnet 三个代理文件，每份都是 156 个题号、每题 20 个条目。三份文件和 CVDP 的 10 个开发题号均无交集。剥掉 `cvdp_copilot_` 或 `cvdp_agentic_` 前缀后仍无匹配。官方补充材料目录列出六个 2024 年 9 月归档，为论文实验结果。目录中未发现额外的 CVDP 代理发布，未解包补充归档。[CorrectBench 数据与代理目录](https://github.com/AutoBench/CorrectBench/tree/a2dcd36097b9416fd48dece8c2801401425dfcd1/data/HDLBits) · [论文 IV-A](https://arxiv.org/html/2411.08510#S4.SS1) · [补充材料目录](https://drive.google.com/drive/folders/1ldVzdAKC4HQb10ez0aUasNevWnTP5RRc?usp=sharing) · [代理清单与 SHA-256](correctbench_inventory.csv)

| CVDP 开发题 | 匹配代理 | 尝试的 (p, G) 对 | Formal-cex hard H / Oracle-F | stimulus-v2 A0-long hard H |
| --- | ---: | ---: | --- | ---: |
| ring_token_0004 | 0 | 0 | 未运行 | 66.67% |
| asyc_reset_0004 | 0 | 0 | 未运行 | 100.00% |
| digital_stopwatch_0017 | 0 | 0 | 未运行 | 47.14% |
| manchester_enc_0009 | 0 | 0 | 未运行 | 90.00% |
| signed_adder_0003 | 0 | 0 | 未运行 | 81.00% |
| IIR_filter_0012 | 0 | 0 | 未运行 | 83.00% |
| hill_cipher_0012 | 0 | 0 | 未运行 | 90.00% |
| simple_spi_0003 | 0 | 0 | 未运行 | 65.00% |
| byte_enable_ram_0004 | 0 | 0 | 未运行 | 83.00% |
| word_change_detector_0012 | 0 | 0 | 未运行 | 90.00% |

[逐题输入核验](stage0_tasks.csv) · [逐题逐配置历史对照](stimulus_v2_reference.csv)

## 阶段 0 分类与工具检查

| 项目 | 数量 | 说明 |
| --- | ---: | --- |
| 缺少同题的公开代理 | 10 题 | 输入阻塞 |
| 解析/elab 失败 | 0 对 | 没有可尝试的对 |
| 不支持的语法 | 0 对 | 没有可尝试的对 |
| k 内等价 | 0 对 | 没有可尝试的对 |
| 超时 | 0 对 | 没有可尝试的对 |
| 转换失败 | 0 对 | 没有可尝试的对 |
| 复位语义不匹配 | 0 对 | 没有可尝试的对 |
| 其他 | 0 对 | 没有可尝试的对 |
| 正式求解、修复轮次、模型调用 | 各 0 | 缺少代理归档发生在任何 BMC 运行之前 |

Yosys 0.52、SymbiYosys 0.52、Boolector 3.2.4、Z3 4.13.3 和 Icarus 12.0 均可执行。Yosys 已确认支持 `miter -equiv`。这些是工具入口检查，开发题的 miter、复位约束和 trace 转换还没有实例可验证。语法预处理、复位约束和时钟建模无法补齐输入数据，因此没有虚构三轮求解修复。未加载 golden、H 或封存题的设计内容，未调用模型。[工具版本](toolchain.csv) · [失败类别 CSV](stage0_categories.csv) · [逐对原始 CSV](stage0_pairs.csv)

## 阶段 1 与历史对照

Formal-cex 的 hard H 宏平均及 pooled、G 杀伤率、G→H 迁移差、反例额外周期数、求解耗时、Oracle-F 有界上限、Wilcoxon p 值和 bootstrap 区间均未测。下表只使用上一版已提交的聚合回执。每配置 100 次，hard H 共 950 个运行与变异体组合。原 stimulus-v2 的初稿生成输入含发布 RTL。本次预注册要求用合规的代理输入重新生成初稿。[stimulus-v2 逐运行结果](../../../stimulus-v2/reports/by_run.csv) · [历史对照 CSV](stimulus_v2_reference.csv)

| stimulus-v2 配置 | hard H macro | hard H pooled |
| --- | ---: | ---: |
| A0 | 73.40% | 74.53% |
| A0-long | 79.58% | 80.63% |
| B | 81.16% | 82.42% |
| O | 81.33% | 82.53% |
| O+F | 82.43% | 83.68% |

恢复阶段 0 需要十道开发题的 CorrectBench 代理 RTL 和可核验的来源或题号映射。如果已有独立发布或私有归档，提供该归档即可核对。采用其他代理来源需要先修订数据协议。

## 复查

从 HDMI 仓库根目录运行，参数为已克隆的官方 CorrectBench 仓库。脚本始终读取锁定的 CorrectBench Git 对象，从开发集只取题号并输出 CSV。

```sh
python3 experiments/formal-cex/preflight.py /path/to/CorrectBench
```
