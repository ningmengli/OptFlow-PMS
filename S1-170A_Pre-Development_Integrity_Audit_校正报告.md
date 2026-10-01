# S1-170A｜Pre-Development Integrity Audit 校正报告

---

## §0. Metadata

| 字段 | 内容 |
|---|---|
| Audit ID | S1-170A |
| Audit Date | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base S1-170 | `S1-170_Pre-Development_Integrity_Audit.md`(不修改) |
| Scope | S1-170 审计报告自身的统计口径 / 范围 / 结论 / 证据复核 |
| 严禁 | 修改任何历史 MD / 修改源码 / 修改数据库 / commit / push / 创建 S1-171 |

---

## §1. Audit Objective

### 1.1 唯一核心问题

> **S1-170_Pre-Development_Integrity_Audit.md 自身的审计结论、统计口径、范围定义、证据引用是否成立?**
> **S1-170 把"S1-169 范围"与"OptFlow PMS 全项目范围"是否混为一谈?**
> **S1-170 的关键数字(API / Object / State / 补丁数)是否与仓库真实文件一致?**

### 1.2 本审计严禁项

- ✗ 不修改 `S1-170_Pre-Development_Integrity_Audit.md` 任何字节
- ✗ 不修改任何 S1-169 / S1-168 / S1-167 / S1-166 / S1-165 等历史 MD
- ✗ 不修改源码 / VisionCare PMS
- ✗ 不修改数据库
- ✗ 不创建 S1-171
- ✗ 不 commit / push

### 1.3 本审计允许项

- ✓ 读取仓库现状(实际文件清单 / SHA256 / Git 历史)
- ✓ 读取已有设计文档 / 审计文档
- ✓ 静态交叉核验
- ✓ 新增 `S1-170A_Pre-Development_Integrity_Audit_校正报告.md`

---

## §2. S1-170 原审计范围重构

### 2.1 仓库真实文件清单(全项目,不含 _gen_phase0_placeholders 与早期遗留)

**【S1-170A 真实扫描结果】**

| 系列 | 文件数 | 范围说明 |
|---|---:|---|
| **0x 系列**(项目核心规则 / 索引 / 状态 / 业务规则等)| **11** | 00_项目总索引 / 00_项目核心规则_认识论 / 01_菜单结构 / 02_页面分析 / 03_业务流程 / 04_数据模型 / 05_业务规则 / 06_UI与交互规范 / 07_测试用例 / 08_未确认问题 / 09_变更记录 |
| **1x 系列** | 0 | 无 |
| **2x 系列**(20x ~ 29x 全项目)| **93** | 详见下方细分 |
| ├ 20x(领域总审计 1)| 约 10 | MedicalRecord / Customer / Patient / Sale / Delivery / Cashflow 等 |
| ├ 21x(领域总审计 2)| 约 10 | Product / Marketing / School / Appointment / CustomerFollowUp 等 |
| ├ 22x(领域总审计 3 + 总纲)| 约 10 | DataReport / SystemSetting / 诊所管理 / 全局交叉 / 总纲 / 5 步法 FLOW003 等 |
| ├ 23x(API 前置 + 40 API 字段级 + PAGE 证据)| 约 6 | 230 / 231 / 232 / 233 + PAGE 证据 |
| ├ 234(独立工程能力 + ID 类型)| 3 | 234 / 234A / 234B |
| ├ 235(数据模型 + DDL 前置 + 修订)| 3 | 235 / 235A / 235B |
| ├ 236(DDL 草案 + 修正 + 文字纠错)| 3 | 236 / 236A / 236B |
| ├ 237(DDL 独立审计)| 2 | 237 / 237A |
| ├ 238(实施前置)| 2 | 238 / 238A |
| ├ 239(S1-169-0)| 2 | 239 / 239A |
| ├ 240(Q4 跨公司隔离正式裁决)| 1 | 240 |
| ├ 241 + 241A + 241A-1(S1-169-1 基础)| 3 | 241 / 241A / 241A-1 |
| ├ 241V2 / 241V3 / 241V4(S1-169-1 基础修正)| 3 | 241V2 / 241V3 / 241V4 |
| ├ 241V2A(S1-169-1 P0-2 强制覆盖补丁)| 1 | 241V2A |
| ├ 241V2A-1 ~ 35(S1-169-1 补丁)| 35 | S1-169-1 独立盲审裁决补丁 |
| ├ 241V2A-36 ~ 42(S1-169-2 P2 关闭)| 7 | S1-169-2 P2 整改与措辞校正 |
| ├ S1-170(本审计)| 1 | S1-170_Pre-Development_Integrity_Audit.md |
| **总计(全项目)** | **≈ 105** | 不含早期遗留 / controller.js 等 |

### 2.2 S1-170 声明的审计对象集合 vs 实际

**【S1-170 §2.1 声明】**:
> 已审计文档清单(60 份 S1-169 + 5 份项目核心 = **65 份**)
> - S1-169-0:2 份(239 / 239A)
> - S1-169-1 基础:5 份(241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4)
> - S1-169-1 P1/P2 修复:35 份
> - S1-169-2 P2 关闭:7 份
> - 项目核心规则:2 份
> - 项目热数据:1 份
> - 未确认问题:1 份
> - 页面证据:1 份

**【S1-170A 实际核验】**:

| 编号 | S1-170 声明 | 实际仓库 | 差异 | 差异原因 |
|---:|---:|---:|---:|---|
| S1-169-0 | 2 份 | 2 份(239 + 239A) | ✓ 一致 | — |
| S1-169-1 基础 | **5 份** | **6 份**(241 + 241A + 241A-1 + 241V2 + 241V3 + 241V4) | **差 1 份** | S1-170 漏算 241V4 |
| S1-169-1 补丁 | **35 份** | **36 份**(241V2A + 241V2A-1 ~ 35) | **差 1 份** | S1-170 漏算 241V2A(P0-2 强制覆盖补丁) |
| S1-169-2 P2 关闭 | 7 份 | 7 份(241V2A-36 ~ 42) | ✓ 一致 | — |
| 项目核心规则 | 2 份 | 2 份(00_项目总索引 + 00_项目核心规则_认识论) | ✓ 一致 | — |
| 项目热数据 | 1 份 | 1 份(10_AI当前状态) | ✓ 一致 | — |
| 未确认问题 | 1 份 | 1 份(08_未确认问题) | ✓ 一致 | — |
| 页面证据 | 1 份 | 1 份(11_页面证据矩阵) | ✓ 一致 | — |
| **合计** | **54** | **55** | **差 1 份** | 漏算 241V4 + 241V2A = 2 份;但 241V2A 已被算入 35 份补丁?需重新核算 |

**【S1-170A 重新核算】**:

| 类别 | 实际 | S1-170 声明 |
|---|---:|---:|
| S1-169-0 | 2 | 2 |
| S1-169-1 基础(241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4) | **6** | 5 |
| S1-169-1 P1/P2 修复(241V2A + 241V2A-1 ~ 35) | **36** | 35 |
| S1-169-2 P2 关闭(241V2A-36 ~ 42) | 7 | 7 |
| 项目核心规则 | 2 | 2 |
| 项目热数据 | 1 | 1 |
| 未确认问题 | 1 | 1 |
| 页面证据 | 1 | 1 |
| **合计** | **56** | **54** |

**【S1-170A 关键发现 P1-01-1】**:
- S1-170 实际漏算 **241V4**(表数量与 TenantLine 覆盖率一致性补丁)
- S1-170 实际漏算 **241V2A**(P0-2 强制覆盖补丁)
- S1-170 §2.1 声明"60 份 S1-169 + 5 份项目核心" = 65 份,但实际数字应为 **56 份**(S1-169 全系列 51 份 + 项目核心 5 份)
- **S1-170 数字"60 / 5 / 65"全部错误**

