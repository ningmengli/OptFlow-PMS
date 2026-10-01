# 241V2A-42｜S1-169-2｜P2-2 Java Executor 生命周期语义二次校正补丁

---

## # 1. 补丁元数据

| 字段 | 内容 |
|---|---|
| Stage | S1-169-2 |
| Patch ID | 241V2A-42 |
| Issue ID | P2-2 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Patch Type | Java Executor 生命周期语义二次校正(非状态改变)|
| Priority | P2 |
| Date/Time | 2026-09-16 |
| Author | S1-169-2 独立审计 |
| Previous Patch | 241V2A-40(P2-2 KEEP)→ 241V2A-41(语义校正)→ 241V2A-42(本轮二次校正)|
| Scope | 仅本文件(241V2A-42) |

---

## # 2. 本轮目标

**不修改 241V2A-40 / 241V2A-41 / 任何其他历史 MD**。

**最终裁决保留**(与 241V2A-40 + 241V2A-41 完全一致):

```
P2-2 = CLOSED (Effective Spec, KEEP shutdown-only)

Production Implementation = NOT YET VERIFIED

Runtime Test Execution = NOT EXECUTED
```

**唯一动作**:新建本补丁,对 241V2A-41 中仍存在的两个 Java Executor 生命周期语义过强表述做二次校正:

- **P1**:不要把 local variable 等同于 ExecutorService 已经具备 GC eligibility
- **P2**:不要把 ThreadPoolExecutor 内部数据结构持有的 ExecutorService 引用路径等同于"已被 GC 回收"

**严禁**:
- 重新打开 P2-2
- 改变 KEEP shutdown-only 裁决
- 改变三层状态
- 修改 241V2A-40 / 241V2A-41 / 任何历史 MD

---

## # 3. 校正背景

241V2A-41 已经做了一次 Java Executor 生命周期语义校正,但仍存在**两个过强表述**:

| 编号 | 位置 | 过强表述 |
|---|---|---|
| **P1** | 241V2A-41 §4.6 / §11.2 / §11.5 | "local pool → ExecutorService 对象 GC eligibility = ✓(理论)";把 local variable 等同于 ExecutorService 已经具备 GC eligibility |
| **P2** | 241V2A-41 §11.2 第 3 项定义 | "ExecutorService 对象 GC eligibility = ExecutorService 对象已无强引用,可被 GC 回收"——这个定义**本身**忽略了 ThreadPoolExecutor 内部数据结构对 GC eligibility 的影响 |

两个问题都不影响 P2-2 最终裁决(KEEP shutdown-only),但需要校正措辞以避免:
- 把 local variable 等同于 GC eligibility
- 忽略 ThreadPoolExecutor 内部数据结构对 GC 的影响

---

## # 4. P1 校正:local variable ≠ GC eligibility

### 4.1 原表述问题(241V2A-41 中需要二次校正的部分)

**【241V2A-41 §4.6 当前精确表述】**:
| 状态 | 表述 |
|---|---|
| ExecutorService 已 shutdown | ✓ |
| 业务任务已到达 finally | ✓ |
| **worker threads 真正终止** | **未严格保证** |
| ExecutorService 对象 GC eligibility | **✓(理论)** ← **问题** |
| **GC 实际执行时点** | **不可预测** |

**【241V2A-41 §11.2 第 3 项定义】**:
> **ExecutorService 对象 GC eligibility**:ExecutorService 对象已无强引用,可被 GC 回收

### 4.2 严格区分五个概念(241V2A-42 显式建立)

**【241V2A-42 显式建立】** 必须严格区分以下五个概念,不可混淆:

| # | 概念 | 定义 | 关键约束 |
|---:|---|---|---|
| 1 | **局部变量生命周期** | 方法栈帧中存在该局部变量的时间区间 | 方法返回后,栈帧销毁,局部变量引用消失 |
| 2 | **对象是否还有可达引用路径** | 从 GC roots 是否存在引用链到达该对象 | 即使局部变量消失,对象仍可能有其他 GC root 引用路径 |
| 3 | **ExecutorService GC eligibility** | ExecutorService 对象**没有任何 GC root 引用路径** | 需要 worker thread 也释放对 ExecutorService 内部结构的引用 |
| 4 | **worker thread 真正终止** | ThreadPoolExecutor 中所有 worker thread 已退出 JVM 线程状态(TERMINATED)| 需要 `awaitTermination()` 返回 true |
| 5 | **JVM 何时实际执行 GC** | JVM GC 调度器选择执行 GC 的时机 | **不可预测**,与 GC eligibility 是不同概念 |

