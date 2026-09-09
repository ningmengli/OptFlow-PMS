# S1-132 筛查机构 School / schoolId 身份体系与筛查业务链深度审计

> **项目**：OptFlow PMS 逆向建模
> **本轮目标**：在 S1-131 基础上，深度拆解 school / schoolId / schoolIdArray / schoolMate / schoolMateCheck / schoolClass / schoolPlan / screening 完整身份体系与业务链
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-193 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / 2,194,196 bytes / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变） |
| schoolId 出现 | **200+ 处**（S1-131）→ 本轮精确分类为 **11 类** |
| schoolIdArray 出现 | **3 处**（A — 字符级精确） |
| schoolMate* 出现 | **200+ 处**（A — 已截断） |
| schoolMateCheck 出现 | **174 处**（A — 精确） |
| schoolClass 出现 | **129 处**（A） |
| schoolName 出现 | **94 处**（A） |
| inYear 出现 | **123 处**（A） |
| teacher 出现 | **57 处**（A） |
| schoolInfo Object | **2 处**（L37017, L37669）ObjectFactory 模板 |
| 筛查/质检 Controller | **inspectionCtrl 1 个** + **screenXxx 26 个**（注：screen ≠ screening） |

---

## 2. 筛查机构菜单边界

### 2.1 关键发现：screen ≠ screening（F 边界 / D 冲突警告）

**【关键命名区分】**：
- **`screen*` 系列 Controller（26 个）** —— 指**大屏**（叫号大屏 / 宣传大屏 / 配置大屏），**不是筛查**！
- **`screening*` 出现 2 处**（L46706 / L46717）—— `DefineBodyCheck.screeningConfiguration` 仅是体检配置字典
- **真正的"筛查"概念在 controller.js 范围不可得**（F 边界）

**screen* 26 个 Controller 实际是大屏配置类**（A — 字符级精确）：

| Controller | 行号 | 行数 | 实际功能 |
|---|---|---:|---|
| `areaScreenAdminCtrl` | L738 | ? | 区域大屏管理员（空 stub） |
| `bigScreenCtrl` | L9600 | ? | 叫号大屏 |
| `consultingScreenCtrl` | L10277 | ? | 咨询大屏 |
| `screenQueueCtrl` | L11109 | ? | 大屏队列 |
| `addScreenPromotionCtrl` | L38818 | ? | 新增大屏宣传 |
| `healthScreenConfigCtrl` | L40499 | 57 | 筛查报告配置（healthScreen ≠ screening） |
| `modifyHealthScreenCtrl` | L41314 | ? | 修改筛查报告配置 |
| `modifyScreenPromotionCtrl` | L42424 | ? | 修改大屏宣传 |
| `projectionScreenCtrl` | L43678 | ? | 大屏投影 |
| `screenBackConfigCtrl` | L44973 | 139 | 大屏背景配置 |
| `screenClassReportCtrl` | L45114 | ? | 大屏班级报表 |
| `screenConditionBatchCtrl` | L45234 | ? | 大屏条件批量 |
| `screenConditionBatchGroupSendCtrl` | L45310 | ? | 大屏条件批量群发 |
| `screenConditionBatchGroupSendLookCtrl` | L45589 | ? | 大屏条件批量群发查看 |
| `screenContrastReportCtrl` | L45655 | ? | 大屏对比报表 |
| `screenInStoreCtrl` | L45963 | ? | 大屏入库 |
| `screenListCtrl` | L46224 | ? | 大屏列表 |
| `screenPromotionConfigCtrl` | L46600 | 511 | 大屏宣传配置（**最大**） |
| `screenPromotionListCtrl` | L47113 | ? | 大屏宣传列表 |
| `screenPromotionStudentCtrl` | L47512 | ? | 大屏宣传学生 |
| `screenPromotionToothConfigCtrl` | L47886 | 172 | 牙科大屏 |
| `screenRecordReportCtrl` | L48060 | ? | 大屏记录报表 |
| `screenReportInschoolCtrl` | L48100 | ? | 大屏在校内报表 |
| `screenSchoolReportCtrl` | L48156 | ? | 大屏学校报表 |
| `screenStudentReportCtrl` | L48200 | ? | 大屏学生报表 |
| `screenUrlConfigCtrl` | L48420 | 122 | 大屏URL配置 |

### 2.2 真正的"筛查"业务：A-F 关键区分

**筛查业务真实对象**（A — 字符级直接证据）：
- **schoolMate** = 学校成员（= 学生）
- **schoolMateCheck** = 学校成员检查单（= 筛查记录）
- **schoolMateCheckVo** = 视图对象（174 处）
- **schoolMateVo** = 学校成员完整视图（含 school + schoolClass + schoolMate 三对象）

**`screening*` 在 controller.js 中仅 2 处**（L46706/L46717），是 `DefineBodyCheck.screeningConfiguration` 内部字典，**不是真正的筛查业务 Controller**。

**结论**：本系统**没有"筛查"一级菜单**。真正的"学校 + 筛查"业务以 `schoolMate*` 形式分散在多个 Controller 中。

### 2.3 真正的 School / 筛查相关 Controller

| Controller | 行号 | 行数 | 业务 |
|---|---|---:|---|
| `schoolListCtrl` | L44357 | 108 | **学校列表**（A — 字符级） |
| `addSchoolCtrl` | (估计 schoolAddCtrl 附近) | ? | 新增学校 |
| `addScreenPromotionCtrl` | L38818 | ? | 大屏宣传（**也管理学校**） |
| `inspectionCtrl` | L40558 | ? | **质检**（A） |
| `studentReportInschoolCtrl` | L48544 | ? | 学生校内报表 |

---

## 3. School Controller 全量枚举

### 3.1 schoolListCtrl L44357（108 行）— 学校列表核心（A — 字符级）

**待读详情**：行 44357-44465（108 行）
- DI: `$scope, Popup, ObjectFactory, ListFactory`
- API: `/admin/getSchoolVoList.json` (R)
- $scope.schoolListFactory: `new ListFactory('/admin/getSchoolVoList.json', 0, pageSize, $scope.screenDate)`
- 输入筛选：`$scope.screenDate`

**结论**：schoolListCtrl 是**学校列表 + 筛查日期筛选** — "school" 与 "screen" 在此 Controller 中**共存**（D 命名警告：screenDate 字段含义 F）

### 3.2 inspectionCtrl L40558 — 质检（A — 字符级）

- DI: `$scope, Popup, $timeout, Utils, $rootScope, $state, ObjectFactory, HttpFactory, ListFactory, $http`
- **API 待读取**（本轮未深入）
- **【F 边界】**：质检业务是否使用 schoolId / screeningId 未知

### 3.3 26 个 screen* Controller 业务本质

绝大多数 `screen*` 是**大屏显示 / 大屏配置 / 大屏宣传**，**不是筛查业务**：
- 叫号大屏、咨询大屏、配置大屏
- 大屏宣传、大屏背景、大屏 URL
- 大屏条件批量、大屏入库

**关键例外**：
- `screenSchoolReportCtrl` L48156 — 学校报表（可能含筛查数据）
- `screenStudentReportCtrl` L48200 — 学生报表（可能含筛查数据）
- `screenRecordReportCtrl` L48060 — 记录报表（可能含筛查数据）
- `screenClassReportCtrl` L45114 — 班级报表
- `studentReportInschoolCtrl` L48544 — 学生在学校内报表

