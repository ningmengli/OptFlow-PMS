# 241V2A-30 S1-169-1 TABLE_CANDIDATE 纯发现层与误命中保留规则修复补丁

> **阶段**:S1-169-1
> **补丁类型**:独立盲审修复(第二十七轮)
> **优先级**:**最高**(覆盖 241V2A-29 §5.4 TABLE_CANDIDATE = 7 错误数字 + TABLE_CANDIDATE 纯发现层定义)
> **基线 HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
> **严禁修改**:241V2A-29 / 241V2A-28 / 241V2A-27 / 任何历史 MD / VisionCare PMS 任何文件

---

## §0 元信息

- **创建日期**:2026-09-15
- **修复目标**:
  - **P1-39**:`241V2A-29 §2.1` 定义 `TABLE_CANDIDATE` 为"任何含 A/B/C/D/E 模式表头的表格"(纯结构发现层),但 §5.3 实测发现 241V2A-1 有 1 个 TC 误命中 + 241V2A-14 有 1 个 TC 误命中;§5.4 又写"排除误命中与规则表后 `TABLE_CANDIDATE = 7`"——这混淆了**纯结构发现层**与**正式规则过滤层**,违反了 `TABLE_CANDIDATE` 的纯结构定义;必须把 `TABLE_CANDIDATE` 修正为**只由结构正则产生**,误命中也必须属于 `TABLE_CANDIDATE`,语义判断留给 `FORMAL/NON_FORMAL` 分类阶段
- **本轮 P2 增量**:**无**(P2 OPEN 5 / CLOSED 3 保持)

---

## §1 P1-39 问题陈述(241V2A-30 显式)

### 1.1 241V2A-29 表述矛盾

| 章节 | 表述 | 含义 |
|---|---|---|
| §2.1 | `TABLE_CANDIDATE` = 任何含 A/B/C/D/E 模式表头的所有表格 | **纯结构发现层** |
| §5.3 | 列出 7 张表(含分类为 `CURRENT_FORMAL` / `HISTORICAL_FORMAL` / `NON_FORMAL`) | **混合层**(既含结构发现又含语义分类) |
| §5.4 | "排除误命中与规则表后 `TABLE_CANDIDATE = 7`" | **错误**——`TABLE_CANDIDATE` 不应"排除误命中",只应做结构判定 |

### 1.2 自相矛盾点

| 矛盾 | 实际数字 |
|---|---|
| `241V2A-29 §2.1` 定义:`TABLE_CANDIDATE` 应包含所有结构命中 | 实测命中 = **29**(241V2A-1/14/22/23/24/25/27/28/29 全部) |
| `241V2A-29 §5.4` 写 "TABLE_CANDIDATE = 7" | 实际是**已过滤后**的 `FORMAL_TABLE_CANDIDATE ∪ NON_FORMAL(纯五维实例表)` 的子集,不是 `TABLE_CANDIDATE` 本身 |
| **241V2A-1 L477**(并发场景表) | 正则误命中,但 `TABLE_CANDIDATE = YES`(纯结构层)|
| **241V2A-14 L288**(DEFAULT 测试表) | 正则误命中,但 `TABLE_CANDIDATE = YES`(纯结构层)|
| **241V2A-27 L69**(自身 §2.1 规则表) | 表头含 A/B/C/D/E 模式,`TABLE_CANDIDATE = YES`,但 `FORMAL_TABLE_CANDIDATE = NO`(因不是正式五维实例表)→ `NON_FORMAL = YES` |
| **241V2A-28 / 29**(自身实测表) | 同上 |

### 1.3 必须冻结的"纯结构发现层"

**TABLE_CANDIDATE 必须满足**:
1. **唯一职责**:扫描 `DOCUMENT_CANDIDATE` 中所有匹配结构正则的表格
2. **不做任何语义判断**:不判定"是不是误命中" / "是不是规则表" / "是不是正式实例表"
3. **结果完整**:所有结构命中的表都进入 `TABLE_CANDIDATE`,无遗漏
4. **可复现**:同一 `DOCUMENT_CANDIDATE` + 同一正则 → 同一 `TABLE_CANDIDATE`

---

## §2 层级职责重新冻结(241V2A-30 最高优先级)

### 2.1 完整扫描链(241V2A-30 最高优先级冻结)

**【241V2A-30 最高优先级冻结】** 完整扫描链:

