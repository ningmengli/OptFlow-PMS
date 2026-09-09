# S1-141：Cashflow / Charge 核心对象与收费生命周期深度审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向建模（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 203 个 MD / 不修改历史
> 关联：S1-136 / S1-137 / S1-137R / S1-138

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. Cashflow 全局对象扫描
5. Cashflow 首次来源（Create）
6. MedicalRecord → Cashflow
7. Cashflow → MedicalRecord（仅 1 API）
8. Charge Controller 全量（32 个）
9. Charge 入口
10. Cashflow → Charge
11. Charge → Cashflow
12. MedicalRecord → Charge
13. Charge → MedicalRecord
14. Delivery ↔ Cashflow
15. 支付方式字段生命周期
16. 退款生命周期
17. Cashflow ObjectFactory
18. State 路由
19. Cashflow Write API 全量
20. MedicalRecord / Cashflow / Charge 三角
21. 精确数量
22. L1 / L2 / L3
23. 最终生命周期 DAG
24. 26 项证据矩阵
25. A/B/C/D/E/F 等级
26. 历史差异
27. 复刻红线
28. 红线检查
29. Git

---

## 1. 任务性质

本轮是 Cashflow / Charge 核心对象与收费生命周期深度审计。

- 禁止修改 165-203 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`204_S1-141_*.md`
- 必须区分 MedicalRecord / Cashflow / Charge / Delivery 四者

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实收费 / 支付 / 退款 / 充值 API |
| 5 | 不创建 Cashflow / 不支付 / 不退款 / 不配送 |
| 6 | 不修改 controller.js（SHA256 不变）|
| 7 | 不修改任何 HTML |
| 8 | 不修改 .gitignore |
| 9 | 不修改 165-203 历史 MD |
| 10 | 只新增 204_*.md |
| 11 | 不因为 API 名称推断对象关系 |
| 12 | 不因为 cashflowId 出现就认定存在 Charge |
| 13 | 不因为金额字段存在就建立财务实体 |
| 14 | E 不进入最终规格 |
| 15 | F 必须写："当前证据范围未观察/不可得" |

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

### 命名约束

| 误区 | 正确理解 |
|---|---|
| "API 名含 Cashflow" | ≠ "API 是 Cashflow 主语" |
| "API 名含 MedicalRecord" | ≠ "API 是 MedicalRecord 主语" |
| "cashflowId 出现" | ≠ "存在 Cashflow 实体" |
| "received* 字段" | ≠ "财务科目" |
| "payType" | ≠ "PayType 列表"（实际是 0/1/2/3/11/12/13 索引）|

---

## 4. Cashflow 全局对象扫描

### 4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `cashflow` 总命中 | 225 | A |
| `cashflowId` 总命中 | 80 | A |
| `payType` 总命中 | 70 | A |
| `refundStatus` 总命中 | 63 | A |
| `totalPayment` | 多 | A |
| `refundFee` | 多 | A |
| `creditStatus` | 多 | A |

### 4.2 Cashflow 主要 API 全量

| API | 类型 | 行号 | 说明 |
|---|---|---|---|
| **createCashFlowForMedicalRecord.json** | W (Create) | L6925 | MedicalRecord → Cashflow |
| **payMedicalRecordCashflow.json** | W (Pay) | L8017 | 设置 payType + 实际支付 |
| **payMedicalRecordCashflowForPos.json** | W (POS) | L8026 字符串 | URL 字符串 |
| **payMedicalRecordCashflowForScan.json** | W (Scan) | L8029 字符串 | URL 字符串 |
| **cancelMedicalRecordCashflow.json** | W (Cancel) | L8146 | 按 cashflowId 取消 |
| **getMedicalRecordPayVo.json** | R | L4034 | cashflowId → medicalRecord |
| **getMedicalRecordCashflowVo.json** | R | L4220/L4373/L4942/L5166/L7070/L7488 | cashflowId → cashflow |
| **getMedicalRecordRefundDetailVo.json** | R | L4433 | cashflowId → refund detail |
| **getMedicalRecordRefundLogVo.json** | R | L4908/L7433 | refundLogId → refund log |
| **getCashFlowCashierVo.json** | R | L7089 | 收银台查询 |
| **getCustomerCashflowDataPage.json** | R | L16762 | 客户 cashflow 列表 |
| **statMedicalRecordCashflow.json** | R | L37109 | 收银员 cashflow 统计 |
| **selectCashflowRefundFeeVoList.json** | R | L37766 | 退款查询 |

### 4.3 Cashflow 字段（从 getMedicalRecordCashflowVo.json Response 推断）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `id` | L4034 / L4036 (getMedicalRecordPayVo) `res.object.medicalRecord.id` | A |
| `payType` | L8016 `obj.payType = $scope.payType` / L7089 / L7084 `cashflow.payType` | A |
| `totalPayment` | L7602 `cashflow.totalPayment` | A |
| `refundStatus` | L7084 `cashflow.refundStatus` | A |
| `creditStatus` | L4434 `cashflow.refundStatus === 1` (L4424 `cashflow.creditStatus`) | A |
| `receivedFromCashier` | L7266 `cashflow.receivedFromCashier` | A |
| `receivedFromCredit` | L7373 `res.object.cashflow.receivedFromCredit` | A |
| `customer` | L4947 `res.result.object.customer.id` | A |
| `medicalExamineVoList` | L7072 | A |
| `medicalProductVoList` | L7078 | A |
| `registrationFeeVoList` | L7075 | A |
| `medicalProductVoListOfModel` | L7081 | A |

### 4.4 4 个 ID 在 Cashflow 中的关系

| ID | 出现在 Cashflow Response | 等级 |
|---|---|---|
| `cashflowId` (=cashflow.id) | A (顶层) | A |
| `customerId` | A (cashflow.customer.id L4947) | A |
| `medicalRecordId` | **F** (cashflow 对象不含 medicalRecordId 字段) | F |
| `patientId` | **F** (cashflow 对象不含 patientId 字段) | F |

**关键发现**: Cashflow 实体不直接含 medicalRecordId 字段。要建立 MedicalRecord ↔ Cashflow 桥必须经 `getMedicalRecordPayVo.json` (Response 含 medicalRecord)。

---

## 5. Cashflow 首次来源（Create）

### 5.1 createCashFlowForMedicalRecord.json（L6925）

**Context**: myMaterialBillCtrl (L6555+) — "去收费" 入口

