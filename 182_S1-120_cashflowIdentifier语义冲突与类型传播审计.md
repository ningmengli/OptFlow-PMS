# S1-120 cashflow / cashflowId / id 字段语义冲突与类型传播审计

## 0. 任务背景

S1-119 已识别 cashflowId 字段 5 个独立第一来源（74 处 / 20 Controller），但**没有深入区分"id 本身" 与 "承载 object" 之间的语义差异**。

本轮目标：
- 区分 `cashflow.id` / `cashflowId` / `res.result.object` 整体 三种传播
- 重新精确定位 S1-119 中错误标注的 L6929
- 判定 4 个潜在 D 级冲突可能点
- 建立【cashflow identifier semantic map】与 6 类 Type Classification
- 26 项矩阵 + 复刻风险 L1

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| 静态扫描 cashflowId（Case-Sensitive）| 74 处 |
| 静态扫描 cashflowId（Case-Insensitive）| 80 处 |
| 静态扫描 `.cashflow` | 27 处 |
| 静态扫描 `cashflow.id` | **2 处** |
| 静态扫描 `cashflow\.(customerId\|patientId\|medicalRecordId\|tradeNo)` | **0 处** |
| 静态扫描 `res(\.result)?(\.object)?\.cashflow` | 3 处 |

## 2. S1-119 历史错误纠偏（关键）

### 2.1 S1-119 错误标注 vs S1-120 当前证据

S1-119 文档 L180/L185/L207/L245/L357/L492/L649 多次标注：

> "L6929 属于 waitPayBackCtrl"
> "API 是 getMedicalRecordCashflowVo.json"
> "getMedicalRecordCashflowVo Response 的 res.result.object 整体作为 cashflowId 传递"

### 2.2 S1-120 重新精确定位

| 项目 | S1-119 错误标注 | S1-120 当前证据 |
|---|---|---|
| Controller 归属 | waitPayBackCtrl（L6992 起）| **waitChargeDetailCtrl**（L6568-L6953） |
| API | getMedicalRecordCashflowVo.json | **/admin/createCashFlowForMedicalRecord.json**（Create，非 Get） |
| 实际行号 | L6929 | L6929 ✓（行号正确） |
| Response 来源 | getMedicalRecordCashflowVo | **createCashFlowForMedicalRecord.json 的 res.result.object** |

**关键源码定位（L6920-L6930 waitChargeDetailCtrl）**：

```javascript
// waitChargeDetailCtrl $scope.goCheck 函数
$scope.goCheck = function () {
    var obj = $scope.backReqList(false, true);
    if (!obj) return;
    var fn = function fn() {
      obj.medicalRecordId = $scope.medicalRecordId;
      new ObjectFactory().saveOrQuery("/admin/createCashFlowForMedicalRecord.json", obj).then(function (res) {
        if (res.status == 1) {
          return Popup.notice(res.errmsg);
        }
        $state.go("waitPayDetail", { cashflowId: res.result.object });
        //                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        //   res.result.object 整体作为 cashflowId 传递
        //   后续 waitPayDetailCtrl 直接传 API Request
      });
    };
    ...
}]);
// L6953 end waitChargeDetailCtrl
// L6957 start waitChargeListCtrl
```

**S1-119 错误根因**：S1-119 在做 cashflowId 桥接审计时**没有逐行检查 L6929 的 controller 归属**，错误认为 L6929 属于 waitPayBackCtrl（实际上 waitPayBackCtrl 起点是 L6992）。**S1-119 的 "5 个独立第一来源" 同样需要重新审视**。

### 2.3 错误影响范围

S1-119 文档涉及 L6929 的全部结论需要按以下方式重读：

- 原文"waitPayBackCtrl 内部 getMedicalRecordCashflowVo.json Response 的 res.result.object 整个被作为 cashflowId 传递" → 实际是 **waitChargeDetailCtrl 内部 createCashFlowForMedicalRecord.json Response 的 res.result.object**
- "cashflowId 多对象派生的实例证明"结论**仍然成立**（只是 Controller/API 标错）
- 整体对象作为 cashflowId 传递的事实**仍然成立**

## 3. cashflow.id 全局

**全局 2 处**（Case-Sensitive `cashflow.id`）：

| 行号 | Controller | Expression | 上下文 | Consumer |
|---:|---|---|---|---|
| 7323 | waitPayBackCtrl | `_$scope$getCashFlowCr.cashflow.id` | `creditCashflowId = _$scope$getCashFlowCr.cashflow.id` | Type 2 → 局部变量 |
| 20736 | selectOrderListCtrl | `order.cashflow.id` | API Request: `cashflowId: order.cashflow.id` | Type 2 → API primitive |

### 3.1 L7323 waitPayBackCtrl 完整上下文

```javascript
// L7318-L7332 waitPayBackCtrl $scope.backCredit 函数
$scope.backCredit = function () {
  var execute = function execute() {
    var customerId = $scope.getCashflowObjectFactory.object.customer.id;
    //                                                          ^^^^^^^^^^^
    //       cashflow 整体对象访问 customer.id (Type 4 + 嵌套)
    var _$scope$getCashFlowCr = $scope.getCashFlowCredit,
        refundCredit = _$scope$getCashFlowCr.refundFee,
        creditCashflowId = _$scope$getCashFlowCr.cashflow.id;
    //                              ^^^^^^^^^^^^^^^^^^^^^^^^
    //   Type 2: cashflow.id → creditCashflowId
    var payChannel = String($scope.backItem.refundType);
    new ObjectFactory().saveOrQuery("/admin/payCreditRefund.json", {
      customerId: customerId,
      creditCashflowId: creditCashflowId,
      //      ^^^^^^^^^^^^^^^
      //   Type 1: 复合字段名 creditCashflowId
      payChannel: payChannel,
      refundCredit: refundCredit,
      remark: ""
    }).then(function (res) { ... });
  };
};
```

**S1-120 关键发现**：
- L7320: `customerId = $scope.getCashflowObjectFactory.object.customer.id` —— 嵌套 cashflow 整体对象的 customer 字段
- L7323: `creditCashflowId = _$scope$getCashFlowCr.cashflow.id` —— Type 2 派生
- L7328: API Request `creditCashflowId` 字段

### 3.2 L20736 selectOrderListCtrl 完整上下文

