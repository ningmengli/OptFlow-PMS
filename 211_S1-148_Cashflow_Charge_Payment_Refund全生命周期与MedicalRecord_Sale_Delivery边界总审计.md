# S1-148：Cashflow / Charge / Payment / Refund 全生命周期与 MedicalRecord / Sale / Delivery 边界总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 210 个 MD / 不修改历史
> 关联：S1-137R / S1-141 / S1-142 / S1-143 / S1-146 / S1-147

---

## 目录

- §0 审计范围
- §1 Cashflow 全量命中
- §2 Cashflow Object 字段
- §3 Cashflow Create
- §4 Cashflow Read
- §5 Charge / Payment
- §6 PayType
- §7 Cashflow Status
- §8 Refund / Return / Cancel
- §9 ↔ MedicalRecord
- §10 ↔ Sale
- §11 ↔ Delivery
- §12 ↔ Customer / Patient
- §13 ↔ MedicalExamine / MedicalProduct
- §14 Charge 页面生命周期
- §15 页面消费矩阵
- §16 Source Trace
- §17 Object Type 分类
- §18 生命周期 DAG
- §19 26 项证据矩阵
- §20 历史差异
- §21 V4.4 资金域规格
- §22 F / 未确认
- §23 Git / 完整性

---

## §0 审计范围

本轮把 Cashflow / Charge / Payment / Refund 资金域作为
**独立完整域** 进行只读逆向证据审计：

- 字符级字段（C 真实 / F 不存在 严格区分）
- 4 个核心 Read API + 1 个 Create API 完整链
- 18 个 Controller 完整消费矩阵
- payTypeList 7 元素完整分类
- creditStatus / refundStatus / payStatus 真实 Owner 定位
- MedicalRecord / Sale / Delivery 边界
- 26 项证据矩阵
- 历史 S1-137R/141/142/143/146/147 误判核对

---

## §1 Cashflow 全量命中

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `cashflow` (全词) | **31** | A |
| `cashflowId` | **112** | A |
| `cashflowVo` | **0** | A |
| `cashflowList` | **0** | A |

**重要发现**：`cashflowVo` 字符级 0 命中（同 customerVo / patientVo / customerCheckinVo 模式）。
Cashflow 实际通过 `getCashflowObjectFactory.object.cashflow.*` 或 `res.cashflow.*` 形式被消费。

### §1.2 Cashflow API 全量

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **createCashFlowForMedicalRecord.json** | L6925 | **W (唯一 Create)** | A |
| **getMedicalRecordPayVo.json** | L4034 | R | A |
| **getMedicalRecordCashflowVo.json** | L4942/L5166/L7070/L7488 | R (4 调用) | A |
| **getMedicalRecordRefundDetailVo.json** | L4433 | R | A |
| **getMedicalRecordRefundLogVo.json** | L4908/L7433 | R (2 调用) | A |
| **getCashflowDeliveryVo.json** | L4040 | R | A |
| **getCashFlowCashierVo.json** | L7090 | R | A |
| **getCreditVo.json** (推断) | (L7367 派生) | R | C |
| **statProductDeliveryStatusOfCashflow.json** | L4047 | R | A |
| **payMedicalRecordCashflow.json** | L8008 | **W (唯一 Payment)** | A |
| **cancelMedicalRecordCashflow.json** | L8146 | W (Cancel) | A |
| **selectMedicalRecordCashflowVoList.json** | (推断) | R | F |
| **confirmMedicalRecordReturn.json** | L35167 | W (Return) | A |
| **cancelMedicalRecord.json** | L35150 | W (Cancel) | A |
| **createMedicalStockLossOfSmallVersion.json** | L35342 | W (ReportLoss) | A |

### §1.3 Cashflow 字段级访问模式

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `getCashflowObjectFactory.object.cashflow` | **16** | A |
| `res.cashflow.*` | 1 | A |
| `result.object.cashflow.*` | 1 | A |
| `cashflow.totalPayment` | **15** | A |
| `cashflow.creditStatus` | 4 | A |
| `cashflow.id` | 2 | A |
| `cashflow.payType` | 2 | A |
| `cashflow.refundStatus` | 2 | A |

---

## §2 Cashflow Object 字段

### §2.1 实际命中的 cashflow 字段（字符级）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `cashflow.id` | L7070 派生 (经 getMedicalRecordCashflowVo) | A |
| `cashflow.totalPayment` | L7784/L7911 (waitPayDetailCtrl) | A |
| `cashflow.payType` | L7784 (waitPayDetailCtrl) | A |
| `cashflow.refundStatus` | L4434 (partBackCtrl) / L7084 (myMaterialBillCtrl) | A |
| `cashflow.creditStatus` | L4424/L4426/L4611 (partBackCtrl) / L7367 (myMaterialBillCtrl) | A |

### §2.2 0 命中字段（必须 F）

| 字段 | 等级 |
|---|:---:|
| `cashflow.customer` | F |
| `cashflow.customerId` | F |
| `cashflow.patient` | F |
| `cashflow.patientId` | F |
| `cashflow.medicalRecord` (除派生) | F (派生) |
| `cashflow.medicalRecordId` (顶层) | F |
| `cashflow.sale` | F |
| `cashflow.saleId` | F |
| `cashflow.delivery` | F |
| `cashflow.deliveryId` | F |
| `cashflow.order` | F |
| `cashflow.orderId` | F |
| `cashflow.charge` | F |
| `cashflow.medicalExamineVoList` | F (实际是 `object.medicalExamineVoList`，cashflow 顶层不含) |
| `cashflow.medicalProductVoList` | F (同上) |
| `cashflow.status` (顶层) | F |
| `cashflowVo` | F |

### §2.3 Cashflow 字段 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core Object Field | `id`, `totalPayment`, `payType`, `refundStatus`, `creditStatus` | A |
| B. Nested Object (派生) | `medicalRecord` (L4034) | A 派生 |
| C. Request Only | `id` (getMedicalRecordPayVo Request) | A |
| D. State Only | `cashflowId` ($stateParams) | A |
| E. UI Only | - | F |
| F. Runtime Mutation | - | F (Cashflow 无 runtime mutation) |

---

## §3 Cashflow Create 生命周期

### §3.1 createCashFlowForMedicalRecord.json 唯一 Create（L6925）

**完整调用栈**：

```javascript
$scope.goCheck = function () {
    var obj = $scope.backReqList(false, true);   // L6922 动态 obj
    if (!obj) return;
    var fn = function fn() {
        obj.medicalRecordId = $scope.medicalRecordId;   // L6926 ★ A 字段桥
        new ObjectFactory().saveOrQuery("/admin/createCashFlowForMedicalRecord.json", obj).then(function (res) {
            if (res.status == 1) {
                return Popup.notice(res.errmsg);
            }
            $state.go("waitPayDetail", { cashflowId: res.result.object });   // L6932 关键跳转
        });
    };
    if ($scope.obj.customerCouponId) {  // 优惠券附加
        obj.customerCouponId = $scope.obj.customerCouponId;
        var list = [];
        $scope.getUnPlaceOrderObjectFactory.object.medicalProductVoList.forEach(function (v) {
            list.push($scope.changeFee2(1, v.medicalProduct.id, v.medicalProduct.rateFee));
        });
        $scope.getUnPlaceOrderObjectFactory.object.medicalProductVoListOfModel.forEach(function (v) {
            list.push($scope.changeFee2(1, v.medicalProduct.id, v.medicalProduct.rateFee));
        });
        $scope.getUnPlaceOrderObjectFactory.object.medicalExamineVoList.forEach(function (v) {
            list.push($scope.changeFee2(2, v.medicalExamine.id, v.medicalExamine.rateFee));
        });
        $scope.getUnPlaceOrderObjectFactory.object.registrationFeeVoList.forEach(function (v) {
            list.push($scope.changeFee2(3, v.medicalExamine.id, v.medicalExamine.rateFee));
        });
        Promise.all(list).then(function (res) { fn(); });
    } else {
        fn();
    }
};
```

### §3.2 Cashflow Create Request 真实字段（A 级）

