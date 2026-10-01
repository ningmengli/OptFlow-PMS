# G2-Contract-Audit-04｜G2-Contract-04 独立盲审

> **审计对象**:`G2-Contract-04_OptFlow-PMS_Production-Implementation-Contract.md`
> **审计性质**:独立、从零、反向验证。**不修改被审计对象 1 字节**。
> **本审计不接受 G2-Contract-04 的任何自述结论为证据**,包括但不限于:
> "3 GAP 已修复" / "New P0 = 0" / "New P1 = 0" / "Regression = PASS" / "Keyword scan = PASS"。
>
> **Baseline HEAD**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`
> **0 号闸门**:`controller.js` / `deliveryList.html` / `machineOrderCompleted.html` / `machineOrderList.html` SHA256 **4 / 4 PASS**(与 G2-04 声明一致)
>
> **本审计不修复 Contract,不进入 G2-Contract-05,不进入 G3。**

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-04_Production-Implementation-Contract独立盲审.md` |
| 性质 | 独立盲审报告(唯一新增文件)|
| 审计对象行数 | 848 行 |
| 审计方法 | 全文逐行阅读 + 一手基线回溯 + 可复现关键词检索 |
| 严禁 | 修改 G2-Contract-04 / 任何历史 MD / 代码 / DDL / DB / Test / commit / push |

---

## §1 最终判定

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           G2-Contract-Audit-04  =  BLOCK                     ║
║                                                              ║
║   原有 3 项 GAP 实际关闭数 : 0 / 3                            ║
║   New P0 : 8    New P1 : 6    New P2 : 5                      ║
║   Issue : 19   Root Cause : 8    Fix Action : 19              ║
║                                                              ║
║   G2 READY  = BLOCK(维持)                                     ║
║   G3 ENTRY  = BLOCK(维持,不允许进入)                          ║
║   Backend   = 不允许创建(维持)                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**一句话结论**:G2-Contract-04 表面诚实(§19 自报 `Contract Gaps Closed = 0`),但正文 §3 / §6 / §7 **新引入了 8 项直接 P0 冲突**,其中 3 项(API-001/009 的 `companyId` DTO 暴露、复用 ID 错写 `uuid`、`scheduleId/slotId` 错写 `Long`)**与它自己引用的证据源在同一行内自相矛盾**;另有 2 项直接重开 `G2-Contract-Audit-03` 已判 PASS 的历史 Issue(P1-A1 / P1-A2),并通过 1 个改名 + 1 个自检表漏项双重掩盖。GAP-01 / GAP-02 / GAP-03 **一项都没有真正关闭**。

---

## §2 审计基线与证据优先级

### 2.1 本轮采信的一手基线

| 基线 | 生命周期 | 本轮用于裁决 |
|---|---|:-:|
| `241V2 §4.4` | S1-169 | **DTO 隔离(P0-01 裁决依据)** |
| `241V2A-17 §3.2/§3.3` | S1-169 | **60004 = USER_DISABLED(P0-08)** |
| `241V2A-18 §1.3.2` / `241V2A-19` | S1-169 | 60003/60004 证据等级 = 【OptFlow设计】 |
| `241A-1 §10` | S1-169 | 独立确认 DTO 隔离 = A 级 |
| `240 §18` | S1-169 | 严格禁止 fallback companyId |
| `238 §2.1/§3.1/§4.6/§4.8/§4.9/§5.1/§15.2/§15.4/§19` | S1-169 | **ID 类型最终映射 + BigScreen JSON + 事务动作** |
| **`234A`** | S1-168 前 | **复用实体 ID 逆向核验专项报告 —— 已预先判定 233 的 `uuid` 为错误** |
| **`234B`** | S1-168 前 | ID 类型后端 Schema 证据核验(后端文件 = 0,`Long` 为 E 级推断) |
| **`236A`** | S1-168 | **最终 DDL 冻结:6 BIGINT AUTO_INCREMENT + 6 CHAR(36) UUID** |
| `236B` | S1-168 | 12 PK = 6 BIGINT + 6 CHAR(36);31/31 FK 匹配 |
| `235B §2` | S1-167B | Employee.adminId NOT NULL(裁决 P0-08 引用错误)|
| `233 §2/§4/§5/§6/§7/§8/§9` | S1-167 | API 编号/路径/Method/Role/状态动作 |
| `G2-Contract-03 §3/§6.2/§16.1` | 本链 | 回归基线(FA-09/FA-10/P1-A1/P1-A2)|

### 2.2 冲突裁决规则(本轮实际执行)

文档编号序 = 生命周期序。同域冲突时**后序冻结覆盖前序**:

```
233 (S1-167)  <  235B/236A/236B (S1-168)  <  238/240/241V2/241V2A (S1-169)
                     ↑
              234A / 234B 逆向核验(位于 233 之后、236A 之前)
```

因此:
- 233 line 156-158 的 `companyId/patientId/employeeId = uuid` **不构成最终 Contract**。**`234A §4.1 line 357` 早已明确判定该写法为「错误」**(原文:`233 §4 API-001 Request | "companyId / patientId / employeeId 类型 uuid" | **错误** — 无 UUID 证据,实际不是 UUID`)。`234A §4.1 line 358` 同样判定 `233 §API-021 Request` 的 `employeeId / consultRoomId = uuid` 为**错误**。**本条不再是"后序覆盖前序"的一般推断,而是专项逆向核验报告的显式纠错裁决。**
- 233 line 156 的 `companyId` 出现在 Request DTO,**不构成 DTO 可暴露的授权**,被 241V2 §4.4 覆盖为**禁止**。
- 233 line 159-160 的 `scheduleId/slotId = uuid` 方向上与 236A/238 的 `CHAR(36)` **一致**(新建 UUID 域),但 `uuid` 文本不得机械沿用。

> **本审计明确拒绝的推理链**:
> "233 写了 → 所以 G2-Contract 冻结" = 证据污染,不成立。
> "238 §4.8 是我自己引用的 → 所以 Long 正确" = 自相矛盾,不成立。
> "234A 只是 E 级推断 → 所以类型待确认" = **同样不成立** —— 234A 的 **A 级证据(0 UUID 字面量 + 数字字面量 + parseInt 模式)**已锁定"非 UUID/非 String"的方向;其后的 236A/236B 已把 DDL **冻结**为 BIGINT,238 再映射为 `Long`。当前有效 Contract 类型 = `Long`,证据等级 = **【OptFlow设计】**(非【原系统事实】)。见 §4.2 证据等级修正。

---

## §3 回归核验(0 号闸门 + 历史不变量)

### 3.1 可复现关键词检索(独立执行)

检索对象:`G2-Contract-04_OptFlow-PMS_Production-Implementation-Contract.md` 全文 848 行。

| 关键词 | 命中数 | 命中行 | 独立裁决 |
|---|---:|---|:-:|
| `NURSE` | 1 | 763 | ✅ 仅自检表,无角色回流 |
| `BIGSCREEN` | 9 | 352,475,478,482,484,503,673,724,764 | ✅ 全为 BigScreen Entity/Service/模块名,**无 BIGSCREEN role** |
| `7 roles` | 0 | — | ✅ |
| `LIMIT 1` | 1 | 762 | ✅ 仅自检表 |
| `selectDefaultCompanyId` | 5 | 55,416,417,766,786 | ✅ 全为严禁说明 / Mapper 测试专用,无 LIMIT/ORDER BY |
| `getEmployeeByLogin` | 3 | 441,449,767 | ✅ 严禁声明 + 删除行 + 自检 |
| `公司初始化` | 3 | 441,491,769 | ✅ 同上 |
| `SaaS 初始化` | 3 | 441,491,770 | ✅ 同上 |
| `rollback` | — | §7.2 step 9 | ✅ Transfer 全回滚冻结保留 |
| **`companyId`** | **13** | **98,228** 为 Request DTO 必填字段 | ❌ **P0-01** |
| **`defaultCompanyId`** | 5 | 55,416,417,766,786 | ✅ 全为严禁说明 |
| **`String(uuid)`** | 25 处 | 98-228 区间为主 | ❌ **P0-02 / P0-03** |
| **`Long`** | 8 处 | 229,241,253,263,273,283,297 | ❌ **P0-03**(其中 229/283 正确)|
| **`可能`** | **2** | **570,604** | ❌ **P0-05** |
| **`parseConsultRoomIdArray`** | 4 | 441,475,**483**,768 | ❌ **483 为活跃 Service 方法行 → P0-07** |
| **`parseConsultRoomIdArrayJson`** | 1 | **483** | ❌ **P0-07(自检表未覆盖)** |
| **`getCurrentEmployee`** | 1 | 450 | ❌ **P0-08(证据归属错误)** |
| **`validateEmployeeActive`** | 1 | 451 | ❌ **P0-08(自建常量)** |
| **`createPatient`** | 1 | 460 | ⚠️ 【待确认】,未冻结,合规 |
| **`listForDisplay`** | 1 | 484 | ⚠️ 【待确认】,未冻结,合规 |
| **`EMPLOYEE_DISABLED`** | **1** | **451** | ❌ **P0-08(全库仅此 1 处 = G2-04 自创)** |
| **`60004`** | **1** | **451** | ❌ **P0-08(全库冻结值为 USER_DISABLED)** |
| **`List<Long>`** | 1 | 483 | ❌ **P0-07(238 §15.2 标【待确认】/不推荐)** |

### 3.2 回归核验结论

