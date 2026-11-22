# 典型误报核对

以下三例使用全量 Ours 在冻结 A0 激励上的首次已知位失配。周期从 1 开始。

- **2014_q3c，种子序号 2，周期 27。** spec 表中 `y=010, x=1` 的下一状态是 `001`，所以 `Y0=1`。周期 26 的 `mid` 将 `x` 改为 0，周期 27 的主输入再将 `x` 驱动为 1。检查器在读取周期 27 前用上周期的 `pending["x"]` 覆盖了新行的值，实际查询 `x=0` 的列并输出 0。该检查器通过了检查 A，检查 B 在多个相符的候选中选择了编写者版本。spec 的单拍真值表例子没有覆盖这段输入覆盖顺序。[最终检查器](../runs/2014_q3c/rep2/off/final_models/89753f071ad005ad2b0a/model.py) · [检查 A](../runs/2014_q3c/rep2/configs/Ours/A_check.json) · [检查 B](../runs/2014_q3c/rep2/configs/Ours/B_resolution.json)
- **circuit10，种子序号 1，周期 3。** 检查器先用当前本地 `state` 计算并输出 `q,state`，随后才执行契约 R1 的状态更新。这一拍两者都预测为 0，golden 主边沿稳定后两者均为 1。预测值与后一拍的两个已知输出相同，支持可见时刻有偏差的诊断。这项对照覆盖该采样点。检查 A 的两次重生成后仍有例子失配，并按协议保留最后一份可执行模型。[最终检查器](../runs/circuit10/rep1/off/a_repairs/394605a2ff11a044c9e9/try2/model.py) · [契约](../runs/circuit10/rep1/configs/Ours/final_contract.json) · [检查 A](../runs/circuit10/rep1/configs/Ours/A_check.json)
- **circuit10，种子序号 2，周期 2。** 契约 R1 把状态更新写成 `a XOR b`，源代码直接实现了这个假设。spec 波形中 85 ns、90 ns 和 95 ns 的 `a,b` 都是 1，95 ns 的 `state` 为 1，与该假设给出的 0 冲突。冻结激励周期 2 的 `state` 预测为 1，golden 为 0。上一拍的 `state` 未知，下一拍仍为 0。这里有波形证据表明状态转移公式需要修正。检查 A 的两次重生成未消除全部契约例子失配。[最终检查器](../runs/circuit10/rep2/off/a_repairs/c57e741309b3ae282b85/try2/model.py) · [契约](../runs/circuit10/rep2/configs/Ours/final_contract.json) · [失配记录](false_positive_cases.json)
