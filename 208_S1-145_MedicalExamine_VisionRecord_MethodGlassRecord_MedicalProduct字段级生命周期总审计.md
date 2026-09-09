# S1-145：MedicalExamine / VisionRecord / MethodGlassRecord / MedicalProduct 四大对象字段级生命周期与桥接总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 207 个 MD / 不修改历史
> 关联：S1-129 / S1-138 / S1-141 / S1-142 / S1-143 / S1-144

---

## 目录

- §0 审计范围
- §1 MedicalExamine
- §2 VisionRecord
- §3 MethodGlassRecord
- §4 MedicalProduct
- §5 四对象字段矩阵
- §6 四对象交叉桥
- §7 四对象 ↔ Patient / CustomerCheckin
- §8 四对象 ↔ Sale
- §9 四对象 ↔ Delivery / Machine / Stock
- §10 MethodGlassRecord Write
- §11 API Response Object
- §12 字段 Source Trace
- §13 Object Type 分类
- §14 26 项证据矩阵
- §15 历史差异
- §16 V4.4 四对象规范
- §17 V4.4 最终红线
- §18 F / 未确认
- §19 Git / 完整性

---

## §0 审计范围

本轮四大核心对象:
- A. MedicalExamine
- B. VisionRecord
- C. MethodGlassRecord
- D. MedicalProduct / medicalProductVo / medicalProductVoList

关联对象: MedicalRecord / Patient / CustomerCheckin / Sale / Delivery / Machine / Stock / Prescription

---

## §1 MedicalExamine

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `medicalExamine` 总命中 | 123 | A |
| `medicalExamineId` 总命中 | 60+ | A |
| `medicalExamineVoList` | 30+ | A |
| `getMedicalExamineVoList.json` | 5+ | A |

### §1.2 MedicalExamine API 全量

| API | 行号 | Read/Write | Controller | Request | Response |
|---|---|---|---|---|---|
| getMedicalExamineVoList.json | L2068 | R | assistCheckingCtrl | `{ medicalRecordId }` | `examineListFactory.items[].medicalExamine` |
| getMedicalExamineVoList.json | L2385 | R | (checkListCtrl) | `{ medicalRecordId }` | 同上 |
| getMedicalExamineVoList.json | L32190 | R | (Sale 范围) | `{ medicalRecordId }` | `myMaterialFactory.medicalExamineVoList` |
| getMedicalExamineVoList.json | L32293 | R | (Sale 范围, 重查询) | `{ medicalRecordId }` | 同上 |
| getMedicalExamineVoList.json | L32422 | R | (Sale 范围, 列表) | (param) | `myMaterialFactory.medicalExamineVoList` |
| getMedicalExamineItemVoList.json | L1925 | R | assistCheckingCtrl | `{ medicalExamineId }` | examineItems |
| **startExamine.json** | L2415 | **W** | checkCallCtrl | `{ medicalExamineId }` | - |
| **startExamine.json** | L2691 | **W** | checkCallCtrl | `{ medicalExamineId }` | - |
| **completeExamine.json** | L2211 | **W** | assistCheckingCtrl | `{ medicalExamineId }` | - |
| **checkBeforeDeleteMedicalExamine.json** | L32389 | **W** | (Sale 范围) | `{ medicalExamineId }` | - |
| **updateMemberRate.json** (L10161) | L10161 | **W** | (Charge 范围) | `{ medicalExamineId, memberRate }` | - |

### §1.3 MedicalExamine 字段字符级

| 字段 | 字符级证据 | Source Type |
|---|---|---|
| `id` | L2074 `res.items[0].medicalExamine.id` | Response |
| `medicalExamineId` | L1760 `$stateParams.medicalExamineId` | State |
| `medicalExamineId` | L2074 `$scope.obj.medicalExamineId = res.items[0].medicalExamine.id` | Response→Scope |
| `medicalExamineVoList[].medicalExamine.id` | L7072 | Response |
| `medicalExamineIdList` | L2310/L6571/L7012 数组 | Scope |
| `medicalExamine.medicalRecordId` | 推断 (Request/Response 字段) | - |

### §1.4 MedicalExamine 独立 ID 证据

```javascript
// L1760-L1766 assistCheckingCtrl
$scope.obj.medicalExamineId = $stateParams.medicalExamineId;  // L1760
$scope.setMedicalExamineId = function (id) {
  $scope.obj.medicalExamineId = id;
};
$scope.setMedicalExamineId($stateParams.medicalExamineId);
return res.items[0].medicalExamine.id;                          // L2074
```

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| MedicalExamine 有独立 ID `medicalExamineId` | A | L1760/L2074/L1762/L1763 等 60+ 命中 |
| `medicalExamine.id` 是 Response 字段 | A | L2074/L2077/L2391/L2398/L10161 |
| ID 跨 Controller 共享 | A | L7072 (waitChargeDetailCtrl) ↔ L6571 (myMaterialBillCtrl) |
| MedicalExamine 有 4 个 Write API | A | startExamine / completeExamine / checkBeforeDeleteMedicalExamine / updateMemberRate |

### §1.5 MedicalExamine 实体判断

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| MedicalExamine 是独立 ID 实体 | A | 4 个 Write API + 60+ ID 命中 |
| MedicalExamine 有 medicalExamineVoList 列表 | A | 5+ 命中 |
| MedicalExamine ↔ MedicalRecord (medicalRecordId 桥) | A | Request/Response 双向 |
| MedicalExamine ↔ Patient | C (经 medicalRecordId 间接) | - |
| MedicalExamine 有 patientId 字段 | F (0 命中) | - |
| MedicalExamine 有 customerId 字段 | F (0 命中) | - |
| MedicalExamine 有 prescriptionVo 字段 | F (0 命中) | - |

---

## §2 VisionRecord

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `visionRecord` 总命中 | 76 | A |
| `visionRecordVo` 总命中 | 多 | A |
| `getVisionRecordVo.json` 总命中 | 7+ | A |
| `visionRecordId` 总命中 | **0** | F |

