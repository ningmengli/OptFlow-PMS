# 06｜模块 chargeAdmin 收费/退费

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/chargeAdmin/` |
| 中文名 | 收费/退费 |
| 开发波次 | W6 |
| 页面数 | **19** |
| 端点数（去重） | **57** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `deliveryInput` | `/deliveryInput?cashflowId` | `views/chargeAdmin/deliveryInput.html` | `deliveryInputCtrl` | 0 |
| 2 | `deliveryInputRecord` | `/deliveryInputRecord?cashflowId` | `views/chargeAdmin/deliveryInputRecord.html` | `deliveryInputRecordCtrl` | 0 |
| 3 | `deliveryList` | `/deliveryList` | `views/chargeAdmin/deliveryList.html` | `deliveryListCtrl` | 5 |
| 4 | `deliveryProcessing` | `/deliveryProcessing?cashflowId` | `views/chargeAdmin/deliveryProcessing.html` | `deliveryProcessingCtrl` | 0 |
| 5 | `machineOrderList` | `/machineOrderList` | `views/chargeAdmin/machineOrderList.html` | `machineOrderListCtrl` | 4 |
| 6 | `partBack` | `/partBack?cashflowId` | `views/chargeAdmin/partBack.html` | `partBackCtrl` | 13 |
| 7 | `payBackDetail` | `/payBackDetail?refundId&refundLogId` | `views/chargeAdmin/payBackDetail.html` | `payBackDetailCtrl` | 0 |
| 8 | `payedDetail` | `/payedDetail?cashflowId` | `views/chargeAdmin/payedDetail.html` | `payedDetailCtrl` | 0 |
| 9 | `payedList` | `/payedList` | `views/chargeAdmin/payedList.html` | `payedListCtrl` | 4 |
| 10 | `reChargeList` | `/reChargeList` | `views/chargeAdmin/reChargeList.html` | `reChargeListCtrl` | 13 |
| 11 | `reChargeListBack` | `/reChargeListBack?customerId` | `views/chargeAdmin/reChargeListBack.html` | `reChargeListBackCtrl` | 9 |
| 12 | `unPayDetail` | `/unPayDetail?customerId` | `views/chargeAdmin/unPayDetail.html` | `unPayDetailCtrl` | 4 |
| 13 | `unPayList` | `/unPayList` | `views/chargeAdmin/unPayList.html` | `unPayListCtrl` | 1 |
| 14 | `waitChargeDetail` | `/waitChargeDetail?medicalRecordId` | `views/chargeAdmin/waitChargeDetail.html` | `waitChargeDetailCtrl` | 10 |
| 15 | `waitChargeList` | `/waitChargeList` | `views/chargeAdmin/waitChargeList.html` | `waitChargeListCtrl` | 1 |
| 16 | `waitPayBack` | `/waitPayBack?cashflowId` | `views/chargeAdmin/waitPayBack.html` | `waitPayBackCtrl` | 5 |
| 17 | `waitPayBackList` | `/waitPayBackList` | `views/chargeAdmin/waitPayBackList.html` | `waitPayBackListCtrl` | 4 |
| 18 | `waitPayDetail` | `/waitPayDetail?cashflowId` | `views/chargeAdmin/waitPayDetail.html` | `waitPayDetailCtrl` | 8 |
| 19 | `waitPayList` | `/waitPayList` | `views/chargeAdmin/waitPayList.html` | `waitPayListCtrl` | 2 |

## §2 端点清单（去重 57 个）

- `POST /admin/cancelMedicalRecordCashflow.json`
- `POST /admin/changeMedicalExamineRateFee.json`
- `POST /admin/changeMedicalProductRateFee.json`
- `POST /admin/commitPartRefundForExistScan.json`
- `POST /admin/commitPartRefundForNotExistScan.json`
- `POST /admin/commitSubBanlance.json`
- `POST /admin/computeUnPlaceOrderMedicalRecordFee.json`
- `POST /admin/computeUsableCustomerCoupon.json`
- `POST /admin/createCashFlowForMedicalRecord.json`
- `POST /admin/createPartRefund.json`
- `POST /admin/deliveryMachineCenterOrder.json`
- `POST /admin/getCashFlowCashierVo.json`
- `POST /admin/getCashFlowCreditVo.json`
- `POST /admin/getCashflowDeliveryVo.json`
- `POST /admin/getCashflowDeliveryVoList.json`
- `POST /admin/getCompanyCashConf.json`
- `POST /admin/getCompanyOfMine.json`
- `POST /admin/getCorpCashConf.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getCorpPayChannel.json`
- `POST /admin/getCustomerCashflowCreditLogVoToPay.json`
- `POST /admin/getCustomerMember.json`
- `POST /admin/getCustomerPoint.json`
- `POST /admin/getCustomerVo.json`
- `POST /admin/getCustomerWallet.json`
- `POST /admin/getCustomerWalletLogVo.json`
- `POST /admin/getMedicalRecordCashflowVo.json`
- `POST /admin/getMedicalRecordCashflowVoListOfCompany.json`
- `POST /admin/getMedicalRecordRefundDetailVo.json`
- `POST /admin/getMedicalRecordRefundLogVo.json`
- `POST /admin/getPatientInfo.json`
- `POST /admin/getUnPlaceOrderMedicalRecordVoList.json`
- `POST /admin/initAddBanlance.json`
- `POST /admin/initSubBanlance.json`
- `POST /admin/initSubBanlanceAuto.json`
- `POST /admin/isCustomerCouponUsable.json`
- `POST /admin/payCreditCashflowIdList.json`
- `POST /admin/payCreditRefund.json`
- `POST /admin/payMedicalRecordCashflow.json`
- `POST /admin/pointToMoney.json`
- `POST /admin/reComputeUnPlaceOrderMedicalRecordFee.json`
- `POST /admin/receiveMachineCenterOrder.json`
- `POST /admin/refundCreditCashflowForScan.json`
- `POST /admin/refundCreditCashflowIdList.json`
- `POST /admin/rollbackCredit.json`
- `POST /admin/selectCustomerCreditVoList.json`
- `POST /admin/selectCustomerWalletLogVoList.json`
- `POST /admin/selectCustomerWalletVoList.json`
- `POST /admin/selectMachineCenterListOfProduct.json`
- `POST /admin/selectMachineCenterOrderRecordVoList.json`
- `POST /admin/selectMedicalRecordRefundLogVoListOfCompany.json`
- `POST /admin/selectOrCreateWechatCard.json`
- `POST /admin/selectPosDeviceListOfCompany.json`
- `POST /admin/selectUsableCustomerCouponVoList.json`
- `POST /admin/statProductDeliveryStatus.json`
- `POST /admin/statProductDeliveryStatusOfCashflow.json`
- `POST /admin/xxx.json`

## §3 逐页字段规格

### 6.1 `deliveryInput`

- **URL**：`/deliveryInput?cashflowId`
- **模板**：`views/chargeAdmin/deliveryInput.html`
- **控制器**：`deliveryInputCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 请选择是否加工 |
| 2 | 品牌/类目/生产厂家 |
| 3 | 商品基本信息 |
| 4 | 规格 |
| 5 | 数量 |
| 6 | 发货仓库 |
| 7 | 批号 |
| 8 | 收费状态 |
| 9 | 商品基本信息 |
| 10 | 规格 |
| 11 | 下单数量 |
| 12 | 发货仓库 |
| 13 | 批号 生产日期 有效期 唯一标识码 剩余数量 发货数量 定制参数 |
| 14 | 商品基本信息 |
| 15 | 规格 |
| 16 | 下单数量 |
| 17 | 加工中心 |
| 18 | 类型 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.medicalProduct.objectId` |
| `item.medicalProduct.object` |
| `iten.deliveryCount` |
| `startTime` |
| `dateSearch` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `getStatusDeliveryFactory.object.waitingDeliveryCount` |
| `corpInfo.employeeTitle` |
| `getMedicalRecordDeliveryFactory.result.object.medicalRecord.createrName` |
| `item.lockMachineCenter.name` |
| `item.lockMachineCenter.id` |
| `modelName` |
| `modelName.name` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `item.lockStorehouse.name` |
| `iten.stockInSku.batchNo` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.productSku.skuCode` |
| `printModel` |
| `itea.modelName` |
| `itea.modelValue` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.uniqueCode` |
| `iten.stockInSkuExistCount` |
| `val.modelName` |
| `val.modelValue` |
| `iten.stockInSku.remark` |
| `item.machineCenter.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddModal()` |
| `showDeliveryModal()` |
| `saveStock()` |
| `stockDetail=false` |
| `open1()` |
| `searchDate()` |
| `selectOrder()` |
| `hideAddModal()` |

**跳转到**：`deliveryList`

### 6.2 `deliveryInputRecord`

- **URL**：`/deliveryInputRecord?cashflowId`
- **模板**：`views/chargeAdmin/deliveryInputRecord.html`
- **控制器**：`deliveryInputRecordCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目/生产厂家 |
| 2 | 商品基本信息 |
| 3 | 规格 |
| 4 | 数量 |
| 5 | 发货仓库 |
| 6 | 批号 |
| 7 | 生产日期 |
| 8 | 说明 |
| 9 | 发货时间 |
| 10 | 收费状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.medicalProductDelivery.deliveryComment` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `getStatusDeliveryFactory.object.deliveryedCount` |
| `corpInfo.employeeTitle` |
| `getMedicalRecordDeliveryFactory.result.object.medicalRecord.doctorName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.product.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `item.lockStorehouse.name` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalProductDelivery.deliveryComment` |
| `item.medicalProductDelivery.completeTime` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setToggle()` |
| `saveRemark()` |

