# 等价性复核与 CVDP 难触发变异体

使用原来的 golden RTL 和原来的 A0、长随机激励。没有新增激励生成调用。新 H 的生成调用只发送发布 RTL 与变异要求，模型为 `gpt-6-luna`。

## 工具与比较边界

- Yosys 0.52、SymbiYosys v0.52、Berkeley ABC 1.01、Z3 4.13.3、Boolector 3.2.4。证据复放用 Icarus Verilog 12.0。等价小例特意让变异体只在 golden 为 X 时不同，结果通过 52 周期。不等价小例在第一个主时钟周期给出反例，Icarus 复现了若干已知位中的差异。[工具版本](reports/tool_versions.json) · [小例证明及反例](reports/smoke_cases/smoke/)
- 形式化 miter 为两个实例共享输入。每个完整时钟周期拆成四个阶段，输入可在两个边沿之间变化，边沿时保持稳定。有显式复位的设计从一次共同有效复位开始，此后复位可任意变化。时钟和异步控制用 Yosys `clk2fflogic` 建模。用 `xprop` 分离值与未知位掩码，逐位比较全部输出。golden 未知位跳过，golden 已知而变异体未知仍算差异。形式化结果适用于这些时序与复位假设。
- 常规 BMC 目标为 **52 个完整主时钟周期**，初始状态一起比较。覆盖了 async reset 计数器从 31 到 0 的完整倒计时，以及 SPI 的完整 16 位传输。对证明失败的候选，从 ABC 见证重建 SMT 波形，并在原始 Icarus RTL 上复放。只用受约束模型搜索反例时，搜索通过不会作为等价证明。
- 秒表保持默认 50 MHz。分频器一圈 50,000,000 周期，一小时路径约 180,000,000,000 周期。有限深度扫描覆盖不到这些状态。对共有分频器的候选，用原样输出逻辑在 1 Hz 事件上复放可达前缀，再用 Yosys SAT 证明首次分歧的转移。对分频器改动，用 SAT 检查原始状态转移或可达不变量，并以游程压缩记录默认频率下的反例输入。完全等价的秒表项由可达不变量推出。没有证明、也没有有效反例的长深度项归为未定。
- 全尺寸 CVDP RAM 的 X 状态展开成本高，先在两个或八个地址上找反例，再把地址零扩展，在发布的 8,192 地址 RTL 上复放。该缩减不能给出全尺寸等价证明。Word Change 的多驱动 RTL 用规范化副本找反例，只有原始 RTL 复放通过的反例才纳入。AutoBench 的少数不完整 `always_comb` 用 Yosys 可综合的锁存语义建模，反例仍以原始 RTL 复放核对。

## 重算口径

旧批次以题目和原始 RTL 对的哈希去重。AutoBench v3 与 CVDP 只把形式化确认不等价的旧候选加回原 H，并沿用各自原有的观察时刻。AutoBench v3 A0 用归档最终激励及原评分域，CVDP 仍在时钟正负沿即时比较。CVDP A0 正式 50 份样本中的 4 次已有生成失败继续记为零。

新 H 每题 10 个，共 100 个。编译失败和形式化认定等价的候选剔除。对形式化未定但能仿真的候选，主暴露表保留它们并单列来源，另给只含确认不等价候选的结果。仿真结果没有参与等价筛选。CVDP 的长随机仍用原来三个独立的 2,000 周期种子。暴露率是逐题计算后等权宏平均。

[旧批次逐例分类](reports/old_formal.csv) · [旧反例周期分布](reports/old_counterexample_distribution.csv) · [AutoBench v3 重算](reports/autobench_v3_addback.csv) · [CVDP 逐题对比](reports/cvdp_exposure_comparison.csv) · [新批次逐例分类](reports/new_formal.csv) · [未暴露与预计触发条件](reports/cvdp_rare_unexposed.csv) · [汇总](reports/summary.json)

## 结果

| 来源 | 提交复核数 | 52 周期有界等价 | 完全等价 | 确认不等价 | 未定 |
|---|---:|---:|---:|---:|---:|
| AutoBench 第二轮 | 36 | 27 | 0 | 2 | 7 |
| AutoBench 第三轮 | 26 | 20 | 0 | 2 | 4 |
| CVDP 原 H | 15 | 0 | 0 | 15 | 0 |
| 去重合计 | 51 | 27 | 0 | 17 | 7 |

第三轮 26 个与第二轮重叠。旧批次反例有 8 个在 3–32 周期，9 个在 50,000,001–180,050,000,001 周期。较长的九个均为秒表，保留了游程压缩的默认时钟输入序列和对应的 SAT 转移证据。

| 评测组 | A0 宏平均暴露率 | 长随机宏平均暴露率 |
|---|---:|---:|
| AutoBench v3 原 H | 90.24% | — |
| AutoBench v3 加回 2 个不等价项 | 88.48% | — |
| CVDP 原 H | 92.00% | 99.26% |
| CVDP 加回 15 个不等价项 | 83.80% | 85.00% |
| CVDP 新 H 含 10 个未定项 | 80.32% | 72.65% |
| CVDP 新 H 只计 85 个确认不等价项 | 82.31% | 75.64% |

新 H 的 100 个候选有 2 个编译失败，3 个完全等价，85 个确认不等价，10 个未定。可仿真的 95 个进入主暴露表。仅按 46 个已有有效 A0 样本计算，新 H 宏平均是 86.16%。两组激励都未暴露的 7 个候选中，5 个已确认不等价。例子包括秒表 R07 的 58 秒提前回绕，R01/R02/R10 的 59:59 终态，以及 R04 的分频器到达终点后先暂停一拍再恢复。剩余两个的触发条件来自模型描述，形式化尚未确认。A0 在新 H 上优于长随机，但加入深时序反例后，原先“没有明显提升空间”的判断不再成立。

## 复跑

从仓库根目录执行。保留 `equiv-audit/.work/` 到重试阶段结束。原激励的向量文件缺失时，从已有 Python 激励代码和种子在本地重建。生成新变异体的命令读取归档响应，有缺失时才调用模型。

```bash
bash equiv-audit/setup.sh equiv-audit/.work/tools
source equiv-audit/.work/tools/env.sh
# 在 PATH 中加入已有 iverilog 和 vvp。使用 CVDP 已冻结的数据集版本。
python3 equiv-audit/rare_mutants.py dataset.parquet
python3 equiv-audit/formal.py smoke
python3 equiv-audit/formal.py old dataset.parquet
python3 equiv-audit/formal.py new dataset.parquet
python3 equiv-audit/supplement.py old dataset.parquet
python3 equiv-audit/supplement.py new dataset.parquet
python3 equiv-audit/stopwatch.py dataset.parquet --cohort old
python3 equiv-audit/stopwatch.py dataset.parquet --cohort new
python3 equiv-audit/divider.py dataset.parquet
python3 equiv-audit/new_divider.py dataset.parquet
python3 equiv-audit/restricted_search.py dataset.parquet --cohort old
python3 equiv-audit/restricted_search.py dataset.parquet --cohort new
python3 equiv-audit/score.py dataset.parquet
```
