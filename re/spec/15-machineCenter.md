# 15｜模块 machineCenter 加工中心

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/machineCenter/` |
| 中文名 | 加工中心 |
| 开发波次 | W5 |
| 页面数 | **21** |
| 端点数（去重） | **20** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `goods.companyStockList` | `/companyStockList` | `views/machineCenter/companyStockList.html` | `companyStockListCtrl` | 7 |
| 2 | `chainStockList` | `/chainStockList` | `views/machineCenter/companyStockList.html` | `companyStockListCtrl` | 7 |
| 3 | `goods.completeStockLoss` | `/completeStockLoss?stockLossId` | `views/machineCenter/completeStockLoss.html` | `completeStockLossCtrl` | 0 |
| 4 | `completeChainStockLoss` | `/completeChainStockLoss?stockLossId` | `views/machineCenter/completeStockLoss.html` | `completeStockLossCtrl` | 0 |
| 5 | `machineOrder` | `/machineOrder` | `views/machineCenter/machineOrder.html` | `machineOrderCtrl` | 9 |
| 6 | `machineOrderBroken` | `/machineOrderBroken?cashflowId&machineCenterId&chain` | `views/machineCenter/machineOrderBroken.html` | `machineOrderBrokenCtrl` | 4 |
| 7 | `machineOrderChainBroken` | `/machineOrderChainBroken?cashflowId&machineCenterId&chain` | `views/machineCenter/machineOrderBroken.html` | `machineOrderBrokenCtrl` | 4 |
| 8 | `machineOrderChainWaitAccess` | `/machineOrderChainWaitAccess` | `views/machineCenter/machineOrderChainWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 9 | `machineOrderChainWaitProcess` | `/machineOrderChainWaitProcess` | `views/machineCenter/machineOrderChainWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 10 | `machineOrderChainProcessing` | `/machineOrderChainProcessing` | `views/machineCenter/machineOrderChainWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 11 | `machineOrderChainTesting` | `/machineOrderChainTesting` | `views/machineCenter/machineOrderChainWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 12 | `machineOrderCompleted` | `/machineOrderCompleted?cashflowId&machineCenterId` | `views/machineCenter/machineOrderCompleted.html` | `machineOrderBrokenCtrl` | 4 |
| 13 | `machineOrderChainCompleted` | `/machineOrderChainCompleted?cashflowId&machineCenterId` | `views/machineCenter/machineOrderCompleted.html` | `machineOrderBrokenCtrl` | 4 |
| 14 | `machineOrderWaitProcess` | `/machineOrderWaitProcess` | `views/machineCenter/machineOrderWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 15 | `machineOrderWaitAccess` | `/machineOrderWaitAccess` | `views/machineCenter/machineOrderWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 16 | `machineOrderProcessing` | `/machineOrderProcessing` | `views/machineCenter/machineOrderWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 17 | `machineOrderTesting` | `/machineOrderTesting` | `views/machineCenter/machineOrderWaitAccess.html` | `machineOrderWaitProcessCtrl` | 1 |
| 18 | `goods.stockLossDetail` | `/stockLossDetail?stockLossId` | `views/machineCenter/stockLossDetail.html` | `stockLossDetailCtrl` | 0 |
| 19 | `chainStockLossDetail` | `/chainStockLossDetail?stockLossId` | `views/machineCenter/stockLossDetail.html` | `stockLossDetailCtrl` | 0 |
| 20 | `stockLossList` | `/stockLossList` | `views/machineCenter/stockLossList.html` | `stockLossListCtrl` | 5 |
| 21 | `stockChainLossList` | `/stockChainLossList` | `views/machineCenter/stockLossList.html` | `stockLossListCtrl` | 5 |

## §2 端点清单（去重 20 个）

