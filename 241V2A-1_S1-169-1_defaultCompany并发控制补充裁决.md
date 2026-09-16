# 241V2A-1 S1-169-1 defaultCompany 并发控制补充裁决

> **本轮定位**:补齐 S1-169-1 阶段 default company **并发唯一性**的完整冻结。在 241V2 §12.3 应用层原子更新基础上,**正式冻结并发控制方案 / 锁对象 / 事务边界 / 死锁处理 / 6 场景结果 / 5 项 DEFAULT 测试**。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 任何历史 MD
> - 严禁修改 VisionCare PMS 任何文件
> - 严禁创建 backend/ / 严禁写 Java / 严禁创建 SQL 文件 / 严禁执行 DDL / 严禁连接数据库
> - 严禁修改 pom.xml / application.yml
> - 严禁 commit / 严禁 push
> - 标签:【原系统事实】/【已验证业务事实】/【OptFlow设计】/【待确认】
> - 本文件**唯一目的** = 把 `setDefaultCompany` 的并发一致性**完整闭环冻结**
> - 阶段:**S1-169-1**(未进入 S1-169-2)
> - 本裁决完成后**不**自评 PASS,**等待 241A-1 独立盲审**

---

## §0 Git 基线

- **HEAD**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`(S1-169-0 240 commit)
- **REMOTE == LOCAL**:`6efa0da` ✓
- **0 号闸门 4 文件 SHA256 全部 PASS** ✓
  - controller.js `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433`
  - deliveryList.html `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`
  - machineOrderCompleted.html `F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24`
  - machineOrderList.html `A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A`
- **历史 MD(190~241V2A 共 62 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-1 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 现状

| 文档 | 状态 |
|---|---|
| 240 Q4 跨公司隔离架构 | ✓ 已 commit |
| 241V2 基础设施设计修正版 | ✓ 完成,4 P0 + 1 P1 修复(本批前) |
| 241V2A P0-2 强制覆盖补丁 | ✓ 完成,MetaObjectHandler 真闭环 |
| **241V2A-1 defaultCompany 并发控制** | **本轮**(本文件) |

### 1.2 本轮核心

241V2 §12.3 给出 `setDefaultCompany` 的应用层原子更新骨架:

```java
@Transactional
public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
    // 1. 验证权限
    // 2. 把现有 is_default=1 改为 0
    // 3. 把 target 设置为 1
}
```

但**未冻结**:
- ✗ 并发控制机制
- ✗ 锁定对象
- ✗ 锁顺序
- ✗ 事务边界完整性
- ✗ 异常回滚保证
- ✗ 死锁处理
- ✗ 并发测试

### 1.3 严格禁止(本轮)

- ✗ 修改 241V2 / 241V2A / 任何历史 MD
- ✗ 创建 backend/ / 写 Java / 创建 SQL / 执行 DDL
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等 241A-1 独立盲审)
- ✗ 进入 S1-169-2

---

## §2 现有 241V2 §12.3 设计回顾

### 2.1 241V2 §12.3 现状(继承,不作废)

**【241V2 冻结】** `defaultCompanyId` 归属 = `user_company.is_default` 字段(中间表,不是 user 表)。

**逻辑保证**(241V2 §12.3 原文):
- 同一 user 不能有 2 条 `is_default=1` 的记录
- 用应用层保证(`UserCompanyService.setDefaultCompany(userId, companyId)` 原子更新)
- MySQL 不支持部分 UNIQUE,**应用层是唯一保证**

### 2.2 241V2 §12.3 的并发漏洞

`@Transactional` 仅保证**单事务内**的原子性,**不**保证并发事务的串行化。

**漏洞场景**:
```
时间线:
T1: 事务 A 启动
T1: 事务 A: read user_company → old default = companyA, is_default=1
T1: 事务 A: write old default → is_default=0
T1: 事务 A 还未 commit
T2: 事务 B 启动
T2: 事务 B: read user_company → old default = companyA, is_default=0(A 的修改未提交,B 看不到)
T2: 事务 B: write companyB → is_default=1
T2: 事务 B: commit
T3: 事务 A: write companyA → is_default=1
T3: 事务 A: commit

