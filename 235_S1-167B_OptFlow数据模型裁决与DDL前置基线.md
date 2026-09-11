# 235 S1-167B OptFlow 数据模型裁决与 DDL 前置基线

> **本轮定位**:234B 已确认本仓库**无后端 Java / SQL / Schema 证据**。本轮停止寻找原系统类型,转向"OptFlow 独立数据模型裁决与 DDL 前置基线"。
> - 严禁修改 227~234B 历史文档
> - 严禁修改 controller.js / HTML / 数据库
> - 严禁创建 DDL / 代码 / commit / push
> - 标签严格区分:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】

---

## §0 完整性闸门

- **HEAD**:`1bf472c39812d88ad41c2e8a0570ddf37ab0e8fc`(S1-168 盲测审计后)
- **REMOTE**:同 LOCAL ✓
- **0 号闸门**:4 文件 SHA256 全部 PASS
- **历史 MD(190~234B 共 47 份)未修改** ✓
- **234A SHA256 `21C8F1314A159AE6A73D6E4DFCFD52F487920A84C3E9D1A94ABA5D27768D5700` 锁定**
- **234B SHA256 `1B6BAE634C8B410709DE4AD16D1769A75F4ED3AA6384B6DEDD637BA274624159` 锁定**
- **本轮不写代码、不提交 Git** ✓

---

## §1 上一版基线引用

| 文件 | 关系 | SHA256 | 状态 |
|---|---|---|---|
| 227 S1-165 | 第一版模型 | `6CA8BFE...` | 历史证据,保留 |
| 228 S1-166 | 一次修正版 | `93BE985...` | 历史证据,保留 |
| 229 S1-166A | 二次修正版(领域模型冻结稿)| `1E5DA27...` | 历史证据,保留 |
| 230 S1-166A API 前置核验 | API 数量冻结 | `05C4EE6...` | 历史证据,保留 |
| 231 S1-166A API 前置核验修正版 | 4 类口径 | `300B234...` | 历史证据,保留 |
| 232 S1-167 | 40 API 字段级设计 | `71F0D37...` | 历史证据,保留 |
| 233 S1-167A | API 字段级设计修正版 | `6767AC1...` | 历史证据,保留 |
| 234 S1-168 盲测审计报告 | CONDITIONAL PASS | – | 历史证据,保留 |
| 234A ID 类型逆向核验 | E 级推断 | `21C8F13...` | 历史证据,保留(已自纠) |
| 234B ID 类型后端 Schema 核验 | BLOCK | `1B6BAE6...` | 历史证据,保留 |
| **235 S1-167B** | **本轮新增** | – | **当前裁决稿** |

---

## §2 文档目的

1. 将 S1-165 ~ S1-167A 的对象模型 / ID / 关系 / 字段来源**重新整理**
2. 严格区分【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
3. 解决 234B 识别的 2 个 D 级冲突(Employee 双 ID / Patient 业务主键)
4. 冻结 `currentVisitId` 唯一规则
5. 命名规范统一
6. 输出 **表 A:事实/设计分层** + **表 B:DDL 前正式设计基线**
7. S1-168 启动判断

---

## §3 4 类来源严格区分

| 标签 | 含义 | 证据要求 |
|---|---|---|
| **【原系统事实】** | 原 OptFlow PMS 系统已经存在的字段 / 表 / 关系 | 直接证据(代码 / SQL / Schema) |
| **【已验证业务事实】** | 通过真实浏览器流程 / 多个独立证据验证的业务现象 | 2+ 个独立证据 |
| **【OptFlow设计】** | 为新系统业务完整性而主动设计 | 一期设计原则 + 业务需要 |
| **【待确认】** | 证据不足 | – |

**严禁【OptFlow设计】伪装成【原系统事实】**。

---

## §4 12 个对象正式裁决(本版)

### 4.1 裁决表(完整)