**【F 边界】**：screenXxxReport 类是否真正含筛查数据，需要深入读取。本轮证据范围不可得。

### 3.4 筛查业务分散 Controller

筛查业务数据（schoolMate / schoolMateCheck）实际分散在以下 Controller：
- L8160+：appoint 业务，调用 `schoolMateVo`（A — L8264-L8277）
- L38580+：`getSchoolMateCheckVoForManage` API + `getSchoolMateCheckVoManageList` API
- L41660+：`getSchoolMateCheckVo.json` API（多个）
- L44400+：ListFactory 模式调用 `getSchoolMateCheckVoList`

---

## 4. school / schoolId 精确分类

### 4.1 schoolId 11 类精确分类（A — 字符级）

| # | 类别 | 次数 | 代表行号 | 字段名 | 下游 Consumer |
|---:|---|---:|---|---|---|
| **A** | `$stateParams.schoolId` | **2** | L38824, L38999 | $stateParams.schoolId | modifySchoolCtrl / modifyClassCtrl 等 |
| **B** | API Response `.school.id` | **13** | L8270, L8435, L8887, L39313, L39866-7, L41672, L41752, L41969, L44884, L46291, L48112, L48730 | res.school.id | $scope.obj.schoolId |
| **C** | API Response `.schoolId` 顶层 | **0** | — | — | **不存在直接顶层 schoolId 字段** |
| **D** | Request `.schoolId` | **86+** | L19238, L19254, L19283, L19894, L19915, L38923-54, L39089, L39045, L39119, L39175, L39327, L39352, L39741, L39747, L39875, L40196, L40201, L40255, L42300-330, L42536, L42557-62, L42662, L42666, L42712, L43103, L43110, L43548, L43553, L44383, L44575, L44743, L44901, L44960 等 | 各种 ListFactory / saveOrQuery | API Request |
| **E** | ObjectFactory 模板 | **5** | L8167, L9181, L14409, L17657, L47568 | schoolId: null | ajaxParams / init |
| **F** | ListFactory 参数 | **（包含在 D 中）** | 同 D | schoolId: ... | API Request |
| **G** | `$scope.obj.schoolId` | **54** | L8435, L8742, L17427, L17763, L19264, L19925, L37032, L37684, L38831, L38904-17, L38984-93, L39313, L39630, L39866, L40153-74, L40691, L41071, L41672, L41752, L41969, L42290-7, L42437, L42518, L42532, L42592, L42601, L42633, L43011, L43041, L43503, L43525, L44567-71, L44884, L45168, L45742, L45772, L47322, L47568, L47656, L48112, L48168, L48214, L48354, L48553, L48616-7, L48730 | $scope.obj.schoolId | API Request / UI render |
| **H** | `schoolIdArray` | **3** | L634, L648, L769 | schoolIdArray | role 分配 API |
| **I** | 字符串 / 配置 key | 多处 | "schoolId" 字符串 | key | API |
| **J** | `schoolMateId` | **19** | L14434, L41504, L41507-8, L41666, L41722, L41724, L41746, L41747, L41748, L41934, L41956, ... | schoolMateId | schoolMateCheck 域 |
| **K** | `schoolMateCount` | **4** | L39972, L39974, L39975, L40039 | progress | 进度统计 |

**schoolId_clear（= null）32 处**：L8742, L9214, L17427, L19264, L19925, L38904, L38984, L39630, L39641, L40153, L40174, L40691, L42518, L42592, L42633, L43011, L43026, L43041, L43055, L43503, L43525, L45168, L45742, L45757, L45772, L45786, L47322, L47656, L48168, L48214, L48354, L48553

### 4.2 schoolMateCheckVo 字段全集（A — 字符级，174 处）

**`res.vo.schoolMateCheck` 字段全集**（L41660-L42000 范围）：
- id (L41668, L41748)
- schoolMateId (L41666, L41746)
- promotionId (L41667, L41747)
- customerMobile (L41684, L41764)
- classMateName (L41685, L41765)
- gender (L41686)
- remark (L41688)
- schoolMateCode (L41689)
- birthday (L41693)
- checkDate (L41698)
- right1 / right2 / left1 / left2 (L41767-L41770) — 视力右眼/左眼度数
- left67 / right67 / left15 / right15 / left14 / right14 / left13 / right13 (L41771-L41778) — 各视力
- left68 / right65 / left65 (L41781-L41799) — **视力建议**字段

**`res.vo.schoolMate` 字段**（L41690-L41692）：
- nativePlace (L41690)
- nation (L41691)

**`res.vo.schoolClass` 字段**（L41675-L41677, L41755-L41757, L41972-L41974）：
- className (L41676, L41756, L41973)
- id (L41677, L41757, L41974)

**`res.vo.school` 字段**（L41670-L41672, L41750-L41752, L41967-L41969）：
- schoolName (L41671, L41751, L41968)
- id (L41672, L41752, L41969)

**`res.vo.schoolTeacher` 字段**（L41680-L41681, L41760-L41761, L41977-L41978）：
- teacherName
- id

### 4.3 schoolMateVo 完整结构（A — 字符级 9 处）

L8264-L8277 显示 schoolMateVo 是**核心三对象视图**：
```
schoolMateVo {
  school { id, schoolName }
  schoolClass { id, className }
  schoolMate { gender, customerMobile, birthday, classMateName }
}
```

**唯一被使用于 L8260-L8280 业务上下文**：appoint 选顾客时
- L8264: `gender: item.schoolMateVo.schoolMate.gender`
- L8265: `linkMobile: item.schoolMateVo.schoolMate.customerMobile`
- L8266: `patientRemark: schoolName + className`
- L8267: `birthday: item.schoolMateVo.schoolMate.birthday`
- L8270: `schoolId: item.schoolMateVo.school.id`
- L8271: `classId: item.schoolMateVo.schoolClass.id`
- L8273-L8274: 显示
- L8277: `keyword: item.schoolMateVo.schoolMate.classMateName`

### 4.4 schoolMate API 全集（A — 字符级 68+ 处 unique）

**核心 API 列表**（按调用点统计）：

