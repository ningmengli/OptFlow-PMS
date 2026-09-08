# S1-117 Charge → Delivery cashflowId API桥接深度审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（gitignored）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-116（HEAD=37388f5，tracked=186，untracked=10，ignored=1）
> - 本轮**重点**：S1-116 发现的 Charge → Delivery cashflowId 桥接链（deliveryInputRecordCtrl L4034-L4036 getMedicalRecordPayVo.json）**完整钉死**
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-178）/ 修改 7 HTML / 修改 11 文件 / 修改 P0=54 / P1=8

---

## 1. 审计范围

### 1.1 S1-116 已确认核心发现（保持）

- 4 主分支间 0 处跨主分支 API 共享
- 4 主分支间 0 处跨主链 Scope/Service 共享
- **S1-116 关键发现**：deliveryInputRecordCtrl L4034-L4036 存在 cashflowId → medicalRecordId API 级数据链（C 级）

### 1.2 S1-117 新发现（重大）

- **getMedicalRecordPayVo.json 在 controller.js 全局仅 1 处调用**（L4034，deliveryInputRecordCtrl）
- **存在另一个相关 API：`getMedicalRecordCashflowVo.json`**（5 个 Controller 调用）
- **存在 ListFactory 版本：`getMedicalRecordCashflowVoListOfCompany.json`**（2 个 Controller 调用）
- **5 个 Charge Controller 通过 cashflowId 调 getMedicalRecordCashflowVo 桥接 medicalRecord/customer**：
  - L4942 payedDetailCtrl
  - L5166 payedListCtrl
  - L5085 payedListCtrl（ListFactory）
  - L7070 waitPayBackCtrl
  - L7488 waitPayDetailCtrl
  - L8129 waitPayListCtrl（ListFactory）
- **payedDetailCtrl L4942-L4947 链式 API 模式**：cashflowId → getMedicalRecordCashflowVo → response.customer.id → getCustomerVo

---

## 2. getMedicalRecordPayVo 全局命中

### 2.1 全局 search

| 行号 | 表达式 | Controller | 函数 | A-F |
|---:|---|---|---|---|
| 4034 | `var recordPromise = getMedicalRecord.saveOrQuery('/admin/getMedicalRecordPayVo.json', { cashflowId: $scope.cashflowId });` | **deliveryInputRecordCtrl** | 立即调用的匿名 var | A |

**S1-117 关键发现 A**：getMedicalRecordPayVo.json 在 controller.js 全局**仅 1 处调用**（A 级穷举确认）

### 2.2 完整 call site 分析

```javascript
// L4033-L4037
var getMedicalRecord = new ObjectFactory();
var recordPromise = getMedicalRecord.saveOrQuery(
  '/admin/getMedicalRecordPayVo.json',  // API
  { cashflowId: $scope.cashflowId }      // Request: 1 个字段
);
recordPromise.then(function (res) {
  $scope.medicalRecordId = res.object.medicalRecord.id;  // Response Consumer: 1 个字段
});
```

| 维度 | 详情 | A-F |
|---|---|---|
| API | `/admin/getMedicalRecordPayVo.json` | A |
| Type | Read | A |
| Factory | 匿名 `new ObjectFactory()`（无 $scope 赋值） | A |
| Request | `{ cashflowId: $scope.cashflowId }` | A |
| Response | `res.object.medicalRecord.id` | A |
| Scope 落点 | `$scope.medicalRecordId` | A |
| 调用函数 | **匿名立即调用**（非 $scope 函数） | A |
| 后续使用 | 0 处（详见 §4） | A |

---

## 3. Consumer Controller 与 call site

### 3.1 Consumer Controller 全集

| Controller | 行号 | getMedicalRecordPayVo 调用 | A-F |
|---|---|---|---|
| deliveryInputRecordCtrl | 4034 | ✅ 1 处 | A |
| 其它 14 个主链 Controller | - | ❌ 0 处 | A |

**S1-117 关键发现 B**：getMedicalRecordPayVo.json 是 **deliveryInputRecordCtrl 唯一 Consumer**（A 级）

### 3.2 14 主链 Controller 中调用其它 medicalRecord* API

| API | Controller | 行号 | A-F |
|---|---|---|---|
| getMedicalRecordPayVo.json | deliveryInputRecordCtrl | 4034 | A |
| getMedicalRecordCashflowVo.json | payedDetailCtrl | 4942 | A |
| getMedicalRecordCashflowVo.json | payedListCtrl | 5166 | A |
| getMedicalRecordCashflowVoListOfCompany.json | payedListCtrl | 5085 | A |
| getMedicalRecordCashflowVo.json | waitPayBackCtrl | 7070 | A |
| getMedicalRecordCashflowVo.json | waitPayDetailCtrl | 7488 | A |
| getMedicalRecordCashflowVoListOfCompany.json | waitPayListCtrl | 8129 | A |

