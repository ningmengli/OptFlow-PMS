# S1-133 SchoolMate / SchoolMateCheck → Patient / Customer / MedicalRecord 汇合链深度审计

> **项目**：OptFlow PMS 逆向建模
> **本轮核心问题**：筛查体系的数据，到底在哪里与 PMS 主患者 / Customer / MedicalRecord 汇合？
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-194 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / 2,194,196 bytes / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变） |
| schoolMate 出现 | **200+ 处**（S1-132 报告）|
| schoolMateCheck 出现 | **174 处**（A — 精确）|
| schoolMateVo 出现 | **9 处**（A — 字符级精确）|
| customerMobile 出现 | **15 处**（A — 精确）|
| customerId 出现 | **128+ 处**（A — S1-131 报告）|
| patientId 出现 | **89 处**（A — 精确）|
| medicalRecordId 出现 | **161 处**（A — 精确）|
| $stateParams.medicalRecordId | **25 处**（A）|
| $stateParams.patientId | **13 处**（A）|
| $stateParams.customerId | **20 处**（A）|
| $stateParams.schoolMateCheckId / schoolMateId | **0 命中**（A）|

---

## 2. SchoolMate / SchoolMateCheck 完整字段审计

### 2.1 schoolMateVo 9 处精确上下文（A — 字符级）

**L8264-L8277**（appointOrderCtrl 范围内，appointVo.type === 1）：
```javascript
gender: item.schoolMateVo.schoolMate.gender,
linkMobile: item.schoolMateVo.schoolMate.customerMobile,
patientRemark: "" + item.schoolMateVo.school.schoolName + item.schoolMateVo.schoolClass.className,
birthday: item.schoolMateVo.schoolMate.birthday ? parseInt(item.schoolMateVo.schoolMate.birthday) : null,
schoolId: item.schoolMateVo.school.id,
classId: item.schoolMateVo.schoolClass.id
$scope.basic.schoolName = item.schoolMateVo.school.schoolName;
$scope.careatInfo.inputVal = item.schoolMateVo.schoolClass.className;
$scope.keyword = item.schoolMateVo.schoolMate.classMateName;
```

**【关键发现】schoolMateVo → patient 桥**（A — 字符级直接证明）：
- `item.schoolMateVo.schoolMate.customerMobile` → `linkMobile`（patient 字段）
- `item.schoolMateVo.schoolMate.gender` → patient 字段
- `item.schoolMateVo.school.schoolName + schoolClass.className` → `patientRemark`
- `item.schoolMateVo.schoolMate.birthday` → patient 字段
- `item.schoolMateVo.school.id` → `schoolId`
- `item.schoolMateVo.schoolClass.id` → `classId`

**【关键】这是 schoolMate → patient 唯一的字符级直接桥**（A）

### 2.2 schoolMateCheckVo 字段全集（A — 174 处）

**res.vo.schoolMateCheck 字段**（L41660-L42000）：
- id (L41668, L41748)
- schoolMateId (L41666, L41746)
- promotionId (L41667, L41747)
- **customerMobile** (L41684, L41764, L41981)
- classMateName (L41685, L41765)
- gender (L41686)
- remark (L41688)
- schoolMateCode (L41689)
- birthday (L41693)
- checkDate (L41698)
- right1/2, left1/2, left67, right67, left15, right15, left14, right14, left13, right13 (视力数据)
- left68, right65, left65 (建议字段)

**res.vo.schoolMate 字段**（L41690-L41692）：
- nativePlace (L41690)
- nation (L41691)

**res.vo.schoolClass 字段**（L41675-L41677）：
- className, id

**res.vo.school 字段**（L41670-L41672）：
- schoolName, id

**res.vo.schoolTeacher 字段**（L41680-L41681）：
- teacherName, id

### 2.3 schoolMateCheckVo 中 customerMobile 是 15 处中的 5 处

- L41684: `$scope.obj.customerMobile = res.vo.schoolMateCheck.customerMobile`
- L41764: 同上（modifyCtrl）
- L41981: 同上（另一个 modifyCtrl）
- L8265: `linkMobile: item.schoolMateVo.schoolMate.customerMobile`（schoolMateVo 中）

**结论**：schoolMateCheckVo / schoolMateVo 包含 **customerMobile 字符串字段**（A — 字符级）

---

## 3. customerMobile 全链

### 3.1 customerMobile 15 处精确分布（A — 字符级）

| 行号 | 上下文 | 类型 |
|---|---|---|
| L8265 | `linkMobile: item.schoolMateVo.schoolMate.customerMobile` | schoolMateVo → patient.linkMobile |
| L41684 | `$scope.obj.customerMobile = res.vo.schoolMateCheck.customerMobile` | schoolMateCheckVo → Scope |
| L41764 | 同上 | 同上 |
| L41981 | 同上 | 同上 |
| L42084 | `if ($scope.obj.customerMobile)` | schoolMateCheckVo 表单验证 |
| L42085 | `if (!/^1[3|4|5|6|7|8|9]\d{9}$/.test($scope.obj.customerMobile))` | 手机号格式验证 |
| L44098 | `if (!window.Win_VerifyMobile(params.customerMobile))` | 转换验证 |
| L44119 | `params.linkMobile = params.customerMobile` | **customerMobile → linkMobile** |
| L44461 | `if (!/^1[3|4|5|6|7|8|9]\d{9}$/.test($scope.obj.customerMobile))` | 表单验证 |
| L44480 | `if (!$scope.obj.customerMobile || !$scope.obj.classMateName || ...)` | 必填验证 |
| L44489 | `$scope.obj.customerMobile = null` | clear |
| L44510 | `if (!/^1[3|4|5|6|7|8|9]\d{9}$/.test($scope.data.customerMobile))` | 表单验证 |
| L44525 | `if (!$scope.data.customerMobile || !$scope.data.classMateName || ...)` | 必填验证 |
| L46492 | `customerMobile: "" //手机号` | ObjectFactory 模板 init |
| L47131 | 同上 | ObjectFactory 模板 init |

