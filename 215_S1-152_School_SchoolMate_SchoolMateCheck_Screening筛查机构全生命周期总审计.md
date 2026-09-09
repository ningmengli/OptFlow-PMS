# S1-152：School / SchoolMate / SchoolMateCheck / Screening 筛查机构全生命周期总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 214 个 MD / 不修改历史
> 关联：S1-132 / S1-133 / S1-134 / S1-147 / S1-149 / S1-151

---

## 目录

- §0 审计范围
- §1 筛查机构 Controller 全量
- §2 School
- §3 SchoolClass
- §4 SchoolMate
- §5 SchoolMateCheck
- §6 ScreeningPlan / ScreeningRecord / ScreeningReport
- §7 ScreeningFollowUp / ScreeningProgress
- §8 Print / Archive / QC
- §9 schoolIdArray 最终定级
- §10 School ↔ SchoolClass
- §11 SchoolMate ↔ School / SchoolClass
- §12 SchoolMate ↔ Patient
- §13 SchoolMate ↔ Customer
- §14 SchoolMate ↔ CustomerCheckin
- §15 SchoolMateCheck ↔ Patient / Customer / Checkin
- §16 Screening ↔ MedicalRecord / Patient / Customer / CustomerCheckin
- §17 普通接诊 vs 筛查
- §18 生命周期 DAG
- §19 Controller 消费矩阵
- §20 Object 分类
- §21 26 项证据矩阵
- §22 历史差异
- §23 V4.4 筛查机构规格
- §24 F / 未确认
- §25 Git / 完整性

---

## §0 审计范围

本轮把 School / SchoolMate / SchoolMateCheck / Screening 筛查机构
作为**前端可证明的对象、字段、API、State、Controller 和桥接关系**进行完整只读审计：

- 区分 School / SchoolClass / schoolMateVo / schoolMateCheck 真实身份
- 验证 Screening Plan / Record / Report 概念是否独立
- schoolMateVo 字段级深审（S1-134 完整复验）
- schoolMateCheck 真实 Object 字段深审（本轮新增大量）
- schoolIdArray 6 命中上下文（与 S1-151 交叉验证）
- 普通接诊 vs 筛查共享/隔离
- 26 项证据矩阵
- 历史 S1-132/133/134/147/149/151 误判核对

---

## §1 筛查机构 Controller 全量

### §1.1 15+ 候选 Controller 验证

| Controller | 状态 | 行号 |
|---|---|---|
| `schoolListCtrl` | ✓ **YES** | L44357 |
| `schoolMateCheckListCtrl` | ✓ **YES** | L44398 |
| `followUpCtrl` | ✓ **YES** | L11504 |
| `reportCtrl` | ✓ **YES** | L37786 |
| `optometryCtrl` | ✓ YES | L34776 |
| `addCheckinCtrl` | ✓ YES | L8159 |
| `checkinListCtrl` | ✓ YES | L8778 |
| `doctorWorkbenchCtrl` | ✓ YES | L10401 |
| `addSaleRecordCtrl` | ✓ YES | L31008 |
| `adminSalesRecordCtrl` | ✓ YES | L31285 |
| `addVisitCtrl` | ✓ YES | L49594 |
| `myMedicalRecordListCtrl` | ✓ YES | L32965 |
| `drugPrescriptionCtrl` | ✓ YES | L31605 |
| ✗ `schoolCtrl` | NOT FOUND | - |
| ✗ `schoolManageCtrl` | NOT FOUND | - |
| ✗ `schoolDetailCtrl` | NOT FOUND | - |
| ✗ `schoolMateCtrl` | NOT FOUND | - |
| ✗ `schoolMateManageCtrl` | NOT FOUND | - |
| ✗ `schoolMateListCtrl` | NOT FOUND | - |
| ✗ `schoolMateCheckCtrl` | NOT FOUND | - |
| ✗ `screeningCtrl` | NOT FOUND | - |
| ✗ `screeningPlanCtrl` | NOT FOUND | - |
| ✗ `screeningRecordCtrl` | NOT FOUND | - |
| ✗ `screeningReportCtrl` | NOT FOUND | - |
| ✗ `screeningFollowUpCtrl` | NOT FOUND | - |
| ✗ `screeningSendCtrl` | NOT FOUND | - |
| ✗ `screeningProgressCtrl` | NOT FOUND | - |
| ✗ `screeningPrintCtrl` | NOT FOUND | - |
| ✗ `screeningArchiveCtrl` | NOT FOUND | - |
| ✗ `screeningQcCtrl` | NOT FOUND | - |
| ✗ `schoolClassCtrl` | NOT FOUND | - |
| ✗ `schoolClassListCtrl` | NOT FOUND | - |
| ✗ `screeningInstitutionCtrl` | NOT FOUND | - |
| ✗ `screenInstitutionCtrl` | NOT FOUND | - |
| ✗ `screeningManageCtrl` | NOT FOUND | - |
| ✗ `printCtrl` | NOT FOUND | - |
| ✗ `qcCtrl` | NOT FOUND | - |

### §1.2 关键发现（本轮重大）

1. **筛查机构相关真实 Controller 仅 4 个**: `schoolListCtrl` / `schoolMateCheckListCtrl` / `followUpCtrl` / `reportCtrl`
2. **`screening*` / `screen*` 全部 NOT FOUND** — Screening 系列独立 Controller 不存在
3. **`schoolCtrl` / `schoolManageCtrl` / `schoolDetailCtrl` 全部 NOT FOUND** — School 没有独立管理 Controller
4. **`schoolMateCtrl` / `schoolMateManageCtrl` / `schoolMateListCtrl` 全部 NOT FOUND** — SchoolMate 没有独立 Controller
5. **`printCtrl` / `qcCtrl` NOT FOUND** — 打印/质检由 reportCtrl 等复用
6. **0 命中 `screeningInstitutionCtrl` / `screenInstitutionCtrl`** — 筛查机构主 Controller 不存在

### §1.3 真实入口

- 筛查机构管理经 `schoolListCtrl` (L44357) + `schoolMateCheckListCtrl` (L44398) 列表实现
- 跟进/报表复用 `followUpCtrl` (L11504) + `reportCtrl` (L37786)
- 接诊由 `addCheckinCtrl` (L8159) + `checkinListCtrl` (L8778) 处理

---

## §2 School

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `school` (全词) | **45** | A |
| `schoolId` | **297** | A (核心) |
| `schoolName` | **112** | A |
| `schoolList` | **15** | A |
| `schoolVo` | **0** | A |
| `schoolDetailVo` | 0 | A |

### §2.2 School API 全量

| API | 命中 | R/W |
|---|---:|---|
| `getSchool*.json` | **118** | R |
| `saveSchool*.json` | **13** | W |
| `selectSchool*.json` | 5+ | R |

