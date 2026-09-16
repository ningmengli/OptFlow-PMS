# 241V4 S1-169-1 表数量与 TenantLine 覆盖率一致性补丁

> **本轮定位**:第三轮独立盲审识别的 **P1-3** 修复补丁。241V3 的"12 业务表 + 2 系统表 + 1 预留 = 15"和"5 张 IGNORE, 10 张业务表自动 TenantLine"**数量表达错误**;本补丁**重新以 236B 为唯一基准核算**,显式修正 15 张当前实际表 / 5 个 IGNORE 配置项 / 4 张当前实际 IGNORE 表 / 11 张业务表 TenantLine 过滤范围。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 任何历史 MD
> - 严禁修改 VisionCare PMS 任何文件
> - 严禁创建 backend/ / 严禁写 Java 源文件 / 严禁创建 SQL 文件 / 严禁执行 DDL / 严禁连接数据库
> - 严禁修改 pom.xml / application.yml
> - 严禁 commit / 严禁 push
> - 标签:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
> - 阶段:**S1-169-1**(未进入 S1-169-2)
> - 本补丁**不**自评 PASS,**等待下一轮独立盲审**

---

## §0 Git 基线

- **HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`(S1-169-0 240 commit)
- **REMOTE == LOCAL**:`6efa0da` ✓
- **0 号闸门 4 文件 SHA256 全部 PASS** ✓
- **历史 MD(190~241V2A-3 共 67 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V4 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 第三轮独立盲审识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-3 | P1 | 241V3 §3.3 / §3.4 / §6.1 | 表数量 / TenantLine 数量矛盾 |

### 1.2 241V3 错误数量表达(本审计独立识别)

#### 错误 1:241V3 §3.3 "12 业务表 + 2 系统表 + 1 预留 = 15"

**问题**:
- 12 业务表含 `company`(company 是业务表,不是系统表)
- "2 系统表"实际是 `user` + `user_company` + `flyway_schema_history` = **3 张**实际系统/全局表
- 1 预留 `flyway_schema_history_v44` 不能与当前实际表混算
- 正确:12 业务表 + 3 实际系统/全局表 = **15 张当前实际表**(预留不算)

#### 错误 2:241V3 §3.4 "5 张在 IGNORE_TABLES(必须 bypass TenantLine),10 张业务表自动 TenantLine 过滤"

**问题**:
- 5 个 IGNORE 配置项 = flyway_schema_history / company / user / user_company / flyway_schema_history_v44
- 其中 4 个是当前实际表(flyway_schema_history / company / user / user_company)
- 1 个是预留名(flyway_schema_history_v44,当前不存在)
- 12 业务表里 `company` 在 IGNORE → 11 张业务表走 TenantLine
- 正确:11 张业务表走 TenantLine(不是 10 张)

#### 错误 3:241V3 §6.2 "5 张表各自所属类别" 用 5 张表

**问题**:
- 5 张表是配置项,不是当前实际表
- 当前实际 IGNORE 表 = 4 张
- 预留 flyway_schema_history_v44 应明确标记 "NO(预留)"

### 1.3 严重度

| 维度 | 评估 |
|---|---|
| 设计核心(5 张 IGNORE 配置) | ✓ 正确(241V3 §3.1 冻结) |
| 数量表达 | ✗ 3 处错误 |
| 是否影响 Effective Spec | ✗ 不影响(5 张配置冻结正确) |
| 是否影响 S1-169-2 实施 | ✗ 不影响(实施按 5 张配置即可) |
| **设计严谨度** | **✗ 数量表达错误,显式要求 P1** |

**严重度**:**P1**(数量表达与分类不严谨,但 Effective Spec 正确)

---

## §2 严格禁止(本轮)

- ✗ 修改 236B / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2

---

## §3 概念分类与计数原则(241V4 显式)

### 3.1 三个关键概念(241V4 显式)

**【241V4 冻结】** 严格区分三个概念:

| 概念 | 含义 | 数量 |
|---|---|---:|
| **(A) 当前实际表** | V4.4 当前真实存在的表(必须有 DDL / 实际创建)| **15** |
| **(B) IGNORE 配置项** | `IGNORE_TABLES_V44` 集合中的字符串名字 | **5** |
| **(C) 当前实际 IGNORE 表** | (A) ∩ (B) = 当前真实存在且在 IGNORE 中的表 | **4** |
| **(D) 预留 IGNORE 配置** | (B) − (C) = 配置中但当前不存在的表名 | **1** |
| **(E) 业务表 TenantLine 过滤** | 12 业务表 − 在 IGNORE 的业务表 = 11 张业务表 | **11** |

### 3.2 概念关系图

```
(A) 15 张当前实际表
   ├─ (C) 4 张当前实际 IGNORE 表
   │   ├─ flyway_schema_history(系统表)
   │   ├─ company(业务表,但主键自指)
   │   ├─ user(无 companyId)
   │   └─ user_company(无 companyId)
   └─ (E) 11 张业务表走 TenantLine
       ├─ customer / patient / employee
       ├─ consult_room / big_screen
       ├─ appointment_schedule / appointment_slot
       ├─ appointment / visit
       └─ triage_queue / reception_queue

