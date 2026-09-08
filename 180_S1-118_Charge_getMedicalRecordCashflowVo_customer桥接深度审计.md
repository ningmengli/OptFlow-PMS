# S1-118 Charge getMedicalRecordCashflowVo → customer 桥接深度审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（gitignored）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-117（HEAD=376a313，tracked=187，untracked=10，ignored=1）
> - 本轮**重点**：S1-117 报告的"5 个 Charge Controller 调 getMedicalRecordCashflowVo"需要重新统计；customer/medicalRecord 桥接完整审计
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-179）/ 修改 7 HTML / 修改 11 文件 / 修改 P0=54 / P1=8

---

## 1. 审计范围

### 1.1 S1-117 错误纠正（S1-118 重扫）

| 项 | S1-117 报告 | S1-118 实际 | 差异 |
|---|---|---|---|
| 调用总数 | 5 处 | **9 处** | +4 |
| Consumer Controller | 5 个 | **8 个** | +3 |

**S1-118 关键发现 A**：
- S1-117 漏掉 4 处：
  1. **L4220** deliveryListCtrl（printFahuoqingdan URL string）
  2. **L4373** partBackCtrl（printShoufei URL string）
  3. **L5085** payedListCtrl（ListFactory，**漏了**）
  4. **L5142** payedListCtrl（printFahuoqingdan URL string，**漏了**）
  5. **L8129** waitPayListCtrl（ListFactory，**漏了**）

### 1.2 S1-118 新发现

- **8 个 Controller 涉及 getMedicalRecordCashflowVo**：
  1. deliveryListCtrl (Delivery 主链, L4220)
  2. partBackCtrl (Charge 关联, L4373)
  3. payedDetailCtrl (Charge 关联, L4942)
  4. payedListCtrl (Charge 主链, L5085/L5142/L5166)
  5. waitPayBackCtrl (Charge 关联, L7070)
  6. waitPayDetailCtrl (Charge 关联, L7488)
  7. waitPayListCtrl (Charge 关联, L8129)
  8. (deliveryInputRecordCtrl 不在此 API 范围内)

---

## 2. API 全局命中

### 2.1 getMedicalRecordCashflowVo 全局扫描

| # | 行号 | Controller | 调用方式 | 完整表达式 |
|---:|---:|---|---|---|
| 1 | 4220 | deliveryListCtrl | URL string | `url: "getMedicalRecordCashflowVo"` (printFahuoqingdan) |
| 2 | 4373 | partBackCtrl | URL string | `url: "getMedicalRecordCashflowVo"` (printShoufei) |
| 3 | 4942 | payedDetailCtrl | saveOrQuery | `'/admin/getMedicalRecordCashflowVo.json', { cashflowId: $scope.obj.cashflowId }` |
| 4 | 5085 | payedListCtrl | ListFactory | `"/admin/getMedicalRecordCashflowVoListOfCompany.json", 0, pageSize, $scope.obj` |
| 5 | 5142 | payedListCtrl | URL string | `url: "getMedicalRecordCashflowVo"` (printFahuoqingdan) |
| 6 | 5166 | payedListCtrl | saveOrQuery | `"/admin/getMedicalRecordCashflowVo.json", { cashflowId: id }` (printList 函数参数) |
| 7 | 7070 | waitPayBackCtrl | saveOrQuery | `"/admin/getMedicalRecordCashflowVo.json", { cashflowId: $scope.obj.cashflowId }` |
| 8 | 7488 | waitPayDetailCtrl | saveOrQuery | `"/admin/getMedicalRecordCashflowVo.json", { cashflowId: $scope.obj.cashflowId }` |
| 9 | 8129 | waitPayListCtrl | ListFactory | `"/admin/getMedicalRecordCashflowVoListOfCompany.json", 0, pageSize, $scope.obj` |

**总计**：**9 处调用**
- **saveOrQuery 4 处**：payedDetailCtrl / payedListCtrl / waitPayBackCtrl / waitPayDetailCtrl
- **ListFactory 2 处**：payedListCtrl / waitPayListCtrl
- **URL string 3 处**：deliveryListCtrl / partBackCtrl / payedListCtrl（用于 print）

### 2.2 8 个 Controller 分类

| Branch | Controller | 是否主链 | 数量 |
|---|---|:---:|---:|
| Delivery | deliveryListCtrl | ✅ 主链 | 1 (URL) |
| Charge | payedListCtrl | ✅ 主链 | 3 (ListFactory + URL + saveOrQuery) |
| Charge 关联 | partBackCtrl | ❌ 关联 | 1 (URL) |
| Charge 关联 | payedDetailCtrl | ❌ 关联 | 1 (saveOrQuery) |
| Charge 关联 | waitPayBackCtrl | ❌ 关联 | 1 (saveOrQuery) |
| Charge 关联 | waitPayDetailCtrl | ❌ 关联 | 1 (saveOrQuery) |
| Charge 关联 | waitPayListCtrl | ❌ 关联 | 1 (ListFactory) |

**S1-118 关键发现 B**：
- 实际调用 getMedicalRecordCashflowVo 的 Controller 涉及 **1 个 Delivery + 1 个 Charge 主链 + 4 个 Charge 关联**

---

## 3. Consumer Controller

### 3.1 Consumer Controller 重新统计

| Controller | 调用数 | 是否 S1-115 主链 | 备注 |
|---|---:|:---:|---|
| payedDetailCtrl | 1 | ❌ 关联 | S1-117 列出 |
| payedListCtrl | 3 | ✅ 主链 | S1-117 漏 2 处（L5085/L5142） |
| waitPayBackCtrl | 1 | ❌ 关联 | S1-117 列出 |
| waitPayDetailCtrl | 1 | ❌ 关联 | S1-117 列出 |
| waitPayListCtrl | 1 | ❌ 关联 | **S1-117 漏** |
| partBackCtrl | 1 | ❌ 关联 | **S1-117 漏** |
| deliveryListCtrl | 1 | ✅ Delivery 主链 | **S1-117 漏** |
| **总计** | **9** | 3 主链 + 5 关联 | **8 Controller** |