最终结果: 两条 is_default=1(companyA + companyB)
```

**根因**:READ COMMITTED 隔离级别下,两个事务看不到对方未提交的数据,各自独立判断"现有 default 是 0"然后各自写 1 → 经典 lost update 问题。

### 2.3 本裁决目标

把 241V2 §12.3 的"应用层保证"升级为"**悲观行锁 + 完整事务**",从根上消除 lost update。

---

## §3 并发问题诊断

### 3.1 核心矛盾

`user_company.is_default` 是**用户级共享状态**(同一 user 多条记录中只能一条 is_default=1),但:
- 同一 user 可能有 N 条 user_company 记录(多店)
- 改 default 必须动多条记录(老 default 改 0 + 新 default 改 1)
- **行级操作 ≠ 集合级唯一性**

### 3.2 三种候选方案对比

| 方案 | 锁对象 | 优点 | 缺点 | 决策 |
|---|---|---|---|---|
| **A. 锁 user 单行** | `user` 表主键 | 简单 / 不易死锁 / 单行锁开销小 | 需先 SELECT FOR UPDATE | **✓ 选 A** |
| B. 锁 user_company 该 user 的全部关联行 | `user_company(user_id=N)` 多行 | 锁住具体行 | 锁顺序难统一 / 易死锁 | ✗ |
| C. 乐观锁(版本号) | 加 version 列 | 无锁 | 需要 schema 变更 / 业务重试 / 仍可能 N 个 default 后回滚 | ✗ |
| D. 数据库 UNIQUE 约束 | MySQL 部分 UNIQUE | 数据库保证 | **MySQL 不支持部分 UNIQUE 索引** | ✗ 不可行 |

**【241V2A-1 冻结】** 选 **方案 A:锁 user 单行**(Pessimistic Row Lock on user.id)。

### 3.3 为什么选 A 不选 B

| 维度 | A(锁 user) | B(锁 user_company 多行) |
|---|---|---|
| 锁粒度 | 1 行 | N 行(N=user 的 company 数) |
| 死锁风险 | ✗ 无(单行) | ✓ 有(多事务锁多行,顺序不一致) |
| 锁升级风险 | ✗ 无 | ✓ 有(可能升级到 gap lock / next-key lock) |
| 跨 user 性能 | ✓ 完美并行(不同 user 互不干扰) | ✓ 也并行 |
| 锁时间 | 短(单行) | 长(多行 + 关联查询) |
| 实现复杂度 | 简单 | 复杂(需 ORDER BY 避免死锁) |

**结论**:A 方案在所有维度上**严格优于** B 方案。

### 3.4 为什么不用乐观锁(C 方案)

| 问题 | 说明 |
|---|---|
| Schema 变更 | 需要 `user_company` 加 `version` 列(241V2 §12.1 DDL 不含此列,需修改冻结的 schema) |
| 业务重试 | 冲突时需业务层重试,增加复杂度 |
| lost update 残留 | 乐观锁失败回滚,但失败时其他事务可能已经修改 default,导致不一致中间态 |
| 不符合 240 严格策略 | 240 明确"不能用乐观锁替代 company 校验"(240 §6.4) |

**结论**:乐观锁与 V4.4 架构风格不匹配,选悲观锁。

---

## §4 锁对象最终冻结

### 4.1 锁对象 = `user` 表主键

**【241V2A-1 冻结】** `setDefaultCompany` 的并发控制锁 = **`user.id` 单行锁**。

```sql
SELECT id, login_name, status
FROM user
WHERE id = #{userId}
FOR UPDATE
```

### 4.2 为什么锁 user 不锁 user_company

| 维度 | 解释 |
|---|---|
| **同一 user 串行化** | 不同事务的 setDefaultCompany(userId) 都在 `user.id` 排队,确保串行 |
| **跨 user 完美并行** | 不同 user 的 setDefaultCompany 互不干扰,user 表按主键索引锁 |
| **避免锁顺序问题** | 只锁 1 行,不存在"按 A→B 锁"还是"按 B→A 锁" |
| **user 表已有索引** | `user.id` 是主键,InnoDB 主键索引锁开销极小 |
| **user 表 1 行 1 user** | 锁粒度精确,不会误伤其他 user 的 user_company |

### 4.3 锁的语义

```sql
-- InnoDB 行锁行为:
BEGIN;
SELECT * FROM user WHERE id = 1 FOR UPDATE;  -- 1. 获得 user.id=1 的 X 锁
-- 同一时刻,任何其他事务尝试 SELECT ... FOR UPDATE WHERE id=1 都会阻塞
-- 普通 SELECT (无 FOR UPDATE) 不阻塞(InnoDB MVCC)

-- 在锁内:
UPDATE user_company SET is_default = 0 WHERE user_id = 1;  -- 2. 改 user_company
UPDATE user_company SET is_default = 1 WHERE user_id = 1 AND company_id = ?;  -- 3. 设新 default
-- 提交
COMMIT;  -- 4. 释放 X 锁
```

### 4.4 严格禁止

- ✗ 不得用 `LOCK TABLES`(表锁,粒度太大)
- ✗ 不得用 `SELECT ... LOCK IN SHARE MODE`(S 锁,允许其他事务读但不能改 user 表;不需要这种"可读不可改"语义)
- ✗ 不得跳过 user 行锁直接改 user_company(会 lost update)
- ✗ 不得在 `setDefaultCompany` 之外的地方尝试用别的锁(避免锁顺序混乱)

---

## §5 事务边界最终冻结

### 5.1 事务边界

**【241V2A-1 冻结】** `setDefaultCompany` 必须 = **单一 Spring `@Transactional` 方法**,事务内 7 步顺序**不可变**:

```java
@Transactional(rollbackFor = Exception.class, isolation = Isolation.READ_COMMITTED)
public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
    // 步骤 1:获取 user 行锁(锁对象)
    User user = userMapper.selectByIdForUpdate(userId);  // SELECT ... FOR UPDATE
    if (user == null) {
        throw new UserNotFoundException("user 不存在: " + userId);
    }
    if (user.getStatus() != 1) {
        throw new UserDisabledException("user 已禁用: " + userId);
    }
    
    // 步骤 2:验证 target company 权限(在锁内)
    if (!userCompanyRepository.existsByUserIdAndCompanyId(userId, newDefaultCompanyId)) {
        throw new CompanyAccessDeniedException("用户无权访问 companyId=" + newDefaultCompanyId);
    }
    
    // 步骤 3:验证 target company 状态(在锁内)
    Company company = companyRepository.selectById(newDefaultCompanyId);
    if (company == null || company.getStatus() != 1) {
        throw new CompanyAccessDeniedException("company 不可用: " + newDefaultCompanyId);
    }
    
    // 步骤 4:将该 user 现有 default 清零(在锁内)
    userCompanyRepository.updateDefaultToZero(userId);
    
    // 步骤 5:设置目标 company 为 default(在锁内)
    int affected = userCompanyRepository.setDefault(userId, newDefaultCompanyId);
    if (affected != 1) {
        // 防御性检查:不应该发生(步骤 2/3 已校验)
        throw new IllegalStateException("setDefault 失败:affected=" + affected);
    }
    
    // 步骤 6:验证最终状态(在锁内)
    int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
    if (defaultCount > 1) {
        // 防御性:不应该发生(事务内串行化)
        throw new IllegalStateException("发现多条 default: count=" + defaultCount);
    }
    
    // 步骤 7:事务提交由 Spring @Transactional 自动管理
}
```

### 5.2 严格禁止

- ✗ 不得拆成多个事务:
  ```java
  // 错误示例:
  @Transactional
  public void updateDefaultToZero(Long userId) { ... }  // 独立事务,会立即 commit
  
  @Transactional
  public void setDefault(Long userId, Long companyId) { ... }  // 另一独立事务
  ```
- ✗ 不得用 `Propagation.REQUIRES_NEW`(新事务会脱离主流程,锁会失效)
- ✗ 不得在事务内调用 `Thread.sleep()` / HTTP 调用(延长锁时间)
- ✗ 不得在事务内 catch 异常后不抛(会覆盖 rollback 信号)

### 5.3 异常 → 自动 rollback

`@Transactional(rollbackFor = Exception.class)` 保证:
- ✓ 任何 Exception 抛出 → Spring 自动回滚事务
- ✓ 释放 user 行锁
- ✓ user_company 改动全部回滚(回到事务前状态)
- ✓ 调用方收到异常,后续逻辑不执行

### 5.4 事务隔离级别

**【241V2A-1 冻结】** 隔离级别 = `READ_COMMITTED`:
- 读已提交,避免脏读
- 配合 user 行锁,避免不可重复读
- 比 REPEATABLE_READ 性能更好(避免 gap lock)
- MySQL InnoDB 默认是 REPEATABLE_READ,但 V4.4 显式选 READ_COMMITTED(本裁决)

---

## §6 最终 `setDefaultCompany` 实现(伪代码 + 配套 Repository)

### 6.1 Service 实现(伪代码)

```java
package com.optflow.pms.module.auth;