### 2.3 S1-170 完全未审计的关键历史文档

**【S1-170A 关键发现 P1-01-2】** S1-170 §2.1 仅审计 S1-169 + 5 份项目核心,但 S1-169 之前已经形成的核心规格文档**完全未审计**:

| 文件 | 关键内容 | S1-170 审计? |
|---|---|:-:|
| **230_S1-166A_API前置核验与数量冻结.md** | API 数量冻结 = 40 | ✗ 未审计 |
| **231_S1-166A_API前置核验修正版.md** | 230 修正版 | ✗ 未审计 |
| **232_S1-167_40个API字段级设计.md** | **40 个 API 字段级契约完整冻结** | ✗ 未审计 |
| **233_S1-167A_API字段级设计修正版.md** | 232 修正版 | ✗ 未审计 |
| **234_独立工程能力盲测报告.md** | 独立工程能力测试 | ✗ 未审计 |
| **234A_复用实体ID类型逆向核验报告.md** | ID 类型逆向核验 | ✗ 未审计 |
| **234B_S1-168_ID类型后端Schema证据核验.md** | ID 类型后端 Schema 核验 | ✗ 未审计 |
| **235_S1-167B_OptFlow数据模型裁决与DDL前置基线.md** | 数据模型裁决 | ✗ 未审计 |
| **235A_S1-167B_DDL前独立冻结审计报告.md** | DDL 前审计 | ✗ 未审计 |
| **235B_S1-167B_最终修订裁决与S1-168启动前置.md** | S1-168 启动前置 | ✗ 未审计 |
| **236_S1-168_DDL草案.md** | DDL 草案 | ✗ 未审计 |
| **236A_S1-168_DDL修正版.md** | DDL 修正 | ✗ 未审计 |
| **236B_S1-168_DDL修正版_文字纠错.md** | DDL 文字纠错 | ✗ 未审计 |
| **237_S1-168_DDL独立审计报告.md** | DDL 独立审计 | ✗ 未审计 |
| **237A_S1-168_DDL独立审计报告_第二轮.md** | DDL 第二轮审计 | ✗ 未审计 |
| **238_S1-169_实施前置映射基线.md** | **12 对象 + 12 PK + 31 真 FK + 40 API + 29 状态 已显式列出** | ✗ 未审计 |
| **238A_S1-169_实施前置待确认问题清单.md** | 实施前置待确认问题 | ✗ 未审计 |
| **225 ~ 229 系列**(门诊预约接诊领域模型 + 状态机)| **4 状态机 29 状态** 已冻结 | ✗ 未审计 |
| **200 ~ 219 系列**(12 个领域总审计)| 12+ 个 Object 已冻结 | ✗ 未审计 |
| **220 ~ 224 系列**(诊所管理 / SystemSetting / 报表域 总审计)| 多个 Object 已冻结 | ✗ 未审计 |

**【S1-170A 关键发现 P1-01-3】**:S1-170 标题是"Pre-Development Integrity Audit(开发前总闸门审计)",应该审计**整个 OptFlow PMS 进入开发前的全局状态**,但实际只审计了 S1-169 范围 + 项目核心 5 份。**S1-169 之前的核心规格文档(40 API / 12 对象 / 29 状态)完全未审计**。

### 2.4 S1-170 §1 范围定义与实际审计范围错配

**【S1-170 §1.1 声明】**:
> 当前 S1-169 全系列文档,是否已经达到"可以开始进入真实开发实施"的最低条件?

**【S1-170 §9 判定】**:
> 综合判定:CONDITIONAL

**【S1-170A 显式指出范围错配】**:

| 维度 | S1-170 范围定义 | S1-170 实际推断范围 | 错配 |
|---|---|---|:-:|
| 题目"Pre-Development" | (隐含)整个 OptFlow PMS | S1-169 子集 | **错配** |
| §1.1 核心问题 | "S1-169 全系列文档" | 实际推断到整个项目 | **错配** |
| §4.3 API = 0 冻结 | 推断整个项目 API | 实际只审计 S1-169 范围 | **严重错配** |
| §4.1 Object = 3 冻结 | 推断整个项目 Object | 实际只审计 S1-169 范围 | **严重错配** |
| §4.4 State = 1 冻结 | 推断整个项目 State | 实际只审计 S1-169 范围 | **严重错配** |
| §9 判定 CONDITIONAL | 推断整个项目开发准备度 | 应只判定 S1-169 scope 准备度 | **错配** |

**【S1-170A 显式】**:S1-170 §1.1 已经显式把范围定义为"S1-169 全系列",但 S1-170 §4 在审计中**跨越到了 S1-169 之外的领域**(API / Object / State 统计被错误推广到全项目),这是**审计范围与判定范围不一致**。

---

## §3. V2A-36~42 修正链复核(后一是否修前)

### 3.1 V2A-36 → V2A-37(P2-0 关闭与证据层级校正)

| 项 | V2A-36 原文 | V2A-37 校正 | 是否真修正? | 是否产生新问题? |
|---|---|---|:-:|:-:|
| **原问题** | P2-0 业务规则 exactly-one(241V2A-11 §4 / 36 / 37) | — | — | — |
| **V2A-36 核心内容** | 关闭 P2-0(代码层)| 校正证据身份 | — | — |
| **证据身份误标** | "当前代码已修复" / "当前测试已通过" | "Effective Spec 中冻结的实施写法" | ✓ 真修正 | ✗ 无新问题 |
| **三层状态缺失** | 仅"代码层 CLOSED" | 增加"Implementation NOT YET VERIFIED + Runtime NOT EXECUTED" | ✓ 真修正 | ✗ 无新问题 |
| **Effective Spec vs Production Implementation 区分** | 模糊 | 显式区分 | ✓ 真修正 | ✗ 无新问题 |
| **判断** | — | — | ✓ **真修正**(A 类:语义补充 / B 类:范围澄清)| ✗ 无 |

**结论**:V2A-37 修正 V2A-36 的过强表述,**属于语义补充 + 范围澄清**,**不产生新问题**。

### 3.2 V2A-37 → V2A-38(P2-0 已 CLOSED,转入 P2-1)

| 项 | V2A-37 → V2A-38 |
|---|---|
| **原问题** | P2-1(DEFAULT-03 未使用 companyBId/companyCId)|
| **V2A-38 核心动作** | P2-1 复核关闭 + 留待二选一 |
| **是否产生新问题** | ✗ 无(只处理 P2-1,不修改 P2-0)|
| **判断** | ✓ **范围分离**(A 类)|

### 3.3 V2A-38 → V2A-39(P2-1 二选一 DELETE 裁决)

| 项 | V2A-38 → V2A-39 |
|---|---|
| **原问题** | P2-1 二选一:删除占位 vs 保留占位 |
| **V2A-39 核心动作** | 正式裁决 **DELETE**(删除 DEFAULT-03 占位声明)|
| **是否产生新问题** | ⚠️ 引入新规则("不得再添加 companyBId/companyCId 占位声明")|
| **判断** | ✓ **范围澄清 + 新规则冻结**(A + B 类)|

### 3.4 V2A-39 → V2A-40(从 P2-1 转 P2-2)

| 项 | V2A-39 → V2A-40 |
|---|---|
| **原问题** | P2-2(pool.shutdown() 后未 awaitTermination)|
| **V2A-40 核心动作** | 正式裁决 **KEEP shutdown-only** |
| **是否产生新问题** | ✗ 无 |
| **判断** | ✓ **范围分离**(A 类)|

### 3.5 V2A-40 → V2A-41(措辞与生命周期语义校正)

**【S1-170A 关键发现 P1-02-1】**:V2A-41 §11.2 第 3 项 GC eligibility 定义本身有问题。