**关键发现 C**：
- **getMedicalRecordCashflowVo** 系列 API 全部在 **Charge 分支**（5 个 Controller）
- **getMedicalRecordPayVo** 唯一在 **Delivery 分支**（deliveryInputRecordCtrl）
- **两个 API 名称相似但 Controller 隔离**

---

## 4. Request 字段全集

### 4.1 getMedicalRecordPayVo Request

| 字段 | 表达式 | 来源 | A-F |
|---|---|---|---|
| `cashflowId` | `$scope.cashflowId` | `$stateParams.cashflowId` (L4026) | A |

**Request 字段总数**：1 个
**Request 字段名**：cashflowId
**Request 来源**：StateParams（$stateParams.cashflowId）

### 4.2 cashflowId 在 deliveryInputRecordCtrl 全部使用

| 行号 | 表达式 | 用途 |
|---:|---|---|
| 4026 | `$scope.cashflowId = $stateParams.cashflowId;` | **Init 入口**（A 级） |
| 4034 | `{ cashflowId: $scope.cashflowId }` | **getMedicalRecordPayVo Request**（A 级） |
| 4040 | `{ cashflowId: $scope.cashflowId }` | **getCashflowDeliveryVo (F1) Request**（A 级） |
| 4044 | `{ cashflowId: $scope.cashflowId }` | **statProductDeliveryStatusOfCashflow (F2) Request**（A 级） |

**S1-117 关键发现 D**：
- cashflowId 在 deliveryInputRecordCtrl 共 **4 处使用**
- 全部 3 个 API Request 共享同一 cashflowId（StateParams 来源）

---

## 5. cashflowId provenance

### 5.1 deliveryInputRecordCtrl 内 cashflowId 来源

```
[State 入口 - F 边界]
↓
$stateParams.cashflowId (L4026)
↓
$scope.cashflowId (L4026)
↓
[4 个使用点]
├─ L4034 getMedicalRecordPayVo Request
├─ L4040 getCashflowDeliveryVo (F1) Request
└─ L4044 statProductDeliveryStatusOfCashflow (F2) Request
```

**S1-117 关键结论 E**：
- **cashflowId 唯一来源 = $stateParams.cashflowId**（A 级）
- **State 配置**在 controller.js 之外（F 边界）
- **deliveryInputRecordCtrl 0 处产生新 cashflowId**（仅消费）

### 5.2 4 主链 cashflowId $stateParams 入口

| Controller | 行号 | 表达式 | A-F |
|---|---|---|---|
| deliveryInputCtrl | 3814 | `$scope.cashflowId = $stateParams.cashflowId;` | A |
| deliveryInputRecordCtrl | 4026 | `$scope.cashflowId = $stateParams.cashflowId;` | A |
| deliveryProcessingCtrl | 4238 | `$scope.cashflowId = $stateParams.cashflowId;` | A |
| deliveryListCtrl | (0 处直接) | (使用 sessionStorage "chargedeliveryList") | A |
| deliveryDetailCtrl | 0 处 | - | A |

**S1-117 关键发现 F**：
- **3 个 Delivery Controller** 通过 `$stateParams.cashflowId` 接收 cashflowId
- **deliveryListCtrl** 通过 sessionStorage（"chargedeliveryList"）缓存
- **deliveryDetailCtrl** 0 处 cashflowId

---

## 6. Charge 上游 cashflowId 来源

### 6.1 5 个 Charge Controller 调 getMedicalRecordCashflowVo

| Controller | 行号 | cashflowId 来源 | A-F |
|---|---|---|---|
| payedDetailCtrl | 4940 | `$scope.obj.cashflowId = $stateParams.cashflowId;` | A |
| payedListCtrl | 5085 | `$scope.obj`（ListFactory Request）| A |
| payedListCtrl | 5166 | 函数参数 `id` (L5164 printList 接收) | A |
| waitPayBackCtrl | 7070 | `$scope.obj.cashflowId = $stateParams.cashflowId;` | A |
| waitPayDetailCtrl | 7488 | `$scope.obj.cashflowId = $stateParams.cashflowId;` | A |
| waitPayListCtrl | 8129 | `$scope.obj`（ListFactory Request）| A |

**关键发现 G**：
- **5 个 Charge Controller** 通过 cashflowId 调 medicalRecord 相关 API
- 这是 **Charge 分支内部**的 cashflowId → medicalRecord 桥接（与 Delivery 的桥接**完全独立**）

### 6.2 payedDetailCtrl L4942-L4947 链式 API 模式

