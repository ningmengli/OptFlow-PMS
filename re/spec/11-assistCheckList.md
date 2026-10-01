# 11｜模块 assistCheckList 辅助检查

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/assistCheckList/` |
| 中文名 | 辅助检查 |
| 开发波次 | W2 |
| 页面数 | **4** |
| 端点数（去重） | **30** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `assistCheckList` | `/assistCheckList` | `views/assistCheckList/assistCheckList.html` | `assistCheckListCtrl` | 9 |
| 2 | `assistChecking` | `/assistChecking?medicalExamineId&editable&medicalRecordId` | `views/assistCheckList/assistChecking.html` | `assistCheckingCtrl` | 15 |
| 3 | `remindList` | `/remindList` | `views/assistCheckList/remindList.html` | `remindListCtrl` | 6 |
| 4 | `smsSet` | `/smsSet` | `views/assistCheckList/smsSet.html` | `smsSetCtrl` | 2 |

## §2 端点清单（去重 30 个）

- `POST /admin/addBrand.json`
- `POST /admin/cancelFollowUp.json`
- `POST /admin/completeExamine.json`
- `POST /admin/disconnectUartDeviceOfAdmin.json`
- `POST /admin/getAdminList.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getLatestUartDeviceLogToSchoolMateCheck.json`
- `POST /admin/getLoginEmployee.json`
- `POST /admin/getMedicalExamineItemVoList.json`
- `POST /admin/getMedicalExamineVoList.json`
- `POST /admin/getMedicalRecord.json`
- `POST /admin/getMedicalRecordExamineListVoList.json`
- `POST /admin/getPatientExamineListVoList.json`
- `POST /admin/getPatientInfo.json`
- `POST /admin/getSchoolCheckConf.json`
- `POST /admin/getVisionRecordVo.json`
- `POST /admin/modifyBrand.json`
- `POST /admin/modifyMedicalExamineItemList.json`
- `POST /admin/saveSchoolCheckConfForTemplate.json`
- `POST /admin/selectBrandByName.json`
- `POST /admin/selectEmployeeVoListOfMyCompany.json`
- `POST /admin/selectFollowUpVoList.json`
- `POST /admin/selectTop50BrandName.json`
- `POST /admin/selectUartDeviceByAdminId.json`
- `POST /admin/selectUartDeviceList.json`
- `POST /admin/setUartDeviceOfAdmin.json`
- `POST /admin/splitBrandArrayString.json`
- `POST /admin/startExamine.json`
- `POST /admin/statExamineCheckStatus.json`
- `POST /admin/uploadExamineResult.json`

## §3 逐页字段规格

### 11.1 `assistCheckList`

- **URL**：`/assistCheckList`
- **模板**：`views/assistCheckList/assistCheckList.html`
- **控制器**：`assistCheckListCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addBrand` | `POST /admin/addBrand.json` |
| `getMedicalExamineVoList` | `POST /admin/getMedicalExamineVoList.json` |
| `getMedicalRecordExamineListVoList` | `POST /admin/getMedicalRecordExamineListVoList.json` |
| `modifyBrand` | `POST /admin/modifyBrand.json` |
| `selectBrandByName` | `POST /admin/selectBrandByName.json` |
| `selectTop50BrandName` | `POST /admin/selectTop50BrandName.json` |
| `splitBrandArrayString` | `POST /admin/splitBrandArrayString.json` |
| `startExamine` | `POST /admin/startExamine.json` |
| `statExamineCheckStatus` | `POST /admin/statExamineCheckStatus.json` |

**表单标签**

| 标签 |
|---|
| {{iten.medicalExamine.examineName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTimer` |
| `medicalExamineIdArray[$index]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `checkCountFactory.object.waitingExamineCount` |
| `checkCountFactory.object.examiningCount` |
| `checkCountFactory.object.examinedCount` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.medicalRecord.medicalRecordType` |
| `medicalRecordType` |
| `item.medicalRecord.medicalCode` |
| `item.examineNames` |
| `item.checkStatus` |
| `checkStatus` |
| `item.waitingSeconds` |
| `waitingTime` |
| `corpInfo.employeeTitle` |
| `item.medicalRecord.doctorName` |
| `item.waitingExamineList.length` |
| `item.examiningList.length` |
| `item.examinedList.length` |
| `iten.medicalExamine.id` |
| `iten.medicalExamine.examineName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `open1()` |
| `open2()` |
| `setId(item.medicalRecord.id)` |
| `goAssistChecking(item.examiningList,item.medicalRecord.id)` |
| `goAssistChecking(item.examinedList,item.medicalRecord.id)` |
| `savePatient(item.patient.id,item.medicalRecord.id)` |
| `hidePatient()` |

### 11.2 `assistChecking`

- **URL**：`/assistChecking?medicalExamineId&editable&medicalRecordId`
- **模板**：`views/assistCheckList/assistChecking.html`
- **控制器**：`assistCheckingCtrl`
- **端点数**：15

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeExamine` | `POST /admin/completeExamine.json` |
| `disconnectUartDeviceOfAdmin` | `POST /admin/disconnectUartDeviceOfAdmin.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getLatestUartDeviceLogToSchoolMateCheck` | `POST /admin/getLatestUartDeviceLogToSchoolMateCheck.json` |
| `getMedicalExamineItemVoList` | `POST /admin/getMedicalExamineItemVoList.json` |
| `getMedicalExamineVoList` | `POST /admin/getMedicalExamineVoList.json` |
| `getMedicalRecord` | `POST /admin/getMedicalRecord.json` |
| `getPatientExamineListVoList` | `POST /admin/getPatientExamineListVoList.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `getVisionRecordVo` | `POST /admin/getVisionRecordVo.json` |
| `modifyMedicalExamineItemList` | `POST /admin/modifyMedicalExamineItemList.json` |
| `selectUartDeviceByAdminId` | `POST /admin/selectUartDeviceByAdminId.json` |
| `selectUartDeviceList` | `POST /admin/selectUartDeviceList.json` |
| `setUartDeviceOfAdmin` | `POST /admin/setUartDeviceOfAdmin.json` |
| `uploadExamineResult` | `POST /admin/uploadExamineResult.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 检查结果 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.left` |
| `tagIdArray[innIndex]` |
| `item.right` |
| `iten.medicalExamine.checkDescription` |
| `iten.medicalExamine.checkComment` |
| `keyword` |
| `device.uartDeviceId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.medicalExamine.examineName` |
| `iten.medicalExamine.examineName` |
| `iten.medicalExamine` |
| `refundAndPayStatus` |
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
| `iten.medicalExamine.remark` |
| `index` |
| `item.leftName` |
| `item.left` |
| `val.checkItemValue` |
| `item.rightName` |
| `item.right` |
| `item` |
| `iten.medicalExamine.id` |
| `iten.medicalExamine.checkDescription` |
| `iten.medicalExamine.checkComment` |
| `selectUartDeviceVoFactory.result.object.deviceCode` |
| `iten.medicalExamine.checkStatus` |
| `checkStatus` |
| `item.patient.patientName` |
| `bigImgUrl` |
| `item.id` |
| `item.deviceCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `medical.idx=-1` |
| `back()` |
| `setMedicalExamineId(item.medicalExamine.id)` |
| `showTagModal(item.left,item.leftValueArr,$index,$event,` |
| `$event.stopPropagation()` |
| `insertTag($index,1)` |
| `showTagModal(item.right,item.rightValueArr,$index,$event,` |
| `insertTag($index,2)` |
| `bigImg(item)` |
| `deleteImg(outerIndex,innerIndex)` |
| `uploadimg($index,iten.medicalExamine.id)` |
| `showDeviceModal()` |
| `devoice()` |
| `saveCheck(iten.medicalExamine.checkDescription,iten.medicalExamine.checkComment,iten.medicalExamine.id,iten.getImgArray)` |
| `setStatus()` |
| `printJianchadan.print(iten.medicalExamine.id)` |
| `getMedicalRecord(iten.medicalExamine.id,item.medicalRecord.id)` |
| `hidePatient()` |
| `imgModal=false` |
| `cancelDoctor()` |
| `selectDevice()` |
| `saveData()` |