- `POST /admin/closeMachineCenterOrder.json`
- `POST /admin/closeMedicalStockLoss.json`
- `POST /admin/completeMachineCenterOrder.json`
- `POST /admin/completeMedicalStockLoss.json`
- `POST /admin/createMedicalStockLoss.json`
- `POST /admin/getAdminInfo.json`
- `POST /admin/getCanBeProcessSkuInListOfProduct.json`
- `POST /admin/getChainMachineCenterOfMine.json`
- `POST /admin/getCompanyMachineCenterOfMine.json`
- `POST /admin/getMachineCenterCashflowVo.json`
- `POST /admin/getMachineCenterOrder.json`
- `POST /admin/getMedicalRecord.json`
- `POST /admin/getMedicalStockLossVo.json`
- `POST /admin/getMethodGlassRecordVo.json`
- `POST /admin/isAdminRoleStateOK.json`
- `POST /admin/saveToBeProcessSkuInListOfProduct.json`
- `POST /admin/selectInStoreMachineCenterCashflowVoList.json`
- `POST /admin/selectMedicalStockLossVoList.json`
- `POST /admin/startMachineCenterOrder.json`
- `POST /admin/statMachineCenterCashflowStatusCount.json`

## §3 逐页字段规格

### 15.1 `goods.companyStockList`

- **URL**：`/companyStockList`
- **模板**：`views/machineCenter/companyStockList.html`
- **控制器**：`companyStockListCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `closeMedicalStockLoss` | `POST /admin/closeMedicalStockLoss.json` |
| `completeMedicalStockLoss` | `POST /admin/completeMedicalStockLoss.json` |
| `getChainMachineCenterOfMine` | `POST /admin/getChainMachineCenterOfMine.json` |
| `getCompanyMachineCenterOfMine` | `POST /admin/getCompanyMachineCenterOfMine.json` |
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectMedicalStockLossVoList` | `POST /admin/selectMedicalStockLossVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登记日期 |
| 2 | 制单人 |
| 3 | 报损责任人 |
| 4 | 审核人 |
| 5 | 审核时间 |
| 6 | 来源 |
| 7 | 仓库 |
| 8 | 状态 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.keyword` |
| `obj.customerKeyword` |
| `obj.createKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getMachineCenterIdFactory.object.machineCenter.name` |
| `getMachineCenterIdFactory.object.storehouse.name` |
| `item.medicalStockLoss.lossDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalStockLoss.createName` |
| `item.lossAdmin.nickname` |
| `item.medicalStockLoss.checkName` |
| `item.medicalStockLoss.checkDate` |
| `item.machineCenter.name` |
| `item.storehouse.name` |
| `item.medicalStockLoss.checked` |
| `lossChecked` |
| `msg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `setStatus(2)` |

### 15.2 `chainStockList`

- **URL**：`/chainStockList`
- **模板**：`views/machineCenter/companyStockList.html`
- **控制器**：`companyStockListCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `closeMedicalStockLoss` | `POST /admin/closeMedicalStockLoss.json` |
| `completeMedicalStockLoss` | `POST /admin/completeMedicalStockLoss.json` |
| `getChainMachineCenterOfMine` | `POST /admin/getChainMachineCenterOfMine.json` |
| `getCompanyMachineCenterOfMine` | `POST /admin/getCompanyMachineCenterOfMine.json` |
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectMedicalStockLossVoList` | `POST /admin/selectMedicalStockLossVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登记日期 |
| 2 | 制单人 |
| 3 | 报损责任人 |
| 4 | 审核人 |
| 5 | 审核时间 |
| 6 | 来源 |
| 7 | 仓库 |
| 8 | 状态 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.keyword` |
| `obj.customerKeyword` |
| `obj.createKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getMachineCenterIdFactory.object.machineCenter.name` |
| `getMachineCenterIdFactory.object.storehouse.name` |
| `item.medicalStockLoss.lossDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalStockLoss.createName` |
| `item.lossAdmin.nickname` |
| `item.medicalStockLoss.checkName` |
| `item.medicalStockLoss.checkDate` |
| `item.machineCenter.name` |
| `item.storehouse.name` |
| `item.medicalStockLoss.checked` |
| `lossChecked` |
| `msg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `setStatus(2)` |

### 15.3 `goods.completeStockLoss`

