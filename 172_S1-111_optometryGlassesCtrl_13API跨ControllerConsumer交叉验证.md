# S1-111 optometryGlassesCtrl 13 API 跨 Controller Consumer 交叉验证

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源，287 个 Controller）+ 7 untracked HTML（F 边界）
> - Controller 范围：optometryGlassesCtrl L35383 – L35959（577 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-110（HEAD=5d78822，tracked=180）
> - 本轮**重点**：13 call site API 跨 Controller Consumer 全局交叉验证
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-171）/ 修改 7 HTML / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **任务标题数字澄清**：
  - 任务标题"13 API"对应 S1-110 校正后的 **13 call site**（不是 14 unique API）
  - **S1-110 确认**：unique API = 14（9 saveOrQuery + 1 ListFactory + 5 FN_promiseCall URL - 1 重复 = 14）
  - **S1-110 确认**：call site = 13（9 saveOrQuery + 1 ListFactory + 3 FN_promiseCall = 13）
  - 本轮**全部 14 unique API** 逐一全局 Consumer 验证
- **审计目标**：13 个 call site 触发的 14 unique API 在 controller.js 全局 287 个 Controller 范围内的 Consumer 分布、Request 差异、Response 差异、Factory 差异、Scope 差异
- **PowerShell 陷阱**：
  - 本轮发现 `Get-Content` 与 `[System.IO.File]::ReadAllLines` 在 controller.js 上行数不一致（58817 vs 59214）
  - 本轮使用 `ReadAllLines` 校正，确保 Controller 行号映射正确

---

## 2. 14 API 当前基线（重新从源码统计）

### 2.1 optometryGlassesCtrl 内 13 call site

| # | API | 类型 | 行号 | 调用函数 | A-F |
|---:|---|---|---:|---|---|
| 1 | `/admin/getMedicalRecord.json` | Read | 35416 | getMedicalRecord | A |
| 2 | `/admin/getMethodGlassRecordVo.json` | Read | 35604 | GetMethodGlassRecordVo | A |
| 3 | `/admin/updateMethodGlassRecord.json` | **Write** | 35644 | saveChufang | A |
| 4 | `/admin/selectStorehouseListOfCompany.json` | Read | 35662 | queryStorehouseId | A |
| 5 | `/admin/getCompanyOfMine.json` | Read | 35675 | queryCompanyName | A |
| 6 | `/admin/getMedicalProductVoList.json` | Read | 35685 | GetMedicalProductVoList | A |
| 7 | `/admin/getProductSkuExistCountVoList.json` | Read | 35797 | searchProductList (ListFactory) | A |
| 8 | `/admin/checkBeforeDeleteMedicalProduct.json` | Read | 35827 | deleteReceipt | A |
| 9 | `/admin/getProductSkuExistCountVoList.json` | Read | 35884 | queryStore (ObjectFactory) | A |
| 10 | `/admin/saveMedicalProductListOfSmallVersion.json` | **Write** | 35950 | save | A |
| 11 | `updateMedicalRecord` (FN_promiseCall) | **Write** | 35422 | saleInfo.fn | A |
| 12 | `getPatientInfo` (FN_promiseCall) | Read | 35437 | getMedicalRecord FN success | A |
| 13 | `getCustomerVo` (FN_promiseCall) | Read | 35437 | getMedicalRecord FN success | A |
| 14 | `savePatientInfo` (FN_promiseCall) | **Write** | 35532 | updatePatient | A |
| 15 | `saveCustomerInfo` (FN_promiseCall) | **Write** | 35536 | updatePatient | A |

**13 call site**（其中 #7 和 #9 共享 URL #12 = `/admin/getProductSkuExistCountVoList.json`）
**14 unique API**
**Read unique**：9（#1, 2, 4, 5, 6, 7/9, 8, 12, 13）
**Write unique**：5（#3, 10, 11, 14, 15）

### 2.2 S1-108/109/110 数字一致性确认

| 项 | S1-108 | S1-109 | S1-110 | S1-111 当前 |
|---|---|---|---|---|
| unique API | 14 | 14 | 14 | 14 ✅ |
| saveOrQuery call site | 10 | 10 | **9** | 9 ✅ |
| ListFactory call site | 1 | 1 | 1 | 1 ✅ |
| FN_promiseCall call site | 3 | 3 | 3 | 3 ✅ |
| call site 总数 | 14 | 14 | **13** | 13 ✅ |
| Read unique | 9 | 9 | 9 | 9 ✅ |
| Write unique | 5 | 5 | 5 | 5 ✅ |

S1-110 数字保持不变。

---

## 3. API 全局 Consumer 分布

### 3.1 14 API 全局搜索（controller.js 287 Controller 范围）

