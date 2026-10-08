# 投稿区（submissions）

每个世界观包一个子目录：`submissions/<pack-id>/`。

- `<pack-id>` 必须与包 `manifest.json` 的 `id` 一致，匹配 `^[a-z0-9_]{2,32}$`。
- 至少包含一个 `manifest.json`（可直接复制 `_template/`）。
- 自托管的包：`manifest.json` 里 `download` 指向你的公开下载地址；
  托管收录的包：把包文件一并提交，`download` 与 `sha256` 由维护者写入。

提交前：

```bash
python3 tools/validate_manifest.py submissions/<pack-id>/manifest.json
```

规则见 [`../CONTENT_POLICY.md`](../CONTENT_POLICY.md) 与 [`../REVIEW_PROCESS.md`](../REVIEW_PROCESS.md)。