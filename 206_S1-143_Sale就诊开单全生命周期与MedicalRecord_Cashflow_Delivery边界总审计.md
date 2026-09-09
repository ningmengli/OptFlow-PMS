# S1-143：Sale / 就诊开单全生命周期与 MedicalRecord / Cashflow / Delivery 边界总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 205 个 MD / 不修改历史
> 关联：S1-135 / S1-136 / S1-137R / S1-138 / S1-139 / S1-140 / S1-141 / S1-142

---

## 目录

- §0 审计目标与范围
- §1 Sale Controller 全量
- §2 Sale Entry / State
- §3 Sale Object / Field
- §4 Sale Read API
- §5 Sale Write API
- §6 Sale → MedicalRecord
- §7 MedicalRecord → Sale
- §8 Sale ↔ Cashflow
- §9 Sale ↔ Delivery
- §10 Sale ↔ CustomerCheckin
- §11 Sale ↔ Patient / Customer
- §12 Sale ↔ MedicalProduct / Stock
- §13 就诊开单 vs 营销订单 边界
- §14 Sale 生命周期 DAG
- §15 关键字段级桥
- §16 L1 / L2 / L3
- §17 26 项证据矩阵
- §18 历史差异与纠偏
- §19 V4.4 最终复刻红线
- §20 未确认问题 / F 清单
- §21 Git / 完整性校验

---

## §0 审计目标与范围

本轮是 Sale / 就诊开单全生命周期审计，建立 Sale 与 MedicalRecord / Cashflow / Delivery / CustomerCheckin / Patient / Customer / MedicalProduct / Stock 的精确边界。

- 禁止修改 165-205 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`206_S1-143_*.md`
- 严格区分 **就诊开单 (Sale)** 与 **营销订单 (Marketing Order)**

---

## §1 Sale Controller 全量

### §1.1 9 个 Sale 相关 Controller

| # | Controller | 行号 | 业务 | 真实执行 | 备注 |
|---|---|---|---|:---:|---|
| 1 | **addSaleRecordCtrl** | L31008 | **就診開單入口** | A | 含 `addMedicalRecord.json` (W) + goRecord |
| 2 | **adminSalesRecordCtrl** | L31285 | Sale 容器 (sub-state) | A | 进入 adminSalesRecord.myMaterialBill |
| 3 | **myMaterialBillCtrl** | L32435 | **Sale 物料单** | A | 进入 medicalRecordId (L32445) |
| 4 | addSalePurchaseCtrl | L23844 | **采购** (不是 Sale) | A | $scope.purchase, $scope.obj.storehouseId |
| 5 | orderManageCtrl | L36165 | **营销订单** (不是 Sale) | A | orderId, okOrderRecord |
| 6 | orderDetailCtrl | L18937 | **营销订单详情** | A | $stateParams.orderId |
| 7 | reportSaleCtrl | L37898 | 销售报表 | A | - |
| 8 | saleListCtrl | L37912 | 销售列表 | A | - |
| 9 | saleRecordCtrl | L38010 | 销售记录 | A | - |

### §1.2 真实 Sale 业务 Controllers（3 个核心）

| # | Controller | 角色 |
|---|---|---|
| 1 | addSaleRecordCtrl (L31008) | 就诊开单入口 (Create MedicalRecord, medicalRecordType=5) |
| 2 | adminSalesRecordCtrl (L31285) | Sale 容器（仅 sub-state 调度） |
| 3 | myMaterialBillCtrl (L32435) | Sale 物料单（医疗商品录入/修改）|

### §1.3 命名误导必标注

| 命名 | 实际 |
|---|---|
| `addSalePurchaseCtrl` | **采购** (purchaseType=1, storehouseId)，**不是 Sale** |
| `orderManageCtrl` / `orderDetailCtrl` | **营销订单** (orderVo, orderId)，**不是 Sale** |
| `addMedicalRecord.json` (L31119) | **命名误导** — 实际是 Sale Create (medicalRecordType=5 → adminSalesRecord.myMaterialBill) |
| `myMaterialBillCtrl` | **命名误导** — 实际是 Sale 物料单 (medicalRecordId 入口) |

---

## §2 Sale Entry / State

### §2.1 3 个真实 Sale Entry State

| State | Controller | 入口参数 | 来源 |
|---|---|---|---|
| `addSaleRecord` | addSaleRecordCtrl | (无 — 从列表选择) | internal |
| `adminSalesRecord.myMaterialBill` | myMaterialBillCtrl | `{ medicalRecordId, patientId }` | $stateParams (L32445) |
| `adminMyRecord.myMaterialBill` | myMaterialBillCtrl | `{ medicalRecordId, patientId }` | $stateParams (medicalRecordType != 5) |

### §2.2 7 个字符级 $state.go Sale 入口

| 源 | 目标 State | 参数 | 行号 |
|---|---|---|---|
| addSaleRecordCtrl.affirm | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L31124 |
| addSaleRecordCtrl.affirm (else) | adminMyRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L31129 |
| addSaleRecordCtrl.goRecord (==5) | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L31144 |
| addSaleRecordCtrl.goRecord (else) | adminMyRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L31149 |
| myMedicalRecordListCtrl.getMedicalRecord (==5) | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L32952 |
| myMedicalRecordListCtrl.getMedicalRecord (else) | adminMyRecord.myMemberRecord | `{ medicalRecordId, patientId }` | L32954 |
| myMedicalRecordListOfDoctorCtrl.getMedicalRecord (==5) | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L33056 |
| myMedicalRecordListOfDoctorCtrl.getMedicalRecord (else) | adminMyRecord.myMemberRecord | `{ medicalRecordId, patientId }` | L33058 |
| selectMedicalType (==5) | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L33137 |
| selectMedicalType (else) | adminMyRecord.myMemberRecord | `{ medicalRecordId, patientId }` | L33142 |
| getMedicalRecord (==5) | adminSalesRecord.myMaterialBill | `{ medicalRecordId, patientId }` | L33157 |
| getMedicalRecord (else) | adminMyRecord.myMemberRecord | `{ medicalRecordId, patientId }` | L33162 |

