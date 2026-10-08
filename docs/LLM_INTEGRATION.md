# LLM 接入（LLM INTEGRATION）

游戏内的「自由对话」通过 OpenAI 兼容的 `chat/completions` 接口实现。

## 1. 配置项（`user://settings.cfg`）

| 键 | 默认值 | 说明 |
|---|---|---|
| `llm/base_url` | `https://api.openai.com/v1/` | 兼容 OpenAI 的接口前缀（含 `/v1/`），可填任意兼容服务 |
| `llm/model` | `z-ai/glm-5.3` | 模型 id |
| `llm/api_key` | `""` | 玩家自填，明文存储 |
| `llm/temperature` | `0.8` | 采样温度 |
| `llm/max_tokens` | `512` | 单次生成上限 |
| `llm/timeout_sec` | `60.0` | 超时 |
| `game/llm_enabled` | `true` | 关闭后走纯剧本 |

> **玩家自填 Key**：引擎不内置任何密钥。玩家在首次向导或设置中填入自己的 Key，
> 支持任意 OpenAI 兼容服务（OpenAI / Claude 网关 / Gemini 网关 / DeepSeek /
> 智谱 / 硅基流动 / 本地 Ollama 等）。

## 2. 请求

```
POST {base_url}chat/completions
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "model": "{model}",
  "messages": [
    { "role": "system", "content": "{角色 system_prompt}" },
    ...历史...
    { "role": "user", "content": "{玩家输入}" }
  ],
  "temperature": 0.8,
  "max_tokens": 512,
  "stream": false
}
```

响应解析：`data["choices"][0]["message"]["content"]`，缺失视为失败。

## 3. 约束与行为

- **单请求串行**：`_busy` 为 true 时立即 `request_failed("busy")`，不排队。
- 历史长度上限 `HISTORY_LIMIT = 20`。
- 超时 / 非 200 / JSON 解析失败 → `request_failed`，错误信息**必须含 HTTP 状态码**。
- **绝不把 api_key 写进日志**（日志中用 `[已隐藏]`）。
- 失败时剧情节点用 `fallback` 台词兜底，保证纯剧本仍可玩。

## 4. 人设不崩（角色约束）

- 每个角色的 `system_prompt` 定义身份、语气、知识边界与禁忌
  （见包内 `characters.json`）。
- 涉及主线悬念（如《清鸣》的"先声""白页身世"）的角色，
  prompt 中应要求**保持模糊或回避**，避免剧透。
- 建议在 system_prompt 中显式声明：「你不知道自己不应该知道的事」。

## 5. 首次配置向导（setup_first_run）

1. 说明页：告知 Key 用途、**明文存储在 `user://settings.cfg`**、可随时清除。
2. 输入：Base URL（预填默认）/ Model（下拉 + 可手填）/ API Key（`Secret` 模式）。
3. 「测试连接」：发一句 `ping`，显示成功/失败与 HTTP 状态。
4. 「保存并继续」→ 写盘 → 进主菜单。
5. 「跳过」→ `game/llm_enabled = false`，纯剧本可玩。

## 6. 隐私与安全

- Key 只发往玩家配置的 `base_url`，不经过引擎作者的任何服务器。
- 不记录、不上传玩家对话内容。
- 发行时不提交任何 Key：`.env` / 本地配置一律进 `.gitignore`。