### 4.3 关键校正原则

**【241V2A-42 显式校正】**:

1. **局部变量生命周期 ≠ 对象 GC eligibility**
   - 局部变量只是该变量在栈帧中的引用
   - 局部变量消失只意味着"该引用源消失"
   - **不等于**"对象没有其他可达路径"
   - **不等于**"对象 GC-eligible"

2. **`pool` 是方法局部变量的精确含义**
   - `pool` 是 ExecutorService 类型的方法局部变量
   - 它只能证明:在方法栈帧存在期间,有这个引用
   - 方法返回后,该引用源消失
   - **但** ExecutorService 对象可能仍有其他 GC root 引用路径

3. **GC eligibility 的精确边界**
   - 必须从所有 GC roots 都没有引用路径到达 ExecutorService 对象
   - GC roots 包括:栈帧局部变量 / 静态字段 / 常量池 / JNI 引用 / 当前活跃线程栈 / Thread 对象本身
   - **ThreadPoolExecutor 的 worker thread 是活跃线程**,worker 线程的 Thread 对象是 GC root
   - 即使 local variable 销毁,**worker thread 可能仍持有 ThreadPoolExecutor 内部数据结构**(包括 ExecutorService 引用)
   - 所以 worker thread 未终止 → ExecutorService 对象仍可能通过 worker thread 可达 → ExecutorService **不** GC-eligible

4. **本轮校正的目的**
   - **不是为了证明** "local variable 销毁 = ExecutorService 已 GC"
   - **不是为了证明** "worker thread 已终止"
   - **是为了纠正** "local variable → GC eligibility = ✓" 的过强表述
   - 当前 KEEP 裁决仍然成立

### 4.4 严禁的过强表述

**【241V2A-42 显式严禁】** 以下表述**严禁出现**:

- ✗ "local pool → GC eligibility = ✓"
- ✗ "方法返回后 pool 理论上可以 GC" 作为确定性结论
- ✗ "local variable 证明 executor 可被 GC"
- ✗ "local pool 因而已经解决生命周期问题"
- ✗ "ExecutorService 对象 GC eligibility = ✓" 单独成立
- ✗ "local 变量 GC 回收" 作为 ExecutorService 已被回收的证据

### 4.5 允许保留的准确表述

**【241V2A-42 显式】** 以下表述**允许保留**:

> "DEFAULT-03 使用方法局部 ExecutorService,**减少跨测试共享 executor 带来的状态耦合**;但局部变量生命周期结束本身不足以证明 ExecutorService 已进入 GC eligibility,因为 ExecutorService 对象可能仍通过 ThreadPoolExecutor 内部数据结构被活跃 worker thread 持有。"

### 4.6 校正后状态(241V2A-42)

| 状态 | 表述 |
|---|---|
| ExecutorService 已 shutdown | ✓ |
| 业务任务已到达 finally | ✓ |
| **worker threads 真正终止** | **未严格保证** |
| **ExecutorService 对象 GC eligibility** | **未严格保证**(取决于 worker thread 是否仍持有 ThreadPoolExecutor 内部引用)|
| **GC 实际执行时点** | **不可预测** |

---

## # 5. P2 校正:ThreadPoolExecutor 内部数据结构对 GC eligibility 的影响

### 5.1 原表述问题(241V2A-41 §11.2 第 3 项定义)

**【241V2A-41 §11.2 第 3 项定义原表述】**:
> **ExecutorService 对象 GC eligibility**:ExecutorService 对象已无强引用,可被 GC 回收

**问题**:这个定义**简化了** ThreadPoolExecutor 内部数据结构对 GC eligibility 的影响。

### 5.2 ThreadPoolExecutor 内部数据结构精确分析

**【241V2A-42 显式建立】** ThreadPoolExecutor 内部数据结构:

```
ThreadPoolExecutor (extends AbstractExecutorService)
├── workers (HashSet<Worker>)
│   └── Worker (each worker holds)
│       ├── Thread thread (worker thread 对象)
│       └── Runnable firstTask (初始任务)
└── (内部状态: corePoolSize, maximumPoolSize, etc.)
```

**关键观察**:

| 对象 | 是否被 ThreadPoolExecutor 内部持有 |
|---|---|
| ThreadPoolExecutor 对象本身 | ✓(被 ExecutorService 接口引用,即 local variable `pool`) |
| Worker 对象 | ✓(被 ThreadPoolExecutor.workers HashSet 持有) |
| Worker 持有的 Thread 对象 | ✓(被 Worker.thread 字段持有) |
| Worker 持有的 Runnable 引用 | ✓(被 Worker.firstTask 字段持有) |