| 不变量 | 状态 | 说明 |
|---|:-:|---|
| API-001~040 编号/路径/Method | ✅ | 引用式继承 G2-03,本轮未发现改动 |
| 6 Role / API-040 = PUBLIC | ✅ | §9 完整沿用 |
| DefaultCompany | ✅ | §5.4 沿用 |
| Repository 4 public methods | ✅ | §5 沿用 |
| Mapper 5 methods | ✅ | §5 沿用 |
| `selectDefaultCompanyId` 无 LIMIT | ✅ | 检索确认 |
| Transfer 9 步 | ✅ | §7.2 完整保留,含"不创建新 ReceptionQueue" |
| Tenant / IGNORE_TABLES | ✅ | §8/§12 沿用 |
| Exception | ✅ | §10 沿用 |
| DEFAULT-01~05 | ✅ | §7.1 沿用 |
| Dev Environment 未编造 | ✅ | §19.2 标【待确认】,符合本轮要求 |
| 2 项文字漏标 P1 已显式标 | ✅ | §13.1 #8 / §17.2 #8 |
| **P1-A1(Repository 升 Service)** | ❌ | **被 §6.2 重开 → P0-06** |
| **P1-A2(自创 parseConsultRoomIdArray)** | ❌ | **被 §6.2.5 改名重开 → P0-07** |
| **241V2A-17/18/19 异常契约** | ❌ | **被 §6.2.1 冲突 → P0-08** |
| **241V2 §4.4 DTO 隔离** | ❌ | **被 §3.2/§3.3 违反 → P0-01** |
| **234A 复用 ID 逆向纠错裁决** | ❌ | **被 §3.2 违反 → P0-02** |
| **236A 最终 DDL(6 BIGINT + 6 CHAR(36))** | ❌ | **被 §3.2/§3.3 违反 → P0-02 / P0-03** |
| **238 §4.6/§4.8/§4.9 类型** | ❌ | **被 §3.2/§3.3 违反 → P0-02 / P0-03** |
| **233 API-016 4 对象** | ❌ | **被 §7.3.1 违反 → P0-04** |
| **233 + 238 T04 API-021 4 动作** | ❌ | **被 §7.3.2 违反 → P0-05** |

---

## §4 用户指定的 5 项重点 P0 核验

> **指令核对(诚实标注)**:本轮指令标题为"重点核验我指出的 **8** 个风险",但正文实际列举 **5** 项(P0-01 ~ P0-05)。
> **本审计的处理**:完整执行列举的 5 项;同时按指令 §三"继续主动寻找其他新问题"的 10 项扫描要求,**独立发现 3 项额外 P0**(见 §5.1 P0-06 / §5.2 P0-07 / §5.3 P0-08)。
> **结果恰好为 8 项 P0**,与指令标题的数量一致。若指令原意另指 3 项未列出的风险,本审计无法追溯,特此标注。

### 4.0 第一轮已核验 / 第二轮补强说明

| P0 | 第一轮证据基础 | 第二轮补强 | 结论是否变化 |
|:-:|---|---|:-:|
| P0-01 | 241V2 §4.4 + 241A-1 §10 + 240 §18 | — | **不变** |
| P0-02 | 238 §4.6/§4.8 + 236B | **+ 234A 专项逆向纠错 + 236A 6 张表逐张 DDL + 证据等级修正** | **不变(证据更强)** |
| P0-03 | 238 §4.8/§4.9 + 236B | **+ 236A 最终 DDL + FK 不可实现性论证** | **不变(严重度上升)** |
| P0-04 | 233 API-016 §2/§8/§6 | — | **不变** |
| P0-05 | 233 line 814 + 238 §19 T04 | — | **不变** |

### 4.1 P0-01 业务 Request DTO 是否重新暴露 companyId / defaultCompanyId —— ❌ **确认违反**

**一手规则(241V2 §4.4,line 175-182)**:

```
### 4.4 DTO 隔离要求(P0-2 配套)
【241V2 新设计】DTO(LoginDTO / UserInfoVO / 业务 Request/Response)必须:
- ✗ 不得 包含 companyId 字段
- ✗ 不得 包含 defaultCompanyId 字段
- ✗ 不得 包含任何 company scope 控制字段
- ✓ 如需展示当前 companyId,只能从 CompanyContext.getCompanyId() 后端注入
```

**独立佐证**:
- `241A-1_S1-169-1_四文档最终独立盲审.md` line 711:`| 10 | DTO 隔离 | 241V2A §4.4 | 不暴露 companyId + @JsonIgnoreProperties | A | ✓ | OK |`
- `240 §18` line 689:"V4.4 严格禁止 fallback companyId=1L(必须从登录态或显式切换获取,缺失 → 抛 CompanyContextMissingException)"

**G2-Contract-04 实际内容**:

| 位置 | 内容 |
|---|---|
| §3.2 API-001,line 98 | `\| companyId \| String(uuid) \| ✅ \| — \| 必须 = 当前用户 companyId \| 233 §4 #4 \|` |
| §3.3 API-009,line 228 | `\| companyId \| String(uuid) \| ✅ \| 238 §4.8 + 233 §5 \|` |
| §3.8,line 364 | `\| **API-001** \| ✅ 11 字段冻结(233 §4) \| ... \| A \| 已冻结 \|` |

**裁决**:
1. 两处 Request DTO 均把 `companyId` 标为 **✅ 必填**,直接违反 241V2 §4.4 的 `✗ 不得包含`。
2. §3.8 将 API-001 的 Evidence Grade 标为 **A 级"已冻结"**,把一条已被上位文档判为**安全不变量违规**的字段升级为冻结事实。
3. **根因可定位**:G2-04 §2 Evidence 表把 `241V2 §4-§6` 一行概括为 **"CompanyContext + TenantLine"**,**完全没有把 §4.4 DTO 隔离纳入证据基线**。241V2 §4.4 在 G2-04 的证据链里根本不存在,因此 233 的旧写法被无阻力复制。
4. 附带:API-025 在 233 line 902 同样含 `companyId` 必填,G2-04 §3.7 将其整体标【待确认】,**规避了复制但也规避了裁决** → 见 P1-04。

---

### 4.2 P0-02 复用实体 ID 是否错误写成 uuid —— ❌ **确认违反**

**专项逆向核验(234A —— 本审计为 P0-02 找到的最强一手证据)**:

`234A_复用实体ID类型逆向核验报告.md` 是**专门为此问题设立的逆向核验报告**,其 §4.1 已逐条判定 233 的写法为错误:

| 来源 | 行 | 原文 |
|---|---:|---|
| `234A §4.1` | 357 | `233 §4 API-001 Request \| "companyId / patientId / employeeId 类型 uuid" \| **错误** — 无 UUID 证据,实际不是 UUID` |
| `234A §4.1` | 358 | `233 §API-021 Request \| "employeeId / consultRoomId 类型 uuid" \| **错误** — 同上` |
| `234A §4.2` | 363-370 | 6 个 ID 修正表:`233 写 uuid` → `真实 long` |
| `234A §7.1` | 433-440 | 给 233 的修正表(同结论)|
| `234A §9` | 483 | `全部是数值类型,极可能是 Long / BIGINT,**不是 UUID**` |

`234A §3.1` 的 **A 级证据**(字符级,可复现):

| A 级证据 | 来源 | 结论 |
|---|---|---|
| `0` UUID 字面量 | `controller.js` 全文件 `[0-9a-f]{8}-[0-9a-f]{4}-...` 检索 | **6 个 ID 都不是 UUID** |
| 数字字面量 `10000` | controller.js L8423 | patientId = 数字 |
| `parseInt` 模式 | controller.js L8213 等 | patientId = string→int |

**最终 DDL 冻结(236A —— 6 张复用表逐张确认)**:

```sql
-- 236A line 129 / 146 / 168 / 190 / 212 / 229
companyId    BIGINT  NOT NULL AUTO_INCREMENT   -- company
customerId   BIGINT  NOT NULL AUTO_INCREMENT   -- customer
patientId    BIGINT  NOT NULL AUTO_INCREMENT   -- patient
employeeId   BIGINT  NOT NULL AUTO_INCREMENT   -- employee
consultRoomId BIGINT NOT NULL AUTO_INCREMENT   -- consult_room
bigScreenId  BIGINT  NOT NULL AUTO_INCREMENT   -- big_screen
```

**Java 映射冻结(238)**:

| 来源 | 行 | 内容 |
|---|---:|---|
| `238 §4.6` | 212-213 | `bigScreenId \| Long` / `companyId \| Long` |
| `238 §4.8` | 255-256 | `companyId \| Long` / `employeeId \| Long` |
| `238 §2.1 / §3.1` | 57-66 / 73-82 | 6 复用 = Long/BIGINT;6 新建 = String/CHAR(36) |
| `236B` | 298 / 330 / 332 | `12 PK(6 BIGINT AUTO_INCREMENT + 6 CHAR(36) UUID)`;`31/31 BIGINT ↔ BIGINT / CHAR(36) ↔ CHAR(36)` |

**一手映射汇总**:

| 域 | ID | DB 类型 | Java 类型 | 来源 |
|---|---|---|---|---|
| 复用(6) | `companyId` | BIGINT | `Long` | 238 §4.6 line 213 / §4.8 line 255 |
| 复用(6) | `customerId` | BIGINT | `Long` | 238 §2.1 |
| 复用(6) | `patientId` | BIGINT | `Long` | 238 §2.1 |
| 复用(6) | `employeeId` | BIGINT | `Long` | 238 §4.8 line 256 |
| 复用(6) | `consultRoomId` | BIGINT | `Long` | 238 §4.9 line 269 |
| 复用(6) | `bigScreenId` | BIGINT | `Long` | 238 §4.6 line 212 |
| 新建(6) | `scheduleId` / `slotId` / `appointmentId` / `visitId` / `triageQueueId` / `receptionQueueId` | CHAR(36) | `String` | 238 §3.2 + 236B line 298/330 |

