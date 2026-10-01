# S1-170C｜Readiness 生命周期与 Entry Gate 语义校正

---

## §0. Metadata

| 字段 | 内容 |
|---|---|
| Audit ID | S1-170C |
| Audit Date | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Audit Target | S1-170B 已建立的 Readiness Vocabulary + E1 / E3 / E4 / E5 / E7 / E8 层级分类 |
| Base | `S1-170B_Pre-Development_Integrity_Audit_自身一致性闸门审计.md`(不修改)|
| Scope | 重新定义 7 层 Readiness 生命周期 + 审计 E 条件层级分类 + 检测循环依赖 |
| 严禁 | 修改任何历史 MD / 修改源码 / 创建 backend / 创建 S1-171 / 创建 V2A-43 / commit / push |

---

## §1. Audit Objective

### 1.1 唯一核心问题

> **S1-170B 已建立的 Readiness Vocabulary 是否被 E 条件错放层级或形成循环依赖?**

### 1.2 最高优先原则

> **"一个阶段的进入条件,不能依赖只有进入该阶段之后才能产生的结果。"**

### 1.3 必须审计的 6 个 E 条件

| E 条件 | 来源 |
|---|---|
| **E1** V2A-42 §5.2 / §5.7 疑点进一步校正 | S1-170B §13.4 |
| **E3** backend/ 创建 + pom.xml + application.yml | S1-170B §13.4 |
| **E4** Production Implementation Contract 完整建立 | S1-170B §13.4 |
| **E5** DEFAULT-01~05 实际运行 + 测试通过 | S1-170B §13.4 |
| **E7** IGNORE_TABLES 完整清单 | S1-170B §13.4 |
| **E8** 生产数据库环境就绪 | S1-170B §13.4 |

### 1.4 严禁项

- ✗ 不修改 S1-170B / S1-170A / S1-170 / 任何历史 MD
- ✗ 不修改源码 / 数据库
- ✗ 不创建 backend / pom.xml / application.yml / V2A-43 / S1-171
- ✗ 不执行 DDL / 不连接数据库 / 不运行测试
- ✗ 不 commit / push

---

## §2. 7 层 Readiness 生命周期(重新定义)

### 2.1 L1 SPEC-READY

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | 当前有效 Effective Spec 已冻结到足以作为实施来源 |
| **必须包含** | 适用范围内的 Object / API / State / DDL / Tenant / Security / Exception / Test Design / Acceptance Criteria |
| **验证手段** | 多份 MD 显式冻结 + 五级证据体系 + 跨文档一致性审计 |
| **不要求** | 代码存在 / 测试运行 / 数据库存在 / 实施产物 |
| **关键边界** | SPEC-READY ≠ 代码存在 |

**【S1-170C 显式】**:SPEC-READY 是**静态规格冻结**的判定,与任何实施产物无关。

### 2.2 L2 CONTRACT-READY

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | Implementation Contract 已达到"可以直接指导编码"的粒度 |
| **必须包含** | Object → Entity / API → Controller+DTO+VO / Repository+Mapper / Service / transaction 边界 / tenant 边界 / security+role / error+exception / test mapping / acceptance criteria / 文件路径+包结构 / 关键方法签名 |
| **验证手段** | 字段级映射文档 + Spring Boot 工程结构文档 + 实施契约清单 |
| **关键边界** | 普通业务设计文档 ≠ Implementation Contract |

**【S1-170C 显式】**:CONTRACT-READY 必须**所有 12 项**都已冻结到粒度,**不**接受"部分冻结"模糊表述。

### 2.3 L3 IMPLEMENTATION-ENTRY-READY

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | 所有"开始编码之前"的真正前置条件已经满足,因此允许创建 backend 目录并开始实施 |
| **核心原则** | **PRE-ENTRY CONDITIONS MUST BE OBSERVABLE BEFORE ENTRY** |
| **不要求** | 代码已存在 / 测试已运行 / 数据库已存在 / backend 已创建 |
| **关键边界** | **进入 L3 之前,所有 Required 条件必须能够在"不执行实际实施"的情况下被验证** |

**【S1-170C 严禁】**:**实施开始以后才能产生的结果不能作为 L3 的前置条件**(包括代码、backend 目录、测试结果、生产部署、数据库迁移)。

### 2.4 L4 IMPLEMENTATION-IN-PROGRESS

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | backend、代码、配置、迁移脚本、测试代码等已经开始实际创建和实施 |
| **允许动作** | 创建 backend / 创建 pom.xml / 创建 application.yml / 创建 Entity / Mapper / Service / Controller / 创建 Flyway SQL / 创建 JUnit |
| **不要求** | 代码完成 / 编译通过 / 测试通过 / 生产部署 |
| **关键边界** | L4 = L3 + 实施动作 |

**【S1-170C 显式】**:L4 是 L3 的"开始实施"之后的执行阶段,**不是 L3 的前置条件**。