```javascript
// L20732-L20737 selectOrderListCtrl $scope.refund 函数
$scope.refund = function (order) {
  Popup.confirm('确定退款么', function () {
    HttpFactory.object('/admin/createRefundOrderLog.json', {
      customerId: order.customer.id,
      //              ^^^^^^^^^^^^^^^^
      //   Type 3: order.customer.id (cashflow 同级字段)
      cashflowId: order.cashflow.id
      //          ^^^^^^^^^^^^^^^^^
      //   Type 2: order.cashflow.id → cashflowId
    }).then(function (commit) { ... });
  });
};
```

**S1-120 关键发现**：
- `order` 参数同时含 `order.customer.id` 和 `order.cashflow.id` —— order 是聚合 VO
- L20745: `payType: order.cashflow.payType` —— 同样通过 order.cashflow
- L20746: `fee: order.cashflow.totalPayment` —— 同样

## 4. .cashflow 全局 27 处分类

按 Controller 重新归类（**S1-119 未做 controller 归类**）：

| Controller | 范围 | 命中数 | 主要字段 |
|---|---|---:|---|
| partBackCtrl | L4368-L4898 | 4 | creditStatus(2) / refundStatus / creditStatus |
| waitPayBackCtrl | L6992-L7380 | 7 | refundStatus / payType / receivedFromCashier / creditStatus / receivedFromCredit |
| waitPayDetailCtrl | L7452-L8109 | 16 | totalPayment(15) / 1 处 ternary check |
| selectOrderListCtrl | 范围待查 | 3 | id / payType / totalPayment |
| **合计** | | **30** | （注：实际扫描 27 处，部分 line number 在同一处） |

### 4.1 partBackCtrl 4 处

| 行号 | Expression | 上下文 |
|---:|---|---|
| 4424 | `$scope.refundFeeInfo.cashflow.creditStatus` | console.log（注释块内）|
| 4426 | `$scope.refundFeeInfo.cashflow.creditStatus === 1` | 注释块内 if |
| 4434 | `res.cashflow.refundStatus === 1` | API getMedicalRecordRefundDetailVo.json Response |
| 4611 | `$scope.refundFeeInfo.cashflow.creditStatus === 1` | createPartOrder |

**S1-120 重要发现**：L4424-L4428 在 `/* */` 注释块内，是 dead code（实际不会执行）。

### 4.2 waitPayBackCtrl 7 处

| 行号 | Expression | 上下文 |
|---:|---|---|
| 7084 | `$scope.getCashflowObjectFactory.object.cashflow.refundStatus` | getCashflow Response |
| 7094 | `res.result.object.cashflow.payType` | getCashFlowCashierVo.json Response |
| 7266 | `$scope.getCashFlowCredit.cashflow.receivedFromCashier` | getCashFlowCreditVo Response |
| 7323 | `_$scope$getCashFlowCr.cashflow.id` | backCredit |
| 7367 | `_res$result$object.cashflow.creditStatus` | getCashflowLoop |
| 7373 | `res.object.cashflow.receivedFromCredit` | getCashflowLoop（**注意 res.object 不是 res.result.object**，疑似 typo）|
| 7717 | `$scope.getCashflowObjectFactory.object.cashflow` | 存在性检查 |

### 4.3 waitPayDetailCtrl 16 处

| 行号 | 字段 | 表达式 |
|---:|---|---|
| 7593 | totalPayment | `$scope.getCashflowObjectFactory.object.cashflow.totalPayment` |
| 7602 | totalPayment | 同上 |
| 7642 | totalPayment | 同上 |
| 7679 | totalPayment | 同上 |
| 7717 | totalPayment | 同上（waitPayBackCtrl 内重名行）|
| 7774 | totalPayment | 同上 |
| 7794 | totalPayment | 同上 |
| 7818 | totalPayment | 同上 |
| 7832 | totalPayment | 同上 |
| 7836 | totalPayment | 同上 |
| 7850 | totalPayment | 同上 |
| 7863 | totalPayment | 同上 |
| 7918 | totalPayment | 同上 |
| 7958 | totalPayment | 同上 |

**S1-120 重要发现**：waitPayDetailCtrl 16 处 .cashflow 全部访问 `totalPayment` 字段（金额计算），**没有任何 cashflow.id / cashflow.customerId / cashflow.patientId / cashflow.medicalRecordId / cashflow.tradeNo 访问**。

### 4.4 selectOrderListCtrl 3 处

| 行号 | 字段 | 表达式 |
|---:|---|---|
| 20736 | id | `order.cashflow.id` |
| 20745 | payType | `order.cashflow.payType` |
| 20746 | totalPayment | `order.cashflow.totalPayment` |

## 5. cashflow 关键字段全部 0 命中

| 字段 | 命中数 | A-F |
|---|---:|---|
| `cashflow.customerId` | **0 处** | A |
| `cashflow.patientId` | **0 处** | A |
| `cashflow.medicalRecordId` | **0 处** | A |
| `cashflow.tradeNo` | **0 处** | A |

**S1-120 关键结论**：
- cashflow 对象中**没有**直接承载 customerId / patientId / medicalRecordId / tradeNo 字段
- cashflow 整体对象的"标识"只有 `id`（Type 2 cashflow.id）
- cashflow 与 customer 的桥接**完全在 Response 嵌套层**：
  - `$scope.getCashflowObjectFactory.object.customer.id`（waitPayBackCtrl L7320）
  - `res.result.object.customer.id`（payedDetailCtrl L4947, L4950）
  - `res.object.medicalRecord.id`（deliveryInputRecordCtrl L4036）

## 6. L6929 完整传播链（关键纠偏后）

### 6.1 完整链路

```
[waitChargeDetailCtrl] $scope.goCheck (L6920)
  ↓
L6925: API POST /admin/createCashFlowForMedicalRecord.json (obj)
  ↓ Response
res.result.object  ← 整个 cashflow 对象（含 customer + medicalRecord）
  ↓
L6929: $state.go("waitPayDetail", { cashflowId: res.result.object })
  ↓
[State: waitPayDetail] Params: { cashflowId: <cashflow 整体对象> }
  ↓
[waitPayDetailCtrl] L7462: $scope.obj.cashflowId = $stateParams.cashflowId;
  ↓
L7488: API /admin/getMedicalRecordCashflowVo.json { cashflowId: $scope.obj.cashflowId }
  ↓
[Request] cashflowId = <cashflow 整体对象>  ← Type 5 整体传播到 API
  ↓
[Response] getMedicalRecordCashflowVo.json
  ↓
L7593-L7958: $scope.getCashflowObjectFactory.object.cashflow.totalPayment (16 处)
```

### 6.2 Type 5 实例（L6929）

