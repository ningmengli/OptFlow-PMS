# 07｜模块 adminManage 权限/角色/区域

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/adminManage/` |
| 中文名 | 权限/角色/区域 |
| 开发波次 | W1' |
| 页面数 | **17** |
| 端点数（去重） | **42** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addRole` | `/addRole` | `views/adminManage/addRole.html` | `addRoleCtrl` | 2 |
| 2 | `adminAreaList` | `/adminAreaList` | `views/adminManage/adminAreaList.html` | `adminAreaListCtrl` | 3 |
| 3 | `adminList` | `/adminList` | `views/adminManage/adminList.html` | `adminListCtrl` | 13 |
| 4 | `adminModify` | `/adminModify?adminId` | `views/adminManage/adminModify.html` | `adminModifyCtrl` | 0 |
| 5 | `adminPasswordModify` | `/adminPasswordModify?adminId` | `views/adminManage/adminPasswordModify.html` | `adminPasswordModifyCtrl` | 2 |
| 6 | `adminAreaPasswordModify` | `/adminAreaPasswordModify?adminId` | `views/adminManage/adminPasswordModify.html` | `adminPasswordModifyCtrl` | 2 |
| 7 | `areaRoleAdmin` | `/areaRoleAdmin` | `views/adminManage/areaRoleAdmin.html` | `areaRoleAdminCtrl` | 1 |
| 8 | `areaScreenAdmin` | `/areaScreenAdmin` | `views/adminManage/areaScreenAdmin.html` | `areaScreenAdminCtrl` | 1 |
| 9 | `createAdmin` | `/createAdmin` | `views/adminManage/createAdmin.html` | `createAdminCtrl` | 4 |
| 10 | `createAdminArea` | `/createAdminArea` | `views/adminManage/createAdminArea.html` | `createAdminAreaCtrl` | 18 |
| 11 | `encryptUser` | `/encryptUser` | `views/adminManage/encryptUser.html` | `encryptUserCtrl` | 0 |
| 12 | `memberAdmin` | `/memberAdmin` | `views/adminManage/memberAdmin.html` | `memberAdminCtrl` | 0 |
| 13 | `modifyAdminArea` | `/modifyAdminArea?adminId` | `views/adminManage/modifyAdminArea.html` | `modifyAdminAreaCtrl` | 5 |
| 14 | `modifyAreaRole` | `/modifyAreaRole?roleId` | `views/adminManage/modifyAreaRole.html` | `modifyAreaRoleCtrl` | 4 |
| 15 | `modifyRole` | `/modifyRole?roleId` | `views/adminManage/modifyRole.html` | `modifyRoleCtrl` | 4 |
| 16 | `roleAdmin` | `/roleAdmin` | `views/adminManage/roleAdmin.html` | `roleAdminCtrl` | 1 |
| 17 | `roleDetail` | `/roleDetail?roleId` | `views/adminManage/roleDetail.html` | `modifyRoleCtrl` | 4 |

## §2 端点清单（去重 42 个）

