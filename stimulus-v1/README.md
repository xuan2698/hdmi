# Stimulus v1 冻结协议

本文件、`protocol.json` 和 `split.json` 在首次生成调用前提交，供实验结束后审计。结果另存于 `reports/`。

## 对象与隔离

以发布的 golden RTL 为参考。评测仅以相同输入下输出是否不同为准，不生成检查器，不依据输出驱动输入。Icarus 在主时钟正负沿即时比较，golden 的 X 位屏蔽，golden 已知位与变异体 X 仍计差异。初稿、后缀和 G 从发布 spec、golden、公开算子与输入本身产生。生成阶段只使用 G。H 在生成完成后由独立脚本加载，包含正式复核后的原 H 与难触发组，后者保留 85 个确认项和 10 个未定项。

开发集固定为已分析的 10 题。其余 15 个候选只记录标识，作为最终测试集。本次不运行其 RTL、不打开其 H。[题目划分](split.json)

## 固定参数

| 开发题 | spec 允许覆盖的 DUT 参数 | 本次固定实例值 |
|---|---|---|
| ring_token_0004 | 无 | 默认 |
| asyc_reset_0004 | 无 | 默认 |
| digital_stopwatch_0017 | CLK_FREQ，整数且大于 1 Hz | 4 Hz |
| manchester_enc_0009 | N | 8 |
| signed_adder_0003 | DATA_WIDTH | 8 |
| IIR_filter_0012 | WIDTH，spec 的实例显式设置 | 16 |
| hill_cipher_0012 | 无 | 默认 |
| simple_spi_0003 | 无 | 默认 |
| byte_enable_ram_0004 | XLEN、LINES | 32、8192 |
| word_change_detector_0012 | DATA_WIDTH | 8 |

只有秒表实际偏离发布 RTL 的默认值。选择 4 Hz 是为了让至少一次完整小时路径能落在 20,000 周期内。每个仿真按相同参数实例化 golden、G 和 H。长随机也用这些参数和 20,000 周期，由原协议的三个种子驱动。

## 冻结的生成与引导规则

每题种子为 20261120–20261124，四种配置共用一份 4,000 周期初稿。A0 停在初稿。B、O、O+F 最多进行四轮追加，每次 4,000 周期，总长度不超过 20,000 周期。既有激励不改写。G 全部暴露后停止。一次生成阶段最多允许两次纯格式或执行修复，修复保留当轮反馈；调用单独记录。追加阶段验证失败就保留最后有效激励并记录失败。模型固定为 `deepseek-v4.1-flash`，传输参数继承已锁定的 AutoBench v2 配置。初稿或后缀是沙箱中的 Python 输入生成函数，唯一可选调度字段是上升沿之后、下降沿之前的 `mid`。

G 固定为每题至多 24 个独立、可编译且能回放的候选。由源行和规则生成后去重，先按算子族轮转，再按种子哈希顺序挑选。保留只通过编译而暂时没有已知公开输出差异的 G，不使用 H 数据做难度筛选。四配置全程共用固定分母。

| 来源 | 实现的算子族 |
|---|---|
| AutoBench 原规则 | 算术、关系与逻辑替换，常量 ±1 与比较阈值 ±1，一元运算变化，条件取反、删除或拼接输入条件，算术或位运算插入，自保持或同宽值替换，位位置偏移，FSM 转移目标替换，主时钟与事件边沿翻转，异步复位项删除、复位或使能条件退化 |
| VeriBugBench 公开分类的适用子集 | PointerUpdate / Insert / Delete，PartselectUpdate / Insert / Delete，ExprInsert / Delete / Update，NSubUpdate / Delete / Insert / Insert_Case / Insert_IF，AssignB2N / N2B，IOFlip1 / IOFlip2，EdgeFlip / Insert / Delete |
| VeriBugBench 未采用部分 | NSubMove 需要可靠的跨语句和跨分支移动分析。该结构变换不纳入本次规则子集。 |

公开分类用于约束局部规则实现。下标规则限可静态表达的目标，I/O 翻转变更连接的值而保持接口，插入赋值仅在能够保持语法的模板中生成。完整清单及原论文来源为 VeriBugBench §IV 和作者发布的算子配置。[论文](https://arxiv.org/html/2609.18022v2#S4) · [公开配置](https://github.com/wndif/VeriBugBench/blob/463d490e261dff247eb6ef82b07b6e924fee19e8/configs/mutation_patterns.yaml)

每轮反馈只包含当轮仍未暴露的 G。B 给出原行和变异行。O 另给到达、感染、传播的可验证诊断。无法验证语义或局部状态时标为诊断不可用，识别的重赋值与复位原因分别记录。O+F 对每个仍未暴露的 G 查询同一 G 的有界模型检验结果，固定 36 个主时钟周期、每个求解 10 秒。相同 G 跨种子和轮次共享缓存。反馈只使用经原始 Icarus 复放验证的反例，并给出触发长度、关键输入及可读的参考状态。不确定和超时照实记录。形式化从不重跑 H。

## 固定统计

逐题先平均五次，再对十题等权。按题配对报告双侧 Wilcoxon 以及用种子 441720 重采样 20,000 次的配对 bootstrap 95% 百分位区间。全零差的 p 值约定为 1。每个 H 的 Pearson 和 Spearman 使用逐次运行的 G、H 暴露率提升，控制同一初稿。A0 的提升为零，变异为零时相关性不定义。长随机和 A0 的未暴露数按各自激励并集统计。