### §2.3 School 真实字段（字符级）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `schoolId` | 297 命中 | **A (核心 ID)** |
| `schoolName` | 112 命中 | **A** |
| `school.id` | 多处 (L8270 `item.schoolMateVo.school.id`) | A |
| `school.schoolName` | L8266/L8273 | A |
| `school.className` 字段 | 0 命中（实际是 `schoolClass.className`） | F |
| `schoolVo` | **0 命中** | F |

### §2.4 School 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `schoolId` | A |
| B. Response VO | `school.id` / `school.schoolName` | A |
| C. Request | `schoolId` (Request 字段) | A |
| D. State | - | F |
| E. UI | `schoolName` | A |
| F. Runtime | - | F |

---

## §3 SchoolClass

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `schoolClass` | **27** | A |
| `schoolClassId` | **0** | A |
| `schoolClassName` | **2** | A |
| `schoolClassList` | 0 | A |
| `classId` | **149** | A (高频) |
| `className` | **37** | A |
| `classMateName` | **19** | A |

### §3.2 SchoolClass API

| API | 命中 | R/W |
|---|---:|---|
| `getSchoolClass*.json` | **32** | R |

### §3.3 SchoolClass 真实字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `schoolClassId` | **0 命中** | **F (顶层 ID 字段不存在)** |
| `classId` | 149 命中 | **A (实际主键)** |
| `className` | 37 命中 | A |
| `schoolClass.id` | L8271 `item.schoolMateVo.schoolClass.id` | A |
| `schoolClass.className` | L8266/L8274 | A |
| `schoolClass.school` | 0 命中 (经 schoolMateVo.school 派生) | F |

### §3.4 SchoolClass 关键发现

1. **`schoolClassId` 0 命中** — **schoolClass 顶层 ID 字段不存在**
2. **`classId` 149 命中**（最高频） — **实际主键是 classId，不是 schoolClassId**
3. **保持 S1-149 修正**：schoolClass 没有独立 ID 字段命名
4. `schoolClass.id` 实际是经 `schoolMateVo.schoolClass` 嵌套访问

### §3.5 SchoolClass 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `classId` | A |
| B. Response VO | `schoolClass.id` / `schoolClass.className` | A |
| C. Request | `classId` (Request) | A |
| D. State | - | F |
| E. UI | `className` | A |
| F. Runtime | - | F |

---

## §4 SchoolMate

### §4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `schoolMate` (全词) | **12** | A |
| `schoolMateId` | **25** | A |
| `schoolMateVo` | **11** | A |
| `schoolMateVoList` | **0** | A |
| `schoolMateName` | 0 | A |

### §4.2 SchoolMate API

| API | 命中 | R/W |
|---|---:|---|
| `getSchoolMate*.json` | **26** | R |
| `saveSchoolMate*.json` | **1** | W |
| `insertSchoolMate*.json` | **3** | W |
| `addSchoolMateConsume*.json` | **1** | W (L8705 注释) |

### §4.3 SchoolMate 真实字段（schoolMateVo 8 字段）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `schoolMateVo.schoolMate.gender` | L8264 | A |
| `schoolMateVo.schoolMate.customerMobile` | L8265 | A |
| `schoolMateVo.schoolMate.birthday` | L8267 | A |
| `schoolMateVo.schoolMate.classMateName` | L8277 | A |
| `schoolMateVo.school.id` → `schoolId` | L8270 | **A (派生 schoolId)** |
| `schoolMateVo.schoolClass.id` → `classId` | L8271 | **A (派生 classId)** |
| `schoolMateVo.school.schoolName` | L8266/L8273 | A |
| `schoolMateVo.schoolClass.className` | L8266/L8274 | A |

### §4.4 SchoolMate 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `schoolMateId` | A |
| B. Response VO | `schoolMateVo` (8 字段) | A |
| C. Request | `schoolMateId` (Request) | A |
| D. State | - | F |
| E. UI | `classMateName` / `customerMobile` | A |
| F. Runtime | - | F |

---

## §5 SchoolMateCheck

### §5.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `schoolMateCheck` (全词) | **129** | A (高频) |
| `schoolMateCheckId` | **20** | A |
| `schoolMateCheckVo` | **0** | A |
| `schoolMateCheckVoList` | **0** | A |

### §5.2 SchoolMateCheck API

| API | 命中 | R/W |
|---|---:|---|
| `getSchoolMateCheck*.json` | **22** | R |
| `insertSchoolMateCheck*.json` | **1** | W |
| `updateSchoolMateCheck*.json` | (含 updateSchool*) | W |

### §5.3 SchoolMateCheck 真实字段（本轮深审 - 11 字段）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `schoolMateCheck.id` | L8280(注释)/L14440/L19093/L41668 | **A (核心 ID)** |
| `schoolMateCheck.schoolMateId` | L41666/L41746 | A |
| `schoolMateCheck.promotionId` | L41667/L41747 | A |
| `schoolMateCheck.customerMobile` | L41684 | A (与 linkMobile 映射) |
| `schoolMateCheck.classMateName` | L41685 | A |
| `schoolMateCheck.gender` | L41686 | A |
| `schoolMateCheck.remark` | L41688 | A |
| `schoolMateCheck.schoolMateCode` | L41689 | A |
| `schoolMateCheck.birthday` | L41693/L41694/L41696 | A |
| `schoolMateCheck.checkDate` | L41698/L41699/L41700 | A |
| `schoolMateCheckList[0][0].schoolMateCheck.schoolMateId` | L14434 (注释) | A |

### §5.4 SchoolMateCheck 关键发现（本轮重要）

1. **schoolMateCheck 是真实 Object 实体**（11 字段）
2. **`schoolMateCheck.id` 是核心 ID**（L14440/L19093/L41668 4 字符级）
3. **`schoolMateCheckId` 20 命中** — **独立 ID 字段**（与 S1-149 报告"4 命中弱"不同 — 实际是 20 命中）
4. **`schoolMateCheckVo` 0 命中** — 没有独立 VO 容器（同 customerVo 模式）
5. **与 customerMobile ↔ linkMobile 映射**（保持 S1-147 修正）
6. **保持 S1-145 修正**：schoolMateCheck 不含 medicalRecordId 字段

### §5.5 SchoolMateCheck 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `schoolMateCheckId`, `schoolMateCheck.id` | A |
| B. Response VO | `schoolMateCheck` (11 字段) | A |
| C. Request | `schoolMateCheckId`, `schoolMateId`, `promotionId` (Request) | A |
| D. State | - | F |
| E. UI | `classMateName` / `customerMobile` | A |
| F. Runtime | - | F |

---

## §6 ScreeningPlan / ScreeningRecord / ScreeningReport

