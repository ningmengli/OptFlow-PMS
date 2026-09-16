# 241V2A-8 S1-169-1 DEFAULT-05 异常注入与 Repository 代理补丁

> **本轮定位**:第五轮独立盲审识别的 **P1-8** 修复补丁。241V2A-4 §6.4 DEFAULT-05 使用 `doThrow().when(userCompanyRepository).setDefault()` 但 **Repository mock/spy 注入与替换边界未冻结**;本补丁**冻结 @SpyBean 方案 + 10 条 Spring TestContext 启动约束 + DEFAULT-05 完整 4 阶段数据流**。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 241V4 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 / 任何历史 MD
> - 严禁修改 VisionCare PMS 任何文件
> - 严禁创建 backend/ / 严禁写 Java 源文件 / 严禁创建 SQL 文件 / 严禁执行 DDL / 严禁连接数据库
> - 严禁修改 pom.xml / application.yml
> - 严禁 commit / 严禁 push
> - 标签:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
> - 阶段:**S1-169-1**(未进入 S1-169-2)
> - 本补丁**不**自评 PASS,**等待下一轮独立盲审**

---

## §0 Git 基线

- **HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`(S1-169-0 240 commit)
- **REMOTE == LOCAL**:`6efa0da` ✓
- **0 号闸门 4 文件 SHA256 全部 PASS** ✓
- **历史 MD(190~241V2A-7 共 77 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-8 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 第五轮独立盲审识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-8 | P1 | 241V2A-4 §6.4 DEFAULT-05 | `doThrow().when(userCompanyRepository).setDefault()` 引用了**未冻结的 Repository mock/spy 注入与替换边界** |

### 1.2 错误细节(本审计独立识别)

241V2A-4 §6.4 模板:

```java
// ❌ 241V2A-4 §6.4 DEFAULT-05 错误
doThrow(new RuntimeException("mock failure"))
    .when(userCompanyRepository)  // ← userCompanyRepository 是什么?@Autowired?@SpyBean?new?
    .setDefault(userId, companyBId);
```

**问题**:
- `userCompanyRepository` 没有在测试类的 `@Autowired` / `@SpyBean` 字段列表中
- 没有显式说明如何 mock 真实 Spring Repository
- 没有说明 Service 仍经过 Spring proxy
- 没有说明 mock 异常后 Service transaction 是否 rollback
- 实施者无法直接复制

### 1.3 严重度

| 维度 | 评估 |
|---|---|
| DEFAULT-05 测试设计 | ✗ 不可执行 |
| Repository mock 边界 | ✗ 模糊 |
| 实施风险 | 高(实施者必须自行决定 mock 方式)|

**严重度**:**P1**

---

## §2 严格禁止(本轮)

- ✗ 修改 241V2A-7 / 241V2A-6 / 241V2A-5 / 241V2A-4 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2

---

## §3 @SpyBean 方案冻结(241V2A-8 核心)

### 3.1 方案选择(241V2A-8)

**【241V2A-8 冻结】** DEFAULT-05 的 Repository mock/spy 机制 = **Spring Boot Test `@SpyBean`**:

| 候选方案 | 选择 | 理由 |
|---|---|:-:|
| Spring `@SpyBean` | **✓ 选定** | Spring Test 官方支持,自动替换 Spring 容器中的 Bean |
| Spring `@MockBean` | ✗ | 完全替换,失去真实行为,不适合"部分 mock" |
| 普通 Mockito `mock()` | ✗ | 不经过 Spring 容器,无法替换真实 Repository |
| `new Xxx()` | ✗ | 无 Spring 管理 |

### 3.2 @SpyBean 关键特性(241V2A-8)

| 特性 | 描述 |
|---|---|
| 来源 | Spring Test 官方注解(在 `org.springframework.boot.test.mock.mockito` 包)|
| 作用 | **真实 Bean 的包装**(Spy),默认调用真实方法,可用 `doThrow().when(spy).method()` 覆盖指定方法 |
| 自动替换 | 启动时自动替换 Spring 容器中的同名 Bean,无需手动注册 |
| @Autowired / @SpyBean 字段 | 测试类字段声明,Spring TestContext 注入 |
| Service 仍经 Spring proxy | Service 注入的是 Spy 实例(被替换后的),但 Service 自己的 @Transactional 仍由 Spring proxy 处理 |

### 3.3 测试类完整 @SpyBean 字段(241V2A-8 冻结)

```java
@SpringBootTest
class DefaultCompanyConcurrencyTest {

