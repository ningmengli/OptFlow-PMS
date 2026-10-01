# G2-Contract-Audit-02｜Production Implementation Contract 独立盲审

> **本轮定位**:对 `G2-Contract-02_OptFlow-PMS_Production-Implementation-Contract.md` 的**独立盲审**。
> **不是**修 Contract,**不是**开发,**不是**修改任何已有文件。
> **本轮唯一输出**:本审计文档。
> **本轮特别强调**:不信任 G2-Contract-02 的自报结果(P0=0 / E=0 / F=0 / 21/21 / Effective Spec conflict=0 — 全部只能作为"待验证声明"),必须重新独立核验。
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史 MD(190~241V2A-42 + S1-170 全系列 + G2-Contract-01 + G2-Contract-Audit-01 全系列 + G2-Contract-02)未修改** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-02_Production-Implementation-Contract独立盲审.md` |
| 任务性质 | 独立盲审(Independent Blind Audit)|
| 审计对象 | G2-Contract-02(本文不对其做修改)|
| 创建时间 | 2026-09-17 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 审计口径 | **以 233 + 235B + 236B + 238 + 240 + 241V2 + 241V2A-12 + 241V2A-13 + 241V4 为绝对基准** |
| 标签 | 【A 直接证据】/【B 多源】/【C 部分】/【D 冲突】/【E 推断】/【F Contract 错误】/【待确认】 |
| 严禁 | 修改 G2-Contract-02 / 修改任何已有审计文件 / 修改任何历史 MD / 创建 backend / 写 Java 源文件 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1 Audit Scope

只回答一个问题:

> **G2-Contract-02 是否真正修复了 G2-Contract-Audit-01R2 §7 锁定的 21 项 Fix Action,是否仍存在 P0 Contract Conflict / P1 Contract Gap,是否达到 G2 READY 标准?**

特别注意:**"自报已修复" ≠ "真正已修复"**。每项 Fix Action 必须独立核验。

---

## §2 Evidence Method

### 2.1 验证流程

| 步骤 | 内容 |
|:-:|---|
| 1 | 重新读取 G2-Contract-02 全部章节(§0-§20)|
| 2 | 重新交叉读取 241V2A-12 / 241V2A-13 / 233 / 235B / 236B / 238 / 241V4 / 240 / 241V2 |
| 3 | **逐项独立核验 RC-1 ~ RC-6 + PA-01 ~ PA-07** |
| 4 | **不信任 G2-Contract-02 自报** — 独立重新判定 5 条硬条件 |

### 2.2 证据等级

| 级别 | 含义 |
|:-:|---|
| A | 直接证据(基线 MD 显式冻结,字段名 / 数值完全一致)|
| B | 多源交叉验证 |
| C | 部分证据 |
| D | 冲突 |
| E | AI 推断(**本轮严禁**) |
| F | Contract 与 Effective Spec 直接冲突(**本轮严禁**)|
| 【待确认】 | 有效证据不足 |

---

## §3 RC-1 API 逐 API 审计

### 3.1 API-001 ~ API-024(已修复验证)

> G2-Contract-02 §4.1 列出的 API-001~024 Path 与 232 完全一致,无冲突。

**结论**:API-001 ~ API-024 = **PASS**。

### 3.2 API-025 ~ API-040(RC-1 重点核验)

| API | G2-02 §4.1 Path | 233 / 232 Path | 核对 |
|---|---|---|:-:|
| **API-025** | `POST /api/visit/create-direct` | `POST /api/visit/create-direct` | ✅ **PASS** |
| **API-026** | `POST /api/queue/next` | `POST /api/queue/next` | ✅ **PASS** |
| **API-027** | `POST /api/queue/call` | `POST /api/queue/call` | ✅ **PASS** |
| **API-028** | `POST /api/queue/skip` | `POST /api/queue/skip` | ✅ **PASS** |
| **API-029** | `POST /api/queue/recall` | `POST /api/queue/recall` | ✅ **PASS** |
| **API-030** | `POST /api/queue/start-consult` | `POST /api/queue/start-consult` | ✅ **PASS** |
| **API-031** | `POST /api/queue/complete` | `POST /api/queue/complete` | ✅ **PASS** |
| **API-032** | `GET /api/queue/console` | `GET /api/queue/console` | ✅ **PASS** |
| **API-033** | `GET /api/queue/room` | `GET /api/queue/room` | ✅ **PASS** |
| **API-034** | `POST /api/visit/transfer` | `POST /api/visit/transfer` | ✅ **PASS** |
| **API-035** | `POST /api/visit/cancel-direct` | `POST /api/visit/cancel-direct` | ✅ **PASS** |
| **API-036** | `GET /api/visit/list-by-appointment` | `GET /api/visit/list-by-appointment` | ✅ **PASS** |
| **API-037** | `POST /api/doctor/pause` | `POST /api/doctor/pause` | ✅ **PASS** |
| **API-038** | `POST /api/doctor/resume` | `POST /api/doctor/resume` | ✅ **PASS** |
| **API-039** | `GET /api/bigscreen/list` | `GET /api/bigscreen/list` | ✅ **PASS** |
| **API-040** | `GET /api/bigscreen/display` | `GET /api/bigscreen/display` | ✅ **PASS** |

### 3.3 RC-1 审计结论

> **RC-1 修复 = COMPLETE**。14 个 API Path 全部正确,与 233 完全一致。

---

## §4 RC-2 Transfer 深度审计

### 4.1 Transfer 9-step 逐步骤核验

| # | 235B §4.2 冻结 | G2-02 §7.2 描述 | 核对 |
|--:|---|---|:-:|
| 1 | validation(Visit.status = IN_CONSULTATION)| `validation` | ✅ **PASS** |
| 2 | create new Visit | `create new Visit(visitId2, appointmentId = oldVisit.appointmentId)` | ✅ **PASS** |
| 3 | create new TriageQueue(IN_POOL) | `create new TriageQueue(IN_POOL, employeeId = NULL, consultRoomId = NULL)` | ✅ **PASS** |
| 4 | Appointment.currentVisitId = newVisitId | `Appointment.currentVisitId = newVisitId` | ✅ **PASS** |
| 5 | Appointment.status = TRIAGE_WAITING | `Appointment.status = TRIAGE_WAITING` | ✅ **PASS** |
| 6 | old Visit = TRANSFERRED | `old Visit = TRANSFERRED` | ✅ **PASS** |
| 7 | old TriageQueue = REMOVED | `old TriageQueue = REMOVED` | ✅ **PASS** |
| 8 | old ReceptionQueue = DONE + cancelReason='TRANSFERRED' | `old ReceptionQueue = DONE + cancelReason = 'TRANSFERRED'` | ✅ **PASS** |
| 9 | COMMIT(任一失败全回滚)| `COMMIT - 所有操作原子提交,任一失败全回滚` | ✅ **PASS** |

### 4.2 关键约束核验

| 关键约束 | 235B §4.3 冻结 | G2-02 §7.2 描述 | 核对 |
|---|---|---|:-:|
| **API-034 不创建新 ReceptionQueue** | "API-034 不创建新 ReceptionQueue。新 ReceptionQueue 由 API-021 triage/assign 创建" | "**不创建新 ReceptionQueue**(新 ReceptionQueue 由 API-021 创建)" | ✅ **PASS** |
| 旧 ReceptionQueue.status = DONE(非 CANCELLED)| DONE | DONE | ✅ **PASS** |
| 旧 TriageQueue.status = REMOVED(非 IN_POOL)| REMOVED | REMOVED | ✅ **PASS** |

### 4.3 🔴 Transfer Rollback 内部矛盾 — **P0 Contract Conflict**

**老板审计任务 §4 明确**:

> 另外重新核对:
> "任一失败全回滚"
> 与:
> "rollback strategy = 【待确认】"
> 是否形成内部矛盾。
>
> 如果 235B 已经明确全回滚:
> 不能再把同一语义标记为待确认。

**G2-Contract-02 内部矛盾**:

| 章节 | G2-02 表述 |
|---|---|
| §7.2 第 9 步 | "COMMIT - 所有操作原子提交,**任一失败全回滚**" — **冻结** |
| §7.5(PA-07)| "Transfer 整体事务 **冻结**(235B §4.2)" + "任一失败全回滚 **冻结**(235B §4.2 COMMIT 语义)" + "部分失败是否全部回滚 **【待确认】**" + "**Rollback strategy = 【待确认】**" |

**矛盾点**:
- §7.2 已冻结 "任一失败全回滚"(COMMIT 语义)
- §7.5 又把 "Rollback strategy" 标为【待确认】
- **"任一失败全回滚" 就是 Rollback strategy 的核心定义**(235B §4.2 COMMIT 语义)
- 把已冻结的同一语义再次标为【待确认】,**违反内部一致性**

> **🔴 P0-A3(P0 Contract Conflict — 内部矛盾)**:
> G2-Contract-02 §7.2 与 §7.5 对同一概念("任一失败全回滚")给出不一致冻结状态。
> **违反 R2 §6 纪律 #1**:已冻结内容不得伪装成未冻结。

### 4.4 RC-2 审计结论

- 9 步骤 + 关键约束 = **PASS**
- **但**:Rollback strategy 内部矛盾 = **🔴 P0-A3**
- 整体 RC-2 = **PARTIAL PASS**(9 步骤 PASS,语义矛盾 P0)

---

## §5 RC-3 Object 逐字段审计

### 5.1 12 业务 Object 字段核验

| Object | 字段数(G2-02)| 字段数(238 / 236B)| 一致 | 备注 |
|---|---:|---:|:-:|---|
| Company | 7 | 7(238 §4.1)| ✅ | phone 标【待确认】(R2 纪律)|
| Customer | 5 | 5(238 §4.2)| ✅ | |
| **Patient** | **8** | **8**(238 §4.3)| ✅ | **medicalCode 已删除** ✓ |
| **Employee** | **10** | **10**(238 §4.4 + 235B §2)| ✅ | **adminId / status 已增** ✓ |
| **ConsultRoom** | **6** | **6**(238 §4.5)| ✅ | **roomNo 已删除** ✓ |
| **BigScreen** | **7** | **7**(238 §4.6 + §15)| ✅ | **consultRoomIdArray JSON 已标** ✓ |
| **AppointmentSchedule** | **7** | **7**(238 §4.8)| ✅ | **employeeId / 删 startTime/endTime** ✓ |
| **AppointmentSlot** | **11** | **11**(238 §4.9 + 236B §3.5)| ✅ | **companyId 字段无 FK** ✓ |
| **Appointment** | **23** | **23**(238 §4.7)| ✅ | **拆 appointmentTime + 增 11 字段** ✓ |
| **Visit** | **16** | **16**(238 §4.10)| ✅ | **删 checkInTime + 增 7 字段** ✓ |
| TriageQueue | 11 | 11(238 §4.11)| ✅ | status 4 状态完整(IN_POOL/ASSIGNED/REMOVED/CANCELLED)|
| **ReceptionQueue** | **15** | **15**(238 §4.12)| ✅ | **triageQueueId UNIQUE + sequenceInRoom + 6 状态** ✓ |

### 5.2 关键核对点

#### Patient.companyId(238 §4.3 + 236B §3)
- G2-02 §3.4:`companyId` Long,**字段保留,无 FK 约束**(236B 已删 fk_patient_company)
- 老板审计任务 §6 明确:Patient.companyId 字段存在,无 FK
- ✅ **PASS**

#### AppointmentSlot.companyId(238 §4.9 + 236B §3.5)
- G2-02 §3.9:`companyId` Long,**字段保留,无 FK 约束**(236B 已删 fk_slot_company)
- 老板审计任务 §6 明确:AppointmentSlot.companyId 字段存在,无 FK
- ✅ **PASS**

#### BigScreen.consultRoomIdArray(238 §15 + 236B §3.5)
- G2-02 §3.7:`consultRoomIdArray` String,**JSON 字符串**(不是 FK),存储关联检查室 ID 列表
- 236B §3.5 明确:"JSON 逻辑(不创建 FK)"
- ✅ **PASS**

#### Employee.adminId(235B §2 显式 NOT NULL UNIQUE)
- G2-02 §3.5:`adminId` Long,**235B §2 显式 NOT NULL UNIQUE**
- ✅ **PASS**

#### Appointment.appointmentNo(238 §4.7 + 236B §B-7 UNIQUE)
- G2-02 §3.10:`appointmentNo` String,**UNIQUE**,业务编号
- ✅ **PASS**

#### ReceptionQueue.triageQueueId UNIQUE(238 §4.12)
- G2-02 §3.13:`triageQueueId` String,**UNIQUE**,FK → triage_queue
- ✅ **PASS**

### 5.3 RC-3 审计结论

> **RC-3 修复 = COMPLETE**。12 业务 Object 全部 9 个重写 + 3 个沿用,字段数与 238 完全一致。
> Patient / AppointmentSlot 的 companyId 字段(无 FK)表达正确。
> BigScreen.consultRoomIdArray JSON 表达正确。

---

## §6 Repository / user_company 深度审计

### 6.1 12 业务 Repository(238 §6.1 / §6.2)

| 维度 | 状态 |
|---|:-:|
| 12 Entity 各 1 个 JpaRepository | ✅ PASS(238 §6.1)|
| 11 个 Custom 查询方法 | ✅ PASS(238 §6.2)|
| 不添加"通用全表扫描"型方法 | ✅ PASS(238 §6.3 沿用)|

### 6.2 🔴 user_company Repository — **P0 Contract Conflict**

**老板审计任务 §6 特别强调**:

> 重点检查 SQL 语义。
> 禁止:LIMIT 1 / ORDER BY / GROUP BY / 任何静默选择一条记录的逻辑
> 必须核验:0 rows / 1 row / >1 rows 的行为。
> 若 Contract 使用 LIMIT 1:立即登记为 P0 Contract Conflict。
> 不要把它归为"待确认"。

#### 6.2.1 G2-Contract-02 §5.4 user_company Repository 描述

```
### 5.4 user_company Repository(沿用 G2-Contract-01 §5.3)