**跳转到**：`deliveryList`

### 6.3 `deliveryList`

- **URL**：`/deliveryList`
- **模板**：`views/chargeAdmin/deliveryList.html`
- **控制器**：`deliveryListCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCashflowDeliveryVo` | `POST /admin/getCashflowDeliveryVo.json` |
| `getCashflowDeliveryVoList` | `POST /admin/getCashflowDeliveryVoList.json` |
| `selectMachineCenterOrderRecordVoList` | `POST /admin/selectMachineCenterOrderRecordVoList.json` |
| `statProductDeliveryStatus` | `POST /admin/statProductDeliveryStatus.json` |
| `statProductDeliveryStatusOfCashflow` | `POST /admin/statProductDeliveryStatusOfCashflow.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTimer` |
| `obj.keyword` |
| `obj.productKeyword` |
| `obj.batchNoKeyword` |
| `medicalExamineIdArray[$index]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyName` |
| `getAdminList.count` |
| `checkCountFactory.object.waitingDeliveryCount` |
| `checkCountFactory.object.sendToMachineCenterCount` |
| `checkCountFactory.object.deliveryedCount` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.medicalRecord.medicalRecordType` |
| `medicalRecordType` |
| `item.medicalRecord.medicalCode` |
| `item.productNames` |
| `item.deliveryStatus` |
| `deliveryStatus` |
| `item.waitingSeconds` |
| `waitingTime` |
| `item.medicalRecord.doctorName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.waitingDeliveryList.length` |
| `item.deliveryedList.length` |
| `item.sendToMachineCenterList.length` |
| `iten.medicalExamine.id` |
| `iten.medicalExamine.examineName` |
| `iten.medicalExamine.payedStatus` |
| `payedStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `open1()` |
| `open2()` |
| `setTab(null)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setFee(0)` |
| `setFee(1)` |
| `printFahuoqingdan.print(item.cashflow.id)` |
| `savePatient(item.patient.id,item.medicalRecord.id)` |
| `hidePatient()` |

**跳转到**：`deliveryList`, `machineOrderList`

### 6.4 `deliveryProcessing`

- **URL**：`/deliveryProcessing?cashflowId`
- **模板**：`views/chargeAdmin/deliveryProcessing.html`
- **控制器**：`deliveryProcessingCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 加工中心 |
| 2 | 加工类型 |
| 3 | 品牌/类目/生产厂家 |
| 4 | 商品基本信息 |
| 5 | 规格 |
| 6 | 数量 |
| 7 | 发货仓库 |
| 8 | 批号 |
| 9 | 收费状态 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `getStatusDeliveryFactory.object.sendToMachineCenterCount` |
| `corpInfo.employeeTitle` |
| `getMedicalRecordDeliveryFactory.result.object.medicalRecord.createrName` |
| `item.machineCenter.name` |
| `item.machineCenter.type` |
| `machineCenterType` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `item.lockStorehouse.name` |
| `iten.stockInSku.batchNo` |

**跳转到**：`deliveryList`

### 6.5 `machineOrderList`

- **URL**：`/machineOrderList`
- **模板**：`views/chargeAdmin/machineOrderList.html`
- **控制器**：`machineOrderListCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deliveryMachineCenterOrder` | `POST /admin/deliveryMachineCenterOrder.json` |
| `receiveMachineCenterOrder` | `POST /admin/receiveMachineCenterOrder.json` |
| `selectMachineCenterListOfProduct` | `POST /admin/selectMachineCenterListOfProduct.json` |
| `selectMachineCenterOrderRecordVoList` | `POST /admin/selectMachineCenterOrderRecordVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 档案号 |
| 3 | 接诊人 |
| 4 | 加工中心 |
| 5 | 提交人 |
| 6 | 提交时间 |
| 7 | 产品名称 |
| 8 | 规格 |
| 9 | 数量 |
| 10 | 预计取镜日期 |
| 11 | 加工状态 |
| 12 | 签收状态 签收是指镜片加工完成，店员签收 发货是指顾客把货提走 |
| 13 | 发货状态 |
| 14 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.keyword` |
| `obj.productKeyword` |
| `obj.machineCenterId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyName` |
| `getAdminList.count` |
| `modelName.id` |
| `modelName.name` |
| `item.patient.patientName` |
| `item.medicalRecord.medicalCode` |
| `item.medicalRecord.doctorName` |
| `item.machineCenter.name` |
| `item.sendAdmin.nickname` |
| `item.machineCenterOrder.gmtCreate` |
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
| `item.medicalProduct.useCount` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.refundCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setTab(4)` |
| `changeReceiveStatus(null)` |
| `changeReceiveStatus(0)` |
| `changeReceiveStatus(1)` |
| `receiveOrder(item.machineCenterOrder.id,$index)` |
| `deliveryReceiveOrder(item.machineCenterOrder.id,$index)` |

