# S1-119 cashflowId 全局 Provenance、生命周期与跨模块 Consumer 审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（gitignored）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-118（HEAD=370e640，tracked=188，untracked=10，ignored=1）
> - 本轮**重点**：cashflowId 在 controller.js 全局的 Provenance / 生命周期 / 跨模块 Consumer 完整审计
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-180）/ 修改 7 HTML / 修改 11 文件 / 修改 P0=54 / P1=8

---

## 1. 审计范围

### 1.1 S1-118 已确认（保持）

- getMedicalRecordCashflowVo：8 Controller / 9 处调用
- getMedicalRecordPayVo：1 Controller（deliveryInputRecordCtrl）
- 两条桥：cashflowId → customer（Charge 内部）+ cashflowId → medicalRecordId（Charge → Delivery）
- waitChargeDetailCtrl L6693 medicalRecord.patientId 派生（来自 computeUnPlaceOrderMedicalRecordFee API）

### 1.2 S1-119 新发现（重大）

- **cashflowId Case-Sensitive 出现 74 次**（S1-115/118 仅扫描 4-8 Controller 范围内）
- **Case-Insensitive 出现 80 次**（多 6 处 `cashflowCreditLogDataList` 等）
- **20 个 Controller 涉及 cashflowId**（S1-115 报 6 Controller，S1-119 实际 **20** 个）

---

## 2. cashflowId 全局命中

### 2.1 Case-Sensitive vs Case-Insensitive

| 模式 | 总数 |
|---|---:|
| Case-Sensitive `cashflowId` | 74 |
| Case-Insensitive `cashflowId` | 80 |
| 差异 | 6（cashflowCreditLogDataList 等） |

**A 级确认**：Case-Sensitive 74 处

### 2.2 20 Controller 全集

| # | Controller | cashflowId 数 |
|---:|---|---:|
| 1 | payedListCtrl | 10 |
| 2 | partBackCtrl | 10 |
| 3 | waitPayBackCtrl | 6 |
| 4 | deliveryListCtrl | 6 |
| 5 | deliveryInputRecordCtrl | 4 |
| 6 | feeCashierCtrl | 4 |
| 7 | feeDayCtrl | 4 |
| 8 | unPayDetailCtrl | 4 |
| 9 | machineOrderBrokenCtrl | 3 |
| 10 | waitPayDetailCtrl | 3 |
| 11 | deliveryProcessingCtrl | 3 |
| 12 | refundFeeCtrl | 3 |
| 13 | deliveryInputCtrl | 3 |
| 14 | optometryCtrl | 3 |
| 15 | machineOrderCtrl | 2 |
| 16 | payedDetailCtrl | 2 |
| 17 | waitChargeDetailCtrl | 1 |
| 18 | chargeListCtrl | 1 |
| 19 | waitPayListCtrl | 1 |
| 20 | selectOrderListCtrl | 1 |
| **总计** | **20** | **74** |

---

## 3. cashflowId Expression 路径全集

### 3.1 8 大类 Expression 路径

| 类别 | 出现次数 | 典型表达式 |
|---|---:|---|
| `$stateParams.cashflowId` | ~7 | `$scope.cashflowId = $stateParams.cashflowId;` |
| `$scope.cashflowId` | ~25 | `$scope.getXxxFactory.saveOrQuery(..., { cashflowId: $scope.cashflowId })` |
| `$scope.obj.cashflowId` | ~10 | `$scope.obj.cashflowId = $stateParams.cashflowId;` |
| `function param cashflowId` | ~5 | `function (cashflowId)` |
| `this.cashflowId` | ~5 | `this.cashflowId = id;` (print modal) |
| `param.cashflowId` | ~10 | `param: { cashflowId: $stateParams.cashflowId }` (URL) |
| `item.cashflow.id` | 1 | `cashflowId: order.cashflow.id` (L20736) |
| `res.object.cashflowId` | ~10 | `res.cashflowCreditLogDataList[idx].cashflowId` |

### 3.2 关键差异

- **`cashflow.id` ≠ `cashflowId`**：cashflow.id 是 cashflow 对象内的字段（如 L7323 / L20736）
- **`this.cashflowId` 在 print modal 中**（如 L4229 / L5157）—— 仅用于 modal display
- **`param.cashflowId` 在 print URL string 中**（如 L4221 / L4374）

