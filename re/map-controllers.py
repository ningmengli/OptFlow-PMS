#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re/map-controllers.py
把 485 条路由 × 控制器 × 端点串成一条可追溯链路

原理
----
生产前端 bundle（controller-*.js）虽经重排但未混淆，控制器以
    angular.module("bestvisionWeb").controller("NAME", [ ... function (...) { ... }]);
顺序注册。因此以「注册起点」切分，区间内出现的 /admin|/auth 端点
即该控制器的端点集合。

产出
----
re/page-api-map.json   state / url / template / controller / endpoints
re/controller-api.csv   controller -> endpoints 汇总
"""
import csv
import json
import os
import re
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(os.environ.get("TEMP", "/tmp"), "sgzj-re", "controller.js")

RE_REG = re.compile(r'angular\.module\("bestvisionWeb"\)\.controller\(\s*"([^"]+)"')
RE_EP = re.compile(r'["\'](/(?:admin|auth)[A-Za-z0-9_\-/\.]*\.json)["\']')


def split_controllers(text):
    """返回 [(name, start, end), ...]"""
    marks = [(m.group(1), m.start()) for m in RE_REG.finditer(text)]
    out = []
    for i, (name, start) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
        out.append((name, start, end))
    return out


def main():
    if not os.path.exists(BUNDLE):
        print("找不到 bundle：%s（先跑 fetch-re.ps1）" % BUNDLE)
        return 1
    text = open(BUNDLE, encoding="utf-8", errors="replace").read()

    blocks = split_controllers(text)
    print("识别控制器 %d 个" % len(blocks))

    ctrl2ep = OrderedDict()
    for name, s, e in blocks:
        eps = sorted(set(RE_EP.findall(text[s:e])))
        ctrl2ep[name] = eps

    total_eps = set()
    for v in ctrl2ep.values():
        total_eps.update(v)
    print("控制器覆盖端点 %d 个（全量基线 904）" % len(total_eps))

    # ---- 关联路由
    rows = []
    with open(os.path.join(HERE, "routes.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if not r.get("Tpl", "").startswith("views/"):
                continue
            ctrl = (r.get("Ctrl") or "").strip()
            eps = ctrl2ep.get(ctrl, [])
            mod = r["Tpl"].split("/")[1]
            rows.append(OrderedDict([
                ("state", r.get("State", "")),
                ("url", r.get("Url", "")),
                ("module", mod),
                ("template", r["Tpl"]),
                ("controller", ctrl),
                ("endpointCount", len(eps)),
                ("endpoints", eps),
            ]))

    with open(os.path.join(HERE, "page-api-map.json"), "w", encoding="utf-8") as f:
        json.dump({"target": "视光之家 6.9", "observedAt": "2026-09-30",
                   "pageCount": len(rows), "controllerCount": len(ctrl2ep),
                   "endpointTotal": len(total_eps), "pages": rows},
                  f, ensure_ascii=False, indent=1)

    with open(os.path.join(HERE, "controller-api.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Controller", "EndpointCount", "Endpoints"])
        for k, v in ctrl2ep.items():
            w.writerow([k, len(v), " | ".join(v)])

    # ---- 统计
    with_ep = [r for r in rows if r["endpointCount"] > 0]
    no_ep = [r for r in rows if r["endpointCount"] == 0]
    print("页面 %d：有端点 %d / 无端点 %d" % (len(rows), len(with_ep), len(no_ep)))

    per = defaultdict(int)
    for r in rows:
        per[r["module"]] += r["endpointCount"]
    print("\n各模块端点引用数（去重前）：")
    for m, c in sorted(per.items(), key=lambda x: -x[1]):
        print("  %-24s %4d" % (m, c))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
