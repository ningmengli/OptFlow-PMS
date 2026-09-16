# 241V2A-35 S1-169-1 DOCUMENT_CANDIDATE 快照成员校正与 TABLE_BLOCK 全量重算补丁

> **阶段**:S1-169-1
> **补丁类型**:独立盲审修复(第三十二轮)
> **优先级**:**最高**(校正 241V2A-34 §1.1 SNAPSHOT_BEFORE 集合成员错误 + 241V2A-34 §5 误排除 241V2A-33 + TABLE_BLOCK 全量重算)
> **基线 HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
> **严禁修改**:241V2A-34 / 241V2A-33 / 241V2A-32 / 241V2A-31 / 241V2A-30 / 任何历史 MD / VisionCare PMS 任何文件

---

## §0 元信息

- **创建日期**:2026-09-15
- **修复目标**:
  - **P1-44**:TABLE_BLOCK_TOTAL 必须在正确 DOCUMENT_CANDIDATE 上重新计算(不依赖 694)
  - **P1-45**:DOCUMENT_CANDIDATE 与逐文件 TABLE_BLOCK_COUNT 必须真正一一对应(不许遗漏)
  - **P1-46**:241V2A-34 §1.1 SNAPSHOT_BEFORE 集合成员错误——241V2A-34 创建时 WORKSPACE = 40(含 241V2A-33),但 241V2A-34 错误按 241V2A-33 §3.2 的 39 份定义排除 241V2A-33
- **本轮 P2 增量**:**无**(P2-0 / P2-1 / P2-2 / P2-6 / P2-7 / P2-8 OPEN 保持)

---

## §1 P1-46 修复:SNAPSHOT_BEFORE 集合成员校正(241V2A-35 最高优先级)

### 1.1 241V2A-34 §1.1 错误诊断**

**【241V2A-34 旧表述,本轮显式作废】**:

> `WORKSPACE_241_MD_TOTAL(扫描执行时) = 40`
> `EXCLUDED_CURRENT_PATCH = 1(241V2A-34 自身)`
> `DOCUMENT_CANDIDATE = 39`

**问题**:
- 241V2A-34 创建时 WORKSPACE = 40(含 241V2A-33 已存在)
- `EXCLUDED_CURRENT_PATCH = 0` (241V2A-33 已存在,**不应**排除)
- `DOCUMENT_CANDIDATE` 应该是 **40**(含 241V2A-33),不是 39
- 241V2A-34 §1.1 错误沿用 241V2A-33 §3.2 的 39 份定义,**遗漏** 241V2A-33

### 1.2 校正规则(241V2A-35 显式)

**【241V2A-35 显式冻结】** `SNAPSHOT_BEFORE(CURRENT_PATCH)` 完整规则:

```
SNAPSHOT_BEFORE(CURRENT_PATCH)
= 在创建 CURRENT_PATCH 之前已经存在的、glob "241*.md" 命中的所有 S1-169-1 untracked 文件

EXCLUDED_CURRENT_PATCH
= 当前正在创建的 CURRENT_PATCH 自身(创建前不存在,自然排除)
= 0(如果扫描在创建之前执行)
或
= 1(如果扫描时当前文件已经临时存在)

DOCUMENT_CANDIDATE
= SNAPSHOT_BEFORE(CURRENT_PATCH) - EXCLUDED_CURRENT_PATCH
```

**严禁**:
- ✗ 沿用前一轮的 39 份列表(241V2A-34 的错误)
- ✗ 为保持"39"数字自动删除 241V2A-33
- ✗ 任意排除已存在的 241*.md 文件

### 1.3 本轮 241V2A-35 的 SNAPSHOT_BEFORE 实测

**【241V2A-35 §1.3 实测】** 当前 WORKSPACE 实测:

```
WORKSPACE_241_MD_TOTAL = 41(含 241V2A-33 / 241V2A-34 已存在,241V2A-35 还未创建)
EXCLUDED_CURRENT_PATCH = 0(241V2A-35 还未创建,自然排除)
DOCUMENT_CANDIDATE = 41
```

---

## §2 重新冻结 SNAPSHOT_BEFORE 规则(241V2A-35 最高优先级)

