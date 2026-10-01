# 14｜模块 hospital 机构/门店/科室

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/hospital/` |
| 中文名 | 机构/门店/科室 |
| 开发波次 | W1 |
| 页面数 | **11** |
| 端点数（去重） | **20** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `hospital.updateHospital.addDepartment` | `/addDepartment` | `views/hospital/addDepartment.html` | `addDepartmentCtrl` | 0 |
| 2 | `addHospital` | `/addHospital` | `views/hospital/addHospital.html` | `addHospitalCtrl` | 0 |
| 3 | `hospital.updateHospital.adminClinic` | `/adminClinic` | `views/hospital/adminClinic.html` | `adminClinicCtrl` | 6 |
| 4 | `hospital.updateHospital.adminMap` | `/adminMap` | `views/hospital/adminMap.html` | `adminMapCtrl` | 4 |
| 5 | `hospital.updateHospital.departmentList` | `/updateDepartment` | `views/hospital/departmentList.html` | `departmentListCtrl` | 0 |
| 6 | `hospital.updateHospital.employeeList` | `/employeeList` | `views/hospital/employeeList.html` | `employeeListCtrl` | 3 |
| 7 | `hospital` | `/hospital` | `views/hospital/hospital.html` | `hospitalCtrl` | 0 |
| 8 | `hospital.hospitallist` | `/hospitallist` | `views/hospital/hospitalList.html` | `hospitalListCtrl` | 8 |
| 9 | `hospital.updateHospital.updateDepartment` | `/updateDepartment?departmentId` | `views/hospital/updateDepartment.html` | `updateDepartmentCtrl` | 0 |
| 10 | `hospital.updateHospital.adminHospital` | `/adminHospital` | `views/hospital/updateHospital.adminHospital.html` | `updateAdminHospitalCtrl` | 0 |
| 11 | `hospital.updateHospital` | `/updateHospital?id&companyId` | `views/hospital/updateHospital.html` | `updateHospitalCtrl` | 1 |

## §2 端点清单（去重 20 个）

- `POST /admin/addConsultRoom.json`
- `POST /admin/changeCompanyStatus.json`
- `POST /admin/deleteDepartment.json`
- `POST /admin/getAllCityMap.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getConsultRoomVo.json`
- `POST /admin/getDepartmentInfo.json`
- `POST /admin/getDepartmentList.json`
- `POST /admin/getExamineVoList.json`
- `POST /admin/getHospitalInfo.json`
- `POST /admin/saveEmployeeAvatar.json`
- `POST /admin/selectConsultRoomVoListOfCompany.json`
- `POST /admin/selectEmployeeVoList.json`
- `POST /admin/setDoctorApproved.json`
- `POST /admin/setEmployeeRank.json`
- `POST /admin/updateConsultRoomInfo.json`
- `POST /admin/updateConsultRoomStatus.json`
- `POST /admin/updateDepartment.json`
- `POST /admin/updateHospital.json`
- `POST /admin/updateHospitalMap.json`

## §3 逐页字段规格

### 14.1 `hospital.updateHospital.addDepartment`

- **URL**：`/addDepartment`
- **模板**：`views/hospital/addDepartment.html`
- **控制器**：`addDepartmentCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 部门名称： |
| 部门图片： |
| 点击选择图片 |
| rank： |
| 描述信息： |

**表格列**

| # | 列名 |
|--:|---|
| 1 | Filename |
| 2 | Size |
| 3 | Detail |
| 4 | Filename |
| 5 | Size |
| 6 | Detail |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `object.departmentName` |
| `object.departPictures` |
| `object.rank1` |
| `object.departDesc` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `f.name` |
| `progress` |
| `errorMsg` |
| `keyimg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `uploadimg()` |
| `toggleactive()` |
| `selectImg()` |
| `addDepartment()` |
| `loadimg()` |
| `ok()` |
| `cancel()` |

### 14.2 `addHospital`

- **URL**：`/addHospital`
- **模板**：`views/hospital/addHospital.html`
- **控制器**：`addHospitalCtrl`
- **端点数**：0

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.companyName` |
| `obj.province` |
| `obj.city` |
| `obj.description` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `copinfoFactory.result.object.companyLimit` |
| `corpInfo.companyTitle` |
| `corpInfo.` |
| `companyTitle` |
| `province` |
| `city` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `update()` |

**跳转到**：`hospital.hospitallist`

### 14.3 `hospital.updateHospital.adminClinic`

- **URL**：`/adminClinic`
- **模板**：`views/hospital/adminClinic.html`
- **控制器**：`adminClinicCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `addConsultRoom` | `POST /admin/addConsultRoom.json` |
| `getConsultRoomVo` | `POST /admin/getConsultRoomVo.json` |
| `getExamineVoList` | `POST /admin/getExamineVoList.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |
| `updateConsultRoomInfo` | `POST /admin/updateConsultRoomInfo.json` |
| `updateConsultRoomStatus` | `POST /admin/updateConsultRoomStatus.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 诊室名称 |
| 2 | 就诊位置 |
| 3 | 备注 |
| 4 | 检查项 |
| 5 | 状态 |
| 6 | 操作 |
| 7 | 选择 |
| 8 | 检查名称 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.consultRoom.status` |
| `clinicPopout.params.remark` |
| `keyword` |
| `clinicPopout.params.consultRoomName` |
| `clinicPopout.params.consultRoomAddress` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.consultRoom.consultRoomName` |
| `item.consultRoom.consultRoomAddress` |
| `item.consultRoom.remark` |
| `item.examineList` |
| `concatStr` |
| `examineName` |
| `clinicPopout.title` |
| `item.examine.examineName` |
| `companyInfo.companyName` |
| `consultRoomName` |
| `consultRoomQrcode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `clinicPopout.showP(true)` |
| `setLine(item,$index)` |
| `printConsultRoomQrCode(item,item.consultRoom.id)` |
| `choseSingle(item,$index)` |
| `clinicPopout.submit()` |
| `clinicPopout.showP(false)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 14.4 `hospital.updateHospital.adminMap`

- **URL**：`/adminMap`
- **模板**：`views/hospital/adminMap.html`
- **控制器**：`adminMapCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getAllCityMap` | `POST /admin/getAllCityMap.json` |
| `getDepartmentList` | `POST /admin/getDepartmentList.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `updateHospitalMap` | `POST /admin/updateHospitalMap.json` |

