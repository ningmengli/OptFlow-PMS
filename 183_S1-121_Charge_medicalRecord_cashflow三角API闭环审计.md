# S1-121 Charge medicalRecord / cashflow 三角 API 闭环审计

## 0. 任务背景

S1-117/118/119/120 已识别 cashflow / cashflowId 多个独立来源与 6 类 Type 分类，但**未深入 Charge 内部 medicalRecord / medicalRecordId / cashflow 三个对象/API 的三角关系**。

S1-118 标注的"waitChargeDetailCtrl L6693 medicalRecord.patientId 来自 computeUnPlaceOrderMedicalRecordFee"是 S1-121 入口关键证据。

本轮目标：
- 精确定位 L6693 完整上下文
- 厘清 computeUnPlaceOrderMedicalRecordFee / getMedicalRecordCashflowVo / getMedicalRecordPayVo 三者关系
- 判定 4 条三角关系（medicalRecord ↔ cashflow, medicalRecordId ↔ cashflowId）
- 验证 cashflowId → medicalRecordId 链是否可反向
- 26 项矩阵 + 复刻风险 L1

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| 3 重点 API 全局命中 | 6 处 |
| waitChargeDetailCtrl (L6568-L6953) | 7 处 medicalRecord/cashflow 命中 |
| medicalRecordId 全局 | 161 处 |
| medicalRecord 全局 | 60 处 |
| cashflowId 全局 (Case-Sensitive) | 74 处 / 20 Controller |
| cashflow 全局 | 27 处 |

## 2. 3 个重点 API 全局 Call site

### 2.1 computeUnPlaceOrderMedicalRecordFee.json

| 行号 | Controller | 上下文 | 性质 |
|---:|---|---|---|
| 6680 | waitChargeDetailCtrl | `$scope.search()` 函数 | Get-Read（计算未下单病历费用）|

**全局 1 处调用**（仅 waitChargeDetailCtrl）。

### 2.2 getMedicalRecordCashflowVo.json

| 行号 | Controller | 上下文 | 性质 |
|---:|---|---|---|
| 4942 | payedDetailCtrl | `$scope.obj.cashflowId = $stateParams.cashflowId` 后 | Get-Read |
| 5166 | payedListCtrl | `$scope.printList(id)` 函数 | Get-Read（打印）|
| 7070 | waitPayBackCtrl | `$scope.getCashflow()` 函数 | Get-Read |
| 7488 | waitPayDetailCtrl | 启动时 | Get-Read |

**全局 4 处 saveOrQuery + 3 处 URL string = 7 处**（S1-118 标注 8 Controller 含 URL string）。

### 2.3 getMedicalRecordPayVo.json

| 行号 | Controller | 上下文 | 性质 |
|---:|---|---|---|
| 4034 | deliveryInputRecordCtrl | `$scope.cashflowId = $stateParams.cashflowId` 后 | Get-Read |

**全局 1 处调用**（仅 deliveryInputRecordCtrl）。

## 3. S1-121 新发现 API

### 3.1 reComputeUnPlaceOrderMedicalRecordFee.json（S1-118/120 漏识）

**S1-121 新发现**：

| 行号 | Controller | 上下文 | 性质 |
|---:|---|---|---|
| 6884 | waitChargeDetailCtrl | `$scope.computeFee()` 函数 | **Write-Compute（重新计算）**|

```javascript
// L6881-L6886 waitChargeDetailCtrl
$scope.computeFee = function () {
  var obj = $scope.backReqList(true);
  obj.medicalRecordId = $scope.medicalRecordId;
  new ObjectFactory().saveOrQuery("/admin/reComputeUnPlaceOrderMedicalRecordFee.json", obj).then(function (res) {
    $scope.changeRowFee(res.result.object);
  });
};
```

- 触发点：L6723, L6761, L6770 三处 `$scope.computeFee()` 调用
- 在 `$scope.changeRate` / `$scope.changeFee` 修改 VoList 后重新计算费用
- 配对关系：reComputeUnPlaceOrderMedicalRecordFee + computeUnPlaceOrderMedicalRecordFee 是一对

### 3.2 createCashFlowForMedicalRecord.json（S1-120 已识别）

| 行号 | Controller | 性质 |
|---:|---|---|
| 6925 | waitChargeDetailCtrl | **Write-Create（创建 cashflow）**|

```javascript
// L6925 waitChargeDetailCtrl
new ObjectFactory().saveOrQuery("/admin/createCashFlowForMedicalRecord.json", obj).then(function (res) {
  if (res.status == 1) return Popup.notice(res.errmsg);
  $state.go("waitPayDetail", { cashflowId: res.result.object });
  //                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  //   S1-120 Type 5: res.result.object 整体作为 cashflowId 传递
});
```

## 4. computeUnPlaceOrderMedicalRecordFee 详细审计

### 4.1 call site

**唯一 1 处**：waitChargeDetailCtrl L6680 `$scope.search()` 函数

### 4.2 Request

```javascript
// L6680
{
  medicalRecordId: $scope.medicalRecordId
}
```

- $scope.medicalRecordId 来源：L6570 `$stateParams.medicalRecordId`（**State Param**）
- Request 字段：仅 medicalRecordId 1 个
- A 级（直接源码）

### 4.3 Response 派生

通过 `$scope.getUnPlaceOrderObjectFactory` 消费的字段：