- **URL**：`/completeStockLoss?stockLossId`
- **模板**：`views/machineCenter/completeStockLoss.html`
- **控制器**：`completeStockLossCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 数量 |
| 5 | 报损原因 |
| 6 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |
| `completeLoss()` |
| `completeLoss(1)` |

### 15.4 `completeChainStockLoss`

- **URL**：`/completeChainStockLoss?stockLossId`
- **模板**：`views/machineCenter/completeStockLoss.html`
- **控制器**：`completeStockLossCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 数量 |
| 5 | 报损原因 |
| 6 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |
| `completeLoss()` |
| `completeLoss(1)` |

### 15.5 `machineOrder`

- **URL**：`/machineOrder`
- **模板**：`views/machineCenter/machineOrder.html`
- **控制器**：`machineOrderCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `closeMachineCenterOrder` | `POST /admin/closeMachineCenterOrder.json` |
| `completeMachineCenterOrder` | `POST /admin/completeMachineCenterOrder.json` |
| `getCanBeProcessSkuInListOfProduct` | `POST /admin/getCanBeProcessSkuInListOfProduct.json` |
| `getMachineCenterOrder` | `POST /admin/getMachineCenterOrder.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `saveToBeProcessSkuInListOfProduct` | `POST /admin/saveToBeProcessSkuInListOfProduct.json` |
| `selectInStoreMachineCenterCashflowVoList` | `POST /admin/selectInStoreMachineCenterCashflowVoList.json` |
| `startMachineCenterOrder` | `POST /admin/startMachineCenterOrder.json` |

**表单标签**

