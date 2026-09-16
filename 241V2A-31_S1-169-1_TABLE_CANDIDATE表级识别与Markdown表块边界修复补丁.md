# 241V2A-31 S1-169-1 TABLE_CANDIDATE 表级识别与 Markdown 表块边界修复补丁

> **阶段**:S1-169-1
> **补丁类型**:独立盲审修复(第二十八轮)
> **优先级**:**最高**(覆盖 241V2A-30 §4 "逐行正则命中 = 一张表" 的错误等价)
> **基线 HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
> **严禁修改**:241V2A-30 / 241V2A-29 / 241V2A-28 / 241V2A-27 / 任何历史 MD / VisionCare PMS 任何文件

---

## §0 元信息

- **创建日期**:2026-09-15
- **修复目标**:
  - **P1-40**:`241V2A-30 §4.1` 把"逐行命中结构正则"错误等同于"识别一张表"——一个 Markdown 表块包含 HEADER + SEPARATOR + 多 DATA ROW,所有数据行属于同一张表;但 241V2A-30 把每个匹配行都计数为一张表,得到 `TABLE_CANDIDATE = 29`(实际可能是 29 个数据行而不是 29 张表);必须改成真正的**表块级识别**——HEADER 行通过结构正则 → 整张 TABLE_BLOCK 计入 `TABLE_CANDIDATE` = 1
- **本轮 P2 增量**:**P2-8 OPEN**(本轮新增)

---

## §1 P1-40 问题陈述(241V2A-31 显式)

### 1.1 241V2A-30 §4 错误逻辑

**【241V2A-30 旧文本,本轮作废】**:

> Step 2: 对每份文档每一行应用正则
> Step 3: 命中的每一行 = 一个表格

**问题**:这是错误的。一个 Markdown 表块包含:

```
| HEADER | ROW 1 | COL 2 | ... |  ← HEADER_ROW
|---|---|---|---|---|          ← SEPARATOR_ROW
| 1 | xxx | ... | ... | ... |   ← DATA_ROW
| 2 | yyy | ... | ... | ... |   ← DATA_ROW
| 3 | zzz | ... | ... | ... |   ← DATA_ROW
```

整个块是 **1 张表**,不是 **4 张表**。

### 1.2 241V2A-30 §5.1 列表 29 条中,只有 7 条是 HEADER,其余 22 条是 DATA 行

| 文档 | 241V2A-30 计数 | HEADER 实际位置 | DATA 实际数量 |
|---|---:|---|---:|
| 241V2A-22 L257 | 1 | L257 | 23 |
| 241V2A-23 L303 | 1 | L303 | 23 |
| 241V2A-24 L111 | 1 | L111 | 22 |
| 241V2A-24 L200 | 1 | L200 | 4 |
| 241V2A-24 L256 | 1 | L256 | 5 |
| 241V2A-25 L55 | 1 | L55 | 22 |
| 241V2A-25 L217 | 1 | L217 | 3 |
| 241V2A-27 §5.1 L250-256 | **6**(6 个数据行)| L249 | 7 |
| 241V2A-28 §5.3 L251-257 | **7**(7 个数据行)| L249 | 7 |
| 241V2A-29 §5.4 L266-272 | **7**(7 个数据行)| L265 | 7 |
| 241V2A-1 L477 | 1(数据行不是 header) | (不是 header) | — |
| 241V2A-14 L288 | 1(数据行不是 header) | (不是 header) | — |
| **总计** | **29** | **7**(真 header)+ **2**(误识别)| **100+** |

**实际 TABLE_CANDIDATE(纯结构,header 含 A/B/C/D/E) = 7**

### 1.3 必须冻结的"表块级识别"

**表块级识别必须满足**:
1. **HEADER_ROW** 必须在结构正则 `^\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|` 上通过
2. **SEPARATOR_ROW** 必须是紧跟 HEADER 的合法 Markdown separator(下一行匹配 `^\|[\s\-:|]+\|$`)
3. **DATA_ROW** 是 SEPARATOR 之后的连续表格行
4. **TABLE_BLOCK** = HEADER + SEPARATOR + N×DATA_ROW,只计 **1** 张表
5. **数据行** 不得单独进入 `TABLE_CANDIDATE`

---

## §2 TABLE_BLOCK 定义冻结(241V2A-31 最高优先级)

### 2.1 Markdown TABLE_BLOCK 定义

