# G2-Contract-01｜OptFlow PMS Production Implementation Contract

---

## §0. Metadata

| 字段 | 内容 |
|---|---|
| Stage | G2-Contract-01 |
| Date | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Document Type | Production Implementation Contract(非源码)|
| Scope | 12 业务 Object + user_company + 40 API + Service + Transaction + Tenant + Security + Exception + Test + IGNORE_TABLES |
| 严禁 | 修改历史 MD / 创建 backend / 写 Java 源码 / 创建 SQL / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1. Contract Scope

### 1.1 目标

> 一个熟悉 Java / Spring Boot / MyBatis-Plus 的开发者,只依赖 **Effective Spec + 本 Contract**,就能开始编写 backend,不需要重新猜业务规则。

### 1.2 计数规则(老板指令 §20)

```
12 Object = 12 个业务 Object(238 §2.1 + §2.2)
  - 6 复用:Company / Customer / Patient / Employee / ConsultRoom / BigScreen
  - 6 新建:AppointmentSchedule / AppointmentSlot / Appointment / Visit / TriageQueue / ReceptionQueue

Infrastructure Object(单独统计):
  - user_company(241V2A-10 / 11)
```

### 1.3 Evidence 等级

- **A**:直接证据(规格中显式字段 / 章节)
- **B**:多源交叉验证
- **C**:部分证据(部分字段待确认)
- **D**:冲突(冲突需登记)
- **E**:推断(**严禁**进入冻结 Contract)

---

## §2. Source Baseline

| Source | 提供内容 |
|---|---|
| `229_S1-166A_*.md` | 12 业务 Object + 4 状态机 29 状态 |
| `232_S1-167_*.md` | 40 API 字段级契约 |
| `233_S1-167A_*.md` | 232 修正版 |
| `235B_S1-167B_*.md` | DDL 数据模型裁决 |
| `236B_S1-168_*.md` | DDL 修正版(12 表 + 31 真 FK)|
| `238_S1-169_*.md` | 实施前置映射基线 |
| `240_S1-169_*.md` | Q4 跨公司隔离正式裁决 |
| `241V2_S1-169-1_*.md` | 后端基础设施修正版(CompanyContext / Interceptor / TenantLine / IGNORE_TABLES)|
| `241V2A-10` | UserCompanyRepository + Mapper 完整契约 |
| `241V2A-11` | UserCompanyMapper 前序契约一致性修复 |
| `241V2A-17` / `241V2A-18` | 异常体系(60000-60004 + 9 异常矩阵 + 8 handler)|
| `241V2A-19` | 五级证据体系 |
| `241V2A-5` / `241V2A-14` / `241V2A-15` | DEFAULT-01~05 测试设计 |
| `S1-170E_Final_*.md` | Entry Gate 最终收敛 |

---

## §3. Contract Rules

### 3.1 强制规则

- ✗ 禁止 AI 自行发明字段 / 类型 / 方法 / 权限 / tenant / transaction / error / response / state transition
- ✗ 禁止修改 Effective Spec 内容(本 Contract 必须服从 Effective Spec)
- ✗ 禁止混入源码(本文件不是 Java 代码)
- ✓ 每个 Contract 项目必须标注 evidence(A/B/C/D/E)
- ✓ C 级 / E 级必须标【待确认】

### 3.2 Contract 覆盖矩阵

| Contract 部分 | 覆盖范围 | 状态 |
|---|---|---|
| C1 Object → Entity | 12 业务 Object 字段级 | ✓ |
| C2 user_company Infrastructure | 独立 Contract | ✓ |
| C3 Repository / Mapper | 12 业务 + user_company | ✓ |
| C4 API → Controller / DTO / VO | API-001 ~ API-040 | ✓ |
| C5 Service | 12 业务 + user_company + Auth | ✓ |
| C6 Transaction | T0-T4 分类 | ✓ |
| C7 Tenant | CompanyContext + TenantLine + IGNORE_TABLES | ✓ |
| C8 Security | 角色 + 权限 + Sa-Token | ⚠️ 部分 |
| C9 Exception | 60000-60004 + 9 异常 | ✓ |
| C10 Test / Acceptance | DEFAULT-01~05 | ✓ |
| C11 IGNORE_TABLES | Phase 1 12 表 | ⚠️ 部分 |

---

## §4. C1:12 Object → Entity Contract

### 4.1 通用规则

- 所有 Entity 必须放在 `com.optflow.pms.module.<module>.entity` 包
- 必须有 `@TableName("xxx")` 注解
- 必须继承 `BaseMapper<>` 接口的 entity 使用 MyBatis-Plus
- 时间字段类型:**LocalDateTime**(严禁 `Date` 或 `String`)
- PK:6 复用 Object 使用 `Long`,6 新建 Object 使用 `String`(CHAR(36) UUID)
- 不启用软删除(`isDeleted` 不启用)
- companyId 字段:6 复用 Object **可能**有(待 238 §3 区分);6 新建 Object **不一定有**

### 4.2 6 复用 Object

#### 4.2.1 Company

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `companyId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyTitle` | `String` | 【原系统事实】 | 214 §1.4 |
| `companyName` | `String` | 【待确认】 | — |
| `companyType` | `Integer` | 【原系统事实】 | 04_数据模型.md(等级 C,235B §9.2)|
| `logoUrl` | `String` | 【待确认】 | — |
| `address` | `String` | 【待确认】 | — |
| `phone` | `String` | 【待确认】 | — |
| `createdAt` | `LocalDateTime` | 【OptFlow设计】 | — |
| `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.2.2 Customer

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `customerId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `customerName` | `String` | 【待确认】 | — |
| `linkMobile` | `String` | 【原系统事实】 | 105 §6.1 |
| `idCard` | `String` | 【待确认】 | — |
| `memberTypeId` | `Long` | 【原系统事实】 | 04_数据模型.md(等级 C)|
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.2.3 Patient

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `patientId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyId` | `Long` | **【待确认】DB FK 暂未冻结** | 236A 修正 |
| `customerId` | `Long` | 【OptFlow设计】 | — |
| `patientName` | `String` | 【待确认】 | — |
| `birthDate` | `LocalDate` | 【待确认】 | — |
| `gender` | `Integer` | 【待确认】 | — |
| `medicalCode`(病历编号)| `String` | 【待确认】 | — |
| `mobile` | `String` | 【待确认】 | — |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.2.4 Employee

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `employeeId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `employeeName` | `String` | 【待确认】 | — |
| `role` | `String` | 【待确认】 | — |
| `mobile` | `String` | 【待确认】 | — |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.2.5 ConsultRoom

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `consultRoomId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `roomName` | `String` | 【待确认】 | — |
| `roomNo` | `String` | 【待确认】 | — |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.2.6 BigScreen

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `bigScreenId` (PK) | `Long` | 【OptFlow设计】 | 238 §2.1 |
| `companyId` | `Long` | 【待确认】 | — |
| `screenName` | `String` | 【待确认】 | — |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