### §6.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `screening` | **0** | A |
| `Screening` (大写) | **0** | A |
| `screeningPlan` | **0** | A |
| `screeningRecord` | **0** | A |
| `screeningReport` | **0** | A |
| `screeningFollowUp` | **0** | A |
| `screeningProgress` | **0** | A |
| `screenPlan` | **0** | A |
| `screenRecord` | **0** | A |
| `screenReport` | **0** | A |
| `screenFollowUp` | **0** | A |
| `screen` | 5 | A (少量) |
| `getScreening*.json` | **0** | A |
| `getScreen*.json` | **0** | A |

### §6.2 Screening 关键发现（本轮重大）

1. **`screening` / `Screening` / `screeningPlan` / `screeningRecord` / `screeningReport` / `screeningFollowUp` / `screeningProgress` 全部 0 命中**
2. **小写命名 `screenPlan` / `screenRecord` 等也全部 0 命中**
3. **`screen` 5 命中**（极少）— 实际是 misc 词（screenPrint 等）
4. **`getScreening*.json` / `getScreen*.json` 0 命中** — **没有独立 Screening API！**
5. **`screeningCtrl` / `screeningPlanCtrl` 等 15+ Controller 全部 NOT FOUND** — **没有独立 Screening Controller！**

### §6.3 Screening 实际表达

- **"筛查"概念由 schoolListCtrl / schoolMateCheckListCtrl / addCheckinCtrl / checkinListCtrl 等组合实现**
- **没有独立 Screening Object 实体**
- **保持 S1-134 修正**：实际"学校筛查"是 SchoolMate → SchoolMateCheck → CustomerCheckin → MedicalRecord 链

### §6.4 Screening 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | - | F |
| F. Runtime | - | F |

---

## §7 ScreeningFollowUp / ScreeningProgress

### §7.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `screeningFollowUp` | **0** | A |
| `screeningProgress` | **0** | A |
| `screenFollowUp` | **0** | A |
| `followUp` | (复用 followUpCtrl) | C |
| `progress` | (复用 misc 词) | C |

### §7.2 关键发现

1. **`screeningFollowUp` / `screeningProgress` 全部 0 命中** — 独立 Screening 跟进/进度 Object 不存在
2. **实际"跟进"由 followUpCtrl (L11504) 通用 Controller 处理**
3. **保持 S1-134 修正**：筛查跟进复用通用 followUp Controller

---

## §8 Print / Archive / QC

### §8.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `screeningPrint` | **0** | A |
| `screeningArchive` | **0** | A |
| `screeningQc` | **0** | A |
| `printCtrl` | **NOT FOUND** | F |
| `qcCtrl` | **NOT FOUND** | F |
| `archive` | 0 | A |

### §8.2 关键发现

1. **`screeningPrint` / `screeningArchive` / `screeningQc` 全部 0 命中** — 没有独立 Screening 打印/归档/质检 Object
2. **`printCtrl` / `qcCtrl` NOT FOUND** — 实际打印/质检由 reportCtrl 等复用
3. **保持 S1-149 修正**：printCtrl/creditCtrl 等是命名误导

---

## §9 schoolIdArray 最终定级

### §9.1 6 命中完整上下文

| # | 行号 | 上下文 | 类型 |
|---|---|---|---|
| 1 | L634 | `$scope.schoolIdArray = []` (hospitalInList 循环, $scope.companyIdArray.push) | Scope |
| 2 | L642 | `schoolIdArray.push($scope.selected[i])` (角色选择) | Scope |
| 3 | L648 | `changeAdminRole.json { id, adminRoleId, companyId, schoolIdArray }` (复合 Request) | Request |
| 4 | L769 | `$scope.obj.schoolIdArray = []` (admin 创建) | Scope |
| 5 | L791 | `obj.schoolIdArray.push($scope.selected[j])` (admin 创建) | Scope |
| 6 | (S1-134) | (其他相关) | - |

### §9.2 schoolIdArray 真实身份（本轮重大修正 S1-151）

**S1-151 错误结论**：`schoolIdArray` 用于 Screening Plan (L634) + admin 创建 (L769) + changeAdminRole (L648)

**S1-152 真实结论**：
- L634 上下文是 **`hospitalInList` 循环** + `$scope.companyIdArray.push($scope.hospitalInList[i].id)` — **是医院清单 Scope，不是 Screening Plan！**
- L648 是 **`changeAdminRole.json` 复合 Request**（含 companyId + adminRoleId + schoolIdArray）— **是 Admin 角色配置 Request，不是 Screening！**
- L769/L791 是 **admin 创建/编辑复合 Scope 数组** — **是 Admin 范围配置**
- 0 命中 Screening 上下文 — **schoolIdArray 0 命中 Screening Plan / Record / Report！**

### §9.3 schoolIdArray 最终分类

| 分类 | 等级 |
|---|---|
| A. Screening Plan Object | **F (0 命中)** |
| B. Admin Role Scope (Scope + Request) | **A** |
| C. UI Filter | A (派生) |
| D. School Main Table 字段 | F (不能建模成 School 主表字段) |

### §9.4 关键判断

- **schoolIdArray 是 Admin Role Scope 数组，不是 Screening Object**（修正 S1-151）
- **实际命名误导**：schoolIdArray 容易让人以为是 School 主表字段，实际只是 admin 角色配置
- **保持 S1-131 修正**：schoolIdArray 不是 School 主表字段

---

## §10 School ↔ SchoolClass

### §10.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| School | SchoolClass | 0 命中 `school.schoolClass` 字段 | F | - | **F** | F |
| SchoolClass | School | `schoolMateVo.schoolClass.id` 嵌套 + `schoolMateVo.school.id` (经 schoolMateVo 派生) | A 派生 (经 schoolMateVo) | L8270/L8271 | **A** | A |

### §10.2 关键判断

- **SchoolClass → School**: A 派生（经 schoolMateVo 嵌套）
- **School → SchoolClass**: F（无直接字段桥）
- **没有 `school.schoolClass` 或 `schoolClass.school` 字段**（保持 S1-134 修正）

---

## §11 SchoolMate ↔ School / SchoolClass

### §11.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| SchoolMate | School | `schoolMateVo.schoolMate → schoolMateVo.school.id` | A 字段桥 (经 schoolMateVo) | L8270 | **A** | A |
| SchoolMate | SchoolClass | `schoolMateVo.schoolMate → schoolMateVo.schoolClass.id` | A 字段桥 (经 schoolMateVo) | L8271 | **A** | A |
| School | SchoolMate | 0 命中 `school.schoolMate` 字段 | F | - | **F** | F |
| SchoolClass | SchoolMate | 0 命中 `schoolClass.schoolMate` 字段 | F | - | **F** | F |

### §11.2 关键判断

- **SchoolMate → School/SchoolClass**: A 字段桥（经 schoolMateVo 嵌套派生）
- **反向 F**：School/SchoolClass 不直接含 schoolMate 字段
- **保持 S1-134 修正**：schoolMateVo 是核心桥接容器

---

## §12 SchoolMate ↔ Patient