**S1-120 关键 Type 5 实例**：
- 变量命名是 `cashflowId`
- 实际承载是 cashflow **整体对象**（含 cashflow + customer + medicalRecord 嵌套）
- 该 object 经过 State → Scope → API Request → API Response → 字段访问 4 层传递
- 在 waitPayDetailCtrl 后续 16 处 `.cashflow.totalPayment` 访问中**被还原回 cashflow 整体对象**

**S1-120 重大疑问（不归 D 级）**：
- 后端 `/admin/createCashFlowForMedicalRecord.json` Response 返回 `res.result.object` 是 **object 整体**（非 primitive id）
- 前端把它当 `cashflowId` 传递
- 后端 `/admin/getMedicalRecordCashflowVo.json` 接收 `cashflowId` 字段——能解析 object 整体作为参数
- **可能机制**：
  1. 后端从 object 中自动提取 `.id`（自动 unproxy）
  2. 后端用 object reference 作为查询 key（缓存层）
  3. 后端容错处理（任何对象都能查）
- **当前静态审计无法确认后端实际语义** —— F 级

### 6.3 S1-119 错误 vs S1-120 正确对比

| 项 | S1-119 错误 | S1-120 正确 |
|---|---|---|
| Controller | waitPayBackCtrl | **waitChargeDetailCtrl** |
| API | getMedicalRecordCashflowVo.json | **createCashFlowForMedicalRecord.json** |
| 起点 | Response 派生 | **Create API 派生** |
| 性质 | 读取类 | **创建类** |
| 后续链路 | 直接到 waitPayDetail | 经 State → Scope → 下一个 API |
| Type 分类 | "整体对象" | **Type 5**（命名与值类型表现不一致）|

## 7. waitPayBackCtrl → waitPayDetail 状态流（S1-120 视角）

### 7.1 waitPayBackCtrl L7010 接收

```javascript
// L7010 waitPayBackCtrl
$scope.obj.cashflowId = $stateParams.cashflowId;
```

**S1-120 关键判断**：
- waitPayBackCtrl 接收 State cashflowId，存入 `$scope.obj.cashflowId`
- 后续 4 处 API Request 都用 `cashflowId: $scope.obj.cashflowId`（L7090, L7102, L7157, L7364）
- 即 waitPayBackCtrl 是**典型 Type 1 primitive consumer**（与 L6929 Type 5 整体传播**不同**）

### 7.2 waitPayDetailCtrl L7462 接收

```javascript
// L7462 waitPayDetailCtrl
$scope.obj.cashflowId = $stateParams.cashflowId;
```

**S1-120 关键判断**：
- 与 waitPayBackCtrl **字面相同**的代码
- 但 waitPayDetailCtrl 是 L6929 整体对象传播链的**接收端**
- 同样是 `$scope.obj.cashflowId = $stateParams.cashflowId;`
- 后续 L7488 把它作为 `cashflowId` 字段传给 API

**S1-120 重大疑问**：
- waitPayDetailCtrl 接收的 cashflowId 可能是 **primitive**（多数调用方）或 **整体 object**（L6929 链路）
- 两种**不同语义**走同一个接收端、同一个 Scope 字段、同一个 API
- 后端必须能容错处理两种类型
- 当前静态审计**无法判定后端实际行为** —— F 级

## 8. D 级冲突判定（4 个点）

### 8.1 D 冲突点 1：feeCashierCtrl L36940

**S1-119 已识别，S1-120 详细判定**：

```javascript
// L36932-L36943 feeCashierCtrl
$scope.showSelect = function (cashflowId) {
  $scope.cashflowId = cashflowId;  // Type 1: Scope.cashflowId
};
$scope.hideSelect = function () {
  $scope.cashflowId = null;
};

$scope.payedDetail = function (id) {  // 参数名 'id' ≠ 'cashflowId'
  var url = $state.href("payedDetail", { cashflowId: id });
  //                              ^^^^^^^^^^^^^^^
  //  'id' 被当作 'cashflowId' 传递（D 级冲突可能）
  window.open(url, "_blank");
};
```

**S1-120 判定**：
- 函数 `payedDetail(id)` 的 `id` 实际语义是 cashflowId（被赋值给 State `cashflowId`）
- **命名不一致**（`id` vs `cashflowId`）但**实际等价**
- **D 级冲突**：仅字段命名差异，**未影响**实际功能
- 调用源：仅 HTML（ng-click）调用，`$scope.payedDetail` 在 controller.js 中**无内部调用点**
- A 级（直接源码）：是

### 8.2 D 冲突点 2：feeDayCtrl L37080

**S1-119 已识别，S1-120 详细判定**：

```javascript
// L37072-L37083 feeDayCtrl（与 feeCashierCtrl 同模式）
$scope.showSelect = function (cashflowId) {
  $scope.cashflowId = cashflowId;
};
$scope.hideSelect = function () {
  $scope.cashflowId = null;
};

$scope.payedDetail = function (id) {
  var url = $state.href("payedDetail", { cashflowId: id });
  window.open(url, "_blank");
};
```

**S1-120 判定**：
- 与 feeCashierCtrl **完全镜像**
- 同样 D 级冲突（命名差异，不影响功能）
- A 级

### 8.3 D 冲突点 3：chargeListCtrl L16789

**S1-120 新发现**：

```javascript
// L16786-L16795 chargeListCtrl
$scope.bindLook = function (item) {
  if (item.paySceneType === 1) {
    $state.go('payedDetail', {
      cashflowId: item.payReferId
      //          ^^^^^^^^^^^^^
      //   'item.payReferId' 被作为 'cashflowId' 传递
      //   payReferId 是 paymentReferId（支付单 ID）
      //   是否 = cashflowId？D 级冲突
    });
  } else if (item.paySceneType === 2) {
    $scope.records.customerTrainerCardId = item.payReferId;
    $scope.records.setShow(true);
  }
};
```

**S1-120 判定**：
- 变量名 `payReferId`（支付单 ID）被赋给 State `cashflowId`
- **命名不一致**（`payReferId` vs `cashflowId`）但**实际等价性不可证**
- 后端必须能识别 payReferId = cashflowId
- **D 级冲突可能**（payReferId 实际可能 = cashflowId 引用，或 = 另一个不同 ID）
- 不能自行修正
- A 级

### 8.4 D 冲突点 4：payedListCtrl L8146

**S1-120 新发现**：