**跳转到**：`deliveryList`, `machineOrderList`

### 6.6 `partBack`

- **URL**：`/partBack?cashflowId`
- **模板**：`views/chargeAdmin/partBack.html`
- **控制器**：`partBackCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitPartRefundForExistScan` | `POST /admin/commitPartRefundForExistScan.json` |
| `commitPartRefundForNotExistScan` | `POST /admin/commitPartRefundForNotExistScan.json` |
| `createPartRefund` | `POST /admin/createPartRefund.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getCustomerWallet` | `POST /admin/getCustomerWallet.json` |
| `getMedicalRecordCashflowVo` | `POST /admin/getMedicalRecordCashflowVo.json` |
| `getMedicalRecordRefundDetailVo` | `POST /admin/getMedicalRecordRefundDetailVo.json` |
| `getMedicalRecordRefundLogVo` | `POST /admin/getMedicalRecordRefundLogVo.json` |
| `refundCreditCashflowForScan` | `POST /admin/refundCreditCashflowForScan.json` |
| `refundCreditCashflowIdList` | `POST /admin/refundCreditCashflowIdList.json` |
| `rollbackCredit` | `POST /admin/rollbackCredit.json` |

**表单标签**

| 标签 |
|---|
| {{item._name}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 全选 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 单价(￥) |
| 5 | 下单数量 |
| 6 | 折扣 |
| 7 | 折后金额(￥) |
| 8 | 备注 |
| 9 | 可退数量 |
| 10 | 本次退货数量 |
| 11 | 退货入库仓 |
| 12 | 操作 |
| 13 | {{item.name}}：{{item.value}} 退款方式 收款渠道 |
| 14 | 退款模式 |
| 15 | 可退金额 |
| 16 | 退款方式 |
| 17 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `partBackClass.allStatus` |
| `item.isChose` |
| `item.chose` |
| `item.value` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `refundFeeInfo.customer.avatar` |
| `refundFeeInfo.patient.patientName` |
| `refundFeeInfo.rollbackCreditMoney` |
| `refundFeeInfo.refundCreditMoney` |
| `refundFeeInfo.patient.patientGender` |
| `gender` |
| `refundFeeInfo.patient.patientBirthday` |
| `howoldFilter` |
| `refundFeeInfo.customer.customerName` |
| `refundFeeInfo.customer.linkMobile` |
| `hidePhone` |
| `refundFeeInfo.medicalRecord.medicalCode` |
| `refundFeeInfo.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `corpInfo.employeeTitle` |
| `refundFeeInfo.medicalRecord.doctorName` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `item._canbackNum` |
| `item.refundStorehouse.name` |
| `partOrderList.length` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `refundTotalProduct` |
| `item.name` |
| `item.value` |
| `creditRefundFeeVoOfMode2.refundTypeFeeVoList.length` |
| `creditRefundFeeVoOfMode1.refundMode` |
| `refundModeType` |
| `creditRefundFeeVoOfMode1.totalRefundableFee` |
| `item._name` |
| `item._backName` |
| `item.refundableFee` |
| `creditRefundFeeVoOfMode2.refundMode` |
| `item.integral` |
| `customerName` |
| `refundFeeInfo.cashflow.creditStatus` |
| `refundTotalCreditFee` |
| `cashRefundFeeVoOfMode2.refundTypeFeeVoList.length` |
| `cashRefundFeeVoOfMode1.refundMode` |
| `cashRefundFeeVoOfMode1.totalRefundableFee` |
| `cash` |
| `index` |
| `cashRefundFeeVoOfMode2.refundMode` |
| `refundTotalCashFee` |

**页面动作（ng-click）**

| 动作 |
|---|
| `partBackClass.choseAll()` |
| `partBackClass.choseSingle()` |
| `verifyAuth(0)` |
| `printShoufei.click()` |
| `diffDisable($index)` |
| `verifyAuth(creditRefundFeeVoOfMode1.refundCashierType,true)` |
| `verifyAuth(creditRefundFeeVoOfMode2.refundCashierType,true)` |
| `getCashRefundTotalFee()` |
| `verifyAuth(cashRefundFeeVoOfMode1.refundCashierType)` |
| `verifyAuth(cashRefundFeeVoOfMode2.refundCashierType)` |

### 6.7 `payBackDetail`

- **URL**：`/payBackDetail?refundId&refundLogId`
- **模板**：`views/chargeAdmin/payBackDetail.html`
- **控制器**：`payBackDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 退费名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 单价(￥) |
| 5 | 数量 |
| 6 | 折扣 |
| 7 | 折后金额(￥) |
| 8 | 退款数量 |
| 9 | 退货入库仓库 |
| 10 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getRefundFactory.cashflow.tradeNo` |
| `getRefundFactory.patient.avatar` |
| `getRefundFactory.patient.patientName` |
| `getRefundFactory.medicalRecord.medicalCode` |
| `getRefundFactory.patient.patientGender` |
| `gender` |
| `getRefundFactory.patient.patientBirthday` |
| `howoldFilter` |
| `getRefundFactory.patient.idCard` |
| `getRefundFactory.customer.customerName` |
| `getRefundFactory.customer.linkMobile` |
| `hidePhone` |
| `item.product.productName` |
| `item.medicalProduct.model1` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.refundProductLog.refundCount` |
| `item.refundStorehouse.name` |
| `item.medicalProduct.remark` |
| `item.examine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `item.refundFee` |
| `item._backName` |
| `getRefundFactory.refundLog.refundTotalFee` |
| `getRefundFactory.object.refund.refundFee` |
| `getRefundFactory.object.refund.refundType` |
| `refundType` |
| `getRefundFactory.object.cashflow.substractFee` |
| `getRefundFactory.object.cashflow.receivedFromMedical` |
| `getRefundFactory.object.cashflow.receivedFromCredit` |
| `getRefundFactory.object.cashflow.receivedFromCommercial` |
| `getRefundFactory.object.cashflow.receivedFromWallet` |
| `getRefundFactory.object.cashflow.receivedFromPoint` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel1` |
| `otherPay.channelName1` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel2` |
| `otherPay.channelName2` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel3` |
| `otherPay.channelName3` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel4` |
| `otherPay.channelName4` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel5` |
| `otherPay.channelName5` |
| `getRefundFactory.object.cashflow.receivedFromCash` |
| `getRefundFactory.object.cashflow.receivedFromBankcard` |
| `getRefundFactory.object.cashflow.receivedFromWechat` |
| `getRefundFactory.object.cashflow.receivedFromAlipay` |
| `getRefundFactory.object.cashflow.receivedFromWechatScan` |
| `getRefundFactory.object.cashflow.receivedFromAlipayScan` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |

### 6.8 `payedDetail`

- **URL**：`/payedDetail?cashflowId`
- **模板**：`views/chargeAdmin/payedDetail.html`
- **控制器**：`payedDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 收费名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 单价(￥) |
| 5 | 数量 |
| 6 | 折扣 |
| 7 | 折后金额(￥) |
| 8 | 备注 |
| 9 | 收费名称 |
| 10 | 规格 |
| 11 | 单位 |
| 12 | 单价(￥) |
| 13 | 数量 |
| 14 | 折扣 |
| 15 | 折后金额(￥) |
| 16 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCashflowObjectFactory.object.cashflow.tradeNo` |
| `getCashflowObjectFactory.object.patient.avatar` |
| `getCashflowObjectFactory.object.patient.patientName` |
| `getCashflowObjectFactory.object.medicalRecord.medicalCode` |
| `getCashflowObjectFactory.object.patient.patientGender` |
| `gender` |
| `getCashflowObjectFactory.object.patient.idCard` |
| `getCashflowObjectFactory.object.customer.customerName` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `getCashflowObjectFactory.object.medicalProductRateFee` |
| `getCashflowObjectFactory.object.medicalExamineRateFee` |
| `getCashflowObjectFactory.object.registrationRateFee` |
| `getCashflowObjectFactory.object.medicalProductModelRateFee` |
| `getCashflowObjectFactory.object.totalFee` |
| `getCashflowObjectFactory.object.substractFee` |
| `getCashflowObjectFactory.object.cashflow.totalPayment` |
| `getCashflowObjectFactory.object.cashflow.substractFee` |
| `getCashflowObjectFactory.object.cashflow.receivedFromMedical` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCredit` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCommercial` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWallet` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPoint` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel1` |
| `otherPay.channelName1` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel2` |
| `otherPay.channelName2` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel3` |
| `otherPay.channelName3` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel4` |
| `otherPay.channelName4` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel5` |
| `otherPay.channelName5` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCash` |
| `getCashflowObjectFactory.object.cashflow.receivedFromBankcard` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechat` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipay` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechatScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipayScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPos` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.patient.patientBirthday` |
| `howoldFilter` |
| `getCashflowObjectFactory.object.customer.linkMobile` |
| `hidePhone` |
| `printModel` |
| `getCashflowObjectFactory.object.company.companyName` |
| `getCashflowObjectFactory.object.company.phone` |
| `getCashflowObjectFactory.object.cashflow.casherName` |
| `corpInfo.employeeTitle` |
| `getCashflowObjectFactory.object.medicalRecord.doctorName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |

### 6.9 `payedList`

- **URL**：`/payedList`
- **模板**：`views/chargeAdmin/payedList.html`
- **控制器**：`payedListCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getMedicalRecordCashflowVo` | `POST /admin/getMedicalRecordCashflowVo.json` |
| `getMedicalRecordCashflowVoListOfCompany` | `POST /admin/getMedicalRecordCashflowVoListOfCompany.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.cashflow.payTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecord.doctorName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.cashflow.totalPayment` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.cashflow.tradeNo` |
| `getCashflowObjectFactory.object.patient.patientName` |
| `getCashflowObjectFactory.object.patient.patientGender` |
| `getCashflowObjectFactory.object.patient.patientBirthday` |
| `getCashflowObjectFactory.object.cashflow.payTime` |
| `getCashflowObjectFactory.object.school.schoolName` |
| `getCashflowObjectFactory.object.schoolClass.className` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `getCashflowObjectFactory.object.medicalProductRateFee` |
| `getCashflowObjectFactory.object.medicalProductModelRateFee` |
| `getCashflowObjectFactory.object.medicalExamineRateFee` |
| `getCashflowObjectFactory.object.registrationRateFee` |
| `getCashflowObjectFactory.object.cashflow.totalPayment` |
| `getCashflowObjectFactory.object.cashflow.substractFee` |
| `getCashflowObjectFactory.object.cashflow.receivedFromMedical` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCredit` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCommercial` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWallet` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPoint` |
| `otherPay.channelName1` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel1` |
| `otherPay.channelName2` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel2` |
| `otherPay.channelName3` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel3` |
| `otherPay.channelName4` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel4` |
| `otherPay.channelName5` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel5` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCash` |
| `getCashflowObjectFactory.object.cashflow.receivedFromBankcard` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechat` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipay` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechatScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipayScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPos` |
| `getCashflowObjectFactory.object.cashflow.customerWalletBalance` |
| `corpInfo.companyTitle` |
| `company.companyName` |
| `company.phone` |
| `getCashflowObjectFactory.object.cashflow.casherName` |
| `getCashflowObjectFactory.object.medicalRecord.doctorName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `open1()` |
| `open2()` |
| `showPrint(item.cashflow.id,$event)` |
| `printShoufei.print(item.cashflow.id)` |
| `printList(item.cashflow.id)` |
| `printPeijing.print(item.cashflow.id,item.medicalRecord.id,false)` |
| `printPeijing.print(item.cashflow.id,item.medicalRecord.id,true)` |
| `back(item.cashflow.id)` |
| `hidePatient()` |

### 6.10 `reChargeList`

- **URL**：`/reChargeList`
- **模板**：`views/chargeAdmin/reChargeList.html`
- **控制器**：`reChargeListCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitSubBanlance` | `POST /admin/commitSubBanlance.json` |
| `getCompanyCashConf` | `POST /admin/getCompanyCashConf.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getCustomerMember` | `POST /admin/getCustomerMember.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getCustomerWallet` | `POST /admin/getCustomerWallet.json` |
| `getCustomerWalletLogVo` | `POST /admin/getCustomerWalletLogVo.json` |
| `initAddBanlance` | `POST /admin/initAddBanlance.json` |
| `initSubBanlance` | `POST /admin/initSubBanlance.json` |
| `selectCustomerWalletLogVoList` | `POST /admin/selectCustomerWalletLogVoList.json` |
| `selectCustomerWalletVoList` | `POST /admin/selectCustomerWalletVoList.json` |
| `selectOrCreateWechatCard` | `POST /admin/selectOrCreateWechatCard.json` |
| `selectPosDeviceListOfCompany` | `POST /admin/selectPosDeviceListOfCompany.json` |

**表单标签**

| 标签 |
|---|
| 只显示有值用户 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 本金金额 |
| 3 | 赠送金额 |
| 4 | 合计金额 |
| 5 | 操作 |
| 6 | 操作时间 |
| 7 | 充值方式 退卡方式 |
| 8 | 本金金额 |
| 9 | 赠送金额 |
| 10 | 合计金额 |
| 11 | 备注 |
| 12 | {{corpInfo. companyTitle}} |
| 13 | 操作 |
| 14 | 收款方式 |
| 15 | 本金金额 |
| 16 | 赠送金额 |
| 17 | 合计 |
| 18 | 备注 |
| 19 | 退款方式 |
| 20 | 本金金额 |
| 21 | 赠送金额 |
| 22 | 合计 |
| 23 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `hasMoney` |
| `logType` |
| `balance.addTrueMoney` |
| `balance.addGiftMoney` |
| `balance.remark` |
| `totalBalanceFrom` |
| `totalBalanceTo` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `wecharCardFactory.result.object.substractType` |
| `substractType` |
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerWallet.trueBalance` |
| `item.customerWallet.giftBalance` |
| `corpInfo.` |
| `companyTitle` |
| `item.customerWalletLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customerWalletLog.payChannel` |
| `payChannel` |
| `returnType` |
| `item.customerWalletLog.addTrueMoney` |
| `item.customerWalletLog.addGiftMoney` |
| `item.customerWalletLog.remark` |
| `item.company.companyName` |
| `getMemberObjectFactory.object.memberName` |
| `patientObjectFactory.vo.customer.customerName` |
| `getWalletObejctFactory.object.trueBalance` |
| `getWalletObejctFactory.object.giftBalance` |
| `item.payChannel` |
| `balance.payChannel` |
| `item.img_chose` |
| `item.img_notchose` |
| `item.name` |
| `getCompanyObjectFactory.result.object.companyName` |
| `balance.addTrueMoney` |
| `companyFactory.object.cashLogo` |
| `companyFactory.object.cashHeader` |
| `walletLogObjectFactory.object.customer.customerName` |
| `walletLogObjectFactory.object.customer.linkMobile` |
| `walletLogObjectFactory.object.customerWalletLog.addTrueMoney` |
| `walletLogObjectFactory.object.customerWalletLog.addGiftMoney` |
| `walletLogObjectFactory.object.customerWalletLog.remark` |
| `walletLogObjectFactory.object.company.companyName` |
| `walletLogObjectFactory.object.company.phone` |
| `walletLogObjectFactory.object.customerWalletLog.casherName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showRecharge(item.customer.id,$index)` |
| `showBackFee(item.customer.id)` |
| `showRecord(item.customer.id)` |
| `printRecode(item.customerWalletLog.id,1)` |
| `printRecode(item.customerWalletLog.id,2)` |
| `hideRechargeModal()` |
| `updatepayChannel_click(item.payChannel,` |
| `saveWallet()` |

### 6.11 `reChargeListBack`

- **URL**：`/reChargeListBack?customerId`
- **模板**：`views/chargeAdmin/reChargeListBack.html`
- **控制器**：`reChargeListBackCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitSubBanlance` | `POST /admin/commitSubBanlance.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getCustomerWallet` | `POST /admin/getCustomerWallet.json` |
| `getCustomerWalletLogVo` | `POST /admin/getCustomerWalletLogVo.json` |
| `initSubBanlance` | `POST /admin/initSubBanlance.json` |
| `initSubBanlanceAuto` | `POST /admin/initSubBanlanceAuto.json` |
| `selectCustomerWalletLogVoList` | `POST /admin/selectCustomerWalletLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 充值时间 |
| 2 | 原充值方式 |
| 3 | 门店 |
| 4 | 充值金额 (本金\|赠金) |
| 5 | 已退本金 |
| 6 | 已扣除赠金 |
| 7 | 操作 |
| 8 | 退款方式 |
| 9 | 本金金额 |
| 10 | 赠送金额 |
| 11 | 合计 |
| 12 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `returnCard.backInfo.subGiftMoney` |
| `returnCard.backInfo.remark` |
| `returnCard.backInfo.subTrueMoney` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `patientObjectFactory.avatar` |
| `patientObjectFactory.customerName` |
| `patientObjectFactory.linkMobile` |
| `hidePhone` |
| `getWalletObejctFactory.trueBalance` |
| `getWalletObejctFactory.giftBalance` |
| `item.customerWalletLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customerWalletLog.payChannel` |
| `payChannel` |
| `item.company.companyName` |
| `item.customerWalletLog.addTrueMoney` |
| `item.customerWalletLog.addGiftMoney` |
| `item.customerWalletLog.refundTrueMoney` |
| `item.customerWalletLog.refundGiftMoney` |
| `orderListFactory.total.addTrueMoney` |
| `orderListFactory.total.addGiftMoney` |
| `orderListFactory.total.refundTrueMoney` |
| `orderListFactory.total.refundGiftMoney` |
| `item.name` |
| `returnCard.backInfo.payChannel` |
| `returnType` |
| `returnCard.showBankInfo.bankName` |
| `returnCard.showBankInfo.payCardId` |
| `getCompanyObjectFactory.result.object.companyName` |
| `returnCard.backInfo.subTrueMoney` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `walletLogObjectFactory.object.customer.customerName` |
| `walletLogObjectFactory.object.customer.linkMobile` |
| `walletLogObjectFactory.object.customerWalletLog.addTrueMoney` |
| `walletLogObjectFactory.object.customerWalletLog.addGiftMoney` |
| `walletLogObjectFactory.object.customerWalletLog.remark` |
| `walletLogObjectFactory.object.company.companyName` |
| `walletLogObjectFactory.object.company.phone` |
| `walletLogObjectFactory.object.customerWalletLog.casherName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `returnCard.openModal(item,$index)` |
| `updatepayChannel_click(item.payChannel)` |
| `returnCard.backInterface()` |
| `returnCard.hideModal()` |

### 6.12 `unPayDetail`

- **URL**：`/unPayDetail?customerId`
- **模板**：`views/chargeAdmin/unPayDetail.html`
- **控制器**：`unPayDetailCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCustomerCashflowCreditLogVoToPay` | `POST /admin/getCustomerCashflowCreditLogVoToPay.json` |
| `getCustomerWallet` | `POST /admin/getCustomerWallet.json` |
| `payCreditCashflowIdList` | `POST /admin/payCreditCashflowIdList.json` |
| `selectPosDeviceListOfCompany` | `POST /admin/selectPosDeviceListOfCompany.json` |

**表单标签**

| 标签 |
|---|
| {{item.name}} |
| 现金 |
| 银行卡 微信记账 |
| 支付宝记账 |
| 余额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `unPayId` |
| `zuhe` |
| `item.isChose` |
| `tagIdArray[0]` |
| `tagIdArray[1]` |
| `tagIdArray[2]` |
| `tagIdArray[3]` |
| `tagIdArray[4]` |
| `item.value` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `customerCashflowCreditLogVo.customer.avatar` |
| `customerCashflowCreditLogVo.customer.customerName` |
| `customerCashflowCreditLogVo.customerCredit.creditBalance` |
| `customerCashflowCreditLogVo.customer.linkMobile` |
| `hidePhone` |
| `customerCashflowCreditLogVo.cashflowCreditLogDataList` |
| `index` |
| `creditMoney` |
| `customerCashflowCreditLogVo.cashflowCreditLogDataList.length` |
| `corpInfo.employeeTitle` |
| `corpInfo.companyTitle` |
| `item.cashflowId` |
| `item.creditTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.creditMoney` |
| `item.medicalCode` |
| `item.patientName` |
| `item.doctorName` |
| `item.casherName` |
| `item.companyName` |
| `item.name` |
| `item.payChannel` |
| `payType` |
| `item.img_chose` |
| `item.img_notchose` |

**页面动作（ng-click）**

| 动作 |
|---|
| `reCompute($index)` |
| `clearCash($index)` |
| `clearCash(0,tagIdArray[0])` |
| `clearCash(3,tagIdArray[1])` |
| `clearCash(1,tagIdArray[2])` |
| `clearCash(2,tagIdArray[3])` |
| `clearCash(4,tagIdArray[4])` |
| `setTab(item.payChannel)` |
| `confirmPay()` |

**跳转到**：`unPayList`

### 6.13 `unPayList`

- **URL**：`/unPayList`
- **模板**：`views/chargeAdmin/unPayList.html`
- **控制器**：`unPayListCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCustomerCreditVoList` | `POST /admin/selectCustomerCreditVoList.json` |

**表单标签**

| 标签 |
|---|
| 只显示未还清用户 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.hasCredit` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerCredit.creditBalance` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `showModal(item.customer.id)` |

### 6.14 `waitChargeDetail`

- **URL**：`/waitChargeDetail?medicalRecordId`
- **模板**：`views/chargeAdmin/waitChargeDetail.html`
- **控制器**：`waitChargeDetailCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeMedicalExamineRateFee` | `POST /admin/changeMedicalExamineRateFee.json` |
| `changeMedicalProductRateFee` | `POST /admin/changeMedicalProductRateFee.json` |
| `computeUnPlaceOrderMedicalRecordFee` | `POST /admin/computeUnPlaceOrderMedicalRecordFee.json` |
| `computeUsableCustomerCoupon` | `POST /admin/computeUsableCustomerCoupon.json` |
| `createCashFlowForMedicalRecord` | `POST /admin/createCashFlowForMedicalRecord.json` |
| `getCorpCashConf` | `POST /admin/getCorpCashConf.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `isCustomerCouponUsable` | `POST /admin/isCustomerCouponUsable.json` |
| `reComputeUnPlaceOrderMedicalRecordFee` | `POST /admin/reComputeUnPlaceOrderMedicalRecordFee.json` |
| `selectUsableCustomerCouponVoList` | `POST /admin/selectUsableCustomerCouponVoList.json` |

**表单标签**

| 标签 |
|---|
| 全选 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 全选 |
| 2 | 收费名称 |
| 3 | 规格 |
| 4 | 单位 |
| 5 | 单价(￥) |
| 6 | 数量 |
| 7 | 折扣 |
| 8 | 折后金额(￥) |
| 9 | 备注 |
| 10 | 优惠券名称 |
| 11 | 种类/面额 |
| 12 | 有效期 |
| 13 | 限制条件 |
| 14 | 使用说明 |
| 15 | 发放日期 |
| 16 | 券码 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `medicalProductIdList[$index]` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `medicalProductModelIdList[$index]` |
| `medicalExamineIdList[$index]` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `registrationFeeIdList[$index]` |
| `obj.customerCouponId` |
| `couponModal.params.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPatientObjectFactory.object.patientName` |
| `getPatientObjectFactory.object.patientGender` |
| `gender` |
| `getPatientObjectFactory.object.patientBirthday` |
| `howoldFilter` |
| `getUnPlaceOrderObjectFactory.result.object.customer.customerName` |
| `getUnPlaceOrderObjectFactory.object.medicalRecord.medicalCode` |
| `couponModal.couponVo.coupon.couponName` |
| `couponModal.couponVo.customerCoupon.couponCode` |
| `item.medicalProduct.id` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalExamine.id` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `getUnPlaceOrderObjectFactory.object.medicalProductRateFee` |
| `getUnPlaceOrderObjectFactory.object.medicalExamineRateFee` |
| `getUnPlaceOrderObjectFactory.object.registrationRateFee` |
| `getUnPlaceOrderObjectFactory.object.medicalProductModelRateFee` |
| `getUnPlaceOrderObjectFactory.object.totalFee` |
| `getUnPlaceOrderObjectFactory.object.substractFee` |
| `getUnPlaceOrderObjectFactory.object.rateFee` |
| `item.customerCoupon.id` |
| `item.coupon.couponName` |
| `item.coupon.couponType` |
| `couponType` |
| `item.couponValue` |
| `item.coupon.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.coupon.useTimeStartDays` |
| `item.coupon.useTimeEnd` |
| `item.coupon.useTimeEndDays` |
| `item.coupon.useScene` |
| `useScene` |
| `item.coupon.useOverMoney` |
| `item.coupon.useOverCount` |
| `item.coupon.useContent` |
| `item.coupon.gmtCreate` |
| `hh` |
| `mm` |
| `ss` |
| `item.customerCoupon.couponCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `couponModal.getList()` |
| `couponModal.deleteCoupon()` |
| `checkAll($event)` |
| `clickComputeFee($event,item.medicalProduct.id,$index)` |
| `goCheck()` |
| `couponModal.hideCouponModal()` |
| `couponModal.setCoupon(item)` |
| `couponModal.modify()` |

**跳转到**：`waitChargeList`

### 6.15 `waitChargeList`

- **URL**：`/waitChargeList`
- **模板**：`views/chargeAdmin/waitChargeList.html`
- **控制器**：`waitChargeListCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getUnPlaceOrderMedicalRecordVoList` | `POST /admin/getUnPlaceOrderMedicalRecordVoList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.firstVisitFrom` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.doctorName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.rateFee` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `open1()` |
| `open2()` |
| `hidePatient()` |

### 6.16 `waitPayBack`

- **URL**：`/waitPayBack?cashflowId`
- **模板**：`views/chargeAdmin/waitPayBack.html`
- **控制器**：`waitPayBackCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCashFlowCashierVo` | `POST /admin/getCashFlowCashierVo.json` |
| `getCashFlowCreditVo` | `POST /admin/getCashFlowCreditVo.json` |
| `getMedicalRecordCashflowVo` | `POST /admin/getMedicalRecordCashflowVo.json` |
| `payCreditRefund` | `POST /admin/payCreditRefund.json` |
| `xxx` | `POST /admin/xxx.json` |

**表单标签**

| 标签 |
|---|
| {{item.medicalExamine.examineName}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 全选 |
| 2 | 收费名称 |
| 3 | 规格 |
| 4 | 单位 |
| 5 | 单价(￥) |
| 6 | 数量 |
| 7 | 折扣 |
| 8 | 折后金额(￥) |
| 9 | 备注 |
| 10 | 退费项目 |
| 11 | 单价(￥) |
| 12 | 数量 |
| 13 | 单位 |
| 14 | 折扣(%) |
| 15 | 收款渠道 |
| 16 | 支付方式 |
| 17 | 退款方式 |
| 18 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `medicalExamineIdList[$index]` |
| `backItem.refundType` |
| `obj.refundType` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCashflowObjectFactory.object.customer.avatar` |
| `getCashflowObjectFactory.object.patient.patientName` |
| `getCashflowObjectFactory.object.waitingPayCredit` |
| `getCashflowObjectFactory.object.patient.patientGender` |
| `gender` |
| `getCashflowObjectFactory.object.customer.customerName` |
| `getCashflowObjectFactory.object.customer.linkMobile` |
| `hidePhone` |
| `getCashflowObjectFactory.object.medicalRecord.medicalCode` |
| `corpInfo.employeeTitle` |
| `getCashflowObjectFactory.object.medicalRecord.doctorName` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalExamine.id` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `getCashflowObjectFactory.object.totalFee` |
| `getCashflowObjectFactory.object.substractFee` |
| `getCashflowObjectFactory.object.cashflow.totalPayment` |
| `getCashflowObjectFactory.object.cashflow.substractFee` |
| `getCashflowObjectFactory.object.cashflow.receivedFromMedical` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCredit` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCommercial` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWallet` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPoint` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel1` |
| `otherPay.channelName1` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel2` |
| `otherPay.channelName2` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel3` |
| `otherPay.channelName3` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel4` |
| `otherPay.channelName4` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPayChannel5` |
| `otherPay.channelName5` |
| `getCashflowObjectFactory.object.cashflow.receivedFromCash` |
| `getCashflowObjectFactory.object.cashflow.receivedFromBankcard` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechat` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipay` |
| `getCashflowObjectFactory.object.cashflow.receivedFromWechatScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromAlipayScan` |
| `getCashflowObjectFactory.object.cashflow.receivedFromPos` |
| `getCashflowObjectFactory.object.refundFee` |
| `getCashFlowCredit.cashflow.receivedFromCredit` |
| `getCashFlowCredit.customerCreditLogAuto.payChannel` |
| `payChannel` |
| `paytype.payChannel` |
| `paytype.creditMoney` |
| `mathAbs` |
| `getCashFlowCredit.refundFee` |
| `channel.name` |
| `getCashFlowCredit.member_card.creditMoney` |
| `backItem.refundType` |
| `returnType` |
| `getCashFlowCredit.oriBankCard.bankName` |
| `getCashFlowCredit.oriBankCard.payCardId` |
| `getCashFlowCredit.cashflow.payType` |
| `getCashFlowCashier.cashflow.payType` |
| `getCashFlowCredit.cashflow.receivedFromCashier` |
| `item.name` |
| `getCashFlowCashier.oriBankCard.bankName` |
| `getCashFlowCashier.oriBankCard.payCardId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `computeFee()` |
| `confirmPayBack()` |
| `confirmPartBack()` |
| `updatepayChannel_click(` |
| `backCredit()` |
| `payBack()` |

### 6.17 `waitPayBackList`

- **URL**：`/waitPayBackList`
- **模板**：`views/chargeAdmin/waitPayBackList.html`
- **控制器**：`waitPayBackListCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyCashConf` | `POST /admin/getCompanyCashConf.json` |
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getMedicalRecordRefundLogVo` | `POST /admin/getMedicalRecordRefundLogVo.json` |
| `selectMedicalRecordRefundLogVoListOfCompany` | `POST /admin/selectMedicalRecordRefundLogVoListOfCompany.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 退费名称 |
| 2 | 单位 |
| 3 | 单价(￥) |
| 4 | 数量 |
| 5 | 费用(￥) |
| 6 | 退款数量 |
| 7 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.refundLog.refundTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.medicalRecord.doctorName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.refundLog.refundTotalFee` |
| `companyFactory.object.cashLogo` |
| `getRefundFactory.object.cashflow.tradeNo` |
| `companyFactory.object.cashHeader` |
| `getRefundFactory.object.patient.patientName` |
| `getRefundFactory.object.patient.patientGender` |
| `getRefundFactory.object.patient.patientBirthday` |
| `getRefundFactory.object.medicalRecord.medicalCode` |
| `getRefundFactory.object.customer.customerName` |
| `showPhone` |
| `getRefundFactory.object.refundLog.refundTime` |
| `item.product.productName` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.rateFee` |
| `item.refundProductLog.refundCount` |
| `item.medicalProduct.remark` |
| `item.examine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |
| `getRefundFactory.object.feeData.refundType` |
| `returnType` |
| `getRefundFactory.object.refundLog.refundTotalFee` |
| `item._backName` |
| `item.refundFee` |
| `getRefundFactory.object.cashflow.substractFee` |
| `getRefundFactory.object.cashflow.receivedFromMedical` |
| `getRefundFactory.object.cashflow.receivedFromCredit` |
| `getRefundFactory.object.cashflow.receivedFromCommercial` |
| `getRefundFactory.object.cashflow.receivedFromWallet` |
| `getRefundFactory.object.cashflow.receivedFromPoint` |
| `otherPay.channelName1` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel1` |
| `otherPay.channelName2` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel2` |
| `otherPay.channelName3` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel3` |
| `otherPay.channelName4` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel4` |
| `otherPay.channelName5` |
| `getRefundFactory.object.cashflow.receivedFromPayChannel5` |
| `getRefundFactory.object.cashflow.receivedFromCash` |
| `getRefundFactory.object.cashflow.receivedFromBankcard` |
| `getRefundFactory.object.cashflow.receivedFromWechat` |
| `getRefundFactory.object.cashflow.receivedFromAlipay` |
| `getRefundFactory.object.cashflow.receivedFromWechatScan` |
| `getRefundFactory.object.cashflow.receivedFromAlipayScan` |
| `getRefundFactory.object.cashflow.receivedFromPos` |
| `getRefundFactory.object.company.companyName` |
| `getRefundFactory.object.company.phone` |
| `getRefundFactory.object.refundLog.casherName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `open1()` |
| `open2()` |
| `printList(item.refundLog.id)` |
| `hidePatient()` |

### 6.18 `waitPayDetail`

- **URL**：`/waitPayDetail?cashflowId`
- **模板**：`views/chargeAdmin/waitPayDetail.html`
- **控制器**：`waitPayDetailCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpCashConf` | `POST /admin/getCorpCashConf.json` |
| `getCustomerPoint` | `POST /admin/getCustomerPoint.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getCustomerWallet` | `POST /admin/getCustomerWallet.json` |
| `getMedicalRecordCashflowVo` | `POST /admin/getMedicalRecordCashflowVo.json` |
| `payMedicalRecordCashflow` | `POST /admin/payMedicalRecordCashflow.json` |
| `pointToMoney` | `POST /admin/pointToMoney.json` |
| `selectPosDeviceListOfCompany` | `POST /admin/selectPosDeviceListOfCompany.json` |

**表单标签**

| 标签 |
|---|
| 医保 |
| 挂账 |
| 商保 |
| 余额 |
| 积分 |
| {{otherPay.channelName1}} |
| {{otherPay.channelName2}} |
| {{otherPay.channelName3}} |
| {{otherPay.channelName4}} |
| {{otherPay.channelName5}} |
| 持卡人：{{patientObjectFactory.vo.customer.customerName}} |
| {{item.name}} |
| 现金 |
| 银行卡 |
| 微信记账 |
| 支付宝记账 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 单价(￥) |
| 5 | 数量 |
| 6 | 折扣 |
| 7 | 折后金额(￥) |
| 8 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `substractFee` |
| `hospitalPay` |
| `waitPay` |
| `businessPay` |
| `balancePay` |
| `pointPay` |
| `channel1Pay` |
| `channel2Pay` |
| `channel3Pay` |
| `channel4Pay` |
| `channel5Pay` |
| `receivedFromMedical` |
| `receivedFromCredit` |
| `receivedFromCommercial` |
| `receivedFromWallet` |
| `receivedFromPoint` |
| `receivedFromPayChannel1` |
| `receivedFromPayChannel2` |
| `receivedFromPayChannel3` |
| `receivedFromPayChannel4` |
| `receivedFromPayChannel5` |
| `obj.remark` |
| `zuhe` |
| `tagIdArray[$index]` |
| `tagIdArray[0]` |
| `tagIdArray[1]` |
| `tagIdArray[2]` |
| `tagIdArray[3]` |
| `cashFee` |
| `bankCardFee` |
| `wechatFee` |
| `alipayFee` |
| `getCash` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCashflowObjectFactory.object.cashflow.tradeNo` |
| `getCashflowObjectFactory.object.cashflow.totalPayment` |
| `getCashflowObjectFactory.object.medicalRecord.medicalCode` |
| `getCashflowObjectFactory.object.patient.patientName` |
| `otherPay.channelName1` |
| `otherPay.channelName2` |
| `otherPay.channelName3` |
| `otherPay.channelName4` |
| `otherPay.channelName5` |
| `patientObjectFactory.vo.customer.customerName` |
| `pointToMoney` |
| `getCustomerPointFactory.result.object.point` |
| `initPoint` |
| `index` |
| `item.name` |
| `item.payChannel` |
| `payType` |
| `item.img_chose` |
| `item.img_notchose` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.memberRate` |
| `item.medicalProduct.rateFee` |
| `item.medicalProduct.remark` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalExamine.examineName` |
| `item.medicalExamine.unitName` |
| `item.medicalExamine.marketPrice` |
| `item.medicalExamine.useCount` |
| `item.medicalExamine.memberRate` |
| `item.medicalExamine.rateFee` |
| `item.medicalExamine.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showPayDetail()` |
| `clearCommon(hospitalPay,` |
| `clearCommon(waitPay,` |
| `clearCommon(businessPay,` |
| `clearCommon(balancePay,` |
| `clearCommon(pointPay,` |
| `clearCommon(channel1Pay,` |
| `clearCommon(channel2Pay,` |
| `clearCommon(channel3Pay,` |
| `clearCommon(channel4Pay,` |
| `clearCommon(channel5Pay,` |
| `clearCash(item.payChannel,tagIdArray[$index])` |
| `clearCash(0,tagIdArray[0])` |
| `clearCash(3,tagIdArray[1])` |
| `clearCash(1,tagIdArray[2])` |
| `clearCash(2,tagIdArray[3])` |
| `setTab(item.payChannel)` |
| `confirmPay()` |
| `setTab(11,true)` |
| `hidePatient()` |

**跳转到**：`waitPayList`

### 6.19 `waitPayList`

- **URL**：`/waitPayList`
- **模板**：`views/chargeAdmin/waitPayList.html`
- **控制器**：`waitPayListCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelMedicalRecordCashflow` | `POST /admin/cancelMedicalRecordCashflow.json` |
| `getMedicalRecordCashflowVoListOfCompany` | `POST /admin/getMedicalRecordCashflowVoListOfCompany.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.doctorName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.cashflow.totalPayment` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `open1()` |
| `open2()` |
| `cancelPay(item.cashflow.id)` |
| `hidePatient()` |

**跳转到**：`payedList`, `reChargeList`, `waitChargeList`, `waitPayList`