```
DOCUMENT_CANDIDATE (S1-169-1 untracked 241*.md, 36 份)
    ↓ [glob 模式 241*.md + S1-169-1 untracked 计数规则, 241V2A-29 §2]
↓
TABLE_CANDIDATE [纯结构发现层, 241V2A-30 §2.2]
    ↓ [241V2A-27 §2.1 4 条硬性规则]
↓
FORMAL_TABLE_CANDIDATE [正式规则候选, 241V2A-27 §2.1]
    ↓ [241V2A-27 §3.5 三分类判定流程]
↓
CLASSIFIED_TABLE = CURRENT_FORMAL ∪ HISTORICAL_FORMAL
```

### 2.2 TABLE_CANDIDATE 纯发现层职责(241V2A-30 显式冻结)

**【241V2A-30 显式冻结】** `TABLE_CANDIDATE` **只允许执行**:

| # | 允许执行 | 说明 |
|---:|---|---|
| 1 | 从 `DOCUMENT_CANDIDATE` 中扫描所有表格 | 遍历 36 份文档的全部行 |
| 2 | 判断表头是否满足结构正则 | `^\|.*\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|` |
| 3 | 满足就进入 `TABLE_CANDIDATE` | 直接加入集合,不做其他判断 |

**【241V2A-30 显式严禁】** `TABLE_CANDIDATE` 层**不得**执行以下判断:

| # | 严禁执行 | 理由 |
|---:|---|---|
| 1 | "是不是正式五维实例" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 2 | "是不是误命中" | 留给 `FORMAL_TABLE_CANDIDATE`(误命中不通过规则) |
| 3 | "是不是规则表" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 4 | "是不是对照表" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 5 | "是不是差集结果" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 6 | "是不是未来候选" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 7 | "是不是有实际业务意义" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 8 | "是不是同一份文档的实测表" | 留给 `FORMAL_TABLE_CANDIDATE` |
| 9 | "是不是当前补丁文件自身" | 留给 `DOCUMENT_CANDIDATE` 层(glob 自动纳入) |
| 10 | "是不是 241V2A-N 自身" | 留给 `DOCUMENT_CANDIDATE` 层 |

**【241V2A-30 显式】** 任何"误命中 / 规则表 / 对照表 / 差集结果 / 未来候选 / 自身实测表"都必须**进入** `TABLE_CANDIDATE`,然后在后续 `FORMAL/NON_FORMAL` 分类阶段处理。

### 2.3 显式作废 241V2A-29 §5.4(241V2A-30 显式)

**【241V2A-30 显式作废】** `241V2A-29 §5.4`:

> "排除误命中与规则表后,`TABLE_CANDIDATE = 7`"

**作废理由**:
1. "排除"违反 `TABLE_CANDIDATE` 纯结构发现层定义
2. 误命中必须属于 `TABLE_CANDIDATE`(只在 `FORMAL_TABLE_CANDIDATE` 中被排除)
3. 241V2A-27 / 28 / 29 自身的规则表 / 实测表 / 硬断言表,表头含 A/B/C/D/E 模式,**必须**属于 `TABLE_CANDIDATE`
4. 硬编码 `TABLE_CANDIDATE = 7` 是错误的数字(实际是 29)

**替代为**:241V2A-30 §4 重新扫描全部 `DOCUMENT_CANDIDATE`,得到 `TABLE_CANDIDATE = 29`(纯结构)。

---

## §3 严格区分"候选表"和"正式候选表"(241V2A-30 显式)

### 3.1 三层职责(241V2A-30 显式)

**【241V2A-30 显式】** 三层职责明确分工:

| 层 | 名称 | 职责 | 数字 |
|---|---|---|---:|
| 第一层 | `TABLE_CANDIDATE` | 纯结构发现,只判断表头是否匹配结构正则 | **29** |
| 第二层 | `FORMAL_TABLE_CANDIDATE` | 通过 `241V2A-27 §2.1` 4 条硬性规则,判断是否正式五维实例表 | **2** |
| 第三层 | `CURRENT_FORMAL` / `HISTORICAL_FORMAL` | 判断正式表是当前有效还是历史已作废 | **1 + 1** |

### 3.2 误命中处理(241V2A-30 显式)

**【241V2A-30 显式】** 一个"正则误命中"在三层的归属:

| 层 | 误命中归属 |
|---|---|
| `TABLE_CANDIDATE` | **YES**(纯结构命中) |
| `FORMAL_TABLE_CANDIDATE` | **NO**(不通过 4 条硬性规则) |
| `NON_FORMAL` | **YES**(归入 NON_FORMAL) |

