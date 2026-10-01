#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gap-audit.py
文档 vs 生产实际 差距量化审计（只读本地证据层，不联网、不写生产）
产出：re/gap-audit.json + 控制台差距矩阵
"""
import csv, json, os, re, collections

BASE = os.path.dirname(os.path.abspath(__file__))


def jload(name):
    with open(os.path.join(BASE, name), encoding='utf-8') as f:
        return json.load(f)


def load_routes():
    out = []
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().lstrip('\ufeff')
                if st.lower() == 'state':
                    continue
                out.append({'state': st, 'url': row[1].strip(),
                            'controller': row[2].strip(), 'template': row[3].strip()})
    return out


def load_endpoint_universe(pam):
    """真实端点全集来自 page-api-map.json；
    注意 re/endpoints.csv 存的是「端点 URL 长度」清单(905行=1表头+904条)，不是路径。"""
    eps = set()
    zero_ep_pages = []
    for p in pam['pages']:
        e = [x.split('?')[0] for x in (p.get('endpoints') or [])]
        e = [x for x in e if x]
        if not e:
            zero_ep_pages.append(p['template'])
        eps.update(e)
    return eps, zero_ep_pages


def main():
    routes = load_routes()
    pj = jload('pages.json')
    sf = jload('state-factory.json')['states']
    mm = jload('menu-map.json')
    graph = jload('ui-graph.json')
    inv = jload('uncovered-analysis.json')
    pmap = jload('page-api-map.json')

    pages = pj['pages']
    byTpl = {p['template']: p for p in pages}
    eps, zero_ep_pages = load_endpoint_universe(pmap)

    # ---------- A. 页面四层覆盖 ----------
    path2states = collections.defaultdict(list)
    for r in routes:
        u = r['url'].split('?')[0].lstrip('/')
        path2states[u].append(r['state'])
        path2states[u.split('/')[-1]].append(r['state'])
    perm_states = set()
    for paths in sf.values():
        for p in paths:
            perm_states.update(path2states.get(p, []))

    def tier(p):
        has_field = bool(p.get('tableColumns') or p.get('requiredLabels'))
        has_struct = bool(p.get('bindings') or p.get('actions') or p.get('labels'))
        has_url = bool(p.get('url'))
        if has_field:
            return 'L1_字段级规格(可施工)'
        if has_struct:
            return 'L2_结构级(有交互无字段表)'
        if has_url:
            return 'L3_仅路由壳(无任何元素结构)'
        return 'L4_空白'

    tiers = collections.defaultdict(list)
    for p in pages:
        tiers[tier(p)].append(p)
    tier_state = {id(p): tier(p) for p in pages}

    # ---------- B. 按模块×层级矩阵 ----------
    mod_tier = collections.defaultdict(collections.Counter)
    for p in pages:
        mod_tier[p.get('module') or '(未归属)'][tier(p)] += 1

    # ---------- C. 端点归属覆盖 ----------
    ctrl = list(csv.DictReader(open(os.path.join(BASE, 'controller-api.csv'),
                                   encoding='utf-8-sig')))
    ctrl_eps = set()
    for c in ctrl:
        for e in (c.get('Endpoints') or '').split('|'):
            e = e.strip()
            if e:
                ctrl_eps.add(e)
    ep_orphan = sorted(eps - ctrl_eps)
    ep_unmapped_ctrl = sorted(ctrl_eps - eps)

    # 端点→页面
    ep2pages = collections.defaultdict(set)
    for p in pmap['pages']:
        for e in (p.get('endpoints') or []):
            ep2pages[e.split('?')[0]].add(p['template'])
    ep_no_page = sorted(e for e in eps if e not in ep2pages)

    # ---------- D. 跳转可达性 ----------
    no_live = {x['template'] for x in graph.get('noLiveEntry', [])}
    live_tpl = [p for p in pages if p['template'] not in no_live]

    # ---------- E. 权限归属 × 字段规格 交叉（真正的施工缺口） ----------
    cross = collections.Counter()
    cross_detail = collections.defaultdict(list)
    for p in pages:
        key = (('权限内' if p.get('state') in perm_states or
                 any(p['template'] == byTpl[t]['template'] for t in [])
                else '权限外'), tier(p))
        # 用 state 直接判定
        key = (('权限内' if p.get('state') in perm_states else '权限外'), tier(p))
        cross[key] += 1
        cross_detail[key].append(p['template'])

    # ---------- F. 未覆盖路由最终定性 ----------
    buckets = {k: v['count'] for k, v in inv['buckets'].items()}

    # ---------- G. 模块级：页面数 / 端点数 / 字段覆盖数 ----------
    mod_stat = {}
    for m, c in mod_tier.items():
        lst = [p for p in pages if (p.get('module') or '(未归属)') == m]
        mod_stat[m] = {
            'pages': len(lst),
            'fieldReady': sum(1 for p in lst if tier(p) == 'L1_字段级规格(可施工)'),
            'structOnly': sum(1 for p in lst if tier(p) == 'L2_结构级(有交互无字段表)'),
            'shellOnly': sum(1 for p in lst if tier(p) == 'L3_仅路由壳(无任何元素结构)'),
            'blank': sum(1 for p in lst if tier(p) == 'L4_空白'),
            'templates': sorted(x['template'] for x in lst)[:400],
        }
        mod_stat[m]['fieldPct'] = round(mod_stat[m]['fieldReady'] / max(1, len(lst)), 3)

    out = {
        'generatedBy': 're/gap-audit.py',
        'inputs': {
            'routes': len(routes), 'pages': len(pages), 'endpoints': len(eps),
            'controllers': len(ctrl), 'permissionStates': len(perm_states),
            'stateFactoryEntries': len(sf),
            'endpointsDeclared': pmap['endpointTotal'],
        },
        'A_页面覆盖四层': {k: len(v) for k, v in sorted(tiers.items())},
        'A_detail': {k: sorted(p['template'] for p in v) for k, v in sorted(tiers.items())},
        'B_模块层级矩阵': {m: dict(c) for m, c in sorted(mod_tier.items())},
        'C_端点归属': {
            'endpointsTotal': len(eps),
            'boundToController': len(eps) - len(ep_orphan),
            'orphanNoController': len(ep_orphan),
            'orphanSample': ep_orphan[:40],
            'controllerEpNotInPageMap': len(ep_unmapped_ctrl),
            'controllerEpNotInPageMapSample': ep_unmapped_ctrl[:30],
            'zeroEndpointPages': len(zero_ep_pages),
            'zeroEndpointPageSample': sorted(zero_ep_pages)[:40],
        },
        'D_跳转可达性': {
            'pagesTotal': len(pages),
            'withLiveEntry': len(live_tpl),
            'noLiveEntry': len(no_live),
        },
        'E_权限x字段交叉': {'%s|%s' % k: v for k, v in sorted(cross.items())},
        'F_未覆盖路由分桶': buckets,
        'G_模块统计': {m: {k: v for k, v in d.items() if k != 'templates'}
                       for m, d in sorted(mod_stat.items())},
        'G_字段覆盖最差模块': sorted(
            [(m, d['fieldPct'], d['pages']) for m, d in mod_stat.items()],
            key=lambda x: (x[1], -x[2]))[:15],
    }
    dest = os.path.join(BASE, 'gap-audit.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # ---------- 控制台 ----------
    I = out['inputs']
    print('== 输入规模 ==')
    print('  路由 %d / 页面 %d / 端点 %d / 控制器 %d / 权限state %d'
          % (I['routes'], I['pages'], I['endpoints'], I['controllers'], I['permissionStates']))
    print('\n== A. 页面四层覆盖 ==')
    for k, v in sorted(out['A_页面覆盖四层'].items(), key=lambda x: -x[1]):
        print('  %-30s %4d  (%.1f%%)' % (k, v, 100.0 * v / len(pages)))
    print('\n== C. 端点归属 ==')
    C = out['C_端点归属']
    print('  端点去重后 %d (page-api-map 声明 %d)'
          % (C['endpointsTotal'], I['endpointsDeclared']))
    print('  已归属控制器 %d (%.1f%%)  无控制器归属 %d'
          % (C['boundToController'],
             100.0 * C['boundToController'] / max(1, C['endpointsTotal']),
             C['orphanNoController']))
    print('  控制器表里但页面映射没有的端点 %d' % C['controllerEpNotInPageMap'])
    print('  零端点页面 %d (%.1f%%)  <-- 文档未登记任何后端接口的界面'
          % (C['zeroEndpointPages'], 100.0 * C['zeroEndpointPages'] / len(pages)))
    print('\n== E. 权限 x 字段 交叉 ==')
    for k, v in sorted(out['E_权限x字段交叉'].items()):
        print('  %-34s %4d' % (k, v))
    print('\n== G. 字段覆盖最差模块 (pct, pages) ==')
    for m, pct, n in out['G_字段覆盖最差模块']:
        print('  %-22s %.0f%%  (%d 页)' % (m, pct * 100, n))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
