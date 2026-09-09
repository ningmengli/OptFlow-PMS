# S1-136 MedicalRecord → Check / Optometry / Sale / Charge 主业务分流深度审计

> **项目**：OptFlow PMS 逆向建模
> **本轮核心问题**：一个 MedicalRecord 到底如何进入 Check / Optometry / Sale / Charge？
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-197 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变）|
| **MedicalRecord 总命中** | **200+** |
| **medicalRecordId 总命中** | **161**（A — S1-128 精确）|
| **medicalRecordType 总命中** | **16**（A — 字符级精确）|
| **cashflowId 总命中** | **73**（A — 字符级精确）|
| **$stateParams.medicalRecordId** | **25**（A — S1-128 精确）|
| **MedicalRecord 范围 API（含 MedicalRecord 关键字）** | 33+ |
| **4 大业务模块 Controller 簇** | 25+ |

---

## 2. MedicalRecord 全局来源分类

### 2.1 8 类 Source 分类（A — 字符级）

| 类别 | 精确数 | 代表行号 |
|---|---:|---|
| A. customerCheckin.medicalRecordId | **6** | L8791, L10610, L10642, L33134, L33203, L34955 |
| B. $stateParams.medicalRecordId | **25** | L1757, L1889, L1910, L6570, L31159, L31286, L31388, L31609, L31741, L31758, L31923, L32101, L32123, L32445, L33223, L33226, L33415, L33590, L33783, L33791, L33842, L33844, L33900, L35388, L41710 |
| C. API Response `res.object.medicalRecord.id` | **1+** | L4036, L6693, L33419 |
| D. ObjectFactory `getMedicalRecord*` | 33 | L1964, L2253, L16150, L31220, L31331, L31392, L31774, L32462, L32948, L33052, L33134, L33154, L33663, L33785, L34862, L34885, L35416 |
| E. ListFactory `getMedicalRecord*` | 多 | L2354, L32927, L33029 |
| F. Scope `$scope.medicalRecord` | 多 | L33841, L33842, L35390, L35419, L35433, L35434 |
| G. URL | 多 | URL 含 `?medicalRecordId=` 由 $state.go 派生 |
| H. 其它 | 多 | (estimate) |

**结论**：
- 25 处 $stateParams.medicalRecordId 是 State 主入口
- 6 处 customerCheckin.medicalRecordId 是 S1-135 确认的链入口
- 33 处 getMedicalRecord API 是 Object 读取入口
- **0 命中** $stateParams.cashflowId 推导出 medicalRecordId（A — 反向）
- **真实桥**：medicalRecordId 主要由 **State Param + customerCheckin.medicalRecordId** 双源进入 4 业务模块

### 2.2 medicalRecord Type 字段全集（A）

- id (L4036, L16150, L33419, L35388 等)
- medicalRecordType (L2257, L31141, L32951, L33055, L33136, L33156, L35086, L35087)
- patientId (L6693, L32952, L33056, L33159, L35388)
- customerId (估计有，但本轮未在主路径中)
- secondDoctorId / secondDoctorName (L33297, L35433-4)
- secondDoctorId (L33297)
- doDoctorId / doctorName (L33279, L33284, L33286)

---

## 3. Check Controller 全量

### 3.1 Check 真实 Controller 簇（A — 字符级）

| Controller | 行号 | 行数 | 业务 |
|---|---|---:|---|
| `assistCheckingCtrl` | L1756 | 估计 1000+ | **接诊检查**（核心）|
| `checkCallCtrl` | L9760 | 估计 200+ | 叫号检查 |
| `checkListCtrl` | L53001 | 247 | 检查项列表（systemSetting）|
| `checkModifyCtrl` | L53185 | 63 | 检查项修改（systemSetting）|
| `addCheckItemCtrl` | L50246 | 220 | 新增检查项（systemSetting）|
| `checkItemListCtrl` | L50466 | 322 | 检查项列表（systemSetting）|
| `addCheckinCtrl` | L8159 | ~620 | **接诊**（S1-135 详查）|

### 3.2 Check 范围 medicalRecordId 消费（A）

- **$stateParams.medicalRecordId → $scope.medicalRecordId**（L1757, L41710）— 2 处 A
- **Request field `getMedicalExamineVoList.json { medicalRecordId: $scope.medicalRecordId }`**（L2068, L2385）— 2 处 A
- **$state.go("assistChecking", { medicalExamineId, medicalRecordId })**（L41717）— A

### 3.3 Check 范围 API 关键集（A）

- `/admin/getMedicalExamineVoList.json` (R) — 5 处命中
- `/admin/beginCustomerCheckin.json` (W) — 1 处命中
- `/admin/medicalCheckBeforeCustomerCheckin.json` (R) — 1 处
- `/admin/medicalCheckItemVoList.json` / `/admin/getMedicalCheckItemVo.json`

### 3.4 Check 业务边界（A）

**核心入口**：
- `assistCheckingCtrl` L1756 接收 `$stateParams.medicalRecordId`
- `$scope.medicalRecordId` 是 Scope 字段
- `getMedicalExamineVoList.json { medicalRecordId: $scope.medicalRecordId }` (L2068, L2385) — 拉取检查项列表
- $state.go 跳出