---

## 4. Source 分类

### 4.1 cashflowId provenance taxonomy

| 类别 | 数量 | 典型来源 | A-F |
|---|---:|---|---|
| **A. API Response** | 3+ | L6054 `res.cashflowCreditLogDataList[idx].cashflowId` | A |
| **B. StateParams** | 7+ | `$scope.cashflowId = $stateParams.cashflowId;` | A |
| **C. Scope** | 25+ | `$scope.cashflowId` / `$scope.obj.cashflowId` | A |
| **D. Factory item** | 1 | `order.cashflow.id` (L20736) | A |
| **E. Function parameter** | 5+ | `function (cashflowId)` 多处 | A |
| **F. URL string** | 10+ | `param: { cashflowId: $stateParams.cashflowId }` | A |
| **G. Constant** | 5+ | `cashflowId: ""` (L4218, L5140, L5154, L35266) | A |
| **H. 派生字段** | 1 | `creditCashflowId = _$scope$getCashFlowCr.cashflow.id` (L7323) | A |
| **I. 未知** | 0 | - | A |

### 4.2 cashflowId 7+ 个 State 入口 Controller

| Controller | 行号 | 表达式 |
|---|---:|---|
| deliveryInputCtrl | 3814 | `$scope.cashflowId = $stateParams.cashflowId;` |
| deliveryInputRecordCtrl | 4026 | 同上 |
| deliveryProcessingCtrl | 4238 | 同上 |
| partBackCtrl | 4381 | 同上 |
| payedDetailCtrl | 4940 | `$scope.obj.cashflowId = $stateParams.cashflowId;` |
| waitPayDetailCtrl | 7462 | 同上 |
| machineOrderBrokenCtrl | 16262 | `$scope.cashflowId = $stateParams.cashflowId;` |

**S1-119 关键发现 A**：
- **7+ 个 Controller** 通过 `$stateParams.cashflowId` 接收 cashflowId
- **没有单一上游主来源**——**严禁** 假设存在一个"主 cashflowId"

---

## 5. 第一来源追迹

### 5.1 主线入口：$stateParams.cashflowId

```
[State 入口 - F 边界: State 配置不在 controller.js]
$stateParams.cashflowId
  ↓
[7+ 个 Controller 直接赋值]
├─ $scope.cashflowId (deliveryInputCtrl/RecordCtrl/ProcessingCtrl/partBackCtrl/machineOrderBrokenCtrl)
└─ $scope.obj.cashflowId (payedDetailCtrl/unPayDetailCtrl/waitPayBackCtrl/waitPayDetailCtrl/waitPayListCtrl)
  ↓
[API Request] 多个 API
```

### 5.2 API Response 入口：cashflowCreditLogDataList

```
$scope.customerCashflowCreditLogVo.cashflowCreditLogDataList[idx].cashflowId
  ↓
$scope.obj.creditCashflowId (L6054 unPayDetailCtrl)
  ↓
后续 API Request
```

### 5.3 派生入口：cashflow.id

```
order.cashflow.id (L20736 selectOrderListCtrl)
  ↓
cashflowId: order.cashflow.id
  ↓
Request.cashflowId (L20736 后续 API)
```

```
_$scope$getCashFlowCr.cashflow.id (L7323 waitPayBackCtrl)
  ↓
creditCashflowId
  ↓
[用于 payCreditRefund.json Request]
```

---

## 6. API Response 提供 cashflowId

### 6.1 全局 API Response 出现 cashflowId

| 行号 | 表达式 | 来源 API | A-F |
|---:|---|---|---|
| 6054 | `res.cashflowCreditLogDataList[idx].cashflowId` | cashflowCreditLogVoList | A |
| 6518 | `res.cashflowCreditLogDataList[$scope.index].cashflowId` | cashflowCreditLogVoList | A |
| 6519 | `res.cashflowCreditLogDataList[$scope.index].cashflowId` | cashflowCreditLogVoList | A |
| 6929 | `res.result.object` (作为 cashflowId 用) | getMedicalRecordCashflowVo.json (waitPayBackCtrl) | A |

### 6.2 S1-119 关键发现 C

- **getMedicalRecordCashflowVo.json 的 cashflow 派生**：
  - L6929 `$state.go("waitPayDetail", { cashflowId: res.result.object })` —— **Response.object 直接作为 cashflowId 传递**
  - **S1-118 漏的**重大新发现**！

