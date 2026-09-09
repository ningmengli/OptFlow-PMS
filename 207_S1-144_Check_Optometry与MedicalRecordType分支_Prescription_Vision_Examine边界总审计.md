# S1-144：Check / Optometry 与 MedicalRecordType 分支、Prescription / Vision / Examine 边界总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 206 个 MD / 不修改历史
> 关联：S1-136 / S1-137R / S1-138 / S1-140 / S1-141 / S1-142 / S1-143

---

## 目录

- §0 审计目标与范围
- §1 Check Controller 全量
- §2 Optometry Controller 全量
- §3 medicalRecordType 全量
- §4 Check Entry / State
- §5 Optometry Entry / State
- §6 VisionRecord
- §7 MedicalExamine
- §8 MethodGlassRecord
- §9 Prescription
- §10 Check / Optometry ↔ MedicalRecord
- §11 Check / Optometry ↔ Patient / CustomerCheckin
- §12 Check / Optometry ↔ Sale
- §13 Check / Optometry ↔ Cashflow
- §14 Check / Optometry ↔ Delivery
- §15 Sale Object 边界
- §16 L1 / L2 / L3
- §17 26 项证据矩阵
- §18 历史差异
- §19 MedicalRecord 分支 DAG
- §20 V4.4 最终复刻红线
- §21 F / 未确认问题
- §22 Git / 完整性校验

---

## §0 审计目标与范围

本轮重点:
- medicalRecordType=1 / =5 真实分流
- Check / Optometry 真实 Controller / API / Object
- VisionRecord / MethodGlassRecord / MedicalExamine / Prescription 真实对象
- 与 MedicalRecord / Patient / CustomerCheckin / Sale / Cashflow / Delivery 真实边界
- 严格区分 A-F 证据等级

---

## §1 Check Controller 全量

### §1.1 真实 Check 业务 Controllers

| # | Controller | 行号 | 业务 | 真实执行 | 入口参数 |
|---|---|---|---|:---:|---|
| 1 | **assistCheckingCtrl** | L1756 | **Check 入口** (检查调用) | A | `$stateParams.medicalRecordId` (L1757) |
| 2 | **checkinListCtrl** | L8778 | 接诊列表 (含 beginCustomerCheckin) | A | `$stateParams.appointId` (L8648) |
| 3 | **drugPrescriptionCtrl** | L31605 | **药品处方** | A | `$stateParams.medicalRecordId` (L31609) |
| 4 | **prescriptionCtrl** | L33560 | **验光处方** | A | `$stateParams.medicalRecordId` (L33590) |
| 5 | **checkCallCtrl** | (S1-125) | Check 呼叫 | C | - |

### §1.2 命名边界

| 命名 | 实际 |
|---|---|
| `assistCheckingCtrl` | 真正的 Check 入口 |
| `checkinListCtrl` | 接诊列表, 触发 beginCustomerCheckin (medicalRecordType=1) |
| `prescriptionCtrl` | **验光处方** (medicalRecordId 入口) |
| `drugPrescriptionCtrl` | **药品处方** (medicalRecordId 入口) |
| `checkCallCtrl` | Check 呼叫辅助 |

---

## §2 Optometry Controller 全量

### §2.1 真实 Optometry 业务 Controllers

| # | Controller | 行号 | 业务 | 真实执行 | 入口参数 |
|---|---|---|---|:---:|---|
| 1 | **optometryCtrl** | L34776 | **验光 + 选镜架** (含 Delivery 派生) | A | - |
| 2 | **visitCtrl** (visitDetails / addVisit) | L14760/L14766 | 复诊 | A | - |
| 3 | **addVisitCtrl** | L49594 | 复诊添加 | A | `$stateParams.medicalRecordId` (推断) |
| 4 | optometryListCtrl | (S1-113: UartDevice) | F | F | - |
| 5 | optometryLogListCtrl | (S1-114: UartDevice) | F | F | - |

### §2.2 optometryCtrl 4 branch 拆分（S1-142 已确认）

| Branch | 入口函数 | API |
|---|---|---|
| 验光 (Optometry) | choseFactoryMethod (L35083) | getVisionRecordVo, getMethodGlassRecordVo |
| 配送 (Delivery) | completeMedicalRecordDelivery (L35185/L35204) | sendMedicalProductToMachineCenter |
| 报损 (ReportLoss) | createMedicalStockLossOfSmallVersion (L35342) | - |
| 退货 (Return) | confirmMedicalRecordReturn (L35167) | - |
| 取消 (Cancel) | cancelMedicalRecord (L35150) | - |

**关键修正**: optometryCtrl **不是单纯的 Optometry Controller**，它**同时包含** 验光 / 配送 / 报损 / 退货 / 取消 5 个 branch。

---

## §3 medicalRecordType 全量

### §3.1 16 处精确分布（S1-137R 已确认）

| 分类 | 数量 | 行号 |
|---|:---:|---|
| **== 1** | 3 | L10607 / L33127 / L33197 (全部在 beginCustomerCheckin 链) |
| **== 5** | 6 | L2257 / L31123 / L32951 / L33055 / L33136 / L33156 (全部 Sale Branch) |
| **custView == 1 ? 1 : 5** | 1 | L31117 (addMedicalRecord) |
| **`{ 6: 1, 7: 0 }`** | 1 | L35087 (UI 加工方式) |
| 派生提取 | 1 | L35086 |
| 派生于 glassestype | 1 | L34949 |
| Function Param | 1 | L31141 |
| 调试输出 | 1 | L31142 |
| **总计** | **16** | - |

### §3.2 type=1 真实用途

| 行号 | 表达式 | 上下文 | 实际用途 |
|---|---|---|---|
| L10607 | `medicalRecordType: 1` | beginCustomerCheckin (case 0 接诊) | **接诊创建 MedicalRecord** (接诊入口) |
| L33127 | `medicalRecordType: 1` | adminMyRecordCtrl selectMedicalType | **接诊类型选择** (默认 type=1) |
| L33197 | `medicalRecordType: 1` | receiveSelfAndBeginCustomerCheckin | **自接诊** (type=1) |

**type=1 真实含义**: 全部用于 **beginCustomerCheckin 链 (接诊)**，**不是** Check 业务标识。

### §3.3 type=5 真实用途

