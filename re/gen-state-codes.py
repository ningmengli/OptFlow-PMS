#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
re/gen-state-codes.py
裁决 D（老板 2026-10-01 拍板）：38 个未知权限 state 自定编码，记【OptFlow设计】。
编码规则：沿用生产 isOldActive 的 state.replace(".","") 去点规则，
         码值 = 对应路由 state 去掉点号，与生产 70 个实值同构。
每个编码标注 evidence：
   PROD  = 生产 stateFactory 实测值（70 个，一比一必须原样保留）
   OF-D  = OptFlow 自定编码（本次生成，需在代码与文档中标注）
只读本地证据层。
"""
import csv, json, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))


def jload(n):
    with open(os.path.join(BASE, n), encoding='utf-8') as f:
        return json.load(f)


def code_of(state):
    """生产命名规则：去掉点号"""
    return state.replace('.', '')


# 数据报表 35 个菜单叶 → 路由 state 的逐项配对
# 依据：叶路径的 L3 分类名 与 路由 state 的第 2 段 一一对应；
#       分类内按语义配对（中文报表名 → 生产英文路由名）。
REPORT_MAP = {
    # 运营统计 → report.reportOperateAll.*
    '数据报表 / 数据报表 / 运营统计 / 整体报表': 'report.reportOperateAll.reportOperate',
    '数据报表 / 数据报表 / 运营统计 / 分店日报': 'report.reportOperateAll.hospitalReport',
    '数据报表 / 数据报表 / 运营统计 / 分店报表': 'report.reportOperateAll.singleHospitalProfit',
    '数据报表 / 数据报表 / 运营统计 / 收银台报表': 'report.reportOperateAll.feeCashier',
    # 医务统计 → report.reportMedicalRate.*
    '数据报表 / 数据报表 / 医务统计 / 成交率': 'report.reportMedicalRate.successRate',
    '数据报表 / 数据报表 / 医务统计 / 评价流水': 'report.reportMedicalRate.satisfyDetailRate',
    '数据报表 / 数据报表 / 医务统计 / 满意度': 'report.reportMedicalRate.satisfyRate',
    '数据报表 / 数据报表 / 医务统计 / 患者来源统计': 'report.reportMedicalRate.customerChannelRate',
    # 费用统计 → report.reportFee.*
    '数据报表 / 数据报表 / 费用统计 / 收费流水': 'report.reportFee.feeDay',
    '数据报表 / 数据报表 / 费用统计 / 退费流水': 'report.reportFee.refundFee',
    '数据报表 / 数据报表 / 费用统计 / 收费月报': 'report.reportFee.feeMonth',
    '数据报表 / 数据报表 / 费用统计 / 充值流水': 'report.reportFee.feeRecharge',
    '数据报表 / 数据报表 / 费用统计 / 充值余额': 'report.reportFee.feeBankCard',
    '数据报表 / 数据报表 / 费用统计 / 挂账流水': 'report.reportFee.unPayCharge',
    '数据报表 / 数据报表 / 费用统计 / 挂账余额': 'report.reportFee.unPayRecharge',
    '数据报表 / 数据报表 / 费用统计 / 积分流水': 'report.reportFee.pointsListCharge',
    '数据报表 / 数据报表 / 费用统计 / 积分余额': 'report.reportFee.pointsListReCharge',
    '数据报表 / 数据报表 / 费用统计 / 次卡流水': 'report.reportFee.timeCardRecharge',
    '数据报表 / 数据报表 / 费用统计 / 次卡余额': 'report.reportFee.timecardBlance',
    '数据报表 / 数据报表 / 费用统计 / 次卡业绩': 'report.reportFee.timecardPerformance',
    # 物资统计 → report.reportMaterial.*
    '数据报表 / 数据报表 / 物资统计 / 入库流水': 'report.reportMaterial.receiptRecord',
    '数据报表 / 数据报表 / 物资统计 / 出库流水': 'report.reportMaterial.deliveryRecordPort',
    '数据报表 / 数据报表 / 物资统计 / 进销存统计': 'report.reportMaterial.jxcRecord',
    # 销售统计 → report.reportSale.*
    '数据报表 / 数据报表 / 销售统计 / 销售流水': 'report.reportSale.saleList',
    '数据报表 / 数据报表 / 销售统计 / 退货流水': 'report.reportSale.backGoodRecord',
    '数据报表 / 数据报表 / 销售统计 / 产品销量': 'report.reportSale.saleRecord',
    '数据报表 / 数据报表 / 销售统计 / 发货流水': 'report.reportSale.deliveryList',
    '数据报表 / 数据报表 / 销售统计 / 加工流水': 'report.reportSale.machineProcessList',
    '数据报表 / 数据报表 / 销售统计 / 限今日数据': 'report.reportSale.todayDataOnly',
    # 客户统计 → report.analysis.*
    '数据报表 / 数据报表 / 客户统计 / 客户转化漏斗': 'report.analysis.conversionFunnel',
    '数据报表 / 数据报表 / 客户统计 / 客户跟进分析': 'report.analysis.followUpAnalysis',
    '数据报表 / 数据报表 / 客户统计 / RFM模型': 'report.analysis.rfmModel',
    '数据报表 / 数据报表 / 客户统计 / 客户画像分析': 'report.analysis.profileAnalysis',
    '数据报表 / 数据报表 / 客户统计 / 查看全部门店报表': 'report.analysis',
    # 高级报表
    '数据报表 / 高级报表': 'reportStatistic',
}

# 诊所管理：11 叶中 stateFactory 已给出 9 个实值，剩下 2 个由路由补
CLINIC_EXTRA = {
    '诊所管理 / 需求提交平台': 'requirementStatus',
    '诊所管理 / 标签打印机': 'cloudPrinterList',
}


def main():
    routes = {}
    with open(os.path.join(BASE, 'routes.csv'), encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if len(row) >= 4 and row[0].strip() and row[0].strip().lower() != 'state':
                routes[row[0].strip().lstrip('\ufeff')] = row[1].strip()

    sf = jload('state-factory.json')['states']
    mm = jload('menu-map.json')

    # 生产已覆盖的 state -> 归属叶（按组粗粒度，仅用于标注重复）
    prod_states = set(sf.keys())

    out = {'rule': 'state.replace(".","")  —— 与生产 isOldActive 同规则',
           'generatedBy': 're/gen-state-codes.py',
           'PROD_实测70': sorted(prod_states),
           'OF-D_自定': []}

    # 数据报表 35 叶
    for leaf, route_state in sorted(REPORT_MAP.items()):
        if route_state not in routes:
            out['OF-D_自定'].append({
                'leaf': leaf, 'routeState': route_state, 'code': code_of(route_state),
                'evidence': 'OF-D', 'note': '路由不存在，需人工命名'})
            continue
        out['OF-D_自定'].append({
            'leaf': leaf,
            'routeState': route_state,
            'url': routes[route_state],
            'code': code_of(route_state),
            'evidence': 'OF-D',
            'note': '与生产 reportOperateAllreportOperate 同构的叶子级细分编码',
        })

    for leaf, route_state in sorted(CLINIC_EXTRA.items()):
        out['OF-D_自定'].append({
            'leaf': leaf, 'routeState': route_state,
            'url': routes.get(route_state, '(无路由)'),
            'code': code_of(route_state), 'evidence': 'OF-D',
            'note': '诊所管理组补齐'})

    # 校验
    dup = [k for k, v in collections.Counter(
        x['code'] for x in out['OF-D_自定']).items() if v > 1]
    collide = sorted({x['code'] for x in out['OF-D_自定']} & prod_states)
    orphan = [x for x in out['OF-D_自定'] if x['note'].startswith('路由不存在')]

    out['_校验'] = {
        '生成总数': len(out['OF-D_自定']),
        '重复码': dup,
        '与生产70个实值碰撞': collide,
        '无对应路由需人工命名': [x['leaf'] for x in orphan],
        '叶覆盖': '%d / 35（数据报表）' % len([x for x in out['OF-D_自定']
                                             if x['leaf'].startswith('数据报表')]),
    }

    dest = os.path.join(BASE, 'state-codes.json')
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print('== 编码生成（裁决 D）==')
    print('  规则: %s' % out['rule'])
    print('  生产实值（PROD，一比一原样保留）: %d' % len(prod_states))
    print('  本次生成（OF-D，OptFlow 自定）  : %d' % len(out['OF-D_自定']))
    print('  合计权限点                      : %d' % (len(prod_states) + len(out['OF-D_自定'])))
    print('\n-- 校验 --')
    for k, v in out['_校验'].items():
        print('  %-24s %s' % (k, v))
    print('\n-- 数据报表样例（前 10）--')
    for x in [y for y in out['OF-D_自定'] if y['leaf'].startswith('数据报表')][:10]:
        print('  %-46s -> %s' % (x['leaf'].split('/')[-1].strip(), x['code']))
    print('\nWrote: %s' % dest)


if __name__ == '__main__':
    main()