### 2.5 L5 IMPLEMENTATION-COMPLETE

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | Implementation Contract 中规定的代码范围已经实现,并满足静态 / 编译 / 代码检查要求 |
| **必须验证** | 所有 Entity / Mapper / Service / Controller 已实现 + 编译通过 + 无编译错误 + 代码检查通过 |
| **不要求** | 测试运行通过 / 生产部署完成 / 性能验证 |
| **关键边界** | L5 ≠ 测试通过 |

### 2.6 L6 PRODUCTION-READY

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | 代码、配置、数据库、部署环境达到可以进行生产部署 / 集成环境运行的条件 |
| **重点考虑** | 生产数据库环境 / application 配置 / 部署参数 / migration / 监控 / runtime dependencies |
| **不要求** | 测试实际运行通过(那是 L7)|
| **关键边界** | **生产数据库环境 ≠ 本地开发数据库** |

### 2.7 L7 RUNTIME-VERIFIED

**【S1-170C 显式定义】**

| 项 | 内容 |
|---|---|
| **定义** | 实际运行并完成规定测试,且通过验收标准 |
| **重点考虑** | DEFAULT-01~05 实际运行 / 集成测试 / 事务测试 / 并发测试 / Runtime verification |
| **关键边界** | **测试实际运行必须依赖已存在的实施产物(代码 / Service / Repository / 数据库)** |

**【S1-170C 显式】**:L7 的所有内容**必须**在 L5 / L6 完成之后才能开始。

### 2.8 7 层生命周期顺序

```
L1 SPEC-READY
    ↓
L2 CONTRACT-READY
    ↓
L3 IMPLEMENTATION-ENTRY-READY
    ↓
L4 IMPLEMENTATION-IN-PROGRESS
    ↓
L5 IMPLEMENTATION-COMPLETE
    ↓
L6 PRODUCTION-READY
    ↓
L7 RUNTIME-VERIFIED
```

**【S1-170C 显式】**:每个 L 层的进入条件**必须在上一层完成之后**才能被验证。任何把下层结果当作上层前置条件的设置都是**非法循环依赖**。

---

## §3. Gate Matrix 建立

### 3.1 Gate Matrix 完整定义

**【S1-170C 显式建立】** 每个格子只允许 **Required / Not Required / Result / N/A**:

| 条件 | L1 SPEC | L2 CONTRACT | L3 ENTRY | L4 IN-PROGRESS | L5 COMPLETE | L6 PROD | L7 RUNTIME |
|---|---|---|---|---|---|---|---|
| **Effective Spec 完整冻结** | **Required** | Not Required | Not Required | Not Required | Not Required | Not Required | Not Required |
| **Implementation Contract 完整建立** | N/A | **Required** | Not Required | Not Required | Not Required | Not Required | Not Required |
| **V2A-42 §5.2 / §5.7 疑点关闭** | Required | Not Required | Not Required | Not Required | Not Required | Not Required | Not Required |
| **backend/ 目录已存在** | Not Required | Not Required | **Not Required** | **Result** | Not Required | Not Required | Not Required |
| **pom.xml 已创建** | Not Required | Not Required | **Not Required** | **Result** | Not Required | Not Required | Not Required |
| **application.yml 已创建** | Not Required | Not Required | **Not Required** | **Result** | Not Required | Not Required | Not Required |
| **IGNORE_TABLES 静态清单冻结** | N/A | **Required** | Not Required | Not Required | Not Required | Not Required | Not Required |
| **IGNORE_TABLES 实际代码配置** | N/A | N/A | N/A | Not Required | **Result** | Not Required | Not Required |
| **DEFAULT-01~05 测试设计冻结** | Required | Not Required | Not Required | Not Required | Not Required | Not Required | Not Required |
| **DEFAULT-01~05 测试代码已创建** | N/A | N/A | N/A | Not Required | **Required** | Not Required | Not Required |
| **DEFAULT-01~05 测试实际运行** | Not Required | Not Required | **Not Required** | Not Required | Not Required | Not Required | **Result** |
| **DEFAULT-01~05 测试通过** | Not Required | Not Required | **Not Required** | Not Required | Not Required | Not Required | **Result** |
| **生产数据库环境就绪** | Not Required | Not Required | **Not Required** | Not Required | Not Required | **Required** | Not Required |
| **本地 / 测试数据库可访问** | N/A | N/A | Required | Not Required | Not Required | Not Required | Not Required |
| **代码完成 / 编译通过** | Not Required | Not Required | Not Required | Not Required | **Required** | Not Required | Not Required |
| **集成测试通过** | Not Required | Not Required | **Not Required** | Not Required | Not Required | Not Required | **Result** |
| **监控 / 部署参数就绪** | Not Required | Not Required | **Not Required** | Not Required | Not Required | Required | Not Required |

### 3.2 Gate Matrix 关键结论

**【S1-170C 关键发现 G1】**:基于 Gate Matrix,E 条件应该正确分类如下:

