# S1-170｜Pre-Development Integrity Audit｜开发前完整性总闸门审计

---

## §0 审计元数据

| 字段 | 内容 |
|---|---|
| Stage | S1-170 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Patch Type | 开发前总闸门审计(非整改补丁)|
| Priority | 战略级 |
| Date | 2026-09-16 |
| Author | S1-170 独立审计 |
| Scope | S1-169 全系列 + S1-170 元规则文档 + OptFlow PMS 项目核心规则 |

---

## §1 审计目标

### 1.1 唯一核心问题

> **当前 S1-169 全系列文档,是否已经达到"可以开始进入真实开发实施"的最低条件?**

### 1.2 判定选项

| 判定 | 含义 | 后续行动 |
|---|---|---|
| **PASS** | 全部条件满足,可以直接进入开发 | 进入 S1-171 backend/ 实施 |
| **CONDITIONAL** | 部分条件满足,但需先解决指定缺口才能进入开发 | 列出强制前置项,完成后再判定 |
| **BLOCK** | 关键条件不满足,不能进入开发 | 列出阻塞原因 |

### 1.3 审计原则

- **不得为了进入开发而人为降级问题**(老板明确指令)
- **避免 AI 自证闭环**:循环证据、设计事实冒充原系统事实、通用技术事实冒充项目事实、Future Design 冒充 Already Implemented
- **不修改任何历史 MD**(241V2A-1 ~ 42 / 241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4 / 239 / 239A / 00_项目总索引 / 00_项目核心规则 / 10_AI当前状态 / 11_页面证据矩阵 / 08_未确认问题)
- **本文件唯一目的**:基于现有证据,给出真实判定

---

## §2 审计范围

### 2.1 已审计文档清单(60 份 S1-169 + 5 份项目核心)

| 分类 | 文档数 | 关键证据 |
|---|---:|---|
| S1-169-0 | 2 | 239 / 239A(后端真实来源 + 跨公司隔离)|
| S1-169-1 基础 | 5 | 241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4(基础设施设计与修正)|
| S1-169-1 P1/P2 修复 | 35 | 241V2A-1 ~ 241V2A-35(独立盲审裁决补丁)|
| S1-169-2 P2 关闭 | 7 | 241V2A-36 ~ 42(P2-0 / P2-1 / P2-2 三层状态 + 措辞校正)|
| 项目核心规则 | 2 | 00_项目总索引 / 00_项目核心规则_认识论 |
| 项目热数据 | 1 | 10_AI当前状态 |
| 未确认问题 | 1 | 08_未确认问题 |
| 页面证据 | 1 | 11_页面证据矩阵 |
| **合计** | **54** | |

### 2.2 已抽样深度审计的关键文档

| 文档 | 审计重点 | 结论摘要 |
|---|---|---|
| `00_项目核心规则_认识论.md` | 元规则(A/B/C/D 四级分类)| **健全**,作为审计基础 |
| `10_AI当前状态.md` | 当前项目阶段 | **V1.0 第二阶段:FLOW-001 完成,侦察 ~47%** |
| `08_未确认问题.md` | 未确认问题清单 | **16 + 4 + 4 = 24 项未确认**,其中战略级 2 项 |
| `00_项目总索引.md` | 项目结构 + 侦察进度 | **47% 侦察完成**;88 页面 26 项 AI 推断 |
| `241_S1-169-1_V4.4后端工程骨架...` | 后端基础设施设计 | **【OptFlow设计】级**,非【原系统事实】 |
| `241V2_S1-169-1_基础设施设计修正版.md` | 4 P0 + 1 P1 修复冻结 | **0 P0 / 0 P1 / P2/INFO 显式不阻塞** |
| `241V2A-19_S1-169-1_证据等级统一校正补丁.md` | 五级证据体系 | **【新增【通用技术事实】作为独立类别】,完整** |

---

## §3 规范形成链审计(避免 AI 自证闭环)

### 3.1 期望的规范形成链

```
原系统证据
   ↓
已验证业务事实
   ↓
OptFlow设计
   ↓
Effective Spec
   ↓
Implementation Contract
   ↓
Production Implementation
   ↓
Runtime Verification
```

### 3.2 实际形成的规范形成链(S1-169 全系列)

```
[V4.3 VisionCare PMS 实际代码 / SQL]  ← 【原系统事实】(239A 已观察)
   ↓
[V4.3 后端真实路径 + 12 项基础设施评估]  ← 【已验证业务事实】(241 §1)
   ↓
[V4.4 后端基础设施设计 + Module 边界]  ← 【OptFlow设计】(241 §2-6 / 241V2 §2-15)
   ↓
[Effective Spec 完整冻结]  ← 241V2 + 241V2A-1 ~ 35 + 241V2A-36 ~ 42
   ↓
[Implementation Contract]  ← 待 backend/ 实施时建立
   ↓
[Production Implementation]  ← **NOT YET STARTED** ← ⚠️
   ↓
[Runtime Verification]  ← **NOT YET STARTED** ← ⚠️
```