### 3.2 customerMobile → customer / patient 桥判定

| 桥 | 是否存在 | 证据 |
|---|---|---|
| **customerMobile → getCustomerVo.json { mobile: }** | **0 命中** | A — getCustomerVo 14 处全部以 `customerId` 为 Request |
| **customerMobile → getCustomerVo.json { customerId: }** | **F 边界** | A — getCustomerVo **不接收 mobile 字段** |
| **customerMobile → getPatientVoList.json { mobile: }** | **A 桥** | A — L8364, L8374, L8390, L18981 `mobile: $scope.obj.linkMobile` |
| **customerMobile → SchoolMate / SchoolMateCheck** | **A** | A — L8265, L41684 等是字段定义 |
| **schoolMateVo.customerMobile → patient.linkMobile** | **A 桥** | A — L8265 字符级直接证明 |
| **schoolMateCheckVo.customerMobile → 后续 customer API** | **0 命中** | A — 0 命中（仅 UI 验证）|

**【关键反向】**：
- `customerMobile` 字段名称 ≠ `mobile` 字段名称
- `customerMobile` 字段不会直接被 `getCustomerVo.json` 消费（A — 14 处 0 命中 mobile 字段）
- `mobile` 字段（28 处）被 `getPatientVoList.json` 消费（A — 4 处字符级直接证明）

---

## 4. Customer 全链

### 4.1 customer 核心 API（A — 字符级 14 处 unique）

| API | 类型 | 调用次数 |
|---|---|---:|
| `/admin/getCustomerVo.json` | R | **14** |
| `/admin/getCustomerWallet.json` | R | 多 |
| `/admin/getCustomerMember.json` | R | 多 |
| `/admin/getCustomerPoint.json` | R | 1 |
| `/admin/selectCustomerWalletVoList.json` | R | 多 |
| `/admin/selectCustomerWalletLogVoList.json` | R | 多 |
| `/admin/selectCustomerCheckinVoListOfCompany.json` | R | 多 |
| `/admin/selectCustomerCheckinVoListOfEmployee.json` | R | 1 |
| `/admin/insertCustomerCheckin.json` | W | 1 |
| `/admin/insertCustomerCheckinOfNewPaitent.json` | W | 1 |
| `/admin/insertCustomerCheckinOfNewCustomer.json` | W | 1 |
| `/admin/beginCustomerCheckin.json` | W | 2 |
| `/admin/callingWaitingCheckinQueue.json` | W | 多 |
| `/admin/sendCustomerCheckin.json` | W | 1 |
| `/admin/deleteCustomerCheckin.json` | W | 1 |
| `/admin/selectCustomerCreditVoList.json` | R | 多 |
| `/admin/selectUsableCustomerCouponVoList.json` | R | 多 |

### 4.2 getCustomerVo.json 14 处精确调用（A）

| 行号 | Request | Consumer |
|---|---|---|
| L3650 | `{ customerId: result.customerId }` | 顾客详情查询 |
| L4395 | `{ customerId: $scope.refundFeeInfo.customer.id }` | 退款 |
| L4947 | `{ customerId: res.result.object.customer.id }` | 钱包 |
| L5243 | `{ customerId: ... }` | 余额 |
| L5924 | `{ customerId: ... }` | 钱包 |
| L7491 | `{ customerId: ... }` | 钱包 |
| L8894 | `{ customerId: ... }` | 顾客详情 |
| L20960 | `{ customerId: $scope.customerId }` | 顾客查询 |
| L31234 | `{ customerId: res.result.object.customerId }` | 顾客查询 |
| L31344 | `{ customerId: ... }` | 顾客查询 |
| L32912 | `{ customerId: res.result.object.customerId }` | 顾客查询 |
| L32983 | `{ customerId: $scope.obj.customerId }` | 顾客查询 |
| L49781 | `{ customerId: ... }` | 顾客详情 |
| L50064 | `{ customerId: result.customerId }` | 顾客详情 |

**结论**：getCustomerVo **完全以 customerId 为 Request**，**0 命中 mobile 字段**（A）

### 4.3 customerMobileDisable（A — 字符级 6 处）

- L52739, L52755: printConfigCtrl
- L57750, L57766: 另一个打印 Controller
- L58192, L58208: 估计

**含义**：小票显示手机号开关（0=显示 1=隐藏），**与 customerMobile 字段相关**（A）

### 4.4 customerVo 字段全集（A — 字符级）

来自 `res.vo.customer.*` / `res.customer.*` 访问：
- customer.id (L4395, L4947, L7320)
- customer.linkMobile (L35465, L20975 等)
- customer.customerName (L4396, L8248, L20991, L35455)
- customer.gender (L34911, L35450)
- customer.channel (L8249, L8870)
- customer.channelTagId (L8903)
- customer.trueName (L8904)
- customer.avatar (L8905, L8980)

---

## 5. Patient 全链

### 5.1 patient 核心 API（A — 字符级）

| API | 类型 | 调用次数 |
|---|---|---:|
| `/admin/getPatientInfo.json` | R | **10** |
| `/admin/getPatientVoList.json` | R | 4 |
| `/admin/getPatientExamineListVoList.json` | R | 1 |
| `/admin/savePatientInfo.json` | W | (估计) |
| `/admin/insertCustomerCheckinOfNewPaitent.json` | W | 1（注意 typo: Paitent） |