### 2.1 完整 SNAPSHOT_BEFORE 定义(241V2A-35 显式)

**【241V2A-35 最高优先级冻结】** `SNAPSHOT_BEFORE(CURRENT_PATCH)`:

| # | 字段 | 内容 |
|---:|---|---|
| 1 | 扫描根目录 | `E:\C\minimax\OptFlow PMS\` |
| 2 | 文件匹配规则 | glob 模式 `241*.md` |
| 3 | 时间快照规则 | `SNAPSHOT_BEFORE(CURRENT_PATCH)` —— 在创建 CURRENT_PATCH 之前已存在的文件集合 |
| 4 | 当前生成文件是否排除 | **是**(创建前不存在,自然排除) |
| 5 | 已存在的快照文件是否纳入 | **是**(必须纳入,包括 241V2A-33 / 241V2A-34 等前序补丁) |
| 6 | DOCUMENT_CANDIDATE | **WORKSPACE - EXCLUDED** |

### 2.2 与 241V2A-33 / 241V2A-34 规则对比

| 规则版本 | 文档数 | 错误? |
|---|---|---|
| 241V2A-33 §1.3 | 39 | ⚠ (当时 241V2A-33 是当前补丁,自身未存在,但 241V2A-30/31/32 已存在)|
| 241V2A-34 §1.1 | 39 | ✗ **错误**(241V2A-33 已存在,应纳入 → 应为 40)|
| **241V2A-35 §1.3** | **41** | ✓ **正确**(241V2A-33 / 34 已存在,纳入)|

---

## §3 完整 41 条记录(241V2A-35 §3 实测)

### 3.1 实测方法

**【241V2A-35 §3.1 实测方法】**:

```
SNAPSHOT_BEFORE(241V2A-35 创建时)= 41 份
= glob "241*.md" ∩ S1-169-1 untracked 文档
EXCLUDED_CURRENT_PATCH = 0(241V2A-35 还未创建)
DOCUMENT_CANDIDATE = 41

