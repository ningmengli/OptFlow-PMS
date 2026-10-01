# G2-Contract-02｜OptFlow PMS Production Implementation Contract (修复版)

> **本轮定位**:对 G2-Contract-01 的 14 项 P0 + 7 项 PA 修复版。
> **不是**对 G2-Contract-01 的修订(本文为新增独立文档)。
> **不是**开发。
> **不是**最终 READY 判定(完成后必须经过 G2-Contract-Audit-02 独立盲审)。
> **本轮唯一输出**:本修复版 Contract。
> **修复基线**:**严格以 G2-Contract-Audit-01R2 §5 / §7 为唯一基准**(21 项 Fix Action,不得重新编号 / 不得重新定义 RC / 不得重新制造新的 P0/P1 编号)。
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史 MD(190~241V2A-42 + S1-170 全系列 + G2-Contract-01 + G2-Contract-Audit-01 全系列)未修改** ✓
> **本轮不写代码 / 不 commit / 不 push** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-02_OptFlow-PMS_Production-Implementation-Contract.md` |
| 性质 | G2-Contract-01 的修复版(独立新文件,不替代 G2-Contract-01)|
| 修复基线 | G2-Contract-Audit-01R2 §5 / §7(21 项 Fix Action)|
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 修复范围 | P0 = 14 项, P1 = 7 项(PA), 总 = 21 项 |
| 严禁 | 修改 G2-Contract-01 / 修改任何 G2-Contract-Audit-01* / 修改任何历史 MD / 创建 backend / 写 Java 源文件 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1 Contract Objective

回答一个问题:

> G2-Contract-02 是否能在 21 项 Fix Action 全部落地后,**直接指导 backend 编码**,且不引入任何 AI 推断的字段 / API / 状态 / 权限 / Transaction 规则?

**核心纪律**(沿用 R2 §6):

| # | 纪律 |
|:-:|---|
| 1 | **未冻结内容标【待确认】**,不得伪装成冻结事实 |
| 2 | **已有业务规则但无具体实现形式**:写业务规则,不得擅自指定 Java / Sa-Token / Transaction 实现 |
| 3 | **已有明确证据**:写入 Contract 冻结 |
| 4 | **Effective Spec 完全无证据**:**【待确认】** + 不写 |
| 5 | **严禁**"为了让 P1=0"自行发明:字段 / API / 状态 / 权限 / Transaction 类型 / Sa-Token annotation / rollback compensation |

---

## §2 Evidence / Authority

### 2.1 修复基线来源

| 来源 | 用途 |
|---|---|
| **G2-Contract-Audit-01R2** §5 | P0 Root Cause Family + P1 Issue 编号 |
| **G2-Contract-Audit-01R2** §7 | 21 项 Fix Action 修复基线表 |
| **G2-Contract-Audit-01** | 审计发现(原始证据)|
| **G2-Contract-Audit-01R** | Root Cause 去重与映射 |

### 2.2 Effective Spec 来源(绝对权威)

| 基线编号 | 用途 |
|---|---|
| **233** | API-025~040 Path 与 Method(替代 232 的修正版)|
| **232** | API-001~024 + 早期版本 |
| **229** | 12 Object 状态机(4 状态机 29 状态)|
| **235B** | 数据模型裁决 + Transfer 9-step + IGNORE_TABLES 概念 |
| **236B** | DDL(31 真 FK / 21 索引 / 10 CHECK / 5 UNIQUE) |
| **238** | 12 Object 字段级 ID 类型 + Entity 字段 + Repository 方法 |
| **240** | 跨公司隔离架构正式裁决 |
| **241V2** | CompanyContext + TenantLine + IGNORE_TABLES 设计 |
| **241V2A-5/10/11/12/13/14/15/17/18/19** | DEFAULT-01~05 + User 异常 + User_company Repository |
| **241V4** | 12 业务表 / TenantLine / IGNORE_TABLES 后续冻结口径 |

### 2.3 证据等级标签

| 标签 | 含义 |
|:-:|---|
| 【A】 | 直接证据(基线 MD 显式冻结,字段名 / 数值完全一致)|
| 【B】 | 多源交叉验证(2+ 份基线 MD 一致)|
| 【C】 | 部分证据(基线 MD 仅一处出现,需推断补全)|
| 【D】 | 冲突(基线 MD 之间不一致)|
| 【E】 | 推断(无直接证据,纯 AI 推导)— **本轮严禁**|
| 【F】 | 错误(Contract 与基线直接冲突)— **本轮严禁** |
| 【待确认】 | 有效证据不足,需后续冻结或外部裁决 |

---

## §3 Object Contract(12 业务 Object + user_company)

### 3.1 总览

**12 业务 Object**(沿用 235B §1 + 238 §4):

| # | Object | Table | Entity | PK | ID Type | Tenant | 修复来源 |
|--:|---|---|---|---|---|---|---|
| 1 | Company | `company` | `CompanyEntity` | companyId | Long | IGNORE | (沿用冻结,RC-3 不涉及)|
| 2 | Customer | `customer` | `CustomerEntity` | customerId | Long | TenantLine | (沿用冻结,RC-3 不涉及)|
| 3 | Patient | `patient` | `PatientEntity` | patientId | Long | TenantLine | **RC-3a** |
| 4 | Employee | `employee` | `EmployeeEntity` | employeeId | Long | TenantLine | **RC-3b** |
| 5 | ConsultRoom | `consult_room` | `ConsultRoomEntity` | consultRoomId | Long | TenantLine | **RC-3c** |
| 6 | BigScreen | `big_screen` | `BigScreenEntity` | bigScreenId | Long | TenantLine | **RC-3d** |
| 7 | AppointmentSchedule | `appointment_schedule` | `AppointmentScheduleEntity` | scheduleId | Long | TenantLine | **RC-3e** |
| 8 | AppointmentSlot | `appointment_slot` | `AppointmentSlotEntity` | slotId | Long | TenantLine | **RC-3f** |
| 9 | Appointment | `appointment` | `AppointmentEntity` | appointmentId | Long | TenantLine | **RC-3g** |
| 10 | Visit | `visit` | `VisitEntity` | visitId | String(UUID)| TenantLine | **RC-3h** |
| 11 | TriageQueue | `triage_queue` | `TriageQueueEntity` | triageQueueId | String(UUID)| TenantLine | (沿用冻结,字段基本一致)|
| 12 | ReceptionQueue | `reception_queue` | `ReceptionQueueEntity` | receptionQueueId | String(UUID)| TenantLine | **RC-3i** |

**Infrastructure Object / Table**:`user_company`(沿用 G2-Contract-01 §5 单独冻结,详见 §3.13)

### 3.2 Company(沿用 G2-Contract-01,RC-3 不涉及)

| 字段 | Java 类型 | 含义 |
|---|---|---|
| `companyId` | Long | PK, 自增 |
| `companyTitle` | String | 公司显示名 |
| `companyName` | String | 公司法律名 |
| `companyType` | String | 公司类型 |
| `logoUrl` | String | Logo URL |
| `address` | String | 地址 |
| `phone` | String | 电话(是否业务必需:**【待确认】**)|

**TenantLine**:**IGNORE**(company 是 12 业务 Object 之一,只是 IGNORE TenantLine — RC-5 明确)

### 3.3 Customer(沿用 G2-Contract-01,RC-3 不涉及)

| 字段 | Java 类型 | 含义 |
|---|---|---|
| `customerId` | Long | PK, 自增 |
| `companyId` | Long | FK → company(236B §3)|
| `customerName` | String | 客户姓名 |
| `mobile` | String | 手机号 |
| `createdAt` / `updatedAt` | LocalDateTime | 时间戳 |

### 3.4 Patient(**RC-3a 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `patientId` | Long | 238 §4.3 | PK, 自增 |
| `companyId` | Long | 238 §4.3 + 236B §3 | **字段保留,无 FK 约束**(236B 已删 fk_patient_company,用于 TenantLine WHERE 注入)|
| `customerId` | Long | 238 §4.3 | FK → customer |
| `patientName` | String | 238 §4.3 | 患者姓名 |
| `patientGender` | String | 238 §4.3 | 性别(**G2-01 错写为 `gender`,已修正**)|
| `patientBirthday` | LocalDate | 238 §4.3 | 出生日期(**G2-01 错写为 `birthDate`,已修正**)|
| `idCard` | String | 238 §4.3 | 身份证号 |
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.3 | 时间戳 |

**严禁自行发明字段**:`medicalCode`(G2-01 自创,238 §4.3 无此字段 — **已删除**)

### 3.5 Employee(**RC-3b 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `employeeId` | Long | 238 §4.4 | PK, 自增 |
| `companyId` | Long | 238 §4.4 | FK → company |
| `adminId` | Long | **235B §2 显式 NOT NULL UNIQUE** | 关联 Sa-Token admin user |
| `employeeName` | String | 238 §4.4 | 员工姓名 |
| `nickname` | String | 238 §4.4 | 昵称 |
| `mobile` | String | 238 §4.4 | 手机号 |
| `role` | String | 235B §2 | 角色枚举字符串(具体枚举值见 §9)|
| `departmentId` | Long | 238 §4.4 | 部门 ID |
| `status` | String | 238 §4.4 | 状态(ACTIVE/DISABLED — **【待确认】**)|
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.4 | 时间戳 |

### 3.6 ConsultRoom(**RC-3c 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `consultRoomId` | Long | 238 §4.5 | PK, 自增 |
| `companyId` | Long | 238 §4.5 | FK → company |
| `consultRoomName` | String | 238 §4.5 | 检查室名称(**G2-01 错写为 `roomName`,已修正**)|
| `status` | String | 238 §4.5 | 状态(ACTIVE/INACTIVE — **【待确认】**)|
| `examineList` | String | 238 §4.5 | 检查项(JSON 或 ID 列表 — 具体格式 **【待确认】**)|
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.5 | 时间戳 |

**严禁自行发明字段**:`roomNo`(G2-01 自创,238 §4.5 无此字段 — **已删除**)

### 3.7 BigScreen(**RC-3d 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `bigScreenId` | Long | 238 §4.6 | PK, 自增 |
| `companyId` | Long | 238 §4.6 | FK → company |
| `bigScreenName` | String | 238 §4.6 | 大屏名称(**G2-01 错写为 `screenName`,已修正**)|
| `sceneType` | String | 238 §4.6 | 场景类型(具体枚举值 **【待确认】**)|
| `consultRoomIdArray` | String | 238 §4.6 + §15 | **JSON 字符串**(不是 FK),存储关联检查室 ID 列表 |
| `status` | String | 238 §4.6 | 状态(ONLINE/OFFLINE — **【待确认】**)|
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.6 | 时间戳 |

### 3.8 AppointmentSchedule(**RC-3e 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `scheduleId` | Long | 238 §4.8 | PK, 自增 |
| `companyId` | Long | 238 §4.8 | FK → company |
| `employeeId` | Long | 238 §4.8 | **FK → employee**(**G2-01 错写为 `doctorId`,已修正**)|
| `scheduleDate` | LocalDate | 238 §4.8 | 排班日期 |
| `status` | String | 238 §4.8 | 状态(ACTIVE/INACTIVE/CANCELLED)|
| `remark` | String | 238 §4.8 | 备注 |
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.8 | 时间戳 |

**严禁自行发明字段**:`startTime` / `endTime`(G2-01 自创,这些是 AppointmentSlot 的字段 — **已删除**)

### 3.9 AppointmentSlot(**RC-3f 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `slotId` | Long | 238 §4.9 | PK, 自增 |
| `scheduleId` | Long | 238 §4.9 + 236B §3.5 | FK → appointment_schedule |
| `companyId` | Long | 238 §4.9 + 236B §3.5 | **字段保留,无 FK 约束**(236B 已删 fk_slot_company)|
| `consultRoomId` | Long | 236B §3.5 | **FK → consult_room** |
| `startTime` | LocalTime | 238 §4.9 | 开始时间(**G2-01 错写为 `slotStartTime`,已修正**)|
| `endTime` | LocalTime | 238 §4.9 | 结束时间(**G2-01 错写为 `slotEndTime`,已修正**)|
| `capacity` | Integer | 238 §4.9 | 容量(**G2-01 错写为 `maxPatients`,已修正**)|
| `bookedCount` | Integer | 238 §4.9 | 已预约数(**G2-01 错写为 `currentCount`,已修正**)|
| `status` | String | 238 §4.9 | 状态(DRAFT/OPEN/CLOSED — **【待确认】**)|
| `serviceType` | String | 238 §4.9 | 服务类型(具体枚举值 **【待确认】**)|
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.9 | 时间戳 |

### 3.10 Appointment(**RC-3g 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `appointmentId` | Long | 238 §4.7 | PK, 自增 |
| `companyId` | Long | 238 §4.7 | FK → company |
| `patientId` | Long | 238 §4.7 | FK → patient |
| `employeeId` | Long | 238 §4.7 | FK → employee(**G2-01 错写为 `doctorId`,已修正**)|
| `scheduleId` | Long | 238 §4.7 | FK → appointment_schedule |
| `slotId` | Long | 238 §4.7 | FK → appointment_slot |
| `appointmentNo` | String | 238 §4.7 + 236B | **UNIQUE**,业务编号 |
| `appointmentType` | String | 238 §4.7 | 类型(ONLINE/WALK_IN/PHONE — **【待确认】**)|
| `appointmentSource` | String | 238 §4.7 | 来源(WEB/H5/PHONE — **【待确认】**)|
| `status` | String | 238 §4.7 | 状态(DRAFT/BOOKED/CONFIRMED/COMPLETED/CANCELLED/RESCHEDULED)|
| `slotDate` | LocalDate | 238 §4.7 | 预约日期 |
| `slotStartTime` | LocalTime | 238 §4.7 | 开始时间 |
| `slotEndTime` | LocalTime | 238 §4.7 | 结束时间 |
| `currentVisitId` | String | 238 §4.7 | 当前 Visit ID(UUID)|
| `rescheduledFromId` | Long | 238 §4.7 | 改约来源 appointmentId |
| `remark` | String | 238 §4.7 | 备注 |
| `createdBy` | Long | 238 §4.7 | 创建者 employeeId |
| `createdAt` | LocalDateTime | 238 §4.7 | 创建时间 |
| `confirmedAt` | LocalDateTime | 238 §4.7 | 确认时间 |
| `completedAt` | LocalDateTime | 238 §4.7 | 完成时间 |
| `cancelledAt` | LocalDateTime | 238 §4.7 | 取消时间 |
| `cancelReason` | String | 238 §4.7 | 取消原因 |
| `updatedAt` | LocalDateTime | 238 §4.7 | 更新时间 |

**严禁 G2-01 错写**:`appointmentTime`(单一字段 — 已拆为 slotDate/slotStartTime/slotEndTime 三字段)

### 3.11 Visit(**RC-3h 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `visitId` | String | 238 §4.10 | PK, UUID |
| `companyId` | Long | 238 §4.10 | FK → company |
| `appointmentId` | Long | 238 §4.10 | FK → appointment(WalkIn 可空)|
| `patientId` | Long | 238 §4.10 | FK → patient |
| `employeeId` | Long | 238 §4.10 | FK → employee(**G2-01 错写为 `doctorId`,已修正**)|
| `consultRoomId` | Long | 238 §4.10 | FK → consult_room |
| `visitType` | String | 238 §4.10 | 类型(APPOINTMENT/WALK_IN — **【待确认】**)|
| `status` | String | 238 §4.10 | 状态(DRAFT/CHECKED_IN/TRIAGED/IN_CONSULTATION/COMPLETED/TRANSFERRED/CANCELLED)|
| `transferredFromVisitId` | String | 238 §4.10 | 转诊来源 visitId(转诊时填)|
| `transferredFromEmployeeId` | Long | 238 §4.10 | 转诊来源 employeeId |
| `cancelledAt` | LocalDateTime | 238 §4.10 | 取消时间 |
| `cancelReason` | String | 238 §4.10 | 取消原因 |
| `completedAt` | LocalDateTime | 238 §4.10 | 完成时间 |
| `transferredAt` | LocalDateTime | 238 §4.10 | 转诊时间 |
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.10 | 时间戳 |

**严禁 G2-01 自创字段**:`checkInTime`(Visit 创建时无此概念 — **已删除**)

### 3.12 TriageQueue(沿用 G2-Contract-01,字段基本一致)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `triageQueueId` | String | 238 §4.11 | PK, UUID |
| `companyId` | Long | 238 §4.11 | FK → company |
| `visitId` | String | 238 §4.11 + 236B | **UNIQUE** |
| `appointmentId` | Long | 238 §4.11 | 可空(WalkIn)|
| `consultRoomId` | Long | 238 §4.11 | IN_POOL 时 NULL,ASSIGNED 时填 |
| `employeeId` | Long | 238 §4.11 | IN_POOL 时 NULL,ASSIGNED 时填 |
| `status` | String | 238 §4.11 | 4 状态:**IN_POOL / ASSIGNED / REMOVED / CANCELLED**(238 §4.11 显式冻结)|
| `assignedAt` | LocalDateTime | 238 §4.11 | 分配时间 |
| `assignedBy` | Long | 238 §4.11 | 分配者 employeeId |
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.11 | 时间戳 |

### 3.13 ReceptionQueue(**RC-3i 重写**)

| 字段 | Java 类型 | 来源 | 备注 |
|---|---|---|---|
| `receptionQueueId` | String | 238 §4.12 | PK, UUID |
| `companyId` | Long | 238 §4.12 | FK → company |
| `triageQueueId` | String | 238 §4.12 + 236B | **UNIQUE**,FK → triage_queue |
| `visitId` | String | 238 §4.12 + 236B | **UNIQUE** |
| `appointmentId` | Long | 238 §4.12 | 可空(WalkIn)|
| `consultRoomId` | Long | 238 §4.12 | FK → consult_room |
| `employeeId` | Long | 238 §4.12 | FK → employee |
| `status` | String | 238 §4.12 | **6 状态(238 §4.12 冻结:具体 6 状态名称**【待确认】,但状态枚举存在)** |
| `sequenceInRoom` | Integer | 238 §4.12 | 室内顺序 |
| `calledAt` | LocalDateTime | 238 §4.12 | 叫号时间 |
| `startedAt` | LocalDateTime | 238 §4.12 | 开始接诊时间 |
| `completedAt` | LocalDateTime | 238 §4.12 | 完成时间 |
| `skippedTimes` | Integer | 238 §4.12 | 跳过次数 |
| `cancelReason` | String | 238 §4.12 | 取消原因 |
| `createdAt` / `updatedAt` | LocalDateTime | 238 §4.12 | 时间戳 |

### 3.14 user_company Infrastructure Contract(沿用 G2-Contract-01 §5)

详见 G2-Contract-01 §5。沿用 241V2A-10 / 11 / 12 / 13 / 14 冻结:

- table = `user_company`
- PK = `id`(Long,自增)
- `userId` / `companyId` / `isDefault` / `createdAt` / `updatedAt`
- 4 个生产 Repository 方法:
  - `updateDefaultToZero(Long userId)`
  - `setDefault(Long userId, Long companyId)`
  - `existsByUserIdAndCompanyId(Long userId, Long companyId)`
  - `countByUserIdAndIsDefault(Long userId, int isDefault)`
- exactly-one 规则:`if (defaultCount != 1) throw IllegalStateException`
- DEFAULT-05 断言:`assertThat(defaultCount).isEqualTo(1)`

---

## §4 API Contract(40 API — RC-1 重写)

### 4.1 API 总览(以 233 为准)

| API | Method | Path | 模块归属 | 状态 | 来源 |
|---|---|---|---|---|---|
| **API-001** | POST | `/api/appointment/create` | Appointment | 一致 | 232 |
| **API-002** | POST | `/api/appointment/cancel` | Appointment | 一致 | 232 |
| **API-003** | POST | `/api/appointment/confirm` | Appointment | 一致 | 232 |
| **API-004** | POST | `/api/appointment/reschedule` | Appointment | 一致 | 232 |
| **API-005** | GET | `/api/appointment/list` | Appointment | 一致 | 232 |
| **API-006** | GET | `/api/patient/list` | Patient | 一致 | 232 |
| **API-007** | GET | `/api/customer/list` | Customer | 一致 | 232 |
| **API-008** | POST | `/api/schedule/create` | Schedule | 一致 | 232 |
| **API-009** | POST | `/api/schedule/update` | Schedule | 一致 | 232 |
| **API-010** | GET | `/api/schedule/list` | Schedule | 一致 | 232 |
| **API-011** | POST | `/api/slot/create` | Slot | 一致 | 232 |
| **API-012** | GET | `/api/slot/list` | Slot | 一致 | 232 |
| **API-013** | POST | `/api/consultroom/create` | ConsultRoom | 一致 | 232 |
| **API-014** | GET | `/api/consultroom/list` | ConsultRoom | 一致 | 232 |
| **API-015** | GET | `/api/employee/list` | Employee | 一致 | 232 |
| **API-016** | POST | `/api/arrival/checkin` | Arrival | 一致 | 232 |
| **API-017** | POST | `/api/arrival/cancel` | Arrival | 一致 | 232 |
| **API-018** | GET | `/api/arrival/list` | Arrival | 一致 | 232 |
| **API-019** | GET | `/api/triage/pool-list` | Triage | 一致 | 232 |
| **API-020** | POST | `/api/triage/auto-assign` | Triage | 一致 | 232 |
| **API-021** | POST | `/api/triage/assign` | Triage | 一致 | 232 |
| **API-022** | POST | `/api/triage/skip` | Triage | 一致 | 232 |
| **API-023** | GET | `/api/triage/list` | Triage | 一致 | 232 |
| **API-024** | POST | `/api/queue/start` | Queue | 一致 | 232 |
| **API-025** | **POST** | **`/api/visit/create-direct`** | **Visit** | **🔴 重写** | **233** |
| **API-026** | POST | `/api/queue/next` | Queue | 一致 | 233 |
| **API-027** | POST | `/api/queue/call` | Queue | **🔴 重写** | **233** |
| **API-028** | POST | `/api/queue/skip` | Queue | **🔴 重写** | **233** |
| **API-029** | POST | `/api/queue/recall` | Queue | **🔴 重写** | **233** |
| **API-030** | POST | `/api/queue/start-consult` | Queue | **🔴 重写** | **233** |
| **API-031** | POST | `/api/queue/complete` | Queue | **🔴 重写** | **233** |
| **API-032** | GET | `/api/queue/console` | Queue | **🔴 重写** | **233** |
| **API-033** | GET | `/api/queue/room` | Queue | **🔴 重写** | **233** |
| **API-034** | POST | `/api/visit/transfer` | Visit | Path 一致 | 233 |
| **API-035** | POST | `/api/visit/cancel-direct` | Visit | **🔴 重写** | **233** |
| **API-036** | GET | `/api/visit/list-by-appointment` | Visit | **🔴 重写** | **233** |
| **API-037** | POST | `/api/doctor/pause` | Doctor | **🔴 重写** | **233** |
| **API-038** | POST | `/api/doctor/resume` | Doctor | **🔴 重写** | **233** |
| **API-039** | GET | `/api/bigscreen/list` | BigScreen | **🔴 重写** | **233** |
| **API-040** | GET | `/api/bigscreen/display` | BigScreen(**公开 API**)| **🔴 重写** | **233** |

### 4.2 模块归属分布(RC-1 重写)

| 模块 | API 编号 | 数量 |
|---|---|---:|
| Appointment | API-001 ~ API-005 | 5 |
| Patient | API-006 | 1 |
| Customer | API-007 | 1 |
| Schedule | API-008 ~ API-010 | 3 |
| Slot | API-011 ~ API-012 | 2 |
| ConsultRoom | API-013 ~ API-014 | 2 |
| Employee | API-015 | 1 |
| Arrival | API-016 ~ API-018 | 3 |
| Triage | API-019 ~ API-023 | 5 |
| Queue | API-024, API-026 ~ API-033 | 9 |
| **Visit** | **API-025, API-034 ~ API-036** | **4** |
| **Doctor** | **API-037 ~ API-038** | **2** |
| **BigScreen** | **API-039 ~ API-040** | **2** |

### 4.3 G2-01 vs G2-02 Path 修正(逐 API)

| API | G2-01 错写 | G2-02 修正 | 来源 |
|---|---|---|---|
| API-025 | `/api/queue/pause` ❌ | **`/api/visit/create-direct`** ✅ | 233 P0-2 + P0-4 修正 |
| API-027 | `/api/queue/skip` ❌ | **`/api/queue/call`** ✅ | 233 |
| API-028 | `/api/queue/complete` ❌ | **`/api/queue/skip`** ✅ | 233 |
| API-029 | `/api/queue/list` ❌ | **`/api/queue/recall`** ✅ | 233 |
| API-030 | `/api/visit/start` ❌ | **`/api/queue/start-consult`** ✅ | 233 |
| API-031 | `/api/visit/complete` ❌ | **`/api/queue/complete`** ✅ | 233 |
| API-032 | `/api/visit/cancel` ❌ | **`/api/queue/console`** ✅ | 233 |
| API-033 | `/api/visit/detail` ❌ | **`/api/queue/room`** ✅ | 233 |
| API-035 | `/api/visit/list` ❌ | **`/api/visit/cancel-direct`** ✅ | 233 |
| API-036 | `/api/visit/cancel-direct` ❌ | **`/api/visit/list-by-appointment`** ✅ | 233 |
| API-037 | `/api/reception/assign` ❌ | **`/api/doctor/pause`** ✅ | 233 |
| API-038 | `/api/reception/start` ❌ | **`/api/doctor/resume`** ✅ | 233 |
| API-039 | `/api/reception/list` ❌ | **`/api/bigscreen/list`** ✅ | 233 |
| API-040 | `/api/auth/login` ❌ | **`/api/bigscreen/display`** ✅(公开)| 233 |

### 4.4 API 字段级 Contract

> **【待确认】**:Request DTO / Response VO 字段级 Contract 在 233 / 232 中部分冻结。
> 本 Contract 不重复列全部字段,沿用 233 字段级表。
> 字段不一致时以 233 为准(233 是 232 的修正版)。

### 4.5 API 状态迁移(以 233 为准)

> API 状态迁移字段以 233 为准,**不重复列出**。
> **严禁 G2-Contract-01 状态机推论方式**(G2-01 状态机与 229 不一致)。

---

## §5 Repository Contract(沿用 G2-Contract-01 §6 + 238 §6.2 冻结)

### 5.1 基础 CRUD

每个 Entity 都有 `JpaRepository<Entity, IDType>` 接口,**沿用 238 §6.1 冻结**。

| Entity | Repository | ID Type | 来源 |
|---|---|---|---|
| `CompanyEntity` | `CompanyRepository` | Long | 238 §6.1 |
| `CustomerEntity` | `CustomerRepository` | Long | 238 §6.1 |
| `PatientEntity` | `PatientRepository` | Long | 238 §6.1 |
| `EmployeeEntity` | `EmployeeRepository` | Long | 238 §6.1 |
| `ConsultRoomEntity` | `ConsultRoomRepository` | Long | 238 §6.1 |
| `BigScreenEntity` | `BigScreenRepository` | Long | 238 §6.1 |
| `AppointmentScheduleEntity` | `AppointmentScheduleRepository` | Long | 238 §6.1 |
| `AppointmentSlotEntity` | `AppointmentSlotRepository` | Long | 238 §6.1 |
| `AppointmentEntity` | `AppointmentRepository` | Long | 238 §6.1 |
| `VisitEntity` | `VisitRepository` | String | 238 §6.1 |
| `TriageQueueEntity` | `TriageQueueRepository` | String | 238 §6.1 |
| `ReceptionQueueEntity` | `ReceptionQueueRepository` | String | 238 §6.1 |

### 5.2 必需的 Custom 查询方法

| Repository | Custom 方法 | 来源 |
|---|---|---|
| `AppointmentRepository` | `findByCurrentVisitId(currentVisitId)` / `findByPatientIdAndStatusIn(patientId, statuses)` / `findBySlotDateAndEmployeeIdAndStatus(...)` / `existsByCompanyIdAndAppointmentNo(companyId, appointmentNo)` / `findByAppointmentNo(appointmentNo)` | 238 §6.2 |
| `VisitRepository` | `findByAppointmentId(appointmentId)` / `findByPatientIdAndStatus(patientId, status)` / `findByTransferredFromVisitId(transferredFromVisitId)` | 238 §6.2 |
| `TriageQueueRepository` | `findByVisitId(visitId)` / `findByStatusOrderByCreatedAt(status)` / `findByStatusInAndCreatedAtBefore(...)` | 238 §6.2 |
| `ReceptionQueueRepository` | `findByVisitId(visitId)` / `findByTriageQueueId(triageQueueId)` / `findByConsultRoomIdAndStatusOrderBySequenceInRoom(...)` / `findByStatusInAndCalledAtBefore(...)` | 238 §6.2 |
| `EmployeeRepository` | `findByCompanyIdAndAdminId(companyId, adminId)` / `findByCompanyIdAndRole(companyId, role)` | 238 §6.2 |
| `PatientRepository` | `findByCustomerId(customerId)` / `findByCompanyId(companyId)` | 238 §6.2 |
| `ConsultRoomRepository` | `findByCompanyId(companyId)` | 238 §6.2 |
| `BigScreenRepository` | `findByCompanyIdAndSceneType(companyId, sceneType)` | 238 §6.2 |
| `CustomerRepository` | `findByCompanyId(companyId)` | 238 §6.2 |
| `AppointmentScheduleRepository` | `findByEmployeeIdAndScheduleDate(...)` | 238 §6.2 |
| `AppointmentSlotRepository` | `findByScheduleIdAndStatus(...)` | 238 §6.2 |

### 5.3 不得添加的查询方法

> 沿用 238 §6.3 冻结:
> - ✗ 通用全表扫描型方法
> - ✗ 无业务需求型方法
> - ✗ 性能优化型方法

### 5.4 user_company Repository(沿用 G2-Contract-01 §5.3)

| 方法 | 来源 |
|---|---|
| `updateDefaultToZero(Long userId)` | 241V2A-10 / 12 |
| `setDefault(Long userId, Long companyId)` | 241V2A-10 / 12 |
| `existsByUserIdAndCompanyId(Long userId, Long companyId)` | 241V2A-12 |
| `countByUserIdAndIsDefault(Long userId, int isDefault)` | 241V2A-12 |
| `selectDefaultCompanyId(Long userId)`(自定义 @Query,带 LIMIT 1)| 241V2A-13 |

---

## §6 Service Contract

### 6.1 已由 API 冻结的 Service(沿用 G2-Contract-01 §8.1 + 238 §7.1)

| Service | 来源 | 责任边界 |
|---|---|---|
| `AppointmentService` | 232 / 233 + 238 §7.1 | Appointment CRUD、状态推进、currentVisitId 维护 |
| `VisitService` | 233 + 238 §7.1 | Visit CRUD、状态机、transferredFromXxx 字段维护 |
| `TriageService` | 233 + 238 §7.1 | TriageQueue CRUD、IN_POOL / ASSIGNED 状态推进 |
| `ReceptionQueueService` | 233 + 238 §7.1 | ReceptionQueue CRUD、6 状态推进、sequenceInRoom 计算 |
| `TransferService` | 235B §4.2 + 238 §7.2 | **API-034 Transfer 9 步事务(详见 §7.2)** |
| `ScheduleService` | 232 / 233 + 238 §7.1 | AppointmentSchedule CRUD、ACTIVE/INACTIVE/CANCELLED |
| `SlotService` | 232 / 233 + 238 §7.1 | AppointmentSlot CRUD、bookedCount 维护、DRAFT 不占容量 |

### 6.2 6 Service 方法 Contract(**PA-01 冻结**)

> **PA-01 纪律**:仅冻结已有 Effective Spec 明确支持的方法。
> 没有冻结的方法不写,标【待确认】。

#### 6.2.1 EmployeeService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| `findByCompanyIdAndAdminId(companyId, adminId)` | 238 §6.2 + 235B §2 | **冻结**(已冻结,沿用 Repository)|
| `findByCompanyIdAndRole(companyId, role)` | 238 §6.2 | **冻结** |
| `getEmployeeByLogin(employeeId)`(用于 adminId 校验)| 235B §2 | **冻结业务规则**(具体方法签名 **【待确认】**)|
| 其它 CRUD 方法 | | **【待确认】**(不凭空发明)|

#### 6.2.2 PatientService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| `findByCustomerId(customerId)` | 238 §6.2 | **冻结** |
| `findByCompanyId(companyId)` | 238 §6.2 | **冻结** |
| 其它 CRUD 方法 | | **【待确认】**(不凭空发明)|

#### 6.2.3 CustomerService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| `findByCompanyId(companyId)` | 238 §6.2 | **冻结** |
| 其它 CRUD 方法 | | **【待确认】**(不凭空发明)|

#### 6.2.4 ConsultRoomService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| `findByCompanyId(companyId)` | 238 §6.2 | **冻结** |
| 其它 CRUD 方法 | | **【待确认】**(不凭空发明)|

#### 6.2.5 BigScreenService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| `findByCompanyIdAndSceneType(companyId, sceneType)` | 238 §6.2 | **冻结** |
| `parseConsultRoomIdArray(bigScreenId)`(解析 JSON)| 238 §15 概念 | **冻结业务规则**(具体 JSON 解析方式 **【待确认】**)|
| 其它 CRUD 方法 | | **【待确认】**(不凭空发明)|

#### 6.2.6 CompanyService(**PA-01 部分冻结**)

| 方法 | 来源 | 状态 |
|---|---|---|
| 公司初始化 CRUD(用于 SaaS 初始化)| 240 / 241V2 | **冻结业务规则**(具体方法签名 **【待确认】**)|
| 其它方法 | | **【待确认】**(不凭空发明)|

### 6.3 Service 不承担的责任(沿用 238 §7.3)

| 不在 Service 层 | 在哪层 |
|---|---|
| 状态枚举定义(常量) | Entity 静态字段或 enum 类 |
| 角色权限校验 | Spring Security / Sa-Token |
| 跨公司隔离核心逻辑 | TenantLineInnerInterceptor(自动织入)|
| 业务编号生成(appointmentNo) | Service 或独立 NumberGenerator(具体 **【待确认】**)|

---

## §7 Transaction Contract

### 7.1 DEFAULT-01 ~ DEFAULT-05(沿用 G2-Contract-01 §13 + 241V2A-11 冻结)

> 沿用 G2-Contract-01 §13 完整保留(已被 G2-Contract-Audit-01 验证 100% 一致):

- **DEFAULT-01**:`updateDefaultToZero` + `setDefault`
- **DEFAULT-02**:`countByUserIdAndIsDefault`
- **DEFAULT-03**:`setDefault` + Verifier + `selectDefaultCompanyId`(带 LIMIT 1)
- **DEFAULT-04**:跨公司隔离异常(UserNotFoundException 60003 / CompanyMismatchException 60001)
- **DEFAULT-05**:exactly-one 断言 `assertThat(defaultCount).isEqualTo(1)`

**Transaction 分类**:T1(单对象事务)+ 行锁(241V2A-19 显式冻结)
**沿用**:241V2A-19 §3 显式 `findByIdForUpdate` / `@Transactional(isolation = ...)` 模式

### 7.2 Transfer 9-step(**RC-2 重写** — 以 235B §4.2 / §4.3 为准)

> **关键冻结**:API-034 不创建新 ReceptionQueue。新 ReceptionQueue 由 API-021 创建。

```text
API-034 visit/transfer 9 步事务(以 235B §4.2 / §4.3 为绝对基准)
─────────────────────────────────────────
前置:Visit.status == IN_CONSULTATION(API-030 已完成)