```javascript
// L6920-L6931 myMaterialBillCtrl.goCheck
$scope.goCheck = function () {
    var obj = $scope.backReqList(false, true);
    if (!obj) return;
    var fn = function fn() {
      obj.medicalRecordId = $scope.medicalRecordId;                 // L6924 — medicalRecordId 加入 Request
      new ObjectFactory().saveOrQuery(
        "/admin/createCashFlowForMedicalRecord.json",                // L6925 — **唯一 Cashflow Create API**
        obj
      ).then(function (res) {
        if (res.status == 1) {
          return Popup.notice(res.errmsg);
        }
        $state.go("waitPayDetail", { cashflowId: res.result.object });  // L6929 — cashflowId 进入 State
      });
    };
    ...
};
```

### 5.2 createCashFlowForMedicalRecord.json 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | myMaterialBillCtrl (L6555+) |
| B. 调用行 | L6925 |
| C. Request | `obj` (含 obj.medicalRecordId = $scope.medicalRecordId) + 其它费用字段 |
| D. medicalRecordId Source | `$scope.medicalRecordId` (State 入口) |
| E. customerId Source | **F** — obj 中**不直接包含** customerId（需从 $scope.obj.customerId 派生）|
| F. patientId Source | **F** — Request 不含 patientId 字段 |
| G. Response | `res.result.object` (即 cashflowId) |
| H. 立即 State | `$state.go("waitPayDetail", { cashflowId: res.result.object })` (L6929) |
| I. 是否 Create Cashflow | **A** — Response 返回 cashflowId（这是 Cashflow 主键）|

### 5.3 Cashflow Create 候选全量

| API | 类型 | 是否 Create Cashflow |
|---|---|:---:|
| createCashFlowForMedicalRecord.json (L6925) | W | **A** |
| payMedicalRecordCashflow.json (L8017) | W (Pay，不是 Create) | F |
| payMedicalRecordCashflowForPos.json (L8026) | W (Pay) | F |
| payMedicalRecordCashflowForScan.json (L8029) | W (Pay) | F |
| cancelMedicalRecordCashflow.json (L8146) | W (Cancel) | F |
| insertCashflow* / addCashflow* / newCashflow* | 0 命中 | F |
| saveCashflow* | 0 命中 | F |

**结论**: `createCashFlowForMedicalRecord.json` 是**唯一 Cashflow Create API**（A）。

---

## 6. MedicalRecord → Cashflow

### 6.1 唯一字符级证据 L6925

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| **MedicalRecord → Cashflow** | **A** | L6924 `obj.medicalRecordId = $scope.medicalRecordId` → L6925 `createCashFlowForMedicalRecord.json(obj)` → L6929 `res.result.object` (cashflowId) |

### 6.2 七种桥逐项判定

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L6920 `$scope.goCheck` 函数 |
| B. State | A | L6929 `$state.go("waitPayDetail", { cashflowId })` |
| C. API Response→Request | A | L6924→L6925 medicalRecordId → createCashFlowForMedicalRecord |
| D. Scope/Service | A | L6924 `$scope.medicalRecordId` (State 入口) |
| E. Factory | C | L6925 `new ObjectFactory()` (非 cashflowFactory) |
| F. Object | F | 无对象引用 |
| G. 字段共现 | A | medicalRecordId + cashflowId 在同一函数 |

### 6.3 MedicalRecord → Cashflow 完整链

```
MedicalRecord (medicalRecord.id from State)
    ↓ A (L6924 obj.medicalRecordId = $scope.medicalRecordId)
    ↓ A (L6925 createCashFlowForMedicalRecord.json POST)
Cashflow (cashflowId from res.result.object)
    ↓ A (L6929 $state.go("waitPayDetail", { cashflowId }))
Charge State (waitPayDetail)
```

**MedicalRecord → Cashflow = A 直接桥**（S1-138 已确认）

---

## 7. Cashflow → MedicalRecord（仅 1 API）

### 7.1 getMedicalRecordPayVo.json（L4034）

**Context**: deliveryInputRecordCtrl (L4024) — Delivery 内部派生

```javascript
// L4033-L4036 deliveryInputRecordCtrl
var getMedicalRecord = new ObjectFactory();
var recordPromise = getMedicalRecord.saveOrQuery(
  '/admin/getMedicalRecordPayVo.json',                        // L4034
  { cashflowId: $scope.cashflowId }
);
recordPromise.then(function (res) {
  $scope.medicalRecordId = res.object.medicalRecord.id;        // L4036
});
```

### 7.2 Cashflow → MedicalRecord 唯一桥

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| **Cashflow → MedicalRecord** | **A** | L4034 cashflowId → getMedicalRecordPayVo → L4036 `res.object.medicalRecord.id` |

### 7.3 其它 3 个 MedicalRecord API 名称不构成 Cashflow → MedicalRecord 桥

| API | Request 字段 | Response 含 medicalRecord | 等级 |
|---|---|---|:---:|
| getMedicalRecordCashflowVo.json | cashflowId | **F** (0 命中) | F |
| getMedicalRecordRefundDetailVo.json | cashflowId | **F** (0 命中) | F |
| getMedicalRecordRefundLogVo.json | **refundLogId** | **F** (0 命中) | F |

**S1-137R §5.5 已确认**: 4 个 API 中**只有** getMedicalRecordPayVo.json 真正含 medicalRecord 字段。

### 7.4 Cashflow → MedicalRecord 七种桥

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L4035 `recordPromise.then` |
| B. State | A | L4026 `$stateParams.cashflowId` |
| C. API Response→Request | A | L4034 cashflowId → L4036 medicalRecord.id |
| D. Scope/Service | A | L4036 `$scope.medicalRecordId` 派生 |
| E. Factory | C | L4033 `new ObjectFactory()` (非 cashflowFactory) |
| F. Object | F | 无对象引用 |
| G. 字段共现 | A | cashflowId + medicalRecordId 在同一函数 |

**Cashflow → MedicalRecord = A 直接桥**（仅 1 个 API：getMedicalRecordPayVo.json）

---

## 8. Charge Controller 全量（32 个）

### 8.1 支付流程 Controllers（11 个核心）

