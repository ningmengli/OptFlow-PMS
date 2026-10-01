# 32｜模块 orderManage 订单

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/orderManage/` |
| 中文名 | 订单 |
| 开发波次 | W5 |
| 页面数 | **1** |
| 端点数（去重） | **0** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `orderManage` | `/orderManage` | `views/orderManage/orderManage.html` | `orderManageCtrl` | 0 |

## §2 端点清单（去重 0 个）


## §3 逐页字段规格

### 32.1 `orderManage`

- **URL**：`/orderManage`
- **模板**：`views/orderManage/orderManage.html`
- **控制器**：`orderManageCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 全选 |
| 病历编号{{item.medicalRecord.medicalCode}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.doctorName` |
| `obj.optometrist` |
| `obj.firstVisitFrom` |
| `rightTimer` |
| `isAll` |
| `medicalRecordIdList[$index]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
| `item.okOrderRecord.medicalRecordId` |
| `item.medicalRecord.medicalCode` |
| `item.medicalRecord.firstVisit` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.medicalRecord.doctorName` |
| `item.visionRecord.optometrist` |
| `item.customer.customerName` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `item.patient.patientBirthday` |
| `howoldFilter` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `checkAll()` |
| `modify($event)` |