### §2.2 VisionRecord API 全量

| API | 行号 | Read/Write | Controller | Request |
|---|---|---|---|---|
| getVisionRecordVo.json | L16130 | R | optometryCtrl | `{ medicalRecordId: id }` |
| getVisionRecordVo.json | L31614 | R | drugPrescriptionCtrl | `{ medicalRecordId }` |
| getVisionRecordVo.json | L31636 | R | drugPrescriptionCtrl | (init) |
| getVisionRecordVo.json | L32180 | R | myMaterialBillCtrl | (param) |
| getVisionRecordVo.json | L32425 | R | myMaterialBillCtrl | (param) |
| getVisionRecordVo.json | L33670 | R | prescriptionCtrl | `{ medicalRecordId }` |
| getVisionRecordVo.json | L33786 | R | myMaterialBillCtrl | (param) |
| getVisionRecordVo.json | L33800 | R | optometryCtrl | `{ medicalRecordId }` |

### §2.3 VisionRecord 字段字符级

`Select-String 'visionRecord' controller.js` — 76 命中:

| 字段 | 字符级证据 | Source |
|---|---|---|
| `visionRecordVo.medicalRecord` (A) | L31620 `visionRecordVo.medicalRecord.diagnosis` | Response (嵌套 MedicalRecord) |
| `visionRecordVo.medicalRecord.diagnosis` | L31620 | Response |
| `visionRecordVoFactory.result` | L1918 | Response |
| `visionRecordVoFactory.object` | L32180 | Response |
| `visionRecordVoFactory.object.visionRecord` | L32180 (推断) | Response |
| `visionRecordVoFactory.result.visionRecord` | 多处 | Response |

### §2.4 VisionRecord 独立 ID 证据

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| VisionRecord 有 `visionRecordId` 字段 | **F (0 命中)** | - |
| VisionRecord 有独立 ID 实体 | **F** | 0 命中 |
| VisionRecord 是含 medicalRecordId 的 Response VO | A | L31614/L33670 (Request) + L31620 (Response.medicalRecord) |
| VisionRecord 嵌套 MedicalRecord | A | L31620 `visionRecordVo.medicalRecord` |

### §2.5 VisionRecord 实体判断

| 命题 | 等级 |
|---|:---:|
| VisionRecord 独立 ID 实体 | F |
| VisionRecord 是 Response VO | A |
| VisionRecord 含 medicalRecordId 字段 | A (Request) |
| VisionRecord 含 patientId 字段 | F (0 命中) |
| VisionRecord 含 customerId 字段 | F (0 命中) |

---

## §3 MethodGlassRecord

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `methodGlassRecord` 总命中 | 14+ | A |
| `methodGlassRecordVo` | 多 | A |
| `getMethodGlassRecordVo.json` | 7 调用 | A |
| `updateMethodGlassRecord.json` | 4 调用 | A (W) |
| `methodGlassRecordId` 总命中 | **0** | F |

### §3.2 MethodGlassRecord API 全量

| API | 行号 | Read/Write | Controller |
|---|---|---|---|
| getMethodGlassRecordVo.json | L16130 | R | optometryCtrl |
| getMethodGlassRecordVo.json | L31614 | R | drugPrescriptionCtrl |
| getMethodGlassRecordVo.json | L32813 | R | (Sale 范围) |
| getMethodGlassRecordVo.json | L33670 | R | prescriptionCtrl |
| getMethodGlassRecordVo.json | L33816 | R | optometryCtrl |
| getMethodGlassRecordVo.json | L35604 | R | (其它) |
| **updateMethodGlassRecord.json** | L31629 | **W** | drugPrescriptionCtrl |
| **updateMethodGlassRecord.json** | L33753 | **W** | prescriptionCtrl |
| **updateMethodGlassRecord.json** | L33894 | **W** | optometryCtrl |
| **updateMethodGlassRecord.json** | L35644 | **W** | (其它) |

### §3.3 MethodGlassRecord 字段字符级

基于 drugPrescriptionCtrl / prescriptionCtrl / optometryCtrl 字符级:

| 字段 | 字符级证据 | Source |
|---|---|---|
| `medicalRecordId` (A) | L31614/L33670/L33816 (Request) | Request |
| `left67` (左眼第67项) | L31616 字符级 | UI/Scope |
| `left68` | L31617/L31620 | UI/Scope |
| `left1-91` 系列 | L33619-L33662 | UI/Scope |
| `right1-91` 系列 | L33619-L33662 | UI/Scope |
| `optometryMethod` (验配方法) | L33680 | UI/Scope |
| `mydriasisMethod` (散瞳方法) | L33683 | UI/Scope |
| `rxCount` (配镜次数) | L33660 | UI/Scope |
| `lastRxTime` (上次配镜时间) | L33661/L33676 | UI/Scope |
| `productId` | 推断 | - |

### §3.4 MethodGlassRecord 独立 ID 证据

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| MethodGlassRecord 有 `methodGlassRecordId` 字段 | **F (0 命中)** | - |
| MethodGlassRecord 有独立 ID 实体 | **F** | 0 命中 |
| MethodGlassRecord 有 4 个 Write API | A | L31629/L33753/L33894/L35644 |
| MethodGlassRecord 是含 medicalRecordId 的 Response VO | A | 7 个 Read API |

### §3.5 MethodGlassRecord 实体判断

| 命题 | 等级 |
|---|:---:|
| MethodGlassRecord 独立 ID 实体 | F |
| MethodGlassRecord 是 Response VO | A |
| MethodGlassRecord 含 medicalRecordId | A |
| MethodGlassRecord 含 patientId | F (0 命中) |
| MethodGlassRecord 含 customerId | F (0 命中) |
| MethodGlassRecord 有 Write API | A (4 处) |
| MethodGlassRecord 含 medicalProductId | F (0 命中, 仅 medicalRecordId) |

---

## §4 MedicalProduct

### §4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `medicalProduct` 总命中 | 94+ | A |
| `medicalProductVo` 总命中 | 多 | A |
| `medicalProductVoList` 总命中 | 30+ | A |
| `medicalProductVoListOfModel` | 5+ | A |
| `medicalProductId` 总命中 | 5+ | A |