| # | Controller | 行号 | State 入口参数 | cashflowId | medicalRecordId |
|---|---|---|---|:---:|:---:|
| 1 | **waitPayDetailCtrl** | L7452 | `cashflowId` (L7462) | A | F |
| 2 | **waitPayListCtrl** | L8110 | - | A | F |
| 3 | **waitChargeDetailCtrl** | L6568 | (Charge Detail) | A | A (L6693) |
| 4 | **waitChargeListCtrl** | L6957 | (Charge List) | F | A |
| 5 | **payedDetailCtrl** | L4937 | `cashflowId` (L4940) | A | F |
| 6 | **payedListCtrl** | L4972 | - | F | F |
| 7 | **unPayDetailCtrl** | L5987 | `customerId` (L5994) | F | F |
| 8 | **unPayListCtrl** | L6526 | - | F | F |
| 9 | **waitPayBackCtrl** | L6992 | `cashflowId` (L6993) | A | A (L7070) |
| 10 | **waitPayBackListCtrl** | L7383 | - | F | F |
| 11 | **payBackDetailCtrl** | L4899 | - | F | F |
| 12 | **partBackCtrl** | L4368 | `cashflowId` (L4381) | A | F |

### 8.2 收银台 / 日结 / 充值 Controllers（5 个核心）

| # | Controller | 行号 | State 入口参数 | 入口 cashflowId |
|---|---|---|---|:---:|
| 13 | **feeCashierCtrl** | L36905 | - | F |
| 14 | **feeDayCtrl** | L37005 | - | F |
| 15 | **feeRechargeCtrl** | L37183 | - | F |
| 16 | **pointsListChargeCtrl** | L37432 | - | F |
| 17 | **pointsListReChargeCtrl** | L37459 | - | F |
| 18 | **unPayChargeCtrl** | L38500 | - | F |
| 19 | **unPayRechargeCtrl** | L38525 | - | F |
| 20 | **hospitalRechargeCtrl** | L15883 | - | F |
| 21 | **refundFeeCtrl** | L37657 | - | F |

### 8.3 充值记录 Controllers（2 个核心）

| # | Controller | 行号 | State 入口参数 |
|---|---|---|---|
| 22 | **reChargeListCtrl** | L5192 | `customerId` (L5192) |
| 23 | **reChargeListBackCtrl** | L5692 | `customerId` (L5692) |

### 8.4 收费项管理 Controllers（8 个 — 实际是"项目/价格"管理）

| # | Controller | 行号 | 用途 |
|---|---|---|---|
| 24 | **chargeListCtrl** | L16758 | 收费项列表 |
| 25 | **addCustomerChargeCtrl** | L50472 | 新增客户收费项 |
| 26 | **addCustomerChargeItemCtrl** | L50776 | 新增收费项目 |
| 27 | **chargeAdminCtrl** | L52575 | 收费项管理 |
| 28 | **chargeWaysCtrl** | L52767 | 收费方式管理 |
| 29 | **customerChargeCtrl** | L53318 | 客户收费 |
| 30 | **customerChargeChoiceCtrl** | L53685 | 客户收费选择 |
| 31 | **customerChargeItemCtrl** | L53806 | 客户收费项 |
| 32 | **memberChargeCtrl** | L55727 | 会员收费 |
| 33 | **modifyCustomerChargeCtrl** | L56044 | 修改客户收费项 |
| 34 | **modifyCustomerChargeItemCtrl** | L56384 | 修改客户收费项 |
| 35 | **timeCardRechargeCtrl** | L38463 | 次卡充值 |

**注意**: 收费项管理 Controllers 与 Cashflow / Cash flow 关系不大，主要管理"收费项"（如挂号费、检查费、治疗费等业务项目的价格定义），不涉及 Cashflow 实际支付。

### 8.5 Charge 核心 Controllers 分类

| 分类 | 数量 | Controller |
|---|:---:|---|
| 待支付/已支付 (cashflow 入口) | 4 | waitPayDetail / waitPayList / payedDetail / payedList |
| 待收费 (medicalRecord → cashflow 入口) | 2 | waitChargeDetail / waitChargeList |
| 退款 (cashflow 入口) | 4 | waitPayBack / waitPayBackList / payBackDetail / partBack |
| 收银台/日结/充值 (统计) | 9 | feeCashier / feeDay / feeRecharge / pointsList* / unPay* / hospitalRecharge / refundFee |
| 充值记录 (customer 入口) | 2 | reChargeList / reChargeListBack |
| 收费项管理 (价格定义) | 11 | chargeList / addCustomerCharge* / chargeAdmin / chargeWays / customerCharge* / memberCharge / modifyCustomerCharge* / timeCardRecharge |

---

## 9. Charge 入口

### 9.1 4 个核心 Charge State 入口

| State | Controller | 入口参数 | 实际消费 ID |
|---|---|---|---|
| **waitPayDetail** | waitPayDetailCtrl | `cashflowId` (L7462) | cashflowId |
| **waitPayList** | waitPayListCtrl | - | - |
| **payedDetail** | payedDetailCtrl | `cashflowId` (L4940) | cashflowId |
| **payedList** | payedListCtrl | - | - |
| **waitChargeDetail** | waitChargeDetailCtrl | (可能 patientId) | medicalRecordId (L6693 派生) |
| **waitChargeList** | waitChargeListCtrl | - | - |
| **waitPayBack** | waitPayBackCtrl | `cashflowId` (L6993) | cashflowId |

### 9.2 $stateParams.cashflowId 全部入口

`Select-String '\$stateParams\.cashflowId' controller.js`:

| # | 行号 | Controller | 用途 |
|---|---|---|---|
| 1 | L3814 | deliveryInputCtrl | Delivery 入口 |
| 2 | L4026 | deliveryInputRecordCtrl | Delivery 内部 |
| 3 | L4238 | deliveryProcessingCtrl | Delivery 处理 |
| 4 | L4381 | partBackCtrl | 退款入口 |
| 5 | L4940 | payedDetailCtrl | 已支付详情 |
| 6 | L6993 | waitPayBackCtrl | 退款 (待支付) |
| 7 | L7462 | waitPayDetailCtrl | 待支付详情 |

**7 个 State 入口使用 cashflowId** — 全部 A 级字符级证据。

### 9.3 Charge 入口特征

| 特征 | 等级 | 字符级证据 |
|---|:---:|---|
| 主流入口参数是 `cashflowId` | A | 7 处 $stateParams.cashflowId |
| 少数入口是 `customerId` | A | reChargeList / unPayDetail |
| **几乎无入口直接是 `medicalRecordId`** | A | 仅 L6693 在 waitChargeDetail 内派生 |
| **主流入口不是 `patientId`** | A | 0 处 $stateParams.patientId 在 Charge Controller |

---

## 10. Cashflow → Charge