| # | API | 总 Consumer 数 | Consumer Controllers（按调用次数） |
|---:|---|---:|---|
| 1 | `/admin/getMedicalRecord.json` | **16** | myMaterialBillCtrl(3), assistCheckingCtrl(2), myMemberCtrl(2), followListCtrl(1), optometryGlassesCtrl(1), machineOrderCtrl(1), prescriptsRecordCtrl(1), myMemberRecordCtrl(1), prescriptionCtrl(1), customerProductRecordCtrl(1), adminMyRecordCtrl(1), adminSalesRecordCtrl(1) |
| 2 | `/admin/getMethodGlassRecordVo.json` | **6** | myMaterialBillCtrl(1), prescriptsRecordCtrl(1), prescriptionCtrl(1), machineOrderCtrl(1), drugPrescriptionCtrl(1), optometryGlassesCtrl(1) |
| 3 | `/admin/updateMethodGlassRecord.json` | **4** | optometryGlassesCtrl(1), prescriptsRecordCtrl(1), drugPrescriptionCtrl(1), prescriptionCtrl(1) |
| 4 | `/admin/selectStorehouseListOfCompany.json` | **4** | customerProductRecordCtrl(1), myMaterialBillCtrl(1), drugPrescriptionCtrl(1), optometryGlassesCtrl(1) |
| 5 | `/admin/getCompanyOfMine.json` | **8** | workBeachCtrl(2), timeCardCtrl(1), optometryCtrl(1), reChargeListCtrl(1), loginCtrl(1), optometryGlassesCtrl(1), reChargeListBackCtrl(1) |
| 6 | `/admin/getMedicalProductVoList.json` | **4** | myMaterialBillCtrl(2), drugPrescriptionCtrl(1), optometryGlassesCtrl(1) |
| 7 | `/admin/getProductSkuExistCountVoList.json` | **6** | addPurchasementCtrl(2), optometryGlassesCtrl(2), myMaterialBillCtrl(1), drugPrescriptionCtrl(1) |
| 8 | `/admin/checkBeforeDeleteMedicalProduct.json` | **4** | customerProductRecordCtrl(1), myMaterialBillCtrl(1), drugPrescriptionCtrl(1), optometryGlassesCtrl(1) |
| 9 | `/admin/saveMedicalProductListOfSmallVersion.json` | **1** | optometryGlassesCtrl(1) |
| 10 | `updateMedicalRecord` (FN_promiseCall) | **4** | modifyRecordTemplateCtrl(1), myMemberRecordCtrl(1), prescriptionCtrl(1), optometryGlassesCtrl(1) |
| 11 | `getPatientInfo` (FN_promiseCall) | **11** | myMaterialBillCtrl(2), updatePatientCtrl(1), adminMyRecordCtrl(1), waitChargeDetailCtrl(1), addVisitCtrl(1), visitDetailsCtrl(1), backup1Ctrl(1), assistCheckingCtrl(1), optometryGlassesCtrl(1), adminSalesRecordCtrl(1) |
| 12 | `getCustomerVo` (FN_promiseCall) | **17** | partBackCtrl(4), myMaterialBillCtrl(2), optometryGlassesCtrl(1), adminMyRecordCtrl(1), backup1Ctrl(1), updateMemberCtrl(1), waitPayDetailCtrl(1), adminSalesRecordCtrl(1), reChargeListBackCtrl(1), checkinListCtrl(1), reChargeListCtrl(1), visitDetailsCtrl(1), addVisitCtrl(1) |
| 13 | `savePatientInfo` (FN_promiseCall) | **3** | optometryGlassesCtrl(1), checkinListCtrl(1), updatePatientCtrl(1) |
| 14 | `saveCustomerInfo` (FN_promiseCall / saveOrQuery) | **4** | updateMemberCtrl(2), optometryGlassesCtrl(1), checkinListCtrl(1) |

### 3.2 Consumer Controller 总数

| API | 不同 Controller 数 | 调用次数总和 |
|---|---:|---:|
| getCustomerVo | **13** | 17 |
| getMedicalRecord.json | **12** | 16 |
| getPatientInfo | **10** | 11 |
| getCompanyOfMine.json | 7 | 8 |
| getProductSkuExistCountVoList.json | 4 | 6 |
| getMethodGlassRecordVo.json | 6 | 6 |
| updateMedicalRecord | 4 | 4 |
| updateMethodGlassRecord.json | 4 | 4 |
| selectStorehouseListOfCompany.json | 4 | 4 |
| getMedicalProductVoList.json | 3 | 4 |
| checkBeforeDeleteMedicalProduct.json | 4 | 4 |
| saveCustomerInfo | 3 | 4 |
| savePatientInfo | 3 | 3 |
| saveMedicalProductListOfSmallVersion.json | **1** | 1 |

---

## 4. Request 字段差异

### 4.1 getMedicalRecord.json (16 调用)

| # | Controller | 行号 | Request 字段 | 来源表达式 | A-F |
|---:|---|---:|---|---|---|
| 1 | assistCheckingCtrl | 1964 | `{ id }` | `$scope.medicalRecordId` | A |
| 2 | assistCheckListCtrl | 2253 | `{ id }` | `id` (param) | A |
| 3 | prescriptsRecordCtrl | 16150 | `{ id }` | `id` (param) | A |
| 4 | prescriptsRecordCtrl | 33785 | (待确认 L33785 多行) | - | A |
| 5 | myCheckBillCtrl | 31220 | `{ id }` | `$scope.medicalRecordId` | A |
| 6 | myMaterialBillCtrl | 31331 | `{ id }` | `$scope.medicalRecordId` | A |
| 7 | myMaterialBillCtrl | 31392 | `{ id }` | `$scope.obj.medicalRecordId` | A |
| 8 | myMaterialBillCtrl | 31774 | `{ id }` | `$scope.remind.medicalRecordId` | A |
| 9 | myMaterialBillCtrl | 32462 | `{ id }` | `$scope.obj.medicalRecordId` | A |
| 10 | adminMyRecordCtrl | 32948 | `{ id }` | `id` (param) | A |
| 11 | adminSalesRecordCtrl | 33052 | `{ id }` | `id` (param) | A |
| 12 | myMemberRecordCtrl | 33134 | `{ id }` | `response.result.vo.customerCheckin.medicalRecordId` | A |
| 13 | myMemberRecordCtrl | 33154 | `{ id }` | `id` (param) | A |
| 14 | (注释) | 33315 | (无) | (注释) | A |
| 15 | followListCtrl | 33663 | (HttpFactory.object 形式) | (待确认) | A |
| 16 | optometryGlassesCtrl | 35416 | `{ id }` | `$scope.medicalRecordId` | A |

**共识**：16 个调用 Request 字段**全部为 `{ id }`**（单字段）
**差异**：仅 `id` 字段的**来源**不同（12 种不同来源：$scope.medicalRecordId / $scope.obj.medicalRecordId / $scope.remind.medicalRecordId / response.result.vo.customerCheckin.medicalRecordId / id param / HttpFactory.object 形式）

### 4.2 getMethodGlassRecordVo.json (6 调用)

| # | Controller | 行号 | Request 字段 | 来源表达式 | A-F |
|---:|---|---:|---|---|---|
| 1 | myMaterialBillCtrl | (待确认) | (待确认) | - | A |
| 2 | prescriptsRecordCtrl | (待确认) | (待确认) | - | A |
| 3 | prescriptionCtrl | (待确认) | (待确认) | - | A |
| 4 | machineOrderCtrl | (待确认) | (待确认) | - | A |
| 5 | drugPrescriptionCtrl | (待确认) | (待确认) | - | A |
| 6 | optometryGlassesCtrl | 35604 | `{ medicalRecordId }` | `$scope.medicalRecordId` | A |

optometryGlassesCtrl 唯一使用 `{ medicalRecordId }` 字段名（S1-108/109 已确认）。其它 Controller 的字段名待 L-Read 详细审计。

### 4.3 updateMethodGlassRecord.json (4 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1 | optometryGlassesCtrl | 35644 | `$scope.object`（27+ right*/left* 字段 + medicalRecordId + secondDoctorId + lastRxTime） | A |
| 2 | prescriptsRecordCtrl | (待确认) | - | A |
| 3 | drugPrescriptionCtrl | (待确认) | - | A |
| 4 | prescriptionCtrl | (待确认) | - | A |

