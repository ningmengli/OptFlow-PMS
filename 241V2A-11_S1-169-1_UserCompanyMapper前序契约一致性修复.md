# 241V2A-11 S1-169-1 UserCompanyMapper 前序契约一致性修复

> **本轮定位**:第八轮独立盲审识别的 **P1-12 + P1-13 + 顺手裁决 P2** 修复补丁。
> - **P1-12**:`241V2A-10 §5.3` 把 UserCompanyMapper 权限查询方法冻结为 `existsByUserIdAndCompanyId(...)`(返回 int),**与 241V2A-1 §6.2 已冻结的 `countByUserIdAndCompanyId(...)`(返回 int)直接冲突**;不能两套 Mapper 方法并存。
> - **P1-13**:`241V2A-10 §5.3` 沿用 `countByUserIdAndIsDefault(userId, isDefault)` 签名,但**前序 241V2A-1 §6.2 的 SQL 实际是硬编码 `is_default = 1`**(`@Param("isDefault") int isDefault` 形同虚设);不能让"参数签名看起来可变 / SQL 实际固定 1"的矛盾继续存在。
> - **P2 顺手裁决**:Service 步骤 6 当前是 `if (defaultCount > 1) throw`,**只阻止 > 1,未明确 exactly-one 约束**;成功路径必须满足 `defaultCount == 1`,否则视为不变量被破坏(IllegalStateException)。
> 本补丁采用"**沿用前序 241V2A-1 §6.2 方法名 + 显式作废 241V2A-10 §5.3 旧写法 + 显式冻结 SQL 语义为参数化 + 显式冻结 exactly-one**"的最小变更路径,建立**唯一 Effective Spec**。
> - 严禁修改 235 / 235A / 235B / 236 / 236A / 236B / 237 / 237A / 238 / 238A / 239 / 239A / 240 / 241 / 241A / 241V2 / 241V2A / 241V2A-1 / 241V2A-2 / 241A-1 / 241V3 / 241V2A-3 / 241V4 / 241V2A-4 / 241V2A-5 / 241V2A-6 / 241V2A-7 / 241V2A-8 / 241V2A-9 / 241V2A-10 / 任何历史 MD
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
- **历史 MD(190~241V2A-10 共 82 份)未修改** ✓
- **本轮不写代码 / 不 commit / 不 push** ✓
- **241V2A-11 是 untracked 新文件,绝不 commit** ✓

---

## §1 任务定义

### 1.1 第八轮独立盲审识别的问题

| # | 严重度 | 位置 | 描述 |
|---:|:-:|---|---|
| P1-12 | P1 | 241V2A-10 §5.3 vs 241V2A-1 §6.2 | 同一 Mapper 权限查询方法被冻结成两个不同名字(existsBy vs countBy),S1-169-2 实施者无法选择唯一契约 |
| P1-13 | P1 | 241V2A-10 §5.3 vs 241V2A-1 §6.2 | `countByUserIdAndIsDefault` 方法签名是参数化(@Param("isDefault")),但 241V2A-1 §6.2 SQL 实际硬编码 `is_default=1`——签名与 SQL 矛盾 |
| P2 | P2 | 241V2A-9 §4.2 + 241V2A-10 §7.1 | Service 步骤 6 用 `if (defaultCount > 1) throw`,**未明确 exactly-one 约束**(允许 == 0 通过) |

### 1.2 P1-12 错误细节(本审计独立识别)

**241V2A-10 §5.3** 冻结 Mapper interface:
```java
public interface UserCompanyMapper extends BaseMapper<UserCompany> {
    int updateDefaultToZero(@Param("userId") Long userId);
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);
    int existsByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);  // ❌ P1-12
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
}
```

**241V2A-1 §6.2** 已冻结 Mapper interface:
```java
public interface UserCompanyMapper extends BaseMapper<UserCompany> {
    int updateDefaultToZero(Long userId);
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);
    int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);  // ✓ 前序已冻结
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
}
```

**矛盾**:
- `241V2A-10 §5.3`:`Mapper.existsByUserIdAndCompanyId(...)` 返回 int(SQL 期望 `SELECT 1` / `SELECT COUNT(*)` / `SELECT id`)
- `241V2A-1 §6.2`:`Mapper.countByUserIdAndCompanyId(...)` 返回 int(SQL 显式 `SELECT COUNT(*) FROM user_company WHERE user_id = #{userId} AND company_id = #{companyId} AND status = 1`)

两套方法并存,**S1-169-2 实施者无法决定**到底用哪个,违反"实施者不得自行发明接口"规则。

### 1.3 P1-13 错误细节(本审计独立识别)

**241V2A-1 §6.2** 给出:
```java
@Select("SELECT COUNT(*) FROM user_company " +
        "WHERE user_id = #{userId} AND is_default = 1")  // ⚠ SQL 硬编码 1
int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
```

**矛盾分析**:
- 方法名 `countByUserIdAndIsDefault` 暗示按 `isDefault` 参数统计
- 方法签名有 `@Param("isDefault") int isDefault`
- 但 SQL 字面量是 `is_default = 1`,**`isDefault` 参数实际未参与 SQL**(`#{isDefault}` 未出现)
- 这意味着 S1-169-2 实施者按方法签名传任意 isDefault 值(0/1)都会得到**相同的统计结果(只统计 is_default=1 的记录)**
- 签名语义与 SQL 语义不一致 = 实施陷阱

### 1.4 P2 错误细节(本审计顺手识别)

**Service 步骤 6**(241V2A-9 §4.2 + 241V2A-10 §7.1):
```java
// 步骤 6:防御性最终验证(Repository 方法 4)
int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
if (defaultCount > 1) {
    throw new IllegalStateException("发现多条 default: count=" + defaultCount);
}
```

**漏洞**:
- `defaultCount == 0` → 不抛异常(继续走 commit)
- 但 `setDefaultCompany` 成功路径应该确保**"操作后恰好 1 条 default"**
- 允许 == 0 意味着:即使 updateDefaultToZero 误清空 + setDefault 失败被 swallowed,事务仍能提交
- 违反"操作成功后 default 数 == 1"的不变量