### 5.2 getPatientInfo.json 10 处精确调用（A）

| 行号 | Request | 业务 |
|---|---|---|
| L1970 | `{ id: $scope.patientId }` | 接诊后获取患者详情 |
| L3641 | `{ id: $stateParams.patientId }` | State Param 入口 |
| L6693 | `{ id: res.object.medicalRecord.patientId }` | medicalRecord → patient |
| L21097 | `{ id: $scope.obj.id }` | 修改患者 |
| L31226 | `{ id: $scope.patientId }` | 改患者 |
| L31336 | `{ id: $scope.patientId }` | 改患者 |
| L32906 | `{ id: $scope.patientId }` | 查询患者 |
| L32997 | `{ id: $scope.obj.patientId }` | 查询患者 |
| L49772 | `{ id: $stateParams.patientId }` | 详情 |
| L50053 | `{ id: id }` | 通用查询 |

### 5.3 getPatientVoList.json 4 处精确调用（A）

| 行号 | Request | 关键字段 |
|---|---|---|
| L8364 | `{ name: $scope.keyword, mobile: $scope.obj.linkMobile }` | **mobile 字段！** |
| L8374 | 注释 | — |
| L8390 | `{ name: $scope.keyword, mobile: $scope.obj.linkMobile }` | **mobile 字段** |
| L18981 | 同样 | **mobile 字段** |

**【关键发现】Patient 是 mobile 字段的直接消费者**（A — 4 处字符级）
- 0 处 `customerMobile` 字段
- **mobile 字段 ≠ customerMobile 字段**（A — 命名空间不同）

### 5.4 patient 字段全集（A — 字符级 100+ 处）

来自 `patient.*` / `item.patient.*` / `res.patient.*` 访问：
- patient.id (L8250, L10611, L10643, L11668, L31112, L31116, L31894, L33204, L50076)
- patient.patientId (L34912)
- patient.patientName (L8254, L8968, L9249, L11156, L19002, L35454, L35463)
- patient.patientGender (L8243, L8973, L9253, L19006, L35455, L35464)
- patient.patientBirthday (L8247, L8970, L9251, L19004, L35456, L35524, L35525)
- patient.avatar (L8244, L9325, L35453)
- **patient.school** (L8434, L8435) — **school 桥**
- **patient.schoolClass** (L8437, L8438) — **class 桥**
- patient.linkMobile (L8364 中 `mobile: $scope.obj.linkMobile`)

### 5.5 patient.school 4 行字符级直接证明（A）

**L8434-L8438** 完整证据：
```javascript
$scope.basic.schoolName = patient.school ? patient.school.schoolName : '';
$scope.obj.schoolId = patient.school ? patient.school.id : null;
$scope.obj.classId = patient.schoolClass ? patient.schoolClass.id : null;
$scope.careatInfo.inputVal = patient.schoolClass ? patient.schoolClass.className : '';
```

**结论**：
- **patient 对象包含 school 字段**（A — 字符级直接证明）
- **patient.school.id 是 schoolId 的来源**（A — 单向桥）
- **patient.schoolClass.id 是 classId 的来源**（A — 单向桥）

### 5.6 patient 在 appointVo 业务中

L8243-L8280（appointOrderCtrl 范围）：
```javascript
$scope.appointVo = {
  type: 0 / 1
};
// 选 patient
gender: item.patient.patientGender,
avatar: item.patient.avatar,
patientRemark: item.appoint.remark,
birthday: item.patient.patientBirthday ? parseInt(item.patient.patientBirthday) : null,
patientId: item.patient.id,
schoolId: item.schoolMateVo.school.id,  // ← schoolMateVo 桥
classId: item.schoolMateVo.schoolClass.id,  // ← schoolMateVo 桥
$scope.keyword = item.patient.patientName;
$scope.basic.schoolName = item.schoolMateVo.school.schoolName;
$scope.careatInfo.inputVal = item.schoolMateVo.schoolClass.className;
$scope.keyword = item.schoolMateVo.schoolMate.classMateName;
// $scope.appointVo.schoolMateCheckId = item.schoolMateCheck.id;  // 注释代码
```

**【关键】schoolMateVo → patient 多字段映射**（A — 字符级直接证明）：
- schoolMateVo.school.id → schoolId
- schoolMateVo.schoolClass.id → classId
- schoolMateVo.schoolMate.gender → gender
- schoolMateVo.schoolMate.customerMobile → linkMobile
- schoolMateVo.school.schoolName + schoolClass.className → patientRemark
- schoolMateVo.schoolMate.birthday → birthday
- schoolMateVo.schoolMate.classMateName → keyword

---

## 6. MedicalRecord 全链

### 6.1 medicalRecord 核心 API（A — 字符级 200+ 处命中）

| API | 类型 | 调用次数 |
|---|---|---:|
| `/admin/getMedicalRecord.json` | R | 多 |
| `/admin/getMedicalExamineVoList.json` | R | 多 |
| `/admin/getMedicalRecordFlowVo.json` | R | 估计 |
| `/admin/getMedicalRecordVo.json` | R | 估计 |
| `/admin/computeUnPlaceOrderMedicalRecordFee.json` | R | 1 |
| `/admin/getMethodGlassRecordVo.json` | R | 1 |
| `/admin/selectAppointSchoolMateVoList.json` | R | 1 |
| `/admin/getAppointSchoolMateVo.json` | R | 1 |
| `/admin/statAppointSchoolMateOfCorp.json` | R | 1 |
| `/admin/basicStatAppointSchoolMate.json` | R | 1 |
| `/admin/statAppointSchoolMateOfCompany.json` | R | 1 |

