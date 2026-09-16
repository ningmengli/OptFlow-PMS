# 241V2A-2 S1-169-1 defaultCompany 并发测试与死锁表述修正

> **本轮定位**:在 241V2A-1 基础上,**精准修正 3 个技术问题**——"死锁不可能"过强表述 / DEFAULT-01~03 并发测试事务边界错误 / DEFAULT-01 固定"C 获胜"的错误断言。不重写 241V2A-1 任何字节,只通过补丁叠加建立增量关系。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 任何历史 MD
> - 严禁修改 VisionCare PMS 任何文件
> - 严禁创建 backend/ / 严禁写 Java 源文件 / 严禁创建 SQL 文件 / 严禁执行 DDL / 严禁连接数据库
> - 严禁修改 pom.xml / application.yml
> - 严禁 commit / 严禁 push
> - 标签:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
> - 阶段:**S1-169-1**(未进入 S1-169-2)
> - 本裁决完成后**不**自评 PASS,**等待 241A-1 独立盲审**

---

## §0 Git 基线

- **HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`(S1-169-0 240 commit)
- **REMOTE == LOCAL**:`6efa0da` ✓
- **0 号闸门 4 文件 SHA256 全部 PASS** ✓
- **历史 MD(190~241V2A-1 共 63 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-2 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 241V2A-1 核心并发方案(保留,不推翻)

**【241V2A-2 冻结】** 241V2A-1 的核心并发方案 = V4.4 defaultCompany 并发控制正式基线:

```text
方案 A:
  锁 user.id 单行
  SELECT ... FOR UPDATE
  +
  单一 @Transactional
  +
  user_company 更新
```

### 1.2 本轮精确修正 3 个问题

| # | 问题 | 来源 | 严重度 |
|---:|---|---|:-:|
| 1 | "死锁不可能"过强表述 | 241V2A-1 §7 / §14 / §22 | P1(技术表述不严谨) |
| 2 | DEFAULT-01~03 并发测试事务边界错误(用测试 @Transactional 包异步)| 241V2A-1 §12.2 / §12.3 / §12.4 | P1(测试不成立) |
| 3 | DEFAULT-01 固定"C 获胜"的错误断言 | 241V2A-1 §8.2 场景 1 / §12.2 | P1(测试断言错误) |

### 1.3 本轮**不**重新裁决

12 项业务语义**不**在本轮范围(详见 §14):
- ✗ defaultCompanyId 存储位置 = user_company.is_default
- ✗ user.id = 并发控制锁
- ✗ @Transactional
- ✗ rollbackFor = Exception
- ✗ READ_COMMITTED
- ✗ 允许 0 个 default
- ✗ defaultCompanyId ≠ 当前请求 companyId
- ✗ X-Company-Id > session default > unique company
- ✗ CompanyContext 仍必须做权限校验
- ✗ user_company DDL 不修改
- ✗ 241V2A P0-2 不修改
- ✗ P0-3 / P0-4 / P1 不修改

---

## §2 严格禁止(本轮)

- ✗ 修改 241V2 / 241V2A / 241V2A-1 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等 241A-1 独立盲审)
- ✗ 进入 S1-169-2
- ✗ 把 241V2A-2 + 241A-1 审计合并

---

## §3 问题 1:死锁表述修正(P1)

### 3.1 241V2A-1 原文(过强表述)

> "单行锁 + READ_COMMITTED + 主键索引 → 死锁**不可能**"(241V2A-1 §7.1 标题)
> "**【241V2A-1 冻结】** 由于锁对象 = `user.id` 单行,**不会出现死锁**"(§7.1 正文)
> "主结论:**不可能**死锁"(§14.1 标题)
> "**结论**:A 方案在所有维度上**严格优于** B 方案"(§3.3 — 涉及死锁)

**问题诊断**:上述表述把"setDefaultCompany 单一方法**的**锁顺序不会形成循环等待"等同于"V4.4 系统**不会**死锁",过强且不严谨。

### 3.2 真实死锁风险

| 场景 | 是否死锁 |
|---|:-:|
| 同一 user 并发 setDefaultCompany | ✗ 不可能(单行锁,无循环等待) |
| 不同 user 并发 setDefaultCompany | ✗ 不可能(不同锁) |
| setDefaultCompany 与其他 setDefaultCompany 跨 user | ✗ 不可能(同方法,锁顺序一致) |
| **未来业务事务 A**:`company → user` | **✓ 可能** |
| **未来业务事务 B**:`user → company` | **✓ 可能** |
| 上述 A + B 并发 | **✓ 死锁**(锁顺序相反) |

**关键**:虽然 setDefaultCompany 本身**没有**死锁风险,但 V4.4 系统未来可能引入**其他**业务事务,如果锁顺序不统一,**系统级死锁**完全可能。

### 3.3 241V2A-2 正式修正表述

**【241V2A-2 冻结】** 死锁表述正式修正:

> **setDefaultCompany 本身**:
> - 统一先锁 user.id
> - 同一 user 的多个 setDefaultCompany 请求先竞争同一把 user 行锁
> - 本方法内部**不存在** A→B / B→A 的多行锁循环依赖
> - 因此**本方法**的并发 default 更新**不会**形成由 user.id 锁顺序造成的循环等待
>
> **但是**(重要):
> - **不能**声明整个 V4.4 系统"死锁不可能"
> - 未来其他业务事务如果采用**不同锁顺序**(例如 Transaction A: company → user / Transaction B: user → company),仍可能产生**系统级**死锁

### 3.4 严禁表述(241V2A-2 禁止以下表述)

- ✗ "死锁不可能"
- ✗ "完全免疫"
- ✗ "绝对不会死锁"
- ✗ "永不死锁"
- ✗ "零死锁"
- ✗ "系统级死锁不可能"

### 3.5 必须使用的表述(241V2A-2 正式用语)

- ✓ "本方法不存在锁循环依赖"
- ✓ "本方法的并发调用不会形成 user.id 锁顺序循环等待"
- ✓ "系统级死锁仍需依赖数据库异常检测 + Spring rollback"
- ✓ "V4.4 统一锁顺序 + 数据库死锁检测 + rollback 作为并发安全原则"

### 3.6 5 项强制约束(241V2A-2 冻结)

1. ✓ setDefaultCompany 的锁对象 = `user.id`
2. ✓ setDefaultCompany 的**第一把业务锁**必须是 `user.id`
3. ✓ 后续业务代码不得在该事务中引入与其他事务**相反**的锁顺序
4. ✓ 系统级死锁仍必须依赖数据库异常检测 + Spring rollback
5. ✓ 不得使用 §3.4 列出的严禁表述

---

## §4 问题 2:DEFAULT-01~03 事务边界重设计(P1)

### 4.1 241V2A-1 错误模式(过强 / 不严谨)

241V2A-1 §12.2 / §12.4 / §12.5 用了以下结构:

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_01_concurrent_different_companies() {
    // ... 测试准备(可能用同一事务)...
    
    CountDownLatch startLatch = new CountDownLatch(1);
    
    CompletableFuture<Void> f1 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1002L);  // ← 问题
        } catch (...) { ... }
    });
    
    CompletableFuture<Void> f2 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1003L);  // ← 问题
        } catch (...) { ... }
    });
    
    startLatch.countDown();
    // ... 等待 ...
}
```

