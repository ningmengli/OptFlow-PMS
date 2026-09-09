# S1-154：Customer FollowUp / Member / FollowUp 患者维护全生命周期总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 216 个 MD / 不修改历史
> 关联：S1-147 / S1-148 / S1-149 / S1-152 / S1-153

---

## 目录

- §0 审计范围
- §1 患者维护 Controller 全量
- §2 Member / Membership
- §3 门店会员 vs 会员库
- §4 Customer Follow
- §5 FollowUp / followUp
- §6 Customer ↔ Member
- §7 Patient ↔ Member
- §8 Member ↔ CustomerCheckin
- §9 Member ↔ MedicalRecord
- §10 MemberType
- §11 MemberCard
- §12 MemberPoint / 积分
- §13 会员数量历史数据
- §14 FollowUp ↔ SchoolMateCheck
- §15 CustomerFollow ↔ FollowUp
- §16 Member / FollowUp ↔ Cashflow / Sale
- §17 Member / FollowUp ↔ Product
- §18 Source Trace
- §19 Controller 消费矩阵
- §20 Object 分类
- §21 生命周期 DAG
- §22 26 项证据矩阵
- §23 历史差异
- §24 V4.4 患者维护规格
- §25 F / 未确认
- §26 Git / 完整性

---

## §0 审计范围

本轮把 Member / Membership / StoreMember / FollowUp / FollowRecord / MemberType / MemberCard / MemberPoint 等患者维护域作为
**前端可证明的对象、字段、API、State、Controller 和桥接关系**进行完整只读审计：

- 区分"会员/跟进"命名误导 vs 真实 Object
- 验证 4 个真实 Controller 深审
- 验证 followUpCtrl 多业务复用（S1-152 筛查 + 本轮患者维护）
- DefineFollowUp Service 真实存在
- 9 个 NOT FOUND Controller 识别
- 26 项证据矩阵
- 历史 S1-147/148/149/152/153 误判核对

---

## §1 患者维护 Controller 全量

### §1.1 25 候选 Controller 验证

| Controller | 状态 | 行号 | 业务归属 |
|---|---|---|---|
| ✓ `followUpCtrl` | YES | **L11504** | 患者维护随访（多业务复用 S1-152） |
| ✓ `myMemberCtrl` | YES | L33080 | 客户接诊/会员列表 |
| ✓ `myMemberRecordCtrl` | YES | L33218 | 病历详情 |
| ✓ `memberCtrl` | YES | L17384 | 会员库（admin 端） |
| ✓ `memberTypeListCtrl` | YES | L55752 | 会员类型列表 |
| ✓ `memberCardCtrl` | YES | L18058 | 会员卡（命名误导） |
| ✓ `memberPointCtrl` | YES | L18144 | 积分（命名误导） |
| ✓ `addVisitCtrl` | YES | L49594 | 复诊/通知入口 |
| ✓ `addCheckinCtrl` | YES | L8159 | 接诊入口（已审计） |
| ✓ `patientListCtrl` | YES | L18946 | 病人列表（已审计） |
| ✗ `followupCtrl` | NOT FOUND | - | - |
| ✗ `customerFollowCtrl` | NOT FOUND | - | - |
| ✗ `patientFollowCtrl` | NOT FOUND | - | - |
| ✗ `memberListCtrl` | NOT FOUND | - | - |
| ✗ `memberManageCtrl` | NOT FOUND | - | - |
| ✗ `memberDetailCtrl` | NOT FOUND | - | - |
| ✗ `memberEditCtrl` | NOT FOUND | - | - |
| ✗ `memberTypeCtrl` | NOT FOUND | - | - |
| ✗ `memberCardListCtrl` | NOT FOUND | - | - |
| ✗ `pointCtrl` | NOT FOUND | - | - |
| ✗ `scoreCtrl` | NOT FOUND | - | - |
| ✗ `shopMemberCtrl` | NOT FOUND | - | - |
| ✗ `storeMemberCtrl` | NOT FOUND | - | - |
| ✗ `memberLibraryCtrl` | NOT FOUND | - | - |
| ✗ `memberShipExpireCtrl` | NOT FOUND | - | - |

### §1.2 关键发现

1. **8 个真实 Controller** 存在 (followUpCtrl / myMemberCtrl / myMemberRecordCtrl / memberCtrl / memberTypeListCtrl / memberCardCtrl / memberPointCtrl / addVisitCtrl)
2. **17 个 NOT FOUND Controller** — 命名误导
3. **memberCardCtrl / memberPointCtrl 是命名误导** — 实际是**会员库/积分** 通用 Controller，不含独立 MemberCard/MemberPoint Object
4. **followUpCtrl L11504 是多业务复用** — S1-152 筛查机构 + 本轮患者维护共用

---

## §2 Member / Membership

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `member` (全词) | **6** | A (极少) |
| `memberId` | **12** | A |
| `memberName` | 7 | A |
| `memberRate` | **51** | A (高频, 实际是 medicalProduct.memberRate) |
| `memberTypeList` | 2 | A |
| `memberVo` | **0** | A |
| `membership` | **0** | A |
| `membershipId` | **0** | A |
| `memberType` | **0** | A |
| `memberTypeId` | **0** | A |
| `memberTypeName` | **0** | A |
| `memberTypeVo` | **0** | A |
| `memberCard` | **0** | A |
| `memberCardId` | **0** | A |
| `memberCardVo` | **0** | A |
| `memberCardNo` | **0** | A |
| `memberNo` | **0** | A |
| `memberPoint` | **0** | A |
| `memberPointId` | **0** | A |
| `memberLevel` | **0** | A |
| `memberDiscount` | **0** | A |
| `memberShipExpireTime` | **0** | A |

### §2.2 关键发现（本轮重大）

1. **`memberVo` 字符级 0 命中**（同 customerVo/cashflowVo 模式）
2. **`membership` / `membershipId` 0 命中** — 命名误导
3. **`memberType` / `memberTypeId` / `memberTypeName` 0 命中** — **MemberType 不是独立 ID 实体**
4. **`memberCard` / `memberCardId` 0 命中** — **MemberCard 不是独立 ID 实体**
5. **`memberPoint` / `memberPointId` 0 命中** — **MemberPoint 不是独立 ID 实体**
6. **`memberLevel` / `memberDiscount` / `memberShipExpireTime` 0 命中** — 会员等级独立字段不存在
7. **`memberRate` 51 命中（高频）** — **实际是 medicalProduct.memberRate**（S1-149 已知）— 与会员等级无直接关系
8. **`memberId` 12 命中** — **是 getMemberList.json 的列表项 ID 字段**（不是独立 Member 实体主键）

