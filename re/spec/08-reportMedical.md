# 08｜模块 reportMedical 报表/统计

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/reportMedical/` |
| 中文名 | 报表/统计 |
| 开发波次 | W8 |
| 页面数 | **42** |
| 端点数（去重） | **40** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `report.reportSale.backGoodRecord` | `/backGoodRecord` | `views/reportMedical/backGoodRecord.html` | `backGoodRecordCtrl` | 2 |
| 2 | `report.reportMedicalRate.customerChannelRate` | `/customerChannelRate` | `views/reportMedical/customerChannelRate.html` | `customerChannelRateCtrl` | 1 |
| 3 | `report.reportSale.deliveryList` | `/deliveryList` | `views/reportMedical/deliveryList.html` | `deliveryReportListCtrl` | 2 |
| 4 | `report.reportMaterial.deliveryRecordPort` | `/deliveryRecordPort` | `views/reportMedical/deliveryRecordPort.html` | `deliveryRecordPortCtrl` | 2 |
| 5 | `report.reportFee.feeBankCard` | `/feeBankCard` | `views/reportMedical/feeBankCard.html` | `feeBankCardCtrl` | 1 |
| 6 | `report.reportOperateAll.feeCashier` | `/feeCashier` | `views/reportMedical/feeCashier.html` | `feeCashierCtrl` | 3 |
| 7 | `report.reportFee.feeDay` | `/feeDay` | `views/reportMedical/feeDay.html` | `feeDayCtrl` | 3 |
| 8 | `report.reportFee.feeMonth` | `/feeMonth` | `views/reportMedical/feeMonth.html` | `feeMonthCtrl` | 2 |
| 9 | `report.reportFee.feeRecharge` | `/feeRecharge` | `views/reportMedical/feeRecharge.html` | `feeRechargeCtrl` | 1 |
| 10 | `feeStatistic` | `/feeStatistic` | `views/reportMedical/feeStatistic.html` | `reportFeeCtrl` | 0 |
| 11 | `report.reportOperateAll.hospitalReport` | `/hospitalReport` | `views/reportMedical/hospitalReport.html` | `hospitalReportCtrl` | 1 |
| 12 | `report.reportMaterial.jxcRecord` | `/jxcRecord` | `views/reportMedical/jxcRecord.html` | `jxcRecordCtrl` | 3 |
| 13 | `report.reportSale.machineProcessList` | `/machineProcessList` | `views/reportMedical/machineProcessList.html` | `machineProcessListCtrl` | 4 |
| 14 | `materialStatistic` | `/materialStatistic` | `views/reportMedical/materialStatistic.html` | `reportSaleCtrl` | 0 |
| 15 | `medicalStatistic` | `/medicalStatistic` | `views/reportMedical/medicalStatistic.html` | `reportMedicalRateCtrl` | 0 |
| 16 | `materialStatistic.myDeliveryRecord` | `/myDeliveryRecord` | `views/reportMedical/myDeliveryRecord.html` | `myDeliveryRecordCtrl` | 0 |
| 17 | `materialStatistic.myJxcRecord` | `/myJxcRecord` | `views/reportMedical/myJxcRecord.html` | `myJxcRecordCtrl` | 0 |
| 18 | `materialStatistic.myReceiptRecord` | `/myReceiptRecord` | `views/reportMedical/myReceiptRecord.html` | `myReceiptRecordCtrl` | 0 |
| 19 | `report.reportFee.pointsListCharge` | `/pointsListCharge` | `views/reportMedical/pointsListCharge.html` | `pointsListChargeCtrl` | 0 |
| 20 | `report.reportFee.pointsListReCharge` | `/pointsListReCharge` | `views/reportMedical/pointsListReCharge.html` | `pointsListReChargeCtrl` | 1 |
| 21 | `profitReport` | `/profitReport` | `views/reportMedical/profitReport.html` | `profitReportCtrl` | 3 |
| 22 | `report.reportMaterial.receiptRecord` | `/receiptRecord` | `views/reportMedical/receiptRecord.html` | `receiptRecordCtrl` | 2 |
| 23 | `report.reportFee.refundFee` | `/refundFee` | `views/reportMedical/refundFee.html` | `refundFeeCtrl` | 3 |
| 24 | `report` | `/report` | `views/reportMedical/report.html` | `reportCtrl` | 1 |
| 25 | `report.reportFee` | `/reportFee` | `views/reportMedical/reportFee.html` | `reportFeeCtrl` | 0 |
| 26 | `report.reportMaterial` | `/reportMaterial` | `views/reportMedical/reportMaterial.html` | `reportSaleCtrl` | 0 |
| 27 | `report.reportMedicalRate` | `/reportMedicalRate` | `views/reportMedical/reportMedicalRate.html` | `reportMedicalRateCtrl` | 0 |
| 28 | `report.reportOperateAll.reportOperate` | `/reportOperate` | `views/reportMedical/reportOperate.html` | `reportOperateCtrl` | 6 |
| 29 | `report.reportOperateAll` | `/reportOperateAll` | `views/reportMedical/reportOperateAll.html` | `reportOperateAllCtrl` | 0 |
| 30 | `report.reportSale` | `/reportSale` | `views/reportMedical/reportSale.html` | `reportSaleCtrl` | 0 |
| 31 | `report.reportSale.saleList` | `/saleList` | `views/reportMedical/saleList.html` | `saleListCtrl` | 2 |
| 32 | `report.reportSale.saleRecord` | `/saleRecord` | `views/reportMedical/saleRecord.html` | `saleRecordCtrl` | 2 |
| 33 | `report.reportMedicalRate.satisfyDetailRate` | `/satisfyDetailRate` | `views/reportMedical/satisfyDetailRate.html` | `satisfyDetailRateCtrl` | 2 |
| 34 | `report.reportMedicalRate.satisfyRate` | `/satisfyRate` | `views/reportMedical/satisfyRate.html` | `satisfyRateCtrl` | 0 |
| 35 | `report.reportOperateAll.singleHospitalProfit` | `/singleHospitalProfit` | `views/reportMedical/singleHospitalProfit.html` | `singleHospitalProfitCtrl` | 1 |
| 36 | `stockInReport` | `/stockInReport` | `views/reportMedical/stockInReport.html` | `jxcRecordCtrl` | 3 |
| 37 | `report.reportMedicalRate.successRate` | `/successRate` | `views/reportMedical/successRate.html` | `successRateCtrl` | 1 |
| 38 | `report.reportFee.timeCardRecharge` | `/timeCardRecharge` | `views/reportMedical/timeCardRecharge.html` | `timeCardRechargeCtrl` | 2 |
| 39 | `report.reportFee.timecardBlance` | `/timecardBlance` | `views/reportMedical/timecardBlance.html` | `timecardBlanceCtrl` | 2 |
| 40 | `report.reportFee.timecardPerformance` | `/timecardPerformance` | `views/reportMedical/timecardPerformance.html` | `timecardPerformanceCtrl` | 2 |
| 41 | `report.reportFee.unPayCharge` | `/unPayCharge` | `views/reportMedical/unPayCharge.html` | `unPayChargeCtrl` | 0 |
| 42 | `report.reportFee.unPayRecharge` | `/unPayRecharge` | `views/reportMedical/unPayRecharge.html` | `unPayRechargeCtrl` | 1 |

## §2 端点清单（去重 40 个）

- `POST /admin/getChannelTagTreeVoPage.json`
- `POST /admin/getChildrenLinkAndCode.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCompanyListOfMine.json`
- `POST /admin/getCompanySalesDataList.json`
- `POST /admin/getCorpPayChannel.json`
- `POST /admin/getCustomerDataBetween.json`
- `POST /admin/getOkSalesDataBetween.json`
- `POST /admin/getSchoolVoList.json`
- `POST /admin/getStockInSkuDataList.json`
- `POST /admin/getStockOutSkuDataList.json`
- `POST /admin/getSupplier.json`
- `POST /admin/getYmOkSalesDataList.json`
- `POST /admin/selectCashRegisterVoList.json`
- `POST /admin/selectCashflowRefundFeeVoList.json`
- `POST /admin/selectCommentEmployeeVoList.json`
- `POST /admin/selectCompanyDayReportVoList.json`
- `POST /admin/selectCustomerCreditLogVoList.json`
- `POST /admin/selectCustomerCreditVoList.json`
- `POST /admin/selectCustomerPointLogVoList.json`
- `POST /admin/selectCustomerPointVoList.json`
- `POST /admin/selectCustomerTrainerCardDataListForStatBalance.json`
- `POST /admin/selectCustomerTrainerCardDataListForStatGoals.json`
- `POST /admin/selectCustomerTrainerCardVoListForDetailReport.json`
- `POST /admin/selectCustomerWalletLogVoList.json`
- `POST /admin/selectCustomerWalletVoList.json`
- `POST /admin/selectMachineCenterOrderRecordVoList.json`
- `POST /admin/selectMachineCenterVoList.json`
- `POST /admin/selectMedicalProductDeliveryVoList.json`
- `POST /admin/selectMedicalProductKpiDataListOfEmployee.json`
- `POST /admin/selectMedicalProductSalesVoList.json`
- `POST /admin/selectProductSkuSalesDataList.json`
- `POST /admin/selectRefundProductLogVoList.json`
- `POST /admin/selectStockInSkuDataVoList.json`
- `POST /admin/selectStorehouseVoList.json`
- `POST /admin/statCashRegisterByType.json`
- `POST /admin/statCommentEmployee.json`
- `POST /admin/statCustomerWalletAndTrainerCard.json`
- `POST /admin/statMedicalRecordCashflow.json`
- `POST /admin/statMedicalRecordFeeYmdList.json`

## §3 逐页字段规格

### 8.1 `report.reportSale.backGoodRecord`

- **URL**：`/backGoodRecord`
- **模板**：`views/reportMedical/backGoodRecord.html`
- **控制器**：`backGoodRecordCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectRefundProductLogVoList` | `POST /admin/selectRefundProductLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}退货流水报表 |
| 2 | 退货时间 |
| 3 | 会员 |
| 4 | 产品名称 |
| 5 | 规格 |
| 6 | 生产厂商 |
| 7 | 默认供应商 |
| 8 | 数量 |
| 9 | 费用合计 |
| 10 | 折后金额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.keyword` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `item.refundProductLog.refundTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customer.customerName` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.refundProductLog.refundCount` |
| `item.refundProductLog.useCount` |
| `item.refundProductLog.marketPrice` |
| `item.refundProductLog.rateFee` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

