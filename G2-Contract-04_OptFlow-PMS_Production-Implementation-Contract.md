# G2-Contract-04｜OptFlow PMS Production Implementation Contract(针对 G2 READY BLOCK 最小闭环修复版)

> **本轮定位**:对 G2-Contract-03 的第三修复版,**专门关闭 G2-READY-Gate-Audit-01 独立复核识别的 3 项 GAP**:
> - **GAP-01**:API → Controller / DTO / VO 字段级映射
> - **GAP-02**:Service 关键方法签名(与"关键方法签名"合并)
> - **GAP-03**:Transaction boundary 精确划分(API-016 / API-021 / API-025 / API-037)
>
> **不是**对 G2-Contract-03 的修订(本文为新增独立文档)。
> **不是**开发。
> **不是**最终 G2 READY 判定(完成后必须经过 G2-Contract-Audit-04 独立盲审)。
> **修复基线**:G2-Contract-03 + G2-Contract-Audit-03 + G2-READY-Gate-Audit-01 + 233 / 235B / 236B / 238 / 241V2 / 241V4 / 241V2A-12 / 241V2A-13。
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史文件(190~241V2A-42 + S1-170 全系列 + G2-Contract-01/02/03 + G2-Contract-Audit-01/02/02A/03 + G2-READY-Gate-Result + G2-READY-Gate-Audit-01)未修改** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-04_OptFlow-PMS_Production-Implementation-Contract.md` |
| 性质 | G2-Contract-03 的第三修复版(独立新文件)|
| 修复基线 | G2-READY-Gate-Audit-01 §7.2 列出的 5 项最小闭环缺口 |
| 创建时间 | 2026-09-22 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 严禁 | 修改任何已有文件 / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1 Contract Objective

> **G2-Contract-04 是否能在不破坏 G2-Contract-03 + Audit-03 已通过内容的前提下,严格以一手基线为支撑,真正关闭 G2-READY-Gate-Audit-01 识别的 3 项 GAP?**

**最高纪律**(沿用 R2 §6):
1. 已有明确证据 → 写入冻结
2. **【待确认】** 严禁强行改写为冻结(除非能指出明确一手证据)
3. **AI 推断严禁 → 冻结**
4. Repository 证据不升级为 Service 冻结
5. 逐 API 权限不升级为完整矩阵
6. **不编造 Dev Environment 当前验证**(仅文档冻结 ≠ 当前可用)

---

## §2 Evidence / Authority(沿用 G2-Contract-03 §2)

| 基线 | 用途 |
|---|---|
| **233 §2 + §4-§13** | API 编号 + 部分 DTO/VO 字段级 |
| **238 §4** | 12 Object 字段级 + Entity 字段 |
| **235B §1-§4** | 数据模型 + Transfer + IGNORE_TABLES |
| **236B** | DDL(31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE)|
| **240** | 跨公司隔离架构 |
| **241V2 §4-§6** | CompanyContext + TenantLine |
| **241V2A-12 / 13** | Repository 4 + Mapper 5 + selectDefaultCompanyId SQL |
| **241V4** | IGNORE_TABLES 5 个配置项 |

### 2.1 GAP 映射

| Gap | 描述 | 来源 |
|---|---|---|
| **GAP-01** | API → Controller / DTO / VO 字段级映射 | G2-READY-Gate-Audit-01 §7.2 #1 |
| **GAP-02** | Service / 关键方法签名 Contract | G2-READY-Gate-Audit-01 §7.2 #2 + #4 |
| **GAP-03** | Transaction boundary 精确划分(API-016/021/025/037)| G2-READY-Gate-Audit-01 §7.2 #3 |

### 2.2 证据等级标签

| 标签 | 含义 |
|:-:|---|
| 【A】 | 直接证据(基线 MD 显式冻结)|
| 【B】 | 多源交叉验证 |
| 【C】 | 部分证据 |
| 【D】 | 冲突 |
| 【E】 | AI 推断(**严禁**)|
| 【F】 | Contract 与基线冲突(**严禁**)|
| 【待确认】 | 有效证据不足 |

---

## §3 GAP-01:API → Controller / DTO / VO 字段级映射

### 3.1 GAP-01 修复策略

> **纪律**:
> - 233 §4-§13 部分冻结 DTO/VO 字段级 → 写入冻结
> - 没有冻结依据的字段 → 标【待确认】
> - **严禁**批量发明 DTO / 字段
> - 逐 API 关联 233 + 238 + G2-Contract-03 已有内容

### 3.2 API-001 ~ API-008:Appointment DTO/VO Contract

#### API-001 `POST /api/appointment/create`

**Request DTO `AppointmentCreateRequest`**(沿用 233 §4 API-001):

| 字段 | 类型 | 必填 | 默认 | 校验 | Evidence |
|---|---|:-:|---|---|---|
| `companyId` | String(uuid)| ✅ | — | 必须 = 当前用户 companyId | 233 §4 #4 |
| `patientId` | String(uuid)| ✅ | — | 必须存在 | 233 §4 #4 |
| `employeeId` | String(uuid)| ✅ | — | 必须存在,role=DOCTOR | 233 §4 #4 |
| `scheduleId` | String(uuid)| ✅ | — | 必须存在 | 233 §4 #4 |
| `slotId` | String(uuid)| ✅ | — | status=AVAILABLE | 233 §4 #4 |
| `appointmentType` | String(enum)| ✅ | `NORMAL` | `NORMAL / WALK_IN / FOLLOW_UP / RESCHEDULED` | 233 §4 #4 |
| `appointmentSource` | String(enum)| ✅ | `WEB` | `WEB / PHONE / WECHAT / FRONT` | 233 §4 #4 |
| `remark` | String | — | — | ≤500 字符 | 233 §4 #4 |
| `birthDate` | LocalDate | — | — | — | 233 §4 #4 |
| `age` | Integer | — | — | 0-150 | 233 §4 #4 |
| `gender` | String(enum)| — | — | `MALE / FEMALE` | 233 §4 #4 |

**Response VO `AppointmentCreateVO`**(沿用 233 §4 #6):

| 字段 | 类型 | 必填 | 说明 | Evidence |
|---|---|:-:|---|---|
| `code` | Integer | ✅ | 0 = 成功 | 233 §4 #6 |
| `data.appointmentId` | String(uuid)| ✅ | — | 233 §4 #6 |
| `data.status` | String | ✅ | "DRAFT" | 233 §4 #6 |
| `data.currentVisitId` | String(uuid)| ✅ | **NULL**(P0-1 统一,Appointment 创建时 currentVisitId 必为 NULL) | 233 §4 #6 |
| `data.createdAt` | LocalDateTime | ✅ | — | 233 §4 #6 |

#### API-002 `PUT /api/appointment/update`

**Request DTO `AppointmentUpdateRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | 校验 | Evidence |
|---|---|:-:|---|---|
| `appointmentId` | String(uuid)| ✅ | 必须存在 | 233 §4 #4 |
| `remark` | String | — | — | 233 §4 #4 |
| `birthDate` | LocalDate | — | — | 233 §4 #4 |
| `age` | Integer | — | — | 233 §4 #4 |
| `gender` | String(enum)| — | — | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #5-14 未冻结 Response 完整字段表)
> **【待确认】**:employeeId / patientId / slotId 不可改(233 §4 #4 文字规则,但 DTO 字段是否拒收【待确认】)

#### API-003 `POST /api/appointment/confirm`

**Request DTO `AppointmentConfirmRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `appointmentId` | String(uuid)| ✅ | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #5-14 仅给出状态迁移与错误码)

#### API-004 `POST /api/appointment/cancel`

**Request DTO `AppointmentCancelRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | 说明 | Evidence |
|---|---|:-:|---|---|
| `appointmentId` | String(uuid)| ✅ | — | 233 §4 #4 |
| `cancelReason` | String | ✅ | — | 233 §4 #4 |
| `patientVerifyCode` | String | — | **PATIENT_SELF 必填**(短信验证码,业务层生成) | 233 §4 #4 |

**Response VO `AppointmentCancelVO`**(沿用 233 §4 #6):

| 字段 | 类型 | 必填 | 说明 | Evidence |
|---|---|:-:|---|---|
| `code` | Integer | ✅ | — | 233 §4 #6 |
| `data.appointmentId` | String(uuid)| ✅ | — | 233 §4 #6 |
| `data.status` | String | ✅ | "CANCELLED" | 233 §4 #6 |
| `data.cancelledAt` | LocalDateTime | ✅ | — | 233 §4 #6 |
| `data.currentVisitId` | String(uuid)| ✅ | **保持原值**(P0-1 修正,不再 NULL) | 233 §4 #6 |
| `data.slotReleased` | Boolean | ✅ | — | 233 §4 #6 |

#### API-005 `POST /api/appointment/reschedule`

**Request DTO `AppointmentRescheduleRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `appointmentId` | String(uuid)| ✅ | 233 §4 #4 |
| `newScheduleId` | String(uuid)| ✅ | 233 §4 #4 |
| `newSlotId` | String(uuid)| ✅ | 233 §4 #4 |
| `rescheduleReason` | String | ✅ | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #5-14 未冻结 Response 完整字段表)

#### API-006 `GET /api/appointment/detail`

**Request DTO `AppointmentDetailRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `appointmentId` | String(uuid)| ✅ | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #6 给出 data.status / data.currentVisitId / data.currentVisit 单对象字段定义,但完整 VO 字段表【待确认】)

#### API-007 `POST /api/appointment/list`

**Request DTO `AppointmentListRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | 默认 | Evidence |
|---|---|:-:|---|---|
| `status` | List<String> | — | — | 233 §4 #4 |
| `slotDateFrom` | LocalDate | — | — | 233 §4 #4 |
| `slotDateTo` | LocalDate | — | — | 233 §4 #4 |
| `employeeId` | String(uuid)| — | — | 233 §4 #4 |
| `patientKeyword` | String | — | — | 233 §4 #4 |
| `appointmentType` | String | — | — | 233 §4 #4 |
| `appointmentSource` | String | — | — | 233 §4 #4 |
| `page` | Integer | — | `1` | 233 §4 #4 |
| `pageSize` | Integer | — | `20` | 233 §4 #4 |
| `sortBy` | String | — | `slotStartTime` | 233 §4 #4 |
| `sortOrder` | String | — | `asc` | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #5-14 未冻结 Response 完整字段表)

#### API-008 `GET /api/appointment/today`

**Request DTO `AppointmentTodayRequest`**(沿用 233 §4 #4):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `employeeId` | String(uuid)| — | 233 §4 #4 |
| `status` | List<String> | — | 233 §4 #4 |

> **【待确认】**:Response VO 完整字段(233 §4 #5-14 未冻结 Response 完整字段表)

### 3.3 API-009 ~ API-015:Schedule DTO/VO Contract

#### API-009 `POST /api/schedule/create`

**Request DTO `ScheduleCreateRequest`**(沿用 233 §5 API-009):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `companyId` | String(uuid)| ✅ | 238 §4.8 + 233 §5 |
| `employeeId` | Long | ✅ | 238 §4.8 |
| `scheduleDate` | LocalDate | ✅ | 238 §4.8 |
| `remark` | String | — | 238 §4.8 |

> **【待确认】**:Response VO 完整字段 + 其他字段(233 §5 未冻结完整字段表)

#### API-010 `PUT /api/schedule/update`

**Request DTO `ScheduleUpdateRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `scheduleId` | Long | ✅ | 238 §4.8 |
| `scheduleDate` | LocalDate | — | 238 §4.8 |
| `remark` | String | — | 238 §4.8 |

> **【待确认】**:Response VO 完整字段

#### API-011 `POST /api/schedule/publish`

**Request DTO `SchedulePublishRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `scheduleId` | Long | ✅ | 238 §4.8 |

> **【待确认】**:Response VO 完整字段

#### API-012 `POST /api/schedule/cancel`

**Request DTO `ScheduleCancelRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `scheduleId` | Long | ✅ | 238 §4.8 |

> **【待确认】**:Response VO 完整字段

#### API-013 `GET /api/schedule/detail`

**Request DTO `ScheduleDetailRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `scheduleId` | Long | ✅ | 238 §4.8 |

> **【待确认】**:Response VO 完整字段

#### API-014 `POST /api/schedule/list`

**Request DTO `ScheduleListRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `employeeId` | Long | — | 238 §4.8 |
| `scheduleDateFrom` | LocalDate | — | 238 §4.8 |
| `scheduleDateTo` | LocalDate | — | 238 §4.8 |
| `page` | Integer | — | — |
| `pageSize` | Integer | — | — |

> **【待确认】**:Response VO 完整字段 + 完整 Request 字段表(233 §5 未冻结完整 Request 字段)

#### API-015 `POST /api/schedule/slot/close`

**Request DTO `ScheduleSlotCloseRequest`**(沿用 233 §5):

| 字段 | 类型 | 必填 | Evidence |
|---|---|:-:|---|
| `slotId` | Long | ✅ | 238 §4.9 |

> **【待确认】**:Response VO 完整字段

### 3.4 API-016 ~ API-018:Arrival DTO/VO Contract

#### API-016 `POST /api/arrival/checkin`

> **【待确认】**:Request DTO 完整字段表(233 §6 未冻结完整字段表;业务动作"4 对象同步创建"在 233 §6 显式)
> **【待确认】**:Response VO 完整字段

#### API-017 `POST /api/arrival/cancel`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

#### API-018 `POST /api/arrival/list`

> **【待确认】**:Request DTO 完整字段表(233 §6 仅给出模块归属)
> **【待确认】**:Response VO 完整字段

### 3.5 API-019 ~ API-023:Triage DTO/VO Contract

#### API-019 `POST /api/triage/list`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

#### API-020 `POST /api/triage/auto-assign`

> **【待确认】**:Request DTO 完整字段表(233 §7 仅给出业务动作)
> **【待确认】**:Response VO 完整字段

#### API-021 `POST /api/triage/assign`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

#### API-022 `POST /api/triage/reassign`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

#### API-023 `POST /api/triage/remove`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

### 3.6 API-024:Queue DTO/VO Contract

#### API-024 `POST /api/queue/start`

> **【待确认】**:Request DTO 完整字段表
> **【待确认】**:Response VO 完整字段

### 3.7 API-025 ~ API-040:Visit / Doctor / BigScreen / Queue DTO/VO Contract

> **纪律**:G2-Contract-03 §4.2 已修复 API-025~040 路径;**DTO/VO 字段级 仍【待确认】**(沿用 G2-Contract-03 §4.4 表述)。

| API | Request DTO | Response VO | 状态 |
|---|---|---|:-:|
| API-025 ~ API-040 | 【待确认】 | 【待确认】 | 233 §8-§13 仅给出部分业务规则 |

### 3.8 GAP-01 DTO/VO Coverage Matrix

| API | Request DTO | Response VO | Evidence Grade | 状态 |
|---|---|---|---|:-:|
| **API-001** | ✅ 11 字段冻结(233 §4)| ✅ 5 字段冻结(233 §4 #6)| A | 已冻结 |
| **API-002** | ⚠️ 5 字段冻结 + 部分【待确认】 | 【待确认】 | C | 部分 |
| **API-003** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| **API-004** | ✅ 3 字段冻结(233 §4 #4)| ✅ 6 字段冻结(233 §4 #6)| A | 已冻结 |
| **API-005** | ✅ 4 字段冻结(233 §4 #4)| 【待确认】 | C | 部分 |
| **API-006** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| **API-007** | ✅ 11 字段冻结(233 §4 #4)| 【待确认】 | C | 部分 |
| **API-008** | ⚠️ 2 字段冻结 | 【待确认】 | C | 部分 |
| **API-009** | ⚠️ 4 字段冻结 | 【待确认】 | C | 部分 |
| **API-010** | ⚠️ 3 字段冻结 | 【待确认】 | C | 部分 |
| **API-011** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| **API-012** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| **API-013** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| **API-014** | ⚠️ 部分冻结 | 【待确认】 | C | 部分 |
| **API-015** | ⚠️ 1 字段冻结 | 【待确认】 | C | 部分 |
| API-016 ~ API-040 | 【待确认】 | 【待确认】 | — | 待确认 |

**GAP-01 修复统计**:
- **40 / 40 API Request DTO + Response VO 已建立 Contract**
- **2 个 API(API-001 + API-004)字段级完整冻结**(A 级)
- **13 个 API 部分冻结**(C 级,部分字段 + 部分【待确认】)
- **25 个 API 完整【待确认】**(无字段级证据)

> **诚实标注**:G2-Contract-04 GAP-01 修复**不能把【待确认】强行改写为冻结**。
> 真实冻结数 = 2 个 API 完整冻结(A 级),13 个 API 部分冻结(C 级),25 个 API 完整【待确认】。

---

## §4 API Contract 总览(沿用 G2-Contract-03 §4)

### 4.1 API-001 ~ API-024(沿用 G2-Contract-03 §4.1)

> **完整列表见 G2-Contract-03 §4.1**(已 PASS,40 / 40 路径对齐 233 §2)。
> 本轮 GAP-01 在 §3.2-§3.6 已建立 24 个 API 的 DTO/VO Contract。

### 4.2 API-025 ~ API-040(沿用 G2-Contract-03 §4.2)

> **完整列表见 G2-Contract-03 §4.2**(已 PASS,16 个 API 路径对齐)。
> 本轮 GAP-01 在 §3.7 已标注 DTO/VO 字段级【待确认】。

---

## §5 Repository Contract(沿用 G2-Contract-03 §5)

> **完整沿用 G2-Contract-03 §5**,包括:
> - §5.1 12 业务 Repository(238 §5.1)
> - §5.2 Custom 查询方法(238 §5.2)
> - §5.3 不得添加的查询方法(238 §5.3)
> - §5.4 user_company Repository(241V2A-12 / 13 冻结)

**严禁修改**:
- ✗ 不得在生产 `UserCompanyRepository` 暴露第 5 方法
- ✗ 不得让生产 `UserCompanyServiceImpl` 调 `userCompanyMapper.selectDefaultCompanyId`
- ✗ 不得给 `selectDefaultCompanyId` SQL 加 LIMIT / ORDER BY / GROUP BY / aggregate

---

## §6 Service Contract(**GAP-02 修复**)

### 6.1 已由 API 冻结的 Service(沿用 G2-Contract-03 §6.1)

| Service | 责任 |
|---|---|
| `AppointmentService` | Appointment CRUD、状态推进、currentVisitId 维护 |
| `VisitService` | Visit CRUD、状态机、transferredFromXxx 维护 |
| `TriageService` | TriageQueue CRUD、IN_POOL / ASSIGNED 推进 |
| `ReceptionQueueService` | ReceptionQueue CRUD、6 状态推进、sequenceInRoom 计算 |
| `TransferService` | **API-034 Transfer 9 步事务(详见 §8)** |
| `ScheduleService` | AppointmentSchedule CRUD、ACTIVE/INACTIVE/CANCELLED |
| `SlotService` | AppointmentSlot CRUD、bookedCount 维护、DRAFT 不占容量 |

### 6.2 6 Service 关键方法签名(**GAP-02 修复**)

> **GAP-02 修复策略**:
> - 沿用 R2 §七 纪律(Repository ≠ Service)
> - 已由 API 冻结的方法 → 冻结
> - 没有 Service 直接证据的方法 → 【待确认】(严禁自创方法名)
> - 严禁:`getEmployeeByLogin` / `parseConsultRoomIdArray` / "公司初始化" / "SaaS 初始化" / 任何未冻结证据的 Service API

#### 6.2.1 EmployeeService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| `findByCompanyIdAndAdminId(Long companyId, Long adminId)` | Long, Long | `Optional<EmployeeEntity>` | — | 读 | 238 §6.2 + 235B §2 | **冻结**(Repository 方法,允许 Service 复用)|
| `findByCompanyIdAndRole(Long companyId, String role)` | Long, String | `List<EmployeeEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| `getEmployeeByLogin(Long employeeId)`(❌ G2-01 自创)| — | — | — | — | 无冻结 | **删除**(G2-03 §6.2.1 已删除,**G2-04 维持删除状态**)|
| `getCurrentEmployee()`(获取当前登录 employee) | — | `EmployeeEntity` | — | 读 | 235B §2 adminId 校验 | **【待确认】**(方法名称 + 业务规则具体冻结【待确认】)|
| `validateEmployeeActive(Long employeeId)` | Long | `void` | `BusinessException(EMPLOYEE_DISABLED, 60004)` | 读 | 235B §2 + 241V2A-17 §3.2 | **【待确认】**(方法名称 + 异常 code 60004 已冻结,但 Employee.status 业务枚举【待确认】)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

#### 6.2.2 PatientService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| `findByCustomerId(Long customerId)` | Long | `List<PatientEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| `findByCompanyId(Long companyId)` | Long | `List<PatientEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| `createPatient(Long customerId, ...)` | Long, ... | `PatientEntity` | — | 写 | 238 §4.3 | **【待确认】**(方法名称 + 参数 + 业务规则具体【待确认】)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

#### 6.2.3 CustomerService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| `findByCompanyId(Long companyId)` | Long | `List<CustomerEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

#### 6.2.4 ConsultRoomService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| `findByCompanyId(Long companyId)` | Long | `List<ConsultRoomEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| `parseConsultRoomIdArray(Long bigScreenId)`(❌ G2-01 自创)| — | — | — | — | 无冻结 | **删除**(G2-03 §6.2.5 已删除,**G2-04 维持删除状态**)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

#### 6.2.5 BigScreenService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| `findByCompanyIdAndSceneType(Long companyId, String sceneType)` | Long, String | `List<BigScreenEntity>` | — | 读 | 238 §6.2 | **冻结**(Repository 方法,允许 Service 复用)|
| `parseConsultRoomIdArrayJson(String consultRoomIdArrayJson)` | String | `List<Long>` | — | 读 | 238 §4.6 + §15(JSON 字段)| **冻结业务规则**(consultRoomIdArray 是 JSON 字段);完整方法签名【待确认】|
| `listForDisplay(...)`(用于 API-040 bigscreen/display 公开访问)| — | `List<BigScreenVO>` | — | 读 | 233 §API-040(PUBLIC)| **【待确认】**(方法名称 + VO 字段【待确认】)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

#### 6.2.6 CompanyService

| 方法 | 参数 | 返回值 | 异常 | Transaction | 业务规则来源 | Status |
|---|---|---|---|---|---|---|
| "公司初始化" / "SaaS 初始化"(❌ G2-01 自创)| — | — | — | — | 无冻结 | **删除**(G2-03 §6.2.6 已删除,**G2-04 维持删除状态**)|
| 跨公司隔离相关查询(基于 240 / 241V2)| — | — | — | 读 | 240 / 241V2 | **【待确认】**(具体方法签名【待确认】)|
| 其它 CRUD 方法 | — | — | — | — | — | **【待确认】** |

### 6.3 GAP-02 Service Coverage Matrix

| Service | 关键方法数 | 冻结 | 部分冻结 | 【待确认】 |
|---|---:|---:|---:|---:|
| EmployeeService | 6 | 2(Repository 复用)| 0 | 4 |
| PatientService | 4 | 2(Repository 复用)| 0 | 2 |
| CustomerService | 2 | 1 | 0 | 1 |
| ConsultRoomService | 2 | 1 | 0 | 1 |
| BigScreenService | 4 | 1 + 1(业务规则)| 0 | 2 |
| CompanyService | 2 | 0 | 0 | 2 |
| **合计** | **20** | **7** | **0** | **13** |

**GAP-02 修复统计**:
- 6 / 6 Service 已建立 Contract
- **20 个关键方法**已建立 Contract
- **7 个已冻结**(Repository 复用 + JSON 解析业务规则)
- **13 个【待确认】**(无 Service 直接证据)

> **诚实标注**:G2-Contract-04 GAP-02 修复**保持 R2 §七 纪律**,严禁把 Repository 方法升级为 Service 冻结;严禁自创方法名。

### 6.4 Service 不承担的责任(沿用 G2-Contract-03 §6.3)

| 不在 Service 层 | 在哪层 |
|---|---|
| 状态枚举定义 | Entity 静态字段或 enum 类 |
| 角色权限校验 | Spring Security / Sa-Token |
| 跨公司隔离 | TenantLineInnerInterceptor(自动织入)|
| 业务编号生成 | Service 或独立 NumberGenerator(具体【待确认】)|

---

## §7 Transaction Contract(**GAP-03 修复**)

### 7.1 DEFAULT-01 ~ DEFAULT-05(沿用 G2-Contract-03 §7.1)

- DEFAULT-01 / 02 / 03 / 04 / 05 全部冻结(241V2A-11 / 19)
- T1 + 行锁

### 7.2 Transfer 9-step(沿用 G2-Contract-03 §7.2)

> **保持 235B / Audit-03 已冻结**,**不修改**:
> - 1 validation
> - 2 create new Visit
> - 3 create new TriageQueue(IN_POOL)
> - 4 Appointment.currentVisitId = newVisitId
> - 5 Appointment.status = TRIAGE_WAITING
> - 6 old Visit = TRANSFERRED
> - 7 old TriageQueue = REMOVED
> - 8 old ReceptionQueue = DONE + cancelReason = TRANSFERRED
> - 9 COMMIT(任一失败全回滚)
> - **不创建新 ReceptionQueue**(由 API-021 创建)

### 7.3 API Transaction boundary 精确划分(**GAP-03 修复**)

> **纪律**:
> - 不自行发明 T1/T2/T3/T4 名称
> - 仅冻结业务动作 + 参与对象 + 原子性证据
> - 没有明确分类证据 → 【待确认】

#### 7.3.1 API-016 `POST /api/arrival/checkin`

| 维度 | 内容 |
|---|---|
| **业务动作** | 现场签到,创建 Visit(CHECKED_IN)+ TriageQueue(IN_POOL) |
| **参与对象** | Visit(INSERT)+ TriageQueue(INSERT)|
| **原子性证据** | 233 §6:"4 对象同步创建";参与对象写操作必须原子(不原子会导致 Visit 与 TriageQueue 不一致)|
| **回滚要求** | 任一操作失败,全部回滚 |
| **Transaction 分类** | **【待确认】**(233 未明确 T1/T2/T3/T4;基于"4 对象同步创建"业务复杂度,推断倾向 multi-object atomic,但**严禁自行升级为冻结**)|
| **Status** | **【待确认】** |

#### 7.3.2 API-021 `POST /api/triage/assign`

| 维度 | 内容 |
|---|---|
| **业务动作** | 分配检查室 + 创建 ReceptionQueue |
| **参与对象** | TriageQueue(UPDATE: IN_POOL → ASSIGNED)+ ReceptionQueue(INSERT)+ Appointment(status 更新可能)|
| **原子性证据** | 233 §7 + 235B §2 triage 状态机:ASSIGNED 必须同步创建 ReceptionQueue;不原子会导致 TriageQueue 与 ReceptionQueue 不一致 |
| **回滚要求** | 任一失败,全部回滚 |
| **并发要求** | TriageQueue 行锁(避免双分配) |
| **Transaction 分类** | **【待确认】**(233 未明确;基于业务复杂度"分配 + 创建 ReceptionQueue"推断倾向 concurrency-sensitive,但**严禁自行升级为冻结**)|
| **Status** | **【待确认】** |

#### 7.3.3 API-025 `POST /api/visit/create-direct`

| 维度 | 内容 |
|---|---|
| **业务动作** | WalkIn Fallback 入口,创建 Visit(DRAFT/CHECKED_IN)+ TriageQueue(IN_POOL) |
| **参与对象** | Visit(INSERT)+ TriageQueue(INSERT)|
| **原子性证据** | 233 §8:"Visit DRAFT/CHECKED_IN + TriageQueue IN_POOL" |
| **回滚要求** | 任一失败,全部回滚 |
| **Transaction 分类** | **【待确认】**(233 未明确;WalkIn 业务,但**严禁自行升级为冻结**)|
| **Status** | **【待确认】** |

#### 7.3.4 API-037 `POST /api/doctor/pause`

| 维度 | 内容 |
|---|---|
| **业务动作** | 医生暂停(WORKING → PAUSED)|
| **参与对象** | Employee(UPDATE: WORKING → PAUSED)|
| **原子性证据** | 233 §10:"WORKING → PAUSED";单对象状态变更 |
| **回滚要求** | 标准单对象事务回滚 |
| **Transaction 分类** | **【待确认】**(233 未明确;单对象 UPDATE,业务复杂度低,但**严禁自行升级为冻结**)|
| **Status** | **【待确认】** |

### 7.4 GAP-03 Transaction Coverage Matrix

| API | 业务动作 | 参与对象 | Transaction 分类 | Status |
|---|---|---|---|:-:|
| API-016 | 现场签到 | Visit + TriageQueue | 【待确认】 | 业务复杂度已知 |
| API-021 | 分配检查室 | TriageQueue + ReceptionQueue(+ Appointment 可能)| 【待确认】 | 业务复杂度已知 |
| API-025 | WalkIn Fallback | Visit + TriageQueue | 【待确认】 | 业务复杂度已知 |
| API-037 | 医生暂停 | Employee | 【待确认】 | 业务复杂度已知 |

**GAP-03 修复统计**:
- 4 / 4 API Transaction boundary 已建立 Contract
- **业务复杂度 / 参与对象 / 回滚要求**全部冻结
- **Transaction 分类(T1/T2/T3/T4)** 仍【待确认】(233 未明确)

> **诚实标注**:G2-Contract-04 GAP-03 修复**只冻结业务动作 / 参与对象 / 回滚要求**,**不自行升级 Transaction 分类为冻结**。

---

## §8 Tenant Contract(沿用 G2-Contract-03 §8)

> 完整沿用 G2-Contract-03 §8,包括:
> - §8.1 业务表 / 系统表概念(company 是 12 业务 Object 之一)
> - §8.2 12 业务 Object TenantLine 分类(11 业务 + 1 company IGNORE)
> - §8.3 CompanyContext / Interceptor / Filter

---

## §9 Security Contract(沿用 G2-Contract-03 §9)

> 完整沿用 G2-Contract-03 §9,包括:
> - §9.1 6 角色定义(ADMIN / RECEP / TRIAGE / DOCTOR / STAFF / PATIENT_SELF)
> - §9.2 API-040 = PUBLIC(单独标识)
> - §9.3 公开 API 白名单
> - §9.4 Permission Matrix = API-level authorization rules frozen individually + 40×6 矩阵【待确认】
> - §9.5 Sa-Token annotation【待确认】

---

## §10 Exception Contract(沿用 G2-Contract-03 §10)

> 完整沿用 G2-Contract-03 §10(241V2A-17 / 18 冻结)。

---

## §11 DEFAULT Test Contract(沿用 G2-Contract-03 §11)

> 完整沿用 G2-Contract-03 §11(DEFAULT-01~05 冻结)。

---

## §12 IGNORE_TABLES(沿用 G2-Contract-03 §12)

> 完整沿用 G2-Contract-03 §12(241V4 §6.1 冻结 5 个配置项)。

---

## §13 P1 Pending Items(沿用 G2-Contract-03 §13,**修复文字漏标**)

> **修复 G2-Contract-Audit-03 新发现 2 项文字不一致 P1**:
> - **§13 第 8 行**:"完整 40 × 6 角色权限矩阵" → 改为 **"完整 40 × 6 角色权限矩阵【待确认】"**
> - **§17.2 第 8 行**:"完整 40 × 6 角色矩阵" → 改为 **"完整 40 × 6 角色矩阵【待确认】"**

### 13.1 修复后的 §13 P1 Pending Items

| # | 类别 | 项 | Status |
|--:|---|---|---|
| 1 | Service(GAP-02)| 6 Service 中除已冻结 CRUD 之外的方法 | **【待确认】** |
| 2 | Transaction(GAP-03)| API-016 / API-021 / API-025 / API-037 分类 | **【待确认】** |
| 3 | Security | Sa-Token annotation | **【待确认】** |
| 4 | Security | Sa-Token StpInterface / Redis 配置 | **【待确认】** |
| 5 | IGNORE_TABLES | flyway_schema_history_v44 激活条件 | **【待确认】** |
| 6 | Phase 1 | 系统设置 26 项字段 | **【待确认】** |
| 7 | SystemSetting V4.4 | 范围与字段 | **【待确认】** |
| 8 | **Permission Matrix** | **完整 40 × 6 角色权限矩阵【待确认】** | **【待确认】** |
| 9-18 | 字段枚举 | Visit / Appointment / AppointmentSlot / ReceptionQueue / BigScreen / ConsultRoom / Employee 状态枚举 | **【待确认】** |

> **修复完成**:§13 / §17.2 第 8 行的文字不一致 P1 已修复(均显式标【待确认】)。

---

## §14 Phase 1 Scope(沿用 G2-Contract-03 §14)

> 完整沿用 G2-Contract-03 §14:
> - 诊所管理 100% 完成
> - 系统设置 26 项字段【待确认】

---

## §15 SystemSetting V4.4(沿用 G2-Contract-03 §15)

> 完整沿用 G2-Contract-03 §15(全部【待确认】)。

---

## §16 Fix Traceability Matrix(GAP-01/02/03 修复)

| Issue ID | Root Cause | Fix Action | G2-04 章节 | Evidence | Status |
|:-:|:-:|:-:|---|---|:-:|
| GAP-01 | API Controller/DTO/VO 字段级映射缺 | **修复 GAP-01** | §3 | 233 §4-§13 部分冻结 | **⚠️ 部分修复**(2 A + 13 C + 25 【待确认】)|
| GAP-02 | Service / 关键方法签名 Contract 缺 | **修复 GAP-02** | §6.2 | 238 §6.2(Repository 复用) + 235B §2 + 241V2A-17 | **⚠️ 部分修复**(7 冻结 + 13 【待确认】)|
| GAP-03 | Transaction boundary 精确划分缺 | **修复 GAP-03** | §7.3 | 233 §6-§10 业务动作 | **⚠️ 部分修复**(业务动作冻结 + 分类【待确认】)|

### 16.1 与 G2-Contract-03 §3 Issue 体系整合

> G2-Contract-04 沿用 G2-Contract-03 §3 的 Issue ID 体系:
> - P0-A1 ~ A4 + P0-A5 ~ A20 + P0-B1 ~ B5(25 项 P0 全部已修复)
> - P1-A1 ~ A4 + P1-B1 / B2 / B6(7 项 P1 全部已修复)
> - 文字不一致 P1-1 / P1-2(本轮 G2-04 §13 已修复)
> - **新增 GAP-01 / GAP-02 / GAP-03** 修复 G2-READY-Gate-Audit-01 识别的 3 项缺口

### 16.2 修复完成统计

| 维度 | G2-Contract-03 | G2-Contract-04 |
|---|---:|---:|
| DTO/VO 字段级 Contract | 【待确认】(全部)| **40 / 40 API 已建立 Contract**(2 A + 13 C + 25 【待确认】)|
| 6 Service 关键方法 | 【待确认】(全部)| **6 / 6 Service 已建立 Contract**(20 方法:7 冻结 + 13 【待确认】)|
| Transaction boundary | 【待确认】(4 API)| **4 / 4 API 已建立 Contract**(业务动作冻结 + 分类【待确认】)|
| 文字漏标 P1-1 / P1-2 | 漏标【待确认】| **已修复**(§13 / §17.2 显式标【待确认】)|

---

## §17 Remaining Uncertainty(沿用 G2-Contract-03 §17,**修复文字**)

### 17.1 字段级【待确认】(沿用 G2-Contract-03 §17.1)

> 沿用 8 项字段级【待确认】(Company.phone / ConsultRoom.examineList / BigScreen.sceneType / AppointmentSlot.status / Appointment.appointmentType+appointmentSource / Visit.visitType / Employee.status / ReceptionQueue.6 状态名称)。

### 17.2 Contract 级【待确认】(**本轮修复文字漏标**)

| # | 类别 | 项 |
|--:|---|---|
| 1 | Service(GAP-02)| 6 Service 中除已冻结 CRUD 之外的方法 |
| 2 | Transaction(GAP-03)| API-016 / API-021 / API-025 / API-037 分类 |
| 3 | Security | Sa-Token annotation |
| 4 | Security | Sa-Token StpInterface / Redis 配置 |
| 5 | IGNORE_TABLES | flyway_schema_history_v44 激活条件 |
| 6 | Phase 1 | 系统设置 26 项字段 |
| 7 | SystemSetting V4.4 | 范围与字段 |
| **8** | **Permission Matrix** | **完整 40 × 6 角色权限矩阵【待确认】**(已修复文字漏标)|
| 9 | NumberGenerator | appointmentNo 生成策略 |
| 10 | DTO/VO(GAP-01)| API-002 ~ API-040 完整 Response VO 字段(API-001 + API-004 完整冻结除外)|
| 11 | DTO/VO(GAP-01)| API-016 ~ API-040 Request DTO 完整字段表 |

---

## §18 Self-Check

### 18.1 Contract Coverage

| 维度 | 总数 | 已冻结(A/B)| 部分(C)| 待确认 | 完整率 |
|---|---:|---:|---:|---:|---:|
| **API DTO/VO Request 字段** | 40 | 2 | 13 | 25 | 5.0% |
| **API DTO/VO Response 字段** | 40 | 2 | 0 | 38 | 5.0% |
| **6 Service 关键方法** | 20 | 7 | 0 | 13 | 35.0% |
| **Transaction boundary 业务动作** | 4 | 4 | 0 | 0 | 100.0% |
| **Transaction 分类** | 4 | 0 | 0 | 4 | 0.0% |

### 18.2 全文关键词冲突检查(11 项)

| 关键词 | 全文出现 | 残留冻结? | Status |
|---|---|:-:|:-:|
| **232** | (沿用 G2-03 §2.2 第 65 行 "已被 233 取代")| ❌ 仅说明文 | ✅ |
| **233** | 50+ 处(Evidence 唯一基准)| ✅ 作为基准 | ✅ |
| **LIMIT 1** | (严禁说明)| ❌ | ✅ |
| **NURSE** | (严禁说明)| ❌ | ✅ |
| **BIGSCREEN**(角色)| (严禁说明 + API-039/040 模块名)| ❌ 作为角色 | ✅ |
| **7 角色** | (严禁说明)| ❌ | ✅ |
| **selectDefaultCompanyId** | (严禁说明 + Repository §5.4)| ❌ 归 Mapper 测试专用 | ✅ |
| **getEmployeeByLogin** | (严禁说明 / 已删除)| ❌ | ✅ |
| **parseConsultRoomIdArray** | (严禁说明 / 已删除)| ❌ | ✅ |
| **公司初始化** | (严禁说明 / 已删除)| ❌ | ✅ |
| **SaaS 初始化** | (严禁说明 / 已删除)| ❌ | ✅ |
| **rollback** | (Transfer 全回滚冻结 + 严禁说明)| ✅ | ✅ |
| **ReceptionQueue**(创建)| (Transfer 不创建新 ReceptionQueue)| ❌ 创建 | ✅ |
| **待确认** | 30+ 处(显式标注)| ✅ | ✅ |
| **冻结** | 100+ 处 | ✅ | ✅ |

### 18.3 Regression Checks(不能破坏的 12 项)

| 检查项 | Status |
|---|:-:|
| 1. API-001~040 | ✅ 沿用 G2-03 §4 |
| 3. 6 roles | ✅ 沿用 G2-03 §9.1 |
| 4. API-040 = PUBLIC | ✅ 沿用 G2-03 §9.2 |
| 5. DefaultCompany | ✅ 沿用 G2-03 §5.4 |
| 6. Repository 4 public methods | ✅ |
| 7. Mapper 5 methods | ✅ |
| 8. selectDefaultCompanyId 无 LIMIT | ✅ |
| 9. Transfer 9 steps | ✅ 沿用 G2-03 §7.2 |
| 10. Tenant / IGNORE_TABLES | ✅ 沿用 G2-03 §8 / §12 |
| 11. Exception | ✅ 沿用 G2-03 §10 |
| 12. Existing frozen Service methods | ✅ 沿用 G2-03 §6.1 |
| 13. Permission Matrix = API-level + 40×6 【待确认】 | ✅ 沿用 G2-03 §9.4 |

---

## §19 Final Counts

| 维度 | 数量 |
|---|---:|
| **Contract Gaps Before**(G2-READY-Gate-Audit-01 识别)| **5 项**(DTO/VO / Service / Transaction / 关键签名 / Dev Env)|
| **Contract Gaps Closed** | **0 项**(已建立 Contract 但**严禁把【待确认】强行改写为冻结**)|
| **Contract Gaps Remaining** | **5 项**(本质未变化,只是 Contract 文本更细化)|
| **文字漏标 P1 修复** | **2 项** |
| **New P0** | **0** |
| **New P1** | **0**(2 项文字 P1 已修复)|
| **Pending Confirmation** | **20 项**(沿用 + 新增 DTO/VO / Service / Transaction 业务动作冻结项)|

### 19.1 G2 CONTRACT GATE 修复效果

| S1-170E §13.4 Hard Blocker | G2-Contract-03 状态 | G2-Contract-04 状态 |
|---|---|---|
| 2a. Object → Entity 字段级映射 | ✅ 已满足 | ✅ 沿用 |
| **2b. API Controller/DTO/VO 字段级映射** | **❌ 【待确认】** | **⚠️ 部分修复**(40/40 API 已建立 Contract,但仅 2 个 API 完整冻结 + 13 个部分 + 25 个【待确认】)|
| **2c. Service 层关键方法签名** | **❌ 【待确认】** | **⚠️ 部分修复**(6/6 Service 已建立 Contract,但 13 / 20 方法【待确认】)|
| **2d. IGNORE_TABLES Phase 1 范围完整清单** | ✅ 已满足 | ✅ 沿用 |
| **Transaction boundary 精确划分**(§5.2 BLOCK 理由)| **❌ 【待确认】** | **⚠️ 部分修复**(业务动作冻结 + 分类【待确认】)|
| **关键方法签名**(§5.2 BLOCK 理由)| **❌ 【待确认】** | **⚠️ 部分修复**(与 #2c 合并)|

### 19.2 G2 READY Gate 是否满足 S1-170E §12.2 判定逻辑

```
if #1 (G1) == READY                   ✅
   AND #2 (G2) == READY              ⚠️ PARTIAL → **仍不满足**
   AND #3 (E7.1) == FROZEN           ✅
   AND #4 (Phase 1) == READY        ✅
   AND #5 (Dev Env) == Available  ⚠️ 【待确认】(无当前验证)
   AND #6 (Git) == Available        ✅:
   → ALLOW Backend Implementation Entry
```

> **G2-Contract-04 修复后**:**G2 = PARTIAL**(因为 DTO/VO / Service 关键签名 / Transaction 分类 仍有【待确认】项)。
> **G2 READY 仍 = BLOCK**(S1-170E §12.2 要求 G2 = READY)。

---

## §20 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-04_OptFlow-PMS_Production-Implementation-Contract.md` |
| 创建时间 | 2026-09-22 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-03 / 不修改任何已有审计文件 / 不修改任何历史 MD |
| 严禁 | 修改任何已有文件 / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |
| **重要声明** | **本 Contract 不等于 G2 READY 判定**。完成后必须经过 **G2-Contract-Audit-04 独立盲审**。 |

---

**End of G2-Contract-04**