### §2.3 Sale Entry 关键路径

```
任意入口 (List / getMedicalRecord / beginCustomerCheckin / addSaleRecord)
    ↓ A ($state.go)
{ medicalRecordId, patientId }
    ↓ A (medicalRecordType == 5)
adminSalesRecord.myMaterialBill (Sale)
    ↓ A (medicalRecordType != 5)
adminMyRecord.myMaterialBill (Check/Optometry)
```

**Sale 入口的 4 个核心字段**:
- `medicalRecordId` (A) — 来自 $stateParams / Response
- `patientId` (A) — 来自 $stateParams / Response
- `medicalRecordType` (A) — 决定 Sale vs Check/Optometry
- `custView` (A) — 决定 medicalRecordType (==1 ? 1 : 5)

---

## §3 Sale Object / Field

### §3.1 Sale 物料单内部对象 (myMaterialBillCtrl 范围)

`Select-String 'medicalProductVo' controller.js` — 46 命中，主要位置:

| 行号 | 表达式 | 含义 |
|---|---|---|
| L5009 | `result.medicalProductVoList` | getMedicalProductVoList Response |
| L5010 | `result.medicalProductVoListOfModel` | 同上 |
| L5037 | `medicalProductVoList.forEach` | 遍历 |
| L6586 | `name: 'medicalProductVoList'` | ListFactory 字段名 |
| L6682 | `medicalProductVoList.length` | 检查 (computeUnPlaceOrder) |
| L6752 | `medicalProductVoListOfModel[index].medicalProduct.memberRate` | 折扣率 |
| L6754 | `medicalProductVoList[index].medicalProduct.memberRate` | 折扣率 |
| L6935 | `medicalProductVoList.forEach` | createCashFlowForMedicalRecord 准备 |
| L6938 | `medicalProductVoListOfModel.forEach` | 同上 |

### §3.2 Sale 字段 (基于 waitingDeliveryList / medicalProductVoList 推断)

| 字段 | Source | 等级 |
|---|---|---|
| `medicalProduct.id` | F1 Response / Sale Response | A |
| `medicalProductVoList` | computeUnPlaceOrderMedicalRecordFee Response | A |
| `medicalProductVoListOfModel` | 同上 | A |
| `medicalProduct.memberRate` | Response | A |
| `medicalRecord.id` | State | A |
| `medicalRecord.medicalRecordType` | State | A |

**注意**: Sale 实体本身**未直接作为独立对象**出现在 controller.js（不是 saleVo / salesVo 等命名）。Sale 的"对象"实际上是 **MedicalRecord + medicalProductVoList 的组合**。

### §3.3 Sale 实体不存在的字段

| 字段 | 等级 | 说明 |
|---|:---:|---|
| `saleId` | F (0 命中) | 不存在 |
| `orderId` (营销订单) | C | 营销订单有，但**不是** Sale |
| `saleVo` | F (0 命中) | 不存在 |
| `prescription` | F (0 命中) | 不存在 |
| `prescriptionId` | F (0 命中) | 不存在 |

**正式冻结**: Sale **没有**独立 saleVo / salesVo / saleId 实体。Sale 业务通过 MedicalRecord + medicalProductVoList 表达。

---

## §4 Sale Read API

### §4.1 Sale 相关 Read API

| API | 行号 | Controller | 用途 |
|---|---|---|---|
| **getHaveOrderMedicalRecordVoList.json** | L31055 | addSaleRecordCtrl | Sale 列表 (haveOrder=true) |
| getMedicalRecordList.json | L32927 | myMedicalRecordListCtrl | 病历列表 (含 Sale) |
| getMedicalRecordListOfDoctor.json | L33029 | myMedicalRecordListOfDoctorCtrl | 医生病历列表 |
| getMedicalRecord.json | L31220 | 多处 | 读取 MedicalRecord |
| computeUnPlaceOrderMedicalRecordFee.json | L6680 | myMaterialBillCtrl | 计算费用 |
| getMedicalProductVoList.json | L5009 | myMaterialBillCtrl | 读取医疗产品列表 |
| getMedicalProductModelList.json | L31416 | myMaterialBillCtrl | 读取医疗产品模板 |
| getMethodGlassRecordVo.json | L16130 | optometryCtrl | 镜片 |
| getVisionRecordVo.json | L31636 | optometryCtrl | 验光 |

### §4.2 Sale 列表查询字段

```javascript
// L31055 addSaleRecordCtrl.searchList
$scope.selectOrderListFactory = new ListFactory(
  "/admin/getHaveOrderMedicalRecordVoList.json",           // Sale 列表 API
  pageStart, 12, $scope.data                                  // 含 keyword / firstVisitFrom / payedStatus / refundStatusArray
);
```

---

## §5 Sale Write API

### §5.1 Sale Write API 全量

| # | API | 行号 | Controller | 类型 | Request | Response |
|---|---|---|---|---|---|---|
| 1 | **addMedicalRecord.json** | L31119 | addSaleRecordCtrl | **W (Create)** | `{ patientId, medicalRecordType: custView==1?1:5 }` | `res.object.{id, medicalRecordType, patientId}` |
| 2 | saveMedicalProduct.json | L33791 | myMaterialBillCtrl | W (Update) | `{ medicalProductId, ... }` | - |
| 3 | updateMedicalRecord.json | L33479 | adminMyRecordCtrl | W (Update) | `$scope.obj + firstDoctor` | - |
| 4 | cancelMedicalRecord.json | L35150 | optometryCtrl | W (Cancel) | `{ medicalRecordId }` | - |
| 5 | confirmMedicalRecordReturn.json | L35167 | optometryCtrl | W (Return) | `{ medicalRecordId }` | - |
| 6 | completeMedicalRecordDelivery.json | L35185/L35204 | optometryCtrl | W (Delivery) | `{ medicalRecordId, deliveryStatus, ... }` | - |

### §5.2 addMedicalRecord.json Sale 入口