`236B line 332`:`31/31 BIGINT ↔ BIGINT / CHAR(36) ↔ CHAR(36)`。

**G2-Contract-04 实际内容**:

| 位置 | 内容 | 238 实际 | 裁决 |
|---|---|---|:-:|
| line 98 | `companyId \| String(uuid)` | `Long`(§4.8 line 255)| ❌ |
| line 99 | `patientId \| String(uuid)` | `Long` | ❌ |
| line 100 | `employeeId \| String(uuid)` | `Long`(§4.8 line 256)| ❌ |
| line 228 | `companyId \| String(uuid)`,Evidence 写 **`238 §4.8`** | §4.8 line 255 = **`Long`** | ❌ **引用与内容直接矛盾** |

**裁决**:
- line 228 是最强证据:G2-04 **主动引用 `238 §4.8`**,而 238 §4.8 第 255 行写的是 `companyId | Long`。**引用来源与被引内容在同一份 Contract 内互相否定**,不属"表述风格差异"。
- **补充决定性证据**:`236A` 的 `appointment` 表(line 298-303)把 API-001 的 5 个 ID 字段**并列冻结在同一条 DDL 里**:
  ```sql
  appointmentId  CHAR(36) NOT NULL DEFAULT (UUID()),   -- 新建 UUID
  companyId      BIGINT   NOT NULL,                    -- 复用 BIGINT
  patientId      BIGINT   NOT NULL,                    -- 复用 BIGINT
  employeeId     BIGINT   NOT NULL,                    -- 复用 BIGINT
  scheduleId     CHAR(36) NOT NULL,                    -- 新建 UUID
  slotId         CHAR(36) NOT NULL,                    -- 新建 UUID
  ```
  G2-04 §3.2 把这 **5 个字段全部写成 `String(uuid)`** —— **3/5 错误**。这是"复用 vs 新建"二分未被执行的最直接证据:**同一张表内、同一段 DDL 里,两种类型并存,G2-04 未能区分。**
- **证据等级修正**:G2-04 §3.8 line 364 将 API-001 标为 `Evidence Grade = A`。但 234A §5.2 / 234B §2-§6 均把 `Long/BIGINT` 定为 **E 级推断**(后端 Java POJO 未观察,234B §1.2 `后端文件 = 0 个`),其后的 236A/236B 是**【OptFlow设计】冻结**而非【原系统事实】。G2-04 既写错类型,又标错证据等级 —— **双重错误**。
- **复用 vs 新建的分野未被遵守**:G2-04 对新建 ID 用 `String(uuid)` 方向正确(但见 P0-03),对复用 ID 同样用 `String(uuid)`,**说明未执行"6 Long / 6 String"的二分**。
- **附带发现**:`234A §4.1 line 358` 判定 `233 §API-021 Request` 的 `employeeId / consultRoomId = uuid` 亦为错误。G2-04 §7.3.2 讨论 API-021 但其 DTO 全部【待确认】,**该纠错未被继承也未被登记** → 并入 P1-04 冲突清单。

---

### 4.3 P0-03 scheduleId / slotId 是否错误写成 Long —— ❌ **确认违反**

**最终 DDL 冻结(236A —— 决定性)**:

```sql
-- 236A line 246-255  appointment_schedule
CREATE TABLE appointment_schedule (
  scheduleId     CHAR(36)     NOT NULL DEFAULT (UUID()),   -- ← UUID
  companyId      BIGINT       NOT NULL,
  employeeId     BIGINT       NOT NULL,
  ...
  PRIMARY KEY (scheduleId),
  CONSTRAINT fk_schedule_employee FOREIGN KEY (employeeId) REFERENCES employee(employeeId) ON DELETE RESTRICT,

-- 236A line 271-285  appointment_slot
CREATE TABLE appointment_slot (
  slotId         CHAR(36)     NOT NULL DEFAULT (UUID()),   -- ← UUID
  scheduleId     CHAR(36)     NOT NULL,                   -- ← UUID
  companyId      BIGINT       NOT NULL,
  consultRoomId  BIGINT       NULL,
  ...
  PRIMARY KEY (slotId),
  CONSTRAINT fk_slot_schedule FOREIGN KEY (scheduleId) REFERENCES appointment_schedule(scheduleId) ON DELETE RESTRICT,
```

**Java 映射冻结(238)**:

| 来源 | 行 | 内容 |
|---|---:|---|
| `238 §4.8` | 254 | `\| scheduleId \| scheduleId \| String \| 【OptFlow设计】 \|` |
| `238 §4.9` | 266 | `\| slotId \| slotId \| String \| 【OptFlow设计】 \|` |
| `238 §4.9` | 267 | `\| scheduleId \| scheduleId \| String \| 【OptFlow设计】 \|` |
| `236A` | 79-80 | `整数主键 = BIGINT NOT NULL AUTO_INCREMENT` / `UUID 主键 = CHAR(36) NOT NULL DEFAULT (UUID())` |
| `236B` | 298 / 330 | `12 PK(6 BIGINT AUTO_INCREMENT + 6 CHAR(36) UUID)` |
| `236B` | 332 | `FK 类型匹配 = 31/31 BIGINT ↔ BIGINT / CHAR(36) ↔ CHAR(36)` |

**G2-Contract-04 实际内容**:

| 位置 | API | 字段 | G2-04 写的类型 | 声称 Evidence | 238 实际 |
|---|---|---|---|---|---|
| line 241 | API-010 | `scheduleId` | `Long` | `238 §4.8` | `String` |
| line 253 | API-011 | `scheduleId` | `Long` | `238 §4.8` | `String` |
| line 263 | API-012 | `scheduleId` | `Long` | `238 §4.8` | `String` |
| line 273 | API-013 | `scheduleId` | `Long` | `238 §4.8` | `String` |
| line 297 | API-015 | `slotId` | `Long` | `238 §4.9` | `String` |

**裁决**:
- **5 处全部与所引证据直接矛盾**。这是本审计发现的最密集、最无解释空间的冲突簇。
- **DDL 不可实现性论证(新增,决定性)**:若采用 G2-04 的 `scheduleId | Long`,则 236A 的 `fk_slot_schedule FOREIGN KEY (scheduleId) REFERENCES appointment_schedule(scheduleId)` 将变成 **`CHAR(36) → BIGINT` 的跨类型外键**。
  - MySQL 要求 FK 两端类型**完全一致**(类型 + 长度 + 有符号性),`CHAR(36)` 与 `BIGINT` 不匹配 → **该 FK 无法创建**。
  - 这直接违反 `236B line 332` 已冻结的 `31/31 BIGINT ↔ BIGINT / CHAR(36) ↔ CHAR(36)`。
  - 同理 `appointment` 表的 `scheduleId` / `slotId` 两列(line 302-303)也必须为 `CHAR(36)`。
  - **裁决:G2-04 的 `Long` 不仅是类型标注错误,而是会使已冻结 DDL 在数据库层无法落地的阻断级错误。**
- **对照反证(排除"整体误用 Long"的可能)**:line 229 API-009 `employeeId | Long ✅ 238 §4.8` —— 238 §4.8 line 256 与 236A line 249 (`employeeId BIGINT`) 均为 `Long`,**这一处是对的**;line 283 API-014 `employeeId | Long ✅ 238 §4.8` 同样正确。
- 因此 `scheduleId/slotId → Long` **不是表述风格问题,而是 5 处独立的类型判定错误**。
- 附:238 §4.9 line 268 `companyId | Long【待确认】DB FK 暂未冻结` —— 对应 236A line 274 `companyId BIGINT NOT NULL COMMENT 'companyId scope 字段保留,DB FK 暂不创建(236A 修正)'`。G2-04 未处理该【待确认】标记。

---

### 4.4 P0-04 API-016 Transaction 参与者是否漏 Appointment 状态与 currentVisitId —— ❌ **确认违反**

**一手规则(233 API-016,line 700-705 + 726-730)**:

```
#### 2. 业务目的
**患者签到**(主路径)。**4 对象同步创建**:
- Appointment: WAITING_ARRIVAL → ARRIVED → TRIAGE_WAITING
- Visit: INSERT (DRAFT → CHECKED_IN)
- TriageQueue: INSERT (IN_POOL, employeeId=NULL, consultRoomId=NULL)
- **Appointment.currentVisitId = visit.id**(P0-1 修正)

#### 8. 状态迁移
- Appointment: WAITING_ARRIVAL → ARRIVED → TRIAGE_WAITING
- Visit: (none) → DRAFT → CHECKED_IN
- TriageQueue: (none) → IN_POOL
- currentVisitId: NULL → visit.id
```

233 §6 Response 另冻结:`data.currentVisitId ✓ = visitId`、`data.appointmentStatus ✓ = "TRIAGE_WAITING"`。

**G2-Contract-04 §7.3.1 实际内容(line 556-563)**:

| 维度 | G2-04 内容 |
|---|---|
| 业务动作 | 现场签到,创建 Visit(CHECKED_IN)+ TriageQueue(IN_POOL) |
| **参与对象** | **Visit(INSERT)+ TriageQueue(INSERT)** |
| 原子性证据 | **233 §6:"4 对象同步创建"**;参与对象写操作必须原子 |