| 方法 | 来源 |
|---|---|
| `updateDefaultToZero(Long userId)` | 241V2A-10 / 12 |
| `setDefault(Long userId, Long companyId)` | 241V2A-10 / 12 |
| `existsByUserIdAndCompanyId(Long userId, Long companyId)` | 241V2A-12 |
| `countByUserIdAndIsDefault(Long userId, int isDefault)` | 241V2A-12 |
| **`selectDefaultCompanyId(Long userId)`(自定义 @Query,带 LIMIT 1)** | 241V2A-13 |
```

#### 6.2.2 与 Effective Spec 的双重冲突

| 维度 | G2-02 §5.4 | Effective Spec 冻结 | 冲突 |
|:-:|---|---|:-:|
| **Repository 公开方法数** | 列出 5 个(含 `selectDefaultCompanyId`)| 241V2A-12 §2.3 / §4.2 显式冻结:**生产 Repository 严格 4 个公开方法,不增加 `selectDefaultCompanyId`** | **🔴 P0-A2** |
| **SQL 字面量** | "带 LIMIT 1" | 241V2A-13 §3.2 / §3.5 显式作废:`SQL: SELECT company_id FROM user_company WHERE user_id = #{userId} AND is_default = 1`(**无 LIMIT**),严禁 `LIMIT 1` / `ORDER BY ... LIMIT 1` / `MAX(company_id)` / `MIN(company_id)` / `GROUP BY user_id` | **🔴 P0-A1** |
| **方法分类** | 列入 Repository 章节 | 241V2A-12 §4.2 显式:`selectDefaultCompanyId` 是 Mapper 第 5 方法,**仅供测试验证使用,不归生产业务**;241V2A-13 §1 重申:"生产 Service / Repository 不得调用" | **🔴 P0-A2**(分类错)|
| **来源标注** | 标 241V2A-13 | 241V2A-13 §1 显式冻结:**显式作废 241V2A-12 §4.2 的 LIMIT 1**(反 LIMIT 1) | **🔴 P0-A1**(来源错标)|

