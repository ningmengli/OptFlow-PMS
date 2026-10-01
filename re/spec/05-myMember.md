# 05｜模块 myMember 我的会员

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/myMember/` |
| 中文名 | 我的会员 |
| 开发波次 | W1 |
| 页面数 | **18** |
| 端点数（去重） | **78** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addSaleRecord` | `/addSaleRecord` | `views/myMember/addSaleRecord.html` | `addSaleRecordCtrl` | 2 |
| 2 | `adminMyRecord` | `/adminMyRecord?medicalRecordId` | `views/myMember/adminMyRecord.html` | `adminMyRecordCtrl` | 5 |
| 3 | `adminSalesRecord` | `/adminSalesRecord?medicalRecordId` | `views/myMember/adminSalesRecord.html` | `adminSalesRecordCtrl` | 3 |
| 4 | `adminMyRecord.customerProductRecord` | `/customerProductRecord` | `views/myMember/customerProductRecord.html` | `customerProductRecordCtrl` | 9 |
| 5 | `adminMyRecord.drugPrescription` | `/drugPrescription` | `views/myMember/drugPrescription.html` | `drugPrescriptionCtrl` | 8 |
| 6 | `adminMyRecord.followList` | `/followList` | `views/myMember/followList.html` | `followListCtrl` | 12 |
| 7 | `adminMyRecord.myCheckBill` | `/myCheckBill` | `views/myMember/myCheckBill.html` | `myCheckBillCtrl` | 8 |
| 8 | `adminMyRecord.myMaterialBill` | `/myMaterialBill` | `views/myMember/myMaterialBill.html` | `myMaterialBillCtrl` | 18 |
| 9 | `adminSalesRecord.myMaterialBill` | `/myMaterialBill` | `views/myMember/myMaterialBill.html` | `myMaterialBillCtrl` | 18 |
| 10 | `myMedicalHistory` | `/myMedicalHistory?patientId` | `views/myMember/myMedicalHistory.html` | `myMedicalHistoryCtrl` | 0 |
| 11 | `myMedicalRecordList` | `/myMedicalRecordList?patientId&customerId` | `views/myMember/myMedicalRecordList.html` | `myMedicalRecordListCtrl` | 0 |
| 12 | `myMember` | `/myMember` | `views/myMember/myMember.html` | `myMemberCtrl` | 5 |
| 13 | `adminMyRecord.myMemberRecord` | `/myMemberRecord` | `views/myMember/myMemberRecord.html` | `myMemberRecordCtrl` | 10 |
| 14 | `adminSalesRecord.myMemberRecord` | `/myMemberRecord` | `views/myMember/myMemberRecord.html` | `myMemberRecordCtrl` | 10 |
| 15 | `adminMyRecord.prescription` | `/prescription` | `views/myMember/prescription.html` | `prescriptionCtrl` | 4 |
| 16 | `adminMyRecord.prescriptsRecord` | `/prescriptsRecord` | `views/myMember/prescriptsRecord.html` | `prescriptsRecordCtrl` | 10 |
| 17 | `timeCard` | `/timeCard` | `views/myMember/timeCard.html` | `timeCardCtrl` | 16 |
| 18 | `updateMyMember` | `/updateMyMember?customerId` | `views/myMember/updateMyMember.html` | `updateMemberCtrl` | 7 |

## §2 端点清单（去重 78 个）

- `POST /admin/addMedicalRecord.json`
- `POST /admin/addRegistrationFee.json`
- `POST /admin/addRemind.json`
- `POST /admin/beginCustomerCheckin.json`
- `POST /admin/cancelFollowUp.json`
- `POST /admin/checkBeforeDeleteMedicalExamine.json`
- `POST /admin/checkBeforeDeleteMedicalProduct.json`
- `POST /admin/consumeCustomerTrainerCardNumbers.json`
- `POST /admin/deleteNews.json`
- `POST /admin/disBandingWechatByCustomerId.json`
- `POST /admin/getAdminInfo.json`
- `POST /admin/getBandingWechatQrcode.json`
- `POST /admin/getBrandListOfProduct.json`
- `POST /admin/getCompanyCashConf.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCompanyOfMine.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getCustomerTrainerCard.json`
- `POST /admin/getCustomerVo.json`
- `POST /admin/getExamineVoList.json`
- `POST /admin/getHaveOrderMedicalRecordVoList.json`
- `POST /admin/getIntroducerList.json`
- `POST /admin/getMedicalExamineVoList.json`
- `POST /admin/getMedicalProductModelList.json`
- `POST /admin/getMedicalProductVoList.json`
- `POST /admin/getMedicalRecord.json`
- `POST /admin/getMedicalRecordList.json`
- `POST /admin/getMedicalRecordListOfDoctor.json`
- `POST /admin/getMethodGlassRecordVo.json`
- `POST /admin/getNews.json`
- `POST /admin/getNewsCategoryTree2Level.json`
- `POST /admin/getOkReceivedRecordVo.json`
- `POST /admin/getOkReviewRecordVo.json`
- `POST /admin/getPackageProductVo.json`
- `POST /admin/getPatientInfo.json`
- `POST /admin/getProductSkuExistCountVoList.json`
- `POST /admin/getProductSkuModelVoList.json`
- `POST /admin/getRegistrationFee.json`
- `POST /admin/getStockConf.json`
- `POST /admin/getStorehouseVo.json`
- `POST /admin/getVisionRecordVo.json`
- `POST /admin/insertMedicalRecordTemplate.json`
- `POST /admin/insertNews.json`
- `POST /admin/investMoneyForCustomerTrainerCard.json`
- `POST /admin/isBandingWechat.json`
- `POST /admin/receiveSelfAndBeginCustomerCheckin.json`
- `POST /admin/saveCustomerInfo.json`
- `POST /admin/saveMedicalExamineVoList.json`
- `POST /admin/saveMedicalProductList.json`
- `POST /admin/saveMedicalProductModelList.json`
- `POST /admin/saveOkReceivedRecord.json`
- `POST /admin/saveOkReviewRecord.json`
- `POST /admin/selectCorpMedicalConfByCorpId.json`
- `POST /admin/selectCustomerCheckinVoListOfCompany.json`
- `POST /admin/selectCustomerCheckinVoListOfEmployee.json`
- `POST /admin/selectCustomerList.json`
- `POST /admin/selectCustomerTrainerCardVoList.json`
- `POST /admin/selectEmployeeByName.json`
- `POST /admin/selectEmployeeVoListOfMyCompany.json`
- `POST /admin/selectFirstCustomerTrainerCardLog.json`
- `POST /admin/selectFollowUpVoList.json`
- `POST /admin/selectMedicalRecordTemplateVoList.json`
- `POST /admin/selectModelValueList.json`
- `POST /admin/selectNewsList.json`
- `POST /admin/selectPackageVoList.json`
- `POST /admin/selectPosDeviceListOfCompany.json`
- `POST /admin/selectRemindList.json`
- `POST /admin/selectStorehouseExistSkuCountVoList.json`
- `POST /admin/selectStorehouseListOfCompany.json`
- `POST /admin/selectTagList.json`
- `POST /admin/selectTrainerCardList.json`
- `POST /admin/startExamine.json`
- `POST /admin/statMedicalRecordFeeCount.json`
- `POST /admin/updateCustomerTags.json`
- `POST /admin/updateMedicalRecord.json`
- `POST /admin/updateMethodGlassRecord.json`
- `POST /admin/updateNews.json`
- `POST /admin/viewSalesRecordFee.json`