**裁决**:
1. **自我否定**:G2-04 在"原子性证据"列**明确引用了"4 对象同步创建"**,却在"参与对象"列**只列出 2 个**。引用了正确规则却写出错误内容,属于可被内部一致性检查直接捕获的缺陷。
2. **遗漏 2 项**:
   - `Appointment.status`:`WAITING_ARRIVAL → ARRIVED → TRIAGE_WAITING`(两段迁移,非单段)
   - `Appointment.currentVisitId`:`NULL → visit.id`
3. **遗漏 1 项约束**:TriageQueue 插入时 `employeeId=NULL, consultRoomId=NULL`(233 line 704 冻结)。
4. **回滚范围随之失效**:G2-04 写"任一操作失败,全部回滚",但只声明了 2 个对象的原子性,Appointment 更新失败时的回滚边界未定义。
5. **未登记的证据冲突(额外发现)**:238 §19 T02(line 958)记 `Appointment.status=ARRIVED`(无 TRIAGE_WAITING),与 233 §8 的终态 `TRIAGE_WAITING` 存在**证据层冲突**。G2-04 既未采用 233,也未将该冲突登记为【D】——属"通过省略规避裁决" → 见 P1-04。

---

### 4.5 P0-05 API-021 是否把确定业务动作写成"可能" —— ❌ **确认违反**

**一手规则(双源确认)**:

| 来源 | 行 | 内容 |
|---|---:|---|
| `233 API-021 §5-14` | 814 | `状态迁移:TriageQueue IN_POOL → ASSIGNED + ReceptionQueue INSERT(ASSIGNED)+ Appointment → WAITING_RECEPTION + Visit → TRIAGED` |
| `238 §19 T04` | 960 | `TriageQueue.status=ASSIGNED, ReceptionQueue(新)=ASSIGNED, Appointment.status=WAITING_RECEPTION, Visit.status=TRIAGED` &#124; 涉及 Entity:`TriageQueue + ReceptionQueue + Appointment + Visit` |

**G2-Contract-04 §7.3.2 实际内容(line 570)+ §7.4(line 604)**:

```
| **参与对象** | TriageQueue(UPDATE: IN_POOL → ASSIGNED)+ ReceptionQueue(INSERT)+ Appointment(status 更新可能)|
...
| API-021 | 分配检查室 | TriageQueue + ReceptionQueue(+ Appointment 可能)| 【待确认】 | 业务复杂度已知 |
```

**裁决(两个独立缺陷)**:

| # | 缺陷 | 233 | 238 T04 | G2-04 | 性质 |
|:-:|---|---|---|---|:-:|
| a | Appointment 动作 | `→ WAITING_RECEPTION`(确定)| `=WAITING_RECEPTION`(确定)| **"可能"** | ❌ **语义降级** |
| b | `Visit → TRIAGED` | 明确列出 | 明确列出 | **完全缺失** | ❌ **参与对象遗漏** |

- 两个独立一手源(233 + 238 T04)均把 4 个动作写为**确定性断言**,G2-04 却将其中 1 个降级为"可能"、另 1 个整条删除。
- G2-04 §7.3.2 的"业务动作"列写 `分配检查室 + 创建 ReceptionQueue`,**同样未包含 Visit → TRIAGED**,说明遗漏贯穿两列,非单点笔误。
- 全文 `可能` 仅 2 次命中,**全部集中在 line 570 与 604,即 P0-05 现场**。这是"为规避冲突而主动弱化"的特征,不是无意的措辞。
- **自检漏项**:§18.2 的 15 项关键词表中**没有** `可能` / `可选` / `视情况` / `或许`,因此该弱化在 G2-04 自检中**必然漏过**。

---

## §5 主动扫描发现的其他新问题

### 5.1 P0-06 Service 纪律回归:Repository 方法被升级为 Service 冻结(重开 P1-A1)

**G2-Contract-04 §6.2 自我声明与实际行为冲突**:

- §6.2 修复策略原文:`- 沿用 R2 §七 纪律(Repository ≠ Service)` / `- 严禁把 Repository 方法升级为 Service 冻结`
- §6.3 诚实标注原文:`G2-Contract-04 GAP-02 修复**保持 R2 §七 纪律**,严禁把 Repository 方法升级为 Service 冻结`

**但同一节内 7 处直接违反**:

| 位置 | 方法 | G2-04 Status |
|---|---|---|
| line 447 | `findByCompanyIdAndAdminId(Long, Long)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 448 | `findByCompanyIdAndRole(Long, String)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 458 | `findByCustomerId(Long)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 459 | `findByCompanyId(Long)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 467 | `findByCompanyId(Long)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 474 | `findByCompanyId(Long)` | **冻结**(Repository 方法,允许 Service 复用)|
| line 482 | `findByCompanyIdAndSceneType(Long, String)` | **冻结**(Repository 方法,允许 Service 复用)|

**回归基线(必须保持的冻结)**:

| 来源 | 行 | 内容 |
|---|---:|---|
| `G2-Contract-03 §3 FA-09` | 118 | `6 Service 方法 Contract 全部【待确认】(**Repository 证据不升级**)` |
| `G2-Contract-03 §6.2.2` | 344 | `findByCompanyId(companyId)(Repository 方法) \| **【待确认】** \|` |
| `G2-Contract-03 §6.2.3` | 351 | 同上 **【待确认】** |
| `G2-Contract-03 §6.2.4` | 358 | 同上 **【待确认】** |
| `G2-Contract-03 §16.1 P1-A1` | 696 | `RC-η(Repository 升 Service) \| FA-09 \| §6.2 \| **✅ 已修复**` |

**裁决**:
- 这 7 个方法与 G2-Contract-03 §6.2 的对应行**逐字相同**,唯一差异是 Status 从 **【待确认】** 变成 **冻结**。
- 措辞"**允许 Service 复用**"是本轮**新造的授权性表述**,G2-Contract-03 无此措辞。它把"Repository 存在该方法"升格为"Service 冻结该方法",正是 P1-A1 的原始缺陷形态。
- **G2-04 §16.1 line 705 同时声称**:`P1-A1 ~ A4 + P1-B1 / B2 / B6(7 项 P1 全部已修复)` —— **与 §6.2 现状直接矛盾**。
- `G2-Contract-Audit-03` 判 PASS 的正是"历史 Contract 冲突已修复"。G2-04 在继承其结论的同时,重新打开了其中 2 项。

---

### 5.2 P0-07 自创 Service 方法改名回流:`parseConsultRoomIdArrayJson`

**G2-Contract-04 §6.2.4(line 475)与 §6.2.5(line 483)并列**:

```
§6.2.4 ConsultRoomService
| `parseConsultRoomIdArray(Long bigScreenId)`(❌ G2-01 自创)| ... | **删除**(G2-03 §6.2.5 已删除)|