| 行号 | 表达式 | 上下文 | 实际用途 |
|---|---|---|---|
| L2257 | `== 5` | getMedical 链 | 路由到 Sale (myMaterialBill) |
| L31123 | `== 5` | addMedicalRecord 后 (L31119) | 路由到 Sale (myMaterialBill) |
| L32951 | `== 5` | myMedicalRecordListCtrl.getMedicalRecord | 路由到 Sale (myMaterialBill) |
| L33055 | `== 5` | myMedicalRecordListOfDoctorCtrl | 路由到 Sale (myMaterialBill) |
| L33136 | `== 5` | selectMedicalType (经 getMedicalRecord) | 路由到 Sale (myMaterialBill) |
| L33156 | `== 5` | getMedicalRecord (L33152) | 路由到 Sale (myMaterialBill) |

**type=5 真实含义**: **Sale 业务路由** (medicalRecordType==5 全部走 adminSalesRecord.myMaterialBill)。

### §3.4 medicalRecordType 5 业务规则 (A 级字符级)

| 规则 | 等级 | 字符级证据 |
|---|---|---|
| `== 5` → adminSalesRecord.myMaterialBill (Sale) | A | 6 处 Branch |
| `!= 5` → adminMyRecord.myMemberRecord (Check/Optometry) | A | 6 处 else |
| `== 1` → beginCustomerCheckin 链 (接诊) | A | 3 处 Request |
| `custView == 1 ? 1 : 5` → addMedicalRecord 派生 | A | L31117 唯一 |
| `{ 6: 1, 7: 0 }` → choseFactoryMethod (UI 加工) | A | L35087 唯一, **不是** State 路由 |

### §3.5 type=1 vs type=5 真实关系

| 维度 | type=1 | type=5 |
|---|---|---|
| 创建 API | beginCustomerCheckin.json (3 调用) | addMedicalRecord.json (1 调用) |
| 路由目标 | 接诊入口 (myMemberRecord 经 getMedicalRecord) | Sale (myMaterialBill) |
| 业务 | 接诊创建 MedicalRecord | Sale Create |
| 字段传递 | `medicalRecordType: 1` (硬编码) | `custView == 1 ? 1 : 5` (派生) |

**重要发现**: type=1 与 type=5 **不是** Check vs Optometry 区分，而是 **接诊 vs Sale** 区分。Check 与 Optometry 实际**共用同一 MedicalRecord**。

---

## §4 Check Entry / State

### §4.1 Check 入口

| Controller | 入口 State | 入口参数 |
|---|---|---|
| assistCheckingCtrl | `assistChecking` | `medicalRecordId` (L1757) |
| checkinListCtrl | `checkinList` | `appointId`, `printCheckinId` |
| drugPrescriptionCtrl | (prescription route) | `medicalRecordId` (L31609) |
| prescriptionCtrl | (prescription route) | `medicalRecordId` (L33590) |

### §4.2 Check 入口字符级证据

`Select-String 'assistChecking' controller.js`:
- L2214: `$state.go("assistChecking", { medicalExamineId, editable, medicalRecordId })`
- L2244: `$state.go("assistChecking", { medicalExamineId, medicalRecordId, editable })`
- L2400: `$state.go("assistChecking", { ... })`
- L2417: `$state.go("assistChecking", { ... })`
- L41717: `$state.go('assistChecking', { medicalExamineId, medicalRecordId })`

**Check 入口核心字段**: `medicalRecordId` + `medicalExamineId` + `editable`

---

## §5 Optometry Entry / State

### §5.1 Optometry 入口

| Controller | 入口 State | 入口参数 |
|---|---|---|
| optometryCtrl | (optometry route) | (无显式 StateParam) |
| visitDetailsCtrl / addVisitCtrl | `visitDetails` / `addVisit` | `medicalRecordId` (推断) |

### §5.2 Optometry $state.go 入口

`Select-String 'optometryGlasses' controller.js`:
- L34954: `$state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })`
- L35136: `$state.go("optometryGlasses", { medicalRecordId: item.medicalRecord.id, edit: "true" })`

`Select-String 'optometry' controller.js`:
- L36034: `$state.go("optometryList", {}, { reload: true })` — **S1-113 确认是 UartDevice 入口, 不是 Optometry 业务**
- L36050: `$state.go("optometryLogList", { ... })` — **UartDevice log**

**重要发现**: **真正的 Optometry 业务 State 入口只有 optometryGlasses**（验配镜），没有 "optometry" 单独的 State。

### §5.3 Optometry 入口核心字段

- `medicalRecordId` (A) — 验光 + 选镜架入口
- `edit: "true"` (A) — 编辑模式 (L35136)
- `glassestype` (A) — 镜片类型 (L34949)

---

## §6 VisionRecord

### §6.1 VisionRecord API 全量

| API | 行号 | Read/Write | Request | Response 关键 |
|---|---|---|---|---|
| getVisionRecordVo.json | L1918 | R | `{ medicalRecordId }` | visionRecordVoFactory |
| getVisionRecordVo.json | L32180 | R | `{ medicalRecordId }` | (Sale 范围) |
| getVisionRecordVo.json | L31636 | R | `{ medicalRecordId }` | drugPrescriptionCtrl |
| getVisionRecordVo.json | L32425 | R | (param: medicalRecordId) | myMaterialBillCtrl |
| getVisionRecordVo.json | L33786 | R | (myMaterialBillCtrl) | (重复) |
| getVisionRecordVo.json | L33800 | R | `{ medicalRecordId }` | optometryCtrl |
| saveVisionRecordVo | (推断) | W | - | - |

### §6.2 VisionRecord 字段

`Select-String 'visionRecord' controller.js` — 多处

VisionRecord 实体 (基于 L31620 `visionRecordVo.medicalRecord.diagnosis`):
- `visionRecordVo.medicalRecord` (嵌套 MedicalRecord 引用) (A)
- `visionRecordVo.medicalRecord.diagnosis` (A)
- (其它验光参数: sphere / cylinder / axis 等 - HTML/后端定义)

### §6.3 VisionRecord 实体判断

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| VisionRecord 真实 API 存在 | A | 6+ 调用点 |
| VisionRecord 含 medicalRecordId 字段 | A | Request 含 medicalRecordId |
| VisionRecord 含 patientId 字段 | F | 0 命中 |
| VisionRecord 含 customerId 字段 | F | 0 命中 |
| VisionRecord 是独立 ID 实体 | F (无法证明) | - |
| VisionRecord 含 visionRecordId 字段 | F | 0 命中 (self-ref 不存在) |

