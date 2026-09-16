# 241V2A-40｜S1-169-2｜P2-2 二选一正式裁决补丁(KEEP shutdown-only)

---

## # 1. 补丁元数据

| 字段 | 内容 |
|---|---|
| Stage | S1-169-2 |
| Patch ID | 241V2A-40 |
| Issue ID | P2-2 |
| Baseline HEAD | `6efa0daecd386eb022bd4ac1065e4b08ed529dc1` |
| Patch Type | Effective Spec 正式裁决(KEEP shutdown-only) |
| Priority | P2 |
| Date/Time | 2026-09-16 |
| Author | S1-169-2 独立审计 |
| Previous Patch | 241V2A-39(P2-1 正式裁决 DELETE)|

---

## # 2. 本轮目标

**唯一目标**:正式裁决 241V2A-16 §4.3 给出的二选一选项——
- A. 增加 awaitTermination
- B. 保留 shutdown-only 现状

通过建立**证据型决策矩阵**,基于已冻结 Effective Spec 给出最终选择。

**不修改生产代码 / 不修改任何历史 MD**。

---

## # 3. P2-2 原问题(精确还原)

### 3.1 事实源头(241V2A-15 §3.1 L308)

```java
startLatch.countDown();
boolean done = endLatch.await(5, TimeUnit.SECONDS);
pool.shutdown();    // ← **没有 awaitTermination**
```

### 3.2 P2-2 显式记录(241V2A-16 §4.3)

> **【241V2A-16 记录为 P2,显式保持,不得升级】**:
> - 241V2A-15 §3.1 DEFAULT-03 模板中 `pool.shutdown();` 后未调用 `awaitTermination(timeout, unit)` 等待资源清理
> - **不影响测试正确性**(`endLatch.await()` 已确保并发任务完成),但资源回收不显式
> - P2 状态:**功能正确但风格不完美**
> - 本轮**不修改** 241V2A-15,本轮**不创建** 241V2A-17
> - **留待后续单独裁决**(可以加 `awaitTermination` / 也可以保留现状)

### 3.3 P2-2 完整轨迹

| 文档 | P2-2 状态 |
|---|---|
| 241V2A-16 §4.3 / §5.1 | 显式记录 OPEN,留待单独裁决 |
| 241V2A-17 ~ 35 | 全部保持 OPEN(状态记录,但未修复)|
| 241V2A-36 / 37 | NOT TOUCHED |
| 241V2A-38 / 39 | NOT TOUCHED(P2-0 / P2-1 处理) |

---

## # 4. 关键概念区分(必须先建立)

### 4.1 业务任务完成 vs ExecutorService 完全终止

**【241V2A-40 显式建立】** 这两个是**完全不同的概念**:

| 概念 | 定义 | 实现机制 |
|---|---|---|
| **业务任务完成** | Runnable.run() / Callable.call() 方法体执行完毕 | T1/T2 的 try/catch/finally 块执行完毕,endLatch.countDown() 被调用 |
| **ExecutorService 完全终止** | ThreadPoolExecutor 中**所有 worker 线程**都已退出 | 需要 `shutdown()` + `awaitTermination()` 或 `shutdownNow()` |

**【241V2A-40 显式】** 不能用"业务任务完成"推断"ExecutorService 完全终止":
- `endLatch.await()` 只能证明 T1/T2 的 Runnable.run() 执行完毕(countDown 在 finally 块)
- **不能**证明 ThreadPoolExecutor 的 worker 线程已经退出 JVM 线程状态
- worker 线程在 Runnable.run() 返回后,可能仍在 ThreadPoolExecutor 的空闲 worker 集合中等待新任务
- 只有 `shutdown()` 之后的 `awaitTermination()` 或 `shutdownNow()` 才能保证 worker 完全终止

**关键区分**:`endLatch.await()` ≠ `pool.awaitTermination()`

### 4.2 shutdown() 的精确语义

**【通用技术事实,Java JDK 标准库】** `ExecutorService.shutdown()`:
- **不再接受新任务**(submit() 会抛 RejectedExecutionException)
- **不**等待已提交任务完成
- **不**中断正在执行的任务
- worker 线程在当前任务完成后**自然退出**或进入 idle 等待状态

**【通用技术事实】** `ExecutorService.awaitTermination(timeout, unit)`:
- 阻塞当前线程,直到:
  - 所有任务执行完毕 + worker 全部终止 → 返回 true
  - 超时 → 返回 false