| 项 | V2A-40 原文 | V2A-41 校正 | 是否真修正? | 是否产生新问题? |
|---|---|---|:-:|:-:|
| **原问题** | "local pool → GC 回收 pool"作为生命周期证据 | — | — | — |
| **V2A-41 §11.2 第 3 项** | (无,这是新增定义) | "ExecutorService 对象已无强引用,可被 GC 回收" | — | **⚠️ 简化**(忽略 ThreadPoolExecutor 内部数据结构对 GC 的影响)|
| **GC eligibility 定义** | — | "ExecutorService 对象已无强引用,可被 GC 回收" | — | **⚠️ 过度简化** |
| **判断** | — | — | ⚠️ **部分修正 + 引入新定义**(A + D 类)|

**【S1-170A 显式】**:
- V2A-41 的 §11.2 第 3 项定义"ExecutorService 对象已无强引用,可被 GC 回收"**本身是有问题的**:
  1. **"已无强引用"≠ GC eligibility** —— 即使局部变量销毁,对象可能仍被 ThreadPoolExecutor 内部数据结构持有
  2. **GC eligibility ≠ GC 已发生** —— GC eligibility 仅意味着"无 GC root 可达",**不等于** JVM 已经执行 GC
  3. **"Worker Thread 仍持有 ExecutorService 内部数据结构"** —— ThreadPoolExecutor 通过活跃 worker Thread → Worker → ThreadPoolExecutor 内部数据结构 间接可达
- V2A-41 把 GC eligibility 等同于"已无强引用"是**过度简化**,但这是 §11.2 引入的新定义,V2A-40 没有,所以**严格来说不是 V2A-41 修正 V2A-40 的问题**,而是 V2A-41 自己引入的新不准确

### 3.6 V2A-41 → V2A-42(Java Executor 生命周期语义二次校正)

**【S1-170A 关键发现 P1-02-2】**:V2A-42 存在三个具体疑点(老板 §5 列出)。

| 疑点 | V2A-42 表述 | 严谨判断 |
|---|---|---|
| **疑点一:JVM GC ≠ GC eligibility** | V2A-42 §4.3 第 5 点"JVM GC 调度器选择执行 GC 的时机,**不可预测**" | **部分成立**。V2A-42 把 GC eligibility 与 JVM GC 时点区分是对的。但 V2A-42 §5.7 GC eligibility 三条件表述为"(c) JVM GC 调度器实际执行 GC",**混淆了 GC eligibility 与 GC 完成** |
| **疑点二:OpenJDK 内部结构** | V2A-42 §5.2 描述 ThreadPoolExecutor 内部 HashSet<Worker> / Worker / Thread 引用链 | **不能提升为"Java ExecutorService 普遍规范"**。这是 OpenJDK 实现细节,Java API 契约(ExecutorService 接口)不保证此内部结构。其他实现(Hazelcast / Netty 等)可能不同 |
| **疑点三:endLatch.await() ≠ 破坏一致性** | V2A-42 §11.2 表中"endLatch.await(timeout, unit) 证明业务任务到达 finally 并完成其业务执行路径,**不等于** awaitTermination() 提供的 executor termination 等待" | **正确**。V2A-42 区分了业务任务完成与 executor 终止,这是对的 |

**【S1-170A 详细判断】**:

#### 3.6.1 疑点一详细分析

V2A-42 §5.7 表述:
> ExecutorService 对象 GC eligibility 取决于:**(a)** local variable 引用销毁;**(b)** 所有 worker thread 已终止释放 ThreadPoolExecutor 内部数据结构;**(c)** JVM GC 调度器实际执行 GC。三个条件**同时**满足时,ExecutorService 才进入 GC eligibility。

**问题**:**(c) 条件错误**。
- JVM GC 调度器实际执行 GC **不是 GC eligibility 的条件**
- GC eligibility 仅取决于"无 GC root 可达"
- JVM 是否执行 GC 是 GC eligibility 之后的另一个独立事件
- **应该改为**:
  > ExecutorService 对象 GC eligibility 取决于:**(a)** 无 GC root 可达(包括 local variable 销毁 + 活跃 worker thread 终止释放内部数据结构);**(b)** 之后,JVM GC 调度器可在任何时点执行 GC 回收该对象(时点不可预测)。

#### 3.6.2 疑点二详细分析

V2A-42 §5.2 表述:
```
ThreadPoolExecutor (extends AbstractExecutorService)
├── workers (HashSet<Worker>)
│   └── Worker (each worker holds)
│       ├── Thread thread (worker thread 对象)
│       └── Runnable firstTask (初始任务)
└── (内部状态: corePoolSize, maximumPoolSize, etc.)
```

**问题**:
- ThreadPoolExecutor 是 OpenJDK **java.util.concurrent** 包的**具体实现**
- 但 Java API 规范(`ExecutorService` 接口)只定义了 `submit / execute / shutdown / shutdownNow / awaitTermination / isShutdown / isTerminated` 等方法
- HashSet<Worker> 是 OpenJDK **实现细节**,**不在 Java API 规范中**
- 其他 ExecutorService 实现(如 `ForkJoinPool` / `ScheduledThreadPoolExecutor` / Netty `EventExecutorGroup` / Hazelcast `IExecutor` 等)内部结构不同

**应该改为**:
- 明确标注【通用技术事实 / OpenJDK 实现证据】
- 不能提升为"Java ExecutorService 普遍规范"
- 这只是"OpenJDK `ThreadPoolExecutor` 实现的引用关系"

#### 3.6.3 疑点三详细分析

V2A-42 §11.2 表中表述:
> endLatch.await(timeout, unit) 证明业务任务到达 finally 并完成其业务执行路径,**不等于** awaitTermination() 提供的 executor termination 等待

**判断**:**正确**。
- endLatch.await() 等待的是 T1/T2 在 finally 中 countDown
- T1/T2 Runnable.run() 返回后,worker Thread 仍可能存活(在 ThreadPoolExecutor 中等待)
- 两者不是同一件事

但需要注意:**这并不等于"破坏测试一致性"**。DEFAULT-03 测试三道断言是 `done.isTrue()` + `err1.get().isNull()` + `err2.get().isNull()`,这些断言在 `pool.shutdown()` 之后执行,**不依赖 worker Thread 是否终止**。所以**V2A-40 的 KEEP 裁决仍然成立**。

### 3.7 V2A-42 完整判断

**【S1-170A 显式判断 V2A-42】**:

| 维度 | 判断 |
|---|---|
| 是否修正 V2A-41 的过强表述 | ✓ 是(GC eligibility ≠ worker thread 已终止)|
| 是否产生新问题 | ⚠️ 是(疑点一:GC eligibility 三条件混淆 GC eligibility 与 GC 执行;疑点二:OpenJDK 内部结构被表述为普遍规范)|
| 是否修正 V2A-40 的 KEEP 裁决 | ✗ 否(KEEP 裁决保持)|
| 是否属于自诱发问题 | ⚠️ **部分自诱发**(V2A-41 引入的 §11.2 第 3 项不准确定义,被 V2A-42 §5.2 进一步具体化为"OpenJDK 内部结构")|
| 当前有效状态 | **保留 KEEP 裁决,GC eligibility 表述需进一步澄清** |

**【S1-170A 显式】**:V2A-42 的疑点一和疑点二**需要进一步校正**,但不影响 P2-2 KEEP 裁决。

### 3.8 V2A-36~42 修正链是否存在自诱发问题

**【S1-170A 关键发现 P1-02-3】**:

| 补丁 | 类别 | 自诱发? |
|---|---|:-:|
| **V2A-36** | 关闭 P2-0(代码层 CLOSED)| ✗ |
| **V2A-37** | 校正 V2A-36 过强表述 + 引入五级体系强化 | **A 类:语义补充**(部分自诱发)|
| **V2A-38** | 处理 P2-1(范围分离)| ✗ |
| **V2A-39** | 处理 P2-1 二选一(范围分离)| ✗ |
| **V2A-40** | 处理 P2-2 二选一(范围分离)| ✗ |
| **V2A-41** | 校正 V2A-40 措辞 + **引入 §11.2 第 3 项新定义** | **D 类:前一修正文档自诱发的问题** + A 类:语义补充 |
| **V2A-42** | 校正 V2A-41 + **引入 §5.2 OpenJDK 内部结构作为普遍规范 + §5.7 GC eligibility 三条件混淆** | **D 类:V2A-41 自诱发的部分被进一步具体化(同时引入新问题)** |

**【S1-170A 显式结论】**:
- V2A-37 → V2A-41 → V2A-42 **形成 3 层语义校正链**
- V2A-41 引入了**新定义**(§11.2 第 3 项),这被 V2A-42 进一步具体化为 OpenJDK 内部结构
- V2A-42 §5.7 GC eligibility 三条件中 "(c) JVM GC 调度器实际执行 GC" **混淆了 GC eligibility 与 GC 执行**
- V2A-42 §5.2 把 OpenJDK ThreadPoolExecutor 内部结构表述为普遍规范,**越界**

**结论**:**V2A-36~42 修正链总体稳定**(P0/P1 修复闭环 + P2 关闭),但 **V2A-42 自身需要进一步校正**(疑点一、二)。

### 3.9 修正链是否影响 P2-2 状态

**【S1-170A 显式】**:
- P2-2 = CLOSED(Effective Spec, KEEP shutdown-only) 状态**保持**
- V2A-41 / 42 的措辞校正是**语义精度审计**,不改变 P2-2 实质裁决
- 但 V2A-42 §5.2 / §5.7 的疑点一、二**需要后续单独校正**(不阻塞 P2-2 关闭)

---

## §4. F4 ≥80% 全局侦察门槛复核

### 4.1 S1-170 原文

**【S1-170 §8.2 F4】**:
> F4 | 侦察进度 ≥80% | 47%(缺 32 子菜单) | **阻塞**

**【S1-170 §10.1 风险 R3】**:
> R3 | Effective Spec 大量存在,Production Implementation 空白 → **实施时可能跳过"已冻结"边界** | **高**

### 4.2 当前真实侦察进度

**【S1-170A 重新核验】**:
- `10_AI当前状态.md` 最后更新 2026-08-28 21:30(最后更新距今 **19 天**)
- 顶级菜单 8 大(已确认 100%)
- 子菜单 61 个(已侦察 29/61 = **47%**)
- 88 页面 26 项字段为 AI 推断
- 32 个子菜单未侦察(营销 9 + 预约叫号 7 + 患者维护 4 + 筛查机构 12)

### 4.3 Phase 1 正式范围(老板指令明确)

**【S1-170A 引用老板指令 §6】**:
> 当前 Phase 1 正式范围:
> - 诊所管理
> - 系统设置

### 4.4 Phase 1 是否真的依赖整个系统 ≥80% 页面侦察?

**【S1-170A 独立分析】**:

#### 4.4.1 A. Phase 1 是否依赖整个系统 ≥80% 侦察?

**【S1-170A 判断】**:**否**

理由:
- Phase 1 范围仅"诊所管理 + 系统设置"
- "诊所管理"(PAGE-801 ~ 811) + "系统设置"(PAGE-9A.1 ~ 9I.20)= **31 个页面**
- 这 31 个页面的 26 项字段**与"营销 9 + 预约叫号 7 + 患者维护 4 + 筛查机构 12 = 32 个未侦察页面"无直接依赖**
- **未侦察的 32 个页面与 Phase 1 范围无业务耦合**

#### 4.4.2 B. 还是只需要 Phase 1 相关模块达到足够证据闭环?

**【S1-170A 判断】**:**是**

理由:
- Phase 1 范围(诊所管理 + 系统设置)对应的 31 个页面侦察进度需要单独评估
- `00_项目总索引.md` §"8️⃣ 诊所管理(PAGE-801 ~ PAGE-811)" 已确认 **100%** 侦察
- `00_项目总索引.md` §"⚙️ 系统设置(PAGE-9A ~ PAGE-9I + 子)" 状态未明确列出(但侦察历史显示已大部分观察)
- **Phase 1 相关模块的侦察进度可能已经 ≥80%,但 S1-170 没有区分**

#### 4.4.3 C. 是否存在跨模块依赖,导致必须达到全局 80%?

**【S1-170A 判断】**:**无明确证据**

理由:
- Phase 1 范围(诊所管理 + 系统设置)与其他顶级菜单(营销 / 预约叫号 / 患者维护 / 筛查机构)**无业务耦合**(这些是独立模块)
- "跨模块依赖"在 S1-170 中**未给出明确证据**
- 如果存在跨模块依赖,应具体说明是哪个模块的哪个功能依赖哪个模块的哪个字段

#### 4.4.4 D. F4 ≥80% 门槛的最终分类

**【S1-170A 显式四选一】**:

| 选项 | 含义 | S1-170A 选择 |
|---|---|:-:|
| **Hard blocker** | 全项目绝对门槛 | ✗ 否 |
| **Scope-dependent prerequisite** | 范围相关前置 | ✓ **是** |
| **Recommendation** | 建议 | (部分)|
| **Not established** | 证据不足 | ✗ 不采用 |

**【S1-170A 显式判定】**:**F4 应改为"范围相关前置项"(Scope-dependent prerequisite),而非"Hard blocker"**。

具体地:
- Phase 1 范围 = 诊所管理 + 系统设置
- Phase 1 相关侦察进度 = PAGE-801~811 + PAGE-9A.1~9I.20 = 31 个页面
- 当前侦察进度(全项目 47%)**不等于 Phase 1 范围侦察进度**
- **Phase 1 相关侦察进度需要单独审计**

### 4.5 F4 校正后结论

**【S1-170A 显式】**:
- S1-170 把"全项目 ≥80% 侦察"作为**Hard blocker** 是**错误的**
- 正确分类:**Scope-dependent prerequisite** + 需要单独审计 Phase 1 相关页面侦察进度
- 不得作为"全项目绝对门槛"

---

## §5. API / Object / State 统计口径复核

### 5.1 S1-170 §4.3 原文

**【S1-170 §4.3.1 API 数量与状态】**:
| 维度 | 实际状态 |
|---|---|
| 当前冻结 API 数 | **0 个完整冻结** |
| 老板指令中提到"约 40 个 API" | **未冻结** |
| API 契约(request / response / state change / transaction boundary / authorization / company isolation / error)| **0 个完整冻结** |

### 5.2 API 真实冻结状态(232 + 233)

**【S1-170A 关键发现 P1-04-1】**:**API-001 ~ API-040 已经在 S1-167 / S1-167A 完整冻结**。

**【232_S1-167_40个API字段级设计.md §1】** 显式列出:

