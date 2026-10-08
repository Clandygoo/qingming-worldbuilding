# 《清鸣》世界观 · 世界观包仓库

> 归属：**All by AI** 引擎生态 · 世界观包 / 索引仓库
> 一句话世界观：在"记忆会凝结成实体"的灾变后世界，一个没有过去的人，带领一群听得见死者之声的同伴，为滞留的声音"送行"——直到他发现，那些声音也许根本不是来自过去。

本仓库同时是：

1. **《清鸣》世界观包**（`manifest.json` + `story.json` + `characters.json` + `WORLDVIEW.md`）；
2. **世界观包索引与审核骨架**（`CONTENT_POLICY.md` / `REVIEW_PROCESS.md` / `registry.json` / `tools/`）；
3. **开发者文档入口**（[`docs/`](./docs/README.md)）。

> 项目采用**自建站 + 源码仓库**发行：源码仓库只带引擎，连内置剧情也通过世界观包导入；
> 本体站只放游戏本体；世界观包（含本作）免费，唯一允许的收款是自愿个人捐赠（Buy a Coffee）。

---

## 目录

| 路径 | 内容 |
|---|---|
| [`WORLDVIEW.md`](./WORLDVIEW.md) | 《清鸣》世界观架构与主线设计案 |
| [`manifest.json`](./manifest.json) | 本包元数据（含分级与许可） |
| [`story.json`](./story.json) | 入口剧本 |
| [`characters.json`](./characters.json) | 角色与 LLM 人设 |
| [`docs/`](./docs/README.md) | **开发文档**（引擎架构 / 剧本格式 / 包格式 / LLM / 构建测试 / 路线图） |
| [`CONTENT_POLICY.md`](./CONTENT_POLICY.md) | 内容政策：红线、分级、授权、商业化限制 |
| [`REVIEW_PROCESS.md`](./REVIEW_PROCESS.md) | 审核、申诉、举报与下架流程 |
| [`MODERATION_PIPELINE.md`](./MODERATION_PIPELINE.md) | 审核流水线技术设计 |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | 如何投稿世界观包 |
| [`DISCLAIMER.md`](./DISCLAIMER.md) | 免责声明 |
| [`registry.json`](./registry.json) · [`registry.schema.json`](./registry.schema.json) | 世界观包索引与其 Schema |
| [`submissions/`](./submissions/README.md) | 投稿区 |
| [`tools/`](./tools) | 校验 / 索引 / 预筛工具 |

---

## 快速开始（内容创作者）

```bash
# 1. 复制投稿模板
cp -r submissions/_template submissions/<你的包id>

# 2. 编辑 manifest.json，然后本地自检
python3 tools/validate_manifest.py submissions/<你的包id>/manifest.json

# 3. 硬规则预筛（可选）
python3 tools/hard_rules.py <你的包目录>

# 4. 提交 Pull Request
```

详见 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 与 [`docs/PACK_FORMAT.md`](./docs/PACK_FORMAT.md)。

---

## 合规与免责

- 全部专有名词为原创造词；力量体系为声学 / 共振科幻；**无宗教体系、无神明实体**。
- 本作为虚构作品，与任何现实国家、政权、组织、宗教及真实人物无关。
- 第三方世界观包由作者自负其责，平台仅提供索引与审核，**不作背书**。
  详见 [`DISCLAIMER.md`](./DISCLAIMER.md)。
- 若内容侵犯您的权益，请提交 issue，我们核实后及时处理。

## 授权

- **文字内容**（`*.md`、世界观设定）：[CC BY-NC-SA 4.0](./LICENSE) —— 署名 · 非商业 · 相同方式共享。
- **代码 / 工具**（`tools/` 下的脚本）：MIT。
- 详细见 [`LICENSE`](./LICENSE)。