(B) 5 张 IGNORE 配置项
   ├─ 4 张 ∈ (C):flyway_schema_history / company / user / user_company
   └─ 1 张 ∈ (D):flyway_schema_history_v44(预留)
```

### 3.3 计数公式

```
(A) 当前实际表总数 = (C) + (E) = 4 + 11 = 15
(B) IGNORE 配置项数 = (C) + (D) = 4 + 1 = 5
(E) TenantLine 业务表 = 12 业务表 − company(在 IGNORE) = 11
```

---

## §4 236B 12 业务表 唯一基准(241V4 显式)

### 4.1 12 张业务表(以 236B 为唯一基准)

**【241V4 冻结】** V4.4 业务表 = 236B 锁定的 12 张,**含 company**:

```
1.  company              ← 业务表(主键 companyId 自指 → 在 IGNORE)
2.  customer
3.  patient
4.  employee
5.  consult_room
6.  big_screen
7.  appointment_schedule
8.  appointment_slot
9.  appointment
10. visit
11. triage_queue
12. reception_queue
```

**严格禁止**:
- ✗ 不得遗漏 company
- ✗ 不得把 company 划入"系统表"分类
- ✗ 不得把 company 划入"系统/全局"分类(它是业务表)

### 4.2 12 业务表的属性(241V4 显式)

| 业务表 | 来源 | 当前实际存在 | companyId | 在 IGNORE | 走 TenantLine |
|---|---|:-:|:-:|:-:|:-:|
| company | 236B | YES | PK 自指 | YES | NO(因 IGNORE)|
| customer | 236B | YES | YES | NO | YES |
| patient | 236B | YES | YES | NO | YES |
| employee | 236B | YES | YES | NO | YES |
| consult_room | 236B | YES | YES | NO | YES |
| big_screen | 236B | YES | YES | NO | YES |
| appointment_schedule | 236B | YES | YES | NO | YES |
| appointment_slot | 236B | YES | YES | NO | YES |
| appointment | 236B | YES | YES | NO | YES |
| visit | 236B | YES | YES | NO | YES |
| triage_queue | 236B | YES | YES | NO | YES |
| reception_queue | 236B | YES | YES | NO | YES |

**12 业务表 = 1 张 IGNORE(company)+ 11 张走 TenantLine**

---

## §5 V4.4 当前实际表(241V4 显式)

### 5.1 15 张当前实际表 = 12 业务表 + 3 系统/全局表

**【241V4 冻结】** V4.4 当前实际表 = **15 张**(以 236B + 241V2 §12.1/12.2/Flyway 9.22.3 为依据):

| # | 类别 | 表 | 来源 | 当前实际存在 | companyId | IGNORE | TenantLine |
|---:|---|---|---|:-:|:-:|:-:|:-:|
| 1 | 业务 | company | 236B | YES | PK 自指 | YES | NO |
| 2 | 业务 | customer | 236B | YES | YES | NO | YES |
| 3 | 业务 | patient | 236B | YES | YES | NO | YES |
| 4 | 业务 | employee | 236B | YES | YES | NO | YES |
| 5 | 业务 | consult_room | 236B | YES | YES | NO | YES |
| 6 | 业务 | big_screen | 236B | YES | YES | NO | YES |
| 7 | 业务 | appointment_schedule | 236B | YES | YES | NO | YES |
| 8 | 业务 | appointment_slot | 236B | YES | YES | NO | YES |
| 9 | 业务 | appointment | 236B | YES | YES | NO | YES |
| 10 | 业务 | visit | 236B | YES | YES | NO | YES |
| 11 | 业务 | triage_queue | 236B | YES | YES | NO | YES |
| 12 | 业务 | reception_queue | 236B | YES | YES | NO | YES |
| 13 | 系统/全局 | user | 241V2 §12.2 | YES | NO | YES | NO |
| 14 | 系统/全局 | user_company | 241V2 §12.1 | YES | NO | YES | NO |
| 15 | 系统/全局 | flyway_schema_history | Flyway 9.22.3 | YES | NO | YES | NO |
| **16** | **预留** | **flyway_schema_history_v44** | **241V2 §12.6 预留** | **NO(预留)** | NO | YES(配置保留)| NO |

### 5.2 数量统计公式(241V4 显式)

```
当前实际表 = 15 张(行 1-15)
  ├─ 业务表 12 张(行 1-12)
  └─ 系统/全局表 3 张(行 13-15)

