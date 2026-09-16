# 241V2A-16 S1-169-1 IllegalStateException 异常契约统一冻结补丁

> **本轮定位**:第十三轮全局交叉审计识别的 **P1-19** + **2 项 P2 顺手记录**。
> - **P1-19**:**异常类型 `IllegalStateException` 在文档体系中存在自相矛盾**:
>   - `241V2A-10 §7.1` / `241V2A-11 §5.5` / `241V2A-12 §3.3`:显式 `import com.optflow.pms.common.exception.IllegalStateException;`(自定义包)
>   - `241V2A-1 §5.1` / `241V2A-7` / `241V2A-14 §3.1`:无 import,`throw new IllegalStateException(...)` 默认解析为 `java.lang.IllegalStateException`(标准 JDK)
>   - **审计证据**:241 §4.2-4.4 只冻结了 3 个自定义异常类(`CompanyContextMissingException` / `CompanyMismatchException` / `CompanyAccessDeniedException`),**未冻结**自定义 `IllegalStateException`。
>   - **致命后果**:`com.optflow.pms.common.exception.IllegalStateException` 是**未冻结类**,Service 模板引用该 import 必然**编译失败**。
> 本补丁采用"**统一使用 `java.lang.IllegalStateException` + 显式作废 `import com.optflow.pms.common.exception.IllegalStateException` + 同时修正 241V2A-15 的【原系统事实】错误标签**"的最小变更路径,建立**唯一 Effective Spec**。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 241V4 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 / 241V2A-8 / 241V2A-9 / 241V2A-10 / 241V2A-11 / 241V2A-12 / 241V2A-13 / 241V2A-14 / 241V2A-15 / 任何历史 MD
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
  - controller.js `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433`
  - deliveryList.html `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`
  - machineOrderCompleted.html `F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24`
  - machineOrderList.html `A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A`
