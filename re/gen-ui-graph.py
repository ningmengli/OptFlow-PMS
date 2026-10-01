#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gen-ui-graph.py
全量界面跳转图 + 可达性分析
- 扫描 re 缓存的全部 views/**/*.html 模板
- 提取 ui-sref / ui-sref-append 跳转边
- 行级 HTML 注释状态机：标记「被注释 = 界面上无入口」
- 合并 routes.csv 的 ui-router 父子嵌套关系
- 输出模块 -> 子菜单 -> 页面 -> 子界面 的完整树
只读本地缓存，不触网。
"""
import csv, json, os, re, collections

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'sgzj-re')
PAGES = os.path.join(CACHE, 'pages')
ROUTES = os.path.join(BASE, 'routes.csv')

UI_SREF = re.compile(r'ui-sref(?:-append)?\s*=\s*["\']([A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*)')
COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
# 提取 sref 之后最近的锚/按钮/span 文本作为中文名
TEXT_AFTER = re.compile(r'>\s*([^<>{}]{1,20}?)\s*<')
STATE_ONLY = re.compile(r'^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*$')


def strip_state_params(s):
    """ui-sref="state({a:1})" -> state"""
    i = s.find('(')
    return s[:i] if i > 0 else s


def scan_templates():
    edges = []          # (srcTemplate, targetState, label, commented)
    if not os.path.isdir(PAGES):
        raise SystemExit('cache not found: %s' % PAGES)
    n_files = 0
    scanned = set()
    for root, _dirs, files in os.walk(PAGES):
        for fn in files:
            if not fn.endswith('.html'):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, PAGES).replace('\\', '/')
            n_files += 1
            scanned.add(rel)
            with open(fp, encoding='utf-8', errors='replace') as f:
                text = f.read()
            # 先剥离全部 HTML 注释块（字符区间级，不用行级状态机）
            comments = []

            def _repl(m):
                comments.append(m.group(0))
                return '\n' * m.group(0).count('\n')

            clean = COMMENT.sub(_repl, text)
            # 有效边
            for m in UI_SREF.finditer(clean):
                st = strip_state_params(m.group(1))
                if not STATE_ONLY.match(st):
                    continue
                t = TEXT_AFTER.search(clean[m.end():])
                edges.append({'from': rel, 'to': st,
                              'label': t.group(1).strip() if t else '',
                              'commented': False})
            # 注释内的边
            for blk in comments:
                for m in UI_SREF.finditer(blk):
                    st = strip_state_params(m.group(1))
                    if not STATE_ONLY.match(st):
                        continue
                    t = TEXT_AFTER.search(blk[m.end():])
                    edges.append({'from': rel, 'to': st,
                                  'label': t.group(1).strip() if t else '',
                                  'commented': True})
    return edges, n_files, scanned


def load_routes():
    out = []
    with open(ROUTES, encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().strip('﻿')
                if st.lower() == 'state':      # 跳过表头
                    continue
                out.append({
                    'state': st,
                    'url': row[1].strip(),
                    'controller': row[2].strip(),
                    'template': row[3].strip(),
                })
    return out


def module_of(template):
    p = template.split('/')
    return p[1] if len(p) >= 3 and p[0] == 'views' else '(root)'


def main():
    edges, n_files, scanned = scan_templates()
    routes = load_routes()
    states = {r['state'] for r in routes}
    rmap = {r['state']: r for r in routes}

    # 缓存中缺失的路由模板
    missing = sorted(
        r['template'] for r in routes
        if r['template'].startswith('views/') and r['template'] not in scanned
    )

    # 父状态
    parent_of = {}
    for r in routes:
        parts = r['state'].split('.')
        parent = None
        for i in range(len(parts) - 1, 0, -1):
            cand = '.'.join(parts[:i])
            if cand in states:
                parent = cand
                break
        parent_of[r['state']] = parent

    # 入边统计：谁被指向（= 界面入口）
    inbound = collections.defaultdict(list)
    for e in edges:
        inbound[e['to']].append(e)

    # 界面树（按 state 父子）
    def subtree(st, depth=0, maxd=3):
        node = {
            'state': st,
            'url': rmap[st]['url'] if st in rmap else '',
            'template': rmap[st]['template'] if st in rmap else '',
            'label': '',
            'depth': depth,
            'inboundMenus': [],
            'children': [],
        }
        for e in inbound.get(st, []):
            if not e['commented'] and e['label']:
                node['inboundMenus'].append({'from': e['from'], 'label': e['label']})
        if depth < maxd:
            for c in sorted(s for s in states if parent_of.get(s) == st):
                node['children'].append(subtree(c, depth + 1, maxd))
        return node

    hosts = sorted(
        [s for s in states
         if any(parent_of.get(x) == s for x in states)],
        key=lambda s: -sum(1 for x in states if parent_of.get(x) == s)
    )

    # 可达性：没有任何非注释入边，且不是根 => 疑似无入口
    roots = [s for s in states if parent_of.get(s) is None]
    no_entry = []
    for s in states:
        if parent_of.get(s) is None:
            continue
        live = [e for e in inbound.get(s, []) if not e['commented']]
        dead = [e for e in inbound.get(s, []) if e['commented']]
        if not live and dead:
            no_entry.append({'state': s, 'template': rmap[s]['template'],
                             'onlyCommented': len(dead)})

    modules = collections.defaultdict(lambda: {
        'module': '', 'states': [], 'hosts': []})
    for r in routes:
        m = module_of(r['template'])
        modules[m]['module'] = m
        modules[m]['states'].append(r['state'])
    for h in hosts:
        m = module_of(rmap[h]['template'])
        if m in modules:
            modules[m]['hosts'].append(h)

    out = {
        'generatedBy': 're/gen-ui-graph.py',
        'totals': {
            'templatesScanned': n_files,
            'jumpEdges': len(edges),
            'liveEdges': sum(1 for e in edges if not e['commented']),
            'commentedEdges': sum(1 for e in edges if e['commented']),
            'states': len(states),
            'rootStates': len(roots),
            'nestedHosts': len(hosts),
            'statesWithNoLiveEntry': len(no_entry),
            'missingTemplates': len(missing),
        },
        'missingTemplates': missing,
        'modules': [
            {
                'module': m,
                'stateCount': len(v['states']),
                'nestedHosts': sorted(v['hosts']),
            }
            for m, v in sorted(modules.items(), key=lambda kv: -len(kv[1]['states']))
        ],
        'nestedHostTrees': [subtree(h) for h in hosts],
        'noLiveEntry': sorted(no_entry, key=lambda x: x['template']),
    }
    dest = os.path.join(BASE, 'ui-graph.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    t = out['totals']
    print('== TOTALS ==')
    for k, v in t.items():
        print('  %-26s %s' % (k, v))
    print('\n== NESTED HOSTS (二级界面宿主) ==')
    for h in hosts:
        kids = [x for x in states if parent_of.get(x) == h]
        gk = [x for x in kids if any(parent_of.get(y) == x for y in states)]
        print('  %-34s children=%-4d grandchildren=%d' % (h, len(kids), len(gk)))
    print('\n== NO LIVE ENTRY (仅被注释引用 = 界面无入口) %d ==' % len(no_entry))
    for x in no_entry[:40]:
        print('  %-46s commentedRefs=%d' % (x['template'], x['onlyCommented']))
    if len(no_entry) > 40:
        print('  ... +%d more' % (len(no_entry) - 40))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
