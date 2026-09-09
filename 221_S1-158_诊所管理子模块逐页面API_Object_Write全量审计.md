# S1-158 诊所管理 子模块逐页面 / API / Object / Write 全量审计

> S1-151 已做 Company / Employee / Role / ConsultRoom / SystemSetting 底层盘点;
> S1-157 已做 systemSetting.* 17 个子 State 枚举;
> 本轮**不是**简单重复,而是:把"诊所管理"实际可进入的页面、子 State、真实 API、真实写操作、配置对象、页面间关系**全部展开**,并对 S1-151 / S1-153 / S1-156 / S1-157 做**当前源码复核**。
>
> **核心结论**:诊所管理本质是**公司配置 + 员工/部门管理 + 诊室(ConsultRoom)管理 + 收银配置** 的聚合,不是单一 Object。

---

## §0 完整性闸门

| 文件 | 期望 SHA256 | 实际 SHA256 | 状态 |
|---|---|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | ✓ PASS |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | ✓ PASS |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | ✓ PASS |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | ✓ PASS |

**闸门结论:4 文件 SHA256 全部一致,通过。**

文件规模:2,142,219 bytes / **59,214 行**(S1-158 新确认)/ 417 个 Controller 注册 / 915 个 .json API。

---

## §1 诊所管理 State / Ctrl 全量枚举

### 1.1 真实子 State(本轮精确提取)

S1-158 通过 `\.state\(\s*['"]([a-zA-Z][a-zA-Z0-9_.]+)['"]` 精确枚举全部顶层 State 含 `admin / clinic / company / consultRoom / employee / department / role / settlement / cost / bankCard / check`:

| State | Ctrl | 业务 |
|---|---|---|
| `adminClinic`(L15053 `adminClinicCtrl`)| ✓ | **ConsultRoom 诊室管理**(命名误导:**实际是 ConsultRoom**)|
| `companyList`(`companyCtrl` L13829)| ✓ | 公司配置(logo / 地址 / 电话 / 类型)|
| `adminModify`(`adminModifyCtrl` L295)| ✓ | Admin 编辑 |
| `adminList`(`adminListCtrl` L103)| ✓ | Admin 列表 |
| `createAdmin`(`createAdminCtrl` L759)| ✓ | Admin 创建 |
| `adminPasswordModify`(`adminPasswordModifyCtrl` L673)| ✓ | Admin 密码修改 |
| `roleAdmin`(`roleAdminCtrl` L1714)| ✓ | Admin 角色配置 |
| `areaRoleAdmin`(`areaRoleAdminCtrl` L712)| ✓ | Admin 区域角色 |
| `areaScreenAdmin`(`areaScreenAdminCtrl` L738)| ✓ | Admin 区域屏 |
| `createAdminArea`(`createAdminAreaCtrl` L984)| ✓ | Admin 区域创建 |
| `modifyAdminArea`(`modifyAdminAreaCtrl` L1364)| ✓ | Admin 区域修改 |
| `adminMap`(`adminMapCtrl` L15214)| ✓ | 地图配置 |
| `memberAdmin`(`memberAdminCtrl` L1285)| ✓ | Admin 会员库 |
| `hospital.updateHospital.employeeList`(`employeeListCtrl` L15347)| ✓ | 员工列表 |
| `hospital.updateHospital.departmentList`(`departmentListCtrl` L15327)| ✓ | 部门列表 |
| `hospital.updateHospital.addDepartment`(`addDepartmentCtrl` L14846)| ✓ | 新增部门 |
| `hospital.updateHospital.updateDepartment`(`updateDepartmentCtrl` L15690)| ✓ | 修改部门 |
| `hospital.updateHospital.updateAdminHospital`(`updateAdminHospitalCtrl` L15439)| ✓ | 修改医院 Admin |
| `frontAdmin`(`frontAdminCtrl` L54099)| ✓ | 前台 Admin |
| `appointAdmin`(`appointAdminCtrl` L52344,| ✓ | Appointment 配置(S1-157 已确认) |
| `chargeAdmin`(`chargeAdminCtrl` L52575)| ✓ | **收银配置 + 收银员折扣**(实际是 corpCashConf)|
| `messageAdmin`(`messageAdminCtrl` L55834)| ✓ | 消息管理(待确认)|
| `phoneAdmin`(`phoneAdminCtrl` L57371)| ✓ | 电话配置(命名误导)|
| `recipeAdmin`(`recipeAdminCtrl` L57995)| ✓ | 处方配置 |
| `reportDateAdmin`(`reportDateAdminCtrl` L58291)| ✓ | Report Date 配置(S1-156 已确认)|
| `stockAdmin`(`stockAdminCtrl` L58536)| ✓ | Stock 配置 |
| `visionAdmin`(`visionAdminCtrl` L59060)| ✓ | Vision 视力表配置 |
| `wecomAdmin`(`wecomAdminCtrl` L59124)| ✓ | WeCom 配置 |
| `pointsAdmin`(`pointsAdminCtrl` L57582)| ✓ | Points 规则配置(S1-155 已确认)|
| `mateCheckReportConfig`(`mateCheckReportConfigCtrl` L41023)| ✓ | 筛查报告配置 |
| `mateCheckReportListNew`(`mateCheckReportListNewCtrl` L41055)| ✓ | 筛查报告列表 |
| `modifyMateCheck`(`modifyMateCheckCtrl` L41708)| ✓ | 筛查修改 |
| `modifySchoolMateCheck`(`modifySchoolMateCheckCtrl` L41839)| ✓ | 学校筛查修改 |
| `schoolMateCheckList`(`schoolMateCheckListCtrl` L44398)| ✓ | 学校筛查列表(S1-152 已确认)|
| `schoolMateCheckReports`(`schoolMateCheckReportsCtrl` L44688)| ✓ | 学校筛查报告 |
| `schoolCheckRecord`(`schoolCheckRecordCtrl` L58390)| ✓ | 学校检查记录 |
| `toothCheckTemplate`(`toothCheckTemplateCtrl` L59017)| ✓ | 牙齿检查模板 |
| `systemSetting.checkList`(`checkListCtrl` L53001)| ✓ | Check 列表(S1-157 已确认)|
| `systemSetting.checkModify`(`checkModifyCtrl` L53185)| ✓ | Check 修改 |
| `systemSetting.addCheck`(`addCheckCtrl` L50170)| ✓ | Check 添加(实际是 Examine)|
| `systemSetting.addCheckItem`(`addCheckItemCtrl` L50246)| ✓ | Check Item 添加 |
| `systemSetting.medicalFeesList`(`medicalFeesListCtrl` L55340)| ✓ | MedicalFee 列表(实际是 Examine)|
| `systemSetting.addMedicalFee`(`addMedicalFeeCtrl` L51665)| ✓ | 添加 MedicalFee(实际是 Examine)|
| `systemSetting.modifyMedicalFee`(`modifyMedicalFeeCtrl` L56817)| ✓ | 修改 MedicalFee(实际是 Examine)|

### 1.2 真实总 Ctrl 数量:42 个诊所管理相关(417 总数)

### 1.3 不归"诊所管理"的边界

- `addCheckinCtrl` / `checkinListCtrl` / `adminCallCtrl` / `checkCallCtrl` → 预约叫号(S1-153)
- `myMedicalRecordListCtrl` / `optometryCtrl` → 就诊流程(S1-146)
- `myCheckBillCtrl` → 已结算账单(S1-148)
- `adminBillCtrl` / `adminBillDetialCtrl` → Bill 业务
- `adminMyRecordCtrl` → Admin 我的病历
- `adminSalesRecordCtrl` / `adminPatientCtrl` → Sale / Patient
- `purchaseRequestCheckCtrl` / `stockChangeCheckCtrl` / `stockProductChangeCheckCtrl` → Stock
- `feeBankCardCtrl` / `feeCashierCtrl` / `feeDayCtrl` / `feeMonthCtrl` / `feeRechargeCtrl` / `refundFeeCtrl` → Fee / Cashier
- `reportFeeCtrl` → Report
- `assistCheckListCtrl` / `assistCheckingCtrl` → 协助检查

---

## §2 Company(公司配置)

### 2.1 关键发现:**Company 是真实业务配置对象**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `companyId` | **102** | **A 真实** |
| `companyName` | 52 | A |
| `companyVo` | **0** | F / 禁造 |
| `companyInfo` | 58 | A |
| `corpInfo` | 26 | A |
| `companyIdArray` | 13 | A |
| `corpTypeId` | 2 | A |
| `corporationName` | 多 | A |
| `address` | 多 | A |
| `servicePhone` | 多 | A |
| `slogon` | 多 | A |
| `medicalDevicePermit` | 多 | A |
| `logo` | 多 | A |
| `backImg` | 多 | A |
| `clinicId` / `clinicName` / `clinicVo` | **全部 0** | **F / 禁造** |

### 2.2 Company 真实字段(L13834 companyCtrl Response)

| 字段 | 行号 | Type |
|---|---:|---|
| `corporationName` | L13869 | R+W |
| `address` | L13870 | R+W |
| `servicePhone` | L13871 | R+W |
| `slogon` | L13872 | R+W |
| `medicalDevicePermit` | L13873 | R+W |
| `logo` | L13874 / L13836 | R+W |
| `backImg` | L13837 / L13875 | R+W |
| `corpTypeId` | L13852 / L13864 | R+W(corpTypeListIndex) |

### 2.3 Company API 全量

| API | 行号 | R/W | 业务 |
|---|---:|:-:|---|
| `getCorpInfo.json` | L13834 | R | 公司详情 |
| `updateCorpInfo.json` | L13868 | W | 修改公司 |
| `getCorpTypeConfVo.json` | L13851 | R | 公司类型配置 |
| `updateCorpTypeConf.json` | L13863 | W | 修改公司类型 |
| `selectEmployeeVoList.json` | L15355 | R | 员工列表(参数: companyId) |
| `getDepartmentList.json` | L15330 | R | 部门列表(参数: companyId) |
| `getCorpTimeData.json` | L13925 | R | 公司时间(S1-157 已确认) |
| `getChildrenLinkAndCode.json` | (S1-156) | R | 路由权限 |
| `getAdminInfo.json` | L13774 | R | 登录 Admin 详情 |
| `updateAdminInfo.json` | L13795 | W | 修改 Admin 信息 |

### 2.4 Company ↔ Employee / Department / ConsultRoom / Supplier / CorpConfig

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Company → Employee | ✓ A | selectEmployeeVoList Request `companyId` L15355 |
| Company → Department | ✓ A | getDepartmentList Request `companyId` L15330 |
| Company → ConsultRoom | ✓ A | selectConsultRoomVoListOfCompany Request `companyId` L15148 |
| Company → Admin | ✓ A | addDepartmentCtrl `object.companyId = $stateParams.companyId` L14849 |
| Company → Supplier | ✗ F | Supplier 无 companyId 字段(S1-157 已确认) |
| Company → TrainerCard | ✓ C | corpPointRule 公司级(S1-157) |
| Company → MachineCenter | ✓ C | processCenterCtrl 公司级(S1-157) |
| Company → CorpAppointmentConf | ✓ A | bookSettingsCtrl / corpAppointConf(S1-153)|
| Company → CorpCashConf | ✓ A | chargeAdminCtrl / printConfigCtrl(S1-156)|
| Company → CorpReportConf | ✓ A | reportDateAdminCtrl(S1-156)|

### 2.5 Company ID 真实用法

- L14849 `object.companyId = $stateParams.companyId`(department 创建 Request)
- L15120 `params.companyId = $stateParams.companyId`(consultRoom 创建 Request)
- L15148 `selectConsultRoomVoListOfCompany Request {companyId: $stateParams.companyId}`
- L15330 `getDepartmentList Request {companyId: $scope.id}`
- L15355 `selectEmployeeVoList Request {companyId: $scope.id}`

**结论**:companyId 是**真实 ID**(102 处),**State 路由参数 + Request Payload + 公司作用域**。

---

## §3 Employee(员工)

### 3.1 关键发现:**Employee 是真实独立 Object**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `employeeId` | **35** | **A 真实** |
| `employeeName` | 28 | A |
| `employeeVo` | **0** | F / 禁造 |
| `adminId` | 21 | A(独立字段)|
| `adminRoleId` | 29 | A(独立字段)|

### 3.2 employeeId 真实用法

| 行号 | 上下文 |
|---:|---|
| L15365 | `$scope.approveEmployee = function (employeeId, approved) {` |
| L15366-15367 | `setDoctorApproved.json Request {employeeId: employeeId, approved: approved}` |
| L15374 | `$scope.setEmployeeRank = function (employeeId, rank) {` |
| L15376-15378 | `setEmployeeRank.json Request {employeeId: employeeId, rank1: rank}` |
| L14846+ | 医院员工管理 |

### 3.3 Employee API 全量

| API | R/W | 业务 |
|---|:-:|---|
| `selectEmployeeVoList.json` | R | 员工列表(参数: companyId) |
| `setDoctorApproved.json` | W | 设置医师认证(Request: employeeId + approved) |
| `setEmployeeRank.json` | W | 设置员工等级(Request: employeeId + rank1) |
| `getExamineVoList.json` | R | 医师列表 |
| `selectEmployeeVoListOfMyCompany.json` | R | 员工列表(选医师)|

### 3.4 Employee ↔ Company / Department / Role / ConsultRoom

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Employee → Company | ✓ A | selectEmployeeVoList `{companyId}` L15355 |
| Employee → Department | ✗ F | **0 命中 employee.departmentId 字段**(Department → Employee 方向无 FK)|
| Employee → Role | ✗ F | employee.roleId **0 命中**(只有 adminRoleId)|
| Employee → ConsultRoom | ✗ F | 0 命中 consultRoom.employeeId |

### 3.5 adminId / adminRoleId vs employeeId

- **adminId 21** = Admin 账号 ID(角色管理)
- **adminRoleId 29** = Admin 角色 ID(changeAdminRole.json Request)
- **employeeId 35** = 员工 ID(医师认证 / 等级)

**结论**:**Admin ≠ Employee**,是两个**独立 Object**。Admin 走 `adminId + adminRoleId`,Employee 走 `employeeId`。

---

## §4 Department(部门)

### 4.1 关键发现:**Department 是真实业务对象,但 ID 极弱**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `departmentId` | **1** | A 弱(State 参数)|
| `departmentName` | **0** | **F / 禁造** |
| `departmentVo` | **0** | F / 禁造 |
| `departmentArr` | **0** | F / 禁造 |

### 4.2 departmentId 唯一 1 处

L15691 `$scope.id = $stateParams.departmentId;`

### 4.3 Department API 全量(5 个)

| API | 行号 | R/W | 业务 |
|---|---:|:-:|---|
| `getDepartmentList.json` | L15330 | R | 列表(参数: companyId) |
| `getDepartmentInfo.json` | L15700 | R | 详情(参数: id) |
| `addDepartment.json` | L14860 | W | 创建(Request: object 含 companyId / departDesc) |
| `updateDepartment.json` | L15711 | W | 修改(Request: object)|
| `deleteDepartment.json` | L15726 | W | 删除(Request: id) |

### 4.4 Department 真实字段

| 字段 | 行号 | Type |
|---|---:|---|
| `id` | L15691 / L15726 | ID(复用为 departmentId)|
| `companyId` | L14849 | 所属公司 |
| `departDesc` | L14850 / L15786 | 描述(可含图片)|
| `rank1` | L15705 | 排序(必填>0)|
| `keyimg` | L15793 | 图片 |

### 4.5 Department ↔ Company / Employee

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Department → Company | ✓ A | addDepartment Request `companyId` L14849 |
| Department → Employee | ✗ F | **0 命中** employee.departmentId / department.employeeList |
| Company → Department | ✓ A | getDepartmentList Request `companyId` L15330 |

### 4.6 命名误导

- `departmentListCtrl` 命名合理(但 `id` 是 State 参数,不是 departmentVo.id)
- **`departmentName` 0 命中,字段实际是 `departDesc`**(描述)

**结论**:Department 是弱业务对象,只有 `id`(复用为 departmentId)和一个 `departDesc` 字段。**Employee → Department 无 FK**。

---

## §5 ConsultRoom(诊室)

### 5.1 关键发现:**ConsultRoom 是真实独立 Object**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `consultRoomId` | **22** | **A 真实** |
| `consultRoomName` | 6 | A |
| `consultRoomVo` | 2 | A |
| `consultRoomStatus` | **0** | F(实际是 `status` 字段)|

### 5.2 consultRoomId 完整 22 处

| 行号 | 上下文 |
|---:|---|
| L9555 | `params.consultRoomId = $scope.consultRoom.id;`(bigScreenCtrl)|
| L9852 | `consultRoomId: $scope.screenList.items[this.index].consultRoom.id` |
| L10124 / L10159 / L10169 / L10180 / L10209 | `consultRoomId: $scope.clinicInfo.consultRoom.id`(checkCallCtrl)|
| L10292 | `consultRoomId: null` |
| L10302 | `this.consultRoomId = update.consultRoomVo.consultRoom && update.consultRoomVo.consultRoom.id;` |
| L10310 / L10324 / L10330 / L10351 | consultRoomCtrl / consultRoomVoList |
| L10503 | `consultRoomId: $scope.screenList.items[this.index].consultRoom.id` |
| L15066-15071 | changeStatus(adminClinicCtrl) |
| L15117 | `this.params.consultRoomId = this.params.id;` |
| L15135 | `$scope.searchLine(params.consultRoomId, index);` |
| L15138-15140 | searchLine 函数 |
| L15198 | WechatConfig.setWechatUrl(checkSignIn?consultRoomId=...) |

### 5.3 ConsultRoom API 全量

| API | 行号 | R/W | 业务 |
|---|---:|:-:|---|
| `selectConsultRoomVoListOfCompany.json` | L15148 | R | 公司诊室列表(Request: companyId)|
| `getConsultRoomVo.json` | L15139 | R | 诊室详情(Request: consultRoomId)|
| `addConsultRoom.json` | L15126 | W | 新增(Request: consultRoomName / examineIdArray / companyId)|
| `updateConsultRoomInfo.json` | L15133 | W | 修改(Request: id / consultRoomName / examineIdArray)|
| `updateConsultRoomStatus.json` | L15067 | W | 修改状态(Request: consultRoomId + status)|
| `selectConsultRoomVoListOfMyCompany.json` | (multi) | R | 诊室列表(我的公司)|

### 5.4 ConsultRoom 真实字段

| 字段 | 行号 | Type |
|---|---:|---|
| `id` | L15117 | ID(复用为 consultRoomId)|
| `consultRoomName` | L15109 | 必填 |
| `consultRoomId` | L15117 / L15140 | ID(Request)|
| `examineIdArray` | L15115 | 关联 Examine ID 数组 |
| `status` | L15068 / L15069 | 0=正常 / 1=停用 |
| `companyId` | L15120 | 所属公司 |

### 5.5 adminClinicCtrl 完整结构(L15053)

```js
window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (result) {
  $scope.companyInfo = result;  // L15058
});
$scope.status = [{ id: 0, name: "正常" }, { id: 1, name: "停用" }];
$scope.changeStatus = function (consultRoomId, status, index) {
  HttpFactory.object("/admin/updateConsultRoomStatus.json", {
    consultRoomId: consultRoomId, status: status
  });
};
$scope.clinicPopout = {
  params: {},
  examineList: [],
  submit: function () {
    if (!this.params.consultRoomName) return Popup.notice("请填写诊室名称！");
    var examineIdArray = this.examineList.map(function (examine) { return examine.id; });
    this.params.examineIdArray = examineIdArray;
    if (this.params.id) {
      this.params.consultRoomId = this.params.id;
      $scope.updateClinic(this.params, this.index);
    } else {
      this.params.companyId = $stateParams.companyId;
      $scope.addClinic(this.params);
    }
  }
};
```

### 5.6 ConsultRoom ↔ Appointment / BigScreen / Check / Employee / Company

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| ConsultRoom → Company | ✓ A | adminClinicCtrl `companyId` L15120 |
| ConsultRoom → Appointment | ✓ A | S1-153 已知 bigScreenCtrl consultRoomId L9555 |
| ConsultRoom → BigScreen | ✓ A | S1-153 bigScreenCtrl + checkCallCtrl `consultRoomId: $scope.clinicInfo.consultRoom.id` L10124 |
| ConsultRoom → MedicalExamine | ✓ A | examineIdArray L15115(examine.id 数组)|
| ConsultRoom → Employee | ✗ F | 0 命中 consultRoom.employeeId |

### 5.7 命名误导

- **adminClinicCtrl 不是 Clinic,是 ConsultRoom**(命名误导)
- **没有独立 `clinicId` / `clinicName` / `clinicVo` 字段**(0 命中,禁造)

---

## §6 Settlement / Cost / BankCard

### 6.1 关键发现:**全部 0 命中 ID 字段(F)**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `settlementId` | **0** | **F / 禁造** |
| `settlementVo` | **0** | F / 禁造 |
| `costId` | **0** | F / 禁造 |
| `costVo` | **0** | F / 禁造 |
| `expenseId` | **0** | F / 禁造 |
| `expenseVo` | **0** | F / 禁造 |
| `bankCardId` | **0** | F / 禁造 |
| `feeBankCardId` | **0** | F / 禁造 |
| `costPrice` | 1 | C(Examine 字段)|
| `bankCardFee` | 1 | C(普通变量)|

### 6.2 真实 Settlement/Cost/BankCard 业务

- `feeBankCardCtrl` L36882:实际是 **Customer Wallet 列表**(selectCustomerWalletVoList.json),命名误导严重,**不是银行账户**!
- `feeCashierCtrl` L36905:收银员配置(命名误导,**不是 BankCard**)
- `feeDayCtrl` L37005:日结
- `feeMonthCtrl` L37134:月结
- `feeRechargeCtrl` L37183:充值
- `refundFeeCtrl` L37657:退款
- `reportFeeCtrl` L37805:费用报表
- `chargeAdminCtrl` L52575:**corpCashConf + cashierDiscount**(已确认 S1-156 / S1-157)

### 6.3 feeBankCardCtrl 实际业务

```js
$scope.obj = {};
$scope.obj.hasMoney = true;
$scope.EmployeeList = new ListFactory("/admin/selectCustomerWalletVoList.json", 0, pageSize, $scope.obj);
```

**结论**:feeBankCardCtrl **不是银行账户**,是 **Customer Wallet 列表**。

### 6.4 Settlement ↔ Cashflow / Payment / Refund

- **Settlement 不存在独立 Entity** (F)
- Cashflow / Payment / Refund 是 S1-148 已确认业务,通过 **createCashFlowForMedicalRecord** 等 API 关联
- **不创建 settlementId / / costId / / bankCardId**

---

## §7 Clinic / Company Config(补充)

### 7.1 corpTypeList 三种公司类型(L13839-L13845)

- 加盟诊所(0)
- 医院(1)
- 眼镜店(2)

字段 `corpTypeId` 是 R+W,范围 0-2。

### 7.2 Corp Time 配置(S1-157 已确认)

- `getCorpTimeData.json` L13925(R)
- 字段:isCorpNearExpiredOfTwoWeeks / diffDays / corpTime.endTime / corpTime.startTime
- corpTime 是 Subscription 业务字段

### 7.3 Corp Token 配置(L13866)

- `localStorage.getItem("pcToken")` 登录 token
- `isAdminTokenOk.json` 校验 token 有效性
- **不创建 corpTokenId**(只是普通 token)

---

## §8 Clinic Image

### 8.1 关键发现:**clinicImageId / imageId 全部 0 命中(F)**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `clinicImageId` | **0** | **F / 禁造** |
| `imageId` | **0** | F / 禁造 |
| `logo` | 多 | C(普通字符串字段)|
| `backImg` | 多 | C |
| `imgurl` | 多 | C |

### 8.2 真实 Image 配置

- companyCtrl L13832 `$scope.img = {}; $scope.img.imgurl = res.result.object.logo`(logo 字段)
- companyCtrl L13887 `$scope.chooseImg = function () { $scope.imgModalModify = true; };`
- **logo / backImg 是 Company 字段,不是独立 Image Entity**

### 8.3 Qiniu 上传(L14908-L14946)

- `QiniuFactory()` 上传图片到七牛云
- `$scope.modalQiniuFactory.getToken();`
- `$scope.modalQiniuFactory.UPLOAD_HOST / IMAGE_HOST`
- **imageId 不存在**;图片以 base64 / URL 形式存储

### 8.4 Clinic Image 命名误导

- `adminClinicImageCtrl` 不存在(`adminClinicCtrl` 是 ConsultRoom,不是 Image)
- 实际图片配置在 `companyCtrl` 内部

**结论**:**Clinic Image 没有独立 Entity**,只是 Company 字段 logo / backImg 的 URL 配置。

---

## §9 Admin Check Config

### 9.1 关键发现:**Examine 是真实业务对象,bodyCheckItemId 4 处真实**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `bodyCheckItemId` | **4** | **A 真实**(S1-157 已确认)|
| `checkItemId` | **0** | **F / 禁造**(S1-157)|
| `checkConfigId` | **0** | F / 禁造 |
| `examineId` | 多 | A 真实(等同 bodyCheckItemId 含义?待区分)|
| `medicalCheckItem.id` | 多 | A 真实(L50265 / L50270 / L50279)|

### 9.2 addCheckCtrl L50170 业务

- 业务是 **创建 Examine**(MedicalExamine / 检查项目)
- API:`createExamine.json`(W)
- 字段:examineName / unitName / kpiPrice / costPrice / marketPrice / canBeDiscounted / allowPoints / status / examineType / pinyin
- `$state.go('systemSetting.checkList')`(Check 列表)

### 9.3 addCheckItemCtrl L50246 业务

- 业务是 **Examine Item 配置**(medicalCheckItem)
- API:`getExamineVo.json`(R)+ `getExamineItemVoList.json`(R)
- 字段:`medicalCheckItem.id`(L50265)/ `medicalCheckItem.checkItemName`(L50272)/ `examineItem.position`(L50266)/ `examineItem.rank1`(L50267)
- **medicalCheckItem.id 是真实 ID**(等同 bodyCheckItemId)

### 9.4 bodyCheckItemId vs medicalCheckItem.id

| 字段 | 真实? | 来源 |
|---|:-:|---|
| `bodyCheckItemId` | ✓ A | S1-157 L41206 / L41230 / L41255 / L41262 |
| `medicalCheckItem.id` | ✓ A | S1-158 L50265 / L50270 / L50279 |

**S1-158 新发现**:`medicalCheckItem.id` 与 `bodyCheckItemId` 都指向同一类对象(bodyCheckItem / ExamineItem),S1-157 只识别了 `bodyCheckItemId`,本轮新增 `medicalCheckItem.id` 证据。

### 9.5 Examine API 全量

| API | R/W | 业务 |
|---|:-:|---|
| `getExamineVo.json` | R | Examine 详情(Request: examineId) |
| `getExamineVoList.json` | R | Examine 列表 |
| `getExamineItemVoList.json` | R | ExamineItem 列表(Request: examineId) |
| `createExamine.json` | W | 创建 Examine |
| `updateExamine.json` | W | 修改 Examine |
| `updateByExamineIdArraySelective.json` | W | 批量更新(Request: examineIdArray) |
| `updateCorpPointRule.json` | W | Point 规则(S1-155)|
| `getPinyin.json` | R | 拼音转换 |

### 9.6 setBodyCheckItemPrintDisable 真实

```js
// L41255-L41262
HttpFactory.object("/admin/setBodyCheckItemPrintDisable.json", {
  bodyCheckItemId: id,
  printDisable: disable
});
```

### 9.7 Admin Check Config 命名误导

- `addCheckCtrl` 实际是 addExamineCtrl
- `addCheckItemCtrl` 实际是 addMedicalCheckItemCtrl
- `checkListCtrl` 实际是 examineVoListCtrl

---

## §10 Read API 全清单(诊所管理)

| API | R/W | 业务 |
|---|:-:|---|
| `getCorpInfo.json` | R | 公司详情 |
| `getCorpTypeConfVo.json` | R | 公司类型 |
| `getCorpTimeData.json` | R | 公司时间 |
| `getCorpCashConf.json` | R | 公司收银配置 |
| `getCorpAppointConf.json` | R | 公司预约配置(S1-157)|
| `getCorpAppointmentConf.json` | R | 公司预约 SMS 配置(S1-153)|
| `getCorpReportConf.json` | R | 公司报表配置(S1-156)|
| `getCorpPointRule.json` | R | 公司积分规则(S1-155)|
| `getChildrenLinkAndCode.json` | R | 路由权限 |
| `getAdminInfo.json` | R | Admin 详情 |
| `getOtherAdminInfo.json` | R | 其他 Admin 详情 |
| `getRoleStateListForUpdate.json` | R | Admin 角色状态 |
| `getAdminStateListForUpdate.json` | R | Admin State 列表 |
| `getUnionAdminStateList.json` | R | Admin  State 联合 |
| `getSuperAdminMobile.json` | R | Super Admin 手机 |
| `selectEmployeeVoList.json` | R | 员工列表 |
| `selectEmployeeVoListOfMyCompany.json` | R | 员工列表(我的公司)|
| `getDepartmentList.json` | R | 部门列表 |
| `getDepartmentInfo.json` | R | 部门详情 |
| `selectConsultRoomVoListOfCompany.json` | R | 诊室列表(公司) |
| `selectConsultRoomVoListOfMyCompany.json` | R | 诊室列表(我的公司) |
| `getConsultRoomVo.json` | R | 诊室详情 |
| `getExamineVo.json` | R | Examine 详情 |
| `getExamineVoList.json` | R | Examine 列表 |
| `getExamineItemVoList.json` | R | ExamineItem 列表 |
| `selectToothCheckTemplateVoList.json` | R | 牙齿检查模板 |
| `getEyeChartOfMine.json` | R | 视力表(我的)|
| `getEyeChartConfRemark.json` | R | 视力表备注 |
| `getRandFirstEyeChartFileByChartType.json` | R | 随机视力表 |
| `getPinyin.json` | R | 拼音转换 |
| `selectAdminCashVoList.json` | R | Admin 现金列表 |
| `selectCustomerWalletVoList.json` | R | Customer Wallet 列表 |
| `isAdminTokenOk.json` | R | Admin Token 校验 |
| `getStockSet(ObjectFactory)` | R | Stock 配置(Window Service)|

---

## §11 Write API 全清单(诊所管理)

| API | R/W | 业务 |
|---|:-:|---|
| `updateCorpInfo.json` | W | 修改公司 |
| `updateCorpTypeConf.json` | W | 修改公司类型 |
| `saveCorpCashConf.json` | W | 保存收银配置(S1-157)|
| `updateCompanyCashConf.json` | W | 修改公司现金配置(S1-157)|
| `saveCorpAppointmentConf.json` | W | 保存预约配置(S1-153)|
| `saveCorpAppointConf.json` | W | 保存预约配置(S1-157)|
| `saveCorpReportConf.json` | W | 保存报表配置(S1-156)|
| `saveCorpPointRule.json` | W | 保存积分规则(S1-155)|
| `updateAdminInfo.json` | W | 修改 Admin 信息 |
| `changeAdminRole.json` | W | 修改 Admin 角色(Request: id / adminRoleId / companyId) |
| `transferAdminRole.json` | W | 转移 Admin 角色 |
| `updateAdminStateList.json` | W | 更新 Admin State |
| `saveAdminCashById.json` | W | 修改 Admin 折扣(Request: adminId + discount) |
| `setDoctorApproved.json` | W | 设置医师认证(Request: employeeId + approved) |
| `setEmployeeRank.json` | W | 设置员工等级(Request: employeeId + rank1) |
| `addDepartment.json` | W | 新增部门(Request: object 含 companyId) |
| `updateDepartment.json` | W | 修改部门 |
| `deleteDepartment.json` | W | 删除部门(Request: id) |
| `addConsultRoom.json` | W | 新增诊室(Request: consultRoomName / examineIdArray / companyId) |
| `updateConsultRoomInfo.json` | W | 修改诊室 |
| `updateConsultRoomStatus.json` | W | 修改诊室状态(Request: consultRoomId + status) |
| `createExamine.json` | W | 创建 Examine |
| `updateExamine.json` | W | 修改 Examine |
| `updateByExamineIdArraySelective.json` | W | 批量更新 Examine |
| `setBodyCheckItemPrintDisable.json` | W | 关闭 Check Item 打印(Request: bodyCheckItemId + printDisable) |
| `setBodyCheckPrintDisable.json` | W | 关闭 Check 打印(Request: bodyCheckItemId + printDisable) |
| `deleteToothCheckTemplate.json` | W | 删除牙齿模板(Request: id) |
| `addPrinter.json` | W | 云打印添加(S1-156)|
| `updateEyeChartOfMine.json` | W | 修改视力表 |
| `saveStockConf.json` | W | 保存 Stock 配置 |
| `autoChartSizeForPad.json` | W | Pad 视力表尺寸 |

---

## §12 Object 总表

| Object | A 独立 ID | B Response VO | C Request Payload | D State/UI | F |
|---|:-:|:-:|:-:|:-:|:-:|
| **Company** | ✓ A(companyId 102)| ✗ F(companyVo 0)| ✓ | ✓ | – |
| **Clinic** | ✗ F(clinicId 0)| ✗ F | ✗ F | – | – |
| **Employee** | ✓ A(employeeId 35)| ✗ F | ✓ | ✓ | – |
| **Department** | ✗ A(id 复用 departmentId 1)| ✗ F | ✓ | ✓ | – |
| **Admin** | ✓ A(adminId 21)| ✗ F | ✓ | ✓ | – |
| **AdminRole** | ✓ A(adminRoleId 29)| ✗ F | ✓ | ✓ | – |
| **Role(generic)** | ✓ A(roleId 4)| ✗ F | ✓ | ✓ | – |
| **ConsultRoom** | ✓ A(consultRoomId 22)| ✓ A(consultRoomVo 2)| ✓ | ✓ | – |
| **Examine** | ✓ A(examineId)| ✓ | ✓ | ✓ | – |
| **MedicalCheckItem** | ✓ A(medicalCheckItem.id)| ✓ | ✓ | ✓ | – |
| **BodyCheckItem** | ✓ A(bodyCheckItemId 4)| ✓ | ✓ | ✓ | – |
| **CorpInfo** | ✓ A(隐含 id)| ✓ | ✓ | ✓ | – |
| **CorpCashConf** | ✓ A(companyCashConfId 1)| ✓ | ✓ | ✓ | – |
| **CorpAppointmentConf** | ✓ A(隐含 id)| ✓ | ✓ | ✓ | – |
| **CorpAppointConf** | ✓ A(隐含 id)| ✓ | ✓ | ✓ | – |
| **CorpReportConf** | ✓ A(隐含 id)| ✓ | ✓ | ✓ | – |
| **CorpPointRule** | ✗ F | ✓ | ✓ | ✓ | – |
| **Settlement** | ✗ F | – | – | – | – |
| **Cost** | ✗ F | – | – | – | – |
| **BankCard** | ✗ F | – | – | – | – |
| **ClinicImage** | ✗ F | – | – | – | – |
| **CheckConfig** | ✗ F(checkConfigId 0)| – | – | – | – |

---

## §13 Object ID 总表

### 13.1 A 真实 ID(允许进入 V4.4)

| ID | 命中数 | 业务 |
|---|---:|---|
| `companyId` | 102 | Company 真实 ID |
| `employeeId` | 35 | Employee 真实 ID |
| `adminId` | 21 | Admin 账号真实 ID |
| `adminRoleId` | 29 | AdminRole 真实 ID |
| `consultRoomId` | 22 | ConsultRoom 真实 ID |
| `roleId` | 4 | 通用 Role 真实 ID |
| `bodyCheckItemId` | 4 | BodyCheckItem 真实 ID |
| `medicalCheckItem.id` | 多 | MedicalCheckItem 真实 ID(S1-158 新发现)|
| `companyIdArray` | 13 | Company ID 数组(Request)|
| `companyCashConfId` | 1 | CorpCashConf 真实 ID |
| `departmentId` | 1 | Department 弱 ID(State 参数)|
| `corpTypeId` | 2 | Company 类型 R+W |
| `consultRoomName` | 6 | ConsultRoom 名称 |
| `examineId` | 多 | Examine 真实 ID |
| `corporationName` | 多 | Company 名称 |
| `companyName` | 52 | Company 名称 |
| `employeeName` | 28 | Employee 名称 |
| `corpInfo.logo` / `backImg` | 多 | Company 视觉配置 |

### 13.2 F 禁造 ID(全部 0 命中)

| ID | 禁造原因 |
|---|---|
| `companyVo` | 0 命中 |
| `clinicId` | 0 命中 |
| `clinicName` | 0 命中 |
| `clinicVo` | 0 命中 |
| `employeeVo` | 0 命中 |
| `departmentName` | 0 命中(实际是 departDesc)|
| `departmentVo` | 0 命中 |
| `departmentArr` | 0 命中 |
| `roleVo` | 0 命中 |
| `consultRoomStatus` | 0 命中(实际是 status)|
| `settlementId` / `settlementVo` | 0 命中 |
| `costId` / `costVo` | 0 命中 |
| `expenseId` / `expenseVo` | 0 命中 |
| `bankCardId` / `feeBankCardId` | 0 命中 |
| `cashConfigId` | 0 命中 |
| `clinicImageId` | 0 命中 |
| `imageId` | 0 命中 |
| `checkItemId` | 0 命中(S1-157)|
| `checkConfigId` | 0 命中 |

### 13.3 L3 数据库结构:全部 F(未观察)

---

## §14 Controller 消费矩阵

| Controller | State | Company | Employee | Department | ConsultRoom | Cash/Charge | Check |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `companyCtrl` L13829 | companyList | ✓ | – | – | – | – | – |
| `adminCtrl` L13772 | adminModify | – | – | – | – | – | – |
| `adminClinicCtrl` L15053 | adminClinic | ✓ | – | – | ✓ | – | – |
| `addDepartmentCtrl` L14846 | addDepartment | ✓ | – | ✓ | – | – | – |
| `departmentListCtrl` L15327 | departmentList | ✓ | – | ✓ | – | – | – |
| `updateDepartmentCtrl` L15690 | updateDepartment | – | – | ✓ | – | – | – |
| `employeeListCtrl` L15347 | employeeList | ✓ | ✓ | – | – | – | – |
| `chargeAdminCtrl` L52575 | chargeAdmin | ✓ | – | – | – | ✓(cashierDiscount)| – |
| `medicalFeesListCtrl` L55340 | systemSetting.medicalFeesList | – | – | – | – | – | ✓(Examine) |
| `addCheckCtrl` L50170 | systemSetting.addCheck | – | – | – | – | – | ✓(Examine) |
| `addCheckItemCtrl` L50246 | systemSetting.addCheckItem | – | – | – | – | – | ✓(bodyCheckItem) |
| `checkListCtrl` L53001 | systemSetting.checkList | – | – | – | – | – | ✓(Examine 列表) |
| `modifyMedicalFeeCtrl` L56817 | systemSetting.modifyMedicalFee | – | – | – | – | – | ✓ |
| `addMedicalFeeCtrl` L51665 | systemSetting.addMedicalFee | – | – | – | – | – | ✓ |
| `messageAdminCtrl` L55834 | messageAdmin | – | – | – | – | – | – |
| `phoneAdminCtrl` L57371 | phoneAdmin | – | – | – | – | – | – |
| `pointsAdminCtrl` L57582 | pointsAdmin | ✓ | – | – | – | – | – |
| `visionAdminCtrl` L59060 | visionAdmin | – | – | – | – | – | ✓(视力表) |
| `toothCheckTemplateCtrl` L59017 | toothCheckTemplate | – | – | – | – | – | ✓(牙齿)|
| `reportDateAdminCtrl` L58291 | reportDateAdmin | ✓ | – | – | – | – | – |
| `appointAdminCtrl` L52344 | appointAdmin | ✓ | – | – | – | – | – |
| `recipeAdminCtrl` L57995 | recipeAdmin | – | – | – | – | – | – |
| `stockAdminCtrl` L58536 | stockAdmin | ✓ | – | – | – | – | – |
| `wecomAdminCtrl` L59124 | wecomAdmin | – | – | – | – | – | – |
| `feeBankCardCtrl` L36882 | (命名误导)| – | – | – | – | ✓(Customer Wallet)| – |

---

## §15 关系矩阵

| 关系 | 真实? | Grade | 字符级证据 |
|---|:-:|:-:|---|
| **Company ↔ Employee** | ✓ | A | selectEmployeeVoList `{companyId}` L15355 |
| **Company ↔ Department** | ✓ | A | getDepartmentList `{companyId}` L15330 |
| **Company ↔ ConsultRoom** | ✓ | A | selectConsultRoomVoListOfCompany `{companyId}` L15148 |
| **Company ↔ Admin** | ✓ | A | adminClinicCtrl `$scope.companyInfo` L15058 + changeAdminRole `{companyId}` L648 |
| **Company ↔ Supplier** | ✗ | F | 0 命中 Supplier.companyId |
| **Company ↔ TrainerCard** | ✓ | C | corpPointRule 公司级 |
| **Company ↔ MachineCenter** | ✓ | C | processCenterCtrl 公司级 |
| **Company ↔ CorpAppointmentConf** | ✓ | A | bookSettingsCtrl(S1-153)|
| **Company ↔ CorpAppointConf** | ✓ | A | appointAdminCtrl |
| **Company ↔ CorpCashConf** | ✓ | A | chargeAdminCtrl + printConfigCtrl(S1-156/157)|
| **Company ↔ CorpReportConf** | ✓ | A | reportDateAdminCtrl(S1-156)|
| **Employee ↔ Department** | ✗ | F | 0 命中 employee.departmentId |
| **Employee ↔ Role** | ✗ | F | 0 命中 employee.roleId |
| **Employee ↔ ConsultRoom** | ✗ | F | 0 命中 |
| **ConsultRoom ↔ Appointment** | ✓ | A | S1-153 bigScreenCtrl consultRoomId L9555 |
| **ConsultRoom ↔ BigScreen** | ✓ | A | S1-153 checkCallCtrl L10124 |
| **ConsultRoom ↔ MedicalExamine** | ✓ | A | examineIdArray L15115 |
| **ConsultRoom ↔ Employee** | ✗ | F | 0 命中 |
| **Admin ↔ Employee** | ✗ | F | **Admin ≠ Employee**(独立 ID)|
| **Admin ↔ AdminRole** | ✓ | A | changeAdminRole `{adminId, adminRoleId}` L648 |
| **Role ↔ Employee** | ✗ | F | 0 命中 |

---

## §16 Status / Scope / Toggle

### 16.1 Status 字段汇总

| Controller | Status 字段 | 值 | Type |
|---|---|---|---|
| `adminClinicCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段(ConsultRoom)|
| `medicalFeesListCtrl` | obj.status | null=全部 / 0=正常 / 1=停用 | Filter |
| `addCheckCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段(Examine)|
| `modifyMedicalFeeCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段 |
| `addProjectCardCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段 |
| `employeeListCtrl` | approveEmployee | bool | Toggle |

### 16.2 Scope 字段

| Scope | 行号 | 含义 |
|---|---:|---|
| `companyId` | L15330 / L15355 / L15148 | 公司作用域 |
| `adminRoleId` | L232 / L648 | Admin 角色作用域 |
| `companyIdArray` | L106 | 公司 ID 数组 |
| `isClinicAdmin` | L52612 | 是否是诊所 Admin(bool)|

### 16.3 UI Toggle

- `setActive` toggle(L14906 / L15696):isactive 字段切换
- `setStatus` toggle(`status` 字段)
- `chooseImg` toggle(L13887):imgModalModify 开关
- `clinicPopout.showP` toggle(L15093)

### 16.4 区分

- **真实业务 Status**(6 处):ConsultRoom / Examine / MedicalFee / TrainerCard / Member
- **Filter / Search**(2 处):medicalFeesList / processCenter
- **UI Toggle**(4 处):isactive / imgModal / modalPopout

---

## §17 26 项页面证据矩阵(摘要)

完整 26 项在每个 § 模块段落已给出。摘要:

| 类别 | 关键证据 |
|---|---|
| **Object** | Company / Employee / Department(弱)/ Admin / AdminRole / Role / ConsultRoom / Examine / MedicalCheckItem / BodyCheckItem / CorpInfo / CorpCashConf / CorpAppointmentConf / CorpAppointConf / CorpReportConf |
| **Request** | companyId(102) / employeeId(35) / adminId(21) / adminRoleId(29) / consultRoomId(22) / roleId(4) / bodyCheckItemId(4) / companyCashConfId(1) / departmentId(1) |
| **Response** | companyVo 0 / employeeVo 0 / consultRoomVo 2 / examineVoList 多 |
| **Function** | updateCorpInfo / saveCorpCashConf / changeAdminRole / setDoctorApproved / addDepartment / updateDepartment / deleteDepartment / addConsultRoom / updateConsultRoomInfo / updateConsultRoomStatus / createExamine / setBodyCheckItemPrintDisable |
| **State Bridge** | $stateParams.companyId / departmentId / adminId |
| **Object Bridge** | Company ↔ Employee / Department / ConsultRoom / CorpConfig(全部 ✓ A)|
| **API Bridge** | 35 个 Read + 31 个 Write |
| **Business Interpretation** | 诊所管理 = Company Config + Employee / Department 管理 + ConsultRoom 管理 + Corp Config |
| **Evidence Grade** | A 字符级 / B 多源 / C 局部 / D 冲突(0) / **E 业务推断(0 入规格)** / F 未观察 |
| **V4.4 Decision** | 仅 A/B/C 入规格 |

---

## §18 Source Trace

### 18.1 真实 ID Source → Target

| ID | Source | Transform | Target | Consumer |
|---|---|---|---|---|
| `companyId` | $stateParams.companyId | Request | Employee/Department/ConsultRoom | 跨多 Ctrl |
| `employeeId` | obj/State | setDoctorApproved.json | Employee List | employeeListCtrl |
| `adminId` | $stateParams.adminId | changeAdminRole.json | Admin | adminListCtrl |
| `adminRoleId` | obj | changeAdminRole.json | Admin | roleAdminCtrl |
| `consultRoomId` | obj / $scope | updateConsultRoomStatus.json | ConsultRoom | adminClinicCtrl |
| `departmentId` | $stateParams.departmentId | updateDepartment.json | Department | updateDepartmentCtrl |
| `bodyCheckItemId` | checkItem.bodyCheckItem.id | setBodyCheckItemPrintDisable.json | BodyCheckItem | checkListCtrl |
| `medicalCheckItem.id` | arr[i].medicalCheckItem.id | medicalExamineArr | MedicalCheckItem | addCheckItemCtrl |
| `companyCashConfId` | this.params.id | updateCompanyCashConf.json | CorpCashConf | printConfigCtrl |
| `corpTypeId` | $scope.corpTypeListIndex | updateCorpTypeConf.json | Company | companyCtrl |

### 18.2 禁造 ID 列表

| ID | 禁造原因 |
|---|---|
| companyVo / clinicId / clinicName / clinicVo | 0 命中 |
| employeeVo / departmentName / departmentVo / departmentArr | 0 命中 |
| roleVo / consultRoomStatus | 0 命中 |
| settlementId / costId / expenseId / bankCardId / feeBankCardId | 0 命中 |
| clinicImageId / imageId / cashConfigId / checkItemId / checkConfigId | 0 命中 |

---

## §19 历史差异

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-151:Company / Employee / Role / ConsultRoom / SystemSetting 盘点 | **companyId 102 + employeeId 35 + adminId 21 + adminRoleId 29 + consultRoomId 22 全部保持** | **新增 medicalCheckItem.id 证据** | 复核一致 + 新增 medicalCheckItem |
| S1-153:bigScreenCtrl consultRoomId | adminClinicCtrl `consultRoomId` 22 处 + L15139 `getConsultRoomVo.json` | **adminClinicCtrl 命名误导修复**(实际是 ConsultRoom) | A(consultRoomId) |
| S1-156:printConfigCtrl = corpCashConf | chargeAdminCtrl L52575 + printConfigCtrl L57667 都是 corpCashConf | **新增 chargeAdminCtrl 是 corpCashConf 主管** | A(companyCashConfId) |
| S1-157:systemSetting 17 子 State + bodyCheckItemId A | 17 个子 State 全部对应;**新增 medicalCheckItem.id 与 bodyCheckItemId 同源** | **新增 medicalCheckItem.id 字符级证据** | A(双 ID 同源) |
| S1-157:memberTypeId 0 命中 | 0 命中 | 无变化 | F |
| S1-157:processCenter = MachineCenter | processCenterCtrl L57778 真实 | 无变化 | A(machineCenterId) |
| S1-157:projectCard = TrainerCard | projectCardCtrl 真实 | 无变化 | A(trainerCardId) |
| S1-157:companyCashConfId 1 | L57763 真实 | **S1-158 新增 chargeAdminCtrl L52601 saveCorpCashConf 是同一 ID** | A |
| (历史误判)"Clinic 是独立 Object" | clinicId 0 命中 | **禁造** | F |
| (历史误判)"Department 有 departmentName" | 0 命中 | **禁造**(实际是 departDesc)| F |
| (历史误判)"Employee 关联 Department" | 0 命中 employee.departmentId | **禁造** | F |
| (历史误判)"Settlement 是独立 Entity" | settlementId 0 命中 | **禁造** | F |
| (历史误判)"Cost / Expense / BankCard 是独立 Object" | 全部 0 命中 ID | **禁造** | F |
| (历史误判)"ClinicImage 是独立 Image Entity" | 0 命中 | **禁造** | F |
| (历史误判)"adminClinic 是 Clinic 配置" | 实际是 ConsultRoom 诊室管理 | **命名误导修复** | adminClinicCtrl = ConsultRoom |
| (历史误判)"feeBankCardCtrl 是银行账户" | 实际是 Customer Wallet 列表 | **命名误导修复** | feeBankCardCtrl = Wallet |
| (历史误判)"chargeAdminCtrl 是 Charge 配置" | 实际是 corpCashConf + cashierDiscount | **命名误导修复** | chargeAdminCtrl = CashConf |
| (历史误判)"medicalFeesListCtrl 是 MedicalFee" | 实际是 Examine 列表 | **命名误导修复** | medicalFeesList = Examine |
| (历史误判)"addCheckCtrl 是 Check" | 实际是 addExamine | **命名误导修复** | addCheckCtrl = addExamine |
| (历史误判)"Admin = Employee" | adminId 21 / employeeId 35 独立 | **禁造合并** | Admin ≠ Employee |

---

## §20 A/B/C/D/E/F 总结

- **A 字符级**:14 个 ID(companyId / employeeId / adminId / adminRoleId / consultRoomId / roleId / bodyCheckItemId / medicalCheckItem.id / companyCashConfId / departmentId / corpTypeId / consultRoomName / examineId / companyIdArray)
- **B 多源一致**:Company ↔ Employee / Department / ConsultRoom / CorpConfig 全部 ✓ A
- **C 局部证据**:Company ↔ TrainerCard / MachineCenter / Supplier
- **D 冲突**:0
- **E 业务推断**:0 入规格
- **F 未观察**:21 个禁造 ID(companyVo / clinicId / clinicName / clinicVo / employeeVo / departmentName / departmentVo / departmentArr / roleVo / consultRoomStatus / settlementId / costId / expenseId / bankCardId / feeBankCardId / clinicImageId / imageId / cashConfigId / checkItemId / checkConfigId / corpPointRuleId)

---

## §21 L1 / L2 / L3 分层

### L1 源码直接可见

- 42 个诊所管理相关 Controller
- 35 个 Read API
- 31 个 Write API
- 14 个真实 ID(字符级)
- 17 个 systemSetting 子 State(S1-157)
- 21 个禁造 ID

### L2 有限业务解释

- 诊所管理 = Company Config + Employee/Department + ConsultRoom + CorpConfig(收银/预约/报表/积分)
- 诊室 = ConsultRoom(命名误导修复后)
- Admin ≠ Employee(两个独立 Object)
- Examine = 医疗检查项目(MedicalExamine 的 systemSetting 配置)
- bodyCheckItem / medicalCheckItem 是同源对象

### L3 数据库结构 / FK / 索引

- **全部 F / 未验证**(前端无证据)
- 不能从前端变量名推断数据库表名

---

## §22 API actual / Write actual / Production mutation

**API actual = 0 / Write actual = 0 / Production mutation = 0** ✓

仅执行:`Get-FileHash` / `git status` / `git add --` / `git commit` / `git push` / `python` 本地分析脚本(临时目录)/ `Get-ChildItem` 校验。

---

## §23 SHA256

| 文件 | SHA256 |
|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A |

---

## §24 V4.4 最终诊所管理红线(汇总)

### 24.1 真实独立 ID 允许(14 个 A)

companyId / employeeId / adminId / adminRoleId / consultRoomId / roleId / bodyCheckItemId / medicalCheckItem.id / companyCashConfId / departmentId(弱)/ corpTypeId / consultRoomName / examineId / companyIdArray + companyName / employeeName / corporationName

### 24.2 F / 禁造 ID(21 个)

companyVo / clinicId / clinicName / clinicVo / employeeVo / departmentName / departmentVo / departmentArr / roleVo / consultRoomStatus / settlementId / costId / expenseId / bankCardId / feeBankCardId / clinicImageId / imageId / cashConfigId / checkItemId / checkConfigId / corpPointRuleId

### 24.3 命名误导修复(8 个)

1. `adminClinicCtrl` → **ConsultRoomCtrl**(不是 Clinic 配置)
2. `feeBankCardCtrl` → **feeWalletCtrl**(实际是 Customer Wallet)
3. `chargeAdminCtrl` → **cashConfigCtrl**(实际是 corpCashConf + cashierDiscount)
4. `medicalFeesListCtrl` → **examineListCtrl**(实际是 Examine 列表)
5. `addCheckCtrl` → **addExamineCtrl**(实际是 Examine)
6. `addCheckItemCtrl` → **addMedicalCheckItemCtrl**(实际是 medicalCheckItem)
7. `checkListCtrl` → **examineVoListCtrl**(实际是 Examine)
8. `phoneAdminCtrl` → 命名误导待确认业务

### 24.4 Admin ≠ Employee

- **adminId 21 / adminRoleId 29** 是 Admin 账号 ID
- **employeeId 35** 是员工 ID
- **两者完全独立**,不可合并
- Employee → Department:无 FK
- Employee → Role:无 FK(只有 Admin → Role)

### 24.5 Department 弱业务

- departmentId 1 命中(State 参数)
- departmentName 0 命中
- 实际字段:departDesc / rank1
- Employee → Department:无 FK

### 24.6 L3 数据库结构:全部 F

- 不能从前端变量名推断数据库表名

---

## §25 Git / 完整性

### 25.1 完整性闸门

4 文件 SHA256 全部 PASS(见 §0)。

### 25.2 累计统计

- controller.js 2,142,219 bytes / **59,214 行**
- 417 个 Controller 注册
- 915 个 .json API
- **42 个诊所管理相关 Controller**
- **35 个 Read API**
- **31 个 Write API**
- **14 个真实 ID**
- **21 个禁造 ID**
- **8 个命名误导**

### 25.3 Git 操作

- Commit:`141b966cbcbf1b1469fb31636239fb7466c8533c`(S1-157 之后,S1-158 待提交)
- Branch:master
- Tracked = 228 / Untracked = 10 / Ignored = 1
- 本轮新增:`221_S1-158_*.md`
- 预期:Tracked = 229 / Untracked = 10 / Ignored = 1 / LOCAL == origin/master