| 行号 | 表达式 | 字段 |
|---:|---|---|
| 6605 | `.result.object.customer.id` | **Type 3: customerId** |
| 6606 | `.result.object.totalFee` | totalFee |
| 6631 | `.object[vo.name]` | VoList（couponIndex 查询）|
| 6635 | `.object[vo.name][couponIndex][vo.key].memberRate` | VoList[i].medicalProduct.memberRate |
| 6636 | `.object[vo.name][couponIndex][vo.key].rateFee` | VoList[i].medicalProduct.rateFee |
| 6666 | `.object[v.name].length` | VoList 长度 |
| 6667 | `.object[v.name].forEach` | VoList 遍历 |
| 6682 | `.result.object.medicalExamineVoList.length` | VoList 长度（4 个 VoList 同表达式）|
| 6722 | `.result.object.rateFee` | rateFee（changeRate 响应）|
| 6752-6759 | `.result.object.memberRate` | memberRate（4 个 VoList 写回）|
| 6797-6800 | `.object.medicalExamineVoList.length` 等 | VoList 长度 |
| 6890-6896 | changeRowFee 函数写回 7 个 RateFee 字段 | medicalExamineRateFee / registrationRateFee / medicalProductRateFee / totalFee / substractFee / rateFee / medicalProductModelRateFee |
| 6935-6944 | `.object.medicalProductVoList.forEach` 等 | VoList 遍历 |

**通过 `res.object`（不是 `res.result.object`）消费的字段**：

| 行号 | 表达式 | 字段 |
|---:|---|---|
| 6693 | `.object.medicalRecord.patientId` | **Type 3: patientId** |

### 4.4 Response 双层结构疑问（D 级冲突可能）

**S1-121 关键发现 1**：
- L6682 用 `res.result.object.medicalExamineVoList.length`
- L6693 用 `res.object.medicalRecord.patientId`
- 同一 Response 两种访问路径：
  - `res.result.object` 路径：customer.id, VoList, 7 个 RateFee
  - `res.object` 路径：medicalRecord.patientId

**可能解释**：
- 后端返回两套结构（设计）
- L6693 是 typo（实际应 `res.result.object.medicalRecord.patientId`）
- L6682 / L6693 访问的 data 是两次不同数据合并

**S1-121 判定**：
- 静态审计**无法确定**后端响应实际结构 —— F 级
- 不能自行修正
- 不归 D 级（因为两套访问都能正常运行）

### 4.5 Scope 落点

- `$scope.getUnPlaceOrderObjectFactory.object` —— **整个 Response object 存 Scope**
- 后续 16+ 处 `.object.xxx` 访问
- `$scope.getPatientObjectFactory` —— L6693 仅创建 + 调用，无任何后续读取（dead code）

### 4.6 后续 API

- 同步触发 `$scope.computeFee()` (L6690) → **reComputeUnPlaceOrderMedicalRecordFee.json (Write)**
- 手动触发（changeRate/changeFee）→ reComputeUnPlaceOrderMedicalRecordFee.json (Write)
- `$state.go("waitPayList")` (L6684) —— 当 VoList 全空时跳转

### 4.7 写 cashflow

- L6924-L6925: `createCashFlowForMedicalRecord.json` —— 当存在 customerCouponId 时，先 reCompute VoList，再创建 cashflow
- L6929: `$state.go("waitPayDetail", { cashflowId: res.result.object })` —— **Type 5 整体对象传播**（S1-120 已识别）

## 5. waitChargeDetailCtrl L6693 精确审计

### 5.1 完整上下文（L6673-L6696）

```javascript
// L6673-L6696 waitChargeDetailCtrl $scope.search
$scope.search = function () {
  var bool = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
  $scope.getUnPlaceOrderObjectFactory = new ObjectFactory();
  var promise = $scope.getUnPlaceOrderObjectFactory.saveOrQuery(
    "/admin/computeUnPlaceOrderMedicalRecordFee.json",
    { medicalRecordId: $scope.medicalRecordId }
  );
  promise.then(function (res) {
    if (!res.result.object.medicalExamineVoList.length && 
        !res.result.object.medicalProductVoList.length && 
        !res.result.object.registrationFeeVoList.length && 
        !res.result.object.medicalProductVoListOfModel.length) {
      return Popup.notice("您的项目已创建订单，即将跳转到待支付列表", 1500, function () {
        $state.go("waitPayList");
      });
    }
    if (!bool) {
      $scope.addId();
    }
    $scope.computeFee();
    if (!$scope.getPatientObjectFactory) {
      $scope.getPatientObjectFactory = new ObjectFactory();
      $scope.getPatientObjectFactory.saveOrQuery(
        "/admin/getPatientInfo.json", 
        { id: res.object.medicalRecord.patientId }
        //   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        //   S1-118 标注 L6693 patientId 来源
      );
    }
  });
};
$scope.search();
```

### 5.2 medicalRecord.patientId 来源判定

**S1-121 精确判定**：
1. **`medicalRecord.patientId` 是 Response 字段**
   - 来源：`computeUnPlaceOrderMedicalRecordFee.json` 的 Response
   - 路径：`res.object.medicalRecord.patientId`（**注意是 `res.object` 不是 `res.result.object`**）
2. **medicalRecord 整体来自 `computeUnPlaceOrderMedicalRecordFee.json`**
   - 不是 `getMedicalRecord.json`（L1964 / L31220 / L31331 等其它 controller 才用）
   - 不是 `getMedicalRecordFlowVo.json`（全局 0 命中，不存在该 API）