§6.2.5 BigScreenService
| `parseConsultRoomIdArrayJson(String consultRoomIdArrayJson)` | String | `List<Long>` | ... | **冻结业务规则**;完整方法签名【待确认】|
```

**裁决(3 层)**:

1. **改名回流**:G2-Contract-03 FA-10(line 119)+ P1-A2(line 697)冻结为**删除**自创 `parseConsultRoomIdArray`。G2-04 保留了删除标记,却在同一文档内新增 `parseConsultRoomIdArrayJson` —— **同一概念族,加后缀 `Json` 后重新作为 Service 方法出现**。
2. **证据污染**:`List<Long>` 作为返回值被呈现。238 §15.2 明确:
   - 选项 A `String consultRoomIdArray` = 【OptFlow设计】(冻结)
   - 选项 B `List<Long> consultRoomIdList` = **【待确认】(需查现有项目 ORM 习惯)** / 不推荐
   - 238 §4.6 line 216 + §5.1 line 340 冻结的是 `String` + **应用层手工解析 JSON**

   G2-04 把【待确认】选项 B 提升为方法签名的返回类型,违反其自定 §2.2 **【E】AI 推断(严禁)**。
3. **已冻结业务规则被弱化并丢失**:238 §15.4(line 837-856)冻结的 Service 层处理包含 3 件事:
   - JSON 解析出 `List<Long> roomIds`
   - 写入时 `writeValueAsString`
   - **跨公司校验**:`CONSULT_ROOM_NOT_FOUND` / `CROSS_COMPANY_VIOLATION` 异常 + 每个 roomId 必须属于同 companyId

   G2-04 只保留了"`consultRoomIdArray` 是 JSON 字段"这一**远弱于 §15.4** 的表述,**丢失了已冻结的异常契约**。

**自检假 PASS(本轮指定核查项)**:

- G2-04 §18.2 line 768:`| **parseConsultRoomIdArray** | (严禁说明 / 已删除)| ❌ | ✅ |`
- 独立检索实测:`parseConsultRoomIdArray` 命中 **4 次**,其中 **line 483 是活跃 Service 方法行**;`parseConsultRoomIdArrayJson` 命中 1 次(line 483)。
- 该 banned token 作为前缀完整包含在活跃方法名中。**G2-04 的"仅说明文"结论为假**。
- 这正是本轮要求核查的"精确关键词 PASS,但改名/后缀后实际仍存在"漏洞,**已实证存在**。

---

### 5.3 P0-08 伪造异常常量与错误证据归属:`EMPLOYEE_DISABLED` / `60004`

**G2-Contract-04 §6.2.1 line 451 原文**:

```
| `validateEmployeeActive(Long employeeId)` | Long | `void` | `BusinessException(EMPLOYEE_DISABLED, 60004)` | 读
| 235B §2 + 241V2A-17 §3.2 | **【待确认】**(方法名称 + 异常 code 60004 **已冻结**,但 Employee.status 业务枚举【待确认】)|
```

**裁决(4 项)**:

1. **`EMPLOYEE_DISABLED` 全库不存在**。独立检索:整个 workspace 该常量**仅出现 1 次,即 G2-04 第 451 行自身**。
2. **`60004` 的冻结值是 `USER_DISABLED`**:

| 来源 | 行 | 内容 |
|---|---:|---|
| `241V2A-17 §3.3` | 197 | `\| **60004** \| **USER_DISABLED** \| 用户已禁用 \| 241V2A-17 冻结 \|` |
| `241V2A-17 §3.2` | 166 | `UserDisabledException 完整类定义`(**User 域,非 Employee 域**)|
| `241V2A-19` | 254 | `60004 USER_DISABLED = 【OptFlow设计】` |

3. **6xxx 段已满,且明文禁止扩域**:

| 来源 | 行 | 严禁条款 |
|---|---:|---|
| `241V2A-17 §3.3` | 205 | `✗ 不得跳号` |
| `241V2A-17 §3.3` | 207 | `✗ 不得新增 USER_LOCKED / USER_EXPIRED 等其他 User 异常 ResultCode(本轮仅冻结 60003 / 60004)` |

   60000~60004 全部占满。`EMPLOYEE_DISABLED` 在该段内**无编号可用**,把它挂到 60004 会与已冻结的 `USER_DISABLED` 语义直接冲突。Employee 域错误码需要**新的编码段裁决** —— 这是一项**尚未做出的【OptFlow设计】决策**,不是"已冻结"。

4. **证据等级被抹去**:G2-04 标"异常 code 60004 **已冻结**"。而 241V2A-18 §1.3.2(line 116)+ 241V2A-19(line 254)明确将 60003/60004 的证据等级校正为 **【OptFlow设计】**(**非**原系统直接观测)。G2-04 未标注证据等级,把设计值当既有冻结事实使用。

**同一行的第二个引用错误(line 450)**:

```
| `getCurrentEmployee()`(获取当前登录 employee) | ... | 业务规则来源: `235B §2 adminId 校验` |
```

`235B §2`(line 40-62)实际冻结内容:

```
### 2.2 最终规则(本版冻结)
| Employee.adminId 是否 NOT NULL | ✓ NOT NULL(强制必填) |
| Employee.adminId 是否 UNIQUE  | ✓ UNIQUE(companyId, adminId)组合唯一 |
| "每个 Employee 必有 admin 账号" | ✓ 是,严格强制 |
```

这是**数据模型 / DDL 裁决**,**不包含任何"获取当前登录 employee"的规则**。以此作为 `getCurrentEmployee()` 的业务规则来源属**证据归属错误**。

---

### 5.4 P1-01 GAP-01 覆盖率统计口径失真

**G2-04 §3.8 line 382 声明**:

```
- **40 / 40 API Request DTO + Response VO 已建立 Contract**
```

**实际内容**:

| API 区间 | G2-04 §3 的记录方式 | 是否逐 API |
|---|---|:-:|
| API-001~008 | 独立小节 + 字段表 | ✅ |
| API-009~015 | 独立小节 + 字段表 | ✅ |
| **API-016~018** | §3.4 每 API **仅 2 行**"【待确认】","(233 §6 未冻结完整字段表)" | ❌ 无 DTO 类名 |
| **API-019~023** | §3.5 每 API **仅 2 行**"【待确认】" | ❌ |
| **API-024** | §3.6 **仅 2 行**"【待确认】" | ❌ |
| **API-025~040** | §3.7 **合并为 1 行**:`\| API-025 ~ API-040 \| 【待确认】 \| 【待确认】 \|` | ❌ **16 个 API 全部无独立记录** |

- GAP-01 的 Gate 要求(用户原始指令)是**"API-001 ~ API-040 完整覆盖矩阵"**,且明确要求列出 **DTO 类名 / VO 类名 / 字段 / 类型 / 必填 / 默认值 / 枚举 / 含义 / 使用范围**。
- G2-04 对 **25 个 API** 连 DTO 类名都没有给出,仅以"【待确认】"占位。
- **自相矛盾**:§18.1 line 750-751 自报 DTO Request 完整率 **5.0%**、Response 完整率 **5.0%**,却与 §3.8 的"40/40 已建立 Contract"并列陈述。**同一文档两个口径**。
- **裁决:GAP-01 未关闭。**"建立矩阵行"≠"字段级映射"。

---

### 5.5 P1-02 §3.8 / §6.3 / §18.1 / §19 统计数字互不自洽

| 表 | 声明 | 算术校验 | 裁决 |
|---|---|:-:|---|
| §3.8 line 383-385 | 2 A + 13 C + 25 待确认 = **40** | ✅ 自洽 | — |
| §18.1 line 750 (Request) | 冻结 2 + 部分 13 + 待确认 25 = **40** | ✅ 自洽 | — |
| §18.1 line 751 (Response) | 冻结 2 + 部分 **0** + 待确认 **38** = **40** | ✅ 算术自洽 | ❌ **分类与 §3.8 冲突** |
| §6.3 line 505 | 20 方法 = 冻结 7 + 待确认 13 | ✅ 自洽 | ❌ **分母口径失真** |
| §19 line 805 | Pending Confirmation = **20 项** | ❌ | ❌ **无法从文中复算** |

**具体冲突**:

1. **同一 13 个 API 在两表分类不同**:§3.8 判定 API-002/003/005/006/007/008/009/010/011/012/013/014/015 为"部分冻结(C)",§18.1 Response 侧却把同样这批 API 全部归入"待确认 38"(部分 = 0)。至少一张表的分类是错的。
2. **§6.3 的"关键方法数 = 20"不可复核**:6 个 Service 的行中包含 3 行**"其它 CRUD 方法"占位行**、**1 行"已删除"**(line 449 `getEmployeeByLogin`)、**1 行"公司初始化/SaaS 初始化"已删除**(line 491)。把"已删除"和占位行计入 Service 关键方法分母,使 §19 line 813 对 S1-170E §13.4 硬阻塞 **2c** 的自评"⚠️ 部分修复"偏乐观。
3. **§19 的 20 项无法复算**:§13.1 列 10 行(其中 #9-18 合并为 1 行)、§17.2 列 11 行,两表内容高度重叠,§3 另有大量字段级【待确认】未计入。20 这个数字在文中任何一处都推导不出。
4. **"7 个已冻结"的水分**:其中 6 个是 Repository 复用(P0-06),1 个是 `parseConsultRoomIdArrayJson` 的"冻结业务规则"但签名【待确认】(P0-07)。**真正的 Service 方法冻结数 = 0**。

---

### 5.6 P1-03 §6.2 冻结口径把 Repository 复用计入 Service 冻结数

见 5.1 / 5.5 第 2、4 点。独立列为 Issue 的理由:这不只是 P0-06 的重复描述,而是**统计口径缺陷** —— 它使 GAP-02 的完成度被系统性高估,直接影响 S1-170E §13.4 硬阻塞 2c 的判定。

---

### 5.7 P1-04 API-025 / API-016 的未登记冲突

| # | 冲突 | 来源 | G2-04 处理 |
|:-:|---|---|---|
| a | 233 API-025 §4 line 902 Request 含 `companyId` uuid ✅ 必填(**违反 241V2 §4.4**)| 233 line 902-908 | §3.7 整体标【待确认】,**未登记冲突** |
| b | 238 §19 T03 line 959 记 API-025 结果 `Visit + TriageQueue, appointmentId=NULL`;§7.3.3 未说明 Appointment 是否参与 | 238 line 959 | §7.3.3 只写 `Visit + TriageQueue` |
| c | 233 §8 line 727 `Appointment → TRIAGE_WAITING` vs 238 §19 T02 line 958 `Appointment.status=ARRIVED` | 双源冲突 | **两源均未采用,冲突未登记为【D】** |
| d | `234A §4.1 line 358` 判定 `233 §API-021 Request` 的 `employeeId / consultRoomId = uuid` 为**错误** | 234A line 358 | §7.3.2 讨论 API-021 但 DTO 全【待确认】,**该纠错未继承也未登记** |
| e | `234A` 的 `Long/BIGINT` 结论证据等级 = **A(非 UUID)+ E(Long 推断)**,非纯 A 级事实 | 234A §5.1 / §5.2 | §3.8 将 API-001 标为 `Evidence Grade = A`,**抹掉了 E 级成分** |

**裁决**:通过"整体标【待确认】"或"省略字段"规避裁决,不满足本轮"冲突必须登记"的要求。API-025 实际处于**未裁决状态**。

---

### 5.8 P1-05 §18.2 关键词自检不可复现 / 覆盖不足

**G2-04 §18.2 声明检查 15 项。**本轮指定的必查词中,**以下 12 项完全不在自检表内**:

`companyId` / `defaultCompanyId` / `String(uuid)` / `Long` / `scheduleId` / `slotId` / `parseConsultRoomIdArrayJson` / `getCurrentEmployee` / `validateEmployeeActive` / `EMPLOYEE_DISABLED` / `可能` / `可选`

**已实证的漏检**:

| 漏检词 | 实际命中 | 自检结果 |
|---|---:|---|
| `parseConsultRoomIdArrayJson` | line 483(活跃 Service 方法行)| ❌ 自检表无此项,且 `parseConsultRoomIdArray` 行判"✅ 仅说明文" |
| `可能` | line 570, 604(正是 P0-05 现场)| ❌ 自检表无此项 |
| `EMPLOYEE_DISABLED` | line 451 | ❌ 自检表无此项 |

**方法论缺陷**:§18.2 为**人工填写的结论表**,不含可复现的检索命令与行号输出,无法作为 Gate 证据。**G2-04 自称的 "Keyword scan = PASS" 不可采信**。

---

### 5.9 P1-06 §16.1 用历史 Issue 编号为当前状态背书

**G2-04 §16.1 line 704-706**:

```
- P0-A1 ~ A4 + P0-A5 ~ A20 + P0-B1 ~ B5(25 项 P0 全部已修复)
- P1-A1 ~ A4 + P1-B1 / B2 / B6(7 项 P1 全部已修复)
- 文字不一致 P1-1 / P1-2(本轮 G2-04 §13 已修复)
```

**实际**:

| 声称 | 现状 |
|---|---|
| `P1-A1(RC-η Repository 升 Service)` ✅ 已修复 | ❌ §6.2 line 447/448/458/459/467/474/482 **7 处重开** |
| `P1-A2(RC-η 自创 parseConsultRoomIdArray)` ✅ 已修复 | ❌ §6.2.5 line 483 **改名重开** |
| `P0-* 25 项全部已修复` | 未能独立复核(引用式继承),且 P0-08 与 241V2A-17/18/19 冲突 |

**裁决**:以历史 Issue 编号的历史结论替代本轮独立核验,违反"独立证据链"要求。**该节不能作为回归证明**。

---

### 5.10 P2-01 ~ P2-05

| # | Issue | 位置 | 证据 |
|:-:|---|---|---|
| **P2-01** | 引用精度停留在模块级,无法定位到条目 | §7.3.1 line 560 写 `233 §6:"4 对象同步创建"`,但该规则实际在 233 的 **API-016 §2(业务目的)与 §8(状态迁移)**;233 §6 是 **Response 字段表**。§3.2 反复写 `233 §4 #4`,`#4` 是小节号而非行号 | 233 line 700-730 / 718-724 |
| **P2-02** | 把技术推断写进 Contract 表格单元 | §7.3.1 line 562 `基于"4 对象同步创建"业务复杂度,**推断倾向** multi-object atomic`;§7.3.2 line 574 `基于业务复杂度…**推断倾向** concurrency-sensitive` | — |
| **P2-03** | nullability 表述自相矛盾 | §3.2 line 117:`data.currentVisitId \| String(uuid) \| ✅(必填)\| **NULL**`。字段"必填 ✅"与"值恒为 NULL"并列,实现者无法判断是"键必存在但值为 null"还是"键可缺失" | 233 line 201 `currentVisitId: NULL` / line 723 `data.currentVisitId ✓ = visitId` |
| **P2-04** | Service 计数把"已删除"与占位行计入分母 | §6.3 line 499 `EmployeeService 关键方法数 = 6`,其中含 1 行"已删除"(line 449)+ 1 行"其它 CRUD"占位 | §6.2.1 |
| **P2-05** | Pending Confirmation 计数无法复算 | §19 line 805 `Pending Confirmation = 20 项`,而 §13.1(10 行)/ §17.2(11 行)/ §3(字段级)三处均无法加总出 20 | — |