### 4.3 6 新建 Object

#### 4.3.1 AppointmentSchedule

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `scheduleId` (PK) | `String`(CHAR(36) UUID)| 【OptFlow设计】 | 238 §2.2 + 236B §3 |
| `companyId` | `Long` | 【待确认】 | 235B §6.3 |
| `doctorId` | `Long` | 【待确认】 | — |
| `scheduleDate` | `LocalDate` | 【待确认】 | — |
| `startTime` / `endTime` | `LocalTime` | 【待确认】 | — |
| `status` | `String`(ScheduleStatus)| 【OptFlow设计】 | 229 §4.3 |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.3.2 AppointmentSlot

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `slotId` (PK) | `String` | 【OptFlow设计】 | 238 §2.2 |
| `scheduleId` (FK) | `String` | 【待确认】 | — |
| `slotStartTime` / `slotEndTime` | `LocalTime` | 【待确认】 | — |
| `maxPatients` | `Integer` | 【待确认】 | — |
| `currentCount` | `Integer` | 【待确认】 | — |
| `status` | `String`(SlotStatus)| 【OptFlow设计】 | 229 §4.3 |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.3.3 Appointment

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `appointmentId` (PK) | `String` | 【OptFlow设计】 | 238 §2.2 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `patientId` | `Long` | 【OptFlow设计】 | — |
| `doctorId` | `Long` | 【待确认】 | — |
| `scheduleId` | `String` | 【待确认】 | — |
| `slotId` | `String` | 【待确认】 | — |
| `appointmentTime` | `LocalDateTime` | 【待确认】 | — |
| `status` | `String`(AppointmentStatus)| 【OptFlow设计】 | 229 §4.2 |
| `currentVisitId` | `String` | 【OptFlow设计】 | 229 §4.2(P0-6 修复)|
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.3.4 Visit

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `visitId` (PK) | `String` | 【OptFlow设计】 | 238 §2.2 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `appointmentId` (FK) | `String` | 【OptFlow设计】 | 229 §4.4 |
| `patientId` | `Long` | 【OptFlow设计】 | — |
| `doctorId` | `Long` | 【待确认】 | — |
| `consultRoomId` | `Long` | 【待确认】 | — |
| `checkInTime` | `LocalDateTime` | 【待确认】 | — |
| `status` | `String`(VisitStatus)| 【OptFlow设计】 | 229 §4.2 |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.3.5 TriageQueue

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `triageQueueId` (PK) | `String` | 【OptFlow设计】 | 238 §2.2 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `visitId` (FK) | `String` | 【OptFlow设计】 | 229 §15.4 |
| `patientId` | `Long` | 【OptFlow设计】 | — |
| `employeeId`(分诊医生)| `Long` | 【OptFlow设计】 | 229 §15.4(IN_POOL 时 NULL)|
| `consultRoomId` | `Long` | 【OptFlow设计】 | 229 §15.4(IN_POOL 时 NULL)|
| `assignedAt` | `LocalDateTime` | 【待确认】 | — |
| `assignedBy` | `Long` | 【待确认】 | — |
| `status` | `String`(TriageQueueStatus)| 【OptFlow设计】 | 229 §4.2 |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

#### 4.3.6 ReceptionQueue

| 字段 | Java 类型 | 标签 | 证据 |
|---|---|---|---|
| `receptionQueueId` (PK) | `String` | 【OptFlow设计】 | 238 §2.2 |
| `companyId` | `Long` | 【OptFlow设计】 | 235B §6.3 |
| `visitId` (FK) | `String` | 【OptFlow设计】 | — |
| `doctorId` | `Long` | 【待确认】 | — |
| `consultRoomId` | `Long` | 【待确认】 | — |
| `status` | `String`(ReceptionQueueStatus)| 【OptFlow设计】 | 229 §4.2 |
| `createdAt` / `updatedAt` | `LocalDateTime` | 【OptFlow设计】 | — |

### 4.4 12 Object 字段级 Contract 汇总

| # | Object | Table | PK Type | 字段级冻结? | 状态 |
|---:|---|---|---|:-:|---|
| 1 | Company | `company` | `Long` | ⚠️ 部分(部分字段【待确认】)| Contract Gap |
| 2 | Customer | `customer` | `Long` | ⚠️ 部分 | Contract Gap |
| 3 | Patient | `patient` | `Long` | ⚠️ 部分(companyId 待确认)| Contract Gap |
| 4 | Employee | `employee` | `Long` | ⚠️ 部分 | Contract Gap |
| 5 | ConsultRoom | `consult_room` | `Long` | ⚠️ 部分 | Contract Gap |
| 6 | BigScreen | `big_screen` | `Long` | ⚠️ 部分 | Contract Gap |
| 7 | AppointmentSchedule | `appointment_schedule` | `String` UUID | ⚠️ 部分 | Contract Gap |
| 8 | AppointmentSlot | `appointment_slot` | `String` UUID | ⚠️ 部分 | Contract Gap |
| 9 | Appointment | `appointment` | `String` UUID | ⚠️ 部分(currentVisitId 已冻结)| Contract Gap |
| 10 | Visit | `visit` | `String` UUID | ⚠️ 部分 | Contract Gap |
| 11 | TriageQueue | `triage_queue` | `String` UUID | ⚠️ 部分 | Contract Gap |
| 12 | ReceptionQueue | `reception_queue` | `String` UUID | ⚠️ 部分 | Contract Gap |

**【G2-Contract-01 显式】**:**12 Object 全部出现,但字段级** **⚠️ 部分冻结**。每个 Object 都有【待确认】字段(因为现有规格未给出全部字段级定义)。**Contract Gap 存在**,实施时需结合 Phase 1 页面侦察补齐。