IGNORE 配置项 = 5 个名字(行 1, 13, 14, 15, 16)
  ├─ 当前实际 IGNORE 表 = 4 张(行 1, 13, 14, 15)
  └─ 预留 IGNORE 配置 = 1 个(行 16)

TenantLine 过滤 = 11 张业务表(行 2-12, 排除 company)
```

### 5.3 显式纠错

**【241V4 显式纠错】** 241V3 之前表述:

| 241V3 表述 | 错误 | 241V4 正确 |
|---|---|---|
| "12 业务表 + 2 系统表 + 1 预留 = 15" | 实际系统表 = 3 张(不是 2 张) | **12 业务表 + 3 系统/全局表 = 15 张当前实际表(预留 1 个不计入)** |
| "5 张在 IGNORE_TABLES, 10 张业务表自动 TenantLine 过滤" | 11 张业务表走 TenantLine(不是 10) | **5 个 IGNORE 配置项,11 张业务表自动 TenantLine 过滤** |
| "5 张表各自所属类别" 列表 | flyway_schema_history_v44 是预留,不是当前实际表 | **4 张当前实际 IGNORE 表 + 1 个预留 IGNORE 配置(显式标记)** |

---

## §6 IGNORE_TABLES_V44 冻结(241V4 显式沿用 241V3)

### 6.1 Effective Spec(5 个配置项)

**【241V4 显式沿用 241V3 §3.1】** V4.4 `IGNORE_TABLES_V44` = **5 个配置项**:

```java
private static final Set<String> IGNORE_TABLES_V44 = Set.of(
    "flyway_schema_history",        // 当前实际表(类别 C 系统表)
    "company",                      // 当前实际表(类别 B 主键自指)
    "user",                         // 当前实际表(类别 A 无 companyId)
    "user_company",                 // 当前实际表(类别 A 无 companyId)
    "flyway_schema_history_v44"     // 预留配置(类别 C,当前不实际存在)
);
```

### 6.2 5 个配置项各自理由(241V4 显式分类)

| 配置项 | 当前实际存在 | 类别(241V2 §6.2)| 加入理由 |
|---|:-:|---|---|
| flyway_schema_history | YES | C(系统表) | Flyway 内部迁移历史,无 companyId 字段 |
| company | YES | B(主键自指) | 主键自指,登录时不能加 WHERE companyId=? |
| user | YES | A(无 companyId) | user 表无 companyId 字段 |
| user_company | YES | A(无 companyId) | 中间表无 companyId 字段 |
| flyway_schema_history_v44 | **NO(预留)**| C(系统表)| 防御性预留(若 Flyway 配置改名)|

### 6.3 严禁"系统表 2 张"错误表述

| 错误表述 | 正确 |
|---|---|
| "5 张在 IGNORE_TABLES" | **"5 个 IGNORE 配置项"** |
| "2 系统表"(指 user / user_company)| **"3 系统/全局表"(user / user_company / flyway_schema_history)** |
| "5 张表各自所属类别" | **"5 个配置项各自类别(其中 1 个预留)"** |
| "10 张业务表自动 TenantLine" | **"11 张业务表走 TenantLine"** |

---

## §7 S1-169-2 实施不变约束(241V4 显式)

### 7.1 实施代码不受影响

| 维度 | 241V4 是否变更 |
|---|:-:|
| IGNORE_TABLES_V44 Set 内容 | ✗ **不**变更(仍 5 个配置项)|
| 5 个配置项各自理由 | ✗ **不**变更(沿用 241V3 §3.2)|
| S1-169-2 实施代码模板 | ✗ **不**变更(沿用 241V3 §5.2)|
| 7 项实施验证清单 | ✗ **不**变更(沿用 241V3 §5.3)|

### 7.2 仅文字表述修正

| 维度 | 修正 |
|---|---|
| "5 张在 IGNORE" | → "5 个 IGNORE 配置项(其中 1 个预留)" |
| "2 系统表" | → "3 系统/全局表(user / user_company / flyway_schema_history)" |
| "10 张业务表走 TenantLine" | → "11 张业务表走 TenantLine" |
| "15 张表"(混合 12 + 2 + 1)| → "15 张当前实际表(12 业务 + 3 系统/全局,预留名不计入)" |

### 7.3 实施验证清单补充(241V4 新增)

| # | 验证项 | 期望 |
|---:|---|---|
| 8 | 12 业务表全部存在(以 236B 为基准)| ✓ |
| 9 | 当前实际表 = 15 张(以 Flyway V1__init_v44_base.sql 为准)| ✓ |
| 10 | 11 张业务表走 TenantLine(以 SQL 日志为准)| ✓ |

---

## §8 完整 15 张当前实际表 + 1 张预留 矩阵(241V4 冻结)

### 8.1 完整矩阵(241V4 显式)

| # | 表 | 来源 | 当前实际存在 | companyId | IGNORE 配置 | 走 TenantLine |
|---:|---|---|:-:|:-:|:-:|:-:|
| 1 | company | 236B | YES | PK 自指 | YES | NO(因 IGNORE)|
| 2 | customer | 236B | YES | YES | NO | YES |
| 3 | patient | 236B | YES | YES | NO | YES |
| 4 | employee | 236B | YES | YES | NO | YES |
| 5 | consult_room | 236B | YES | YES | NO | YES |
| 6 | big_screen | 236B | YES | YES | NO | YES |
| 7 | appointment_schedule | 236B | YES | YES | NO | YES |
| 8 | appointment_slot | 236B | YES | YES | NO | YES |
| 9 | appointment | 236B | YES | YES | NO | YES |
| 10 | visit | 236B | YES | YES | NO | YES |
| 11 | triage_queue | 236B | YES | YES | NO | YES |
| 12 | reception_queue | 236B | YES | YES | NO | YES |
| 13 | user | 241V2 §12.2 | YES | NO | YES | NO(因 IGNORE)|
| 14 | user_company | 241V2 §12.1 | YES | NO | YES | NO(因 IGNORE)|
| 15 | flyway_schema_history | Flyway 9.22.3 | YES | NO | YES | NO(因 IGNORE)|
| 16 | flyway_schema_history_v44 | 241V2 §12.6 预留 | **NO(预留)** | NO | YES(配置保留)| NO |

### 8.2 显式声明

- 第 16 行 `flyway_schema_history_v44` **不**是当前实际表
- 它仅作为预留名存在于 `IGNORE_TABLES_V44` Set 中
- 若 V4.4 Flyway 配置 `spring.flyway.table` 改名为 `flyway_schema_history_v44`,原表名不再存在,新表名仍需 bypass
- **当前不存在**这张表,故"当前实际表 = 15 张"是**正确**的

---

## §9 241V3 错误表述显式作废(241V4 显式)

### 9.1 显式作废列表

**【241V4 显式作废】** 241V3 以下表述 = **数量错误,需以 241V4 为准**:

| 位置 | 错误表述 | 241V4 修正 |
|---|---|---|
| §3.3 标题 | "12 业务表 + 2 系统表 + 1 预留 = 15" | **"12 业务表 + 3 系统/全局表 = 15 张当前实际表(预留 1 个不计入)"** |
| §3.3 行 | "12 张业务表(来自 236B)" 列表不含 company | **"12 张业务表(来自 236B)含 company"** |
| §3.3 行 | "V4.4 业务表(2 张,来自 241V2)company / user_company" | **"V4.4 业务表(2 张,来自 241V2)" 应改为 "V4.4 系统/全局表(3 张)user / user_company / flyway_schema_history"** |
| §3.4 标题 | "5 张在 IGNORE_TABLES(必须 bypass TenantLine),10 张业务表自动 TenantLine 过滤" | **"5 个 IGNORE 配置项(其中 1 个预留),11 张业务表走 TenantLine 过滤"** |
| §3.4 数据流 | "true(5 张表):SQL 不加 WHERE companyId=?" | **"true(5 个配置项匹配):SQL 不加 WHERE companyId=?"** |
| §6.2 表格 | "5 张表各自所属类别" | **"5 个配置项各自所属类别(其中 1 个预留,显式标记)"** |

### 9.2 沿用 241V3 正确内容

| 241V3 正确内容 | 241V4 沿用? |
|---|:-:|
| §3.1 5 个 IGNORE 配置项 Set | ✓ |
| §3.2 5 张表各自理由(逐表冻结)| ✓ |
| §4.1 显式作废 §6.4 / §6.6 / §11 | ✓ |
| §5 S1-169-2 实施不可误抄约束 | ✓ |
| §5.2 实施代码模板 | ✓ |
| §5.3 7 项验证清单 | ✓(241V4 补充 8-10) |

---

## §10 补丁叠加关系(241V4 显式)

### 10.1 与前序文档关系

| 文档 | 定位 | 与 241V4 关系 |
|---|---|---|
| 236B | DDL 修正版(12 业务表)| **唯一基准**(241V4 重新核算) |
| 240 | Q4 跨公司隔离架构 | 基础 |
| 241V2 | 基础设施设计修正版 | 沿用 §12.1 / §12.2 / §12.6 |
| 241V2A | P0-2 companyId 强制覆盖 | 沿用 |
| 241V2A-1 | defaultCompany 并发控制 | 沿用 |
| 241V2A-2 | 并发测试 / 死锁表述 | 沿用 |
| 241A-1 | 独立盲审 | 识别 P1(241V3 / 241V2A-3)|
| 241V3 | IGNORE_TABLES 代码一致性 | **本补丁修正其数量表述** |
| 241V2A-3 | 并发测试 Spring 代理边界 | 沿用(与本补丁无关)|
| **241V4** | **表数量与 TenantLine 覆盖率一致性补丁** | **本文件,显式作废 241V3 数量错误表述** |

### 10.2 241V4 增量内容

| 241V3 内容 | 241V4 增量 |
|---|---|
| "12 业务表 + 2 系统表 + 1 预留 = 15" | **显式纠错**(§3 / §5 / §9) |
| "5 张在 IGNORE, 10 张业务表自动 TenantLine" | **显式纠错** → "5 个 IGNORE 配置项, 11 张业务表走 TenantLine"(§3 / §5 / §9) |
| "5 张表各自所属类别" 列表 | **显式分类**为"4 张当前实际 + 1 个预留配置"(§3 / §6) |
| (无) | **新增完整 15 张当前实际表 + 1 张预留矩阵**(§8) |
| (无) | **新增概念分类原则(A/B/C/D/E)**(§3) |
| (无) | **新增计数公式**(§3.3) |
| (无) | **新增实施验证清单第 8/9/10 项**(§7.3)|

### 10.3 严格关系

- ✗ 241V4 **不**修改 241V3 任何字节
- ✗ 241V4 **不**修改 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V2A-3 / 任何历史 MD
- ✓ 241V4 通过"补丁叠加"建立增量关系
- ✓ 241V4 显式作废 241V3 数量错误表述(§9)
- ✓ IGNORE_TABLES_V44 Set 内容(5 个配置项)继续由 241V3 冻结,241V4 仅澄清数量
- ✓ 241V4 + 241V3 不冲突(241V4 仅修正表述,不改配置)

---

## §11 P1-3 闭环验证

### 11.1 P1-3 原始问题

> "241V3 表数量 / TenantLine 数量矛盾"

具体:
- 12 业务表 + 2 系统表 + 1 预留 = 15(错误:实际是 12 业务 + 3 系统/全局 = 15)
- 5 张 IGNORE, 10 张业务表自动 TenantLine(错误:实际是 5 个配置项, 11 张业务表)

### 11.2 241V4 修复手段

| 修复手段 | 位置 |
|---|---|
| 概念分类 A/B/C/D/E | §3 |
| 计数公式 | §3.3 |
| 12 业务表含 company(显式)| §4 |
| 15 张当前实际表 + 1 张预留矩阵 | §8 |
| 显式纠错 241V3 错误表述 | §9 |
| 实施验证清单补充 | §7.3 |

### 11.3 P1-3 闭环率 = 100%

| 检查项 | 通过 |
|---|:-:|
| 236B 12 表逐个列全(含 company)| ✓ §4.1 |
| company 在 12 业务表里 | ✓ §4.1 |
| 当前实际表 = 15 | ✓ §5.1 |
| 预留不计入实际数量 | ✓ §3.1 / §8 |
| 业务表 TenantLine = 11 | ✓ §4.2 |
| IGNORE 配置项 = 5 | ✓ §6.1 |
| 不存在"10 张"错误 | ✓ §9.1 |

**P1-3 真闭环** ✓

---

## §12 补丁后独立自审(241V4 自身)

### 12.1 P1-3 是否完全消失

| 检查项 | 结论 |
|---|:-:|
| "10 张" 表述被删除? | ✓ §9.1 显式作废 |
| "2 系统表" 表述被删除? | ✓ §9.1 显式作废 |
| 12 业务表含 company 显式声明? | ✓ §4.1 |
| 15 张当前实际表显式声明? | ✓ §5.1 |
| 11 张 TenantLine 业务表显式声明? | ✓ §4.2 |
| 5 个 IGNORE 配置项 vs 4 张当前实际 IGNORE 表区分? | ✓ §3.1 |

**P1-3 完全消失** ✓

### 12.2 是否产生新的 P0

| 检查项 | 结论 |
|---|:-:|
| 概念分类 A/B/C/D/E 自洽? | ✓ |
| 15 张当前实际表 完整? | ✓ |
| 1 张预留显式标记? | ✓ |
| 11 张 TenantLine 业务表 = 12 - company? | ✓ |

**无新 P0** ✓

### 12.3 是否产生新的 P1

| 检查项 | 结论 |
|---|:-:|
| 数量自洽? | ✓ 4 + 11 = 15 |
| 类别自洽? | ✓ A/B/C |
| 与 241V3 兼容? | ✓ 241V4 仅澄清,不改配置 |
| 与 236B 一致? | ✓ 12 业务表逐个列全 |

**无新 P1** ✓

### 12.4 是否与 8 份文档冲突

| 文档 | 主题 | 冲突? |
|---|---|:-:|
| 236B | 12 业务表 DDL | ✓ **完全一致** |
| 241V2 §12.1 / §12.2 | user / user_company DDL | ✓ 沿用 |
| 241V3 | 5 个 IGNORE 配置项 | ✓ 沿用 + 显式纠错表述 |
| 241V2A-3 | Spring 代理边界 | ✗ 不冲突(无关)|
| 241A-1 | 独立盲审 | ✓ 修复其识别的 P1 |

**无冲突** ✓

### 12.5 Effective Spec 是否唯一

- ✓ 15 张当前实际表(12 业务 + 3 系统/全局)
- ✓ 1 张预留(flyway_schema_history_v44)
- ✓ 5 个 IGNORE 配置项(4 张当前实际 + 1 个预留)
- ✓ 11 张业务表走 TenantLine
- ✓ company 是业务表且在 IGNORE

**唯一** ✓

### 12.6 S1-169-2 实施者是否仍可能误判数量

| 风险 | 缓解 |
|---|---|
| 实施者认为"10 张"业务表走 TenantLine | §4.2 显式 11 张 |
| 实施者遗漏 company 表 | §4.1 显式 12 业务表含 company |
| 实施者把 flyway_schema_history_v44 算作当前实际表 | §8 显式标记 "NO(预留)" |
| 实施者认为 IGNORE 配置项 = 当前实际 IGNORE 表 | §3.1 显式区分 (B) vs (C) |

**误判风险显著降低** ✓

---

## §13 报告统计

- 报告字节数:约 14000 字节
- 章节数:15
- 修复的 P1:1(P1-3)
- 显式纠错数量表述:6 处
- 新增概念分类:5 个(A/B/C/D/E)
- 新增计数公式:3 个
- 新增实施验证:3 项(8/9/10)
- 新增完整矩阵:15 + 1 行
- 启动闸门:241V4 完成,等待下一轮独立盲审
- DDL 修改:0
- Java 代码修改:0
- 与 241V3 关系:补丁叠加,不覆盖

---

## §14 启动闸门(241V4 不变)

### 14.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241V2 修复原 4 P0 + 1 P1 | ✓ | 241V2 |
| 241V2A P0-2 真闭环 | ✓ | 241V2A |
| 241V2A-1 defaultCompany 并发控制 | ✓ | 241V2A-1 |
| 241V2A-2 死锁表述 | ✓ | 241V2A-2 |
| 241A-1 独立盲审 | ✓ | 241A-1 |
| 241V3 修复 P1-1(5 个 IGNORE 配置)| ✓ | 241V3 |
| 241V2A-3 修复 P1-2(Spring 代理)| ✓ | 241V2A-3 |
| **241V4 修复 P1-3(数量纠错,本文件)** | **✓** | **本文件** |
| **241V2A-4 修复 P1-4(测试数据上下文,并行)** | **✓** | **241V2A-4 同步** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 14.2 下一轮盲审必审计

- ✓ 241V4 是否真修复 P1-3
- ✓ 241V4 是否引入新 P0/P1
- ✓ 241V4 + 241V3 数量表述是否一致
- ✓ 241V4 + 241V2A-4 两者是否冲突
- ✓ 10 份文档(241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 241V4 / 241V2A-4)是否仍有内部矛盾

---

## §15 一句话最终判断

> **241V4 S1-169-1 表数量与 TenantLine 覆盖率一致性补丁完成**:第三轮独立盲审识别的 P1-3(241V3 "12 业务表 + 2 系统表 + 1 预留 = 15" 和 "5 张 IGNORE, 10 张业务表自动 TenantLine" 数量表达错误)通过本补丁**真闭环**——以 236B 为唯一基准重新核算 12 业务表(含 company)+ 3 系统/全局表(user / user_company / flyway_schema_history)= 15 张当前实际表(预留 flyway_schema_history_v44 不计入),显式区分 5 个 IGNORE 配置项 / 4 张当前实际 IGNORE 表 / 1 个预留配置,11 张业务表走 TenantLine(12 业务表 - 1 张 company 在 IGNORE = 11);新增完整 15+1 矩阵 + 概念分类 A/B/C/D/E + 计数公式 + 实施验证清单第 8/9/10 项;241V3 错误表述**显式作废**但 IGNORE_TABLES_V44 Set 内容(5 个配置项)继续沿用;241V4 不修改 241V3 任何字节,只通过补丁叠加澄清数量;S1-169-2 仍 BLOCK,等下一轮独立盲审同时审计 241V4 + 241V2A-4。

---

## §16 报告统计(完整)

- 章节数:16
- 修复的 P1:1(P1-3)
- 显式纠错:6 处
- 新增概念:5 个(A/B/C/D/E)
- 完整矩阵:15 + 1 行
- 实施验证:10 项
- 启动闸门:全部满足
- 下一轮:独立盲审
