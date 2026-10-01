#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/final-classify.py
终局定性：
  1) 197 未覆盖路由 -> 合并 G-07 命令式可达 -> 剩余逐个归入 7 类
  2) 162 零端点页面 -> 按模块与形态归类（纯前端壳 / 静态展示 / 抽取失败）
只读本地证据层。
"""
import json, os, csv, collections

BASE = os.path.dirname(os.path.abspath(__file__))


def jload(n):
    with open(os.path.join(BASE, n), encoding='utf-8') as f:
        return json.load(f)


def load_routes():
    out = {}
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip():
                st = row[0].strip().lstrip('\ufeff')
                if st.lower() != 'state':
                    out[st] = {'url': row[1].strip(), 'template': row[3].strip()}
    return out


# ---- 定性规则：先匹配先生效 ----
RULES = [
    ('F1_微信授权回调页',
     lambda s, u, t, d: 'wechatAuth' in s or 'wechatAuth' in u),
    ('F2_介绍/说明/测试落地页',
     lambda s, u, t, d: s in ('aioIntroduce', 'coinRuleIntroduce', 'testPage')),
    ('F3_大屏/喊叫器/工作台(免登录工作区)',
     lambda s, u, t, d: s in ('bigScreen', 'adminCall', 'checkCall',
                              'consultingScreen', 'doctorWorkbench',
                              'workBeach', 'projectionScreen', 'pos')),
    ('F4_硬件对接(蓝牙/检测仪/云打印/投屏配置)',
     lambda s, u, t, d: s in ('blueToothTransfer', 'detectionLog',
                              'cloudPrinterList', 'screenUrlConfig')),
    ('F5_报表 Tab 子页(已在 R6 Tab 机制内)',
     lambda s, u, t, d: s.startswith('report.') or d == 'reportMedical'),
    ('F6_系统设置二级界面(R6 硬编码 36 项内)',
     lambda s, u, t, d: s.startswith('systemSetting') or d == 'systemSetting'),
    ('F7_详情/编辑/变更页(必须带 id 入参,无独立入口)',
     lambda s, u, t, d: ('?' in u) or s.split('.')[-1] in (
         'Detail', 'Modify', 'Change', 'List', 'Edit', 'Check', 'recordDetail')),
    ('F8_独立业务页(权限树未收录,需裁决归属)',
     lambda s, u, t, d: True),
]


def main():
    routes = load_routes()
    inv = jload('uncovered-analysis.json')
    cmd = set(jload('command-jumps.json')['distinctTargetStates'])
    pmap = jload('page-api-map.json')
    pagesj = jload('pages.json')
    bytes_of = {p['template']: (p.get('bytes') or 0) for p in pagesj['pages']}

    # ---------- 1. 197 终局定性 ----------
    final = collections.defaultdict(list)
    resolved_by_cmd = []
    for k, v in inv['buckets'].items():
        for it in v['items']:
            st = it['state']
            d = it['template'].split('/')[1] if len(it['template'].split('/')) > 2 else '(root)'
            if st in cmd:
                resolved_by_cmd.append(it)
                final['G0_命令式可达(R6 静态扫描盲区)'].append(it)
                continue
            for name, fn in RULES:
                if fn(st, it['url'], it['template'], d):
                    final[name].append(it)
                    break

    # ---------- 2. 零端点页面定性 ----------
    # 注意：必须遍历 pmap['pages'] 全量，不能按 template 去重
    # （36 个模板被多 state 共用，去重会丢记录）
    zero = [p for p in pmap['pages'] if not (p.get('endpoints') or [])]
    zc = collections.defaultdict(list)
    for p in zero:
        st = p.get('state', '')
        d = p.get('module') or '(未归属)'
        nbytes = bytes_of.get(p['template'], 0)
        if nbytes < 1200:
            zc['Z1_模板近乎空壳(<1.2KB)'].append(p['template'])
        elif st.startswith('report.') or d == 'reportMedical':
            zc['Z2_报表 Tab 页(数据由父页注入)'].append(p['template'])
        elif st.startswith('systemSetting') or d == 'systemSetting':
            zc['Z3_系统设置二阶页(配置项为主)'].append(p['template'])
        else:
            zc['Z4_有结构但未挂端点(疑似抽取失败)'].append(p['template'])

    zmod = collections.Counter(p.get('module') or '(未归属)' for p in zero)

    out = {
        'generatedBy': 're/final-classify.py',
        '197_终局定性': {k: {'count': len(v), 'items': v} for k, v in sorted(final.items())},
        '162_零端点定性': {k: {'count': len(v), 'items': sorted(v)}
                           for k, v in sorted(zc.items())},
        '零端点_按模块': dict(zmod.most_common()),
    }
    dest = os.path.join(BASE, 'final-classify.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('== 197 未覆盖路由 终局定性 ==')
    tot = 0
    for k, v in sorted(final.items(), key=lambda x: -len(x[1])):
        print('  %-44s %4d' % (k, len(v)))
        tot += len(v)
    print('  %-44s %4d' % ('合计', tot))
    print('\n== 162 零端点页面 终局定性 ==')
    zt = 0
    for k, v in sorted(zc.items(), key=lambda x: -len(x[1])):
        print('  %-44s %4d' % (k, len(v)))
        zt += len(v)
    print('  %-44s %4d' % ('合计', zt))
    print('\n-- 零端点页面 Top 模块 --')
    for m, n in zmod.most_common(12):
        print('  %-22s %3d' % (m, n))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