**P2-02 补充说明**:虽标注"严禁自行升级为冻结",但把推断文本放进 Contract 的表格单元,后续版本极易被当作已决结论继承。**推断应移出 Contract,仅留在审计或待确认清单**。

---

## §6 历史 GAP 关闭状态裁决

### 6.1 Historical G2-Ready Gaps

`G2-READY-Gate-Audit-01 §7.2` 列出 **5 项**最小闭环缺口。G2-04 §19 自身也确认为 5 项:

| # | Gap | 来源 |
|:-:|---|---|
| 1 | API → Controller / DTO / VO 字段级映射 | §7.2 #1 |
| 2 | Service 关键方法签名(与"关键方法签名"合并)| §7.2 #2 + #4 |
| 3 | Transaction boundary 精确划分(API-016/021/025/037)| §7.2 #3 |
| 4 | Dev Environment 可用性证据 | §7.2 #5 |
| 5 | Permission Matrix 40×6 | §7.2 |

### 6.2 逐项关闭裁决

| # | Gap | G2-04 自评 | **本审计独立裁决** | 依据 |
|:-:|---|---|:-:|---|
| 1 | DTO/VO 字段级映射 | ⚠️ 部分修复 | ❌ **未关闭** | 25/40 API 零字段;16 个 API 合并为 1 行占位;连 DTO 类名都未给出;§18.1 自报完整率 5.0% |
| 2 | Service 关键方法签名 | ⚠️ 部分修复 | ❌ **未关闭** | 7 个"冻结"中 6 个是 Repository 复用(P0-06);真正的 Service 冻结数 = 0;20 个方法中含占位/已删除行 |
| 3 | Transaction boundary | ⚠️ 部分修复 | ❌ **未关闭且倒退** | API-016 漏 2 项参与对象;API-021 漏 1 项 + 弱化 1 项;4/4 分类仍【待确认】 |
| 4 | Dev Environment | ⚠️【待确认】 | ✅ **按要求未编造** | §19.2 正确标【待确认】,本轮不属 Contract 文本修复对象 |
| 5 | Permission Matrix 40×6 | ✅ 沿用 | ✅ **文字漏标已修** | §13.1 #8 / §17.2 #8 显式标【待确认】,与 Audit-03 一致 |

```
Historical G2-Ready Gaps  =  5
Contract Gaps Closed      =  1  (仅 Gap #5 文字漏标修复)
Still Open                =  4  (Gap #1 / #2 / #3 / #4)
```

> **说明**:G2-04 §19 自报 `Contract Gaps Closed = 0 / Remaining = 5`。本审计采信该**数字口径**但修正其**归因** —— Gap #5 的文字漏标确已修复,故 Closed = 1、Remaining = 4。**无论按哪个口径,3 个目标 GAP(GAP-01/02/03)均未关闭。**

---

## §7 Issue 汇总

### 7.1 New P0(8 项)

| ID | Issue | 位置 | 违反的一手基线 | Root Cause | Fix Action |
|:-:|---|---|---|---|---|
| **P0-01** | 业务 Request DTO 重新暴露 `companyId`,标 A 级"已冻结" | §3.2 line 98 / §3.3 line 228 / §3.8 line 364 | `241V2 §4.4`(✗ 不得含 companyId/defaultCompanyId/任何 company scope 字段);`241A-1 §10`;`240 §18` | **RC-A** | **FA-01 + FA-02** |
| **P0-02** | 复用实体 ID(`companyId`/`patientId`/`employeeId`)错写 `String(uuid)`;line 228 引用 238 §4.8 而该节写 `Long` | §3.2 line 98-100 / §3.3 line 228 | `238 §2.1/§3.1/§4.6 line 213/§4.8 line 255-256`;`236B line 298/330/332` | **RC-B + RC-C** | **FA-03** |
| **P0-03** | `scheduleId`(4 处)/ `slotId`(1 处)错写 `Long`,且均与所引 238 §4.8/§4.9 内容直接矛盾 | §3.3 line 241/253/263/273/297 | `238 §4.8 line 254`;`238 §4.9 line 266-267`;`236B line 298` | **RC-C** | **FA-04** |
| **P0-04** | API-016 参与对象只列 2 个,漏 `Appointment` 两段状态迁移 + `currentVisitId`;引用了"4 对象"却写 2 个 | §7.3.1 line 558-563 | `233 API-016 §2 line 700-705`;`§8 line 726-730`;`§6 line 718-724` | **RC-D** | **FA-05 + FA-07** |
| **P0-05** | API-021 `Appointment → WAITING_RECEPTION` 被弱化为"可能";`Visit → TRIAGED` 完全缺失 | §7.3.2 line 570 / §7.4 line 604 | `233 line 814`;`238 §19 T04 line 960`(双源确定)| **RC-E** | **FA-06** |
| **P0-06** | 7 个 Repository 方法被升级为 Service **冻结**,重开 P1-A1;与 §6.2/§6.3 自定纪律及 §16.1 声称直接矛盾 | §6.2 line 447/448/458/459/467/474/482 | `G2-Contract-03 FA-09 line 118`;`G2-Contract-03 §6.2 line 344/351/358`;`G2-Contract-03 §16.1 P1-A1 line 696` | **RC-F** | **FA-08 + FA-13** |
| **P0-07** | 自创 `parseConsultRoomIdArray` 加后缀 `Json` 回流;`List<Long>` 把 238 §15.2 的【待确认】选项升为冻结;丢失 238 §15.4 跨公司校验与异常契约;§18.2 判"仅说明文"为假 | §6.2.5 line 483 / §18.2 line 768 | `G2-Contract-03 FA-10 line 119`;`P1-A2 line 697`;`238 §4.6 line 216`;`§5.1 line 340`;`§15.2 line 821-825`;`§15.4 line 837-856` | **RC-F + RC-H** | **FA-09 + FA-12 + FA-13** |
| **P0-08** | 伪造 `EMPLOYEE_DISABLED` 常量并冒用 `60004`(实为 `USER_DISABLED`),6xxx 段已满且明文禁止扩域;`getCurrentEmployee` 证据来源错配(235B §2 = adminId NOT NULL,非登录态规则)| §6.2.1 line 450-451 | `241V2A-17 §3.2 line 166` / `§3.3 line 197/205/207`;`241V2A-18 §1.3.2 line 116`;`241V2A-19 line 254`;`235B §2 line 40-62` | **RC-G** | **FA-10 + FA-11** |