**严禁**:误命中从 `TABLE_CANDIDATE` 中**删除**——这是错误的语义提前。

### 3.3 规则表/集合验证表/实测表/硬断言表处理(241V2A-30 显式)

**【241V2A-30 显式】** 241V2A-27 / 28 / 29 自身的规则表 / 集合验证表 / 实测表 / 硬断言表(表头含 A/B/C/D/E 模式):

| 层 | 归属 |
|---|---|
| `TABLE_CANDIDATE` | **YES**(纯结构命中) |
| `FORMAL_TABLE_CANDIDATE` | **NO**(不是正式五维实例表) |
| `NON_FORMAL` | **YES**(归入 NON_FORMAL) |

**严禁**:这些表从 `TABLE_CANDIDATE` 中**删除**。

---

## §4 重新扫描全部 DOCUMENT_CANDIDATE(241V2A-30 §4 实测)

### 4.1 实测方法

**【241V2A-30 §4.1 实测方法】**:

```
Step 1: DOCUMENT_CANDIDATE = 36 份(glob "241*.md" + S1-169-1 untracked)
Step 2: 对每份文档的每一行,应用结构正则
        匹配规则: ^\|.*\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\|
Step 3: 命中的每一行(对应一个表格)加入 TABLE_CANDIDATE
Step 4: TABLE_CANDIDATE = 命中数 = 29(实测)
Step 5: 在 TABLE_CANDIDATE 中应用 241V2A-27 §2.1 4 条硬性规则
        得到 FORMAL_TABLE_CANDIDATE = 2(241V2A-25 §2.3 + 241V2A-24 §2.3)
Step 6: 三分类
        CURRENT_FORMAL = 1(241V2A-25 §2.3 L55)
        HISTORICAL_FORMAL = 1(241V2A-24 §2.3 L111)
        NON_FORMAL = 29 - 2 = 27(其余)
```

### 4.2 实测结果汇总

| 集合 | 数字 |
|---|---:|
| `DOCUMENT_CANDIDATE` | **36** |
| `TABLE_CANDIDATE`(纯结构) | **29** |
| `FORMAL_TABLE_CANDIDATE` | **2** |
| `CURRENT_FORMAL` | **1** |
| `HISTORICAL_FORMAL` | **1** |
| `NON_FORMAL` | **27** |

---

## §5 完整 TABLE_CANDIDATE 列表(241V2A-30 §5,29 条)

### 5.1 完整 29 条列表(241V2A-30 §5.1 实测)