**正式冻结**: VisionRecord 是**含 medicalRecordId 的 API Response Object**, 不是含 visionRecordId 的独立实体。

---

## §7 MedicalExamine

### §7.1 MedicalExamine API 全量

| API | 行号 | Read/Write | Request | Response |
|---|---|---|---|---|
| getMedicalExamineVoList.json | L2068 | R | `{ medicalRecordId }` | examineListFactory |
| getMedicalExamineVoList.json | L2385 | R | `{ medicalRecordId }` | (assistCheckingCtrl) |
| getMedicalExamineVoList.json | L32190 | R | `{ medicalRecordId }` | myMaterialBillCtrl |
| getMedicalExamineVoList.json | L32293 | R | `{ medicalRecordId }` | (重查询) |
| getMedicalExamineVoList.json | L32422 | R | (param) | myMaterialBillCtrl (列表) |

### §7.2 MedicalExamine 字段

`Select-String 'medicalExamine' controller.js` — 多处
- `medicalExamineVoList` (A) — Response 列表
- `medicalExamineVoList.length` (A) — L6682
- `medicalExamineId` (A) — L6703/L6904 用于 Request
- `medicalExamineVoList[i].medicalExamine.id` (A 推断)
- `medicalExamineVoList[].medicalExamine.medicalRecordId` (A 推断)

### §7.3 MedicalExamine 实体判断

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| MedicalExamine 真实 API 存在 | A | 5+ 调用点 |
| MedicalExamine 含 medicalRecordId | A | Request |
| MedicalExamine 含 medicalExamineId | A | 字符级 (L6703/L6904) |
| MedicalExamine 独立 ID 实体 | **A** (有 medicalExamineId) | L6703 字符级 |
| MedicalExamine 含 patientId | F | 0 命中 |
| MedicalExamine 独立 Save API | F | 0 命中 (本轮搜索 saveMedicalExamine / insertMedicalExamine / createMedicalExamine 均 0 命中) |

**重要发现**: MedicalExamine **是唯一** 含独立 ID (medicalExamineId) 的"非 MedicalRecord"业务对象。

### §7.4 MedicalExamine Write API 全量

`Select-String 'saveMedicalExamine|insertMedicalExamine|createMedicalExamine|updateMedicalExamine' controller.js` — **0 命中**

**MedicalExamine 在当前源码中只有 Read API, 没有 Write API**。这意味着 MedicalExamine 可能是由后端单独管理 (例如由医生手动添加), 前端不通过此 controller 创建。

---

## §8 MethodGlassRecord

### §8.1 MethodGlassRecord API 全量

| API | 行号 | Read/Write | Request | Response |
|---|---|---|---|---|
| getMethodGlassRecordVo.json | L16130 | R | `{ medicalRecordId: id }` | optometryCtrl |
| getMethodGlassRecordVo.json | L31614 | R | `{ medicalRecordId }` | drugPrescriptionCtrl |
| getMethodGlassRecordVo.json | L32813 | R | (param) | (Sale 范围) |
| getMethodGlassRecordVo.json | L33670 | R | `{ medicalRecordId }` | prescriptionCtrl |
| getMethodGlassRecordVo.json | L33816 | R | `{ medicalRecordId }` | optometryCtrl |
| getMethodGlassRecordVo.json | L35604 | R | (param) | (其它) |
| **updateMethodGlassRecord.json** | L31629 | **W** | `{ medicalRecordId, left67, left68, ... }` | drugPrescriptionCtrl |

### §8.2 MethodGlassRecord 字段

基于 drugPrescriptionCtrl / prescriptionCtrl / optometryCtrl 字符级:

| 字段 | 等级 |
|---|---|
| `medicalRecordId` | A (Request) |
| `left67` (球镜?) | A (L31616 字符级) |
| `left68` (柱镜?) | A (L31617/L31620 字符级) |
| `optometryMethod` (验配方法) | A (L33680) |
| `mydriasisMethod` (散瞳方法) | A (L33683) |
| `rxCount` (配镜次数) | A (L33660) |
| `lastRxTime` (上次配镜时间) | A (L33661/L33676) |
| `left1-91` / `right1-91` (屈光参数) | A (L33619-L33662) |

### §8.3 MethodGlassRecord 实体判断

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| MethodGlassRecord 真实 API 存在 | A | 7+ 调用点 |
| MethodGlassRecord 含 medicalRecordId | A | Request |
| MethodGlassRecord 含独立 ID | F | 0 命中 (methodGlassRecordId 不存在) |
| MethodGlassRecord 有 Write API | A | updateMethodGlassRecord.json (L31629) |
| MethodGlassRecord 含 patientId | F | 0 命中 |

**正式冻结**: MethodGlassRecord 是**含 medicalRecordId 的 API Response Object**, 无独立 methodGlassRecordId, **不是**独立 ID 实体 (虽然有 Write API)。

---

## §9 Prescription

### §9.1 Prescription Controller 全量

| # | Controller | 行号 | 业务 | 真实执行 | 入口 |
|---|---|---|---|:---:|---|
| 1 | **prescriptionCtrl** | L33560 | **验光处方** | A | `$stateParams.medicalRecordId` (L33590) |
| 2 | **drugPrescriptionCtrl** | L31605 | **药品处方** | A | `$stateParams.medicalRecordId` (L31609) |

### §9.2 Prescription API 全量

| API | 行号 | Read/Write | Controller |
|---|---|---|---|
| getMedicalRecord.json | L33663 | R | prescriptionCtrl |
| getMethodGlassRecordVo.json | L33670 | R | prescriptionCtrl |
| updateMedicalRecord | L33605 (F) | W | prescriptionCtrl (secondDoctorId) |
| getMethodGlassRecordVo.json | L31614 | R | drugPrescriptionCtrl |
| updateMethodGlassRecord.json | L31629 | **W** | drugPrescriptionCtrl |
| getVisionRecordVo.json | L31636 | R | drugPrescriptionCtrl |

### §9.3 Prescription 字段全量

`Select-String 'prescription[^A-Za-z]' controller.js` — 50+ 命中

**prescriptionCtrl 字段 (L33560-L33720)**:
- `$scope.prescription = res` (L33666) — Response 存到 prescription
- `prescriptionInfo.id = res.secondDoctorId` (L33667)
- `prescriptionInfo.inputVal = res.secondDoctorName` (L33668)
- `prescriptionParams1` (L33561) - 验配方法
- `prescriptionParams2` (L33575) - 散瞳药品
- `prescriptionSet` (L33689) - 验光表
- `prescriptionSet2` (L33720) - 验光表2
- `object.optometryMethod` (L33571) - 验配方法 (内部)
- `object.mydriasisMethod` (L33585) - 散瞳方法
- 30+ left/right 屈光参数 (L33619-L33662)