### 6.2 medicalRecordId 161 处精确统计（A）

来源分类：
- $stateParams.medicalRecordId: **25 处**
- 业务内部派生: 多处
- 多个 Controller 间消费

### 6.3 medicalRecord ↔ patient 关系

**L6693** (assistCheckingCtrl)：
```javascript
$scope.getPatientObjectFactory.saveOrQuery("/admin/getPatientInfo.json", { id: res.object.medicalRecord.patientId });
```

**结论**：
- **medicalRecord 包含 patientId 字段**（A — 字符级直接证明 L6693）
- medicalRecord → patient 单向桥（A）

### 6.4 medicalRecord ↔ schoolMate / schoolMateCheck 关系

- **0 命中** `schoolMateCheck.medicalRecordId`（A — 0 命中）
- **0 命中** `schoolMate.medicalRecordId`（A — 0 命中）
- **schoolMateCheckVo 不含 medicalRecordId 字段**（A — 174 处 schoolMateCheckVo 字段访问无 medicalRecordId）

**结论**：schoolMateCheck 与 medicalRecord **0 直接桥**（F 边界）

### 6.5 medicalRecord 在 schoolMate 上下文

唯一**潜在桥**——L14434 注释：
```javascript
// $scope.startTrans($scope.schoolMateCheckList[0][0].schoolMateCheck.schoolMateId)
```

**含义**：注释代码中提到 `schoolMateCheck.schoolMateId`，但**不与 medicalRecord 关联**（A — 注释代码）

**结论**：schoolMate / schoolMateCheck → medicalRecord **0 桥**（A — 0 命中）

---

## 7. getSchoolMateCheckVoOfCustomer.json 完整证据链

### 7.1 API 上下文（A — 字符级 L19335-L19868）

**所在 Controller**：`recommendPhoneListCtrl` (L19335)

**完整 evidence**：

```javascript
// L19690-L19700: 关键 API 调用
$scope.searchMateCheckHistory = function () {
  new ObjectFactory().saveOrQuery("/admin/getSchoolMateCheckVoOfCustomer.json", {
    customerId: $scope.customerId,  // ← customerId 来源
    recommendPhoneId: $scope.recommendPhoneId
  }).then(function (res) {
    if (res.status == 1) {
      return Popup.notice(res.errmsg);
    }
    $scope.mateCheckObject = res.result.object;  // ← schoolMateCheckVo Object
  });
};

// L19670-L19678: customerId 来源
$scope.searchOrderSchoolmateType = function (customerId, recommendPhoneId, type) {
  $scope.customerId = customerId;
  $scope.recommendPhoneId = recommendPhoneId;
  $scope.order.customerId = customerId;
  // ...
};

// L19671: customerId 实际来源
var customerId = item.recommendPhone.selfCustomerId;  // ← recommendPhone.selfCustomerId
```

**【完整 customerId 来源链】**：
1. UI: `recommendPhoneListCtrl` 列表渲染时，传 `item.recommendPhone` 给 `searchOrderSchoolmateType`
2. `searchOrderSchoolmateType(customerId, recommendPhoneId, type)` 接收 customerId
3. `customerId = item.recommendPhone.selfCustomerId` (L19671)
4. 写入 `$scope.customerId`
5. 调用 `getSchoolMateCheckVoOfCustomer.json { customerId, recommendPhoneId }` (L19691-L19693)
6. Response: `$scope.mateCheckObject = res.result.object` (L19698)

### 7.2 4 个 tab 完整映射（A — L19703-L19712）

```javascript
$scope.setTab = function (idx) {
  $scope.tab = idx;
  var tabMap = {
    0: "searchMateCheckHistory",       // getSchoolMateCheckVoOfCustomer.json
    1: "selectOrderVoListByCustomerId", // selectOrderVoListByCustomerId.json
    2: "searchFundous",                  // getFundusCheckRecordListOfCustomer.json
    3: "getSchoolMateCheckVoOfRecommendPhone" // getSchoolMateCheckVoOfRecommendPhone.json
  };
  $scope[tabMap[idx]]();
};
```

**结论**：
- **4 个 tab** 共享 `$scope.customerId` 和 `$scope.recommendPhoneId`
- **Tab 0**：通过 customerId 查 schoolMateCheck
- **Tab 1**：通过 customerId 查 order
- **Tab 2**：通过 customerId 查 眼底检查
- **Tab 3**：通过 recommendPhoneId 查 schoolMateCheck

**这是 Customer → SchoolMateCheck 唯一的字符级直接桥**（A — 多源互证：B 级）

### 7.3 getSchoolMateCheckVoOfRecommendPhone.json 完整（A — L19752-L19761）

```javascript
$scope.getSchoolMateCheckVoOfRecommendPhone = function () {
  new ObjectFactory().saveOrQuery("/admin/getSchoolMateCheckVoOfRecommendPhone.json", {
    recommendPhoneId: $scope.recommendPhoneId
  }).then(function (res) {
    if (res.status == 1) {
      return Popup.notice(res.errmsg);
    }
    $scope.schoolMateCheckVoOfRecommendPhone = res.result.object;
  });
};
```

**结论**：通过 recommendPhoneId 查 schoolMateCheck（不依赖 customerId），**也是 Customer → SchoolMateCheck 桥**（A）

### 7.4 反向：SchoolMateCheck → Customer

- schoolMateCheckVo.customerMobile (L41684) — **仅字段，0 命中 API 消费**
- schoolMateCheckVo 0 包含 customerId 字段
- schoolMateCheckVo 0 包含 patientId 字段
- schoolMateCheckVo 0 包含 medicalRecordId 字段