**【通用技术事实】** `ExecutorService.shutdownNow()`:
- 尝试中断所有正在执行的任务
- 不等待任务完成
- 返回未开始执行的任务列表

### 4.3 关键边界:local pool vs static pool

| pool 类型 | 生命周期风险 | Effective Spec 现状 |
|---|---|---|
| **static pool**(类级别 static 变量) | 跨测试共享,JVM 不重启可能永不释放 | 241V2A-4 §5.1 原始 DEFAULT-01 用 static |
| **local pool**(方法内局部变量)| 测试方法返回后局部变量 GC 可回收 | 241V2A-14 §5.1 + 241V2A-15 §3.1 修订后用 local |

**【241V2A-40 显式】** 241V2A-4 → 241V2A-14/15 的修订本身就是**生命周期优化**(从 static 改 local)。

---

## # 5. DEFAULT-03 实际冻结时序(241V2A-15 §3.1 L276-313)

```
[阶段 A] TestDataFixture.prepareTestData() (REQUIRES_NEW commit)
    ↓
TestDataContext(userId, companyAId)
    ↓
[阶段 B] ExecutorService pool = Executors.newFixedThreadPool(2)
        ↓
        CountDownLatch startLatch = new CountDownLatch(1)
        CountDownLatch endLatch = new CountDownLatch(2)
        AtomicReference<Throwable> err1 = new AtomicReference<>();
        AtomicReference<Throwable> err2 = new AtomicReference<>();
        ↓
        pool.submit(() -> {              ← T1 submit
            try {
                startLatch.await();
                userCompanyService.setDefaultCompany(userId, companyAId);
            } catch (Throwable t) {
                err1.set(t);
            } finally {
                endLatch.countDown();    ← T1 finally 中 countDown
            }
        });
        pool.submit(() -> {              ← T2 submit
            try {
                startLatch.await();
                userCompanyService.setDefaultCompany(userId, companyAId);
            } catch (Throwable t) {
                err2.set(t);
            } finally {
                endLatch.countDown();    ← T2 finally 中 countDown
            }
        });
        ↓
        startLatch.countDown();           ← 主线程同步触发
        ↓
        boolean done = endLatch.await(5, TimeUnit.SECONDS);  ← 主线程等待
        ↓
        pool.shutdown();                  ← shutdown(不 awaitTermination)
        ↓
[阶段 B 成功性证明三道断言]
        assertThat(done).isTrue();
        assertThat(err1.get()).isNull();
        assertThat(err2.get()).isNull();
        ↓
[阶段 C] testVerifier.verifyFinalState(A, A)
        ↓
        assertThat(defaultCount).isEqualTo(1);
        assertThat(defaultCompanyId).isEqualTo(A);
        ↓
        测试方法返回
```

**【241V2A-40 显式】** shutdown 后**没有** awaitTermination,直接进入三道断言,然后是阶段 C,测试方法返回。

---

## # 6. DEFAULT-01~05 线程池生命周期矩阵

### 6.1 完整矩阵

| Test | pool 创建 | shutdown | awaitTermination | shutdownNow | 线程完成证明 | 来源 |
|---|---|---|---|---|---|---|
| **DEFAULT-01** | local pool(241V2A-14 §5.1) / static pool(241V2A-4 §5.1) | ✓ | ✗ | ✗ | endLatch.await | 241V2A-4 §5.1 + 241V2A-14 §5.1 |
| **DEFAULT-02** | ✗ 不使用 | N/A | N/A | N/A | N/A(串行) | 241V2A-5 §5.2 |
| **DEFAULT-03** | local pool(241V2A-15 §3.1) | ✓ | ✗ | ✗ | endLatch.await | 241V2A-15 §3.1 |
| **DEFAULT-04** | ✗ 不使用 | N/A | N/A | N/A | N/A(串行 + 异常) | 241V2A-5 §5.3 |
| **DEFAULT-05** | ✗ 不使用 | N/A | N/A | N/A | N/A(串行 + Spy throw) | 241V2A-5 §5.4 |

### 6.2 DEFAULT-01 / 03 一致性审计(241V2A-15 §4.1 显式)

**【241V2A-15 §4.1 显式冻结】** DEFAULT-01 与 DEFAULT-03 必须采用**同一并发调用成功性验证结构**(11 项结构完全一致):

