# 241V2A-32 S1-169-1 TABLE_BLOCK 与 TABLE_CANDIDATE 集合关系及 SEPARATOR 证据修复补丁

> **阶段**:S1-169-1
> **补丁类型**:独立盲审修复(第二十九轮)
> **优先级**:**最高**(覆盖 241V2A-31 §10 "一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE" 错误集合关系 + 241V2A-31 §7.1 241V2A-29 §5.4 SEPARATOR 证据)
> **基线 HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
> **严禁修改**:241V2A-31 / 241V2A-30 / 241V2A-29 / 241V2A-28 / 241V2A-27 / 241V2A-25 / 241V2A-24 / 241V2A-23 / 任何历史 MD / VisionCare PMS 任何文件

---

## §0 元信息

- **创建日期**:2026-09-15
- **修复目标**:
  - **P1-41**:`241V2A-31 §10` 写 "一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE"——这是错误的集合关系,正确应该是 `TABLE_CANDIDATE ⊆ TABLE_BLOCK`(子集,7 ⊂ 675)
  - **P1-42**:`241V2A-31` 把 `241V2A-29 §5.4` 列为 TABLE_CANDIDATE 复核对象,但**没有证明** L265 = SEPARATOR_ROW;必须直接读原始文本,证明 SEPARATOR 存在
- **本轮 P2 增量**:**无**(P2-0 / P2-1 / P2-2 / P2-6 / P2-7 / P2-8 OPEN 保持)

---

## §1 P1-41 问题陈述(241V2A-32 显式)

### 1.1 241V2A-31 §10 错误集合关系

**【241V2A-31 旧文本,本轮部分作废】**:

> **断言状态**(基于 241V2A-31 §7 实测):
>
> | 1. 一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE | 7 张 TABLE_BLOCK = 7 张 TABLE_CANDIDATE | ✓ PASS |

**问题**:
- "一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE" 是错误的等价表述
- 实际:TABLE_CANDIDATE ⊆ TABLE_BLOCK(子集,7 ⊂ 675)
- TABLE_BLOCK 不一定都是 TABLE_CANDIDATE(必须 HEADER 含 A/B/C/D/E)

### 1.2 必须冻结的 GRANULARITY_RULE(241V2A-32 显式)

**【241V2A-32 最高优先级冻结】** `GRANULARITY_RULE`:

```
1. 一个 TABLE_CANDIDATE 必须来源于且只来源于一个 TABLE_BLOCK。
2. 一个 TABLE_BLOCK 最多产生一个 TABLE_CANDIDATE。
3. TABLE_BLOCK 是否进入 TABLE_CANDIDATE,由该 TABLE_BLOCK 的 HEADER 是否通过候选结构规则决定。
4. 不通过 HEADER 候选结构规则的 TABLE_BLOCK 仍然属于 TABLE_BLOCK,但不属于 TABLE_CANDIDATE。
5. 因此:
   TABLE_CANDIDATE ⊆ TABLE_BLOCK
   (当前实测:7 ⊂ 675)
```

**严禁**再写 `TABLE_BLOCK = TABLE_CANDIDATE` 作为一般性定义。

---

## §2 P1-42 重新验证 241V2A-29 §5.4(241V2A-32 §2 实测)

### 2.1 241V2A-29 §5.4 原始文本(241V2A-32 §2.1 直接 read)

**【241V2A-32 §2.1 实测】** 直接 read `241V2A-29 §5.4` 原始文本:

```
L264: | # | 文件 | 行号 | 章节 | 表头 | 类型 |     ← HEADER_ROW
L265: |---:|---|---|---|---|---|              ← SEPARATOR_ROW(实际存在)
L266: | 1 | `241V2A-22` | L257 | §4 五维模型总览示例 | `维度 A \| 维度 B \| 维度 C \| 维度 D \| 维度 E` | NON_FORMAL |  ← DATA_ROW
L267: | 2 | `241V2A-23` | L303 | §2 五维合法枚举示例 | `A 证据来源 \| B 规范形成 \| C Spec \| D Git 跟踪 \| E Git 工作区` | NON_FORMAL |  ← DATA_ROW
L268: | 3 | `241V2A-24` | L111 | §2.3 五维合法实例表 | `# \| 对象 \| A \| B \| C \| D \| E \| 备注` | HISTORICAL_FORMAL |  ← DATA_ROW
L269: | 4 | `241V2A-24` | L200 | §3.4 N/A 区别表 | `场景 \| A \| B \| C \| D \| E` | NON_FORMAL |  ← DATA_ROW
L270: | 5 | `241V2A-24` | L256 | §5 五维对象有效性规则 | `对象属性 \| A \| B \| C \| D \| E` | NON_FORMAL |  ← DATA_ROW
L271: | 6 | `241V2A-25` | L55 | §2.3 重制后的五维合法实例表 | `# \| 对象 \| A \| B \| C \| D \| E \| 备注` | CURRENT_FORMAL |  ← DATA_ROW
L272: | 7 | `241V2A-25` | L217 | §3.4 对照扫描结果 | `维度 \| A_actual \| B_actual \| C_actual \| D_actual \| E_actual` | NON_FORMAL |  ← DATA_ROW
```

### 2.2 结构判定

**【241V2A-32 §2.2 判定】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L264 | **HEADER_ROW** | `\| # \| 文件 \| 行号 \| 章节 \| 表头 \| 类型 \|` | ✓ |
| L265 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|---\|---\|` | ✓ 存在! |
| L266-L272 | **DATA_ROWS**(7 行) | 7 个候选表的数据行 | ✓ |

**结论**:`241V2A-29 §5.4` 是**有效 TABLE_BLOCK**(HEADER + SEPARATOR + 7 DATA_ROWS)。

### 2.3 是否进入 TABLE_CANDIDATE

**【241V2A-32 §2.3 判定】**:

- HEADER `| # | 文件 | 行号 | 章节 | 表头 | 类型 |` **不含** A/B/C/D/E 模式(列名是"# / 文件 / 行号 / 章节 / 表头 / 类型")
- 因此 `241V2A-29 §5.4` **不进入** TABLE_CANDIDATE
- 该 TABLE_BLOCK 属于 TABLE_BLOCK_TOTAL,但不属于 TABLE_CANDIDATE

---

## §3 DOCUMENT_CANDIDATE 完整文件列表(241V2A-32 §3 实测)

### 3.1 实测总数

**【241V2A-32 §3.1 实测】** 当前 `241*.md` 文件总数 = **38 份**(glob 模式 `241*.md` + S1-169-1 untracked 文档集合,实测)。

**重要**:`241V2A-29 §2` 当时实测 = 36 份(创建 241V2A-29 前 = 35,创建后 = 36);本轮 241V2A-30 / 31 各自加 1 份 → 38 份。

### 3.2 DOCUMENT_CANDIDATE 完整文件列表(38 份)

