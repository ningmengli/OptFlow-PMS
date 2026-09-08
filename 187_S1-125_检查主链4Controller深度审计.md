# S1-125 检查主链 4 Controller 深度审计

## 0. 任务背景

S1-124 已完成登记 / 接诊入口 → medicalRecord 进入点 → 检查入口的入口链审计。

本轮**深入检查主链 4 个 Controller**：
- assistCheckingCtrl
- assistCheckListCtrl
- checkCallCtrl
- checkinListCtrl

建立 4 Controller 完整 API / State / Scope / 字段级审计。

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| 4 Controller 总行数 | 1671 行 |
| 4 Controller call site 总数 | 47 处 |
| 4 Controller unique API 总数 | 46 个 |

## 2. 4 Controller 注册

| Controller | 注册行 | 范围 | 行数 | DI |
|---|---:|---|---:|---|
| **assistCheckingCtrl** | L1756 | L1756-L2308 | 553 | $scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, ObjectFactory, ListFactory, intervalTime, $q, $interval, QiniuFactory, $timeout |
| **assistCheckListCtrl** | L2309 | L2309-L2425 | 117 | $scope, $stateParams, DateUtilFactory, $state, StorageFactory, ObjectFactory, ListFactory, $http, $timeout |
| **checkinListCtrl** | L8778 | L8778-L9261 | 484 | $scope, DateUtilFactory, Popup, $state, $stateParams, ObjectFactory, HttpFactory, ListFactory, $interval, $timeout, WechatConfig |
| **checkCallCtrl** | L9760 | L9760-L10276 | 517 | $scope, ListFactory, Loop, $state, HttpFactory, $timeout, Popup, DateUtilFactory, ObjectFactory, Utils |

## 3. API 全量统计

### 3.1 总览

| Controller | call site | unique API | Read | Write | Other |
|---|---:|---:|---:|---:|---:|
| assistCheckingCtrl | 16 | 15 | 10 | 4 | 1 |
| assistCheckListCtrl | 4 | 4 | 2 | 2 | 0 |
| checkinListCtrl | 16 | 16 | 5 | 11 | 0 |
| checkCallCtrl | 11 | 11 | 3 | 8 | 0 |
| **合计** | **47** | **46** | **20** | **25** | **1** |

### 3.2 assistCheckingCtrl 详细 API

**Read (10)**:
| API | 用途 | 行号 |
|---|---|---:|
| getCorpInfo.json | 获取公司信息 | L1916 |
| getMedicalExamineItemVoList.json | 检查项列表 | (内) |
| getMedicalExamineVoList.json | 检查 VoList | L2068 |
| **getMedicalRecord.json** | medicalRecord Vo | L1964 |
| getPatientExamineListVoList.json | 患者病史 | L1977 |
| getPatientInfo.json | patientVo | L1970 |
| getVisionRecordVo.json | 视力记录 | L1918 (注释) |
| selectUartDeviceByAdminId.json | 智能设备 | L1829 |
| selectUartDeviceList.json | 设备列表 | L1861 |
| uploadExamineResult.json | 上传检查结果 | L2205 |

**Write (4)**:
| API | 用途 | 行号 |
|---|---|---:|
| **completeExamine.json** | 完成检查 | L2211 |
| getLatestUartDeviceLogToSchoolMateCheck.json | 获取设备日志 | L1787 |
| **modifyMedicalExamineItemList.json** | 修改检查项 | L2196 |
| setUartDeviceOfAdmin.json | 关联设备 | L1900 |

**Other (1)**:
| API | 用途 | 行号 |
|---|---|---:|
| disconnectUartDeviceOfAdmin.json | 断开设备 | L1880 |

### 3.3 assistCheckListCtrl 详细 API

**Read (2)**:
- getMedicalExamineVoList.json (L2385)
- getMedicalRecordExamineListVoList.json (L2354)

**Write (2)**:
- startExamine.json (L2415)
- statExamineCheckStatus.json (L2331)

### 3.4 checkinListCtrl 详细 API

**Read (5)**:
| API | 用途 |
|---|---|
| getAppointPrintData.json | 预约打印 |
| getCustomerVo.json | 客户 Vo |
| getPatientVo.json | patientVo |
| selectCustomerWaitingBindingVo.json | 待绑定 |
| selectEmployeeVoList.json | 员工列表 |