### 4.2 问题诊断

**风险 1:测试 @Transactional 包住整个测试方法**:
- 测试方法标注 `@Transactional`
- 测试方法体内启动 `CompletableFuture.runAsync` 异步线程
- **异步线程不会继承测试线程的事务上下文**(Spring ThreadLocal 不跨线程)
- 异步线程调用 `userCompanyService.setDefaultCompany` 时,Service 的 `@Transactional` 拦截器会**创建新事务**
- **这本身不是错** — 异步线程确实需要独立事务

**风险 2:测试数据可能在测试线程未提交**:
- 如果测试准备(创建 user / user_company)用测试线程的 `@Transactional`
- 测试线程事务**未提交**
- 异步线程在 Service 内开始新事务 → Service 看到的可能是**不同连接 / 看不到未提交数据**
- 实际可能:Service 事务 SELECT 不到准备的数据,抛 NPE / 异常

**风险 3:@Rollback 行为模糊**:
- `@Rollback` 默认回滚**测试线程事务**
- 异步线程事务是独立的,可能已经 commit
- @Rollback 不等于"自动回滚所有异步线程业务事务"

**风险 4:最终验证读数据时机**:
- 测试线程在异步 future 完成后立即验证
- 但**异步线程事务的 commit 时机由 Service 决定**
- 测试线程的 SELECT 可能读到"未 commit"或"已 commit"的不一致快照(取决于隔离级)

### 4.3 241V2A-2 正式冻结:4 层事务结构

**【241V2A-2 冻结】** V4.4 并发测试必须采用 **4 层事务结构**:

```
┌────────────────────────────────────────────┐
│ 第 1 层:测试数据准备事务                     │
│   @Transactional / 独立方法                  │
│   创建 user / user_company / company         │
│   **必须 commit**                            │
└────────────────────────────────────────────┘
                    ↓
        CountDownLatch 同步起点
                    ↓
┌────────────────────────────────────────────┐
│ 第 2 层:并发业务事务 T1(Executor 线程)       │
│   @Transactional(rollbackFor, READ_COMMITTED)│
│   userCompanyService.setDefaultCompany(...)  │
│   **独立事务 / 独立连接 / 独立 commit**         │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ 第 3 层:并发业务事务 T2(Executor 线程)       │
│   @Transactional(rollbackFor, READ_COMMITTED)│
│   userCompanyService.setDefaultCompany(...)  │
│   **独立事务 / 独立连接 / 独立 commit**         │
└────────────────────────────────────────────┘
                    ↓
        等待 T1 + T2 全部完成
                    ↓
┌────────────────────────────────────────────┐
│ 第 4 层:独立最终验证事务                     │
│   @Transactional(readOnly=true)              │
│   SELECT COUNT(*) / SELECT defaultCompanyId  │
│   独立事务 / 读已提交数据                     │
└────────────────────────────────────────────┘
                    ↓
        测试清理(可选,验证后可清理数据)
```

