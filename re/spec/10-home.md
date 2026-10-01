# 10｜模块 home 主页/工作台

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/home/` |
| 中文名 | 主页/工作台 |
| 开发波次 | W0 |
| 页面数 | **12** |
| 端点数（去重） | **36** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `404` | `/404` | `views/home/404.html` | `404Ctrl` | 0 |
| 2 | `admin` | `/admin` | `views/home/admin.html` | `adminCtrl` | 0 |
| 3 | `allSize` | `/allSize` | `views/home/allSize.html` | `allSizeCtrl` | 0 |
| 4 | `systemSetting.company` | `/company` | `views/home/company.html` | `companyCtrl` | 4 |
| 5 | `home` | `/home?renew` | `views/home/home.html` | `homeCtrl` | 5 |
| 6 | `homeAnnouncement` | `/homeAnnouncement` | `views/home/homeAnnouncement.html` | `homeAnnouncementCtrl` | 1 |
| 7 | `homeAnnouncementDetails` | `/homeAnnouncementDetails?id` | `views/home/homeAnnouncementDetails.html` | `homeAnnouncementDetailsCtrl` | 1 |
| 8 | `homePage` | `/homePage` | `views/home/homePage.html` | `homePageCtrl` | 0 |
| 9 | `login` | `/login` | `views/home/login.html` | `loginCtrl` | 6 |
| 10 | `modifyPassword` | `/modifyPassword` | `views/home/modifyPassword.html` | `modifyPasswordCtrl` | 3 |
| 11 | `testPage` | `/testPage` | `views/home/testPage.html` | `testPageCtrl` | 4 |
| 12 | `workBeach` | `/workBeach` | `views/home/workBeach.html` | `workBeachCtrl` | 17 |

## §2 端点清单（去重 36 个）

- `POST /admin/addDepartment.json`
- `POST /admin/addHospital.json`
- `POST /admin/checkSchoolBodyCheckInfoVersion.json`
- `POST /admin/employeeSubscribeMessage.json`
- `POST /admin/getAdminInfo.json`
- `POST /admin/getAdminSystemNoticeVo.json`
- `POST /admin/getAllCityMap.json`
- `POST /admin/getAppointPatientVo.json`
- `POST /admin/getCompanyOfMine.json`
- `POST /admin/getCorpConf.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getCorpTimeData.json`
- `POST /admin/getCorpTypeConfVo.json`
- `POST /admin/getEmployeeSchedulingWeekVoOfEmployee.json`
- `POST /admin/getLoginEmployee.json`
- `POST /admin/modifyPass.json`
- `POST /admin/readAdminSystemNotice.json`
- `POST /admin/saveEmployeeAvatar.json`
- `POST /admin/saveSchoolBodyCheckInfo.json`
- `POST /admin/selectAdminSystemNoticeVoList.json`
- `POST /admin/selectCorpSmsByCorpId.json`
- `POST /admin/selectEmployeeAppointByWeek.json`
- `POST /admin/selectMessageCategoryList.json`
- `POST /admin/selectMessageLogList.json`
- `POST /admin/selectSchoolMateCheckVoList.json`
- `POST /admin/selectSchoolPromotionListVoList.json`
- `POST /admin/sendCodeToMe.json`
- `POST /admin/updateAdminReadStatusToIgnore.json`
- `POST /admin/updateAdminReadStatusToRead.json`
- `POST /admin/updateAllAdminReadStatusToIgnore.json`
- `POST /admin/updateCorpInfo.json`
- `POST /admin/updateCorpTypeConf.json`
- `POST /auth/adminLogin.json`
- `POST /auth/adminSendPass.json`
- `POST /auth/getMyAdminCorpList.json`
- `POST /auth/isAdminTokenOk.json`

## §3 逐页字段规格

### 10.1 `404`

- **URL**：`/404`
- **模板**：`views/home/404.html`
- **控制器**：`404Ctrl`
- **端点数**：0

**页面动作（ng-click）**

| 动作 |
|---|
| `goBack()` |

**跳转到**：`home`

### 10.2 `admin`

- **URL**：`/admin`
- **模板**：`views/home/admin.html`
- **控制器**：`adminCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 用户名： |
| * 手机号： |
| 邮箱： |

**表单标签**

| 标签 |
|---|
| * 用户名： |
| * 手机号： |
| 邮箱： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `adminObjectFactory.object.nickname` |
| `adminObjectFactory.object.mobile` |
| `adminObjectFactory.object.email` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

### 10.3 `allSize`

