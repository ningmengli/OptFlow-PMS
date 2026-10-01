# 27｜模块 getGlassNotify 取镜通知

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/getGlassNotify/` |
| 中文名 | 取镜通知 |
| 开发波次 | W5 |
| 页面数 | **1** |
| 端点数（去重） | **2** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `getGlassNotifyList` | `/getGlassNotifyList` | `views/getGlassNotify/getGlassNotifyList.html` | `getGlassNotifyListCtrl` | 2 |

## §2 端点清单（去重 2 个）

- `POST /admin/getMedicalRecordListOfReceiveSms.json`
- `POST /admin/sendTakeMirrorNotice.json`

## §3 逐页字段规格

### 27.1 `getGlassNotifyList`

- **URL**：`/getGlassNotifyList`
- **模板**：`views/getGlassNotify/getGlassNotifyList.html`
- **控制器**：`getGlassNotifyListCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getMedicalRecordListOfReceiveSms` | `POST /admin/getMedicalRecordListOfReceiveSms.json` |
| `sendTakeMirrorNotice` | `POST /admin/sendTakeMirrorNotice.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `firstVisitFrom` |
| `rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.medicalRecord.medicalCode` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.receiveSmsLog.gmtCreate` |
| `item.receiveSmsLog.smsContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `sendmsg(item.medicalRecord.id,$index)` |

**跳转到**：`getGlassNotifyList`