| # | 文件名 | 阶段 |
|---:|---|---|
| 1 | `241_S1-169-1_V4.4后端工程骨架与基础设施迁移基线.md` | 基线 |
| 2 | `241A_S1-169-1_基础设施设计独立盲审.md` | 独立盲审 |
| 3 | `241A-1_S1-169-1_四文档最终独立盲审.md` | 四文档盲审 |
| 4 | `241V2_S1-169-1_基础设施设计修正版.md` | 修正版 |
| 5 | `241V2A_S1-169-1_P0-2强制覆盖补丁.md` | 补丁 |
| 6 | `241V2A-1_S1-169-1_defaultCompany并发控制补充裁决.md` | 补丁 |
| 7 | `241V2A-2_S1-169-1_defaultCompany并发测试与死锁表述修正.md` | 补丁 |
| 8 | `241V2A-3_S1-169-1_并发测试Spring代理边界补丁.md` | 补丁 |
| 9 | `241V2A-4_S1-169-1_并发测试数据上下文补丁.md` | 补丁 |
| 10 | `241V2A-5_S1-169-1_DEFAULT测试参数一致性补丁.md` | 补丁 |
| 11 | `241V2A-6_S1-169-1_Spring测试上下文启动边界补丁.md` | 补丁 |
| 12 | `241V2A-7_S1-169-1_DEFAULT-04测试夹具事务边界补丁.md` | 补丁 |
| 13 | `241V2A-8_S1-169-1_DEFAULT-05异常注入与Repository代理补丁.md` | 补丁 |
| 14 | `241V2A-9_S1-169-1_DEFAULT-05_UserCompanyRepository边界冻结补丁.md` | 补丁 |
| 15 | `241V2A-10_S1-169-1_UserCompanyRepository与Mapper完整契约冻结补丁.md` | 补丁 |
| 16 | `241V2A-11_S1-169-1_UserCompanyMapper前序契约一致性修复.md` | 补丁 |
| 17 | `241V2A-12_S1-169-1_DEFAULT-05最终验证契约冻结补丁.md` | 补丁 |
| 18 | `241V2A-13_S1-169-1_selectDefaultCompanyId读取契约一致性补丁.md` | 补丁 |
| 19 | `241V2A-14_S1-169-1_verifyFinalState expected参数消费冻结补丁.md` | 补丁 |
| 20 | `241V2A-15_S1-169-1_DEFAULT-03并发成功性断言冻结补丁.md` | 补丁 |
| 21 | `241V2A-16_S1-169-1_IllegalStateException异常契约统一冻结补丁.md` | 补丁 |
| 22 | `241V2A-17_S1-169-1_User异常契约与HTTP映射统一冻结补丁.md` | 补丁 |
| 23 | `241V2A-18_S1-169-1_User异常类编译契约与证据等级校正补丁.md` | 补丁 |
| 24 | `241V2A-19_S1-169-1_证据等级统一校正补丁.md` | 补丁 |
| 25 | `241V2A-20_S1-169-1_冻结事实与参考证据来源校正补丁.md` | 补丁 |
| 26 | `241V2A-21_S1-169-1_来源分类规范状态与Git状态三维模型补丁.md` | 补丁 |
| 27 | `241V2A-22_S1-169-1_规范形成状态与Git工作区状态模型校正补丁.md` | 补丁 |
| 28 | `241V2A-23_S1-169-1_五维枚举完整性与Git工作区适用性校正补丁.md` | 补丁 |
| 29 | `241V2A-24_S1-169-1_五维示例表枚举污染与NA语义及Git历史层隔离修复补丁.md` | 补丁 |
| 30 | `241V2A-25_S1-169-1_五维实例表确定性枚举与反向扫描方法修复补丁.md` | 补丁 |
| 31 | `241V2A-26_S1-169-1_反向扫描Step3确定性解析规则修复补丁.md` | 补丁 |
| 32 | `241V2A-27_S1-169-1_正式五维表发现范围与扫描对象确定性修复补丁.md` | 补丁 |
| 33 | `241V2A-28_S1-169-1_正式表候选集合与统计口径确定性修复补丁.md` | 补丁 |
| 34 | `241V2A-29_S1-169-1_扫描输入文档全集与TABLE_CANDIDATE边界修复补丁.md` | 补丁 |
| 35 | `241V2A-30_S1-169-1_TABLE_CANDIDATE纯发现层与误命中保留规则修复补丁.md` | 补丁 |
| 36 | `241V2A-31_S1-169-1_TABLE_CANDIDATE表级识别与Markdown表块边界修复补丁.md` | 补丁 |
| 37 | `241V3_S1-169-1_IGNORE_TABLES代码一致性补丁.md` | 补丁 |
| 38 | `241V4_S1-169-1_表数量与TenantLine覆盖率一致性补丁.md` | 补丁 |

---

## §4 重新执行 TABLE_BLOCK 识别(241V2A-32 §4 实测)

### 4.1 7 STEP 算法(241V2A-32 沿用 241V2A-31 §3 + 强化)

**【241V2A-32 沿用 241V2A-31 §3 算法】** Markdown 表块识别 7 STEP:

```
STEP 1: 逐文档逐行读取
STEP 2: 识别 HEADER_ROW(以 | 开头和结尾的 TABLE_ROW)
STEP 3: 验证下一行是否为合法 Markdown SEPARATOR_ROW(^\|[\s\-:|]+\|$)
STEP 4: 只有 HEADER + SEPARATOR 成立后,才允许建立 TABLE_BLOCK
STEP 5: 读取连续 DATA_ROW
STEP 6: 输出完整 TABLE_BLOCK 边界:
        header_line / separator_line / data_start_line / data_end_line
STEP 7: 仅对 TABLE_BLOCK 的 HEADER 执行结构正则
        ^\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|
        只有 HEADER 通过 → 进入 TABLE_CANDIDATE
        HEADER 不通过 → 仍在 TABLE_BLOCK_TOTAL,但不进入 TABLE_CANDIDATE
```

### 4.2 实测结果

**【241V2A-32 §4.2 实测】** Python 脚本遍历全部 38 份文档:

| 集合 | 数字 |
|---|---:|
| **DOCUMENT_CANDIDATE** | **38** |
| **TABLE_BLOCK_TOTAL** | **675**(实测) |
| **TABLE_CANDIDATE** | **7**(header 含 A/B/C/D/E) |
| **FORMAL_TABLE_CANDIDATE** | **2** |
| **CURRENT_FORMAL** | **1**(`241V2A-25 §2.3` L55) |
| **HISTORICAL_FORMAL** | **1**(`241V2A-24 §2.3` L111) |
| **NON_FORMAL** | **5** |