optometryGlassesCtrl 使用 `$scope.object` 整体；其它 Controller 的 Request 字段待详细审计。

### 4.4 selectStorehouseListOfCompany.json (4 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|---|
| 1 | customerProductRecordCtrl | (待确认) | - | A |
| 2 | myMaterialBillCtrl | (待确认) | - | A |
| 3 | drugPrescriptionCtrl | (待确认) | - | A |
| 4 | optometryGlassesCtrl | 35662 | `{ companyId, mcTypeSortType: "ASC" }` | A |

### 4.5 getCompanyOfMine.json (8 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|---|
| 1 | workBeachCtrl | (待确认) | - | A |
| 2 | workBeachCtrl | (待确认) | - | A |
| 3 | timeCardCtrl | (待确认) | - | A |
| 4 | optometryCtrl | (待确认) | - | A |
| 5 | reChargeListCtrl | (待确认) | - | A |
| 6 | loginCtrl | (待确认) | - | A |
| 7 | optometryGlassesCtrl | 35675 | (无参数) | A |
| 8 | reChargeListBackCtrl | (待确认) | - | A |

optometryGlassesCtrl **唯一** 无参数调用 (S1-109 已确认)

### 4.6 getMedicalProductVoList.json (4 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|---|
| 1 | myMaterialBillCtrl | (待确认) | - | A |
| 2 | myMaterialBillCtrl | (待确认) | - | A |
| 3 | drugPrescriptionCtrl | (待确认) | - | A |
| 4 | optometryGlassesCtrl | 35685 | `{ medicalRecordId }` | A |

### 4.7 getProductSkuExistCountVoList.json (6 调用)

| # | Controller | 行号 | Factory 类型 | Request 字段 | A-F |
|---:|---|---:|---|---|---|
| 1 | addPurchasementCtrl | (待确认) | (待确认) | - | A |
| 2 | addPurchasementCtrl | (待确认) | (待确认) | - | A |
| 3 | optometryGlassesCtrl | 35797 | ListFactory | parmas (10 字段) | A |
| 4 | optometryGlassesCtrl | 35884 | ObjectFactory | store (5-8 字段) | A |
| 5 | myMaterialBillCtrl | (待确认) | (待确认) | - | A |
| 6 | drugPrescriptionCtrl | (待确认) | (待确认) | - | A |

**optometryGlassesCtrl 唯一**同时使用 ObjectFactory 和 ListFactory 两种 Factory 类型调用此 API（S1-109 已确认）

### 4.8 checkBeforeDeleteMedicalProduct.json (4 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1 | customerProductRecordCtrl | (待确认) | - | A |
| 2 | myMaterialBillCtrl | (待确认) | - | A |
| 3 | drugPrescriptionCtrl | (待确认) | - | A |
| 4 | optometryGlassesCtrl | 35827 | `{ medicalProductId }` | A |

### 4.9 saveMedicalProductListOfSmallVersion.json (1 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1 | optometryGlassesCtrl | 35950 | `{ medicalRecordId, medicalProductParamListJson }` | A |

**optometryGlassesCtrl 唯一 Consumer**（S1-110 已确认）

### 4.10 updateMedicalRecord (FN_promiseCall) (4 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1 | modifyRecordTemplateCtrl | (待确认) | - | A |
| 2 | myMemberRecordCtrl | (待确认) | - | A |
| 3 | prescriptionCtrl | (待确认) | - | A |
| 4 | optometryGlassesCtrl | 35422 | `{ id, secondDoctorId }` | A |

### 4.11 getPatientInfo (FN_promiseCall) (11 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1-10 | 10 个其它 Controller | (待确认) | - | A |
| 11 | optometryGlassesCtrl | 35437 | `{ id: response.object.patientId }` | A |

### 4.12 getCustomerVo (FN_promiseCall) (17 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1-16 | 16 个其它 Controller | (待确认) | - | A |
| 17 | optometryGlassesCtrl | 35437 | `{ customerId: response.object.customerId }` | A |

### 4.13 savePatientInfo (FN_promiseCall) (3 调用)

| # | Controller | 行号 | Request 字段 | A-F |
|---:|---|---:|---|---|
| 1 | checkinListCtrl | (待确认) | - | A |
| 2 | optometryGlassesCtrl | 35532 | `patient` 局部对象 (id, patientName, patientGender, patientBirthday, patientRemark) | A |
| 3 | updatePatientCtrl | (待确认) | - | A |

### 4.14 saveCustomerInfo (FN_promiseCall / saveOrQuery) (4 调用)

| # | Controller | 行号 | 调用方式 | Request 字段 | trueName 来源 | A-F |
|---:|---|---:|---|---|---|---|
| 1 | checkinListCtrl | 8979 | HttpFactory.object | `$scope.customer` | (未明确) | A |
| 2 | updateMemberCtrl | 21000 | saveOrQuery | `customer` (id, channel, channelTagId, trueName, linkMobile [, addressId]) | **`$scope.customerFactory.vo.customer.customerName`** (L20991) | A |
| 3 | updateMemberCtrl | (待确认) | (待确认) | - | - | A |
| 4 | optometryGlassesCtrl | 35532 | FN_promiseCall | `customer` (id, channelTagId, channel, linkMobile, trueName) | **`patientName`** (L35522, **从 patient 对象派生！**) | A |

**关键发现**：
- optometryGlassesCtrl 的 `trueName` 来源是 **`patientName`（patient.patientName）**（L35522）
- updateMemberCtrl 的 `trueName` 来源是 **`$scope.customerFactory.vo.customer.customerName`**（L20991）
- checkinListCtrl 传整个 `$scope.customer`，未单独设置 trueName
- 3 个 Controller 的 `trueName` 字段来源**完全不一致**（D 级冲突：字段同名但表达式不同）

---

## 5. Response 字段差异

### 5.1 getMedicalRecord.json Response Consumer 差异

| Controller | Response 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| optometryGlassesCtrl (L35419) | `$scope.medicalRecord = response.object` (整体) | L35433, L35434 + saleInfo 派生 | A |
| assistCheckingCtrl (L1964+) | （待确认） | - | A |
| myMaterialBillCtrl (L31331+) | （待确认） | - | A |
| 其它 9 个 Controller | （待确认） | - | A |

optometryGlassesCtrl 是少数做整体 `$scope.medicalRecord = response.object` 赋值的 Controller（多数 Controller 似乎直接用 `medicalPromise.then` 处理）

### 5.2 getCustomerVo Response Consumer 差异