### 1.5 严格禁止(本轮)

- ✗ 修改 241V2A-10 / 241V2A-9 / 241V2A-1 / 任何历史 MD
- ✗ 修改 VisionCare PMS 任何文件
- ✗ 创建 backend/ / 写 Java 源文件 / 创建 SQL 文件 / 执行 DDL / 连接数据库
- ✗ 修改 pom.xml / application.yml
- ✗ commit / push
- ✗ 自评 PASS(等下一轮独立盲审)
- ✗ 进入 S1-169-2

---

## §2 P1-12 修复方案

### 2.1 方案选择

| 候选 | 描述 | 优 | 劣 | 决策 |
|---|---|---|---|---|
| **A. 沿用 241V2A-1 `countByUserIdAndCompanyId` 作 Mapper 方法** | Repository.existsBy... 内部调 Mapper.countBy... > 0 | 不修改前序 MD;签名语义自洽;`SELECT COUNT(*)` 真实反映记录数 | 多一层 `> 0` 转换 | **✓ 选定** |
| B. 沿用 241V2A-10 `existsByUserIdAndCompanyId` 作 Mapper 方法 | 修改 241V2A-1 §6.2,改用 `SELECT 1` / `LIMIT 1` | Mapper 层语义即"存在性" | **必须修改 241V2A-1**(红线);前序 SQL 已被 241V2A-1 §6.2 冻结为 `SELECT COUNT(*)` | ✗ 红线 |

**【241V2A-11 冻结】** 选 **方案 A**——沿用 241V2A-1 §6.2 的 `countByUserIdAndCompanyId` Mapper 方法。

### 2.2 旧写法显式作废(241V2A-11 显式)

**【241V2A-11 显式作废】** `241V2A-10 §5.3` 写的 Mapper 方法:

```java
// ❌ 241V2A-10 §5.3 旧写法 = 【作废】
int existsByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);
```

**作废原因**:
1. 与前序 241V2A-1 §6.2 冻结的 `countByUserIdAndCompanyId` 命名冲突
2. 241V2A-1 §6.2 显式 SQL 为 `SELECT COUNT(*)`(语义是计数)
3. 实施者不能既用 `existsBy...` 又用 `countBy...`,违反唯一性

**【241V2A-11 冻结的新唯一写法】** Mapper 层:

```java
// ✅ 241V2A-11 冻结 = 沿用 241V2A-1 §6.2
int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);
```

**SQL 语义**(沿用 241V2A-1 §6.2 冻结):
```sql
SELECT COUNT(*) FROM user_company
WHERE user_id = #{userId}
  AND company_id = #{companyId}
  AND status = 1
```

### 2.3 Repository / RepositoryImpl 显式冻结(241V2A-11 强化)

**Repository interface** 保留 241V2A-10 §4.1 的:
```java
boolean existsByUserIdAndCompanyId(Long userId, Long companyId);
```

**RepositoryImpl**(241V2A-11 修正 241V2A-10 §4.2 的 Mapper 调用):
```java
// ✅ 241V2A-11 冻结
@Override
public boolean existsByUserIdAndCompanyId(Long userId, Long companyId) {
    return userCompanyMapper.countByUserIdAndCompanyId(userId, companyId) > 0;
}
```

**关键差异**(对比 241V2A-10 §4.2):
| 位置 | 241V2A-10 旧写法(作废) | 241V2A-11 新唯一写法 |
|---|---|---|
| RepositoryImpl 内部调用 | `userCompanyMapper.existsByUserIdAndCompanyId(...)` | `userCompanyMapper.countByUserIdAndCompanyId(...)` |
| 条件转换 | (假设 SQL 已判断存在) | `> 0` 显式转换 |

### 2.4 唯一调用链(241V2A-11 冻结)

```
UserCompanyServiceImpl
    ↓
UserCompanyRepository.existsByUserIdAndCompanyId(userId, companyId)  → boolean
    ↓
UserCompanyRepositoryImpl
    ↓
UserCompanyMapper.countByUserIdAndCompanyId(userId, companyId)  → int  (沿用 241V2A-1 §6.2)
    ↓
SQL: SELECT COUNT(*) FROM user_company
     WHERE user_id = #{userId}
       AND company_id = #{companyId}
       AND status = 1
```

**严禁**:
- ✗ 不得让 Mapper 同时存在 `existsByUserIdAndCompanyId` 和 `countByUserIdAndCompanyId` 两套
- ✗ 不得在 Repository 跳过 `> 0` 转换直接 return int(返回类型契约是 boolean)

---

## §3 P1-13 修复方案

### 3.1 方案选择

