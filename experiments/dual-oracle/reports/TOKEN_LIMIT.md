# OpenCode Go 输出预算核对

| 问题 | 查证结果 |
| --- | --- |
| 使用的网关 | OpenCode Go 官方文档将 `deepseek-v4.1-flash` 列为 OpenAI 兼容 Chat Completions 模型。实验保持该路由。 |
| `max_tokens` 是否包含思考 | 包含。DeepSeek 把生成的 `reasoning_tokens` 列在 completion 用量细项中。原试运行中该 Go 路由有 10 条 `length` 回执，每条 `completion_tokens=16384`、最终正文为空。 |
| 最大值 | OpenCode Go 的 Models.dev 模型目录标注输出上限 384,000；DeepSeek 原生接口文档最大值为 393,216。目录数值是公开的 Go 上限，和上游原生接口分开记录。本次请求设为目录上限以内的 32,768。 |
| 单独思考预算 | 公开 Chat Completions 参数提供 `thinking.type` 和 `reasoning_effort`（low/high/max）。后者为档位，公开文档没有列出单独按 token 数设置思考预算的参数。此次不发送额外档位或思考预算字段。 |

[OpenCode Go 官方路由](https://opencode.ai/docs/console/go/) · [OpenCode Go 模型目录](https://models.opencode.ai/providers/opencode-go/) · [DeepSeek Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/) · [DeepSeek Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/) · [旧试运行报告](REPORT.md)