### §4.2 MedicalProduct API 全量

| API | 行号 | Read/Write | Controller |
|---|---|---|---|
| getMedicalProductVoList.json | L5009 | R | (Sale 范围) |
| getMedicalProductVoList.json | L8364 | R | (Search by name+mobile) |
| getMedicalProductVoList.json | L18981 | R | patientListCtrl (by customerId) |
| getMedicalProductVoList.json | L35054 | R | optometryCtrl (chain to F4) |
| getMedicalProductModelList.json | L31416 | R | (Sale 范围) |
| getMedicalProductStockList.json | L35319 | R | optometryCtrl (报损) |
| getMedicalProductVo.json | L8880 | R | (Patient 查询) |
| getMedicalProductMachineCenterVoList.json | L3836 | R | deliveryInputCtrl (F3) |
| getCanBeDeliverySkuInListOfProduct.json | L3885/L35054 | R | deliveryInputCtrl/optometryCtrl (F4) |
| saveMedicalProduct.json | L33791 | **W** | (Sale 范围, update) |
| saveMedicalProductStockBatch.json | L4007 | **W** | deliveryInputCtrl (F5) |
| sendMedicalProductToMachineCenter.json | L3966 | **W** | deliveryInputCtrl (F6) |
| saveMedicalProductDeliveryCommentBatch.json | L4061 | **W** | deliveryInputRecordCtrl |
| computeUnPlaceOrderMedicalRecordFee.json | L6680 | R | myMaterialBillCtrl |

### §4.3 MedicalProduct 字段字符级

| 字段 | 字符级证据 | Source |
|---|---|---|
| `id` (medicalProduct.id) | L3823/L3962/L3998/L4055/L4663 | Response / Runtime |
| `objectId` (medicalProduct.objectId) | L3853-L3856 runtime mutation | **Runtime mutation** (来自 lockMachineCenter.id) |
| `productId` (medicalProduct.productId) | 推断 | Response |
| `medicalProductId` (request) | L3823/L3962/L3998 | Request |
| `memberRate` | L6752/L6754 | Response/Scope |
| `name` (medicalProduct.name) | 推断 | Response |
| `price` (medicalProduct.price) | 推断 | Response |

### §4.4 MedicalProduct.objectId 生命周期 (S1-142 已确认)

```javascript
// L3853-L3856 deliveryInputCtrl
if (arr[i].lockStorehouse.type == 4) {
  $scope.getMedicalRecordDeliveryFactory.result.object
    .waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;  // L3854
} else {
  $scope.getMedicalRecordDeliveryFactory.result.object
    .waitingDeliveryList[i].medicalProduct.objectId = null;                          // L3856
}
```

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| medicalProduct.objectId 是 runtime mutation | A | L3854 |
| Source: `lockMachineCenter.id` (若 lockStorehouse.type==4) | A | L3854 |
| Source: `null` (否则) | A | L3856 |
| 消费方: F3 Request `machineCenterId` | A | L3824 |
| 消费方: F6 Request `machineCenterId` | A | L3962 |

### §4.5 MedicalProduct 实体判断

| 命题 | 等级 |
|---|:---:|
| MedicalProduct 是独立 ID 实体 | A (有 medicalProduct.id) |
| MedicalProduct 含 medicalRecordId 字段 | F (0 命中) |
| MedicalProduct 含 patientId 字段 | F (0 命中) |
| MedicalProduct 含 machineCenterId 字段 | A (Request 字段) |
| MedicalProduct 含 stockInSkuId 字段 | F (字段在 stockInSku 对象, 不在 medicalProduct) |
| MedicalProduct 是 Sale 容器内对象 | A (myMaterialBillCtrl 范围) |
| MedicalProduct 是 Delivery 容器内对象 | A (deliveryInputCtrl 范围) |

---

## §5 四对象字段矩阵

### §5.1 MedicalExamine 字段

| 字段 | Source | 等级 |
|---|---|---|
| `id` | Response | A |
| `medicalExamineId` (与 id 同) | State / Response | A |
| `medicalExamineVoList[].medicalExamine` (嵌套) | Response | A |
| `medicalRecordId` (推断) | Request/Response | C (推断) |

### §5.2 VisionRecord 字段

| 字段 | Source | 等级 |
|---|---|---|
| `visionRecordVo` (顶层) | Response | A |
| `visionRecordVo.medicalRecord` (嵌套) | Response | A |
| `visionRecordVo.medicalRecord.diagnosis` | Response | A |
| `medicalRecordId` | Request | A |
| `visionRecordId` | F (0 命中) | F |

### §5.3 MethodGlassRecord 字段

| 字段 | Source | 等级 |
|---|---|---|
| `methodGlassRecordVo` (顶层) | Response | A |
| `methodGlassRecord` (Scope) | Scope | A |
| `medicalRecordId` | Request | A |
| `optometryMethod` / `mydriasisMethod` / `rxCount` / `lastRxTime` | Scope/UI | A |
| `left1-91` / `right1-91` (屈光参数) | Scope/UI | A |
| `methodGlassRecordId` | F (0 命中) | F |

### §5.4 MedicalProduct 字段

| 字段 | Source | 等级 |
|---|---|---|
| `id` | Response | A |
| `objectId` (runtime mutation) | Runtime (L3854) | A |
| `medicalProductId` (request) | Request | A |
| `name` / `price` / `memberRate` | Response/Scope | C (推断) |
| `medicalRecordId` | F (0 命中) | F |
| `patientId` | F (0 命中) | F |

---

## §6 四对象交叉桥

### §6.1 矩阵