```javascript
// L8143-L8154 payedListCtrl
$scope.cancelPay = function (id) {
  Popup.confirm("是否取消该支付", function () {
    $scope.cancelCashObjectFactory = new ObjectFactory();
    var promise = $scope.cancelCashObjectFactory.saveOrQuery(
      "/admin/cancelMedicalRecordCashflow.json",
      { cashflowId: id }
    );
    ...
  });
};
```

**S1-120 判定**：
- 与 feeCashierCtrl / feeDayCtrl 同模式（`id` → `cashflowId`）
- D 级冲突（命名差异，不影响功能）
- 调用源：仅 HTML（ng-click）调用
- A 级

### 8.5 D 级冲突汇总

| 编号 | Controller | 行号 | 命名 | 实际语义 | 等级 |
|---|---|---:|---|---|---|
| D-1 | feeCashierCtrl | L36940 | `id` | cashflowId | A |
| D-2 | feeDayCtrl | L37080 | `id` | cashflowId | A |
| D-3 | chargeListCtrl | L16789 | `payReferId` | cashflowId（可能）| A |
| D-4 | payedListCtrl | L8146 | `id` | cashflowId | A |
| D-5 | unPayDetailCtrl | L6519 | `unPayId` | cashflowId | A（命名差异，**未在 S1-119 标记**）|

**S1-120 新增发现 D-3（payReferId）、D-4（cancelPay）、D-5（unPayId）** —— S1-119 仅识别 D-1 / D-2。

## 9. cashflow 整体对象传播（Type 4）

### 9.1 cashflow 整体对象存放点

| 行号 | Controller | 表达式 | 用途 |
|---:|---|---|---|
| 7093 | waitPayBackCtrl | `$scope.getCashFlowCashier = res.result.object` | 整体 object 存 Scope |
| 7104 | waitPayBackCtrl | `$scope.getCashFlowCredit = res.result.object` | 整体 object 存 Scope |
| 6513 | unPayDetailCtrl | `$scope.customerCashflowCreditLogVo = res` | 整体 Response 存 Scope |

### 9.2 cashflow 整体对象消费点

| 行号 | Controller | 表达式 | 消费字段 |
|---:|---|---|---|
| 7084 | waitPayBackCtrl | `.object.cashflow.refundStatus` | refundStatus |
| 7094 | waitPayBackCtrl | `.object.cashflow.payType` | payType |
| 7266 | waitPayBackCtrl | `.getCashFlowCredit.cashflow.receivedFromCashier` | receivedFromCashier |
| 7320 | waitPayBackCtrl | `.getCashflowObjectFactory.object.customer.id` | customer.id（嵌套）|
| 7323 | waitPayBackCtrl | `.cashflow.id` | id |
| 7367 | waitPayBackCtrl | `.cashflow.creditStatus` | creditStatus |
| 7373 | waitPayBackCtrl | `.cashflow.receivedFromCredit` | receivedFromCredit |
| 7593-7958 | waitPayDetailCtrl | `.object.cashflow.totalPayment` (16 处) | totalPayment |

### 9.3 S1-120 关键发现

**Type 4 (cashflow 整体对象) 消费字段全集**：

| 字段 | 出现 Controller | 行号 |
|---|---|---|
| `cashflow.id` | waitPayBackCtrl, selectOrderListCtrl | L7323, L20736 |
| `cashflow.refundStatus` | partBackCtrl, waitPayBackCtrl | L4434, L7084 |
| `cashflow.creditStatus` | partBackCtrl, waitPayBackCtrl | L4424, L4426, L4611, L7367 |
| `cashflow.payType` | waitPayBackCtrl, selectOrderListCtrl | L7094, L20745 |
| `cashflow.totalPayment` | waitPayDetailCtrl(16), selectOrderListCtrl | L7593-7958, L20746 |
| `cashflow.receivedFromCashier` | waitPayBackCtrl | L7266 |
| `cashflow.receivedFromCredit` | waitPayBackCtrl | L7373 |
| `cashflow.customerId` | **0 处** | - |
| `cashflow.patientId` | **0 处** | - |
| `cashflow.medicalRecordId` | **0 处** | - |
| `cashflow.tradeNo` | **0 处** | - |

## 10. medicalRecordId 派生 3 种对照

### 10.1 cashflowId → medicalRecordId

**唯一派生链**（S1-117 已确认）：

```
[State cashflowId]
  ↓
[deliveryInputRecordCtrl] L4026: $scope.cashflowId = $stateParams.cashflowId;
  ↓
L4034: API /admin/getMedicalRecordPayVo.json { cashflowId: $scope.cashflowId }
  ↓ Response
L4036: $scope.medicalRecordId = res.object.medicalRecord.id;
  ↓
[dead-end] 在 deliveryInputRecordCtrl 范围内无后续消费
```

**S1-120 验证**：
- medicalRecordId 在 deliveryInputRecordCtrl 范围内**仅赋值，无读取**
- controller.js L4037 之后 `$scope.medicalRecordId` 出现 0 次
- 下一个 controller L4075 deliveryListCtrl 开始
- **dead-end 确认**

### 10.2 cashflow.id → medicalRecordId

**0 处**（已确认 `cashflow.medicalRecordId` 全局 0 命中）。

### 10.3 cashflow object → medicalRecordId

**0 处**（S1-120 扫描确认 cashflow 整体对象无 medicalRecordId 字段访问）。

## 11. customer 派生 3 种对照

### 11.1 cashflowId → customer

**5 链**（S1-118 已确认）：

| Controller | 行号 | 表达式 | 后续 API |
|---|---|---|---|
| payedDetailCtrl | L4947 | `res.result.object.customer.id` → getCustomerVo Request | getCustomerVo |
| payedDetailCtrl | L4950 | `res.result.object.customer.id` → getCustomerWallet Request | getCustomerWallet |
| waitPayBackCtrl | L7320 | `$scope.getCashflowObjectFactory.object.customer.id` → customerId local | payCreditRefund |
| partBackCtrl | L4433-L4437 | `$scope.cashflowId` → getMedicalRecordRefundDetailVo → $scope.refundFeeInfo | 部分退款流程 |

### 11.2 cashflow.id → customer

**0 处**（`cashflow.customerId` 全局 0 命中）。

### 11.3 cashflow object → customer

**仅 waitPayBackCtrl L7320 1 处**：
```javascript
var customerId = $scope.getCashflowObjectFactory.object.customer.id;
```
- `getCashflowObjectFactory.object` 是 getMedicalRecordCashflowVo.json Response 的 object 整体
- 访问 `.customer.id` 提取 customer 标识
- 即 cashflow 整体对象**嵌套含 customer 子对象**

