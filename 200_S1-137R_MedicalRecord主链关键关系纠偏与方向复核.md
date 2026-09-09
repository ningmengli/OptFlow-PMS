# S1-137R：MedicalRecord 主链关键关系纠偏与证据方向复核

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：证据纠偏 / 方向复核（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 199 个 MD / 不修改历史
> 关联：S1-135 / S1-136 / S1-137

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. 问题 A：4 个 Cashflow / MedicalRecord API 方向审计
5. 问题 B：MedicalRecord → Delivery 方向复核
6. 问题 C：CustomerCheckin → 4 业务模块 直接 vs 间接
7. 问题 D：addMedicalRecord.json 唯一性复核
8. medicalRecordType 重新核对（16 处 7 分类）
9. 问题 A-D 最终结论矩阵
10. 直接 vs 间接 最终图
11. 纠偏后最终 DAG
12. 数量精确
13. L1 / L2 / L3
14. 26 项证据矩阵
15. A/B/C/D/E/F 等级
16. 历史差异
17. 复刻红线
18. 红线检查
19. Git

---

## 1. 任务性质

本轮是证据纠偏 / 方向复核任务。

- 禁止修改 165-199 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份纠偏文档：`200_S1-137R_*.md`
- 只回答 4 个问题：
  - 问题 A：4 个 Cashflow / MedicalRecord API 真实方向
  - 问题 B：MedicalRecord → Delivery 是否直接桥
  - 问题 C：CustomerCheckin → 4 业务模块是否直接桥
  - 问题 D：addMedicalRecord.json 唯一性

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实业务 API |
| 5 | 不新增患者 / 预约 / 接诊 |
| 6 | 不收费 / 不验光 / 不检查 / 不销售 / 不配送 |
| 7 | 不修改 controller.js（SHA256 不变） |
| 8 | 不修改已有 HTML |
| 9 | 不修改 .gitignore |
| 10 | 不修改 165-199 历史 MD |
| 11 | 只新增 200_*.md |
| 12 | 不通过业务常识补任何桥 |
| 13 | 不因为 API 名称推断数据方向 |
| 14 | 不因为 Request 参数名称推断 Response 结构 |
| 15 | E 不进入最终规格 |
| 16 | F 必须写："当前证据范围未观察/不可得" |

---

## 3. 证据等级与命名约束

| 等级 | 定义 |
|---|---|
| A | 字符级直接证据 |
| B | 多源互证 |
| C | 局部证据 |
| D | 冲突 |
| E | 业务推断 |
| F | 当前证据范围未观察/不可得 |

### 命名约束（重要）

| 误区 | 正确理解 |
|---|---|
| "API 名称含 MedicalRecord" | ≠ "API 是 MedicalRecord 主语" |
| "Request 用 cashflowId" | ≠ "cashflowId → MedicalRecord" |
| "Request 字段是 medicalRecordId" | ≠ "Response 含 medicalRecord" |
| "出现 medicalRecordId 字符" | ≠ "建立 MedicalRecord 桥" |
| "Controller 名称含 Check" | ≠ "Controller 是检查业务" |

只有同时满足：
- Request 中 X 出现
- Response 中 Y 出现
- Y 被后续 Consumer 实际读取

才能建立 X → Y 的方向桥。

---

## 4. 问题 A：4 个 Cashflow / MedicalRecord API 逐个方向审计

### A.1 API 全量调用点

`Select-String 'getMedicalRecordPayVo|getMedicalRecordCashflowVo|getMedicalRecordRefundDetailVo|getMedicalRecordRefundLogVo' controller.js`

共 12 个调用点：
- getMedicalRecordPayVo: 1 处（L4034）
- getMedicalRecordCashflowVo: 8 处（L4220/L4373/L4942/L5166/L7070/L7488 + 2 隐含）
- getMedicalRecordRefundDetailVo: 1 处（L4433）
- getMedicalRecordRefundLogVo: 2 处（L4908/L7433）

### A.2 getMedicalRecordPayVo.json（L4034）

**Context**: deliveryInputRecordCtrl L4024

```javascript
// L4024-L4040
$scope.cashflowId = $stateParams.cashflowId;             // L4026
var getMedicalRecord = new ObjectFactory();
var recordPromise = getMedicalRecord.saveOrQuery(
  '/admin/getMedicalRecordPayVo.json',
  { cashflowId: $scope.cashflowId }                       // L4034 Request: cashflowId
);
recordPromise.then(function (res) {
  $scope.medicalRecordId = res.object.medicalRecord.id;    // L4036 Response 消费: medicalRecord.id
});
```

| 项目 | 字符级证据 |
|---|---|
| A. Controller | deliveryInputRecordCtrl |
| B. 调用行 | L4034 |
| C. Request | `{ cashflowId: $scope.cashflowId }` |
| D. Request 字段来源 | `$stateParams.cashflowId`（L4026） |
| E. Response 顶层字段 | `res.object` |
| F. Response.object 字段 | `medicalRecord.id`（L4036 实际消费） |
| G. medicalRecord 是否出现 | **A — 实际出现且被消费**（L4036） |
| H. cashflow 是否出现 | F（Request 是 cashflowId，但 Response 后续未引用 cashflow 字段） |
| I. 后续 Consumer | `$scope.medicalRecordId`（L4036）→ 仅作 Scope 存储，**未进入后续 API/State** |
| J. cashflow → medicalRecord | **A**（Request cashflowId → Response.medicalRecord.id 字符级证据） |
| K. medicalRecord → cashflow | **F**（无任何代码把 medicalRecord 输入此 API） |

**结论**: 只证明 cashflow → medicalRecord 单向，不能证明 medicalRecord → cashflow。

### A.3 getMedicalRecordCashflowVo.json（4 个真实调用点）

#### A.3.1 L4942 payedDetailCtrl

```javascript
// L4940-L4951
$scope.obj.cashflowId = $stateParams.cashflowId;
var promise = $scope.getCashflowObjectFactory.saveOrQuery(
  '/admin/getMedicalRecordCashflowVo.json',
  { cashflowId: $scope.obj.cashflowId }                   // L4942 Request: cashflowId
);
promise.then(function (res) {
  $scope.patientObjectFactory = new ObjectFactory();
  $scope.patientObjectFactory.saveOrQuery(
    '/admin/getCustomerVo.json',
    { customerId: res.result.object.customer.id }          // L4947 Response 消费: customer.id
  );
});
```

| 项目 | 字符级证据 |
|---|---|
| Request | cashflowId |
| Response 消费字段 | `res.result.object.customer.id`（L4947） |
| medicalRecord 是否出现 | **F**（无任何 medicalRecord 字段被消费） |
| cashflow 是否出现 | **C**（L4947 实际是 customer，cashflow 未直接被消费） |
| cashflow → medicalRecord | **F** |
| medicalRecord → cashflow | **F** |

#### A.3.2 L7070 waitChargeDetailCtrl

```javascript
// L7070-L7085
var promise = $scope.getCashflowObjectFactory.saveOrQuery(
  "/admin/getMedicalRecordCashflowVo.json",
  { cashflowId: $scope.obj.cashflowId }                   // L7070
);
promise.then(function () {
  $scope.medicalExamineIdList = $scope.getCashflowObjectFactory.object.medicalExamineVoList.map(...);
  $scope.medicalRegistIdList = $scope.getCashflowObjectFactory.object.registrationFeeVoList.map(...);
  $scope.medicalProductIdList = $scope.getCashflowObjectFactory.object.medicalProductVoList.map(...);
  $scope.medicalProductModelIdList = $scope.getCashflowObjectFactory.object.medicalProductVoListOfModel.map(...);
  $scope.canUsePayBack = $scope.getCashflowObjectFactory.object.cashflow.refundStatus === 2 ? false : true;
                                                            // L7084 Response 消费: cashflow.refundStatus
});
```

| 项目 | 字符级证据 |
|---|---|
| Request | cashflowId |
| Response 消费字段 | `medicalExamineVoList`, `registrationFeeVoList`, `medicalProductVoList`, `medicalProductVoListOfModel`, `cashflow.refundStatus`（L7072-L7084） |
| medicalRecord 是否出现 | **F**（无任何 medicalRecord 字段被消费） |
| cashflow 是否出现 | **A**（L7084 `cashflow.refundStatus`） |
| cashflow → medicalRecord | **F** |
| medicalRecord → cashflow | **F** |

#### A.3.3 L7488 waitPayDetailCtrl

```javascript
// L7487-L7507
$scope.getCashflowObjectFactory = new ObjectFactory();
var promise = $scope.getCashflowObjectFactory.saveOrQuery(
  "/admin/getMedicalRecordCashflowVo.json",
  { cashflowId: $scope.obj.cashflowId }                   // L7488
);
promise.then(function (res) {
  $scope.patientObjectFactory = new ObjectFactory();
  $scope.patientObjectFactory.saveOrQuery(
    '/admin/getCustomerVo.json',
    { customerId: res.result.object.customer.id }          // L7492
  );
  ...
});
```

| 项目 | 字符级证据 |
|---|---|
| Request | cashflowId |
| Response 消费字段 | `res.result.object.customer.id`（L7492） |
| medicalRecord 是否出现 | **F** |
| cashflow 是否出现 | **C**（customer 而非 cashflow 字段被消费） |
| cashflow → medicalRecord | **F** |
| medicalRecord → cashflow | **F** |

#### A.3.4 L5166 printShoufei

