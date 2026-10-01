# S1-170B｜S1-170A 自身一致性与结论闸门审计

---

## §0. Metadata

| 字段 | 内容 |
|---|---|
| Audit ID | S1-170B |
| Audit Date | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Audit Target | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md`(不修改)|
| Base | `S1-170_Pre-Development_Integrity_Audit.md`(不修改)|
| Scope | S1-170A 自身内部一致性 / 统计一致性 / 结论一致性 / 证据一致性 |
| 严禁 | 修改任何历史 MD / 修改源码 / 创建 backend / 创建 S1-171 / 创建 V2A-43 / commit / push |

---

## §1. Audit Objective

### 1.1 唯一核心问题

> **S1-170A 自身是否已经具备"可以作为下一阶段开发闸门依据"的内部一致性、统计一致性、结论一致性和证据一致性?**

### 1.2 必须审查的 9 个具体问题(老板指令 §1)

1. S1-170A 自身是否出现"前文修正了,后文仍使用旧数字"的问题
2. S1-170A 的 READY / CONDITIONAL / BLOCKED 分类是否与其自身证据一致
3. S1-170A 是否混淆:Specification Ready / Implementation Entry Ready / Production Implementation Ready / Runtime Verified
4. P1/P2 风险是否重复计数
5. V2A-42 是否被同时列为 P1 和 P2,导致严重度和风险总数不一致
6. "整个项目 Effective Spec 已完整冻结"这个结论是否超过证据范围
7. "S1-169 Scope READY"与 E1/E3/E4/E5/E7/E8 的阻塞条件是否逻辑冲突
8. F4 校正后的"Scope-dependent prerequisite"定义是否与 Phase 1 证据要求一致
9. S1-170A 是否已经足以作为下一阶段入口闸门

### 1.3 严禁项

- ✗ 不修改 S1-170A / S1-170 / 任何历史 MD 任何字节
- ✗ 不修改源码 / 数据库
- ✗ 不创建 backend / S1-171 / V2A-43
- ✗ 不 commit / push

---

## §2. Numeric Consistency Audit

### 2.1 全部数字汇总(从 S1-170A 全文抽取)

**【S1-170B 显式抽取】** 逐项列出 S1-170A 中所有数字声明及其出现位置:

| # | 数字 | 出现位置 | 上下文 | 状态 |
|---:|---:|---|---|---|
| 1 | **51** | §1.3 / §2.2 / §11 标题 | S1-169 全系列文件数 | 当前事实 |
| 2 | **56** | §2.2 | S1-169 实际 + 项目核心 5 = 56 | 当前事实 |
| 3 | **60** | §2.1(已校正声明)| S1-170 §2.1 错误数字 | 历史引用 |
| 4 | **65** | §2.1(已校正声明)| S1-170 §2.1 错误数字 | 历史引用 |
| 5 | **36** | §2.2 / §9.1 C2 | S1-169-1 补丁数 | 当前事实 |
| 6 | **35** | §2.2(对比)| S1-170 §7.2 错误数字 | 历史引用 |
| 7 | **41** | §11.2 B(READY 结论)| "41 份 P1/P2 修复 + 7 份 P2 关闭" | **需重新核对** |
| 8 | **7** | §11.2 B | S1-169-2 P2 关闭补丁数 | 当前事实 |
| 9 | **40** | §11.2 B / §9.1 C4 | API 冻结数(232 + 233)| 当前事实 |
| 10 | **12** | §11.2 B / §9.1 C5 | Object 冻结数(238 §2)| 当前事实 |
| 11 | **29** | §11.2 B / §9.1 C6 | State 冻结数(229 §4.2)| 当前事实 |
| 12 | **4** | §11.2 B / §9.1 C6 | 状态机数 | 当前事实 |
| 13 | **31** | §11.2 B | 真 FK 关系数(236B)| 当前事实 |
| 14 | **21** | §11.2 B | 索引数(236B)| 当前事实 |
| 15 | **10** | §11.2 B | CHECK 约束数(236B)| 当前事实 |
| 16 | **5** | §11.2 B | UNIQUE 约束数(236B)| 当前事实 |
| 17 | **47%** | §4.2 / §13 | 当前侦察进度 | 当前事实 |
| 18 | **31 pages** | §4.4.4 | Phase 1 相关页面 | 当前事实 |
| 19 | **32 pages** | §4.4.1 / §4.4.2 | 未侦察子菜单数 | 当前事实 |
| 20 | **41** | §11.2 B | S1-169 P1/P2 修复补丁数 | **⚠️ 矛盾点** |

### 2.2 关键矛盾:§2 vs §11 数字不一致

**【S1-170B 关键发现 N1】** S1-170A 内部数字存在不一致:

| 位置 | S1-170-1 补丁数声明 |
|---|---:|
| **§2.2 表中"S1-169-1 补丁"** | **36**(241V2A + 241V2A-1 ~ 35)|
| **§9.1 C2 "S1-169-1 补丁数量"** | **36** |
| **§11.2 结论 B "41 份 P1/P2 修复 + 7 份 P2 关闭"** | **41**(错误)|

**【S1-170B 显式判断】**:
- §2.2 数字正确(36 份)
- §11.2 结论 B 数字错误(应为 **36 份**,不是 41 份)
- §11.2 结论 B 沿用了 S1-170 §7.2 的旧数字"41"
- **S1-170A 自身出现"前文修正了(§2.2),后文仍使用旧数字(§11.2)"的问题**

**【S1-170B 显式校正建议】**:
- §11.2 结论 B 应改为"36 份 P1/P2 修复 + 7 份 P2 关闭"

### 2.3 旧数字残留审计

**【S1-170B 显式审计】** 检索 S1-170A 全文,以下数字/表述每次出现:

| 数字/表述 | 出现位置 | 分类 | 处理 |
|---|---|---|---|
| **60** | §2.1 / §2.2 / §9.1 C1 | 已校正数字 + 历史引用 | ✓ 已正确处理 |
| **65** | §2.1 / §9.1 C1 | 已校正数字 + 历史引用 | ✓ 已正确处理 |
| **41 份** | §11.2 结论 B(错误)| **未校正残留** | ⚠️ **需修正**(S1-170B 显式标记)|
| **API = 0** | §5 / §9.1 C4 | 已校正声明 + 历史引用 | ✓ 已正确处理 |
| **Object = 3** | §5 / §9.1 C5 | 已校正声明 + 历史引用 | ✓ 已正确处理 |
| **State = 1** | §5 / §9.1 C6 | 已校正声明 + 历史引用 | ✓ 已正确处理 |
| **Hard blocker** | §4.4.4(已校正为 Scope-dependent prerequisite)| 已校正 | ✓ 已正确处理 |
| **COMPLETE** | 未出现 | — | — |
| **READY** | §11.2 结论 B(可能混淆)| **⚠️ 见 §4 详细分析** | — |

### 2.4 当前有效数字矩阵

**【S1-170B 显式】** S1-170A 的当前有效数字(全部已校正):

```
S1-169 全系列文件数:    51 份
S1-169-1 基础:          6 份 (241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4)
S1-169-1 P1/P2 修复:   36 份 (241V2A + 241V2A-1 ~ 35)
S1-169-2 P2 关闭:       7 份 (241V2A-36 ~ 42)
项目核心:               5 份 (00_项目总索引 / 00_项目核心规则_认识论 / 10_AI当前状态 / 08_未确认问题 / 11_页面证据矩阵)