| E 条件 | 正确层级 | S1-170B 错误分类(如有)|
|---|---|---|
| **E1** V2A-42 校正 | **L1 SPEC-READY**(因为是 Effective Spec 错误)| (需重新审计)|
| **E3** backend/ 创建 | **L4 IN-PROGRESS 的第一步,不是 L3 前置** | (需重新审计)|
| **E4** Implementation Contract 完整建立 | **L2 CONTRACT-READY** | (需重新审计)|
| **E5** DEFAULT-01~05 实际运行 | **L7 RUNTIME-VERIFIED** | (需重新审计)|
| **E7** IGNORE_TABLES 静态清单 | **L2 CONTRACT-READY** | (需重新审计)|
| **E8** 生产数据库环境就绪 | **L6 PRODUCTION-READY** | (需重新审计)|

---

## §4. E1 核心审计:V2A-42 校正

### 4.1 V2A-42 两个疑点回顾

**【S1-170C 引用 S1-170A §3.6】**:

| 疑点 | 内容 |
|---|---|
| **疑点一**:GC eligibility 与 GC 执行时点混淆 | V2A-42 §5.7 GC eligibility 三条件中 "(c) JVM GC 调度器实际执行 GC" **混淆了 GC eligibility 与 GC 完成** |
| **疑点二**:OpenJDK ThreadPoolExecutor 内部结构不能泛化为 ExecutorService API 规范 | V2A-42 §5.2 把 OpenJDK 内部 HashSet<Worker> 表述为普遍规范,**越界** |

### 4.2 E1 阻塞层级严格审计

**【S1-170C 逐层回答】**:

| 问题 | 答案 | 依据 |
|---|---|---|
| **Q1**:E1 阻塞 L1 SPEC-READY 吗? | ⚠️ **部分** | V2A-42 是 Effective Spec 文档,疑点是 Effective Spec 错误。但 V2A-42 不在"核心 Effective Spec"中(P2-2 裁决已 CLOSED,KEEP 裁决稳定)。疑点仅影响 V2A-42 自身表述精度,**不**影响 P2-2 KEEP 实质裁决 |
| **Q2**:E1 阻塞 L2 CONTRACT-READY 吗? | ⚠️ **可能** | 如果 V2A-42 疑点进入 Implementation Contract(如 §5.2 OpenJDK 内部结构被引用),**可能**误导实施。**但**通过限定性引用隔离可以避免 |
| **Q3**:E1 阻塞 L3 IMPLEMENTATION-ENTRY-READY 吗? | ✗ **否** | E1 不是 IMPLEMENTATION-ENTRY-READY 的真正前置条件。SPEC-READY 已经在核心领域达成,V2A-42 疑点不影响 SPEC-READY 整体 |
| **Q4**:E1 阻塞 L5 IMPLEMENTATION-COMPLETE 吗? | ✗ **否** | E1 与代码完成 / 编译无关 |
| **Q5**:E1 阻塞 L6 PRODUCTION-READY 吗? | ✗ **否** | E1 与生产部署无关 |
| **Q6**:E1 阻塞 L7 RUNTIME-VERIFIED 吗? | ✗ **否** | E1 与测试运行无关(测试设计冻结在 L1,V2A-42 疑点不影响 DEFAULT-03 实质行为)|

### 4.3 E1 风险传递链

**【S1-170C 显式建立】**:

```
[V2A-42 §5.2 / §5.7 疑点]
    ↓
风险传递
    ↓
[Effective Spec 错误:V2A-42 文档表述精度问题]
    ↓
[可能影响 L2 CONTRACT-READY(如果进入 Implementation Contract)]
    ↓
[必须通过"限定性引用隔离"避免]
    ↓
[不阻塞 L3 / L5 / L6 / L7]
```

### 4.4 E1 真正严重度

**【S1-170C 显式重新分类 E1】**:

| 维度 | 评估 |
|---|---|
| **原始严重度(S1-170B §13.4)** | "高(阻塞)" |
| **S1-170C 重新分类** | "中(部分阻塞 L1,可能影响 L2,**不阻塞** L3)" |
| **理由** | V2A-42 疑点是 Effective Spec 表述精度问题,**不影响** P2-2 KEEP 实质裁决。通过 L2 的限定性引用隔离可以避免 |

### 4.5 E1 处理建议

**【S1-170C 显式】**:

1. **L1 SPEC-READY**:V2A-42 疑点不阻塞 SPEC-READY(因为核心 Effective Spec 已达成)
2. **L2 CONTRACT-READY**:在准备 Implementation Contract 时,**必须**对 V2A-42 §5.2 / §5.7 内容进行限定性引用
   - §5.2 OpenJDK 内部结构 → 明确标注"OpenJDK 实现证据,**非** Java API 普遍规范"
   - §5.7 GC eligibility 三条件 → 改为"GC eligibility 仅取决于无 GC root 可达;JVM GC 时点不可预测"
3. **是否需要创建 V2A-43 / V2A-44 校正**:可以作为 L2 阶段的审计工作,**不阻塞 L3**

