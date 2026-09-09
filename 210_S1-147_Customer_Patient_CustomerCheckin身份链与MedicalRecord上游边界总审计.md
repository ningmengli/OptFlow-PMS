# S1-147：Customer / Patient / CustomerCheckin 身份链与 MedicalRecord 上游边界总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 209 个 MD / 不修改历史
> 关联：S1-132 / S1-134 / S1-135 / S1-137R / S1-138 / S1-139 / S1-140 / S1-141 / S1-146

---

## 目录

- §0 审计范围
- §1 Customer 全量命中
- §2 Patient 全量命中
- §3 CustomerCheckin 全量命中
- §4 Customer 生命周期
- §5 Patient 生命周期
- §6 CustomerCheckin 生命周期
- §7 CustomerCheckin → MedicalRecord 完整 Source Trace
- §8 CustomerCheckin ↔ Patient
- §9 CustomerCheckin ↔ Customer
- §10 School / SchoolMate / SchoolMateCheck
- §11 Appointment 入口
- §12 三大对象字段矩阵
- §13 四方关系矩阵
- §14 生命周期 DAG
- §15 页面消费矩阵
- §16 26 项证据矩阵
- §17 历史差异
- §18 V4.4 上游身份模型
- §19 F / 未确认
- §20 Git / 完整性

---

## §0 审计范围

本轮把 Customer / Patient / CustomerCheckin 三个上游核心对象作为
**身份链 / 生命周期 / State / MedicalRecord 上游边界** 进行独立完整审计：

- 字符级字段（每个对象真实出现的所有字段）
- API 级（Read / Write / 全部调用点）
- State 级（$stateParams 入口）
- 跨对象字段桥（A 字段桥 / B API 桥 / C 参数桥 / F 未观察）
- 18 个 Controller 完整消费矩阵
- 26 项证据矩阵
- 历史 S1-132/134/135/137R/138/139/140/141/146 误判核对

---

## §1 Customer 全量命中

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `customer` (全词) | **84** | A |
| `customerId` | **207** | A |
| `customerVo` | **0** | A |
| `customerName` | **29** | A |
| `linkMobile` | **46** | A |
| `customerMobile` | **18** | A |

**重要发现**：`customerVo` 字符级 0 命中。Customer 实际没有"customerVoList"容器，
而是通过 `item.customer.*` 或 `res.vo.customer.*` 形式被消费。

### §1.2 Customer API 全量

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **getCustomerVo.json** | L3650/L4395/L4947/L5243/L5924/L7435/L8245/L8880/L19000/L20986/L31118/L31134 等 14+ | R | A |
| **getCustomerWallet.json** | L4950/L5240 | R | A |
| **saveCustomerInfo.json** | L8979/L21000 | **W** | A |
| **updateCustomerTags.json** | L8975/L17872/L20986 | W | A |
| **insertCustomerTags.json** | L17872 | W | A |
| **saveCustomerInfo.json** (其他 context) | L21000 | W | A |
| deleteCustomerCheckin.json | L8846 | W (实际删 Checkin) | A |

### §1.3 Customer 真实字段（按 access 路径分类）

| 字段 | Access 路径 | 行号 | 等级 |
|---|---|---|---|
| `id` | `item.customer.id` | L17511 | A |
| `linkMobile` | `item.customer.linkMobile` / `res.vo.customer.linkMobile` / `result.linkMobile` | L8245/L3652/L7435 | A |
| `customerName` | `item.customer.customerName` / `result.customerName` | L8248/L8268/L8981 | A |
| `channel` | `item.customer.channel` | L8249 | A |
| `channelTagId` | (State param) | L8424 | A |
| `tagIdArray` | (Request) | L8976 | A |

---

## §2 Patient 全量命中

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `patient` (全词) | **58** | A |
| `patientId` | **131** | A |
| `patientVo` | **0** | A |
| `patientName` | **38** | A |
| `patientBirthday` | **55** | A |
| `patientGender` | **33** | A |

**重要发现**：`patientVo` 字符级 0 命中（同 customerVo）。
Patient 实际通过 `item.patient.*` 或 `res.patient.*` 形式被消费。

### §2.2 Patient API 全量

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **getPatientInfo.json** | L1970/L3641/L6693/L21097/L31226/L31338 等 10+ | R | A |
| **getPatientVoList.json** | L8364/L8374/L8390/L18981 | R | A |
| **getPatientVo.json** | L8880 | R | A |
| **getPatientExamineListVoList.json** | L1977 | R | A |
| **savePatientInfo.json** | L8965/L21117 | **W** | A |

### §2.3 Patient 真实字段

| 字段 | Access 路径 | 行号 | 等级 |
|---|---|---|---|
| `id` | `item.patient.id` / `res.patient.id` | L8250/L11668/L31116 | A |
| `patientName` | `item.patient.patientName` / `res.patientName` | L8254/L8968 | A |
| `patientBirthday` | `item.patient.patientBirthday` / `res.patientBirthday` | L8247/L8970 | A |
| `patientGender` | `item.patient.patientGender` / `res.patientGender` | L8243/L8973 | A |
| `avatar` | `item.patient.avatar` | L8244/L9325 | A |
| `idCard` | `patient.patient.idCard` | L8451 | A |
| `patientRemark` | `item.patient.patientRemark` / `res.patientRemark` | L19007 | A |
| `school` (嵌套) | `patient.school.id` / `patient.school.schoolName` | L8434/L8435 | A |
| `schoolClass` (嵌套) | `patient.schoolClass.id` / `className` | L8437/L8438 | A |

### §2.4 Patient 写入 API 完整调用

| API | 行号 | Controller | Request | Response | 等级 |
|---|---|---|---|---|---|
| savePatientInfo.json | L8965 | (inline, checkinListCtrl 修改) | `$scope.data` | `res.patientName/patientBirthday/patientGender` | A |
| savePatientInfo.json | L21117 | (admin 端 patientUpdate) | `$scope.obj` | 跳 adminPatient.medicalRecordList | A |

**重要：Patient 实际无独立 Create API**（0 命中 `insertPatient*.json` / `createPatient*.json`）。
Patient 写入只通过 `savePatientInfo.json`（Update 模式，依赖已存在 id）。

---

## §3 CustomerCheckin 全量命中

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `customerCheckin` (全词) | **48** | A |
| `customerCheckinId` | **24** | A |
| `customerCheckinVo` | **0** | A |
| `customerCheckinVoList` | **0** | A |

