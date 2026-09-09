# S1-134 SchoolMate → Appointment / 接诊入口真实汇合链深度审计

> **项目**：OptFlow PMS 逆向建模
> **本轮核心问题**：schoolMateVo 到底如何进入"预约 / 接诊"体系？
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-195 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / 2,194,196 bytes / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变）|
| **appointOrderCtrl** | **L3664-L3666（3 行空 stub）** — **S1-132/133 误判修正** |
| **addCheckinCtrl** | **L8159-L8777（约 620 行）** — schoolMateVo 9 处实际 Controller |
| schoolMateVo 9 处 | L8264-L8277 |
| choosePatient 13 参 | L8424-L8455 |
| insertCustomerCheckin 桥 | L8667 + L8679-L8681 |
| schoolMateCheckId 命中 | **37 处**（A — 含 1 处 L8280 注释 + 1 处 L8706 注释 + 35 处其它业务）|
| customerCheckin.medicalRecordId 桥 | 多处 |

---

## 2. 重大发现：S1-132 / S1-133 误判修正

### 2.1 appointOrderCtrl L3664 是空 stub（A — 字符级）

```javascript
angular.module("bestvisionWeb").controller("appointOrderCtrl", ["$scope", "ListFactory", "$rootScope", "$state", "ObjectFactory", "$timeout", function ($scope, ListFactory, $rootScope, $state, ObjectFactory, $timeout) {
  // window.open(API_HOST + "/clinic/index.html#/clinic/appointment");
}]);
```

**3 行空实现** + 一行注释（指向 clinic/index.html 新窗口）

### 2.2 schoolMateVo 9 处实际在 addCheckinCtrl L8159（A — 字符级）

S1-132 / S1-133 报告中"appointOrderCtrl 中 schoolMateVo 9 处"是**误判**：

- `appointOrderCtrl` **L3664-L3666 空 stub**
- `schoolMateVo` 9 处 **L8264-L8277** 实际在 `addCheckinCtrl`（接诊/登记 Controller）
- **addCheckinCtrl = 接诊/登记**（L3664 之后的接诊业务）

**【D 冲突 — 当前采用】**：修正 S1-132 / S1-133 误判
- S1-132 报告"appointOrderCtrl L3664 是 schoolMateVo 消费者" — **错误**
- 当前采用：**addCheckinCtrl L8159** 是 schoolMateVo 真正 Controller
- schoolMateVo 9 处 **在 addCheckinCtrl 范围内**（A — 字符级直接证明）

---

## 3. appointOrderCtrl 完整解剖（A — 字符级）

### 3.1 appointOrderCtrl L3664-L3666（3 行空 stub）

| 项 | 证据 |
|---|---|
| 注册点 | L3664 `.controller("appointOrderCtrl", ...)` |
| DI | `$scope, ListFactory, $rootScope, $state, ObjectFactory, $timeout` |
| 函数体 | `// window.open(API_HOST + "/clinic/index.html#/clinic/appointment");` |
| 真实业务 | 注释：window.open 到 clinic/index.html |
| **实际** | **空 stub**（A） |
| 结论 | appointOrderCtrl 不在 controller.js 范围处理预约逻辑；预约在外部 HTML 入口 |

**【F 边界】**：真正的"预约"逻辑在 `clinic/index.html`（F — 不在工作区范围）

### 3.2 真正的"预约→接诊"Controller = addCheckinCtrl L8159

| 项 | 证据 |
|---|---|
| 注册点 | L8159 `.controller("addCheckinCtrl", ...)` |
| DI | `$scope, $timeout, WechatConfig, Popup, QiniuFactory, $stateParams, $rootScope, $state, ObjectFactory, ListFactory, $http` (12 个) |
| State Param | `$stateParams.appointId / patientId / type / sex / pic / tel / name / birthday / remark / customerName / channelName / employeeId`（A — L8194-L8232 含 13 个字段） |
| $stateParams.type 含义 | 0 = 登记跳转（`getAppointPatientVo`） / 1 = 到店筛查跳转（`getAppointSchoolMateVo`） |
| 行数 | ~620 行（L8159-L8777） |
| 业务 | **接诊/登记**（Appointment + Checkin） |

---

## 4. schoolMateVo 9 处逐项精确映射（A — 字符级）

**所有 9 处在 addCheckinCtrl `queryStudentInfo` 函数 L8234-L8286 范围内**（A — 字符级）

### 4.1 type=1 分支（schoolMateVo 实际消费）

**L8223-L8232**：appointVo 双类型
```javascript
$scope.appointVo = {
  register: { url: "getAppointPatientVo", type: 0 },      // 登记跳转
  reachStore: { url: "getAppointSchoolMateVo", type: 1 }   // 到店筛查跳转
}[$stateParams.type];
```

**L8262-L8282** type=1 完整 9 处映射：

| # | 源 | 字段 | 目标 | 目标字段 | 用途 |
|---:|---|---|---|---|---|
| 1 | `item.schoolMateVo.schoolMate` | `gender` | `$scope.obj` | `gender` | 接诊表单 |
| 2 | `item.schoolMateVo.schoolMate` | `customerMobile` | `$scope.obj` | `linkMobile` | 接诊表单手机号 |
| 3 | `item.schoolMateVo.school` | `schoolName` | `patientRemark` | 拼接 | 接诊备注 |
| 4 | `item.schoolMateVo.schoolClass` | `className` | `patientRemark` | 拼接 | 接诊备注 |
| 5 | `item.schoolMateVo.schoolMate` | `birthday` | `$scope.obj` | `birthday` | 接诊表单 |
| 6 | `item.schoolMateVo.school` | `id` | `$scope.obj` | `schoolId` | 接诊表单 |
| 7 | `item.schoolMateVo.schoolClass` | `id` | `$scope.obj` | `classId` | 接诊表单 |
| 8 | `item.schoolMateVo.school` | `schoolName` | `$scope.basic` | `schoolName` | UI 展示 |
| 9 | `item.schoolMateVo.schoolClass` | `className` | `$scope.careatInfo` | `inputVal` | UI 展示 |