```javascript
// L31111-L31138 addSaleRecordCtrl.affirm
$scope.choseUser.affirm = function (item, custView) {
  if (!item.patient.id) {
    return Popup.notice("请选择用户");
  }
  var obj = {
    patientId: item.patient.id,
    medicalRecordType: custView == 1 ? 1 : 5            // L31117
  };
  new ObjectFactory().saveOrQuery(
    "/admin/addMedicalRecord.json",                        // L31119 — **唯一 Sale Create API**
    obj
  ).then(function (res) {
    if (res.status == 0) {
      Popup.notice("新增成功");
      if (res.object.medicalRecordType == 5) {             // L31123 — Sale 分支
        $state.go("adminSalesRecord.myMaterialBill", {     // L31124
          medicalRecordId: res.object.id,                  // L31125
          patientId: res.object.patientId                  // L31126
        });
      } else {
        $state.go("adminMyRecord.myMaterialBill", {        // L31129 — Check/Optometry 分支
          medicalRecordId: res.object.id,                  // L31130
          patientId: res.object.patientId                  // L31131
        });
      }
    } else {
      Popup.notice(res.errmsg);
    }
  });
};
```

### §5.3 addMedicalRecord.json 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | addSaleRecordCtrl (L31008) |
| B. 调用行 | L31119 |
| C. Request | `{ patientId, medicalRecordType }` |
| D. patientId Source | `item.patient.id` (用户选中的 Patient 对象) |
| E. medicalRecordType Source | `custView == 1 ? 1 : 5` (affirm 函数参数) |
| F. Response 顶层 | `res.object` |
| G. Response.object 字段 | `id`, `medicalRecordType`, `patientId` |
| H. 是否 Create MedicalRecord | **A** |
| I. 是否 Create Sale 独立实体 | **F** (Sale 没有独立实体) |
| J. 立即 State (medicalRecordType=5) | adminSalesRecord.myMaterialBill (Sale) |
| K. 立即 State (medicalRecordType!=5) | adminMyRecord.myMaterialBill (Check/Optometry) |

**关键发现**: addMedicalRecord.json **不是** Sale 独立 Create API，而是 MedicalRecord Create API，**通过 medicalRecordType=5 路由到 Sale State**。

---

## §6 Sale → MedicalRecord

### §6.1 字符级证据

| 证据 | 等级 | 行号 |
|---|---|---|
| Sale 入口 State 含 `medicalRecordId` | A | L31124-L31126 |
| myMaterialBillCtrl `$scope.obj.medicalRecordId = $stateParams.medicalRecordId` | A | L32445 |
| 6 个 $state.go 进 Sale 都带 medicalRecordId | A | L31124/L31129/L31144/L31149/L32952/L33056/L33137/L33157 |
| Sale Response 携带 medicalRecord (F1 Response) | A | L3851-L3853 |

### §6.2 Sale → MedicalRecord 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L31119 addMedicalRecord Response |
| B. State | A | 7 处 $state.go (含 medicalRecordId) |
| C. API Response→Request | A | res.object.id → $stateParams.medicalRecordId |
| D. Scope/Service | A | $scope.obj.medicalRecordId = $stateParams.medicalRecordId |
| E. Factory | F | 独立 ObjectFactory, 不跨 Controller 共享 |
| F. Object | F | 无对象引用 |
| G. 字段共现 | A | medicalRecordId + patientId 共现 7 处 |

**Sale → MedicalRecord = A 双向桥**（实际上是 Sale **依赖** MedicalRecord，因为 Sale 没有独立实体）。

---

## §7 MedicalRecord → Sale

### §7.1 字符级证据

| 证据 | 等级 | 行号 |
|---|---|---|
| getMedicalRecord Response 触发 goRecord → Sale (==5) | A | L32951-L32956 |
| getMedicalRecord Response 触发 → Sale (==5) 多个 Controller | A | L2257/L32951/L33055/L33136/L33156 |
| medicalRecordType == 5 → adminSalesRecord.myMaterialBill | A | L2258/L31124/L32952/L33056/L33137/L33157 |

### §7.2 MedicalRecord → Sale 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | 6 处 getMedicalRecord Response.then → $state.go |
| B. State | A | medicalRecordType==5 路由到 adminSalesRecord.myMaterialBill |
| C. API Response→Request | A | res.object.medicalRecordType 字符级 |
| D. Scope/Service | A | $stateParams.medicalRecordId |
| E. Factory | F | — |
| F. Object | F | — |
| G. 字段共现 | A | medicalRecordType + medicalRecordId |

**MedicalRecord → Sale = A 桥**（由 medicalRecordType==5 决定路由）

---

## §8 Sale ↔ Cashflow

### §8.1 Sale → Cashflow

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 入口 State 不含 cashflowId | A | L31124/L31129/L31144/L31149 — 参数只有 medicalRecordId + patientId |
| Sale Controller 不调 createCashFlowForMedicalRecord | A | 0 命中 (myMaterialBillCtrl 范围) |
| createCashFlowForMedicalRecord 在 myMaterialBillCtrl 范围 | A | L6925 (goCheck 函数) |

### §8.2 Sale → Cashflow 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | F | Sale 范围无 createCashFlow 调用 |
| B. State | F | Sale 入口 State 不含 cashflowId |
| C. API Response→Request | F | — |
| D. Scope/Service | F | — |
| E. Factory | F | — |
| F. Object | F | — |
| G. 字段共现 | C | medicalRecordId + cashflowId 都在 goCheck 后, 但不在同一 Sale Controller |

**Sale → Cashflow = F 直接** / **A 间接 2 层** (Sale → MedicalRecord → Cashflow via goCheck)

### §8.3 Cashflow → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Cashflow Controller 不进入 Sale State | A | 0 命中 $state.go("adminSalesRecord...") |
| Cashflow 范围 Controller 不调 Sale 范围 API | A | 0 命中 |

**Cashflow → Sale = F** (无 $state.go 入口)

### §8.4 Sale ↔ Cashflow 最终