| API 编号 | API 名称 | 方法 | 路径 | 模块 | 状态动作 | 权限角色 |
|---|---|---|---|---|---|---|
| API-001 | appointment/create | POST | /api/appointment/create | Appointment | 创建 DRAFT | RECEP / ADMIN |
| API-002 | appointment/update | PUT | /api/appointment/update | Appointment | 更新 DRAFT/CONFIRMED | RECEP / ADMIN |
| API-003 | appointment/confirm | POST | /api/appointment/confirm | Appointment | DRAFT → CONFIRMED | RECEP / ADMIN |
| API-004 | appointment/cancel | POST | /api/appointment/cancel | Appointment | 任意非终态 → CANCELLED | RECEP / ADMIN |
| API-005 | appointment/reschedule | POST | /api/appointment/reschedule | Appointment | CONFIRMED/WAITING_ARRIVAL → RESCHEDULED + 新 CONFIRMED | RECEP / ADMIN |
| API-006 | appointment/detail | GET | /api/appointment/detail | Appointment | 无状态变更 | RECEP / TRIAGE / DOCTOR / ADMIN |
| API-007 | appointment/list | POST | /api/appointment/list | Appointment | 无状态变更 | RECEP / TRIAGE / DOCTOR / ADMIN |
| API-008 | appointment/today | GET | /api/appointment/today | Appointment | 无状态变更 | RECEP / DOCTOR / ADMIN |
| API-009 | schedule/create | POST | /api/schedule/create | Schedule | 创建 ACTIVE/INACTIVE | ADMIN |
| API-010 | schedule/update | PUT | /api/schedule/update | Schedule | 更新排班 | ADMIN |
| API-011 | schedule/publish | POST | /api/schedule/publish | Schedule | DRAFT/INACTIVE → ACTIVE | ADMIN |
| API-012 | schedule/cancel | POST | /api/schedule/cancel | Schedule | ACTIVE → CANCELLED | ADMIN |
| API-013 | schedule/detail | GET | /api/schedule/detail | Schedule | 无状态变更 | ADMIN / DOCTOR / RECEP |
| API-014 | schedule/list | POST | /api/schedule/list | Schedule | 无状态变更 | ADMIN / DOCTOR / RECEP |
| API-015 | schedule/slot/close | POST | /api/schedule/slot/close | Schedule | AVAILABLE/FULL → CLOSED | ADMIN |
| API-016 | arrival/checkin | POST | /api/arrival/checkin | Arrival | 4 对象同步创建 | RECEP / STAFF / ADMIN |
| API-017 | arrival/cancel | POST | /api/arrival/cancel | Arrival | 撤销签到(待确认)| RECEP / ADMIN |
| API-018 | arrival/list | POST | /api/arrival/list | Arrival | 无状态变更 | RECEP / TRIAGE / DOCTOR / ADMIN |
| API-019 | triage/list | POST | /api/triage/list | Triage | 无状态变更 | TRIAGE / ADMIN |
| API-020 | triage/auto-assign | POST | /api/triage/auto-assign | Triage | IN_POOL → ASSIGNED(批量)| SYSTEM / ADMIN |
| API-021 | triage/assign | POST | /api/triage/assign | Triage | IN_POOL → ASSIGNED | TRIAGE / ADMIN |
| API-022 | triage/reassign | POST | /api/triage/reassign | Triage | ASSIGNED → IN_POOL | TRIAGE / ADMIN |
| API-023 | triage/remove | POST | /api/triage/remove | Triage | IN_POOL → REMOVED | TRIAGE / ADMIN |
| API-024 | queue/start | POST | /api/queue/start | Queue | ASSIGNED → WAITING | DOCTOR |
| API-025 | queue/pause | POST | /api/queue/pause | Queue | 暂停(仅 Doctor 状态)| DOCTOR |
| API-026 | queue/next | POST | /api/queue/next | Queue | WAITING → CALLED(自动选下一位)| DOCTOR |
| API-027 ~ API-040 | (后续)| ... | ... | ... | ... | ... |

**【S1-170A 抽样核验 232 §2 API-021】**:
- API-021 triage/assign
- Request 字段: triageQueueId / employeeId / consultRoomId
- Response 字段: code / data.triageQueueId / data.receptionQueueId / data.appointmentId / data.status / data.visitStatus
- 状态迁移:TriageQueue IN_POOL → ASSIGNED + ReceptionQueue INSERT(ASSIGNED)+ Appointment TRIAGE_WAITING → WAITING_RECEPTION + Visit CHECKED_IN → TRIAGED
- 事务边界:**4 对象同步**
- 错误码:`TRIAGE_NOT_FOUND` / `TRIAGE_ASSIGN_INVALID_STATE` / `TRIAGE_EMPLOYEE_INVALID` / `TRIAGE_ROOM_INVALID`
- 审计:action = "triage.assign"

**【S1-170A 显式】**:每个 API **完整冻结了**:
- ✓ 请求字段(类型 / 必填 / 说明)
- ✓ 响应字段(类型 / 必填 / 说明)
- ✓ 状态迁移路径
- ✓ 事务边界
- ✓ 错误码
- ✓ 审计要求
- ✓ 权限角色

**S1-170 §4.3 的 "API 契约 = 0 个完整冻结" 是完全错误的**。

### 5.3 Object 真实冻结状态(229 / 235B / 236B)

**【S1-170A 关键发现 P1-04-2】**:**12 个 Object 在 S1-167B / S1-168 / S1-169 已经完整冻结**。

**【238_S1-169_实施前置映射基线.md §2】** 显式列出:

**复用对象 6 个**(原系统实体 / 沿用 / BIGINT PK):
| # | 业务对象 | 表名 | PK | ID 类型 |
|---:|---|---|---|---|
| 1 | Company | `company` | `companyId` | BIGINT AUTO_INCREMENT |
| 2 | Customer | `customer` | `customerId` | BIGINT AUTO_INCREMENT |
| 3 | Patient | `patient` | `patientId` | BIGINT AUTO_INCREMENT |
| 4 | Employee | `employee` | `employeeId` | BIGINT AUTO_INCREMENT |
| 5 | ConsultRoom | `consult_room` | `consultRoomId` | BIGINT AUTO_INCREMENT |
| 6 | BigScreen | `big_screen` | `bigScreenId` | BIGINT AUTO_INCREMENT |

**新建对象 6 个**(本轮设计 / UUID PK):
| # | 业务对象 | 表名 | PK | ID 类型 |
|---:|---|---|---|---|
| 7 | AppointmentSchedule | `appointment_schedule` | `scheduleId` | CHAR(36) UUID v4 |
| 8 | AppointmentSlot | `appointment_slot` | `slotId` | CHAR(36) UUID v4 |
| 9 | Appointment | `appointment` | `appointmentId` | CHAR(36) UUID v4 |
| 10 | Visit | `visit` | `visitId` | CHAR(36) UUID v4 |
| 11 | TriageQueue | `triage_queue` | `triageQueueId` | CHAR(36) UUID v4 |
| 12 | ReceptionQueue | `reception_queue` | `receptionQueueId` | CHAR(36) UUID v4 |

**【S1-170 §4.1.1 原文】**:
> Customer / Patient / Employee / ConsultRoom / Appointment / AppointmentSchedule / AppointmentSlot / TriageQueue / ReceptionQueue / Visit 等核心业务对象在 S1-169 中仅有目录占位,无完整 Effective Spec

**【S1-170A 显式】**:**S1-170 §4.1.1 严重错误**。这 10 个 Object **全部已经在 229 / 235B / 236B / 238 完整冻结**,S1-170 完全没审计这些历史文档。

**【229_S1-166A §4.1 显式】**:
> A 复用实体(6):Company / Customer / Patient / Employee / ConsultRoom / BigScreen
> B 新增实体(6):Appointment / AppointmentSchedule / AppointmentSlot / TriageQueue / ReceptionQueue / Visit

**【229 §4.2 显式】**:
> AppointmentStatus(12) + VisitStatus(7) + TriageQueueStatus(4) + ReceptionQueueStatus(6) = **29 状态**

### 5.4 State 真实冻结状态(229)

**【S1-170A 关键发现 P1-04-3】**:**4 个核心状态机 29 状态已经在 S1-166A 完整冻结**。

| 状态机 | 状态数 | 状态 |
|---|---:|---|
| AppointmentStatus | 12 | DRAFT / CONFIRMED / WAITING_ARRIVAL / ARRIVED / TRIAGE_WAITING / WAITING_RECEPTION / CALLED / IN_CONSULTATION / COMPLETED / CANCELLED / NO_SHOW / RESCHEDULED |
| VisitStatus | 7 | DRAFT / CHECKED_IN / TRIAGED / IN_CONSULTATION / COMPLETED / TRANSFERRED / CANCELLED |
| TriageQueueStatus | 4 | IN_POOL / ASSIGNED / REMOVED / CANCELLED |
| ReceptionQueueStatus | 6 | ASSIGNED / WAITING / CALLED / SKIPPED / IN_CONSULTATION / DONE |
| **合计** | **29** | — |