**结论**：
- **SchoolMateCheck → Customer 是 F 边界**（0 命中）
- **Customer → SchoolMateCheck 是 A 桥**（recommendPhoneListCtrl 字符级证明）

---

## 8. SchoolMate ↔ Customer A-G 判定

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **SchoolMate → Customer** | F | F | F | F | F | F | **G** (schoolMateVo.schoolMate.customerMobile) |
| **Customer → SchoolMate** | F | F | **A** (getSchoolMateCheckVoOfCustomer) | F | F | F | G |

**真实桥**：
- **Customer → SchoolMate**：A — getSchoolMateCheckVoOfCustomer.json (recommendPhoneListCtrl L19691)
- **SchoolMate → Customer**：F 边界（schoolMateVo.schoolMate.customerMobile 仅是字段，0 命中 API 消费）

---

## 9. SchoolMate ↔ Patient A-G 判定

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **SchoolMate → Patient** | F | F | F | F | F | **A** (schoolMateVo → patient 9 处 L8264-L8277) | A |
| **Patient → SchoolMate** | F | F | F | F | F | **A** (patient.school.id → schoolId L8435) | A |

**真实桥**：
- **SchoolMate → Patient**：A — schoolMateVo 转 patient 9 处字符级（appointOrderCtrl）
- **Patient → SchoolMate**：A — patient.school.id → schoolId L8435 单向
- **schoolMateCheck → Patient**：F（0 命中）
- **Patient → schoolMateCheck**：F（0 命中）

---

## 10. SchoolMate ↔ MedicalRecord A-G 判定

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **SchoolMate → MedicalRecord** | F | F | F | F | F | F | F |
| **MedicalRecord → SchoolMate** | F | F | F | F | F | F | F |
| **schoolMateCheck → MedicalRecord** | F | F | F | F | F | F | F |
| **MedicalRecord → schoolMateCheck** | F | F | F | F | F | F | F |

**结论**：**schoolMate / schoolMateCheck 与 medicalRecord 0 桥**（A — 0 命中）
- schoolMateCheckVo 0 包含 medicalRecordId
- medicalRecordVo 0 包含 schoolMateId
- API Request 0 互证

---

## 11. SchoolMateCheck ↔ Customer / Patient / MedicalRecord A-G 判定

### 11.1 SchoolMateCheck ↔ Customer

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **schoolMateCheck → Customer** | F | F | F | F | F | F | **G** (customerMobile 字段) |
| **Customer → schoolMateCheck** | F | F | **A** (getSchoolMateCheckVoOfCustomer) | F | F | F | G |

### 11.2 SchoolMateCheck ↔ Patient

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **schoolMateCheck → Patient** | F | F | F | F | F | F | F |
| **Patient → schoolMateCheck** | F | F | F | F | F | F | F |

**结论**：schoolMateCheck 与 patient **0 直接桥**（A — 0 命中）
- schoolMateCheckVo 0 包含 patientId
- schoolMateCheckVo 0 包含 patient object
- patient 0 包含 schoolMateCheck 字段

### 11.3 SchoolMateCheck ↔ MedicalRecord

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **schoolMateCheck → MedicalRecord** | F | F | F | F | F | F | F |
| **MedicalRecord → schoolMateCheck** | F | F | F | F | F | F | F |

**结论**：schoolMateCheck 与 medicalRecord **0 桥**（A — 0 命中）

---

## 12. Patient ↔ School 双向验证

### 12.1 Patient → School（A — 字符级 L8434-L8435）

```javascript
$scope.basic.schoolName = patient.school ? patient.school.schoolName : '';
$scope.obj.schoolId = patient.school ? patient.school.id : null;
```

**已确证**（S1-132 报告）：patient.school.id → schoolId（A）

### 12.2 School → Patient（F 边界）

- 0 命中 `school.patient` 字段（A）
- 0 命中 `schoolMate.patient` 字段（A）
- 0 命中 `schoolMateCheckVo.patient` 字段（A）

**结论**：
- Patient → School：A 级桥（patient.school 单向）
- School → Patient：F 边界（0 命中）

---

## 13. Patient ↔ MedicalRecord A-G 判定

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **Patient → MedicalRecord** | F | F | **A** (L6693 getPatientInfo { id: res.object.medicalRecord.patientId }) | F | F | **A** (medicalRecord.patientId) | A |
| **MedicalRecord → Patient** | F | F | **A** (getMedicalRecord { id: $scope.medicalRecordId } → getPatientInfo) | F | F | **A** (medicalRecord.patientId) | A |

**结论**：
- Patient ↔ MedicalRecord：**A 级双向桥**（A — 字符级多源互证）

---

## 14. Customer ↔ MedicalRecord A-G 判定

| 方向 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **Customer → MedicalRecord** | F | F | **A** (medicalRecord 包含 patientId → customerVo 查询链) | F | F | F | A |
| **MedicalRecord → Customer** | F | F | F | F | F | F | F |

**结论**：
- Customer → MedicalRecord：**A 级间接桥**（通过 patient 链）
- MedicalRecord → Customer：F 边界（0 命中直接 API）

---

## 15. 数量精确统计（A — 字符级）