**重要发现**：
- `customerCheckinVo` 0 命中 → CustomerCheckin 没有独立 VO 命名
- `customerCheckinVoList` 0 命中 → 通过 `selectCustomerCheckinVoListOfCompany.json`（**`VoList` 实际是 list item 内的 customerCheckin 字段**）

### §3.2 CustomerCheckin API 全量

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **selectCustomerCheckinVoListOfCompany.json** | L8778 多次 | R | A |
| **insertCustomerCheckinOfNewPaitent.json** | L8667 | **W (Create Patient + Checkin)** | A |
| **insertCustomerCheckinOfNewCustomer.json** | L8679 (动态 URL) | **W (Create Customer + Checkin)** | A |
| **insertCustomerCheckin.json** | L8681/L34914 | **W (Checkin only)** | A |
| **beginCustomerCheckin.json** | L10605/L33127/L34947 | **W (Begin → MedicalRecord)** | A |
| **receiveSelfAndBeginCustomerCheckin.json** | L33195 | **W (Begin + MedicalRecordType=1)** | A |
| **confirmArrivalOfAppoint.json** | L8658 | **W (预约到店)** | A |
| **medicalCheckBeforeCustomerCheckin.json** | L8791 | **W (预检前)** | A |
| **deleteCustomerCheckin.json** | L8846 | **W (Delete)** | A |
| **addSchoolMateConsume.json** | L8705 (注释) | W | C |
| **callingEmployeeCheckinQueue.json** | L10651 | W | A |
| **callingWaitingCheckinQueue.json** | (推断) | W | F |

### §3.3 CustomerCheckin 真实字段

| 字段 | Access 路径 | 行号 | 等级 |
|---|---|---|---|
| `id` | `item.customerCheckin.id` / `res.result.vo.customerCheckin.id` | L8791/L8667 | A |
| `medicalRecordId` | `res.customerCheckin.medicalRecordId` / `item.customerCheckin.medicalRecordId` | L8791/L10642/L33134 | A（6 处） |
| `customerCheckinId` (top-level) | `$scope.customerCheckin.customerCheckinId` | L9118/L9122/L9139/L9160 | A |
| `checkinNumber` | `p.customerCheckin.checkinNumber` | L11157 | A |

**重要**：6 处字符级 `customerCheckin.medicalRecordId` 是 CustomerCheckin → MedicalRecord 的核心 A 桥
（详见 §7）。

---

## §4 Customer 生命周期

### §4.1 Customer 真实入口

**Customer 没有独立 Create 入口**。0 命中 `insertCustomer*.json` / `createCustomer*.json`。
Customer 实际通过 3 条隐式路径进入系统：

| 路径 | API | 行号 | 等级 |
|---|---|---|---|
| A. 同步 Patient + Checkin | insertCustomerCheckinOfNewCustomer.json | L8679 | A |
| B. 异步 admin 保存 | saveCustomerInfo.json | L8979/L21000 | A |
| C. 通过 linkMobile 反查 | getCustomerVo.json ({customerId: ...}) | 14+ 调用 | A |

### §4.2 Customer State 入口

- `$stateParams.customerId` → getPatientVoList({customerId}) (L18949 patientListCtrl)
- `$scope.refundFeeInfo.customer.id` → getCustomerVo (L4395)
- `res.result.object.customer.id` → getCustomerVo (L4947)
- `item.customer.id` (L8248 / L17511)

### §4.3 Customer → Wallet

- `getCustomerWallet.json` (L4950/L5240) — 钱包独立 VO（不在本轮范围）

### §4.4 Customer Create 流程（addCheckinCtrl L8667 上下文）

```
addCheckinCtrl.checkCustomer
  → insertCustomerCheckinOfNewPaitent.json (L8667)   // 有 patient 但无 customer
  → insertCustomerCheckinOfNewCustomer.json (L8679)  // 无 patient 无 customer（自动建）
  → insertCustomerCheckin.json (L8681)               // 已有 customer + patient
  → 全部返回 res.result.vo.customerCheckin
```

---

## §5 Patient 生命周期

### §5.1 Patient 真实入口

**Patient 没有独立 Create API**。0 命中 `insertPatient*.json` / `createPatient*.json`。

Patient 实际通过 3 条路径进入：

| 路径 | API | 行号 | 等级 |
|---|---|---|---|
| A. 同步 Customer + Checkin | insertCustomerCheckinOfNewPaitent.json | L8667 | A |
| B. 异步 admin 保存 | savePatientInfo.json | L8965/L21117 | A |
| C. 通过 mobile 搜索 | getPatientVoList.json | L8364/L8374/L8390/L18981 | A |

### §5.2 Patient State 入口

- `$stateParams.patientId` → getPatientInfo (L3641/L6693)
- `$scope.patientId` → getPatientInfo (L1970)
- `res.object.medicalRecord.patientId` → getPatientInfo (L6693) — **MR → Patient A 派生桥**
- `v.patient.id` → 列表项 (L2728/L31894)
- `item.patient.id` → 列表项 (L8250/L11668)
- `response.customerCheckin.medicalRecordId` + `employee.patient.id` (L10610)
- `customerCheckin.patientId` (L8707 **注释代码，运行时 0 消费**)

### §5.3 Patient → School / SchoolClass

- `patient.school.id` / `patient.school.schoolName` (L8434/L8435)
- `patient.schoolClass.id` / `className` (L8437/L8438)
- 通过 getPatientVo.json Response `res.school` / `res.schoolClass` 派生 (L8880)

### §5.4 Patient → Customer 字段桥

#### A. List item 嵌套（A 字段桥）
- `getPatientVoList.json` Response = `res.list`，每个 item 同时含 `customer` + `patient`
- `item.customer.customerName` (L8248) + `item.patient.patientName` (L8254)
- `$scope.patientList[i].customer.customerName = result.customerName` (L19000)
- `$scope.patientList[i].patient.patientName = result.patientName` (L19002)
- **A 字段桥**（list item 嵌套），但**只在 list 响应上下文有效**

#### B. C 参数桥（S1-140 修正保持）
- `patientListCtrl` L18948: `$scope.customerId = $stateParams.customerId`
- L18981: `getPatientVoList({customerId: $scope.customerId, ...})`
- **C 参数桥**（Request 携带 customerId）

#### C. 反向直接 A 桥
- `patient.customerId` 字符级 **0 命中**
- `customerVo.patient` 字符级 **0 命中**
- **A 字段桥不存在**（S1-139 报告需修正）

---

## §6 CustomerCheckin 生命周期

### §6.1 4 个 CustomerCheckin 写入 API 详细

#### A. beginCustomerCheckin.json（3 调用）

