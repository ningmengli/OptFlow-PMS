# 19｜模块 visitManage 随访

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/visitManage/` |
| 中文名 | 随访 |
| 开发波次 | W7 |
| 页面数 | **2** |
| 端点数（去重） | **14** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addVisit` | `/remindList/addVisit?followUpId?patientId` | `views/visitManage/addVisit.html` | `addVisitCtrl` | 12 |
| 2 | `visitDetails` | `/remindList/visitDetails?followUpId&look` | `views/visitManage/visitDetails.html` | `visitDetailsCtrl` | 6 |

## §2 端点清单（去重 14 个）

- `POST /admin/createFollowUpArray.json`
- `POST /admin/excuteFollowUp.json`
- `POST /admin/getCustomerVo.json`
- `POST /admin/getFollowUpConf.json`
- `POST /admin/getFollowUpVo.json`
- `POST /admin/getLoginEmployeeVo.json`
- `POST /admin/getPatientInfo.json`
- `POST /admin/saveFollowUpConf.json`
- `POST /admin/selectCorpSmsTemplatePoolForScene.json`
- `POST /admin/selectCorpVoiceTemplatePoolForScene.json`
- `POST /admin/selectEmployeeVoListOfMyCompany.json`
- `POST /admin/selectFollowUpContentTemplateVoList.json`
- `POST /admin/selectFollowUpResultTemplateVoList.json`
- `POST /admin/updateFollowUp.json`

## §3 逐页字段规格

### 19.1 `addVisit`

- **URL**：`/remindList/addVisit?followUpId?patientId`
- **模板**：`views/visitManage/addVisit.html`
- **控制器**：`addVisitCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createFollowUpArray` | `POST /admin/createFollowUpArray.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getFollowUpConf` | `POST /admin/getFollowUpConf.json` |
| `getFollowUpVo` | `POST /admin/getFollowUpVo.json` |
| `getLoginEmployeeVo` | `POST /admin/getLoginEmployeeVo.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `saveFollowUpConf` | `POST /admin/saveFollowUpConf.json` |
| `selectCorpSmsTemplatePoolForScene` | `POST /admin/selectCorpSmsTemplatePoolForScene.json` |
| `selectCorpVoiceTemplatePoolForScene` | `POST /admin/selectCorpVoiceTemplatePoolForScene.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectFollowUpContentTemplateVoList` | `POST /admin/selectFollowUpContentTemplateVoList.json` |
| `updateFollowUp` | `POST /admin/updateFollowUp.json` |

**表单标签**

| 标签 |
|---|
| {{item.name}} |

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

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.startTime` |
| `visitCarryTimeList[0].startTime` |
| `visitInfo.visitContent` |
| `item.chose` |
| `wechatContent` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `updatePatientFactory.patientName` |
| `updatePatientFactory.patientGender` |
| `gender` |
| `updatePatientFactory.patientBirthday` |
| `howoldFilter` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `updatePatientFactory.linkMobile` |
| `hidePhone` |
| `item.name` |
| `item.info` |
| `item.smsTemplate.marketType` |
| `marketType` |
| `item.smsTemplate.title` |
| `item.smsTemplate.example` |
| `item.voiceTemplate.marketType` |
| `item.voiceTemplate.title` |
| `item.voiceTemplate.example` |
| `chosePerson.wechatSendName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `openStart($index)` |
| `addVisit()` |
| `subtractVisit($index)` |
| `openStart(0)` |
| `updateCarry(0)` |
| `updateCarry(1)` |
| `updateCarry(2)` |
| `choseComp(true,` |
| `addressInfo.click(item.status)` |
| `save()` |
| `startUse(` |
| `unlock(item.smsTemplate,0)` |
| `unlock(item.voiceTemplate,1)` |
| `chosePerson.setShow(true)` |
| `setDefaultOptions()` |

### 19.2 `visitDetails`

- **URL**：`/remindList/visitDetails?followUpId&look`
- **模板**：`views/visitManage/visitDetails.html`
- **控制器**：`visitDetailsCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `excuteFollowUp` | `POST /admin/excuteFollowUp.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getFollowUpVo` | `POST /admin/getFollowUpVo.json` |
| `getPatientInfo` | `POST /admin/getPatientInfo.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectFollowUpResultTemplateVoList` | `POST /admin/selectFollowUpResultTemplateVoList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `visitObj.startTime` |
| `visitObj.way` |
| `visitObj.visitContent` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `updatePatientFactory.patientName` |
| `updatePatientFactory.patientGender` |
| `gender` |
| `updatePatientFactory.patientBirthday` |
| `howoldFilter` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `updatePatientFactory.linkMobile` |
| `followInfo.followUp.createTime` |
| `followInfo.createAdmin.nickname` |
| `followInfo.followUp.excuteTime` |
| `followInfo.excuteDoctor.employeeName` |
| `followInfo.followUp.wechatContent` |
| `followInfo.followUp.smsContent` |
| `followInfo.followUp.voiceContent` |
| `followInfo.followUp.followUpChannelType` |
| `follow_up_channel_type2` |
| `followInfo.followUp.followUpContent` |
| `followInfo.followUp.followUpResult` |
| `modelName` |
| `visitObj.imgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `openStart()` |
| `choseComp(true)` |
| `visitObj.imgUrl=` |
| `save()` |