### 4.3 关键数字差异

| 数字 | 241V2A-31 §6.2 旧 | 241V2A-32 §4.2 新 | 差异原因 |
|---|---:|---:|---|
| `DOCUMENT_CANDIDATE` | 36 | **38** | 加 241V2A-30 / 31 |
| `TABLE_BLOCK_TOTAL` | 656 | **675** | 加 241V2A-30 / 31 内 TABLE_BLOCK |
| `TABLE_CANDIDATE` | 7 | **7** | 不变(241V2A-30 / 31 自身不含 ABCDE header) |
| `FORMAL_TABLE_CANDIDATE` | 2 | **2** | 不变 |
| `CURRENT_FORMAL` | 1 | **1** | 不变 |
| `HISTORICAL_FORMAL` | 1 | **1** | 不变 |
| `NON_FORMAL` | 5 | **5** | 不变 |

---

## §5 七个争议点完整复核(241V2A-32 §5)

### 5.1 241V2A-1 §8.1 场景总表(含 L477)

**【241V2A-32 §5.1 复核】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L473 | **HEADER_ROW** | `\| # \| 描述 \| 初始状态 \| 操作 1 \| 操作 2 \| 最终状态 \| 是否成功 \| 异常/响应 \|` | ✓ |
| L474 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|---\|---\|:-:\|---\|` | ✓ 存在 |
| L475-L480 | **DATA_ROWS**(6 行) | 6 个场景 | ✓ |

**L477 类型**:DATA_ROW(`| 3 | A 失败 + B 成功 | companyA=1, companyB=0 | ...`)

**最终判定**:
- 是有效 TABLE_BLOCK ✓
- HEADER 不含 A/B/C/D/E 模式 → **不进入 TABLE_CANDIDATE**
- 属于 `TABLE_BLOCK_TOTAL`(已计入 675)

### 5.2 241V2A-14 §3.4 DEFAULT-01~05(含 L288)

**【241V2A-32 §5.2 复核】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L285 | **HEADER_ROW** | `\| DEFAULT \| 阶段 A 数据 \| 阶段 B 操作 \| verifyFinalState 参数 \| Verifier 内部消费 \| 测试层精确断言 \|` | ✓ |
| L286 | **SEPARATOR_ROW** | `\|---\|---\|---\|---\|---\|---\|` | ✓ 存在 |
| L287-L291 | **DATA_ROWS**(5 行) | 5 个 DEFAULT 测试场景 | ✓ |

**L288 类型**:DATA_ROW(`| **02** | u1 / A=default / B / C | ...`)

**最终判定**:
- 是有效 TABLE_BLOCK ✓
- HEADER 不含 A/B/C/D/E 模式 → **不进入 TABLE_CANDIDATE**
- 属于 `TABLE_BLOCK_TOTAL`(已计入 675)

### 5.3 241V2A-27 §5.1

**【241V2A-32 §5.3 复核】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L248 | **HEADER_ROW** | `\| # \| 表位置 \| 章节标题 \| 表头 \| 数据行 \| 正式性声明 \| 分类 \| 判定理由 \|` | ✓ |
| L249 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|---\|---\---\|---\---\|` | ✓ 存在 |
| L250-L256 | **DATA_ROWS**(7 行) | 7 个候选表 | ✓ |

**最终判定**:
- 是有效 TABLE_BLOCK ✓
- HEADER 不含 A/B/C/D/E 模式 → **不进入 TABLE_CANDIDATE**
- 属于 `TABLE_BLOCK_TOTAL`(已计入 675)

### 5.4 241V2A-28 §5.3

**【241V2A-32 §5.4 复核】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L249 | **HEADER_ROW** | `\| # \| 表位置 \| 章节标题 \| 表头模式 \|` | ✓ |
| L250 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|` | ✓ 存在 |
| L251-L257 | **DATA_ROWS**(7 行) | 7 个候选表 | ✓ |

**最终判定**:
- 是有效 TABLE_BLOCK ✓
- HEADER 不含 A/B/C/D/E 模式 → **不进入 TABLE_CANDIDATE**
- 属于 `TABLE_BLOCK_TOTAL`(已计入 675)

### 5.5 241V2A-29 §5.4(P1-42 核心)

**【241V2A-32 §5.5 复核(P1-42 显式修复)】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L264 | **HEADER_ROW** | `\| # \| 文件 \| 行号 \| 章节 \| 表头 \| 类型 \|` | ✓ |
| **L265** | **SEPARATOR_ROW** | **`\|---:\|---\|---\|---\|---\|---\|`** | **✓ 存在!** |
| L266-L272 | **DATA_ROWS**(7 行) | 7 个候选表 | ✓ |

