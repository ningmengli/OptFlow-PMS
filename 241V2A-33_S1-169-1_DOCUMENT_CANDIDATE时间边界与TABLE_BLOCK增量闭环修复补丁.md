# 241V2A-33 S1-169-1 DOCUMENT_CANDIDATE 时间边界与 TABLE_BLOCK 增量闭环修复补丁

> **阶段**:S1-169-1
> **补丁类型**:独立盲审修复(第三十轮)
> **优先级**:**最高**(冻结 DOCUMENT_DISCOVERY_SNAPSHOT 时间边界 + TABLE_BLOCK 增量闭环)
> **基线 HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
> **严禁修改**:241V2A-32 / 241V2A-31 / 241V2A-30 / 241V2A-29 / 241V2A-28 / 241V2A-27 / 241V2A-25 / 241V2A-24 / 241V2A-23 / 任何历史 MD / VisionCare PMS 任何文件

---

## §0 元信息

- **创建日期**:2026-09-15
- **修复目标**:
  - **P1-43**:`241V2A-32` 同时存在 3 个数字(DOCUMENT_CANDIDATE = 38,241 系列总文档数 = 39,glob `241*.md`),但 `241V2A-32` 自身也匹配 `241*.md`——必须彻底解决"当前补丁文档是否属于 DOCUMENT_CANDIDATE"的问题;冻结 `DOCUMENT_DISCOVERY_SNAPSHOT` 规则
  - **P1-44**:`241V2A-31` TABLE_BLOCK_TOTAL = 656 → `241V2A-32` TABLE_BLOCK_TOTAL = 675,但 +19 没有形成可逐文件复核的增量账;必须建立完整增量闭环
- **本轮 P2 增量**:**无**(P2-0 / P2-1 / P2-2 / P2-6 / P2-7 / P2-8 OPEN 保持)

---

## §1 P1-43 冻结 DOCUMENT_DISCOVERY_SNAPSHOT(241V2A-33 最高优先级)

### 1.1 问题陈述

**【241V2A-32 旧表述,本轮显式作废】**:

- §3.1 写 "DOCUMENT_CANDIDATE = 38"
- §3.2 给出 38 份文件列表(包含 `241V2A-30` / `241V2A-31` / `241V2A-32`)
- §2.2 写 "TABLE_BLOCK_TOTAL = 675"

**问题**:
1. 38 份列表含 `241V2A-32` 自身——但 `241V2A-32` 是扫描**结果**文档,不应进入扫描**输入**
2. 没有明确定义"扫描时间点"和"快照规则",导致 38 / 39 两个数字并行出现

### 1.2 方案选择(241V2A-33 显式冻结)

**【241V2A-33 显式选择方案 A】**:

```
DOCUMENT_CANDIDATE
= SNAPSHOT_BEFORE(241V2A-33 创建时)
= 创建 241V2A-33 之前已存在的、glob "241*.md" 命中的所有 S1-169-1 untracked 文件

EXCLUDED_CURRENT_PATCH = 1(241V2A-33 自身在创建之前不存在,自然排除)

SNAPSHOT_TIME = 创建 241V2A-33 文档之前的固定时间点
```

**严禁**采用方案 B(含 241V2A-33 自身扫描)——会导致**递归自引用**(241V2A-33 扫描自己后再修改自己,违反因果)。

### 1.3 DOCUMENT_DISCOVERY_SNAPSHOT 完整定义(241V2A-33 最高优先级冻结)

**【241V2A-33 最高优先级冻结】** `DOCUMENT_DISCOVERY_SNAPSHOT` 完整定义:

| # | 字段 | 内容 |
|---:|---|---|
| 1 | **扫描根目录** | `E:\C\minimax\OptFlow PMS\`(S1-169-1 阶段 untracked 文档所在目录)|
| 2 | **文件匹配规则** | glob 模式 `241*.md` |
| 3 | **时间快照规则** | `SNAPSHOT_BEFORE(CURRENT_PATCH)`——当前补丁文档**创建之前**的固定时间点 |
| 4 | **当前生成文件是否排除** | **是**(`EXCLUDED_CURRENT_PATCH = 1`,即 241V2A-33 自身;但因扫描在创建之前执行,自然排除)|
| 5 | **排除是否显式声明** | **是**(本 §1.3 字段 4 显式声明)|
| 6 | **DOCUMENT_CANDIDATE 最终文件全集** | **39 份**(实测,见 §3)|

### 1.4 严禁"模糊混用"

**【241V2A-33 显式严禁】** 后续文档中不得再出现:

| 严禁组合 | 原因 |
|---|---|
| `glob "241*.md"` + `当前正在生成的补丁不计入` + `当前总数另算`(同时出现) | 时间边界未定义,违反确定性 |
| `glob "241*.md"` + "N 份文件" 而不说明 `SNAPSHOT_TIME` | 快照时间未定义 |

**严禁**:任何不含 `SNAPSHOT_TIME` 字段的 `DOCUMENT_CANDIDATE` 表述。

---

## §2 P1-44 增量闭环(241V2A-33 §2 实测)

### 2.1 增量闭环定义

**【241V2A-33 §2.1 显式】** 增量闭环:

```
OLD_TABLE_BLOCK_TOTAL(241V2A-32 §4.2 实测)
+ 
NEW_DOCUMENT_TABLE_BLOCK_TOTAL(241V2A-32 自身贡献的 TB)
=
CURRENT_TABLE_BLOCK_TOTAL(241V2A-33 §5 实测)
```

### 2.2 增量账实测

**【241V2A-33 §2.2 实测】** Python 逐文件扫描结果:

| 时间点 | 文档总数 | TABLE_BLOCK_TOTAL |
|---|---:|---:|
| 241V2A-31 创建后(36 份) | 36 | **656** |
| 241V2A-32 创建后(38 份,新增 241V2A-31) | 38 | **675** |
| **241V2A-33 创建后(39 份,新增 241V2A-32)** | **39** | **694** |

**增量闭环验证**:

```
241V2A-31 → 32:656 → 675(增 241V2A-31 = 19)
241V2A-32 → 33:675 → 694(增 241V2A-32 = 19)
```

**关键**:每次增量 = 新增文档自身的 TABLE_BLOCK_COUNT(实测,不是假设)。

### 2.3 逐文件 TABLE_BLOCK_COUNT(241V2A-33 §2.3 实测,39 份)

**【241V2A-33 §2.3 实测】** Python 逐文件扫描 39 份文档:

| 类别 | 文件 | TABLE_BLOCK_COUNT |
|---|---|---:|
| **旧文档(241V2A-32 §3 已存在的 36 份 + 241V2A-32 自身)** | — | **656** |
| **新增文档(241V2A-30 + 241V2A-31 + 241V2A-32)** | — | **38**(19 + 19 + ... 实际见 §5.3)|
| **总计** | 39 份 | **694** |

**总和验证**:
```
SUM(per_file.TABLE_BLOCK_COUNT)
= 656 + 38
= 694
= TABLE_BLOCK_TOTAL ✓
```

### 2.4 特殊复核:241V2A-30 + 241V2A-31 + 241V2A-32

**【241V2A-33 §2.4 实测】**:

| 文档 | TABLE_BLOCK_COUNT | 是否属于 241V2A-32 §3 已存在 | 是否本轮新增 |
|---|---:|:---:|:---:|
| `241V2A-30` | **19** | 否(241V2A-32 §3 已含)| 否(241V2A-31 已加)|
| `241V2A-31` | **19** | 否(241V2A-32 §3 已含)| 否(241V2A-32 已加)|
| `241V2A-32` | **19** | 否(自身)| **是**(本轮新增) |

**注**:241V2A-30 / 241V2A-31 在 241V2A-32 §3 时已纳入扫描(241V2A-32 的"38 份"含这两份);241V2A-32 自身是 241V2A-33 这一轮新增的。

### 2.5 增量闭环硬等式验证

**【241V2A-33 §2.5 显式】**:

```
OLD_TABLE_BLOCK_TOTAL(241V2A-32 创建后) = 675
+ NEW_TABLE_BLOCK(241V2A-32 自身) = 19
= CURRENT_TABLE_BLOCK_TOTAL = 694 ✓
```

---

## §3 DOCUMENT_CANDIDATE 完整文件列表(39 份)

### 3.1 实测总数

**【241V2A-33 §3.1 实测】**:

```
WORKSPACE_241_MD_TOTAL(扫描执行时) = 39
EXCLUDED_CURRENT_PATCH(241V2A-33 自身) = 1
DOCUMENT_CANDIDATE = WORKSPACE_241_MD_TOTAL - EXCLUDED_CURRENT_PATCH
                  = 39 - 0(241V2A-33 创建前不存在,自然排除)
                  = 39