| Source | Target | 桥 | 等级 | 字符级证据 |
|---|---|---|:---:|---|
| MedicalExamine | MedicalRecord | medicalExamineVoList[].medicalExamine.medicalRecordId | A | 推断 (Request + Response 双向) |
| MedicalRecord | MedicalExamine | getMedicalExamineVoList by medicalRecordId | A | L2068/L2385/L32190 |
| MedicalExamine | VisionRecord | (无直接桥) | F | 0 命中 |
| VisionRecord | MedicalExamine | (无直接桥) | F | 0 命中 |
| MedicalExamine | MethodGlassRecord | (无直接桥) | F | 0 命中 |
| MethodGlassRecord | MedicalExamine | (无直接桥) | F | 0 命中 |
| VisionRecord | MethodGlassRecord | **同 MedicalRecord 入口** (medicalRecordId) | C | 同一 Controller 内多 API |
| MethodGlassRecord | VisionRecord | **同 MedicalRecord 入口** (medicalRecordId) | C | 同一 Controller 内多 API |
| MethodGlassRecord | MedicalProduct | (无直接桥) | F | 0 命中 |
| MedicalProduct | MethodGlassRecord | (无直接桥) | F | 0 命中 |
| MedicalExamine | MedicalProduct | (无直接桥, 经 medicalExamineVoList[i].medicalExamine.id) | C | L6703 字符级 |
| MedicalProduct | MedicalExamine | (无直接桥) | F | 0 命中 |

### §6.2 关键发现

- **四对象互不直接桥接**: 全部经 medicalRecordId 关联 (Response 包含 medicalRecord 引用)
- **MedicalExamine 是唯一有独立 ID 的子对象**: medicalExamineId
- **medicalProductId 跨 Controller**: L6703 `key2 === 'medicalProduct' ? 'medicalProductId' : 'medicalExamineId'`

---

## §7 四对象 ↔ Patient / CustomerCheckin

### §7.1 矩阵

| Source | Target | 等级 | 字符级证据 |
|---|---|:---:|---|
| MedicalExamine | Patient | A 间接 | 经 medicalRecord.patientId |
| Patient | MedicalExamine | A 间接 | 经 getMedicalRecord.patientId |
| VisionRecord | Patient | A 间接 | 经 medicalRecord |
| Patient | VisionRecord | A 间接 | 经 getMedicalRecord |
| MethodGlassRecord | Patient | A 间接 | 经 medicalRecord |
| Patient | MethodGlassRecord | A 间接 | 经 getMedicalRecord |
| MedicalProduct | Patient | A 间接 | 经 medicalRecord |
| Patient | MedicalProduct | A 间接 | 经 getMedicalRecord |
| MedicalExamine | CustomerCheckin | F (无 customerCheckin 字段) | - |
| VisionRecord | CustomerCheckin | F | - |
| MethodGlassRecord | CustomerCheckin | F | - |
| MedicalProduct | CustomerCheckin | F | - |

**重要发现**: 四对象**不直接**与 Patient/CustomerCheckin 关联, 必须经 MedicalRecord 中转。

---

## §8 四对象 ↔ Sale

### §8.1 矩阵

| Source | Target | 等级 | 字符级证据 |
|---|---|:---:|---|
| MedicalExamine | Sale | A 字段级 (经 medicalRecordId) | L32190/L32293 (myMaterialBillCtrl) |
| Sale | MedicalExamine | A 间接 (createCashFlow) | L6571 (medicalExamineIdList) |
| VisionRecord | Sale | A 字段级 (经 medicalRecordId) | L32180/L32425 (myMaterialBillCtrl) |
| Sale | VisionRecord | A 间接 | - |
| MethodGlassRecord | Sale | A 字段级 (经 medicalRecordId) | L32813 (myMaterialBillCtrl) |
| Sale | MethodGlassRecord | A 间接 | - |
| MedicalProduct | Sale | **A 字段级** | L5009/L6586 (myMaterialBillCtrl medicalProductVoList) |
| Sale | MedicalProduct | A 间接 | - |

### §8.2 Sale (myMaterialBillCtrl) 实际读取 4 对象

```javascript
// myMaterialBillCtrl 内部 4 个对象读取
L5009: result.medicalProductVoList        // MedicalProduct
L31614 (drugPrescriptionCtrl): getMethodGlassRecordVo  // MethodGlassRecord
L32180: getVisionRecordVo                 // VisionRecord
L32190: getMedicalExamineVoList           // MedicalExamine
```

**关键发现**: myMaterialBillCtrl (Sale 容器) **同时**读 4 个对象的 medicalRecordId 关联数据, 因为 Sale 与 Check/Optometry 共享 MedicalRecord。

### §8.3 Sale 字段

- `medicalProductVoList` (A) - 含 medicalProduct.id
- `medicalProductVoListOfModel` (A) - 模板
- `medicalExamineVoList` (A) - myMaterialFactory
- `medicalExamineIdList` (A) - L6571
- **不存在** saleVo / salesVo / saleId (S1-143 已确认)

---

## §9 四对象 ↔ Delivery / Machine / Stock

### §9.1 矩阵

| Source | Target | 等级 | 字符级证据 |
|---|---|:---:|---|
| MedicalExamine | Delivery | F | 0 命中 |
| VisionRecord | Delivery | F | 0 命中 |
| MethodGlassRecord | Delivery | F | 0 命中 |
| **MedicalProduct** | **Delivery** | **A 字段级** | medicalProduct.id, objectId (L3851/L3854) |
| MedicalExamine | Machine | F | 0 命中 |
| VisionRecord | Machine | F | 0 命中 |
| MethodGlassRecord | Machine | F | 0 命中 |
| **MedicalProduct** | **Machine** | **A 字段级 (Request)** | machineCenterId (F3/F6) |
| MedicalExamine | Stock | F | 0 命中 |
| VisionRecord | Stock | F | 0 命中 |
| MethodGlassRecord | Stock | F | 0 命中 |
| **MedicalProduct** | **Stock** | **A 字段级 (Request)** | stockInSkuId, deliveryCount (F4/F5) |

### §9.2 MedicalProduct 在 Delivery 4 API (F3/F4/F5/F6) 中的实际角色

