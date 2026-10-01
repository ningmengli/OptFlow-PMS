# G2-Contract-Audit-01R2｜修复动作与 P1 口径最终校准

> **本轮定位**:G2-Contract-Audit-01R 的**最终口径冻结**。
> **不是**重新审计全部内容。
> **不是**开发。
> **不是**生成 G2-Contract-02。
> **本轮唯一输出**:本元审计文档(R2)。
> **本轮唯一目标**:解决 R1 内部最后一个硬矛盾 — P1 Issue 数 ≠ P1 Fix Action 数 ≠ §10 修复动作数(20)。
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`(G2-Contract-Audit-01R 已落地后 HEAD)
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史 MD(190~241V2A-42 + S1-170 全系列 + G2-Contract-01 + G2-Contract-Audit-01 + G2-Contract-Audit-01R)未修改** ✓
> **本轮不写代码 / 不 commit / 不 push** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-01R2_修复动作与P1口径最终校准.md` |
| 任务性质 | R1 元审计的最终校准 |
| 校准对象 | G2-Contract-Audit-01R(本文不对其做修改)|
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 严禁 | 修改 G2-Contract-01 / G2-Contract-Audit-01 / G2-Contract-Audit-01R / 修改任何历史 MD / 创建 backend / 写 Java 源文件 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / 生成 G2-Contract-02 / commit / push |

---

## §1 R1 内部硬矛盾识别

### 1.1 R1 §7.1 / §7.2 / §7.3 中 P1 数量

| 节 | 描述 | 数量 |
|---|---|:-:|
| §7.2 独立 P1 总数 | P1-1 ~ P1-10 | **10 项** |
| §7.3 真实 Gap 总数 | Gap-02 / Gap-03 / Gap-06 / Gap-07 | **4 项** |
| §8.1 修复优先级表 | 列出 P1 修复分组 | **6 项**(Service / Transaction / Security / IGNORE_TABLES 预留 / Phase 1 系统设置 / Transfer 回滚)|

### 1.2 R1 §8.2 修复基线表

§8.2 修复基线表实际列出 **7 个 P1 修复分组**:
- Gap-02 / P1-1~3(Service 方法)
- P1-4(Transaction 分类)
- P1-5 / Gap-03(权限矩阵 + Sa-Token)
- P1-6(IGNORE_TABLES 预留)
- Gap-06 / P1-7(Phase 1 系统设置)
- Gap-07 / P1-8(SystemSetting V4.4)
- P1-9(Transfer 回滚)

但 P1-10 在 §8.2 中没有作为独立修复动作列出 — **因为 P1-10 = Sa-Token 注解已归入 "P1-5 / Gap-03(权限矩阵 + Sa-Token)"**。

### 1.3 R1 §10 最终汇报

> **总 Fix Actions = 20 项**(14 P0 + 6 P1)

**矛盾**:
- R1 §7.2 写 P1 Issue = 10 项
- R1 §8.2 实际列出 7 个 P1 修复分组
- R1 §10 写 6 P1 Fix Actions
- **三处不一致(10 / 7 / 6)**

### 1.4 R2 校准任务

| 校准项 | 目标 |
|---|---|
| 1 | 冻结 **P1 Issue(问题编号)** vs **P1 Fix Action(修复动作编号)** 的两层模型 |
| 2 | 冻结 **P1 Issue = 10** vs **PA(修复动作)= 7** 的官方映射 |
| 3 | 冻结 **G2-Contract-02 修复动作总量 = 14 P0 + 7 P1 = 21** |
| 4 | 明确 G2-Contract-02 验收条件不用 Coverage 百分比,改用 P0=0 / P1=0 |

---

## §2 A. P1-1 ~ P1-10 完整表(P1 Issue 层)

### 2.1 冻结定义

**P1 Issue** = "Effective Spec 没冲突,但 Contract 不足以直接指导编码"的问题编号。
**冻结编号**:**P1-1 ~ P1-10**(共 **10 项**,沿用 R1 §7.2)。

### 2.2 P1-1 ~ P1-10 完整表