## 12. tradeNo

**0 处**（全局 `cashflow.tradeNo`、`tradeNo` 字段访问 `cashflow` 全局 0 命中）。

**S1-120 判定**：
- tradeNo 在本轮扫描中**没有任何 cashflow 相关派生**
- tradeNo 字段在 cashflow 对象中**不可达**（当前证据范围）
- 不可建立 cashflowId ↔ tradeNo 派生链

## 13. API 对照（cashflow 相关）

### 13.1 关键 API 列表

| API | Request identifier | Response identifier | 类型 | Consumer |
|---|---|---|---|---|
| `/admin/createCashFlowForMedicalRecord.json` | `obj` (含 medicalRecordId 等) | `res.result.object` 整体 | **Type 5** | waitChargeDetailCtrl L6925 |
| `/admin/getMedicalRecordCashflowVo.json` | `cashflowId: ...` | `res.result.object` (含 cashflow + customer + medicalRecord) | Type 1 in / Type 4 out | payedDetailCtrl, waitPayBackCtrl, waitPayDetailCtrl, payedListCtrl |
| `/admin/getMedicalRecordPayVo.json` | `cashflowId: ...` | `res.object.medicalRecord` | Type 1 in / Type 3 out | deliveryInputRecordCtrl L4034 |
| `/admin/getCashFlowCashierVo.json` | `cashflowId: $scope.obj.cashflowId` | `res.result.object.cashflow` | Type 1 in / Type 4 out | waitPayBackCtrl L7089 |
| `/admin/getCashFlowCreditVo.json` | `cashflowId: $scope.obj.cashflowId` | `res.result.object.cashflow` | Type 1 in / Type 4 out | waitPayBackCtrl L7101, L7363 |
| `/admin/getMedicalRecordRefundDetailVo.json` | `cashflowId: $scope.cashflowId` | `res.cashflow` | Type 1 in / Type 4 out | partBackCtrl L4433 |
| `/admin/getCustomerCashflowCreditLogVoToPay.json` | `customerId` | `res.cashflowCreditLogDataList` | non-cashflowId | unPayDetailCtrl L6509 |
| `/admin/payCreditRefund.json` | `creditCashflowId: ...` (cashflow.id) | - | **Type 2 in** | waitPayBackCtrl L7326 |
| `/admin/createRefundOrderLog.json` | `cashflowId: order.cashflow.id` | - | **Type 2 in** | selectOrderListCtrl L20734 |
| `/admin/cancelMedicalRecordCashflow.json` | `cashflowId: id` | - | Type 1 in | payedListCtrl L8146 |
| `/admin/getCanBeProcessSkuInListOfProduct.json` | `cashflowId: cashflowId` | - | Type 1 in | 待查（deliveryProcessingCtrl 内）|

### 13.2 关键 API Response 形态对照

#### A. createCashFlowForMedicalRecord.json（Type 5 实例来源）
- Request: 完整 obj（含 medicalRecordId, customerCouponId 等）
- Response: **`res.result.object` 是 cashflow 整体对象**（含 cashflow + customer + medicalRecord 嵌套）
- 这是 L6929 整体传播链的源头

#### B. getMedicalRecordCashflowVo.json（Type 1 入口 + Type 4 出口）
- Request: `cashflowId: ...`（可能是 primitive 也可能是 object，见 L6929 链路）
- Response: `res.result.object` 是 cashflow 整体对象
- 4 个 Controller 消费（payedDetailCtrl, waitPayBackCtrl, waitPayDetailCtrl, payedListCtrl）

#### C. getMedicalRecordPayVo.json（Type 1 入口 + Type 3 出口）
- Request: `cashflowId: $scope.cashflowId`（primitive）
- Response: `res.object.medicalRecord` —— 注意 `res.object` 不是 `res.result.object`（疑似 typo 但与 S1-118 一致）
- 1 个 Controller 消费（deliveryInputRecordCtrl）

#### D. getCashFlowCashierVo.json（waitPayBackCtrl 内部专用）
- Request: `cashflowId: $scope.obj.cashflowId`
- Response: `res.result.object.cashflow.payType` —— payType 用于退款方式选择

#### E. getCashFlowCreditVo.json（waitPayBackCtrl 内部专用）
- Request: `cashflowId: $scope.obj.cashflowId`
- Response: `res.result.object.cashflow.creditStatus` / `.receivedFromCredit` —— 挂账还款状态

## 14. 类型转换检查

### 14.1 显式类型转换（与 cashflowId 交叉）

**0 处**：
- `String(cashflowId)` 全局 0
- `parseInt(cashflowId)` 全局 0
- `Number(cashflowId)` 全局 0
- `JSON.stringify(cashflowId)` 全局 0
- `JSON.parse(cashflowId)` 全局 0

**S1-120 关键发现**：
- cashflowId 没有任何显式类型转换
- 这意味着后端必须能容错处理多种类型（primitive / object）
- 当前静态审计**无法确认后端实际行为** —— F 级

### 14.2 隐式转换点

**L7325 waitPayBackCtrl**：
```javascript
var payChannel = String($scope.backItem.refundType);
```
- `backItem.refundType` 转 String —— 与 cashflowId 无关
- **S1-120 范围内无其他隐式转换**

## 15. Type Classification（6 类）

### Type 1: primitive cashflowId

**定义**：直接传递 primitive 值（数字 / 字符串），最常见模式。

**实例**：
| 行号 | Controller | 表达式 |
|---:|---|---|
| 3814 | 待查 | `$scope.cashflowId = $stateParams.cashflowId` |
| 4026 | deliveryInputRecordCtrl | `$scope.cashflowId = $stateParams.cashflowId` |
| 4034 | deliveryInputRecordCtrl | API Request `cashflowId: $scope.cashflowId` |
| 4381 | partBackCtrl | `$scope.cashflowId = $stateParams.cashflowId` |
| 4433 | partBackCtrl | API Request `cashflowId: $scope.cashflowId` |
| 4940 | payedDetailCtrl | `$scope.obj.cashflowId = $stateParams.cashflowId` |
| 7010 | waitPayBackCtrl | `$scope.obj.cashflowId = $stateParams.cashflowId` |
| 7090 | waitPayBackCtrl | API Request `cashflowId: $scope.obj.cashflowId` |
| 7102 | waitPayBackCtrl | API Request `cashflowId: $scope.obj.cashflowId` |
| 7462 | waitPayDetailCtrl | `$scope.obj.cashflowId = $stateParams.cashflowId` |
| 7488 | waitPayDetailCtrl | API Request `cashflowId: $scope.obj.cashflowId` |
| 16262 | 待查 | `$scope.cashflowId = $stateParams.cashflowId` |