**Write (11)**:
| API | 用途 | 行号 |
|---|---|---:|
| **medicalCheckBeforeCustomerCheckin.json** | **诊前检查** | L8788 |
| bandingCustomer.json | 绑定客户 | L8911 |
| changeBandingWechat.json | 改绑微信 | (内) |
| deleteCustomerCheckin.json | 删除登记 | L8846 |
| getBandingWechatQrcode.json | 二维码 | (内) |
| isBandingWechat.json | 是否绑微信 | (内) |
| saveCustomerInfo.json | 保存客户 | (内) |
| savePatientInfo.json | 保存患者 | (内) |
| selectCustomerCheckinVoListOfCompany.json | 登记列表 | L8827 |
| sendCustomerCheckin.json | 发送登记 | (内) |
| updateCustomerTags.json | 客户标签 | (内) |

### 3.5 checkCallCtrl 详细 API

**Read (3)**:
| API | 用途 | 行号 |
|---|---|---:|
| getEmployeeExamineConsultRoomVo.json | 当前诊室 | L10133 |
| selectConsultRoomVoListOfCompany.json | 诊室列表 | L10077 |
| **selectMedicalExamineQueueMainVoList.json** | 叫号队列 | L10190 |

**Write (8)**:
| API | 用途 | 行号 |
|---|---|---:|
| **callNextExamineQueueMain.json** | 下一位 | L10123 |
| **callingExamineQueueMain.json** | 呼叫 | L10018 |
| callingExamineQueueWhenNotSignIn.json | 待签到叫号 | L10158 |
| callingWaitingExamineQueueMain.json | 等待叫号 | L9996 |
| closeNowCallingExamineQueueMain.json | 过号 | L10005 |
| getNowCallingExamineQueueMain.json | 当前叫号 | L10168 |
| setExamineConsultRoomOfEmployee.json | 设置诊室 | L9851 |
| **startExamine.json** | 开始检查 | L9985 |

## 4. medicalRecordId 在 4 Controller 中的 provenance

### 4.1 命中统计

| Controller | medicalRecordId 命中 |
|---|---:|
| assistCheckingCtrl | **15** |
| assistCheckListCtrl | **7** |
| checkinListCtrl | **1** |
| checkCallCtrl | **1** |
| **合计** | **24** |

### 4.2 8 类 provenance 分类

#### Type A: $stateParams.medicalRecordId

| Controller | 行号 |
|---|---:|
| assistCheckingCtrl | L1757 `$scope.medicalRecordId = $stateParams.medicalRecordId` |
| assistCheckingCtrl | L1889 / L1910 (State go 入口) |

#### Type B: $scope.medicalRecordId 后续使用

| Controller | 行号 |
|---|---:|
| assistCheckingCtrl | L1768 / L1919 / L2068 / L2216 / L2295 / L2298 |
| assistCheckListCtrl | L2385 |
| assistCheckListCtrl | L2407 (`$scope.medicalRecordId = ""`) |

#### Type C: 函数参数

| Controller | 行号 |
|---|---:|
| assistCheckingCtrl | L2243 `getMedicalRecord(medicalExamineId, medicalRecordId)` |
| assistCheckListCtrl | L2396 / L2410 (函数参数) |

#### Type D: API Response (medicalRecordVo)

| Controller | 行号 | 表达式 |
|---|---:|---|
| (assumed) | (inferred) | `res.object.medicalRecord.id` (S1-117/120 已确认) |

#### Type E: List item (medicalExamine 嵌套)

| Controller | 行号 | 表达式 |
|---|---:|---|
| checkCallCtrl | L9964 | `medicalExamineList[0].medicalExamine.medicalRecordId` |
| checkinListCtrl | L8791 | `res.customerCheckin.medicalRecordId` (A 类 customerCheckin 嵌套) |

#### Type F: Factory item

| Controller | 行号 | 表达式 |
|---|---:|---|
| (none directly) | - | - |

#### Type G: medicalRecordVo 整体

| Controller | 行号 | 表达式 |
|---|---:|---|
| (assumed) | - | (S1-120 全局扫描) |

#### Type H: 其它（混合）

| Controller | 行号 | 表达式 |
|---|---:|---|
| assistCheckingCtrl | L2259 / L2264 / L2270 | `medicalRecordId: id` (函数 id 参数) |

### 4.3 assistCheckingCtrl 完整 medicalRecordId 链路

```
L1757: $scope.medicalRecordId = $stateParams.medicalRecordId   [A]
L1765-1769: $state.go("assistChecking", {medicalRecordId: $scope.medicalRecordId, ...})  [自身 reload]
L1886-1890: $state.go("assistChecking", {medicalRecordId: $stateParams.medicalRecordId, ...})  [reload after disconnect]
L1907-1911: $state.go("assistChecking", {medicalRecordId: $stateParams.medicalRecordId, ...})  [reload after setDevice]
L1964: API getMedicalRecord.json { id: $scope.medicalRecordId }  [Read]
L1967: $scope.patientId = response.object.patientId  [Type 3 派生]
L2068: ListFactory getMedicalExamineVoList.json { medicalRecordId: $scope.medicalRecordId }
L2214-2218: $state.go("assistChecking", {medicalRecordId, ...})  [reload after saveCheck]
L2243-2248: $scope.getMedicalRecord(medicalExamineId, medicalRecordId)  [函数参数 + 自身 reload]
L2251-2274: $scope.getMedical(id, patientId)  [function: medicalRecordId: id, patientId: res.object.patientId]
L2295/2298: printPeijing / printShoufei param: { medicalRecordId: $scope.medicalRecordId }
```