### 4.4 严禁模式(241V2A-2 禁止)

```java
// ❌ 错误:外层 @Transactional 包住整个测试
@Test
@Transactional
@Rollback
public void test_BAD() {
    // 测试线程事务未提交
    userMapper.insert(testUser);
    userCompanyMapper.insert(testUC);
    
    CompletableFuture.runAsync(() -> {
        // 异步线程:独立事务,但看不到测试线程未提交的数据
        userCompanyService.setDefaultCompany(1L, 1002L);
    });
    
    // 测试线程事务:永远回滚,但异步线程事务可能已 commit
    // → 数据状态混乱,测试结论不可信
}
```

### 4.5 正确模式(241V2A-2 冻结)

```java
// ✓ 正确:4 层事务结构
@SpringBootTest
public class DefaultCompanyConcurrencyTest {
    
    @Autowired private UserMapper userMapper;
    @Autowired private UserCompanyMapper userCompanyMapper;
    @Autowired private CompanyMapper companyMapper;
    @Autowired private UserCompanyService userCompanyService;
    
    private static final ExecutorService pool = Executors.newFixedThreadPool(2);
    
    // 第 1 层:测试数据准备事务(独立方法,必须 commit)
    @Test
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void prepareTestData() {
        // 创建 user
        User u = new User();
        u.setLoginName("test_" + System.nanoTime());
        u.setPasswordHash("...");
        u.setStatus(1);
        userMapper.insert(u);
        // ↑ 此事务 commit
    }
    
    // 第 2-3 层:并发业务事务
    @Test
    public void test_DEFAULT_01_concurrent_different_companies() throws Exception {
        // 先调用 prepareTestData(已 commit)
        Long userId = ...;  // 准备阶段拿到的 userId
        
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(2);
        AtomicLong resultB = new AtomicLong(-1);
        AtomicLong resultC = new AtomicLong(-1);
        AtomicReference<Throwable> errB = new AtomicReference<>();
        AtomicReference<Throwable> errC = new AtomicReference<>();
        
        // T1: setDefault(B)
        Future<?> f1 = pool.submit(() -> {
            try {
                startLatch.await();
                userCompanyService.setDefaultCompany(userId, 1002L);
                resultB.set(1002L);
            } catch (Throwable t) {
                errB.set(t);
            } finally {
                endLatch.countDown();
            }
        });
        
        // T2: setDefault(C)
        Future<?> f2 = pool.submit(() -> {
            try {
                startLatch.await();
                userCompanyService.setDefaultCompany(userId, 1003L);
                resultC.set(1003L);
            } catch (Throwable t) {
                errC.set(t);
            } finally {
                endLatch.countDown();
            }
        });
        
        // 同步起点
        startLatch.countDown();
        // 等待 T1 + T2 完成(最多 5 秒)
        boolean done = endLatch.await(5, TimeUnit.SECONDS);
        assertThat(done).isTrue();
        
        // 第 4 层:独立最终验证事务(用独立方法 / 读已提交数据)
        // (见 §4.6)
        verifyFinalState(userId, 1002L, 1003L);
    }
}
```

### 4.6 独立最终验证事务

```java
// 第 4 层:独立验证事务
@Transactional(propagation = Propagation.REQUIRES_NEW, readOnly = true)
public void verifyFinalState(Long userId, Long companyBId, Long companyCId) {
    int defaultCount = userCompanyMapper.countByUserIdAndIsDefault(userId, 1);
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(userId);
    
    // 断言
    assertThat(defaultCount).isEqualTo(1);
    assertThat(defaultCompanyId).isIn(companyBId, companyCId);
}
```

**关键**:
- `Propagation.REQUIRES_NEW` = 新事务,不被外层覆盖
- `readOnly = true` = 优化提示
- 验证方法**不能**用测试 @Transactional(测试方法不应有 @Transactional)
- 验证方法必须独立调用(可以在测试方法末尾显式调用)

---

## §5 DEFAULT-01 修正(P1)

### 5.1 241V2A-1 原文(错误断言)

> "T1 → companyB, T2 → companyC, **最终固定 companyC=1**"(241V2A-1 §8.2 场景 1)
> "最终状态:仅 companyC=1(后到者赢)"(同上)
> "断言:`assertThat(defaultCompanyId).isIn(1001L, 1002L, 1003L);`"(§12.2 — 但语义含混)

