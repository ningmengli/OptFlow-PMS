# 01｜模块 screenAdmin 校园筛查

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/screenAdmin/` |
| 中文名 | 校园筛查 |
| 开发波次 | W4 |
| 页面数 | **76** |
| 端点数（去重） | **194** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `accessReport` | `/accessReport` | `views/screenAdmin/accessReport.html` | `accessReportCtrl` | 4 |
| 2 | `addSchool` | `/addSchool` | `views/screenAdmin/addSchool.html` | `addSchoolCtrl` | 3 |
| 3 | `addSchoolPlan` | `/addSchoolPlan` | `views/screenAdmin/addSchoolPlan.html` | `addSchoolPlanCtrl` | 8 |
| 4 | `addAreaSchoolPlan` | `/addAreaSchoolPlan` | `views/screenAdmin/addSchoolPlan.html` | `addSchoolPlanCtrl` | 8 |
| 5 | `addScreenPromotion` | `/addScreenPromotion?schoolId&classId` | `views/screenAdmin/addScreenPromotion.html` | `addScreenPromotionCtrl` | 0 |
| 6 | `childVisionMesure` | `/childVisionMesure` | `views/screenAdmin/childVisionMesure.html` | `visionMesureCtrl` | 3 |
| 7 | `classList` | `/classList?schoolId` | `views/screenAdmin/classList.html` | `classListCtrl` | 10 |
| 8 | `classReportInschool` | `/classReportInschool` | `views/screenAdmin/classReportInschool.html` | `classReportInschoolCtrl` | 9 |
| 9 | `cloudPrinterConfig` | `/cloudPrinterConfig` | `views/screenAdmin/cloudPrinterConfig.html` | `cloudPrinterConfigCtrl` | 0 |
| 10 | `cloudPrinterList` | `/cloudPrinterList` | `views/screenAdmin/cloudPrinterList.html` | `cloudPrinterListCtrl` | 8 |
| 11 | `contrastReportByArea` | `/contrastReportByArea` | `views/screenAdmin/contrastReportByArea.html` | `contrastReportByAreaCtrl` | 2 |
| 12 | `contrastReportInschool` | `/contrastReportInschool` | `views/screenAdmin/contrastReportInschool.html` | `contrastReportInschoolCtrl` | 6 |
| 13 | `dataChart` | `/dataChart` | `views/screenAdmin/dataChart.html` | `dataChartCtrl` | 8 |
| 14 | `exportrec` | `/exportrec` | `views/screenAdmin/exportrec.html` | `exportrecCtrl` | 6 |
| 15 | `fundus` | `/fundus` | `views/screenAdmin/fundus.html` | `fundusCtrl` | 4 |
| 16 | `fundusLog` | `/fundusLog?fundusDeviceId` | `views/screenAdmin/fundusLog.html` | `fundusLogCtrl` | 1 |
| 17 | `healthScreenConfig` | `/healthScreenConfig` | `views/screenAdmin/healthScreenConfig.html` | `healthScreenConfigCtrl` | 3 |
| 18 | `inspection` | `/inspection` | `views/screenAdmin/inspection.html` | `inspectionCtrl` | 6 |
| 19 | `markOriginSet` | `/markOriginSet` | `views/screenAdmin/markOriginSet.html` | `markOriginSetCtrl` | 8 |
| 20 | `mateCheckReportConfig` | `/mateCheckReportConfig?type` | `views/screenAdmin/mateCheckReportConfig.html` | `mateCheckReportConfigCtrl` | 0 |
| 21 | `mateCheckReportList` | `/mateCheckReportList` | `views/screenAdmin/mateCheckReportList.html` | `schoolMateCheckReportsCtrl` | 0 |
| 22 | `mateCheckReportListNew` | `/mateCheckReportListNew` | `views/screenAdmin/mateCheckReportListNew.html` | `mateCheckReportListNewCtrl` | 0 |
| 23 | `mateClassReport` | `/mateClassReport` | `views/screenAdmin/mateClassReport.html` | `screenClassReportCtrl` | 5 |
| 24 | `mateContrastReport` | `/mateContrastReport` | `views/screenAdmin/mateContrastReport.html` | `screenContrastReportCtrl` | 5 |
| 25 | `mateProgressReport` | `/mateProgressReport` | `views/screenAdmin/mateProgressReport.html` | `mateProgressReportCtrl` | 4 |
| 26 | `mateRecordReport` | `/mateRecordReport` | `views/screenAdmin/mateRecordReport.html` | `screenStudentReportCtrl` | 9 |
| 27 | `mateSchoolReport` | `/mateSchoolReport` | `views/screenAdmin/mateSchoolReport.html` | `screenSchoolReportCtrl` | 1 |
| 28 | `medicalConfig` | `/medicalConfig` | `views/screenAdmin/medicalConfig.html` | `medicalConfigCtrl` | 6 |
| 29 | `modifyHealthScreen` | `/modifyHealthScreen?checkId&checkCode` | `views/screenAdmin/modifyHealthScreen.html` | `modifyHealthScreenCtrl` | 8 |
| 30 | `modifyMateCheck` | `/modifyMateCheck?checkId` | `views/screenAdmin/modifyMateCheck.html` | `modifyMateCheckCtrl` | 0 |
| 31 | `modifySchoolMateCheck` | `/modifySchoolMateCheck?checkId` | `views/screenAdmin/modifySchoolMateCheck.html` | `modifySchoolMateCheckCtrl` | 8 |
| 32 | `modifySchoolPlan` | `/modifySchoolPlan?schoolPlanId` | `views/screenAdmin/modifySchoolPlan.html` | `modifySchoolPlanCtrl` | 13 |
| 33 | `modifyAreaSchoolPlan` | `/modifyAreaSchoolPlan?schoolPlanId` | `views/screenAdmin/modifySchoolPlan.html` | `modifySchoolPlanCtrl` | 13 |
| 34 | `modifyScreenPromotion` | `/modifyScreenPromotion?promotionId&schoolPlanId` | `views/screenAdmin/modifyScreenPromotion.html` | `modifyScreenPromotionCtrl` | 0 |
| 35 | `multiImportStudent` | `/multiImportStudent` | `views/screenAdmin/multiImportStudent.html` | `multiImportStudentCtrl` | 8 |
| 36 | `physicalContrastReport` | `/physicalContrastReport` | `views/screenAdmin/physicalContrastReport.html` | `physicalContrastReportCtrl` | 5 |
| 37 | `physicalReport` | `/physicalReport` | `views/screenAdmin/physicalReport.html` | `physicalReportCtrl` | 0 |
| 38 | `pos` | `/pos` | `views/screenAdmin/pos.html` | `posCtrl` | 6 |
| 39 | `printStudentReport` | `/printStudentReport` | `views/screenAdmin/printStudentReport.html` | `printStudentReportCtrl` | 1 |
| 40 | `progressReport` | `/progressReport` | `views/screenAdmin/progressReport.html` | `progressReportCtrl` | 4 |
| 41 | `projectionScreen` | `/projectionScreen` | `views/screenAdmin/projectionScreen.html` | `projectionScreenCtrl` | 7 |
| 42 | `reachStoreAppointAllReport` | `/reachStoreAppointAllReport` | `views/screenAdmin/reachStoreAppointAllReport.html` | `reachStoreAppointAllReportCtrl` | 1 |
| 43 | `reachStoreAppointDetails` | `/reachStoreAppointDetails` | `views/screenAdmin/reachStoreAppointDetails.html` | `reachStoreAppointDetailsCtrl` | 4 |
| 44 | `reachStoreAppointSingleReport` | `/reachStoreAppointSingleReport` | `views/screenAdmin/reachStoreAppointSingleReport.html` | `reachStoreAppointSingleReportCtrl` | 1 |
| 45 | `reportRecord` | `/reportRecord` | `views/screenAdmin/reportRecord.html` | `reportRecordCtrl` | 1 |
| 46 | `reportStatistic` | `/reportStatistic` | `views/screenAdmin/reportStatistic.html` | `reportStatisticCtrl` | 11 |
| 47 | `schoolList` | `/schoolList` | `views/screenAdmin/schoolList.html` | `schoolListCtrl` | 0 |
| 48 | `schoolMateCheckList` | `/schoolMateCheckList?promotionId&schoolPlanId` | `views/screenAdmin/schoolMateCheckList.html` | `schoolMateCheckListCtrl` | 0 |
| 49 | `schoolMateCheckReports` | `/schoolMateCheckReports` | `views/screenAdmin/schoolMateCheckReports.html` | `schoolMateCheckReportsCtrl` | 0 |
| 50 | `schoolPlanList` | `/schoolPlanList` | `views/screenAdmin/schoolPlanList.html` | `schoolPlanListCtrl` | 8 |
| 51 | `areaSchoolPlanList` | `/areaSchoolPlanList` | `views/screenAdmin/schoolPlanList.html` | `schoolPlanListCtrl` | 8 |
| 52 | `schoolPlanReport` | `/schoolPlanReport` | `views/screenAdmin/schoolPlanReport.html` | `schoolPlanReportCtrl` | 5 |
| 53 | `screenBackConfig` | `/screenBackConfig` | `views/screenAdmin/screenBackConfig.html` | `screenBackConfigCtrl` | 4 |
| 54 | `screenClassReport` | `/screenClassReport` | `views/screenAdmin/screenClassReport.html` | `screenClassReportCtrl` | 5 |
| 55 | `screenConditionBatch` | `/screenConditionBatch` | `views/screenAdmin/screenConditionBatch.html` | `screenConditionBatchCtrl` | 2 |
| 56 | `screenConditionBatchGroupSend` | `/screenConditionBatchGroupSend?taskScreenTemplateBatchSendId` | `views/screenAdmin/screenConditionBatchGroupSend.html` | `screenConditionBatchGroupSendCtrl` | 4 |
| 57 | `screenConditionBatchGroupSendLook` | `/screenConditionBatchGroupSendLook?taskScreenTemplateBatchSendId` | `views/screenAdmin/screenConditionBatchGroupSendLook.html` | `screenConditionBatchGroupSendLookCtrl` | 1 |
| 58 | `screenContrastReport` | `/screenContrastReport` | `views/screenAdmin/screenContrastReport.html` | `screenContrastReportCtrl` | 5 |
| 59 | `screenInStore` | `/screenInStore` | `views/screenAdmin/screenInStore.html` | `screenInStoreCtrl` | 5 |
| 60 | `screenList` | `/screenList?promotionId&schoolPlanId` | `views/screenAdmin/screenList.html` | `screenListCtrl` | 16 |
| 61 | `screenPromotionConfig` | `/screenPromotionConfig` | `views/screenAdmin/screenPromotionConfig.html` | `screenPromotionConfigCtrl` | 19 |
| 62 | `screenPromotionList` | `/screenPromotionList` | `views/screenAdmin/screenPromotionList.html` | `screenPromotionListCtrl` | 15 |
| 63 | `screenPromotionStudent` | `/screenPromotionStudent` | `views/screenAdmin/screenPromotionStudent.html` | `screenPromotionStudentCtrl` | 10 |
| 64 | `screenPromotionToothConfig` | `/screenPromotionToothConfig` | `views/screenAdmin/screenPromotionToothConfig.html` | `screenPromotionToothConfigCtrl` | 8 |
| 65 | `screenRecordReport` | `/screenRecordReport` | `views/screenAdmin/screenRecordReport.html` | `screenRecordReportCtrl` | 0 |
| 66 | `screenReportInschool` | `/screenReportInschool` | `views/screenAdmin/screenReportInschool.html` | `screenReportInschoolCtrl` | 3 |
| 67 | `screenSchoolReport` | `/screenSchoolReport` | `views/screenAdmin/screenSchoolReport.html` | `screenSchoolReportCtrl` | 1 |
| 68 | `screenStudentReport` | `/screenStudentReport` | `views/screenAdmin/screenStudentReport.html` | `screenStudentReportCtrl` | 9 |
| 69 | `screenUrlConfig` | `/screenUrlConfig` | `views/screenAdmin/screenUrlConfig.html` | `screenUrlConfigCtrl` | 3 |
| 70 | `studentReportInschool` | `/studentReportInschool` | `views/screenAdmin/studentReportInschool.html` | `studentReportInschoolCtrl` | 11 |
| 71 | `transformationRate` | `/transformationRate` | `views/screenAdmin/transformationRate.html` | `transformationRateCtrl` | 3 |
| 72 | `updateSchool` | `/updateSchool?schoolId` | `views/screenAdmin/updateSchool.html` | `updateSchoolCtrl` | 5 |
| 73 | `viewSchoolMateCheck` | `/viewSchoolMateCheck?checkId` | `views/screenAdmin/viewSchoolMateCheck.html` | `modifySchoolMateCheckCtrl` | 8 |
| 74 | `adultVisionMesure` | `/adultVisionMesure` | `views/screenAdmin/visionMesure.html` | `visionMesureCtrl` | 3 |
| 75 | `visionMesure` | `/visionMesure` | `views/screenAdmin/visionSelect.html` | `visionMesureCtrl` | 3 |
| 76 | `zhiShiBangConfig` | `/zhiShiBangConfig` | `views/screenAdmin/zhiShiBangConfig.html` | `zhiShiBangConfigCtrl` | 4 |

## §2 端点清单（去重 194 个）

- `POST /admin/addEmployeeSchedulingAndDetail.json`
- `POST /admin/addEmployeeSchedulingTempNumber.json`
- `POST /admin/addPrinter.json`
- `POST /admin/autoChartSizeForPad.json`
- `POST /admin/bandingSchoolMatePromotion.json`
- `POST /admin/basicStatAppointSchoolMate.json`
- `POST /admin/basicStatGenderVision.json`
- `POST /admin/basicStatVisionOfManage.json`
- `POST /admin/basicStatVisionOfManageOfArea.json`
- `POST /admin/basicStatVisionOfManageOfCheckYear.json`
- `POST /admin/basicStatVisionOfManageOfGender.json`
- `POST /admin/basicStatVisionOfManageOfLast3Year.json`
- `POST /admin/basicStatVisionOfManageOfSchoolLevel.json`
- `POST /admin/batchInsertSchoolClass.json`
- `POST /admin/batchInsertSchoolClassByNames.json`
- `POST /admin/cancelAppointOfPatient.json`
- `POST /admin/cancelScreenTemplateBatchSendTask.json`
- `POST /admin/checkSchoolBodyCheckInfoVersion.json`
- `POST /admin/cleanPrinterTask.json`
- `POST /admin/commitBatchSchoolMateTask.json`
- `POST /admin/completeSchoolMateCheck.json`
- `POST /admin/completeSchoolPlanSchool.json`
- `POST /admin/copyLastWeek.json`
- `POST /admin/countStatSchoolMateCheckIdList.json`
- `POST /admin/createBatchSchoolMateTask.json`
- `POST /admin/createExamine.json`
- `POST /admin/createPromotionOfSchool.json`
- `POST /admin/createScreenTemplateBatchSendTask.json`
- `POST /admin/delEmployeeSchedulingAndDetail.json`
- `POST /admin/delSchoolCheckWechatShow.json`
- `POST /admin/deleteFundusDevice.json`
- `POST /admin/deletePosDevice.json`
- `POST /admin/deletePrinter.json`
- `POST /admin/deleteSchool.json`
- `POST /admin/deleteSchoolCheckImageFile.json`
- `POST /admin/deleteSchoolClass.json`
- `POST /admin/disBandingSchoolMatePromotion.json`
- `POST /admin/disableSchoolMateCheck.json`
- `POST /admin/disableSchoolPlan.json`
- `POST /admin/enableSchoolMateCheck.json`
- `POST /admin/enableSchoolPlan.json`
- `POST /admin/getAppointSchoolMateVo.json`
- `POST /admin/getArea.json`
- `POST /admin/getBodyCheck.json`
- `POST /admin/getBodyCheckItem.json`
- `POST /admin/getBodyCheckList.json`
- `POST /admin/getBodyCheckVoList.json`
- `POST /admin/getCloudPrinterVo.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCompanyQrcode.json`
- `POST /admin/getCorpAppointConf.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getCorpSchoolPlanVoOfCompany.json`
- `POST /admin/getDefaultSchoolPlanByAdminId.json`
- `POST /admin/getDefaultSchoolPlanRootByAdminId.json`
- `POST /admin/getEmployeeSchedulingDetailTimeVo.json`
- `POST /admin/getEmployeeSchedulingWeekVoOfCompany.json`
- `POST /admin/getEyeChartOfMine.json`
- `POST /admin/getEyeChartPicVoForPad.json`
- `POST /admin/getFundusDevice.json`
- `POST /admin/getInYearList.json`
- `POST /admin/getPinyin.json`
- `POST /admin/getPosDevice.json`
- `POST /admin/getPromotionVo.json`
- `POST /admin/getRandFirstEyeChartFileByChartType.json`
- `POST /admin/getReportStatusOfSchoolAdmin.json`
- `POST /admin/getSchoolBodyCheckInfo.json`
- `POST /admin/getSchoolBodyCheckInfoListOfSchoolPlan.json`
- `POST /admin/getSchoolBodyCheckPsychologyVo.json`
- `POST /admin/getSchoolCheckConf.json`
- `POST /admin/getSchoolCheckWechatShow.json`
- `POST /admin/getSchoolCheckWechatVo.json`
- `POST /admin/getSchoolClass.json`
- `POST /admin/getSchoolClassList.json`
- `POST /admin/getSchoolInfo.json`
- `POST /admin/getSchoolLevelList.json`
- `POST /admin/getSchoolList.json`
- `POST /admin/getSchoolMateCheckPrintConf.json`
- `POST /admin/getSchoolMateCheckVo.json`
- `POST /admin/getSchoolMateCheckVoByUniqueKey.json`
- `POST /admin/getSchoolMateCheckVoForManage.json`
- `POST /admin/getSchoolMateCheckVoList.json`
- `POST /admin/getSchoolMateCheckVoListOfSecond.json`
- `POST /admin/getSchoolMateCheckVoListWithSameCode.json`
- `POST /admin/getSchoolMateCheckVoManageList.json`
- `POST /admin/getSchoolMateCountOfPromotions.json`
- `POST /admin/getSchoolPlan.json`
- `POST /admin/getSchoolPlanRoot.json`
- `POST /admin/getSchoolTeacher.json`
- `POST /admin/getSchoolTeacherList.json`
- `POST /admin/getSchoolVo.json`
- `POST /admin/getSchoolVoList.json`
- `POST /admin/getSecondCheckQualifyDataManageVo.json`
- `POST /admin/getSecondCheckQualifyDataVo.json`
- `POST /admin/initBodyCheck.json`
- `POST /admin/insertAddress.json`
- `POST /admin/insertSchool.json`
- `POST /admin/insertSchoolClass.json`
- `POST /admin/insertSchoolMate.json`
- `POST /admin/insertSchoolMateAndCreatePromotion.json`
- `POST /admin/insertSchoolMateCheck.json`
- `POST /admin/insertSchoolPlan.json`
- `POST /admin/insertSchoolPlanRoot.json`
- `POST /admin/moveSchoolCheckWechatShow.json`
- `POST /admin/printSchoolPromotionListVoList.json`
- `POST /admin/resetEyeChartOfMine.json`
- `POST /admin/saveCorpAppointConf.json`
- `POST /admin/saveCorpWechatAccountConf.json`
- `POST /admin/saveSchoolBodyCheckInfo.json`
- `POST /admin/saveSchoolCheckBandingType.json`
- `POST /admin/saveSchoolCheckCodeType.json`
- `POST /admin/saveSchoolCheckConf.json`
- `POST /admin/saveSchoolCheckIndicatorBarImage.json`
- `POST /admin/saveSchoolCheckPostConf.json`
- `POST /admin/saveSchoolCheckSecondCheckEnable.json`
- `POST /admin/saveSchoolMateCheck.json`
- `POST /admin/selectAppointSchoolMateVoList.json`
- `POST /admin/selectBodyCheckItemListOfCorp.json`
- `POST /admin/selectBodyCheckVoByCode.json`
- `POST /admin/selectByCorpId.json`
- `POST /admin/selectCheckItemListOfCorp.json`
- `POST /admin/selectCloudPrinterList.json`
- `POST /admin/selectCloudPrinterVoList.json`
- `POST /admin/selectCorpSmsByCorpId.json`
- `POST /admin/selectCorpVoiceByCorpId.json`
- `POST /admin/selectCorpWechatAccountConf.json`
- `POST /admin/selectEmployeeSchedulingDetailListOfCompany.json`
- `POST /admin/selectEmployeeSchedulingDetailTimeVoList.json`
- `POST /admin/selectFundusCheckRecordDetialVoList.json`
- `POST /admin/selectFundusCheckReportVo.json`
- `POST /admin/selectFundusDeviceList.json`
- `POST /admin/selectInYearListBySchoolPlan.json`
- `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json`
- `POST /admin/selectOtherSystemByCorpId.json`
- `POST /admin/selectPosDeviceList.json`
- `POST /admin/selectSchoolCheckImageFileList.json`
- `POST /admin/selectSchoolCheckQuestionnaireConfVoList.json`
- `POST /admin/selectSchoolCheckWechatList.json`
- `POST /admin/selectSchoolCheckWechatShowList.json`
- `POST /admin/selectSchoolMateCheckVoList.json`
- `POST /admin/selectSchoolMateScreenInStoreStatVoList.json`
- `POST /admin/selectSchoolPlanList.json`
- `POST /admin/selectSchoolPlanListBySchool.json`
- `POST /admin/selectSchoolPlanRootList.json`
- `POST /admin/selectSchoolPromotionListVoList.json`
- `POST /admin/selectScreenTemplateBatchSendTaskDetails.json`
- `POST /admin/selectTaskItemList.json`
- `POST /admin/selectTaskScreenTemplateBatchSendList.json`
- `POST /admin/selectTaskTemplateBatchSendLogVoList.json`
- `POST /admin/selectToothCheckTemplateVoList.json`
- `POST /admin/selectVisionGroupList.json`
- `POST /admin/selectVisionGroupManageList.json`
- `POST /admin/sendMsgToSchoolMateCheckBySelected.json`
- `POST /admin/sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json`
- `POST /admin/sendSmsToSchoolMateCheck.json`
- `POST /admin/setBodyCheckItemPrintDisable.json`
- `POST /admin/setBodyCheckPrintDisable.json`
- `POST /admin/setCorpSchoolPlan.json`
- `POST /admin/setDefaultSchoolCheckImageFile.json`
- `POST /admin/setDefaultSchoolPlanByAdminId.json`
- `POST /admin/setDefaultSchoolPlanRootByAdminId.json`
- `POST /admin/splitStringToArray.json`
- `POST /admin/startSchoolPlanSchool.json`
- `POST /admin/statAppointSchoolMateOfCompany.json`
- `POST /admin/statAppointSchoolMateOfCorp.json`
- `POST /admin/statCheckStatusOfPromotion.json`
- `POST /admin/statSchoolComplete.json`
- `POST /admin/statSchoolCompleteGroupManage.json`
- `POST /admin/statSchoolCompleteManage.json`
- `POST /admin/statScreenInStore.json`
- `POST /admin/statVisionOfSchool.json`
- `POST /admin/syncSchoolInfoOfPromotion.json`
- `POST /admin/testPrinter.json`
- `POST /admin/updateAddress.json`
- `POST /admin/updateCloudPrinterInfo.json`
- `POST /admin/updateCloudPrinterStatus.json`
- `POST /admin/updateFundusDeviceStatus.json`
- `POST /admin/updatePosDeviceStatus.json`
- `POST /admin/updatePromotionOfSchool.json`
- `POST /admin/updateSchool.json`
- `POST /admin/updateSchoolCheckPostConf.json`
- `POST /admin/updateSchoolCheckQuestionnaireConf.json`
- `POST /admin/updateSchoolCheckWechat.json`
- `POST /admin/updateSchoolCheckWechatItemValue.json`
- `POST /admin/updateSchoolCheckWechatShowOpenEnable.json`
- `POST /admin/updateSchoolCheckWechatShowStatus.json`
- `POST /admin/updateSchoolClass.json`
- `POST /admin/updateSchoolMateCheck.json`
- `POST /admin/updateSchoolMateCheckPrintConfImageUrl.json`
- `POST /admin/updateSchoolPlan.json`
- `POST /admin/updateSchoolPlanCheckSwitch.json`
- `POST /admin/updateSchoolPlanRoot.json`
- `POST /auth/getMyAdminCorpList.json`
- `POST /auth/isAdminTokenOk.json`

## §3 逐页字段规格

### 1.1 `accessReport`

- **URL**：`/accessReport`
- **模板**：`views/screenAdmin/accessReport.html`
- **控制器**：`accessReportCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |
| `getSchoolMateCheckVoForManage` | `POST /admin/getSchoolMateCheckVoForManage.json` |
| `getSchoolMateCheckVoManageList` | `POST /admin/getSchoolMateCheckVoManageList.json` |
| `getSecondCheckQualifyDataManageVo` | `POST /admin/getSecondCheckQualifyDataManageVo.json` |