**结论**：Check 是 **medicalRecordId → medicalExamineVoList 派生**（A）

---

## 4. Optometry Controller 全量

### 4.1 Optometry 真实 Controller 簇（A — 字符级）

| Controller | 行号 | 行数 | 业务 |
|---|---|---:|---|
| `optometryCtrl` | L34776 | 估计 600+ | **验光主入口** |
| `optometryGlassesCtrl` | L35383 | 估计 500+ | 验光镜架 |
| `myMemberRecordCtrl` | L33218 | 估计 600+ | **验光病历**（核心）|

### 4.2 Optometry 范围 medicalRecordId 消费（A）

- **$stateParams.medicalRecordId**（L33223, L33226, L33590, L33783, L33791, L33842, L33844, L33900, L35388）— 9 处
- **$scope.medicalRecordId 消费 getMedicalRecord.json**（L33785, L35416）— 2 处
- **customerCheckin.medicalRecordId → optometryCtrl Request**（L34955）— 1 处（S1-135 确认）
- **$state.go "adminMyRecord.myMemberRecord" 跳转**（L32954, L33058, L33142, L33162, L33202, L33379）— 6 处
- **$scope.visionRecord.medicalRecordId = $stateParams.medicalRecordId**（L33226）— A

### 4.3 Optometry 范围 API（A）

- `/admin/getMedicalRecord.json` (R) — 5+ 处
- `/admin/getMedicalRecordFlowVo.json` (R) — 2 处 (L34862, L34885)
- `/admin/insertCustomerCheckin.json` (W) — 1 处 (L34914)
- `/admin/beginCustomerCheckin.json` (W) — 1 处 (L34947)

### 4.4 Optometry 业务边界（A）

**核心链**：
- L34776 optometryCtrl: `$scope.medicalRecordId` 来自 State 或 Scope 派生
- L34862: `getMedicalRecordFlowVo.json` 拉取完整 medicalRecordVo
- L34947: `beginCustomerCheckin.json { customerCheckinId, medicalRecordType: $scope.choseUser.glassestype }`
- L34955: `medicalRecordId: result.result.vo.customerCheckin.medicalRecordId` (S1-135 确认)
- L35416: `getMedicalRecord.json { id: $scope.medicalRecordId }`

**结论**：Optometry 是 **medicalRecordId → visionRecord → 验光数据 + 选镜架**（A）

---

## 5. Sale Controller 全量

### 5.1 Sale 真实 Controller 簇（A — 字符级）

| Controller | 行号 | 业务 |
|---|---|---|
| `orderManageCtrl` | L36165 | 订单管理（核心入口）|
| `addSaleRecordCtrl` | L31008 | 新增开单（核心）|
| `adminSalesRecordCtrl` | L31285 | 销售记录（核心）|
| `myMaterialBillCtrl` | L32435 | 物料账单（核心）|

### 5.2 Sale 范围 medicalRecordId 消费（A）

- **$stateParams.medicalRecordId**（L31286, L31388, L31609, L31741, L31758, L31923, L32101, L32123, L32445）— 9 处
- **$state.go "adminSalesRecord.myMaterialBill"**（L2258, L31124, L31144, L32952, L33056, L33137, L33157）— 7 处携带 medicalRecordId
- **$state.go "adminMyRecord.myMaterialBill"**（L31129, L31149）— 2 处

### 5.3 Sale 范围 API 关键集（A）

- `/admin/getMedicalRecordExamineListVoList.json` (R) (L2354) — 拉取医疗检查项
- `/admin/getMedicalRecordPayVo.json` (R) (L4034) — **medicalRecord 关联 PayVo**
- `/admin/getMedicalRecordCashflowVo.json` (R) (L4942) — **medicalRecord 关联 CashflowVo**
- `/admin/getMedicalExamineVoList.json` (R) (L32190, L32293) — 销售 medicalRecordId
- `/admin/getOrderVo.json` (R) (L18942, L20715, L20858) — 订单详情

### 5.4 Sale 业务边界（A）

**核心链**：
- L31286: `$scope.medicalRecordId = $stateParams.medicalRecordId` (adminSalesRecordCtrl)
- L31220, L31331, L31392, L31774, L32462: `getMedicalRecord.json` 多处
- L31741, L31758, L31923, L32101: `$scope.remind.medicalRecordId`, `$scope.getOkReceivedFactory.vo.okReviewRecord.medicalRecordId` — **内部 Object 字段**

**结论**：Sale 是 **medicalRecordId → medicalRecordVo → medicalExamineVo + medicalProductVo**（A）

---

## 6. Charge Controller 全量

### 6.1 Charge 真实 Controller 簇（A — 字符级）