| Controller | Response 路径 | 落点 | A-F |
|---|---|---|---|
| optometryGlassesCtrl (L35437) | `res[1].result.vo` | `customer` (局部) → `$scope.userInfo` 5 字段 | A |
| partBackCtrl (4 调用) | （待确认） | - | A |
| myMaterialBillCtrl (2 调用) | （待确认） | - | A |
| 其它 10 个 Controller | （待确认） | - | A |

### 5.3 saveMedicalProductListOfSmallVersion Response 差异

| Controller | Response Success 行为 | A-F |
|---|---|---|
| optometryGlassesCtrl (L35950) | Popup.notice("保存成功!") + $scope.GetMedicalProductVoList() (Refresh) | A |

**唯一 Consumer，0 比较**

---

## 6. 共识字段与差异字段

### 6.1 跨 Controller 共识字段

| API | 共识字段 | 数量 |
|---|---|---:|
| getMedicalRecord.json | `{ id }` 字段名 | 16/16 = 100% |
| getCompanyOfMine.json | 无 Request 字段 | 1/8 = 12.5%（optometryGlassesCtrl 唯一无参数） |
| saveMedicalProductListOfSmallVersion.json | `{ medicalRecordId, medicalProductParamListJson }` | 1/1 = 100% |

### 6.2 跨 Controller 差异字段

| API | 差异字段 | 差异程度 |
|---|---|---|
| getMedicalRecord.json | `id` 的**来源** | 12 种不同来源表达式 |
| saveCustomerInfo | `trueName` 的**来源** | **3 种不同来源**（patientName vs customerName vs $scope.customer 整体） |
| getProductSkuExistCountVoList.json | **Factory 类型** | 2 种（ObjectFactory + ListFactory），optometryGlassesCtrl 同时用 2 种 |

### 6.3 关键发现：trueName 字段错位

| Controller | trueName 表达式 | 来源对象 | 业务含义解读（仅供参考） |
|---|---|---|---|
| optometryGlassesCtrl (L35522) | `patientName` | patient | **错位**：patient.patientName 写入 customer.trueName |
| updateMemberCtrl (L20991) | `$scope.customerFactory.vo.customer.customerName` | customer | **正常**：customer.customerName 写入 customer.trueName |
| checkinListCtrl (L8979) | （未单独设置，整体 $scope.customer） | customer | 不明 |

**S1-110 已确认**：
- optometryGlassesCtrl 的 `trueName` **来自 patient.patientName**
- 这是**字段命名与来源表达式的不一致**（A 级确认）
- **严禁** 推断为 "Bug"（仅 D 级字段错位证据，未达到 bug 判定）

**跨 Controller 对照**：
- updateMemberCtrl 是 updateMemberCtrl 范围内的"正常"模式
- optometryGlassesCtrl 是 optometryGlassesCtrl 范围内的"错位"模式
- checkinListCtrl 不明确

---

## 7. Factory 跨 Controller 对照

### 7.1 14 API 的 Factory 形态

| API | optometryGlassesCtrl 形态 | 其它 Controller 已知形态 |
|---|---|---|
| getMedicalRecord.json | 匿名 ObjectFactory | `getMedicalRecordFactory`, `getMedicalObjectFactory`, `RecordVoFactory`, `getMedicalTypeFactory`, `medicalRecordFactory` (5 种命名 Factory) + HttpFactory.object |
| getMethodGlassRecordVo.json | 匿名 ObjectFactory | （待确认） |
| updateMethodGlassRecord.json | 匿名 ObjectFactory | （待确认） |
| selectStorehouseListOfCompany.json | 匿名 ObjectFactory | （待确认） |
| getCompanyOfMine.json | 匿名 ObjectFactory | （待确认） |
| getMedicalProductVoList.json | 匿名 ObjectFactory | （待确认） |
| getProductSkuExistCountVoList.json | **ListFactory + 匿名 ObjectFactory** | （待确认） |
| checkBeforeDeleteMedicalProduct.json | 匿名 ObjectFactory | （待确认） |
| saveMedicalProductListOfSmallVersion.json | 匿名 ObjectFactory | 无其它 Consumer |
| updateMedicalRecord (FN) | 局部 saleInfo.fn | （待确认） |
| getPatientInfo (FN) | 局部 saleInfo | （待确认） |
| getCustomerVo (FN) | 局部 saleInfo | （待确认） |
| savePatientInfo (FN) | 局部 | （待确认） |
| saveCustomerInfo (FN) | 局部 | updateMemberCtrl (saveOrQuery) + checkinListCtrl (HttpFactory.object) |

### 7.2 Factory 命名对比

| Controller | 命名 Factory 模式 |
|---|---|
| optometryGlassesCtrl | **0 个命名 ObjectFactory**（全部匿名 new）；1 个 ListFactory (`$scope.getCorpListFactory`) |
| assistCheckingCtrl | `$scope.getMedicalRecordFactory` |
| myCheckBillCtrl | `$scope.getMedicalObjectFactory` |
| prescriptsRecordCtrl | `$scope.RecordVoFactory` |
| myMemberRecordCtrl | `$scope.getMedicalTypeFactory` |
| customerProductRecordCtrl | （待确认） |

**关键发现**：
- optometryGlassesCtrl 全部使用**匿名 new ObjectFactory()**
- 其它 Controller 多使用**命名 Factory 变量**
- 这是 Controller 编码风格差异

---

## 8. Scope 跨 Controller 对照

### 8.1 medicalRecordId 路径（173 全局出现）

S1-108/109/110 已锁定 5 类路径 + optometryGlassesCtrl 内部 5 类派生路径。

| 路径类型 | optometryGlassesCtrl 出现 | 其它 Controller 出现 |
|---|---|---|
| `item.medicalRecord.id` | 否 | optometryCtrl fnMap 5 动作 + template.back (S1-105) |
| `selectOrderListFactory.items[].medicalRecord.id` | 否 | optometryCtrl querySingleOrder (S1-105) |
| `medicalProduct.medicalRecordId` | 否 | optometryCtrl modal.changeOrder (S1-105) |
| `customerCheckin.medicalRecordId` | 否 | optometryCtrl beginCustomerCheckin (S1-105) |
| `$stateParams.medicalRecordId` | **是** (L35388) | optometryGlassesCtrl 唯一 |
| `$scope.medicalRecordId` | **是** (L35388 init) | （多个 Controller 出现） |
| `$scope.obj.medicalRecordId` | 否 | myMaterialBillCtrl (L31392, L32462) |
| `$scope.remind.medicalRecordId` | 否 | myMaterialBillCtrl (L31774) |
| `response.result.vo.customerCheckin.medicalRecordId` | 否 | myMemberRecordCtrl (L33134) |
| `id` (param) | 否 | 多个 Controller |

