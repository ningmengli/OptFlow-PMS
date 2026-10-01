#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gen-ui-inventory.py
全量界面清点：模块 x 子菜单 x 页面 三维测绘 + 父子路由树 + 二级界面识别
只读本地证据层，不触网。
"""
import csv, json, os, collections, sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROUTES = os.path.join(BASE, 'routes.csv')
PAGES = os.path.join(BASE, 'pages.json')

def load_routes():
    out = []
    with open(ROUTES, encoding='utf-8') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                out.append({
                    'state': row[0].strip(),
                    'url': row[1].strip(),
                    'controller': row[2].strip(),
                    'template': row[3].strip(),
                })
    return out

def load_pages():
    with open(PAGES, encoding='utf-8') as f:
        return json.load(f)

def module_of(template):
    # views/<module>/<file>.html
    parts = template.split('/')
    if len(parts) >= 3 and parts[0] == 'views':
        return parts[1]
    return '(root)'

def is_dead(state, url):
    return url == '' or url == '/'

def main():
    routes = load_routes()
    pages = load_pages()
    pmap = {p['state']: p for p in pages['pages']}

    # ---- 父子关系：state 形如 a.b.c，父为最长前缀且存在的祖先 ----
    states = {r['state'] for r in routes}
    parent_of = {}
    children_of = collections.defaultdict(list)
    for r in routes:
        parts = r['state'].split('.')
        parent = None
        for i in range(len(parts) - 1, 0, -1):
            cand = '.'.join(parts[:i])
            if cand in states:
                parent = cand
                break
        parent_of[r['state']] = parent
        if parent:
            children_of[parent].append(r['state'])

    # ---- 模块聚合 ----
    mods = collections.defaultdict(lambda: {
        'module': '', 'pages': [], 'roots': set(), 'nested': 0, 'dead': 0,
    })
    for r in routes:
        m = module_of(r['template'])
        e = mods[m]
        e['module'] = m
        e['pages'].append(r)
        if parent_of[r['state']] is None:
            e['roots'].add(r['state'])
        else:
            e['nested'] += 1
        if is_dead(r['state'], r['url']):
            e['dead'] += 1

    # ---- 汇总 ----
    summary = []
    for m, e in sorted(mods.items(), key=lambda kv: -len(kv[1]['pages'])):
        summary.append({
            'module': m,
            'pageCount': len(e['pages']),
            'rootMenus': len(e['roots']),
            'nestedPages': e['nested'],
            'deadRoutes': e['dead'],
        })

    # ---- 有子页面的"父界面" = 二级界面宿主 ----
    hosts = []
    for st, kids in children_of.items():
        hosts.append({
            'hostState': st,
            'childCount': len(kids),
            'children': sorted(kids),
        })
    hosts.sort(key=lambda x: -x['childCount'])

    out = {
        'generatedBy': 're/gen-ui-inventory.py',
        'source': {
            'routes': 're/routes.csv',
            'pages': 're/pages.json',
        },
        'totals': {
            'routes': len(routes),
            'pageTemplates': pages.get('pageCount'),
            'failedTemplates': pages.get('failed'),
            'modules': len(summary),
            'rootMenus': sum(s['rootMenus'] for s in summary),
            'nestedPages': sum(s['nestedPages'] for s in summary),
            'deadRoutes': sum(s['deadRoutes'] for s in summary),
            'hostsWithChildren': len(hosts),
        },
        'moduleSummary': summary,
        'nestedHosts': hosts,
    }
    dest = os.path.join(BASE, 'ui-inventory.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # ---- 控制台摘要 ----
    t = out['totals']
    print('== TOTALS ==')
    for k, v in t.items():
        print('  %-22s %s' % (k, v))
    print('\n== MODULES (%d) ==' % len(summary))
    print('  %-26s %6s %6s %6s %5s' % ('module', 'pages', 'roots', 'nested', 'dead'))
    for s in summary:
        print('  %-26s %6d %6d %6d %5d' % (
            s['module'], s['pageCount'], s['rootMenus'], s['nestedPages'], s['deadRoutes']))
    print('\n== TOP NESTED HOSTS (二级界面宿主) ==')
    for h in hosts[:25]:
        print('  %-40s -> %d children' % (h['hostState'], h['childCount']))
    print('\nWrote: %s' % dest)

if __name__ == '__main__':
    main()