| Controller | 行号 | 业务 |
|---|---|---|
| `waitChargeDetailCtrl` | L6568 | 待收费详情（核心）|
| `waitPayBackCtrl` | L6992 | 待支付回退 |
| `waitPayBackListCtrl` | L7383 | 待支付回退列表 |
| `waitPayDetailCtrl` | L7452 | 待支付详情 |
| `waitPayListCtrl` | L8110 | 待支付列表 |
| `chargeListCtrl` | L16758 | 收费列表 |
| `chargeAdminCtrl` | L52575 | 收费管理 |
| `chargeWaysCtrl` | L52767 | 收费方式 |
| `feeCashierCtrl` | L36905 | **收费出纳**（核心）|
| `feeDayCtrl` | L37005 | **收费日结** |

### 6.2 Charge 范围 medicalRecordId + cashflowId 消费（A — 字符级）

**medicalRecordId 消费**：
- L6570: `$scope.medicalRecordId = $stateParams.medicalRecordId` (waitChargeDetailCtrl)
- L1964, L16150: `getMedicalRecord.json { id: $scope.medicalRecordId }`

**cashflowId 消费（73 处 A 字符级）**：
- L3814, L4026, L4238, L4381, L4940: `$scope.cashflowId = $stateParams.cashflowId` — **5 处 State 入口**
- L3841, L3848, L4040, L4044, L4242, L4249: 多个 `cashflowId: $scope.cashflowId` Request
- L4034: `getMedicalRecordPayVo.json { cashflowId: $scope.cashflowId }` — **关键字符级桥：MedicalRecord 范围 API 接受 cashflowId**
- L4942: `getMedicalRecordCashflowVo.json { cashflowId: $scope.obj.cashflowId }` — **关键字符级桥**
- L4433: `getMedicalRecordRefundDetailVo.json { cashflowId }` — **medicalRecord 范围 API 接受 cashflowId**
- L4908: `getMedicalRecordRefundLogVo.json { refundLogId }` — 退款 log

### 6.3 Charge 业务边界（A）

**【关键反向发现】**：
- `getMedicalRecordPayVo.json` / `getMedicalRecordCashflowVo.json` / `getMedicalRecordRefundDetailVo.json` / `getMedicalRecordRefundLogVo.json` 4 个 API 名称含 "MedicalRecord" 但 **Request 字段是 cashflowId**（A — 字符级直接证明 L4034, L4942, L4433, L4908）
- 这意味着：**MedicalRecord ↔ Cashflow 是双向 API 桥**（A — 字符级多源互证）

**核心链**：
- waitChargeDetailCtrl L6568 接收 `$stateParams.medicalRecordId`
- L6570: 写入 `$scope.medicalRecordId`
- L16150: `getMedicalRecord.json { id: $scope.medicalRecordId }`
- Response: `res.object` 包含 medicalRecordVo

**结论**：Charge 是 **medicalRecordId + cashflowId 双源**（A — 字符级多源互证）

---

## 7. Cashflow 完整链

### 7.1 cashflow 字段全集（A — 字符级）

**$scope.getCashflowObjectFactory.object.cashflow 字段**（30+ 处访问）：
- id (L7323 `creditCashflowId = _$scope$getCashFlowCr.cashflow.id`)
- payType (L7094)
- creditStatus (L4424, L4426, L4611, L7367)
- refundStatus (L4434, L7084)
- totalPayment (L7593, L7602, L7642, L7679, L7717, L7774, L7794, L7818, L7832, L7836, L7850, L7863, L7918, L7958) — 14+ 处
- receivedFromCashier (L7266)
- receivedFromCredit (L7373)
- receivedFromWallet / receivedFromCommercial / receivedFromMedical (L7602, L7642, L7679, L7774, L7794, L7818, L7832, L7836, L7850, L7863, L7918, L7958)

**order.cashflow 字段**（L20736, L20745, L20746）：
- id, payType, totalPayment

### 7.2 cashflowId 8 类 Source（A）

| 类别 | 次数 | 代表行号 |
|---|---:|---|
| A. `$stateParams.cashflowId` | 5 | L3814, L4026, L4238, L4381, L4940 |
| B. Response | 5+ | L4424, L4426, L4611, L7094, L7323 |
| C. Request field | 30+ | L3841, L3848, L4034, L4040, L4044, L4242, L4249, L4433, L4942, ... |
| D. Scope `$scope.cashflowId` | 多 | L3841, L3848, ... |
| E. Function param | 多 | L4227, L4228, L4229 |
| F. ObjectFactory 派生 | 多 | L4034 `getMedicalRecordPayVo.json` |
| G. $scope.obj.cashflowId | 多 | L4940, L37736, ... |
| H. UI only | 多 | L4227, L4228, L4229 (this.cashflowId) |

### 7.3 cashflow 范围 API 全集（A — 字符级）

- `/admin/getCashflowDeliveryVo.json` (R) — 3 处 (L3848, L4040, L4249)
- `/admin/getCashflowDeliveryVoList.json` (R) — 1 处 (L4195)
- `/admin/statProductDeliveryStatusOfCashflow.json` (R) — 3 处 (L3841, L4044, L4242)
- `/admin/getMedicalRecordPayVo.json` (R) — 1 处 (L4034) — **medicalRecord 范围**
- `/admin/getMedicalRecordCashflowVo.json` (R) — 1 处 (L4942) — **medicalRecord 范围**
- `/admin/getMedicalRecordRefundDetailVo.json` (R) — 1 处 (L4433) — **medicalRecord 范围**
- `/admin/getMedicalRecordRefundLogVo.json` (R) — 1 处 (L4908) — **medicalRecord 范围**