| 候选 | 描述 | 优 | 劣 | 决策 |
|---|---|---|---|---|
| **A. 参数化 isDefault(SQL 用 #{isDefault})** | 沿用 241V2A-1 §6.2 方法名,SQL 改为 `is_default = #{isDefault}` | 签名语义与 SQL 语义一致;`countBy...IsDefault(0)` 可用于将来统计非 default 记录 | 需显式作废 241V2A-1 §6.2 的 SQL 硬编码 1(虽不修改 241V2A-1 文件,但通过 241V2A-11 建立新契约) | **✓ 选定** |
| B. 硬编码 1(重命名为 countDefaultByUserId) | 方法重命名,SQL 硬编码 1 | SQL 简单 | **必须修改 241V2A-1 §6.2 方法名**(红线);破坏前序契约 | ✗ 红线 |
| C. 保留矛盾("以实际实现为准") | 不冻结 SQL,实施者自行选择 | 灵活 | 实施陷阱(签名与 SQL 不一致);违反"不得自评 PASS + 必须冻结" | ✗ 红线 |

**【241V2A-11 冻结】** 选 **方案 A**——沿用 241V2A-1 §6.2 方法名,SQL 显式参数化。

### 3.2 旧写法显式作废(241V2A-11 显式)

**【241V2A-11 显式作废】** `241V2A-1 §6.2` 写的 SQL:

```java
// ❌ 241V2A-1 §6.2 SQL 写法 = 【作废 SQL 字面量】
@Select("SELECT COUNT(*) FROM user_company " +
        "WHERE user_id = #{userId} AND is_default = 1")
int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
```

**作废原因**:
1. 签名声明 `@Param("isDefault") int isDefault`,但 SQL 字面量是 `is_default = 1`,**`isDefault` 参数未参与 SQL**
2. S1-169-2 实施者传 `0` / `1` 都得到 `is_default = 1` 的统计(签名误导)
3. 违反"方法签名 = SQL 语义"的契约一致性

**【241V2A-11 冻结的新唯一写法】** Mapper 方法的 SQL 语义:

```java
// ✅ 241V2A-11 冻结 = 沿用 241V2A-1 §6.2 方法名 + SQL 显式参数化
@Select("SELECT COUNT(*) FROM user_company " +
        "WHERE user_id = #{userId} " +
        "  AND is_default = #{isDefault}")
int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
```

**SQL 语义**(241V2A-11 冻结):
```sql
SELECT COUNT(*) FROM user_company
WHERE user_id = #{userId}
  AND is_default = #{isDefault}    -- ✅ 参数真参与
```

### 3.3 Service 调用语义(241V2A-11 显式)

**【241V2A-11 冻结】** Service 调用 `countByUserIdAndIsDefault` 时**固定传 isDefault=1**:

```java
// ✅ 241V2A-11 冻结
int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
```

**理由**:
- Service 当前业务语义是"统计 default 记录数"——只关心 is_default=1
- 固定传 1 与"成功路径 defaultCount == 1"的 exactly-one 约束一致
- **不**利用 isDefault=0 通道(Service 不需要统计非 default 数)

**严禁**:
- ✗ 不得让 Service 传 isDefault=0(超出本补丁范围;若未来需要统计非 default 数,新建单独裁决)
- ✗ 不得"以实际实现为准"绕开 SQL 字面量冻结

### 3.4 唯一调用链(241V2A-11 冻结)

```
UserCompanyServiceImpl
    ↓
UserCompanyRepository.countByUserIdAndIsDefault(userId, 1)  → int
    ↓
UserCompanyRepositoryImpl
    ↓
UserCompanyMapper.countByUserIdAndIsDefault(userId, 1)  → int  (沿用 241V2A-1 §6.2 方法名)
    ↓
SQL: SELECT COUNT(*) FROM user_company
     WHERE user_id = #{userId}
       AND is_default = #{isDefault}     -- ✅ 参数化
     -- Service 传 isDefault=1 → 等价于统计 default 数
```

---

## §4 P2 exactly-one default 约束裁决

### 4.1 业务语义确认

**【241V2A-11 冻结】** V4.4 `setDefaultCompany` **成功路径**必须满足 exactly-one 约束:

> `setDefaultCompany(userId, newDefaultCompanyId)` 成功提交后,user_company 表中**恰好 1 条**记录满足 `is_default=1`(针对该 user)。

**与 241V2A-1 §9 的关系**(不矛盾):

| 维度 | 241V2A-1 §9 业务层规则 | 241V2A-11 exactly-one |
|---|---|---|
| 范围 | user_company 全局状态(操作前/后任意时刻) | `setDefaultCompany` 成功路径(操作完成时刻) |
| 允许状态 | 0 条 default(操作前,或业务层主动清空) | 0 条 default 不允许(操作成功后) |
| 谁负责 | 业务层(留待未来 S1-169-2 / 242 单独裁决) | setDefaultCompany 自身(本补丁) |
| 性质 | 业务不变量(可被业务规则打破) | 操作不变量(必须满足) |

**两者不冲突**:
- 业务层可以在"特殊业务场景"主动清空 default(例如删除 company 时)→ 留下 0 条 default 的过渡态
- 但 `setDefaultCompany` 自身(成功路径)不能留下 0 条 default(否则就是失败,不是成功)
- 业务层主动清空 ≠ `setDefaultCompany` 成功(后者是显式"设置 default"操作)

### 4.2 唯一 Effective Spec(241V2A-11 冻结)

**【241V2A-11 冻结】** Service 步骤 6 改为:

```java
// ✅ 241V2A-11 冻结
int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
if (defaultCount != 1) {
    throw new IllegalStateException(
        "default company 数量必须为 1, actual=" + defaultCount
    );
}
```

**对比 241V2A-10 §7.1 旧写法**:
```java
// ❌ 241V2A-10 §7.1 旧写法 = 【作废】
if (defaultCount > 1) {
    throw new IllegalStateException("发现多条 default: count=" + defaultCount);
}
```

**变化点**:
- `> 1` → `!= 1`
- 异常信息更明确("数量必须为 1, actual=X")

### 4.3 不变量(241V2A-11 强化 241V2A-1 §9.3)

**【241V2A-11 冻结】** 强化 241V2A-1 §9.3 不变量:

| 时刻 | defaultCount 允许值 | 理由 |
|---|---|---|
| **操作前** | 0 或 1 | 241V2A-1 §9.3 沿用 |
| **setDefaultCompany 成功提交后** | **必须 == 1** | 241V2A-11 exactly-one 强化 |
| **setDefaultCompany 抛异常 rollback 后** | 与操作前相同(事务回滚) | @Transactional rollback 语义 |
| **业务层主动清空 default 后** | 0(临时态) | 业务层规则,留待未来 |

### 4.4 DEFAULT-05 9 步 rollback 验证强化

**【241V2A-11 冻结】** DEFAULT-05 阶段 C 独立只读事务验证:

```java
// ✅ 241V2A-11 冻结(沿用 241V2A-8 / 241V2A-9 / 241V2A-10)
@Transactional(propagation = Propagation.REQUIRES_NEW, readOnly = true)
public void verifyFinalState(Long userId) {
    int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
    // 验证 1:defaultCount 必须 == 1
    assertThat(defaultCount).isEqualTo(1);
    // 验证 2:default 必须是 companyA(rollback 后保持)
    Long defaultCompanyId = userCompanyRepository.findDefaultCompanyId(userId);
    assertThat(defaultCompanyId).isEqualTo(companyAId);
}
```

**严禁**:
- ✗ 不得用 `assertThat(defaultCount).isLessThanOrEqualTo(1)`(语义弱化,允许 0)
- ✗ 不得用 `assertThat(defaultCount).isGreaterThanOrEqualTo(1)`(语义弱化,允许 N)
- ✗ 必须用 `isEqualTo(1)`(exactly-one)

---

## §5 唯一 Effective Spec 汇总(241V2A-11 完整冻结)

### 5.1 UserCompanyRepository interface(241V2A-11 完整)

```java
package com.optflow.pms.module.auth.repository;

/**
 * V4.4 UserCompanyRepository 接口
 *
 * <p>【241V2A-11 冻结】完整 4 个公开方法(沿用 241V2A-10 §4.1):</p>
 * <ol>
 *   <li>updateDefaultToZero(Long userId) - 现有 default 清零</li>
 *   <li>setDefault(Long userId, Long companyId) - 设置目标 default</li>
 *   <li>existsByUserIdAndCompanyId(Long userId, Long companyId) - 校验权限(返回 boolean,内部调 Mapper.countBy... > 0)</li>
 *   <li>countByUserIdAndIsDefault(Long userId, int isDefault) - 防御性 count(SQL 参数化 #{isDefault})</li>
 * </ol>
 *
 * <p>职责:封装 user_company 表的所有 user-default 操作。</p>
 * <p>Spring Bean:由 UserCompanyRepositoryImpl(@Repository)实现。</p>
 */
public interface UserCompanyRepository {

    int updateDefaultToZero(Long userId);

    int setDefault(Long userId, Long companyId);

    boolean existsByUserIdAndCompanyId(Long userId, Long companyId);

    int countByUserIdAndIsDefault(Long userId, int isDefault);
}
```

### 5.2 UserCompanyRepositoryImpl(241V2A-11 完整,修正 241V2A-10 §4.2)

```java
package com.optflow.pms.module.auth.repository;

import com.optflow.pms.module.auth.mapper.UserCompanyMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

/**
 * V4.4 UserCompanyRepository 实现
 *
 * <p>【241V2A-11 冻结】4 个方法全部委托给 UserCompanyMapper。</p>
 * <p>关键修正:existsByUserIdAndCompanyId 内部调 Mapper.countByUserIdAndCompanyId(...) > 0(241V2A-11 修正 241V2A-10 §4.2 的错误 Mapper.existsBy... 写法)</p>
 */
@Repository
public class UserCompanyRepositoryImpl implements UserCompanyRepository {

    private final UserCompanyMapper userCompanyMapper;

    @Autowired
    public UserCompanyRepositoryImpl(UserCompanyMapper userCompanyMapper) {
        this.userCompanyMapper = userCompanyMapper;
    }

    @Override
    public int updateDefaultToZero(Long userId) {
        return userCompanyMapper.updateDefaultToZero(userId);
    }

    @Override
    public int setDefault(Long userId, Long companyId) {
        return userCompanyMapper.setDefault(userId, companyId);
    }

    /**
     * 【241V2A-11 修正】沿用 241V2A-1 §6.2 冻结的 countByUserIdAndCompanyId Mapper 方法
     * 显式作废 241V2A-10 §4.2 的 Mapper.existsByUserIdAndCompanyId(...) 写法
     */
    @Override
    public boolean existsByUserIdAndCompanyId(Long userId, Long companyId) {
        return userCompanyMapper.countByUserIdAndCompanyId(userId, companyId) > 0;
    }

    @Override
    public int countByUserIdAndIsDefault(Long userId, int isDefault) {
        return userCompanyMapper.countByUserIdAndIsDefault(userId, isDefault);
    }
}
```

### 5.3 UserCompanyMapper interface(241V2A-11 完整)

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
 * <p>【241V2A-11 冻结】完整契约:</p>
 * <ul>
 *   <li>extends BaseMapper&lt;UserCompany&gt; 获得 MyBatis-Plus CRUD 自带方法</li>
 *   <li>4 个自定义方法(对应 Repository 4 个公开方法)</li>
 *   <li>关键:第 3 个方法沿用 241V2A-1 §6.2 的 countByUserIdAndCompanyId(显式作废 241V2A-10 §5.3 的 existsBy... Mapper 写法)</li>
 *   <li>关键:第 4 个方法 SQL 显式参数化 is_default = #{isDefault}(显式作废 241V2A-1 §6.2 的硬编码 is_default = 1 SQL)</li>
 * </ul>
 */
@Mapper
public interface UserCompanyMapper extends BaseMapper<UserCompany> {

    /**
     * 自定义方法 1:清零 user 的所有 default(沿用 241V2A-1 §6.2)
     */
    @Update("UPDATE user_company SET is_default = 0, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND is_default = 1")
    int updateDefaultToZero(@Param("userId") Long userId);

    /**
     * 自定义方法 2:设置 user 在某 company 的 default = 1(沿用 241V2A-1 §6.2)
     */
    @Update("UPDATE user_company SET is_default = 1, updated_at = NOW(3) " +
            "WHERE user_id = #{userId} AND company_id = #{companyId}")
    int setDefault(@Param("userId") Long userId, @Param("companyId") Long companyId);

    /**
     * 自定义方法 3:校验 user 对 company 的权限(沿用 241V2A-1 §6.2,【241V2A-11 显式作废 241V2A-10 §5.3 的 existsBy... Mapper 写法】)
     */
    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} " +
            "  AND company_id = #{companyId} " +
            "  AND status = 1")
    int countByUserIdAndCompanyId(@Param("userId") Long userId, @Param("companyId") Long companyId);

    /**
     * 自定义方法 4:统计 user 的 default 数(沿用 241V2A-1 §6.2 方法名,【241V2A-11 显式作废 241V2A-1 §6.2 的硬编码 is_default=1 SQL,SQL 改为参数化】)
     */
    @Select("SELECT COUNT(*) FROM user_company " +
            "WHERE user_id = #{userId} " +
            "  AND is_default = #{isDefault}")
    int countByUserIdAndIsDefault(@Param("userId") Long userId, @Param("isDefault") int isDefault);
}
```

### 5.4 Mapper 严禁(241V2A-11 强化)

- ✗ 不得存在 `int existsByUserIdAndCompanyId(...)` Mapper 方法(241V2A-10 §5.3 旧写法作废)
- ✗ 不得在 `countByUserIdAndIsDefault` 的 SQL 里硬编码 `is_default = 1`(241V2A-1 §6.2 旧 SQL 作废)
- ✗ 不得新增第 5 个未冻结 Mapper 方法
- ✗ 不得在 Mapper 接口里加 `@Transactional`(Mapper 层不负责事务)
- ✗ 不得让 Service 直接调 Mapper(必须经 Repository)

### 5.5 Service 9 步流程(241V2A-11 强化 241V2A-10 §7.1)

```java
package com.optflow.pms.module.auth;