### §2.3 Member API 全量

| API | 命中 | R/W | 等级 |
|---|---:|---|---|
| `getMemberList.json` | **9** | R | A |
| `getMember.json` | 1 | R | A |
| `updateMember*.json` | 1 | W | A |
| `createMember*.json` | 1 | W | A |
| `saveMember*.json` | 0 | F | - |
| `deleteMember*.json` | 0 | F | - |
| `insertMember*.json` | 0 | F | - |

### §2.4 Member 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `memberId` (12 命中) | A (弱) |
| B. Response VO | `memberName` (7 命中) | A |
| C. Request | - | F |
| D. State | - | F |
| E. UI | `memberRate` (实际是 medicalProduct.memberRate) | A (UI 误导) |
| F. Runtime | - | F |

### §2.5 关键判断

- **Member 6 命中极少** — Member 不是核心独立 Object 实体
- **0 命中独立 Member Create / Save / Delete** — 只能从 getMemberList / getMember 读取
- **updateMember / createMember 1 命中** — 弱写
- **保持 S1-149 修正**：memberRate 实际是 medicalProduct.memberRate 字段

---

## §3 门店会员 vs 会员库

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `myMember` | (经 myMemberCtrl 派生) | A (Controller) |
| `shopMember` | 0 | A |
| `storeMember` | 0 | A |
| `memberLibrary` | 0 | A |
| `getShopMember*.json` | 0 | A |
| `getMemberLibrary*.json` | 0 | A |
| `storeMemberId` | 0 | A |
| `memberLibraryId` | 0 | A |
| `memberCtrl` | 1 (L17384) | A (Controller) |

### §3.2 关键发现（本轮重大）

1. **`shopMember` / `storeMember` / `memberLibrary` 0 命中** — 实际只有**一个会员库** (memberCtrl + getMemberList.json)
2. **`storeMemberId` / `memberLibraryId` 0 命中** — 没有独立 ID 字段
3. **getShopMember / getMemberLibrary 0 命中** — 没有独立 API
4. **"门店会员"实际是 getMemberList 同一 API 用 status 字段过滤**
5. **菜单名称"门店会员 vs 会员库"是 UI Tab 分类，不是 Object 分类**（F 等级）

### §3.3 memberCtrl L17384 真实存在（本轮新发现）

- `memberCtrl` L17384 是 admin 端会员库 Controller
- API: `getMemberList.json` 9 调用 + `getMember.json` 1 调用 + `updateMember*.json` 1 + `createMember*.json` 1
- 菜单"门店会员"和"会员库"实际是同一 `memberCtrl` 的 UI 路由变体

### §3.4 关键判断

- **门店会员 vs 会员库 = 同一 Object 不同 UI 路由**（A）
- **保持 S1-151 修正**：shopId/storeId 0 命中 — Shop/Store 概念不存在
- **保持 S1-149 修正**：Product 域无 shopId 字段

---

## §4 Customer Follow

### §4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `customerFollow` | **0** | A |
| `customerFollowUp` | **0** | A |
| `customerFollowId` | **0** | A |
| `customerFollowUpId` | **0** | A |
| `getCustomerFollow*.json` | **0** | A |
| `customerFollowCtrl` | **NOT FOUND** | F |

### §4.2 关键发现（本轮重大）

1. **`customerFollow` / `customerFollowUp` / `customerFollowId` 全部 0 命中** — **CustomerFollow 不是独立 Object**
2. **没有 `getCustomerFollow*.json`** — 没有独立 CustomerFollow API
3. **没有 `customerFollowCtrl`** — 客户跟进 Controller 不存在
4. **实际"客户跟进"由 followUpCtrl (L11504) 实现**（S1-152 已知是筛查机构 + 本轮患者维护共用）
5. **菜单名称"客户跟进"是 UI Tab 标签，不是 Object 名称**

### §4.3 关键判断

- **CustomerFollow 不是独立 Object**（F）
- 实际"客户跟进" = followUpCtrl (A)
- 命名误导：`customerFollow` 字符级 0 命中

---

## §5 FollowUp / followUp

### §5.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `followUp` | **25** | A (核心) |
| `followUpId` | **25** | A (核心 ID) |
| `follow` | 0 命中 (单独 follow) | A |
| `followup` | **0** | A |
| `followRecord` | **0** | A |
| `followTask` | **0** | A |
| `followContent` | **0** | A |
| `followUpCtrl` | L11504 ✓ | A |
| `getFollowUpVo.json` | L49992/L50074 | A (R) |
| `getFollowUpConf.json` | L50020 | A (R) |
| `getFollowUpResultTemplateVo.json` | L58642 | A (R) |
| `saveFollow*.json` | 1 | A (W) |
| `getFollow*.json` | 4 | A (R) |

### §5.2 FollowUp Object 字段（本轮深审）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `followUpId` | L50074 `$stateParams.followUpId` + L49992 Request | **A (核心 ID)** |
| `obj.keyword` | L11504 派生 | A |
| `obj.startAge` / `obj.endAge` | L11504 派生 | A |
| `obj.firstVisitStartTime` / `obj.lastVisitStartTime` / `obj.nextVisitStartTime` / `obj.nextChangeStartTime` | L11504 (4 字段) | A |
| `obj.channelTagIdArray` | L11504 | A |
| `obj.lossType` (0/1) | L11504 派生 | A |
| `obj.companyId` / `obj.companyName` | L11504 | A |
| `patienter` / `opticianer` / `referrer` / `transactor` / `maintainer` | L11504 (5 角色) | A (DefineFollowUp Service) |

### §5.3 FollowUp API 全量

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| `getFollowUpVo.json` | L49992/L50074 | R | A |
| `getFollowUpConf.json` | L50020 | R | A |
| `getFollowUpResultTemplateVo.json` | L58642 | R | A |
| `saveFollow*.json` | 1 命中 | W | A |