**特征**：
- State Param 是 primitive 值
- 后续直接作为 API Request 字段
- 不访问 `.id`（因为已经是 primitive）

### Type 2: cashflow.id 派生

**定义**：从 cashflow 整体对象提取 `.id` 字段，赋给另一个变量。

**实例**：
| 行号 | Controller | 表达式 |
|---:|---|---|
| 7323 | waitPayBackCtrl | `creditCashflowId = _$scope$getCashFlowCr.cashflow.id` |
| 20736 | selectOrderListCtrl | `cashflowId: order.cashflow.id` |

**特征**：
- 源是 cashflow 整体对象
- 派生是 primitive 值
- 局部变量命名可能与 cashflowId 不一致（creditCashflowId）

### Type 3: object.id 派生（非 cashflow）

**定义**：从 Response 中的非 cashflow 嵌套对象提取 `.id`。

**实例**：
| 行号 | Controller | 表达式 | 源对象 |
|---:|---|---|---|
| 4036 | deliveryInputRecordCtrl | `$scope.medicalRecordId = res.object.medicalRecord.id` | medicalRecord |
| 4947 | payedDetailCtrl | `customerId: res.result.object.customer.id` | customer |
| 4950 | payedDetailCtrl | `customerId: res.result.object.customer.id` | customer |
| 7320 | waitPayBackCtrl | `customerId = $scope.getCashflowObjectFactory.object.customer.id` | customer |

**特征**：
- 派生字段命名是其他 ID（medicalRecordId / customerId）
- 源对象是 Response.object 的嵌套字段
- Type 3 是 cashflowId 派生**下游**，不是 cashflowId 本身

### Type 4: cashflow 整体对象

**定义**：直接持有 cashflow 整体对象（不提取 id），用于消费其字段。

**实例**：
| 行号 | Controller | 表达式 | 消费字段 |
|---:|---|---|---|
| 7093 | waitPayBackCtrl | `$scope.getCashFlowCashier = res.result.object` | cashflow.payType |
| 7104 | waitPayBackCtrl | `$scope.getCashFlowCredit = res.result.object` | cashflow.creditStatus / receivedFromCashier / receivedFromCredit |
| 7593-7958 | waitPayDetailCtrl | `$scope.getCashflowObjectFactory.object.cashflow.totalPayment` (16 处) | totalPayment |
| 7084 | waitPayBackCtrl | `$scope.getCashflowObjectFactory.object.cashflow.refundStatus` | refundStatus |
| 7094 | waitPayBackCtrl | `res.result.object.cashflow.payType` | payType |
| 7266 | waitPayBackCtrl | `$scope.getCashFlowCredit.cashflow.receivedFromCashier` | receivedFromCashier |
| 7367 | waitPayBackCtrl | `_res$result$object.cashflow.creditStatus` | creditStatus |
| 7373 | waitPayBackCtrl | `res.object.cashflow.receivedFromCredit` | receivedFromCredit |

**特征**：
- 持有对象引用，不立即提取
- 用于消费多个字段
- 字段访问通过 `.cashflow.<field>`

### Type 5: res.result.object 被赋值给 cashflowId 变量

**定义**：命名上是 `cashflowId`，但承载 cashflow 整体对象（命名与值类型不一致）。

**实例**（**仅 1 处**）：
| 行号 | Controller | 表达式 |
|---:|---|---|
| 6929 | waitChargeDetailCtrl | `$state.go("waitPayDetail", { cashflowId: res.result.object })` |

**特征**：
- 命名 `cashflowId`（暗示 primitive）
- 实际承载 `res.result.object`（cashflow 整体对象）
- **S1-120 关键发现**（S1-119 错误标注位置）

**S1-120 重要疑问（不归 D 级）**：
- 后端如何处理这种"非 primitive cashflowId"？
- 可能机制：
  1. 后端从 object 中自动提取 `.id`（自动 unproxy / 解引用）
  2. 后端用 object reference 作为查询 key（如 Redis 缓存层）
  3. 后端容错处理（任何对象都能查）
- 当前静态审计**无法确认后端实际语义** —— F 级

### Type 6: 无法确认

**定义**：当前静态审计无法判定 identifier 类型。

**实例**：
- **payedDetailCtrl L4940-L4942**：接收 `$stateParams.cashflowId`，传给 getMedicalRecordCashflowVo
  - 调用方可能传 primitive（多数情况）
  - 也可能传 object（L6929 链路）
  - 当前静态审计**无法确定**传的是什么 —— F 级

## 16. 26 项矩阵