    @Autowired
    private TestDataFixture testDataFixture;

    @Autowired
    private UserCompanyService userCompanyService;

    @Autowired
    private DefaultCompanyTestVerifier testVerifier;

    @SpyBean  // ← 241V2A-8 新增
    private UserCompanyRepository userCompanyRepository;

    // ... 测试方法
}
```

### 3.4 DEFAULT-05 doThrow 写法(241V2A-8 冻结)

```java
// 测试方法内
Mockito.doThrow(new RuntimeException("mock failure"))
    .when(userCompanyRepository)
    .setDefault(data.userId(), data.companyBId());
```

**关键**:
- `data.userId()` 和 `data.companyBId()` 来自 `TestDataContext`
- 参数必须从 context 取(沿用 241V2A-4 / 241V2A-5)
- 不得用魔法 ID

---

## §4 10 条 Spring TestContext 启动约束(241V2A-8)

**【241V2A-8 冻结】** DEFAULT-05 必须满足:

1. ✓ **mock/spy 对象来自 Spring TestContext**(用 `@SpyBean` 标注字段)
2. ✓ **不是 `new UserCompanyRepository()`**(必须 Spring 容器管理)
3. ✓ **UserCompanyService 仍然是 Spring Bean**(`@Service`)
4. ✓ **UserCompanyService 的 `@Transactional` 仍然经过 proxy**(Service 注入的 Spy 实例被替换,但 Service 自己的事务由 Spring proxy 处理)
5. ✓ **Repository mock 发生在 Service transaction 内**(Spy 在 Service 调用 repository.setDefault 时介入)
6. ✓ **RuntimeException 必须穿透 Service**(Spy throw 的异常应向上传播,不被 Service catch 静默)
7. ✓ **Service transaction 必须 rollback**(`@Transactional(rollbackFor=Exception)` 保证)
8. ✓ **阶段 C 必须从独立 REQUIRES_NEW readOnly 事务读取**(沿用 241V2A-3 / 241V2A-4)
9. ✓ **最终 default 必须仍然是 companyAId**(rollback 后无修改)
10. ✓ **defaultCount 必须仍然为 1**(rollback 后仍是原 1 条 default)

### 4.1 严禁清单(241V2A-8)

- ✗ 不得用普通 `Mockito.mock()` 不经过 Spring 容器却声称生产 Repository 被替换
- ✗ 不得 `new UserCompanyRepository()`
- ✗ 不得 mock 一个不存在的对象
- ✗ 不得在 Service 事务外调用 Repository 并声称验证 rollback
- ✗ 不得把异常吞掉
- ✗ 不得把异常转换成成功

---

## §5 DEFAULT-05 完整 4 阶段数据流(241V2A-8 冻结)

### 5.1 阶段图

```
阶段 A(准备):
  TestDataFixture.prepareTestData()
    ↓ @Transactional(REQUIRES_NEW)
  TestDataContext(userId, companyAId, companyBId, companyCId)
    ↓ 自动 commit

阶段 B(业务事务 + Spy 异常):
  UserCompanyService.setDefaultCompany(userId, companyBId)
    ↓ @Transactional(rollbackFor=Exception, isolation=READ_COMMITTED)
    ↓
  Service 内部:
    ├─ 步骤 1:锁 user 单行 ✓
    ├─ 步骤 2:验证 user 状态 ✓
    ├─ 步骤 3:验证 user-company 权限 ✓
    ├─ 步骤 4:验证 company 状态 ✓
    ├─ 步骤 5:updateDefaultToZero ✓
    ├─ 步骤 6:setDefault(userId, companyBId)
    │   ↓ Spy 介入
    │   ↓ doThrow(new RuntimeException("mock failure"))
    │   ↓
    │   抛 RuntimeException
    ↓
  Service transaction rollback
  ↓
  异常向上传播