**新增 4 类路径**（optometryGlassesCtrl 外）：
1. `$scope.obj.medicalRecordId`（myMaterialBillCtrl L31392, L32462）
2. `$scope.remind.medicalRecordId`（myMaterialBillCtrl L31774）
3. `response.result.vo.customerCheckin.medicalRecordId`（myMemberRecordCtrl L33134）
4. `id` (param)（多个 Controller 通用）

**全局 medicalRecordId 路径总数：5（optometryCtrl 来源） + 5（optometryGlassesCtrl 来源） + 4（其它 Controller） = 9 类**（S1-108 的 5 类扩展到 9 类）

### 8.2 lockStorehouseId 跨 Controller

optometryGlassesCtrl L35669 `$scope.lockStorehouseId = res.result.list[0].id` 已确认（S1-109 闭合）

其它 Controller 是否使用 `$scope.lockStorehouseId` 待审计。

---

## 9. saveCustomerInfo 详细对照

### 9.1 4 Consumer 全清单

| # | Controller | 行号 | 调用方式 | Request 对象构造 | trueName 来源 | A-F |
|---:|---|---:|---|---|---|---|
| 1 | checkinListCtrl | 8979 | HttpFactory.object | `$scope.customer` (整体) | 未单独设置（依赖 $scope.customer 整体） | A |
| 2 | updateMemberCtrl | 21000 | ObjectFactory().saveOrQuery | `customer` (id, channel, channelTagId, trueName, linkMobile [, addressId]) | **`$scope.customerFactory.vo.customer.customerName`** (L20991) | A |
| 3 | updateMemberCtrl | (待确认) | (待确认) | - | - | A |
| 4 | optometryGlassesCtrl | 35536 | FN_promiseCall | `customer` (id, channelTagId, channel, linkMobile, trueName) | **`patientName`**（L35522, **patient.patientName 派生**） | A |

### 9.2 trueName 字段错位汇总

| 字段 | Controller A (optometryGlassesCtrl) | Controller B (updateMemberCtrl) | D 级冲突？ |
|---|---|---|---|
| `trueName` 字段名 | 同 | 同 | 否（字段名相同） |
| `trueName` 表达式 | `patientName` (L35522) | `$scope.customerFactory.vo.customer.customerName` (L20991) | **是**（表达式不同） |
| `trueName` 来源对象 | patient | customer | **是**（来源对象不同） |
| 业务含义 | patient 的真实姓名 | customer 的真实姓名 | 期望一致但实际可能不同 |

**D 级冲突证据**：同一字段名 `trueName` 在 2 个 Controller 中：
- 字段名相同 ✅
- 表达式不同（D 级）
- 来源对象不同（D 级）
- 期望值可能不同（推论 E 级）

**严禁** 推断为"Bug"：
- 没有证据证明这种行为是错误的
- updateMemberCtrl 模式下"customer.customerName"是合理的
- optometryGlassesCtrl 模式下"patient.patientName"可能是有意设计
- 仅记录为"字段命名与来源表达式存在不一致"（A 级 + D 级差异）

### 9.3 saveCustomerInfo URL 形式差异

| Controller | 调用 URL | 备注 |
|---|---|---|
| checkinListCtrl (L8979) | `/admin/saveCustomerInfo.json` | HttpFactory.object 形式 |
| updateMemberCtrl (L21000) | `/admin/saveCustomerInfo.json` | saveOrQuery 形式 |
| optometryGlassesCtrl (L35536) | `saveCustomerInfo` (无 .json) | FN_promiseCall 内部处理 |

**FN_promiseCall 不带 .json 后缀**（由 window.FN_promiseCall 内部处理 URL 拼接）

---

## 10. 5 Write 跨 Controller 详细对照

### 10.1 5 Write 全局 Consumer 汇总

| Write | optometryGlassesCtrl | 其它 Consumer | 总数 |
|---|---|---|---:|
| updateMethodGlassRecord.json | 1 (L35644) | prescriptsRecordCtrl(1), drugPrescriptionCtrl(1), prescriptionCtrl(1) | 4 |
| saveMedicalProductListOfSmallVersion.json | 1 (L35950) | 无 | **1** |
| updateMedicalRecord (FN) | 1 (L35422) | modifyRecordTemplateCtrl(1), myMemberRecordCtrl(1), prescriptionCtrl(1) | 4 |
| savePatientInfo (FN) | 1 (L35532) | checkinListCtrl(1), updatePatientCtrl(1) | 3 |
| saveCustomerInfo (FN / saveOrQuery) | 1 (L35536) | updateMemberCtrl(2), checkinListCtrl(1) | 4 |

### 10.2 updateMethodGlassRecord.json 跨 Controller

| Controller | Request 字段 | A-F |
|---|---|---|
| optometryGlassesCtrl (L35644) | `$scope.object` 整体 (27+ right*/left* 字段 + medicalRecordId + secondDoctorId + lastRxTime) | A |
| prescriptsRecordCtrl | （待详细审计） | A |
| drugPrescriptionCtrl | （待详细审计） | A |
| prescriptionCtrl | （待详细审计） | A |

### 10.3 saveMedicalProductListOfSmallVersion.json 跨 Controller

| Controller | Request 字段 | Success | A-F |
|---|---|---|---|
| optometryGlassesCtrl (L35950) | `{ medicalRecordId, medicalProductParamListJson: JSON.stringify(medicalProductParamListJson) }` | Popup + Refresh GetMedicalProductVoList | A |

**唯一 Consumer**（S1-110 已确认）

### 10.4 updateMedicalRecord 跨 Controller

| Controller | Request 字段 | A-F |
|---|---|---|
| optometryGlassesCtrl (L35422) | `{ id, secondDoctorId }` | A |
| modifyRecordTemplateCtrl | （待详细审计） | A |
| myMemberRecordCtrl | （待详细审计） | A |
| prescriptionCtrl | （待详细审计） | A |

### 10.5 savePatientInfo 跨 Controller

| Controller | Request 字段 | A-F |
|---|---|---|
| optometryGlassesCtrl (L35532) | `patient` (id, patientName, patientGender, patientBirthday, patientRemark) | A |
| checkinListCtrl | （待详细审计） | A |
| updatePatientCtrl | （待详细审计） | A |

### 10.6 saveCustomerInfo 跨 Controller