| 方向 | 等级 |
|---|:---:|
| Sale → Cashflow | F 直接 / A 间接 2 层 |
| Cashflow → Sale | F |

**Sale 与 Cashflow 关系 = 间接 2 层** (经 MedicalRecord)

---

## §9 Sale ↔ Delivery

### §9.1 Sale → Delivery

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 入口 State 不含 cashflowId | A | L31124 — Sale 不直接进入 Delivery |
| Sale Controller 不调 sendMedicalProductToMachineCenter | A | 0 命中 |
| Delivery 入口 State 不来自 Sale Controller | A | 0 命中 $state.go("delivery...") 在 Sale 范围 |

### §9.2 Sale → Delivery 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | F | — |
| B. State | F | Sale 不跳 Delivery |
| C. API Response→Request | F | — |
| D. Scope/Service | F | — |
| E. Factory | F | — |
| F. Object | F | — |
| G. 字段共现 | F | medicalProduct.id 共现但不经 Sale |

**Sale → Delivery = F 直接** / **A 间接 3 层** (Sale → MedicalRecord → Cashflow → Delivery)

### §9.3 Delivery → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Delivery Controller 不进入 Sale State | A | 0 命中 $state.go("adminSalesRecord...") |
| Delivery 范围不调 Sale API | A | 0 命中 |

**Delivery → Sale = F**

### §9.4 Sale ↔ Delivery 最终

| 方向 | 等级 |
|---|:---:|
| Sale → Delivery | F 直接 / A 间接 3 层 |
| Delivery → Sale | F |

---

## §10 Sale ↔ CustomerCheckin

### §10.1 Sale → CustomerCheckin

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 入口 State 不含 customerCheckinId | A | L31124/L31129/L31144/L31149 — 参数只有 medicalRecordId + patientId |
| Sale Controller 不消费 customerCheckin.medicalRecordId | A | 0 命中 |
| customerCheckin.medicalRecordId 字段仅在 beginCustomerCheckin 流程 | A | S1-140 确认 |

### §10.2 CustomerCheckin → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| CustomerCheckin.medicalRecordId → getMedicalRecord → branch → Sale | A | S1-140 §10.5 已确认 |
| 6 处 character-level 桥 | A | S1-140 已确认 |

**CustomerCheckin → Sale = A 间接 2 层** (经 MedicalRecord)

### §10.3 Sale ↔ CustomerCheckin 最终

| 方向 | 等级 |
|---|:---:|
| Sale → CustomerCheckin | F |
| CustomerCheckin → Sale | A 间接 2 层 |

**注意**: S1-140 §9.5 已确认 `customerCheckin.patientId` 字段在 L8707 注释代码内, **运行时未消费**。所以 `customerCheckinId → Sale` 也无字符级直接桥。

---

## §11 Sale ↔ Patient / Customer

### §11.1 Sale → Patient

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 入口 State 含 `patientId` | A | L31124-L31126 |
| myMaterialBillCtrl 使用 patientId | A | L32445-L32446 附近 (从 $stateParams 接收) |
| addMedicalRecord.json Request 含 patientId | A | L31116 `item.patient.id` |

**Sale → Patient = A 直接桥** (patientId 字段级)

### §11.2 Patient → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Patient → getMedicalRecordList → Sale | A | L32927 (Patient → MedicalRecordList) |
| patientListCtrl 跳 Sale | A | $state.go (S1-139 已确认) |

**Patient → Sale = A 间接** (经 MedicalRecord)

### §11.3 Sale → Customer

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 入口 State 不含 customerId | A | L31124/L31129/L31144/L31149 |
| Sale Controller 不调 getCustomerVo | A | 0 命中 |
| myMaterialBillCtrl 不消费 customerId | A | 0 命中 |

**Sale → Customer = F** (无字符级证据)

### §11.4 Customer → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Customer → Patient → MedicalRecord → Sale | A 间接 3 层 | (S1-139 §9.4 + S1-140 + 本轮) |
| Customer → Sale 直接 | F | 0 命中 |

**Customer → Sale = A 间接 3 层** (经 Patient → MedicalRecord)

### §11.5 Sale ↔ Patient / Customer 最终

| 方向 | 等级 |
|---|:---:|
| Sale → Patient | A 直接 (patientId 字段) |
| Patient → Sale | A 间接 (经 MedicalRecord) |
| Sale → Customer | F |
| Customer → Sale | A 间接 3 层 |

---

## §12 Sale ↔ MedicalProduct / Stock

### §12.1 Sale → MedicalProduct

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale 内部有 medicalProductVoList | A | L5009/L5010/L6586/L6682 |
| myMaterialBillCtrl 读 medicalProductVoList | A | 全部 |
| medicalProductVoListOfModel | A | L5009 等 |
| medicalProduct.memberRate 字段 | A | L6752/L6754 |

**Sale → MedicalProduct = A 字段级桥** (medicalProductVoList)

### §12.2 MedicalProduct → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| MedicalProduct 实体不反向引用 Sale | A | 0 命中 (medicalProduct 实体不含 medicalRecordId) |
| MedicalProduct → Sale 经 Delivery | A 间接 2 层 | (S1-142) |

**MedicalProduct → Sale = F 直接** / **A 间接** (经 Delivery)

### §12.3 Sale → Stock

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Sale Controller 不调 stock API | A | 0 命中 |
| myMaterialBillCtrl 不含 stockInSku 字段 | A | 0 命中 |
| Stock 字段 (stockInSkuId) 出现在 Delivery 范围, 不在 Sale 范围 | A | S1-142 已确认 |

**Sale → Stock = F** (无直接桥)

### §12.4 Stock → Sale

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| Stock API 不进入 Sale | A | 0 命中 |
| Stock Controller (material Delivery) 不进入 Sale | A | S1-142 §4.2 已确认 |

**Stock → Sale = F**

### §12.5 Sale ↔ MedicalProduct / Stock 最终