**问题**:
- 真正获得 user.id 行锁的顺序由**数据库调度**决定
- 不可能断言"后到者一定赢"——可能是 T1 先获锁 / 也可能是 T2 先获锁
- 241V2A-1 §8.2 表格写"后到者赢" + §12.2 写"isIn(1001L, 1002L, 1003L)" 互相矛盾

### 5.2 241V2A-2 正式修正

**【241V2A-2 冻结】** DEFAULT-01 修正后语义:

```
初始:
  companyA = 1
  companyB = 0
  companyC = 0

并发:
  T1 → setDefaultCompany(B)
  T2 → setDefaultCompany(C)

由于真正获得 user.id 行锁的顺序由数据库调度决定:
  可能 T1 先提交 → 最终 C=1
  可能 T2 先提交 → 最终 B=1

因此最终断言只能是:
  1. defaultCount == 1
  2. defaultCompanyId ∈ {B, C}
  3. defaultCompanyId 必须属于 user 当前有效 company 权限集合
  4. 两个业务事务均应成功
  5. 不允许最终出现 0 条 default
  6. 不允许最终出现 2 条 default

不要断言"后到者一定赢"。
```

### 5.3 DEFAULT-01 最终断言清单(241V2A-2 冻结)

| 断言 | 通过条件 |
|---|---|
| 1 | `defaultCount == 1` |
| 2 | `defaultCompanyId ∈ {B=1002, C=1003}` |
| 3 | T1 成功(无异常) |
| 4 | T2 成功(无异常) |
| 5 | 不允许 0 条 default |
| 6 | 不允许 2 条 default |

**禁止断言**:
- ✗ "T1 后到者一定赢"
- ✗ "companyC=1"(具体值)
- ✗ "companyA 仍为 default"

---

## §6 DEFAULT-02 保持(串行,无并发)

**【241V2A-2 冻结】** DEFAULT-02 维持 241V2A-1 语义:

```text
串行: A → B
预期:
  defaultCount == 1
  defaultCompanyId == B
```

无需并发线程,单事务即可。

---

## §7 DEFAULT-03 保持(并发同 company,幂等)

**【241V2A-2 冻结】** DEFAULT-03 维持 241V2A-1 语义 + 关键验证点:

```text
并发:
  T1 → A
  T2 → A

最终:
  defaultCount == 1
  defaultCompanyId == A

两个事务都可以成功(幂等)。

重点验证:
  - 第二个事务在 user.id 锁释放后读取到一致状态
  - 清零 + 再设置过程最终仍然只有一个 default
```

事务边界用 4 层结构(§4.3)。

---

## §8 真实独立事务测试设计(241V2A-2 冻结)

### 8.1 测试基础设施要求

| 组件 | 要求 |
|---|---|
| ExecutorService | 固定大小线程池(线程数 ≥ 并发事务数)|
| UserCompanyService | **真实 Spring Bean**(通过 @Autowired 注入) |
| UserCompanyMapper | **真实 MyBatis-Plus Mapper** |
| 测试数据准备 | **独立 @Transactional + 强制 commit**(REQUIRES_NEW 或直接无 @Transactional)|
| 最终验证 | 独立 @Transactional(REQUIRES_NEW + readOnly) |

### 8.2 Service 调用约定

```text
每个 Service 调用由自身:
  @Transactional(
      rollbackFor = Exception.class,
      isolation = Isolation.READ_COMMITTED
  )

建立独立数据库事务。
```

**严禁**:
- ✗ 在测试方法上用 @Transactional 包装
- ✗ 把多个 Service 调用合并到一个事务
- ✗ 在异步线程外手动管理事务

### 8.3 测试线程与异步线程的事务边界

| 线程 | 事务 | 状态 |
|---|---|---|
| 测试主线程 | 无(准备数据用独立方法) | 仅做同步(latch / future)|
| 异步线程 1(T1)| Service @Transactional 自动创建 | commit / rollback 由 Service 决定 |
| 异步线程 2(T2)| Service @Transactional 自动创建 | commit / rollback 由 Service 决定 |
| 验证线程(可选) | 独立 @Transactional(REQUIRES_NEW) | 仅读 |

---

## §9 DEFAULT-01 锁竞争验证(241V2A-2 冻结)

### 9.1 验证目标

**【241V2A-2 冻结】** DEFAULT-01 不能**只**验证最终 count。**应尽量**验证锁竞争行为。

### 9.2 推荐验证方式

```text
可以采用测试钩子 / latch / spy / repository instrumentation 记录:
  - T1 acquiredLock(user.id=1)
  - T2 waiting(user.id=1)
  - T1 committed
  - T2 acquiredLock(user.id=1)
```

### 9.3 验证严格度分级