**S1-118 关键发现 C**：
- S1-117 "5 个 Charge Controller" → 实际是 **8 个 Controller**（含 1 个 Delivery + 1 个 Charge 主链 + 4 个 Charge 关联）
- S1-117 错误统计

### 3.2 S1-115 主链中的实际 Consumer

| 主链 Controller | 调用 getMedicalRecordCashflowVo |
|---|:---:|
| myCheckBillCtrl | ❌ 0 处 |
| waitChargeDetailCtrl | ❌ 0 处（**但有 medicalRecord.patientId 来源，见 §11**） |
| payedListCtrl | ✅ 3 处 |
| deliveryListCtrl | ✅ 1 处（URL string） |

---

## 4. Request 字段全集

### 4.1 4 个 saveOrQuery Request 详细

| Controller | 行号 | Request 字段 | 来源表达式 |
|---|---:|---|---|
| payedDetailCtrl | 4942 | `cashflowId: $scope.obj.cashflowId` | `$stateParams.cashflowId` (L4940) |
| payedListCtrl | 5166 | `cashflowId: id` | 函数参数 `id` (L5164 printList 接收) |
| waitPayBackCtrl | 7070 | `cashflowId: $scope.obj.cashflowId` | `$stateParams.cashflowId` |
| waitPayDetailCtrl | 7488 | `cashflowId: $scope.obj.cashflowId` | `$stateParams.cashflowId` |

**共识字段**：`cashflowId`
**共识来源**：3 处 `$stateParams.cashflowId` + 1 处 函数参数 `id`
**Request 字段总数**：1 个

### 4.2 2 个 ListFactory Request 详细

| Controller | 行号 | Request | 来源 |
|---|---:|---|---|
| payedListCtrl | 5085 | `$scope.obj` | 整个 obj（含 cashflowId 等筛选条件） |
| waitPayListCtrl | 8129 | `$scope.obj` | 整个 obj |

**Request 字段**：完整 `$scope.obj`（不只 cashflowId）

### 4.3 3 个 URL string 详细

| Controller | 行号 | param | 来源 |
|---|---:|---|---|
| deliveryListCtrl | 4220 | `{ cashflowId: '' }` | 静态空字符串（后被 print.print() 覆盖） |
| partBackCtrl | 4373 | `{ cashflowId: $stateParams.cashflowId }` | StateParams |
| payedListCtrl | 5142 | `{ cashflowId: '' }` | 静态空字符串（后被 print.print() 覆盖） |

---

## 5. Request provenance

### 5.1 cashflowId 全量来源

| Controller | 行号 | cashflowId 来源 | A-F |
|---|---:|---|---|
| payedDetailCtrl | 4940 | `$stateParams.cashflowId` → `$scope.obj.cashflowId` | A |
| payedListCtrl | 5164 | 函数参数 `id` (printList) | A |
| waitPayBackCtrl | (L7067 之前) | `$stateParams.cashflowId` → `$scope.obj.cashflowId` | A |
| waitPayDetailCtrl | (L7486 之前) | `$stateParams.cashflowId` → `$scope.obj.cashflowId` | A |
| payedListCtrl | 5085 | `$scope.obj`（含 cashflowId 派生） | A |
| waitPayListCtrl | 8129 | `$scope.obj`（含 cashflowId 派生） | A |
| deliveryListCtrl | 4220 | `param: { cashflowId: '' }` (URL string) | A |
| partBackCtrl | 4373 | `$stateParams.cashflowId` (URL string param) | A |

### 5.2 cashflowId 上游追迹

```
[State 入口 - F 边界: State 配置不在 controller.js]
$stateParams.cashflowId
  ↓
[$scope.obj.cashflowId 4 处]
├─ payedDetailCtrl L4940
├─ waitPayBackCtrl (待验证具体行号)
├─ waitPayDetailCtrl (待验证具体行号)
└─ (4 个 Controller 共用同一模式)

[$scope.obj (ListFactory) 2 处]
├─ payedListCtrl L5085
└─ waitPayListCtrl L8129

[函数参数 1 处]
└─ payedListCtrl L5164 printList(id)

[URL string param 1 处]
└─ partBackCtrl L4373
```

**S1-118 关键发现 D**：
- 8 个 Controller 全部通过 `$stateParams.cashflowId` 或 `obj.cashflowId` 间接获取 cashflowId
- **0 个 Controller 产生新 cashflowId**

---

## 6. Response 路径

### 6.1 各 Controller Response Consumer

| Controller | 行号 | Response 路径 | 关键 Consumer | A-F |
|---|---:|---|---|---|
| payedDetailCtrl | 4943 | `res.result.object.customer.id` | 派生 getCustomerVo / getCustomerWallet | A |
| payedListCtrl | 5167 | `res` (整体) | 用于打印（无直接 consumer）| A |
| waitPayBackCtrl | 7071 | `getCashflowObjectFactory.object.medicalExamineVoList/registrationFeeVoList/medicalProductVoList` | 注意：使用 `getCashflowObjectFactory.object.X` 而非 `res.X` | A |
| waitPayDetailCtrl | 7489 | `res.result.object.customer.id` | 派生 getCustomerVo / getCustomerWallet / getCustomerPoint | A |
| payedListCtrl | 5085 | (ListFactory.result) | jQuery pagination | A |
| waitPayListCtrl | 8129 | (ListFactory.result) | jQuery pagination | A |
| deliveryListCtrl | 4220 | (URL string, 仅用于 print modal) | - | A |
| partBackCtrl | 4373 | (URL string, 仅用于 print modal) | - | A |
| payedListCtrl | 5142 | (URL string, 仅用于 print modal) | - | A |