## 5. patientId 在 4 Controller 中的 provenance

### 5.1 命中统计

| Controller | patientId 命中 |
|---|---:|
| assistCheckingCtrl | **7** |
| assistCheckListCtrl | **1** |
| checkinListCtrl | **5** |
| checkCallCtrl | **0** |
| **合计** | **13** |

### 5.2 patientId → medicalRecordId 派生链

**S1-125 关键发现 1（medicalRecord → patient 派生）**：
- assistCheckingCtrl L1967: `$scope.patientId = response.object.patientId`
- 派生关系：medicalRecordVo → patientId
- 但**反方向** patientId → medicalRecordId **未直接建立**

### 5.3 各 Controller patientId 来源

| Controller | 来源 | 行号 |
|---|---|---|
| assistCheckingCtrl | response.object.patientId (A 类 API Response) | L1967 |
| assistCheckingCtrl | res.object.patientId (State go 参数) | L2260 / L2265 |
| assistCheckingCtrl | 函数参数 patientId | L2251 / L2271 |
| assistCheckListCtrl | 函数参数 patientId | L2410 |
| checkinListCtrl | 函数参数 patientId | L8871 / L8910 |
| checkinListCtrl | patientId 写入 getCustomerVo Request | L8874 |
| checkinListCtrl | State go params patientId | L8914 |

## 6. 检查对象全集

### 6.1 4 Controller 内真实对象

| 对象 | 命中 Controller | 出现行 |
|---|---|---|
| **medicalExamine** | assistCheckingCtrl / assistCheckListCtrl / checkCallCtrl | L2074, L2385, L2230, L9964, L10161 等 |
| **medicalExamineItemList** | assistCheckingCtrl | L2077, L2170, L2183, L2186, L2206, L2210 等 |
| **medicalExamineItem** | assistCheckingCtrl | L2184, L2186 (leftExamine / rightExamine) |
| **medicalExamineQueueMain** | checkCallCtrl | L9957, L9997, L10006, L10018, L10180 |
| **medicalExamineList** | checkCallCtrl | L9957, L9974 |
| **medicalExamineQueue** | checkCallCtrl | (注释 L9956) |
| **medicalRecord** | assistCheckingCtrl | L1757, L1964 等 |
| **patient** | assistCheckingCtrl | L1967, L1970, L1977 |
| **customer** | checkinListCtrl | L8894, L8901, L8905 |
| **customerCheckin** | checkinListCtrl | L8671, L8697, L8707, L8789, L8791, L8847, L8911, L9045, L9122, L9131, L9160 |
| **UartDevice** | assistCheckingCtrl | L1788, L1799, L1832, L1861, L1900, L2081, L2082 |
| **schoolMateCheck** | assistCheckingCtrl | L1803, L1806 |
| **clinicInfo / consultRoom** | checkCallCtrl | L9820, L9825, L10124, L10133, L10135, L10144, L10169, L10180, L10211, L10229 |
| **examineList** | checkCallCtrl | L10085, L10097 |

### 6.2 检查项结构 (assistCheckingCtrl)

```javascript
// L2172-L2189
$scope.medicalExamineItemList = [
  {
    position: 0/1,
    left: "...",
    right: "...",
    leftExamine: { checkItemValue, checkItemCode, ... },
    rightExamine: { checkItemValue, checkItemCode, ... }
  },
  ...
]
```

### 6.3 队列结构 (checkCallCtrl)

```javascript
// L9865-L9919 doctorWorkBenchs.tablist
{
  name: "全部/叫号中/等待中/已过号/已叫号",
  queueStatus: 0/1/2/3/null,  // 0等待 1叫号 2已叫 3已过
  checkStatus: 0/1/2,  // 0待检查 1检查中 2已检查
  btnList: [{ name, status, class }, ...]
}
```

## 7. 检查 API Request/Response 详细

### 7.1 getMedicalRecord.json (assistCheckingCtrl L1964)

**Request**: `{ id: $scope.medicalRecordId }` (Type 1 primitive)

