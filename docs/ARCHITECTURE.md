# 引擎架构

> 权威契约：`docs/SPEC.md`。本文是架构总览。

## 1. 定位

视觉小说 + LLM 自由对话 + 小游戏 + 玩家世界观包。不是 Galgame：
无好感度系统、叙事结构为「章节 + 场景 + 节点」、视觉为立绘 + 背景 + UI 叠加。

技术栈：**Godot 4.7（GDScript）**，纯数据驱动，外部内容不执行代码。

## 2. 目录结构

```
res://
├── autoload/         # 单例（顺序见 project.godot）
├── data/
│   ├── base/         # 本体内容（characters.json / story_*.json）
│   └── schema/       # JSON Schema
├── minigames/        # 内置小游戏（继承 MinigameBase）
├── scenes/           # boot / title / setup_first_run / novel / minigame_host
├── ui/               # 通用 UI 组件
├── tools/            # 开发工具（不进发行包）
└── assets/           # 字体、美术等（程序化生成见 make_art.py）

user://
├── settings.cfg      # 配置（含 LLM key，明文）
├── mods/<id>/        # 导入的世界观包
├── saves/slot_<n>.json
└── tmp/              # 解压暂存
```

## 3. 单例（autoload）与初始化顺序

顺序有依赖：`Settings` 必须最先（其他单例 `_ready` 可能读配置）。

| 顺序 | 单例 | 职责 |
|---|---|---|
| 1 | **Settings** | 配置读写（`user://settings.cfg`），LLM key、默认值 |
| 2 | **LLMClient** | OpenAI 兼容 `chat/completions`，单请求串行 |
| 3 | **Story** | 剧本解析 + 播放状态机 + 跳转 |
| 4 | **CharacterDB** | 合并本体与各包的 `characters.json`，同 id 副本覆盖 |
| 5 | **MinigameHost** | 小游戏注册与调度 |
| 6 | **ModManager** ★安全关键 | 世界观包导入 / 校验 / 加载 |
| 7 | **SaveSystem** | 存档读写 |

## 4. 数据流

### 4.1 剧本播放
```
story_*.json → Story.load_chapter()（校验）
            → Story.play() → node_entered(node)
            → novel.gd 按 type 渲染（line/narrate/bg/bgm/choice/llm/minigame）
            → 玩家点击 Story.advance() / 选择 Story.choose(i)
            → 跳转解析（@label / 整数偏移）→ 目标不存在则 chapter_finished
```
- 每个节点 `type` 是判别器；小游戏类型用独立字段 `game`。
- 节点在 `novel.gd._on_node_entered` 处理后发 `node_finished`；
  `choice/llm/minigame` 节点会**阻塞 `advance()`**，等待玩家交互。

### 4.2 LLM 对话
```
novel._open_chat(node) → LLMClient.chat(system_prompt, user_text, history)
                       → HTTPRequest → {base_url}chat/completions
                       → response_received / request_failed
                       → 成功显示，失败显示 fallback 台词
```
- 每个角色的 `system_prompt` 来自 `CharacterDB`，约束人设不崩。
- 历史长度上限 `HISTORY_LIMIT = 20`；`_busy` 时直接返回 "busy"（不排队）。

### 4.3 小游戏
```
minigame 节点 → MinigameHost.run(game, params)
             → 实例化到 minigame_host.tscn 容器
             → completed(success) → minigame_finished → Story 跳 on_success/on_fail
```
- 未注册类型 → `minigame_finished(false)` 并告警，不崩。

### 4.4 世界观包
```
玩家导入 zip → ModManager.import_zip()（见 PACK_FORMAT.md 安全流程）
             → 校验通过改名到 user://mods/<id>/
             → CharacterDB.load_all() 重新合并角色
```

## 5. 场景流转

```
boot.tscn ──> title.tscn ──(开始游戏)──> setup_first_run.tscn（未配置时）
                                 │                  │
                                 └──(已配置)────────┴──> novel.tscn
                       title ──(设置)──> setup_first_run.tscn
```

## 6. 安全模型

- 世界观包**只有数据**：JSON / 图片 / 音频 / 字体。**绝不执行包内代码**。
- 导入时逐条校验：路径穿越、绝对路径、扩展名白名单、体积、条目数、
  manifest 必填、`entry.id` 与 manifest `id` 一致。
- 小游戏必须是 `MinigameHost.available_types()` 已注册类型。
- LLM key 明文存于 `user://settings.cfg`，**绝不写入日志**（日志用 `[已隐藏]`）。

## 7. 代码规范

- GDScript 4.7，**所有变量和函数签名带类型标注**。
- autoload 单例**不加** `class_name`；`minigames/` 下的类**加** `class_name`。
- 信号用过去式命名（`request_started` / `node_entered`）；私有成员前缀 `_`。
- 文件读写一律 `FileAccess`，路径用 `res://` / `user://`。
- 无 try/except：解析外部 JSON 必须显式判空（`JSON.parse_string` 失败返回 `null`）。
- 中文注释解释「为什么」；不留空 `pass` 占位，未完成写 `# TODO` 并说明缺什么。