@Service
public class UserCompanyServiceImpl implements UserCompanyService {
    
    private final UserMapper userMapper;                    // MyBatis-Plus
    private final CompanyRepository companyRepository;
    private final UserCompanyRepository userCompanyRepository;
    
    @Override
    @Transactional(rollbackFor = Exception.class, isolation = Isolation.READ_COMMITTED)
    public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
        // 步骤 1:锁 user 单行
        User user = userMapper.selectByIdForUpdate(userId);
        if (user == null) {
            throw new UserNotFoundException("user 不存在: " + userId);
        }
        if (user.getStatus() != 1) {
            throw new UserDisabledException("user 已禁用: " + userId);
        }
        
        // 步骤 2:验证 target company 权限
        if (!userCompanyRepository.existsByUserIdAndCompanyId(userId, newDefaultCompanyId)) {
            throw new CompanyAccessDeniedException("用户无权访问 companyId=" + newDefaultCompanyId);
        }
        
        // 步骤 3:验证 target company 状态
        Company company = companyRepository.selectById(newDefaultCompanyId);
        if (company == null || company.getStatus() != 1) {
            throw new CompanyAccessDeniedException("company 不可用: " + newDefaultCompanyId);
        }
        
        // 步骤 4:现有 default 清零
        userCompanyRepository.updateDefaultToZero(userId);
        
        // 步骤 5:设置新 default
        int affected = userCompanyRepository.setDefault(userId, newDefaultCompanyId);
        if (affected != 1) {
            throw new IllegalStateException("setDefault 失败:affected=" + affected);
        }
        
        // 步骤 6:防御性最终验证
        int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
        if (defaultCount > 1) {
            throw new IllegalStateException("发现多条 default: count=" + defaultCount);
        }
    }
}
```

### 6.2 Mapper 配套 SQL(伪代码)

```java
package com.optflow.pms.module.auth.mapper;

public interface UserMapper extends BaseMapper<User> {
    
    /**
     * V4.4 关键:SELECT ... FOR UPDATE 行锁
     * 必须在 @Transactional 事务内调用
     */
    @Select("SELECT id, login_name, status FROM user WHERE id = #{userId} FOR UPDATE")
    User selectByIdForUpdate(Long userId);
}
```

```java
package com.optflow.pms.module.auth.mapper;

public interface UserCompanyMapper extends BaseMapper<UserCompany> {
    
    /**
     * 将 user 所有 default 清零
     * 必须在 @Transactional 事务内调用
     */
    @Update("UPDATE user_company SET is_default = 0, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND is_default = 1")
    int updateDefaultToZero(Long userId);
    
