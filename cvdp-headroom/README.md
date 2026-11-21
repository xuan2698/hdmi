# CVDP-ECov 时序激励余量预检

修复了第三版重试的提示词拼装。检查器和激励两条路径的回归测试均证实，验证失败后的重试同时保留当轮诊断、上一份源码和验证错误。

## 数据来源核对

检查了 LLM4Cov 论文链接的作者仓库 `main`、`slime_rl`、`gh-pages` 及其公开历史和发布附件。可找到的覆盖组只有 `tests/resources/tb_counter.sv` 的工具测试样例。CVDP-ECov 正式加载器读取题目说明、RTL 和数值目标，公开评测分支没有附带逐题功能覆盖 bin 或模型。README 说明 Xcelium/IMC 的服务器端工具调用和解析实现未随仓库公开。服务协议中的示例也允许 `Functional Average` 为空。[作者仓库](https://github.com/HejiaZ2023/llm4cov_oss/tree/1566cb00dd4901671160a393b8a53283fb185fac) · [工具测试覆盖组](https://github.com/HejiaZ2023/llm4cov_oss/blob/1566cb00dd4901671160a393b8a53283fb185fac/tests/resources/tb_counter.sv) · [EDA 协议](https://github.com/HejiaZ2023/llm4cov_oss/blob/1566cb00dd4901671160a393b8a53283fb185fac/src/llm4cov/eda_client/protocol.md)

直接扫描数据文件得到 83 道题，67 道的 RTL 包含边沿触发块，可作为时序候选清单。83 道都按题号匹配到原版 CVDP 的 v1.0.2 commercial harness。每道都有 IMC 报告命令，两个数据源均未找到每题的 coverage group、coverpoint 或 cover property/sequence 源码。数据目标中的 `Overall Average` 是阈值或汇总指标，不能当成长随机功能覆盖实测值。本环境的开源仿真器可用，Xcelium 和 IMC 未安装。[发布数据](https://huggingface.co/datasets/hez2024/CVDP-ECov-eval/tree/26a8b0012436b460c539ebe5f893fba6e1d601a4) · [原版 CVDP 数据](https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset/tree/5b807d945f6a99aa645f7e43a64a2115e281b4bf) · [逐题审计](reports/dataset_inventory.csv) · [数据集审计汇总](reports/dataset_audit.json)

## 运行状态

- DeepSeek V4.1 Flash 最小请求成功，返回的模型 ID 为 `deepseek-v4.1-flash`。正式版 `hy4` 返回 HTTP 403，错误类型为 `permission_error`，服务端说明 `Model access is disabled.`。[调用预检](reports/model_preflight.json) · [OpenCode Go 模型文档](https://opencode.ai/docs/console/go/)
- 用公开的 SPI 时序题验证评测接线。3 个种子各跑 2,000 周期并在正负沿即时取样，每次取到 4,000 个样本。两个相同 RTL 实例零误报，注入已知输出差异后均能检出。Verilator 合并覆盖 10/11 个 DUT 行插桩点。结果仅用于验证工具链。[技术验证结果](reports/spi_smoke.json)
- 正式样本目前为 0/10，工具预检的数据不计入 A0 或长随机组。缺少既有功能覆盖模型和测量入口，无法按 <95% 排序抽题，也无法报告功能覆盖率。Hy4 未授权使 H 的生成与预筛无法执行，因此没有正式暴露率、覆盖率或诊断分布，90% 的判定条件尚无实测值可用。

## 可复查的抽样规则

配置固定在 [protocol.json](protocol.json)。在候选时序题上使用种子 101、203、307，各运行 2,000 周期。选题用三个种子的功能覆盖率算术平均，优先抽取低于 95% 的题。同一档先按题号排序，再用 `20261121` 抽取。保留每种子的实测值和覆盖模型标识。后续 A0 每题五次，H 每题十个 Hy4 变异体。H 的生成、筛选和评测数据与 A0 请求分开。

```bash
python3 -m pip install pyarrow
python3 cvdp-headroom/audit_sources.py dataset.parquet \
  --original cvdp_v1.0.2_agentic_code_generation_commercial.jsonl cvdp_v1.0.2_nonagentic_code_generation_commercial.jsonl
python3 cvdp-headroom/smoke_spi.py dataset.parquet
```

已有覆盖模型的测量导出可通过 `--coverage-runs` 传给审计脚本。CSV 字段为 `task_id,coverage_model,seed,cycles,functional_percent`，百分数范围为 0 到 100。只有三种子测量完整的题参与抽样。继续正式试运行需要可执行的功能覆盖模型或对应的已有测量，以及 OpenCode Go 对 `hy4` 的访问权限。