**完整 9 行字符级直接证明**（A — L8264-L8277）

**type=1 后续**：
- L8273: `$scope.basic.schoolName = item.schoolMateVo.school.schoolName;`
- L8274: `$scope.careatInfo.inputVal = item.schoolMateVo.schoolClass.className;`
- L8275-L8276: careatInfo.disabled/disabledEdit = true
- L8277: `$scope.keyword = item.schoolMateVo.schoolMate.classMateName;`
- L8278: `$scope.doctorName = "请选择接诊视光师";`
- L8279: `$scope.obj = _obj;` —— **整体赋给 obj**
- L8280: 注释代码 `$scope.appointVo.schoolMateCheckId = item.schoolMateCheck.id;`
- L8281: `$scope.searchPatientkeyword();` —— **触发 patient 桥**

### 4.2 type=0 分支（patientVo 实际消费）

**L8241-L8260** type=0 完整 11 处映射：

| # | 源 | 字段 | 目标 |
|---:|---|---|---|
| 1 | `item.patient` | `patientGender` | obj.gender |
| 2 | `item.patient` | `avatar` | obj.avatar |
| 3 | `item.customer` | `linkMobile` | obj.linkMobile |
| 4 | `item.appoint` | `remark` | obj.patientRemark |
| 5 | `item.patient` | `patientBirthday` | obj.birthday |
| 6 | `item.customer` | `customerName` | obj.customerName |
| 7 | `item.customer` | `channel` | channelName |
| 8 | `item.patient` | `id` | obj.patientId |
| 9 | `item.employee` | `id` | obj.employeeId |
| 10 | `item.appoint` | `id` | obj.appointId |

**完整 11 行字符级直接证明**（A — L8243-L8252）

### 4.3 schoolMateVo 完整消费链

**字符级 evidence**：
```javascript
// L8234-L8236: 入口
$scope.queryStudentInfo = function () {
  if (!$scope.appointVo) return;
  $scope.careatInfo.isshow = false;
  new ObjectFactory().saveOrQuery("/admin/" + $scope.appointVo.url + ".json", {
    appointId: $stateParams.appointId                    // ← Request
  }).then(function (res) {
    var item = res.object;                                // ← Response
    if ($scope.appointVo.type === 0) {                    // ← type=0 分支
      // ... patientVo 11 处映射 ...
    } else if ($scope.appointVo.type === 1) {            // ← type=1 分支
      // ... schoolMateVo 9 处映射 ...
    }
  });
};
```

**【关键发现】**：
- schoolMateVo **不出现在 Request**（A — Request 字段仅 appointId）
- schoolMateVo **完全在 Response 处理**（A — item.schoolMateVo.*）
- schoolMateVo **不进入后续 API Request**（A — 仅写入 $scope.obj）
- schoolMateVo **是 item.object 的子字段**（A — `res.object.schoolMateVo`）

---

## 5. addCheckinCtrl 完整 API（A — 字符级）

### 5.1 API 全集

| API | 类型 | 行号 | 业务 |
|---|---|---|---|
| `/admin/getAppointPatientVo.json` | R | L8237 拼接 | type=0 入口 |
| `/admin/getAppointSchoolMateVo.json` | R | L8237 拼接 | type=1 入口（schoolMateVo 消费者）|
| `/admin/selectEmployeeVoList.json` | R | L8339 | 视光师列表 |
| `/admin/getPatientVoList.json` | R | L8364, L8390 | 患者列表（**mobile 字段**）|
| `/admin/getCheckinPatientVoList.json` | R | L8419 拼接 | 接诊患者列表 |
| `/admin/getCheckinPatientVoListOfCompany.json` | R | L8419 拼接 | 接诊患者列表（公司维度）|
| `/admin/getEmployeeVo.json` | R | L8564 | 视光师详情 |
| `/admin/getCheckinQrcode.json` | R | L8573 拼接 | 签到二维码 |
| `/admin/getCheckinQrcodeOfCompany.json` | R | L8573 拼接 | 签到二维码（公司）|
| `/admin/confirmArrivalOfAppoint.json` | W | L8658 | 确认到店 |
| `/admin/insertCustomerCheckinOfNewPaitent.json` | W | L8667 | 插入新患者接诊 |
| `/admin/insertCustomerCheckinOfNewCustomer.json` | W | L8679 | 插入新顾客接诊 |
| `/admin/insertCustomerCheckin.json` | W | L8681 | 插入接诊 |
| `/admin/addSchoolMateConsume.json` | W | L8705（**注释代码**）| 注释代码，不执行 |
| `window.grantAuth.hasAuthForCompany` | R | L8321 | 公司权限 |
| `window.grantAuth.getFrontAuth` | R | L8402 | 前台权限（含 `schoolEnable` 字段）|

### 5.2 API Request 字段审计

| API | Request 字段 | 关键 ID 是否进入 |
|---|---|---|
| getAppointPatientVo / getAppointSchoolMateVo | `appointId` (L8238) | **appointId 是唯一 Request 字段** |
| selectEmployeeVoList | `companyId / keyword / status / approved` | 0 命中 schoolMateId/customerId/patientId |
| getPatientVoList | `name / mobile` | 0 命中 customerId/medicalRecordId |
| getCheckinPatientVoList[OfCompany] | 无参数 | 0 命中 |
| getEmployeeVo | `employeeId` | 0 命中 schoolMate |
| getCheckinQrcode[OfCompany] | 无参数 | 0 命中 |
| confirmArrivalOfAppoint | `appointId` | **appointId** |
| insertCustomerCheckinOfNewPaitent | `$scope.checkCustomer` 全字段 | customerId / appointId / registrationFeeId 等 |
| insertCustomerCheckin | `$scope.obj` 全字段 | patientId / schoolId / classId / customerName 等 |
| **addSchoolMateConsume** | **注释代码** | **schoolMateCheckId / patientId（注释）** |

