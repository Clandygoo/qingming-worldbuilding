# 贡献指南（CONTRIBUTING）

感谢你为 All by AI 生态创作世界观包。请先阅读本指南，再提交。

## 一、你可以贡献什么

| 类型 | 说明 |
|---|---|
| 世界观包 | 剧情 / 角色 / 关卡等纯数据内容 |
| 政策与流程改进 | 对 `CONTENT_POLICY.md` / `REVIEW_PROCESS.md` 的改进建议 |
| 工具 | `tools/` 下的校验、索引、审核辅助脚本 |

## 2. 提交世界观包

### 2.1 两种收录方式

1. **自托管 + 索引收录（推荐）**
   - 你把自己的世界观包托管在你自己的仓库 / 站点；
   - 向本仓库提交一个 `submissions/<pack-id>/manifest.json`，指向你的下载地址。
2. **托管收录**
   - 通过 Pull Request 把包提交到 `submissions/<pack-id>/`。
   - `download` 与 `sha256` 由维护者归档后写入。

### 2.2 提交前必做

1. 阅读并遵守 [`CONTENT_POLICY.md`](./CONTENT_POLICY.md)。
- 确保 `manifest.json` 通过 `tools/validate_manifest.py` 校验。
- 确认包内素材**自己拥有或已获授权**，许可允许再分发。
- 如实填写 `content_rating` / `content_descriptors` / `trigger_warnings`。
- 世界观包**必须免费**；唯一允许的收款是自愿个人捐赠（"Buy a Coffee"）。

### 3. 提交方式

1. Fork 本仓库。
2. 在 `submissions/<你的包id>/` 下添加 `manifest.json`（可复制 `submissions/_template/`）。
3. 运行本地校验：`python3 tools/validate_manifest.py submissions/<你的包id>/manifest.json`
4. 提交 Pull Request，说明包的内容与来源授权。

审核流程见 [`REVIEW_PROCESS.md`](./REVIEW_PROCESS.md)。

## 4. 提交代码/工具

- 保持与现有脚本风格一致，Python 3，无第三方依赖优先。
- 提交前自测通过。

## 5. 禁止事项

- 盗用他人素材、夹带可执行文件、违规内容、收费解锁。
- 提交真实货币赌博机制、站外交易引导。

## 6. 行为准则

尊重其他创作者。审核只针对内容合规，不评判题材与风格。末世、战争、悬疑题材**不被歧视**，只需如实分级。