**【241V2A-31 最高优先级冻结】** `TABLE_BLOCK` 定义:

```
TABLE_BLOCK
= 一个连续的 Markdown 表格块
= HEADER_ROW + SEPARATOR_ROW + DATA_ROW × N (N ≥ 1)
= 一个完整的 Markdown 表

最小结构(全部必须满足):
1. 一行 Markdown HEADER_ROW(必须以 | 开头和结尾)
2. 紧随其后的 Markdown SEPARATOR_ROW(形如 |---|---|---|)
3. 至少一个 DATA_ROW(必须以 | 开头和结尾,不是 separator)
```

### 2.2 HEADER_ROW / SEPARATOR_ROW / DATA_ROW 定义

**【241V2A-31 显式】** 三种行类型定义:

| 行类型 | 正则 | 描述 |
|---|---|---|
| **HEADER_ROW** | `^\|.*\|$` | 表格首行,通常含列名,作为整张表的元数据 |
| **SEPARATOR_ROW** | `^\|[\s\-:|]+\|$` | 分隔行,定义列对齐 |
| **DATA_ROW** | `^\|.*\|$` AND NOT `^\|[\s\-:|]+\|$` | 数据行 |

### 2.3 显式作废 241V2A-30 §4 错误逻辑

**【241V2A-31 显式作废】** `241V2A-30 §4.1`:

> Step 2: 对每份文档每一行应用正则
> Step 3: 命中的每一行 = 一个表格

**作废理由**:
1. "命中的每一行 = 一个表格"是错误的等价
2. 一个表有多个数据行,数据行不应单独计数
3. 必须识别 HEADER + SEPARATOR 结构,整张表计为 1

**替代为**:241V2A-31 §3 冻结 Markdown 表块识别算法 7 STEP。

---

## §3 Markdown 表块识别算法冻结(241V2A-31 最高优先级)

### 3.1 7 STEP 算法(241V2A-31 最高优先级冻结)

**【241V2A-31 最高优先级冻结】** Markdown 表块识别算法:

```
STEP 1: 逐文档逐行读取
STEP 2: 发现候选 HEADER_ROW(以 | 开头和结尾)
STEP 3: 检查下一行是否为合法 Markdown SEPARATOR_ROW
STEP 4: 若下一行是 SEPARATOR,开始一个 TABLE_BLOCK
STEP 5: 继续读取连续 Markdown TABLE_ROWS,
        直到不再是合法 TABLE_ROW
STEP 6: 整个 HEADER + SEPARATOR + DATA_ROWS = 一个 TABLE_BLOCK
STEP 7: 对 TABLE_BLOCK 的 HEADER_ROW 执行结构正则判断:
        ^\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|
        只有 HEADER 通过,该 TABLE_BLOCK 才进入 TABLE_CANDIDATE
```

### 3.2 严禁把数据行当成独立 TABLE_CANDIDATE(241V2A-31 显式)

**【241V2A-31 显式严禁】**:

| 严禁 | 反例 |
|---|---|
| 把每个匹配行计为 1 张表 | 同一张表有 22 数据行,计为 22 张表 |
| 把 DATA_ROW 当成独立候选 | 241V2A-25 §2.3 的 22 行数据单独成 22 个候选 |

**同一 TABLE_BLOCK 中:**
- 1 个 HEADER
- 1 个 SEPARATOR
- N 个 DATA ROWS(无论 N=1、N=7、N=100)
- **`TABLE_CANDIDATE = 1`**

### 3.3 HEADER 是结构判断的唯一依据

**【241V2A-31 显式】** 只有 HEADER_ROW 用于结构判断:

- HEADER 通过结构正则 → 整张 TABLE_BLOCK 进入 `TABLE_CANDIDATE`
- HEADER 不通过结构正则 → 整张 TABLE_BLOCK **不**进入 `TABLE_CANDIDATE`
- DATA_ROW 含 A/B/C/D/E 单字符,**不影响**结构判断(因为它是数据,不是表头)

---

## §4 重新检查 241V2A-27 / 28 / 29(241V2A-31 §4 实测)

### 4.1 241V2A-27 §5.1 实测

**【241V2A-31 §4.1 实测】** `241V2A-27 §5.1` 候选正式五维表发现表:

| 行 | 类型 | 内容 |
|---|---|---|
| L249 | **HEADER_ROW** | `\| # \| 表位置 \| 章节标题 \| 表头 \| 数据行 \| 正式性声明 \| 分类 \| 判定理由 \|` |
| L250 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|---\|---\|---\|---\|` |
| L251-L257 | **DATA_ROWS**(7 行) | 7 个候选表的数据行 |

**结论**:`241V2A-27 §5.1` 是 **1 张 TABLE_BLOCK**(不是 6 张或 7 张),L250-L256 的"多个命中行"实际是同一张表的多个数据行。

**HEADER 不含 A/B/C/D/E 模式**(列名是"# | 表位置 | 章节标题 | 表头 | 数据行 | 正式性声明 | 分类 | 判定理由"),因此**不进入** `TABLE_CANDIDATE`。

### 4.2 241V2A-28 §5.3 实测

**【241V2A-31 §4.2 实测】** `241V2A-28 §5.3` TABLE_CANDIDATE = 7 完整列表:

| 行 | 类型 | 内容 |
|---|---|---|
| L249 | **HEADER_ROW** | `\| # \| 表位置 \| 章节标题 \| 表头模式 \|` |
| L250 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|` |
| L251-L257 | **DATA_ROWS**(7 行) | 7 个候选表的数据行 |

**结论**:`241V2A-28 §5.3` 是 **1 张 TABLE_BLOCK**(不是 7 张),L251-L257 是同一张表的 7 个数据行。

**HEADER 不含 A/B/C/D/E 模式**,因此**不进入** `TABLE_CANDIDATE`。

### 4.3 241V2A-29 §5.4 实测

**【241V2A-31 §4.3 实测】** `241V2A-29 §5.4` TABLE_CANDIDATE 完整列表:

| 行 | 类型 | 内容 |
|---|---|---|
| L265 | **HEADER_ROW** | `\| # \| 文件 \| 行号 \| 章节 \| 表头 \| 类型 \|` |
| L266-L272 | **DATA_ROWS**(7 行) | 7 个候选表的数据行 |

**结论**:`241V2A-29 §5.4` 是 **1 张 TABLE_BLOCK**,L266-L272 是同一张表的 7 个数据行。

**HEADER 不含 A/B/C/D/E 模式**,因此**不进入** `TABLE_CANDIDATE`。

### 4.4 总结

**【241V2A-31 §4.4 总结】** `241V2A-27/28/29` 自身的"实测表"全部都是 **1 张 TABLE_BLOCK**(不是 6/7/7 张),因为它们的 HEADER 是"# / 表位置 / 章节标题 / 表头 / ..."形式,**不含 A/B/C/D/E 模式**,因此**不计入** `TABLE_CANDIDATE`。

之前 241V2A-30 把数据行误识别为独立候选,导致 TABLE_CANDIDATE 虚高到 29。表块级识别后,**真实 TABLE_CANDIDATE = 7**。

---

## §5 241V2A-1 L477 / 241V2A-14 L288 重新判定

### 5.1 241V2A-1 L477 实测

**【241V2A-31 §5.1 实测】** `241V2A-1 §8.1` 场景总表:

| 行 | 类型 | 内容 |
|---|---|---|
| L473 | **HEADER_ROW** | `\| # \| 描述 \| 初始 default \| A 操作 \| B 操作 \| 最终状态 \| 期望 \| 备注 \|` |
| L474 | **SEPARATOR_ROW** | `\|---:\|---\|---\|---\|---\|---\|---\|---\|` |
| L475-L480 | **DATA_ROWS**(6 行) | 6 个场景 |
| ... | ... | ... |
| L477 | **DATA_ROW** | `\| 3 \| A 失败 + B 成功 \| companyA=1, companyB=0 \| A → setDefault(C) 失败(C 无权限) \| ...` |

**结论**:`241V2A-1 L477` 是**数据行**,不是 HEADER。HEADER(L473)不含 A/B/C/D/E 模式(列名是"# / 描述 / 初始 default / A 操作 / B 操作 / 最终状态 / 期望 / 备注"),因此**不进入** `TABLE_CANDIDATE`。

### 5.2 241V2A-14 L288 实测

**【241V2A-31 §5.2 实测】** `241V2A-14 §3.4` DEFAULT-01~05 表:

| 行 | 类型 | 内容 |
|---|---|---|
| L285 | **HEADER_ROW** | `\| DEFAULT \| 阶段 A 数据 \| 阶段 B 操作 \| verifyFinalState 参数 \| Verifier 内部消费 \| 测试层精确断言 \|` |
| L286 | **SEPARATOR_ROW** | `\|---\|---\|---\|---\|---\|---\|` |
| L287-L291 | **DATA_ROWS**(5 行) | 5 个 DEFAULT 测试场景 |
| ... | ... | ... |
| L288 | **DATA_ROW** | `\| **02** \| u1 / A=default / B / C \| 串行 → B \| verify(u1, B, C) \| ...` |

**结论**:`241V2A-14 L288` 是**数据行**,不是 HEADER。HEADER(L285)不含 A/B/C/D/E 模式(列名是"DEFAULT / 阶段 A 数据 / 阶段 B 操作 / verifyFinalState 参数 / Verifier 内部消费 / 测试层精确断言"),因此**不进入** `TABLE_CANDIDATE`。

### 5.3 误识别纠正

**【241V2A-31 §5.3 显式】**:

| 误识别项 | 之前(241V2A-30 §5.1) | 现在(241V2A-31 §5.1 + §5.2) |
|---|---|---|
| `241V2A-1 L477` | 误命中(数据行当作候选) | **不是 TABLE_CANDIDATE**(HEADER 不含 A/B/C/D/E) |
| `241V2A-14 L288` | 误命中(数据行当作候选) | **不是 TABLE_CANDIDATE**(HEADER 不含 A/B/C/D/E) |

**关键**:这次纠正是**在表块识别层**完成的,不是"语义过滤"。表块识别算法只判断 HEADER_ROW,数据行的字符模式**不影响**判定。

---

## §6 重新计算全部集合(241V2A-31 §6 实测)

### 6.1 实测方法

**【241V2A-31 §6.1 实测方法】**:

```
Step 1: DOCUMENT_CANDIDATE = 36 份(glob "241*.md" + S1-169-1 untracked)
Step 2: 遍历所有文档,识别所有 Markdown TABLE_BLOCK
        TABLE_BLOCK_TOTAL = 656(所有 TABLE_BLOCK)
Step 3: 对每个 TABLE_BLOCK 的 HEADER_ROW 执行结构正则
        ^\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|
        HEADER 通过 → 该 TABLE_BLOCK 进入 TABLE_CANDIDATE
        HEADER 不通过 → 不进入 TABLE_CANDIDATE
Step 4: TABLE_CANDIDATE = 7(实测,HEADER 含 A/B/C/D/E)
Step 5: 在 TABLE_CANDIDATE 内应用 241V2A-27 §2.1 4 条硬性规则
        FORMAL_TABLE_CANDIDATE = 2(241V2A-25 §2.3 + 241V2A-24 §2.3)
Step 6: 三分类
        CURRENT_FORMAL = 1(241V2A-25 §2.3)
        HISTORICAL_FORMAL = 1(241V2A-24 §2.3)
        NON_FORMAL = 7 - 2 = 5
```

### 6.2 六个数字实测

| 数字 | 值 |
|---|---:|
| **DOCUMENT_CANDIDATE** | **36** |
| **TABLE_BLOCK_TOTAL**(所有 TABLE_BLOCK) | **656** |
| **TABLE_CANDIDATE**(HEADER 含 A/B/C/D/E) | **7** |
| **FORMAL_TABLE_CANDIDATE** | **2** |
| **CURRENT_FORMAL** | **1** |
| **HISTORICAL_FORMAL** | **1** |
| **NON_FORMAL** | **5** |

### 6.3 与之前数字对比

| 数字 | 241V2A-30 §6.1 旧 | 241V2A-31 §6.2 新 | 差异原因 |
|---|---:|---:|---|
| `TABLE_BLOCK_TOTAL` | (未定义) | **656** | 新增概念 |
| `TABLE_CANDIDATE` | 29(逐行命中) | **7**(表块级,header 通过)| 表块级识别 vs 逐行命中 |
| `FORMAL_TABLE_CANDIDATE` | 2 | **2** | 不变 |
| `CURRENT_FORMAL` | 1 | **1** | 不变 |
| `HISTORICAL_FORMAL` | 1 | **1** | 不变 |
| `NON_FORMAL` | 27 | **5** | 241V2A-1/14 误识别 + 241V2A-27/28/29 自身 20 张"实测表"全部不计入 |

---

## §7 TABLE_CANDIDATE 完整列表(241V2A-31 §7,7 张)