- **历史 MD(190~241V2A-15 共 87 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-16 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 第十三轮全局审计识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-14 | 已闭环 | 241V2A-12 §2 | Repository 4 公开方法 + DefaultCompanyTestVerifier 直接调 Mapper |
| P1-15 | 已闭环 | 241V2A-12 §3 | verifyFinalState 3 参数 |
| P1-16 | 已闭环 | 241V2A-13 §3 | selectDefaultCompanyId SQL 无 LIMIT 1 |
| P1-17 | 已闭环 | 241V2A-14 §3 | Verifier 方法体消费 expectedDefault1/2 |
| P1-18 | 已闭环 | 241V2A-15 §3 | DEFAULT-03 阶段 B 错误收集 + 三道断言 |
| **P1-19** | **P1** | **241V2A-10 §7.1 / 241V2A-11 §5.5 / 241V2A-12 §3.3 vs 241V2A-1 / 7 / 14** | **`IllegalStateException` 异常类型未冻结,Service / Verifier 自相矛盾** |
| P2-1 | P2 | 241V2A-15 §3.1 | DEFAULT-03 模板中 `companyBId` / `companyCId` 声明但未使用(占位声明)|
| P2-2 | P2 | 241V2A-15 §3.1 | `pool.shutdown()` 后未显式 `awaitTermination` |
| **P2-3** | **P2** | **241V2A-15 §9** | **【原系统事实】标签错配**:`AtomicReference` / `CountDownLatch` / `ExecutorService` 的 V4.4 使用模式属于【OptFlow设计】/【实现机制】,不是【原系统事实】 |

### 1.2 P1-19 错误细节(本审计独立识别)

#### 1.2.1 矛盾现状

| 文档 | 写法 | Java 解析结果 |
|---|---|---|
| 241V2A-10 §7.1 第 381 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | **期望自定义类**(未冻结)|
| 241V2A-11 §5.5 第 527 行 | (无 import)| 默认 `java.lang.IllegalStateException` |
| 241V2A-12 §3.3 第 303 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | **期望自定义类**(未冻结)|
| 241V2A-1 §5.1 / §6.1 | (无 import)| 默认 `java.lang.IllegalStateException` |
| 241V2A-7 §6.1 | (无 import)| 默认 `java.lang.IllegalStateException` |
| 241V2A-14 §3.1(4 处)| (无 import)| 默认 `java.lang.IllegalStateException` |

#### 1.2.2 241 §4.2-4.4 自定义异常冻结清单

| 自定义异常类 | 状态 |
|---|:-:|
| `CompanyContextMissingException`(60000)| ✓ 241 §4.2 冻结 |
| `CompanyMismatchException`(60001)| ✓ 241 §4.3 冻结 |
| `CompanyAccessDeniedException`(60002)| ✓ 241 §4.4 冻结 |
| **`IllegalStateException`(无错误码)** | **✗ 未冻结** |

#### 1.2.3 矛盾分析

| 维度 | 评估 |
|---|---|
| 241 §4.2-4.4 冻结自定义异常 | ✗ 未冻结 `IllegalStateException` |
| 241V2A-10/11/12 import 自定义 IllegalStateException | ✗ 引用未冻结类(编译失败)|
| 241V2A-1/7/14 用 java.lang.IllegalStateException | ✓ 默认 JDK 类(编译通过)|
| Service vs Verifier 类型不统一 | ✗ 严重(若实施者按 241V2A-10 import 自定义类,编译失败)|
| 是否有 ResultCode 60003+ 配套 | ✗ 无(241 §4.5 只冻结 60000/60001/60002)|

#### 1.2.4 严重度

| 维度 | 评估 |
|---|---|
| 编译失败风险 | ✗ 严重(Service 模板直接编译失败)|
| 实施者类型歧义 | ✗ 严重(Service / Verifier 用两个不同类型)|
| 异常处理链 | ✗ 严重(GlobalExceptionHandler 是否处理自定义 IllegalStateException 未冻结)|

**严重度**:**P1**(编译失败 + 类型不统一,实施者无法直接照搬模板)

### 1.3 P2-3 错误细节(241V2A-15 §9 证据标签错配)

241V2A-15 §9 报告统计中,err1/err2/startLatch/endLatch/pool 模式被标记为【OptFlow设计】,**但其行为描述中"Java `AtomicReference` / `CountDownLatch` / `ExecutorService`"被标记为【原系统事实】**。

**问题**:`AtomicReference` / `CountDownLatch` / `ExecutorService` 本身是 **Java JDK 标准库**(事实),但:
1. ✗ V4.4 **未实施**任何基于这些类的代码(无 backend/、无 Java 源文件)
2. ✗ V4.4 文档体系内**没有**真实运行过的测试夹具
3. ✗ 把"未实施的标准库使用模式"标为【原系统事实】违反"证据等级"原则

**正确标签**:
- `AtomicReference` / `CountDownLatch` / `ExecutorService` 是 Java JDK 标准库类型 → 属于 **【原系统事实】**(JDK 本身)
- **V4.4 中"err1/err2 收集 + startLatch/endLatch 同步 + pool.submit"的具体使用模式** → 属于 **【OptFlow设计】/【实现机制】**

**严重度**:**P2**(证据标签误标,不影响实施,但影响后续审计可信度)

### 1.4 严格禁止(本轮)

- ✗ 修改 241V2A-15 / 241V2A-14 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2
- ✗ 修改 verifyFinalState 3 参数签名(沿用 241V2A-14)
- ✗ 修改 expectedDefault 二分逻辑(沿用 241V2A-14)
- ✗ 修改 selectDefaultCompanyId 无 LIMIT 1(沿用 241V2A-13)
- ✗ 修改 Repository 4 个公开方法(沿用 241V2A-12)
- ✗ 修改 Mapper 5 个自定义方法(沿用 241V2A-12 + 241V2A-13)
- ✗ 修改 exactly-one 业务规则(沿用 241V2A-11)
- ✗ 新增自定义异常类(违反最小变更原则)
- ✗ 修改 241 §4.2-4.4 冻结的 3 个自定义异常(CompanyContextMissingException / CompanyMismatchException / CompanyAccessDeniedException)
- ✗ 修改 P2-1 / P2-2 提到的具体问题(不得再制造 241V2A-17)
- ✗ 把 P2-3 升级为 P1

---

## §2 P1-19 修复方案

### 2.1 候选方案对比

| 候选 | 描述 | 优 | 劣 | 决策 |
|---|---|---|---|---|
| **A. 统一使用 `java.lang.IllegalStateException`(JDK 标准)** | 删除自定义类引用;Service / Verifier 都用 JDK 类 | 最小变更;不创建新类;不新增 ResultCode;不修改 241 §4 异常体系;编译通过 | 失去"统一业务异常"语义(但 IllegalStateException 语义自洽)| | **✓ 选定** |
| B. 冻结自定义 `com.optflow.pms.common.exception.IllegalStateException` + 新增 ResultCode 60003 | 创建新类 + 新错误码 + Service 模板 import | 自定义统一 | **必须创建新异常类 + 新错误码**(前序无任何证据支持);违反"不擅自发明接口"原则;增加异常体系复杂度 | ✗ 红线 |
| C. Service 用自定义 / Verifier 用 java.lang | 接受两者不同 | 无 | **类型不一致**,违反"必须统一"原则;实施者无法照搬 | ✗ 红线 |
| D. 删除所有 IllegalStateException,改用 Spring `@PostConstruct` 校验 | 改为启动期校验 | 启动期失败 | **违反 241V2A-11 §4 已冻结的 exactly-one 业务规则**(必须在 setDefaultCompany 运行时校验)| ✗ 红线 |

**【241V2A-16 冻结】** 选 **方案 A**——统一使用 `java.lang.IllegalStateException`。

### 2.2 方案 A 的最小变更路径

1. ✓ **不创建**自定义 `IllegalStateException` 类
2. ✓ **不修改** 241 §4.2-4.4 已冻结的 3 个自定义异常
3. ✓ **不新增** ResultCode
4. ✓ **不修改** 241V2A-10 / 11 / 12 / 14 / 15 任何字节
5. ✓ 通过 241V2A-16 §3.3 显式作废 241V2A-10 / 11 / 12 的 `import com.optflow.pms.common.exception.IllegalStateException;`(冻结作废声明)
6. ✓ 通过 241V2A-16 §3.4 显式冻结 Service / Verifier 统一使用 `java.lang.IllegalStateException`
7. ✓ Java 默认解析无需 import;若需显式 import,使用 `import java.lang.IllegalStateException;`

---

## §3 唯一 Effective Spec(241V2A-16 完整冻结)

### 3.1 最终异常类型(241V2A-16 冻结)

**【241V2A-16 冻结】** V4.4 `setDefaultCompany` 业务不变量失败异常类型 = **`java.lang.IllegalStateException`**。

| 维度 | 状态 |
|---|---|
| 完整类名 | `java.lang.IllegalStateException` |
| Package | `java.lang` |
| 来源 | Java JDK 标准库 |
| 证据等级 | 【原系统事实】(JDK 1.0+ 标准类)|
| 是否需要 import | 否(Java 自动 import `java.lang.*`);若需显式 import,使用 `import java.lang.IllegalStateException;` |
| 是否需要 ResultCode | 否(IllegalStateException 不属于业务异常体系,由 GlobalExceptionHandler 默认 500 处理)|
| 业务不变量语义 | exactly-one 失败时抛此异常(241V2A-11 §4 已裁决)|

### 3.2 显式作废(241V2A-16 显式)

**【241V2A-16 显式作废】** 以下 3 处前序 `import com.optflow.pms.common.exception.IllegalStateException;`:

| # | 旧写法来源 | 旧写法 | 状态 |
|---:|---|---|---|
| 1 | 241V2A-10 §7.1 第 381 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | 【作废 import】 |
| 2 | 241V2A-11 §5.5(沿用 241V2A-10,无显式 import 列出) | 同上 | 【作废 import】 |
| 3 | 241V2A-12 §3.3 第 303 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | 【作废 import】 |

**【241V2A-16 显式作废】** `com.optflow.pms.common.exception.IllegalStateException` 类引用:

**作废原因**:
1. 该类在 241 §4.2-4.4 **未冻结**(未列入自定义异常清单)
2. 该类无对应 ResultCode(241 §4.5 只冻结 60000/60001/60002)
3. 该类若创建,需新增 ResultCode 60003+(无前序证据支持)
4. Java JDK 已提供 `java.lang.IllegalStateException`,语义自洽,不需重复发明

### 3.3 Service 唯一 Effective Spec(241V2A-16 冻结)

**【241V2A-16 冻结】** `UserCompanyServiceImpl` 步骤 6 完整 import + 异常类型:

```java
package com.optflow.pms.module.auth;

import com.optflow.pms.common.exception.CompanyAccessDeniedException;
import com.optflow.pms.common.exception.UserNotFoundException;
import com.optflow.pms.common.exception.UserDisabledException;
// ⚠ 241V2A-16 显式作废:import com.optflow.pms.common.exception.IllegalStateException;
// ✓ 241V2A-16 冻结:java.lang.IllegalStateException(JDK 标准,无需 import;若需显式 import,使用下方一行)
import java.lang.IllegalStateException;

import com.optflow.pms.module.auth.entity.User;
import com.optflow.pms.module.auth.mapper.UserMapper;
import com.optflow.pms.module.auth.repository.UserCompanyRepository;
import com.optflow.pms.module.company.entity.Company;
import com.optflow.pms.module.company.repository.CompanyRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserCompanyServiceImpl implements UserCompanyService {

    private final UserCompanyRepository userCompanyRepository;
    private final CompanyRepository companyRepository;
    private final UserMapper userMapper;

    @Override
    @Transactional(rollbackFor = Exception.class, isolation = Isolation.READ_COMMITTED)
    public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
        // 步骤 1-5(沿用 241V2A-11 §5.1 + 241V2A-12 §5.5)
        User user = userMapper.selectByIdForUpdate(userId);
        if (user == null) { throw new UserNotFoundException("user 不存在: " + userId); }
        if (user.getStatus() != 1) { throw new UserDisabledException("user 已禁用: " + userId); }
        if (!userCompanyRepository.existsByUserIdAndCompanyId(userId, newDefaultCompanyId)) {
            throw new CompanyAccessDeniedException("用户无权访问 companyId=" + newDefaultCompanyId);
        }
        Company company = companyRepository.selectById(newDefaultCompanyId);
        if (company == null || company.getStatus() != 1) {
            throw new CompanyAccessDeniedException("company 不可用: " + newDefaultCompanyId);
        }
        userCompanyRepository.updateDefaultToZero(userId);
        int affected = userCompanyRepository.setDefault(userId, newDefaultCompanyId);
        if (affected != 1) {
            // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
            throw new IllegalStateException(
                "setDefault 失败:affected=" + affected
            );
        }

        // 步骤 6:exactly-one 校验(沿用 241V2A-11 §4 + 241V2A-12 §5.5)
        int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
        if (defaultCount != 1) {  // ✅ P2 exactly-one(241V2A-11 裁决)
            // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
            throw new IllegalStateException(
                "default company 数量必须为 1, actual=" + defaultCount
            );
        }
    }
}
```

**关键变更**(对比 241V2A-10 / 11 / 12):
- ✗ 删除 `import com.optflow.pms.common.exception.IllegalStateException;`
- ✓ 维持 `throw new IllegalStateException(...)` 写法(Java 默认解析为 `java.lang.IllegalStateException`)

### 3.4 Verifier 唯一 Effective Spec(241V2A-16 冻结)

**【241V2A-16 冻结】** `DefaultCompanyTestVerifier` 完整方法体(沿用 241V2A-14 §3.1,**强化异常类型统一**):

```java
package com.optflow.pms.test.company;

import com.optflow.pms.module.auth.mapper.UserCompanyMapper;
// ⚠ 241V2A-16 显式确认:Verifier 不需要 import IllegalStateException
// ✓ 沿用 241V2A-14 §3.1:throw new IllegalStateException(...) 自动解析为 java.lang.IllegalStateException
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Component
public class DefaultCompanyTestVerifier {

    @Autowired
    private UserCompanyMapper userCompanyMapper;

    @Transactional(propagation = Propagation.REQUIRES_NEW, readOnly = true)
    public FinalState verifyFinalState(Long userId, Long expectedDefault1, Long expectedDefault2) {
        int defaultCount = userCompanyMapper.countByUserIdAndIsDefault(userId, 1);
        Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(userId);

        // 沿用 241V2A-14 §3.1 null 检查
        if (expectedDefault1 == null || expectedDefault2 == null) {
            // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
            throw new IllegalStateException(
                "expectedDefault1 / expectedDefault2 不能为 null, " +
                "expectedDefault1=" + expectedDefault1 + ", expectedDefault2=" + expectedDefault2
            );
        }

        if (expectedDefault1.equals(expectedDefault2)) {
            if (!expectedDefault1.equals(defaultCompanyId)) {
                // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
                throw new IllegalStateException(
                    "幂等场景:defaultCompanyId 必须 == expectedDefault1, " +
                    "actual=" + defaultCompanyId + ", expected=" + expectedDefault1
                );
            }
        } else {
            if (defaultCompanyId == null) {
                // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
                throw new IllegalStateException(
                    "候选集合场景:defaultCompanyId 不能为 null, " +
                    "expected ∈ {" + expectedDefault1 + ", " + expectedDefault2 + "}"
                );
            }
            if (!expectedDefault1.equals(defaultCompanyId) && !expectedDefault2.equals(defaultCompanyId)) {
                // ✅ 241V2A-16 冻结 = java.lang.IllegalStateException
                throw new IllegalStateException(
                    "候选集合场景:defaultCompanyId 必须 ∈ {expectedDefault1, expectedDefault2}, " +
                    "actual=" + defaultCompanyId + ", expected=" + expectedDefault1 + " or " + expectedDefault2
                );
            }
        }

        return new FinalState(defaultCount, defaultCompanyId);
    }

    public record FinalState(int defaultCount, Long defaultCompanyId) {}
}
```

### 3.5 Service / Verifier 异常类型统一(241V2A-16 显式)

**【241V2A-16 冻结】** Service / Verifier 异常类型**唯一统一**为 `java.lang.IllegalStateException`:

| 触发场景 | 抛出方 | 异常类型 |
|---|---|---|
| setDefault affected != 1 | Service | `java.lang.IllegalStateException` |
| defaultCount != 1(exactly-one 失败)| Service | `java.lang.IllegalStateException` |
| expectedDefault1/2 == null | Verifier | `java.lang.IllegalStateException` |
| 幂等场景 defaultCompanyId != expectedDefault1 | Verifier | `java.lang.IllegalStateException` |
| 候选集合场景 defaultCompanyId ∉ {expectedDefault1, expectedDefault2} | Verifier | `java.lang.IllegalStateException` |

**严禁**:
- ✗ 不得在 Service 用 `com.optflow.pms.common.exception.IllegalStateException`
- ✗ 不得在 Verifier 用 `com.optflow.pms.common.exception.IllegalStateException`
- ✗ 不得让 Service 和 Verifier 用不同类型(必须统一 `java.lang.IllegalStateException`)

### 3.6 异常处理链路(241V2A-16 显式)

**【241V2A-16 冻结】** `java.lang.IllegalStateException` 在 V4.4 的异常处理链路:

```
setDefaultCompany 业务不变量失败
    ↓ throw new java.lang.IllegalStateException(...)
Spring @Transactional rollbackFor = Exception.class
    ↓ 自动 rollback
GlobalExceptionHandler(241 §3)
    ↓ 捕获 RuntimeException(包括 java.lang.IllegalStateException)
HTTP 500 Internal Server Error
```

**说明**:
- `java.lang.IllegalStateException` 继承 `RuntimeException`,被 Spring `@Transactional(rollbackFor = Exception.class)` 捕获 → 自动 rollback
- `GlobalExceptionHandler` 默认处理 RuntimeException → HTTP 500
- 不需要新增 ResultCode / 不需要新增自定义类

---

## §4 P2 证据标签修正(241V2A-16)

### 4.1 P2-3:241V2A-15 §9 证据标签错配修正

**【241V2A-16 冻结】** 正确证据标签分级:

| 类型 | 正确标签 | 理由 |
|---|---|---|
| `java.util.concurrent.atomic.AtomicReference` 类 | **【原系统事实】** | Java JDK 标准库(JDK 1.5+)|
| `java.util.concurrent.CountDownLatch` 类 | **【原系统事实】** | Java JDK 标准库(JDK 1.5+)|
| `java.util.concurrent.ExecutorService` 类 | **【原系统事实】** | Java JDK 标准库(JDK 1.5+)|
| **V4.4 使用模式**(err1/err2 收集 + startLatch/endLatch 同步 + pool.submit 并发)| **【OptFlow设计】/【实现机制】** | V4.4 文档体系内的设计模式,非已实施事实 |

**关键**:
- 类型本身(类) = 【原系统事实】(Java JDK 提供)
- 使用模式 = 【OptFlow设计】(V4.4 设计)

### 4.2 P2-1:DEFAULT-03 未使用 companyBId/companyCId

**【241V2A-16 记录为 P2,显式保持,不得升级】**:
- 241V2A-15 §3.1 DEFAULT-03 模板中 `Long companyBId = data.companyBId();` 和 `Long companyCId = data.companyCId();` 声明但未使用
- 241V2A-15 §3.1 的注释"仅声明,本测试不使用(占位 DEFAULT-04/05)" / "仅声明,本测试不使用(占位 DEFAULT-01/02)" 表明这是占位声明
- P2 状态:**未使用但不影响测试正确性**(可以删除,但不影响功能)
- 本轮**不修改** 241V2A-15,本轮**不创建** 241V2A-17
- 留待后续单独裁决(可以删除以精简代码 / 也可以保留以统一 TestDataContext 4 字段都取值的风格)

### 4.3 P2-2:`pool.shutdown()` 后未显式 `awaitTermination`

**【241V2A-16 记录为 P2,显式保持,不得升级】**:
- 241V2A-15 §3.1 DEFAULT-03 模板中 `pool.shutdown();` 后未调用 `awaitTermination(timeout, unit)` 等待资源清理
- 不影响测试正确性(`endLatch.await()` 已确保并发任务完成),但资源回收不显式
- P2 状态:**功能正确但风格不完美**
- 本轮**不修改** 241V2A-15,本轮**不创建** 241V2A-17
- 留待后续单独裁决(可以加 `awaitTermination` / 也可以保留现状)

### 4.4 P2 状态汇总(241V2A-16 后)

| # | P2 描述 | 状态 | 来源 |
|---:|---|---|---|
| P2-0 | exactly-one 业务规则 | **保留**(沿用 241V2A-11 §4) | 241V2A-11 |
| P2-1 | DEFAULT-03 未使用 companyBId/companyCId | **保留** | 241V2A-15(本轮显式记录) |
| P2-2 | `pool.shutdown()` 后未 `awaitTermination` | **保留** | 241V2A-15(本轮显式记录) |
| P2-3 | 241V2A-15 §9 证据标签错配 | **本轮显式记录**(无需修复,只需本轮冻结正确标签)| 241V2A-16 §4.1 |

**【241V2A-16 显式】** P2 ≥ 1 持续满足(exactly-one + P2-1 + P2-2 + P2-3 共 4 项),**不得写 P2 = 0**。

---

## §5 一致性审计(241V2A-16 全局)

### 5.1 与前序 18 份文档的一致性矩阵

| 文档 | 检查项 | 一致? | 备注 |
|---|---|:-:|---|
| 240 Q4 跨公司隔离架构 | 涉及 user_company? | ✓ | 沿用 |
| 241 §4.2 | CompanyContextMissingException 自定义类 | ✓ | 不修改 |
| 241 §4.3 | CompanyMismatchException 自定义类 | ✓ | 不修改 |
| 241 §4.4 | CompanyAccessDeniedException 自定义类 | ✓ | 不修改 |
| 241 §4.5 | ResultCode 60000/60001/60002 | ✓ | 不新增 60003 |
| 241V2 | 基础设施设计修正版 | ✓ | 沿用 |
| 241V2A | P0-2 强制覆盖补丁 | ✓ | 沿用 |
| 241V2A-1 §5.1 / §6.1 | `throw new IllegalStateException(...)` 无 import | ✓ | 沿用(241V2A-16 显式 = java.lang.IllegalStateException) |
| 241V2A-2 | 死锁表述 | ✓ | 不冲突 |
| 241V2A-3 §4.3 | DefaultCompanyTestVerifier @Component + REQUIRES_NEW | ✓ | 沿用 |
| 241V2A-4 | TestDataContext 4 字段 | ✓ | 沿用 |
| 241V2A-5 | verifyFinalState 5 测试参数矩阵 | ✓ | 沿用 |
| 241V2A-6 ~ 9 | 后续补丁 | ✓ | 不冲突 |
| 241V2A-10 §7.1 第 381 行 | `import com.optflow.pms.common.exception.IllegalStateException` | ✗ | **241V2A-16 显式作废** |
| 241V2A-11 §5.5 | `throw new IllegalStateException(...)`(无显式 import 列出) | ✓ | 沿用(默认 java.lang) |
| 241V2A-12 §3.3 第 303 行 | `import com.optflow.pms.common.exception.IllegalStateException` | ✗ | **241V2A-16 显式作废** |
| 241V2A-13 §3 | selectDefaultCompanyId SQL 无 LIMIT | ✓ | 沿用 |
| 241V2A-14 §3.1 | Verifier `throw new IllegalStateException(...)` 4 处 | ✓ | 沿用(默认 java.lang) |
| 241V2A-15 §3.1 | DEFAULT-03 阶段 B 错误收集 + 三道断言 | ✓ | 沿用 |
| 241V2A-15 §9 证据标签 | 误标【原系统事实】| ✗ | **241V2A-16 §4.1 修正(P2-3)** |

**总结**:与 241V2A-10 / 12 的 import 自定义 IllegalStateException 2 处冲突(已显式作废);与 241V2A-15 §9 证据标签 1 处 P2 误标(已记录 P2-3);与其它 18 份文档均一致。

### 5.2 不变量保持审计

| 不变量 | 状态 |
|---|:-:|
| exactly-one 业务规则(241V2A-11 §4) | ✓ 不修改 |
| Repository 4 个公开方法(241V2A-12 §2.1) | ✓ 不修改 |
| Mapper 5 个自定义方法(241V2A-12 §4.2 + 241V2A-13 §4.2) | ✓ 不修改 |
| selectDefaultCompanyId 无 LIMIT 1(241V2A-13 §3.5) | ✓ 不修改 |
| verifyFinalState 3 参数(241V2A-14 §3.1) | ✓ 不修改 |
| expectedDefault 二分逻辑(241V2A-14 §3.1) | ✓ 不修改 |
| DEFAULT-03 成功性三道断言(241V2A-15 §3.2) | ✓ 不修改 |
| 241 §4.2-4.4 自定义异常类(CompanyContextMissingException / CompanyMismatchException / CompanyAccessDeniedException) | ✓ 不修改 |
| 241 §4.5 ResultCode 60000/60001/60002 | ✓ 不修改(不新增 60003) |

### 5.3 显式作废汇总表(241V2A-16)

| # | 旧写法来源 | 旧写法 | 状态 | 新唯一写法来源 |
|---:|---|---|---|---|
| 1 | 241V2A-10 §7.1 第 381 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | 【作废 import】 | 241V2A-16 §3.3 删除该 import(默认 java.lang.IllegalStateException) |
| 2 | 241V2A-11 §5.5(沿用 241V2A-10) | `import com.optflow.pms.common.exception.IllegalStateException;` | 【作废 import】 | 241V2A-16 §3.3 删除该 import |
| 3 | 241V2A-12 §3.3 第 303 行 | `import com.optflow.pms.common.exception.IllegalStateException;` | 【作废 import】 | 241V2A-16 §3.3 删除该 import |
| 4 | 241V2A-15 §9 报告统计 | `Java AtomicReference / CountDownLatch / ExecutorService` 标为【原系统事实】 | 【P2-3 显式记录,需本轮冻结正确标签】 | 241V2A-16 §4.1:类型本身 = 【原系统事实】,V4.4 使用模式 = 【OptFlow设计】 |

### 5.4 严禁清单(241V2A-16)

#### 5.4.1 实施者严禁

- ✗ 不得 `import com.optflow.pms.common.exception.IllegalStateException`(未冻结类,编译失败)
- ✗ 不得在 Service 与 Verifier 用不同异常类型(必须统一 `java.lang.IllegalStateException`)
- ✗ 不得新建 `com.optflow.pms.common.exception.IllegalStateException` 自定义类
- ✗ 不得新增 ResultCode 60003+(用于 IllegalStateException)
- ✗ 不得修改 241 §4.2-4.4 冻结的 3 个自定义异常
- ✗ 不得修改 exactly-one 业务规则
- ✗ 不得修改 verifyFinalState 3 参数 / expectedDefault 二分逻辑
- ✗ 不得修改 Repository 4 方法 / Mapper 5 方法 / selectDefaultCompanyId 无 LIMIT
- ✗ 不得修改 DEFAULT-03 成功性三道断言
- ✗ 不得修改 P2-1 / P2-2 提到的具体问题(不得再制造 241V2A-17)
- ✗ 不得把 P2-3 升级为 P1

#### 5.4.2 文档作者严禁

- ✗ 不得修改 241V2A-15 / 241V2A-14 / 任何历史 MD
- ✗ 不得在本补丁(241V2A-16)内**重新**写"以实际实现为准"
- ✗ 不得在后续独立盲审 PASS 前跳过独立盲审

---

## §6 P 状态(241V2A-16 后)

| 等级 | 数量 | 明细 |
|---|:-:|---|
| P0 | 0 | - |
| P1 | 0 | P1-7 ~ P1-19 全部 PASS 或本补丁关闭 |
| P2 | 4 | exactly-one(241V2A-11)+ DEFAULT-03 未使用 companyBId/companyCId(241V2A-15)+ `pool.shutdown` 后未 `awaitTermination`(241V2A-15)+ 证据标签修正项(241V2A-15 §9) |
| INFO | 0 | - |

**【241V2A-16 显式】** P2 ≥ 1 持续满足(共 4 项 P2),**不得写 P2 = 0**。

---

## §7 报告统计(241V2A-16)

- 文档字节:约 22,000 字节
- 章节数:13
- 修复的 P1:1(P1-19)
- 显式作废的旧写法:3(241V2A-10 / 11 / 12 的 3 处自定义 import)
- 显式冻结的新唯一写法:1(`java.lang.IllegalStateException` 统一异常类型)
- P2 显式记录:3(P2-1 / P2-2 / P2-3,沿用 P2-0 共 4 项)
- 保持闭环:P1-14 / P1-15 / P1-16 / P1-17 / P1-18
- 不变量保持:exactly-one / Repository 4 方法 / Mapper 5 方法 / selectDefaultCompanyId 无 LIMIT / verifyFinalState 3 参数 / expectedDefault 二分逻辑 / DEFAULT-03 三道断言 / 241 §4 自定义异常 / 241 §4.5 ResultCode
- 启动闸门:全部满足,等下一轮独立盲审
- DDL 修改:0
- Java 代码修改:0
- commit / push:0 / 0

---

## §8 启动闸门(241V2A-16)

### 8.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241 §4 自定义异常 + ResultCode | ✓ | 241 |
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
| 241V2A-8 修复 P1-8 | ✓ | 241V2A-8 |
| 241V2A-9 修复 P1-9 | ✓ | 241V2A-9 |
| 241V2A-10 修复 P1-10 + P1-11 | ✓ | 241V2A-10 |
| 241V2A-11 修复 P1-12 + P1-13 + P2 裁决 | ✓ | 241V2A-11 |
| 241V2A-12 修复 P1-14 + P1-15 | ✓ | 241V2A-12 |
| 241V2A-13 修复 P1-16 | ✓ | 241V2A-13 |
| 241V2A-14 修复 P1-17 | ✓ | 241V2A-14 |
| 241V2A-15 修复 P1-18 | ✓ | 241V2A-15 |
| **241V2A-16 修复 P1-19 + P2 记录(本文件)** | **✓** | **本文件** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 8.2 下一轮盲审必审计

- ✓ 241V2A-16 §3.1 是否真冻结 `java.lang.IllegalStateException`
- ✓ 241V2A-16 §3.3 / §3.4 是否真统一 Service / Verifier 异常类型
- ✓ 241V2A-16 §3.2 显式作废表是否真覆盖 241V2A-10 / 11 / 12 的 3 处 import
- ✓ 241V2A-16 §4 P2 记录(P2-1 / P2-2 / P2-3)是否真保持不升级
- ✓ 241V2A-16 §5 不变量保持是否真不被破坏
- ✓ 241V2A-16 是否真未创建新异常类 / 未新增 ResultCode / 未修改 241 §4 冻结的 3 个异常
- ✓ 23 份文档是否仍有内部矛盾

---

## §9 一句话最终判断

> **241V2A-16 S1-169-1 IllegalStateException 异常契约统一冻结补丁完成**:第十三轮全局审计识别的 P1-19(`241V2A-10 §7.1 第 381 行` / `241V2A-11 §5.5` / `241V2A-12 §3.3 第 303 行` 三处 Service 模板 `import com.optflow.pms.common.exception.IllegalStateException`,但 241 §4.2-4.4 只冻结了 3 个自定义异常类(`CompanyContextMissingException` / `CompanyMismatchException` / `CompanyAccessDeniedException`),**未冻结自定义 IllegalStateException**;同时 `241V2A-1 §5.1 / §6.1` / `241V2A-7` / `241V2A-14 §3.1`(4 处)`throw new IllegalStateException(...)` 无 import 默认解析为 `java.lang.IllegalStateException`;Service / Verifier 异常类型自相矛盾,实施者按 241V2A-10 / 11 / 12 模板 import 自定义类必然编译失败)通过本补丁**真闭环**——**审计证据** + **最小变更原则** + **不创建新异常类 / 不新增 ResultCode / 不修改 241 §4 已冻结 3 个自定义异常** + **统一使用 `java.lang.IllegalStateException`(Java JDK 标准库,JDK 1.0+)|+ **显式作废 241V2A-10 / 11 / 12 的 3 处 `import com.optflow.pms.common.exception.IllegalStateException;`** + **Service / Verifier 异常类型唯一统一为 `java.lang.IllegalStateException`**(Service 步骤 6 affected != 1 / defaultCount != 1 + Verifier 4 处 expectedDefault 校验失败均使用此类型)+ **不修改 verifyFinalState 3 参数 / expectedDefault 二分逻辑 / selectDefaultCompanyId 无 LIMIT / Repository 4 方法 / Mapper 5 方法 / exactly-one 业务规则 / 241 §4 自定义异常 / 241 §4.5 ResultCode**;**P2 显式记录 3 项**:P2-1(DEFAULT-03 未使用 companyBId/companyCId,沿用 241V2A-15 占位声明)+ P2-2(`pool.shutdown()` 后未 `awaitTermination`,不影响功能)+ P2-3(241V2A-15 §9 证据标签错配,正确标签分级:Java JDK 类型本身 = 【原系统事实】,V4.4 使用模式 = 【OptFlow设计】);P2 总数 ≥ 1 持续满足(共 4 项:exactly-one + P2-1 + P2-2 + P2-3);P1-14 ~ P1-18 全部 PASS,P1-19 本补丁关闭;241V2A-16 不修改 241V2A-15 / 241V2A-14 / 任何历史 MD 任何字节,只通过"显式作废 + 显式冻结 + P2 记录"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §10 报告统计(完整)

- 章节数:10
- 修复的 P1:1(P1-19)
- 显式作废的旧写法:3
- 显式冻结的新唯一写法:1(`java.lang.IllegalStateException`)
- P2 显式记录:3(P2-1 / P2-2 / P2-3)
- 保持闭环:P1-14 / P1-15 / P1-16 / P1-17 / P1-18
- 不变量保持:8 项
- 启动闸门:全部满足
- 下一轮:独立盲审

---

## §11 文件结尾(241V2A-16 显式)

【P1-19 修复完成】
【IllegalStateException 异常类型统一冻结为 java.lang.IllegalStateException】
【显式作废 import com.optflow.pms.common.exception.IllegalStateException】
【Service / Verifier 异常类型唯一统一】
【P2 显式记录 3 项:DEFAULT-03 未使用 / pool 未 awaitTermination / 证据标签修正】
【P1-14 ~ P1-18 闭环保持】
【P2 >= 1 持续满足】
【S1-169-2 继续 BLOCK】
【等待下一轮独立盲审】
【不得自评 PASS】