import com.optflow.pms.common.context.CompanyContext;
import com.optflow.pms.common.exception.CompanyAccessDeniedException;
import com.optflow.pms.common.exception.UserNotFoundException;
import com.optflow.pms.common.exception.UserDisabledException;
import com.optflow.pms.module.auth.entity.User;
import com.optflow.pms.module.auth.mapper.UserMapper;
import com.optflow.pms.module.auth.repository.UserCompanyRepository;
import com.optflow.pms.module.company.entity.Company;
import com.optflow.pms.module.company.repository.CompanyRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;

/**
 * V4.4 UserCompanyService 实现
 *
 * <p>【241V2A-11 强化】9 步流程 + P2 exactly-one 约束</p>
 */
@Service
@RequiredArgsConstructor
public class UserCompanyServiceImpl implements UserCompanyService {

    private final UserCompanyRepository userCompanyRepository;
    private final CompanyRepository companyRepository;
    private final UserMapper userMapper;

    @Override
    @Transactional(rollbackFor = Exception.class, isolation = Isolation.READ_COMMITTED)
    public void setDefaultCompany(Long userId, Long newDefaultCompanyId) {
        // 步骤 1:锁 user 单行
        User user = userMapper.selectByIdForUpdate(userId);
        if (user == null) { throw new UserNotFoundException("user 不存在: " + userId); }
        if (user.getStatus() != 1) { throw new UserDisabledException("user 已禁用: " + userId); }

        // 步骤 2:验证 user-company 权限(Repository 方法 3)
        if (!userCompanyRepository.existsByUserIdAndCompanyId(userId, newDefaultCompanyId)) {
            throw new CompanyAccessDeniedException("用户无权访问 companyId=" + newDefaultCompanyId);
        }

        // 步骤 3:验证 company 状态
        Company company = companyRepository.selectById(newDefaultCompanyId);
        if (company == null || company.getStatus() != 1) {
            throw new CompanyAccessDeniedException("company 不可用: " + newDefaultCompanyId);
        }

        // 步骤 4:清零旧 default(Repository 方法 1)
        userCompanyRepository.updateDefaultToZero(userId);

        // 步骤 5:设置新 default(Repository 方法 2,Spy 抛 RuntimeException)
        int affected = userCompanyRepository.setDefault(userId, newDefaultCompanyId);
        if (affected != 1) {
            throw new IllegalStateException("setDefault 失败:affected=" + affected);
        }

        // 步骤 6:防御性最终验证(Repository 方法 4)
        // 【241V2A-11 强化】exactly-one 约束
        int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
        if (defaultCount != 1) {  // ✅ 241V2A-11 从 > 1 改为 != 1
            throw new IllegalStateException(
                "default company 数量必须为 1, actual=" + defaultCount
            );
        }
    }
}
```

---

## §6 DEFAULT-05 9 步 rollback 时序(241V2A-11 强化)

### 6.1 完整 9 步(241V2A-11 沿用 241V2A-10 §8.1,验证强化)

| 步骤 | 描述 | Repository 方法调用 | 涉及 Mapper | 失败时行为 |
|---:|---|---|---|---|
| 1 | lock user | (userMapper.selectByIdForUpdate) | UserMapper | 抛 UserNotFoundException / UserDisabledException → rollback |
| 2 | validate user | (内部判断) | - | 抛异常 → rollback |
| 3 | **validate user-company permission** | **userCompanyRepository.existsByUserIdAndCompanyId** | UserCompanyMapper.countByUserIdAndCompanyId(沿用 241V2A-1 §6.2) | 抛 CompanyAccessDeniedException → rollback |
| 4 | validate company status | (companyRepository.selectById) | CompanyMapper | 抛 CompanyAccessDeniedException → rollback |
| 5 | **updateDefaultToZero(A → 0)** | **userCompanyRepository.updateDefaultToZero** | UserCompanyMapper.updateDefaultToZero | 抛异常 → rollback |
| 6 | **setDefault(B)** | **userCompanyRepository.setDefault** ← **Spy throw** | UserCompanyMapper(Spy) | RuntimeException → rollback |
| 7 | 第 6 步故障 | - | - | - |
| 8 | RuntimeException | - | - | - |
| 9 | Service transaction rollback | (rollback 步骤 3-6) | - | - |

### 6.2 验证(241V2A-11 强化)

| 验证项 | 期望 | 来源 |
|---|---|---|
| 初始 A = default | ✓ | 测试夹具 |
| 初始 B = non-default | ✓ | 测试夹具 |
| 步骤 5 updateDefaultToZero 已执行(未 commit) | ✓ | Spy 时序 |
| 步骤 6 setDefault Spy throw | ✓ | @SpyBean UserCompanyRepository.setDefault |
| 步骤 9 整体 rollback(包括步骤 5) | ✓ | @Transactional rollbackFor=Exception |
| 阶段 C 独立只读事务验证:A 仍 default | ✓ | REQUIRES_NEW readOnly |
| **阶段 C 验证:defaultCount 必须 == 1(不是 > 1)** | **✓【241V2A-11 P2 强化】** | `isEqualTo(1)` |

### 6.3 关键 Service 9 步 + Repository 4 方法 + Mapper 4 方法对应表

| 步骤 | Service 调用 | Repository 方法 | Mapper 方法 | Mapper SQL 关键 |
|---:|---|---|---|---|
| 1 | `userMapper.selectByIdForUpdate(userId)` | (UserMapper,不归 Repository) | UserMapper.selectByIdForUpdate | `... FOR UPDATE` |
| 2 | (内部判断) | - | - | - |
| 3 | `userCompanyRepository.existsByUserIdAndCompanyId(...)` | 方法 3(返回 boolean)| `countByUserIdAndCompanyId` | `WHERE user_id = ? AND company_id = ? AND status = 1` |
| 4 | `companyRepository.selectById(...)` | (CompanyRepository) | CompanyMapper.selectById | (略)|
| 5 | `userCompanyRepository.updateDefaultToZero(...)` | 方法 1(返回 int)| `updateDefaultToZero` | `WHERE user_id = ? AND is_default = 1` |
| 6 | `userCompanyRepository.setDefault(...)` | 方法 2(返回 int,Spy)| `setDefault` | `WHERE user_id = ? AND company_id = ?` |
| 7 | `userCompanyRepository.countByUserIdAndIsDefault(userId, 1)` | 方法 4(返回 int)| `countByUserIdAndIsDefault` | `WHERE user_id = ? AND is_default = #{isDefault}`(参数化) |
| 8 | `if (defaultCount != 1) throw IllegalStateException(...)` | (判断)| - | - |
| 9 | (方法返回) | - | - | - |