### 6.3 getMedicalRecordCashflowVo Response 派生 cashflowId 完整链

```
[waitPayBackCtrl 内部]
$scope.obj.cashflowId = $stateParams.cashflowId
  ↓
getMedicalRecordCashflowVo.json { cashflowId: $scope.obj.cashflowId }  (L7070)
  ↓ Response
res.result.object  ← 这个 object 含 cashflow + customer
  ↓
$state.go("waitPayDetail", { cashflowId: res.result.object })  (L6929)
  ↓
[waitPayDetailCtrl 接收]
$scope.obj.cashflowId = $stateParams.cashflowId  (L7462)
  ↓
getMedicalRecordCashflowVo.json Request  (L7488)
```

**S1-119 关键发现 D**：
- **waitPayBackCtrl 内部 getMedicalRecordCashflowVo.json Response 的 `res.result.object` 整个被作为 cashflowId 传递**
- 这是 S1-115 锁定 cashflowId 多对象派生的**实例证明**（cashflowId 实际是 cashflow 对象的整体）

---

## 7. API Request 消费 cashflowId

### 7.1 跨主链 API Request 消费 cashflowId 分布

| Branch | API | Controller |
|---|---|---|
| Delivery | getCashflowDeliveryVo.json | deliveryInputCtrl/RecordCtrl/ProcessingCtrl |
| Delivery | statProductDeliveryStatusOfCashflow.json | deliveryInputCtrl/RecordCtrl/ProcessingCtrl |
| Delivery | getMedicalRecordPayVo.json | deliveryInputRecordCtrl |
| Charge | getMedicalRecordCashflowVo.json | payedDetailCtrl/payedListCtrl/waitPayBackCtrl/waitPayDetailCtrl |
| Charge | getMedicalRecordCashflowVoListOfCompany.json | payedListCtrl/waitPayListCtrl |
| Charge | getCustomerVo.json | payedDetailCtrl/waitPayDetailCtrl |
| Charge | getCustomerWallet.json | payedDetailCtrl/waitPayDetailCtrl |
| Charge | getCustomerPoint.json | waitPayDetailCtrl |
| Charge | getMedicalRecordRefundDetailVo.json | partBackCtrl |
| Charge | payCreditRefund.json | waitPayBackCtrl |
| Charge | cancelMedicalRecordCashflow.json | unPayDetailCtrl |
| Other | getCanBeProcessSkuInListOfProduct.json | machineOrderBrokenCtrl |

### 7.2 跨主链流动分析

**S1-119 关键发现 E**：
- **cashflowId 不直接通过 API Request 跨主链**（F 边界）
- **跨主链流动由 State 配置承担**（`$stateParams.cashflowId`）

---

## 8. State 传递

### 8.1 $state.go with cashflowId

| 行号 | 表达式 | State | 来源 |
|---:|---|---|---|
| 6929 | `$state.go("waitPayDetail", { cashflowId: res.result.object })` | waitPayDetail | **Response 派生** |

### 8.2 $state.href with cashflowId

| 行号 | 表达式 | State | 来源 |
|---:|---|---|---|
| 36940 | `$state.href("payedDetail", { cashflowId: id })` | payedDetail | `id` (函数参数) |
| 37080 | `$state.href("payedDetail", { cashflowId: id })` | payedDetail | `id` (函数参数) |

### 8.3 State 入口（$stateParams.cashflowId）

| Controller | 行号 |
|---|---:|
| deliveryInputCtrl | 3814 |
| deliveryInputRecordCtrl | 4026 |
| deliveryProcessingCtrl | 4238 |
| partBackCtrl | 4381 |
| payedDetailCtrl | 4940 |
| waitPayDetailCtrl | 7462 |
| machineOrderBrokenCtrl | 16262 |

**总计**：**7+ 个 Controller** 接收 `$stateParams.cashflowId`

---

## 9. URL 传递

### 9.1 URL string Consumer

| 行号 | Controller | param 来源 | 用途 |
|---:|---|---|---|
| 4218-4229 | deliveryListCtrl | `$stateParams.cashflowId` | printFahuoqingdan modal |
| 4373-4374 | partBackCtrl | `$stateParams.cashflowId` | printShoufei modal |
| 5140-5147 | payedListCtrl | `cashflowId: ''` + param 覆盖 | printFahuoqingdan modal |
| 5154-5157 | payedListCtrl | function param `cashflowId` | print modal |
| 35266-35270 | optometryCtrl | function param | print modal |