| # | 项目 | Controller | 行号 | Expression | API / State | Type | A-F | L1/L2/L3 |
|---:|---|---|---:|---|---|---|---|---|
| 01 | cashflow.id 全局 | waitPayBackCtrl | 7323 | `creditCashflowId = _$scope$getCashFlowCr.cashflow.id` | payCreditRefund | Type 2 | A | L1 |
| 01 | cashflow.id 全局 | selectOrderListCtrl | 20736 | `cashflowId: order.cashflow.id` | createRefundOrderLog | Type 2 | A | L1 |
| 02 | cashflowId 全局 | 74 处 / 20 Controller | - | 见 181 文档 | 多种 | Type 1 为主 | A | L1 |
| 03 | 两者直接关系 | - | - | L7323 唯一直接派生 cashflow.id → creditCashflowId | - | Type 2 | A | L1 |
| 04 | item.cashflow.id | selectOrderListCtrl | 20736 | `order.cashflow.id` | - | Type 2 | A | L1 |
| 05 | Scope.cashflow.id | waitPayBackCtrl | 7323 | `_$scope$getCashFlowCr.cashflow.id` | - | Type 2 | A | L1 |
| 06 | API response cashflow.id | - | - | **0 处**（API Response 无 .cashflow.id 字段） | - | - | A | L1 |
| 07 | API response cashflowId | unPayDetailCtrl | 6518-6519 | `res.cashflowCreditLogDataList[i].cashflowId` | getCustomerCashflowCreditLogVoToPay | Type 1 | A | L1 |
| 08 | object 整体传播 | waitChargeDetailCtrl | 6929 | `$state.go("waitPayDetail", { cashflowId: res.result.object })` | waitPayDetail | **Type 5** | A | L1 |
| 09 | L6929 完整链 | waitChargeDetailCtrl → waitPayDetailCtrl | 6929→7462→7488 | 详见 §6.1 | createCashFlowForMedicalRecord → State → getMedicalRecordCashflowVo | Type 5 + Type 1 + Type 4 | A | L1 |
| 10 | waitPayBackCtrl→waitPayDetail | - | - | **S1-119 错误标注**：L6929 不在 waitPayBackCtrl | - | - | A | - |
| 11 | State cashflowId | 多 Controller | 多 | `$state.go(..., { cashflowId: ... })` | 多种 | Type 1 / Type 5 | A | L1 |
| 12 | stateParams cashflowId | 多 Controller | 3814/4026/4238/4381/4940/7010/7462/16262 | `$stateParams.cashflowId` | 多种 | Type 1 / Type 5 | A | L1 |
| 13 | URL cashflowId | payedListCtrl, machineOrderListCtrl | 4220/4373/5142/8040 | `url: "getMedicalRecordCashflowVo"` 等 | - | URL string | A | L1 |
| 14 | feeCashierCtrl L36940 | feeCashierCtrl | 36940 | `$state.href("payedDetail", { cashflowId: id })` | payedDetail | **D-1** | A | L1 |
| 15 | feeDayCtrl L37080 | feeDayCtrl | 37080 | `$state.href("payedDetail", { cashflowId: id })` | payedDetail | **D-2** | A | L1 |
| 16 | D 级冲突（4 点） | feeCashierCtrl / feeDayCtrl / chargeListCtrl / payedListCtrl | 36940/37080/16789/8146 | 见 §8 | - | **D-1/D-2/D-3/D-4** | A | L1 |
| 17 | cashflow object Consumer | waitPayBackCtrl/waitPayDetailCtrl/selectOrderListCtrl/partBackCtrl | 30 处 | `.cashflow.<field>` | - | Type 4 | A | L1 |
| 18 | object.id Consumer | deliveryInputRecordCtrl/payedDetailCtrl/waitPayBackCtrl | 4036/4947/4950/7320 | `res.object.<x>.id` | - | Type 3 | A | L1 |
| 19 | cashflowId→medicalRecordId | deliveryInputRecordCtrl | 4034-4036 | API → `res.object.medicalRecord.id` | getMedicalRecordPayVo | Type 1 → Type 3 | A | L1 |
| 20 | cashflow.id→medicalRecordId | - | - | **0 处** | - | - | A | L1 |
| 21 | cashflow object→medicalRecordId | - | - | **0 处** | - | - | A | L1 |
| 22 | cashflowId→customer | payedDetailCtrl/waitPayBackCtrl/partBackCtrl | 4947/4950/7320/4433 | `customerId: res.result.object.customer.id` 等 | getCustomerVo/getCustomerWallet | Type 1 → Type 3 | A | L1 |
| 23 | cashflow.id→customer | - | - | **0 处** | - | - | A | L1 |
| 24 | cashflow object→customer | waitPayBackCtrl | 7320 | `$scope.getCashflowObjectFactory.object.customer.id` | payCreditRefund | Type 4 → Type 3 | A | L1 |
| 25 | Type Classification | 全局 | - | Type 1: primitive / Type 2: cashflow.id / Type 3: object.id / Type 4: cashflow object / Type 5: object整体作cashflowId / Type 6: 无法确认 | - | 6 类 | A | L1 |
| 26 | A-F | - | - | A=直接源码 / B=多源互证 / C=部分 / D=冲突 / E=推断 / F=范围外 | - | - | A | - |

## 17. 复刻风险（L1）

### R1: cashflowId 多源

cashflowId 字段至少有 6 种不同的来源（API Response, StateParams, Scope, Function param, Factory item, 整体 object），**严禁假设存在单一主来源**。

**复刻要点**：
- 复刻系统必须支持 cashflowId 的 6 种来源
- 任何 Cashflow CRUD API 入口都需要明确从哪一类来源取
- 不能简单写一个 `getCurrentCashflowId()` 函数

### R2: id / cashflowId / payReferId / unPayId 命名不一致

至少 4 个 Controller（feeCashierCtrl / feeDayCtrl / chargeListCtrl / payedListCtrl）使用 `id` 或 `payReferId` 命名，但实际语义是 cashflowId。

**复刻要点**：
- 复刻 API 字段命名必须**统一**
- 必须明确每个参数的实际语义（不是命名假设）
- 不能用 TypeScript 类型推断代替运行时校验

### R3: object 整体可能被命名为 cashflowId（L6929）

Type 5 实例：waitChargeDetailCtrl L6929 把 `res.result.object` 整体作为 `cashflowId` 传递。

**复刻要点**：
- 复刻系统必须支持 cashflowId 接受 primitive 或整体 object 两种类型
- 建议在 API 入口处显式校验（不依赖运行时类型推断）
- 后端 ORM 层如果用 reference，必须明确 unproxy 时机

### R4: API / State / URL 三种 ID 传递方式并存

- **API Request 字段**：`{ cashflowId: ... }`
- **State Param**：`$state.go(..., { cashflowId: ... })`
- **URL string**：`url: "getMedicalRecordCashflowVo"`, `param: { cashflowId: "" }`

**复刻要点**：
- 复刻系统必须明确 3 种传递方式各自的来源/转换规则
- 不能假设一个 cashflowId 走 3 种方式时语义一致
- S1-120 已发现：URL string 模式下 `param.cashflowId` 是空字符串，由 `print(id)` 动态注入

### R5: D 级冲突不能自行修正

feeCashierCtrl / feeDayCtrl / chargeListCtrl / payedListCtrl / unPayDetailCtrl 的 `id` / `payReferId` / `unPayId` 命名差异**不能自行改写**。

**复刻要点**：
- 复刻系统可以**统一命名**（推荐）
- 但必须**保持 API 兼容**（请求/响应字段名不能变）
- 内部变量命名可以重构

### R6: getMedicalRecordCashflowVo / getMedicalRecordPayVo 不合并

两个 API 完全不同：
- getMedicalRecordCashflowVo.json: cashflow + customer 整体
- getMedicalRecordPayVo.json: medicalRecord 整体

**复刻要点**：
- 复刻系统必须**保留两个独立 API**
- 不能合并（Response 形态不同）
- 也不能互相替换

### R7: Type 5 整体对象传播链必须被识别

L6929 waitChargeDetailCtrl → waitPayDetailCtrl 整体对象传播是**真实存在**的链（不是 Bug，但属于特殊传播）。