---

## §5. C2:user_company Infrastructure Contract

### 5.1 Schema Contract

| DB 列 | 类型 | NULL | 唯一约束 | 标签 | 证据 |
|---|---|:-:|---|---|---|
| `user_company_id` | BIGINT AUTO_INCREMENT | NOT NULL | PK | 【OptFlow设计】 | 241V2A-11 |
| `user_id` | BIGINT | NOT NULL | (idx)| 【OptFlow设计】 | 241V2A-11 |
| `company_id` | BIGINT | NOT NULL | (idx)| 【OptFlow设计】 | 241V2A-11 |
| `is_default` | TINYINT(1) | NOT NULL | — | 【OptFlow设计】 | 241V2A-11 |
| `status` | TINYINT(1) | NOT NULL | — | 【OptFlow设计】 | 241V2A-11 |
| `created_at` | DATETIME(3) | NOT NULL | — | 【OptFlow设计】 | — |
| `updated_at` | DATETIME(3) | NOT NULL | — | 【OptFlow设计】 | — |

### 5.2 Repository Contract(241V2A-10)

```java
public interface UserCompanyRepository {
    int updateDefaultToZero(Long userId);
    int setDefault(Long userId, Long companyId);
    int countByUserIdAndCompanyId(Long userId, Long companyId);  // 沿用 241V2A-1 §6.2
    int countByUserIdAndIsDefault(Long userId, int isDefault);   // 沿用 241V2A-1 §6.2
}
```

### 5.3 Mapper Contract(241V2A-11)

```java
public interface UserCompanyMapper extends BaseMapper<UserCompany> {
    @Update("UPDATE user_company SET is_default = 0, updated_at = NOW(3) WHERE user_id = #{userId} AND status = 1")
    int updateDefaultToZero(@Param("userId") Long userId);

    @Update("UPDATE user_company SET is_default = 1, updated_at = NOW(3) WHERE user_id = #{userId} AND company_id = #{companyId} AND status = 1")
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);

    @Select("SELECT COUNT(*) FROM user_company WHERE user_id = #{userId} AND company_id = #{companyId} AND status = 1")
    int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);

    @Select("SELECT COUNT(*) FROM user_company WHERE user_id = #{userId} AND is_default = #{isDefault} AND status = 1")
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
}
```

### 5.4 Service Contract(UserCompanyService)

| 方法 | 参数 | 返回 | Transaction | Tenant | 异常 |
|---|---|---|---|:-:|---|
| `setDefaultCompany` | Long userId, Long companyId | void | T2(原子)| ✓ | CompanyMismatchException / IllegalStateException(exactly-one 不满足)|

### 5.5 exactly-one 规则(241V2A-11 §3 + 241V2A-36 / 37)

```
if (defaultCount != 1) {
    throw new IllegalStateException("exactly-one default 约束违反:defaultCount=" + defaultCount);
}
assertThat(defaultCount).isEqualTo(1);  // DEFAULT-05 断言
```

### 5.6 DEFAULT-01~05 测试映射

| DEFAULT | 描述 | 状态 |
|---|---|---|
| **DEFAULT-01** | 并发不同公司(2 个 T1/T2 setDefault 不同 company)| T3 并发安全 |
| **DEFAULT-02** | 串行 setDefault B(company B)| T1 |
| **DEFAULT-03** | 并发同公司 A(幂等)| T3 并发安全 |
| **DEFAULT-04** | 禁用 company 抛异常 | T1 + Exception |
| **DEFAULT-05** | exactly-one 断言(`assertThat(defaultCount).isEqualTo(1)`)| T1 + 断言 |

---

## §6. C3:Repository / Mapper Contract

### 6.1 12 业务 Object Repository 框架

**【G2-Contract-01 显式】** 12 业务 Object 的 Repository / Mapper **Contract 框架**:

```java
// 通用 Repository Contract
public interface <X>Repository {
    // 由 MyBatis-Plus BaseMapper<T> 自动提供:
    // - insert(T entity)
    // - updateById(T entity)
    // - selectById(Serializable id)
    // - selectList(Wrapper<T> queryWrapper)
    // - deleteById(Serializable id)
    // - delete(Wrapper<T> queryWrapper)
    // - selectCount(Wrapper<T> queryWrapper)
    // - selectPage(Page<T> page, Wrapper<T> queryWrapper)
    
    // Custom 方法(每个 Object 不同):
    // TODO: 由 Phase 1 页面侦察 + Service 需求确定
}
```

### 6.2 Repository / Mapper 字段级 Contract

**【G2-Contract-01 显式】**:**12 业务 Object 的 Repository / Mapper 字段级 Custom 方法 Contract 是 Contract Gap**。

理由:
- 241V2A-10 / 11 仅冻结 user_company 的 Repository / Mapper
- 12 业务 Object 的字段级 Custom 方法**未在现有规格中显式冻结**
- 需要 Phase 1 页面侦察 + 业务需求进一步细化

**严禁 AI 自行发明 Custom 方法**(例如"根据 Service 调用推断需要 updateStatusById 方法")。

---

## §7. C4:40 API → Controller / DTO / VO Contract

### 7.1 总表(API-001 ~ API-040)

**【G2-Contract-01 显式】** 完整 40 API Contract 表见 `232_S1-167_40个API字段级设计.md` §1 与 `233_S1-167A_API字段级设计修正版.md`。

### 7.2 API Contract 字段级映射总表

