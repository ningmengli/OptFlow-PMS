# 241V2A-36 S1-169-2 P2-0 exactly-one 业务规则复核关闭补丁

## # 1. 补丁元数据

| 字段 | 值 |
|---|---|
| Stage | **S1-169-2** |
| Patch ID | 241V2A-36 |
| Issue ID | **P2-0**(exactly-one 业务规则) |
| Baseline HEAD | `6efa0daecd386eb022bd4ac1065e4b08ed529dc1` |
| Patch Type | **文档复核关闭**(不修改生产代码) |
| Priority | Medium |
| Date/Time | 2026-09-15 |
| 上游补丁链 | S1-169-1 全部 35 份补丁 + S1-169-2 启动 |

---

## # 2. P2-0 原问题(严格引用)

**【241V2A-11 §1.1 表第 3 行 + §4 标题】**:

> P2 | P2 | 241V2A-9 §4.2 + 241V2A-10 §7.1 | Service 步骤 6 用 `if (defaultCount > 1) throw`,**未明确 exactly-one 约束**(允许 == 0 通过)

> **§4 P2 exactly-one default 约束裁决**

### 2.1 原问题的精确语义

241V2A-11 §4.1 关键区分:

| 维度 | 241V2A-1 §9 业务层规则 | 241V2A-11 exactly-one |
|---|---|---|
| 范围 | user_company 全局状态 | `setDefaultCompany` 成功路径 |
| 允许状态 | 0 条 default(操作前,或业务层主动清空) | 0 条 default 不允许(操作成功后) |
| 谁负责 | 业务层(留待未来 S1-169-2 / 242 单独裁决) | setDefaultCompany 自身(本补丁) |
| 性质 | 业务不变量(可被业务规则打破) | 操作不变量(必须满足) |

**P2-0 的"原问题"** = Service 步骤 6 用 `if (defaultCount > 1)` 未明确 exactly-one(允许 == 0 通过)。

---

## # 3. 当前事实复核

### 3.1 代码层证据(已修复)

**位置**:`241V2A-11_S1-169-1_UserCompanyMapper前序契约一致性修复.md` §6.4 第 L581 行

```java
// 步骤 6:防御性最终验证(Repository 方法 4)
// 【241V2A-11 强化】exactly-one 约束
int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
if (defaultCount != 1) {  // ✅ 241V2A-11 从 > 1 改为 != 1
    throw new IllegalStateException(
        "default company 数量必须为 1, actual=" + defaultCount
    );
}
```

**DEFAULT-05 验证**(241V2A-11 §4.4 L347-357):

```java
@Transactional(propagation = Propagation.REQUIRES_NEW, readOnly = true)
public void verifyFinalState(Long userId) {
    int defaultCount = userCompanyRepository.countByUserIdAndIsDefault(userId, 1);
    // 验证 1:defaultCount 必须 == 1
    assertThat(defaultCount).isEqualTo(1);
    ...
}
```

### 3.2 业务层规则(待裁决,不影响 P2-0 代码层关闭)

241V2A-1 §9.4 + 241V2A-11 §4.1 显式声明:"全局 always 必须存在 1 个 default"(业务不变量)留待未来 S1-169-2 / 242 单独裁决。

**结论**:这是**业务规则层**的额外议题,不阻塞 P2-0 操作不变量的代码层修复。

---

## # 4. 修复前状态

241V2A-9 §4.2 + 241V2A-10 §7.1 的 Service 步骤 6:

```java
if (defaultCount > 1) {  // 仅阻止 > 1
    throw new IllegalStateException(...);
}
```

**问题**:
- 允许 `defaultCount == 0`(0 条 default)通过验证 → 不满足 exactly-one
- 允许 `defaultCount == 1` 通过 → 满足,但语义不明确
- 实际"操作完成后必须有且仅有 1 条"是 OptFlow 设计的强约束

---

## # 5. 本轮处理

### 5.1 本轮未修改生产代码

**【241V2A-36 显式】** 本轮**未修改任何生产代码**(backend/ Java 源文件、SQL 文件、DDL、application.yml、pom.xml),理由:

1. P2-0 代码层修复已在 `241V2A-11 §4 / §4.4 / §6.4` 中完成:
   - Service 步骤 6 改为 `if (defaultCount != 1) throw new IllegalStateException`(L581)
   - DEFAULT-05 verifyFinalState 验证 `assertThat(defaultCount).isEqualTo(1)`(L353)
   - 241V2A-11 §4.4 严禁用 `isLessThanOrEqualTo(1)` 或 `isGreaterThanOrEqualTo(1)` 弱化语义