**【S1-170 §4.4.1 原文】**:
> **UserCompany**(setDefaultCompany) | ✓ 部分 | 241V2A-11 §4 / 36 / 37:exactly-one 冻结
> Appointment / Visit / TriageQueue / ReceptionQueue / Employee / Company | ✗ | 仅目录

**【S1-170A 显式】**:**S1-170 §4.4.1 严重错误**。4 个核心状态机(Appointment / Visit / TriageQueue / ReceptionQueue)+ 29 状态**已经在 229 完整冻结**,S1-170 完全没审计。

### 5.5 S1-170 §4.5 关键结论错误

**【S1-170 §4.5 原文】**:
> | 维度 | 状态 | 阻塞开发? |
> | API 契约 | ✗ 完全未冻结 | **是** |
> | State 状态机 | ✗ 仅 UserCompany 冻结 | **是** |

**【S1-170A 校正】**:
- **API 契约 = 40 个完整冻结(232 + 233)** → ✗ 不再阻塞
- **State 状态机 = 4 个核心状态机 29 状态完整冻结(229) + UserCompany exactly-one 冻结(241V2A-11)** → ✗ 不再阻塞

### 5.6 统计口径错误根因

**【S1-170A 显式】**:

| S1-170 表述 | 真实情况 | 错误原因 |
|---|---|---|
| API = 0 冻结 | 40 个冻结 | **S1-170 §2.1 范围仅审计 S1-169,完全没审计 232/233** |
| Object = 3 冻结 | 12 冻结 | **S1-170 §2.1 范围仅审计 S1-169,完全没审计 229/235B/238** |
| State = 1 冻结 | 4 状态机 29 状态 + UserCompany | **S1-170 §2.1 范围仅审计 S1-169,完全没审计 229** |

**【S1-170A 显式】**:S1-170 的统计口径错误**根因**是把"老板指令中提到约 40 个 API"误解为"40 个 API 尚未冻结",并把"S1-169 本批次没有重新冻结业务对象"误写为"项目尚未冻结业务对象"。

---

## §6. S1-169 Scope vs Project Scope 分离

### 6.1 S1-170 实际回答的问题 vs 应该回答的问题

**【S1-170A 显式】**:

| 问题 | S1-170 实际回答 | S1-170 应该回答 |
|---|---|---|
| **问题 A**:"S1-169 全系列做得是否严谨?" | 隐含涉及 | **核心**(标题是 Pre-Development Integrity Audit,§1.1 显式)|
| **问题 B**:"OptFlow PMS 整个项目是否可以开始 Phase 1 开发?" | 隐含涉及 | **核心**(标题 Pre-Development)|

### 6.2 S1-170A 显式分离

#### 6.2.1 S1-169 Scope Readiness

**S1-169 范围内**(只审计 S1-169 + 5 份项目核心):
- ✓ Effective Spec 完整(41 份补丁 + 7 份 P2 关闭)
- ✓ P0 = 0 / P1 = 0
- ✓ 五级证据体系完整(241V2A-19)
- ✓ P2-0/1/2 CLOSED(241V2A-36/37/38/39/40/41/42)
- ✓ 补丁链膨胀审计 PASS(0 Circular,0 Administrative)
- ⚠️ V2A-42 §5.2 / §5.7 疑点一、二需要进一步校正

#### 6.2.2 Project Development Readiness

**整个 OptFlow PMS 范围**(审计 232 + 233 + 229 + 235B + 236B + 20x~22x):
- ✓ 12 个 Object 完整冻结(238 §2)
- ✓ 4 个状态机 29 状态完整冻结(229 §4.2)
- ✓ 40 个 API 字段级契约完整冻结(232 + 233)
- ✓ 31 真 FK / 21 索引 / 10 CHECK / 5 UNIQUE 完整冻结(236B §1.1)
- ⚠️ Production Implementation = NOT YET VERIFIED(backend/ 未创建)
- ⚠️ Runtime Test Execution = NOT EXECUTED(测试未运行)
- ⚠️ Phase 1 范围(诊所管理 + 系统设置)侦察进度未单独审计
- ⚠️ V2A-42 §5.2 / §5.7 疑点需要进一步校正

### 6.3 S1-170 范围错配的纠正

**【S1-170A 显式纠正】**:
- S1-170 §1.1 写"S1-169 全系列文档"作为审计范围,**这是范围 A**
- 但 S1-170 §4.3 / §4.4 / §4.5 推断到"OptFlow PMS 整个项目",**这是范围 B**
- **S1-170 把范围 A 的审计结果用范围 B 的措辞表达** → 范围错配
- **正确做法**:S1-170 应该明确分两段,范围 A 的判定与范围 B 的判定分开

---

## §7. Current Effective Spec Universe 重建

### 7.1 Layer 分层(按 241V2A-19 / 22 + S1-170A 校正)

| Layer | 含义 | 验证手段 |
|---|---|---|
| **Layer 1** | 历史文档 | 文件存在 |
| **Layer 2** | 已验证事实 | 多维证据交叉 |
| **Layer 3** | OptFlow设计 | 文档显式冻结 |
| **Layer 4** | Effective Spec | 当前有效规格(未作废)|
| **Layer 5** | Implementation Contract | 待 backend/ 实施时建立 |
| **Layer 6** | Production Implementation | backend/ 实际代码 |
| **Layer 7** | Runtime Verification | 实际运行测试 |

### 7.2 关键领域当前状态矩阵

**【S1-170A 显式】** 只填有证据的内容,无证据写"未在本次审计范围内证明"。

| 领域 | 历史来源 | 当前有效 Spec | Implementation Contract | Production | Runtime |
|---|---|---|---|---|---|
| **Tenant** | 240(跨公司隔离正式裁决)| 241V2 §5.4(双层防御 + 状态机)+ 241V2 §6(TenantLine)| 241V2 §6 设计但 IGNORE_TABLES 完整清单待核验 | NOT YET STARTED | NOT YET EXECUTED |
| **Company** | 239 / 239A(V4.3 真实结构)| 235B §6.3 + 236B §4(31 真 FK 关系矩阵)+ 241V2 §12(user_company schema)| 241V2 §12.1 user_company 字段级 schema | NOT YET STARTED | NOT YET EXECUTED |
| **UserCompany** | 239A(V4.3 真实存在)| 241V2A-11 §4 + 241V2A-36 / 37(exactly-one 业务规则)| 241V2A-10 / 11(Mapper / Repository 契约)| NOT YET STARTED | NOT EXECUTED |
| **Appointment** | 225 / 226 / 227 / 228 / 229(S1-162 ~ S1-166A)| 229 §4.2(AppointmentStatus 12 状态)+ 229 §5.4(Appointment 1:N Visit)| 232 API-001 ~ API-008(8 个 API 字段级契约)+ 233 修正版 | NOT YET STARTED | NOT EXECUTED |
| **Visit** | 229 §6.2(VisitStatus 7 状态)| 229 §6.2 + 232 API-027~028(部分 API)| 待 S1-169-2 实施 | NOT YET STARTED | NOT EXECUTED |
| **TriageQueue** | 229 §6.3(TriageQueueStatus 4 状态)| 229 §6.3 + 232 API-019 ~ API-023(5 个 API)| 待 S1-169-2 实施 | NOT YET STARTED | NOT EXECUTED |
| **ReceptionQueue** | 229 §6.4(ReceptionQueueStatus 6 状态)| 229 §6.4 + 232 API-024 ~ API-028(部分 API)| 待 S1-169-2 实施 | NOT YET STARTED | NOT EXECUTED |
| **SystemSetting** | 220(诊所管理)+ 221(SystemSetting 子模块)| 221 §(SystemSetting 全量审计)+ 232 SystemSetting 相关 API | 待 S1-169-2 实施 | NOT YET STARTED | NOT EXECUTED |
| **API** | 232(40 API)+ 233(修正版)| **232 + 233 完整冻结** 40 个 API 字段级契约 | 待 backend/ 实施时建立 | NOT YET STARTED | NOT EXECUTED |
| **State** | 229(4 状态机 29 状态)| **229 完整冻结** 4 状态机 + 29 状态 + 状态转换路径 | 232 API 状态迁移定义 | NOT YET STARTED | NOT EXECUTED |
| **DDL** | 236(DDL 草案)+ 236A(修正版)+ 236B(文字纠错)| **236B 完整冻结** 12 表 + 31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE | 236B §4 逐表 FK 锁定 | NOT YET STARTED | NOT EXECUTED |