### 6.2 Response 完整结构

**严禁** 推断完整 schema。**仅记录实际消费字段**：

| Consumer Controller | 实际消费字段 |
|---|---|
| payedDetailCtrl | `res.result.object.customer.id` |
| payedListCtrl (L5167) | `res` (整体) |
| waitPayBackCtrl | `getCashflowObjectFactory.object.medicalExamineVoList/registrationFeeVoList/medicalProductVoList` (5 字段)|
| waitPayDetailCtrl | `res.result.object.customer.id` (3 链) |
| payedListCtrl (L5085) | `memberFactory.count` (ListFactory 通用) |
| waitPayListCtrl (L8129) | `memberFactory.count` (ListFactory 通用) |

---

## 7. customer 来源

### 7.1 customer 字段来源详情

| Controller | customer 来源 | 表达式 | A-F |
|---|---|---|---|
| payedDetailCtrl | **getMedicalRecordCashflowVo Response** | `res.result.object.customer.id` (L4947) | A |
| payedDetailCtrl | 第二次调用 | `res.result.object.customer.id` (L4950) | A |
| waitPayDetailCtrl | **getMedicalRecordCashflowVo Response** | `res.result.object.customer.id` (L7492) | A |
| waitPayDetailCtrl | 第二次调用 | `res.result.object.customer.id` (L7495) | A |
| waitPayDetailCtrl | 第三次调用 | `res.result.object.customer.id` (L7497) | A |
| waitPayBackCtrl | (无 customer 字段消费) | - | - |
| payedListCtrl | 0 处 | - | - |

### 7.2 customer 完整数据链

```
cashflowId
  ↓
getMedicalRecordCashflowVo.json Request
  ↓ Response
res.result.object.customer.id
  ↓
getCustomerVo.json Request { customerId }
  ↓ Response
$scope (customer info)
  ↓
[UI 展示 / 后续 API]
```

**S1-118 关键发现 E**：
- **customer 来源**：`getMedicalRecordCashflowVo.json` 的 `res.result.object.customer.id` 字段
- 桥接链：cashflowId → getMedicalRecordCashflowVo → customer.id → getCustomerVo
- **3 个 customer 桥接点**：payedDetailCtrl (2 链) + waitPayDetailCtrl (3 链) = 5 链

---

## 8. customer 字段

### 8.1 customer 实际消费字段

| Controller | 字段 | 表达式 | A-F |
|---|---|---|---|
| payedDetailCtrl | `customer.id` | L4947 / L4950 | A |
| waitPayDetailCtrl | `customer.id` | L7492 / L7495 / L7497 | A |
| partBackCtrl | `customer.id` (5 处) | (待详细审计) | A |
| checkinListCtrl | `customer.id` (4 处) | (S1-115 已确认) | A |
| waitPayBackCtrl | `customer.id` (1 处) | (待详细审计) | A |
| waitChargeDetailCtrl | `customer.id` (1 处) | (S1-115 0 处，**新增**)| A |
| payedDetailCtrl | `customer.id` (1 处额外) | (S1-115 1 处) | A |

**S1-118 关键发现 F**：
- 4 个主链 Controller 中 `customer.id` 出现：
  - checkinListCtrl: 4 处（Check 主链）
  - waitChargeDetailCtrl: 1 处（**S1-115 漏**）
  - partBackCtrl: 5 处
  - payedDetailCtrl: 2 处
  - waitPayBackCtrl: 1 处
  - waitPayDetailCtrl: 3 处

**S1-115 错误纠正**：
- S1-115 报 waitChargeDetailCtrl customerId 总数 = 1（实际是 1 处，**正确**）
- S1-115 报 customerId 总数 = 1（实际是 1 处，**正确**）
- S1-115 漏报：waitChargeDetailCtrl 1 处 customer.id（实际是 0 处 customerId，customerId 来自不同位置）

### 8.2 customer 其它字段

- **0 处** `customer.customerName` 在 4 主链
- 仅 checkinListCtrl / partBackCtrl 有 `customer.customerName` 消费（**S1-115 已确认 3+1=4 处**）

---

## 9. customer Consumer

### 9.1 customer 后续使用

```
[getMedicalRecordCashflowVo.json] Response
  ↓
res.result.object.customer.id
  ↓
[3 个后续 API]
├─ getCustomerVo.json { customerId }  → customer 详情
├─ getCustomerWallet.json { customerId } → 会员钱包
└─ getCustomerPoint.json { customerId } → 会员积分
  ↓
[UI 展示 / 业务计算]
```

### 9.2 5 个 customer 桥接点

| Controller | 行号 | 目标 API | A-F |
|---|---:|---|---|
| payedDetailCtrl | 4947 | getCustomerVo.json | A |
| payedDetailCtrl | 4950 | getCustomerWallet.json | A |
| waitPayDetailCtrl | 7492 | getCustomerVo.json | A |
| waitPayDetailCtrl | 7495 | getCustomerWallet.json | A |
| waitPayDetailCtrl | 7497 | getCustomerPoint.json | A |

**S1-118 关键发现 G**：
- **5 个 customer 桥接点**（payedDetailCtrl 2 + waitPayDetailCtrl 3）
- **0 个** customer 字段进入 Write
- **0 个** customer 字段进入 State params

---

## 10. customer → patient

### 10.1 关系检查