- `POST /admin/changeAdminRole.json`
- `POST /admin/changeStatus.json`
- `POST /admin/createAdmin.json`
- `POST /admin/createAdminRole.json`
- `POST /admin/createAreaAdmin.json`
- `POST /admin/getAdminAreaLevelVo.json`
- `POST /admin/getAdminCustVoList.json`
- `POST /admin/getAdminList.json`
- `POST /admin/getAdminRoleVo.json`
- `POST /admin/getAdminStateListForUpdate.json`
- `POST /admin/getAreaAdminRole.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCorpWatchdogConf.json`
- `POST /admin/getLoginAdminAreaLevelVo.json`
- `POST /admin/getLoginAdminSubAreaAdminList.json`
- `POST /admin/getOtherAdminInfo.json`
- `POST /admin/getProvinceVoList.json`
- `POST /admin/getRoleStateListForUpdate.json`
- `POST /admin/getSchoolList.json`
- `POST /admin/getSchoolMateManageCorpVoList.json`
- `POST /admin/getSuperStateList.json`
- `POST /admin/getUnionAdminStateList.json`
- `POST /admin/getWatchdog.json`
- `POST /admin/modifyOtherPass.json`
- `POST /admin/moveCustomersOfEmployee.json`
- `POST /admin/refreshWatchdogLocalStore.json`
- `POST /admin/saveCorpWatchdogConf.json`
- `POST /admin/selectAdminRoleVoList.json`
- `POST /admin/selectBandingCustomerList.json`
- `POST /admin/selectEmployeeVoList.json`
- `POST /admin/selectLoginAdminSubAreaLevelList.json`
- `POST /admin/selectWatchdogList.json`
- `POST /admin/transferAdminRole.json`
- `POST /admin/updateAdminRoleInfo.json`
- `POST /admin/updateAdminStateList.json`
- `POST /admin/updateAreaAdmin.json`
- `POST /admin/updateOtherAdminInfo.json`
- `POST /admin/updateRoleStateList.json`
- `POST /admin/updateWatchdog.json`
- `POST /admin/updateWatchdogLocalStore.json`
- `POST /admin/updateWatchdogStatus.json`
- `POST /auth/isCertificateDeleted.json`

## §3 逐页字段规格

### 7.1 `addRole`

- **URL**：`/addRole`
- **模板**：`views/adminManage/addRole.html`
- **控制器**：`addRoleCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createAdminRole` | `POST /admin/createAdminRole.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |

**必填项**

| 标签 |
|---|
| * 角色名称 |

**表单标签**

| 标签 |
|---|
| * 角色名称 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.roleName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `create()` |

**跳转到**：`roleAdmin`

### 7.2 `adminAreaList`

- **URL**：`/adminAreaList`
- **模板**：`views/adminManage/adminAreaList.html`
- **控制器**：`adminAreaListCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeStatus` | `POST /admin/changeStatus.json` |
| `getLoginAdminSubAreaAdminList` | `POST /admin/getLoginAdminSubAreaAdminList.json` |
| `selectLoginAdminSubAreaLevelList` | `POST /admin/selectLoginAdminSubAreaLevelList.json` |

**表单标签**

| 标签 |
|---|
| {{item.admin.nickname}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登录账户 |
| 2 | 姓名 |
| 3 | 单位名称 |
| 4 | 单位级别 |
| 5 | 所在(省、市、区/县） |
| 6 | 角色 |
| 7 | 状态 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `item.admin.status` |
| `normalKeyword` |
| `transfer.adminId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.admin.username` |
| `item.admin.nickname` |
| `item.adminAreaLevel.governmentName` |
| `item.adminAreaLevel.areaLevelId` |
| `areaLevel` |
| `item.adminAreaLevel.province` |
| `item.adminAreaLevel.city` |
| `item.adminAreaLevel.district` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `showMsg()` |
| `hideModal()` |
| `setRole()` |

**跳转到**：`areaRoleAdmin`, `areaScreenAdmin`, `createAdminArea`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 7.3 `adminList`

- **URL**：`/adminList`
- **模板**：`views/adminManage/adminList.html`
- **控制器**：`adminListCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeAdminRole` | `POST /admin/changeAdminRole.json` |
| `changeStatus` | `POST /admin/changeStatus.json` |
| `getAdminList` | `POST /admin/getAdminList.json` |
| `getAdminStateListForUpdate` | `POST /admin/getAdminStateListForUpdate.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getOtherAdminInfo` | `POST /admin/getOtherAdminInfo.json` |
| `getRoleStateListForUpdate` | `POST /admin/getRoleStateListForUpdate.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |
| `getSuperStateList` | `POST /admin/getSuperStateList.json` |
| `getUnionAdminStateList` | `POST /admin/getUnionAdminStateList.json` |
| `transferAdminRole` | `POST /admin/transferAdminRole.json` |
| `updateAdminStateList` | `POST /admin/updateAdminStateList.json` |
| `updateOtherAdminInfo` | `POST /admin/updateOtherAdminInfo.json` |

**表单标签**