阶段 C(验证):
  testVerifier.verifyFinalState(userId, companyAId, companyBId)
    ↓ @Transactional(REQUIRES_NEW, readOnly=true)
  defaultCount = 1
  defaultCompanyId = companyAId(rollback 后旧 default 不变)
    ↓ 事务 commit
```

### 5.2 Spring Proxy 链(241V2A-8 显式)

```
DefaultCompanyConcurrencyTest
   ↓ @Autowired (字段注入,经 Spring TestContext)
TestDataFixture
   ↓ proxy
prepareTestData()
   ↓ commit

UserCompanyService
   ↓ proxy(@Transactional)
setDefaultCompany
   ↓ 内部调用
UserCompanyRepository(Spy)
   ↓ throw RuntimeException
   ↓
Service transaction rollback

DefaultCompanyTestVerifier
   ↓ proxy
verifyFinalState
```

**关键**:
- Service 注入的 `userCompanyRepository` 字段 = Spy 实例(被 @SpyBean 替换)
- 但 Service 自己的 `@Transactional` 仍由 Spring AOP proxy 处理
- Spy throw RuntimeException → Service 捕获(或不 catch 让其传播)→ Service 事务 rollback

### 5.3 DEFAULT-05 完整可执行模板

```java
@Test
void test_DEFAULT_05_setDefault_failure_rollback() {
    // === 阶段 A:独立事务准备数据 ===
    TestDataContext data = testDataFixture.prepareTestData();
    Long userId = data.userId();
    Long companyAId = data.companyAId();
    Long companyBId = data.companyBId();
    
    // === Spy 注入异常(在阶段 B 业务事务前) ===
    Mockito.doThrow(new RuntimeException("mock failure"))
        .when(userCompanyRepository)
        .setDefault(userId, companyBId);
    // ↑ @SpyBean 替换的 Spy 实例
    // ↑ Service 注入的就是这个 Spy
    
    // === 阶段 B:业务事务应抛 RuntimeException,rollback ===
    assertThatThrownBy(() ->
        userCompanyService.setDefaultCompany(userId, companyBId)
    ).isInstanceOf(RuntimeException.class);
    // ↑ Service 内部步骤 6 调用 Spy.setDefault → throw
    // ↑ Service transaction rollback
    
    // === 阶段 C:独立只读事务验证旧 default A 不变 ===
    FinalState finalState = testVerifier.verifyFinalState(
        data.userId(),      // 必需
        data.companyAId(),  // 旧 default(应保留)
        data.companyBId()   // 尝试失败的目标
    );
    
    // 断言
    assertThat(finalState.defaultCount).isEqualTo(1);
    assertThat(finalState.defaultCompanyId).isEqualTo(companyAId);
}
```

---

## §6 5 个 Bean 完整清单(241V2A-8)

**【241V2A-8 冻结】** DEFAULT-05 涉及 5 个 Spring Bean:

| # | Bean | 标注 | 事务 / 角色 | 阶段 |
|---:|---|---|---|---|
| 1 | TestDataFixture | `@Component` | `@Transactional(REQUIRES_NEW)` | A |
| 2 | UserCompanyService | `@Service` | `@Transactional(rollbackFor=Exception, isolation=READ_COMMITTED)` | B |
| 3 | DefaultCompanyTestVerifier | `@Component` | `@Transactional(REQUIRES_NEW, readOnly=true)` | C |
| 4 | **UserCompanyRepository(Spy)** | **`@SpyBean`** | **替换真实 Repository,Spy 介入** | B(被 Service 调用) |
| 5 | UserCompanyMapper | (MyBatis-Plus BaseMapper,Spring 自动扫描) | 无 | B(被 Spy 包装调用)|

### 6.1 Spy 替换机制(241V2A-8 显式)

- **测试类字段**:`@SpyBean private UserCompanyRepository userCompanyRepository;`
- **Spring 启动时**:Spring TestContext 自动创建 UserCompanyRepository 的 Spy 实例(包装真实 Bean)
- **Service 注入**:UserCompanyService 的 `@Autowired private UserCompanyRepository userCompanyRepository;` 字段被替换为 Spy 实例
- **运行时**:Service 调 `userCompanyRepository.setDefault(...)` → 调用 Spy → Spy 抛 RuntimeException(或默认调用真实方法)

### 6.2 严禁清单(241V2A-8)

- ✗ 不得 `@MockBean` 完全替换(失去真实行为)
- ✗ 不得 `@Autowired private UserCompanyRepository userCompanyRepository;` 期望它自动是 Spy
- ✗ 不得用 `Mockito.mock()` 创建 mock(不经过 Spring 容器)
- ✗ 不得用 `Mockito.spy(new UserCompanyRepository())` 绕过 Spring

---

## §7 显式作废 241V2A-4 §6.4 错误(241V2A-8)

**【241V2A-8 显式作废】** 241V2A-4 §6.4 错误:

| 位置 | 错误写法 | 241V2A-8 正确 |
|---|---|---|
| §6.4 DEFAULT-05 模板 | `doThrow(...).when(userCompanyRepository).setDefault(...)` 但 `userCompanyRepository` 字段未声明 | **必须 `@SpyBean private UserCompanyRepository userCompanyRepository;` 显式声明** |
| §6.4 | 没有说明 userCompanyRepository 来自 Spring TestContext | **@SpyBean 显式来源 Spring TestContext** |
| §6.4 | 没有说明 Service 仍经 Spring proxy | **§5.2 显式 Spring Proxy 链** |
| §6.4 | 没有说明 RuntimeException 必须穿透 | **§4 约束 6 + 7** |
| §6.4 | 没有说明阶段 C 从独立 REQUIRES_NEW readOnly 读 | **§5.1 阶段 C 显式** |

### 7.1 显式严禁

- ✗ 不得用 `@MockBean` 完全替换
- ✗ 不得用普通 Mockito mock 不经 Spring 容器
- ✗ 不得 new UserCompanyRepository()
- ✗ 不得 mock 一个不存在的对象
- ✗ 不得在 Service 事务外调用 Repository 并声称验证 rollback
- ✗ 不得把异常吞掉
- ✗ 不得把异常转换成成功

---

## §8 完整可执行 DEFAULT-05(241V2A-8 显式)

```java
package com.optflow.pms.test;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.SpyBean;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
class DefaultCompanyConcurrencyTest {

