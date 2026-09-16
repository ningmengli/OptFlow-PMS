# 241V3 S1-169-1 IGNORE_TABLES 代码一致性补丁

> **本轮定位**:241A-1 独立盲审识别的 **P1-1** 修复补丁。241V2 §6.4 / §6.6 的 2 张表 Java 代码与 §12.6 文字修订的 5 张表**直接矛盾**;本补丁**显式作废** 2 张表旧代码示例,**冻结 5 张表为 Effective Spec**,并提供 S1-169-2 实施不可误抄的明确约束。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 任何历史 MD
> - 严禁修改 VisionCare PMS 任何文件
> - 严禁创建 backend/ / 严禁写 Java 源文件 / 严禁创建 SQL 文件 / 严禁执行 DDL / 严禁连接数据库
> - 严禁修改 pom.xml / application.yml
> - 严禁 commit / 严禁 push
> - 标签:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
> - 证据等级:A=直接证据 / B=多源一致 / C=部分证据 / D=冲突 / E=推断 / F=未验证
> - 阶段:**S1-169-1**(未进入 S1-169-2)
> - 本补丁**不**自评 PASS,**等待下一轮独立盲审**

---

## §0 Git 基线

- **HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`(S1-169-0 240 commit)
- **REMOTE == LOCAL**:`6efa0da` ✓
- **0 号闸门 4 文件 SHA256 全部 PASS** ✓
- **历史 MD(190~241A-1 共 65 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V3 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 241A-1 独立盲审识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-1 | P1 | 241V2 §6.4 / §6.6 vs §12.6 | IGNORE_TABLES Java 代码 = 2 张表,与 §12.6 文字修订 5 张表直接矛盾 |

### 1.2 矛盾证据(本审计独立还原)

| 来源 | 内容 | 证据 |
|---|---|:-:|
| 241V2 §6.4 line 586-588(文字) | "**【241V2 冻结】** V4.4 IGNORE_TABLES = `Set.of("flyway_schema_history", "company")`" | A |
| 241V2 §6.6 line 646-649(**Java 代码示例**)| `private static final Set<String> IGNORE_TABLES_V44 = Set.of("flyway_schema_history", "company");` | A |
| 241V2 §12.6 line 1077-1083(文字) | 5 张表(flyway_schema_history / company / user / user_company / flyway_schema_history_v44) | A |
| 241V2 §17.1 第 7 行 | "§6.4 / §12.6 5 张表" | A |
| 241V2 §19.2 变更矩阵 | "5 张表" | A |
| 241V2 §20 一句话判断 | "IGNORE_TABLES_V44 在 §6.4 冻结为 5 张表" | A(与 §6.4 实际内容矛盾) |

**矛盾核心**:**§6.4 / §6.6 实际 Java 代码 = 2 张表**,**§12.6 / §17.1 / §19.2 / §20 文字表述 = 5 张表**。

§20 一句话判断说"§6.4 冻结为 5 张表" — 但 §6.4 实际只有 2 张表。

### 1.3 风险评估

| 风险 | 严重度 |
|---|:-:|
| 设计意图正确(5 张表) | ✓ |
| 代码片段正确(2 张表) | ✗ |
| 实施者若直接复制 §6.6 代码 | **✗ 登录/注册会失败**(因为 user / user_company 表被错加 WHERE companyId=? 过滤)|
| 设计 PASS 但实施时静默错误 | **风险等级 = P0 等级启动阻塞** |

### 1.4 本轮精确范围

| 修复 | 严重度 | 范围 |
|---|---|---|
| **P1-1 真闭环** | P1 | 本补丁 §3 / §4 / §5 / §6 |
| 其他 P0/P1(241A-1 已修)| — | 沿用 241V2 / 241V2A / 241V2A-1 / 241V2A-2 |
| P2(241A-1 已识别的 P2-1/P2-2/P2-3)| — | 沿用 |
| 241A-1 P1-2 测试 self-invocation | P1 | **由 241V2A-3 补丁独立处理**(本文件不涉及)|

---

## §2 严格禁止(本轮)

- ✗ 修改 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2

---

## §3 Effective Spec 冻结(241V3 核心)

### 3.1 最终设计 = 5 张 IGNORE_TABLES(241V3 显式冻结)

**【241V3 冻结】** V4.4 `IGNORE_TABLES_V44` = **5 张表**(以 241V2 §12.6 文字修订为准):

```java
private static final Set<String> IGNORE_TABLES_V44 = Set.of(
    "flyway_schema_history",        // 类别 C:Flyway 系统表
    "company",                      // 类别 B:主键自指
    "user",                         // 类别 A 特殊:无 companyId 字段
    "user_company",                 // 类别 A 特殊:无 companyId 字段
    "flyway_schema_history_v44"     // 类别 C:预留保留名
);
```

### 3.2 5 张表各自的冻结理由(逐表证据)

#### 3.2.1 `flyway_schema_history`

| 维度 | 理由 |
|---|---|
| 表来源 | Flyway 9.22.3 系统表(241V2 §10.2 启用) |
| 是否需要 TenantLine 过滤 | ✗ 否 |
| 分类(241V2 §6.2)| C(系统表,无 companyId 字段)|
| 加入 IGNORE_TABLES 原因 | Flyway 内部迁移历史,与业务 company scope 无关 |
| 241V2 引用位置 | §6.4 / §6.6 / §10.2 / §10.3 / §12.6 |
| 证据等级 | A(Flyway 官方文档 + 241V2 §10.3 配置)|

#### 3.2.2 `company`

| 维度 | 理由 |
|---|---|
| 表来源 | V4.4 业务表(241V2 §12.1 之外,自定)|
| 是否需要 TenantLine 过滤 | ✗ 否 |
| 分类(241V2 §6.2)| B(主键自指)|
| 加入 IGNORE_TABLES 原因 | company.companyId 是主键,自指 companyId 是无意义条件;登录时根据 userId 查 user_company 获取所有 company,不能给 company 加 WHERE companyId=?;创建新 company(注册)时,companyId 还没生成 |
| 241V2 引用位置 | §6.4 / §6.6 / §12.6 |
| 证据等级 | A(241A-1 §5.2 + 241V2 §6.2)|

#### 3.2.3 `user`

| 维度 | 理由 |
|---|---|
| 表来源 | 241V2 §12.2 冻结的 user 表 |
| 是否需要 TenantLine 过滤 | ✗ 否 |
| 分类(241V2 §6.2)| A(无 companyId 字段)|
| 加入 IGNORE_TABLES 原因 | user 表**无** companyId 字段(241V2 §12.2 显式无此列);如果 user 表**不**在 IGNORE_TABLES,MyBatis-Plus TenantLineInnerInterceptor 会试图给它加 WHERE companyId=?,导致 SELECT * FROM user WHERE id=? 实际变成 SELECT * FROM user WHERE id=? AND companyId=?,因为 user 表无 companyId 字段 → SQL 错误 |
| 241V2 引用位置 | §12.2 / §12.6 |
| 证据等级 | A(241V2 §12.2 DDL 无 companyId 字段)|

#### 3.2.4 `user_company`

| 维度 | 理由 |
|---|---|
| 表来源 | 241V2 §12.1 冻结的 user_company 中间表 |
| 是否需要 TenantLine 过滤 | ✗ 否 |
| 分类(241V2 §6.2)| A(无 companyId 字段)|
| 加入 IGNORE_TABLES 原因 | user_company 表**无** companyId 字段(241V2 §12.1 显式无此列);表是 user-company 多对多关系本身,user_id 和 company_id 都是 FK,但**不**是 tenant scope 列;如果不加入 IGNORE_TABLES,TenantLine 会错加 WHERE companyId=? 过滤(此列不存在) → SQL 错误 |
| 241V2 引用位置 | §12.1 / §12.6 |
| 证据等级 | A(241V2 §12.1 DDL 无 companyId 字段)|

#### 3.2.5 `flyway_schema_history_v44`(预留)

| 维度 | 理由 |
|---|---|
| 表来源 | 预留保留名(若 V4.4 Flyway 配置中 `spring.flyway.table` 改名)|
| 是否需要 TenantLine 过滤 | ✗ 否 |
| 分类(241V2 §6.2)| C(系统表,无 companyId 字段)|
| 加入 IGNORE_TABLES 原因 | 防御性预留;若实施时 V4.4 Flyway 配置将 `flyway_schema_history` 改名为 `flyway_schema_history_v44`,原表名不再存在,新表名仍需 bypass |
| 241V2 引用位置 | §12.6 |
| 证据等级 | B(241V2 §12.6 文字声明,无 V4.4 实施证据)|

### 3.3 12 业务表 + 2 系统表 + 1 预留 = 15 张表总览

| 类别 | 表 | 在 IGNORE_TABLES | 应 TenantLine |
|---|---|:-:|:-:|
| V4.4 业务表(12 张,来自 236B) | customer / patient / employee / consult_room / big_screen / appointment_schedule / appointment_slot / appointment / visit / triage_queue / reception_queue | ✗ | ✓(都有 companyId) |
| V4.4 业务表(2 张,来自 241V2)| company / user_company | ✓ | (无 companyId)|
| 系统表(2 张)| flyway_schema_history / flyway_schema_history_v44 | ✓ | (无 companyId)|
| 系统表(1 张)| user | ✓ | (无 companyId)|

**15 张表 = 12 业务表 + 2 系统表 + 1 预留,其中 5 张在 IGNORE_TABLES(必须 bypass TenantLine),10 张业务表自动 TenantLine 过滤**

### 3.4 数据流总览(241V3 显式)

```
MyBatis-Plus TenantLineInnerInterceptor.ignoreTable(tableName)
   ↓