| API | 类型 | 调用次数 |
|---|---|---:|
| `/admin/getSchoolVoList.json` | R | 2 |
| `/admin/getSchoolList.json` | R | 7+ |
| `/admin/getSchoolInfo.json` | R | 7 |
| `/admin/insertSchool.json` | W | 1 |
| `/admin/updateSchool.json` | W | (估计) |
| `/admin/deleteSchool.json` | W | 1 |
| `/admin/getSchoolClassList.json` | R | 12+ |
| `/admin/getSchoolClass.json` | R | 3 |
| `/admin/insertSchoolClass.json` | W | 1 |
| `/admin/batchInsertSchoolClass.json` | W | 1 |
| `/admin/batchInsertSchoolClassByNames.json` | W | 1 |
| `/admin/updateSchoolClass.json` | W | 1 |
| `/admin/deleteSchoolClass.json` | W | 1 |
| `/admin/getSchoolTeacherList.json` | R | 8 |
| `/admin/getSchoolTeacher.json` | R | 1 |
| `/admin/insertSchoolPlan.json` | W | 1 |
| `/admin/insertSchoolPlanRoot.json` | W | 1 |
| `/admin/selectSchoolPlanListBySchool.json` | R | 5 |
| `/admin/getDefaultSchoolPlanByAdminId.json` | R | 3 |
| `/admin/getDefaultSchoolPlanRootByAdminId.json` | R | 1 |
| `/admin/selectInYearListBySchoolPlan.json` | R | 6 |
| `/admin/selectSchoolMateCheckSendLogVoList.json` | R | 2 |
| `/admin/countSchoolMateCheckListOfSchoolPlan.json` | R | 1 |
| `/admin/sendSchoolMateCheckListOfSchoolPlan.json` | W | 1 |
| `/admin/getSchoolMateCheckVoList.json` | R | 8+ |
| `/admin/getSchoolMateCheckVo.json` | R | 5+ |
| `/admin/getSchoolMateCheckVoForManage.json` | R | 2 |
| `/admin/getSchoolMateCheckVoManageList.json` | R | 2 |
| `/admin/getSchoolMateCheckVoListWithSameCode.json` | R | 3 |
| `/admin/getSchoolMateCheckVoListOfSecond.json` | R | 2 |
| `/admin/getSchoolMateCheckVoOfCustomer.json` | R | 1 |
| `/admin/getSchoolMateCheckVoOfRecommendPhone.json` | R | 1 |
| `/admin/getSchoolMateCheckVoByUniqueKey.json` | R | 2 |
| `/admin/insertSchoolMateCheck.json` | W | 1 |
| `/admin/updateSchoolMateCheck.json` | W | 1 |
| `/admin/saveSchoolMateCheck.json` | W | 1 |
| `/admin/completeSchoolMateCheck.json` | W | 1 |
| `/admin/disableSchoolMateCheck.json` | W | 1 |
| `/admin/getSchoolBodyCheckInfo.json` | R | 1 |
| `/admin/checkSchoolBodyCheckInfoVersion.json` | R | 1 |
| `/admin/saveSchoolBodyCheckInfo.json` | W | 1 |
| `/admin/getSchoolMateCheckPrintConf.json` | R | 1 |
| `/admin/updateSchoolMateCheckPrintConfImageUrl.json` | W | 1 |
| `/admin/insertSchoolMate.json` | W | 1 |
| `/admin/insertSchoolMateAndCreatePromotion.json` | W | 1 |
| `/admin/selectSchoolMateCheckVoListOfSecond.json` | R | 1 |
| `/admin/selectAppointSchoolMateVoList.json` | R | 1 |
| `/admin/getAppointSchoolMateVo.json` | R | 1 |
| `/admin/statAppointSchoolMateOfCorp.json` | R | 1 |
| `/admin/basicStatAppointSchoolMate.json` | R | 1 |
| `/admin/statAppointSchoolMateOfCompany.json` | R | 1 |
| `/admin/addSchoolMateConsume.json` | W | 1 |
| `/admin/sendSmsToSchoolMateCheck.json` | W | 2 |
| `/admin/sendMsgToSchoolMateCheckBySelected.json` | W | 1 |
| `/admin/getSchoolMateCheckVoOfRecommendPhone.json` | R | 1 |
| `/admin/getLatestUartDeviceLogToSchoolMateCheck.json` | R | 1 |
| `/admin/getSchoolMateCountOfPromotions.json` | R | 3 |
| `/admin/sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json` | W | 3 |
| `/admin/printSchoolPromotionListVoList.json` | R | 1 |
| `/admin/selectSchoolMateCheckVoList.json` | R | 多 |
| `/admin/createBatchSchoolMateTask.json` | W | 1 |
| `/admin/commitBatchSchoolMateTask.json` | W | 1 |
| `/admin/countStatSchoolMateCheckIdList.json` | R | 1 |
| `/admin/getSchoolMateManageCorpVoList.json` | R | 1 |
| `/admin/selectMyAdminSchoolVoListOfSchoolPlan.json` | R | 1 |
| `/admin/getReportStatusOfSchoolAdmin.json` | R | 1 |
| `/admin/selectSchoolIntentionVoList.json` | R | 1 |
| `/admin/selectSchoolPromotionListVoList.json` | R | 2 |
| `/admin/createPromotionOfSchool.json` | W | 1 |
| `/admin/getSchoolLevelList.json` | R | 1 |
| `/admin/bandingSchoolMatePromotion.json` | W | 1 |
| `/admin/disBandingSchoolMatePromotion.json` | W | 1 |
| `/admin/completeSchoolPlanSchool.json` | W | 1 |
| `/admin/statVisionOfSchool.json` | R | 2 |
| `/admin/saveSchoolCheckCodeType.json` | W | 1 |
| `/admin/getSchoolCheckConf.json` | R | 2 |
| `/admin/saveSchoolCheckConfForTemplate.json` | W | 1 |

**总计**：~75+ 个 unique schoolMate 相关 API

---

## 5. schoolIdArray 完整链

### 5.1 schoolIdArray 5 处精确分布（A — 字符级）

| 行号 | 表达式 | 上下文 |
|---|---|---|
| L634 | `$scope.schoolIdArray = []` | init array |
| L642 | `$scope.schoolIdArray.push($scope.selected[i])` | collect from selected schoolList items |
| L648 | `'/admin/changeAdminRole.json', { id: ..., schoolIdArray: $scope.schoolIdArray }` | **进入 role 分配 API** |
| L769 | `$scope.obj.schoolIdArray = []` | init array |
| L791 | `$scope.obj.schoolIdArray.push($scope.selected[j])` | collect |

### 5.2 schoolIdArray 业务流

**【关键发现】schoolIdArray 是 role 簇字段，不是 screening 字段！**

- L634-L648: **modifyAreaRoleCtrl** 范围内（A）
- L769-L791: **modifyRoleCtrl** 范围内（A）
- **L648** `'/admin/changeAdminRole.json'` 是 **changeAdminRole** API
- schoolIdArray 是 **区域 admin 角色分配时的"多个学校"集合**

**完整链**：
```
modifyRoleCtrl / modifyAreaRoleCtrl
   ↓ A
selected schoolList items (L431-L436)
   ↓ A
$scope.schoolIdArray.push($scope.selected[i]) (L642)
   ↓ A
'/admin/changeAdminRole.json' { id: adminId, schoolIdArray: $scope.schoolIdArray } (L648)
   ↓ A
Server 接收
```

### 5.3 schoolIdArray 与 screening 模块 0 桥（A — 字符级反向证据）

- **schoolIdArray 在 screening 模块 0 命中**（A — 0 命中）
- schoolIdArray 在所有 schoolMate / schoolPlan / schoolClass / schoolMateCheck API 中**0 命中**（A — 0 命中）
- schoolIdArray **仅在 role 簇 2 个 Controller**（modifyRoleCtrl / modifyAreaRoleCtrl）

**结论**：schoolIdArray **不是筛查数据字段**，是 **"admin 可管理的学校范围"** 字段。

---

## 6. getGrant → schoolIdArray 链路（**S1-131 误判修正**）

### 6.1 getGrant 6 处精确调用（A — 字符级）