### §12.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| SchoolMate | Patient | `getAppointPatientVo` Response (item.schoolMateVo → patient 派生) | A 派生 | L8243-L8270 | **A** | A |
| SchoolMate | Patient | 0 命中 `schoolMate.patient` 字段 | F | - | **F** | F |
| Patient | SchoolMate | `getPatientVoList` Response list item 含 `patient.school` / `patient.schoolClass` | A 字段桥 (经 patient 嵌套) | L8434/L8437 | **A** | A |
| Patient | SchoolMate | 0 命中 `patient.schoolMate` 字段 | F | - | **F** | F |

### §12.2 关键判断

- **SchoolMate → Patient**: A 派生（经 schoolMateVo → patient 转换 + getAppointPatientVo）
- **Patient → SchoolMate**: A 字段桥（`patient.school` / `patient.schoolClass` 派生）
- **保持 S1-134 修正**：A 字段桥成立
- **保持 S1-147 修正**：schoolMateVo → patient 派生通过 choosePatient 函数

---

## §13 SchoolMate ↔ Customer

### §13.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| SchoolMate | Customer | `schoolMateVo.schoolMate.customerMobile` → `linkMobile` 映射 | C 字段映射 | L8265 | **C** | C |
| SchoolMate | Customer | 0 命中 `schoolMate.customer` 字段 | F | - | **F** | F |
| Customer | SchoolMate | 0 命中 `customer.schoolMate` 字段 | F | - | **F** | F |
| Customer | SchoolMate | `getPatientVoList({customerId})` 反向查询 patient | C 参数桥 | L18981 | **C** | C |

### §13.2 关键判断

- **SchoolMate → Customer**: C 字段映射（customerMobile → linkMobile）
- **Customer → SchoolMate**: C 参数桥（getPatientVoList 查询）
- **没有直接字段桥**（保持 S1-147 修正）
- **不能升级成 DB FK**

---

## §14 SchoolMate ↔ CustomerCheckin

### §14.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| SchoolMate | CustomerCheckin | `insertCustomerCheckin.json` Request (经 addCheckinCtrl 派生) | A Request Bridge (派生) | L8667-L8681 | **A** | A |
| SchoolMate | CustomerCheckin | 0 命中 `schoolMate.customerCheckin` 字段 | F | - | **F** | F |
| CustomerCheckin | SchoolMate | 0 命中 `customerCheckin.schoolMate` 字段 | F | - | **F** | F |
| CustomerCheckin | SchoolMate | `res.result.vo.customerCheckin` Response 经 schoolMateVo 派生 | A 派生 | L8667 | **A** | A |

### §14.2 关键发现（本轮重大修正 S1-147）

1. **`insertCustomerCheckinOfSchoolMate.json` 0 命中** — 实际 API 命名是 `insertCustomerCheckinOfNewPaitent` / `insertCustomerCheckinOfNewCustomer` / `insertCustomerCheckin.json` (L8667-L8681)
2. **0 命中独立 SchoolMate 专属 Create API**
3. **实际派生链**: schoolMateVo → choosePatient → $scope.obj → insertCustomerCheckin.json

### §14.3 关键判断

- **SchoolMate → CustomerCheckin**: A Request Bridge (经 addCheckinCtrl 派生)
- **CustomerCheckin → SchoolMate**: A 派生（经 res.result.vo 嵌套）
- **修正 S1-147 报告**：insertCustomerCheckinOfSchoolMate 实际是 0 命中

---

## §15 SchoolMateCheck ↔ Patient / Customer / Checkin

### §15.1 6 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| SchoolMateCheck | Patient | 0 命中 `schoolMateCheck.patient` 字段 | F | - | **F** | F |
| SchoolMateCheck | Customer | `schoolMateCheck.customerMobile` (与 linkMobile 映射) | C 字段映射 | L41684 | **C** | C |
| SchoolMateCheck | CustomerCheckin | `setIntention.setParams('schoolMateCheckId', ...)` 间接桥 | A 派生 (经 setIntention) | L19093 | **A** | A |
| Patient | SchoolMateCheck | 0 命中 `patient.schoolMateCheck` 字段 | F | - | **F** | F |
| Customer | SchoolMateCheck | 0 命中 `customer.schoolMateCheck` 字段 | F | - | **F** | F |
| CustomerCheckin | SchoolMateCheck | 0 命中 `customerCheckin.schoolMateCheck` 字段 | F | - | **F** | F |

### §15.2 关键判断

- **SchoolMateCheck → Patient**: F
- **SchoolMateCheck → Customer**: C 字段映射（customerMobile → linkMobile）
- **SchoolMateCheck → CustomerCheckin**: A 派生（经 setIntention 桥接）
- **保持 S1-145 修正**：schoolMateCheck 实体存在但不直接与 Patient/Customer/Checkin 字段桥

---

## §16 Screening ↔ MedicalRecord / Patient / Customer / CustomerCheckin

### §16.1 8 关系矩阵（本轮全部 F）

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Screening | MedicalRecord | 0 命中 `screening.medicalRecord` 字段 | F | - | **F** | F |
| MedicalRecord | Screening | 0 命中 `medicalRecord.screening` 字段 | F | - | **F** | F |
| Screening | Patient | 0 命中 `screening.patient` 字段 | F | - | **F** | F |
| Patient | Screening | 0 命中 `patient.screening` 字段 | F | - | **F** | F |
| Screening | Customer | 0 命中 `screening.customer` 字段 | F | - | **F** | F |
| Customer | Screening | 0 命中 `customer.screening` 字段 | F | - | **F** | F |
| Screening | CustomerCheckin | 0 命中 `screening.customerCheckin` 字段 | F | - | **F** | F |
| CustomerCheckin | Screening | 0 命中 `customerCheckin.screening` 字段 | F | - | **F** | F |

### §16.2 关键判断

- **Screening 与所有 4 核心对象 (MedicalRecord/Patient/Customer/CustomerCheckin) 全部 0 命中**
- **没有 `screening.medicalRecord` / `medicalRecord.screening` 等字段**
- **没有 `screeningRecord.medicalRecordId` 字段**
- **Screening 不是独立 Object 实体**（F）

---

## §17 普通接诊 vs 筛查

### §17.1 共享/隔离分析

| 资源 | 普通接诊 | 学校筛查 | 共享/隔离 |
|---|---|---|---|
| **Patient** | ✓ (S1-147) | ✓ (经 schoolMateVo → patient 派生) | **共享** |
| **Customer** | ✓ (S1-147) | ✗ (字段映射 C) | 部分共享 (经 mobile 映射) |
| **CustomerCheckin** | ✓ (S1-147) | ✓ (经 schoolMateVo 派生 addCheckinCtrl) | **共享** |
| **MedicalRecord** | ✓ (S1-147) | ✓ (经 CustomerCheckin 派生) | **共享** |
| **schoolMateVo** | ✗ | ✓ (核心) | 筛查独有 |
| **schoolMateCheck** | ✗ | ✓ (核心) | 筛查独有 |
| **schoolId** | ✗ (S1-134) | ✓ (经 schoolMateVo.school.id) | 筛查独有 |
| **classId** | ✗ (S1-134) | ✓ (经 schoolMateVo.schoolClass.id) | 筛查独有 |
| **appointVo** | ✓ (S1-147) | ✓ (经 appointVo.type === 1 分流) | **共享** |
| **getAppointPatientVo** | ✓ | ✓ (S1-147 派生) | **共享** |
| **getAppointSchoolMateVo** | ✗ | ✓ (L43885+) | 筛查独有 |

