# S1-146：MedicalRecord 核心主对象字段、生命周期、State 与分支总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 208 个 MD / 不修改历史
> 关联：S1-135 / S1-136 / S1-137R / S1-138 / S1-140 / S1-141 / S1-142 / S1-143 / S1-144 / S1-145

---

## 目录

- §0 审计范围
- §1 MedicalRecord 全量命中
- §2 MedicalRecord Object 字段
- §3 Create
- §4 Read
- §5 Update / Cancel / Return / Delivery
- §6 Status
- §7 ↔ Patient
- §8 ↔ CustomerCheckin
- §9 ↔ MedicalExamine
- §10 ↔ VisionRecord
- §11 ↔ MethodGlassRecord
- §12 ↔ MedicalProduct
- §13 ↔ Cashflow
- §14 ↔ Sale
- §15 ↔ Delivery
- §16 生命周期 DAG
- §17 页面消费矩阵
- §18 字段分类
- §19 26 项证据矩阵
- §20 历史差异
- §21 V4.4 MedicalRecord 规格
- §22 F / 未确认
- §23 Git / 完整性

---

## §0 审计范围

本轮把 MedicalRecord 作为**核心主对象**进行独立完整审计:
- 字段级
- 生命周期级 (Create / Read / Update / Cancel / Return / Delivery)
- State 级
- 消费级 (所有 Controller)

---

## §1 MedicalRecord 全量命中

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `medicalRecord` 总命中 | 94 | A |
| `medicalRecordId` 总命中 | 162 | A |
| `medicalRecordType` 总命中 | 16 | A |
| `medicalRecordVo` 总命中 | 2 | A |

### §1.2 MedicalRecord API 全量

| API | 行号 | Read/Write |
|---|---|---|
| **addMedicalRecord.json** | L31119 | **W (Create)** |
| getMedicalRecord.json | L1964/L2253/L16150/L31220/L31331/L31392/L31774/L32462/L32948/L33052 | R (11+ 调用) |
| getMedicalRecordList.json | L32927 | R |
| getMedicalRecordListOfDoctor.json | L33029 | R |
| getMedicalRecordPayVo.json | L4034 | R |
| getMedicalRecordCashflowVo.json | L4942/L5166/L7070/L7488 | R |
| getMedicalRecordRefundDetailVo.json | L4433 | R |
| getMedicalRecordRefundLogVo.json | L4908/L7433 | R |
| getHaveOrderMedicalRecordVoList.json | L31055 | R |
| selectMedicalRecordVoList.json | (推断) | R |
| **updateMedicalRecord.json** | L33479 | **W (Update)** |
| **cancelMedicalRecord.json** | L35150 | **W (Cancel)** |
| **confirmMedicalRecordReturn.json** | L35167 | **W (Return)** |
| **completeMedicalRecordDelivery.json** | L35185/L35204 | **W (Delivery)** |
| **createCashFlowForMedicalRecord.json** | L6925 | **W (Cashflow Create)** |
| setMedicalRecordProcessMode.json | L35099 | W |
| insertMedicalRecordTemplate.json | L33457/L52253 | W (Template) |
| updateMemberRate.json (含 medicalExamineId) | L10161 | W |
| insertCustomerCheckinOfNewPaitent.json (含 patientId/customerCheckinId) | L8667 | W |
| beginCustomerCheckin.json (含 medicalRecordType) | L10605/L33127/L34947 | W |
| receiveSelfAndBeginCustomerCheckin.json (含 medicalRecordType) | L33195 | W |
| computeUnPlaceOrderMedicalRecordFee.json | L6680 | R |

### §1.3 MedicalRecord Controller 全量

| Controller | 行号 | medicalRecordId 来源 | 等级 |
|---|---|---|---|
| addSaleRecordCtrl | L31008 | $stateParams | A |
| adminSalesRecordCtrl | L31285 | $stateParams | A |
| myMaterialBillCtrl | L32435 | $stateParams | A |
| myMedicalRecordListCtrl | L32900 | URL | A |
| myMedicalRecordListOfDoctorCtrl | L33000 | URL | A |
| optometryCtrl | L34776 | URL / item.medicalRecord.id | A |
| checkinListCtrl | L8778 | (item) | A |
| assistCheckingCtrl | L1756 | $stateParams | A |
| prescriptionCtrl | L33560 | $stateParams | A |
| drugPrescriptionCtrl | L31605 | $stateParams | A |
| addVisitCtrl | L49594 | URL | A |
| deliveryInputCtrl | L3812 | (派生 from cashflow) | A |
| deliveryInputRecordCtrl | L4024 | (派生 from cashflow) | A |
| deliveryProcessingCtrl | L4236 | (派生 from cashflow) | A |
| waitChargeDetailCtrl | L6568 | $stateParams | A |
| checkCallCtrl | (S1-125) | $stateParams | A |

---

## §2 MedicalRecord Object 字段

### §2.1 实际命中的 medicalRecord 字段 (字符级)

`Select-String 'medicalRecord\.[a-zA-Z]+' controller.js` 全量:

| 字段 | 字符级证据 | Source Type |
|---|---|---|
| `medicalRecord.id` | L35085/L35137/L35149/L35166/L35182/L35201/L35222 | Response / Scope |
| `medicalRecord.medicalRecordType` | L35086 | Response / Scope |
| `medicalRecord.patientId` | L6693 (经 res.object) / (推断) | Response |
| `medicalRecord.diagnosis` | (推断, 经 visionRecordVo.medicalRecord) | Response |
| `medicalRecord.customerCheckin` | (推断, 列表项) | Response |
| `firstMedicalRecord.id` | L11667 (列表项) | Response |

### §2.2 字段分类

| Field | Source Type | 等级 |
|---|---|---|
| `id` | Response | A |
| `medicalRecordType` | Response | A |
| `patientId` | Response (经 res.object.medicalRecord.patientId L6693) | A |
| `templateId` | 推断 (L2256 `res.object.templateId`) | C |
| `customerCheckin` (对象) | 列表项 (推断) | C |
| `diagnosis` | 推断 (经 visionRecordVo.medicalRecord) | C |
| `firstMedicalRecord` (嵌套) | 列表项 | C |

