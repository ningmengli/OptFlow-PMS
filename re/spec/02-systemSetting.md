# 02｜模块 systemSetting 

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/systemSetting/` |
| 中文名 | 【待确认】 |
| 开发波次 | W9 |
| 页面数 | **80** |
| 端点数（去重） | **165** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `systemSetting.InspectList` | `/InspectList` | `views/systemSetting/InspectList.html` | `InspectListCtrl` | 0 |
| 2 | `systemSetting.addCheck` | `/addCheck` | `views/systemSetting/addCheck.html` | `addCheckCtrl` | 0 |
| 3 | `systemSetting.addCheckItem` | `/addCheckItem?id` | `views/systemSetting/addCheckItem.html` | `addCheckItemCtrl` | 5 |
| 4 | `systemSetting.addCustomerCharge` | `/addCustomerCharge` | `views/systemSetting/addCustomerCharge.html` | `addCustomerChargeCtrl` | 12 |
| 5 | `systemSetting.addCustomerChargeItem` | `/addCustomerChargeItem` | `views/systemSetting/addCustomerChargeItem.html` | `addCustomerChargeItemCtrl` | 0 |
| 6 | `systemSetting.addDepot` | `/addDepot` | `views/systemSetting/addDepot.html` | `addDepotCtrl` | 0 |
| 7 | `addFirstDoctor` | `/addFirstDoctor` | `views/systemSetting/addFirstDoctor.html` | `addFirstDoctorCtrl` | 0 |
| 8 | `systemSetting.addGroupedit` | `/addGroupedit` | `views/systemSetting/addGroupedit.html` | `addGroupeditCtrl` | 4 |
| 9 | `systemSetting.addInspect` | `/addInspect` | `views/systemSetting/addInspect.html` | `addInspectCtrl` | 0 |
| 10 | `systemSetting.addMaterial` | `/addMaterial` | `views/systemSetting/addMaterial.html` | `addMaterialCtrl` | 4 |
| 11 | `systemSetting.addMedicalFee` | `/addMedicalFee` | `views/systemSetting/addMedicalFee.html` | `addMedicalFeeCtrl` | 9 |
| 12 | `systemSetting.addMemberType` | `/addMemberType?id` | `views/systemSetting/addMemberType.html` | `addMemberTypeCtrl` | 0 |
| 13 | `systemSetting.addProcessCenter` | `/addProcessCenter` | `views/systemSetting/addProcessCenter.html` | `addProcessCenterCtrl` | 0 |
| 14 | `systemSetting.addProductPlan` | `/addProductPlan` | `views/systemSetting/addProductPlan.html` | `addProductPlanCtrl` | 0 |
| 15 | `systemSetting.addProjectCard` | `/addProjectCard?id` | `views/systemSetting/addProjectCard.html` | `addProjectCardCtrl` | 5 |
| 16 | `systemSetting.addRecordTemplate` | `/addRecordTemplate` | `views/systemSetting/addRecordTemplate.html` | `addRecordTemplateCtrl` | 0 |
| 17 | `systemSetting.addSupplier` | `/addSupplier` | `views/systemSetting/addSupplier.html` | `addSupplierCtrl` | 0 |
| 18 | `systemSetting.appConfig` | `/appConfig` | `views/systemSetting/appConfig.html` | `appConfigCtrl` | 1 |
| 19 | `systemSetting.appointAdmin` | `/appointAdmin` | `views/systemSetting/appointAdmin.html` | `appointAdminCtrl` | 2 |
| 20 | `systemSetting.batchMaterial` | `/batchMaterial` | `views/systemSetting/batchMaterial.html` | `batchMaterialCtrl` | 4 |
| 21 | `systemSetting.brandList` | `/brandList` | `views/systemSetting/brandList.html` | `brandListCtrl` | 0 |
| 22 | `systemSetting.chargeAdmin` | `/chargeAdmin` | `views/systemSetting/chargeAdmin.html` | `chargeAdminCtrl` | 7 |
| 23 | `systemSetting.chargeWays` | `/chargeWays` | `views/systemSetting/chargeWays.html` | `chargeWaysCtrl` | 6 |
| 24 | `systemSetting.checkList` | `/checkList` | `views/systemSetting/checkList.html` | `checkListCtrl` | 7 |
| 25 | `systemSetting.checkModify` | `/checkModify?id` | `views/systemSetting/checkModify.html` | `checkModifyCtrl` | 0 |
| 26 | `systemSetting.commonSetTemp` | `/commonSetTemp?type&id` | `views/systemSetting/commonSetTemp.html` | `commonSetTempCtrl` | 7 |
| 27 | `systemSetting.customerCharge` | `/customerCharge` | `views/systemSetting/customerCharge.html` | `customerChargeCtrl` | 0 |
| 28 | `systemSetting.customerChargeChoice` | `/customerChargeChoice?id` | `views/systemSetting/customerChargeChoice.html` | `customerChargeChoiceCtrl` | 11 |
| 29 | `systemSetting.customerChargeItem` | `/customerChargeItem` | `views/systemSetting/customerChargeItem.html` | `customerChargeItemCtrl` | 0 |
| 30 | `systemSetting.customerMaterialCertificate` | `/customerMaterialCertificate?productId&productSkuId` | `views/systemSetting/customerMaterialCertificate.html` | `materialCertificateCtrl` | 0 |
| 31 | `systemSetting.depotList` | `/depotList` | `views/systemSetting/depotList.html` | `depotListCtrl` | 0 |
| 32 | `systemSetting.depotModify` | `/depotModify?id` | `views/systemSetting/depotModify.html` | `depotModifyCtrl` | 0 |
| 33 | `systemSetting.firstApproval` | `/firstApproval?productId&productSkuId&supplierId&type` | `views/systemSetting/firstApproval.html` | `firstApprovalCtrl` | 1 |
| 34 | `firstDoctorList` | `/firstDoctorList` | `views/systemSetting/firstDoctorList.html` | `firstDoctorListCtrl` | 0 |
| 35 | `systemSetting.frontAdmin` | `/frontAdmin` | `views/systemSetting/frontAdmin.html` | `frontAdminCtrl` | 1 |
| 36 | `systemSetting.groupeditList` | `/groupeditList` | `views/systemSetting/groupeditList.html` | `groupeditListCtrl` | 9 |
| 37 | `logList` | `/logList?deviceId` | `views/systemSetting/logList.html` | `logListCtrl` | 0 |
| 38 | `systemSetting.materialCertificate` | `/materialCertificate?productId&productSkuId` | `views/systemSetting/materialCertificate.html` | `materialCertificateCtrl` | 0 |
| 39 | `systemSetting.materialImport` | `/materialImport` | `views/systemSetting/materialImport.html` | `materialImportCtrl` | 3 |
| 40 | `materialImport` | `/materialImport` | `views/systemSetting/materialImport.html` | `materialImportCtrl` | 3 |
| 41 | `systemSetting.materialModify` | `/materialModify?productId&productSkuId` | `views/systemSetting/materialModify.html` | `materialModifyCtrl` | 21 |
| 42 | `systemSetting.materiallist` | `/materiallist` | `views/systemSetting/materiallist.html` | `materiallistCtrl` | 7 |
| 43 | `systemSetting.medicalFeesList` | `/medicalFeesList` | `views/systemSetting/medicalFeesList.html` | `medicalFeesListCtrl` | 0 |
| 44 | `systemSetting.memberChannelList` | `/memberChannelList` | `views/systemSetting/memberChannelList.html` | `memberChannelListCtrl` | 0 |
| 45 | `systemSetting.memberCharge` | `/memberCharge` | `views/systemSetting/memberCharge.html` | `memberChargeCtrl` | 0 |
| 46 | `systemSetting.memberTypeList` | `/memberTypeList` | `views/systemSetting/memberTypeList.html` | `memberTypeListCtrl` | 0 |
| 47 | `systemSetting.memberTypeModify` | `/memberTypeModify?id` | `views/systemSetting/memberTypeModify.html` | `memberTypeModifyCtrl` | 0 |
| 48 | `systemSetting.messageAdmin` | `/messageAdmin` | `views/systemSetting/messageAdmin.html` | `messageAdminCtrl` | 6 |
| 49 | `systemSetting.modifyCustomerCharge` | `/modifyCustomerCharge?productId&productSkuId` | `views/systemSetting/modifyCustomerCharge.html` | `modifyCustomerChargeCtrl` | 11 |
| 50 | `systemSetting.modifyCustomerChargeItem` | `/modifyCustomerChargeItem?id` | `views/systemSetting/modifyCustomerChargeItem.html` | `modifyCustomerChargeItemCtrl` | 0 |
| 51 | `modifyFirstDoctor` | `/modifyFirstDoctor?id` | `views/systemSetting/modifyFirstDoctor.html` | `modifyFirstDoctorCtrl` | 0 |
| 52 | `systemSetting.modifyGroupedit` | `/modifyGroupedit?id` | `views/systemSetting/modifyGroupedit.html` | `modifyGroupeditCtrl` | 15 |
| 53 | `systemSetting.modifyInspect` | `/modifyInspect?id` | `views/systemSetting/modifyInspect.html` | `modifyInspectCtrl` | 0 |
| 54 | `systemSetting.modifyMedicalFee` | `/modifyMedicalFee?id` | `views/systemSetting/modifyMedicalFee.html` | `modifyMedicalFeeCtrl` | 0 |
| 55 | `systemSetting.modifyProcessCenter` | `/modifyProcessCenter?id` | `views/systemSetting/modifyProcessCenter.html` | `modifyProcessCenterCtrl` | 0 |
| 56 | `systemSetting.modifyProductPlan` | `/modifyProductPlan?productId` | `views/systemSetting/modifyProductPlan.html` | `modifyProductPlanCtrl` | 0 |
| 57 | `systemSetting.modifyRecordTemplate` | `/modifyRecordTemplate?id` | `views/systemSetting/modifyRecordTemplate.html` | `modifyRecordTemplateCtrl` | 2 |
| 58 | `systemSetting.openPlate` | `/openPlate` | `views/systemSetting/openPlate.html` | `openPlateCtrl` | 2 |
| 59 | `systemSetting.phoneAdmin` | `/phoneAdmin` | `views/systemSetting/phoneAdmin.html` | `phoneAdminCtrl` | 6 |
| 60 | `systemSetting.pointsAdmin` | `/pointsAdmin` | `views/systemSetting/pointsAdmin.html` | `pointsAdminCtrl` | 2 |
| 61 | `systemSetting.printConfig` | `/printConfig` | `views/systemSetting/printConfig.html` | `printConfigCtrl` | 7 |
| 62 | `systemSetting.processCenter` | `/processCenter` | `views/systemSetting/processCenter.html` | `processCenterCtrl` | 0 |
| 63 | `systemSetting.productPlanList` | `/productPlanList` | `views/systemSetting/productPlanList.html` | `productPlanListCtrl` | 0 |
| 64 | `systemSetting.projectCard` | `/projectCard` | `views/systemSetting/projectCard.html` | `projectCardCtrl` | 3 |
| 65 | `systemSetting.recipeAdmin` | `/recipeAdmin` | `views/systemSetting/recipeAdmin.html` | `recipeAdminCtrl` | 9 |
| 66 | `systemSetting.recordTemplateList` | `/recordTemplateList` | `views/systemSetting/recordTemplateList.html` | `recordTemplateListCtrl` | 3 |
| 67 | `systemSetting.reportDateAdmin` | `/reportDateAdmin` | `views/systemSetting/reportDateAdmin.html` | `reportDateAdminCtrl` | 2 |
| 68 | `sataServerList` | `/sataServerList` | `views/systemSetting/sataServerList.html` | `sataServerListCtrl` | 2 |
| 69 | `systemSetting.schoolCheckRecord` | `/schoolCheckRecord` | `views/systemSetting/schoolCheckRecord.html` | `schoolCheckRecordCtrl` | 5 |
| 70 | `systemSetting.stockAdmin` | `/stockAdmin` | `views/systemSetting/stockAdmin.html` | `stockAdminCtrl` | 2 |
| 71 | `systemSetting.suiFangJieLunTem` | `/suiFangJieLunTem?id` | `views/systemSetting/suiFangJieLunTem.html` | `suiFangJieLunTemCtrl` | 3 |
| 72 | `systemSetting.suiFangJieLunTemplate` | `/suiFangJieLunTemplate` | `views/systemSetting/suiFangJieLunTemplate.html` | `suiFangJieLunTemplateCtrl` | 3 |
| 73 | `systemSetting.suiFangNeiRongTemplate` | `/suiFangNeiRongTemplate` | `views/systemSetting/suiFangNeiRongTemplate.html` | `suiFangNeiRongTemplateCtrl` | 10 |
| 74 | `systemSetting.supplierCertificate` | `/supplierCertificate?supplierId` | `views/systemSetting/supplierCertificate.html` | `supplierCertificateCtrl` | 0 |
| 75 | `systemSetting.supplierList` | `/supplierList` | `views/systemSetting/supplierList.html` | `supplierListCtrl` | 0 |
| 76 | `systemSetting.supplierModify` | `/supplierModify?supplierId` | `views/systemSetting/supplierModify.html` | `supplierModifyCtrl` | 0 |
| 77 | `systemSetting` | `/systemSetting` | `views/systemSetting/systemSetting.html` | `systemSettingCtrl` | 0 |
| 78 | `systemSetting.toothCheckTemplate` | `/toothCheckTemplate` | `views/systemSetting/toothCheckTemplate.html` | `toothCheckTemplateCtrl` | 2 |
| 79 | `visionAdmin` | `/visionAdmin?chartType&isSocket` | `views/systemSetting/visionAdmin.html` | `visionAdminCtrl` | 4 |
| 80 | `systemSetting.wecomAdmin` | `/wecomAdmin` | `views/systemSetting/wecomAdmin.html` | `wecomAdminCtrl` | 5 |

## §2 端点清单（去重 165 个）

- `POST /admin/activeWecomAccountOfAdmin.json`
- `POST /admin/addCourseType.json`
- `POST /admin/addTrainerCard.json`
- `POST /admin/changeProductSkuSelectiveByProductId.json`
- `POST /admin/changeUartDeviceStatus.json`
- `POST /admin/copyExamine.json`
- `POST /admin/copyParamNameAndValue.json`
- `POST /admin/createExamine.json`
- `POST /admin/createMember.json`
- `POST /admin/createModelName.json`
- `POST /admin/createProductAndModelList.json`
- `POST /admin/createProductAndSkuList.json`
- `POST /admin/createProductAndSkuListOfGlass.json`
- `POST /admin/createProductBatchFileTask.json`
- `POST /admin/createProductModelBatchFileTask.json`
- `POST /admin/createSupplier.json`
- `POST /admin/deleteChannelTag.json`
- `POST /admin/deleteExamines.json`
- `POST /admin/deleteFollowUpContentTemplate.json`
- `POST /admin/deleteFollowUpResultTemplate.json`
- `POST /admin/deleteProductSkus.json`
- `POST /admin/deleteToothCheckTemplate.json`
- `POST /admin/disableMedicalRecordTemplate.json`
- `POST /admin/enableMedicalRecordTemplate.json`
- `POST /admin/getBrandListOfProduct.json`
- `POST /admin/getCategory.json`
- `POST /admin/getCategoryTree2Level.json`
- `POST /admin/getCategoryTree2LevelWithSkuCount.json`
- `POST /admin/getChannelTagTreeVoPage.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCorpAppointConf.json`
- `POST /admin/getCorpCashConf.json`
- `POST /admin/getCorpPayChannel.json`
- `POST /admin/getCorpPointRule.json`
- `POST /admin/getCorpReportConf.json`
- `POST /admin/getExamineItemVoList.json`
- `POST /admin/getExamineVo.json`
- `POST /admin/getExamineVoList.json`
- `POST /admin/getEyeChartConfRemark.json`
- `POST /admin/getEyeChartOfMine.json`
- `POST /admin/getFollowUpResultTemplateVo.json`
- `POST /admin/getHospitalInfo.json`
- `POST /admin/getIntroducer.json`
- `POST /admin/getIntroducerList.json`
- `POST /admin/getMachineCenterVo.json`
- `POST /admin/getMedicalCheckItemVo.json`
- `POST /admin/getMedicalRecordTemplateVo.json`
- `POST /admin/getMember.json`
- `POST /admin/getMemberList.json`
- `POST /admin/getModelNameVo.json`
- `POST /admin/getOpenApp.json`
- `POST /admin/getPackageVo.json`
- `POST /admin/getPayChannelOfCorpAccount.json`
- `POST /admin/getPinyin.json`
- `POST /admin/getProductSkuModelVo.json`
- `POST /admin/getProductSkuModelVoList.json`
- `POST /admin/getProductSkuVoList.json`
- `POST /admin/getProductVo.json`
- `POST /admin/getProductVoList.json`
- `POST /admin/getProductVoOnly.json`
- `POST /admin/getStorehouseVo.json`
- `POST /admin/getSuperAdminMobile.json`
- `POST /admin/getSupplier.json`
- `POST /admin/getSupplierVoList.json`
- `POST /admin/getTrainerCard.json`
- `POST /admin/getUartDevice.json`
- `POST /admin/insertChannelTag.json`
- `POST /admin/insertFollowUpResultTemplate.json`
- `POST /admin/insertIntroducer.json`
- `POST /admin/insertMachineCenterOfChainStore.json`
- `POST /admin/insertMedicalCheckItem.json`
- `POST /admin/insertMedicalRecordTemplate.json`
- `POST /admin/insertPackage.json`
- `POST /admin/insertStorehouse.json`
- `POST /admin/modifyOpenAppSecret.json`
- `POST /admin/randomProductCode.json`
- `POST /admin/refreshWecomActiveCodeListOfCorpId.json`
- `POST /admin/saveAdminCashById.json`
- `POST /admin/saveCardSubstractType.json`
- `POST /admin/saveCorpAppointConf.json`
- `POST /admin/saveCorpCashConf.json`
- `POST /admin/saveCorpMedicalConfByCorpId.json`
- `POST /admin/saveCorpPayChannel.json`
- `POST /admin/saveCorpPointRule.json`
- `POST /admin/saveCorpReportConf.json`
- `POST /admin/saveCorpSchoolCheckConf.json`
- `POST /admin/saveCorpWechatMedicalConf.json`
- `POST /admin/saveExamineItemList.json`
- `POST /admin/saveModelValueList.json`
- `POST /admin/saveProductQualifyList.json`
- `POST /admin/saveStockConf.json`
- `POST /admin/saveStockConfReleaseStock.json`
- `POST /admin/saveSupplierQualifyList.json`
- `POST /admin/selectAdminCashVoList.json`
- `POST /admin/selectAdminWecomVoList.json`
- `POST /admin/selectCompanyCashConfVoList.json`
- `POST /admin/selectCompanyPayChannelVoList.json`
- `POST /admin/selectCorpMedicalConfByCorpId.json`
- `POST /admin/selectCorpSchoolCheckConfByCorpId.json`
- `POST /admin/selectCorpSmsAddLogVoList.json`
- `POST /admin/selectCorpSmsByCorpId.json`
- `POST /admin/selectCorpSmsUseLogVoList.json`
- `POST /admin/selectCorpVoiceAddLogVoList.json`
- `POST /admin/selectCorpVoiceByCorpId.json`
- `POST /admin/selectCorpVoiceUseLogVoList.json`
- `POST /admin/selectCorpWechatMedicalConf.json`
- `POST /admin/selectCorpWechatMedicalConfByCorpId.json`
- `POST /admin/selectDataCorpSmsList.json`
- `POST /admin/selectDataCorpVoiceList.json`
- `POST /admin/selectFollowUpContentTemplateVoList.json`
- `POST /admin/selectFollowUpResultTemplateVoList.json`
- `POST /admin/selectMachineCenterVoList.json`
- `POST /admin/selectMedicalCheckItemVoList.json`
- `POST /admin/selectMedicalRecordTemplateVoList.json`
- `POST /admin/selectModelNameVoList.json`
- `POST /admin/selectModelValueList.json`
- `POST /admin/selectNotActiveWecomAdminList.json`
- `POST /admin/selectOrCreateWechatCard.json`
- `POST /admin/selectPackageVoList.json`
- `POST /admin/selectParamNameVoList.json`
- `POST /admin/selectParamValueList.json`
- `POST /admin/selectProductQualifyList.json`
- `POST /admin/selectProductSkuIndex.json`
- `POST /admin/selectProductSkuList.json`
- `POST /admin/selectStorehouseVoList.json`
- `POST /admin/selectSupplierQualifyList.json`
- `POST /admin/selectTaskItemList.json`
- `POST /admin/selectTaskList.json`
- `POST /admin/selectToothCheckTemplateVoList.json`
- `POST /admin/selectTrainerCardList.json`
- `POST /admin/selectUartDeviceList.json`
- `POST /admin/selectUartDeviceLogVoList.json`
- `POST /admin/transferActiveWecomAccountOfAdmin.json`
- `POST /admin/updateByExamineIdArraySelective.json`
- `POST /admin/updateByProductSkuIdArraySelective.json`
- `POST /admin/updateByTrainerCardIdArraySelective.json`
- `POST /admin/updateChannelTag.json`
- `POST /admin/updateCompanyCashConf.json`
- `POST /admin/updateCorpAppConf.json`
- `POST /admin/updateCorpLoginConf.json`
- `POST /admin/updateCorpSmsDisable.json`
- `POST /admin/updateCorpSmsWarningCount.json`
- `POST /admin/updateCorpVoiceDisable.json`
- `POST /admin/updateCorpVoiceWarningCount.json`
- `POST /admin/updateCourseType.json`
- `POST /admin/updateExamine.json`
- `POST /admin/updateEyeChartConfOfMine.json`
- `POST /admin/updateFollowUpResultTemplate.json`
- `POST /admin/updateIntroducer.json`
- `POST /admin/updateMachineCenterCompanyIdArray.json`
- `POST /admin/updateMachineCenterInfo.json`
- `POST /admin/updateMedicalCheckItem.json`
- `POST /admin/updateMedicalRecordTemplate.json`
- `POST /admin/updateMember.json`
- `POST /admin/updateModelName.json`
- `POST /admin/updatePackage.json`
- `POST /admin/updateProductAndModelList.json`
- `POST /admin/updateProductAndSkuList.json`
- `POST /admin/updateProductWarningQualifyExpiresDays.json`
- `POST /admin/updateStorehouse.json`
- `POST /admin/updateSupplier.json`
- `POST /admin/updateSupplierWarningQualifyExpiresDays.json`
- `POST /admin/updateTrainerCard.json`
- `POST /auth/isAdminTokenOk.json`
- `POST /auth/privateDownloadUrl.json`

## §3 逐页字段规格

### 2.1 `systemSetting.InspectList`

- **URL**：`/InspectList`
- **模板**：`views/systemSetting/InspectList.html`
- **控制器**：`InspectListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 项目名称 |
| 2 | 英文缩写 |
| 3 | 单位 |
| 4 | 数据类型 |
| 5 | 参考值 |
| 6 | 状态 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.medicalCheckItem.checkItemName` |
| `item.medicalCheckItem.checkItemEnglish` |
| `item.medicalCheckItem.checkItemUnitName` |
| `item.medicalCheckItem.checkItemValueSample` |
| `item.medicalCheckItem.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |

**跳转到**：`systemSetting.addInspect`

### 2.2 `systemSetting.addCheck`

- **URL**：`/addCheck`
- **模板**：`views/systemSetting/addCheck.html`
- **控制器**：`addCheckCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| 检查名称 * |
| 成本价 * |
| 零售价 * |
| 状态 * |
| 允许折扣 * |
| 允许积分 * |

**表单标签**

| 标签 |
|---|
| 检查名称 * |
| 英文名称 |
| 拼音码 |
| 单位 |
| 成本价 * |
| 零售价 * |
| 绩效 |
| 备注 |
| 科室地址 |
| 状态 * |
| 允许折扣 * |
| 允许积分 * |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.examineName` |
| `obj.englishName` |
| `obj.pinyin` |
| `obj.unitName` |
| `obj.costPrice` |
| `obj.marketPrice` |
| `obj.kpiPrice` |
| `obj.remark` |
| `obj.address` |
| `obj.status` |
| `obj.canBeDiscounted` |
| `obj.allowPoints` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addCheck()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
```

### 2.3 `systemSetting.addCheckItem`

- **URL**：`/addCheckItem?id`
- **模板**：`views/systemSetting/addCheckItem.html`
- **控制器**：`addCheckItemCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getExamineItemVoList` | `POST /admin/getExamineItemVoList.json` |
| `getExamineVo` | `POST /admin/getExamineVo.json` |
| `getMedicalCheckItemVo` | `POST /admin/getMedicalCheckItemVo.json` |
| `saveExamineItemList` | `POST /admin/saveExamineItemList.json` |
| `selectMedicalCheckItemVoList` | `POST /admin/selectMedicalCheckItemVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 顺序 |
| 2 | 项目名称 |
| 3 | 操作 |
| 4 | 顺序 |
| 5 | 项目名称 |
| 6 | 操作 |
| 7 | 项目名称 |
| 8 | 英文缩写 |
| 9 | 单位 |
| 10 | 参考值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.keyword` |
| `selectTab.checkItemIdArray` |
| `checkModel` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierObjectFactory.result.object.examineItemCount` |
| `getSupplierObjectFactory.result.object.examine.examineName` |
| `iten.leftName` |
| `iten.rightName` |
| `index` |
| `getSupplierObjectFactory.result.object.uartDeviceType.deviceTypeName` |
| `item.medicalCheckItem.id` |
| `item.medicalCheckItem.checkItemName` |
| `item.medicalCheckItem.checkItemEnglish` |
| `item.medicalCheckItem.checkItemUnitName` |
| `item.medicalCheckItem.checkItemValueSample` |

**页面动作（ng-click）**

| 动作 |
|---|
| `upMove(medicalExamineItemList,$index,medicalExamineItemList.length)` |
| `downMove(medicalExamineItemList,$index,medicalExamineItemList.length)` |
| `showCheckModal(1,$index,iten.left)` |
| `showCheckModal(2,$index,iten.right)` |
| `deleteItem($index,iten.position)` |
| `addItem()` |
| `showAddModal()` |
| `addCheck()` |
| `hideModal()` |
| `modifyCheck()` |
| `addCheckItem()` |

**跳转到**：`systemSetting.checkList`

### 2.4 `systemSetting.addCustomerCharge`

- **URL**：`/addCustomerCharge`
- **模板**：`views/systemSetting/addCustomerCharge.html`
- **控制器**：`addCustomerChargeCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createModelName` | `POST /admin/createModelName.json` |
| `createProductAndModelList` | `POST /admin/createProductAndModelList.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `getModelNameVo` | `POST /admin/getModelNameVo.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `insertIntroducer` | `POST /admin/insertIntroducer.json` |
| `insertStorehouse` | `POST /admin/insertStorehouse.json` |
| `randomProductCode` | `POST /admin/randomProductCode.json` |
| `selectModelNameVoList` | `POST /admin/selectModelNameVoList.json` |
| `selectModelValueList` | `POST /admin/selectModelValueList.json` |

**必填项**

| 标签 |
|---|
| * 产品名称 |
| * 产品编码 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 单位 |
| * 成本价 |
| * 零售价 |
| * 绩效 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |

**表单标签**

| 标签 |
|---|
| * 产品名称 |
| * 产品编码 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 单位 |
| * 成本价 |
| * 零售价 |
| * 绩效 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |
| 拼音 |
| 英文名称 |
| 默认供应商 |
| 生产厂家 |
| 生产许可证号 |
| 备注 |
| 图片 |
| {{categoryItem.categoryItem.itemName}} |
| 全选 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 参数名称 |
| 2 | 可选值 |
| 3 | 顺序 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.productCode` |
| `categoryName` |
| `obj.unitName` |
| `obj.costPrice` |
| `obj.marketPrice` |
| `obj.kpiPrice` |
| `obj.status` |
| `obj.canBeDiscounted` |
| `obj.allowPoints` |
| `obj.pinyin` |
| `obj.englishName` |
| `obj.factory` |
| `obj.factoryLicense` |
| `obj.remark` |
| `modelName.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `CommonRemark.category` |
| `unitName.id` |
| `unitName.name` |
| `sta.id` |
| `sta.name` |
| `obj.modelPicture` |
| `categoryItem.categoryItem.itemName` |
| `iten.name` |
| `item.root.categoryName` |
| `item.modelName.name` |
| `iten.value` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `chooseImg()` |
| `searchModelList()` |
| `showModalName(iten.id)` |
| `upMove(selectedName,$index,selectedName.length)` |
| `downMove(selectedName,$index,selectedName.length)` |
| `deleteItem($index)` |
| `modify()` |
| `selectCategory(item.childList,item.root.categoryName,item.root.id)` |
| `selectCategoryId(item.root.categoryName,item.root.id)` |
| `hideCategory()` |
| `selectAll($event)` |
| `updateSelection($event,item.modelName.id,item.modelName.name)` |
| `schoolModal=false` |
| `addName()` |
| `modelNameModal=false` |
| `firstApproval.confirm()` |

**跳转到**：`systemSetting.customerCharge`

### 2.5 `systemSetting.addCustomerChargeItem`