## §3 逐页字段规格

### 5.1 `addSaleRecord`

- **URL**：`/addSaleRecord`
- **模板**：`views/myMember/addSaleRecord.html`
- **控制器**：`addSaleRecordCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addMedicalRecord` | `POST /admin/addMedicalRecord.json` |
| `getHaveOrderMedicalRecordVoList` | `POST /admin/getHaveOrderMedicalRecordVoList.json` |

**表单标签**

| 标签 |
|---|
| 包含未开单的病历 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 用户 |
| 2 | 联系人 |
| 3 | 接诊{{corpInfo.employeeTitle}}/时间 |
| 4 | 品牌/类目 |
| 5 | 商品信息 |
| 6 | 规格 |
| 7 | 数量 |
| 8 | 折后金额 |
| 9 | 合计 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.firstVisitFrom` |
| `rightTime` |
| `hasPoint` |
| `data.keyword` |
| `data.productKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
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
| `iten.brand.brandName` |
| `iten.category.categoryName` |
| `iten.product.productName` |
| `iten.product.factory` |
| `iten.productSku.marketPrice` |
| `iten.productSku.unitName` |
| `iten.product.productCode` |
| `iten.productSku.skuCode` |
| `iten.product.model1Name` |
| `iten.productSku.model1` |
| `iten.product.model2Name` |
| `iten.productSku.model2` |
| `iten.medicalProduct.useCount` |
| `iten.medicalProduct.refundCount` |
| `iten.medicalProduct.rateFee` |
| `iten.medicalProduct` |
| `refundAndPayStatus` |
| `item.medicalProductRateFee` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `choseUser.open()` |
| `setTab(4)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `goRecord(item.medicalRecord.id,item.medicalRecord.medicalRecordType,item.patient.id)` |

### 5.2 `adminMyRecord`

- **URL**：`/adminMyRecord?medicalRecordId`
- **模板**：`views/myMember/adminMyRecord.html`
- **控制器**：`adminMyRecordCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `selectCorpMedicalConfByCorpId` | `POST /admin/selectCorpMedicalConfByCorpId.json` |
| `statMedicalRecordFeeCount` | `POST /admin/statMedicalRecordFeeCount.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `updatePatientFactory.object.patientName` |
| `updatePatientFactory.object.patientGender` |
| `gender` |
| `date.checkYear` |
| `addAge` |
| `updatePatientFactory.object.height` |
| `updatePatientFactory.object.weight` |
| `customerInfoFactory.vo.customer.customerName` |
| `customerInfoFactory.vo.customer.linkMobile` |
| `hidePhone` |
| `updatePatientFactory.object.idCard` |
| `updatePatientFactory.object.patientRemark` |
| `countFactory.result.vo.medicalExamineCount` |
| `countFactory.result.vo.medicalProductCount` |
| `countFactory.result.vo.medicalProductCountOfModel` |
| `tabSave` |
| `medicalRecordId` |
| `patientId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `showEndClinic()` |
| `showFee()` |
| `showPatientModal()` |
| `showHistoryModal()` |
| `screenCalibrationRecord.open(updatePatientFactory,customerInfoFactory)` |
| `setTab(1)` |
| `setTab(4)` |
| `setTab(6)` |
| `setTab(7)` |
| `setTab(9)` |
| `setTab(5)` |
| `setTab(8)` |
| `setTab(2)` |
| `hidePatient()` |
| `hideHistory()` |

### 5.3 `adminSalesRecord`

- **URL**：`/adminSalesRecord?medicalRecordId`
- **模板**：`views/myMember/adminSalesRecord.html`
- **控制器**：`adminSalesRecordCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `updatePatientFactory.object.patientName` |
| `updatePatientFactory.object.patientGender` |
| `gender` |
| `date.checkYear` |
| `addAge` |
| `updatePatientFactory.object.height` |
| `updatePatientFactory.object.weight` |
| `customerInfoFactory.vo.customer.customerName` |
| `customerInfoFactory.vo.customer.linkMobile` |
| `tabSave` |
| `medicalRecordId` |
| `patientId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `showEndClinic()` |
| `showFee()` |
| `showPatientModal()` |
| `showHistoryModal()` |
| `screenCalibrationRecord.open(updatePatientFactory,customerInfoFactory)` |
| `setTab(1)` |
| `setTab(2)` |
| `hidePatient()` |
| `hideHistory()` |

### 5.4 `adminMyRecord.customerProductRecord`