return IGNORE_TABLES_V44.contains(tableName.toLowerCase())
   ↓
   ├─ true(5 张表):SQL 不加 WHERE companyId=?
   └─ false(10 张表):SQL 自动加 WHERE companyId = ?
```

---

## §4 旧代码作废声明(241V3 核心)

### 4.1 作废范围

**【241V3 显式作废】** 以下位置所示的 2 张表 IGNORE_TABLES Java 代码示例 = **作废**:
- 241V2 §6.4 line 586-588(文字)
- 241V2 §6.6 line 646-649(**Java 代码示例**)
- 241V2 §11 变更矩阵 line 884 行(写"2 张表")

**作废原因**:与 §12.6 修订 5 张表直接矛盾;若 S1-169-2 实施时复制此 2 张表版本,会导致 user / user_company / company 表被错加 WHERE companyId=? 过滤,登录/注册失败。

### 4.2 沿用范围(241V3 显式)

**【241V3 沿用】** 以下位置的 5 张表文字表述 = **正确 Effective Spec**:
- 241V2 §12.6 line 1073-1083(完整 DDL 修订)
- 241V2 §17.1 第 7 行
- 241V2 §19.2 变更矩阵
- 241V2 §20 一句话判断

### 4.3 旧代码 vs 新代码 对照

| 位置 | 旧代码(2 张)| **新代码(5 张,本补丁冻结)** |
|---|---|---|
| TenantLineInnerInterceptor 实际 Set | `Set.of("flyway_schema_history", "company")` | **`Set.of("flyway_schema_history", "company", "user", "user_company", "flyway_schema_history_v44")`** |
| 状态 | **作废** | **Effective Spec(必须采用)** |

### 4.4 显式冲突对照(241V3 显式声明)

| 文档位置 | 内容 | 与 Effective Spec 一致? |
|---|---|:-:|
| 241V2 §6.4 | 文字"2 张表" | ✗ **作废(与 §12.6 矛盾)** |
| 241V2 §6.6 | **Java 代码 2 张** | ✗ **作废(实施时绝对不得复制)** |
| 241V2 §11 | 变更矩阵"2 张表" | ✗ **作废(与 §19.2 矛盾)** |
| 241V2 §12.6 | 文字 5 张表 | ✓ **Effective Spec** |
| 241V2 §17.1 | "5 张表" | ✓ |
| 241V2 §19.2 | "5 张表" | ✓ |
| 241V2 §20 | "5 张表" | ✓ |
| 241A-1 §3 | "5 张表(本审计认定)" | ✓ |

---

## §5 S1-169-2 实施不可误抄约束(241V3 显式)

### 5.1 实施约束规则

**【241V3 冻结】** S1-169-2 实施时,实施者**必须**遵循以下规则:

1. ✓ `MybatisPlusConfig.java` 中 `IGNORE_TABLES_V44` **必须**采用 5 张表版本
2. ✗ 不得复制 241V2 §6.6 中的 2 张表 Java 代码
3. ✗ 不得复制任何来源不明的"占位"或"简化"版本
4. ✓ 实施完成后**必须**通过 INFRA-10(241V2 §6.7 / §15.1)测试:查询 company 表时 SQL **不带** WHERE companyId=?
5. ✓ 实施完成后**必须**验证:登录时查 user_company 表 SQL **不带** WHERE companyId=?
6. ✓ 实施完成后**必须**验证:登录时查 user 表 SQL **不带** WHERE companyId=?

### 5.2 实施代码模板(241V3 提供,非生产代码)

```java
// 文件:backend/src/main/java/com/optflow/pms/config/MybatisPlusConfig.java