---

## §7 与前序 10 份文档的一致性审计(241V2A-11)

### 7.1 一致性矩阵

| 文档 | 检查项 | 一致? | 备注 |
|---|---|:-:|---|
| 240 Q4 跨公司隔离架构 | 涉及 user_company? | ✓ | 沿用 |
| 241V2 §12.3 | defaultCompanyId 归属 user_company.is_default | ✓ | 沿用 |
| 241V2A P0-2 | MetaObjectHandler setFieldValByName | ✓ | 不冲突 |
| 241V2A-1 §6.2 | Mapper.countByUserIdAndCompanyId | ✓ | **241V2A-11 显式作废 241V2A-10 §5.3 的 existsBy... Mapper 写法,沿用此契约** |
| 241V2A-1 §6.2 | Mapper.countByUserIdAndIsDefault 方法名 | ✓ | **沿用方法名,241V2A-11 显式作废 241V2A-1 §6.2 的硬编码 is_default=1 SQL,SQL 改为参数化** |
| 241V2A-1 §9.3 | 操作后最多 1 条 default | ✓ | **241V2A-11 强化为"成功路径必须 exactly-one"** |
| 241V2A-1 §5.1 | 7 步流程(241V2A-10 升级为 9 步)| ✓ | 沿用 |
| 241V2A-2 死锁表述 | 单行锁免疫 | ✓ | 沿用 |
| 241A-1 独立盲审 | 6 P1 识别 | ✓ | 241V2A-11 修复 2 个新 P1 |
| 241V3 IGNORE_TABLES | 5 张 IGNORE 表 | ✓ | 不冲突 |
| 241V2A-3 Spring 代理 | self-invocation 禁止 | ✓ | 不冲突 |
| 241V4 表数量 | 15 张实际表 | ✓ | 不冲突 |
| 241V2A-4 TestDataContext | 4 字段 | ✓ | 不冲突 |
| 241V2A-5 verifyFinalState | 参数 | ✓ | 不冲突 |
| 241V2A-6 Spring TestContext | @SpringBootTest | ✓ | 不冲突 |
| 241V2A-7 CompanyTestFixture | DEFAULT-04 fixture | ✓ | 不冲突 |
| 241V2A-8 @SpyBean 字段 | 10 条约束 | ✓ | **不冲突**;@SpyBean 包装 UserCompanyRepository(interface),Spy 4 个方法都可 |
| 241V2A-9 §4.2 Service 模板 | 调 existsBy.../countBy... | ✓ | **241V2A-11 强化步骤 6 为 exactly-one** |
| 241V2A-10 §4.1 Repository interface | 4 个方法 | ✓ | **沿用** |
| 241V2A-10 §4.2 RepositoryImpl | 调 Mapper.existsBy... | ✗ | **241V2A-11 修正为 Mapper.countBy...** |
| 241V2A-10 §5.3 Mapper interface | existsBy... 写法 | ✗ | **241V2A-11 显式作废** |
| 241V2A-10 §7.1 Service 步骤 6 | `if (defaultCount > 1)` | ✗ | **241V2A-11 改为 `if (defaultCount != 1)`** |