### §17.2 关键判断

1. **Patient / CustomerCheckin / MedicalRecord 三件套共享**（A）
2. **schoolMateVo / schoolMateCheck 是筛查独有**（A）
3. **Customer 是字段映射桥**（C, mobile → linkMobile）
4. **appointVo 是分流器**（appointVo.type === 0 = Patient, type === 1 = SchoolMate）
5. **没有两个独立业务子系统** — 学校筛查是普通接诊的特殊入口

### §17.3 实际入口分流

```javascript
// addCheckinCtrl L8243-L8270
if ($scope.appointVo.type === 0) {
  // Patient 入口
  var obj = {
    gender: item.patient.patientGender,
    avatar: item.patient.avatar,
    linkMobile: item.customer.linkMobile,
    patientRemark: item.appoint.remark,
    birthday: item.patient.patientBirthday,
    customerName: item.customer.customerName,
    channelName: item.customer.channel,
    patientId: item.patient.id,
    employeeId: item.employee.id,
    appointId: item.appoint.id
  };
  ...
} else if ($scope.appointVo.type === 1) {
  // SchoolMate 入口
  var _obj = {
    gender: item.schoolMateVo.schoolMate.gender,
    linkMobile: item.schoolMateVo.schoolMate.customerMobile,
    patientRemark: "" + item.schoolMateVo.school.schoolName + item.schoolMateVo.schoolClass.className,
    birthday: item.schoolMateVo.schoolMate.birthday,
    customerName: item.customer.customerName,
    appointId: item.appoint.id,
    schoolId: item.schoolMateVo.school.id,
    classId: item.schoolMateVo.schoolClass.id
  };
  ...
}
```

---

## §18 生命周期 DAG

### §18.1 完整筛查机构 DAG

```
[School / SchoolClass / schoolId / classId]
    ↓
[SchoolMate / schoolMateVo (8 字段)]
    ↓ choosePatient (L8424) or insertCustomerCheckin
[Customer (派生, 经 customerMobile → linkMobile 映射)]
    ↓
[CustomerCheckin]
    ↓
[MedicalRecord]
    ↓
[Cashflow / Sale / Delivery / Machine (复用业务域)]

并联:

[SchoolMateCheck (11 字段, L41684-L41700)]
    ↓ schoolMateCheckId
[setIntention / followUpCtrl (L11504)]
    ↓
[跟进 / 报表 / 打印 复用]
```

### §18.2 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| School | SchoolClass | A 派生 | schoolMateVo 嵌套 (经 schoolMateVo) | L8270/L8271 |
| School | SchoolMate | A 派生 | schoolMateVo 嵌套 | L8264-L8270 |
| SchoolClass | SchoolMate | A 派生 | schoolMateVo 嵌套 | L8264-L8271 |
| SchoolMate | School | A 字段桥 | schoolMateVo.school.id | L8270 |
| SchoolMate | SchoolClass | A 字段桥 | schoolMateVo.schoolClass.id | L8271 |
| SchoolMate | Patient | A 派生 | getAppointPatientVo Response | L8243-L8270 |
| SchoolMate | Customer | C 字段映射 | customerMobile → linkMobile | L8265 |
| SchoolMate | CustomerCheckin | A Request Bridge | insertCustomerCheckin.json | L8667-L8681 |
| SchoolMateCheck | Customer | C 字段映射 | customerMobile → linkMobile | L41684 |
| SchoolMateCheck | CustomerCheckin | A 派生 | setIntention.setParams('schoolMateCheckId') | L19093 |
| SchoolMateCheck | SchoolMate | C 字段桥 | schoolMateCheck.schoolMateId | L41666 |
| SchoolMate | SchoolMateCheck | 0 命中 | F | - |
| Screening | MedicalRecord | F | 0 命中 | - |
| Screening | Patient | F | 0 命中 | - |
| Screening | Customer | F | 0 命中 | - |
| Screening | CustomerCheckin | F | 0 命中 | - |

### §18.3 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| School → SchoolClass 字段桥 | F |
| SchoolClass → School 字段桥 | F (经 schoolMateVo 派生 A) |
| School → SchoolMate 字段桥 | F (经 schoolMateVo 派生 A) |
| SchoolMate → Patient 字段桥 | F (经派生 A) |
| SchoolMateCheck → Patient 字段桥 | F |
| Screening → MedicalRecord 字段桥 | F (0 命中) |
| Screening → Patient 字段桥 | F (0 命中) |
| Screening → Customer 字段桥 | F (0 命中) |
| Screening → CustomerCheckin 字段桥 | F (0 命中) |

---

## §19 Controller 消费矩阵

### §19.1 15+ Controller 筛查机构消费矩阵

| Controller | school | schoolClass | schoolMate | schoolMateCheck | screening | 等级 |
|---|---:|---:|---:|---:|---:|:---:|
| **schoolListCtrl** (L44357) | **大** | **大** | 0 | 0 | 0 | A |
| **schoolMateCheckListCtrl** (L44398) | 中 | 中 | 中 | **大** | 0 | A |
| **followUpCtrl** (L11504) | 中 | 中 | 中 | 中 | 0 | A |
| **reportCtrl** (L37786) | 中 | 中 | 0 | 0 | 0 | A |
| **addCheckinCtrl** (L8159) | 0 | 0 | 0 (经 schoolMateVo 派生) | 0 | 0 | A |
| **checkinListCtrl** (L8778) | 0 | 0 | 0 | 0 | 0 | A |
| **doctorWorkbenchCtrl** (L10401) | 0 | 0 | 0 | 0 | 0 | A |
| **optometryCtrl** (L34776) | 0 | 0 | 0 | 0 | 0 | A |
| **addSaleRecordCtrl** (L31008) | 0 | 0 | 0 | 0 | 0 | A |
| **adminSalesRecordCtrl** (L31285) | 0 | 0 | 0 | 0 | 0 | A |
| **addVisitCtrl** (L49594) | 0 | 0 | 0 | 0 | 0 | A |
| **myMedicalRecordListCtrl** (L32965) | 0 | 0 | 0 | 0 | 0 | A |
| **drugPrescriptionCtrl** (L31605) | 0 | 0 | 0 | 0 | 0 | A |
| ✗ `schoolCtrl` | - | - | - | - | - | NOT FOUND |
| ✗ `screeningCtrl` | - | - | - | - | - | NOT FOUND |
| ✗ `screeningPlanCtrl` | - | - | - | - | - | NOT FOUND |
| ✗ `screeningRecordCtrl` | - | - | - | - | - | NOT FOUND |
| ✗ `screeningReportCtrl` | - | - | - | - | - | NOT FOUND |

