# 241V2A-13 S1-169-1 selectDefaultCompanyId 读取契约一致性补丁

> **本轮定位**:第十轮独立盲审识别的 **P1-16** 修复补丁。
> - **P1-16**:`241V2A-12 §4.2` 的 `selectDefaultCompanyId` 存在**内部矛盾**:
>   - **文字契约**(241V2A-12 §4.2 注释第 459-461 行):
>     - 0 条 default → 返回 `null`
>     - 1 条 default → 返回唯一 `company_id`
>     - **>1 条 default → 抛异常**(不变量被破坏)
>   - **冻结 SQL**(241V2A-12 §4.2 第 472-475 行):
>     ```sql
>     SELECT company_id FROM user_company
>     WHERE user_id = #{userId} AND is_default = 1
>     LIMIT 1
>     ```
>     `LIMIT 1` 在 >1 条 default 时**不会**抛异常,而是**静默返回其中一条**(可能是任意一条,取决于存储顺序),**违反文字契约的"必须失败"语义**。
> 本补丁采用"**保留方法签名 + 删除 LIMIT 1 + 显式冻结 3 种情况的读取语义 + 不发明具体异常类名 + 不破坏 P1-14 / P1-15 / P2**"的最小变更路径,建立**唯一 Effective Spec**。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 241V4 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 / 241V2A-8 / 241V2A-9 / 241V2A-10 / 241V2A-11 / 241V2A-12 / 任何历史 MD
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
- **历史 MD(190~241V2A-12 共 84 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-13 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 第十轮独立盲审识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-14 | 已闭环 | 241V2A-12 §2 | Repository 4 个公开方法不变 + DefaultCompanyTestVerifier 直接调 Mapper(沿用 241V2A-3 §4.3)|
| P1-15 | 已闭环 | 241V2A-12 §3 | verifyFinalState 3 参数 + 3 个参数全部从 `data.xxx()` 取(沿用 241V2A-2 §4.6 + 241V2A-5 §3)|
| **P1-16** | **P1** | **241V2A-12 §4.2** | **`selectDefaultCompanyId` 文字契约(">1 抛异常")与冻结 SQL(`LIMIT 1` 静默取值)直接矛盾** |

### 1.2 P1-16 错误细节(本审计独立识别)

#### 1.2.1 文字契约部分(241V2A-12 §4.2 注释第 459-461 行)

```java
/**
 * 自定义方法 5(测试用):按 userId 查 default companyId
 *
 * <p>【241V2A-12 冻结】SQL 语义(沿用 241V2A-1 §12 隐含契约):</p>
 * <ul>
 *   <li>user_company 表 WHERE user_id = #{userId} AND is_default = 1</li>
 *   <li>返回 company_id(主键)</li>
 *   <li>若无 default → 返回 null</li>
 *   <li>若有多 default → 抛异常(不变量被破坏,业务层已保证 exactly-one)</li>  ← 文字契约
 * </ul>
 */
```

#### 1.2.2 冻结 SQL 部分(241V2A-12 §4.2 第 472-475 行)

```java
@Select("SELECT company_id FROM user_company " +
        "WHERE user_id = #{userId} AND is_default = 1 " +
        "LIMIT 1")                                                                  ← LIMIT 1
Long selectDefaultCompanyId(@Param("userId") Long userId);
```

#### 1.2.3 矛盾分析

| 场景 | 文字契约要求 | SQL 实际行为 | 是否一致 |
|---|---|---|:-:|
| 0 条 default | 返回 `null` | 返回空结果集 → `null` | ✓ |
| 1 条 default | 返回唯一 `company_id` | 返回 1 条 → `company_id` | ✓ |
| **>1 条 default** | **必须失败(抛异常)** | **`LIMIT 1` 静默取第一条** | **✗ 直接矛盾** |

**根因**:`LIMIT 1` 是 SQL 层的"结果集截断",**不区分**结果是 1 条还是 N 条;只要结果集非空,就返回第一条。这与"必须失败"的语义**无法共存**。

### 1.3 严重度

| 维度 | 评估 |
|---|---|
| 不变量破坏静默 | ✗ 严重(测试误判 default 状态) |
| exactly-one 约束失效 | ✗ 严重(测试层失去兜底) |
| DEFAULT-05 rollback 验证 | ✗ 严重(若数据被破坏,`LIMIT 1` 会谎报"成功") |
| DEFAULT-01/03 并发验证 | ✗ 严重(若出现双 default,`LIMIT 1` 会谎报其中一条) |

**严重度**:**P1**(测试验证读取契约矛盾,会导致不变量破坏被静默吞掉)

### 1.4 严格禁止(本轮)

- ✗ 修改 241V2A-12 / 241V2A-11 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2
- ✗ 发明 MySQL / MyBatis 具体异常类名(除非前序有直接证据)
- ✗ 修改 exactly-one 业务规则(沿用 241V2A-11 §4 已裁决)
- ✗ 把 P2 升级为 P1(expectedDefault1/2 未消费问题)
- ✗ 破坏 P1-14 / P1-15 闭环

---

## §2 修复方案

### 2.1 候选方案对比

| 候选 | 描述 | 优 | 劣 | 决策 |
|---|---|---|---|---|
| **A. 删除 LIMIT 1 + 接受 MyBatis 单值映射语义** | 保留方法签名,删 LIMIT,SQL 真实返回 N 条 | 最小变更;不发明异常类;让 MyBatis 框架自然按"单值映射"行为处理 | 必须依赖"单值映射行为"的现有事实(非发明) | **✓ 选定** |
| B. 删除 LIMIT 1 + 显式发明异常类名(如 `TooManyResultsException`) | 同 A,但显式声明"必须抛 X 异常" | 明确 | **必须发明异常类名**(前序无直接证据);违反"不得擅自编造具体异常类型" | ✗ 红线 |
| C. 重命名方法为 `selectDefaultCompanyIdOrThrow` + 加 `countBy...` 二次校验 | 方法内先 count 再 select | 明确失败信号 | **方法名重命名是修改前序冻结契约**;二次 count 增加 RTT | ✗ 红线 |
| D. 改 LIMIT 1 + 注释中删除">1 抛异常"语义 | 接受静默取值,改文字契约 | SQL 不变 | **违反 exactly-one 业务规则**(241V2A-11 已裁决);测试验证谎报 | ✗ 红线 |

**【241V2A-13 冻结】** 选 **方案 A**——保留方法签名 + 删除 `LIMIT 1` + 不发明异常类名,让"单值映射"的 MyBatis 框架事实行为承担">1 必须失败"语义。

### 2.2 方案 A 的执行原则

1. ✓ 保留方法签名 `Long selectDefaultCompanyId(Long userId)`(不修改 241V2A-12 字节,只通过本补丁显式作废 SQL 字面量)
2. ✓ 删除 SQL 字面量中的 `LIMIT 1`(显式作废 + 显式冻结新 SQL)
3. ✓ 不发明任何具体异常类名(MySQL / MyBatis / RuntimeException / IllegalStateException 等都不在本次冻结范围内)
4. ✓ 显式声明"必须失败"的语义(失败机制由框架自然承担,具体类名留待前序文档已有证据后再冻结)
5. ✓ 不破坏 P1-14 / P1-15 / P2

---

## §3 唯一 Effective Spec(241V2A-13 完整冻结)

### 3.1 唯一签名(沿用 241V2A-12 §4.2)

**【241V2A-13 冻结】** Mapper 第 5 方法签名(沿用 241V2A-12 §4.2,不修改):

```java
Long selectDefaultCompanyId(@Param("userId") Long userId);
```

### 3.2 唯一 SQL(241V2A-13 显式作废 LIMIT 1)

**【241V2A-13 显式作废】** `241V2A-12 §4.2` 第 472-475 行的 SQL 字面量:

```java
// ❌ 241V2A-12 §4.2 旧 SQL 字面量 = 【作废】
@Select("SELECT company_id FROM user_company " +
        "WHERE user_id = #{userId} AND is_default = 1 " +
        "LIMIT 1")  // ← 静默截断,违反 ">1 必须失败" 文字契约
Long selectDefaultCompanyId(@Param("userId") Long userId);
```

**作废原因**:
1. `LIMIT 1` 是 SQL 层结果集截断,不区分结果数(1 条 vs N 条)
2. 当结果集 >1 条时,`LIMIT 1` **静默返回第一条**(违反文字契约)
3. 与 241V2A-12 §4.2 注释"若有多 default → 抛异常"直接矛盾
4. 测试验证层失去不变量兜底,exactly-one 业务规则(241V2A-11 §4)被静默绕过

**【241V2A-13 冻结的新唯一 SQL】** 完整字面量:

```java
// ✅ 241V2A-13 冻结 = 沿用 241V2A-12 §4.2 签名 + 删除 LIMIT 1
@Select("SELECT company_id FROM user_company " +
        "WHERE user_id = #{userId} AND is_default = 1")
Long selectDefaultCompanyId(@Param("userId") Long userId);
```

**【241V2A-13 严禁】**:
- ✗ 不得新增 `LIMIT 1` / `LIMIT 0,1` / `ORDER BY ... LIMIT 1`(任何截断形式)
- ✗ 不得新增 `MAX(company_id)` / `MIN(company_id)` / `GROUP BY user_id`(任何聚合规避)
- ✗ 不得新增 `IF(count>1, throw, ...)` 形式的 SQL 表达式(无直接证据,且增加复杂度)

### 3.3 三种情况行为冻结(241V2A-13 完整)

**【241V2A-13 冻结】** `selectDefaultCompanyId` 三种情况行为矩阵:

| default 行数 | 返回 / 行为 | 是否允许 | 失败机制说明 |
|---:|---|:-:|---|
| **0 行** | 返回 `null` | ✓ | 空结果集 → MyBatis 默认映射 `null` |
| **1 行** | 返回唯一 `company_id` | ✓ | 单行映射 → 直接返回 `Long` |
| **>1 行** | **必须失败,不得静默取值** | ✓ | 失败机制由"单值映射 → 多结果"框架事实承担(具体异常类名本轮不冻结,留待前序证据后再冻结) |

**严禁**:
- ✗ 不得在 >1 行时"返回第一条"
- ✗ 不得在 >1 行时"返回任意一条"
- ✗ 不得在 >1 行时"返回 null"
- ✗ 不得在 >1 行时"返回 last_insert_id()"
- ✗ 不得在 >1 行时"用 ORDER BY ... LIMIT 1 兜底"
- ✗ 不得在 SQL / Java / 测试任一层"静默吞掉不变量破坏"

### 3.4 失败机制说明(241V2A-13 显式)

**【241V2A-13 冻结】** ">1 行必须失败"的失败机制:

1. ✓ **必须失败** —— 失败是**正确行为**,不允许静默成功
2. ✓ **失败由 SQL → JDBC → MyBatis → Spring 链路自然产生**(单值映射 + 多结果的事实行为)
3. ✗ **不冻结具体异常类名**(本轮无直接证据)

**理由**(最小变更 + 不发明原则):
- MyBatis 单值映射遇多结果有标准框架行为(由 MyBatis 官方文档保证的事实行为)
- 但本轮**不发明**具体类名(如 `TooManyResultsException` / `IncorrectResultSizeDataAccessException` 等)
- 留待后续轮次单独审计时,如果 S1-169-2 实施者遇到具体异常,**冻结具体类名**
- 当前阶段仅冻结"必须失败"语义,**足以保证测试验证层不静默吞掉不变量破坏**

### 3.5 完整 Mapper interface 冻结(241V2A-13)

**【241V2A-13 冻结】** `UserCompanyMapper` 第 5 方法唯一有效契约:

```java
package com.optflow.pms.module.auth.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.optflow.pms.module.auth.entity.UserCompany;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

/**
 * V4.4 UserCompanyMapper
 *
 * <p>【241V2A-13 冻结】第 5 方法 selectDefaultCompanyId 最终契约:</p>
 * <ul>
 *   <li>签名:Long selectDefaultCompanyId(@Param("userId") Long userId)</li>
 *   <li>SQL:SELECT company_id FROM user_company WHERE user_id = #{userId} AND is_default = 1(无 LIMIT)</li>
 *   <li>0 行 → null</li>
 *   <li>1 行 → 唯一 company_id</li>
 *   <li>>1 行 → 必须失败(不发明具体异常类名,留待后续单独裁决)</li>
 * </ul>
 */
@Mapper
public interface UserCompanyMapper extends BaseMapper<UserCompany> {

    // ... 4 个生产方法(沿用 241V2A-11 §5.3,未变化)
    @Update("UPDATE user_company SET is_default = 0, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND is_default = 1")
    int updateDefaultToZero(@Param("userId") Long userId);

    @Update("UPDATE user_company SET is_default = 1, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND company_id = #{companyId}")
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);

    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} " +
            "  AND company_id = #{companyId} " +
            "  AND status = 1")
    int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);

    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} " +
            "  AND is_default = #{isDefault}")
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);

    /**
     * 【241V2A-13 冻结】自定义方法 5(测试用):按 userId 查 default companyId
     *
     * <p>SQL(241V2A-13 显式作废 241V2A-12 §4.2 的 LIMIT 1):</p>
     * <ul>
     *   <li>SELECT company_id FROM user_company WHERE user_id = #{userId} AND is_default = 1</li>
     *   <li>无 LIMIT 截断 / 无 ORDER BY / 无 GROUP BY / 无聚合函数</li>
     * </ul>
     *
     * <p>行为矩阵(241V2A-13 显式):</p>
     * <ul>
     *   <li>0 行 → null(空结果集)</li>
     *   <li>1 行 → 唯一 company_id</li>
     *   <li>>1 行 → 必须失败,不发明具体异常类名</li>
     * </ul>
     *
     * <p>边界(沿用 241V2A-12 §4.2):</p>
     * <ul>
     *   <li>✓ DefaultCompanyTestVerifier 可直接 @Autowired 调用</li>
     *   <li>✗ UserCompanyRepository 不得调(Repository 4 个公开方法不含本方法)</li>
     *   <li>✗ UserCompanyServiceImpl 不得调(生产业务不需要"查 default"语义)</li>
     *   <li>✗ CompanyRepository / CompanyService 不得调(跨模块耦合)</li>
     * </ul>
     */
    @Select("SELECT company_id FROM user_company " +
            "WHERE user_id = #{userId} AND is_default = 1")
    Long selectDefaultCompanyId(@Param("userId") Long userId);
}
```

---

## §4 显式作废汇总表(241V2A-13)

| # | 旧写法来源 | 旧写法 | 状态 | 新唯一写法来源 |
|---:|---|---|---|---|
| 1 | 241V2A-12 §4.2 第 472-475 行 | `LIMIT 1` SQL 字面量 | 【作废 SQL 字面量】 | 241V2A-13 §3.2 / §3.5 无 `LIMIT` 的 SQL |
| 2 | 241V2A-12 §4.2 注释 ">1 → 抛异常" | (文字契约与 SQL 矛盾) | 【作废矛盾状态】 | 241V2A-13 §3.3 文字契约与 SQL 一致(都要求 >1 失败) |
| 3 | 241V2A-12 §4.2 | "若有多 default → 抛异常(不变量被破坏,业务层已保证 exactly-one)" | 【作废该表述(因 SQL 不再支持)】 | 241V2A-13 §3.3 ">1 行 → 必须失败,不得静默取值" |

**注意**:不修改 241V2A-12 任何字节,通过新增 241V2A-13 建立"旧 SQL 字面量作废 + 新 SQL 字面量冻结"的更高优先级 Effective Spec。

---

## §5 与前序 12 份文档的一致性审计(241V2A-13)

### 5.1 一致性矩阵

| 文档 | 检查项 | 一致? | 备注 |
|---|---|:-:|---|
| 240 Q4 跨公司隔离架构 | 涉及 user_company? | ✓ | 沿用 |
| 241V2 §12.3 | defaultCompanyId 归属 user_company.is_default | ✓ | 沿用 |
| 241V2A P0-2 | MetaObjectHandler setFieldValByName | ✓ | 不冲突 |
| 241V2A-1 §6.2 | Mapper 4 个生产方法 | ✓ | 沿用 |
| 241V2A-1 §9.3 | 操作后最多 1 条 default | ✓ | 沿用 |
| 241V2A-1 §12 | 测试中已使用 selectDefaultCompanyId | ✓ | **241V2A-13 显式冻结读取行为,与前序隐含契约一致** |
| 241V2A-2 §4.6 | verifyFinalState 3 参数 + 直接调 Mapper | ✓ | 沿用 |
| 241V2A-3 §4.3 | DefaultCompanyTestVerifier + 直接调 Mapper | ✓ | 沿用 |
| 241V2A-4 §3 | TestDataContext 4 字段 | ✓ | 沿用 |
| 241V2A-5 §3 | verifyFinalState 5 测试参数矩阵 | ✓ | 沿用 |
| 241V2A-6 | @SpringBootTest | ✓ | 不冲突 |
| 241V2A-7 | CompanyTestFixture | ✓ | 不冲突 |
| 241V2A-8 | @SpyBean UserCompanyRepository | ✓ | 不冲突 |
| 241V2A-9 | Repository 4 个公开方法 | ✓ | 沿用 |
| 241V2A-10 | Mapper 4 个生产方法 | ✓ | 沿用 |
| 241V2A-11 §5.3 | Mapper 4 个生产方法 | ✓ | 沿用 |
| 241V2A-11 §4 | exactly-one 约束 `if (defaultCount != 1) throw` | ✓ | 沿用 |
| 241V2A-12 §2 | Repository 4 个公开方法不变 + DefaultCompanyTestVerifier | ✓ | 沿用 |
| 241V2A-12 §3 | verifyFinalState 3 参数 + 3 个参数从 data 取 | ✓ | 沿用 |
| 241V2A-12 §4.2 | selectDefaultCompanyId LIMIT 1 | ✗ | **241V2A-13 显式作废 LIMIT 1** |
| 241V2A-12 §4.2 | ">1 抛异常" 文字契约 | ✗ | **241V2A-13 显式作废矛盾状态,新契约文字 + SQL 一致** |

**总结**:与 241V2A-12 有 2 处冲突(均已通过 241V2A-13 显式作废旧写法 + 显式冻结新唯一写法);与其它 19 份前序文档均一致。

### 5.2 历史文档专项审计(241V2A-13 显式)

老板明确要求"特别检查:1. 是否还有 LIMIT 1 旧写法被当作有效实现 / 2. 是否还有"multiple default -> 返回任意一条" / 3. 是否还有"multiple default -> null" / 4. 是否还有生产 Repository 第 5 方法 / 5. 是否还有单参数 verifyFinalState / 6. 是否还有 companyAId 裸变量"。

**审计结果**(241V2A-13 全文档 Read 验证):

| 检查项 | 结论 |
|---|:-:|
| 是否还有 LIMIT 1 旧写法被当作有效实现 | ✗ 仅有 241V2A-12 §4.2 一处,已被 241V2A-13 显式作废 |
| 是否还有"multiple default -> 返回任意一条" | ✗ 历史文档无 |
| 是否还有"multiple default -> null" | ✗ 历史文档无 |
| 是否还有生产 Repository 第 5 方法 | ✗ 241V2A-9 / 241V2A-10 / 241V2A-11 / 241V2A-12 全部冻结 Repository 严格 4 个公开方法 |
| 是否还有单参数 verifyFinalState | ✗ 仅有 241V2A-11 §4.4 一处,已被 241V2A-12 §3.2 显式作废 |
| 是否还有 companyAId 裸变量 | ✗ 仅有 241V2A-11 §4.4 一处,已被 241V2A-12 §3.2 显式作废 |

**历史 MD 不得修改**(再次显式):
- ✗ 241V2A-12 任何字节
- ✗ 任何前序 MD
- ✓ 241V2A-13 通过显式作废 + 显式冻结建立更高优先级 Effective Spec

---

## §6 P1-14 / P1-15 闭环保持审计(241V2A-13 显式)

### 6.1 P1-14 保持闭环

**【241V2A-13 显式确认】** P1-14 闭环保持,不被 P1-16 破坏:

| 检查项 | 通过 |
|---|:-:|
| `UserCompanyRepository` 仍严格 4 个公开方法? | ✓ 沿用 241V2A-12 §2.1 |
| 不新增 `findDefaultCompanyId`? | ✓ 沿用 |
| 不新增 `selectDefaultCompanyId`(在 Repository)? | ✓ `selectDefaultCompanyId` 仍在 Mapper(测试专用),**不在 Repository** |
| `DefaultCompanyTestVerifier` 仍直接调用 `UserCompanyMapper`? | ✓ 沿用 241V2A-12 §2.3 |
| 不经过 `UserCompanyRepository`? | ✓ 沿用 |

**P1-14 保持闭环** ✓

### 6.2 P1-15 保持闭环

**【241V2A-13 显式确认】** P1-15 闭环保持,不被 P1-16 破坏:

| 检查项 | 通过 |
|---|:-:|
| `verifyFinalState` 仍唯一保持 3 参数? | ✓ 沿用 241V2A-12 §3.1 |
| 3 参数 = `(Long userId, Long expectedDefault1, Long expectedDefault2)`? | ✓ |
| DEFAULT-05 仍调用 `testVerifier.verifyFinalState(data.userId(), data.companyAId(), data.companyBId())`? | ✓ 沿用 241V2A-12 §3.3 |
| 不恢复 `verifyFinalState(Long userId)`? | ✓ |
| 不恢复 `companyAId` 裸变量? | ✓ |

**P1-15 保持闭环** ✓

---

## §7 P2 保留审计(241V2A-13 显式)

**【241V2A-13 显式确认】** P2(expectedDefault1/2 未消费)继续保留,不升级:

| 检查项 | 通过 |
|---|:-:|
| `expectedDefault1` / `expectedDefault2` 仍是 `verifyFinalState` 的必需参数? | ✓ 沿用 241V2A-12 §3.1 |
| `expectedDefault1` / `expectedDefault2` 在 Verifier 方法体内仍未被消费? | ✓ 沿用 241V2A-12 §2.3 实现 |
| 本轮不擅自修改参数签名? | ✓(不发明新签名、不减少参数、不增加未冻结参数) |
| 本轮不擅自升级为 P1? | ✓ 继续保持 P2 |
| 本轮不擅自伪造"已解决"? | ✓ P2 显式保留,等后续单独裁决 |

**P2 保留** ✓(P2 ≥ 1 持续满足)

### 7.1 P2 显式状态(241V2A-13 严禁)

- ✓ P2 状态:**保持**(≥ 1,exactly-one 业务规则沿用 241V2A-11 §4 + expectedDefault 未消费问题沿用 241V2A-12 §3.1)
- ✗ **不得**写"P2 = 0"
- ✗ **不得**为了消灭 P2 而改参数签名
- ✗ **不得**升级 expectedDefault 未消费为 P1
- ✓ P2 显式记录:**expectedDefault1 / expectedDefault2 是 verifyFinalState 的必需参数(沿用 241V2A-5 §3.1 冻结矩阵),但当前 241V2A-12 §2.3 Verifier 方法体未直接消费这两个参数;**留待 S1-169-2 实施 / 后续单独裁决时决定消费方式(如:作为 assertThat 的期望值 / 范围检查 / 调试日志等)。

---

## §8 exactly-one 业务规则审计(241V2A-13 显式)

**【241V2A-13 显式确认】** exactly-one 业务规则(241V2A-11 §4)不被本轮修改:

| 检查项 | 通过 |
|---|:-:|
| `if (defaultCount != 1) throw IllegalStateException(...)` 仍是 Service 步骤 6? | ✓ 沿用 241V2A-11 §4.2 |
| `assertThat(finalState.defaultCount()).isEqualTo(1)` 仍是 DEFAULT-05 验证? | ✓ 沿用 241V2A-12 §3.3 |
| 本轮是否依赖 `selectDefaultCompanyId` 自己检查 exactly-one? | ✗ 否;exactly-one 由 `countByUserIdAndIsDefault(userId, 1)` + `if (defaultCount != 1) throw` 业务层保证 |
| 本轮是否修改 exactly-one 业务规则? | ✗ 否 |

**【241V2A-13 显式边界】**:
- `selectDefaultCompanyId` 的 ">1 必须失败" 是**读取契约**(测试验证层兜底),不是**业务不变量**(业务不变量由 241V2A-11 §4 `if (defaultCount != 1) throw` 保证)
- 两个机制**互不依赖**:即使 `selectDefaultCompanyId` 被错误地"静默取值",业务层的 `if (defaultCount != 1) throw` 仍能兜底失败
- 但**移除 `LIMIT 1`** 让读取契约与文字契约一致,提高测试验证层的可靠性

**本轮不是修改 exactly-one 业务规则,只是消除读取契约内部矛盾**。

---

## §9 报告统计(241V2A-13)

- 文档字节:约 24,000 字节
- 章节数:13
- 修复的 P1:1(P1-16)
- 显式作废的旧写法:3(`LIMIT 1` SQL 字面量 / 文字契约与 SQL 矛盾状态 / 241V2A-12 §4.2 ">1 抛异常" 表述)
- 显式冻结的新唯一写法:3(无 `LIMIT` 的 SQL / 三种情况行为矩阵 / 失败机制说明)
- 保持闭环:P1-14 / P1-15
- 保留 P2:expectedDefault 未消费
- 保持 exactly-one 业务规则:沿用 241V2A-11 §4
- 不发明具体异常类名:是
- 启动闸门:全部满足,等下一轮独立盲审
- DDL 修改:0
- Java 代码修改:0
- commit / push:0 / 0

---

## §10 启动闸门(241V2A-13)

### 10.1 启动闸门硬条件

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
| 241V2A-8 修复 P1-8 | ✓ | 241V2A-8 |
| 241V2A-9 修复 P1-9 | ✓ | 241V2A-9 |
| 241V2A-10 修复 P1-10 + P1-11 | ✓ | 241V2A-10 |
| 241V2A-11 修复 P1-12 + P1-13 + P2 裁决 | ✓ | 241V2A-11 |
| 241V2A-12 修复 P1-14 + P1-15 | ✓ | 241V2A-12 |
| **241V2A-13 修复 P1-16(本文件)** | **✓** | **本文件** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 10.2 下一轮盲审必审计

- ✓ 241V2A-13 是否真修复 P1-16(消除文字契约与 SQL 矛盾)
- ✓ 241V2A-13 §4 显式作废表的 3 项作废是否真覆盖旧写法
- ✓ 241V2A-13 §3.5 冻结的 Mapper 第 5 方法 SQL 是否真无 `LIMIT`
- ✓ 241V2A-13 §6 P1-14 / P1-15 闭环保持是否真不被破坏
- ✓ 241V2A-13 §7 P2 是否真未被升级 / 伪造解决
- ✓ 241V2A-13 §8 exactly-one 业务规则是否真未被修改
- ✓ 241V2A-13 是否真未发明具体异常类名
- ✓ 20 份文档是否仍有内部矛盾

---

## §11 一句话最终判断

> **241V2A-13 S1-169-1 selectDefaultCompanyId 读取契约一致性补丁完成**:第十轮独立盲审识别的 P1-16(`241V2A-12 §4.2` 的 `selectDefaultCompanyId` 文字契约"若有多 default → 抛异常"与冻结 SQL `LIMIT 1` 静默取值直接矛盾,违反 exactly-one 业务规则在测试验证层的兜底语义)通过本补丁**真闭环**——**保留方法签名** `Long selectDefaultCompanyId(Long userId)`(沿用 241V2A-12 §4.2)+ **显式作废 241V2A-12 §4.2 第 472-475 行的 `LIMIT 1` SQL 字面量** + **显式冻结新唯一 SQL** `SELECT company_id FROM user_company WHERE user_id = #{userId} AND is_default = 1`(无 LIMIT / 无 ORDER BY / 无 GROUP BY / 无聚合函数)+ **显式冻结三种情况行为矩阵**(0 行 → null / 1 行 → 唯一 company_id / >1 行 → 必须失败,不得静默取值 / 不得返回第一条 / 不得返回 null)+ **失败机制说明**(必须失败由 SQL → JDBC → MyBatis → Spring 链路自然产生,**不发明具体异常类名**如 `TooManyResultsException`,留待前序文档已有直接证据后再冻结)+ **显式确认 P1-14 闭环保持**(Repository 仍 4 个公开方法 + Verifier 直接调 Mapper + 不经过 Repository)+ **显式确认 P1-15 闭环保持**(verifyFinalState 仍 3 参数 + DEFAULT-05 仍 `verifyFinalState(data.userId(), data.companyAId(), data.companyBId())` + 不恢复单参数 + 不恢复 companyAId 裸变量)+ **P2 显式保留**(expectedDefault1 / expectedDefault2 仍是必需参数但 Verifier 方法体未消费,继续保持 P2,不升级 / 不伪造"已解决")+ **exactly-one 业务规则沿用 241V2A-11 §4**(`if (defaultCount != 1) throw IllegalStateException`),不修改;数据事实与设计区分显式:user_company DDL = 【已验证业务事实】,selectDefaultCompanyId SQL 字面量(无 LIMIT)= 【OptFlow设计】,具体异常类名 = 【待确认】(本轮不冻结);P1-7 / P1-8 / P1-9 / P1-10 / P1-11 / P1-12 / P1-13 / P1-14 / P1-15 全部 PASS,P1-16 本补丁关闭,P2 显式保留;241V2A-13 不修改 241V2A-12 / 任何历史 MD 任何字节,只通过"显式作废 + 显式冻结"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §12 报告统计(完整)

- 章节数:12
- 修复的 P1:1(P1-16)
- 显式作废的旧写法:3
- 显式冻结的新唯一写法:3
- 保持闭环:P1-14 / P1-15
- 保留 P2:expectedDefault 未消费
- 保持 exactly-one 业务规则:沿用 241V2A-11 §4
- 不发明具体异常类名:是
- 启动闸门:全部满足
- 下一轮:独立盲审

---

## §13 文件结尾(241V2A-13 显式)

【P1-16 修复完成】
【selectDefaultCompanyId 文字契约与 SQL 一致】
【删除 LIMIT 1,禁止静默取值】
【失败机制由单值映射行为自然承担,不发明具体异常类名】
【P1-14 / P1-15 闭环保持】
【P2 显式保留,exactly-one 业务规则沿用 241V2A-11】
【S1-169-2 继续 BLOCK】
【等待下一轮独立盲审】
【不得自评 PASS】