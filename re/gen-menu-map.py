#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gen-menu-map.py
以【生产权限树 8 个一级分组】为主干，统计每组的子菜单数与界面数。
- 权限分组与叶子清单：re/permission-tree.json（生产实测）
- 权限 state -> 界面路径：re/state-factory.json（生产 bundle 实测）
- 路由全表：re/routes.csv
分组归属为语义对齐（stateFactory 未携带 stateType 信息），已标注。
"""
import csv, json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))

def load(p):
    with open(os.path.join(BASE, p), encoding='utf-8') as f:
        return json.load(f)

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

# ---- 70 个 stateFactory state -> 8 个权限一级分组（语义对齐）----
GROUP_OF = {
    '就诊流程': ['home', 'myMember', 'waitChargeList', 'member', 'orderList',
                'machineOrderWaitAccess', 'machineOrderChainWaitAccess', 'addCheckin',
                'fundus', 'adminBill', 'myAccount', 'optometry', 'optometryList',
                'allSize', 'dataChart',
                'deliveryList', 'visionMesure',
                # 「预约叫号」在权限树中是 就诊流程 下的 L2，不是独立一级分组
                'queueMachine', 'bookManage', 'getGlassNotifyList', 'selectOrderList'],
    '患者维护': ['branchMember', 'clientsList', 'followUp', 'recommendCustomer',
                'recommendDetail', 'recommendPhoneList', 'remindList'],
    '营销管理': ['grouponList', 'couponList', 'secKillPromotionList', 'pointsList',
                'orderManage', 'sendPlatform', 'addSaleRecord', 'hospitalRecharge'],
    '筛查机构': ['schoolList', 'schoolPlanList', 'areaSchoolPlanList', 'schoolPlanReport',
                'schoolMateCheckReports', 'screenPromotionList', 'screenConditionBatch',
                'healthScreenConfig', 'printStudentReport', 'inspectList', 'encryptUser',
                'mateCheckReportList', 'physicalReport'],
    '到店筛查': ['screenInStore', 'screenPromotionConfig'],
    '物资管理': ['companyInventory', 'stockList', 'materialPurchase', 'materialPurchaseRequest',
                'stockListCustomer', 'viewStockList', 'chainStockList', 'stockInReport',
                'cashClients'],
    '数据报表': ['reportOperateAllreportOperate'],
    '诊所管理': ['adminList', 'adminAreaList', 'hospitalhospitallist', 'sataServerList',
                'systemSettingcheckList', 'newsList', 'wechatAuth', 'assistCheckList',
                'brandList'],
}

def main():
    pt = load('permission-tree.json')
    sf = load('state-factory.json')['states']
    routes = load_routes()

    leaf_of = {}
    for g in pt['tree']:
        def walk(node, path):
            name = node.get('name') or node.get('stateType')
            kids = node.get('children') or []
            if kids:
                for k in kids:
                    walk(k, path + [name])
            else:
                leaf_of.setdefault(g['stateType'], []).append(' / '.join(path + [name]))
        for c in (g.get('children') or []):
            walk(c, [g['stateType']])

    # 路由 URL 拼接（ui-router 0.2.x 父子拼接）
    states = {r['state'] for r in routes}
    def real_url(st):
        parts = st.split('.')
        acc = []
        for i in range(len(parts)):
            cand = '.'.join(parts[:i + 1])
            if cand in states:
                r = next(x for x in routes if x['state'] == cand)
                u = r['url']
                if i == 0:
                    acc.append(u)
                else:
                    acc.append(u.lstrip('/'))
        return '#!/' + '/'.join(x for x in acc if x)

    # stateFactory 路径 -> 匹配到的路由 state
    path2states = collections.defaultdict(list)
    for r in routes:
        st = r['state']
        u = r['url'].split('?')[0]
        path2states[u.lstrip('/')].append(st)
        path2states[u.lstrip('/').split('/')[-1]].append(st)

    rows = []
    unassigned = []
    covered_paths = set()
    for grp, sts in GROUP_OF.items():
        gp = 0
        gs = 0
        detail = []
        for s in sts:
            if s not in sf:
                unassigned.append('%s / %s' % (grp, s))
                continue
            gs += 1
            n = len(sf[s])
            gp += n
            covered_paths.update(sf[s])
            detail.append({'state': s, 'paths': sf[s], 'n': n})
        leaves = leaf_of.get(grp, [])
        rows.append({
            'group': grp,
            'subMenus': len(leaves),
            'leaves': leaves,
            'permissionStates': gs,
            'coveredPaths': gp,
            'states': detail,
        })

    # 覆盖率
    covered_routes = set()
    for p in covered_paths:
        for st in path2states.get(p, []):
            covered_routes.add(st)

    out = {
        'caliber': '生产权限树 8 个一级分组为主干（唯一与生产 UI 一致的口径）',
        'groupingNote': 'GROUP_OF 为语义对齐：stateFactory 本身不携带 stateType 信息，'
                        '分组归属需在 G-01（108 个 state 实值）闭合后复核',
        'groups': rows,
        'unassignedStates': unassigned,
        'coverage': {
            'totalRoutes': len(routes),
            'distinctTemplates': len({r['template'] for r in routes}),
            'stateFactoryStates': len(sf),
            'stateFactoryPaths': sum(len(v) for v in sf.values()),
            'routesCoveredByPermissions': len(covered_routes),
            'routesNotCoveredByPermissions': len(routes) - len(covered_routes),
        },
    }
    dest = os.path.join(BASE, 'menu-map.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('%-10s %8s %10s %12s' % ('分组', '子菜单数', '权限state', '覆盖界面'))
    print('-' * 46)
    for r in rows:
        print('%-10s %8d %10d %12d' % (r['group'], r['subMenus'],
                                        r['permissionStates'], r['coveredPaths']))
    print('-' * 46)
    print('%-10s %8d %10d %12d' % ('合计',
                                    sum(r['subMenus'] for r in rows),
                                    sum(r['permissionStates'] for r in rows),
                                    sum(r['coveredPaths'] for r in rows)))
    c = out['coverage']
    print('\n路由 %d / 去重模板 %d / 权限state %d / 权限路径 %d' % (
        c['totalRoutes'], c['distinctTemplates'],
        c['stateFactoryStates'], c['stateFactoryPaths']))
    print('被权限覆盖的路由 %d，未被任何权限state覆盖 %d' % (
        c['routesCoveredByPermissions'], c['routesNotCoveredByPermissions']))
    if unassigned:
        print('\n未在 stateFactory 中找到的 state: %s' % unassigned)
    print('\nWrote: %s' % dest)

if __name__ == '__main__':
    main()