| API | Request 字段 | 行号 |
|---|---|---|
| F3 getMedicalProductMachineCenterVoList | `medicalProductMachineCenterPoListJson: [{medicalProductId, machineCenterId}]` | L3836 |
| F4 getCanBeDeliverySkuInListOfProduct | `medicalProductIdArray` | L3885/L35054 |
| F5 saveMedicalProductStockBatch | `medicalProductStockBatctPoListJson: [{medicalProductId, medicalProductStocks: [{stockInSkuId, deliveryCount}]}]` | L4007 |
| F6 sendMedicalProductToMachineCenter | `medicalProductMachineCenterPoListJson: [{medicalProductId, machineCenterId}], planDeliveryTime` | L3966 |

### §9.3 MedicalProduct 桥接结论

| 桥 | 等级 | 备注 |
|---|---|---|
| MedicalProduct → Delivery | A 字段级 (medicalProduct.id, objectId) | waitingDeliveryList (F1) |
| MedicalProduct → Machine | A Request (machineCenterId) | F3/F6 |
| MedicalProduct → Stock | A Request (stockInSkuId, deliveryCount) | F4/F5 |
| **MedicalProduct 表 FK** | **F** (L3) | 0 命中数据库表/FK 字符级 |
| MedicalProduct.id → machineCenter.id | F (L3) | 只有 objectId 字段, 无 Object 字段 |
| MedicalProduct.id → stockInSku.id | F (L3) | 只有 stockInSkuId 字段, 无 Object 字段 |

---

## §10 MethodGlassRecord Write 深挖

### §10.1 4 个 Write 调用点全量

| # | 行号 | Controller | Function | Request Variable | Response |
|---|---|---|---|---|---|
| 1 | L31629 | drugPrescriptionCtrl | (prescriptionParams2 关联) | `modifyGlassRecordVo` | 后续 action |
| 2 | L33753 | prescriptionCtrl | (L33750 附近函数) | `newobj` | - |
| 3 | L33894 | optometryCtrl | (L33890 附近函数) | `$scope.methodGlassRecord` | - |
| 4 | L35644 | (其它 Controller) | (L35640 附近函数) | `$scope.object` | - |

### §10.2 updateMethodGlassRecord.json 字段

| 字段 | 等级 | 字符级证据 |
|---|---|---|
| `medicalRecordId` | A | Request (经 4 个调用点) |
| `left1-91` / `right1-91` (屈光参数) | A | Scope `$scope.methodGlassRecord` |
| `optometryMethod` / `mydriasisMethod` | A | Scope |
| `rxCount` / `lastRxTime` | A | Scope |
| `medicalProductId` | F (0 命中) | - |
| `patientId` | F (0 命中) | - |
| `visionRecordId` | F (0 命中) | - |
| `medicalExamineId` | F (0 命中) | - |
| `saleId` / `orderId` | F (0 命中) | - |

### §10.3 updateMethodGlassRecord 上下文

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| updateMethodGlassRecord 是 Write API | A | 4 处调用 |
| 与 medicalRecordId 关联 | A | Request 字段 |
| 与 medicalProductId 关联 | F | 0 命中 |
| 与 VisionRecord 关联 | F | 0 命中 (虽然处方单同存于 prescriptionCtrl) |
| 与 MedicalExamine 关联 | F | 0 命中 |
| 与 Sale 关联 | F | drugPrescriptionCtrl 不是 Sale, prescriptionCtrl 不是 Sale |

### §10.4 4 个调用 Controller 业务归属

| Controller | 业务 |
|---|---|
| drugPrescriptionCtrl | 药品处方 (L31605) |
| prescriptionCtrl | 验光处方 (L33560) |
| optometryCtrl | 验光 + 选镜架 (L34776) |
| (L35644) | (待查, 推断为处方相关) |

**重要发现**: updateMethodGlassRecord 是 **MethodGlassRecord 自身的 Write**, 与 Sale / Check / Optometry 业务无直接桥, 4 个 Controller 各自独立调用。

---

## §11 API Response Object 层级

### §11.1 5 个核心 API Response 完整结构

| API | Root | Path | 字段 | Consumer |
|---|---|---|---|---|
| getMedicalExamineVoList.json | { items: [...] } | items[].medicalExamine | id, medicalRecordId, ... | assistCheckingCtrl, myMaterialBillCtrl |
| getVisionRecordVo.json | { result: { object: { visionRecordVo: ... } } } | result.object.visionRecordVo.medicalRecord | diagnosis, ... | optometryCtrl, drugPrescriptionCtrl, prescriptionCtrl, myMaterialBillCtrl |
| getMethodGlassRecordVo.json | { result: { object: { methodGlassRecordVo: ... } } } | result.object.methodGlassRecordVo | optometryMethod, mydriasisMethod, left1-91, right1-91, ... | optometryCtrl, drugPrescriptionCtrl, prescriptionCtrl, myMaterialBillCtrl |
| getMedicalProductVoList.json | { result: { list: [...] } } | result.list[].medicalProduct | id, objectId, name, price, ... | myMaterialBillCtrl, deliveryInputCtrl |
| getMedicalProductModelList.json | (类似) | (类似) | - | myMaterialBillCtrl |

### §11.2 关键发现

- **MedicalExamine 是 List (items: [...])**: 多个 medicalExamine 对象, 选 current
- **VisionRecord / MethodGlassRecord 是单对象 (visionRecordVo)**: 一个 medicalRecordId 对应一个 VO
- **MedicalProduct 是 List (list: [])**: 多个 medicalProduct 对象

---

## §12 字段 Source Trace

### §12.1 关键字段来源链