### 5.3 GC 引用链精确分析

**【241V2A-42 显式建立】** GC 引用链:

```
local variable `pool` (栈帧 GC root)
    ↓
ThreadPoolExecutor 对象
    ↓
workers HashSet
    ↓
Worker 对象
    ↓
Thread 对象 (活跃线程 → Thread 是 GC root)
```

**关键事实**:
- **活跃 Thread 对象本身就是 GC root**(线程运行时,栈和 Thread 对象不能被 GC)
- 即使 local variable `pool` 销毁,**worker Thread 仍在运行**(未终止)
- worker Thread → ThreadPoolExecutor → Worker → ThreadPoolExecutor 内部数据结构
- 整个引用链**通过 worker Thread 间接可达**

**所以**:
- local variable 销毁 ≠ ExecutorService 对象 GC-eligible
- worker Thread 未终止 → ThreadPoolExecutor 通过 worker Thread 间接可达 → **ExecutorService 不 GC-eligible**

### 5.4 关键校正原则

**【241V2A-42 显式校正】**:

1. **活跃 Thread 是 GC root**
   - Java 内存模型:活跃线程的 Thread 对象不能被 GC
   - 活跃线程的栈不能被 GC
   - 活跃线程通过栈帧 / Thread 字段持有的所有对象都可达

2. **ThreadPoolExecutor 通过 worker Thread 间接持有**
   - 即使 local variable `pool` 销毁
   - worker Thread 仍持有 ThreadPoolExecutor 内部数据结构
   - ThreadPoolExecutor 仍可达(通过 worker Thread → Worker → ThreadPoolExecutor)

3. **GC eligibility 的真实边界**
   - ExecutorService 对象 GC-eligible **当且仅当**:
     - local variable `pool` 已销毁(方法返回)
     - **且**所有 worker Thread 已终止(进入 TERMINATED 状态)
     - **且**没有其他 GC root 持有该 ExecutorService
   - 这就是为什么"worker thread 真正终止"是 GC eligibility 的前提条件

### 5.5 严禁的过强表述

**【241V2A-42 显式严禁】** 以下表述**严禁出现**:

- ✗ "ExecutorService 对象 GC eligibility = ExecutorService 对象已无强引用"
- ✗ "局部变量销毁后 ExecutorService 可被 GC"(忽略 worker Thread 间接持有)
- ✗ "ThreadPoolExecutor 与 worker Thread 互相独立"(实际通过 Worker 互相持有)
- ✗ "worker Thread 终止后 ExecutorService 立即 GC"(GC 时点不可预测)

### 5.6 允许保留的准确表述

**【241V2A-42 显式】** 以下表述**允许保留**:

> ExecutorService 对象 GC eligibility 取决于:**(a)** local variable 引用销毁;**(b)** 所有 worker thread 已终止释放 ThreadPoolExecutor 内部数据结构;**(c)** JVM GC 调度器实际执行 GC。三个条件**同时**满足时,ExecutorService 才进入 GC eligibility。

### 5.7 校正后 §11.2 第 3 项定义

**【241V2A-42 校正后】** §11.2 第 3 项定义应为:

> **ExecutorService 对象 GC eligibility**:ExecutorService 对象**没有任何 GC root 可达路径**——包括**(a)** 局部变量已销毁,**(b)** worker thread 已终止释放 ThreadPoolExecutor 内部数据结构,**(c)** JVM GC 调度器实际执行 GC。三个条件**同时**满足才成立。

---

## # 6. 校正后 P2-2 三层状态(完全保留)

### 6.1 P2-2 三层状态

```
P2-2 = CLOSED (Effective Spec, KEEP shutdown-only)
       ↑
       沿用 241V2A-40 §12.1 锁定结论

Production Implementation = NOT YET VERIFIED
       ↑
       沿用 241V2A-40 §12.1 锁定结论

Runtime Test Execution = NOT EXECUTED
       ↑
       沿用 241V2A-40 §12.1 锁定结论
```

### 6.2 Effective Spec 唯一写法(完全保留)

```java
ExecutorService pool = Executors.newFixedThreadPool(2);   // local pool
// ... submit / startLatch / endLatch.await / shutdown ...
pool.shutdown();                                          // ← KEEP shutdown-only
// 不增加 awaitTermination
```

---

## # 7. 校正前后对比