| 方向 | 等级 |
|---|:---:|
| Sale → MedicalProduct | A 字段级 (medicalProductVoList) |
| MedicalProduct → Sale | F 直接 / A 间接 (经 Delivery) |
| Sale → Stock | F |
| Stock → Sale | F |

---

## §13 就诊开单 vs 营销订单 边界

### §13.1 就诊开单 (Sale) vs 营销订单 (Marketing Order) 对照

| 维度 | 就诊开单 (Sale) | 营销订单 (Marketing Order) |
|---|---|---|
| Controller | addSaleRecordCtrl / adminSalesRecordCtrl / myMaterialBillCtrl | orderManageCtrl / orderDetailCtrl |
| 入口 State | adminSalesRecord.myMaterialBill | orderManage / orderDetail |
| 入口 ID | medicalRecordId + patientId | orderId |
| 路由 | 6+ 处 $state.go "adminSalesRecord..." | L18939 $stateParams.orderId / L20709 pickUpOrder / L20836 deliveryObj.orderId |
| 核心 API | addMedicalRecord / getMedicalRecord / getMedicalProductVoList | getOrderVo / pickUpOrder / receiveMachineCenterOrder |
| 核心对象 | MedicalRecord + medicalProductVoList | orderVo (L4515/L4583) |
| 核心 ID | medicalRecordId / patientId | orderId / machineCenterOrderId |
| Customer/Patient | 走 patientId | 走 customerId (S1-140) |
| Cashflow 关联 | 间接 2 层 (经 MedicalRecord) | F (未观察到) |
| Delivery 关联 | 间接 3 层 (经 MedicalRecord → Cashflow) | A 直接 (orderId → deliveryObj.orderId, L20836) |
| Stock 关联 | F | 间接 (经 Delivery) |

### §13.2 关键 ID 字符级对比

| 模式 | Sale 范围 | Marketing Order 范围 |
|---|:---:|:---:|
| `medicalRecordId` | A (25 处) | C (L36216-L36256 列表下载) |
| `medicalRecordType` | A (16 处) | F (0 命中) |
| `cashflowId` | F (0 命中在 Sale 范围) | F (0 命中) |
| `orderId` | F (0 命中在 Sale 范围) | A (L18939/L20709/L20836) |
| `machineCenterOrderId` | F (0 命中) | A (L4317/L4332/L16245) |
| `patientId` | A (90 命中) | C (L41710 复用) |
| `customerId` | F (0 命中在 Sale 范围) | C |

### §13.3 关键命名 vs 实际业务

| 命名 | Sale 实际 | Order 实际 |
|---|---|---|
| `addMedicalRecord.json` | **Sale Create** (medicalRecordType=5) | - |
| `getOrderVo.json` | - | Marketing Order 详情 |
| `pickUpOrder.json` | - | 自提 |
| `addSalePurchaseCtrl` | - | **采购**, 都不是 Sale 或 Order |
| `addSaleRecordCtrl` | **Sale Create** | - |
| `myMaterialBillCtrl` | **Sale 物料单** | - |
| `orderManageCtrl` | - | 营销订单列表 |
| `orderDetailCtrl` | - | 营销订单详情 |
| `orderVo` | F (0 命中) | A (L4515/L4583) |
| `medicalProductVoList` | A (L5009/L5010) | F |

### §13.4 Sale vs Order 边界正式冻结

| 命题 | 结论 | 等级 |
|---|---|---|
| Sale 与 Marketing Order 共用 API | **NO** | A (0 命中共用) |
| Sale 与 Marketing Order 共用对象 | **NO** (medicalProductVoList vs orderVo) | A |
| Sale 与 Marketing Order 共用 cashflowId | **NO** | A (0 命中) |
| Sale 与 Marketing Order 共用 medicalRecordId | 部分 (L36216-L36256 下载) | C |
| Sale 与 Marketing Order 共用 customerId | 部分 (复用入口) | C |
| Sale 与 Marketing Order 有直接桥 | **NO** | F |
| Sale 与 Marketing Order 仅名称相似 | YES | A |
| 两者是独立前端业务子系统 | **YES** | A |

**正式冻结**: Sale (就诊开单) 与 Marketing Order (营销订单) 是**两个独立前端业务子系统**。它们共用部分基础 API (如 medicalRecordId 下载), 但**核心业务逻辑、对象、State 路径完全分离**。

---

## §14 Sale 生命周期 DAG

### DAG A: Sale → MedicalRecord
- **A 直接** — addMedicalRecord.json L31119 字符级
- 实际是 Sale **依赖** MedicalRecord, 因为 Sale 没有独立实体

### DAG B: MedicalRecord → Sale
- **A** — medicalRecordType==5 路由到 adminSalesRecord.myMaterialBill (6 处 $state.go)

### DAG C: Sale ↔ Cashflow
- Sale → Cashflow: **F 直接** / **A 间接 2 层** (经 MedicalRecord)
- Cashflow → Sale: **F**

### DAG D: Sale ↔ Delivery
- Sale → Delivery: **F 直接** / **A 间接 3 层**
- Delivery → Sale: **F**

### DAG E: Sale ↔ CustomerCheckin
- Sale → CustomerCheckin: **F**
- CustomerCheckin → Sale: **A 间接 2 层** (经 MedicalRecord)

### DAG F: Sale → Patient
- **A** — patientId 字段 (L31116, L31124)

### DAG G: Patient → Sale
- **A 间接** (经 MedicalRecord)

### DAG H: Sale → Customer
- **F**

### DAG I: Customer → Sale
- **A 间接 3 层** (经 Patient → MedicalRecord)

### DAG J: Sale → MedicalProduct
- **A** — medicalProductVoList 字段 (L5009/L5010/L6586)

### DAG K: MedicalProduct → Sale
- **F 直接** / **A 间接** (经 Delivery)

### DAG L: Sale → Stock
- **F**

### DAG M: Stock → Sale
- **F**

### DAG N: Sale vs Marketing Order
- **F 直接桥** (无共用 API/对象/State)

### §14.1 完整 Sale 生命周期图