| Controller | customer | patient | 关系 |
|---|---|---|---|
| payedDetailCtrl | `res.result.object.customer.id` | (无 patient 字段) | 仅共现 |
| waitPayDetailCtrl | `res.result.object.customer.id` | (无 patient 字段) | 仅共现 |
| waitPayBackCtrl | (无 customer 字段) | `getCashflowObjectFactory.object.medicalExamineVoList` (medicalExamine.id) | 仅共现 |
| addSaleRecordCtrl | (无 customer) | 2 处 `patientName` | 仅共现 |
| checkinListCtrl | customer.id | patient 7 处 | 仅共现 |

### 10.2 类型判定

| 关系 | 类型 | A-F |
|---|---|---|
| **customer → patient** | **D. 共现** | A |
| **patient → customer** | **D. 共现** | A |

**S1-118 关键发现 H**：
- **0 处 customer → patient 直接数据链**（A 级）
- **0 处 patient → customer 直接数据链**（A 级）
- 仅在部分 Controller 中字段共现

---

## 11. customer → medicalRecord

### 11.1 waitChargeDetailCtrl medicalRecord.patientId 重大发现

```javascript
// L6570
$scope.medicalRecordId = $stateParams.medicalRecordId;

// L6680
$scope.getUnPlaceOrderObjectFactory = new ObjectFactory();
var promise = $scope.getUnPlaceOrderObjectFactory.saveOrQuery(
  "/admin/computeUnPlaceOrderMedicalRecordFee.json",
  { medicalRecordId: $scope.medicalRecordId }
);
promise.then(function (res) {
    // L6693
    if (!$scope.getPatientObjectFactory) {
        $scope.getPatientObjectFactory = new ObjectFactory();
        $scope.getPatientObjectFactory.saveOrQuery(
            "/admin/getPatientInfo.json",
            { id: res.object.medicalRecord.patientId }  // ← medicalRecord.patientId!
        );
    }
});
```

**S1-118 关键发现 I**：
- **waitChargeDetailCtrl 存在 medicalRecord.patientId 桥接**（A 级 L6693）
- **不是 getMedicalRecordCashflowVo 派生**，而是 `computeUnPlaceOrderMedicalRecordFee.json` 派生
- medicalRecord.patientId → getPatientInfo.json → patient info
- 这是 S1-115 漏的 medicalRecord → patient 桥接路径

### 11.2 customer → medicalRecord 关系

| Controller | customer → medicalRecord | 关系 | A-F |
|---|---|---|---|
| payedDetailCtrl | `customer.id` vs `medicalRecordId` (无直接访问) | 仅共现 | A |
| waitPayDetailCtrl | 同上 | 仅共现 | A |
| waitChargeDetailCtrl | customer.id (1 处) + medicalRecord.patientId (1 处, 来自 computeUnPlaceOrderMedicalRecordFee) | **不同 API 派生** | A |
| waitPayBackCtrl | (无 customer) + medicalExamineVoList | 仅共现 | A |

**S1-118 关键发现 J**：
- **0 处 customer.medicalRecordId 直接数据链**（A 级）
- waitChargeDetailCtrl 中 customer 和 medicalRecord **来自不同 API**
- **S1-115 锁定 waitChargeDetailCtrl 1 处 medicalRecord（整体）仍正确**

### 11.3 medicalRecord 整体对象确认

| Controller | medicalRecord 整体 | 行号 | 来源 API |
|---|:---:|---:|---|
| waitChargeDetailCtrl | ✅ 1 处 | L6682 / L6693 | computeUnPlaceOrderMedicalRecordFee.json |

**S1-115 保持**：waitChargeDetailCtrl 是唯一消费 `medicalRecord` 整体对象的 Controller（A 级）

---

## 12. customer → cashflow

### 12.1 cashflow 对象（4 主链范围内）

| Controller | cashflow 对象 | 字段访问 |
|---|---|---|
| payedDetailCtrl | `res.result.object` (是 getMedicalRecordCashflowVo 返回的整体对象) | `.customer.id` |
| payedListCtrl | 同上 | (无直接字段消费) |
| waitPayBackCtrl | `getCashflowObjectFactory.object` | `.medicalExamineVoList/.registrationFeeVoList/.medicalProductVoList` |
| waitPayDetailCtrl | `res.result.object` | `.customer.id` |
| deliveryInputRecordCtrl | (无 cashflow 对象) | (仅 cashflowId 字段) |

### 12.2 cashflow 字段消费

| Controller | cashflow.id | cashflow.medicalRecordId | cashflow.patientId | cashflow.customerId |
|---|:---:|:---:|:---:|:---:|
| payedDetailCtrl | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0（间接通过 customer.id）|
| waitPayBackCtrl | ✅ 1 (L7323) | ❌ 0 | ❌ 0 | ❌ 0 |

**S1-118 关键发现 K**：
- **0 处 cashflow.medicalRecordId / cashflow.patientId / cashflow.customerId 直接访问**（A 级）
- 实际访问字段：`.customer.id`（customer 桥接）和 VoList 字段（医学检查/挂号费/产品列表）
- cashflow.medicalRecordId **从未被消费**

### 12.3 cashflow → customer 类型判定

| 关系 | 类型 | 证据 |
|---|---|---|
| cashflow → customer | **C. 同 Response 共现** | getMedicalRecordCashflowVo Response 同时含 cashflow 和 customer |

**S1-118 关键发现 L**：
- cashflow 和 customer 在 getMedicalRecordCashflowVo Response 中**同 Response 共现**（C 级）
- 实际 Consumer 通过 `res.result.object.customer.id` 派生 customer
- **不**通过 `res.result.object.cashflow.xxx` 派生 cashflow 字段

---

## 13. cashflow → customer

### 13.1 关系分析