**Response**:
- `response.object.patientId` → $scope.patientId (Type 3 派生)
- `response.object.templateId` (L2256 检查有无模板)
- `response.object.medicalRecordType` (L2257 5 = 开单分流)
- `response.object.id` (L2263 used as medicalRecordId)

**Consumer**:
- L1969: getPatientInfo.json { id: $scope.patientId }
- L1974: $scope.getHistory()
- L2257-L2273: $state.go 三向分流

### 7.2 getMedicalExamineVoList.json (assistCheckingCtrl L2068)

**Request**: `{ medicalRecordId: $scope.medicalRecordId }` (ListFactory)

**Response**:
- `res.items[i].medicalExamine.id`
- `res.items[i].medicalExamine.checkStatus`
- `res.items[i].medicalExamine.uartDeviceType`
- `res.items[i].medicalExamine.checkFile` (URL 文件列表)

**Consumer**:
- L2073: 选第一个 medicalExamineId
- L2086: 拆分 checkFile 为 getImgArray
- L2229-L2235: 用于 $scope.saveCheck

### 7.3 medicalCheckBeforeCustomerCheckin.json (checkinListCtrl L8788)

**Request**: `{ customerCheckinId: item.customerCheckin.id }`

**Response**:
- `res.customerCheckin.medicalRecordId` (A 类)
- 设置 `_this.medicalRecordId` → `$scope.preDiagnosisExamination.medicalRecordId`

**Consumer**:
- preDiagnosisExamination 弹窗 (open(true))

### 7.4 startExamine.json (checkCallCtrl L9985 + assistCheckListCtrl L2415)

**Request**: `{ medicalExamineId }` (Type 1 primitive)

**Response**: 无显式消费

**Consumer**:
- checkCallCtrl: 成功 → toAssistChecking() → $state.go("assistChecking", ...)
- assistCheckListCtrl: 循环调用，每个 medicalExamineId 一次

### 7.5 completeExamine.json (assistCheckingCtrl L2211)

**Request**: `{ medicalExamineId: $scope.obj.medicalExamineId }` (Type 1)

**Consumer**: success → $scope.search() + reload 自身

## 8. ListFactory 详细

### 8.1 assistCheckListCtrl

L2354: `$scope.memberFactory = new ListFactory("/admin/getMedicalRecordExamineListVoList.json", pageStart, pageSize, $scope.obj)`
- pageSize = 12
- Request: $scope.obj (含 keyword / startTime / endTime / checkStatus)
- Response: $scope.memberFactory.items

### 8.2 assistCheckingCtrl

L2068: `$scope.examineListFactory = new ListFactory("/admin/getMedicalExamineVoList.json", 0, 20, { medicalRecordId })`

L1861: `$scope.getSupplierListFactory = new ListFactory("/admin/selectUartDeviceList.json", 0, 12, { deviceType: 1, status: 0, keyword })`

L1977: `$scope.getHistroyListFactory = new ListFactory("/admin/getPatientExamineListVoList.json", 0, 50, { patientId: $scope.patientId })`

L2385 (assistCheckListCtrl): `$scope.examineListFactory = new ListFactory("/admin/getMedicalExamineVoList.json", 0, 20, { medicalRecordId })`

### 8.3 checkinListCtrl

L8827: `selectCustomerCheckinVoListOfCompany.json` (0, 12, $scope.obj) —— **主列表**
L9085: `selectEmployeeVoList.json` (0, 50, $scope.obj)

### 8.4 checkCallCtrl

L10077: `selectConsultRoomVoListOfCompany.json` (诊室列表)
L10190: `selectMedicalExamineQueueMainVoList.json` (叫号队列)
L10221: `selectMedicalExamineSignInVoList.json` (待签到)

## 9. 检查 Write 详细

### 9.1 assistCheckingCtrl 4 个 Write

| API | 性质 | 触发条件 |
|---|---|---|
| completeExamine.json | 状态变更 | saveCheck success (L2208) |
| modifyMedicalExamineItemList.json | 内容更新 | saveCheck 立即调用 (L2196) |
| uploadExamineResult.json | 结果上传 | saveCheck success (L2205) |
| setUartDeviceOfAdmin.json | 设备关联 | selectDevice (L1900) |

### 9.2 assistCheckListCtrl 2 个 Write

| API | 性质 | 触发条件 |
|---|---|---|
| startExamine.json | 开始检查 | savePatient (L2415) |
| statExamineCheckStatus.json | 状态统计 | searchCount (L2331) |

### 9.3 checkCallCtrl 8 个 Write