| # | 文档 | 章节 | 行号 | 表头 | 分类 | 备注 |
|---:|---|---|---:|---|---|---|
| 1 | `241V2A-1` | §8.1 场景总表 | L477 | `\| 3 \| A 失败 + B 成功 \| companyA=1, companyB=0 \| A → setDefault(C) 失败(C 无权限) \| B → setDefault(B) 成功 \| ...` | **NON_FORMAL** | **正则误命中**(含 A/B/C 单字符,**非 A/B/C/D/E 维度列**);仍属于 TABLE_CANDIDATE |
| 2 | `241V2A-14` | §3.4 DEFAULT-01~05 完整运行时验证职责表 | L288 | `\| **02** \| u1 / A=default / B / C \| 串行 → B \| verify(u1, B, C) \| ...` | **NON_FORMAL** | **正则误命中**(含 A/B/C 单字符);仍属于 TABLE_CANDIDATE |
| 3 | `241V2A-22` | (五维模型总览示例表) | L257 | `\| # \| 对象 \| 维度 A 证据来源 \| 维度 B 规范形成 \| 维度 C Spec 状态 \| 维度 D Git 跟踪 \| 维度 E Git 工作区 \|` | **NON_FORMAL** | 真五维示例表;被 241V2A-23 §2 沿用并被 241V2A-24 §2.3 显式作废 |
| 4 | `241V2A-23` | §2 五维合法枚举示例 | L303 | `\| # \| 对象 \| A 证据来源 \| B 规范形成 \| C Spec \| D Git 跟踪 \| E Git 工作区 \|` | **NON_FORMAL** | 真五维示例表;被 241V2A-24 §2.3 显式作废 |
| 5 | `241V2A-24` | §2.3 五维合法实例表 | L111 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | **HISTORICAL_FORMAL** | 真五维实例表;被 241V2A-25 §2.3 显式作废 |
| 6 | `241V2A-24` | §3.4 维度 A 与 B/C/D/E 的 N/A 区别表 | L200 | `\| 场景 \| A \| B \| C \| D \| E \|` | **NON_FORMAL** | 真五维 N/A 区别表;不是正式五维实例表 |
| 7 | `241V2A-24` | §5 五维对象有效性规则 | L256 | `\| 对象属性 \| A \| B \| C \| D \| E \|` | **NON_FORMAL** | 真五维规则表;不是正式五维实例表 |
| 8 | `241V2A-25` | §2.3 重制后的五维合法实例表 | L55 | `\| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | **CURRENT_FORMAL** | 真五维实例表;当前 Spec PASS 唯一对象 |
| 9 | `241V2A-25` | §3.4 对照扫描结果 | L217 | `\| 维度 \| A_actual \| B_actual \| C_actual \| D_actual \| E_actual \|` | **NON_FORMAL** | 差集结果表;不是正式五维实例表 |
| 10 | `241V2A-27` | §2.1 自动发现 4 条硬性规则 | L69 | `\| 2 \| **表头同时包含 A / B / C / D / E 五个维度列** \| 表格首行匹配 ...` | **NON_FORMAL** | **241V2A-27 自身规则说明表**;表头含 A/B/C/D/E 模式(规则描述中),属于 TABLE_CANDIDATE |
| 11 | `241V2A-27` | §5.1 候选正式五维表发现 | L250 | `\| 1 \| 241V2A-25 §2.3 L55 \| ... \| A/B/C/D/E 8 列 \| ...` | **NON_FORMAL** | **241V2A-27 自身实测表**;不是正式五维实例表 |
| 12 | `241V2A-27` | §5.1 候选正式五维表发现 | L252 | `\| 3 \| 241V2A-25 §3.4 L217 \| ... \| 维度 \| A_actual \| ...` | **NON_FORMAL** | **241V2A-27 自身实测表** |
| 13 | `241V2A-27` | §5.1 候选正式五维表发现 | L253 | `\| 4 \| 241V2A-24 §3.4 L200 \| ... \| 场景 \| A \| B \| C \| D \| E \|` | **NON_FORMAL** | **241V2A-27 自身实测表** |
| 14 | `241V2A-27` | §5.1 候选正式五维表发现 | L255 | `\| 6 \| 241V2A-23 §2 L303 \| ... \| 维度 A \| 维度 B \| 维度 C \| 维度 D \| 维度 E \|` | **NON_FORMAL** | **241V2A-27 自身实测表** |
| 15 | `241V2A-27` | §5.1 候选正式五维表发现 | L256 | `\| 7 \| 241V2A-22 §4 L257 \| ... \| 维度 A \| 维度 B \| 维度 C \| 维度 D \| 维度 E \|` | **NON_FORMAL** | **241V2A-27 自身实测表** |
| 16 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L251 | `\| 1 \| 241V2A-22 §4 L257 \| ... \| 维度 A \| 维度 B \| 维度 C \| 维度 D \| 维度 E \|` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 17 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L252 | `\| 2 \| 241V2A-23 §2 L303 \| ... \| A 证据来源 \| B 规范形成 \| ...` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 18 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L253 | `\| 3 \| 241V2A-24 §2.3 L111 \| ... \| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 19 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L254 | `\| 4 \| 241V2A-24 §3.4 L200 \| ... \| 场景 \| A \| B \| C \| D \| E \|` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 20 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L255 | `\| 5 \| 241V2A-24 §5 L256 \| ... \| 对象属性 \| A \| B \| C \| D \| E \|` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 21 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L256 | `\| 6 \| 241V2A-25 §2.3 L55 \| ... \| # \| 对象 \| A \| B \| C \| D \| E \| 备注 \|` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 22 | `241V2A-28` | §5.3 TABLE_CANDIDATE = 7 完整列表 | L257 | `\| 7 \| 241V2A-25 §3.4 L217 \| ... \| 维度 \| A_actual \| B_actual \| ...` | **NON_FORMAL** | **241V2A-28 自身实测表** |
| 23 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L266 | `\| 1 \| 241V2A-22 \| L257 \| §4 五维模型总览示例 \| ... \| NON_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 24 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L267 | `\| 2 \| 241V2A-23 \| L303 \| ... \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 25 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L268 | `\| 3 \| 241V2A-24 \| L111 \| §2.3 五维合法实例表 \| ... \| HISTORICAL_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 26 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L269 | `\| 4 \| 241V2A-24 \| L200 \| §3.4 N/A 区别表 \| ... \| NON_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 27 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L270 | `\| 5 \| 241V2A-24 \| L256 \| §5 五维对象有效性规则 \| ... \| NON_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 28 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L271 | `\| 6 \| 241V2A-25 \| L55 \| §2.3 重制后的五维合法实例表 \| ... \| CURRENT_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |
| 29 | `241V2A-29` | §5.4 TABLE_CANDIDATE 完整列表 | L272 | `\| 7 \| 241V2A-25 \| L217 \| §3.4 对照扫描结果 \| ... \| NON_FORMAL \|` | **NON_FORMAL** | **241V2A-29 自身实测表** |