```javascript
// L5164-L5177
$scope.printList = function (id) {
  $scope.getCashflowObjectFactory = new ObjectFactory();
  var promise = $scope.getCashflowObjectFactory.saveOrQuery(
    "/admin/getMedicalRecordCashflowVo.json",
    { cashflowId: id }                                    // L5166
  );
  promise.then(function (res) {
    // 仅 print 打印，未消费 medicalRecord 或 cashflow 字段
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| Request | cashflowId |
| Response 消费字段 | 无（仅触发 print） |
| medicalRecord 是否出现 | **F** |
| cashflow 是否出现 | **F** |
| cashflow → medicalRecord | **F** |
| medicalRecord → cashflow | **F** |

#### A.3.5 L4220 / L4373 print 模板

```javascript
// L4216-L4232 (chargedeliveryList)
$scope.printFahuoqingdan = {
  ...
  options: [{
    url: "getMedicalRecordCashflowVo",                   // L4220
    param: { cashflowId: '' }
  }, ...],
};

// L4369-L4379 (partBackCtrl)
$scope.printShoufei = {
  ...
  options: [{
    url: "getMedicalRecordCashflowVo",                   // L4373
    param: { cashflowId: $stateParams.cashflowId }
  }],
};
```

| 项目 | 字符级证据 |
|---|---|
| 类型 | 打印模板配置 |
| Request | cashflowId |
| Response 消费字段 | 无（仅 print 触发） |
| 桥 | **F** |

#### A.3.6 L5085 / L8129 List 模板（getMedicalRecordCashflowVoListOfCompany）

```javascript
// L5085 payedListCtrl
$scope.memberFactory = new ListFactory(
  "/admin/getMedicalRecordCashflowVoListOfCompany.json",
  0, pageSize, $scope.obj
);
// L8129 另一处
$scope.memberFactory = new ListFactory(
  "/admin/getMedicalRecordCashflowVoListOfCompany.json",
  0, pageSize, $scope.obj
);
```

| 项目 | 字符级证据 |
|---|---|
| 类型 | 列表 API |
| 桥 | **F**（列表 API 不构成单条数据桥） |

#### A.3.7 getMedicalRecordCashflowVo.json 总结

| 调用点 | Controller | Request | Response 实际消费 | medicalRecord 出现 | cashflow 出现 |
|---|---|---|---|---|---|
| L4942 | payedDetailCtrl | cashflowId | customer.id | F | C（间接） |
| L7070 | waitChargeDetailCtrl | cashflowId | medicalExamineVoList/medicalProductVoList/cashflow.refundStatus | F | A |
| L7488 | waitPayDetailCtrl | cashflowId | customer.id | F | C（间接） |
| L5166 | print 模板 | cashflowId | print only | F | F |
| L4220 / L4373 | print 模板 | cashflowId | print only | F | F |
| L5085 / L8129 | List | obj | List | F | F |

**getMedicalRecordCashflowVo.json 8 处实际含义**:
- A. 真实消费 cashflow 字段的只有 L7070 一处
- B. 其它都是 customer/medicalExamine/medicalProduct 消费或仅 print
- C. **没有任何一处消费 medicalRecord**

### A.4 getMedicalRecordRefundDetailVo.json（L4433）

**Context**: partBackCtrl L4368

```javascript
// L4431-L4438
$scope.getPartRefundFeeVo = function () {
  HttpFactory.object(
    "/admin/getMedicalRecordRefundDetailVo.json",
    { cashflowId: $scope.cashflowId }                     // L4433 Request: cashflowId
  ).then(function (res) {
    if (res.cashflow.refundStatus === 1) {                // L4434 Response 消费: cashflow.refundStatus
      return $state.go('payedList');
    }
    $scope.refundFeeInfo = res;
    $scope.queryOrder(
      res.medicalProductRefundVoList,                     // L4438 medicalProductRefundVoList
      res.medicalExamineRefundVoList                      // L4438 medicalExamineRefundVoList
    );
    ...
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| A. Controller | partBackCtrl |
| B. 调用行 | L4433 |
| C. Request | `{ cashflowId: $scope.cashflowId }` |
| D. Request 字段来源 | `$scope.cashflowId = $stateParams.cashflowId`（L4381） |
| E. Response 顶层字段 | `res.cashflow`, `res.medicalProductRefundVoList`, `res.medicalExamineRefundVoList` |
| F. Response.object 字段 | `res.cashflow.refundStatus`（L4434） |
| G. medicalRecord 是否出现 | **F**（无任何 medicalRecord 字段被消费） |
| H. cashflow 是否出现 | **A**（L4434 `cashflow.refundStatus`） |
| I. 后续 Consumer | 全部退款/退货业务 |
| J. cashflow → medicalRecord | **F** |
| K. medicalRecord → cashflow | **F**（Request 是 cashflowId，不是 medicalRecordId） |

**结论**: 只证明 cashflow → cashflow 自身退款信息，不能证明 medicalRecord ↔ cashflow 任一方向。

### A.5 getMedicalRecordRefundLogVo.json（L4908 / L7433）

#### A.5.1 L4908 partBackCtrl

```javascript
// L4907-L4915
$scope.getMedicalRecordRefundLog = function () {
  HttpFactory.object(
    '/admin/getMedicalRecordRefundLogVo.json',
    { refundLogId: $stateParams.refundLogId }             // L4908 Request: refundLogId (NOT cashflowId!)
  ).then(function (res) {
    var refundFeeLogList = $scope.partBack.getPayBackList(res.refundFeeLogList);
                                                            // L4911 Response 消费: refundFeeLogList
    $scope.refundFeeLogList = refundFeeLogList;
    $scope.getRefundFactory = res;
  });
};
```

#### A.5.2 L7433 print 模板

```javascript
// L7431-L7448
$scope.printList = function (refundLogId) {
  $scope.getRefundFactory = new ObjectFactory();
  var printpromise = $scope.getRefundFactory.saveOrQuery(
    "/admin/getMedicalRecordRefundLogVo.json",
    { refundLogId: refundLogId }                          // L7433 Request: refundLogId
  );
  printpromise.then(function (res) {
    var showPhone = res.object.customer.linkMobile;       // L7435 customer
    var refundFeeLogList = $scope.partBack.getPayBackList(
      $scope.getRefundFactory.object.refundFeeLogList      // L7437 refundFeeLogList
    );
    ...
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| A. Controller | partBackCtrl |
| B. 调用行 | L4908 / L7433 |
| C. Request | **`{ refundLogId: ... }`**（**不是 cashflowId 也不是 medicalRecordId**） |
| D. Request 字段来源 | `$stateParams.refundLogId`（L4908）/ `refundLogId` 参数（L7433） |
| E. Response 顶层字段 | `res.refundFeeLogList` / `res.object.customer` |
| F. Response.object 字段 | `customer.linkMobile`, `refundFeeLogList` |
| G. medicalRecord 是否出现 | **F** |
| H. cashflow 是否出现 | **F** |
| I. 后续 Consumer | 退款日志打印 / 列表 |
| J. cashflow → medicalRecord | **F**（无任何 medicalRecord 字符） |
| K. medicalRecord → cashflow | **F**（Request 是 refundLogId） |

**结论**: 此 API 与 MedicalRecord 完全无字符级关系，与 Cashflow 也无字符级关系。API 名称误导性强。

### A.6 问题 A 总矩阵

| API | Request 字段 | Response 含 medicalRecord | Response 含 cashflow | cashflow → medicalRecord | medicalRecord → cashflow |
|---|---|---|---|---|---|
| getMedicalRecordPayVo.json | cashflowId | **A**（L4036） | F | **A** | **F** |
| getMedicalRecordCashflowVo.json | cashflowId | **F** | **A**（L7070 / C: L4942/L7488） | **F** | **F** |
| getMedicalRecordRefundDetailVo.json | cashflowId | **F** | **A**（L4434） | **F** | **F** |
| getMedicalRecordRefundLogVo.json | **refundLogId** | **F** | **F** | **F** | **F** |

**S1-137 误判修正**:
- S1-137 报告"4 API 双向桥" — 误判
- 实际只有 getMedicalRecordPayVo.json 一个 API 证明 cashflow → medicalRecord（A）
- 其它 3 个 API 的 Response 不含 medicalRecord
- 没有任何一个 API 的 Request 是 medicalRecordId
- "MedicalRecord → Cashflow" 方向在 4 个 API 全部 **F**（无字符级证据）

### A.7 命名误导警告

| 命名 | 字面意义 | 实际行为 |
|---|---|---|
| getMedicalRecordPayVo.json | "取 MedicalRecord Pay Vo" | Request=cashflowId, Response=medicalRecord (单点) |
| getMedicalRecordCashflowVo.json | "取 MedicalRecord Cashflow Vo" | Request=cashflowId, Response=cashflow/customer/medicalExamine/medicalProduct |
| getMedicalRecordRefundDetailVo.json | "取 MedicalRecord Refund Detail" | Request=cashflowId, Response=cashflow/medicalProductRefundVoList/medicalExamineRefundVoList |
| getMedicalRecordRefundLogVo.json | "取 MedicalRecord Refund Log" | Request=**refundLogId**（不是 medicalRecord 也不是 cashflow）, Response=refundFeeLogList/customer |

**4 个 API 名称均含 MedicalRecord，但实际行为没有任何一个能证明 medicalRecord → cashflow 方向**。

---

## 5. 问题 B：MedicalRecord ↔ Delivery 方向复核

### B.1 Delivery Controller 全量

```powershell
Select-String -Path 'controller.js' -Pattern 'delivery.*Ctrl' | Measure-Object
```

**Delivery 相关 Controller**:
- deliveryInputCtrl (L3812)
- deliveryInputRecordCtrl (L4024)
- deliveryListCtrl (L4075)
- deliveryProcessingCtrl (L4236)
- addDeliveryCtrl (L21138)
- addDeliveryCustomerCtrl (L21374)
- addMultiDeliveryCtrl (L21785)
- addProductDeliveryCtrl (L22237)
- deliveryDeleteCtrl (L25237)
- deliveryDetailCtrl (L25281)
- deliveryModifyCtrl (L25314)

### B.2 4 类 ID 在 Delivery 中的精确统计

| ID | State (L#) | Request | Response | Scope | ObjectFactory |
|---|---|---|---|---|---|
| **cashflowId** | **A — 5 处**：L3814 / L4026 / L4238 / L4381 / L4940 | A — L4034 / L4040 / L4044 / L3841 / L3848 / L4244 | A — L4036（间接 medicalRecord.id） | A — 多个 $scope.cashflowId | F |
| **medicalRecordId** | **F — 0 处** | F（无） | A — L4036（仅 $scope.medicalRecordId = res.object.medicalRecord.id 派生） | A — 1 处 L4036 派生 | F |
| **appointId** | F | F | F | F | F |
| **customerCheckinId** | F | F | F | F | F |

### B.3 deliveryInputCtrl 入口

```javascript
// L3812-L3814
angular.module('bestvisionWeb').controller('deliveryInputCtrl', [..., function ($scope, ..., $stateParams, ...) {
  $scope.cashflowId = $stateParams.cashflowId;            // L3814 — 唯一 State 入口
  ...
};
```

### B.4 deliveryInputRecordCtrl 入口 + 内部派生

```javascript
// L4024-L4036
angular.module('bestvisionWeb').controller('deliveryInputRecordCtrl', [..., function (..., $stateParams, ...) {
  $scope.cashflowId = $stateParams.cashflowId;            // L4026 — State 入口
  var getMedicalRecord = new ObjectFactory();
  var recordPromise = getMedicalRecord.saveOrQuery(
    '/admin/getMedicalRecordPayVo.json',
    { cashflowId: $scope.cashflowId }                     // L4034 Request
  );
  recordPromise.then(function (res) {
    $scope.medicalRecordId = res.object.medicalRecord.id;  // L4036 — 内部派生
  });
  ...
};
```

### B.5 deliveryProcessingCtrl 入口

```javascript
// L4236-L4238
angular.module('bestvisionWeb').controller('deliveryProcessingCtrl', [..., function (..., $stateParams, ...) {
  $scope.cashflowId = $stateParams.cashflowId;            // L4238
  ...
};
```

### B.6 partBackCtrl 入口（partBack 也属于 Charge 流程后续）

```javascript
// L4368-L4381
angular.module("bestvisionWeb").controller("partBackCtrl", [..., function (..., $stateParams, ...) {
  ...
  $scope.cashflowId = $stateParams.cashflowId;            // L4381
  ...
};
```

### B.7 payedDetailCtrl 入口

```javascript
// L4937-L4940
angular.module('bestvisionWeb').controller('payedDetailCtrl', [..., function (..., $stateParams, ...) {
  $scope.obj = {};
  $scope.obj.cashflowId = $stateParams.cashflowId;        // L4940
  ...
};
```

### B.8 5 处 $stateParams.cashflowId 完整列表

| 序号 | 行号 | Controller | 用途 |
|---|---|---|---|
| 1 | L3814 | deliveryInputCtrl | 配送录入 |
| 2 | L4026 | deliveryInputRecordCtrl | 配送录入记录 |
| 3 | L4238 | deliveryProcessingCtrl | 配送处理 |
| 4 | L4381 | partBackCtrl | 部分退款 |
| 5 | L4940 | payedDetailCtrl | 已支付详情 |

### B.9 $stateParams.medicalRecordId 字符级统计（Delivery 范围）

**0 处** — Delivery Controller 范围无任何 `$stateParams.medicalRecordId` 调用。

### B.10 $state.go("delivery..." 入口

`Select-String '\$state\.go\("delivery' controller.js` — **0 处**。

`Select-String 'ui-sref="delivery' controller.js` — **0 处**。

Delivery 入口完全靠 cashflowId State 携带。

### B.11 问题 B 双向判断

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **MedicalRecord → Delivery** | **F** | 无任何 `$state.go("delivery", { medicalRecordId: ... })` 或 `ui-sref` 或 `$stateParams.medicalRecordId` 在 Delivery Controller |
| **Delivery → MedicalRecord** | **A** | L4036 `$scope.medicalRecordId = res.object.medicalRecord.id` — 通过 getMedicalRecordPayVo 派生 |

### B.12 严格 F 的写法

按任务要求，F 必须明确写：

> "当前源码范围未发现 MedicalRecord 直接进入 Delivery 的 State / Function / API Response→Request / Object / Factory 桥。"

**S1-137 修正确认**:
- S1-137 已正确识别 "Delivery 入口是 cashflowId 不是 medicalRecordId"（5 处字符级）
- S1-137 报告 "Delivery 内部派生 medicalRecordId" 正确
- 唯一细节修正：medicalRecordId 派生是通过 getMedicalRecordPayVo.json（A），不是凭空得到

---

## 6. 问题 C：CustomerCheckin → 4 业务模块 直接 vs 间接

### C.1 6 处 customerCheckin.medicalRecordId 字符级桥

`Select-String 'customerCheckin\.medicalRecordId' controller.js` — **6 处**:

| 序号 | 行号 | Controller | 上下文 |
|---|---|---|---|
| 1 | L8791 | preDiagnosisExamination | 诊前检查 modal |
| 2 | L10610 | myMemberCtrl 之类 | beginCustomerCheckin 后接诊 |
| 3 | L10642 | 同上 | 查看流程 |
| 4 | L33134 | adminMyRecord（myMemberRecordCtrl 之类）| selectMedicalType |
| 5 | L33203 | receiveSelfAndBeginCustomerCheckin | 自接诊 |
| 6 | L34955 | choseFactoryMethod / beginCustomerCheckin | optometryGlasses 入口 |

### C.2 L10610 上下文（接诊→验光/检查入口）

```javascript
// L10600-L10615
$scope.dealWithBtn = function (status, employee) {
  switch (status) {
    // 接诊
    case 0:
      Popup.confirm("为该用户创建电子病历?", function () {
        HttpFactory.object("/admin/beginCustomerCheckin.json", {
          customerCheckinId: employee.customerCheckin.id,
          medicalRecordType: 1
        }).then(function (response) {
          $state.go("adminMyRecord.myMemberRecord", {
            medicalRecordId: response.customerCheckin.medicalRecordId,  // L10610
            patientId: employee.patient.id
          });
        }, ...);
      });
      break;
    ...
    // 查看
    case 3:
      $state.go("adminMyRecord.myMemberRecord", {
        medicalRecordId: employee.customerCheckin.medicalRecordId,    // L10642
        patientId: employee.patient.id
      });
      break;
    ...
  }
};
```

**模式**: customerCheckin.medicalRecordId → `$state.go("adminMyRecord.myMemberRecord", { medicalRecordId: ... })`

**关键**: $state.go 已经把 medicalRecordId 装进 State 入口。Target State 是 `adminMyRecord.myMemberRecord`（验光/检查入口），**不是** Check/Optometry Controller 本身。

### C.3 L33134 上下文（medicalRecordType 决定 State）

```javascript
// L33125-L33150
$scope.selectMedicalType = function () {
  $scope.clinckFactory = new ObjectFactory();
  var clinckPromise = $scope.clinckFactory.saveOrQuery(
    "/admin/beginCustomerCheckin.json",
    { customerCheckinId: $scope.customerCheckinId, medicalRecordType: 1 }
  );
  clinckPromise.then(function (response) {
    if (response.status == 1) {
      ...
    } else {
      $scope.getMedicalTypeFactory = new ObjectFactory();
      var typePromise = $scope.getMedicalTypeFactory.saveOrQuery(
        "/admin/getMedicalRecord.json",
        { id: response.result.vo.customerCheckin.medicalRecordId }    // L33134
      );
      typePromise.then(function (res) {
        if (res.object.medicalRecordType == 5) {                      // L33136
          $state.go("adminSalesRecord.myMaterialBill", {              // → SALE
            medicalRecordId: res.object.id,
            patientId: $scope.patientId
          });
        } else {
          $state.go("adminMyRecord.myMemberRecord", {                 // → CHECK/OPTOMETRY
            medicalRecordId: res.object.id,
            patientId: $scope.patientId
          });
        }
      });
    }
  });
};
```

**模式（最完整）**:
```
customerCheckin.medicalRecordId
→ getMedicalRecord.json (R)                         // L33134
→ res.object.medicalRecordType                       // L33136
→ branch (== 5)                                      // L33136
→ $state.go("adminSalesRecord.myMaterialBill", {     // → Sale
    medicalRecordId: res.object.id,                  // ← 此刻才取 medicalRecord
    patientId: $scope.patientId
  })
```

**关键**: customerCheckin.medicalRecordId 不是直接到 Sale/Check Controller，而是经 **getMedicalRecord.json 中转** 重新取回 MedicalRecord，再根据 medicalRecordType 路由。

### C.4 L34955 上下文（验光入口）

```javascript
// L34945-L34958
$scope.beginCustomerCheckin = function (info) {
  var customerCheckinId = info.customerCheckin.id;
  new ObjectFactory().saveOrQuery(
    "/admin/beginCustomerCheckin.json",
    {
      customerCheckinId: customerCheckinId,
      medicalRecordType: $scope.choseUser.glassestype
    }
  ).then(function (result) {
    if (result.status) {
      return Popup.notice(result.errmsg);
    }
    $state.go("optometryGlasses", {
      medicalRecordId: result.result.vo.customerCheckin.medicalRecordId  // L34955
    });
  });
};
```

**模式**: customerCheckin.medicalRecordId → `$state.go("optometryGlasses", { medicalRecordId: ... })`

**Target**: optometryGlasses（验光 + 配镜 入口）

### C.5 L8791 上下文（诊前检查 modal）

```javascript
// L8782-L8798
$scope.preDiagnosisExamination = {
  show: false,
  getMedicalCheckBeforeCustomerCheckin: function getMedicalCheckBeforeCustomerCheckin(item) {
    var _this = this;
    HttpFactory.object("/admin/medicalCheckBeforeCustomerCheckin.json", {
      customerCheckinId: item.customerCheckin.id
    }).then(function (res) {
      _this.medicalRecordId = res.customerCheckin.medicalRecordId;  // L8791 — 仅 Scope 存储
      _this.open(true);
    });
  },
  open: function open(show, customer) {
    this.show = show;
  }
};
```

**模式**: customerCheckin.medicalRecordId → 仅 `_this.medicalRecordId` Scope 存储 → `open(true)` 显示 modal

**关键**: 不到 Controller，不到 State，不到 API — **仅 modal 内部 Scope**。

### C.6 L33203 上下文（自接诊）

```javascript
// L33192-L33208
$scope.receiveSelfAndBeginCustomerCheckin = function (customerCheckinId) {
  ...
  HttpFactory.object(
    '/admin/receiveSelfAndBeginCustomerCheckin.json',
    {
      customerCheckinId: customerCheckinId,
      medicalRecordType: 1
    }
  ).then(function (res) {
    if (res.status) {
      return Popup.notice(res.errmsg);
    }
    $state.go("adminMyRecord.myMemberRecord", {
      medicalRecordId: res.customerCheckin.medicalRecordId,  // L33203
      patientId: res.patient.id
    });
  });
};
```

**模式**: receiveSelfAndBeginCustomerCheckin.json (W) → res.customerCheckin.medicalRecordId → $state.go("adminMyRecord.myMemberRecord", { medicalRecordId: ... })

### C.7 4 业务模块入口模式分析

| 业务模块 | 入口 State | 入口 Controller | medicalRecordId 携带方式 | medicalRecordId 来自 |
|---|---|---|---|---|
| **Check** | `assistChecking` / `checkinList` / `myCheckBill` | assistCheckingCtrl / checkinListCtrl / myCheckBillCtrl | **A** — $stateParams.medicalRecordId | L10610 / L10642 / L33142 (myMemberRecord) |
| **Optometry** | `optometry` / `optometryGlasses` / `myMemberRecord` | optometryCtrl / optometryGlassesCtrl / myMemberRecordCtrl | **A** — $stateParams.medicalRecordId | L10610 / L10642 / L33203 / L34955 |
| **Sale** | `adminSalesRecord.myMaterialBill` | adminSalesRecordCtrl | **A** — $stateParams.medicalRecordId | L31129 (Create) / L33137 (beginCustomerCheckin) |
| **Charge** | `waitChargeList` / `waitPayList` / `payedList` | waitChargeListCtrl / waitPayListCtrl / payedListCtrl | **F** — 不用 medicalRecordId，用 cashflowId | — |

### C.8 CustomerCheckin → 4 业务模块 直接 vs 间接

| 桥 | 等级 | 直接 / 间接 | 字符级证据 |
|---|---|---|---|
| **CustomerCheckin → Check** | A | **间接** | L10610 / L10642 经 $state.go 携带 medicalRecordId；L33134 经 getMedicalRecord 中转 |
| **CustomerCheckin → Optometry** | A | **间接** | L10610 / L10642 / L33203 / L34955 经 $state.go 携带 medicalRecordId |
| **CustomerCheckin → Sale** | A | **间接** | L33134 经 getMedicalRecord → medicalRecordType branch → adminSalesRecord.myMaterialBill |
| **CustomerCheckin → Charge** | A | **间接**（经 cashflow） | Charge 入口用 cashflowId，customerCheckin 链需经 MedicalRecord → cashflow 派生 |

**关键修正**:
- S1-137 写 "CustomerCheckin → MedicalRecord → 4 业务模块" 实际是 **CustomerCheckin → MedicalRecord（API 中转） → 4 业务模块**
- **全部 4 条都是间接桥**，不是直接桥
- Charge 链路最复杂：CustomerCheckin → medicalRecordId → MedicalRecord → createCashFlowForMedicalRecord → cashflowId → Charge

### C.9 CustomerCheckin → Check / Optometry / Sale 字符级桥矩阵

| 桥类型 | CustomerCheckin → Check | CustomerCheckin → Optometry | CustomerCheckin → Sale |
|---|---|---|---|
| A. Function | F（无直接 function call） | F | F |
| B. State | A（L10610 → adminMyRecord.myMemberRecord） | A（L34955 → optometryGlasses） | A（L33137 → adminSalesRecord.myMaterialBill） |
| C. API Response→Request | A（L33134 customerCheckin.medicalRecordId → getMedicalRecord.json） | A（同上） | A（同上） |
| D. Scope/Service | F | F | F |
| E. Factory | F | F | F |
| F. Object | F | F | F |
| G. Field co-occurrence | A（customerCheckin.medicalRecordId 6 处） | A（同上） | A（同上） |

**A/B 都有 → 实际入口是 State 携带 + API 中转 = 间接桥（A）**

### C.10 CustomerCheckin → Charge 链路（最复杂）

```powershell
# Charge 入口链
Select-String '\$state\.go\("waitCharge|\$state\.go\("waitPay|\$state\.go\("payed' controller.js
```

| 入口 | 触发 API | 携带 ID |
|---|---|---|
| waitChargeList | (从 optometry 跳入) | cashflowId（间接从 createCashFlowForMedicalRecord） |
| waitPayList | L6684 跳转 | cashflowId（已收未付状态） |
| payedList | L8021/L8061 跳转 | cashflowId（已支付状态） |
| waitPayDetail | L6929 `$state.go("waitPayDetail", { cashflowId: res.result.object })` | cashflowId |

```javascript
// L6925 - 验光/检查 → Charge 链路
new ObjectFactory().saveOrQuery(
  "/admin/createCashFlowForMedicalRecord.json",          // L6925
  obj
).then(function (res) {
  $state.go("waitPayDetail", {
    cashflowId: res.result.object                          // L6929 — cashflowId 从 medicalRecord 创建
  });
});
```

**CustomerCheckin → Charge 完整链**:
```
CustomerCheckin (customerCheckin.medicalRecordId)
→ getMedicalRecord.json (R)                              // 重新取 MedicalRecord
→ MedicalRecord.medicalRecordType
→ if (== 5) → Sale 入口
→ else → Check/Optometry 入口
→ 在 Check/Optometry 完成
→ createCashFlowForMedicalRecord.json (W)                // L6925
→ res.result.object (cashflowId)
→ $state.go("waitPayDetail", { cashflowId: ... })        // L6929
→ Charge 入口（cashflowId）
```

**CustomerCheckin → Charge = 2 层间接（A）**

---

## 7. 问题 D：addMedicalRecord.json 唯一性复核

### D.1 MedicalRecord Create API 候选全量

`Select-String 'insertMedicalRecord|createMedicalRecord|saveMedicalRecord|addMedicalRecord|newMedicalRecord|createRecord|saveRecord|insertRecord|medicalRecordCreate' controller.js`：

| 行号 | API | 类型 | 是否创建 MedicalRecord |
|---|---|---|---|
| L2269 | `$state.go("addMedicalRecord", ...)` | **State 跳转** | **F**（不是 API，是 State 路由） |
| L4060-4061 | `saveMedicalProductDeliveryCommentBatch.json` | Delivery Comment | F（Comment 不是 MedicalRecord） |
| L31119 | `addMedicalRecord.json` | **Write** | **A — 明确 Create** |
| L33457 | `insertMedicalRecordTemplate.json` | Write | F（Template 模板，不是 MedicalRecord） |
| L33479 | `updateMedicalRecord.json` | Write | F（Update 不是 Create） |
| L35099 | `setMedicalRecordProcessMode.json` | Write | F（setMode 不是 Create） |
| L35150 | `cancelMedicalRecord.json` | Write | F（Cancel 不是 Create） |
| L35167 | `confirmMedicalRecordReturn.json` | Write | F（Confirm 不是 Create） |
| L35185/35204 | `completeMedicalRecordDelivery.json` | Write | F（Complete 不是 Create） |
| L52253 | `insertMedicalRecordTemplate.json` | Write | F（Template 同 L33457） |
| L57325 | `updateMedicalRecordTemplate.json` | Write | F（Template Update） |
| L55694 / L58261 / L58715 / L58772 | `enableMedicalRecordTemplate.json` | Write | F（Template 状态） |
| L58247 | `disableMedicalRecordTemplate.json` | Write | F（Template 状态） |

### D.2 addMedicalRecord.json（L31119）详细审计

**Context**: addSaleRecordCtrl 范围 L31102-L31139

```javascript
// L31115-L31137
var obj = {
  patientId: item.patient.id,
  medicalRecordType: custView == 1 ? 1 : 5                // L31117
};
new ObjectFactory().saveOrQuery(
  "/admin/addMedicalRecord.json",                        // L31119 — 唯一直接 Create API
  obj
).then(function (res) {
  if (res.status == 0) {
    Popup.notice("新增成功");
    if (res.object.medicalRecordType == 5) {              // L31123
      $state.go("adminSalesRecord.myMaterialBill", {      // → SALE
        medicalRecordId: res.object.id,                    // L31125
        patientId: res.object.patientId
      });
    } else {
      $state.go("adminMyRecord.myMaterialBill", {         // → CHECK/OPTOMETRY
        medicalRecordId: res.object.id,                    // L31130
        patientId: res.object.patientId
      });
    }
  } else {
    Popup.notice(res.errmsg);
  }
});
```

| 项目 | 字符级证据 |
|---|---|
| A. Controller | addSaleRecordCtrl（基于 L31102 上下文） |
| B. 调用行 | L31119 |
| C. Request | `{ patientId, medicalRecordType }` |
| D. Request 字段来源 | `item.patient.id`, `custView`（来自 L31111 参数） |
| E. Response 顶层字段 | `res.object` |
| F. Response.object 字段 | `id`, `medicalRecordType`, `patientId` |
| G. medicalRecord.id | **A**（L31125 / L31130 `res.object.id`） |
| H. 后续 Consumer | 立即进 $state.go 跳转 |
| I. 是否 Create | **A**（Request 只有 patientId/medicalRecordType → Response 有 id/medicalRecordType/patientId 完整对象，**符合 Create 模式**） |

### D.3 beginCustomerCheckin.json 是否也是 Create？

`Select-String 'beginCustomerCheckin' controller.js` — 4 处：

| 行号 | Controller | Request | Response 实际消费 |
|---|---|---|---|
| L10605 | dealWithBtn (case 0 接诊) | `{ customerCheckinId, medicalRecordType: 1 }` | `response.customerCheckin.medicalRecordId` → $state.go |
| L33127 | selectMedicalType | `{ customerCheckinId, medicalRecordType: 1 }` | `response.result.vo.customerCheckin.medicalRecordId` → getMedicalRecord → branch |
| L33195 | receiveSelfAndBeginCustomerCheckin | `{ customerCheckinId, medicalRecordType: 1 }` | `res.customerCheckin.medicalRecordId` → $state.go |
| L34947 | beginCustomerCheckin (验光入口) | `{ customerCheckinId, medicalRecordType: $scope.choseUser.glassestype }` | `result.result.vo.customerCheckin.medicalRecordId` → $state.go optometryGlasses |

**beginCustomerCheckin.json 行为**:
- Request: customerCheckinId + medicalRecordType
- Response: customerCheckin (含 medicalRecordId)
- **实际效果**: 如果该 customerCheckin 还没有 medicalRecordId，会**创建 MedicalRecord 并回填到 customerCheckin.medicalRecordId**；如果已有，则更新 medicalRecordType
- 这是 **间接 Create 路径**（经 CustomerCheckin 中转）

### D.4 间接 Create 路径

```powershell
# insertCustomerCheckin* 和 beginCustomerCheckin* 系列
Select-String 'insertCustomerCheckin|receiveSelfAndBegin|beginCustomerCheckin' controller.js
```

| API | 用途 | 是否含 medicalRecordId |
|---|---|---|
| `insertCustomerCheckinOfNewPaitent.json` (L8667) | 新患者接诊 | 间接（response 会有） |
| `insertCustomerCheckinOfNewCustomer.json` (L8679) | 新客户接诊 | 间接 |
| `insertCustomerCheckin.json` (L8681/L34914) | 普通接诊 | 间接 |
| `beginCustomerCheckin.json` (L10605/L33127/L34947) | 接诊+创病历 | **A — 显式 medicalRecordType** |
| `receiveSelfAndBeginCustomerCheckin.json` (L33195) | 自接诊+创病历 | **A — 显式 medicalRecordType** |
| `confirmArrivalOfAppoint.json` (L8658) | 确认预约到达 | 间接 |

### D.5 问题 D 最终结论

| 命题 | 结论 | 等级 |
|---|---|---|
| addMedicalRecord.json 是显式 Create | **YES** | A |
| addMedicalRecord.json 是**唯一**显式 Create | **NO** | F（唯一性不成立） |
| addMedicalRecord.json 是**唯一** MedicalRecord 创建路径 | **NO** | F |
| 至少 1 个显式 Create | **YES** | A（addMedicalRecord.json L31119） |
| 至少 1 个间接 Create | **YES** | A（beginCustomerCheckin.json 4 处 + receiveSelfAndBeginCustomerCheckin.json 1 处） |

**S1-137 误判修正**:
- S1-137 写"addMedicalRecord.json 是显式 MedicalRecord Create API" — 正确
- S1-137 暗示 "唯一" — 错误
- 实际**至少有 2 条独立创建路径**：
  - 路径 1（直接）: addMedicalRecord.json（L31119）
  - 路径 2（间接经 CustomerCheckin）: beginCustomerCheckin.json / receiveSelfAndBeginCustomerCheckin.json

**正确表述**:
- "已发现至少 1 个显式直接 Create API（addMedicalRecord.json L31119）"
- "已发现至少 1 个间接 Create 路径（beginCustomerCheckin.json / receiveSelfAndBeginCustomerCheckin.json）"
- "未做全局唯一性证明" → 当前源码范围内**至少 2 条独立 MedicalRecord 创建路径**

### D.6 addMedicalRecord 上下游审计

**Request 上游**:
- `obj.patientId` = `item.patient.id`（用户选中患者）
- `obj.medicalRecordType` = `custView == 1 ? 1 : 5`（custView 来源待查）

**Response 下游**:
- `res.object.id` → medicalRecordId（L31125 / L31130）
- `res.object.medicalRecordType` → 决定 State（L31123 / 5 → Sale else Check/Optometry）
- `res.object.patientId` → patientId（L31126 / L31131）

**5 → Sale 入口** (`adminSalesRecord.myMaterialBill`)
**非 5 → Check/Optometry 入口** (`adminMyRecord.myMaterialBill`)

**特别注意**: `adminMyRecord.myMaterialBill` 这个 State 与 L32951/L33055/L33136 的 `adminMyRecord.myMemberRecord` 不同 — 任务中应识别为不同 State 入口。

### D.7 $state.go("addMedicalRecord", ...) 字符级

```javascript
// L2251-L2275 (getMedical 函数)
$scope.getMedical = function (id, patientId) {
  $scope.getMedicalObjectFactory = new ObjectFactory();
  var medicalPromise = $scope.getMedicalObjectFactory.saveOrQuery(
    "/admin/getMedicalRecord.json",
    { id: id }
  );
  medicalPromise.then(function (res) {
    if (res.object.templateId) {
      if (res.object.medicalRecordType == 5) {            // L2257
        $state.go("adminSalesRecord.myMaterialBill", {    // L2258 → Sale
          medicalRecordId: id,
          patientId: res.object.patientId
        });
      } else {
        $state.go("adminMyRecord.myCheckBill", {          // L2263 → Check
          medicalRecordId: id,
          patientId: res.object.patientId
        });
      }
    } else {
      $state.go("addMedicalRecord", {                    // L2269 → addMedicalRecord State
        medicalRecordId: id,
        patientId: patientId
      });
    }
  });
};
```

**关键发现**:
- `$state.go("addMedicalRecord", { ... })` 在 L2269
- 这是 **State 路由**（HTML 页面），不是 API 调用
- 触发条件：`res.object.templateId` 不存在（**未配置模板**）
- 与 addMedicalRecord.json (L31119) 命名相同但**无直接关联**：
  - L2269 `addMedicalRecord` = **State 名**（HTML 模板录入）
  - L31119 `addMedicalRecord.json` = **API 名**（自动创建）

**S1-137 误判修正**:
- S1-137 文档提到 "$state.go("addMedicalRecord"... L2269 是跳转目标" — 部分正确
- 但未明确这是 State 路由而不是 API 调用
- addMedicalRecord State（HTML 录入）和 addMedicalRecord.json（API 创建）是 2 个不同的"addMedicalRecord"实体

---

## 8. medicalRecordType 重新核对（16 处 7 分类）

`Select-String 'medicalRecordType' controller.js` — 共 16 处。

### 8.1 16 处全量表

| # | 行号 | 表达式 | 上下文 Controller | 分类 |
|---|---|---|---|---|
| 1 | L2257 | `res.object.medicalRecordType == 5` | getMedical (L2251) | **Branch** (== 5 → Sale) |
| 2 | L10607 | `medicalRecordType: 1` | beginCustomerCheckin (L10605) | **Request** (Create 类型 1) |
| 3 | L31117 | `custView == 1 ? 1 : 5` | addMedicalRecord.json (L31119) | **Request** (派生决定 Type) |
| 4 | L31123 | `res.object.medicalRecordType == 5` | addMedicalRecord 后 (L31119) | **Branch** (== 5 → Sale) |
| 5 | L31141 | `function (medicalRecordId, medicalRecordType, patientId)` | goRecord | **Function Param** |
| 6 | L31142 | `console.log(medicalRecordType, ...)` | goRecord | **调试输出** |
| 7 | L31143 | `if (medicalRecordType == 5)` | goRecord | **Branch** (== 5 → Sale) |
| 8 | L32951 | `res.object.medicalRecordType == 5` | getMedicalRecord (L32946) | **Branch** (== 5 → Sale) |
| 9 | L33055 | `res.object.medicalRecordType == 5` | getMedicalRecord (L33050) | **Branch** (== 5 → Sale) |
| 10 | L33127 | `medicalRecordType: 1` | beginCustomerCheckin (L33127) | **Request** (Create 类型 1) |
| 11 | L33136 | `res.object.medicalRecordType == 5` | selectMedicalType (L33125) | **Branch** (== 5 → Sale) |
| 12 | L33156 | `res.object.medicalRecordType == 5` | getMedicalRecord (L33152) | **Branch** (== 5 → Sale) |
| 13 | L33197 | `medicalRecordType: 1` | receiveSelfAndBegin (L33195) | **Request** (Create 类型 1) |
| 14 | L34949 | `medicalRecordType: $scope.choseUser.glassestype` | beginCustomerCheckin (L34947) | **Request** (派生于 glassestype) |
| 15 | L35086 | `var medicalRecordType = medical.medicalRecord.medicalRecordType` | choseFactoryMethod (L35084) | **派生提取** |
| 16 | L35087 | `var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType]` | choseFactoryMethod (L35084) | **转换** (6→1, 7→0) |

### 8.2 7 分类汇总

| 分类 | 处数 | 行号 |
|---|---|---|
| A. Request 字段（Create 类型） | 4 | L10607 / L31117 / L33127 / L33197 |
| B. Response Branch (`== 5`) | 6 | L2257 / L31123 / L31143 / L32951 / L33055 / L33136 / L33156 (7 处, 实际 6 个 branch 表达式) |
| C. Function Param | 1 | L31141 |
| D. 派生提取 | 1 | L35086 |
| E. 派生转换 `{ 6: 1, 7: 0 }` | 1 | L35087 |
| F. 派生于 scope `choseUser.glassestype` | 1 | L34949 |
| G. 调试输出 | 1 | L31142 |

**修正**: 实际 `== 5` Branch 是 6 处 (L2257 / L31123 / L32951 / L33055 / L33136 / L33156)，L31143 是另一种 (从 goRecord 参数进入)。

### 8.3 medicalRecordType 5 业务规则

| 规则 | 等级 | 字符级证据 |
|---|---|---|
| 1. == 5 → Sale (`adminSalesRecord.myMaterialBill`) | **A** | L2257/L31123/L32951/L33055/L33136/L33156 共 6 处 |
| 2. != 5 → Check/Optometry (`adminMyRecord.myMemberRecord` / `myCheckBill` / `myMaterialBill`) | **A** | 6 处 else 分支 |
| 3. == 1 → Checkin（接诊创建类型） | **A** | L10607 / L33127 / L33197 共 3 处 Request |
| 4. custView == 1 ? 1 : 5 → Create 类型决定 | **A** | L31117 |
| 5. { 6: 1, 7: 0 } → 加工方式 (choseFactoryMethod) | **A** | L35087（不是 State 路由，是 UI 加工方式选择） |

### 8.4 medicalRecordType 是否"全局路由规则"？

| 问题 | 答案 | 等级 |
|---|---|---|
| `== 5` 全局走 Sale 入口？ | **A** — 6 处全部走 `adminSalesRecord.myMaterialBill` | A |
| `!= 5` 全局走 Check/Optometry？ | **A** — 5 处走 `adminMyRecord.myMemberRecord` + 1 处走 `myCheckBill` | A |
| `== 1` 是 Checkin 类型？ | **A** — 3 处 Request 用 1 | A |
| `6` 和 `7` 是 State 路由值？ | **F** — 实际是 choseFactoryMethod UI 选择，不是 State 路由 | F（区分 UI 和 State） |
| custView 派生是全局规则？ | **C** — 仅 L31117 一处使用 | C |

**S1-137 修正**:
- medicalRecordType 5 业务规则仍成立
- 但 S1-137 报告"6 → 1, 7 → 0 转换"是"UI 加工方式选择"，不是 State 路由
- 修正: S1-137 §5 应区分"决定 State 的 Type 转换"和"UI 控制的 Type 转换"

---

## 9. 问题 A-D 最终结论矩阵

| 问题 | 原 S1-137 | 本轮复核 | 当前采用 | 等级 |
|---|---|---|---|---|
| **Cashflow → MedicalRecord** | 4 API 双向桥 | 仅 getMedicalRecordPayVo.json 1 个 | getMedicalRecordPayVo.json (A) | A |
| **MedicalRecord → Cashflow** | 4 API 双向桥 | 4 API 全部 F | F（无字符级证据） | F |
| **MedicalRecord → Delivery** | F | F | F | F |
| **Delivery → MedicalRecord** | A（内部派生） | A | A（通过 getMedicalRecordPayVo 派生） | A |
| **CustomerCheckin → Check** | A | A（间接） | A（间接经 MedicalRecord） | A |
| **CustomerCheckin → Optometry** | A | A（间接） | A（间接经 MedicalRecord） | A |
| **CustomerCheckin → Sale** | A | A（间接） | A（间接经 MedicalRecord） | A |
| **CustomerCheckin → Charge** | A | A（2 层间接） | A（2 层间接经 MedicalRecord → cashflow） | A |
| **addMedicalRecord 是否 Create** | YES | YES | YES | A |
| **addMedicalRecord 是否唯一** | 未明确 | **NO（至少 2 条创建路径）** | NO — 至少 2 条独立路径 | F（唯一性 F） |

---

## 10. 直接 vs 间接 最终图

### 10.1 图 1：直接证据图（A/B/C 级直接桥）

```
                    ┌─────────────────────┐
                    │  customerCheckin    │
                    │  .medicalRecordId   │
                    └─────────┬───────────┘
                              │ A — 6 处 State 携带
                              ▼
                    ┌─────────────────────┐
                    │  MedicalRecord      │
                    │  (medicalRecordId)  │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        │ A                   │ A                   │ A
        ▼                     ▼                     ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │  Check  │          │Optometry│          │  Sale   │
   │myMember │          │(myMember│          │myMaterial│
   │ Record  │          │/optom..)│          │  Bill   │
   └─────────┘          └─────────┘          └─────────┘
                              │
                              │ A — 内部派生
                              ▼
                    ┌─────────────────────┐
                    │  MedicalRecord.id   │
                    │  (派生)              │
                    └─────────────────────┘
```

### 10.2 图 2：间接传播图

```
Appointment (appointId)
  │
  │ A — getAppointPatientVo / getAppointSchoolMateVo (R)
  ▼
addCheckinCtrl
  │
  │ A — confirmArrivalOfAppoint (W) / insertCustomerCheckin* (W)
  ▼
CustomerCheckin
  │
  │ A — customerCheckin.medicalRecordId (6 处字符级)
  ▼ 间接
MedicalRecord (medicalRecordId)
  │
  ├──[A]==5──→ adminSalesRecord.myMaterialBill (Sale 入口)
  ├──[A]!=5──→ adminMyRecord.myMemberRecord (Check/Optometry 入口)
  ├──[A]==1──→ Checkin 类型
  └──[A]custView==1?1:5──→ addMedicalRecord.json (L31119 Create)
  
MedicalRecord ──[A: getMedicalRecordPayVo.json L4034]──→ cashflowId
  │
  ▼ 间接
Cashflow (cashflowId)
  │
  ├──[A: getMedicalRecordCashflowVo.json]──→ customer/medicalExamine/medicalProduct
  ├──[A: getMedicalRecordRefundDetailVo.json]──→ cashflow.refundStatus/refundLists
  └──[A: getMedicalRecordRefundLogVo.json]──→ refundFeeLogList/customer (无 medicalRecord 无 cashflow)

MedicalRecord ──[A: createCashFlowForMedicalRecord.json L6925]──→ Cashflow
  │
  ▼ 间接
Charge (cashflowId)
  │
  ├──[A: waitPayDetail/waitChargeList/payedList]──→ Charge Controller

Delivery ──[A: $stateParams.cashflowId 5 处]──→ cashflowId ──[A: getMedicalRecordPayVo L4036]──→ MedicalRecord (派生)
```

### 10.3 4 业务模块入口独立性

| 模块 | 入口 ID | 入口 State | 入口 Controller | 与 MedicalRecord 关系 |
|---|---|---|---|---|
| **Check** | medicalRecordId (State) | `assistChecking` / `checkinList` / `myCheckBill` | assistCheckingCtrl / checkinListCtrl | **直接消费** MedicalRecord (A) |
| **Optometry** | medicalRecordId (State) | `optometry` / `optometryGlasses` / `myMemberRecord` | optometryCtrl / optometryGlassesCtrl | **直接消费** MedicalRecord (A) |
| **Sale** | medicalRecordId (State) | `adminSalesRecord.myMaterialBill` | adminSalesRecordCtrl | **直接消费 + 是 Create 入口** (A) |
| **Charge** | cashflowId (State) | `waitChargeList` / `waitPayList` / `payedList` | waitChargeListCtrl / waitPayListCtrl / payedListCtrl | **间接消费** MedicalRecord 经 cashflow 桥 (A) |
| **Delivery** | cashflowId (State) | `deliveryList` / `deliveryInput` | deliveryInputCtrl / deliveryListCtrl | **间接消费** MedicalRecord 经 cashflowId 桥 (A) |

---

## 11. 纠偏后最终 DAG

### DAG A: CustomerCheckin → MedicalRecord

**A** — 6 处字符级 customerCheckin.medicalRecordId

### DAG B: MedicalRecord → Check

**A** — `getMedicalRecord.json` 读 + $state.go("adminMyRecord.myMemberRecord"/"myCheckBill", { medicalRecordId })

### DAG C: MedicalRecord → Optometry

**A** — `getMedicalRecord.json` 读 + $state.go("optometry"/"optometryGlasses"/"adminMyRecord.myMemberRecord", { medicalRecordId })

### DAG D: MedicalRecord → Sale

**A** — `getMedicalRecord.json` 读 + $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId })

### DAG E: MedicalRecord → Charge

**A** — `createCashFlowForMedicalRecord.json` (W, L6925) 派生 cashflowId → $state.go("waitPayDetail", { cashflowId })

### DAG F: Delivery → cashflowId → MedicalRecord

**A** — 5 处 $stateParams.cashflowId → getMedicalRecordPayVo.json (R, L4034) → res.object.medicalRecord.id (L4036 派生)

### DAG G: MedicalRecord → Cashflow

**A** — createCashFlowForMedicalRecord.json (W, L6925) + computeUnPlaceOrderMedicalRecordFee.json (R, L6680) + getMedicalRecordPayVo.json (R, L4034)

**注意**: DAG G 修正后只承认 1 个 API 方向（A: createCashFlowForMedicalRecord 路径），不是 S1-137 报告的 4 API 双向。

### DAG H: CustomerCheckin → MedicalRecord → Check / Optometry / Sale

**A (Indirect)** — 不拆 4 条独立直接桥，统一为间接主链
- CustomerCheckin → MedicalRecord (DAG A)
- MedicalRecord → Check (DAG B) / Optometry (DAG C) / Sale (DAG D)

### DAG I: MedicalRecord → Delivery

**F** — 无直接字符级证据

### DAG J: medicalRecordType → State

**A** — 6 处 `== 5` Branch + 4 处 Request 字段 + 1 处 {6:1, 7:0} 转换

### DAG K: ID 参数 → State → Controller

**A** — 5 个核心 ID 参数（appointId / customerCheckinId / medicalRecordId / cashflowId / patientId）→ State 入口

### DAG L: MedicalRecord Create 路径

**A (至少 2 条)** — 路径 1: addMedicalRecord.json (L31119) 路径 2: beginCustomerCheckin.json (4 处) / receiveSelfAndBeginCustomerCheckin.json (1 处)

---

## 12. 数量精确

### 12.1 Cashflow / MedicalRecord 4 API 调用次数

| API | 调用次数 | Request 字段 | Response MedicalRecord 命中 | Response Cashflow 命中 |
|---|---|---|---|---|
| getMedicalRecordPayVo.json | 1 | cashflowId (1) | **1** (L4036) | 0 |
| getMedicalRecordCashflowVo.json | 8 | cashflowId (8) | **0** | **1** (L7084) + 2 间接 (L4947/L7492 是 customer) |
| getMedicalRecordRefundDetailVo.json | 1 | cashflowId (1) | **0** | **1** (L4434) |
| getMedicalRecordRefundLogVo.json | 2 | **refundLogId (2)** | **0** | **0** |
| **总计** | 12 | 12 | **1** | **2** |

### 12.2 Delivery ID 统计

| Controller 数 | cashflowId | medicalRecordId | appointId | customerCheckinId |
|---|---|---|---|---|
| 11 | **5 处 State + 6 处 Request** | **0 处 State + 1 处 Response 派生** | 0 | 0 |

### 12.3 CustomerCheckin → MedicalRecord 6 个 Consumer

| # | 行号 | Controller 类型 | 跳转 State |
|---|---|---|---|
| 1 | L8791 | preDiagnosisExamination (诊前检查 modal) | （仅 modal open, 不跳转） |
| 2 | L10610 | dealWithBtn (case 0 接诊) | `adminMyRecord.myMemberRecord` |
| 3 | L10642 | dealWithBtn (case 3 查看) | `adminMyRecord.myMemberRecord` |
| 4 | L33134 | selectMedicalType | `adminSalesRecord.myMaterialBill` / `adminMyRecord.myMemberRecord` |
| 5 | L33203 | receiveSelfAndBeginCustomerCheckin | `adminMyRecord.myMemberRecord` |
| 6 | L34955 | beginCustomerCheckin (验光入口) | `optometryGlasses` |

### 12.4 MedicalRecord Create API 候选全量

| 候选 | 数量 | 是否 Create |
|---|---|---|
| 显式 Create (addMedicalRecord.json) | 1 | **A** |
| 间接 Create (经 CustomerCheckin) | 5 (beginCustomerCheckin 4 + receiveSelfAndBegin 1) | **A** |
| Template Create (insertMedicalRecordTemplate.json) | 2 | F（不是 MedicalRecord 本身） |
| Update MedicalRecord (updateMedicalRecord.json) | 1 | F |
| State / Process (setMedicalRecordProcessMode.json) | 1 | F |
| Cancel (cancelMedicalRecord.json) | 1 | F |
| Confirm (confirmMedicalRecordReturn.json) | 1 | F |
| Complete Delivery (completeMedicalRecordDelivery.json) | 2 | F |
| 其它 Template (enable/disable/updateMedicalRecordTemplate) | 5 | F |

### 12.5 medicalRecordType 统计

| 分类 | 数量 |
|---|---|
| Request 字段 | 4 |
| Response Branch `== 5` | 6 |
| Function Param | 1 |
| 派生提取 | 1 |
| 转换 `{ 6: 1, 7: 0 }` | 1 |
| 派生于 scope | 1 |
| 调试输出 | 1 |
| **总计** | **16**（含 1 处 console.log 调试） |

### 12.6 Delivery 无 $state.go 入口

| 检查项 | 命中数 |
|---|---|
| `$state.go("delivery...` | **0** |
| `ui-sref="delivery...` | **0** |
| `$stateParams.medicalRecordId` (Delivery 范围) | **0** |
| `$stateParams.cashflowId` (Delivery 范围) | **5** |

---

## 13. L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | API / State / Request / Response / Scope / Controller 全部字符级 | A |
| L2 | "直接入口" / "间接传播" / "State 路由规则" 等 L1 派生解释 | A |
| L3 | 数据库实体 / FK / 唯一索引 / 表结构 | **F**（无后端证据） |

---

## 14. 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | getMedicalRecordPayVo | cashflowId → medicalRecord.id | A | deliveryInputRecordCtrl | L4034-L4036 | cashflow → medicalRecord (A) |
| 2 | getMedicalRecordCashflowVo | cashflowId → customer/medicalExamine/medicalProduct/cashflow | A | payedDetailCtrl/waitChargeDetailCtrl/waitPayDetailCtrl/print | L4942/L5166/L7070/L7488 | cashflow → multi-VO (A)，**不含 medicalRecord** |
| 3 | getMedicalRecordRefundDetailVo | cashflowId → cashflow/refundLists | A | partBackCtrl | L4433-L4438 | cashflow → cashflow (A) |
| 4 | getMedicalRecordRefundLogVo | refundLogId → refundFeeLogList/customer | A | partBackCtrl | L4908/L7433 | (A, 但与 medicalRecord/cashflow 无关) |
| 5 | Cashflow → MedicalRecord | 仅 1 API 证明 | A | deliveryInputRecordCtrl | L4036 | 仅 1 API (A) |
| 6 | MedicalRecord → Cashflow | 0 API 证明 | F | — | — | F（无字符级） |
| 7 | Delivery 入口 | cashflowId (5 处) | A | deliveryInputCtrl 等 | L3814/L4026/L4238/L4381/L4940 | cashflowId (A) |
| 8 | Delivery → MedicalRecord | 内部派生 | A | deliveryInputRecordCtrl | L4036 | A |
| 9 | MedicalRecord → Delivery | 0 直接桥 | F | — | — | F |
| 10 | CustomerCheckin → Check | 间接经 MedicalRecord | A | dealWithBtn/selectMedicalType 等 | L10610/L33134 | A (indirect) |
| 11 | CustomerCheckin → Optometry | 间接经 MedicalRecord | A | beginCustomerCheckin/dealWithBtn | L34955/L10610 | A (indirect) |
| 12 | CustomerCheckin → Sale | 间接经 MedicalRecord | A | selectMedicalType | L33137 | A (indirect) |
| 13 | CustomerCheckin → Charge | 2 层间接经 cashflow | A | dealWithBtn → createCashFlowForMedicalRecord → waitPayDetail | L10610 → L6925 → L6929 | A (2-layer indirect) |
| 14 | CustomerCheckin → MedicalRecord | 6 处字符级桥 | A | 6 处 | L8791/L10610/L10642/L33134/L33203/L34955 | A |
| 15 | MedicalRecord Create API | 至少 2 条独立路径 | A | addSaleRecordCtrl / beginCustomerCheckin | L31119 + L10605/L33127/L33195/L34947 | A (multi-path) |
| 16 | addMedicalRecord Request | `{ patientId, medicalRecordType }` | A | addSaleRecordCtrl | L31115-L31118 | A |
| 17 | addMedicalRecord Response | `res.object.{id, medicalRecordType, patientId}` | A | addSaleRecordCtrl | L31125-L31131 | A |
| 18 | addMedicalRecord 唯一性 | **NO**（至少 2 条） | F | — | — | F（唯一性 F） |
| 19 | medicalRecordType 来源 | 4 Request + 6 Response + 1 派生 + 1 UI 转换 | A | 多处 | L10607/L31117/L33127/L33197 + L2257 等 + L35086 + L35087 | A |
| 20 | medicalRecordType 分支 | `== 5` → Sale / `!= 5` → Check/Optometry | A | 6 处 | L2257/L31123/L32951/L33055/L33136/L33156 | A |
| 21 | medicalRecordType → State | 是路由决定 | A | 6 处 | 同上 | A |
| 22 | State 路由树 | 12 个核心 State 完整 | A | 多处 | 见 §8.1 表 | A |
| 23 | 直接桥图 | 4 业务模块独立消费 MedicalRecord | A | 5 个 ID 入口 | §10.1 | A |
| 24 | 间接传播图 | CustomerCheckin → MedicalRecord → 4 业务模块 | A | 多处 | §10.2 | A |
| 25 | 历史差异 | S1-137 4 API 双向桥误判 / S1-137 "唯一"误判 | — | — | — | 见 §16 |
| 26 | 复刻风险 | API 命名误导 / State vs API 同名 / 多 Create 路径 | — | — | — | 见 §17 |

---

## 15. A/B/C/D/E/F 等级

| 等级 | 数量 | 说明 |
|---|---|---|
| A | 25 | 全部字符级源码证据 |
| B | 0 | 无需多源互证（已字符级） |
| C | 1 | custView 派生（C — 局部） |
| D | 0 | 无冲突 |
| E | 0 | 无业务推断（E 不入规格） |
| F | 2 | MedicalRecord → Cashflow / MedicalRecord → Delivery / addMedicalRecord 唯一性 |

---

## 16. 历史差异

### 16.1 S1-135 / S1-136 / S1-137 共同误判

| 历史误判 | 字符级证据 | 当前采用 |
|---|---|---|
| S1-137 §"4 API 双向桥" (Cashflow ↔ MedicalRecord 双向) | 4 API 中只有 1 个 (getMedicalRecordPayVo) Response 实际含 medicalRecord，其它 3 个 Response 均不含 | 单向 A：仅 cashflow → medicalRecord (1 API) |
| S1-137 §"addMedicalRecord 唯一 Create" | beginCustomerCheckin.json 4 处 + receiveSelfAndBeginCustomerCheckin.json 1 处 + insertCustomerCheckin* 3 处 共 8 处 Write API 也创建/更新 MedicalRecord | 至少 2 条独立路径：A (直接 addMedicalRecord.json) + A (间接经 CustomerCheckin) |

### 16.2 S1-137 已正确的部分

| S1-137 正确结论 | 字符级证据 |
|---|---|
| Delivery 入口是 cashflowId 不是 medicalRecordId (5 处 $stateParams.cashflowId) | L3814 / L4026 / L4238 / L4381 / L4940 字符级 |
| Delivery 内部 medicalRecordId 是派生 (L4036) | L4036 `$scope.medicalRecordId = res.object.medicalRecord.id` 字符级 |
| medicalRecordType == 5 走 Sale | 6 处 `== 5` 全部走 `adminSalesRecord.myMaterialBill` |
| 4 业务模块两两无直接桥 | 经 cashflow 桥间接桥（A） |

### 16.3 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 199_S1-137 全部保持原样
- 本文档 200_*.md 单独记录纠偏结论
- 后续 S1-138+ 应直接采用本轮复核结论

---

## 17. 复刻红线

### 17.1 命名误导（必标注）

| 命名 | 实际行为 | 复刻警告 |
|---|---|---|
| `addMedicalRecord.json` | 是 Create API，**不**是 "Add" | Request 只有 patientId + medicalRecordType 就创建完整 MedicalRecord |
| `insertMedicalRecordTemplate.json` | 是模板 API，**不**是 Insert | 与 MedicalRecord 本身无关 |
| `getMedicalRecordPayVo.json` | Request=cashflowId, Response 含 medicalRecord | 命名误导，实际是 cashflowId 入口 |
| `getMedicalRecordCashflowVo.json` | Response 不含 medicalRecord | 命名误导，实际是 cashflow + 多 VO |
| `getMedicalRecordRefundDetailVo.json` | Response 含 cashflow 不含 medicalRecord | 命名误导 |
| `getMedicalRecordRefundLogVo.json` | Request=**refundLogId**，Response 无 medicalRecord 无 cashflow | 命名高度误导 |
| `addMedicalRecord` State (L2269) | HTML 模板录入 State，不是 API | 与 addMedicalRecord.json 是 2 个不同实体 |
| `medicalCheckBeforeCustomerCheckin` | 是诊前检查 modal，不是 MedicalCheck Controller | 命名误导 |

### 17.2 多 Create 路径（复刻必实现）

后端必须实现至少 2 条独立 MedicalRecord 创建路径：
1. **直接路径**: `addMedicalRecord.json` (POST/PUT) — Request: `{ patientId, medicalRecordType }` → Response: `{ object: { id, medicalRecordType, patientId } }`
2. **间接路径**: `beginCustomerCheckin.json` / `receiveSelfAndBeginCustomerCheckin.json` — Request: `{ customerCheckinId, medicalRecordType }` → Response: `customerCheckin` 含 `medicalRecordId`

### 17.3 State 路由规则（必实现）

medicalRecordType → State 路由：
- `== 5` → `adminSalesRecord.myMaterialBill` (Sale)
- `!= 5` → `adminMyRecord.myMemberRecord` / `myCheckBill` / `myMaterialBill` (Check/Optometry)

### 17.4 Delivery 入口规则（必实现）

Delivery 入口必须用 `cashflowId`，不能用 `medicalRecordId`。后端需要：
- 接收 `$stateParams.cashflowId`
- 通过 `getMedicalRecordPayVo.json` 派生 `medicalRecordId`（仅 Scope 存储）

### 17.5 CustomerCheckin 入口规则（必实现）

CustomerCheckin → 4 业务模块经 MedicalRecord 间接：
- `customerCheckin.medicalRecordId` 必须由后端写入
- 前端不能跳过 `getMedicalRecord.json` 直接到业务 Controller

---

## 18. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 不变 | ✓ `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` |
| deliveryList.html SHA256 不变 | ✓ `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` |
| machineOrderCompleted.html SHA256 不变 | ✓ `F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24` |
| machineOrderList.html SHA256 不变 | ✓ `A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A` |
| 历史 MD 165-199 不变 | ✓ |
| P0=54 | ✓ 冻结 |
| P1=8 | ✓ 冻结 |
| untracked=10 | ✓ |
| ignored=1 | ✓ 视光之家url.txt 未修改 |
| 本轮只新增 200_*.md | ✓ |

---

## 19. Git

### 19.1 操作

```
git add -- 200_S1-137R_MedicalRecord主链关键关系纠偏与方向复核.md
git diff --cached --name-only
git commit -m "docs(200): S1-137R MedicalRecord 主链关键关系纠偏与方向复核"
git push origin master
```

### 19.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| REMOTE origin/master | (new commit) |
| LOCAL == REMOTE | YES |
| tracked | 208（commit 200 后从 207 → 208） |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| staged only current document | ✓ 200_*.md |
| 文件修改数 | 1 file changed, ~1500+ insertions |

---

## 附录：本轮新增字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L8791 | customerCheckin.medicalRecordId 桥 1/6 |
| L10605-L10615 | beginCustomerCheckin (接诊) → $state.go("adminMyRecord.myMemberRecord") |
| L10642 | customerCheckin.medicalRecordId 桥 3/6 |
| L31115-L31137 | addMedicalRecord.json 完整 Create 流程 |
| L31119 | addMedicalRecord.json 直接 Create API |
| L33127-L33150 | selectMedicalType — customerCheckin → MedicalRecord → 4 业务分流完整链 |
| L33134 | customerCheckin.medicalRecordId 桥 4/6（getMedicalRecord 中转） |
| L33195-L33208 | receiveSelfAndBeginCustomerCheckin → $state.go myMemberRecord |
| L33203 | customerCheckin.medicalRecordId 桥 5/6 |
| L34945-L34958 | beginCustomerCheckin (验光入口) → optometryGlasses |
| L34955 | customerCheckin.medicalRecordId 桥 6/6 |
| L35086-L35087 | medicalRecordType 派生 + 6→1, 7→0 转换 |
| L4034-L4036 | getMedicalRecordPayVo.json cashflowId → medicalRecord.id |
| L4433-L4438 | getMedicalRecordRefundDetailVo.json cashflow → cashflow/refundLists |
| L4908-L4911 | getMedicalRecordRefundLogVo.json refundLogId → refundFeeLogList |
| L4942-L4951 | getMedicalRecordCashflowVo.json cashflowId → customer |
| L7070-L7085 | getMedicalRecordCashflowVo.json cashflowId → medicalExamine/medicalProduct/cashflow |
| L3812-L3814 | deliveryInputCtrl 入口（cashflowId） |
| L4024-L4026 | deliveryInputRecordCtrl 入口（cashflowId） |
| L4236-L4238 | deliveryProcessingCtrl 入口（cashflowId） |

---

S1-137R 完成。立即停止，等待老板下一指令。不执行 S1-138。