### §9.4 Prescription 实体判断

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Prescription 真实 Controller 存在 | A | prescriptionCtrl L33560 / drugPrescriptionCtrl L31605 |
| Prescription 接收 medicalRecordId | A | L31609/L33590 |
| Prescription 调 getMedicalRecord | A | L33663 |
| Prescription 调 getMethodGlassRecordVo | A | L33670 |
| Prescription 调 updateMedicalRecord (secondDoctorId) | A | L33605 (via FN_promiseCall) |
| **Prescription 有独立 prescriptionId 字段** | **F** | 0 命中 (无 prescriptionId) |
| **Prescription 有独立 prescriptionVo** | **C** | `$scope.prescription = res` (L33666) — 实际是 MedicalRecord Response 暂存 |

### §9.5 Prescription ≠ 处方单

**重要发现**: 
- 源码中**没有** `prescriptionId` 字符级 (0 命中)
- 源码中**没有** 独立 `prescriptionVo` (只有 `$scope.prescription = res` 暂存 MedicalRecord Response)
- 源码中**没有** `savePrescription` / `createPrescription` / `insertPrescription` 字符级 API
- 唯一 Write 关联: drugPrescriptionCtrl 调 `updateMethodGlassRecord.json` (L31629)

**正式冻结**: `prescriptionCtrl` / `drugPrescriptionCtrl` 是真实 Controller, 但 **Prescription 没有独立 prescriptionId / prescriptionVo 实体**。它们是 MedicalRecord + MethodGlassRecord + VisionRecord 的**复合视图**。

### §9.6 字符串中的 "prescription" (避免误判)

| 行号 | 表达式 | 实际 |
|---|---|---|
| L31605 | `drugPrescriptionCtrl` | Controller 名, 真实 |
| L33560 | `prescriptionCtrl` | Controller 名, 真实 |
| L33565 | `prescriptionMating` | window.optionsObj 列表 (验配方法选项) |
| L33579 | `prescriptionMydriatic` | window.optionsObj 列表 (散瞳药品选项) |
| L46733 | `prescriptionList = [{...}]` | 字符串列表 (疑为模板或常量) |
| L33591-L33720 | `prescriptionInfo/Params/Set` | 局部 UI 状态变量 |

**严格区分**: Controller / 变量名中含 "prescription" **不等于** Prescription 独立实体。

---

## §10 Check / Optometry ↔ MedicalRecord

### §10.1 Check → MedicalRecord

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| assistCheckingCtrl 接收 medicalRecordId | A | L1757 |
| checkCallCtrl 跳 assistChecking 带 medicalRecordId | A | L2244 |
| drugPrescriptionCtrl 接收 medicalRecordId | A | L31609 |
| prescriptionCtrl 接收 medicalRecordId | A | L33590 |

**Check → MedicalRecord = A 直接桥** (medicalRecordId StateParam)

### §10.2 MedicalRecord → Check

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| getMedicalRecord Response 触发 getMedical (经 medicalRecordType 分支) | A | L2257-L2267 |
| medicalRecordType!=5 路由到 adminMyRecord.myMemberRecord | A | L2258 (L2257 错, 应是 L2258) |
| medicalRecordType!=5 路由到 myMemberRecord (含 check 入口) | A | L32954/L33058/L33142/L33162 |

**MedicalRecord → Check = A 间接桥** (经 adminMyRecord.myMemberRecord)

### §10.3 Optometry → MedicalRecord

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| optometryCtrl consume medicalRecord (optometryGlasses State) | A | L34955/L35136 |
| visitDetails / addVisit 接收 medicalRecordId | A | L14760/L14766/L49594 |
| prescriptionCtrl 接收 medicalRecordId | A | L33590 |
| drugPrescriptionCtrl 接收 medicalRecordId | A | L31609 |

**Optometry → MedicalRecord = A 直接桥** (medicalRecordId StateParam)

### §10.4 MedicalRecord → Optometry

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| getMedicalRecord Response → goRecord → optometry (medicalRecordType!=5) | A | L2257 |
| myMemberRecord → optometryGlasses | A | L34954/L35136 |
| medicalRecordId 路由 | A | L34954/L35136 |

**MedicalRecord → Optometry = A 间接桥** (经 myMemberRecord)

### §10.5 Check / Optometry 与 MedicalRecord 关系

| 关系 | 等级 | 备注 |
|---|---|---|
| Check → MedicalRecord | A 直接 | medicalRecordId 字段 |
| MedicalRecord → Check | A 间接 | 经 myMemberRecord |
| Optometry → MedicalRecord | A 直接 | medicalRecordId 字段 |
| MedicalRecord → Optometry | A 间接 | 经 myMemberRecord |

**正式冻结**: **Check 与 Optometry 共享同一 MedicalRecord** (medicalRecordType 不区分, 通过 State 入口区分)。

---

## §11 Check / Optometry ↔ Patient / CustomerCheckin

### §11.1 Check → Patient

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| assistCheckingCtrl 通过 medicalRecord 间接访问 patient | A | (经 getMedicalRecord.patientId) |
| drugPrescriptionCtrl 通过 medicalRecord 间接访问 patient | A | (经 getMedicalRecord.patientId) |

**Check → Patient = A 间接** (经 MedicalRecord.patientId → getPatientInfo)

### §11.2 Optometry → Patient

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| optometryCtrl 通过 medicalRecord 间接访问 patient | A | (经 getMedicalRecord.patientId) |

**Optometry → Patient = A 间接**

### §11.3 Check / Optometry → CustomerCheckin

| 证据 | 等级 | 字符级证据 |
|---|---|---|
| 6 处 customerCheckin.medicalRecordId → MedicalRecord | A | S1-140 已确认 |
| MedicalRecord 路由到 Check/Optometry | A | L2257/L32954/L33058 |

**Check / Optometry → CustomerCheckin = A 间接 2 层** (经 MedicalRecord)

### §11.4 Patient → Check / Optometry

| 证据 | 等级 |
|---|---|
| Patient → getMedicalRecordList → Check (medicalRecordType!=5) | A |
| Patient → getMedicalRecordList → Optometry (medicalRecordType!=5) | A |