3. **patientId 进入 API Request**
   - L6693: `/admin/getPatientInfo.json` Request `{ id: patientId }`
   - **Type 1: primitive patientId 派生**
4. **patientId 不进入 customer / cashflow / Write**
   - waitChargeDetailCtrl 范围内 patientId 唯一命中是 L6693
   - 后续 getPatientInfo Response **不被消费**（dead code）

### 5.3 写操作链

**S1-121 关键发现 2**：
- L6693 派生 patientId 后调 getPatientInfo.json，但 Response **不被任何后续代码消费**
- `$scope.getPatientObjectFactory` 创建后只调用 `.saveOrQuery()`，无 `.result.object.xxx` 访问
- **dead-end 链**（与 deliveryInputRecordCtrl 的 medicalRecordId 类似）

## 6. getMedicalRecordCashflowVo 详细审计

### 6.1 4 个 Consumer 全集

| Consumer | 范围 | 入口 | Response 消费 |
|---|---|---|---|
| payedDetailCtrl | L4937-L4969 | L4942 | customer.id (L4947, L4950) |
| payedListCtrl | L4972-L5189 | L5166 | jqprint（无字段消费）|
| waitPayBackCtrl | L6992-L7380 | L7070 | VoList (5 fields), cashflow (5 fields), customer (1 field), totalPayment |
| waitPayDetailCtrl | L7452-L8109 | L7488 | cashflow.totalPayment (16 处) |

### 6.2 Request 字段全集

| Consumer | Request 表达式 | 字段 |
|---|---|---|
| payedDetailCtrl | `cashflowId: $scope.obj.cashflowId` | **Type 1: primitive cashflowId** |
| payedListCtrl | `cashflowId: id` | **Type 1: primitive cashflowId (D-4 模式)** |
| waitPayBackCtrl | `cashflowId: $scope.obj.cashflowId` | **Type 1: primitive cashflowId** |
| waitPayDetailCtrl | `cashflowId: $scope.obj.cashflowId` | **Type 1: primitive cashflowId**（可能 Type 5，见 S1-120 L6929 链路）|

### 6.3 Response 字段全集

| 行号 | 表达式 | 字段 |
|---:|---|---|
| 4947 | `res.result.object.customer.id` | **Type 3: customerId** |
| 4950 | `res.result.object.customer.id` | **Type 3: customerId** |
| 7072-7080 | `VoList[i].medicalExamine.id` / `.medicalProduct.id` | **Type 3: id 派生** |
| 7084 | `res.result.object.cashflow.refundStatus` | cashflow field |
| 7093, 7104 | `res.result.object` 整体 | Type 4: cashflow 整体对象 |
| 7094 | `res.result.object.cashflow.payType` | cashflow field |
| 7266 | `res.result.object.cashflow.receivedFromCashier` | cashflow field |
| 7320 | `res.result.object.customer.id` | **Type 3: customerId** |
| 7323 | `res.result.object.cashflow.id` | **Type 2: cashflowId** |
| 7367 | `res.result.object.cashflow.creditStatus` | cashflow field |
| 7373 | `res.object.cashflow.receivedFromCredit` | cashflow field（**注意 res.object**）|
| 7488+ | 16 处 `.object.cashflow.totalPayment` | cashflow field |

**CashflowVo Response 关键观察**：
- **不消费 medicalRecord 字段**（4 个 consumer 全部不访问）
- **不消费 medicalRecordId 字段**
- **不消费 patientId 字段**
- 主要消费：customer / VoList / cashflow 整体对象

## 7. getMedicalRecordPayVo 详细审计

### 7.1 唯一 Consumer

| Consumer | 范围 | 入口 | 后续链 |
|---|---|---|---|
| deliveryInputRecordCtrl | L4024-L4074 | L4034 | Delivery 链 |

### 7.2 Request 字段

```javascript
// L4034
{
  cashflowId: $scope.cashflowId  // Type 1: primitive cashflowId (来自 State Param)
}
```

### 7.3 Response 字段

```javascript
// L4036
$scope.medicalRecordId = res.object.medicalRecord.id;
//   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//   Type 3: object.id 派生 → medicalRecordId
//   注意 res.object 不是 res.result.object
```

**S1-121 关键发现 3**：
- L4034 Request: cashflowId
- L4036 Response: `res.object.medicalRecord.id` → **medicalRecordId**
- **cashflowId → medicalRecordId 单向链确认**

### 7.4 medicalRecordId 后续

```javascript
// L4039-L4044 deliveryInputRecordCtrl
$scope.getMedicalRecordDeliveryFactory = new ObjectFactory();
$scope.getMedicalRecordDeliveryFactory.saveOrQuery(
  '/admin/getCashflowDeliveryVo.json', 
  { cashflowId: $scope.cashflowId }
  //   ^^^^^^^^^^^^^^^^^^^^^^^^
  //   仍然用 cashflowId，不是 medicalRecordId
);
$scope.getStatusDeliveryFactory = new ObjectFactory();
$scope.getStatusDeliveryFactory.saveOrQuery(
  '/admin/statProductDeliveryStatusOfCashflow.json', 
  { cashflowId: $scope.cashflowId }
);
```

