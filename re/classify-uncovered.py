#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/classify-uncovered.py
对「未被任何权限 state 覆盖」的路由逐个定性：
  二级/三级界面 / 链式未挂载 / 独立未挂载 / 死路由候选
只读本地证据层。
"""
import csv, json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))


def load_routes():
    out = []
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().strip('﻿')
                if st.lower() == 'state':
                    continue
                out.append({'state': st, 'url': row[1].strip(),
                            'controller': row[2].strip(), 'template': row[3].strip()})
    return out


def main():
    routes = load_routes()
    states = {r['state'] for r in routes}
    rmap = {r['state']: r for r in routes}

    with open(os.path.join(BASE, 'menu-map.json'), encoding='utf-8') as f:
        mm = json.load(f)
    with open(os.path.join(BASE, 'state-factory.json'), encoding='utf-8') as f:
        sf = json.load(f)['states']
    with open(os.path.join(BASE, 'ui-graph.json'), encoding='utf-8') as f:
        graph = json.load(f)
    with open(os.path.join(BASE, 'pages.json'), encoding='utf-8') as f:
        pj = json.load(f)
    pmap = {}
    for p in pj['pages']:
        pmap.setdefault(p['template'], p)

    # 权限覆盖：stateFactory 路径 -> 路由
    path2states = collections.defaultdict(list)
    for r in routes:
        u = r['url'].split('?')[0]
        path2states[u.lstrip('/')].append(r['state'])
        path2states[u.lstrip('/').split('/')[-1]].append(r['state'])

    covered = set()
    for paths in sf.values():
        for p in paths:
            for st in path2states.get(p, []):
                covered.add(st)

    # 父子关系
    parent_of = {}
    for r in routes:
        parts = r['state'].split('.')
        par = None
        for i in range(len(parts) - 1, 0, -1):
            cand = '.'.join(parts[:i])
            if cand in states:
                par = cand
                break
        parent_of[r['state']] = par

    # 有效 ui-sref 入边
    inbound = collections.defaultdict(list)
    for h in graph['nestedHostTrees']:
        pass
    # ui-graph 的 noLiveEntry 只给"无有效入口"，这里从原始边重建
    # 简化：读 ui-graph 的 edges 未落盘，改用 noLiveEntry 判定
    no_live = {x['template'] for x in graph['noLiveEntry']}

    uncovered = [r for r in routes if r['state'] not in covered]

    buckets = collections.defaultdict(list)
    for r in uncovered:
        st = r['state']
        par = parent_of.get(st)
        p = pmap.get(r['template'], {})
        has_ep = bool(p.get('tableColumns') or p.get('bindings') or p.get('actions'))
        is_list = bool(p.get('tableColumns'))
        depth = st.count('.')
        if par and par in covered:
            k = 'A_权限点的二级界面'
        elif par and par not in covered:
            k = 'B_链式未挂载(父也未覆盖)'
        elif depth > 0:
            k = 'B_链式未挂载(父也未覆盖)'
        else:
            k = 'C_独立未挂载'
        if not has_ep:
            k += '_无结构特征'
        buckets[k].append({
            'state': st, 'url': r['url'], 'template': r['template'],
            'controller': r['controller'], 'parent': par,
            'isList': is_list,
            'hasUiSrefOnlyCommented': r['template'] in no_live,
        })

    out = {
        'total': len(uncovered),
        'coveredByPermissions': len(covered),
        'buckets': {k: {'count': len(v), 'items': v} for k, v in sorted(buckets.items())},
    }
    dest = os.path.join(BASE, 'uncovered-analysis.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('未覆盖路由总数: %d  (已覆盖 %d / 共 %d)' % (len(uncovered), len(covered), len(routes)))
    print('\n%-38s %6s' % ('分类', '数量'))
    print('-' * 46)
    for k, v in sorted(buckets.items()):
        print('%-38s %6d' % (k, len(v)))
    print('\n-- 各分类模板目录分布 top --')
    for k, v in sorted(buckets.items()):
        c = collections.Counter(x['template'].split('/')[1] if len(x['template'].split('/')) > 2
                                 else '(root)' for x in v)
        print('  %s' % k)
        print('     %s' % ', '.join('%s:%d' % (d, n) for d, n in c.most_common(8)))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