| 标签 |
|---|
| 查看处方 |
| 查看来源 |
| 右 |
| 左 |
| BI |
| BO |
| BU |
| BD |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 用户 |
| 2 | 联系人 |
| 3 | 接诊{{corpInfo.employeeTitle}}/时间 |
| 4 | {{corpInfo. companyTitle}} |
| 5 | 配镜时间 取镜时间 状态 操作 |
| 6 | 用户 |
| 7 | 处方 |
| 8 | 商品基本信息 规格 折后金额 状态 |
| 9 | 操作 |
| 10 | 品牌/类目 |
| 11 | 商品基本信息 |
| 12 | 规格 |
| 13 | 下单数量 |
| 14 | 批号 有效期 剩余数量 发货数量 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.keyword` |
| `toggle` |
| `mainOpticEye` |
| `methodGlassRecord.right83` |
| `methodGlassRecord.left83` |
| `methodGlassRecord.right84` |
| `methodGlassRecord.left84` |
| `iten.deliveryCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
| `corpInfo.` |
| `companyTitle` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.medicalRecord.doctorName` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.hospitalName` |
| `iten.machineCenterOrder.gmtCreate` |
| `iten.machineCenterOrder.planDeliveryTime` |
| `iten.machineCenterOrder.status` |
| `machineOrder` |
| `item.methodGlassRecord.right15` |
| `item.methodGlassRecord.left15` |
| `item.methodGlassRecord.right14` |
| `item.methodGlassRecord.left14` |
| `item.methodGlassRecord.right13` |
| `item.methodGlassRecord.left13` |
| `iten.medicalProduct.productName` |
| `iten.medicalProduct.marketPrice` |
| `iten.medicalProduct.unitName` |
| `iten.medicalProduct.useCount` |
| `iten.brand.brandName` |
| `iten.medicalProduct.skuCode` |
| `iten.category.categoryName` |
| `iten.product.factory` |
| `ite.modelName` |
| `ite.modelValue` |
| `iten.product.model1Name` |
| `iten.medicalProduct.model1` |
| `printModel` |
| `iten.product.model2Name` |
| `iten.medicalProduct.model2` |
| `iten.medicalProduct.remark` |
| `iten.medicalProduct.rateFee` |
| `RecordVoFactory.result.object.medicalCode` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right15` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right14` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right13` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right12` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left15` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left14` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left13` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left12` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right24` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left24` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right85` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left85` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right86` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left86` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right1` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left1` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right82` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left82` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right81` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left81` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right29` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left29` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left67` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `itea.modelName` |
| `itea.modelValue` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSkuExistCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `startOrder(iten.machineCenterOrder.id,iten.medicalRecord.id,$index)` |
| `completeOrder(iten.machineCenterOrder.id,iten.medicalRecord.id,$index)` |
| `showRecord(item.medicalRecord.id)` |
| `print(item.machineCenterOrder.id)` |
| `processProduct(item.cashflow.id,item.medicalRecord.id,$index)` |
| `hideAddModal()` |
| `saveStock()` |
| `stockDetail=false` |

### 15.6 `machineOrderBroken`

- **URL**：`/machineOrderBroken?cashflowId&machineCenterId&chain`
- **模板**：`views/machineCenter/machineOrderBroken.html`
- **控制器**：`machineOrderBrokenCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeMachineCenterOrder` | `POST /admin/completeMachineCenterOrder.json` |
| `createMedicalStockLoss` | `POST /admin/createMedicalStockLoss.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getMachineCenterCashflowVo` | `POST /admin/getMachineCenterCashflowVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目/生产厂家 |
| 2 | 商品基本信息 |
| 3 | 规格 |
| 4 | 下单数量 |
| 5 | 批号 生产日期 有效期 唯一标识码 领料数量 报损 报损后，由仓库管理员在【本店物资】里审核通过后，重新领料，再完成制作。 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `lossCount` |
| `modal.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `itea.modelName` |
| `itea.modelValue` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.uniqueCode` |
| `iten.medicalProductStock.deliveryCount` |
| `productName` |
| `lossCount` |
| `adminname` |
| `machineCenterId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |
| `showLoss(iten.medicalProductStock.id,iten.medicalProductStock.deliveryCount,outerIndex)` |
| `completeOrder()` |
| `modifyLoss()` |
| `hideModal()` |

### 15.7 `machineOrderChainBroken`

- **URL**：`/machineOrderChainBroken?cashflowId&machineCenterId&chain`
- **模板**：`views/machineCenter/machineOrderBroken.html`
- **控制器**：`machineOrderBrokenCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeMachineCenterOrder` | `POST /admin/completeMachineCenterOrder.json` |
| `createMedicalStockLoss` | `POST /admin/createMedicalStockLoss.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getMachineCenterCashflowVo` | `POST /admin/getMachineCenterCashflowVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目/生产厂家 |
| 2 | 商品基本信息 |
| 3 | 规格 |
| 4 | 下单数量 |
| 5 | 批号 生产日期 有效期 唯一标识码 领料数量 报损 报损后，由仓库管理员在【本店物资】里审核通过后，重新领料，再完成制作。 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `lossCount` |
| `modal.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `itea.modelName` |
| `itea.modelValue` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.uniqueCode` |
| `iten.medicalProductStock.deliveryCount` |
| `productName` |
| `lossCount` |
| `adminname` |
| `machineCenterId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |
| `showLoss(iten.medicalProductStock.id,iten.medicalProductStock.deliveryCount,outerIndex)` |
| `completeOrder()` |
| `modifyLoss()` |
| `hideModal()` |

### 15.8 `machineOrderChainWaitAccess`

- **URL**：`/machineOrderChainWaitAccess`
- **模板**：`views/machineCenter/machineOrderChainWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `stockChainLossList`

### 15.9 `machineOrderChainWaitProcess`

- **URL**：`/machineOrderChainWaitProcess`
- **模板**：`views/machineCenter/machineOrderChainWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `stockChainLossList`

### 15.10 `machineOrderChainProcessing`

- **URL**：`/machineOrderChainProcessing`
- **模板**：`views/machineCenter/machineOrderChainWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `stockChainLossList`

### 15.11 `machineOrderChainTesting`

