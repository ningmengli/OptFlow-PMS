# 09｜模块 clinic 叫号/队列/大屏

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/clinic/` |
| 中文名 | 叫号/队列/大屏 |
| 开发波次 | W2 |
| 页面数 | **8** |
| 端点数（去重） | **39** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `adminCall` | `/adminCall` | `views/clinic/adminCall.html` | `adminCallCtrl` | 9 |
| 2 | `bigScreen` | `/bigScreen` | `views/clinic/bigScreen.html` | `bigScreenCtrl` | 3 |
| 3 | `checkCall` | `/checkCall` | `views/clinic/checkCall.html` | `checkCallCtrl` | 12 |
| 4 | `consultingScreen` | `/consultingScreen` | `views/clinic/consultingScreen.html` | `consultingScreenCtrl` | 3 |
| 5 | `doctorWorkbench` | `/doctorWorkbench` | `views/clinic/doctorWorkbench.html` | `doctorWorkbenchCtrl` | 11 |
| 6 | `queueMachine` | `/queueMachine` | `views/clinic/queueMachine.html` | `queueMachineCtrl` | 5 |
| 7 | `queueMachineConfig` | `/queueMachineConfig?queueMachineId` | `views/clinic/queueMachineConfig.html` | `queueMachineConfigCtrl` | 2 |
| 8 | `screenQueue` | `/screenQueue?bigScreenId` | `views/clinic/screenQueue.html` | `screenQueueCtrl` | 2 |

## §2 端点清单（去重 39 个）

- `POST /admin/beginCustomerCheckin.json`
- `POST /admin/callNextExamineQueueMain.json`
- `POST /admin/callingEmployeeCheckinQueue.json`
- `POST /admin/callingExamineQueueMain.json`
- `POST /admin/callingExamineQueueWhenNotSignIn.json`
- `POST /admin/callingWaitingCheckinQueue.json`
- `POST /admin/callingWaitingExamineQueueMain.json`
- `POST /admin/closeNowCallingCheckinQueue.json`
- `POST /admin/closeNowCallingExamineQueueMain.json`
- `POST /admin/deleteQueueMachine.json`
- `POST /admin/getBigScreenConfVo.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getConsultRoomScreenVo.json`
- `POST /admin/getEmployeeConsultRoomVo.json`
- `POST /admin/getEmployeeExamineConsultRoomVo.json`
- `POST /admin/getNowCallingCheckinQueue.json`
- `POST /admin/getNowCallingCheckinQueueOfBigScreen.json`
- `POST /admin/getNowCallingExamineQueueMain.json`
- `POST /admin/getQueueMachineVo.json`
- `POST /admin/restartEmployeeCheckinQueue.json`
- `POST /admin/selectBigScreenConfVoListOfCompany.json`
- `POST /admin/selectBigScreenQueueVoList.json`
- `POST /admin/selectConsultRoomScreenVoList.json`
- `POST /admin/selectConsultRoomVoListOfCompany.json`
- `POST /admin/selectCustomerCheckinVoListOfCompany.json`
- `POST /admin/selectEmployeeCheckinQueueVoList.json`
- `POST /admin/selectEmployeeCheckinQueueVoListOfBigScreen.json`
- `POST /admin/selectEmployeeVoList.json`
- `POST /admin/selectMedicalExamineQueueMainVoList.json`
- `POST /admin/selectMedicalExamineSignInVoList.json`
- `POST /admin/selectQueueMachineVoList.json`
- `POST /admin/setConsultRoomOfEmployee.json`
- `POST /admin/setEmployeeConsultRoomStatus.json`
- `POST /admin/setEmployeeManageBigScreenId.json`
- `POST /admin/setExamineConsultRoomOfEmployee.json`
- `POST /admin/startExamine.json`
- `POST /admin/topEmployeeCheckinQueue.json`
- `POST /admin/updateQueueMachine.json`
- `POST /auth/getMyAdminCorpList.json`

## §3 逐页字段规格

### 9.1 `adminCall`

- **URL**：`/adminCall`
- **模板**：`views/clinic/adminCall.html`
- **控制器**：`adminCallCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getEmployeeConsultRoomVo` | `POST /admin/getEmployeeConsultRoomVo.json` |
| `getNowCallingCheckinQueueOfBigScreen` | `POST /admin/getNowCallingCheckinQueueOfBigScreen.json` |
| `restartEmployeeCheckinQueue` | `POST /admin/restartEmployeeCheckinQueue.json` |
| `selectBigScreenConfVoListOfCompany` | `POST /admin/selectBigScreenConfVoListOfCompany.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |
| `selectEmployeeCheckinQueueVoListOfBigScreen` | `POST /admin/selectEmployeeCheckinQueueVoListOfBigScreen.json` |
| `selectEmployeeVoList` | `POST /admin/selectEmployeeVoList.json` |
| `setEmployeeManageBigScreenId` | `POST /admin/setEmployeeManageBigScreenId.json` |
| `topEmployeeCheckinQueue` | `POST /admin/topEmployeeCheckinQueue.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 手机号 |
| 3 | 诊室 |
| 4 | 医师 |
| 5 | 排队号 |
| 6 | 状态 |
| 7 | 操作 |
| 8 | 选择 |
| 9 | 叫号大屏名称 |
| 10 | 诊室 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `clinicPopout.index` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `clinicInfo.bigScreen.bigScreenName` |
| `callNow` |
| `concatStr` |
| `patient.patientName` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `item.consultRoom.consultRoomName` |
| `item.employee.employeeName` |
| `item.employeeCheckinQueue.queueNumber` |
| `paddingZero` |
| `temp.name` |
| `iten.name` |
| `item.bigScreen.bigScreenName` |
| `item.consultRoomListFilter` |

**页面动作（ng-click）**

| 动作 |
|---|
| `clinicPopout.showP(true)` |
| `refresh()` |
| `dealWithBtn(iten.status,item)` |
| `clinicPopout.submit()` |

### 9.2 `bigScreen`

- **URL**：`/bigScreen`
- **模板**：`views/clinic/bigScreen.html`
- **控制器**：`bigScreenCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBigScreenConfVo` | `POST /admin/getBigScreenConfVo.json` |
| `selectBigScreenConfVoListOfCompany` | `POST /admin/selectBigScreenConfVoListOfCompany.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 大屏编号 |
| 2 | 叫号大屏名称 |
| 3 | 诊室 |
| 4 | 场景 |
| 5 | 显示内容 |
| 6 | 操作 |
| 7 | 选择 |
| 8 | 诊室名称 |
| 9 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `bigScreenPopout.bigScreenName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyInfo.companyName` |
| `item.bigScreen.screenNumber` |
| `item.bigScreen.bigScreenName` |
| `item.consultRoomVoList` |
| `concatStr` |
| `consultRoom.consultRoomName` |
| `item.bigScreen.sceneType` |
| `consultRoomSceneType` |
| `item.showFilter` |
| `bigScreenPopout.title` |
| `item.consultRoom.consultRoomName` |
| `item.consultRoom.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `bigScreenPopout.showP(true)` |
| `bigScreenPopout.showP(true,item,$index)` |
| `screenful(item)` |
| `bigScreenPopout.setSceneType(1)` |
| `bigScreenPopout.setSceneType(2)` |
| `bigScreenPopout.choseSingle(item,$event)` |
| `bigScreenPopout.submit()` |
| `bigScreenPopout.showP(false)` |

### 9.3 `checkCall`

- **URL**：`/checkCall`
- **模板**：`views/clinic/checkCall.html`
- **控制器**：`checkCallCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `callNextExamineQueueMain` | `POST /admin/callNextExamineQueueMain.json` |
| `callingExamineQueueMain` | `POST /admin/callingExamineQueueMain.json` |
| `callingExamineQueueWhenNotSignIn` | `POST /admin/callingExamineQueueWhenNotSignIn.json` |
| `callingWaitingExamineQueueMain` | `POST /admin/callingWaitingExamineQueueMain.json` |
| `closeNowCallingExamineQueueMain` | `POST /admin/closeNowCallingExamineQueueMain.json` |
| `getEmployeeExamineConsultRoomVo` | `POST /admin/getEmployeeExamineConsultRoomVo.json` |
| `getNowCallingExamineQueueMain` | `POST /admin/getNowCallingExamineQueueMain.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |
| `selectMedicalExamineQueueMainVoList` | `POST /admin/selectMedicalExamineQueueMainVoList.json` |
| `selectMedicalExamineSignInVoList` | `POST /admin/selectMedicalExamineSignInVoList.json` |
| `setExamineConsultRoomOfEmployee` | `POST /admin/setExamineConsultRoomOfEmployee.json` |
| `startExamine` | `POST /admin/startExamine.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 手机号 |
| 3 | 诊室 |
| 4 | 检查项 |
| 5 | 叫号人 |
| 6 | 排队号 |
| 7 | 状态 |
| 8 | 操作 |
| 9 | 选择 |
| 10 | 诊室名称 |
| 11 | 检查项 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `clinicPopout.index` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `clinicInfo.consultRoom.consultRoomName` |
| `exam.examineName` |
| `callNum.medicalExamineQueueMain.queueNumber` |
| `paddingZero` |
| `callNum.patient.patientName` |
| `clinicInfo.examine.examineName` |
| `waitingList.count` |
| `clinicInfo.examineList` |
| `concatStr` |
| `examineName` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `item.medicalExamine.examineName` |
| `loop.looping` |
| `t.time` |
| `item.consultRoom.consultRoomName` |
| `item.medicalExamineList` |
| `medicalExamine.examineName` |
| `item.employee.employeeName` |
| `item.medicalExamineQueueMain.queueNumber` |
| `temp.setName` |
| `iten.name` |
| `weekInfo.monthTitle` |
| `date` |
| `yyyy` |
| `MM` |
| `week` |
| `filterWeek` |
| `week.date` |
| `dd` |
| `common.content` |
| `common.title` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setPopoutShow()` |
| `dealWithBtn(4,callNum)` |
| `dealWithBtn(2,callNum)` |
| `dealWithBtn(0,callNum)` |
| `nextStep()` |
| `queryWaitingList()` |
| `callingExamineQueueWhenNotSignIn(item)` |
| `autoLoop(timeListIndex)` |
| `setTime($index)` |
| `refresh()` |
| `dealWithBtn(iten.status,item)` |
| `weekInfo.setTime(false)` |
| `weekInfo.setTime(true)` |
| `weekInfo.setWeekChose($index)` |
| `common.fun()` |
| `clinicPopout.back()` |
| `clinicPopout.submit()` |

### 9.4 `consultingScreen`

- **URL**：`/consultingScreen`
- **模板**：`views/clinic/consultingScreen.html`
- **控制器**：`consultingScreenCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getConsultRoomScreenVo` | `POST /admin/getConsultRoomScreenVo.json` |
| `selectConsultRoomScreenVoList` | `POST /admin/selectConsultRoomScreenVoList.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 诊室屏编号 |
| 2 | 诊室屏名称 |
| 3 | 诊室 |
| 4 | 场景 |
| 5 | 显示内容 |
| 6 | 温馨提醒 |
| 7 | 操作 |
| 8 | 选择 |
| 9 | 诊室名称 |
| 10 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `keyword` |
| `consultingScreenPopout.roomScreenName` |
| `consultingScreenPopout.roomScreenRemark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `companyInfo.companyName` |
| `item.consultRoomScreen.screenNumber` |
| `item.consultRoomScreen.roomScreenName` |
| `item.consultRoomVo.consultRoom.consultRoomName` |
| `item.consultRoomScreen.sceneType` |
| `consultRoomSceneType` |
| `item.showFilter` |
| `item.consultRoomScreen.roomScreenRemark` |
| `consultingScreenPopout.title` |
| `item.consultRoom.consultRoomName` |
| `item.consultRoom.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `consultingScreenPopout.showP(true)` |
| `consultingScreenPopout.showP(true,item,$index)` |
| `consultingScreenPopout.setSceneType(1)` |
| `consultingScreenPopout.setSceneType(2)` |
| `consultingScreenPopout.choseSingle(item)` |
| `consultingScreenPopout.submit()` |
| `consultingScreenPopout.showP(false)` |