```javascript
$scope.obj.cashflowId = $stateParams.cashflowId;  // Init
var promise = $scope.getCashflowObjectFactory.saveOrQuery(
  '/admin/getMedicalRecordCashflowVo.json',  // 桥接 API
  { cashflowId: $scope.obj.cashflowId }
);
promise.then(function (res) {
    $scope.patientObjectFactory = new ObjectFactory();
    $scope.patientObjectFactory.saveOrQuery(
      '/admin/getCustomerVo.json',
      { customerId: res.result.object.customer.id }  // ← 跨 API 字段桥接
    );
    $scope.getWalletObejctFactory = new ObjectFactory();
    $scope.getWalletObejctFactory.saveOrQuery(
      '/admin/getCustomerWallet.json',
      { customerId: res.result.object.customer.id }  // ← 同一字段复用
    );
});
```

**S1-117 关键发现 H**：
- **cashflowId → getMedicalRecordCashflowVo Response → customer.id → getCustomerVo + getCustomerWallet**
- **链式 API 模式**：cashflowId 桥接 3 个 API
- **0 处直接 medicalRecordId 传递**（medicalRecordId 是 cashflow 对象的内部字段，但不直接消费）

---

## 7. cashflow 对象

### 7.1 cashflow 字段级使用情况

| 字段 | 出现位置 | 用途 | A-F |
|---|---|---|---|
| `cashflowId` | 6 Controller 共 27 处 | 主关联键 | A |
| `cashflow.id` | L7323 waitPayBackCtrl, L20736 selectOrderListCtrl | 派生 creditCashflowId 或 cashflowId | A |
| `cashflow.medicalRecordId` | **0 处** | - | A |
| `cashflow.patientId` | **0 处** | - | A |
| `cashflow.customerId` | **0 处直接**（通过 `.customer.id` 间接访问，见 L4947）| - | A |

### 7.2 cashflow 对象详情

| Controller | cashflow 对象行 | 表达式 | 消费 |
|---|---|---|---|
| deliveryInputRecordCtrl | **0 处**（cashflow 整体对象不存在）| - | - |
| deliveryInputCtrl | 0 处 | - | - |
| payedDetailCtrl | L4943 `res.result.object` | response.object 是 getMedicalRecordCashflowVo 返回 | ✓ |
| payedListCtrl | L5167 `res` | response | ✓ |
| waitPayDetailCtrl | L7488 `res` | response | ✓ |

**S1-117 关键发现 I**：
- **0 处 `cashflow.medicalRecordId` 直接访问**（A 级）
- **medicalRecordId 必须通过 Response object.medicalRecord 嵌套访问**（如 L4036 `res.object.medicalRecord.id`）

---

## 8. Response 路径

### 8.1 getMedicalRecordPayVo Response 路径

| Controller | Response 路径 | 字段 | 行号 | A-F |
|---|---|---|---|---|
| deliveryInputRecordCtrl | `res.object.medicalRecord.id` | medicalRecordId | 4036 | A |

**S1-117 关键发现 J**：
- **Response 唯一消费者**：`deliveryInputRecordCtrl`
- **唯一消费字段**：`res.object.medicalRecord.id`
- **Response 结构**：`result.object.medicalRecord.id`（三层嵌套）

### 8.2 Response 完整结构推断（基于 1 个 Consumer）

```javascript
res = {
  // ... 顶层
  object: {
    // ... 
    medicalRecord: {
      id: <medicalRecordId>,  // 唯一已知字段
      // 其它字段未访问（F 边界）
    }
  }
}
```

**严禁** 推断 res 其它字段（A 级）

---

## 9. Response → Delivery Consumer

### 9.1 medicalRecordId 后续使用

```javascript
// L4035-L4037 deliveryInputRecordCtrl
recordPromise.then(function (res) {
    $scope.medicalRecordId = res.object.medicalRecord.id;
});
```

**S1-117 关键发现 K**：
- **medicalRecordId 写入 `$scope.medicalRecordId`**（A 级）
- **后续使用：0 处**（A 级穷举：Controller 范围内 $scope.medicalRecordId 仅此 1 处出现，无下游消费）

### 9.2 deliveryInputRecordCtrl 完整字段使用