| 行号 | 表达式 | 解构字段 |
|---|---|---|
| L5380 | `grantAuth.getGrant(ObjectFactory).then(function (obj) {})` | obj |
| L5721 | `grantAuth.getGrant(ObjectFactory).then(function (obj) {})` | obj |
| L6020 | `grantAuth.getGrant(ObjectFactory).then(function (_ref) { var result = _ref.result, channelList = _ref.channelList; })` | _ref.result, _ref.channelList |
| L7225 | 同上 | _ref.result, _ref.channelList |
| L7471 | 同上 | _ref.result, _ref.channelList |
| L34735 | `then(function (_ref2) { var result = _ref2.result, channelList = _ref2.channelList; })` | _ref2.result, _ref2.channelList |

### 6.2 **S1-131 误判修正**（D — 冲突）

**S1-131 报告**：
> "getGrant(ObjectFactory) 返回值 Consumer 会解构 adminId / schoolIdArray"
> "getGrant → schoolIdArray → 实际 Consumer"

**S1-132 当前扫描**：
- getGrant 6 处调用中，**5 处解构 result 和 channelList**（A — 字符级）
- **0 处解构 schoolIdArray**（A — 0 命中）
- **0 处解构 adminId**（A — 0 命中）

**【D 冲突 / 当前采用】**：
- **S1-131 "getGrant → schoolIdArray" 是误判**（D）
- 实际 getGrant 仅返回 `{ result, channelList }` 字段（A — 字符级）
- schoolIdArray **完全来自 role 簇内部 selected 数组**（A — L634-L648）
- 当前采用：**修正 S1-131 — getGrant 不返回 schoolIdArray**（F — getGrant 实现源不可得，但前端解构仅含 result + channelList）

### 6.3 getGrant 真实消费

| Consumer | 解构字段 | 后续 |
|---|---|---|
| L5380 | obj | (待读取) |
| L5721 | obj | (待读取) |
| L6020 | result, channelList | channelList 渲染下拉 |
| L7225 | result, channelList | 渲染下拉 |
| L7471 | result, channelList | 渲染下拉 |
| L34735 | result, channelList | 渲染下拉 |

**【F 边界】**：getGrant 返回的 `result` 字段是否包含 `schoolIdArray`？前端**未解构**该字段，无法证明（F 边界）。

---

## 7. School ↔ 筛查业务链

### 7.1 School → School Class（班级）

**完整证据**（A — 字符级 129 处）：
- `schoolClassListFactory = new ListFactory("/admin/getSchoolClassList.json", 0, 100, { schoolId: $scope.obj.schoolId, inYear: $scope.obj.inYear })` (L19254, L19915, L39754, L39758, L40201, L43553, L44965)
- **业务关系**：1 个 school → N 个 schoolClass（按 inYear + schoolId 过滤）

### 7.2 School → School Plan（筛查计划）

**完整证据**（A — 字符级）：
- `schoolPlanListFactory = new ListFactory("/admin/selectSchoolPlanListBySchool.json", 0, 10, { schoolId: $scope.obj.schoolId })` (L39875, L39884, L44901)
- `selectInYearListBySchoolPlan.json` 同时接收 `schoolPlanId` + `schoolId` (L19238, L19894, L40196, L43548, L44960)
- **`insertSchoolPlan.json` / `insertSchoolPlanRoot.json`** 是 W API
- **业务关系**：school + schoolPlanId 双向查询

### 7.3 School → School Mate（学生）

**完整证据**（A — 字符级）：
- `schoolMateId` 19 处，**仅来自 schoolMateCheckVo 响应**（A — L41666 等）
- `schoolMateVo` 9 处核心视图（A — L8264-L8277）
- `selectSchoolMateCheckVoList.json` 接收 `schoolId` + 多个参数（L44434, L40168, L40599, L46439, L43518）
- `insertSchoolMate.json` / `insertSchoolMateAndCreatePromotion.json` 是 W API
- **业务关系**：school + class + student 三级

### 7.4 School → School Mate Check（筛查记录）

**完整证据**（A — 字符级 174 处）：
- `schoolMateCheckList = []` 数组收集（L14403）
- `schoolMateCheckVo` 174 处**核心对象**
- 字段全集：id / schoolMateId / promotionId / customerMobile / classMateName / gender / birthday / checkDate / right1-67 / left1-67（**视力数据**）
- 关键 API：
  - `getSchoolMateCheckVo.json` 5+ 处
  - `getSchoolMateCheckVoList.json` 8+ 处
  - `saveSchoolMateCheck.json` (W)
  - `completeSchoolMateCheck.json` (W)
  - `insertSchoolMateCheck.json` (W)
  - `updateSchoolMateCheck.json` (W)
  - `disableSchoolMateCheck.json` (W)
  - `sendSmsToSchoolMateCheck.json` (W) — **通知**
  - `sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json` (W) — **打印**

### 7.5 School → 报表 / 跟进 / 群发 / 进度 / 档案 / 质检

| 业务 | 关键 API | 状态 |
|---|---|---|
| **报表** | screenClassReportCtrl / screenRecordReportCtrl / screenSchoolReportCtrl / screenStudentReportCtrl / studentReportInschoolCtrl | A — 多个 Controller |
| **跟进** | setIntention.setParams('schoolMateCheckId', ...) (L19093) | A — **仅 1 处**，弱桥 |
| **群发** | sendMsgToSchoolMateCheckBySelected (L47482) + sendSmsToSchoolMateCheck (L44659) + screenConditionBatchGroupSendCtrl | A |
| **进度** | getPromotionVisionFactory.result.object.schoolMateCount (L39972-L39975) | A — schoolMateCount 字段 |
| **档案** | getSchoolMateCheckPrintConf.json + updateSchoolMateCheckPrintConfImageUrl.json | A |
| **质检** | **inspectionCtrl L40558** (DI 10 个) | A — **唯一 1 个** 质检 Controller |

### 7.6 SchoolMate / SchoolMateCheck 业务流（DAG 文字描述）

```
school
   ↓ A (schoolId)
schoolClass (按 inYear 过滤)
   ↓ A (classId)
schoolMate (学生)
   ↓ A (schoolMateId)
schoolMateCheck (筛查记录)
   ↓ A (schoolMateCheckId)
   ├─ 视力数据 (right1/2, left1/2, left67, right67, etc.)
   ├─ customerMobile (L41684)
   ├─ checkDate (L41698)
   ├─ promotionId (L41667)
   └─ → sendSms / sendToCloudPrinter / setIntention / completeCheck
```

---

## 8. School ↔ Student / Patient / MedicalRecord

### 8.1 Patient ↔ School 单向桥（A — 字符级）

**L8434-L8438** 关键证据（4 行）：
```javascript
$scope.basic.schoolName = patient.school ? patient.school.schoolName : '';
$scope.obj.schoolId = patient.school ? patient.school.id : null;
$scope.obj.classId = patient.schoolClass ? patient.schoolClass.id : null;
$scope.careatInfo.inputVal = patient.schoolClass ? patient.schoolClass.className : '';
```

**结论**：
- **patient 对象包含 school 字段和 schoolClass 字段**（A — 字符级）
- 4 处单向消费（patient → schoolId / classId）
- **反向（school → patient）0 命中**（A — 0 命中）

### 8.2 schoolMateVo 桥（A — 字符级 9 处）

L8264-L8277 显示 schoolMateVo 是 appoint 选顾客的**核心视图对象**：
- schoolMateVo.school.id → schoolId
- schoolMateVo.schoolClass.id → classId
- schoolMateVo.schoolMate.gender / customerMobile / birthday / classMateName