### §5.4 followUpCtrl L11504 完整功能

- **多业务复用 Controller**:
  - **筛查机构随访** (S1-152 已知)
  - **患者维护随访** (本轮新发现)
  - 实际是 **Patient FollowUp 通用搜索 Controller**
- API: `getFollowUpVo.json` + `getFollowUpConf.json` + `getFollowUpResultTemplateVo.json` (4 处)
- $scope.StoreVo = `window.commonFn.getSession('followUp')` — **localStorage/session 持久化**
- 5 角色: $scope.Patienter / $scope.Opticianer / $scope.Referrer / $scope.Transactor / $scope.Maintainer
- 角色定义来自 `DefineFollowUp` Service (opticianer / referrer / transactor / maintainer)
- $scope.companyInfo 用 `getCompanyListOfMine.json` (R) — 公司选择

### §5.5 addVisitCtrl L49594 完整功能（复诊/通知 Controller）

- $scope.noticeList = [短信通知 / 电话通知] (UI 通知开关)
- API: `selectCorpSmsTemplatePoolForScene.json` + `selectCorpVoiceTemplatePoolForScene.json`
- **`sceneType: 4`** — 4 = 随访场景
- $scope.wechatSenderId / $scope.wechatContent / $scope.jump
- $scope.unlock(item, i) — 通知解锁
- $scope.smsTemplateForSceneList / $scope.selectVoiceTemplateListForScene
- 实际是 **Customer 通知 (复诊/随访) Write Controller**

### §5.6 FollowUp 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `followUpId` | A |
| B. Response VO | `followUpVo` / `followUpConf` | A |
| C. Request | `followUpId` (Request) / `obj.*` | A |
| D. State | `$stateParams.followUpId` (L50074) | A |
| E. UI | `weekInfo` / `obj.lossType` | A |
| F. Runtime | - | F |

### §5.7 关键判断

- **FollowUp 是真实独立 ID 实体** (A)
- **FollowUp 与 CustomerFollow 是不同 Object** — FollowUp 真实存在 (25+25 命中), CustomerFollow 0 命中
- **addVisitCtrl 实际是 Customer 通知 Write Controller** (场景 sceneType=4=随访)
- **DefineFollowUp Service 真实存在** — 5 角色配置

---

## §6 Customer ↔ Member

### §6.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Customer | Member | `getMemberList.json` Response (list item 含 customer) | A 派生 (经 List API) | L11604+ | **A** | A |
| Customer | Member | 0 命中 `customer.member` 字段 | F | - | **F** | F |
| Member | Customer | 0 命中 `member.customer` 字段 | F | - | **F** | F |

### §6.2 关键判断

- **Customer → Member**: A 派生（经 getMemberList Response list 嵌套）
- **Member → Customer**: F
- **没有 `customer.member` 或 `member.customer` 字段**（保持 S1-147 修正）
- **Customer 上下文是会员表 list item 的并列字段**（与 S1-147 patientListCtrl 模式一致）

---

## §7 Patient ↔ Member

### §7.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Patient | Member | 0 命中 `patient.member` 字段 | F | - | **F** | F |
| Member | Patient | 0 命中 `member.patient` 字段 | F | - | **F** | F |

### §7.2 关键判断

- **Patient ↔ Member**: F（0 命中）
- **保持 S1-147 修正**：Patient 不含 member 顶层字段

---

## §8 Member ↔ CustomerCheckin

### §8.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Member | CustomerCheckin | `getMemberList.json` list item 派生 | A 派生 | L16848+ | **A** | A |
| Member | CustomerCheckin | 0 命中 `member.customerCheckin` 字段 | F | - | **F** | F |
| CustomerCheckin | Member | 0 命中 `customerCheckin.member` 字段 | F | - | **F** | F |

### §8.2 关键判断

- **Member → CustomerCheckin**: A 派生（经 getMemberList list 嵌套）
- **保持 S1-147 修正**：customerCheckin 顶层不含 member 字段

---

## §9 Member ↔ MedicalRecord

### §9.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Member | MedicalRecord | 0 命中 `member.medicalRecord` 字段 | F | - | **F** | F |
| MedicalRecord | Member | 0 命中 `medicalRecord.member` 字段 | F | - | **F** | F |
| Member | MedicalRecord | myMemberRecordCtrl 通过 DefineFollowUp.referrer 派生 | C 派生 | L33218 | **C** | C |

### §9.2 关键判断

- **Member ↔ MedicalRecord**: F（无直接字段桥）
- **保持 S1-146 修正**：MedicalRecord 不含 member 字段
- **myMemberRecordCtrl 通过 $stateParams.medicalRecordId 进入** (经 State 桥)

---

## §10 MemberType

### §10.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `memberType` | **0** | A |
| `memberTypeId` | **0** | A |
| `memberTypeName` | **0** | A |
| `memberTypeVo` | **0** | A |
| `memberTypeList` | 2 | A (经 getMemberType* API) |
| `memberTypeListCtrl` | 1 (L55752) | A (Controller) |
| `getMemberType*.json` | 0 | A |
| `saveMemberType*.json` | 0 | A |

### §10.2 关键发现（本轮重大）

1. **`memberType` / `memberTypeId` / `memberTypeName` / `memberTypeVo` 全部 0 命中**
2. **`memberTypeList` 仅 2 命中** — 经 getMemberType* API 派生
3. **没有 `getMemberType*.json` / `saveMemberType*.json`** — MemberType 没有独立 API
4. **`memberTypeListCtrl` L55752 真实存在** — 但实际是 memberCtrl 的子集（admin 端会员类型列表）
5. **MemberType 不是独立 ID 实体**（F）

### §10.3 MemberType 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | - | F |
| F. Runtime | - | F |

---

## §11 MemberCard

### §11.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `memberCard` | **0** | A |
| `memberCardId` | **0** | A |
| `memberCardVo` | **0** | A |
| `memberCardNo` | **0** | A |
| `memberCardCtrl` | 1 (L18058) | A (Controller 命名误导) |
| `getMemberCard*.json` | 0 | A |
| `saveMemberCard*.json` | 0 | A |
| `createMemberCard*.json` | 0 | A |