| 行号 | Controller | Request | Response | 后续 State |
|---|---|---|---|---|
| L10605 | doctorWorkbenchCtrl case 0 | `{ customerCheckinId, medicalRecordType: 1 }` | `response.customerCheckin.medicalRecordId` | $state.go adminMyRecord.myMemberRecord |
| L33127 | myMemberCtrl selectMedicalType | `{ customerCheckinId, medicalRecordType: 1 }` | `response.result.vo.customerCheckin.medicalRecordId` | getMedicalRecord (type 路由) |
| L34947 | optometryCtrl beginCustomerCheckin | `{ customerCheckinId, medicalRecordType: choseUser.glassestype }` | `result.result.vo.customerCheckin.medicalRecordId` | $state.go optometryGlasses |

**关键**：`medicalRecordType: 1` 是接诊标识（L10605/L33127），`medicalRecordType: choseUser.glassestype` 是验光分支（L34947）。
这 3 处都是 CustomerCheckin → MedicalRecord 桥的源。

#### B. receiveSelfAndBeginCustomerCheckin.json（1 调用）

| 行号 | Controller | Request | Response | 后续 State |
|---|---|---|---|---|
| L33195 | myMemberCtrl receiveSelfAndBeginCustomerCheckin | `{ customerCheckinId, medicalRecordType: 1 }` | `res.customerCheckin.medicalRecordId` + `res.patient.id` | $state.go adminMyRecord.myMemberRecord |

#### C. insertCustomerCheckin*.json（3 变种）

| API | 行号 | Controller | 用途 | 等级 |
|---|---|---|---|---|
| insertCustomerCheckinOfNewPaitent.json | L8667 | addCheckinCtrl | 已有 Patient 无 Customer | A |
| insertCustomerCheckinOfNewCustomer.json | L8679 | addCheckinCtrl | 已有 Customer 无 Patient | A（动态 URL） |
| insertCustomerCheckin.json | L8681 | addCheckinCtrl | 已有 Customer + Patient | A（动态 URL） |
| insertCustomerCheckin.json | L34914 | optometryCtrl choseUser | 创建 Checkin | A |

#### D. confirmArrivalOfAppoint.json（1 调用）

| 行号 | Controller | Request | 后续 |
|---|---|---|---|
| L8658 | addCheckinCtrl changeStatusFactory | `{ appointId: aId }` | (无显式 success state) |

### §6.2 CustomerCheckin → Checkin Number

- `p.customerCheckin.checkinNumber` (L11157) — 排队号显示
- 来源是列表项 `item.customerCheckin.checkinNumber`

### §6.3 CustomerCheckin 删除

- `deleteCustomerCheckin.json` (L8846 checkinListCtrl.deleteCheck) — `{ customerCheckinId: id }`
- 删除成功调用 `$scope.search()` 刷新列表

---

## §7 CustomerCheckin → MedicalRecord 完整 Source Trace

### §7.1 6 处字符级 A 桥（保持 S1-135 修正）

| # | 行号 | API | Access 路径 | 后续 State | 等级 |
|---|---|---|---|---|---|
| 1 | L8791 | medicalCheckBeforeCustomerCheckin.json | `_this.medicalRecordId = res.customerCheckin.medicalRecordId` | (本地 modal) | A |
| 2 | L10610 | beginCustomerCheckin.json | `$state.go adminMyRecord.myMemberRecord({ medicalRecordId: response.customerCheckin.medicalRecordId, patientId: employee.patient.id })` | adminMyRecord.myMemberRecord | A |
| 3 | L10642 | (列表项直接读) | `$state.go adminMyRecord.myMemberRecord({ medicalRecordId: employee.customerCheckin.medicalRecordId, patientId: employee.patient.id })` | adminMyRecord.myMemberRecord | A |
| 4 | L33134 | beginCustomerCheckin.json (链式) | `var typePromise = getMedicalRecord({ id: response.result.vo.customerCheckin.medicalRecordId })` → `if (res.object.medicalRecordType == 5) $state.go adminSalesRecord.myMaterialBill` | adminSalesRecord.myMaterialBill (type=5) / adminMyRecord.myMemberRecord (其他) | A |
| 5 | L33203 | receiveSelfAndBeginCustomerCheckin.json | `$state.go adminMyRecord.myMemberRecord({ medicalRecordId: res.customerCheckin.medicalRecordId, patientId: res.patient.id })` | adminMyRecord.myMemberRecord | A |
| 6 | L34955 | beginCustomerCheckin.json | `$state.go optometryGlasses({ medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })` | optometryGlasses | A |

### §7.2 Source Trace 链

```
CustomerCheckin (List item)
  item.customerCheckin.medicalRecordId (top-level field)
    ↓
  beginCustomerCheckin / receiveSelfAndBegin / medicalCheckBefore API
    ↓
  Response.res.customerCheckin.medicalRecordId
  或 Response.result.vo.customerCheckin.medicalRecordId
    ↓
  $state.go State X ({
    medicalRecordId: response.customerCheckin.medicalRecordId,
    patientId: ...
  })
    ↓
  State X 控制器 (adminMyRecord.myMemberRecord / optometryGlasses / adminSalesRecord.myMaterialBill)
    ↓
  15 个 MR 共享 Controller 之一
```

### §7.3 CustomerCheckin → MedicalRecord 6 个跳转目标汇总

| State | medicalRecordType | Controller | 等级 |
|---|---|---|---|
| adminMyRecord.myMemberRecord | 1 (默认) | myMemberRecordCtrl (L33218) | A |
| adminSalesRecord.myMaterialBill | 5 (Sale 路由) | myMaterialBillCtrl (L32435) | A |
| optometryGlasses | choseUser.glassestype | optometryGlasses | A |

---

## §8 CustomerCheckin ↔ Patient

### §8.1 CustomerCheckin → Patient

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| `customerCheckin.patientId` 字段 | **0 命中**（L8707 在 `/* */` 注释代码内） | F |
| `customerCheckin.patient` 字段 | **0 命中** | F |
| `res.patient.id` (派生) | L33203 (receiveSelfAndBeginCustomerCheckin Response) | A |
| `employee.patient.id` (派生) | L10610/L10642 (selectEmployeeCheckinVoList 列表项) | A |

**S1-140 修正保持**：`customerCheckin.patientId` 在 L8707 是 `/* */` 注释代码，
运行时未消费。运行时实际是经 `res.patient.id` 或 `employee.patient.id` 派生。

### §8.2 Patient → CustomerCheckin

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| `patient.customerCheckin` | 0 命中 | F |
| `patient.customerCheckinId` | 0 命中 | F |
| `getPatientVoList` Response list item 含 `customerCheckin` | 0 命中 (L8243-L8277 详查 list item 字段) | F |
| `selectCustomerCheckinVoListOfCompany` 列表项 `item.customerCheckin.id` | L8791 | A |