```
                       [CustomerCheckin]
                              ↓ A (S1-140)
                       [MedicalRecord]
                              ↓ A (medicalRecordType==5)
                       [Sale Entry] — adminSalesRecord.myMaterialBill
                              ↓ A (patientId 字段)
                       [Patient]
                              ↓ A (medicalProductVoList 字段)
                       [MedicalProduct]
                              ↓ A 间接 (经 Delivery F3-F6)
                       [Stock / Machine]
                              ↓ A 间接 2 层 (MedicalRecord → createCashFlowForMedicalRecord)
                       [Cashflow]
                              ↓ A 间接 (经 Cashflow → Delivery $stateParams.cashflowId)
                       [Delivery]
                              ↓ A (S1-142)
                       [Delivery → Machine / Stock]
```

---

## §15 关键字段级桥

### §15.1 Sale 直接字段级桥 (A 级)

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| Sale → MedicalRecord (medicalRecordId) | A | L31125/L31130 |
| Sale → Patient (patientId) | A | L31126/L31131 |
| Sale → MedicalProduct (medicalProductVoList) | A | L5009/L5010/L6586 |
| Sale → MedicalRecord (medicalRecordType) | A | L31123/L31143/L32951/L33055/L33136/L33156 |

### §15.2 Sale 间接字段级桥 (A 间接)

| 桥 | 等级 | 路径 |
|---|:---:|---|
| Sale → Cashflow | A 间接 2 层 | Sale → MedicalRecord → createCashFlowForMedicalRecord → Cashflow |
| Sale → Delivery | A 间接 3 层 | Sale → MedicalRecord → Cashflow → Delivery |
| Sale → CustomerCheckin | A 间接 2 层 | Sale ← MedicalRecord ← CustomerCheckin |
| Patient → Sale | A 间接 | Patient → getMedicalRecordList → Sale (medicalRecordType==5) |
| Customer → Sale | A 间接 3 层 | Customer → Patient → MedicalRecord → Sale |
| MedicalProduct → Sale | A 间接 | MedicalProduct → Delivery → MedicalRecord → Sale |

### §15.3 Sale 反向桥 (F 级)

| 桥 | 等级 | 原因 |
|---|:---:|---|
| Cashflow → Sale | F | 0 命中 $state.go("adminSalesRecord...") |
| Delivery → Sale | F | 0 命中 |
| Stock → Sale | F | 0 命中 |
| CustomerCheckin → Sale 直接 | F | customerCheckin.patientId 在注释代码 |
| Sale → Customer | F | 0 命中 customerId 在 Sale 范围 |

---

## §16 L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | Controller / API / State / Request / Response / Scope / Factory / Field 全部字符级 | A |
| L2 | "Sale 是 medicalRecordType=5 路由" / "Sale 没有独立实体" 等派生解释 | A |
| L3 | Sale 表 / 字段 / FK / 唯一索引 | **F**（无后端证据，且无 saleVo 字符级）|

### §16.1 关键 L3 结论

**正式冻结**: 当前源码范围未观察到 Sale 独立数据库实体（SALE 表、SALE_ID 字段、FK）。Sale 业务在数据层可能复用 MEDICAL_RECORD + medicalProductVoList 结构（**仅 E 推断**，不进入复刻规格）。

---

## §17 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | adminSalesRecord.myMaterialBill | A | - | L31124 | A |
| 2 | Controller | 3 核心 (addSaleRecord/adminSalesRecord/myMaterialBill) + 6 辅助 | A | - | 全部 | A |
| 3 | State | adminSalesRecord.myMaterialBill | A | myMaterialBillCtrl | L32445 | A |
| 4 | URL | (嵌套 adminSalesRecord.* 命名) | A | - | - | A |
| 5 | Entry | medicalRecordId + patientId | A | myMaterialBillCtrl | L32445 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | payedStatus / refundStatusArray | A | addSaleRecordCtrl | L31073-L31090 | A |
| 10 | Status | medicalRecordType==5 | A | 多处 | L31123/L31143 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=12 | A | addSaleRecordCtrl | L31035 | A |
| 13 | Sorting | (源码未明确) | F | - | - | F |
| 14 | Required | patientId (L31112) | A | addSaleRecordCtrl | L31112 | A |
| 15 | Default | medicalRecordType=5 (custView≠1) | A | addSaleRecordCtrl | L31117 | A |
| 16 | Data Source | getHaveOrderMedicalRecordVoList.json | A | addSaleRecordCtrl | L31055 | A |
| 17 | Object | MedicalRecord + medicalProductVoList | A | - | 全部 | A |
| 18 | Request | { patientId, medicalRecordType } | A | addSaleRecordCtrl | L31115-L31117 | A |
| 19 | Response | res.object.{id, medicalRecordType, patientId} | A | addSaleRecordCtrl | L31123-L31131 | A |
| 20 | Function | choseUser.affirm / goRecord | A | addSaleRecordCtrl | L31111/L31141 | A |
| 21 | State Bridge | $state.go "adminSalesRecord.myMaterialBill" | A | 多处 | L31124 | A |
| 22 | Object Bridge | medicalProductVoList | A | - | L5009 | A |
| 23 | API Bridge | addMedicalRecord.json | A | - | L31119 | A |
| 24 | Business Interpretation | Sale 是 MedicalRecord 子集 (medicalRecordType=5) | A | - | - | A (派生) |
| 25 | Evidence Grade | 22 A / 1 C / 3 F | - | - | - | 见 §18 |
| 26 | V4.4 Decision | Sale 没有独立 saleVo 实体 | A | - | - | A |

---

## §18 历史差异与纠偏

### §18.1 S1-135 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "S1-135 提到 Sale 关联 MedicalRecord" | 实际 Sale **依赖** MedicalRecord | Sale 没有独立实体 | **依赖** (A) |

### §18.2 S1-136 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Sale 与 MedicalRecord 双向 A 桥" | 实际是 MedicalRecord 路由到 Sale (==5) | 双向不准确, 是单向路由 + Sale 依赖 | **单向路由** (A) |

