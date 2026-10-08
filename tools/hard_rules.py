#!/usr/bin/env python3
"""世界观包硬规则预筛（审核流水线第 ②/③ 步的最小实现）。

用法：
    python3 tools/hard_rules.py <包目录>
    python3 tools/hard_rules.py <包.zip>

检查：
  - 文件扩展名白名单（与引擎 ModManager 对齐）
  - 路径穿越 / 绝对路径条目名
  - 体积上限（单文件 / 总量）
  - 明显的违规正则（收款账号、加密货币地址、站外交易链接）

退出码：0 未命中，1 命中红线。
"""

import os
import re
import sys
import zipfile

# 与引擎 ModManager.ALLOWED_EXT 对齐；额外放行 md/txt 供包内 README / 说明文档使用。
# 注意：引擎当前白名单不含 md/txt，正式分发前需将引擎白名单同步加上这两个后缀。
ALLOWED_EXT = {"json", "png", "jpg", "jpeg", "webp", "ogg", "wav", "mp3",
               "ttf", "otf", "woff2", "md", "txt"}
MAX_ENTRY_BYTES = 32 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024

BLACKLIST = [
    (re.compile(r"\b(?:0x[0-9a-fA-F]{40}|bc1[0-9a-z]{25,})\b"), "疑似加密货币地址"),
    (re.compile(r"(?i)\b(paypal|alipay|微信支付|收款码|银行卡号)\b"), "疑似收款信息"),
    (re.compile(r"(?i)https?://[^\s]+\.(exe|apk|dmg|msi|bat|sh)\b"), "疑似外链可执行文件"),
]


def _rel(name: str) -> str:
    n = name.replace("\\", "/")
    if n.startswith("/") or ":" in n:
        return ""
    parts = [p for p in n.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        return ""
    return "/".join(parts)


def scan_zip(path: str) -> list[str]:
    hits: list[str] = []
    total = 0
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            if _rel(name) == "":
                hits.append(f"非法条目名（穿越/绝对路径）: {name}")
                continue
            ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
            if ext not in ALLOWED_EXT:
                hits.append(f"不允许的文件类型 .{ext}: {name}")
            if info.file_size > MAX_ENTRY_BYTES:
                hits.append(f"单文件过大: {name} ({info.file_size} B)")
            total += info.file_size
            if ext in {"json"}:
                try:
                    text = zf.read(name).decode("utf-8", "ignore")
                except Exception:
                    continue
                for rx, why in BLACKLIST:
                    if rx.search(text):
                        hits.append(f"{why}: {name}")
    if total > MAX_TOTAL_BYTES:
        hits.append(f"解压总量超过上限: {total} B")
    return hits


def scan_dir(path: str) -> list[str]:
    hits: list[str] = []
    total = 0
    for base, _dirs, files in os.walk(path):
        for fn in files:
            full = os.path.join(base, fn)
            ext = fn.rsplit(".", 1)[-1].lower() if "." in fn else ""
            if ext not in ALLOWED_EXT:
                hits.append(f"不允许的文件类型 .{ext}: {os.path.relpath(full, path)}")
            try:
                size = os.path.getsize(full)
            except OSError:
                continue
            if size > MAX_ENTRY_BYTES:
                hits.append(f"单文件过大: {fn} ({size} B)")
            total += size
            if ext == "json":
                try:
                    with open(full, encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                except OSError:
                    continue
                for rx, why in BLACKLIST:
                    if rx.search(text):
                        hits.append(f"{why}: {fn}")
    if total > MAX_TOTAL_BYTES:
        hits.append(f"总量超过上限: {total} B")
    return hits


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 tools/hard_rules.py <包目录|包.zip>")
        return 2
    target = sys.argv[1]
    hits = scan_zip(target) if zipfile.is_zipfile(target) else scan_dir(target)
    if hits:
        print(f"✗ 命中红线: {target}")
        for h in hits:
            print(f"   - {h}")
        return 1
    print(f"✓ 未命中红线: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())