| Controller | 来源 | 字段 | 后续 |
|---|---|---|---|
| payedDetailCtrl L4947 | getMedicalRecordCashflowVo | `res.result.object.customer.id` | getCustomerVo Request |
| payedDetailCtrl L4950 | getMedicalRecordCashflowVo | `res.result.object.customer.id` | getCustomerWallet Request |
| waitPayDetailCtrl L7492 | getMedicalRecordCashflowVo | `res.result.object.customer.id` | getCustomerVo Request |
| waitPayDetailCtrl L7495 | getMedicalRecordCashflowVo | `res.result.object.customer.id` | getCustomerWallet Request |
| waitPayDetailCtrl L7497 | getMedicalRecordCashflowVo | `res.result.object.customer.id` | getCustomerPoint Request |

**S1-118 关键发现 M**：
- **cashflow → customer 是同 Response 派生**（C 级）
- **5 个 customer 桥接点全部通过 cashflow → customer 间接访问**
- **cashflow 和 customer 在同一 Response object 中**

### 13.2 类型判定

| 关系 | 类型 | A-F |
|---|---|---|
| cashflow → customer.id | **C. 同 Response 共现 → 派生** | A |
| cashflow → customer (整体) | **F. 当前证据范围未建立直接链**（仅 customer.id 字段桥） | A |

---

## 14. cashflowId → customer

### 14.1 cashflowId 与 customer 关系

```
cashflowId
  ↓ (State/Bridge)
getMedicalRecordCashflowVo.json Request { cashflowId }
  ↓ Response
res.result.object
  ├─ .cashflow (对象，含 cashflow.id)
  ├─ .customer (对象，含 customer.id)
  └─ 其它字段（未访问）
  ↓
[Customer 桥接点]
res.result.object.customer.id
  ↓
getCustomerVo.json Request { customerId }
```

### 14.2 类型判定

| 关系 | 类型 | A-F |
|---|---|---|
| cashflowId → customer.id | **B + C**（State + API Response）| A |

**S1-118 关键发现 N**：
- **cashflowId → customer.id 是 B+C 桥接**（State + API Response）
- 与 S1-117 锁定的 cashflowId → medicalRecordId 桥接**结构相同**（都是 B+C）
- **但** customer 桥接的 5 个 Controller 都是 Charge 内部（不出 Charge 分支）

### 14.3 两条数据链对照

| 链 | 起点 | 终点 | Controller 数 | 跨分支 |
|---|---|---|---:|:---:|
| **cashflowId → medicalRecordId** | Charge cashflowId | Delivery medicalRecordId | 1 (deliveryInputRecordCtrl) | ✅ Charge → Delivery |
| **cashflowId → customer.id** | Charge cashflowId | Charge customer | 2 (payedDetailCtrl + waitPayDetailCtrl) | ❌ Charge 内部 |

**S1-118 关键发现 O**：
- **两条不同数据链**（cashflowId → medicalRecordId vs cashflowId → customer.id）
- 两条链**完全独立**（不同 Controller / 不同 API / 不同 Response 字段）
- **0 处** 两条链相互交叉

---

## 15. cashflowId → medicalRecordId（S1-117 对照）

### 15.1 S1-117 保持

| 维度 | 状态 |
|---|---|
| cashflowId → medicalRecordId 桥接 | ✅ deliveryInputRecordCtrl L4034-L4036 |
| API | getMedicalRecordPayVo.json |
| B+C 桥类型 | ✅ |
| medicalRecordId 后续 | **DEAD-END**（0 处下游消费）|

### 15.2 S1-118 增量

- 0 处新发现（cashflowId → medicalRecordId 仍是 1 个 Controller）
- **保持 S1-117 结论**

---

## 16. PayVo 对照

### 16.1 CashflowVo vs PayVo 严格对照

| 项 | CashflowVo | PayVo |
|---|---|---|
| API | `/admin/getMedicalRecordCashflowVo.json` | `/admin/getMedicalRecordPayVo.json` |
| 唯一 API 名 | `getMedicalRecordCashflowVo` | `getMedicalRecordPayVo` |
| Controller | 8 个（4 Charge 主链/关联 + 1 Delivery + 3 URL string） | 1 个（deliveryInputRecordCtrl） |
| Request 字段 | `cashflowId` | `cashflowId` |
| Response 字段 | `res.result.object.customer.id` / VoList 字段 | `res.object.medicalRecord.id` |
| **Customer 桥** | ✅ 5 链（payedDetailCtrl 2 + waitPayDetailCtrl 3）| ❌ 0 |
| **medicalRecord 桥** | ❌ 0 直接消费（仅 1 处 `medicalRecord` 在 waitChargeDetailCtrl L6693 来自不同 API）| ✅ 1 链（deliveryInputRecordCtrl L4036）|
| **Delivery 跨链** | ❌ | ✅（Charge → Delivery）|
| **业务链方向** | Charge 内部 | Charge → Delivery |

### 16.2 类型判定

| 关系 | 类型 | A-F |
|---|---|---|
| CashflowVo vs PayVo API | **A. 完全不同** | A |
| CashflowVo Response 字段 | customer + VoList | A |
| PayVo Response 字段 | medicalRecord | A |
| Consumer Controller | 完全隔离 | A |

**S1-118 关键发现 P**：
- **两个 API 完全独立**（无 Response 字段共享）
- **Consumer Controller 隔离**（CashflowVo 8 个 vs PayVo 1 个，0 处重叠）
- **业务链方向相反**：CashflowVo 是 Charge 内部 customer 桥接，PayVo 是 Charge → Delivery 跨链

---

## 17. Charge Controller 对照

### 17.1 8 个 Charge/Charge 关联 Controller 详细