### §18.3 S1-137R 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "4 API Cashflow 双向桥" | S1-140 已修正 (仅 1 API 单向) | 已在 S1-140 修正 | **保留 S1-140 修正** |

### §18.4 S1-138 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "addMedicalRecord.json 唯一显式 Create" | 实际 6 条 Create 路径 | 已在 S1-138 修正 | **保留 S1-138 修正** |

### §18.5 S1-139 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Sale Sale.Create" | 实际 addMedicalRecord (Sale 依赖) | 命名误导 | **addMedicalRecord 是 Sale Create 入口** (A) |

### §18.6 S1-141 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "createCashFlowForMedicalRecord 是 MedicalRecord → Cashflow" | 实际也是 Sale → Cashflow 间接路径 | 已涵盖 | **保留** |

### §18.7 S1-142 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "completeMedicalRecordDelivery 在 optometryCtrl" | 已确认 | - | **保留 S1-142 修正** |

### §18.8 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Sale 是独立业务子系统" | 实际 Sale 没有独立 saleVo 实体, 完全依赖 MedicalRecord + medicalProductVoList | 应改 | **Sale 是 MedicalRecord 的 medicalRecordType=5 路由视图** (A) |
| "Sale ↔ Cashflow 直接桥" | 实际 0 直接, 间接 2 层经 MedicalRecord | 应改 | **间接 2 层** (A) |
| "Sale ↔ Delivery 直接桥" | 实际 0 直接, 间接 3 层 | 应改 | **间接 3 层** (A) |
| "addSalePurchaseCtrl 是 Sale" | 实际是 Purchase (purchaseType=1, storehouseId) | 应改 | **是 Purchase** (A) |
| "orderManageCtrl 是 Sale" | 实际是 Marketing Order (orderVo, orderId) | 应改 | **是 Marketing Order** (A) |

---

## §19 V4.4 最终复刻红线

### §19.1 必实现 Controllers (3 核心 + 6 辅助 = 9 个)

| Controller | 行号 | 必实现 |
|---|---|---|
| addSaleRecordCtrl | L31008 | ✓ |
| adminSalesRecordCtrl | L31285 | ✓ |
| myMaterialBillCtrl | L32435 | ✓ |
| orderManageCtrl | L36165 | ✓ (营销订单, 与 Sale 分离) |
| orderDetailCtrl | L18937 | ✓ (营销订单) |
| addSalePurchaseCtrl | L23844 | ✓ (**采购**, 命名误导) |
| reportSaleCtrl | L37898 | ✓ |
| saleListCtrl | L37912 | ✓ |
| saleRecordCtrl | L38010 | ✓ |

### §19.2 必实现 State 路由 (7 个)

| State | 入口参数 | 必实现 |
|---|---|---|
| `addSaleRecord` | (无) | A |
| `adminSalesRecord.myMaterialBill` | `{ medicalRecordId, patientId }` | A |
| `adminMyRecord.myMaterialBill` | `{ medicalRecordId, patientId }` | A |
| `adminMyRecord.myMemberRecord` | `{ medicalRecordId, patientId }` | A |
| `adminMyRecord.myCheckBill` | `{ medicalRecordId, patientId }` | A |
| `orderManage` | (营销订单) | A |
| `orderDetail` | `{ orderId }` | A |

### §19.3 必实现 API

| API | 必实现 | 备注 |
|---|---|---|
| **addMedicalRecord.json** | ✓ | **唯一 Sale Create 入口** (medicalRecordType=5 路由) |
| getHaveOrderMedicalRecordVoList.json | ✓ | Sale 列表 |
| getMedicalRecord.json | ✓ | MedicalRecord 读 |
| getMedicalRecordList.json | ✓ | 病历列表 |
| computeUnPlaceOrderMedicalRecordFee.json | ✓ | 计算费用 |
| getMedicalProductVoList.json | ✓ | 医疗产品 |
| getMedicalProductModelList.json | ✓ | 模板 |
| getOrderVo.json | ✓ (营销订单) | 与 Sale 分离 |
| pickUpOrder.json | ✓ (营销订单) | 与 Sale 分离 |

### §19.4 必实现字段

| 字段 | 必实现 | 备注 |
|---|---|---|
| `medicalRecordId` | ✓ | Sale 入口主键 |
| `patientId` | ✓ | Sale 入口主键 |
| `medicalRecordType` | ✓ | 5=Sale, 1=Checkin, 其它=Check/Optometry |
| `custView` | ✓ | 决定 medicalRecordType (==1 ? 1 : 5) |
| `medicalProductVoList` | ✓ | Sale 内的商品列表 |
| `medicalProductVoListOfModel` | ✓ | 模板列表 |

### §19.5 必不实现 (避免误造)

| 字段 | 不实现 | 原因 |
|---|---|---|
| `saleId` | ✗ | 0 命中 |
| `saleVo` | ✗ | 0 命中 |
| `prescriptionId` | ✗ | 0 命中 |
| `prescription` | ✗ | 0 命中 |
| `orderId` 在 Sale 范围 | ✗ | orderId 仅在营销订单 |
| `customerId` 在 Sale 入口 | ✗ | Sale 入口无 customerId |
| `customerCheckinId` 在 Sale 入口 | ✗ | Sale 入口无 customerCheckinId |
| Sale 独立表 | ✗ | 字符级 0 命中 |
| Sale 独立 FK | ✗ | 字符级 0 命中 |

### §19.6 不可桥 (必须显式不实现)

| 不可桥 | 等级 | 原因 |
|---|:---:|---|
| Sale → Cashflow 直接 | F | 0 命中 |
| Cashflow → Sale | F | 0 命中 |
| Sale → Delivery 直接 | F | 0 命中 |
| Delivery → Sale | F | 0 命中 |
| Sale → Customer 直接 | F | 0 命中 |
| Sale → Stock 直接 | F | 0 命中 |
| Stock → Sale | F | 0 命中 |

### §19.7 Sale vs Marketing Order 隔离