**重要**：Patient 与 CustomerCheckin 的桥是**反向经列表项**，不是 Patient 内嵌 customerCheckin。

### §8.3 CustomerCheckin ↔ Patient 总结

| 方向 | 直接字段 | 派生 | 等级 |
|---|---|---|---|
| CustomerCheckin → Patient | F | res.patient.id / employee.patient.id (A) | A (经 API 响应派生) |
| Patient → CustomerCheckin | F | F | F |

---

## §9 CustomerCheckin ↔ Customer

### §9.1 CustomerCheckin → Customer

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| `customerCheckin.customerId` | **0 命中** | F |
| `customerCheckin.customer` 字段 | 0 命中 | F |
| `res.customer` (派生) | L8905 `$scope.customer.linkMobile = response.customer.linkMobile` (但 `response` 是 `getCustomerVo` Response 不是 Checkin) | C |

### §9.2 Customer → CustomerCheckin

| 命题 | 字符级证据 | 等级 |
|---|---|---|
| `customer.customerCheckin` | 0 命中 | F |
| `customer.customerCheckinId` | 0 命中 | F |
| `getCustomerVo` Response 含 customerCheckin | 0 命中 (实际是 `res.vo.customer.*`) | F |

### §9.3 CustomerCheckin ↔ Customer 总结

| 方向 | 等级 |
|---|---|
| CustomerCheckin → Customer | F |
| Customer → CustomerCheckin | F |

**桥不存在**：Customer 与 CustomerCheckin 没有直接字段桥，必须经 Patient 中转（patientListCtrl 模式）
或经列表项拼接。

---

## §10 School / SchoolMate / SchoolMateCheck

### §10.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `school` (全词) | 45 | A |
| `schoolId` | **297** | A |
| `schoolName` | 112 | A |
| `schoolMate` | 12 | A |
| `schoolMateId` | 25 | A |
| `schoolMateVo` | 11 | A |
| `schoolMateCheck` | 129 | A |
| `schoolMateCheckId` | 20 | A |
| `schoolClass` | 27 | A |
| `classId` | **149** | A |

### §10.2 SchoolMate → Patient 字段桥（A）

`getAppointPatientVo` Response item 同时含 schoolMateVo（type=1 路径）：

| 字段 | 行号 | 等级 |
|---|---|---|
| `item.schoolMateVo.schoolMate.gender` | L8264 | A |
| `item.schoolMateVo.schoolMate.customerMobile` | L8265 | A |
| `item.schoolMateVo.schoolMate.birthday` | L8267 | A |
| `item.schoolMateVo.schoolMate.classMateName` | L8277 | A |
| `item.schoolMateVo.school.id` → `schoolId` | L8270 | A |
| `item.schoolMateVo.schoolClass.id` → `classId` | L8271 | A |
| `item.schoolMateVo.school.schoolName` | L8266/L8273 | A |
| `item.schoolMateVo.schoolClass.className` | L8266/L8274 | A |

### §10.3 customerMobile → linkMobile 映射（A 字段桥）

- `linkMobile: item.schoolMateVo.schoolMate.customerMobile` (L8265)
- `$scope.obj.customerMobile = res.vo.schoolMateCheck.customerMobile` (L41684/L41764/L41981)
- `params.linkMobile = params.customerMobile` (L44119)
- **A 字段桥**：customerMobile 是 schoolMate 内部字段，linkMobile 是 patient/customer 字段
- 通过 schoolMateVo 解构实现映射

### §10.4 School / SchoolMate / SchoolMateCheck ↔ 三大对象

| Source | Target | Mechanism | 等级 |
|---|---|---|---|
| SchoolMateVo | Patient | list item 字段桥 (L8264-L8277) | A |
| SchoolMateCheck | Patient | $scope.obj.customerMobile 派生 (L41684) | A |
| SchoolMateCheck | CustomerCheckin | 0 命中直接字段 | F |
| SchoolMateCheck | MedicalRecord | 0 命中 | F |
| School | Patient | `patient.school.id` (L8435) / `item.schoolMateVo.school.id` (L8270) | A |
| School | Customer | 0 命中 | F |
| SchoolClass | Patient | `patient.schoolClass.id` (L8437) | A |
| School | SchoolClass | `item.schoolMateVo.schoolClass.id` (L8271) | A |

---

## §11 Appointment 入口

### §11.1 appointOrderCtrl L3664 详细 — **Stub 确认**

```javascript
angular.module("bestvisionWeb").controller("appointOrderCtrl", ["$scope", "ListFactory", "$rootScope", "$state", "ObjectFactory", "$timeout", function ($scope, ListFactory, $rootScope, $state, ObjectFactory, $timeout) {
  // window.open(API_HOST + "/clinic/index.html#/clinic/appointment");
}]);
```

**关键发现**：`appointOrderCtrl` 是空 Stub 控制器，整个函数体只有 1 行注释。
所有预约实际走 `addCheckinCtrl`（L8159）。

### §11.2 真实预约 Controller

- **addCheckinCtrl** (L8159) — 唯一真实预约接诊入口
- **bookDetailCtrl** (L3669) — 预约详情独立 Controller（与接诊分离）

### §11.3 Appointment API

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **getAppointmentVo.json** | L3672 | R | A |
| **updateAppointCompanyRemark.json** | L3681 | W | A |
| **confirmAppointment.json** | L3702 | W | A |
| **getAppointPrintData.json** | L9049 | R | A |
| **getAppointPatientVo.json** | L14748/L8225 | R | A |
| **getAppointSchoolMateVo.json** | L43885/L43934/L43972/L44000/L44060/L8229 | R | A |
| **confirmArrivalOfAppoint.json** | L8658 | W | A |

### §11.4 Appointment → CustomerCheckin 桥

- `confirmArrivalOfAppoint.json` (L8658) — Request `{ appointId: aId }`，**无显式 patientId/customerId**
- Appointment → CustomerCheckin 桥是**C 参数桥**（只传 appointId）
- 真实 Checkin 创建由后续 addCheckinCtrl 处理

### §11.5 Appointment → MedicalRecord 桥

- **F**（Appointment 没有直接 medicalRecordId 桥）
- 链式：A appointId → confirmArrivalOfAppoint → addCheckinCtrl → insertCustomerCheckin → beginCustomerCheckin → customerCheckin.medicalRecordId

---

## §12 三大对象字段矩阵