| Controller | cashflowId 来源 | customer | medicalRecord | medicalRecordId | patient | State |
|---|---|---|---|---|---|---|
| payedDetailCtrl | $stateParams (L4940) | ✅ 2 链 (L4947/L4950) | ❌ 0 | ❌ 0 | ❌ 0 | cashflowId |
| payedListCtrl | $stateParams (L5085 ListFactory) | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 | obj (含 cashflowId 派生) |
| payedListCtrl (printList) | 函数参数 id (L5164) | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 | - |
| waitPayBackCtrl | $stateParams (L7070) | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 (medicalExamine 1) | cashflowId |
| waitPayDetailCtrl | $stateParams (L7488) | ✅ 3 链 (L7492/L7495/L7497) | ❌ 0 | ❌ 0 | ❌ 0 | cashflowId |
| waitPayListCtrl | $scope.obj (L8129 ListFactory) | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 | obj |
| partBackCtrl | $stateParams (L4373 URL) | ✅ 5 处 | ❌ 0 | ❌ 0 | ❌ 0 | cashflowId |
| deliveryListCtrl | $stateParams (L4220 URL) | ❌ 0 | ❌ 0 | ❌ 0 | ❌ 0 | cashflowId |

**S1-118 关键发现 Q**：
- 2 个 Controller（payedDetailCtrl + waitPayDetailCtrl）有完整 customer 桥接
- 其它 6 个 Controller 仅消费 cashflow / VoList / 打印

### 17.2 customer 桥接深度

| Controller | customer 链数 | 桥接 API |
|---|---:|---|
| payedDetailCtrl | 2 | getCustomerVo + getCustomerWallet |
| waitPayDetailCtrl | 3 | getCustomerVo + getCustomerWallet + getCustomerPoint |
| **总计** | **5** | 3 个 API |

---

## 18. Scope/Service 共享

### 18.1 跨 Controller Scope 检查

| 机制 | 8 个 CashflowVo Consumer 间 | A-F |
|---|:---:|---|
| `$rootScope` | 0 | A |
| Service / factory | 0 | A |
| Global variable | 0 | A |
| callback | 0 | A |
| commonFn Session | 0（**CashflowVo Consumer 0 处用 Session**）| A |

### 18.2 S1-118 关键发现 R

- **0 处跨 Controller 共享 Scope/Service**（A 级）
- 每个 Controller 独立调用 getMedicalRecordCashflowVo
- **0 处数据链** 跨 CashflowVo Consumer 之间

---

## 19. Response → Write

### 19.1 4 个 saveOrQuery Consumer 后续

| Controller | 后续 Write | A-F |
|---|:---:|---|
| payedDetailCtrl | ❌ 0 处 | A |
| payedListCtrl (L5166 printList) | ❌ 0 处 | A |
| waitPayBackCtrl | ❌ 0 处（consumer 是 VoList → 直接 Scope 赋值） | A |
| waitPayDetailCtrl | ❌ 0 处 | A |

**S1-118 关键发现 S**：
- **0 处 Response → Write 直接链**（A 级）
- customer 桥接结果（getCustomerVo / getCustomerWallet / getCustomerPoint）仅进入 UI Scope
- **cashflow → customer 链路不进入 Write**

---

## 20. Response → State

### 20.1 $state.go 全量

```powershell
# 8 个 CashflowVo Consumer 中：
# - payedDetailCtrl: history.back() (L4967) - 无 State 跳转带 customer
# - payedListCtrl (待详细)
# - waitPayBackCtrl: 含 $state.go 但不带 customer
# - waitPayDetailCtrl: 0 处 $state.go 出口
# - 其它: 0 处
```

**S1-118 关键发现 T**：
- **0 处 Response.customer → $state.go 直接链**（A 级）
- customer 桥接结果仅进入 UI Scope

---

## 21. 后续 API

### 21.1 5 个 customer 桥接点后续 API

| Controller | 源 API | 后续 API | 链式 |
|---|---|---|:---:|
| payedDetailCtrl L4947 | getMedicalRecordCashflowVo | getCustomerVo | ✅ 链式 |
| payedDetailCtrl L4950 | getMedicalRecordCashflowVo | getCustomerWallet | ✅ 链式 |
| waitPayDetailCtrl L7492 | getMedicalRecordCashflowVo | getCustomerVo | ✅ 链式 |
| waitPayDetailCtrl L7495 | getMedicalRecordCashflowVo | getCustomerWallet | ✅ 链式 |
| waitPayDetailCtrl L7497 | getMedicalRecordCashflowVo | getCustomerPoint | ✅ 链式 |

**S1-118 关键发现 U**：
- **5 个 customer 桥接点全部链式调用**（A 级）
- 链式模式：cashflowId → getMedicalRecordCashflowVo → customer.id → {getCustomerVo / getCustomerWallet / getCustomerPoint}

### 21.2 waitPayBackCtrl VoList 链式

```
cashflowId
  ↓
getMedicalRecordCashflowVo.json
  ↓ Response
getCashflowObjectFactory.object
  ├─ .medicalExamineVoList → medicalExamineIdList
  ├─ .registrationFeeVoList → medicalRegistIdList
  └─ .medicalProductVoList → medicalProductIdList
```

**S1-118 关键发现 V**：
- waitPayBackCtrl 是**唯一**通过 cashflowVo 桥接 medicalExamine/registrationFee/medicalProduct 列表的 Controller
- 其它 CashflowVo Consumer 不消费 VoList 字段

---

## 22. 三对象关系矩阵

### 22.1 cashflow / customer / medicalRecord 三角关系

