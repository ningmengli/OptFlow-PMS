# G2-Contract-Audit-01R｜问题去重与修复基线校准

> **本轮定位**:对 `G2-Contract-Audit-01_Production-Implementation-Contract独立盲审.md` 的**元审计(Meta-Audit)**:去重 + 修复基线校准。
> **不是**重新做一次完整盲审。
> **不是**修 G2 Contract。
> **不是**开发。
> **本轮唯一输出**:本元审计文档。
> **Git 基线**:`6c5acfb1de9342e140f8f813068c92b4fee0b263`(G2-Contract-Audit-01 已落地后 HEAD)
> **0 号闸门 SHA256 全部 PASS** ✓
> **历史 MD(190~241V2A-42 + S1-170 全系列 + G2-Contract-01 + G2-Contract-Audit-01)未修改** ✓
> **本轮不写代码 / 不 commit / 不 push** ✓

---

## §0 Metadata

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-01R_问题去重与修复基线校准.md` |
| 任务性质 | 元审计(Meta-Audit):G2-Contract-Audit-01 自身内部一致性校准 |
| 校准对象 | G2-Contract-Audit-01(本文不对其做修改)|
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| 校准口径 | 以 G2-Contract-Audit-01 自身证据 + 233 + 235B + 236B + 238 + 241V4 重新统计 |
| 严禁 | 修改 G2-Contract-01 / 修改 G2-Contract-Audit-01 / 修改任何历史 MD / 创建 backend / 写 Java 源文件 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

## §1 Objective

回答四个校准问题:

1. **API P0 数量**:G2-Contract-Audit-01 §3.4 写"15 项"且表内 "1+7+5=13",实际是多少?
2. **Gap 数量**:G2-Contract-Audit-01 §9.3 总结写"3 项真实 Gap",但 §9 表内列出 Gap-02/03/06/07(4 项),实际是多少?
3. **P0 去重**:G2-Contract-Audit-01 §3.3 / §4 / §5 / §6 / §7 / §8 中 P0-C1~C86,真正独立 Root Cause 多少?
4. **Coverage 数学**:G2-Contract-Audit-01 §11 写 "62+9+40=111 但冲突率按 40/121 计算",实际数学是什么?

---

## §2 API P0 数量重新统计

### 2.1 原始计数错误

**G2-Contract-Audit-01 §3.4 原文**:

> | 统计 | 数量 |
> | **P0 Contract Conflict** | **15 项**(API-025, 027~033, 035~040 = 1 + 7 + 5 = 13 项直接冲突 + 2 项顺延)|

**内部不一致**:
- 总数写 "15"
- 拆解写 "1+7+5=13 项直接冲突 + 2 项顺延"
- 13 + 2 = 15 ✓(加法对)
- 但 "1+7+5=13" 拆解本身有误

### 2.2 真实直接 Path 冲突数(API 编号唯一性)

按 API 编号唯一性,逐个列出直接 Path 冲突:

| 编号 | G2 写 | 233 / 232 冻结 | Root |
|---|---|---|:-:|
| **API-025** | `/api/queue/pause` | `/api/visit/create-direct` | RC-API-1 |
| **API-027** | `/api/queue/skip` | `/api/queue/call` | RC-API-2 |
| **API-028** | `/api/queue/complete` | `/api/queue/skip` | RC-API-3 |
| **API-029** | `/api/queue/list` | `/api/queue/recall` | RC-API-4 |
| **API-030** | `/api/visit/start` | `/api/queue/start-consult` | RC-API-5 |
| **API-031** | `/api/visit/complete` | `/api/queue/complete` | RC-API-6 |
| **API-032** | `/api/visit/cancel` | `/api/queue/console` | RC-API-7 |
| **API-033** | `/api/visit/detail` | `/api/queue/room` | RC-API-8 |
| **API-035** | `/api/visit/list` | `/api/visit/cancel-direct` | RC-API-9 |
| **API-036** | `/api/visit/cancel-direct` | `/api/visit/list-by-appointment` | RC-API-10 |
| **API-037** | `/api/reception/assign` | `/api/doctor/pause` | RC-API-11 |
| **API-038** | `/api/reception/start` | `/api/doctor/resume` | RC-API-12 |
| **API-039** | `/api/reception/list` | `/api/bigscreen/list` | RC-API-13 |
| **API-040** | `/api/auth/login` | `/api/bigscreen/display` | RC-API-14 |

### 2.3 数学重新核算

- **API-025**(1 项)
- **API-027~033**(7 项:027, 028, 029, 030, 031, 032, 033)
- **API-035~040**(6 项:035, 036, 037, 038, 039, 040)
- **直接 Path 冲突总数 = 1 + 7 + 6 = 14 项**

> **G2-Contract-Audit-01 §3.4 "1+7+5=13" 中 "5" 应为 "6"**(API-035~040 是 6 项,不是 5 项)

### 2.4 §3.3 次生 P0 (P0-C15~C19) 去重

§3.3 列了 5 项次生 P0,全部是 §3.2 的 14 项的直接 consequence,按"一个 API 编号只能产生一个根本路径冲突 ID"原则,这些**不能作为独立 P0**:

| 原 P0 编号 | 内容 | 实质 |
|---|---|---|
| P0-C15 | G2 缺 visit/create-direct | duplicate of RC-API-1(API-025)|
| P0-C16 | G2 缺 visit/cancel-direct | duplicate of RC-API-9(API-035)|
| P0-C17 | G2 缺 bigscreen/list 和 bigscreen/display | duplicate of RC-API-13 + RC-API-14(API-039 + API-040)|
| P0-C18 | G2 缺 doctor/pause 和 doctor/resume | duplicate of RC-API-11 + RC-API-12(API-037 + API-038)|
| P0-C19 | G2 把 API-040 当 auth/login | duplicate of RC-API-14(API-040)|

**§3.3 的 5 项次生 P0 全部是 consequence,不形成新独立 Root Cause**。

### 2.5 API P0 最终统计

| 统计维度 | 数值 | 备注 |
|---|:-:|---|
| **直接 Path 冲突**(独立 Root Cause)| **14 项** | API-025, 027~033, 035~040 |
| §3.3 次生 P0(去重后)| 0 | 全部是 consequence,不形成新 Root |
| §3.4 写的 "15 项" | **错误** | 应为 **14 项** |
| §3.4 表内 "1+7+5=13" | **错误** | "5" 应为 "6",和为 **14 项** |

> **🔴 校准结论**:G2-Contract-Audit-01 §3.4 写 "15 项 P0" 与 "1+7+5=13" 双重错误,真实直接冲突 = **14 项**。

---

## §3 Gap 数量重新核实

### 3.1 原始计数错误

**G2-Contract-Audit-01 §9 表中**列出的真实 Gap:

| Gap | G2 自报内容 | 独立判断结论 |
|---|---|---|
| Gap-01 | 12 业务 Object 字段级 Custom 方法 Contract 缺 | 🔴 不是 Gap,是 P0 Contract Conflict |
| **Gap-02** | 6 个 Service 方法 Contract 缺 | 🟡 **真实 Gap** |
| **Gap-03** | Sa-Token 注解 Contract 缺 | 🟡 **真实 Gap** |
| Gap-04 | Patient / BigScreen / AppointmentSchedule / AppointmentSlot 的 companyId 字段 | 🔴 不是 Gap,是 P0 Contract Conflict |
| Gap-05 | 若干字段(doctorId / consultRoomId / scheduleId 等)| 🔴 不是 Gap,是 P0 Contract Conflict |
| **Gap-06** | Phase 1 范围 26 项页面字段 | 🟡 **真实 Gap** |
| **Gap-07** | SystemSetting 范围 V4.4 重新冻结 | 🟡 **真实 Gap** |

**§9 表中明确列出 4 项真实 Gap**:Gap-02 / Gap-03 / Gap-06 / Gap-07

### 3.2 §9.3 总结中的错误

**G2-Contract-Audit-01 §9.3 原文**:

> **Gap 重新判断结论**:
> - **3 项真实 Gap**:Gap-02(6 Service)/ Gap-03(Sa-Token 注解)/ Gap-06(Phase 1 系统设置侦察)/ Gap-07(SystemSetting V4.4)
> - **3 项 P0 Contract Conflict(Contract 自标 Gap 但实际冲突)**:Gap-01 / Gap-04 / Gap-05

**§9.3 写"3 项真实 Gap"但实际列了 4 项**(Gap-02 + Gap-03 + Gap-06 + Gap-07)。

### 3.3 Gap 最终统计

| 维度 | 数量 | 备注 |
|---|:-:|---|
| **真实 Gap(G2 自身未冻结 + Effective Spec 未冻结)** | **4 项** | Gap-02 / Gap-03 / Gap-06 / Gap-07 |
| Contract 自标 Gap 但实为 P0 Conflict | 3 项 | Gap-01 / Gap-04 / Gap-05 |
| §9.3 写的 "3 项真实 Gap" | **错误** | 应为 **4 项真实 Gap** |

> **🔴 校准结论**:G2-Contract-Audit-01 §9.3 写"3 项真实 Gap"错误,真实 Gap = **4 项**。

---

## §4 P0 Root-Cause 去重

### 4.1 G2-Contract-Audit-01 原 P0 编号清单(P0-C1 ~ P0-C86)

| 区段 | 编号范围 | 数量 | 内容性质 |
|---|---|---:|---|
| §3.2 API Path | P0-C1 ~ C14 | 14 | API 路径冲突 |
| §3.3 API 顺延 | P0-C15 ~ C19 | 5 | 次生(都是 consequence)|
| §4.3 Transfer | P0-C20 ~ C24 | 5 | Transfer 步骤错 |
| §5.1 Object 字段 | P0-C25 ~ C36 | 12 | Object 字段缺失/错误 |
| §6.1 IGNORE_TABLES | P0-C37 ~ C38 | 2 | Tenant 列表不完整 |
| §6.3 Tenant 完整性 | P0-C39 ~ C45 | 7 | Tenant 子项 |
| §7.1 Service | P0-C46 ~ C56 | 11 | Service 路径错 + 未冻结 |
| §7.2 Transaction | P0-C57 ~ C65 | 9 | Transaction 分类 |
| §7.3 Security | P0-C66 ~ C70 | 5 | Security 子项 |
| §7.4 Exception | P0-C71 ~ C80 | 10 | 全部一致(无 P0)|
| §7.5 DEFAULT | P0-C81 ~ C85 | 5 | 全部一致(无 P0)|
| §8 E-level Inference | P0-C86.1 ~ C86.14 | 14 | 自创字段 / 重命名 |
| **合计原 P0 编号** | | **86 项** | |

### 4.2 Root Cause 去重与分类

> **去重原则**:同一根本错误在不同章节的重复表现,只形成 1 个独立 Root Cause。

#### RC-1:API 路径错位(14 项 API)

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-1**(API 路径错位 14 项)| P0-C1 / C2 / C3 / C4 / C5 / C6 / C7 / C8 / C9 / C10 / C11 / C12 / C13 / C14 | §3.2 API-025~040 表 | **必须**完整重写 G2 §7.2,以 233 / 232 为准 |
| (duplicate / consequence) | P0-C15 / C16 / C17 / C18 / C19 | §3.3 API 顺延次生 | 已并入 RC-1 |
| (duplicate) | P0-C46 / C47 / C48 / C49 | §7.1 Service 路径错 | 已并入 RC-1 |
| (duplicate) | P0-C59 / C61 | §7.2 Transaction 路径错 | 已并入 RC-1 |
| (duplicate) | P0-C70(部分) | §7.3 跨角色权限矩阵路径错 | 已并入 RC-1 |
| (duplicate) | P0-C86.4 / C86.12 | §8 自创字段路径错 | 已并入 RC-1 |

**RC-1 合计独立 P0 = 1 项**(14 个 API 路径错位,1 个根本修复动作 = 重写 G2 §7.2)

#### RC-2:API-034 Transfer 9-step 错位(单一根因)

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-2**(Transfer 9-step 错位)| P0-C20 / C21 / C22 / C23 / C24 | §4.3 Transfer 步骤 | **必须**完整重写 G2 §9.2,以 235B §4.2 / §4.3 为准 |
| (duplicate) | P0-C50 | §7.1 TransferService | 已并入 RC-2 |
| (duplicate) | P0-C60 | §7.2 Transaction 错 | 已并入 RC-2 |
| (duplicate) | P0-C86.5 / C86.10 | §8 Transfer 创建 ReceptionQueue / 顺序错 | 已并入 RC-2 |

**RC-2 合计独立 P0 = 1 项**(Transfer 9-step 完整重写)

#### RC-3:12 Object 字段级 9 项 P0(单一根因类型)

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-3a**(Patient 字段错)| P0-C27 | §5.1 Patient 行 | 重写 G2 §4.2.3 |
| **RC-3b**(Employee 字段缺)| P0-C28 | §5.1 Employee 行 | 重写 G2 §4.2.4 |
| **RC-3c**(ConsultRoom 字段错)| P0-C29 | §5.1 ConsultRoom 行 | 重写 G2 §4.2.5 |
| **RC-3d**(BigScreen 字段错)| P0-C30 | §5.1 BigScreen 行 | 重写 G2 §4.2.6 |
| **RC-3e**(AppointmentSchedule 字段错)| P0-C31 | §5.1 AppointmentSchedule 行 | 重写 G2 §4.3.1 |
| **RC-3f**(AppointmentSlot 字段错)| P0-C32 | §5.1 AppointmentSlot 行 | 重写 G2 §4.3.2 |
| **RC-3g**(Appointment 字段缺)| P0-C33 | §5.1 Appointment 行 | 重写 G2 §4.3.3 |
| **RC-3h**(Visit 字段缺)| P0-C34 | §5.1 Visit 行 | 重写 G2 §4.3.4 |
| **RC-3i**(ReceptionQueue 字段缺)| P0-C36 | §5.1 ReceptionQueue 行 | 重写 G2 §4.3.6 |
| (duplicate) | P0-C86.2 / C86.6 / C86.7 / C86.8 / C86.9 / C86.11 | §8 自创字段 | 已并入 RC-3 |

**RC-3 合计独立 P0 = 9 项**(9 个 Object 各 1 个独立修复动作 = 9 个根因,不是 1 个合并根因)

#### RC-4:IGNORE_TABLES 静态清单不完整

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-4**(IGNORE_TABLES 不完整)| P0-C37 | §6.1 IGNORE_TABLES 总配置 | **必须**重写 G2 §14.4,从 `{company, user_company}` 改为 5 个配置项 |
| (duplicate) | P0-C43 | §6.3 Tenant 完整性 | 已并入 RC-4 |
| (duplicate) | P0-C86.14 | §8 IGNORE_TABLES 静态清单 | 已并入 RC-4 |

**RC-4 合计独立 P0 = 1 项**

#### RC-5:company 业务表概念混淆

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-5**(company 业务表概念错)| P0-C38 | §6.1 / §6.2 业务表 / 系统表 | **必须**改 G2 §14.2,明确 company 是 12 业务表之一,TenantLine IGNORE |
| (duplicate) | P0-C44 | §6.3 IGNORE_TABLES 业务表归属 | 已并入 RC-5 |

**RC-5 合计独立 P0 = 1 项**

#### RC-6:公开 API 白名单缺 bigscreen/display

| Root-Cause-ID | 原 P0 编号 | 涉及章节 | 修复动作 |
|---|---|---|---|
| **RC-6**(公开 API 白名单缺)| P0-C45 | §6.3 公开 API 白名单 | **必须**改 G2 §11.2,补 `/api/bigscreen/display`(API-040)|
| (duplicate) | P0-C69 | §7.3 Security 公开 API 白名单 | 已并入 RC-6 |

**RC-6 合计独立 P0 = 1 项**

### 4.3 Root Cause 独立 P0 汇总

| Root-Cause-ID | 描述 | 独立 P0 数量 |
|---|---|:-:|
| RC-1 | API 路径错位(14 API 重写 G2 §7.2)| **1** |
| RC-2 | Transfer 9-step 错位(重写 G2 §9.2)| **1** |
| RC-3 | 12 Object 字段级 9 项错位(逐 Object 重写 G2 §4)| **9** |
| RC-4 | IGNORE_TABLES 不完整(重写 G2 §14.4)| **1** |
| RC-5 | company 业务表概念错(改 G2 §14.2)| **1** |
| RC-6 | 公开 API 白名单缺 bigscreen/display(改 G2 §11.2)| **1** |
| **独立 P0 总数** | | **14 项** |

### 4.4 与原 P0-C1~C86 对照

| 原 P0 编号 | 数量 | 去重后归属 |
|---|---:|---|
| 真正独立 Root Cause | **14 项** | RC-1 ~ RC-6 |
| §3.3 次生 P0(duplicate)| 5 | 并入 RC-1 |
| §6.3 / §7.x / §8 duplicate | 12 | 并入 RC-1/2/4/5/6 |
| §7.4 Exception / §7.5 DEFAULT 一致项(非 P0)| 15 | 不计为 P0 |
| 原始 P0 编号 C1~C86 中实际冲突 | **31 项** | 归入 RC-1~RC-6 |
| 原始 P0 编号 C1~C86 中实际冲突率 | 31/86 = 36.0% | 其余 55 项是重复/一致 |
| **🔴 G2-Contract-Audit-01 §13.1 写 "86 项 P0"** | **错误** | 应为 **14 项独立 Root Cause P0** |

> **🔴 校准结论**:G2-Contract-Audit-01 §13.1 写"86 项 P0 Contract Conflict"严重错误,真实独立 P0 = **14 项**(6 个 Root Cause Family)。

---

## §5 Coverage 重新计算(明确分母)

### 5.1 原 Coverage 错误

**G2-Contract-Audit-01 §11 原文**:

> | **总计** | **62** | **9** | **40** | 部分 | 部分 | **51.2%** |

**问题**:
- 62 + 9 + 40 = 111 ≠ §11 各 Domain 之和(116)
- §11 冲突率写"33.1%(40 / 121)",分母 121 完全无依据
- §11 "完整率 51.2%" 用 62 / 121,但 62 + 9 + 40 = 111 不等于 121

### 5.2 重新建立分母与数值

#### 各 Domain 的分母

| Domain | 分母 | 定义 |
|---|---:|---|
| Object | **12** | 12 业务 Object |
| API | **40** | 40 个 API |
| Repository | **12** | 12 业务 Object 各 1 个 Repository |
| Service | **13** | 12 业务 Service + 1 个 TransferService |
| Transaction | **11** | 关键 7 个(API-016/021/025/034/037 + DEFAULT-01/03)+ 4 个其他(DEFAULT-02/04/05 + 232 其他)|
| Tenant | **7** | CompanyContext / TenantLineInnerInterceptor / X-Company-Id / 跨公司隔离 / IGNORE_TABLES / 业务表归属 / 公开 API 白名单 |
| Security | **5** | 角色定义 / @SaCheckRole / @SaCheckPermission / 公开 API 白名单 / 权限矩阵 |
| Exception | **10** | 8 异常类 + GlobalExceptionHandler + ResultCode |
| Test(DEFAULT) | **5** | DEFAULT-01 ~ DEFAULT-05 |
| IGNORE_TABLES 静态清单 | **1** | 单独主体 |
| **总 Domain 分母** | **116** | 各 Domain 分母相加 |

#### 重新分配数字(按"覆盖 ≠ 正确覆盖"原则)

| Domain | total | correct | partial | conflict | inference | pending |
|---|---:|---:|---:|---:|---:|---:|
| Object(12)| 12 | 1 | 2 | 9 | 0 | 0 |
| API(40)| 40 | 25 | 0 | **14** | 0 | **1**(API-034 transfer steps)|
| Repository(12)| 12 | 12 | 0 | 0 | 0 | 0 |
| Service(13)| 13 | 0 | 5 | 5 | 0 | **3** |
| Transaction(11)| 11 | 4 | 0 | **5** | 0 | **2** |
| Tenant(7)| 7 | 4 | 0 | 3 | 0 | 0 |
| Security(5)| 5 | 1 | 2 | 2 | 0 | 0 |
| Exception(10)| 10 | **10** | 0 | 0 | 0 | 0 |
| Test(5)| 5 | **5** | 0 | 0 | 0 | 0 |
| IGNORE_TABLES(1)| 1 | 0 | 0 | **1** | 0 | 0 |
| **总计** | **116** | **62** | **9** | **39** | **0** | **6** |

#### 各 Domain 覆盖率与冲突率

| Domain | 完整率 | 冲突率 |
|---|---:|---:|
| Object | 1/12 = 8.3% | 9/12 = 75.0% |
| API | 25/40 = 62.5% | 14/40 = 35.0% |
| Repository | 12/12 = 100.0% | 0% |
| Service | 0/13 = 0% | 5/13 = 38.5% |
| Transaction | 4/11 = 36.4% | 5/11 = 45.5% |
| Tenant | 4/7 = 57.1% | 3/7 = 42.9% |
| Security | 1/5 = 20.0% | 2/5 = 40.0% |
| Exception | 10/10 = 100.0% | 0% |
| Test | 5/5 = 100.0% | 0% |
| IGNORE_TABLES | 0/1 = 0% | 1/1 = 100.0% |
| **总体** | **62/116 = 53.4%** | **39/116 = 33.6%** |

### 5.3 与原 §11 对照

| 维度 | §11 原文 | 校准后 | 差异 |
|---|---:|---:|---|
| 总分母 | 121(无依据)| **116** | 🔴 修正 |
| 完整且正确 | 62 | **62** | ✓ 一致 |
| 部分 | 9 | **9** | ✓ 一致 |
| 冲突 | 40 | **39** | 🔴 修正(API 实际 14 而非 15)|
| 推断 + 待确认 | 部分 | **6** | 🔴 修正 |
| 完整率 | 51.2% | **53.4%** | 🔴 修正(分母 116)|
| 冲突率 | 33.1% | **33.6%** | 🔴 修正 |

### 5.4 Coverage 判定

- 完整且正确覆盖率 = **53.4%**(62/116)
- 冲突率 = **33.6%**(39/116)
- 推断 + 待确认 = **5.2%**(6/116)

> **🔴 校准结论**:G2-Contract-Audit-01 §11 Coverage 矩阵的"完整率 51.2%"和"冲突率 33.1%"分母错误,真实数字 = **53.4% 完整率 / 33.6% 冲突率**(分母 116)。
> **Contract Coverage 判定仍 = FAIL**(完整率 < 80% 且冲突率 > 5%)

---

## §6 Service / Transaction 统计重新计算

### 6.1 API-034 必须拆分原则

**老板任务 §5**:

> 不得把同一 API 既算正确又算 P0。
> API-034 Transfer:
> "Path 正确"与"Transaction steps 错误"必须拆成:
> API identity = PASS
> Transfer implementation contract = P0

### 6.2 API-034 拆分

| 维度 | 状态 |
|---|:-:|
| API-034 Path(`/api/visit/transfer`)| ✓ **PASS**(与 233 一致)|
| API-034 Method / Controller | ✓ **PASS** |
| API-034 State Transition | ⚠️ 部分(Target Visit 状态 IN_CONSULTATION 对,但后续步骤错)|
| API-034 Transaction 分类(T2)| ✓ **PASS** |
| API-034 Transfer 9-step 实现 | ❌ **P0**(5 处错位,见 §4.3 RC-2)|

### 6.3 Service 重新统计

| Service | 状态 | 拆分归属 |
|---|---|---|
| AppointmentService | ❌ P0(Path 错位的 5 API)| RC-1 |
| VisitService | ❌ P0(Path 错位的 5 API)| RC-1 |
| TriageService | ❌ P0(Path 错位的 5 API)| RC-1 |
| QueueService / ReceptionQueueService | ❌ P0(Path 错位的 9 API)| RC-1 |
| TransferService | ❌ P0(9-step 错)| RC-2 |
| CustomerService | ⚠️ Pending(未冻结)| P1 |
| PatientService | ⚠️ Pending(未冻结)| P1 |
| EmployeeService | ⚠️ Pending(部分冻结)| P1 |
| ConsultRoomService | ⚠️ Pending(未冻结)| P1 |
| BigScreenService | ⚠️ Pending(未冻结)| P1 |
| CompanyService | ⚠️ Pending(部分冻结)| P1 |

### 6.4 Transaction 重新统计

| 项 | 状态 | 拆分归属 |
|---|---|---|
| API-016 arrival/checkin | ⚠️ Pending(233 未明确)| P1 |
| API-021 triage/assign | ⚠️ Pending(233 未明确)| P1 |
| API-025 visit/create-direct | ❌ P0(Path 错)| RC-1 |
| API-034 visit/transfer | ⚠️ 拆分(Path PASS + steps P0)| RC-2 |
| API-037 doctor/pause | ❌ P0(Path 错)| RC-1 |
| DEFAULT-01 | ✓ PASS | — |
| DEFAULT-03 | ✓ PASS | — |
| 其他 4 项(DEFAULT-02/04/05 + 232 其他)| ✓ PASS | — |

---

## §7 独立 P0 / P1 / Gap 最终统计

### 7.1 独立 P0 总数

| Root-Cause-ID | 描述 | 数量 |
|---|---|:-:|
| RC-1 | API 路径错位(14 API 重写 G2 §7.2)| 1 |
| RC-2 | Transfer 9-step 错位(重写 G2 §9.2)| 1 |
| RC-3a~i | 12 Object 字段级 9 项错位 | 9 |
| RC-4 | IGNORE_TABLES 不完整 | 1 |
| RC-5 | company 业务表概念错 | 1 |
| RC-6 | 公开 API 白名单缺 bigscreen/display | 1 |
| **独立 P0 总数** | | **14 项** |

### 7.2 独立 P1 总数

| P1-编号 | 描述 | 来源 |
|---|---|---|
| P1-1 | CustomerService / PatientService / ConsultRoomService / BigScreenService 方法 Contract 缺 | Gap-02(部分)|
| P1-2 | EmployeeService.adminId 校验逻辑部分冻结 | Gap-02(部分)|
| P1-3 | CompanyService CRUD 部分冻结 | Gap-02(部分)|
| P1-4 | API-016 / API-021 Transaction 边界分类未冻结 | §7.2 + §3.5 |
| P1-5 | 7 角色完整列表 + 40 API × 7 角色权限矩阵 Contract 缺 | §7.3 + Gap-02 |
| P1-6 | IGNORE_TABLES flyway_schema_history_v44 预留表激活条件未冻结 | §6.1 |
| P1-7 | Phase 1 系统设置 26 项页面字段未冻结 | Gap-06 |
| P1-8 | SystemSetting V4.4 范围未冻结 | Gap-07 |
| P1-9 | Transfer 部分失败回滚策略未冻结 | §7.2 + §4.4 |
| P1-10 | Sa-Token @SaCheckRole / @SaCheckPermission 注解 Contract 缺 | Gap-03 |
| **独立 P1 总数** | | **10 项** |

### 7.3 真实 Gap 总数

| Gap | 描述 | 来源 |
|---|---|---|
| **Gap-02** | 6 Service 方法 Contract 缺(Customer / Patient / Employee / ConsultRoom / BigScreen / Company)| §9 真实 Gap |
| **Gap-03** | Sa-Token @SaCheckRole / @SaCheckPermission 注解 Contract 缺 | §9 真实 Gap |
| **Gap-06** | Phase 1 系统设置 26 项页面字段未冻结 | §9 真实 Gap |
| **Gap-07** | SystemSetting V4.4 范围未冻结 | §9 真实 Gap |
| **真实 Gap 总数** | | **4 项** |

### 7.4 Contract 自标 Gap 误判(P0 错位)

| Gap | G2 自报 | 真实归属 |
|---|---|---|
| Gap-01 | 12 Object 字段级 Custom 方法 Contract 缺 | **🔴 P0**(对应 RC-3)|
| Gap-04 | 4 表 companyId 字段 Contract 缺 | **🔴 P0**(对应 RC-3 + RC-5)|
| Gap-05 | doctorId / consultRoomId / scheduleId 字段 | **🔴 P0**(对应 RC-3)|

---

## §8 G2-Contract-02 修复基线表

### 8.1 修复优先级

| 优先级 | Root-Cause-ID | 描述 | 影响范围 | 修复章节 |
|:-:|---|---|---|---|
| 🔴 **P0-最高** | RC-1 | API 路径错位(14 API)| 25 个原 P0 编号 | G2-Contract-02 §7 |
| 🔴 **P0-最高** | RC-2 | Transfer 9-step 错位 | 5 个原 P0 编号 | G2-Contract-02 §9 |
| 🔴 **P0-高** | RC-3a~i | 12 Object 字段级 9 项错位 | 9 个原 P0 编号 | G2-Contract-02 §4 |
| 🔴 **P0-高** | RC-4 | IGNORE_TABLES 不完整 | 3 个原 P0 编号 | G2-Contract-02 §14 |
| 🔴 **P0-中** | RC-5 | company 业务表概念错 | 2 个原 P0 编号 | G2-Contract-02 §14 |
| 🔴 **P0-中** | RC-6 | 公开 API 白名单缺 bigscreen/display | 2 个原 P0 编号 | G2-Contract-02 §11 |
| 🟡 **P1** | Gap-02 / P1-1~3 | 6 Service 方法 Contract | 部分未冻结 | G2-Contract-02 §8 |
| 🟡 **P1** | P1-4 | API-016/021 Transaction 分类 | 推断未冻结 | G2-Contract-02 §9 |
| 🟡 **P1** | P1-5 / Gap-03 | 权限矩阵 / Sa-Token 注解 | 部分冻结 | G2-Contract-02 §11 |
| 🟡 **P1** | P1-6 | IGNORE_TABLES flyway_schema_history_v44 | 预留激活条件 | G2-Contract-02 §14 |
| 🟡 **P1** | Gap-06 / P1-7 | Phase 1 系统设置 26 项字段 | V4.4 未冻结 | G2-Contract-02 后续 Phase 2 |
| 🟡 **P1** | Gap-07 / P1-8 | SystemSetting V4.4 范围 | V4.4 未冻结 | G2-Contract-02 后续 Phase 2 |
| 🟡 **P1** | P1-9 | Transfer 部分失败回滚策略 | 235B 未冻结 | G2-Contract-02 §9 |

### 8.2 修复基线表

| Root-Cause-ID | 原 P0 编号 | Domain | Contract 章节 | Effective Spec | 修复动作 | 是否必须修复后 G2 READY |
|---|---|---|---|---|---|:-:|
| **RC-1** | P0-C1 / C2 / C3 / C4 / C5 / C6 / C7 / C8 / C9 / C10 / C11 / C12 / C13 / C14 | API 路径 | G2 §7.2 | 233 §API-025~040 + 232 §API-025~040 | **完整重写 G2 §7.2,以 233 / 232 为准**(共 14 API Path)| **🔴 必须** |
| **RC-2** | P0-C20 / C21 / C22 / C23 / C24 | Transfer 9-step | G2 §9.2 | 235B §4.2 / §4.3 | **完整重写 G2 §9.2,以 235B §4.2 / §4.3 为准** | **🔴 必须** |
| **RC-3a** | P0-C27 | Object 字段 | G2 §4.2.3 | 238 §4.3 + 236B §3 | Patient 字段重写:`birthDate → patientBirthday`, `gender → patientGender`, 增 `idCard`, **删 `medicalCode`** | **🔴 必须** |
| **RC-3b** | P0-C28 | Object 字段 | G2 §4.2.4 | 238 §4.4 + 235B §2 | Employee 字段重写:增 `adminId`(NOT NULL UNIQUE)/ `nickname` / `departmentId` / `status` | **🔴 必须** |
| **RC-3c** | P0-C29 | Object 字段 | G2 §4.2.5 | 238 §4.5 | ConsultRoom 字段重写:`roomName → consultRoomName`, **删 `roomNo`**, 增 `status` / `examineList` | **🔴 必须** |
| **RC-3d** | P0-C30 | Object 字段 | G2 §4.2.6 | 238 §4.6 + §15 | BigScreen 字段重写:`screenName → bigScreenName`, 增 `sceneType` / `consultRoomIdArray`(JSON)/ `status` | **🔴 必须** |
| **RC-3e** | P0-C31 | Object 字段 | G2 §4.3.1 | 238 §4.8 | AppointmentSchedule 字段重写:`doctorId → employeeId`, **删 `startTime/endTime`**, 增 `remark` | **🔴 必须** |
| **RC-3f** | P0-C32 | Object 字段 | G2 §4.3.2 | 238 §4.9 + 236B §3.5 | AppointmentSlot 字段重写:`maxPatients → capacity`, `currentCount → bookedCount`, `slotStartTime/slotEndTime → startTime/endTime`, 增 `consultRoomId`(FK)/ `serviceType`;**明确 companyId 字段保留但无 FK** | **🔴 必须** |
| **RC-3g** | P0-C33 | Object 字段 | G2 §4.3.3 | 238 §4.7 | Appointment 字段重写:`appointmentTime → slotDate/slotStartTime/slotEndTime`, `doctorId → employeeId`, 增 11+ 字段(appointmentNo/appointmentType/appointmentSource/rescheduledFromId/remark/createdBy/confirmedAt/completedAt/cancelledAt/cancelReason)| **🔴 必须** |
| **RC-3h** | P0-C34 | Object 字段 | G2 §4.3.4 | 238 §4.10 | Visit 字段重写:`doctorId → employeeId`, **删 `checkInTime`**, 增 `visitType` / `transferredFromVisitId` / `transferredFromEmployeeId` / `cancelledAt` / `cancelReason` / `completedAt` / `transferredAt` | **🔴 必须** |
| **RC-3i** | P0-C36 | Object 字段 | G2 §4.3.6 | 238 §4.12 | ReceptionQueue 字段重写:增 `triageQueueId`(UNIQUE)/ `sequenceInRoom` / `calledAt` / `startedAt` / `completedAt` / `skippedTimes` / `cancelReason`,列 6 状态 | **🔴 必须** |
| **RC-4** | P0-C37 | IGNORE_TABLES | G2 §14.4 | 241V4 §6.1 | IGNORE_TABLES 静态清单重写:`{company, user_company}` → 5 个配置项(flyway_schema_history, company, user, user_company, flyway_schema_history_v44)| **🔴 必须** |
| **RC-5** | P0-C38 | Tenant 概念 | G2 §14.2 | 235B §1 + 238 §4.1 | G2 §14.2 明确 company 是 12 业务表之一(不是系统表)| **🔴 必须** |
| **RC-6** | P0-C45 | 公开 API 白名单 | G2 §11.2 | 241V2 §5.6 + 233 §API-040 | G2 §11.2 补 `/api/bigscreen/display`(公开 API)| **🔴 必须** |
| **Gap-02 / P1-1~3** | (未冻结 Service)| Service 方法 | G2 §8.7 | 232 / 233 / 235B / 240 / 241V2 | 6 Service 方法 Contract 冻结(沿用已有冻结)| 🟡 必须 |
| **P1-4** | (未冻结)| Transaction 分类 | G2 §9.1 | 233 | API-016 / API-021 Transaction 分类冻结或标【待确认】 | 🟡 必须 |
| **P1-5 / Gap-03** | (未冻结)| Security | G2 §11.3 / §11.4 | 235B §2 + 233 | 7 角色完整列表 + 40 API × 7 角色权限矩阵 + Sa-Token 注解 冻结 | 🟡 必须 |
| **P1-6** | (未冻结)| IGNORE_TABLES 预留 | G2 §14.4 | 241V4 §6.1 | flyway_schema_history_v44 激活条件 冻结 | 🟡 必须 |
| **Gap-06 / P1-7** | (未冻结)| Phase 1 范围 | (新增)| (侦察未闭环)| Phase 1 系统设置 26 项页面字段 冻结 | 🟡 必须(Phase 1 内)|
| **Gap-07 / P1-8** | (未冻结)| SystemSetting V4.4 | (新增)| (未冻结)| SystemSetting V4.4 范围 冻结 | 🟡 必须(Phase 1 内)|
| **P1-9** | (未冻结)| Transfer 异常处理 | G2 §9.2 | 235B §4.2(未冻结)| Transfer 部分失败回滚策略 冻结或标【待确认】 | 🟡 必须 |

---

## §9 最终判定

### 9.1 G2-Contract-Audit-01 校准结论

| 维度 | 原 G2-Contract-Audit-01 结论 | 校准后结论 |
|---|---|---|
| API P0 数量 | 15(§3.4)+ "1+7+5=13" 内部矛盾 | **🔴 14 项**(1+7+6=14,§3.4 写 5 应为 6)|
| Gap 真实数量 | 3(§9.3 总结)| **🔴 4 项**(§9 表内列 Gap-02/03/06/07,§9.3 漏 1)|
| P0 总数 | 86(§13.1)| **🔴 14 项独立 Root Cause**(原 86 项是同一根因的多次重复计数)|
| Coverage 完整率 | 51.2%(§11)| **🔴 53.4%**(分母应为 116)|
| Coverage 冲突率 | 33.1%(§11)| **🔴 33.6%**(39/116)|
| API-034 Transfer | Path PASS + Transfer P0(混算)| **🔴 已拆分**(Path PASS,Transfer RC-2)|
| 五项独立结论 | A PASS / B-D FAIL / E NOT READY | **保持不变**(校准不改变实质性结论)|

### 9.2 G2-Contract-01 = BLOCK 是否保持

> **保持 = YES**
>
> 校准后,G2-Contract-01 仍有 **14 项独立 Root Cause P0** + **10 项 P1** + **4 项 Gap**:
> - 完整且正确覆盖率仅 **53.4%**(必须 ≥ 80%)
> - 冲突率 **33.6%**(必须 ≤ 5%)
> - Contract Coverage = **FAIL**
> - G2 Contract Readiness = **NOT READY(BLOCK)**

### 9.3 Backend Entry = BLOCK 是否保持

> **保持 = YES**
>
> S1-170E §12 明确:
> > "不允许开始 backend,除非 G2 Contract Gate = READY"
>
> 当前 G2 = NOT READY → Backend Entry = **BLOCK**(沿用 S1-170E 判定)

### 9.4 是否允许进入 G2-Contract-02

> **允许 = YES(下一阶段可创建 G2-Contract-02)**
>
> 前提:
> 1. 不修改 G2-Contract-01(由 G2-Contract-02 替代)
> 2. 不修改任何历史 MD
> 3. G2-Contract-02 必须按 §8 修复基线表逐项修复
> 4. G2-Contract-02 完成后必须再次独立盲审(G2-Contract-Audit-02)
> 5. 只有 G2-Contract-Audit-02 通过后才能讨论 G2 → READY → Backend Entry

---

## §10 最终汇报

### A. 原审计结论哪些仍然有效

| 结论 | 是否有效 |
|---|:-:|
| A. Contract Structural Integrity = PASS | ✓ 仍有效(章节结构完整)|
| B. Effective Spec Consistency = FAIL | ✓ 仍有效(校准后 14 项独立 Root Cause P0)|
| C. API Contract Consistency = FAIL | ✓ 仍有效(14 API Path 错)|
| D. Tenant Contract Consistency = FAIL | ✓ 仍有效(RC-4/5/6)|
| E. G2 Contract Readiness = NOT READY(BLOCK)| ✓ 仍有效 |
| Exception 章节 100% 一致 | ✓ 仍有效 |
| Test(DEFAULT)章节 100% 一致 | ✓ 仍有效 |
| 7 Gap 中 3 项是 P0 Conflict(不是 Gap)| ✓ 仍有效(Gap-01/04/05)|
| Backend Entry = BLOCK | ✓ 仍有效 |

### B. 哪些只是重复计数

| 项 | 数量 | 性质 |
|---|---:|---|
| §3.3 P0-C15~C19(API 顺延次生)| 5 | duplicate of RC-1 |
| §6.3 P0-C39~C45(Tenant 完整性)| 4 | 3 duplicate(RC-4/5/6)+ 3 ✓ 一致 |
| §7.x P0-C46~C70(Service / Transaction / Security)| 11 | 9 duplicate(RC-1/2)+ 7 一致/部分 |
| §8 P0-C86.1~C86.14(E-level Inference)| 14 | 11 duplicate(RC-1/2/3)+ 2 P1 + 1 ✓ |
| §7.4 / §7.5 编号 C71~C85(Exception + DEFAULT)| 15 | 全部 ✓ 一致,**不应列为 P0** |
| **重复 / 一致项合计** | **49 项** | 不形成独立 P0 |

### C. 独立 P0 总数

> **14 项**(RC-1 ~ RC-6,共 6 个 Root Cause Family)

### D. 独立 P1 总数

> **10 项**(P1-1 ~ P1-10)

### E. 4 个真实 Gap

> **Gap-02**(6 Service 方法)+ **Gap-03**(Sa-Token 注解)+ **Gap-06**(Phase 1 系统设置)+ **Gap-07**(SystemSetting V4.4)

### F. G2-Contract-02 修复基线表

> 详见 §8.2 修复基线表(20 项修复动作,14 项 P0 必须 + 6 项 P1 必须)

---

## §11 元审计元约束

> 本元审计(Audit-01R)的局限:

1. **未读取 G2-Contract-01 完整内容**(只读了 §3-§11 关键章节)
2. **基于 G2-Contract-Audit-01 自身证据重新统计**,未独立交叉验证每个 P0 的原始证据
3. **Root Cause 去重基于"修复动作独立性"原则**,不是"语义独立性"原则 — 同一个错误语义可能涉及多个修复动作(如 RC-3 包含 9 个 Object,每个独立修复)

---

## §12 文件元信息

| 字段 | 内容 |
|---|---|
| 文件路径 | `E:\C\minimax\OptFlow PMS\G2-Contract-Audit-01R_问题去重与修复基线校准.md` |
| 创建时间 | 2026-09-16 |
| Baseline HEAD | `6c5acfb1de9342e140f8f813068c92b4fee0b263` |
| Base | 不修改 G2-Contract-01 / 不修改 G2-Contract-Audit-01 / 不修改任何历史 MD |
| 严禁 | 修改 G2-Contract-01 / 修改 G2-Contract-Audit-01 / 修改任何历史 MD / 创建 backend / 写 Java 源码 / 执行 DDL / 连接数据库 / 运行测试 / 创建 V2A-43 / V2A-44 / S1-171 / commit / push |

---

**End of G2-Contract-Audit-01R**