#### 6.2.3 行为矩阵核对(241V2A-13 §3.4)

> **241V2A-13 显式冻结的 `selectDefaultCompanyId` 三种情况行为**:

| 结果 | G2-02 §5.4 隐含行为(LIMIT 1)| 241V2A-13 §3.4 冻结 | 冲突 |
|---|---|---|:-:|
| 0 行 | 静默返回 null | 静默返回 null | ✅ 一致 |
| 1 行 | 返回该 companyId | 返回该 companyId | ✅ 一致 |
| **>1 行** | **LIMIT 1 静默返回第一条,谎报成功** | **MyBatis 单值映射自动抛 `TooManyResultsException`,必须失败** | **🔴 直接冲突** |

> **严重性**:一旦按 G2-Contract-02 §5.4 实现(带 LIMIT 1),当出现双 default 时会**静默谎报成功**,违反 exactly-one 业务规则(241V2A-11 §4 已裁决),导致 DEFAULT-01/03/05 测试全部失效。

#### 6.2.4 P0-A1 / P0-A2 结论

> **🔴 P0-A1(P0 Contract Conflict)**:
> G2-Contract-02 §5.4 "带 LIMIT 1" 与 241V2A-13 §3.2 / §3.5 显式作废 LIMIT 1 直接冲突。
> 必须立刻修复。