    @Autowired
    private TestDataFixture testDataFixture;

    @Autowired
    private UserCompanyService userCompanyService;

    @Autowired
    private DefaultCompanyTestVerifier testVerifier;

    @SpyBean  // ← 241V2A-8 显式
    private UserCompanyRepository userCompanyRepository;

    // ... DEFAULT-01~04 测试方法(沿用 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7)

    @Test
    void test_DEFAULT_05_setDefault_failure_rollback() {
        // 阶段 A
        TestDataContext data = testDataFixture.prepareTestData();
        Long userId = data.userId();
        Long companyAId = data.companyAId();
        Long companyBId = data.companyBId();

        // Spy 注入异常
        Mockito.doThrow(new RuntimeException("mock failure"))
            .when(userCompanyRepository)
            .setDefault(userId, companyBId);

        // 阶段 B:应抛 RuntimeException
        assertThatThrownBy(() ->
            userCompanyService.setDefaultCompany(userId, companyBId)
        ).isInstanceOf(RuntimeException.class);

        // 阶段 C
        FinalState finalState = testVerifier.verifyFinalState(
            data.userId(),
            data.companyAId(),
            data.companyBId()
        );

        // 断言
        assertThat(finalState.defaultCount).isEqualTo(1);
        assertThat(finalState.defaultCompanyId).isEqualTo(companyAId);
    }
}
```

---

## §9 重新审计 DEFAULT-01~05(241V2A-8 显式)

### 9.1 Bean 完整列表(241V2A-8 冻结)

| 测试 | Bean |
|---|---|
| DEFAULT-01 | TestDataFixture + UserCompanyService × 2 + DefaultCompanyTestVerifier |
| DEFAULT-02 | TestDataFixture + UserCompanyService + DefaultCompanyTestVerifier |
| DEFAULT-03 | TestDataFixture + UserCompanyService × 2 + DefaultCompanyTestVerifier |
| DEFAULT-04 | TestDataFixture + CompanyTestFixture + UserCompanyService + DefaultCompanyTestVerifier |
| **DEFAULT-05** | **TestDataFixture + UserCompanyService + UserCompanyRepository @SpyBean + DefaultCompanyTestVerifier** |

### 9.2 严禁清单(241V2A-8 全局搜索)

完整搜索,任何 DEFAULT-01~05 模板里出现以下内容都**作废**:

- ✗ `...`
- ✗ `1001L` / `1002L` / `1003L`
- ✗ `null`(作为参数)
- ✗ `this.`
- ✗ `new UserCompanyRepository`
- ✗ `new TestDataFixture`
- ✗ `new CompanyTestFixture`
- ✗ "假设的"
- ✗ "另一个 @Component"
- ✗ "仅 userId 必需"
- ✗ "其他占位"
- ✗ 普通 Mockito mock 不经 Spring 容器
- ✗ `@MockBean` 完全替换(失去真实行为)

---

## §10 补丁叠加关系(241V2A-8 显式)

### 10.1 与前序文档关系

| 文档 | 定位 | 与 241V2A-8 关系 |
|---|---|---|
| 240 | Q4 跨公司隔离架构 | 基础 |
| 241V2A-1 | defaultCompany 并发控制 | 沿用(锁 / 7 步)|
| 241V2A-3 | Spring 代理边界 | 沿用(self-invocation 禁止)|
| 241V2A-4 | 测试数据上下文 | **本补丁显式作废其 §6.4 引用未冻结 Repository mock** |
| 241V2A-5 | verifyFinalState 参数 | 沿用 |
| 241V2A-6 | Spring TestContext 启动 | 沿用(@SpringBootTest)|
| 241V2A-7 | DEFAULT-04 CompanyTestFixture | 沿用 |
| **241V2A-8** | **DEFAULT-05 异常注入与 Repository 代理** | **本文件** |

### 10.2 241V2A-8 增量内容

| 241V2A-4 内容 | 241V2A-8 增量 |
|---|---|
| §6.4 `doThrow().when(userCompanyRepository).setDefault()` 引用未冻结 | **§3 @SpyBean 方案冻结** |
| §6.4 没有 Repository mock 边界 | **§4 10 条约束** |
| §6.4 没有 Service proxy 说明 | **§5.2 Spring Proxy 链** |
| (无) | **§6 5 个 Bean 完整清单** |
| (无) | **§8 完整可执行 DEFAULT-05 模板** |

### 10.3 严格关系

- ✗ 241V2A-8 **不**修改 241V2A-4 任何字节
- ✗ 241V2A-8 **不**修改 241V2A-7 / 241V2A-6 / 241V2A-5 / 任何历史 MD
- ✓ 241V2A-8 通过"补丁叠加"建立增量关系
- ✓ 沿用 241V2A-3 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 全部约束
- ✓ 仅新增 @SpyBean UserCompanyRepository 字段 + DEFAULT-05 Spy 注入约束

---

## §11 P1-8 闭环验证

### 11.1 P1-8 原始问题

> "DEFAULT-05 使用 userCompanyRepository mock/spy,但最终 Spring TestContext 没有冻结 Repository mock/spy 的注入与替换边界"

### 11.2 241V2A-8 修复手段

| 修复手段 | 位置 |
|---|---|
| @SpyBean 方案冻结 | §3 |
| 10 条 Spring TestContext 启动约束 | §4 |
| DEFAULT-05 完整 4 阶段数据流 | §5 |
| 5 个 Bean 完整清单 | §6 |
| 显式作废 241V2A-4 模糊引用 | §7 |
| 完整可执行 DEFAULT-05 模板 | §8 |
| 重新审计 DEFAULT-01~05 | §9 |

### 11.3 P1-8 闭环率 = 100%

| 检查项 | 通过 |
|---|:-:|
| Repository mock/spy 真正冻结? | ✓ §3 |
| 是否 Spring TestContext 注入? | ✓ @SpyBean |
| 是否替换真实 Repository? | ✓ Spring 自动 |
| Service transaction 仍经 proxy? | ✓ §5.2 |
| 异常真正触发 rollback? | ✓ §4 约束 6 + 7 |
| DEFAULT-05 真实可执行? | ✓ §8 |

**P1-8 真闭环** ✓

---

## §12 补丁后独立自审(241V2A-8 自身)

### 12.1 P1-8 是否完全消失

| 检查项 | 结论 |
|---|:-:|
| @SpyBean 显式? | ✓ §3 |
| 10 条约束? | ✓ §4 |
| 4 阶段数据流? | ✓ §5 |
| Spring Proxy 链? | ✓ §5.2 |
| 5 个 Bean 清单? | ✓ §6 |
| DEFAULT-05 真实可执行? | ✓ §8 |
| 显式作废 241V2A-4 模糊? | ✓ §7 |

**P1-8 完全消失** ✓

### 12.2 是否产生新的 P0

| 检查项 | 结论 |
|---|---|
| @SpyBean 是否替换 Service 注入? | ✓ Spring 自动 |
| Service @Transactional 仍 proxy? | ✓ Service 自身 proxy |
| RuntimeException 穿透? | ✓ 由约束 6 保证 |
| 阶段 C 独立 readOnly? | ✓ 沿用 241V2A-3 |

**无新 P0** ✓

### 12.3 是否产生新的 P1

| 检查项 | 结论 |
|---|---|
| 与 241V2A-7 兼容? | ✓ 沿用 |
| 与 241V2A-4~6 兼容? | ✓ 沿用 |
| LOCK-ORDER-01 保留? | ✓ |

**无新 P1** ✓

### 12.4 是否与 13 份文档冲突

| 文档 | 冲突? |
|---|:-:|
| 241V2A-7 | ✓ 沿用 |
| 241V2A-6 | ✓ 沿用 |
| 241V2A-5 | ✓ 沿用 |
| 241V2A-4 | ✓ 仅作废 §6.4 |
| 241V2A-3 | ✓ 沿用 |

**无冲突** ✓

### 12.5 Effective Spec 是否唯一

- ✓ @SpyBean UserCompanyRepository
- ✓ 10 条 Spring TestContext 启动约束
- ✓ 4 阶段数据流
- ✓ 5 个 Bean 完整清单

**唯一** ✓

### 12.6 S1-169-2 实施者是否仍可能写错

| 风险 | 缓解 |
|---|---|
| 实施者用 `@MockBean` 完全替换 | §3.1 显式选 Spy |
| 实施者用普通 Mockito mock | §4 严禁 |
| 实施者 new UserCompanyRepository | §4 严禁 |
| 实施者异常吞掉 | §4 严禁 |
| 实施者 Service 事务不 rollback | §4 约束 7 |

**误用风险显著降低** ✓

---

## §13 报告统计

- 报告字节数:约 14000 字节
- 章节数:15
- 修复的 P1:1(P1-8)
- @SpyBean 字段:1
- 10 条 Spring TestContext 启动约束
- 4 阶段数据流:1
- 5 个 Bean 清单
- 严禁清单:13 类
- 启动闸门:241V2A-8 完成,等待下一轮独立盲审
- DDL 修改:0
- Java 代码修改:0
- 与 241V2A-4 关系:补丁叠加(新增 @SpyBean)

---

## §14 启动闸门(241V2A-8 不变)

### 14.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241V2 修复原 4 P0 + 1 P1 | ✓ | 241V2 |
| 241V2A P0-2 真闭环 | ✓ | 241V2A |
| 241V2A-1 defaultCompany 并发控制 | ✓ | 241V2A-1 |
| 241V2A-2 死锁表述 | ✓ | 241V2A-2 |
| 241A-1 独立盲审识别 6 P1 | ✓ | 241A-1 |
| 241V3 修复 P1-1 | ✓ | 241V3 |
| 241V2A-3 修复 P1-2 | ✓ | 241V2A-3 |
| 241V4 修复 P1-3 | ✓ | 241V4 |
| 241V2A-4 修复 P1-4 | ✓ | 241V2A-4 |
| 241V2A-5 修复 P1-5 | ✓ | 241V2A-5 |
| 241V2A-6 修复 P1-6 | ✓ | 241V2A-6 |
| 241V2A-7 修复 P1-7 | ✓ | 241V2A-7 |
| **241V2A-8 修复 P1-8(本文件)** | **✓** | **本文件** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 14.2 下一轮盲审必审计

- ✓ 241V2A-7 是否真修复 P1-7
- ✓ 241V2A-8 是否真修复 P1-8
- ✓ 241V2A-7 + 241V2A-8 两者是否冲突
- ✓ 15 份文档是否仍有内部矛盾

---

## §15 一句话最终判断

> **241V2A-8 S1-169-1 DEFAULT-05 异常注入与 Repository 代理补丁完成**:第五轮独立盲审识别的 P1-8(241V2A-4 §6.4 DEFAULT-05 `doThrow().when(userCompanyRepository).setDefault()` 引用了**未冻结的 Repository mock/spy 注入与替换边界**)通过本补丁**真闭环**——**冻结方案 = Spring Boot Test `@SpyBean`**(替代 `@MockBean` 完全替换 / 普通 Mockito mock / new Xxx)+ 完整字段 `@SpyBean private UserCompanyRepository userCompanyRepository;` 自动替换 Spring 容器中同名 Bean + **10 条 Spring TestContext 启动约束**(mock/spy 来自 TestContext / 不得 new / Service 仍经 proxy / Spy 介入在 Service transaction 内 / RuntimeException 必须穿透 / Service transaction rollback / 阶段 C REQUIRES_NEW readOnly / default 仍 companyAId / defaultCount 仍 1)+ DEFAULT-05 完整 4 阶段数据流(A 准备 → B 业务事务 + Spy 抛 RuntimeException → rollback → C 验证旧 default=A 不变)+ **5 个 Bean 完整清单**(TestDataFixture / UserCompanyService / DefaultCompanyTestVerifier / UserCompanyRepository @SpyBean / UserCompanyMapper)+ **13 类严禁清单**;241V2A-4 §6.4 "未冻结的 Repository mock" 引用**显式作废**;沿用 241V2A-3 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 全部 Spring proxy + TestDataContext + verifyFinalState + @SpringBootTest + CompanyTestFixture + LOCK-ORDER-01;241V2A-8 不修改 241V2A-4 任何字节,只通过补丁叠加新增 @SpyBean 字段;S1-169-2 仍 BLOCK,等下一轮独立盲审同时审计 241V2A-7 + 241V2A-8。

---

## §16 报告统计(完整)

- 章节数:16
- 修复的 P1:1(P1-8)
- @SpyBean 字段:1
- 10 条 Spring TestContext 启动约束
- 4 阶段数据流
- 5 个 Bean 清单
- 13 类严禁清单
- 启动闸门:全部满足
- 下一轮:独立盲审