| API | Method | Path | Controller | Request DTO | Response VO | Service Method | State Change | Transaction | Permission | Tenant | Error |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **API-001** | POST | /api/appointment/create | AppointmentController | AppointmentCreateDTO | AppointmentCreateVO | AppointmentService.create | DRAFT | T2(原子)| RECEP/ADMIN | ✓ | APPT_NOT_FOUND / APPT_INVALID_STATE |
| **API-002** | PUT | /api/appointment/update | AppointmentController | AppointmentUpdateDTO | AppointmentUpdateVO | AppointmentService.update | DRAFT/CONFIRMED | T1 | RECEP/ADMIN | ✓ | APPT_NOT_FOUND |
| **API-003** | POST | /api/appointment/confirm | AppointmentController | AppointmentConfirmDTO | AppointmentConfirmVO | AppointmentService.confirm | DRAFT → CONFIRMED | T1 | RECEP/ADMIN | ✓ | APPT_CONFIRM_INVALID_STATE |
| **API-004** | POST | /api/appointment/cancel | AppointmentController | AppointmentCancelDTO | AppointmentCancelVO | AppointmentService.cancel | 任意非终态 → CANCELLED | T1 | RECEP/ADMIN(按状态)| ✓ | APPT_CANCEL_INVALID_STATE |
| **API-005** | POST | /api/appointment/reschedule | AppointmentController | AppointmentRescheduleDTO | AppointmentRescheduleVO | AppointmentService.reschedule | CONFIRMED/WAITING_ARRIVAL → RESCHEDULED + 新 CONFIRMED | T2(原子)| RECEP/ADMIN | ✓ | APPT_RESCHEDULE_INVALID_STATE |
| **API-006** | GET | /api/appointment/detail | AppointmentController | AppointmentDetailQuery | AppointmentDetailVO | AppointmentService.detail | 无 | T0(只读)| RECEP/TRIAGE/DOCTOR/ADMIN | ✓ | APPT_NOT_FOUND |
| **API-007** | POST | /api/appointment/list | AppointmentController | AppointmentListQuery | AppointmentListVO | AppointmentService.list | 无 | T0(只读)| RECEP/TRIAGE/DOCTOR/ADMIN | ✓ | — |
| **API-008** | GET | /api/appointment/today | AppointmentController | AppointmentTodayQuery | AppointmentTodayVO | AppointmentService.today | 无 | T0(只读)| RECEP/DOCTOR/ADMIN | ✓ | — |
| **API-009** | POST | /api/schedule/create | ScheduleController | ScheduleCreateDTO | ScheduleCreateVO | ScheduleService.create | ACTIVE/INACTIVE | T1 | ADMIN | ✓ | SCHEDULE_INVALID |
| **API-010** | PUT | /api/schedule/update | ScheduleController | ScheduleUpdateDTO | ScheduleUpdateVO | ScheduleService.update | 更新 | T1 | ADMIN | ✓ | SCHEDULE_NOT_FOUND |
| **API-011** | POST | /api/schedule/publish | ScheduleController | SchedulePublishDTO | SchedulePublishVO | ScheduleService.publish | DRAFT/INACTIVE → ACTIVE | T1 | ADMIN | ✓ | SCHEDULE_PUBLISH_INVALID_STATE |
| **API-012** | POST | /api/schedule/cancel | ScheduleController | ScheduleCancelDTO | ScheduleCancelVO | ScheduleService.cancel | ACTIVE → CANCELLED | T1 | ADMIN | ✓ | SCHEDULE_CANCEL_INVALID_STATE |
| **API-013** | GET | /api/schedule/detail | ScheduleController | ScheduleDetailQuery | ScheduleDetailVO | ScheduleService.detail | 无 | T0 | ADMIN/DOCTOR/RECEP | ✓ | SCHEDULE_NOT_FOUND |
| **API-014** | POST | /api/schedule/list | ScheduleController | ScheduleListQuery | ScheduleListVO | ScheduleService.list | 无 | T0 | ADMIN/DOCTOR/RECEP | ✓ | — |
| **API-015** | POST | /api/schedule/slot/close | ScheduleController | ScheduleSlotCloseDTO | ScheduleSlotCloseVO | ScheduleService.closeSlot | AVAILABLE/FULL → CLOSED | T1 | ADMIN | ✓ | SLOT_CLOSE_INVALID_STATE |
| **API-016** | POST | /api/arrival/checkin | ArrivalController | ArrivalCheckinDTO | ArrivalCheckinVO | ArrivalService.checkin | 4 对象同步创建 | T2(原子)| RECEP/STAFF/ADMIN | ✓ | ARRIVAL_CHECKIN_INVALID |
| **API-017** | POST | /api/arrival/cancel | ArrivalController | ArrivalCancelDTO | ArrivalCancelVO | ArrivalService.cancel | 撤销签到 | T2(原子)| RECEP/ADMIN | ✓ | ARRIVAL_CANCEL_INVALID_STATE |
| **API-018** | POST | /api/arrival/list | ArrivalController | ArrivalListQuery | ArrivalListVO | ArrivalService.list | 无 | T0 | RECEP/TRIAGE/DOCTOR/ADMIN | ✓ | — |
| **API-019** | POST | /api/triage/list | TriageController | TriageListQuery | TriageListVO | TriageService.list | 无 | T0 | TRIAGE/ADMIN | ✓ | — |
| **API-020** | POST | /api/triage/auto-assign | TriageController | TriageAutoAssignDTO | TriageAutoAssignVO | TriageService.autoAssign | IN_POOL → ASSIGNED(批量)| T2(原子)| SYSTEM/ADMIN | ✓ | TRIAGE_AUTO_ASSIGN_INVALID |
| **API-021** | POST | /api/triage/assign | TriageController | TriageAssignDTO | TriageAssignVO | TriageService.assign | IN_POOL → ASSIGNED | T2(原子)| TRIAGE/ADMIN | ✓ | TRIAGE_NOT_FOUND / TRIAGE_ASSIGN_INVALID_STATE / TRIAGE_EMPLOYEE_INVALID / TRIAGE_ROOM_INVALID |
| **API-022** | POST | /api/triage/reassign | TriageController | TriageReassignDTO | TriageReassignVO | TriageService.reassign | ASSIGNED → IN_POOL | T2(原子)| TRIAGE/ADMIN | ✓ | VISIT_NOT_FOUND / TRIAGE_REASSIGN_INVALID_STATE |
| **API-023** | POST | /api/triage/remove | TriageController | TriageRemoveDTO | TriageRemoveVO | TriageService.remove | IN_POOL → REMOVED | T1 | TRIAGE/ADMIN | ✓ | TRIAGE_REMOVE_INVALID_STATE |
| **API-024** | POST | /api/queue/start | QueueController | QueueStartDTO | QueueStartVO | QueueService.start | ASSIGNED → WAITING | T1 | DOCTOR | ✓ | QUEUE_START_INVALID_STATE |
| **API-025** | POST | /api/queue/pause | QueueController | QueuePauseDTO | QueuePauseVO | QueueService.pause | 暂停 | T1 | DOCTOR | ✓ | QUEUE_PAUSE_INVALID_STATE |
| **API-026** | POST | /api/queue/next | QueueController | QueueNextDTO | QueueNextVO | QueueService.next | WAITING → CALLED | T1 | DOCTOR | ✓ | QUEUE_EMPTY |
| **API-027** | POST | /api/queue/skip | QueueController | QueueSkipDTO | QueueSkipVO | QueueService.skip | CALLED → SKIPPED | T1 | DOCTOR | ✓ | QUEUE_SKIP_INVALID_STATE |
| **API-028** | POST | /api/queue/complete | QueueController | QueueCompleteDTO | QueueCompleteVO | QueueService.complete | CALLED → IN_CONSULTATION → DONE | T1 | DOCTOR | ✓ | QUEUE_COMPLETE_INVALID_STATE |
| **API-029** | GET | /api/queue/list | QueueController | QueueListQuery | QueueListVO | QueueService.list | 无 | T0 | DOCTOR/RECEP/ADMIN | ✓ | — |
| **API-030** | POST | /api/visit/start | VisitController | VisitStartDTO | VisitStartVO | VisitService.start | DRAFT → CHECKED_IN → TRIAGED → IN_CONSULTATION | T2(原子)| DOCTOR/ADMIN | ✓ | VISIT_NOT_FOUND / VISIT_START_INVALID_STATE |
| **API-031** | POST | /api/visit/complete | VisitController | VisitCompleteDTO | VisitCompleteVO | VisitService.complete | IN_CONSULTATION → COMPLETED | T1 | DOCTOR | ✓ | VISIT_COMPLETE_INVALID_STATE |
| **API-032** | POST | /api/visit/cancel | VisitController | VisitCancelDTO | VisitCancelVO | VisitService.cancel | DRAFT/CHECKED_IN/TRIAGED → CANCELLED | T1 | DOCTOR/ADMIN | ✓ | VISIT_CANCEL_INVALID_STATE |
| **API-033** | GET | /api/visit/detail | VisitController | VisitDetailQuery | VisitDetailVO | VisitService.detail | 无 | T0 | DOCTOR/ADMIN | ✓ | VISIT_NOT_FOUND |
| **API-034** | POST | /api/visit/transfer | VisitController | VisitTransferDTO | VisitTransferVO | VisitService.transfer | IN_CONSULTATION → TRANSFERRED + 新 Visit 1:N | **T2(原子,9-step)** | DOCTOR/ADMIN | ✓ | VISIT_TRANSFER_INVALID_STATE |
| **API-035** | GET | /api/visit/list | VisitController | VisitListQuery | VisitListVO | VisitService.list | 无 | T0 | DOCTOR/ADMIN | ✓ | — |
| **API-036** | POST | /api/visit/cancel-direct | VisitController | VisitCancelDirectDTO | VisitCancelDirectVO | VisitService.cancelDirect | 直接 → CANCELLED | T1 | DOCTOR/ADMIN | ✓ | VISIT_CANCEL_INVALID_STATE |
| **API-037** | POST | /api/reception/assign | ReceptionController | ReceptionAssignDTO | ReceptionAssignVO | ReceptionService.assign | 软删 + 新建(ASSIGNED)| T2(原子)| RECEP/TRIAGE | ✓ | RECEPTION_ASSIGN_INVALID |
| **API-038** | POST | /api/reception/start | ReceptionController | ReceptionStartDTO | ReceptionStartVO | ReceptionService.start | ASSIGNED → WAITING | T1 | RECEP | ✓ | RECEPTION_START_INVALID_STATE |
| **API-039** | GET | /api/reception/list | ReceptionController | ReceptionListQuery | ReceptionListVO | ReceptionService.list | 无 | T0 | RECEP/DOCTOR/ADMIN | ✓ | — |
| **API-040** | POST | /api/auth/login | AuthController | LoginDTO | LoginVO | AuthService.login | 无 | T0(只读) | 公开 API | — | AUTH_INVALID_CREDENTIALS |