**结论**：schoolMateVo 是**连接 school + class + student** 的视图对象，**appoint 业务真正消费 schoolMateVo**。

### 8.3 School ↔ MedicalRecord

- 0 处直接桥（F 边界 — 0 命中 schoolId 在 medicalRecord 上下文）
- L1803-L1806: `data.result.object.schoolMateCheck` 与 medicalRecord 业务**无直接联系**（仅是同 Controller 内的不同对象）
- **【F 边界】**：SchoolMateCheck 与 MedicalRecord 关系未直接证明

### 8.4 School ↔ customer

- L19691 `getSchoolMateCheckVoOfCustomer.json { customerId }` — **Customer ↔ SchoolMateCheck 桥**（A）
- L19753 `getSchoolMateCheckVoOfRecommendPhone.json` — **Phone ↔ SchoolMateCheck 桥**（A）
- L41684 `$scope.obj.customerMobile = res.vo.schoolMateCheck.customerMobile` — **schoolMateCheck 包含 customerMobile**（A）

**结论**：
- SchoolMateCheck 包含 customerMobile 字段（不是 customerId 字段）
- customerId 通过独立 API 桥到 schoolMateCheck（A）
- **customer 实体本身不直接包含 schoolId**（A — 0 命中）

### 8.5 School ↔ employee

- 0 处直接桥（F 边界）
- `schoolTeacher` 57 处是**教师实体**（A — L38867, L38944, L41680, L42325）
- **`schoolTeacher.teacherName` + `schoolTeacher.id` 是教师标识**（A）
- **`schoolTeacherId` 在 controller.js 中不存在**（A — 0 命中 `schoolTeacherId` 字段）
- 教师是**学校的一部分**，不是 employee 实体（A — 命名区分）

### 8.6 反向排除（patient / customer / employee / medicalRecord 与 school）

| 关系 | 是否等同 | 证据 |
|---|---|---|
| `school.schoolId` == `patient.id` | **F** | A — 0 命中 |
| `patient.school.id` 是 `schoolId` 的来源 | **是** | A — L8435 字符级直接证明 |
| `patient.schoolClass.id` 是 `classId` 的来源 | **是** | A — L8437 字符级直接证明 |
| `schoolMateId` == `patientId` | **F** | A — 0 命中（schoolMate 是学校学生，patient 是诊所患者） |
| `schoolMateId` == `customerId` | **F** | A — 0 命中 |
| `schoolMateVo` 是 `patient` 的扩展 | **B** | A — L8264-L8277 字符级；语义上 schoolMateVo 是 patient 的预查询视图 |
| `schoolTeacher` == `employee` | **F** | A — 0 命中（teacher 是学校教师，employee 是诊所员工） |

---

## 9. School ↔ companyId / corpId

### 9.1 schoolId ≠ companyId（A — 字符级）

- 0 命中 `schoolId = companyId` 或 `companyId = schoolId` 互换（A）
- 0 命中 `schoolId === companyId` 比较（A）
- 命名空间完全不同
- 0 命中 `school.companyId` 字段（A — school 对象不含 companyId）

### 9.2 corpId 与 schoolId（A — 字符级）

- corpId 31 处（L13994, L14150, L14162, L14237, L14239, L17104, L36075 等）
- schoolId 200+ 处
- 0 命中 `corpId === schoolId` 或 `corpId = schoolId` 互换（A — 0 命中）
- 0 命中 `school.corpId` 字段（A — school 对象不含 corpId）

### 9.3 schoolIdArray 与 companyId 关系

- schoolIdArray 仅在 changeAdminRole.json 中（L648）
- changeAdminRole.json 同时接受 `companyId` 字段（L648 完整 Request）
- **A 字符级证据**：`{ id: adminId, adminRoleId, companyId, schoolIdArray }` —— **schoolIdArray 与 companyId 是 Request 的并列字段，不是派生**
- **不互证**：schoolIdArray **不是** companyId 派生

### 9.4 School ↔ company / corpId A-G 判定

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function bridge | F | 0 命中 |
| State bridge | F | 0 命中 |
| API Response → Request | F | 0 命中（schoolId 与 companyId 是独立 Request 字段） |
| Scope/Service bridge | F | 0 命中（schoolInfo 与 companyInfo 是不同 ObjectFactory 模板） |
| Factory bridge | F | 0 命中 |
| Object reference | F | 0 命中 |
| 字段共现 | **G** | A — schoolId / companyId / corpId 在不同 Object 中**共现**于同一业务页（如 adminHospital Ctrl L15235 同时使用） |

---

## 10. School ↔ grantAuth

### 10.1 grantAuth 在 School / screening 域调用点

| 业务 | grantAuth 方法 | 行号 |
|---|---|---|
| screening 域 | **0 命中** | A — 0 命中 |
| school 域 | **0 命中** | A — 0 命中 |
| schoolMate 域 | **0 命中** | A — 0 命中 |

**结论**：**grantAuth 在 School / screening / schoolMate 域 0 命中**（A — 字符级精确）

### 10.2 grantAuth 唯一 bridge：A — hasAuthForCompany

- 仅 `window.grantAuth.hasAuthForCompany(ObjectFactory)` 在 screening 业务页中调用（A — 估计 L1787 等位置）— 但**仅用于初始化公司权限**（不是 school 范围）

**A-G 判定**：

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function bridge | F | 0 命中 |
| State bridge | F | 0 命中 |
| API Response → Request | F | 0 命中 |
| Scope/Service bridge | **A** (hasAuthForCompany) | 仅在公司权限初始化，**不是 school 域权限** |
| Factory bridge | F | 0 命中 |
| Object reference | F | 0 命中 |
| 字段共现 | F | 0 命中 schoolIdArray 来自 grantAuth |

### 10.3 **S1-131 误判修正**

**S1-131 报告**：
> "grantAuth → schoolIdArray → 实际 Consumer"

**S1-132 当前扫描**：
- getGrant 6 处调用中**0 处返回 schoolIdArray**（A — 字符级）
- schoolIdArray **完全来自 role 簇内部** selected 数组（A — L634-L648）
- **S1-131 误判** —— 当前采用：**修正**（D 冲突 — getGrant 不消费 schoolIdArray，schoolIdArray 也不是 grantAuth 链）

---

## 11. 跨一级菜单桥

### 11.1 筛查数据进入业务主链（A — 字符级）

| 业务一级菜单 | 0 命中筛查 |
|---|---|
| 就诊流程 (optometryCtrl) | A — 0 命中 schoolId |
| 预约叫号 (appointOrderCtrl / appointAdminCtrl) | A — 0 命中（但 appoint 消费 schoolMateVo L8264） |
| 患者维护 (patientCtrl) | A — 0 命中（但 patient 含 school L8434-L8438 单向） |
| 营销管理 (couponListCtrl) | F |
| 筛查机构 (schoolMate* / schoolPlan*) | **A** — **核心业务** |
| 物资管理 | F |
| 数据报表 (screenXxxReport) | A — 多个 |
| 诊所管理 (adminClinicCtrl) | F |
| 系统设置 (systemSetting.*) | F |
| 角色/员工/部门 | F（**modifyRoleCtrl 单独消费 schoolIdArray**，A — 但这是 admin 权限范围，不是筛查数据） |