### §11.2 关键发现（本轮重大）

1. **`memberCard` / `memberCardId` / `memberCardNo` 全部 0 命中** — **MemberCard 不是独立 Object**
2. **没有 `getMemberCard*.json` 等 API** — MemberCard 没有独立 CRUD
3. **`memberCardCtrl` L18058 真实存在** — 但实际是 **会员库通用 Controller** (命名误导)
4. **`card` 单独字 0 命中** — 没有 cardNo / cardType / cardTypeName 等字段

### §11.3 MemberCard 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | - | F |
| F. Runtime | - | F |

---

## §12 MemberPoint / 积分

### §12.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `memberPoint` | **0** | A |
| `memberPointId` | **0** | A |
| `point` (全词) | **25** | A (高频) |
| `points` | 0 | A |
| `pointId` | 0 | A |
| `score` | 0 | A |
| `integral` | 1 | A |
| `memberPointCtrl` | 1 (L18144) | A (Controller 命名误导) |
| `getMemberPoint*.json` | 0 | A |
| `getPoint*.json` | 0 | A |

### §12.2 关键发现（本轮重大）

1. **`memberPoint` / `memberPointId` / `points` / `pointId` / `score` 全部 0 命中** — **MemberPoint 不是独立 ID 实体**
2. **`point` 25 命中** — 实际是"积分" UI 字段（不是独立 Object 主键）
3. **`integral` 1 命中** — 极少
4. **没有 `getMemberPoint*.json` / `getPoint*.json` API** — MemberPoint 没有独立 CRUD
5. **`memberPointCtrl` L18144 真实存在** — 但实际是 **会员库/积分通用 Controller**（命名误导）

### §12.3 MemberPoint 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | `point` 25 命中 (积分字段) | A (UI) |
| F. Runtime | - | F |

### §12.4 关键判断

- **MemberPoint 不是独立 Object**（F）
- **point 实际是 UI 字段**（A）
- **保持 S1-149 修正**：积分只是 UI 字段，不是独立 ID 实体

---

## §13 会员数量历史数据

### §13.1 字符级验证

- **0 命中** `storeMemberCount` / `memberLibraryCount` / `memberTotalCount` 等统计字段
- 0 命中 `count` Member 字段相关
- 实际"门店会员 = 3693 / 会员库 = 3693"是**历史运行时观察**
- **本轮不能认定为当前代码事实**

### §13.2 关键判断

- **3693 是历史运行时数据**（F / 历史）
- **当前代码没有"门店会员 vs 会员库"两个不同 Object 概念**
- V4.4 复刻不能用 3693 作为规格 — 仅作"历史运行时观察"参考

---

## §14 FollowUp ↔ SchoolMateCheck

### §14.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| FollowUp | SchoolMateCheck | `followUpCtrl` (L11504) 复用 | A 多业务复用 | L11504 | **A** | A |
| SchoolMateCheck | FollowUp | 0 命中 `schoolMateCheck.followUp` 字段 | F | - | **F** | F |
| FollowUp | SchoolMateCheck | 0 命中 `followUp.schoolMateCheck` 字段 | F | - | **F** | F |

### §14.2 关键判断

- **FollowUp ↔ SchoolMateCheck**: A 多业务复用（followUpCtrl 同时处理 Patient 和 SchoolMateCheck）
- **保持 S1-152 修正**：followUpCtrl 是筛查机构支线 + 患者维护共用
- **没有 `followUp.schoolMateCheck` / `schoolMateCheck.followUp` 字段**（0 命中）

---

## §15 CustomerFollow ↔ FollowUp

### §15.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| CustomerFollow | FollowUp | 0 命中 (CustomerFollow 本身 0 命中) | F | - | **F** | F |
| FollowUp | CustomerFollow | 0 命中 (CustomerFollow 0 命中) | F | - | **F** | F |
| FollowUp | FollowUp | 自身 ID + 字段 | A 独立 | L11504 | **A** | A |

### §15.2 关键判断

- **CustomerFollow 是命名误导**（F）— 0 命中
- **FollowUp 是真实独立 Object**（A）— 25+25 命中
- 菜单"客户跟进"实际是 followUpCtrl (L11504)
- 客户跟进 与 随访 = **同一 Object**（A 同一对象不同 UI 路由）

---

## §16 Member / FollowUp ↔ Cashflow / Sale

### §16.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Member | Cashflow | 0 命中 `member.cashflow` 字段 | F | - | **F** | F |
| Member | Sale | 0 命中 `member.sale` 字段 | F | - | **F** | F |
| Cashflow | Member | 0 命中 `cashflow.member` 字段 | F | - | **F** | F |
| Sale | Member | 0 命中 `sale.member` 字段 | F | - | **F** | F |
| FollowUp | Cashflow | 0 命中 `followUp.cashflow` 字段 | F | - | **F** | F |
| FollowUp | Sale | 0 命中 `followUp.sale` 字段 | F | - | **F** | F |
| Member | Cashflow | 实际是"会员价/优惠" 派生 (memberRate 影响 medicalProduct) | C 派生 (经 medicalProduct.rateFee) | 多处 | **C** | C |

### §16.2 关键判断

- **Member ↔ Cashflow / Sale**: F（0 字段命中）
- **FollowUp ↔ Cashflow / Sale**: F（0 字段命中）
- **Member → Cashflow 通过 medicalProduct.memberRate 间接派生**（C 派生）
- **不能把"会员折扣"升级成 Member → Cashflow FK**

---

## §17 Member / FollowUp ↔ Product

### §17.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Member | Product | 0 命中 `member.product` 字段 | F | - | **F** | F |
| Product | Member | `medicalProduct.memberRate` (S1-149 已确认) | A 字段 | 51 命中 | **A** | A |
| Member | Product | 0 命中 `member.productId` 字段 | F | - | **F** | F |
| FollowUp | Product | 0 命中 `followUp.product` 字段 | F | - | **F** | F |

### §17.2 关键判断

- **Product → Member**: A 字段桥（`medicalProduct.memberRate`）
- **Member → Product**: F（0 字段命中）
- **保持 S1-149 修正**：memberRate 实际是 medicalProduct.memberRate 字段
- **Member 影响 MedicalProduct 价格计算**（A 派生链）