- **URL**：`/customerProductRecord`
- **模板**：`views/myMember/customerProductRecord.html`
- **控制器**：`customerProductRecordCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalProduct` | `POST /admin/checkBeforeDeleteMedicalProduct.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getMedicalProductModelList` | `POST /admin/getMedicalProductModelList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getProductSkuModelVoList` | `POST /admin/getProductSkuModelVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `saveMedicalProductModelList` | `POST /admin/saveMedicalProductModelList.json` |
| `selectModelValueList` | `POST /admin/selectModelValueList.json` |
| `selectStorehouseListOfCompany` | `POST /admin/selectStorehouseListOfCompany.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.useCount` |
| `item.remark` |
| `iten.modelValue` |
| `select.brandId` |
| `select.keyword` |
| `select.priceFromInclude` |
| `select.priceToInclude` |
| `product.productSku` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.productCode` |
| `item.storeName` |
| `item.placeOrderStatus` |
| `item.deliveryStatus` |
| `iten.modelName` |
| `item.value` |
| `province.id` |
| `province.brandName` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `iten.modelName.name` |
| `item.productModelVoList` |
| `modelName.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `deleteReceipt($index,item.id)` |
| `getModelValue(iten.modelNameId,outerIndex,innerIndex,$event)` |
| `selectModelName(item.value)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item)` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `hideProductModal()` |

### 5.5 `adminMyRecord.drugPrescription`

- **URL**：`/drugPrescription`
- **模板**：`views/myMember/drugPrescription.html`
- **控制器**：`drugPrescriptionCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalProduct` | `POST /admin/checkBeforeDeleteMedicalProduct.json` |
| `getMedicalProductVoList` | `POST /admin/getMedicalProductVoList.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `getProductSkuExistCountVoList` | `POST /admin/getProductSkuExistCountVoList.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `saveMedicalProductList` | `POST /admin/saveMedicalProductList.json` |
| `selectStorehouseListOfCompany` | `POST /admin/selectStorehouseListOfCompany.json` |
| `updateMethodGlassRecord` | `POST /admin/updateMethodGlassRecord.json` |

**表单标签**

| 标签 |
|---|
| 可售库存大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 处方笺(档案编号：{{visionRecordVo.medicalRecord.medicalCode}}) 患者姓名 性别 年龄 {{visionRecordVo.patient.patientBirthday \| howoldFilter}} 开具日期 {{visionRecordVo.medicalRecord.firstVisit\| date:'yyyy-MM-dd'}} 医师 {{visionRecordVo.medicalRecord.doctorName}} 临床诊断 RP 名称 |
| 2 | 规格 |
| 3 | 剂型 |
| 4 | 数量 |
| 5 | 单价 |
| 6 | 单位 |
| 7 | 生产厂家 |
| 8 | 用法用量 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.medicalProduct.useCount` |
| `item.medicalProduct.productUsage` |
| `modifyGlassRecordVo.left67` |
| `select.keyword` |
| `select.model1Keyword` |
| `select.model2Keyword` |
| `select.priceFromInclude` |
| `select.priceToInclude` |
| `select.unLockMoreThanZero` |
| `modifyGlassRecordVo.left68` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `visionRecordVo.medicalRecord.medicalCode` |
| `visionRecordVo.patient.patientBirthday` |
| `howoldFilter` |
| `visionRecordVo.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `visionRecordVo.medicalRecord.doctorName` |
| `item.product.productName` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.product.productSpecialItem.medicineDosageform` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `stockInSkuTotalPrice` |
| `toFixed` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.unLockExistSkuCount` |
| `item.allUnLockExistSkuCount` |
| `val.storehouse.name` |
| `val.unLockExistSkuCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteReceipt($index,item.medicalProduct.id)` |
| `choseProduct(true)` |
| `addDelivery()` |
| `printChufangjian.print()` |
| `searchProductWord()` |
| `selectProductName($index)` |
| `showStockModel(item.productSku.id,$event)` |
| `$event.stopPropagation()` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `choseProduct(false)` |

### 5.6 `adminMyRecord.followList`

- **URL**：`/followList`
- **模板**：`views/myMember/followList.html`
- **控制器**：`followListCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addRemind` | `POST /admin/addRemind.json` |
| `cancelFollowUp` | `POST /admin/cancelFollowUp.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getIntroducerList` | `POST /admin/getIntroducerList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getOkReceivedRecordVo` | `POST /admin/getOkReceivedRecordVo.json` |
| `saveOkReceivedRecord` | `POST /admin/saveOkReceivedRecord.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectFollowUpVoList` | `POST /admin/selectFollowUpVoList.json` |
| `selectRemindList` | `POST /admin/selectRemindList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 随访状态 |
| 2 | 计划随访时间 |
| 3 | 随访内容 |
| 4 | 随访结论 |
| 5 | 创建人员 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `remind.remindTime` |
| `payChannel` |
| `remind.remindContent` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.followUp.planExcuteTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.followUp.followUpContent` |
| `item.followUp.followUpResult` |
| `item.createAdmin.nickname` |
| `corpInfo.employeeTitle` |
| `getDoctorPhoneObjectFactory.result.object.mobile` |
| `getHospitalPhoneObjectFactory.result.object.servicePhone` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePatient()` |
| `showModal()` |
| `gotoPath(null,2)` |
| `gotoPath(item,item.followUp.followUpStatus)` |
| `updateFollow(item.followUp.id,$event)` |
| `gotoPath(item,item.followUp.followUpStatus,true)` |
| `gotoPath(item,item.followUp.followUpStatus,false)` |
| `getCancelReason.fn(item)` |
| `hideModal()` |
| `open1()` |
| `setPhone(getDoctorPhoneObjectFactory.result.object.mobile)` |
| `setPhone(getHospitalPhoneObjectFactory.result.object.servicePhone)` |
| `addRemind()` |

### 5.7 `adminMyRecord.myCheckBill`