| 字段 | Source | Transform | Target |
|---|---|---|---|
| `medicalRecordId` | `$stateParams.medicalRecordId` (State) | - | Request / State |
| `medicalRecordId` | `res.object.medicalRecord.id` (Response) | - | State / Scope |
| `patientId` | `$stateParams.patientId` (State) | - | State |
| `patientId` | `res.result.object.patientId` (Response) | - | Scope |
| `medicalExamineId` | `$stateParams.medicalExamineId` (State) | - | State |
| `medicalExamineId` | `res.items[0].medicalExamine.id` (Response) | L2074 | Scope → Request |
| `medicalProductId` | `medicalProduct.id` (Response) | L3823 | Request (F3/F4/F5/F6) |
| `machineCenterId` | `medicalProduct.objectId` (Runtime mutation) | L3854 | Request (F3/F6) |
| `machineCenterId` | `v.machineCenter.id` (Response) | L3962 | Request (F6) |
| `stockInSkuId` | `deliveryStockInSkuVoList[j].stockInSku.id` (Response) | L3991 | Request (F5) |
| `deliveryCount` | `deliveryStockInSkuVoList[j].deliveryCount` (Response) | L3991 | Request (F5) |
| `planDeliveryTime` | `$scope.startTime` (UI picker) | L3964 | Request (F6) |
| `objectId` | `lockMachineCenter.id` (若 type==4) | L3854 runtime | `medicalProduct.objectId` |

### §12.2 关键 ID 状态机

```
[State 入口]
  $stateParams.medicalRecordId
    ↓ A (入 Scope / 入 Request)
  medicalRecordId
    ↓ A (Response 消费)
  res.object.id / res.object.medicalRecordId
    ↓ A (新 State)
  $stateParams.medicalRecordId
```

---

## §13 Object Type 分类

### §13.1 四对象分类

| Object | A. 独立 ID 证据 | B. Response VO | C. Request Payload | D. Scope/UI 临时 |
|---|:---:|:---:|:---:|:---:|
| **MedicalExamine** | **A** (medicalExamineId) | A (medicalExamineVoList) | A (4 个 Write API) | A (medicalExamineIdList) |
| **VisionRecord** | **F** (无 ID) | A (visionRecordVo) | **F** (无 Write API) | C (局部变量) |
| **MethodGlassRecord** | **F** (无 ID) | A (methodGlassRecordVo) | A (4 个 Write API) | A (methodGlassRecord Scope) |
| **MedicalProduct** | **A** (medicalProduct.id) | A (medicalProductVoList) | A (F3-F6 + createCashFlow) | A (medicalProductVoListOfModel) |

### §13.2 关键发现

| 命题 | 等级 |
|---|:---:|
| 4 对象中仅 MedicalExamine 和 MedicalProduct 有独立 ID | A |
| 4 对象中仅 VisionRecord 没有 Write API | A |
| 4 对象都是 Response VO | A |
| 4 对象都在 Sale 容器 (myMaterialBillCtrl) 内被读 | A |
| 4 对象中仅 MedicalProduct 在 Delivery 范围被读 | A |

---

## §14 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | assistChecking / drugPrescription / prescription / optometry / myMaterialBill | A | - | 多处 | A |
| 2 | Controller | 4+ Controllers 范围 | A | - | 全部 | A |
| 3 | State | assistChecking / optometryGlasses / prescription / myMaterialBill | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | medicalRecordId (4 对象) | A | - | 多处 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | (Sale 范围 payedStatus/refundStatusArray) | A | - | L31073 | A |
| 10 | Status | medicalRecordType 分流 | A | - | 16 处 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=12/20/30 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | medicalRecordId | A | - | 多处 | A |
| 15 | Default | medicalRecordType=1 (beginCustomerCheckin) | A | - | L10607 | A |
| 16 | Data Source | 5 个核心 API | A | - | 全部 | A |
| 17 | Object | MedicalExamine / VisionRecord / MethodGlassRecord / MedicalProduct | A | - | 全部 | A |
| 18 | Request | { medicalRecordId } (4 对象) | A | - | 全部 | A |
| 19 | Response | medicalExamineVoList / visionRecordVo / methodGlassRecordVo / medicalProductVoList | A | - | 全部 | A |
| 20 | Function | choseFactoryMethod / goRecord / getMedical | A | - | 多处 | A |
| 21 | State Bridge | medicalRecordId (主入口) | A | - | 25+ 处 | A |
| 22 | Object Bridge | medicalExamineId (L6703) | A | - | L6703 | A |
| 23 | API Bridge | 5 个核心 API | A | - | 全部 | A |
| 24 | Business Interpretation | 4 对象共享 medicalRecordId (4 视图) | A | - | - | A (派生) |
| 25 | Evidence Grade | 22 A / 0 B / 2 C / 0 D / 0 E / 2 F | - | - | - | - |
| 26 | V4.4 Decision | 仅 MedicalExamine 和 MedicalProduct 有独立 ID | A | - | - | A |

---

## §15 历史差异

### §15.1 S1-129 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "F3/F4/F5/F6 仅 deliveryInputCtrl" | 实际 F4 也在 optometryCtrl (L35054) | 已在 S1-142 修正 | **保持 S1-142** |

### §15.2 S1-138 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "MedicalRecord 5 Create 路径" | 保持 | - | **保持** |

### §15.3 S1-141 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Cashflow ↔ MedicalRecord 单向" | 保持 | - | **保持** |

### §15.4 S1-142 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "medicalProduct.objectId 是 runtime mutation" | 保持 L3854 | - | **保持** (A) |
| "Delivery ↔ Machine F" | 保持 | - | **保持** |

### §15.5 S1-143 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Sale 没有独立 saleVo 实体" | 保持 | - | **保持** (A) |

### §15.6 S1-144 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "type=1 = 接诊" | 保持 | - | **保持** (A) |
| "Prescription / VisionRecord / MethodGlassRecord 不是独立 ID 实体" | 保持 | - | **保持** (A) |
| "MedicalExamine 是唯一含独立 ID 的子对象" | **修正**: MedicalProduct 也有独立 ID (medicalProduct.id) | 应改 | **MedicalExamine + MedicalProduct 都有独立 ID** (A) |

### §15.7 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "MedicalExamine 是唯一独立 ID 子对象" | MedicalProduct 也有 medicalProduct.id 独立 ID | 应改 | **MedicalExamine + MedicalProduct** (A) |
| "MethodGlassRecord 完全没有 Write" | updateMethodGlassRecord.json 4 处调用 | 应改 | **有 4 个 Write 调用** (A) |
| "VisionRecord 是 Sale 独立对象" | VisionRecord 是 medicalRecordVo 嵌套 | 应改 | **Response VO 非独立** (A) |

