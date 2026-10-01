# G2-Contract-Audit-02A｜233 前 24 API + Security Role 补充独立核验

> **本轮定位**:对 G2-Contract-Audit-02 的**补充独立核验**(Audit-02A)。
> **不是**重新完整审计 G2-Contract-02。
> **不是**修改 G2-Contract-02 / Audit-02 / 任何已有文件。
> **本轮唯一输出**:本补充审计文档。
> **本轮唯一目标**:补 Audit-02 漏掉的两个独立问题:
> 1. API-001~024 当前有效编号 / Path / Method(以 233 §2 为绝对基准,**不假设 232 的前 24 项直接有效**)
> 2. Security Role 当前有效集合(以 233 §3 为绝对基准)
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史 MD(190~241V2A-42 + S1-170 全系列 + G2-Contract-01 / G2-Contract-Audit-01 全系列 + G2-Contract-02 + G2-Contract-Audit-02)未修改** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-02A_233前24API与Security角色补充核验.md` |
| 任务性质 | 补充独立核验(Supplementary Independent Audit)|
| 审计对象 | G2-Contract-02 §4.1(API-001~024 部分)+ §9.1(Security Role 部分)|
| 创建时间 | 2026-09-17 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 审计基准 | **233_S1-167A_API字段级设计修正版.md §2 + §3**(233 是 232 的修正版)|
| 严禁 | 修改 G2-Contract-02 / 修改 G2-Contract-Audit-02 / 修改任何已有审计文件 / 修改任何历史 MD / 创建 backend / 写 Java 源文件 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1 Audit Scope

回答两个独立问题:

1. **API-001~024**:以 233 §2 "40 API 总表(本版冻结)"为唯一 API 编号基准,G2-Contract-02 §4.1 是否一致?
2. **Security Role**:以 233 §3 "角色定义(本版 P0-5 修正)"为唯一角色基准,G2-Contract-02 §9.1 是否一致?

---

## §2 Evidence Method

### 2.1 233 §2 "40 API 总表(本版冻结)"完整提取

> 233 §2 是 232 的修正版,**重新输出完整 40 API**(API-001~API-040),反映全部 5 个 P0 + 1 个 P1 修正。

| 233 §2 关键说明 | 内容 |
|---|---|
| 与 232 的关键差异 | API-025 由 `queue/pause` 替换为 `visit/create-direct`(P0-2 + P0-4 联动)|
| 顺延影响 | API-026~040 顺延 +1(原 API-025 删除,后 15 个不变内容)|
| **P0-5 新增角色** | **PATIENT_SELF**(患者自助),仅 CONFIRMED/WAITING_ARRIVAL 状态可用 |

### 2.2 233 §3 "角色定义(本版 P0-5 修正)"完整提取

| 角色 | 业务身份 | 范围 | 来源 |
|---|---|---|---|
| **ADMIN** | 管理员 | 全量 | 233 §3 |
| **RECEP** | 预约员 / 前台 | 预约 + 签到 | 233 §3 |
| **TRIAGE** | 分诊员 | 分诊全流程 | 233 §3 |
| **DOCTOR** | 医生 / 验光师 | 接诊 / 叫号 / 转诊 / 暂停 | 233 §3 |
| **STAFF** | 普通员工 | 仅签到(API-016 限定)| 233 §3 |
| **PATIENT_SELF** | 患者自助(本版 P0-5 新增)| 仅 CONFIRMED / WAITING_ARRIVAL 状态可取消(API-004 限定)| 233 §3 |
| **API-040 = PUBLIC** | 公开访问(无鉴权)| 仅 API-040 | 233 §2 第 83 行 |

**233 §3 明确 6 个角色 + API-040 是 PUBLIC(不是角色)**

---

## §3 API-001 ~ API-024 逐 API 核验

### 3.1 逐 API 独立核验表

| API | G2-02 §4.1 描述 | 233 §2 真实冻结 | 核对 | 严重度 |
|:-:|---|---|---|:-:|
| **API-001** | POST /api/appointment/create | POST /api/appointment/create,RECEP / ADMIN,Appointment → DRAFT | ✅ **PASS** | — |
| **API-002** | **POST /api/appointment/cancel** | **PUT /api/appointment/update**,RECEP / ADMIN,更新字段(不变更状态)| **🔴 P0-A5**(G2 错位 + Method 错)| **P0** |
| **API-003** | POST /api/appointment/confirm | POST /api/appointment/confirm,RECEP / ADMIN,DRAFT → CONFIRMED / WAITING_ARRIVAL | ✅ **PASS** | — |
| **API-004** | **POST /api/appointment/reschedule** | **POST /api/appointment/cancel**,RECEP / ADMIN / **PATIENT_SELF**(状态限定),任意非终态 → CANCELLED,currentVisitId 保持原值(P0-1)| **🔴 P0-A6**(G2 错位)| **P0** |
| **API-005** | **GET /api/appointment/list** | **POST /api/appointment/reschedule**,RECEP / ADMIN,旧 → RESCHEDULED + 新 CONFIRMED | **🔴 P0-A7**(G2 错位 + Method 错)| **P0** |
| **API-006** | **GET /api/patient/list** | **GET /api/appointment/detail**,RECEP / TRIAGE / DOCTOR / ADMIN,无状态动作 | **🔴 P0-A8**(G2 错位:把 patient/list 当 API-006,实际 API-006 = appointment/detail)| **P0** |
| **API-007** | **GET /api/customer/list** | **POST /api/appointment/list**,RECEP / TRIAGE / DOCTOR / ADMIN,无 | **🔴 P0-A9**(G2 错位 + Method 错)| **P0** |
| **API-008** | **POST /api/schedule/create** | **GET /api/appointment/today**,RECEP / DOCTOR / ADMIN,无 | **🔴 P0-A10**(G2 错位 + Method 错)| **P0** |
| **API-009** | **POST /api/schedule/update** | **POST /api/schedule/create**,ADMIN,创建 ACTIVE / INACTIVE | **🔴 P0-A11**(G2 错位)| **P0** |
| **API-010** | **GET /api/schedule/list** | **PUT /api/schedule/update**,ADMIN,更新字段 | **🔴 P0-A12**(G2 错位 + Method 错)| **P0** |
| **API-011** | **POST /api/slot/create** | **POST /api/schedule/publish**,ADMIN,INACTIVE → ACTIVE(P0-3 修正,无 DRAFT)| **🔴 P0-A13**(G2 错位:Slot 模块被 Schedule 模块替换)| **P0** |
| **API-012** | **GET /api/slot/list** | **POST /api/schedule/cancel**,ADMIN,ACTIVE / INACTIVE → CANCELLED | **🔴 P0-A14**(G2 错位)| **P0** |
| **API-013** | **POST /api/consultroom/create** | **GET /api/schedule/detail**,ADMIN / DOCTOR / RECEP,无 | **🔴 P0-A15**(G2 错位:ConsultRoom 模块被 Schedule 模块替换 + Method 错)| **P0** |
| **API-014** | **GET /api/consultroom/list** | **POST /api/schedule/list**,ADMIN / DOCTOR / RECEP,无 | **🔴 P0-A16**(G2 错位 + Method 错)| **P0** |
| **API-015** | **GET /api/employee/list** | **POST /api/schedule/slot/close**,ADMIN,AVAILABLE / FULL → CLOSED | **🔴 P0-A17**(G2 错位:Employee 模块被 Schedule 模块替换 + Method 错)| **P0** |
| **API-016** | POST /api/arrival/checkin | POST /api/arrival/checkin,RECEP / STAFF / ADMIN,4 对象同步创建 | ✅ **PASS** | — |
| **API-017** | POST /api/arrival/cancel | POST /api/arrival/cancel,ADMIN,默认禁用(229 §3.2.4)| ✅ **PASS** | — |
| **API-018** | **GET /api/arrival/list** | **POST /api/arrival/list**,RECEP / TRIAGE / DOCTOR / ADMIN,无 | **🟡 P1-B1**(Method 错位:GET vs POST)| **P1** |
| **API-019** | **GET /api/triage/pool-list** | **POST /api/triage/list**,TRIAGE / ADMIN,无 | **🔴 P0-A18**(G2 错位:Path 错 + Method 错)| **P0** |
| **API-020** | POST /api/triage/auto-assign | POST /api/triage/auto-assign,ADMIN,IN_POOL → ASSIGNED(批量)| ✅ **PASS** | — |
| **API-021** | POST /api/triage/assign | POST /api/triage/assign,TRIAGE / ADMIN,IN_POOL → ASSIGNED | ✅ **PASS** | — |
| **API-022** | **POST /api/triage/skip** | **POST /api/triage/reassign**,TRIAGE / ADMIN,ASSIGNED → IN_POOL | **🔴 P0-A19**(G2 错位)| **P0** |
| **API-023** | **GET /api/triage/list** | **POST /api/triage/remove**,TRIAGE / ADMIN,IN_POOL → REMOVED | **🔴 P0-A20**(G2 错位 + Method 错)| **P0** |
| **API-024** | POST /api/queue/start | POST /api/queue/start,DOCTOR,ASSIGNED → WAITING | ✅ **PASS** | — |

### 3.2 错位规律(系统性问题)

> **G2-Contract-02 §4.1 API-001~024 的错位不是随机,而是系统性偏移**:
>
> - API-002 / 004 / 005 / 006 / 007:**G2 的 API-002~007 是 233 的 API-001~006 内容顺延 / 错位**
> - API-008 ~ API-015:**G2 把 Schedule 模块整个错位到 Slot / ConsultRoom / Employee 模块**
> - API-018 ~ API-023:**Triage 模块错位**
>
> **根因**:G2-02 似乎假设 232 是基线,但**没有按 233 §2 修正版重新对齐**。

### 3.3 API-025 ~ API-040 复检

| API | G2-02 §4.1 | 233 §2 | 核对 |
|---|---|---|:-:|
| API-025 | POST /api/visit/create-direct | POST /api/visit/create-direct,ADMIN | ✅ |
| API-026 | POST /api/queue/next | POST /api/queue/next,DOCTOR | ✅ |
| API-027 | POST /api/queue/call | POST /api/queue/call,DOCTOR | ✅ |
| API-028 | POST /api/queue/skip | POST /api/queue/skip,DOCTOR | ✅ |
| API-029 | POST /api/queue/recall | POST /api/queue/recall,DOCTOR | ✅ |
| API-030 | POST /api/queue/start-consult | POST /api/queue/start-consult,DOCTOR | ✅ |
| API-031 | POST /api/queue/complete | POST /api/queue/complete,DOCTOR | ✅ |
| API-032 | GET /api/queue/console | GET /api/queue/console,DOCTOR | ✅ |
| API-033 | GET /api/queue/room | GET /api/queue/room,TRIAGE / DOCTOR / ADMIN | ✅ |
| API-034 | POST /api/visit/transfer | POST /api/visit/transfer,DOCTOR(转出方)/ ADMIN,7 对象联动 | ✅ |
| API-035 | POST /api/visit/cancel-direct | POST /api/visit/cancel-direct,ADMIN | ✅ |
| **API-036** | **GET** /api/visit/list-by-appointment | **POST** /api/visit/list-by-appointment | **🟡 P1-B2**(Method 错位:GET vs POST)|
| API-037 | POST /api/doctor/pause | POST /api/doctor/pause,DOCTOR,WORKING → PAUSED | ✅ |
| API-038 | POST /api/doctor/resume | POST /api/doctor/resume,DOCTOR,PAUSED → WORKING | ✅ |
| API-039 | GET /api/bigscreen/list | GET /api/bigscreen/list,ADMIN | ✅ |
| API-040 | GET /api/bigscreen/display | GET /api/bigscreen/display,**PUBLIC** | ✅ |

### 3.4 API 冲突唯一编号列表

| 序号 | 严重度 | API 编号 | 冲突类型 |
|--:|:-:|:-:|---|
| 1 | 🔴 P0 | **API-002** | Path 错位 + Method 错 |
| 2 | 🔴 P0 | **API-004** | Path 错位 |
| 3 | 🔴 P0 | **API-005** | Path 错位 + Method 错 |
| 4 | 🔴 P0 | **API-006** | Path 错位 |
| 5 | 🔴 P0 | **API-007** | Path 错位 + Method 错 |
| 6 | 🔴 P0 | **API-008** | Path 错位 + Method 错 |
| 7 | 🔴 P0 | **API-009** | Path 错位 |
| 8 | 🔴 P0 | **API-010** | Path 错位 + Method 错 |
| 9 | 🔴 P0 | **API-011** | Path 错位(模块替换)|
| 10 | 🔴 P0 | **API-012** | Path 错位(模块替换)|
| 11 | 🔴 P0 | **API-013** | Path 错位 + Method 错(模块替换)|
| 12 | 🔴 P0 | **API-014** | Path 错位(模块替换)|
| 13 | 🔴 P0 | **API-015** | Path 错位 + Method 错(模块替换)|
| 14 | 🔴 P0 | **API-019** | Path 错位 + Method 错 |
| 15 | 🔴 P0 | **API-022** | Path 错位 |
| 16 | 🔴 P0 | **API-023** | Path 错位 + Method 错 |
| 17 | 🟡 P1 | **API-018** | Method 错位(GET vs POST)|
| 18 | 🟡 P1 | **API-036** | Method 错位(GET vs POST)|

### 3.5 API-001~024 一致性最终统计

| 维度 | 数量 |
|---|---:|
| 一致(PASS)| **7 项**(API-001, 003, 016, 017, 020, 021, 024)|
| **P0 Contract Conflict** | **16 项** |
| P1(仅 Method 错位)| 1 项(API-018)|
| 总计 | **24 项** |

---

## §4 Security Role 独立核验

### 4.1 233 §3 真实角色集合

> 233 §3 "角色定义(本版 P0-5 修正)":

| 角色 | 业务身份 | 范围 |
|---|---|---|
| **ADMIN** | 管理员 | 全量 |
| **RECEP** | 预约员 / 前台 | 预约 + 签到 |
| **TRIAGE** | 分诊员 | 分诊全流程 |
| **DOCTOR** | 医生 / 验光师 | 接诊 / 叫号 / 转诊 / 暂停 |
| **STAFF** | 普通员工 | 仅签到(API-016 限定)|
| **PATIENT_SELF** | 患者自助(本版 P0-5 新增)| 仅 CONFIRMED / WAITING_ARRIVAL 状态可取消(API-004 限定)|
| **API-040 = PUBLIC** | 公开访问 | 仅 API-040 |

**233 §3 明确 = 6 个角色 + 1 个 PUBLIC 标识(API-040)**

### 4.2 G2-Contract-02 §9.1 角色集合

| G2-02 §9.1 列出的角色 | 来源声称 | 233 §3 是否存在 |
|---|---|:-:|
| ADMIN | 235B §2 | ✅ 存在 |
| DOCTOR | 235B §2 | ✅ 存在 |
| **NURSE** | 235B §2 | **❌ 233 §3 没有 NURSE** |
| RECEP | 235B §2 | ✅ 存在 |
| STAFF | 235B §2 | ✅ 存在 |
| **BIGSCREEN** | 233 §API-040 | **❌ 233 §3 没有 BIGSCREEN 角色;API-040 = PUBLIC,不是角色**|

**G2-Contract-02 §9.1 缺失 233 §3 中明确存在的 2 个角色**:

| G2-02 §9.1 缺失 | 233 §3 中存在 | 来源 |
|---|---|---|
| **TRIAGE** | ✅ 分诊员 | 233 §3 显式冻结 |
| **PATIENT_SELF** | ✅ 患者自助 | 233 §3 + P0-5 修正 |

### 4.3 G2-Contract-02 §9.4 / §13 / §17 角色数量自相矛盾

> G2-Contract-02 §9.4 第 1 行:
> | 7 角色完整定义 | **冻结**(233 各 API + 235B §2)|
>
> G2-Contract-02 §13 第 18 项:
> | 18 | 角色 | 7 角色完整定义(233 散落冻结)| 【待确认】|
>
> G2-Contract-02 §17.2 第 10 项:
> | 10 | 角色 | 7 角色完整定义(233 散落冻结)| 【待确认】|

**🔴 G2-02 §9.1 列了 6 个角色,但 §9.4 / §13 / §17 反复说 "7 角色完整列表 / 7 角色完整定义"**

| 项 | G2-02 §9.1(实际)| G2-02 §9.4 / §13 / §17(声称)| 233 §3(真实) |
|:-:|---|---|---|
| 角色数量 | 6 个 | 7 个 | **6 个** |
| ADMIN | ✅ | ✅ | ✅ |
| RECEP | ✅ | ✅ | ✅ |
| TRIAGE | ❌ 缺失 | ✅ | ✅ |
| DOCTOR | ✅ | ✅ | ✅ |
| STAFF | ✅ | ✅ | ✅ |
| PATIENT_SELF | ❌ 缺失 | ✅ | ✅ |
| NURSE | ❌ 自创(233 无) | — | ❌ |
| BIGSCREEN | ❌ 自创(API-040 = PUBLIC,不是角色)| — | ❌ |

### 4.4 API-040 与 BIGSCREEN 角色辨析

> 233 §2 第 83 行:
> | **API-040** | **bigscreen/display** | GET | /api/bigscreen/display | BigScreen | 无 | **PUBLIC** |

**关键**:API-040 的权限角色 = **PUBLIC**(公开访问,无需鉴权)
**不**是角色。BIGSCREEN 不是 233 §3 中的角色。

> G2-Contract-02 §9.1 第 6 行写 "BIGSCREEN" 角色,这是**自行发明**(把 API-040 的 PUBLIC 误当作角色名)。

### 4.5 Security Role P0 Contract Conflict

| # | 严重度 | 描述 |
|--:|:-:|---|
| **P0-B1** | 🔴 **P0** | G2-Contract-02 §9.1 缺失 **TRIAGE** 角色,与 233 §3 直接冲突 |
| **P0-B2** | 🔴 **P0** | G2-Contract-02 §9.1 缺失 **PATIENT_SELF** 角色,与 233 §3 P0-5 修正直接冲突 |
| **P0-B3** | 🔴 **P0** | G2-Contract-02 §9.1 自创 **NURSE** 角色,与 233 §3 直接冲突(233 §3 无 NURSE) |
| **P0-B4** | 🔴 **P0** | G2-Contract-02 §9.1 自创 **BIGSCREEN** 角色,与 233 §3 / §2 直接冲突(API-040 = PUBLIC,不是角色)|
| **P0-B5** | 🔴 **P0** | G2-Contract-02 §9.4 / §13 / §17 写"7 角色"与 233 §3 的"6 角色"直接矛盾 |

**说明**:
- B1 / B2 / B3 / B4 = Role 集合内容冲突(各计 1 项 P0)
- B5 = Role 数量矛盾(1 项 P0)
- **合计 5 项 P0**(与 G2-Contract-Audit-02 P0-A4 是不同维度,P0-A4 是 "6 vs 7 角色" 数量矛盾,P0-B1~B5 是内容 + 数量全面冲突)

### 4.6 40 API × Role 权限矩阵

> G2-Contract-02 §9.3 声称:
> | 角色 × API 权限矩阵(业务规则)| **冻结**(233 各 API + 235B §2)|

**G2-02 §9.3 写"权限矩阵冻结",§13 又把"40 API × 7 角色完整矩阵"标【待确认】**

> **🔴 P1-B6(内部矛盾)**:G2-02 §9.3 与 §13 自相矛盾
>
> 233 §2 实际是**逐 API 显式冻结权限角色**(每个 API 单独列出 Permission 列表,**没有完整矩阵**):
> - API-001:RECEP / ADMIN
> - API-002:RECEP / ADMIN
> - API-003:RECEP / ADMIN
> - API-004:RECEP / ADMIN / PATIENT_SELF(状态限定)
> - ...
>
> 完整 40 API × 7 Role 矩阵 **不存在**。
>
> 正确表达:**API-level authorization rules are frozen individually**(逐 API 冻结权限角色),完整 40×7 矩阵【待确认】。

---

## §5 40×7 权限矩阵重新判断

### 5.1 233 §3 是否冻结完整 40×7 矩阵?

> **🔴 否**:233 §3 只冻结了 6 个角色的定义 + 业务身份 + 范围。
> **233 §2 是逐 API 冻结 Permission**(每个 API 单独列可访问角色列表)。
> 完整 40×7 矩阵 = **不存在**。

### 5.2 正确表达

| 项 | 状态 |
|---|---|
| 6 角色定义 | ✅ **冻结**(233 §3)|
| 逐 API Permission 列表 | ✅ **冻结**(233 §2)|
| 完整 40×7 矩阵 | 🔴 **【待确认】**(233 未冻结完整矩阵)|
| Sa-Token annotation | 🔴 **【待确认】**(Effective Spec 未冻结)|
| Sa-Token StpInterface | 🔴 **【待确认】**|

---

## §6 与 G2-Contract-Audit-02 的关系

### 6.1 Audit-02 错误结论纠正

| Audit-02 原结论 | 本轮重新核验 | 状态 |
|---|---|---|
| **Audit-02 §3.1:"API-001~024 = PASS"** | **❌ 错误**:API-001~024 中有 **16 项 P0 Contract Conflict** + 1 项 P1 | **🔴 必须纠正** |
| Audit-02 §3.2:API-025~040 = 15 项 P0(其中 14 项 Path 错位 + 1 项顺延) | ✅ 部分正确:本轮发现 API-036 还有 1 项 P1(Method 错)| ⚠️ 补 1 项 P1 |
| Audit-02 §3.3:RC-1 修复 = COMPLETE | ❌ 错误:G2-02 §4.1 API-001~024 部分仍错,RC-1 实际只修复了 API-025~040 | 🔴 必须纠正 |
| **Audit-02 P0-A4:"6 vs 7 角色"内部矛盾** | ⚠️ 部分错误:实际 G2-02 §9.1 列的 6 个角色中 2 个是自创(NURSE / BIGSCREEN),且缺失 2 个真实角色(TRIAGE / PATIENT_SELF);233 §3 实际只有 6 角色(没有"7 角色")| **🔴 必须纠正** |
| Audit-02 P0-A1 / A2:user_company SQL | ✅ 保持 |
| Audit-02 P0-A3:Transfer Rollback 矛盾 | ✅ 保持 |
| Audit-02 P1-A1~A4:Service / 权限矩阵矛盾 | ✅ 保持 |
| Audit-02 RC-2/3/4/5/6 PASS | ✅ 保持 |
| Audit-02 PA-02/04/05/06 PASS | ✅ 保持 |

### 6.2 Audit-02 漏掉的 P0(本轮发现)

| # | 类别 | API 编号 | 严重度 |
|--:|---|---|:-:|
| P0-A5 | API Path 错位 + Method 错 | API-002 | 🔴 P0 |
| P0-A6 | API Path 错位 | API-004 | 🔴 P0 |
| P0-A7 | API Path 错位 + Method 错 | API-005 | 🔴 P0 |
| P0-A8 | API Path 错位 | API-006 | 🔴 P0 |
| P0-A9 | API Path 错位 + Method 错 | API-007 | 🔴 P0 |
| P0-A10 | API Path 错位 + Method 错 | API-008 | 🔴 P0 |
| P0-A11 | API Path 错位 | API-009 | 🔴 P0 |
| P0-A12 | API Path 错位 + Method 错 | API-010 | 🔴 P0 |
| P0-A13 | API Path 错位(模块替换)| API-011 | 🔴 P0 |
| P0-A14 | API Path 错位(模块替换)| API-012 | 🔴 P0 |
| P0-A15 | API Path 错位 + Method 错 | API-013 | 🔴 P0 |
| P0-A16 | API Path 错位(模块替换)| API-014 | 🔴 P0 |
| P0-A17 | API Path 错位 + Method 错 | API-015 | 🔴 P0 |
| P0-A18 | API Path 错位 + Method 错 | API-019 | 🔴 P0 |
| P0-A19 | API Path 错位 | API-022 | 🔴 P0 |
| P0-A20 | API Path 错位 + Method 错 | API-023 | 🔴 P0 |
| P0-B1 | Role 缺失 | TRIAGE | 🔴 P0 |
| P0-B2 | Role 缺失 | PATIENT_SELF | 🔴 P0 |
| P0-B3 | Role 自创 | NURSE | 🔴 P0 |
| P0-B4 | Role 自创(BIGSCREEN vs PUBLIC)| API-040 标识错 | 🔴 P0 |
| P0-B5 | Role 数量矛盾(7 vs 6)| §9.4 / §13 / §17 | 🔴 P0 |
| P1-B1 | Method 错位(GET vs POST)| API-018 | 🟡 P1 |
| P1-B2 | Method 错位(GET vs POST)| API-036 | 🟡 P1 |
| P1-B6 | 权限矩阵矛盾 | §9.3 vs §13 | 🟡 P1 |

---

## §7 累计 P0 / P1 全局汇总

### 7.1 累计 P0 Contract Conflict

| 来源 | 编号 | 数量 |
|---|---|---:|
| Audit-02 已发现 | P0-A1 / A2(user_company SQL)+ P0-A3(Transfer Rollback 矛盾)+ P0-A4(6 vs 7 角色数量矛盾) | 4 项 |
| **Audit-02A 新发现(API Path 错位 16 项)**| **P0-A5 ~ A20** | **16 项** |
| **Audit-02A 新发现(Role 内容 4 项)**| **P0-B1 / B2(缺失)+ P0-B3 / B4(自创)+ P0-B5(数量矛盾扩展)** | **5 项** |
| **累计 P0** | | **25 项** |

### 7.2 累计 P1 Contract Gap

| 来源 | 编号 | 数量 |
|---|---|---:|
| Audit-02 已发现 | P1-A1(Repository 误升级)+ P1-A2(`parseConsultRoomIdArray` 自创)+ P1-A3(Service 方法名 / 业务概念自创)+ P1-A4(权限矩阵矛盾)| 4 项 |
| **Audit-02A 新发现** | **P1-B1 / B2(API Method 错位)+ P1-B6(权限矩阵矛盾扩展)** | **3 项** |
| **累计 P1** | | **7 项** |

---

## §8 最终输出

### A. API-001~024 实际冲突数量

> **🔴 16 项 P0 Contract Conflict + 1 项 P1 Contract Gap(API-018 Method 错)= 17 项冲突**

### B. API 冲突唯一编号列表

> **P0:API-002 / 004 / 005 / 006 / 007 / 008 / 009 / 010 / 011 / 012 / 013 / 014 / 015 / 019 / 022 / 023(16 项)**
> **P1:API-018(Method 错)**
> **API-036(Method 错)已在 §3.3 中另列(P1)**

### C. Security Role 实际有效集合

> **233 §3 明确 6 个角色**:
> 1. **ADMIN**(管理员)
> 2. **RECEP**(预约员 / 前台)
> 3. **TRIAGE**(分诊员)
> 4. **DOCTOR**(医生 / 验光师)
> 5. **STAFF**(普通员工)
> 6. **PATIENT_SELF**(患者自助,233 §3 P0-5 新增)
>
> **API-040 = PUBLIC**(公开访问,**不是角色**)

### D. G2-02 Role Contract 是否存在直接冲突

> **🔴 是(5 项 P0 直接冲突)**:
> - 缺失 **TRIAGE**(实际存在)
> - 缺失 **PATIENT_SELF**(实际存在)
> - 自创 **NURSE**(实际不存在)
> - 自创 **BIGSCREEN**(API-040 = PUBLIC,不是角色)
> - "7 角色"数量矛盾(实际只有 6 个)

### E. 新增独立 P0 数量

> **本轮新增 21 项独立 P0**:
> - 16 项 API Path 错位(P0-A5 ~ A20)
> - 5 项 Role 直接冲突(P0-B1 / B2 / B3 / B4 / B5)
>
> 累计全部 P0(Audit-02 + Audit-02A)= **25 项**

### F. Audit-02 原结论哪些保持

| 结论 | 状态 |
|---|:-:|
| Audit-02 §3.1 "API-001~024 = PASS" | ❌ **错误**(本轮发现 17 项冲突)|
| Audit-02 §3.2 "API-025~040 = 15 项 P0"(部分正确,API-036 还需 P1)| ⚠️ 部分 |
| Audit-02 §3.3 "RC-1 修复 = COMPLETE" | ❌ **错误**(只修复 API-025~040,API-001~024 仍错)|
| Audit-02 P0-A1 / A2(user_company SQL)| ✅ 保持 |
| Audit-02 P0-A3(Transfer Rollback 矛盾)| ✅ 保持 |
| Audit-02 P0-A4(6 vs 7 角色数量矛盾)| ⚠️ 部分错误(实际 G2 §9.1 6 角色中 2 自创 + 2 缺失)|
| Audit-02 P1-A1 ~ A4 | ✅ 保持 |
| Audit-02 RC-2 / 3 / 4 / 5 / 6 PASS | ✅ 保持 |
| Audit-02 PA-02 / 04 / 05 / 06 PASS | ✅ 保持 |
| Audit-02 G2-Contract-02 = BLOCK | ✅ 保持 |
| Audit-02 Backend Entry = BLOCK | ✅ 保持 |

### G. G2-Contract-03 是否仍 BLOCK

> **是**。G2-Contract-02 = **BLOCK**(累计 25 项 P0 + 7 项 P1)
>
> 进入 G2-Contract-03 前**最少必须修复 21 项新 P0**(16 API Path 错位 + 5 Role 冲突)+ 3 项新 P1(API Method 错 + 权限矩阵矛盾)。

### H. Backend Entry 是否继续 BLOCK

> **是**(沿用 S1-170E §12 + Audit-02 §17.4)

---

## §9 最少必须修复项(本轮新增)

### 9.1 G2-Contract-02 §4.1 API Path 16 项修复

| # | API | G2-02 错 | 233 真实 | 修复路径 |
|--:|---|---|---|---|
| 1 | API-002 | POST /api/appointment/cancel | PUT /api/appointment/update | 改 Path + Method |
| 2 | API-004 | POST /api/appointment/reschedule | POST /api/appointment/cancel | 改 Path |
| 3 | API-005 | GET /api/appointment/list | POST /api/appointment/reschedule | 改 Path + Method |
| 4 | API-006 | GET /api/patient/list | GET /api/appointment/detail | 改 Path |
| 5 | API-007 | GET /api/customer/list | POST /api/appointment/list | 改 Path + Method |
| 6 | API-008 | POST /api/schedule/create | GET /api/appointment/today | 改 Path + Method |
| 7 | API-009 | POST /api/schedule/update | POST /api/schedule/create | 改 Path |
| 8 | API-010 | GET /api/schedule/list | PUT /api/schedule/update | 改 Path + Method |
| 9 | API-011 | POST /api/slot/create | POST /api/schedule/publish | 改 Path + 模块 |
| 10 | API-012 | GET /api/slot/list | POST /api/schedule/cancel | 改 Path + 模块 |
| 11 | API-013 | POST /api/consultroom/create | GET /api/schedule/detail | 改 Path + Method + 模块 |
| 12 | API-014 | GET /api/consultroom/list | POST /api/schedule/list | 改 Path + Method + 模块 |
| 13 | API-015 | GET /api/employee/list | POST /api/schedule/slot/close | 改 Path + Method + 模块 |
| 14 | API-019 | GET /api/triage/pool-list | POST /api/triage/list | 改 Path + Method |
| 15 | API-022 | POST /api/triage/skip | POST /api/triage/reassign | 改 Path |
| 16 | API-023 | GET /api/triage/list | POST /api/triage/remove | 改 Path + Method |

### 9.2 G2-Contract-02 §9.1 Role 5 项修复

| # | 修复路径 |
|--:|---|
| 1 | 删 **NURSE**(233 §8 自创) |
| 2 | 删 **BIGSCREEN**(API-040 = PUBLIC,不是角色)|
| 3 | 增 **TRIAGE**(233 §8 真实存在) |
| 4 | 增 **PATIENT_SELF**(233 §8 P0-5 新增) |
| 5 | §9.4 / §13 / §17 全文统一改为 "6 角色"(删"7 角色"字样)|

### 9.3 G2-Contract-02 §4.1 API Method 1 项修复

| # | API | G2-02 | 233 | 修复 |
|--:|---|---|---|---|
| 1 | API-018 | GET /api/arrival/list | POST /api/arrival/list | 改 Method |
| 2 | API-036 | GET /api/visit/list-by-appointment | POST /api/visit/list-by-appointment | 改 Method |

### 9.4 G2-Contract-02 §9.3 / §13 权限矩阵修复

| # | 修复路径 |
|--:|---|
| 1 | §9.3 改为:API-level authorization rules are frozen individually(逐 API 冻结)|
| 2 | §13 保持:"40 API × 6 角色完整矩阵"【待确认】(233 未冻结完整矩阵)|
| 3 | 全文"7 角色"改为"6 角色" |

---

## §10 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-02A_233前24API与Security角色补充核验.md` |
| 创建时间 | 2026-09-17 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-02 / 不修改 G2-Contract-Audit-02 / 不修改任何已有审计文件 / 不修改任何历史 MD |
| 严禁 | 修改任何已有文件 / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

**End of G2-Contract-Audit-02A**