---

## 10. Function 参数传递

### 10.1 cashflowId 作为函数参数

| 行号 | Controller | 函数签名 |
|---:|---|---|
| 16173 | machineOrderBrokenCtrl | `$scope.processProduct = function (cashflowId, idx)` |
| 36932 | feeCashierCtrl | `$scope.showSelect = function (cashflowId)` |
| 37072 | feeDayCtrl | `$scope.showSelect = function (cashflowId)` |
| 37702 | refundFeeCtrl | `$scope.showSelect = function (cashflowId)` |

### 10.2 S1-119 纠偏（D 级冲突可能）

```javascript
// feeCashierCtrl L36932-L36940
$scope.showSelect = function (cashflowId) {  // 函数参数是 cashflowId
    $scope.cashflowId = cashflowId;
    var url = $state.href("payedDetail", { cashflowId: id });  // ← 用了 id！
};
```

**S1-119 关键发现 H（D 级冲突）**：
- **feeCashierCtrl L36940** 和 **feeDayCtrl L37080** 的 `$state.href` 使用未声明的 `id` 变量
- **D 级冲突**：要么 `id` 是闭包外变量，要么这是潜在 bug
- A 级证据：源码中**未找到** `var id` 在该函数范围内

---

## 11. Scope 传递

### 11.1 cashflowId Scope 路径

| 路径 | 行号 | Controller |
|---|---:|---|
| `$scope.cashflowId` | 多处 | 5+ Controller |
| `$scope.obj.cashflowId` | 多处 | 5+ Controller |
| `$scope.obj.creditCashflowId` | 6054 | unPayDetailCtrl |
| `this.cashflowId` (print modal) | 多处 | 5+ Controller |

**S1-119 关键发现 I**：
- **`$scope.cashflow` 与 `$scope.cashflowId` 是两条不同路径**
- **严禁** 假设 `$scope.cashflow.id` 与 `$scope.cashflowId` 同步

---

## 12. Factory 传递

### 12.1 Factory 中 cashflowId 消费

| 行号 | Controller | Factory 类型 | 用途 |
|---:|---|---|---|
| 5085 | payedListCtrl | ListFactory | getMedicalRecordCashflowVoListOfCompany |
| 8129 | waitPayListCtrl | ListFactory | getMedicalRecordCashflowVoListOfCompany |
| 16175 | machineOrderBrokenCtrl | ObjectFactory | getCanBeProcessSkuInListOfProduct |

### 12.2 Factory item.cashflowId

- `order.cashflow.id` (L20736 selectOrderListCtrl) — **唯一** Factory item.cashflowId 出现

---

## 13. cashflow 对象

### 13.1 cashflow 字段级使用情况

| 字段 | 出现位置 | 用途 | A-F |
|---|---|---|---|
| `cashflowId` | 74 处 | 主键 | A |
| `cashflow.id` | 2 处 (L7323, L20736) | 派生 creditCashflowId / cashflowId | A |
| `cashflow.medicalRecordId` | **0 处** | - | A |
| `cashflow.customerId` | **0 处** | - | A |
| `cashflow.patientId` | **0 处** | - | A |
| `cashflow.tradeNo` | **0 处** | - | A |
| `res.result.object` (整体作为 cashflowId) | 1 处 (L6929) | waitPayBackCtrl → waitPayDetail | A |

### 13.2 S1-119 关键发现 J

- **`res.result.object` 实际是 cashflow 对象整体**
- **L6929 `$state.go("waitPayDetail", { cashflowId: res.result.object })`** —— `res.result.object` 实际是 cashflow 整体，**不是** customer.id
- 这是 cashflowId 多对象派生的**实例证明**

---

## 14. 6 桥审计

### 14.1 cashflowId → customer（Charge 内部）

| 维度 | 状态 |
|---|---|
| 链 | cashflowId → getMedicalRecordCashflowVo.json → res.result.object.customer.id → getCustomerVo/getCustomerWallet/getCustomerPoint |
| Type | **B + C** |
| Controller | 2 (payedDetailCtrl + waitPayDetailCtrl) |
| Call site | 5 |