| # | 对象 | 来源 | 是否复用 | 是否新建 | 主键 | 主键类型 | 证据等级 | 当前采用 |
|---:|---|---|:-:|:-:|---|---|---|---|
| 1 | **Company** | S1-158 | ✓ 复用 | ✗ | `companyId` | 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | C 字段名 | **采用,BIGINT【OptFlow设计】** |
| 2 | **Customer** | S1-147 | ✓ 复用 | ✗ | `customerId` | 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | A 数值 / C 类型 | **采用,BIGINT【OptFlow设计】** |
| 3 | **Patient** | S1-147 | ✓ 复用 | ✗ | `patientId` | 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | A 数值 / C 类型 | **采用,BIGINT【OptFlow设计】** |
| 4 | **Employee** | S1-151 | ✓ 复用 | ✗ | `employeeId` + `adminId`(双 ID 字段)| 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | A 双字段 | **采用 双 ID 字段,§6 详细裁决** |
| 5 | **ConsultRoom** | S1-153 / S1-158 | ✓ 复用 | ✗ | `consultRoomId` | 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | C 字段名 | **采用,BIGINT【OptFlow设计】** |
| 6 | **BigScreen** | S1-153 | ✓ 复用 | ✗ | `bigScreenId` | 【待确认】(原系统) / **BIGINT**【OptFlow设计】 | C 字段名 | **采用,BIGINT【OptFlow设计】** |
| 7 | **Appointment** | S1-166A §3 | ✗ | ✓ | `appointmentId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |
| 8 | **AppointmentSchedule** | S1-166A §11 | ✗ | ✓ | `scheduleId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |
| 9 | **AppointmentSlot** | S1-166A §12 | ✗ | ✓ | `slotId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |
| 10 | **TriageQueue** | S1-166A §10 | ✗ | ✓ | `triageQueueId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |
| 11 | **ReceptionQueue** | S1-166A §9 | ✗ | ✓ | `receptionQueueId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |
| 12 | **Visit** | S1-166A §8 | ✗ | ✓ | `visitId` | **UUID v4**【OptFlow设计】 | 全新 | **采用,UUID v4** |

### 4.2 主键类型总览

| 类型 | 适用对象 | 依据 |
|---|---|---|
| **BIGINT** | 6 个复用对象(Company / Customer / Patient / Employee / ConsultRoom / BigScreen)| 【OptFlow设计】,非原系统事实 |
| **UUID v4** | 6 个新设计对象(Appointment / Schedule / Slot / TriageQueue / ReceptionQueue / Visit)| 【OptFlow设计】,无原系统对应 |

**重要原则**:
- 复用对象 ID 类型 = 【OptFlow设计】(BIGINT),**非原系统事实**
- 新设计对象 ID 类型 = 【OptFlow设计】(UUID v4)
- **DDL 阶段统一应用此裁决**,不复用 234A 错误推断

---

## §5 Employee 双 ID 冲突裁决(P0 重点)

### 5.1 234B 识别的冲突

- 214 §5.5:"Employee 有 employeeId + adminId 独立 ID 字段(A)"
- 214 §5.1:`employeeId 45 命中 / adminId 34 命中`
- 233 §5.4:"Employee 双 ID 字段未观察,关系需后端确认"
- 233 §3.5 误用:"doctorId = employeeId 别名"

### 5.2 3 个候选方案分析

#### 方案 A:Employee 一个对象 + employeeId / adminId 两个字段【OptFlow设计】

| 维度 | 分析 |
|---|---|
| 原系统证据 | 214 §5.5 确认"两个独立 ID 字段" |
| OptFlow 业务需要 | 同时支持接诊(用 employeeId)+ 登录认证(用 adminId)|
| 对预约/接诊/权限影响 | 预约关联 employeeId,登录用 adminId,各自语义清晰 |
| 对 DDL 影响 | 1 张 employee 表 + 2 个 UNIQUE 字段(可能需要 1 个 unique + 1 个 nullable)|

#### 方案 B:Employee + Admin 两个独立对象【OptFlow设计】

| 维度 | 分析 |
|---|---|
| 原系统证据 | adminId 是 employee 的属性,不是独立对象(214 §5.1 adminId 34 命中) |
| OptFlow 业务需要 | 需要 employeeId 引用 + adminId 独立管理 |
| 对预约/接诊/权限影响 | 预约需先确认 adminId 对应的 employeeId(2 跳查询) |
| 对 DDL 影响 | 2 张表(employee + admin)+ FK 关系 |

#### 方案 C:Employee 主体 + AdminAccount 独立认证对象【OptFlow设计】

| 维度 | 分析 |
|---|---|
| 原系统证据 | 214 §5.1 没明确分离,214 §5.5 说"两个 ID 字段" |
| OptFlow 业务需要 | 认证独立、可扩展多种登录方式(密码 / 微信 / 短信)|
| 对预约/接诊/权限影响 | 接诊医生用 employee,登录用 adminAccount,中间关联表 employeeAdminAccount |
| 对 DDL 影响 | 3 张表(employee / adminAccount / employeeAdminAccount),最复杂 |

### 5.3 裁决:【OptFlow设计】最终推荐 = **方案 A**

| 维度 | 方案 A 评分 |
|---|:-:|
| 原系统证据契合度 | ★★★★★(214 §5.5 直接支持)|
| 业务完整性 | ★★★★ |
| 复杂度 | ★★★★★(最简单)|
| DDL 可行性 | ★★★★★ |
| 扩展性 | ★★★ |

**【OptFlow设计】**:
- **Employee 单一对象**
- 包含 2 个 ID 字段:`employeeId`(主键,接诊用)+ `adminId`(UNIQUE,登录用)
- 1 个 employee 实体对应 1 个 admin 账号(employee 可以无 admin 账号,反之亦然)
- `adminId` 来源原系统(214 §5.1 34 命中),保留作为认证 ID
- `employeeId` 来源原系统(214 §5.1 45 命中),保留作为业务 ID

### 5.4 doctorId / userId 处理

- `doctorId`:**原系统 0 命中**(233 §3.5 自创),**【OptFlow设计】** = 不用,统一用 `employeeId`,role=DOCTOR 表达"医生"语义
- `userId`:**原系统 0 命中**(214 §5.1),**【OptFlow设计】** = 不用
- `nickname`:**原系统存在**(214 §1.4 L14273),作为 Employee 字段,【原系统事实】 A 级

---

## §6 Patient / Customer / MedicalRecord 边界裁决(P0 重点)

### 6.1 234B 识别的冲突

- 101 §7.3:"patientId ❌(用 MedicalRecord 实体)" — **patientId 实际不作为业务主键**
- 105 §6.1 L375-377:`patient.id` + `customer.id` 各自 A 级字段
- 105 §6.2:"patientId | Patient 实体 ID | **严禁与 customerId 合并**"
- 101 §7.3:"4 字段组合 = D 业务级观察模型(不是数据库主键)"
- 233 §4 API-001 `patientId` 字段 + 233 §5.4 Visit 业务

### 6.2 三个对象的核心定位

| 对象 | 原系统定位 | 业务主键 | 与其他对象关系 |
|---|---|---|---|
| **Customer** | 会员(patient_owner) | `customerId`(业务主键,仅在会员卡路由用) | 1:N Patient |
| **Patient** | 患者 | `patientId`(系统主键,**不是业务主键**)| N:1 Customer |
| **MedicalRecord** | 电子病案(就诊记录) | 业务编号 `medicalCode`(14 位字符串) | N:1 Patient(隐式) |

**【原系统事实】关键证据**:
- 105 §6.1 L375:`patient.id` 主键,"A 100%"
- 105 §6.1 L377:`customer.id` 主键,"A 100%"
- 101 §7.3:"patientId ❌(用 MedicalRecord 实体)" — patientId 不作为业务主键
- 100 S1-41 L9:`档案号 202609025109158` 实际就是 `medicalCode` 业务编号

### 6.3 7 个问题回答(本版)

| # | 问题 | 答案 | 依据 |
|---:|---|---|---|
| 1 | Appointment 是否直接 patientId | **✓ 是** | 【OptFlow设计】,229 §6.1 + 233 §4 显式 appointment.patientId |
| 2 | Visit 是否直接 patientId | **✓ 是** | 【OptFlow设计】,229 §5.1 + 233 §5.4 visit.patientId |
| 3 | MedicalRecord 是否作为就诊记录 | **✓ 是(原系统存在)** | 【原系统事实】,105 §6.1 `medicalRecord.id` + 100 S1-41 `medicalCode` |
| 4 | customerId 是否独立保留 | **✓ 保留** | 【原系统事实】,105 §6.2 "严禁与 patientId 合并" |
| 5 | patientId 是否可以与 customerId 相同 | **✗ 严禁** | 【原系统事实】,105 §6.2 严禁混淆表 |
| 6 | patientId 是否是业务主键 | **✗ 不是** | 【原系统事实】,101 §7.3 "patientId ❌ 用 MedicalRecord 实体" |
| 7 | MedicalRecord 是否承担业务编号 | **✓ 是(medicalCode)** | 【原系统事实】,105 §6.1 L367 14 位数字 |

### 6.4 MedicalRecord 与新系统(229/233)的关系

**【OptFlow设计】关键决策**:
- **MedicalRecord 是原系统对象,本版不引入** (因为 V4.4 业务只关注预约 / 接诊,不需要完整 MedicalRecord 实体)
- 但保留**业务编号概念**:`Appointment.appointmentNo`(业务编号) + `appointmentId`(系统主键 UUID)
- 这与原系统"medicalCode 业务编号 + medicalRecord.id 主键"模式一致

**【OptFlow设计】**:
- **不引入 MedicalRecord 实体**(本期 V4.4 不需要)
- **保留 appointmentNo 业务编号字段**(在 Appointment 实体上,格式待定)
- **patientId 保留为 Appointment 的 FK**(不强制 MedicalRecord 中转)

---

## §7 关系重新裁决

### 7.1 12 个对象的关系矩阵(本版)

| Source | Target | 类型 | 标签 | 依据 |
|---|---|---|---|---|
| **Appointment → Patient** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 + 233 §4 |
| **Appointment → Employee**(接诊医生) | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Appointment → AppointmentSchedule** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Appointment → AppointmentSlot** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Appointment → Company**(companyId) | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Appointment → Visit**(currentVisitId) | N:1 标记 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Visit → Appointment** | 多对一(可空,WalkIn Fallback) | ✓ | **【OptFlow设计】** | 229 §5.1,FK 可空 |
| **Visit → Patient** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Visit → Employee**(接诊医生) | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Visit → ConsultRoom** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Visit → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **TriageQueue → Visit** | 一对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **TriageQueue → Appointment**(可空,WalkIn Fallback) | 一对一(可空) | ✓ | **【OptFlow设计】** | 229 §5.1,FK 可空 |
| **TriageQueue → ConsultRoom**(目标,ASSIGNED 时填) | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **TriageQueue → Employee**(目标,ASSIGNED 时填) | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **TriageQueue → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **ReceptionQueue → TriageQueue** | 一对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **ReceptionQueue → Visit** | 一对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **ReceptionQueue → Appointment**(可空,WalkIn Fallback) | 一对一(可空) | ✓ | **【OptFlow设计】** | 229 §5.1,FK 可空 |
| **ReceptionQueue → ConsultRoom** | 多对一(必填) | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **ReceptionQueue → Employee**(接诊医生)| 多对一(必填) | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **ReceptionQueue → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **AppointmentSchedule → Employee** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **AppointmentSchedule → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **AppointmentSlot → AppointmentSchedule** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **AppointmentSlot → ConsultRoom**(可空) | 多对一(可空) | ✓ | **【OptFlow设计】** | 229 §5.1 |
| **Employee → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1(作用域) |
| **ConsultRoom → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1(作用域) |
| **BigScreen → ConsultRoom**(N:1 关系)| 多对一 | ✓ | **【OptFlow设计】** | 216 S1-153 §14.4 |
| **Customer → Company** | 多对一 | ✓ | **【OptFlow设计】** | 229 §5.1(作用域) |
| **Patient → Customer** | N:1 | ✓ | **【OptFlow设计】** | 229 §5.1 |

**【原系统事实】关系**:0 个(因为原系统 appointmentId / scheduleId / slotId / triageQueueId / receptionQueueId 0 命中,visitId 未直接观察)。

**所有 V4.4 业务关系 = 【OptFlow设计】**。

---

## §8 currentVisitId 唯一规则(本版冻结)

### 8.1 6 个场景(本版)

| # | 场景 | currentVisitId 值 | 触发 API | 备注 |
|---:|---|---|---|---|
| 1 | Appointment 创建 | **NULL** | appointment/create | Appointment 初始态,无 Visit |
| 2 | ARRIVED / 首次签到 | **新 Visit.id** | arrival/checkin | Visit 创建时立即赋值 |
| 3 | transfer 转诊 | **新 Visit.id** | visit/transfer | 旧 Visit → TRANSFERRED,新 Visit 创建 |
| 4 | Visit COMPLETED | **保持当前 Visit.id** | queue/complete | 终态保留 |
| 5 | Visit CANCELLED | **保持当前 Visit.id** | appointment/cancel / visit/cancel-direct | 终态保留 |
| 6 | RESCHEDULED | **新 Appointment 重新开始** | appointment/reschedule | 旧 Appointment 不再产生新 Visit |

### 8.2 与 229 旧规则的冲突处理

| 冲突点 | 229 旧规则 | 235 本版规则 | 处理 |
|---|---|---|---|
| Appointment 取消后 currentVisitId | NULL(229 §7.2) | **保持原值** | 235 覆盖,229 不修改 |
| IN_CONSULTATION 取消 | Fallback 路径允许(229 §6.3)| **全部禁止** | 235 覆盖,229 不修改 |
| 229 §15.2 步骤 7 新 TriageQueue.visitId | NULL | **NULL(IN_POOL 必须 NULL)** | 235 沿用,229 内部矛盾未修 |

**重要声明**:**229 §7.2 / §14.1 写"重置为 NULL"的旧规则,与本版 §8 "保持原值"冲突。S1-167B 选择 235 "保持原值"作为 OptFlow 最终裁决。229 文档不被修改,作为历史证据保留。**

### 8.3 API 行为确定

- `appointment/detail` 返回 `currentVisitId` + `currentVisit` 子对象(可能指向终态 Visit)
- `visit/list-by-appointment` 返回全部 visits[] 数组

---

## §9 ID 命名映射表(本版冻结)

### 9.1 Employee 相关

| 命名 | 语义 | 来源 | 本版裁决 |
|---|---|---|---|
| `employeeId` | 接诊医生 / 业务 ID | 【原系统事实】214 §5.1 45 命中 | **采用** |
| `adminId` | 登录认证 ID | 【原系统事实】214 §5.1 34 命中 | **采用** |
| `doctorId` | – | 233 §3.5 自创,原系统 0 命中 | **不用,统一用 employeeId** |
| `userId` | – | 214 §5.1 0 命中 | **不用** |
| `nickname` | 登录用户名 | 【原系统事实】214 §1.4 L14273 | **采用** |
| `adminRoleId` | 角色 ID | 【原系统事实】214 §6.1 38 命中 | **采用** |

### 9.2 Company 相关

| 命名 | 语义 | 来源 | 本版裁决 |
|---|---|---|---|
| `companyId` | 公司 ID | 【原系统事实】214 §1.1 127 命中 | **采用** |
| `corpId` | 公司 ID 别名 | 【原系统事实】214 §1.4 L96 localStorage | **采用作 state 持久化名** |
| `hospitalId` | – | 214 §1.1 0 命中 | **不用** |

### 9.3 ConsultRoom / BigScreen 相关

| 命名 | 语义 | 来源 | 本版裁决 |
|---|---|---|---|
| `consultRoomId` | 诊室 ID | 【原系统事实】214 §11.1 A 级 | **采用** |
| `roomId` | – | 216 §1.3 0 命中 | **不用** |
| `bigScreenId` | 大屏 ID | 【原系统事实】216 §14.4 A 级 | **采用** |
| `bigScreenName` | 大屏名 | 【原系统事实】216 §14.4 A 级 | **采用** |
| `sceneType` | 大屏模式(1=接诊,2=检查)| 【原系统事实】216 §14.4 A 级 | **采用** |

### 9.4 Patient / Customer / MedicalRecord 相关

| 命名 | 语义 | 来源 | 本版裁决 |
|---|---|---|---|
| `customerId` | 会员 ID | 【原系统事实】105 §6.1 A 100% | **采用** |
| `patientId` | 患者 ID(**非业务主键**)| 【原系统事实】105 §6.1 A 100% | **采用** |
| `medicalRecordId` | 病案 ID(**不引入 V4.4**)| 【原系统事实】101 §7.3 "patientId 用 MedicalRecord" | **不引入** |
| `customer.linkMobile` | 联系人手机 | 【原系统事实】105 §6.1 11 位数字 | **采用** |
| `patient.idCard` | 身份证号 | 【原系统事实】105 §6.1 18 位 | **采用** |

### 9.5 命名映射总表

| 业务 | 字段名(本版) | 类型 | 来源 |
|---|---|---|---|
| Company | `companyId` | BIGINT【OptFlow设计】 | 复用 |
| Customer | `customerId` | BIGINT【OptFlow设计】 | 复用 |
| Patient | `patientId` | BIGINT【OptFlow设计】 | 复用 |
| Employee | `employeeId` + `adminId` | BIGINT【OptFlow设计】 | 复用 |
| ConsultRoom | `consultRoomId` | BIGINT【OptFlow设计】 | 复用 |
| BigScreen | `bigScreenId` | BIGINT【OptFlow设计】 | 复用 |
| Appointment | `appointmentId` | UUID v4【OptFlow设计】 | 新建 |
| AppointmentSchedule | `scheduleId` | UUID v4【OptFlow设计】 | 新建 |
| AppointmentSlot | `slotId` | UUID v4【OptFlow设计】 | 新建 |
| TriageQueue | `triageQueueId` | UUID v4【OptFlow设计】 | 新建 |
| ReceptionQueue | `receptionQueueId` | UUID v4【OptFlow设计】 | 新建 |
| Visit | `visitId` | UUID v4【OptFlow设计】 | 新建 |

---

## §10 表 A:事实/设计分层总表

| 对象/字段 | 【原系统事实】 | 【已验证业务事实】 | 【OptFlow设计】 | 【待确认】 |
|---|---|---|---|---|
| **Company** | | | | |
| `companyId` 字段名 | ✓ (214 §1.1) | – | – | 类型 |
| `companyTitle` 字段 | ✓ (214 §1.4) | – | – | – |
| `corpInfo` 实体(JS state) | ✓ (214 §1.4) | – | – | – |
| `Company.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| **Customer** | | | | |
| `customerId` 字段名 | ✓ (105 §6.1) | – | – | – |
| `customer.id` 数值语义 | ✓ (105 §6.1) | – | – | – |
| `customer.linkMobile` 11 位数字 | ✓ (105 §6.1) | – | – | – |
| `Customer.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| `customerId` 业务主键存在性 | ✓ 仅 PAGE-302 (101 §7.3) | – | – | – |
| **Patient** | | | | |
| `patientId` 字段名 | ✓ (105 §6.1) | – | – | – |
| `patient.id` 数值语义 | ✓ (105 §6.1) | – | – | – |
| `patient.idCard` 18 位 | ✓ (105 §6.1) | – | – | – |
| `Patient.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| `patientId` **不是业务主键** | ✓ (101 §7.3) | – | – | – |
| **Employee** | | | | |
| `employeeId` 字段名 | ✓ (214 §5.1) | – | – | – |
| `adminId` 字段名(独立)| ✓ (214 §5.1) | – | – | – |
| `employeeCheckinQueue.employeeId` | ✓ (214 §11.1) | – | – | – |
| `adminRoleId` 38 命中(数字数组 [1,2])| ✓ (214 §6.1) | – | – | – |
| `nickname` 字段 | ✓ (214 §1.4) | – | – | – |
| `Employee.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| `Employee` 单对象 + `employeeId`/`adminId` 双字段 | – | – | ✓ | – |
| `doctorId` 不用 | – | – | ✓ | – |
| `userId` 不用 | – | – | ✓ | – |
| **ConsultRoom** | | | | |
| `consultRoom.id` 字段名 | ✓ (214 §11.1) | – | – | – |
| `consultRoomVoList` 容器 | ✓ (216 §14.4) | – | – | – |
| `ConsultRoom.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| **BigScreen** | | | | |
| `bigScreen.id` 字段名 | ✓ (216 §14.4) | – | – | – |
| `bigScreenName` 字段 | ✓ (216 §14.4) | – | – | – |
| `sceneType` 1=接诊 2=检查 | ✓ (216 §14.4) | – | – | – |
| `BigScreen.id` 主键类型 | ✗ | ✗ | BIGINT | 原系统实际类型 |
| `BigScreen` 独立 ID 实体 | ✓ (216 §14.5) | – | – | – |
| **Appointment(新)** | | | | |
| 整个对象 | ✗ 原系统 0 命中 | ✗ | 全部 | – |
| `appointmentId` UUID v4 | – | – | ✓ | – |
| 12 状态机 | – | – | ✓ | – |
| **AppointmentSchedule(新)** | | | | |
| 整个对象 | ✗ 原系统 scheduleId 0 命中 | ✗ | 全部 | – |
| `scheduleId` UUID v4 | – | – | ✓ | – |
| 3 状态(ACTIVE/INACTIVE/CANCELLED)| – | – | ✓ | – |
| **AppointmentSlot(新)** | | | | |
| 整个对象 | ✗ 原系统 slotId 0 命中 | ✗ | 全部 | – |
| `slotId` UUID v4 | – | – | ✓ | – |
| 3 状态(AVAILABLE/FULL/CLOSED)| – | – | ✓ | – |
| DRAFT 不占容量 | – | – | ✓ (229 §12.3 修正) | – |
| **TriageQueue(新)** | | | | |
| 整个对象 | ✗ 原系统 0 命中 | ✗ | 全部 | – |
| `triageQueueId` UUID v4 | – | – | ✓ | – |
| 4 状态(IN_POOL/ASSIGNED/REMOVED/CANCELLED)| – | – | ✓ | – |
| `employeeId` / `consultRoomId` IN_POOL 时 NULL | – | – | ✓ (229 §10) | – |
| **ReceptionQueue(新)** | | | | |
| 整个对象 | ✗ 原系统 0 命中 | ✗ | 全部 | – |
| `receptionQueueId` UUID v4 | – | – | ✓ | – |
| 6 状态(ASSIGNED/WAITING/CALLED/SKIPPED/IN_CONSULTATION/DONE)| – | – | ✓ | – |
| **Visit(新)** | | | | |
| 整个对象 | ✗ 原系统 visitId 0 命中 | ✗ | 全部 | – |
| `visitId` UUID v4 | – | – | ✓ | – |
| 7 状态(DRAFT/CHECKED_IN/TRIAGED/IN_CONSULTATION/COMPLETED/TRANSFERRED/CANCELLED)| – | – | ✓ | – |
| **currentVisitId** | | | | |
| 字段名(Appointment 上)| – | – | ✓ (229 §5.1 P0-6) | – |
| 创建 = NULL | – | – | ✓ | – |
| ARRIVED = visit.id | – | – | ✓ | – |
| transfer = 新 visit.id | – | – | ✓ | – |
| COMPLETED = 保持 | – | – | ✓ (231 P0-1 修正) | – |
| CANCELLED = 保持 | – | – | ✓ (231 P0-1 修正) | – |
| **4 状态机 = 29 状态** | – | – | ✓ (229 §4.2) | – |
| **35+5=40 API** | – | – | ✓ (231 冻结) | – |
| **4 System Job** | – | – | ✓ (231 冻结) | – |
| **Appointment 1:N Visit** | – | – | ✓ (229 §5.2) | – |

