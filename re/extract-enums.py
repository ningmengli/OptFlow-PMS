#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re/extract-enums.py
从生产前端 bundle 抽取枚举常量

生产用两种模式承载枚举：
  1) 数组： [{id: 0, name: "开启"}, {id: 1, name: "停用"}]
  2) 映射： { 0: "效果不佳", 1: "价格问题", ... }

本脚本把两种模式全量抽出，落 re/enums.json + re/spec/90-枚举总表.md
只读：仅分析已下载到本地的静态 bundle，不发起任何网络请求。
"""
import json
import os
import re
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(os.environ.get("TEMP", "/tmp"), "sgzj-re")

RE_ARRAY_ENUM = re.compile(
    r'(?P<name>[A-Za-z_$][A-Za-z0-9_$]{2,50})\s*[:=]\s*\[(?P<body>(?:\s*\{\s*id\s*:\s*[^,}]+,\s*name\s*:\s*[\'"][^\'"]+[\'"]\s*\}\s*,?){1,40})\]',
    re.S)
RE_ITEM = re.compile(r'id\s*:\s*["\']?([^,"\'}\s]+)["\']?\s*,\s*name\s*:\s*[\'"]([^\'"]+)[\'"]')
# 末项允许无逗号
RE_MAP_ENUM = re.compile(
    r'(?P<name>[A-Za-z_$][A-Za-z0-9_$]{2,50})\s*[:=]\s*\{(?P<body>(?:\s*["\']?\d+["\']?\s*:\s*["\'][^"\']+["\']\s*,){0,39}\s*["\']?\d+["\']?\s*:\s*["\'][^"\']+["\']\s*)\}',
    re.S)
RE_MAP_ITEM = re.compile(r'["\']?(\d+)["\']?\s*:\s*["\']([^"\']+)["\']')

# 只有含中文的才算业务枚举，过滤掉 URL / 样式等
CJK = re.compile(r'[\u4e00-\u9fa5]')
# 排除明显非枚举的键
SKIP = re.compile(r'url|Url|URL|path|Path|css|class|style|icon|src|href|color|font|margin|padding|width|height')


def main():
    bundles = {}
    for name in ("controller.js", "property.js", "factory.js", "directive.js", "main.js"):
        p = os.path.join(TMP, name)
        if os.path.exists(p):
            bundles[name] = open(p, encoding="utf-8", errors="replace").read()
    print("分析 bundle：%s" % ", ".join(bundles))

    arr = OrderedDict()
    mp = OrderedDict()
    for bname, text in bundles.items():
        for m in RE_ARRAY_ENUM.finditer(text):
            name = m.group("name")
            if SKIP.search(name):
                continue
            items = [(i.group(1).strip(), i.group(2).strip())
                     for i in RE_ITEM.finditer(m.group("body"))]
            if not items or not any(CJK.search(n) for _, n in items):
                continue
            # 按内容去重：同名不同义是常态，必须区分
            sig = "|".join("%s=%s" % kv for kv in items)
            key = "%s :: %s" % (name, sig)
            if key in arr:
                arr[key]["occurrences"] += 1
            else:
                arr[key] = {"name": name, "items": items,
                            "bundle": bname, "occurrences": 1}
        for m in RE_MAP_ENUM.finditer(text):
            name = m.group("name")
            if SKIP.search(name):
                continue
            items = [(i.group(1), i.group(2).strip())
                     for i in RE_MAP_ITEM.finditer(m.group("body"))]
            if len(items) < 2 or not any(CJK.search(n) for _, n in items):
                continue
            sig = "|".join("%s=%s" % kv for kv in items)
            key = "%s :: %s" % (name, sig)
            if key in mp:
                mp[key]["occurrences"] += 1
            else:
                mp[key] = {"name": name, "items": items,
                           "bundle": bname, "occurrences": 1}

    print("数组型枚举 %d 个 / 映射型枚举 %d 个" % (len(arr), len(mp)))

    out = OrderedDict([
        ("target", "视光之家 6.9"),
        ("observedAt", "2026-09-30"),
        ("arrayEnums", arr),
        ("mapEnums", mp),
    ])
    with open(os.path.join(HERE, "enums.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # Markdown 总表
    L = ["# 90｜枚举总表（生产实测）\n",
         "> 由 `re/extract-enums.py` 从本地 bundle 自动抽取。**只含 bundle 中真实出现的中文枚举**，不含推测。",
         "> 数组型 %d 组 / 映射型 %d 组（已按内容去重；同名不同义分别列出，`出现次数` 为 bundle 内重复定义次数）\n"
         % (len(arr), len(mp)),
         "## §1 数组型枚举（`[{id, name}]`）\n"]
    for key, o in arr.items():
        L.append("### `%s` 　<sub>出现 %d 次</sub>\n" % (o["name"], o["occurrences"]))
        L.append("| 取值 | 名称 |")
        L.append("|---|---|")
        for k, v in o["items"]:
            L.append("| `%s` | %s |" % (k, v))
        L.append("")
    L.append("## §2 映射型枚举（`{code: name}`）\n")
    for key, o in mp.items():
        L.append("### `%s` 　<sub>出现 %d 次</sub>\n" % (o["name"], o["occurrences"]))
        L.append("| 取值 | 名称 |")
        L.append("|---|---|")
        for k, v in o["items"]:
            L.append("| `%s` | %s |" % (k, v))
        L.append("")
    os.makedirs(os.path.join(HERE, "spec"), exist_ok=True)
    with open(os.path.join(HERE, "spec", "90-枚举总表.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("写出 enums.json 与 spec/90-枚举总表.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