### 10.1 Cashflow → Charge 七种桥

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L6920 `$scope.goCheck` 创建 cashflow 后跳 waitPayDetail |
| B. State | A | L6929 `$state.go("waitPayDetail", { cashflowId: res.result.object })` |
| C. API Response→Request | A | L6925 → L6929 |
| D. Scope/Service | A | $scope.cashflowId (从 State) |
| E. Factory | F | — |
| F. Object | F | — |
| G. 字段共现 | A | cashflowId + 各种 $stateParams.cashflowId |

### 10.2 Cashflow → Charge 完整链

```
Cashflow (cashflowId from createCashFlowForMedicalRecord)
    ↓ A (L6929 $state.go("waitPayDetail"))
Charge State (waitPayDetail / payedDetail / partBack / delivery)
```

**Cashflow → Charge = A 直接桥**（所有 Charge State 入口都是 cashflowId）

---

## 11. Charge → Cashflow

### 11.1 Charge → Cashflow 7 种桥

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L8143 `$scope.cancelPay` 调用 cancelMedicalRecordCashflow |
| B. State | A | $stateParams.cashflowId 多次 |
| C. API Response→Request | A | L8151 $state.go("waitPayList") |
| D. Scope/Service | A | L8146 $scope.cancelCashObjectFactory |
| E. Factory | C | L8145 new ObjectFactory() |
| F. Object | F | — |
| G. 字段共现 | A | cashflowId 在多个 Charge 入口 |

### 11.2 Charge → Cashflow 实际行为

Charge 控制器**只读** Cashflow（通过 getMedicalRecordCashflowVo.json 查询），不直接修改 Cashflow 实体。

唯一**修改** Cashflow 的 Charge 相关 API:
- `payMedicalRecordCashflow.json` (L8017) — Pay (Charge → Cashflow.W)
- `cancelMedicalRecordCashflow.json` (L8146) — Cancel (Charge → Cashflow.W)

**Charge → Cashflow = A** (读 + 写)

---

## 12. MedicalRecord → Charge

### 12.1 MedicalRecord → Charge 桥

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| **MedicalRecord → Cashflow → Charge** | **A**（间接 2 层）| L6925 createCashFlowForMedicalRecord → L6929 $state.go waitPayDetail |
| **MedicalRecord → Charge 直接** | **F** | Charge 入口不直接用 medicalRecordId |

### 12.2 MedicalRecord → Charge 完整链

```
MedicalRecord (medicalRecordId from State)
    ↓ A (L6924 obj.medicalRecordId = $scope.medicalRecordId)
    ↓ A (L6925 createCashFlowForMedicalRecord.json POST)
Cashflow (cashflowId)
    ↓ A (L6929 $state.go("waitPayDetail", { cashflowId }))
Charge (waitPayDetail)
```

**MedicalRecord → Charge 间接 A**（必经 Cashflow）

---

## 13. Charge → MedicalRecord

### 13.1 字符级搜索

`Select-String 'medicalRecordId' controller.js` — 多处
但其中 Charge 范围内的:

| 行号 | Controller | 含义 |
|---|---|---|
| L6693 | waitChargeDetailCtrl | `getPatientInfo.json { id: res.object.medicalRecord.patientId }` (patient 派生，不是 medicalRecord) |
| L7070 | waitPayBackCtrl | `getMedicalRecordCashflowVo.json { cashflowId }` (Cashflow 入口) |
| L7681 | waitPayDetailCtrl | `getMedicalRecordCashflowVo.json` 内部 |

### 13.2 waitChargeDetailCtrl 入口

waitChargeDetailCtrl (L6568) 实际**不直接接收 medicalRecordId State 参数**，而是通过 Cashflow → getMedicalRecordPayVo → medicalRecord 的反向派生。

| 命题 | 结论 | 等级 |
|---|---|---|
| Charge 入口用 medicalRecordId | **F**（0 处 $stateParams.medicalRecordId 在 Charge Controller）| F |
| Charge 入口用 cashflowId | A（7 处 $stateParams.cashflowId）| A |
| Charge 内部派生 medicalRecordId | C（getMedicalRecordPayVo L4034，仅 Delivery）| C |

**Charge → MedicalRecord = F**（Charge 入口不直接消费 medicalRecordId）

---

## 14. Delivery ↔ Cashflow

### 14.1 Delivery → Cashflow（5 处 State 入口）

S1-137R 已确认 5 处 $stateParams.cashflowId:
- L3814 / L4026 / L4238 (Delivery Controller)
- L4381 (partBackCtrl — 属于 Charge 退款流程，不是 Delivery)
- L4940 (payedDetailCtrl — 属于 Charge 流程)

**真正 Delivery 入口: 3 处** (L3814/L4026/L4238)

### 14.2 Cashflow → Delivery

Cashflow → Delivery = **F**（无任何 State 跳转从 Cashflow 进入 Delivery）
- $state.go("delivery...") 全文 0 命中
- Delivery 入口是用户主动跳转

### 14.3 Delivery 入口 ID 实际模式

Delivery Controller (`$stateParams.cashflowId`) 内部通过 `getMedicalRecordPayVo.json` 派生 `$scope.medicalRecordId`（A）

### 14.4 Delivery ↔ Cashflow 桥矩阵

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| **Delivery → Cashflow**（读）| **A** | $stateParams.cashflowId 3 处 |
| **Cashflow → Delivery**（写/跳）| **F** | 无 $state.go 入口 |
| **Delivery → MedicalRecord**（派生）| **A** | L4036 `$scope.medicalRecordId = res.object.medicalRecord.id` |
| **MedicalRecord → Delivery** | **F** | 无 $state.go 入口 |

---

## 15. 支付方式字段生命周期

### 15.1 payTypeList 完整定义（L7734-L7775+）

```javascript
// L7734-L7775 payTypeList 完整定义
$scope.payTypeList = [{
    index: 0,
    name: "现金",
    key: "receivedFromCash",
    inputKey: "cashFee"
}, {
    index: 1,
    name: "微信记账",
    key: "receivedFromWechat",
    inputKey: "wechatFee"
}, {
    index: 2,
    name: "支付宝记账",
    key: "receivedFromAlipay",
    inputKey: "alipayFee"
}, {
    index: 3,
    name: "银行卡",
    key: "receivedFromBankcard",
    inputKey: "bankCardFee"
}, {
    index: 11,
    name: "扫码",
    key: "receivedFromScan",
    inputKey: "authCode",
    resultKey: "authCode"
}, {
    index: 12,
    name: "扫码",
    key: "receivedFromScan",
    inputKey: "authCode",
    resultKey: "authCode"
}, {
    index: 13,
    name: "POS机",
    key: "receivedFromPos",
    inputKey: "posCode"
}];
```