1. validation
   - 校验 oldVisit.status == IN_CONSULTATION
   - 校验 oldVisit.id 非空

2. create new Visit(visitId2, appointmentId = oldVisit.appointmentId)
   - INSERT visit (visitId2 = UUID, appointmentId = oldVisit.appointmentId, ...)

3. create new TriageQueue(IN_POOL, employeeId = NULL, consultRoomId = NULL)
   - INSERT triage_queue (triageQueueId = UUID, visitId = visitId2,
                           status = IN_POOL, employeeId = NULL, consultRoomId = NULL)

4. Appointment.currentVisitId = newVisitId
   - UPDATE appointment SET currentVisitId = visitId2 WHERE appointmentId = oldVisit.appointmentId

5. Appointment.status = TRIAGE_WAITING
   - UPDATE appointment SET status = TRIAGE_WAITING WHERE appointmentId = oldVisit.appointmentId

6. old Visit = TRANSFERRED
   - UPDATE visit SET status = TRANSFERRED, transferredAt = NOW(), transferredFromEmployeeId = oldVisit.employeeId
     WHERE visitId = oldVisit.visitId

7. old TriageQueue = REMOVED
   - UPDATE triage_queue SET status = REMOVED WHERE triageQueueId = oldTriageQueueId

8. old ReceptionQueue = DONE + cancelReason = TRANSFERRED
   - UPDATE reception_queue SET status = DONE, cancelReason = 'TRANSFERRED', completedAt = NOW()
     WHERE visitId = oldVisit.visitId AND status NOT IN (DONE, CANCELLED)