- **URL**：`/addCustomerChargeItem`
- **模板**：`views/systemSetting/addCustomerChargeItem.html`
- **控制器**：`addCustomerChargeItemCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| 参数名称 * |

**表单标签**

| 标签 |
|---|
| 参数名称 * |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addCheck()` |

### 2.6 `systemSetting.addDepot`

- **URL**：`/addDepot`
- **模板**：`views/systemSetting/addDepot.html`
- **控制器**：`addDepotCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 仓库名称： |
| * 仓库类型： |
| * 所属{{corpInfo. companyTitle}}： |

**表单标签**

| 标签 |
|---|
| * 仓库名称： |
| * 仓库类型： |
| 默认仓库 |
| 门店仓库 |
| 自建仓库 |
| * 所属{{corpInfo. companyTitle}}： |
| 仓库地址： |
| {{item.companyName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.name` |
| `obj.type` |
| `obj.address` |
| `keyword` |
| `obj.companyId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `getHospitalInfoFactory.result.object.companyName` |
| `item.id` |
| `item.companyName` |
| `item.address` |
| `item.linkman` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddModal()` |
| `delteCompany()` |
| `addDepot()` |
| `selectCompany()` |
| `addDepotModal=false` |

### 2.7 `addFirstDoctor`

- **URL**：`/addFirstDoctor`
- **模板**：`views/systemSetting/addFirstDoctor.html`
- **控制器**：`addFirstDoctorCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 推荐人名称 |
| * 来源 |

**表单标签**

| 标签 |
|---|
| * 推荐人名称 |
| 手机号 |
| * 来源 |
| 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.name` |
| `obj.mobile` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ft` |

**页面动作（ng-click）**

| 动作 |
|---|
| `obj.fromType=$index` |
| `addSupplier()` |

### 2.8 `systemSetting.addGroupedit`

- **URL**：`/addGroupedit`
- **模板**：`views/systemSetting/addGroupedit.html`
- **控制器**：`addGroupeditCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getExamineVo` | `POST /admin/getExamineVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `insertMedicalCheckItem` | `POST /admin/insertMedicalCheckItem.json` |
| `insertPackage` | `POST /admin/insertPackage.json` |

**必填项**

| 标签 |
|---|
| * 套餐名称 |
| * 检查列表 |
| * 套餐折扣（请输入 0 到 100之间的整数，如 50 表示 5 折） % * 套餐金额 元 * 状态 |

**表单标签**

| 标签 |
|---|
| * 套餐名称 |
| * 检查列表 |
| * 套餐折扣（请输入 0 到 100之间的整数，如 50 表示 5 折） % * 套餐金额 元 * 状态 |
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.packageName` |
| `iten` |
| `obj.status` |
| `isAll` |
| `obj.keyword` |
| `checkItemIdArray[$index+schoolListFactory.index-12]` |
| `obj.packageRate` |
| `obj.packageFee` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.examineName` |
| `iten.unitName` |
| `iten.marketPrice` |
| `iten.id` |
| `item.examine.id` |
| `item.examine.examineName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteItem($index)` |
| `showCheckModal()` |
| `add()` |
| `checkAll()` |
| `selectId(schoolListFactory.index)` |
| `schoolModal=false` |
| `modifyCheck()` |

**跳转到**：`systemSetting.groupeditList`

### 2.9 `systemSetting.addInspect`

- **URL**：`/addInspect`
- **模板**：`views/systemSetting/addInspect.html`
- **控制器**：`addInspectCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 项目名称 |

**表单标签**

| 标签 |
|---|
| * 项目名称 |
| 英文缩写 |
| 单位 |
| 定量 |
| 定性 |
| 可选项 |
| 单选 |
| 多选 |
| 特殊 |
| 临床意义 |
| 状态 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 可选项 单选 单选 多选 |
| 3 | 性别 |
| 4 | 年龄 |
| 5 | 参考值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.checkItemName` |
| `obj.checkItemEnglish` |
| `obj.checkItemUnitName` |
| `obj.checkItemType` |
| `choose` |
| `obj.singleValue` |
| `iten.rank1` |
| `iten.checkItemValue` |
| `obj.checkItemValueSample` |
| `obj.checkItemValueMin` |
| `obj.checkItemValueMax` |
| `except` |
| `iten.gender` |
| `iten.ageMin` |
| `iten.ageMax` |
| `iten.checkItemValueMin` |
| `iten.checkItemValueMax` |
| `obj.checkItemMeaning` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteValueItem($index)` |
| `addValueItem()` |
| `deleteItem($index)` |
| `addItem()` |
| `addInspect()` |

**跳转到**：`systemSetting.InspectList`

### 2.10 `systemSetting.addMaterial`

- **URL**：`/addMaterial`
- **模板**：`views/systemSetting/addMaterial.html`
- **控制器**：`addMaterialCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createProductAndSkuList` | `POST /admin/createProductAndSkuList.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `randomProductCode` | `POST /admin/randomProductCode.json` |

**必填项**

| 标签 |
|---|
| * 产品名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警数量 |

**表单标签**