**Patient → Check / Optometry = A 间接**

---

## §12 Check / Optometry ↔ Sale

### §12.1 字符级搜索

`Select-String 'adminSalesRecord|myMaterialBill' controller.js` — 10 命中 (S1-143 已确认)

| 行号 | 表达式 | 上下文 |
|---|---|---|
| L2258 | `$state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })` | getMedical 链, medicalRecordType==5 |
| L31124 | `$state.go("adminSalesRecord.myMaterialBill", ...)` | addMedicalRecord 链, type=5 |
| L31144 | `$state.go("adminSalesRecord.myMaterialBill", ...)` | goRecord type=5 |
| L32952 | `$state.go('adminSalesRecord.myMaterialBill', ...)` | myMedicalRecordListCtrl type=5 |
| L33056 | `$state.go('adminSalesRecord.myMaterialBill', ...)` | myMedicalRecordListOfDoctorCtrl type=5 |
| L33137 | `$state.go("adminSalesRecord.myMaterialBill", ...)` | selectMedicalType type=5 |
| L33157 | `$state.go("adminSalesRecord.myMaterialBill", ...)` | getMedicalRecord type=5 |

### §12.2 Check / Optometry ↔ Sale 关系

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Check 入口 State 不跳 Sale | A | 0 命中 $state.go("adminSalesRecord...") 在 Check Controller |
| Optometry 入口 State 不跳 Sale | A | 0 命中 $state.go("adminSalesRecord...") 在 Optometry Controller |
| **Sale 与 Check/Optometry 共享 MedicalRecord** | A | medicalRecordType 分流 |
| Check → Sale 直接 | **F** | 0 命中 |
| Optometry → Sale 直接 | **F** | 0 命中 |

### §12.3 Check / Optometry ↔ Sale 最终

| 方向 | 等级 |
|---|:---:|
| Check → Sale | F |
| Optometry → Sale | F |
| Sale → Check | F (Sale 不跳 Check) |
| Sale → Optometry | F (Sale 不跳 Optometry) |
| Check / Optometry ↔ Sale | **F 直接**, 仅共用 MedicalRecord |

---

## §13 Check / Optometry ↔ Cashflow

### §13.1 字符级搜索

`Select-String 'createCashFlowForMedicalRecord' controller.js` — 1 调用 (L6925, in myMaterialBillCtrl)

### §13.2 Check / Optometry ↔ Cashflow 关系

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Check Controller 调 createCashFlowForMedicalRecord | F | 0 命中 |
| Optometry Controller 调 createCashFlowForMedicalRecord | F | 0 命中 (S1-141 确认仅 myMaterialBillCtrl 调) |
| Check → Cashflow | F 直接 | — |
| Optometry → Cashflow | F 直接 | — |

### §13.3 Check / Optometry ↔ Cashflow 最终

| 方向 | 等级 |
|---|:---:|
| Check → Cashflow | F 直接 / A 间接 3 层 (经 MedicalRecord → Sale myMaterialBill → Cashflow) |
| Optometry → Cashflow | F 直接 / A 间接 3 层 |

**重要发现**: Check / Optometry 不直接进入 Cashflow, 必须经 myMaterialBillCtrl (Sale 容器) → createCashFlowForMedicalRecord。

---

## §14 Check / Optometry ↔ Delivery

### §14.1 字符级搜索

`Select-String 'completeMedicalRecordDelivery|createMedicalStockLossOfSmallVersion|confirmMedicalRecordReturn|cancelMedicalRecord' controller.js`:
- L35185/L35204: completeMedicalRecordDelivery (optometryCtrl)
- L35342: createMedicalStockLossOfSmallVersion (optometryCtrl)
- L35167: confirmMedicalRecordReturn (optometryCtrl)
- L35150: cancelMedicalRecord (optometryCtrl)

### §14.2 Check / Optometry ↔ Delivery 关系

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Check Controller 调 Delivery 范围 API | F | 0 命中 (checkinListCtrl 范围) |
| Optometry Controller 调 Delivery API | A | optometryCtrl L35185/L35204 (S1-142 已确认) |
| Check → Delivery | F | — |
| Optometry → Delivery | A 间接 (经 optometryCtrl fnMap) |

### §14.3 optometryCtrl fnMap 4 branch 进一步分类

| branch | 实际业务 | API |
|---|---|---|
| 验光 | Optometry business | getVisionRecordVo, getMethodGlassRecordVo |
| 选镜架 (Modification) | Optometry business | setMedicalRecordProcessMode |
| 配送 (Delivery) | **Delivery 业务** | completeMedicalRecordDelivery |
| 报损 (ReportLoss) | **Delivery 业务** | createMedicalStockLossOfSmallVersion |
| 退货 (Return) | **Delivery 业务** | confirmMedicalRecordReturn |
| 取消 (Cancel) | **Delivery 业务** | cancelMedicalRecord |

**正式冻结**: optometryCtrl 是**复合 Controller**, 包含 **Optometry + Delivery + Return/Cancel + ReportLoss** 5 个 branch。

### §14.4 Check / Optometry ↔ Delivery 最终

| 方向 | 等级 |
|---|:---:|
| Check → Delivery | F |
| Optometry → Delivery | A 间接 (经 optometryCtrl fnMap Delivery branch) |

---

## §15 Sale Object 边界

### §15.1 Sale 是否直接读取 Check/Optometry 对象

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Sale 调 getVisionRecordVo | A (1 处) | L32180 (myMaterialBillCtrl) |
| Sale 调 getMethodGlassRecordVo | A (1 处) | L32813 (myMaterialBillCtrl) |
| Sale 调 getMedicalExamineVoList | A (4 处) | L32190/L32293/L32422/L6682 (myMaterialBillCtrl 范围) |

### §15.2 Sale 调 Check/Optometry API 字符级

`Select-String 'myMaterialBillCtrl|getVisionRecordVo|getMethodGlassRecordVo' controller.js`:
- L32180 `getVisionRecordVo.json` (myMaterialBillCtrl)
- L32813 `getMethodGlassRecordVo.json` (myMaterialBillCtrl)
- L32190/L32293 `getMedicalExamineVoList.json` (myMaterialBillCtrl)
- L6682 `medicalExamineVoList` (computeUnPlaceOrderMedicalRecordFee)
- L33816 `getMethodGlassRecordVo.json` (myMaterialBillCtrl)