### 14.2 cashflowId → medicalRecordId（Delivery 桥接）

| 维度 | 状态 |
|---|---|
| 链 | cashflowId → getMedicalRecordPayVo.json → res.object.medicalRecord.id → $scope.medicalRecordId |
| Type | **B + C** |
| Controller | 1 (deliveryInputRecordCtrl) |
| Call site | 1 |
| medicalRecordId 后续 | **DEAD-END**（0 处消费）|

### 14.3 cashflowId → medicalProduct

| 维度 | 状态 |
|---|---|
| 链 | **未建立** |
| Type | E. 共现 |

### 14.4 cashflowId → patient

| 维度 | 状态 |
|---|---|
| 链 | **未建立** |
| Type | E. 共现 |

### 14.5 cashflowId → customerId

| 维度 | 状态 |
|---|---|
| 链 | getMedicalRecordCashflowVo → customer.id → getCustomerVo { customerId } |
| Type | **C. 同 Response 共现** |

### 14.6 cashflowId → tradeNo

| 维度 | 状态 |
|---|---|
| 链 | **未建立** |
| Type | E. 共现 |

---

## 15. 四大主链 cashflowId 分布

| Branch | Controllers | cashflowId Source |
|---|---:|---|
| **Check** | 0 | - |
| **Sale** | 1 (selectOrderListCtrl) | `order.cashflow.id` (D) |
| **Charge** | 8+ | `$stateParams.cashflowId` (B) + API Response (A) + obj (C) + URL (F) |
| **Delivery** | 4 | `$stateParams.cashflowId` (B) |
| **Other** | 7 | 多源 |

---

## 16. Bridge Matrix

| 跨 Controller 关系 | Bridge Type | 证据 |
|---|---|---|
| $stateParams.cashflowId → $scope.cashflowId | **B. State 参数** | 7+ Controller |
| $stateParams.cashflowId → $scope.obj.cashflowId | **B. State 参数** | 5+ Controller |
| res.result.object.customer.id → getCustomerVo Request | **C. API Response → Request** | 5 链 |
| res.object.medicalRecord.id → $scope.medicalRecordId | **C. API Response → Scope** | 1 链 |
| res.result.object (整体) → $state.go | **B. State 参数** | 1 链（L6929）|
| order.cashflow.id → cashflowId | **D. Factory item** | 1 链 |
| _$scope$getCashFlowCr.cashflow.id → creditCashflowId | **C. 局部变量** | 1 链 |

---

## 17. Bridge 节点

| Controller | cashflowId 命中 | 角色 |
|---|---:|---|
| **payedListCtrl** | 10 | Charge 主链 |
| **partBackCtrl** | 10 | Charge 关联 |
| **waitPayBackCtrl** | 6 | customer 桥核心（getMedicalRecordCashflowVo + VoList）|
| **deliveryListCtrl** | 6 | Delivery 主链（printFahuoqingdan）|
| **deliveryInputRecordCtrl** | 4 | medicalRecordId 桥核心（getMedicalRecordPayVo）|
| **feeCashierCtrl** | 4 | showSelect + $state.href |

**S1-119 关键发现 K**：
- **payedListCtrl / partBackCtrl 是 cashflowId 最高频 Controller**（各 10 处）
- **waitPayBackCtrl 是 customer 桥核心节点**
- **deliveryInputRecordCtrl 是 medicalRecordId 桥核心节点**

---

## 18. Multiple Provenance

### 18.1 7 种 Source 互不相依

| Source | Controller | 互不相依？ |
|---|---|---|
| A. API Response | unPayDetailCtrl / waitPayBackCtrl | 是 |
| B. StateParams | 7+ Controller | 是 |
| C. Scope | 20 Controller (内部传递) | 派生 A/B |
| D. Factory item | selectOrderListCtrl | 是 |
| E. Function param | 5+ Controller | 是 |
| F. URL string | 3+ Controller | 派生 B |
| G. Constant | 5+ Controller (空字符串) | 是 |
| H. 派生字段 | 2 Controller (cashflow.id) | 是 |

**S1-119 关键发现 L**：
- **A、B、D、E、G、H 是 5 个独立**第一来源**
- **C、F 是派生**（C 从 A/B 派生，F 从 B 派生）
- **严禁** 假设"一个主来源"