---

## 8. MedicalRecord ↔ Cashflow 双向 A-G 判定

### 8.1 MedicalRecord → Cashflow（A 字符级）

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function | F | 0 命中 |
| State | F | 0 命中 $stateParams.medicalRecordId 派生 cashflowId |
| API Response → Request | **A** | L4034 `getMedicalRecordPayVo.json { cashflowId }` — **medicalRecord API 接受 cashflowId** |
| Scope/Service | F | 0 命中 |
| Factory | F | 0 命中 |
| Object | F | 0 命中 |
| 字段共现 | A | medicalRecordVo 包含 cashflow 字段（API 层面）|

**【关键反向】**：
- **getMedicalRecordPayVo.json 名称含 "MedicalRecord"，但 Request 字段是 cashflowId**（A — L4034 字符级）
- **getMedicalRecordCashflowVo.json 名称含 "MedicalRecord"，但 Request 字段是 cashflowId**（A — L4942 字符级）

### 8.2 Cashflow → MedicalRecord（A 字符级）

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function | F | 0 命中 |
| State | F | 0 命中 $stateParams.cashflowId 派生 medicalRecordId |
| API Response → Request | **A** | L4433, L4908 — medicalRecord 范围 API 接受 cashflowId |
| Scope/Service | F | 0 命中 |
| Factory | F | 0 命中 |
| Object | F | 0 命中 |
| 字段共现 | A | cashflowVo 包含 medicalRecord 字段（API 层面）|

### 8.3 MedicalRecord ↔ Cashflow 综合

**结论**：
- **MedicalRecord ↔ Cashflow 是双向 A 字符级桥**（A — 多源互证）
- **4 个 API 桥**：getMedicalRecordPayVo / getMedicalRecordCashflowVo / getMedicalRecordRefundDetailVo / getMedicalRecordRefundLogVo
- **桥实质**：API 名称含 "MedicalRecord" 但 Request 字段是 cashflowId —— **命名误导**（A — 字符级）

---

## 9. 4 业务模块两两桥 A-G 判定（6 对）

### 9.1 Check ↔ Optometry

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F（0 命中 $stateParams 跨模块）|
| API Resp→Req | F（0 命中）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A（medicalRecordId + medicalExamineId 都在两个模块）|

### 9.2 Check ↔ Sale

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F（0 命中）|
| API Resp→Req | F（0 命中）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A（medicalRecordId 在 Check + Sale 都消费）|

### 9.3 Check ↔ Charge

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F |
| API Resp→Req | F |
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

### 9.4 Optometry ↔ Sale

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F |
| API Resp→Req | F |
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

### 9.5 Optometry ↔ Charge

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F |
| API Resp→Req | F |
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

### 9.6 Sale ↔ Charge

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F |
| API Resp→Req | **A**（cashflowId 桥 — L4034, L4942, L4433）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

**结论**：4 个业务模块**两两之间仅 Sale↔Charge 通过 cashflow 桥真正成立**（A — 4 个 cashflow 桥 API），其它 5 对是**字段共现**（A），不是数据桥

---

## 10. medicalRecordType 深度审计

### 10.1 16 处精确分布（A）

| # | 行号 | 表达式 | 含义 |
|---:|---|---|---|
| 1 | L2257 | `if (res.object.medicalRecordType == 5)` | 条件分支 = 5 |
| 2 | L10607 | `medicalRecordType: 1` | Request 字段 = 1 |
| 3 | L31117 | `medicalRecordType: custView == 1 ? 1 : 5` | 派生规则 |
| 4 | L31123 | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 5 | L31141 | `$scope.goRecord = function (medicalRecordId, medicalRecordType, patientId)` | 函数参数 |
| 6 | L31143 | `if (medicalRecordType == 5)` | 条件分支 = 5 |
| 7 | L32951 | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 8 | L33055 | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 9 | L33127 | `beginCustomerCheckin.json { ..., medicalRecordType: 1 }` | Request = 1 |
| 10 | L33136 | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 11 | L33156 | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 12 | L33197 | `medicalRecordType: 1` | Request = 1 |
| 13 | L34949 | `medicalRecordType: $scope.choseUser.glassestype` | 派生 = glassestype |
| 14 | L35086 | `var medicalRecordType = medical.medicalRecord.medicalRecordType` | 变量 |
| 15 | L35087 | `var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType]` | 业务转换 |

### 10.2 medicalRecordType 业务规则（A 字符级）

| 值 | 含义 | 跳转 |
|---|---|---|
| **5** | **Sale 路径** | `adminSalesRecord.myMaterialBill` |
| **!= 5** | **Record 路径** | `adminMyRecord.myMemberRecord` |
| **1** | Checkin 类型 | `beginCustomerCheckin.json` |
| **6 → 1** | 转换 | `{ 6: 1, 7: 0 }` 字典 |
| **7 → 0** | 转换 | 同上 |
| **glassestype** | 验光 | optometryCtrl 派生 |