### 8.2 `report.reportMedicalRate.customerChannelRate`

- **URL**：`/customerChannelRate`
- **模板**：`views/reportMedical/customerChannelRate.html`
- **控制器**：`customerChannelRateCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getChannelTagTreeVoPage` | `POST /admin/getChannelTagTreeVoPage.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setDate(item,$index)` |

### 8.3 `report.reportSale.deliveryList`

- **URL**：`/deliveryList`
- **模板**：`views/reportMedical/deliveryList.html`
- **控制器**：`deliveryReportListCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectMedicalProductDeliveryVoList` | `POST /admin/selectMedicalProductDeliveryVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}发货流水报表 |
| 2 | 收费时间 |
| 3 | 门店 |
| 4 | 开单人 |
| 5 | 患者 |
| 6 | 会员 |
| 7 | 手机号 |
| 8 | 品牌 |
| 9 | 类目 |
| 10 | 产品编码/ 条形码 |
| 11 | 产品名称 |
| 12 | 规格 |
| 13 | 生产厂商 |
| 14 | 默认供应商 |
| 15 | 默认成本 |
| 16 | 单位 |
| 17 | 待发货数量 |
| 18 | 发货数量 |
| 19 | 折后金额 |
| 20 | 批号 |
| 21 | 数量 |
| 22 | 进货成本 |
| 23 | 发货人 |
| 24 | 发货时间 |
| 25 | 发货状态 |
| 26 | 收费状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.payStartTime` |
| `obj.rightTimer` |
| `obj.deliveryStartTime` |
| `obj.rightTimer2` |
| `obj.productKeyword` |
| `obj.batchNoKeyword` |
| `pageSize` |
| `obj.keyword` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `hasAuth` |
| `VIEW_COST_PRICE` |
| `obj` |
| `dateformat` |
| `getDataList.total.waitingDeliveryCount` |
| `getDataList.total.deliveryCount` |
| `item.rowspan` |
| `item.medicalProduct.payedTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecordVo.company.companyName` |
| `item.medicalRecordVo.medicalRecord.doctorName` |
| `item.medicalRecordVo.patient.patientName` |
| `item.medicalRecordVo.customer.customerName` |
| `item.medicalRecordVo.customer.linkMobile` |
| `hidePhone` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productCode` |
| `item.medicalProduct.skuCode` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `printModel` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.productSku.costPrice` |
| `item.medicalProduct.unitName` |
| `item.deliveryData.waitingDeliveryCount` |
| `item.deliveryData.deliveryCount` |
| `item.medicalProduct.rateFee` |
| `item.stockInSku.batchNo` |
| `item.medicalProductStock.deliveryCount` |
| `item.stockInSku.skuPrice` |
| `item.medicalProductDelivery.completePersonName` |
| `item.medicalProductDelivery.completeTime` |
| `item.medicalProductDelivery.deliveryStatus` |
| `deliveryStatus` |
| `getDataList.count` |
| `pageIndex` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setFee(null)` |
| `setFee(2)` |
| `setFee(3)` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `downloadModal=true` |
| `downloadModal=false` |
| `daochu()` |

### 8.4 `report.reportMaterial.deliveryRecordPort`

- **URL**：`/deliveryRecordPort`
- **模板**：`views/reportMedical/deliveryRecordPort.html`
- **控制器**：`deliveryRecordPortCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getStockOutSkuDataList` | `POST /admin/getStockOutSkuDataList.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}出库流水报表 |
| 2 | 仓库 |
| 3 | 出库日期 |
| 4 | 出库单号 |
| 5 | 出库类型 |
| 6 | 出库人员 |
| 7 | 领用人员 |
| 8 | 商品编码/ 条形码 |
| 9 | 商品名称 |
| 10 | 规格 |
| 11 | 生产厂商 |
| 12 | 默认供应商 |
| 13 | 采购供应商 |
| 14 | 数量 |
| 15 | 单位 |
| 16 | 零售价 |
| 17 | 成本价 |
| 18 | 成本合计 |
| 19 | 批号 |
| 20 | 有效期 |
| 21 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.factoryKeyword` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.batchNoKeyword` |
| `obj.outType` |
| `obj.drawEmployeeKeyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDataList.count` |
| `hasAuth` |
| `VIEW_COST_PRICE` |
| `obj` |
| `dateformat` |
| `getDataList.total.outCount` |
| `getDataList.total.outTotalCostPrice` |
| `item.storehouse.name` |
| `item.stockOut.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockOut.id` |
| `item.stockOut.outType` |
| `outType` |
| `item.stockOut.createName` |
| `item.drawEmployee.employeeName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.productName` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.supplier.supplierName` |
| `item.stockOutSku.outCount` |
| `item.productSku.unitName` |
| `item.productSku.marketPrice` |
| `item.stockInSku.skuPrice` |
| `item.stockOutSku.outTotalCostPrice` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockOut.remark` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `selectId()` |
| `downloadModal=false` |
| `daochu()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
```

### 8.5 `report.reportFee.feeBankCard`

- **URL**：`/feeBankCard`
- **模板**：`views/reportMedical/feeBankCard.html`
- **控制器**：`feeBankCardCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerWalletVoList` | `POST /admin/selectCustomerWalletVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 充值余额统计 |
| 2 | 会员姓名 |
| 3 | 手机号 |
| 4 | 本金金额 |
| 5 | 赠送金额 |
| 6 | 合计 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `EmployeeList.total.trueBalance` |
| `EmployeeList.total.giftBalance` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerWallet.trueBalance` |
| `item.customerWallet.giftBalance` |

### 8.6 `report.reportOperateAll.feeCashier`

- **URL**：`/feeCashier`
- **模板**：`views/reportMedical/feeCashier.html`
- **控制器**：`feeCashierCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `selectCashRegisterVoList` | `POST /admin/selectCashRegisterVoList.json` |
| `statCashRegisterByType` | `POST /admin/statCashRegisterByType.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ data \| dateformatter}}收银台流水报表 日期 |
| 2 | 档案号 |
| 3 | 所属{{corpInfo.companyTitle}} 特殊说明：2019.04.15之前的会员卡充值和挂账还款数据未做分{{corpInfo. companyTitle}}统计，不显示 |
| 4 | 姓名 |
| 5 | 会员名 |
| 6 | 类型 |
| 7 | 缴费合计 缴费合计 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码 |
| 8 | 现金 |
| 9 | 银行卡记账 |
| 10 | 微信记账 |
| 11 | 支付宝记账 |
| 12 | POS机刷卡 |
| 13 | 微信扫码 |
| 14 | 支付宝扫码 |
| 15 | 医保 |
| 16 | 挂账 |
| 17 | 商保 |
| 18 | 会员卡支付 会员卡支付=会员卡本金+会员卡赠金 |
| 19 | {{otherPay.channelName1}} |
| 20 | {{otherPay.channelName2}} |
| 21 | {{otherPay.channelName3}} |
| 22 | {{otherPay.channelName4}} |
| 23 | {{otherPay.channelName5}} |
| 24 | 优惠金额 优惠金额 = 打折优惠 + 减免优惠 + 积分优惠 |
| 25 | 备注 |
| 26 | 收银员 |
| 27 | 本金 |
| 28 | 赠金 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |
| `obj.keyword` |
| `obj.casherName` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `EmployeeList.total.amountTurneIn` |
| `EmployeeList.total.receivedFromCash` |
| `EmployeeList.total.receivedFromBankcard` |
| `EmployeeList.total.receivedFromWechat` |
| `EmployeeList.total.receivedFromAlipay` |
| `EmployeeList.total.receivedFromPos` |
| `EmployeeList.total.receivedFromWechatScan` |
| `EmployeeList.total.receivedFromAlipayScan` |
| `otherPay.channelName1` |
| `otherPay.channelName2` |
| `otherPay.channelName3` |
| `otherPay.channelName4` |
| `otherPay.channelName5` |
| `stateCashFactory.object` |
| `amountTurneIn` |
| `toZero` |
| `receivedFromCash` |
| `receivedFromBankcard` |
| `receivedFromWechat` |
| `receivedFromAlipay` |
| `receivedFromPos` |
| `receivedFromWechatScan` |
| `receivedFromAlipayScan` |
| `receivedFromMedical` |
| `receivedFromCredit` |
| `receivedFromCommercial` |
| `receivedFromWalletTrue` |
| `receivedFromWalletGift` |
| `receivedFromPayChannel1` |
| `receivedFromPayChannel2` |
| `receivedFromPayChannel3` |
| `receivedFromPayChannel4` |
| `receivedFromPayChannel5` |
| `amountPreferential` |
| `corpInfo.` |
| `companyTitle` |
| `data` |
| `dateformatter` |
| `corpInfo.companyTitle` |
| `EmployeeList.total.receivedFromMedical` |
| `EmployeeList.total.receivedFromCredit` |
| `EmployeeList.total.receivedFromCommercial` |
| `EmployeeList.total.receivedFromWalletTrue` |
| `EmployeeList.total.receivedFromWalletGift` |
| `EmployeeList.total.receivedFromPayChannel1` |
| `EmployeeList.total.receivedFromPayChannel2` |
| `EmployeeList.total.receivedFromPayChannel3` |
| `EmployeeList.total.receivedFromPayChannel4` |
| `EmployeeList.total.receivedFromPayChannel5` |
| `EmployeeList.total.amountPreferential` |
| `EmployeeList.total.remark` |
| `item.registerTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.company.companyName` |
| `item.patient.patientName` |
| `item.customer.customerName` |
| `item.registerType` |
| `registerType` |
| `item.receivedFromCredit` |
| `item.amountTurneIn` |
| `item.receivedFromCash` |
| `item.receivedFromBankcard` |
| `item.receivedFromWechat` |
| `item.receivedFromAlipay` |
| `item.receivedFromPos` |
| `item.receivedFromWechatScan` |
| `item.receivedFromAlipayScan` |
| `item.receivedFromMedical` |
| `item.receivedFromCommercial` |
| `item.receivedFromWalletTrue` |
| `item.receivedFromWalletGift` |
| `item.receivedFromPayChannel1` |
| `item.receivedFromPayChannel2` |
| `item.receivedFromPayChannel3` |
| `item.receivedFromPayChannel4` |
| `item.receivedFromPayChannel5` |
| `item.amountPreferential` |
| `item.remark` |
| `item.casherName` |
| `EmployeeList.count` |
| `downloadIndex` |
| `pageSize` |
| `EmployeeList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setFee(null)` |
| `setFee(1)` |
| `setFee(4)` |
| `setFee(3)` |
| `setFee(6)` |
| `setFee(2)` |
| `setFee(5)` |
| `downloadModal=true` |
| `downloadModal=false` |
| `daochu()` |