---

## 19. medicalRecordId 对照

### 19.1 两条 cashflowId 派生链

| 链 | 起点 | 终点 | Controller | Type |
|---|---|---|---|---|
| **cashflowId → customer.id** | `$stateParams.cashflowId` | `getCustomerVo.json { customerId }` | 2 | B + C |
| **cashflowId → medicalRecord.id** | `$stateParams.cashflowId` | `$scope.medicalRecordId` (dead-end) | 1 | B + C |
| **cashflowId → res.result.object (整体)** | `$stateParams.cashflowId` | `$state.go("waitPayDetail", { cashflowId: res.result.object })` | 1 (L6929) | B + C |

**S1-119 关键发现 M**：
- **cashflowId 至少服务 3 个不同对象**（customer / medicalRecord / cashflow 整体）
- 三条链**完全独立**（不同 API / 不同 Controller / 不同 Response 字段）

### 19.2 waitChargeDetailCtrl 独立路径

| 链 | 起点 | 终点 | Controller | Type |
|---|---|---|---|---|
| `medicalRecordId` → `medicalRecord.patientId` | `$stateParams.medicalRecordId` | `getPatientInfo.json { id }` | 1 (waitChargeDetailCtrl L6693) | B + C |

**S1-119 关键发现 N**：
- waitChargeDetailCtrl **不**依赖 cashflowId 桥接 medicalRecord
- 直接从 `$stateParams.medicalRecordId` 入口
- medicalRecord.patientId 来自 computeUnPlaceOrderMedicalRecordFee.json Response
- 这是与 cashflowId 桥**完全独立**的 medicalRecord 派生路径

---

## 20. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | 全局命中数 | 74（Case-Sensitive）/ 20 Controller | A | L1 |
| 02 | Controller 数 | 20 | A | L1 |
| 03 | 函数数 | 5+ Controller 显式函数 | A | L1 |
| 04 | expression 路径全集 | 7 大类 | A | L1 |
| 05 | API Response 来源 | 4 处 | A | L1 |
| 06 | API Request 消费 | 13+ API | A | L1 |
| 07 | StateParams | 7+ Controller | A | L1 |
| 08 | State 传递 | 1 $state.go + 2 $state.href | A | L1 |
| 09 | URL 传递 | 3+ Controller | A | L1 |
| 10 | Scope 传递 | 20 Controller | A | L1 |
| 11 | Factory 传递 | 4 Controller | A | L1 |
| 12 | 函数参数传递 | 5+ Controller | A | L1 |
| 13 | cashflow 对象 | 1 Controller (L20736) | A | L1 |
| 14 | cashflow.id | 2 Controller | A | L1 |
| 15 | cashflow.customerId | 0 处 | A | L1 |
| 16 | cashflow.patientId | 0 处 | A | L1 |
| 17 | cashflow.medicalRecordId | 0 处 | A | L1 |
| 18 | tradeNo | 0 处 | A | L1 |
| 19 | customer 桥 | B + C（5 链）| A | L1 |
| 20 | medicalRecordId 桥 | B + C（1 链，dead-end）| A | L1 |
| 21 | medicalProduct 桥 | F. 未建立 | A | L1 |
| 22 | patient 桥 | F. 未建立 | A | L1 |
| 23 | 四大主链 | Charge 8+ / Delivery 4 / Sale 1 / Check 0 | A | L1 |
| 24 | Bridge Matrix | 7 类 | A | L1 |
| 25 | Multiple Provenance | 5 独立第一来源 | A | L1 |
| 26 | A/B/C/D/E/F | A: 25 / F: 1 | A | L1 |

### 20.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 25 | 96% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 1 | 4% |

### 20.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 21. A-F 总结

- **A 级**：25 项（96%）
- **F 级**：1 项（HTML 边界）
- **B/C/D/E 级**：0

---

## 22. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0
- **L3**：0

---

## 23. F 边界

| F 项 | 详情 |
|---|---|
| 1 | HTML 模板 | 全部 F 边界 |
| 2 | State 配置 | 0 处 .state() in controller.js |
| 3 | API Response 完整 schema | 仅已知 1 字段（res.result.object）|

---

## 24. 复刻风险（L1）

### 24.1 关键注意事项