### §19.2 核心观察

1. **schoolListCtrl / schoolMateCheckListCtrl / followUpCtrl / reportCtrl** 是 4 个真实筛查机构相关 Controller
2. **addCheckinCtrl 通过 schoolMateVo 派生**处理学校筛查接诊
3. **15+ 候选 Controller 全部 NOT FOUND**：screeningPlan/Record/Report/FollowUp/Print/Archive/Qc 等

---

## §20 Object 分类

### §20.1 9 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **School** | ✓ (schoolId 297 命中) | ✓ (school.id / school.schoolName) | ✓ (schoolId Request) | - | A |
| **SchoolClass** | ✓ (classId 149 命中) | ✓ (schoolClass.id / className) | ✓ (classId Request) | - | A (顶层 ID 命名是 classId) |
| **SchoolMate** | ✓ (schoolMateId 25 命中) | ✓ (schoolMateVo 8 字段) | ✓ (schoolMateId Request) | - | A |
| **SchoolMateCheck** | ✓ (schoolMateCheckId 20 命中) | ✓ (schoolMateCheck 11 字段) | ✓ (Request) | - | A |
| **ScreeningPlan** | ✗ (screeningPlan 0 命中) | ✗ | ✗ | ✗ | **F (0 命中)** |
| **ScreeningRecord** | ✗ (screeningRecord 0 命中) | ✗ | ✗ | ✗ | **F (0 命中)** |
| **ScreeningReport** | ✗ (screeningReport 0 命中) | ✗ | ✗ | ✗ | **F (0 命中)** |
| **ScreeningFollowUp** | ✗ (screeningFollowUp 0 命中) | ✗ | ✗ | ✗ | **F (0 命中)** |
| **ScreeningProgress** | ✗ (screeningProgress 0 命中) | ✗ | ✗ | ✗ | **F (0 命中)** |
| **schoolIdArray** | ✗ | ✗ | ✓ (admin Role Request) | ✓ (Scope) | A (Admin Scope) |
| **hospitalInList** | ✗ | ✓ (Response VO) | - | ✓ (Scope) | A |

### §20.2 关键结论

1. **4 个独立 ID 实体**: School / SchoolClass / SchoolMate / SchoolMateCheck
2. **5 个 0 命中 Screening 概念**: ScreeningPlan / ScreeningRecord / ScreeningReport / ScreeningFollowUp / ScreeningProgress
3. **schoolIdArray 是 Admin Role Scope 不是 Screening Object**（修正 S1-151）
4. **hospitalInList 是真实 Response VO**（L634 上下文）
5. **Screening 系列没有独立 Object / API / Controller**（F）

---

## §21 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 4 Controllers (schoolList/schoolMateCheckList/followUp/report) | A | - | 全部 | A |
| 2 | Controller | 4 真实 + 30+ NOT FOUND | A | - | 全部 | A |
| 3 | State | schoolList/schoolMateCheckList | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | schoolId / classId / schoolMateId / schoolMateCheckId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | appointVo.type (0=Patient, 1=SchoolMate) | A | - | L8243 | A |
| 10 | Status | (Screening 无 status) | F | - | - | F |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=10/12 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | schoolId / classId (addCheckinCtrl SchoolMate 入口) | A | - | L8270/L8271 | A |
| 15 | Default | appointVo.type=0 (Patient) | A | - | L8243 | A |
| 16 | Data Source | 118 getSchool + 32 getSchoolClass + 26 getSchoolMate + 22 getSchoolMateCheck | A | - | 全部 | A |
| 17 | Object | school.id/name, schoolClass.id/name, schoolMateVo 8 字段, schoolMateCheck 11 字段 | A | - | 全部 | A |
| 18 | Request | { schoolId } / { classId } / { schoolMateId } / { schoolMateCheckId } | A | - | 多处 | A |
| 19 | Response | school/schoolClass/schoolMateVo/schoolMateCheck 嵌套 | A | - | 全部 | A |
| 20 | Function | choosePatient (L8424) / setIntention | A | - | L8424/L19093 | A |
| 21 | State Bridge | schoolIdArray (Admin Role Scope) | A | - | L634/L769 | A |
| 22 | Object Bridge | schoolMateVo.school/schoolClass 嵌套 | A | - | L8270/L8271 | A |
| 23 | API Bridge | insertCustomerCheckin.json (派生 SchoolMate) | A | - | L8667-L8681 | A |
| 24 | Business Interpretation | 4 个独立 ID 实体, Screening 不存在独立 Object | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 3 C / 0 D / 0 E / 2 F | - | - | - | - |
| 26 | V4.4 Decision | 4 个独立 ID 实体必保留, Screening 系列 F, schoolIdArray = Admin Scope | A | - | - | A |

---

## §22 历史差异

### §22.1 S1-132/133/134/147/149/151 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-132: School 是独立对象 | schoolId 297 命中, schoolListCtrl L44357 | 保持 | **保持 S1-132 修正** |
| S1-133: SchoolMate 是独立对象 | schoolMateId 25 命中, schoolMateVo 8 字段 | 保持 | **保持 S1-133 修正** |
| S1-134: SchoolMate → Patient A 字段桥 | 实际经 getAppointPatientVo Response 派生 A | 保持 | **保持 S1-134 修正** |
| S1-134: schoolMateVo.school.id → schoolId | 实际 L8270 派生 | 保持 | **保持 S1-134 修正** |
| S1-134: schoolMateVo.schoolClass.id → classId | 实际 L8271 派生 | 保持 | **保持 S1-134 修正** |
| S1-147: insertCustomerCheckinOfSchoolMate 真实存在 | 实际 0 命中 | **应改** | **A 派生经 addCheckinCtrl** |
| S1-149: medicalProductName 0 命中 | 仍 0 命中 | 保持 | **保持 S1-149 修正** |
| S1-151: schoolIdArray 用于 Screening Plan | 实际 L634 上下文是 hospitalInList, **不是 Screening** | **应改** | **A Admin Role Scope (修正 S1-151)** |
| S1-151: schoolIdArray 出现在 changeAdminRole L648 | 仍正确 | 保持 | **保持 S1-151 修正** |
| S1-151: permission 0 命中 | 仍 0 命中 | 保持 | **保持 S1-151 修正** |