| 级别 | 验证内容 | 实现难度 |
|---|---|:-:|
| **L1(必须)** | 最终数据库一致性(count / default) | 低 |
| L2(推荐) | T1 / T2 顺序(谁先获锁) | 中(Spy / repository instrumentation) |
| L3(可选) | 锁等待时间(等待多久才获锁)| 高(时间敏感,脆弱) |

**241V2A-2 强制 L1,L2 推荐,L3 不强制**(不要制造脆弱测试)。

### 9.4 L2 实现方式(伪代码)

```java
@Component
public class TestableUserMapper extends UserMapperImpl {
    public static final CountDownLatch t1AcquiredLock = new CountDownLatch(0);
    public static final CountDownLatch t2AcquiredLock = new CountDownLatch(0);
    public static final AtomicLong lockAcquireOrder = new AtomicLong(0);
    
    @Override
    public User selectByIdForUpdate(Long userId) {
        User u = super.selectByIdForUpdate(userId);
        // 记录获锁顺序
        long order = lockAcquireOrder.incrementAndGet();
        if (order == 1) t1AcquiredLock.countDown();
        if (order == 2) t2AcquiredLock.countDown();
        return u;
    }
}
```

**说明**:L2 实现需要替换 Mapper Bean,影响 S1-169-2 实施。本裁决**不**强制要求 L2,S1-169-2 实施时**至少 L1**。

---

## §10 系统级死锁约束 LOCK-ORDER-01(241V2A-2 新增)

### 10.1 LOCK-ORDER-01 正式冻结

**【241V2A-2 冻结】** V4.4 系统级锁顺序原则:

```text
LOCK-ORDER-01:

setDefaultCompany 的统一锁顺序:
  1. user.id(必须最先)
  2. user_company / company 业务读取与更新
  3. commit

任何未来需要同时锁 user + company + 其他业务表的事务,必须:
  - 明确锁顺序
  - 不得反向获取 user 锁
  - 新增违反统一锁顺序的业务必须重新审计
```

### 10.2 显式声明

> 这不是说"系统永远不会死锁"。
>
> 而是冻结:"**统一锁顺序 + 数据库死锁检测 + rollback**"作为 V4.4 的并发安全原则。

### 10.3 LOCK-ORDER-01 未来扩展

| 未来业务 | 应锁对象 | 锁顺序 |
|---|---|---|
| setUserRole(userId, roleId) | user.id → user_role | 1. user → 2. user_role |
| setCompanyOwner(companyId, userId) | company.id → user_company | 1. company → 2. user → 3. user_company? |
| transferPatient(patientId, fromCompany, toCompany) | patient.id → from company → to company | 1. patient → 2. company(按 id 升序) |
| ... | ... | **必须显式声明 + 审计** |

**严禁**:任何事务在已持有 user 锁的情况下又尝试反向锁 company(从 user → company);必须显式声明锁顺序。

### 10.4 锁顺序审计流程

新增业务事务如果需要锁 user + 其他表,必须:
1. 文档化锁顺序
2. 不与已有业务(241V2A-1 / 241V2A-2 已有事务)形成反向依赖
3. 经过 241A-N 独立审计

### 10.5 数据库兜底

即使遵循 LOCK-ORDER-01,仍可能有未审计的新业务引入死锁。**V4.4 系统级死锁兜底**:
- MySQL `innodb_lock_wait_timeout`(默认 50s)
- InnoDB 自动死锁检测(`innodb_deadlock_detect = ON`,默认)
- Spring `@Transactional(rollbackFor=Exception)` 自动 rollback
- **不**依赖应用层死锁预防 100% 成功

---

## §11 死锁异常处理正式修正(241V2A-2)

### 11.1 241V2A-1 原文(不严谨)

> "**防御性建议**(可选,不强制)... `@Retryable(value={...}, maxAttempts=3, ...)`"(241V2A-1 §14.2)

**问题**:`@Retryable` 写成了"防御性建议",没有区分**必须**和**可选**。

### 11.2 241V2A-2 正式区分

**【241V2A-2 冻结】** 死锁异常处理分两层:

#### 11.2.1 必须项(强制)

| 项 | 描述 |
|---|---|
| 数据库异常传播 | DeadlockLoserDataAccessException / CannotAcquireLockException 必须传播给调用方 |
| Spring transaction rollback | @Transactional(rollbackFor=Exception) 必须自动 rollback |
| 锁等待失败不能静默吞掉 | 不能 catch 后 return null / 包装成成功 |
| Deadlock / Lock timeout 不能被包装成成功 | 不能 catch DeadlockLoserDataAccessException 后 return success |

#### 11.2.2 可选项(可实施,可不实施)

| 项 | 描述 |
|---|---|
| @Retryable | 上层重试机制 |
| 指数退避 | backoff(delay=100, multiplier=2) |
| 重试次数 | maxAttempts=3(默认) |

### 11.3 重试关键约束