API 冻结数:            40 个 (232 + 233)
Object 冻结数:          12 个 (238 §2)
State 状态机数:         4 个 (229 §4.2)
State 总状态数:         29 个 (229 §4.2)
真 FK 关系数:           31 条 (236B §1.1)
索引数:                21 个 (236B §1.1)
CHECK 约束数:          10 个 (236B §1.1)
UNIQUE 约束数:          5 个 (236B §1.1)
当前侦察进度:           47%
Phase 1 相关页面:       31 个
未侦察子菜单:          32 个
```

---

## §3. Readiness Vocabulary

### 3.1 强制建立 5 层 Readiness 定义

**【S1-170B 显式建立】** S1-170A 缺乏明确的 Readiness 分层,必须正式建立:

| Readiness Level | 定义 | 验证手段 | 当前证据状态 |
|---|---|---|---|
| **SPEC-READY** | Effective Spec 核心内容已经冻结 | 多份 MD 显式冻结 + 五级证据体系 | **核心领域已确认 SPEC-READY** |
| **CONTRACT-READY** | Implementation Contract 足够完整,可以指导编码 | Java Entity / Mapper / Service / Controller 字段级映射 + 输入输出 / 事务 / 安全 / 多租户 / 错误 / 测试 / 验收标准 | **仅 user_company 部分 CONTRACT-READY** |
| **IMPLEMENTATION-READY** | 允许开始 backend/ 实施 | SPEC-READY + CONTRACT-READY + 实施环境就绪 + IGNORE_TABLES 清单 + 公开 API 白名单 | **NOT ESTABLISHED** |
| **PRODUCTION-READY** | 代码 / 配置 / 数据库等已经达到部署条件 | IMPLEMENTATION 完成 + 集成测试 + 部署脚本 + 监控 | **NOT ESTABLISHED** |
| **RUNTIME-VERIFIED** | 测试已经实际执行并达到验收标准 | 测试报告 / Surefire 输出 / 覆盖率 | **NOT ESTABLISHED** |

### 3.2 严禁混淆

**【S1-170B 显式严禁】**:

- ✗ SPEC-READY ≠ IMPLEMENTATION-READY
- ✗ CONTRACT-READY ≠ IMPLEMENTATION-READY
- ✗ IMPLEMENTATION-READY ≠ PRODUCTION-READY
- ✗ PRODUCTION-READY ≠ RUNTIME-VERIFIED
- ✗ 一个 REPORTED READY 不能跨层级推广

### 3.3 当前各层 Readiness 状态

| Layer | S1-169 Scope | OptFlow PMS 整体 | Phase 1 范围 |
|---|:-:|:-:|:-:|
| **SPEC-READY** | ✓ READY | ✓ READY(核心领域)| ⚠️ 未单独审计 |
| **CONTRACT-READY** | ⚠️ 部分(仅 user_company)| ⚠️ 部分(仅 user_company)| ⚠️ 未单独审计 |
| **IMPLEMENTATION-READY** | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED |
| **PRODUCTION-READY** | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED |
| **RUNTIME-VERIFIED** | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED | ✗ NOT ESTABLISHED |

---

## §4. READY / BLOCKER 逻辑一致性审计

### 4.1 S1-170A §11.2 结论 B vs §12 Entry Conditions

**【S1-170B 关键发现 N2】** S1-170A 内部存在"READY"与"BLOCKED"概念冲突:

| 结论 | S1-170A 表述 |
|---|---|
| **结论 B** | S1-169 Scope Readiness = **READY** |
| **E1** | V2A-42 校正 = **阻塞** |
| **E3** | backend/ 实际创建 = **阻塞** |
| **E4** | Production Implementation Contract 完整建立 = **阻塞** |
| **E5** | DEFAULT-01~05 实际运行 = **阻塞** |
| **E7** | IGNORE_TABLES 完整清单 = **阻塞** |
| **E8** | 生产数据库环境就绪 = **阻塞** |

### 4.2 矛盾分析

**【S1-170B 显式判断】**:

S1-170A §11.2 结论 B 说"S1-169 Scope READY",同时 §12 Entry Conditions 列出 6 个阻塞条件。这两个结论在表面上看是矛盾的:

- **如果 S1-169 真正 READY**,就不应该有这么多阻塞条件
- **如果有这么多阻塞条件**,就不应该宣称 READY

**但 S1-170A 没有区分 Readiness Layer**——它使用单一的 READY 标签,既指 Effective Spec 层面的 SPEC-READY,又隐含 Implementation Entry Ready。

### 4.3 S1-170B 重新定义 S1-169 Readiness

**【S1-170B 显式】** 根据 §3 建立的 5 层 Readiness:

| Layer | S1-169 当前状态 |
|---|:-:|
| **SPEC-READY** | ✓ READY(Effective Spec 完整)|
| **CONTRACT-READY** | ⚠️ **部分 READY**(仅 user_company 部分有 Implementation Contract)|
| **IMPLEMENTATION-READY** | ✗ NOT ESTABLISHED(E1/E3/E4/E5/E7/E8 阻塞)|
| **PRODUCTION-READY** | ✗ NOT ESTABLISHED |
| **RUNTIME-VERIFIED** | ✗ NOT ESTABLISHED |

### 4.4 S1-170A 矛盾解决方案

**【S1-170B 显式建议】** S1-170A §11.2 结论 B 应改为:

> **S1-169 SPEC-READY** = READY
> **S1-169 CONTRACT-READY** = CONDITIONAL(仅 user_company 部分冻结)
> **S1-169 IMPLEMENTATION-READY** = NOT ESTABLISHED(E1/E3/E4/E5/E7/E8 阻塞)

### 4.5 S1-170A §12.1"禁止进入 S1-171"是否成立?

**【S1-170B 显式】**:
- S1-170A §12.1 说"当前禁止进入 S1-171"
- 但 §11.2 结论 B 又说"S1-169 Scope READY"
- **禁止进入 S1-171 与 Scope READY 表面矛盾**

**解决方案**:
- Scope READY 指 SPEC-READY + 部分 CONTRACT-READY
- 禁止进入 S1-171 是因为 IMPLEMENTATION-READY = NOT ESTABLISHED
- **两者不矛盾**,只需要明确分层

### 4.6 P1-06:READY / BLOCKER 逻辑冲突风险登记

**【S1-170B 显式】** 这是一个新的 P1 风险(老板指令 §6 显式建议编号 P1-06):

| 编号 | 风险 |
|---|---|
| **P1-06** | S1-170A §11.2 结论 B "S1-169 Scope READY" 与 §12 Entry Conditions 6 个阻塞条件在表层逻辑上冲突,且未使用 5 层 Readiness 分层 |

**严重度**:**高**(影响 S1-170A 作为开发闸门的可信度)

**解决**:补充 5 层 Readiness 分层(§3),并将 §11.2 结论 B 改为多 Layer 表达(§4.4)

---

## §5. V2A-42 风险重复登记审计

### 5.1 S1-170A 当前 V2A-42 风险登记

**【S1-170B 显式】** S1-170A 同时列出:

| 编号 | 风险描述 | 严重度 |
|---|---|:-:|
| **P1-02** | V2A-42 §5.2 把 OpenJDK 内部结构表述为普遍规范 + §5.7 GC eligibility 三条件混淆 GC eligibility 与 GC 执行 | 高 |
| **P2-01** | V2A-42 疑点一(GC eligibility 三条件混淆 GC eligibility 与 GC 执行)| 中 |
| **P2-02** | V2A-42 疑点二(OpenJDK 内部结构表述为普遍规范)| 中 |

### 5.2 重复登记分析

**【S1-170B 关键发现 N3】** P1-02 与 P2-01 / P2-02 是**完全重复登记**:

| 风险点 | P1-02 | P2-01 | P2-02 |
|---|:-:|:-:|:-:|
| §5.7 GC eligibility 三条件 | ✓ 包含 | ✓ 相同 | — |
| §5.2 OpenJDK 内部结构 | ✓ 包含 | — | ✓ 相同 |

**【S1-170B 显式判断】**:
- P2-01 与 P1-02 第一项**完全相同**(GC eligibility 三条件)
- P2-02 与 P1-02 第二项**完全相同**(OpenJDK 内部结构)
- **P1-02 与 P2-01/P2-02 是同一具体缺陷的不同层级表达**

### 5.3 父子风险关系建议

**【S1-170B 显式建议】** 应建立清晰的父子风险关系:

```
P1-02 (主风险): "V2A-42 存在未闭环的语义错误"
├── P2-01 (子问题): 具体语义错误一(GC eligibility 三条件)
└── P2-02 (子问题): 具体语义错误二(OpenJDK 内部结构表述)
```

这样:
- **P1 总数 = 5**(不增加新 P1)
- **P2 总数 = 4**(其中 P2-01/P2-02 是 P1-02 的子项,不重复计数)
- **风险总数 = 5 + 2**(P1 数 + 真正独立 P2 数)

### 5.4 P2-03 / P2-04 与 P1-01 关系

**【S1-170B 显式】**:

| 风险点 | P1-01 | P2-03 | P2-04 |
|---|:-:|:-:|:-:|
| S1-170 审计对象集合不完整 | ✓ 包含 | — | — |
| S1-170 §7.2 "41 份 S1-169-1 补丁"实际 36 份 | — | ✓ 包含 | — |
| S1-170 §2.1 "60 份 S1-169"实际 51 份 | — | — | ✓ 包含 |

**【S1-170B 判断】**:
- P2-03 和 P2-04 是 P1-01 的**具体表现**,不是独立风险
- P2-03 / P2-04 应作为 P1-01 的子项

### 5.5 修正后 P1/P2 计数

**【S1-170B 显式】**:

| 类别 | 修正前 | 修正后 |
|---|---:|---:|
| **P1 总数** | 5 | **5**(不变)|
| **P2 总数** | 4 | **2**(去除 P2-01/P2-02 的独立计数;P2-03/P2-04 归入 P1-01 子项)|
| **风险总数** | 9 | **5 + 2 = 7** |

### 5.6 风险登记修正表

| 编号 | 风险描述 | 严重度 | 父子关系 |
|---|---|:-:|---|
| **P1-01** | S1-170 审计对象集合不完整 + 漏审计 232~238 + 20x~22x | 高 | 主风险 |
| **P1-02** | V2A-42 存在未闭环的语义错误 | 中 | 主风险 |
| **P1-03** | F4 ≥80% 错误归类 | 高 | 主风险 |
| **P1-04** | API / Object / State 统计严重错误 | 高 | 主风险 |
| **P1-05** | S1-169 scope vs Project scope 范围错配 | 高 | 主风险 |
| **P1-06**(新)| S1-170A §11.2 结论 B 与 §12 Entry Conditions 逻辑冲突 + 缺乏 5 层 Readiness 分层 | 高 | 主风险 |
| **P2-01**(子)| V2A-42 §5.7 GC eligibility 三条件混淆 | 中 | **P1-02 子项** |
| **P2-02**(子)| V2A-42 §5.2 OpenJDK 内部结构表述 | 中 | **P1-02 子项** |
| **P2-03**(子)| S1-170 §7.2 数字 41 实际 36 | 低 | **P1-01 子项** |
| **P2-04**(子)| S1-170 §2.1 数字 60 实际 51 | 低 | **P1-01 子项** |

---

## §6. Effective Spec Coverage 重新审查

### 6.1 S1-170A §7.2 / §11.2 原文

**【S1-170A §11.2 C】**:
> 整个项目 Effective Spec 已完整冻结(12 Object + 40 API + 4 状态机 29 状态 + 31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE)

### 6.2 证据范围分析

**【S1-170B 显式】** "整个项目 Effective Spec 已完整冻结"需要分层分析:

#### 6.2.1 可以证明的

| 类别 | 证据 | 状态 |
|---|---|---|
| 12 Object 核心定义 | 238 §2 + 229 §4.1 | ✓ Confirmed |
| 40 API 字段级契约 | 232 §1 + 233 | ✓ Confirmed |
| 4 状态机 29 状态 | 229 §4.2 | ✓ Confirmed |
| 31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE | 236B §1.1 | ✓ Confirmed |
| UserCompany exactly-one | 241V2A-11 §4 | ✓ Confirmed |
| 异常体系 | 241V2A-17 / 18 | ✓ Confirmed |
| DEFAULT-01~05 测试设计 | 241V2A-5 / 14 / 15 | ✓ Confirmed |

#### 6.2.2 不能自动证明的

| 类别 | 证据 | 状态 |
|---|---|---|
| **所有历史规格都已统一** | ⚠️ S1-170A 未审计 234A / 234B / 234 / 235A / 235 等 | ✗ **Not Yet Audited** |
| **所有模块规格都无冲突** | ⚠️ 232 vs 233 已修正,229 vs 228 已修正,但跨文档冲突未完整审计 | ✗ **Not Yet Audited** |
| **所有引用关系都已经闭环** | ⚠️ S1-170A 未审计 20x~22x 领域的跨对象引用 | ✗ **Not Yet Audited** |
| **所有废止关系都已经闭环** | ⚠️ 226 vs 227 vs 228 vs 229 已有废止声明,但完整废止链路未审计 | ✗ **Not Yet Audited** |
| **所有 Phase 1 页面字段都已经完成证据闭环** | ⚠️ 88 页面 26 项字段中仅 21 个已观察 | ✗ **Not Yet Audited** |
| **所有实施边界都已经形成 Implementation Contract** | ⚠️ 仅 user_company 部分冻结 | ✗ **Not Yet Audited** |

### 6.3 Effective Spec Coverage Status(S1-170B 显式建立)

**【S1-170B 显式】** 不使用模糊的"完整冻结",必须使用以下分级:

| Coverage Status | 定义 | 当前应用范围 |
|---|---|---|
| **Confirmed Complete** | 多份 MD 显式冻结 + 五级证据体系确认 + 跨文档一致性审计通过 | 12 Object / 40 API / 4 状态机 / DDL / Tenant / UserCompany |
| **Confirmed Partial** | 部分子领域冻结,部分仍待审计 | 跨文档冲突 / 引用关系 / 废止关系 |
| **Not Yet Audited** | S1-170A 审计范围未覆盖 | Phase 1 页面字段 / Implementation Contract / Production Implementation |
| **Conflicting** | 跨文档存在未关闭冲突 | (经 S1-170A 审计无重大冲突,但 234A / 234B 未审计)|
| **Not Applicable** | 不适用于当前 Phase 1 范围 | (不适用)|

### 6.4 "整个项目 Effective Spec 已完整冻结"的校正

**【S1-170B 显式】** S1-170A §11.2 表述应改为:

> **核心领域 Effective Spec 已 Confirmed Complete**(12 Object + 40 API + 4 状态机 29 状态 + DDL + Tenant + UserCompany + 异常体系 + DEFAULT 测试设计)
>
> **整个项目 Effective Spec 整体状态 = Confirmed Partial**(核心领域完整,但跨文档一致性 / 引用闭环 / 废止闭环 / Phase 1 页面字段 / Implementation Contract 仍待审计)

**严格区分**:
- ✓ "核心领域 Effective Spec 已 Confirmed Complete"
- ⚠️ "整个项目 Effective Spec 整体状态 = Confirmed Partial"

---

## §7. Implementation Contract Coverage 重新审查

### 7.1 S1-170A §7.3 / §11.2 原文

**【S1-170A §7.3 Implementation Contract】**:
> Implementation Contract | 部分冻结 | 待 backend/ 实施时建立

### 7.2 Implementation Contract 严格定义

**【S1-170B 显式】** Implementation Contract 必须至少说明:

1. 要实现什么(Object / API / State / DDL)
2. 在哪个代码层(Entity / Mapper / Service / Controller / DTO / VO)
3. 对应哪些 Entity / Mapper / Service / Controller 类名
4. 输入输出(Request / Response 字段级)
5. transaction(Spring @Transactional 边界)
6. security(权限角色 / Sa-Token 注解)
7. tenant(CompanyContext / TenantLineInnerInterceptor)
8. error(异常类 + 错误码 + HTTP 状态)
9. test(单元测试 / 集成测试 / DEFAULT-01~05)
10. acceptance criteria(冻结的断言 / 验收标准)

### 7.3 Implementation Contract Coverage 矩阵

**【S1-170B 显式建立】**:

| 项目 | Effective Spec | Implementation Contract |
|---|---|---|
| **Object** | ✓ Confirmed(238 §2 12 Object 冻结)| ⚠️ 部分(仅 user_company 字段级 schema + CompanyContext 设计)|
| **API** | ✓ Confirmed(232 + 233 40 API 字段级契约)| ⚠️ 部分(仅 Request / Response 字段级,但缺 Entity / Mapper / Service / Controller 类名)|
| **State** | ✓ Confirmed(229 §4.2 4 状态机 29 状态)| ⚠️ 部分(状态机设计,但缺 Service 层状态转换实现细节)|
| **DDL** | ✓ Confirmed(236B §4 12 表 31 FK)| ⚠️ 部分(Flyway V1__init_v44_base.sql 设计但未实施)|
| **Tenant** | ✓ Confirmed(241V2 §4-6 CompanyContext + TenantLineInnerInterceptor)| ⚠️ 部分(241V2 §5.4 双层防御 + 状态机,但缺实际类路径与包结构)|
| **Exception** | ✓ Confirmed(241V2A-17 / 18 9 异常 + 8 @ExceptionHandler)| ⚠️ 部分(异常类设计,但缺 GlobalExceptionHandler 完整路径)|
| **Security** | ✓ Confirmed(241 §4.5 60000-60004 错误码)| ⚠️ 部分(错误码设计,但缺 Sa-Token 注解与权限角色映射)|
| **Test** | ✓ Confirmed(241V2A-5 / 14 / 15 DEFAULT-01~05)| ⚠️ 部分(测试设计,但缺实际 JUnit 类名 + 测试运行验证)|

### 7.4 Implementation Contract 当前真实状态

**【S1-170B 显式】**:

```
Implementation Contract = NOT ESTABLISHED(部分冻结,但未达到可直接编码粒度)
```

理由:
- 仅有 Effective Spec + 部分设计层契约
- 缺:具体 Java 类路径 / Entity / Mapper / Service / Controller 完整字段映射
- 缺:Spring @Transactional 边界精确划分
- 缺:Sa-Token 注解与权限角色精确映射
- 缺:Flyway V1 SQL 文件实际内容
- 缺:实际 JUnit 测试类

### 7.5 S1-170A §7.3 / §11.2 表述校正

**【S1-170B 显式】**:
- "Implementation Contract = 部分冻结" **不准确**——"部分冻结"暗示部分领域已 CONTRACT-READY
- 应改为:
  > Implementation Contract = **NOT ESTABLISHED**(当前仅有 Effective Spec + 部分设计层契约,未达到可直接编码粒度)

---

## §8. F4 Scope-dependent Prerequisite 校正审查

### 8.1 S1-170A §4.4.4 校正结果

**【S1-170A §4.4.4】**:F4 从 Hard blocker 改为 Scope-dependent prerequisite。

### 8.2 S1-170B 独立审计

**【S1-170B 显式】** Phase 1 Scope-dependent prerequisite 需要实际证据:

#### 8.2.1 Phase 1 范围页面清单

根据老板指令 §6:**Phase 1 正式范围 = 诊所管理 + 系统设置**

| 范围 | 页面 | 数量 | 侦察状态 |
|---|---|---:|---|
| 诊所管理 | PAGE-801 ~ 811 | 11 | 100%(00_项目总索引 §"8️⃣ 诊所管理")|
| 系统设置 | PAGE-9A.1 ~ 9I.20 | 约 35+ | **未单独审计** |
| **Phase 1 合计** | | **≈ 46** | **未单独审计** |

#### 8.2.2 实际数字

**【S1-170B 显式】**:
- 诊所管理 11 个页面 = **100%** 已确认(00_项目总索引)
- 系统设置 35+ 个子页面 = **未单独审计具体进度**
- **Phase 1 整体侦察进度 = NOT ESTABLISHED**(因为系统设置未单独审计)

### 8.3 F4 当前真实状态

**【S1-170B 显式】**:

| 范围 | F4 实际状态 |
|---|:-:|
| 全项目 96 页面 | ⚠️ 47%(S1-170A §4.2)|
| 诊所管理 11 页面 | ✓ 100% |
| 系统设置 35+ 页面 | ⚠️ **Not Yet Audited** |
| Phase 1 整体(诊所管理 + 系统设置) | ⚠️ **Not Yet Audited** |

### 8.4 F4 校正建议

**【S1-170B 显式】**:

F4 应分为:
- **F4.1 全项目 ≥80%**:Hard blocker?→ **否**(无证据支持是 hard blocker)
- **F4.2 Phase 1 ≥80%**:Scope-dependent prerequisite?→ **待审计**(系统设置未单独审计)

**最终判断**:
- F4.1(全项目)→ ✗ **NOT ESTABLISHED**(没有证据证明是 hard blocker)
- F4.2(Phase 1)→ ⚠️ **PARTIAL**(诊所管理 100%,系统设置未单独审计)

---

## §9. 三个 Final Decision 重新审查

### 9.1 S1-170A §11.2 原文

| Decision | 当前状态 | 定义 |
|---|---|---|
| **A**:S1-170 Audit Validity | FAIL | S1-170 审计报告自身 |
| **B**:S1-169 Scope Readiness | READY | S1-169 范围 |
| **C**:OptFlow PMS Phase 1 Development Readiness | CONDITIONAL | 整个项目 |

### 9.2 S1-170B 重新给出(基于 5 层 Readiness)

#### 9.2.1 Decision A:S1-170 Audit Validity

**【S1-170B 显式】**:**FAIL**

理由:
- 数字错误(60 / 65 / 41)
- 范围错配(S1-169 scope vs Project scope)
- 统计口径错误(API / Object / State)
- F4 错误分类
- **本轮新增**:S1-170A 自身出现"前文修正了,后文仍使用旧数字"的问题(§11.2 "41 份"残留)

#### 9.2.2 Decision B:S1-169 Specification Readiness

**【S1-170B 显式】**:**READY**

定义:**SPEC-READY** = S1-169 范围内核心 Effective Spec 已冻结

证据:
- 36 份 P1/P2 修复 + 7 份 P2 关闭
- 五级证据体系完整(241V2A-19)
- P0 = 0 / P1 = 0
- P2-0/1/2 = CLOSED(Effective Spec)
- UserCompany exactly-one 业务规则冻结

**未达成**:CONTRACT-READY / IMPLEMENTATION-READY / PRODUCTION-READY / RUNTIME-VERIFIED

#### 9.2.3 Decision C:S1-169 Implementation Entry Readiness

**【S1-170B 显式新增】**:**NOT ESTABLISHED**

定义:**IMPLEMENTATION-READY** = 允许开始 backend/ 实施

证据:
- ✗ E1 V2A-42 校正未完成
- ✗ E3 backend/ 未创建
- ✗ E4 Production Implementation Contract 未完整建立
- ✗ E5 DEFAULT-01~05 未实际运行
- ✗ E7 IGNORE_TABLES 完整清单未核验
- ✗ E8 生产数据库环境未确认

#### 9.2.4 Decision D:Phase 1 Development Readiness

**【S1-170B 显式】**:**CONDITIONAL**

定义:**Phase 1 整体进入开发的准备度**

证据:
- ✓ 核心领域 Effective Spec Confirmed Complete
- ⚠️ Phase 1 整体侦察进度 Not Yet Audited(系统设置未单独审计)
- ⚠️ Implementation Contract 仅部分冻结
- ✗ Production Implementation = NOT YET STARTED
- ✗ Runtime Test Execution = NOT YET EXECUTED

---

## §10. S1-171 Entry Gate

### 10.1 S1-170A §12 Entry Conditions 重新审计

**【S1-170B 显式】** S1-170A §12.2 的 E1/E3/E4/E5/E7/E8 阻塞条件是否真正阻塞 S1-171?

| # | 条件 | 真正阻塞 IMPLEMENTATION-READY? |
|---:|---|:-:|
| **E1** | V2A-42 §5.2 / §5.7 疑点一、二进一步校正 | ⚠️ 见 §10.2 详细分析 |
| **E3** | backend/ 实际创建 + pom.xml + application.yml | ✓ 阻塞(没有 backend/ 无法实施)|
| **E4** | Production Implementation Contract 完整建立 | ✓ 阻塞(仅 user_company 部分冻结)|
| **E5** | DEFAULT-01~05 实际运行 + 测试通过 | ✓ 阻塞(测试未运行)|
| **E7** | IGNORE_TABLES 完整清单 | ✓ 阻塞(只有分类原则,具体清单待核验)|
| **E8** | 生产数据库环境就绪 | ✓ 阻塞(未确认)|

### 10.2 E1 为什么阻塞(深入分析)

**【S1-170B 显式】** S1-170A 自身矛盾:
- §11.2 结论 B 说"V2A-42 疑点不影响 P2-2 KEEP 裁决"
- §12.2 E1 说"V2A-42 校正 = 阻塞"

这两个表述表面矛盾。需要明确:

**【S1-170B 显式判断】**:

| 视角 | E1 是否阻塞 |
|---|:-:|
| **Effective Spec 层** | ✗ 不阻塞(已 SPEC-READY)|
| **Implementation Contract 层** | ⚠️ **部分阻塞**(V2A-42 疑点可能进入 Implementation Contract)|
| **IMPLEMENTATION-READY 层** | ⚠️ **条件性阻塞** |

**具体分析**:
- V2A-42 §5.2(OpenJDK 内部结构)→ **如果** 实施时引用 OpenJDK 内部结构作为"普遍规范",**会**误导实施
- V2A-42 §5.7(GC eligibility 三条件)→ **如果** 实施时把 GC eligibility 与 GC 执行混淆,**会**导致 lifecycle 测试语义错误
- 因此 E1 阻塞的是 **CONTRACT-READY**(因为 V2A-42 疑点可能进入 Implementation Contract)
- E1 不应作为 **IMPLEMENTATION-READY** 的绝对阻塞(可以在 Implementation Contract 中通过限定性引用隔离)

**【S1-170B 显式建议】**:
- E1 重新归类为 **CONTRACT-READY 的部分阻塞**
- 不应作为 IMPLEMENTATION-READY 的绝对 blocker
- 在进入 S1-171 时,**首先**完成 V2A-42 校正(避免误传入 Implementation Contract),**然后**允许进入 S1-171

### 10.3 E1 严重度重新评估

**【S1-170B 显式】**:
- 原严重度:**阻塞**(S1-170A §12.2)
- 校正严重度:**部分阻塞**(仅 CONTRACT-READY 阻塞,非绝对)

**【S1-170B 显式判断 E1 的两种合法场景】**:

| 场景 | 判断 |
|---|---|
| **A. 该语义问题必须进入 Implementation Contract 前关闭** | ✓ 阻塞 CONTRACT-READY |
| **B. 该语义问题仅属于历史文档文字问题,不进入 Implementation Contract** | ✗ 不阻塞任何层 |

**【S1-170B 显式】** 实际属于场景 A(因为 V2A-42 §5.2 / §5.7 都是 Effective Spec 层的语义错误,**会**进入 Implementation Contract)→ **必须阻塞 CONTRACT-READY**。

### 10.4 S1-171 是否允许进入?

**【S1-170B 显式】**:
- IMPLEMENTATION-READY = NOT ESTABLISHED(因为多个 E 条件阻塞)
- 但 S1-171 = "开发前总闸门审计"(S1-170A 标题),**不是开发实施**
- 如果 S1-171 是**审计 / 准备工作**(如创建 V2A-43 / V2A-44 校正补丁 / 准备 Production Implementation Contract),**允许进入**
- 如果 S1-171 是**实际 backend/ 实施**,**不允许进入**

**【S1-170B 显式】**:S1-171 的具体定位决定了是否能进入:
- 如果 S1-171 = "创建 V2A-43 / V2A-44 / 准备 Implementation Contract 草案",**ALLOW**
- 如果 S1-171 = "实际 backend/ 编码",**BLOCK**

**老板必须明确 S1-171 的具体定位**,S1-170B 不能默认决定。

---

## §11. P1/P2 风险最终清单

### 11.1 P1 风险(5 项 + 1 新增)

| # | 风险 | 严重度 | 来源 | 父子关系 |
|---:|---|:-:|---|---|
| **P1-01** | S1-170 审计对象集合不完整 + 漏审计 232~238 + 20x~22x | 高 | S1-170A §10.1 | 主风险(含 P2-03/P2-04 子项)|
| **P1-02** | V2A-42 存在未闭环的语义错误 | 中 | S1-170A §10.1 | 主风险(含 P2-01/P2-02 子项)|
| **P1-03** | F4 ≥80% 错误归类 | 高 | S1-170A §10.1 | 主风险 |
| **P1-04** | API / Object / State 统计严重错误 | 高 | S1-170A §10.1 | 主风险 |
| **P1-05** | S1-169 scope vs Project scope 范围错配 | 高 | S1-170A §10.1 | 主风险 |
| **P1-06**(新)| S1-170A 自身数字残留 + 缺乏 5 层 Readiness 分层 + §11.2 结论 B 与 §12 Entry Conditions 逻辑冲突 | 高 | **S1-170B 新增** | 主风险 |

### 11.2 P2 风险(2 项独立 + 4 项子项)

| # | 风险 | 严重度 | 父子关系 |
|---:|---|:-:|---|
| **P2-01** | V2A-42 §5.7 GC eligibility 三条件混淆 GC eligibility 与 GC 执行 | 中 | **P1-02 子项** |
| **P2-02** | V2A-42 §5.2 OpenJDK 内部结构表述为普遍规范 | 中 | **P1-02 子项** |
| **P2-03** | S1-170 §7.2 数字 41 实际 36 | 低 | **P1-01 子项** |
| **P2-04** | S1-170 §2.1 数字 60 实际 51 | 低 | **P1-01 子项** |

### 11.3 风险计数

- **P1 总数**:6 项
- **P2 总数**:2 项独立 + 4 项子项
- **独立风险总数**:6 + 2 = **8 项**

---

## §12. Evidence Index

| 关键结论 | 文件 | 章节 / 行号 |
|---|---|---|
| S1-170A §11.2 结论 B "41 份"数字残留 | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md` | §11.2 |
| S1-170A §7.3 Implementation Contract 表述 | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md` | §7.3 |
| S1-170A §11.2 结论 C "整个项目 Effective Spec 已完整冻结" | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md` | §11.2 C |
| S1-170A §12.2 E1 严重度 | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md` | §12.2 |
| 12 Object 完整冻结 | `238_S1-169_实施前置映射基线.md` | §2.1 + §2.2 |
| 4 状态机 29 状态 | `229_S1-166A_门诊预约接诊领域模型状态机二次修正版.md` | §4.2 |
| 40 API 字段级契约 | `232_S1-167_40个API字段级设计.md` | §1 40 API 总表 |
| 31 真 FK 关系矩阵 | `236B_S1-168_DDL修正版_文字纠错.md` | §1.1 + §5 |
| V2A-42 疑点一(GC eligibility 三条件) | `241V2A-42_S1-169-2_P2-2_JavaExecutor生命周期语义二次校正补丁.md` | §5.7 |
| V2A-42 疑点二(OpenJDK 内部结构) | `241V2A-42_S1-169-2_P2-2_JavaExecutor生命周期语义二次校正补丁.md` | §5.2 |
| 诊所管理 100% 已侦察 | `00_项目总索引.md` | §"8️⃣ 诊所管理" |
| 系统设置侦察进度未单独审计 | `00_项目总索引.md` | §"⚙️ 系统设置" |
| Phase 1 范围 = 诊所管理 + 系统设置 | 老板指令 §6 | (本审计引用)|

---

## §13. Final Verdict

### 13.1 五项判定

#### A. S1-170A Audit Validity

**FAIL**

**定义**:S1-170A 自身作为审计报告的有效性。

**证据依据**:
- S1-170A 内部数字残留(§11.2 "41 份" 应为 36 份)
- S1-170A §11.2 结论 B 与 §12 Entry Conditions 逻辑冲突
- S1-170A 缺乏 5 层 Readiness 分层
- S1-170A §7.3 "Implementation Contract 部分冻结" 不准确(应为 NOT ESTABLISHED)
- S1-170A §11.2 结论 C "整个项目 Effective Spec 已完整冻结" 超过证据范围(应为 Confirmed Partial)

#### B. S1-169 Specification Readiness

**READY**

**定义**:**SPEC-READY** = S1-169 范围内核心 Effective Spec 已冻结

**证据依据**:
- 36 份 P1/P2 修复 + 7 份 P2 关闭(全部 CLOSED in Effective Spec)
- 五级证据体系完整(241V2A-19)
- P0 = 0 / P1 = 0
- P2-0/1/2 = CLOSED(Effective Spec)
- UserCompany exactly-one 业务规则冻结(241V2A-11 §4)
- DEFAULT-01~05 测试设计冻结(241V2A-5 / 14 / 15)

#### C. S1-169 Implementation Entry Readiness

**NOT ESTABLISHED**

**定义**:**IMPLEMENTATION-READY** = 允许开始 backend/ 实际编码实施

**证据依据**:
- ✗ V2A-42 §5.2 / §5.7 疑点未关闭(E1 阻塞 CONTRACT-READY)
- ✗ backend/ 未创建(E3)
- ✗ Production Implementation Contract 仅 user_company 部分冻结(E4)
- ✗ DEFAULT-01~05 未实际运行(E5)
- ✗ IGNORE_TABLES 完整清单未核验(E7)
- ✗ 生产数据库环境未确认(E8)

#### D. Phase 1 Development Readiness

**CONDITIONAL**

**定义**:Phase 1 范围(诊所管理 + 系统设置)进入开发的整体准备度

**证据依据**:
- ✓ 核心领域 Effective Spec Confirmed Complete(12 Object + 40 API + 4 状态机 + DDL + Tenant + UserCompany)
- ✓ 诊所管理(PAGE-801 ~ 811)100% 侦察
- ⚠️ 系统设置(PAGE-9A.1 ~ 9I.20)侦察进度未单独审计
- ⚠️ Implementation Contract 仅 user_company 部分冻结
- ✗ Production Implementation = NOT YET STARTED
- ✗ Runtime Test Execution = NOT YET EXECUTED

#### E. S1-171

**CONDITIONAL**

**定义**:S1-171 是否允许进入(取决于 S1-171 的具体定位)

**证据依据**:
- 如果 S1-171 = "创建 V2A-43 / V2A-44 / 准备 Implementation Contract 草案" → **ALLOW**(这是 SPEC-READY 范围内的继续工作)
- 如果 S1-171 = "实际 backend/ 编码" → **BLOCK**(IMPLEMENTATION-READY = NOT ESTABLISHED)

**S1-171 是否允许取决于老板对其具体定位的明确**。

### 13.2 P1/P2 数量

- **P1 总数**:6 项(P1-01 ~ P1-06,P1-06 为本轮新增)
- **P2 独立总数**:2 项
- **P2 子项总数**:4 项
- **独立风险总数**:8 项

### 13.3 S1-171 是否允许

**CONDITIONAL**(取决于老板对 S1-171 具体定位)

### 13.4 真正阻塞条件

| # | 条件 | 真正阻塞的 Layer | 严重度 |
|---:|---|---|:-:|
| **E1** | V2A-42 §5.2 / §5.7 疑点进一步校正(V2A-43 / V2A-44)| **CONTRACT-READY**(部分)| 高 |
| **E3** | backend/ 实际创建 + pom.xml + application.yml | **IMPLEMENTATION-READY** | 高 |
| **E4** | Production Implementation Contract 完整建立(对应 12 Object + 40 API)| **CONTRACT-READY** | 高 |
| **E5** | DEFAULT-01~05 实际运行 + 测试通过 | **RUNTIME-VERIFIED** | 高 |
| **E7** | IGNORE_TABLES 完整清单(基于 Phase 1 范围 12 表)| **CONTRACT-READY** | 中 |
| **E8** | 生产数据库环境就绪 | **IMPLEMENTATION-READY** | 高 |

### 13.5 S1-171 允许的边界

如果 S1-171 是以下任一,**ALLOW**:
- ✓ 创建 V2A-43 / V2A-44 等校正补丁(完成 E1)
- ✓ 准备 Production Implementation Contract 草案(完成 E4)
- ✓ IGNORE_TABLES 完整清单核验(完成 E7)
- ✓ 系统设置侦察进度单独审计(完成 F4.2)

如果 S1-171 是以下任一,**BLOCK**:
- ✗ 直接开始 backend/ 实际编码
- ✗ 修改 pom.xml / application.yml
- ✗ 执行 DDL / 连接数据库
- ✗ 创建 backend/ 目录

---

## §14. 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\S1-170B_Pre-Development_Integrity_Audit_自身一致性闸门审计.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | `S1-170A_Pre-Development_Integrity_Audit_校正报告.md`(不修改)|
| 严禁修改 | S1-170A / S1-170 / 任何历史 MD / 源码 / 数据库 |

---

**End of S1-170B**