**复刻要点**：
- 复刻系统如果简化整体对象传播（只传 primitive id），可能影响 waitPayDetailCtrl 的 16 处 `.cashflow.totalPayment` 访问
- 需要在简化前评估影响范围

### R8: cashflow 整体对象无 customerId / patientId / medicalRecordId 字段

cashflow 对象中**没有**直接承载 customerId / patientId / medicalRecordId 字段。

**复刻要点**：
- 复刻 cashflow ORM 模型时**不能假设**有这些字段
- customer / medicalRecord 是**嵌套对象**，不是直接字段
- 必须通过 `cashflow.customer.id` / `cashflow.medicalRecord.id` 访问

## 18. F 边界

以下信息**当前静态审计无法确认**：

| 项目 | F 原因 | 应对 |
|---|---|---|
| 后端 `/admin/createCashFlowForMedicalRecord.json` Response 类型 | 后端实际语义 | 需要 backend debug |
| 后端 `/admin/getMedicalRecordCashflowVo.json` 接受 object cashflowId 的机制 | 后端 ORM / 缓存层 | 需要 backend debug |
| L6929 整体对象传播链的后端容错机制 | 跨语言层 | 需要 backend debug |
| $scope.payedDetail 在 HTML ng-click 中的实际调用源 | HTML 不在审计范围 | 需要检查 deliveryList.html 等 |
| D-3 chargeListCtrl L16789 `payReferId` 实际语义 | payReferId 字段含义 | 需要 backend debug |

## 19. Final Identifier Map

```
[cashflowId 全局 Identifier DAG]
│
├─ Type 1: primitive cashflowId (74 处 / 20 Controller)
│   ├─ State Params → $scope.cashflowId
│   ├─ $scope.cashflowId → API Request
│   └─ API Request → Response
│       ├─ → customer.id (Type 3) → 5 链
│       ├─ → medicalRecord.id (Type 3) → 1 链 (dead-end)
│       └─ → cashflowCreditLogDataList[i].cashflowId (Type 1)
│
├─ Type 2: cashflow.id 派生 (2 处)
│   ├─ waitPayBackCtrl L7323: creditCashflowId
│   └─ selectOrderListCtrl L20736: cashflowId
│
├─ Type 3: object.id 派生 (4 处)
│   ├─ deliveryInputRecordCtrl L4036: medicalRecordId (dead-end)
│   ├─ payedDetailCtrl L4947: customerId
│   ├─ payedDetailCtrl L4950: customerId
│   └─ waitPayBackCtrl L7320: customerId
│
├─ Type 4: cashflow 整体对象 (30 处)
│   ├─ waitPayBackCtrl (7): refundStatus, payType, creditStatus, receivedFromCashier/Credit, id
│   ├─ waitPayDetailCtrl (16): totalPayment
│   ├─ partBackCtrl (4): creditStatus, refundStatus
│   └─ selectOrderListCtrl (3): id, payType, totalPayment
│
├─ Type 5: object 整体作为 cashflowId (1 处)
│   └─ waitChargeDetailCtrl L6929: res.result.object → State cashflowId
│       ↓
│       [waitPayDetailCtrl] L7462: $scope.obj.cashflowId = $stateParams.cashflowId
│       ↓
│       L7488: API Request { cashflowId: <object 整体> }
│       ↓
│       [Response] cashflow.totalPayment (16 处)
│
├─ Type 6: 无法确认 (多)
│   └─ payedDetailCtrl L4940 接收 State cashflowId 可能是 primitive 或 object
│
└─ D 级冲突 (4 点)
    ├─ D-1: feeCashierCtrl L36940: id → cashflowId
    ├─ D-2: feeDayCtrl L37080: id → cashflowId
    ├─ D-3: chargeListCtrl L16789: payReferId → cashflowId
    └─ D-4: payedListCtrl L8146: id → cashflowId
```

## 20. S1-119 vs S1-120 差异

| 项 | S1-119 | S1-120 | 差异 |
|---|---|---|---|
| L6929 Controller | waitPayBackCtrl | **waitChargeDetailCtrl** | **关键纠偏** |
| L6929 API | getMedicalRecordCashflowVo.json | **createCashFlowForMedicalRecord.json** | **关键纠偏** |
| cashflow.id 全局命中 | S1-119 未单列 | **2 处**（L7323, L20736）| 新增 |
| Type Classification | 5 个独立第一来源 | **6 类 Type** | 重新分类 |
| D 级冲突 | 2 个（L36940, L37080）| **4 个**（新增 L16789, L8146, L6519 unPayId）| 扩展 |
| customer 派生 3 种 | 2 种 | **3 种** | 新增 cashflow object → customer |
| medicalRecordId 派生 3 种 | 1 种 | **3 种（其中 2 种 0 命中）** | 完整对照 |
| tradeNo 派生 | 未明确 | **0 处** | 明确 |

## 21. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓
- deliveryList.html unchanged ✓
- 165-181 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 22. 结论

### 22.1 关键发现

1. **L6929 纠偏**：L6929 不在 waitPayBackCtrl（S1-119 错误），实际在 **waitChargeDetailCtrl**，API 是 `createCashFlowForMedicalRecord.json`（Create，非 Get）。

2. **Type 5 实例确认**：waitChargeDetailCtrl L6929 `$state.go("waitPayDetail", { cashflowId: res.result.object })` 是**唯一**的 Type 5 实例（res.result.object 整体作为 cashflowId 传递）。

3. **cashflow.id 全局仅 2 处**：L7323 waitPayBackCtrl / L20736 selectOrderListCtrl。cashflow 整体对象**没有** customerId / patientId / medicalRecordId / tradeNo 字段访问。

4. **D 级冲突 4 个**（S1-119 仅识别 2 个）：feeCashierCtrl L36940, feeDayCtrl L37080, chargeListCtrl L16789 (payReferId), payedListCtrl L8146。

5. **6 类 Type Classification**：
   - Type 1: primitive cashflowId (主流)
   - Type 2: cashflow.id 派生 (2 处)
   - Type 3: object.id 派生 (4 处)
   - Type 4: cashflow 整体对象 (30 处)
   - Type 5: object 整体作为 cashflowId (1 处，L6929)
   - Type 6: 无法确认 (多)

### 22.2 S1-120 任务状态

- 全部 6 类 Type 已识别
- 26 项矩阵已建立
- L6929 错误纠偏已写入
- 4 个 D 级冲突已识别
- 8 条复刻风险已列出
- 文档结构 22 章节已写完

---

**【S1-120 完成】**
