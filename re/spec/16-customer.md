# 16｜模块 customer 客户

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/customer/` |
| 中文名 | 客户 |
| 开发波次 | W1 |
| 页面数 | **7** |
| 端点数（去重） | **15** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `report.analysis` | `/analysis` | `views/customer/analysis.html` | `analysisCtrl` | 0 |
| 2 | `report.analysis.conversionFunnel` | `/conversionFunnel` | `views/customer/conversionFunnel.html` | `conversionFunnelCtrl` | 4 |
| 3 | `followUp` | `/followUp` | `views/customer/followUp.html` | `followUpCtrl` | 3 |
| 4 | `report.analysis.followUpAnalysis` | `/followUpAnalysis` | `views/customer/followUpAnalysis.html` | `followUpAnalysisCtrl` | 2 |
| 5 | `followUpDetails` | `/followUpDetails?firstMedicalRecordId&patientId` | `views/customer/followUpDetails.html` | `followUpDetailsCtrl` | 2 |
| 6 | `report.analysis.profileAnalysis` | `/profileAnalysis` | `views/customer/profileAnalysis.html` | `profileAnalysisCtrl` | 4 |
| 7 | `report.analysis.rfmModel` | `/rfmModel` | `views/customer/rfmModel.html` | `rfmModelCtrl` | 4 |

## §2 端点清单（去重 15 个）

- `POST /admin/getCompanyListOfMine.json`
- `POST /admin/getDataMedicalRecordCourseDetail.json`
- `POST /admin/getMemberList.json`
- `POST /admin/selectCustomerFmStatDataList.json`
- `POST /admin/selectCustomerRfmVoList.json`
- `POST /admin/selectMedicalRecordCourseDataPage.json`
- `POST /admin/selectVisionRecordVoListOfCourse.json`
- `POST /admin/selectYmCustomerChannelTagDataList.json`
- `POST /admin/selectYmCustomerRStatDataList.json`
- `POST /admin/statCustomerFunnelData.json`
- `POST /admin/statCustomerPersonaData.json`
- `POST /admin/statCustomerRfmLabelData.json`
- `POST /admin/statLossCustomerChannelTagData.json`
- `POST /admin/statMedicalRecordCourseFollowUpData.json`
- `POST /admin/statValidDealCustomerChannelTagData.json`

## §3 逐页字段规格

### 16.1 `report.analysis`

- **URL**：`/analysis`
- **模板**：`views/customer/analysis.html`
- **控制器**：`analysisCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `ite.corpAdminHome.state` |
| `ite.corpAdminHome.stateName` |

### 16.2 `report.analysis.conversionFunnel`

- **URL**：`/conversionFunnel`
- **模板**：`views/customer/conversionFunnel.html`
- **控制器**：`conversionFunnelCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `statCustomerFunnelData` | `POST /admin/statCustomerFunnelData.json` |
| `statLossCustomerChannelTagData` | `POST /admin/statLossCustomerChannelTagData.json` |
| `statValidDealCustomerChannelTagData` | `POST /admin/statValidDealCustomerChannelTagData.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.createStartTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
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
| `cn.name` |
| `cn.value` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
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
| `setHasPhone()` |

### 16.3 `followUp`