### 4.6 E1 不是 IMPLEMENTATION-ENTRY blocker

**【S1-170C 显式判定】**:**E1 不应作为 IMPLEMENTATION-ENTRY-READY 的绝对 blocker**。

理由:
- V2A-42 疑点不影响 P2-2 KEEP 实质裁决
- V2A-42 疑点是 Effective Spec 文档精度问题,**不**是核心 Effective Spec 错误
- 可以在 L2 阶段通过限定性引用隔离
- **不应**因为 V2A-42 文档表述问题就拒绝进入实施

---

## §5. E3 核心审计:backend/ 创建 + pom.xml + application.yml

### 5.1 E3 描述回顾

**【S1-170C 引用 S1-170B §13.4】**:
> E3 | backend/ 实际创建 + pom.xml + application.yml | **IMPLEMENTATION-READY** | 高

### 5.2 循环依赖严格审计

**【S1-170C 显式检测循环依赖】**:

如果:
- **L3 IMPLEMENTATION-ENTRY-READY 的前置条件** = "backend 必须已经创建"
- **backend 创建** = "实施开始"
- **实施开始** = "进入 L4"

那么形成:
```
"必须开始实施,才能允许开始实施"
= "backend 必须创建才能进入 L3"
= "L3 的前置条件 = L4 的第一步"
= 循环依赖(非法)
```

### 5.3 E3 真正层级分类

**【S1-170C 显式】**:

| 维度 | S1-170B | S1-170C 校正 |
|---|---|---|
| **E3 真正含义** | "backend/ 实际创建 + pom.xml + application.yml" | 同左 |
| **正确层级** | **L4 IN-PROGRESS 的第一步**(不是 L3 前置)| **L4 IN-PROGRESS 的第一步** |
| **是否阻塞 L3** | (隐含)是 | ✗ **否** |

### 5.4 P1-07:循环依赖风险登记

**【S1-170C 关键发现 P1-07】** S1-170B 把 E3 放在 L3 IMPLEMENTATION-ENTRY-READY 是**非法循环依赖**。

| 项 | 内容 |
|---|---|
| **风险编号** | **P1-07**(新)|
| **风险描述** | S1-170B §13.4 把 E3(backend 创建 + pom.xml + application.yml)放在 IMPLEMENTATION-ENTRY-READY 层,形成"必须开始实施才能允许开始实施"的非法循环依赖 |
| **严重度** | **高** |
| **正确分类** | E3 应放在 L4 IN-PROGRESS(实施开始后的第一步)|
| **解决** | E3 不应作为 L3 blocker。L3 的真正前置条件是 L1 + L2 已完成 |

**【S1-170C 显式】**:
- **L3 IMPLEMENTATION-ENTRY-READY 的真正前置条件**(根据 Gate Matrix):
  - L1 SPEC-READY 已达成
  - L2 CONTRACT-READY 已达成
  - 本地 / 测试数据库可访问
  - IGNORE_TABLES 静态清单冻结
- **L3 不应**包含 E3 / E5 / E8 / 集成测试通过等"实施开始后才会产生"的条件

---

## §6. E5 核心审计:DEFAULT-01~05 实际运行

### 6.1 E5 描述回顾

**【S1-170C 引用 S1-170B §13.4】**:
> E5 | DEFAULT-01~05 实际运行 + 测试通过 | **RUNTIME-VERIFIED** | 高

### 6.2 E5 真正层级分类

**【S1-170C 显式】**:

| 维度 | 评估 |
|---|---|
| **E5 含义** | "DEFAULT-01~05 实际运行 + 测试通过" |
| **正确层级** | **L7 RUNTIME-VERIFIED** |
| **S1-170B 分类** | L7 RUNTIME-VERIFIED ✓ |

### 6.3 E5 依赖关系分析

**【S1-170C 显式】**:E5 必须依赖以下条件才能执行:

| 依赖 | 层级 | 验证 |
|---|---|---|
| DEFAULT-01~05 测试设计 | L1 SPEC-READY | ✓ 已冻结(241V2A-5 / 14 / 15)|
| DEFAULT-01~05 测试代码(JUnit 类)| L5 IMPLEMENTATION-COMPLETE | ✗ 未实施 |
| Service / Repository 实现 | L5 IMPLEMENTATION-COMPLETE | ✗ 未实施 |
| Spring 上下文启动 | L5 IMPLEMENTATION-COMPLETE | ✗ 未实施 |
| 本地 / 测试数据库可访问 | L3 IMPLEMENTATION-ENTRY-READY | ✗ 未确认 |

**【S1-170C 显式】**:E5 是 **L7 RUNTIME-VERIFIED** 的**结果**,**不是 L3 的前置条件**。

### 6.4 P1-08:测试运行不能作为编码入口条件