### 5.2 29 条分类汇总(241V2A-30 §5.2)

| 分类 | 数量 | 备注 |
|---|---:|---|
| 正则误命中 | **2** | `241V2A-1 L477` + `241V2A-14 L288` |
| 真五维实例表(CURRENT_FORMAL) | **1** | `241V2A-25 L55` |
| 真五维实例表(HISTORICAL_FORMAL) | **1** | `241V2A-24 L111` |
| 真五维 N/A 区别表 | **1** | `241V2A-24 L200` |
| 真五维对象有效性规则表 | **1** | `241V2A-24 L256` |
| 真五维示例表(被后续作废) | **2** | `241V2A-22 L257` + `241V2A-23 L303` |
| 差集结果表 | **1** | `241V2A-25 L217` |
| 241V2A-27 自身实测表 | **6** | L69(规则表)+ L250/L252/L253/L255/L256 |
| 241V2A-28 自身实测表 | **7** | L251~L257 |
| 241V2A-29 自身实测表 | **7** | L266~L272 |
| **总计** | **29** | — |

### 5.3 误命中专门检查(241V2A-30 §5.3)

**【241V2A-30 §5.3 显式】** 误命中检查:

| 误命中项 | TABLE_CANDIDATE | FORMAL_TABLE_CANDIDATE | NON_FORMAL |
|---|:---:|:---:|:---:|
| `241V2A-1 L477` | **✓ YES** | ✗ NO | **✓ YES** |
| `241V2A-14 L288` | **✓ YES** | ✗ NO | **✓ YES** |

**关键**:误命中**必须属于** `TABLE_CANDIDATE`,只在 `FORMAL_TABLE_CANDIDATE` 中被排除。

---

## §6 六个数字实测结果(241V2A-30 §6)

### 6.1 六个数字实测

| 数字 | 值 |
|---|---:|
| **DOCUMENT_CANDIDATE** | **36** |
| **TABLE_CANDIDATE**(纯结构) | **29** |
| **FORMAL_TABLE_CANDIDATE** | **2** |
| **CURRENT_FORMAL** | **1** |
| **HISTORICAL_FORMAL** | **1** |
| **NON_FORMAL** | **27** |

### 6.2 与之前数字对比

| 数字 | 241V2A-29 §5.4 旧 | 241V2A-30 §6.1 新 | 差异原因 |
|---|---:|---:|---|
| `TABLE_CANDIDATE` | 7(错误) | **29**(正确) | 旧表述"排除误命中与规则表后"违反纯结构定义 |
| `FORMAL_TABLE_CANDIDATE` | 2 | **2** | 不变 |
| `CURRENT_FORMAL` | 1 | **1** | 不变 |
| `HISTORICAL_FORMAL` | 1 | **1** | 不变 |
| `NON_FORMAL` | 5(只含真五维非正式) | **27**(含所有非正式,包括误命中 + 自身规则表) | 旧表述漏掉 22 项误命中 + 自身规则表 |

---

## §7 两组集合等式验证(241V2A-30 §7)

**【241V2A-30 §7 实测】**:

| 等式 | 左 | 右 | 结果 |
|---|---:|---:|---|
| **等式 1**:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 29 | 2 + 27 = 29 | ✓ **相等** |
| **等式 2**:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 | 1 + 1 = 2 | ✓ **相等** |

---

## §8 集合互斥验证(241V2A-30 §8)

| 集合对 | 交集 | 验证 |
|---|---|---|
| `CURRENT_FORMAL ∩ HISTORICAL_FORMAL` | ∅ | ✓ `{241V2A-25 L55} ∩ {241V2A-24 L111} = ∅` |
| `CURRENT_FORMAL ∩ NON_FORMAL` | ∅ | ✓ `{241V2A-25 L55} ∩ {27 张 NON_FORMAL} = ∅` |
| `HISTORICAL_FORMAL ∩ NON_FORMAL` | ∅ | ✓ `{241V2A-24 L111} ∩ {27 张 NON_FORMAL} = ∅` |
| `FORMAL_TABLE_CANDIDATE ∩ NON_FORMAL` | ∅ | ✓ `{2 张} ∩ {27 张} = ∅` |