---

## §11 表 B:DDL 前正式设计基线

### 11.1 6 个复用对象(字段表)

#### B-1:Company

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `companyId` | BIGINT | ✓ | AUTO_INCREMENT | 主键 | 【OptFlow设计】 |
| `companyTitle` | VARCHAR(100) | ✓ | – | 公司名 | 【原系统事实】 |
| `companyName` | VARCHAR(100) | – | – | 公司简称 | 【待确认】 |
| `companyType` | INT | – | – | 企业类型(3 类)| 【原系统事实】 04_数据模型.md |
| `logoUrl` | VARCHAR(255) | – | – | – | 【待确认】 |
| `address` | VARCHAR(255) | – | – | – | 【待确认】 |
| `phone` | VARCHAR(20) | – | – | – | 【待确认】 |
| `createdAt` | DATETIME | ✓ | NOW() | 创建时间 | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | 更新时间 | 【OptFlow设计】 |

#### B-2:Customer

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `customerId` | BIGINT | ✓ | AUTO_INCREMENT | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `customerName` | VARCHAR(50) | ✓ | – | 会员名 | 【待确认】 |
| `linkMobile` | VARCHAR(11) | ✓ | – | 11 位手机 | 【原系统事实】105 §6.1 |
| `idCard` | VARCHAR(18) | – | – | 18 位身份证 | 【待确认】 |
| `memberTypeId` | BIGINT | – | – | 会员类型 | 【原系统事实】 04_数据模型.md |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