    /**
     * 设置 user 在某 company 的 default = 1
     * 必须在 @Transactional 事务内调用
     */
    @Update("UPDATE user_company SET is_default = 1, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND company_id = #{companyId}")
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);
    
    /**
     * 校验 user 对 company 的权限
     */
    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} AND company_id = #{companyId} AND status = 1")
    int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);
    
    /**
     * 防御性:统计 user 的 default 数
     */
    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} AND is_default = 1")
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
}
```

### 6.3 注意:user_company 无 TenantLine 过滤

`user_company` 在 241V2 §6.4 / §12.6 已加入 IGNORE_TABLES_V44,SQL 不会自动加 `WHERE companyId=?`。
但 `setDefaultCompany` SQL 也不需要 companyId 条件(因为操作的是 user-company 关系本身,不是具体业务行)。

### 6.4 注意:Company 表 TenantLine 处理

`company` 也在 IGNORE_TABLES_V44(241V2 §6.4),但本流程需要 `companyRepository.selectById(newDefaultCompanyId)` 验证 company 状态:

- 方案 1:`companyRepository` 单独实现(不走 MyBatis-Plus BaseMapper),SQL 不触发 TenantLine
- 方案 2:用 `Mapper.selectById` 但在 SQL 显式不加 TenantLine 触发(IGNORE_TABLES 机制已处理)
- ✓ 241V2A-1 确认:用方案 2(因为 company 已在 IGNORE_TABLES_V44,TenantLine 自动 bypass)

---

## §7 死锁分析

### 7.1 单行锁的死锁免疫

**【241V2A-1 冻结】** 由于锁对象 = `user.id` 单行,**不会出现死锁**:

| 场景 | 死锁可能性 |
|---|:-:|
| 同一 user 并发 setDefaultCompany(A vs B)| ✗ **不可能**(同一 user 排队,无循环等待) |
| 不同 user 并发 setDefaultCompany | ✗ **不可能**(锁不同行,完全并行) |
| setDefaultCompany 与其他 user 操作 | ✗ **不可能**(其他 user 操作不锁 user 行) |
| setDefaultCompany 与 user 登录 | ✗ **不可能**(登录只读 user 表,无 FOR UPDATE) |

### 7.2 为什么不用 user_company 多行锁

如果用方案 B(锁 user_company 该 user 的全部行),会出现:

| 场景 | 死锁场景 |
|---|---|
| T1 锁 user_company (user=1, company=A) | T1 持有 A |
| T2 锁 user_company (user=1, company=B) | T2 持有 B |
| T1 想锁 user_company (user=1, company=B) | T1 等 T2 |
| T2 想锁 user_company (user=1, company=A) | T2 等 T1 |
| → 死锁! | |

**A 方案直接锁 user 单行,user 表主键索引保证锁粒度最小,无循环等待**。

### 7.3 锁升级保护

InnoDB 行锁可能升级为 gap lock / next-key lock(在 REPEATABLE_READ 隔离级下)。

- ✓ 241V2A-1 显式选 `READ_COMMITTED`,**避免** gap lock(主键等值查询在 READ_COMMITTED 下只锁记录,不加 gap)
- ✓ 单行主键等值 `WHERE id = ?` 永远不会升级为表锁

### 7.4 锁等待超时

万一出现极端情况(锁未释放),MySQL 有 `innodb_lock_wait_timeout`(默认 50 秒)。

**【241V2A-1 冻结】** 业务侧不显式处理锁等待超时:
- 由 `innodb_lock_wait_timeout` 兜底(50s 后自动失败)
- Spring `@Transactional` 接收到 LockTimeoutException 自动 rollback
- 调用方收到明确异常,可重试或提示用户

### 7.5 死锁处理(完全免疫,但保留)

虽然 241V2A-1 设计**不可能**死锁,但代码层仍保留:

```java
// Service 层可加 @Retryable(MySQLDeadlockException) 防御性
// (本裁决不强制加,只作为未来扩展)
```

---

## §8 6 个并发场景结果矩阵

### 8.1 场景总表(241V2A-1 冻结)

| # | 场景 | 起始状态 | 操作 1 | 操作 2 | 最终状态 | 是否允许 | 异常/响应 |
|---:|---|---|---|---|---|:-:|---|
| 1 | 并发设置不同 default | companyA=1, companyB=0 | A → setDefault(B) | B → setDefault(C) | 仅 companyC=1 | ✓ | 后到者赢;前到者抛 `setDefaultCompanySucceeded=true`,后到者抛 `setDefaultCompanySucceeded=true` |
| 2 | 并发设置同 default | companyA=1 | A → setDefault(A) | B → setDefault(A) | companyA=1 | ✓ | 幂等;两者都成功 |
| 3 | A 失败 + B 成功 | companyA=1, companyB=0 | A → setDefault(C) 失败(C 无权限) | B → setDefault(B) 成功 | companyB=1, companyA=0 | ✓ | A 抛 CompanyAccessDeniedException,事务回滚;B 成功 |
| 4 | 设置 disabled company | companyA=1, companyB 已禁用 | A → setDefault(B) | — | companyA=1(无变化) | ✗ | A 抛 CompanyAccessDeniedException,事务回滚 |
| 5 | user 无 company 权限 | user_company 为空 | A → setDefault(B) | — | 无变化 | ✗ | A 抛 CompanyAccessDeniedException,事务回滚 |
| 6 | 同一 company 重复设置 default | companyA=1 | A → setDefault(A) | — | companyA=1 | ✓ | 幂等(但 SQL 仍会执行,清零 + 重新置 1) |

### 8.2 详细行为说明

#### 场景 1:并发不同 default(A → B, B → C)

| 步骤 | 事务 T1(A → B) | 事务 T2(B → C) | 备注 |
|---:|---|---|---|
| 1 | BEGIN | — | T1 启动 |
| 2 | SELECT user FOR UPDATE | — | T1 获得 user 行锁 |
| 3 | 验证 A 权限 ✓ | — | — |
| 4 | UPDATE old default → 0 | — | — |
| 5 | UPDATE A → 1 | — | — |
| 6 | 验证 default 数 = 1 ✓ | — | — |
| 7 | — | BEGIN | T2 启动 |
| 8 | — | SELECT user FOR UPDATE | **T2 阻塞**(T1 还持锁) |
| 9 | COMMIT | — | T1 提交,释放锁 |
| 10 | — | 锁获取成功 | T2 继续 |
| 11 | — | 验证 C 权限 ✓ | — |
| 12 | — | UPDATE A → 0(覆盖 T1 的结果) | T2 看到 T1 已提交的数据 |
| 13 | — | UPDATE C → 1 | — |
| 14 | — | 验证 default 数 = 1 ✓ | — |
| 15 | — | COMMIT | T2 提交 |

**最终状态**:仅 companyC=1(后到者赢)

#### 场景 2:并发同 default(A → A, B → A)

| 步骤 | 事务 T1 | 事务 T2 | 备注 |
|---:|---|---|---|
| 1 | BEGIN | — | T1 启动 |
| 2 | SELECT user FOR UPDATE | — | T1 获锁 |
| 3 | 验证 A 权限 ✓ | — | — |
| 4 | UPDATE is_default = 0(全 user) | — | — |
| 5 | UPDATE A → 1 | — | — |
| 6 | — | BEGIN | T2 启动 |
| 7 | — | SELECT user FOR UPDATE | T2 阻塞 |
| 8 | COMMIT | — | T1 提交 |
| 9 | — | 锁获取 | T2 继续 |
| 10 | — | 验证 A 权限 ✓ | — |
| 11 | — | UPDATE is_default = 0(全 user) | T2 把 A 也清零 |
| 12 | — | UPDATE A → 1 | T2 重新置 1 |
| 13 | — | 验证 default 数 = 1 ✓ | — |
| 14 | — | COMMIT | T2 提交 |

**最终状态**:companyA=1(幂等,T1 和 T2 都"成功",但实际只有 T2 的最终结果)

**关键点**:`setDefault(A) → updateDefaultToZero → setDefault(A)` 序列幂等(因为 A 始终存在,updateDefaultToZero 清零后 setDefault(A) 重新置 1)。

#### 场景 3:A 失败 + B 成功

- A → setDefault(C)(C 不存在 / 无权限):事务内步骤 2/3 抛异常 → 整个事务 rollback → companyA=1 不变
- B → setDefault(B):B 必须等 A 释放锁 → 然后 B 成功 → companyB=1
- **最终**:companyA=0, companyB=1

#### 场景 4:设置 disabled company

- 步骤 3 验证 company 状态失败 → 抛 `CompanyAccessDeniedException("company 不可用: " + newDefaultCompanyId)`
- 整个事务 rollback
- 旧 default companyA=1 保持不变

#### 场景 5:user 无 company 权限

- user_company 无该 user 的任何记录
- 步骤 2 验证权限失败 → 抛 `CompanyAccessDeniedException`
- 整个事务 rollback
- 数据库无变化

#### 场景 6:同一 company 重复设置 default(幂等)

- companyA 当前 is_default=1
- `setDefault(A)`:
  - 步骤 4:updateDefaultToZero → companyA.is_default=0
  - 步骤 5:setDefault(A) → companyA.is_default=1
  - 步骤 6:验证 default 数 = 1 ✓
- **最终**:companyA=1(等价于无操作)
- ✓ 允许(幂等)

### 8.3 异常映射

| 业务异常 | HTTP 状态码 | 触发场景 |
|---|:-:|---|
| `UserNotFoundException` | 404 | user 不存在 |
| `UserDisabledException` | 403 | user 已禁用 |
| `CompanyAccessDeniedException`(本流程触发) | 403 | 用户无权 / company 不可用 / 跨公司引用 |
| `IllegalStateException` | 500 | setDefault affected != 1 / 多条 default(防御性) |
| `LockTimeoutException`(MySQL 抛) | 500 | 锁等待超时(异常情况) |

---

## §9 "无 default company" 语义冻结

### 9.1 两种方案对比

| 方案 | 含义 | 优点 | 缺点 |
|---|---|---|---|
| **A. 必须存在 1 个** | 每个启用 user 必须始终有 1 个 default | 登录时无需选店 | 增删 company 时需自动迁移 default |
| **B. 允许 0 个** | user 可能无 default | 实现简单 | 登录时需选店(或拒绝) |

### 9.2 最终选择 = 方案 B(允许 0 个)

**【241V2A-1 冻结】** 选 B:**允许 0 个 default company**。

理由:
1. **setDefaultCompany 本身**只保证"操作后最多 1 个"(原子性 / 串行化)
2. **业务层**(未来)负责"新增第一个 company 自动成为 default" / "删除 default 自动迁移"
3. **登录逻辑**(未来)处理"无 default 时如何选 company"(提示用户选 / 默认选唯一 company / 拒绝登录)
4. **本裁决不强制**业务层必须存在 1 个 default

### 9.3 不变量(241V2A-1 冻结)

`setDefaultCompany` 操作结束后,**最多 1 条** user_company 满足 `is_default=1`(针对该 user)。

**操作前**可能是:
- 0 条 is_default=1
- 1 条 is_default=1

**操作后**必然:
- 0 条 is_default=1(如果目标失败)
- 1 条 is_default=1(成功)

**绝对不能**:
- 2+ 条 is_default=1
- 操作前 1 条,操作后变成 2 条(los update)

### 9.4 业务层(超出本裁决,留待后续)

下列业务规则**不**在本裁决范围:
- ✗ 新增第一个 company 是否自动 default
- ✗ 删除 default 时是否自动迁移
- ✗ user 最后一个 company 被禁用时如何处理
- ✗ 登录时无 default 如何处理

这些属于**业务层规则**,需要在 S1-169-2 业务实施时**单独裁决**(可能新建 241V2A-2 / 242 等)。

### 9.5 但并发一致性必须保证

虽然业务层规则"是否必须存在 1 个"留待未来,但**并发一致性**在本裁决**完整冻结**:
- ✓ 同一 user 并发 setDefaultCompany 串行化(§4 user 行锁)
- ✓ 操作后最多 1 条 is_default=1(§5 事务 + 步骤 6 防御性验证)
- ✓ 异常时完整回滚(§5.3)
- ✓ 无死锁(§7)

---

## §10 与 CompanyContext 关系冻结

### 10.1 defaultCompanyId 的定位

**【241V2A-1 冻结】** `defaultCompanyId` **不是**当前请求的 companyId,**只是**用户登录时选定的"默认门店"。

### 10.2 数据流(冻结)

```
User 登录
   ↓