### 9.5 `doctorWorkbench`

- **URL**：`/doctorWorkbench`
- **模板**：`views/clinic/doctorWorkbench.html`
- **控制器**：`doctorWorkbenchCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `beginCustomerCheckin` | `POST /admin/beginCustomerCheckin.json` |
| `callingEmployeeCheckinQueue` | `POST /admin/callingEmployeeCheckinQueue.json` |
| `callingWaitingCheckinQueue` | `POST /admin/callingWaitingCheckinQueue.json` |
| `closeNowCallingCheckinQueue` | `POST /admin/closeNowCallingCheckinQueue.json` |
| `getEmployeeConsultRoomVo` | `POST /admin/getEmployeeConsultRoomVo.json` |
| `getNowCallingCheckinQueue` | `POST /admin/getNowCallingCheckinQueue.json` |
| `selectConsultRoomVoListOfCompany` | `POST /admin/selectConsultRoomVoListOfCompany.json` |
| `selectCustomerCheckinVoListOfCompany` | `POST /admin/selectCustomerCheckinVoListOfCompany.json` |
| `selectEmployeeCheckinQueueVoList` | `POST /admin/selectEmployeeCheckinQueueVoList.json` |
| `setConsultRoomOfEmployee` | `POST /admin/setConsultRoomOfEmployee.json` |
| `setEmployeeConsultRoomStatus` | `POST /admin/setEmployeeConsultRoomStatus.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 手机号 |
| 3 | 诊室 |
| 4 | 医师 |
| 5 | 排队号 |
| 6 | 状态 |
| 7 | 操作 |
| 8 | 选择 |
| 9 | 诊室名称 |
| 10 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `clinicPopout.index` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `clinicInfo.consultRoom.consultRoomName` |
| `callNum.employeeCheckinQueue.queueNumber` |
| `paddingZero` |
| `callNum.patient.patientName` |
| `waitingList.count` |
| `item.customerCheckin.checkinNumber` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `loop.looping` |
| `t.time` |
| `item.consultRoom.consultRoomName` |
| `item.employee.employeeName` |
| `temp.setName` |
| `iten.name` |
| `weekInfo.monthTitle` |
| `date` |
| `yyyy` |
| `MM` |
| `week` |
| `filterWeek` |
| `week.date` |
| `dd` |
| `common.content` |
| `common.title` |
| `item.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setPopoutShow()` |
| `nextStep()` |
| `toClinic(0)` |
| `toClinic(1)` |
| `queryWaitingList()` |
| `autoLoop(timeListIndex)` |
| `setTime($index)` |
| `refresh()` |
| `dealWithBtn(iten.status,item)` |
| `weekInfo.setTime(false)` |
| `weekInfo.setTime(true)` |
| `weekInfo.setWeekChose($index)` |
| `common.fun()` |
| `clinicPopout.back()` |
| `clinicPopout.submit()` |