| # | 维度 | DEFAULT-01 | DEFAULT-03 | 是否一致 |
|---:|---|---|---|:-:|
| 1 | `err1` / `err2` AtomicReference | ✓ | ✓ | ✓ |
| 2 | `startLatch` CountDownLatch(1) | ✓ | ✓ | ✓ |
| 3 | `endLatch` CountDownLatch(2) | ✓ | ✓ | ✓ |
| 4 | `pool.submit` 提交 T1/T2 | ✓ | ✓ | ✓ |
| 5 | `catch (Throwable t) { errX.set(t); }` | ✓ | ✓ | ✓ |
| 6 | `startLatch.countDown()` | ✓ | ✓ | ✓ |
| 7 | `endLatch.await(5, TimeUnit.SECONDS)` | ✓ | ✓ | ✓ |
| 8 | **`pool.shutdown()`** | ✓ | ✓ | ✓ |
| 9 | `assertThat(done).isTrue()` | ✓ | ✓ | ✓ |
| 10 | `assertThat(err1.get()).isNull()` | ✓ | ✓ | ✓ |
| 11 | `assertThat(err2.get()).isNull()` | ✓ | ✓ | ✓ |

**【241V2A-40 关键发现】** 第 8 项 `pool.shutdown()` 在 241V2A-15 §4.1 显式确认 DEFAULT-01 / 03 **完全一致**——shutdown-only 是**已冻结的统一模式**。

### 6.3 DEFAULT-01 池演变的两个版本

| 文档 | pool 类型 | 是否 awaitTermination |
|---|---|---|
| 241V2A-4 §5.1(原始)| `private static final ExecutorService pool`(类静态) | ✗ |
| 241V2A-14 §5.1(修订)| `ExecutorService pool = Executors.newFixedThreadPool(2);`(方法局部) | ✗ |

**【241V2A-40 关键发现】** 241V2A-4 → 241V2A-14 的池修改是**生命周期优化**(从 static 改 local),**不涉及 awaitTermination**。

### 6.4 严禁事实

- ✗ 没有任何 DEFAULT-01 / DEFAULT-03 模板使用 awaitTermination
- ✗ 没有任何 DEFAULT-01 / DEFAULT-03 模板使用 shutdownNow
- ✗ 没有 `@AfterEach` / `@AfterAll` 处理 pool
- ✗ 没有显式的 teardown 方法
- ✗ DEFAULT-02 / 04 / 05 不用线程池,不涉及此问题

---

## # 7. shutdown vs awaitTermination 精确分析

### 7.1 当前 DEFAULT-03 时序分析

| 时序节点 | 当前(241V2A-15) | 是否需要修改 |
|---|---|---|
| pool 创建(local)| ✓ 局部变量 | 不变 |
| T1 / T2 submit | ✓ 已提交 | 不变 |
| startLatch.countDown | ✓ 同步触发 | 不变 |
| endLatch.await(5, TimeUnit.SECONDS) | ✓ 业务任务完成证明 | 不变 |
| `pool.shutdown()` | ✓ 阻止新任务 | **不变(本轮 KEEP)** |
| `assertThat(done).isTrue()` | ✓ 成功性证明 | 不变 |
| `assertThat(err1.get()).isNull()` | ✓ T1 成功证明 | 不变 |
| `assertThat(err2.get()).isNull()` | ✓ T2 成功证明 | 不变 |
| 阶段 C verifyFinalState | ✓ Verifier 验证 | 不变 |
| 测试方法返回 | ✓ JUnit 生命周期 | 不变 |

### 7.2 当前时序已经满足的语义

| 语义要求 | 当前时序是否满足 | 证据 |
|---|---|---|
| 业务任务完成证明 | **✓** | `endLatch.await()` + `done.isTrue()` |
| T1 业务成功证明 | **✓** | `assertThat(err1.get()).isNull()` |
| T2 业务成功证明 | **✓** | `assertThat(err2.get()).isNull()` |
| 不再接受新任务 | **✓** | `pool.shutdown()` |
| 测试方法返回 | **✓** | JUnit 框架 |
| 测试间隔离(local pool)| **✓** | 241V2A-14 §5.1 修订后 |
| GC 回收 pool | **✓** | local 变量 |

### 7.3 当前时序**未**满足的语义(若 ADD awaitTermination)

