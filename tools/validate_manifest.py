#!/usr/bin/env python3
"""校验世界观包 manifest.json 的结构与字段。

用法：python3 tools/validate_manifest.py <manifest.json 路径>

只依赖标准库。退出码：0 通过，1 失败。
"""

import json
import os
import re
import sys

ID_RE = re.compile(r"^[a-z0-9_]{2,32}$")
REQUIRED = ["id", "name", "version", "entry"]
RATINGS = {"all", "teen", "mature"}
DESCRIPTORS = {
    "violence", "death", "gore", "horror", "substance",
    "language", "romance", "self_harm", "flashing", "sensitive",
}


def validate(path: str) -> list[str]:
    errors: list[str] = []

    if not os.path.isfile(path):
        return [f"文件不存在: {path}"]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON 解析失败: {e}"]

    if not isinstance(data, dict):
        return ["manifest 顶层必须是对象"]

    for field in REQUIRED:
        v = data.get(field)
        if v is None or str(v).strip() == "":
            errors.append(f"缺少必填字段或为空: {field}")

    mod_id = str(data.get("id", ""))
    if mod_id and not ID_RE.match(mod_id):
        errors.append(f"id 非法（需匹配 {ID_RE.pattern}）: {mod_id}")

    rating = data.get("content_rating")
    if rating is not None and rating not in RATINGS:
        errors.append(f"content_rating 必须是 {sorted(RATINGS)} 之一: {rating}")

    descs = data.get("content_descriptors", [])
    if not isinstance(descs, list):
        errors.append("content_descriptors 必须是数组")
    else:
        for d in descs:
            if d not in DESCRIPTORS:
                errors.append(f"未知 content_descriptor: {d}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 tools/validate_manifest.py <manifest.json>")
        return 2
    errors = validate(sys.argv[1])
    if errors:
        print(f"✗ 校验失败: {sys.argv[1]}")
        for e in errors:
            print(f"   - {e}")
        return 1
    print(f"✓ 校验通过: {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())