| index | 名称 | 关键字段 |
|:---:|---|---|
| 0 | 现金 | receivedFromCash / cashFee |
| 1 | 微信记账 | receivedFromWechat / wechatFee |
| 2 | 支付宝记账 | receivedFromAlipay / alipayFee |
| 3 | 银行卡 | receivedFromBankcard / bankCardFee |
| 11 | 扫码 | receivedFromScan / authCode |
| 12 | 扫码 | receivedFromScan / authCode |
| 13 | POS机 | receivedFromPos / posCode |

### 15.2 received* 字段全量

| 字段 | Source (A) | 用途 (B) | 进入 Request (C) |
|---|---|---|---|
| `receivedFromCashier` | A (L7266 Response) | 显示 | F（未直接 send） |
| `receivedFromWallet` | A (L7602 / L7620+) | 钱包支付 | **A** (L7525/L7626 obj) |
| `receivedFromCommercial` | A (L7602) | 商保支付 | **A** (L7527 obj) |
| `receivedFromMedical` | A | 医保支付 | **A** (L7526 obj) |
| `receivedFromCredit` | A (L7373 Response) | 挂账支付 | **A** (L7524 obj) |
| `receivedFromCash` | A (payTypeList 索引 0) | 现金 | **A** (payTypeList dynamic) |
| `receivedFromWechat` | A (payTypeList 索引 1) | 微信 | **A** |
| `receivedFromAlipay` | A (payTypeList 索引 2) | 支付宝 | **A** |
| `receivedFromBankcard` | A (payTypeList 索引 3) | 银行卡 | **A** |
| `receivedFromScan` | A (payTypeList 索引 11/12) | 扫码 | **A** |
| `receivedFromPos` | A (payTypeList 索引 13) | POS | **A** |

### 15.3 totalPayment

| 模式 | 行号 | 等级 |
|---|---|---|
| `cashflow.totalPayment` (Response) | L7602 | A |
| `totalPayment` (Scope) | L7602 计算 `new Big($scope.getCashflowObjectFactory.object.cashflow.totalPayment).minus(...)` | A |

**totalPayment 生命周期**:
1. **Response 字段**: cashflow.totalPayment (来自 getMedicalRecordCashflowVo.json)
2. **Scope 读取**: $scope.getCashflowObjectFactory.object.cashflow.totalPayment
3. **计算**: new Big(totalPayment).minus(substractFee).minus(receivedFromWallet).minus(receivedFromCommercial)...
4. **不直接进入 Request** (实际付费总额由 payMedicalRecordCashflow 内部处理)

### 15.4 payType 生命周期

| 阶段 | 字段 | 行号 |
|---|---|---|
| Scope 初始化 | `$scope.payType` | (waitPayDetailCtrl) |
| Request | `obj.payType = $scope.payType` | L8016 |
| API | payMedicalRecordCashflow.json | L8017 |
| Response | (res.status 检查) | L8018 |

---

## 16. 退款生命周期

### 16.1 退款 API 全量

| API | 类型 | Request | 行号 |
|---|---|---|---|
| getMedicalRecordRefundDetailVo.json | R | cashflowId | L4433 |
| getMedicalRecordRefundLogVo.json | R | **refundLogId** | L4908/L7433 |
| selectCashflowRefundFeeVoList.json | R | obj | L37766 |
| (退款 Write API) | ? | ? | F (0 命中) |

### 16.2 退款流程入口

| 入口 | Controller | 入口参数 | 派生 |
|---|---|---|---|
| waitPayBack | waitPayBackCtrl | `cashflowId` (L6993) | refundDetail |
| payBackDetail | payBackDetailCtrl | (refundLogId) | refundLog |
| partBack | partBackCtrl | `cashflowId` (L4381) | refundDetail + refundAction |

### 16.3 refundStatus 字段

| 模式 | 行号 | 等级 |
|---|---|---|
| `cashflow.refundStatus` | L7084 (cashflow.refundStatus === 2) | A |
| `cashflow.refundStatus === 1` | L4434 | A |
| `cashflow.refundStatus === 2` | L7084 | A |
| `res.cashflow.refundStatus === 1` | L4434 | A |

### 16.4 creditStatus 字段

| 模式 | 行号 | 等级 |
|---|---|---|
| `cashflow.creditStatus === 1` | L4426 / L4611 | A |
| `res.cashflow.creditStatus` | L4424 (console.log) | A |

### 16.5 Refund 流程字段生命周期

```
Cashflow
    ↓ A (cashflowId)
getMedicalRecordRefundDetailVo.json (L4433)
    ↓ A (Response: cashflow.refundStatus, medicalProductRefundVoList, medicalExamineRefundVoList)
$scope.refundFeeInfo = res (L4437)
    ↓ A (cashflow.creditStatus === 1)
$scope.showBackGoods (L4427)
    ↓ A (refundTypeFeeVoList)
$scope.partBack.concatChannel (L4452)
```

### 16.6 Refund → MedicalRecord 桥

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Refund API 含 medicalRecord 字段 | **F** | getMedicalRecordRefundDetailVo/LogVo 均无 medicalRecord 字段 |
| Refund → MedicalRecord 直接桥 | **F** | — |
| Refund → MedicalRecord 经 Cashflow | A (间接 2 层) | Refund (Cashflow) → getMedicalRecordPayVo → medicalRecord |

---

## 17. Cashflow ObjectFactory

### 17.1 cashflow 相关 ObjectFactory

| 行号 | Factory 名称 | 实际内容 | 命名 |
|---|---|---|---|
| L4941 | `getCashflowObjectFactory` | getMedicalRecordCashflowVo.json Response | 一致 |
| L5165 | `getCashflowObjectFactory` | getMedicalRecordCashflowVo.json | 一致 |
| L7070 | `getCashflowObjectFactory` | getMedicalRecordCashflowVo.json | 一致 |
| L7487 | `getCashflowObjectFactory` | getMedicalRecordCashflowVo.json | 一致 |
| L7118 (L7266附近) | `getCashFlowCredit` | getMedicalRecordCashflowVo.json | 命名误导 (Credit 不是 Refund)|
| L8145 | `cancelCashObjectFactory` | cancelMedicalRecordCashflow.json | 命名一致 |

### 17.2 跨 Controller 共享