### 8.7 `report.reportFee.feeDay`

- **URL**：`/feeDay`
- **模板**：`views/reportMedical/feeDay.html`
- **控制器**：`feeDayCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getSchoolVoList` | `POST /admin/getSchoolVoList.json` |
| `statMedicalRecordCashflow` | `POST /admin/statMedicalRecordCashflow.json` |

**表单标签**

| 标签 |
|---|
| 按收费方式 按收费分类 不含全部退货 |
| 不含部分退货 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ data \| dateformatter}}收费流水报表 |
| 2 | 姓名 |
| 3 | 档案号 |
| 4 | 费用合计 |
| 5 | 折后金额 |
| 6 | 缴费金额 缴费金额 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码 |
| 7 | 现金 |
| 8 | 银行卡记账 |
| 9 | 微信记账 |
| 10 | 支付宝记账 |
| 11 | POS机刷卡 |
| 12 | 微信扫码 |
| 13 | 支付宝扫码 |
| 14 | 医保 |
| 15 | 挂账 |
| 16 | 商保 |
| 17 | 余额支付 余额支付=会员卡本金+会员卡赠金 |
| 18 | 积分支付 |
| 19 | {{otherPay.channelName1}} |
| 20 | {{otherPay.channelName2}} |
| 21 | {{otherPay.channelName3}} |
| 22 | {{otherPay.channelName4}} |
| 23 | {{otherPay.channelName5}} |
| 24 | 减免 |
| 25 | 备注 |
| 26 | 学校 |
| 27 | 收费信息 |
| 28 | 接诊{{corpInfo.employeeTitle}} |
| 29 | 商品明细 |
| 30 | 流水单号 |
| 31 | 本金 |
| 32 | 赠金 |
| 33 | {{ data \| dateformatter}}收费流水报表 |
| 34 | 姓名 |
| 35 | 档案号 |
| 36 | 检查费用 |
| 37 | 产品费用 |
| 38 | 定制费用 |
| 39 | 挂号费用 |
| 40 | 合计 |
| 41 | 学校 |
| 42 | 收费时间 |
| 43 | 收费人员 |
| 44 | 接诊{{corpInfo.employeeTitle}} |
| 45 | 商品明细 |
| 46 | 流水单号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |
| `obj.casherName` |
| `refundStatusArray[0]` |
| `refundStatusArray[1]` |
| `obj.keyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `adminConf.schoolEnable` |
| `data` |
| `dateformatter` |
| `otherPay.channelName1` |
| `otherPay.channelName2` |
| `otherPay.channelName3` |
| `otherPay.channelName4` |
| `otherPay.channelName5` |
| `corpInfo.employeeTitle` |
| `EmployeeList.total.totalFee` |
| `EmployeeList.total.totalPayment` |
| `EmployeeList.total.receivedFromCashier` |
| `EmployeeList.total.receivedFromCash` |
| `EmployeeList.total.receivedFromBankcard` |
| `EmployeeList.total.receivedFromWechat` |
| `EmployeeList.total.receivedFromAlipay` |
| `EmployeeList.total.receivedFromPos` |
| `EmployeeList.total.receivedFromWechatScan` |
| `EmployeeList.total.receivedFromAlipayScan` |
| `EmployeeList.total.receivedFromMedical` |
| `EmployeeList.total.receivedFromCredit` |
| `EmployeeList.total.receivedFromCommercial` |
| `EmployeeList.total.receivedFromWalletTrue` |
| `EmployeeList.total.receivedFromWalletGift` |
| `EmployeeList.total.receivedFromPoint` |
| `EmployeeList.total.receivedFromPayChannel1` |
| `EmployeeList.total.receivedFromPayChannel2` |
| `EmployeeList.total.receivedFromPayChannel3` |
| `EmployeeList.total.receivedFromPayChannel4` |
| `EmployeeList.total.receivedFromPayChannel5` |
| `EmployeeList.total.substractFee` |
| `item.patient.patientName` |
| `item.medicalRecord.medicalCode` |
| `item.cashflow.totalFee` |
| `item.cashflow.totalPayment` |
| `item.cashflow.receivedFromCashier` |
| `item.cashflow.receivedFromCash` |
| `item.cashflow.receivedFromBankcard` |
| `item.cashflow.receivedFromWechat` |
| `item.cashflow.receivedFromAlipay` |
| `item.cashflow.receivedFromPos` |
| `item.cashflow.receivedFromWechatScan` |
| `item.cashflow.receivedFromAlipayScan` |
| `item.cashflow.receivedFromMedical` |
| `item.cashflow.receivedFromCredit` |
| `item.cashflow.receivedFromCommercial` |
| `item.receivedFromWalletTrue` |
| `item.cashflow.receivedFromWalletGift` |
| `item.cashflow.receivedFromPoint` |
| `item.cashflow.receivedFromPayChannel1` |
| `item.cashflow.receivedFromPayChannel2` |
| `item.cashflow.receivedFromPayChannel3` |
| `item.cashflow.receivedFromPayChannel4` |
| `item.cashflow.receivedFromPayChannel5` |
| `item.cashflow.substractFee` |
| `item.cashflow.remark` |
| `item.school.schoolName` |
| `item.cashflow.casherName` |
| `item.cashflow.payTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecord.doctorName` |
| `item.medicalProductExamineDetails` |
| `item.cashflow.tradeNo` |
| `EmployeeList.total.medicalExamineRateFee` |
| `EmployeeList.total.medicalProductRateFee` |
| `EmployeeList.total.medicalProductModelRateFee` |
| `EmployeeList.total.registrationRateFee` |
| `item.medicalExamineRateFee` |
| `item.medicalProductRateFee` |
| `item.medicalProductModelRateFee` |
| `item.registrationRateFee` |
| `item.rateFee` |
| `EmployeeList.count` |
| `downloadIndex` |
| `pageSize` |
| `EmployeeList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `downloadModal=true` |
| `setTab(1)` |
| `setTab(2)` |
| `payedDetail(item.cashflow.id)` |
| `downloadModal=false` |
| `daochu()` |

### 8.8 `report.reportFee.feeMonth`

- **URL**：`/feeMonth`
- **模板**：`views/reportMedical/feeMonth.html`
- **控制器**：`feeMonthCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `statMedicalRecordFeeYmdList` | `POST /admin/statMedicalRecordFeeYmdList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}收费月报报表 |
| 2 | 日期 |
| 3 | 档案号 |
| 4 | 费用合计 |
| 5 | 折后金额 |
| 6 | 缴费金额 缴费金额 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码，不计退费 |
| 7 | 现金 |
| 8 | 银行卡记账 |
| 9 | 微信记账 |
| 10 | 支付宝记账 |
| 11 | POS机刷卡 |
| 12 | 微信扫码 |
| 13 | 支付宝扫码 |
| 14 | 医保 |
| 15 | 挂账 |
| 16 | 商保 |
| 17 | 余额支付 余额支付=会员卡本金+会员卡赠金 |
| 18 | 积分支付 |
| 19 | {{otherPay.channelName1}} |
| 20 | {{otherPay.channelName2}} |
| 21 | {{otherPay.channelName3}} |
| 22 | {{otherPay.channelName4}} |
| 23 | {{otherPay.channelName5}} |
| 24 | 减免 |
| 25 | 病历数 |
| 26 | 缴费患者数 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `otherPay.channelName1` |
| `otherPay.channelName2` |
| `otherPay.channelName3` |
| `otherPay.channelName4` |
| `otherPay.channelName5` |
| `EmployeeList.result.total.totalFee` |
| `EmployeeList.result.total.totalPayment` |
| `EmployeeList.result.total.receivedFromCashier` |
| `EmployeeList.result.total.receivedFromCash` |
| `EmployeeList.result.total.receivedFromBankcard` |
| `EmployeeList.result.total.receivedFromWechat` |
| `EmployeeList.result.total.receivedFromAlipay` |
| `EmployeeList.result.total.receivedFromPos` |
| `EmployeeList.result.total.receivedFromWechatScan` |
| `EmployeeList.result.total.receivedFromAlipayScan` |
| `EmployeeList.result.total.receivedFromMedical` |
| `EmployeeList.result.total.receivedFromCredit` |
| `EmployeeList.result.total.receivedFromCommercial` |
| `EmployeeList.result.total.receivedFromWallet` |
| `EmployeeList.result.total.receivedFromPoint` |
| `EmployeeList.result.total.receivedFromPayChannel1` |
| `EmployeeList.result.total.receivedFromPayChannel2` |
| `EmployeeList.result.total.receivedFromPayChannel3` |
| `EmployeeList.result.total.receivedFromPayChannel4` |
| `EmployeeList.result.total.receivedFromPayChannel5` |
| `EmployeeList.result.total.substractFee` |
| `EmployeeList.result.total.medicalRecordCount` |
| `EmployeeList.result.total.patientCount` |
| `item.ymd` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.medicalCode` |
| `item.totalFee` |
| `item.totalPayment` |
| `item.receivedFromCashier` |
| `item.receivedFromCash` |
| `item.receivedFromBankcard` |
| `item.receivedFromWechat` |
| `item.receivedFromAlipay` |
| `item.receivedFromPos` |
| `item.receivedFromWechatScan` |
| `item.receivedFromAlipayScan` |
| `item.receivedFromMedical` |
| `item.receivedFromCredit` |
| `item.receivedFromCommercial` |
| `item.receivedFromWallet` |
| `item.receivedFromPoint` |
| `item.receivedFromPayChannel1` |
| `item.receivedFromPayChannel2` |
| `item.receivedFromPayChannel3` |
| `item.receivedFromPayChannel4` |
| `item.receivedFromPayChannel5` |
| `item.substractFee` |
| `item.medicalRecordCount` |
| `item.patientCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