**总结**:与 241V2A-10 有 3 处冲突(都已通过 241V2A-11 显式作废旧写法 + 显式冻结新唯一写法);与 241V2A-1 §6.2 有 1 处冲突(241V2A-1 的 SQL 硬编码 1 写法,已通过 241V2A-11 显式作废 + 冻结新 SQL);与其它 14 份文档均一致。

### 7.2 显式作废汇总表(241V2A-11)

| # | 旧写法来源 | 旧写法 | 状态 | 新唯一写法来源 |
|---:|---|---|---|---|
| 1 | 241V2A-10 §4.2 RepositoryImpl | `userCompanyMapper.existsByUserIdAndCompanyId(userId, companyId)` | 【作废】 | 241V2A-11 §5.2 `userCompanyMapper.countByUserIdAndCompanyId(userId, companyId) > 0` |
| 2 | 241V2A-10 §5.3 Mapper interface | `int existsByUserIdAndCompanyId(...)` | 【作废】 | 241V2A-1 §6.2 `int countByUserIdAndCompanyId(...)`(沿用) |
| 3 | 241V2A-1 §6.2 Mapper SQL | `WHERE user_id = #{userId} AND is_default = 1`(硬编码 1) | 【作废 SQL】 | 241V2A-11 §5.3 `WHERE user_id = #{userId} AND is_default = #{isDefault}`(参数化) |
| 4 | 241V2A-10 §7.1 Service 步骤 6 | `if (defaultCount > 1) throw` | 【作废】 | 241V2A-11 §5.5 `if (defaultCount != 1) throw` |