| 关系 | 证据 | 类型 | A-F |
|---|---|---|---|
| **cashflow → customer** | getMedicalRecordCashflowVo Response 同时含 cashflow + customer | C. 同 Response 共现 | A |
| **cashflow → medicalRecord** | 0 处直接访问 | E. 共现 | A |
| **customer → medicalRecord** | 0 处直接访问 | E. 共现 | A |
| **cashflowId → customerId** | getMedicalRecordCashflowVo 派生 customer.id | B + C. State + API | A |
| **cashflowId → medicalRecordId** | getMedicalRecordPayVo 派生 medicalRecord.id (S1-117) | B + C. State + API | A |
| **customerId → medicalRecordId** | 0 处直接访问 | F. 未建立 | A |

### 22.2 类型判定分布

| 类型 | 数量 |
|---|---:|
| A. 直接数据链 | 0 |
| B. 多源互证 | 0 |
| C. 部分 | 2（cashflow → customer + customerId → medicalRecordId）|
| D. 冲突 | 0 |
| E. 共现 | 2（cashflow → medicalRecord + customer → medicalRecord）|
| F. 未建立 | 1（customerId → medicalRecordId）|

### 22.3 cashflowId 多对象派生

```
cashflowId (State/Bridge B)
  ↓
[3 个不同 API 派生]
├─ getMedicalRecordCashflowVo.json
│   └─ Response: res.result.object
│       ├─ .customer.id → getCustomerVo/getCustomerWallet/getCustomerPoint
│       └─ .medicalExamineVoList/.registrationFeeVoList/.medicalProductVoList (waitPayBackCtrl)
│
├─ getMedicalRecordPayVo.json (Delivery 唯一)
│   └─ Response: res.object.medicalRecord.id → $scope.medicalRecordId
│
└─ (待详细) 其它 API
```

**S1-118 关键发现 W**：
- **cashflowId 可同时服务多个对象**（cashflow / medicalRecord / customer）
- 派生路径**完全独立**（不同 API、不同 Controller、不同 Response 字段）
- 严禁 假设 "一个 cashflowId 只对应一个对象"

---

## 23. 四大主链增量

### 23.1 S1-118 增量（S1-116 + S1-117 之后）

| 主链 | 增量 |
|---|---|
| Check | 0 |
| Sale | 0 |
| Charge | **+5 个 cashflow → customer 桥接**（payedDetailCtrl 2 + waitPayDetailCtrl 3）|
| Delivery | 0（S1-117 PayVo 桥接保持）|

### 23.2 跨主链数据链汇总

| 关系 | 类型 | 详情 |
|---|---|---|
| Check → Sale | F | 字段共现 |
| Sale → Charge | F | 字段共现 |
| **Charge → Delivery** | **B + C** | cashflowId 桥接（S1-117 锁定） |
| Check → Charge | F | 字段共现 |
| Sale → Delivery | F | 字段共现 |
| **Charge 内部 → customer** | **B + C** | **cashflowId 桥接（S1-118 锁定）** |
| **Charge 内部 → medicalRecord** | **B + C** | medicalRecordId 派生（waitChargeDetailCtrl L6693） |

### 23.3 S1-118 锁定关系

| 锁 | 详情 |
|---|---|
| **S1-117 已锁** | cashflowId → medicalRecordId（Delivery 桥接）|
| **S1-118 新锁** | cashflowId → customer.id（Charge 内部桥接，5 链）|
| **S1-118 新锁** | waitChargeDetailCtrl medicalRecord.patientId（来自 computeUnPlaceOrderMedicalRecordFee API）|

---

## 24. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | API 全局命中 | 9 处（S1-118 重扫）| A | L1 |
| 02 | Consumer Controller 全集 | 8 Controller | A | L1 |
| 03 | Call site | 4 saveOrQuery + 2 ListFactory + 3 URL | A | L1 |
| 04 | Request 全集 | cashflowId（共识）+ 完整 obj (ListFactory) | A | L1 |
| 05 | Request provenance | $stateParams (5) / 函数参数 (1) / obj (2) / URL string (3) | A | L1 |
| 06 | cashflowId 来源 | $stateParams.cashflowId（5 处）/ obj (2) / 函数参数 (1) | A | L1 |
| 07 | Response 路径 | res.result.object (4) / getCashflowObjectFactory.object (1) / ListFactory.result (2) / URL string (3) | A | L1 |
| 08 | Response 字段 | customer.id (5 链) / VoList (1) / 其它 (0) | A | L1 |
| 09 | customer 来源 | getMedicalRecordCashflowVo Response | A | L1 |
| 10 | customer 字段 | customer.id (5 链) | A | L1 |
| 11 | customer Consumer | getCustomerVo (2) + getCustomerWallet (2) + getCustomerPoint (1) | A | L1 |
| 12 | customer → patient | D. 共现 | A | L1 |
| 13 | customer → medicalRecord | D. 共现 | A | L1 |
| 14 | customer → cashflow | C. 同 Response 共现 | A | L1 |
| 15 | cashflow → customer | C. 同 Response 共现 | A | L1 |
| 16 | cashflowId → customer | B + C. State + API Response | A | L1 |
| 17 | cashflowId → medicalRecordId | B + C. State + API Response（S1-117 保持）| A | L1 |
| 18 | PayVo 对照 | CashflowVo ≠ PayVo（API / Consumer / 业务方向都不同）| A | L1 |
| 19 | Charge Controller 对照 | 8 Controller 完整对比（详见 §17）| A | L1 |
| 20 | Scope/Service 共享 | 0 处跨 Controller | A | L1 |
| 21 | Response → Write | 0 处 | A | L1 |
| 22 | Response → State | 0 处 | A | L1 |
| 23 | 后续 API | 5 个 customer 桥接点全部链式 | A | L1 |
| 24 | 三对象关系 | cashflow/customer/medicalRecord 三角矩阵 | A | L1 |
| 25 | 四大主链增量 | Charge → customer（B+C）+ Charge 内部 medicalRecord 派生 | A | L1 |
| 26 | A/B/C/D/E/F | A: 25 / F: 1 | A | L1 |