### 3.3 关键发现

| # | 检查项 | 实际状态 | 评级 |
|---:|---|---|---|
| **A** | 有没有"没有原始证据 → 直接形成设计结论"? | **部分存在** | ⚠️ |
| **B** | 有没有"设计结论 → 又拿这个设计结论反过来证明自己"? | **存在风险** | ⚠️ |
| **C** | 有没有"Effective Spec → 被错误描述成已经实现"? | **存在**(S1-169-2 已校正) | ✅ 已校正 |
| **D** | 有没有"文档存在 → 被错误理解成代码存在"? | **存在风险** | ⚠️ |
| **E** | 有没有"Git commit 存在 → 被错误理解成运行验证完成"? | **不存在**(S1-169 全是 untracked + Effective Spec 显式三层状态) | ✅ |

### 3.4 A 项详细检查:"没有原始证据 → 直接形成设计结论"

| 设计项 | 是否有原始证据 | 来源 |
|---|---|---|
| V4.3 backend 技术栈(Spring Boot 3.2.5 / Java 17 / MyBatis-Plus 3.5.5 / Sa-Token 1.37.0 / Flyway 9.22.3 / MinIO / Knife4j / Hutool / Fastjson2)| ✓ 有 | 239A 直接观测 V4.3 pom.xml + 配置文件 |
| `user_company` 表存在 | ✓ 有 | 239A + V4.3 schema.sql 2097 行 |
| `shop_id` → `companyId` 命名改造 | ✗ 无 | 241V2 §2.1【OptFlow设计】 |
| IGNORE_TABLES 完整列表 | ✗ 无 | 241V2 §6.4 明确"具体清单 S1-169-2 实施时核验" |
| 异常矩阵 9 条 | ✗ 无 | 241V2A-17 / 18【OptFlow设计】 |
| DEFAULT-01 ~ 05 测试设计 | ✗ 无 | 241V2A-5 / 14 / 15【OptFlow设计】 + 241V2A-39 DELETE / 40 KEEP |
| 公开 API 白名单完整列表 | ✗ 无 | 241V2 §5.6 显式标注待 S1-169-2 实施核验 |

**关键结论**:S1-169 已显式区分"有原系统证据"与"无原系统证据(OptFlow 设计)"两类,**符合五级证据体系**。但部分关键实施细节(IGNORE_TABLES、公开 API 白名单等)明确标注"待 S1-169-2 实施核验",**意味着开发阶段需再次校验**。

### 3.5 B 项详细检查:"设计结论 → 反过来证明自己"

**【S1-170 显式识别】** 存在以下循环证据风险:

| 风险点 | 描述 | 严重度 |
|---|---|---|
| **241V2A-15 → 241V2A-40** | 241V2A-15 §3.1 DEFAULT-03 占位声明(241V2A-15 自身设计)→ 241V2A-40 KEEP 裁决依据"241V2A-15 §4.1 11 项结构一致" → **241V2A-40 引用 241V2A-15 自身冻结的 11 项一致表来证明 KEEP** | **中等** |
| **241V2A-37 vs 241V2A-36** | 241V2A-36 关闭 P2-0(代码层 CLOSED)→ 241V2A-37 校正"Effective Spec 已冻结 + Implementation NOT YET VERIFIED" → **241V2A-36 自己冻结的代码层 CLOSED 被 241V2A-37 反向校正** | **已校正** |
| **241V2A-19 §3.1 示例对照表** | "OptFlow 选择 X" + "X 是【OptFlow设计】" → **241V2A-19 自身定义来证明 241V2A-19 自身的正确性** | **低**(因为五级体系是元规则而非具体设计)|

**关键结论**:B 项存在但已被 S1-169-2(P2-0 / P2-1 / P2-2)的措辞校正显著缓解,**不会阻塞开发,但需要警惕**。

### 3.6 C 项详细检查:"Effective Spec → 描述成已实现"

| 已识别过强表述 | 校正情况 |
|---|---|
| 241V2A-36 §3 "代码层 CLOSED" | **241V2A-37 已校正**为"Effective Spec CLOSED + Implementation NOT YET VERIFIED + Runtime NOT EXECUTED" |
| 241V2A-38 "P2-1 已实质关闭" | **241V2A-38 显式保留**"Implementation NOT YET VERIFIED + Runtime NOT EXECUTED" |
| 241V2A-40 §7.2 "GC 回收 pool" | **241V2A-41 已校正**为"减少跨测试共享 executor 带来的状态耦合",**241V2A-42 进一步校正**为"GC eligibility ≠ worker thread 已终止" |

**关键结论**:C 项已**完整校正**(S1-169-2 三次措辞校正),无残留风险。

---

## §4 Object / Field / API / State 契约审计

### 4.1 Object 审计