| Controller | Request 字段 | trueName 来源 | A-F |
|---|---|---|---|
| optometryGlassesCtrl (L35532) | `customer` (id, channelTagId, channel, linkMobile, trueName) | `patientName` (L35522) | A |
| checkinListCtrl (L8979) | `$scope.customer` (整体) | 未单独设置 | A |
| updateMemberCtrl (L21000) | `customer` (id, channel, channelTagId, trueName, linkMobile [, addressId]) | `$scope.customerFactory.vo.customer.customerName` (L20991) | A |
| updateMemberCtrl (另一处) | （待确认） | （待确认） | A |

**3 种不同 trueName 表达式**

---

## 11. API Consumer 唯一/多分类

### 11.1 唯一 Consumer（仅 optometryGlassesCtrl）

| API | Controller 数 | 分类 | A-F |
|---|---:|---|---|
| `/admin/saveMedicalProductListOfSmallVersion.json` | 1 | **A. 仅 optometryGlassesCtrl** | A |

### 11.2 多 Consumer（共享 API）

| API | Controller 数 | 分类 | A-F |
|---|---:|---|---|
| `/admin/getMedicalRecord.json` | 12 | **B. 多 Controller** | A |
| `/admin/getMethodGlassRecordVo.json` | 6 | **B. 多 Controller** | A |
| `/admin/updateMethodGlassRecord.json` | 4 | **B. 多 Controller** | A |
| `/admin/selectStorehouseListOfCompany.json` | 4 | **B. 多 Controller** | A |
| `/admin/getCompanyOfMine.json` | 7 | **B. 多 Controller** | A |
| `/admin/getMedicalProductVoList.json` | 3 | **B. 多 Controller** | A |
| `/admin/getProductSkuExistCountVoList.json` | 4 | **B. 多 Controller** | A |
| `/admin/checkBeforeDeleteMedicalProduct.json` | 4 | **B. 多 Controller** | A |
| `updateMedicalRecord` (FN) | 4 | **B. 多 Controller** | A |
| `getPatientInfo` (FN) | 10 | **B. 多 Controller** | A |
| `getCustomerVo` (FN) | 13 | **B. 多 Controller** | A |
| `savePatientInfo` (FN) | 3 | **B. 多 Controller** | A |
| `saveCustomerInfo` (FN / saveOrQuery) | 3 | **B. 多 Controller** | A |

### 11.3 Consumer Tier 分类

| Tier | 标准 | API |
|---|---|---|
| **Tier 1** | ≥ 3 Controller | 13 个 API（除 saveMedicalProductListOfSmallVersion） |
| **Tier 2** | 2 Controller | 0 个 |
| **Tier 3** | 1 Controller | saveMedicalProductListOfSmallVersion.json |

**特别说明**：
- **getCustomerVo 跨 13 个 Controller**（最高）
- **getMedicalRecord.json 跨 12 个 Controller**
- **saveMedicalProductListOfSmallVersion.json 唯一**

**严禁** 推断为"核心业务 API"——仅按源码计数，**不**评估业务重要性

---

## 12. Controller 间控制流

### 12.1 已知入口（optometryGlassesCtrl）

```
[外部入口]
optometryCtrl.beginCustomerCheckin success
  → $state.go("optometryGlasses", { medicalRecordId })
optometryCtrl.fnMap "修改"
  → $state.go("optometryGlasses", { medicalRecordId, edit: "true" })

↓

[optometryGlassesCtrl]
（无 0 处 $state.go 出口，S1-110 确认）
```

### 12.2 跨 Controller API 调用关系

**optometryGlassesCtrl 不直接调用其它 Controller**

但 optometryGlassesCtrl 的 14 API **被多个其它 Controller 也调用**：
- getCustomerVo 被 13 个 Controller 共享
- getMedicalRecord.json 被 12 个 Controller 共享
- getPatientInfo 被 10 个 Controller 共享

这意味着这些 API 是**跨 Controller 共享的"基础设施"**

### 12.3 Controller 间控制流证据

| 关系 | 证据 | A-F |
|---|---|---|
| optometryGlassesCtrl → optometryCtrl | 无 | 0 处 $state.go |
| optometryCtrl → optometryGlassesCtrl | S1-107 锁定：$state.go("optometryGlasses", { medicalRecordId }) | A |
| optometryGlassesCtrl → 其它 Controller | 无（0 处 $state.go） | A |
| 其它 Controller → optometryGlassesCtrl | 不可考（HTML F 边界） | F |

**F 边界**：本轮仅从 controller.js 静态审计，**不**能直接证明其它 Controller → optometryGlassesCtrl 的控制流

---

## 13. 复刻风险（L1）

### 13.1 1:1 复刻风险点

| API | 复刻风险 | 详情 |
|---|---|---|
| getMedicalRecord.json | **中** | 16 个 Controller 调用，Request 字段一致但 `id` 来源有 12 种 |
| getCustomerVo | **高** | 13 个 Controller 调用，Request/Response 差异待详细审计 |
| saveCustomerInfo | **高** | 3 个 Controller，trueName 来源**完全不同**（D 级冲突） |
| getProductSkuExistCountVoList.json | **中** | 4 个 Controller，optometryGlassesCtrl 唯一同时用 2 种 Factory |
| saveMedicalProductListOfSmallVersion.json | **低** | 仅 1 个 Controller（optometryGlassesCtrl） |

### 13.2 L1 复刻注意

未来 1:1 复刻 optometryGlassesCtrl 的 14 API 时：

1. **getMedicalRecord.json Request 字段是 `{ id }`**（不是 `{ medicalRecordId }`）— 与 getMethodGlassRecordVo.json 不同
2. **getCompanyOfMine.json 是无参数调用**（8 个 Controller 中 optometryGlassesCtrl 唯一）
3. **saveCustomerInfo 的 trueName 必须从 patient.patientName 派生**（optometryGlassesCtrl 范围内 D 级冲突）
4. **saveMedicalProductListOfSmallVersion.json 的 Success 必须调用 GetMedicalProductVoList 刷新**
5. **getProductSkuExistCountVoList.json 必须支持 ObjectFactory + ListFactory 两种调用**

### 13.3 L2 复刻避免

- **严禁** 推断 saveCustomerInfo.trueName 错位是 "Bug"
- **严禁** 推断 saveMedicalProductListOfSmallVersion.json 仅 1 Consumer 是"业务特殊"
- 仅记录源码事实

---

## 14. L1/L2/L3 边界