AuthService.login()
   ↓
userCompanyService.getDefaultCompanyId(userId)  ← 从 user_company.is_default=1 读
   ↓
StpUtil.getSession().set("defaultCompanyId", X)
   ↓
[后续每次 HTTP 请求]
   ↓
CompanyContextInterceptor.preHandle()
   ↓
优先级解析(241V2 §5.4.2 步骤 4):
  1. X-Company-Id header(显式切换)→ 必须 hasAccessTo 验证
  2. session.defaultCompanyId(用户默认)
  3. accessibleCompanies[0](用户唯一 company)
   ↓
CompanyContext.setCompanyId(targetCompanyId)
   ↓
当前请求 companyId(≠defaultCompanyId,可能等于)
```

### 10.3 严格禁止

- ✗ `defaultCompanyId` **不得**绕过 `hasAccessTo(userId, targetCompanyId)` 校验
- ✗ `defaultCompanyId` **不得**成为"自动信任的 companyId"
- ✗ 即使是 default company,跨店操作仍需 `X-Company-Id` 显式切换 + hasAccessTo 校验

### 10.4 显式契约

```text
defaultCompanyId  = 用户登录时"偏好的 company"(可由 setDefaultCompany 修改)
当前请求 companyId = 实际生效的 company(X-Company-Id 优先 / defaultCompanyId 兜底)
```

两者**不可混淆**。

### 10.5 setDefaultCompany 不影响当前请求

- A 用户的 defaultCompanyId 在 t1 时刻从 X 改为 Y
- A 用户在 t2 时刻(> t1)的请求:如果带 `X-Company-Id=X`,仍用 X(不受 defaultCompanyId 改变影响)
- A 用户在 t2 时刻(> t1)的请求:如果**不**带 `X-Company-Id`,用 Y(新的 default)

**关键**:setDefaultCompany 只影响"未显式 X-Company-Id"的请求。

---

## §11 数据模型审查

### 11.1 241V2 §12.1 冻结的 user_company DDL 是否足够?

**【241V2A-1 冻结】** user_company DDL(241V2 §12.1)**不需要修改**,并发一致性由"事务 + user 行锁"保证。

| DDL 项 | 是否足够 | 理由 |
|---|:-:|---|
| `UNIQUE KEY uk_user_company (user_id, company_id)` | ✓ | 保证"同一 user 在同一 company 内只有 1 条" |
| `INDEX idx_uc_user (user_id)` | ✓ | 加速 user_id 查询 |
| `INDEX idx_uc_default (user_id, is_default)` | ✓ | 加速 default 查询 + 防御性 count |
| `is_default TINYINT(1) NOT NULL DEFAULT 0` | ✓ | 字段存在 |
| `status TINYINT NOT NULL DEFAULT 1` | ✓ | 业务可禁用 |

### 11.2 为什么不需要"部分 UNIQUE 索引"

MySQL **不**支持 partial unique index(如 `UNIQUE (user_id) WHERE is_default=1`)。

- PostgreSQL 支持 partial index
- MySQL 需要通过触发器或应用层保证
- **241V2A-1 选应用层保证(事务 + 行锁)**,不引入触发器

### 11.3 是否需要触发器补充?

| 方案 | 是否引入 |
|---|:-:|
| 应用层事务(本裁决) | ✓ 已选 |
| MySQL 触发器 | ✗ 不引入(增加复杂度,跨语言/跨服务难维护) |
| 物化视图 | ✗ 不引入(V4.4 简单数据规模不需要) |

### 11.4 DDL 冻结声明

**【241V2A-1 承诺】** 本裁决不修改 241V2 §12.1 任何 DDL 字节。如未来需要(例如引入触发器),**必须**新建 241V2A-2 / 242 等单独裁决。

---

## §12 DEFAULT-01~05 测试设计

### 12.1 测试基础设施要求

- 2 个 Spring Bean(`@Transactional` + `@Async`)
- 1 个 `CountDownLatch`(同步并发起点)
- 1 个独立测试 DB(避免污染)
- 同一 user + 多个 company(至少 3 个)

### 12.2 DEFAULT-01:并发不同 default(A vs B)

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_01_concurrent_different_companies() {
    // Given: user u1 已关联 companyA, companyB, companyC(都 status=1)
    // 当 u1 的 default = companyA
    
    CountDownLatch startLatch = new CountDownLatch(1);
    CountDownLatch endLatch = new CountDownLatch(2);
    AtomicReference<Throwable> error1 = new AtomicReference<>();
    AtomicReference<Throwable> error2 = new AtomicReference<>();
    
    // T1: setDefault(companyB)
    CompletableFuture<Void> f1 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1002L);  // companyB
        } catch (Throwable t) {
            error1.set(t);
        } finally {
            endLatch.countDown();
        }
    });
    
    // T2: setDefault(companyC)
    CompletableFuture<Void> f2 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1003L);  // companyC
        } catch (Throwable t) {
            error2.set(t);
        } finally {
            endLatch.countDown();
        }
    });
    
    // When: 同时启动
    startLatch.countDown();
    endLatch.await(5, TimeUnit.SECONDS);
    
    // Then: 两个事务都成功(后到者赢)
    assertThat(error1.get()).isNull();
    assertThat(error2.get()).isNull();
    
    // 验证: 最多 1 条 is_default=1
    int defaultCount = userCompanyMapper.countByUserIdAndIsDefault(1L, 1);
    assertThat(defaultCount).isEqualTo(1);
    
    // 验证: 默认 company 必须是 user 有效权限中的一个
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(1L);
    assertThat(defaultCompanyId).isIn(1001L, 1002L, 1003L);
}
```