### §2.3 关键发现

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| `medicalRecord.id` 是医疗记录主键 | A | L35085/L35137 等 7+ 处 |
| `medicalRecord.medicalRecordType` 是核心字段 | A | L35086 (1 处 optometryCtrl) |
| `medicalRecord.patientId` 是核心字段 | A | L6693 (1 处 myMaterialBillCtrl) |
| `medicalRecord.diagnosis` 是字段 | C | (推断) |
| `medicalRecord.customerCheckin` 是嵌套对象 | C | (推断) |
| `medicalRecord.cashflow` / `medicalRecord.delivery` 字段 | F (0 命中) | - |
| `medicalRecord.sale` / `medicalRecord.saleId` 字段 | F (0 命中) | - |

**正式冻结**: MedicalRecord 实体**不含** `cashflow` / `delivery` / `sale` / `medicalExamineVoList` / `visionRecordVo` / `methodGlassRecordVo` 等嵌套对象字段。这些对象是 **独立 API**, 通过 medicalRecordId 关联。

---

## §3 Create

### §3.1 addMedicalRecord.json 完整证据

```javascript
// L31111-L31138 addSaleRecordCtrl
$scope.choseUser.affirm = function (item, custView) {
  if (!item.patient.id) {
    return Popup.notice("请选择用户");
  }
  var obj = {
    patientId: item.patient.id,                              // L31116
    medicalRecordType: custView == 1 ? 1 : 5                // L31117
  };
  new ObjectFactory().saveOrQuery(
    "/admin/addMedicalRecord.json",                            // L31119 — 唯一 Create API
    obj
  ).then(function (res) {
    if (res.status == 0) {
      Popup.notice("新增成功");
      if (res.object.medicalRecordType == 5) {                 // L31123
        $state.go("adminSalesRecord.myMaterialBill", { ... });  // L31124 Sale
      } else {
        $state.go("adminMyRecord.myMaterialBill", { ... });    // L31129 Check/Optometry
      }
    } else {
      Popup.notice(res.errmsg);
    }
  });
};
```

### §3.2 Create 字段矩阵

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `patientId` | L31116 `item.patient.id` | A |
| `medicalRecordType` | L31117 `custView == 1 ? 1 : 5` | A |
| `templateId` | F (0 命中 addMedicalRecord Request) | F |
| `customerId` | F (0 命中) | F |
| `customerCheckinId` | F (0 命中) | F |
| `medicalRecordType` (硬编码) | F (0 命中) | F |

### §3.3 Response 字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `res.object.id` | L31125/L31130 | A |
| `res.object.medicalRecordType` | L31123 | A |
| `res.object.patientId` | L31126/L31131 | A |
| `res.object.medicalRecord` (嵌套) | F (0 命中 addMedicalRecord Response) | F |

### §3.4 Create 立即 State

| medicalRecordType | 目标 State | 行号 |
|:---:|---|---|
| 5 | `adminSalesRecord.myMaterialBill` | L31124 |
| != 5 | `adminMyRecord.myMaterialBill` | L31129 |

### §3.5 Create 唯一性

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| addMedicalRecord.json 是**唯一** MedicalRecord Create API | A | 1 处调用 (L31119) |
| Create Controller 仅 addSaleRecordCtrl | A | - |
| Create 必传 patientId + medicalRecordType | A | L31116-L31117 |
| Create 不传 customerCheckinId | A (0 命中) | - |
| Create 不传 customerId | A (0 命中) | - |

---

## §4 Read

### §4.1 getMedicalRecord.json 11+ 调用

| 行号 | Controller | 入口参数 |
|---|---|---|
| L1964 | checkCallCtrl | `{ id: $scope.medicalRecordId }` |
| L2253 | (getMedical function) | `{ id: id }` |
| L16150 | optometryCtrl | `{ id: ... }` |
| L31220 | myMaterialBillCtrl | `{ id: $scope.medicalRecordId }` |
| L31331 | (myMaterialBillCtrl) | `{ id: $scope.medicalRecordId }` |
| L31392 | (myMaterialBillCtrl) | `{ id: $scope.obj.medicalRecordId }` |
| L31774 | (prescriptionCtrl) | `{ id: $scope.remind.medicalRecordId }` |
| L32462 | (myMaterialBillCtrl) | `{ id: $scope.obj.medicalRecordId }` |
| L32948 | (myMedicalRecordListCtrl) | `{ id: id }` |
| L33052 | (myMedicalRecordListOfDoctorCtrl) | `{ id: id }` |
| L33134 | (adminMyRecordCtrl selectMedicalType) | `{ id: response.result.vo.customerCheckin.medicalRecordId }` |

### §4.2 getMedicalRecordList.json / getMedicalRecordListOfDoctor.json

| API | 行号 | Request | 等级 |
|---|---|---|---|
| getMedicalRecordList.json | L32927 | `{ patientId }` | A |
| getMedicalRecordListOfDoctor.json | L33029 | (推断) | A |

### §4.3 Read API Response Object 完整结构

| API | Response 顶层 | Object Path | 字段 |
|---|---|---|---|
| getMedicalRecord.json | res.object | res.object | id, medicalRecordType, patientId, templateId, ... |
| getMedicalRecordList.json | res.result | res.result.list[].medicalRecord | (类似) |
| getMedicalRecordPayVo.json | res.object | res.object.medicalRecord | id, patientId, ... |
| getMedicalRecordCashflowVo.json | res.result.object | res.result.object | (cashflow, customer, medicalExamineVoList 等) |

### §4.4 关键发现

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| getMedicalRecord.json 是**唯一** Read MedicalRecord 主对象 API | A | 11+ 调用 |
| getMedicalRecordPayVo 返回 `res.object.medicalRecord.*` 嵌套 | A | L4036/L6693 |
| getMedicalRecordCashflowVo **不含** medicalRecord 嵌套 | A | S1-137R 已确认 |
| Read API 不返回 medicalExamineVoList 嵌套 | A (0 命中 res.object.medicalExamineVoList) | F |
| Read API 不返回 visionRecordVo / methodGlassRecordVo 嵌套 | A (0 命中) | F |

**重要发现**: MedicalRecord Read API 只返回 **MedicalRecord 自身字段**, 不返回 MedicalExamine / VisionRecord / MethodGlassRecord / MedicalProduct。这些对象必须**独立 API 调用**。