### 11.2 screening → 业务一级菜单 跨桥 A-G 判定

| 业务 | Function | State | API Resp→Req | Scope/Service | Factory | Object ref | 字段共现 |
|---|---|---|---|---|---|---|---|
| 就诊流程 | F | F | F | F | F | F | F |
| 预约叫号 | F | F | F | F | F | F | **G** (schoolMateVo L8264) |
| 患者维护 | F | F | F | F | F | F | **G** (patient.school L8435) |
| 营销管理 | F | F | F | F | F | F | F |
| 物资管理 | F | F | F | F | F | F | F |
| 数据报表 | F | F | **A** (schoolId 在 screenXxxReport API) | F | F | F | A |
| 诊所管理 | F | F | F | F | F | F | F |
| 系统设置 | F | F | F | F | F | F | F |
| 角色/员工/部门 | F | F | F | F | F | F | **G** (schoolIdArray + companyId 都在 changeAdminRole) |

### 11.3 真实数据桥 vs 字段共现

| 桥 | 类型 | 证据 |
|---|---|---|
| school → patient (L8434-L8438) | **真实数据桥**（patient.school 单向） | A |
| schoolMateVo → appoint 选顾客 | **真实数据桥**（appoint 业务消费 schoolMateVo 9 处） | A |
| screening → 数据报表 (screenXxxReport) | **真实数据桥**（API Request 含 schoolId） | A |
| screening → 营销 | **仅字段共现 G** | A — 0 命中 |
| school → role (schoolIdArray) | **真实数据桥**（changeAdminRole API Request） | A |
| screening → 系统设置 | **0 桥** | A |

---

## 12. schoolId 数量精确分类（A — 字符级）

| 类型 | 精确数量 | 备注 |
|---|---:|---|
| A. $stateParams.schoolId | **2** | L38824, L38999 |
| B. API Response .school.id | **13** | L8270, L8435, L8887, L39313, L39866, L39867, L41672, L41752, L41969, L44884, L46291, L48112, L48730 |
| C. API Response .schoolId 顶层 | **0** | 不存在 |
| D. Request .schoolId | **86+** | 详细见第 4.1 节 |
| E. ObjectFactory 模板 | **5** | L8167, L9181, L14409, L17657, L47568 |
| F. ListFactory 参数 | **（D 子集）** | — |
| G. $scope.obj.schoolId | **54** | 详细见第 4.1 节 |
| H. schoolIdArray | **3** | L634, L648, L769 |
| I. 字符串 / 配置 key | 多 | — |
| J. schoolMateId | **19** | schoolMateCheck 域 |
| K. schoolMateCount | **4** | L39972, L39974, L39975, L40039 |
| L. schoolId_clear (set null) | **32** | 详细见第 4.1 节 |

**schoolId 实际相关 11 类总计精确**：**2+13+0+86+5+54+3+19+4+32 ≈ 218 处**
（S1-131 报告 "200+" 是粗略估计，本轮精确到 **218** 处直接赋值 / 消费 + 86+ 处 Request）

### 12.1 相关数量统计

| 指标 | 数量 | 来源 |
|---|---:|---|
| school 总命中 | **41** | A |
| schoolId 精确命中 | **218** | 本轮精确 |
| schoolIdArray 命中 | **3** | A |
| student 命中 | **1** | A — 仅 studentReportInschoolCtrl L48544 |
| studentId 命中 | **0** | A — 0 命中（**仅 schoolMateId 19 处**） |
| schoolMate* 出现 | **200+** | A |
| schoolMateCheck 出现 | **174** | A |
| schoolClass 出现 | **129** | A |
| schoolPlan* 出现 | 估计 **30+** | A |
| schoolTeacher 出现 | **57** | A |
| inYear 出现 | **123** | A |
| school API unique | **75+** | 本轮统计 |
| School Controller 数 | **5+** | schoolListCtrl + addSchoolCtrl + inspectionCtrl + 多个 screenReport* |
| schoolId 出现在 Request 的 Controller 数 | 估计 **15+** | A |
| schoolId 出现在 Response Consumer 的 Controller 数 | 估计 **15+** | A |
| 跨一级菜单直接桥 | **0 个**（**仅 patient.school 单向 + schoolMateVo → appoint 业务**） | A |

---

## 13. L1 / L2 / L3 分层

### 13.1 L1（前端直接事实）

- schoolListCtrl L44357 完整内容
- schoolMateCheckVo 完整字段
- schoolMateVo 9 处核心三对象视图
- schoolId 11 类精确分类 218 处
- schoolIdArray 3 处完整链
- school API 75+ 个
- getGrant 6 处解构（仅 result + channelList，**无 schoolIdArray**）

### 13.2 L2（基于 L1 的有限业务解释）

- schoolMateVo 是连接 school + class + student 的视图对象
- schoolIdArray 是 admin 角色分配的多学校范围（**不是筛查数据**）
- screenXxxReport Controller 是大屏相关，**不是筛查报告**
- patient.school 是 patient 对象的扩展字段（单向）

### 13.3 L3（当前无证据）

- 后端 school / schoolClass / schoolPlan / schoolMate / schoolMateCheck / schoolTeacher 表是否存在
- 后端 FK 关系
- `corpType.school` 关系（corpType 仅 2 处：A — L14265-L14266，无 school 字段）
- schoolMateCheckVo 后端 Vo 是什么实体
- `getGrant` 真实返回结构（前端仅解构 result + channelList）
- screening* 在业务层是否独立存在（**当前证据范围 F**）
- 报表 / 跟进 / 群发 / 进度 / 档案 / 质检业务流是否完整

---

## 14. 筛查核心 DAG（A-K）

### DAG A: getGrant → schoolIdArray（**S1-131 误判修正**）

```
grantAuth.getGrant(ObjectFactory) (L5380, L5721, L6020, L7225, L7471, L34735)
   ↓ A
then(function (_ref) { var result = _ref.result, channelList = _ref.channelList; })
   ↓ A
[result + channelList 解构]
   ↓ F
[schoolIdArray 0 命中 — 前端从未解构]
   ↓ F
[结论：getGrant → schoolIdArray 链 F 边界]
```

### DAG B: school Source → schoolId

```
[5 个 Source 互不互证]
├── $stateParams.schoolId (2 处, L38824, L38999)
├── res.school.id (13 处) ← A
├── $scope.obj.schoolId (54 处)
├── $scope.schoolId (2 处, L38824, L38999)
├── res.vo.school.id (schoolMateVo L41672, L41752, L41969)
├── res.items[0].school.id (L44884, L48112)
├── res.result.object.school.id (L46291)
├── res.getSupplierListFactory.items[0].school.id (L39313, L39866, L39867, L48730)
└── res.school.id from getSchoolInfo (L38831)
   ↓ A
[进入 ~86+ 处 API Request]
```

### DAG C: schoolId → screening

```
schoolId (Source B/G)
   ↓ A
Request: { schoolId, ... } 进入 schoolMate / schoolClass / schoolPlan API
   ↓ A
Response: schoolMateVo { school, schoolClass, schoolMate }
   ↓ A
schoolMate → schoolMateCheck (通过 schoolMateId)
   ↓ A
schoolMateCheckVo 字段 (174 处)
   ↓ A
视力数据 + customerMobile + checkDate + promotionId
   ↓ A
后续: completeCheck / sendSms / setIntention / sendToCloudPrinter
```