- **URL**：`/allSize`
- **模板**：`views/home/allSize.html`
- **控制器**：`allSizeCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `width` |
| `height` |

### 10.4 `systemSetting.company`

- **URL**：`/company`
- **模板**：`views/home/company.html`
- **控制器**：`companyCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getCorpTypeConfVo` | `POST /admin/getCorpTypeConfVo.json` |
| `updateCorpInfo` | `POST /admin/updateCorpInfo.json` |
| `updateCorpTypeConf` | `POST /admin/updateCorpTypeConf.json` |

**必填项**

| 标签 |
|---|
| 公司名称： |
| 标语口号： |
| 公司地址： |
| 客服电话： |
| 后台背景： |
| 企业类型： |

**表单标签**

| 标签 |
|---|
| 公司名称： |
| 标语口号： |
| 公司地址： |
| 客服电话： |
| 医械许可： |
| 后台背景： |
| 企业类型： |
| {{corp.name}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `companyFactory.object.corporationName` |
| `companyFactory.object.slogon` |
| `companyFactory.object.address` |
| `companyFactory.object.servicePhone` |
| `companyFactory.object.medicalDevicePermit` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `img.imgurl` |
| `keyimg` |
| `corp.name` |
| `bigImgUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseImg()` |
| `bigImg(keyimg)` |
| `choseCorp($index)` |
| `modify()` |
| `imgModal=false` |

### 10.5 `home`

- **URL**：`/home?renew`
- **模板**：`views/home/home.html`
- **控制器**：`homeCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminSystemNoticeVo` | `POST /admin/getAdminSystemNoticeVo.json` |
| `getCorpTimeData` | `POST /admin/getCorpTimeData.json` |
| `readAdminSystemNotice` | `POST /admin/readAdminSystemNotice.json` |
| `selectAdminSystemNoticeVoList` | `POST /admin/selectAdminSystemNoticeVoList.json` |
| `selectCorpSmsByCorpId` | `POST /admin/selectCorpSmsByCorpId.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.corporationName` |
| `companyFactory.result.object.backImg` |
| `nowDate` |
| `date` |
| `yyyy` |
| `testurl` |
| `remainDay` |
| `transform.color` |
| `transform.deg` |
| `maxEndTime` |
| `MM` |
| `dd` |
| `common.content` |
| `li.systemNotice.title` |
| `li.systemNotice.publishTime` |
| `corpNearExpired` |
| `systemNotice.title` |
| `systemNotice.content` |
| `img` |

**页面动作（ng-click）**

| 动作 |
|---|
| `renew()` |
| `common.fun()` |
| `location()` |
| `changeStatus(li)` |

### 10.6 `homeAnnouncement`

- **URL**：`/homeAnnouncement`
- **模板**：`views/home/homeAnnouncement.html`
- **控制器**：`homeAnnouncementCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectAdminSystemNoticeVoList` | `POST /admin/selectAdminSystemNoticeVoList.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `li.systemNotice.publishTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `li.systemNotice.title` |
| `li.systemNotice.content` |

**页面动作（ng-click）**

| 动作 |
|---|
| `changeStatus(li)` |

### 10.7 `homeAnnouncementDetails`

- **URL**：`/homeAnnouncementDetails?id`
- **模板**：`views/home/homeAnnouncementDetails.html`
- **控制器**：`homeAnnouncementDetailsCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminSystemNoticeVo` | `POST /admin/getAdminSystemNoticeVo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `systemNotice.publishTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `systemNotice.title` |
| `systemNotice.content` |
| `img` |

**页面动作（ng-click）**

| 动作 |
|---|
| `lookImg(img)` |

### 10.8 `homePage`

- **URL**：`/homePage`
- **模板**：`views/home/homePage.html`
- **控制器**：`homePageCtrl`
- **端点数**：0

**跳转到**：`login`

### 10.9 `login`

- **URL**：`/login`
- **模板**：`views/home/login.html`
- **控制器**：`loginCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getCorpTypeConfVo` | `POST /admin/getCorpTypeConfVo.json` |
| `adminLogin` | `POST /auth/adminLogin.json` |
| `adminSendPass` | `POST /auth/adminSendPass.json` |
| `getMyAdminCorpList` | `POST /auth/getMyAdminCorpList.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `user.name` |
| `user.password` |
| `user.corpId` |
| `findpassword.mobile` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyLogo` |
| `companyName` |
| `nowDate` |
| `date` |
| `yyyy` |
| `item.id` |
| `item.corporationName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(2)` |
| `login()` |
| `modify()` |
| `setTab(1)` |

**下拉数据源（ng-options）**

```
item.id as item.corporationName for item in corpList.items
item.id as item.corporationName for item in corpList2.items
```

### 10.10 `modifyPassword`

- **URL**：`/modifyPassword`
- **模板**：`views/home/modifyPassword.html`
- **控制器**：`modifyPasswordCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `modifyPass` | `POST /admin/modifyPass.json` |
| `sendCodeToMe` | `POST /admin/sendCodeToMe.json` |