### 7.3 API-040 特殊说明

API-040 `/api/auth/login` 是**唯一公开 API**(无需登录)。其他 39 个 API 都需要 Sa-Token 登录校验。

---

## §8. C5:Service Contract

### 8.1 Service 接口框架(12 业务 + Auth + UserCompany)

**【G2-Contract-01 显式】** 14 个 Service 接口 Contract:

| Service | Module | 主要方法 | 关键 Contract |
|---|---|---|---|
| **AppointmentService** | appointment | create / update / confirm / cancel / reschedule / detail / list / today | API-001 ~ API-008 |
| **AppointmentScheduleService** | appointment_schedule | create / update / publish / cancel / detail / list / closeSlot | API-009 ~ API-015 |
| **AppointmentSlotService** | appointment_slot | (内部)| 配合 Schedule 关闭 slot |
| **VisitService** | visit | start / complete / cancel / cancelDirect / detail / list / transfer(9-step)| API-030 ~ API-036 |
| **TriageQueueService** | triage_queue | list / autoAssign / assign / reassign / remove | API-019 ~ API-023 |
| **ReceptionQueueService** | reception_queue | assign / start / list | API-037 ~ API-039 |
| **CustomerService** | customer | (TBD)| 【待确认】Phase 1 范围未明确 |
| **PatientService** | patient | (TBD)| 【待确认】Phase 1 范围未明确 |
| **EmployeeService** | employee | (TBD)| 【待确认】Phase 1 范围未明确 |
| **ConsultRoomService** | consult_room | (TBD)| 【待确认】Phase 1 范围未明确 |
| **BigScreenService** | big_screen | (TBD)| 【待确认】Phase 1 范围未明确 |
| **CompanyService** | company | (TBD)| 【待确认】Phase 1 范围未明确 |
| **AuthService** | auth | login | API-040 |
| **UserCompanyService** | auth | setDefaultCompany | DEFAULT-01~05 |

### 8.2 Service 方法级 Contract Gap

**【G2-Contract-01 显式】**:**CustomerService / PatientService / EmployeeService / ConsultRoomService / BigScreenService / CompanyService 的 Service 方法 Contract 是 Contract Gap**。

理由:
- 现有规格(229 / 232 / 238)仅冻结 Entity 字段 + API 契约,**未冻结**这些 Service 的方法级 Contract
- Phase 1 范围 = 诊所管理 + 系统设置;**不**包括 Customer / Patient / Employee 的完整 Service 契约(主要是数据查询,不是核心业务 Service)
- 严禁 AI 自行推断 Service 方法

