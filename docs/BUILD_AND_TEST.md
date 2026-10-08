# 构建与测试（BUILD AND TEST）

## 1. 环境

- **Godot 4.7**（stable）。
- 开发机已装即可，无需额外依赖。
- 程序化美术 / 工具脚本用 **Python 3.10+**（标准库优先）。

macOS 下引擎路径示例：`/Applications/Godot.app/Contents/MacOS/Godot`。

## 2. 运行

```bash
# 导入资源（新增/改动资源后）
Godot --headless --path . --import

# 直接运行（走 boot → title）
Godot --path .
```

## 3. 自动化自检

### 3.1 引擎自检

```bash
Godot --headless --path . res://scenes/selftest.tscn
# 期望：SELFTEST PASS — N 项全部通过
```

覆盖：单例契约、剧本解析、角色合并、小游戏注册、存档等。

### 3.2 世界观包导入安全测试

```bash
# 先生成测试夹具（zip），再跑
python3 tools/mkmodtest.py          # 引擎仓库中的工具，输出到 /tmp/prts/modtest/
Godot --headless --path . res://scenes/modtest.tscn
# 期望：MODTEST PASS — 25 项全部通过
```

覆盖：正常导入、路径穿越 / 绝对路径 / 夹带脚本 / 非法 id / id 不一致 / 缺 manifest /
文件不存在，以及越权文件未落地与暂存清理。

> **注意**：夹具在 `/tmp` 下，系统清理后需重新生成，否则 modtest 会因「源文件不存在」失败。

## 4. 美术资源

程序化 SVG 由 `tools/make_art.py` 生成到 `assets/art/`：

```bash
python3 tools/make_art.py
```

- 文字用 fontTools 转 `<path>`（Godot 的 ThorVG SVG 解码器不支持 `<text>` / 滤镜 / 外链）。
- 生成后跑一次 `--import` 让 Godot 建立 `.import` 缓存。

## 5. 提交前检查清单

- [ ] `Godot --headless --path . --import` 无报错
- [ ] `SELFTEST PASS`
- [ ] 如改动了导入逻辑：`MODTEST PASS`
- [ ] 新增 JSON 通过对应 Schema 校验
- [ ] 未提交任何密钥（检查 `.gitignore` 与 `git diff`）
- [ ] 新增/修改的世界观包通过 `tools/validate_manifest.py`

## 6. 发布

- **源码仓库**：只含引擎与工具，**不含内置剧情**；世界观包单独发布/索引。
- **本体站**：发布游戏本体（导出产物）。
- 导出（示例，命令行）：

```bash
# macOS
Godot --headless --path . --export-release "macOS" build/AllByAI.dmg
# Windows / Linux 同理，按需配置 export preset
```

> 发行包**不包含** `tools/`；世界观包由玩家自行导入。