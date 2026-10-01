#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re/fetch-pages.py
视光之家 6.9 页面模板结构化抓取器（一比一对标用）

只读保证
--------
- 仅 GET https://<PROD_HOST>/pc/views/** 下的**静态 HTML 模板**
- 不携带 Cookie / Token / 任何凭据
- 不调用 /admin/*.json 或 /auth/*.json 业务端点
- 不产生任何生产数据写入
- 限速 150ms/请求，对生产无压力

产出
----
%TEMP%/sgzj-re/pages/<模板路径>   原始模板缓存（可续跑）
re/pages.json                    485 页结构化规格
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import OrderedDict, defaultdict

BASE = os.environ.get("SGVJ_PROD_HOST", "https://<PROD_HOST>/pc/")
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.environ.get("TEMP", "/tmp"), "sgzj-re", "pages")
DELAY = 0.15
RETRIES = 3
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OptFlow-PMS-ReverseEng/1.0 (read-only)"


# ---------------------------------------------------------------- 文本工具
def clean(s):
    if s is None:
        return ""
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def read_routes():
    path = os.path.join(HERE, "routes.csv")
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f)]


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return open(dest, encoding="utf-8", errors="replace").read(), "cache"
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read().decode("utf-8", errors="replace")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(data)
            time.sleep(DELAY)
            return data, "net"
        except Exception as e:                       # noqa: BLE001
            if attempt == RETRIES - 1:
                return "", "fail:%s" % e
            time.sleep(1.0 * (attempt + 1))
    return "", "fail"


# ---------------------------------------------------------------- 结构抽取
RE_MODEL = re.compile(r'ng-model\s*=\s*["\']([^"\']+)["\']')
RE_MODEL2 = re.compile(r'\bmodel\s*=\s*["\']([^"\']+)["\']')          # 自定义指令
RE_LABEL = re.compile(r"<label[^>]*>(.*?)</label>", re.S | re.I)
RE_TH = re.compile(r"<th[^>]*>(.*?)</th>", re.S | re.I)
RE_CLICK = re.compile(r'ng-click\s*=\s*["\']([^"\']+)["\']')
RE_SREF = re.compile(r'ui-sref\s*=\s*["\']([^"\']+)["\']')
RE_REPEAT = re.compile(r'ng-repeat\s*=\s*["\']([^"\']+)["\']')
RE_INTERP = re.compile(r"\{\{\s*([^}]+?)\s*\}\}")
RE_TYPE = re.compile(r'type\s*=\s*["\'](text|number|date|datetime-local|password|email|file|checkbox|radio|submit)["\']', re.I)
RE_INPUT = re.compile(r"<input\b[^>]*>", re.I)
RE_TEXTAREA = re.compile(r"<textarea\b[^>]*>(.*?)</textarea>", re.S | re.I)
RE_SELECT = re.compile(r"<select\b[^>]*>(.*?)</select>", re.S | re.I)
RE_NGOPTIONS = re.compile(r'ng-options\s*=\s*["\']([^"\']+)["\']')
RE_HREF_STATE = re.compile(r'ui-sref\s*=\s*["\']([\w.]+)[\'"]')
RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)


def parse_template(raw):
    """从一个 Angular 模板中抽取结构化规格。"""
    spec = OrderedDict()

    # 标题
    m = RE_TITLE.search(raw)
    spec["title"] = clean(m.group(1)) if m else ""

    # 字段绑定（ng-model + 自定义指令的 model 属性）
    models = []
    for x in RE_MODEL.findall(raw):
        x = x.strip()
        if x and x not in models:
            models.append(x)
    for x in RE_MODEL2.findall(raw):
        x = x.strip()
        if x and x not in models:
            models.append(x)
    spec["bindings"] = models

    # 字段标签
    labels = []
    for x in RE_LABEL.findall(raw):
        c = clean(x)
        if c and c not in labels and len(c) < 60:
            labels.append(c)
    spec["labels"] = labels

    # 必填标记（label 内的 asterisk）
    required = []
    for m2 in re.finditer(r"<label[^>]*>(.*?)</label>", raw, re.S | re.I):
        inner = m2.group(1)
        c = clean(inner)
        if c and re.search(r'class\s*=\s*["\']asterisk["\']', inner):
            if c not in required:
                required.append(c)
    spec["requiredLabels"] = required

    # 表格列
    spec["tableColumns"] = [clean(x) for x in RE_TH.findall(raw) if clean(x)]

    # 交互动作
    acts = []
    for x in RE_CLICK.findall(raw):
        x = x.strip()
        if x and x not in acts and len(x) < 160:
            acts.append(x)
    spec["actions"] = acts

    # 导航目标
    spec["navigatesTo"] = sorted(set(RE_HREF_STATE.findall(raw)))

    # 循环列表
    spec["repeats"] = sorted(set(x.strip() for x in RE_REPEAT.findall(raw) if x.strip()))

    # 插值显示字段
    interp = []
    for x in RE_INTERP.findall(raw):
        x = x.strip()
        if x and x not in interp and len(x) < 80:
            interp.append(x)
    spec["interpolations"] = interp

    # 输入控件类型统计
    types = defaultdict(int)
    for itag in RE_INPUT.findall(raw):
        mt = RE_TYPE.search(itag)
        if mt:
            types[mt.group(1).lower()] += 1
    else:
        pass
    if "<textarea" in raw.lower():
        types["textarea"] += 1
    if "<select" in raw.lower():
        types["select"] += 1
    spec["inputTypes"] = dict(types)

    # 下拉枚举
    spec["enumOptions"] = [x.strip() for x in RE_NGOPTIONS.findall(raw) if x.strip()]

    # 多选/单选的可辨识选项
    opts = []
    for m3 in re.finditer(r'ng-options\s*=\s*["\']([^"\']+)["\']', raw):
        expr = m3.group(1)
        if "." in expr and " as " in expr:
            opts.append(expr.strip())
    spec["selectOptions"] = sorted(set(opts))

    return spec


# ---------------------------------------------------------------- 主流程
def main():
    routes = read_routes()
    routes = [r for r in routes if r.get("Tpl", "").startswith("views/")]
    print("待抓取模板：%d 个" % len(routes), flush=True)

    out = []
    ok = cached = fail = 0
    for i, r in enumerate(routes, 1):
        tpl = r["Tpl"]
        url = BASE + tpl
        dest = os.path.join(CACHE, tpl)
        raw, how = fetch(url, dest)
        if how.startswith("fail") or not raw:
            fail += 1
            rec = {"template": tpl, "state": r.get("State", ""),
                   "url": r.get("Url", ""), "controller": r.get("Ctrl", ""),
                   "error": how}
        else:
            ok += 1
            if how == "cache":
                cached += 1
            rec = {"template": tpl, "state": r.get("State", ""),
                   "url": r.get("Url", ""), "controller": r.get("Ctrl", ""),
                   "bytes": len(raw)}
            rec.update(parse_template(raw))
        mod = tpl.split("/")[1] if "/" in tpl else "?"
        rec["module"] = mod
        out.append(rec)
        if i % 40 == 0 or i == len(routes):
            print("  [%3d/%d] 成功=%d 缓存=%d 失败=%d" % (i, len(routes), ok, cached, fail), flush=True)

    dest_json = os.path.join(HERE, "pages.json")
    with open(dest_json, "w", encoding="utf-8") as f:
        json.dump({"target": "视光之家 6.9", "observedAt": "2026-09-30",
                   "pageCount": len(out), "failed": fail, "pages": out},
                  f, ensure_ascii=False, indent=1)

    print("\n写出 %s" % dest_json)
    print("成功 %d / 失败 %d / 缓存命中 %d" % (ok, fail, cached))
    if fail:
        print("失败清单已记录在 pages.json 的 error 字段", file=sys.stderr)
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