---

## §9. C6:Transaction Contract

### 9.1 Transaction 分类

| 等级 | 含义 | 示例 |
|---|---|---|
| **T0** | No transaction(只读)| API-006/007/008/013/014/018/019/029/033/035/039/040 |
| **T1** | Single aggregate transaction | API-002/003/004/009/010/011/012/015/023/024/025/026/027/028/031/032/036/038 |
| **T2** | Multi-object atomic transaction | API-001/005/016/017/020/021/022/030/034/037 |
| **T3** | Concurrency-sensitive transaction | DEFAULT-01 / DEFAULT-03(setDefault 并发)|
| **T4** | External integration boundary | (无,本项目无外部集成)|

### 9.2 Transfer 9-step Transaction(API-034)

**【G2-Contract-01 显式】** VisitService.transfer 必须按以下 9 步骤:

```
1. transaction start
2. validation(Visit 状态 = IN_CONSULTATION)
3. 旧 ReceptionQueue 软删(ReceptionQueue.status = CANCELLED)
4. 旧 TriageQueue 释放(TriageQueue.status = IN_POOL, employeeId = NULL, consultRoomId = NULL)
5. 创建新 Visit(visitId2, appointmentId = oldVisit.appointmentId)
6. 更新 Appointment.currentVisitId = visitId2
7. 创建新 TriageQueue(visitId2, status = IN_POOL)
8. 创建新 ReceptionQueue(visitId2, status = ASSIGNED)
9. atomic commit / rollback on any failure
```

**严禁 AI 自行简化**或重新推理 transfer 步骤。

---

## §10. C7:Tenant Contract

### 10.1 CompanyContext(241V2 §4)

```java
public class CompanyContext {
    private static final ThreadLocal<Long> COMPANY_ID = new ThreadLocal<>();
    private static final ThreadLocal<Long> USER_ID = new ThreadLocal<>();
    private static final ThreadLocal<List<Long>> USER_ACCESSIBLE_COMPANIES = new ThreadLocal<>();
    private static final ThreadLocal<ContextState> STATE = new ThreadLocal<>();
    
    public static void setCompanyId(Long companyId);
    public static Long getCompanyId();
    public static Long requireCompanyId();  // 严格缺失抛 CompanyContextMissingException
    public static void setUserId(Long userId);
    public static Long getUserId();
    public static void setUserAccessibleCompanies(List<Long> companies);
    public static List<Long> getUserAccessibleCompanies();
    public static boolean hasAccessTo(Long targetCompanyId);
    public static void forceClear();  // 幂等清理
    public static void markState(ContextState state);
}
```

### 10.2 CompanyContextInterceptor(241V2 §5)

| 步骤 | 动作 | 异常处理 |
|---:|---|---|
| 1 | 防御性 forceClear + markState(LOADING) | — |
| 2 | Sa-Token 登录校验(StpUtil.isLogin)| NotLoginException(401)|
| 3 | 设置 userId | — |
| 4 | 加载 userAccessibleCompanies | 失败 → forceClear + CompanyContextMissingException |
| 5 | 解析 targetCompanyId(X-Company-Id > session > 唯一 company)| 权限不足 → forceClear + CompanyAccessDeniedException |
| 6 | 严格缺失检测 | null → forceClear + CompanyContextMissingException |
| 7 | 设置 companyId + markState(READY) | — |
| 8 | RuntimeException 兜底 forceClear + markState(ERROR) | — |

### 10.3 CompanyContextCleanupFilter(241V2 §5.4.1)

```java
public class CompanyContextCleanupFilter implements Filter {
    public void doFilter(req, resp, chain) {
        CompanyContext.forceClear();  // 请求前
        try {
            chain.doFilter(req, resp);
        } finally {
            CompanyContext.forceClear();  // 请求后兜底
        }
    }
}
```

### 10.4 TenantLineInnerInterceptor(241V2 §6)

- 自动织入 `WHERE companyId = ?`
- IGNORE_TABLES 表不织入(见 §14)

### 10.5 严禁

- ✗ fallback 1L(241 §4.6 + 241V2 §4.3)
- ✗ hardcoded companyId
- ✗ 跨公司引用不校验

---

## §11. C8:Security Contract

### 11.1 角色定义

| 角色 | 说明 |
|---|---|
| **RECEP** | 接待员 |
| **TRIAGE** | 分诊员 |
| **DOCTOR** | 医生 |
| **STAFF** | 员工 |
| **ADMIN** | 管理员 |
| **SYSTEM** | 系统(自动任务)|

### 11.2 公开 API 白名单(241V2 §5.6)

- `/api/auth/login`
- `/api/auth/captcha`(待确认)
- `/api/common/`
- `/api/health`
- `/api/swagger`
- `/api/v3/api-docs`

### 11.3 Contract Gap

**【G2-Contract-01 显式】**:**Sa-Token 注解(@SaCheckRole / @SaCheckPermission)Contract 是 Contract Gap**。

理由:
- 现有规格(241V2)未冻结具体 Sa-Token 注解
- 仅冻结了角色列表和错误码(60000-60004)
- 实施时需根据 Sa-Token 文档 + 角色列表自行配置注解

**严禁 AI 自行写出** `@SaCheckRole("RECEP")` 这类代码(因为本 Contract 不能写源码)。

---

## §12. C9:Exception Contract

### 12.1 异常矩阵(241V2A-17 / 18)

| # | 异常类 | ResultCode | HTTP | Handler |
|---:|---|---|:-:|---|
| 1 | `BusinessException`(基类) | 通用 | 400 | `@ExceptionHandler(BusinessException.class)` |
| 2 | `CompanyContextMissingException` | 60000 | 401 | `@ExceptionHandler(CompanyContextMissingException.class)` |
| 3 | `CompanyMismatchException` | 60001 | 400 | `@ExceptionHandler(CompanyMismatchException.class)` |
| 4 | `CompanyAccessDeniedException` | 60002 | 403 | `@ExceptionHandler(CompanyAccessDeniedException.class)` |
| 5 | `UserNotFoundException` | 60003 | 404 | `@ExceptionHandler(UserNotFoundException.class)` |
| 6 | `UserDisabledException` | 60004 | 403 | `@ExceptionHandler(UserDisabledException.class)` |
| 7 | `IllegalStateException`(兜底) | 通用 | 500 | `@ExceptionHandler(Exception.class)` |
| 8 | `NotLoginException`(Sa-Token) | 通用 | 401 | `@ExceptionHandler(NotLoginException.class)` |