- **URL**：`/machineOrderChainTesting`
- **模板**：`views/machineCenter/machineOrderChainWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `stockChainLossList`

### 15.12 `machineOrderCompleted`

- **URL**：`/machineOrderCompleted?cashflowId&machineCenterId`
- **模板**：`views/machineCenter/machineOrderCompleted.html`
- **控制器**：`machineOrderBrokenCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeMachineCenterOrder` | `POST /admin/completeMachineCenterOrder.json` |
| `createMedicalStockLoss` | `POST /admin/createMedicalStockLoss.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getMachineCenterCashflowVo` | `POST /admin/getMachineCenterCashflowVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目/生产厂家 |
| 2 | 商品基本信息 |
| 3 | 规格 |
| 4 | 下单数量 |
| 5 | 批号 生产日期 有效期 唯一标识码 领料数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `itea.modelName` |
| `itea.modelValue` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.uniqueCode` |
| `iten.medicalProductStock.deliveryCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 15.13 `machineOrderChainCompleted`

- **URL**：`/machineOrderChainCompleted?cashflowId&machineCenterId`
- **模板**：`views/machineCenter/machineOrderCompleted.html`
- **控制器**：`machineOrderBrokenCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeMachineCenterOrder` | `POST /admin/completeMachineCenterOrder.json` |
| `createMedicalStockLoss` | `POST /admin/createMedicalStockLoss.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getMachineCenterCashflowVo` | `POST /admin/getMachineCenterCashflowVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目/生产厂家 |
| 2 | 商品基本信息 |
| 3 | 规格 |
| 4 | 下单数量 |
| 5 | 批号 生产日期 有效期 唯一标识码 领料数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `cashflowId` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.medicalProduct.productName` |
| `item.medicalProduct.marketPrice` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.skuCode` |
| `itea.modelName` |
| `itea.modelValue` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.medicalProduct.remark` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `iten.stockInSku.batchNo` |
| `iten.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.uniqueCode` |
| `iten.medicalProductStock.deliveryCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 15.14 `machineOrderWaitProcess`

- **URL**：`/machineOrderWaitProcess`
- **模板**：`views/machineCenter/machineOrderWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockLossList`

### 15.15 `machineOrderWaitAccess`

- **URL**：`/machineOrderWaitAccess`
- **模板**：`views/machineCenter/machineOrderWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockLossList`

### 15.16 `machineOrderProcessing`

- **URL**：`/machineOrderProcessing`
- **模板**：`views/machineCenter/machineOrderWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockLossList`

### 15.17 `machineOrderTesting`

- **URL**：`/machineOrderTesting`
- **模板**：`views/machineCenter/machineOrderWaitAccess.html`
- **控制器**：`machineOrderWaitProcessCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `centername` |
| `storehousename` |
| `countObj.waitAcceptCount` |
| `countObj.waitProcessCount` |
| `countObj.processingCount` |
| `countObj.completeCount` |
| `tab` |

**跳转到**：`machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockLossList`

### 15.18 `goods.stockLossDetail`

- **URL**：`/stockLossDetail?stockLossId`
- **模板**：`views/machineCenter/stockLossDetail.html`
- **控制器**：`stockLossDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 数量 |
| 5 | 报损原因 |
| 6 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.checkName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 15.19 `chainStockLossDetail`

- **URL**：`/chainStockLossDetail?stockLossId`
- **模板**：`views/machineCenter/stockLossDetail.html`
- **控制器**：`stockLossDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 规格 |
| 3 | 单位 |
| 4 | 数量 |
| 5 | 报损原因 |
| 6 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.checkName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 15.20 `stockLossList`