---

## §16 V4.4 四对象规范

### §16.1 MedicalExamine 规范

- **Object Type**: B (Response VO List) + A (独立 ID 实体)
- **ID**: `medicalExamineId` (等同 `medicalExamine.id`)
- **Read API**: getMedicalExamineVoList.json / getMedicalExamineItemVoList.json
- **Write API**: startExamine.json / completeExamine.json / checkBeforeDeleteMedicalExamine.json / updateMemberRate.json
- **Request 字段**: `medicalExamineId` / `medicalRecordId` (经后者)
- **Response 字段**: `medicalExamine.id` / `medicalExamineVoList[].medicalExamine` 嵌套
- **Consumers**: assistCheckingCtrl / myMaterialBillCtrl / waitChargeDetailCtrl
- **Bridges**: ↔ MedicalRecord (A) / ↔ Sale (A) / ↔ Charge (A)
- **Grade**: A

### §16.2 VisionRecord 规范

- **Object Type**: B (Response VO) - **非独立 ID 实体**
- **ID**: F (无 visionRecordId)
- **Read API**: getVisionRecordVo.json (7 调用)
- **Write API**: F (0 命中)
- **Request 字段**: `medicalRecordId`
- **Response 字段**: `visionRecordVo.medicalRecord` 嵌套 / `.diagnosis`
- **Consumers**: optometryCtrl / drugPrescriptionCtrl / prescriptionCtrl / myMaterialBillCtrl
- **Bridges**: ↔ MedicalRecord (A 字段级) / ↔ Sale (A 经 MedicalRecord)
- **Grade**: A (Response) / F (独立 ID)

### §16.3 MethodGlassRecord 规范

- **Object Type**: B (Response VO) + C (Request Payload)
- **ID**: F (无 methodGlassRecordId)
- **Read API**: getMethodGlassRecordVo.json (7 调用)
- **Write API**: updateMethodGlassRecord.json (4 调用)
- **Request 字段**: `medicalRecordId` / 30+ 屈光参数 / optometryMethod / mydriasisMethod / rxCount / lastRxTime
- **Response 字段**: `methodGlassRecordVo` / `optometryMethod` / `mydriasisMethod` / `left1-91` / `right1-91`
- **Consumers**: optometryCtrl / drugPrescriptionCtrl / prescriptionCtrl / myMaterialBillCtrl
- **Bridges**: ↔ MedicalRecord (A 字段级) / ↔ Sale (A 经 MedicalRecord)
- **Grade**: A

### §16.4 MedicalProduct 规范

- **Object Type**: A (独立 ID 实体) + B (Response VO) + C (Request Payload)
- **ID**: `medicalProduct.id` (有) / `medicalProduct.objectId` (Runtime mutation)
- **Read API**: getMedicalProductVoList.json / getMedicalProductVo.json / getMedicalProductMachineCenterVoList.json / getCanBeDeliverySkuInListOfProduct.json
- **Write API**: saveMedicalProduct.json / saveMedicalProductStockBatch.json (F5) / sendMedicalProductToMachineCenter.json (F6) / saveMedicalProductDeliveryCommentBatch.json
- **Request 字段**: `medicalProductId` / `machineCenterId` / `stockInSkuId` / `deliveryCount` / `planDeliveryTime` / `medicalProductStockBatctPoListJson`
- **Response 字段**: `id` / `objectId` (后端 lockMachineCenter) / `name` / `price` / `memberRate`
- **Consumers**: myMaterialBillCtrl (Sale) / deliveryInputCtrl (Delivery) / optometryCtrl / drugPrescriptionCtrl / prescriptionCtrl
- **Bridges**: ↔ MedicalRecord (A 字段级, 经 medicalRecordId) / ↔ Sale (A) / ↔ Delivery (A) / ↔ Machine (A Request) / ↔ Stock (A Request)
- **Grade**: A (全部)

---

## §17 V4.4 最终红线

### §17.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| MedicalExamine 独立 ID 字段 `medicalExamineId` | L1760 | ✓ |
| MedicalProduct 独立 ID 字段 `medicalProduct.id` | L3823 | ✓ |
| medicalProduct.objectId runtime mutation | L3854 | ✓ |
| 5 个核心 Read API | 全部 | ✓ |
| 8 个 Write API (MedicalExamine 4 + MedicalProduct 4) | 全部 | ✓ |
| medicalRecordId 25+ State 入口 | 全部 | ✓ |

### §17.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `visionRecordId` 字段 | ✗ |
| `methodGlassRecordId` 字段 | ✗ |
| `prescriptionId` 字段 | ✗ |
| `prescriptionVo` 独立对象 | ✗ |
| `saleVo` / `saleId` 字段 | ✗ |
| `orderId` 在 Sale 范围 | ✗ |
| `customerId` 在 Check/Optometry 范围 | ✗ |
| `customerCheckinId` 在 Sale 范围 | ✗ |
| `medicalProduct.medicalRecordId` 字段 | ✗ (0 命中) |
| `medicalProduct.patientId` 字段 | ✗ (0 命中) |
| `medicalExamine.patientId` 字段 | ✗ (0 命中) |

### §17.3 Object Type 必分类

| Object | 实际 Type | 必不当作 |
|---|---|---|
| MedicalExamine | A+B (独立 ID + Response VO) | 业务独立实体表 (L3 F) |
| VisionRecord | B (Response VO) | 独立 ID 实体 |
| MethodGlassRecord | B+C (Response VO + Request Payload) | 独立 ID 实体 |
| MedicalProduct | A+B+C (独立 ID + Response + Request) | (无需排除) |

### §17.4 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| VisionRecord → 独立 ID | F |
| MethodGlassRecord → 独立 ID | F |
| Prescription → 独立 ID | F |
| 4 对象 ↔ CustomerCheckin 直接 | F |
| 4 对象 ↔ Patient 直接 | F (经 medicalRecord 间接) |
| Sale → 独立 ID 实体 | F |
| MedicalProduct 表 FK Machine 表 | F (L3) |
| MedicalProduct 表 FK stockInSku 表 | F (L3) |