1. **cashflowId 多源问题**
   - **5 个独立第一来源**（API Response / StateParams / Factory item / Function param / Constant）
   - **严禁** 假设"主来源"

2. **State/API/URL 三种传递方式并存**

3. **customer 与 medicalRecordId 两条独立桥**

4. **medicalRecordId 桥 dead-end**

5. **D 级冲突可能**：feeCashierCtrl L36940 / feeDayCtrl L37080 用 `id` 而非 `cashflowId`

6. **cashflow.id 与 cashflowId 路径差异**

7. **L6929 整体 cashflow 传递**

---

## 25. 关键纠偏（S1-119 vs S1-115/117/118）

| 旧结论 | 新结论 | 依据 |
|---|---|---|
| S1-115: 6 Controller 涉及 cashflowId | **20 Controller** | S1-119 全局扫描 |
| S1-115/118: cashflowId 27 处 | **74 处**（Case-Sensitive）| S1-119 重新统计 |
| S1-118: getMedicalRecordCashflowVo Response 是 cashflow + customer 整体 | **L6929 确认 res.result.object 整体作为 cashflowId 传递** | S1-119 重新审计 |
| S1-117: cashflowId → medicalRecordId 1 个 Controller | **保持**（deliveryInputRecordCtrl）| S1-119 重扫 |
| S1-118: cashflowId → customer 是 5 链 | **保持 5 链** | S1-119 重扫 |
| **S1-119 新增** | **feeCashierCtrl L36940 / feeDayCtrl L37080 潜在 bug** | S1-119 重新审计 |
| **S1-119 新增** | **L6929 res.result.object 整体作为 cashflowId 传递** | S1-119 重新审计 |

---

## 26. Final cashflowId DAG

```
[多个独立第一来源]
├─ A. API Response (3 Controller)
├─ B. StateParams ($stateParams.cashflowId) (7+ Controller)
├─ D. Factory item (1 Controller)
├─ E. Function param (5+ Controller)
├─ G. Constant (5+ Controller)
└─ H. 派生 cashflow.id (2 Controller)
  ↓
[Scope 传递]
$scope.cashflowId / $scope.obj.cashflowId (20 Controller)
  ↓
[API Request] (13+ API)
  ↓ Response
[API Response 提供]
├─ customer.id (5 Controller 消费 → 3 个后续 API)
├─ medicalRecord.id (1 Controller 消费 → dead-end)
├─ res.result.object (1 Controller 消费 → 整体传递)
└─ VoList (1 Controller 消费)
  ↓
[State 传递]
├─ $state.go("waitPayDetail", { cashflowId: res.result.object }) (L6929)
└─ $state.href("payedDetail", { cashflowId: id }) (L36940, L37080) [D 级冲突]
```

---

## 27. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不调用任何 API | ✅ |
| 5. 不打开真实生产系统 | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-118 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-180） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 10 untracked + 1 gitignored 原样保留 | ✅ |
| 14. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 28. 最终结论

### 28.1 cashflowId 全局特征

- **74 Case-Sensitive 出现**（A 级）
- **20 Controller 涉及**（A 级）
- **7 大 Source 类型**（多源，5 独立第一来源）
- **主导来源**：B. StateParams（7+ Controller，~50% Controller 使用）
- **3 个独立桥**：customer / medicalRecord / cashflow 整体

### 28.2 4 大主链 cashflowId 分布

| 主链 | Controller | 角色 |
|---|---:|---|
| Check | 0 | - |
| Sale | 1 | selectOrderListCtrl (D. Factory item) |
| Charge | 8+ | 主消费（含 customer 桥 5 Controller）|
| Delivery | 4 | 消费 F1/F2/F3/F4/F5/F6（cashflowId 入口）|

### 28.3 S1-119 关键发现

1. **cashflowId 是多源字段**（**严禁** 假设"主来源"）
2. **5 个独立第一来源**（A/B/D/E/G/H）
3. **cashflowId 可服务多个对象**（customer / medicalRecord / cashflow 整体）
4. **L6929 整体 cashflow 传递**（**S1-119 全新发现**）
5. **D 级冲突可能**：feeCashierCtrl L36940 / feeDayCtrl L37080
6. **waitChargeDetailCtrl 独立路径**（不依赖 cashflowId）

---

**审计完成。本文档为 181 号，提交后将形成 tracked=189，untracked=10，ignored=1。**