### §12.1 Customer 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `id` | A | A | - | A | - | A |
| `linkMobile` | A | A | A ($stateParams.tel) | A | - | A |
| `customerName` | A | A | A | A | - | A |
| `channel` | A | A | - | A | - | A |
| `channelTagId` | - | - | A | A | - | A |
| `tagIdArray` | - | A | - | - | - | A |
| `appointVo.schoolMateCheckId` | - | - | A | - | - | C (注释) |
| `customer.customerCheckin` | - | - | - | - | - | F |

### §12.2 Patient 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `id` | A | A | A | A | - | A |
| `patientName` | A | A | A | A | - | A |
| `patientBirthday` | A | A | A | A | - | A |
| `patientGender` | A | A | - | A | - | A |
| `avatar` | A | - | A | A | - | A |
| `idCard` | A | - | - | A | - | A |
| `patientRemark` | A | A | A | A | - | A |
| `school` (嵌套) | A | - | - | A | - | A |
| `schoolClass` (嵌套) | A | - | - | A | - | A |
| `patient.customerId` | - | - | - | - | - | **F** |
| `patient.customerCheckin` | - | - | - | - | - | **F** |

### §12.3 CustomerCheckin 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `id` | A | A | A | A | - | A |
| `medicalRecordId` | A | - | - | A | - | A (6 处字符级) |
| `customerCheckinId` | A | A | A | A | - | A |
| `checkinNumber` | A | - | - | A | - | A |
| `customerCheckin.patientId` | - | - | - | - | - | **F** (L8707 注释) |
| `customerCheckin.customerId` | - | - | - | - | - | **F** |
| `customerCheckin.customer` | - | - | - | - | - | **F** |
| `customerCheckin.medicalRecord` | - | - | - | - | - | **F** |
| `customerCheckin.schoolMate` | - | - | - | - | - | **F** |

---

## §13 四方关系矩阵

### §13.1 12 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Customer | Patient | `$stateParams.customerId → getPatientVoList({customerId})` | C 参数桥 | L18949/L18981 | **C** | C |
| Customer | Patient | list item 嵌套 (`item.customer + item.patient`) | A 字段桥 | L8245/L8250 | **A** (list item) | A (list) |
| Customer | Patient | `customerVo.patient` | 0 命中 | - | **F** | F |
| Patient | Customer | list item 嵌套 (`item.patient + item.customer`) | A 字段桥 | L8250/L8245 | **A** (list item) | A (list) |
| Patient | Customer | `patient.customerId` 字段 | 0 命中 | - | **F** | F |
| Patient | CustomerCheckin | list item `item.customerCheckin` | A 字段桥 | L8791 | **A** | A |
| Patient | CustomerCheckin | `patient.customerCheckin` 字段 | 0 命中 | - | **F** | F |
| CustomerCheckin | Patient | `customerCheckin.patientId` 字段 | 0 命中（L8707 注释） | L8707 | **F** | F |
| CustomerCheckin | Patient | `res.patient.id` (receiveSelfAndBegin Response) | A 派生 | L33203 | **A** | A (派生) |
| CustomerCheckin | Patient | `employee.patient.id` (列表项) | A 派生 | L10610/L10642 | **A** | A (列表项) |
| Customer | CustomerCheckin | `customer.customerCheckin` 字段 | 0 命中 | - | **F** | F |
| CustomerCheckin | Customer | `customerCheckin.customerId` 字段 | 0 命中 | - | **F** | F |
| Patient | MedicalRecord | `res.object.medicalRecord.patientId` | A 派生 | L6693 | **A** | A (派生) |
| MedicalRecord | Patient | `addMedicalRecord Request { patientId: item.patient.id }` | A Request 桥 | L31116 | **A** | A |
| CustomerCheckin | MedicalRecord | `customerCheckin.medicalRecordId` 字段 | A 字段桥 | L8791/L10610/L10642/L33134/L33203/L34955 | **A** | A (6 处字符级) |
| MedicalRecord | CustomerCheckin | `medicalRecord.customerCheckinId` | 0 命中 | - | **F** | F |
| MedicalRecord | Customer | `medicalRecord.customerId` | 0 命中 | - | **F** | F |

### §13.2 12 关系等级汇总

| 等级 | 数量 | 关系 |
|---|---:|---|
| A | 7 | Customer→Patient (list item), Patient→Customer (list item), Patient→CustomerCheckin (list item), CustomerCheckin→Patient (res.patient.id), CustomerCheckin→Patient (employee.patient.id), Patient→MedicalRecord (派生), MedicalRecord→Patient (Request), CustomerCheckin→MedicalRecord (6 字符级) |
| C | 1 | Customer→Patient (patientListCtrl $stateParams) |
| F | 4 | customerCheckin.patientId, patient.customerId, medicalRecord.customerCheckinId, medicalRecord.customerId |

---

## §14 生命周期 DAG

### §14.1 Customer 生命周期

```
[外部] ──linkMobile──→ getCustomerVo({customerId}) ──→ res.vo.customer.* (Read)
                          ↓
                       saveCustomerInfo.json (Update) [L8979/L21000]
                          ↓
                       res.customerName/result.linkMobile
                          ↓
                       修改 list item: items[i].customer.* (L8981)
```

**Customer 没有独立 Create API**。Customer 进入系统通过 `insertCustomerCheckinOfNewCustomer.json` (L8679)。

### §14.2 Patient 生命周期

```
[外部] ──patientId──→ getPatientInfo (Read) [L1970/L3641/L6693]
                          ↓
                       res.patient.* (top-level patient object)
                          ↓
                       savePatientInfo.json (Update) [L8965/L21117]
                          ↓
                       res.patientName/patientBirthday/patientGender
                          ↓
                       修改 list item: items[i].patient.* (L8968-L8973)
                          ↓
                       adminPatient.medicalRecordList ({patientId}) (L21117)
```

**Patient 没有独立 Create API**。Patient 进入系统通过 `insertCustomerCheckinOfNewPaitent.json` (L8667)。

### §14.3 CustomerCheckin 生命周期

```
[外部] ──customerCheckinId──→ selectCustomerCheckinVoListOfCompany (Read) [L8778]
                                ↓
                             list item: item.customerCheckin.* (id, medicalRecordId, checkinNumber)
                                ↓
                             beginCustomerCheckin / receiveSelfAndBegin (Begin → MR) [L10605/L33127/L33195/L34947]
                                ↓
                             response.customerCheckin.medicalRecordId
                                ↓
                             $state.go adminMyRecord.myMemberRecord / optometryGlasses / adminSalesRecord.myMaterialBill
                                ↓
                             15 个 MR 共享 Controller
```