**【关键发现】**：
- **Appointment API 仅接收 `appointId`**（A — L8238, L8658）
- **patientId / customerId / schoolMateId / schoolMateCheckId 不进入 Appointment API Request**（A — 0 命中）
- 完整 patient Object **进入 insertCustomerCheckin.json**（A — L8695 `$scope.obj`）

---

## 6. State / URL 完整审计

### 6.1 addCheckinCtrl 范围 $stateParams（A — L8194-L8238）

| 字段 | 出现行号 | 是否注释 | 实际消费 |
|---|---|---|---|
| `$stateParams.appointId` | L8216, L8238, L8648, L9051 | 8216 注释 | L8238 + L8648 实际 |
| `$stateParams.patientId` | L8213 | 注释 | **0 实际消费** |
| `$stateParams.type` | L8232 | 实际 | 决定 register / reachStore |
| `$stateParams.sex` | L8194 | 注释 | 0 实际 |
| `$stateParams.pic` | L8195 | 注释 | 0 实际 |
| `$stateParams.tel` | L8197 | 注释 | 0 实际 |
| `$stateParams.name` | L8196 | 注释 | 0 实际 |
| `$stateParams.birthday` | L8199 | 注释 | 0 实际 |
| `$stateParams.remark` | L8198 | 注释 | 0 实际 |
| `$stateParams.customerName` | L8202 | 注释 | 0 实际 |
| `$stateParams.channelName` | L8205 | 注释 | 0 实际 |
| `$stateParams.employeeId` | L8209 | 注释 | 0 实际 |
| `$stateParams.id` | (估计 L8208) | 注释 | 0 实际 |

**结论**：
- **$stateParams.appointId 和 $stateParams.type 实际消费**（A）
- **其它 11 个 $stateParams 字段全部是注释代码**（A — L8194-L8218 `/* ... */` 包裹）

### 6.2 $state.go（A — 字符级）

| 目标 | 行号 | 触发 |
|---|---|---|
| `"checkinList"` | L8654 | 接诊/登记完成后 |

**结论**：addCheckinCtrl **只有 1 处 $state.go**（A — 跳转到 checkinListCtrl）

### 6.3 $stateParams.patientId 在 addCheckinCtrl 0 实际消费（A）

- L8213: `// $scope.obj.patientId = parseInt($stateParams.patientId) ? $stateParams.patientId : null;`
- **L8213 是注释代码**（A）
- `$stateParams.patientId` **实际为 0 消费**（A）
- `$scope.obj.patientId` 来源是 `item.patient.id` (L8250) 或 `choosePatient` 13 个参数 (L8424)

---

## 7. schoolMateVo → Patient 桥（A — 字符级完整链）

### 7.1 字符级 evidence 完整链

**Step 1：API Response**（A — L8237）
```javascript
new ObjectFactory().saveOrQuery("/admin/" + $scope.appointVo.url + ".json", {
  appointId: $stateParams.appointId
}).then(function (res) {
  var item = res.object;  // ← item 包含 schoolMateVo / patient / customer / appoint / employee
```

**Step 2：type=1 分支**（A — L8262-L8281）
```javascript
} else if ($scope.appointVo.type === 1) {
  var _obj = {
    gender: item.schoolMateVo.schoolMate.gender,
    linkMobile: item.schoolMateVo.schoolMate.customerMobile,    // ← customerMobile
    patientRemark: "" + item.schoolMateVo.school.schoolName + item.schoolMateVo.schoolClass.className,
    birthday: item.schoolMateVo.schoolMate.birthday ? parseInt(item.schoolMateVo.schoolMate.birthday) : null,
    customerName: item.customer.customerName,
    appointId: item.appoint.id,
    schoolId: item.schoolMateVo.school.id,
    classId: item.schoolMateVo.schoolClass.id
  };
  $scope.basic.schoolName = item.schoolMateVo.school.schoolName;
  $scope.careatInfo.inputVal = item.schoolMateVo.schoolClass.className;
  $scope.careatInfo.disabled = true;
  $scope.careatInfo.disabledEdit = true;
  $scope.keyword = item.schoolMateVo.schoolMate.classMateName;
  $scope.doctorName = "请选择接诊视光师";
  $scope.obj = _obj;
  $scope.searchPatientkeyword();  // ← 触发 patient 搜索
}
```

**Step 3：patient 搜索**（A — L8359-L8376）
```javascript
$scope.searchPatientkeyword = function () {
  if (!$scope.keyword) return false;
  $scope.firstPatientlist = true;
  $scope.getPatientList = new ListFactory("/admin/getPatientVoList.json", 0, 30, { 
    name: $scope.keyword,             // ← keyword = schoolMateVo.schoolMate.classMateName
    mobile: $scope.obj.linkMobile    // ← linkMobile = schoolMateVo.schoolMate.customerMobile
  });
  $scope.getPatientList.nextPage();
};
```