| 语义要求 | 当前时序是否满足 | 若 ADD 后 |
|---|---|---|
| ExecutorService worker 完全终止 | ✗(不严格保证)| ✓ |
| worker 线程显式 join | ✗ | ✓ |
| 资源回收最显式化 | ✗(部分)| ✓ |

**关键问题**:这些"未满足的语义"是否构成"必须 ADD"的理由?

**【241V2A-40 显式判定】**:**否**。
- worker 完全终止不是测试正确性的必要条件
- 测试间污染风险已被 local pool 消除
- 没有冻结规范要求"必须 awaitTermination"
- 241V2A-16 §4.3 显式接受"保留现状"

---

## # 8. 决策矩阵(证据型)

### 8.1 完整决策矩阵

| 评价维度 | ADD awaitTermination | KEEP shutdown-only | 证据 | 证据强度 |
|---|---|---|---|---|
| **DEFAULT-03 业务正确性** | 不影响(已正确)| 不影响(已正确)| 241V2A-15 §3.2 三道断言 | A(直接规格证据)|
| **并发任务完成证明** | 已有(endLatch.await)| 已有(endLatch.await)| 241V2A-15 §3.2 + 241V2A-14 §5.1 | A |
| **ExecutorService 完全终止** | 显式保证 | 不严格保证(但不影响测试)| 【通用技术事实】Java JDK ExecutorService | B(通用技术事实)|
| **测试生命周期完整性** | 更显式 | 已足够(241V2A-14 §5.1 修订后)| 241V2A-14 §5.1 修订 | A |
| **测试间污染风险** | 显式降低 | 已消除(local pool)| 241V2A-14 §5.1(从 static 改 local)| A |
| **资源回收显式性** | 更显式 | 241V2A-16 §4.3 接受 | 241V2A-16 §4.3 | A |
| **与其他 DEFAULT 模板一致性** | ✗ **破坏 DEFAULT-01/03 11 项一致** | ✓ 11 项完全一致 | 241V2A-15 §4.1 | **A(关键证据)** |
| **与历史冻结模板一致性** | ✗ 与 241V2A-4 / 14 / 15 DEFAULT-01 / 03 模板不一致 | ✓ 完全一致 | 241V2A-4 §5.1 + 241V2A-14 §5.1 + 241V2A-15 §3.1 | **A(关键证据)** |
| **实现复杂度** | +1 行 awaitTermination 调用 | 当前写法 | — | — |
| **是否改变已有冻结语义** | **是(破坏 11 项结构一致)** | **否** | 241V2A-15 §4.1 | **A(关键证据)** |
| **是否引入新业务规则** | 否(只是风格)| 否(只是现状保持)| — | — |
| **是否需要新 P0/P1** | 否(P2 风格问题) | 否 | 241V2A-16 §4.3 | A |

### 8.2 证据强度汇总

| 证据 | 来源 | 强度 | 方向 |
|---|---|---|---|
| 241V2A-15 §4.1 显式确认 DEFAULT-01 / 03 11 项结构完全一致(含 `pool.shutdown()`) | 241V2A-15 §4.1 | A 直接规格证据 | **KEEP** |
| 241V2A-4 §5.1 原始 DEFAULT-01 = static pool + shutdown-only(无 awaitTermination) | 241V2A-4 §5.1 L254 | A 直接规格证据 | KEEP |
| 241V2A-14 §5.1 修订后 DEFAULT-01 = local pool + shutdown-only | 241V2A-14 §5.1 | A 直接规格证据 | KEEP |
| 241V2A-15 §3.1 DEFAULT-03 = local pool + shutdown-only | 241V2A-15 §3.1 | A 直接规格证据 | KEEP |
| 241V2A-16 §4.3 显式接受"保留现状"路径 | 241V2A-16 §4.3 | A 直接规格证据 | **KEEP** |
| 没有 DEFAULT 模板使用 awaitTermination(任何文档)| 缺位证据 | E | KEEP |
| 没有 @AfterEach / @AfterAll / teardown | 缺位证据 | E | KEEP |
| ADD awaitTermination 是 Java 并发最佳实践 | 【通用技术事实】 | B(仅通用技术,无冻结)| ADD(技术价值)|
| endLatch.await() 已证明业务任务完成 | 241V2A-15 §3.2 + 241V2A-16 §4.3 | A | KEEP |