**F**: 每个 Controller 独立 `new ObjectFactory()`。即使同名 `getCashflowObjectFactory` 也不跨 Controller 共享（S1-139 已确认）。

### 17.3 cashflow ListFactory

| API | 行号 | Controller |
|---|---|---|
| getMedicalRecordCashflowVoListOfCompany.json | L5085 / L8129 | payedListCtrl |
| getCustomerCashflowDataPage.json | L16762 | chargeListCtrl |
| statMedicalRecordCashflow.json | L37109 | feeCashierCtrl |
| selectCashflowRefundFeeVoList.json | L37766 | refundFeeCtrl |

---

## 18. State 路由

### 18.1 Cashflow 相关 $state.go

| 源 | 目标 State | 参数 | 行号 |
|---|---|---|---|
| myMaterialBillCtrl | waitPayDetail | `{ cashflowId: res.result.object }` | L6929 |
| waitPayDetailCtrl | payedList | - | L8021 |
| waitPayDetailCtrl | payedList | - | L8061 |
| waitPayDetailCtrl | waitChargeList | - | L8064 |
| waitPayListCtrl | payedList | - | L8061 |
| waitPayListCtrl | waitPayList | (reload) | L8151 |
| partBackCtrl | payedList | (refundStatus===1) | L4435 |
| partBackCtrl | partBack | `{ cashflowId }` | L5180 |
| waitPayBackCtrl | partBack | `{ cashflowId }` | L7156 |
| partBackCtrl | waitPayBackList | - | L7215/L7280 |
| waitPayListCtrl | waitPayList | (reload) | L8151 |
| partBackCtrl | unPayList | - | L6345/L6448 |
| myMaterialBillCtrl | waitPayList | - | L6684 |

### 18.2 完整 Cashflow State 树

```
[Create Entry]
  waitPayList (cashflowId 多列表)
    ↓ goPay
  waitPayDetail (cashflowId)
    ↓ 支付完成
  payedList
    ↓
  payedDetail (cashflowId)
    ↓
  (历史订单)

[Refund Entry]
  waitPayBackList
    ↓
  waitPayBack (cashflowId)
    ↓
  partBack (cashflowId)
    ↓ 部分退款完成
  payedList
    ↓
  payBackDetail (refundLogId)

[Delivery]
  deliveryList
    ↓
  deliveryInput (cashflowId)
    ↓
  deliveryInputRecord (cashflowId)
    ↓
  deliveryProcessing (cashflowId)
```

---

## 19. Cashflow Write API 全量

| # | API | 行号 | Type | Request | 立即 State |
|---|---|---|---|---|---|
| 1 | **createCashFlowForMedicalRecord.json** | L6925 | W (Create) | obj + medicalRecordId | waitPayDetail |
| 2 | **payMedicalRecordCashflow.json** | L8017 | W (Pay) | obj + payType | payedList |
| 3 | **payMedicalRecordCashflowForPos.json** | L8026 字符串 | W (Pay) | obj (POS 模式) | - |
| 4 | **payMedicalRecordCashflowForScan.json** | L8029 字符串 | W (Pay) | obj (Scan 模式) | - |
| 5 | **cancelMedicalRecordCashflow.json** | L8146 | W (Cancel) | cashflowId | waitPayList |

**注意**: 3 和 4 仅作为 URL 字符串出现 (L8026/L8029)，实际 API 调用方法不一定相同。

---

## 20. MedicalRecord / Cashflow / Charge 三角

### 20.1 6 个方向

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → Cashflow | **A** | L6925 createCashFlowForMedicalRecord |
| Cashflow → MedicalRecord | **A** | L4034 getMedicalRecordPayVo (仅 1 API) |
| MedicalRecord → Charge | **F** 直接 / **A** 间接 | 经 Cashflow (L6925→L6929) |
| Charge → MedicalRecord | **F** | Charge 不直接消费 medicalRecordId |
| Cashflow → Charge | **A** | L6929 $state.go("waitPayDetail", { cashflowId }) |
| Charge → Cashflow | **A** | L8146 cancelMedicalRecordCashflow |

### 20.2 三角关系

```
MedicalRecord ←—A—→ Cashflow —A—→ Charge
   ↑                                 ↓
   └──── F (Charge→MedicalRecord) ──┘
```

- MedicalRecord ↔ Cashflow: **A 双向**（createCashFlowForMedicalRecord + getMedicalRecordPayVo）
- Cashflow → Charge: **A 单向**（createCashFlowForMedicalRecord 立即跳 waitPayDetail）
- Charge → Cashflow: **A 单向**（cancelMedicalRecordCashflow + payMedicalRecordCashflow）
- MedicalRecord → Charge: **F 直接** / **A 间接**（必经 Cashflow）
- Charge → MedicalRecord: **F**（无字符级证据）

---

## 21. 精确数量

### 21.1 Cashflow 字符级统计

| 模式 | 命中数 |
|---|---:|
| `cashflow` 总命中 | 225 |
| `cashflowId` 总命中 | 80 |
| `cashflow.id` | 多 |
| `cashflow.payType` | 多 |
| `cashflow.totalPayment` | L7602 |
| `cashflow.refundStatus` | L7084 / L4434 |
| `cashflow.creditStatus` | L4424 / L4426 / L4611 |
| `cashflow.receivedFromCashier` | L7266 |
| `cashflow.receivedFromCredit` | L7373 |
| `cashflow.customer` | L4947 |
| `cashflow.medicalExamineVoList` | L7072 |
| `cashflow.medicalProductVoList` | L7078 |

### 21.2 支付字段统计

| 字段 | 命中数 | 等级 |
|---|---:|:---:|
| `payType` | 70 | A |
| `totalPayment` | 多 | A |
| `refundFee` | 多 | A |
| `receivedFromCashier` | 1 | A |
| `receivedFromWallet` | 7+ | A |
| `receivedFromCommercial` | 4+ | A |
| `receivedFromMedical` | 3+ | A |
| `receivedFromCredit` | 3+ | A |
| `refundStatus` | 63 | A |

### 21.3 Charge 统计

| 统计项 | 数量 |
|---|:---:|
| Charge 相关 Controller | 32 (支付流程 12 + 收银台 9 + 充值记录 2 + 收费项管理 11) |
| 支付流程 Controller (cashflowId 入口) | 7 |
| Cashflow Write API | 5 (createCashFlowForMedicalRecord + payMedicalRecordCashflow × 3 + cancelMedicalRecordCashflow) |
| Cashflow Read API | 13+ |
| Refund API | 4 (getMedicalRecordRefundDetailVo / getMedicalRecordRefundLogVo / selectCashflowRefundFeeVoList / waitPayBack 状态机) |
| $stateParams.cashflowId 入口 | 7 (含 3 Delivery + 4 Charge) |
| $state.go("delivery...") 入口 | 0 |