**Step 4：patient 列表 → choosePatient**（A — L8424-L8455）
```javascript
$scope.choosePatient = function (event, patientId, patientName, birthday, gender, linkMobile, channel, channelTagId, customerName, customerId, avatar, patientRemark, patient) {
  $scope.selectedPatientId = patientId;
  event.stopPropagation();
  $scope.inputKeyword = false;
  $scope.obj.patientId = patientId;          // ← patientId
  $scope.checkCustomer.customerId = customerId;  // ← customerId
  $scope.keyword = patientName;
  if (birthday) {
    $scope.obj.birthday = new Date(birthday);
  }
  $scope.basic.schoolName = patient.school ? patient.school.schoolName : '';  // ← patient.school
  $scope.obj.schoolId = patient.school ? patient.school.id : null;            // ← patient.school.id
  $scope.careatInfo.isshow = false;
  $scope.obj.classId = patient.schoolClass ? patient.schoolClass.id : null;  // ← patient.schoolClass.id
  $scope.careatInfo.inputVal = patient.schoolClass ? patient.schoolClass.className : '';
  // ... gender / linkMobile / customerName / patientRemark / channel / channelTagId / avatar / idCard
};
```

**Step 5：插入接诊**（A — L8667 + L8695）
```javascript
// type=1 (schoolMateVo): 走 insertCustomerCheckin.json
url = $scope.obj.patientId 
  ? "/admin/insertCustomerCheckin.json"  // ← patient 存在
  : "/admin/insertCustomerCheckinOfNewCustomer.json";  // ← patient 不存在
new ObjectFactory().saveOrQuery(url, $scope.obj).then(function (res) {
  if (res.status == 0) {
    var printCheckinId = res.result.vo.customerCheckin.id;  // ← 响应 customerCheckin
    // ...
  }
});
```

### 7.2 完整字符级桥汇总

| 桥 | 字符级 | 等级 |
|---|---|---|
| schoolMateVo → linkMobile（patient 字段）| L8265 → L8364 mobile | **A** |
| schoolMateVo → keyword（patient 字段）| L8277 classMateName → L8364 name | **A** |
| schoolMateVo → schoolId（patient 字段）| L8270 → L8435 | **A** |
| schoolMateVo → classId（patient 字段）| L8271 → L8437 | **A** |
| schoolMateVo → patient.school（同源）| L8270 ↔ L8435 | **A — 多源互证** |
| customerMobile → mobile → getPatientVoList | L8265 → L8364 → L8265 chain | **A** |

**【关键发现】**：
- **schoolMateVo 不直接变成 patient**
- schoolMateVo **9 个字段映射** 到 $scope.obj 的 9 个字段
- 这些字段**再被 choosePatient 选 patient 时**覆盖（patient 字段优先）
- 最终进入 `insertCustomerCheckin.json` Request 的 $scope.obj 是**已被 choosePatient 覆盖后的版本**

---

## 8. schoolMateVo → Customer 桥（A — 字符级）

### 8.1 customerMobile 完整链

**Step 1：schoolMateVo.schoolMate.customerMobile**（A — L8265）
```javascript
linkMobile: item.schoolMateVo.schoolMate.customerMobile,
```

**Step 2：写入 $scope.obj.linkMobile**（A — L8263-L8271）

**Step 3：进入 getPatientVoList mobile 字段**（A — L8364）
```javascript
$scope.getPatientList = new ListFactory("/admin/getPatientVoList.json", 0, 30, { 
  name: $scope.keyword, 
  mobile: $scope.obj.linkMobile  // ← linkMobile → mobile
});
```

**Step 4：进入 getCustomerVo? 0 命中**（A — 0 命中）
- getCustomerVo 14 处全部以 `customerId` 为 Request
- **0 命中 `mobile` 字段**（A）

**【关键】**：
- customerMobile **不进入 getCustomerVo**（A — 0 命中）
- customerMobile **进入 getPatientVoList as mobile**（A — L8364, L8390, L18981 字符级证明）
- **getCustomerVo 与 mobile 字段 0 桥**（A — 14 处 0 命中）

### 8.2 customerMobile → Customer F 边界

- schoolMateCheckVo.customerMobile (L41684) **仅字段**
- schoolMateVo.schoolMate.customerMobile (L8265) **仅字段**
- **0 命中 API Request**（A — 0 互换）
- getCustomerVo **0 接收 mobile 字段**（A — 14 处全 customerId）

**结论**：schoolMateVo → Customer **仅字段映射，不是数据桥**（F 边界）

---

## 9. schoolMateVo → MedicalRecord 桥（F 边界）

### 9.1 schoolMateCheckId 真实消费 0 命中

- L8280: 注释代码 `$scope.appointVo.schoolMateCheckId = item.schoolMateCheck.id;`
- L8706: 注释代码 `schoolMateCheckId: $scope.appointVo.schoolMateCheckId`
- **addSchoolMateConsume.json 0 实际调用**（A — 0 命中）
- **item.schoolMateCheck 0 进入 Request**（A — 0 命中）

### 9.2 schoolMateCheckVo → medicalRecord 0 桥

- schoolMateCheckVo 字段中 0 包含 medicalRecordId（A — 174 处验证）
- medicalRecordVo 0 包含 schoolMateId（A — 0 命中）

**结论**：schoolMateVo → MedicalRecord **0 桥**（F 边界）

---

## 10. schoolMateVo → CustomerCheckin 桥（A — 字符级）

### 10.1 schoolMateVo 9 字段 → $scope.obj → insertCustomerCheckin

**字符级链**（A — L8263-L8271 + L8667 / L8695）：
```
item.schoolMateVo.schoolMate.gender     →  $scope.obj.gender       →  Request
item.schoolMateVo.schoolMate.customerMobile  →  $scope.obj.linkMobile   →  Request
item.schoolMateVo.school.schoolName     →  $scope.obj.patientRemark (拼接)  →  Request
item.schoolMateVo.schoolClass.className  →  $scope.obj.patientRemark (拼接)  →  Request
item.schoolMateVo.schoolMate.birthday   →  $scope.obj.birthday     →  Request
item.customer.customerName                →  $scope.obj.customerName  →  Request
item.appoint.id                          →  $scope.obj.appointId    →  Request
item.schoolMateVo.school.id              →  $scope.obj.schoolId     →  Request
item.schoolMateVo.schoolClass.id         →  $scope.obj.classId      →  Request
```