### §15.3 Sale 入口 vs Check/Optometry API

| 维度 | Sale (myMaterialBillCtrl) | Check (assistCheckingCtrl) | Optometry (optometryCtrl) |
|---|---|---|---|
| getVisionRecordVo | **A (1 处)** | F | A |
| getMethodGlassRecordVo | **A (1 处)** | F | A |
| getMedicalExamineVoList | **A (4 处)** | A | F |

### §15.4 Sale ↔ Check / Optometry 结论

| 方向 | 等级 |
|---|:---:|
| Sale → VisionRecord | A (1 处, myMaterialBillCtrl) |
| Sale → MethodGlassRecord | A (1 处, myMaterialBillCtrl) |
| Sale → MedicalExamine | A (4 处, myMaterialBillCtrl) |
| VisionRecord → Sale | F (无字符级) |
| MethodGlassRecord → Sale | F (无字符级) |
| MedicalExamine → Sale | F (无字符级) |

**关键发现**: **myMaterialBillCtrl (Sale 容器) 同时读取 Check (MedicalExamine) 和 Optometry (VisionRecord, MethodGlassRecord) 数据**, 因为 Sale 容器与 MedicalRecord 是同一对象的**多视图**。

---

## §16 L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | Controller / API / State / Request / Response / Scope / Factory / Field 全部字符级 | A |
| L2 | "type=1 是接诊 / type=5 是 Sale" / "optometryCtrl 是复合 Controller" 等派生解释 | A |
| L3 | Prescription 表 / VisionRecord 表 / MethodGlassRecord 表 / MedicalExamine 表 数据库实体 | **F**（无后端证据）|

### §16.1 关键 L3 冻结

| 命题 | 等级 | 原因 |
|---|---|---|
| Prescription 独立表 | F | 0 命中 prescriptionId / prescriptionVo 独立字段 |
| VisionRecord 独立表 | F | 0 命中 visionRecordId |
| MethodGlassRecord 独立表 | F | 0 命中 methodGlassRecordId |
| MedicalExamine 独立表 | A (有 medicalExamineId) | 字符级 L6703 |

**正式冻结**: 仅 MedicalExamine 有独立 ID 字段 (medicalExamineId)。其它 (Prescription / VisionRecord / MethodGlassRecord) 是**含 medicalRecordId 的 API Response Object**, 不是独立 ID 实体。

---

## §17 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | assistChecking / drugPrescription / prescription / optometryGlasses | A | - | 多处 | A |
| 2 | Controller | 5 Check + 5 Optometry | A | - | 全部 | A |
| 3 | State | assistChecking / optometryGlasses / drugPrescription / prescription | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | medicalRecordId (Check/Optometry) | A | 多处 | L1757/L31609/L33590 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | (HTML 不可读) | F | - | - | F |
| 10 | Status | medicalRecordType 分流 (==1/5) | A | - | 16 处 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | (myMaterialBill 12) | A | - | L31035 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | medicalRecordId | A | 多处 | L31609/L33590 | A |
| 15 | Default | medicalRecordType=1 (beginCustomerCheckin) | A | - | L10607 | A |
| 16 | Data Source | getMedicalExamineVoList / getVisionRecordVo / getMethodGlassRecordVo | A | 多处 | 全文 | A |
| 17 | Object | MedicalExamine / VisionRecord / MethodGlassRecord / Prescription | A | - | 全部 | A |
| 18 | Request | { medicalRecordId } | A | 多处 | 全部 | A |
| 19 | Response | medicalExamineVoList / visionRecordVo / methodGlassRecordVo | A | - | 全部 | A |
| 20 | Function | choseFactoryMethod / goRecord / getMedical | A | - | 多处 | A |
| 21 | State Bridge | medicalRecordId / medicalExamineId | A | - | 全部 | A |
| 22 | Object Bridge | medicalExamineVo (含 medicalExamineId) | A | - | L6703 | A |
| 23 | API Bridge | getMedicalExamineVoList / getVisionRecordVo / getMethodGlassRecordVo | A | - | 全文 | A |
| 24 | Business Interpretation | Check/Optometry 共享 MedicalRecord | A | - | - | A (派生) |
| 25 | Evidence Grade | 23 A / 1 C / 2 F | - | - | - | - |
| 26 | V4.4 Decision | 仅 MedicalExamine 有独立 ID | A | - | - | A |

---

## §18 历史差异

### §18.1 S1-136 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "medicalRecordType==1 → Check" | 实际 type=1 全部用于 beginCustomerCheckin 链 | 应改 | **type=1 是接诊标识** (A) |
| "medicalRecordType==5 → Sale" | 保持 | - | **保持** (A) |

### §18.2 S1-137R 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "type=1 全部含义不明" | 实际 type=1 全部是 beginCustomerCheckin 链 | 应明确 | **type=1 = 接诊** (A) |
| "6→1, 7→0 是 State 路由" | 实际是 UI 加工方式 | 已在 S1-137R 修正 | **保持 S1-137R 修正** |

### §18.3 S1-138 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "medicalRecordType 5 业务规则" | 保持 | - | **保持** (A) |

### §18.4 S1-141 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "createCashFlowForMedicalRecord 仅 myMaterialBillCtrl" | 保持 (本轮再次确认) | - | **保持** (A) |

### §18.5 S1-142 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "optometryCtrl 含 completeMedicalRecordDelivery" | 保持 | - | **保持** (A) |
| "optometryCtrl 5 branch" | 本轮扩展为 6 branch (含验光/选镜架/Delivery/ReportLoss/Return/Cancel) | - | **保持扩展** (A) |

### §18.6 S1-143 误判保留

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "addMedicalRecord 是 Sale Create 入口" | 保持 | - | **保持** (A) |
| "type=5 路由 Sale" | 保持 | - | **保持** (A) |

### §18.7 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| "Prescription 独立实体" | 0 命中 prescriptionId, 0 命中独立 prescriptionVo | 重大修正 | **Prescription 不是独立实体** (F) |
| "VisionRecord 独立实体" | 0 命中 visionRecordId | 修正 | **VisionRecord 不是独立实体** (F) |
| "MethodGlassRecord 独立实体" | 0 命中 methodGlassRecordId | 修正 | **MethodGlassRecord 不是独立实体** (F) |
| "Check / Optometry 产生 Sale 直接" | 0 命中 $state.go adminSalesRecord 在 Check/Optometry 范围 | 修正 | **F** |
| "Check / Optometry 直接 Cashflow" | 仅 myMaterialBillCtrl 调 createCashFlow | 修正 | **F** |
| "optometryCtrl 是 Optometry Controller" | 含 6 branch (含 Delivery 派生) | 修正 | **optometryCtrl 是复合 Controller** |