**表单标签**

| 标签 |
|---|
| {{item.admin.nickname}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 身份证号 |
| 3 | 学校 |
| 4 | 班级 |
| 5 | 原测/复测 |
| 6 | 戴镜类型 |
| 7 | 戴镜视力(右\|左) |
| 8 | 祼眼视力(右\|左) |
| 9 | 等效球镜(右\|左) |
| 10 | 球镜(右\|左) |
| 11 | 柱镜(右\|左) |
| 12 | 轴位(右\|左) |
| 13 | 检查时间 |
| 14 | 操作 |
| 15 | 姓名 |
| 16 | 出生日期 |
| 17 | 身份证号 |
| 18 | 性别 |
| 19 | 民族 |
| 20 | 籍贯 |
| 21 | 省份 |
| 22 | 城市 |
| 23 | 区县 |
| 24 | 学校 |
| 25 | 班级 |
| 26 | 检查时间 |
| 27 | 眼别 |
| 28 | 裸眼视力 |
| 29 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 30 | 右眼 |
| 31 | 左眼 |
| 32 | 眼别 |
| 33 | 等效球镜度数(球镜+1/2柱镜) |
| 34 | 右眼 |
| 35 | 左眼 |
| 36 | 姓名 |
| 37 | 出生日期 |
| 38 | 身份证号 |
| 39 | 性别 |
| 40 | 民族 |
| 41 | 籍贯 |
| 42 | 省份 |
| 43 | 城市 |
| 44 | 区县 |
| 45 | 学校 |
| 46 | 班级 |
| 47 | 检查时间 |
| 48 | 眼别 |
| 49 | 裸眼视力 |
| 50 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 51 | 右眼 |
| 52 | 左眼 |
| 53 | 眼别 |
| 54 | 等效球镜度数(球镜+1/2柱镜) |
| 55 | 右眼 |
| 56 | 左眼 |
| 57 | 姓名 |
| 58 | 出生日期 |
| 59 | 身份证号 |
| 60 | 性别 |
| 61 | 民族 |
| 62 | 籍贯 |
| 63 | 省份 |
| 64 | 城市 |
| 65 | 区县 |
| 66 | 学校 |
| 67 | 班级 |
| 68 | 检查时间 |
| 69 | 眼别 |
| 70 | 裸眼视力 |
| 71 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 72 | 右眼 |
| 73 | 左眼 |
| 74 | 眼别 |
| 75 | 等效球镜度数(球镜+1/2柱镜) |
| 76 | 右眼 |
| 77 | 左眼 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `normalKeyword` |
| `transfer.adminId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right2` |
| `vision` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheckSecond.right2` |
| `item.schoolMateCheckSecond.left2` |
| `item.schoolMateCheck.right1` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheckSecond.right1` |
| `item.schoolMateCheckSecond.left1` |
| `item.schoolMateCheck.rightSe` |
| `item.schoolMateCheck.leftSe` |
| `item.schoolMateCheckSecond.rightSe` |
| `item.schoolMateCheckSecond.leftSe` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheckSecond.right15` |
| `item.schoolMateCheckSecond.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheckSecond.right14` |
| `item.schoolMateCheckSecond.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheckSecond.right13` |
| `item.schoolMateCheckSecond.left13` |
| `item.schoolMateCheck.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheckSecond.checkDate` |
| `getCheckVoFactory.vo.schoolMateCheck.classMateName` |
| `getCheckVoFactory.vo.schoolMateCheck.schoolMateCode` |
| `getCheckVoFactory.vo.schoolMateCheck.gender` |
| `gender` |
| `getCheckVoFactory.vo.schoolMate.nation` |
| `getCheckVoFactory.vo.schoolMate.nativePlace` |
| `getCheckVoFactory.vo.schoolAddress.province` |
| `getCheckVoFactory.vo.schoolAddress.city` |
| `getCheckVoFactory.vo.schoolAddress.district` |
| `getCheckVoFactory.vo.school.schoolName` |
| `getCheckVoFactory.vo.schoolClass.className` |
| `getCheckVoFactory.vo.schoolMateCheck.right1` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.right1Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.right2` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.right2Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.left1` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.left1Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.left2` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.left2Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.rightSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecond.rightSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.rightSeDiff` |
| `getCheckVoFactory.vo.schoolMateCheck.leftSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecond.leftSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.leftSeDiff` |
| `getCheckVoFactory.vo.schoolMateCheck.remark` |
| `item.schoolMateCheck.birthday` |
| `item.schoolMateCheck.gender` |
| `item.schoolMate.nation` |
| `item.schoolMate.nativePlace` |
| `item.schoolAddress.province` |
| `item.schoolAddress.city` |
| `item.schoolAddress.district` |
| `item.schoolMateCheckSecondDiffVo.right1Diff` |
| `item.schoolMateCheckSecondDiffVo.right2Diff` |
| `item.schoolMateCheckSecondDiffVo.left1Diff` |
| `item.schoolMateCheckSecondDiffVo.left2Diff` |
| `item.schoolMateCheckSecondDiffVo.rightSeDiff` |
| `item.schoolMateCheckSecondDiffVo.leftSeDiff` |
| `item.schoolMateCheck.remark` |
| `item.admin.nickname` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `printAll()` |
| `showReport(item.schoolMateCheck.id)` |
| `printSingle(item.schoolMateCheck.id)` |
| `hideModal()` |
| `setRole()` |

### 1.2 `addSchool`

- **URL**：`/addSchool`
- **模板**：`views/screenAdmin/addSchool.html`
- **控制器**：`addSchoolCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `insertAddress` | `POST /admin/insertAddress.json` |
| `insertSchool` | `POST /admin/insertSchool.json` |

**必填项**

| 标签 |
|---|
| * 学校名称 |
| * 学校类别 |
| * 关联门店 |
| * 省份 |
| * 城市 |
| * 区县 |
| * 片区 |
| * 监测点 |

**表单标签**

| 标签 |
|---|
| * 学校名称 |
| 学校编码 |
| * 学校类别 |
| * 关联门店 |
| * 省份 |
| * 城市 |
| * 区县 |
| * 片区 |
| * 监测点 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolName` |
| `obj.schoolCode` |
| `obj.schoolLevelId` |
| `address.province` |
| `address.city` |
| `address.district` |
| `erea.districtVal` |
| `erea.monitorVal` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hide()` |
| `addSchool()` |

**跳转到**：`schoolList`

**下拉数据源（ng-options）**

```
item.id as item.schoolLevelName for item in levelObjectFactory.result.list
item.name as item.name for item in citiesData
item.name as item.name for item in data
item.name as item.name for item in districtData
```

### 1.3 `addSchoolPlan`

- **URL**：`/addSchoolPlan`
- **模板**：`views/screenAdmin/addSchoolPlan.html`
- **控制器**：`addSchoolPlanCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createPromotionOfSchool` | `POST /admin/createPromotionOfSchool.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `insertSchoolPlan` | `POST /admin/insertSchoolPlan.json` |
| `insertSchoolPlanRoot` | `POST /admin/insertSchoolPlanRoot.json` |

**必填项**

| 标签 |
|---|
| 筛查计划名称 * |

**表单标签**

| 标签 |
|---|
| 筛查计划名称 * |
| 备注 |
| 设置成当前筛查计划 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `seletedYear` |
| `obj.planName` |
| `obj.remark` |
| `obj.setDefaultPlan` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `inyear.id` |
| `inyear.name` |
| `obj.planName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setSeason(1)` |
| `setSeason(3)` |
| `setSeason(2)` |
| `setSeason(4)` |
| `addPlan()` |

**跳转到**：`areaSchoolPlanList`, `schoolPlanList`

### 1.4 `addAreaSchoolPlan`

- **URL**：`/addAreaSchoolPlan`
- **模板**：`views/screenAdmin/addSchoolPlan.html`
- **控制器**：`addSchoolPlanCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createPromotionOfSchool` | `POST /admin/createPromotionOfSchool.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `insertSchoolPlan` | `POST /admin/insertSchoolPlan.json` |
| `insertSchoolPlanRoot` | `POST /admin/insertSchoolPlanRoot.json` |

**必填项**

| 标签 |
|---|
| 筛查计划名称 * |

**表单标签**

| 标签 |
|---|
| 筛查计划名称 * |
| 备注 |
| 设置成当前筛查计划 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `seletedYear` |
| `obj.planName` |
| `obj.remark` |
| `obj.setDefaultPlan` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `inyear.id` |
| `inyear.name` |
| `obj.planName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setSeason(1)` |
| `setSeason(3)` |
| `setSeason(2)` |
| `setSeason(4)` |
| `addPlan()` |

**跳转到**：`areaSchoolPlanList`, `schoolPlanList`

### 1.5 `addScreenPromotion`

- **URL**：`/addScreenPromotion?schoolId&classId`
- **模板**：`views/screenAdmin/addScreenPromotion.html`
- **控制器**：`addScreenPromotionCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： |
| * 活动日期： |
| * 学校： |
| * 班级： |
| * 社区： |

**表单标签**

| 标签 |
|---|
| * 活动名称： |
| * 活动日期： |
| 筛查类型： |
| 学校 |
| 社区 |
| * 学校： |
| * 班级： |
| * 社区： |
| 活动地址： |
| 活动说明： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `startTime` |
| `obj.checkType` |
| `modifySchoolName` |
| `classKeyword` |
| `homeName` |
| `obj.address` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `schoolitem.schoolName` |
| `classitem.className` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `modifySchool(schoolitem.id,schoolitem.schoolName)` |
| `chooseClass(classitem.className,classitem.id)` |
| `modifyHome(schoolitem.id,schoolitem.schoolName)` |
| `create()` |

**跳转到**：`schoolList`, `screenPromotionList`

### 1.6 `childVisionMesure`

- **URL**：`/childVisionMesure`
- **模板**：`views/screenAdmin/childVisionMesure.html`
- **控制器**：`visionMesureCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getEyeChartOfMine` | `POST /admin/getEyeChartOfMine.json` |
| `resetEyeChartOfMine` | `POST /admin/resetEyeChartOfMine.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `homeFactory.result.admin.mobile` |
| `getEyeChartFactory.result.object.eyeChart.testDistance` |
| `id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 1.7 `classList`

- **URL**：`/classList?schoolId`
- **模板**：`views/screenAdmin/classList.html`
- **控制器**：`classListCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `batchInsertSchoolClass` | `POST /admin/batchInsertSchoolClass.json` |
| `batchInsertSchoolClassByNames` | `POST /admin/batchInsertSchoolClassByNames.json` |
| `deleteSchoolClass` | `POST /admin/deleteSchoolClass.json` |
| `getInYearList` | `POST /admin/getInYearList.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `insertSchoolClass` | `POST /admin/insertSchoolClass.json` |
| `splitStringToArray` | `POST /admin/splitStringToArray.json` |
| `updateSchoolClass` | `POST /admin/updateSchoolClass.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 班级名称 |
| 2 | 入学年份 |
| 3 | 年级 |
| 4 | 班级 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `add.inYear` |
| `add.classNumber` |
| `add.className` |
| `data.inYear` |
| `data.classNumber` |
| `data.className` |
| `add.inYearFrom` |
| `add.inYearTo` |
| `add.classCount` |
| `customClass.info.inYear` |
| `brand.brandName` |
| `customClass.info.className` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSchoolObjectFactory.result.object.schoolName` |
| `schoolClassListFactory.count` |
| `item.className` |
| `item.inYear` |
| `item.classNumber` |
| `inyear.id` |
| `inyear.name` |
| `add.classCount` |
| `add.inYearTo` |
| `add.inYearFrom` |
| `mathToAbs` |
| `genereatClassName` |
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddSchool()` |
| `showMultiAddSchool()` |
| `customClass.open()` |
| `update(item.id)` |
| `delete(item.id)` |
| `screenModal()` |
| `addClass()` |
| `updateSchool()` |
| `addMultiClass()` |
| `customClass.close()` |
| `customClass.execute()` |
| `customClass.save()` |

**跳转到**：`schoolList`

### 1.8 `classReportInschool`

- **URL**：`/classReportInschool`
- **模板**：`views/screenAdmin/classReportInschool.html`
- **控制器**：`classReportInschoolCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getReportStatusOfSchoolAdmin` | `POST /admin/getReportStatusOfSchoolAdmin.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `printSchoolPromotionListVoList` | `POST /admin/printSchoolPromotionListVoList.json` |
| `saveSchoolCheckCodeType` | `POST /admin/saveSchoolCheckCodeType.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectMyAdminSchoolVoListOfSchoolPlan` | `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json` |
| `selectSchoolPlanListBySchool` | `POST /admin/selectSchoolPlanListBySchool.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.schoolName` |
| `obj.planName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `item.schoolPlan.planName` |
| `item.promotion.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.classVisionStatVo.schoolMateCount` |
| `item.classVisionStatVo.examinedSchoolMateCount` |
| `item.classVisionStatVo.visionNormalCount` |
| `item.classVisionStatVo.visionAlert1Count` |
| `item.classVisionStatVo.visionAlert2Count` |
| `item.classVisionStatVo.visionAlert3Count` |
| `item.classVisionStatVo.dioptersNormalCountNew` |
| `item.classVisionStatVo.dioptersAlert1CountNew` |
| `item.classVisionStatVo.dioptersAlert2CountNew` |
| `item.classVisionStatVo.dioptersAlert3CountNew` |
| `item.classVisionStatVo.dioptersAlertCount` |
| `item.classVisionStatVo.dioptersNormalCount` |
| `item.classVisionStatVo.visionNormalRate` |
| `toFixed` |
| `item.classVisionStatVo.visionAlert1Rate` |
| `item.classVisionStatVo.visionAlert2Rate` |
| `item.classVisionStatVo.visionAlert3Rate` |
| `item.classVisionStatVo.dioptersAlertRate` |
| `item.classVisionStatVo.dioptersNormalRate` |
| `iten.classMateName` |
| `iten.right1` |
| `vision` |
| `iten.right2` |
| `iten.left1` |
| `iten.left2` |
| `iten.right15` |
| `iten.right14` |
| `iten.right13` |
| `iten.left15` |
| `iten.left14` |
| `iten.left13` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectSchool()` |
| `showSelectPlan()` |
| `downloadModal=true` |
| `downloadModal=false` |

### 1.9 `cloudPrinterConfig`

- **URL**：`/cloudPrinterConfig`
- **模板**：`views/screenAdmin/cloudPrinterConfig.html`
- **控制器**：`cloudPrinterConfigCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 条形码 |
| 二维码 |
| 条形码和二维码同时打印 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.codeType` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `bigImgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `save()` |
| `imgModal=false` |
| `$event.stopPropagation()` |

**跳转到**：`screenBackConfig`, `screenPromotionConfig`, `smsSet`, `zhiShiBangConfig`

### 1.10 `cloudPrinterList`

- **URL**：`/cloudPrinterList`
- **模板**：`views/screenAdmin/cloudPrinterList.html`
- **控制器**：`cloudPrinterListCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addPrinter` | `POST /admin/addPrinter.json` |
| `cleanPrinterTask` | `POST /admin/cleanPrinterTask.json` |
| `deletePrinter` | `POST /admin/deletePrinter.json` |
| `getCloudPrinterVo` | `POST /admin/getCloudPrinterVo.json` |
| `selectCloudPrinterVoList` | `POST /admin/selectCloudPrinterVoList.json` |
| `testPrinter` | `POST /admin/testPrinter.json` |
| `updateCloudPrinterInfo` | `POST /admin/updateCloudPrinterInfo.json` |
| `updateCloudPrinterStatus` | `POST /admin/updateCloudPrinterStatus.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 打印机编号SN |
| 2 | 打印机名称 |
| 3 | 在线 返回打印机状态信息。共三种： 1、离线。 2、在线，工作状态正常。 3、在线，工作状态不正常。 备注：异常一般是无纸，离线的判断是打印机与服务器失去联系超过2分钟。 |
| 4 | 状态 |
| 5 | 待打印 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `item.deviceType` |
| `item.cloudPrinter.status` |
| `addPrint.serialNumber` |
| `addPrint.secretKey` |
| `addPrint.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.cloudPrinter.serialNumber` |
| `item.cloudPrinter.remark` |
| `item.printerInfo.data` |
| `item.orderInfo.data.waiting` |
| `wh.width` |
| `wh.height` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAdd()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchSupplierList()` |
| `showSet.openShow(item.cloudPrinter.id)` |
| `showModify(item.cloudPrinter.id,$index,item.cloudPrinter.remark)` |
| `clear(item.cloudPrinter.id,$index)` |
| `deleteDevice(item.cloudPrinter.id,$index)` |
| `addPrintDevice()` |
| `addDeviceModal=false` |
| `modifyDevice(modifyId,modifyIndex)` |
| `modifyDeviceModal=false` |
| `setChose($index)` |
| `test()` |
| `showSet.openShow(false)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
x.id as x.name for x in typeArr
```

### 1.11 `contrastReportByArea`

- **URL**：`/contrastReportByArea`
- **模板**：`views/screenAdmin/contrastReportByArea.html`
- **控制器**：`contrastReportByAreaCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatVisionOfManage` | `POST /admin/basicStatVisionOfManage.json` |
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 项目 |
| 2 | 人次 |
| 3 | 比率 |
| 4 | 人次 |
| 5 | 比率 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `object.planName` |
| `obj.schoolName` |
| `object.schoolName` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionObjectVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert3Count` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert3CountNew` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showPlan()` |
| `showSelectSchool()` |
| `clearAllSchool($event)` |
| `showSchool()` |
| `clearAllTwoSchool($event)` |

### 1.12 `contrastReportInschool`

- **URL**：`/contrastReportInschool`
- **模板**：`views/screenAdmin/contrastReportInschool.html`
- **控制器**：`contrastReportInschoolCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getReportStatusOfSchoolAdmin` | `POST /admin/getReportStatusOfSchoolAdmin.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectMyAdminSchoolVoListOfSchoolPlan` | `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json` |
| `selectSchoolPlanListBySchool` | `POST /admin/selectSchoolPlanListBySchool.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 统计分类 |
| 2 | 项目 |
| 3 | 人次 |
| 4 | 比率 |
| 5 | 人次 |
| 6 | 比率 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `object.inYear` |
| `obj.classId` |
| `object.classId` |
| `obj.gender` |
| `object.gender` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.schoolName` |
| `object.schoolName` |
| `obj.planName` |
| `object.planName` |
| `inyear` |
| `class.id` |
| `class.className` |
| `class.name` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionObjectVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert3Count` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlertCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlertCount` |
| `getPromotionVisionFactory.result.object.dioptersNormalCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersNormalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectSchool()` |
| `showSchool()` |
| `showSelectPlan()` |
| `showPlan()` |

### 1.13 `dataChart`

- **URL**：`/dataChart`
- **模板**：`views/screenAdmin/dataChart.html`
- **控制器**：`dataChartCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatVisionOfManage` | `POST /admin/basicStatVisionOfManage.json` |
| `basicStatVisionOfManageOfArea` | `POST /admin/basicStatVisionOfManageOfArea.json` |
| `basicStatVisionOfManageOfCheckYear` | `POST /admin/basicStatVisionOfManageOfCheckYear.json` |
| `basicStatVisionOfManageOfGender` | `POST /admin/basicStatVisionOfManageOfGender.json` |
| `basicStatVisionOfManageOfLast3Year` | `POST /admin/basicStatVisionOfManageOfLast3Year.json` |
| `basicStatVisionOfManageOfSchoolLevel` | `POST /admin/basicStatVisionOfManageOfSchoolLevel.json` |
| `getArea` | `POST /admin/getArea.json` |
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `mapDest.tab` |
| `teen.tab` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `getPromotionVisionFactory.result.object.examinedSchoolMateCount` |
| `today` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item` |
| `mapDest.tab` |
| `progressNumber` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `teen.tab` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |

### 1.14 `exportrec`

- **URL**：`/exportrec`
- **模板**：`views/screenAdmin/exportrec.html`
- **控制器**：`exportrecCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `range.range` |
| `obj.inYear` |
| `obj.classId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `item` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |
| `exportbtn()` |

### 1.15 `fundus`

- **URL**：`/fundus`
- **模板**：`views/screenAdmin/fundus.html`
- **控制器**：`fundusCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteFundusDevice` | `POST /admin/deleteFundusDevice.json` |
| `getFundusDevice` | `POST /admin/getFundusDevice.json` |
| `selectFundusDeviceList` | `POST /admin/selectFundusDeviceList.json` |
| `updateFundusDeviceStatus` | `POST /admin/updateFundusDeviceStatus.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 眼底相机序列号 |
| 2 | 眼底相机名称 |
| 3 | 状态 |
| 4 | 下载二维码 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.status` |
| `deviceInfo.serialNumber` |
| `deviceInfo.remark` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getFundusListFactory.count` |
| `item.serialNumber` |
| `item.remark` |
| `deviceModalOptions.type` |
| `deviceModalOptions.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAdd()` |
| `updateDevice(item,$index)` |
| `deleteDevice(item.id)` |
| `lookLog(item)` |
| `fundusDevice()` |
| `addDeviceModal=false` |

**跳转到**：`reportRecord`, `reportStatistic`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 1.16 `fundusLog`

- **URL**：`/fundusLog?fundusDeviceId`
- **模板**：`views/screenAdmin/fundusLog.html`
- **控制器**：`fundusLogCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectFundusCheckRecordDetialVoList` | `POST /admin/selectFundusCheckRecordDetialVoList.json` |

**表单标签**

| 标签 |
|---|
| 查看二进制 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 时间 |
| 2 | 用途 |
| 3 | 查看报告 |
| 4 | 状态 |
| 5 | 设备编号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `hex` |
| `obj.logKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.fundusCheckRecord.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.fundusCheckRecord.pdf` |
| `item.fundusCheckRecord.h5` |
| `item.fundusCheckRecord.status` |
| `filter_fundusLog` |
| `item.fundusDevice.serialNumber` |

**跳转到**：`fundus`

### 1.17 `healthScreenConfig`

- **URL**：`/healthScreenConfig`
- **模板**：`views/screenAdmin/healthScreenConfig.html`
- **控制器**：`healthScreenConfigCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBodyCheckVoList` | `POST /admin/getBodyCheckVoList.json` |
| `initBodyCheck` | `POST /admin/initBodyCheck.json` |
| `saveSchoolCheckConf` | `POST /admin/saveSchoolCheckConf.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.bodyCheck.checkName` |
| `iten.bodyCheckItem.itemName` |
| `iten.bodyCheckItem.itemUnitName` |
| `iten.bodyCheckItem.itemType` |
| `itemTypeStauts` |
| `iten.bodyCheckItem.defaultValue` |
| `iten.bodyCheckItem.id` |
| `iten.bodyCheckItem.defaultValueEnable` |

**页面动作（ng-click）**

| 动作 |
|---|
| `initBtn()` |
| `setBodyCheckItemPrintDisable(iten.bodyCheckItem,indexOut,$index)` |

### 1.18 `inspection`

- **URL**：`/inspection`
- **模板**：`views/screenAdmin/inspection.html`
- **控制器**：`inspectionCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolMateCheckVo` | `POST /admin/getSchoolMateCheckVo.json` |
| `getSchoolMateCheckVoListOfSecond` | `POST /admin/getSchoolMateCheckVoListOfSecond.json` |
| `getSecondCheckQualifyDataVo` | `POST /admin/getSecondCheckQualifyDataVo.json` |
| `saveSchoolCheckSecondCheckEnable` | `POST /admin/saveSchoolCheckSecondCheckEnable.json` |

**表单标签**

| 标签 |
|---|
| {{item.admin.nickname}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 身份证号 |
| 3 | 学校 |
| 4 | 班级 |
| 5 | 原测/复测 |
| 6 | 戴镜类型 |
| 7 | 戴镜视力(右\|左) |
| 8 | 祼眼视力(右\|左) |
| 9 | 等效球镜(右\|左) |
| 10 | 球镜(右\|左) |
| 11 | 柱镜(右\|左) |
| 12 | 轴位(右\|左) |
| 13 | 检查时间 |
| 14 | 操作 |
| 15 | 姓名 |
| 16 | 出生日期 |
| 17 | 身份证号 |
| 18 | 性别 |
| 19 | 民族 |
| 20 | 籍贯 |
| 21 | 省份 |
| 22 | 城市 |
| 23 | 区县 |
| 24 | 学校 |
| 25 | 班级 |
| 26 | 检查时间 |
| 27 | 眼别 |
| 28 | 裸眼视力 |
| 29 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 30 | 右眼 |
| 31 | 左眼 |
| 32 | 眼别 |
| 33 | 等效球镜度数(球镜+1/2柱镜) |
| 34 | 右眼 |
| 35 | 左眼 |
| 36 | 姓名 |
| 37 | 出生日期 |
| 38 | 身份证号 |
| 39 | 性别 |
| 40 | 民族 |
| 41 | 籍贯 |
| 42 | 省份 |
| 43 | 城市 |
| 44 | 区县 |
| 45 | 学校 |
| 46 | 班级 |
| 47 | 检查时间 |
| 48 | 眼别 |
| 49 | 裸眼视力 |
| 50 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 51 | 右眼 |
| 52 | 左眼 |
| 53 | 眼别 |
| 54 | 等效球镜度数(球镜+1/2柱镜) |
| 55 | 右眼 |
| 56 | 左眼 |
| 57 | 姓名 |
| 58 | 出生日期 |
| 59 | 身份证号 |
| 60 | 性别 |
| 61 | 民族 |
| 62 | 籍贯 |
| 63 | 省份 |
| 64 | 城市 |
| 65 | 区县 |
| 66 | 学校 |
| 67 | 班级 |
| 68 | 检查时间 |
| 69 | 眼别 |
| 70 | 裸眼视力 |
| 71 | 戴镜视力 请打勾选择（ 框架眼镜 隐形眼镜 夜戴角膜塑形镜 ） |
| 72 | 右眼 |
| 73 | 左眼 |
| 74 | 眼别 |
| 75 | 等效球镜度数(球镜+1/2柱镜) |
| 76 | 右眼 |
| 77 | 左眼 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `normalKeyword` |
| `transfer.adminId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `secondCheckEnable` |
| `obj.planName` |
| `obj.schoolName` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right2` |
| `vision` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheckSecond.right2` |
| `item.schoolMateCheckSecond.left2` |
| `item.schoolMateCheck.right1` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheckSecond.right1` |
| `item.schoolMateCheckSecond.left1` |
| `item.schoolMateCheck.rightSe` |
| `item.schoolMateCheck.leftSe` |
| `item.schoolMateCheckSecond.rightSe` |
| `item.schoolMateCheckSecond.leftSe` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheckSecond.right15` |
| `item.schoolMateCheckSecond.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheckSecond.right14` |
| `item.schoolMateCheckSecond.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheckSecond.right13` |
| `item.schoolMateCheckSecond.left13` |
| `item.schoolMateCheck.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheckSecond.checkDate` |
| `getCheckVoFactory.vo.schoolMateCheck.classMateName` |
| `getCheckVoFactory.vo.schoolMateCheck.schoolMateCode` |
| `getCheckVoFactory.vo.schoolMateCheck.gender` |
| `gender` |
| `getCheckVoFactory.vo.schoolMate.nation` |
| `getCheckVoFactory.vo.schoolMate.nativePlace` |
| `getCheckVoFactory.vo.schoolAddress.province` |
| `getCheckVoFactory.vo.schoolAddress.city` |
| `getCheckVoFactory.vo.schoolAddress.district` |
| `getCheckVoFactory.vo.school.schoolName` |
| `getCheckVoFactory.vo.schoolClass.className` |
| `getCheckVoFactory.vo.schoolMateCheck.right1` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.right1Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.right2` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.right2Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.left1` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.left1Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.left2` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.left2Diff` |
| `getCheckVoFactory.vo.schoolMateCheck.rightSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecond.rightSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.rightSeDiff` |
| `getCheckVoFactory.vo.schoolMateCheck.leftSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecond.leftSe` |
| `getCheckVoFactory.vo.schoolMateCheckSecondDiffVo.leftSeDiff` |
| `getCheckVoFactory.vo.schoolMateCheck.remark` |
| `item.schoolMateCheck.birthday` |
| `item.schoolMateCheck.gender` |
| `item.schoolMate.nation` |
| `item.schoolMate.nativePlace` |
| `item.schoolAddress.province` |
| `item.schoolAddress.city` |
| `item.schoolAddress.district` |
| `item.schoolMateCheckSecondDiffVo.right1Diff` |
| `item.schoolMateCheckSecondDiffVo.right2Diff` |
| `item.schoolMateCheckSecondDiffVo.left1Diff` |
| `item.schoolMateCheckSecondDiffVo.left2Diff` |
| `item.schoolMateCheckSecondDiffVo.rightSeDiff` |
| `item.schoolMateCheckSecondDiffVo.leftSeDiff` |
| `item.schoolMateCheck.remark` |
| `item.admin.nickname` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `saveSchoolCheckSecondCheckEnable()` |
| `showSelectPlan()` |
| `showSelectSchool()` |
| `printAll()` |
| `showReport(item.schoolMateCheck.id)` |
| `printSingle(item.schoolMateCheck.id)` |
| `hideModal()` |
| `setRole()` |

### 1.19 `markOriginSet`

- **URL**：`/markOriginSet`
- **模板**：`views/screenAdmin/markOriginSet.html`
- **控制器**：`markOriginSetCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addEmployeeSchedulingAndDetail` | `POST /admin/addEmployeeSchedulingAndDetail.json` |
| `addEmployeeSchedulingTempNumber` | `POST /admin/addEmployeeSchedulingTempNumber.json` |
| `copyLastWeek` | `POST /admin/copyLastWeek.json` |
| `delEmployeeSchedulingAndDetail` | `POST /admin/delEmployeeSchedulingAndDetail.json` |
| `getEmployeeSchedulingDetailTimeVo` | `POST /admin/getEmployeeSchedulingDetailTimeVo.json` |
| `getEmployeeSchedulingWeekVoOfCompany` | `POST /admin/getEmployeeSchedulingWeekVoOfCompany.json` |
| `selectEmployeeSchedulingDetailListOfCompany` | `POST /admin/selectEmployeeSchedulingDetailListOfCompany.json` |
| `selectEmployeeSchedulingDetailTimeVoList` | `POST /admin/selectEmployeeSchedulingDetailTimeVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 时间段 |
| 2 | {{msgObj.week[$index]}} {{item\|substr:5}} {{msgObj.appointList[$index].dailyNotData?'添加':'临时'}}号源 |
| 3 | 日期 |
| 4 | 上午 |
| 5 | 下午 |
| 6 | 夜间 |
| 7 | 已预约情况 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `customDate.startTime` |
| `addInfo.setTime.startTime` |
| `addInfo.setTime.endTime` |
| `deleteInfo.params.startTime` |
| `deleteInfo.params.endTime` |
| `editTableForChose.allStatus` |
| `item.isChose` |
| `date.intervalSource` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyInfo.companyName` |
| `customDate.startTime` |
| `substr` |
| `msgObj.week` |
| `index` |
| `item` |
| `msgObj.appointList` |
| `dailyNotData` |
| `item.name` |
| `item1` |
| `item.key` |
| `startTime` |
| `setDate` |
| `HM` |
| `endTime` |
| `totalCount` |
| `addInfo.enough` |
| `addInfo.nowDayTime` |
| `date.name` |
| `date.intervalNum` |
| `date.total` |
| `addInfo.totalSource` |
| `item.intervalStartTime` |
| `item.intervalEndTime` |
| `item.countTotalNumber` |
| `item.schedulingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.employeeSchedulingDetail1.startTime` |
| `item.employeeSchedulingDetail1.endTime` |
| `item.employeeSchedulingDetail1.totalCount` |
| `item.employeeSchedulingDetail5.startTime` |
| `item.employeeSchedulingDetail5.endTime` |
| `item.employeeSchedulingDetail5.totalCount` |
| `item.employeeSchedulingDetail9.startTime` |
| `item.employeeSchedulingDetail9.endTime` |
| `item.employeeSchedulingDetail9.totalCount` |
| `item.usedAppointNumbers1` |
| `item.usedAppointNumbers5` |
| `item.usedAppointNumbers9` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteInfo.popoutStatus(true)` |
| `copyLastWeek()` |
| `addInfo.popoutStatus(true)` |
| `openIncrementNumber(item)` |
| `deleteInfo.submitOne(item,item1)` |
| `openIncrementNumber(msgObj.weekList[$index],item.schedulingType)` |
| `open1()` |
| `open2()` |
| `incrementNumber(date,item,outIndex)` |
| `addPaiBan()` |
| `closePaiBan()` |
| `editTableForChose.choseAll()` |
| `editTableForChose.choseSingle()` |
| `deleteInfo.submit()` |
| `deleteInfo.popoutStatus(false)` |

**跳转到**：`reachStoreAppointDetails`, `screenInStore`

### 1.20 `mateCheckReportConfig`

- **URL**：`/mateCheckReportConfig?type`
- **模板**：`views/screenAdmin/mateCheckReportConfig.html`
- **控制器**：`mateCheckReportConfigCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `title` |
| `item.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `changeSet(item)` |

### 1.21 `mateCheckReportList`

- **URL**：`/mateCheckReportList`
- **模板**：`views/screenAdmin/mateCheckReportList.html`
- **控制器**：`schoolMateCheckReportsCtrl`
- **端点数**：0

### 1.22 `mateCheckReportListNew`

- **URL**：`/mateCheckReportListNew`
- **模板**：`views/screenAdmin/mateCheckReportListNew.html`
- **控制器**：`mateCheckReportListNewCtrl`
- **端点数**：0

### 1.23 `mateClassReport`

- **URL**：`/mateClassReport`
- **模板**：`views/screenAdmin/mateClassReport.html`
- **控制器**：`screenClassReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `printSchoolPromotionListVoList` | `POST /admin/printSchoolPromotionListVoList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `item.schoolPlan.planName` |
| `item.promotion.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.classVisionStatVo.schoolMateCount` |
| `item.classVisionStatVo.visionCheckedCount` |
| `item.classVisionStatVo.visionNormalCount` |
| `item.classVisionStatVo.visionAlert1Count` |
| `item.classVisionStatVo.visionAlert2Count` |
| `item.classVisionStatVo.visionAlert3Count` |
| `item.classVisionStatVo.dioptersNormalCountNew` |
| `item.classVisionStatVo.dioptersAlert1CountNew` |
| `item.classVisionStatVo.dioptersAlert2CountNew` |
| `item.classVisionStatVo.dioptersAlert3CountNew` |
| `item.classVisionStatVo.dioptersAlertCount` |
| `item.classVisionStatVo.dioptersNormalCount` |
| `item.classVisionStatVo.dioptersErrorAlertCount` |
| `item.classVisionStatVo.dioptersErrorNormalCount` |
| `item.classVisionStatVo.dioptersDiffAlertCount` |
| `item.classVisionStatVo.dioptersDiffNormalCount` |
| `item.classVisionStatVo.hyperopicReserveAlertCount` |
| `item.classVisionStatVo.hyperopicReserveNormalCount` |
| `item.classVisionStatVo.dioptersAlertRate` |
| `toFixed` |
| `item.classVisionStatVo.dioptersErrorAlertRate` |
| `percent` |
| `item.classVisionStatVo.dioptersErrorNormalRate` |
| `item.classVisionStatVo.dioptersDiffAlertRate` |
| `item.classVisionStatVo.dioptersDiffNormalRate` |
| `item.classVisionStatVo.hyperopicReserveAlertRate` |
| `item.classVisionStatVo.hyperopicReserveNormalRate` |
| `iten.classMateName` |
| `iten.right1` |
| `vision` |
| `iten.right2` |
| `iten.left1` |
| `iten.left2` |
| `iten.right15` |
| `iten.right14` |
| `iten.right13` |
| `iten.left15` |
| `iten.left14` |
| `iten.left13` |
| `obj.schoolPlanId` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool($event)` |
| `downloadModal=true` |
| `downloadModal=false` |

### 1.24 `mateContrastReport`

- **URL**：`/mateContrastReport`
- **模板**：`views/screenAdmin/mateContrastReport.html`
- **控制器**：`screenContrastReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 统计分类 |
| 2 | 项目 |
| 3 | 人次 |
| 4 | 比率 |
| 5 | 人次 |
| 6 | 比率 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolPoint` |
| `object.schoolPoint` |
| `obj.schoolLevelId` |
| `object.schoolLevelId` |
| `obj.inYear` |
| `object.inYear` |
| `obj.classId` |
| `object.classId` |
| `obj.gender` |
| `object.gender` |
| `obj.checkYear` |
| `object.checkYear` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `object.planName` |
| `erea` |
| `schoolCategory.schoolLevelName` |
| `obj.schoolName` |
| `object.schoolName` |
| `inyear` |
| `class.id` |
| `class.className` |
| `class.name` |
| `class.key` |
| `class.value` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.visionCheckedCount` |
| `getPromotionObjectVisionFactory.result.object.visionCheckedCount` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionObjectVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `getPromotionObjectVisionFactory.result.object.visionAlert3Count` |
| `getPromotionVisionFactory.result.object.dioptersCheckedCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersCheckedCount` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlert3CountNew` |
| `getPromotionVisionFactory.result.object.dioptersErrorNormalCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersErrorNormalCount` |
| `getPromotionVisionFactory.result.object.dioptersErrorAlertCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersErrorAlertCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersErrorAlertRate` |
| `percent` |
| `getPromotionVisionFactory.result.object.dioptersDiffNormalCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersDiffNormalCount` |
| `getPromotionVisionFactory.result.object.dioptersDiffAlertCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersDiffAlertCount` |
| `getPromotionVisionFactory.result.object.hyperopicReserveNormalCount` |
| `getPromotionObjectVisionFactory.result.object.hyperopicReserveNormalCount` |
| `getPromotionVisionFactory.result.object.hyperopicReserveAlertCount` |
| `getPromotionObjectVisionFactory.result.object.hyperopicReserveAlertCount` |
| `getPromotionVisionFactory.result.object.dioptersAlertCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersAlertCount` |
| `getPromotionVisionFactory.result.object.dioptersNormalCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersNormalCount` |
| `getPromotionVisionFactory.result.object.visionCorrectAlertCount` |
| `getPromotionObjectVisionFactory.result.object.visionCorrectAlertCount` |
| `getPromotionVisionFactory.result.object.visionCorrectAlert2Count` |
| `getPromotionObjectVisionFactory.result.object.visionCorrectAlert2Count` |
| `getPromotionVisionFactory.result.object.visionCorrectAlert1Count` |
| `getPromotionObjectVisionFactory.result.object.visionCorrectAlert1Count` |
| `getPromotionVisionFactory.result.object.visionCorrectAlert3Count` |
| `getPromotionObjectVisionFactory.result.object.visionCorrectAlert3Count` |
| `getPromotionVisionFactory.result.object.visionCorrectNormalCount` |
| `getPromotionObjectVisionFactory.result.object.visionCorrectNormalCount` |
| `schoolCategory` |
| `obj.schoolPlanId` |
| `schoolCategory2` |
| `object.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showPlan()` |
| `showSelectSchool()` |
| `clearAllSchool($event)` |
| `showSchool()` |
| `clearAllTwoSchool($event)` |
| `exportDefault()` |

### 1.25 `mateProgressReport`

- **URL**：`/mateProgressReport`
- **模板**：`views/screenAdmin/mateProgressReport.html`
- **控制器**：`mateProgressReportCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeSchoolPlanSchool` | `POST /admin/completeSchoolPlanSchool.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `selectVisionGroupList` | `POST /admin/selectVisionGroupList.json` |
| `statSchoolComplete` | `POST /admin/statSchoolComplete.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校名称 |
| 2 | 学生数量 |
| 3 | 已完成 |
| 4 | 未筛查 |
| 5 | 筛查进度 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `stateObjectFactory.result.object.schoolCount` |
| `stateObjectFactory.result.object.examinedSchoolCount` |
| `stateObjectFactory.result.object.examiningSchoolCount` |
| `stateObjectFactory.result.object.waitingExamineSchoolCount` |
| `item.school.schoolName` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `item.waitingExamineSchoolMateCount` |
| `item.examiningSchoolMateCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `confirm(item.school.id,$index)` |
| `checkBefore()` |
| `hideModal()` |

### 1.26 `mateRecordReport`

- **URL**：`/mateRecordReport`
- **模板**：`views/screenAdmin/mateRecordReport.html`
- **控制器**：`screenStudentReportCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolBodyCheckInfoListOfSchoolPlan` | `POST /admin/getSchoolBodyCheckInfoListOfSchoolPlan.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectBodyCheckVoByCode` | `POST /admin/selectBodyCheckVoByCode.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**表单标签**

| 标签 |
|---|
| 视力筛查 |
| 屈光筛查 |
| {{iten.checkName}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 性别 |
| 5 | 生日 |
| 6 | 联系电话 |
| 7 | 身份证号或学籍号 |
| 8 | 祼眼视力(右\|左) |
| 9 | 视力诊断(右\|左) |
| 10 | 戴镜视力(右\|左) |
| 11 | 戴镜类型 |
| 12 | 筛查性近视 |
| 13 | 视力矫正 |
| 14 | 常见眼科疾病 |
| 15 | 方案建议 |
| 16 | 备注 |
| 17 | 检查日期 |
| 18 | 操作 |
| 19 | 学校 |
| 20 | 班级 |
| 21 | 姓名 |
| 22 | 性别 |
| 23 | 生日 |
| 24 | 联系电话 |
| 25 | 身份证号或学籍号 |
| 26 | 球镜(右\|左) |
| 27 | 柱镜(右\|左) |
| 28 | 轴位(右\|左) |
| 29 | 屈光诊断(右\|左) |
| 30 | 视力矫正 |
| 31 | 眼压(右\|左) |
| 32 | 眼轴(右\|左) |
| 33 | 角膜曲率K1(右\|左) |
| 34 | 角膜曲率K2(右\|左) |
| 35 | 角膜曲率D1(右\|左) |
| 36 | 角膜曲率D2(右\|左) |
| 37 | 验光单照片 |
| 38 | 学校 |
| 39 | 班级 |
| 40 | 姓名 |
| 41 | 性别 |
| 42 | 生日 |
| 43 | 联系电话 |
| 44 | 身份证号或学籍号 |
| 45 | {{iten.bodyCheckItem.itemName}} ({{iten.bodyCheckItem.itemUnitName}}) (右\|左) |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `obj.keyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `iten.checkName` |
| `tab` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.visionCorrectStatus` |
| `visionCorrectStatus` |
| `item.schoolMateCheck.commonRemark` |
| `item.schoolMateCheck.left68` |
| `item.schoolMateCheck.remark` |
| `item.schoolMateCheck.checkDate` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheck.right265` |
| `quCheckResult` |
| `item.schoolMateCheck.right11` |
| `item.schoolMateCheck.left11` |
| `item.schoolMateCheck.right36` |
| `item.schoolMateCheck.left36` |
| `item.schoolMateCheck.right89` |
| `item.schoolMateCheck.left89` |
| `item.schoolMateCheck.right90` |
| `item.schoolMateCheck.left90` |
| `item.schoolMateCheck.right92` |
| `item.schoolMateCheck.left92` |
| `item.schoolMateCheck.right93` |
| `item.schoolMateCheck.left93` |
| `iten.bodyCheckItem.itemName` |
| `iten.bodyCheckItem.itemUnitName` |
| `val.bodyCheckItemValue` |
| `val.bodyCheckItemValueRight` |
| `val.bodyCheckItemValueLeft` |
| `obj.schoolPlanId` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |
| `imgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |
| `setMateVision(null)` |
| `setMateVision(0)` |
| `setMateVision(1)` |
| `setMateVision(2)` |
| `setMateVision(3)` |
| `setMateVision2(null)` |
| `setMateVision2(0)` |
| `setMateVision2(1)` |
| `setMateVision2(2)` |
| `setMateVision2(3)` |
| `setTab(1)` |
| `setTab(2,$event)` |
| `setCheckCode(iten.checkCode,3+$index)` |
| `showDaochu($event,3)` |
| `showDaochu($event,1)` |
| `showDaochu($event,2)` |
| `searchMateHistory(item.schoolMateCheck.schoolMateId)` |
| `showImg(item.schoolMateCheck.scaCheckFile)` |
| `downloadModal=false` |
| `daochu()` |
| `daochuBodycheck()` |
| `hideImgModal()` |

### 1.27 `mateSchoolReport`

- **URL**：`/mateSchoolReport`
- **模板**：`views/screenAdmin/mateSchoolReport.html`
- **控制器**：`screenSchoolReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |

### 1.28 `medicalConfig`

- **URL**：`/medicalConfig`
- **模板**：`views/screenAdmin/medicalConfig.html`
- **控制器**：`medicalConfigCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBodyCheck` | `POST /admin/getBodyCheck.json` |
| `getBodyCheckItem` | `POST /admin/getBodyCheckItem.json` |
| `getSchoolMateCheckPrintConf` | `POST /admin/getSchoolMateCheckPrintConf.json` |
| `setBodyCheckItemPrintDisable` | `POST /admin/setBodyCheckItemPrintDisable.json` |
| `setBodyCheckPrintDisable` | `POST /admin/setBodyCheckPrintDisable.json` |
| `updateSchoolMateCheckPrintConfImageUrl` | `POST /admin/updateSchoolMateCheckPrintConfImageUrl.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `rate.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setImageRateIndex(rate.imageRate)` |
| `exportConfigComp.open(false)` |
| `exportConfigComp.loadImg()` |

**跳转到**：`printStudentReport`, `screenRecordReport`

### 1.29 `modifyHealthScreen`

- **URL**：`/modifyHealthScreen?checkId&checkCode`
- **模板**：`views/screenAdmin/modifyHealthScreen.html`
- **控制器**：`modifyHealthScreenCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkSchoolBodyCheckInfoVersion` | `POST /admin/checkSchoolBodyCheckInfoVersion.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getSchoolBodyCheckInfo` | `POST /admin/getSchoolBodyCheckInfo.json` |
| `getSchoolBodyCheckPsychologyVo` | `POST /admin/getSchoolBodyCheckPsychologyVo.json` |
| `getSchoolMateCheckVo` | `POST /admin/getSchoolMateCheckVo.json` |
| `getSchoolMateCheckVoListWithSameCode` | `POST /admin/getSchoolMateCheckVoListWithSameCode.json` |
| `saveSchoolBodyCheckInfo` | `POST /admin/saveSchoolBodyCheckInfo.json` |
| `selectToothCheckTemplateVoList` | `POST /admin/selectToothCheckTemplateVoList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.bodyCheckItemValue` |
| `tagIdArray[innIndex]` |
| `item.bodyCheckItemValueRight` |
| `item.bodyCheckItemValueLeft` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.classMateName` |
| `obj.gender` |
| `gender` |
| `date` |
| `howoldMatecheck` |
| `obj.nation` |
| `obj.nativePlace` |
| `obj.customerMobile` |
| `keyword` |
| `classKeyword` |
| `iten.checkName` |
| `getCheckVoFactory.result.vo.schoolMateCheck.checkCode` |
| `questions.questionContent` |
| `questions.answerValue` |
| `TeethClass.toothQuestionTitle` |
| `tooth.name` |
| `t.toothQuestionListIndex` |
| `t.name` |
| `item.bodyCheckItemVo.bodyCheckItem.itemName` |
| `item.bodyCheckItemVo.bodyCheckItem.itemUnitName` |
| `item.bodyCheckItemValue` |
| `val.itemValue` |
| `schoolMateHistoryListFactory.items` |
| `schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.checkYear` |
| `item.schoolMateCheck.checkDate` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right64` |
| `item.schoolMateCheck.left64` |
| `checkInfoFactory.errmsg` |
| `singleParams.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePosition()` |
| `goback()` |
| `searchMateHistory()` |
| `getMedical(medicalRecordId,patientId)` |
| `goCheck(checkId)` |
| `clickTooth(tooth,outerIndex,$index)` |
| `cardOption.open()` |
| `showTagModal(item.bodyCheckItemValue,item.bodyCheckItemVo.bodyCheckItemValueList,outerIndex,$event)` |
| `$event.stopPropagation()` |
| `insertTag(outerIndex,1)` |
| `medical.idx=-1` |
| `showTagModal(item.bodyCheckItemValueRight,item.bodyCheckItemVo.bodyCheckItemValueList,outerIndex,$event,` |
| `insertTag(outerIndex,2)` |
| `showTagModal(item.bodyCheckItemValueLeft,item.bodyCheckItemVo.bodyCheckItemValueList,outerIndex,$event,` |
| `insertTag(outerIndex,3)` |
| `back()` |
| `saveInter()` |
| `hideSchoolMateHistory()` |
| `refresh(item.schoolMateCheck.id)` |
| `tongbu()` |
| `infoModal=false` |
| `singleParams.pageCallback()` |
| `toothQuestionPopout=false` |

**下拉数据源（ng-options）**

```
x.itemValue as x.itemValue for x in item.bodyCheckItemVo.bodyCheckItemValueList
```

### 1.30 `modifyMateCheck`

- **URL**：`/modifyMateCheck?checkId`
- **模板**：`views/screenAdmin/modifyMateCheck.html`
- **控制器**：`modifyMateCheckCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{val.checkItemValue}} |
| 上传图片 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 项目 |
| 3 | 检查结果 |
| 4 | 单位 |
| 5 | 参考值 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `iten.checkItemValue` |
| `tagIdArray[innIndex]` |
| `iten.medicalExamine.checkDescription` |
| `iten.medicalExamine.checkComment` |

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
| `customerInfoFactory.vo.customer.customerName` |
| `customerInfoFactory.vo.customer.linkMobile` |
| `item.medicalExamine.examineName` |
| `iten.medicalExamine.examineName` |
| `iten.medicalExamine.payedStatus` |
| `payedStatus` |
| `corpInfo.employeeTitle` |
| `iten.medicalExamine.createName` |
| `iten.medicalExamine.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `iten.medicalExamine.checkPersonName` |
| `index` |
| `iten.checkItemName` |
| `iten.checkItemEnglish` |
| `val.checkItemValue` |
| `iten.checkItemUnitName` |
| `iten.checkItemValueSample` |
| `item` |
| `iten.medicalExamine.id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `medical.idx=-1` |
| `back()` |
| `getMedical(medicalRecordId,patientId)` |
| `showHistory()` |
| `setMedicalExamineId(item.medicalExamine.id)` |
| `showTagModal(iten.checkItemValue,selectValueArr[$index],$index,$event)` |
| `$event.stopPropagation()` |
| `insertTag($index)` |
| `deleteItem($index)` |
| `showCheckModal()` |
| `bigImg(item)` |
| `deleteImg(outerIndex,innerIndex)` |
| `uploadimg($index,iten.medicalExamine.id)` |
| `saveCheck(iten.medicalExamine.checkDescription,iten.medicalExamine.checkComment,iten.medicalExamine.id,iten.getImgArray)` |

**跳转到**：`assistCheckList`

**下拉数据源（ng-options）**

```
x.checkItemValue as x.checkItemValue for x in selectValueArr[$index]
```

### 1.31 `modifySchoolMateCheck`

- **URL**：`/modifySchoolMateCheck?checkId`
- **模板**：`views/screenAdmin/modifySchoolMateCheck.html`
- **控制器**：`modifySchoolMateCheckCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeSchoolMateCheck` | `POST /admin/completeSchoolMateCheck.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolMateCheckVo` | `POST /admin/getSchoolMateCheckVo.json` |
| `getSchoolMateCheckVoListWithSameCode` | `POST /admin/getSchoolMateCheckVoListWithSameCode.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `saveSchoolMateCheck` | `POST /admin/saveSchoolMateCheck.json` |

**必填项**

| 标签 |
|---|
| 框架眼镜 隐形眼镜 夜戴角膜塑形镜 视力正常 轻度不良 中度不良 重度不良 {{obj.left1 \| vision}} 请选择 {{obj.left2 \| vision}} 请选择 框架眼镜 隐形眼镜 夜戴角膜塑形镜 视力正常 轻度不良 中度不良 重度不良 屈光筛查 屈光筛查 球镜 * 柱镜 * 轴位 近视分级 非近视：等效球镜>+0.75D 近视前期：-0.50D&lt;等效球镜≤+0.75D（近视50度以下） 低度近视：-6.00D&lt;等效球镜≤-0.50D（近视50~600度之间） 高度近视： 等效球镜≤-6.00D（近视600度以上） 球镜 * 柱镜 * 轴位 近视分级 非近视：等效球镜>+0.75D 近视前期：-0.50D&lt;等效球镜≤+0.75D（近视50度以下） 低度近视：-6.00D&lt;等效球镜≤-0.50D（近视50~600度之间） 高度近视： 等效球镜≤-6.00D（近视600度以上） 非近视 近视前期 低度近视 高度近视 非近视 近视前期 低度近视 高度近视 筛查性近视 矫正情况 可疑远视储备量不足 屈光不正 屈光参差 筛查性近视 矫正情况 可疑远视储备量不足 屈光不正 屈光参差 是 否 无需矫正 未矫正 已矫正 欠矫正 是 否 是 否 是 否 是 否 无需矫正 未矫正 已矫正 欠矫正 是 否 是 否 是 否 其他筛查 其他筛查 眼压 眼轴 眼压 眼轴 角膜曲率K1 角膜曲率K2 角膜曲率D1 角膜曲率D2 角膜曲率K1 角膜曲率K2 角膜曲率D1 角膜曲率D2 方案建议 {{item}} |

**表单标签**

| 标签 |
|---|
| {{item}} |
| 视力正常 轻度不良 中度不良 重度不良 {{item}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.checkDate` |
| `keyword` |
| `obj.schoolMateCode` |
| `teacherKeyword` |
| `obj.customerMobile` |
| `obj.classMateName` |
| `obj.birthday` |
| `obj.gender` |
| `obj.nation` |
| `obj.nativePlace` |
| `obj.homeAddress` |
| `obj.right1` |
| `obj.right2` |
| `obj.left87` |
| `obj.right167` |
| `obj.left1` |
| `obj.left2` |
| `obj.left167` |
| `obj.right15` |
| `obj.right14` |
| `obj.right13` |
| `obj.right265` |
| `obj.left15` |
| `obj.left14` |
| `obj.left13` |
| `obj.left265` |
| `obj.right165` |
| `obj.visionCorrectStatus1` |
| `obj.right96` |
| `obj.right94` |
| `obj.right95` |
| `obj.left165` |
| `obj.visionCorrectStatus2` |
| `obj.left96` |
| `obj.left94` |
| `obj.left95` |
| `obj.right11` |
| `obj.right36` |
| `obj.left11` |
| `obj.left36` |
| `obj.right89` |
| `obj.right90` |
| `obj.right92` |
| `obj.right93` |
| `obj.left89` |
| `obj.left90` |
| `obj.left92` |
| `obj.left93` |
| `newadvise[$index]` |
| `obj.remark` |
| `newadvise` |
| `commonRemark` |
| `newright` |
| `newleft` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.classMateName` |
| `obj.gender` |
| `gender` |
| `date` |
| `howoldMatecheck` |
| `obj.nation` |
| `obj.nativePlace` |
| `obj.customerMobile` |
| `keyword` |
| `classKeyword` |
| `getCheckVoFactory.result.vo.schoolMateCheck.outRecordId` |
| `iten.checkName` |
| `getCheckVoFactory.result.vo.schoolMateCheck.checkCode` |
| `schoolitem.schoolName` |
| `teacheritem.schoolTeacher.teacherName` |
| `obj.right1` |
| `vision` |
| `obj.right2` |
| `obj.left1` |
| `obj.left2` |
| `item` |
| `advise` |
| `advanceVirus` |
| `advice` |
| `schoolMateHistoryListFactory.items` |
| `schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.checkYear` |
| `addAge` |
| `item.schoolMateCheck.checkDate` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.right1` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right64` |
| `item.schoolMateCheck.left64` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goback()` |
| `searchMateHistory()` |
| `getMedical(medicalRecordId,patientId)` |
| `open2()` |
| `chooseSchool(schoolitem.id,schoolitem.schoolName)` |
| `chooseTeacher(teacheritem.schoolTeacher.id,teacheritem.schoolTeacher.teacherName)` |
| `open1()` |
| `toggleInfo()` |
| `toggleElse()` |
| `modify()` |
| `back()` |
| `completeCheck()` |
| `hideSchoolMateHistory()` |
| `refresh(item.schoolMateCheck.id)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x  in sightArr
x.id as x.name for x in  gender
x.id as x.name for x in sightArr
```

### 1.32 `modifySchoolPlan`

- **URL**：`/modifySchoolPlan?schoolPlanId`
- **模板**：`views/screenAdmin/modifySchoolPlan.html`
- **控制器**：`modifySchoolPlanCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getPromotionVo` | `POST /admin/getPromotionVo.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolPlan` | `POST /admin/getSchoolPlan.json` |
| `getSchoolPlanRoot` | `POST /admin/getSchoolPlanRoot.json` |
| `getSchoolTeacher` | `POST /admin/getSchoolTeacher.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `syncSchoolInfoOfPromotion` | `POST /admin/syncSchoolInfoOfPromotion.json` |
| `updatePromotionOfSchool` | `POST /admin/updatePromotionOfSchool.json` |
| `updateSchoolPlan` | `POST /admin/updateSchoolPlan.json` |
| `updateSchoolPlanRoot` | `POST /admin/updateSchoolPlanRoot.json` |

**必填项**

| 标签 |
|---|
| 筛查计划名称 * |

**表单标签**

| 标签 |
|---|
| 筛查计划名称 * |
| 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.year` |
| `obj.planName` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `inyear.id` |
| `inyear.name` |
| `obj.planName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setSeason(1)` |
| `setSeason(3)` |
| `setSeason(2)` |
| `setSeason(4)` |
| `addPlan()` |

**跳转到**：`areaSchoolPlanList`, `schoolPlanList`

### 1.33 `modifyAreaSchoolPlan`

- **URL**：`/modifyAreaSchoolPlan?schoolPlanId`
- **模板**：`views/screenAdmin/modifySchoolPlan.html`
- **控制器**：`modifySchoolPlanCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getPromotionVo` | `POST /admin/getPromotionVo.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolPlan` | `POST /admin/getSchoolPlan.json` |
| `getSchoolPlanRoot` | `POST /admin/getSchoolPlanRoot.json` |
| `getSchoolTeacher` | `POST /admin/getSchoolTeacher.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `syncSchoolInfoOfPromotion` | `POST /admin/syncSchoolInfoOfPromotion.json` |
| `updatePromotionOfSchool` | `POST /admin/updatePromotionOfSchool.json` |
| `updateSchoolPlan` | `POST /admin/updateSchoolPlan.json` |
| `updateSchoolPlanRoot` | `POST /admin/updateSchoolPlanRoot.json` |

**必填项**

| 标签 |
|---|
| 筛查计划名称 * |

**表单标签**

| 标签 |
|---|
| 筛查计划名称 * |
| 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.year` |
| `obj.planName` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `inyear.id` |
| `inyear.name` |
| `obj.planName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setSeason(1)` |
| `setSeason(3)` |
| `setSeason(2)` |
| `setSeason(4)` |
| `addPlan()` |

**跳转到**：`areaSchoolPlanList`, `schoolPlanList`

### 1.34 `modifyScreenPromotion`

- **URL**：`/modifyScreenPromotion?promotionId&schoolPlanId`
- **模板**：`views/screenAdmin/modifyScreenPromotion.html`
- **控制器**：`modifyScreenPromotionCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： * 活动日期： 学校筛查 社区筛查 |

**表单标签**

| 标签 |
|---|
| * 活动名称： * 活动日期： 学校筛查 社区筛查 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `startTime` |
| `modifySchoolName` |
| `classKeyword` |
| `homeName` |
| `obj.address` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `schoolitem.schoolName` |
| `classitem.className` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `modifySchool(schoolitem.id,schoolitem.schoolName)` |
| `chooseClass(classitem.className,classitem.id)` |
| `modifyHome(schoolitem.id,schoolitem.schoolName)` |
| `modify()` |

**跳转到**：`schoolList`, `screenPromotionList`

### 1.35 `multiImportStudent`

- **URL**：`/multiImportStudent`
- **模板**：`views/screenAdmin/multiImportStudent.html`
- **控制器**：`multiImportStudentCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitBatchSchoolMateTask` | `POST /admin/commitBatchSchoolMateTask.json` |
| `createBatchSchoolMateTask` | `POST /admin/createBatchSchoolMateTask.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `selectBodyCheckItemListOfCorp` | `POST /admin/selectBodyCheckItemListOfCorp.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `selectSchoolPromotionListVoList` | `POST /admin/selectSchoolPromotionListVoList.json` |
| `selectTaskItemList` | `POST /admin/selectTaskItemList.json` |
| `startSchoolPlanSchool` | `POST /admin/startSchoolPlanSchool.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 班级 |
| 2 | 姓名 |
| 3 | 性别 |
| 4 | 手机号 |
| 5 | 学号/身份证号 |
| 6 | 出生日期 |
| 7 | 民族 |
| 8 | 籍贯 |
| 9 | 家庭住址 |
| 10 | 右眼-裸眼视力 |
| 11 | 戴镜视力 |
| 12 | 球镜(S) |
| 13 | 柱镜(C) |
| 14 | 轴位(A) |
| 15 | 左眼-裸眼视力 |
| 16 | 戴镜视力 |
| 17 | 球镜(S) |
| 18 | 柱镜(C) |
| 19 | 轴位(A) |
| 20 | 戴镜类型 |
| 21 | 备注 |
| 22 | {{item.itemName }}{{!item.itemUnitName?"":"("+item.itemUnitName+")"}}{{item.single==1?"":"(右\|左)"}} |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDefaultObjectFactory.result.object.planName` |
| `obj.schoolName` |
| `iten.schoolClass.className` |
| `iten.schoolMateCount` |
| `classmateName` |
| `val.schoolMateCheck.classMateName` |
| `data.filepath` |
| `obj.schoolPlanId` |
| `obj.schoolId` |
| `createTaskFactory.result.object.msg` |
| `taskListFactory.count` |
| `item.itemName` |
| `item.itemUnitName` |
| `item.single` |
| `item.className` |
| `item.name` |
| `item.gender` |
| `gender` |
| `item.mobile` |
| `item.idCard` |
| `item.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.nation` |
| `item.nativePlace` |
| `item.homeAddress` |
| `item.right1` |
| `vision` |
| `item.right2` |
| `item.right15` |
| `item.right14` |
| `item.right13` |
| `item.left1` |
| `item.left2` |
| `item.left15` |
| `item.left14` |
| `item.left13` |
| `item.left87` |
| `item.remark` |
| `item.newBody` |
| `body.itemCode` |
| `bodyCorpList.length` |
| `item.error` |
| `item.line` |
| `toFixed` |

**页面动作（ng-click）**

| 动作 |
|---|
| `switchTab(1)` |
| `switchTab(2)` |
| `downLoad(` |
| `addSchool()` |
| `showSelectSchool()` |
| `searchMateName(iten.promotion.id,iten.schoolClass.className)` |
| `$event.stopPropagation()` |
| `addClass()` |
| `showAll()` |
| `hideAll()` |
| `modify()` |

**跳转到**：`screenPromotionStudent`

### 1.36 `physicalContrastReport`

- **URL**：`/physicalContrastReport`
- **模板**：`views/screenAdmin/physicalContrastReport.html`
- **控制器**：`physicalContrastReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 统计分类 |
| 2 | 项目 |
| 3 | 数据 |
| 4 | 比率 |
| 5 | 数据 |
| 6 | 比率 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolPoint` |
| `object.schoolPoint` |
| `obj.schoolLevelId` |
| `object.schoolLevelId` |
| `obj.inYear` |
| `object.inYear` |
| `obj.classId` |
| `object.classId` |
| `obj.gender` |
| `object.gender` |
| `obj.checkYear` |
| `object.checkYear` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `object.planName` |
| `erea` |
| `schoolCategory.schoolLevelName` |
| `obj.schoolName` |
| `object.schoolName` |
| `inyear` |
| `class.id` |
| `class.className` |
| `class.name` |
| `class.key` |
| `class.value` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionVisionFactory.result.object.avgHeight` |
| `getPromotionObjectVisionFactory.result.object.avgHeight` |
| `getPromotionVisionFactory.result.object.avgWeight` |
| `getPromotionObjectVisionFactory.result.object.avgWeight` |
| `getPromotionVisionFactory.result.object.avgBust` |
| `getPromotionObjectVisionFactory.result.object.avgBust` |
| `getPromotionVisionFactory.result.object.avgCapacity` |
| `getPromotionObjectVisionFactory.result.object.avgCapacity` |
| `physical.rowSpan` |
| `physical.rowName` |
| `physical.colName` |
| `getPromotionVisionFactory.result.object` |
| `physical.td1` |
| `physical.tdComment` |
| `getPromotionObjectVisionFactory.result.object` |
| `schoolCategory` |
| `obj.schoolPlanId` |
| `schoolCategory2` |
| `object.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showPlan()` |
| `showSelectSchool()` |
| `clearAllSchool($event)` |
| `showSchool()` |
| `clearAllTwoSchool($event)` |

### 1.37 `physicalReport`

- **URL**：`/physicalReport`
- **模板**：`views/screenAdmin/physicalReport.html`
- **控制器**：`physicalReportCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|

### 1.38 `pos`

- **URL**：`/pos`
- **模板**：`views/screenAdmin/pos.html`
- **控制器**：`posCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deletePosDevice` | `POST /admin/deletePosDevice.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getPosDevice` | `POST /admin/getPosDevice.json` |
| `selectPosDeviceList` | `POST /admin/selectPosDeviceList.json` |
| `updatePosDeviceStatus` | `POST /admin/updatePosDeviceStatus.json` |
| `getMyAdminCorpList` | `POST /auth/getMyAdminCorpList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | POS机序列号 |
| 2 | POS机名称 |
| 3 | 所属收银台 |
| 4 | 状态 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.posDevice.status` |
| `deviceInfo.posDeviceSn` |
| `deviceInfo.remark` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPosListFactory.count` |
| `item.posDevice.posDeviceSn` |
| `item.posDevice.remark` |
| `item.company.companyName` |
| `deviceModalOptions.type` |
| `deviceModalOptions.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAdd()` |
| `updateDevice(item,$index)` |
| `deleteDevice(item.posDevice.id)` |
| `posDevice()` |
| `addDeviceModal=false` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 1.39 `printStudentReport`

- **URL**：`/printStudentReport`
- **模板**：`views/screenAdmin/printStudentReport.html`
- **控制器**：`printStudentReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `countStatSchoolMateCheckIdList` | `POST /admin/countStatSchoolMateCheckIdList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCondition.preview` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showExport($event,1)` |
| `showExport($event,3)` |
| `showExport($event,2)` |
| `getCondition.preview=!getCondition.preview` |

**跳转到**：`medicalConfig`, `screenRecordReport`

### 1.40 `progressReport`

- **URL**：`/progressReport`
- **模板**：`views/screenAdmin/progressReport.html`
- **控制器**：`progressReportCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |
| `selectVisionGroupManageList` | `POST /admin/selectVisionGroupManageList.json` |
| `statSchoolCompleteGroupManage` | `POST /admin/statSchoolCompleteGroupManage.json` |
| `statSchoolCompleteManage` | `POST /admin/statSchoolCompleteManage.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校名称 |
| 2 | 学生数量 |
| 3 | 已完成 |
| 4 | 未筛查 |
| 5 | 筛查进度 |
| 6 | 操作 |
| 7 | 筛查范围 |
| 8 | 学校数量 |
| 9 | 已完成 |
| 10 | 筛查中 |
| 11 | 未开始 |
| 12 | 未完成 |
| 13 | 筛查进度 |
| 14 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `stateObjectFactory.result.object.schoolCount` |
| `stateObjectFactory.result.object.examinedSchoolCount` |
| `stateObjectFactory.result.object.examiningSchoolCount` |
| `stateObjectFactory.result.object.waitingExamineSchoolCount` |
| `item.school.schoolName` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `item.waitingExamineSchoolMateCount` |
| `item.examiningSchoolMateCount` |
| `item.area.name` |
| `item.schoolCount` |
| `item.examinedSchoolCount` |
| `item.examiningSchoolCount` |
| `item.waitingExamineSchoolCount` |
| `toFixed` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `viewCity(item.area.id)` |
| `viewDistrict(item.area.id)` |
| `viewSchool(item.area.id)` |

### 1.41 `projectionScreen`

- **URL**：`/projectionScreen`
- **模板**：`views/screenAdmin/projectionScreen.html`
- **控制器**：`projectionScreenCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `autoChartSizeForPad` | `POST /admin/autoChartSizeForPad.json` |
| `getEyeChartOfMine` | `POST /admin/getEyeChartOfMine.json` |
| `getEyeChartPicVoForPad` | `POST /admin/getEyeChartPicVoForPad.json` |
| `getRandFirstEyeChartFileByChartType` | `POST /admin/getRandFirstEyeChartFileByChartType.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `resetEyeChartOfMine` | `POST /admin/resetEyeChartOfMine.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `homeFactory.result.admin.mobile` |
| `getEyeChartFactory.result.object.eyeChart.testDistance` |
| `default_picture` |
| `title` |
| `pic` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 1.42 `reachStoreAppointAllReport`

- **URL**：`/reachStoreAppointAllReport`
- **模板**：`views/screenAdmin/reachStoreAppointAllReport.html`
- **控制器**：`reachStoreAppointAllReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `statAppointSchoolMateOfCorp` | `POST /admin/statAppointSchoolMateOfCorp.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.statObjectName` |
| `item.statChildrenName` |
| `item.appointNumberCount` |
| `item.arrivalNumberCount` |
| `item.appointOfArrivalRate` |
| `toFixed` |
| `li.statObjectName` |
| `li.appointNumberCount` |
| `li.arrivalNumberCount` |
| `li.appointOfArrivalRate` |

**页面动作（ng-click）**

| 动作 |
|---|
| `exportDefault()` |

**跳转到**：`markOriginSet`, `reachStoreAppointAllReport`, `reachStoreAppointDetails`, `reachStoreAppointSingleReport`, `screenInStore`, `transformationRate`

### 1.43 `reachStoreAppointDetails`

- **URL**：`/reachStoreAppointDetails`
- **模板**：`views/screenAdmin/reachStoreAppointDetails.html`
- **控制器**：`reachStoreAppointDetailsCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatAppointSchoolMate` | `POST /admin/basicStatAppointSchoolMate.json` |
| `cancelAppointOfPatient` | `POST /admin/cancelAppointOfPatient.json` |
| `getAppointSchoolMateVo` | `POST /admin/getAppointSchoolMateVo.json` |
| `selectAppointSchoolMateVoList` | `POST /admin/selectAppointSchoolMateVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 身份证号或学籍号 |
| 5 | 联系电话 |
| 6 | 预约门店 |
| 7 | 预约时间 |
| 8 | 创建时间 |
| 9 | 状态 |
| 10 | 备注 |
| 11 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.endTime` |
| `dateSearch` |
| `obj.pageSize` |
| `obj.keyword` |
| `cancelPopout.result.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.schoolMateVo.school.schoolName` |
| `item.schoolMateVo.schoolClass.className` |
| `item.schoolMateVo.schoolMate.classMateName` |
| `item.schoolMateVo.schoolMate.schoolMateCode` |
| `item.schoolMateVo.schoolMate.customerMobile` |
| `item.company.companyName` |
| `item.appoint.appointDay` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.appoint.appointStartTime` |
| `HH` |
| `mm` |
| `item.appoint.appointEndTime` |
| `item.appoint.appointCode` |
| `item.appoint.gmtCreate` |
| `ss` |
| `item.appoint` |
| `filterAppointStatus` |
| `singleStudent.schoolMateVo.schoolMate.classMateName` |
| `singleStudent.schoolMateVo.school.schoolName` |
| `singleStudent.schoolMateVo.schoolClass.className` |
| `singleStudent.appoint.appointDay` |
| `singleStudent.appoint.appointStartTime` |
| `singleStudent.appoint.appointEndTime` |
| `singleStudent.appoint.appointCode` |
| `singleStudent.appoint` |
| `singleStudent.appoint.cancelReason` |
| `cancelPopout.params.schoolMateVo.schoolMate.classMateName` |
| `cancelPopout.params.appoint.appointDay` |
| `cancelPopout.params.appoint.appointStartTime` |
| `cancelPopout.params.appoint.appointEndTime` |
| `cancelPopout.params.appoint.appointCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `searchByDate($event,` |
| `searchByDate($event,null)` |
| `showDaochu($event)` |
| `newAppoint()` |
| `addOneStudent(item,$index)` |
| `toAddCheckin(item)` |
| `lookInfo(item)` |
| `lookInfo(false)` |
| `cancelConfirm()` |
| `opCancelPopout(false)` |

**跳转到**：`markOriginSet`, `reachStoreAppointAllReport`, `reachStoreAppointDetails`, `reachStoreAppointSingleReport`, `screenInStore`, `transformationRate`

### 1.44 `reachStoreAppointSingleReport`

- **URL**：`/reachStoreAppointSingleReport`
- **模板**：`views/screenAdmin/reachStoreAppointSingleReport.html`
- **控制器**：`reachStoreAppointSingleReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `statAppointSchoolMateOfCompany` | `POST /admin/statAppointSchoolMateOfCompany.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.endTime` |
| `dateSearch` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.statObjectName` |
| `item.statChildrenName` |
| `item.appointNumberCount` |
| `item.arrivalNumberCount` |
| `item.appointOfArrivalRate` |
| `toFixed` |
| `li.statObjectName` |
| `li.appointNumberCount` |
| `li.arrivalNumberCount` |
| `li.appointOfArrivalRate` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `searchByDate($event,` |
| `searchByDate($event,null)` |
| `exportDefault()` |

**跳转到**：`markOriginSet`, `reachStoreAppointAllReport`, `reachStoreAppointDetails`, `reachStoreAppointSingleReport`, `screenInStore`, `transformationRate`

### 1.45 `reportRecord`

- **URL**：`/reportRecord`
- **模板**：`views/screenAdmin/reportRecord.html`
- **控制器**：`reportRecordCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectFundusCheckRecordDetialVoList` | `POST /admin/selectFundusCheckRecordDetialVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 检查单号 |
| 2 | 检查日期 |
| 3 | 姓名 |
| 4 | 联系方式 |
| 5 | 性别 |
| 6 | 年龄 |
| 7 | 身高 |
| 8 | 体重 |
| 9 | 屈光度(左) |
| 10 | 屈光度(右) |
| 11 | 病史 |
| 12 | 状态 |
| 13 | 检查设备 |
| 14 | 眼底报告 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTime` |
| `obj.personKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.fundusDevice.medicalRecordNo` |
| `item.fundusCheckRecord.medicalRecordNo` |
| `item.fundusCheckRecord.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.fundusCheckRecord.name` |
| `item.fundusCheckRecord.phone` |
| `item.fundusCheckRecord.gender` |
| `gender` |
| `item.fundusCheckRecord.age` |
| `item.fundusCheckRecord.height` |
| `item.fundusCheckRecord.weight` |
| `item.fundusCheckRecord.osDiopter` |
| `fundusDiopter` |
| `item.fundusCheckRecord.odDiopter` |
| `item.fundusCheckRecord.medicalHistory` |
| `fundusMedicalHistory` |
| `item.fundusCheckRecord.status` |
| `filter_fundusLog` |
| `item.fundusDevice.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `lookLog(item)` |

**跳转到**：`fundus`, `reportStatistic`

### 1.46 `reportStatistic`

- **URL**：`/reportStatistic`
- **模板**：`views/screenAdmin/reportStatistic.html`
- **控制器**：`reportStatisticCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteSchool` | `POST /admin/deleteSchool.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolMateCheckVo` | `POST /admin/getSchoolMateCheckVo.json` |
| `getSchoolMateCheckVoList` | `POST /admin/getSchoolMateCheckVoList.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `getSchoolVoList` | `POST /admin/getSchoolVoList.json` |
| `insertSchoolMateCheck` | `POST /admin/insertSchoolMateCheck.json` |
| `selectFundusCheckReportVo` | `POST /admin/selectFundusCheckReportVo.json` |
| `sendSmsToSchoolMateCheck` | `POST /admin/sendSmsToSchoolMateCheck.json` |
| `updateSchoolMateCheck` | `POST /admin/updateSchoolMateCheck.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 眼底相机序列号 |
| 2 | 眼底相机名称 |
| 3 | 已完成 |
| 4 | 测试中 |
| 5 | 待测试 |
| 6 | 图片异常 |
| 7 | 合计 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `deviceInfo.serialNumber` |
| `deviceInfo.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.deviceSerialNumber` |
| `item.deviceName` |
| `item.endCheckCount` |
| `item.onCheckCount` |
| `item.waitingCheckCount` |
| `item.imageErrorCheckCount` |
| `item.totalCount` |
| `getReportStatistic.totalCount.endCheckCount` |
| `getReportStatistic.totalCount.onCheckCount` |
| `getReportStatistic.totalCount.waitingCheckCount` |
| `getReportStatistic.totalCount.imageErrorCheckCount` |
| `getReportStatistic.totalCount.totalCount` |
| `deviceModalOptions.type` |
| `deviceModalOptions.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `fundusDevice()` |
| `addDeviceModal=false` |

**跳转到**：`fundus`, `reportRecord`

### 1.47 `schoolList`

- **URL**：`/schoolList`
- **模板**：`views/screenAdmin/schoolList.html`
- **控制器**：`schoolListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校编码 |
| 2 | 学校名称 |
| 3 | 类别 |
| 4 | 省份 |
| 5 | 城市 |
| 6 | 区/县 |
| 7 | 乡/镇/街道 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `screenDate.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.school.schoolCode` |
| `item.school.schoolName` |
| `item.schoolLevel.schoolLevelName` |
| `item.address.province` |
| `item.address.city` |
| `item.address.district` |
| `item.address.street` |
| `item.classCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteSchool(item.school.id)` |
| `screenModal()` |

**跳转到**：`addSchool`, `schoolList`, `townList`

### 1.48 `schoolMateCheckList`

- **URL**：`/schoolMateCheckList?promotionId&schoolPlanId`
- **模板**：`views/screenAdmin/schoolMateCheckList.html`
- **控制器**：`schoolMateCheckListCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `vo.keyword` |
| `isAll` |
| `schoolMateCheckClass.allStatus` |
| `item.isChose` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.schoolMateCheck.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck` |
| `howoldMatecheck` |
| `item.schoolMateCheck.customerMobile` |
| `item.mateCheckSmsLog.gmtCreate` |
| `item.mateCheckSmsLog.smsContent` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.right64` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.left64` |
| `item.schoolMateCheck.left68` |
| `item.schoolMateCheck.active` |
| `wechat` |

**页面动作（ng-click）**

| 动作 |
|---|
| `daochu()` |
| `checkAll()` |
| `schoolMateCheckClass.choseAll()` |
| `sendMessageAll($event)` |
| `schoolMateCheckClass.choseSingle()` |
| `sendMessage(item.schoolMateCheck.id,$index)` |
| `modifyAdminList(item.schoolMateCheck.id)` |
| `goCheck(item.schoolMateCheck.id)` |
| `screenModal()` |

**跳转到**：`screenPromotionList`

### 1.49 `schoolMateCheckReports`

- **URL**：`/schoolMateCheckReports`
- **模板**：`views/screenAdmin/schoolMateCheckReports.html`
- **控制器**：`schoolMateCheckReportsCtrl`
- **端点数**：0

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolPlanId` |
| `obj.inYear` |
| `obj.classId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `inyear.id` |
| `inyear.planName` |
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.className` |
| `getVisionObjectFactory.result.object.schoolPlan.planName` |
| `getVisionObjectFactory.result.object.goodCount` |
| `getVisionObjectFactory.result.object.notGoodCount` |
| `getVisionObjectFactory.result.object.lowCount` |
| `getVisionObjectFactory.result.object.dioptersGoodCount` |
| `getVisionObjectFactory.result.object.dioptersNotGoodCount` |
| `getVisionObjectFactory.result.object.dioptersNotGoodCount1` |
| `getVisionObjectFactory.result.object.dioptersNotGoodCount2` |
| `getVisionObjectFactory.result.object.dioptersNotGoodCount3` |
| `getVisionObjectFactory.result.object.dioptersNotCheckCount` |
| `getVisionObjectFactory.result.object.schoolMateCount` |
| `getVisionObjectFactory.result.object.examinedSchoolMateCount` |
| `item.school.schoolName` |
| `item.goodCount` |
| `item.goodRate` |
| `toFixed` |
| `item.notGoodCount` |
| `item.notGoodRate` |
| `item.lowCount` |
| `item.lowRate` |
| `item.dioptersGoodCount` |
| `item.dioptersGoodRate` |
| `item.dioptersNotGoodCount` |
| `item.dioptersNotGoodRate` |
| `item.dioptersNotGoodCount1` |
| `item.dioptersNotGoodRate1` |
| `item.dioptersNotGoodCount2` |
| `item.dioptersNotGoodRate2` |
| `item.dioptersNotGoodCount3` |
| `item.dioptersNotGoodRate3` |
| `item.dioptersNotCheckCount` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `getSchoolVisionObjectFactory.result.object.school.schoolName` |
| `getSchoolVisionObjectFactory.result.object.goodCount` |
| `getSchoolVisionObjectFactory.result.object.notGoodCount` |
| `getSchoolVisionObjectFactory.result.object.lowCount` |
| `getSchoolVisionObjectFactory.result.object.dioptersGoodCount` |
| `getSchoolVisionObjectFactory.result.object.dioptersNotGoodCount` |
| `getSchoolVisionObjectFactory.result.object.dioptersNotGoodCount1` |
| `getSchoolVisionObjectFactory.result.object.dioptersNotGoodCount2` |
| `getSchoolVisionObjectFactory.result.object.dioptersNotGoodCount3` |
| `getSchoolVisionObjectFactory.result.object.dioptersNotCheckCount` |
| `getSchoolVisionObjectFactory.result.object.schoolMateCount` |
| `getSchoolVisionObjectFactory.result.object.examinedSchoolMateCount` |
| `item.inYear` |
| `inYear` |
| `getVisionYearObjectFactory.result.object.inYear` |
| `getVisionYearObjectFactory.result.object.goodCount` |
| `getVisionYearObjectFactory.result.object.notGoodCount` |
| `getVisionYearObjectFactory.result.object.lowCount` |
| `getVisionYearObjectFactory.result.object.dioptersGoodCount` |
| `getVisionYearObjectFactory.result.object.dioptersNotGoodCount` |
| `getVisionYearObjectFactory.result.object.dioptersNotGoodCount1` |
| `getVisionYearObjectFactory.result.object.dioptersNotGoodCount2` |
| `getVisionYearObjectFactory.result.object.dioptersNotGoodCount3` |
| `getVisionYearObjectFactory.result.object.dioptersNotCheckCount` |
| `getVisionYearObjectFactory.result.object.schoolMateCount` |
| `getVisionYearObjectFactory.result.object.examinedSchoolMateCount` |
| `getVisionClassObjectFactory.result.object.schoolClass.className` |
| `getVisionClassObjectFactory.result.object.goodCount` |
| `getVisionClassObjectFactory.result.object.notGoodCount` |
| `getVisionClassObjectFactory.result.object.lowCount` |
| `getVisionClassObjectFactory.result.object.dioptersGoodCount` |
| `getVisionClassObjectFactory.result.object.dioptersNotGoodCount` |
| `getVisionClassObjectFactory.result.object.dioptersNotGoodCount1` |
| `getVisionClassObjectFactory.result.object.dioptersNotGoodCount2` |
| `getVisionClassObjectFactory.result.object.dioptersNotGoodCount3` |
| `getVisionClassObjectFactory.result.object.dioptersNotCheckCount` |
| `getVisionClassObjectFactory.result.object.schoolMateCount` |
| `getVisionClassObjectFactory.result.object.examinedSchoolMateCount` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |

### 1.50 `schoolPlanList`

- **URL**：`/schoolPlanList`
- **模板**：`views/screenAdmin/schoolPlanList.html`
- **控制器**：`schoolPlanListCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disableSchoolPlan` | `POST /admin/disableSchoolPlan.json` |
| `enableSchoolPlan` | `POST /admin/enableSchoolPlan.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |
| `selectSchoolPlanList` | `POST /admin/selectSchoolPlanList.json` |
| `selectSchoolPlanRootList` | `POST /admin/selectSchoolPlanRootList.json` |
| `setDefaultSchoolPlanByAdminId` | `POST /admin/setDefaultSchoolPlanByAdminId.json` |
| `setDefaultSchoolPlanRootByAdminId` | `POST /admin/setDefaultSchoolPlanRootByAdminId.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 筛查计划名称 |
| 2 | 所属年度 |
| 3 | 备注 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `getDefaultObjectFactory.result.object.planName` |
| `item.planName` |
| `item.year` |
| `item.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setRecyle(1)` |
| `setRecyle(2)` |
| `delete(item.id)` |
| `recovery(item.id)` |
| `setDefault(item.id)` |
| `setAreaDefault(item.id)` |

**跳转到**：`addAreaSchoolPlan`, `addSchoolPlan`

### 1.51 `areaSchoolPlanList`

- **URL**：`/areaSchoolPlanList`
- **模板**：`views/screenAdmin/schoolPlanList.html`
- **控制器**：`schoolPlanListCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disableSchoolPlan` | `POST /admin/disableSchoolPlan.json` |
| `enableSchoolPlan` | `POST /admin/enableSchoolPlan.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getDefaultSchoolPlanRootByAdminId` | `POST /admin/getDefaultSchoolPlanRootByAdminId.json` |
| `selectSchoolPlanList` | `POST /admin/selectSchoolPlanList.json` |
| `selectSchoolPlanRootList` | `POST /admin/selectSchoolPlanRootList.json` |
| `setDefaultSchoolPlanByAdminId` | `POST /admin/setDefaultSchoolPlanByAdminId.json` |
| `setDefaultSchoolPlanRootByAdminId` | `POST /admin/setDefaultSchoolPlanRootByAdminId.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 筛查计划名称 |
| 2 | 所属年度 |
| 3 | 备注 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `getDefaultObjectFactory.result.object.planName` |
| `item.planName` |
| `item.year` |
| `item.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setRecyle(1)` |
| `setRecyle(2)` |
| `delete(item.id)` |
| `recovery(item.id)` |
| `setDefault(item.id)` |
| `setAreaDefault(item.id)` |

**跳转到**：`addAreaSchoolPlan`, `addSchoolPlan`

### 1.52 `schoolPlanReport`

- **URL**：`/schoolPlanReport`
- **模板**：`views/screenAdmin/schoolPlanReport.html`
- **控制器**：`schoolPlanReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getReportStatusOfSchoolAdmin` | `POST /admin/getReportStatusOfSchoolAdmin.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectMyAdminSchoolVoListOfSchoolPlan` | `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json` |
| `selectSchoolPlanListBySchool` | `POST /admin/selectSchoolPlanListBySchool.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.schoolName` |
| `obj.planName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectSchool()` |
| `showSelectPlan()` |

### 1.53 `screenBackConfig`

- **URL**：`/screenBackConfig`
- **模板**：`views/screenAdmin/screenBackConfig.html`
- **控制器**：`screenBackConfigCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteSchoolCheckImageFile` | `POST /admin/deleteSchoolCheckImageFile.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `selectSchoolCheckImageFileList` | `POST /admin/selectSchoolCheckImageFileList.json` |
| `setDefaultSchoolCheckImageFile` | `POST /admin/setDefaultSchoolCheckImageFile.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `checkImg.imageTitle` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.imageTitle` |
| `checkList.items` |
| `previewIndex` |
| `imageUrl` |
| `typeOfPopout` |
| `checkImg.imageUrl` |
| `bigImgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `openPopout(item)` |
| `delete(item,$index)` |
| `switch(item)` |
| `openPopout()` |
| `changeStatus()` |
| `save()` |
| `clear()` |
| `imgModal=false` |
| `$event.stopPropagation()` |

### 1.54 `screenClassReport`

- **URL**：`/screenClassReport`
- **模板**：`views/screenAdmin/screenClassReport.html`
- **控制器**：`screenClassReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `printSchoolPromotionListVoList` | `POST /admin/printSchoolPromotionListVoList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `item.schoolPlan.planName` |
| `item.promotion.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.classVisionStatVo.schoolMateCount` |
| `item.classVisionStatVo.examinedSchoolMateCount` |
| `item.classVisionStatVo.goodCount` |
| `item.classVisionStatVo.notGoodCount` |
| `item.classVisionStatVo.lowCount` |
| `item.classVisionStatVo.dioptersGoodCount` |
| `item.classVisionStatVo.dioptersNotGoodCount` |
| `item.classVisionStatVo.dioptersNotGoodCount1` |
| `item.classVisionStatVo.dioptersNotGoodCount2` |
| `item.classVisionStatVo.dioptersNotGoodCount3` |
| `item.classVisionStatVo.dioptersNotCheckCount` |
| `item.classVisionStatVo.goodRate` |
| `toFixed` |
| `item.classVisionStatVo.notGoodRate` |
| `item.classVisionStatVo.lowRate` |
| `item.classVisionStatVo.dioptersGoodRate` |
| `iten.classMateName` |
| `iten.right1` |
| `vision` |
| `iten.right2` |
| `iten.left1` |
| `iten.left2` |
| `iten.right15` |
| `iten.right14` |
| `iten.right13` |
| `iten.left15` |
| `iten.left14` |
| `iten.left13` |
| `obj.schoolPlanId` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool($event)` |
| `downloadModal=true` |
| `downloadModal=false` |

### 1.55 `screenConditionBatch`

- **URL**：`/screenConditionBatch`
- **模板**：`views/screenAdmin/screenConditionBatch.html`
- **控制器**：`screenConditionBatchCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelScreenTemplateBatchSendTask` | `POST /admin/cancelScreenTemplateBatchSendTask.json` |
| `selectTaskScreenTemplateBatchSendList` | `POST /admin/selectTaskScreenTemplateBatchSendList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 目标人群 |
| 3 | 预计投放人数 |
| 4 | 发送成功 |
| 5 | 发送状态 |
| 6 | 异常原因 |
| 7 | 开始发送时间 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.taskName` |
| `item.totalCount` |
| `item.sendCount` |
| `item.status` |
| `smsStatus` |
| `item.failReason` |
| `item.taskStartTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |

**页面动作（ng-click）**

| 动作 |
|---|
| `newAddGroup()` |
| `lookCondition(item.id)` |
| `cancelTask(item.id,$index)` |

### 1.56 `screenConditionBatchGroupSend`

- **URL**：`/screenConditionBatchGroupSend?taskScreenTemplateBatchSendId`
- **模板**：`views/screenAdmin/screenConditionBatchGroupSend.html`
- **控制器**：`screenConditionBatchGroupSendCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createScreenTemplateBatchSendTask` | `POST /admin/createScreenTemplateBatchSendTask.json` |
| `selectCorpSmsByCorpId` | `POST /admin/selectCorpSmsByCorpId.json` |
| `selectCorpVoiceByCorpId` | `POST /admin/selectCorpVoiceByCorpId.json` |
| `selectScreenTemplateBatchSendTaskDetails` | `POST /admin/selectScreenTemplateBatchSendTaskDetails.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 类型 |
| 2 | 内容 |
| 3 | 模板 |
| 4 | 操作 |
| 5 | 发送时间 |
| 6 | 姓名 |
| 7 | 手机号 |
| 8 | 内容 |
| 9 | 发送状态 |
| 10 | 学校 |
| 11 | 班级 |
| 12 | 姓名 |
| 13 | 性别 |
| 14 | 生日 |
| 15 | 联系电话 |
| 16 | 身份证号或学籍号 |
| 17 | 祼眼视力(右\|左) |
| 18 | 视力诊断(右\|左) |
| 19 | 戴镜视力(右\|左) |
| 20 | 戴镜类型 |
| 21 | 球镜(右\|左) |
| 22 | 柱镜(右\|左) |
| 23 | 轴位(右\|左) |
| 24 | 屈光诊断(右\|左) |
| 25 | 筛查性近视 |
| 26 | 视力矫正 |
| 27 | 常见眼科疾病 |
| 28 | 方案建议 |
| 29 | 检查日期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.time` |
| `obj.taskName` |
| `object.keyword` |
| `searchValue.schoolBodyStatParam.keyword` |
| `searchKey.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `templateAddress` |
| `item.name` |
| `item.info` |
| `exportObject.exportCount` |
| `item.count` |
| `item.unit` |
| `choseTable.smsInfo.smsTemplate.title` |
| `choseTable.smsInfo.smsTemplate.example` |
| `choseTable.voiceInfo.voiceTemplate.title` |
| `choseTable.voiceInfo.voiceTemplate.example` |
| `searchValue.taskScreenTemplateBatchSend.taskName` |
| `searchValue.smsTemplate.example` |
| `searchValue.voiceTemplate.example` |
| `searchValue.taskScreenTemplateBatchSend.status` |
| `item.smsLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.voiceLog.gmtCreate` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.customerMobile` |
| `item.smsLog.smsContent` |
| `item.voiceLog.voiceContent` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheck.right265` |
| `quCheckResult` |
| `item.schoolMateCheck.left265` |
| `item.schoolMateCheck.visionCorrectStatus` |
| `visionCorrectStatus` |
| `item.schoolMateCheck.commonRemark` |
| `item.schoolMateCheck.left68` |
| `item.schoolMateCheck.checkDate` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addressInfo.click(item.status)` |
| `preview=!preview` |
| `choseMessage($index,$event)` |
| `choseTable.openPopout(` |
| `sendTimeInfo.click(item.status)` |
| `sendTimeInfo.groupList[0].addOne()` |
| `sendTimeInfo.groupList[0].subOne($index)` |
| `sendTask()` |

**跳转到**：`screenConditionBatch`

### 1.57 `screenConditionBatchGroupSendLook`

- **URL**：`/screenConditionBatchGroupSendLook?taskScreenTemplateBatchSendId`
- **模板**：`views/screenAdmin/screenConditionBatchGroupSendLook.html`
- **控制器**：`screenConditionBatchGroupSendLookCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectTaskTemplateBatchSendLogVoList` | `POST /admin/selectTaskTemplateBatchSendLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 类型 |
| 3 | 内容 |
| 4 | 开始发送时间 |
| 5 | 发送时间 |
| 6 | 类型 |
| 7 | 会员 |
| 8 | 手机号 |
| 9 | 内容 |
| 10 | 发送状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `paramsObj.taskTemplateBatchSend.taskName` |
| `paramsObj.smsTemplate.example` |
| `paramsObj.voiceTemplate.example` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.model` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `item.content` |

### 1.58 `screenContrastReport`

- **URL**：`/screenContrastReport`
- **模板**：`views/screenAdmin/screenContrastReport.html`
- **控制器**：`screenContrastReportCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 项目 |
| 2 | 人次 |
| 3 | 比率 |
| 4 | 人次 |
| 5 | 比率 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `object.inYear` |
| `obj.classId` |
| `object.classId` |
| `obj.gender` |
| `object.gender` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `object.planName` |
| `obj.schoolName` |
| `object.schoolName` |
| `inyear` |
| `class.id` |
| `class.className` |
| `class.name` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionObjectVisionFactory.result.object.examinedSchoolMateCount` |
| `getPromotionVisionFactory.result.object.goodCount` |
| `getPromotionVisionFactory.result.object.goodRate` |
| `toFixed` |
| `getPromotionObjectVisionFactory.result.object.goodCount` |
| `getPromotionObjectVisionFactory.result.object.goodRate` |
| `getPromotionVisionFactory.result.object.notGoodCount` |
| `getPromotionVisionFactory.result.object.notGoodRate` |
| `getPromotionObjectVisionFactory.result.object.notGoodCount` |
| `getPromotionObjectVisionFactory.result.object.notGoodRate` |
| `getPromotionVisionFactory.result.object.lowCount` |
| `getPromotionVisionFactory.result.object.lowRate` |
| `getPromotionObjectVisionFactory.result.object.lowCount` |
| `getPromotionObjectVisionFactory.result.object.lowRate` |
| `getPromotionVisionFactory.result.object.dioptersGoodCount` |
| `getPromotionVisionFactory.result.object.dioptersGoodRate` |
| `getPromotionObjectVisionFactory.result.object.dioptersGoodCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersGoodRate` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodRate` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodRate` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount1` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodRate1` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodCount1` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodRate1` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount2` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodRate2` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodCount2` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodRate2` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount3` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodRate3` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodCount3` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotGoodRate3` |
| `getPromotionVisionFactory.result.object.dioptersNotCheckCount` |
| `getPromotionObjectVisionFactory.result.object.dioptersNotCheckCount` |
| `obj.schoolPlanId` |
| `object.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showPlan()` |
| `showSelectSchool()` |
| `clearAllSchool($event)` |
| `showSchool()` |
| `clearAllTwoSchool($event)` |

### 1.59 `screenInStore`

- **URL**：`/screenInStore`
- **模板**：`views/screenAdmin/screenInStore.html`
- **控制器**：`screenInStoreCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyQrcode` | `POST /admin/getCompanyQrcode.json` |
| `getCorpSchoolPlanVoOfCompany` | `POST /admin/getCorpSchoolPlanVoOfCompany.json` |
| `selectSchoolPlanList` | `POST /admin/selectSchoolPlanList.json` |
| `setCorpSchoolPlan` | `POST /admin/setCorpSchoolPlan.json` |
| `updateSchoolPlanCheckSwitch` | `POST /admin/updateSchoolPlanCheckSwitch.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 类型 |
| 2 | 项目 |
| 3 | 操作 |
| 4 | 类型 |
| 5 | 项目 |
| 6 | 操作 |
| 7 | 筛查计划名称 |
| 8 | 所属年度 |
| 9 | 备注 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `search.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyInfo.companyName` |
| `storeSchoolPlan.planName` |
| `switchList` |
| `bodyCheckVo.bodyCheckItemList.length` |
| `bodyCheckVo.bodyCheck.checkName` |
| `bodyCheckVo.bodyCheckItemList` |
| `bodyCheckItem.itemName` |
| `item.bodyCheckItem.itemName` |
| `item.planName` |
| `item.year` |
| `item.remark` |
| `srcimg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideTab()` |
| `downLoad(false)` |
| `downLoad(true)` |
| `switchPlan()` |
| `operation(0,0)` |
| `operation(0,1)` |
| `operation(1,0)` |
| `operation(1,1)` |
| `operation(2,0)` |
| `operation(2,1)` |
| `operation(3,0)` |
| `operation(3,1)` |
| `operation(4,0)` |
| `operation(4,1)` |
| `operation(5,0)` |
| `operation(5,1)` |
| `operation(6,0)` |
| `operation(6,1)` |
| `closePlan()` |
| `cutPlan(item)` |

**跳转到**：`addSchoolPlan`, `markOriginSet`, `reachStoreAppointDetails`

### 1.60 `screenList`

- **URL**：`/screenList?promotionId&schoolPlanId`
- **模板**：`views/screenAdmin/screenList.html`
- **控制器**：`screenListCtrl`
- **端点数**：16

**调用的端点**

| 动作 | 端点 |
|---|---|
| `bandingSchoolMatePromotion` | `POST /admin/bandingSchoolMatePromotion.json` |
| `disBandingSchoolMatePromotion` | `POST /admin/disBandingSchoolMatePromotion.json` |
| `getPromotionVo` | `POST /admin/getPromotionVo.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolClass` | `POST /admin/getSchoolClass.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolMateCheckVoByUniqueKey` | `POST /admin/getSchoolMateCheckVoByUniqueKey.json` |
| `getSchoolMateCountOfPromotions` | `POST /admin/getSchoolMateCountOfPromotions.json` |
| `insertSchoolMate` | `POST /admin/insertSchoolMate.json` |
| `selectCheckItemListOfCorp` | `POST /admin/selectCheckItemListOfCorp.json` |
| `selectCloudPrinterList` | `POST /admin/selectCloudPrinterList.json` |
| `selectOtherSystemByCorpId` | `POST /admin/selectOtherSystemByCorpId.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `sendSchoolMateCheckCodeOfPromotionsToCloudPrinter` | `POST /admin/sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json` |
| `statCheckStatusOfPromotion` | `POST /admin/statCheckStatusOfPromotion.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| 性别 |
| 出生年月 |
| 证件号 |
| 手机号 |
| 民族 |
| 籍贯 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.classMateName` |
| `customerField.gender` |
| `customerField.birthday` |
| `customerField.schoolMateCode` |
| `customerField.customerMobile` |
| `customerField.nation` |
| `customerField.nativePlace` |
| `customerField.outRecordId` |
| `cloud.cloudPrinterId` |
| `sort.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPromotionFactory.result.object.promotion.title` |
| `modifySchoolName` |
| `classKeyword` |
| `homeName` |
| `getPromotionFactory.result.object.promotion.address` |
| `getPromotionFactory.result.object.promotion.remark` |
| `memberFactory.allData.statData.totalCount` |
| `memberFactory.allData.statData.checkedCount` |
| `memberFactory.allData.statData.waitingCheckCount` |
| `item.schoolMateCheck.namePinyin` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.checkCode` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.checkStatusMap` |
| `checkScreenStatus2` |
| `screenProjectOptions.list` |
| `class.id` |
| `class.name` |
| `customerField.birthday` |
| `getSchoolPrintCountFactory.result.object` |
| `printTime` |
| `val.id` |
| `val.remark` |
| `val.serialNumber` |
| `checkconfFactory.result.object.codeType` |
| `codeType` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `printAll()` |
| `modifyId=null` |
| `setTab(null)` |
| `setTab(true)` |
| `setTab(false)` |
| `infoModal=true` |
| `sortSearch(1)` |
| `sortSearch(2)` |
| `sortSearch(3)` |
| `sortSearch(4)` |
| `goCheck(item.schoolMateCheck.schoolMateId)` |
| `cancenBand(item.schoolMateCheck.schoolMateId,$event)` |
| `modify(item.schoolMate.id,$event)` |
| `cancenBand(item.schoolMate.id,$event)` |
| `open1()` |
| `quickAddMedical()` |
| `closeInfoModal()` |
| `infoModal=false` |
| `printAllModel=false` |
| `selectPrintDevice()` |

**跳转到**：`screenPromotionList`

### 1.61 `screenPromotionConfig`

- **URL**：`/screenPromotionConfig`
- **模板**：`views/screenAdmin/screenPromotionConfig.html`
- **控制器**：`screenPromotionConfigCtrl`
- **端点数**：19

**调用的端点**

| 动作 | 端点 |
|---|---|
| `delSchoolCheckWechatShow` | `POST /admin/delSchoolCheckWechatShow.json` |
| `getCorpAppointConf` | `POST /admin/getCorpAppointConf.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolCheckWechatShow` | `POST /admin/getSchoolCheckWechatShow.json` |
| `getSchoolCheckWechatVo` | `POST /admin/getSchoolCheckWechatVo.json` |
| `moveSchoolCheckWechatShow` | `POST /admin/moveSchoolCheckWechatShow.json` |
| `saveCorpAppointConf` | `POST /admin/saveCorpAppointConf.json` |
| `saveCorpWechatAccountConf` | `POST /admin/saveCorpWechatAccountConf.json` |
| `saveSchoolCheckBandingType` | `POST /admin/saveSchoolCheckBandingType.json` |
| `saveSchoolCheckConf` | `POST /admin/saveSchoolCheckConf.json` |
| `selectCorpWechatAccountConf` | `POST /admin/selectCorpWechatAccountConf.json` |
| `selectSchoolCheckQuestionnaireConfVoList` | `POST /admin/selectSchoolCheckQuestionnaireConfVoList.json` |
| `selectSchoolCheckWechatList` | `POST /admin/selectSchoolCheckWechatList.json` |
| `selectSchoolCheckWechatShowList` | `POST /admin/selectSchoolCheckWechatShowList.json` |
| `updateSchoolCheckQuestionnaireConf` | `POST /admin/updateSchoolCheckQuestionnaireConf.json` |
| `updateSchoolCheckWechat` | `POST /admin/updateSchoolCheckWechat.json` |
| `updateSchoolCheckWechatItemValue` | `POST /admin/updateSchoolCheckWechatItemValue.json` |
| `updateSchoolCheckWechatShowOpenEnable` | `POST /admin/updateSchoolCheckWechatShowOpenEnable.json` |

**表单标签**

| 标签 |
|---|
| 统一引流到门店 |
| 统一引流到总部 |
| {{dv.itemValueName}}： |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 名称 |
| 2 | 内容 |
| 3 | 状态 |
| 4 | 问卷标题 |
| 5 | 填写来源 |
| 6 | 填写方式 |
| 7 | 针对人群 |
| 8 | 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.openEnable` |
| `obj.wechatCheckRecordTitle` |
| `obj.wechatCheckRecordRemark` |
| `dv.itemValueContent` |
| `item.schoolCheckQuestionnaireConf.openEnable` |
| `loadPicture.vo.content` |
| `loadPicture.vo.title` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.rowspan` |
| `item.name` |
| `item.contentName` |
| `item` |
| `obj.wechatCheckRecordImage` |
| `item.checkName` |
| `currentName` |
| `item.schoolCheckParamItem.itemName` |
| `dv.itemValueName` |
| `item.title` |
| `index` |
| `item.schoolCheckQuestionnaire.questionnaireTitle` |
| `item.schoolCheckQuestionnaire.fillSource` |
| `item.schoolCheckQuestionnaire.fillMethod` |
| `item.schoolCheckQuestionnaire.targetPopulation` |
| `getCorpInfoObjectFactory.object.corporationName` |
| `partCompany.companyName` |
| `getCorpInfoObjectFactory.object.servicePhone` |
| `partCompany.phone` |
| `getCorpInfoObjectFactory.object.address` |
| `partCompany.address` |
| `item.image` |
| `item.content` |
| `loadPicture.type` |
| `bigImgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePopout($event)` |
| `changeConfig(0)` |
| `changeConfig(1)` |
| `changeConfig(2)` |
| `deleteImg()` |
| `bigImg(obj.wechatCheckRecordImage)` |
| `save()` |
| `setDioptersAndVisionIndex(index,item)` |
| `setBandingType(2)` |
| `setBandingType(1)` |
| `changeStatus(dv,$index)` |
| `updatePromotion()` |
| `changePicStatus(item)` |
| `openPopout($index,$event)` |
| `deletePicConfig(item)` |
| `translateY(item,true)` |
| `editorPromotion(item,$index)` |
| `translateY(item,false)` |
| `savePicConfig()` |
| `clear()` |
| `imgModal=false` |
| `$event.stopPropagation()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 1.62 `screenPromotionList`

- **URL**：`/screenPromotionList`
- **模板**：`views/screenAdmin/screenPromotionList.html`
- **控制器**：`screenPromotionListCtrl`
- **端点数**：15

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `getSchoolMateCheckVoByUniqueKey` | `POST /admin/getSchoolMateCheckVoByUniqueKey.json` |
| `getSchoolMateCountOfPromotions` | `POST /admin/getSchoolMateCountOfPromotions.json` |
| `insertSchoolMateAndCreatePromotion` | `POST /admin/insertSchoolMateAndCreatePromotion.json` |
| `selectCloudPrinterList` | `POST /admin/selectCloudPrinterList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectOtherSystemByCorpId` | `POST /admin/selectOtherSystemByCorpId.json` |
| `selectSchoolPromotionListVoList` | `POST /admin/selectSchoolPromotionListVoList.json` |
| `sendMsgToSchoolMateCheckBySelected` | `POST /admin/sendMsgToSchoolMateCheckBySelected.json` |
| `sendSchoolMateCheckCodeOfPromotionsToCloudPrinter` | `POST /admin/sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json` |
| `setDefaultSchoolPlanByAdminId` | `POST /admin/setDefaultSchoolPlanByAdminId.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |
| * 学校 |
| * 班级 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| * 学校 |
| * 班级 |
| 性别 |
| 出生年月 |
| 证件号 |
| 手机号 |
| 民族 |
| 籍贯 |
| 家庭住址 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `basic.name` |
| `basic.className` |
| `customerField.gender` |
| `customerField.birthday` |
| `customerField.schoolMateCode` |
| `customerField.customerMobile` |
| `customerField.nation` |
| `customerField.nativePlace` |
| `basic.homeAddress` |
| `basic.outRecordId` |
| `obj.inYear` |
| `obj.classId` |
| `obj.keyword` |
| `cloud.cloudPrinterId` |
| `item.classIdArr[innerIndex]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDefaultObjectFactory.result.object.planName` |
| `basic.schoolName` |
| `inyear.id` |
| `inyear.className` |
| `class.id` |
| `class.name` |
| `customerField.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `stateObjectFactory.object.schoolCount` |
| `stateObjectFactory.object.classCount` |
| `stateObjectFactory.object.schoolMateCount` |
| `stateObjectFactory.object.visionCheckedCount` |
| `obj.schoolName` |
| `inyear` |
| `item.school.schoolName` |
| `item.classCount` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `iten.schoolMateCount` |
| `iten.checkStatusStatVo.examinedCount` |
| `iten.schoolClass.className` |
| `iten.promotion.startTime` |
| `item.qrcodeTicket.expireDate` |
| `dateQrcoder` |
| `item.qrcodeTicket.qrcode` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `obj.schoolPlanId` |
| `classArray.length` |
| `getSchoolPrintCountFactory.result.object` |
| `printTime` |
| `val.id` |
| `val.remark` |
| `val.serialNumber` |
| `checkconfFactory.result.object.codeType` |
| `codeType` |
| `iten.promotion.id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `addOneStudy()` |
| `openSchoolPop()` |
| `clearBasicSchool()` |
| `open1()` |
| `confirmBasic()` |
| `closePopout()` |
| `printAll()` |
| `showSelectSchool()` |
| `clearSchool()` |
| `sendInform({schoolId:item.school.id},true)` |
| `goScreenList(iten)` |
| `sendInform({schoolId:item.school.id,classId:iten.schoolClass.id},false)` |
| `printAllModel=false` |
| `recompute()` |
| `selectPrintDevice()` |

**跳转到**：`multiImportStudent`, `screenPromotionStudent`

### 1.63 `screenPromotionStudent`

- **URL**：`/screenPromotionStudent`
- **模板**：`views/screenAdmin/screenPromotionStudent.html`
- **控制器**：`screenPromotionStudentCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disableSchoolMateCheck` | `POST /admin/disableSchoolMateCheck.json` |
| `enableSchoolMateCheck` | `POST /admin/enableSchoolMateCheck.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolInfo` | `POST /admin/getSchoolInfo.json` |
| `selectCheckItemListOfCorp` | `POST /admin/selectCheckItemListOfCorp.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectOtherSystemByCorpId` | `POST /admin/selectOtherSystemByCorpId.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `setDefaultSchoolPlanByAdminId` | `POST /admin/setDefaultSchoolPlanByAdminId.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 性别 |
| 5 | 生日 |
| 6 | 联系电话 |
| 7 | 身份证号或学籍号 |
| 8 | 民族 |
| 9 | 籍贯 |
| 10 | 家庭住址 |
| 11 | 状态 |
| 12 | 未录入项目 |
| 13 | 外部记录ID |
| 14 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `obj.keyword` |
| `isAll` |
| `schoolMateCheckIdArray[$index]` |
| `pageSize` |
| `obj.outRecordIdKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDefaultObjectFactory.result.object.planName` |
| `memberFactory.allData.statData.totalCount` |
| `memberFactory.allData.statData.checkedCount` |
| `memberFactory.allData.statData.waitingCheckCount` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `arrLabel.length` |
| `thirdPartyVo.sendType` |
| `item.schoolMateCheck.id` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMate.nation` |
| `item.schoolMate.nativePlace` |
| `item.schoolMate.homeAddress` |
| `item.checkStatusMap` |
| `checkScreenStatus3` |
| `screenProjectOptions.list` |
| `checkScreenStatus4` |
| `item.schoolMateCheck.outRecordId` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `setRecyle(1)` |
| `setRecyle(0)` |
| `setTab(null)` |
| `setTab(true)` |
| `setTab(false)` |
| `showSelectSchool()` |
| `clearSchool()` |
| `multiDelete()` |
| `multiRecovery()` |
| `recycle()` |
| `checkAll()` |
| `setLabelBtn()` |
| `goCheck(item.schoolMateCheck.id)` |
| `delete(item.schoolMateCheck.id)` |
| `recovery(item.schoolMateCheck.id)` |
| `smsPop.close()` |
| `smsPop.confirm()` |

**跳转到**：`multiImportStudent`, `screenPromotionList`

### 1.64 `screenPromotionToothConfig`

- **URL**：`/screenPromotionToothConfig`
- **模板**：`views/screenAdmin/screenPromotionToothConfig.html`
- **控制器**：`screenPromotionToothConfigCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `delSchoolCheckWechatShow` | `POST /admin/delSchoolCheckWechatShow.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `getSchoolCheckWechatShow` | `POST /admin/getSchoolCheckWechatShow.json` |
| `moveSchoolCheckWechatShow` | `POST /admin/moveSchoolCheckWechatShow.json` |
| `saveSchoolCheckConf` | `POST /admin/saveSchoolCheckConf.json` |
| `selectSchoolCheckWechatShowList` | `POST /admin/selectSchoolCheckWechatShowList.json` |
| `updateSchoolCheckWechatShowStatus` | `POST /admin/updateSchoolCheckWechatShowStatus.json` |

**表单标签**

| 标签 |
|---|
| 统一引流到门店 |
| 统一引流到总部 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.bandingType` |
| `loadPicture.vo.content` |
| `loadPicture.vo.title` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.title` |
| `index` |
| `partCompany.companyName` |
| `getCorpInfoObjectFactory.object.corporationName` |
| `getCorpInfoObjectFactory.object.servicePhone` |
| `partCompany.phone` |
| `getCorpInfoObjectFactory.object.address` |
| `partCompany.address` |
| `item.image` |
| `item.content` |
| `myCorpList.companyName` |
| `myCorpList.phone` |
| `myCorpList.address` |
| `obj.wechatCheckRecordImage` |
| `obj.wechatCheckRecordTitle` |
| `obj.wechatCheckRecordRemark` |
| `loadPicture.type` |
| `bigImgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePopout($event)` |
| `setBandingType(2)` |
| `setBandingType(1)` |
| `changeStatus(item,$index)` |
| `openPopout($index,$event)` |
| `deletePicConfig(item)` |
| `translateY(item,true)` |
| `updatePromotion(item,$index)` |
| `translateY(item,false)` |
| `updatePromotion()` |
| `savePicConfig()` |
| `clear()` |
| `imgModal=false` |
| `$event.stopPropagation()` |

### 1.65 `screenRecordReport`

- **URL**：`/screenRecordReport`
- **模板**：`views/screenAdmin/screenRecordReport.html`
- **控制器**：`screenRecordReportCtrl`
- **端点数**：0

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCondition.preview` |
| `exportObject.exportCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showExport($event,4)` |
| `showExport($event,1)` |
| `showExport($event,2)` |
| `showExport($event,3)` |
| `getCondition.preview=!getCondition.preview` |

**跳转到**：`medicalConfig`, `printStudentReport`

### 1.66 `screenReportInschool`

- **URL**：`/screenReportInschool`
- **模板**：`views/screenAdmin/screenReportInschool.html`
- **控制器**：`screenReportInschoolCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getReportStatusOfSchoolAdmin` | `POST /admin/getReportStatusOfSchoolAdmin.json` |
| `selectMyAdminSchoolVoListOfSchoolPlan` | `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json` |
| `selectSchoolPlanListBySchool` | `POST /admin/selectSchoolPlanListBySchool.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.schoolName` |
| `obj.planName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectSchool()` |
| `showSelectPlan()` |

### 1.67 `screenSchoolReport`

- **URL**：`/screenSchoolReport`
- **模板**：`views/screenAdmin/screenSchoolReport.html`
- **控制器**：`screenSchoolReportCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `getVisionObjectFactory.result.object.schoolPlan.planName` |
| `item.school.schoolName` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `item.goodCount` |
| `item.goodRate` |
| `toFixed` |
| `item.notGoodCount` |
| `item.notGoodRate` |
| `item.lowCount` |
| `item.lowRate` |
| `item.dioptersNotGoodCount1` |
| `item.dioptersNotGoodRate1` |
| `item.dioptersNotGoodCount2` |
| `item.dioptersNotGoodRate2` |
| `item.dioptersNotGoodCount3` |
| `item.dioptersNotGoodRate3` |
| `item.genderChildren` |
| `children.length` |
| `iten.gender` |
| `gender` |
| `iten.inYear` |
| `inYear` |
| `iten.schoolMateCount` |
| `iten.examinedSchoolMateCount` |
| `iten.goodCount` |
| `iten.goodRate` |
| `iten.notGoodCount` |
| `iten.notGoodRate` |
| `iten.lowCount` |
| `iten.lowRate` |
| `iten.dioptersNotGoodCount1` |
| `iten.dioptersNotGoodRate1` |
| `iten.dioptersNotGoodCount2` |
| `iten.dioptersNotGoodRate2` |
| `iten.dioptersNotGoodCount3` |
| `iten.dioptersNotGoodRate3` |
| `schoolMateCount` |
| `examinedSchoolMateCount` |
| `goodCount` |
| `goodRate` |
| `notGoodCount` |
| `notGoodRate` |
| `lowCount` |
| `lowRate` |
| `dioptersNotGoodCount1` |
| `dioptersNotGoodCount2` |
| `dioptersNotGoodCount3` |
| `getSchoolVisionObjectFactory.result.object.school.schoolName` |
| `item.inYear` |
| `iten.schoolClass.className` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |

### 1.68 `screenStudentReport`

- **URL**：`/screenStudentReport`
- **模板**：`views/screenAdmin/screenStudentReport.html`
- **控制器**：`screenStudentReportCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolBodyCheckInfoListOfSchoolPlan` | `POST /admin/getSchoolBodyCheckInfoListOfSchoolPlan.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectBodyCheckVoByCode` | `POST /admin/selectBodyCheckVoByCode.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**表单标签**

| 标签 |
|---|
| 视力筛查 屈光筛查 {{iten.checkName}} 其他筛查 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 性别 |
| 5 | 生日 |
| 6 | 联系电话 |
| 7 | 身份证号或学籍号 |
| 8 | 祼眼视力(右\|左) |
| 9 | 视力诊断(右\|左) |
| 10 | 戴镜视力(右\|左) |
| 11 | 戴镜类型 |
| 12 | 方案建议 |
| 13 | 备注 |
| 14 | 操作 |
| 15 | 学校 |
| 16 | 班级 |
| 17 | 姓名 |
| 18 | 性别 |
| 19 | 生日 |
| 20 | 联系电话 |
| 21 | 身份证号或学籍号 |
| 22 | 球镜(右\|左) |
| 23 | 柱镜(右\|左) |
| 24 | 轴位(右\|左) |
| 25 | 屈光诊断(右\|左) |
| 26 | 眼压(右\|左) |
| 27 | 眼轴(右\|左) |
| 28 | 角膜曲率K1(右\|左) |
| 29 | 角膜曲率K2(右\|左) |
| 30 | 角膜曲率D1(右\|左) |
| 31 | 角膜曲率D2(右\|左) |
| 32 | 验光单照片 |
| 33 | 学校 |
| 34 | 班级 |
| 35 | 姓名 |
| 36 | 性别 |
| 37 | 生日 |
| 38 | 联系电话 |
| 39 | 身份证号或学籍号 |
| 40 | {{iten.bodyCheckItem.itemName}} ({{iten.bodyCheckItem.itemUnitName}}) (右\|左) |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `obj.keyword` |
| `tab` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.goodCount` |
| `getPromotionVisionFactory.result.object.notGoodCount` |
| `getPromotionVisionFactory.result.object.lowCount` |
| `getPromotionVisionFactory.result.object.dioptersGoodCount` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount1` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount2` |
| `getPromotionVisionFactory.result.object.dioptersNotGoodCount3` |
| `iten.checkName` |
| `tab` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.right67` |
| `item.schoolMateCheck.left67` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.left68` |
| `item.schoolMateCheck.remark` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheck.right65` |
| `item.schoolMateCheck.left65` |
| `item.schoolMateCheck.right11` |
| `item.schoolMateCheck.left11` |
| `item.schoolMateCheck.right36` |
| `item.schoolMateCheck.left36` |
| `item.schoolMateCheck.right89` |
| `item.schoolMateCheck.left89` |
| `item.schoolMateCheck.right90` |
| `item.schoolMateCheck.left90` |
| `item.schoolMateCheck.right92` |
| `item.schoolMateCheck.left92` |
| `item.schoolMateCheck.right93` |
| `item.schoolMateCheck.left93` |
| `iten.bodyCheckItem.itemName` |
| `iten.bodyCheckItem.itemUnitName` |
| `val.bodyCheckItemValue` |
| `val.bodyCheckItemValueRight` |
| `val.bodyCheckItemValueLeft` |
| `obj.schoolPlanId` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |
| `imgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool()` |
| `setVision(4)` |
| `setVision(1)` |
| `setVision(2)` |
| `setVision(3)` |
| `setVision2(6)` |
| `setVision2(1)` |
| `setVision2(2)` |
| `setVision2(3)` |
| `setVision2(4)` |
| `setVision2(5)` |
| `setTab(1)` |
| `setTab(2)` |
| `setCheckCode(iten.checkCode,3)` |
| `setTab(3)` |
| `showDaochu($event)` |
| `searchMateHistory(item.schoolMateCheck.schoolMateId)` |
| `showImg(item.schoolMateCheck.scaCheckFile)` |
| `downloadModal=false` |
| `daochu()` |
| `daochuBodycheck()` |
| `hideImgModal()` |

### 1.69 `screenUrlConfig`

- **URL**：`/screenUrlConfig`
- **模板**：`views/screenAdmin/screenUrlConfig.html`
- **控制器**：`screenUrlConfigCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `saveSchoolCheckPostConf` | `POST /admin/saveSchoolCheckPostConf.json` |
| `selectByCorpId` | `POST /admin/selectByCorpId.json` |
| `updateSchoolCheckPostConf` | `POST /admin/updateSchoolCheckPostConf.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `urlConfig.http` |
| `urlConfig.ipAddress` |
| `urlConfig.port` |
| `urlConfig.requestPath` |
| `urlConfig.url` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `http` |
| `urlConfig.http` |
| `urlConfig.ipAddress` |
| `urlConfig.port` |
| `urlConfig.requestPath` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updateStatus(1)` |
| `addOrUpdate(` |
| `updateStatus(2)` |
| `save()` |
| `update()` |

### 1.70 `studentReportInschool`

- **URL**：`/studentReportInschool`
- **模板**：`views/screenAdmin/studentReportInschool.html`
- **控制器**：`studentReportInschoolCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `basicStatGenderVision` | `POST /admin/basicStatGenderVision.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getReportStatusOfSchoolAdmin` | `POST /admin/getReportStatusOfSchoolAdmin.json` |
| `getSchoolBodyCheckInfoListOfSchoolPlan` | `POST /admin/getSchoolBodyCheckInfoListOfSchoolPlan.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectBodyCheckVoByCode` | `POST /admin/selectBodyCheckVoByCode.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectMyAdminSchoolVoListOfSchoolPlan` | `POST /admin/selectMyAdminSchoolVoListOfSchoolPlan.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `selectSchoolPlanListBySchool` | `POST /admin/selectSchoolPlanListBySchool.json` |
| `statVisionOfSchool` | `POST /admin/statVisionOfSchool.json` |

**表单标签**

| 标签 |
|---|
| 视力筛查 |
| 屈光筛查 |
| {{iten.checkName}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 性别 |
| 5 | 生日 |
| 6 | 联系电话 |
| 7 | 身份证号或学籍号 |
| 8 | 祼眼视力(右\|左) |
| 9 | 视力诊断(右\|左) |
| 10 | 戴镜视力(右\|左) |
| 11 | 戴镜类型 |
| 12 | 筛查性近视 |
| 13 | 视力矫正 |
| 14 | 常见眼科疾病 |
| 15 | 方案建议 |
| 16 | 备注 |
| 17 | 检查日期 |
| 18 | 操作 |
| 19 | 学校 |
| 20 | 班级 |
| 21 | 姓名 |
| 22 | 性别 |
| 23 | 生日 |
| 24 | 联系电话 |
| 25 | 身份证号或学籍号 |
| 26 | 球镜(右\|左) |
| 27 | 柱镜(右\|左) |
| 28 | 轴位(右\|左) |
| 29 | 屈光诊断(右\|左) |
| 30 | 眼压(右\|左) |
| 31 | 眼轴(右\|左) |
| 32 | 角膜曲率K1(右\|左) |
| 33 | 角膜曲率K2(右\|左) |
| 34 | 角膜曲率D1(右\|左) |
| 35 | 角膜曲率D2(右\|左) |
| 36 | 验光单照片 |
| 37 | 学校 |
| 38 | 班级 |
| 39 | 姓名 |
| 40 | 性别 |
| 41 | 生日 |
| 42 | 联系电话 |
| 43 | 身份证号或学籍号 |
| 44 | {{iten.bodyCheckItem.itemName}} ({{iten.bodyCheckItem.itemUnitName}}) (右\|左) |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `obj.keyword` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.schoolName` |
| `obj.planName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `getPromotionVisionFactory.result.object.schoolMateCount` |
| `getPromotionVisionFactory.result.object.visionNormalCount` |
| `getPromotionVisionFactory.result.object.visionAlert1Count` |
| `getPromotionVisionFactory.result.object.visionAlert2Count` |
| `getPromotionVisionFactory.result.object.visionAlert3Count` |
| `getPromotionVisionFactory.result.object.dioptersNormalCountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert1CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert2CountNew` |
| `getPromotionVisionFactory.result.object.dioptersAlert3CountNew` |
| `iten.checkName` |
| `tab` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.visionCorrectStatus` |
| `visionCorrectStatus` |
| `item.schoolMateCheck.commonRemark` |
| `item.schoolMateCheck.left68` |
| `item.schoolMateCheck.remark` |
| `item.schoolMateCheck.checkDate` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheck.right265` |
| `quCheckResult` |
| `item.schoolMateCheck.right11` |
| `item.schoolMateCheck.left11` |
| `item.schoolMateCheck.right36` |
| `item.schoolMateCheck.left36` |
| `item.schoolMateCheck.right89` |
| `item.schoolMateCheck.left89` |
| `item.schoolMateCheck.right90` |
| `item.schoolMateCheck.left90` |
| `item.schoolMateCheck.right92` |
| `item.schoolMateCheck.left92` |
| `item.schoolMateCheck.right93` |
| `item.schoolMateCheck.left93` |
| `iten.bodyCheckItem.itemName` |
| `iten.bodyCheckItem.itemUnitName` |
| `val.bodyCheckItemValue` |
| `val.bodyCheckItemValueRight` |
| `val.bodyCheckItemValueLeft` |
| `memberFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `memberFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectSchool()` |
| `showSelectPlan()` |
| `setMateVision(null)` |
| `setMateVision(0)` |
| `setMateVision(1)` |
| `setMateVision(2)` |
| `setMateVision(3)` |
| `setMateVision2(null)` |
| `setMateVision2(0)` |
| `setMateVision2(1)` |
| `setMateVision2(2)` |
| `setMateVision2(3)` |
| `setTab(1)` |
| `setTab(2,$event)` |
| `setCheckCode(iten.checkCode,3+$index)` |
| `showDaochu($event,3)` |
| `showDaochu($event,1)` |
| `showDaochu($event,2)` |
| `searchMateHistory(item.schoolMateCheck.schoolMateId)` |
| `showImg(item.schoolMateCheck.scaCheckFile)` |
| `downloadModal=false` |
| `daochu()` |
| `daochuBodycheck()` |

### 1.71 `transformationRate`

- **URL**：`/transformationRate`
- **模板**：`views/screenAdmin/transformationRate.html`
- **控制器**：`transformationRateCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `selectSchoolMateScreenInStoreStatVoList` | `POST /admin/selectSchoolMateScreenInStoreStatVoList.json` |
| `statScreenInStore` | `POST /admin/statScreenInStore.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 学校 |
| 2 | 班级 |
| 3 | 姓名 |
| 4 | 身份证号或学籍号 |
| 5 | 联系电话 |
| 6 | 开单数 |
| 7 | 检查数 |
| 8 | 消费数 |
| 9 | 检查费用 |
| 10 | 销售费用 |
| 11 | 消费金额 |
| 12 | 实付金额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolLevelId` |
| `obj.gender` |
| `obj.startTime` |
| `obj.endTime` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `schoolCategory.schoolLevelName` |
| `class.id` |
| `class.name` |
| `StatScreenInStore.appointCount` |
| `StatScreenInStore.schoolMateCheckCount` |
| `StatScreenInStore.customerCheckinCount` |
| `StatScreenInStore.medicalRecordCount` |
| `StatScreenInStore.medicalExamineCount` |
| `StatScreenInStore.medicalProductCount` |
| `StatScreenInStore.medicalExaminePayment` |
| `StatScreenInStore.medicalProductPayment` |
| `StatScreenInStore.totalOrderPrice` |
| `StatScreenInStore.totalOrderPayment` |
| `item.schoolName` |
| `item.className` |
| `item.classMateName` |
| `item.schoolMateCode` |
| `item.customerMobile` |
| `item.medicalRecordCount` |
| `item.medicalExamineCount` |
| `item.medicalProductCount` |
| `item.medicalExaminePayment` |
| `item.medicalProductPayment` |
| `item.totalOrderPrice` |
| `item.totalOrderPayment` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |

**跳转到**：`markOriginSet`, `reachStoreAppointAllReport`, `reachStoreAppointDetails`, `reachStoreAppointSingleReport`, `screenInStore`, `transformationRate`

### 1.72 `updateSchool`

- **URL**：`/updateSchool?schoolId`
- **模板**：`views/screenAdmin/updateSchool.html`
- **控制器**：`updateSchoolCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSchoolLevelList` | `POST /admin/getSchoolLevelList.json` |
| `getSchoolVo` | `POST /admin/getSchoolVo.json` |
| `insertAddress` | `POST /admin/insertAddress.json` |
| `updateAddress` | `POST /admin/updateAddress.json` |
| `updateSchool` | `POST /admin/updateSchool.json` |

**必填项**

| 标签 |
|---|
| * 学校名称 |
| * 学校类别 |
| * 关联门店 |
| * 省份 |
| * 城市 |
| * 区县 |
| * 片区 |
| * 监测点 |

**表单标签**

| 标签 |
|---|
| * 学校名称 |
| 学校编码 |
| * 学校类别 |
| * 关联门店 |
| * 省份 |
| * 城市 |
| * 区县 |
| * 片区 |
| * 监测点 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.schoolName` |
| `obj.schoolCode` |
| `obj.schoolLevelId` |
| `address.province` |
| `address.city` |
| `address.district` |
| `obj.districtVal` |
| `obj.monitorVal` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hide()` |
| `updateSchool()` |

**跳转到**：`schoolList`, `screenPromotionList`

**下拉数据源（ng-options）**

```
item.id as item.schoolLevelName for item in levelObjectFactory.result.list
item.name as item.name for item in citiesData
item.name as item.name for item in data
item.name as item.name for item in districtData
```

### 1.73 `viewSchoolMateCheck`

- **URL**：`/viewSchoolMateCheck?checkId`
- **模板**：`views/screenAdmin/viewSchoolMateCheck.html`
- **控制器**：`modifySchoolMateCheckCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeSchoolMateCheck` | `POST /admin/completeSchoolMateCheck.json` |
| `getBodyCheckList` | `POST /admin/getBodyCheckList.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSchoolMateCheckVo` | `POST /admin/getSchoolMateCheckVo.json` |
| `getSchoolMateCheckVoListWithSameCode` | `POST /admin/getSchoolMateCheckVoListWithSameCode.json` |
| `getSchoolTeacherList` | `POST /admin/getSchoolTeacherList.json` |
| `saveSchoolMateCheck` | `POST /admin/saveSchoolMateCheck.json` |

**表单标签**

| 标签 |
|---|
| {{item}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 筛查记录(档案编号：{{getCheckVoFactory.result.vo.schoolMateCheck.checkCode}}) |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `teacherKeyword` |
| `keyword` |
| `newadvise[$index]` |
| `newadvise` |
| `newright` |
| `newleft` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.classMateName` |
| `obj.gender` |
| `gender` |
| `date` |
| `howoldMatecheck` |
| `obj.nation` |
| `obj.nativePlace` |
| `obj.customerMobile` |
| `keyword` |
| `classKeyword` |
| `getCheckVoFactory.result.vo.schoolMateCheck.checkCode` |
| `teacheritem.schoolTeacher.teacherName` |
| `obj.checkDate` |
| `yyyy` |
| `MM` |
| `dd` |
| `schoolitem.schoolName` |
| `obj.schoolMateCode` |
| `obj.birthday` |
| `obj.right1` |
| `vision` |
| `obj.right167` |
| `newCheckResult` |
| `obj.right2` |
| `obj.left87` |
| `obj.left1` |
| `obj.left167` |
| `obj.left2` |
| `obj.right15` |
| `obj.right14` |
| `obj.right13` |
| `obj.right265` |
| `quCheckResult` |
| `obj.left15` |
| `obj.left14` |
| `obj.left13` |
| `obj.left265` |
| `obj.right11` |
| `obj.right36` |
| `obj.right89` |
| `obj.right90` |
| `obj.left11` |
| `obj.left36` |
| `obj.left89` |
| `obj.left90` |
| `item` |
| `obj.remark` |
| `schoolMateHistoryListFactory.items` |
| `schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.checkYear` |
| `item.schoolMateCheck.checkDate` |
| `item.schoolMateCheck.right1` |
| `item.schoolMateCheck.right167` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right64` |
| `item.schoolMateCheck.left64` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchMateHistory()` |
| `getMedical(medicalRecordId,patientId)` |
| `handleMsg()` |
| `chooseTeacher(teacheritem.schoolTeacher.id,teacheritem.schoolTeacher.teacherName)` |
| `chooseSchool(schoolitem.id,schoolitem.schoolName)` |
| `back()` |
| `hideSchoolMateHistory()` |
| `refreshView(item.schoolMateCheck.id)` |

### 1.74 `adultVisionMesure`

- **URL**：`/adultVisionMesure`
- **模板**：`views/screenAdmin/visionMesure.html`
- **控制器**：`visionMesureCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getEyeChartOfMine` | `POST /admin/getEyeChartOfMine.json` |
| `resetEyeChartOfMine` | `POST /admin/resetEyeChartOfMine.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `homeFactory.result.admin.mobile` |
| `getEyeChartFactory.result.object.eyeChart.testDistance` |
| `id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

### 1.75 `visionMesure`

- **URL**：`/visionMesure`
- **模板**：`views/screenAdmin/visionSelect.html`
- **控制器**：`visionMesureCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getEyeChartOfMine` | `POST /admin/getEyeChartOfMine.json` |
| `resetEyeChartOfMine` | `POST /admin/resetEyeChartOfMine.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |

**跳转到**：`adultVisionMesure`, `childVisionMesure`, `home`, `projectionScreen`

### 1.76 `zhiShiBangConfig`

- **URL**：`/zhiShiBangConfig`
- **模板**：`views/screenAdmin/zhiShiBangConfig.html`
- **控制器**：`zhiShiBangConfigCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createExamine` | `POST /admin/createExamine.json` |
| `getPinyin` | `POST /admin/getPinyin.json` |
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `saveSchoolCheckIndicatorBarImage` | `POST /admin/saveSchoolCheckIndicatorBarImage.json` |

**表单标签**

| 标签 |
|---|
| 标准指示棒 |
| 红色指示棒 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `codeType` |

**页面动作（ng-click）**

| 动作 |
|---|
| `save()` |