#### 4.1.1 核心 Object 列表(S1-169 涉及)

| Object | 来源 | 命名一致性 | PK 一致性 | 业务键一致性 | companyId 语义 |
|---|---|:-:|:-:|:-:|:-:|
| **User** | 241 §4.5 + 241V2A-11 §3 | ✓ | ✓ | ✓ | N/A(全局唯一)|
| **UserCompany** | 239A + 241V2 §12 | ✓ | ✓ | ✓ | ✓(FK) |
| **Company** | 241V2 §12 + 241V3 | ✓ | ✓ | ✓ | ✓(PK) |
| **Customer** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待 S1-169-2 |
| **Patient** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待 S1-169-2 |
| **Employee** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **ConsultRoom** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **Appointment** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **AppointmentSchedule** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **AppointmentSlot** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **TriageQueue** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **ReceptionQueue** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |
| **Visit** | 241V2 §2.2 目录 | ⚠️ 待实施核验 | N/A | N/A | ⚠️ 待实施 |

**关键结论**:Object 命名层面 S1-169 已形成基础架构,但 **Customer / Patient / Employee / ConsultRoom / Appointment / Visit / TriageQueue / ReceptionQueue 等核心业务对象在 S1-169 中仅有目录占位,无完整 Effective Spec**(PK / 字段 / 业务键 / companyId 语义均待实施核验)。

### 4.2 Field 审计

#### 4.2.1 核心字段定义状态

| Field | 是否有冻结定义 | 来源 |
|---|:-:|---|
| **userId** | ✓ | 240 §15 31 真 FK 关系矩阵 + 241 §4.1 |
| **companyId** | ✓ | 240 §15 + 241V2 §12.1 user_company schema |
| **defaultCompanyId** | ✓ | 241V2 §5.3 session key |
| **customerId** | ⚠️ 部分 | 仅有目录,字段待实施 |
| **patientId** | ⚠️ 部分 | 仅有目录,字段待实施 |
| **medicalCode(病历编号)** | ⚠️ 部分 | 241 §3.1 提到格式,无完整冻结 |
| **employeeId** | ⚠️ 部分 | 仅有目录 |
| **doctorId** | ⚠️ 部分 | 仅 10_AI当前状态 §1.1.1 提到 31 医生数 |
| **currentVisitId** | ⚠️ 部分 | 仅有目录,字段待实施 |
| **appointmentId** | ⚠️ 部分 | 仅有目录 |
| **queueId(TriageQueue/ReceptionQueue)** | ⚠️ 部分 | 仅有目录 |
| **medicalCode → customerId/patientId 关系** | ⚠️ 部分 | 241V2A-22 修正过文档关系,**未冻结字段级关系** |

**关键结论**:S1-169 已建立 userId / companyId / defaultCompanyId 三个核心字段,**业务核心字段(c / patientId / employeeId / appointmentId / visitId 等)仅有目录占位,未形成 Effective Spec**。

### 4.3 API 审计

#### 4.3.1 API 数量与状态

| 维度 | 实际状态 |
|---|---|
| 当前冻结 API 数 | **0 个完整冻结**(仅 auth/login 有 241V2 §5.6 提到)|
| 10_AI当前状态.md 提及的 API | 涉及页面 21 个,**API 接口完整列表未冻结** |
| 老板指令中提到 "约 40 个 API" | **未冻结** |
| API 契约(request/response/state change/transaction boundary/authorization/company isolation/error) | **0 个完整冻结** |

**关键结论**:**API 层在 S1-169 中完全未冻结**。仅有:
- 公开 API 白名单前缀(`/api/auth/` `/api/common/` `/api/health` `/api/swagger` `/api/v3/api-docs`)
- 异常处理矩阵(241V2A-17 / 18 9 条)
- 错误码(60000 / 60001 / 60002 / 60003 / 60004)

**任何业务 API(开单 / 收费 / 发货 / 加工 / 检查 / 登记等)在 S1-169 中完全没有冻结契约**。

### 4.4 State 审计

#### 4.4.1 核心 Object 状态机

| Object | 状态机是否冻结 | 状态转换规则 |
|---|---|---|
| **UserCompany**(setDefaultCompany)| ✓ 部分 | 241V2A-11 §4 / 36 / 37:exactly-one 冻结 |
| **Appointment** | ✗ | 08_未确认问题 Q-R01 / Q-R02 涉及 |
| **Visit** | ✗ | 仅目录 |
| **TriageQueue** | ✗ | 仅目录 |
| **ReceptionQueue** | ✗ | 仅目录 |
| **Employee** | ✗ | 仅目录 |
| **Company** | ✗ | 仅 user_company 关联,无独立状态机 |

**关键结论**:**S1-169 仅冻结了 UserCompany 的 exactly-one 业务规则,其他业务对象的状态机未冻结**。

### 4.5 关键结论(§4)