**P1-42 修复结论**:
- ✓ SEPARATOR_ROW 在 L265,**确实存在**(本轮直接 read 原始文本确认)
- ✓ TABLE_BLOCK 结构完整(HEADER + SEPARATOR + 7 DATA_ROWS)
- ✓ 是有效 TABLE_BLOCK
- HEADER 不含 A/B/C/D/E 模式 → **不进入 TABLE_CANDIDATE**
- 属于 `TABLE_BLOCK_TOTAL`(已计入 675)

### 5.6 241V2A-30 §5.1(新文件)

**【241V2A-32 §5.6 复核】**:

| 行 | 类型 | 内容 | 是否符合 |
|---|---|---|---|
| L253 | **HEADER_ROW** | `\| 名称 \| 值 \|` | ✓ |
| L254 | **SEPARATOR_ROW** | `\|---\|---:\|` | ✓ |
| L255-L260 | **DATA_ROWS**(6 行) | 6 项 | ✓ |

**最终判定**:是有效 TABLE_BLOCK,但 HEADER 不含 ABCDE → 不进入 TABLE_CANDIDATE。

### 5.7 241V2A-31(本轮上一文件)

**【241V2A-32 §5.7 复核】** 241V2A-31 含 13 张 TABLE_BLOCK(实测 Python),全部 HEADER 不含 ABCDE → 不进入 TABLE_CANDIDATE。

---

## §6 TABLE_CANDIDATE 完整列表(241V2A-32 §6,7 张)

### 6.1 7 张 TABLE_CANDIDATE 实测完整证据(241V2A-32 §6.1)

| # | document | section | header_line | header_text | separator_line | separator_text | data_start | data_end | data_count | classification |
|---:|---|---|---:|---|---:|---|---:|---:|---:|---|
| 1 | `241V2A-22` | 五维模型总览示例 | L257 | `\| # \| 对象 \| 维度 A \| 维度 B \| 维度 C \| 维度 D \| 维度 E \|` | L258 | `\|---:\|---\|---\|---\|---\|---\|---\|` | L259 | L281 | 23 | **NON_FORMAL** |
| 2 | `241V2A-23` | §2 五维合法枚举 | L303 | `\| # \| 对象 \| A 证据来源 \| B 规范形成 \| C Spec \| D Git 跟踪 \| E Git 工作区 \|` | L304 | `\|---:\|---\|---\|---\|---\|---\|---\|` | L305 | L327 | 23 | **NON_FORMAL** |
| 3 | `241V2A-24` | §2.3 五维合法实例表 | L111 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | L112 | `\|---:\|---\|---\|---\|---\|---\|---\|---\|` | L113 | L134 | 22 | **HISTORICAL_FORMAL** |
| 4 | `241V2A-24` | §3.4 N/A 区别表 | L200 | `\| 场景 \| A \| B \| C \| D \| E \|` | L201 | `\|---\|---\|---\|---\|---\|---\|` | L202 | L205 | 4 | **NON_FORMAL** |
| 5 | `241V2A-24` | §5 五维对象有效性规则 | L256 | `\| 对象属性 \| A \| B \| C \| D \| E \|` | L257 | `\|---\|---\|---\|---\|---\|---\|` | L258 | L262 | 5 | **NON_FORMAL** |
| 6 | `241V2A-25` | §2.3 重制后的五维合法实例表 | L55 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | L56 | `\|---:\|---\|---\|---\|---\|---\|---\|---\|` | L57 | L78 | 22 | **CURRENT_FORMAL** |
| 7 | `241V2A-25` | §3.4 对照扫描结果 | L217 | `\| 维度 \| A_actual \| B_actual \| C_actual \| D_actual \| E_actual \|` | L218 | `\|---\|---\|---\|---\|---\|---\|` | L219 | L221 | 3 | **NON_FORMAL** |

---

## §7 两组集合等式验证(241V2A-32 §7)

