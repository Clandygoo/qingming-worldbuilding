#!/usr/bin/env python3
"""从 submissions/ 生成 registry.json 索引。

用法：python3 tools/build_index.py [仓库根目录]

- 扫描 submissions/<pack-id>/manifest.json
- 合并到 registry.json（保留已有条目的 moderation / download / sha256）
- 只依赖标准库
"""

import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_manifest import validate  # noqa: E402


def _merge_entry(manifest: dict, old: dict | None) -> dict:
    old = old or {}
    entry = {
        "id": manifest.get("id"),
        "name": manifest.get("name"),
        "author": manifest.get("author", ""),
        "version": manifest.get("version"),
        "engine_version": manifest.get("engine_version", ""),
        "license": manifest.get("license", ""),
        "content_rating": manifest.get("content_rating", "all"),
        "content_descriptors": manifest.get("content_descriptors", []),
        "trigger_warnings": manifest.get("trigger_warnings", []),
        "homepage": manifest.get("homepage"),
        "download": manifest.get("download", old.get("download")),
        "sha256": manifest.get("sha256", old.get("sha256")),
        "donation_url": manifest.get("donation_url"),
        "moderation": old.get("moderation", {
            "status": "pending",
            "pipeline_version": "v0.1",
            "reviewed_at": None,
        }),
    }
    return entry


def build(root: str) -> int:
    reg_path = os.path.join(root, "registry.json")
    old_packs: dict[str, dict] = {}
    if os.path.isfile(reg_path):
        with open(reg_path, encoding="utf-8") as f:
            old_packs = {p["id"]: p for p in json.load(f).get("packs", [])}

    subs = os.path.join(root, "submissions")
    packs: list[dict] = []
    skipped: list[str] = []
    if os.path.isdir(subs):
        for name in sorted(os.listdir(subs)):
            if name.startswith("_"):
                continue
            mpath = os.path.join(subs, name, "manifest.json")
            if not os.path.isfile(mpath):
                continue
            errs = validate(mpath)
            if errs:
                skipped.append(f"{name}: {'; '.join(errs)}")
                continue
            with open(mpath, encoding="utf-8") as f:
                manifest = json.load(f)
            packs.append(_merge_entry(manifest, old_packs.get(manifest.get("id"))))

    registry = {
        "schema_version": 1,
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "packs": packs,
    }
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"✓ 已生成 registry.json：{len(packs)} 个包")
    for s in skipped:
        print(f"  ! 跳过 {s}")
    return 0


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    raise SystemExit(build(root))