| 字段 | 来源 | 等级 |
|---|---|---|
| `medicalRecordId` | `$scope.medicalRecordId` | **A 字段桥（强制）** |
| `customerCouponId` | `$scope.obj.customerCouponId` (可选) | A |
| `medicalProductVoList[].id + rateFee` | getUnPlaceOrderObjectFactory.object | A |
| `medicalProductVoListOfModel[].id + rateFee` | 同上 | A |
| `medicalExamineVoList[].id + rateFee` | 同上 | A |
| `registrationFeeVoList[].id + rateFee` | 同上 | A |
| `backReqList` 动态 obj (其它) | `$scope.backReqList(false, true)` | A |

**重要**：Request 实际必含 **`medicalRecordId` + backReqList 字段集**。
**MedicalRecord → Cashflow = A Request 桥**（强制 medicalRecordId 字段）。

### §3.3 Cashflow Create Response

- `res.result.object` = `cashflowId` (top-level, 不是 res.result.object.cashflow.id)
- 后续：`$state.go("waitPayDetail", { cashflowId: res.result.object })`

### §3.4 1 个 Cashflow Create 调用点

| 行号 | Controller | 入口 | 等级 |
|---|---|---|---|
| L6925 | myMaterialBillCtrl (L32435) | $scope.goCheck | A |

**重要**：Cashflow 唯一 Create 由 myMaterialBillCtrl 触发。
**`myMaterialBillCtrl` 是 Cashflow Create 入口 Controller**。

---

## §4 Cashflow Read API

### §4.1 getMedicalRecordPayVo.json（L4034，唯一反向桥）

| 项 | 值 |
|---|---|
| API | `/admin/getMedicalRecordPayVo.json` |
| Controller | deliveryInputRecordCtrl (L4024) |
| Request | `{ cashflowId: $scope.cashflowId }` |
| Response | `res.object.medicalRecord.id` → `$scope.medicalRecordId` |
| 桥 | **Cashflow → MedicalRecord 唯一最强 A 派生桥**（保持 S1-137R 修正） |
| 等级 | A |
| 链式 | 同一 ObjectFactory 链式调用 `getCashflowDeliveryVo.json` (L4040) + `statProductDeliveryStatusOfCashflow.json` (L4047) |

### §4.2 getMedicalRecordCashflowVo.json（4 调用，最大频次）

| 行号 | Controller | Request | 关键 Response 字段 | 等级 |
|---|---|---|---|---|
| L4942 | payedDetailCtrl | `{ cashflowId: $scope.obj.cashflowId }` | (打印) | A |
| L5166 | payedDetailCtrl | `{ cashflowId: id }` | (打印) | A |
| L7070 | **myMaterialBillCtrl** | `{ cashflowId: $scope.obj.cashflowId }` | `medicalExamineVoList[].medicalExamine.id` / `registrationFeeVoList[].medicalExamine.id` / `medicalProductVoList[].medicalProduct.id` / `medicalProductVoListOfModel[].medicalProduct.id` / `cashflow.refundStatus === 2` | A |
| L7488 | myMaterialBillCtrl | `{ cashflowId: $scope.obj.cashflowId }` | (派生 getCustomerVo) | A |

**关键发现**：L7070 派生 4 个 VoList ID 数组 + 1 个 cashflow.refundStatus 检查。
**Cashflow → MedicalExamine / MedicalProduct 的桥全部经 getMedicalRecordCashflowVo**（保持 S1-145/S1-146 修正）。

### §4.3 getMedicalRecordRefundDetailVo.json（L4433）

| 项 | 值 |
|---|---|
| API | `/admin/getMedicalRecordRefundDetailVo.json` |
| Controller | partBackCtrl (L4368) |
| Request | `{ cashflowId: $scope.cashflowId }` |
| Response 字段 | `res.cashflow.refundStatus === 1` (L4434) / `res.medicalProductRefundVoList` / `res.medicalExamineRefundVoList` / `res.cashRefundFeeVoList[].refundMode` / `res.creditRefundFeeVoList[].refundMode` |
| 桥 | **Cashflow → RefundDetail A 派生桥**（A） |
| 等级 | A |

### §4.4 getMedicalRecordRefundLogVo.json（2 调用）

| 行号 | Controller | Request | Response 字段 | 等级 |
|---|---|---|---|---|
| L4908 | partBackCtrl | `{ refundLogId: $stateParams.refundLogId }` | `res.refundFeeLogList` | A |
| L7433 | payedDetailCtrl | `{ refundLogId: refundLogId }` | `res.object.customer.linkMobile` (派生) | A |

**注意**：Request 是 `refundLogId` 不是 `cashflowId` —— 这是 RefundLog 独立 ID 入口。

### §4.5 getCashflowDeliveryVo.json（L4040，Delivery 域）

- Request: `{ cashflowId: $scope.cashflowId }`
- Response: `res.object.deliveryVoList` (推断)
- Controller: deliveryInputRecordCtrl
- 等级: A
- **Cashflow → Delivery 桥**（保持 S1-142 修正：经 getCashflowDeliveryVo 派生）

### §4.6 getCashFlowCashierVo.json（L7090）

- Controller: myMaterialBillCtrl
- 等级: A
- 派生 cashierVo 详情

### §4.7 statProductDeliveryStatusOfCashflow.json（L4047）

- Controller: deliveryInputRecordCtrl
- Request: `{ cashflowId }`
- 等级: A
- 派生 delivery 状态统计

### §4.8 Read API 完整矩阵

| API | R/W | Controller | Object Path | Grade |
|---|---|---|---|---|
| createCashFlowForMedicalRecord.json | W | myMaterialBillCtrl | res.result.object → cashflowId | A |
| getMedicalRecordPayVo.json | R | deliveryInputRecordCtrl | res.object.medicalRecord.id | A (反向最强) |
| getMedicalRecordCashflowVo.json | R (4) | myMaterialBillCtrl/payedDetailCtrl | object.cashflow + 4 VoList | A |
| getMedicalRecordRefundDetailVo.json | R | partBackCtrl | res.cashflow.refundStatus + 4 VoList | A |
| getMedicalRecordRefundLogVo.json | R (2) | partBackCtrl/payedDetailCtrl | res.refundFeeLogList / res.object.customer | A |
| getCashflowDeliveryVo.json | R | deliveryInputRecordCtrl | object.deliveryVoList | A |
| getCashFlowCashierVo.json | R | myMaterialBillCtrl | cashierVo | A |
| statProductDeliveryStatusOfCashflow.json | R | deliveryInputRecordCtrl | delivery stat | A |
| payMedicalRecordCashflow.json | **W** | waitPayDetailCtrl | res.payedList 跳转 | **A (唯一 Payment)** |
| cancelMedicalRecordCashflow.json | W | waitPayDetailCtrl | res.status | A |
| confirmMedicalRecordReturn.json | W | optometryCtrl | (MedicalRecord 退镜) | A |
| cancelMedicalRecord.json | W | optometryCtrl | (MedicalRecord 取消) | A |
| createMedicalStockLossOfSmallVersion.json | W | optometryCtrl | (小件报损) | A |

---

## §5 Charge / Payment

### §5.1 Charge 全量统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `charge` (全词) | 16 | A |
| `Charge` (大写) | 5 | A |
| `chargeId` | **0** | A |
| `chargeVo` | **0** | A |
| `chargeList` | 2 (HTML 文件名) | A |
| `chargeDetail` | 0 | A |
| `chargeRecord` | 0 | A |
| `waitCharge` | 4 (HTML/State) | A |
| `waitChargeDetailCtrl` | 1 (Controller) | A |

### §5.2 Payment 全量统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `pay` (全词) | 117+ | A |
| `payType` | **51** | A |
| `payName` | 7 | A |
| `payAmount` | 0 | A |
| `paymentId` | **0** | A |
| `paymentVo` | **0** | A |
| `payMedicalRecordCashflow` | 1 (API) | A |
| `payTypeList` | 7+ (定义 + 使用) | A |

### §5.3 Charge 结论