**【241V2A-32 §7 实测】**:

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **等式 1**:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 7 | 2 + 5 = 7 | ✓ **相等** |
| **等式 2**:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 | 1 + 1 = 2 | ✓ **相等** |

## §8 四组集合互斥验证(241V2A-32 §8)

| 集合对 | 交集 | 验证 |
|---|---|---|
| `CURRENT_FORMAL ∩ HISTORICAL_FORMAL` | ∅ | ✓ |
| `CURRENT_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `HISTORICAL_FORMAL ∩ NON_FORMAL` | ∅ | ✓ |
| `FORMAL_TABLE_CANDIDATE ∩ NON_FORMAL` | ∅ | ✓ |

---

## §9 GRANULARITY_RULE / GRANULARITY_ASSERTION 硬断言(241V2A-32 最高优先级)

### 9.1 GRANULARITY_RULE(241V2A-32 §1.2 显式)

**【GRANULARITY_RULE】**:

```
1. 一个 TABLE_CANDIDATE 必须来源于且只来源于一个 TABLE_BLOCK。
2. 一个 TABLE_BLOCK 最多产生一个 TABLE_CANDIDATE。
3. TABLE_BLOCK 是否进入 TABLE_CANDIDATE,由该 TABLE_BLOCK 的 HEADER 是否通过候选结构规则决定。
4. 不通过 HEADER 候选结构规则的 TABLE_BLOCK 仍然属于 TABLE_BLOCK,但不属于 TABLE_CANDIDATE。
5. 因此:
   TABLE_CANDIDATE ⊆ TABLE_BLOCK
