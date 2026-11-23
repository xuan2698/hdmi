# Dual-oracle 复现

在仓库根目录使用 Python 3、NumPy、SciPy、PyArrow、Icarus Verilog 和 bubblewrap。CVDP-ECov Parquet 文件使用 [CVDP 初始试运行归档的版本](../../cvdp-headroom/README.md)。模型凭据从进程环境读取。

```sh
python3 experiments/dual-oracle/data.py "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/eval/cvdp.py "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/generate.py pilot
python3 experiments/dual-oracle/eval/score.py pilot "$CVDP_ECOV_PARQUET"
python3 experiments/dual-oracle/eval/report.py pilot
```

试运行结束后检查 `reports/pilot_gate.json`。通过门槛再把 N 写入 `PREREG.md` Amendment 和 `amendment.json` 并提交。然后依次运行上述三份生成和评测脚本的 `full` 模式。每个 API 产物单独保存原始收据、原始响应和校验状态，执行断开后可从这些断点恢复。A 组已归档的 Base-think 检查器从预注册指定的 commit 逐文件读取。

- [预注册](PREREG.md)
- [CVDP 自回放](reports/cvdp_self_replay.json)
- [试运行修复日志](reports/REPAIRS.md)