| P1 编号 | 描述 | 来源 | 证据 |
|:-:|---|---|---|
| **P1-1** | CustomerService / PatientService / ConsultRoomService / BigScreenService 方法 Contract 缺 | Gap-02(部分)| R1 §7.1 P0-C51 / C52 / C54 / C55 标 ⚠️ |
| **P1-2** | EmployeeService.adminId 校验逻辑部分冻结 | Gap-02(部分)| R1 §7.1 P0-C53;235B §2 显式冻结 adminId 但方法未冻结 |
| **P1-3** | CompanyService CRUD 方法 Contract 部分冻结 | Gap-02(部分)| R1 §7.1 P0-C56;240 / 241V2 部分冻结 |
| **P1-4** | API-016 arrival/checkin / API-021 triage/assign Transaction 边界分类未冻结 | R1 §3.5 P1 + R1 §7.2 P0-C57 / C58 | 233 §API-016 / 021 未明确 transaction 分类 |
| **P1-5** | 7 角色完整列表 + 40 API × 7 角色权限矩阵 Contract 缺 | R1 §7.3 P0-C70(部分)+ Gap-02(部分)| 235B §2 + 233 各 API permission 部分冻结 |
| **P1-6** | IGNORE_TABLES flyway_schema_history_v44 预留表激活条件未冻结 | R1 §6.1 P0-C37(预留说明部分)| 241V4 §6.1 部分冻结 |
| **P1-7** | Phase 1 系统设置 26 项页面字段未冻结 | Gap-06 | S1-170A / B / C / D / E 多次识别 |
| **P1-8** | SystemSetting V4.4 范围未冻结 | Gap-07 | S1-170A / B / C / D / E 多次识别 |
| **P1-9** | Transfer 部分失败回滚策略未冻结 | R1 §4.4 + R1 §7.2 | 235B §4.2 未冻结回滚策略 |
| **P1-10** | Sa-Token @SaCheckRole / @SaCheckPermission 注解 Contract 缺 | Gap-03 | 235B / 233 未冻结具体注解 |

### 2.3 P1 总量冻结

> **P1 Issue 总数 = 10 项**(P1-1 ~ P1-10)

---

## §3 B. PA-01 ~ PA-07 完整表(P1 Fix Action 层)

### 3.1 冻结定义

**PA = P1 Fix Action** = G2-Contract-02 中实际需要执行的具体修复动作(问题级别 vs 修复级别的区分)。
**冻结编号**:**PA-01 ~ PA-07**(共 **7 项**)。

### 3.2 PA-01 ~ PA-07 完整表

| PA 编号 | 名称 | 涉及 Contract 章节 | 涉及 Effective Spec | 修复动作 |
|:-:|---|---|---|---|
| **PA-01** | **Service Contract 补齐** | G2-Contract-01 §8 | 232 / 233 / 235B / 240 / 241V2 | 冻结 6 Service 方法 Contract(CustomerService / PatientService / EmployeeService / ConsultRoomService / BigScreenService / CompanyService) |
| **PA-02** | **Transaction Contract 补齐** | G2-Contract-01 §9 | 233 §API-016 / 021 | API-016 / API-021 Transaction 边界分类 冻结为 T1 / T3(具体分类由 G2-Contract-02 决定,需 Effective Spec 显式冻结)|
| **PA-03** | **Security Contract 补齐** | G2-Contract-01 §11 | 235B §2 + 233 | 冻结 7 角色完整列表 + 40 API × 7 角色权限矩阵 + Sa-Token @SaCheckRole / @SaCheckPermission 注解映射表 |
| **PA-04** | **IGNORE_TABLES Reserved 补齐** | G2-Contract-01 §14.4 | 241V4 §6.1 | 冻结 flyway_schema_history_v44 预留表激活条件(何时启用 / 启用前是否 IGNORE)|
| **PA-05** | **Phase 1 System Settings 范围冻结** | G2-Contract-02 新增 | (待 Phase 1 页面侦察完成)| 冻结 Phase 1 系统设置 26 项页面字段 |
| **PA-06** | **SystemSetting V4.4 范围冻结** | G2-Contract-02 新增 | (待 V4.4 重新冻结)| 冻结 SystemSetting V4.4 范围与字段 |
| **PA-07** | **Transfer Rollback Contract 冻结** | G2-Contract-01 §9.2 | 235B §4.2 | 冻结 Transfer 9 步事务的部分失败回滚策略(全回滚 vs 部分补偿)|