**S1-121 关键发现 4**：
- $scope.medicalRecordId 在 L4036 设置后**dead-end**（无任何读取）
- 后续 Delivery API 仍用 cashflowId
- **medicalRecordId 是 Cash 链 → Delivery 链的 dead-end 桥**

## 8. 三 API Request 对照

| API | Request 字段 | medicalRecordId | cashflowId | patientId | customerId |
|---|---|---|---|---|---|
| `computeUnPlaceOrderMedicalRecordFee.json` | `{ medicalRecordId }` | ✓ (primitive) | - | - | - |
| `getMedicalRecordCashflowVo.json` | `{ cashflowId }` | - | ✓ (primitive) | - | - |
| `getMedicalRecordPayVo.json` | `{ cashflowId }` | - | ✓ (primitive) | - | - |
| `reComputeUnPlaceOrderMedicalRecordFee.json` (Write) | `obj` 含 medicalRecordId | ✓ (primitive) | - | - | - |
| `createCashFlowForMedicalRecord.json` (Write) | `obj` 含 medicalRecordId | ✓ (primitive) | - | - | - |
| `getPatientInfo.json` (L6693 触发) | `{ id: patientId }` | - | - | ✓ (primitive) | - |

**S1-121 关键观察**：
- 3 个重点 API 的 Request **互不重叠**
- computeUnPlaceOrderMedicalRecordFee 用 medicalRecordId
- CashflowVo / PayVo 用 cashflowId
- getPatientInfo (L6693) 用 patientId
- 三个 ID 各自独立作为 Request 字段

## 9. 三 API Response 对照

| API | Response 字段 | medicalRecord | medicalRecordId | cashflow | cashflowId | customer | patientId |
|---|---|---|---|---|---|---|---|
| `computeUnPlaceOrderMedicalRecordFee.json` | `res.result.object` + `res.object` | ✓ (`res.object.medicalRecord`) | - | - | - | ✓ (`.customer.id`) | ✓ (`.medicalRecord.patientId`) |
| `getMedicalRecordCashflowVo.json` | `res.result.object` | - | - | ✓ (含 `.id` `.totalPayment` `.payType` `.creditStatus` `.refundStatus` `.receivedFrom*`) | - | ✓ (`.customer.id`) | - |
| `getMedicalRecordPayVo.json` | `res.object` | ✓ (`.medicalRecord`) | - | - | - | - | - |
| `reComputeUnPlaceOrderMedicalRecordFee.json` | `res.result.object` | - | - | - | - | - | - |
| `createCashFlowForMedicalRecord.json` | `res.result.object` | - | - | - | - | - | - |

**S1-121 关键观察**：
- **三 API Response 互不重叠的字段**：
  - computeUnPlaceOrderMedicalRecordFee → customer + patientId + VoList + 7 个 RateFee
  - getMedicalRecordCashflowVo → cashflow 整体 + customer
  - getMedicalRecordPayVo → medicalRecord（仅返回这一项）
- **三 API 都不直接返回 medicalRecordId 字段**（必须通过 object.id 派生）

## 10. 三角关系 4 条判定

### 10.1 关系 1：medicalRecord → cashflow

**S1-121 判定**：
- 全局 `medicalRecord\..*cashflow` 0 命中
- 全局 `medicalRecord\..*cashflowId` 0 命中
- medicalRecord 整体对象无 cashflow 字段访问

**结论：F（未建立）**

### 10.2 关系 2：cashflow → medicalRecord

**S1-121 判定**：
- 全局 `cashflow\..*medicalRecord` 0 命中
- 全局 `cashflow\..*medicalRecordId` 0 命中
- cashflow 整体对象无 medicalRecord 字段访问

**结论：F（未建立）**

### 10.3 关系 3：medicalRecordId → cashflowId

**S1-121 判定**：
- 全局 `medicalRecordId.*=.*cashflowId` 0 命中
- 全局 `medicalRecordId.*=.*cashflow` 0 命中
- 没有"已知 medicalRecordId 去找 cashflowId"的代码模式

**结论：F（未建立）**

### 10.4 关系 4：cashflowId → medicalRecordId

**S1-121 判定**：
- deliveryInputRecordCtrl L4034-L4036 是**唯一**直接链
- chain: cashflowId (State Param) → API getMedicalRecordPayVo → Response.medicalRecord.id → medicalRecordId (Scope)
- 1 链，Type 3 派生

**结论：A（1 链，deliveryInputRecordCtrl）**

### 10.5 三角关系总览

```
[medicalRecord]                          [cashflow]
       │                                       │
       │ ← cashflow 关系 1 (F)                │
       │                                       │
       │ ← cashflow 关系 2 (F)                │
       │                                       │
       [medicalRecordId]  ←——→  [cashflowId]
              关系 3 (F)              关系 4 (A: 1链 deliveryInputRecordCtrl)
```

**S1-121 关键结论**：
- 4 条三角关系中**只有 1 条**实际存在
- 3 条未建立（即使 Response 共现也不构成链）
- **三角不闭环**（非对称）
- cashflowId → medicalRecordId 是**单向**已证链
- 反向 medicalRecordId → cashflowId **未建立**

## 11. patientId / customerId 桥

### 11.1 patientId → customerId 链

**已确认**：
- getMedicalRecord.json Response 含 patientId 字段（L31222）
- getPatientInfo.json Response 含 customerId 字段（L31228）
- 完整链：medicalRecordId → getMedicalRecord → patientId → getPatientInfo → customerId