> **🔴 P0-A2(P0 Contract Conflict)**:
> G2-Contract-02 §5.4 把 Mapper 方法 `selectDefaultCompanyId` 列入 Repository 章节,
> 违反 241V2A-12 §4.2 显式冻结"生产 Repository 严格 4 公开方法"+ 241V2A-13 §1 显式重
> 申"生产 Service / Repository 不得调用 selectDefaultCompanyId"。
> 必须立刻修复。

### 6.3 12 业务 Repository 审计结论

| 维度 | 状态 |
|---|:-:|
| 12 业务 Repository | ✅ PASS(238 §6.1 / §6.2)|
| 11 个 Custom 方法 | ✅ PASS(238 §6.2)|
| user_company Repository 描述 | **🔴 P0-A1 + P0-A2** |

---

## §7 PA-01 Service 深度审计(关键:Repository ≠ Service)

### 7.1 老板审计任务 §7 纪律

> 必须严格区分:Repository method vs Service method
> 不得因为 238 §6.2 出现某个 Repository 方法,就自动认定同名 Service method 已冻结。
> 没有 Service 直接证据:必须保持【待确认】
> 不能把 Repository 证据升级成 Service 冻结。

### 7.2 6 Service 方法逐个核验

#### 7.2.1 EmployeeService(G2-02 §6.2.1)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| `findByCompanyIdAndAdminId(companyId, adminId)` | "238 §6.2 + 235B §2" 标冻结 | 这是 **Repository 方法**(238 §6.2 EmployeeRepository),**不是 Service 方法** | 🔴 **P1-A1**(Repository 误升级为 Service 冻结)|
| `findByCompanyIdAndRole(companyId, role)` | "238 §6.2" 标冻结 | 同上(Repository 方法)| 🔴 **P1-A1**(Repository 误升级)|
| **`getEmployeeByLogin(employeeId)`** | "235B §2" 标"业务规则冻结",具体方法签名【待确认】 | 235B §2 显式冻结 adminId 逻辑,但**未冻结 Service 方法名 `getEmployeeByLogin`** | **🔴 P1-A1(自行发明 Service 方法名)** |

#### 7.2.2 PatientService(G2-02 §6.2.2)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| `findByCustomerId(customerId)` | "238 §6.2" 标冻结 | 这是 **Repository 方法** | 🔴 **P1-A1**(Repository 误升级)|
| `findByCompanyId(companyId)` | "238 §6.2" 标冻结 | 同上 | 🔴 **P1-A1**(Repository 误升级)|
| 其它 CRUD 方法 | 【待确认】 | 无 Service 方法证据 | ✅ 正确标【待确认】 |

#### 7.2.3 CustomerService(G2-02 §6.2.3)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| `findByCompanyId(companyId)` | "238 §6.2" 标冻结 | Repository 方法 | 🔴 **P1-A1** |
| 其它 CRUD 方法 | 【待确认】 | 无 Service 方法证据 | ✅ 正确标【待确认】 |

#### 7.2.4 ConsultRoomService(G2-02 §6.2.4)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| `findByCompanyId(companyId)` | "238 §6.2" 标冻结 | Repository 方法 | 🔴 **P1-A1** |
| 其它 CRUD 方法 | 【待确认】 | 无 Service 方法证据 | ✅ 正确标【待确认】 |

#### 7.2.5 BigScreenService(G2-02 §6.2.5)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| `findByCompanyIdAndSceneType(companyId, sceneType)` | "238 §6.2" 标冻结 | Repository 方法 | 🔴 **P1-A1** |
| **`parseConsultRoomIdArray(bigScreenId)`** | "238 §15 概念" 标"业务规则冻结",具体 JSON 解析方式【待确认】 | 238 §15 只说明 `consultRoomIdArray` 是 JSON 字段,**未冻结 Service 方法名 `parseConsultRoomIdArray`** | **🔴 P1-A2(自行发明 Service 方法名)** |
| 其它 CRUD 方法 | 【待确认】 | 无 Service 方法证据 | ✅ 正确标【待确认】 |

#### 7.2.6 CompanyService(G2-02 §6.2.6)

| 方法 | 来源声称 | 独立证据 | 状态 |
|---|---|---|:-:|
| **"公司初始化 CRUD(用于 SaaS 初始化)"** | "240 / 241V2" 标"业务规则冻结",具体方法签名【待确认】 | 240 / 241V2 冻结跨公司隔离原则,但**未冻结"公司初始化"业务概念 + 未冻结 Service 方法名** | **🔴 P1-A3(自行发明业务概念 + Service 方法名)** |
| 其它方法 | 【待确认】 | 无 Service 方法证据 | ✅ 正确标【待确认】 |