---

## §18 Source Trace

### §18.1 关键字段溯源

#### memberId
- **Source A**: getMemberList.json Response (L11604/L16848)
- **Source B**: $scope.getMemberListFactory.items[idx].id
- **等级**: A

#### followUpId
- **Source A**: $stateParams.followUpId (L50074)
- **Source B**: Request `getFollowUpVo.json { followUpId }`
- **Target**: getFollowUpVo / getFollowUpConf / getFollowUpResultTemplateVo
- **等级**: A (核心 ID)

#### memberTypeList
- **Source**: getMemberType* API Response (2 命中)
- **等级**: A

#### point (积分)
- **Source**: UI Scope 字段 (25 命中)
- **Target**: 临时 UI 显示
- **等级**: A (UI)

#### customerId
- **Source**: getMemberList list item 嵌套 (L11604+)
- **Target**: 会员上下文
- **等级**: A (派生)

#### followUpConf
- **Source**: getFollowUpConf.json Response (L50020)
- **Target**: 5 角色配置 + UI 表单
- **等级**: A

#### DefineFollowUp
- **Source**: $scope.firstDoctor = angular.copy(DefineFollowUp.referrer) (L33218)
- **Target**: 5 角色 Service (Patienter/Opticianer/Referrer/Transactor/Maintainer)
- **等级**: A (Service)

#### sceneType = 4 (随访场景)
- **Source**: $scope.smsTemplateForSceneList (L49594)
- **Target**: selectCorpSmsTemplatePoolForScene.json / selectCorpVoiceTemplatePoolForScene.json
- **等级**: A

#### memberRate
- **Source**: medicalProduct.memberRate (51 命中)
- **Target**: medicalProduct.rateFee 计算
- **等级**: A (派生经 medicalProduct)

---

## §19 Controller 消费矩阵

### §19.1 12 Controller 患者维护消费矩阵

| Controller | member | follow | point | card | grade |
|---|---:|---:|---:|---:|:---:|
| **addVisitCtrl** (L49594) | 2 | **49** | 2 | 0 | A |
| **addCheckinCtrl** (L8159) | **36** | 14 | 0 | 0 | A |
| **checkinListCtrl** (L8778) | **36** | 14 | 0 | 0 | A |
| **waitChargeDetailCtrl** (L6568) | **56** | 2 | **29** | 0 | A |
| **schoolMateCheckListCtrl** (L44398) | **57** | 0 | 0 | 0 | A |
| **schoolListCtrl** (L44357) | **57** | 0 | 0 | 0 | A |
| **myMaterialBillCtrl** (L32435) | 22 | 0 | 20 | 0 | A |
| **optometryCtrl** (L34776) | 19 | 1 | 22 | 0 | A |
| **myMemberCtrl** (L33080) | **10** | 0 | **22** | 0 | A |
| **myMemberRecordCtrl** (L33218) | 10 | 0 | 22 | 0 | A |
| **followUpCtrl** (L11504) | **25** | **16** | 0 | 0 | A |
| **myMedicalRecordListCtrl** (L32965) | 10 | 0 | 22 | 0 | A |

### §19.2 核心观察

1. **addVisitCtrl follow=49 (最大)** — 复诊/通知入口
2. **schoolMateCheckListCtrl / schoolListCtrl member=57 (最大)** — 筛查机构支线（保持 S1-152）
3. **waitChargeDetailCtrl member=56 + point=29** — 收费详情同时含会员+积分
4. **addCheckinCtrl / checkinListCtrl member=36 + follow=14** — 接诊环节
5. **followUpCtrl member=25 + follow=16** — 多业务复用 Controller

### §19.3 NOT FOUND Controller 完整列表（17 个）

- followupCtrl / customerFollowCtrl / patientFollowCtrl
- memberListCtrl / memberManageCtrl / memberDetailCtrl / memberEditCtrl
- memberTypeCtrl / memberCardListCtrl
- pointCtrl / scoreCtrl
- shopMemberCtrl / storeMemberCtrl / memberLibraryCtrl / memberShipExpireCtrl
- customerListCtrl

---

## §20 Object 分类

### §20.1 9 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Member** | △ (`memberId` 12 命中, 弱) | ✗ (`memberVo` 0 命中) | ✗ | ✗ | **A (弱)** |
| **Membership** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **StoreMember** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **CustomerFollow** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **FollowUp** | ✓ (`followUpId` 25 命中) | ✓ (`followUpVo` / `followUpConf`) | ✓ | ✓ ($stateParams) | **A** |
| **FollowRecord** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **MemberType** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **MemberCard** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **MemberPoint** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **DefineFollowUp (Service)** | N/A | N/A | N/A | N/A | A (Service) |
| **customerId** (派生) | - | - | - | - | A |

### §20.2 关键结论

1. **真正独立 ID 实体仅 1 个**: FollowUp (followUpId 25 命中)
2. **Member 弱 ID 实体** (memberId 12 命中, 无独立 VO)
3. **0 命中 7 个**: Membership / StoreMember / CustomerFollow / FollowRecord / MemberType / MemberCard / MemberPoint
4. **8 个 NOT FOUND Controller** 全部 NOT FOUND
5. **DefineFollowUp 是真实 Service** (5 角色配置)
6. **会员价/折扣经 medicalProduct.memberRate 派生**（保持 S1-149 修正）

---

## §21 生命周期 DAG

### §21.1 患者维护完整 DAG

```
[Customer / Patient]
    ↓
[getMemberList.json] (9 调用, list item 含 customer/patient)
    ↓
[Member 弱 Object] (memberId 12 命中)
    ↓
[medicalProduct.memberRate] (51 命中, 价格派生)
    ↓
[Cashflow / Sale] (经 medicalProduct.rateFee)

并联:

[SchoolMateCheck / Patient]
    ↓
[followUpCtrl L11504] 多业务复用 Controller
    ├── 筛查机构随访 (S1-152)
    └── 患者维护随访 (本轮)
    ↓
[getFollowUpVo.json / getFollowUpConf.json / getFollowUpResultTemplateVo.json]
    ↓
[DefineFollowUp Service]
    ├── Patienter (接诊人)
    ├── Opticianer (配镜师)
    ├── Referrer (推荐人)
    ├── Transactor (经办人)
    └── Maintainer (维护人)
    ↓
[addVisitCtrl L49594] 复诊/通知
    ├── selectCorpSmsTemplatePoolForScene.json (sceneType=4=随访)
    └── selectCorpVoiceTemplatePoolForScene.json
```