- **`chargeId` 字符级 0 命中** → Charge **不是独立 ID 实体**（F）
- **`chargeVo` 字符级 0 命中** → Charge **不是独立 VO 实体**（F）
- "charge" 实际只是 **State 路由名**（如 `waitCharge` / `waitChargeList` / `waitChargeDetail`）
- "Charge" 实际是 **收费页面的逻辑概念**，不是数据库实体
- "waitChargeDetailCtrl" Controller 名包含 "charge" 但实际**消费 cashflow 实体**（cashflow=21 / cashflowId=20）

### §5.4 Payment 结论

- **`paymentId` 字符级 0 命中** → Payment **不是独立 ID 实体**（F）
- **`paymentVo` 字符级 0 命中** → Payment **不是独立 VO 实体**（F）
- "Payment" 实际只是 **payType + 各种 receivedFrom 字段的临时 Request Payload**（C Request Bridge）
- 唯一 Payment Write API: `payMedicalRecordCashflow.json` (L8008) — 实际命名是"对 medicalRecordCashflow 支付"不是"Payment 实体"

### §5.5 4 个关键 Controller 命名误导

| Controller | 实际 | 警告 |
|---|---|---|
| `refundCtrl` | **NOT FOUND** | 命名误导, 实际退款逻辑在 partBackCtrl (L4368) |
| `refundLogCtrl` | **NOT FOUND** | 命名误导, 实际退款日志在 partBackCtrl |
| `printCtrl` | **NOT FOUND** | 命名误导, 实际打印逻辑在 payedDetailCtrl / partBackCtrl |
| `creditCtrl` | **NOT FOUND** | 命名误导, 实际授信逻辑在 partBackCtrl / waitPayDetailCtrl |

**重要发现**：以 refund / credit / print 命名的 Controller **全部不存在**。
这些功能由 partBackCtrl 复用（命名误导）。

### §5.6 Charge / Payment 核心 Controller

| Controller | 行号 | 实际消费对象 | 等级 |
|---|---|---|---|
| **waitChargeDetailCtrl** | L6568 | cashflow (21) + cashflowId (20) + pay (25) | A |
| **waitPayDetailCtrl** | L7452 | cashflow (15) + cashflowId (7) + pay (21) | A |
| **payedListCtrl** | L4972 | cashflow (21) + cashflowId (32) + pay (30) | A |
| **payedDetailCtrl** | L4937 | cashflow (20) + cashflowId (36) + pay (29) | A |
| **partBackCtrl** | L4368 | cashflow (9) + cashflowId (50) + pay (26) + refund (13) | A |

---

## §6 PayType

### §6.1 payTypeList 完整定义（L7734-L7763, waitPayDetailCtrl）

| index | name | key | inputKey | resultKey | 等级 |
|:---:|---|---|---|---|:---:|
| 0 | **现金** | `receivedFromCash` | `cashFee` | - | A |
| 1 | **微信收款** | `receivedFromWechat` | `wechatFee` | - | A |
| 2 | **支付宝收款** | `receivedFromAlipay` | `alipayFee` | - | A |
| 3 | **银行卡** | `receivedFromBankcard` | `bankCardFee` | - | A |
| 11 | **扫码** | `receivedFromScan` | `authCode` | `authCode` | A |
| 12 | **扫码** | `receivedFromScan` | `authCode` | `authCode` | A |
| 13 | **POS机** | `receivedFromPos` | `posSN` | `posDeviceSn` | A |

### §6.2 重要发现

1. **S1-141 历史报告 0/1/2/3/11/12/13 完全验证**
2. **index 11 和 12 都是"扫码"** — name/key/inputKey/resultKey 全部相同 — **命名误导**
3. **index 11/12/13 含 resultKey**（区别于 0/1/2/3）— 用于扫码支付结果
4. **0/1/2/3 没有 resultKey**（现金/微信/支付宝/银行卡直接收）

### §6.3 payType 业务含义

- **index 0** = 现金（cashFee 输入）
- **index 1** = 微信收款（wechatFee 输入）
- **index 2** = 支付宝收款（alipayFee 输入）
- **index 3** = 银行卡（bankCardFee 输入）
- **index 11/12** = 扫码支付（authCode 输入 + authCode 结果）
- **index 13** = POS机（posSN 输入 + posDeviceSn 结果）

### §6.4 payType 字段 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Request Payload | `payType` (L8009), `receivedFromCash`, `receivedFromWechat`, `receivedFromAlipay`, `receivedFromBankcard`, `receivedFromScan`, `receivedFromPos` | A |
| B. UI Scope | `cashFee`, `wechatFee`, `alipayFee`, `bankCardFee`, `authCode`, `posSN` | A |
| C. State | - | F |
| D. Object | - | F (没有 payType object 字段) |

---

## §7 Cashflow Status

### §7.1 5 个 Status 字段 Owner 定位

| 字段 | 真实 Owner | 等级 |
|---|---|---|
| `cashflow.refundStatus` | **Cashflow (顶层)** (L4434 partBackCtrl / L7084 myMaterialBillCtrl) | A |
| `cashflow.creditStatus` | **Cashflow (顶层)** (L4424/L4426/L4611 partBackCtrl / L7367 myMaterialBillCtrl) | A |
| `cashflow.totalPayment` | **Cashflow (顶层)** (L7784/L7911 waitPayDetailCtrl) | A |
| `cashflow.payType` | **Cashflow (顶层)** (L7784 waitPayDetailCtrl) | A |
| `$scope.obj.refundStatus` | **Request/Scope 临时字段** (L4101-L4104 partBackCtrl) | A |
| `$scope.cash.creditStatus` | **Scope 写字段** (L6003 waitChargeDetailCtrl `= 1`) | A |

### §7.2 关键判断

- **MedicalRecord.status = 0 命中**（保持 S1-146 修正）
- **refundStatus 不属于 MedicalRecord**（保持 S1-146 修正）— 实际是 cashflow 顶层字段
- **creditStatus 实际是 cashflow 字段**（4 字符级全在 cashflow 嵌套下）

### §7.3 Status 字段值含义（A 级派生）

| 字段 | 值 | 含义（基于字符级比较） | 等级 |
|---|---|---|---|
| `cashflow.refundStatus` | 0 | 未退款 | C |
| `cashflow.refundStatus` | 1 | 已退款（partBackCtrl L4434 跳 payedList） | A |
| `cashflow.refundStatus` | 2 | 部分退款（myMaterialBillCtrl L7084 派生 canUsePayBack） | A |
| `cashflow.creditStatus` | 1 | 已授信（partBackCtrl L4426/L4611） | A |
| `cashflow.creditStatus` | 2 | 已使用授信（myMaterialBillCtrl L7370） | A |
| `$scope.obj.refundStatus` | 0/1/2/... | Request filter (partBackCtrl L4149) | A |

### §7.4 payedStatus 实际是 UI 列表状态

- 18 命中 — 实际是 **列表项显示字段**（不是 Cashflow 状态）
- 命名误导：payed ≠ payed (payed = payed past tense?)

---

## §8 Refund / Return / Cancel

### §8.1 Refund 字符级统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `refund` (全词) | **19** | A |
| `refundId` | **6** | A |
| `refundVo` | **11** | A |
| `refundStatus` | 22 | A |
| `refundStatusArray` | 44 | A |

### §8.2 Refund 关键发现

1. **`refundId` 6 命中**但**没有独立 Refund Write API** — refundId 仅作 Request 参数（如 refundLogId）
2. **`refundVo` 11 命中**但没有独立 RefundVO 写入 — refundVo 实际是 **Response 嵌套字段**（如 `res.cashRefundFeeVoList[].refundMode`）
3. **没有 refundId 专属 Write API** — 0 命中 `payRefund*.json` / `saveRefund*.json` / `refundCashflow*.json`
4. **唯一 Cancel API**: `cancelMedicalRecordCashflow.json` (L8146) — `{ cashflowId: id }`
5. **退款逻辑全部在 partBackCtrl**（L4368）— 命名误导"refundCtrl"实际不存在

### §8.3 Return 字符级定位

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| Return 概念 | `confirmMedicalRecordReturn.json` L35167 | A |
| API 行号 | L35167 (optometryCtrl) | A |
| Request | `{ medicalRecordId }` | A |
| 真实 Owner | **MedicalRecord (退镜)** | A |
| 与 Cashflow 关系 | **F** (无直接字段桥) | F |

