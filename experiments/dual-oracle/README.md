# Dual-oracle 复现

在仓库根目录使用 Python 3、NumPy、SciPy、PyArrow、Icarus Verilog 和 bubblewrap。CVDP-ECov Parquet 文件使用 [CVDP 初始试运行归档的版本](../../cvdp-headroom/README.md)。模型凭据从进程环境读取。

```sh
python3 experiments/dual-oracle/data.py "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/eval/cvdp.py "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/generate.py pilot
python3 experiments/dual-oracle/eval/score.py pilot "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/eval/report.py pilot
```

32,768-token 试运行结束后检查 `reports/32768/pilot_gate.json`。通过门槛后运行 `generate.py calibrate`，把正式 N 写入 `PREREG.md` Amendment 和 `reports/32768/amendment.json` 并提交，再依次运行上述三个生成和评测脚本的 `full` 模式。每个 API 产物单独保存原始收据、原始响应和校验状态。执行断开后可从同一上限的断点恢复。

16,384-token 试运行已封存，原始结果留在 `runs/` 和 `reports/`。32,768-token 的结果使用独立目录。

- [预注册](PREREG.md)
- [CVDP 自回放](reports/cvdp_self_replay.json)
- [试运行修复日志](reports/REPAIRS.md)
- [16,384-token 停止决定与结果](reports/REPORT.md)
- [OpenCode Go 输出上限证据](reports/TOKEN_LIMIT.md)