### 8.9 `report.reportFee.feeRecharge`

- **URL**：`/feeRecharge`
- **模板**：`views/reportMedical/feeRecharge.html`
- **控制器**：`feeRechargeCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerWalletLogVoList` | `POST /admin/selectCustomerWalletLogVoList.json` |

**表单标签**

| 标签 |
|---|
| 充值 |
| 消费 |
| 退卡 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}充值流水报表 |
| 2 | 操作时间 |
| 3 | {{corpInfo. companyTitle}} 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，不显示 |
| 4 | 会员姓名 |
| 5 | 收费方式 |
| 6 | 本金金额 |
| 7 | 赠送金额 |
| 8 | 合计 |
| 9 | 备注 |
| 10 | 操作人员 |
| 11 | {{ obj \| dateformat}}消费流水报表 |
| 12 | 操作时间 |
| 13 | {{corpInfo. companyTitle}} 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，不显示 |
| 14 | 会员姓名 |
| 15 | 档案号 |
| 16 | 患者姓名 |
| 17 | 本金金额 |
| 18 | 赠送金额 |
| 19 | 合计 |
| 20 | 备注 |
| 21 | 操作人员 |
| 22 | {{ obj \| dateformat}}退卡流水报表 |
| 23 | 操作时间 |
| 24 | {{corpInfo. companyTitle}} 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，不显示 |
| 25 | 会员姓名 |
| 26 | 退卡方式 |
| 27 | 本金金额 |
| 28 | 赠送金额 |
| 29 | 合计 |
| 30 | 备注 |
| 31 | 操作人员 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `corpInfo.` |
| `companyTitle` |
| `EmployeeList.total.addTrueMoney` |
| `EmployeeList.total.addGiftMoney` |
| `item.customerWalletLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.company.companyName` |
| `item.customer.customerName` |
| `item.customerWalletLog.payChannel` |
| `payChannel` |
| `item.customerWalletLog.addTrueMoney` |
| `item.customerWalletLog.addGiftMoney` |
| `item.customerWalletLog.remark` |
| `item.customerWalletLog.casherName` |
| `item.medicalRecord.medicalCode` |
| `returnType` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |

### 8.10 `feeStatistic`

- **URL**：`/feeStatistic`
- **模板**：`views/reportMedical/feeStatistic.html`
- **控制器**：`reportFeeCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.11 `report.reportOperateAll.hospitalReport`

- **URL**：`/hospitalReport`
- **模板**：`views/reportMedical/hospitalReport.html`
- **控制器**：`hospitalReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCompanyDayReportVoList` | `POST /admin/selectCompanyDayReportVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}分店日报报表 |
| 2 | 日期 |
| 3 | 病历数 |
| 4 | 接待患者人数 |
| 5 | 收费 收费 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码 |
| 6 | 充卡 充卡为本金金额，不包含赠送金金额 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，显示为0 |
| 7 | 挂账还款 挂账后收回的欠款 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，显示为0 |
| 8 | 挂账退款 挂账还款后再退款 特殊说明：2022.09.01之前的挂账退款数据合并在退费里统计，之后单独对其进行统计 |
| 9 | 退费 |
| 10 | 退卡 |
| 11 | 缴费合计 缴费合计 = 收费 + 会员卡充值 + 挂账还款 - 挂账退款 - 退费 - 退卡 特殊说明：2019.04.15之前的数据未做会员卡充值和挂账还款的分{{corpInfo. companyTitle}}统计，相应项目显示为0。 |
| 12 | 验配数 |
| 13 | 成交率 |
| 14 | 验配销售额 |
| 15 | 二次销售额 |
| 16 | 总销售额 |
| 17 | 总销售额（已缴） |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `corpInfo.` |
| `companyTitle` |
| `item.reportDay` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecordCount` |
| `item.userCount` |
| `item.receivedFromCashier1` |
| `item.receivedFromCashier4` |
| `item.receivedFromCashier3` |
| `item.receivedFromCashier6` |
| `item.receivedFromCashier2` |
| `item.receivedFromCashier5` |
| `item.amountTurneIn` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

### 8.12 `report.reportMaterial.jxcRecord`

- **URL**：`/jxcRecord`
- **模板**：`views/reportMedical/jxcRecord.html`
- **控制器**：`jxcRecordCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectStockInSkuDataVoList` | `POST /admin/selectStockInSkuDataVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 按商品 按批号 本期库存有变动 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}进销存统计报表 |
| 2 | 仓库 |
| 3 | 商品编码 |
| 4 | 条形码 |
| 5 | 商品名称 |
| 6 | 规格 |
| 7 | 生产厂商 |
| 8 | 默认供应商 |
| 9 | 采购供应商 |
| 10 | 单位 |
| 11 | 零售价 |
| 12 | 成本价 |
| 13 | 批号 |
| 14 | 有效期 |
| 15 | 期初库存数量 |
| 16 | 本期入库数量 |
| 17 | 本期出库数量 |
| 18 | 本期盘点数量 盘点数量：盘点时增减的库存数，盘盈为正，盘亏为负 |
| 19 | 本期下单数量 下单数量：下单后出库或领料时扣减的库存数，含已收费、已退费两种情况 |
| 20 | 本期退货数量 |
| 21 | 期末库存数量 |
| 22 | {{ obj \| dateformat}}进销存统计报表 |
| 23 | 仓库 |
| 24 | 商品编码 |
| 25 | 条形码 |
| 26 | 商品名称 |
| 27 | 规格 |
| 28 | 生产厂商 |
| 29 | 默认供应商 |
| 30 | 采购供应商 |
| 31 | 单位 |
| 32 | 零售价 |
| 33 | 成本价 |
| 34 | 期初库存数量 |
| 35 | 本期入库数量 |
| 36 | 本期出库数量 |
| 37 | 本期盘点数量 盘点数量：盘点时增减的库存数，盘盈为正，盘亏为负 |
| 38 | 本期下单数量 下单数量：下单后出库或领料时扣减的库存数，含已收费、已退费两种情况 |
| 39 | 本期退货数量 |
| 40 | 期末库存数量 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `hasTransaction` |
| `obj.factoryKeyword` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.batchNoKeyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDataList.count` |
| `hasAuth` |
| `VIEW_COST_PRICE` |
| `obj` |
| `dateformat` |
| `getDataList.total.beforeExistCount` |
| `getDataList.total.inCount` |
| `getDataList.total.outCount` |
| `getDataList.total.takingCount` |
| `getDataList.total.orderCount` |
| `getDataList.total.refundCount` |
| `getDataList.total.afterExistCount` |
| `item.stockInSkuVo.storehouse.name` |
| `item.stockInSkuVo.product.productCode` |
| `item.stockInSkuVo.productSku.skuCode` |
| `item.stockInSkuVo.product.productName` |
| `item.stockInSkuVo.product.model1Name` |
| `item.stockInSkuVo.productSku.model1` |
| `item.stockInSkuVo.product.model2Name` |
| `item.stockInSkuVo.productSku.model2` |
| `item.stockInSkuVo.product.factory` |
| `item.stockInSkuVo.mainSupplier.supplierName` |
| `item.stockInSkuVo.supplier.supplierName` |
| `item.stockInSkuVo.productSku.unitName` |
| `item.stockInSkuVo.productSku.marketPrice` |
| `item.stockInSkuVo.productSku.costPrice` |
| `item.stockInSkuVo.stockInSku.batchNo` |
| `item.stockInSkuVo.stockInSku.expiresDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockInSkuDataLine.beforeExistCount` |
| `item.stockInSkuDataLine.inCount` |
| `item.stockInSkuDataLine.outCount` |
| `item.stockInSkuDataLine.takingCount` |
| `item.stockInSkuDataLine.orderCount` |
| `item.stockInSkuDataLine.refundCount` |
| `item.stockInSkuDataLine.afterExistCount` |
| `item.storehouse.name` |
| `item.productSkuVo.product.productCode` |
| `item.productSkuVo.productSku.skuCode` |
| `item.productSkuVo.product.productName` |
| `item.productSkuVo.product.model1Name` |
| `item.productSkuVo.productSku.model1` |
| `item.productSkuVo.product.model2Name` |
| `item.productSkuVo.productSku.model2` |
| `item.productSkuVo.product.factory` |
| `item.productSkuVo.mainSupplier.supplierName` |
| `item.productSkuVo.productSku.unitName` |
| `item.productSkuVo.productSku.marketPrice` |
| `item.productSkuVo.productSku.costPrice` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `open1()` |
| `open2()` |
| `selectId()` |
| `downloadModal=false` |
| `daochujxc()` |
| `daochujxcProduct()` |

### 8.13 `report.reportSale.machineProcessList`

- **URL**：`/machineProcessList`
- **模板**：`views/reportMedical/machineProcessList.html`
- **控制器**：`machineProcessListCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectCustomerPointVoList` | `POST /admin/selectCustomerPointVoList.json` |
| `selectMachineCenterOrderRecordVoList` | `POST /admin/selectMachineCenterOrderRecordVoList.json` |
| `selectMachineCenterVoList` | `POST /admin/selectMachineCenterVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ dateFilter \| dateformat}}加工流水报表 |
| 2 | 姓名 |
| 3 | 档案号 |
| 4 | 接诊人 |
| 5 | 开单门店 |
| 6 | 加工中心 |
| 7 | 完成人 |
| 8 | 完成时间 |
| 9 | 产品名称 |
| 10 | 规格 |
| 11 | 生产厂商 |
| 12 | 默认供应商 |
| 13 | 单位 |
| 14 | 数量 |
| 15 | 费用合计 |
| 16 | 加工状态 |
| 17 | 签收状态 签收是指镜片加工完成，店员签收 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.keyword` |
| `obj.productKeyword` |
| `obj.completeKeyword` |
| `obj.machineCenterId` |
| `pageSize` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `modelName.machineCenter.id` |
| `modelName.machineCenter.name` |
| `dateFilter` |
| `dateformat` |
| `getDataList.total.deliveryCount` |
| `getDataList.total.totalFee` |
| `item.patient.patientName` |
| `item.medicalRecord.medicalCode` |
| `item.medicalRecord.doctorName` |
| `item.company.companyName` |
| `item.machineCenter.name` |
| `item.completeAdmin.nickname` |
| `item.machineCenterOrder.completeTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.medicalProduct.unitName` |
| `item.medicalProductDeliveryCount` |
| `item.medicalProduct.marketPrice` |
| `getDataList.count` |
| `pageIndex` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `downloadModal=false` |
| `daochu()` |

### 8.14 `materialStatistic`

- **URL**：`/materialStatistic`
- **模板**：`views/reportMedical/materialStatistic.html`
- **控制器**：`reportSaleCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.15 `medicalStatistic`