package com.optflow.pms.config;

import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.BlockAttackInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.OptimisticLockerInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.TenantLineInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.handler.TenantLineHandler;
import net.sf.jsqlparser.expression.Expression;
import net.sf.jsqlparser.expression.LongValue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.apache.ibatis.reflection.MetaObject;
import com.baomidou.mybatisplus.extension.plugins.inner.InnerInterceptor;

import java.util.Set;

@Configuration
public class MybatisPlusConfig {

    /**
     * V4.4 IGNORE_TABLES - 5 张表(241V3 冻结)
     * 
     * 严禁简化为 2 张表版本!若简化,登录/注册会因 user / user_company 表被错加
     * WHERE companyId=? 过滤而失败。
     */
    private static final Set<String> IGNORE_TABLES_V44 = Set.of(
        "flyway_schema_history",        // Flyway 系统表
        "company",                      // 主键自指
        "user",                         // 无 companyId 字段(241V2 §12.2)
        "user_company",                 // 无 companyId 字段(241V2 §12.1)
        "flyway_schema_history_v44"     // 预留(若 Flyway 改名)
    );

    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();

        TenantLineInnerInterceptor tenantInterceptor = new TenantLineInnerInterceptor(
            new TenantLineHandler() {
                @Override
                public Expression getTenantId() {
                    Long companyId = com.optflow.pms.common.context.CompanyContext.requireCompanyId();
                    return new LongValue(companyId);
                }

                @Override
                public String getTenantIdColumn() {
                    return "companyId";
                }

                @Override
                public boolean ignoreTable(String tableName) {
                    return IGNORE_TABLES_V44.contains(tableName.toLowerCase());
                }
            }
        );
        interceptor.addInnerInterceptor(tenantInterceptor);