**下拉数据源（ng-options）**

```
x.checkItemValue as x.checkItemValue for x in item.leftValueArr
x.checkItemValue as x.checkItemValue for x in item.rightValueArr
```

### 11.3 `remindList`

- **URL**：`/remindList`
- **模板**：`views/assistCheckList/remindList.html`
- **控制器**：`remindListCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelFollowUp` | `POST /admin/cancelFollowUp.json` |
| `getAdminList` | `POST /admin/getAdminList.json` |
| `getLoginEmployee` | `POST /admin/getLoginEmployee.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectFollowUpVoList` | `POST /admin/selectFollowUpVoList.json` |
| `startExamine` | `POST /admin/startExamine.json` |

**表单标签**

| 标签 |
|---|
| 按计划执行时间 |
| 按创建时间 |
| 微信通知 |
| 短信通知 |
| 智能语音通知 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `searchCondition.createStartTime` |
| `searchCondition.createEndTime` |
| `searchCondition.planExcuteStartTime` |
| `searchCondition.planExcuteEndTime` |
| `searchCondition.excuteStartTime` |
| `searchCondition.excuteEndTime` |
| `searchCondition.keyword` |
| `sortName` |
| `searchStatus.useWechatStatus` |
| `searchStatus.useSmsStatus` |
| `searchStatus.useVoiceStatus` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.createAdmin.nickname` |
| `item.followUp.createTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.followUp.followUpStatus` |
| `filter_remind` |
| `item` |
| `filter_remind2` |
| `item.followUp.planExcuteTime` |
| `item.followUp.autoRemind` |
| `filter_autoRemind` |
| `item.followUp` |
| `followUpFilter` |
| `content` |
| `item.followUp.followUpResult` |
| `item.followUp.cancelReason` |
| `items.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addVisit()` |
| `openPop(` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab2(null)` |
| `setTab2(0)` |
| `setTab2(1)` |
| `changeSortType()` |
| `changeSortType(` |
| `remindVisit_look(item)` |
| `remindVisit(item,items)` |

### 11.4 `smsSet`

- **URL**：`/smsSet`
- **模板**：`views/assistCheckList/smsSet.html`
- **控制器**：`smsSetCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSchoolCheckConf` | `POST /admin/getSchoolCheckConf.json` |
| `saveSchoolCheckConfForTemplate` | `POST /admin/saveSchoolCheckConfForTemplate.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 选择 |
| 2 | 类型 |
| 3 | 内容 |
| 4 | 模板 |
| 5 | 选择 |
| 6 | 类型 |
| 7 | 内容 |
| 8 | 模板 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.name` |
| `item.info` |
| `item.id` |
| `item.notChoseInfo` |
| `item.smsTemplate.marketType` |
| `marketType` |
| `item.smsTemplate.title` |
| `item.smsTemplate.templateId` |
| `item.smsTemplate.example` |
| `item.voiceTemplate.marketType` |
| `item.voiceTemplate.title` |
| `item.voiceTemplate.ttsCode` |
| `item.voiceTemplate.example` |

**页面动作（ng-click）**

| 动作 |
|---|
| `groupInfo.click($index)` |
| `save()` |
| `addressInfo.click(item.status)` |
| `item.click()` |
| `startUse(item.smsTemplate,0)` |
| `unlock(item.smsTemplate,0)` |
| `startUse(item.voiceTemplate,1)` |
| `unlock(item.voiceTemplate,1)` |

**跳转到**：`cloudPrinterConfig`, `screenBackConfig`, `screenPromotionConfig`, `zhiShiBangConfig`