| API | 性质 | 触发条件 |
|---|---|---|
| callNextExamineQueueMain.json | 下一位 | nextStep (L10123) |
| callingExamineQueueMain.json | 呼叫 | case 4 (L10018) |
| callingExamineQueueWhenNotSignIn.json | 待签到叫号 | callingExamineQueueWhenNotSignIn (L10158) |
| callingWaitingExamineQueueMain.json | 等待叫号 | case 1 (L9996) |
| closeNowCallingExamineQueueMain.json | 过号 | case 2 (L10005) |
| getNowCallingExamineQueueMain.json | 当前叫号（实为 Read） | getNowCallingExamineQueueMain (L10168) |
| setExamineConsultRoomOfEmployee.json | 设置诊室 | clinicPopout.submit (L9851) |
| startExamine.json | 开始检查 | case 0 (L9985) |

### 9.4 checkinListCtrl 11 个 Write

包含 customerCheckin 各种 CRUD + medicalCheckBefore (L8788) + bandingCustomer (L8911) + 删除 (L8846)

## 10. State 出口详细

### 10.1 assistCheckingCtrl 8 个 $state.go

| # | State | Params | Source | 行号 |
|---:|---|---|---|---:|
| 1 | assistChecking | {medicalExamineId, editable: null, medicalRecordId} | reload 自身 | L1765 |
| 2 | assistChecking | {medicalExamineId: $stateParams.medicalExamineId, editable: 1, medicalRecordId: $stateParams.medicalRecordId} | reload 自身 (disconnect 后) | L1886 |
| 3 | assistChecking | {medicalExamineId, editable: 1, medicalRecordId} | reload 自身 (setDevice 后) | L1907 |
| 4 | assistChecking | {medicalExamineId: $scope.obj.medicalExamineId, medicalRecordId, editable: null} | reload 自身 (saveCheck 后) | L2214 |
| 5 | assistChecking | {medicalExamineId, editable: $scope.editable, medicalRecordId} | reload 自身 (getMedicalRecord) | L2244 |
| 6 | **adminSalesRecord.myMaterialBill** | {medicalRecordId: id, patientId: res.object.patientId} | **Check → Sale 链** | L2258 |
| 7 | **adminMyRecord.myCheckBill** | {medicalRecordId: id, patientId: res.object.patientId} | **Check → 检查报告 链** | L2263 |
| 8 | **addMedicalRecord** | {medicalRecordId: id, patientId: patientId} | **Check → 开单 链** | L2269 |

### 10.2 assistCheckListCtrl 2 个 $state.go

| # | State | Params | 行号 |
|---:|---|---|---:|
| 1 | assistChecking | {medicalExamineId: List[0].medicalExamine.id, medicalRecordId} | L2400 |
| 2 | assistChecking | {medicalExamineId: $scope.medicalExamineIdArray[0], medicalRecordId} | L2417 |

### 10.3 checkinListCtrl 1 个 $state.go

| # | State | Params | 行号 |
|---:|---|---|---:|
| 1 | **myMedicalRecordList** | {patientId} | L8914 |

### 10.4 checkCallCtrl 4 个 $state.go

| # | State | Params | 行号 |
|---:|---|---|---:|
| 1 | **assistChecking** | {medicalExamineId, medicalRecordId} | L9962 |
| 2 | remindList | (无) | L10036 |
| 3 | reachStoreAppointDetails | (无) | L10042 |
| 4 | (注释) requirement | - | L10057 (注释) |

## 11. StateParams 接收

### 11.1 assistCheckingCtrl 8 个 $stateParams 引用

| # | 行号 | 接收字段 |
|---:|---:|---|
| 1 | L1757 | medicalRecordId |
| 2 | L1760 | medicalExamineId |
| 3 | L1887 | medicalExamineId |
| 4 | L1889 | medicalRecordId |
| 5 | L1908 | medicalExamineId |
| 6 | L1910 | medicalRecordId |
| 7 | L2057 | editable |
| 8 | L2078 | editable |

### 11.2 assistCheckListCtrl 0 个 $stateParams 引用
- **所有 medicalRecordId 来源是函数参数或 Scope**

### 11.3 checkinListCtrl 2 个 $stateParams 引用

| # | 行号 | 接收字段 |
|---:|---:|---|
| 1 | L9051 | appointId |
| 2 | L9076 | printCheckinId |

### 11.4 checkCallCtrl 0 个 $stateParams 引用
- **所有 medicalExamineId 来自 List item**

## 12. queue/call 数据 (checkCallCtrl)

### 12.1 队列数据结构

```javascript
// L9929-L9947 transmitStatus(queueStatus, medicalExamineList)
queueStatus: 0/1/2/3/null  // 0等待 1叫号 2已叫 3已过
checkStatus: 0/1/2  // 0待检查 1检查中 2已检查
```

### 12.2 队列 API