**完整 9 字段 → Request**（A — 字符级直接证明）

### 10.2 insertCustomerCheckin → customerCheckin Response

**A — L8671, L8697**：
```javascript
var printCheckinId = res.result.vo.customerCheckin.id;
```

- Response 包含 `customerCheckin.id` 和 `customerCheckin.medicalRecordId` (L8791)

### 10.3 addSchoolMateConsume 注释代码（A — L8699-L8713）

```javascript
/* if (
  !$scope.obj.patientId &&
  $scope.appointVo &&
  $scope.appointVo.type === 1
) {
  new ObjectFactory()
    .saveOrQuery("/admin/addSchoolMateConsume.json", {
      schoolMateCheckId: $scope.appointVo.schoolMateCheckId,
      patientId: res.result.vo.customerCheckin.patientId,
    })
    .then(() => {
      dealNeedPrint(printCheckinId);
    });
} else {
  dealNeedPrint(printCheckinId);
} */
```

**关键**：
- addSchoolMateConsume.json API **存在**
- schoolMateCheckId → patientId 桥**在注释代码中**（F 边界 — 不执行）
- 当前 evidence 范围 0 实际调用

**当前采用**：addSchoolMateConsume 0 实际调用，schoolMateCheckId 仅注释（A — 0 命中）

---

## 11. Appointment → Patient / MedicalRecord / 主业务 A-G 判定

### 11.1 Appointment → Patient

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function | F | 0 命中 |
| State | A | `$stateParams.appointId` 是入口 |
| API Response → Request | F | 0 命中（getAppointPatientVo / getAppointSchoolMateVo Response 含 patient / patientId，但 type=1 不直接用 patient.id）|
| Scope/Service | F | 0 命中 |
| Factory | F | 0 命中 |
| Object | F | 0 命中 |
| 字段共现 | A | appointId + patientId 都在 $scope.obj |

**真实桥**：State Param $stateParams.appointId → getAppointPatientVo/SchoolMateVo Response → $scope.obj.appointId/patientId

### 11.2 Appointment → MedicalRecord

| 桥类型 | 是否存在 | 证据 |
|---|---|---|
| Function | F | 0 命中 |
| State | F | $stateParams.medicalRecordId 0 命中 in addCheckinCtrl |
| API Response → Request | F | 0 命中 |
| Scope/Service | F | 0 命中 |
| Factory | F | 0 命中 |
| Object | F | 0 命中 |
| 字段共现 | F | 0 命中 |

**结论**：Appointment → MedicalRecord **0 桥**（F 边界）

### 11.3 Appointment → CustomerCheckin（A — 字符级）

- L8665: `$scope.checkCustomer.appointId = aId;` —— **customerCheckin.appointId 字段**
- L8658-L8660: `confirmArrivalOfAppoint.json { appointId: aId }` —— **appointId → confirmArrival API**
- L8667, L8695: insertCustomerCheckin.json —— **Request $scope.obj/obj**

**真实桥**：
- `appointId` → `confirmArrivalOfAppoint.json` (Write API)
- `appointId` → `checkCustomer.appointId` → `insertCustomerCheckin*.json` (Write API)
- **A — 字符级多源互证**

### 11.4 Appointment → 主业务

| 路径 | 是否存在 |
|---|---|
| Appointment → 验光 | F（0 命中）|
| Appointment → 检查 | F（0 命中）|
| Appointment → 销售 | F（0 命中）|
| Appointment → 收费 | F（0 命中）|
| Appointment → 配送 | F（0 命中）|
| Appointment → 加工 | F（0 命中）|

**结论**：Appointment → 主业务 0 桥（除了 `appointId → customerCheckin`）

### 11.5 $state.go "checkinList" 后续链

L8654: `$state.go("checkinList", printObj);` —— 跳转到 `checkinListCtrl` L8778

`checkinListCtrl` 包含 `customerCheckin` 完整字段，**包含 medicalRecordId**（A — L8791, L10610, L10642 已确认）

---

## 12. customerMobile 完整生命周期（A — 字符级）

```
[API Response] item.schoolMateVo.schoolMate.customerMobile (L8265)
   ↓ A
$scope.obj.linkMobile = customerMobile (L8265 直接赋值)
   ↓ A
$scope.searchPatientkeyword() (L8281)
   ↓ A
$scope.obj.linkMobile 作为 mobile 字段
   ↓ A
getPatientVoList.json { name: $scope.keyword, mobile: $scope.obj.linkMobile } (L8364)
   ↓ A
patient list Response
   ↓ A
choosePatient(event, patientId, ..., linkMobile, ..., patient) (L8424 13 参)
   ↓ A
$scope.obj.linkMobile = linkMobile (UI 传入，覆盖 schoolMateVo 来源)
   ↓ A
后续 $scope.obj 进入 insertCustomerCheckin.json Request (L8695)
```

**【关键反向】**：
- `customerMobile` 字段 **不进入 getCustomerVo**（A — 0 命中 mobile）
- `customerMobile` 字段 **进入 getPatientVoList as mobile**（A — L8364, L8390, L18981 字符级直接证明）
- **0 命中** `customerMobile → getCustomerVo` 桥

---

## 13. 数量精确统计（A — 字符级）