### 7.2 New P1(6 项)

| ID | Issue | 位置 | Root Cause | Fix Action |
|:-:|---|---|:-:|---|
| **P1-01** | GAP-01 以"合并行 + 占位"充数,16 个 API 无独立记录,连 DTO 类名都未给;与 §18.1 自报 5.0% 完整率矛盾 | §3.4 / §3.5 / §3.6 / §3.7 line 354-358 / §3.8 line 382 | **RC-A + RC-C** | **FA-15 + FA-14** |
| **P1-02** | §3.8 / §6.3 / §18.1 / §19 四个统计表互不自洽;同一 13 个 API 在 Request/Response 侧分类不同;20 个关键方法含占位与"已删除"行 | §3.8 / §6.3 line 505 / §18.1 line 750-751 | **RC-C** | **FA-14** |
| **P1-03** | 6 个"冻结"中 6 个是 Repository 复用、1 个签名【待确认】 → **真正的 Service 冻结数 = 0**,使硬阻塞 2c 完成度被系统性高估 | §6.3 line 505 / §19 line 813 | **RC-F** | **FA-14** |
| **P1-04** | **5 项**已识别的证据冲突(API-025 `companyId`、API-025 Appointment 参与、233 vs 238 T02 终态、`234A` 对 233 API-021 的 uuid 纠错、证据等级 A/E 误标)**未登记为【D】**,以"标【待确认】/省略"规避裁决 | §3.7 line 358 / §7.3.3 line 581-586 | **RC-A** | **FA-07** |
| **P1-05** | §18.2 自检表缺 12 个必查词,含全部 8 个 P0 的定位词;无行号输出、不可复现;"Keyword scan = PASS" 不可采信 | §18.2 line 756-774 | **RC-H** | **FA-12** |
| **P1-06** | §16.1 以历史 Issue 编号为当前状态背书,其中 P1-A1 / P1-A2 实际被本轮重开 | §16.1 line 704-706 | **RC-F** | **FA-13** |

### 7.3 New P2(5 项)

| ID | Issue | 位置 | Root Cause | Fix Action |
|:-:|---|---|:-:|---|
| **P2-01** | 引用停留在模块级(`233 §6`),实际规则在 §2/§8;`#4` 为小节号非行号 → 引用与内容错配无法被内部检查发现 | §7.3.1 line 560 / §3.2 | **RC-C** | **FA-16** |
| **P2-02** | 技术推断("推断倾向 multi-object atomic" / "concurrency-sensitive")被写入 Contract 表格单元,易被后续版本继承为结论 | §7.3.1 line 562 / §7.3.2 line 574 | **RC-C** | **FA-17** |
| **P2-03** | `data.currentVisitId` "✅ 必填" 与 "值恒为 NULL" 并列,nullability 无法判定 | §3.2 line 117 | **RC-C** | **FA-18** |
| **P2-04** | Service 关键方法分母含"已删除"行与"其它 CRUD"占位行,覆盖率失真 | §6.3 line 499-505 | **RC-C** | **FA-19** |
| **P2-05** | §19 `Pending Confirmation = 20 项` 在文中任何一处均无法复算 | §19 line 805 | **RC-C** | **FA-14** |

---

## §8 Root Cause(8 项,不合并)

| ID | Root Cause | 触发 Issue |
|:-:|---|---|
| **RC-A** | **证据基线表不完整**:§2 把 `241V2 §4-§6` 概括为 "CompanyContext + TenantLine",**§4.4 DTO 隔离从未进入证据链**。上位禁令缺席 → 下位旧写法无阻力复制 | P0-01, P1-01, P1-04 |
| **RC-B** | **沿用前序文档时未执行生命周期裁决**:233(S1-167)的 `uuid` 文本被直接复制并升级为 A 级冻结,未对照 238/236B(S1-169)后序覆盖 | P0-02 |
| **RC-C** | **引用来源与被引内容未做一致性校验**:5 处 `scheduleId/slotId → Long` 与 1 处 `companyId → String(uuid)` 均在**引用 238 §4.8/§4.9 的同时**与之矛盾;统计口径与引用精度也未交叉校验 | P0-02, P0-03, P1-01, P1-02, P2-01~P2-05 |
| **RC-D** | **多对象规则在转写时被压缩**:API-016 的"4 对象同步创建"被压缩为 2 个参与对象,且保留了"4 对象"的引用文字,形成自我否定 | P0-04 |
| **RC-E** | **确定性业务动作在转写时被语义降级**:`Appointment → WAITING_RECEPTION` → "可能";`Visit → TRIAGED` → 整条删除。全文"可能"仅 2 次,全部集中于该处 | P0-05 |
| **RC-F** | **上一轮已判修复的 Issue 未设置回归锁**:P1-A1 / P1-A2 在 §16.1 被声称"已修复"的同时于 §6.2 被重开;Repository 复用计数又反向掩盖了重开事实 | P0-06, P0-07, P1-03, P1-06 |
| **RC-G** | **异常常量与错误码缺少全库唯一性检索**:`EMPLOYEE_DISABLED` 未做全库检索即写入;`60004` 未核对其冻结语义归属与 6xxx 段容量;`getCurrentEmployee` 未核对 235B §2 实际内容 | P0-08 |
| **RC-H** | **自检表为人工填写且关键词集合与风险面不匹配**:缺 12 个必查词(含全部 8 个 P0 定位词),无行号输出、不可复现,导致"改名回流"与"弱化描述"必然漏过 | P0-07, P1-05 |

---

## §9 Fix Action(19 项)

| ID | Fix Action | 对应 Issue | 优先级 |
|:-:|---|---|:-:|
| **FA-01** | 删除 API-001 / API-009 Request DTO 的 `companyId` 行,改为显式引用 241V2 §4.4 禁令 + 后端从 `CompanyContext.getCompanyId()` 注入 | P0-01 | **P0** |
| **FA-02** | §2 Evidence 表补入 `241V2 §4.4`(DTO 隔离)、`240 §18`、`241A-1 §10`;并将 `241V2 §4-§6` 的概括拆分为可定位条目 | P0-01 | **P0** |
| **FA-03** | 全文将 6 个**复用** ID(`companyId`/`customerId`/`patientId`/`employeeId`/`consultRoomId`/`bigScreenId`)改为 `Long`,依据 238 §2.1/§3.1 + 236B | P0-02 | **P0** |
| **FA-04** | 全文将 6 个**新建** ID(`scheduleId`/`slotId`/`appointmentId`/`visitId`/`triageQueueId`/`receptionQueueId`)改为 `String`,依据 238 §3.2/§4.8/§4.9 + 236B;并逐处复核"引用 vs 内容"一致 | P0-02, P0-03 | **P0** |
| **FA-05** | 重写 §7.3.1 API-016 参与对象为 **4 项**:Appointment 两段状态迁移 + Visit INSERT + TriageQueue INSERT + `currentVisitId: NULL → visit.id`;补 TriageQueue `employeeId=NULL, consultRoomId=NULL` 约束 | P0-04 | **P0** |
| **FA-06** | 重写 §7.3.2 与 §7.4 的 API-021 参与对象为 **4 项确定动作**,删除全部"可能"表述 | P0-05 | **P0** |
| **FA-07** | 登记 **5 项**未裁决冲突为【D】:233 §8 `TRIAGE_WAITING` vs 238 §19 T02 `ARRIVED`;API-025 是否含 Appointment 参与;API-025 `companyId` 与 241V2 §4.4;`234A §4.1 line 358` 对 233 API-021 `employeeId/consultRoomId = uuid` 的纠错;`234A` 的 A+E 混合证据等级被误标为纯 A | P0-04, P1-04 | **P0** |
| **FA-08** | 回滚 §6.2 的 7 处 Repository→Service 冻结,恢复 G2-Contract-03 §6.2 的 **【待确认】**;删除"允许 Service 复用"这一新造授权表述 | P0-06 | **P0** |
| **FA-09** | 删除 `parseConsultRoomIdArrayJson`;如需保留 238 §15.4 业务规则,改为**无方法名**的规则描述,并补回 `CONSULT_ROOM_NOT_FOUND` / `CROSS_COMPANY_VIOLATION` 跨公司校验与异常契约 | P0-07 | **P0** |
| **FA-10** | 删除 `EMPLOYEE_DISABLED` 与 `60004` 的归属;改为【待确认】并说明 6xxx 段 60000~60004 已满、Employee 域错误码需独立编码段裁决;补标 60003/60004 证据等级 = 【OptFlow设计】 | P0-08 | **P0** |
| **FA-11** | 修正 `getCurrentEmployee` 的证据来源:235B §2 = `Employee.adminId NOT NULL + UNIQUE(companyId, adminId)` 数据模型裁决,**不构成**登录态获取规则 | P0-08 | **P0** |
| **FA-12** | §18.2 重做为**可复现检索清单**,补入 `companyId` / `defaultCompanyId` / `String(uuid)` / `Long` / `scheduleId` / `slotId` / `parseConsultRoomIdArrayJson` / `getCurrentEmployee` / `validateEmployeeActive` / `EMPLOYEE_DISABLED` / `可能` / `可选` / `视情况`,每项附命中行号;将 `parseConsultRoomIdArray*` 视为**同一概念族**整体判定 | P0-07, P1-05 | **P0** |
| **FA-13** | 为 P1-A1 / P1-A2 建立**回归锁**条目,禁止后续版本重开;§16.1 改为引用本轮独立核验结论,不得以历史编号背书 | P0-06, P0-07, P1-06 | **P0** |
| **FA-14** | 统一 §3.8 / §6.3 / §18.1 / §19 统计口径,每个数字可从文中复算;Service 关键方法分母剔除"已删除"与占位行;`Pending Confirmation` 给出可加总明细 | P1-01, P1-02, P1-03, P2-05 | P1 |
| **FA-15** | API-016 ~ API-040 **逐 API** 建立 DTO/VO 记录(即使全部为【待确认】亦须逐条列出 DTO 类名 + 字段占位),不以合并行充数 | P1-01 | P1 |
| **FA-16** | 引用精度从模块级提升到条目级(`233 API-016 §2/§8` 而非 `233 §6`);字段级引用补行号 | P2-01 | P2 |
| **FA-17** | §7.3 中"推断倾向 multi-object atomic" / "concurrency-sensitive" 等推断语句**移出 Contract 表格**,仅保留于待确认清单 | P2-02 | P2 |
| **FA-18** | 修正 API-001 `data.currentVisitId` nullability 表述为"键必存在 / 值恒为 null",依据 233 line 201 | P2-03 | P2 |
| **FA-19** | §6.3 `EmployeeService 关键方法数` 等分母剔除"已删除"行(3 处)与"其它 CRUD"占位行(6 处) | P2-04 | P2 |