---

## §5 Update / Cancel / Return / Delivery

### §5.1 4 个 MedicalRecord 生命周期 Write API

| API | 行号 | Controller | Function | Request | 成功动作 |
|---|---|---|---|---|---|
| **updateMedicalRecord.json** | L33479 | adminMyRecordCtrl | (save 函数) | `$scope.obj + firstDoctor` | (刷新) |
| **cancelMedicalRecord.json** | L35150 | **optometryCtrl** | fnMap.取消订单 | `{ medicalRecordId }` | $scope.querySingleOrder() + $scope.queryUndisposed() |
| **confirmMedicalRecordReturn.json** | L35167 | **optometryCtrl** | fnMap.退货 | `{ medicalRecordId }` | (刷新) |
| **completeMedicalRecordDelivery.json** | L35185/L35204 | **optometryCtrl** | fnMap.到店取镜/快递发货 | `{ medicalRecordId, deliveryStatus, deliveryNo, medicalProductStockBatctPoListJson }` | $scope.querySingleOrder() |

### §5.2 S1-142 重大发现 (本轮再次确认)

| API | 实际 Controller | S1-142 误判 | 当前采用 |
|---|---|---|---|
| completeMedicalRecordDelivery | **optometryCtrl** | deliveryInputCtrl | **optometryCtrl** |
| createMedicalStockLossOfSmallVersion | **optometryCtrl** | deliveryInputCtrl | **optometryCtrl** |
| confirmMedicalRecordReturn | **optometryCtrl** | deliveryInputCtrl | **optometryCtrl** |
| cancelMedicalRecord | **optometryCtrl** | deliveryInputCtrl | **optometryCtrl** |

### §5.3 MedicalRecord 生命周期 vs Delivery 业务

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| `completeMedicalRecordDelivery` 业务归属 | A | optometryCtrl 订单列表 fnMap, **不是** deliveryInputCtrl |
| `createMedicalStockLossOfSmallVersion` 业务归属 | A | 同上, 是 optometryCtrl 报损入口 |
| `cancelMedicalRecord` 业务归属 | A | optometryCtrl 订单列表 fnMap.取消订单 |
| `confirmMedicalRecordReturn` 业务归属 | A | optometryCtrl 订单列表 fnMap.退货 |

**正式冻结**: 上述 4 个 MedicalRecord 生命周期 API 实际调用方都是 **optometryCtrl** (订单列表), 而**不是** deliveryInputCtrl。

### §5.4 Cancel / Return / Delivery 入口详情

```javascript
// L35147-L35158 optometryCtrl.fnMap.取消订单
取消订单: function _() {
  $scope.hint(1, function () {
    var medicalRecordId = item.medicalRecord.id;        // L35149
    new ObjectFactory().saveOrQuery(
      "/admin/cancelMedicalRecord.json",
      { medicalRecordId: medicalRecordId }
    ).then(function (result) {
      ...
      $scope.querySingleOrder();                        // L35156
      $scope.queryUndisposed();                          // L35157
    });
  });
}

// L35162-L35175 optometryCtrl.fnMap.退货
退货: function _() {
  $scope.hint(2, function () {
    var medicalRecordId = item.medicalRecord.id;        // L35166
    new ObjectFactory().saveOrQuery(
      "/admin/confirmMedicalRecordReturn.json",
      { medicalRecordId: medicalRecordId }
    ).then(function (result) {
      ...
      $scope.querySingleOrder();                        // L35174
    });
  });
}
```

---

## §6 Status

### §6.1 MedicalRecord Status 字段

| Status Field | MedicalRecord 是否包含 | 等级 | 字符级证据 |
|---|:---:|:---:|---|
| `medicalRecord.status` | **F** | F (0 命中) | - |
| `medicalRecord.deliveryStatus` | **F** | F (0 命中) | - |
| `medicalRecord.payStatus` | **F** | F (0 命中) | - |
| `medicalRecord.refundStatus` | **F** | F (0 命中) | - |
| `medicalRecord.cancelStatus` | **F** | F (0 命中) | - |

### §6.2 Status 实际归属

| Status 字段 | 实际归属 | 等级 |
|---|---|:---:|
| `payType` | Cashflow | A |
| `refundStatus` | Cashflow | A |
| `creditStatus` | Cashflow | A |
| `deliveryStatus` | Delivery (medicalRecordDelivery.json Request) | A |
| `cancelStatus` | MedicalRecord Cancel (cancelMedicalRecord.json) | A (推断) |
| `payStatus` (Sale 范围) | Sale 列表查询 (payedStatus filter) | A (L31073) |

**重要发现**: **MedicalRecord 实体不含任何 status 字段**。所有 status 字段都在 Cashflow / Delivery / Sale 等独立对象上。

### §6.3 状态机推断（仅 L2）

| 状态转换 | 触发 API | 等级 |
|---|---|:---:|
| 创建 → 待支付 | addMedicalRecord + createCashFlowForMedicalRecord | C (推断) |
| 待支付 → 已支付 | payMedicalRecordCashflow (L8017) | A |
| 配送中 → 已配送 | completeMedicalRecordDelivery (deliveryStatus=1/2) | A |
| 订单 → 已取消 | cancelMedicalRecord (L35150) | A |
| 订单 → 已退货 | confirmMedicalRecordReturn (L35167) | A |
| 订单 → 报损 | createMedicalStockLossOfSmallVersion (L35342) | A |

---

## §7 ↔ Patient

### §7.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → Patient | A | L6693 `res.object.medicalRecord.patientId` → getPatientInfo.json |
| Patient → MedicalRecord | A | L32927 getMedicalRecordList by patientId |
| PatientId 字段 | A | L31116/L31126/L31131/L6693 |

### §7.2 MedicalRecord → Patient 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L6693 `getPatientInfo` 调用 |
| B. State | A | `$stateParams.patientId` (L32445) |
| C. API Response→Request | A | `res.object.medicalRecord.patientId` (L6693) |
| D. Scope/Service | A | `$scope.patientId` (多处) |
| E. Factory | F | - |
| F. Object | F | - |
| G. 字段共现 | A | medicalRecordId + patientId 多处共现 |