### 7.1 P1 校正前后

| 项目 | 241V2A-41 原表述 | 241V2A-42 校正后 |
|---|---|---|
| 局部变量与 GC 关系 | "local pool → GC eligibility = ✓(理论)" | 局部变量生命周期 ≠ GC eligibility |
| ExecutorService GC 边界 | "✓(理论)" 单一标志 | **未严格保证**(需 worker thread 也终止)|
| 严禁表述 | (未充分列出)| "local variable 证明 executor 可被 GC" 严禁 |

### 7.2 P2 校正前后

| 项目 | 241V2A-41 §11.2 第 3 项原表述 | 241V2A-42 校正后 |
|---|---|---|
| GC eligibility 定义 | "ExecutorService 对象已无强引用,可被 GC 回收" | "ExecutorService 对象没有任何 GC root 可达路径——包括 (a) 局部变量销毁 (b) worker thread 终止释放内部数据结构 (c) JVM GC 调度" |
| ThreadPoolExecutor 内部引用 | (忽略)| **活跃 worker Thread 是 GC root,通过 Worker 持有 ThreadPoolExecutor 内部数据结构** |
| GC eligibility 三条件 | (未明确)| (a) local variable 销毁 + (b) worker Thread 终止 + (c) JVM GC 执行 |

---

## # 8. 校正后严禁清单

### 8.1 P1 严禁(沿用 241V2A-41 + 本轮强化)

- ✗ "local pool → GC eligibility = ✓"
- ✗ "方法返回后 pool 理论上可以 GC" 作为确定性结论
- ✗ "local variable 证明 executor 可被 GC"
- ✗ "ExecutorService 对象 GC eligibility = ✓" 单独成立
- ✗ "local 变量 GC 回收" 作为 ExecutorService 已被回收的证据

### 8.2 P2 严禁(本轮新增)

- ✗ 把 GC eligibility 等同于"ExecutorService 对象已无强引用"
- ✗ 忽略 ThreadPoolExecutor 通过活跃 worker Thread 间接持有 ExecutorService 内部数据结构
- ✗ 把活跃 Thread 不当 GC root
- ✗ 把"local variable 销毁"与"ExecutorService GC-eligible"等同

### 8.3 仍然保留的严禁(沿用 241V2A-41)

- ✗ 把 GC eligibility 作为 worker thread 已终止的证据
- ✗ 把 `endLatch.await()` 等同于 `awaitTermination()`
- ✗ 把 "改 local pool" 描述为 "线程生命周期优化"
- ✗ 在没有新独立补丁 + 一致性复核的情况下,**单独**修改 DEFAULT-03 添加 awaitTermination
- ✗ 把当前 KEEP 裁决误解为"awaitTermination 永远禁止"
- ✗ 重新打开 P2-2

---

## # 9. 影响范围

| 范围 | 影响 |
|---|---|
| 生产代码 | **0 改动** |
| 241V2A-40 / 241V2A-41 | **0 改动**(本轮不修改)|
| 任何其他历史 MD(241V2A-1 ~ 241V2A-41) | **0 改动** |
| VisionCare PMS | **0 改动** |
| backend/ | **0 创建** |
| P2-0 / P2-1 / P2-6 / P2-7 / P2-8 | **0 改动** |
| P2-2 状态 | **0 改动**(仍 CLOSED,KEEP) |
| P2-2 三层状态 | **0 改动** |

**本轮唯一动作**:新增 `241V2A-42_*.md`,通过显式校正叠加建立更准确的语义表述。

---

## # 10. 其他 P2 状态(显式 NOT TOUCHED)

```
P2-0 = CLOSED(Effective Spec) [241V2A-36 + 37]
P2-1 = CLOSED(Effective Spec, DELETE) [241V2A-38 + 39]
P2-2 = CLOSED(Effective Spec, KEEP shutdown-only) [241V2A-40 + 41 + 42 三次语义校正]
P2-6 = NOT TOUCHED
P2-7 = NOT TOUCHED
P2-8 = NOT TOUCHED
```

---

## # 11. 反证检查

### 11.1 反问 1:本轮二次校正是否改变了 P2-2 最终裁决?

**回答**:**否**。
- P2-2 = CLOSED(Effective Spec, KEEP shutdown-only)
- 与 241V2A-40 + 241V2A-41 完全一致
- 本轮只二次校正措辞

### 11.2 反问 2:本轮二次校正是否改变了 P2-2 三层状态?