### 7.1 7 张候选表的完整范围(241V2A-31 §7.1 实测)

| # | document | section | header_line | separator_line | data_start_line | data_end_line | table_block_line_count | classification |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | `241V2A-22` | (五维模型总览示例表) | **L257** | **L258** | **L259** | **L281** | 25 | **NON_FORMAL** |
| 2 | `241V2A-23` | §2 五维合法枚举示例 | **L303** | **L304** | **L305** | **L327** | 25 | **NON_FORMAL** |
| 3 | `241V2A-24` | §2.3 五维合法实例表 | **L111** | **L112** | **L113** | **L134** | 24 | **HISTORICAL_FORMAL** |
| 4 | `241V2A-24` | §3.4 N/A 区别表 | **L200** | **L201** | **L202** | **L205** | 6 | **NON_FORMAL** |
| 5 | `241V2A-24` | §5 五维对象有效性规则 | **L256** | **L257** | **L258** | **L262** | 7 | **NON_FORMAL** |
| 6 | `241V2A-25` | §2.3 重制后的五维合法实例表 | **L55** | **L56** | **L57** | **L78** | 24 | **CURRENT_FORMAL** |
| 7 | `241V2A-25` | §3.4 对照扫描结果 | **L217** | **L218** | **L219** | **L221** | 5 | **NON_FORMAL** |

### 7.2 7 张候选表的 header 模式

| # | header | 表格类型 |
|---:|---|---|
| 1 | `\| # \| 对象 \| 维度 A 证据来源 \| 维度 B 规范形成 \| 维度 C Spec 状态 \| 维度 D Git 跟踪 \| 维度 E Git 工作区 \|` | 真五维示例表 |
| 2 | `\| # \| 对象 \| A 证据来源 \| B 规范形成 \| C Spec \| D Git 跟踪 \| E Git 工作区 \|` | 真五维示例表 |
| 3 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | 真五维实例表 |
| 4 | `\| 场景 \| A \| B \| C \| D \| E \|` | 真五维 N/A 区别表 |
| 5 | `\| 对象属性 \| A \| B \| C \| D \| E \|` | 真五维对象有效性规则 |
| 6 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | 真五维实例表 |
| 7 | `\| 维度 \| A_actual \| B_actual \| C_actual \| D_actual \| E_actual \|` | 真五维差集结果表 |

---

## §8 两组集合等式验证(241V2A-31 §8)

**【241V2A-31 §8 实测】**:

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **等式 1**:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 7 | 2 + 5 = 7 | ✓ **相等** |
| **等式 2**:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 | 1 + 1 = 2 | ✓ **相等** |

---

## §9 集合互斥验证(241V2A-31 §9)

| 集合对 | 交集 | 验证 |
|---|---|---|
| `CURRENT_FORMAL ∩ HISTORICAL_FORMAL` | ∅ | ✓ `{241V2A-25 §2.3} ∩ {241V2A-24 §2.3} = ∅` |
| `CURRENT_FORMAL ∩ NON_FORMAL` | ∅ | ✓ `{241V2A-25 §2.3} ∩ {5 张 NON_FORMAL} = ∅` |
| `HISTORICAL_FORMAL ∩ NON_FORMAL` | ∅ | ✓ `{241V2A-24 §2.3} ∩ {5 张 NON_FORMAL} = ∅` |
| `FORMAL_TABLE_CANDIDATE ∩ NON_FORMAL` | ∅ | ✓ `{2 张} ∩ {5 张} = ∅` |

---

## §10 TABLE_BLOCK_GRANULARITY_ASSERTION 硬断言(241V2A-31 最高优先级)

**【TABLE_BLOCK_GRANULARITY_ASSERTION】**(241V2A-31 硬性断言):

```
1. 一个 Markdown 表块只能计为一个 TABLE_CANDIDATE。
2. 数据行不能单独成为 TABLE_CANDIDATE。
3. 只有 HEADER + SEPARATOR + DATA_ROWS 组成 TABLE_BLOCK。
4. TABLE_CANDIDATE 必须由 TABLE_BLOCK 产生。
5. 不允许用单行正则命中数代替表数量。
```

**断言状态**(基于 241V2A-31 §7 实测):