### 7.3 PA-01 关键发现汇总

| 类型 | 数量 | 严重度 |
|---|---:|:-:|
| **Repository 误升级为 Service 冻结** | 6 处(P1-A1,Employee / Patient / Customer / ConsultRoom / BigScreen / Customer 各 1 处)| **P1** |
| **自行发明 Service 方法名** | 2 处(P1-A1 `getEmployeeByLogin` / P1-A2 `parseConsultRoomIdArray`)| **P1** |
| **自行发明业务概念** | 1 处(P1-A3 "公司初始化" / "SaaS 初始化")| **P1** |

### 7.4 PA-01 审计结论

> **🔴 PA-01 修复 = INCOMPLETE**。
> - 6 处 P1(P1-A1 / A2 / A3):把 Repository 方法误升级为 Service 冻结 + 自行发明 Service 方法名
> - 虽然 Service 方法名后跟【待确认】标签,但**方法名本身就是 AI 推断**,违反 R2 §六 严禁
> - 必须修复:删除所有自行发明的 Service 方法名,只保留"具体方法签名【待确认】"

---

## §8 PA-02 Transaction 审计

### 8.1 G2-02 §7.3 API-016 / API-021 Transaction 分类

| API | G2-02 §7.3 描述 | 独立证据 | 状态 |
|---|---|---|:-:|
| API-016 | "Transaction classification = 【待确认】"(业务复杂度提示:多对象联动)| 233 §API-016 字段级已冻结,233 未明确 transaction 分类 | ✅ **PASS** |
| API-021 | "Transaction classification = 【待确认】"(业务复杂度提示:多对象联动 + 并发敏感)| 233 §API-021 字段级已冻结,233 未明确 transaction 分类 | ✅ **PASS** |

### 8.2 PA-02 关键发现

> G2-Contract-02 §7.3 严格遵守 R2 §三 PA-02 纪律:
> - ✓ 没有自行写 T1 / T2 / T3 / T4
> - ✓ 仅记录业务动作 + 参与对象
> - ✓ Transaction 分类保持【待确认】
> - ✓ 描述"现有 Effective Spec 是否冻结原子性/锁语义"作为决策依据

### 8.3 PA-02 审计结论

> **✅ PA-02 = PASS**。API-016 / API-021 Transaction 分类处理正确。

---

## §9 PA-03 Security 深度审计

### 9.1 7 角色 vs 6 角色 — **P0 Contract Conflict(内部矛盾)**

**G2-Contract-02 §9.1 实际列出的角色**:

| # | 角色 | 来源声称 |
|--:|---|---|
| 1 | ADMIN | 235B §2 |
| 2 | DOCTOR | 235B §2 |
| 3 | NURSE | 235B §2 |
| 4 | RECEP | 235B §2 |
| 5 | STAFF | 235B §2 |
| 6 | BIGSCREEN | 233 §API-040 |
| **?**| **第 7 个角色** | **未列出** |

**G2-Contract-02 内部矛盾**:
- §9.1:**只列 6 个角色**
- §9.4 / §13 / §17:反复出现 "**7 角色**完整列表" / "7 角色完整定义" 等说法
- **第 7 个角色既未列出,也未显式标【待确认】**

**🔴 P0-A4(P0 Contract Conflict — 内部矛盾)**:
G2-Contract-02 §9.1 列了 6 个角色,但 §9.4 / §13 / §17 反复说 "7 角色"。
**违反内部一致性 + 违反 R2 §六 严禁"未冻结内容伪装成冻结事实"**。
必须修复:补全第 7 个角色(需 233 证据),或改为 "6 角色" 全文一致。

### 9.2 40 API × 7 Role 权限矩阵

**G2-Contract-02 §13 第 19 项**:
> 9.2 权限 | 40 API × 7 角色完整矩阵 | 【待确认】

**G2-Contract-02 §9.3**:
> | 角色 × API 权限矩阵(业务规则)| **冻结**(233 各 API + 235B §2)|

**矛盾点**:
- §9.3 声称 40 API × 7 角色矩阵**冻结**
- §13 又把 "40 API × 7 角色完整矩阵" 标【待确认】

> **🔴 P1-A4(内部矛盾)**:§9.3 vs §13 自相矛盾

### 9.3 Sa-Token Annotation

**G2-Contract-02 §9.3 / §9.4**:
> Sa-Token `@SaCheckRole` 具体 annotation = **【待确认】**(Effective Spec 未冻结具体 annotation)
> Sa-Token `@SaCheckPermission` 具体 annotation = **【待确认】**

**判断**:
- ✓ Sa-Token annotation 严守 R2 §三 PA-03 纪律,没有自行指定 `@SaCheckRole("DOCTOR")`
- ✓ 区分 Business Authorization Rule vs Sa-Token Implementation Annotation
- ✅ **PASS**

### 9.4 公开 API 白名单

**G2-Contract-02 §9.2** 已补 `/api/bigscreen/display`(RC-6 修复)。

✅ **PASS**

### 9.5 PA-03 审计结论

| 维度 | 状态 |
|---|:-:|
| 角色定义 | 🔴 **P0-A4**(6 vs 7 内部矛盾)|
| 权限矩阵 | 🔴 **P1-A4** §9.3 vs §13 自相矛盾 |
| Sa-Token Annotation | ✅ PASS(严守 R2 纪律)|
| 公开 API 白名单 | ✅ PASS(RC-6 修复完整)|