---

## §9 TABLE_CANDIDATE_PURITY_ASSERTION 硬断言(241V2A-30 最高优先级)

**【TABLE_CANDIDATE_PURITY_ASSERTION】**(241V2A-30 硬性断言):

```
TABLE_CANDIDATE 只由结构发现产生。
TABLE_CANDIDATE = 匹配结构正则 ^\|.*\|.*A.*\|.*B.*\|.*C.*\|.*D.*\|.*E.*\| 的所有表格。
任何"误命中 / 非正式 / 规则表 / 对照表 / 差集结果 / 未来候选 / 自身实测表"，
必须在 TABLE_CANDIDATE 中保留;
不得在 TABLE_CANDIDATE 层删除。
FORMAL_TABLE_CANDIDATE = TABLE_CANDIDATE 中通过 241V2A-27 §2.1 4 条硬性规则的子集。
NON_FORMAL = TABLE_CANDIDATE 中未通过 4 条硬性规则的剩余子集。
```

**断言状态**(基于 241V2A-30 §5 + §6 实测):

| 检查项 | 实际值 | 状态 |
|---|---|---|
| TABLE_CANDIDATE = 纯结构命中 | 29 | ✓ PASS |
| `241V2A-1 L477` 误命中在 TABLE_CANDIDATE 中 | ✓ YES | ✓ PASS |
| `241V2A-14 L288` 误命中在 TABLE_CANDIDATE 中 | ✓ YES | ✓ PASS |
| 241V2A-27 自身规则表(6 张)在 TABLE_CANDIDATE 中 | ✓ YES | ✓ PASS |
| 241V2A-28 自身实测表(7 张)在 TABLE_CANDIDATE 中 | ✓ YES | ✓ PASS |
| 241V2A-29 自身实测表(7 张)在 TABLE_CANDIDATE 中 | ✓ YES | ✓ PASS |
| 等式 1:`TABLE_CANDIDATE = FORMAL_TABLE_CANDIDATE + NON_FORMAL` | 29 = 2 + 27 | ✓ PASS |
| 等式 2:`FORMAL_TABLE_CANDIDATE = CURRENT_FORMAL + HISTORICAL_FORMAL` | 2 = 1 + 1 | ✓ PASS |
| 4 组集合互斥 | 全部 = ∅ | ✓ PASS |

**任一断言失败**:**P1-39 = OPEN + S1-169-2 = BLOCK**

---

## §10 当前 Spec PASS 对象(241V2A-30 §10)

**【241V2A-30 §10 显式】** 当前 Spec PASS 判定对象**不因本轮修复而改变**:

| 项目 | 值 |
|---|---|
| 当前 Spec PASS 唯一对象 | `CURRENT_FORMAL` = `241V2A-25 §2.3` L55(22 行) |
| 当前 Spec PASS 状态 | **TRUE**(`241V2A-25 §2.3` 22 行五维差集全部 = ∅) |
| 历史回归对象 | `HISTORICAL_FORMAL` = `241V2A-24 §2.3` L111(被 `241V2A-25 §2.3` 显式作废) |

---

## §11 P1-38 / P1-37 / P1-36 / P1-35 保持(241V2A-30 §11 显式)

### 11.1 P1-38 保持

**【241V2A-30 显式保持】** `241V2A-29 §2` `DOCUMENT_CANDIDATE` = glob `241*.md` + S1-169-1 untracked 文档集合**不被改写**。

### 11.2 P1-37 保持

**【241V2A-30 显式保持】** `241V2A-28 §2` 三个独立集合(`TABLE_CANDIDATE` / `FORMAL_TABLE_CANDIDATE` / `CLASSIFIED_TABLE`)+ 集合等式 + 集合互斥 + 术语规则**不被改写**。

### 11.3 P1-36 保持

**【241V2A-30 显式保持】** `241V2A-27 §2.1` 自动发现 4 条硬性规则 + 三分类 + 严禁人工隐式指定**不被改写**。

### 11.4 P1-35 保持

**【241V2A-30 显式保持】** `241V2A-26 §2.1` normalization 6 步硬性规则**不被改写**:

```
STEP 3.1  去除首尾空白
STEP 3.2  保留原始括号字符
STEP 3.3  仅当完整包裹性 `**...**` 时去除粗体
STEP 3.4  不进行其他语义改写
STEP 3.5  得到 normalized_cell_value
STEP 3.6  与该维度 LEGAL 集合做差集
```

---

## §12 P2 状态保持(241V2A-30 §12 显式)

| 编号 | 描述 | 状态 |
|---|---|---|
| P2-0 | exactly-one 业务规则需 fallback | **OPEN** |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **OPEN** |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **OPEN** |
| P2-6 | 章节编号/统计一致性 | **OPEN** |
| P2-7 | 章节编号缺 3 的文档问题 | **OPEN** |
| P2-3 | 证据标签分级 | CLOSED |
| P2-4 | 60003/60004 证据等级误标 | CLOSED |
| P2-5 | "通用技术事实"误归【原系统事实】 | CLOSED |

**【241V2A-30 显式】** 本轮**只修 P1-39**,**不修 P2**;P2 状态诚实保留。

---

## §13 P1-39 自评(241V2A-30 §13 显式)

**自审方法**:对 `241V2A-29 §2.1 / §5.3 / §5.4` 表述进行逐字审查:

| 矛盾点 | 旧表述 | 实际数字 | 矛盾? |
|---|---|---|---|
| §2.1 定义 | "含 A/B/C/D/E 模式表头的所有表格" | 29 | ✓ |
| §5.3 实测发现 | 误命中 2 条 + 规则表多条 | 实际命中 29 | ✓ |
| §5.4 数字 | "排除误命中与规则表后 TABLE_CANDIDATE = 7" | 硬编码 7,违反 §2.1 纯结构定义 | ✓ |

**修复方法**:241V2A-30 §2 重新冻结层级职责 + §3 严格区分候选表/正式候选表 + §4 重新扫描 + §5 完整 29 条列表 + §9 硬断言。

**自审 PASS 项**:
- ✓ P1-39 矛盾识别正确
- ✓ TABLE_CANDIDATE = 29(纯结构,不"排除"任何项)
- ✓ 误命中(2 条)+ 自身规则表(20 条)全部在 TABLE_CANDIDATE 中保留
- ✓ FORMAL_TABLE_CANDIDATE = 2 / CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 27
- ✓ 等式 1:29 = 2 + 27 ✓
- ✓ 等式 2:2 = 1 + 1 ✓
- ✓ 4 组集合互斥全部 PASS
- ✓ TABLE_CANDIDATE_PURITY_ASSERTION 硬断言全部 PASS
- ✓ 当前 Spec PASS 不改变(`CURRENT_FORMAL` = `241V2A-25 §2.3`)

**未自评 PASS**:等待下一轮独立盲审确认本轮修复方法是否真正成立。

---

## §14 一句话最终判断