**证据强度统计**:
- **KEEP**:**A × 6 + E × 2 = 强支持**
- **ADD**:**B × 1 = 弱支持(只有通用技术价值,无冻结规范支持)**

### 8.3 关键证据分析

**关键证据 1:241V2A-15 §4.1 11 项结构一致表显式确认 `pool.shutdown()`**

如果 ADD awaitTermination,**必须同时修改 DEFAULT-01 和 DEFAULT-03**,这会**破坏** 241V2A-15 §4.1 已冻结的"11 项结构完全一致"。

**这意味着 ADD 会破坏已有冻结的不变量**。

**关键证据 2:241V2A-4 → 241V2A-14 池演变不涉及 awaitTermination**

241V2A-14 §5.1 已经把 pool 从 static 改为 local(优化生命周期),但**没有** ADD awaitTermination。这说明 Effective Spec 在池生命周期优化上已经选择了"local pool"路径,而**不**是"awaitTermination"路径。

---

## # 9. 反方观点(必须显式考虑并反驳)

### 9.1 反方观点 1:"awaitTermination 是 Java ExecutorService 最佳实践"

**反驳**:
1. 这是【通用技术事实】,**不是** OptFlow 冻结规范
2. 241V2A-16 §4.3 显式判定 P2-2 为"功能正确但风格不完美",未升级为必须修复
3. 241V2A-16 §4.3 显式给出"保留现状"是合法路径
4. **没有冻结文档要求 awaitTermination**

**证据强度**:**B(通用技术事实)** vs **A(冻结规范 241V2A-16 §4.3)** → **A 胜**

### 9.2 反方观点 2:"如果不 awaitTermination,worker 线程可能不会立即终止"

**反驳**:
1. 这是事实,但**不影响测试正确性**
2. worker 线程最终会自然终止(任务完成后 run() 返回)
3. local pool 在测试方法返回后,worker 也会自然退出
4. 241V2A-16 §4.3 显式判定:"不影响测试正确性"

**证据强度**:**A(241V2A-16 §4.3 显式判定)** → 反驳成立

### 9.3 反方观点 3:"shutdown-only 在高负载下可能导致下一个测试延迟"

**反驳**:
1. 这是**未来可能性推断**,不是**当前已冻结需求**
2. 当前 Effective Spec(241V2A-15 §3.1)接受 shutdown-only
3. 没有证据表明 DEFAULT-03 在 S1-169-2 实施后会产生高负载问题
4. 即使产生,也属于 P1 问题,**不是** P2

**证据强度**:**E 推断证据** → 反驳成立

### 9.4 反方观点 4:"local pool 自然退出需要时间,可能在测试间产生资源竞争"

**反驳**:
1. 缺乏冻结证据
2. JUnit 5 默认测试方法串行执行(同一测试类内)
3. Spring Boot Test 框架会管理测试生命周期
4. 241V2A-15 §3.1 显式接受 local pool + shutdown-only,**不**接受"必须 awaitTermination"

**证据强度**:**E 推断证据** → 反驳成立

---

## # 10. 最终裁决

### 10.1 裁决结果

**【241V2A-40 正式裁决】**:**KEEP shutdown-only**

### 10.2 裁决理由

1. **241V2A-15 §4.1 已冻结 11 项结构一致表显式确认 `pool.shutdown()`**:DEFAULT-01 / 03 必须采用同一并发调用成功性验证结构。**ADD 会破坏 11 项结构一致**。

2. **241V2A-4 §5.1 + 241V2A-14 §5.1 + 241V2A-15 §3.1 三份已冻结 Effective Spec 全部使用 shutdown-only**:没有任何文档使用 awaitTermination。

3. **241V2A-14 §5.1 已经优化生命周期**(从 static pool 改为 local pool):Effective Spec 已经选择了"local pool 路径",**不**是"awaitTermination 路径"。

4. **241V2A-16 §4.3 显式接受"保留现状"路径**:"功能正确但风格不完美"+"可以加 awaitTermination / 也可以保留现状"。

5. **endLatch.await() 已证明业务任务完成**(241V2A-15 §3.2 三道断言 + 241V2A-14 §5.1)。

6. **没有任何冻结规范要求 awaitTermination**:241V2A-17 ~ 35 全部保持 OPEN 但**未要求 ADD**。

7. **DEFAULT-02 / 04 / 05 不使用线程池**:不涉及此问题,无需统一处理。