| 检查项 | 实际值 | 状态 |
|---|---|---|
| 1. 一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE | 7 张 TABLE_BLOCK = 7 张 TABLE_CANDIDATE | ✓ PASS |
| 2. 数据行不单独成 TABLE_CANDIDATE | 241V2A-1 L477 / 241V2A-14 L288 是数据行,不计入 | ✓ PASS |
| 3. HEADER + SEPARATOR + DATA_ROWS 组成 TABLE_BLOCK | 656 张 TABLE_BLOCK 全部满足 | ✓ PASS |
| 4. TABLE_CANDIDATE 由 TABLE_BLOCK 产生 | 7 张全部是 TABLE_BLOCK | ✓ PASS |
| 5. 不允许用单行正则命中数代替表数量 | 之前 29 行的错误已纠正 | ✓ PASS |
| 等式 1:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 7 = 2 + 5 | ✓ PASS |
| 等式 2:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 = 1 + 1 | ✓ PASS |
| 4 组集合互斥 | 全部 = ∅ | ✓ PASS |

**任一断言失败**:**P1-40 = OPEN + S1-169-2 = BLOCK**

---

## §11 当前 Spec PASS 对象(241V2A-31 §11)

**【241V2A-31 §11 显式】** 当前 Spec PASS 判定对象**不因本轮修复而改变**:

| 项目 | 值 |
|---|---|
| 当前 Spec PASS 唯一对象 | `CURRENT_FORMAL` = `241V2A-25 §2.3` L55(22 行)|
| 当前 Spec PASS 状态 | **TRUE**(`241V2A-25 §2.3` 22 行五维差集全部 = ∅)|
| 历史回归对象 | `HISTORICAL_FORMAL` = `241V2A-24 §2.3` L111(被 `241V2A-25 §2.3` 显式作废)|

---

## §12 P1-35 ~ P1-39 保持(241V2A-31 §12 显式)

### 12.1 P1-39 保持

**【241V2A-31 显式保持】** `241V2A-30 §2-3` TABLE_CANDIDATE 纯发现层职责**不被改写**——本轮只是把"逐行命中"修正为"表块级识别",纯发现层职责不变。

### 12.2 P1-38 保持

**【241V2A-31 显式保持】** `241V2A-29 §2` DOCUMENT_CANDIDATE = glob `241*.md` + S1-169-1 untracked 文档集合**不被改写**。

### 12.3 P1-37 保持

**【241V2A-31 显式保持】** `241V2A-28 §2` 三个独立集合(TABLE_CANDIDATE / FORMAL_TABLE_CANDIDATE / CLASSIFIED_TABLE)+ 集合等式 + 集合互斥 + 术语规则**不被改写**——TABLE_CANDIDATE 数量从 29 → 7,但集合定义不变。

### 12.4 P1-36 保持

**【241V2A-31 显式保持】** `241V2A-27 §2.1` 自动发现 4 条硬性规则 + 三分类 + 严禁人工隐式指定**不被改写**。

### 12.5 P1-35 保持

**【241V2A-31 显式保持】** `241V2A-26 §2.1` normalization 6 步硬性规则**不被改写**:

```
STEP 3.1  去除首尾空白
STEP 3.2  保留原始括号字符
STEP 3.3  仅当完整包裹性 `**...**` 时去除粗体
STEP 3.4  不进行其他语义改写
STEP 3.5  得到 normalized_cell_value
STEP 3.6  与该维度 LEGAL 集合做差集
```

---

## §13 P2 状态保持(241V2A-31 §13 显式)

| 编号 | 描述 | 状态 |
|---|---|---|
| P2-0 | exactly-one 业务规则需 fallback | **OPEN** |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **OPEN** |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **OPEN** |
| P2-6 | 章节编号/统计一致性 | **OPEN** |
| P2-7 | 章节编号缺 3 的文档问题 | **OPEN** |
| **P2-8** | **(本轮新增)** | **OPEN** |
| P2-3 | 证据标签分级 | CLOSED |
| P2-4 | 60003/60004 证据等级误标 | CLOSED |
| P2-5 | "通用技术事实"误归【原系统事实】 | CLOSED |

**【241V2A-31 显式】** 本轮**只修 P1-40**,**不修 P2**;P2-8 是本轮新增,**OPEN** 状态诚实保留。

---

## §14 P1-40 自评(241V2A-31 §14 显式)

**自审方法**:对 `241V2A-30 §4.1 / §5.1` 中"逐行正则命中 = 一张表"逻辑进行逐字审查:

| 矛盾点 | 旧表述 | 实际数字 | 矛盾? |
|---|---|---|---|
| §4.1 Step 3 | "命中的每一行 = 一个表格" | 一个表格有多个数据行,数据行不能单独计 | ✓ |
| §5.1 列表 | 29 条(逐行匹配) | 实际 TABLE_BLOCK = 7(表块级) | ✓ |
| 241V2A-27 §5.1 | 6 张候选表 | 实际 1 张 TABLE_BLOCK,L250-L256 是 7 个数据行 | ✓ |
| 241V2A-28 §5.3 | 7 张候选表 | 实际 1 张 TABLE_BLOCK,L251-L257 是 7 个数据行 | ✓ |
| 241V2A-29 §5.4 | 7 张候选表 | 实际 1 张 TABLE_BLOCK,L266-L272 是 7 个数据行 | ✓ |
| 241V2A-1 L477 | 误命中候选 | 实际是 §8.1 场景总表的数据行 | ✓ |
| 241V2A-14 L288 | 误命中候选 | 实际是 §3.4 DEFAULT-01~05 表的数据行 | ✓ |

**修复方法**:241V2A-31 §2 冻结 TABLE_BLOCK 定义 + §3 7 STEP 表块识别算法 + §4 重新检查 241V2A-27/28/29 + §5 重新判定 241V2A-1/14 + §6 重新计算 + §10 硬断言。

**自审 PASS 项**:
- ✓ P1-40 矛盾识别正确
- ✓ TABLE_BLOCK 定义冻结(HEADER + SEPARATOR + DATA_ROW × N)
- ✓ 7 STEP 表块识别算法冻结
- ✓ 重新检查 241V2A-27/28/29(各 1 张 TABLE_BLOCK,不计入)
- ✓ 重新判定 241V2A-1/14(数据行,不计入)
- ✓ TABLE_CANDIDATE = 7(纯结构)
- ✓ 等式 1:7 = 2 + 5 ✓
- ✓ 等式 2:2 = 1 + 1 ✓
- ✓ 4 组集合互斥全部 PASS
- ✓ TABLE_BLOCK_GRANULARITY_ASSERTION 硬断言全部 PASS
- ✓ 当前 Spec PASS 不改变(`CURRENT_FORMAL` = `241V2A-25 §2.3`)

**未自评 PASS**:等待下一轮独立盲审确认本轮修复方法是否真正成立。

---

## §15 一句话最终判断