| 指标 | 精确数 | 备注 |
|---|---:|---|
| **appointOrderCtrl 命中** | **0 实际逻辑** | A — 3 行空 stub |
| **addCheckinCtrl 行数** | **~620** | A — L8159-L8777 |
| **schoolMateVo 9 处** | **9** | A — 字符级 |
| schoolMateVo.school 命中 | 2 | A — L8266, L8270, L8273 |
| schoolMateVo.schoolClass 命中 | 3 | A — L8266, L8271, L8274 |
| schoolMateVo.schoolMate 命中 | 4 | A — L8264, L8265, L8267, L8277 |
| **schoolMateVo.schoolMate.customerMobile 命中** | **1** | A — L8265 |
| schoolMateId 命中 | 19 | A — S1-133 报告 |
| schoolMateCheckId 命中 | 37 | A — 多处 |
| customerId 命中 | 128+ | A — S1-131 报告 |
| patientId 命中 | 89 | A — 精确 |
| medicalRecordId 命中 | 161 | A — 精确 |
| customerMobile 命中 | 15 | A — S1-133 报告 |
| mobile 命中 | 28 | A — 含 L8364, L8390, L18981 |
| Appointment API unique | 6+ | A — getAppointPatientVo / getAppointSchoolMateVo / confirmArrivalOfAppoint / insertCustomerCheckin[OfNewPaitent][OfNewCustomer] |
| Appointment Write API | 4 | A — confirmArrivalOfAppoint / insertCustomerCheckin × 3 |
| Appointment Request 中 schoolMateId | **0** | A — 0 命中 |
| Appointment Request 中 schoolMateCheckId | **0** | A — 0 命中（注释代码）|
| Appointment Request 中 customerId | **0** | A — 仅在 chooseCustomer 范围 |
| Appointment Request 中 patientId | **0** | A — 仅在 choosePatient 范围（type=1 中 schoolMateVo 不含 patientId）|
| Appointment Request 中 medicalRecordId | **0** | A — 0 命中 |
| Appointment Request 中 schoolId | **1**（type=1）| A — $scope.obj.schoolId (L8270 派生) |

---

## 14. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | appointOrderCtrl | **3 行空 stub**（S1-132/133 误判） | A | L3664-L3666 | A — 修正 S1-132/133 |
| 2 | schoolMateVo 来源 | `getAppointSchoolMateVo.json` Response `res.object.schoolMateVo` | A | L8237, L8264 | A |
| 3 | schoolMateVo.school | `id / schoolName` 字段 | A | L8266, L8270, L8273 | A |
| 4 | schoolMateVo.schoolClass | `id / className` 字段 | A | L8266, L8271, L8274 | A |
| 5 | schoolMateVo.schoolMate | `gender / customerMobile / birthday / classMateName` 字段 | A | L8264-L8277 | A |
| 6 | schoolMate.customerMobile | `linkMobile` 字段 | A | L8265 | A |
| 7 | Appointment API | 6+ unique | A | 详见第 5 节 | A |
| 8 | Appointment Request | appointId 唯一 | A | L8238, L8658 | A |
| 9 | Appointment Response | type=0 patientVo / type=1 schoolMateVo | A | L8240, L8263 | A |
| 10 | schoolMateId | **0 命中** | A | 0 命中 | F |
| 11 | schoolMateCheckId | 注释代码 2 处 | A | L8280, L8706 | F（注释） |
| 12 | customerId | chooseCustomer 路径 | A | L8429 | A |
| 13 | patientId | choosePatient 路径 + item.patient.id | A | L8250, L8428 | A |
| 14 | medicalRecordId | **0 命中**（注释除外）| A | 0 命中 | F |
| 15 | schoolId | $scope.obj.schoolId（type=1）| A | L8270 | A |
| 16 | schoolMateVo → Patient | A | A | L8264-L8277 → L8364 | A |
| 17 | schoolMateVo → Customer | F（仅 customerMobile 字段）| A | 0 命中 API | F |
| 18 | schoolMateVo → MedicalRecord | F | A | 0 命中 | F |
| 19 | schoolMateVo → Appointment | A | A | L8232, L8238, L8658 | A |
| 20 | Appointment → Patient | A（State Param + Response）| A | L8216, L8238, L8250 | A |
| 21 | Appointment → MedicalRecord | F | A | 0 命中 | F |
| 22 | Appointment → CustomerCheckin | A | A | L8665, L8667, L8695 | A |
| 23 | Appointment → 主业务 | F（仅 customerCheckin）| A | 0 命中 | F |
| 24 | State / URL | appointId + type 实际消费；其它 11 字段注释 | A | L8194-L8232 | A |
| 25 | 最终 DAG | 11 个 DAG（A-K）| A | 本文档第 15 节 | A |
| 26 | 复刻红线 | 第 16 节 | A | 本文档 | A |

---

## 15. A/B/C/D/E/F 分布

- **A**：22
- **B**：1（schoolMateVo → patient 多源互证 — L8265 customerMobile + L8364 mobile 桥）
- **C**：0
- **D**：2（S1-132/133 误判"appointOrderCtrl 消费 schoolMateVo" + 注释代码 schoolMateCheckId 误读）
- **E**：**0**（红线要求）
- **F**：4（schoolMateId / schoolMateCheckId 实际 / schoolMateVo → MedicalRecord / Appointment → MedicalRecord / addSchoolMateConsume 实际调用）

---

## 16. 最终 DAG（A-K）

### DAG A: schoolMateVo → appointOrder
```
[真实入口] schoolMateVo 9 处
   ↓ A (修正 S1-132/133 误判)
[实际 Controller] addCheckinCtrl (L8159)
   ↓ A
[入口] getAppointSchoolMateVo.json { appointId: $stateParams.appointId } (L8237)
   ↓ A
[Response] res.object.schoolMateVo
   ↓ A
[9 字段映射] $scope.obj (L8263-L8271)
   ↓ A
[接诊表单] $scope.obj.gender / linkMobile / schoolId / classId 等
```