8. **没有 @AfterEach / @AfterAll / teardown**:Effective Spec 接受 local pool 自然生命周期。

---

## # 11. Effective Spec 冻结

### 11.1 唯一 Effective Spec(DEFAULT-01 / DEFAULT-03 阶段 B)

**【241V2A-40 正式冻结】** DEFAULT-01 / DEFAULT-03 阶段 B 线程池处理:

```java
// === 阶段 B:并发调用 ===
ExecutorService pool = Executors.newFixedThreadPool(2);   // local pool
AtomicReference<Throwable> err1 = new AtomicReference<>();
AtomicReference<Throwable> err2 = new AtomicReference<>();
CountDownLatch startLatch = new CountDownLatch(1);
CountDownLatch endLatch = new CountDownLatch(2);

pool.submit(() -> {
    try {
        startLatch.await();
        userCompanyService.setDefaultCompany(userId, X);
    } catch (Throwable t) {
        err1.set(t);
    } finally {
        endLatch.countDown();
    }
});
pool.submit(() -> {
    try {
        startLatch.await();
        userCompanyService.setDefaultCompany(userId, Y);
    } catch (Throwable t) {
        err2.set(t);
    } finally {
        endLatch.countDown();
    }
});

startLatch.countDown();
boolean done = endLatch.await(5, TimeUnit.SECONDS);
pool.shutdown();                                          // ← **KEEP shutdown-only**

assertThat(done).isTrue();
assertThat(err1.get()).isNull();
assertThat(err2.get()).isNull();
```

### 11.2 严禁的回归

**【241V2A-40 显式严禁】**:
- ✗ 不得在 DEFAULT-01 / DEFAULT-03 中**添加** `pool.awaitTermination(...)` 调用
- ✗ 不得添加 `pool.shutdownNow()` 调用
- ✗ 不得添加 `@AfterEach` / `@AfterAll` 处理 pool
- ✗ 不得改回 `static pool`(241V2A-14 §5.1 修订前写法)
- ✗ 不得"为了更完整"破坏 241V2A-15 §4.1 11 项结构一致

如果未来需要"awaitTermination 路径",必须**新开补丁**显式修改 241V2A-15 §4.1 11 项结构表 + 显式作废本轮 KEEP 裁决。

### 11.3 DEFAULT-02 / DEFAULT-04 / DEFAULT-05 不变

| Test | 线程池处理 |
|---|---|
| DEFAULT-02 | 不使用线程池(串行调用)|
| DEFAULT-04 | 不使用线程池(单线程异常调用)|
| DEFAULT-05 | 不使用线程池(单线程 + Spy throw)|

这些测试**不受本轮裁决影响**。

---

## # 12. 三层状态

### 12.1 P2-2 最终状态

```
P2-2 = CLOSED (Effective Spec - KEEP shutdown-only)
       ↑
       Effective Spec 已冻结 KEEP 路径

Production Implementation = NOT YET VERIFIED
       ↑
       backend/ 未创建,实际写法未观察到

Runtime Test Execution = NOT EXECUTED
       ↑
       DEFAULT-01 / DEFAULT-03 测试未实际运行
```

### 12.2 与 P2-0 / P2-1 关闭模式对照

| 维度 | P2-0(241V2A-36 + 37) | P2-1(241V2A-38 + 39) | P2-2(241V2A-40) |
|---|---|---|---|
| 关闭路径 | Effective Spec 已冻结 exactly-one | Effective Spec 已冻结 DELETE 占位 | Effective Spec 已冻结 KEEP shutdown-only |
| 三层状态 | CLOSED / NOT YET VERIFIED / NOT EXECUTED | CLOSED / NOT YET VERIFIED / NOT EXECUTED | CLOSED / NOT YET VERIFIED / NOT EXECUTED |

---

## # 13. 影响范围

| 范围 | 影响 |
|---|---|
| 生产代码 | **0 改动** |
| SQL | **0 改动** |
| DDL | **0 改动** |
| API | **0 改动** |
| 历史 MD(241V2A-1 ~ 241V2A-39) | **0 改动** |
| VisionCare PMS | **0 改动** |
| backend/ | **0 创建** |
| P2-0 / P2-1 / P2-6 / P2-7 / P2-8 | **0 改动** |

**本轮唯一动作**:新增 `241V2A-40_*.md`,通过显式冻结 KEEP 路径建立新 Effective Spec。

