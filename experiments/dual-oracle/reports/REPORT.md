# Dual-oracle 试运行与停止决定

三轮修复后，全量启动门槛未通过。35 个计划配置中，22 个可评分，6 个已确认生成失败，7 个在门槛处封存。确定失败率下界为 **17.14%**，门槛为 10%，最多允许 3 个失败。Vote-think 留存了 3 个 A 组首候选 RM，N 未完成标定。全量运行未启动。[预注册](../PREREG.md) · [机器可读门槛](pilot_gate.json) · [试运行完整表格](PILOT.md)

## 门槛复核

| 项目 | 结果 |
| --- | --- |
| CVDP golden 自回放 | 50／50 份冻结 A0 通过，400,000 个正负沿采样，8,758,910 个已知位零失配 |
| 环形令牌题 | 独立 TB 通过校验。初始 RM 与 Base-think 均耗尽三次逻辑尝试，合计 14 次传输，10 次达到 16,384-token 上限且没有最终正文，4 次连接断开 |
| 6 个确定失败的归属 | 同一道环形令牌题中，初始 RM 缺失使 Ours 和四个消融组失败，Base-think 独立失败 |
| 7 个封存槽位 | 五个 Vote-think 槽位，以及 signed_adder 的 Ours 和 Ours-noArbiter 的未完成修正 |
| 推理设置 | DeepSeek V4.1 Flash，原生思考开启。沿用温度、token 上限和传输重试策略 |

三轮分别处理了场景标签别名、缺失的 CVDP 行为说明，以及长提示与沙箱类型检查兼容。恢复的模型和定向期望来自原始 API 响应。日志包含所有已收到的失败收据。[golden 自回放明细](cvdp_self_replay.json) · [三轮修复](REPAIRS.md) · [全部计划槽位](pilot_by_run.csv)

## 已完成评分

- **A 组。** edgecapture、fsm3s 和 dff8r 的 Base-think 与 Ours 均通过 golden。两组逐题 H 检出依次为 10／10、10／10 和 8／9。追加定向激励后这三个计数相同。
- **B 组。** signed_adder 有四个可执行配置，均在固定 A0 上误报，golden 条件检错均为 0／10。完整 Ours 停在第二轮修正。环形令牌题的 9 个已确认 hard H 仍计入已失败配置的计划分母。

五题结果用于核查流程。全量假设检验和十个全量案例不具备开展条件。试运行配对、逐轮样例、逐变异体观察及评测记录分别归档。[逐题结果](pilot_by_task.csv) · [试运行配对](pilot_paired.csv) · [逐变异体结果](pilot_by_mutant.csv) · [六类流程样例](pilot_examples.json)

## 共模错误与裁决

- **共模错误。** signed_adder 初始 RM 与独立 TB 在 60 个有效定向采样中有 12 个共同出错。场景 s2 的第 8 个采样（第 4 拍负沿）两者都给出 `o_resultant_sum=15`、`o_ready=1`，golden 对这两项均为 0。这次一致错误不会进入分歧裁决。[共模错误与输入历史](pilot_common_mode_examples.json)
- **裁决错误。** signed_adder 场景 s5 的第 7 个采样（第 4 拍正沿），对 `o_status`，RM 给 0、TB 给 2、golden 为二进制 `10`。第一轮裁决将错误归给 TB，第二轮对同一点判 RM 错。第二轮 RM 修正在停止时尚未完成。[裁决错误](pilot_arbiter_error_examples.json) · [全部裁决原始 CSV](pilot_judgments.csv)
- **归档完整性。** 离线核对发现，旧解析器有时将场景 ID 覆写成端口名，可能误路由 TB 定点修正。已修复解析器，并在五份归档 TB 上验证了原始场景 ID。历史裁决按输入前缀和原 TB 值追溯，无法唯一定位的点单列。发生碰撞路径上的 TB 定点修正不计成功率。这项离线修复未开启第四轮，也未触发新调用。[试运行评分与诊断](PILOT.md)

已收到的收据合计 51 次逻辑调用、88 次传输、941,333 token，Go 用量 USD 0.634986，额外扣费为 USD 0。中止时部分连接的用量尚未返回。[用量与诊断表](PILOT.md)