- **URL**：`/stockLossList`
- **模板**：`views/machineCenter/stockLossList.html`
- **控制器**：`stockLossListCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getChainMachineCenterOfMine` | `POST /admin/getChainMachineCenterOfMine.json` |
| `getCompanyMachineCenterOfMine` | `POST /admin/getCompanyMachineCenterOfMine.json` |
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |
| `selectMedicalStockLossVoList` | `POST /admin/selectMedicalStockLossVoList.json` |
| `statMachineCenterCashflowStatusCount` | `POST /admin/statMachineCenterCashflowStatusCount.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登记日期 |
| 2 | 制单人 |
| 3 | 报损责任人 |
| 4 | 审核人 |
| 5 | 审核时间 |
| 6 | 来源 |
| 7 | 仓库 |
| 8 | 状态 |
| 9 | 操作 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 单位 |
| 13 | 数量 |
| 14 | 报损原因 |
| 15 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.customerKeyword` |
| `obj.keyword` |
| `obj.createKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getMachineCenterIdFactory.object.machineCenter.name` |
| `getMachineCenterIdFactory.object.storehouse.name` |
| `getOrderCountFactory.object.waitAcceptCount` |
| `getOrderCountFactory.object.waitProcessCount` |
| `getOrderCountFactory.object.processingCount` |
| `getOrderCountFactory.object.completeCount` |
| `item.medicalStockLoss.lossDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalStockLoss.createName` |
| `item.lossAdmin.nickname` |
| `item.medicalStockLoss.checkName` |
| `item.medicalStockLoss.checkDate` |
| `item.machineCenter.name` |
| `item.storehouse.name` |
| `item.medicalStockLoss.checked` |
| `lossChecked` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.checkName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `setStatus(2)` |
| `showLossDetail(item.medicalStockLoss.id)` |
| `stockDetail=false` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockChainLossList`, `stockLossList`

### 15.21 `stockChainLossList`

- **URL**：`/stockChainLossList`
- **模板**：`views/machineCenter/stockLossList.html`
- **控制器**：`stockLossListCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getChainMachineCenterOfMine` | `POST /admin/getChainMachineCenterOfMine.json` |
| `getCompanyMachineCenterOfMine` | `POST /admin/getCompanyMachineCenterOfMine.json` |
| `getMedicalStockLossVo` | `POST /admin/getMedicalStockLossVo.json` |
| `selectMedicalStockLossVoList` | `POST /admin/selectMedicalStockLossVoList.json` |
| `statMachineCenterCashflowStatusCount` | `POST /admin/statMachineCenterCashflowStatusCount.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登记日期 |
| 2 | 制单人 |
| 3 | 报损责任人 |
| 4 | 审核人 |
| 5 | 审核时间 |
| 6 | 来源 |
| 7 | 仓库 |
| 8 | 状态 |
| 9 | 操作 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 单位 |
| 13 | 数量 |
| 14 | 报损原因 |
| 15 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.customerKeyword` |
| `obj.keyword` |
| `obj.createKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getMachineCenterIdFactory.object.machineCenter.name` |
| `getMachineCenterIdFactory.object.storehouse.name` |
| `getOrderCountFactory.object.waitAcceptCount` |
| `getOrderCountFactory.object.waitProcessCount` |
| `getOrderCountFactory.object.processingCount` |
| `getOrderCountFactory.object.completeCount` |
| `item.medicalStockLoss.lossDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalStockLoss.createName` |
| `item.lossAdmin.nickname` |
| `item.medicalStockLoss.checkName` |
| `item.medicalStockLoss.checkDate` |
| `item.machineCenter.name` |
| `item.storehouse.name` |
| `item.medicalStockLoss.checked` |
| `lossChecked` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.createName` |
| `getStockTakingObjectFactory.result.object.medicalStockLoss.checkName` |
| `getStockTakingObjectFactory.result.object.machineCenter.name` |
| `getStockTakingObjectFactory.result.object.storehouse.name` |
| `getStockTakingObjectFactory.result.object.lossAdmin.nickname` |
| `item.medicalProduct.productName` |
| `item.product.model1Name` |
| `item.medicalProduct.model1` |
| `item.product.model2Name` |
| `item.medicalProduct.model2` |
| `item.medicalProduct.unitName` |
| `item.medicalStockLossSku.lossCount` |
| `item.lossReason.reasonName` |
| `item.medicalStockLossSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `setStatus(2)` |
| `showLossDetail(item.medicalStockLoss.id)` |
| `stockDetail=false` |

**跳转到**：`machineOrderChainProcessing`, `machineOrderChainTesting`, `machineOrderChainWaitAccess`, `machineOrderChainWaitProcess`, `machineOrderProcessing`, `machineOrderTesting`, `machineOrderWaitAccess`, `machineOrderWaitProcess`, `stockChainLossList`, `stockLossList`
