# 12｜模块 checkinList 登记

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/checkinList/` |
| 中文名 | 登记 |
| 开发波次 | W2 |
| 页面数 | **3** |
| 端点数（去重） | **27** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addCheckin` | `/addCheckin?appointId&type` | `views/checkinList/addCheckin.html` | `addCheckinCtrl` | 10 |
| 2 | `checkinList` | `/checkinList?printCheckinId&appointId` | `views/checkinList/checkinList.html` | `checkinListCtrl` | 19 |
| 3 | `yuYueJiLu` | `/yuYueJiLu` | `views/checkinList/yuYueJiLu.html` | `yuYueJiLuCtrl` | 1 |

## §2 端点清单（去重 27 个）

- `POST /admin/addSchoolMateConsume.json`
- `POST /admin/bandingCustomer.json`
- `POST /admin/changeBandingWechat.json`
- `POST /admin/confirmArrivalOfAppoint.json`
- `POST /admin/deleteCustomerCheckin.json`
- `POST /admin/getAppointPrintData.json`
- `POST /admin/getBandingWechatQrcode.json`
- `POST /admin/getCustomerVo.json`
- `POST /admin/getEmployeeVo.json`
- `POST /admin/getExamineVoList.json`
- `POST /admin/getPatientVo.json`
- `POST /admin/getPatientVoList.json`
- `POST /admin/getSchoolClassList.json`
- `POST /admin/insertCustomerCheckin.json`
- `POST /admin/insertCustomerCheckinOfNewCustomer.json`
- `POST /admin/insertCustomerCheckinOfNewPaitent.json`
- `POST /admin/isBandingWechat.json`
- `POST /admin/medicalCheckBeforeCustomerCheckin.json`
- `POST /admin/saveCustomerInfo.json`
- `POST /admin/savePatientInfo.json`
- `POST /admin/selectAppointPatientVoList.json`
- `POST /admin/selectCustomerCheckinVoListOfCompany.json`
- `POST /admin/selectCustomerWaitingBindingVo.json`
- `POST /admin/selectEmployeeVoList.json`
- `POST /admin/selectTagList.json`
- `POST /admin/sendCustomerCheckin.json`
- `POST /admin/updateCustomerTags.json`

## §3 逐页字段规格

### 12.1 `addCheckin`