- **URL**：`/medicalStatistic`
- **模板**：`views/reportMedical/medicalStatistic.html`
- **控制器**：`reportMedicalRateCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.16 `materialStatistic.myDeliveryRecord`

- **URL**：`/myDeliveryRecord`
- **模板**：`views/reportMedical/myDeliveryRecord.html`
- **控制器**：`myDeliveryRecordCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.17 `materialStatistic.myJxcRecord`

- **URL**：`/myJxcRecord`
- **模板**：`views/reportMedical/myJxcRecord.html`
- **控制器**：`myJxcRecordCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.18 `materialStatistic.myReceiptRecord`

- **URL**：`/myReceiptRecord`
- **模板**：`views/reportMedical/myReceiptRecord.html`
- **控制器**：`myReceiptRecordCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 8.19 `report.reportFee.pointsListCharge`

- **URL**：`/pointsListCharge`
- **模板**：`views/reportMedical/pointsListCharge.html`
- **控制器**：`pointsListChargeCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 只显示有积分用户 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 积分余额统计 |
| 2 | 会员姓名 |
| 3 | 手机号 |
| 4 | 积分 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `hasPoint` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `orderListFactory.total.pointBalance` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerPoint.point` |

### 8.20 `report.reportFee.pointsListReCharge`

- **URL**：`/pointsListReCharge`
- **模板**：`views/reportMedical/pointsListReCharge.html`
- **控制器**：`pointsListReChargeCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerPointLogVoList` | `POST /admin/selectCustomerPointLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}} 挂账 积分报表 |
| 2 | 操作时间 |
| 3 | 姓名 |
| 4 | 手机号 |
| 5 | 操作类型 |
| 6 | 积分 |
| 7 | 备注 |
| 8 | 操作人员 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `logListFactory.total.addPoint` |
| `item.customerPointLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerPointLog.channelType` |
| `pointChannel` |
| `item.customerPointLog.addPoint` |
| `item.customerPointLog.remark` |
| `item.customerPointLog.casherName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(0)` |
| `setTab(1)` |

### 8.21 `profitReport`

- **URL**：`/profitReport`
- **模板**：`views/reportMedical/profitReport.html`
- **控制器**：`profitReportCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectProductSkuSalesDataList` | `POST /admin/selectProductSkuSalesDataList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}利润报表 |
| 2 | 产品名称 |
| 3 | 类目名称 |
| 4 | 品牌名称 |
| 5 | 规格 |
| 6 | 生产厂商 |
| 7 | 默认供应商 |
| 8 | 销量 报表在产品下单后统计销量 |
| 9 | 退货 |
| 10 | 合计 |
| 11 | 费用合计 |
| 12 | 业绩 业绩为优惠分摊后的金额 ，业绩 = 折后金额-减免分摊-积分分摊-赠金分摊 |
| 13 | 预计成本 |
| 14 | 进货成本 进货成本 = 每次进货的成本单价 * 该批次下的扣减数量 每次进货的成本单价和系统设置里的成本单价不一样 |
| 15 | 利润 |
| 16 | 门店名称 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.productStatType` |
| `obj.companyId` |
| `obj.companyStatType` |
| `pageSize` |
| `obj.keyword` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `hospital.id` |
| `hospital.companyName` |
| `calcColspan` |
| `obj` |
| `dateformat` |
| `getDataList.total.useCount` |
| `getDataList.total.returnUseCount` |
| `getDataList.total.remainUseCount` |
| `getDataList.total.remainTotalFee` |
| `getDataList.total.remainPerformance` |
| `toFixed` |
| `getDataList.total.remainDefaultTotalCostPrice` |
| `getDataList.total.remainTotalCostPrice` |
| `getDataList.total.remainProfit` |
| `item.product.productName` |
| `item.category.categoryName` |
| `item.brand.brandName` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.useCount` |
| `item.returnUseCount` |
| `item.remainUseCount` |
| `item.remainTotalFee` |
| `item.remainPerformance` |
| `item.remainDefaultTotalCostPrice` |
| `item.remainTotalCostPrice` |
| `item.remainProfit` |
| `item.company.companyName` |
| `getDataList.count` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `downloadModal=true` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`profitReport`, `stockInReport`

### 8.22 `report.reportMaterial.receiptRecord`

- **URL**：`/receiptRecord`
- **模板**：`views/reportMedical/receiptRecord.html`
- **控制器**：`receiptRecordCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getStockInSkuDataList` | `POST /admin/getStockInSkuDataList.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}入库流水报表 |
| 2 | 仓库 |
| 3 | 入库日期 |
| 4 | 入库单号 |
| 5 | 入库类型 |
| 6 | 入库人员 |
| 7 | 商品编码/ 条形码 |
| 8 | 商品名称 |
| 9 | 规格 |
| 10 | 生产厂商 |
| 11 | 默认供应商 |
| 12 | 采购供应商 |
| 13 | 数量 |
| 14 | 单位 |
| 15 | 零售价 |
| 16 | 成本价 |
| 17 | 成本合计 |
| 18 | 批号 |
| 19 | 有效期 |
| 20 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.factoryKeyword` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.batchNoKeyword` |
| `obj.inType` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDataList.count` |
| `hasAuth` |
| `VIEW_COST_PRICE` |
| `obj` |
| `dateformat` |
| `getDataList.total.skuCount` |
| `getDataList.total.skuTotalPrice` |
| `item.storehouse.name` |
| `item.stockIn.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockIn.id` |
| `item.stockIn.inType` |
| `inType` |
| `item.stockIn.createName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.productName` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.supplier.supplierName` |
| `item.stockInSku.skuCount` |
| `item.productSku.unitName` |
| `item.productSku.marketPrice` |
| `item.stockInSku.skuPrice` |
| `item.stockInSku.skuTotalPrice` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockIn.remark` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `selectId()` |
| `downloadModal=false` |
| `daochu()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
```

### 8.23 `report.reportFee.refundFee`

- **URL**：`/refundFee`
- **模板**：`views/reportMedical/refundFee.html`
- **控制器**：`refundFeeCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getSchoolVoList` | `POST /admin/getSchoolVoList.json` |
| `selectCashflowRefundFeeVoList` | `POST /admin/selectCashflowRefundFeeVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ data \| dateformatter}}退费流水报表 |
| 2 | 姓名 |
| 3 | 档案号 |
| 4 | 费用合计 |
| 5 | 折后金额 |
| 6 | 扣减作废 |
| 7 | 现金退回 |
| 8 | 银行卡记账退回 |
| 9 | 微信记账退回 |
| 10 | 支付宝记账退回 |
| 11 | POS机刷卡退回 |
| 12 | 微信扫码退回 |
| 13 | 支付宝扫码退回 |
| 14 | 医保退回 |
| 15 | 挂账退回 |
| 16 | 商保退回 |
| 17 | 余额支付退回 |
| 18 | 积分支付退回 |
| 19 | {{otherPay.channelName1}}退回 |
| 20 | {{otherPay.channelName2}}退回 |
| 21 | {{otherPay.channelName3}}退回 |
| 22 | {{otherPay.channelName4}}退回 |
| 23 | {{otherPay.channelName5}}退回 |
| 24 | 学校 |
| 25 | 退费信息 |
| 26 | 接诊{{corpInfo.employeeTitle}} |
| 27 | 查看 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `adminConf.schoolEnable` |
| `data` |
| `dateformatter` |
| `otherPay.channelName1` |
| `otherPay.channelName2` |
| `otherPay.channelName3` |
| `otherPay.channelName4` |
| `otherPay.channelName5` |
| `corpInfo.employeeTitle` |
| `EmployeeList.total.totalFee` |
| `EmployeeList.total.totalPayment` |
| `EmployeeList.total.substractFee` |
| `EmployeeList.total.refundFromCash` |
| `EmployeeList.total.refundFromBankcard` |
| `EmployeeList.total.refundFromWechat` |
| `EmployeeList.total.refundFromAlipay` |
| `EmployeeList.total.refundFromPOS` |
| `EmployeeList.total.refundFromWechatScan` |
| `EmployeeList.total.refundFromAlipayScan` |
| `EmployeeList.total.refundFromMedical` |
| `EmployeeList.total.refundFromCreditRollback` |
| `EmployeeList.total.refundFromCommercial` |
| `EmployeeList.total.refundFromWallet` |
| `EmployeeList.total.refundFromPoint` |
| `EmployeeList.total.refundFromPayChannel1` |
| `EmployeeList.total.refundFromPayChannel2` |
| `EmployeeList.total.refundFromPayChannel3` |
| `EmployeeList.total.refundFromPayChannel4` |
| `EmployeeList.total.refundFromPayChannel5` |
| `item.feeDataList.length` |
| `item.patient.patientName` |
| `item.medicalRecord.medicalCode` |
| `item.cashflow.totalFee` |
| `item.cashflow.totalPayment` |
| `item.cashflow.substractFee` |
| `item.refundFromCash` |
| `item.refundFromBankcard` |
| `item.refundFromWechat` |
| `item.refundFromAlipay` |
| `item.refundFromPOS` |
| `item.refundFromWechatScan` |
| `item.refundFromAlipayScan` |
| `item.refundFromMedical` |
| `item.refundFromCreditRollback` |
| `item.refundFromCommercial` |
| `item.refundFromWallet` |
| `item.refundFromPoint` |
| `item.refundFromPayChannel1` |
| `item.refundFromPayChannel2` |
| `item.refundFromPayChannel3` |
| `item.refundFromPayChannel4` |
| `item.refundFromPayChannel5` |
| `item.school.schoolName` |
| `item.casherName` |
| `item.refundTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecord.doctorName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goDetail(item)` |

### 8.24 `report`

- **URL**：`/report`
- **模板**：`views/reportMedical/report.html`
- **控制器**：`reportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.children` |
| `corpAdminHome.state` |
| `iten.corpAdminHome.stateName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab($index,iten)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setTab(4)` |
| `setTab(5)` |

**跳转到**：`report.reportFee.feeDay`, `report.reportMaterial.receiptRecord`, `report.reportMedicalRate.successRate`, `report.reportOperateAll.reportOperate`, `report.reportSale.saleRecord`

### 8.25 `report.reportFee`

- **URL**：`/reportFee`
- **模板**：`views/reportMedical/reportFee.html`
- **控制器**：`reportFeeCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