---

## # 14. 其他 P2 状态(显式 NOT TOUCHED)

```
P2-0 = CLOSED(Effective Spec) [241V2A-36 + 37]
P2-1 = CLOSED(Effective Spec, DELETE) [241V2A-38 + 39]
P2-2 = CLOSED(Effective Spec, KEEP shutdown-only) [241V2A-40 本轮]
P2-6 = NOT TOUCHED
P2-7 = NOT TOUCHED
P2-8 = NOT TOUCHED
```

---

## # 15. 反证检查

### 15.1 反问 1:KEEP 是否破坏 DEFAULT-03 业务正确性?

**回答**:**否**。
- 241V2A-15 §3.2 三道断言顺序不变
- `done.isTrue()` / `err1.get().isNull()` / `err2.get().isNull()` 都成立
- 业务正确性已经证明

### 15.2 反问 2:KEEP 是否影响 DEFAULT-01 / 03 11 项结构一致?

**回答**:**否**。
- 241V2A-15 §4.1 显式确认 11 项结构完全一致
- 本轮 KEEP 维持这一不变量

### 15.3 反问 3:KEEP 是否导致 worker 线程泄漏?

**回答**:**理论上存在,实际上可接受**。
- worker 线程在 run() 返回后会被 ThreadPoolExecutor 回收
- local pool 在测试方法返回后被 GC 回收
- 即使短期存在残留,不影响测试正确性

### 15.4 反问 4:KEEP 是否影响测试可重复执行?

**回答**:**否**。
- local pool 每次测试新创建,跨测试无状态
- JUnit 5 默认串行执行

### 15.5 反问 5:有没有任何冻结文档要求 awaitTermination?

**回答**:**否**。
- 241V2A-4 / 14 / 15 全部使用 shutdown-only
- 241V2A-16 §4.3 显式接受"保留现状"
- 后续 241V2A-17 ~ 35 全部保持 OPEN 但未要求 ADD

### 15.6 反证结论

**没有反证可以推翻 P2-2 = CLOSED(KEEP shutdown-only)**。

---

## # 16. 最终状态

### 16.1 P2-2 三层状态

```
P2-2 = CLOSED (Effective Spec - KEEP shutdown-only)

Production Implementation = NOT YET VERIFIED

Runtime Test Execution = NOT EXECUTED
```

### 16.2 Effective Spec 锁定结论

**【241V2A-40 锁定】** DEFAULT-01 / DEFAULT-03 阶段 B 线程池处理:

```java
ExecutorService pool = Executors.newFixedThreadPool(2);   // local pool
// ... submit / startLatch / endLatch.await / shutdown ...
pool.shutdown();                                          // ← KEEP shutdown-only
// 不增加 awaitTermination
```

---

## # 17. 下一步

**等待独立盲审**。

任何未来的:
- P2-6 / P2-7 / P2-8 整改
- 241V2A-41 及以后的 S1-169-2 补丁
- backend/ 实际创建与实施验证
- DEFAULT-01 / DEFAULT-03 实际运行与执行验证
- DEFAULT-01 / DEFAULT-03 awaitTermination 路径的重新裁决(需新补丁)

**均需独立盲审后由老板下达指令**。

**严禁**:
- 自行开始 P2-6
- 自行在 DEFAULT-01 / DEFAULT-03 中添加 awaitTermination
- 自行声称"实施已完成"
- 自行声称"测试已通过"
- 自行 commit / push

---

## # 18. 附录:术语对齐

| 术语 | 本轮定义 |
|---|---|
| 业务任务完成 | Runnable.run() / Callable.call() 方法体执行完毕,T1/T2 finally 块中 countDown |
| ExecutorService 完全终止 | ThreadPoolExecutor 中所有 worker 线程都已退出(线程状态为 TERMINATED)|
| shutdown() | 阻止新任务提交,worker 自然退出 |
| awaitTermination(timeout, unit) | 阻塞等待所有 worker 终止,超时返回 false |
| shutdown-only | 仅调用 shutdown(),不调用 awaitTermination() |
| local pool | 方法内局部变量 ExecutorService,测试方法返回后 GC 回收 |
| static pool | 类级别 static final ExecutorService,跨测试共享 |
| 三层状态模型 | Effective Spec + Production Implementation + Runtime Test Execution(241V2A-37 §6.2)|

---

**End of 241V2A-40**