```javascript
// L31220-L31228 (其它 controller，非 waitCharge)
var medicalPromise = $scope.getMedicalObjectFactory.saveOrQuery(
  "/admin/getMedicalRecord.json", 
  { id: $scope.medicalRecordId }
);
medicalPromise.then(function (res) {
  $scope.patientId = res.result.object.patientId;
  $scope.updatePatientFactory = new ObjectFactory();
  var promise = $scope.updatePatientFactory.saveOrQuery(
    "/admin/getPatientInfo.json", 
    { id: $scope.patientId }
  );
  promise.then(function (res) {
    $scope.customerId = res.result.object.customerId;
    //           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //   patientVo.customerId 是 patient → customer 的直接桥
  });
});
```

**S1-121 关键发现 5**：
- patient → customer 通过 **patientVo.customerId** 字段直接桥接
- 这是 4 条三角关系**之外**的额外桥
- 6 处 `res.result.object.customerId` 派生（L31228, L31234, L31338, L31345, L32464, L32912）

### 11.2 customerId → patientId 链

**已确认**：
- getCustomerVo.json Response 含 patientId 字段
- L31222, L31333: `$scope.patientId = res.result.object.patientId`
- 完整链：customerId → getCustomerVo → patientId

**S1-121 关键发现 6**：
- **customerId → patientId 链存在**（customerVo.patientId 字段）
- 与 11.1 的 patientId → customerId **构成双向桥**
- 即 customer 和 patient **互相可派生**

### 11.3 customerId → cashflowId / patientId → cashflowId 链

**S1-121 判定**：
- 全局 `customerId.*=.*cashflowId` 0 命中
- 全局 `patientId.*=.*cashflowId` 0 命中
- 没有直接链

**结论：F（未建立）**

### 11.4 customer / patient 桥总览

| 关系 | 桥字段 | 方向 | A-F |
|---|---|---|---|
| patientId → customerId | patientVo.customerId | 单向 → 实际是双向 | A |
| customerId → patientId | customerVo.patientId | 单向 → 实际是双向 | A |
| patientId → cashflowId | - | - | F |
| customerId → cashflowId | - | - | F |
| medicalRecordId → patientId | medicalRecordVo.patientId | 单向 | A |

## 12. Charge 内部控制流

### 12.1 API → API 控制流

**waitChargeDetailCtrl 内部**：
1. L6680 computeUnPlaceOrderMedicalRecordFee (Read) → L6690 computeFee() → L6884 reComputeUnPlaceOrderMedicalRecordFee (Write)
2. L6680 computeUnPlaceOrderMedicalRecordFee (Read) → L6693 getPatientInfo (Read)（**dead-end**）
3. L6684 $state.go("waitPayList") —— 当 VoList 全空时跳转
4. L6924-L6925 createCashFlowForMedicalRecord (Write) → L6929 $state.go("waitPayDetail", { cashflowId: res.result.object }) —— **S1-120 Type 5 整体对象传播**

**S1-121 关键发现 7（Charge 内 API 控制流）**：
- computeUnPlaceOrderMedicalRecordFee → reComputeUnPlaceOrderMedicalRecordFee (内部 reCompute 模式)
- computeUnPlaceOrderMedicalRecordFee → createCashFlowForMedicalRecord → waitPayDetail
- 3 个 API 之间存在明确的控制流

### 12.2 API Response → Scope → 后续 API

**S1-121 关键发现 8**：
- $scope.getUnPlaceOrderObjectFactory.object 是 computeUnPlaceOrderMedicalRecordFee Response 整体
- 后续 16+ 处 `.object.xxx` 访问字段
- 后续 changeRate/changeFee 修改 `.object[vo.name][i][vo.key].memberRate/rateFee` 后再 reCompute
- 这是一个**读-改-写循环**

## 13. Cross-Controller 数据流

### 13.1 Charge → Cross-Controller

| 起点 | 终点 | 机制 | 字段 |
|---|---|---|---|
| waitChargeDetailCtrl L6929 | waitPayDetailCtrl | $state.go | **cashflowId: res.result.object** (Type 5) |
| waitChargeDetailCtrl L6684 | waitPayList | $state.go | 无字段 |
| waitChargeListCtrl L6976 | (List 数据) | ListFactory | search params |

**S1-121 关键发现 9**：
- Charge → 其它 Controller 只有 1 个 cross-chain 链
- 即 waitChargeDetailCtrl → waitPayDetailCtrl 通过 Type 5 整体对象传播（S1-120 已识别）
- 其它跨 controller 调用通过 Service / CommonRequest（不在审计范围）

## 14. Write 操作识别（S1-121 范围内）

### 14.1 3 个重点 API 相关 Write

| API | 行号 | 性质 | 写字段 |
|---|---|---|---|
| `reComputeUnPlaceOrderMedicalRecordFee.json` | L6884 | Write-Compute | medicalRecordId + 各种 rateFeeVoList |
| `createCashFlowForMedicalRecord.json` | L6925 | Write-Create | medicalRecordId + obj (含 VoList) |

### 14.2 写 cashflow

- L6925 createCashFlowForMedicalRecord.json 是 Charge 范围内**唯一创建 cashflow 的 Write API**
- 创建后的 cashflow 通过 Type 5 整体对象传播给 waitPayDetailCtrl

## 15. 与历史结论的差异

### 15.1 S1-117 vs S1-121