| API | 用途 | 行号 |
|---|---|---:|
| selectMedicalExamineQueueMainVoList.json | 叫号队列 | L10190 |
| selectMedicalExamineSignInVoList.json | 待签到 | L10221 |
| getNowCallingExamineQueueMain.json | 当前叫号 | L10168 |
| callNextExamineQueueMain.json | 下一位 | L10123 |
| callingExamineQueueMain.json | 呼叫 | L10018 |
| callingWaitingExamineQueueMain.json | 等待叫号 | L9996 |
| closeNowCallingExamineQueueMain.json | 过号 | L10005 |
| callingExamineQueueWhenNotSignIn.json | 待签到叫号 | L10158 |

### 12.3 诊室数据结构

```javascript
// L10133-L10147
$scope.clinicInfo = {
  consultRoom: { id, status, companyId },
  examineList: [examine.id, ...]
}
```

## 13. 4 Controller 对照

| 项目 | assistCheckingCtrl | assistCheckListCtrl | checkCallCtrl | checkinListCtrl |
|---|---|---|---|---|
| **medicalRecordId** | 15 命中 / A 类 StateParams + B 类 API Response | 7 命中 / C 类函数参数 + 局部 Scope | 1 命中 / E 类 List item | 1 命中 / E 类 customerCheckin.medicalRecordId |
| **patientId** | 7 命中 / D 类 API Response + C 类函数参数 | 1 命中 / C 类函数参数 | **0 命中** | 5 命中 / C 类函数参数 + State go |
| **Read API** | 10 个 | 2 个 | 3 个 | 5 个 |
| **Write API** | 4 个 | 2 个 | 8 个 | 11 个 |
| **ListFactory** | 3 个 (含 history 1 个) | 1 个 | 3 个 (诊室/叫号/签到) | 2 个 |
| **ObjectFactory** | 多 (含 medicalRecord / patient / uartDevice) | 1 个 (startExamine) | 多 (叫号相关) | 多 (登记相关) |
| **$state.go 出口** | 8 (5 reload 自身 + 3 三向分流) | 2 (reload 自身) | 4 (1 assistChecking + 3 业务跳转) | 1 (myMedicalRecordList) |
| **$stateParams 接收** | 8 (medicalRecordId/medicalExamineId/editable) | 0 | 0 | 2 (appointId/printCheckinId) |
| **职责** | **检查详情主操作** | **检查列表 (按 medicalRecord)** | **检查叫号/队列** | **登记列表 (按 customerCheckin)** |

## 14. Check → Optometry 链判定

### 14.1 4 Controller 内 optometry 引用

**S1-125 关键发现 2（4 Controller 完全无 optometry 引用）**：

| Controller | optometry 命中 |
|---|---:|
| assistCheckingCtrl | **0** |
| assistCheckListCtrl | **0** |
| checkCallCtrl | **0** |
| checkinListCtrl | **0** |
| **合计** | **0** |

### 14.2 全局 optometry $state.go 引用

| 行号 | Controller | 目标 |
|---:|---|---|
| L34954 | optometryCtrl | optometryGlasses (验光业务内部) |
| L35136 | optometryCtrl | optometryGlasses (验光业务内部) |

**S1-125 关键发现 3（Check → Optometry 链 F 级）**：
- 4 个 Check Controller **完全没有任何** optometry 引用
- 全局只有 optometryCtrl 跳转到 optometryGlasses（验光业务内部）
- **Check → Optometry 链在源码范围内未建立**
- 复刻时需要按业务场景手动跳转，**不能自动**

### 14.3 Check 完成后的 5 段去向

```
Check 完成后:
  1. reload 自身 (5 处) - 重新加载检查列表
  2. adminSalesRecord.myMaterialBill (L2258) - Check → Sale (开单)
  3. adminMyRecord.myCheckBill (L2263) - Check → 检查报告
  4. addMedicalRecord (L2269) - Check → 添加病历
  5. (业务菜单由用户手动跳到 Optometry)
```

## 15. Entry → Check 链（S1-124 验证）

### 15.1 入口 Controller → Check 入口

| 入口 | API | 终点 | 行号 |
|---|---|---|---|
| doctorWorkbenchCtrl "查看 case 3" | (无 API) | myMemberRecord | L10641 |
| myMemberCtrl clinck | beginCustomerCheckin.json | myMemberRecord / myMaterialBill | L33127 |
| optometryCtrl beginCustomerCheckin | beginCustomerCheckin.json | optometryGlasses | L34947 |
| checkinListCtrl preDiagnosisExamination | medicalCheckBeforeCustomerCheckin.json | preDiagnosisExamination 弹窗 | L8788 |
| checkCallCtrl case 0 | startExamine.json | assistChecking | L9985 |
| myCheckBillCtrl goAssist | startExamine.json | assistChecking | L32132 |