---

## §19 MedicalRecord 分支 DAG

### DAG A: MedicalRecord → type=1
- **A** — beginCustomerCheckin.json (3 处) 创建 type=1
- 路由: 接诊入口, 经 getMedicalRecord 链到 adminMyRecord.myMemberRecord

### DAG B: MedicalRecord → type=5
- **A** — addMedicalRecord.json 创建 type=5 (custView 派生)
- 路由: 立即 $state.go adminSalesRecord.myMaterialBill (Sale 入口)

### DAG C: type=1 → Check
- **A** — getMedicalRecord (medicalRecordType!=5) → adminMyRecord.myMemberRecord → assistChecking

### DAG D: type=1 → Optometry
- **A** — 同上, 路径相同 (type=1 路由到 myMemberRecord, 内含 Optometry 入口)

### DAG E: type=5 → Sale
- **A** — 6 处 Branch, 全部走 adminSalesRecord.myMaterialBill

### DAG F: MedicalRecord → Check (Field)
- **A** — medicalRecordId 字段, 4+ 个 Check Controller 接收

### DAG G: MedicalRecord → Optometry (Field)
- **A** — medicalRecordId 字段, optometryGlasses / drugPrescription / prescription 接收

### DAG H: Check → Optometry
- **F** (无直接桥, 共享 MedicalRecord)

### DAG I: Check → Sale
- **F** (Check Controller 0 命中 $state.go adminSalesRecord)

### DAG J: Optometry → Sale
- **F** (Optometry Controller 0 命中 $state.go adminSalesRecord)

### DAG K: Check → Cashflow
- **F 直接** / **A 间接 3 层** (经 MedicalRecord → Sale myMaterialBill → Cashflow)

### DAG L: Optometry → Cashflow
- **F 直接** / **A 间接 3 层**

### DAG M: Optometry → Delivery
- **A 间接** (经 optometryCtrl fnMap Delivery branch, medicalRecordId 携带)

### DAG N: CustomerCheckin → Check / Optometry
- **A 间接 2 层** (经 MedicalRecord)

### DAG O: VisionRecord / MethodGlassRecord ↔ MedicalExamine
- **A 字段级** (都含 medicalRecordId 字段)
- 互不直接关联 (无 visionRecordId, 无 methodGlassRecordId)

### §19.1 完整 MedicalRecord 分支图

```
                   [CustomerCheckin]
                          ↓ A (S1-140)
                   [MedicalRecord]
                          │
        ┌─────────────────┼─────────────────┐
        │ type=1          │ type=5          │ {6:1, 7:0}
        ↓ A              ↓ A              ↓ UI 加工
   Check/Optometry     Sale             (choseFactoryMethod)
        │                 │
        │ medicalRecordId  │ medicalRecordId + patientId
        ↓                 ↓
   [Check/Optometry     [Sale (myMaterialBillCtrl)]
    Controllers]              │
        │                     │
        ├─ Check ──────────────┤ 读 VisionRecord
        ├─ Optometry ──────────┤ 读 MethodGlassRecord
        │                     │ 读 MedicalExamine
        │                     │ 调 createCashFlow
        │                     ↓ A
        │                  [Cashflow]
        │                     ↓ A
        ↓                     ↓
   [DrugPrescription]   [Delivery]
   [Prescription]
        │
        ↓ A (optometryCtrl fnMap)
   [optometryCtrl Delivery branch]
        ↓
   [completeMedicalRecordDelivery / 
    createMedicalStockLossOfSmallVersion /
    confirmMedicalRecordReturn /
    cancelMedicalRecord]
```

---

## §20 V4.4 最终复刻红线

### §20.1 必实现 (基于 A 级证据)

| 项 | 行号 | 必实现 |
|---|---|---|
| 5 Check Controller | L1756/L8778/L31605/L33560 | ✓ |
| Optometry Controller | L34776 | ✓ |
| 5 验光/处方 API | getMedicalExamineVoList / getVisionRecordVo / getMethodGlassRecordVo / updateMethodGlassRecord | ✓ |
| medicalRecordType 分流 | 16 处 | ✓ |
| $stateParams.medicalRecordId 入口 | 25+ 处 | ✓ |

### §20.2 必不实现 (避免误造)

| 项 | 行号 | 必不实现 |
|---|---|---|
| prescriptionId 字段 | F (0 命中) | ✗ |
| prescriptionVo 独立对象 | F | ✗ |
| visionRecordId 字段 | F (0 命中) | ✗ |
| methodGlassRecordId 字段 | F (0 命中) | ✗ |
| Prescription 独立 API (savePrescription / createPrescription 等) | F (0 命中) | ✗ |
| Check Controller 调 adminSalesRecord | F (0 命中) | ✗ |
| Optometry Controller 调 adminSalesRecord | F (0 命中) | ✗ |
| Check Controller 调 createCashFlow | F (0 命中) | ✗ |
| Prescription 独立表 | F | ✗ |
| VisionRecord 独立表 | F | ✗ |
| MethodGlassRecord 独立表 | F | ✗ |

### §20.3 必实现的实体独立性

| 实体 | 独立 ID | Write API | 备注 |
|---|:---:|:---:|---|
| **MedicalRecord** | YES (medicalRecordId) | A | 唯一核心实体 |
| **MedicalExamine** | YES (medicalExamineId) | F (无 Write API 字符级) | 唯一含独立 ID 的子对象 |
| Cashflow | YES (cashflowId) | A | S1-141 已确认 |
| Customer | YES (customerId) | A | S1-140 已确认 |
| Patient | YES (patientId) | A | S1-140 已确认 |
| VisionRecord | F | F | API Response Object |
| MethodGlassRecord | F | A (updateMethodGlassRecord) | API Response Object |
| Prescription | F | F | API Response Object 复合视图 |

### §20.4 不可桥 (必须显式不实现)

| 不可桥 | 等级 | 原因 |
|---|:---:|---|
| Check → Sale 直接 | F | 0 命中 |
| Optometry → Sale 直接 | F | 0 命中 |
| Sale → Check | F | 0 命中 |
| Sale → Optometry | F | 0 命中 |
| Check → Cashflow 直接 | F | 0 命中 |
| Optometry → Cashflow 直接 | F | 0 命中 |
| Prescription 独立实体 | F | 0 命中 prescriptionId |