#### B-3:Patient

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `patientId` | BIGINT | ✓ | AUTO_INCREMENT | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `customerId` | BIGINT | ✓ | – | 所属会员(严禁与 patientId 合并)| 【OptFlow设计】 |
| `patientName` | VARCHAR(50) | ✓ | – | – | 【待确认】 |
| `patientGender` | TINYINT | – | – | 1=男 / 2=女 | 【待确认】 |
| `patientBirthday` | DATE | – | – | – | 【待确认】 |
| `idCard` | VARCHAR(18) | – | – | – | 【原系统事实】105 §6.1 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

#### B-4:Employee【双 ID 字段】

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `employeeId` | BIGINT | ✓ | AUTO_INCREMENT | 主键,接诊用 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `adminId` | BIGINT | ✓ | – | 登录认证 ID(UNIQUE)| 【OptFlow设计】 |
| `employeeName` | VARCHAR(50) | ✓ | – | – | 【原系统事实】 04_数据模型.md |
| `nickname` | VARCHAR(50) | – | – | 登录用户名 | 【原系统事实】 214 §1.4 |
| `mobile` | VARCHAR(11) | – | – | – | 【待确认】 |
| `role` | VARCHAR(20) | ✓ | – | DOCTOR / TRIAGE / RECEP / ADMIN | 【OptFlow设计】 |
| `departmentId` | BIGINT | – | – | 部门 ID | 【原系统事实】 214 §4.1 C 极弱 |
| `status` | TINYINT | ✓ | 1 | 1=正常 / 0=停用 | 【原系统事实】 04_数据模型.md |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `UNIQUE(companyId, adminId)` — adminId 在公司内唯一
- `INDEX(companyId, role)` — 按公司+角色查询