**【S1-170C 关键发现 P1-08】** S1-170B §13.4 正确把 E5 放在 L7 RUNTIME-VERIFIED。**但** S1-170B §13.5 "S1-171 真正阻塞条件" 把 E5 列为 S1-171 阻塞,**需要进一步审计 S1-171 是否被定义为 L3 入口**。

| 项 | 内容 |
|---|---|
| **风险编号** | **P1-08**(预防性登记)|
| **风险描述** | 如果 S1-171 被定义为"开始 backend/ 编码实施",E5(测试运行)就不应作为 L3 / L4 的前置条件。E5 应严格属于 L7 RUNTIME-VERIFIED |
| **严重度** | **中**(预防性登记,当前 S1-170B 已正确分类 E5 到 L7)|
| **正确分类** | E5 = L7 RUNTIME-VERIFIED,**不**阻塞 L3 / L4 / L5 / L6 |
| **S1-171 定位必须明确** | S1-171 不能同时是"审计 / 准备"和"backend 编码" |

**【S1-170C 显式】**:
- **测试实际运行结果不能作为编码入口条件,因为测试运行依赖已经存在的实施产物(代码 / Service / Repository / 数据库)**
- E5 应严格属于 L7,**不能**错放在 L3 / L4 / L5 / L6

---

## §7. E8 核心审计:生产数据库环境

### 7.1 E8 描述回顾

**【S1-170C 引用 S1-170B §13.4】**:
> E8 | 生产数据库环境就绪 | **IMPLEMENTATION-READY** | 高

### 7.2 数据库层级严格分类

**【S1-170C 显式】**:

| 数据库类型 | 用途 | 正确层级 |
|---|---|---|
| **本地开发数据库**(H2 / dev DB)| 开发者本地编码测试 | L3 IMPLEMENTATION-ENTRY-READY |
| **测试数据库**(单元测试 / 集成测试)| 测试运行 | L7 RUNTIME-VERIFIED(可以更早,但不应在 L3 阻塞)|
| **集成环境数据库** | 集成测试 / 预发布 | L6 PRODUCTION-READY |
| **生产数据库** | 真实生产环境 | **L6 PRODUCTION-READY**(不能错放在 L3)|

### 7.3 E8 真正层级分类

**【S1-170C 显式】**:

| 维度 | S1-170B | S1-170C 校正 |
|---|---|---|
| **E8 含义** | "生产数据库环境就绪" | 同左 |
| **正确层级** | **L6 PRODUCTION-READY** | **L6 PRODUCTION-READY** |
| **S1-170B 错误分类** | "IMPLEMENTATION-READY" | ⚠️ **错放** |

### 7.4 P1-09:E8 错放层级风险登记

**【S1-170C 关键发现 P1-09】** S1-170B §13.4 把 E8(生产数据库)放在 L3 IMPLEMENTATION-ENTRY-READY 是**严重错放**。

| 项 | 内容 |
|---|---|
| **风险编号** | **P1-09**(新)|
| **风险描述** | S1-170B §13.4 把 E8(生产数据库环境就绪)放在 IMPLEMENTATION-ENTRY-READY,实际应属于 L6 PRODUCTION-READY。生产数据库不应是"开始编码"的前置条件 |
| **严重度** | **高** |
| **正确分类** | E8 = L6 PRODUCTION-READY。L3 IMPLEMENTATION-ENTRY-READY 只需要"本地 / 测试数据库可访问" |
| **解决** | 把 E8 从 L3 移到 L6。L3 仅保留"本地 / 测试数据库可访问"作为前置 |

**【S1-170C 显式】**:
- **"生产数据库"** 是 PRODUCTION-READY 的前置,**不是** IMPLEMENTATION-ENTRY-READY 的前置
- **"本地 / 测试数据库"** 可以是 IMPLEMENTATION-ENTRY-READY 的前置
- **不能** 把生产数据库与本地数据库混为一个 E8

### 7.5 E8 不应阻塞实施开始

**【S1-170C 显式判定】**:
- E8 应从 L3 IMPLEMENTATION-ENTRY-READY 移除
- E8 应放在 L6 PRODUCTION-READY
- **不应**因为"生产数据库未就绪"就拒绝开始 backend/ 编码

---

## §8. E4 核心审计:Implementation Contract 完整建立

### 8.1 E4 描述回顾

**【S1-170C 引用 S1-170B §13.4】**:
> E4 | Production Implementation Contract 完整建立 | **CONTRACT-READY** | 高

### 8.2 E4 真正层级分类

**【S1-170C 显式】**:

| 维度 | S1-170B | S1-170C 校正 |
|---|---|---|
| **E4 含义** | "Production Implementation Contract 完整建立" | 同左 |
| **正确层级** | **L2 CONTRACT-READY** | **L2 CONTRACT-READY** ✓ |

### 8.3 E4 与 L3 的关系

**【S1-170C 显式】**:
- E4 = **L2 CONTRACT-READY 的形成条件**
- E4 完成后,系统进入 L2 = CONTRACT-READY
- L3 = L2 + 其它 L3 前置条件