### 3.3 PA 总量冻结

> **P1 Fix Action 总数 = 7 项**(PA-01 ~ PA-07)

---

## §4 C. P1 Issue → Fix Action 映射

### 4.1 映射原则

> 一个 P1 Issue 可能被多个 PA 覆盖,一个 PA 可能覆盖多个 P1 Issue。
> 映射按"该 Issue 是否被该 PA 实质解决"判定。

### 4.2 完整映射表

| P1 Issue | 描述 | 映射到 PA | 说明 |
|:-:|---|:-:|---|
| **P1-1** | CustomerService / PatientService / ConsultRoomService / BigScreenService 方法 Contract 缺 | **PA-01** | PA-01 覆盖 6 Service,C/P/CR/B 均在内 |
| **P1-2** | EmployeeService.adminId 校验逻辑部分冻结 | **PA-01** | PA-01 覆盖 6 Service,Employee 在内 |
| **P1-3** | CompanyService CRUD 方法 Contract 部分冻结 | **PA-01** | PA-01 覆盖 6 Service,Company 在内 |
| **P1-4** | API-016 / API-021 Transaction 边界分类未冻结 | **PA-02** | PA-02 专项 |
| **P1-5** | 7 角色完整列表 + 40 API × 7 角色权限矩阵 Contract 缺 | **PA-03** | PA-03 第一部分(角色 + 矩阵)|
| **P1-6** | IGNORE_TABLES flyway_schema_history_v44 预留表激活条件未冻结 | **PA-04** | PA-04 专项 |
| **P1-7** | Phase 1 系统设置 26 项页面字段未冻结 | **PA-05** | PA-05 专项 |
| **P1-8** | SystemSetting V4.4 范围未冻结 | **PA-06** | PA-06 专项 |
| **P1-9** | Transfer 部分失败回滚策略未冻结 | **PA-07** | PA-07 专项 |
| **P1-10** | Sa-Token @SaCheckRole / @SaCheckPermission 注解 Contract 缺 | **PA-03** | PA-03 第二部分(Sa-Token 注解)|

### 4.3 映射统计

| PA | 覆盖 P1 Issue | 数量 |
|:-:|---|:-:|
| **PA-01** | P1-1 / P1-2 / P1-3 | 3 |
| **PA-02** | P1-4 | 1 |
| **PA-03** | P1-5 / P1-10 | 2 |
| **PA-04** | P1-6 | 1 |
| **PA-05** | P1-7 | 1 |
| **PA-06** | P1-8 | 1 |
| **PA-07** | P1-9 | 1 |
| **合计** | P1-1 ~ P1-10 全部覆盖 | **10 → 7** |

### 4.4 映射验证

> **数学验证**:10 项 P1 Issue 通过 7 项 PA 修复动作覆盖,平均 1.43 个 P1 / PA。
> - PA-01: 3 个 P1
> - PA-02 ~ PA-07: 各 1 个 P1(PA-03 = 2 个)
> - 全部 P1 Issue 都至少被 1 个 PA 覆盖
> - 无 P1 Issue 遗漏

> **✅ 映射 = COMPLETE**(无遗漏,无重复覆盖同一 Issue)

---

## §5 D. 最终 P0 / P1 / Fix Action 数量

### 5.1 独立 Root Cause(P0)数量

**沿用 R1 §4.3 冻结**:**6 个 Root Cause Family,14 项独立 P0**

| Root-Cause-ID | 描述 | 数量 |
|---|---|:-:|
| RC-1 | API 路径错位(14 API Path)| 1 |
| RC-2 | Transfer 9-step 错位 | 1 |
| RC-3a~i | 12 Object 字段级 9 项错位 | 9 |
| RC-4 | IGNORE_TABLES 不完整(2 vs 5)| 1 |
| RC-5 | company 业务表概念错 | 1 |
| RC-6 | 公开 API 白名单缺 bigscreen/display | 1 |
| **独立 P0 Root Cause 总数** | | **14 项** |

