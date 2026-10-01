# 22｜模块 customize 定制

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/customize/` |
| 中文名 | 定制 |
| 开发波次 | W5 |
| 页面数 | **2** |
| 端点数（去重） | **8** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `blueToothTransfer` | `/blueToothTransfer` | `views/customize/blueToothTransfer.html` | `blueToothTransferCtrl` | 5 |
| 2 | `detectionLog` | `/detectionLog` | `views/customize/detectionLog.html` | `detectionLogCtrl` | 4 |

## §2 端点清单（去重 8 个）

- `POST /admin/countSchoolMateCheckListOfSchoolPlan.json`
- `POST /admin/getDefaultSchoolPlanByAdminId.json`
- `POST /admin/reTransferOtherEyeCheckLogList.json`
- `POST /admin/saveOtherSystem.json`
- `POST /admin/selectOtherEyeCheckLogList.json`
- `POST /admin/selectOtherSystemByCorpId.json`
- `POST /admin/selectSchoolMateCheckSendLogVoList.json`
- `POST /admin/sendSchoolMateCheckListOfSchoolPlan.json`

## §3 逐页字段规格

### 22.1 `blueToothTransfer`

- **URL**：`/blueToothTransfer`
- **模板**：`views/customize/blueToothTransfer.html`
- **控制器**：`blueToothTransferCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `reTransferOtherEyeCheckLogList` | `POST /admin/reTransferOtherEyeCheckLogList.json` |
| `saveOtherSystem` | `POST /admin/saveOtherSystem.json` |
| `selectOtherEyeCheckLogList` | `POST /admin/selectOtherEyeCheckLogList.json` |
| `selectOtherSystemByCorpId` | `POST /admin/selectOtherSystemByCorpId.json` |
| `selectSchoolMateCheckSendLogVoList` | `POST /admin/selectSchoolMateCheckSendLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 记录ID |
| 2 | 祼眼视力(右\|左) |
| 3 | 戴镜视力(右\|左) |
| 4 | 戴镜类型 |
| 5 | 创建时间 |
| 6 | 状态 |
| 7 | 开始时间 |
| 8 | 结束时间 |
| 9 | 人员信息 |
| 10 | 发送内容 |
| 11 | 开始状态 |
| 12 | 结束状态 |
| 13 | 开始时间 |
| 14 | 结束时间 |
| 15 | 回执 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.endTime` |
| `startTime` |
| `rightTime` |
| `data.recordId` |
| `obj.keyword` |
| `thirdPartyVo.httpPostUrl` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `otherEyeCheckLogList.count` |
| `item.recordId` |
| `item.rightVision` |
| `item.leftVision` |
| `item.rightGlassedVision` |
| `item.leftGlassedVision` |
| `item.glassesType` |
| `glassesStatus` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.sendStatus` |
| `transferStatus` |
| `item.sendStartTime` |
| `item.sendEndTime` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.outRecordId` |
| `item.schoolMateCheckSendLog.content` |
| `item.schoolMateCheckSendLog.startStatus` |
| `powerStatus` |
| `startStatus` |
| `item.schoolMateCheckSendLog.endStatus` |
| `endStatus` |
| `item.schoolMateCheckSendLog.startTime` |
| `item.schoolMateCheckSendLog.endTime` |
| `item.schoolMateCheckSendLog.responseInfo` |
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `trigger(0)` |
| `trigger(1)` |
| `trigger(2)` |
| `reload()` |
| `selectOtherEyeCheckLogList(0,true)` |
| `open1()` |
| `open2()` |
| `setStatus(` |
| `updateThirdPartySystemIndex($index)` |
| `saveThirdPartyVo()` |

### 22.2 `detectionLog`

- **URL**：`/detectionLog`
- **模板**：`views/customize/detectionLog.html`
- **控制器**：`detectionLogCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `countSchoolMateCheckListOfSchoolPlan` | `POST /admin/countSchoolMateCheckListOfSchoolPlan.json` |
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `selectSchoolMateCheckSendLogVoList` | `POST /admin/selectSchoolMateCheckSendLogVoList.json` |
| `sendSchoolMateCheckListOfSchoolPlan` | `POST /admin/sendSchoolMateCheckListOfSchoolPlan.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 人员信息 |
| 2 | 发送内容 |
| 3 | 开始状态 |
| 4 | 结束状态 |
| 5 | 开始时间 |
| 6 | 结束时间 |
| 7 | 回执 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `startTime` |
| `rightTime` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getDefaultObjectFactory.result.object.planName` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.checkCode` |
| `item.schoolMateCheckSendLog.content` |
| `item.schoolMateCheckSendLog.startStatus` |
| `powerStatus` |
| `startStatus` |
| `item.schoolMateCheckSendLog.endStatus` |
| `endStatus` |
| `item.schoolMateCheckSendLog.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.schoolMateCheckSendLog.endTime` |
| `item.schoolMateCheckSendLog.responseInfo` |

**页面动作（ng-click）**

| 动作 |
|---|
| `anewTransfer()` |
| `open1()` |
| `open2()` |
| `setStatus(` |

**跳转到**：`schoolPlanList`