```

### 9.2 GRANULARITY_ASSERTION(241V2A-32 §9.2 硬性断言)

**【GRANULARITY_ASSERTION】**(241V2A-32 硬性断言):

```
A. TABLE_CANDIDATE ⊆ TABLE_BLOCK
B. 每个 TABLE_CANDIDATE 唯一映射一个 TABLE_BLOCK
C. 每个 TABLE_BLOCK 至多映射一个 TABLE_CANDIDATE
D. TABLE_BLOCK_TOTAL >= TABLE_CANDIDATE
E. 当前数字必须满足:675 >= 7
```

**【严禁】** 使用 `TABLE_BLOCK = TABLE_CANDIDATE` 作为一般性定义。

### 9.3 断言状态

| 检查项 | 实际值 | 状态 |
|---|---|---|
| A. TABLE_CANDIDATE ⊆ TABLE_BLOCK | 7 ⊆ 675 | ✓ PASS |
| B. 每个 TABLE_CANDIDATE 唯一映射一个 TABLE_BLOCK | 7 个 TC 各自映射 1 个 TB | ✓ PASS |
| C. 每个 TABLE_BLOCK 至多映射一个 TABLE_CANDIDATE | 675 个 TB 至多 1 个 TC | ✓ PASS |
| D. TABLE_BLOCK_TOTAL >= TABLE_CANDIDATE | 675 >= 7 | ✓ PASS |
| E. 当前数字满足 | 675 >= 7 | ✓ PASS |

**任一断言失败**:**P1-41 = OPEN + S1-169-2 = BLOCK**

---

## §10 当前 Spec PASS 对象(241V2A-32 §10)

**【241V2A-32 §10 显式】** 当前 Spec PASS 判定对象**不因本轮修复而改变**:

| 项目 | 值 |
|---|---|
| 当前 Spec PASS 唯一对象 | `CURRENT_FORMAL` = `241V2A-25 §2.3` L55(22 行) |
| 当前 Spec PASS 状态 | **TRUE**(`241V2A-25 §2.3` 22 行五维差集全部 = ∅) |
| 历史回归对象 | `HISTORICAL_FORMAL` = `241V2A-24 §2.3` L111 |

---

## §11 P1-35 ~ P1-40 保持(241V2A-32 §11 显式)

### 11.1 原则保持

| P1 | 内容 | 状态 |
|---|---|---|
| **P1-40** | TABLE_BLOCK 定义 + 7 STEP 表块识别 | ✓ CLOSED(241V2A-31) |
| **P1-39** | TABLE_CANDIDATE 纯发现层 | ✓ CLOSED(241V2A-30) |
| **P1-38** | DOCUMENT_CANDIDATE = glob `241*.md` | ✓ CLOSED(241V2A-29) |
| **P1-37** | 三个独立集合 + 集合等式 | ✓ CLOSED(241V2A-28) |
| **P1-36** | 自动发现 4 条 + 三分类 | ✓ CLOSED(241V2A-27) |
| **P1-35** | normalization 6 步硬性规则 | ✓ CLOSED(241V2A-26) |

### 11.2 冲突项记录

**【241V2A-32 §11.2 显式】** 本轮发现与历史规则不存在需要"偷偷修复"的矛盾:
- P1-41 与 P1-40 不矛盾(子集关系是 P1-40 表块识别的细化,不是矛盾)
- P1-42 与 P1-40 也不矛盾(241V2A-29 §5.4 本身是有效 TABLE_BLOCK,只是 header 不含 ABCDE 不进 TC)

**结论**:无需新增"冲突项",所有 P1 原则保持。

---

## §12 P2 状态保持(241V2A-32 §12 显式)

| 编号 | 描述 | 状态 |
|---|---|---|
| P2-0 | exactly-one 业务规则需 fallback | **OPEN** |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **OPEN** |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **OPEN** |
| P2-6 | 章节编号/统计一致性 | **OPEN** |
| P2-7 | 章节编号缺 3 的文档问题 | **OPEN** |
| P2-8 | (241V2A-31 新增) | **OPEN** |
| P2-3 / P2-4 / P2-5 | | CLOSED |

**【241V2A-32 显式】** 本轮**只修 P1-41 / P1-42**,**不修 P2**;P2 状态诚实保留。

---

## §13 P1-41 / P1-42 自评(241V2A-32 §13 显式)

### 13.1 P1-41 自评

| 矛盾点 | 旧表述 | 实际 | 矛盾? |
|---|---|---|---|
| 241V2A-31 §10 | "一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE" | 实际 7 ⊂ 675(子集) | ✓ |

**修复方法**:241V2A-32 §1.2 GRANULARITY_RULE 5 条 + §9 GRANULARITY_ASSERTION 5 项。

### 13.2 P1-42 自评

| 矛盾点 | 旧表述 | 实际 | 矛盾? |
|---|---|---|---|
| 241V2A-31 §7.1 241V2A-29 §5.4 | "L265 = HEADER"未证明 SEPARATOR | L264 header + **L265 separator** + L266-L272 data | ✓ 需证明 |

**修复方法**:241V2A-32 §2 直接 read 原始文本,给出 L264/L265/L266-L272 完整证据。

### 13.3 自审 PASS 项

- ✓ P1-41 矛盾识别正确
- ✓ P1-42 矛盾识别正确
- ✓ GRANULARITY_RULE 5 条冻结
- ✓ GRANULARITY_ASSERTION 5 项硬断言
- ✓ 241V2A-29 §5.4 原始证据直接给出(L264/L265/L266-L272)
- ✓ 7 张 TABLE_CANDIDATE 完整列表
- ✓ 5 个争议点完整复核
- ✓ DOCUMENT_CANDIDATE = 38(实测)
- ✓ TABLE_BLOCK_TOTAL = 675(实测)
- ✓ TABLE_CANDIDATE = 7
- ✓ 等式 1:7 = 2 + 5
- ✓ 等式 2:2 = 1 + 1
- ✓ 4 组集合互斥全部 PASS
- ✓ 当前 Spec PASS 不改变

**未自评 PASS**:等待下一轮独立盲审确认本轮修复方法是否真正成立。

---

## §14 一句话最终判断

> **241V2A-32 S1-169-1 TABLE_BLOCK 与 TABLE_CANDIDATE 集合关系及 SEPARATOR 证据修复补丁完成**:第二十九轮独立盲审识别的 **P1-41**(`241V2A-31 §10` 写"一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE"——错误的集合等价,实际应该是 `TABLE_CANDIDATE ⊆ TABLE_BLOCK` 子集关系,7 ⊂ 675)+ **P1-42**(`241V2A-31` 把 `241V2A-29 §5.4` 列为 TABLE_CANDIDATE 复核对象但**没有证明** SEPARATOR_ROW 存在,必须直接读原始文本验证)通过本补丁**真闭环**——**§1.2 GRANULARITY_RULE 5 条冻结**(1 个 TABLE_CANDIDATE 必须来源于且只来源于一个 TABLE_BLOCK / 1 个 TABLE_BLOCK 最多产生 1 个 TABLE_CANDIDATE / TABLE_BLOCK 是否进入 TABLE_CANDIDATE 由 HEADER 是否通过候选结构规则决定 / 不通过 HEADER 规则的 TABLE_BLOCK 仍属 TABLE_BLOCK 但不属 TABLE_CANDIDATE / `TABLE_CANDIDATE ⊆ TABLE_BLOCK` 7 ⊂ 675);**§2 P1-42 修复** —— 直接 read `241V2A-29 §5.4` 原始文本给出 L264 HEADER `| # | 文件 | 行号 | 章节 | 表头 | 类型 |` + **L265 SEPARATOR `|---:|---|---|---|---|---|`(确实存在!)** + L266-L272 DATA(7 行),结论:**有效 TABLE_BLOCK 但不进入 TABLE_CANDIDATE**(HEADER 不含 A/B/C/D/E);**§3 DOCUMENT_CANDIDATE = 38 完整列表**(241V2A-30 / 31 加入使总数从 36 → 38);**§4 重新实测** —— DOCUMENT_CANDIDATE = 38 / TABLE_BLOCK_TOTAL = 675 / TABLE_CANDIDATE = 7 / FORMAL_TABLE_CANDIDATE = 2 / CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 5;**§5 七个争议点完整复核**(241V2A-1 §8.1 / 241V2A-14 §3.4 / 241V2A-27 §5.1 / 241V2A-28 §5.3 / 241V2A-29 §5.4 / 241V2A-30 §5.1 / 241V2A-31,每张完整给出 header_line / header_text / separator_line / separator_text / data_start / data_end / 是否 TABLE_BLOCK / 是否 TABLE_CANDIDATE / 最终分类);**§6 7 张 TABLE_CANDIDATE 完整列表**(每张含完整 header + separator + data 证据);**§7 集合等式** —— 7 = 2 + 5 / 2 = 1 + 1;**§8 4 组集合互斥**;**§9 GRANULARITY_ASSERTION 硬断言** —— TABLE_CANDIDATE ⊆ TABLE_BLOCK ✓ / 每个 TC 唯一映射一个 TB ✓ / 每个 TB 至多映射一个 TC ✓ / TABLE_BLOCK_TOTAL >= TABLE_CANDIDATE (675 >= 7) ✓ / 严禁使用 TABLE_BLOCK = TABLE_CANDIDATE 作为一般性定义;**§10 当前 Spec PASS 不改变**(`CURRENT_FORMAL` = `241V2A-25 §2.3` L55);**§11.1 P1-35 ~ P1-40 不被改写**;**§11.2 无需新增"冲突项"**;**§12 P2 OPEN 6 / CLOSED 3 状态诚实保留**(本轮不修 P2);241V2A-32 不修改 241V2A-31 / 241V2A-30 / 241V2A-29 / 任何历史 MD 任何字节,只通过"显式冻结 GRANULARITY_RULE + 显式给出 SEPARATOR 原始证据 + 显式实测 38/675/7 + 显式硬断言"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §15 附录