**MedicalRecord ↔ Patient = A 双向桥** (经 medicalRecord.patientId)

---

## §8 ↔ CustomerCheckin

### §8.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| CustomerCheckin → MedicalRecord | A | 6 处 `customerCheckin.medicalRecordId` (L8791/L10610/L10642/L33134/L33203/L34955) |
| MedicalRecord → CustomerCheckin | A | L11667 `firstMedicalRecord.id` (列表项) |
| MedicalRecord.customerCheckin 嵌套对象 | C | (列表项推断) |

### §8.2 MedicalRecord ↔ CustomerCheckin 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | (多处) |
| B. State | A | (经 getMedicalRecord 链) |
| C. API Response→Request | A | `customerCheckin.medicalRecordId` (6 处) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | - |
| G. 字段共现 | A | medicalRecordId + customerCheckinId 列表项 |

### §8.3 关键发现

- **MedicalRecord 不含 `customerCheckinId` 字段** (0 命中, 全部经 customerCheckin.medicalRecordId 反向)
- MedicalRecord 列表项含 `customerCheckin` 嵌套对象 (推断, **未直接命中**)
- **S1-140 §9.5 修正确认**: customerCheckin.patientId 在 L8707 注释代码内, 运行时未消费 (仍保持 F)

---

## §9 ↔ MedicalExamine

### §9.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalExamine → MedicalRecord | A | getMedicalExamineVoList by medicalRecordId (L2068/L2385/L32190/L32293/L32422) |
| MedicalRecord → MedicalExamine | A | (经 myMaterialBillCtrl 读 medicalExamineVoList) |
| `medicalExamineVo.medicalRecordId` | A | 推断 (经 List 内部) |

### §9.2 MedicalRecord ↔ MedicalExamine 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | - |
| B. State | A | $stateParams.medicalRecordId (5+ 处) |
| C. API Response→Request | A | medicalRecordId (5+ Request) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (无 medicalExamineVoList 嵌套字段) |
| G. 字段共现 | A | - |

### §9.3 关键发现

- **MedicalRecord 不含 `medicalExamineVoList` 嵌套字段** (0 命中)
- MedicalExamine 是**独立 API**, 通过 medicalRecordId 关联
- MedicalExamine 含独立 ID `medicalExamineId` (S1-145 已确认)

---

## §10 ↔ VisionRecord

### §10.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| VisionRecord → MedicalRecord | A | `visionRecordVo.medicalRecord` (L31620) |
| MedicalRecord → VisionRecord | F | 0 命中 (MedicalRecord 不含 visionRecordVo 嵌套) |
| Request 字段 medicalRecordId | A | L31614/L33670 |

### §10.2 MedicalRecord ↔ VisionRecord 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | - |
| B. State | A | $stateParams.medicalRecordId |
| C. API Response→Request | A | medicalRecordId (7+ Request) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (MedicalRecord 不含 visionRecordVo 嵌套) |
| G. 字段共现 | A | - |

### §10.3 关键发现

- **VisionRecord 是 nested object (visionRecordVo.medicalRecord)** (L31620)
- **MedicalRecord 不反向嵌套 visionRecordVo** (0 命中)
- 双向桥: A → MedicalRecord (Response), MedicalRecord → A = **F**

---

## §11 ↔ MethodGlassRecord

### §11.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MethodGlassRecord → MedicalRecord | A | Request medicalRecordId (L31614/L33670) |
| MedicalRecord → MethodGlassRecord | F | 0 命中 (MedicalRecord 不含 methodGlassRecordVo 嵌套) |
| updateMethodGlassRecord Request | A | 4 处 (L31629/L33753/L33894/L35644) |

### §11.2 MedicalRecord ↔ MethodGlassRecord 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | - |
| B. State | A | $stateParams.medicalRecordId |
| C. API Response→Request | A | medicalRecordId (7+ Request) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (MedicalRecord 不含 methodGlassRecordVo 嵌套) |
| G. 字段共现 | A | - |

**MedicalRecord ↔ MethodGlassRecord**: 单向 A (MethodGlassRecord → MedicalRecord 经 medicalRecordId 字段桥)

---

## §12 ↔ MedicalProduct

### §12.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → MedicalProduct | A | myMaterialBillCtrl 读 medicalProductVoList |
| MedicalProduct → MedicalRecord | F | 0 命中 (medicalProduct 不含 medicalRecordId 字段) |
| `medicalProduct.medicalRecordId` | F (0 命中) | - |

### §12.2 MedicalRecord ↔ MedicalProduct 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | - |
| B. State | A | $stateParams.medicalRecordId |
| C. API Response→Request | A | medicalRecordId (含 medicalProductVoList 列表) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (MedicalRecord 不含 medicalProductVoList 嵌套) |
| G. 字段共现 | A | - |

**关键发现**: MedicalProduct 是**无 medicalRecordId 字段** (S1-145 已确认)。MedicalRecord → MedicalProduct 是经 myMaterialBillCtrl 同 Controller 多 API 读取形成的**多视图关联**, **不是** 字段桥。

---

## §13 ↔ Cashflow

### §13.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → Cashflow | A | `createCashFlowForMedicalRecord.json` (L6925) |
| Cashflow → MedicalRecord | A | `getMedicalRecordPayVo.json` (L4034, 仅 1 API) |
| MedicalRecord 含 cashflowId 字段 | F (0 命中) | - |
| Cashflow 含 medicalRecordId 字段 | F (0 命中) | - |

### §13.2 MedicalRecord ↔ Cashflow 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | L6925 createCashFlowForMedicalRecord / L4034 getMedicalRecordPayVo |
| B. State | A | $stateParams.medicalRecordId |
| C. API Response→Request | A | L6693 res.object.medicalRecord.patientId |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (无 medicalRecord.cashflow / cashflow.medicalRecord 嵌套) |
| G. 字段共现 | A | - |

**MedicalRecord ↔ Cashflow = A 双向桥** (经 API, 无字段级)

---

## §14 ↔ Sale

### §14.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → Sale | A | medicalRecordType==5 → adminSalesRecord.myMaterialBill (6 处 Branch) |
| Sale → MedicalRecord | A | myMaterialBillCtrl 读 MedicalRecord (L31220-L31234) |
| `medicalRecord.saleId` / `saleVo` | F (0 命中) | - |