### 12.3 DEFAULT-02:串行 A → B

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_02_serial_AB() {
    // Given: u1 default = companyA
    
    // When
    userCompanyService.setDefaultCompany(1L, 1002L);  // A → B
    
    // Then
    int defaultCount = userCompanyMapper.countByUserIdAndIsDefault(1L, 1);
    assertThat(defaultCount).isEqualTo(1);
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(1L);
    assertThat(defaultCompanyId).isEqualTo(1002L);  // 仅 B
}
```

### 12.4 DEFAULT-03:并发同 default(A vs A)

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_03_concurrent_same_company() {
    // Given: u1 default = companyA
    
    CountDownLatch startLatch = new CountDownLatch(1);
    CountDownLatch endLatch = new CountDownLatch(2);
    
    CompletableFuture<Void> f1 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1001L);  // A
        } catch (Throwable t) {
        } finally {
            endLatch.countDown();
        }
    });
    CompletableFuture<Void> f2 = CompletableFuture.runAsync(() -> {
        try {
            startLatch.await();
            userCompanyService.setDefaultCompany(1L, 1001L);  // A
        } catch (Throwable t) {
        } finally {
            endLatch.countDown();
        }
    });
    
    startLatch.countDown();
    endLatch.await(5, TimeUnit.SECONDS);
    
    // Then: 最终还是 companyA=1
    int defaultCount = userCompanyMapper.countByUserIdAndIsDefault(1L, 1);
    assertThat(defaultCount).isEqualTo(1);
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(1L);
    assertThat(defaultCompanyId).isEqualTo(1001L);
}
```

### 12.5 DEFAULT-04:设置 disabled company

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_04_disabled_company() {
    // Given: u1 default = companyA, companyB 已被禁用(status=0)
    companyRepository.updateStatus(1002L, 0);
    
    // When: u1 尝试 setDefault(companyB)
    assertThatThrownBy(() -> userCompanyService.setDefaultCompany(1L, 1002L))
        .isInstanceOf(CompanyAccessDeniedException.class);
    
    // Then: 旧 default companyA=1 保持不变
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(1L);
    assertThat(defaultCompanyId).isEqualTo(1001L);
}
```

### 12.6 DEFAULT-05:setDefault 失败回滚

```java
@Test
@Transactional
@Rollback
public void test_DEFAULT_05_setDefault_failure_rollback() {
    // Given: u1 default = companyA
    
    // 模拟: 在 updateDefaultToZero 之后,setDefault 之前注入异常
    // (实际实现时可用 Spy / Mock Bean)
    doThrow(new RuntimeException("mock setDefault failure"))
        .when(userCompanyRepository).setDefault(anyLong(), anyLong());
    
    // When
    assertThatThrownBy(() -> userCompanyService.setDefaultCompany(1L, 1002L))
        .isInstanceOf(RuntimeException.class);
    
    // Then: 旧 default companyA=1 保持不变(整个事务回滚)
    Long defaultCompanyId = userCompanyMapper.selectDefaultCompanyId(1L);
    assertThat(defaultCompanyId).isEqualTo(1001L);
}
```

### 12.7 测试矩阵汇总

| 测试 | 并发 | 输入 | 预期最终 | 异常 |
|---|---|---|---|---|
| DEFAULT-01 | 是 | A→B + B→C | 仅 C=1 | 无 |
| DEFAULT-02 | 否 | A→B | 仅 B=1 | 无 |
| DEFAULT-03 | 是 | A→A + A→A | 仅 A=1 | 无 |
| DEFAULT-04 | 否 | →disabledB | companyA=1 不变 | CompanyAccessDeniedException |
| DEFAULT-05 | 否 | A→B(失败) | companyA=1 不变 | RuntimeException |

---

## §13 最终流程图

```
HTTP POST /api/auth/setDefaultCompany
    body: { newDefaultCompanyId: 1002 }
    ↓
AuthController.setDefaultCompany()
    ↓
UserCompanyService.setDefaultCompany(userId, newDefaultCompanyId)
    ↓
[Spring @Transactional 事务开始, isolation=READ_COMMITTED]
    ↓
步骤 1: SELECT * FROM user WHERE id = #{userId} FOR UPDATE
    ├─ user == null → UserNotFoundException → [ROLLBACK]
    └─ user.status != 1 → UserDisabledException → [ROLLBACK]
    ↓
