#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/verify-orphan-controllers.py
核实「零端点页面引用的控制器不在 287 控制器清单内」是否属实，
并统计这些控制器实际带出多少未登记端点 → 判定 904 是否被低估。
只读本地缓存。
"""
import os, re, json, csv, collections

BUNDLE_DIR = os.path.join(os.environ.get('TEMP', '/tmp'), 'sgzj-re')
BASE = os.path.dirname(os.path.abspath(__file__))
EP_RE = re.compile(r'["\'](/[A-Za-z0-9_/\.]+\.json)["\']')


def main():
    fc = json.load(open(os.path.join(BASE, 'final-classify.json'), encoding='utf-8'))
    z4 = fc['162_零端点定性']['Z4_有结构但未挂端点(疑似抽取失败)']['items']
    z4set = set(z4)

    pam = {p['template']: p
           for p in json.load(open(os.path.join(BASE, 'page-api-map.json'),
                                   encoding='utf-8'))['pages']}
    ctrl = {c['Controller']: c
            for c in csv.DictReader(open(os.path.join(BASE, 'controller-api.csv'),
                                         encoding='utf-8-sig'))}
    known_ep = set()
    for c in ctrl.values():
        for e in (c.get('Endpoints') or '').split('|'):
            if e.strip():
                known_ep.add(e.strip())

    # 孤儿控制器 = 零端点页面引用、但不在 287 表内
    orphan_ctrl = collections.defaultdict(set)
    for t in z4set:
        c = pam.get(t, {}).get('controller')
        if c and c not in ctrl:
            orphan_ctrl[c].add(t)

    src = ''
    for fn in ('controller.js', 'directive.js', 'service.js', 'factory.js', 'property.js'):
        fp = os.path.join(BUNDLE_DIR, fn)
        if os.path.exists(fp):
            src += open(fp, encoding='utf-8', errors='replace').read()

    found, missing, new_eps, per_ctrl = 0, [], set(), {}
    for c, tpls in sorted(orphan_ctrl.items()):
        # 控制器定义点：取最后一次出现（routes 里是字符串引用，定义在后面）
        hits = list(re.finditer(r'\b' + re.escape(c) + r'\b', src))
        if not hits:
            missing.append(c)
            continue
        m = hits[-1]
        # 控制器函数体：从定义点向后取 20KB
        seg = src[m.start():m.start() + 20000]
        eps = {e for e in EP_RE.findall(seg) if e not in known_ep}
        found += 1
        per_ctrl[c] = {'templates': sorted(tpls), 'occurrences': len(hits),
                       'newEndpoints': sorted(eps)}
        new_eps |= eps

    out = {
        'orphanControllers': len(orphan_ctrl),
        'foundInBundle': found,
        'notFoundInBundle': missing,
        'newUnregisteredEndpoints': len(new_eps),
        'newEndpointList': sorted(new_eps),
        'perController': per_ctrl,
    }
    dest = os.path.join(BASE, 'orphan-controllers.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('== 零端点页面引用的孤儿控制器 ==')
    print('  孤儿控制器数           : %d' % len(orphan_ctrl))
    print('  在 bundle 中找到定义   : %d' % found)
    print('  bundle 中也找不到      : %d  %s' % (len(missing), missing[:8]))
    print('  这些控制器带出的未登记端点: %d' % len(new_eps))
    print('\n-- 端点数最多的 12 个孤儿控制器 --')
    rank = sorted(per_ctrl.items(), key=lambda x: -len(x[1]['newEndpoints']))
    for c, d in rank[:12]:
        print('  %-28s %3d 端点  (%d 个模板)'
              % (c, len(d['newEndpoints']), len(d['templates'])))
    print('\n-- 未登记端点样例 --')
    for e in sorted(new_eps)[:25]:
        print('   ', e)
    print('\n结论：已登记端点 904，本轮新增未登记 %d，真实端点规模约 %d~%d'
          % (len(new_eps), 904, 904 + len(new_eps)))
    print('Wrote: %s' % dest)


if __name__ == '__main__':
    main()