- **URL**：`/myCheckBill`
- **模板**：`views/myMember/myCheckBill.html`
- **控制器**：`myCheckBillCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalExamine` | `POST /admin/checkBeforeDeleteMedicalExamine.json` |
| `getCompanyCashConf` | `POST /admin/getCompanyCashConf.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getMedicalExamineVoList` | `POST /admin/getMedicalExamineVoList.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `saveMedicalExamineVoList` | `POST /admin/saveMedicalExamineVoList.json` |
| `selectPackageVoList` | `POST /admin/selectPackageVoList.json` |
| `startExamine` | `POST /admin/startExamine.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 套餐名称 |
| 2 | 检查单 |
| 3 | 折扣 |
| 4 | 金额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.remark` |
| `keyword` |
| `examine.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.productName` |
| `item.mark` |
| `item.useCount` |
| `item.placeOrderStatus` |
| `item.payedStatus` |
| `productKeyword` |
| `item.examine.examineName` |
| `item.examine.remark` |
| `printCount` |
| `item.pkg.packageName` |
| `iten.examineName` |
| `item.pkg.packageRate` |
| `item.pkg.packageFee` |
| `companyFactory.object.cashLogo` |
| `companyFactory.object.cashHeader` |
| `iten.medicalExamine.examineName` |
| `iten.medicalExamine.payedStatus` |
| `payedStatus` |
| `visionRecordVoFactory.vo.patient.patientName` |
| `visionRecordVoFactory.vo.patient.patientGender` |
| `gender` |
| `visionRecordVoFactory.vo.patient.patientBirthday` |
| `howoldFilter` |
| `visionRecordVoFactory.vo.medicalRecord.medicalCode` |
| `visionRecordVoFactory.vo.customer.customerName` |
| `visionRecordVoFactory.vo.customer.linkMobile` |
| `hidePhone` |
| `index` |
| `item.leftName` |
| `item.left` |
| `item.rightName` |
| `item.right` |
| `item` |
| `iten.medicalExamine.checkDescription` |
| `iten.medicalExamine.checkComment` |
| `iten.medicalExamine.createName` |
| `iten.medicalExamine.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `iten.medicalExamine.checkPersonName` |
| `iten.medicalExamine.checkTime` |
| `item.medicalExamine.examineName` |
| `item.consultRoomList` |
| `concatStr` |
| `consultRoomName` |
| `consultRoomAddress` |
| `item.medicalExamine.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `showModal()` |
| `deleteReceipt($index,item.checkStatus,item.id)` |
| `goAssist(item.id,item.checkStatus)` |
| `showEmployee($event)` |
| `searchProduct(keyword,$event)` |
| `selectProductId(item.examine.examineName,item,item.examine.id)` |
| `addDelivery()` |
| `print()` |
| `printJianchadan.print()` |
| `selectProductIdArr(item.examinePackageVoList)` |
| `checkbillModal=false` |

### 5.8 `adminMyRecord.myMaterialBill`

- **URL**：`/myMaterialBill`
- **模板**：`views/myMember/myMaterialBill.html`
- **控制器**：`myMaterialBillCtrl`
- **端点数**：18

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalProduct` | `POST /admin/checkBeforeDeleteMedicalProduct.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getMedicalProductVoList` | `POST /admin/getMedicalProductVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMedicalRecordList` | `POST /admin/getMedicalRecordList.json` |
| `getMedicalRecordListOfDoctor` | `POST /admin/getMedicalRecordListOfDoctor.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `getPackageProductVo` | `POST /admin/getPackageProductVo.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `getProductSkuExistCountVoList` | `POST /admin/getProductSkuExistCountVoList.json` |
| `getStockConf` | `POST /admin/getStockConf.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `saveMedicalProductList` | `POST /admin/saveMedicalProductList.json` |
| `selectPackageVoList` | `POST /admin/selectPackageVoList.json` |
| `selectStorehouseExistSkuCountVoList` | `POST /admin/selectStorehouseExistSkuCountVoList.json` |
| `selectStorehouseListOfCompany` | `POST /admin/selectStorehouseListOfCompany.json` |
| `viewSalesRecordFee` | `POST /admin/viewSalesRecordFee.json` |

**表单标签**

| 标签 |
|---|
| 可售库存大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品规格信息 |
| 3 | 规格 |
| 4 | 下单仓库 |
| 5 | 可售库存 可售库存 = 本仓剩余 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 6 | 下单数量 |
| 7 | 备注 |
| 8 | 操作 |
| 9 | 套餐名称 |
| 10 | 商品 |
| 11 | 折扣 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.useCount` |
| `item.remark` |
| `select.brandId` |
| `select.keyword` |
| `select.model1Keyword` |
| `select.model2Keyword` |
| `select.priceFromInclude` |
| `select.priceToInclude` |
| `select.unLockMoreThanZero` |
| `product.productSku` |
| `examine.keyword` |
| `packageQuery.keyword` |
| `packageQuery.model1Keyword` |
| `packageQuery.model2Keyword` |
| `productPlanArr[outerIndex]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `medicalRecordFactory.result.object.hospitalName` |
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
| `item.existCount` |
| `item.placeOrderStatus` |
| `item.deliveryStatus` |
| `province.id` |
| `province.brandName` |
| `methodGlassRecord.right15` |
| `methodGlassRecord.right14` |
| `methodGlassRecord.left15` |
| `methodGlassRecord.left14` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.allUnLockExistSkuCount` |
| `val.storehouse.name` |
| `val.unLockExistSkuCount` |
| `item.pkg.packageName` |
| `iten.product.productName` |
| `item.productPackageVoList` |
| `productRate` |
| `pkgProductVo.productExistCountVoList.length` |
| `selectedCount` |
| `item.productPackage.packageItemCount` |
| `item.productPackage.packageItemRate` |
| `item.product.id` |
| `iten.productSku.id` |
| `iten.productSku.model1` |
| `printModel` |
| `iten.productSku.model2` |
| `iten.productSku.marketPrice` |
| `iten.productSku.unitName` |
| `iten.productSku.skuCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `showModal()` |
| `deleteReceipt($index,item.id)` |
| `showAddModal()` |
| `addDelivery()` |
| `searchProductWord()` |
| `fullEye(` |
| `selectProductName($index)` |
| `showStockModel(item.productSku.id,$event)` |
| `$event.stopPropagation()` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `hideProductModal()` |
| `selectProductIdArr(item.pkg.id)` |
| `checkbillModal=false` |
| `selectProductPlanName(iten.stockInSkuExistCount,$event)` |
| `selectProductPlan()` |
| `addProductPlanModal=false` |

### 5.9 `adminSalesRecord.myMaterialBill`

- **URL**：`/myMaterialBill`
- **模板**：`views/myMember/myMaterialBill.html`
- **控制器**：`myMaterialBillCtrl`
- **端点数**：18

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkBeforeDeleteMedicalProduct` | `POST /admin/checkBeforeDeleteMedicalProduct.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getMedicalProductVoList` | `POST /admin/getMedicalProductVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMedicalRecordList` | `POST /admin/getMedicalRecordList.json` |
| `getMedicalRecordListOfDoctor` | `POST /admin/getMedicalRecordListOfDoctor.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `getPackageProductVo` | `POST /admin/getPackageProductVo.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `getProductSkuExistCountVoList` | `POST /admin/getProductSkuExistCountVoList.json` |
| `getStockConf` | `POST /admin/getStockConf.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `saveMedicalProductList` | `POST /admin/saveMedicalProductList.json` |
| `selectPackageVoList` | `POST /admin/selectPackageVoList.json` |
| `selectStorehouseExistSkuCountVoList` | `POST /admin/selectStorehouseExistSkuCountVoList.json` |
| `selectStorehouseListOfCompany` | `POST /admin/selectStorehouseListOfCompany.json` |
| `viewSalesRecordFee` | `POST /admin/viewSalesRecordFee.json` |

**表单标签**

| 标签 |
|---|
| 可售库存大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品规格信息 |
| 3 | 规格 |
| 4 | 下单仓库 |
| 5 | 可售库存 可售库存 = 本仓剩余 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 6 | 下单数量 |
| 7 | 备注 |
| 8 | 操作 |
| 9 | 套餐名称 |
| 10 | 商品 |
| 11 | 折扣 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.useCount` |
| `item.remark` |
| `select.brandId` |
| `select.keyword` |
| `select.model1Keyword` |
| `select.model2Keyword` |
| `select.priceFromInclude` |
| `select.priceToInclude` |
| `select.unLockMoreThanZero` |
| `product.productSku` |
| `examine.keyword` |
| `packageQuery.keyword` |
| `packageQuery.model1Keyword` |
| `packageQuery.model2Keyword` |
| `productPlanArr[outerIndex]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `medicalRecordFactory.result.object.hospitalName` |
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
| `item.existCount` |
| `item.placeOrderStatus` |
| `item.deliveryStatus` |
| `province.id` |
| `province.brandName` |
| `methodGlassRecord.right15` |
| `methodGlassRecord.right14` |
| `methodGlassRecord.left15` |
| `methodGlassRecord.left14` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.allUnLockExistSkuCount` |
| `val.storehouse.name` |
| `val.unLockExistSkuCount` |
| `item.pkg.packageName` |
| `iten.product.productName` |
| `item.productPackageVoList` |
| `productRate` |
| `pkgProductVo.productExistCountVoList.length` |
| `selectedCount` |
| `item.productPackage.packageItemCount` |
| `item.productPackage.packageItemRate` |
| `item.product.id` |
| `iten.productSku.id` |
| `iten.productSku.model1` |
| `printModel` |
| `iten.productSku.model2` |
| `iten.productSku.marketPrice` |
| `iten.productSku.unitName` |
| `iten.productSku.skuCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `showModal()` |
| `deleteReceipt($index,item.id)` |
| `showAddModal()` |
| `addDelivery()` |
| `searchProductWord()` |
| `fullEye(` |
| `selectProductName($index)` |
| `showStockModel(item.productSku.id,$event)` |
| `$event.stopPropagation()` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `hideProductModal()` |
| `selectProductIdArr(item.pkg.id)` |
| `checkbillModal=false` |
| `selectProductPlanName(iten.stockInSkuExistCount,$event)` |
| `selectProductPlan()` |
| `addProductPlanModal=false` |

### 5.10 `myMedicalHistory`

- **URL**：`/myMedicalHistory?patientId`
- **模板**：`views/myMember/myMedicalHistory.html`
- **控制器**：`myMedicalHistoryCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPatientObjectFactory.object.patientName` |
| `getPatientObjectFactory.object.patientGender` |
| `gender` |
| `getPatientObjectFactory.object.patientBirthday` |
| `howoldFilter` |
| `getPatientObjectFactory.object.height` |
| `getPatientObjectFactory.object.weight` |
| `item.customer.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `item.patient.patientBirthday` |
| `item.medicalRecord.medicalCode` |
| `item.medicalRecord.medicalRecordType` |
| `medicalRecordType` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `corpInfo.employeeTitle` |
| `item.medicalRecord.doctorName` |
| `customerInfoFactory.vo.customer.customerName` |
| `customerInfoFactory.vo.customer.linkMobile` |
| `item.patient.avatar` |
| `item.cashflowReceivedFromCashier` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `getMedicalRecord(item.medicalRecord.id)` |
| `back()` |
| `showPatient()` |

### 5.11 `myMedicalRecordList`

- **URL**：`/myMedicalRecordList?patientId&customerId`
- **模板**：`views/myMember/myMedicalRecordList.html`
- **控制器**：`myMedicalRecordListCtrl`
- **端点数**：0

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.firstVisitFrom` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `customerName` |
| `patientName` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.medicalRecord.medicalRecordType` |
| `medicalRecordType` |
| `item.medicalRecord.medicalCode` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `corpInfo.employeeTitle` |
| `item.medicalRecord.doctorName` |
| `item.cashflowReceivedFromCashier` |
| `item.medicalRecord.hospitalName` |
| `item.medicalRecord.chiefComplaint` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `showAddPatient()` |
| `open1()` |
| `open2()` |
| `refresh()` |
| `getMedicalRecord(item.medicalRecord.id,item.patient.id)` |
| `getMedicalRecord(item.medicalRecord.id)` |
| `hidePatient()` |

**跳转到**：`myMedicalRecordList`, `myMember`

### 5.12 `myMember`

- **URL**：`/myMember`
- **模板**：`views/myMember/myMember.html`
- **控制器**：`myMemberCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `beginCustomerCheckin` | `POST /admin/beginCustomerCheckin.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `receiveSelfAndBeginCustomerCheckin` | `POST /admin/receiveSelfAndBeginCustomerCheckin.json` |
| `selectCustomerCheckinVoListOfCompany` | `POST /admin/selectCustomerCheckinVoListOfCompany.json` |
| `selectCustomerCheckinVoListOfEmployee` | `POST /admin/selectCustomerCheckinVoListOfEmployee.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `rightTime` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `waitingList.count` |
| `item.customerCheckin.checkinNumber` |
| `paddingZero` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `memberFactory.total.totalCount` |
| `memberFactory.total.sendedCount` |
| `memberFactory.total.receivedCount` |
| `memberFactory.total.completeCount` |
| `item.customerCheckin.status` |
| `checkinTwoStatus` |
| `item.patient.avatar` |
| `item.patient.patientGender` |
| `gender` |
| `item.customer.customerName` |
| `item.customerCheckin.createName` |
| `item.customerCheckin.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customerCheckin.sendTime` |
| `fromNow` |
| `item.employee.employeeName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `queryWaitingList()` |
| `receiveSelfAndBeginCustomerCheckin(item.customerCheckin.id)` |
| `searchTab(null)` |
| `searchTab(1)` |
| `searchTab(2)` |
| `searchTab(3)` |
| `open1()` |
| `clinck(item.customerCheckin.id,item.patient.id)` |
| `getMedicalRecord(item.customerCheckin.medicalRecordId,item.patient.id)` |

**跳转到**：`myMedicalRecordList`

### 5.13 `adminMyRecord.myMemberRecord`

- **URL**：`/myMemberRecord`
- **模板**：`views/myMember/myMemberRecord.html`
- **控制器**：`myMemberRecordCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addRegistrationFee` | `POST /admin/addRegistrationFee.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getRegistrationFee` | `POST /admin/getRegistrationFee.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `insertMedicalRecordTemplate` | `POST /admin/insertMedicalRecordTemplate.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectMedicalRecordTemplateVoList` | `POST /admin/selectMedicalRecordTemplateVoList.json` |
| `updateMedicalRecord` | `POST /admin/updateMedicalRecord.json` |

**必填项**

| 标签 |
|---|
| 个人 共享 模板名称 创建日期 创建人员 类型 {{item.medicalRecordTemplate.templateName}} {{item.medicalRecordTemplate.gmtCreate \| date:'yyyy-MM-dd'}} {{item.createAdmin.nickname}} {{item.medicalRecordTemplate.shared \| shared}} 新增病历模板 * 模板名称 模板类型 个人使用 |

**表单标签**

| 标签 |
|---|
| {{firstDoctor.tip}}： |
| 共享使用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `visionRecordVoFactory.vo.visionRecord.medicalRecordId` |
| `visionRecordVoFactory.vo.medicalRecord.id` |
| `obj.firstVisit` |
| `visionRecordVoFactory.vo.medicalRecord.secondDoctorName` |
| `obj.complain` |
| `obj.presentHistory` |
| `obj.illnessHistory` |
| `obj.familyHistory` |
| `obj.operationHistory` |
| `obj.allergyHistory` |
| `obj.otherHistory` |
| `obj.diagnosis` |
| `obj.resolution` |
| `obj.method` |
| `obj.nextVisitTime` |
| `obj.nextChangeTime` |
| `obj.remark` |
| `template.keyword` |
| `template.shared` |
| `save.templateName` |
| `save.shared` |
| `save.complain` |
| `save.presentHistory` |
| `save.illnessHistory` |
| `save.familyHistory` |
| `save.operationHistory` |
| `save.allergyHistory` |
| `save.otherHistory` |
| `save.diagnosis` |
| `save.resolution` |
| `save.method` |
| `save.remark` |
| `customerCheckin.guahao` |
| `customerCheckin.registrationFeeId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `firstDoctor.tip` |
| `firstDoctor.name` |
| `courseType.courseTypeName` |
| `visionRecordVoFactory.vo.medicalRecord.medicalCode` |
| `corpInfo.companyTitle` |
| `visionRecordVoFactory.vo.medicalRecord.hospitalName` |
| `corpInfo.employeeTitle` |
| `visionRecordVoFactory.vo.medicalRecord.doctorName` |
| `optitem.employeeName` |
| `item.medicalRecordTemplate.templateName` |
| `item.medicalRecordTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.medicalRecordTemplate.shared` |
| `shared` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `visionRecordVoFactory.vo.patient.patientName` |
| `visionRecordVoFactory.vo.patient.patientGender` |
| `gender` |
| `visionRecordVoFactory.vo.patient.patientBirthday` |
| `howoldFilter` |
| `visionRecordVoFactory.vo.customer.customerName` |
| `visionRecordVoFactory.vo.customer.linkMobile` |
| `hidePhone` |
| `visionRecordVoFactory.vo.medicalRecord.complain` |
| `visionRecordVoFactory.vo.medicalRecord.presentHistory` |
| `visionRecordVoFactory.vo.medicalRecord.illnessHistory` |
| `visionRecordVoFactory.vo.medicalRecord.familyHistory` |
| `visionRecordVoFactory.vo.medicalRecord.operationHistory` |
| `visionRecordVoFactory.vo.medicalRecord.allergyHistory` |
| `visionRecordVoFactory.vo.medicalRecord.otherHistory` |
| `visionRecordVoFactory.vo.medicalRecord.diagnosis` |
| `visionRecordVoFactory.vo.medicalRecord.resolution` |
| `visionRecordVoFactory.vo.medicalRecord.method` |
| `visionRecordVoFactory.vo.medicalRecord.remark` |
| `visionRecordVoFactory.vo.medicalRecord.firstVisit` |
| `registFee.inputVal` |

**页面动作（ng-click）**

| 动作 |
|---|
| `firstDoctor.show = true` |
| `setCourseTypeId(courseType)` |
| `registerFee()` |
| `showModal()` |
| `open2()` |
| `chooseopt(optitem.id,optitem.employeeName)` |
| `toggleInfo()` |
| `toggleInfo2()` |
| `open1()` |
| `open3()` |
| `modify()` |
| `reloadPage()` |
| `showSaveModal()` |
| `selectTemplate(item.medicalRecordTemplate)` |
| `checkbillModal=false` |
| `saveModal=false` |
| `addTemplate()` |
| `create()` |
| `hideCheckModel()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in registArr
```

### 5.14 `adminSalesRecord.myMemberRecord`

- **URL**：`/myMemberRecord`
- **模板**：`views/myMember/myMemberRecord.html`
- **控制器**：`myMemberRecordCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addRegistrationFee` | `POST /admin/addRegistrationFee.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getRegistrationFee` | `POST /admin/getRegistrationFee.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `insertMedicalRecordTemplate` | `POST /admin/insertMedicalRecordTemplate.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectMedicalRecordTemplateVoList` | `POST /admin/selectMedicalRecordTemplateVoList.json` |
| `updateMedicalRecord` | `POST /admin/updateMedicalRecord.json` |

**必填项**

| 标签 |
|---|
| 个人 共享 模板名称 创建日期 创建人员 类型 {{item.medicalRecordTemplate.templateName}} {{item.medicalRecordTemplate.gmtCreate \| date:'yyyy-MM-dd'}} {{item.createAdmin.nickname}} {{item.medicalRecordTemplate.shared \| shared}} 新增病历模板 * 模板名称 模板类型 个人使用 |

**表单标签**

| 标签 |
|---|
| {{firstDoctor.tip}}： |
| 共享使用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `visionRecordVoFactory.vo.visionRecord.medicalRecordId` |
| `visionRecordVoFactory.vo.medicalRecord.id` |
| `obj.firstVisit` |
| `visionRecordVoFactory.vo.medicalRecord.secondDoctorName` |
| `obj.complain` |
| `obj.presentHistory` |
| `obj.illnessHistory` |
| `obj.familyHistory` |
| `obj.operationHistory` |
| `obj.allergyHistory` |
| `obj.otherHistory` |
| `obj.diagnosis` |
| `obj.resolution` |
| `obj.method` |
| `obj.nextVisitTime` |
| `obj.nextChangeTime` |
| `obj.remark` |
| `template.keyword` |
| `template.shared` |
| `save.templateName` |
| `save.shared` |
| `save.complain` |
| `save.presentHistory` |
| `save.illnessHistory` |
| `save.familyHistory` |
| `save.operationHistory` |
| `save.allergyHistory` |
| `save.otherHistory` |
| `save.diagnosis` |
| `save.resolution` |
| `save.method` |
| `save.remark` |
| `customerCheckin.guahao` |
| `customerCheckin.registrationFeeId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `firstDoctor.tip` |
| `firstDoctor.name` |
| `courseType.courseTypeName` |
| `visionRecordVoFactory.vo.medicalRecord.medicalCode` |
| `corpInfo.companyTitle` |
| `visionRecordVoFactory.vo.medicalRecord.hospitalName` |
| `corpInfo.employeeTitle` |
| `visionRecordVoFactory.vo.medicalRecord.doctorName` |
| `optitem.employeeName` |
| `item.medicalRecordTemplate.templateName` |
| `item.medicalRecordTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.medicalRecordTemplate.shared` |
| `shared` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `visionRecordVoFactory.vo.patient.patientName` |
| `visionRecordVoFactory.vo.patient.patientGender` |
| `gender` |
| `visionRecordVoFactory.vo.patient.patientBirthday` |
| `howoldFilter` |
| `visionRecordVoFactory.vo.customer.customerName` |
| `visionRecordVoFactory.vo.customer.linkMobile` |
| `hidePhone` |
| `visionRecordVoFactory.vo.medicalRecord.complain` |
| `visionRecordVoFactory.vo.medicalRecord.presentHistory` |
| `visionRecordVoFactory.vo.medicalRecord.illnessHistory` |
| `visionRecordVoFactory.vo.medicalRecord.familyHistory` |
| `visionRecordVoFactory.vo.medicalRecord.operationHistory` |
| `visionRecordVoFactory.vo.medicalRecord.allergyHistory` |
| `visionRecordVoFactory.vo.medicalRecord.otherHistory` |
| `visionRecordVoFactory.vo.medicalRecord.diagnosis` |
| `visionRecordVoFactory.vo.medicalRecord.resolution` |
| `visionRecordVoFactory.vo.medicalRecord.method` |
| `visionRecordVoFactory.vo.medicalRecord.remark` |
| `visionRecordVoFactory.vo.medicalRecord.firstVisit` |
| `registFee.inputVal` |

**页面动作（ng-click）**

| 动作 |
|---|
| `firstDoctor.show = true` |
| `setCourseTypeId(courseType)` |
| `registerFee()` |
| `showModal()` |
| `open2()` |
| `chooseopt(optitem.id,optitem.employeeName)` |
| `toggleInfo()` |
| `toggleInfo2()` |
| `open1()` |
| `open3()` |
| `modify()` |
| `reloadPage()` |
| `showSaveModal()` |
| `selectTemplate(item.medicalRecordTemplate)` |
| `checkbillModal=false` |
| `saveModal=false` |
| `addTemplate()` |
| `create()` |
| `hideCheckModel()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in registArr
```

### 5.15 `adminMyRecord.prescription`

- **URL**：`/prescription`
- **模板**：`views/myMember/prescription.html`
- **控制器**：`prescriptionCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `updateMethodGlassRecord` | `POST /admin/updateMethodGlassRecord.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `prescription.medicalCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `printChufang2.print()` |

### 5.16 `adminMyRecord.prescriptsRecord`

- **URL**：`/prescriptsRecord`
- **模板**：`views/myMember/prescriptsRecord.html`
- **控制器**：`prescriptsRecordCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getIntroducerList` | `POST /admin/getIntroducerList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getMethodGlassRecordVo` | `POST /admin/getMethodGlassRecordVo.json` |
| `getOkReviewRecordVo` | `POST /admin/getOkReviewRecordVo.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `saveOkReviewRecord` | `POST /admin/saveOkReviewRecord.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `updateMethodGlassRecord` | `POST /admin/updateMethodGlassRecord.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
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
| `mainOpticEye` |
| `methodGlassRecord.right83` |
| `methodGlassRecord.right85` |
| `methodGlassRecord.left83` |
| `methodGlassRecord.left85` |
| `methodGlassRecord.right84` |
| `methodGlassRecord.right86` |
| `methodGlassRecord.left84` |
| `methodGlassRecord.left86` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right1` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left1` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right91` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left91` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right82` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left82` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right81` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left81` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.right29` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left29` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.rxCount` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.lastRxTime` |
| `methodGlassRecordVoFactory.vo.methodGlassRecord.left67` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `RecordVoFactory.result.object.medicalCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `toggleInfo()` |
| `open2()` |
| `printChufang.print()` |

### 5.17 `timeCard`

- **URL**：`/timeCard`
- **模板**：`views/myMember/timeCard.html`
- **控制器**：`timeCardCtrl`
- **端点数**：16

**调用的端点**

| 动作 | 端点 |
|---|---|
| `consumeCustomerTrainerCardNumbers` | `POST /admin/consumeCustomerTrainerCardNumbers.json` |
| `deleteNews` | `POST /admin/deleteNews.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getCustomerTrainerCard` | `POST /admin/getCustomerTrainerCard.json` |
| `getNews` | `POST /admin/getNews.json` |
| `getNewsCategoryTree2Level` | `POST /admin/getNewsCategoryTree2Level.json` |
| `insertNews` | `POST /admin/insertNews.json` |
| `investMoneyForCustomerTrainerCard` | `POST /admin/investMoneyForCustomerTrainerCard.json` |
| `selectCustomerList` | `POST /admin/selectCustomerList.json` |
| `selectCustomerTrainerCardVoList` | `POST /admin/selectCustomerTrainerCardVoList.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectFirstCustomerTrainerCardLog` | `POST /admin/selectFirstCustomerTrainerCardLog.json` |
| `selectNewsList` | `POST /admin/selectNewsList.json` |
| `selectPosDeviceListOfCompany` | `POST /admin/selectPosDeviceListOfCompany.json` |
| `selectTrainerCardList` | `POST /admin/selectTrainerCardList.json` |
| `updateNews` | `POST /admin/updateNews.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 用户 |
| 2 | 次卡名称 |
| 3 | 售价 / 次数 / 剩余次数 |
| 4 | 状态 |
| 5 | 失效原因 |
| 6 | 有效期 |
| 7 | 备注 |
| 8 | 销售员 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.marketPrice` |
| `obj.numbers` |
| `obj.remark` |
| `returnCard.info.isAllMoney` |
| `returnCard.info.discountMoney` |
| `returnCard.info.returnCardReasons` |
| `returnCard.info.returnCardReason` |
| `returnCard.info.remarks` |
| `deductionTimeModal.info.returnNumbers` |
| `deductionTimeModal.info.remarks` |
| `object.keyword` |
| `returnCard.info.returnNumbers` |
| `returnCard.info.discountRate` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.customerTrainerCard.trainerCardName` |
| `item.customerTrainerCard.sourceMoney` |
| `item.customerTrainerCard.sourceNumber` |
| `item.customerTrainerCard.balanceNumber` |
| `item.customerTrainerCard.status` |
| `timeCardStatus` |
| `item.customerTrainerCard.invaildReason` |
| `cardInvalidReason` |
| `item.customerTrainerCard.validTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.customerTrainerCard.remark` |
| `item.sales.employeeName` |
| `obj.info.trainerCardName` |
| `obj.info.validMonths` |
| `validTime` |
| `obj.info.allowReturnCard` |
| `isAllow` |
| `item.payChannel` |
| `obj.payChannel` |
| `item.img_chose` |
| `item.img_notchose` |
| `item.name` |
| `obj.companyName` |
| `obj.marketPrice` |
| `returnCard.info.balanceNumber` |
| `returnCard.info.addMoney` |
| `updatePayChannel` |
| `returnType` |
| `returnCard.showBankInfo.bankName` |
| `returnCard.showBankInfo.payCardId` |
| `deductionTimeModal.info.balanceNumber` |

**页面动作（ng-click）**

| 动作 |
|---|
| `openCard()` |
| `deductionTime(item,$index)` |
| `lookRecord(item)` |
| `getCompanyName(item,$index)` |
| `updatepayChannel_click(item.payChannel,` |
| `chargeCard()` |
| `hideRechargeModal()` |
| `returnCard.affirm()` |
| `deductionTimeModal.affirm()` |

### 5.18 `updateMyMember`

- **URL**：`/updateMyMember?customerId`
- **模板**：`views/myMember/updateMyMember.html`
- **控制器**：`updateMemberCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disBandingWechatByCustomerId` | `POST /admin/disBandingWechatByCustomerId.json` |
| `getBandingWechatQrcode` | `POST /admin/getBandingWechatQrcode.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `isBandingWechat` | `POST /admin/isBandingWechat.json` |
| `saveCustomerInfo` | `POST /admin/saveCustomerInfo.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `updateCustomerTags` | `POST /admin/updateCustomerTags.json` |

**必填项**

| 标签 |
|---|
| * 会员姓名 |

**表单标签**

| 标签 |
|---|
| * 会员姓名 |
| 手机号 |
| 会员来源 |
| 微信绑定管理 |
| {{item.tagName}} + 增加标签 --> 会员标签 |
| 家庭住址 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `customerFactory.vo.customer.customerName` |
| `customerFactory.vo.customer.linkMobile` |
| `tagIdArray[$index]` |
| `tag.tagName` |
| `address.detail` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `common.channel` |
| `customerFactory.vo.wechatCustomer.nickName` |
| `item.id` |
| `item.tagName` |
| `imgSrc` |
| `corpInfo.employeeTitle` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showCommon()` |
| `connectWeixin()` |
| `cancelBind()` |
| `addLabel=true` |
| `saveCustomerInfo()` |
| `hidePatient()` |