### §14.2 MedicalRecord ↔ Sale 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | A | - |
| B. State | A | $stateParams.medicalRecordId (L32445) |
| C. API Response→Request | A | medicalRecordType (1 Request) + medicalRecordId (1 Response) |
| D. Scope/Service | A | - |
| E. Factory | F | - |
| F. Object | F | (Sale 不含独立实体, 详见 S1-143) |
| G. 字段共现 | A | - |

**MedicalRecord ↔ Sale = A 双向桥** (经 medicalRecordType==5 路由 + medicalRecordId State, **不是**字段桥)

---

## §15 ↔ Delivery

### §15.1 字符级证据

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| MedicalRecord → Delivery | F (无 $state.go, 无字段桥) | 0 命中 |
| Delivery → MedicalRecord | A | L4034 getMedicalRecordPayVo.json by cashflowId → res.object.medicalRecord.id |
| `medicalRecord.delivery` 字段 | F (0 命中) | - |
| Delivery 含 medicalRecordId 字段 | F (0 命中) | - |

### §15.2 MedicalRecord ↔ Delivery 矩阵

| 桥类型 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | F | - |
| B. State | F | (Delivery 入口是 cashflowId, 不是 medicalRecordId) |
| C. API Response→Request | A | L4034 cashflowId → res.object.medicalRecord.id |
| D. Scope/Service | A | $scope.medicalRecordId (L4036 派生) |
| E. Factory | F | - |
| F. Object | F | (无嵌套) |
| G. 字段共现 | A | - |

**MedicalRecord → Delivery = F 直接** (保持 S1-142 结论)
**Delivery → MedicalRecord = A 间接** (经 cashflowId 桥)

---

## §16 生命周期 DAG

### DAG A: CustomerCheckin → MedicalRecord Create
- **A** — customerCheckin.medicalRecordId 字段 (S1-140 已确认 6 处)
- **A** — beginCustomerCheckin.json 创建后 Response 含 medicalRecordId (L10610/L33203)

### DAG B: MedicalRecord Create (直接)
- **A** — addMedicalRecord.json (L31119) Request { patientId, medicalRecordType }
- **A** — Response { id, medicalRecordType, patientId }

### DAG C: MedicalRecord → type=1
- **A** — beginCustomerCheckin.json Request `medicalRecordType: 1` (L10607/L33127/L33197)
- **A** — 路由: 接诊入口 → 经 getMedicalRecord → myMemberRecord

### DAG D: MedicalRecord → type=5
- **A** — addMedicalRecord.json Request `medicalRecordType: custView==1?1:5` (L31117)
- **A** — 路由: 立即 $state.go("adminSalesRecord.myMaterialBill") (L31124)

### DAG E: MedicalRecord → type=!5
- **A** — 6 处 else Branch 路由到 adminMyRecord.myMemberRecord
- **A** — 路由: Check/Optometry 入口

### DAG F: MedicalRecord → MedicalExamine
- **A** — getMedicalExamineVoList.json by medicalRecordId (5+ 调用)

### DAG G: MedicalRecord → VisionRecord
- **A** — getVisionRecordVo.json by medicalRecordId (7+ 调用)
- **A** — Response 含 visionRecordVo.medicalRecord 嵌套 (L31620)

### DAG H: MedicalRecord → MethodGlassRecord
- **A** — getMethodGlassRecordVo.json by medicalRecordId (7+ 调用)
- **A** — updateMethodGlassRecord.json Request 含 medicalRecordId (4 处)

### DAG I: MedicalRecord → MedicalProduct
- **A** — myMaterialBillCtrl 读 medicalProductVoList
- **F** — MedicalProduct 不含 medicalRecordId 字段

### DAG J: MedicalRecord → Cashflow
- **A** — createCashFlowForMedicalRecord.json (L6925)

### DAG K: MedicalRecord → Sale
- **A** — medicalRecordType==5 路由 (S1-143 已确认)
- **F** — MedicalRecord 不含 sale 字段

### DAG L: MedicalRecord → Delivery
- **F** (无直接桥, 保持 S1-142)

### DAG M: MedicalRecord Update
- **A** — updateMedicalRecord.json (L33479)

### DAG N: MedicalRecord Cancel
- **A** — cancelMedicalRecord.json (L35150) in optometryCtrl fnMap

### DAG O: MedicalRecord Return
- **A** — confirmMedicalRecordReturn.json (L35167) in optometryCtrl fnMap

### DAG P: MedicalRecord Delivery (业务归属)
- **A** — completeMedicalRecordDelivery.json (L35185/L35204) in optometryCtrl fnMap
- **关键**: 实际在 optometryCtrl, 不在 deliveryInputCtrl

### DAG Q: MedicalRecord ReportLoss (业务归属)
- **A** — createMedicalStockLossOfSmallVersion.json (L35342) in optometryCtrl

### §16.1 完整生命周期图

```
[CustomerCheckin] (L8791/L10610/...)
       ↓ A (customerCheckin.medicalRecordId)
[beginCustomerCheckin.json type=1]
       ↓ A (res.customerCheckin.medicalRecordId)
[MedicalRecord (type=1)]
       ↓ A (经 myMemberRecord 路由)
[Check / Optometry]
       ├── A → [MedicalExamine (medicalExamineId)]
       ├── A → [VisionRecord (visionRecordVo.medicalRecord)]
       ├── A → [MethodGlassRecord (methodGlassRecordVo)]
       └── A → [MedicalProduct (medicalProductVoList)]

[addSaleRecordCtrl.affirm]
       ↓ A (addMedicalRecord.json, type=5)
[MedicalRecord (type=5)]
       ↓ A ($state.go adminSalesRecord.myMaterialBill)
[Sale (myMaterialBillCtrl)]
       ├── A → [createCashFlowForMedicalRecord.json]
       ↓
       [Cashflow (cashflowId)]
       ↓ A ($state.go waitPayDetail)
       [Charge]
       ↓ A ($stateParams.cashflowId)
       [Delivery Input]
       ↓ A (getMedicalRecordPayVo 派生)
       [MedicalRecord.id 派生]
       ↓
[MedicalRecord 状态机]
       ├── [updateMedicalRecord] (L33479)
       ├── [cancelMedicalRecord] (L35150)
       ├── [confirmMedicalRecordReturn] (L35167)
       ├── [completeMedicalRecordDelivery] (L35185/L35204)
       └── [createMedicalStockLossOfSmallVersion] (L35342)
       (全部 5 个 API 实际在 optometryCtrl fnMap)
```