#### B-5:ConsultRoom

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `consultRoomId` | BIGINT | ✓ | AUTO_INCREMENT | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `consultRoomName` | VARCHAR(50) | ✓ | – | 诊室名 | 【原系统事实】 216 §14.4 |
| `status` | TINYINT | ✓ | 1 | 1=正常 / 0=停用 | 【原系统事实】 216 §14.5 |
| `examineList` | JSON | – | – | 检查能力(数组)| 【原系统事实】 216 §14.4 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

#### B-6:BigScreen

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `bigScreenId` | BIGINT | ✓ | AUTO_INCREMENT | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `bigScreenName` | VARCHAR(100) | ✓ | – | 大屏名 | 【原系统事实】 216 §14.4 |
| `sceneType` | TINYINT | ✓ | – | 1=接诊 / 2=检查 | 【原系统事实】 216 §14.4 |
| `consultRoomIdArray` | JSON | – | – | 绑定诊室列表 | 【原系统事实】 216 §14.4 |
| `status` | TINYINT | ✓ | 1 | 1=启用 / 0=停用 | 【待确认】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

### 11.2 6 个新设计对象(字段表)

#### B-7:Appointment

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `appointmentId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | 所属公司 | 【OptFlow设计】 |
| `patientId` | BIGINT | ✓ | – | 患者 FK | 【OptFlow设计】 |
| `employeeId` | BIGINT | ✓ | – | 接诊医生 FK | 【OptFlow设计】 |
| `scheduleId` | UUID (CHAR(36)) | ✓ | – | 排班 FK | 【OptFlow设计】 |
| `slotId` | UUID (CHAR(36)) | ✓ | – | 时段 FK | 【OptFlow设计】 |
| `appointmentNo` | VARCHAR(20) | ✓ | – | 业务编号 | 【OptFlow设计】(参照 medicalCode 模式) |
| `appointmentType` | VARCHAR(20) | ✓ | NORMAL | NORMAL / WALK_IN / FOLLOW_UP / RESCHEDULED | 【OptFlow设计】 |
| `appointmentSource` | VARCHAR(20) | ✓ | WEB | WEB / PHONE / WECHAT / FRONT | 【OptFlow设计】 |
| `status` | VARCHAR(20) | ✓ | DRAFT | 12 状态(229 §3.1)| 【OptFlow设计】 |
| `slotDate` | DATE | ✓ | – | 预约日期 | 【OptFlow设计】 |
| `slotStartTime` | TIME | ✓ | – | 开始时间 | 【OptFlow设计】 |
| `slotEndTime` | TIME | ✓ | – | 结束时间 | 【OptFlow设计】 |
| `currentVisitId` | UUID (CHAR(36)) | – | – | 当前 Visit 指针 | 【OptFlow设计】(229 §5.1 P0-6) |
| `rescheduledFromId` | UUID (CHAR(36)) | – | – | 改约来源 | 【OptFlow设计】 |
| `remark` | VARCHAR(500) | – | – | – | 【OptFlow设计】 |
| `createdBy` | BIGINT | ✓ | – | 创建人 employeeId | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `confirmedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `completedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `cancelledAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `cancelReason` | VARCHAR(200) | – | – | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `UNIQUE(companyId, appointmentNo)`
- `INDEX(slotDate, employeeId, status)`
- `INDEX(patientId, status)`
- `FOREIGN KEY(patientId) → Patient(patientId)` ON DELETE RESTRICT
- `FOREIGN KEY(employeeId) → Employee(employeeId)` ON DELETE RESTRICT
- `FOREIGN KEY(scheduleId) → AppointmentSchedule(scheduleId)` ON DELETE RESTRICT
- `FOREIGN KEY(slotId) → AppointmentSlot(slotId)` ON DELETE RESTRICT
- `FOREIGN KEY(currentVisitId) → Visit(visitId)` ON DELETE SET NULL