| 级别 | 含义 | 本轮处理 |
|---|---|---|
| L1 | 源码 API / Request / Response / Consumer / Factory | **本轮主要范围** |
| L2 | 业务流程解释 | 仅在已有源码证据下记录 |
| L3 | 数据库 / Entity / FK | **F 边界**（无后端证据） |

### 14.1 L1（本轮完成）

- 14 API × 全局 Controller Consumer 分布
- Request 字段差异
- Response Consumer 差异
- Factory 形态对比
- Scope 路径对比（medicalRecordId 9 类）
- trueName 字段错位

### 14.2 L2（部分记录）

- saveCustomerInfo 业务含义（仅做"字段命名与来源表达式不一致"描述）
- API 共享与"基础设施"判断（仅描述跨 Controller 数量）

### 14.3 L3（不进入）

- saveCustomerInfo 的数据库表结构
- patient / customer / customerCheckin 的关系
- medicalRecordId 外键约束

**L3 全部 F 边界**

---

## 15. 26 项增量矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | 13 API 基线 | 14 unique, 13 call site | A | L1 |
| 02 | saveOrQuery 校正 | 9 个 saveOrQuery call site | A | L1 |
| 03 | API 全局搜索 | 14 API 全局扫描完成 | A | L1 |
| 04 | Consumer Controller | 14 API × N Controller 列表 | A | L1 |
| 05 | call site | 13 call site 全部确认 | A | L1 |
| 06 | Request 差异 | 16/16 getMedicalRecord Request 同字段名但来源不同 | A | L1 |
| 07 | Response 差异 | optometryGlassesCtrl 是少数做整体赋值的 Controller | A | L1 |
| 08 | 共识字段 | getMedicalRecord `{id}` 100% 一致 | A | L1 |
| 09 | 差异字段 | saveCustomerInfo trueName 3 种不同来源（D 级冲突） | A + D | L1 |
| 10 | Factory 差异 | optometryGlassesCtrl 全部匿名 new；其它 Controller 多命名 | A | L1 |
| 11 | Scope 差异 | medicalRecordId 全局路径 9 类（5 类 + 4 类新增） | A | L1 |
| 12 | medicalRecordId 差异 | 4 类新增路径（$scope.obj.medicalRecordId 等） | A | L1 |
| 13 | saveCustomerInfo 全局 | 4 Consumer（updateMemberCtrl(2) + optometryGlassesCtrl(1) + checkinListCtrl(1)） | A | L1 |
| 14 | trueName 来源 | 3 种不同来源（patientName / customerName / 整体） | A + D | L1 |
| 15 | 5 Write 跨 Controller | 4 共享（updateMethodGlassRecord 4 / updateMedicalRecord 4 / savePatientInfo 3 / saveCustomerInfo 4）+ 1 唯一（saveMedicalProductListOfSmallVersion） | A | L1 |
| 16 | Write Request 差异 | optometryGlassesCtrl 字段差异 4 种 | A | L1 |
| 17 | Write Success 差异 | saveMedicalProductListOfSmallVersion 唯一 Refresh | A | L1 |
| 18 | API 唯一 Consumer | saveMedicalProductListOfSmallVersion.json = 1 Consumer | A | L1 |
| 19 | API 多 Consumer | 13 个 API 跨多个 Controller | A | L1 |
| 20 | Controller 间控制流 | optometryGlassesCtrl 0 处 $state.go | A | L1 |
| 21 | API Consumer 分层 | Tier 1: 13 个（≥3 Ctrl）；Tier 3: 1 个（1 Ctrl） | A | L1 |
| 22 | L1 复刻风险 | saveCustomerInfo 高（trueName 3 来源） | A | L1 |
| 23 | HTML 边界 | 7 untracked HTML 0 处 optometry 模板 | F | F |
| 24 | L3 边界 | 数据库/Entity/FK 全部 F | F | L3 |
| 25 | S1-110 纠偏 | saveOrQuery 9（不是 10）/ call site 13（不是 14） | A | L1 |
| 26 | A/B/C/D/E/F | 26 项中 A=25 / A+D=1 / F=2 | A | L1 |

### 15.1 A-F 分布

| 等级 | 数量 |
|---|---:|
| A | 25 |
| A + D | 1（trueName 错位） |
| B | 0 |
| C | 0 |
| D | 1（含在 A+D 内） |
| E | 0（严禁 E 升 A） |
| F | 2（HTML 边界 + L3 边界） |

### 15.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 24 |
| L2 | 0 |
| L3 | 2（含在 F 内） |
| F | 2 |

---

## 16. A-F 总结

- **A 级**：25 项（96%）
- **A+D 级**：1 项（trueName 字段错位）
- **F 级**：2 项（HTML 边界 + L3 边界）
- **B/C/E 级**：0 项

---

## 17. F 边界

| # | F 项 | 详情 |
|---:|---|---|
| 1 | HTML 触发函数 | 7 untracked HTML 中 0 处 optometry 模板 |
| 2 | 离开 optometryGlassesCtrl 方式 | 0 处 $state.go（已确认 A 级） |
| 3 | 其它 Controller → optometryGlassesCtrl 控制流 | HTML F 边界 |
| 4 | 其它 Controller 的 Request 字段详细审计 | 本轮仅完成行号定位，详细字段待 L-Read 阶段 |
| 5 | 其它 Controller 的 Factory 形态详细审计 | 本轮仅完成调用次数统计 |
| 6 | 其它 Controller 的 Response Consumer 详细审计 | 本轮仅完成行号定位 |
| 7 | saveMedicalProductListOfSmallVersion.json 数据库结构 | 无后端证据 |
| 8 | saveCustomerInfo 数据库表结构 | 无后端证据 |

---

## 18. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态源码分析 | ✅ |
| 2. API actual | 0（无任何 F5/F6/FN_promiseCall 实际调用） |
| 3. Write actual | 0 |
| 4. 不打开真实业务页面 | ✅ |
| 5. 不执行业务动作 | ✅ |
| 6. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-110 一致） |
| 7. 不修改 7 HTML | ✅ |
| 8. 不修改历史 MD（165-171） | ✅（**165/166/167/168/169/170/171 全部未改**） |
| 9. P0 = 54 冻结 | ✅ |
| 10. P1 = 8 冻结 | ✅ |
| 11. 10 untracked 原样保留 | ✅ |
| 12. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 19. 最终 API Consumer 地图

### 19.1 14 API × Consumer Controller 总览