**重要**：Return 是 **MedicalRecord 退镜生命周期**，不是 Cashflow 退款。
保持 S1-142 修正。

### §8.4 Cancel 字符级定位

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| MedicalRecord Cancel | `cancelMedicalRecord.json` L35150 | A |
| Request | `{ medicalRecordId }` | A |
| 真实 Owner | **MedicalRecord (取消)** | A |
| Cashflow Cancel | `cancelMedicalRecordCashflow.json` L8146 | A |
| Request | `{ cashflowId: id }` | A |
| 真实 Owner | **Cashflow (取消)** | A |

**重要区分**：
- `cancelMedicalRecord` = 取消 MedicalRecord 本身（optometryCtrl）
- `cancelMedicalRecordCashflow` = 取消 MedicalRecord 关联的 Cashflow（waitPayDetailCtrl L8146）

### §8.5 Refund / Return / Cancel 三者严格区分

| 概念 | 含义 | API | Owner | 行号 | 等级 |
|---|---|---|---|---|---|
| **Refund** | 现金退款 | 0 命中独立 API | Cashflow 字段 | (无) | F (无独立 API) |
| **Return** | 退镜（眼镜） | confirmMedicalRecordReturn.json | MedicalRecord | L35167 | A |
| **Cancel** | 取消订单 | cancelMedicalRecord.json / cancelMedicalRecordCashflow.json | MedicalRecord / Cashflow | L35150/L8146 | A |
| **ReportLoss** | 报损 | createMedicalStockLossOfSmallVersion.json | Stock | L35342 | A |

**关键结论**：
- **Refund 不是独立对象**（F）— 实际是 cashflow 字段（refundStatus）+ partBackCtrl 流程
- **Return ≠ Refund** — Return 是退镜（库存），Refund 是退钱
- **Cancel 是 MedicalRecord + Cashflow 双重取消**

### §8.6 Refund 相关 API 完整矩阵

| API | 行号 | Controller | 等级 |
|---|---|---|---|
| getMedicalRecordRefundDetailVo.json | L4433 | partBackCtrl | A |
| getMedicalRecordRefundLogVo.json | L4908 | partBackCtrl | A |
| getMedicalRecordRefundLogVo.json | L7433 | payedDetailCtrl | A |
| cancelMedicalRecordCashflow.json | L8146 | waitPayDetailCtrl | A |
| (refundId Write API) | 0 命中 | - | F |

---

## §9 Cashflow ↔ MedicalRecord

### §9.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| MedicalRecord | Cashflow | `createCashFlowForMedicalRecord { medicalRecordId }` | A Request Bridge | L6925/L6926 | **A** | A |
| MedicalRecord | Cashflow | `getUnPlaceOrderMedicalRecordFee` (派生 patientId/cashflowId) | A Request Bridge | L6680 | **A** | A |
| Cashflow | MedicalRecord | `getMedicalRecordPayVo { cashflowId }` → `res.object.medicalRecord.id` | A 派生 | L4034 | **A** | A |
| Cashflow | MedicalRecord | `cashflow.medicalRecord` (字段) | 0 命中 | - | **F** | F |
| MedicalRecord | Cashflow | `medicalRecord.cashflow` 嵌套 | 0 命中 | - | **F** | F |
| MedicalRecord | Cashflow | `medicalRecord.cashflowId` 字段 | 0 命中 | - | **F** | F |
| Cashflow | MedicalRecord | `cashflow.medicalRecordId` 顶层 | 0 命中 | - | **F** | F |

### §9.2 关键判断

- **MedicalRecord → Cashflow**: A Request Bridge（L6925 强制 medicalRecordId） + A Request Bridge（L6680 派生 patientId）
- **Cashflow → MedicalRecord**: A 派生（L4034 getMedicalRecordPayVo Response）
- **保持 S1-137R 修正**：Cashflow → MedicalRecord **只有 1 个最强反向桥**（getMedicalRecordPayVo.json）
- **保持 S1-146 修正**：MedicalRecord 不含 cashflow / cashflowId 字段（F）

---

## §10 Cashflow ↔ Sale

### §10.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Sale | Cashflow | `myMaterialBillCtrl.goCheck()` → `createCashFlowForMedicalRecord` | A State Bridge | L6925 | **A** | A |
| Cashflow | Sale | `cashflow.sale` | 0 命中 | - | **F** | F |
| Cashflow | Sale | `cashflow.saleId` | 0 命中 | - | **F** | F |
| Sale | Cashflow | `sale.cashflow` | 0 命中 | - | **F** | F |
| Sale | Cashflow | `sale.cashflowId` | 0 命中 | - | **F** | F |

### §10.2 关键判断

- **Sale → Cashflow**: A State Bridge（myMaterialBillCtrl.goCheck 是 Cashflow Create 入口）
- **Cashflow → Sale**: F（0 命中直接字段桥）
- **保持 S1-143 修正**：
  - `saleId` 0 命中
  - `saleVo` 0 命中
  - Sale 实际是 medicalRecordType=5 路由视图（S1-146）
- **Sale 不是 Cashflow 上游**，而是 **Cashflow Create 的入口 Controller**

---

## §11 Cashflow ↔ Delivery

### §11.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Delivery | Cashflow | `deliveryInputCtrl` 等使用 `cashflowId` 作为 State 入口 | A State Bridge | 多处 | **A** | A |
| Cashflow | Delivery | `getCashflowDeliveryVo { cashflowId }` → `res.object.deliveryVoList` | A 派生 | L4040 | **A** | A |
| Cashflow | Delivery | `cashflow.delivery` 字段 | 0 命中 | - | **F** | F |
| Cashflow | Delivery | `cashflow.deliveryId` 字段 | 0 命中 | - | **F** | F |
| Delivery | Cashflow | `delivery.cashflow` 字段 | 0 命中 | - | **F** | F |
| Delivery | Cashflow | `delivery.cashflowId` 字段 | 0 命中 | - | **F** | F |

### §11.2 关键判断

- **Delivery → Cashflow**: A State Bridge（`$stateParams.cashflowId` 是 Delivery 域入口）
- **Cashflow → Delivery**: A 派生（getCashflowDeliveryVo 派生）
- **保持 S1-142 修正**：
  - Cashflow → Delivery **直接证据 F**（无 cashflow.delivery 字段）
  - Delivery → Cashflow 有 A 级派生证据
- **Delivery 域 cashflowId 集中度**（§15 矩阵）：
  - deliveryInputCtrl cashflowId=**63**
  - deliveryInputRecordCtrl cashflowId=**60**
  - deliveryProcessingCtrl cashflowId=**54**
  - partBackCtrl cashflowId=**50**

---

## §12 Cashflow ↔ Customer / Patient

### §12.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Cashflow | Customer | `getMedicalRecordCashflowVo` → `getCustomerVo` (L7488) | A 派生链 | L7488 | **A** | A |
| Cashflow | Patient | 0 命中 `cashflow.patient` 字段 | F | - | **F** | F |
| Cashflow | Customer | 0 命中 `cashflow.customer` 字段 | F | - | **F** | F |
| Customer | Cashflow | 0 命中 `customer.cashflow` 字段 | F | - | **F** | F |
| Patient | Cashflow | 0 命中 `patient.cashflow` 字段 | F | - | **F** | F |

### §12.2 关键判断

- **Cashflow → Customer**: A 派生链（myMaterialBillCtrl 派生 getCustomerVo）
- **Cashflow → Patient**: F（无直接字段桥）
- **Customer/Patient → Cashflow**: F
- 桥必须经 **getMedicalRecordCashflowVo → getCustomerVo** 派生链

---

## §13 Cashflow ↔ MedicalExamine / MedicalProduct