### §14.4 Combined Upstream DAG（A/B/C 边）

```
                       [addCheckinCtrl]
                              │
              insertCustomerCheckinOfNewPaitent.json (L8667)
              insertCustomerCheckinOfNewCustomer.json (L8679)
              insertCustomerCheckin.json (L8681)
                              │
              ┌───────────────┴───────────────┐
              ↓                               ↓
       Customer (F 直接)                CustomerCheckin (A)
              │                               │
              │ patientListCtrl               │ 6 处 .medicalRecordId
              │ $stateParams.customerId       │ (L8791/L10610/L10642/
              │ → getPatientVoList (C)        │  L33134/L33203/L34955)
              ↓                               ↓
       Patient (A list item)            MedicalRecord (A)
              │                               │
              │ item.patient.id               │ 15 个 Controller 共享
              │ → addMedicalRecord (A Req)    │
              ↓                               ↓
       MedicalRecord (A)                (详见 S1-146)
```

### §14.5 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| addCheckinCtrl | Customer | A (派生) | insertCustomerCheckinOfNewCustomer.json | L8679 |
| addCheckinCtrl | Patient | A (派生) | insertCustomerCheckinOfNewPaitent.json | L8667 |
| addCheckinCtrl | CustomerCheckin | A (派生) | insertCustomerCheckin.json | L8681 |
| CustomerCheckin | MedicalRecord | A (6 字符级) | .medicalRecordId | L8791/L10610/L10642/L33134/L33203/L34955 |
| Customer | Patient | A (list item) | item.customer + item.patient | L8245/L8250 |
| Customer | Patient | C (参数) | $stateParams.customerId | L18949 |
| Patient | MedicalRecord | A (Request) | addMedicalRecord { patientId } | L31116 |

---

## §15 页面消费矩阵

### §15.1 18 个 Controller 消费矩阵

| Controller | Customer | Patient | CustomerCheckin | MedicalRecord | 作用 | Entry | Grade |
|---|---|---|---|---|---|---|---|
| checkinListCtrl (L8778) | 23 | 13 | **33** | 0 | 接诊列表 | URL | A |
| addCheckinCtrl (L8159) | **27** | **29** | **36** | 0 | 新增接诊 | URL | A |
| doctorWorkbenchCtrl (L10401) | 0 | 5 | 5 | 0 | 医生工作台 | URL | A |
| myMemberCtrl (L33080) | 19 | 19 | 12 | **54** | 我的客户 | URL | A |
| myMemberRecordCtrl (L33218) | 19 | 18 | 10 | **54** | 病历详情 | URL | A |
| optometryCtrl (L34776) | 20 | 18 | 2 | 16 | 验光 | URL | A |
| myMedicalRecordListCtrl (L32965) | 20 | 19 | 12 | **54** | 病历列表 | URL | A |
| assistCheckingCtrl (L1756) | 4 | 1 | 0 | 1 | 辅助检查 | $stateParams | A |
| prescriptionCtrl (L33560) | 20 | 18 | 2 | 24 | 验光处方 | $stateParams | A |
| drugPrescriptionCtrl (L31605) | 1 | 2 | 10 | 46 | 药品处方 | $stateParams | A |
| addSaleRecordCtrl (L31008) | 1 | 4 | 10 | 46 | 新增售卖 | $stateParams | A |
| myMaterialBillCtrl (L32435) | 3 | 2 | 12 | **54** | 物料单 | $stateParams | A |
| adminMyRecordCtrl (L31158) | 1 | 2 | 10 | 46 | admin 病历 | $stateParams | A |
| adminSalesRecordCtrl (L31285) | 1 | 2 | 10 | 46 | admin 售卖 | $stateParams | A |
| addVisitCtrl (L49594) | 2 | 1 | 0 | 0 | 复诊 | URL | A |
| waitChargeDetailCtrl (L6568) | **33** | **25** | **31** | 1 | 待收费详情 | $stateParams | A |
| deliveryInputCtrl (L3812) | 10 | 0 | 0 | 2 | 配送录入 | (派生) | A |
| deliveryInputRecordCtrl (L4024) | 10 | 0 | 0 | 2 | 配送记录 | (派生) | A |

### §15.2 三大对象核心消费 Controller

| 对象 | 核心 Controller | 等级 |
|---|---|---|
| Customer | waitChargeDetailCtrl (33) / addCheckinCtrl (27) / optometryCtrl (20) / prescriptionCtrl (20) | A |
| Patient | addCheckinCtrl (29) / waitChargeDetailCtrl (25) / myMedicalRecordListCtrl (19) / myMemberRecordCtrl (18) | A |
| CustomerCheckin | addCheckinCtrl (36) / checkinListCtrl (33) / waitChargeDetailCtrl (31) / myMaterialBillCtrl (12) | A |

**关键观察**：
- **addCheckinCtrl** 是唯一同时大量消费 Customer(27) + Patient(29) + CustomerCheckin(36) 的 Controller — 是核心接诊入口
- **waitChargeDetailCtrl** 大量消费 Customer(33) + Patient(25) + CustomerCheckin(31)，是收费详情核心页
- **addVisitCtrl** 不消费 CustomerCheckin（0 命中）和 MedicalRecord（0 命中），仅 Customer(2) + Patient(1)

---

## §16 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 18 Controllers 范围 | A | - | 全部 | A |
| 2 | Controller | 18 Controllers | A | - | 全部 | A |
| 3 | State | addCheckin / myMember / myMemberRecord / optometryGlasses / patientList | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | customerCheckinId / patientId / customerId / medicalRecordId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | linkMobile / mobile (患者搜索) | A | - | L8364/L8374/L8390/L18981 | A |
| 10 | Status | **CustomerCheckin 不含 status 顶层字段** | A | - | 0 命中（item.status 在容器） | C |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=9/10/12/30 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | patientName / linkMobile (接诊) | A | - | L8623 | A |
| 15 | Default | medicalRecordType=1 (接诊默认) | A | - | L10605 | A |
| 16 | Data Source | 11+ Read API | A | - | 全部 | A |
| 17 | Object | customer / patient / customerCheckin 各自 top-level | A | - | 全部 | A |
| 18 | Request | { customerId } / { patientId } / { customerCheckinId } | A | - | 全部 | A |
| 19 | Response | res.vo.customer / res.patient / res.customerCheckin | A | - | 全部 | A |
| 20 | Function | choseUser.affirm / getCustomerCheckin / deleteCheck | A | - | 多处 | A |
| 21 | State Bridge | medicalRecordId (主入口经 CustomerCheckin) | A | - | 6 字符级 | A |
| 22 | Object Bridge | customerCheckin.medicalRecordId (A) / item.customer+item.patient (A list) | A | - | 多处 | A |
| 23 | API Bridge | beginCustomerCheckin / receiveSelfAndBegin / insertCustomerCheckin* | A | - | 全部 | A |
| 24 | Business Interpretation | 三大对象是 MedicalRecord 上游身份链 | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 1 C / 0 D / 0 E / 4 F | - | - | - | - |
| 26 | V4.4 Decision | 三大对象必保留, 字段桥精确分级 | A | - | - | A |