Python 脚本:遍历 41 份文档,逐文件统计 TABLE_BLOCK_COUNT + HEADER_ABCDE_COUNT
```

### 3.2 41 条完整记录(241V2A-35 §3.2 实测)

| # | 文件名 | TABLE_BLOCK_COUNT | HEADER_ABCDE_COUNT |
|---:|---|---:|---:|
| 1 | `241A-1_S1-169-1_四文档最终独立盲审.md` | 38 | 0 |
| 2 | `241A_S1-169-1_基础设施设计独立盲审.md` | 17 | 0 |
| 3 | `241V2A-10_S1-169-1_UserCompanyRepository与Mapper完整契约冻结补丁.md` | 22 | 0 |
| 4 | `241V2A-11_S1-169-1_UserCompanyMapper前序契约一致性修复.md` | 19 | 0 |
| 5 | `241V2A-12_S1-169-1_DEFAULT-05最终验证契约冻结补丁.md` | 16 | 0 |
| 6 | `241V2A-13_S1-169-1_selectDefaultCompanyId读取契约一致性补丁.md` | 13 | 0 |
| 7 | `241V2A-14_S1-169-1_verifyFinalState expected参数消费冻结补丁.md` | 14 | 0 |
| 8 | `241V2A-15_S1-169-1_DEFAULT-03并发成功性断言冻结补丁.md` | 16 | 0 |
| 9 | `241V2A-16_S1-169-1_IllegalStateException异常契约统一冻结补丁.md` | 16 | 0 |
| 10 | `241V2A-17_S1-169-1_User异常契约与HTTP映射统一冻结补丁.md` | 17 | 0 |
| 11 | `241V2A-18_S1-169-1_User异常类编译契约与证据等级校正补丁.md` | 24 | 0 |
| 12 | `241V2A-19_S1-169-1_证据等级统一校正补丁.md` | 15 | 0 |
| 13 | `241V2A-1_S1-169-1_defaultCompany并发控制补充裁决.md` | 19 | 0 |
| 14 | `241V2A-20_S1-169-1_冻结事实与参考证据来源校正补丁.md` | 21 | 0 |
| 15 | `241V2A-21_S1-169-1_来源分类规范状态与Git状态三维模型补丁.md` | 17 | 0 |
| 16 | `241V2A-22_S1-169-1_规范形成状态与Git工作区状态模型校正补丁.md` | 16 | **1** |
| 17 | `241V2A-23_S1-169-1_五维枚举完整性与Git工作区适用性校正补丁.md` | 16 | **1** |
| 18 | `241V2A-24_S1-169-1_五维示例表枚举污染与NA语义及Git历史层隔离修复补丁.md` | 18 | **3** |
| 19 | `241V2A-25_S1-169-1_五维实例表确定性枚举与反向扫描方法修复补丁.md` | 13 | **2** |
| 20 | `241V2A-26_S1-169-1_反向扫描Step3确定性解析规则修复补丁.md` | 12 | 0 |
| 21 | `241V2A-27_S1-169-1_正式五维表发现范围与扫描对象确定性修复补丁.md` | 11 | 0 |
| 22 | `241V2A-28_S1-169-1_正式表候选集合与统计口径确定性修复补丁.md` | 18 | 0 |
| 23 | `241V2A-29_S1-169-1_扫描输入文档全集与TABLE_CANDIDATE边界修复补丁.md` | 12 | 0 |
| 24 | `241V2A-2_S1-169-1_defaultCompany并发测试与死锁表述修正.md` | 16 | 0 |
| 25 | `241V2A-30_S1-169-1_TABLE_CANDIDATE纯发现层与误命中保留规则修复补丁.md` | **19** | 0 |
| 26 | `241V2A-31_S1-169-1_TABLE_CANDIDATE表级识别与Markdown表块边界修复补丁.md` | **19** | 0 |
| 27 | `241V2A-32_S1-169-1_TABLE_BLOCK与TABLE_CANDIDATE集合关系及SEPARATOR证据修复补丁.md` | **19** | 0 |
| 28 | `241V2A-33_S1-169-1_DOCUMENT_CANDIDATE时间边界与TABLE_BLOCK增量闭环修复补丁.md` | **20** | 0 |
| 29 | `241V2A-34_S1-169-1_TABLE_BLOCK逐文件全覆盖与总数一致性修复补丁.md` | **11** | 0 |
| 30 | `241V2A-3_S1-169-1_并发测试Spring代理边界补丁.md` | 17 | 0 |
| 31 | `241V2A-4_S1-169-1_并发测试数据上下文补丁.md` | 18 | 0 |
| 32 | `241V2A-5_S1-169-1_DEFAULT测试参数一致性补丁.md` | 16 | 0 |
| 33 | `241V2A-6_S1-169-1_Spring测试上下文启动边界补丁.md` | 22 | 0 |
| 34 | `241V2A-7_S1-169-1_DEFAULT-04测试夹具事务边界补丁.md` | 17 | 0 |
| 35 | `241V2A-8_S1-169-1_DEFAULT-05异常注入与Repository代理补丁.md` | 17 | 0 |
| 36 | `241V2A-9_S1-169-1_DEFAULT-05_UserCompanyRepository边界冻结补丁.md` | 21 | 0 |
| 37 | `241V2A_S1-169-1_P0-2强制覆盖补丁.md` | 10 | 0 |
| 38 | `241V2_S1-169-1_基础设施设计修正版.md` | 26 | 0 |
| 39 | `241V3_S1-169-1_IGNORE_TABLES代码一致性补丁.md` | **24** | 0 |
| 40 | `241V4_S1-169-1_表数量与TenantLine覆盖率一致性补丁.md` | **24** | 0 |
| 41 | `241_S1-169-1_V4.4后端工程骨架与基础设施迁移基线.md` | 9 | 0 |

### 3.3 总和验证

**【241V2A-35 §3.3 实测】**:

```
COUNT(records) = 41
SUM(TABLE_BLOCK_COUNT) = 725
SUM(HEADER_ABCDE_COUNT) = 7
```

**`SUM(TABLE_BLOCK_COUNT) = 725 = TABLE_BLOCK_TOTAL`** ✓
**`SUM(HEADER_ABCDE_COUNT) = 7 = TABLE_CANDIDATE`** ✓

### 3.4 特别检查:241V2A-30 ~ 34 / 241V3 / 241V4

**【241V2A-35 §3.4 特别检查】**:

| 文档 | TABLE_BLOCK_COUNT | HEADER_ABCDE_COUNT |
|---|---:|---:|
| `241V2A-30` | **19** | 0 |
| `241V2A-31` | **19** | 0 |
| `241V2A-32` | **19** | 0 |
| `241V2A-33` | **20** | 0 |
| `241V2A-34` | **11** | 0 |
| `241V3` | **24** | 0 |
| `241V4` | **24** | 0 |

**所有 7 个特别检查项都有记录**(在 §3.2 表的 #25-29 / #39 / #40)。

---

## §4 增量关系(241V2A-35 §4 显式)

### 4.1 增量闭环

**【241V2A-35 §4.1 实测】**:

```
旧快照(241V2A-34 §2.3)DOCUMENT_CANDIDATE = 39
+ 新增文件(241V2A-33 + 241V2A-34)= 2
= 当前快照(241V2A-35 §3.3)DOCUMENT_CANDIDATE = 41