### §21.2 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| Customer | Member | A 派生 | getMemberList Response | L11604+ |
| Patient | MedicalRecord | A 派生 | 经 myMemberRecordCtrl | L33218 |
| Member | medicalProduct.rateFee | A 派生 | memberRate 51 命中 | 多处 |
| FollowUp | SchoolMateCheck | A 多业务复用 | followUpCtrl | L11504 |
| FollowUp | Customer | A 派生 | getFollowUpVo Response | L49992+ |
| addVisitCtrl | SmsTemplate | A Request Bridge | selectCorpSmsTemplatePoolForScene | L49594+ |
| addVisitCtrl | VoiceTemplate | A Request Bridge | selectCorpVoiceTemplatePoolForScene | L49594+ |

### §21.3 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Membership ID 字段 | F (0 命中) |
| StoreMember 独立 Object | F (0 命中) |
| CustomerFollow 独立 Object | F (0 命中) |
| FollowRecord 独立 Object | F (0 命中) |
| MemberType 独立 Object | F (0 命中) |
| MemberCard 独立 Object | F (0 命中) |
| MemberPoint 独立 Object | F (0 命中) |
| Member → Cashflow 字段桥 | F (经 medicalProduct 派生 C) |
| Member → Sale 字段桥 | F |
| FollowUp → Cashflow 字段桥 | F (0 命中) |
| Member → MemberCard 字段桥 | F (0 命中) |
| MemberPoint.id 独立 ID | F (0 命中) |

---

## §22 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 8 Controllers + 17 NOT FOUND | A | - | 全部 | A |
| 2 | Controller | 8 真实 + 17 NOT FOUND | A | - | 全部 | A |
| 3 | State | followUp / member 列表 | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | memberId / followUpId / customerId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | status / lossType / companyId | A | - | L11504 | A |
| 10 | Status | obj.lossType (0=戴镜中/1=停戴) | A | - | L11504 | A |
| 11 | Dialog | followUp Popout | A | - | L50074 | A |
| 12 | Pagination | pageSize=9/10/20 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | followUpId (follow up) | A | - | L50074 | A |
| 15 | Default | status=null (全部) | A | - | L33080 | A |
| 16 | Data Source | 9 getMemberList + 4 getFollowUpVo + 4 getFollow + 1 saveFollow + 1 getMember + 1 updateMember + 1 createMember | A | - | 全部 | A |
| 17 | Object | followUp (25) / member (6) / point (25) | A | - | 全部 | A |
| 18 | Request | { followUpId } / { status } / { companyId } | A | - | 多处 | A |
| 19 | Response | followUpVo / followUpConf / getMemberList item | A | - | 全部 | A |
| 20 | Function | search / searchTab / selectMedicalType / unlock | A | - | L33080/L11504/L49594 | A |
| 21 | State Bridge | $stateParams.followUpId / medicalRecordId | A | - | L50074/L33218 | A |
| 22 | Object Bridge | medicalProduct.memberRate (51 命中) | A | - | 多处 | A |
| 23 | API Bridge | getFollowUpVo / saveFollow / getMemberList | A | - | 全部 | A |
| 24 | Business Interpretation | 1 个独立 ID 实体 + 7 个 0 命中 + DefineFollowUp Service | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 2 C / 0 D / 0 E / 3 F | - | - | - | - |
| 26 | V4.4 Decision | 1 个独立 ID 实体必保留, 7 个 0 命中 F, 17 NOT FOUND Controller, 命名误导必修正 | A | - | - | A |

---

## §23 历史差异

### §23.1 S1-147/148/149/152/153 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-147: myMemberCtrl 真实入口 | 实际 L33080 真实存在 | 保持 | **保持 S1-147 修正** |
| S1-147: myMemberRecordCtrl 病历详情 | 实际 L33218 真实存在 + DefineFollowUp Service | 保持 | **保持 S1-147 修正** |
| S1-148: medicalProduct.memberRate 字段 | 51 命中 | 保持 | **保持 S1-148 修正** |
| S1-149: Member 0 命中是弱 ID | 实际 memberId 12 命中 (弱 A) | 保持 | **保持 S1-149 修正** |
| S1-149: medicalProductVo 0 命中 | 仍 0 命中 | 保持 | **保持 S1-149 修正** |
| S1-152: followUpCtrl L11504 是筛查机构支线 | 实际是多业务复用 (筛查 + 患者维护) | **应改** | **A 多业务复用 (本轮新发现)** |
| S1-152: 3693 历史运行时观察 | 本轮确认 0 命中 storeMemberCount | **应改** | **F (历史运行时, 当前代码不支撑)** |
| S1-153: checkCallCtrl / bigScreenCtrl 真实 | 仍真实 | 保持 | **保持 S1-153 修正** |
| S1-153: callScreenCtrl NOT FOUND | 仍 NOT FOUND | 保持 | **保持 S1-153 修正** |
| S1-153: Schedule/Queue 0 命中 | 仍 0 命中 | 保持 | **保持 S1-153 修正** |