- **URL**：`/addCheckin?appointId&type`
- **模板**：`views/checkinList/addCheckin.html`
- **控制器**：`addCheckinCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addSchoolMateConsume` | `POST /admin/addSchoolMateConsume.json` |
| `confirmArrivalOfAppoint` | `POST /admin/confirmArrivalOfAppoint.json` |
| `getEmployeeVo` | `POST /admin/getEmployeeVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getPatientVoList` | `POST /admin/getPatientVoList.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `insertCustomerCheckin` | `POST /admin/insertCustomerCheckin.json` |
| `insertCustomerCheckinOfNewCustomer` | `POST /admin/insertCustomerCheckinOfNewCustomer.json` |
| `insertCustomerCheckinOfNewPaitent` | `POST /admin/insertCustomerCheckinOfNewPaitent.json` |
| `selectEmployeeVoList` | `POST /admin/selectEmployeeVoList.json` |

**必填项**

| 标签 |
|---|
| * 姓名 如果是微信昵称，请登记为真实姓名，便于以后查询 |
| * 会员姓名 如果是微信昵称，请登记为真实姓名，便于以后查询 |
| * 姓名 |

**表单标签**

| 标签 |
|---|
| * 姓名 如果是微信昵称，请登记为真实姓名，便于以后查询 |
| 手机号 |
| 性别 |
| 男 女 男 女 出生年月 |
| 身份证号码 |
| 备注 |
| * 会员姓名 如果是微信昵称，请登记为真实姓名，便于以后查询 |
| 会员来源 |
| 学校 |
| 班级 |
| * 姓名 |
| 男 女 出生年月 |
| 诊所 |
| 接诊{{corpInfo.employeeTitle}} |
| {{item.employee.employeeName}} 返回 确定 完成登记 挂号费 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.linkMobile` |
| `obj.gender` |
| `obj.birthday` |
| `obj.idCard` |
| `obj.patientRemark` |
| `obj.customerName` |
| `checkCustomer.name` |
| `checkCustomer.gender` |
| `checkCustomer.birthday` |
| `checkCustomer.idCard` |
| `checkCustomer.patientRemark` |
| `doctorKeyword` |
| `obj.employeeId` |
| `guahao` |
| `registrationFeeId` |
| `needPrint.isNeed` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `qrcodeImg` |
| `keyword` |
| `firstDocitem.patient.avatar` |
| `firstDocitem.patient.patientName` |
| `firstDocitem.customer.linkMobile` |
| `obj.linkMobile` |
| `obj.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `channel.channel` |
| `basic.schoolName` |
| `obj.avatar` |
| `checkCustomer.avatar` |
| `companyName` |
| `corpInfo.employeeTitle` |
| `doctorName` |
| `firstDocitem.patient.patientGender` |
| `gender` |
| `myCroppedImage` |
| `item.employee.id` |
| `item.employee.employeeName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePatient()` |
| `showCode($event)` |
| `$event.stopPropagation()` |
| `searchPatientkeyword($event)` |
| `searchPatientMobile($event)` |
| `open1()` |
| `Popout.showChannelModal=true` |
| `openSchoolPop()` |
| `clearBasicSchool()` |
| `chooseImg()` |
| `showAddCustomer()` |
| `open2()` |
| `chooseCustomerImg()` |
| `showAddDoctorModal()` |
| `searchCheckinPatient()` |
| `getPatientChecikList.nextPage()` |
| `clear()` |
| `checkBefore()` |
| `getBaseCode()` |
| `hideImgModal()` |
| `setApproved()` |
| `clearDoctor()` |
| `selectDoctor()` |
| `selectDoctorModal=false` |
| `create()` |
| `hideCheckModel()` |

**跳转到**：`checkinList`, `yuYueJiLu`

**下拉数据源（ng-options）**

```
x.id as x.name for x in  gender
x.id as x.name for x in registArr
```

### 12.2 `checkinList`

- **URL**：`/checkinList?printCheckinId&appointId`
- **模板**：`views/checkinList/checkinList.html`
- **控制器**：`checkinListCtrl`
- **端点数**：19

**调用的端点**

| 动作 | 端点 |
|---|---|
| `bandingCustomer` | `POST /admin/bandingCustomer.json` |
| `changeBandingWechat` | `POST /admin/changeBandingWechat.json` |
| `deleteCustomerCheckin` | `POST /admin/deleteCustomerCheckin.json` |
| `getAppointPrintData` | `POST /admin/getAppointPrintData.json` |
| `getBandingWechatQrcode` | `POST /admin/getBandingWechatQrcode.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `getPatientVo` | `POST /admin/getPatientVo.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `isBandingWechat` | `POST /admin/isBandingWechat.json` |
| `medicalCheckBeforeCustomerCheckin` | `POST /admin/medicalCheckBeforeCustomerCheckin.json` |
| `saveCustomerInfo` | `POST /admin/saveCustomerInfo.json` |
| `savePatientInfo` | `POST /admin/savePatientInfo.json` |
| `selectCustomerCheckinVoListOfCompany` | `POST /admin/selectCustomerCheckinVoListOfCompany.json` |
| `selectCustomerWaitingBindingVo` | `POST /admin/selectCustomerWaitingBindingVo.json` |
| `selectEmployeeVoList` | `POST /admin/selectEmployeeVoList.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `sendCustomerCheckin` | `POST /admin/sendCustomerCheckin.json` |
| `updateCustomerTags` | `POST /admin/updateCustomerTags.json` |

**必填项**

| 标签 |
|---|
| * 患者姓名 身份证号码 |
| * 性别 |
| * 联系人 |
| * 患者和联系人的关系 本人 儿子 女儿 父亲 母亲 配偶 其他 会员来源 |

**表单标签**