旧快照(241V2A-34 §2.3)TABLE_BLOCK_TOTAL = 694
+ 新增文件 TABLE_BLOCK:
  241V2A-33 = 20
  241V2A-34 = 11
  = 31
= 当前快照 TABLE_BLOCK_TOTAL = 725
```

### 4.2 增量闭环硬等式验证

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **DC:** 旧 + 新增 = 当前 | 39 + 2 | **41** | ✓ |
| **TB:** 旧 + 新增 = 当前 | 694 + 31 | **725** | ✓ |

### 4.3 241V2A-34 错误诊断与校正

**【241V2A-35 §4.3 显式】** 241V2A-34 §1.1 的错误:

| 项目 | 241V2A-34 旧 | 241V2A-35 校正 |
|---|---:|---:|
| WORKSPACE | 40 | **41**(241V2A-33 已存在)|
| EXCLUDED_CURRENT_PATCH | 1(241V2A-34)| **0**(241V2A-35)|
| DOCUMENT_CANDIDATE | 39(错误)| **41**(正确)|
| 241V2A-33 | 排除(不在 DC)| **纳入**(20 TB)|
| TABLE_BLOCK_TOTAL | 694 | **725**(实测,41 份)|

**严禁**为保持 694 / 39 数字而排除 241V2A-33。

---

## §5 DOCUMENT_SNAPSHOT_MEMBERSHIP_ASSERTION 硬断言(241V2A-35 最高优先级)

**【DOCUMENT_SNAPSHOT_MEMBERSHIP_ASSERTION】**(241V2A-35 硬性断言):

| # | 检查项 | 实际值 | 状态 |
|---:|---|---|---|
| A | 所有匹配 241*.md 的快照文件都有明确成员状态 | 41 份全部明确 | ✓ PASS |
| B | 当前补丁不进入自己的输入集合 | 241V2A-35 未纳入(创建前不存在)| ✓ PASS |
| C | 所有在当前补丁之前已存在的 241*.md 必须进入集合 | 241V2A-33 / 34 已纳入 | ✓ PASS |
| D | DOCUMENT_CANDIDATE 完整列表与实际快照集合完全相等 | 41 份全部列出,set equality 验证 | ✓ PASS |
| E | 不允许只验证 cardinality | 41 份逐一列出 | ✓ PASS |
| F | 必须验证 set equality | set(files) = 41 = DOCUMENT_CANDIDATE | ✓ PASS |

**任一断言失败**:**P1-46 = OPEN + S1-169-2 = BLOCK**

---

## §6 DOCUMENT_TABLE_BLOCK_RECALCULATION_ASSERTION 硬断言(241V2A-35 最高优先级)

**【DOCUMENT_TABLE_BLOCK_RECALCULATION_ASSERTION】**(241V2A-35 硬性断言):

| # | 检查项 | 实际值 | 状态 |
|---:|---|---|---|
| A | 每个 DOCUMENT_CANDIDATE 恰有一条 TB_COUNT | 41 条记录 = 41 份文档 | ✓ PASS |
| B | 无遗漏 | 41 份全部有记录 | ✓ PASS |
| C | 无重复 | set = 41 | ✓ PASS |
| D | SUM = TABLE_BLOCK_TOTAL | 725 = 725 | ✓ PASS |
| E | TABLE_CANDIDATE 来自正确 TB 集合 | 7 来自 HEADER 含 ABCDE 的 7 张 TABLE_BLOCK | ✓ PASS |

**任一断言失败**:**P1-44 / P1-45 = OPEN + S1-169-2 = BLOCK**

---

## §7 两组集合等式验证(241V2A-35 §7 实测)

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **等式 1**:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 7 | 2 + 5 = 7 | ✓ |
| **等式 2**:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 | 1 + 1 = 2 | ✓ |

## §8 四组集合互斥验证(241V2A-35 §8 实测)

| 集合对 | 交集 | 验证 |
|---|---|---|
| `CURRENT_FORMAL ∩ HISTORICAL_FORMAL` | ∅ | ✓ |
| `CURRENT_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `HISTORICAL_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `FORMAL_TABLE_CANDIDATE ∩ NON_FORMAL` | ∅ | ✓ |

---

## §9 当前 Spec PASS 对象(241V2A-35 §9)

**【241V2A-35 §9 显式】** 当前 Spec PASS 判定对象**不因本轮修复而改变**:

| 项目 | 值 |
|---|---|
| 当前 Spec PASS 唯一对象 | `CURRENT_FORMAL` = `241V2A-25 §2.3` L55(22 行) |
| 当前 Spec PASS 状态 | **TRUE**(`241V2A-25 §2.3` 22 行五维差集全部 = ∅) |
| 历史回归对象 | `HISTORICAL_FORMAL` = `241V2A-24 §2.3` L111 |

---

## §10 P1-41 / P1-42 保持(241V2A-35 §10 显式)

### 10.1 P1-41 / P1-42 保持

**【241V2A-35 显式保持】**:

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-42** | 241V2A-29 §5.4 真实: L264 HEADER + L265 SEPARATOR + L266-L272 DATA | ✓ CLOSED(241V2A-32)|
| **P1-41** | GRANULARITY_RULE / TABLE_CANDIDATE ⊆ TABLE_BLOCK | ✓ CLOSED(241V2A-32)|
| **1 TC -> exactly 1 TB** | | ✓ 保持 |
| **1 TB -> at most 1 TC** | | ✓ 保持 |

**严禁**改写历史文件或重定义 P1-41 / P1-42。

### 10.2 P1-44 / P1-45 / P1-46 状态

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-46** | SNAPSHOT_BEFORE 集合成员校正 | ✓ CLOSED(241V2A-35)|
| **P1-45** | DOCUMENT_TABLE_BLOCK_COVERAGE_ASSERTION | ✓ CLOSED(241V2A-34,但基数错误已校正)|
| **P1-44** | TABLE_BLOCK_TOTAL 重新独立验证(725 实测)| ✓ CLOSED(241V2A-34,但数字校正)|

### 10.3 P1-35 ~ P1-43 保持

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-43** | DOCUMENT_DISCOVERY_SNAPSHOT 时间边界 | ✓ CLOSED(241V2A-33) |
| P1-40 / P1-39 / P1-38 / P1-37 / P1-36 / P1-35 | 全部 CLOSED | 不变 |

---

## §11 P2 状态保持(241V2A-35 §11 显式)

| 编号 | 描述 | 状态 |
|---|---|---|
| P2-0 | exactly-one 业务规则需 fallback | **OPEN** |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **OPEN** |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **OPEN** |
| P2-6 | 章节编号/统计一致性 | **OPEN** |
| P2-7 | 章节编号缺 3 的文档问题 | **OPEN** |
| P2-8 | (241V2A-31 新增) | **OPEN** |
| P2-3 / P2-4 / P2-5 | | CLOSED |

**【241V2A-35 显式】** 本轮**只修 P1-44 / P1-45 / P1-46**,**不修 P2**;P2 状态诚实保留。

---

## §12 P1-44 / P1-45 / P1-46 自评(241V2A-35 §12 显式)

### 12.1 P1-46 自评

| 矛盾点 | 旧 | 实测 | 矛盾? |
|---|---|---|---|
| 241V2A-34 §1.1 DC = 39 | 排除 241V2A-33 | 应为 40(含 241V2A-33)| ✓ |
| 241V2A-34 §5 误排除 | 39 份不重复 | 实际 40 份 | ✓ |

**修复方法**:241V2A-35 §1.2 校正规则 + §2.1 完整 6 字段定义 + §5 硬断言。

### 12.2 P1-45 自评

| 检查项 | 实际值 | 状态 |
|---|---|---|
| A. 39 份 → 41 份 | 41 | ✓(重新扫描 41 份)|
| B. 39 条 → 41 条 | 41 | ✓ |
| C. 一一对应,无遗漏 | 41 份 = 41 条 | ✓ |
| D. 无重复 | set = 41 | ✓ |
| E. SUM = TABLE_BLOCK_TOTAL | 725 = 725 | ✓ |

**修复方法**:241V2A-35 §3 完整 41 条记录 + §6 硬断言。

### 12.3 P1-44 自评

| 检查项 | 旧 | 实测 | 状态 |
|---|---|---|---|
| 旧 39 份 TB | 694 | 694 | ✓ |
| 241V2A-33 TB | (未纳入) | **20** | ✓ 重新实测 |
| 241V2A-34 TB | (未纳入) | **11** | ✓ 重新实测 |
| 当前 41 份 TB | 694 | **725** | ✓ |
| 增量闭环 | 694 + 31 = 725 | 725 | ✓ |

**修复方法**:241V2A-35 §4 增量闭环 + 不依赖 694 / 39 先验。

### 12.4 自审 PASS 项

- ✓ P1-46 矛盾识别正确(241V2A-34 §1.1 错误排除 241V2A-33)
- ✓ 校正 SNAPSHOT_BEFORE 规则
- ✓ DOCUMENT_CANDIDATE = 41(实测,含 241V2A-33 / 34)
- ✓ 41 条记录全覆盖,无遗漏无重复
- ✓ 241V3 = 24,241V4 = 24,241V2A-30/31/32/33/34 = 19/19/19/20/11
- ✓ TABLE_BLOCK_TOTAL = 725(实测,不依赖 694)
- ✓ 增量闭环:39 + 2 = 41,694 + 31 = 725
- ✓ 等式 1:7 = 2 + 5 ✓
- ✓ 等式 2:2 = 1 + 1 ✓
- ✓ 4 组集合互斥全部 PASS
- ✓ DOCUMENT_SNAPSHOT_MEMBERSHIP_ASSERTION 6 项全部 PASS
- ✓ DOCUMENT_TABLE_BLOCK_RECALCULATION_ASSERTION 5 项全部 PASS
- ✓ 当前 Spec PASS 不改变

**未自评 PASS**:等待下一轮独立盲审确认本轮修复方法是否真正成立。

---

## §13 一句话最终判断

> **241V2A-35 S1-169-1 DOCUMENT_CANDIDATE 快照成员校正与 TABLE_BLOCK 全量重算补丁完成**:第三十二轮独立盲审识别的 **P1-46**(`241V2A-34 §1.1` SNAPSHOT_BEFORE 集合成员错误——241V2A-34 创建时 WORKSPACE = 40(含 241V2A-33),但 241V2A-34 错误按 241V2A-33 §3.2 的 39 份定义排除 241V2A-33,得到错的 DC = 39)+ **P1-45**(DOCUMENT_CANDIDATE 与逐文件 TABLE_BLOCK_COUNT 必须真正一一对应)+ **P1-44**(TABLE_BLOCK_TOTAL 当前总数必须在正确 DOCUMENT_CANDIDATE 上重新计算)通过本补丁**真闭环**——**§1.2 SNAPSHOT_BEFORE 规则校正**(`EXCLUDED_CURRENT_PATCH = 0` 如果当前文件还未创建;严禁沿用前一轮数字);**§2.1 完整 6 字段 SNAPSHOT_BEFORE 重新冻结**(扫描根目录 / glob 241*.md / SNAPSHOT_BEFORE(CURRENT_PATCH) / 当前生成文件排除 / 已存在快照文件必须纳入 / DOCUMENT_CANDIDATE = WORKSPACE - EXCLUDED);**§3.2 完整 41 条记录(241V2A-35 §3 实测,Python 逐文件扫描)**——每条对应一份文档,标注 TABLE_BLOCK_COUNT + HEADER_ABCDE_COUNT,所有 41 份全部有记录,无遗漏无重复;**§3.3 总和验证实测** —— COUNT(records) = 41 / SUM(TABLE_BLOCK_COUNT) = 725 / SUM(HEADER_ABCDE_COUNT) = 7;**§3.4 特别检查 241V2A-30 = 19 / 241V2A-31 = 19 / 241V2A-32 = 19 / 241V2A-33 = 20 / 241V2A-34 = 11 / 241V3 = 24 / 241V4 = 24**(全部实测,不假定);**§4 增量闭环** —— 旧 39 份(694)+ 新增 241V2A-33(20)+ 241V2A-34(11)= 31 → 当前 41 份 725 ✓ / DC:39 + 2 = 41 ✓;**§5 DOCUMENT_SNAPSHOT_MEMBERSHIP_ASSERTION 6 项硬断言** —— A 全部明确 / B 当前补丁排除 / C 已存在快照文件必须纳入 / D set equality / E 不只验证 cardinality / F set equality 验证;**§6 DOCUMENT_TABLE_BLOCK_RECALCULATION_ASSERTION 5 项硬断言** —— A 41 条对应 41 份 / B 无遗漏 / C 无重复 / D SUM = TABLE_BLOCK_TOTAL / E TABLE_CANDIDATE 来自正确 TB 集合;**§7-8 集合等式 + 互斥全部 PASS**;**§9 当前 Spec PASS 不改变**(`CURRENT_FORMAL` = `241V2A-25 §2.3` 22 行五维差集全部 = ∅);**§10 P1-41 / P1-42 / P1-43 / P1-35 ~ P1-40 全部保持**;**§11 P2 OPEN 6 / CLOSED 3 状态诚实保留**(本轮不修 P2);241V2A-35 不修改 241V2A-34 / 241V2A-33 / 任何历史 MD 任何字节,只通过"校正 SNAPSHOT_BEFORE 集合成员 + 实测 41 份 725 TB + 双硬断言"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §14 附录

- 章节数:15(§0 元信息 + §1 P1-46 + §2 重新冻结 + §3 41 条记录 + §4 增量 + §5 快照断言 + §6 重算断言 + §7 等式 + §8 互斥 + §9 当前 Spec PASS + §10 P1 保持 + §11 P2 + §12 自评 + §13 一句话最终判断 + §14 附录)
- 修复的 P1:3(P1-44 + P1-45 + P1-46)
- 显式校正:`241V2A-34 §1.1` DC = 39 → 实际应为 40(含 241V2A-33)
- 严禁使用先验答案:656 / 675 / 694 / 39
- WORKSPACE_241_MD_TOTAL = 41(实测)
- DOCUMENT_CANDIDATE = 41(含 241V2A-33 / 34)
- EXCLUDED_CURRENT_PATCH = 0(241V2A-35 还未创建)
- TABLE_BLOCK_TOTAL = 725(实测,41 份)
- TABLE_CANDIDATE = 7(实测)
- FORMAL_TABLE_CANDIDATE = 2
- CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 5
- 增量闭环:39 + 2 = 41 / 694 + 31 = 725 全部 PASS
- 集合等式:7 = 2 + 5 / 2 = 1 + 1 全部 PASS
- 集合互斥:4 组全部 PASS
- 双硬断言:DOCUMENT_SNAPSHOT_MEMBERSHIP_ASSERTION(6 项) + DOCUMENT_TABLE_BLOCK_RECALCULATION_ASSERTION(5 项)全部 PASS
- 保持闭环:P1-14 ~ P1-43 不被改写
- 当前 Spec PASS:CURRENT_FORMAL = `241V2A-25 §2.3`(22 行五维差集全部 = ∅)
- P2 OPEN 6 / CLOSED 3(状态诚实)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- S1-169-2 = BLOCK

**【241V2A-35 自评声明】** 已完成 P1-44 / P1-45 / P1-46 修复并建立新的证据闭环,**等待下一轮独立盲审**。**不声明 PASS**。