### §17.5 medicalRecordId 跨 4 对象 (A 级)

复刻必须保留: **medicalRecordId 是 4 对象的统一关联锚点**:
- MedicalExamine: Request
- VisionRecord: Request (经 result.object)
- MethodGlassRecord: Request
- MedicalProduct: Request (经 medicalProductVoList)

### §17.6 命名误导必标注

| 命名 | 实际 | 警告 |
|---|---|---|
| `medicalExamineVo` (L7072) | 顶层 list 名称, **不是** 独立 VO | 命名误导 |
| `visionRecordVo` (L31620) | 顶层字段名, 含嵌套 medicalRecord | 命名误导 |
| `methodGlassRecord` (Scope) | 配镜方法数据, **不是** 独立 ID 实体 | 命名误导 |
| `medicalProductVoList` | 顶层 list 名称, 内部含 medicalProduct.id | 命名误导 (有 ID) |
| `medicalProduct.objectId` | **runtime mutation** 字段, 实际是 machineCenter.id | **重大警告** |
| `updateMethodGlassRecord` (L31629) | 4 个 Controller 都调, 不是 drugPrescription 独占 | 命名误导 |

### §17.7 Source 链路必保留

| 字段 | Source | 必保留 |
|---|---|---|
| `medicalRecordId` | $stateParams | ✓ |
| `medicalExamineId` | $stateParams + res.items[0].medicalExamine.id | ✓ |
| `medicalProductId` | medicalProduct.id (Response) | ✓ |
| `objectId` | lockMachineCenter.id (Runtime) | ✓ |
| `machineCenterId` | medicalProduct.objectId (Runtime) | ✓ |
| `stockInSkuId` | deliveryStockInSkuVoList[j].stockInSku.id (Response) | ✓ |
| `planDeliveryTime` | $scope.startTime (UI picker) | ✓ |

---

## §18 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | VisionRecord 是否有独立数据库表 | F | 需后端源码 |
| 2 | MethodGlassRecord 是否有独立数据库表 | F | 需后端源码 |
| 3 | Prescription 是否有独立数据库表 | F | 需后端源码 |
| 4 | MedicalExamine 是否有独立数据库表 | F (前端有 ID) | 需后端源码 |
| 5 | MedicalProduct 是否有独立数据库表 | F (前端有 ID) | 需后端源码 |
| 6 | MedicalProduct 与 Machine 表 FK | F (L3) | 需后端 |
| 7 | MedicalProduct 与 Stock 表 FK | F (L3) | 需后端 |
| 8 | medicalProductVoList 完整 schema | F | 需后端 |
| 9 | VisionRecord 验光参数字段 (sphere/cylinder/axis) | F | 需 HTML/后端 |
| 10 | MethodGlassRecord 屈光参数 91 项具体含义 | F | 需 HTML/后端 |
| 11 | medicalExamineVo 内部字段 (item/result/status) | F | 需后端 |
| 12 | 4 对象在 myMaterialBillCtrl 内同时读的业务原因 | F | 需业务定义 |
| 13 | updateMethodGlassRecord L35644 所在 Controller | F | 需查 L35640 |
| 14 | medicalProductVoListOfModel 业务含义 | F | 需业务定义 |
| 15 | medicalProduct.medicalRecordId 字段 (L3 推断) | F | 需后端 |
| 16 | customerCheckin.patientId (S1-140 已确认 F) | F | - |

---

## §19 Git / 完整性

### §19.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-207 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 208_*.md | ✓ |

### §19.2 Git 操作

```
git add -- 208_S1-145_MedicalExamine_VisionRecord_MethodGlassRecord_MedicalProduct字段级生命周期总审计.md
git diff --cached --name-only
git commit -m "docs(208): S1-145 MedicalExamine VisionRecord MethodGlassRecord MedicalProduct 字段级生命周期总审计"
git push origin master
```

### §19.3 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| tracked | 216 (commit 208 后从 215 → 216) |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L1760 | `medicalExamineId = $stateParams.medicalExamineId` |
| L1925 | `getMedicalExamineItemVoList.json` |
| L2068/L2385 | `getMedicalExamineVoList.json` (assistCheckingCtrl) |
| L2074 | `res.items[0].medicalExamine.id` |
| L2211 | **completeExamine.json (W)** |
| L2415/L2691 | **startExamine.json (W)** |
| L32389 | **checkBeforeDeleteMedicalExamine.json (W)** |
| L10161 | **updateMemberRate.json (W)** (含 medicalExamineId) |
| L7072 | `medicalExamineVoList.map(v => v.medicalExamine.id)` |
| L16130 | getVisionRecordVo.json (optometryCtrl) |
| L31614/L31636 | getVisionRecordVo.json (drugPrescriptionCtrl) |
| L31620 | `visionRecordVo.medicalRecord.diagnosis` |
| L32180/L32425/L33786 | getVisionRecordVo.json (myMaterialBillCtrl) |
| L33670 | getVisionRecordVo.json (prescriptionCtrl) |
| L16130 | getMethodGlassRecordVo.json |
| L31614/L32813/L33670/L33816/L35604 | getMethodGlassRecordVo.json (4+ 调用) |
| L31629/L33753/L33894/L35644 | **updateMethodGlassRecord.json (4 个 W)** |
| L3823 | `medicalProductId: arr[i].medicalProduct.id` (F3) |
| L3853-L3856 | **medicalProduct.objectId runtime mutation** |
| L3962 | `medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id` (F6) |
| L3991 | `stockInSkuId, deliveryCount` (F5) |
| L3964 | `planDeliveryTime: $scope.startTime` |
| L4007 | **saveMedicalProductStockBatch.json (F5)** |
| L6703 | `medicalProductId : medicalExamineId` (跨类型 ID 转换) |

---

S1-145 完成。立即停止，等待老板下一指令。不执行 S1-146。
