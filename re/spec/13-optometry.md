# 13｜模块 optometry 验光配镜

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/optometry/` |
| 中文名 | 验光配镜 |
| 开发波次 | W7 |
| 页面数 | **2** |
| 端点数（去重） | **25** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `optometry` | `/optometry` | `views/optometry/optometry.html` | `optometryCtrl` | 16 |
| 2 | `optometryGlasses` | `/optometryGlasses?medicalRecordId&edit` | `views/optometry/optometryGlasses.html` | `optometryGlassesCtrl` | 10 |

## §2 端点清单（去重 25 个）

- `POST /admin/beginCustomerCheckin.json`
- `POST /admin/cancelMedicalRecord.json`
- `POST /admin/checkBeforeDeleteMedicalProduct.json`
- `POST /admin/completeMedicalRecordDelivery.json`
- `POST /admin/confirmMedicalRecordReturn.json`
- `POST /admin/createMedicalStockLossOfSmallVersion.json`
- `POST /admin/getAdminInfo.json`
- `POST /admin/getCanBeDeliverySkuInListOfProduct.json`
- `POST /admin/getCompanyOfMine.json`
- `POST /admin/getLoginEmployee.json`
- `POST /admin/getMedicalProductVoList.json`
- `POST /admin/getMedicalRecord.json`
- `POST /admin/getMedicalRecordFlowVo.json`
- `POST /admin/getMethodGlassRecordVo.json`
- `POST /admin/getProductSkuExistCountVoList.json`
- `POST /admin/insertCustomerCheckin.json`
- `POST /admin/saveMedicalProductListOfSmallVersion.json`
- `POST /admin/selectEmployeeVoListOfMyCompany.json`
- `POST /admin/selectMedicalProductStockList.json`
- `POST /admin/selectMedicalRecordFlowVoList.json`
- `POST /admin/selectStorehouseListOfCompany.json`
- `POST /admin/sendTakeMirrorNotice.json`
- `POST /admin/setMedicalRecordProcessMode.json`
- `POST /admin/stateTodoMedicalRecordCount.json`
- `POST /admin/updateMethodGlassRecord.json`

## §3 逐页字段规格

### 13.1 `optometry`

- **URL**：`/optometry`
- **模板**：`views/optometry/optometry.html`
- **控制器**：`optometryCtrl`
- **端点数**：16

**调用的端点**

| 动作 | 端点 |
|---|---|
| `beginCustomerCheckin` | `POST /admin/beginCustomerCheckin.json` |
| `cancelMedicalRecord` | `POST /admin/cancelMedicalRecord.json` |
| `completeMedicalRecordDelivery` | `POST /admin/completeMedicalRecordDelivery.json` |
| `confirmMedicalRecordReturn` | `POST /admin/confirmMedicalRecordReturn.json` |
| `createMedicalStockLossOfSmallVersion` | `POST /admin/createMedicalStockLossOfSmallVersion.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getCanBeDeliverySkuInListOfProduct` | `POST /admin/getCanBeDeliverySkuInListOfProduct.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getLoginEmployee` | `POST /admin/getLoginEmployee.json` |
| `getMedicalRecordFlowVo` | `POST /admin/getMedicalRecordFlowVo.json` |
| `insertCustomerCheckin` | `POST /admin/insertCustomerCheckin.json` |
| `selectMedicalProductStockList` | `POST /admin/selectMedicalProductStockList.json` |
| `selectMedicalRecordFlowVoList` | `POST /admin/selectMedicalRecordFlowVoList.json` |
| `sendTakeMirrorNotice` | `POST /admin/sendTakeMirrorNotice.json` |
| `setMedicalRecordProcessMode` | `POST /admin/setMedicalRecordProcessMode.json` |
| `stateTodoMedicalRecordCount` | `POST /admin/stateTodoMedicalRecordCount.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 日期 |
| 2 | 订单号 |
| 3 | 用户信息 |
| 4 | 视光师 |
| 5 | 类型 |
| 6 | 收费 |
| 7 | 状态 |
| 8 | 操作 |
| 9 | 品牌/类目 |
| 10 | 商品基本信息 |
| 11 | 规格 |
| 12 | 数量 |
| 13 | 出库仓 |
| 14 | 折后金额 |
| 15 | 合计 |
| 16 | 报损数量 |
| 17 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTime` |
| `modal.shopInfo.useCount` |
| `modal.shopInfo.remark` |
| `obj.keyword` |
| `obj.productKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyName` |
| `order.name` |
| `route.name` |
| `toPayCount` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.medicalCode` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.medicalRecord.secondDoctorName` |
| `item.medicalRecord.medicalRecordType` |
| `medicalRecordType` |
| `filter_medicalRecordStatus` |
| `item` |
| `fee` |
| `name` |
| `status` |
| `btn.name` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.refundCount` |
| `item.lockStorehouse.name` |
| `item.medicalProduct.rateFee` |
| `order.object.medicalProductVoList.length` |
| `order.object.rateFee` |
| `order.object.totalRefundFee` |
| `item.lossCount` |
| `item.medicalProduct.remark` |
| `item.gmtCreate` |
| `HH` |
| `mm` |
| `item.content` |
| `item.createName` |
| `modal.shopInfo.productName` |
| `modal.shopInfo.adminname` |
| `modal.shopInfo.machineCenterId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `orderList.click()` |
| `orderList.open(true,$event)` |
| `orderList.setType(order.status)` |
| `routeClick($index)` |
| `open1()` |
| `open2()` |
| `order.show(true,item.medicalRecord.id)` |
| `addUser.editInfo(item)` |
| `clickBtn(btn.name,item,index)` |
| `printPeijing.print(item.cashflow.id,item.medicalRecord.id)` |
| `order.show(false)` |
| `modal.changeOrder(true,$index)` |
| `modal.affrim()` |
| `modal.changeOrder(false)` |

### 13.2 `optometryGlasses`

- **URL**：`/optometryGlasses?medicalRecordId&edit`
- **模板**：`views/optometry/optometryGlasses.html`
- **控制器**：`optometryGlassesCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalProduct` | `POST /admin/checkBeforeDeleteMedicalProduct.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getMedicalProductVoList` | `POST /admin/getMedicalProductVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `getProductSkuExistCountVoList` | `POST /admin/getProductSkuExistCountVoList.json` |
| `saveMedicalProductListOfSmallVersion` | `POST /admin/saveMedicalProductListOfSmallVersion.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectStorehouseListOfCompany` | `POST /admin/selectStorehouseListOfCompany.json` |
| `updateMethodGlassRecord` | `POST /admin/updateMethodGlassRecord.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |
| * 性别 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| * 性别 |
| 男 女 出生年月 |
| 手机号 |
| 会员来源 |
| 备注 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 眼别/测试项 |
| 2 | * 球镜S |
| 3 | * 柱镜C |
| 4 | 轴位A |
| 5 | 瞳距 |
| 6 | 瞳高 |
| 7 | 矫正视力 |
| 8 | 裸眼视力 |
| 9 | 棱镜 |
| 10 | 下加光 |
| 11 | 主视眼 |
| 12 | 品牌/类目 |
| 13 | 商品规格信息 |
| 14 | 规格 |
| 15 | 下单仓库 |
| 16 | 可售库存 |
| 17 | 下单数量 |
| 18 | 备注 |
| 19 | 操作 |
| 20 | 品牌/类目 |
| 21 | 商品规格信息 |
| 22 | 规格 |
| 23 | 下单仓库 |
| 24 | 可售库存 |
| 25 | 下单数量 |
| 26 | 备注 |
| 27 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `userInfo.patientGender` |
| `userInfo.patientBirthday` |
| `userInfo.patientRemark` |
| `object.right15` |
| `object.right14` |
| `object.right13` |
| `object.right24` |
| `object.right81` |
| `object.right12` |
| `object.right1` |
| `object.right83` |
| `object.right85` |
| `object.right82` |
| `object.right45` |
| `object.left45` |
| `object.left15` |
| `object.left14` |
| `object.left13` |
| `object.left24` |
| `object.left81` |
| `object.left12` |
| `object.left1` |
| `object.left83` |
| `object.left85` |
| `object.left82` |
| `object.lastRxTime` |
| `glassesInfo.model1Keyword1` |
| `glassesInfo.model2Keyword1` |
| `glassesInfo.model1Keyword2` |
| `glassesInfo.model2Keyword2` |
| `item.useCount` |
| `item.remark` |
| `userInfo.patientName` |
| `userInfo.linkMobile` |
| `object.right91` |
| `object.left91` |
| `object.rxCount` |
| `object.left67` |
| `glassesInfo.keyword1` |
| `glassesInfo.priceFromInclude1` |
| `glassesInfo.priceToInclude1` |
| `glassesInfo.remark1` |
| `glassesInfo.keyword2` |
| `glassesInfo.priceFromInclude2` |
| `glassesInfo.priceToInclude2` |
| `glassesInfo.remark2` |
| `glassesInfo.keyword3` |
| `glassesInfo.priceFromInclude3` |
| `glassesInfo.priceToInclude3` |
| `glassesInfo.remark3` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `medicalRecord.medicalRecordType` |
| `medicalRecord.medicalCode` |
| `userInfo.avatar` |
| `userInfo.name` |
| `userInfo.gender` |
| `gender` |
| `userInfo.mobile` |
| `userInfo.channel` |
| `companyName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.product.productCode` |
| `glassesInfo.unLockExistSkuCount1` |
| `glassesInfo.marketPrice1` |
| `glassesInfo.unLockExistSkuCount2` |
| `glassesInfo.marketPrice2` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `glassesInfo.unLockExistSkuCount3` |
| `glassesInfo.marketPrice3` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.storeName` |
| `item.unLockExistSkuCount` |
| `item.placeOrderStatus` |
| `item.deliveryStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `prevent($event)` |
| `updateImg()` |
| `upOther(` |
| `dateCom.open($event)` |
| `showCommon()` |
| `updatePatient()` |
| `update2(` |
| `open1()` |
| `printChufang.print()` |
| `showsupplierList($event,` |
| `setProduct(item,` |
| `deleteReceipt($index,item.id)` |
| `addStore.switch(true)` |
| `printShoufei.print()` |
| `save()` |