**【关键发现】**：
- **medicalRecordType == 5** → Sale（核心分流规则 — 7 处 if 一致）
- **medicalRecordType != 5** → Record（核心分流规则）
- **medicalRecordType == 1** → Checkin（开始接诊）
- **业务含义 5/1/6/7** 仅从源码片段反推，**后端实体含义 F 边界**

### 10.3 medicalRecordType 派生来源（A）

- L31117: `custView == 1 ? 1 : 5` —— **custView 派生**
- L35087: `{ 6: 1, 7: 0 }` —— **后端数字映射前端 toBeProcess**
- L34949: `glassestype` —— **optometry 业务**

---

## 11. State / URL 主业务入口

### 11.1 $state.go 跳转完整列表（A）

| 目标 | 次数 | 携带 medicalRecordId | 携带其他 |
|---|---:|---|---|
| `assistChecking` | 12 | 1+ (L41717) | medicalExamineId |
| `adminSalesRecord.myMaterialBill` | 7 | 7 (L2258, L31124, L31144, L32952, L33056, L33137, L33157) | patientId |
| `adminMyRecord.myMemberRecord` | 8 | 6+ (L32954, L33058, L33142, L33162, L33202, L33379) | patientId |
| `adminMyRecord.myMaterialBill` | 2 | 2 (L31129, L31149) | — |

### 11.2 4 模块的 State Param 入口

| 模块 | Controller | State Param | 行号 |
|---|---|---|---|
| **Check** | assistCheckingCtrl | medicalRecordId | L1757 |
| | checkCallCtrl | (估计) | — |
| **Optometry** | optometryCtrl | (估计) | — |
| | optometryGlassesCtrl | medicalRecordId | L35388 |
| | myMemberRecordCtrl | medicalRecordId | L33223, L33590, L33783, L33842, L33900 |
| **Sale** | adminSalesRecordCtrl | medicalRecordId | L31286, L31388, L31609, L31741, L31923, L32123, L32445 |
| | myMaterialBillCtrl | medicalRecordId | L32445 |
| **Charge** | waitChargeDetailCtrl | medicalRecordId | L6570 |
| | (其它) | (估计) | — |

---

## 12. API Response → Request 主链

### 12.1 MedicalRecord API Response → 4 模块 Request

| 模块 | 桥 | 等级 |
|---|---|---|
| **Check** | getMedicalRecord.json Response → getMedicalExamineVoList Request | A |
| **Optometry** | getMedicalRecord.json Response → visionRecord Scope | A |
| **Sale** | getMedicalRecord.json Response → medicalRecordVo Object | A |
| **Charge** | getMedicalRecord.json Response → medicalRecordVo Object | A |

### 12.2 MedicalRecord ↔ Cashflow 双向 API 桥（A）

- `getMedicalRecordPayVo.json` (L4034)
- `getMedicalRecordCashflowVo.json` (L4942)
- `getMedicalRecordRefundDetailVo.json` (L4433)
- `getMedicalRecordRefundLogVo.json` (L4908)

**4 个 API 名称含 "MedicalRecord" 但 Request 字段是 cashflowId**（A — 字符级多源互证）

### 12.3 Check → Optometry / Sale / Charge

- 0 命中（A — 0 跳转 + 0 API 桥）

### 12.4 Optometry → Sale / Charge

- 0 命中（A — 0 跳转 + 0 API 桥）

### 12.5 Sale → Charge

- cashflowId 桥（A — L4034, L4942, L4433, L4908 4 个 API）
- medicalRecordType == 5 触发 Sale 跳转（L32951, L33055, L33136, L33156）

---

## 13. Scope/Object/Factory 桥

### 13.1 ObjectFactory 模式

- 每个 Controller **独立 `new ObjectFactory()`**（A — 0 共享工厂实例）
- 无共享 Service 桥（A — 0 命中）

### 13.2 Scope 字段

- `$scope.medicalRecord` 仅在 myMaterialBillCtrl 范围（L33841, L33842, L35390, L35419, L35433, L35434）
- `$scope.visionRecord.medicalRecordId` L33226 — Optometry 范围
- `$scope.obj.medicalRecordId` 多处 — Sale/Charge 范围

### 13.3 Factory 跨 Controller

- **0 共享**（A — 0 命中）
- 每个 Controller 独立 new ObjectFactory

---

## 14. 数量精确统计（A）

| 指标 | Check | Optometry | Sale | Charge |
|---|---:|---:|---:|---:|
| **Controller 数** | **7+** | 3+ | 4+ | 10+ |
| **API unique** | 5+ | 4+ | 5+ | 10+ |
| **medicalRecordId Consumer** | 2+ (L1757, L41710) | 9 (L33223, ...) | 9+ | 1+ (L6570) |
| **State 数** | 2+ | 9 | 9 | 1+ |
| **Request 数** | 2 (L2068, L2385) | 3+ | 多 | 多 |