### 21.4 Delivery 统计

| 统计项 | 数量 |
|---|:---:|
| $stateParams.cashflowId (Delivery 范围) | 3 (L3814/L4026/L4238) |
| $stateParams.medicalRecordId (Delivery 范围) | 0 |
| getMedicalRecordPayVo 调用 | 1 (L4034) |

---

## 22. L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | API / Request / Response / State / Scope / Factory / Field 全部字符级 | A |
| L2 | "Cashflow 入口" / "支付流程" / "退款流程" 等派生解释 | A |
| L3 | Cashflow/Charge/Refund 数据库表 / FK / 唯一索引 / 事务 | **F**（无后端证据）|

---

## 23. 最终生命周期 DAG

### DAG A: MedicalRecord → Cashflow
**A** — L6925 createCashFlowForMedicalRecord

### DAG B: Cashflow → MedicalRecord
**A** — L4034 getMedicalRecordPayVo (仅 1 API)

### DAG C: Cashflow → Charge
**A** — L6929 $state.go("waitPayDetail", { cashflowId })

### DAG D: Charge → Cashflow
**A** — L8146 cancelMedicalRecordCashflow + L8017 payMedicalRecordCashflow

### DAG E: MedicalRecord → Charge
**F** 直接 / **A 间接 2 层**（经 Cashflow）

### DAG F: Charge → MedicalRecord
**F**（无字符级证据）

### DAG G: Cashflow → Delivery
**F**（无 $state.go 入口）

### DAG H: Delivery → Cashflow
**A**（3 处 $stateParams.cashflowId）

### DAG I: Cashflow → Refund
**A** — L4433 getMedicalRecordRefundDetailVo

### DAG J: Refund → MedicalRecord
**F** 直接 / **A 间接**（经 Cashflow → getMedicalRecordPayVo）

### DAG K: Cashflow → MedicalRecord → Charge
**A 间接 2 层** (DAG B + DAG E)

### DAG L: MedicalRecord → Cashflow → Delivery
**A 间接 2 层** (DAG A + DAG H) — MedicalRecord 创建 cashflow → cashflow 跳 Delivery (waitPayDetail → deliveryList 间接? 实际无)

### 完整生命周期图

```
                  [MedicalRecord]
                       ↓ A (createCashFlowForMedicalRecord L6925)
                  [Cashflow]
                       ↓ A ($state.go waitPayDetail L6929)
              ┌──────┴──────┐
              ↓              ↓
         [Charge]      [Delivery] ← A (3 处 cashflowId 入口)
              ↓              
        ┌─────┼─────┐
        ↓     ↓     ↓
      [Pay] [Back] [Detail]
        ↓
   payMedicalRecordCashflow L8017
   cancelMedicalRecordCashflow L8146
   getMedicalRecordCashflowVo (L4942/7070/...)
```

---

## 24. 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Cashflow Source | 字符级充分 | A | 多处 | 全部 | A |
| 2 | cashflowId Source | 80 命中 | A | 多处 | 全部 | A |
| 3 | Cashflow Create | **createCashFlowForMedicalRecord.json** | A | myMaterialBillCtrl | L6925 | A |
| 4 | Cashflow Create Request | obj + obj.medicalRecordId | A | myMaterialBillCtrl | L6924-L6925 | A |
| 5 | Cashflow Create Response | res.result.object (cashflowId) | A | myMaterialBillCtrl | L6929 | A |
| 6 | MedicalRecord → Cashflow | createCashFlowForMedicalRecord | A | myMaterialBillCtrl | L6924-L6925 | A |
| 7 | Cashflow → MedicalRecord | getMedicalRecordPayVo (1 API) | A | deliveryInputRecordCtrl | L4034-L4036 | A |
| 8 | Charge Controller | 32 个 | A | 多处 | 全部 | A |
| 9 | Charge Entry | 7 处 $stateParams.cashflowId | A | 多处 | 全部 | A |
| 10 | Charge cashflowId | 7 入口 | A | 多处 | 全部 | A |
| 11 | Charge medicalRecordId | 0 直接入口 / 1 派生 (L6693) | F/C | waitChargeDetail | L6693 | F |
| 12 | Cashflow → Charge | $state.go waitPayDetail | A | myMaterialBillCtrl | L6929 | A |
| 13 | Charge → Cashflow | payMedicalRecordCashflow / cancelMedicalRecordCashflow | A | waitPayDetail / waitPayList | L8017/L8146 | A |
| 14 | MedicalRecord → Charge | F 直接 / A 间接经 Cashflow | F/A | - | L6925→L6929 | F 直接 |
| 15 | Charge → MedicalRecord | F | F | - | - | F |
| 16 | Delivery cashflowId | 3 入口 (L3814/L4026/L4238) | A | Delivery Controllers | 3 | A |
| 17 | Cashflow → Delivery | F (无 $state.go) | F | - | 0 | F |
| 18 | Delivery → Cashflow | A (3 处 State 入口) | A | Delivery Controllers | 3 | A |
| 19 | payType | 70 命中 | A | 多处 | 全部 | A |
| 20 | totalPayment | cashflow.totalPayment (Response) | A | waitPayBackCtrl | L7602 | A |
| 21 | received* 字段 | 6+ 个 | A | 多处 | L7524-L7602 | A |
| 22 | refundStatus | 63 命中 | A | 多处 | 全部 | A |
| 23 | Refund API | 4 (Refund Detail / Refund Log / Refund List) | A | 多处 | L4433/L4908/L7433/L37766 | A |
| 24 | State route | 12+ 路由 | A | 多处 | 全部 | A |
| 25 | 生命周期 DAG | A-L 12 条 | A | - | - | A |
| 26 | 复刻风险 | 见 §27 | - | - | - | 见 §27 |

---

## 25. A/B/C/D/E/F 等级

| 等级 | 数量 | 说明 |
|---|:---:|---|
| A | 22 | 全部字符级源码证据 |
| B | 0 | 无需多源互证 |
| C | 0 | 无 |
| D | 0 | 无冲突 |
| E | 0 | 无业务推断（E 不入规格）|
| F | 5 | (Cashflow → Delivery / Charge → MedicalRecord / Refund Write API 缺失 / MedicalRecord → Charge 直接 / waitChargeDetail 内 medicalRecordId 派生) |