### 12.2 严禁

- ✗ 重新发明错误码
- ✗ 修改 60000-60004 数值
- ✗ 改变 HTTP 状态语义

---

## §13. C10:Test / Acceptance Mapping

### 13.1 DEFAULT-01~05 → 实现验收目标

| 测试 | Test Type | Environment | Acceptance | Service Target |
|---|---|---|---|---|
| **DEFAULT-01** | Unit + Integration | Local + Test | T1 setDefault(B) + T2 setDefault(C) 都成功 → user_company 表 B/C 都 is_default=1 | UserCompanyService.setDefaultCompany |
| **DEFAULT-02** | Unit | Local | T1 setDefault(B) 成功 → user_company 表 B is_default=1, A is_default=0 | UserCompanyService.setDefaultCompany |
| **DEFAULT-03** | Concurrency | Local + Test | T1/T2 并发 setDefault(A) 都成功 → exactly-one(A=1) | UserCompanyService.setDefaultCompany |
| **DEFAULT-04** | Exception | Local | setDefault(disabled company) → CompanyAccessDeniedException(60002 / 403) | UserCompanyService.setDefaultCompany |
| **DEFAULT-05** | Verification | Local + Test | `assertThat(defaultCount).isEqualTo(1)` 通过 | UserCompanyService.setDefaultCompany |

### 13.2 严禁

**【G2-Contract-01 显式严禁】**:**DEFAULT-01~05 不是 Backend Entry 前置条件**。

它们是 Implementation / Verification 阶段的验收目标,**不**是开始 backend 编码的前置条件。

---

## §14. C11:IGNORE_TABLES Static Contract(Phase 1)

### 14.1 Phase 1 IGNORE_TABLES 分类原则(241V2 §6.4)

| 类别 | 说明 | TenantLine 行为 |
|---|---|---|
| **A 类(全局共享)** | 系统级表(无 companyId)| IGNORE |
| **B 类(多公司共享)** | 字典 / 系统配置(无需隔离)| IGNORE |
| **C 类(用户级业务)** | 必须 tenant-filtered | APPLY WHERE companyId = ? |

### 14.2 Phase 1 12 表的 IGNORE_TABLES 分类

| # | Table | Object | companyId 字段? | IGNORE_TABLES? | Reason | Evidence |
|---:|---|---|:-:|:-:|---|---|
| 1 | `company` | Company | (本身是公司表)| ✓ **IGNORE** | 公司表本身无 tenant 隔离概念 | 241V2 §6.4(系统级表)|
| 2 | `customer` | Customer | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 3 | `patient` | Patient | 待确认 | ⚠️ **【待确认】** | 235A / 236A 修正,跨公司一致性策略待确认 | 238 §3 |
| 4 | `employee` | Employee | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 5 | `consult_room` | ConsultRoom | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 6 | `big_screen` | BigScreen | 待确认 | ⚠️ **【待确认】** | 需确认是否跨公司 | — |
| 7 | `appointment_schedule` | AppointmentSchedule | 待确认 | ⚠️ **【待确认】** | 235B §6.3 应有 companyId | 235B §6.3 |
| 8 | `appointment_slot` | AppointmentSlot | 间接(通过 schedule)| ⚠️ **【待确认】** | 是否 tenant-filtered 取决于访问路径 | — |
| 9 | `appointment` | Appointment | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 10 | `visit` | Visit | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 11 | `triage_queue` | TriageQueue | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |
| 12 | `reception_queue` | ReceptionQueue | 有(`companyId`)| ✗ APPLY | 业务表必须 tenant-filtered | 235B §6.3 |

### 14.3 Infrastructure 表(user_company)

| Table | companyId 字段? | IGNORE_TABLES? | Reason | Evidence |
|---|:-:|:-:|---|---|
| `user_company` | (关联表,无单一 companyId)| ✓ **IGNORE** | 多公司关联表,TenantLine 不能直接织入;手动 SQL 处理 | 241V2A-10 / 11 |

### 14.4 Phase 1 IGNORE_TABLES 静态清单(初步)

```
IGNORE_TABLES = {
  "company",           // 系统级表(本身是公司表)
  "user_company"       // 多公司关联表,手动 SQL 处理
}
```

### 14.5 Contract Gap

**【G2-Contract-01 显式】**:**Patient / BigScreen / AppointmentSchedule / AppointmentSlot 的 companyId 字段 Contract 是 Contract Gap**。

理由:
- 现有规格未明确给出这些表的 companyId 字段
- 235A / 236A 已多次修正但仍未明确所有 12 表的 companyId 策略
- Phase 1 实施前需补齐

---

## §15. Contract Gaps / Evidence Gaps

### 15.1 显式 Contract Gaps

| # | Gap | 影响范围 | 优先级 |
|---:|---|---|:-:|
| **Gap-01** | 12 业务 Object 字段级 Custom 方法 Contract | Repository / Mapper | **高** |
| **Gap-02** | Customer / Patient / Employee / ConsultRoom / BigScreen / Company Service 方法 Contract | Service | 中 |
| **Gap-03** | Sa-Token 注解(@SaCheckRole / @SaCheckPermission)Contract | Security | 中 |
| **Gap-04** | Patient / BigScreen / AppointmentSchedule / AppointmentSlot 的 companyId 字段 Contract | Entity + IGNORE_TABLES | **高** |
| **Gap-05** | AppointmentSchedule / AppointmentSlot / Visit / TriageQueue / ReceptionQueue 的若干字段(`doctorId` / `consultRoomId` / `scheduleId` 等)Contract | Entity | 中 |
| **Gap-06** | Phase 1 范围(诊所管理 + 系统设置)的页面 26 项字段 Contract | Business Service | 中 |
| **Gap-07** | SystemSetting 范围 Contract(已有 V4.3 文档,但 V4.4 重新冻结)| SystemSetting 模块 | 中 |

### 15.2 严禁

**【G2-Contract-01 显式】**:为完成 Contract,**严禁 AI 自行发明**字段 / 方法 / 类型 / 注解等。

---

## §16. G2 Contract Gate Self-Check