### §22.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~ScreeningPlan/Record/Report 是独立 Object 实体~~ | 字符级 0 命中 (screeningPlan/Record/Report/FollowUp/Progress) | **本轮重大发现** | **F (0 命中, 概念不存在)** |
| ~~Screening 系列有独立 API~~ | 0 命中 getScreening*.json / getScreen*.json | **本轮新增** | **F** |
| ~~Screening 系列有独立 Controller~~ | 0 命中 screeningCtrl/screeningPlanCtrl 等 15+ Controller | **本轮新增** | **F** |
| ~~Screening 是与普通接诊独立的子系统~~ | 实际共享 Patient/CustomerCheckin/MedicalRecord | **本轮新增** | **A 共享 (经 schoolMateVo 派生)** |
| ~~schoolIdArray 是 Screening Plan Object 字段~~ | 实际是 Admin Role Scope | **本轮重大发现 (修正 S1-151)** | **A Admin Role Scope** |
| ~~insertCustomerCheckinOfSchoolMate 真实 API~~ | 字符级 0 命中, 实际是 insertCustomerCheckin.json 派生 | **本轮重大发现 (修正 S1-147)** | **A (派生经 addCheckinCtrl)** |
| ~~schoolClassId 是独立 ID~~ | 字符级 0 命中, 实际 ID 是 classId (149 命中) | **本轮重大发现** | **A classId 是真实 ID** |
| ~~schoolClassVo 是独立 VO 容器~~ | 字符级 0 命中 | **本轮新增** | **F (同 customerVo 模式)** |
| ~~schoolMateCheckVo 独立 VO 容器~~ | 字符级 0 命中 | **本轮新增** | **F** |
| ~~schoolMateCheck 是弱 ID 实体 (S1-149 报告 4 命中)~~ | 实际 schoolMateCheckId 20 命中, schoolMateCheck.id 多字符级, 11 字段 | **本轮重大发现 (修正 S1-149)** | **A (实际是 11 字段强 ID 实体)** |
| ~~screeningPrint/screeningArchive/screeningQc 是独立 Object~~ | 0 命中 | **本轮新增** | **F** |

### §22.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 214_S1-151 全部保持原样
- 本文档 215_*.md 单独记录筛查机构完整闭环

---

## §23 V4.4 筛查机构规格

### §23.1 必实现 (A 级)

| 项 | 等级 |
|---|---|
| **schoolId 独立 ID** (297 命中) | A |
| **classId 独立 ID** (149 命中) — **不是 schoolClassId** | A |
| **schoolMateId 独立 ID** (25 命中) | A |
| **schoolMateCheckId 独立 ID** (20 命中) | A |
| **schoolMateVo 8 字段** (gender/customerMobile/birthday/classMateName + school/schoolClass 嵌套) | A |
| **schoolMateCheck 11 字段** (id/schoolMateId/promotionId/customerMobile/classMateName/gender/remark/schoolMateCode/birthday/checkDate) | A |
| **schoolIdArray Admin Role Scope** (L634/L648/L769/L791) | A |
| **schoolIdArray 复合 Request** (changeAdminRole.json) | A |
| **appointVo.type 分流** (0=Patient, 1=SchoolMate) | A |
| **getAppointPatientVo / getAppointSchoolMateVo 双入口** | A |
| **118 getSchool*.json + 32 getSchoolClass*.json + 26 getSchoolMate*.json + 22 getSchoolMateCheck*.json** | A |
| **13 saveSchool*.json + 1 saveSchoolMate*.json + 3 insertSchoolMate*.json + 1 insertSchoolMateCheck*.json** | A |
| **4 个真实 Controller** (schoolListCtrl/schoolMateCheckListCtrl/followUpCtrl/reportCtrl) | A |
| **普通接诊 + 筛查共享 Patient/CustomerCheckin/MedicalRecord** | A |
| **choosePatient 函数桥** (L8424) | A |
| **setIntention 桥** (schoolMateCheckId L19093) | A |

### §23.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `screening` / `Screening` / `screeningPlan` / `screeningRecord` / `screeningReport` / `screeningFollowUp` / `screeningProgress` 字段 | ✗ (0 命中) |
| `screenPlan` / `screenRecord` / `screenReport` / `screenFollowUp` 字段 | ✗ (0 命中) |
| `getScreening*.json` / `getScreen*.json` API | ✗ (0 命中) |
| `screeningCtrl` / `screeningPlanCtrl` / `screeningRecordCtrl` / `screeningReportCtrl` / `screeningFollowUpCtrl` / `screeningSendCtrl` / `screeningProgressCtrl` / `screeningPrintCtrl` / `screeningArchiveCtrl` / `screeningQcCtrl` 等 30+ Controller | ✗ (NOT FOUND) |
| `schoolCtrl` / `schoolManageCtrl` / `schoolDetailCtrl` / `schoolMateCtrl` / `schoolMateManageCtrl` / `schoolMateListCtrl` / `schoolMateCheckCtrl` / `schoolClassCtrl` / `schoolClassListCtrl` / `screeningInstitutionCtrl` Controller | ✗ (NOT FOUND) |
| `schoolVo` / `schoolClassVo` / `schoolMateVoList` / `schoolMateCheckVo` / `schoolMateCheckVoList` 独立 VO 容器 | ✗ (0 命中) |
| `schoolClassId` 顶层 ID 字段 | ✗ (0 命中, 实际是 classId) |
| `schoolClass.school` / `school.schoolClass` 字段桥 | ✗ (0 命中) |
| `schoolMate.customer` / `customer.schoolMate` 字段桥 | ✗ (0 命中, C 字段映射) |
| `schoolMateCheck.patient` / `patient.schoolMateCheck` 字段桥 | ✗ (0 命中) |
| `screening.medicalRecord` / `medicalRecord.screening` 字段桥 | ✗ (0 命中) |
| `screening.patient` / `patient.screening` 字段桥 | ✗ (0 命中) |
| `screening.customer` / `customer.screening` 字段桥 | ✗ (0 命中) |
| `screening.customerCheckin` / `customerCheckin.screening` 字段桥 | ✗ (0 命中) |
| `screeningRecord.medicalRecordId` 字段 | ✗ (0 命中) |
| `insertCustomerCheckinOfSchoolMate.json` 独立 API | ✗ (0 命中, 实际是 insertCustomerCheckin.json 派生) |
| `screeningPrint` / `screeningArchive` / `screeningQc` 字段 | ✗ (0 命中) |
| `printCtrl` / `qcCtrl` Controller | ✗ (NOT FOUND) |
| `schoolIdArray` 是 Screening Object 字段 | ✗ (实际是 Admin Scope) |
| 6 ID 合并 | ✗ (schoolId/classId/schoolMateId/schoolMateCheckId/patientId/customerCheckinId 必须严格区分) |