### 7.3 与 S1-170 §3 规范形成链对比

**【S1-170 §3 期望链】**:
```
原系统证据 → 已验证业务事实 → OptFlow设计 → Effective Spec → Implementation Contract → Production Implementation → Runtime Verification
```

**【S1-170A 实际填充】**:
- 原系统证据:**239A**(V4.3 真实 backend 结构)+ **240**(跨公司隔离)
- 已验证业务事实:**235B §6.3**(31 真 FK 关系矩阵)
- OptFlow设计:**229 / 232 / 233 / 235 / 236 / 238 / 241V2**
- Effective Spec:**完整冻结**(12 Object + 40 API + 29 状态 + 31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE)
- Implementation Contract:**部分冻结**(user_company schema + DEFAULT-01~05 测试设计 + IGNORE_TABLES 分类原则)
- Production Implementation:**NOT YET STARTED**(backend/ 未创建)
- Runtime Verification:**NOT YET EXECUTED**(测试未运行)

---

## §8. Effective Spec / Implementation / Runtime 分层

### 8.1 S1-170 已建立的三层状态模型(241V2A-37)

```
Effective Spec: CLOSED / NOT YET VERIFIED
Production Implementation: NOT YET VERIFIED
Runtime Test Execution: NOT EXECUTED
```

### 8.2 S1-170A 强化后的分层模型

| 层 | 内容 | 当前状态 |
|---|---|---|
| **Effective Spec** | OptFlow PMS 当前有效规格(12 Object + 40 API + 29 状态 + DDL + Tenant)| **完整冻结** |
| **Implementation Contract** | 待 backend/ 实施时建立的 Java Entity / Repository / Service / Controller 映射 | **部分冻结**(user_company schema + DEFAULT-01~05)|
| **Production Implementation** | backend/ 实际代码 | **NOT YET STARTED** |
| **Runtime Test Execution** | 实际运行测试 | **NOT YET EXECUTED** |

### 8.3 三层独立的判定

**【S1-170A 显式】**:
- Effective Spec 完整 ≠ Production Implementation 完成
- Implementation Contract 部分冻结 ≠ Production Implementation 完成
- Production Implementation 完成 ≠ Runtime Test 通过

任何报告如果混淆这三层,都会导致**审计结论错配**。

---

## §9. S1-170 原结论逐项复核

### 9.1 S1-170 原结论矩阵

| 原结论 | 原依据 | 本次核验 | 当前状态 | 是否需要修正 |
|---|---|---|---|:-:|
| **C1**:S1-170 审计对象 = 60 S1-169 + 5 项目核心 | §2.1 计数 | 实际 56 份(S1-169 全系列 51 + 项目核心 5)| **数字错误** | ✓ 需要修正 |
| **C2**:41 份 S1-169-1 补丁 | §7.2 计数 | 实际 36 份(241V2A P0-2 + 241V2A-1 ~ 35)| **数字错误** | ✓ 需要修正 |
| **C3**:40 True / 3 Wording / 5 Self-Induced | §7.4 分类 | 需重新核对分类 | **部分错误** | ✓ 需要修正 |
| **C4**:API = 0 冻结 | §4.3 | 实际 40 冻结(232 + 233)| **严重错误** | ✓ 需要修正 |
| **C5**:Object = 3 冻结(User/UserCompany/Company)| §4.1 | 实际 12 冻结(238 §2)| **严重错误** | ✓ 需要修正 |
| **C6**:State = UserCompany only | §4.4 | 实际 4 状态机 29 状态 + UserCompany(229)| **严重错误** | ✓ 需要修正 |
| **C7**:F4 ≥80% 全局侦察 = Hard blocker | §8.2 F4 | 应为 Scope-dependent prerequisite | **错误分类** | ✓ 需要修正 |
| **C8**:判定 CONDITIONAL | §9 | 应分开判定(S1-169 scope / Project scope)| **范围错配** | ✓ 需要修正 |
| **C9**:R1 风险(241V2A-15 → 241V2A-40 循环引用)| §10.1 R1 | 该判断成立,但忽略了 232~238 之间的循环引用 | **不完整** | ✓ 需要扩展 |
| **C10**:V2A-36~42 修正链稳定 | §7.3 | V2A-42 疑点一、二需要进一步校正 | **部分成立** | ✓ 需要修正 |

### 9.2 修正后结论矩阵

**【S1-170A 显式】**:

| 维度 | S1-170 原结论 | S1-170A 校正结论 |
|---|---|---|
| **C1 审计对象数量** | 60 + 5 = 65 | **56**(S1-169 全系列 51 + 项目核心 5)|
| **C2 S1-169-1 补丁数量** | 41 | **36**(241V2A P0-2 + 241V2A-1 ~ 35)|
| **C3 分类** | 40 / 3 / 5 / 0 / 0 | **41 / 3 / 5 / 0 / 0**(S1-170A 重分类,需进一步细查)|
| **C4 API 冻结数** | 0 | **40**(232 + 233)|
| **C5 Object 冻结数** | 3 | **12**(229 + 235B + 236B + 238)|
| **C6 State 冻结数** | 1(UserCompany)| **4 状态机 29 状态 + UserCompany**(229 + 241V2A-11)|
| **C7 F4 分类** | Hard blocker | **Scope-dependent prerequisite** |
| **C8 判定** | CONDITIONAL(隐含项目范围)| **需分开**:S1-169 scope = READY,Project scope = CONDITIONAL |
| **C9 R1 风险** | 241V2A-15 → 241V2A-40 循环引用 | 应增加 **R1'**:232 / 233 与 S1-169 之间可能存在循环引用 |
| **C10 V2A-42** | 修正链稳定 | **P2-2 实质裁决稳定** + **V2A-42 §5.2 / §5.7 需进一步校正** |

---

## §10. 风险登记

### 10.1 P1 风险(必须修正)

| # | 风险 | 严重度 | 来源 |
|---:|---|:-:|---|
| **P1-01** | S1-170 审计对象集合不完整(漏算 241V4 / 241V2A;完全漏审计 232~238 + 20x~22x)| **高** | §2.1 / §2.3 |
| **P1-02** | V2A-42 §5.2 把 OpenJDK 内部结构表述为普遍规范 + §5.7 GC eligibility 三条件混淆 GC eligibility 与 GC 执行 | **中** | §3.6.1 / §3.6.2 |
| **P1-03** | F4 ≥80% 错误归类为 Hard blocker,实际应为 Scope-dependent prerequisite | **高** | §4 |
| **P1-04** | API / Object / State 统计严重错误(40 API / 12 Object / 4 状态机 29 状态 已经在 S1-167/168/169 冻结,S1-170 误写为 0 / 3 / 1)| **高** | §5 |
| **P1-05** | S1-169 scope 与 Project scope 范围错配,导致结论推广错误 | **高** | §6 |