**回答**:**否**。
- Effective Spec: CLOSED
- Production Implementation: NOT YET VERIFIED
- Runtime Test Execution: NOT EXECUTED
- 与 241V2A-40 + 241V2A-41 完全一致

### 11.3 反问 3:本轮是否重新讨论了 KEEP / ADD?

**回答**:**否**。
- 本轮严格保持 KEEP shutdown-only
- 不重新讨论 KEEP / ADD
- 不改变 Effective Spec 唯一写法

### 11.4 反问 4:本轮二次校正是否影响了 241V2A-41 的内容?

**回答**:**否**。
- 241V2A-41 字节不变
- 本轮通过新建 241V2A-42 叠加校正
- 241V2A-41 仍是有效的语义校正

### 11.5 反问 5:本轮是否引入了新的 P0 / P1?

**回答**:**否**。
- 两个语义校正都是**审计精度**问题,不是新缺陷
- 不影响 P2-2 状态
- 不影响其他 P2 状态

---

## # 12. 最终状态

### 12.1 P2-2 三层状态(完全保留)

```
P2-2 = CLOSED (Effective Spec, KEEP shutdown-only)

Production Implementation = NOT YET VERIFIED

Runtime Test Execution = NOT EXECUTED
```

### 12.2 本轮两个校正点

| 校正点 | 方向 |
|---|---|
| **P1**:local variable ≠ ExecutorService GC eligibility | 严格区分 5 个概念,严禁 local variable 等同于 GC eligibility |
| **P2**:ThreadPoolExecutor 通过活跃 worker Thread 间接持有 | 校正 §11.2 第 3 项定义,GC eligibility 三条件 |

### 12.3 Effective Spec 锁定结论(完全保留)

**【241V2A-42 锁定】** DEFAULT-01 / DEFAULT-03 阶段 B 线程池处理:

```java
ExecutorService pool = Executors.newFixedThreadPool(2);   // local pool
// ... submit / startLatch / endLatch.await / shutdown ...
pool.shutdown();                                          // ← KEEP shutdown-only
// 不增加 awaitTermination
```

---

## # 13. 下一步

**等待独立盲审**。

任何未来的:
- P2-6 / P2-7 / P2-8 整改
- 241V2A-43 及以后的 S1-169-2 补丁
- backend/ 实际创建与实施验证
- DEFAULT-01 / DEFAULT-03 实际运行与执行验证
- DEFAULT-01 / DEFAULT-03 awaitTermination 路径的重新裁决(**需新独立补丁 + 一致性复核 + 业务裁决**)

**均需独立盲审后由老板下达指令**。

**严禁**:
- 自行开始 P2-6
- 自行在 DEFAULT-01 / DEFAULT-03 中**单独**添加 awaitTermination
- 自行声称"实施已完成"
- 自行声称"测试已通过"
- 自行 commit / push

---

## # 14. 附录:术语对齐(241V2A-42 二次校正后)

| 术语 | 241V2A-42 校正后定义 |
|---|---|
| 局部变量生命周期 | 方法栈帧中存在该局部变量的时间区间,方法返回后栈帧销毁 |
| 对象可达引用路径 | 从 GC roots 是否存在引用链到达该对象 |
| ExecutorService GC eligibility | ExecutorService 对象**没有任何 GC root 可达路径**——需 (a) 局部变量销毁 + (b) worker Thread 终止 + (c) JVM GC 调度 |
| 活跃 Thread 作为 GC root | 活跃线程的 Thread 对象和栈不能被 GC |
| ThreadPoolExecutor 内部数据结构 | 通过活跃 worker Thread → Worker → ThreadPoolExecutor 间接可达 |
| worker thread 真正终止 | ThreadPoolExecutor 中所有 worker Thread 已退出 JVM 线程状态(TERMINATED)|
| JVM GC 实际执行时点 | JVM GC 调度器选择执行 GC 的时机,不可预测 |
| shutdown() | 状态变更,阻止新任务,不等待已提交任务完成,不保证 worker 立即终止 |
| awaitTermination(timeout, unit) | 阻塞等待所有 worker 终止,超时返回 false |
| endLatch.await(timeout, unit) | 证明业务任务到达 finally 并完成其业务执行路径,**不等于** awaitTermination() 提供的 executor termination 等待 |
| local pool | 方法内局部 ExecutorService 变量,方法返回后**理论上**可 GC——但 GC eligibility 需 worker Thread 也终止 |
| 三层状态模型 | Effective Spec + Production Implementation + Runtime Test Execution(241V2A-37 §6.2)|

---

**End of 241V2A-42**