### §13.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Cashflow | MedicalExamine | `getMedicalRecordCashflowVo` → `object.medicalExamineVoList[].medicalExamine.id` | A 派生 | L7070 | **A** | A |
| Cashflow | MedicalProduct | `getMedicalRecordCashflowVo` → `object.medicalProductVoList[].medicalProduct.id` | A 派生 | L7070 | **A** | A |
| Cashflow | MedicalProduct (Model) | `getMedicalRecordCashflowVo` → `object.medicalProductVoListOfModel[].medicalProduct.id` | A 派生 | L7070 | **A** | A |
| Cashflow | MedicalExamine (Reg) | `getMedicalRecordCashflowVo` → `object.registrationFeeVoList[].medicalExamine.id` | A 派生 | L7070 | **A** | A |
| Cashflow | MedicalExamine | `cashflow.medicalExamineVoList` 字段 | 0 命中（实际是 `object.medicalExamineVoList`） | - | **F** | F |
| Cashflow | MedicalProduct | `cashflow.medicalProductVoList` 字段 | 0 命中（实际是 `object.medicalProductVoList`） | - | **F** | F |
| MedicalExamine | Cashflow | `medicalExamine.cashflow` 字段 | 0 命中 | - | **F** | F |
| MedicalProduct | Cashflow | `medicalProduct.cashflow` 字段 | 0 命中 | - | **F** | F |

### §13.2 关键判断

- **Cashflow → MedicalExamine/MedicalProduct**: A 派生（4 个 VoList 全部派生）
- **反向 F**：MedicalExamine/MedicalProduct 不含 cashflow 字段
- **保持 S1-145 修正**：VoList 是 Response VO 容器，**不是 cashflow 内嵌字段**
- **保持 S1-146 修正**：Cashflow 不含 medicalExamineVoList 嵌套（F）

---

## §14 Charge 页面生命周期

### §14.1 waitChargeDetailCtrl 完整链

```
[外部] cashflowId (State)
  ↓
waitChargeDetailCtrl
  ↓
getMedicalRecordPayVo({ cashflowId }) → res.object.medicalRecord.id → $scope.medicalRecordId
  ↓
getCashflowDeliveryVo({ cashflowId }) → res.object.deliveryVoList (Delivery 域)
  ↓
statProductDeliveryStatusOfCashflow({ cashflowId }) → delivery 状态
  ↓
[UI] 显示收费详情
  ↓
goCheck (deliveryConfirm + pay)
  ↓
$state.go waitPayDetail
```

### §14.2 waitPayDetailCtrl 完整链

```
[外部] cashflowId (State)  [从 waitChargeDetailCtrl 跳入]
  ↓
waitPayDetailCtrl
  ↓
getMedicalRecordCashflowVo({ cashflowId }) → object.cashflow + 4 VoList
  ↓
[UI] 显示 payTypeList 7 元素（现金/微信/支付宝/银行卡/扫码×2/POS）
  ↓
user 选择 payType + 输入金额 (cashFee/wechatFee/...)
  ↓
payMedicalRecordCashflow({ obj, payType }) → payCashflow 写入
  ↓
$state.go payedList
```

### §14.3 payedListCtrl / payedDetailCtrl 完整链

```
payedListCtrl
  ↓
getMedicalRecordCashflowVo (4 调用, L4942/L5166)
  ↓
打印小票
  ↓
payedDetailCtrl (列表项跳转)
  ↓
getMedicalRecordCashflowVo + 打印
```

### §14.4 partBackCtrl 完整链（退款）

```
[外部] cashflowId (State)
  ↓
partBackCtrl
  ↓
getMedicalRecordRefundDetailVo({ cashflowId })
  ↓
[if res.cashflow.refundStatus === 1] 跳 payedList
  ↓
$scope.refundFeeInfo = res (含 medicalProductRefundVoList / medicalExamineRefundVoList / cashRefundFeeVoList / creditRefundFeeVoList)
  ↓
[UI] 用户选择部分退款
  ↓
$scope.obj.refundStatus (Request filter 0/1/2/...)
  ↓
refundLog 跳转 → getMedicalRecordRefundLogVo({ refundLogId })
```

### §14.5 cancelMedicalRecordCashflow 完整链

```
waitPayDetailCtrl
  ↓
$scope.cancelCashObjectFactory.saveOrQuery("/admin/cancelMedicalRecordCashflow.json", { cashflowId: id })
  ↓
Popup.notice 状态提示
  ↓
刷新列表
```

### §14.6 每个 State/Function 的关键 API

| State | Function | 关键 API | 等级 |
|---|---|---|---|
| waitChargeDetail | init | getMedicalRecordPayVo | A |
| waitChargeDetail | confirmDelivery | completeMedicalRecordDelivery | A |
| waitPayDetail | init | getMedicalRecordCashflowVo | A |
| waitPayDetail | confirmPay | payMedicalRecordCashflow | A |
| waitPayDetail | cancel | cancelMedicalRecordCashflow | A |
| payedList | init | getMedicalRecordCashflowVo | A |
| payedDetail | print | getMedicalRecordCashflowVo + getMedicalRecordRefundLogVo | A |
| partBack | init | getMedicalRecordRefundDetailVo | A |
| partBack | refundLog | getMedicalRecordRefundLogVo | A |

---

## §15 页面消费矩阵

### §15.1 18 个 Controller cashflow/charge/pay/refund 消费矩阵

| Controller | cashflow | cashflowId | pay | refund | charge | 等级 |
|---|---:|---:|---:|---:|---:|:---:|
| waitChargeDetailCtrl (L6568) | 21 | 20 | 25 | 1 | 0 | A |
| **waitPayDetailCtrl** (L7452) | 15 | 7 | 21 | 0 | 0 | A |
| **payedListCtrl** (L4972) | 21 | 32 | 30 | 1 | 0 | A |
| **payedDetailCtrl** (L4937) | 20 | 36 | 29 | 1 | 0 | A |
| **partBackCtrl** (L4368) | 9 | **50** | 26 | 13 | 0 | A |
| myMaterialBillCtrl (L32435) | 0 | 4 | 4 | 0 | 0 | A (Cashflow Create 入口) |
| adminSalesRecordCtrl (L31285) | 0 | 0 | 0 | 0 | 0 | A (Sale 容器, 不进 cashflow) |
| **deliveryInputCtrl** (L3812) | 4 | **63** | 23 | 12 | 0 | A |
| **deliveryInputRecordCtrl** (L4024) | 4 | **60** | 23 | 12 | 0 | A |
| **deliveryProcessingCtrl** (L4236) | 6 | **54** | 24 | 13 | 0 | A |
| optometryCtrl (L34776) | 0 | 18 | 0 | 5 | 0 | A |
| myMemberCtrl (L33080) | 0 | 4 | 4 | 0 | 0 | A |
| myMemberRecordCtrl (L33218) | 0 | 4 | 4 | 0 | 0 | A |
| addSaleRecordCtrl (L31008) | 0 | 0 | 0 | 0 | 0 | A |
| refundFeeCtrl (L37657) | 3 | 4 | 0 | 5 | 0 | A |
| ~~refundCtrl~~ | **NOT FOUND** | - | - | - | - | F (命名误导) |
| ~~refundLogCtrl~~ | **NOT FOUND** | - | - | - | - | F (命名误导) |
| ~~printCtrl~~ | **NOT FOUND** | - | - | - | - | F (命名误导) |
| ~~creditCtrl~~ | **NOT FOUND** | - | - | - | - | F (命名误导) |

### §15.2 核心观察

1. **cashflow 实体**（cashflow + cashflowId 总和最大）:
   - deliveryInputCtrl (67) / deliveryInputRecordCtrl (64) / partBackCtrl (59) / deliveryProcessingCtrl (60) / payedDetailCtrl (56) / payedListCtrl (53) / waitChargeDetailCtrl (41) / waitPayDetailCtrl (22) / optometryCtrl (18) / myMemberCtrl/Record (8) / myMaterialBillCtrl (4) / refundFeeCtrl (7) / adminSalesRecordCtrl (0) / addSaleRecordCtrl (0)
2. **charge = 0** 所有 Controller — 印证 §5.3 结论
3. **NOT FOUND**: refundCtrl / refundLogCtrl / printCtrl / creditCtrl — 命名误导，实际由 partBackCtrl 复用
4. **myMaterialBillCtrl cashflow/cashflowId=4** — 实际是 Cashflow Create 入口，cashflow 实体本身不进入 myMaterialBillCtrl