- **URL**：`/followUp`
- **模板**：`views/customer/followUp.html`
- **控制器**：`followUpCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `selectMedicalRecordCourseDataPage` | `POST /admin/selectMedicalRecordCourseDataPage.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 首诊日期 |
| 2 | 档案编号 |
| 3 | 最近一次就诊日期 |
| 4 | 姓名 |
| 5 | 性别 |
| 6 | 手机号 |
| 7 | 当前年龄 |
| 8 | 会员类型 |
| 9 | 会员来源 |
| 10 | 转介绍人次 |
| 11 | 充值金额 |
| 12 | 接诊人 |
| 13 | 验配师 |
| 14 | 会员推荐人 |
| 15 | 成交人 |
| 16 | 维护人 |
| 17 | 戴镜状态 |
| 18 | 复查超期 |
| 19 | 换片超期 |
| 20 | 门店 |
| 21 | 备注 |
| 22 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.firstVisitStartTime` |
| `rightTimer` |
| `obj.lastVisitStartTime` |
| `rightTimer2` |
| `obj.nextVisitStartTime` |
| `rightTimer3` |
| `obj.nextChangeStartTime` |
| `rightTimer4` |
| `obj.keyword` |
| `obj.startAge` |
| `obj.endAge` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `count` |
| `over.name` |
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
| `item.firstMedicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.firstMedicalRecord.medicalCode` |
| `item.lastMedicalRecord.firstVisit` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.customer.linkMobile` |
| `item.member.memberName` |
| `item.channelTag.tagName` |
| `item.customerWallet.trueBalance` |
| `item.doctorOfFirstMr.employeeName` |
| `item.secondDoctorOfFirstMr.employeeName` |
| `item.introducer.name` |
| `item.dealdoneEmployee.employeeName` |
| `item.serviceEmployee.employeeName` |
| `item.patient.lossType` |
| `filterLossType` |
| `item.overdueReview` |
| `filterOverdueReview` |
| `item.overdueChange` |
| `item.companyOfFirstMr.companyName` |
| `item.firstMedicalRecord.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `overDue.click($index)` |
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
| `open1()` |
| `open2()` |
| `open3()` |
| `open4()` |
| `open5()` |
| `open6()` |
| `open7()` |
| `open8()` |
| `look(item)` |

**跳转到**：`analysis.conversionFunnel`

### 16.4 `report.analysis.followUpAnalysis`

- **URL**：`/followUpAnalysis`
- **模板**：`views/customer/followUpAnalysis.html`
- **控制器**：`followUpAnalysisCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `statMedicalRecordCourseFollowUpData` | `POST /admin/statMedicalRecordCourseFollowUpData.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 员工姓名 |
| 2 | 客户数 |
| 3 | 超期未复查记录数 |
| 4 | 超期未换片记录数 |
| 5 | 戴镜中患者数 |
| 6 | 停戴患者数 |
| 7 | 戴镜状态未记录患者数 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.firstVisitStartTime` |
| `obj.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `echart.name` |
| `f.name` |
| `f.followUpName` |
| `f.customerCount` |
| `f.overdueReviewRecordCount` |
| `f.overdueChangeRecordCount` |
| `f.wearingCount` |
| `f.stopWearCount` |
| `f.noRecordOfWearCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setHasPhone()` |
| `setFollowUpIndex($index)` |

### 16.5 `followUpDetails`

- **URL**：`/followUpDetails?firstMedicalRecordId&patientId`
- **模板**：`views/customer/followUpDetails.html`
- **控制器**：`followUpDetailsCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDataMedicalRecordCourseDetail` | `POST /admin/getDataMedicalRecordCourseDetail.json` |
| `selectVisionRecordVoListOfCourse` | `POST /admin/selectVisionRecordVoListOfCourse.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `patientInfo.patientName` |
| `patientInfo.patientGender` |
| `gender` |
| `patientInfo.patientBirthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `howoldMatecheck` |
| `customerInfo.customer.customerName` |
| `customerInfo.customer.linkMobile` |
| `customerInfo.dealdoneEmployee.employeeName` |
| `customerInfo.serviceEmployee.employeeName` |
| `record.name` |
| `record.value` |
| `record.unit` |
| `filterOverdueReview` |
| `item.medicalRecord.firstVisit` |
| `item.show` |
| `item.medicalRecord.doctorName` |
| `item.medicalRecord.hospitalName` |
| `ToChineseNumber` |
| `visionRecordVoListOfCourse.length` |
| `outerIndex` |
| `item.medicalRecord.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `setTab(1)` |
| `setTab(2)` |
| `toggle(outerIndex)` |

### 16.6 `report.analysis.profileAnalysis`

- **URL**：`/profileAnalysis`
- **模板**：`views/customer/profileAnalysis.html`
- **控制器**：`profileAnalysisCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectYmCustomerChannelTagDataList` | `POST /admin/selectYmCustomerChannelTagDataList.json` |
| `statCustomerPersonaData` | `POST /admin/statCustomerPersonaData.json` |
| `statCustomerRfmLabelData` | `POST /admin/statCustomerRfmLabelData.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `dc.name` |
| `dc.value` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setHasPhone()` |

### 16.7 `report.analysis.rfmModel`

- **URL**：`/rfmModel`
- **模板**：`views/customer/rfmModel.html`
- **控制器**：`rfmModelCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectCustomerFmStatDataList` | `POST /admin/selectCustomerFmStatDataList.json` |
| `selectCustomerRfmVoList` | `POST /admin/selectCustomerRfmVoList.json` |
| `selectYmCustomerRStatDataList` | `POST /admin/selectYmCustomerRStatDataList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 手机号 |
| 3 | R（最近消费距离月数） |
| 4 | F（消费频率） |
| 5 | M（累计消费金额） |
| 6 | 客户分类 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `rfm.customer.customerName` |
| `rfm.customer.linkMobile` |
| `rfm.orderMonths` |
| `rfm.orderCount` |
| `rfm.orderPrice` |
| `rfm.rfmLabel` |
| `filterRfmModel` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setHasPhone()` |