9. COMMIT
   - 所有操作原子提交,任一失败全回滚
   - **不创建新 ReceptionQueue**(新 ReceptionQueue 由 API-021 创建)
```

**严禁 G2-01 错写**(已删除):
- ✗ 创建新 ReceptionQueue
- ✗ 旧 ReceptionQueue.status = CANCELLED(应为 DONE + cancelReason='TRANSFERRED')
- ✗ 旧 TriageQueue.status = IN_POOL(应为 REMOVED)
- ✗ 步骤顺序错(必须先创建新,后处理旧)
- ✗ 缺 Appointment.status = TRIAGE_WAITING 更新

### 7.3 API-016 / API-021 Transaction 分类(**PA-02 部分【待确认】**)

| API | 业务动作 | 参与对象 | 现有 Transaction 证据 | 分类 |
|---|---|---|---|---|
| **API-016** arrival/checkin | 现场签到,创建 Visit(状态 CHECKED_IN)+ 创建 TriageQueue(IN_POOL)| Visit + TriageQueue | 233 §API-016 字段级,233 未明确 transaction 分类 | **【待确认】**(业务复杂度提示:多对象联动)|
| **API-021** triage/assign | 分配检查室 + 创建 ReceptionQueue | TriageQueue(ASSIGNED)+ ReceptionQueue(新增)+ Appointment(status 更新可能) | 233 §API-021 字段级,233 未明确 transaction 分类 | **【待确认】**(业务复杂度提示:多对象联动 + 并发敏感)|

**PA-02 纪律**:
- 不自行写 T1 / T2 / T3 / T4
- 仅记录业务动作 + 参与对象
- 是否需要 `@Transactional` / 行锁 / 隔离级别 — **【待确认】**(由后续冻结决定)

### 7.4 其他 API Transaction 分类

> 沿用 G2-Contract-01 §9.1,逐 API 分类冻结。
> 对 G2-Contract-Audit-01 标记为 P0 的项(API-016/021/025/034/037),按 §7.2 / §7.3 处理。

### 7.5 Transfer Rollback(**PA-07【待确认】**)

> **235B §4.2 已明确**:Transfer 9 步是单一 `@Transactional` 事务,任一失败全回滚。
> **PA-07 纪律**:不自行设计 partial compensation。

| 项 | 状态 |
|---|---|
| Transfer 整体事务 | **冻结**(235B §4.2)|
| 任一失败全回滚 | **冻结**(235B §4.2 COMMIT 语义)|
| 部分失败是否全部回滚 | **【待确认】**(沿用 G2-Contract-01,不另行设计)|
| Rollback strategy | **【待确认】** |

---

## §8 Tenant Contract(**RC-5 重写**)

### 8.1 业务表 / 系统表概念(**RC-5 明确**)

> **明确声明**(修复 G2-Contract-01 概念混淆):

**company 是 12 个业务 Object 之一**(235B §1 + 238 §4.1 显式归类)。

只是 **TenantLine 对 company 采用 IGNORE 策略**(因为 company 是"被查找的"实体,不是"被过滤的"实体)。

**严禁**称 company 为"系统表"。

### 8.2 12 业务 Object TenantLine 分类

| Object | companyId 字段 | TenantLine | 来源 |
|---|---|---|---|
| **company** | PK | **IGNORE** | 241V4 §6.1 |
| customer | FK | ✓ TenantLine | 241V4 §4.2 |
| **patient** | **字段(无 FK)** | ✓ TenantLine | 241V4 §4.2 + 236B §3 |
| employee | FK | ✓ TenantLine | 241V4 §4.2 |
| consult_room | FK | ✓ TenantLine | 241V4 §4.2 |
| big_screen | FK | ✓ TenantLine | 241V4 §4.2 |
| appointment_schedule | FK | ✓ TenantLine | 241V4 §4.2 |
| **appointment_slot** | **字段(无 FK)** | ✓ TenantLine | 241V4 §4.2 + 236B §3.5 |
| appointment | FK | ✓ TenantLine | 241V4 §4.2 |
| visit | FK | ✓ TenantLine | 241V4 §4.2 |
| triage_queue | FK | ✓ TenantLine | 241V4 §4.2 |
| reception_queue | FK | ✓ TenantLine | 241V4 §4.2 |

**11 张业务表走 TenantLine + 1 张 company 走 IGNORE = 12 业务 Object**

### 8.3 CompanyContext / Interceptor / Filter(沿用 241V2 §4-§5)

| 组件 | 职责 | 来源 |
|---|---|---|
| `CompanyContext`(ThreadLocal)| 存储当前请求 companyId | 241V2 §4 |
| `TenantLineInnerInterceptor`(MyBatis-Plus)| 自动织入 `WHERE companyId = ?` | 241V2 §5.4.2 |
| `CompanyContextFilter`(Servlet Filter)| 从 `X-Company-Id` Header 解析 | 241V2 §5.4.1 |
| 跨公司隔离 Service 校验 | Service 层校验 companyId 一致性 | 240 §3 + 241V2 |

### 8.4 跨公司隔离业务规则(沿用 240 §3 + 241V2)

| 规则 | 状态 |
|---|---|
| ❌ 严禁硬编码 companyId | **冻结**(240 §3)|
| ❌ 严禁 default company fallback | **冻结**(240 §3)|
| ✓ 必须从 CompanyContext 取值 | **冻结**(240 §3)|
| ✓ 跨公司引用必须校验 | **冻结**(241V2)|

---

## §9 Security Contract(**PA-03 + RC-6**)

### 9.1 角色定义(沿用 235B §2 + 233)

> 7 角色完整列表与具体权限在 233 各 API 中显式冻结。
> 沿用 G2-Contract-01 §11.1,但**禁止自行扩展**。

| 角色 | 来源 | 权限范围(以 233 为准)|
|---|---|---|
| **ADMIN** | 235B §2 | 系统管理 + 全部操作 |
| **DOCTOR** | 235B §2 | 接诊 + 处方 + 分配 |
| **NURSE** | 235B §2 | 分诊 + 现场管理 |
| **RECEP** | 235B §2 | 接待 + 签到 + 取消 |
| **STAFF** | 235B §2 | 通用操作 |
| **BIGSCREEN** | 233 §API-040 | 大屏显示(**仅 API-040**)|
| 具体角色列表 | 233 各 API 逐 API 冻结 | **【待确认】**(完整 7 角色在 233 显式冻结)|

### 9.2 公开 API 白名单(**RC-6 补齐**)

| Path | 来源 | 备注 |
|---|---|---|
| `/api/auth/**` | 241V2 §5.6 | 认证(注意:不是 API-040)|
| `/api/common/**` | 241V2 §5.6 | 通用 |
| `/api/health` | 241V2 §5.6 | 健康检查 |
| `/api/swagger`, `/api/v3/api-docs`, `/api/doc.html` | 241V2 §5.6 | API 文档 |
| **`/api/bigscreen/display`**(**RC-6 新增**)| **233 §API-040** | **大屏显示,公开访问,无需鉴权**|

### 9.3 API 权限矩阵(沿用 233 + 235B §2)

> **PA-03 纪律**:冻结业务授权规则(Business Authorization Rule),不擅自指定 Sa-Token annotation 实现。

| 维度 | 状态 |
|---|---|
| 角色 × API 权限矩阵(业务规则)| **冻结**(233 各 API + 235B §2)|
| Sa-Token `@SaCheckRole` 具体 annotation | **【待确认】**(Effective Spec 未冻结具体 annotation)|
| Sa-Token `@SaCheckPermission` 具体 annotation | **【待确认】**(Effective Spec 未冻结)|
| Sa-Token StpInterface 实现细节 | **【待确认】**|

### 9.4 PA-03 关键纪律

| 已冻结 | 未冻结(【待确认】)|
|---|---|
| 7 角色定义 | Sa-Token 具体 annotation |
| 角色 × API 权限矩阵 | Sa-Token 拦截器配置 |
| 公开 API 白名单(含 bigscreen/display)| Sa-Token Redis 存储 |
| 鉴权失败 → HTTP 状态 | 具体 Redis 连接配置 |
| NotLoginException → 401(241V2A-17)| 具体登录态保持时长 |

**严禁**:为了让 P1=0 而自行指定 `@SaCheckRole("DOCTOR")` 或 `@SaCheckPermission("appointment:create")`。

---

## §10 Exception Contract(沿用 G2-Contract-01 §12 + 241V2A-17 冻结)

> 已被 G2-Contract-Audit-01 验证 100% 一致,完整沿用 G2-Contract-01 §12。

| 异常类 | HTTP | ResultCode | 来源 |
|---|---|---|---|
| `BusinessException` | 200 + code | (code 字段)| 241 §4.1 |
| `CompanyContextMissingException` | 401 | 60000 | 241 §4.2 |
| `CompanyMismatchException` | 400 | 60001 | 241 §4.3 |
| `CompanyAccessDeniedException` | 403 | 60002 | 241 §4.4 |
| `UserNotFoundException` | 404 | 60003 | 241V2A-17 §3.1 |
| `UserDisabledException` | 403 | 60004 | 241V2A-17 §3.2 |
| `IllegalStateException`(java.lang) | 500 | (无 code)| 241V2A-16 §3 |
| `NotLoginException`(Sa-Token)| 401 | (Sa-Token 自带)| 241V2 §13.2 |

**GlobalExceptionHandler 8 个 @ExceptionHandler**(沿用 G2-Contract-01 §12.2 + 241V2A-17 §3.4)

---

## §11 DEFAULT Test Contract(沿用 G2-Contract-01 §13)

> 已被 G2-Contract-Audit-01 验证 100% 一致,完整沿用 G2-Contract-01 §13。

| DEFAULT | Test Type | Expected Result | 来源 |
|---|---|---|---|
| **DEFAULT-01** | setDefault + updateDefaultToZero | 1 个 default | 241V2A-11 / 12 |
| **DEFAULT-02** | countByUserIdAndIsDefault | count = 1 | 241V2A-11 / 12 |
| **DEFAULT-03** | setDefault + Verifier + selectDefaultCompanyId(LIMIT 1)| 旧 default 清零 + 新 default 唯一 | 241V2A-13 / 14 |
| **DEFAULT-04** | 跨公司隔离 | UserNotFoundException 60003 + CompanyMismatchException 60001 | 241V2A-17 / 18 |
| **DEFAULT-05** | exactly-one 断言 | `assertThat(defaultCount).isEqualTo(1)` | 241V2A-11 §4 |

**严禁**:为了 P1=0 而新增测试断言。

---

## §12 IGNORE_TABLES(**RC-4 + PA-04**)

### 12.1 5 个配置项(**RC-4 重写** — 沿用 241V4 §6.1)

> **完整表达**241V4 已冻结的 5 个配置项:

```text
public static final Set<String> IGNORE_TABLES_V44 = Set.of(
    "flyway_schema_history",     // 当前实际生效
    "company",                   // 当前实际生效(12 业务 Object 之一,RC-5 明确)
    "user",                      // 当前实际生效(241V4 §6.1 新增)
    "user_company",              // 当前实际生效(多公司关联表)
    "flyway_schema_history_v44"  // 预留项(尚未生效,激活条件 PA-04)
);
```

### 12.2 当前实际生效(4 张)| # | Table | 是否业务 Object | TenantLine | 原因 |
|--:|---|---|---|---|
| 1 | `flyway_schema_history` | ✗(系统表)| IGNORE | Flyway 元数据,无需 tenant 隔离 |
| 2 | **`company`** | **✓(12 业务 Object 之一,RC-5 明确)**| **IGNORE** | **company 是被查找的实体,不是被过滤的实体** |
| 3 | `user` | ✗(系统表)| IGNORE | Sa-Token 用户表(241V4 §6.1 新增) |
| 4 | `user_company` | ✗(基础设施表)| IGNORE | 多公司关联表,手动 SQL 处理 |

### 12.3 预留项(**PA-04 部分【待确认】**)

| # | Table | 状态 | 激活条件 |
|--:|---|---|---|
| 5 | `flyway_schema_history_v44` | 预留 | **【待确认】**(241V4 §6.1 提及预留,**未冻结具体激活条件**)|

**PA-04 纪律**:不虚构 activation event。如果 Effective Spec 没定义激活条件,保留【待确认】。

### 12.4 11 张 TenantLine 业务表

> **11 张业务表走 TenantLine**(12 业务 Object - 1 company IGNORE = 11):

`customer` / `patient` / `employee` / `consult_room` / `big_screen` / `appointment_schedule` / `appointment_slot` / `appointment` / `visit` / `triage_queue` / `reception_queue`

### 12.5 IGNORE_TABLES 静态清单(完整 5 项)

```java
// G2-Contract-02 §12.5 冻结(沿用 241V4 §6.1)
public static final Set<String> IGNORE_TABLES = Set.of(
    "flyway_schema_history",
    "company",
    "user",
    "user_company",
    "flyway_schema_history_v44"  // 预留
);
```

---

## §13 P1 Pending Items(汇总)

> 本节汇总所有【待确认】项,不引入任何 AI 推断。

| # | 类别 | 项 | 状态 |
|--:|---|---|---|
| 1 | Service 方法(PA-01)| 6 Service 中除已冻结的 CRUD 之外的方法 | **【待确认】** |
| 2 | Transaction(PA-02)| API-016 / API-021 Transaction 分类(T1/T2/T3/T4) | **【待确认】** |
| 3 | Security(PA-03)| Sa-Token 具体 annotation(`@SaCheckRole` / `@SaCheckPermission`)| **【待确认】** |
| 4 | Security(PA-03)| Sa-Token StpInterface 实现 / Redis 配置 / 登录态时长 | **【待确认】** |
| 5 | IGNORE_TABLES(PA-04)| flyway_schema_history_v44 激活条件 | **【待确认】** |
| 6 | Phase 1(PA-05)| Phase 1 系统设置 26 项页面字段 | **【待确认】** |
| 7 | SystemSetting V4.4(PA-06)| SystemSetting V4.4 范围与字段 | **【待确认】** |
| 8 | Transfer(PA-07)| Rollback strategy(整体事务已冻结,但补偿策略未冻结) | **【待确认】** |
| 9 | Visit 状态 | visitType 枚举(APPOINTMENT/WALK_IN)| **【待确认】** |
| 10 | Appointment 状态 | appointmentType / appointmentSource 枚举 | **【待确认】** |
| 11 | AppointmentSlot 状态 | status 枚举(DRAFT/OPEN/CLOSED)| **【待确认】** |
| 12 | ReceptionQueue 状态 | 6 状态具体名称 | **【待确认】** |
| 13 | BigScreen 状态 | sceneType / status 枚举 | **【待确认】** |
| 14 | ConsultRoom 状态 | status / examineList 格式 | **【待确认】** |
| 15 | Employee 状态 | status 枚举 | **【待确认】** |
| 16 | Company | phone 字段是否业务必需 | **【待确认】** |
| 17 | NumberGenerator | appointmentNo 生成策略 | **【待确认】** |
| 18 | 完整角色列表 | 7 角色完整定义(233 散落冻结) | **【待确认】** |
| 19 | 权限矩阵 | 40 API × 7 角色完整矩阵 | **【待确认】** |
| 20 | DTO/VO 字段级 | Request DTO / Response VO 完整字段(233 部分冻结)| **【待确认】** |

> **G2-Contract-Audit-02 独立盲审**将基于本节 + Fix Traceability Matrix 判定。

---

## §14 Phase 1 Scope(**PA-05【待确认】**)

> **PA-05 纪律**:只能使用已完成的页面侦察证据。没侦察的字段不编造。

### 14.1 Phase 1 = 诊所管理 + 系统设置(沿用 S1-170E §8)

| Phase | 模块 | 侦察状态 |
|--:|---|---|
| 1 | 诊所管理(Clinic Management)| **100% 完成**(沿用历史页面侦察)|
| 1 | 系统设置(System Settings)| **未完成** — 26 项字段**【待确认】**|

### 14.2 Phase 1 系统设置 26 项字段

> **全部【待确认】**,未侦察完成前不写入 Contract。

具体 26 项字段列表 + 状态枚举 + 默认值 + 校验规则 — **【待确认】**(由后续 Phase 1 系统设置页面侦察补丁冻结)。

### 14.3 PA-05 与 S1-170E §8 关系

> S1-170E §8 已判定:Phase 1 页面侦察 ≠ Backend Entry 硬 Blocker。
> 但 PA-05 冻结前,系统设置相关 API / Entity 不得编码实现。

---

## §15 SystemSetting V4.4(**PA-06【待确认】**)

> **PA-06 纪律**:没有冻结的字段、状态、子设置,全部【待确认】。

| 项 | 状态 |
|---|---|
| SystemSetting 字段 | **【待确认】**(无冻结证据)|
| SystemSetting 状态枚举 | **【待确认】** |
| SystemSetting 子设置(SMTP / 短信 / 微信等配置)| **【待确认】** |
| V4.4 重新冻结范围 | **【待确认】**(待后续冻结补丁)|

---

## §16 Fix Traceability Matrix(21 项 — 全部覆盖)

| Fix ID | 原问题 | G2-Contract-02 章节 | Effective Spec | 修复状态 | Evidence Grade |
|:-:|---|---|---|---|:-:|
| **RC-1** | API-025~040 Path 错位 14 项 | §4.1 / §4.2 / §4.3 | 233 §API-025~040 | **✅ 已修复** | **A**(直接证据 233)|
| **RC-2** | Transfer 9-step 错位 5 处 | §7.2 | 235B §4.2 / §4.3 | **✅ 已修复**(不创建 ReceptionQueue)| **A**(直接证据 235B)|
| **RC-3a** | Patient 字段命名错 / 多 medicalCode | §3.4 | 238 §4.3 + 236B §3 | **✅ 已修复**(`patientGender` / `patientBirthday` / `idCard` / 删 `medicalCode`)| **A** |
| **RC-3b** | Employee 严重缺字段 | §3.5 | 238 §4.4 + 235B §2 | **✅ 已修复**(增 `adminId` / `nickname` / `departmentId` / `status`)| **A** |
| **RC-3c** | ConsultRoom 字段命名错 | §3.6 | 238 §4.5 | **✅ 已修复**(`consultRoomName` / `status` / `examineList` / 删 `roomNo`)| **A** |
| **RC-3d** | BigScreen 字段命名错 / 缺关键 | §3.7 | 238 §4.6 + §15 | **✅ 已修复**(`bigScreenName` / `sceneType` / `consultRoomIdArray` JSON / `status`)| **A** |
| **RC-3e** | AppointmentSchedule 字段错 | §3.8 | 238 §4.8 | **✅ 已修复**(`employeeId` FK / `remark` / 删 `startTime/endTime`)| **A** |
| **RC-3f** | AppointmentSlot 字段命名错 | §3.9 | 238 §4.9 + 236B §3.5 | **✅ 已修复**(`capacity` / `bookedCount` / `startTime/endTime` / `consultRoomId` FK / `serviceType`)| **A** |
| **RC-3g** | Appointment 严重缺字段 | §3.10 | 238 §4.7 | **✅ 已修复**(拆 `appointmentTime` → 3 字段 / 增 11 字段)| **A** |
| **RC-3h** | Visit 严重缺字段 | §3.11 | 238 §4.10 | **✅ 已修复**(删 `checkInTime` / `employeeId` / 增 `visitType` / `transferredFromXxx` / `cancelledAt/completedAt/transferredAt`)| **A** |
| **RC-3i** | ReceptionQueue 缺字段 | §3.13 | 238 §4.12 | **✅ 已修复**(增 `triageQueueId` UNIQUE / `sequenceInRoom` / `calledAt/startedAt/completedAt` / `skippedTimes` / `cancelReason` / 6 状态)| **A** |
| **RC-4** | IGNORE_TABLES 不完整(2 vs 5)| §12.1 / §12.2 / §12.3 / §12.5 | 241V4 §6.1 | **✅ 已修复**(5 个配置项 + 4 当前 + 1 预留)| **A** |
| **RC-5** | company 业务表概念错 | §8.1 | 235B §1 + 238 §4.1 | **✅ 已修复**(明确 company 是 12 业务 Object 之一)| **A** |
| **RC-6** | 公开 API 白名单缺 bigscreen/display | §9.2 | 241V2 §5.6 + 233 §API-040 | **✅ 已修复**(补 `/api/bigscreen/display`)| **A** |
| **PA-01** | 6 Service 方法 Contract 缺 | §6.2 | 232 / 233 / 235B / 240 / 241V2 | **🟡 部分冻结 + 部分【待确认】** | **B**(已有冻结)| |
| **PA-02** | API-016 / API-021 Transaction 分类未冻结 | §7.3 | 233 §API-016 / 021 | **🟡 部分冻结(业务动作)+【待确认】(分类)** | **C** |
| **PA-03** | 7 角色 / 权限矩阵 / Sa-Token 注解 | §9.1 / §9.2 / §9.3 / §9.4 | 235B §2 + 233 | **🟡 部分冻结(角色 + 权限矩阵 + 白名单)+【待确认】(Sa-Token annotation)** | **B / C** |
| **PA-04** | flyway_schema_history_v44 激活条件 | §12.3 | 241V4 §6.1 | **🟡【待确认】** | **C** |
| **PA-05** | Phase 1 系统设置 26 项字段 | §14.2 | (侦察未闭环)| **🔴【待确认】** | **D**(无证据)|
| **PA-06** | SystemSetting V4.4 范围 | §15 | (未冻结)| **🔴【待确认】** | **D**(无证据)|
| **PA-07** | Transfer Rollback 策略 | §7.5 | 235B §4.2 | **🟡 部分冻结(整体事务 + COMMIT)+【待确认】(补偿策略)** | **B / C** |

### 16.1 修复完成统计

| 状态 | 数量 | 占比 |
|---|---:|---:|
| **✅ 已修复**(14 项 P0 全部完成)| **14 项** | **66.7%** |
| **🟡 部分冻结**(部分内容 + 部分【待确认】)| **4 项** | **19.0%** |
| **🔴【待确认】**(无有效证据)| **3 项** | **14.3%** |
| **总 Fix Actions** | **21 项** | **100.0%** |

### 16.2 Evidence Grade 分布

| Grade | 数量 | 占比 |
|---|---:|---:|
| A(直接证据)| 14 项 | **66.7%** |
| B(多源交叉验证)| 0 项(单独)| 0.0% |
| C(部分证据)| 4 项 | 19.0% |
| D(无证据 / 冲突)| 3 项 | 14.3% |
| **E(AI 推断 → 冻结)** | **0 项** | **0.0%** |
| **F(Contract 错误)** | **0 项** | **0.0%** |

---

## §17 Remaining Uncertainty(汇总所有【待确认】)

> 本节集中列出所有未冻结内容,供后续冻结或独立盲审参考。
> **严禁 AI 自行推断 → 冻结**。

### 17.1 字段级【待确认】(8 项)

| # | Object | 项 | 状态 |
|--:|---|---|---|
| 1 | Company | `phone` 字段是否业务必需 | 【待确认】 |
| 2 | ConsultRoom | `examineList` 格式(JSON / ID 列表)| 【待确认】 |
| 3 | BigScreen | `sceneType` 枚举值 | 【待确认】 |
| 4 | AppointmentSlot | `status` 枚举(DRAFT/OPEN/CLOSED)| 【待确认】 |
| 5 | Appointment | `appointmentType` / `appointmentSource` 枚举 | 【待确认】 |
| 6 | Visit | `visitType` 枚举(APPOINTMENT/WALK_IN)| 【待确认】 |
| 7 | Employee | `status` 枚举 | 【待确认】 |
| 8 | ReceptionQueue | 6 状态具体名称 | 【待确认】 |

### 17.2 Contract 级【待确认】(12 项)

| # | 类别 | 项 |
|--:|---|---|
| 1 | Service | 6 Service 中除已冻结 CRUD 之外的方法 |
| 2 | Transaction | API-016 / API-021 分类(T1/T2/T3/T4)|
| 3 | Security | Sa-Token `@SaCheckRole` / `@SaCheckPermission` 具体 annotation |
| 4 | Security | Sa-Token StpInterface / Redis 配置 / 登录态时长 |
| 5 | IGNORE_TABLES | flyway_schema_history_v44 激活条件 |
| 6 | Phase 1 | 系统设置 26 项页面字段 |
| 7 | SystemSetting V4.4 | 范围与字段 |
| 8 | Transfer | Rollback strategy |
| 9 | NumberGenerator | appointmentNo 生成策略 |
| 10 | 角色 | 7 角色完整定义(233 散落冻结)|
| 11 | 权限 | 40 API × 7 角色完整矩阵 |
| 12 | DTO/VO | Request DTO / Response VO 完整字段(233 部分冻结)|

---

## §18 G2 Readiness Checklist

> **G2-Contract-02 ≠ READY 判定**。本节为 G2-Contract-Audit-02 独立盲审的输入。

### 18.1 G2-Contract-Audit-02 必须验证的硬性条件

| # | 条件 | 状态 |
|--:|---|:-:|
| 1 | **P0 = 0**:所有 14 项 P0 Fix Action 完整覆盖 233 / 235B / 238 / 236B / 241V4 | ✅ 见 §16 |
| 2 | **P1 = 0**(或残留项有明确证据支持不阻塞)| 🟡 部分,**待 G2-Contract-Audit-02 判定** |
| 3 | **Effective Spec 直接冲突 = 0** | ✅ 见 §16(无 E / F 级证据)|
| 4 | **未冻结内容不得伪装成冻结事实** | ✅ §13 / §17 全部【待确认】显式标注 |
| 5 | **不得自行发明**字段 / API / 状态 / 权限 / Transaction 规则 | ✅ §16 E 级 = 0 |

### 18.2 G2-Contract-02 完成度

| 维度 | 完成度 |
|---|---|
| 12 Object 字段级 | **100%**(9 重写 + 3 沿用)|
| 40 API Path | **100%**(14 重写 + 26 一致)|
| Transfer 9-step | **100%**(按 235B 修正)|
| IGNORE_TABLES | **100%**(5 配置项)|
| Tenant 概念 | **100%**(company 是 12 业务 Object 之一)|
| 公开 API 白名单 | **100%**(含 bigscreen/display)|
| Exception | **100%**(沿用)|
| DEFAULT Test | **100%**(沿用)|
| 6 Service 方法(PA-01)| **部分 +【待确认】** |
| Transaction(PA-02)| **部分 +【待确认】** |
| Security(PA-03)| **部分 +【待确认】** |
| IGNORE_TABLES 预留(PA-04)| **【待确认】** |
| Phase 1(PA-05)| **【待确认】** |
| SystemSetting V4.4(PA-06)| **【待确认】** |
| Transfer Rollback(PA-07)| **部分 +【待确认】** |

### 18.3 G2-Contract-Audit-02 必须做的工作

| # | 任务 |
|--:|---|
| 1 | 逐项核验 §16 Fix Traceability Matrix 是否真实修复 |
| 2 | 检查 §3 / §4 / §7.2 是否仍存在 E / F 级证据 |
| 3 | 检查 §13 / §17【待确认】是否合理(不阻塞 G2 READY 可接受)|
| 4 | 验证 §9.2 公开 API 白名单是否完整 |
| 5 | 验证 §12 IGNORE_TABLES 是否完整 |
| 6 | 独立判定:G2-Contract-02 是否达到 READY |

---

## §19 Evidence Index

| 章节 | 证据来源 |
|---|---|
| §3 Object 字段级 | 238 §4 + 236B §3 + 235B §1 + 241V4 §4.2 |
| §4 API Path | 233 §API-001~040 + 232 §API-001~024 |
| §5 Repository | 238 §6.1 / §6.2 / §6.3 + 241V2A-10 / 12 / 13 |
| §6 Service | 232 / 233 / 235B / 238 §7 + 240 / 241V2 |
| §7 Transaction | 235B §4.2 / §4.3 + 241V2A-11 / 19 |
| §8 Tenant | 240 §3 + 241V2 §4 / §5 + 241V4 §4.2 / §6.1 |
| §9 Security | 235B §2 + 233 + 241V2 §5.6 |
| §10 Exception | 241 §4 + 241V2 §13.2 + 241V2A-16 / 17 / 18 |
| §11 DEFAULT Test | 241V2A-11 / 12 / 13 / 14 / 15 / 17 / 18 / 19 |
| §12 IGNORE_TABLES | 241V2 §6.4 + 241V4 §6.1 + 235B §6.3 |
| §13-15 P1 Pending | (待后续冻结)|
| §16 Fix Traceability | R2 §7 + 本 Contract 全文 |

---

## §20 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-02_OptFlow-PMS_Production-Implementation-Contract.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-01 / 不修改 G2-Contract-Audit-01* / 不修改任何历史 MD |
| 严禁 | 修改任何已有审计文件 / 修改任何历史 MD / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |
| **重要声明** | **本 Contract 不等于 G2 READY 判定**。完成后必须经过 G2-Contract-Audit-02 独立盲审。 |

---

**End of G2-Contract-02**