### 10.2 P2 风险(需关注但不阻塞)

| # | 风险 | 严重度 | 来源 |
|---:|---|:-:|---|
| **P2-01** | V2A-42 疑点一(GC eligibility 三条件混淆 GC eligibility 与 GC 执行)| 中 | §3.6.1 |
| **P2-02** | V2A-42 疑点二(OpenJDK 内部结构表述为普遍规范)| 中 | §3.6.2 |
| **P2-03** | S1-170 §7.2 "41 份 S1-169-1 补丁"实际 36 份 | 低 | §9.1 C2 |
| **P2-04** | S1-170 §2.1 "60 份 S1-169"实际 51 份 | 低 | §9.1 C1 |

---

## §11. Final Decision

### 11.1 三个独立结论

#### 结论 A:S1-170 Audit Validity(S1-170 审计报告自身有效性)

**【S1-170A 显式】**:**FAIL**

理由:
- 审计对象集合不完整(漏算 241V4 / 241V2A;完全漏审计 232~238 + 20x~22x)
- 关键数字错误(60 / 65 / 41 / 0 / 3 / 1)
- 范围错配(把 S1-169 scope 推断为 Project scope)
- 统计口径错误(API = 0 / Object = 3 / State = 1 与仓库真实状态严重不符)
- F4 ≥80% 门槛错误归类为 Hard blocker

**S1-170 不能作为可靠审计依据**。S1-170A 必须重新校正经修正后才能成为有效审计报告。

#### 结论 B:S1-169 Scope Readiness(S1-169 范围内开发准备度)

**【S1-170A 显式】**:**READY**

理由:
- ✓ Effective Spec 完整(41 份 P1/P2 修复 + 7 份 P2 关闭)
- ✓ P0 = 0 / P1 = 0
- ✓ 五级证据体系完整(241V2A-19)
- ✓ P2-0/1/2 CLOSED(Effective Spec)
- ✓ 补丁链膨胀审计 PASS(0 Circular,0 Administrative)
- ⚠️ V2A-42 §5.2 / §5.7 疑点一、二需要进一步校正(不影响 P2-2 KEEP 裁决)

S1-169 范围内所有 P0/P1/P2 全部 CLOSED(Effective Spec 层),S1-169 范围内的基础设施 + 异常体系 + DEFAULT 测试设计 + UserCompany exactly-one 业务规则已经完整冻结,**S1-169 范围内可以直接进入 S1-169-2 backend/ 实施**。

#### 结论 C:OptFlow PMS Phase 1 Development Readiness(整个项目 Phase 1 开发准备度)

**【S1-170A 显式】**:**CONDITIONAL**

理由:
- ✓ 整个项目 Effective Spec 已完整冻结(12 Object + 40 API + 4 状态机 29 状态 + DDL 31 真 FK + 21 索引 + 10 CHECK + 5 UNIQUE)
- ⚠️ Production Implementation = NOT YET STARTED(backend/ 未创建)
- ⚠️ Runtime Test Execution = NOT EXECUTED(测试未运行)
- ⚠️ Phase 1 范围(诊所管理 + 系统设置)侦察进度未单独审计
- ⚠️ V2A-42 §5.2 / §5.7 疑点需要进一步校正

整个 OptFlow PMS 的 Effective Spec 层已基本就绪,但 Production Implementation 与 Runtime Test 仍是空白,Phase 1 范围侦察进度需单独审计。

### 11.2 三个结论的独立性

**【S1-170A 显式】**:
- 结论 A(S1-170 自身 FAIL)≠ 结论 B(S1-169 scope READY)
- 结论 B(S1-169 scope READY)≠ 结论 C(Project CONDITIONAL)
- **三个结论必须相互独立,不能合并**

---

## §12. S1-171 Entry Conditions

### 12.1 S1-170A 显式禁止

- **当前禁止进入 S1-171**
- 即使 S1-169 scope READY,**S1-171 仍需额外条件**

### 12.2 S1-171 前必须完成的条件

**【S1-170A 显式列出】**:

| # | 条件 | 严重度 |
|---:|---|:-:|
| **E1** | 完成 V2A-42 §5.2 / §5.7 疑点一、二的进一步校正(新增 V2A-43 等校正补丁)| 阻塞 |
| **E2** | 完成 S1-170 数字 / 范围 / 统计口径的校正(可选,通过 S1-170A 已校正)| 不阻塞 S1-171 |
| **E3** | backend/ 实际创建 + 初始化 pom.xml + application.yml | 阻塞 |
| **E4** | Production Implementation Contract 完整建立(对应 Effective Spec 12 Object + 40 API)| 阻塞 |
| **E5** | DEFAULT-01~05 实际运行 + 测试通过 | 阻塞 |
| **E6** | Phase 1 范围(诊所管理 + 系统设置)侦察进度单独审计 | 推荐 |
| **E7** | IGNORE_TABLES 完整清单(基于 Phase 1 范围 12 表)| 阻塞 |
| **E8** | 生产数据库环境就绪 | 阻塞 |
| **E9** | V4.3 真实 schema 完整映射核验(已部分确认 236B)| 推荐 |
| **E10** | 公开 API 白名单完整清单核验(已部分确认 241V2 §5.6)| 推荐 |

### 12.3 不允许直接进入 S1-171 的理由

**【S1-170A 显式】**:
- V2A-42 §5.2 / §5.7 疑点一、二是**已知的语义问题**
- 如果直接进入 S1-171,**这些语义问题会被带入 Implementation Contract**
- **建议**:先完成 V2A-43 等校正补丁,再进入 S1-171

---

## §13. Evidence Index

| 关键结论 | 文件 | 章节 / 行号 |
|---|---|---|
| 40 API 完整冻结 | `232_S1-167_40个API字段级设计.md` | §1 40 API 总表(行 21-50+)|
| 12 Object 完整冻结 | `238_S1-169_实施前置映射基线.md` | §2.1 + §2.2(行 59-80+)|
| 4 状态机 29 状态 | `229_S1-166A_门诊预约接诊领域模型状态机二次修正版.md` | §4.2(行 59-65)|
| 31 真 FK 关系矩阵 | `236B_S1-168_DDL修正版_文字纠错.md` | §1.1(行 27-34)+ §5(31 真 FK 闭合矩阵)|
| 12 表 DDL 草案 | `236_S1-168_DDL草案.md` + `236A_S1-168_DDL修正版.md` | (全文)|
| exactly-one 业务规则 | `241V2A-11_S1-169-1_UserCompanyMapper前序契约一致性修复.md` | §4(全文)|
| 五级证据体系 | `241V2A-19_S1-169-1_证据等级统一校正补丁.md` | §2(全文)|
| V2A-42 疑点一 | `241V2A-42_S1-169-2_P2-2_JavaExecutor生命周期语义二次校正补丁.md` | §5.7(GC eligibility 三条件)|
| V2A-42 疑点二 | `241V2A-42_S1-169-2_P2-2_JavaExecutor生命周期语义二次校正补丁.md` | §5.2(ThreadPoolExecutor 内部结构)|
| 跨公司隔离裁决 | `240_S1-169_Q4跨公司隔离架构正式裁决.md` | (全文)|
| V4.3 真实 backend 结构 | `239A_S1-169-0_后端真实来源追踪调查.md` | (全文)|
| 项目核心规则 | `00_项目核心规则_认识论.md` | (全文)|
| 当前项目阶段 | `10_AI当前状态.md` | §项目概览 + §下一步 |

---

## §14. 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\S1-170A_Pre-Development_Integrity_Audit_校正报告.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base S1-170 | `S1-170_Pre-Development_Integrity_Audit.md`(不修改)|
| 严禁修改 | S1-170 / 任何历史 MD / 源码 / 数据库 |

---

**End of S1-170A**
