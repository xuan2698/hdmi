# 第三版试运行

本实验使用第二版标定后冻结的 17 题。每个题目使用五个种子。每个题目和种子各生成一份初始激励与检查逻辑，五种配置共用命名一致的初稿，然后分别运行各自的修订流程。每次运行和全部中间产物均保留在对应的任务、配置和重复目录。

推理调用沿用第二版的 DeepSeek、流式传输、关闭思考、温度、token 上限、超时和重试策略。所有配置执行同一检查完整性要求。每个检查周期的每个输出须有位宽内的整数期望值。生成不合格时最多重新生成两次，调用及失败原因保存在源代码旁。模型生成失败在主检出分母中占一个计划机会并计零，误报率按实际执行 golden 的 TB 计算。

H 预筛在评测侧比较三种种子下每次的 2,000 个周期，包含主边沿前、主边沿后和相反边沿后的采样。四态完全一致标记为疑似等价。仅在 golden 的 X/Z 位不同标记为按评分规则等价。最终评测使用主边沿采样，只比较 golden 已知位。通过 golden 的最终 TB 才有 H 检出。漏检分为 golden 失败、未暴露、已暴露但未报错、生成失败和模拟错误。所有 H 信息和代理 golden TB 正确性仅供评测。

激励仍只追加。每行允许附加 mid 输入字典，在主边沿采样后、相反边沿前驱动这些输入。O 激励侧对未感染位置尽量给出可自动推导的感染条件和采样到的操作数范围。比较器阈值和等位宽偏移使用规则。简单运算符使用位宽受限的充分条件示例。不可推导的表达式保留标记。O 同时检查主评分边沿以外的采样差异。源码探针在复杂分支的到达判定可能近似，G 是否暴露由实际输出重放判定。感染条件发送后暴露的统计描述时序关联。每次修订仍可能同时包含多个变异点的反馈。

B 检查侧继续使用三份 GPT-4o 代理。O 检查侧每题使用归档中 GPT-4o、GPT-4o-mini 和 Claude 3.5 Sonnet 各前三份代理，以信号和公共 spec 条款作为问题点键，在一次运行中至多发一次。只有至少六份给出同一已知值时才向模型提供代理数值。其余问题点仅发信号和 spec 条款。编译失败或输出未知的代理不投票，阈值保持六份。G 使用首个可运行的归档代理作为变异锚点，优先用 GPT-4o 的第一份。gshare 的第一份无法编译，该题使用第二份作为 G 锚点，O 投票仍保留原九个代理位置。

配对检验以题为单位。先在每题内汇总五次重复，再计算跨题宏平均。Wilcoxon 使用双侧精确符号翻转分布，零差配对不计秩，并保留并列秩。区间对同题的配置差值作 20,000 次配对 bootstrap。四个 p 值均为未校正值。长度相关性把 golden 失败编码为 1，按 TB 计算 Pearson 和 Spearman。

逐次结果的 shared 字段是本次配置所引用初稿的费用和用量。全量账单对每份共用初稿只累计一次，另加各配置的增量调用。

## 结果

- [425 次逐次结果](reports/trials.csv) · [17 题逐题汇总](reports/per_task.csv) · [配置宏平均](reports/macro.csv)
- [配对检验和置信区间](reports/paired_comparisons.csv) · [逐题配对差](reports/paired_task_deltas.csv)
- [逐 TB 散点数据](reports/length_scatter.csv) · [长度相关系数](reports/length_correlations.csv) · [散点图](reports/length_scatter.png)
- [H 预筛](reports/h_prescreen.csv) · [九代理正确数](reports/proxy_correctness.csv)
- [逐例感染条件](reports/infection_feedback.csv) · [检查侧问题点](reports/checker_issue_counts.csv) · [反馈实例](reports/feedback_examples.json) · [用量与费用](reports/summary.json)

## 复跑

工具安装、源仓库固定与密钥设置参见上一级 README。分析需要 NumPy、SciPy。Matplotlib 用于绘图，数值报告可独立生成。

```bash
python3 pilot3_inputs.py
python3 pilot3_evaluation.py
python3 pilot3_guidance.py
python3 pilot3_generate.py
python3 pilot3_run.py
python3 pilot3_report.py
```