**表单标签**

| 标签 |
|---|
| 省份： |
| 城市： |
| 搜索： |
| 纬度： |
| 经度： |
| 修改地址： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.province` |
| `obj.city` |
| `add` |
| `obj.address` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `province` |
| `city` |
| `obj.latitude` |
| `obj.longitude` |

**页面动作（ng-click）**

| 动作 |
|---|
| `mapDepartment()` |

### 14.5 `hospital.updateHospital.departmentList`

- **URL**：`/updateDepartment`
- **模板**：`views/hospital/departmentList.html`
- **控制器**：`departmentListCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `index` |
| `item.departmentName` |

**跳转到**：`hospital.updateHospital.addDepartment`

### 14.6 `hospital.updateHospital.employeeList`

- **URL**：`/employeeList`
- **模板**：`views/hospital/employeeList.html`
- **控制器**：`employeeListCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectEmployeeVoList` | `POST /admin/selectEmployeeVoList.json` |
| `setDoctorApproved` | `POST /admin/setDoctorApproved.json` |
| `setEmployeeRank` | `POST /admin/setEmployeeRank.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.employeeCompany.rank1` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.employee.employeeName` |
| `item.employee.mobile` |
| `item.doctorExamine.approved` |

**页面动作（ng-click）**

| 动作 |
|---|
| `approveEmployee(item.employee.id,1-item.doctorExamine.approved)` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in employeerank
```

### 14.7 `hospital`

- **URL**：`/hospital`
- **模板**：`views/hospital/hospital.html`
- **控制器**：`hospitalCtrl`
- **端点数**：0

### 14.8 `hospital.hospitallist`

- **URL**：`/hospitallist`
- **模板**：`views/hospital/hospitalList.html`
- **控制器**：`hospitalListCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeCompanyStatus` | `POST /admin/changeCompanyStatus.json` |
| `deleteDepartment` | `POST /admin/deleteDepartment.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getDepartmentInfo` | `POST /admin/getDepartmentInfo.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `saveEmployeeAvatar` | `POST /admin/saveEmployeeAvatar.json` |
| `updateDepartment` | `POST /admin/updateDepartment.json` |
| `updateHospital` | `POST /admin/updateHospital.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 医院名称 |
| 2 | 客服电话 |
| 3 | 地址 |
| 4 | {{corpInfo.employeeTitle}}数 |
| 5 | 状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `item.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.id` |
| `item.companyName` |
| `corpInfo.employeeTitle` |
| `item.phone` |
| `item.province` |
| `item.city` |
| `item.address` |
| `item.employeeCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `goHospital(item.id)` |
| `changeStatusStop($event)` |

**跳转到**：`addHospital`

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 14.9 `hospital.updateHospital.updateDepartment`

- **URL**：`/updateDepartment?departmentId`
- **模板**：`views/hospital/updateDepartment.html`
- **控制器**：`updateDepartmentCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 部门名称： |
| 部门图片： |
| 点击选择图片--> <!-- |
| rank： |
| 描述信息： |
| 点击选择图片 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `updateDepartmentFactory.object.departmentName` |
| `updateDepartmentFactory.object.departPictures` |
| `updateDepartmentFactory.object.rank1` |
| `updateDepartmentFactory.object.departDesc` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `keyimg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `uploadimg()` |
| `toggleactive()` |
| `selectImg()` |
| `modifyDepartment()` |
| `deleteDepartment()` |
| `loadimg()` |
| `ok()` |
| `cancel()` |

### 14.10 `hospital.updateHospital.adminHospital`

- **URL**：`/adminHospital`
- **模板**：`views/hospital/updateHospital.adminHospital.html`
- **控制器**：`updateAdminHospitalCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{corpInfo. companyTitle}}名： 图片： |
| 点击选择图片 |
| logo： |
| 电话： |
| 描述信息： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `updateHospitalFactory.object.companyName` |
| `updateHospitalFactory.object.logo` |
| `updateHospitalFactory.object.phone` |
| `updateHospitalFactory.object.description` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `keyimg` |
| `myCroppedImage` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseImg()` |
| `selectImg()` |
| `modify()` |
| `backhome()` |
| `getBaseCode()` |
| `imgModalModify=false` |
| `loadimg()` |
| `toggleactive()` |
| `ok()` |
| `cancel()` |

### 14.11 `hospital.updateHospital`

- **URL**：`/updateHospital?id&companyId`
- **模板**：`views/hospital/updateHospital.html`
- **控制器**：`updateHospitalCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `hospitalFactory.object.companyName` |
| `corpInfo.employeeTitle` |
| `corpInfo.` |
| `companyTitle` |

**页面动作（ng-click）**

| 动作 |
|---|
| `indexTab=1` |
| `indexTab=2` |
| `indexTab=4` |
| `indexTab=3` |
| `onClick(1)` |
| `onClick(2)` |
| `onClick(4)` |
| `onClick(3)` |
| `onClick(5)` |

**跳转到**：`hospital.hospitallist`, `hospital.updateHospital.departmentList`, `hospital.updateHospital.employeeList`