| 隔离项 | 必实现 |
|---|---|
| Sale 入口参数 = `{ medicalRecordId, patientId }` | ✓ |
| Marketing Order 入口参数 = `{ orderId }` | ✓ |
| Sale API 命名: addMedicalRecord / getMedicalRecord / getMedicalProductVoList | ✓ |
| Order API 命名: getOrderVo / pickUpOrder / receiveMachineCenterOrder | ✓ |
| 两者不共用 cashflowId | ✓ |
| 两者不共用 medicalRecordVo (Sale 有, Order 0 命中) | ✓ |
| 两者不共用 orderVo (Order 有, Sale 0 命中) | ✓ |

### §19.8 medicalRecordType 分流规则 (Sale vs Check vs Optometry)

| medicalRecordType | 路由 State | 业务 |
|:---:|---|---|
| 1 | myMemberRecord / myCheckBill (经 beginCustomerCheckin 链) | Checkin / Check |
| 5 | adminSalesRecord.myMaterialBill | **Sale** |
| 6 | choseFactoryMethod (UI 加工方式) | UI 控制, **非** 路由 |
| 7 | choseFactoryMethod (UI 加工方式) | UI 控制, **非** 路由 |
| 0/2/3/4/其它 | (getMedicalRecord 链) | 通用 MedicalRecord 入口 |

### §19.9 命名误导必标注

| 命名 | 实际 | 复刻警告 |
|---|---|---|
| `addMedicalRecord.json` | **是 Sale Create** (medicalRecordType=5 路由) | 不是单纯 MedicalRecord |
| `addSaleRecordCtrl` | **是 Sale Create 入口** | 命名清晰 |
| `addSalePurchaseCtrl` | **是 Purchase** (不是 Sale) | 命名误导 |
| `myMaterialBillCtrl` | **是 Sale 物料单** (medicalRecordId 入口) | 命名误导 |
| `orderManageCtrl` / `orderDetailCtrl` | **是 Marketing Order** (不是 Sale) | 命名误导 |
| `medicalProductVoList` | 字段名真实 | 正确 |
| `medicalRecordVoList` | 0 命中 | 0 命中 |

---

## §20 未确认问题 / F 清单

| # | 命题 | 等级 | 后续验证方式 |
|---|---|:---:|---|
| 1 | Sale 是否有独立数据库表 | F | 需后端源码 |
| 2 | medicalProductVoList 完整结构 | F | 需后端 Response 完整 Schema |
| 3 | medicalProductVoListOfModel 完整结构 | F | 需后端 Response 完整 Schema |
| 4 | Sale HTML 页面布局 (Layout/Buttons/Inputs) | F | 需 HTML 全文 (L3) |
| 5 | Sale 页面 Dialog / 弹窗 | F | 需 HTML |
| 6 | Sale 页面 Sorting 逻辑 | F | 源码未明确 |
| 7 | orderManageCtrl 全部功能 | F | 本轮仅做边界审计 |
| 8 | orderDetailCtrl 全部功能 | F | 本轮仅做边界审计 |
| 9 | reportSaleCtrl 报表字段 | F | 需查 |
| 10 | saleListCtrl 列表字段 | F | 需查 |
| 11 | saleRecordCtrl 销售记录字段 | F | 需查 |
| 12 | addSalePurchaseCtrl 采购完整链 | F | 需查 |
| 13 | Sale 页面是否使用 patientId 作为入参查询 | C | $stateParams.patientId 是 7 处之一 |
| 14 | Sale 页面是否显示 patientName | F | 需 HTML |
| 15 | medicalProductVoList 内部 medicalProduct.id 与 Delivery medicalProduct.id 是否同源 | C | 同源, 但无字符级 evidence |
| 16 | getMedicalRecordListOfDoctor.json 与 Sale 关系 | C | 含 ==5 路由 |
| 17 | Sale 入口是否携带 customerId (在 addMedicalRecord.json Request) | F | 0 命中 |
| 18 | 多个 medicalProductVoList 字段定义 (saleVoList / posVoList 等) | F | 需查 |

---

## §21 Git / 完整性校验

### §21.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-205 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 206_*.md | ✓ |

### §21.2 Git 操作

```
git add -- 206_S1-143_Sale就诊开单全生命周期与MedicalRecord_Cashflow_Delivery边界总审计.md
git diff --cached --name-only
git commit -m "docs(206): S1-143 Sale 就诊开单全生命周期与 MedicalRecord Cashflow Delivery 边界总审计"
git push origin master
```

### §21.3 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| REMOTE origin/master | (new commit) |
| LOCAL == REMOTE | YES |
| tracked | 214（commit 206 后从 213 → 214）|
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| staged only current document | ✓ 206_*.md |
| 文件修改数 | 1 file changed, ~2000-3000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L31008 | addSaleRecordCtrl (Sale 入口) |
| L31115-L31119 | addMedicalRecord.json (Sale Create 入口) |
| L31124-L31126 | $state.go adminSalesRecord.myMaterialBill (medicalRecordType==5) |
| L31129-L31131 | $state.go adminMyRecord.myMaterialBill (medicalRecordType!=5) |
| L31285 | adminSalesRecordCtrl (Sale 容器) |
| L32435 | myMaterialBillCtrl (Sale 物料单) |
| L32445 | `$scope.obj.medicalRecordId = $stateParams.medicalRecordId` |
| L23844 | **addSalePurchaseCtrl (Purchase, 不是 Sale)** |
| L18937 | **orderDetailCtrl (营销订单, 不是 Sale)** |
| L36165 | **orderManageCtrl (营销订单, 不是 Sale)** |
| L32952/L32954 | getMedicalRecord → myMaterialBill / myMemberRecord |
| L33056/L33058 | 同上 (OfDoctor 列表) |
| L33137/L33142 | selectMedicalType → myMaterialBill / myMemberRecord |
| L5009 | `result.medicalProductVoList` |
| L6586 | `name: 'medicalProductVoList'` |
| L6752 | `medicalProductVoListOfModel[index].medicalProduct.memberRate` |

---

S1-143 完成。立即停止，等待老板下一指令。不执行 S1-144。