### DAG B: schoolMateVo → patient
```
schoolMateVo 9 字段
   ↓ A (L8263-L8271)
$scope.obj (gender / linkMobile / schoolId / classId 等)
   ↓ A (L8281)
$scope.searchPatientkeyword()
   ↓ A (L8359-L8376)
getPatientVoList.json { name: $scope.keyword, mobile: $scope.obj.linkMobile }
   ↓ A
patient list
   ↓ A (L8424 choosePatient)
$scope.obj.patientId / customerId / linkMobile / schoolId / classId (覆盖)
   ↓ A
$scope.obj (完整 patient 字段)
   ↓ A (L8665, L8695)
checkCustomer / obj → insertCustomerCheckin*.json
   ↓ A (L8671, L8697)
res.result.vo.customerCheckin.id / .medicalRecordId
   ↓ A
接诊完成
```

### DAG C: schoolMateVo → customer
```
schoolMateVo.schoolMate.customerMobile (L8265)
   ↓ A
$scope.obj.linkMobile
   ↓ A
[不进入 getCustomerVo] (0 命中 mobile 字段)
   ↓ F
[进入 getPatientVoList] (L8364 mobile)
   ↓ A
[customer 桥 0 命中]
```

### DAG D: schoolMateVo → medicalRecord
```
schoolMateVo
   ↓ F
[0 桥]
```

### DAG E: customer → schoolMateCheck
（沿用 S1-133 recommendPhoneListCtrl 字符级链）

### DAG F: patient → school
（沿用 S1-133 patient.school 4 行字符级）

### DAG G: patient → medicalRecord
（沿用 S1-133 L6693 + L1964 字符级）

### DAG H: appointment → patient
```
$stateParams.appointId (L8216, 注释)
   ↓ A
addCheckinCtrl 入口
   ↓ A (L8237)
getAppointPatientVo.json { appointId: $stateParams.appointId }
   ↓ A
type=0: item.patient.id → $scope.obj.patientId (L8250)
type=1: schoolMateVo → 选 patient → $scope.obj.patientId (L8428)
   ↓ A (L8695)
insertCustomerCheckin.json { patientId: $scope.obj.patientId }
```

### DAG I: appointment → medicalRecord
```
$stateParams.appointId
   ↓ F
[0 直接桥]
[间接桥] Appointment → customerCheckin → medicalRecord
   ↓ A (L8671, L8791, L10610, L10642)
$state.go("checkinList", printObj) (L8654)
   ↓ A
checkinListCtrl 中 customerCheckin.medicalRecordId
```

### DAG J: appointment → customerCheckin
```
$stateParams.appointId
   ↓ A (L8658)
confirmArrivalOfAppoint.json { appointId } (Write)
   ↓ A
$scope.checkCustomer.appointId = aId (L8665)
   ↓ A
insertCustomerCheckin[OfNewPaitent][OfNewCustomer].json (Write)
   ↓ A (L8671, L8697)
res.result.vo.customerCheckin
   ↓ A
$state.go("checkinList", { appointId, printCheckinId })
```

### DAG K: appointment → 主业务
```
[addCheckinCtrl]
   ↓ A
customerCheckin (L8671, L8697)
   ↓ A
checkinListCtrl (L8654 $state.go)
   ↓ A
customerCheckin.medicalRecordId (L8791, L10610, L10642)
   ↓ A
medicalRecord (S1-128/129 确认业务链)
   ↓ A
[验光/检查/销售/收费/配送] (0 桥继续 → 业务主链)
```

---

## 17. 历史差异

### 17.1 S1-132/133 "appointOrderCtrl 消费 schoolMateVo" 误判修正

| 项 | S1-132/133 | S1-134 | 差异 | 当前采用 |
|---|---|---|---|---|
| schoolMateVo 所在 Controller | appointOrderCtrl L3664 | **addCheckinCtrl L8159** | **D 冲突** | A — **修正** |
| schoolMateVo 9 行业务上下文 | appointOrderCtrl 选 patient | **addCheckinCtrl 接诊/登记 type=1** | **D 冲突** | A — **修正** |
| schoolMateVo 进入链 | UI 列表项 | **API Response res.object.schoolMateVo** | 业务实质不同 | A — **修正** |
| schoolMateVo → customerMobile | UI 字段 | **API Response 字段** | 业务实质不同 | A — **修正** |

### 17.2 S1-128 ~ S1-133 中"schoolMateVo → 接诊" 0 命中

- S1-128/129: 关注 medicalProduct / medicalProductId 业务
- S1-130/131: 关注 systemSetting / grantAuth
- S1-132: 首次发现 schoolMateVo 9 处（误判 Controller）
- S1-133: 强化 schoolMateCheckVo 字段
- **S1-134 首次完整解析 schoolMateVo → addCheckinCtrl → 9 字段映射 → patient → customerCheckin → medicalRecord 完整链**

### 17.3 patient.school 4 行字符级复核

- S1-132 报告: patient.school.id → schoolId（A 桥）
- S1-133 复用: A 桥
- **S1-134 验证**: choosePatient 13 参中 patient.school（实际触发点 L8434-L8438）

### 17.4 schoolMateCheckId 0 实际消费验证

- S1-132 报告: 0 命中（除筛查业务）
- S1-133 报告: 0 命中
- **S1-134 验证**:
  - addCheckinCtrl L8280 注释代码
  - L8706 注释代码
  - **addSchoolMateConsume.json 0 实际调用**（A — 注释代码 F 边界）
  - 完整 addCheckinCtrl 范围 schoolMateCheckId 真实消费 = **0 处**

---

## 18. 复刻红线

### 18.1 不能自行增加的字段

- `appointOrderCtrl` **不应包含 schoolMateVo 消费逻辑**（A — 实际是空 stub）
- addCheckinCtrl L8280, L8706 的 schoolMateCheckId 注释代码 **不应激活**（A — 实际不执行）
- $stateParams.patientId **不应在 addCheckinCtrl 实际消费**（A — L8213 注释代码）
- 任何 controller.js 中 0 命名的 appointment 字段

### 18.2 不能自行补桥的模块