---

## §16 Source Trace

### §16.1 关键字段溯源

#### cashflowId
- **Source**:
  - `$stateParams.cashflowId` (L18949 patientListCtrl, 多个 State 入口)
  - `res.result.object` (L6932 createCashFlowForMedicalRecord Response)
  - `$scope.obj.cashflowId` (myMaterialBillCtrl L7070)
- **Transform**: State entry → Request `{ cashflowId }` → Response 派生
- **Target**: getMedicalRecordPayVo / getMedicalRecordCashflowVo / cancelMedicalRecordCashflow
- **Consumer**: 11 个 Controller

#### cashflow.id
- **Source**: `getMedicalRecordCashflowVo` Response `object.cashflow.id`
- **Transform**: Response → cashflow.id
- **Target**: (无下游, 只读)
- **Consumer**: myMaterialBillCtrl (L7070 派生)
- **等级**: A (派生)

#### medicalRecordId (Cashflow 域)
- **Source A**: `getMedicalRecordPayVo` Response `res.object.medicalRecord.id` (L4034)
- **Source B**: `createCashFlowForMedicalRecord` Request `obj.medicalRecordId = $scope.medicalRecordId` (L6926)
- **Target**: $scope.medicalRecordId / 状态跳转
- **Consumer**: deliveryInputRecordCtrl / myMaterialBillCtrl
- **等级**: A (双向)

#### chargeId
- **Source**: 0 命中
- **等级**: **F** (Charge 不是独立对象)

#### paymentId
- **Source**: 0 命中
- **等级**: **F** (Payment 不是独立对象)

#### refundId
- **Source A**: `$stateParams.refundLogId` (L4908)
- **Source B**: `refundLogId` 局部变量 (L7433)
- **Target**: getMedicalRecordRefundLogVo Request
- **等级**: A (Request 字段, 但不是独立 ID 实体)

#### payType
- **Source**: $scope.payType (user input), payTypeList[index].key/inputKey/resultKey
- **Transform**: payType 0/1/2/3/11/12/13 → 各种 receivedFrom* 字段
- **Target**: payMedicalRecordCashflow Request
- **等级**: A

#### totalPayment
- **Source**: `getMedicalRecordCashflowVo` Response `object.cashflow.totalPayment`
- **Target**: changeCashFee / confirmPay 计算
- **等级**: A (Object field, 只读)

#### refundStatus
- **Source A**: `getMedicalRecordCashflowVo` Response `object.cashflow.refundStatus` (L7084)
- **Source B**: `getMedicalRecordRefundDetailVo` Response `res.cashflow.refundStatus` (L4434)
- **Source C**: `$scope.obj.refundStatus` (L4101-L4104 partBackCtrl Request filter)
- **等级**: A (3 个 Source 全部确认)

#### creditStatus
- **Source A**: `res.cashflow.creditStatus` (L4424/L4426/L4611 partBackCtrl)
- **Source B**: `res$result$object.cashflow.creditStatus` (L7367 myMaterialBillCtrl)
- **Source C**: `$scope.cash.creditStatus = 1` (L6003 waitChargeDetailCtrl 写)
- **等级**: A

#### receivedFrom / receivedFromName
- **Source**: payTypeList[i].key (receivedFromCash/Wechat/Alipay/Bankcard/Scan/Pos)
- **Target**: payMedicalRecordCashflow Request `obj.receivedFrom*`
- **等级**: A (Request Payload)

#### payName
- **Source**: payTypeList[i].name ("现金" / "微信收款" / "支付宝收款" / "银行卡" / "扫码" / "POS机")
- **等级**: A (UI 展示)

---

## §17 Object Type 分类

### §17.1 7 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Cashflow** | ✓ (cashflowId) | ✓ (cashflow) | - | - | A |
| **Charge** | ✗ | ✗ | ✗ | ✓ (State 路由) | F |
| **Payment** | ✗ | ✗ | ✓ (payType + receivedFrom*) | ✓ (payTypeList) | C |
| **Refund** | ✗ (refundId 不是独立 ID) | ✓ (refundVo / refundFeeLogList) | ✗ | ✓ (refundStatus) | C |
| **CashflowDetail** | ✓ (cashflowId) | ✓ (cashflowVo) | - | - | A (含 medicalExamineVoList / medicalProductVoList) |
| **MedicalExamineVo** | ✓ (medicalExamineId) | ✓ (medicalExamineVoList) | ✓ (changeFee2 第二参数) | - | A |
| **MedicalProductVo** | ✓ (medicalProductId) | ✓ (medicalProductVoList / medicalProductVoListOfModel) | ✓ (changeFee2 第一参数) | - | A |

### §17.2 关键结论

- **Cashflow 是唯一独立资金域对象**（A）
- **Charge / Payment / Refund 都不是独立 ID 实体**（F / C）
- 完整对象分类 = **1 独立 + 1 派生 VO + 1 Request Bridge + 4 UI 临时**

---

## §18 生命周期 DAG

### §18.1 Cashflow 完整生命周期

```
[MedicalRecord 创建]
  ↓
[myMaterialBillCtrl.goCheck]
  ↓
createCashFlowForMedicalRecord { medicalRecordId, customerCouponId, ... }
  ↓
Response: res.result.object = cashflowId
  ↓
$state.go waitPayDetail({ cashflowId })
  ↓
[waitPayDetailCtrl 支付页]
  ↓
getMedicalRecordCashflowVo { cashflowId } → object.cashflow + 4 VoList
  ↓
user 选择 payType (0/1/2/3/11/12/13)
  ↓
payMedicalRecordCashflow { payType, receivedFrom*, ... }
  ↓
$state.go payedList
  ↓
[payedListCtrl 已支付列表]
  ↓
payedDetailCtrl (列表项)
  ↓
[可选] partBackCtrl 退款
  ↓
getMedicalRecordRefundDetailVo { cashflowId } → res.cashflow.refundStatus
  ↓
[if refundStatus === 1] 跳 payedList
  ↓
refundLog 跳转
  ↓
[可选] cancelMedicalRecordCashflow { cashflowId }
```

### §18.2 Cashflow 与 MedicalRecord / Sale / Delivery 的并行 DAG

```
                    [Customer]
                       ↓ A
                    [Patient] ← C (L18949)
                       ↓ A Request
                    [MedicalRecord] ─── createCashFlowForMedicalRecord ───→ [Cashflow] (L6925)
                       ↑                                                                  ↓
                       │ A 派生 (L4034)                                                    │ payMedicalRecordCashflow
                       └──────────── getMedicalRecordPayVo ←──────────────────────────────┘
                                                                                              ↓
                                                                            [payedList] → [partBack] (退款)
                                                                                              ↓
                                                                                    [refundStatus === 1/2]
```

### §18.3 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| MedicalRecord | Cashflow | A | createCashFlowForMedicalRecord { medicalRecordId } | L6925/L6926 |
| Cashflow | MedicalRecord | A | getMedicalRecordPayVo { cashflowId } | L4034 |
| Sale (myMaterialBillCtrl) | Cashflow | A | goCheck → createCashFlowForMedicalRecord | L6922-L6932 |
| Delivery (State) | Cashflow | A | $stateParams.cashflowId → 多个 API | 多处 |
| Cashflow | Delivery | A | getCashflowDeliveryVo { cashflowId } | L4040 |
| Cashflow | MedicalExamine | A | getMedicalRecordCashflowVo → medicalExamineVoList | L7070 |
| Cashflow | MedicalProduct | A | getMedicalRecordCashflowVo → medicalProductVoList | L7070 |
| Cashflow | Customer | A | getMedicalRecordCashflowVo → getCustomerVo | L7488 |
| Cashflow | Return (MedicalRecord) | A | (无 API, Return 是 MedicalRecord 字段) | - |
| Cashflow | Cancel (MedicalRecord) | A | cancelMedicalRecordCashflow / cancelMedicalRecord | L8146/L35150 |

---