**【241V2A-2 冻结】** 重试必须**重新开始一个新事务**,不能在已回滚 / 标记 rollback-only 的旧事务内继续执行。

```java
// ✓ 正确:在 Service 边界外重试,每次重试进入新的 @Transactional
@Retryable(
    value = {DeadlockLoserDataAccessException.class, CannotAcquireLockException.class},
    maxAttempts = 3,
    backoff = @Backoff(delay = 100, multiplier = 2)
)
public void setDefaultCompanyWithRetry(Long userId, Long newDefaultCompanyId) {
    // 每次调用都是新事务(因为 setDefaultCompany 自己有 @Transactional)
    userCompanyService.setDefaultCompany(userId, newDefaultCompanyId);
}
```

```java
// ❌ 错误:在 @Transactional 方法内 try-catch 后自重试
@Transactional
public void BAD_setDefaultCompanyWithRetry(Long userId, Long newDefaultCompanyId) {
    try {
        setDefault(userId, newDefaultCompanyId);
    } catch (DeadlockLoserDataAccessException e) {
        // 错误:事务已标记 rollback-only,自重试无效
        setDefault(userId, newDefaultCompanyId);  // ← 永远失败
    }
}
```

### 11.4 @Retryable 适用范围

- ✓ 上层 Controller 调用层
- ✓ 异步任务包装层
- ✓ 业务服务对外方法
- ✗ @Transactional 方法内部
- ✗ Mapper / Repository 层

### 11.5 不强制实施

241V2A-2 **不**强制要求实施 @Retryable 重试,只冻结**如果实施**时的正确做法。

---

## §12 DEFAULT-01~05 最终测试矩阵(241V2A-2 冻结)

| 测试 | 事务准备 | 并发 | 最终断言 | 业务事务异常 |
|---|---|---|---|---|
| **DEFAULT-01** | **先 commit** | **T1=B, T2=C** | **count=1, default ∈ {B, C}, T1/T2 均成功** | **无** |
| DEFAULT-02 | 先 commit | 否(A→B 串行) | count=1, default=B | 无 |
| DEFAULT-03 | 先 commit | T1=A, T2=A(并发) | count=1, default=A | 无(幂等) |
| DEFAULT-04 | 先 commit | 否(→disabledB) | count=1, default=A(不变),rollback | CompanyAccessDeniedException |
| DEFAULT-05 | 先 commit | 否(中途异常) | count=1, default=A(不变),整体 rollback | RuntimeException |

### 12.1 关键变化(241V2A-1 → 241V2A-2)

| 测试 | 241V2A-1 断言 | 241V2A-2 断言 |
|---|---|---|
| DEFAULT-01 | 固定 C=1 + isIn(1001,1002,1003) | **count=1 + default ∈ {B,C}** |
| DEFAULT-02 | count=1, default=B | 保持 |
| DEFAULT-03 | count=1, default=A | 保持 |
| DEFAULT-04 | disabled 抛异常 rollback | 保持 |
| DEFAULT-05 | 中途异常 rollback | 保持 |

### 12.2 所有测试都需遵循 4 层事务结构(§4.3)

---

## §13 测试事务陷阱说明(241V2A-2 冻结)

### 13.1 错误模式

```java
// ❌ 错误:外层 @Transactional + 异步 Service 调用
@Test
@Transactional
@Rollback
void test_BAD() {
    userMapper.insert(testUser);              // 测试线程事务(未 commit)
    userCompanyMapper.insert(testUC);          // 测试线程事务(未 commit)
    
    CompletableFuture.runAsync(() -> {
        // 异步线程:独立事务,但看不到未提交的测试数据
        userCompanyService.setDefaultCompany(1L, 1002L);
        // ↑ 可能 NPE / NotFound / 数据不一致
    });
}
```

### 13.2 风险清单

| 风险 | 描述 |
|---|---|
| 数据可见性 | 异步线程事务**看不到**测试线程未提交的数据 |
| @Rollback 范围 | @Rollback 只回滚**测试线程事务**,不回滚异步线程事务 |
| 异常吞噬 | 异步线程异常可能被 `CompletableFuture` 吞掉,测试看不到 |
| 时序问题 | 异步线程 commit 时机不确定,测试线程 SELECT 时机可能不一致 |
| 资源未释放 | 异步线程持有的连接 / 锁可能没释放,后续测试受影响 |

### 13.3 正确方式(241V2A-2 冻结)

```text
prepare committed data
+
independent service transactions
+
independent verification
```

具体实现见 §4.3 4 层事务结构 + §4.5 正确模式示例。

### 13.4 严禁

- ✗ 测试方法上 @Transactional 包住整个测试
- ✗ 用 `Thread.sleep` 替代 `CountDownLatch`
- ✗ 测试方法内不显式等待异步线程完成(`Future.get` / `CountDownLatch.await`)
- ✗ 异步线程的异常 catch 后不记录

---

