#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/extract-g07.py
闭合 G-07「命令式跳转全量不可见」：
从 %TEMP%/sgzj-re 的 6 个前端 bundle 中全量提取 $state.go / $location.path 等
命令式跳转目标，与 485 路由做匹配，标注哪些命令式边是静态扫描看不到的。
只读本地缓存，不联网、不带任何凭据。
"""
import os, re, json, csv, collections, glob

BUNDLE_DIR = os.path.join(os.environ.get('TEMP', '/tmp'), 'sgzj-re')
BASE = os.path.dirname(os.path.abspath(__file__))

# 跳转构造形式
PATTERNS = [
    ('$state.go', re.compile(r'\$state\.go\(\s*[\'"]([^\'"]+)[\'"]')),
    ('$state.go var', re.compile(r'\$state\.go\(\s*([A-Za-z_$][\w$]*)')),
    ('$location.path', re.compile(r'\$location\.(?:path|search|hash|url)\(\s*[\'"]([^\'"]+)[\'"]')),
    ('location.hash', re.compile(r'location\.hash\s*=\s*[\'"]([^\'"]+)[\'"]')),
    ('gotoState', re.compile(r'gotoState\(\s*[\'"]([^\'"]+)[\'"]')),
    ('goState', re.compile(r'(?<!\w)goState\(\s*[\'"]([^\'"]+)[\'"]')),
    ('$state.go obj', re.compile(r'\$state\.go\(\s*[^,]+,\s*\{\s*[\'"]?(\w+)')),
]


def load_routes():
    out = {}
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().lstrip('\ufeff')
                if st.lower() != 'state':
                    out[st] = {'url': row[1].strip(), 'template': row[3].strip()}
    return out


def main():
    routes = load_routes()
    states = set(routes)
    urls = {r['url'].split('?')[0].lstrip('/') for r in routes.values()}

    files = sorted(glob.glob(os.path.join(BUNDLE_DIR, '*.js')))
    if not files:
        print('BUNDLE CACHE MISSING: %s' % BUNDLE_DIR)
        return

    edges = []          # 命令式边
    unresolved = []     # 变量式跳转
    per_file = {}

    for fp in files:
        name = os.path.basename(fp)
        with open(fp, encoding='utf-8', errors='replace') as f:
            src = f.read()
        cnt = 0
        for label, pat in PATTERNS:
            for m in pat.finditer(src):
                tgt = m.group(1).strip()
                if not tgt:
                    continue
                line = src.count('\n', 0, m.start()) + 1
                # 归一化 target
                t_state, t_url, kind = None, None, 'unresolved'
                if tgt in states:
                    t_state, kind = tgt, 'state'
                elif tgt.lstrip('/') in urls or tgt.lstrip('#!').lstrip('/') in urls:
                    t_url = tgt.lstrip('#!').lstrip('/')
                    kind = 'url'
                else:
                    t = tgt.lstrip('#!/')
                    if t in states:
                        t_state, kind = t, 'state(hash)'
                    elif t in urls:
                        t_url, kind = t, 'url(hash)'
                if label.endswith('var'):
                    unresolved.append({'file': name, 'line': line, 'raw': tgt,
                                      'var': True, 'source': label})
                    continue
                edges.append({'kind': kind, 'label': label, 'file': name,
                              'line': line, 'raw': tgt, 'targetState': t_state,
                              'targetUrl': t_url})
                cnt += 1
        per_file[name] = cnt

    resolved = [e for e in edges if e['kind'] != 'unresolved']
    by_label = collections.Counter(e['label'] for e in edges)
    by_kind = collections.Counter(e['kind'] for e in edges)

    # 命令式可达但静态 ui-sref 扫不到的 state
    covered_states = {e['targetState'] for e in resolved if e['targetState']}
    covered_urls = {e['targetUrl'] for e in resolved if e['targetUrl']}

    # 权限树覆盖（re/state-factory.json）
    with open(os.path.join(BASE, 'state-factory.json'), encoding='utf-8') as f:
        sf = json.load(f)['states']
    path2states = collections.defaultdict(list)
    for st, r in routes.items():
        u = r['url'].split('?')[0].lstrip('/')
        path2states[u].append(st)
        path2states[u.split('/')[-1]].append(st)
    perm_states = set()
    for paths in sf.values():
        for p in paths:
            perm_states.update(path2states.get(p, []))

    cmd_only = sorted(covered_states - perm_states)
    cmd_only_urls = sorted(u for u in covered_urls if u not in
                           {x for st in perm_states for x in path2states.get(u, [])})

    out = {
        'bundleDir': BUNDLE_DIR,
        'files': {os.path.basename(p): os.path.getsize(p) for p in files},
        'perFileEdgeCount': per_file,
        'totalEdges': len(edges),
        'resolvedEdges': len(resolved),
        'unresolvedVarEdges': len(unresolved),
        'byLabel': dict(by_label),
        'byKind': dict(by_kind),
        'distinctTargetStates': sorted(covered_states),
        'distinctTargetUrls': sorted(covered_urls),
        'commandStyleStatesOutsidePermissionTree': cmd_only,
        'commandStyleUrlsOutsidePermissionTree': cmd_only_urls,
        'unresolvedSamples': unresolved[:60],
    }
    dest = os.path.join(BASE, 'command-jumps.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('== G-07 命令式跳转全量提取 ==')
    print('bundle 目录: %s' % BUNDLE_DIR)
    for k, v in sorted(per_file.items()):
        print('  %-16s %5d 处' % (k, v))
    print('  合计边 %d (可解析 %d / 变量式待定 %d)' % (len(edges), len(resolved), len(unresolved)))
    print('\n-- 按构造形式 --')
    for k, v in by_label.most_common():
        print('  %-22s %4d' % (k, v))
    print('\n-- 按目标类型 --')
    for k, v in by_kind.most_common():
        print('  %-22s %4d' % (k, v))
    print('\n命令式可达 state 去重 %d 个' % len(covered_states))
    print('其中「不在权限树内」的 %d 个:' % len(cmd_only))
    for s in cmd_only[:40]:
        print('   -', s)
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