| 标签 |
|---|
| * 患者姓名 身份证号码 |
| * 性别 |
| 生日 |
| 身高(cm) |
| 体重(kg) |
| 学校 |
| 班级 |
| 民族 |
| 籍贯 |
| * 联系人 |
| 联系人手机号 |
| * 患者和联系人的关系 本人 儿子 女儿 父亲 母亲 配偶 其他 会员来源 |
| 备注 |
| 会员标签 |
| {{item.employee.employeeName}} 返回 确定 完成登记 挂号费 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `rightTime` |
| `obj.keyword` |
| `data.patientName` |
| `data.idCard` |
| `data.patientGender` |
| `data.patientBirthday` |
| `data.height` |
| `data.weight` |
| `data.nation` |
| `data.nativePlace` |
| `customer.trueName` |
| `customer.linkMobile` |
| `data.relationShip` |
| `data.patientRemark` |
| `customerCheckin.employeeId` |
| `customerCheckin.guahao` |
| `customerCheckin.registrationFeeId` |
| `customerCheckin.isNeedPrint` |
| `doctorKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.total.totalCount` |
| `memberFactory.total.waitingSendCount` |
| `memberFactory.total.sendedCount` |
| `memberFactory.total.receivedCount` |
| `memberFactory.total.completeCount` |
| `item.customerCheckin.status` |
| `checkinStatus` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.customerCheckin.createName` |
| `item.customerCheckin.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `corpInfo.employeeTitle` |
| `item.employee.employeeName` |
| `basic.schoolName` |
| `customer.channel` |
| `item.employee.id` |
| `qrcodeInfo.imgSrc` |
| `qrcodeInfo.bindUser.lastCustomer.avatar` |
| `qrcodeInfo.bindUser.lastCustomer.customerName` |
| `printInfo.companyName` |
| `printInfo.patientName` |
| `printInfo.appointDay` |
| `printInfo.appointTime` |
| `printInfo.employeeName` |
| `printInfo.consultRoomName` |
| `printInfo.consultRoomAddress` |
| `printInfo.queueNumber` |
| `printInfo.nowTime` |
| `ss` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchTab(2)` |
| `searchTab(3)` |
| `open1()` |
| `preDiagnosisExamination.getMedicalCheckBeforeCustomerCheckin(item)` |
| `showPatientModal(item.patient.id,$index)` |
| `qrcodeInfo.bindWechat(item)` |
| `goMyMember(item.customer.id,item.patient.id)` |
| `sendCustomerCheckin(item)` |
| `deleteCheck(item.customerCheckin.id)` |
| `updatePatientModal=false` |
| `open2()` |
| `openSchoolPop()` |
| `clearBasicSchool()` |
| `showCommon()` |
| `updatePatient()` |
| `medicalRecordModal=false` |
| `clearDoctor()` |
| `selectDoctor()` |
| `create()` |
| `hideCheckModel()` |
| `qrcodeInfo.bindWechatAffirm()` |
| `qrcodeInfo.showPopout(false)` |

**跳转到**：`addCheckin`, `yuYueJiLu`

**下拉数据源（ng-options）**

```
x.id as x.name for x in registArr
x.id as x.name for x in sex
```

### 12.3 `yuYueJiLu`

- **URL**：`/yuYueJiLu`
- **模板**：`views/checkinList/yuYueJiLu.html`
- **控制器**：`yuYueJiLuCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectAppointPatientVoList` | `POST /admin/selectAppointPatientVoList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `rightTime` |
| `parameterObj.yuyueMingxiForm.keyword` |
| `resultObj.dialogMsg.employee.employeeName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `MessageObj.successNum` |
| `MessageObj.cancelNum` |
| `memberFactory.total.sendedCount` |
| `item.appoint.cancelStatus` |
| `item.patient.avatar` |
| `item.patient.patientName` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.employee.employeeName` |
| `item.appoint.appointStartTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `MessageObj.picUrl` |
| `resultObj.dialogMsg.patient.patientName` |
| `resultObj.dialogMsg.customer.linkMobile` |
| `resultObj.dialogMsg.patient.patientGender` |
| `resultObj.dialogMsg.patient.patientBirthday` |
| `resultObj.dialogMsg.appoint.appointDay` |
| `resultObj.dialogMsg.appoint.appointStartTime` |
| `resultObj.dialogMsg.appoint.appointEndTime` |
| `resultObj.dialogMsg.appoint.appointCode` |
| `resultObj.dialogMsg.appoint.remark` |
| `resultObj.dialogMsg.appoint.gmtCreate` |
| `ss` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideMember()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `open1()` |
| `showPatientModal(item)` |
| `updatePatientModal=false` |
| `updatePatientModal = false` |
| `medicalRecordModal=false` |

**跳转到**：`addCheckin`, `checkinList`, `yuYueJiLu`