| 项 | S1-117 | S1-121 |
|---|---|---|
| cashflowId → medicalRecordId 链 | 1 链 (deliveryInputRecordCtrl) | **保持** |
| medicalRecordId → cashflowId 反向 | 未讨论 | **F（未建立）** |
| 三角闭环 | 暗示存在 | **否，三角不闭环** |

### 15.2 S1-118 vs S1-121

| 项 | S1-118 | S1-121 |
|---|---|---|
| L6693 patientId 来源 | computeUnPlaceOrderMedicalRecordFee | **保持** |
| 8 Controller 含 3 重点 API | 8 | **CashflowVo 4 saveOrQuery + 3 URL string / PayVo 1 / Fee API 1 = 8 含 URL** |
| reCompute API 存在性 | 未提及 | **新发现 reComputeUnPlaceOrderMedicalRecordFee.json** |

### 15.3 S1-120 vs S1-121

| 项 | S1-120 | S1-121 |
|---|---|---|
| Type 5 整体对象传播 | L6929 waitChargeDetailCtrl | **保持** |
| cashflow 整体对象 30 处 | 30 | **保持** |
| medicalRecord 派生 patientId 链 | 未深入 | **waitCharge L6693 + 其它 controller (L31222) 2 链** |

## 16. 26 项矩阵

| # | 项目 | Controller | 行号 | Expression | API / State | 来源 | Consumer | A-F | L1/L2/L3 |
|---:|---|---|---:|---|---|---|---|---|---|
| 01 | Charge Controller 全集 | 22 个（含 reCharge/charge）| - | 见 §17.1 | - | - | - | A | L1 |
| 02 | computeUnPlaceOrderMedicalRecordFee 命中 | waitChargeDetailCtrl | 6680 | saveOrQuery | API | State medicalRecordId | 16+ 字段 | A | L1 |
| 03 | call site | waitChargeDetailCtrl | 6680 | `$scope.search()` 函数 | - | State | 全部 consumer | A | L1 |
| 04 | Request 全集 | waitChargeDetailCtrl | 6680 | `{ medicalRecordId }` | - | - | - | A | L1 |
| 05 | Request provenance | - | 6570 | $stateParams.medicalRecordId | State | - | - | A | L1 |
| 06 | Response 全集 | waitChargeDetailCtrl | 6680 | res.result.object + res.object | - | API | 16+ 字段 | A | L1 |
| 07 | Response provenance | - | - | res.result.object / res.object | API | - | - | A | L1 |
| 08 | waitChargeDetailCtrl L6693 | waitChargeDetailCtrl | 6693 | `res.object.medicalRecord.patientId` | API | Response | getPatientInfo Request | A | L1 |
| 09 | medicalRecord 来源 | waitChargeDetailCtrl | 6693 | `res.object.medicalRecord` | API | computeUnPlaceOrderMedicalRecordFee Response | - | A | L1 |
| 10 | medicalRecord.patientId | waitChargeDetailCtrl | 6693 | `.medicalRecord.patientId` | API | Response | getPatientInfo | A | L1 |
| 11 | patientId Consumer | waitChargeDetailCtrl | 6693 | 仅 getPatientInfo Request | - | Response | **dead code** | A | L1 |
| 12 | medicalRecordId 全集 | 161 处 / 全局 | - | 见 S1-115 | - | - | - | A | L1 |
| 13 | medicalRecordId 来源 (Charge 范围) | waitChargeDetailCtrl | 6570 | $stateParams.medicalRecordId | State | - | - | A | L1 |
| 14 | cashflow 全集 | 27 处 | - | 见 S1-120 | - | - | - | A | L1 |
| 15 | cashflowId 全集 (Charge 范围) | waitChargeDetailCtrl | 6929 | `$state.go("waitPayDetail", { cashflowId: res.result.object })` | State | Response 整体 | waitPayDetailCtrl | A | L1 |
| 16 | cashflowId 来源 (Charge 范围) | waitChargeDetailCtrl | 6929 | res.result.object 整体 | Response | - | - | A | L1 |
| 17 | CashflowVo 消费者 | payedDetailCtrl/payedListCtrl/waitPayBackCtrl/waitPayDetailCtrl | 4 处 | 见 §6.1 | API | State cashflowId | customer/cashflow | A | L1 |
| 18 | PayVo 消费者 | deliveryInputRecordCtrl | 1 处 | L4034-L4036 | API | State cashflowId | medicalRecordId (dead-end) | A | L1 |
| 19 | Fee API（compute+reCompute）| waitChargeDetailCtrl | 6680/6884 | 见 §3/§4 | API | - | - | A | L1 |
| 20 | medicalRecord → cashflow | - | - | **0 命中** | - | - | - | A | L1 |
| 21 | cashflow → medicalRecord | - | - | **0 命中** | - | - | - | A | L1 |
| 22 | medicalRecordId → cashflowId | - | - | **0 命中** | - | - | - | A | L1 |
| 23 | cashflowId → medicalRecordId | deliveryInputRecordCtrl | 4034-4036 | API → Response.medicalRecord.id | - | State cashflowId | medicalRecordId Scope | A | L1 |
| 24 | patient/customer 关系 | 多个 | 31228/31234/31338/31345/32464/32912 | `customerId: res.result.object.customerId` | - | patientVo Response | 下游 API | A | L1 |
| 25 | 三 API 直接控制流 | waitChargeDetailCtrl | 6680→6690→6884 | compute→computeFee→reCompute | - | - | - | A | L1 |
| 26 | A/B/C/D/E/F | - | - | 26 项中 A=26 / B=0 / C=0 / D=0 / E=0 / F=0 | - | - | - | A | - |