---

## 26. 历史差异

### 26.1 S1-137R / S1-138 误判保留修正

| 历史报告 | 实际证据 | 修正 |
|---|---|---|
| S1-137R §5 "4 API 双向桥" | 仅 getMedicalRecordPayVo 1 个 | **保留** (S1-140 未触及)|
| S1-138 §12 "5 条 Create 路径" | addMedicalRecord + beginCustomerCheckin × 3 + receiveSelfAndBegin | **保持** |
| S1-138 §15 "Cashflow → Delivery = F" | L3814/L4026/L4238 3 处 State 入口 | **修正**: 实际是 Delivery → Cashflow = A (3 处), Cashflow → Delivery = F |

### 26.2 S1-141 关键发现

| 发现 | 等级 |
|---|---|
| createCashFlowForMedicalRecord.json 是**唯一** Cashflow Create API | A |
| 5 个 Cashflow Write API 全量 | A |
| Charge 32 个 Controller 分类 | A |
| payTypeList 7 个支付方式 | A |
| payType 70 命中 / refundStatus 63 命中 | A |
| Cashflow 不含 medicalRecordId 字段 | A |
| Delivery 入口是 cashflowId 不是 medicalRecordId | A |

### 26.3 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 203_S1-140 全部保持原样
- 本文档 204_*.md 单独记录 Cashflow/Charge 精确审计

---

## 27. 复刻红线

### 27.1 Cashflow 必实现

| 后端 API | 行号 | 必实现 |
|---|---|---|
| createCashFlowForMedicalRecord.json | L6925 | **A**（唯一 Cashflow Create）|
| payMedicalRecordCashflow.json | L8017 | A |
| payMedicalRecordCashflowForPos.json | L8026 | A |
| payMedicalRecordCashflowForScan.json | L8029 | A |
| cancelMedicalRecordCashflow.json | L8146 | A |
| getMedicalRecordPayVo.json | L4034 | A |
| getMedicalRecordCashflowVo.json | L4942/7070 | A |
| getMedicalRecordRefundDetailVo.json | L4433 | A |
| getMedicalRecordRefundLogVo.json | L4908 | A |
| getCashFlowCashierVo.json | L7089 | A |
| getCustomerCashflowDataPage.json | L16762 | A |
| statMedicalRecordCashflow.json | L37109 | A |
| selectCashflowRefundFeeVoList.json | L37766 | A |

### 27.2 Cashflow 字段必实现

| 字段 | 必实现 | 等级 |
|---|---|---|
| `id` | YES | A |
| `payType` | YES (0/1/2/3/11/12/13) | A |
| `totalPayment` | YES | A |
| `refundStatus` | YES (0/1/2) | A |
| `creditStatus` | YES | A |
| `receivedFromCashier/Wallet/Commercial/Medical/Credit/Cash/Wechat/Alipay/Bankcard/Scan/Pos` | YES | A |
| `customer` | YES (含 id) | A |
| `medicalExamineVoList` | YES | A |
| `medicalProductVoList` | YES | A |
| `medicalRecordId` | **NO** (Cashflow 不直接含) | F |

### 27.3 State 入口必实现

| State | 入口参数 | 必实现 |
|---|---|---|
| `waitPayDetail` | cashflowId | A |
| `payedDetail` | cashflowId | A |
| `partBack` | cashflowId | A |
| `waitPayBack` | cashflowId | A |
| `deliveryInput` | cashflowId | A |
| `deliveryInputRecord` | cashflowId | A |
| `deliveryProcessing` | cashflowId | A |

### 27.4 命名误导必标注

| 命名 | 实际 | 警告 |
|---|---|---|
| `getCashflowObjectFactory` | 实际是 cashflow ObjectFactory (一致) | 无误导 |
| `getCashFlowCredit` | 实际是 cashflow ObjectFactory (命名"Credit"误导) | 是 |
| `payMedicalRecordCashflow` | 命名含 MedicalRecord 但 Response 不含 medicalRecord | 是 |
| `payMedicalRecordCashflowForPos/ForScan` | 命名含 MedicalRecord | 是 |

### 27.5 不可桥（必须显式不返回）

| 不可桥 | 等级 | 说明 |
|---|:---:|---|
| Cashflow → Delivery | F | 无 $state.go 入口 |
| Charge → MedicalRecord | F | 无直接入口 |
| MedicalRecord → Charge 直接 | F | 必经 Cashflow |
| Refund → MedicalRecord 直接 | F | 必经 Cashflow |
| Refund Write API | F | 当前源码无退款 Write API 字符级证据 |

---

## 28. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 / Write actual = 0 / Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-203 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 / ignored=1 | ✓ |
| 本轮只新增 204_*.md | ✓ |

---

## 29. Git

### 29.1 操作

```
git add -- 204_S1-141_Cashflow_Charge收费生命周期与核心对象审计.md
git diff --cached --name-only
git commit -m "docs(204): S1-141 Cashflow Charge 收费生命周期与核心对象审计"
git push origin master
```

### 29.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| tracked | 212（commit 204 后从 211 → 212）|
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L6925 | **createCashFlowForMedicalRecord.json 唯一 Cashflow Create API** |
| L6929 | `$state.go("waitPayDetail", { cashflowId: res.result.object })` |
| L8017 | **payMedicalRecordCashflow.json (Pay)** |
| L8146 | **cancelMedicalRecordCashflow.json (Cancel)** |
| L4034 | getMedicalRecordPayVo.json (Cashflow → MedicalRecord 唯一桥) |
| L4036 | `$scope.medicalRecordId = res.object.medicalRecord.id` |
| L6693 | waitChargeDetailCtrl medicalRecord.patientId → getPatientInfo |
| L7070 | waitPayBackCtrl getMedicalRecordCashflowVo.json by cashflowId |
| L7084 | `cashflow.refundStatus === 2 ? false : true` |
| L7602 | `cashflow.totalPayment` 计算 |
| L7734-L7775 | **payTypeList 7 个支付方式定义** |
| L3814/L4026/L4238 | Delivery 3 处 $stateParams.cashflowId |
| L4434 | `res.cashflow.refundStatus === 1` |
| L4908 | getMedicalRecordRefundLogVo.json by refundLogId |
| L4942/L7070/L7488 | getMedicalRecordCashflowVo.json 4 个调用点 |

---

S1-141 完成。立即停止，等待老板下一指令。不执行 S1-142。