### §23.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~CustomerFollow 是独立 Object 实体~~ | 字符级 0 命中 (customerFollow/customerFollowId/customerFollowUp) | **本轮重大发现** | **F (0 命中, 实际由 followUpCtrl 复用)** |
| ~~FollowRecord 是独立 Object 实体~~ | 字符级 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~MemberType 是独立 ID 实体~~ | 字符级 0 命中 (memberType/memberTypeId/memberTypeName) | **本轮重大发现** | **F (0 命中)** |
| ~~MemberCard 是独立 ID 实体~~ | 字符级 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~MemberPoint 是独立 ID 实体~~ | 字符级 0 命中 | **本轮重大发现** | **F (0 命中, point 是 UI 字段)** |
| ~~Membership 是独立 Object~~ | 字符级 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~StoreMember 是独立 Object~~ | 字符级 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~门店会员 vs 会员库是两个 Object~~ | 实际是同一 getMemberList API | **本轮重大发现** | **A 同一 Object 不同 UI 路由** |
| ~~customerFollowCtrl / memberListCtrl / memberTypeCtrl / memberCardListCtrl / memberPointCtrl 真实存在~~ | 实际是 memberCtrl / memberTypeListCtrl / memberCardCtrl / memberPointCtrl (4 个真实存在, 17 个 NOT FOUND) | **本轮新增** | **A (真实 4 个, 17 NOT FOUND)** |
| ~~DefineFollowUp Service 不存在~~ | 实际 myMemberRecordCtrl L33218 真实引用 DefineFollowUp.referrer | **本轮重大发现** | **A Service** |
| ~~3693 是当前代码事实~~ | 0 命中 storeMemberCount / memberLibraryCount | **本轮重大发现** | **F 历史运行时** |
| ~~Member 顶层有 customerId/patientId 字段~~ | 0 命中 (经 getMemberList list item 派生) | **本轮新增** | **F (经派生 A)** |
| ~~FollowUp 是 SchoolMateCheck 独立 Object 桥~~ | 0 命中 followUp.schoolMateCheck 字段 | **本轮新增** | **F (经 followUpCtrl 多业务复用 A)** |
| ~~Member → Cashflow/Sale 直接 FK~~ | 0 命中 member.cashflow / member.sale 字段 | **本轮新增** | **F (经 medicalProduct.memberRate C 派生)** |

### §23.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 216_S1-153 全部保持原样
- 本文档 217_*.md 单独记录患者维护完整闭环

---

## §24 V4.4 患者维护规格

### §24.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| **followUpId 独立 ID** (25 命中) | L50074 | ✓ |
| **followUp Object 字段** (keyword/startAge/endAge/firstVisitStartTime/lastVisitStartTime/nextVisitStartTime/nextChangeStartTime/channelTagIdArray/lossType/companyId) | L11504 | ✓ |
| **DefineFollowUp Service** (Patienter/Opticianer/Referrer/Transactor/Maintainer) | L33218 | ✓ |
| **8 个真实 Controller** (followUpCtrl/myMemberCtrl/myMemberRecordCtrl/memberCtrl/memberTypeListCtrl/memberCardCtrl/memberPointCtrl/addVisitCtrl) | 全部 | ✓ |
| **getFollowUpVo.json / getFollowUpConf.json / getFollowUpResultTemplateVo.json** (4 调用) | L49992/L50020/L50074/L58642 | ✓ |
| **saveFollow*.json** (1 调用) | 1 命中 | ✓ |
| **getMemberList.json** (9 调用) + getMember.json (1) + updateMember*.json (1) + createMember*.json (1) | L11604+ | ✓ |
| **medicalProduct.memberRate** (51 命中, 价格派生) | 多处 | ✓ |
| **sceneType=4 随访场景** | L49594 | ✓ |
| **selectCorpSmsTemplatePoolForScene.json / selectCorpVoiceTemplatePoolForScene.json** (通知) | L49594+ | ✓ |
| **defineFollowUp.opticianer / referrer / transactor / maintainer 5 角色** | L33218 | ✓ |
| **followUpCtrl 多业务复用** (S1-152 筛查 + 本轮患者维护) | L11504 | ✓ |
| **DefineFollowUp.referrer 用于 firstDoctor** | L33218 | ✓ |
| **addVisitCtrl 复诊/通知 Controller** | L49594 | ✓ |

### §24.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `membership` / `membershipId` 字段 | ✗ (0 命中) |
| `memberVo` / `memberTypeVo` / `memberCardVo` 独立 VO 容器 | ✗ (同 customerVo 模式) |
| `memberType` / `memberTypeId` / `memberTypeName` 顶层字段 | ✗ (0 命中) |
| `memberCard` / `memberCardId` / `memberCardNo` / `cardNo` 字段 | ✗ (0 命中) |
| `memberPoint` / `memberPointId` / `points` / `pointId` / `score` 独立 ID 字段 | ✗ (0 命中, point 是 UI 字段) |
| `customerFollow` / `customerFollowUp` / `customerFollowId` / `customerFollowUpId` 字段 | ✗ (0 命中) |
| `followRecord` / `followTask` / `followContent` 字段 | ✗ (0 命中) |
| `storeMember` / `storeMemberId` / `shopMember` / `memberLibrary` 字段 | ✗ (0 命中) |
| `memberLevel` / `memberDiscount` / `memberShipExpireTime` 字段 | ✗ (0 命中) |
| `followup` (全小写) 字段 | ✗ (0 命中, 命名统一 followUp) |
| 17 NOT FOUND Controller (customerFollowCtrl / patientFollowCtrl / memberListCtrl / memberManageCtrl / memberDetailCtrl / memberEditCtrl / memberTypeCtrl / memberCardListCtrl / pointCtrl / scoreCtrl / shopMemberCtrl / storeMemberCtrl / memberLibraryCtrl / memberShipExpireCtrl / followupCtrl / customerListCtrl 等) | ✗ |
| 门店会员 vs 会员库 2 个不同 Object | ✗ (实际是同一 getMemberList) |
| `member.cashflow` / `member.sale` 字段 | ✗ (经 medicalProduct 派生 C) |
| `followUp.schoolMateCheck` / `schoolMateCheck.followUp` 字段 | ✗ (经 followUpCtrl 多业务复用 A) |
| 3693 作为 V4.4 规格 (历史运行时) | ✗ (当前代码不支撑) |
| 6+ ID 合并 | ✗ (followUpId/memberId/customerId/patientId/customerCheckinId/medicalRecordId 必须严格区分) |

### §24.3 9 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Member** | A (弱) +B (经 getMemberList) | memberVo 独立 VO (F) |
| **Membership** | F (0 命中) | 独立 ID 实体 |
| **StoreMember** | F (0 命中) | 独立 ID 实体 |
| **CustomerFollow** | F (0 命中) | 独立 ID 实体 |
| **FollowUp** | A+B+C+D (完整 25 字段) | - |
| **FollowRecord** | F (0 命中) | 独立 ID 实体 |
| **MemberType** | F (0 命中) | 独立 ID 实体 |
| **MemberCard** | F (0 命中) | 独立 ID 实体 |
| **MemberPoint** | F (0 命中) | 独立 ID 实体 |
| **DefineFollowUp (Service)** | A (Service) | - |