**【S1-170C 严禁】**:
- 不能把 E4 同时定义为 L2 的形成条件 **和** L3 的额外重复条件
- 必须建立 **Contract Gate**(L2 完成判定)**与** **Implementation Entry Gate**(L3 完成判定)**两个层次**

### 8.4 Contract Gate 与 Implementation Entry Gate 分离

**【S1-170C 显式建立】**:

```
Contract Gate (L2 → L3):
  L1 SPEC-READY ✓ (前置)
  + E4 Implementation Contract 完整建立 ✓ (本 Gate 唯一条件)
  → L2 CONTRACT-READY 已达成

Implementation Entry Gate (L2 → L3 完成后,允许进入 L4):
  L2 CONTRACT-READY ✓ (前置)
  + 本地 / 测试数据库可访问 ✓
  + V2A-42 疑点已在 L2 限定性引用隔离 ✓
  → L3 IMPLEMENTATION-ENTRY-READY 已达成
  → 允许进入 L4 IN-PROGRESS
```

**【S1-170C 显式】**:
- E4 完成后进入 L2,**不**直接进入 L3
- L3 还需要**其它**前置条件(本地数据库 / V2A-42 隔离)
- **不能**把 E4 同时定义为 L2 形成条件和 L3 额外条件

---

## §9. E7 核心审计:IGNORE_TABLES

### 9.1 E7 描述回顾

**【S1-170C 引用 S1-170B §13.4】**:
> E7 | IGNORE_TABLES 完整清单 | **CONTRACT-READY** | 中

### 9.2 E7 三层分离

**【S1-170C 显式】** E7 必须分离为 3 个独立条件:

| 子条件 | 内容 | 正确层级 |
|---|---|---|
| **E7.1** | IGNORE_TABLES **静态清单冻结**(文档级)| **L2 CONTRACT-READY** |
| **E7.2** | IGNORE_TABLES **实际代码配置**(application.yml / MybatisPlusConfig)| **L5 IMPLEMENTATION-COMPLETE** |
| **E7.3** | IGNORE_TABLES **实际租户隔离测试通过**(跨表查询无公司数据泄漏)| **L7 RUNTIME-VERIFIED** |

### 9.3 E7 不能作为单一 E 条件

**【S1-170C 显式】**:
- E7 = "IGNORE_TABLES 完整清单" 这个单一描述**不清晰**
- 应拆分为 E7.1 / E7.2 / E7.3
- E7.1(L2)= 静态文档冻结
- E7.2(L5)= 实际代码配置
- E7.3(L7)= 实际租户隔离测试

### 9.4 E7 错误分类风险

**【S1-170C 显式】**:

| 维度 | S1-170B | S1-170C 校正 |
|---|---|---|
| **E7 单一描述** | "IGNORE_TABLES 完整清单" + CONTRACT-READY + 中 | ⚠️ **不清晰** |
| **正确描述** | E7.1 + E7.2 + E7.3 三层分离 | ✓ |

**【S1-170C 显式】**:
- S1-170B §13.4 把 E7 笼统放在 CONTRACT-READY,**部分正确**(只覆盖了 E7.1)
- 应改为 3 个独立条件

---

## §10. P1/P2 风险登记(S1-170C 新增)

### 10.1 新增 P1 风险

| # | 风险 | 严重度 | 来源 |
|---:|---|:-:|---|
| **P1-07**(新)| S1-170B §13.4 把 E3(backend 创建 + pom.xml + application.yml)放在 L3 IMPLEMENTATION-ENTRY-READY,形成"必须开始实施才能允许开始实施"的非法循环依赖 | 高 | §5 |
| **P1-08**(新)| S1-170B §13.5 把 E5(测试运行)列为 S1-171 阻塞,需要进一步审计 S1-171 是否被定义为 L3 入口;如果 S1-171 是 backend 编码入口,E5 错放为 L3 前置构成非法循环 | 中 | §6 |
| **P1-09**(新)| S1-170B §13.4 把 E8(生产数据库)放在 L3 IMPLEMENTATION-ENTRY-READY,实际应属于 L6 PRODUCTION-READY | 高 | §7 |

### 10.2 P1 风险汇总

| 风险编号 | 描述 | 严重度 |
|---|---|:-:|
| P1-01 | S1-170 审计对象集合不完整 + 漏审计 232~238 + 20x~22x | 高 |
| P1-02 | V2A-42 存在未闭环的语义错误 | 中 |
| P1-03 | F4 ≥80% 错误归类 | 高 |
| P1-04 | API / Object / State 统计严重错误 | 高 |
| P1-05 | S1-169 scope vs Project scope 范围错配 | 高 |
| P1-06 | S1-170A 数字残留 + 缺乏 5 层 Readiness 分层 | 高 |
| **P1-07**(新)| E3 错放 L3 形成非法循环依赖 | 高 |
| **P1-08**(新)| E5 可能错放 L3 入口 | 中 |
| **P1-09**(新)| E8 错放 L3 应为 L6 | 高 |
| **P1-10**(新)| E7 单一描述不清晰,应分离为 E7.1 / E7.2 / E7.3 | 中 |