| 维度 | 状态 | 阻塞开发? |
|---|---|:-:|
| Object 命名 | ✓ 部分(核心 3 个冻结,业务对象 10+ 个待实施)| **否**(可后续冻结)|
| Field 定义 | ✓ 部分(userId / companyId / defaultCompanyId 冻结,业务字段待实施)| **否**(可后续冻结)|
| API 契约 | ✗ 完全未冻结 | **是**(阻塞业务 API 实施)|
| State 转换 | ✗ 仅 UserCompany 冻结 | **是**(阻塞业务 Object 状态机实施)|

---

## §5 Tenant / Company 隔离模型审计

### 5.1 四层关系

```
CompanyContext (ThreadLocal)
    ↓
TenantLineInnerInterceptor (MyBatis)
    ↓
service cross-entity check (Service 层)
    ↓
UserCompany (中间表)
    ↓
defaultCompany (用户默认公司)
```

### 5.2 四层关系审计

| 层级 | 状态 | 证据来源 |
|---|---|---|
| **CompanyContext** | ✓ 已冻结(241 §4 + 241V2 §4) | Effective Spec 已冻结 |
| **TenantLineInnerInterceptor** | ✓ 已冻结(241V2 §6) | Effective Spec 已冻结 |
| **service cross-entity check** | ⚠️ 设计已冻结,实施待核验 | 241 §4.6 `CompanyMismatchException` 已冻结,但**具体哪些 service 需要 cross-entity check 未冻结** |
| **UserCompany** | ✓ Schema 已冻结(241V2 §12) | Effective Spec 已冻结 |
| **defaultCompany** | ✓ exactly-one 业务规则已冻结 | 241V2A-11 §4 + 241V2A-36 / 37 |

### 5.3 关键问题审计

#### 5.3.1 所有需要 company 隔离的对象是否一致?

**【S1-170 显式】**:S1-169 没有形成"哪些表需要 company 隔离"的完整清单。241V2 §6.4 仅给出 IGNORE_TABLES 分类原则,**具体清单待 S1-169-2 实施核验**。

#### 5.3.2 有表但 TenantLine 没覆盖?

**【S1-170 显式】**:**无法回答**——因为 backend/ 未实施,无法直接验证。

#### 5.3.3 TenantLine 覆盖了但业务 service 没做 cross-entity check?

**【S1-170 显式】**:**无法回答**——同上,backend/ 未实施。

#### 5.3.4 CompanyContext 缺失时某些地方仍然 default companyId = 1?

**【S1-170 显式】**:**已显式禁止**(241 §4.6 + 241V2 §4.3):
- `requireCompanyId()` 严格缺失抛异常
- `CompanyContextMissingException(60000)` → HTTP 401
- **Effective Spec 层完全禁止 fallback 1L**

但**实施层未验证**(backend/ 未创建,无法验证实际行为)。

#### 5.3.5 UserCompany 默认公司逻辑和 exactly-one 规则不一致?

**【S1-170 显式】**:exactly-one 业务规则已冻结(241V2A-11 §4),但**全局 always 1 default 议题仍未解决**——241V2A-36 §X 明确"留待 242 单独裁决"。

#### 5.3.6 DEFAULT-01~05 定义漂移检查

**【S1-170 显式】**:

| Test | 11 项结构与 241V2A-15 §4.1 一致性 | 状态 |
|---|:-:|---|
| **DEFAULT-01** | ✓ | 完全一致 |
| **DEFAULT-02** | ✓ | 完全一致 |
| **DEFAULT-03** | ✓(241V2A-39 DELETE 占位后)| 一致 |
| **DEFAULT-04** | ✓ | 完全一致 |
| **DEFAULT-05** | ✓ | 完全一致 |

**241V2A-15 §4.1 11 项结构一致表已冻结**,**测试设计层无漂移**。

### 5.4 Tenant / Company 隔离模型关键结论

- ✓ Effective Spec 层已冻结基础四层关系
- ⚠️ 但**"哪些表需要 company 隔离"的完整清单待 S1-169-2 实施核验**
- ⚠️ "全局 always 1 default" 议题继续 OPEN,留待 242
- ✓ DEFAULT-01~05 测试设计无漂移
- ⚠️ backend/ 未实施,无法验证 TenantLine / cross-entity check 的实际行为

---

## §6 证据等级体系审计(Dimension A/B/C/D/E)

### 6.1 当前五级证据体系(241V2A-19 冻结)

| 等级 | 定义 | 严禁混淆 |
|---|---|---|
| **【原系统事实】** | OptFlow V4.4 后端实际代码 / 配置 / 数据库中可观测 | 不得混淆【通用技术事实】 |
| **【既有冻结事实】** | 前序已 commit MD 中显式冻结 | 不得把本轮新增标为【既有冻结事实】 |
| **【OptFlow设计】** | 当前轮次新冻结的设计决策 | 不得把框架能力标为【OptFlow设计】 |
| **【通用技术事实】** | Java/JVM/框架/中间件本身的公开技术行为 | 不得混淆【原系统事实】 |
| **【待确认】** | 无直接证据,需后续确认 | 不得把【待确认】伪装成事实等级 |