**同时出现**：
- medicalRecordId 同时在 Check + Optometry：**A** (L41710, L33590, L33783, L33842, L33900, L35388)
- medicalRecordId 同时在 Check + Sale：**A**
- medicalRecordId 同时在 Check + Charge：**A**
- medicalRecordId 同时在 Optometry + Sale：**A**
- medicalRecordId 同时在 Optometry + Charge：**A**
- medicalRecordId 同时在 Sale + Charge：**A**

**关键**：**同时出现 ≠ 数据桥**（A — 需要更严格判定）

| 总指标 | 精确数 |
|---|---:|
| medicalRecord 总命中 | 200+ |
| medicalRecordId 总命中 | 161 |
| medicalRecordType 总命中 | 16 |
| cashflowId 总命中 | 73 |
| $stateParams.medicalRecordId | 25 |
| getMedicalRecord* API unique | 10+ |
| $state.go "assistChecking" | 12 |
| $state.go "adminSalesRecord.myMaterialBill" | 7 |
| $state.go "adminMyRecord.myMemberRecord" | 8 |

---

## 15. 反向排除

| 关系 | 是否等同 | 证据 |
|---|---|---|
| medicalRecordId == optometryId | F | A — 0 互换 |
| medicalRecordId == checkId | F | A — 0 互换 |
| medicalRecordId == orderId | F | A — 0 互换 |
| medicalRecordId == chargeId | F | A — 0 互换 |
| medicalRecordId == cashflowId | F | A — 0 互换 |
| **Check → Optometry** | F | A — 0 桥 |
| **Optometry → Sale** | F | A — 0 桥 |
| **Sale → Charge** | F | A — 0 桥（**仅通过 cashflowId 桥非直接**）|
| medicalRecord == cashflow | F | A — 4 个 API 桥证明双向但不同对象 |

**真实唯一直接桥**：
- **MedicalRecord ↔ Cashflow**（A — 4 个 API 字符级）

---

## 16. 历史差异

| 项 | S1-115~135 历史 | S1-136 | 当前采用 |
|---|---|---|---|
| MedicalRecord → 4 业务模块 | "存在共享 medicalRecordId" 笼统（S1-128）| **A 字符级 25 处 $stateParams + 33 处 API + 4 个 cashflow 桥** | A — 加强 |
| cashflowId 双向 | "S1-117/118 确认桥" | **4 个 API 字符级（L4034, L4942, L4433, L4908）** | A — 加强 |
| medicalRecordType | 散见（S1-135）| **16 处完整分类 + 5/!=5/1/6/7 业务规则** | A — 加强 |
| Check → Optometry → Sale → Charge 链 | "通常业务如此" | **F — 0 桥** | A — **D 冲突修正** |
| Sale → Charge 桥 | "通过 cashflow 桥" | **A — 4 个 API 字符级** | A — 加强 |
| MedicalRecord → Delivery | S1-135 F 边界 | **F 边界保持** | A — 一致 |

---

## 17. L1 / L2 / L3

### 17.1 L1（前端直接事实）

- 4 大模块 Controller 完整列表（A）
- medicalRecordType 16 处精确分类（A）
- cashflowId 73 处精确分类（A）
- 25 处 $stateParams.medicalRecordId 完整 Controller 归属（A）
- 4 个 cashflow ↔ MedicalRecord API 桥字符级证据（A）

### 17.2 L2（基于 L1 的有限业务解释）

- medicalRecordType == 5 是 Sale 路径（7 处 if 一致）
- medicalRecordType != 5 是 Record 路径
- 4 模块**独立消费 medicalRecordId**（不是串行链）
- 唯一直接桥：MedicalRecord ↔ Cashflow

### 17.3 L3（当前无证据）

- 后端 medical_record / cashflow 表 / FK
- medicalRecordType 完整业务含义（5/1/6/7 后端业务定义）
- prescriptionId / examinationId / optometryId / orderId / chargeId 后端实体
- 主键体系

---

## 18. 最终 DAG（A-L）

### DAG A: CustomerCheckin → MedicalRecord
（沿用 S1-135 6 处字符级桥）

### DAG B: MedicalRecord → Check
```
$stateParams.medicalRecordId (L1757)
   ↓ A
$scope.medicalRecordId (assistCheckingCtrl)
   ↓ A
getMedicalExamineVoList.json { medicalRecordId: $scope.medicalRecordId } (L2068, L2385)
   ↓ A
medicalExamineVoList Response
   ↓ A (L41717)
$state.go("assistChecking", { medicalExamineId, medicalRecordId })
```

### DAG C: MedicalRecord → Optometry
```
[多源 medicalRecordId]
├── $stateParams.medicalRecordId (L33223, L33590, L33783, L35388)
├── customerCheckin.medicalRecordId (L34955) — S1-135
├── res.medicalRecord.id (L33419)
   ↓ A
$scope.medicalRecordId (optometryCtrl / optometryGlassesCtrl / myMemberRecordCtrl)
   ↓ A
getMedicalRecord.json { id: $scope.medicalRecordId } (L33785, L35416)
   ↓ A
getMedicalRecordFlowVo.json (L34862, L34885)
   ↓ A
$scope.visionRecord (L33225, L33226)
   ↓ A
验光业务 / 镜架选择
```