---

## §10 PA-04 IGNORE_TABLES 审计

### 10.1 G2-Contract-02 §12 IGNORE_TABLES 描述

| 维度 | G2-02 §12 | 241V4 §6.1 | 核对 |
|---|---|---|:-:|
| 5 个配置项 | flyway_schema_history + company + user + user_company + flyway_schema_history_v44 | 5 个配置项 | ✅ PASS |
| 区分当前生效 vs 预留 | §12.2 / §12.3 区分 | 241V4 §6.1 区分 | ✅ PASS |
| flyway_schema_history_v44 激活条件 | §12.3 标【待确认】 | 241V4 §6.1 提及预留但未冻结激活条件 | ✅ PASS(R2 §三 PA-04 纪律)|

### 10.2 PA-04 审计结论

> **✅ PA-04 = PASS**。IGNORE_TABLES 静态清单严格遵守 R2 §三 PA-04 纪律,不虚构 activation condition。

---

## §11 PA-05 / PA-06 审计

### 11.1 PA-05 Phase 1 系统设置(G2-02 §14)

| 维度 | 状态 |
|---|:-:|
| Phase 1 = 诊所管理 + 系统设置 | ✅ PASS(沿用 S1-170E §8)|
| 诊所管理 100% 完成 | ✅ PASS(沿用历史侦察)|
| 系统设置 26 项字段 | **🔴 【待确认】**(未编造)|
| 26 项字段未自行发明 | ✅ PASS |

**老板审计任务 §11 明确**:
> "全部【待确认】"在没有证据时可以是合法状态,不要为了完整度强行判 P0。

### 11.2 PA-06 SystemSetting V4.4(G2-02 §15)

| 维度 | 状态 |
|---|:-:|
| SystemSetting 字段 / 状态 / 子配置 | **🔴 【待确认】**(未编造)|
| V4.4 范围 | **🔴 【待确认】** |
| 未自行发明 | ✅ PASS |

### 11.3 PA-05 / PA-06 审计结论

> **✅ PA-05 / PA-06 = PASS**。严守"全部【待确认】"状态,不伪造字段。

---

## §12 Exception / DEFAULT 审计(沿用 G2-Contract-01)

### 12.1 Exception Contract(G2-02 §10)

> 沿用 G2-Contract-01 §12 + 241V2A-17 / 18 / 241V2A-16 冻结。

| 异常类 | HTTP | ResultCode | 来源 | 核对 |
|---|---|---|---|:-:|
| BusinessException | 200 + code | — | 241 §4.1 | ✅ |
| CompanyContextMissingException | 401 | 60000 | 241 §4.2 | ✅ |
| CompanyMismatchException | 400 | 60001 | 241 §4.3 | ✅ |
| CompanyAccessDeniedException | 403 | 60002 | 241 §4.4 | ✅ |
| UserNotFoundException | 404 | 60003 | 241V2A-17 §3.1 | ✅ |
| UserDisabledException | 403 | 60004 | 241V2A-17 §3.2 | ✅ |
| IllegalStateException(java.lang)| 500 | — | 241V2A-16 §3 | ✅ |
| NotLoginException | 401 | — | 241V2 §13.2 | ✅ |

### 12.2 DEFAULT Test(G2-02 §11)

| DEFAULT | 核对 |
|---|:-:|
| DEFAULT-01 setDefault + updateDefaultToZero | ✅ |
| DEFAULT-02 countByUserIdAndIsDefault | ✅ |
| DEFAULT-03 setDefault + Verifier + selectDefaultCompanyId | ✅ |
| DEFAULT-04 跨公司隔离 | ✅ |
| DEFAULT-05 exactly-one 断言 | ✅ |

### 12.3 Exception / DEFAULT 审计结论

> **✅ Exception / DEFAULT = PASS**。100% 沿用 G2-Contract-01 冻结 + 241V2A-X 冻结。

---

## §13 Internal Consistency Audit

> 重点检查 G2-Contract-02 自身的内部一致性。

| # | 内部矛盾 | 章节冲突 | 严重度 |
|--:|---|---|:-:|
| IC-1 | **Rollback strategy 矛盾** | §7.2 vs §7.5 | **🔴 P0-A3**(已登记)|
| IC-2 | **7 角色 vs 6 角色 矛盾** | §9.1 vs §9.4 / §13 / §17 | **🔴 P0-A4**(已登记)|
| IC-3 | **权限矩阵矛盾** | §9.3 vs §13 | **🔴 P1-A4**(已登记)|
| IC-4 | **Service 方法名自行发明** | §6.2 | **🔴 P1-A1 / A2 / A3**(已登记)|
| IC-5 | **user_company SQL 字面量错** | §5.4 | **🔴 P0-A1 / A2**(已登记)|

---

## §14 21 Fix Action Verdict

### 14.1 RC-1 ~ RC-6(P0 Fix Actions)