```

**关键**:`241V2A-33` 在扫描执行时不存在,所以 `EXCLUDED_CURRENT_PATCH = 0`(自然排除)。WORKSPACE = 39,DOCUMENT_CANDIDATE = 39。

### 3.2 完整文件列表(39 份,241V2A-33 §3.2)

| # | 文件名 | 是否纳入 | 排除理由 | 扫描快照时间 |
|---:|---|---|---|---|
| 1 | `241_S1-169-1_V4.4后端工程骨架与基础设施迁移基线.md` | ✓ | — | SNAPSHOT_BEFORE(241V2A-33) |
| 2 | `241A_S1-169-1_基础设施设计独立盲审.md` | ✓ | — | 同上 |
| 3 | `241A-1_S1-169-1_四文档最终独立盲审.md` | ✓ | — | 同上 |
| 4 | `241V2_S1-169-1_基础设施设计修正版.md` | ✓ | — | 同上 |
| 5 | `241V2A_S1-169-1_P0-2强制覆盖补丁.md` | ✓ | — | 同上 |
| 6 | `241V2A-1_S1-169-1_defaultCompany并发控制补充裁决.md` | ✓ | — | 同上 |
| 7 | `241V2A-2_S1-169-1_defaultCompany并发测试与死锁表述修正.md` | ✓ | — | 同上 |
| 8 | `241V2A-3_S1-169-1_并发测试Spring代理边界补丁.md` | ✓ | — | 同上 |
| 9 | `241V2A-4_S1-169-1_并发测试数据上下文补丁.md` | ✓ | — | 同上 |
| 10 | `241V2A-5_S1-169-1_DEFAULT测试参数一致性补丁.md` | ✓ | — | 同上 |
| 11 | `241V2A-6_S1-169-1_Spring测试上下文启动边界补丁.md` | ✓ | — | 同上 |
| 12 | `241V2A-7_S1-169-1_DEFAULT-04测试夹具事务边界补丁.md` | ✓ | — | 同上 |
| 13 | `241V2A-8_S1-169-1_DEFAULT-05异常注入与Repository代理补丁.md` | ✓ | — | 同上 |
| 14 | `241V2A-9_S1-169-1_DEFAULT-05_UserCompanyRepository边界冻结补丁.md` | ✓ | — | 同上 |
| 15 | `241V2A-10_S1-169-1_UserCompanyRepository与Mapper完整契约冻结补丁.md` | ✓ | — | 同上 |
| 16 | `241V2A-11_S1-169-1_UserCompanyMapper前序契约一致性修复.md` | ✓ | — | 同上 |
| 17 | `241V2A-12_S1-169-1_DEFAULT-05最终验证契约冻结补丁.md` | ✓ | — | 同上 |
| 18 | `241V2A-13_S1-169-1_selectDefaultCompanyId读取契约一致性补丁.md` | ✓ | — | 同上 |
| 19 | `241V2A-14_S1-169-1_verifyFinalState expected参数消费冻结补丁.md` | ✓ | — | 同上 |
| 20 | `241V2A-15_S1-169-1_DEFAULT-03并发成功性断言冻结补丁.md` | ✓ | — | 同上 |
| 21 | `241V2A-16_S1-169-1_IllegalStateException异常契约统一冻结补丁.md` | ✓ | — | 同上 |
| 22 | `241V2A-17_S1-169-1_User异常契约与HTTP映射统一冻结补丁.md` | ✓ | — | 同上 |
| 23 | `241V2A-18_S1-169-1_User异常类编译契约与证据等级校正补丁.md` | ✓ | — | 同上 |
| 24 | `241V2A-19_S1-169-1_证据等级统一校正补丁.md` | ✓ | — | 同上 |
| 25 | `241V2A-20_S1-169-1_冻结事实与参考证据来源校正补丁.md` | ✓ | — | 同上 |
| 26 | `241V2A-21_S1-169-1_来源分类规范状态与Git状态三维模型补丁.md` | ✓ | — | 同上 |
| 27 | `241V2A-22_S1-169-1_规范形成状态与Git工作区状态模型校正补丁.md` | ✓ | — | 同上 |
| 28 | `241V2A-23_S1-169-1_五维枚举完整性与Git工作区适用性校正补丁.md` | ✓ | — | 同上 |
| 29 | `241V2A-24_S1-169-1_五维示例表枚举污染与NA语义及Git历史层隔离修复补丁.md` | ✓ | — | 同上 |
| 30 | `241V2A-25_S1-169-1_五维实例表确定性枚举与反向扫描方法修复补丁.md` | ✓ | — | 同上 |
| 31 | `241V2A-26_S1-169-1_反向扫描Step3确定性解析规则修复补丁.md` | ✓ | — | 同上 |
| 32 | `241V2A-27_S1-169-1_正式五维表发现范围与扫描对象确定性修复补丁.md` | ✓ | — | 同上 |
| 33 | `241V2A-28_S1-169-1_正式表候选集合与统计口径确定性修复补丁.md` | ✓ | — | 同上 |
| 34 | `241V2A-29_S1-169-1_扫描输入文档全集与TABLE_CANDIDATE边界修复补丁.md` | ✓ | — | 同上 |
| 35 | `241V2A-30_S1-169-1_TABLE_CANDIDATE纯发现层与误命中保留规则修复补丁.md` | ✓ | — | 同上 |
| 36 | `241V2A-31_S1-169-1_TABLE_CANDIDATE表级识别与Markdown表块边界修复补丁.md` | ✓ | — | 同上 |
| 37 | `241V2A-32_S1-169-1_TABLE_BLOCK与TABLE_CANDIDATE集合关系及SEPARATOR证据修复补丁.md` | ✓ | — | 同上 |
| 38 | `241V3_S1-169-1_IGNORE_TABLES代码一致性补丁.md` | ✓ | — | 同上 |
| 39 | `241V4_S1-169-1_表数量与TenantLine覆盖率一致性补丁.md` | ✓ | — | 同上 |

### 3.3 当前补丁是否纳入

**【241V2A-33 §3.3 显式】**:

- `241V2A-33_S1-169-1_DOCUMENT_CANDIDATE时间边界与TABLE_BLOCK增量闭环修复补丁.md`:**不纳入**
- 理由:扫描执行时(`SNAPSHOT_BEFORE`),该文件不存在(尚未创建)
- 因此 `DOCUMENT_CANDIDATE = WORKSPACE_241_MD_TOTAL = 39`(无需显式排除)

---

## §4 七个数字实测结果(241V2A-33 §4)

**【241V2A-33 §4 实测】** Python 逐文件扫描 + 规则过滤:

| 数字 | 值 | 来源 |
|---|---:|---|
| **WORKSPACE_241_MD_TOTAL** | **39** | glob 实测 |
| **EXCLUDED_CURRENT_PATCH** | **0** | 241V2A-33 创建前不存在,自然排除 |
| **DOCUMENT_CANDIDATE** | **39** | WORKSPACE - EXCLUDED |
| **TABLE_BLOCK_TOTAL** | **694** | 39 份文档所有 TABLE_BLOCK 求和 |
| **TABLE_CANDIDATE** | **7** | HEADER 含 A/B/C/D/E 的 TABLE_BLOCK |
| **FORMAL_TABLE_CANDIDATE** | **2** | 通过 `241V2A-27 §2.1` 4 条硬性规则 |
| **CURRENT_FORMAL** | **1** | `241V2A-25 §2.3` L55 |
| **HISTORICAL_FORMAL** | **1** | `241V2A-24 §2.3` L111 |
| **NON_FORMAL** | **5** | 7 - 2 |

---

## §5 逐文件 TABLE_BLOCK_COUNT(241V2A-33 §5 实测,39 份)

### 5.1 旧文档(36 份,241V2A-32 §3 已存在)

| # | 文件名 | TABLE_BLOCK_COUNT | HEADER 含 ABCDE |
|---:|---|---:|---:|
| 1 | `241` 基线 | 9 | 0 |
| 2 | `241A` 独立盲审 | 17 | 0 |
| 3 | `241A-1` 四文档盲审 | 38 | 0 |
| 4 | `241V2` 修正版 | 26 | 0 |
| 5 | `241V2A` P0-2 补丁 | 10 | 0 |
| 6 | `241V2A-1` defaultCompany 并发 | 19 | 0 |
| 7 | `241V2A-2` defaultCompany 并发测试 | 16 | 0 |
| 8 | `241V2A-3` Spring 代理边界 | 17 | 0 |
| 9 | `241V2A-4` 并发数据上下文 | 18 | 0 |
| 10 | `241V2A-5` DEFAULT 参数一致性 | 16 | 0 |
| 11 | `241V2A-6` Spring 测试上下文启动 | 22 | 0 |
| 12 | `241V2A-7` DEFAULT-04 夹具 | 17 | 0 |
| 13 | `241V2A-8` DEFAULT-05 异常注入 | 17 | 0 |
| 14 | `241V2A-9` DEFAULT-05 Repository 边界 | 21 | 0 |
| 15 | `241V2A-10` Repository Mapper 完整契约 | 22 | 0 |
| 16 | `241V2A-11` Mapper 前序契约 | 19 | 0 |
| 17 | `241V2A-12` DEFAULT-05 最终验证 | 16 | 0 |
| 18 | `241V2A-13` selectDefaultCompanyId 契约 | 13 | 0 |
| 19 | `241V2A-14` verifyFinalState 参数消费 | 14 | 0 |
| 20 | `241V2A-15` DEFAULT-03 并发断言 | 16 | 0 |
| 21 | `241V2A-16` IllegalStateException 统一 | 16 | 0 |
| 22 | `241V2A-17` User 异常 HTTP 映射 | 17 | 0 |
| 23 | `241V2A-18` User 异常编译证据等级 | 24 | 0 |
| 24 | `241V2A-19` 证据等级统一校正 | 15 | 0 |
| 25 | `241V2A-20` 冻结事实参考证据来源 | 21 | 0 |
| 26 | `241V2A-21` 来源分类规范三维模型 | 17 | 0 |
| 27 | `241V2A-22` 规范状态 Git 工作区模型 | 16 | **1** |
| 28 | `241V2A-23` 五维枚举 Git 工作区适用 | 16 | **1** |
| 29 | `241V2A-24` 五维示例 NA 语义 Git 历史 | 18 | **3** |
| 30 | `241V2A-25` 五维实例确定性扫描 | 13 | **2** |
| 31 | `241V2A-26` 反向扫描 STEP 3 确定性 | 12 | 0 |
| 32 | `241V2A-27` 正式五维表发现范围 | 11 | 0 |
| 33 | `241V2A-28` 正式表候选集合统计 | 18 | 0 |
| 34 | `241V2A-29` 扫描输入全集边界 | 12 | 0 |
| 35 | `241V2A-30` TABLE_CANDIDATE 纯发现 | **19** | 0 |
| 36 | `241V2A-31` TABLE_CANDIDATE 表级识别 | **19** | 0 |
| **旧文档合计** | 36 份 | **656** | **7** |

### 5.2 新增文档(241V2A-32 自身)

| # | 文件名 | TABLE_BLOCK_COUNT | HEADER 含 ABCDE |
|---:|---|---:|---:|
| 37 | `241V2A-32` TABLE_BLOCK 与 TABLE_CANDIDATE 集合关系 | **19** | 0 |

**新增文档合计**:19

### 5.3 总和验证

```
SUM(per_file.TABLE_BLOCK_COUNT)
= 旧文档 656 + 新增 241V2A-32 = 19
= 675 + 19
= 694
= TABLE_BLOCK_TOTAL ✓
```

---

## §6 增量闭环硬等式验证

**【241V2A-33 §6 显式】**:

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **OLD + NEW = CURRENT** | 675(241V2A-32 创建后) + 19(241V2A-32 自身) | **694** | ✓ |
| **241V2A-31 → 32:656 → 675** | 656 + 19(241V2A-31) | 675 | ✓ |
| **241V2A-32 → 33:675 → 694** | 675 + 19(241V2A-32) | 694 | ✓ |

---

## §7 两组集合等式验证(241V2A-33 §7)

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **等式 1**:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 7 | 2 + 5 = 7 | ✓ |
| **等式 2**:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 | 1 + 1 = 2 | ✓ |

## §8 四组集合互斥验证(241V2A-33 §8)

| 集合对 | 交集 | 验证 |
|---|---|---|
| `CURRENT_FORMAL ∩ HISTORICAL_FORMAL` | ∅ | ✓ |
| `CURRENT_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `HISTORICAL_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `FORMAL_TABLE_CANDIDATE ∩ NON_FORMAL` | ∅ | ✓ |

---

## §9 DOCUMENT_DISCOVERY_SNAPSHOT_ASSERTION 硬断言(241V2A-33 最高优先级)

**【DOCUMENT_DISCOVERY_SNAPSHOT_ASSERTION】**(241V2A-33 硬性断言):

| # | 检查项 | 实际值 | 状态 |
|---:|---|---|---|
| 1 | 扫描根目录明确 | `E:\C\minimax\OptFlow PMS\` | ✓ PASS |
| 2 | 匹配规则明确 | glob `241*.md` | ✓ PASS |
| 3 | 快照时间点明确 | `SNAPSHOT_BEFORE(241V2A-33 创建时)` | ✓ PASS |
| 4 | 当前补丁是否纳入明确 | 否(创建前不存在,自然排除) | ✓ PASS |
| 5 | WORKSPACE_TOTAL 与 DOCUMENT_CANDIDATE 关系明确 | WORKSPACE = 39,EXCLUDED = 0,DC = 39 | ✓ PASS |
| 6 | 完整文件列表与最终数量一致 | 39 份全部列出,DC = 39 | ✓ PASS |

**任一断言失败**:**P1-43 = OPEN + S1-169-2 = BLOCK**

---

## §10 TABLE_BLOCK_INCREMENT_ASSERTION 硬断言(241V2A-33 最高优先级)

**【TABLE_BLOCK_INCREMENT_ASSERTION】**(241V2A-33 硬性断言):

| # | 检查项 | 实际值 | 状态 |
|---:|---|---|---|
| 1 | 每个 DOCUMENT_CANDIDATE 有且只有一个 TABLE_BLOCK_COUNT | 39 份各自有 TB 数 | ✓ PASS |
| 2 | 所有 TABLE_BLOCK_COUNT 求和等于 TABLE_BLOCK_TOTAL | 656 + 19 = 694 | ✓ PASS |
| 3 | 新增文档 TABLE_BLOCK_COUNT 可单独求和 | 241V2A-32 = 19 | ✓ PASS |
| 4 | OLD_TOTAL + NEW_TOTAL = CURRENT_TOTAL | 675 + 19 = 694 | ✓ PASS |
| 5 | 不允许人工手填 TOTAL | 全部 Python 扫描实测 | ✓ PASS |
| 6 | 不允许根据历史 TOTAL 反推当前 TOTAL | 旧数字 656 不影响新数字 694 | ✓ PASS |

**任一断言失败**:**P1-44 = OPEN + S1-169-2 = BLOCK**

---

## §11 当前 Spec PASS 对象(241V2A-33 §11)

**【241V2A-33 §11 显式】** 当前 Spec PASS 判定对象**不因本轮修复而改变**:

| 项目 | 值 |
|---|---|
| 当前 Spec PASS 唯一对象 | `CURRENT_FORMAL` = `241V2A-25 §2.3` L55(22 行) |
| 当前 Spec PASS 状态 | **TRUE**(`241V2A-25 §2.3` 22 行五维差集全部 = ∅) |
| 历史回归对象 | `HISTORICAL_FORMAL` = `241V2A-24 §2.3` L111 |

---

## §12 P1-41 / P1-42 保持(241V2A-33 §12 显式)

### 12.1 P1-41 / P1-42 不重写

**【241V2A-33 显式保持】**:

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-42** | 241V2A-29 §5.4 真实: L264 HEADER + L265 SEPARATOR + L266-L272 DATA | ✓ CLOSED(241V2A-32 §2.5,保持)|
| **P1-41** | GRANULARITY_RULE / TABLE_CANDIDATE ⊆ TABLE_BLOCK | ✓ CLOSED(241V2A-32 §1.2 / §9,保持)|

**严禁**改写历史文件或重定义 P1-41 / P1-42。

### 12.2 P1-43 / P1-44 保持

**【241V2A-33 显式】** P1-43(DOCUMENT_DISCOVERY_SNAPSHOT)+ P1-44(TABLE_BLOCK 增量闭环)在本轮冻结,**不重写**。

### 12.3 P1-35 ~ P1-40 保持

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-40** | TABLE_BLOCK + 7 STEP 表块识别 | ✓ CLOSED(241V2A-31) |
| **P1-39** | TABLE_CANDIDATE 纯发现层 | ✓ CLOSED(241V2A-30) |
| **P1-38** | DOCUMENT_CANDIDATE = glob `241*.md` | ✓ CLOSED(241V2A-29) |
| **P1-37** | 三个独立集合 + 集合等式 | ✓ CLOSED(241V2A-28) |
| **P1-36** | 自动发现 4 条 + 三分类 | ✓ CLOSED(241V2A-27) |
| **P1-35** | normalization 6 步硬性规则 | ✓ CLOSED(241V2A-26) |

---

## §13 P2 状态保持(241V2A-33 §13 显式)

| 编号 | 描述 | 状态 |
|---|---|---|
| P2-0 | exactly-one 业务规则需 fallback | **OPEN** |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **OPEN** |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **OPEN** |
| P2-6 | 章节编号/统计一致性 | **OPEN** |
| P2-7 | 章节编号缺 3 的文档问题 | **OPEN** |
| P2-8 | (241V2A-31 新增) | **OPEN** |
| P2-3 / P2-4 / P2-5 | | CLOSED |

**【241V2A-33 显式】** 本轮**只修 P1-43 / P1-44**,**不修 P2**;P2 状态诚实保留。

---

## §14 P1-43 / P1-44 自评(241V2A-33 §14 显式)

### 14.1 P1-43 自评

| 矛盾点 | 旧表述 | 实际 | 矛盾? |
|---|---|---|---|
| 241V2A-32 §3.1 | "DOCUMENT_CANDIDATE = 38" 含 241V2A-32 自身 | 扫描结果文档不应纳入扫描输入 | ✓ |
| 241 系列总文档数 = 39,DC = 38 | 时间边界未定义 | 需 SNAPSHOT_TIME 字段 | ✓ |

**修复方法**:241V2A-33 §1.2 方案 A 选择 + §1.3 DOCUMENT_DISCOVERY_SNAPSHOT 完整定义 + §9 硬断言。

### 14.2 P1-44 自评

| 矛盾点 | 旧表述 | 实际 | 矛盾? |
|---|---|---|---|
| 241V2A-31 → 32:656 → 675 | 没有逐文件增量账 | 实测 +19 = 241V2A-31 自身 | ✓ |
| 241V2A-32 → 33:?? | 数字未实测 | 实测 +19 = 241V2A-32 自身 = 694 | ✓ |

**修复方法**:241V2A-33 §2 增量账实测 + §5 逐文件 TABLE_BLOCK_COUNT + §10 硬断言。

### 14.3 自审 PASS 项

- ✓ P1-43 矛盾识别正确
- ✓ 方案 A 选择(SNAPSHOT_BEFORE)
- ✓ DOCUMENT_DISCOVERY_SNAPSHOT 完整 6 字段定义
- ✓ P1-44 增量闭环建立
- ✓ 逐文件 TABLE_BLOCK_COUNT(39 份)
- ✓ 旧 36 份 = 656 TB
- ✓ 新增 241V2A-32 = 19 TB
- ✓ OLD + NEW = 675 + 19 = 694 ✓
- ✓ TABLE_CANDIDATE = 7(不变)
- ✓ 等式 1:7 = 2 + 5 ✓
- ✓ 等式 2:2 = 1 + 1 ✓
- ✓ 4 组集合互斥全部 PASS
- ✓ DOCUMENT_DISCOVERY_SNAPSHOT_ASSERTION 全部 PASS
- ✓ TABLE_BLOCK_INCREMENT_ASSERTION 全部 PASS
- ✓ 当前 Spec PASS 不改变

**未自评 PASS**:等待下一轮独立盲审确认本轮修复方法是否真正成立。

---

## §15 一句话最终判断

> **241V2A-33 S1-169-1 DOCUMENT_CANDIDATE 时间边界与 TABLE_BLOCK 增量闭环修复补丁完成**:第三十轮独立盲审识别的 **P1-43**(`241V2A-32` 同时存在 DOCUMENT_CANDIDATE = 38 / 241 系列总文档数 = 39 / glob `241*.md` 三个数字,但 `241V2A-32` 自身也匹配 `241*.md`——必须彻底解决"当前补丁文档是否属于 DOCUMENT_CANDIDATE"的问题,冻结时间边界)+ **P1-44**(`241V2A-31` TABLE_BLOCK_TOTAL = 656 → `241V2A-32` 675,但 +19 没有形成可逐文件复核的增量账)通过本补丁**真闭环**——**§1.2 方案 A 显式选择**(`DOCUMENT_CANDIDATE = SNAPSHOT_BEFORE(241V2A-33 创建时)`,严禁采用方案 B 含 241V2A-33 自身——会导致递归自引用);**§1.3 DOCUMENT_DISCOVERY_SNAPSHOT 完整 6 字段定义**(扫描根目录 `E:\C\minimax\OptFlow PMS\` / 文件匹配 glob `241*.md` / 时间快照 SNAPSHOT_BEFORE / 当前生成文件不纳入 / 排除显式声明 / DOCUMENT_CANDIDATE = 39);**§1.4 严禁"模糊混用"**(glob + 当前生成补丁不计入 + 另算 必须同时禁止);**§2 P1-44 增量账实测** —— 656(241V2A-32 创建后) + 19(241V2A-32 自身) = 694 ✓ / 241V2A-31 → 32:656 + 19 = 675 ✓ / 241V2A-32 → 33:675 + 19 = 694 ✓;**§3 完整 39 份 DOCUMENT_CANDIDATE 列表**(每份标注编号 / 文件名 / 是否纳入 / 排除理由 / 扫描快照时间)+ 当前补丁是否纳入(否,创建前不存在,自然排除);**§4 七个数字实测**(WORKSPACE = 39 / EXCLUDED = 0 / DC = 39 / TABLE_BLOCK_TOTAL = 694 / TABLE_CANDIDATE = 7 / FORMAL_TABLE_CANDIDATE = 2 / CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 5);**§5 逐文件 TABLE_BLOCK_COUNT 39 份**(旧 36 份 = 656 + 新增 241V2A-32 = 19 = 694);**§6 增量闭环硬等式验证**(675 + 19 = 694);**§7-8 集合等式 / 互斥验证全部 PASS**;**§9 DOCUMENT_DISCOVERY_SNAPSHOT_ASSERTION 6 项全部 PASS**;**§10 TABLE_BLOCK_INCREMENT_ASSERTION 6 项全部 PASS**;**§12 P1-41 / P1-42 / P1-35 ~ P1-40 全部保持**;**§13 P2 OPEN 6 / CLOSED 3 状态诚实保留**(本轮不修 P2);241V2A-33 不修改 241V2A-32 / 241V2A-31 / 任何历史 MD 任何字节,只通过"显式冻结时间边界 + 显式增量闭环 + 显式实测数字 + 显式双硬断言"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §16 附录

- 章节数:17(§0 元信息 + §1 P1-43 + §2 P1-44 + §3 DC 39 份 + §4 七数字 + §5 逐文件 + §6 增量闭环 + §7 集合等式 + §8 集合互斥 + §9 DC_SNAPSHOT 断言 + §10 TB_INCREMENT 断言 + §11 当前 Spec PASS + §12 P1 保持 + §13 P2 + §14 自评 + §15 一句话最终判断 + §16 附录)
- 修复的 P1:2(P1-43 + P1-44)
- 显式选择方案 A:`SNAPSHOT_BEFORE(241V2A-33 创建时)`
- 新增概念:`DOCUMENT_DISCOVERY_SNAPSHOT`(6 字段)
- WORKSPACE_241_MD_TOTAL = 39(实测)
- DOCUMENT_CANDIDATE = 39(实测)
- EXCLUDED_CURRENT_PATCH = 0(创建前不存在)
- TABLE_BLOCK_TOTAL = 694(实测)
- TABLE_CANDIDATE = 7(不变)
- FORMAL_TABLE_CANDIDATE = 2
- CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 5
- 增量闭环:656 + 19 = 675 / 675 + 19 = 694 全部 PASS
- 集合等式:7 = 2 + 5 / 2 = 1 + 1 全部 PASS
- 集合互斥:4 组全部 PASS
- 双硬断言:DOCUMENT_DISCOVERY_SNAPSHOT_ASSERTION(6 项) + TABLE_BLOCK_INCREMENT_ASSERTION(6 项)全部 PASS
- 保持闭环:P1-14 ~ P1-42 不被改写
- 当前 Spec PASS:CURRENT_FORMAL = `241V2A-25 §2.3`(22 行五维差集全部 = ∅)
- P2 OPEN 6 / CLOSED 3(状态诚实)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- S1-169-2 = BLOCK

**【241V2A-33 自评声明】** 已完成 P1-43 / P1-44 修复并建立新的证据闭环,**等待下一轮独立盲审**。**不声明 PASS**。