**必填项**

| 标签 |
|---|
| * 手机号： |
| * 验证码： |
| * 新密码： |
| * 新密码确认： |

**表单标签**

| 标签 |
|---|
| 验证码： |
| 新密码： |
| 新密码确认： |
| 确定 |
| * 手机号： |
| * 验证码： |
| * 新密码： |
| * 新密码确认： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.code` |
| `obj.password` |
| `password` |
| `obj.mobile` |

**页面动作（ng-click）**

| 动作 |
|---|
| `sendCode()` |
| `modify()` |
| `cancel()` |

### 10.11 `testPage`

- **URL**：`/testPage`
- **模板**：`views/home/testPage.html`
- **控制器**：`testPageCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkSchoolBodyCheckInfoVersion` | `POST /admin/checkSchoolBodyCheckInfoVersion.json` |
| `saveSchoolBodyCheckInfo` | `POST /admin/saveSchoolBodyCheckInfo.json` |
| `selectSchoolMateCheckVoList` | `POST /admin/selectSchoolMateCheckVoList.json` |
| `selectSchoolPromotionListVoList` | `POST /admin/selectSchoolPromotionListVoList.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.i` |

**页面动作（ng-click）**

| 动作 |
|---|
| `updateSchoolMateCheck()` |
| `updateSchoolMateCheck2(` |

### 10.12 `workBeach`

- **URL**：`/workBeach`
- **模板**：`views/home/workBeach.html`
- **控制器**：`workBeachCtrl`
- **端点数**：17

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addDepartment` | `POST /admin/addDepartment.json` |
| `addHospital` | `POST /admin/addHospital.json` |
| `employeeSubscribeMessage` | `POST /admin/employeeSubscribeMessage.json` |
| `getAllCityMap` | `POST /admin/getAllCityMap.json` |
| `getAppointPatientVo` | `POST /admin/getAppointPatientVo.json` |
| `getCompanyOfMine` | `POST /admin/getCompanyOfMine.json` |
| `getCorpConf` | `POST /admin/getCorpConf.json` |
| `getEmployeeSchedulingWeekVoOfEmployee` | `POST /admin/getEmployeeSchedulingWeekVoOfEmployee.json` |
| `getLoginEmployee` | `POST /admin/getLoginEmployee.json` |
| `saveEmployeeAvatar` | `POST /admin/saveEmployeeAvatar.json` |
| `selectEmployeeAppointByWeek` | `POST /admin/selectEmployeeAppointByWeek.json` |
| `selectMessageCategoryList` | `POST /admin/selectMessageCategoryList.json` |
| `selectMessageLogList` | `POST /admin/selectMessageLogList.json` |
| `updateAdminReadStatusToIgnore` | `POST /admin/updateAdminReadStatusToIgnore.json` |
| `updateAdminReadStatusToRead` | `POST /admin/updateAdminReadStatusToRead.json` |
| `updateAllAdminReadStatusToIgnore` | `POST /admin/updateAllAdminReadStatusToIgnore.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{item.name}} |
| 2 | {{item.name}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `allAppoint.dialogMsg.employee.employeeName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `msgObj.avatar` |
| `msgObj.nickName` |
| `msgObj.companyName` |
| `item.messageCategory.messageCategoryName` |
| `item.ListNum` |
| `items.saveMsg` |
| `item.name` |
| `item1` |
| `item.key` |
| `allAppoint.ppName` |
| `allAppoint.dialogMsg.customer.avatar` |
| `allAppoint.dialogMsg.patient.patientName` |
| `allAppoint.dialogMsg.customer.linkMobile` |
| `allAppoint.dialogMsg.patient.patientGender` |
| `gender` |
| `allAppoint.dialogMsg.patient.patientBirthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `howoldFilter` |
| `allAppoint.dialogMsg.appoint.appointDay` |
| `allAppoint.dialogMsg.appoint.appointStartTime` |
| `HH` |
| `mm` |
| `allAppoint.dialogMsg.appoint.appointEndTime` |
| `allAppoint.dialogMsg.appoint.appointCode` |
| `allAppoint.dialogMsg.appoint.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `closeDaiban()` |
| `selectAll($event,$index)` |
| `affrimDaiban()` |
| `daibanPopout.popout = true` |
| `lookAllBacklog($index)` |
| `ignoreAll(item)` |
| `neglectInfo(items,false)` |
| `lookDetails(items)` |
| `openVisit(items,true)` |
| `closePopout()` |
| `neglectInfo(items,true)` |
| `openVisit(items,false)` |
| `closeLookDetails()` |