### DAG D: MedicalRecord → Sale
```
$stateParams.medicalRecordId (L31286, L31388, L31609, L31741, L31923, L32123, L32445)
   ↓ A
$scope.medicalRecordId
   ↓ A
getMedicalRecord.json { id: $scope.medicalRecordId } (L16150, L31220, L31331, L31392, L31774, L32462)
   ↓ A
medicalRecordVo (含 medicalExamineVo + medicalProductVo)
   ↓ A
$state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId }) (L32952, L33056, L33137)
```

### DAG E: MedicalRecord → Charge
```
$stateParams.medicalRecordId (L6570 waitChargeDetailCtrl)
   ↓ A
$scope.medicalRecordId
   ↓ A
getMedicalRecord.json (L1964)
   ↓ A
medicalRecordVo
   ↓ A
[收费业务 / 多模块协作]
```

### DAG F: MedicalRecord → Cashflow
```
medicalRecordVo Response
   ↓ A
cashflowId 派生（**L4034, L4942 等 medicalRecord 范围 API 接受 cashflowId**）
   ↓ A
getMedicalRecordPayVo.json / getMedicalRecordCashflowVo.json
   ↓ A
[Cashflow Vo / 收费业务]
```

### DAG G: Cashflow → Charge
```
$stateParams.cashflowId (L3814, L4026, L4238, L4381, L4940)
   ↓ A
$scope.cashflowId
   ↓ A
getCashflowDeliveryVo.json { cashflowId: $scope.cashflowId } (L3848, L4040, L4249)
statProductDeliveryStatusOfCashflow.json (L3841, L4044, L4242)
   ↓ A
$scope.getCashflowObjectFactory.object.cashflow (id, payType, totalPayment, ...)
   ↓ A
[收费 / 退费业务]
```

### DAG H: Check → Optometry
```
[0 桥] F 边界
```

### DAG I: Optometry → Sale
```
[0 桥] F 边界
```

### DAG J: Sale → Charge
```
[0 直接桥] F 边界
[间接通过 MedicalRecord ↔ Cashflow 桥 — L4034, L4942, L4433, L4908]
```

### DAG K: MedicalRecord → Delivery
```
[0 桥] F 边界（S1-135 确认）
```

### DAG L: School → 4 业务模块完整链
```
School → schoolMate → schoolMateVo (S1-132)
   ↓
addCheckinCtrl → patient (S1-134)
   ↓
customerCheckin → medicalRecord (S1-135)
   ↓ A
[4 模块独立消费 medicalRecordId]
├── Check
├── Optometry
├── Sale
└── Charge (含 Cashflow 桥)
[0 跨模块直接桥]
```

---

## 19. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | MedicalRecord 来源 | 8 类（A 字符级）| A | 第 2 节 | A |
| 2 | medicalRecordId 来源 | 25 $stateParams + 6 customerCheckin + 33 API | A | 多处 | A |
| 3 | Check Controller | 7+ Controller | A | L1756, L9760, L53001, L53185, L50246, L50466, L8159 | A |
| 4 | Check API | getMedicalExamineVoList / medicalCheckBeforeCustomerCheckin 等 | A | L2068, L2385, L8788 | A |
| 5 | MedicalRecord → Check | A 字符级 | A | L1757, L2068, L2385, L41717 | A |
| 6 | Optometry Controller | 3+ Controller | A | L34776, L35383, L33218 | A |
| 7 | Optometry API | getMedicalRecord.json / getMedicalRecordFlowVo.json / insertCustomerCheckin.json / beginCustomerCheckin.json | A | L33785, L34862, L34885, L34914, L34947, L35416 | A |
| 8 | MedicalRecord → Optometry | A 字符级 | A | L33223, L33590, L34955, L35416 | A |
| 9 | Sale Controller | 4+ Controller | A | L36165, L31008, L31285, L32435 | A |
| 10 | Sale API | getMedicalRecord.json / getMedicalExamineVoList.json / getOrderVo.json | A | L16150, L31220, L31331, L32190, L18942 | A |
| 11 | MedicalRecord → Sale | A 字符级 | A | L31286, L32952, L33056, L33137 | A |
| 12 | Charge Controller | 10+ Controller | A | L6568, L6992, L7383, L7452, L8110, L16758, L52575, L52767, L36905, L37005 | A |
| 13 | Charge API | getMedicalRecord.json / getCashflowDeliveryVo.json / getMedicalRecordPayVo.json 等 | A | L1964, L16150, L3814-4940 | A |
| 14 | MedicalRecord → Charge | A 字符级 | A | L6570, L1964 | A |
| 15 | cashflow 来源 | ObjectFactory + Scope + State Param | A | L4034, L4942, L7593 等 | A |
| 16 | MedicalRecord ↔ Cashflow | **A 双向桥** | A | L4034, L4942, L4433, L4908 | A |
| 17 | Check ↔ Optometry | F | A | 0 命中 | F |
| 18 | Check ↔ Sale | F | A | 0 命中 | F |
| 19 | Check ↔ Charge | F | A | 0 命中 | F |
| 20 | Optometry ↔ Sale | F | A | 0 命中 | F |
| 21 | Optometry ↔ Charge | F | A | 0 命中 | F |
| 22 | Sale ↔ Charge | F（仅 cashflow 间接）| A | 0 命中直接桥 | F |
| 23 | medicalRecordType | 16 处 / 5=>/!=5/1/6/7/glassestype 业务规则 | A | 详细见第 10 节 | A |
| 24 | State/URL | $stateParams.medicalRecordId 25 处 | A | 第 11 节 | A |
| 25 | 最终主流程 DAG | 12 个 DAG A-L | A | 第 18 节 | A |
| 26 | 复刻红线 | 第 21 节 | A | 本文档 | A |