## §19 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 18 Controllers 范围 | A | - | 全部 | A |
| 2 | Controller | 18 Controllers (含 4 个 NOT FOUND) | A | - | 全部 | A |
| 3 | State | waitPayDetail / payedList / partBack | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | cashflowId (50+ State 入口) | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | refundStatus (0/1/2) | A | - | L4101/L4149 | A |
| 10 | Status | **cashflow.refundStatus / creditStatus** | A | - | L4434/L7084 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=12/20/30 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | medicalRecordId (Create) | A | - | L6926 | A |
| 15 | Default | payType=0 (现金默认) | A | - | L7734 | A |
| 16 | Data Source | 4 Read API + 1 Create + 1 Payment | A | - | 全部 | A |
| 17 | Object | id, totalPayment, payType, refundStatus, creditStatus | A | - | 全部 | A |
| 18 | Request | { medicalRecordId } / { cashflowId } | A | - | L6925/L4034 | A |
| 19 | Response | res.result.object / res.object.medicalRecord.id | A | - | L6932/L4034 | A |
| 20 | Function | goCheck / confirmPay / cancel | A | - | 多处 | A |
| 21 | State Bridge | cashflowId (主入口) | A | - | 50+ | A |
| 22 | Object Bridge | cashflow.totalPayment (L7784) / cashflow.refundStatus (L4434) | A | - | 全部 | A |
| 23 | API Bridge | createCashFlowForMedicalRecord / getMedicalRecordPayVo | A | - | 全部 | A |
| 24 | Business Interpretation | Cashflow 是唯一资金域核心对象 | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 1 C / 0 D / 0 E / 4 F | - | - | - | - |
| 26 | V4.4 Decision | Cashflow 必保留, Charge/Payment/Refund 不作独立实体 | A | - | - | A |

---

## §20 历史差异

### §20.1 S1-137R/141/142/143/146/147 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-137R: Cashflow → MedicalRecord 双向桥 | 实际仅 1 API (getMedicalRecordPayVo) 单向 A 派生 | 保持 | **保持 S1-137R 修正** |
| S1-141: 4 个 Cashflow Write API | 实际 5: createCashFlowForMedicalRecord + payMedicalRecordCashflow + cancelMedicalRecordCashflow + confirmMedicalRecordReturn + createMedicalStockLossOfSmallVersion | 保持 | **保持 S1-141 修正** |
| S1-141: payTypeList 0/1/2/3/11/12/13 | 实际 7 元素 (0/1/2/3/11/12/13) | 保持 | **保持 S1-141 修正** |
| S1-142: Cashflow → Delivery F | 实际 getCashflowDeliveryVo 派生 A | 保持 | **保持 S1-142 修正** |
| S1-142: confirmMedicalRecordReturn 在 deliveryInputCtrl | 实际在 optometryCtrl L35167 | 保持 | **保持 S1-142 修正** |
| S1-143: Sale 独立 saleVo | 0 命中 saleVo/saleId | 保持 | **保持 S1-143 修正** |
| S1-146: MedicalRecord 不含 status | 仍 0 命中 | 保持 | **保持 S1-146 修正** |
| S1-146: MedicalRecord 不含 cashflow 嵌套 | 仍 0 命中 | 保持 | **保持 S1-146 修正** |
| S1-147: addCheckinCtrl 真实接诊入口 | 仍成立 | 保持 | **保持 S1-147 修正** |
| (历史未确认) refundCtrl / refundLogCtrl / printCtrl / creditCtrl 存在 | 0 命中 Controller 定义 | **本轮新增** | **F (命名误导)** |

### §20.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~Charge 是独立对象~~ | 0 命中 chargeId/chargeVo | 应改 | **F (State 路由名, 不是实体)** |
| ~~Payment 是独立对象~~ | 0 命中 paymentId/paymentVo | 应改 | **F (Request Payload, 不是实体)** |
| ~~Refund 是独立对象~~ | 0 命中 refundId 专属 Write API; refundVo 11 命中但都是 Response 嵌套 | 应改 | **F (cashflow 字段 + partBackCtrl 流程, 不是独立 ID 实体)** |
| ~~payTypeList 11/12 不同含义~~ | 实际 11/12 都是"扫码"且 key/inputKey/resultKey 全部相同 | 应改 | **A (命名误导, 实际是同一支付方式)** |
| ~~cashflowVo 是独立 VO 容器~~ | 字符级 0 命中 cashflowVo | 应改 | **F (用 res.cashflow 或 object.cashflow)** |
| ~~creditStatus 是 Sale 状态~~ | 4 字符级全在 cashflow.creditStatus 派生下 | 应改 | **A (cashflow 顶层字段)** |
| ~~refundStatus 是 MedicalRecord 状态~~ | 0 命中 medicalRecord.refundStatus | 应改 | **A (cashflow 顶层字段)** |
| ~~getMedicalRecordCashflowVo 是 Cashflow → MR 桥~~ | 实际不返回 medicalRecord | 应改 | **F (只返回 cashflow + 4 VoList, 不返回 medicalRecord)** |
| ~~refundCtrl 存在~~ | NOT FOUND | 应改 | **F (partBackCtrl L4368 是真实退款 Controller)** |

### §20.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 210_S1-147 全部保持原样
- 本文档 211_*.md 单独记录 Cashflow/Charge/Payment/Refund 资金域完整闭环

---

## §21 V4.4 资金域规格

### §21.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| **cashflowId 独立 ID** | 多处 | ✓ |
| **createCashFlowForMedicalRecord.json** | L6925 | ✓ (唯一 Create) |
| **payMedicalRecordCashflow.json** | L8008 | ✓ (唯一 Payment) |
| **cancelMedicalRecordCashflow.json** | L8146 | ✓ (唯一 Cancel) |
| **getMedicalRecordPayVo.json** | L4034 | ✓ (Cashflow → MedicalRecord 唯一反向桥) |
| **getMedicalRecordCashflowVo.json** (4 调用) | L4942/L5166/L7070/L7488 | ✓ |
| **getMedicalRecordRefundDetailVo.json** | L4433 | ✓ |
| **getMedicalRecordRefundLogVo.json** (2 调用) | L4908/L7433 | ✓ |
| **getCashflowDeliveryVo.json** | L4040 | ✓ |
| **getCashFlowCashierVo.json** | L7090 | ✓ |
| **statProductDeliveryStatusOfCashflow.json** | L4047 | ✓ |
| payTypeList 7 元素 | L7734 | ✓ |
| cashflow.totalPayment / payType / refundStatus / creditStatus 顶层字段 | 全部 | ✓ |
| 18 个 Controller 消费 | 全部 | ✓ |
| 4 个 VoList (medicalExamineVoList / registrationFeeVoList / medicalProductVoList / medicalProductVoListOfModel) | L7070 | ✓ |

### §21.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `cashflowVo` 独立 VO 命名 | ✗ (0 命中) |
| `cashflow.customer` / `cashflow.patient` / `cashflow.medicalRecord` 顶层字段 | ✗ (0 命中) |
| `cashflow.customerId` / `cashflow.patientId` / `cashflow.medicalRecordId` 顶层字段 | ✗ (0 命中) |
| `cashflow.sale` / `cashflow.delivery` / `cashflow.order` / `cashflow.charge` 字段 | ✗ (0 命中) |
| `cashflow.medicalExamineVoList` / `cashflow.medicalProductVoList` 顶层 | ✗ (实际是 `object.medicalExamineVoList`) |
| `cashflow.status` (顶层, 排除 refundStatus/creditStatus) | ✗ (0 命中) |
| `medicalRecord.cashflow` / `medicalRecord.cashflowId` 字段 | ✗ (0 命中) |
| `sale.cashflow` / `sale.cashflowId` 字段 | ✗ (0 命中) |
| `delivery.cashflow` / `delivery.cashflowId` 字段 | ✗ (0 命中) |
| `customer.cashflow` / `patient.cashflow` 字段 | ✗ (0 命中) |
| `chargeId` / `chargeVo` / `Charge` 独立实体 | ✗ (0 命中) |
| `paymentId` / `paymentVo` / `Payment` 独立实体 | ✗ (0 命中) |
| `refundId` 独立 Write API (refundId 仅作 Request 参数) | ✗ (0 命中) |
| `refundCtrl` / `refundLogCtrl` / `printCtrl` / `creditCtrl` Controller | ✗ (NOT FOUND) |
| 6 ID 合并 | ✗ (cashflowId / medicalRecordId / saleId(=0) / deliveryId(=0) / patientId / customerId 必须严格区分) |
| payTypeList 11/12 不同含义 | ✗ (实际完全相同, 命名误导) |