| Fix ID | G2-02 § | 独立审计结论 |
|:-:|:-:|---|
| **RC-1** | §4.1 / §4.3 | ✅ **PASS**(14 API Path 全对)|
| **RC-2** | §7.2 / §7.5 | ⚠️ **PARTIAL**(9 步骤 PASS,但 §7.5 Rollback 策略内部矛盾 = **P0-A3**)|
| **RC-3a** | §3.4 | ✅ **PASS**(Patient 字段全对)|
| **RC-3b** | §3.5 | ✅ **PASS**(Employee 字段全对)|
| **RC-3c** | §3.6 | ✅ **PASS**(ConsultRoom 字段全对)|
| **RC-3d** | §3.7 | ✅ **PASS**(BigScreen 字段全对,JSON 区分正确)|
| **RC-3e** | §3.8 | ✅ **PASS**(AppointmentSchedule 字段全对)|
| **RC-3f** | §3.9 | ✅ **PASS**(AppointmentSlot 字段全对)|
| **RC-3g** | §3.10 | ✅ **PASS**(Appointment 字段全对)|
| **RC-3h** | §3.11 | ✅ **PASS**(Visit 字段全对)|
| **RC-3i** | §3.13 | ✅ **PASS**(ReceptionQueue 字段全对)|
| **RC-4** | §12.1 / §12.5 | ✅ **PASS**(5 个配置项)|
| **RC-5** | §8.1 | ✅ **PASS**(company 是 12 业务表之一)|
| **RC-6** | §9.2 | ✅ **PASS**(bigscreen/display 已补)|

**但**:`selectDefaultCompanyId` SQL 字面量 "带 LIMIT 1" 是 **🔴 P0-A1** + **🔴 P0-A2**(G2-02 §5.4 误归类到 Repository 章节)。

### 14.2 PA-01 ~ PA-07(P1 Fix Actions)

| Fix ID | G2-02 § | 独立审计结论 |
|:-:|:-:|---|
| **PA-01** | §6.2 | ⚠️ **INCOMPLETE**(6 处 P1-A1 + 2 处自创 Service 方法名 + 1 处自创业务概念)|
| **PA-02** | §7.3 | ✅ **PASS**(严守【待确认】纪律)|
| **PA-03** | §9.1 / §9.3 / §9.4 | ⚠️ **PARTIAL**(Sa-Token PASS,但 6 vs 7 角色矛盾 = **P0-A4** + 权限矩阵矛盾 = **P1-A4**)|
| **PA-04** | §12.3 | ✅ **PASS**(不虚构 activation condition)|
| **PA-05** | §14 | ✅ **PASS**(26 项字段【待确认】)|
| **PA-06** | §15 | ✅ **PASS**(V4.4 全部【待确认】)|
| **PA-07** | §7.5 | ⚠️ **CONFLICT**(整体事务冻结 + Rollback strategy【待确认】,内部矛盾 = **P0-A3**)|

---

## §15 Remaining P0 / P1

### 15.1 新发现 P0 Contract Conflict(4 项)

| # | 严重度 | 位置 | 描述 |
|--:|:-:|---|---|
| **P0-A1** | 🔴 **P0** | G2-02 §5.4 | `selectDefaultCompanyId` SQL 字面量 "带 LIMIT 1" 与 241V2A-13 §3.2 / §3.5 显式作废 LIMIT 1 直接冲突 |
| **P0-A2** | 🔴 **P0** | G2-02 §5.4 | `selectDefaultCompanyId` 列入 Repository 章节,违反 241V2A-12 §4.2 显式冻结"生产 Repository 严格 4 公开方法"+ 241V2A-13 §1 重申"生产 Service / Repository 不得调用" |
| **P0-A3** | 🔴 **P0** | G2-02 §7.2 vs §7.5 | Transfer 9 步 "任一失败全回滚" 冻结 vs §7.5 "Rollback strategy = 【待确认】" 内部矛盾 |
| **P0-A4** | 🔴 **P0** | G2-02 §9.1 vs §9.4 / §13 / §17 | 6 角色 vs 7 角色 内部矛盾 |

### 15.2 新发现 P1 Contract Gap(3 项)

| # | 严重度 | 位置 | 描述 |
|--:|:-:|---|---|
| **P1-A1** | 🔴 P1 | G2-02 §6.2.1 / §6.2.2 / §6.2.3 / §6.2.4 / §6.2.5 / §6.2.6 | 6 Service 中 6 个 Repository 方法误升级为 Service 冻结(`findByCompanyIdAndAdminId` / `findByCustomerId` / `findByCompanyId` / `findByCompanyIdAndRole` / `findByCompanyIdAndSceneType` 等)|
| **P1-A2** | 🔴 P1 | G2-02 §6.2.5 | `parseConsultRoomIdArray(bigScreenId)` Service 方法名自行发明 |
| **P1-A3** | 🔴 P1 | G2-02 §6.2.1 / §6.2.5 / §6.2.6 | `getEmployeeByLogin` / "公司初始化" / "SaaS 初始化" 自行发明 Service 方法名 / 业务概念 |
| **P1-A4** | 🟡 P1 | G2-02 §9.3 vs §13 | 角色 × API 权限矩阵"冻结"vs "【待确认】" 内部矛盾 |

### 15.3 P0 / P1 残留汇总

| 维度 | 数量 |
|---|---:|
| **新 P0 Contract Conflict** | **4 项** |
| **新 P1 Contract Gap** | **4 项** |
| RC-1 ~ RC-6(已修复 RC-2 除外)| 13 项 PASS |
| PA-02 / PA-04 / PA-05 / PA-06 | 4 项 PASS |

---

## §16 Five Hard Conditions 重新判定

> 沿用 G2-Contract-Audit-01R2 §6.3 冻结的 5 条硬性验收条件。