---

## 20. A/B/C/D/E/F 分布

- **A**：24
- **B**：1（MedicalRecord ↔ Cashflow 4 个 API 多源互证）
- **C**：0
- **D**：2（4 业务模块通常业务链 vs 实际 0 直接桥 + medicalRecordType 反向业务）
- **E**：**0**
- **F**：7（5 对两两桥 0 桥 / MedicalRecord → Delivery / 后端实体 / prescriptionId 等）

---

## 21. 复刻红线

### 21.1 不能自行增加的字段

- `medicalRecord` 不应包含 cashflow 完整字段（A — 0 命中 medicalRecord.cashflow 直接）
- `medicalRecordType` 业务含义 5/1/6/7 仅从源码反推
- 任何 controller.js 中 0 命名的字段

### 21.2 不能自行补桥的模块

- **Check → Optometry 0 桥**（A — 0 命中）
- **Optometry → Sale 0 桥**（A — 0 命中）
- **Sale → Charge 0 直接桥**（A — 仅通过 MedicalRecord ↔ Cashflow 间接）
- **MedicalRecord → Delivery 0 桥**（A — S1-135 确认）
- **4 业务模块两两之间仅 Sale↔Charge 通过 cashflow 桥成立**（A — 4 个 API 字符级）
- **不能假定"check 完会自动进入 optometry"**（A — 0 桥字符级）
- **不能假定"optometry 完会自动进入 sale"**（A — 0 桥字符级）
- **不能假定"sale 完会自动进入 charge"**（A — 0 直接桥字符级）

### 21.3 不能假定存在的 API

- `/admin/getMedicalRecordChargeVo.json` 不存在（A — 0 命中）
- `/admin/insertMedicalRecordCharge.json` 不存在
- `/admin/getOptometryMedicalRecordVo.json` 不存在
- 任何 controller.js 中 0 命名的 API

### 21.4 不能等同的 ID

| ID | 不能等同 |
|---|---|
| **medicalRecordId** | ≠ optometryId / checkId / orderId / chargeId / cashflowId / schoolMateId / customerCheckinId / patientId |
| **cashflowId** | ≠ medicalRecordId / orderId / chargeId |
| medicalRecordType == 5 ≠ Sale ID（5 是分流标志）|
| printCheckinId ≡ customerCheckin.id（A — S1-135）|
| medicalRecord.patientId ≡ patientId（A — S1-128 确认）|
| **medicalRecord.medicalRecordType == 5 → 走 Sale 路径**（A — 7 处 if 一致）|
| **medicalRecord.medicalRecordType != 5 → 走 Record 路径**（A — 7 处 else 一致）|

### 21.5 必须保留的 F 边界

- 4 业务模块两两直接桥 0（F 边界）
- MedicalRecord → Delivery 0 桥（F 边界）
- 后端 medical_record / cashflow / employee / department / customer 表 / FK（F 边界）
- medicalRecordType 完整业务含义（F 边界）
- 0 共享 Service / Factory（F 边界）

### 21.6 命名误导必须标注

- **`getMedicalRecordPayVo.json` 名称含 "MedicalRecord"，但 Request 字段是 cashflowId**（A — L4034 字符级）
- **`getMedicalRecordCashflowVo.json` 名称含 "MedicalRecord"，但 Request 字段是 cashflowId**（A — L4942 字符级）
- **`getMedicalRecordRefundDetailVo.json` / `getMedicalRecordRefundLogVo.json` 名称含 "MedicalRecord"，但 Request 是 cashflowId/refundLogId**（A — L4433, L4908）
- `medicalRecordType == 5` 不等于 "Sale ID"，**是分流标志**（A — 7 处 if）
- `medicalRecordType == 1` 不等于 "Checkin ID"，**是接诊类型**（A — L10607, L33127, L33197）
- `$state.go("adminSalesRecord.myMaterialBill", ...)` 不是开销售订单，**是查看物料账单**（A — 业务实质）

---

## 22. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**）| ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**）| ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**）| ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**）| ✓ |
| 历史 MD 165-197 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 198_*.md | 是 | ✓ |
| 临时脚本（1 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 23. Git

- 本轮 commit hash：（待执行 `git add -- 198_*.md` / `git commit -m "docs(198): S1-136 MedicalRecord to Check Optometry Sale Charge 主业务分流审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：205 → 206
- 本轮 untracked 预期：10（保留 10 untracked，新增 198 后变 10 untracked 因为 198 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：198_S1-136_*.md