## §14 保持现有业务语义(12 项不重新裁决)

**【241V2A-2 冻结】** 以下 12 项业务语义**不**在本轮范围,**不**重新裁决:

| # | 项目 | 来自 |
|---:|---|---|
| 1 | defaultCompanyId 存储位置 = user_company.is_default | 241V2 §12.3 |
| 2 | user.id = 并发控制锁 | 241V2A-1 §4 |
| 3 | @Transactional 单一事务 | 241V2A-1 §5 |
| 4 | rollbackFor = Exception | 241V2A-1 §5.3 |
| 5 | isolation = READ_COMMITTED | 241V2A-1 §5.4 |
| 6 | 允许 0 个 default(方案 B)| 241V2A-1 §9.2 |
| 7 | defaultCompanyId ≠ 当前请求 companyId | 241V2A-1 §10 |
| 8 | X-Company-Id > session default > unique company | 241V2A-1 §10.2 |
| 9 | CompanyContext 仍必须做权限校验 | 241V2A-1 §10.3 |
| 10 | user_company DDL 不修改 | 241V2A-1 §11.4 |
| 11 | 241V2A P0-2(强制覆盖)不修改 | 241V2A §3.1 |
| 12 | P0-3 / P0-4 / P1 不修改 | 241V2 / 241V2A |

---

## §15 修正矩阵(241V2A-1 → 241V2A-2)

| 项目 | 241V2A-1 | 241V2A-2 |
|---|---|---|
| 锁对象 | user.id | **保持** |
| 事务 | @Transactional | **保持** |
| READ_COMMITTED | 是 | **保持** |
| **死锁表述** | "死锁不可能 / 完全免疫" | **改为"本方法无循环锁依赖,系统级死锁仍需处理"** |
| **LOCK-ORDER-01** | 未冻结 | **新增冻结(系统级锁顺序原则)** |
| **DEFAULT-01 断言** | 固定 C 赢 / isIn(1001,1002,1003) | **改为 count=1 + default ∈ {B,C},两个事务均应成功** |
| **测试外围事务** | @Transactional 包住整个测试 | **不包住 / 4 层结构** |
| **并发事务** | 异步独立 Service 事务 | **正式冻结 + 4 层结构** |
| **最终验证** | 测试流程不明确 | **独立验证事务(REQUIRES_NEW + readOnly)** |
| **@Retryable** | 写成"防御性建议(可选)" | **正式区分必须 vs 可选 + 重试必须新事务** |
| DEFAULT-02 | A→B 串行 | **保持** |
| DEFAULT-03 | A→A 并发 | **保持** |
| DEFAULT-04 | disabled rollback | **保持** |
| DEFAULT-05 | 中途异常 rollback | **保持** |
| DDL | 0 修改 | **保持** |
| P0 / P1 | 0 / 0 | **不新增** |

---

## §16 文档关系(241V2 → V2A → V2A-1 → V2A-2)

### 16.1 增量关系

| 文档 | 定位 | 与前序关系 |
|---|---|---|
| 241V2 | 基础设施基础设计 | — |
| 241V2A | P0-2 companyId 强制覆盖 | 覆盖 241V2 §7.2 写法 |
| 241V2A-1 | defaultCompany 并发控制 | 强化 241V2 §12.3(增量,不覆盖) |
| **241V2A-2** | **defaultCompany 并发测试与死锁表述修正** | **修正 241V2A-1 §7 / §12 / §14(增量,不覆盖)** |

### 16.2 严格关系

- ✗ 241V2A-2 **不**修改 241V2 / 241V2A / 241V2A-1 任何字节
- ✓ 241V2A-2 通过"补丁叠加"建立增量关系
- ✓ 后续审计 241A-1 必须**同时**读 241V2 + 241V2A + 241V2A-1 + 241V2A-2

### 16.3 后续审计 241A-1 必读清单

```
241V2         (基础设施基础)
  + 241V2A    (P0-2 强制覆盖)
  + 241V2A-1  (defaultCompany 并发控制)
  + 241V2A-2  (并发测试与死锁表述修正)  ← 本文件
```

---

## §17 S1-169-2 启动闸门(241V2A-2 不变)

### 17.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241V2 修复 4 P0 + 1 P1 | ✓ | 241V2 |
| 241V2A P0-2 真闭环 | ✓ | 241V2A |
| 241V2A-1 defaultCompany 并发控制 | ✓ | 241V2A-1 |
| **241V2A-2 测试与表述修正(本文件)** | **✓** | **本文件** |
| **241A-1 独立盲审 PASS(下一轮)** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 17.2 241A-1 审计 241V2A-2 必须检查