**跳转到**：`report.reportFee.feeBankCard`, `report.reportFee.feeDay`, `report.reportFee.feeMonth`, `report.reportFee.feeRecharge`, `report.reportFee.pointsListCharge`, `report.reportFee.pointsListReCharge`, `report.reportFee.refundFee`, `report.reportFee.unPayCharge`, `report.reportFee.unPayRecharge`

### 8.26 `report.reportMaterial`

- **URL**：`/reportMaterial`
- **模板**：`views/reportMedical/reportMaterial.html`
- **控制器**：`reportSaleCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

**跳转到**：`report.reportMaterial.deliveryRecordPort`, `report.reportMaterial.jxcRecord`, `report.reportMaterial.receiptRecord`

### 8.27 `report.reportMedicalRate`

- **URL**：`/reportMedicalRate`
- **模板**：`views/reportMedical/reportMedicalRate.html`
- **控制器**：`reportMedicalRateCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

**跳转到**：`report.reportMedicalRate.customerChannelRate`, `report.reportMedicalRate.satisfyDetailRate`, `report.reportMedicalRate.satisfyRate`, `report.reportMedicalRate.successRate`

### 8.28 `report.reportOperateAll.reportOperate`

- **URL**：`/reportOperate`
- **模板**：`views/reportMedical/reportOperate.html`
- **控制器**：`reportOperateCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCustomerDataBetween` | `POST /admin/getCustomerDataBetween.json` |
| `getOkSalesDataBetween` | `POST /admin/getOkSalesDataBetween.json` |
| `getYmOkSalesDataList` | `POST /admin/getYmOkSalesDataList.json` |
| `selectCustomerCreditLogVoList` | `POST /admin/selectCustomerCreditLogVoList.json` |
| `selectCustomerCreditVoList` | `POST /admin/selectCustomerCreditVoList.json` |
| `statCustomerWalletAndTrainerCard` | `POST /admin/statCustomerWalletAndTrainerCard.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{year}}年整体统计报表 |
| 2 | 日期 |
| 3 | 会员数 |
| 4 | 病历数 |
| 5 | 接待患者人数 |
| 6 | 收费 收费 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码 |
| 7 | 充卡 会员卡充值为本金金额，不包含赠送金额 |
| 8 | 挂账还款 挂账后收回的欠款 |
| 9 | 挂账退款 挂账还款后再退款 特殊说明：2022.09.01之前的挂账退款数据合并在退费里统计，之后单独对其进行统计 |
| 10 | 验配数 |
| 11 | 成交率 |
| 12 | 验配销售额 |
| 13 | 二次销售额 |
| 14 | 总销售额 |
| 15 | 总销售额（已缴） |
| 16 | 退费 |
| 17 | 退卡 |
| 18 | 缴费合计 缴费合计 = 收费 + 充卡 + 挂账还款 - 挂账退款 - 退费 - 退卡 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `orderObjectFactory.object.medicalRecordCount` |
| `orderObjectFactory.object.medicalRecordPatientCount` |
| `customerObjectFactory.object.customerCount` |
| `totalOrderObjectFactory.object.medicalRecordCount` |
| `totalOrderObjectFactory.object.medicalRecordPatientCount` |
| `totalCustomerObjectFactory.object.customerCount` |
| `orderObjectFactory.object.cashflowReceivedFromCashier` |
| `orderObjectFactory.object.customerWalletAddTrueMoney` |
| `totalOrderObjectFactory.object.customerWalletAddTrueMoney` |
| `statCustomerWalletAndTrainerCard.object.trueBalance` |
| `statCustomerWalletAndTrainerCard.object.giftBalance` |
| `creditVoList.total.creditBalance` |
| `item` |
| `year` |
| `item.statDate` |
| `date` |
| `yyyy` |
| `MM` |
| `item.customerCount` |
| `item.medicalRecordCount` |
| `item.medicalRecordPatientCount` |
| `item.cashflowReceivedFromCashier` |
| `item.customerWalletAddTrueMoney` |
| `item.okOrderCount` |
| `item.okOrderRate` |
| `percent` |
| `item.okFittingTotalMoney` |
| `item.okReviewTotalMoney` |
| `item.okFittingPayedMoney` |
| `item.okReviewPayedMoney` |
| `item.creditPayment` |
| `item.creditRefund` |
| `item.refundFee` |
| `item.refundCard` |
| `item.cashflowTotal` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setDate(item,$index)` |
| `daochu()` |

### 8.29 `report.reportOperateAll`

- **URL**：`/reportOperateAll`
- **模板**：`views/reportMedical/reportOperateAll.html`
- **控制器**：`reportOperateAllCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

**跳转到**：`report.reportOperateAll.feeCashier`, `report.reportOperateAll.hospitalReport`, `report.reportOperateAll.reportOperate`, `report.reportOperateAll.singleHospitalProfit`, `reportOperateAll.reportMedicalReviewRate`

### 8.30 `report.reportSale`

- **URL**：`/reportSale`
- **模板**：`views/reportMedical/reportSale.html`
- **控制器**：`reportSaleCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

**跳转到**：`report.reportSale.backGoodRecord`, `report.reportSale.deliveryList`, `report.reportSale.machineProcessList`, `report.reportSale.saleList`, `report.reportSale.saleRecord`

### 8.31 `report.reportSale.saleList`