---

## §10 最终统计(Issue / Root Cause / Fix Action 分别计数)

| 维度 | 数量 |
|---|---:|
| **Historical G2-Ready Gaps** | **5** |
| **Contract Gaps Closed** | **1**(Gap #5 文字漏标修复)|
| **Still Open** | **4**(Gap #1 / #2 / #3 / #4)|
| **New P0** | **8** |
| **New P1** | **6** |
| **New P2** | **5** |
| **Issue 合计** | **19** |
| **Root Cause** | **8** |
| **Fix Action** | **19** |

**未合并声明**:8 项 P0 涉及 4 个互不相同的缺陷域(DTO 安全隔离 / ID 类型 / Transaction 参与对象 / Service 纪律与证据污染),**未因数量压力合并**。P0-05 内的"Appointment 弱化"与"Visit 遗漏"作为同一 Issue 的两个独立缺陷分别记录(共 2 个 Fix Action 维度:FA-06 覆盖动作修正,FA-07 覆盖冲突登记)。Root Cause 仅在**根因机制相同**时合并(如 P0-02/P0-03 同属 RC-C"引用与内容未校验",但因涉及不同 ID 域仍各计 1 个 Issue + 独立 Fix Action)。

---

## §11 G2 READY / G3 ENTRY 状态裁决

### 11.1 S1-170E §13.4 Hard Blocker 逐项

| 硬阻塞 | G2-04 自评 | **本审计裁决** | 依据 |
|---|:-:|:-:|---|
| 2a. Object → Entity 字段级映射 | ✅ | ✅ 沿用 | 本轮未改动 |
| **2b. API Controller/DTO/VO 字段级映射** | ⚠️ 部分 | ❌ **BLOCK** | 25/40 API 零字段;16 API 合并占位;完整率 5.0% |
| **2c. Service 层关键方法签名** | ⚠️ 部分 | ❌ **BLOCK** | Service 冻结数实际 = 0;7 个"冻结"为 Repository 复用;20 分母含占位/已删除 |
| 2d. IGNORE_TABLES Phase 1 范围 | ✅ | ✅ 沿用 | 本轮未改动 |
| **Transaction boundary 精确划分** | ⚠️ 部分 | ❌ **BLOCK 且倒退** | API-016 漏 2 项;API-021 漏 1 项 + 弱化 1 项;4/4 分类仍【待确认】 |

### 11.2 S1-170E §12.2 判定逻辑

```
if #1 (G1)     == READY                    ✅
   AND #2 (G2) == READY                   ❌ BLOCK(2b / 2c / Transaction 未关闭)
   AND #3 (E7.1) == FROZEN                ✅
   AND #4 (Phase 1) == READY              ✅
   AND #5 (Dev Env) == Available          ⚠️ 【待确认】(本轮无实际验证,且不属本轮修复对象)
   AND #6 (Git) == Available              ✅(modified 0 / staged 0 / no commit)
   → ALLOW Backend Implementation Entry
```

**裁决**:`#2` 条件不成立 → **不得进入 Backend Implementation**。

### 11.3 Gate 状态(维持)

| Gate | 状态 |
|---|---|
| `G2-Contract-Audit-03` | PASS(仅证明历史 Contract 冲突已修复;**其 P1-A1 / P1-A2 已被 G2-04 重开**)|
| **`G2-Contract-Audit-04`** | **BLOCK** |
| `G2-READY-Gate-Result` | **INVALID**(维持 `G2-READY-Gate-Audit-01` 裁决)|
| **G2 READY** | **BLOCK** |
| **G3 ENTRY** | **不允许进入** |
| **Backend 创建** | **不允许** |

---

## §12 本审计的独立性与局限声明

### 12.1 独立性声明

1. 本审计**未采信** G2-Contract-04 的任何自述结论作为证据,包括"40/40 已建立" / "6/6 Service 已建立" / "4/4 Transaction 已建立" / "New P0 = 0" / "New P1 = 0" / "Keyword scan = PASS" / "Regression PASS"。
2. 本审计的所有裁决均可回溯到 §2.1 所列一手基线的**具体行号**。
3. 本审计**未修改** G2-Contract-04 或任何历史文件的任何字节。
4. 本审计的关键词检索为**独立执行并附行号输出**(§3.1),不引用 G2-04 §18.2 的结论。

### 12.2 局限性(诚实标注)

| # | 局限 | 影响 |
|:-:|---|---|
| 1 | §4~§18 采用"完整沿用 G2-Contract-03"的章节(API 总表 / Repository / Tenant / Security / Exception / DEFAULT / IGNORE_TABLES)**未逐条独立复核** | 这些章节可能存在本轮未发现的问题。本审计的 BLOCK 结论**不依赖**这些章节 |
| 2 | ~~236A 未逐行通读~~ **已闭合** | 第二轮已完整调阅 236A:line 53-54(6 BIGINT + 6 CHAR(36))、line 79-80(主键类型规则)、line 129/146/168/190/212/229(6 张复用表 PK)、line 246-256(`appointment_schedule` DDL)、line 271-288(`appointment_slot` DDL)、line 297-312(`appointment` DDL)。**P0-02 / P0-03 结论不变且证据更强** |
| 3 | ~~234A 未逐行通读~~ **已闭合** | 第二轮已完整调阅 234A(483 行)§4.1/§4.2/§7.1/§9 的专项纠错裁决,并补阅 234B(后端文件 = 0 的 Schema 取证报告,确认 `Long` 为 E 级推断而非 A 级事实)。**P0-02 结论不变且新增"证据等级误标"维度** |
| 4 | Dev Environment 实际可用性(Java 17 / Maven / Spring Boot / H2)**本轮未做任何验证** | 按本轮指令,该项不属 Contract 文本修复对象;但 **G3 ENTRY 前必须提供实际证据** |
| 5 | 本审计未评估 40×6 Permission Matrix 的实质正确性(仍【待确认】)| 维持开放 |
| 6 | `234A` / `234B` 共同确认:**原系统后端 Java POJO 与数据库 Schema 从未被直接观察**(234B §1.2 `后端文件 = 0 个`)。因此"6 复用 ID = `Long`"的证据等级是 **【OptFlow设计】** 而非【原系统事实】 | 该性质不削弱 P0-02 裁决(G2-04 的 `String(uuid)` 在**任何**等级下都是错的);但意味着 **FA-03 执行时须保留该证据等级标注**,不得标为原系统事实 |

### 12.3 下一轮前置建议(仅记录,本审计不执行)

1. **不得创建 G2-Contract-05**,等待明确指令。
2. 若进入修复轮,建议按 §9 的 P0 优先级顺序执行(FA-01 ~ FA-13 为 P0)。
3. **建议先建立 FA-12 的可复现自检清单**,再执行任何修复 —— 否则同名问题会在下一轮重复出现(P0-07 已是第 2 轮复发:P1-A2 → `...Json`)。
4. ~~建议补做 234A / 236A 的完整裁决记录~~ **已完成(第二轮)**:234A / 234B / 236A 已全部调阅并写入 §2.1 / §4.2 / §4.3,§12.2 局限 #2 / #3 已闭合。

---

## §13 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-04_Production-Implementation-Contract独立盲审.md` |
| 性质 | 独立盲审报告(**本轮唯一新增文件**)|
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 0 号闸门 | SHA256 **4 / 4 PASS** |
| 审计对象 | `G2-Contract-04_OptFlow-PMS_Production-Implementation-Contract.md`(848 行)|
| 修改的历史文件 | **0** |
| Git | modified = 0 / staged = 0 / no commit / no push |
| 代码 / DDL / DB / Test | **未触碰** |
| **最终判定** | **`G2-Contract-Audit-04 = BLOCK`** |
| 后续动作 | **暂停,等待指令。不进入 G2-Contract-05,不进入 G3。** |

---

**End of G2-Contract-Audit-04**