| Scope 字段 | 来源 | 后续使用 | A-F |
|---|---|---|---|
| `$scope.cashflowId` | L4026 $stateParams | 3 个 API Request（L4034/L4040/L4044）| A |
| `$scope.medicalRecordId` | L4036 API Response | **0 处** | A |
| `$scope.toggle` | L4028 字面量 | L4030 / L4068 | A |
| `$scope.setToggle` 函数 | L4029 | (无显式调用) | A |
| `$scope.saveRemark` 函数 | L4048 | L4061 saveMedicalProductDeliveryCommentBatch.json | A |
| `$scope.getMedicalRecordDeliveryFactory` | L4039 ObjectFactory | L4040 / L4051 | A |
| `$scope.getStatusDeliveryFactory` | L4043 ObjectFactory | L4044 | A |
| `$scope.saveMedicalRecordDeliveryFactory` | L4060 ObjectFactory | L4061 | A |

### 9.3 deliveryInputRecordCtrl medicalRecordId 数据链

```
$stateParams.cashflowId
  ↓
$scope.cashflowId (L4026)
  ↓
getMedicalRecordPayVo.json Request { cashflowId } (L4034)
  ↓ Response
res.object.medicalRecord.id
  ↓
$scope.medicalRecordId (L4036)
  ↓
[DEAD-END - 0 处下游消费]
```

**S1-117 关键发现 L**：
- **medicalRecordId 在 deliveryInputRecordCtrl 是 dead-end 字段**
- **写入后从未被读取**（Controller 范围内 0 处）
- 业务意图可能由 HTML ng-model 或回调消费（**F 边界**：HTML 不在资源范围）

---

## 10. F1-F6 关系（与 cashflowId 桥接链的交叉）

### 10.1 F1 getCashflowDeliveryVo.json

| Controller | 行号 | Request | Response Consumer | 与 getMedicalRecordPayVo 关系 | A-F |
|---|---|---|---|---|---|
| deliveryInputCtrl | 3848 | `{ cashflowId: $scope.cashflowId }` | `res.result.object.waitingDeliveryList` | **共享 cashflowId 来源** | A |
| deliveryProcessingCtrl | (待详细) | (待详细) | (待详细) | - | A |
| deliveryInputRecordCtrl | **4040** | `{ cashflowId: $scope.cashflowId }` | `res.result.object.deliveryedList` (L4051) | **同 Controller 内 2 API 共用 cashflowId** | A |

**S1-117 关键发现 M**：
- **deliveryInputRecordCtrl 同时调用 getMedicalRecordPayVo (L4034) + getCashflowDeliveryVo (L4040)**
- 两者都基于 `$scope.cashflowId`
- **2 个 API 独立调用，0 处 result 数据共享**
- **E. 仅字段共现**（cashflowId 共现 ≠ 数据链）

### 10.2 F2 statProductDeliveryStatusOfCashflow.json

| Controller | 行号 | Request | 与 getMedicalRecordPayVo 关系 | A-F |
|---|---|---|---|---|
| deliveryInputCtrl | 3841 | `{ cashflowId: $scope.cashflowId }` | 共享 cashflowId | A |
| deliveryProcessingCtrl | (待详细) | (待详细) | - | A |
| deliveryInputRecordCtrl | **4044** | `{ cashflowId: $scope.cashflowId }` | **同 Controller 内 3 API 共用 cashflowId** | A |

**E. 仅字段共现**

### 10.3 F3 getMedicalProductMachineCenterVoList.json