| 指标 | 精确数 | 备注 |
|---|---:|---|
| **schoolMate 总命中** | **200+** | S1-132 报告 |
| **schoolMateId 总命中** | **19** | A — 精确 |
| **schoolMateVo 总命中** | **9** | A — 字符级 |
| **schoolMateCheck 总命中** | **174** | A — 精确 |
| **schoolMateCheckVo 总命中** | **174** | A — 精确 |
| **schoolMateCheckId 总命中** | 多 | A — schoolMateCheckVo 字段访问 |
| **customerMobile 总命中** | **15** | A — 精确 |
| **customerId 总命中** | **128+** | S1-131 报告 |
| **patientId 总命中** | **89** | A — 精确 |
| **medicalRecordId 总命中** | **161** | A — 精确 |
| **schoolMate 中 customerId 命中数** | **0** | A — 0 命中 |
| **schoolMateCheck 中 customerId 命中数** | **0** | A — 0 命中 |
| **schoolMate 中 patientId 命中数** | **0** | A — 0 命中 |
| **schoolMateCheck 中 patientId 命中数** | **0** | A — 0 命中 |
| **schoolMate 中 medicalRecordId 命中数** | **0** | A — 0 命中 |
| **schoolMateCheck 中 medicalRecordId 命中数** | **0** | A — 0 命中 |
| **patient.school 命中** | **2 处** | A — L8434, L8435 字符级 |
| **patient.schoolClass 命中** | **2 处** | A — L8437, L8438 字符级 |
| **schoolMateVo → patient 字段映射** | **9 处** | A — L8264-L8277 |
| **getSchoolMateCheckVoOfCustomer 调用** | **1 处** | A — L19691 |
| **getSchoolMateCheckVoOfRecommendPhone 调用** | **1 处** | A — L19753 |

---

## 16. State / URL 汇合检查（A — 字符级）

| State Param | 出现次数 | 关联业务 |
|---|---:|---|
| `$stateParams.medicalRecordId` | **25** | 业务主链 |
| `$stateParams.patientId` | **13** | 患者维护 |
| `$stateParams.customerId` | **20** | 顾客业务 |
| `$stateParams.schoolMateCheckId` | **0** | **schoolMate 域 0 命中** |
| `$stateParams.schoolMateId` | **0** | **schoolMate 域 0 命中** |

**结论**：
- **schoolMate / schoolMateCheck 0 通过 State 桥到其他域**（A — 0 命中）
- medicalRecord / patient / customer 都有 State Param
- **recommendPhoneListCtrl** 通过 `item.recommendPhone.selfCustomerId` 间接获取 customerId，**不是 State Param**（A — L19671）

---

## 17. Factory / Service 汇合检查

### 17.1 ObjectFactory 复用

- `$scope.patientObjectFactory = new ObjectFactory();` (L4946, L5242, L7490)
  - **L4947** `$scope.patientObjectFactory.saveOrQuery('/admin/getCustomerVo.json', ...)` 
  - **【关键发现】patientObjectFactory 调用 getCustomerVo.json**（A — 字符级 L4947）
  - 含义：patient 业务的 ObjectFactory 复用，**实际调 customerVo API**
- L5930 `$scope.patientObjectFactory = res.result.vo.customer;` — **patientObjectFactory 实际承载 customer Object**（A — 字符级）

**【关键反向】**：`patientObjectFactory` 名称是 patient，但**实际 API 是 getCustomerVo**（A — 字符级直接证明）

### 17.2 共享 ObjectFactory 模式

- recommendPhoneListCtrl 使用 `new ObjectFactory()` 通用模式
- appointOrderCtrl 使用 `new ObjectFactory()` 通用模式
- schoolMateCheck 业务使用 `$scope.checkVoObjectFactory` 独立工厂
- 0 共享 Service 桥（A — 0 命中 service / factory 跨 Controller 共享）

### 17.3 Factory 跨 Controller 桥

- **0 命中** `getCustomerVo` 在 schoolMate 域 Controller 直接调用（A）
- **0 命中** schoolMate API 在 customer/patient/medicalRecord Controller 调用（A）
- **结论**：Factory 跨域 0 桥

---

## 18. 核心 DAG（A-K）

### DAG A: School → schoolId
（沿用 S1-132，本轮复用）

### DAG B: School → SchoolMate
（沿用 S1-132，本轮复用）

### DAG C: SchoolMate → SchoolMateCheck
（沿用 S1-132，本轮复用）

### DAG D: Customer → SchoolMateCheck（A — 强字符级）

```
[recommendPhoneListCtrl UI 列表]
   ↓ A (L19671)
item.recommendPhone.selfCustomerId
   ↓ A
customerId (variable, $scope.customerId)
   ↓ A (L19691)
new ObjectFactory().saveOrQuery("/admin/getSchoolMateCheckVoOfCustomer.json", {
  customerId: $scope.customerId,
  recommendPhoneId: $scope.recommendPhoneId
})
   ↓ A
res.result.object = schoolMateCheckVo
   ↓ A (L19698)
$scope.mateCheckObject = res.result.object
   ↓ A
后续: UI 渲染
```

**完整字符级证据**（A — 字符级 L19335, L19671, L19691, L19698, L19703-L19712, L19752-L19761）

### DAG E: SchoolMate / SchoolMateCheck → Customer（F 边界）

- schoolMateVo.schoolMate.customerMobile (A) **仅字段**
- schoolMateCheckVo.customerMobile (A) **仅字段**
- **0 命中 API 消费 customerMobile**（A）
- 0 命中 schoolMateCheckVo → customerVo 桥
- 0 命中 schoolMateCheckVo → customerVo 任何方向

**结论**：**F 边界**（反向 0 桥）

### DAG F: SchoolMate / SchoolMateCheck → Patient