| # | 验收条件 | 独立判定 | 状态 |
|--:|---|---|:-:|
| 1 | **P0 = 0** | ❌ **FAIL**(存在 4 项新 P0: P0-A1 / A2 / A3 / A4) | 🔴 |
| 2 | **P1 = 0 或残留项有证据不阻塞** | ❌ **FAIL**(存在 4 项新 P1: P1-A1 ~ A4)| 🔴 |
| 3 | **Effective Spec 直接冲突 = 0** | ❌ **FAIL**(P0-A1 / A2 是 Effective Spec 直接冲突)| 🔴 |
| 4 | **未冻结内容不伪装成冻结事实** | ❌ **FAIL**(P1-A1 Repository 误升级 + P1-A3 自创业务概念 + P0-A4 7 角色矛盾)| 🔴 |
| 5 | **不得自行发明字段 / API / 状态 / 权限 / Transaction** | ❌ **FAIL**(P1-A2 `parseConsultRoomIdArray` 自创方法名 + P1-A3 自创业务概念)| 🔴 |

**5 条硬条件 = 0 / 5 PASS**

---

## §17 Final G2 Decision

### 17.1 G2-Contract-02 整体判定

| 维度 | 状态 |
|---|:-:|
| RC-1 API Path | ✅ |
| RC-2 Transfer 9-step | ⚠️ PARTIAL(§7.2 PASS,§7.5 矛盾)|
| RC-3a~i 12 Object 字段 | ✅ |
| RC-4 IGNORE_TABLES | ✅ |
| RC-5 company 业务表概念 | ✅ |
| RC-6 公开 API 白名单 | ✅ |
| PA-01 Service | ⚠️ INCOMPLETE(6 处 P1)|
| PA-02 Transaction | ✅ |
| PA-03 Security | ⚠️ PARTIAL(7 角色矛盾 P0-A4 + 矩阵矛盾 P1-A4)|
| PA-04 IGNORE_TABLES 预留 | ✅ |
| PA-05 Phase 1 系统设置 | ✅ |
| PA-06 SystemSetting V4.4 | ✅ |
| PA-07 Transfer Rollback | ⚠️ CONFLICT(§7.5 矛盾 P0-A3)|
| Exception / DEFAULT | ✅ |

### 17.2 G2-Contract-02 自报 vs 独立审计对照

| 维度 | G2-02 自报 | 独立审计结论 |
|---|---|---|
| P0 = 0 | ✅ | **❌ FAIL(4 项新 P0)** |
| E = 0 | ✅ | ✅ |
| F = 0 | ✅ | **❌ FAIL(P0-A1 / A2 是 F 级)** |
| 21/21 Fix Action | ✅ | **❌ FAIL(实际有效修复 17/21)** |
| Effective Spec conflict = 0 | ✅ | **❌ FAIL(2 项直接冲突)** |

### 17.3 G2-Contract-02 最终判定

> **G2-Contract-02 = BLOCK**

**理由**:
1. 存在 **4 项 P0 Contract Conflict**(user_company SQL 字面量 / Repository 分类 / Transfer 内部矛盾 / 7 角色内部矛盾)
2. 存在 **4 项 P1 Contract Gap**(Repository 误升级 Service / 自创 Service 方法名 / 自创业务概念 / 权限矩阵矛盾)
3. 5 条硬性验收条件 0 / 5 PASS

### 17.4 Backend Entry

> **Backend Entry = BLOCK**(沿用 S1-170E §12)

### 17.5 最少必须满足的修复项

> 进入 G2-Contract-03 必须修复的最小集合:

| # | 修复项 | 位置 | 修复路径 |
|--:|---|---|---|
| 1 | **删除 §5.4 `selectDefaultCompanyId` 行)| §5.4 | 移到 Mapper 章节(非 Repository)+ 删除"带 LIMIT 1"字样,改为"自定义 @Query,无 LIMIT 截断,沿用 241V2A-13 §3.5 冻结"|
| 2 | **删除 §7.5 Rollback strategy = 【待确认】** | §7.5 | Rollback strategy 与整体回滚语义一致,**冻结**为"任一失败全回滚,沿用 235B §4.2 COMMIT 语义"(不再标【待确认】)|
| 3 | **补全第 7 个角色** | §9.1 / §9.4 / §13 / §17 | 改为 "6 角色"(删 §9.4 等处"7 角色"字样),或查 233 冻结补全第 7 个角色 |
| 4 | **删除所有自创 Service 方法名** | §6.2 | 删除 `getEmployeeByLogin` / `parseConsultRoomIdArray` / "公司初始化" 等,只保留"具体方法签名【待确认】"|
| 5 | **修复 §9.3 vs §13 权限矩阵矛盾** | §9.3 / §13 | 统一为"权限矩阵:Business Authorization Rule 部分冻结(233 各 API permission),完整 40×7 矩阵【待确认】" |

### 17.6 不需要修复的(PASS)

| 维度 | 数量 |
|---|---:|
| RC-1 API Path | 14 项 ✅ |
| RC-3a~i 12 Object 字段 | 9 项 ✅ |
| RC-4 IGNORE_TABLES 5 配置项 | ✅ |
| RC-5 company 是 12 业务表 | ✅ |
| RC-6 公开 API 白名单 | ✅ |
| PA-02 API-016/021 Transaction | ✅ |
| PA-04 IGNORE_TABLES 预留 | ✅ |
| PA-05 Phase 1 系统设置 | ✅ |
| PA-06 SystemSetting V4.4 | ✅ |
| Exception / DEFAULT 沿用 | ✅ |

---

## §18 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-02_Production-Implementation-Contract独立盲审.md` |
| 创建时间 | 2026-09-17 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-02 / 不修改任何已有审计文件 / 不修改任何历史 MD |
| 严禁 | 修改 G2-Contract-02 / 修改任何已有审计文件 / 修改任何历史 MD / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

**End of G2-Contract-Audit-02**