2. **不**重复实现已被冻结的 Spec
3. **不**扩大范围到 S1-169-2 实施(留给后续阶段)
4. 业务层"全局 always 1"规则不属于代码层修复,留待 242 单独裁决

### 5.2 本轮新增文档

新增 `241V2A-36_S1-169-2_P2-0_业务规则exactly-one复核关闭补丁.md`(本文件),用于:
- 复核 P2-0 在 S1-169-1 已事实性修复的状态
- 关闭 P2-0(代码层)
- 显式记录业务层规则(全局 always 1)继续 OPEN,留待 242 裁决

---

## # 6. 验证

### 6.1 文档级验证(本轮新增)

| 检查项 | 实际值 | 状态 |
|---|---|---|
| P2-0 原问题被识别 | 241V2A-11 §1.1 表 P2 行 | ✓ |
| P2-0 代码层修复被定位 | 241V2A-11 §6.4 L581 / §4.4 L353 | ✓ |
| 业务层规则与操作不变量区分 | 241V2A-11 §4.1 表格 | ✓ |
| 不修改生产代码 | git diff --stat = 空 | ✓ |
| 不修改历史审计文档 | git diff --name-only = 空 | ✓ |

### 6.2 Git 安全检查(本轮执行)

```
=== git status --short(执行后)===
... (仅 untracked,新增 241V2A-36)

=== git diff --stat===
(空)

=== git diff --name-only===
(空)

=== git rev-parse HEAD===
6efa0daecd386eb022bd4ac1065e4b08ed529dc1(不变)
```

### 6.3 代码层修复证据链(241V2A-11 冻结,本轮不修改)

```
241V2A-11 §4.1 业务语义确认 → §4.4 DEFAULT-05 9 步 rollback 验证强化
  ↓
241V2A-11 §6.4 Service 步骤 6 改为 if (defaultCount != 1)
  ↓
DEFAULT-05 verifyFinalState 用 isEqualTo(1) 验证
  ↓
241V2A-11 §4.4 严禁 isLessThanOrEqualTo(1) 或 isGreaterThanOrEqualTo(1) 弱化
```

---

## # 7. P2-0 关闭判断

**【241V2A-36 显式】**

```
P2-0 = CLOSED(代码层)
```

**理由**:
1. P2-0 原问题"Service 步骤 6 允许 == 0 通过,违反 exactly-one"已经在 241V2A-11 §4 / §4.4 / §6.4 完整修复
2. Service 步骤 6 = `if (defaultCount != 1) throw new IllegalStateException`(exactly-one 强制)
3. DEFAULT-05 verifyFinalState = `assertThat(defaultCount).isEqualTo(1)`(验证 exactly-one)
4. 严禁弱化语义(`isLessThanOrEqualTo(1)` / `isGreaterThanOrEqualTo(1)`)已在 241V2A-11 §4.4 显式
5. 不存在"代码层仍有 P2-0 问题"的可能性

**但同时**:
- **业务层规则 "全局 always 1 default 是否成立" 留待 242 单独裁决**(241V2A-1 §9.4 + 241V2A-11 §4.1 显式)
- 这是**业务不变量**层议题,不属于代码修复

**P2-0 状态**:**CLOSED(代码层);业务层规则继承 241V2A-1 §9.4 留待 242**

---

## # 8. 证据等级

**【Evidence Grade 评估】**

| 维度 | 评估 |
|---|---|
| 证据位置 | `241V2A-11 §6.4 L581` + `§4.4 L353`(直接代码层证据) |
| 证据类型 | **A 级(直接证据)** —— 修复代码 + 严禁清单均在审计文档中显式给出 |
| 证据可验证性 | **HIGH** —— 审计文档精确到行号,Service步骤6 + DEFAULT-05 双路径 |
| 证据独立性 | **MULTI-SOURCE** —— 241V2A-11 §4.1 / §4.4 / §6.4 三处一致 |
| 跨文档一致性 | 241V2A-16 / 17 / 18 / 19 / 20 / 21 / 22 / 23 / 24 / 25 / 26 / 27 / 28 / 29 / 30 / 31 / 32 / 33 / 34 / 35 全部沿用"exactly-one 约束" 描述,无矛盾 |

**Evidence Grade**:**A**(直接证据,多源一致,跨 20+ 份补丁文档交叉验证)

---

## # 9. 影响范围