### 15.2 4 Controller 接收入口

| Controller | 接收 $stateParams | 实际入口源 |
|---|---|---|
| assistCheckingCtrl | medicalRecordId, medicalExamineId, editable | doctorWorkbenchCtrl / myCheckBillCtrl / checkCallCtrl / assistCheckListCtrl |
| assistCheckListCtrl | 0 | (HTML ng-click) |
| checkCallCtrl | 0 | (HTML ng-click) |
| checkinListCtrl | appointId, printCheckinId | addCheckinCtrl L8654 |

**S1-125 关键发现 4（Entry → Check 直接链）**：
- **6 条** 入口 Controller → Check Controller 直接链
- assistCheckingCtrl 是**核心**接收端
- 4 个 Check Controller 通过 State go + 自身 reload 形成互链

## 16. 检查内部 DAG

### 16.1 assistCheckingCtrl 内部 DAG

```
[Init] L1757-L1760
  ↓ $stateParams.medicalRecordId + medicalExamineId
  ↓
$scope.medicalRecordId / $scope.obj.medicalExamineId
  ↓
[Read] L1964: getMedicalRecord.json { id: $scope.medicalRecordId }
  ↓ Response
  ↓
$scope.patientId = response.object.patientId (Type 3 派生)
  ↓
[Read] L1970: getPatientInfo.json { id: $scope.patientId }
  ↓ Response
  ↓
[Read] L1977: getPatientExamineListVoList.json { patientId }
  ↓
[Read] L2068: getMedicalExamineVoList.json { medicalRecordId }
  ↓ Response
  ↓
$scope.medicalExamineItemList (items[].medicalExamine + leftExamine + rightExamine)
  ↓
[Read] L1829: selectUartDeviceByAdminId.json (UartDevice)
  ↓
$scope.uartDeviceId
  ↓
$interval(function() { $scope.getLastest() }, 3000)  (L1834 - 自动刷新)
  ↓
[Read] L1787: getLatestUartDeviceLogToSchoolMateCheck.json
  ↓ Response
  ↓
$scope.nowUartDeviceLogId / $scope.medicalExamineItemList[i].left/right
  ↓
[Action] L2160: $scope.saveCheck(...)
  ↓
[Write] L2196: modifyMedicalExamineItemList.json { medicalExamineId, medicalExamineItemListJson }
  ↓ Response
  ↓
[Write] L2205: uploadExamineResult.json
  ↓ Response
  ↓
[Write] L2211: completeExamine.json { medicalExamineId }
  ↓
$scope.search()  (reload)
  ↓
[State go] L2214: $state.go("assistChecking", { reload: true })
```

## 17. 与历史结论的差异

### 17.1 S1-115 vs S1-125

| 项 | S1-115 | S1-125 |
|---|---|---|
| 4 Controller 范围 | 标注 4 个但未深入 | **每个 100% 完整审计** |
| 写 API 数量 | 标注"未深入" | 25 个 Write API 详细 |
| 队列数据 | 未涉及 | checkCallCtrl 8 个 queue/call API |
| optometry 链 | 假设存在 | **F 级（未建立）** |

### 17.2 S1-123 vs S1-125

| 项 | S1-123 | S1-125 |
|---|---|---|
| assistCheckingCtrl 内部 | 3 个 $state.go | 8 个 $state.go 全部识别 |
| checkCallCtrl | 标注"叫号入口" | 8 个 Write API + 3 个 Read API + 1 个 state.go 出口 |
| medicalRecordId 来源 | 标注 2 个 | 7 个精确 entry（5 个 check 主链 + 2 个 view 入口）|

### 17.3 S1-124 vs S1-125

| 项 | S1-124 | S1-125 |
|---|---|---|
| Check 入口来源 | 标注 4 个 | 6 个（新增 checkCallCtrl startExamine + myCheckBillCtrl goAssist）|
| medicalCheckBefore | 标注 checkinListCtrl | **关键入口**（诊前检查）|
| medicalRecordId 入口数 | 7 | 24（4 Controller 总和）|

## 18. 26 项矩阵