### 9.6 `queueMachine`

- **URL**：`/queueMachine`
- **模板**：`views/clinic/queueMachine.html`
- **控制器**：`queueMachineCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteQueueMachine` | `POST /admin/deleteQueueMachine.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getQueueMachineVo` | `POST /admin/getQueueMachineVo.json` |
| `selectQueueMachineVoList` | `POST /admin/selectQueueMachineVoList.json` |
| `getMyAdminCorpList` | `POST /auth/getMyAdminCorpList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 叫号机序列号 |
| 2 | 叫号机备注 |
| 3 | 门店名称 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `deviceInfo.machineCode` |
| `deviceInfo.remark` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getQueueListFactory.count` |
| `item.queueMachine.machineCode` |
| `item.queueMachine.remark` |
| `item.company.companyName` |
| `deviceModalOptions.type` |
| `deviceModalOptions.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAdd()` |
| `updateDevice(item,$index)` |
| `configDevice(item)` |
| `deleteDevice(item.queueMachine.id)` |
| `addDevice()` |
| `addDeviceModal=false` |

### 9.7 `queueMachineConfig`

- **URL**：`/queueMachineConfig?queueMachineId`
- **模板**：`views/clinic/queueMachineConfig.html`
- **控制器**：`queueMachineConfigCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getQueueMachineVo` | `POST /admin/getQueueMachineVo.json` |
| `updateQueueMachine` | `POST /admin/updateQueueMachine.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.value` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `index` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `affirm()` |

### 9.8 `screenQueue`

- **URL**：`/screenQueue?bigScreenId`
- **模板**：`views/clinic/screenQueue.html`
- **控制器**：`screenQueueCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getNowCallingCheckinQueueOfBigScreen` | `POST /admin/getNowCallingCheckinQueueOfBigScreen.json` |
| `selectBigScreenQueueVoList` | `POST /admin/selectBigScreenQueueVoList.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `setCompanyModal.companyName` |
| `time.today` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `time.weekDay` |
| `filterWeek` |
| `HH` |
| `mm` |
| `clinic.consultRoom.consultRoomName` |
| `clinic.employee.employeeName` |
| `clinic.doing.customerCheckin.checkinNumber` |
| `paddingZero` |
| `clinic.doing.patient.patientName` |
| `filterName` |
| `item.customerCheckin.checkinNumber` |
| `item.patient.patientName` |
| `storeBigScreenIdList` |
| `callSb.callIndex` |
| `consultRoomName` |
| `checkinNumber` |
| `patientName` |
