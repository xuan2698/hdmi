# CVDP-ECov 时序激励试运行

本次从用户提供的 25 道非饱和候选中抽样。按发布 RTL 中的边沿触发事件判断，25 道全部符合条件。将数据集中的实际 ID 排序后，使用种子 `20261121` 抽取 10 道。候选是否非饱和沿用用户此前复检结果，本次 **功能覆盖率待补**。[候选、边沿证据与选题](reports/selection.json) · [发布数据](https://huggingface.co/datasets/hez2024/CVDP-ECov-eval/tree/26a8b0012436b460c539ebe5f893fba6e1d601a4)

## 模型与隔离

Hy4 最小请求返回 HTTP 403 `permission_error`。从 OpenCode Go 模型目录查询到 GPT 6 Luna 的 ID 为 `gpt-6-luna`，最小请求返回 HTTP 200、相同模型 ID 和完成标志。H 组生成调用均使用 `gpt-6-luna`，A0 均使用 `deepseek-v4.1-flash`。[模型预检](reports/model_preflight.json) · [OpenCode Go 模型文档](https://opencode.ai/docs/console/go/)

H 每题生成 10 个候选。对字节级重复 RTL 和一条无法准确应用的引用，仅根据生成稿和参考 RTL 重新生成候选。编译和仿真结果不参与这些重新生成。H 原始响应、变异体源码和筛选结果保存在 `eval/`。A0 只读取发布 spec、参考 RTL、沿和端口配置，各次仅采用一份生成响应，不生成检查器或根据评测反馈迭代。

Manchester 的输入接口在首批提示词中将 `rst_in` 错标为低有效。核对 RTL 后，把这 5 份提示全部作废，在相同种子下重新一次性生成。它们未计入正式 50 次，单独记录了调用及提示哈希。正式样本中，截断和超出位宽的失败计为零暴露，代码覆盖率仅汇总有效运行。[协议更正与作废调用](reports/protocol_correction.json)

## 评测口径

- A0 每题 5 个种子，每次 2,000 周期。长随机基线按每个端口宽度均匀随机，复位在开头两拍有效，此后低概率触发，种子为 101、203、307，每个 2,000 周期。筛选 H 使用另三个固定种子 409、503、607，同样每个 2,000 周期。
- 用 Icarus 在正负沿即时比较，同一仿真内运行 golden 和变异体，使用 AutoBench 的 `ref === (ref ^ dut ^ ref)` 比较式。每个激励均先用同一 golden 验证零差异。所有 golden 输出均无 Z，该试验中的评分差异即 golden 已知位的差异。
- 编译失败单列。筛选的三个种子都未出现 golden 已知位差异时，有原始四态差异的标为按评分规则等价，其余标为疑似等价。
- H 暴露率先按运行得到每题 5 次的均值和样本标准差，再对 10 道题等权平均。长随机报告 3 次均值，另存并集。九题的代码覆盖率来自 Verilator 对 golden 的行和分支插桩。Word Change 的发布 RTL 混用阻塞和非阻塞赋值，Verilator 兼容运行与 Icarus 输出不一致。该题改用 Icarus 对赋值行和分支臂做执行计数，逐个验证所有 8 个激励下插桩前后的双边沿稳定输出一致。H 评分均使用未经插桩的原始 RTL，即时比较。

## 结果

H 的 100 个最终候选中，15 个疑似等价，编译失败和按评分规则等价均为 0 个，保留 85 个。A0 的 46 个有效运行都暴露了各自的全部 H。1 次输出截断和 3 次输入越界计为零，正式 50 次的 A0 宏平均为 **92.00%**。独立长随机基线的宏平均为 **99.26%**，三个种子的并集覆盖全部保留 H。按预设的 90% 门槛，本次样本和 2,000 周期预算下没有观察到明显的激励侧 H 暴露提升空间。时钟默认参数和有限筛选会限制保留的 H，例如 Digital Stopwatch 只保留了 1 个变异体。

[逐题指标](reports/headroom_by_task.csv) · [逐次指标](reports/headroom_by_run.csv) · [宏平均、筛选与用量](reports/headroom_summary.json) · [逐变异体筛选及复放](eval/results/)

## 复跑

安装 Icarus Verilog、Verilator、C++ 构建工具、`bwrap`、`pyarrow` 和 `pyslang` 后，从仓库根目录运行。已归档的生成源码、响应和验证状态允许不调用模型地复放。A0 输入向量可以由归档源码和种子重建。

```bash
python3 -m pip install pyarrow pyslang
curl -fLo dataset.parquet https://huggingface.co/datasets/hez2024/CVDP-ECov-eval/resolve/26a8b0012436b460c539ebe5f893fba6e1d601a4/data/eval-00000-of-00001.parquet
python3 cvdp-headroom/eval/run.py dataset.parquet
python3 cvdp-headroom/eval/report.py
```