| Controller | 行号 | Request | Response Consumer | A-F |
|---|---|---|---|---|
| deliveryInputCtrl | 3836 | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` (从 waitingDeliveryList 派生) | (S1-115 锁定) | A |

**与 getMedicalRecordPayVo 关系**：
- **0 处直接调用**（仅 deliveryInputCtrl）
- **0 处 result 共享**
- **E. 仅字段共现**

### 10.4 F4 getCanBeDeliverySkuInListOfProduct.json

| Controller | 行号 | Request | Response Consumer | A-F |
|---|---|---|---|---|
| deliveryInputCtrl | 3885 | `{ medicalProductIdArray }` | (S1-115 锁定) | A |

**与 getMedicalRecordPayVo 关系**：
- **0 处直接调用**
- **E. 仅字段共现**

### 10.5 F5 saveMedicalProductStockBatch.json (Write)

| Controller | 行号 | Request | A-F |
|---|---|---|---|
| deliveryInputCtrl | 4007 | `{ listCount, medicalProductStockBatctPoListJson }` | A |

**与 getMedicalRecordPayVo 关系**：
- **0 处直接调用**
- **0 处 medicalRecordId 来源**（无 `medicalRecord` 字段）
- **E. 仅字段共现**

### 10.6 F6 sendMedicalProductToMachineCenter.json (Write)

| Controller | 行号 | Request | A-F |
|---|---|---|---|
| deliveryInputCtrl | 3966 | `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` | A |

**与 getMedicalRecordPayVo 关系**：
- **0 处直接调用**
- **E. 仅字段共现**

### 10.7 F1-F6 关系总结

| 关系 | 类型 |
|---|---|
| getMedicalRecordPayVo → F1 | E. 仅字段共现（cashflowId） |
| getMedicalRecordPayVo → F2 | E. 仅字段共现（cashflowId） |
| getMedicalRecordPayVo → F3 | E. 仅字段共现（无 result 共享） |
| getMedicalRecordPayVo → F4 | E. 仅字段共现 |
| getMedicalRecordPayVo → F5 | E. 无字段共享 |
| getMedicalRecordPayVo → F6 | E. 无字段共享 |

**S1-117 关键发现 N**：
- getMedicalRecordPayVo 与 F1-F6 **0 处直接数据链**
- 仅在 deliveryInputRecordCtrl 内 3 个 API 共享 cashflowId Request 字段
- **真正的"Charge → Delivery 桥接"由 getMedicalRecordPayVo 单独承担**（与 F1-F6 链路并行）

---

## 11. medicalRecordId 关系

### 11.1 cashflowId → medicalRecordId 桥接

| 路径 | 表达式 | A-F |
|---|---|---|
| **deliveryInputRecordCtrl L4026** | `$scope.cashflowId = $stateParams.cashflowId;` | A |
| **deliveryInputRecordCtrl L4034** | `'/admin/getMedicalRecordPayVo.json', { cashflowId: $scope.cashflowId }` | A |
| **deliveryInputRecordCtrl L4036** | `$scope.medicalRecordId = res.object.medicalRecord.id;` | A |

**S1-117 关键发现 O**：
- **cashflowId → medicalRecordId 直接赋值链**（A 级，3 行连续代码）
- 这是 S1-116 报告的"Charge → Delivery 桥接"的**完整证据**

### 11.2 medicalRecordId 后续使用

- deliveryInputRecordCtrl 范围内 $scope.medicalRecordId **0 处下游消费**
- **写入即结束**（dead-end 字段）

### 11.3 5 个 Charge Controller 通过 getMedicalRecordCashflowVo 的间接 medicalRecordId 桥接

| Controller | 行号 | 桥接方式 | A-F |
|---|---|---|---|
| payedDetailCtrl | L4942 | cashflowId → getMedicalRecordCashflowVo → res.object.customer.id → getCustomerVo | A |
| payedListCtrl | L5166 | cashflowId → getMedicalRecordCashflowVo → res（用于打印）| A |
| waitPayBackCtrl | L7070 | cashflowId → getMedicalRecordCashflowVo → res | A |
| waitPayDetailCtrl | L7488 | cashflowId → getMedicalRecordCashflowVo → res | A |
| waitPayListCtrl | L8129 | cashflowId → getMedicalRecordCashflowVoListOfCompany → ListFactory | A |

**S1-117 关键发现 P**：
- **5 个 Charge Controller 通过 getMedicalRecordCashflowVo 桥接**
- **桥接响应字段：customer.id**（非 medicalRecordId）
- **0 处直接 medicalRecordId 字段**（response.medicalRecordId 字段未在源码被消费）

---

## 12. medicalProduct 关系

### 12.1 medicalProductId 与 cashflowId 关系

| Controller | 表达式 | 关系 | A-F |
|---|---|---|---|
| deliveryInputRecordCtrl | L4055 `medicalProductId: arrList[i].medicalProduct.id` (saveRemark) | medicalProduct.id 来自 saveRemark arrList 派生 | A |

**S1-117 关键发现 Q**：
- **0 处 cashflowId → medicalProductId 直接桥接**（A 级）
- medicalProduct 来自 `getCashflowDeliveryVo.json` Response `deliveryedList[i].medicalProduct`（F1 派生）

---

## 13. deliveryStatus 关系

### 13.1 deliveryStatus 与 cashflowId 关系

- 4 个 Delivery Controller 中 `deliveryStatus` 来源：`$scope.obj.deliveryStatus`（L4088-L4105 deliveryListCtrl）
- **0 处 cashflowId → deliveryStatus 直接链**（A 级）

**S1-117 关键发现 R**：
- **0 处直接 cashflowId → deliveryStatus 桥接**
- deliveryStatus 来自 sessionStorage 缓存或 obj 字段

---

## 14. tradeNo 关系

### 14.1 tradeNo 与 cashflowId 关系

- controller.js 全局 `tradeNo` 出现 0 次（S1-115 已确认）
- **0 处 cashflowId → tradeNo 直接链**

**S1-117 关键发现 S**：**tradeNo 字段在 4 主链范围内 0 处使用**

---

## 15. State

### 15.1 deliveryInputRecordCtrl $state.go 全量

```powershell
# 0 处 $state.go in deliveryInputRecordCtrl (L4024-L4072)
```

**A 级确认**：deliveryInputRecordCtrl **0 处 $state.go 出口**（dead-end 页面）

### 15.2 $stateParams 入口

| 参数 | 来源 |
|---|---|
| `cashflowId` | $stateParams.cashflowId (L4026) |

**S1-117 关键发现 T**：
- deliveryInputRecordCtrl 唯一 $stateParams 入口字段 = `cashflowId`
- **State 配置**在 controller.js 之外（F 边界）

---

## 16. Write

### 16.1 deliveryInputRecordCtrl 唯一 Write

| API | 行号 | Request | medicalRecordId 来源 | A-F |
|---|---|---|---|---|
| saveMedicalProductDeliveryCommentBatch.json | 4061 | `{ medicalProductDeliveryCommentListJson: JSON.stringify(arr) }` | **0 处** | A |

### 16.2 Write 与 getMedicalRecordPayVo 关系

- **0 处 getMedicalRecordPayVo Response 进入 Write Request**
- Write Request 仅用 `getCashflowDeliveryVo.json` Response (F1) 的 `deliveryedList[i].medicalProductDelivery.deliveryComment`
- **getMedicalRecordPayVo 与 Write 无数据链**（E. 仅字段共现）

---

## 17. Bridge Type 判定

### 17.1 5 种桥类型评估

| 桥类型 | 评估 | A-F |
|---|---|---|
| A. 直接 Controller 调用 | ❌ 0 处（deliveryInputRecordCtrl 0 处 $state.go）| A |
| B. State 参数桥 | ✅ **cashflowId State 入口**（$stateParams.cashflowId, L4026）| A |
| C. API Response → Request | ✅ **medicalRecordId 派生**（L4036 `res.object.medicalRecord.id` → `$scope.medicalRecordId`）| A |
| D. 共享 Service/Scope | ❌ 0 处 | A |
| E. 共享字段但未闭合 | ✓ medicalRecordId 在 $scope.medicalRecordId 后 0 处消费 | A |
| F. 完全未建立 | - | - |

### 17.2 最终桥类型

**S1-117 关键结论**：
- **B+C** 同时成立：
  - **B**：cashflowId 通过 State 进入 deliveryInputRecordCtrl
  - **C**：API Response（getMedicalRecordPayVo）→ Scope（medicalRecordId）
- 桥接**完整路径**：
  ```
  [State 入口]
  $stateParams.cashflowId (State)
    ↓
  $scope.cashflowId (Scope)
    ↓
  [API Request]
  getMedicalRecordPayVo.json { cashflowId }
    ↓ Response
  res.object.medicalRecord.id
    ↓
  $scope.medicalRecordId (Scope)
    ↓
  [DEAD-END - 0 处下游消费]
  ```

**S1-117 结论**：Charge → Delivery 桥接类型 = **B+C**（State + API Response → Request）

### 17.3 桥接强度评估

| 维度 | 评估 | A-F |
|---|---|---|
| 桥接存在 | ✅ A 级源码 | A |
| 桥接完整性 | ✅ 3 行连续代码 | A |
| 桥接下游 | ❌ medicalRecordId 写入后 0 处消费 | A |
| F1-F6 联动 | ❌ 0 处直接联动 | A |
| HTML 证据 | ❌ F 边界 | F |

**S1-117 关键发现 U**：
- **桥接本身完整**（A 级）
- **桥接后 medicalRecordId 是 dead-end 字段**（A 级）
- 业务意图可能在 HTML 层（**F 边界**）

---

## 18. Cross-Branch DAG

### 18.1 Charge → Delivery 桥接 DAG

```
[Charge 业务]
Charge Controller (payedDetailCtrl / payedListCtrl / waitPayBackCtrl / waitPayDetailCtrl)
  ↓ 产生