---

## §17 历史差异

### §17.1 S1-132/134/135/137R/138/139/140/141/146 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-135: CustomerCheckin → MedicalRecord 6 处 A | 实际 6 处仍是 A (L8791/L10610/L10642/L33134/L33203/L34955) | 保持 | **保持 S1-135 修正** |
| S1-137R: 4 API 双向桥 | 仅 getMedicalRecordPayVo 1 API 单向 | 已在 S1-137R 修正 | **保持** |
| S1-138: 5-6 Create 路径 | 仍是 6 路径 | 保持 | **保持 S1-138 修正** |
| S1-139: patient.customerId A 字段桥 | 实际 `patient.customerId` 字符级 0 命中 | **应改** | **F** (list item 嵌套才是 A) |
| S1-140: Customer → Patient C 参数桥 | 实际 patientListCtrl L18949 $stateParams.customerId → getPatientVoList | 保持 | **保持 S1-140 修正** |
| S1-140: customerCheckin.patientId 注释代码 | 实际 L8707 仍在 `/* */` 注释内, 运行时 0 消费 | 保持 | **保持 S1-140 修正 (F)** |
| S1-141: Cashflow 5 Write | 保持 | 保持 | **保持** |
| S1-146: MedicalRecord 不含 status | 仍 0 命中 medicalRecord.status | 保持 | **保持 S1-146 修正** |
| S1-146: MedicalRecord 不含 cashflow/delivery 嵌套 | 仍 0 命中 | 保持 | **保持 S1-146 修正** |
| S1-134: SchoolMate → Patient A | 实际 schoolMateVo 嵌套字段 A (L8264-L8277) | 保持 | **保持 S1-134 修正** |
| (历史未确认) appointOrderCtrl | 实际是空 Stub (1 行注释) | **本轮新增** | **F (Stub)** |

### §17.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~Customer 有独立 Create API~~ | 0 命中 insertCustomer*.json / createCustomer*.json | 应改 | **F (派生创建, 经 insertCustomerCheckinOfNewCustomer)** |
| ~~Patient 有独立 Create API~~ | 0 命中 insertPatient*.json / createPatient*.json | 应改 | **F (派生创建, 经 insertCustomerCheckinOfNewPaitent)** |
| ~~appointOrderCtrl 真实预约 Controller~~ | 实际是空 Stub (L3664 仅 1 行注释) | 应改 | **F (Stub, 真实入口是 addCheckinCtrl L8159)** |
| ~~customerVo 字段访问存在~~ | 字符级 0 命中 customerVo | 应改 | **F (用 res.vo.customer 或 item.customer)** |
| ~~patientVo 字段访问存在~~ | 字符级 0 命中 patientVo | 应改 | **F (用 res.patient 或 item.patient)** |
| ~~customerCheckinVo 字段访问存在~~ | 字符级 0 命中 | 应改 | **F (用 item.customerCheckin 或 res.vo.customerCheckin)** |
| ~~patient.customerId 字段桥 A~~ | 字符级 0 命中 | 应改 (S1-139 误判) | **F (list item 嵌套才是 A)** |
| ~~CustomerCheckin → Patient A 字段桥~~ | 实际 `customerCheckin.patientId` 字符级 0 (注释) | 应改 | **F (派生经 res.patient.id)** |
| ~~Patient → CustomerCheckin A 字段桥~~ | 0 命中 patient.customerCheckin | 应改 | **F (派生经列表项 item.customerCheckin)** |
| ~~Customer ↔ CustomerCheckin 直接字段桥~~ | 0 命中 customerCheckin.customerId | 应改 | **F (无直接桥, 必须经 Patient 中转)** |

### §17.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 209_S1-146 全部保持原样
- 本文档 210_*.md 单独记录 Customer/Patient/CustomerCheckin 上游身份链完整闭环

---

## §18 V4.4 上游身份模型

### §18.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| getCustomerVo.json | 14+ 调用 | ✓ |
| getCustomerWallet.json | 2+ 调用 | ✓ |
| saveCustomerInfo.json | 2 调用 | ✓ |
| updateCustomerTags.json | 2 调用 | ✓ |
| getPatientInfo.json | 10+ 调用 | ✓ |
| getPatientVoList.json | 4 调用 | ✓ |
| getPatientVo.json | 1 调用 | ✓ |
| getPatientExamineListVoList.json | 1 调用 | ✓ |
| savePatientInfo.json | 2 调用 | ✓ |
| selectCustomerCheckinVoListOfCompany.json | 多次 | ✓ |
| insertCustomerCheckinOfNewPaitent.json | 1 调用 | ✓ |
| insertCustomerCheckinOfNewCustomer.json | 1 调用 (动态 URL) | ✓ |
| insertCustomerCheckin.json | 2 调用 | ✓ |
| beginCustomerCheckin.json | 3 调用 | ✓ |
| receiveSelfAndBeginCustomerCheckin.json | 1 调用 | ✓ |
| confirmArrivalOfAppoint.json | 1 调用 | ✓ |
| medicalCheckBeforeCustomerCheckin.json | 1 调用 | ✓ |
| deleteCustomerCheckin.json | 1 调用 | ✓ |
| getAppointmentVo.json | 1 调用 | ✓ |
| updateAppointCompanyRemark.json | 1 调用 | ✓ |
| confirmAppointment.json | 1 调用 | ✓ |
| getAppointPrintData.json | 1 调用 | ✓ |
| getAppointPatientVo.json | 2 调用 | ✓ |
| getAppointSchoolMateVo.json | 5+ 调用 | ✓ |
| 18 个 Controller 全部 | 全部 | ✓ |
| 6 处 customerCheckin.medicalRecordId 桥 | 全部 | ✓ |
| list item 嵌套 (customer+patient) | 全部 list | ✓ |