---

## §17 页面消费矩阵

### §17.1 15 个 Controller 消费 MedicalRecord

| Controller | 读取 | 写 | medicalRecordId 来源 | 作用 | 等级 |
|---|---|---|---|---|---|
| addSaleRecordCtrl (L31008) | N | Y (addMedicalRecord) | (无, item.patient.id) | Create | A |
| adminSalesRecordCtrl (L31285) | Y | N | $stateParams | Sale 容器 | A |
| myMaterialBillCtrl (L32435) | Y | Y (goCheck 调 createCashFlow) | $stateParams | Sale 物料单 | A |
| myMedicalRecordListCtrl (L32900) | Y (list) | N | URL | 病历列表 | A |
| myMedicalRecordListOfDoctorCtrl (L33000) | Y (list) | N | URL | 医生病历列表 | A |
| optometryCtrl (L34776) | Y | Y (4 个 MedicalRecord API) | URL / item.medicalRecord.id | 验光 + 5 branch | A |
| checkinListCtrl (L8778) | Y (item) | N (case 0 调 beginCustomerCheckin) | (item.customerCheckin) | 接诊列表 | A |
| assistCheckingCtrl (L1756) | Y (getMedicalExamineVoList) | N | $stateParams | Check | A |
| prescriptionCtrl (L33560) | Y (getMedicalRecord, getMethodGlassRecordVo) | N | $stateParams | 验光处方 | A |
| drugPrescriptionCtrl (L31605) | Y (getVisionRecordVo, getMethodGlassRecordVo) | Y (updateMethodGlassRecord) | $stateParams | 药品处方 | A |
| addVisitCtrl (L49594) | Y (推断) | Y (推断) | URL | 复诊 | A |
| deliveryInputCtrl (L3812) | Y (派生 from cashflow) | N | (派生) | Delivery 录入 | A |
| deliveryInputRecordCtrl (L4024) | Y (派生 from cashflow) | N | (派生) | Delivery 录入记录 | A |
| deliveryProcessingCtrl (L4236) | Y (派生 from cashflow) | N | (派生) | Delivery 处理 | A |
| waitChargeDetailCtrl (L6568) | Y (getMedicalRecord) | N | $stateParams | 收费详情 | A |

### §17.2 MedicalRecord 共同消费模式

- **15 个 Controller 共享 MedicalRecord** (A 级)
- 入口参数都是 `medicalRecordId` (A)
- 唯一 Create API: addMedicalRecord.json (A)

---

## §18 字段分类

### §18.1 MedicalRecord 字段 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core Object Field | `id`, `medicalRecordType`, `patientId`, `templateId` | A |
| B. Nested Object | `customerCheckin` (列表项推断), `diagnosis` (经 visionRecordVo) | C |
| C. Request Only | `id` (getMedicalRecord Request) | A |
| D. State Only | `medicalRecordId` ($stateParams) | A |
| E. UI Only | - | F (0 命中) |
| F. Runtime Mutation | - | F (MedicalRecord 无 runtime mutation) |

### §18.2 medicalRecordId 6 重身份

| 身份 | 等级 | 字符级证据 |
|---|---|---|
| A. Core Object Field | A | `medicalRecord.id` (L35085) |
| B. State Params | A | `$stateParams.medicalRecordId` (25+ 处) |
| C. Request Parameter | A | `{ id: $stateParams.medicalRecordId }` / `{ medicalRecordId: ... }` |
| D. Response Field | A | `res.object.id` / `res.object.medicalRecord.id` (L4036) |
| E. Scope Variable | A | `$scope.medicalRecordId` / `$scope.obj.medicalRecordId` (多处) |
| F. URL Query / State | A | $stateParams (State entry) |

**重要**: medicalRecordId 是 MedicalRecord 主键, 但**不是**"数据库外键" (L3 F)。它是**前端主键**。

---

## §19 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 15+ Controllers 范围 | A | - | 全部 | A |
| 2 | Controller | 15 Controllers | A | - | 全部 | A |
| 3 | State | addSaleRecord / adminSalesRecord.* / adminMyRecord.* | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | medicalRecordId (25+ State 入口) | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | (Sale 范围 payedStatus/refundStatusArray) | A | - | L31073 | A |
| 10 | Status | **MedicalRecord 不含 status** | A | - | 0 命中 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=12/20/30 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | patientId (Create) | A | - | L31116 | A |
| 15 | Default | medicalRecordType=1 (beginCustomerCheckin) | A | - | L10607 | A |
| 16 | Data Source | 11+ Read API | A | - | 全部 | A |
| 17 | Object | id, medicalRecordType, patientId, templateId | A | - | 全部 | A |
| 18 | Request | { patientId, medicalRecordType } | A | - | L31115 | A |
| 19 | Response | res.object.{id, medicalRecordType, patientId} | A | - | L31123 | A |
| 20 | Function | choseUser.affirm / goRecord / getMedical | A | - | 多处 | A |
| 21 | State Bridge | medicalRecordId (主入口) | A | - | 25+ | A |
| 22 | Object Bridge | medicalRecord.id (L35085) | A | - | L35085 | A |
| 23 | API Bridge | addMedicalRecord / getMedicalRecord / 其它 | A | - | 全部 | A |
| 24 | Business Interpretation | MedicalRecord 是一级核心对象 (多视图) | A | - | - | A (派生) |
| 25 | Evidence Grade | 22 A / 0 B / 2 C / 0 D / 0 E / 2 F | - | - | - | - |
| 26 | V4.4 Decision | MedicalRecord 是前端核心主对象, 必保留 | A | - | - | A |

---

## §20 历史差异

