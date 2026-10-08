# 剧本格式（STORY FORMAT）

剧本是章节 JSON，由 `Story` 单例加载播放。结构：`id` / `title` / `nodes[]`。

## 1. 章节结构

```json
{
  "id": "ch01",
  "title": "第一章 · 苏醒",
  "nodes": [ { "type": "narrate", "text": "……" } ]
}
```

- `id` / `title` 必填；`nodes` 必须是数组。
- 每个节点必须有 `type`，且在允许集合内；未知 type → 记 warning **跳过**（不崩溃）。
- 同一对象内不得出现重复键（`type` 是判别器，小游戏类型另用 `game` 字段）。

## 2. 节点类型

| type | 说明 | 关键字段 |
|---|---|---|
| `line` | 单句台词 | `speaker`（显示名）、`speaker_id`（角色 id）、`text`、`emotion` |
| `narrate` | 旁白 | `text` |
| `bg` | 切背景 | `bg`（资源路径）、`transition`（`fade` / `instant`） |
| `bgm` | 切音乐 | `bgm`、`loop` |
| `choice` | 分支 | `prompt`、`options[{ text, goto }]` |
| `llm` | LLM 自由对话 | `character`（角色 id）、`hint`、`fallback` |
| `minigame` | 小游戏 | `game`（**不是** type）、`params{}`、`on_success`、`on_fail` |

可选字段：任意节点可加 `"label": "name"`，供跳转定位。

## 3. 示例

```json
{
  "id": "ch01",
  "title": "第一章",
  "nodes": [
    { "type": "bg", "bg": "res://assets/art/bg/medbay.svg", "transition": "fade" },
    { "type": "narrate", "text": "顶灯亮起，白得刺眼。" },
    { "label": "wake_up",
      "type": "line", "speaker": "???", "speaker_id": "kelxi",
      "emotion": "neutral", "text": "……醒了。" },
    { "type": "choice", "prompt": "你想先问什么？",
      "options": [
        { "text": "我昏迷了多久？", "goto": "@ask_time" },
        { "text": "……先让我一个人待会儿。", "goto": "@alone" }
      ] },
    { "label": "ask_time",
      "type": "line", "speaker": "???", "speaker_id": "kelxi", "text": "两年零七个月。" },
    { "label": "alone",
      "type": "minigame", "game": "sequence",
      "params": { "length": 4, "speed": 0.6 },
      "on_success": "@ok", "on_fail": "@fail" },
    { "label": "ok", "type": "narrate", "text": "成功了。" },
    { "label": "fail", "type": "narrate", "text": "失败了。" },
    { "type": "llm", "character": "kelxi",
      "hint": "（你可以自由提问。）",
      "fallback": "……（她只是看着你，没有说话。）" },
    { "type": "narrate", "text": "——完——" }
  ]
}
```

## 4. 跳转语义（`goto`）

- `"@label"`：跳到带有 `"label": "label"` 的节点。
- **整数**：相对当前节点的偏移（如 `1` 表示下下个节点）。
- `choice.options[].goto` 与 `minigame.on_success/on_fail` 均适用。
- **任何跳转目标不存在 → 发 `chapter_finished` 结束，不崩溃。**

## 5. 播放行为

- `line` / `narrate` / `bg` / `bgm`：等待玩家点击 `advance()` 推进。
- `choice` / `llm` / `minigame`：**阻塞** `advance()`，由玩家操作结果推进
  （`choose()` / 对话关闭 / 小游戏 `completed`）。

## 6. 校验清单

- [ ] 根字段 `id`、`title` 存在
- [ ] `nodes` 是数组，每个元素是对象
- [ ] 每个节点 `type` 合法（`line/narrate/bg/choice/llm/minigame/bgm`）
- [ ] `choice.options[].goto` 指向的 label 存在
- [ ] `minigame.game` 在 `MinigameHost.available_types()` 内
- [ ] `line.speaker_id` 在 `characters.json` 中（否则立绘/颜色取默认）

## 7. 与 LLM 的耦合（送行玩法）

「送行对话」依赖信息补全：当玩家尚未在关卡 / 探索中获得关键线索时，
LLM 对话会出现「断片」（信息不足则回避关键内容）。线索可作为
`Story` 的变量或独立状态传给对话系统（玩法细化见 `ROADMAP.md`）。