### 5.2 P0 Fix Action 数量

| Root-Cause-ID | P0 Fix Action(实际修复动作)| 数量 |
|---|---|:-:|
| RC-1 | 重写 G2 §7.2(API-025~040 路径) | 1 |
| RC-2 | 重写 G2 §9.2(Transfer 9-step)| 1 |
| RC-3a | 重写 G2 §4.2.3(Patient 字段)| 1 |
| RC-3b | 重写 G2 §4.2.4(Employee 字段)| 1 |
| RC-3c | 重写 G2 §4.2.5(ConsultRoom 字段)| 1 |
| RC-3d | 重写 G2 §4.2.6(BigScreen 字段)| 1 |
| RC-3e | 重写 G2 §4.3.1(AppointmentSchedule 字段)| 1 |
| RC-3f | 重写 G2 §4.3.2(AppointmentSlot 字段)| 1 |
| RC-3g | 重写 G2 §4.3.3(Appointment 字段)| 1 |
| RC-3h | 重写 G2 §4.3.4(Visit 字段)| 1 |
| RC-3i | 重写 G2 §4.3.6(ReceptionQueue 字段)| 1 |
| RC-4 | 重写 G2 §14.4(IGNORE_TABLES 5 个配置项)| 1 |
| RC-5 | 改 G2 §14.2(company 业务表概念)| 1 |
| RC-6 | 改 G2 §11.2(公开 API 白名单)| 1 |
| **P0 Fix Action 总数** | | **14 项** |

### 5.3 P1 Issue / Fix Action 数量

| 层级 | 编号 | 数量 |
|---|---|:-:|
| P1 Issue | P1-1 ~ P1-10 | **10 项** |
| P1 Fix Action | PA-01 ~ PA-07 | **7 项** |

### 5.4 G2-Contract-02 修复动作总量

> **P0 Fix Actions = 14**
> **P1 Fix Actions = 7**
> **总 Fix Actions = 21 项**

| 维度 | 数值 |
|---|---:|
| P0 Fix Actions | 14 |
| P1 Fix Actions | 7 |
| **总 Fix Actions** | **21** |

### 5.5 与 R1 §10 修正

| R1 §10 原值 | R2 校准值 | 差异 |
|---|---:|---|
| 20 项 = 14 P0 + 6 P1 | **21 项 = 14 P0 + 7 P1** | 🔴 R1 §10 写 "6 P1" 错,应为 7 PA |

> **🔴 R1 §10 数学错误**:"总 20 项 = 14 P0 + 6 P1" → 应为 **21 项 = 14 P0 + 7 P1**。

---

## §6 Coverage 数字处理

### 6.1 R1 Coverage 数字

| 维度 | R1 数值 |
|---|---:|
| 完整且正确覆盖率 | 53.4%(62/116)|
| 冲突率 | 33.6%(39/116)|
| 分母 | 116 |

### 6.2 R2 重新定性

> **🔴 R2 校准**:53.4% / 33.6% / 116 **不是永久 Gate 规范**,仅是 **"G2-Contract-Audit-01 当前统计口径"**。
> 不能将其升级为 G2-Contract-02 验收条件。

### 6.3 G2-Contract-02 正式验收条件

G2-Contract-02 通过条件 **优先采用以下 5 条**(任一不满足即 FAIL):

| # | 验收条件 | 类型 |
|:-:|---|:-:|
| 1 | **P0 = 0**(全部 14 项 P0 Fix Action 完成且通过验证)| **硬性** |
| 2 | **P1 = 0**,或 P1 中残留项被**明确标记为不阻塞项**(需有效证据支持)| **硬性** |
| 3 | **Effective Spec 直接冲突 = 0**(不允许 Contract 与 233 / 235B / 236B / 238 / 241V4 等有任何直接冲突)| **硬性** |
| 4 | **未冻结内容不得伪装成冻结事实**(所有【待确认】必须显式标注,不得编造)| **硬性** |
| 5 | **不得自行发明字段 / API / 状态 / 权限 / Transaction 规则**(严格沿用 Effective Spec,无证据不写)| **硬性** |

### 6.4 Coverage 数字退居辅助参考