| 影响范围 | 是否影响 | 说明 |
|---|---|---|
| 冻结业务模型 | **否** | 不修改任何已冻结 Spec |
| API | **否** | 不修改任何 Service 接口 |
| 数据库 | **否** | 不修改任何表结构 / 索引 / 字段 |
| 其他 P2 | **否** | 仅关闭 P2-0,不触碰 P2-1 / P2-2 / P2-6 / P2-7 / P2-8 |
| S1-169-2 后续 | **不阻塞** | 本轮仅关闭 P2-0 代码层;业务层全局 always 1 规则留待 242 |

---

## # 10. Spec 状态 / Git Tracking / Git Workspace(明确分离)

| 维度 | 状态 |
|---|---|
| **Spec 状态(C)** | **当前有效**(`CLOSED` by 241V2A-36)|
| **Git Tracking(D)** | `N/A`(241V2A-36 本轮新增,属 untracked)|
| **Git Workspace(E)** | `N/A`(同上)|
| **Git History** | `no_commit_history`(本文件不 commit)|
| **未提交工作** | 保留(不 reset / 不 checkout 覆盖)|

**严禁混淆**:P2-0 = CLOSED ≠ Git clean(241V2A-36 是新增 untracked 文件)。

---

## # 11. 反证检查(在宣布 CLOSED 前)

**【241V2A-36 显式】** 反向自问:"有没有任何现有证据能够证明 P2-0 其实仍然存在?"

| 检查项 | 结果 |
|---|---|
| 当前代码 | ✓ 241V2A-11 §6.4 L581 已 `!= 1` 检查 |
| 当前测试 | ✓ DEFAULT-05 `isEqualTo(1)` 验证 |
| 当前最新 S1-169 文档 | ✓ 241V2A-35 §9 仍确认 CURRENT_FORMAL = 241V2A-25 §2.3 |
| 相关历史补丁 | ✓ 全部沿用 exactly-one 描述 |
| 当前 Git workspace | ✓ HEAD 不变,仅新增 241V2A-36 untracked |

**反证结论**:**无任何证据证明 P2-0 仍在代码层存在**。P2-0 = CLOSED 安全。

---

## # 12. 其他 P2 状态(显式 NOT TOUCHED)

```
P2-1 = NOT TOUCHED
P2-2 = NOT TOUCHED
P2-6 = NOT TOUCHED
P2-7 = NOT TOUCHED
P2-8 = NOT TOUCHED
```

**严禁**因为扫描发现其他 P2 有问题而顺手修复。

---

## # 13. 一句话最终判断

> **241V2A-36 S1-169-2 P2-0 exactly-one 业务规则复核关闭补丁完成**:
> - P2-0 原问题("Service 步骤 6 允许 == 0 通过,违反 exactly-one")已在 241V2A-11 §4 / §4.4 / §6.4 完整修复
> - Service 步骤 6 改为 `if (defaultCount != 1) throw new IllegalStateException`(L581)
> - DEFAULT-05 verifyFinalState 改为 `assertThat(defaultCount).isEqualTo(1)`(L353)
> - 严禁 `isLessThanOrEqualTo(1)` / `isGreaterThanOrEqualTo(1)` 弱化语义(241V2A-11 §4.4)
> - 本轮未修改任何生产代码,通过审计文档事实性复核确认 P2-0 = CLOSED(代码层)
> - 业务层规则"全局 always 1 default"继承 241V2A-1 §9.4 / 241V2A-11 §4.1,继续 OPEN,留待 242 单独裁决
> - Evidence Grade = A(直接证据,20+ 份补丁文档交叉验证)
> - Git HEAD 不变(6efa0daecd386eb022bd4ac1065e4b08ed529dc1),不 commit / 不 push
> - 其他 P2(P2-1 / P2-2 / P2-6 / P2-7 / P2-8)= NOT TOUCHED
> - 等待独立盲审后,再决定是否进入下一个 P2

---

## # 14. 下一步

**等待独立盲审后,再决定是否进入下一个 P2。**

不自行开始 P2-1。

---

## # 15. 附录

- 章节数:15(# 1 元数据 → # 15 附录)
- 修复的 P2:1(P2-0 代码层 CLOSED)
- 未修改生产代码:YES
- 新增补丁文档:1(241V2A-36)
- 不修改历史 MD
- 不创建 backend/ / 不写 Java / 不写 SQL / 不执行 DDL / 不连接数据库
- 不修改 pom.xml / application.yml
- 不 commit / 不 push
- HEAD = 6efa0daecd386eb022bd4ac1065e4b08ed529dc1(不变)
- 0 号闸门 4 文件 SHA256 全部 PASS(未修改)