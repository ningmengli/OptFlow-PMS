# 18｜模块 bookManage 预约叫号

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/bookManage/` |
| 中文名 | 预约叫号 |
| 开发波次 | W2 |
| 页面数 | **4** |
| 端点数（去重） | **14** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `appointOrder` | `/appointOrder` | `views/bookManage/appointOrder.html` | `appointOrderCtrl` | 3 |
| 2 | `bookDetail` | `/bookDetail?appointmentId` | `views/bookManage/bookDetail.html` | `bookDetailCtrl` | 0 |
| 3 | `bookManage` | `/bookManage` | `views/bookManage/bookManage.html` | `bookManageCtrl` | 11 |
| 4 | `bookSettings` | `/bookSettings` | `views/bookManage/bookSettings.html` | `bookSettingsCtrl` | 0 |

## §2 端点清单（去重 14 个）

- `POST /admin/confirmAppointment.json`
- `POST /admin/getAppointmentVo.json`
- `POST /admin/getCanBeDeliverySkuInListOfProduct.json`
- `POST /admin/getCashflowDeliveryVo.json`
- `POST /admin/getCorpAppointmentConf.json`
- `POST /admin/getMedicalProductMachineCenterVoList.json`
- `POST /admin/getMedicalRecordPayVo.json`
- `POST /admin/saveCorpAppointmentConf.json`
- `POST /admin/saveMedicalProductDeliveryCommentBatch.json`
- `POST /admin/saveMedicalProductStockBatch.json`
- `POST /admin/selectAppointmentVoList.json`
- `POST /admin/sendMedicalProductToMachineCenter.json`
- `POST /admin/statProductDeliveryStatusOfCashflow.json`
- `POST /admin/updateAppointCompanyRemark.json`

## §3 逐页字段规格

### 18.1 `appointOrder`

- **URL**：`/appointOrder`
- **模板**：`views/bookManage/appointOrder.html`
- **控制器**：`appointOrderCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `confirmAppointment` | `POST /admin/confirmAppointment.json` |
| `getAppointmentVo` | `POST /admin/getAppointmentVo.json` |
| `updateAppointCompanyRemark` | `POST /admin/updateAppointCompanyRemark.json` |

### 18.2 `bookDetail`

- **URL**：`/bookDetail?appointmentId`
- **模板**：`views/bookManage/bookDetail.html`
- **控制器**：`bookDetailCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 会员姓名: |
| 会员电话: |
| 预约类型: |
| 地址: |
| 预约时间: |
| 取消原因: |
| 状态: |
| 会员留言: |
| {{corpInfo. companyTitle}}备注: |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `getAppointmentObjectFactory.vo.appointment.companyRemark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getAppointmentObjectFactory.vo.appointment.personName` |
| `getAppointmentObjectFactory.vo.appointment.mobile` |
| `getAppointmentObjectFactory.vo.appointment.appointType` |
| `appointType` |
| `getAppointmentObjectFactory.vo.company.companyName` |
| `getAppointmentObjectFactory.vo.company.address` |
| `getAppointmentObjectFactory.vo.company.phone` |
| `getAppointmentObjectFactory.vo.appointment.custAddress` |
| `getAppointmentObjectFactory.vo.appointment.arriveTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `getAppointmentObjectFactory.vo.appointment.cancelReason` |
| `getAppointmentObjectFactory.vo.appointment.status` |
| `appointStatus` |
| `getAppointmentObjectFactory.vo.appointment.chiefComplaint` |
| `corpInfo.` |
| `companyTitle` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modifyRemark()` |
| `cofirmAppointment()` |

**跳转到**：`bookManage`

### 18.3 `bookManage`

- **URL**：`/bookManage`
- **模板**：`views/bookManage/bookManage.html`
- **控制器**：`bookManageCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCanBeDeliverySkuInListOfProduct` | `POST /admin/getCanBeDeliverySkuInListOfProduct.json` |
| `getCashflowDeliveryVo` | `POST /admin/getCashflowDeliveryVo.json` |
| `getCorpAppointmentConf` | `POST /admin/getCorpAppointmentConf.json` |
| `getMedicalProductMachineCenterVoList` | `POST /admin/getMedicalProductMachineCenterVoList.json` |
| `getMedicalRecordPayVo` | `POST /admin/getMedicalRecordPayVo.json` |
| `saveCorpAppointmentConf` | `POST /admin/saveCorpAppointmentConf.json` |
| `saveMedicalProductDeliveryCommentBatch` | `POST /admin/saveMedicalProductDeliveryCommentBatch.json` |
| `saveMedicalProductStockBatch` | `POST /admin/saveMedicalProductStockBatch.json` |
| `selectAppointmentVoList` | `POST /admin/selectAppointmentVoList.json` |
| `sendMedicalProductToMachineCenter` | `POST /admin/sendMedicalProductToMachineCenter.json` |
| `statProductDeliveryStatusOfCashflow` | `POST /admin/statProductDeliveryStatusOfCashflow.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `arriveTimeFrom` |
| `rightTimer` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.customer.customerName` |
| `item.company.address` |
| `item.appointment.custAddress` |
| `item.company.phone` |
| `item.appointment.appointType` |
| `appointType` |
| `item.appointment.arriveTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.appointment.status` |
| `appointStatus` |
| `item.company.companyName` |
| `item.appointment.personName` |
| `item.appointment.mobile` |
| `item.appointment.chiefComplaint` |
| `corpInfo.` |
| `companyTitle` |
| `item.appointment.companyRemark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(1,null)` |
| `setTab(2,1)` |
| `setTab(3,2)` |
| `setTab(5,4)` |
| `open1()` |
| `open2()` |
| `searcHosptalList()` |

**跳转到**：`bookSettings`

### 18.4 `bookSettings`

- **URL**：`/bookSettings`
- **模板**：`views/bookManage/bookSettings.html`
- **控制器**：`bookSettingsCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 管理员 |
| 管理员备份 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.smsAdminName` |
| `obj.smsMobile` |
| `obj.smsBackAdminName` |
| `obj.smsBackMobile` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**跳转到**：`bookManage`