> G2-Contract-Audit-02 完成后,Coverage 数字可作为辅助参考(展示进步趋势),但不作为主要验收条件。
> 主要验收条件 = 上述 5 条硬性条件。

---

## §7 E. G2-Contract-02 唯一修复基线

### 7.1 修复基线总表

| 序号 | Root-Cause / PA | Fix Action | Contract 章节 | Effective Spec | 硬性 / 软性 |
|:-:|---|---|---|---|:-:|
| 1 | RC-1 | 重写 G2 §7.2(API-025~040 路径)| G2 §7.2 | 233 §API-025~040 | **🔴 硬性** |
| 2 | RC-2 | 重写 G2 §9.2(Transfer 9-step)| G2 §9.2 | 235B §4.2 / §4.3 | **🔴 硬性** |
| 3 | RC-3a | 重写 G2 §4.2.3(Patient 字段)| G2 §4.2.3 | 238 §4.3 + 236B §3 | **🔴 硬性** |
| 4 | RC-3b | 重写 G2 §4.2.4(Employee 字段)| G2 §4.2.4 | 238 §4.4 + 235B §2 | **🔴 硬性** |
| 5 | RC-3c | 重写 G2 §4.2.5(ConsultRoom 字段)| G2 §4.2.5 | 238 §4.5 | **🔴 硬性** |
| 6 | RC-3d | 重写 G2 §4.2.6(BigScreen 字段)| G2 §4.2.6 | 238 §4.6 + §15 | **🔴 硬性** |
| 7 | RC-3e | 重写 G2 §4.3.1(AppointmentSchedule 字段)| G2 §4.3.1 | 238 §4.8 | **🔴 硬性** |
| 8 | RC-3f | 重写 G2 §4.3.2(AppointmentSlot 字段)| G2 §4.3.2 | 238 §4.9 + 236B §3.5 | **🔴 硬性** |
| 9 | RC-3g | 重写 G2 §4.3.3(Appointment 字段)| G2 §4.3.3 | 238 §4.7 | **🔴 硬性** |
| 10 | RC-3h | 重写 G2 §4.3.4(Visit 字段)| G2 §4.3.4 | 238 §4.10 | **🔴 硬性** |
| 11 | RC-3i | 重写 G2 §4.3.6(ReceptionQueue 字段)| G2 §4.3.6 | 238 §4.12 | **🔴 硬性** |
| 12 | RC-4 | 重写 G2 §14.4(IGNORE_TABLES 5 个配置项)| G2 §14.4 | 241V4 §6.1 | **🔴 硬性** |
| 13 | RC-5 | 改 G2 §14.2(company 业务表概念)| G2 §14.2 | 235B §1 + 238 §4.1 | **🔴 硬性** |
| 14 | RC-6 | 改 G2 §11.2(公开 API 白名单)| G2 §11.2 | 241V2 §5.6 + 233 §API-040 | **🔴 硬性** |
| 15 | PA-01 | 补齐 6 Service 方法 Contract(Customer / Patient / Employee / ConsultRoom / BigScreen / Company)| G2 §8 | 232 / 233 / 235B / 240 / 241V2 | **🟡 硬性** |
| 16 | PA-02 | 冻结 API-016 / API-021 Transaction 边界分类 | G2 §9 | 233 §API-016 / 021 | **🟡 硬性** |
| 17 | PA-03 | 冻结 7 角色完整列表 + 权限矩阵 + Sa-Token 注解映射 | G2 §11 | 235B §2 + 233 | **🟡 硬性** |
| 18 | PA-04 | 冻结 flyway_schema_history_v44 预留表激活条件 | G2 §14.4 | 241V4 §6.1 | **🟡 硬性** |
| 19 | PA-05 | 冻结 Phase 1 系统设置 26 项页面字段 | G2 §Phase 1 范围 | (待 Phase 1 页面侦察完成)| **🟡 硬性** |
| 20 | PA-06 | 冻结 SystemSetting V4.4 范围与字段 | G2 §SystemSetting | (待 V4.4 重新冻结)| **🟡 硬性** |
| 21 | PA-07 | 冻结 Transfer 9 步事务回滚策略 | G2 §9.2 | 235B §4.2 | **🟡 硬性** |

