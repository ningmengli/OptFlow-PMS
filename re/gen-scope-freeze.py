#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gen-scope-freeze.py
把 5 项裁决落成 485 路由的施工范围冻结表。
裁决（老板 2026-10-01 拍板）：
  A 12 死路由            -> 不建
  B 大屏/工作台 8 建；硬件对接 4 -> Phase 2
  C F8 独立业务页 29     -> 建，本期不补权限点（挂最近父菜单）
  D 38 未知 state        -> 自定编码【OptFlow设计】
  E W0                   -> 与线 A 并行开工
只读本地证据层。
"""
import csv, json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))

# 生产侧 12 个死路由：模板 HTTP 404 / 0 字节
# 注意：state 名并非 orderAdmin.xxx / reportMedical.xxx 形式，
#       实际是 addOrder / materialStatistic.myJxcRecord 这类，必须按模板路径锁定
DEAD_TEMPLATES = {
    'views/orderAdmin/addOrder.html', 'views/orderAdmin/modifyOrder.html',
    'views/orderAdmin/dealRecord.html', 'views/orderAdmin/deliveryRecord.html',
    'views/reportMedical/feeStatistic.html', 'views/reportMedical/medicalStatistic.html',
    'views/reportMedical/materialStatistic.html', 'views/reportMedical/myReceiptRecord.html',
    'views/reportMedical/myDeliveryRecord.html', 'views/reportMedical/myJxcRecord.html',
    'views/memberManage/promotionDetail.html', 'views/memberManage/addMemberTag.html',
}

# 裁决 B：大屏/喊叫器/工作台 -> 一期建
PHASE1_SCREEN = {
    'bigScreen', 'adminCall', 'checkCall', 'consultingScreen',
    'doctorWorkbench', 'workBeach', 'projectionScreen', 'pos',
}
# 裁决 B：硬件对接 -> Phase 2
PHASE2_HW = {'blueToothTransfer', 'detectionLog', 'cloudPrinterList', 'screenUrlConfig'}
# 未纳入 5 项裁决、需老板单独拍板的落地页（本轮不擅自裁）
PENDING = {'aioIntroduce', 'coinRuleIntroduce', 'testPage'}


def jload(n):
    with open(os.path.join(BASE, n), encoding='utf-8') as f:
        return json.load(f)


def main():
    routes = []
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip() and row[0].strip().lower() != 'state':
                routes.append({'state': row[0].strip().lstrip('\ufeff'),
                               'url': row[1].strip(), 'controller': row[2].strip(),
                               'template': row[3].strip()})
    sf = jload('state-factory.json')['states']
    inv = jload('uncovered-analysis.json')
    cmd = set(jload('command-jumps.json')['distinctTargetStates'])

    # 权限归属
    path2states = collections.defaultdict(list)
    for r in routes:
        u = r['url'].split('?')[0].lstrip('/')
        path2states[u].append(r['state'])
        path2states[u.split('/')[-1]].append(r['state'])
    perm = set()
    for paths in sf.values():
        for p in paths:
            perm.update(path2states.get(p, []))

    # F8 集合
    f8 = set()
    for k, v in inv['buckets'].items():
        for it in v['items']:
            f8.add(it['state'])

    rows, tally = [], collections.Counter()
    for r in routes:
        st = r['state']
        # 裁决落地
        if r['template'] in DEAD_TEMPLATES:
            disp, why = '不建', '裁决A：生产模板 404/0字节，一比一不继承'
        elif st in PENDING:
            disp, why = '待裁决', '介绍/测试落地页，不在 5 项裁决范围，需单独拍板'
        elif st in PHASE1_SCREEN:
            disp, why = '建-P1', '裁决B：大屏/工作台，一期建'
        elif st in PHASE2_HW:
            disp, why = 'Phase2', '裁决B：硬件对接，一期不做'
        elif st in perm:
            disp, why = '建-P1', '权限树内，有界面归属'
        elif st in cmd:
            disp, why = '建-P1', '裁决C：命令式可达（静态盲区）'
        elif st in f8:
            disp, why = '建-P1', '裁决C：独立业务页，本期不补权限点'
        else:
            disp, why = '建-P1', 'Tab/二级界面，随父级建设'
        tally[disp] += 1
        rows.append({'state': st, 'url': r['url'], 'template': r['template'],
                     'controller': r['controller'], 'disposition': disp,
                     'reason': why,
                     'permissionState': ('PROD' if st in perm else
                                         ('CMD' if st in cmd else 'NONE'))})

    out = {'generatedBy': 're/gen-scope-freeze.py',
           'basis': '裁决 A~E（老板 2026-10-01 拍板）',
           'total': len(rows), 'tally': dict(tally),
           'permissionAttribution': dict(collections.Counter(
               r['permissionState'] for r in rows)),
           'routes': rows}
    dest = os.path.join(BASE, 'scope-freeze.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('== 485 路由 施工范围冻结表 ==')
    print('  总路由 %d' % len(rows))
    for k, v in sorted(tally.items()):
        print('    %-10s %4d  (%.1f%%)' % (k, v, 100.0 * v / len(rows)))
    print('\n-- 权限归属标注 --')
    for k, v in sorted(out['permissionAttribution'].items()):
        print('    %-10s %4d' % (k, v))
    print('\n-- 不建清单 (%d) --' % tally['不建'])
    for r in rows:
        if r['disposition'] == '不建':
            print('    %-40s %s' % (r['state'], r['reason']))
    print('\n-- Phase2 清单 (%d) --' % tally['Phase2'])
    for r in rows:
        if r['disposition'] == 'Phase2':
            print('    %-40s %s' % (r['state'], r['reason']))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