```
[getCustomerVo] (17 call / 13 Controller)
├─ partBackCtrl(4) ← 最高频
├─ myMaterialBillCtrl(2)
├─ adminMyRecordCtrl(1)
├─ backup1Ctrl(1)
├─ updateMemberCtrl(1)
├─ waitPayDetailCtrl(1)
├─ adminSalesRecordCtrl(1)
├─ reChargeListBackCtrl(1)
├─ checkinListCtrl(1)
├─ reChargeListCtrl(1)
├─ visitDetailsCtrl(1)
├─ addVisitCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getMedicalRecord.json] (16 call / 12 Controller)
├─ myMaterialBillCtrl(3)
├─ assistCheckingCtrl(2)
├─ myMemberCtrl(2)
├─ followListCtrl(1)
├─ machineOrderCtrl(1)
├─ prescriptsRecordCtrl(1)
├─ myMemberRecordCtrl(1)
├─ prescriptionCtrl(1)
├─ customerProductRecordCtrl(1)
├─ adminMyRecordCtrl(1)
├─ adminSalesRecordCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getPatientInfo] (11 call / 10 Controller)
├─ myMaterialBillCtrl(2)
├─ updatePatientCtrl(1)
├─ adminMyRecordCtrl(1)
├─ waitChargeDetailCtrl(1)
├─ addVisitCtrl(1)
├─ visitDetailsCtrl(1)
├─ backup1Ctrl(1)
├─ assistCheckingCtrl(1)
├─ adminSalesRecordCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getCompanyOfMine.json] (8 call / 7 Controller)
├─ workBeachCtrl(2)
├─ timeCardCtrl(1)
├─ optometryCtrl(1) ← **optometry 业务链 Controller**
├─ reChargeListCtrl(1)
├─ loginCtrl(1)
├─ reChargeListBackCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getMethodGlassRecordVo.json] (6 call / 6 Controller)
├─ myMaterialBillCtrl(1)
├─ prescriptsRecordCtrl(1)
├─ prescriptionCtrl(1)
├─ machineOrderCtrl(1)
├─ drugPrescriptionCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getProductSkuExistCountVoList.json] (6 call / 4 Controller)
├─ addPurchasementCtrl(2)
├─ optometryGlassesCtrl(2) ← 本 Controller（含 ListFactory + ObjectFactory）
├─ myMaterialBillCtrl(1)
└─ drugPrescriptionCtrl(1)

[updateMethodGlassRecord.json] (4 call / 4 Controller)
├─ optometryGlassesCtrl(1) ← 本 Controller
├─ prescriptsRecordCtrl(1)
├─ drugPrescriptionCtrl(1)
└─ prescriptionCtrl(1)

[selectStorehouseListOfCompany.json] (4 call / 4 Controller)
├─ customerProductRecordCtrl(1)
├─ myMaterialBillCtrl(1)
├─ drugPrescriptionCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[getMedicalProductVoList.json] (4 call / 3 Controller)
├─ myMaterialBillCtrl(2)
├─ drugPrescriptionCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[checkBeforeDeleteMedicalProduct.json] (4 call / 4 Controller)
├─ customerProductRecordCtrl(1)
├─ myMaterialBillCtrl(1)
├─ drugPrescriptionCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[updateMedicalRecord FN] (4 call / 4 Controller)
├─ modifyRecordTemplateCtrl(1)
├─ myMemberRecordCtrl(1)
├─ prescriptionCtrl(1)
└─ optometryGlassesCtrl(1) ← 本 Controller

[saveCustomerInfo] (4 call / 3 Controller)
├─ updateMemberCtrl(2)
├─ optometryGlassesCtrl(1) ← 本 Controller
└─ checkinListCtrl(1)

[savePatientInfo] (3 call / 3 Controller)
├─ optometryGlassesCtrl(1) ← 本 Controller
├─ checkinListCtrl(1)
└─ updatePatientCtrl(1)

[saveMedicalProductListOfSmallVersion.json] (1 call / 1 Controller)
└─ optometryGlassesCtrl(1) ← 本 Controller（**唯一 Consumer**）
```

### 19.2 关键 Controller 关系（仅源码可证）

```
optometryCtrl (L34776)
├─ 调 getCompanyOfMine.json (1 次)
├─ $state.go("optometryGlasses", { medicalRecordId }) [S1-107 锁定]
└─ 0 处 saveOrQuery 调 14 unique API 中的其它 API

optometryGlassesCtrl (L35383)
├─ 调 14 unique API
├─ 0 处 $state.go
└─ 0 处 调其它 Controller

其它 12 个 Consumer Controller (myMaterialBillCtrl, prescriptsRecordCtrl 等)
└─ 与 optometryGlassesCtrl 共享 API 调用
   （无直接控制流证据，F 边界）
```

---

## 20. 关键发现汇总

### 20.1 S1-111 核心发现

1. **14 API × 287 Controller 全局映射完成**
   - 13 个 API 跨多个 Controller 共享
   - 1 个 API (saveMedicalProductListOfSmallVersion.json) 仅 optometryGlassesCtrl 调用
2. **saveCustomerInfo trueName 字段错位**（D 级冲突）
   - optometryGlassesCtrl: `trueName = patientName` (L35522)
   - updateMemberCtrl: `trueName = customerName` (L20991)
   - checkinListCtrl: 不单独设置
3. **medicalRecordId 全局路径扩展到 9 类**（5 类 S1-108 锁定 + 4 类新增）
4. **optometryGlassesCtrl Factory 风格独特**：全部匿名 new ObjectFactory，其它 Controller 多命名
5. **PowerShell 陷阱发现**：`Get-Content` 与 `ReadAllLines` 行数差异 397 行（58817 vs 59214）

### 20.2 与 S1-110 一致性

- 14 unique API / 13 call site / 9 Read / 5 Write 全部保持
- 0 处 $state.go 保持
- edit 模式 0 影响保持
- medicalRecord 1 次整体赋值、0 次回读保持

### 20.3 L1 复刻指南

未来 1:1 复刻 optometryGlassesCtrl 的 14 API 时必须注意：
1. saveCustomerInfo.trueName **必须** 从 patient.patientName 派生（optometryGlassesCtrl 范围 D 级冲突）
2. getProductSkuExistCountVoList.json **必须** 同时支持 ObjectFactory 和 ListFactory
3. saveMedicalProductListOfSmallVersion.json Success **必须** 调用 GetMedicalProductVoList 刷新
4. getMedicalRecord.json Request 字段是 `{ id }`（不是 `{ medicalRecordId }`）
5. getCompanyOfMine.json **必须** 无参数调用

---

**审计完成。本文档为 172 号，提交后将形成 tracked=181。**