步骤 2: SELECT COUNT(*) FROM user_company WHERE user_id=? AND company_id=? AND status=1
    └─ count == 0 → CompanyAccessDeniedException("无权限") → [ROLLBACK]
    ↓
步骤 3: SELECT * FROM company WHERE id = #{newDefaultCompanyId}
    ├─ company == null → CompanyAccessDeniedException("company 不存在") → [ROLLBACK]
    └─ company.status != 1 → CompanyAccessDeniedException("company 不可用") → [ROLLBACK]
    ↓
步骤 4: UPDATE user_company SET is_default=0 WHERE user_id=? AND is_default=1
    ↓
步骤 5: UPDATE user_company SET is_default=1 WHERE user_id=? AND company_id=?
    ├─ affected != 1 → IllegalStateException → [ROLLBACK]
    └─ affected == 1 → 继续
    ↓
步骤 6: SELECT COUNT(*) FROM user_company WHERE user_id=? AND is_default=1
    └─ count > 1 → IllegalStateException("发现多条 default") → [ROLLBACK]
    ↓
[事务自动 COMMIT]
    ↓
[释放 user.id 行锁]
    ↓
返回 Result.success()
```

---

## §14 死锁处理细则(防御性)

### 14.1 主结论:不可能死锁

§7 已分析:**单行锁 + READ_COMMITTED + 主键索引** → 死锁**不可能**。

### 14.2 防御性建议(可选,不强制)

```java
@Service
public class UserCompanyServiceImpl implements UserCompanyService {
    
    @Retryable(
        value = {CannotAcquireLockException.class, DeadlockLoserDataAccessException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 100, multiplier = 2)
    )
    @Override
    public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
        // ... 事务逻辑
    }
}
```

**说明**:
- @Retryable 防御性:即使出现极端锁竞争,也自动重试
- 重试 3 次,backoff 100ms/200ms/400ms
- **不**强制要求(241V2A-1 仅推荐,非强制)

### 14.3 锁等待超时配置

`my.cnf` / `application.yml`:
```yaml
spring.datasource:
  hikari:
    maximum-pool-size: 20
    connection-timeout: 30000