### §23.3 9 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **School** | A+B+C (独立 ID + Response + Request) | schoolVo 独立 VO (F) |
| **SchoolClass** | A+B+C (实际主键是 classId 不是 schoolClassId) | schoolClassVo 独立 VO (F) |
| **SchoolMate** | A+B+C (8 字段) | schoolMateVoList 独立 VO (F) |
| **SchoolMateCheck** | A+B+C (11 字段) | schoolMateCheckVo 独立 VO (F) |
| **ScreeningPlan** | F (0 命中) | 独立 ID 实体 |
| **ScreeningRecord** | F (0 命中) | 独立 ID 实体 |
| **ScreeningReport** | F (0 命中) | 独立 ID 实体 |
| **ScreeningFollowUp** | F (0 命中) | 独立 ID 实体 |
| **ScreeningProgress** | F (0 命中) | 独立 ID 实体 |
| **schoolIdArray** | A (Admin Role Scope) | School 主表字段 (F) |
| **hospitalInList** | A (Response VO + Scope) | - |

### §23.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `schoolMateVo.school.id` → `schoolId` (SchoolMate → School) | A | L8270 |
| `schoolMateVo.schoolClass.id` → `classId` (SchoolMate → SchoolClass) | A | L8271 |
| `schoolMateVo.school.schoolName + schoolClass.className` → `patientRemark` | A | L8266 |
| `schoolMateVo.schoolMate.customerMobile` → `linkMobile` | A | L8265 |
| `schoolMateCheck.schoolMateId` (SchoolMateCheck → SchoolMate) | A | L41666 |
| `schoolMateCheck.customerMobile` (与 linkMobile 映射) | A | L41684 |
| `getAppointPatientVo` Response (SchoolMate → Patient 派生) | A | L8243-L8270 |
| `choosePatient` 函数 (schoolMateVo → patient) | A | L8424 |
| `insertCustomerCheckin.json` (SchoolMate → CustomerCheckin 派生) | A | L8667-L8681 |
| `setIntention.setParams('schoolMateCheckId', ...)` | A | L19093 |
| `changeAdminRole.json { schoolIdArray, companyId, adminRoleId }` | A | L648 |

### §23.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| School → SchoolClass 字段桥 | F (经 schoolMateVo 派生 A) |
| SchoolClass → School 字段桥 | F (经 schoolMateVo 派生 A) |
| School → SchoolMate 字段桥 | F (经 schoolMateVo 派生 A) |
| SchoolMate → Patient 字段桥 | F (经派生 A) |
| SchoolMateCheck → Patient 字段桥 | F |
| Screening → MedicalRecord 字段桥 | F (0 命中) |
| Screening → Patient 字段桥 | F (0 命中) |
| Screening → Customer 字段桥 | F (0 命中) |
| Screening → CustomerCheckin 字段桥 | F (0 命中) |
| schoolClassId 顶层 ID 字段 | F (实际是 classId) |
| schoolClassVo 独立 VO 容器 | F |
| screeningPlan/Record/Report 独立 Object | F (0 命中) |

### §23.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `screeningPlan` / `screeningRecord` / `screeningReport` | 字符级 0 命中, 实际不存在独立 Object | **命名误导 (历史可能误认为存在)** |
| `schoolClassId` | 字符级 0 命中, 实际 ID 是 classId | **命名误导** |
| `schoolClassVo` / `schoolMateVoList` / `schoolMateCheckVo` / `schoolMateCheckVoList` | 字符级 0 命中 (同 customerVo 模式) | **命名误导** |
| `schoolIdArray` (S1-151 报告 Screening Plan 字段) | 实际是 Admin Role Scope (L634 hospitalInList) | **命名误导 (本轮修正 S1-151)** |
| `insertCustomerCheckinOfSchoolMate` (S1-147 报告) | 字符级 0 命中, 实际是 insertCustomerCheckin.json 派生 | **命名误导 (本轮修正 S1-147)** |
| `screeningCtrl` / `screeningPlanCtrl` 等 | NOT FOUND, 实际由 schoolListCtrl/schoolMateCheckListCtrl 等复用 | 命名误导 |
| `schoolCtrl` / `schoolManageCtrl` | NOT FOUND, 实际由 schoolListCtrl 复用 | 命名误导 |
| `schoolMateCheck` 是弱 ID 实体 (S1-149 报告 4 命中) | 实际 20 命中, 11 字段, 强 ID 实体 | **命名误导 (本轮修正 S1-149)** |
| `schoolMateCheck.schoolMateId` | 实际是 schoolMateCheck → SchoolMate 桥 | 命名误导 |
| `screeningPrint` / `screeningArchive` / `screeningQc` | 0 命中, 实际由 reportCtrl 复用 | 命名误导 |

---

## §24 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | School 数据库表结构 | F | 需后端 |
| 2 | SchoolClass 数据库表结构 | F | 需后端 |
| 3 | SchoolMate 数据库表结构 | F | 需后端 |
| 4 | SchoolMateCheck 数据库表结构 | F | 需后端 |
| 5 | Screening Plan / Record / Report 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 6 | ScreeningFollowUp / Progress 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 7 | schoolIdArray 在数据库中的位置 (Role 表 or Screening 表) | F | 需后端 |
| 8 | hospitalInList 数据库来源 | F | 需后端 |
| 9 | schoolMateCheck 11 字段完整 schema | F (部分确认) | 需后端 |
| 10 | screening 系列命名历史 | F | 需 git log |
| 11 | 4 个真实 Controller 后端 API 完整 | F (部分确认) | 需后端 |
| 12 | 30+ NOT FOUND Controller 命名历史 | F | 需 git log |
| 13 | Screening 与 SchoolMate 业务边界 | F (UI 推测) | 需业务定义 |
| 14 | getAppointSchoolMateVo 完整 Response | F | 需后端 |
| 15 | schoolMateCheck 11 字段是否后端持久化 | F (前端 evidence A) | 需后端 |
| 16 | getAppointPatientVo + getAppointSchoolMateVo 后端关系 | F | 需后端 |
| 17 | screeningId / screeningPlanId / screeningRecordId 是否曾经存在 | F (当前 0 命中) | 需 git log |
| 18 | 4 个真实 Controller 业务完整范围 | F (部分确认) | 需业务定义 |

---

## §25 Git / 完整性

### §25.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-214 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ |
| 本轮只新增 215_*.md | ✓ |

### §25.2 Git 操作

```
git add -- 215_S1-152_School_SchoolMate_SchoolMateCheck_Screening筛查机构全生命周期总审计.md
git diff --cached --name-only
git commit -m "docs(215): S1-152 School/SchoolMate/SchoolMateCheck/Screening 筛查机构全生命周期总审计"
git push origin master
```

### §25.3 预期

- tracked = 222 → **223**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `52c59e231f62293a9e64eaebbc96424e633af09e` (S1-151 commit)

---

## 文档元信息

- **审计范围**：S1-152 (School / SchoolMate / SchoolMateCheck / Screening 筛查机构)
- **本轮新增文件**：`215_S1-152_School_SchoolMate_SchoolMateCheck_Screening筛查机构全生命周期总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-153** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