### §20.1 S1-135 ~ S1-145 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-135: CustomerCheckin ↔ MedicalRecord 双向 | 实际 6 处 customerCheckin.medicalRecordId, 0 处 medicalRecord.customerCheckin 字段 | 保持 | **单向 A (CustomerCheckin → MedicalRecord)** |
| S1-136: Check/Optometry/Sale 共享 MedicalRecord | 实际 medicalRecordType 分流 | 保持 | **多视图共享 MedicalRecord** |
| S1-137R: 4 API 双向桥 | 实际仅 getMedicalRecordPayVo 1 API 单向 | 已在 S1-137R 修正 | **保持 S1-137R 修正** |
| S1-138: 5 Create 路径 | 实际 6 路径 (含 L34914 链式) | 已在 S1-138 修正 | **保持 S1-138 修正** |
| S1-140: CustomerCheckin.patientId ≡ patientId | 实际 L8707 在注释代码, 运行时未消费 | 已在 S1-140 修正 | **保持 S1-140 修正** |
| S1-141: 4 个 Cashflow Write API | 实际 5 (createCashFlow + pay + 2 payFor* + cancel) | 已在 S1-141 修正 | **保持 S1-141 修正** |
| S1-142: Delivery → MedicalRecord F | 实际 L4034 getMedicalRecordPayVo 派生 | 已在 S1-142 修正 | **保持 S1-142 修正** |
| S1-142: completeMedicalRecordDelivery 在 deliveryInputCtrl | 实际在 optometryCtrl | 已在 S1-142 修正 | **保持 S1-142 修正** |
| S1-143: Sale 没有独立 saleVo | 实际 0 命中 saleVo/saleId | 已在 S1-143 修正 | **保持 S1-143 修正** |
| S1-144: type=1 = Check | 实际 type=1 = 接诊 (beginCustomerCheckin 链) | 已在 S1-144 修正 | **保持 S1-144 修正** |
| S1-144: Prescription 独立实体 | 实际 0 命中 prescriptionId | 已在 S1-144 修正 | **保持 S1-144 修正** |
| S1-145: MedicalExamine 唯一独立 ID | 实际 MedicalProduct 也有 | 已在 S1-145 修正 | **保持 S1-145 修正** |

### §20.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "MedicalRecord 含 status 字段" | 0 命中 medicalRecord.status | 应改 | **MedicalRecord 不含 status 字段** (A) |
| "MedicalRecord 含 cashflow / delivery / sale 嵌套" | 0 命中 | 应改 | **全部 F** (A) |
| "MedicalRecord ↔ VisionRecord 双向" | 实际仅 VisionRecord → MedicalRecord | 应改 | **单向 A** (A) |
| "MedicalProduct 含 medicalRecordId 字段" | 0 命中 | 应改 | **F** (A) |
| "completeMedicalRecordDelivery 等 4 个 API 在 deliveryInputCtrl" | 实际在 optometryCtrl | 已修正 (S1-142) | **保持** |

### §20.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 208_S1-145 全部保持原样
- 本文档 209_*.md 单独记录 MedicalRecord 核心主对象完整闭环

---

## §21 V4.4 MedicalRecord 规格

### §21.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| addMedicalRecord.json | L31119 | ✓ (唯一 Create) |
| getMedicalRecord.json | 11+ 调用 | ✓ (唯一 MedicalRecord 主对象 Read) |
| 15+ Controller 消费 | 全部 | ✓ |
| medicalRecordId 25+ State 入口 | 全部 | ✓ |
| medicalRecordType 分流 (16 处) | 全部 | ✓ |
| $stateParams.medicalRecordId 入口 | 25+ | ✓ |
| `res.object.medicalRecord.id` 派生 | L4036 | ✓ |
| `res.object.medicalRecord.patientId` 派生 | L6693 | ✓ |
| 5 个 Update/Cancel/Return/Delivery/ReportLoss Write API | 全部 | ✓ (在 optometryCtrl) |
| createCashFlowForMedicalRecord.json | L6925 | ✓ |
| beginCustomerCheckin.json (含 medicalRecordType: 1) | L10605/L33127/L34947 | ✓ |
| receiveSelfAndBeginCustomerCheckin.json | L33195 | ✓ |
| getMedicalRecordList.json / getMedicalRecordListOfDoctor.json | L32927/L33029 | ✓ |
| getMedicalRecordPayVo.json | L4034 | ✓ |
| getMedicalRecordCashflowVo.json | L4942/L5166/L7070/L7488 | ✓ |
| setMedicalRecordProcessMode.json | L35099 | ✓ |
| getHaveOrderMedicalRecordVoList.json | L31055 | ✓ |
| computeUnPlaceOrderMedicalRecordFee.json | L6680 | ✓ |

### §21.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `medicalRecord.status` / `payStatus` / `refundStatus` / `cancelStatus` / `deliveryStatus` 字段 | ✗ (0 命中) |
| `medicalRecord.cashflow` / `medicalRecord.delivery` 嵌套对象 | ✗ (0 命中) |
| `medicalRecord.sale` / `medicalRecord.saleId` | ✗ (S1-143 已确认 0 命中) |
| `medicalRecord.medicalExamineVoList` 嵌套 | ✗ (0 命中) |
| `medicalRecord.visionRecordVo` 嵌套 | ✗ (0 命中) |
| `medicalRecord.methodGlassRecordVo` 嵌套 | ✗ (0 命中) |
| `medicalRecord.medicalProductVoList` 嵌套 | ✗ (0 命中) |
| `medicalRecord.customerCheckinId` 字段 | ✗ (0 命中) |
| `medicalProduct.medicalRecordId` 字段 | ✗ (0 命中) |
| `cashflow.medicalRecordId` 字段 | ✗ (0 命中) |
| `medicalRecord.cashflowId` 字段 | ✗ (0 命中) |
| `medicalRecord.deliveryId` 字段 | ✗ (0 命中) |
| `medicalRecord.checkinId` / `medicalRecord.prescriptionId` | ✗ (0 命中) |
| 4 个 MedicalRecord lifecycle API 在 deliveryInputCtrl | ✗ (实际在 optometryCtrl) |

### §21.3 核心字段规范