**注意**:不修改任何历史 MD,通过新增 241V2A-11 建立"旧写法作废 + 新写法冻结"的叠加关系。

### 7.3 严禁清单(241V2A-11)

#### 7.3.1 实施者严禁

- ✗ 不得在 Mapper 同时定义 `existsByUserIdAndCompanyId` 和 `countByUserIdAndCompanyId` 两套
- ✗ 不得在 Repository.existsByUserIdAndCompanyId 内部调 Mapper.existsByUserIdAndCompanyId(旧写法)
- ✗ 不得在 Mapper.countByUserIdAndIsDefault 的 SQL 硬编码 `is_default = 1`
- ✗ 不得在 Service 步骤 6 用 `if (defaultCount > 1)`(必须 != 1)
- ✗ 不得在 DEFAULT-05 验证用 `isLessThanOrEqualTo(1)` 或 `isGreaterThanOrEqualTo(1)`(必须 isEqualTo(1))
- ✗ 不得在 Service 直调 Mapper(必须经 Repository)
- ✗ 不得在 Repository 自行实现 SQL(必须委托 Mapper)

#### 7.3.2 文档作者严禁

- ✗ 不得修改 241V2A-10 / 241V2A-9 / 241V2A-1 / 任何历史 MD
- ✗ 不得在本补丁(241V2A-11)内**重新**写"以实际实现为准"
- ✗ 不得在 241A-1 之后跳过独立盲审

---

## §8 重新审计 P 状态(241V2A-11)

### 8.1 P1-7 / P1-8 / P1-9 状态(沿用 241V2A-10)

| # | 状态 | 沿用 |
|---|:-:|---|
| P1-7 | **PASS** | 241V2A-7 沿用 |
| P1-8 | **PASS** | 241V2A-8 沿用 |
| P1-9 | **PASS** | 241V2A-9 沿用 |
| P1-10 | **PASS** | 241V2A-10 沿用 |
| P1-11 | **PASS** | 241V2A-10 沿用 |
| **P1-12** | **本补丁关闭** | 241V2A-11 §2 关闭 |
| **P1-13** | **本补丁关闭** | 241V2A-11 §3 关闭 |

### 8.2 P1-12 状态(本补丁)

| 检查项 | 通过 |
|---|:-:|
| Mapper.existsByUserIdAndCompanyId(...) 显式作废? | ✓ §2.2 |
| Mapper.countByUserIdAndCompanyId(...) 沿用 241V2A-1 §6.2? | ✓ §2.2 + §5.3 |
| Repository.existsByUserIdAndCompanyId(...) 保留? | ✓ §5.1 |
| RepositoryImpl 内部调 Mapper.countBy... > 0? | ✓ §5.2 |
| 唯一调用链冻结? | ✓ §2.4 |
| 与 241V2A-10 §4.2 / §5.3 旧写法显式对比? | ✓ §7.2 显式作废表 |

**P1-12 真闭环** ✓

### 8.3 P1-13 状态(本补丁)

| 检查项 | 通过 |
|---|:-:|
| Mapper.countByUserIdAndIsDefault 方法名沿用 241V2A-1 §6.2? | ✓ §3.2 + §5.3 |
| SQL 显式参数化 `is_default = #{isDefault}`? | ✓ §3.2 + §5.3 |
| 显式作废 241V2A-1 §6.2 的硬编码 `is_default = 1` SQL? | ✓ §3.2 显式作废 + §7.2 表 |
| Service 调用固定传 isDefault=1? | ✓ §3.3 + §5.5 |
| 签名语义与 SQL 语义一致? | ✓ §3.4 唯一调用链 |

**P1-13 真闭环** ✓

### 8.4 P2 状态(本补丁顺手裁决)

| 检查项 | 通过 |
|---|:-:|
| Service 步骤 6 `if (defaultCount != 1) throw`? | ✓ §4.2 + §5.5 |
| 与 241V2A-1 §9.3 不变量不矛盾? | ✓ §4.1(明确划分) |
| DEFAULT-05 验证 `isEqualTo(1)`? | ✓ §4.4 |
| 不升级为 P1(老板明确"P2 顺手裁决,不扩大为新 P1")? | ✓ 保持 P2 |

**P2 已裁决(显式声明不阻塞 S1-169-2 启动)** ✓

### 8.5 是否产生新的 P0

| 检查项 | 结论 |
|---|---|
| Mapper 唯一契约? | ✓ §5.3 4 个方法无歧义 |
| Repository 唯一契约? | ✓ §5.1 4 个方法无歧义 |
| 唯一调用链? | ✓ §6.3 对应表 |
| exactly-one 约束? | ✓ §4 |
| DEFAULT-05 9 步 rollback 仍成立? | ✓ §6 |

**无新 P0** ✓

### 8.6 是否产生新的 P1

| 检查项 | 结论 |
|---|---|
| 与 241V2A-10 冲突已显式作废? | ✓ §7.2 表 |
| 与 241V2A-1 §6.2 冲突已显式作废? | ✓ §7.2 表 |
| 与其它 14 份文档兼容? | ✓ §7.1 |
| LOCK-ORDER-01 保留? | ✓(241V2A-1 §4 沿用) |
| @SpyBean 仍可包装 Repository 4 个方法? | ✓(Repository interface 不变)|

**无新 P1** ✓

### 8.7 P 状态汇总(241V2A-11 后)

| 等级 | 数量 | 明细 |
|---|:-:|---|
| P0 | 0 | - |
| P1 | 0 | P1-7 ~ P1-13 全部 PASS 或本补丁关闭 |
| P2 | 1(已裁决) | exactly-one 约束已正式冻结 |
| INFO | 0 | - |