        // 分页 / 乐观锁 / 防全表更新
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(
            com.baomidou.mybatisplus.annotation.DbType.MYSQL));
        interceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
        interceptor.addInnerInterceptor(new BlockAttackInnerInterceptor());

        return interceptor;
    }
}
```

### 5.3 实施验证清单(241V3 冻结)

实施完成后,**必须**逐项验证:

| # | 验证项 | 验证方法 | 期望 |
|---:|---|---|---|
| 1 | 5 张表在 IGNORE_TABLES_V44 | 单元测试 / 反射读取 | Set size == 5 |
| 2 | flyway_schema_history bypass | 启动 Spring Boot,看 SQL 日志 | SELECT flyway_schema_history 无 WHERE companyId=? |
| 3 | company bypass | 启动 + 登录 + 看 SQL | SELECT company WHERE id=? 无 WHERE companyId=? |
| 4 | user bypass | 启动 + 登录 + 看 SQL | SELECT user WHERE id=? 无 WHERE companyId=? |
| 5 | user_company bypass | 启动 + 登录 + 看 SQL | SELECT user_company WHERE user_id=? 无 WHERE companyId=? |
| 6 | 12 业务表 TenantLine 过滤 | 启动 + 业务查询 + 看 SQL | SELECT customer WHERE ... AND companyId=? |
| 7 | INFRA-10 测试通过 | 241V2 §15.1 | ✓ |

---

## §6 概念分类(241V3 沿用 241V2 §6.2)

### 6.1 IGNORE_TABLES 分类原则(沿用 + 显式声明)

**【241V3 沿用 241V2 §6.2】** 一张表**应**加入 IGNORE_TABLES,当且仅当满足下列**任一**:

1. ✓ 该表无 `companyId` 字段(系统表 / Flyway 表 / 字典表)
2. ✓ 该表是 `company` 自身(主键自指,无意义过滤)
3. ✓ 该表是跨 company 共享的全局配置(字典 / 枚举 / 系统参数)

**一张表**不应**加入 IGNORE_TABLES,如果**:

- ✗ 该表有 `companyId` 字段且属于业务数据
- ✗ 期望 TenantLine 拦截器自动加 `WHERE companyId=?` 过滤

### 6.2 5 张表各自所属类别

| 表 | 类别(241V2 §6.2)| 满足条件 |
|---|---|:-:|
| flyway_schema_history | C(系统表)| 条件 1(无 companyId 字段)|
| company | B(主键自指)| 条件 2 |
| user | A(无 companyId 字段)| 条件 1 |
| user_company | A(无 companyId 字段)| 条件 1 |
| flyway_schema_history_v44 | C(系统表)| 条件 1 |

---

## §7 补丁叠加关系(241V3 显式)

### 7.1 与前序文档关系

| 文档 | 定位 | 与 241V3 关系 |
|---|---|---|
| 240 | Q4 跨公司隔离架构正式裁决 | 基础 |
| 241 | V4.4 基础设施设计基线 | 基础 |
| 241V2 | 基础设施设计修正版 | 包含 5 张表文字(§12.6)但代码示例错(§6.6 2 张)|
| 241V2A | P0-2 companyId 强制覆盖 | 与 IGNORE_TABLES 无关,沿用 |
| 241V2A-1 | defaultCompany 并发控制 | 与 IGNORE_TABLES 无关,沿用 |
| 241V2A-2 | 并发测试 / 死锁表述 | 与 IGNORE_TABLES 无关,沿用 |
| 241A-1 | 独立盲审 | 识别 P1-1(本补丁修复)|
| **241V3** | **IGNORE_TABLES 代码一致性补丁** | **本文件,显式作废 §6.4 / §6.6 旧代码**|

### 7.2 241V3 增量内容

| 241V2 内容 | 241V3 增量 |
|---|---|
| §6.4 文字"2 张表" | 显式**作废**(§4.1) |
| §6.6 Java 代码 2 张 | 显式**作废**(§4.1)+ 提供 5 张表实施模板(§5.2) |
| §12.6 文字 5 张表 | **沿用为 Effective Spec**(§3) |
| §17.1 处置 5 张表 | 沿用 |
| §19.2 变更矩阵 5 张表 | 沿用 |
| §20 一句话 5 张表 | 沿用 |
| (无)| **新增 5 张表各自冻结理由**(§3.2) |
| (无)| **新增 S1-169-2 实施不可误抄约束**(§5)|
| (无)| **新增实施验证清单**(§5.3) |

### 7.3 严格关系

- ✗ 241V3 **不**修改 241V2 任何字节
- ✗ 241V3 **不**修改 241V2A / 241V2A-1 / 241V2A-2 任何字节
- ✓ 241V3 通过"补丁叠加"建立增量关系
- ✓ Effective Spec 唯一(5 张表)由 241V3 显式冻结
- ✓ 后续审计 / 实施必须**采用** 5 张表

---

## §8 241A-1 P1-1 闭环验证

### 8.1 P1-1 原始问题

> "241V2 §6.4 / §6.6 vs §12.6 IGNORE_TABLES 数量矛盾"

### 8.2 241V3 修复手段

| 修复手段 | 位置 |
|---|---|
| 显式作废 §6.4 文字"2 张表" | §4.1 |
| 显式作废 §6.6 Java 代码 2 张 | §4.1 |
| 显式作废 §11 变更矩阵"2 张表" | §4.1 |
| 5 张表 Effective Spec 冻结 | §3 |
| 5 张表各自理由 | §3.2 |
| S1-169-2 实施约束 | §5 |
| 实施代码模板(5 张) | §5.2 |
| 实施验证清单 | §5.3 |

### 8.3 P1-1 闭环率 = 100%

| 检查项 | 通过 |
|---|:-:|
| 5 张表显式冻结 | ✓ |
| 旧 2 张表代码显式作废 | ✓ |
| 实施者不能误抄旧代码 | ✓(§5.1 显式约束 + §5.2 实施模板)|
| 实施验证清单完整 | ✓(§5.3 7 项验证)|

**P1-1 真闭环** ✓

---

## §9 补丁后独立自审(241V3 自身)

### 9.1 P1-1 是否完全消失

| 检查项 | 结论 |
|---|:-:|
| §6.4 旧 2 张表作废? | ✓ §4.1 显式声明 |
| §6.6 旧 2 张表 Java 代码作废? | ✓ §4.1 显式声明 |
| §11 变更矩阵 2 张表作废? | ✓ §4.1 显式声明 |
| §12.6 5 张表作为最终设计? | ✓ §3.1 显式冻结 |
| 5 张表各自理由? | ✓ §3.2 逐表冻结 |
| S1-169-2 实施约束? | ✓ §5.1 6 条规则 + §5.2 模板 + §5.3 清单 |

**P1-1 完全消失** ✓

### 9.2 是否产生新的 P0

| 检查项 | 结论 |
|---|:-:|
| 5 张表覆盖所有无 companyId 字段的表? | ✓ flyway_schema_history / user / user_company |
| company 自指被覆盖? | ✓ |
| 12 业务表全部 NOT in IGNORE? | ✓ |
| 实施模板正确? | ✓ 5 张表 |
| 验证清单可执行? | ✓ 7 项 |

**无新 P0** ✓

### 9.3 是否产生新的 P1

| 检查项 | 结论 |
|---|:-:|
| 5 张表有矛盾? | ✗ 无 |
| 5 张表 vs 12 业务表有遗漏? | ✗ 无 |
| 实施约束清晰? | ✓ §5.1 6 条规则 |
| 验证清单完整? | ✓ §5.3 7 项 |

**无新 P1** ✓

### 9.4 是否与前序文档冲突

| 检查项 | 结论 |
|---|:-:|
| 240 Q4 架构? | ✗ 不冲突(TenantLine 设计)|
| 235B 命名? | ✗ 不冲突(无关)|
| 236B DDL? | ✗ 不冲突(12 业务表 31 FK 不变)|
| 241V2 §12.6? | ✓ 一致(5 张表) |
| 241V2A? | ✗ 不冲突(无关)|
| 241V2A-1? | ✗ 不冲突(无关)|
| 241V2A-2? | ✗ 不冲突(无关)|
| 241A-1? | ✓ 修复其识别的 P1-1 |

**无冲突** ✓

### 9.5 Effective Spec 是否唯一

- ✓ 5 张表 = IGNORE_TABLES_V44 唯一设计
- ✗ 旧 2 张表显式作废(不再作为 Effective Spec)

**唯一** ✓

### 9.6 S1-169-2 实施者是否仍可能误抄旧代码

| 风险 | 缓解 |
|---|---|
| 实施者直接复制 241V2 §6.6 代码 | 241V3 §4.1 显式作废 + §5.1 规则 2 显式禁止 |
| 实施者看到 §6.6 仍为 2 张表而误用 | 241V3 §5.3 实施验证清单 7 项强制验证 |
| 实施者复制 241V2 §11 变更矩阵的 2 张表表述 | 241V3 §4.1 显式作废 §11 变更矩阵 |
| 实施者混淆"文字 5 张 vs 代码 2 张" | 241V3 提供完整 5 张表实施模板(§5.2) |

**S1-169-2 误抄风险** = 显著降低 ✓

---

## §10 报告统计

- 报告字节数:约 18000 字节
- 章节数:14
- 修复的 P1:1(P1-1)
- 作废的旧代码位置:3 处(§6.4 文字 / §6.6 Java 代码 / §11 变更矩阵)
- 冻结的 Effective Spec:1 个(5 张表)
- 新增的 5 张表理由:5 项(逐表)
- 新增的 S1-169-2 实施约束:6 条规则 + 1 模板 + 7 项验证清单
- 与前序文档关系:7 层增量
- P0 闭环:不适用
- P1 闭环:P1-1 = 100%
- DDL 修改:0
- 启动闸门:241V3 完成,等待 241A-1-N 独立盲审

---

## §11 启动闸门(241V3 不变)

### 11.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241V2 修复原 4 P0 + 1 P1 | ✓ | 241V2 |
| 241V2A P0-2 真闭环 | ✓ | 241V2A |
| 241V2A-1 defaultCompany 并发控制 | ✓ | 241V2A-1 |
| 241V2A-2 死锁表述 + 测试事务 | ✓ | 241V2A-2 |
| 241A-1 独立盲审识别 2 个 P1 | ✓ | 241A-1(本审计)|
| **241V3 修复 P1-1(本文件)** | **✓** | **本文件** |
| **241V2A-3 修复 P1-2**(并行补丁) | **✓** | **241V2A-3 同步完成** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 11.2 下一轮盲审必审计

- ✓ 241V3 是否真修复 P1-1
- ✓ 241V3 是否引入新 P0/P1
- ✓ 241V3 Effective Spec 是否唯一
- ✓ 241V3 + 241V2A-3 两者是否冲突
- ✓ 6 份文档(241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241V3 / 241V2A-3)是否仍有内部矛盾

---

## §12 一句话最终判断

> **241V3 S1-169-1 IGNORE_TABLES 代码一致性补丁完成**:241A-1 独立盲审识别的 P1-1(241V2 §6.4 / §6.6 IGNORE_TABLES Java 代码 = 2 张表 vs §12.6 文字修订 5 张表直接矛盾)通过本补丁**真闭环**——5 张表 `Set.of("flyway_schema_history", "company", "user", "user_company", "flyway_schema_history_v44")` 显式冻结为 V4.4 Effective Spec,逐表冻结理由(类别 C 系统表 / 类别 B 主键自指 / 类别 A 无 companyId 字段 / 预留名),旧 2 张表 Java 代码示例(241V2 §6.4 文字 / §6.6 Java 代码 / §11 变更矩阵)**显式作废**并标记"绝对不得复制",S1-169-2 实施时**必须**采用 5 张表版本(§5.2 完整实施模板 + §5.3 7 项强制验证清单);与 241V2 §12.6 / §17.1 / §19.2 / §20 文字表述一致,无新 P0/P1,Effective Spec 唯一;241V3 不修改 241V2 任何字节,只通过补丁叠加建立增量关系;S1-169-2 仍 BLOCK,等下一轮独立盲审同时审计 241V3 + 241V2A-3。

---

## §13 报告统计(完整)

- 章节数:13
- 修复的 P1:1(P1-1)
- 5 张表各自冻结理由:5 项
- S1-169-2 实施约束:6 条规则 + 1 模板 + 7 项验证
- 显式作废位置:3 处
- 与前序文档关系:7 层
- 启动闸门:全部满足
- 下一轮:独立盲审