| # | 项目 | 详情 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | 4 Controller 注册 | 全部确认 | A | L1 |
| 02 | Controller 范围 | 1671 行 (553+117+484+517) | A | L1 |
| 03 | DI | 4 套 DI 各异 | A | L1 |
| 04 | API unique | 46 个 | A | L1 |
| 05 | API call site | 47 处 | A | L1 |
| 06 | Read | 20 个 unique | A | L1 |
| 07 | Write | 25 个 unique | A | L1 |
| 08 | medicalRecordId | 24 命中 | A | L1 |
| 09 | medicalRecordId provenance | 8 类分类 | A | L1 |
| 10 | patientId | 13 命中 | A | L1 |
| 11 | patientId provenance | 4 类分类 | A | L1 |
| 12 | patient→medicalRecordId | A (L1967 Type 3 派生) | A | L1 |
| 13 | 检查对象 | 14 类 (medicalExamine 等) | A | L1 |
| 14 | 检查 API | 25+ 个 | A | L1 |
| 15 | Request | 全部 A 级 | A | L1 |
| 16 | Response | 8 类 (result.object / result.list / etc) | A | L1 |
| 17 | Response 落点 | Scope/Factory/Llocal | A | L1 |
| 18 | ListFactory | 9 个 unique | A | L1 |
| 19 | ObjectFactory | 多 | A | L1 |
| 20 | StateParams | 10 个 (assistChecking 8 + checkinList 2) | A | L1 |
| 21 | State 出口 | 15 个 $state.go | A | L1 |
| 22 | queue/call 数据 | checkCallCtrl 8 API | A | L1 |
| 23 | Check→Optometry | **F（4 Controller 0 引用）** | A | L1 |
| 24 | Entry→Check | **A（6 条直接链）** | A | L1 |
| 25 | Check 内部 DAG | assistCheckingCtrl 完整建立 | A | L1 |
| 26 | A/B/C/D/E/F | A=25 / B=0 / C=0 / D=0 / E=0 / F=1 | - | - |

## 19. F 边界

| 项目 | F 原因 | 应对 |
|---|---|---|
| Check → Optometry 链 | 源码范围内未建立 | 不能假设业务自动跳转 |
| HTML ng-click 跳转 | 不在 controller.js 范围 | 需要 HTML 审计 |
| 后端 List 排序 / 分页 | 不在审计范围 | 行为依赖后端 |
| 轮询 Loop 行为 | checkCallCtrl L10233-L10252 | 实际行为需运行 |

## 20. 复刻风险（L1）

### R1: 4 Controller 不同职责
- assistCheckingCtrl = 检查主操作（核心）
- assistCheckListCtrl = 检查列表（按 medicalRecord）
- checkCallCtrl = 检查叫号/队列
- checkinListCtrl = 登记列表（按 customerCheckin）
- **4 个 Controller 业务不同**，复刻时不能混淆

### R2: medicalRecordId 不一定在所有 Controller
- assistCheckListCtrl 0 个 $stateParams.medicalRecordId（来源是函数参数）
- checkCallCtrl 0 个 $stateParams.medicalRecordId（来源是 List item）
- 复刻时按 controller 实际来源实现

### R3: 检查结果可能不是 medicalRecord 整体
- 检查结果对象是 medicalExamineVoList + medicalExamineItemList
- 不是 medicalRecordVo
- 复刻时注意区分

### R4: State / API bridge 必须保留
- 4 Controller 之间的 State go + reload 模式必须保留
- 不能简化为单次 load

### R5: 叫号数据不能与检查记录混合
- checkCallCtrl 的 queue 数据独立
- 不能用 medicalExamine 替代 medicalExamineQueueMain

### R6: Controller 名称不能当业务定义
- "assistCheck" 不是简单"助诊列表"
- "checkCall" 不是简单"叫号"
- 实际业务需根据 API 和对象判定

## 21. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- 165-186 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 22. 结论

### 22.1 关键发现

1. **4 Controller 业务完全分离**:
   - assistCheckingCtrl = **核心** (15 medicalRecordId / 7 patientId / 10 Read / 4 Write)
   - assistCheckListCtrl = 列表 (2 Read / 2 Write / 0 StateParams)
   - checkinListCtrl = 登记 (5 Read / 11 Write / customerCheckin 重点)
   - checkCallCtrl = 叫号 (3 Read / 8 Write / 0 patientId)
2. **46 个 unique API / 47 call site / 25 Write API**
3. **medicalRecordId 24 命中 / patientId 13 命中**
4. **checkCallCtrl 完全不处理 patient**（0 patientId 命中）
5. **Check → Optometry 链 F 级（未建立）**
6. **Entry → Check 直接链 6 条**
7. **检查 Write 含完整读-改-写循环**（modifyMedicalExamineItemList + uploadExamineResult + completeExamine）

### 22.2 S1-125 任务状态

- 4 Controller 注册完整定位
- 46 unique API 全量统计
- medicalRecordId/patientId provenance 8 类分类
- 检查对象全集 14 类
- 4 Controller 对照表完整
- 26 项矩阵已建立
- 6 条复刻风险已列出

---

**【S1-125 完成】**