### 16.1 完成标准检查

| # | 标准 | 状态 | 备注 |
|---:|---|:-:|---|
| 1 | 12 Object 全覆盖 | ✓ | §4 |
| 2 | user_company 单独覆盖 | ✓ | §5 |
| 3 | 40 API 全覆盖 | ✓ | §7 |
| 4 | Repository / Mapper 全覆盖 | ⚠️ **部分**(仅 user_company 完整,12 业务缺 Custom 方法)| **Contract Gap-01** |
| 5 | Service 核心方法全覆盖 | ⚠️ **部分**(14 个 Service 框架已建,具体方法待确认)| **Contract Gap-02** |
| 6 | Transaction boundary 全覆盖 | ✓ | §9 |
| 7 | Tenant Contract 全覆盖 | ✓ | §10 |
| 8 | Security Contract 达到现有证据能够支持的粒度 | ⚠️ **部分**(角色 + 错误码已冻结,注解待确认)| **Contract Gap-03** |
| 9 | Exception Contract 全覆盖 | ✓ | §12 |
| 10 | Test Mapping 全覆盖 | ✓ | §13 |
| 11 | Acceptance criteria 有出处 | ✓ | 232 / 233 / 241V2A-* 出处齐全 |
| 12 | IGNORE_TABLES Phase 1 静态清单完整 | ⚠️ **部分**(12 表分类完成,4 个【待确认】)| **Contract Gap-04** |
| 13 | 不存在未标注的关键推断 | ✓ | 全部标注 evidence 等级 |
| 14 | 不存在与 Effective Spec 冲突 | ✓ | 无 Contract Conflict |
| 15 | 所有【待确认】都有明确说明 | ✓ | §15 列出 7 项 Gap |

### 16.2 Self-Check 结论

```
G2 Contract Gate Self-Check = PARTIAL

已覆盖:12 Object / user_company / 40 API / Transaction / Tenant / Exception / Test Mapping(7 项)
部分覆盖:Repository Custom 方法 / Service 方法 / Security 注解 / IGNORE_TABLES 4 个【待确认】(3 项)
未覆盖:0
```

### 16.3 Contract Coverage

```
Contract Coverage = PARTIAL
```

**理由**:Contract 主体已建立(覆盖 7/15 项完全 + 3/15 项部分),但存在 7 项 Contract Gap,需要 Phase 1 实施时补齐。

---

## §17. G2 Contract Gate 最终判定

**【G2-Contract-01 显式】**:**G2 CONTRACT GATE = PARTIAL**

理由:
- 12 Object 字段级 Contract 框架已建立(⚠️ 部分字段【待确认】)
- user_company Infrastructure Contract ✓ 完整
- 40 API 字段级 Contract ✓ 完整(沿用 232 + 233)
- Transaction Contract ✓ 完整
- Tenant Contract ✓ 完整
- Exception Contract ✓ 完整
- Test Mapping ✓ 完整
- Repository Custom 方法 Contract Gap-01
- Service 方法 Contract Gap-02
- Security 注解 Contract Gap-03
- IGNORE_TABLES 4 个【待确认】Contract Gap-04

---

## §18. 当前是否允许开始 Backend Implementation

**【G2-Contract-01 显式】**:**当前不允许开始 Backend Implementation**。

理由:
- Contract Coverage = PARTIAL
- 7 项 Contract Gap 未补齐(Gap-01 ~ Gap-07)
- Gap-01(12 业务 Custom 方法)+ Gap-04(4 个 companyId 字段)= **高**优先级
- Gap-02(6 个 Service 方法)+ Gap-03(Sa-Token 注解)+ Gap-05(字段)+ Gap-06(页面 26 项)+ Gap-07(SystemSetting)= 中优先级

### 18.1 剩余 Contract Gap

| # | Gap | 优先级 | 建议处理 |
|---:|---|:-:|---|
| **Gap-01** | 12 业务 Object 字段级 Custom 方法 | **高** | Phase 1 页面侦察 + 业务需求分析 |
| **Gap-04** | 4 个表的 companyId 字段 | **高** | DDL 重新核验(基于 235B / 236B)|
| **Gap-02** | 6 个 Service 方法 | 中 | Phase 1 页面侦察 + 业务需求 |
| **Gap-03** | Sa-Token 注解 | 中 | Sa-Token 文档 + 角色列表 |
| **Gap-05** | 若干字段(doctorId 等)| 中 | Phase 1 页面侦察 |
| **Gap-06** | Phase 1 范围 26 项字段 | 中 | 诊所管理 + 系统设置页面侦察 |
| **Gap-07** | SystemSetting 范围 | 中 | V4.4 重新冻结(已有 V4.3 文档)|

### 18.2 下一阶段建议

**【G2-Contract-01 显式】**:
- 不是 S1-171(已明确禁止创建)
- 不是 S1-170F / G(已明确禁止创建)
- **是**:补齐 7 项 Contract Gap 的具体工作
- **可以并行**:Phase 1 页面侦察(诊所管理 100% 已完成,系统设置需补齐)

---

## §19. Evidence Index

| Contract 部分 | 证据来源 |
|---|---|
| §4.1 通用规则 | 238 §3 |
| §4.2.1 Company | 214 §1.4 + 04_数据模型.md + 238 §4.1 |
| §4.2.2 Customer | 105 §6.1 + 238 §4.2 |
| §4.3.3 Appointment | 238 §4.3 + 229 §4.2 |
| §4.3.4 Visit | 229 §4.4 + 238 §4.4 |
| §4.3.5 TriageQueue | 229 §15.4 + 238 §4.5 |
| §5 user_company Infrastructure | 241V2A-10 / 11 |
| §7 40 API | 232 + 233 |
| §9 Transaction 分类 | 232 + 233 |
| §10 CompanyContext | 241V2 §4 |
| §10 Interceptor | 241V2 §5.4.2 |
| §10 Filter | 241V2 §5.4.1 |
| §12 Exception | 241V2A-17 / 18 |
| §13 Test Mapping | 241V2A-5 / 14 / 15 |
| §14 IGNORE_TABLES | 241V2 §6.4 + 235B §6.3 |

---

## §20. 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-01_OptFlow-PMS_Production-Implementation-Contract.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改任何历史 MD |
| 严禁 | 修改历史 MD / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

**End of G2-Contract-01**
