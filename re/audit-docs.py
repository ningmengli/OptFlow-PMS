#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/audit-docs.py
文档自检：把 485 个生产页面逐个对照 re/spec/ 分册 + routes.csv + pages.json
只读，不修改任何文件。输出机器可读的自检报告。
"""
import csv, json, os, re, collections

BASE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(BASE, 'spec')
ROUTES = os.path.join(BASE, 'routes.csv')
PAGES = os.path.join(BASE, 'pages.json')
API_MAP = os.path.join(BASE, 'page-api-map.json')
GRAPH = os.path.join(BASE, 'ui-graph.json')

ROW = re.compile(
    r'^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|')
HEAD_PAGECOUNT = re.compile(r'\|\s*页面数\s*\|\s*\*{0,2}(\d+)\*{0,2}\s*\|')
HEAD_CN = re.compile(r'\|\s*中文名\s*\|\s*(.+?)\s*\|')
HEAD_DIR = re.compile(r'\|\s*模块目录\s*\|\s*`([^`]+)`\s*\|')
HEAD_WAVE = re.compile(r'\|\s*开发波次\s*\|\s*(.+?)\s*\|')


def load_routes():
    out = []
    with open(ROUTES, encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().strip('﻿')
                if st.lower() == 'state':      # 跳过表头
                    continue
                out.append({'state': st, 'url': row[1].strip(),
                            'controller': row[2].strip(), 'template': row[3].strip()})
    return out


def parse_spec():
    """返回 (分册列表, 分册内页面行列表)"""
    books, rows = [], []
    for fn in sorted(os.listdir(SPEC)):
        if not fn.endswith('.md') or fn.startswith('90-'):
            continue
        p = os.path.join(SPEC, fn)
        with open(p, encoding='utf-8') as f:
            lines = f.readlines()
        head = {'file': fn, 'declaredPages': None, 'cnName': None,
                'dir': None, 'wave': None, 'actualRows': 0}
        for ln in lines[:40]:
            m = HEAD_PAGECOUNT.search(ln)
            if m:
                head['declaredPages'] = int(m.group(1))
            m = HEAD_CN.search(ln)
            if m:
                head['cnName'] = m.group(1).strip()
            m = HEAD_DIR.search(ln)
            if m:
                head['dir'] = m.group(1)
            m = HEAD_WAVE.search(ln)
            if m:
                head['wave'] = m.group(1).strip()
        for ln in lines:
            m = ROW.match(ln)
            if m:
                head['actualRows'] += 1
                rows.append({
                    'book': fn, 'idx': int(m.group(1)), 'state': m.group(2),
                    'url': m.group(3), 'template': m.group(4),
                    'controller': m.group(5), 'endpoints': int(m.group(6)),
                })
        books.append(head)
    return books, rows


def main():
    routes = load_routes()
    with open(PAGES, encoding='utf-8') as f:
        pages = f.read()
    books, rows = parse_spec()
    with open(GRAPH, encoding='utf-8') as f:
        graph = json.load(f)

    R = {r['state']: r for r in routes}
    findings = collections.OrderedDict()

    # ---------- 1. 总量 ----------
    findings['1_总量'] = {
        'routes.csv 路由数': len(routes),
        'pages.json 声明页数': json.loads(pages)['pageCount'],
        'spec 分册数（不含枚举表）': len(books),
        'spec 页面行总数': len(rows),
        '分册声明页数之和': sum(b['declaredPages'] or 0 for b in books),
        'ui-graph 状态数': graph['totals']['states'],
    }

    # ---------- 2. 覆盖：分册是否漏页 / 多页 ----------
    spec_states = collections.Counter(r['state'] for r in rows)
    route_states = set(R)
    missing = sorted(route_states - set(spec_states))
    extra = sorted(set(spec_states) - route_states)
    dup = {s: c for s, c in spec_states.items() if c > 1}
    findings['2_覆盖'] = {
        '路由中未出现在任何分册的state数': len(missing),
        '未覆盖样例': missing[:20],
        '分册中出现但路由表没有的state数': len(extra),
        '多出样例': extra[:20],
        '分册内重复登记的state数': len(dup),
        '重复明细': dup,
    }

    # ---------- 3. 分册声明页数 vs 实际行数 ----------
    mismatch = []
    for b in books:
        if b['declaredPages'] is not None and b['declaredPages'] != b['actualRows']:
            mismatch.append({'book': b['file'], 'declared': b['declaredPages'],
                             'actualRows': b['actualRows']})
    findings['3_分册页数自洽'] = {
        '声明与实际行数不符的分册数': len(mismatch),
        '明细': mismatch,
        '声明合计': sum(b['declaredPages'] or 0 for b in books),
        '实际行数合计': len(rows),
    }

    # ---------- 4. 重复模板（同一界面被算成多页） ----------
    tpl = collections.Counter(r['template'] for r in routes)
    dup_tpl = {t: c for t, c in tpl.items() if c > 1}
    findings['4_重复模板'] = {
        '被多个state共用的模板数': len(dup_tpl),
        '总重复state数': sum(c - 1 for c in dup_tpl.values()),
        '明细': [{'template': t, 'states': [x['state'] for x in routes if x['template'] == t]}
                 for t in sorted(dup_tpl)],
    }

    # ---------- 5. 目录归属 vs 路由前缀 ----------
    dir_mismatch = []
    for r in routes:
        p = r['template'].split('/')
        d = p[1] if len(p) >= 3 else '(root)'
        prefix = r['state'].split('.')[0]
        if d != '(root)' and prefix != d and d != 'home':
            dir_mismatch.append({'state': r['state'], 'dir': d, 'prefix': prefix})
    findings['5_目录与路由前缀不一致'] = {
        '数量': len(dir_mismatch),
        '样例': dir_mismatch[:25],
        '说明': '这些 state 的模板在 A 目录，但 state 前缀是 B；复刻时模块归属需明确以哪个为准',
    }

    # ---------- 6. 中文名缺失 ----------
    no_cn = [b['file'] for b in books
             if (b['cnName'] or '').strip() in ('', '【待确认】', '待确认')]
    findings['6_模块中文名'] = {
        '仍为【待确认】的模块数': len(no_cn),
        '模块总数': len(books),
        '清单': no_cn,
    }

    # ---------- 7. 零端点页面 ----------
    zero_ep = [r for r in rows if r['endpoints'] == 0]
    ctrl_map = {}
    with open(API_MAP, encoding='utf-8') as f:
        am = json.load(f)
    findings['7_端点覆盖'] = {
        '分册页面行总数': len(rows),
        '零端点页面数': len(zero_ep),
        '零端点占比': round(len(zero_ep) / max(len(rows), 1), 3),
        '有端点页面数': len(rows) - len(zero_ep),
        '端点总数（去重前累加）': sum(r['endpoints'] for r in rows),
    }

    # ---------- 8. 可达性 ----------
    no_live = graph['noLiveEntry']
    nle_states = set()
    for x in no_live:
        st = [r['state'] for r in routes if r['template'] == x['template']]
        nle_states.update(st)
    in_spec_no_entry = sorted(nle_states & set(spec_states))
    findings['8_可达性'] = {
        '注释边总数': graph['totals']['commentedEdges'],
        '有效边总数': graph['totals']['liveEdges'],
        '无有效入口的state数': len(nle_states),
        '其中已登记进spec分册的': len(in_spec_no_entry),
        '样例': in_spec_no_entry[:20],
        '风险': '这些页面在生产界面上没有可点入口，却已被当作常规页面写入分册',
    }

    # ---------- 9. URL 契约 ----------
    findings['9_URL契约'] = {
        '分册记录的url形态': '子状态自身定义（ui-router state.url 原文）',
        '实际浏览器URL形态': '父url + "/" + 子url（ui-router 0.2.x 拼接）',
        '实证': 'routes.csv 记 /medicalFeesList，生产实际 #!/systemSetting/medicalFeesList',
        '影响': '分册 §1 页面清单的 url 列不能直接当作可访问 URL 使用',
        '嵌套宿主数': len(graph['nestedHostTrees']),
    }

    # ---------- 10. 路由树嵌套 ----------
    nested = {h['state']: len(h.get('children', [])) for h in graph['nestedHostTrees']}
    findings['10_嵌套层级'] = {
        '嵌套宿主': nested,
        '嵌套页面总数': graph['totals']['states'] - graph['totals']['rootStates'],
        '说明': '分册按 views 目录平铺，未表达 ui-router 父子嵌套，复刻时需补嵌套视图层',
    }

    dest = os.path.join(BASE, 'audit-report.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)

    for k, v in findings.items():
        print('\n===== %s =====' % k)
        if isinstance(v, dict):
            for kk, vv in v.items():
                s = json.dumps(vv, ensure_ascii=False)
                if len(s) > 400:
                    s = s[:400] + ' ...(+%d)' % (len(s) - 400)
                print('  %-32s %s' % (kk, s))
        else:
            print('  %s' % v)
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