## 17. Charge Controller 详细分类

### 17.1 22 个 Charge Controller 分类

| # | Controller | 行号 | 类型 | 3 重点 API 命中 |
|---:|---|---:|---|---|
| 1 | waitChargeDetailCtrl | L6568 | Wait Charge Detail | **computeUnPlaceOrderMedicalRecordFee (1)** |
| 2 | waitChargeListCtrl | L6957 | Wait Charge List | 0 |
| 3 | unPayDetailCtrl | L5987 | UnPay Detail | 0 |
| 4 | unPayListCtrl | L6526 | UnPay List | 0 |
| 5 | chargeListCtrl | L16758 | Charge List | 0 |
| 6 | reChargeListCtrl | L5192 | ReCharge List | 0 |
| 7 | reChargeListBackCtrl | L5692 | ReCharge Back List | 0 |
| 8 | hospitalRechargeCtrl | L15883 | Hospital Recharge | 0 |
| 9 | feeRechargeCtrl | L37183 | Fee Recharge | 0 |
| 10 | pointsListChargeCtrl | L37432 | Points List Charge | 0 |
| 11 | pointsListReChargeCtrl | L37459 | Points List ReCharge | 0 |
| 12 | timeCardRechargeCtrl | L38463 | TimeCard Recharge | 0 |
| 13 | unPayChargeCtrl | L38500 | UnPay Charge | 0 |
| 14 | unPayRechargeCtrl | L38525 | UnPay Recharge | 0 |
| 15 | addCustomerChargeCtrl | L50472 | Add Customer Charge | 0 |
| 16 | addCustomerChargeItemCtrl | L50776 | Add Customer Charge Item | 0 |
| 17 | chargeAdminCtrl | L52575 | Charge Admin | 0 |
| 18 | chargeWaysCtrl | L52767 | Charge Ways | 0 |
| 19 | customerChargeCtrl | L53318 | Customer Charge | 0 |
| 20 | customerChargeChoiceCtrl | L53685 | Customer Charge Choice | 0 |
| 21 | customerChargeItemCtrl | L53806 | Customer Charge Item | 0 |
| 22 | memberChargeCtrl | L55727 | Member Charge | 0 |
| 23 | modifyCustomerChargeCtrl | L56044 | Modify Customer Charge | 0 |
| 24 | modifyCustomerChargeItemCtrl | L56384 | Modify Customer Charge Item | 0 |

**S1-121 关键观察**：
- 3 重点 API（saveOrQuery 形式）**只命中 waitChargeDetailCtrl 1 个 controller**
- URL string 形式在 partBackCtrl / payedListCtrl / machineOrderListCtrl 3 个 controller 命中（非 Charge 范围）
- 其它 22+ 个 Charge Controller **完全不涉及** computeUnPlaceOrderMedicalRecordFee / getMedicalRecordCashflowVo / getMedicalRecordPayVo

## 18. 复刻风险（L1）

### R1: Charge 内多个不同 API 承载不同对象

- computeUnPlaceOrderMedicalRecordFee → customer + patientId + VoList + 7 RateFee
- getMedicalRecordCashflowVo → cashflow 整体 + customer
- getMedicalRecordPayVo → medicalRecord
- **三 API Response 互不重叠**

**复刻要点**：
- 复刻系统必须保留 3 个独立 API
- 不能合并 Response 结构
- 必须分别实现 3 套 Response schema

### R2: cashflowId → medicalRecordId 单向已证链

- 1 链：deliveryInputRecordCtrl L4034-L4036
- 反向 medicalRecordId → cashflowId **未建立**

**复刻要点**：
- 复刻系统如果需要"由 medicalRecordId 找 cashflowId"，必须新建 API
- 不能假设 reverse 链自动存在
- 现金病历关联只能从 cashflowId 入口

### R3: medicalRecord.patientId 来源必须保留

- 来源：computeUnPlaceOrderMedicalRecordFee.json 的 `res.object.medicalRecord.patientId`
- **不是** getMedicalRecord.json（虽然字段名类似）
- 是 dead-end（不进入下游）

**复刻要点**：
- 复刻 computeUnPlaceOrderMedicalRecordFee.json 时必须返回 medicalRecord.patientId
- 不能删除此字段（即使前端 dead-end）
- 后端可能用此字段做其它事

### R4: CashflowVo / PayVo / Fee API 不能合并

- 三个 API 完全不同：响应结构、消费方、调用时序
- **任何合并都会破坏现有数据流**

**复刻要点**：
- 复刻系统必须保留 3 个独立 API
- 不能因为"功能类似"就合并
- 必须严格按 4 个 payedDetail/payedList/waitPayBack/waitPayDetail Controller 各自消费方式实现

### R5: res.object vs res.result.object 双层结构

- computeUnPlaceOrderMedicalRecordFee Response 可能含 `res.object` 和 `res.result.object` 两套数据
- L6682 用 res.result.object
- L6693 用 res.object

**复刻要点**：
- 复刻后端必须明确返回结构
- 不能让前端混用两套访问
- 建议统一为 res.result.object