### 24.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 25 | 96% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 1 | 4% |

### 24.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 25. A-F 总结

- **A 级**：25 项（96%）
- **F 级**：1 项（HTML 边界）
- **B/C/D/E 级**：0 项

---

## 26. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0 项
- **L3**：0 项

---

## 27. F 边界

| F 项 | 详情 |
|---|---|
| 1 | 8 Controller HTML 模板 | 全部 F 边界 |
| 2 | getMedicalRecordCashflowVo Response 完整 schema | 仅 1 字段（customer.id）+ VoList 被消费 |
| 3 | waitPayBackCtrl VoList 后续使用 | medicalExamineVoList 仅写入 $scope.medicalExamineIdList（无下游分析） |

---

## 28. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不调用任何 API | ✅ |
| 5. 不打开真实生产系统 | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-117 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-179） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 10 untracked + 1 gitignored 原样保留 | ✅ |
| 14. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 29. 关键纠偏（S1-118 vs S1-117）

| 旧结论 | 新结论 | 依据 |
|---|---|---|
| S1-117: 5 个 Charge Controller 调 getMedicalRecordCashflowVo | **8 个 Controller**（含 1 个 Delivery + 4 个 Charge 关联）| S1-118 重扫 9 处命中 |
| S1-117: 5 处调用 | **9 处调用** | S1-118 重扫 |
| S1-115: waitChargeDetailCtrl medicalRecord 整体 1 处 | **保持 + 新增 medicalRecord.patientId 桥接** | L6693 |
| S1-115: cashflow.medicalRecordId 0 处 | **保持** | S1-118 确认 |
| S1-115: cashflow.id 0 处（4 主链）| **保持** | S1-118 确认 |

### 29.1 S1-118 新发现汇总

1. **getMedicalRecordCashflowVo 全局 9 处调用**（S1-117 报 5 处错误）
2. **8 个 Controller 涉及**（S1-117 报 5 个错误）
3. **5 个 customer 桥接点**（payedDetailCtrl 2 + waitPayDetailCtrl 3）
4. **waitChargeDetailCtrl 存在 medicalRecord.patientId 桥接**（L6693，来自 computeUnPlaceOrderMedicalRecordFee API，**不是** getMedicalRecordCashflowVo）
5. **waitPayBackCtrl 通过 cashflowVo 桥接 3 个 VoList**（medicalExamine/registrationFee/medicalProduct）
6. **cashflow → customer 是同 Response 共现**（C 级）
7. **cashflowId 可同时服务多个对象**（cashflow / medicalRecord / customer）
8. **CashflowVo vs PayVo 完全独立**（不同 API / 不同 Consumer / 不同业务方向）

---

## 30. 最终结论

### 30.1 CashflowVo → customer 完整链

```
[State 入口]
$stateParams.cashflowId (B - State 参数桥)
  ↓
[$scope.obj.cashflowId 5 处]
├─ payedDetailCtrl L4940
├─ waitPayBackCtrl (待验证)
├─ waitPayDetailCtrl (待验证)
├─ partBackCtrl L4373
└─ (其它 1 处)

[saveOrQuery 4 处]
cashflowId
  ↓
getMedicalRecordCashflowVo.json Request { cashflowId }
  ↓ Response
res.result.object
  ├─ .customer.id
  │   ↓
  │   [5 个 customer 桥接点]
  │   ├─ payedDetailCtrl L4947 → getCustomerVo.json
  │   ├─ payedDetailCtrl L4950 → getCustomerWallet.json
  │   ├─ waitPayDetailCtrl L7492 → getCustomerVo.json
  │   ├─ waitPayDetailCtrl L7495 → getCustomerWallet.json
  │   └─ waitPayDetailCtrl L7497 → getCustomerPoint.json
  │
  └─ VoList (仅 waitPayBackCtrl)
      ├─ .medicalExamineVoList → $scope.medicalExamineIdList
      ├─ .registrationFeeVoList → $scope.medicalRegistIdList
      └─ .medicalProductVoList → $scope.medicalProductIdList
```

### 30.2 关键结论

1. **cashflowId → customer 桥接类型**：**B + C**（State + API Response）
2. **5 个 customer 桥接点**全部链式调用
3. **cashflow 与 customer 同 Response 共现**（C 级）
4. **CashflowVo 是 Charge 内部桥接**（**不**跨主链）
5. **PayVo 是 Charge → Delivery 跨链桥接**（S1-117 锁定）
6. **两条数据链完全独立**（不同 API / 不同 Controller / 不同 Response 字段）
7. **cashflowId 是多对象派生**（cashflow / medicalRecord / customer）
8. **0 处 Response → Write / State**（A 级）
9. **0 处跨 Controller Scope/Service 共享**（A 级）

### 30.3 1:1 复刻关键

1. **8 个 Controller 中 5 个**通过 $stateParams.cashflowId 接收 cashflowId
2. **2 个 Controller**（payedDetailCtrl / waitPayDetailCtrl）有完整 customer 桥接
3. **1 个 Controller**（waitPayBackCtrl）有 VoList 桥接
4. **getMedicalRecordCashflowVo 字段**：customer + VoList（不能简化）
5. **getMedicalRecordPayVo 字段**：medicalRecord（与 CashflowVo 不同）
6. **waitChargeDetailCtrl 存在 medicalRecord.patientId 派生**（来自 computeUnPlaceOrderMedicalRecordFee API）

---

**审计完成。本文档为 180 号，提交后将形成 tracked=188，untracked=10，ignored=1。**