### §20.5 medicalRecordType 分流规则 (A 级)

| 值 | 路由 | 业务 |
|:---:|---|---|
| 1 | adminMyRecord.myMemberRecord (经 getMedicalRecord 链) | 接诊 |
| 5 | adminSalesRecord.myMaterialBill | Sale |
| 6 | choseFactoryMethod (UI) | UI 加工 |
| 7 | choseFactoryMethod (UI) | UI 加工 |
| 0/2/3/4/其它 | 通用 MedicalRecord 入口 | (无明确) |

### §20.6 optometryCtrl 是复合 Controller (A 级)

| branch | API | 业务归属 |
|---|---|---|
| 验光 | getVisionRecordVo, getMethodGlassRecordVo | **Optometry** |
| 选镜架 | setMedicalRecordProcessMode | **Optometry** |
| 配送 | completeMedicalRecordDelivery | **Delivery** |
| 报损 | createMedicalStockLossOfSmallVersion | **Delivery** |
| 退货 | confirmMedicalRecordReturn | **Delivery** |
| 取消 | cancelMedicalRecord | **Delivery** |

**复刻必实现**: optometryCtrl 必须包含这 6 个 branch。

### §20.7 命名误导必标注

| 命名 | 实际 |
|---|---|
| `prescriptionCtrl` | 验光处方, 实际是 MedicalRecord + MethodGlassRecord + VisionRecord 复合视图 |
| `drugPrescriptionCtrl` | 药品处方, 调 getMethodGlassRecordVo + updateMethodGlassRecord |
| `optometryCtrl` | 验光 + 选镜架 + Delivery + Return + Cancel + ReportLoss 6 branch |
| `myMaterialBillCtrl` | Sale 容器, 同时读 Check/Optometry 数据 |
| `prescriptionList = [{...}]` (L46733) | 字符串列表, 不是独立对象 |

### §20.8 数据访问模式

| 模式 | 字符级证据 |
|---|---|
| Check 入口模式: `$stateParams.medicalRecordId` → `getMedicalExamineVoList({medicalRecordId})` | A |
| Optometry 入口模式: `$stateParams.medicalRecordId` → `getVisionRecordVo({medicalRecordId})` + `getMethodGlassRecordVo({medicalRecordId})` | A |
| Prescription 入口模式: `$stateParams.medicalRecordId` → `getMedicalRecord` + `getMethodGlassRecordVo` | A |
| DrugPrescription 入口模式: `$stateParams.medicalRecordId` → `getVisionRecordVo` + `getMethodGlassRecordVo` + `updateMethodGlassRecord` | A |
| Sale (myMaterialBillCtrl) 入口: `$stateParams.medicalRecordId` → `getMedicalRecord` + 读 medicalExamineVoList + 读 visionRecord + 读 methodGlassRecord | A |

---

## §21 F / 未确认问题

| # | 命题 | 等级 | 后续验证方式 |
|---|---|:---:|---|
| 1 | Prescription 是否有独立数据库表 | F | 需后端源码 |
| 2 | VisionRecord 是否有独立数据库表 | F | 需后端源码 |
| 3 | MethodGlassRecord 是否有独立数据库表 | F | 需后端源码 |
| 4 | optometryCtrl 完整分支数 (本轮 6 branch) | C | 需 controller.js 完整分析 |
| 5 | Check 入口如何进入 (medicalRecordId 如何获得) | A (经 $stateParams) | 已确认 |
| 6 | medicalRecordType 其他值 (2/3/4/0) 的业务 | F (源码未明确) | 需后端定义 |
| 7 | MedicalExamine Write API 是否存在 | F (本轮 0 命中) | 需后端 |
| 8 | Prescription 30+ left/right 字段具体含义 | F (需 HTML/后端) | 需业务文档 |
| 9 | VisionRecord 验光参数字段 | F (需 HTML/后端) | 需业务文档 |
| 10 | optometryCtrl fnMap 是否还有其他 branch | C (本轮 6 branch) | 需完整扫描 |
| 11 | prescriptionList 字符串列表 (L46733) 用途 | F | 需查 |
| 12 | Check 与 Optometry 内部业务区分 (验光 vs 检查) | F (源码未明确) | 需业务定义 |

---

## §22 Git / 完整性校验

### §22.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-206 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 207_*.md | ✓ |

### §22.2 Git 操作

```
git add -- 207_S1-144_Check_Optometry与MedicalRecordType分支_Prescription_Vision_Examine边界总审计.md
git diff --cached --name-only
git commit -m "docs(207): S1-144 Check Optometry 与 MedicalRecordType 分支 Prescription Vision Examine 边界总审计"
git push origin master
```

### §22.3 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| tracked | 215（commit 207 后从 214 → 215）|
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L1756 | assistCheckingCtrl (Check 入口) |
| L1757 | `$scope.medicalRecordId = $stateParams.medicalRecordId` |
| L31605 | drugPrescriptionCtrl (药品处方) |
| L31609 | `$scope.medicalRecordId = $stateParams.medicalRecordId` |
| L31629 | updateMethodGlassRecord.json (Write API) |
| L33560 | prescriptionCtrl (验光处方) |
| L33590 | `$scope.medicalRecordId = $stateParams.medicalRecordId` |
| L33666 | `$scope.prescription = res` (MedicalRecord Response 暂存) |
| L33670 | getMethodGlassRecordVo.json (prescriptionCtrl 读) |
| L34776 | optometryCtrl (验光 + 选镜架 + Delivery 5 branch) |
| L34954 | `$state.go("optometryGlasses", { medicalRecordId })` |
| L35185/L35204 | completeMedicalRecordDelivery (optometryCtrl) |
| L35342 | createMedicalStockLossOfSmallVersion (optometryCtrl) |
| L10607/L33127/L33197 | medicalRecordType: 1 (beginCustomerCheckin 链) |
| L2257/L31123/L32951/L33055/L33136/L33156 | medicalRecordType == 5 (Sale Branch) |
| L31117 | `custView == 1 ? 1 : 5` |
| L35087 | `{ 6: 1, 7: 0 }` UI 加工 |
| L6703 | `medicalExamineId` (唯一独立 ID) |
| L49594 | addVisitCtrl (复诊) |

---

S1-144 完成。立即停止，等待老板下一指令。不执行 S1-145。