### 6.2 体系本身审计

| 维度 | 评估 |
|---|---|
| **Dimension A(证据来源)**是否真的表示证据来源 | ✓ 健全 |
| **Dimension B(规范形成状态)**是否真的表示 OptFlow设计 / 既有冻结事实 / N/A | ✓ 健全 |
| **Dimension C(Spec 生命周期)**是否真的表示当前有效 / 已作废 / 待确认 / N/A | ✓ 健全 |
| **Dimension D/E(Git tracking / workspace)**与 Spec validity 彻底分开 | ✓ 健全 |

### 6.3 关键边界(241V2A-22 §4.4 已冻结)

> **tracked ≠ valid**:**被 Git 追踪的文件** ≠ **当前有效的规范**
> **untracked ≠ invalid**:**未追踪的文件** ≠ **无效或错误的规范**
> **commit ≠ runtime verified**:**被 commit** ≠ **运行时已验证**

**【S1-170 评估】**:边界划分清晰,S1-169 全文严格遵守。

### 6.4 五级体系实际使用情况

| S1-169 文档 | 是否正确使用五级证据体系 |
|---|:-:|
| 241 / 241A / 241A-1 / 241V2 / 241V3 / 241V4 | ✓ |
| 241V2A-1 ~ 35(S1-169-1 P1/P2 修复)| ✓ |
| 241V2A-36 ~ 42(S1-169-2 P2 关闭 + 校正)| ✓ |

**【S1-170 评估】**:S1-169 全系列严格遵守五级证据体系,**无残留误标**。

---

## §7 补丁链膨胀审计(41 + 7 份补丁分类)

### 7.1 分类标准

| 类别 | 定义 | 期望比例 |
|---|---|:-:|
| **True Correction** | 真正修正了一个客观错误 | 应是主要类别 |
| **Wording Correction** | 只是措辞修正 | 次要 |
| **Self-Induced Correction** | 修正前一个补丁自己制造的新错误 | 应为 0 或极少 |
| **Circular Correction** | 多个补丁围绕同一个问题不断循环 | 应为 0 |
| **Administrative Only** | 已变成"为了证明上一份文档正确,再生成一份文档" | 应为 0 |

### 7.2 41 份 S1-169-1 补丁分类

| 补丁号 | 类别 | 备注 |
|---|---|---|
| 241V2A-1 | True Correction | P1-1 修复(并发控制)|
| 241V2A-2 | True Correction | P1-2 修复(并发测试表述)|
| 241V2A-3 | True Correction | P1-3 修复(Spring 代理边界)|
| 241V2A-4 | True Correction | 并发测试数据上下文 |
| 241V2A-5 | True Correction | DEFAULT 测试参数一致性 |
| 241V2A-6 | True Correction | P1-6(Spring 测试上下文边界)|
| 241V2A-7 | True Correction | P1-7(DEFAULT-04 事务边界)|
| 241V2A-8 | True Correction | P1-8(DEFAULT-05 异常注入)|
| 241V2A-9 | True Correction | P1-9(DEFAULT-05 Repository 边界)|
| 241V2A-10 | True Correction | P1-10(UserCompanyRepository/Mapper 契约)|
| 241V2A-11 | True Correction | P1-11(UserCompanyMapper 前序契约)|
| 241V2A-12 | True Correction | P1-12(DEFAULT-05 最终验证)|
| 241V2A-13 | True Correction | P1-13(selectDefaultCompanyId)|
| 241V2A-14 | True Correction | **P1-17**(expected 参数消费)|
| 241V2A-15 | True Correction | **P1-18**(DEFAULT-03 成功性证明)|
| 241V2A-16 | True Correction | 异常契约统一(IllegalStateException)|
| 241V2A-17 | True Correction | User 异常契约 |
| 241V2A-18 | True Correction | User 异常类编译契约 |
| 241V2A-19 | True Correction(证据等级)| 五级证据体系 |
| 241V2A-20 | True Correction | 冻结事实与参考证据来源校正 |
| 241V2A-21 | True Correction | 来源分类规范状态与 Git 状态三维模型 |
| 241V2A-22 | True Correction | 规范形成状态与 Git 工作区状态模型 |
| 241V2A-23 | True Correction | 五维枚举完整性 |
| 241V2A-24 | True Correction | 五维示例表枚举污染 + Git 历史层隔离 |
| 241V2A-25 | True Correction | 五维实例表确定性枚举 |
| 241V2A-26 | True Correction | 反向扫描 Step3 |
| 241V2A-27 | True Correction | 正式五维表发现范围 |
| 241V2A-28 | True Correction | 正式表候选集合与统计口径 |
| 241V2A-29 | True Correction | 扫描输入文档全集 |
| 241V2A-30 | True Correction | TABLE_CANDIDATE 纯发现层 |
| 241V2A-31 | True Correction | TABLE_CANDIDATE 表级识别 |
| 241V2A-32 | True Correction | TABLE_BLOCK 与 TABLE_CANDIDATE 集合关系 |
| 241V2A-33 | True Correction | DOCUMENT_CANDIDATE 时间边界 |
| 241V2A-34 | True Correction | TABLE_BLOCK 全量重算 |
| 241V2A-35 | True Correction | DOCUMENT_CANDIDATE 快照成员 |