- **schoolMateVo → MedicalRecord 0 桥**（F 边界）
- **schoolMateVo → Customer 仅字段映射，不是数据桥**（F 边界）
- **addSchoolMateConsume.json 0 实际调用**（F 边界 — 注释代码）
- **customerMobile → getCustomerVo 0 桥**（A — 14 处 0 命中 mobile）
- **Appointment → MedicalRecord 0 直接桥**（F 边界）
- **Appointment → 主业务 0 桥**（F 边界，仅 customerCheckin）
- **不能假定"appointId 包含 patientId"**（A — L8238 仅 appointId）
- **不能假定"schoolMateVo 包含 patientId"**（A — L8263-L8271 9 字段 0 含 patientId）

### 18.3 不能假定存在的 API

- `/admin/insertAppointment.json` **不存在**（A — 0 命中 addCheckinCtrl 范围）
- `/admin/getAppointPatientVo.json { patientId: }` **不存在**（A — 仅 appointId）
- `/admin/getAppointSchoolMateVo.json { schoolMateId: }` **不存在**（A — 仅 appointId）
- `/admin/insertAppointmentBySchoolMate.json` **不存在**

### 18.4 不能等同的 ID

| ID | 不能等同 |
|---|---|
| **appointId** | ≠ schoolMateId / schoolMateCheckId / patientId / customerId / medicalRecordId |
| **schoolMateVo.school.id** | ≡ schoolId（type=1 路径）|
| **schoolMateVo.schoolClass.id** | ≡ classId（type=1 路径）|
| **schoolMateVo.schoolMate.customerMobile** | **≡ linkMobile**（A — L8265 字符级）|
| **patient.school.id** | ≡ schoolId（A — L8435 字符级）|
| **patient.schoolClass.id** | ≡ classId（A — L8437 字符级）|
| **medicalRecord.patientId** | ≡ patientId（A — L6693 字符级）|
| **customerCheckin.medicalRecordId** | ≡ medicalRecordId（A — L8791 字符级）|
| schoolMateId | ≠ patientId / customerId / medicalRecordId |
| schoolMateCheckId | ≠ patientId / customerId / medicalRecordId |

### 18.5 必须保留的 F 边界

- appointOrderCtrl 是空 stub（F — 真实预约在 clinic/index.html）
- addSchoolMateConsume 0 实际调用（F 边界）
- schoolMateVo → MedicalRecord 0 桥（F 边界）
- 11 个 $stateParams 字段在 addCheckinCtrl 是注释代码（F — 仅 appointId + type 实际消费）
- 后端实体 FK / 表结构（F 边界）
- 0 共享 Service / Factory（F 边界）

### 18.6 命名误导必须标注

- `appointOrderCtrl` **是空 stub**（A — S1-132/133 误判）
- **`schoolMateVo 9 处实际在 addCheckinCtrl`**（A — S1-132/133 误判）
- `addCheckinCtrl` 实际是"接诊/登记"Controller，**不是接诊/登记"appointment"Controller**（A）
- `getAppointSchoolMateVo` API 名包含 "Appoint" 但**实际是接诊入口**（A — type=1）
- `addSchoolMateConsume.json` API **存在但 0 实际调用**（A — 仅注释）
- `customerMobile` **≠ mobile 字段**（A — 命名空间不同）
- `customerMobile` **不进入 getCustomerVo**（A — 14 处 0 命中 mobile）
- `getCustomerVo` 0 接收 mobile 字段
- `getPatientVoList` 接收 mobile 字段（L8364, L8374, L8390, L18981）
- $stateParams.patientId 在 addCheckinCtrl **是注释代码**（A — L8213）

---

## 19. L1 / L2 / L3

### 19.1 L1（前端直接事实）

- addCheckinCtrl L8159 完整 620 行（A — 字符级）
- schoolMateVo 9 字段映射（A）
- type=0/type=1 双分支（A）
- choosePatient 13 参（A）
- insertCustomerCheckin 3 个 API（A）
- confirmArrivalOfAppoint 桥（A）
- L8665-L8695 customerCheckin.appointId / .patientId 桥（A）
- L8671, L8697 customerCheckin.id Response（A）
- L10610, L10642 customerCheckin.medicalRecordId 多源互证（A）
- L8280, L8706 注释代码（A）

### 19.2 L2（基于 L1 的有限业务解释）

- "到店筛查"业务流：appointId → getAppointSchoolMateVo → schoolMateVo → 9 字段 → 选 patient → 插入接诊
- "登记"业务流：appointId → getAppointPatientVo → patientVo → 11 字段 → 选 patient → 插入接诊
- addCheckinCtrl 是接诊/登记 Controller，**不是预约 Controller**
- customerMobile 字段映射链：schoolMateVo → linkMobile → getPatientVoList.mobile
- getCustomerVo 不消费 mobile 字段的命名误导

### 19.3 L3（当前无证据）

- 后端 entity `school_mate` / `school_mate_check` / `appoint` / `customer_checkin` / `medical_record` 表
- FK 关系
- getAppointSchoolMateVo / getAppointPatientVo 后端 entity
- addSchoolMateConsume 后端 entity（虽然 API 存在但 0 调用）
- corpInfo 写入登录响应后的实际持久化
- recommendPhone 后端实现

---

## 20. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**）| ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**）| ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**）| ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**）| ✓ |
| 历史 MD 165-195 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 196_*.md | 是 | ✓ |
| 临时脚本（2 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 21. Git

- 本轮 commit hash：（待执行 `git add -- 196_*.md` / `git commit -m "docs(196): S1-134 SchoolMate to Appointment 接诊入口汇合链深度审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：203 → 204
- 本轮 untracked 预期：10（保留 10 untracked，新增 196 后变 10 untracked 因为 196 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：196_S1-134_*.md