### 7.2 修复优先级

| 优先级 | 修复项 | 阻塞 G2 READY |
|:-:|---|:-:|
| **P0-最高** | RC-1 / RC-2(API Path + Transfer 9-step)| **🔴 必须先修复**(整个 40 API 与 Transfer 业务的核心)|
| **P0-高** | RC-3a~i(9 Object 字段级)| **🔴 必须先修复**(12 业务表完整性)|
| **P0-中** | RC-4 / RC-5 / RC-6(Tenant + 概念)| **🔴 必须先修复** |
| **P1** | PA-01 ~ PA-07 | **🟡 必须先修复** |

### 7.3 G2-Contract-02 必须遵守的纪律

| # | 纪律 |
|:-:|---|
| 1 | **不修改 G2-Contract-01**(G2-Contract-02 是新文件,不是 G2-Contract-01 的修订版)|
| 2 | **不修改任何历史 MD** |
| 3 | **不写 Java / 不创建 backend / 不写 pom.xml / 不写 application.yml** |
| 4 | **不执行 DDL / 不连接数据库 / 不运行测试** |
| 5 | **不创建 V2A-43 / V2A-44 / S1-171** |
| 6 | **不 commit / 不 push** |
| 7 | **不得自行发明字段 / API / 状态 / 权限 / Transaction 规则**(严格沿用 Effective Spec)|
| 8 | **所有【待确认】必须显式标注**(不得编造冻结事实)|

### 7.4 G2-Contract-02 完成后必须做的事

| 步骤 | 任务 | 输出 |
|:-:|---|---|
| 1 | G2-Contract-02 完成 21 项 Fix Action | `G2-Contract-02_OptFlow-PMS_Production-Implementation-Contract.md` |
| 2 | G2-Contract-Audit-02 独立盲审 | `G2-Contract-Audit-02_...md` |
| 3 | 验收 5 条硬性条件(§6.3)| 5 条全部通过 → G2 READY |
| 4 | G3 BACKEND IMPLEMENTATION ENTRY GATE 单独判定 | S1-170E §G3 标准 |

---

## §8 F. 最终判定

### 8.1 G2-Contract-01 状态

> **G2-Contract-01 = BLOCK**(保持)
>
> 理由:
> - 14 项独立 P0 未修复
> - 10 项 P1 Issue 未修复
> - 7 项 PA 未执行
> - Contract Coverage = FAIL(53.4% 完整率 / 33.6% 冲突率)

### 8.2 Backend Entry 状态

> **Backend Entry = BLOCK**(保持)
>
> 理由:沿用 S1-170E §12:"不允许开始 backend,除非 G2 Contract Gate = READY"
> 当前 G2 = NOT READY → Backend Entry = BLOCK

### 8.3 下一阶段

> **下一步 = G2-Contract-02**(允许创建)
>
> 前提:
> 1. 不修改 G2-Contract-01
> 2. 不修改任何历史 MD
> 3. 按 §7.1 修复基线表逐项执行 21 项 Fix Action
> 4. 完成后必须 G2-Contract-Audit-02 独立盲审
> 5. 通过 5 条硬性验收条件才能 G2 → READY

---

## §9 元约束

> 本 R2 元审计(Audit-01R2)的局限:

1. **本轮不重新审计 G2-Contract-01 全部内容**,只解决 R1 内部 P1 口径数学不一致
2. **P1 Issue 编号(P1-1 ~ P1-10)沿用 R1 §7.2 冻结**,不再重新编号
3. **P0 Root Cause Family(RC-1 ~ RC-6)与 P0 Fix Action(14 项)沿用 R1 §4.3 / §8.2 冻结**
4. **PA-01 ~ PA-07 是本轮新增冻结**,但其覆盖的 P1 Issue 都已在 R1 中识别

---

## §10 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-01R2_修复动作与P1口径最终校准.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-01 / G2-Contract-Audit-01 / G2-Contract-Audit-01R / 不修改任何历史 MD |
| 严禁 | 修改任何已有审计文件 / 修改任何历史 MD / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / 生成 G2-Contract-02 / commit / push |

---

**End of G2-Contract-Audit-01R2**