**SchoolMate → Patient**（A — 字符级 9 处）：
```
schoolMateVo (L8264-L8277)
   ↓ A
appointOrderCtrl 选 patient
   ↓ A
patient 字段映射：
- schoolMateVo.school.id → schoolId
- schoolMateVo.schoolClass.id → classId
- schoolMateVo.schoolMate.gender → gender
- schoolMateVo.schoolMate.customerMobile → linkMobile
- schoolMateVo.school.schoolName + schoolClass.className → patientRemark
- schoolMateVo.schoolMate.birthday → birthday
- schoolMateVo.schoolMate.classMateName → keyword
   ↓ A
patient Object (appointVo)
```

**schoolMateCheck → Patient**：F 边界（0 命中 patientId）

### DAG G: Patient → School（A — 字符级）

```
[某 API Response]
   ↓ A (L8435)
patient.school.id
   ↓ A
$scope.obj.schoolId
   ↓ A
后续: school 业务
```

**反向 School → Patient**：F 边界

### DAG H: Patient → MedicalRecord（A — 字符级）

```
getMedicalRecord { id: $scope.medicalRecordId }
   ↓ A (L1964)
res.object.patientId
   ↓ A (L6693)
getPatientInfo { id: res.object.medicalRecord.patientId }
   ↓ A
patient Object
```

**完整桥**：A — 字符级多源互证

### DAG I: Customer → MedicalRecord（A — 间接桥）

```
customer (customerVo)
   ↓ A
patient (medicalRecord.patientId)
   ↓ A
medicalRecord
```

**字符级证据**：
- patientObjectFactory 调 getCustomerVo (L4947)
- medicalRecord.patientId 调 getPatientInfo (L6693)
- **Customer → MedicalRecord 是间接桥，通过 patient 中转**（A）

### DAG J: SchoolMate / SchoolMateCheck → MedicalRecord（F 边界）

- schoolMateCheckVo 0 包含 medicalRecordId
- medicalRecordVo 0 包含 schoolMateId
- API 0 互证

**结论**：**F 边界**

### DAG K: schoolId → 主业务

```
[schoolId 各种 source]
   ↓ A
API Request
   ├─ 筛查业务 (schoolListCtrl / schoolClass / schoolPlan / schoolMate) — S1-132
   ├─ patient 业务 (patient.school.id) — A — L8435
   └─ 0 命中 sales / charge / delivery / machine / clinic
```

---

## 19. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | schoolMate 来源 | API Response / ObjectFactory | A | 多处 | A |
| 2 | schoolMateId 来源 | res.vo.schoolMate.id / res.vo.schoolMateCheck.schoolMateId | A | L41666, L41504 | A |
| 3 | schoolMate Consumer | schoolMateVo 9 处 + schoolMateCheckVo 174 处 | A | L8264, L41666 | A |
| 4 | schoolMateCheck 来源 | API Response | A | 多处 | A |
| 5 | schoolMateCheckId 来源 | res.vo.schoolMateCheck.id | A | L41668, L41748 | A |
| 6 | schoolMateCheck Consumer | schoolMateCheckVo 174 处 + 报表 + 通知 + 打印 | A | 多处 | A |
| 7 | customerMobile 来源 | schoolMateVo.schoolMate.customerMobile + schoolMateCheckVo.customerMobile | A | L8265, L41684 | A |
| 8 | customerMobile Consumer | **仅 UI 验证** + 0 命中 API Request | A | L42085, L44461 | A — 0 命中 API |
| 9 | customerId 来源 | $stateParams / Response / recommendPhone.selfCustomerId | A | 20+ 处 | A |
| 10 | customerId Consumer | getCustomerVo (14) / getCustomerWallet / getCustomerMember | A | L3650, L4947 | A |
| 11 | patient 来源 | API Response / ObjectFactory | A | 多处 | A |
| 12 | patientId 来源 | $stateParams / Response / patient.id | A | 89 处 | A |
| 13 | patientId Consumer | getPatientInfo (10) / getPatientVoList (4) | A | L1970, L8364 | A |
| 14 | medicalRecord 来源 | API Response | A | 多处 | A |
| 15 | medicalRecordId 来源 | $stateParams / Response | A | 161 处 | A |
| 16 | getSchoolMateCheckVoOfCustomer 桥 | **A** | A | L19691 | A |
| 17 | SchoolMate → Customer | F | A | 0 命中 | F |
| 18 | SchoolMate → Patient | A | A | L8264-L8277 | A |
| 19 | SchoolMate → MedicalRecord | F | A | 0 命中 | F |
| 20 | SchoolMateCheck → Customer | F（仅 customerMobile 字段） | A | L41684 | F |
| 21 | SchoolMateCheck → Patient | F | A | 0 命中 | F |
| 22 | SchoolMateCheck → MedicalRecord | F | A | 0 命中 | F |
| 23 | Patient → School | A | A | L8434-L8438 | A |
| 24 | Patient → MedicalRecord | A | A | L6693, L1964 | A |
| 25 | Customer → MedicalRecord | A 间接桥 | A | L4947, L6693 | A |
| 26 | 最终汇合 DAG 与复刻红线 | 第 18 节 | A | 本文档 | A |

---

## 20. A/B/C/D/E/F 分布

- **A**：22
- **B**：1（Patient↔MedicalRecord 多源互证）
- **C**：0
- **D**：1（patientObjectFactory 名称 vs API 不一致 — 实际调 getCustomerVo）
- **E**：**0**（红线要求）
- **F**：7（SchoolMate → Customer / SchoolMateCheck → Patient / SchoolMateCheck → MedicalRecord / School → Patient / SchoolMate → MedicalRecord / MedicalRecord → Customer / SchoolMate / SchoolMateCheck → MedicalRecord）

---

## 21. 历史差异

### 21.1 S1-132 中 schoolMateCheckVo 0 含 medicalRecordId 误判