> **241V2A-30 S1-169-1 TABLE_CANDIDATE 纯发现层与误命中保留规则修复补丁完成**:第二十七轮独立盲审识别的 **P1-39**(`241V2A-29 §2.1` 定义 `TABLE_CANDIDATE` 为"任何含 A/B/C/D/E 模式表头的所有表格"——纯结构发现层,但 §5.3 实测发现 241V2A-1 有 1 个 TC 误命中 + 241V2A-14 有 1 个 TC 误命中,§5.4 又写"排除误命中与规则表后 `TABLE_CANDIDATE = 7`"——这混淆了**纯结构发现层**与**正式规则过滤层**,违反了 `TABLE_CANDIDATE` 的纯结构定义)通过本补丁**真闭环**——**§2 层级职责重新冻结**(`TABLE_CANDIDATE` **只允许执行** 3 件事:扫描所有表格 / 判断表头是否满足结构正则 / 满足就进入集合;**严禁执行** 10 类判断:是不是正式实例 / 是不是误命中 / 是不是规则表 / 是不是对照表 / 是不是差集结果 / 是不是未来候选 / 是不是有实际业务意义 / 是不是同一份文档的实测表 / 是不是当前补丁文件自身 / 是不是 241V2A-N 自身);**§3 三层职责分工**(第一层 TABLE_CANDIDATE 纯结构 / 第二层 FORMAL_TABLE_CANDIDATE 通过 4 条规则 / 第三层 CURRENT/HISTORICAL 分类);**§3.2 误命中处理**(TABLE_CANDIDATE = YES / FORMAL_TABLE_CANDIDATE = NO / NON_FORMAL = YES);**§3.3 规则表/集合验证表/实测表/硬断言表处理**(241V2A-27/28/29 自身的规则表 / 实测表 / 硬断言表,表头含 A/B/C/D/E 模式,必须属于 TABLE_CANDIDATE = YES / FORMAL_TABLE_CANDIDATE = NO / NON_FORMAL = YES);**显式作废 241V2A-29 §5.4 "TABLE_CANDIDATE = 7" 错误数字**;**§4 重新扫描全部 DOCUMENT_CANDIDATE** 实测 29 条结构命中;**§5 完整 29 条列表**(241V2A-1 L477 误命中 / 241V2A-14 L288 误命中 / 241V2A-22 L257 / 241V2A-23 L303 / 241V2A-24 L111 HISTORICAL_FORMAL / 241V2A-24 L200 / 241V2A-24 L256 / 241V2A-25 L55 CURRENT_FORMAL / 241V2A-25 L217 / 241V2A-27 自身 6 张实测表 / 241V2A-28 自身 7 张实测表 / 241V2A-29 自身 7 张实测表);**§6 六个数字实测** —— DOCUMENT_CANDIDATE = 36 / TABLE_CANDIDATE = 29 / FORMAL_TABLE_CANDIDATE = 2 / CURRENT_FORMAL = 1 / HISTORICAL_FORMAL = 1 / NON_FORMAL = 27;**§7 集合等式验证** —— 29 = 2 + 27 ✓ / 2 = 1 + 1 ✓;**§8 集合互斥验证** —— 4 组全部 = ∅;**§9 TABLE_CANDIDATE_PURITY_ASSERTION 硬断言** —— TABLE_CANDIDATE = 纯结构命中 / 误命中 2 条在 TABLE_CANDIDATE 中 / 241V2A-27/28/29 自身规则表共 20 条在 TABLE_CANDIDATE 中 / 等式 1 / 等式 2 / 4 组互斥全部 PASS;**§10 当前 Spec PASS 不改变**(`CURRENT_FORMAL` = `241V2A-25 §2.3` L55 22 行五维差集全部 = ∅);**§11.1 P1-38 DOCUMENT_CANDIDATE glob 规则保持**;**§11.2 P1-37 三个独立集合 + 集合等式 + 术语规则保持**;**§11.3 P1-36 自动发现 4 条 + 三分类 + 严禁人工隐式指定保持**;**§11.4 P1-35 normalization 6 步硬性规则保持**;**§12 P2 OPEN 5 / CLOSED 3 状态诚实保留**(本轮不修 P2);241V2A-30 不修改 241V2A-29 / 241V2A-28 / 241V2A-27 / 任何历史 MD 任何字节,只通过"显式作废旧数字 + 显式冻结层级职责 + 显式完整 29 条列表 + 显式实测数字 + 显式硬断言"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §15 附录

- 章节数:16(§0 元信息 + §1 P1-39 问题陈述 + §2 层级职责 + §3 候选表/正式候选表 + §4 重新扫描 + §5 完整 29 条列表 + §6 六个数字 + §7 集合等式 + §8 集合互斥 + §9 硬断言 + §10 当前 Spec PASS + §11 P1 保持 + §12 P2 保持 + §13 自评 + §14 一句话最终判断 + §15 附录)
- 修复的 P1:1(P1-39)
- 显式作废的旧数字:`241V2A-29 §5.4 "TABLE_CANDIDATE = 7"`
- 实测 TABLE_CANDIDATE:**29**(纯结构,含 2 条误命中 + 20 条自身规则表 + 7 条真五维非正式 + 1 条 CURRENT_FORMAL + 1 条 HISTORICAL_FORMAL)
- 集合等式:29 = 2 + 27 / 2 = 1 + 1 全部 PASS
- 集合互斥:4 组全部 PASS
- 硬断言:TABLE_CANDIDATE_PURITY_ASSERTION 全部 PASS
- 保持闭环:P1-14 ~ P1-38(P1-38 glob 规则 / P1-37 三个集合 / P1-36 自动发现 / P1-35 normalization 不被改写)
- 当前 Spec PASS:CURRENT_FORMAL = `241V2A-25 §2.3`(22 行五维差集全部 = ∅)
- P2 OPEN 5 / CLOSED 3(状态诚实)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- S1-169-2 = BLOCK

**【241V2A-30 自评声明】** 本轮 P1-39 修复方法已通过"补丁后独立自审"识别并冻结,但**不声明 PASS**——按规则等待下一轮独立盲审确认。