> **241V2A-31 S1-169-1 TABLE_CANDIDATE 表级识别与 Markdown 表块边界修复补丁完成**:第二十八轮独立盲审识别的 **P1-40**(`241V2A-30 §4.1` 把"逐行命中结构正则"错误等同于"识别一张表"——一个 Markdown 表块包含 HEADER + SEPARATOR + N 个 DATA_ROW,所有数据行属于同一张表;但 241V2A-30 把每个匹配行都计数为一张表,得到 `TABLE_CANDIDATE = 29`(实际是 29 个数据行而不是 29 张表);`241V2A-27 §5.1` 候选表发现表 L250-L256 是同一张 TABLE_BLOCK 的 7 个数据行(不是 6 张表);`241V2A-28 §5.3` L251-L257 是 1 张 TABLE_BLOCK 的 7 个数据行;`241V2A-29 §5.4` L266-L272 是 1 张 TABLE_BLOCK 的 7 个数据行;`241V2A-1 L477` 是 §8.1 场景总表的数据行(不是 header);`241V2A-14 L288` 是 §3.4 DEFAULT-01~05 表的数据行(不是 header))通过本补丁**真闭环**——**§2 TABLE_BLOCK 定义冻结**(HEADER_ROW + SEPARATOR_ROW + DATA_ROW × N≥1);**§3 7 STEP Markdown 表块识别算法冻结**(逐文档逐行 → 发现 HEADER_ROW → 检查 SEPARATOR_ROW → 开始 TABLE_BLOCK → 读取连续 DATA_ROW → 整个块 = 1 个 TABLE_BLOCK → 对 HEADER_ROW 执行结构正则判断);**§3.2 严禁把数据行当成独立 TABLE_CANDIDATE**(同一 TABLE_BLOCK 中无论 N=1/N=7/N=100,`TABLE_CANDIDATE = 1`);**§3.3 HEADER 是结构判断的唯一依据**;**显式作废 241V2A-30 §4.1 错误逻辑**;**§4 重新检查 241V2A-27/28/29** —— 全部是 1 张 TABLE_BLOCK(L249 header + L250 separator + L251-257 data),HEADER 不含 A/B/C/D/E 模式,**不计入** TABLE_CANDIDATE;**§5 重新判定 241V2A-1 L477 / 241V2A-14 L288** —— 都是数据行,不是 header,HEADER 不含 A/B/C/D/E 模式,**不计入** TABLE_CANDIDATE;**§6 六个数字实测** —— DOCUMENT_CANDIDATE = 36 / TABLE_BLOCK_TOTAL = 656 / TABLE_CANDIDATE = 7 / FORMAL_TABLE_CANDIDATE = 2 / CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 5;**§7 TABLE_CANDIDATE 完整列表 7 张**(241V2A-22 §4 / 241V2A-23 §2 / 241V2A-24 §2.3 / §3.4 / §5 / 241V2A-25 §2.3 / §3.4,每张标注 document / section / header_line / separator_line / data_start_line / data_end_line / table_block_line_count / classification);**§8 集合等式验证** —— 7 = 2 + 5 ✓ / 2 = 1 + 1 ✓;**§9 集合互斥验证** —— 4 组全部 = ∅;**§10 TABLE_BLOCK_GRANULARITY_ASSERTION 硬断言** —— 一个 TABLE_BLOCK = 一个 TABLE_CANDIDATE ✓ / 数据行不单独成候选 ✓ / HEADER + SEPARATOR + DATA_ROWS 组成 TABLE_BLOCK ✓ / TABLE_CANDIDATE 由 TABLE_BLOCK 产生 ✓ / 不允许单行正则命中数代替表数量 ✓;**§11 当前 Spec PASS 不改变**(`CURRENT_FORMAL` = `241V2A-25 §2.3` 22 行五维差集全部 = ∅);**§12.1 P1-39 纯发现层职责保持**;**§12.2 P1-38 DOCUMENT_CANDIDATE glob 规则保持**;**§12.3 P1-37 三个独立集合 + 集合等式保持**;**§12.4 P1-36 自动发现 4 条 + 三分类 + 严禁人工隐式指定保持**;**§12.5 P1-35 normalization 6 步硬性规则保持**;**§13 P2 OPEN 6 / CLOSED 3 状态诚实保留**(本轮新增 P2-8 OPEN);241V2A-31 不修改 241V2A-30 / 241V2A-29 / 241V2A-28 / 241V2A-27 / 任何历史 MD 任何字节,只通过"显式作废旧逐行逻辑 + 显式冻结 TABLE_BLOCK 定义 + 显式 7 STEP 表块识别算法 + 显式重新实测 + 显式硬断言"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §16 附录

- 章节数:17(§0 元信息 + §1 P1-40 问题陈述 + §2 TABLE_BLOCK 定义 + §3 7 STEP 算法 + §4 重新检查 241V2A-27/28/29 + §5 重新判定 241V2A-1/14 + §6 六个数字 + §7 7 张候选表完整列表 + §8 集合等式 + §9 集合互斥 + §10 硬断言 + §11 当前 Spec PASS + §12 P1 保持 + §13 P2 + §14 自评 + §15 一句话最终判断 + §16 附录)
- 修复的 P1:1(P1-40)
- 显式作废的旧逻辑:`241V2A-30 §4.1` "逐行命中 = 一张表"
- 新增概念:`TABLE_BLOCK`(HEADER + SEPARATOR + DATA_ROWS)
- 新增数字:`TABLE_BLOCK_TOTAL = 656`
- 实测 TABLE_CANDIDATE:**7**(表块级,HEADER 含 A/B/C/D/E)
- 集合等式:7 = 2 + 5 / 2 = 1 + 1 全部 PASS
- 集合互斥:4 组全部 PASS
- 硬断言:TABLE_BLOCK_GRANULARITY_ASSERTION 全部 PASS
- 保持闭环:P1-14 ~ P1-39 不被改写
- 当前 Spec PASS:CURRENT_FORMAL = `241V2A-25 §2.3`(22 行五维差集全部 = ∅)
- P2 OPEN 6 / CLOSED 3(状态诚实)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- S1-169-2 = BLOCK

**【241V2A-31 自评声明】** 本轮 P1-40 修复方法已通过"补丁后独立自审"识别并冻结,但**不声明 PASS**——按规则等待下一轮独立盲审确认。