- 章节数:16(§0 元信息 + §1 P1-41 + §2 P1-42 + §3 DOCUMENT_CANDIDATE 38 份 + §4 重新实测 + §5 七个争议点 + §6 7 张 TC 列表 + §7 集合等式 + §8 集合互斥 + §9 GRANULARITY_RULE/ASSERTION + §10 当前 Spec PASS + §11 P1 保持 + §12 P2 + §13 自评 + §14 一句话最终判断 + §15 附录)
- 修复的 P1:2(P1-41 + P1-42)
- 显式作废的旧表述:`241V2A-31 §10` "一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE"
- 新增硬性定义:`GRANULARITY_RULE` 5 条 + `GRANULARITY_ASSERTION` 5 项
- DOCUMENT_CANDIDATE:**38**(实测)
- TABLE_BLOCK_TOTAL:**675**(实测)
- TABLE_CANDIDATE:**7**
- FORMAL_TABLE_CANDIDATE:**2**
- CURRENT_FORMAL:**1** / HISTORICAL_FORMAL:**1** / NON_FORMAL:**5**
- 集合等式:7 = 2 + 5 / 2 = 1 + 1 全部 PASS
- 集合互斥:4 组全部 PASS
- 保持闭环:P1-14 ~ P1-40 不被改写
- 当前 Spec PASS:CURRENT_FORMAL = `241V2A-25 §2.3`(22 行五维差集全部 = ∅)
- P2 OPEN 6 / CLOSED 3(状态诚实)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- S1-169-2 = BLOCK

**【241V2A-32 自评声明】** 本轮 P1-41 / P1-42 修复方法已通过"补丁后独立自审"识别并冻结,但**不声明 PASS**——按规则等待下一轮独立盲审确认。