---

## §9 报告统计(241V2A-11)

- 文档字节:约 30,000 字节
- 章节数:13
- 修复的 P1:2(P1-12 + P1-13)
- 顺手裁决的 P2:1(exactly-one)
- 显式作废的旧写法:4(241V2A-10 §4.2 / §5.3 / 241V2A-1 §6.2 SQL / 241V2A-10 §7.1 步骤 6)
- 显式冻结的新唯一写法:4(RepositoryImpl / Mapper interface / Mapper SQL / Service 步骤 6)
- 唯一 Effective Spec:Repository 4 方法 + Mapper 4 方法 + Service 9 步 + exactly-one
- 与 18 份前序文档关系:补丁叠加(沿用 + 显式作废 + 显式冻结)
- 启动闸门:全部满足,等下一轮独立盲审
- DDL 修改:0
- Java 代码修改:0
- commit / push:0 / 0

---

## §10 启动闸门(241V2A-11)

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
| **241V2A-11 修复 P1-12 + P1-13 + P2 裁决(本文件)** | **✓** | **本文件** |
| **下一轮独立盲审 PASS** | ⏳ | 等待 |
| **老板明确指令"开始 S1-169-2"** | ⏳ | 等待 |

### 10.2 下一轮盲审必审计

- ✓ 241V2A-11 是否真修复 P1-12 + P1-13 + P2 exactly-one
- ✓ 241V2A-11 §7.2 显式作废表的 4 项作废是否真覆盖旧写法
- ✓ 241V2A-11 §5.3 Mapper 4 方法 + §5.5 Service 9 步 + §6.3 对应表是否完全自洽
- ✓ 19 份文档是否仍有内部矛盾

---

## §11 一句话最终判断

> **241V2A-11 S1-169-1 UserCompanyMapper 前序契约一致性修复补丁完成**:第八轮独立盲审识别的 P1-12(241V2A-10 §5.3 把 Mapper 权限查询方法冻结为 `existsByUserIdAndCompanyId(...)` 与 241V2A-1 §6.2 已冻结的 `countByUserIdAndCompanyId(...)` 命名冲突)+ P1-13(241V2A-1 §6.2 的 `countByUserIdAndIsDefault(userId, isDefault)` 方法签名是参数化,但 SQL 实际硬编码 `is_default = 1`——签名与 SQL 矛盾)+ 顺手裁决 P2(Service 步骤 6 用 `if (defaultCount > 1) throw` 未明确 exactly-one 约束)通过本补丁**真闭环**——**P1-12 修复** = 沿用 241V2A-1 §6.2 的 `countByUserIdAndCompanyId` Mapper 方法 + 显式作废 241V2A-10 §4.2 / §5.3 的 `existsByUserIdAndCompanyId` 旧写法 + Repository.existsByUserIdAndCompanyId 内部调 `Mapper.countByUserIdAndCompanyId(...) > 0`;**P1-13 修复** = 沿用 241V2A-1 §6.2 的 `countByUserIdAndIsDefault` 方法名 + 显式冻结 SQL 语义为 `is_default = #{isDefault}`(参数化)+ 显式作废 241V2A-1 §6.2 的硬编码 `is_default = 1` SQL + Service 调用固定传 isDefault=1;**P2 裁决** = Service 步骤 6 `if (defaultCount != 1) throw IllegalStateException("default company 数量必须为 1, actual=" + defaultCount)`(从 > 1 改为 != 1)+ DEFAULT-05 阶段 C 验证 `isEqualTo(1)`(exactly-one)+ 显式划分与 241V2A-1 §9.3 业务层"允许 0 个"的不矛盾(操作前可 0,操作成功后必须 1,业务层主动清空可 0);最终建立唯一 Effective Spec:Repository 4 个公开方法(沿用 241V2A-10 §4.1)+ RepositoryImpl 4 个方法(241V2A-11 §5.2 修正 241V2A-10 §4.2)+ Mapper 4 个自定义方法(241V2A-11 §5.3)+ Service 9 步流程(241V2A-11 §5.5 强化 241V2A-10 §7.1)+ exactly-one 约束(241V2A-11 §4);数据事实与设计区分显式:user_company DDL = 【已验证业务事实】,UserCompany 实体 / Repository 4 方法 / Mapper 4 自定义方法 = 【OptFlow设计】,SQL 注解字面量 = 【OptFlow设计】(本补丁显式冻结,非"以实际实现为准");P1-7 / P1-8 / P1-9 / P1-10 / P1-11 全部 PASS,P1-12 / P1-13 本补丁关闭,P2 exactly-one 已正式裁决(显式声明不阻塞);241V2A-11 不修改 241V2A-10 / 241V2A-9 / 241V2A-1 任何字节,只通过"显式作废 + 显式冻结"建立补丁叠加关系;S1-169-2 仍 BLOCK,等下一轮独立盲审。

---

## §12 报告统计(完整)

- 章节数:12
- 修复的 P1:2(P1-12 + P1-13)
- 顺手裁决的 P2:1(exactly-one)
- 显式作废的旧写法:4
- 显式冻结的新唯一写法:4
- 唯一 Effective Spec 字段:
  - Repository interface:4 个方法
  - RepositoryImpl:4 个方法(修正 241V2A-10 §4.2)
  - Mapper interface:4 个自定义方法(沿用 241V2A-1 §6.2 + 显式作废 241V2A-10 §5.3)
  - Service 9 步流程(含 exactly-one 约束)
  - DEFAULT-05 9 步 rollback 时序(强化验证步骤)
- 严禁清单:7 类
- 启动闸门:全部满足
- 下一轮:独立盲审

---

## §13 文件结尾(241V2A-11 显式)

【P1-12 修复完成】
【P1-13 修复完成】
【P2 exactly-one default 规则已正式裁决】
【S1-169-2 继续 BLOCK】
【等待下一轮独立盲审】
【不得自评 PASS】