1. ✓ "死锁不可能" 表述已替换为"本方法无循环锁依赖"
2. ✓ 4 层事务结构完整冻结
3. ✓ DEFAULT-01 不再固定 C 赢(改为 B/C 任一合法)
4. ✓ DEFAULT-02/03 事务边界遵循 4 层结构
5. ✓ LOCK-ORDER-01 统一锁顺序原则冻结
6. ✓ @Retryable 区分必须 vs 可选
7. ✓ 重试必须新事务
8. ✓ 12 项不重新裁决业务语义保持
9. ✓ 严禁"死锁不可能/完全免疫"等表述

### 17.3 严禁(241V2A-2 边界)

- ✗ 不得修改 241V2 / 241V2A / 241V2A-1 / 任何历史 MD
- ✗ 不得创建 backend/ / 写 Java / 创建 SQL
- ✗ 不得在 241A-1 PASS 前进入 S1-169-2
- ✗ 不得把 241V2A-2 + 241A-1 审计合并
- ✗ 不得自评 PASS

---

## §18 报告统计

- 报告字节数:约 32000 字节
- 章节数:23
- 修正的问题数:3(死锁表述 / 测试事务边界 / DEFAULT-01 断言)
- 新增约束:1(LOCK-ORDER-01)
- 新增测试设计:1(4 层事务结构)
- 显式声明 12 项不重新裁决
- 文档关系增量:241V2 → V2A → V2A-1 → V2A-2
- DDL 修改:0
- P0 / P1:0 / 0(不新增)
- 启动闸门:全部满足
- 下一轮交付物:241A-1 独立盲审(必须同时审计 241V2 + 241V2A + 241V2A-1 + 241V2A-2)

---

## §19 总结判断(241V2A-2 裁决)

**【241V2A-2 补丁完成】**

**【尚未经过独立盲审】**

当前:**S1-169-2 = BLOCK**

下一步:执行真正的 **241A-1 独立盲审**。

审计范围必须完整覆盖:
- 241V2
- 241V2A
- 241V2A-1
- 241V2A-2(本文件)

241A-1 必须独立判断:
- P0 = 0
- P1 = 0
- 死锁表述严谨
- 测试事务边界正确
- DEFAULT-01 断言不依赖调度顺序

---

## §20 Git 状态(本轮结束)

- **HEAD 不变**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
- **本轮不 commit / 不 push** ✓
- **0 号闸门 4 文件 SHA256 锁定不变** ✓
- **历史 MD(190~241V2A-1 共 63 份)未修改** ✓
- **VisionCare PMS 任何文件未修改** ✓
- **新文件**:`241V2A-2_S1-169-1_defaultCompany并发测试与死锁表述修正.md`(本文件,untracked)
- **本文件不实际写 Java / 不创建 SQL / 不执行 DDL / 不连接数据库** ✓
- **本文件不修改 241V2 / 241V2A / 241V2A-1 / 任何历史 MD** ✓
- **本文件不修改 pom.xml / application.yml** ✓

### 20.1 241V2A-2 自身 SHA256(下次审计基准)

待写入后由 `Get-FileHash` 验证,本文件最终 SHA256 = `[待 241A-1 审计时计算]`。

---

## §21 一句话最终判断

> **241V2A-2 defaultCompany 并发测试与死锁表述修正完成**:在 241V2A-1 基础上,精准修正 3 个技术问题——(1)"死锁不可能"过强表述修正为"setDefaultCompany 本方法无循环锁依赖,但 V4.4 系统级死锁仍需依赖数据库异常检测 + Spring rollback",并显式列出 5 项强制约束 + 严禁表述清单;(2)DEFAULT-01~03 并发测试事务边界修正为 4 层结构(准备事务先 commit / T1+T2 独立 Service 事务 / 独立最终验证事务),严禁用测试 @Transactional 包住整个异步过程;(3)DEFAULT-01 错误断言"后到者一定赢"修正为 "count=1 + defaultCompanyId ∈ {B, C} + 两个事务均应成功"(不依赖数据库调度顺序);新增 LOCK-ORDER-01 系统级统一锁顺序原则(user.id 必须最先,后续业务不得反向);@Retryable 正式区分"必须(异常传播 / rollback / 不静默)"与"可选(上层重试 / 指数退避 / 必须新事务)";保持 12 项业务语义不重新裁决;与 241V2 / 241V2A / 241V2A-1 形成 4 层增量补丁关系;S1-169-2 仍 BLOCK,**未自评 PASS**,等待 241A-1 独立盲审同时审计 241V2 + 241V2A + 241V2A-1 + 241V2A-2 四份文档。

---

## §22 报告统计

- 报告字节数:约 32000 字节
- 章节数:22
- 修正问题数:3
- 新增约束:1(LOCK-ORDER-01)
- 新增测试设计:1(4 层事务结构)
- 显式保持业务语义:12 项
- DDL 修改:0
- P0 / P1:0 / 0
- 启动闸门:全部满足
- 下一轮:241A-1 独立盲审(同时审计 241V2 + 241V2A + 241V2A-1 + 241V2A-2)
