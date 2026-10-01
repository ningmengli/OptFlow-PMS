#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/extract-statefactory.py
从生产 bundle 提取 stateFactory：权限 state -> 界面路径清单
这是 G-01（108 个权限点的真实 state 值）的权威来源之一。
只读本地缓存。
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), 'sgzj-re')
FACTORY = os.path.join(CACHE, 'factory.js')

# 抓 constant("stateFactory", { ... });
START = re.compile(r'constant\(\s*["\']stateFactory["\']\s*,\s*\{')
# key: [ "a", "b", ... ]  （可跨行）
KV = re.compile(r'([A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*\[(.*?)\]', re.DOTALL)
STR = re.compile(r'["\']([^"\']*)["\']')


def main():
    if not os.path.isfile(FACTORY):
        raise SystemExit('factory.js not found: %s' % FACTORY)
    with open(FACTORY, encoding='utf-8', errors='replace') as f:
        text = f.read()

    m = START.search(text)
    if not m:
        raise SystemExit('stateFactory not found in factory.js')
    start = m.end()

    # 粗略取到下一个 "\n});" 为止
    end = text.find('\n});', start)
    block = text[start:end if end > 0 else len(text)]

    # 去掉行注释，避免把注释掉的 key 抓进来
    block = re.sub(r'//[^\n]*', '', block)

    table = {}
    for km in KV.finditer(block):
        key = km.group(1)
        arr = STR.findall(km.group(2))
        if arr:
            table[key] = arr

    total_paths = sum(len(v) for v in table.values())

    out = {
        'source': 'production bundle factory.js (constant "stateFactory")',
        'purpose': '权限 state -> 该权限覆盖的界面路径清单（主导航 isOldActive 高亮判定用）',
        'stateCount': len(table),
        'pathCount': total_paths,
        'states': table,
    }
    dest = os.path.join(BASE, 'state-factory.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('stateFactory entries : %d' % len(table))
    print('total path values    : %d' % total_paths)
    print('\n-- 前 40 个权限 state --')
    for i, (k, v) in enumerate(list(table.items())[:40]):
        print('  %-28s %2d  %s' % (k, len(v), ', '.join(v[:4]) + (' ...' if len(v) > 4 else '')))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