- **URL**：`/saleList`
- **模板**：`views/reportMedical/saleList.html`
- **控制器**：`saleListCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectProductSkuSalesDataList` | `POST /admin/selectProductSkuSalesDataList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}产品销量报表 |
| 2 | 产品名称 类目名称 品牌名称 |
| 3 | 规格 |
| 4 | 生产厂商 |
| 5 | 默认供应商 |
| 6 | 销量 报表在产品下单后统计销量 |
| 7 | 退货 |
| 8 | 合计 |
| 9 | 费用合计 |
| 10 | 业绩 业绩为优惠分摊后的金额 ，业绩 = 折后金额-减免分摊-积分分摊-赠金分摊 |
| 11 | 门店名称 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.keyword` |
| `obj.productStatType` |
| `obj.companyStatType` |
| `pageSize` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `calcColspan` |
| `obj` |
| `dateformat` |
| `getDataList.total.useCount` |
| `getDataList.total.returnUseCount` |
| `getDataList.total.remainUseCount` |
| `getDataList.total.remainTotalFee` |
| `getDataList.total.remainPerformance` |
| `toFixed` |
| `item.product.productName` |
| `item.category.categoryName` |
| `item.brand.brandName` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.mainSupplier.supplierName` |
| `item.useCount` |
| `item.returnUseCount` |
| `item.remainUseCount` |
| `item.remainTotalFee` |
| `item.remainPerformance` |
| `item.company.companyName` |
| `getDataList.count` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `downloadModal=true` |
| `downloadModal=false` |
| `daochu()` |

### 8.32 `report.reportSale.saleRecord`

- **URL**：`/saleRecord`
- **模板**：`views/reportMedical/saleRecord.html`
- **控制器**：`saleRecordCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectMedicalProductSalesVoList` | `POST /admin/selectMedicalProductSalesVoList.json` |

**表单标签**

| 标签 |
|---|
| 不含退货 |
| 不含部分退货 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}销售流水报表 |
| 2 | 收费时间 |
| 3 | {{corpInfo.companyTitle}} |
| 4 | 单次推荐人 |
| 5 | 接诊人 |
| 6 | 验配师 |
| 7 | 会员推荐人 |
| 8 | 成交人 |
| 9 | 维护人 |
| 10 | 患者 |
| 11 | 会员 |
| 12 | 类目 |
| 13 | 品牌 |
| 14 | 产品编码/ 条形码 |
| 15 | 产品名称 |
| 16 | 规格 |
| 17 | 生产厂商 |
| 18 | 默认供应商 |
| 19 | 默认成本 |
| 20 | 下单数量 |
| 21 | 退货数量 |
| 22 | 销售数量 |
| 23 | 费用合计 |
| 24 | 业绩 业绩为优惠分摊后的金额 ，业绩 = 折后金额-减免分摊-积分分摊-赠金分摊 |
| 25 | 优惠金额 优惠金额 = 费用合计 - 业绩 |
| 26 | 优惠率 优惠率 = 优惠金额 ÷ 费用合计 |
| 27 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `refundStatusArray[0]` |
| `refundStatusArray[1]` |
| `pageSize` |
| `obj.firstDoctorName` |
| `obj.doctorName` |
| `obj.secondDoctorName` |
| `obj.keyword` |
| `obj.factoryKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `firstDoctor.name` |
| `firstDoctor.tip` |
| `Patienter.name` |
| `Patienter.tip` |
| `Opticianer.name` |
| `Opticianer.tip` |
| `Referrer.name` |
| `Referrer.tip` |
| `Transactor.name` |
| `Transactor.tip` |
| `Maintainer.name` |
| `Maintainer.tip` |
| `corpInfo.employeeTitle` |
| `hasAuth` |
| `VIEW_COST_PRICE` |
| `obj` |
| `dateformat` |
| `corpInfo.companyTitle` |
| `getDataList.total.useCount` |
| `getDataList.total.returnUseCount` |
| `getDataList.total.remainUseCount` |
| `getDataList.total.remainTotalFee` |
| `getDataList.total.remainPerformance` |
| `toFixed` |
| `getDataList.total.preferentialFee` |
| `getDataList.total.preferentialRate` |
| `toFixedzero` |
| `item.medicalProduct.payedTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecordVo.medicalRecord.hospitalName` |
| `item.medicalRecordVo.medicalRecord.firstDoctorName` |
| `item.medicalRecordVo.medicalRecord.doctorName` |
| `item.medicalRecordVo.medicalRecord.secondDoctorName` |
| `item.medicalRecordVo.introducer.name` |
| `item.medicalRecordVo.dealdoneEmployee.employeeName` |
| `item.medicalRecordVo.serviceEmployee.employeeName` |
| `item.medicalRecordVo.patient.patientName` |
| `item.medicalRecordVo.customer.customerName` |
| `item.productSkuVo.category.categoryName` |
| `item.productSkuVo.brand.brandName` |
| `item.productSkuVo.product.productCode` |
| `item.medicalProduct.skuCode` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.productSkuVo.product.factory` |
| `item.productSkuVo.mainSupplier.supplierName` |
| `item.productSkuVo.productSku.costPrice` |
| `item.salesData.useCount` |
| `item.salesData.returnUseCount` |
| `item.salesData.remainUseCount` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.marketPrice` |
| `item.salesData.remainTotalFee` |
| `item.salesData.remainPerformance` |
| `item.salesData.preferentialFee` |
| `item.salesData.preferentialRate` |
| `item.medicalProduct.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `showDaochu($event)` |
| `firstDoctor.show = true` |
| `firstDoctor.close($event)` |
| `Patienter.show = true` |
| `Patienter.close($event)` |
| `Opticianer.show = true` |
| `Opticianer.close($event)` |
| `Referrer.show = true` |
| `Referrer.close($event)` |
| `Transactor.show = true` |
| `Transactor.close($event)` |
| `Maintainer.show = true` |
| `Maintainer.close($event)` |

### 8.33 `report.reportMedicalRate.satisfyDetailRate`

- **URL**：`/satisfyDetailRate`
- **模板**：`views/reportMedical/satisfyDetailRate.html`
- **控制器**：`satisfyDetailRateCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCommentEmployeeVoList` | `POST /admin/selectCommentEmployeeVoList.json` |
| `statCommentEmployee` | `POST /admin/statCommentEmployee.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}满意度统计报表 |
| 2 | 接诊{{corpInfo.employeeTitle}} |
| 3 | 不满意 |
| 4 | 满意 |
| 5 | 非常满意 |
| 6 | 满意度 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `corpInfo.employeeTitle` |
| `item.employeeName` |
| `item.score1Count` |
| `item.score3Count` |
| `item.score5Count` |
| `item.satisfyPercent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

### 8.34 `report.reportMedicalRate.satisfyRate`

- **URL**：`/satisfyRate`
- **模板**：`views/reportMedical/satisfyRate.html`
- **控制器**：`satisfyRateCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 接诊{{corpInfo.employeeTitle}}评价流水报表 |
| 2 | 评价时间 |
| 3 | {{corpInfo.employeeTitle}}名称 |
| 4 | 客户名称 |
| 5 | 客户评论 |
| 6 | 评论标签 |
| 7 | 满意度 |
| 8 | 类型 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.commentScore` |
| `obj.employeeName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
| `item.commentEmployee.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.employee.employeeName` |
| `item.customer.customerName` |
| `item.commentEmployee.commentText` |
| `item.commentEmployee.commentTags` |
| `item.commentEmployee.commentScore` |
| `commentScore` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(null)` |
| `setTab(1)` |
| `setTab(3)` |
| `setTab(5)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 8.35 `report.reportOperateAll.singleHospitalProfit`

- **URL**：`/singleHospitalProfit`
- **模板**：`views/reportMedical/singleHospitalProfit.html`
- **控制器**：`singleHospitalProfitCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanySalesDataList` | `POST /admin/getCompanySalesDataList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}分店报表 |
| 2 | 分店名称 |
| 3 | 病历数 |
| 4 | 接待患者人数 |
| 5 | 收费 收费 = 现金 + 银行卡记账 + 微信记账 + 支付宝记账 + POS机刷卡 + 微信扫码 + 支付宝扫码 |
| 6 | 充卡 充卡为本金金额，不包含赠送金额 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，显示为0 |
| 7 | 挂账还款 挂账后收回的欠款 特殊说明：2019.04.15之前的数据未做分{{corpInfo. companyTitle}}统计，显示为0 |
| 8 | 挂账退款 挂账还款后再退款 特殊说明：2022.09.01之前的挂账退款数据合并在退费里统计，之后单独对其进行统计 |
| 9 | 退费 |
| 10 | 退卡 |
| 11 | 缴费合计 缴费合计 = 收费 + 会员卡充值 + 挂账还款 - 挂账退款 - 退费 - 退卡 特殊说明：2019.04.15之前的数据未做会员卡充值和挂账还款的分{{corpInfo. companyTitle}}统计，相应项目显示为0。 |
| 12 | 验配数 |
| 13 | 成交率 |
| 14 | 验配销售额 |
| 15 | 二次销售额 |
| 16 | 总销售额 |
| 17 | 总销售额（已缴） |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `corpInfo.` |
| `companyTitle` |
| `EmployeeList.total.medicalRecordCount` |
| `EmployeeList.total.medicalRecordPatientCount` |
| `EmployeeList.total.cashflowReceivedFromCashier` |
| `EmployeeList.total.customerWalletAddTrueMoney` |
| `EmployeeList.total.creditPayment` |
| `EmployeeList.total.creditRefund` |
| `EmployeeList.total.refundFee` |
| `EmployeeList.total.refundCard` |
| `EmployeeList.total.cashflowTotal` |
| `item.companyName` |
| `item.medicalRecordCount` |
| `item.medicalRecordPatientCount` |
| `item.cashflowReceivedFromCashier` |
| `item.customerWalletAddTrueMoney` |
| `item.creditPayment` |
| `item.creditRefund` |
| `item.refundFee` |
| `item.refundCard` |
| `item.cashflowTotal` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

### 8.36 `stockInReport`

- **URL**：`/stockInReport`
- **模板**：`views/reportMedical/stockInReport.html`
- **控制器**：`jxcRecordCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectStockInSkuDataVoList` | `POST /admin/selectStockInSkuDataVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 按商品 按批号 本期库存有变动 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}成本报表 |
| 2 | 仓库 |
| 3 | 商品编码 |
| 4 | 条形码 |
| 5 | 商品名称 |
| 6 | 规格 |
| 7 | 生产厂商 |
| 8 | 默认供应商 |
| 9 | 单位 |
| 10 | 零售价 |
| 11 | 期初库存 |
| 12 | 本期入库 |
| 13 | 本期出库 |
| 14 | 本期盘点 |
| 15 | 本期下单 |
| 16 | 本期退货 |
| 17 | 期末库存 |
| 18 | 数量 |
| 19 | 成本 |
| 20 | 数量 |
| 21 | 成本 |
| 22 | 数量 |
| 23 | 成本 |
| 24 | 数量 盘点数量：盘点时增减的库存数，盘盈为正，盘亏为负 |
| 25 | 成本 |
| 26 | 数量 下单数量：下单后出库或领料时扣减的库存数，含已收费、已退费两种情况 |
| 27 | 成本 |
| 28 | 数量 |
| 29 | 成本 |
| 30 | 数量 |
| 31 | 成本 |
| 32 | {{ obj \| dateformat}}成本报表 |
| 33 | 仓库 |
| 34 | 商品编码 |
| 35 | 条形码 |
| 36 | 商品名称 |
| 37 | 规格 |
| 38 | 生产厂商 |
| 39 | 默认供应商 |
| 40 | 采购供应商 |
| 41 | 单位 |
| 42 | 零售价 |
| 43 | 批号 |
| 44 | 有效期 |
| 45 | 成本价 |
| 46 | 期初库存 |
| 47 | 本期入库 |
| 48 | 本期出库 |
| 49 | 本期盘点 |
| 50 | 本期下单 |
| 51 | 本期退货 |
| 52 | 期末库存 |
| 53 | 数量 |
| 54 | 成本 |
| 55 | 数量 |
| 56 | 成本 |
| 57 | 数量 |
| 58 | 成本 |
| 59 | 数量 盘点数量：盘点时增减的库存数，盘盈为正，盘亏为负 |
| 60 | 成本 |
| 61 | 数量 下单数量：下单后出库或领料时扣减的库存数，含已收费、已退费两种情况 |
| 62 | 成本 |
| 63 | 数量 |
| 64 | 成本 |
| 65 | 数量 |
| 66 | 成本 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `hasTransaction` |
| `obj.storehouseId` |
| `obj.factoryKeyword` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.batchNoKeyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDataList.count` |
| `obj` |
| `dateformat` |
| `getDataList.total.beforeExistCount` |
| `getDataList.total.beforeExistCostPrice` |
| `getDataList.total.inCount` |
| `getDataList.total.inCostPrice` |
| `getDataList.total.outCount` |
| `getDataList.total.outCostPrice` |
| `getDataList.total.takingCount` |
| `getDataList.total.takingCostPrice` |
| `getDataList.total.orderCount` |
| `getDataList.total.orderCostPrice` |
| `getDataList.total.refundCount` |
| `getDataList.total.refundCostPrice` |
| `getDataList.total.afterExistCount` |
| `getDataList.total.afterExistCostPrice` |
| `item.storehouse.name` |
| `item.productSkuVo.product.productCode` |
| `item.productSkuVo.productSku.skuCode` |
| `item.productSkuVo.product.productName` |
| `item.productSkuVo.product.model1Name` |
| `item.productSkuVo.productSku.model1` |
| `item.productSkuVo.product.model2Name` |
| `item.productSkuVo.productSku.model2` |
| `item.productSkuVo.product.factory` |
| `item.productSkuVo.mainSupplier.supplierName` |
| `item.productSkuVo.productSku.unitName` |
| `item.productSkuVo.productSku.marketPrice` |
| `item.stockInSkuDataLine.beforeExistCount` |
| `item.stockInSkuDataLine.beforeExistCostPrice` |
| `item.stockInSkuDataLine.inCount` |
| `item.stockInSkuDataLine.inCostPrice` |
| `item.stockInSkuDataLine.outCount` |
| `item.stockInSkuDataLine.outCostPrice` |
| `item.stockInSkuDataLine.takingCount` |
| `item.stockInSkuDataLine.takingCostPrice` |
| `item.stockInSkuDataLine.orderCount` |
| `item.stockInSkuDataLine.orderCostPrice` |
| `item.stockInSkuDataLine.refundCount` |
| `item.stockInSkuDataLine.refundCostPrice` |
| `item.stockInSkuDataLine.afterExistCount` |
| `item.stockInSkuDataLine.afterExistCostPrice` |
| `item.stockInSkuVo.storehouse.name` |
| `item.stockInSkuVo.product.productCode` |
| `item.stockInSkuVo.productSku.skuCode` |
| `item.stockInSkuVo.product.productName` |
| `item.stockInSkuVo.product.model1Name` |
| `item.stockInSkuVo.productSku.model1` |
| `item.stockInSkuVo.product.model2Name` |
| `item.stockInSkuVo.productSku.model2` |
| `item.stockInSkuVo.product.factory` |
| `item.stockInSkuVo.mainSupplier.supplierName` |
| `item.stockInSkuVo.supplier.supplierName` |
| `item.stockInSkuVo.productSku.unitName` |
| `item.stockInSkuVo.productSku.marketPrice` |
| `item.stockInSkuVo.stockInSku.batchNo` |
| `item.stockInSkuVo.stockInSku.expiresDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockInSkuVo.stockInSku.skuPrice` |
| `downloadIndex` |
| `pageSize` |
| `getDataList.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `open1()` |
| `open2()` |
| `selectId()` |
| `downloadModal=false` |
| `daochu()` |
| `daochuProduct()` |