# MySQL 配置(由 DBA 决定):
# innodb_lock_wait_timeout = 50  (默认 50 秒)
```

V4.4 不显式修改 innodb_lock_wait_timeout,沿用默认值。

---

## §15 与 241V2 / 241V2A 关系

### 15.1 三者关系

| 文档 | 定位 | 关系 |
|---|---|---|
| **241V2** | V4.4 基础设施设计修正版(原始)| 基础 |
| **241V2A** | P0-2 强制 companyId 覆盖补丁 | 241V2 补丁(覆盖 §7.2 写法) |
| **241V2A-1** | **defaultCompany 并发控制补充裁决** | 241V2 补丁(补充 §12.3 并发) |

### 15.2 三者**不互相覆盖成不一致版本**

- 241V2 §7.2 代码(已被 241V2A §3.1 替代)
- 241V2 §12.3 文字(被 241V2A-1 §4 / §5 / §6 强化,但**不**作废)
- 241V2 §12.6 IGNORE_TABLES(241V2A-1 不修改)
- 241V2 §6 IGNORE_TABLES(241V2A-1 不修改)

### 15.3 241V2A-1 增量(相比 241V2)

| 241V2 §12.3 内容 | 241V2A-1 增量 |
|---|---|
| defaultCompanyId 归属 user_company.is_default | 沿用 |
| 应用层保证唯一性 | 升级为"事务 + user 行锁" |
| @Transactional 原子更新 | 扩展为 7 步完整事务 |
| 锁对象 | **新增** = `user.id` 单行 |
| 锁顺序 | **新增** = 单一 user 行,无顺序问题 |
| 异常回滚 | **新增** = @Transactional(rollbackFor=Exception) |
| 死锁分析 | **新增** = 单行锁免疫 |
| 6 个并发场景 | **新增** |
| "无 default" 语义 | **新增** = 允许 0 个 |
| CompanyContext 关系 | **新增** = defaultCompanyId ≠ 当前请求 companyId |
| DEFAULT-01~05 测试 | **新增** |

### 15.4 三者不能互改

- 241V2A-1 **不得**修改 241V2 §12.3 文字(避免覆盖)
- 241V2A-1 通过"补丁叠加"建立增量关系
- 后续审计 241A-1 必须**同时读 241V2 + 241V2A + 241V2A-1**

---

## §16 S1-169-2 启动闸门(241V2A-1 不变)

### 16.1 启动闸门硬条件

| 闸门 | 状态 | 来源 |
|---|:-:|---|
| 240 Q4 架构 commit | ✓ | `6efa0da` |
| 241V2 修复 4 P0 + 1 P1 | ✓ | 241V2 |
| 241V2A P0-2 真闭环 | ✓ | 241V2A |
| **241V2A-1 defaultCompany 并发控制**(本文件) | **✓** | **本文件** |
| **241A-1 独立盲审 PASS(下一轮)** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 16.2 241A-1 审计 241V2A-1 必须检查

1. ✓ 锁对象 = `user.id` 单行
2. ✓ 事务边界 = 7 步完整 @Transactional
3. ✓ 死锁分析 = 单行锁免疫
4. ✓ 6 个并发场景结果矩阵
5. ✓ "无 default" 语义 = 允许 0 个
6. ✓ defaultCompanyId ≠ 当前请求 companyId
7. ✓ DEFAULT-01~05 测试设计完整
8. ✓ 数据模型不需要修改(沿用 241V2 §12.1)
9. ✓ 与 241V2 / 241V2A 关系明确(补丁叠加)

### 16.3 严禁(241V2A-1 边界)

- ✗ **不得**修改 241V2 / 241V2A / 任何历史 MD
- ✗ **不得**创建 backend/ / 写 Java / 创建 SQL
- ✗ **不得**在 241A-1 PASS 前进入 S1-169-2
- ✗ **不得**把 241V2A-1 + 241A-1 审计合并
- ✗ **不得**自评 PASS

---

## §17 报告统计

- 报告字节数:约 32000 字节
- 章节数:20
- 冻结的并发控制方案:方案 A(锁 user 单行)
- 冻结的锁对象:`user.id`
- 冻结的事务边界:7 步完整 @Transactional
- 冻结的隔离级别:READ_COMMITTED
- 冻结的异常处理:rollbackFor=Exception
- 冻结的死锁分析:单行锁免疫
- 6 个并发场景结果矩阵:全部冻结
- "无 default company" 语义:允许 0 个(方案 B)
- 5 项 DEFAULT 测试:DEFAULT-01~05
- 新增的 Service 方法:0(强化现有)
- 新增的 Mapper SQL:4(selectByIdForUpdate / updateDefaultToZero / setDefault / countByUserIdAndCompanyId)
- DDL 修改:0(沿用 241V2 §12.1)
- 与 241V2 关系:补丁叠加(不覆盖)
- 启动闸门:全部满足
- 下一轮交付物:241A-1 独立盲审(必须同时审计 241V2 + 241V2A + 241V2A-1)

---

## §18 正式裁决矩阵(241V2A-1 冻结)

| 项目 | 现状 | 241V2A-1 最终裁决 |
|---|---|---|
| default 字段位置 | user_company.is_default | 保持 |
| 唯一 user-company 关系 | UNIQUE(user_id, company_id) | 保持 |
| default 唯一性 | 应用层事务(241V2 §12.3 写法)| 升级为"事务 + user 行锁" |
| **锁对象** | 未冻结 | **`user.id` 单行(SELECT ... FOR UPDATE)** |
| 锁顺序 | 未冻结 | 单一 user 行,无顺序问题(无死锁)|
| **事务边界** | @Transactional(241V2 草写) | **7 步完整 @Transactional(rollbackFor=Exception, isolation=READ_COMMITTED)** |
| **rollback** | 未详细说明 | **任何 Exception → 自动 rollback** |
| **死锁处理** | 未冻结 | **单行锁免疫,无需死锁处理** |
| **DEFAULT-01** | 未存在 | **新增(并发不同 company,后到者赢)** |
| **DEFAULT-02** | 未存在 | **新增(串行 A → B)** |
| **DEFAULT-03** | 未存在 | **新增(并发同 company,幂等)** |
| **DEFAULT-04** | 未存在 | **新增(设置 disabled,CompanyAccessDeniedException,回滚)** |
| **DEFAULT-05** | 未存在 | **新增(setDefault 失败,整个事务回滚)** |
| **"无 default" 语义** | 未明确 | **允许 0 个(方案 B),并发一致性由本裁决保证** |
| **与 CompanyContext 关系** | 未明确 | **defaultCompanyId ≠ 当前请求 companyId** |
| DDL 修改 | 241V2 §12.1 已冻结 | **保持 0 修改** |
| 与 241V2 关系 | 基础 | **补丁叠加(不覆盖 §12.3 文字)** |
| 与 241V2A 关系 | P0-2 补丁 | **互不冲突(本裁决不动 §7.2 主题)** |
| 启动闸门 | 沿用 | **P0=0, P1=0(待 241A-1 验证)** |

---

## §19 总结判断(241V2A-1 裁决)

**【241V2A-1 补充裁决完成】**

**【尚未经过独立盲审】**

当前:**S1-169-2 = BLOCK**

下一步:执行 241A-1 独立盲审,审计范围必须**同时**覆盖:
- 241V2
- 241V2A
- 241V2A-1

重点确认:
- P0 = 0
- P1 = 0
- 并发控制真闭环
- 锁对象 / 事务边界 / 死锁 / 6 场景 / 5 测试 全部冻结

---

## §20 Git 状态(本轮结束)

- **HEAD 不变**:`6efa0daecd386eb022bd4ac1065e4b08ed529dc1`
- **本轮不 commit / 不 push** ✓
- **0 号闸门 4 文件 SHA256 锁定不变** ✓
- **历史 MD(190~241V2A 共 62 份)未修改** ✓
- **VisionCare PMS 任何文件未修改** ✓
- **新文件**:`241V2A-1_S1-169-1_defaultCompany并发控制补充裁决.md`(本文件,untracked)
- **本文件不实际写 Java / 不创建 SQL / 不执行 DDL / 不连接数据库** ✓
- **本文件不修改 241V2 / 241V2A / 任何历史 MD** ✓
- **本文件不修改 pom.xml / application.yml** ✓

### 20.1 241V2A-1 自身 SHA256(下次审计基准)

待写入后由 `Get-FileHash` 验证,本文件最终 SHA256 = `[待 241A-1 审计时计算]`。

---

## §21 一句话最终判断

> **241V2A-1 defaultCompany 并发控制补充裁决完成**:在 241V2 §12.3 应用层原子更新基础上,把 defaultCompanyId 唯一性**完整冻结为"悲观行锁 + 完整事务"**——锁对象 = `user.id` 单行(`SELECT ... FOR UPDATE`,主键索引,无死锁,跨 user 完美并行);事务边界 = 7 步完整 `@Transactional(rollbackFor=Exception, isolation=READ_COMMITTED)`:锁 user 行 → 验证 user 状态 → 验证 target 权限 → 验证 target company 状态 → 现有 default 清零 → 设置新 default → 防御性最终验证;任何 Exception 触发自动 rollback;不选"锁 user_company 多行"(易死锁)、不选"乐观锁"(与 240 风格不符)、不选"MySQL 部分 UNIQUE"(不支持);6 个并发场景结果矩阵(并发不同 / 并发同 / A 失败 B 成功 / disabled company / 无权限 / 重复设置)全部冻结;"无 default company" 语义 = **允许 0 个**(方案 B,业务层规则留待后续);defaultCompanyId ≠ 当前请求 companyId(显式契约);DEFAULT-01~05 五项并发测试完整设计(关键 DEFAULT-01 验证"并发不同 company,最终最多 1 条 default");DDL **保持 0 修改**(沿用 241V2 §12.1 冻结);与 241V2 / 241V2A 关系 = 补丁叠加不覆盖;S1-169-2 仍 BLOCK,**未自评 PASS**,等待 241A-1 独立盲审同时审计 241V2 + 241V2A + 241V2A-1 三者。

---

## §22 报告统计

- 报告字节数:约 32000 字节
- 章节数:22
- 冻结的并发控制方案:方案 A(锁 user 单行)
- 锁对象:`user.id` 单行
- 事务边界:7 步完整 @Transactional
- 隔离级别:READ_COMMITTED
- 6 场景结果矩阵:全部冻结
- 5 项 DEFAULT 测试:DEFAULT-01~05
- DDL 修改:0
- 启动闸门:P0=0, P1=0(待 241A-1 验证)
- 下一轮:241A-1 独立盲审(同时审计 241V2 + 241V2A + 241V2A-1)
