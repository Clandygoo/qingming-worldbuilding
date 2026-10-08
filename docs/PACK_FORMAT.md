# 世界观包格式（PACK FORMAT）

世界观包是可供玩家导入的 **zip**，内容是**纯数据**（JSON / 图片 / 音频 / 字体）。
引擎 `ModManager` 负责安全校验与安装；**绝不执行包内任何代码**。

## 1. 目录结构

```
my_pack.zip
├── manifest.json          # 必需，包元数据
├── story.json             # 入口剧本（由 manifest.entry 指定）
├── characters.json        # 角色（可选）
├── README.md              # 面向玩家 / 审核的说明（建议）
├── CREDITS.md             # 素材来源与授权（建议）
├── portraits/             # 立绘（可选）
├── bg/                    # 背景（可选）
└── fonts/                 # 字体（可选）
```

## 2. manifest.json

### 2.1 引擎必需字段

| 字段 | 说明 |
|---|---|
| `id` | 包标识，匹配 `^[a-z0-9_]{2,32}$` |
| `name` | 显示名 |
| `version` | 版本号 |
| `entry` | 入口剧本路径（如 `story.json`），其 JSON 的 `id` **必须等于** `manifest.id` |

### 2.2 生态扩展字段（推荐）

```json
{
  "id": "my_pack", "name": "我的世界观", "version": "1.0.0", "entry": "story.json",
  "author": "作者名",
  "license": "CC BY-NC-SA 4.0",
  "engine_version": ">=0.1.0",
  "homepage": "https://...", "source": "https://...",
  "description": "一句话简介",
  "content_rating": "all | teen | mature",
  "content_descriptors": ["violence", "death"],
  "trigger_warnings": ["含暴力描写"],
  "donation_url": null
}
```

- `content_rating` / `content_descriptors` 见 [`CONTENT_POLICY.md`](../CONTENT_POLICY.md)。
- 引擎加载只依赖 2.1 的必需字段；扩展字段用于索引、分级与展示。

## 3. characters.json

```json
{ "characters": [
  { "id": "kelxi", "name": "凯尔希", "color": "#8fb0c0",
    "portraits": { "neutral": "portraits/kelxi_neutral.png" },
    "system_prompt": "你是凯尔希……", "voice_pitch": 1.0 }
] }
```

- 合并顺序：本体 `res://data/base/characters.json` → 各副本 `characters.json`；
  **同 id 后者覆盖前者**。
- `system_prompt` 约束 LLM 人设；`color` 用于名字着色；`voice_pitch` 预留。

## 4. 安全约束（导入时由 ModManager 强制）

| 约束 | 值 / 规则 |
|---|---|
| zip 大小 | ≤ 64 MB |
| 条目数 | ≤ 512 |
| 单文件解压后 | ≤ 32 MB |
| 解压总量 | ≤ 128 MB |
| 字体单文件 | ≤ 24 MB |
| 允许扩展名 | `json png jpg jpeg webp ogg wav mp3 ttf otf woff2`（+ 建议的 `md txt`） |
| 路径 | 拒绝 `..` 穿越与绝对路径；拒绝符号链接 |

> ⚠️ **待同步项**：包内 `README.md` 若要随 zip 分发，引擎白名单需加入 `md`/`txt`
> （当前引擎白名单不含，见 `docs/ARCHITECTURE.md` §6）。

导入流程（必须严格照做）：

1. 校验 zip 大小 → 解压到 `user://tmp/<随机>/`
2. 逐条校验条目名（穿越 / 绝对路径 / 扩展名 / 数量）
3. 读 `manifest.json`，校验必填字段与 `id` 合法性
4. `entry` 指向的 JSON 必须可解析且 `id` 与 manifest 一致
5. **全部通过**才改名到 `user://mods/<id>/`（已存在先移除）
6. 任一步失败：删掉 tmp 目录，`import_failed.emit(原因)`

## 5. 提交到生态索引

1. 阅读 [`CONTENT_POLICY.md`](../CONTENT_POLICY.md)。
2. `python3 tools/validate_manifest.py manifest.json` 本地自检。
3. `python3 tools/hard_rules.py <你的包目录>` 预筛。
4. 按 [`CONTRIBUTING.md`](../CONTRIBUTING.md) 提交到 `submissions/<pack-id>/`。