**【S1-170C 显式】**:本轮新增 4 项 P1 风险(P1-07 / P1-08 / P1-09 / P1-10)。

### 10.3 P2 风险汇总

| 风险编号 | 描述 | 父子关系 |
|---|---|---|
| P2-01 | V2A-42 §5.7 GC eligibility 三条件混淆 | P1-02 子项 |
| P2-02 | V2A-42 §5.2 OpenJDK 内部结构表述 | P1-02 子项 |
| P2-03 | S1-170 §7.2 数字 41 实际 36 | P1-01 子项 |
| P2-04 | S1-170 §2.1 数字 60 实际 51 | P1-01 子项 |

### 10.4 风险总数

- **P1 总数**:10 项(S1-170B 6 项 + S1-170C 新增 4 项)
- **P2 独立总数**:2 项
- **P2 子项总数**:4 项
- **独立风险总数**:10 + 2 = **12 项**

---

## §11. E 条件重新归类(S1-170C 校正)

### 11.1 E 条件正确层级(S1-170C 校正版)

| E 条件 | S1-170B 分类 | S1-170C 正确分类 | 严重度变化 |
|---|---|---|---|
| **E1** V2A-42 校正 | IMPLEMENTATION-READY(高)| **L1 SPEC-READY(部分)+ 可能 L2 CONTRACT-READY** | 高 → 中 |
| **E3** backend/ 创建 | IMPLEMENTATION-READY(高)| **L4 IN-PROGRESS 的第一步**(不阻塞 L3)| 高 → N/A(错放)|
| **E4** Implementation Contract | CONTRACT-READY(高)| **L2 CONTRACT-READY** | 高 ✓ 不变 |
| **E5** DEFAULT-01~05 实际运行 | RUNTIME-VERIFIED(高)| **L7 RUNTIME-VERIFIED** | 高 ✓ 不变 |
| **E7** IGNORE_TABLES 清单 | CONTRACT-READY(中)| **L2(静态清单)+ L5(代码配置)+ L7(测试通过)** | 中 → 应拆分为 3 项 |
| **E8** 生产数据库 | IMPLEMENTATION-READY(高)| **L6 PRODUCTION-READY** | 高 → 应从 L3 移到 L6 |

### 11.2 L3 IMPLEMENTATION-ENTRY-READY 真正前置条件

**【S1-170C 显式重建 L3 真正前置条件】**:

```
L3 IMPLEMENTATION-ENTRY-READY 的真正前置条件:

1. L1 SPEC-READY 已达成(Effective Spec 完整冻结)
2. L2 CONTRACT-READY 已达成(Implementation Contract 完整建立)
3. 本地 / 测试数据库可访问(注意:**不是**生产数据库)
4. V2A-42 疑点已在 L2 通过限定性引用隔离(预防性)
```

**【S1-170C 显式严禁】** L3 IMPLEMENTATION-ENTRY-READY **不应包含**:

- ✗ backend/ 已创建(那是 L4 才开始)
- ✗ pom.xml / application.yml 已创建(那是 L4 才开始)
- ✗ IGNORE_TABLES 实际代码配置(那是 L5 才完成)
- ✗ DEFAULT-01~05 测试代码已创建(那是 L5 才完成)
- ✗ DEFAULT-01~05 测试实际运行(那是 L7 才完成)
- ✗ 生产数据库环境就绪(那是 L6 才完成)
- ✗ 集成测试通过(那是 L7 才完成)

---

## §12. S1-171 重新定义

### 12.1 S1-171 必须拆分为多个子阶段

**【S1-170C 显式】**:S1-171 不能简单写成 ALLOW / BLOCK。必须拆分为:

| 子阶段 | 描述 | 层级 |
|---|---|---|
| **S1-171A** | Audit / Spec Correction(V2A-43 / V2A-44 校正 V2A-42 疑点)| L1 SPEC-READY |
| **S1-171B** | Implementation Contract Preparation(基于 L2 形成 E4 完成)| L2 CONTRACT-READY |
| **S1-171C** | Implementation Entry Preparation(本地数据库 / 工具链就绪)| L3 IMPLEMENTATION-ENTRY-READY |
| **S1-171D** | Backend Implementation(创建 backend / pom / Entity / Mapper / Service / Controller / Flyway SQL / JUnit)| L4 IN-PROGRESS |

**【S1-170C 显式】**:
- S1-171A / S1-171B / S1-171C = **审计 / 准备阶段**,**允许**进入
- S1-171D = **backend/ 实施阶段**,需要 L3 已达成才能进入

### 12.2 S1-171 判定框架

**【S1-170C 显式】**:

| S1-171 定位 | 是否允许 |
|---|:-:|
| **S1-171A**(V2A-43 / V2A-44 校正 V2A-42 疑点)| ✓ ALLOW(L1 SPEC-READY 已达成,V2A-42 疑点不属于核心 Effective Spec)|
| **S1-171B**(Implementation Contract 准备)| ✓ ALLOW(L2 CONTRACT-READY 形成工作)|
| **S1-171C**(本地数据库 / 工具链准备)| ✓ ALLOW(L3 IMPLEMENTATION-ENTRY-READY 形成工作)|
| **S1-171D**(backend/ 实际编码)| ⚠️ **CONDITIONAL**(需要 L3 已达成 + 老板明确指令)|

### 12.3 S1-171 实际允许边界

**【S1-170C 显式】** S1-171 允许以下动作:

| 动作 | 层级 | 是否允许 |
|---|---|:-:|
| 创建 V2A-43 / V2A-44 校正 V2A-42 | L1 SPEC-READY | ✓ ALLOW |
| 准备 Implementation Contract 草案 | L2 CONTRACT-READY | ✓ ALLOW |
| IGNORE_TABLES 静态清单核验 | L2 CONTRACT-READY | ✓ ALLOW |
| 准备本地 / 测试数据库 | L3 IMPLEMENTATION-ENTRY-READY | ✓ ALLOW |
| 系统设置侦察进度单独审计 | L1 SPEC-READY | ✓ ALLOW |
| 创建 backend/ 目录 | L4 IN-PROGRESS | ⚠️ CONDITIONAL(需要 L3 达成)|
| 创建 pom.xml | L4 IN-PROGRESS | ⚠️ CONDITIONAL |
| 创建 application.yml | L4 IN-PROGRESS | ⚠️ CONDITIONAL |
| 执行 DDL | L4 / L6 | ✗ BLOCK |
| 连接生产数据库 | L6 PRODUCTION-READY | ✗ BLOCK |
| 创建 JUnit 测试 | L5 IMPLEMENTATION-COMPLETE | ⚠️ CONDITIONAL |

---

## §13. 重新给出 Readiness 判定(S1-170C 校正版)

### 13.1 S1-169 Readiness(基于 7 层)

**【S1-170C 显式】**:

| Layer | S1-169 状态 |
|---|:-:|
| **L1 SPEC-READY** | ✓ **READY** |
| **L2 CONTRACT-READY** | ⚠️ **PARTIAL**(仅 user_company 部分冻结)|
| **L3 IMPLEMENTATION-ENTRY-READY** | ⚠️ **CONDITIONAL**(L1 ✓ + L2 部分 + 本地 DB 待确认)|
| **L4 IN-PROGRESS** | ✗ **NOT ESTABLISHED** |
| **L5 IMPLEMENTATION-COMPLETE** | ✗ **NOT ESTABLISHED** |
| **L6 PRODUCTION-READY** | ✗ **NOT ESTABLISHED** |
| **L7 RUNTIME-VERIFIED** | ✗ **NOT ESTABLISHED** |

### 13.2 OptFlow PMS Phase 1 Readiness

**【S1-170C 显式】**:

| Layer | Phase 1 状态 |
|---|:-:|
| **L1 SPEC-READY** | ✓ **READY**(核心领域 Confirmed Complete)|
| **L2 CONTRACT-READY** | ⚠️ **PARTIAL** |
| **L3 IMPLEMENTATION-ENTRY-READY** | ⚠️ **CONDITIONAL** |
| **L4 IN-PROGRESS** | ✗ **NOT ESTABLISHED** |
| **L5 IMPLEMENTATION-COMPLETE** | ✗ **NOT ESTABLISHED** |
| **L6 PRODUCTION-READY** | ✗ **NOT ESTABLISHED** |
| **L7 RUNTIME-VERIFIED** | ✗ **NOT ESTABLISHED** |

---

## §14. 7 层生命周期最终输出

```
L1 SPEC-READY
   ↓ (依赖 L1)
L2 CONTRACT-READY
   ↓ (依赖 L2 + 本地 DB)
L3 IMPLEMENTATION-ENTRY-READY
   ↓ (开始实施)
L4 IMPLEMENTATION-IN-PROGRESS
   ↓ (代码完成 + 编译通过)
L5 IMPLEMENTATION-COMPLETE
   ↓ (生产数据库 + 部署参数)
L6 PRODUCTION-READY
   ↓ (测试实际运行通过)
L7 RUNTIME-VERIFIED
```

**【S1-170C 最高优先原则】**:
> **PRE-ENTRY CONDITIONS MUST BE OBSERVABLE BEFORE ENTRY.**
> 进入 L3 之前,所有 Required 条件必须能够在"不执行实际实施"的情况下被验证。

---

## §15. 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\S1-170C_Readiness生命周期与EntryGate语义校正.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | `S1-170B_Pre-Development_Integrity_Audit_自身一致性闸门审计.md`(不修改)|
| 严禁修改 | S1-170B / S1-170A / S1-170 / 任何历史 MD / 源码 / 数据库 |

---

**End of S1-170C**