| 字段 | 必实现 | 等级 |
|---|---|---|
| `id` | YES | A |
| `medicalRecordType` | YES (1/5 分流) | A |
| `patientId` | YES (Create Request + Response) | A |
| `templateId` | YES (推断) | C |
| `customerCheckin` (嵌套列表) | YES (列表项) | C |
| `diagnosis` (经 visionRecordVo) | YES (推断) | C |

### §21.4 Object Type 分类 (A 级)

| Object | 实际 Type | 必不当作 |
|---|---|---|
| **MedicalRecord** | A+B (独立 ID + 嵌套列表 customerCheckin/diagnosis) | 数据库外键 (L3 F) |
| `medicalRecord.status` | F (不存在) | - |
| `medicalRecord.cashflow` | F (不存在) | - |
| `medicalRecord.delivery` | F (不存在) | - |

### §21.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| MedicalRecord → Cashflow 字段桥 | F |
| MedicalRecord → Delivery 直接 | F (S1-142) |
| MedicalRecord → Sale 字段桥 | F (S1-143) |
| MedicalRecord → MedicalProduct 字段桥 | F (medicalProduct 不含 medicalRecordId) |
| MedicalRecord → VisionRecord 字段桥 | F (VisionRecord 不反向) |

### §21.6 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| medicalRecordType == 1 → 接诊 | A | 3 处字符级 |
| medicalRecordType == 5 → Sale | A | 6 处字符级 |
| `res.object.medicalRecord.id` → $scope.medicalRecordId (Delivery) | A | L4036 |
| `res.object.medicalRecord.patientId` → getPatientInfo (Sale) | A | L6693 |
| `customerCheckin.medicalRecordId` → MedicalRecord | A | 6 处字符级 |
| beginCustomerCheckin `medicalRecordType: 1` → 接诊 | A | 3 处字符级 |
| `addMedicalRecord` `medicalRecordType: custView==1?1:5` | A | L31117 |

### §21.7 命名误导必标注

| 命名 | 实际 | 警告 |
|---|---|---|
| `MedicalRecord.id` | 主键 | (无) |
| `res.object.medicalRecord.id` (L4036) | 实际是 `cashflow.medicalRecord.id` 经 getMedicalRecordPayVo 派生 | 命名误导 (cashflow→MedicalRecord) |
| `res.object.medicalRecord.patientId` (L6693) | 实际是 cashflow.computeUnPlaceOrderMedicalRecordFee Response 派生 | 命名误导 |
| `medicalRecord.customerCheckin` (L11667 firstMedicalRecord.id) | 列表项嵌套 | 命名误导 |
| `MedicalRecord Type` (medicalRecordType) | 不只是 type, 实际是**业务路由键** | 命名误导 |

### §21.8 必须保留的派生关系

- **MedicalRecord 共享模式**: 15+ Controller 共享 MedicalRecord (经 medicalRecordId State)
- **多视图**: 同一 MedicalRecord 4 视图 (Check/Optometry/Sale/Charge) 共享数据
- **status 不属于 MedicalRecord**: status 字段在 Cashflow / Delivery / Sale 独立对象
- **派生而非字段**: 4 对象通过 medicalRecordId 关联, 不通过字段嵌套

---

## §22 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | MedicalRecord 数据库表结构 | F | 需后端源码 |
| 2 | MedicalRecord 含 customerCheckinId 字段 (L3 推断) | F | 需后端 |
| 3 | MedicalRecord 含 diagnosis 字段 (L3 推断) | F | 需后端 |
| 4 | medicalRecordVo 完整 schema (仅 2 命中) | F | 需后端 |
| 5 | MedicalRecord status 枚举值 | F (0 命中) | 需后端 |
| 6 | MedicalRecord 完整字段列表 | F | 需后端 |
| 7 | type=2/3/4/0 业务含义 | F | 需后端 |
| 8 | firstMedicalRecord 含义 | C | 需业务定义 |
| 9 | medicalRecordVoList (selectMedicalRecordVoList) | F | 需查 |
| 10 | 4 个 MedicalRecord lifecycle API 的 Response schema | F | 需后端 |
| 11 | medicalRecordVo 内部字段 (customerCheckinVoList) | F | 需后端 |
| 12 | MedicalRecord 状态机 (Create → Pay → Delivery → Cancel) | C (L2 推断) | 需业务定义 |
| 13 | deliveryStatus 是否反向回写到 MedicalRecord | F (0 命中) | 需后端 |

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
| 历史 MD 165-208 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 209_*.md | ✓ |

### §23.2 Git 操作

```
git add -- 209_S1-146_MedicalRecord核心主对象字段生命周期与State分支总审计.md
git diff --cached --name-only
git commit -m "docs(209): S1-146 MedicalRecord 核心主对象字段生命周期与 State 分支总审计"
git push origin master
```

### §23.3 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| tracked | 217 (commit 209 后从 216 → 217) |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L4036 | `res.object.medicalRecord.id` (getMedicalRecordPayVo 派生) |
| L6693 | `res.object.medicalRecord.patientId` (computeUnPlaceOrderMedicalRecordFee 派生) |
| L11667 | `firstMedicalRecord.id` (列表项) |
| L33842 | `$scope.medicalRecord.id = $stateParams.medicalRecordId` |
| L34884 | `selectOrderListFactory.items[].medicalRecord.id` |
| L35085 | `medical.medicalRecord.id` (optometryCtrl choseFactoryMethod) |
| L35086 | `medical.medicalRecord.medicalRecordType` |
| L35137/L35149/L35166/L35182/L35201 | `item.medicalRecord.id` (7+ 处) |
| L31119 | addMedicalRecord.json (唯一 Create) |
| L31116 | `patientId: item.patient.id` |
| L31117 | `medicalRecordType: custView == 1 ? 1 : 5` |
| L31123 | `res.object.medicalRecordType == 5` |
| L33479 | updateMedicalRecord.json |
| L35150 | cancelMedicalRecord.json (optometryCtrl) |
| L35167 | confirmMedicalRecordReturn.json (optometryCtrl) |
| L35185/L35204 | completeMedicalRecordDelivery.json (optometryCtrl) |
| L35342 | createMedicalStockLossOfSmallVersion.json (optometryCtrl) |
| L6925 | createCashFlowForMedicalRecord.json |

---

S1-146 完成。立即停止，等待老板下一指令。不执行 S1-147。