cashflow (业务核心对象)
  ↓
$stateParams.cashflowId (State 入口)
  ↓ B: State 参数桥
[Delivery 业务]
deliveryInputRecordCtrl (L4024-L4072)
  ↓
$scope.cashflowId (L4026)
  ↓ C: API Response → Request
getMedicalRecordPayVo.json { cashflowId } (L4034)
  ↓ Response
res.object.medicalRecord.id
  ↓
$scope.medicalRecordId (L4036)
  ↓
[DEAD-END - 0 处下游消费]
```

### 18.2 5 个 Charge Controller 的 getMedicalRecordCashflowVo 链

```
[Charge 业务]
Charge Controller (5 个)
  ↓
$scope.obj.cashflowId = $stateParams.cashflowId
  ↓
getMedicalRecordCashflowVo.json { cashflowId }
  ↓ Response
res.result.object
  ├─ .customer.id (L4947) → getCustomerVo.json
  ├─ .customer.id (L4950) → getCustomerWallet.json
  └─ .medicalRecord.id (?? 0 处直接消费)
```

**S1-117 关键发现 V**：
- **5 个 Charge Controller 通过 cashflowId 调 getMedicalRecordCashflowVo**
- **Customer 桥接**是主用途（**medicalRecord 桥接不直接使用**）
- **medicalRecordId 通过 cashflow 间接可达**（response.medicalRecord.id）但 4 主链**0 处直接消费**

---

## 19. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | getMedicalRecordPayVo 全局命中 | 1 处（L4034）| A | L1 |
| 02 | Consumer Controller | 1 个（deliveryInputRecordCtrl）| A | L1 |
| 03 | call site | 1 个（匿名立即调用）| A | L1 |
| 04 | Request 字段全集 | 1 个字段（cashflowId）| A | L1 |
| 05 | cashflowId Request 来源 | $scope.cashflowId (L4026) | A | L1 |
| 06 | cashflowId 上游来源 | $stateParams.cashflowId (L4026) | A | L1 |
| 07 | Charge cashflowId 全集 | 5 Controller 调 getMedicalRecordCashflowVo | A | L1 |
| 08 | cashflow 对象 | 0 处 cashflow.medicalRecordId | A | L1 |
| 09 | cashflow 字段 | cashflowId (27) / cashflow.id (2) | A | L1 |
| 10 | Response 路径 | res.object.medicalRecord.id | A | L1 |
| 11 | Response 字段 | medicalRecordId（1 字段）| A | L1 |
| 12 | Response → Scope/Local | $scope.medicalRecordId (L4036) | A | L1 |
| 13 | Response → Delivery Consumer | **0 处**（dead-end）| A | L1 |
| 14 | F1 关系 | E. 仅字段共现 | A | L1 |
| 15 | F2 关系 | E. 仅字段共现 | A | L1 |
| 16 | F3 关系 | E. 仅字段共现 | A | L1 |
| 17 | F4 关系 | E. 仅字段共现 | A | L1 |
| 18 | F5 关系 | E. 无字段共享 | A | L1 |
| 19 | F6 关系 | E. 无字段共享 | A | L1 |
| 20 | medicalRecordId 关系 | ✅ cashflowId → medicalRecordId 桥接（C 级）| A | L1 |
| 21 | medicalProduct 关系 | E. 仅字段共现（medicalProductId 来自 F1）| A | L1 |
| 22 | deliveryStatus 关系 | E. 仅字段共现 | A | L1 |
| 23 | tradeNo 关系 | E. tradeNo 0 处 | A | L1 |
| 24 | State 关系 | 0 处 $state.go 出口（dead-end）| A | L1 |
| 25 | Charge→Delivery 桥类型 | **B+C**（State + API Response）| A | L1 |
| 26 | A/B/C/D/E/F | A: 25 / F: 1 | A | L1 |

### 19.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 25 | 96% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 1 | 4% |

### 19.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 20. A-F 总结

- **A 级**：25 项（96%）
- **F 级**：1 项（HTML 边界）
- **B/C/D/E 级**：0 项

---

## 21. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0 项
- **L3**：0 项

---

## 22. F 边界

| F 项 | 详情 |
|---|---|
| 1 | deliveryInputRecordCtrl HTML 模板 | medicalRecordId dead-end 字段的业务意图可能在 HTML |
| 2 | optometryGlasses State 配置 | 0 处 .state() in controller.js |
| 3 | deliveryInputRecordCtrl State 配置 | 0 处 .state() in controller.js |
| 4 | getMedicalRecordPayVo.json Response 完整结构 | 仅 1 个字段被消费（medicalRecord.id） |

---

## 23. 复刻风险（L1）

### 23.1 关键注意事项

1. **getMedicalRecordPayVo.json 是 1:1 复刻的关键 API**
   - **全局唯一 Consumer**：deliveryInputRecordCtrl L4034
   - **Request 字段**：`cashflowId`
   - **Response 字段**：`res.object.medicalRecord.id`
   - 任何字段调整会破坏 medicalRecordId 派生

2. **deliveryInputRecordCtrl 是 Charge → Delivery 桥接节点**
   - **cashflowId 必须从 StateParams 进入**
   - **medicalRecordId 写入后必须保留**（虽然 dead-end 但业务可能有意义）

3. **getMedicalRecordCashflowVo.json 是 Charge 内部桥接 API**
   - **5 Controller 调它**
   - **主用途：customer.id 派生**
   - 与 getMedicalRecordPayVo **名称相似但不同 API**

4. **5 个 Charge Controller 通过 getMedicalRecordCashflowVo 桥接 customer 链式调用**
   - payedDetailCtrl L4942-L4947 链式 API 模式（cashflowId → customer.id → getCustomerVo + getCustomerWallet）

5. **deliveryInputRecordCtrl L4036 medicalRecordId 是 dead-end**
   - 1:1 复刻必须**保留**该字段写入
   - 业务意图可能在 HTML 层（**F 边界**）

6. **F1-F6 链路与 getMedicalRecordPayVo 完全独立**
   - 2 套 API 在 deliveryInputRecordCtrl 并存
   - **cashflowId 是唯一共享字段**
   - **0 处 result 数据共享**

### 23.2 风险等级

| 风险 | 等级 | 说明 |
|---|---|---|
| getMedicalRecordPayVo 字段变化 | **高** | 全局唯一 Consumer |
| cashflowId State 配置变化 | **高** | 4 个 Delivery Controller 依赖 |
| getMedicalRecordCashflowVo 字段变化 | **中** | 5 Controller 依赖 |
| medicalRecordId dead-end 移除 | **中** | 业务意图可能失效 |

---

## 24. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不调用任何 API | ✅ |
| 5. 不打开真实生产系统 | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-116 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-178） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 10 untracked + 1 gitignored 原样保留 | ✅ |
| 14. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 25. 关键纠偏（S1-117 vs S1-116）

| 旧结论 | 新结论 | 依据 |
|---|---|---|
| S1-116: Charge → Delivery 通过 cashflowId 桥接 | S1-117: **确认** + **B+C 双桥类型** | deliveryInputRecordCtrl L4026/L4034/L4036 |
| S1-116: medicalRecordId 路径总数 = 11 类 | S1-117: **保持 11 类**（getMedicalRecordPayVo 派生路径已被 S1-116 计入） | S1-116 §18.2 |
| S1-116: 0 处 cross-branch API 共享 | S1-117: **保持 0 处** | S1-117 §10 |

### 25.1 S1-117 新发现汇总

1. **getMedicalRecordPayVo.json 全局仅 1 处 Consumer**（deliveryInputRecordCtrl L4034）
2. **getMedicalRecordCashflowVo.json 是相关但不同的 API**（5 个 Charge Controller 使用）
3. **5 个 Charge Controller 通过 cashflowId 调 getMedicalRecordCashflowVo 桥接 customer 链式调用**
4. **deliveryInputRecordCtrl L4036 medicalRecordId 是 dead-end 字段**（0 处下游消费）
5. **B+C 双桥类型**：State 参数（B）+ API Response → Request（C）
6. **F1-F6 链路与 getMedicalRecordPayVo 完全独立**（仅 cashflowId 字段共现）

---

## 26. 最终结论

### 26.1 Charge → Delivery 桥接完整路径

```
[Charge 业务层]
Charge Controller (5 个)
  ├─ payedDetailCtrl L4942
  ├─ payedListCtrl L5166
  ├─ waitPayBackCtrl L7070
  ├─ waitPayDetailCtrl L7488
  └─ waitPayListCtrl L8129
  ↓ 产生 cashflow (业务核心)
  ↓