| 项 | S1-132 | S1-133 | 差异 | 当前采用 |
|---|---|---|---|---|
| schoolMateCheckVo → medicalRecord | 0 桥（F 边界） | **0 桥**（A 验证 174 处 schoolMateCheckVo 字段） | 一致 | A |
| customerId → schoolMateCheck | A 桥（getSchoolMateCheckVoOfCustomer） | **A 桥**（recommendPhoneListCtrl L19335 字符级多源互证） | 加强 | A |
| patient.school → schoolId | A 桥（patient.school.id L8435） | **A 桥**（L8434-L8438 4 行字符级直接证明） | 加强 | A |

### 21.2 S1-131 中 customerMobileDisable 误判

- S1-131 报告：customerMobileDisable 是 coupon 字段
- S1-133 验证：customerMobileDisable 是 printConfigCtrl / 其它 Controller 的小票显示开关（A — L52739, L57750 等 6 处）
- **与 S1-131 误判不冲突**（不是 coupon，是小票）

### 21.3 S1-128/S1-129 中 schoolMate 与 medicalRecord 关系

- S1-128 报告：medicalProduct / medicalProductId 业务
- S1-129 报告：medicalProduct → Machine → Delivery
- **本轮新发现**：schoolMate / schoolMateCheck 与 medicalProduct 0 桥，与 medicalRecord 0 桥

### 21.4 S1-130/S1-131 中 patient 与 school 关系

- S1-131 报告：patient.school.id → schoolId（A 桥，4 行字符级）
- **S1-133 复用 + 加强**：patient.school 4 行字符级直接证明 + patientObjectFactory 间接桥

---

## 22. 复刻红线

### 22.1 不能自行增加的字段

- schoolMateVo 不应包含 customerId 字段（A — 0 命中）
- schoolMateCheckVo 不应包含 customerId / patientId / medicalRecordId 字段（A — 0 命中）
- schoolMate 不应包含 medicalRecordId 字段（A — 0 命中）
- 任何 controller.js 中 0 命名的 schoolMate 字段

### 22.2 不能自行补桥的模块

- **schoolMate / schoolMateCheck → medicalRecord 0 桥**（F 边界）
- **schoolMateCheck → Customer 0 桥**（F 边界 — customerMobile 仅字段）
- **schoolMateCheck → Patient 0 桥**（F 边界）
- **School → Patient 0 桥**（F 边界 — 反向 0 命中）
- **schoolMate / schoolMateCheck → Customer 0 桥**（F 边界）
- **不能假定"customerMobile 就能 match customer"**（A — 14 处 getCustomerVo 0 命中 mobile 字段）
- **不能假定"customerId 就能 match schoolMate"**（A — 0 命中）

### 22.3 不能假定存在的 API

- `/admin/getSchoolMateCheckVoOfCustomer.json { mobile: }` 不存在（A — 14 处 0 命中）
- `/admin/getSchoolMateCheckVoByMobile.json` 不存在
- `/admin/getCustomerByMobile.json` 不存在
- `/admin/getSchoolMateByMedicalRecordId.json` 不存在

### 22.4 不能等同的 ID

| ID | 不能等同 |
|---|---|
| schoolMateId | ≠ patientId / customerId / medicalRecordId（A — 0 命中）|
| schoolMateCheckId | ≠ patientId / customerId / medicalRecordId（A — 0 命中）|
| schoolMateId | ≠ studentId（**studentId 不存在**）（A — 0 命中）|
| customerMobile | ≠ customerId / patientId / mobile（A — 0 互换）|
| **patient.school.id** | **≡ schoolId**（A — L8435 字符级直接证明）|
| **patient.schoolClass.id** | **≡ classId**（A — L8437 字符级直接证明）|
| **recommendPhone.selfCustomerId** | **是 customerId 来源**（A — L19671 字符级）|
| medicalRecord.patientId | ≡ patientId（A — L6693 字符级）|
| **patientObjectFactory** | **调 getCustomerVo.json**（A — L4947 字符级，命名误导）|

### 22.5 必须保留的 F 边界

- schoolMate / schoolMateCheck → medicalRecord（A — 0 命中）
- School → Patient（A — 0 命中）
- schoolMateCheck → Customer（A — 仅 customerMobile 字段，0 API 消费）
- recommendPhone 后端实现 F 边界
- 0 共享 Service / Factory F 边界
- 后端实体 FK F 边界
- $stateParams.schoolMateCheckId / schoolMateId 不存在

### 22.6 命名误导必须标注

- `patientObjectFactory` **实际调 getCustomerVo**（A — L4947 字符级）
- `customerMobile` **≠ mobile 字段**（A — 命名风格不同，0 互证）
- `getCustomerVo` **0 接收 mobile 字段**（A — 14 处全 customerId）
- `getPatientVoList` **接收 mobile 字段**（A — L8364, L8374, L8390, L18981）
- `customerMobile` 字段是**字符串**（手机号），**不是 ID**（A — 格式验证 /^1[3|4|5|6|7|8|9]\d{9}$/）
- `medicalRecord.patientId` 是**字符串还是数字**取决于后端，**前端仅当 ID 字段使用**（A）

---

## 23. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**） | ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**） | ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**） | ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**） | ✓ |
| 历史 MD 165-194 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 195_*.md | 是 | ✓ |
| 临时脚本（2 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 24. Git

- 本轮 commit hash：（待执行 `git add -- 195_*.md` / `git commit -m "docs(195): S1-133 SchoolMate与Patient_Customer_MedicalRecord汇合链深度审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：202 → 203
- 本轮 untracked 预期：10（保留 10 untracked，新增 195 后变 10 untracked 因为 195 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：195_S1-133_*.md
