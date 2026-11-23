# OpenCode Go 输出预算核对

| 问题 | 查证结果 |
| --- | --- |
| 使用的网关 | OpenCode Go 官方文档将 `deepseek-v4.1-flash` 列为 OpenAI 兼容 Chat Completions 模型。实验保持该路由。 |
| `max_tokens` 是否包含思考 | 包含。DeepSeek 把生成的 `reasoning_tokens` 列在 completion 用量细项中。原试运行中该 Go 路由有 10 条 `length` 回执，每条 `completion_tokens=16384`、最终正文为空。 |
| 最大值 | OpenCode Go 的 Models.dev 模型目录标注输出上限 384,000。DeepSeek 原生接口文档最大值为 393,216。Go 实测对 384,000、393,216 和 393,217 的短答请求均返回 HTTP 200。请求字段的接受范围至少达到 393,217，公开目录仍以 384,000 为输出上限。短答探测没有测量网关是否内部裁切预算，也未确定网关实际生成上限。实验请求采用 32,768。 |
| 单独思考预算 | 公开 Chat Completions 参数提供 `thinking.type` 和 `reasoning_effort`（low/high/max）。后者为档位，公开文档没有列出单独按 token 数设置思考预算的参数。此次不发送额外档位或思考预算字段。 |

[OpenCode Go 官方路由](https://opencode.ai/docs/console/go/) · [OpenCode Go 模型目录](https://models.opencode.ai/providers/opencode-go/) · [DeepSeek Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/) · [DeepSeek Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/) · [旧试运行报告](REPORT.md) · [短答探测回执](gateway_token_probes/summary.json)