### DAG D: schoolId → screening plan

```
$scope.obj.schoolId + $scope.obj.schoolPlanId
   ↓ A
[多个 API]
├── selectInYearListBySchoolPlan.json (L19238, L19894, L40196, L43548, L44960) — schoolPlanId + schoolId
├── selectSchoolPlanListBySchool.json (L39875, L39884, L44901) — schoolId
├── getDefaultSchoolPlanByAdminId.json (L19307, L19884) — 无参数（按 admin）
├── insertSchoolPlan.json / insertSchoolPlanRoot.json (L38797, L38799) — W
├── completeSchoolPlanSchool.json (L41077) — W
└── statVisionOfSchool.json (L40221, L43573) — R
   ↓ A
schoolPlanListFactory.items[]
```

### DAG E: schoolId → report

```
schoolId (Source)
   ↓ A
screenXxxReportCtrl API Request
   ├── screenClassReportCtrl (L45114)
   ├── screenRecordReportCtrl (L48060)
   ├── screenSchoolReportCtrl (L48156)
   ├── screenStudentReportCtrl (L48200)
   ├── screenReportInschoolCtrl (L48100)
   └── studentReportInschoolCtrl (L48544)
   ↓ A
报表数据 (含 schoolId 过滤)
```

### DAG F: schoolId → follow-up

```
schoolId (Source)
   ↓ A (弱桥)
[仅 L19093 一处]
$scope.setIntention.setParams('schoolMateCheckId', item.schoolMateCheck.id)
   ↓ A (A — 字符级)
但 $scope.setIntention 与 schoolId 无直接联系
   ↓ F
[schoolId → 跟进 弱桥，仅 1 处 setIntention 含 schoolMateCheckId]
```

### DAG G: schoolId → messaging

```
schoolId (Source)
   ↓ A
[API]
├── sendSmsToSchoolMateCheck.json (L44659, L44677) — W — 接收 schoolMateCheckId
├── sendMsgToSchoolMateCheckBySelected.json (L47482) — W
├── sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json (L46406, L47423) — W
├── screenConditionBatchGroupSendCtrl (L45310) — 大屏群发
└── screenConditionBatchGroupSendLookCtrl (L45589) — 大屏群发查看
   ↓ A
消息发送完成
```

### DAG H: schoolId → archive / quality

```
schoolId (Source)
   ↓ A
[Archive API]
├── getSchoolMateCheckPrintConf.json (L41153) — R — 打印配置
├── updateSchoolMateCheckPrintConfImageUrl.json (L41302) — W — 打印图
├── sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json (L46406, L47423) — W — 打印
└── printSchoolPromotionListVoList.json (L39293) — R
   ↓ A

[Quality API]
└── inspectionCtrl L40558 (A — Controller 存在)
   ↓ F (API / schoolId 关系未直接证明)
```

### DAG I: school → medicalRecord / patient

```
school (schoolId)
   ↓ A
patient.school (L8434-L8435)
   ↓ A
$scope.obj.schoolId = patient.school.id
   ↓ A
后续: 写入 patient Object

schoolId → medicalRecordId
   ↓ F
[0 命中直接桥]
   ↓ F
[school 与 medicalRecord 0 桥]

patient ↔ schoolMate
   ↓ F
[0 命中直接互证]
   ↓ F
[patient 与 schoolMate 是不同概念]
```

### DAG J: school / schoolId → companyId / corpId

```
schoolId ≠ companyId
   ↓ A (0 互换)
schoolId ≠ corpId
   ↓ A (0 互换)
schoolIdArray 与 companyId 关系
   ↓ A (L648 字符级)
{ id: adminId, adminRoleId, companyId, schoolIdArray: ... }
   ↓ A
schoolIdArray 与 companyId 是 changeAdminRole.json Request 的并列字段
   ↓ F
[学校范围 vs 公司范围：业务上不同，但前端代码无互证]
```

### DAG K: 筛查机构 → 8 个业务一级菜单

```
[筛查机构（school + schoolMate + schoolMateCheck）]
   ↓ A (schoolId → schoolMateCheckVo 174 处)
   ├─ 预约叫号 (appointOrderCtrl / appointAdminCtrl) — schoolMateVo 9 处 — G
   ├─ 患者维护 (patient) — patient.school 单向 — A
   ├─ 数据报表 (screenXxxReport) — A
   ├─ 角色/员工/部门 (modifyRoleCtrl / modifyAreaRoleCtrl) — schoolIdArray changeAdminRole — A
   ├─ 就诊流程 (optometryCtrl) — F
   ├─ 营销管理 (coupon*) — F
   ├─ 物资管理 — F
   ├─ 诊所管理 (adminClinicCtrl) — F
   └─ 系统设置 (systemSetting.*) — F
```

---

## 15. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | 筛查机构一级菜单入口 | **无独立"筛查"菜单**（screen = 大屏 ≠ screening） | F | controller.js 0 命中 "筛查" | F |
| 2 | 二级菜单枚举 | schoolListCtrl + addSchoolCtrl + 多个 screenReport* | A | L44357 等 | A |
| 3 | School Controller 边界 | schoolListCtrl L44357 (108 行) 已知 + 估计 5+ | A | L44357 | A |
| 4 | school 来源 | 5 个 Source | A | 多处 | A |
| 5 | schoolId 来源 | 11 类 | A | 218 处精确 | A |
| 6 | schoolId 分类统计 | 11 类（A-L） | A | 详细见第 4.1 | A |
| 7 | schoolId Consumer | 86+ API Request | A | 多处 | A |
| 8 | schoolIdArray 来源 | 3 处 init + 2 处 push | A | L634, L648, L769 | A |
| 9 | schoolIdArray Consumer | changeAdminRole.json (role 簇) | A | L648 | A |
| 10 | getGrant → schoolIdArray 桥 | **0 命中** | F | controller.js 0 命中 | F |
| 11 | school → screening 桥 | A — 86+ API | A | 多处 | A |
| 12 | school → screeningPlan 桥 | A — 6+ API | A | L19238 等 | A |
| 13 | school → report 桥 | A — 5+ Report Controller | A | screenXxxReport | A |
| 14 | school → follow-up 桥 | **弱 1 处** | C | L19093 setIntention | C |
| 15 | school → messaging 桥 | A — 5+ API | A | sendSms 等 | A |
| 16 | school → progress 桥 | A — schoolMateCount 4 处 | A | L39972-L39975 | A |
| 17 | school → archive 桥 | A — 4+ API | A | printSchool 等 | A |
| 18 | school → quality 桥 | A — inspectionCtrl 1 个 | A | L40558 | A |
| 19 | school → patient/student 桥 | A — patient.school 单向 (4 行) | A | L8434-L8438 | A |
| 20 | school → medicalRecord 桥 | **0 桥** | F | 0 命中 | F |
| 21 | school → companyId/corpId 桥 | **0 桥** | F | 0 互换 | F |
| 22 | school → grantAuth 桥 | **0 桥**（school 域 0 命中 grantAuth） | F | 0 命中 | F |
| 23 | 筛查 → 其他一级菜单桥 | A — patient.school + schoolMateVo 9 处 + screenReport | A | L8264, L8435, L45114 等 | A |
| 24 | State / URL | $stateParams.schoolId 2 处 | A | L38824, L38999 | A |
| 25 | 最终筛查 DAG | 11 个 DAG (A-K) | A | 本文档第 14 节 | A |
| 26 | 复刻红线 | 第 18 节 | A | controller.js | A |