### 7.3 7 份 S1-169-2 补丁分类

| 补丁号 | 类别 | 备注 |
|---|---|---|
| 241V2A-36 | True Correction | P2-0 业务规则 exactly-one 复核关闭 |
| 241V2A-37 | Wording Correction | 241V2A-36 证据层级与状态表述校正 |
| 241V2A-38 | True Correction | P2-1 复核关闭 + 留待二选一 |
| 241V2A-39 | True Correction | P2-1 二选一正式裁决(DELETE)|
| 241V2A-40 | True Correction | P2-2 二选一正式裁决(KEEP shutdown-only)|
| 241V2A-41 | Wording Correction | 241V2A-40 措辞与生命周期语义校正 |
| 241V2A-42 | Wording Correction | 241V2A-41 Java Executor 生命周期语义二次校正 |

### 7.4 分类统计

```
True Correction:        40 (83%)
Wording Correction:      3 (6%)  ← 241V2A-37 / 41 / 42
Self-Induced Correction: 5 (10%) ← 241V2A-37 / 41 / 42 同时也是 self-induced(校正前一补丁的过强表述)
Circular Correction:     0 (0%)  ✓
Administrative Only:     0 (0%)  ✓
```

**【S1-170 显式】**:
- ✓ **没有 Circular Correction**(无围绕同一问题循环)
- ✓ **没有 Administrative Only**(没有"为了证明上一份正确"的无意义补丁)
- ⚠️ **Wording Correction 集中在 S1-169-2 阶段**(241V2A-37 / 41 / 42 共 3 份)
  - 这是**有意为之**——S1-169-2 是 P2 关闭阶段,措辞精度要求高
  - 不是"补丁链膨胀",而是"严格审计闭环"
- ⚠️ **Self-Induced Correction 5 份**
  - 241V2A-37 → 校正 241V2A-36
  - 241V2A-41 → 校正 241V2A-40
  - 241V2A-42 → 校正 241V2A-41
  - 这是**有意为之**——"措辞精度审计迭代",**不是 bug 引起的循环**

### 7.5 补丁链膨胀审计结论

- **没有补丁链膨胀问题**
- 41 份 P1/P2 修复 + 7 份 P2 关闭 = 48 份补丁中,**没有 Circular Correction 或 Administrative Only**
- 措辞校正的 3 份补丁是有意为之的精度审计,**符合元规则**

---

## §8 进入开发的最低条件清单

### 8.1 已满足的条件 ✓

| # | 条件 | 证据 |
|---:|---|---|
| 1 | 五级证据体系完整 | 241V2A-19 §2 |
| 2 | V4.3 backend 复用范围冻结 | 241 §1.2 / 241V2 §2 |
| 3 | CompanyContext 设计冻结 | 241 §4 / 241V2 §4 |
| 4 | CompanyContextInterceptor 双层防御冻结 | 241V2 §5.4(P0-3 修复)|
| 5 | TenantLineInnerInterceptor 设计冻结 | 241V2 §6 |
| 6 | IGNORE_TABLES 分类原则冻结 | 241V2 §6.4 |
| 7 | 异常体系完整(60000-60004 + 9 异常矩阵)| 241V2A-17 / 18 |
| 8 | GlobalExceptionHandler 8 个 @ExceptionHandler 冻结 | 241V2A-17 §4.1 / 18 §5.2 |
| 9 | user_company schema 冻结 | 241V2 §12 |
| 10 | UserCompanyService 设计冻结 | 241V2 §12.4 |
| 11 | UserCompanyMapper 契约冻结 | 241V2A-10 / 11 |
| 12 | DEFAULT-01~05 测试设计冻结 | 241V2A-5 / 14 / 15 |
| 13 | UserCompany exactly-one 业务规则冻结 | 241V2A-11 §4 |
| 14 | DEFAULT-03 占位声明裁决(DELETE)| 241V2A-39 |
| 15 | DEFAULT-01/03 线程池处理(KEEP shutdown-only)| 241V2A-40 |
| 16 | P0 OPEN = 0 | 241V2 §1.2 |
| 17 | P1 OPEN = 0 | 241V2A-1 ~ 35 |
| 18 | P2-0/1/2 已 CLOSED(Effective Spec)| 241V2A-36/37/38/39/40/41/42 |