**跳转到**：`profitReport`, `stockInReport`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 8.37 `report.reportMedicalRate.successRate`

- **URL**：`/successRate`
- **模板**：`views/reportMedical/successRate.html`
- **控制器**：`successRateCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectMedicalProductKpiDataListOfEmployee` | `POST /admin/selectMedicalProductKpiDataListOfEmployee.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}}成交率统计报表 |
| 2 | 分类 |
| 3 | {{defineList[defineIndex].name}} |
| 4 | 病历数 |
| 5 | 接待患者人数 |
| 6 | 缴费金额 缴费金额 = 现金 + 银行卡 + 微信记账 + 支付宝记账 + 微信扫码 + 支付宝扫码，不计退费 |
| 7 | 绩效金额 |
| 8 | 操作 |
| 9 | 时间 |
| 10 | 产品 |
| 11 | 规格 |
| 12 | 绩效金额 |
| 13 | 数量 |
| 14 | 绩效合计 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
| `d.name` |
| `defineList` |
| `defineIndex` |
| `colspan` |
| `obj` |
| `dateformat` |
| `name` |
| `d.rowspan` |
| `d.colspan` |
| `d.value` |
| `item.statDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.name` |
| `item.model1` |
| `item.model2` |
| `item.kpiPrice` |
| `item.kpiCount` |
| `item.totalKpiPrice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `daochu()` |
| `searchEmployeeRank(1)` |
| `setDefineIndex($index)` |
| `searchEmployeeRank(3)` |
| `PerformanceDetail.open(d.id)` |
| `PerformanceDetail.affrim()` |
| `PerformanceDetail.close()` |

### 8.38 `report.reportFee.timeCardRecharge`

- **URL**：`/timeCardRecharge`
- **模板**：`views/reportMedical/timeCardRecharge.html`
- **控制器**：`timeCardRechargeCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerCreditVoList` | `POST /admin/selectCustomerCreditVoList.json` |
| `selectCustomerTrainerCardVoListForDetailReport` | `POST /admin/selectCustomerTrainerCardVoListForDetailReport.json` |

**表单标签**

| 标签 |
|---|
| 充值 |
| 消费 |
| 退卡 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}} 充值 消费 退卡 流水报表 |
| 2 | 操作时间 |
| 3 | {{corpInfo.companyTitle}} |
| 4 | 用户 |
| 5 | 手机号 |
| 6 | 次卡名称 |
| 7 | 售价 |
| 8 | 次数（总数） |
| 9 | 扣除数量 |
| 10 | 剩余数量 |
| 11 | 退还次数 |
| 12 | 退款金额 |
| 13 | 退卡原因 |
| 14 | 有效期 |
| 15 | 备注 |
| 16 | 操作员工 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.logType` |
| `obj` |
| `dateformat` |
| `corpInfo.companyTitle` |
| `item.customerTrainerCardLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.company.companyName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.customerTrainerCard.trainerCardName` |
| `item.customerTrainerCard.sourceMoney` |
| `item.customerTrainerCard.sourceNumber` |
| `item.customerTrainerCardLog.addNumber` |
| `item.customerTrainerCardLog.balanceNumber` |
| `item.customerTrainerCardLog.addMoney` |
| `item.customerTrainerCardLog.returnCardReason` |
| `item.customerTrainerCard.validTime` |
| `item.customerTrainerCardLog.remark` |
| `item.casher.nickname` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |

### 8.39 `report.reportFee.timecardBlance`

- **URL**：`/timecardBlance`
- **模板**：`views/reportMedical/timecardBlance.html`
- **控制器**：`timecardBlanceCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectCustomerTrainerCardDataListForStatBalance` | `POST /admin/selectCustomerTrainerCardDataListForStatBalance.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 次卡余额统计 |
| 2 | 用户 |
| 3 | 手机号 |
| 4 | 次卡名称 |
| 5 | 售价 / 次数 |
| 6 | 次卡数 |
| 7 | 剩余金额 |
| 8 | 剩余次数 |
| 9 | 合计 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.classify` |
| `obj.customerKeyword` |
| `obj.trainerCardKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `customerTrainerCardVoList.total.validCardNumbersTotal` |
| `customerTrainerCardVoList.total.balanceMoneyTotal` |
| `customerTrainerCardVoList.total.balanceNumbersTotal` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.validCardNumbersTotal` |
| `item.balanceMoneyTotal` |
| `item.balanceNumbersTotal` |
| `item.trainerCard.trainerCardName` |
| `item.trainerCard.marketPrice` |
| `item.trainerCard.numbers` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTrainerCard()` |

### 8.40 `report.reportFee.timecardPerformance`

- **URL**：`/timecardPerformance`
- **模板**：`views/reportMedical/timecardPerformance.html`
- **控制器**：`timecardPerformanceCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectCustomerTrainerCardDataListForStatGoals` | `POST /admin/selectCustomerTrainerCardDataListForStatGoals.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 次卡业绩统计 |
| 2 | 销售员 |
| 3 | 手机号 |
| 4 | 次卡数 |
| 5 | 售出金额 |
| 6 | 售出次数 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |
| `obj.salesKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `customerTrainerCardVoList.total.allCardNumbersTotal` |
| `customerTrainerCardVoList.total.sourceMoneyTotal` |
| `customerTrainerCardVoList.total.sourceNumbersTotal` |
| `item.sales.employeeName` |
| `item.sales.mobile` |
| `item.allCardNumbersTotal` |
| `item.sourceMoneyTotal` |
| `item.sourceNumbersTotal` |

### 8.41 `report.reportFee.unPayCharge`

- **URL**：`/unPayCharge`
- **模板**：`views/reportMedical/unPayCharge.html`
- **控制器**：`unPayChargeCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 挂账余额统计 |
| 2 | 会员姓名 |
| 3 | 手机号 |
| 4 | 挂账金额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.hasCredit` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `EmployeeList.total.creditBalance` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerCredit.creditBalance` |

### 8.42 `report.reportFee.unPayRecharge`

- **URL**：`/unPayRecharge`
- **模板**：`views/reportMedical/unPayRecharge.html`
- **控制器**：`unPayRechargeCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerCreditLogVoList` | `POST /admin/selectCustomerCreditLogVoList.json` |

**表单标签**

| 标签 |
|---|
| 挂账 |
| 挂账还款 |
| 挂账退款 |
| 挂账取消 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{ obj \| dateformat}} 挂账 流水报表 |
| 2 | {{ obj \| dateformat}} 还款 流水报表 |
| 3 | 操作时间 |
| 4 | 姓名 |
| 5 | 手机号 |
| 6 | 还款渠道 |
| 7 | 操作类型 |
| 8 | 金额 |
| 9 | 备注 |
| 10 | 操作人员 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj` |
| `dateformat` |
| `EmployeeList.total.creditMoney` |
| `item.customerCreditLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerCreditLog.payChannel` |
| `payChannel` |
| `item.customerCreditLog.logType` |
| `unPayRecharge` |
| `item.customerCreditLog.creditMoney` |
| `item.customerCreditLog.remark` |
| `item.customerCreditLog.casherName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(3)` |
| `setTab(2)` |