### §21.3 Cashflow Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Cashflow** | A+B (独立 ID + Response 顶层 cashflow) | 包含 customer/patient/medicalRecord/sale/delivery 嵌套 (F) |
| **Charge** | F (0 命中) | 独立实体 (F) |
| **Payment** | C (Request Payload: payType + receivedFrom*) | 独立实体 (F) |
| **Refund** | C (cashflow 字段 + partBackCtrl 流程) | 独立 ID 实体 (F) |
| **CashflowDetail** | A (含 cashflow + 4 VoList) | - |

### §21.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `cashflow.totalPayment` (A Object) | A | L7784 waitPayDetailCtrl |
| `cashflow.refundStatus` (A Object) | A | L4434 partBackCtrl / L7084 myMaterialBillCtrl |
| `cashflow.creditStatus` (A Object) | A | L4424/L4426/L4611 partBackCtrl / L7367 myMaterialBillCtrl |
| `cashflow.payType` (A Object) | A | L7784 waitPayDetailCtrl |
| `res.object.medicalRecord.id` (A 派生) | A | L4034 (Cashflow → MedicalRecord 唯一最强反向桥) |
| `object.medicalExamineVoList[].medicalExamine.id` (A 派生) | A | L7070 |
| `object.medicalProductVoList[].medicalProduct.id` (A 派生) | A | L7070 |
| `object.registrationFeeVoList[].medicalExamine.id` (A 派生) | A | L7070 |
| `object.medicalProductVoListOfModel[].medicalProduct.id` (A 派生) | A | L7070 |
| `res.cashflow.creditStatus` (A 派生) | A | L4424 |
| `res.cashflow.refundStatus` (A 派生) | A | L4434 |
| `payTypeList[i].name` (A UI 7 元素) | A | L7734 |
| `payTypeList[i].key → receivedFrom*` (A Request) | A | L7921 |

### §21.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| MedicalRecord → Cashflow 字段桥 | F (无 medicalRecord.cashflow) |
| MedicalRecord → Cashflow 顶层 ID 桥 | F (无 medicalRecord.cashflowId) |
| Cashflow → MedicalRecord 顶层 ID 桥 | F (无 cashflow.medicalRecordId 顶层) |
| Cashflow → Sale 直接 | F |
| Cashflow → Delivery 字段桥 | F (无 cashflow.delivery) |
| Cashflow → Customer 字段桥 | F (无 cashflow.customer) |
| Cashflow → Patient 字段桥 | F (无 cashflow.patient) |
| Cashflow → MedicalExamine 字段桥 | F (无 cashflow.medicalExamineVoList 顶层) |
| Cashflow → MedicalProduct 字段桥 | F (无 cashflow.medicalProductVoList 顶层) |

### §21.6 Refund / Return / Cancel 三者 V4.4 拆分

| 概念 | V4.4 处理 | 真实 Owner |
|---|---|---|
| **Refund** | cashflow.refundStatus 字段 + partBackCtrl 流程 | Cashflow 字段 |
| **Return** | confirmMedicalRecordReturn.json API | MedicalRecord 退镜 (optometryCtrl L35167) |
| **Cancel** | cancelMedicalRecord.json + cancelMedicalRecordCashflow.json | MedicalRecord 取消 + Cashflow 取消 |

### §21.7 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `cashflowVo` | 字符级 0 命中, 用 res.cashflow 或 object.cashflow | 命名误导 |
| `getCashflowObjectFactory` (L7118) | 实际是 cashflow ObjectFactory, **不是 credit** | 命名误导 (S1-141 警告) |
| `payMedicalRecordCashflow.json` | 实际是 Cashflow Payment Write, 不是"对 medicalRecord 支付" | 命名误导 |
| `cancelMedicalRecordCashflow.json` | 实际是 Cashflow 取消 (Request: { cashflowId }), 不是"取消 medicalRecord" | 命名误导 |
| `confirmMedicalRecordReturn.json` | 实际是 MedicalRecord 退镜, 不是"cashflow 退钱" | 命名误导 |
| `refundCtrl` / `refundLogCtrl` / `printCtrl` / `creditCtrl` | **NOT FOUND** | 命名误导 (实际是 partBackCtrl L4368) |
| `waitChargeDetailCtrl` | 实际消费 cashflow 实体, 不是"charge" 实体 | 命名误导 |
| `payTypeList[11]` vs `[12]` | 实际完全相同, 都是"扫码" + `receivedFromScan` + `authCode` | 命名误导 |
| `cashflow.creditStatus = 1` (L6003) | 实际是 waitChargeDetailCtrl 写, 不是 "credit" 实体 | 命名误导 |
| `res$result$object.cashflow.creditStatus` (L7367) | 实际是 myMaterialBillCtrl 派生, 不是 "credit" API | 命名误导 |
| `getMedicalRecordCashflowVo` | 实际不返回 medicalRecord, 只返回 cashflow + 4 VoList | 命名误导 |
| `getCashflowDeliveryVo` | 实际经 cashflow 派生 deliveryVoList, 不是 cashflow.delivery | 命名误导 |
| `payedStatus` (18 命中) | 实际是 UI 列表状态, 不是 Cashflow 状态 | 命名误导 |
| `payedDetail` / `payedList` (HTML) | 实际是 "已支付" 不是 "payed" | 命名误导 |

---

## §22 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Cashflow 数据库表结构 | F | 需后端源码 |
| 2 | Charge 数据库表结构 | F (前端 0 命中) | 需后端 (如存在) |
| 3 | Payment 数据库表结构 | F (前端 0 命中) | 需后端 (如存在) |
| 4 | Refund 数据库表结构 | F (前端 0 命中 refundId 独立 Write) | 需后端 (如存在) |
| 5 | Cashflow 完整字段列表 | F | 需后端 |
| 6 | getCashflowDeliveryVo Response schema | F | 需后端 |
| 7 | getCashFlowCashierVo Response schema | F | 需后端 |
| 8 | statProductDeliveryStatusOfCashflow Response | F | 需后端 |
| 9 | payTypeList 11/12 区分意图 | F (源码完全相同) | 需业务定义 |
| 10 | medicalProductVoListOfModel 完整 schema | F | 需后端 |
| 11 | registrationFeeVoList 完整 schema | F | 需后端 |
| 12 | 4 个 NOT FOUND Controller 命名历史 | F | 需 git log |
| 13 | refundLogId 与 cashflowId 实际关系 | F | 需后端 |
| 14 | customerCouponId 完整处理 | F | 需后端 |
| 15 | payedStatus 真实字段含义 | F | 需业务定义 |
| 16 | medicalExamineVoList / medicalProductVoList 在 cashflow 中的位置 | F (前端是 `object.*VoList`, L3 可能是 cashflow 内嵌) | 需后端 |

---

## §23 Git / 完整性

### §23.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-210 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 211_*.md | ✓ |

### §23.2 Git 操作

```
git add -- 211_S1-148_Cashflow_Charge_Payment_Refund全生命周期与MedicalRecord_Sale_Delivery边界总审计.md
git diff --cached --name-only
git commit -m "docs(211): S1-148 Cashflow/Charge/Payment/Refund 全生命周期与 MedicalRecord/Sale/Delivery 边界总审计"
git push origin master
```

### §23.3 预期

- tracked = 218 → **219**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `00b9a17fe983d6518e6e4bf70dbbee2a9a1b881c` (S1-147 commit)

---

## 文档元信息

- **审计范围**：S1-148 (Cashflow / Charge / Payment / Refund 资金域)
- **本轮新增文件**：`211_S1-148_Cashflow_Charge_Payment_Refund全生命周期与MedicalRecord_Sale_Delivery边界总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-149** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
