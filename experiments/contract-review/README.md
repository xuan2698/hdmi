# Contract-review 复现

在本分支根目录运行以下命令。Python 需要 NumPy、SciPy 和 v3 自带的 Python 沙箱依赖。评测另需 Icarus Verilog 和 bubblewrap。运行前在宿主环境设置 `OPENCODE_GO_API_KEY`。所有模型参数直接使用 v3 配置。

```sh
python3 experiments/contract-review/examples.py
python3 experiments/contract-review/base_think.py edgecapture 1
python3 experiments/contract-review/workflow.py pilot
python3 experiments/contract-review/eval/score.py pilot
python3 experiments/contract-review/eval/report.py pilot
python3 experiments/contract-review/eval/render.py pilot
```

在 `reports/pilot_gate.json` 验证试运行通过后，按相同顺序运行 `workflow.py full`、`eval/score.py full`、`eval/report.py full` 和 `eval/render.py full`。只有 `eval/score.py` 回放官方参考设计及缺陷版本。检查器在独立沙箱中执行。继续运行时从 `runs/` 中已校验的单步产物恢复。并发运行多个写入相同题、种子和阶段的进程会影响断点归档。

试运行门槛核对完整的 33 个配置槽位、每组至少一份可执行的产物、三份 Base 的 v3 复现、关闭及开启思考各至少两份完成两轮审查的 Ours 产物，以及实际执行的区分序列。执行失败保留在矩阵中；门槛不依赖误报率或检错率。

- [预注册](PREREG.md)
- [原生思考开关核验](reports/thinking_preflight.json)
- [公开 spec 例子](examples.json)
- [冻结的三题试运行和用量快照](https://github.com/xuan2698/hdmi/tree/4f20aa33240b59bf7e6dad7e9c1df9db6d4b508c/experiments/contract-review/reports)
- [全量结果](reports/REPORT.md)