| 标签 |
|---|
| {{iten.corpAdminHome.stateName}} |
| {{val.corpAdminHome.stateName}} |
| {{last.corpAdminHome.stateName}} |
| {{item.admin.nickname}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登录账户 |
| 2 | 姓名 |
| 3 | 所属{{corpInfo.companyTitle}} |
| 4 | 角色 |
| 5 | 权限 含角色权限和动态授权 |
| 6 | 状态 |
| 7 | APP |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `item.admin.status` |
| `item.admin.appStatus` |
| `adminname` |
| `normalKeyword` |
| `transfer.adminId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `state.name` |
| `corpInfo.companyTitle` |
| `item.admin.username` |
| `item.admin.nickname` |
| `item.company.companyName` |
| `item.adminRole.roleName` |
| `item.admin.status` |
| `adminStatus` |
| `item.admin.appStatus` |
| `item.adminStateType.stateTypeName` |
| `iten.corpAdminHome.id` |
| `iten.corpAdminHome.stateName` |
| `val.corpAdminHome.id` |
| `val.corpAdminHome.stateName` |
| `last.corpAdminHome.id` |
| `last.corpAdminHome.stateName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showState()` |
| `clearState()` |
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `viewAdmin(item.admin.id)` |
| `showModifyRole()` |
| `setState(iten.corpAdminHome.state,iten.corpAdminHome.stateName,iten.children.length)` |
| `setState(val.corpAdminHome.state,val.corpAdminHome.stateName)` |
| `setState(last.corpAdminHome.state,last.corpAdminHome.stateName)` |
| `searchName()` |
| `hideModal()` |
| `showMsg()` |
| `setRole()` |

**跳转到**：`createAdmin`, `memberAdmin`, `roleAdmin`

**下拉数据源（ng-options）**

```
x.id as x.name for x in appStatus
x.id as x.name for x in status
```

### 7.4 `adminModify`

- **URL**：`/adminModify?adminId`
- **模板**：`views/adminManage/adminModify.html`
- **控制器**：`adminModifyCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 姓名： |
| * 登录手机： |
| 角色： |

**表单标签**

| 标签 |
|---|
| * 姓名： |
| * 登录手机： |
| 所属{{corpInfo.companyTitle}}： |
| 所属加工中心： |
| 角色： |
| 角色权限： |
| 动态授权： |
| 全选 |
| {{item.schoolName}} |
| {{item.stateName}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.nickname` |
| `object.username` |
| `object` |
| `keyword` |
| `seletedAdminItemArray[$index]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.companyTitle` |
| `item` |
| `item.schoolName` |
| `item.adminStateType.stateTypeName` |
| `item.state` |
| `item.stateName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hide()` |
| `showSchoolModal()` |
| `showMsg()` |
| `modifyAdmin()` |
| `selectAll($event)` |
| `updateSelection($event,item.id,item.schoolName)` |
| `modifySchool()` |
| `schoolModal=false` |
| `selectAdmin(item.adminStateType.id,$index,$event)` |
| `modifyAdminItem(item.state,$event,seletedAdminItemArray[$index],$index)` |
| `hideModal()` |

**跳转到**：`adminList`

**下拉数据源（ng-options）**

```
x  as x.adminRole.roleName for x in getRoleList.items
```

### 7.5 `adminPasswordModify`

- **URL**：`/adminPasswordModify?adminId`
- **模板**：`views/adminManage/adminPasswordModify.html`
- **控制器**：`adminPasswordModifyCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getOtherAdminInfo` | `POST /admin/getOtherAdminInfo.json` |
| `modifyOtherPass` | `POST /admin/modifyOtherPass.json` |

**必填项**

| 标签 |
|---|
| * 手机号： |
| * 新密码： |
| * 新密码确认： |

**表单标签**

| 标签 |
|---|
| * 手机号： |
| * 新密码： |
| * 新密码确认： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.password` |
| `password` |
| `object.sendSms` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getAdminInfoObejctFactory.object.admin.mobile` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**跳转到**：`adminAreaList`, `adminList`

### 7.6 `adminAreaPasswordModify`

- **URL**：`/adminAreaPasswordModify?adminId`
- **模板**：`views/adminManage/adminPasswordModify.html`
- **控制器**：`adminPasswordModifyCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getOtherAdminInfo` | `POST /admin/getOtherAdminInfo.json` |
| `modifyOtherPass` | `POST /admin/modifyOtherPass.json` |

**必填项**

| 标签 |
|---|
| * 手机号： |
| * 新密码： |
| * 新密码确认： |

**表单标签**

| 标签 |
|---|
| * 手机号： |
| * 新密码： |
| * 新密码确认： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.password` |
| `password` |
| `object.sendSms` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getAdminInfoObejctFactory.object.admin.mobile` |

**页面动作（ng-click）**

| 动作 |
|---|
| `modify()` |

**跳转到**：`adminAreaList`, `adminList`

### 7.7 `areaRoleAdmin`

- **URL**：`/areaRoleAdmin`
- **模板**：`views/adminManage/areaRoleAdmin.html`
- **控制器**：`areaRoleAdminCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectAdminRoleVoList` | `POST /admin/selectAdminRoleVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 角色名称 |
| 2 | 状态 |
| 3 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.adminRole.roleName` |
| `item.adminRole.status` |
| `supplierStatus` |

**跳转到**：`adminAreaList`, `areaScreenAdmin`

### 7.8 `areaScreenAdmin`

- **URL**：`/areaScreenAdmin`
- **模板**：`views/adminManage/areaScreenAdmin.html`
- **控制器**：`areaScreenAdminCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSchoolMateManageCorpVoList` | `POST /admin/getSchoolMateManageCorpVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 筛查ID |
| 2 | 筛查名称 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.excuteCorp.id` |
| `item.excuteCorp.corporationName` |

**跳转到**：`adminAreaList`, `areaRoleAdmin`

### 7.9 `createAdmin`

- **URL**：`/createAdmin`
- **模板**：`views/adminManage/createAdmin.html`
- **控制器**：`createAdminCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createAdmin` | `POST /admin/createAdmin.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getRoleStateListForUpdate` | `POST /admin/getRoleStateListForUpdate.json` |
| `getSchoolList` | `POST /admin/getSchoolList.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| * 角色 |
| * 角色权限 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| 所属{{corpInfo.companyTitle}}： |
| * 角色 |
| * 角色权限 |
| 全选 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.nickname` |
| `obj.mobile` |
| `object` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.companyTitle` |
| `item` |
| `modelName` |
| `modelName.adminRole.roleName` |
| `item.schoolName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hide()` |
| `showSchoolModal()` |
| `showMsg()` |
| `create()` |
| `selectAll($event)` |
| `updateSelection($event,item.id,item.schoolName)` |
| `modifySchool()` |
| `schoolModal=false` |

**跳转到**：`adminList`

**下拉数据源（ng-options）**

```
x  as x.adminRole.roleName for x in getRoleList.items
```

### 7.10 `createAdminArea`

- **URL**：`/createAdminArea`
- **模板**：`views/adminManage/createAdminArea.html`
- **控制器**：`createAdminAreaCtrl`
- **端点数**：18

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createAreaAdmin` | `POST /admin/createAreaAdmin.json` |
| `getAdminCustVoList` | `POST /admin/getAdminCustVoList.json` |
| `getAreaAdminRole` | `POST /admin/getAreaAdminRole.json` |
| `getCorpWatchdogConf` | `POST /admin/getCorpWatchdogConf.json` |
| `getLoginAdminAreaLevelVo` | `POST /admin/getLoginAdminAreaLevelVo.json` |
| `getProvinceVoList` | `POST /admin/getProvinceVoList.json` |
| `getWatchdog` | `POST /admin/getWatchdog.json` |
| `moveCustomersOfEmployee` | `POST /admin/moveCustomersOfEmployee.json` |
| `refreshWatchdogLocalStore` | `POST /admin/refreshWatchdogLocalStore.json` |
| `saveCorpWatchdogConf` | `POST /admin/saveCorpWatchdogConf.json` |
| `selectBandingCustomerList` | `POST /admin/selectBandingCustomerList.json` |
| `selectEmployeeVoList` | `POST /admin/selectEmployeeVoList.json` |
| `selectLoginAdminSubAreaLevelList` | `POST /admin/selectLoginAdminSubAreaLevelList.json` |
| `selectWatchdogList` | `POST /admin/selectWatchdogList.json` |
| `updateWatchdog` | `POST /admin/updateWatchdog.json` |
| `updateWatchdogLocalStore` | `POST /admin/updateWatchdogLocalStore.json` |
| `updateWatchdogStatus` | `POST /admin/updateWatchdogStatus.json` |
| `isCertificateDeleted` | `POST /auth/isCertificateDeleted.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| * 机构级别 |
| * 归属地 |
| * 单位名称 |
| * 角色 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| * 机构级别 |
| * 归属地 |
| * 单位名称 |
| * 角色 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `createObj.nickname` |
| `createObj.mobile` |
| `createObj.areaLevelId` |
| `createObj.provinceAreaId` |
| `createObj.cityAreaId` |
| `createObj.districtAreaId` |
| `createObj.governmentName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `iten.id` |
| `iten.areaLevelName` |
| `getRoleObejctFactory.result.object.roleName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hide()` |
| `createArea()` |

**跳转到**：`adminAreaList`

**下拉数据源（ng-options）**

```
item.code as item.name for item in citiesData
item.code as item.name for item in data
item.code as item.name for item in districtData
```

### 7.11 `encryptUser`

- **URL**：`/encryptUser`
- **模板**：`views/adminManage/encryptUser.html`
- **控制器**：`encryptUserCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 启用操作证书 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 证书编号 |
| 3 | 证书状态 |
| 4 | 安装状态 |
| 5 | 安装电脑备注 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.useWatchdog` |
| `keyword` |
| `item.status` |
| `user.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getAdminList.count` |
| `userCert.serialNumber` |
| `hideSerialNumber` |
| `index` |
| `getAdminList.index` |
| `pageSize` |
| `item.serialNumber` |
| `item.localStore` |
| `localStore` |
| `item.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setDog(obj.useWatchdog)` |
| `deleteEncrypt()` |
| `makeEncrypt(item.serialNumber,item.version)` |
| `upload(item.serialNumber)` |
| `showRemark(item.id)` |
| `checkBefore()` |
| `hideModal()` |
| `clearEncrypt()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 7.12 `memberAdmin`

- **URL**：`/memberAdmin`
- **模板**：`views/adminManage/memberAdmin.html`
- **控制器**：`memberAdminCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 登录账户 |
| 2 | 姓名 |
| 3 | 所属{{corpInfo. companyTitle}} |
| 4 | 关注会员数 |
| 5 | 状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `doctorKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `item.admin.username` |
| `item.admin.nickname` |
| `item.company.companyName` |
| `item.adminCustCount` |
| `item.admin.status` |
| `supplierStatus` |
| `fromName` |
| `toName` |
| `item.customer.customerName` |
| `firstDocitem.employee.avatar` |
| `firstDocitem.employee.employeeName` |
| `firstDocitem.employee.mobile` |
| `firstDocitem.company.companyName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |
| `showModal(item.employee.id,item.admin.nickname)` |
| `chooseEmployeeTo(firstDocitem.employee.id,firstDocitem.employee.employeeName)` |
| `employeeListFactory.nextPage()` |
| `modify()` |
| `hideModal()` |

**跳转到**：`adminList`, `roleAdmin`

### 7.13 `modifyAdminArea`

- **URL**：`/modifyAdminArea?adminId`
- **模板**：`views/adminManage/modifyAdminArea.html`
- **控制器**：`modifyAdminAreaCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminAreaLevelVo` | `POST /admin/getAdminAreaLevelVo.json` |
| `getAreaAdminRole` | `POST /admin/getAreaAdminRole.json` |
| `getProvinceVoList` | `POST /admin/getProvinceVoList.json` |
| `selectLoginAdminSubAreaLevelList` | `POST /admin/selectLoginAdminSubAreaLevelList.json` |
| `updateAreaAdmin` | `POST /admin/updateAreaAdmin.json` |

**必填项**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| * 机构级别 |
| * 归属地 |
| * 单位名称 |
| * 角色 |

**表单标签**

| 标签 |
|---|
| * 姓名 |
| * 手机号 |
| * 机构级别 |
| * 归属地 |
| * 单位名称 |
| * 角色 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `createObj.nickname` |
| `createObj.areaLevelId` |
| `createObj.provinceAreaId` |
| `createObj.cityAreaId` |
| `createObj.districtAreaId` |
| `createObj.governmentName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `createObj.mobile` |
| `iten.id` |
| `iten.areaLevelName` |
| `getRoleObejctFactory.result.object.roleName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `createArea()` |

**跳转到**：`adminAreaList`

**下拉数据源（ng-options）**

```
item.code as item.name for item in citiesData
item.code as item.name for item in data
item.code as item.name for item in districtData
```

### 7.14 `modifyAreaRole`

- **URL**：`/modifyAreaRole?roleId`
- **模板**：`views/adminManage/modifyAreaRole.html`
- **控制器**：`modifyAreaRoleCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminRoleVo` | `POST /admin/getAdminRoleVo.json` |
| `getRoleStateListForUpdate` | `POST /admin/getRoleStateListForUpdate.json` |
| `updateAdminRoleInfo` | `POST /admin/updateAdminRoleInfo.json` |
| `updateRoleStateList` | `POST /admin/updateRoleStateList.json` |

**必填项**

| 标签 |
|---|
| * 角色名称 |
| * 权限列表 |

**表单标签**

| 标签 |
|---|
| * 角色名称 |
| * 权限列表 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.roleName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `create()` |

**跳转到**：`areaRoleAdmin`

### 7.15 `modifyRole`

- **URL**：`/modifyRole?roleId`
- **模板**：`views/adminManage/modifyRole.html`
- **控制器**：`modifyRoleCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminRoleVo` | `POST /admin/getAdminRoleVo.json` |
| `getRoleStateListForUpdate` | `POST /admin/getRoleStateListForUpdate.json` |
| `updateAdminRoleInfo` | `POST /admin/updateAdminRoleInfo.json` |
| `updateRoleStateList` | `POST /admin/updateRoleStateList.json` |

**必填项**

| 标签 |
|---|
| * 角色名称 |
| * 状态 |
| * 权限列表 |

**表单标签**

| 标签 |
|---|
| * 角色名称 |
| * 状态 |
| * 权限列表 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.roleName` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `create()` |

**跳转到**：`roleAdmin`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 7.16 `roleAdmin`

- **URL**：`/roleAdmin`
- **模板**：`views/adminManage/roleAdmin.html`
- **控制器**：`roleAdminCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectAdminRoleVoList` | `POST /admin/selectAdminRoleVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 角色名称 |
| 2 | 状态 |
| 3 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.adminRole.roleName` |
| `item.adminRole.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |

**跳转到**：`addRole`, `adminList`, `memberAdmin`

### 7.17 `roleDetail`

- **URL**：`/roleDetail?roleId`
- **模板**：`views/adminManage/roleDetail.html`
- **控制器**：`modifyRoleCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAdminRoleVo` | `POST /admin/getAdminRoleVo.json` |
| `getRoleStateListForUpdate` | `POST /admin/getRoleStateListForUpdate.json` |
| `updateAdminRoleInfo` | `POST /admin/updateAdminRoleInfo.json` |
| `updateRoleStateList` | `POST /admin/updateRoleStateList.json` |

**必填项**

| 标签 |
|---|
| * 角色名称 |
| * 状态 |

**表单标签**

| 标签 |
|---|
| * 角色名称 |
| * 状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.roleName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showMsg()` |

**跳转到**：`roleAdmin`