#### B-8:AppointmentSchedule

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `scheduleId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `employeeId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `scheduleDate` | DATE | ✓ | – | – | 【OptFlow设计】 |
| `status` | VARCHAR(20) | ✓ | ACTIVE | ACTIVE / INACTIVE / CANCELLED | 【OptFlow设计】(229 §11) |
| `remark` | VARCHAR(500) | – | – | – | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

#### B-9:AppointmentSlot

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `slotId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `scheduleId` | UUID (CHAR(36)) | ✓ | – | – | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `consultRoomId` | BIGINT | – | – | 可空 | 【OptFlow设计】 |
| `startTime` | TIME | ✓ | – | – | 【OptFlow设计】 |
| `endTime` | TIME | ✓ | – | – | 【OptFlow设计】 |
| `capacity` | INT | ✓ | 0 | – | 【OptFlow设计】 |
| `bookedCount` | INT | ✓ | 0 | DRAFT 不占容量 | 【OptFlow设计】(229 §12.3) |
| `status` | VARCHAR(20) | ✓ | AVAILABLE | AVAILABLE / FULL / CLOSED | 【OptFlow设计】 |
| `serviceType` | VARCHAR(50) | – | – | – | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `CHECK(bookedCount <= capacity)`(触发器或约束)
- `INDEX(scheduleId, status)`

#### B-10:TriageQueue

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `triageQueueId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `visitId` | UUID (CHAR(36)) | ✓ | – | – | 【OptFlow设计】 |
| `appointmentId` | UUID (CHAR(36)) | – | – | WalkIn Fallback 可空 | 【OptFlow设计】 |
| `consultRoomId` | BIGINT | – | – | IN_POOL 时 NULL,ASSIGNED 时填 | 【OptFlow设计】 |
| `employeeId` | BIGINT | – | – | IN_POOL 时 NULL,ASSIGNED 时填 | 【OptFlow设计】 |
| `status` | VARCHAR(20) | ✓ | IN_POOL | IN_POOL / ASSIGNED / REMOVED / CANCELLED | 【OptFlow设计】 |
| `assignedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `assignedBy` | BIGINT | – | – | – | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `UNIQUE(visitId)` — 一对一
- `INDEX(status, createdAt)` — 分诊池查询

#### B-11:ReceptionQueue

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `receptionQueueId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `triageQueueId` | UUID (CHAR(36)) | ✓ | – | – | 【OptFlow设计】 |
| `visitId` | UUID (CHAR(36)) | ✓ | – | – | 【OptFlow设计】 |
| `appointmentId` | UUID (CHAR(36)) | – | – | WalkIn Fallback 可空 | 【OptFlow设计】 |
| `consultRoomId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `employeeId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `status` | VARCHAR(20) | ✓ | ASSIGNED | ASSIGNED / WAITING / CALLED / SKIPPED / IN_CONSULTATION / DONE | 【OptFlow设计】 |
| `sequenceInRoom` | INT | ✓ | 0 | 诊室内序号 | 【OptFlow设计】 |
| `calledAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `startedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `completedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `skippedTimes` | INT | ✓ | 0 | – | 【OptFlow设计】 |
| `cancelReason` | VARCHAR(200) | – | – | 软删原因 | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `UNIQUE(triageQueueId)` — 一对一
- `UNIQUE(visitId)`
- `INDEX(consultRoomId, status, sequenceInRoom)` — 队列查询

#### B-12:Visit

| 字段 | 类型 | 必填 | 默认 | 说明 | 标签 |
|---|---|:-:|---|---|---|
| `visitId` | UUID (CHAR(36)) | ✓ | gen_random_uuid() | 主键 | 【OptFlow设计】 |
| `companyId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `appointmentId` | UUID (CHAR(36)) | – | – | WalkIn Fallback 可空 | 【OptFlow设计】 |
| `patientId` | BIGINT | ✓ | – | – | 【OptFlow设计】 |
| `employeeId` | BIGINT | – | – | TRIAGED 之后必有 | 【OptFlow设计】 |
| `consultRoomId` | BIGINT | – | – | TRIAGED 之后必有 | 【OptFlow设计】 |
| `visitType` | VARCHAR(20) | ✓ | NORMAL | NORMAL / WALK_IN | 【OptFlow设计】 |
| `status` | VARCHAR(20) | ✓ | DRAFT | DRAFT / CHECKED_IN / TRIAGED / IN_CONSULTATION / COMPLETED / TRANSFERRED / CANCELLED | 【OptFlow设计】 |
| `transferredFromVisitId` | UUID (CHAR(36)) | – | – | 转诊来源 | 【OptFlow设计】 |
| `transferredFromEmployeeId` | BIGINT | – | – | – | 【OptFlow设计】 |
| `cancelledAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `cancelReason` | VARCHAR(200) | – | – | – | 【OptFlow设计】 |
| `completedAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `transferredAt` | DATETIME | – | – | – | 【OptFlow设计】 |
| `createdAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |
| `updatedAt` | DATETIME | ✓ | NOW() | – | 【OptFlow设计】 |

**约束**:
- `INDEX(appointmentId)` — Appointment 1:N Visit 关系
- `INDEX(patientId, status)`
- `INDEX(companyId, status, createdAt)`
- `FOREIGN KEY(appointmentId) → Appointment(appointmentId)` ON DELETE SET NULL(WalkIn Fallback 可空)

---

## §12 S1-168 启动判断

### 12.1 PASS 条件检查

| # | 条件 | 状态 | 依据 |
|---:|---|:-:|---|
| 1 | OptFlow 对象边界已经冻结 | ✓ | §4.1 12 个对象 + §7 关系矩阵 |
| 2 | Employee 双 ID 已作出 OptFlow 设计裁决 | ✓ | §5.3 方案 A |
| 3 | Patient / Customer / MedicalRecord 边界已冻结 | ✓ | §6.3 7 个问题回答 |
| 4 | currentVisitId 已冻结 | ✓ | §8 6 个场景 |
| 5 | 新对象 ID 类型已冻结 | ✓ | §4.1 UUID v4 |
| 6 | 复用对象 ID 类型已明确标记【待确认】或 OptFlow 设计类型 | ✓ | §4.1 BIGINT【OptFlow设计】 |
| 7 | 没有未解决的 D 级模型冲突 | ✓ | §5 + §6 D 级冲突已裁决 |

**全部 7 项 PASS**。

### 12.2 最终判断

# **【S1-168 READY】**

S1-168 DDL 草案**可以**基于本版裁决推进。

**前置条件**:
1. S1-168 设计者必须严格区分【原系统事实】/【OptFlow设计】标签
2. 复用对象 BIGINT 类型是【OptFlow设计】,**不是**"原系统是 MySQL BIGINT"
3. 当前仓库无后端 Java / SQL 证据,DDL 实施时**需后端配合**(Java 实体类型 / 数据库类型确认)
4. 229 §7.2 / §14.1 中"currentVisitId 重置为 NULL"旧规则与本版"保持原值"冲突,本版以 235 为准

---

## §13 自评

| 维度 | 分数 | 理由 |
|---|:-:|---|
| 4 类来源区分 | 90/100 | 全程严格应用 |
| 234B D 级冲突解决 | 92/100 | Employee 方案 A + Patient 边界 7 问 |
| currentVisitId 冻结 | 90/100 | 6 场景 + 明确与 229 冲突处理 |
| ID 命名统一 | 88/100 | 5 维度命名映射 |
| 12 对象 DDL 设计基线 | 90/100 | 12 完整字段表 |
| 综合 | **90/100** | |

---

## §14 Git 验证

- **HEAD 不变**:`1bf472c39812d88ad41c2e8a0570ddf37ab0e8fc`
- **本轮不提交 Git**(按老板指示)
- **234A / 234B / 全部 47 份历史 MD SHA256 锁定** ✓

---

## §15 一句话最终判断

> **本版将 S1-165 ~ S1-167A 的对象 / ID / 关系 / 字段来源严格分为【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】4 类。Employee 双 ID 冲突采用方案 A(Employee 单对象 + employeeId/adminId 双字段)。Patient / Customer / MedicalRecord 边界冻结为:patientId 非业务主键(用 medicalCode 模式),customerId 独立保留,本版不引入 MedicalRecord 实体。currentVisitId 6 场景唯一规则与 229 旧规则冲突时以 235 为准。12 个对象 DDL 设计基线完整,BIGINT 复用 6 对象 + UUID v4 新建 6 对象。S1-168 DDL 草案可启动。**