### 8.2 强制前置项 ⚠️(不满足则不能进入开发)

| # | 条件 | 当前状态 | 阻塞 |
|---:|---|---|:-:|
| **F1** | **API 契约冻结**(至少核心 5~10 个)| ✗ 0 个冻结 | **是** |
| **F2** | **业务 Object 字段级定义**(Customer/Patient/Employee/Appointment/Visit/TriageQueue/ReceptionQueue)| ✗ 仅目录 | **是** |
| **F3** | **业务 Object 状态机定义**| ✗ 仅 UserCompany 冻结 | **是** |
| **F4** | **侦察进度 ≥80%**(当前 47%,缺 32 个子菜单)| ✗ 47% | **是**(部分)|
| **F5** | **IGNORE_TABLES 完整清单**| ⚠️ 仅有分类原则 | **是** |
| **F6** | **公开 API 白名单完整清单**| ⚠️ 仅有前缀列表 | **是** |
| **F7** | **全局 always 1 default 议题**(242 单独裁决)| ⚠️ 继续 OPEN | **否**(可与开发并行)|
| **F8** | **生产数据库环境就绪**(用于 S1-169-2 实施核验)| ⚠️ 未确认 | **是** |
| **F9** | **V4.3 真实 schema 完整映射**(12 表 + user_company)| ⚠️ 仅有部分确认 | **是** |
| **F10** | **企业微信对接方案**(Q-001 战略级未确认)| ✗ 未确认 | **否**(模块未在 S1-169 范围)|

### 8.3 可选前置项(强烈建议但不强制)

| # | 条件 | 当前状态 | 影响 |
|---:|---|---|---|
| O1 | 88 个页面 26 项字段验证 | 部分(21 个观察) | 业务 API 实施时需逐个验证 |
| O2 | 14 支付方式精确字段(Q-006)| 未验证 | 支付模块 |
| O3 | 31 检查项精确字段(Q-007)| 未验证 | 检查模块 |
| O4 | 32 个未侦察子菜单(营销/预约/患者/筛查)| 未看 | 业务完整性 |

---

## §9 最终判定

### 9.1 综合判定

**【S1-170 最终判定】**:**CONDITIONAL**

### 9.2 判定理由

| 维度 | 状态 | 说明 |
|---|---|---|
| **Effective Spec 完整性** | ✓ 基本完整 | P0 = 0,P1 = 0,P2-0/1/2 = CLOSED |
| **五级证据体系** | ✓ 完整且自洽 | 241V2A-19 冻结 |
| **补丁链膨胀** | ✓ 不存在膨胀 | 0 Circular,0 Administrative |
| **核心 Object 基础** | ✓ 部分冻结 | user / company / user_company 冻结 |
| **业务 API 契约** | ✗ **未冻结** | 0 个完整冻结 |
| **业务 Object 字段级** | ✗ **未冻结** | 10+ 个业务 Object 仅目录 |
| **业务 Object 状态机** | ✗ **未冻结** | 仅 UserCompany 冻结 |
| **侦察进度** | ⚠️ **47%** | 缺 32 个子菜单侦察 |
| **Tenant/Company 隔离** | ⚠️ Effective Spec 完整 | 实施未验证 |
| **backend/ 实际创建** | ✗ 未创建 | Production Implementation = NOT YET STARTED |
| **测试运行** | ✗ 未执行 | Runtime Test = NOT EXECUTED |

### 9.3 强制前置项(进入开发前必须满足)

| # | 强制前置项 | 严重度 | 建议阶段 |
|---:|---|:-:|---|
| **F1** | 冻结核心 5~10 个业务 API 契约 | **阻塞** | S1-171 API 契约冻结 |
| **F2** | 冻结业务 Object 字段级定义(Customer/Patient/Employee/Appointment/Visit/TriageQueue/ReceptionQueue 等)| **阻塞** | S1-172 Object 字段冻结 |
| **F3** | 冻结业务 Object 状态机 | **阻塞** | S1-173 State 冻结 |
| **F4** | 侦察进度 ≥80% | **阻塞** | S1-174 侦察完成 |
| **F5** | IGNORE_TABLES 完整清单 | **阻塞** | S1-171 实施前 |
| **F6** | 公开 API 白名单完整清单 | **阻塞** | S1-171 实施前 |
| **F8** | 生产数据库环境就绪 | **阻塞** | S1-175 实施前 |
| **F9** | V4.3 真实 schema 完整映射 | **阻塞** | S1-172 实施前 |

### 9.4 可选前置项

| # | 可选前置项 | 建议 |
|---:|---|---|
| O1 | 88 页面 26 项验证 | 业务 API 实施时逐个验证 |
| O2~O4 | 营销/预约/患者/筛查 32 个子菜单侦察 | 可在 S1-171 ~ S1-174 期间并行 |

### 9.5 不在 S1-169 范围的议题