| 标签 |
|---|
| * 产品名称 |
| 英文名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警数量 |
| 拼音 |
| 默认供应商 |
| 生产厂家 |
| 生产许可证号 |
| 备注 |
| {{categoryItem.categoryItem.itemName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.englishName` |
| `categoryName` |
| `obj.productCode` |
| `obj.warningExpiresDays` |
| `obj.warningQuantity` |
| `obj.highWarningQuantity` |
| `obj.pinyin` |
| `obj.factory` |
| `obj.factoryLicense` |
| `obj.remark` |
| `obj.modelType` |
| `data.model1Name` |
| `data.model2Name` |
| `item.model1` |
| `item.model2` |
| `item.unitName` |
| `optUnitName` |
| `item.costPrice` |
| `item.marketPrice` |
| `item.kpiPrice` |
| `item.warningQuantity` |
| `item.warningExpiresDays` |
| `item.status` |
| `item.canBeDiscounted` |
| `item.allowPoints` |
| `item.skuCode` |
| `tab.unitName` |
| `tab.costPrice` |
| `tab.marketPrice` |
| `tab.status` |
| `tab.canBeDiscounted` |
| `tab.allowPoints` |
| `tab.kpiPrice` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `CommonRemark.category` |
| `categoryItem.categoryItem.itemName` |
| `modelName.id` |
| `modelName.name` |
| `unitName.id` |
| `unitName.name` |
| `sta.id` |
| `sta.name` |
| `item.modelPicture` |
| `item.root.categoryName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `changeType(obj.modelType)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setTab(7)` |
| `setTab(4)` |
| `setTab(5)` |
| `setTab(6)` |
| `chooseImg($index)` |
| `deleteProduct($index)` |
| `addProductList()` |
| `modify()` |
| `selectCategory(item.childList,item.root.categoryName,item.root.id)` |
| `selectCategoryId(item.root.categoryName,item.root.id)` |
| `hideCategory()` |
| `setAllProduct()` |
| `setAllModal=false` |
| `firstApproval.confirm()` |

**跳转到**：`systemSetting.materiallist`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
x.id as x.name for x in unitNames
```

### 2.11 `systemSetting.addMedicalFee`

- **URL**：`/addMedicalFee`
- **模板**：`views/systemSetting/addMedicalFee.html`
- **控制器**：`addMedicalFeeCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createExamine` | `POST /admin/createExamine.json` |
| `createMember` | `POST /admin/createMember.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `getProductVo` | `POST /admin/getProductVo.json` |
| `getProductVoList` | `POST /admin/getProductVoList.json` |
| `insertMachineCenterOfChainStore` | `POST /admin/insertMachineCenterOfChainStore.json` |
| `insertPackage` | `POST /admin/insertPackage.json` |

**必填项**

| 标签 |
|---|
| 挂号费名称 * |
| 挂号费金额 * |
| 成本价 * |
| 状态 * |
| 允许折扣 * |

**表单标签**

| 标签 |
|---|
| 挂号费名称 * |
| 拼音码 |
| 挂号费金额 * |
| 成本价 * |
| 状态 * |
| 允许折扣 * |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.examineName` |
| `obj.pinyin` |
| `obj.marketPrice` |
| `obj.costPrice` |
| `obj.status` |
| `obj.canBeDiscounted` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addSupplier()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
```

### 2.12 `systemSetting.addMemberType`

- **URL**：`/addMemberType?id`
- **模板**：`views/systemSetting/addMemberType.html`
- **控制器**：`addMemberTypeCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 会员类型名称 |
| * 检查费用折扣 |
| * 产品费用折扣 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 会员类型名称 |
| * 检查费用折扣 |
| * 产品费用折扣 |
| * 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.memberName` |
| `obj.examineRate` |
| `obj.productRate` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addSupplier()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.13 `systemSetting.addProcessCenter`

- **URL**：`/addProcessCenter`
- **模板**：`views/systemSetting/addProcessCenter.html`
- **控制器**：`addProcessCenterCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 加工中心名称： |
| * 加工中心类型： |

**表单标签**

| 标签 |
|---|
| * 加工中心名称： |
| * 加工中心类型： |
| 连锁加工中心 |
| 全选 |
| {{item.companyName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.machineCenterName` |
| `company.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `iten.name` |
| `item.companyName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddModal()` |
| `delteCompany($index)` |
| `addDepot()` |
| `selectAll($event)` |
| `updateSelection($event,item.id,item.companyName)` |
| `addDepotModal=false` |
| `selectCompany()` |

### 2.14 `systemSetting.addProductPlan`

- **URL**：`/addProductPlan`
- **模板**：`views/systemSetting/addProductPlan.html`
- **控制器**：`addProductPlanCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 套餐名称 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 套餐名称 |
| * 状态 |
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.packageName` |
| `iten` |
| `iten.packageItemCount` |
| `iten.packageItemRate` |
| `obj.status` |
| `isAll` |
| `keyword` |
| `checkItemIdArray[$index+schoolListFactory.index-12]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.examineName` |
| `iten.id` |
| `item.product.id` |
| `item.product.productName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteItem($index)` |
| `showCheckModal()` |
| `add()` |
| `checkAll()` |
| `selectId(schoolListFactory.index)` |
| `schoolModal=false` |
| `modifyCheck()` |

**跳转到**：`systemSetting.groupeditList`

### 2.15 `systemSetting.addProjectCard`

- **URL**：`/addProjectCard?id`
- **模板**：`views/systemSetting/addProjectCard.html`
- **控制器**：`addProjectCardCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addTrainerCard` | `POST /admin/addTrainerCard.json` |
| `createSupplier` | `POST /admin/createSupplier.json` |
| `getTrainerCard` | `POST /admin/getTrainerCard.json` |
| `insertMedicalRecordTemplate` | `POST /admin/insertMedicalRecordTemplate.json` |
| `updateTrainerCard` | `POST /admin/updateTrainerCard.json` |

**必填项**

| 标签 |
|---|
| 次卡名称 * |
| 售价(元) * |
| 次数 * |
| 允许改价 * |
| 是 否 --> 允许改次 * |
| 是 否 --> 允许退卡 * |
| 是 否 --> 状态 * |

**表单标签**

| 标签 |
|---|
| 次卡名称 * |
| 英文名称 |
| 售价(元) * |
| 次数 * |
| 有效期(月) |
| 到期提醒(天) |
| 允许改价 * |
| 是 否 --> 允许改次 * |
| 是 否 --> 允许退卡 * |
| 是 否 --> 状态 * |
| 正常 停用 --> 备注 |
| 图文描述 |
| 封面图 |
| 详情图 |
| 单次时长(分钟) |
| 次卡简介 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.trainerCardName` |
| `obj.englishName` |
| `obj.marketPrice` |
| `obj.numbers` |
| `obj.validMonths` |
| `obj.remindDays` |
| `obj.allowChangePrice` |
| `obj.allowChangeNumber` |
| `obj.allowReturnCard` |
| `obj.status` |
| `obj.remark` |
| `obj.unitTrainerMinute` |
| `obj.trainerDescription` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.disableValidMonths` |
| `obj.imageCard` |
| `obj.imageDescription` |

**页面动作（ng-click）**

| 动作 |
|---|
| `changeStatus(` |
| `description_popout=true` |
| `projectCard()` |
| `chooseCoverImg(` |
| `cancelPopout()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in allowList
x.id as x.name for x in status
```

### 2.16 `systemSetting.addRecordTemplate`

- **URL**：`/addRecordTemplate`
- **模板**：`views/systemSetting/addRecordTemplate.html`
- **控制器**：`addRecordTemplateCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |

**表单标签**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |
| 个人使用 |
| 共享使用 |
| 主诉 |
| 现病史 |
| 疾病史 |
| 家族史 |
| 手术史 |
| 过敏史 |
| 其他史 |
| 诊断 |
| 处理意见 |
| 治疗方案 |
| 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.templateName` |
| `obj.shared` |
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
| `obj.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `add()` |

**跳转到**：`systemSetting.recordTemplateList`

### 2.17 `systemSetting.addSupplier`

- **URL**：`/addSupplier`
- **模板**：`views/systemSetting/addSupplier.html`
- **控制器**：`addSupplierCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 供应商 |

**表单标签**

| 标签 |
|---|
| * 供应商 |
| 地址 |
| 电话 |
| 联系人 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.supplierName` |
| `obj.address` |
| `obj.phone` |
| `obj.linkman` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addSupplier()` |
| `firstApproval.confirm()` |

### 2.18 `systemSetting.appConfig`

- **URL**：`/appConfig`
- **模板**：`views/systemSetting/appConfig.html`
- **控制器**：`appConfigCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `updateCorpAppConf` | `POST /admin/updateCorpAppConf.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `appC.name` |
| `ac.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setAppConfig(ac)` |

### 2.19 `systemSetting.appointAdmin`

- **URL**：`/appointAdmin`
- **模板**：`views/systemSetting/appointAdmin.html`
- **控制器**：`appointAdminCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpAppointConf` | `POST /admin/getCorpAppointConf.json` |
| `saveCorpAppointConf` | `POST /admin/saveCorpAppointConf.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.appointBeforeDays` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(0)` |
| `setTab(1)` |
| `setStatus(` |
| `modify()` |

### 2.20 `systemSetting.batchMaterial`

- **URL**：`/batchMaterial`
- **模板**：`views/systemSetting/batchMaterial.html`
- **控制器**：`batchMaterialCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createProductAndSkuListOfGlass` | `POST /admin/createProductAndSkuListOfGlass.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `randomProductCode` | `POST /admin/randomProductCode.json` |

**必填项**

| 标签 |
|---|
| * 产品名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警 |
| 状态 * |
| * 单位 |
| * 成本价 |
| * 零售价 |
| * 允许折扣 |
| * 允许积分 |
| * 规格 |
| * 球镜 |
| * 柱镜 |

**表单标签**

| 标签 |
|---|
| * 产品名称 |
| 英文名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警 |
| 状态 * |
| * 单位 |
| * 成本价 |
| * 零售价 |
| 绩效 |
| * 允许折扣 |
| * 允许积分 |
| 拼音 |
| 默认供应商 |
| 生产厂家 |
| 生产许可证号 |
| 备注 |
| {{categoryItem.categoryItem.itemName}} |
| * 规格 |
| * 球镜 |
| * 柱镜 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `params.productName` |
| `params.englishName` |
| `categoryName` |
| `params.productCode` |
| `params.warningExpiresDays` |
| `params.warningQuantity` |
| `params.highWarningQuantity` |
| `params.status` |
| `params.unitName` |
| `params.costPrice` |
| `params.marketPrice` |
| `params.kpiPrice` |
| `params.canBeDiscounted` |
| `params.allowPoints` |
| `params.pinyin` |
| `params.factory` |
| `params.factoryLicense` |
| `params.remark` |
| `params.model1ValueStart` |
| `params.model1ValueEnd` |
| `params.model1ValueStep` |
| `params.model2ValueStart` |
| `params.model2ValueEnd` |
| `params.model2ValueStep` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `CommonRemark.category` |
| `categoryItem.categoryItem.itemName` |
| `item.name` |
| `unitName` |
| `spacing.key` |
| `spacing.value` |
| `item.root.categoryName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `updateStatus(` |
| `modify()` |
| `selectCategory(item.childList,item.root.categoryName,item.root.id)` |
| `selectCategoryId(item.root.categoryName,item.root.id)` |
| `setCategory(false)` |
| `firstApproval.confirm()` |

**跳转到**：`systemSetting.materiallist`

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
x.id as x.name for x in unitNames
```

### 2.21 `systemSetting.brandList`

- **URL**：`/brandList`
- **模板**：`views/systemSetting/brandList.html`
- **控制器**：`brandListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌名称 |
| 2 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `pageSize` |
| `brand.brandName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.brandName` |
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showModal()` |
| `showModal(` |
| `modifyName(item.brandName,item.id)` |
| `hideModal()` |
| `exect(brand.brandName)` |
| `addBrand()` |
| `modifyBrand()` |

### 2.22 `systemSetting.chargeAdmin`

- **URL**：`/chargeAdmin`
- **模板**：`views/systemSetting/chargeAdmin.html`
- **控制器**：`chargeAdminCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpCashConf` | `POST /admin/getCorpCashConf.json` |
| `getSuperAdminMobile` | `POST /admin/getSuperAdminMobile.json` |
| `saveAdminCashById` | `POST /admin/saveAdminCashById.json` |
| `saveCorpCashConf` | `POST /admin/saveCorpCashConf.json` |
| `selectAdminCashVoList` | `POST /admin/selectAdminCashVoList.json` |
| `selectCompanyCashConfVoList` | `POST /admin/selectCompanyCashConfVoList.json` |
| `updateCompanyCashConf` | `POST /admin/updateCompanyCashConf.json` |

**表单标签**

| 标签 |
|---|
| 收银员可以改折扣 |
| 收银员不能改折扣 |
| 收银员可以减免费用 |
| 收银员不能减免费用 |
| 收银员可以使用优惠券打折 |
| 收银员不能使用优惠券打折 |
| 【推荐】通过短信验证码退款(接收人：{{phone}}) |
| 无需验证，直接退款 |
| 微信公众号推送收费明细 |
| 微信公众号不推送收费明细 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | --> 所属门店 |
| 2 | 抬头 |
| 3 | logo |
| 4 | 手机号显示 |
| 5 | 操作 |
| 6 | 登录账号 |
| 7 | 姓名 |
| 8 | 所属门店 |
| 9 | 角色 |
| 10 | 最低折扣权限 |
| 11 | 退款权限 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.cashierChangeRateDisable` |
| `obj.cashierSubstractDisable` |
| `obj.cashierCouponDisable` |
| `obj.refundSmsConfirm` |
| `msgObj.keyword` |
| `obj.wechatTemplateMessageDisable` |
| `item.adminCash.discount` |
| `item.adminCash.refundDisable` |
| `companyCashConfVo.keyword` |
| `editCompanyCashConf.params.cashHeader` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `phone` |
| `item.company.companyName` |
| `item.companyCashConf.cashHeader` |
| `item.companyCashConf.cashLogo` |
| `item.companyCashConf.customerMobileDisable` |
| `tab` |
| `item.adminVo.admin.username` |
| `item.adminVo.admin.nickname` |
| `item.adminVo.company.companyName` |
| `item.adminVo.adminRole.roleName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updatetab(0)` |
| `updatetab(1)` |
| `updatetab(2)` |
| `updatetab(3)` |
| `modify()` |
| `editCompanyCashConf.openEdit(item.companyCashConf)` |
| `changeStatusStop($event)` |
| `editCompanyCashConf.setStatus()` |
| `editCompanyCashConf.closeEdit()` |
| `editCompanyCashConf.affirm()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.23 `systemSetting.chargeWays`

- **URL**：`/chargeWays`
- **模板**：`views/systemSetting/chargeWays.html`
- **控制器**：`chargeWaysCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteChannelTag` | `POST /admin/deleteChannelTag.json` |
| `getCorpPayChannel` | `POST /admin/getCorpPayChannel.json` |
| `getPayChannelOfCorpAccount` | `POST /admin/getPayChannelOfCorpAccount.json` |
| `saveCorpPayChannel` | `POST /admin/saveCorpPayChannel.json` |
| `selectCompanyPayChannelVoList` | `POST /admin/selectCompanyPayChannelVoList.json` |
| `updateChannelTag` | `POST /admin/updateChannelTag.json` |

**表单标签**

| 标签 |
|---|
| 正常 |
| 停用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 门店名称 |
| 2 | 微信支付 |
| 3 | 支付宝支付 |
| 4 | 汇付POS机商户号 |
| 5 | 序号 |
| 6 | 支付方式 |
| 7 | 状态 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `add.name` |
| `add.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `payAccount.specialWechatMerchantId` |
| `payAccount.alipayAppAuthToken` |
| `payAccount.huifuId` |
| `item.company.companyName` |
| `item.companyPayChannel.specialWechatMerchantId` |
| `item.companyPayChannel.alipayAppAuthToken` |
| `item.companyPayChannel.huifuId` |
| `index` |
| `item.name` |
| `item.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updatetab(0)` |
| `updatetab(1)` |
| `showModal(item.name,item.status,$index)` |
| `confirmUse(1,$index)` |
| `confirmUse(2,$index)` |
| `addSupplier()` |
| `hideModal()` |

### 2.24 `systemSetting.checkList`

- **URL**：`/checkList`
- **模板**：`views/systemSetting/checkList.html`
- **控制器**：`checkListCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `copyExamine` | `POST /admin/copyExamine.json` |
| `deleteExamines` | `POST /admin/deleteExamines.json` |
| `getExamineVo` | `POST /admin/getExamineVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `updateByExamineIdArraySelective` | `POST /admin/updateByExamineIdArraySelective.json` |
| `updateExamine` | `POST /admin/updateExamine.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 检查名称 |
| 2 | 单位 |
| 3 | 成本价 |
| 4 | 零售价 |
| 5 | 绩效 |
| 6 | 拼音码 |
| 7 | 备注 |
| 8 | 状态 |
| 9 | 允许折扣 |
| 10 | 允许积分 |
| 11 | 对接设备 |
| 12 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `object.status` |
| `object.canBeDiscounted` |
| `object.allowPoints` |
| `isAll` |
| `examineIdArray[$index+getSupplierListFactory.index-pageSize]` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.examine.id` |
| `item.examine.examineName` |
| `item.examine.unitName` |
| `item.examine.costPrice` |
| `item.examine.marketPrice` |
| `item.examine.kpiPrice` |
| `item.examine.pinyin` |
| `item.examine.remark` |
| `item.examine.status` |
| `supplierStatus` |
| `item.examine.canBeDiscounted` |
| `discountStatus` |
| `item.examine.allowPoints` |
| `item.uartDeviceType.deviceTypeName` |
| `item.examineItemCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchDiscount(null)` |
| `searchDiscount(1)` |
| `searchDiscount(0)` |
| `searchPoints(null)` |
| `searchPoints(1)` |
| `searchPoints(0)` |
| `tagModal=true` |
| `changeSeletedExam(1)` |
| `hideTagModal($event)` |
| `discountModal=true` |
| `changeSeletedExam(3)` |
| `pointModal=true` |
| `changeSeletedExam(2)` |
| `deleteBatch()` |
| `checkAll()` |
| `setLabelBtn()` |
| `anotherRequest(item.examine.id)` |

**跳转到**：`systemSetting.addCheck`

### 2.25 `systemSetting.checkModify`

- **URL**：`/checkModify?id`
- **模板**：`views/systemSetting/checkModify.html`
- **控制器**：`checkModifyCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 检查名称 |
| * 成本价 |
| * 零售价 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |

**表单标签**

| 标签 |
|---|
| * 检查名称 |
| 英文名称 |
| 拼音码 |
| 单位 |
| * 成本价 |
| * 零售价 |
| 绩效 |
| 备注 |
| 科室地址 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.examineName` |
| `obj.englishName` |
| `obj.pinyin` |
| `obj.unitName` |
| `obj.costPrice` |
| `obj.marketPrice` |
| `obj.kpiPrice` |
| `obj.remark` |
| `obj.address` |
| `obj.status` |
| `obj.canBeDiscounted` |
| `obj.allowPoints` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**跳转到**：`systemSetting.checkList`

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
```

### 2.26 `systemSetting.commonSetTemp`

- **URL**：`/commonSetTemp?type&id`
- **模板**：`views/systemSetting/commonSetTemp.html`
- **控制器**：`commonSetTempCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createProductModelBatchFileTask` | `POST /admin/createProductModelBatchFileTask.json` |
| `deleteProductSkus` | `POST /admin/deleteProductSkus.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategory` | `POST /admin/getCategory.json` |
| `getCategoryTree2LevelWithSkuCount` | `POST /admin/getCategoryTree2LevelWithSkuCount.json` |
| `getProductSkuModelVoList` | `POST /admin/getProductSkuModelVoList.json` |
| `updateByProductSkuIdArraySelective` | `POST /admin/updateByProductSkuIdArraySelective.json` |

**必填项**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |

**表单标签**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |
| 个人使用 |
| 共享使用 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.templateName` |
| `obj.shared` |
| `obj.templateContent` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `templateType.html.title` |
| `templateType.html.content` |

**页面动作（ng-click）**

| 动作 |
|---|
| `backUrl()` |
| `add()` |

### 2.27 `systemSetting.customerCharge`

- **URL**：`/customerCharge`
- **模板**：`views/systemSetting/customerCharge.html`
- **控制器**：`customerChargeCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 证件过期预警 |
| {{item.storehouse.name}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品基本信息 |
| 3 | 定制参数 |
| 4 | 状态 |
| 5 | 允许折扣 |
| 6 | 允许积分 |
| 7 | 首营审批 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.qualifyExpiresWarning` |
| `obj.keyword` |
| `obj.priceFromInclude` |
| `obj.priceToInclude` |
| `object.status` |
| `object.canBeDiscounted` |
| `object.allowPoints` |
| `isAll` |
| `productSkuIdArray[$index+getSupplierListFactory.index-pageSize]` |
| `pageSize` |
| `store.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `searchCategoryObjectFactory.object.productSkuCount` |
| `item.root.categoryName` |
| `item.productSkuCount` |
| `iten.root.categoryName` |
| `iten.productSkuCount` |
| `getSupplierListFactory.count` |
| `province.id` |
| `province.brandName` |
| `item.productSku.id` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `iten.modelName.name` |
| `item.productModelVoList` |
| `modelName.name` |
| `item.productSku.status` |
| `supplierStatus` |
| `item.productSku.canBeDiscounted` |
| `discountStatus` |
| `item.productSku.allowPoints` |
| `data.filepath` |
| `item.storehouse.id` |
| `item.storehouse.name` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `importModal=true` |
| `downloadModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `searchTab()` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchDiscount()` |
| `searchDiscount(1)` |
| `searchDiscount(0)` |
| `searchPoints()` |
| `searchPoints(1)` |
| `searchPoints(0)` |
| `tagModal=true` |
| `changeSeletedProduct(1)` |
| `hideTagModal($event)` |
| `discountModal=true` |
| `changeSeletedProduct(3)` |
| `pointModal=true` |
| `changeSeletedProduct(2)` |
| `deleteBatch()` |
| `checkAll()` |
| `setLabelBtn()` |
| `createTask()` |
| `getStoreListFactory.nextPage()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`systemSetting.addCustomerCharge`

### 2.28 `systemSetting.customerChargeChoice`

- **URL**：`/customerChargeChoice?id`
- **模板**：`views/systemSetting/customerChargeChoice.html`
- **控制器**：`customerChargeChoiceCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `copyParamNameAndValue` | `POST /admin/copyParamNameAndValue.json` |
| `getModelNameVo` | `POST /admin/getModelNameVo.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `saveModelValueList` | `POST /admin/saveModelValueList.json` |
| `selectModelNameVoList` | `POST /admin/selectModelNameVoList.json` |
| `selectModelValueList` | `POST /admin/selectModelValueList.json` |
| `selectParamNameVoList` | `POST /admin/selectParamNameVoList.json` |
| `selectParamValueList` | `POST /admin/selectParamValueList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updateModelName` | `POST /admin/updateModelName.json` |
| `updateStorehouse` | `POST /admin/updateStorehouse.json` |

**必填项**

| 标签 |
|---|
| * 参数名称 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 参数名称 |
| * 状态 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 可选值 |
| 2 | 顺序 |
| 3 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `objModel.name` |
| `objModel.status` |
| `modelValue` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.value` |

**页面动作（ng-click）**

| 动作 |
|---|
| `upMove(medicalExamineItemList,$index,medicalExamineItemList.length)` |
| `downMove(medicalExamineItemList,$index,medicalExamineItemList.length)` |
| `deleteItem($index)` |
| `showAddModal()` |
| `addCheck()` |
| `hideModal()` |
| `addCheckItem()` |

**跳转到**：`systemSetting.customerChargeItem`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.29 `systemSetting.customerChargeItem`

- **URL**：`/customerChargeItem`
- **模板**：`views/systemSetting/customerChargeItem.html`
- **控制器**：`customerChargeItemCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 参数名称 |
| 2 | 状态 |
| 3 | 可选值 |
| 4 | 操作 |
| 5 | 参数名称 |
| 6 | 参数值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `pageSize` |
| `paramKeyword` |
| `productSkuIdArray[$index+paramListFactory.index-paramPageSize]` |
| `selete.seletedName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getModelNameListFactory.count` |
| `item.modelName.name` |
| `item.modelName.status` |
| `supplierStatus` |
| `iten.value` |
| `item.paramName.id` |
| `item.paramName.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddModal()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `showModalName(item.modelName.id,1)` |
| `modelNameModal=false` |
| `setLabelBtn()` |
| `showImport(item.paramName.name,item.paramName.id)` |
| `showModalName(item.paramName.id,2)` |
| `checkbillModal=false` |
| `importParam()` |
| `seleteModal=false` |

**跳转到**：`systemSetting.addCustomerChargeItem`

### 2.30 `systemSetting.customerMaterialCertificate`

- **URL**：`/customerMaterialCertificate?productId&productSkuId`
- **模板**：`views/systemSetting/customerMaterialCertificate.html`
- **控制器**：`materialCertificateCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{item.qualifyTitle}}： |
| 有效期： |
| 长期有效 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `warningQualifyExpiresDays` |
| `item.qualifyCode` |
| `item.qualifyExpireDateLong` |
| `item.qualifyPermanent` |
| `title.qualifyTitle` |
| `title.other` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.qualifyTitle` |
| `index` |
| `item.qualifyFileName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteItem($index)` |
| `setPermanent(item.qualifyPermanent,$index,$event)` |
| `download(item.qualifyFile)` |
| `showModal()` |
| `modify()` |
| `selectQuanlify()` |
| `hideModal()` |

**跳转到**：`systemSetting.customerCharge`

### 2.31 `systemSetting.depotList`

- **URL**：`/depotList`
- **模板**：`views/systemSetting/depotList.html`
- **控制器**：`depotListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 仓库名称 |
| 2 | 所属{{corpInfo. companyTitle}} |
| 3 | 所属加工中心 |
| 4 | 类型 |
| 5 | 地址 |
| 6 | 状态 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `corpInfo.` |
| `companyTitle` |
| `item.storehouse.name` |
| `item.company.companyName` |
| `item.machineCenter.name` |
| `item.storehouse.type` |
| `filterDepotList` |
| `item.storehouse.useType` |
| `item.storehouse.address` |
| `item.storehouse.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goAdd()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `modifyRepot(item.storehouse.id)` |

### 2.32 `systemSetting.depotModify`

- **URL**：`/depotModify?id`
- **模板**：`views/systemSetting/depotModify.html`
- **控制器**：`depotModifyCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 仓库名称： {{obj.name}} * 仓库类型： {{obj.type \| depotCenterType}} ({{obj.type\| filterDepotList:obj.useType}}) * 所属门店： 门店名称 {{getSupplierObjectFactory.result.object.company.companyName}} 加工中心： |

**表单标签**

| 标签 |
|---|
| 仓库地址： 状态： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.name` |
| `obj.address` |
| `obj.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.name` |
| `obj.type` |
| `depotCenterType` |
| `filterDepotList` |
| `obj.useType` |
| `getSupplierObjectFactory.result.object.company.companyName` |
| `getSupplierObjectFactory.result.object.machineCenter.name` |
| `obj.status` |
| `adminStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modifyDepot()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.33 `systemSetting.firstApproval`

- **URL**：`/firstApproval?productId&productSkuId&supplierId&type`
- **模板**：`views/systemSetting/firstApproval.html`
- **控制器**：`firstApprovalCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getIntroducerList` | `POST /admin/getIntroducerList.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `title1` |

**页面动作（ng-click）**

| 动作 |
|---|
| `jump(` |
| `jump(0)` |
| `jump(1)` |
| `modify()` |

### 2.34 `firstDoctorList`

- **URL**：`/firstDoctorList`
- **模板**：`views/systemSetting/firstDoctorList.html`
- **控制器**：`firstDoctorListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 推荐人名称 |
| 2 | 手机号 |
| 3 | 备注 |
| 4 | 来源 |
| 5 | 状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `status` |
| `fromType` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.name` |
| `item.mobile` |
| `item.remark` |
| `item.fromType` |
| `filterFromType` |
| `item.status` |
| `supplierStatus` |

**跳转到**：`addFirstDoctor`, `recommendCustomer`

**下拉数据源（ng-options）**

```
x.id as x.name for x in fromTypeArr
x.id as x.name for x in statusArr
```

### 2.35 `systemSetting.frontAdmin`

- **URL**：`/frontAdmin`
- **模板**：`views/systemSetting/frontAdmin.html`
- **控制器**：`frontAdminCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `updateCorpLoginConf` | `POST /admin/updateCorpLoginConf.json` |

**表单标签**

| 标签 |
|---|
| 不需要电话登录 |
| 需要电话登录 |
| 短信验证 |
| 卡券验证 |
| 扫总部二维码 |
| 扫门店二维码 |
| 不打印叫号码 |
| 打印叫号码 |
| 不登记学校 |
| 登记学校 |
| 仅允许前台分诊给医生 |
| 允许医生自已主动分诊 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.loginNeedMobile` |
| `obj.useWechatCard` |
| `obj.useCompanyQrcode` |
| `obj.printQueue` |
| `obj.schoolEnable` |
| `obj.doctorTriageSelf` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updatetab(0)` |
| `updatetab(1)` |
| `updatetab(2)` |
| `modify()` |

### 2.36 `systemSetting.groupeditList`

- **URL**：`/groupeditList`
- **模板**：`views/systemSetting/groupeditList.html`
- **控制器**：`groupeditListCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getProductVoOnly` | `POST /admin/getProductVoOnly.json` |
| `getUartDevice` | `POST /admin/getUartDevice.json` |
| `saveProductQualifyList` | `POST /admin/saveProductQualifyList.json` |
| `selectMedicalCheckItemVoList` | `POST /admin/selectMedicalCheckItemVoList.json` |
| `selectPackageVoList` | `POST /admin/selectPackageVoList.json` |
| `selectProductQualifyList` | `POST /admin/selectProductQualifyList.json` |
| `selectUartDeviceLogVoList` | `POST /admin/selectUartDeviceLogVoList.json` |
| `updateProductWarningQualifyExpiresDays` | `POST /admin/updateProductWarningQualifyExpiresDays.json` |
| `privateDownloadUrl` | `POST /auth/privateDownloadUrl.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 套餐名称 |
| 2 | 收费项目 |
| 3 | 折扣 |
| 4 | 金额 |
| 5 | 状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.pkg.packageName` |
| `iten.examineName` |
| `item.pkg.packageRate` |
| `item.pkg.packageFee` |
| `item.pkg.status` |
| `supplierStatus` |
| `item.pkg.stopMessage` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |

**跳转到**：`systemSetting.addGroupedit`, `systemSetting.addInspect`

### 2.37 `logList`

- **URL**：`/logList?deviceId`
- **模板**：`views/systemSetting/logList.html`
- **控制器**：`logListCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 查看二进制 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 时间 |
| 2 | 用途 |
| 3 | 日志内容 |
| 4 | 状态 |
| 5 | 采集器 |
| 6 | 设备编号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `hex` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.uartDeviceLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.uartDevice.deviceType` |
| `deviceType` |
| `item.uartDeviceLog.content` |
| `item.contentHexAscii` |
| `item.uartDeviceLog.splitStatus` |
| `splitStatus` |
| `item.uartDeviceLog.formatConverter` |
| `item.uartDevice.deviceCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |

**跳转到**：`sataServerList`

### 2.38 `systemSetting.materialCertificate`

- **URL**：`/materialCertificate?productId&productSkuId`
- **模板**：`views/systemSetting/materialCertificate.html`
- **控制器**：`materialCertificateCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{item.qualifyTitle}}： |
| 有效期： |
| 长期有效 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `warningQualifyExpiresDays` |
| `item.qualifyCode` |
| `item.qualifyExpireDateLong` |
| `item.qualifyPermanent` |
| `title.qualifyTitle` |
| `title.other` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.qualifyTitle` |
| `index` |
| `item.qualifyFileName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteItem($index)` |
| `setPermanent(item.qualifyPermanent,$index,$event)` |
| `download(item.qualifyFile)` |
| `showModal()` |
| `modify()` |
| `selectQuanlify()` |
| `hideModal()` |

**跳转到**：`systemSetting.materiallist`

### 2.39 `systemSetting.materialImport`

- **URL**：`/materialImport`
- **模板**：`views/systemSetting/materialImport.html`
- **控制器**：`materialImportCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectTaskItemList` | `POST /admin/selectTaskItemList.json` |
| `selectTaskList` | `POST /admin/selectTaskList.json` |
| `privateDownloadUrl` | `POST /auth/privateDownloadUrl.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 任务名称 |
| 2 | 导入文件 |
| 3 | 创建时间 |
| 4 | 任务类型 |
| 5 | 任务模块 |
| 6 | 错误信息 |
| 7 | 状态 |
| 8 | 导入记录 |
| 9 | 状态 |
| 10 | 原始数据 |
| 11 | 错误信息 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `interval` |
| `obj.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.fileType` |
| `importType` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.msg` |
| `item.status` |
| `importStatus` |
| `item.errorStatus` |
| `errStatus` |
| `item.line` |
| `item.error` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `setInterval(interval)` |
| `download(item.filePath)` |
| `showModal(item.id,item.status)` |
| `hideModal()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.40 `materialImport`

- **URL**：`/materialImport`
- **模板**：`views/systemSetting/materialImport.html`
- **控制器**：`materialImportCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectTaskItemList` | `POST /admin/selectTaskItemList.json` |
| `selectTaskList` | `POST /admin/selectTaskList.json` |
| `privateDownloadUrl` | `POST /auth/privateDownloadUrl.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 任务名称 |
| 2 | 导入文件 |
| 3 | 创建时间 |
| 4 | 任务类型 |
| 5 | 任务模块 |
| 6 | 错误信息 |
| 7 | 状态 |
| 8 | 导入记录 |
| 9 | 状态 |
| 10 | 原始数据 |
| 11 | 错误信息 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `interval` |
| `obj.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.fileType` |
| `importType` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.msg` |
| `item.status` |
| `importStatus` |
| `item.errorStatus` |
| `errStatus` |
| `item.line` |
| `item.error` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `setInterval(interval)` |
| `download(item.filePath)` |
| `showModal(item.id,item.status)` |
| `hideModal()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.41 `systemSetting.materialModify`

- **URL**：`/materialModify?productId&productSkuId`
- **模板**：`views/systemSetting/materialModify.html`
- **控制器**：`materialModifyCtrl`
- **端点数**：21

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeProductSkuSelectiveByProductId` | `POST /admin/changeProductSkuSelectiveByProductId.json` |
| `deleteChannelTag` | `POST /admin/deleteChannelTag.json` |
| `deleteExamines` | `POST /admin/deleteExamines.json` |
| `enableMedicalRecordTemplate` | `POST /admin/enableMedicalRecordTemplate.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getChannelTagTreeVoPage` | `POST /admin/getChannelTagTreeVoPage.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getMember` | `POST /admin/getMember.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `getProductVoOnly` | `POST /admin/getProductVoOnly.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `insertChannelTag` | `POST /admin/insertChannelTag.json` |
| `saveCardSubstractType` | `POST /admin/saveCardSubstractType.json` |
| `selectOrCreateWechatCard` | `POST /admin/selectOrCreateWechatCard.json` |
| `selectProductSkuIndex` | `POST /admin/selectProductSkuIndex.json` |
| `selectProductSkuList` | `POST /admin/selectProductSkuList.json` |
| `updateByExamineIdArraySelective` | `POST /admin/updateByExamineIdArraySelective.json` |
| `updateChannelTag` | `POST /admin/updateChannelTag.json` |
| `updateMember` | `POST /admin/updateMember.json` |
| `updateProductAndSkuList` | `POST /admin/updateProductAndSkuList.json` |

**必填项**

| 标签 |
|---|
| * 产品名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 (product code) |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警 |

**表单标签**

| 标签 |
|---|
| * 产品名称 |
| 英文名称 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 产品编码 (product code) |
| * 近有效期预警天数 |
| * 库存不足预警数量 |
| * 库存上限预警 |
| 拼音 |
| 默认供应商 |
| 生产厂家 |
| 生产许可证号 |
| 备注 |
| {{categoryItem.categoryItem.itemName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.product.productName` |
| `obj.product.englishName` |
| `obj.category.categoryName` |
| `obj.product.productCode` |
| `obj.product.warningExpiresDays` |
| `obj.product.warningQuantity` |
| `obj.product.highWarningQuantity` |
| `obj.product.pinyin` |
| `obj.product.factory` |
| `obj.product.factoryLicense` |
| `obj.product.remark` |
| `item.model1` |
| `item.model2` |
| `item.unitName` |
| `item.costPrice` |
| `item.marketPrice` |
| `item.kpiPrice` |
| `item.warningQuantity` |
| `item.warningExpiresDays` |
| `item.status` |
| `item.canBeDiscounted` |
| `item.allowPoints` |
| `item.skuCode` |
| `tab.unitName` |
| `tab.costPrice` |
| `tab.marketPrice` |
| `tab.status` |
| `tab.canBeDiscounted` |
| `tab.allowPoints` |
| `tab.kpiPrice` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.brand.brandName` |
| `CommonRemark.category` |
| `categoryItem.categoryItem.itemName` |
| `obj.product.model1Name` |
| `obj.product.model2Name` |
| `item.id` |
| `index` |
| `pageNum` |
| `pagesize` |
| `item.customeIndex` |
| `getProductVoObjectFactory.count` |
| `unitName.id` |
| `unitName.name` |
| `sta.id` |
| `sta.name` |
| `item.modelPicture` |
| `item.root.categoryName` |
| `obj.product.productName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setTab(7)` |
| `setTab(4)` |
| `setTab(5)` |
| `setTab(6)` |
| `chooseImg($index)` |
| `deleteProduct($index)` |
| `addProductList()` |
| `modify()` |
| `selectCategory(item.childList,item.root.categoryName,item.root.id)` |
| `selectCategoryId(item.root.categoryName,item.root.id)` |
| `hideCategory()` |
| `setAllProduct()` |
| `setAllModal=false` |
| `firstApproval.confirm()` |

**跳转到**：`systemSetting.materiallist`

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
x.id as x.name for x in unitNames
```

### 2.42 `systemSetting.materiallist`

- **URL**：`/materiallist`
- **模板**：`views/systemSetting/materiallist.html`
- **控制器**：`materiallistCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createProductBatchFileTask` | `POST /admin/createProductBatchFileTask.json` |
| `deleteProductSkus` | `POST /admin/deleteProductSkus.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategory` | `POST /admin/getCategory.json` |
| `getCategoryTree2LevelWithSkuCount` | `POST /admin/getCategoryTree2LevelWithSkuCount.json` |
| `getProductSkuVoList` | `POST /admin/getProductSkuVoList.json` |
| `updateByProductSkuIdArraySelective` | `POST /admin/updateByProductSkuIdArraySelective.json` |

**表单标签**

| 标签 |
|---|
| 证件过期预警 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 状态 |
| 5 | 允许折扣 |
| 6 | 允许积分 |
| 7 | 首营审批 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.qualifyExpiresWarning` |
| `obj.keyword` |
| `obj.priceFromInclude` |
| `obj.priceToInclude` |
| `object.status` |
| `object.canBeDiscounted` |
| `object.allowPoints` |
| `isAll` |
| `productSkuIdArray[$index+getSupplierListFactory.index-pageSize]` |
| `pageSize` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `searchCategoryObjectFactory.object.productSkuCount` |
| `item.root.categoryName` |
| `item.productSkuCount` |
| `iten.root.categoryName` |
| `iten.productSkuCount` |
| `getSupplierListFactory.count` |
| `province.id` |
| `province.brandName` |
| `item.productSku.id` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.productSku.status` |
| `supplierStatus` |
| `item.productSku.canBeDiscounted` |
| `discountStatus` |
| `item.productSku.allowPoints` |
| `data.filepath` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goAdd(` |
| `importModal=true` |
| `downloadModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `searchTab()` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchDiscount()` |
| `searchDiscount(1)` |
| `searchDiscount(0)` |
| `searchPoints()` |
| `searchPoints(1)` |
| `searchPoints(0)` |
| `tagModal=true` |
| `changeSeletedProduct(1)` |
| `hideTagModal($event)` |
| `discountModal=true` |
| `changeSeletedProduct(3)` |
| `pointModal=true` |
| `changeSeletedProduct(2)` |
| `deleteBatch()` |
| `checkAll()` |
| `setLabelBtn()` |
| `modifyMaterial(item.product.id,item.productSku.id)` |
| `createTask()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

### 2.43 `systemSetting.medicalFeesList`

- **URL**：`/medicalFeesList`
- **模板**：`views/systemSetting/medicalFeesList.html`
- **控制器**：`medicalFeesListCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 正常 停用 确定 取消 设置折扣 设置折扣 折扣 打折 |
| 不打折 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 挂号费名称 |
| 2 | 挂号费金额 |
| 3 | 成本价 |
| 4 | 状态 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `object.status` |
| `discount.canBeDiscounted` |
| `isAll` |
| `examineIdArray[$index+getSupplierListFactory.index-pageSize]` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.examine.id` |
| `item.examine.examineName` |
| `item.examine.marketPrice` |
| `item.examine.costPrice` |
| `item.examine.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchDiscount(null)` |
| `searchDiscount(1)` |
| `searchDiscount(0)` |
| `tagModal=true` |
| `changeStatus()` |
| `hideTagModal($event)` |
| `discountModal=true` |
| `changeDiscount()` |
| `deleteBatch()` |
| `checkAll()` |
| `setLabelBtn()` |

**跳转到**：`systemSetting.addMedicalFee`

### 2.44 `systemSetting.memberChannelList`

- **URL**：`/memberChannelList`
- **模板**：`views/systemSetting/memberChannelList.html`
- **控制器**：`memberChannelListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 来源名称 |
| 2 | 创建日期 |
| 3 | 个数 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `add.tagName` |
| `modify.tagName` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberSource.getName` |
| `sourceTotal` |
| `item.tagName` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.useCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showModal(0,[])` |
| `addSupplier()` |
| `hideModal()` |
| `showChild(item)` |
| `showModal(item.id,item.childList)` |
| `showModify(item.tagName,item.id)` |
| `$event.stopPropagation()` |
| `modifyTag(item.id,$event,$index)` |
| `cancel($event)` |
| `deleteContent=true` |
| `deleteTemplate(item.id)` |
| `$event.stopPropagation();deleteContent=false` |

### 2.45 `systemSetting.memberCharge`

- **URL**：`/memberCharge`
- **模板**：`views/systemSetting/memberCharge.html`
- **控制器**：`memberChargeCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 余额支付： |
| 优先使用本金 |
| 优先使用赠金 |
| 本金赠金同比例使用 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.substractType` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

### 2.46 `systemSetting.memberTypeList`

- **URL**：`/memberTypeList`
- **模板**：`views/systemSetting/memberTypeList.html`
- **控制器**：`memberTypeListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 会员类型名称 |
| 2 | 折扣 |
| 3 | 状态 |
| 4 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.memberName` |
| `item.examineRate` |
| `item.productRate` |
| `item.status` |
| `supplierStatus` |

**跳转到**：`systemSetting.addMemberType`

### 2.47 `systemSetting.memberTypeModify`

- **URL**：`/memberTypeModify?id`
- **模板**：`views/systemSetting/memberTypeModify.html`
- **控制器**：`memberTypeModifyCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 会员类型名称 |
| * 检查费用折扣 |
| * 产品费用折扣 |

**表单标签**

| 标签 |
|---|
| * 会员类型名称 |
| * 检查费用折扣 |
| * 产品费用折扣 |
| 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.memberName` |
| `obj.examineRate` |
| `obj.productRate` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.48 `systemSetting.messageAdmin`

- **URL**：`/messageAdmin`
- **模板**：`views/systemSetting/messageAdmin.html`
- **控制器**：`messageAdminCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCorpSmsAddLogVoList` | `POST /admin/selectCorpSmsAddLogVoList.json` |
| `selectCorpSmsByCorpId` | `POST /admin/selectCorpSmsByCorpId.json` |
| `selectCorpSmsUseLogVoList` | `POST /admin/selectCorpSmsUseLogVoList.json` |
| `selectDataCorpSmsList` | `POST /admin/selectDataCorpSmsList.json` |
| `updateCorpSmsDisable` | `POST /admin/updateCorpSmsDisable.json` |
| `updateCorpSmsWarningCount` | `POST /admin/updateCorpSmsWarningCount.json` |

**表单标签**

| 标签 |
|---|
| 我已知晓相关影响,并同意关闭 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 月份 |
| 2 | 短信使用量 根据电信公司的计费标准，如果一条短信超过了67个字符计算为两条短信，按两条短信收费；超过134个字符计算为三条短信，以此类推。 |
| 3 | 时间 |
| 4 | 商户订单号 |
| 5 | 充值条数 |
| 6 | 充值金额 |
| 7 | 支付类型 |
| 8 | 备注 |
| 9 | 操作人 |
| 10 | 发送时间 |
| 11 | 操作人 |
| 12 | 短信使用量 |
| 13 | 短信内容 |
| 14 | 短信手机号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `buy.startTime` |
| `rightTimer` |
| `obj.warningCount` |
| `smsOptions[smsDisable].model` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `smsDisable` |
| `dealWithSmsVoice` |
| `sms` |
| `obj.smsCount` |
| `obj.warningCount` |
| `item` |
| `CompanyOkSaleListFactory.result.total.useCount` |
| `item.ym` |
| `date` |
| `yyyy` |
| `MM` |
| `item.useCount` |
| `item.corpSmsAddLog.gmtCreate` |
| `dd` |
| `HH` |
| `mm` |
| `item.corpSmsAddLog.recordNo` |
| `item.corpSmsAddLog.addCount` |
| `item.corpSmsAddLog.addMoney` |
| `item.corpPaymentVo.corpPayment.payChannel` |
| `payTypeSms` |
| `item.corpSmsAddLog.remark` |
| `item.corpSmsAddLog.cashierName` |
| `item.smsLog.gmtCreate` |
| `item.smsLog.userName` |
| `item.corpSmsUseLog.useCount` |
| `item.smsLog.smsContent` |
| `item.smsLog.smsPhone` |
| `smsOptions` |
| `title` |
| `tip` |
| `index` |

**页面动作（ng-click）**

| 动作 |
|---|
| `smsCharge()` |
| `setCount()` |
| `showPhoto=true` |
| `operationSms(0)` |
| `operationSms(1)` |
| `searchUse()` |
| `searchRecord(1)` |
| `searchRecord(2)` |
| `setDate(item,$index)` |
| `open1()` |
| `open2()` |
| `setDateSearch(year,1)` |
| `setDateSearch(item.ym,2)` |
| `modify()` |
| `hideModal()` |
| `updateSms()` |
| `smsOptions.close()` |

### 2.49 `systemSetting.modifyCustomerCharge`

- **URL**：`/modifyCustomerCharge?productId&productSkuId`
- **模板**：`views/systemSetting/modifyCustomerCharge.html`
- **控制器**：`modifyCustomerChargeCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getIntroducer` | `POST /admin/getIntroducer.json` |
| `getModelNameVo` | `POST /admin/getModelNameVo.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `getProductSkuModelVo` | `POST /admin/getProductSkuModelVo.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `selectModelNameVoList` | `POST /admin/selectModelNameVoList.json` |
| `selectModelValueList` | `POST /admin/selectModelValueList.json` |
| `updateIntroducer` | `POST /admin/updateIntroducer.json` |
| `updateModelName` | `POST /admin/updateModelName.json` |
| `updateProductAndModelList` | `POST /admin/updateProductAndModelList.json` |

**必填项**

| 标签 |
|---|
| * 产品名称 |
| * 产品编码 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 单位 |
| * 成本价 |
| * 零售价 |
| * 绩效 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |

**表单标签**

| 标签 |
|---|
| * 产品名称 |
| * 产品编码 |
| * 品牌 |
| * 类目 {{CommonRemark.category}} |
| * 单位 |
| * 成本价 |
| * 零售价 |
| * 绩效 |
| * 状态 |
| * 允许折扣 |
| * 允许积分 |
| 拼音 |
| 英文名称 |
| 默认供应商 |
| 生产厂家 |
| 生产许可证号 |
| 备注 |
| 图片 |
| {{categoryItem.categoryItem.itemName}} |
| 全选 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 参数名称 |
| 2 | 可选值 |
| 3 | 顺序 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.productCode` |
| `categoryName` |
| `obj.unitName` |
| `obj.costPrice` |
| `obj.marketPrice` |
| `obj.kpiPrice` |
| `obj.status` |
| `obj.canBeDiscounted` |
| `obj.allowPoints` |
| `obj.pinyin` |
| `obj.englishName` |
| `obj.factory` |
| `obj.factoryLicense` |
| `obj.remark` |
| `modelName.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `CommonRemark.category` |
| `unitName.id` |
| `unitName.name` |
| `sta.id` |
| `sta.name` |
| `obj.modelPicture` |
| `categoryItem.categoryItem.itemName` |
| `iten.name` |
| `item.root.categoryName` |
| `item.modelName.name` |
| `iten.value` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `chooseImg()` |
| `searchModelList()` |
| `showModalName(iten.modelNameId)` |
| `upMove(selectedName,$index,selectedName.length)` |
| `downMove(selectedName,$index,selectedName.length)` |
| `deleteItem($index)` |
| `modify()` |
| `selectCategory(item.childList,item.root.categoryName,item.root.id)` |
| `selectCategoryId(item.root.categoryName,item.root.id)` |
| `hideCategory()` |
| `selectAll($event)` |
| `updateSelection($event,item.modelName.id,item.modelName.name)` |
| `schoolModal=false` |
| `addName()` |
| `modelNameModal=false` |
| `firstApproval.confirm()` |

**跳转到**：`systemSetting.customerCharge`

### 2.50 `systemSetting.modifyCustomerChargeItem`

- **URL**：`/modifyCustomerChargeItem?id`
- **模板**：`views/systemSetting/modifyCustomerChargeItem.html`
- **控制器**：`modifyCustomerChargeItemCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 参数名称 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 参数名称 |
| * 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.name` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**跳转到**：`systemSetting.customerChargeItem`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.51 `modifyFirstDoctor`

- **URL**：`/modifyFirstDoctor?id`
- **模板**：`views/systemSetting/modifyFirstDoctor.html`
- **控制器**：`modifyFirstDoctorCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 推荐人名称 |
| * 来源 |

**表单标签**

| 标签 |
|---|
| * 推荐人名称 |
| 手机号 |
| * 来源 |
| 备注 |
| 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.name` |
| `obj.mobile` |
| `obj.remark` |
| `obj.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ft` |

**页面动作（ng-click）**

| 动作 |
|---|
| `obj.fromType=$index` |
| `modify()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in statusArr
```

### 2.52 `systemSetting.modifyGroupedit`

- **URL**：`/modifyGroupedit?id`
- **模板**：`views/systemSetting/modifyGroupedit.html`
- **控制器**：`modifyGroupeditCtrl`
- **端点数**：15

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getExamineVo` | `POST /admin/getExamineVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `getMachineCenterVo` | `POST /admin/getMachineCenterVo.json` |
| `getMedicalCheckItemVo` | `POST /admin/getMedicalCheckItemVo.json` |
| `getPackageVo` | `POST /admin/getPackageVo.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `getProductVo` | `POST /admin/getProductVo.json` |
| `getProductVoList` | `POST /admin/getProductVoList.json` |
| `updateExamine` | `POST /admin/updateExamine.json` |
| `updateMachineCenterCompanyIdArray` | `POST /admin/updateMachineCenterCompanyIdArray.json` |
| `updateMachineCenterInfo` | `POST /admin/updateMachineCenterInfo.json` |
| `updateMedicalCheckItem` | `POST /admin/updateMedicalCheckItem.json` |
| `updatePackage` | `POST /admin/updatePackage.json` |

**必填项**

| 标签 |
|---|
| * 套餐名称 |
| * 检查列表 |
| * 套餐折扣（请输入 0 到 100之间的整数，如 50 表示 5 折） % * 套餐金额 元 * 状态 |

**表单标签**

| 标签 |
|---|
| * 套餐名称 |
| * 检查列表 |
| * 套餐折扣（请输入 0 到 100之间的整数，如 50 表示 5 折） % * 套餐金额 元 * 状态 |
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.packageName` |
| `iten.examineName` |
| `obj.status` |
| `isAll` |
| `obj.keyword` |
| `checkItemIdRealArray[$index+schoolListFactory.index-12]` |
| `obj.packageRate` |
| `obj.packageFee` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.examineName` |
| `iten.unitName` |
| `iten.marketPrice` |
| `iten.id` |
| `item.examine.id` |
| `item.examine.examineName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `getItemList(iten.id)` |
| `deleteItem($index)` |
| `showCheckModal()` |
| `add()` |
| `checkAll()` |
| `selectId(schoolListFactory.index)` |
| `schoolModal=false` |
| `modifyCheck()` |

**跳转到**：`systemSetting.groupeditList`

### 2.53 `systemSetting.modifyInspect`

- **URL**：`/modifyInspect?id`
- **模板**：`views/systemSetting/modifyInspect.html`
- **控制器**：`modifyInspectCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 项目名称 |

**表单标签**

| 标签 |
|---|
| * 项目名称 |
| 英文缩写 |
| 单位 |
| 定量 |
| 定性 |
| 可选项 |
| 单选 |
| 多选 |
| 特殊 |
| 临床意义 |
| 状态 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 可选项 单选 单选 多选 |
| 3 | 性别 |
| 4 | 年龄 |
| 5 | 参考值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.checkItemName` |
| `obj.checkItemEnglish` |
| `obj.checkItemUnitName` |
| `obj.checkItemType` |
| `choose` |
| `obj.singleValue` |
| `iten.rank1` |
| `iten.checkItemValue` |
| `obj.checkItemValueSample` |
| `obj.checkItemValueMin` |
| `obj.checkItemValueMax` |
| `except` |
| `iten.gender` |
| `iten.ageMin` |
| `iten.ageMax` |
| `iten.checkItemValueMin` |
| `iten.checkItemValueMax` |
| `obj.checkItemMeaning` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteValueItem($index)` |
| `addValueItem()` |
| `deleteItem($index)` |
| `addItem()` |
| `updateInspect()` |

**跳转到**：`systemSetting.InspectList`

### 2.54 `systemSetting.modifyMedicalFee`

- **URL**：`/modifyMedicalFee?id`
- **模板**：`views/systemSetting/modifyMedicalFee.html`
- **控制器**：`modifyMedicalFeeCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| 挂号费名称 * |
| 挂号费金额 * |
| 成本价 * |
| 状态 * |
| 允许折扣 * |

**表单标签**

| 标签 |
|---|
| 挂号费名称 * |
| 拼音码 |
| 挂号费金额 * |
| 成本价 * |
| 状态 * |
| 允许折扣 * |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.examineName` |
| `obj.pinyin` |
| `obj.marketPrice` |
| `obj.costPrice` |
| `obj.status` |
| `obj.canBeDiscounted` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in discounts
x.id as x.name for x in status
```

### 2.55 `systemSetting.modifyProcessCenter`

- **URL**：`/modifyProcessCenter?id`
- **模板**：`views/systemSetting/modifyProcessCenter.html`
- **控制器**：`modifyProcessCenterCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 加工中心名称： |

**表单标签**

| 标签 |
|---|
| * 加工中心名称： |
| 加工中心类型： |
| 店内加工中心 |
| 连锁加工中心 |
| 状态 |
| {{item.name}} |
| 全选 |
| {{item.companyName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.machineCenterName` |
| `obj.status` |
| `company.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.machineCenterName` |
| `item.name` |
| `corpInfo.` |
| `companyTitle` |
| `item.companyName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `toggleTab(1)` |
| `toggleTab(2)` |
| `modifyDepot()` |
| `delteCompany($index)` |
| `showAddModal()` |
| `updateMachine()` |
| `selectAll($event)` |
| `updateSelection($event,item.id,item.companyName)` |
| `addDepotModal=false` |
| `selectCompany()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.56 `systemSetting.modifyProductPlan`

- **URL**：`/modifyProductPlan?productId`
- **模板**：`views/systemSetting/modifyProductPlan.html`
- **控制器**：`modifyProductPlanCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 套餐名称 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 套餐名称 |
| * 状态 |
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.packageName` |
| `iten.examineName` |
| `iten.packageItemCount` |
| `iten.packageItemRate` |
| `obj.status` |
| `isAll` |
| `keyword` |
| `checkItemIdRealArray[$index+schoolListFactory.index-12]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.examineName` |
| `iten.id` |
| `item.product.id` |
| `item.product.productName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `getItemList(iten.id)` |
| `deleteItem($index)` |
| `showCheckModal()` |
| `add()` |
| `checkAll()` |
| `selectId(schoolListFactory.index)` |
| `schoolModal=false` |
| `modifyCheck()` |

**跳转到**：`systemSetting.productPlanList`

### 2.57 `systemSetting.modifyRecordTemplate`

- **URL**：`/modifyRecordTemplate?id`
- **模板**：`views/systemSetting/modifyRecordTemplate.html`
- **控制器**：`modifyRecordTemplateCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalRecordTemplateVo` | `POST /admin/getMedicalRecordTemplateVo.json` |
| `updateMedicalRecordTemplate` | `POST /admin/updateMedicalRecordTemplate.json` |

**必填项**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |

**表单标签**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |
| 个人使用 |
| 共享使用 |
| 主诉 |
| 现病史 |
| 疾病史 |
| 家族史 |
| 手术史 |
| 过敏史 |
| 其他史 |
| 诊断 |
| 处理意见 |
| 治疗方案 |
| 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.templateName` |
| `obj.shared` |
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
| `obj.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `add()` |

**跳转到**：`systemSetting.recordTemplateList`

### 2.58 `systemSetting.openPlate`

- **URL**：`/openPlate`
- **模板**：`views/systemSetting/openPlate.html`
- **控制器**：`openPlateCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getOpenApp` | `POST /admin/getOpenApp.json` |
| `modifyOpenAppSecret` | `POST /admin/modifyOpenAppSecret.json` |

**必填项**

| 标签 |
|---|
| 域名： |
| AppKey： |
| AppSecret： |

**表单标签**

| 标签 |
|---|
| 域名： |
| AppKey： |
| AppSecret： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.appSecret` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `host` |
| `obj.appKey` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

### 2.59 `systemSetting.phoneAdmin`

- **URL**：`/phoneAdmin`
- **模板**：`views/systemSetting/phoneAdmin.html`
- **控制器**：`phoneAdminCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCorpVoiceAddLogVoList` | `POST /admin/selectCorpVoiceAddLogVoList.json` |
| `selectCorpVoiceByCorpId` | `POST /admin/selectCorpVoiceByCorpId.json` |
| `selectCorpVoiceUseLogVoList` | `POST /admin/selectCorpVoiceUseLogVoList.json` |
| `selectDataCorpVoiceList` | `POST /admin/selectDataCorpVoiceList.json` |
| `updateCorpVoiceDisable` | `POST /admin/updateCorpVoiceDisable.json` |
| `updateCorpVoiceWarningCount` | `POST /admin/updateCorpVoiceWarningCount.json` |

**表单标签**

| 标签 |
|---|
| 我已知晓相关影响,并同意关闭 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 月份 |
| 2 | 智能语音使用量(分钟) 根据电信公司的计费标准，按每通实际通话分钟数扣除，不满一分钟按一分钟扣除。 |
| 3 | 时间 |
| 4 | 商户订单号 |
| 5 | 充值分钟数 |
| 6 | 充值金额 |
| 7 | 支付类型 |
| 8 | 备注 |
| 9 | 操作人 |
| 10 | 发送时间 |
| 11 | 操作人 |
| 12 | 通话时长(秒) |
| 13 | 智能语音使用量(分钟) |
| 14 | 智能语音内容 |
| 15 | 状态 |
| 16 | 智能语音手机号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `buy.startTime` |
| `rightTimer` |
| `obj.warningCount` |
| `voiceOptions[voiceDisable].model` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `voiceDisable` |
| `dealWithSmsVoice` |
| `voice` |
| `obj.currentCount` |
| `obj.warningCount` |
| `item` |
| `CompanyOkSaleListFactory.result.total.useCount` |
| `item.ym` |
| `date` |
| `yyyy` |
| `MM` |
| `item.useCount` |
| `item.corpVoiceAddLog.gmtCreate` |
| `dd` |
| `HH` |
| `mm` |
| `item.corpVoiceAddLog.recordNo` |
| `item.corpVoiceAddLog.addCount` |
| `item.corpVoiceAddLog.addMoney` |
| `item.corpPaymentVo.corpPayment.payChannel` |
| `payTypeSms` |
| `item.corpVoiceAddLog.remark` |
| `item.corpVoiceAddLog.cashierName` |
| `item.voiceLog.gmtCreate` |
| `item.admin.nickname` |
| `item.voiceLog.durationSeconds` |
| `item.corpVoiceUseLog.useCount` |
| `item.voiceLog.voiceContent` |
| `item.voiceLog.sendStatusMessage` |
| `item.voiceLog.voicePhone` |
| `voiceOptions` |
| `title` |
| `index` |

**页面动作（ng-click）**

| 动作 |
|---|
| `smsCharge()` |
| `setCount()` |
| `showPhoto=true` |
| `operationVoice(0)` |
| `operationVoice(1)` |
| `searchUse()` |
| `searchRecord(1)` |
| `searchRecord(2)` |
| `setDate(item,$index)` |
| `open1()` |
| `open2()` |
| `setDateSearch(year,1)` |
| `setDateSearch(item.ym,2)` |
| `modify()` |
| `hideModal()` |
| `updateSms()` |
| `voiceOptions.close()` |

### 2.60 `systemSetting.pointsAdmin`

- **URL**：`/pointsAdmin`
- **模板**：`views/systemSetting/pointsAdmin.html`
- **控制器**：`pointsAdminCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpPointRule` | `POST /admin/getCorpPointRule.json` |
| `saveCorpPointRule` | `POST /admin/saveCorpPointRule.json` |

**表单标签**

| 标签 |
|---|
| 消费自动积分 |
| 积分规则 |
| 积分抵扣 |
| 积分于次年12月31号清零 |
| 积分于当年12月31号清零 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.payAutoPoint` |
| `obj.payMoney` |
| `obj.toPoint` |
| `obj.payPoint` |
| `obj.toMoney` |
| `obj.yearClear` |
| `obj.yearClearNow` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `modify()` |

### 2.61 `systemSetting.printConfig`

- **URL**：`/printConfig`
- **模板**：`views/systemSetting/printConfig.html`
- **控制器**：`printConfigCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSuperAdminMobile` | `POST /admin/getSuperAdminMobile.json` |
| `saveCorpCashConf` | `POST /admin/saveCorpCashConf.json` |
| `selectAdminCashVoList` | `POST /admin/selectAdminCashVoList.json` |
| `selectCompanyCashConfVoList` | `POST /admin/selectCompanyCashConfVoList.json` |
| `selectMachineCenterVoList` | `POST /admin/selectMachineCenterVoList.json` |
| `selectPackageVoList` | `POST /admin/selectPackageVoList.json` |
| `updateCompanyCashConf` | `POST /admin/updateCompanyCashConf.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 所属门店 |
| 2 | 抬头 |
| 3 | logo |
| 4 | 手机号显示 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `msgObj.keyword` |
| `companyCashConfVo.keyword` |
| `editCompanyCashConf.params.cashHeader` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.company.companyName` |
| `item.companyCashConf.cashHeader` |
| `item.companyCashConf.cashLogo` |
| `item.companyCashConf.customerMobileDisable` |

**页面动作（ng-click）**

| 动作 |
|---|
| `editCompanyCashConf.openEdit(item.companyCashConf)` |
| `editCompanyCashConf.setStatus()` |
| `editCompanyCashConf.closeEdit()` |
| `editCompanyCashConf.affirm()` |

### 2.62 `systemSetting.processCenter`

- **URL**：`/processCenter`
- **模板**：`views/systemSetting/processCenter.html`
- **控制器**：`processCenterCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 加工中心名称 |
| 2 | 附属仓库 |
| 3 | 退货仓库 |
| 4 | 类型 |
| 5 | 下单门店 周边哪些门店的销售订单可以发送到该加工中心 |
| 6 | 状态 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.machineCenter.name` |
| `item.storehouse.name` |
| `item.refundStorehouse.name` |
| `item.machineCenter.type` |
| `machineCenterType` |
| `iten.companyName` |
| `item.machineCenter.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchType(null)` |
| `searchType(1)` |
| `searchType(2)` |

**跳转到**：`systemSetting.addProcessCenter`

### 2.63 `systemSetting.productPlanList`

- **URL**：`/productPlanList`
- **模板**：`views/systemSetting/productPlanList.html`
- **控制器**：`productPlanListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 套餐名称 |
| 2 | 收费项目 |
| 3 | 折扣 |
| 4 | 状态 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.itemKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.pkg.packageName` |
| `iten.product.productName` |
| `item.productPackageVoList` |
| `productRate` |
| `item.pkg.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |

**跳转到**：`systemSetting.addInspect`, `systemSetting.addProductPlan`

### 2.64 `systemSetting.projectCard`

- **URL**：`/projectCard`
- **模板**：`views/systemSetting/projectCard.html`
- **控制器**：`projectCardCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `selectTrainerCardList` | `POST /admin/selectTrainerCardList.json` |
| `updateByTrainerCardIdArraySelective` | `POST /admin/updateByTrainerCardIdArraySelective.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 封面图 |
| 2 | 次卡名称 |
| 3 | 售价 |
| 4 | 次数 |
| 5 | 有效期 |
| 6 | 到期提醒 |
| 7 | 允许退卡 |
| 8 | 允许改价 |
| 9 | 允许改次 |
| 10 | 状态 |
| 11 | 备注 |
| 12 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.allowReturnCard` |
| `object.allowChangePrice` |
| `object.allowChangeNumber` |
| `isAll` |
| `examineIdArray[$index+getTrainerCardListFactory.index-pageSize]` |
| `pageSize` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTrainerCardListFactory.count` |
| `item.id` |
| `item.imageCard` |
| `item.trainerCardName` |
| `item.marketPrice` |
| `item.numbers` |
| `item.validMonths` |
| `item.remindDays` |
| `item.allowReturnCard` |
| `isAllow` |
| `item.allowChangePrice` |
| `item.allowChangeNumber` |
| `item.status` |
| `adminStatus` |
| `item.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `pointModal=true` |
| `changeSeletedExam(` |
| `hideTagModal($event)` |
| `tagModal=true` |
| `discountModal=true` |
| `checkAll()` |
| `setLabelBtn()` |

**跳转到**：`systemSetting.addProjectCard`

### 2.65 `systemSetting.recipeAdmin`

- **URL**：`/recipeAdmin`
- **模板**：`views/systemSetting/recipeAdmin.html`
- **控制器**：`recipeAdminCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addCourseType` | `POST /admin/addCourseType.json` |
| `getSuperAdminMobile` | `POST /admin/getSuperAdminMobile.json` |
| `saveCorpCashConf` | `POST /admin/saveCorpCashConf.json` |
| `saveCorpMedicalConfByCorpId` | `POST /admin/saveCorpMedicalConfByCorpId.json` |
| `selectAdminCashVoList` | `POST /admin/selectAdminCashVoList.json` |
| `selectCompanyCashConfVoList` | `POST /admin/selectCompanyCashConfVoList.json` |
| `selectCorpMedicalConfByCorpId` | `POST /admin/selectCorpMedicalConfByCorpId.json` |
| `updateCompanyCashConf` | `POST /admin/updateCompanyCashConf.json` |
| `updateCourseType` | `POST /admin/updateCourseType.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 处方编号 |
| 2 | 处方名称 |
| 3 | 处方内容 |
| 4 | 状态 |
| 5 | 疗程节点名称 |
| 6 | 状态 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.status` |
| `data.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.num` |
| `item.name` |
| `item.content` |
| `item.courseTypeName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(1)` |
| `setTab(2)` |
| `preview(item.preview)` |
| `addCourseType()` |
| `setCourseType(item)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.66 `systemSetting.recordTemplateList`

- **URL**：`/recordTemplateList`
- **模板**：`views/systemSetting/recordTemplateList.html`
- **控制器**：`recordTemplateListCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disableMedicalRecordTemplate` | `POST /admin/disableMedicalRecordTemplate.json` |
| `enableMedicalRecordTemplate` | `POST /admin/enableMedicalRecordTemplate.json` |
| `selectMedicalRecordTemplateVoList` | `POST /admin/selectMedicalRecordTemplateVoList.json` |

**表单标签**

| 标签 |
|---|
| 全部 |
| 个人使用 |
| 共享使用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.shared` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.medicalRecordTemplate.templateName` |
| `item.medicalRecordTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.medicalRecordTemplate.shared` |
| `shared` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setRecyle(1)` |
| `setRecyle(2)` |
| `deleteTemplate(item.medicalRecordTemplate.id)` |
| `recovery(item.medicalRecordTemplate.id)` |

**跳转到**：`systemSetting.addRecordTemplate`

### 2.67 `systemSetting.reportDateAdmin`

- **URL**：`/reportDateAdmin`
- **模板**：`views/systemSetting/reportDateAdmin.html`
- **控制器**：`reportDateAdminCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpReportConf` | `POST /admin/getCorpReportConf.json` |
| `saveCorpReportConf` | `POST /admin/saveCorpReportConf.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.defaultStartMonth` |
| `obj.defaultStartDay` |
| `obj.defaultEndMonth` |
| `obj.defaultEndDay` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `province.id` |
| `province.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

### 2.68 `sataServerList`

- **URL**：`/sataServerList`
- **模板**：`views/systemSetting/sataServerList.html`
- **控制器**：`sataServerListCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeUartDeviceStatus` | `POST /admin/changeUartDeviceStatus.json` |
| `selectUartDeviceList` | `POST /admin/selectUartDeviceList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 智能解码器编号(DeviceCode) |
| 2 | 用途 |
| 3 | 附加用途 |
| 4 | 类型 |
| 5 | 状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `item.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.deviceCode` |
| `item.deviceType` |
| `deviceType` |
| `item.visionParseEnable` |
| `useSataServer` |
| `item.scaParseEnable` |
| `useOptServer` |
| `item.deviceLinkType` |
| `sataServerType` |
| `getServerListFactory.count` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAdd()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchTab2(null)` |
| `searchTab2(1)` |
| `searchTab2(2)` |
| `addDeviceModal=false` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.69 `systemSetting.schoolCheckRecord`

- **URL**：`/schoolCheckRecord`
- **模板**：`views/systemSetting/schoolCheckRecord.html`
- **控制器**：`schoolCheckRecordCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `saveCorpSchoolCheckConf` | `POST /admin/saveCorpSchoolCheckConf.json` |
| `saveCorpWechatMedicalConf` | `POST /admin/saveCorpWechatMedicalConf.json` |
| `selectCorpSchoolCheckConfByCorpId` | `POST /admin/selectCorpSchoolCheckConfByCorpId.json` |
| `selectCorpWechatMedicalConf` | `POST /admin/selectCorpWechatMedicalConf.json` |
| `selectCorpWechatMedicalConfByCorpId` | `POST /admin/selectCorpWechatMedicalConfByCorpId.json` |

**表单标签**

| 标签 |
|---|
| 打开用户评价并显示 |
| 关闭用户评价并隐藏 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 内容 |
| 3 | 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.employeeEvaluateDisable` |
| `item.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.name` |
| `item.content` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `saveCorp()` |
| `modify()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.70 `systemSetting.stockAdmin`

- **URL**：`/stockAdmin`
- **模板**：`views/systemSetting/stockAdmin.html`
- **控制器**：`stockAdminCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `saveStockConf` | `POST /admin/saveStockConf.json` |
| `saveStockConfReleaseStock` | `POST /admin/saveStockConfReleaseStock.json` |

**表单标签**

| 标签 |
|---|
| 不允许超卖 |
| 允许超卖 |
| 付款同时扣减库存 |
| 发货或领料时扣减库存 |
| 退货时回原仓 |
| 退货时进退货仓 |
| 开单时商品快过期不提醒 |
| 开单时商品快过期会提醒 |
| 出入库日期不可选 |
| 出入库日期可选 |
| 横轴显示规格一，纵轴显示规格二 |
| 横轴显示规格二，纵轴显示规格一 |
| 开单后未付款一直不自动释放库存 第二天凌晨三点释放库存 |
| 第十五天凌晨三点释放库存 |
| 第三十天凌晨三点释放库存 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.enableNegativeStock` |
| `obj.stockOutWhenPayOrder` |
| `obj.orderRefundStorehouse` |
| `obj.stockExpiresWarningWhenOrder` |
| `obj.enableStockDateChange` |
| `obj.modelShow` |
| `releaseStock` |

**展示字段（{{}} 插值）**

| 字段 |
|---|

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `modify()` |
| `modifyStock()` |

### 2.71 `systemSetting.suiFangJieLunTem`

- **URL**：`/suiFangJieLunTem?id`
- **模板**：`views/systemSetting/suiFangJieLunTem.html`
- **控制器**：`suiFangJieLunTemCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getFollowUpResultTemplateVo` | `POST /admin/getFollowUpResultTemplateVo.json` |
| `insertFollowUpResultTemplate` | `POST /admin/insertFollowUpResultTemplate.json` |
| `updateFollowUpResultTemplate` | `POST /admin/updateFollowUpResultTemplate.json` |

**必填项**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |
| * 随访结论 |

**表单标签**

| 标签 |
|---|
| * 模板名称 |
| * 模板类型 |
| 个人使用 |
| 共享使用 |
| * 随访结论 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.templateName` |
| `obj.shared` |
| `obj.templateResult` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `add()` |

**跳转到**：`systemSetting.suiFangJieLunTemplate`

### 2.72 `systemSetting.suiFangJieLunTemplate`

- **URL**：`/suiFangJieLunTemplate`
- **模板**：`views/systemSetting/suiFangJieLunTemplate.html`
- **控制器**：`suiFangJieLunTemplateCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteFollowUpResultTemplate` | `POST /admin/deleteFollowUpResultTemplate.json` |
| `enableMedicalRecordTemplate` | `POST /admin/enableMedicalRecordTemplate.json` |
| `selectFollowUpResultTemplateVoList` | `POST /admin/selectFollowUpResultTemplateVoList.json` |

**表单标签**

| 标签 |
|---|
| 全部 |
| 个人使用 |
| 共享使用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |
| 5 | 随访结论 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.shared` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.followUpResultTemplate.templateName` |
| `item.followUpResultTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.followUpResultTemplate.shared` |
| `shared` |
| `item.followUpResultTemplate.templateResult` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteTemplate(item.followUpResultTemplate.id)` |
| `recovery(item.followUpResultTemplate.id)` |

**跳转到**：`systemSetting.suiFangJieLunTem`

### 2.73 `systemSetting.suiFangNeiRongTemplate`

- **URL**：`/suiFangNeiRongTemplate`
- **模板**：`views/systemSetting/suiFangNeiRongTemplate.html`
- **控制器**：`suiFangNeiRongTemplateCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteFollowUpContentTemplate` | `POST /admin/deleteFollowUpContentTemplate.json` |
| `enableMedicalRecordTemplate` | `POST /admin/enableMedicalRecordTemplate.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `getSupplierVoList` | `POST /admin/getSupplierVoList.json` |
| `saveSupplierQualifyList` | `POST /admin/saveSupplierQualifyList.json` |
| `selectFollowUpContentTemplateVoList` | `POST /admin/selectFollowUpContentTemplateVoList.json` |
| `selectSupplierQualifyList` | `POST /admin/selectSupplierQualifyList.json` |
| `updateSupplier` | `POST /admin/updateSupplier.json` |
| `updateSupplierWarningQualifyExpiresDays` | `POST /admin/updateSupplierWarningQualifyExpiresDays.json` |
| `privateDownloadUrl` | `POST /auth/privateDownloadUrl.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |
| 5 | 随访内容 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.shared` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.followUpContentTemplate.templateName` |
| `item.followUpContentTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.followUpContentTemplate.shared` |
| `shared` |
| `item.followUpContentTemplate.templateContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteTemplate(item.followUpContentTemplate.id)` |
| `recovery(item.followUpContentTemplate.id)` |

### 2.74 `systemSetting.supplierCertificate`

- **URL**：`/supplierCertificate?supplierId`
- **模板**：`views/systemSetting/supplierCertificate.html`
- **控制器**：`supplierCertificateCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{item.qualifyTitle}}： |
| 有效期： |
| 长期有效 |
| 营业执照 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `warningQualifyExpiresDays` |
| `item.qualifyCode` |
| `item.qualifyExpireDateLong` |
| `item.qualifyPermanent` |
| `title.qualifyTitle` |
| `title.other` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.qualifyTitle` |
| `index` |
| `item.qualifyFileName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteItem($index)` |
| `setPermanent(item.qualifyPermanent,$index,$event)` |
| `download(item.qualifyFile)` |
| `showModal()` |
| `modify()` |
| `selectQuanlify()` |
| `hideModal()` |

**跳转到**：`systemSetting.supplierList`

### 2.75 `systemSetting.supplierList`

- **URL**：`/supplierList`
- **模板**：`views/systemSetting/supplierList.html`
- **控制器**：`supplierListCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 证件过期预警 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 供应商名称 |
| 2 | 地址 |
| 3 | 电话 |
| 4 | 联系人 |
| 5 | 证件有效期 |
| 6 | 状态 |
| 7 | 首营审批 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.qualifyExpiresWarning` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.supplier.supplierName` |
| `item.supplier.address` |
| `item.supplier.phone` |
| `item.supplier.linkman` |
| `item.minQualifyExpireDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.supplier.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goAdd()` |
| `modifySupplier(item.supplier.id)` |

### 2.76 `systemSetting.supplierModify`

- **URL**：`/supplierModify?supplierId`
- **模板**：`views/systemSetting/supplierModify.html`
- **控制器**：`supplierModifyCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 供应商 |

**表单标签**

| 标签 |
|---|
| * 供应商 |
| 地址 |
| 电话 |
| 联系人 |
| 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.supplierName` |
| `obj.address` |
| `obj.phone` |
| `obj.linkman` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modifySupplier()` |

**跳转到**：`systemSetting.supplierList`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 2.77 `systemSetting`

- **URL**：`/systemSetting`
- **模板**：`views/systemSetting/systemSetting.html`
- **控制器**：`systemSettingCtrl`
- **端点数**：0

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |

### 2.78 `systemSetting.toothCheckTemplate`

- **URL**：`/toothCheckTemplate`
- **模板**：`views/systemSetting/toothCheckTemplate.html`
- **控制器**：`toothCheckTemplateCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteToothCheckTemplate` | `POST /admin/deleteToothCheckTemplate.json` |
| `selectToothCheckTemplateVoList` | `POST /admin/selectToothCheckTemplateVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 模板名称 |
| 2 | 创建日期 |
| 3 | 创建人员 |
| 4 | 类型 |
| 5 | 检查发现 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.shared` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.toothCheckTemplate.templateName` |
| `item.toothCheckTemplate.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.createAdmin.nickname` |
| `item.toothCheckTemplate.shared` |
| `shared` |
| `item.toothCheckTemplate.templateContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteTemplate(item.toothCheckTemplate.id)` |
| `recovery(item.toothCheckTemplate.id)` |

### 2.79 `visionAdmin`

- **URL**：`/visionAdmin?chartType&isSocket`
- **模板**：`views/systemSetting/visionAdmin.html`
- **控制器**：`visionAdminCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getEyeChartConfRemark` | `POST /admin/getEyeChartConfRemark.json` |
| `getEyeChartOfMine` | `POST /admin/getEyeChartOfMine.json` |
| `updateEyeChartConfOfMine` | `POST /admin/updateEyeChartConfOfMine.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**必填项**

| 标签 |
|---|
| 测试距离： |

**表单标签**

| 标签 |
|---|
| 测试距离： |
| 类型： |
| 测试模式： |
| 最小测试行： |
| 最大测试行： |
| 开始测试行： |
| 测试范围： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.testDistance` |
| `obj.testVisionType` |
| `obj.testModel` |
| `minTestIndex` |
| `obj.maxTestIndex` |
| `obj.startTestIndex` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `homeFactory.result.admin.mobile` |
| `eyeChartFactory.result.object.eyeChart.testDistance` |
| `msg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |
| `goBack()` |

**跳转到**：`home`

**下拉数据源（ng-options）**

```
x.id as x.name for x in distances
x.id as x.name for x in visionTypes
```

### 2.80 `systemSetting.wecomAdmin`

- **URL**：`/wecomAdmin`
- **模板**：`views/systemSetting/wecomAdmin.html`
- **控制器**：`wecomAdminCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `activeWecomAccountOfAdmin` | `POST /admin/activeWecomAccountOfAdmin.json` |
| `refreshWecomActiveCodeListOfCorpId` | `POST /admin/refreshWecomActiveCodeListOfCorpId.json` |
| `selectAdminWecomVoList` | `POST /admin/selectAdminWecomVoList.json` |
| `selectNotActiveWecomAdminList` | `POST /admin/selectNotActiveWecomAdminList.json` |
| `transferActiveWecomAccountOfAdmin` | `POST /admin/transferActiveWecomAccountOfAdmin.json` |

**表单标签**

| 标签 |
|---|
| 账号总数：{{adminWecomVoList.total.totalCount }} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登录账号 |
| 2 | 姓名 |
| 3 | 所属门店 |
| 4 | 角色 |
| 5 | 应用授权 |
| 6 | 账号激活 |
| 7 | 操作 |
| 8 | 操作 |
| 9 | 角色 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `wecom.keyword` |
| `transAdmin.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `adminWecomVoList.total.totalCount` |
| `adminWecomVoList.total.notYetBoundCount` |
| `adminWecomVoList.total.boundAndValidCount` |
| `adminWecomVoList.total.invalidCount` |
| `item.adminVo.admin.username` |
| `item.adminVo.admin.nickname` |
| `item.adminVo.company.companyName` |
| `item.adminVo.adminRole.roleName` |
| `item.wecomAdmin` |
| `item.wecomAdmin.authorized` |
| `auth.tip` |
| `auth.sName` |
| `item.nickname` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updatetab(0)` |
| `auth.fun(item)` |
| `transAdmin.choseSingle($index)` |
| `transAdmin.setShow(false)` |
| `transAdmin.affirm()` |