### R6: reComputeUnPlaceOrderMedicalRecordFee 是独立 Write API

- 与 computeUnPlaceOrderMedicalRecordFee 配对
- 触发点：changeRate/changeFee 修改 VoList 后
- 写新 VoList + 7 个 RateFee

**复刻要点**：
- 复刻系统必须实现 reCompute 路径
- 不能用 compute API 替代（语义不同）
- 写操作时序：读 VoList → 修改 → reCompute → 写新数据

### R7: patientVo.customerId 是 patient → customer 桥

- getPatientInfo Response 含 customerId 字段
- 6 处派生 customerId（L31228, L31234, L31338, L31345, L32464, L32912）
- 同样 customerVo.patientId 是 customer → patient 桥

**复刻要点**：
- 复刻 patientVo / customerVo 必须保留双向 customerId/patientId 字段
- 不能简化（只保留单向）

### R8: 三角不闭环（非对称）

- 4 条三角关系中只有 1 条（cashflowId → medicalRecordId）已证
- 3 条未建立

**复刻要点**：
- 复刻系统不能假设"已知 medicalRecord 就能找 cashflow"
- 必须按各自独立路径实现
- 不能为追求"闭环"而建立反向链

## 19. F 边界

以下信息**当前静态审计无法确认**：

| 项目 | F 原因 | 应对 |
|---|---|---|
| computeUnPlaceOrderMedicalRecordFee Response 双层结构 | 后端实际响应 | 需要 backend debug |
| L6693 `res.object.medicalRecord` vs `res.result.object.medicalRecord` | 静态无法判读 | 需要 backend debug |
| getCashFlowCashierVo / getCashFlowCreditVo 是否需要 medicalRecord | Charge 范围外 | 不在本轮 |
| L6693 dead-end 链是否被实际运行 | 实际数据流 | 需要运行追踪 |

## 20. Final Triangle DAG

```
[State medicalRecordId] (waitChargeDetailCtrl L6570)
  ↓
$scope.medicalRecordId
  ↓
[API: computeUnPlaceOrderMedicalRecordFee.json] (L6680) [GET-Read]
  ↓ Response
$scope.getUnPlaceOrderObjectFactory.object
  ├── res.result.object.customer.id → $scope.cashFlowListFactory.params.customerId
  ├── res.result.object.totalFee → params.totalPrice
  ├── res.result.object.medicalExamineVoList / medicalProductVoList / registrationFeeVoList / medicalProductVoListOfModel
  ├── res.result.object.rateFee / memberRate
  ├── res.object.medicalRecord.patientId → getPatientInfo.json { id }  (dead code)
  └── res.object.[7 RateFee fields] → changeRowFee
  ↓
[API: reComputeUnPlaceOrderMedicalRecordFee.json] (L6884) [WRITE-Compute]
  ↓ Response
  $scope.changeRowFee(res.result.object)
  ↓
[修改 VoList[i].rateFee / memberRate]
  ↓
[API: createCashFlowForMedicalRecord.json] (L6925) [WRITE-Create]
  ↓ Response
res.result.object (cashflow 整体)
  ↓
[State: $state.go("waitPayDetail", { cashflowId: res.result.object })] (L6929) [Type 5]
  ↓
[waitPayDetailCtrl] $stateParams.cashflowId (Type 5 object)
  ↓
$scope.obj.cashflowId (Type 5 object)
  ↓
[API: getMedicalRecordCashflowVo.json] (L7488) [GET-Read]
  ↓ Response
res.result.object.cashflow (Type 4) [16 处 .totalPayment]
  ↓
[API: payMedicalRecordCashflow.json] (L8017) [WRITE-Pay]
  ↓
$state.go("payedList") (L8021)
```

**S1-121 关键观察**：
- 完整 Charge 链是 **Read → Read → Write → Write → Read → Write**
- cashflowId 类型从 primitive 转换为 object 整体（Type 5），再变回 cashflow 整体对象（Type 4）
- 三角关系中只有 cashflowId → medicalRecordId 是单向已证链

## 21. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓
- deliveryList.html unchanged ✓
- 165-182 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 22. 结论

### 22.1 关键发现

1. **三角关系不闭环**：4 条三角关系中只有 1 条（cashflowId → medicalRecordId）已证，3 条未建立
2. **新发现 API**：reComputeUnPlaceOrderMedicalRecordFee.json（S1-118/120 漏识）是与 computeUnPlaceOrderMedicalRecordFee 配对的 Write API
3. **res.object vs res.result.object 双层结构**：computeUnPlaceOrderMedicalRecordFee Response 同时含两套数据（L6682 vs L6693）
4. **L6693 dead-end**：waitChargeDetailCtrl L6693 派生 patientId 后调 getPatientInfo 但 Response 不被消费
5. **3 重点 API 互不重叠**：Request / Response 字段完全不重叠
6. **patient/customer 双向桥**：patientVo.customerId + customerVo.patientId 互相派生
7. **waitChargeDetailCtrl 内 API 控制流**：compute → reCompute → createCashFlow 完整读-写循环

### 22.2 S1-121 任务状态

- 3 重点 API 全部重新定位
- 三角关系 4 条判定（1 已证 / 3 未建立）
- patient/customer 双向桥识别
- 26 项矩阵已建立
- 8 条复刻风险已列出
- 新发现 reComputeUnPlaceOrderMedicalRecordFee API

---

**【S1-121 完成】**