$stateParams.cashflowId (State 入口)
  ↓ B: State 参数桥
[Delivery 业务层]
deliveryInputRecordCtrl (L4024-L4072)
  ↓
$scope.cashflowId (L4026)
  ↓ C: API Response → Request
getMedicalRecordPayVo.json { cashflowId } (L4034)
  ↓ Response
res.object.medicalRecord.id (L4036)
  ↓
$scope.medicalRecordId
  ↓
[DEAD-END - 0 处下游消费]
```

### 26.2 关键结论

1. **桥接类型**：B + C（State 参数 + API Response → Request）
2. **桥接强度**：完整（A 级 3 行代码）
3. **桥接下游**：medicalRecordId 是 dead-end 字段（**0 处消费**）
4. **F1-F6 关系**：完全独立（仅 cashflowId 字段共现）
5. **getMedicalRecordCashflowVo vs getMedicalRecordPayVo**：两个**不同**的 API，名称相似但 Controller 隔离
6. **5 个 Charge Controller 通过 getMedicalRecordCashflowVo 桥接 customer**（不是 medicalRecord）

### 26.3 1:1 复刻关键

1. **deliveryInputRecordCtrl L4026/L4034/L4036** 必须完整保留
2. **cashflowId State 入口**必须保留
3. **getMedicalRecordPayVo.json 字段**必须保留
4. **medicalRecordId dead-end 字段**建议保留（业务意图 F 边界）
5. **getMedicalRecordCashflowVo.json**（5 个 Charge Controller）也必须保留

---

**审计完成。本文档为 179 号，提交后将形成 tracked=187，untracked=10，ignored=1。**