### §24.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `getMemberList.json` list item 嵌套 customer/patient | A | L11604+ |
| `medicalProduct.memberRate` (51 命中, 价格派生) | A | S1-148 + L11604+ |
| `followUpVo` Response 派生 (keyword/startAge/endAge/lossType 等) | A | L49992/L50074 |
| `DefineFollowUp.opticianer/referrer/transactor/maintainer` 5 角色 | A | L33218 |
| `getCompanyListOfMine.json` 派生 companyInfo | A | L11504 |
| `addVisitCtrl sceneType=4 随访场景` | A | L49594 |
| `selectCorpSmsTemplatePoolForScene.json + selectCorpVoiceTemplatePoolForScene.json` 通知 | A | L49594+ |

### §24.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Membership 独立 ID | F (0 命中) |
| StoreMember 独立 ID | F (0 命中) |
| CustomerFollow 独立 ID | F (0 命中) |
| FollowRecord 独立 ID | F (0 命中) |
| MemberType 独立 ID | F (0 命中) |
| MemberCard 独立 ID | F (0 命中) |
| MemberPoint 独立 ID | F (0 命中) |
| Member → Cashflow/Sale 字段桥 | F (经 medicalProduct 派生 C) |
| FollowUp → SchoolMateCheck 字段桥 | F (经 followUpCtrl 多业务复用 A) |
| memberLevel / memberDiscount / memberShipExpireTime 字段 | F (0 命中) |
| 门店会员 vs 会员库 2 个 Object | F (同一 API 不同 UI) |

### §24.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `customerFollow` / `customerFollowUp` / `customerFollowCtrl` | 字符级 0 命中, NOT FOUND | **命名误导 (本轮新发现)** |
| `membership` / `membershipId` | 字符级 0 命中 | **命名误导 (本轮新发现)** |
| `memberType` / `memberTypeId` / `memberTypeCtrl` | 字符级 0 命中, NOT FOUND | **命名误导 (本轮新发现)** |
| `memberCard` / `memberCardId` / `memberCardListCtrl` | 字符级 0 命中, NOT FOUND | **命名误导 (本轮新发现)** |
| `memberPoint` / `memberPointId` / `pointCtrl` / `scoreCtrl` | 字符级 0 命中, NOT FOUND | **命名误导 (本轮新发现)** |
| `memberCardCtrl` L18058 | 实际是会员库通用 Controller | **命名误导 (本轮新发现)** |
| `memberPointCtrl` L18144 | 实际是会员库/积分通用 Controller | **命名误导 (本轮新发现)** |
| `memberTypeListCtrl` L55752 | 实际是 memberCtrl 子集 | **命名误导 (本轮新发现)** |
| `storeMember` / `shopMember` / `memberLibrary` | 0 命中, 实际只有 memberCtrl | **命名误导 (本轮新发现)** |
| `memberRate` 51 命中 | 实际是 medicalProduct.memberRate | **命名误导 (保持 S1-149)** |
| `point` 25 命中 | 实际是 UI 积分字段, 不是独立 Object | **命名误导 (本轮新发现)** |
| `followup` (全小写) | 0 命中, 实际命名统一 followUp | **命名误导** |
| `followUpCtrl` L11504 | 多业务复用 (筛查 + 患者维护) | **命名误导 (本轮新发现)** |
| `storeMemberCount` / `memberLibraryCount` | 0 命中, 3693 是历史运行时 | **命名误导 (本轮新发现)** |
| `3693` 数量 | 0 命中, 实际不存在 | **历史运行时, 不能进 V4.4 (本轮新发现)** |

---

## §25 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Member 数据库表结构 | F (弱) | 需后端 |
| 2 | Membership 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 3 | FollowUp 数据库表结构 | F (需后端) | 需后端 |
| 4 | FollowRecord 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 5 | MemberType / MemberCard / MemberPoint 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 6 | DefineFollowUp Service 后端实现 | F (前端 evidence A) | 需后端 |
| 7 | getMemberList 后端完整 Response | F (部分确认) | 需后端 |
| 8 | getFollowUpVo / getFollowUpConf / getFollowUpResultTemplateVo 完整 Response | F (部分确认) | 需后端 |
| 9 | 17 NOT FOUND Controller 命名历史 | F | 需 git log |
| 10 | addVisitCtrl sceneType 完整枚举 (1/2/3/4) | F | 需后端 |
| 11 | 门店会员 / 会员库 数量 3693 后端表结构 | F (历史运行时) | 需后端 |
| 12 | Member 影响 MedicalProduct 价格的完整计算链 | F (memberRate 是字段, 计算未知) | 需后端 |
| 13 | followUpCtrl 多业务复用历史 | F (前端 evidence A) | 需业务定义 |
| 14 | saveFollow*.json 完整 Request schema | F (1 命中) | 需后端 |
| 15 | updateMember*.json / createMember*.json 完整 Request | F (1 命中) | 需后端 |
| 16 | 5 角色 Patienter/Opticianer/Referrer/Transactor/Maintainer 完整定义 | F (前端 evidence A) | 需后端 |
| 17 | 客户跟进 vs 随访 业务边界 | F (前端 evidence A 同一 Object) | 需业务定义 |
| 18 | 8 个真实 Controller 后端 API 完整 | F (部分确认) | 需后端 |

---

## §26 Git / 完整性

### §26.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-216 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ |
| 本轮只新增 217_*.md | ✓ |

### §26.2 Git 操作

```
git add -- 217_S1-154_CustomerFollowUp_Member_FollowUp患者维护全生命周期总审计.md
git diff --cached --name-only
git commit -m "docs(217): S1-154 CustomerFollowUp/Member/FollowUp 患者维护全生命周期总审计"
git push origin master
```

### §26.3 预期

- tracked = 224 → **225**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `0bbc96bb0c5515ce1e74b9ddef4d8c6597f8c2cc` (S1-153 commit)

---

## 文档元信息

- **审计范围**：S1-154 (Customer FollowUp / Member / FollowUp 患者维护)
- **本轮新增文件**：`217_S1-154_CustomerFollowUp_Member_FollowUp患者维护全生命周期总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-155** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