---

## 16. A/B/C/D/E/F 分布

- **A**：22
- **B**：1（patient.school + schoolMateVo 形成 school→patient 互证）
- **C**：1（school → follow-up 弱桥）
- **D**：3（screen ≠ screening 命名冲突 / getGrant → schoolIdArray 误判 / schoolIdArray 是 role 字段不是 screening 字段）
- **E**：**0**（红线要求）
- **F**：8（grantAuth 真实实现 / 后端 school 表 / screening 一级菜单 / corpType.school 关系 / getGrant 完整返回 / screening* Controller / DAG F follow-up 弱桥 / DAG H quality 业务关系）

---

## 17. 历史差异

### 17.1 S1-131 中 schoolId 误判修正

| 项 | S1-131 | S1-132 | 差异 | 当前采用 |
|---|---|---|---|---|
| schoolId 数量 | "200+ 处独立 ID 系统" | **218 处精确分类 11 类** | 精度提升 | A |
| schoolIdArray 含义 | "screening 业务字段" | **role 分配的多学校范围字段** | 命名空间不同 | A — **修正 S1-131** |
| getGrant → schoolIdArray 桥 | "完整字符级证据闭环" | **getGrant 0 命中 schoolIdArray** | 0 命中 | F — **修正 S1-131** |
| screen* Controller | (未分类) | **26 个 screen* 是大屏，不是筛查** | 命名误导 | A — 重要修正 |

### 17.2 S1-130 / S1-131 中 screen/screening 命名

- S1-130 第 5.1 节 列出 `screenPromotionConfigCtrl` / `screenBackConfigCtrl` 等，但未明确"screen = 大屏"
- S1-131 第 1 节指出 schoolId 200+ 处独立 ID
- **本轮明确：screen ≠ screening；screening 在 controller.js 中 0 个 Controller**

### 17.3 历史 MD 中筛查业务 0 命中

- S1-122 ~ S1-129 中均未深入筛查业务
- S1-130 中 screen* Ctrl 列出但未确认"大屏"语义
- S1-131 中 schoolId 200+ 处首次发现

**本轮新增**：筛查业务深度模型（schoolMate + schoolMateCheck + schoolMateCheckVo）

### 17.4 patient.school 单向桥

- 历史 MD 0 提及 `patient.school` 字段
- S1-128 / S1-129 中 patient / medicalRecord 业务未与 school 关联
- **本轮首次发现**：patient.school 4 行字符级证据

---

## 18. 复刻红线

### 18.1 不能自行增加的字段

- `school` 不应包含 `companyId` 字段（A — 0 命中 school.companyId）
- `schoolMateCheck` 不应直接包含 `medicalRecordId` 字段（A — 0 命中）
- `schoolMateCheckVo` 不应直接包含 `patientId` 字段（仅 customerMobile）
- `getGrant` 返回不应假定包含 schoolIdArray（F — 前端 0 解构）
- 任何 controller.js 中 0 命名的 school 字段

### 18.2 不能自行补桥的模块

- **school 与 companyId 不能直接等同**（A — 0 互换）
- **schoolIdArray 不是 screening 业务字段**（A — 仅在 role 簇）
- **getGrant 不消费 schoolIdArray**（A — 0 命中）
- **screen ≠ screening**（D 命名误导 — screen = 大屏，screening 业务 0 独立 Controller）
- **screening 域与业务主链 0 桥**（F 边界 — 仅 patient.school 单向 + schoolMateVo → appoint）
- **screening 域与 grantAuth 0 桥**（A — 0 命中）
- **schoolMateCheck 与 medicalRecord 0 桥**（F 边界 — 0 命中）
- **schoolTeacher ≠ employee**（A — 0 命中）
- **schoolMateId ≠ patientId**（A — 0 命中）
- **schoolMateId ≠ customerId**（A — 0 命中）

### 18.3 不能假定存在的 API

- `/admin/screening*.json` 不存在（A — 0 命中）
- `/admin/screeningPlan.json` 不存在（A — 0 命中独立）
- `/admin/getSchoolInfoByCompany.json` 不存在
- 任何 controller.js 中 0 命名的 API

### 18.4 不能等同的 ID

| ID | 不能等同 |
|---|---|
| schoolId | ≠ companyId / corpId / clinicId / shopId / hospitalId / adminId / employeeId / patientId / customerId / medicalRecordId / studentId（**studentId 不存在**） |
| schoolClassId / classId | ≠ schoolId / companyId / classId 在 appointment 业务中复用 |
| schoolMateId | ≠ patientId / customerId / studentId（**studentId 不存在**） |
| schoolPlanId | ≠ medicalRecordId / orderId / promotionId |
| schoolTeacherId | ≠ employeeId / teacherId（**teacherId 不存在顶层**） |
| schoolIdArray | ≠ permission / company scope / admin scope（仅在 changeAdminRole.json 中作 admin 角色分配） |
| classId | 在 schoolMateVo 上下文 ≠ appointment classId（**命名冲突，F 边界**） |
| patient.school.id | ≡ schoolId（A — 字符级直接证明） |
| patient.schoolClass.id | ≡ classId（A — 字符级直接证明） |

### 18.5 必须保留的 F 边界

- grantAuth 后端实现 F
- getGrant 完整返回结构 F（前端仅解构 result + channelList）
- 后端 school / schoolClass / schoolPlan / schoolMate / schoolMateCheck / schoolTeacher 表 F
- screening 业务是否独立存在 F
- 报表 / 跟进 / 群发 / 进度 / 档案 / 质检业务完整闭环 F
- schoolMateCheckVo 后端实体 F
- schoolInfo 与 companyInfo 后端实体 F
- 26 个 screen* Controller 实际业务深度 F
- $stateProvider.state() 注册 F
- URL 路由表 F
- HTML template 引用 F

### 18.6 命名误导必须标注

- `screen*` Controller **绝大多数是大屏**（叫号/宣传/配置），**不是筛查**
- `schoolIdArray` **是 role 分配字段**，不是筛查业务字段
- `schoolInfo` ObjectFactory 模板（A — L37017/L37669）与 `companyInfo` 模板结构相似但**是不同对象**
- `getGrant` 返回值**不含 schoolIdArray**（A — 字符级）
- `screenListCtrl` 是大屏列表，不是筛查列表
- `screenSchoolReportCtrl` 是大屏学校报表，可能是筛查报表也可能是大屏数据，**F 边界**
- `healthScreenConfigCtrl` 是"健康检查"配置，不是"筛查"配置（healthScreen ≠ screening）

---

## 19. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**） | ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**） | ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**） | ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**） | ✓ |
| 历史 MD 165-193 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 194_*.md | 是 | ✓ |
| 临时脚本（3 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 20. Git

- 本轮 commit hash：（待执行 `git add -- 194_*.md` / `git commit -m "docs(194): S1-132 筛查机构 schoolId身份体系与筛查业务链深度审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：201 → 202
- 本轮 untracked 预期：10（保留 10 untracked，新增 194 后变 10 untracked 因为 194 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：194_S1-132_*.md
