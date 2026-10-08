# 世界观包生态（ECOSYSTEM）

## 1. 三层结构

```
引擎本体（源码仓库，公开）  ←→  世界观包索引站（自建，registry.json）
        │                                    │
        │ 玩家导入                            │ 收录 / 下架
        ▼                                    ▼
        世界观包（第三方作者，纯数据，免费）
```

| 层 | 内容 | 责任方 |
|---|---|---|
| 引擎 | 运行时、导入器（安全校验）、UI | 项目作者 |
| 索引 | 收录规则、审核、下架 | 平台运营方 |
| 世界观包 | 剧情、素材、观点 | 第三方作者 |

## 2. 收录模型

- **索引收录（默认）**：平台只记录 `manifest`、下载地址、作者、许可、审核结论；
  包文件由作者**自行托管**。平台责任较轻。
- **托管收录（可选）**：作者将包提交到平台仓库，由平台存储与分发；需承担下架义务。

两者都走同一审核流程。

## 2.1 发行渠道

本项目采用**自建站 + 源码仓库**发行：
- Apple / Google 商店的内购与外部捐赠限制**不适用**；
- 源码仓库**只带引擎**，连内置剧情也通过世界观包导入；
- 本体站只放游戏本体。

## 3. 规则文档

| 文档 | 作用 |
|---|---|
| [`CONTENT_POLICY.md`](../CONTENT_POLICY.md) | 收录规则：红线、分级、授权、商业化限制 |
| [`REVIEW_PROCESS.md`](../REVIEW_PROCESS.md) | 审核、申诉、举报与 Takedown |
| [`MODERATION_PIPELINE.md`](../MODERATION_PIPELINE.md) | 自动化预筛 + 人工终审的技术实现 |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | 如何投稿 |
| [`DISCLAIMER.md`](../DISCLAIMER.md) | 平台免责声明 |

## 4. 索引与工具

- `registry.json`：机读索引（唯一权威数据源），由 `tools/build_index.py` 生成。
- `registry.schema.json`：索引校验 Schema。
- `submissions/<pack-id>/`：投稿区（见 `submissions/README.md`）。
- `tools/validate_manifest.py`：本地自检 manifest。
- `tools/hard_rules.py`：硬规则预筛（扩展名 / 路径 / 体积 / 违规正则）。

## 5. 关键红线（速记）

1. 自动化只预筛、**不自动放行**；异常 / 超时一律转人工。
2. 政治 / 法律红线**交人工**判定，模型只出敏感度分数。
3. 不因末世 / 战争题材本身拒稿——**分级标注，而非封杀**。
4. 世界观包**必须免费**，唯一允许的是自愿个人捐赠（Buy a Coffee）。
5. 审核（内容）与 `ModManager`（安全）是**两道独立防线**。