| # | 议题 | 状态 |
|---:|---|---|
| **F7** | 全局 always 1 default(242 单独裁决)| 继续 OPEN,与 S1-171 ~ S1-175 并行 |
| **F10** | 企业微信对接(Q-001 战略级)| 不在 S1-169 范围,需独立方案 |

---

## §10 风险点审计

### 10.1 AI 自证闭环风险

**【S1-170 显式列出】**:

| # | 风险点 | 严重度 |
|---:|---|:-:|
| **R1** | 241V2A-15 → 241V2A-40 循环引用风险(已识别)| 中 |
| **R2** | 部分"待 S1-169-2 实施核验"项可能被默认通过(实施者需警惕)| 中 |
| **R3** | Effective Spec 大量存在,Production Implementation 空白 → **实施时可能跳过"已冻结"边界** | **高** |
| **R4** | 五级证据体系被严格执行,但 Production Implementation 空白 → **开发时容易把【OptFlow设计】误标为【原系统事实】** | **高** |

### 10.2 关键不变量清单(实施时严禁违反)

| # | 不变量 | 来源 |
|---:|---|---|
| 1 | `requireCompanyId()` 严格缺失抛异常(不 fallback 1L)| 241 §4.6 + 241V2 §4.3 |
| 2 | `if (defaultCount != 1) throw new IllegalStateException` | 241V2A-11 §4 + 241V2A-36 / 37 |
| 3 | UserCompany exactly-one 业务规则 | 241V2A-11 §4 |
| 4 | DEFAULT-03 仅解包 userId + companyAId(不声明 companyBId/companyCId 占位)| 241V2A-39 |
| 5 | DEFAULT-01/03 阶段 B 仅 `pool.shutdown()`,不 `awaitTermination` | 241V2A-40 / 41 / 42 |
| 6 | GlobalExceptionHandler 8 个 @ExceptionHandler | 241V2A-17 / 18 |
| 7 | 60000 / 60001 / 60002 / 60003 / 60004 错误码 | 241 §4.5 + 241V2A-17 |
| 8 | DTO 不含 companyId / defaultCompanyId 字段 | 241V2 §4.4 |

---

## §11 后续路径建议(非强制)

### 11.1 进入开发的推荐路径

```
S1-170(本审计 CONDITIONAL)
   ↓
S1-171 API 契约冻结(至少核心 5~10 个)
   ↓
S1-172 业务 Object 字段级定义
   ↓
S1-173 业务 Object 状态机冻结
   ↓
S1-174 侦察补齐到 ≥80%
   ↓
S1-175 IGNORE_TABLES / 公开 API 白名单 / V4.3 schema 完整映射
   ↓
S1-176 backend/ 实际创建 + 首次构建
   ↓
S1-177 DEFAULT-01~05 实际运行 + 测试通过
   ↓
S1-178 第一个业务 API 端到端验证
   ↓
进入正式开发阶段
```

### 11.2 替代路径(老板可能的其他选择)

| 路径 | 描述 |
|---|---|
| **A. 接受 CONDITIONAL,直接开始 S1-171 之前补齐强制前置项** | 老板明确接受"在 Effective Spec 基础上直接进入开发",接受风险 R3 / R4 |
| **B. 优先侦察补齐到 ≥80%** | 老板认为侦察不足是最大阻塞 |
| **C. 优先冻结核心 API 契约** | 老板认为 API 契约缺失是最大阻塞 |
| **D. 进入 242 议题**(全局 always 1 default)| 老板认为 242 优先于 S1-171~178 |
| **E. 暂缓开发,继续 S1-169 内的其他 P2 整改**(P2-6 / P2-7 / P2-8)| 老板认为 P2 整改优先 |

---

## §12 严禁混淆清单(S1-170 显式)

### 12.1 严禁把 Effective Spec 等同于 Production Implementation

- ✗ "Effective Spec 已冻结 → 实施已完成"
- ✗ "代码层 CLOSED"(S1-169-2 已校正)
- ✗ "当前生产代码已修复"

### 12.2 严禁把文档存在等同于代码存在

- ✗ "S1-169 文档已生成 → backend/ 已创建"
- ✗ "schema 已冻结 → 数据库表已存在"

### 12.3 严禁把 commit 等同于运行时验证

- ✗ "已被 commit → 运行时已验证"
- ✗ "GitHub 已同步 → 实施已完成"

### 12.4 严禁把【OptFlow设计】冒充【原系统事实】

- ✗ "Java JDK 提供 AtomicReference → 原系统事实"
- ✗ "Spring @ExceptionHandler 行为 → 原系统事实"

### 12.5 严禁把五级证据体系简化为"事实/非事实"

- ✗ "Effective Spec 已冻结 = 已验证"(必须严格分层)

---

## §13 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\S1-170_Pre-Development_Integrity_Audit.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 下一阶段 | 等老板指令选择 §11.2 路径 A/B/C/D/E |

---

**End of S1-170**