### §18.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `customerVo` / `patientVo` / `customerCheckinVo` / `customerCheckinVoList` 独立 VO 命名 | ✗ (0 命中) |
| `patient.customerId` 字段 | ✗ (0 命中) |
| `patient.customerCheckin` 字段 | ✗ (0 命中) |
| `customerCheckin.patientId` 运行时字段 | ✗ (L8707 仅注释) |
| `customerCheckin.customerId` 字段 | ✗ (0 命中) |
| `customerCheckin.customer` 字段 | ✗ (0 命中) |
| `customer.customerCheckin` 字段 | ✗ (0 命中) |
| `medicalRecord.customerCheckinId` 字段 | ✗ (0 命中) |
| `medicalRecord.customerId` 字段 | ✗ (0 命中) |
| `insertCustomer*.json` / `insertPatient*.json` 独立 Create API | ✗ (0 命中) |
| `appointOrderCtrl` 真实逻辑 | ✗ (仅 1 行注释) |
| 6 个 ID 合并 | ✗ (appointId / customerCheckinId / medicalRecordId / cashflowId / patientId / printCheckinId 必须严格区分) |

### §18.3 三大对象 Object Type 分类

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Customer** | A (独立 ID + Response object) | 独立 Create API (派生经 insertCustomerCheckinOfNewCustomer) |
| **Patient** | A (独立 ID + Response object) | 独立 Create API (派生经 insertCustomerCheckinOfNewPaitent) |
| **CustomerCheckin** | A (独立 ID + Response object) | 含 patientId 字段 (L8707 注释未消费) |
| **MedicalRecord** | A (独立 ID + Response object) | 含 customerCheckinId 字段 (F) |
| **CustomerVo / PatientVo / CustomerCheckinVo** | F (0 命中) | - |

### §18.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `customerCheckin.medicalRecordId` (6 字符级) → MedicalRecord | A | L8791/L10610/L10642/L33134/L33203/L34955 |
| `res.patient.id` → Patient (经 receiveSelfAndBeginCustomerCheckin) | A | L33203 |
| `employee.patient.id` → Patient (经 selectEmployeeCheckinVoList 列表项) | A | L10610/L10642 |
| `res.object.medicalRecord.patientId` → Patient (经 computeUnPlaceOrderMedicalRecordFee) | A | L6693 (S1-146) |
| `addMedicalRecord { patientId: item.patient.id }` → MedicalRecord | A | L31116 (S1-146) |
| `item.customer + item.patient` 共享 customerId (list item) | A | L8245/L8250 |

### §18.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| customerCheckin.patientId (运行时) | F |
| customerCheckin.customerId | F |
| customerCheckin.customer | F |
| patient.customerId (字段) | F |
| patient.customerCheckin | F |
| customer.customerCheckin | F |
| customerCheckinVo / patientVo / customerVo 独立 VO | F |

### §18.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `customerCheckin.patientId` (L8707) | 注释代码, 运行时未消费 | **命名误导 (历史未启用)** |
| `appointOrderCtrl` (L3664) | 空 Stub (1 行注释) | **命名误导 (真实入口是 addCheckinCtrl)** |
| `patientVo` | 字符级 0 命中, 用 res.patient 或 item.patient | 命名误导 |
| `customerVo` | 字符级 0 命中, 用 res.vo.customer 或 item.customer | 命名误导 |
| `customerCheckinVo` | 字符级 0 命中, 用 res.vo.customerCheckin 或 item.customerCheckin | 命名误导 |
| `getCustomerVo.json` Response | 实际是 `res.vo.customer.*` 嵌套, 不是 top-level customerVo | 命名误导 |
| `getPatientVo.json` Response | 实际是 `res.patient.*` top-level, 不是 patientVo | 命名误导 |
| `getPatientVoList.json` Response list item | 同时含 `item.customer` + `item.patient`, 不是单一 patientVo | 命名误导 |
| `medicalRecord.patientId` (L6693) | 实际是 `res.object.medicalRecord.patientId` 派生经 computeUnPlaceOrder | 命名误导 (S1-146) |
| `getCustomerVo` (L5243 patientObjectFactory) | 实际是 patientObjectFactory 在调用 customerVo, **patientObjectFactory 存 customer (L5930/L4947)** | **命名误导** |
| `selectOrderListFactory.items[].medicalRecord` (L34884) | 列表项嵌套, 不是 top-level medicalRecord | 命名误导 |
| `confirmArrivalOfAppoint` Request | 只传 appointId, 无 patientId/customerId | 命名误导 (看似桥实际无桥) |

---

## §19 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Customer 数据库表结构 | F | 需后端源码 |
| 2 | Patient 数据库表结构 | F | 需后端源码 |
| 3 | CustomerCheckin 数据库表结构 | F | 需后端源码 |
| 4 | 3 对象完整字段列表 (含 L3 schema) | F | 需后端 |
| 5 | insertCustomerCheckin*.json 完整 Response schema | F | 需后端 |
| 6 | getAppointPatientVo / getAppointSchoolMateVo 完整 Response | F | 需后端 |
| 7 | 4 个 beginCustomerCheckin 类型 (type=1/5/其它) | C (前端 16 处) | 需业务定义 |
| 8 | 6 字段 ID 完整外键关系 | F (L3) | 需后端 |
| 9 | Customer ↔ CustomerCheckin 桥 (经 Patient) | C | 需业务定义 |
| 10 | appointOrderCtrl 是否未来启用 | F | 需产品决策 |
| 11 | customerVo/patientVo/customerCheckinVo 命名历史 (是否曾有 VO 容器) | F | 需 git log |
| 12 | 18 Controller 完整 HTML 布局 | F | 需 HTML |
| 13 | L8707 customerCheckin.patientId 历史 | C (注释) | 需 git log |
| 14 | 16 字符级 medicalRecordType 完整业务含义 (含 type=2/3/4) | F | 需后端 + 业务 |
| 15 | medicalRecordType==5 路由到 adminSalesRecord.myMaterialBill 的设计意图 | C | 需业务定义 |

---

## §20 Git / 完整性

### §20.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-209 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 210_*.md | ✓ |

### §20.2 Git 操作

```
git add -- 210_S1-147_Customer_Patient_CustomerCheckin身份链与MedicalRecord上游边界总审计.md
git diff --cached --name-only
git commit -m "docs(210): S1-147 Customer/Patient/CustomerCheckin 身份链与 MedicalRecord 上游边界总审计"
git push origin master
```

### §20.3 预期

- tracked = 217 → **218**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `24f07a184c39e23a46a123b6b8f0b215b099f45e` (S1-146 commit)

---

## 文档元信息

- **审计范围**：S1-147 (Customer / Patient / CustomerCheckin 上游身份链)
- **本轮新增文件**：`210_S1-147_Customer_Patient_CustomerCheckin身份链与MedicalRecord上游边界总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-148** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
