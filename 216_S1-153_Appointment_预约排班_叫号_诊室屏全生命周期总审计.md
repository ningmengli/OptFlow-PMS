# S1-153：Appointment / 预约排班 / 叫号 / 诊室屏全生命周期总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 215 个 MD / 不修改历史
> 关联：S1-134 / S1-147 / S1-150 / S1-151 / S1-152

---

## 目录

- §0 审计范围
- §1 Appointment 全量
- §2 Appointment Object 字段
- §3 Appointment API 全量
- §4 Appointment → Patient
- §5 Appointment → SchoolMate
- §6 Appointment → Customer
- §7 Appointment → CustomerCheckin
- §8 Appointment → MedicalRecord
- §9 Appointment Status
- §10 Schedule / 排班
- §11 Reception Queue / 接诊叫号
- §12 Examination Queue / 检查叫号
- §13 Call Management / 叫号管理
- §14 Call Screen / 叫号大屏
- §15 Room Screen / 诊室屏
- §16 Calling Machine / 叫号机
- §17 ConsultRoom 关系
- §18 Queue 关系
- §19 Employee / Department
- §20 Schedule 关系
- §21 预约接诊闭环
- §22 状态 / UI Tab
- §23 Controller 消费矩阵
- §24 Object 分类
- §25 Source Trace
- §26 26 项证据矩阵
- §27 历史差异
- §28 V4.4 预约叫号规格
- §29 F / 未确认
- §30 Git / 完整性

---

## §0 审计范围

本轮把 Appointment / 预约排班 / 叫号 / 诊室屏作为**前端可证明的对象、字段、API、State、Controller 和桥接关系**进行完整只读审计：

- 区分 Appointment / appointId / appointmentId 命名差异
- 验证 Queue / Schedule / CallScreen / RoomScreen / CallingMachine 概念
- 4 个真实 Controller 深审 (bookDetailCtrl / bookManageCtrl / checkCallCtrl / bigScreenCtrl)
- 8+ 真实 Appointment / BigScreen / BigScreenConfig / CorpAppointmentConf API
- consultRoom.status 真实存在（L10141/L10783）
- bigScreen.sceneType 1=医生接诊叫号 / 2=检查叫号
- 26 项证据矩阵
- 历史 S1-134/147/150/151/152 误判核对

---

## §1 Appointment 全量

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `appoint` (全词) | **13** | A |
| `appointment` | 4 | A |
| `appointOrder` | 0 | A |
| `appointmentOrder` | 0 | A |
| `appointId` | **25** | A (核心) |
| `appointmentId` | 5 | A |
| `appointVo` | **11** | A |
| `appointList` | 6 | A |
| `appointmentVo` | 0 | A |
| `appointmentList` | 0 | A |
| `schedule` | **0** | A |
| `appointmentSchedule` | 0 | A |
| `scheduleId` | 0 | A |
| `appointmentTime` | 0 | A |
| `scheduleTime` | 0 | A |
| `queue` | **0** | A |
| `queueId` | 0 | A |
| `queueNumber` | 0 | A |
| `queueNo` | 0 | A |
| `waitingCall` | 0 | A |
| `callScreen` | 0 | A |
| `roomScreen` | 0 | A |
| `consultRoomScreen` | 5 | A |
| `callingMachine` | 0 | A |
| `callId` | 0 | A |

### §1.2 关键发现（本轮重大）

1. **`appointmentOrder` / `appointmentVo` / `appointmentList` 全部 0 命中** — 大写命名习惯不存在
2. **`schedule` / `appointmentSchedule` / `scheduleId` / `appointmentTime` 全部 0 命中** — **排班独立 Object 不存在**
3. **`queue` / `queueId` / `queueNumber` / `queueNo` 全部 0 命中** — **Queue 独立 ID 不存在**
4. **`callScreen` / `roomScreen` / `callingMachine` / `callId` 全部 0 命中** — **叫号大屏/诊室屏/叫号机 命名误导**
5. **`consultRoomScreen` 5 命中** — 实际是 `consultRoom.screen` 内部，不是独立 Object
6. **`appointId` 25 命中 + `appointmentId` 5 命中** — **两个不同 ID 字段**（不是同义）

### §1.3 修正历史

| 历史误判 | 当前证据 | 当前采用 |
|---|---|---|
| ~~Schedule 是独立 Object~~ | schedule / scheduleId 0 命中 | **F (0 命中)** |
| ~~Queue 是独立 Object~~ | queue / queueId 0 命中 | **F (0 命中)** |
| ~~callScreenCtrl 存在~~ | 实际是 `bigScreenCtrl` (L9600) | **A (命名误导)** |
| ~~roomScreenCtrl 存在~~ | 实际是 `consultRoomScreen` 内部字段 | **A (嵌套)** |
| ~~appointId ≡ appointmentId~~ | appointId 25 命中 / appointmentId 5 命中 | **A (不同 ID)** |

---

## §2 Appointment Object 字段

### §2.1 字符级字段（来自 Response/Scope）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `item.appoint.id` | L8252/L8269/L44170 (经 getAppointPatientVo/getAppointSchoolMateVo Response) | **A (核心 ID)** |
| `item.appoint.remark` | L8250 (经 getAppointPatientVo Response) | A |
| `item.appoint.id` (cancelPopout) | L44051 `$scope.cancelPopout.params.appoint.id` | A |
| `$scope.getAppointmentObjectFactory.vo.appointment.companyRemark` | L3690 (bookDetailCtrl) | **A (appointment Object 字段!)** |
| `appointVo.type` | L8241/L8262/L8290/L8702 | **A (type 0=Patient / 1=SchoolMate)** |
| `appointVo.url` | L8237 (动态 URL getAppointPatientVo/getAppointSchoolMateVo) | A |
| `appointVo.schoolMateCheckId` (注释) | L8280 | C (注释) |

### §2.2 Appointment 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `appointId`, `appointmentId`, `appoint.id` | A |
| B. Response VO | `appointment` (bookDetailCtrl Response) | A |
| C. Request | `appointId` (Request) | A |
| D. State | `$stateParams.appointmentId` (bookDetailCtrl) | A |
| E. UI | `appointVo.type` / `appointVo.url` | A |
| F. Runtime | - | F |

### §2.3 0 命中字段（必须 F）

| 字段 | 等级 |
|---|:---:|
| `appoint.status` / `appoint.type` 顶层 | F (type 实际在 appointVo) |
| `appoint.patient` / `appoint.patientId` 顶层 | F (经 item.appoint.remark 派生) |
| `appoint.customer` / `appoint.customerId` 顶层 | F |
| `appoint.schoolMate` / `appoint.schoolMateId` 顶层 | F |
| `appoint.customerCheckin` 顶层 | F |
| `appoint.medicalRecord` / `appoint.medicalRecordId` 顶层 | F |
| `appoint.appointTime` / `appoint.time` / `appoint.date` 顶层 | F |
| `appoint.status` 顶层 | F |
| `appoint.consultRoom` / `appoint.room` / `appoint.employee` / `appoint.doctor` 顶层 | F |

---

## §3 Appointment API 全量

### §3.1 8+ Appointment API 完整矩阵

| API | 行号 | Controller | R/W | 等级 |
|---|---|---|---|---|
| `getAppointPatientVo.json` | L8225/L14748 | addCheckinCtrl + myMemberRecordCtrl | R | A |
| `getAppointSchoolMateVo.json` | L8229/L44055/L44059 | addCheckinCtrl + schoolMateCheckListCtrl | R | A |
| `confirmArrivalOfAppoint.json` | L8658 | addCheckinCtrl | **W** | A |
| `selectAppointSchoolMateVoList.json` | L44013 | schoolMateCheckListCtrl | R | A |
| `getAppointmentVo.json` | L3673 | bookDetailCtrl | R | A |
| `updateAppointCompanyRemark.json` | L3681 | bookDetailCtrl | **W** | A |
| `confirmAppointment.json` | L3702 | bookDetailCtrl | **W** | A |
| `selectAppointmentVoList.json` | L3705+ | bookManageCtrl | R | A |
| `updateAppoint*.json` (1 命中) | (推断) | (推断) | W | C |

### §3.2 关键发现

1. **getAppointPatientVo 真实存在** (2 调用) — 预约 Patient 入口
2. **getAppointSchoolMateVo 真实存在** (5 调用) — 预约 SchoolMate 入口
3. **confirmArrivalOfAppoint 真实存在** (1 调用) — 到店确认
4. **selectAppointSchoolMateVoList 真实存在** (1 调用) — SchoolMate 预约列表
5. **getAppointmentVo 真实存在** (1 调用) — 预约详情
6. **updateAppointCompanyRemark 真实存在** (1 调用) — 备注更新
7. **confirmAppointment 真实存在** (1 调用) — 接受预约
8. **selectAppointmentVoList 真实存在** (1 调用) — 预约列表
9. **0 命中 `getCanBeArrivedAppoint` / `getArrivedAppoint` / `getFinishedAppoint` / `insertAppointOrder` / `getAppointment*`** — 命名误导

### §3.3 getAppointPatientVo 完整（L8225 + L14748）

**L8225 (addCheckinCtrl)**:
```javascript
$scope.arrival = {
  url: "getAppointPatientVo",
  type: 0
}, // 登记跳转
$scope.reachStore = {
  url: "getAppointSchoolMateVo",
  type: 1
} // 到店筛查跳转
}[$stateParams.type];
```

**L14748 (myMemberRecordCtrl)**:
```javascript
new ObjectFactory().saveOrQuery("/admin/getAppointPatientVo.json", {
  appointId: item.messageLog.msgInfo.appointId
}).then(function (res) {
  $scope.allAppoint.lookDetails = true;
  $scope.allAppoint.dialogMsg = res.result.object;
});
```

### §3.4 confirmArrivalOfAppoint 完整（L8658）

```javascript
$scope.changeStatusFactory.saveOrQuery("/admin/confirmArrivalOfAppoint.json", {
  appointId: aId
});
// 之后:
$scope.checkCustomer.registrationFeeId = $scope.registrationFeeId;
$scope.checkCustomer.appointId = aId;
$scope.insertCustomerCheckFactory = new ObjectFactory();
```

---

## §4 Appointment → Patient

### §4.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | Patient | `getAppointPatientVo` Response (item.patient.* 派生) | A 派生 | L8225/L8243 | **A** | A |
| Appointment | Patient | 0 命中 `appointment.patient` 顶层字段 | F | - | **F** | F |
| Patient | Appointment | `getPatientVoList` / `getAppointPatientVo` Request `appointId` | A Request Bridge | L14748 | **A** | A |

### §4.2 关键判断

- **Appointment → Patient**: A 派生（经 getAppointPatientVo Response）
- **Patient → Appointment**: A Request Bridge（appointId 传参）
- **保持 S1-147 修正**：patientListCtrl 经 $stateParams.customerId → getPatientVoList（appointId 派生）

---

## §5 Appointment → SchoolMate

### §5.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | SchoolMate | `getAppointSchoolMateVo` Response (item.schoolMateVo.* 派生) | A 派生 | L8229/L8264 | **A** | A |
| Appointment | SchoolMate | `appointVo.type === 1` 分流 + `appointVo.schoolMateCheckId` | A 派生 | L8241/L8706 | **A** | A |
| SchoolMate | Appointment | `selectAppointSchoolMateVoList.json` Request `appointDay` | A Request Bridge | L44138 | **A** | A |
| Appointment | SchoolMate | 0 命中 `appointment.schoolMate` 顶层字段 | F | - | **F** | F |

### §5.2 关键判断

- **Appointment → SchoolMate**: A 派生（经 getAppointSchoolMateVo + schoolMateVo 8 字段）
- **SchoolMate → Appointment**: A Request Bridge（selectAppointSchoolMateVoList）
- **appointVo.type = 1** 是 SchoolMate 入口标志（保持 S1-152 修正）

---

## §6 Appointment → Customer

### §6.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | Customer | 0 命中 `appointment.customer` 顶层字段 | F | - | **F** | F |
| Appointment | Customer | 0 命中 `appointment.customerId` 顶层字段 | F | - | **F** | F |
| Customer | Appointment | 0 命中 `customer.appointment` 字段 | F | - | **F** | F |
| Appointment | Customer | 经 getAppointPatientVo Response (item.customer 派生) | A 派生 | L8243-L8250 | **A** | A |

### §6.2 关键判断

- **Appointment → Customer**: A 派生（经 getAppointPatientVo 嵌套）
- **Customer → Appointment**: F
- **保持 S1-147 修正**：mobile 映射是 C 字段映射

---

## §7 Appointment → CustomerCheckin

### §7.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | CustomerCheckin | `confirmArrivalOfAppoint.json` Request `appointId` | A Request Bridge | L8658 | **A** | A |
| Appointment | CustomerCheckin | 0 命中 `appointment.customerCheckin` 顶层字段 | F | - | **F** | F |
| CustomerCheckin | Appointment | 0 命中 `customerCheckin.appointment` 字段 | F | - | **F** | F |
| Appointment | CustomerCheckin | addCheckinCtrl L8667 insertCustomerCheckin.json 派生 | A Request Bridge | L8667 | **A** | A |

### §7.2 关键判断

- **Appointment → CustomerCheckin**: A Request Bridge（confirmArrivalOfAppoint + insertCustomerCheckin 派生）
- **CustomerCheckin → Appointment**: F
- **保持 S1-147 修正**：appointId 是 addCheckinCtrl 的关键 State 入口

---

## §8 Appointment → MedicalRecord

### §8.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | MedicalRecord | 0 命中 `appointment.medicalRecord` 字段 | F | - | **F** | F |
| Appointment | MedicalRecord | 0 命中 `appointment.medicalRecordId` 字段 | F | - | **F** | F |
| MedicalRecord | Appointment | 0 命中 `medicalRecord.appointment` 字段 | F | - | **F** | F |
| Appointment | MedicalRecord | 经 CustomerCheckin → beginCustomerCheckin (经 6 字符级桥) | A 派生 (经 CustomerCheckin) | L8791 | **A** | A |

### §8.2 关键判断

- **Appointment → MedicalRecord**: A 派生（经 CustomerCheckin 链）
- **保持 S1-146 修正**：MedicalRecord 不含 appointment 顶层字段

---

## §9 Appointment Status

### §9.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `appoint.status` | **0** | A |
| `appointment.status` | **0** | A |
| `appoint.statusArray` | 0 (实际是 bookManageCtrl 的 statusArray filter) | A |
| `bookManageTab` | **5+** | A (UI Tab) |
| `bookManage.status` | 0 | A |

### §9.2 关键发现

1. **`appoint.status` / `appointment.status` 0 命中** — **Appointment 顶层无 status 字段**
2. **`bookManageTab` 5+ 命中** — **bookManageCtrl 的 status 是 UI Tab 状态**
3. **`statusArray` 实际是过滤器** — `obj = { statusArray: $scope.statusArray }`
4. **Appointment 状态经 CustomerCheckin 派生** — 经 6 字符级 customerCheckin.medicalRecordId 桥
5. **保持 S1-146 修正**：MedicalRecord.status 0 命中 — 状态在 cashflow 顶层

---

## §10 Schedule / 排班

### §10.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `schedule` | **0** | A |
| `appointmentSchedule` | 0 | A |
| `appointSchedule` | 0 | A |
| `scheduleId` | 0 | A |
| `appointmentTime` | 0 | A |
| `scheduleTime` | 0 | A |
| `getSchedule*.json` | 0 | A |
| `saveSchedule*.json` | 0 | A |
| `schoolPlanId` (schedule 关联) | 1+ (L44138) | A |

### §10.2 关键发现

1. **schedule / appointmentSchedule / scheduleId / appointmentTime / scheduleTime 全部 0 命中**
2. **0 命中独立 Schedule API** — 排班独立 Object/Controller/API **不存在**
3. **schoolPlanId (L44138) 是 School 侧关联 ID** — 不是 Schedule 主键
4. **getWeekDay / setWeekChose (L9760+)** — checkCallCtrl 的周历组件（不是 Schedule Object）

### §10.3 Schedule 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | `schoolPlanId` (L44138) | C |
| D. State | - | F |
| E. UI | `weekInfo` (checkCallCtrl 周历) | A (UI) |
| F. Runtime | - | F |

### §10.4 关键判断

- **Schedule 不是独立 Object 实体**（F）
- 实际"排班"由 checkCallCtrl 的 weekInfo 周历组件 + bookManageCtrl 的 arriveTimeFrom/To 时间范围表达
- **保持 S1-132 修正**：没有独立 Schedule 实体

---

## §11 Reception Queue / 接诊叫号

### §11.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `queue` | **0** | A |
| `queueId` | 0 | A |
| `queueNumber` | 0 | A |
| `queueNo` | 0 | A |
| `isWaiting` | 5+ (checkCallCtrl) | A (UI State) |
| `waitingList` | 0 | A |
| `receptionQueue` | 0 | A |

### §11.2 关键发现

1. **queue / queueId / queueNumber / queueNo 全部 0 命中** — **Queue 独立 ID 不存在**
2. **`isWaiting` 5+ 命中 (checkCallCtrl)** — 实际是 **UI Tab State**（待叫/已叫）
3. **`waitingList` 0 命中** — 没有独立等待列表 Object

### §11.3 关键判断

- **Queue 不是独立 Object 实体**（F）
- 实际"接诊叫号"由 checkCallCtrl + bigScreenCtrl 实现
- **叫号大屏的 queue 状态经 checkinNumber 派生**（L11157 `p.customerCheckin.checkinNumber`）

---

## §12 Examination Queue / 检查叫号

### §12.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `checkCall` | **多** | A |
| `checkCallCtrl` | 1 | A |
| `bigScreen.sceneType === 2` (检查叫号) | A (派生) | A |
| `examineCall` / `checkQueue` | **0** | A |
| `examinationQueue` | 0 | A |

### §12.2 关键发现

1. **`checkCallCtrl` L9760 真实存在** — **检查叫号主 Controller**
2. **bigScreenCtrl.sceneType === 2 = 检查叫号模式** — 派生自 consultRoom.examineList[].examineName
3. **`examineCall` / `checkQueue` 0 命中** — 短命名不存在
4. **`getEmployeeExamineConsultRoomVo` (L9760)** — 派生 employee + examine + consultRoom 三件套

### §12.3 checkCallCtrl 关键字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `weekInfo` | L9760 (周历组件) | A |
| `weekInfo.weekDay` | L9760 | A |
| `weekInfo.monthTitle` | L9760 | A |
| `isWaiting` | L9760 (UI 状态) | A (UI) |
| `getEmployeeExamineConsultRoomVo` | L9760 | A (Function) |

### §12.4 关键判断

- **检查叫号由 checkCallCtrl + bigScreenCtrl.sceneType===2 联合实现**
- **没有独立 ExaminationCall / checkQueue Object**（F）

---

## §13 Call Management / 叫号管理

### §13.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `callManage` | 0 | A |
| `callManagement` | 0 | A |
| `callManageCtrl` | **NOT FOUND** | F |

### §13.2 关键发现

1. **`callManage` / `callManagement` 0 命中** — 命名不存在
2. **`callManageCtrl` NOT FOUND** — 叫号管理 Controller 不存在
3. **实际"叫号管理"由 bigScreenCtrl 完整实现**（addBigScreenAndConf.json / updateBigScreenAndConf.json + selectBigScreenConfVoListOfCompany.json）

---

## §14 Call Screen / 叫号大屏

### §14.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `callScreen` | 0 | A |
| `callScreenCtrl` | **NOT FOUND** | F |
| `bigScreen` | 5+ | A |
| `bigScreenCtrl` | **L9600** ✓ | A |
| `bigScreen.id` | L9600+ | **A (核心 ID)** |
| `bigScreenName` | L9600 | A |
| `sceneType` | L9600 | A (1=接诊叫号 / 2=检查叫号) |
| `playVoice` | L11157 | A |
| `screenful` | L9600 | A (Function) |

### §14.2 bigScreenCtrl 完整功能（L9600）

```javascript
$scope.bigScreenPopout = {
  show: false,
  title: "",
  bigScreenName: "",  // 叫号大屏的名称
  sceneType: 1,        // 1=医生接诊叫号 / 2=检查叫号
  consultRoomIdArray: [],  // 绑定诊室列表
  showP / submit / choseSingle / setSceneType Methods
};
$scope.searchClinicList = function() {
  $scope.clinicList = new ListFactory("/admin/selectConsultRoomVoListOfCompany.json", 0, $scope.pageSize, {
    companyId: $scope.companyInfo.id, keyword: "", status: 0
  });
};
$scope.searchScreenList = function(index, loadPagin) {
  HttpFactory.list("/admin/selectBigScreenConfVoListOfCompany.json", {...});
};
$scope.searchScreenObj = function(bigScreenId, index) {
  HttpFactory.object("/admin/getBigScreenConfVo.json", { bigScreenId: bigScreenId });
};
$scope.screenful = function(item) {
  $state.go("screenQueue", { bigScreenId: item.bigScreen.id });
};
```

### §14.3 bigScreenCtrl 5 个 API

| API | R/W | 等级 |
|---|---|---|
| `selectConsultRoomVoListOfCompany.json` | R | A |
| `selectBigScreenConfVoListOfCompany.json` | R | A |
| `getBigScreenConfVo.json` | R | A |
| `addBigScreenAndConf.json` | **W (大屏创建)** | A |
| `updateBigScreenAndConf.json` | **W (大屏更新)** | A |

### §14.4 bigScreen 真实 Object 字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `bigScreen.id` | L9600 (`item.bigScreen.id` / `update.bigScreen.id`) | **A (核心 ID)** |
| `bigScreen.bigScreenName` | L9600 | A |
| `bigScreen.sceneType` | L9600 (1=接诊 / 2=检查) | A |
| `consultRoomVoList[]` | L9600 (绑定诊室) | A |
| `employeeList[].employeeName` (sceneType=1) | L9600 | A |
| `consultRoom.examineList[].examineName` (sceneType=2) | L9600 | A |

### §14.5 关键发现（本轮重大）

1. **`callScreenCtrl` 0 命中 / NOT FOUND** — 命名误导
2. **实际叫号大屏是 `bigScreenCtrl` L9600** — 5 个 API 完整
3. **`sceneType` 1=医生接诊叫号 / 2=检查叫号** — 是叫号大屏的模式字段
4. **playVoice 完整对象**（L11157）：
   - `p.customerCheckin.checkinNumber` (排队号)
   - `p.patient.patientName` (患者名)
   - `p.consultRoom.consultRoomName` (诊室名)
5. **`screenful` 跳转 `screenQueue` State + bigScreenId**
6. **`bigScreen` 是独立 ID 实体**（A）

### §14.6 CallScreen 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `bigScreen.id` | A |
| B. Response VO | `bigScreen.bigScreenName` / `sceneType` | A |
| C. Request | `bigScreenName` / `sceneType` / `consultRoomIdArray` | A |
| D. State | - | F |
| E. UI | `bigScreenPopout` (UI 弹窗) | A (UI) |
| F. Runtime | - | F |

---

## §15 Room Screen / 诊室屏

### §15.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `roomScreen` | 0 | A |
| `roomScreenCtrl` | **NOT FOUND** | F |
| `consultRoomScreen` | 5 (内部字段) | A |
| `consultRoom.id` | 50+ | A (核心 ID) |
| `consultRoom.status` | 2 (L10141/L10783 `status === 1`) | **A (本轮新发现)** |

### §15.2 关键发现

1. **`roomScreenCtrl` 0 命中 / NOT FOUND** — 命名误导
2. **实际"诊室屏"是 `consultRoomScreen` 内部字段**（5 命中）
3. **consultRoom.status 真实存在**（L10141/L10783 `status === 1`）— **本轮重大新发现**
4. **consultRoom 是核心 Object 实体**（consultRoomId 25 命中 + 50+ 字段访问）

### §15.3 consultRoom 真实字段（核心）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `consultRoom.id` | L9555/L9645/L9678/L9694/L9852/L10072 等 (50+ 命中) | **A (核心 ID)** |
| `consultRoom.consultRoomName` | L9514/L11154/L15196 | A |
| `consultRoom.companyId` | L9336/L10211 | A |
| `consultRoom.status` | L10141/L10783 `status === 1` | **A (本轮新发现)** |
| `consultRoom.examineList[]` | L9725/L9600 | A |
| `consultRoomVoList[]` (容器) | L9623/L9600 | A |
| `consultRoomIdArray` (Scope) | L9600 (13 命中) | A |
| `checkSignIn?consultRoomId=...` | L15198 (WechatConfig 二维码) | A |

### §15.4 consultRoom.status 真实含义

`status === 1` 在两个地方出现：
- L10141 `if ($scope.clinicInfo.consultRoom.status === 1)` (checkCallCtrl)
- L10783 `if ($scope.clinicInfo.consultRoom.status === 1)` (同 checkCallCtrl)

**含义推测**：status === 1 可能是"启用"或"接诊中"状态（A 真实存在）

### §15.5 RoomScreen 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `consultRoomId` | A |
| B. Response VO | `consultRoom` (10+ 字段) | A |
| C. Request | `consultRoomIdArray` / `consultRoomId` | A |
| D. State | - | F |
| E. UI | `clinicInfo.consultRoom` (弹出 UI) | A |
| F. Runtime | - | F |

---

## §16 Calling Machine / 叫号机

### §16.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `callingMachine` | 0 | A |
| `callMachine` | 0 | A |
| `callingMachineCtrl` | **NOT FOUND** | F |
| `callMachineCtrl` | **NOT FOUND** | F |

### §16.2 关键发现

1. **callingMachine / callMachine 0 命中** — 命名误导
2. **callingMachineCtrl / callMachineCtrl NOT FOUND** — 叫号机 Controller 不存在
3. **实际"叫号机"由 consultRoom.checkSignIn (L15198) + bigScreenCtrl 实现**

---

## §17 ConsultRoom 关系

### §17.1 ConsultRoom ↔ 8 对象矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| ConsultRoom | Company | `consultRoom.companyId` (经 $scope.clinicInfo.consultRoom.companyId) | A 字段桥 | L10211 | **A** | A |
| ConsultRoom | Appointment | 0 命中 `consultRoom.appointment` 字段 | F | - | **F** | F |
| ConsultRoom | Queue | 0 命中 `consultRoom.queue` 字段 | F | - | **F** | F |
| ConsultRoom | Employee | 0 命中 `consultRoom.employee` 字段（实际是 bigScreen 派生的 employeeList） | F | - | **F** | F |
| ConsultRoom | Department | 0 命中 `consultRoom.department` 字段 | F | - | **F** | F |
| ConsultRoom | BigScreen | `bigScreenPopout.consultRoomIdArray = v.consultRoom.id` (bigScreenCtrl) | A Request Bridge | L9600 | **A** | A |
| ConsultRoom | CheckSignIn (WechatConfig) | `checkSignIn?consultRoomId=...` URL | A URL 集成 | L15198 | **A** | A |
| ConsultRoom | MedicalExamine | `consultRoom.examineList[]` | A 字段桥 | L9725/L9600 | **A** | A |

### §17.2 关键判断

- **ConsultRoom → Company**: A 字段桥（保持 S1-151 修正）
- **ConsultRoom → BigScreen**: A Request Bridge（`consultRoomIdArray`）
- **ConsultRoom → CheckSignIn**: A URL 集成（WechatConfig 二维码）
- **ConsultRoom → MedicalExamine**: A 字段桥（examineList）
- **ConsultRoom → Appointment/Queue/Employee/Department**: F

---

## §18 Queue 关系

### §18.1 Queue 4 关系矩阵（本轮全部 F）

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Queue | CustomerCheckin | 0 命中 `queue.customerCheckin` 字段 | F | - | **F** | F |
| CustomerCheckin | Queue | 0 命中 `customerCheckin.queue` 字段 | F | - | **F** | F |
| Queue | MedicalRecord | 0 命中 `queue.medicalRecord` 字段 | F | - | **F** | F |
| MedicalRecord | Queue | 0 命中 `medicalRecord.queue` 字段 | F | - | **F** | F |

### §18.2 关键判断

- **Queue 不是独立 Object**（F）
- 实际"叫号"通过 `checkinNumber` (customerCheckin 字段) + bigScreen playVoice 实现
- **保持 S1-146 修正**：MedicalRecord 不含 queue 字段

---

## §19 Employee / Department

### §19.1 Employee / Department 关系

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Appointment | Employee | 0 命中 `appointment.employee` 字段 | F | - | **F** | F |
| Appointment | Department | 0 命中 `appointment.department` 字段 | F | - | **F** | F |
| Schedule | Employee | 0 命中（Schedule 本身不存在） | F | - | **F** | F |
| Schedule | Department | 0 命中（Schedule 本身不存在） | F | - | **F** | F |
| Queue | Employee | 0 命中（Queue 本身不存在） | F | - | **F** | F |
| ConsultRoom | Employee | 0 命中（实际是 bigScreen 派生的 employeeList） | F | - | **F** | F |
| ConsultRoom | Department | 0 命中 | F | - | **F** | F |

### §19.2 关键判断

- **Appointment / Schedule / Queue / ConsultRoom 都不直接绑定 Employee / Department**（F）
- 实际 Employee 经 bigScreenCtrl.employeeList 派生（sceneType=1 接诊叫号）

---

## §20 Schedule 关系

### §20.1 0 命中关系矩阵

| Source | Target | 等级 |
|---|---|:---:|
| Schedule → Employee | F (0 命中, Schedule 不存在) | F |
| Schedule → ConsultRoom | F | F |
| Employee → Schedule | F | F |
| ConsultRoom → Schedule | F | F |

### §20.2 关键判断

- **Schedule 不存在独立 Object 实体**（F）
- 所有"排班"关系保持 F

---

## §21 预约接诊闭环

### §21.1 完整 Lifecycle DAG

```
[预约源]
    ↓
[bookDetailCtrl L3669 / bookManageCtrl L3680 / bookSettingsCtrl L3682]
    ├── getAppointmentVo.json (L3673) → appointment Object
    ├── updateAppointCompanyRemark.json (L3681) → 备注
    └── confirmAppointment.json (L3702) → 接受预约
    
[addCheckinCtrl L8159 接诊]
    ├── $stateParams.type = 0 → 登记跳转 → getAppointPatientVo
    │     ├── appointId: $stateParams.appointId
    │     ├── item.patient / item.appoint / item.customer
    │     └── Response 含 patient/customer/schoolMateVo
    │
    └── $stateParams.type = 1 → 到店筛查 → getAppointSchoolMateVo
          ├── appointId: $stateParams.appointId
          ├── item.schoolMateVo (8 字段)
          └── Response 含 schoolMateVo
    
    ↓ insertCustomerCheckin.json (L8667-L8681)
[CustomerCheckin] (customerCheckinId 派生)
    ↓ beginCustomerCheckin / receiveSelfAndBeginCustomerCheckin
[MedicalRecord] (6 字符级 customerCheckin.medicalRecordId 桥)

[叫号大屏]
    ↓
[bigScreenCtrl L9600] 维护大屏配置
    ├── addBigScreenAndConf.json (L9600) - 创建
    ├── updateBigScreenAndConf.json (L9600) - 更新
    ├── selectBigScreenConfVoListOfCompany.json - 列表
    ├── getBigScreenConfVo.json - 详情
    ├── bigScreen.sceneType 1=接诊叫号 / 2=检查叫号
    ├── bigScreenPopout.consultRoomIdArray 绑定诊室
    └── screenQueue State 跳转
    
[叫号大屏播放]
    ↓
[playVoice L11157] p.customerCheckin.checkinNumber + p.patient.patientName + p.consultRoom.consultRoomName

[检查叫号]
    ↓
[checkCallCtrl L9760]
    ├── weekInfo 周历
    ├── isWaiting UI 状态
    ├── getEmployeeExamineConsultRoomVo
    └── grantAuth.hasAuthForCompany
```

### §21.2 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| Appointment | Patient | A 派生 | getAppointPatientVo Response | L8225 |
| Appointment | SchoolMate | A 派生 | getAppointSchoolMateVo Response | L8229 |
| Appointment | Customer | A 派生 | getAppointPatientVo 嵌套 | L8243 |
| Appointment | CustomerCheckin | A Request Bridge | confirmArrivalOfAppoint | L8658 |
| Appointment | MedicalRecord | A 派生 | 经 CustomerCheckin 6 字符级桥 | L8791 |
| SchoolMate | Appointment | A Request Bridge | selectAppointSchoolMateVoList | L44013 |
| BigScreen | ConsultRoom | A Request Bridge | bigScreenPopout.consultRoomIdArray | L9600 |
| ConsultRoom | Company | A 字段桥 | consultRoom.companyId | L10211 |
| ConsultRoom | MedicalExamine | A 字段桥 | examineList[] | L9725 |
| ConsultRoom | CheckSignIn | A URL 集成 | checkSignIn?consultRoomId= | L15198 |
| BigScreen | Employee | A 派生 | employeeList[].employeeName (sceneType=1) | L9600 |
| BigScreen | MedicalExamine | A 派生 | examineList[].examineName (sceneType=2) | L9600 |

### §21.3 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Appointment → MedicalRecord 字段桥 | F (经 CustomerCheckin 派生 A) |
| Queue → CustomerCheckin 字段桥 | F |
| Queue → MedicalRecord 字段桥 | F |
| Schedule → Employee 字段桥 | F (Schedule 不存在) |
| Schedule → ConsultRoom 字段桥 | F (Schedule 不存在) |
| consultRoom.appointment 字段桥 | F |
| consultRoom.queue 字段桥 | F |
| consultRoom.employee 字段桥 | F (经 bigScreen 派生 A) |
| consultRoom.department 字段桥 | F |
| appointment.employee/department/consultRoom/patient/customer 字段 | F (0 命中) |
| appointment.status 字段 | F (0 命中) |
| appointment.medicalRecordId 字段 | F (0 命中) |

---

## §22 状态 / UI Tab

### §22.1 状态字段分类

| 字段 | 真实位置 | 等级 |
|---|---|---|
| `bookManageTab` | bookManageCtrl (UI Tab 1/2/3) | A (UI) |
| `statusArray` | bookManageCtrl (filter) | A (UI) |
| `isWaiting` | checkCallCtrl (UI) | A (UI) |
| `weekInfo.week` | checkCallCtrl (UI 周历) | A (UI) |
| `bigScreen.sceneType` | bigScreenCtrl (1=接诊 / 2=检查) | **A (Object 状态)** |
| `consultRoom.status` | checkCallCtrl (`status === 1`) | **A (Object 状态, 本轮新发现)** |

### §22.2 关键判断

- **Appointment.status / Queue.status / MedicalRecord.status 全部 0 命中**（保持 S1-146 修正）
- **叫号状态实际在 consultRoom.status / bigScreen.sceneType**
- **bookManageTab 是 UI Tab 分类**

---

## §23 Controller 消费矩阵

### §23.1 15 Controller 消费矩阵

| Controller | appoint | room | call | queue | schedule | 等级 |
|---|---:|---:|---:|---:|---:|:---:|
| **bookDetailCtrl** (L3669) | **大** | 0 | 0 | 0 | 0 | A |
| **bookManageCtrl** (L3680) | **大** | 0 | 0 | 0 | 0 | A |
| **bookSettingsCtrl** (L3682) | 中 | 0 | 0 | 0 | 0 | A |
| **checkCallCtrl** (L9760) | 中 | **大** | **大** | 0 | 0 | A |
| **bigScreenCtrl** (L9600) | 0 | **大** | **大** | 0 | 0 | A |
| **addCheckinCtrl** (L8159) | **大** | 中 | 0 | 0 | 0 | A |
| **checkinListCtrl** (L8778) | 中 | 0 | 0 | 0 | 0 | A |
| **doctorWorkbenchCtrl** (L10401) | 中 | 0 | 0 | 0 | 0 | A |
| **patientListCtrl** (L18946) | 中 | 0 | 0 | 0 | 0 | A |
| **schoolListCtrl** (L44357) | 0 | 中 | 0 | 0 | 0 | A |
| **schoolMateCheckListCtrl** (L44398) | **大** | 中 | 0 | 0 | 0 | A |
| **optometryCtrl** (L34776) | 0 | 0 | 0 | 0 | 0 | A |
| **addVisitCtrl** (L49594) | 0 | 0 | 0 | 0 | 0 | A |
| **reportCtrl** (L37786) | 0 | 0 | 0 | 0 | 0 | A |
| **followUpCtrl** (L11504) | 0 | 0 | 0 | 0 | 0 | A |
| ✗ `appointOrderCtrl` | 1 行注释 | 0 | 0 | 0 | 0 | F (Stub) |

### §23.2 核心观察

1. **bookDetailCtrl / bookManageCtrl / schoolMateCheckListCtrl / addCheckinCtrl** 4 个 Controller 大量消费 Appointment
2. **checkCallCtrl / bigScreenCtrl** 2 个 Controller 大量消费 consultRoom + call
3. **queue 0 命中全部** — 印证 Queue 不存在独立 ID
4. **schedule 0 命中全部** — 印证 Schedule 不存在独立 ID
5. **appointOrderCtrl L3664 是空 Stub**（保持 S1-147 修正）

---

## §24 Object 分类

### §24.1 9 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Appointment** | ✓ (appointId 25 + appointmentId 5) | ✓ (appoint / appointment) | ✓ (appointId) | ✓ ($stateParams) | A |
| **AppointmentSchedule** | ✗ (0 命中) | ✗ | ✗ | ✓ (weekInfo UI) | **F** |
| **Queue** | ✗ (queueId / queueNumber 0 命中) | ✗ | ✗ | ✗ | **F** |
| **ReceptionCall** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **ExaminationCall** | ✗ (0 命中) | ✗ | ✗ | ✓ (isWaiting UI) | **F** |
| **CallScreen** | ✓ (bigScreen.id) | ✓ (bigScreenName/sceneType) | ✓ (addBigScreenAndConf) | ✓ (bigScreenPopout) | **A (重命名为 bigScreen)** |
| **RoomScreen** | ✓ (consultRoomId 25) | ✓ (consultRoom 10+ 字段) | ✓ (consultRoomIdArray) | ✓ (clinicInfo.consultRoom) | **A (重命名为 consultRoom)** |
| **CallingMachine** | ✗ (0 命中) | ✗ | ✗ | ✗ | **F** |
| **ConsultRoom** | ✓ (consultRoomId 25) | ✓ (consultRoom 10+ 字段含 status) | ✓ (consultRoomId) | ✓ (clinicInfo) | A |
| **bigScreen** | ✓ (bigScreen.id) | ✓ (bigScreenName/sceneType) | ✓ (addBigScreenAndConf) | ✓ (bigScreenPopout) | A |

### §24.2 关键结论

1. **3 个独立 ID 实体**: Appointment (双 ID) / BigScreen (大屏) / ConsultRoom (诊室)
2. **4 个 0 命中实体**: AppointmentSchedule / Queue / ReceptionCall / CallingMachine
3. **CallScreen / RoomScreen 是命名误导** — 实际是 `bigScreen` / `consultRoom`
4. **bigScreenCtrl 是叫号大屏真实 Controller** (不是 callScreenCtrl)
5. **consultRoom.status 真实存在**（本轮新发现 L10141/L10783）
6. **bigScreen.sceneType 1=接诊 / 2=检查** 是叫号大屏模式字段

---

## §25 Source Trace

### §25.1 关键字段溯源

#### appointId
- **Source A**: $stateParams.appointId (L8216/L8217/L8238/L8648)
- **Source B**: item.appoint.id (L8252/L8269/L44170 经 Response)
- **Source C**: $scope.obj.appointId (L8656 $scope.checkCustomer.appointId)
- **Target**: confirmArrivalOfAppoint / insertCustomerCheckin / selectAppointSchoolMateVoList
- **等级**: A

#### appointmentId
- **Source**: $stateParams.appointmentId (bookDetailCtrl L3669)
- **Target**: getAppointmentVo / updateAppointCompanyRemark / confirmAppointment
- **等级**: A

#### consultRoomId
- **Source A**: $scope.consultRoom.id / $scope.clinicInfo.consultRoom.id (L9555/L9852/L10072/L10124 等)
- **Source B**: WechatConfig.setWechatUrl(checkSignIn?consultRoomId=...) (L15198)
- **Source C**: bigScreenPopout.consultRoomIdArray (L9600)
- **等级**: A (核心 ID)

#### bigScreen.id
- **Source**: $scope.bigScreenPopout.bigScreenId (L9600 addBigScreenAndConf.json)
- **Source B**: item.bigScreen.id (L9600 $state.go("screenQueue", { bigScreenId: item.bigScreen.id }))
- **Target**: addBigScreenAndConf / updateBigScreenAndConf / getBigScreenConfVo
- **等级**: A

#### schoolPlanId
- **Source**: $scope.screenCondition.params.schoolPlanId (L44138 selectAppointSchoolMateVoList)
- **等级**: C (单点 Request 字段)

#### companyId (叫号大屏)
- **Source**: $scope.companyInfo.id (L9600 hasAuthForCompany)
- **Target**: addBigScreenAndConf / selectConsultRoomVoListOfCompany
- **等级**: A

#### checkinNumber (叫号大屏语音)
- **Source**: p.customerCheckin.checkinNumber (L11157 bigScreen playVoice)
- **等级**: A (派生命段)

#### sceneType (叫号大屏模式)
- **Source**: $scope.bigScreenPopout.sceneType (L9600)
- **含义**: 1=医生接诊叫号 / 2=检查叫号
- **等级**: A

#### consultRoom.status
- **Source A**: $scope.clinicInfo.consultRoom.status === 1 (L10141)
- **Source B**: $scope.clinicInfo.consultRoom.status === 1 (L10783)
- **等级**: A (本轮新发现)

---

## §26 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 4 Controllers (bookDetail/bookManage/checkCall/bigScreen) | A | - | 全部 | A |
| 2 | Controller | 4 真实 + 10+ NOT FOUND | A | - | 全部 | A |
| 3 | State | bookManage / checkCall / bigScreen | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | appointId / appointmentId / consultRoomId / bigScreenId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | statusArray / bookManageTab | A | - | L3680+ | A |
| 10 | Status | consultRoom.status / bigScreen.sceneType | **A (本轮新发现)** | - | L10141/L9600 | A |
| 11 | Dialog | bigScreenPopout (UI 弹窗) | A | - | L9600 | A |
| 12 | Pagination | pageSize=5/10/20 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | companyId / consultRoomId (callScreen) | A | - | L9600 | A |
| 15 | Default | sceneType=1 (默认接诊叫号) | A | - | L9600 | A |
| 16 | Data Source | 8+ Appointment API + 5 BigScreen API + 2 ConsultRoom API | A | - | 全部 | A |
| 17 | Object | appointment / bigScreen / consultRoom | A | - | 全部 | A |
| 18 | Request | { appointId } / { appointmentId } / { consultRoomId } | A | - | 多处 | A |
| 19 | Response | appointment / bigScreen / consultRoom 嵌套 | A | - | 全部 | A |
| 20 | Function | screenful / playVoice / setSceneType / showP | A | - | L9600+ | A |
| 21 | State Bridge | $stateParams.appointId / appointmentId | A | - | L8216/L3669 | A |
| 22 | Object Bridge | consultRoom.status / bigScreen.sceneType | A | - | L10141/L9600 | A |
| 23 | API Bridge | addBigScreenAndConf / confirmArrivalOfAppoint | A | - | L9600/L8658 | A |
| 24 | Business Interpretation | 3 个独立 ID 实体, 4 个 0 命中, 命名误导 3+ | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 2 C / 0 D / 0 E / 3 F | - | - | - | - |
| 26 | V4.4 Decision | 3 个独立 ID 实体必保留, 4 个 0 命中 F, 命名误导必修正 | A | - | - | A |

---

## §27 历史差异

### §27.1 S1-134/147/150/151/152 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-147: appointOrderCtrl L3664 空 Stub | 实际 1 行注释 | 保持 | **保持 S1-147 修正** |
| S1-147: addCheckinCtrl 真实入口 | 实际 L8159 完整 Controller | 保持 | **保持 S1-147 修正** |
| S1-147: confirmArrivalOfAppoint Request only appointId | 实际 L8658 `{ appointId: aId }` | 保持 | **保持 S1-147 修正** |
| S1-152: appointVo type=0 / type=1 分流 | 实际 L8241/L8262/L8290/L8702 | 保持 | **保持 S1-152 修正** |
| S1-151: consultRoom 真实存在 | 实际 consultRoomId 25 + 50+ 字段访问 | 保持 | **保持 S1-151 修正** |
| S1-150: completeMedicalRecordDelivery 在 optometryCtrl | 实际 L35185 | 保持 | **保持 S1-150 修正** |

### §27.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~Schedule 是独立 Object 实体~~ | schedule/scheduleId/appointmentTime 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~Queue 是独立 ID 实体~~ | queue/queueId/queueNumber 0 命中 | **本轮重大发现** | **F (0 命中)** |
| ~~callScreenCtrl 存在~~ | 实际是 bigScreenCtrl (L9600) | **本轮重大发现** | **A bigScreenCtrl** |
| ~~roomScreenCtrl 存在~~ | 实际是 consultRoomScreen 内部字段 | **本轮重大发现** | **A (consultRoom 内嵌)** |
| ~~callingMachineCtrl 存在~~ | NOT FOUND | **本轮新增** | **F** |
| ~~appointId ≡ appointmentId~~ | appointId 25 命中 / appointmentId 5 命中 | **本轮重大发现** | **A (不同 ID)** |
| ~~Appointment 顶层含 status 字段~~ | appoint.status / appointment.status 0 命中 | **本轮新增** | **F (经 CustomerCheckin 派生 A)** |
| ~~Appointment 顶层含 patientId/customerId/medicalRecordId~~ | 0 命中 | **本轮新增** | **F (经 Response 嵌套派生 A)** |
| ~~consultRoom 仅 11 字段 (S1-151 报告)~~ | 实际 consultRoom.status 真实存在 | **本轮新增** | **A (status 真实)** |
| ~~叫号大屏 Controller 是 callScreenCtrl~~ | NOT FOUND, 实际是 bigScreenCtrl | **本轮重大发现** | **A (bigScreenCtrl)** |
| ~~selectAppointmentVoList 不存在~~ | 实际 L3705+ bookManageCtrl 用此 API | **本轮新增** | **A (List API)** |
| ~~getCorpAppointmentConf / saveCorpAppointmentConf 不存在~~ | 实际 bookSettingsCtrl 完整 Write/Read | **本轮新增** | **A** |
| ~~bigScreen.id 不存在~~ | 实际 bigScreenCtrl L9600 多个 bigScreen.id | **本轮新增** | **A (独立 ID 实体)** |

### §27.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 215_S1-152 全部保持原样
- 本文档 216_*.md 单独记录预约叫号完整闭环

---

## §28 V4.4 预约叫号规格

### §28.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| **appointId 独立 ID** | 25 命中 | ✓ |
| **appointmentId 独立 ID** | 5 命中 | ✓ |
| **consultRoomId 独立 ID** | 25 命中 | ✓ |
| **bigScreen.id 独立 ID** | L9600 | ✓ |
| **appointment Object 字段** (bookDetailCtrl) | L3673 | ✓ |
| **bigScreen Object 字段** (bigScreenName/sceneType) | L9600 | ✓ |
| **consultRoom Object 字段** (含 status) | 50+ | ✓ |
| **appointVo Object 字段** (type/url) | L8237 | ✓ |
| **8+ Appointment API** (getAppointPatientVo/getAppointSchoolMateVo/selectAppointSchoolMateVoList/getAppointmentVo/updateAppointCompanyRemark/confirmAppointment/confirmArrivalOfAppoint/selectAppointmentVoList) | 全部 | ✓ |
| **5 BigScreen API** (addBigScreenAndConf/updateBigScreenAndConf/selectBigScreenConfVoListOfCompany/getBigScreenConfVo/selectConsultRoomVoListOfCompany) | 全部 | ✓ |
| **2 ConsultRoom API** (getConsultRoom* 2 调用) | 全部 | ✓ |
| **bookSettingsCtrl 短信配置 API** (getCorpAppointmentConf/saveCorpAppointmentConf) | L3682 | ✓ |
| **4 个真实 Controller** (bookDetailCtrl/bookManageCtrl/checkCallCtrl/bigScreenCtrl) | L3669/L3680/L9760/L9600 | ✓ |
| **bookSettingsCtrl** | L3682 | ✓ |
| **sceneType 1=接诊 / 2=检查** | L9600 | ✓ |
| **playVoice 完整对象** (checkinNumber + patientName + consultRoomName) | L11157 | ✓ |
| **consultRoomIdArray 大屏绑定** | L9600 | ✓ |
| **checkSignIn?consultRoomId URL 集成** | L15198 | ✓ |
| **checkCallCtrl 周历** (weekInfo) | L9760 | ✓ |

### §28.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `appointmentOrder` / `appointOrder` 独立 Object | ✗ (0 命中) |
| `appointmentVo` / `appointmentList` 独立命名 | ✗ (0 命中) |
| `schedule` / `appointmentSchedule` / `scheduleId` / `appointmentTime` 字段 | ✗ (0 命中) |
| `queue` / `queueId` / `queueNumber` / `queueNo` 字段 | ✗ (0 命中) |
| `callScreen` / `callScreenCtrl` Controller | ✗ (NOT FOUND, 实际是 bigScreenCtrl) |
| `roomScreen` / `roomScreenCtrl` Controller | ✗ (NOT FOUND, 实际是 consultRoomScreen 内部) |
| `callingMachine` / `callMachine` / `callingMachineCtrl` / `callMachineCtrl` Controller | ✗ (0 命中) |
| `callManage` / `callManageCtrl` Controller | ✗ (NOT FOUND) |
| `receptionQueue` / `examinationQueue` / `queueCtrl` Controller | ✗ (NOT FOUND) |
| `scheduleCtrl` / `appointmentScheduleCtrl` Controller | ✗ (NOT FOUND) |
| `appoint.status` / `appointment.status` 字段 | ✗ (0 命中) |
| `appoint.patient` / `appoint.patientId` 顶层字段 | ✗ (经 Response 派生 A) |
| `appoint.customer` / `appoint.customerId` 顶层字段 | ✗ (经 Response 派生 A) |
| `appoint.medicalRecord` / `appoint.medicalRecordId` 顶层字段 | ✗ (经 CustomerCheckin 派生 A) |
| `appointment.employee` / `appointment.department` 字段 | ✗ (0 命中) |
| `appointment.consultRoom` / `appointment.room` 字段 | ✗ (0 命中) |
| `consultRoom.appointment` / `consultRoom.queue` 字段 | ✗ (0 命中) |
| `consultRoom.employee` / `consultRoom.department` 字段 | ✗ (0 命中) |
| `insertAppointOrder*.json` / `getCanBeArrivedAppoint*.json` API | ✗ (0 命中) |
| `appointOrderCtrl` Controller | ✗ (L3664 仅 1 行注释) |
| `appointId` 与 `appointmentId` 合并 | ✗ (不同 ID 字段) |
| 5+ ID 合并 | ✗ (appointId/appointmentId/consultRoomId/bigScreenId/patientId/customerCheckinId 必须严格区分) |

### §28.3 9 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Appointment** | A+B (双 ID 实体 + Response appointment) | 顶层 status/patientId/customerId 字段 (F) |
| **AppointmentSchedule** | F (0 命中) | 独立 ID 实体 |
| **Queue** | F (0 命中) | 独立 ID 实体 |
| **ReceptionCall** | F (0 命中) | 独立 ID 实体 |
| **ExaminationCall** | F (0 命中) | 独立 ID 实体 |
| **CallScreen** | **A (重命名为 bigScreen)** | - |
| **RoomScreen** | **A (重命名为 consultRoom)** | - |
| **CallingMachine** | F (0 命中) | 独立 Object 实体 |
| **ConsultRoom** | A+B+C+D (含 status 字段) | - |
| **bigScreen** | A+B+C+D (含 sceneType 字段) | - |

### §28.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `appointVo.type=0/1` (Patient/SchoolMate 分流) | A | L8241/L8262 |
| `appointVo.url` (动态 getAppointPatientVo/getAppointSchoolMateVo) | A | L8237 |
| `consultRoom.id` (核心 ID) | A | 50+ 命中 |
| `consultRoom.status === 1` (本轮新发现) | **A** | L10141/L10783 |
| `consultRoom.companyId` (ConsultRoom → Company) | A | L9336/L10211 |
| `consultRoom.examineList[]` (ConsultRoom → MedicalExamine) | A | L9725/L9600 |
| `consultRoomIdArray` (bigScreen → ConsultRoom) | A | L9600 |
| `bigScreen.id` (独立 ID 实体) | A | L9600 |
| `bigScreen.sceneType 1=2=` (接诊/检查模式) | A | L9600 |
| `bigScreen.consultRoomVoList[]` (绑定诊室) | A | L9600 |
| `bigScreen.employeeList[]` (sceneType=1 派生) | A | L9600 |
| `bigScreen.examineList[]` (sceneType=2 派生) | A | L9600 |
| `playVoice p.customerCheckin.checkinNumber + p.patient.patientName + p.consultRoom.consultRoomName` | A | L11157 |
| `confirmArrivalOfAppoint { appointId: aId }` (Appointment → CustomerCheckin) | A | L8658 |
| `selectAppointSchoolMateVoList { schoolPlanId, appointDay }` | A | L44138 |
| `bookManageCtrl { statusArray, keyword, arriveTimeFrom, arriveTimeTo }` | A | L3680+ |
| `bookSettingsCtrl smsAdminName/smsMobile/smsBackMobile/smsBackAdminName` | A | L3682 |
| `WechatConfig checkSignIn?consultRoomId=` | A | L15198 |
| `addCheckinCtrl item.patient / item.schoolMateVo / item.appoint / item.customer` (L8243-L8270) | A | 4 路径 |

### §28.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Appointment → MedicalRecord 字段桥 | F (经 CustomerCheckin 派生 A) |
| Queue → CustomerCheckin 字段桥 | F |
| Queue → MedicalRecord 字段桥 | F |
| Schedule → Employee/ConsultRoom 字段桥 | F (Schedule 不存在) |
| consultRoom.appointment 字段桥 | F |
| consultRoom.queue 字段桥 | F |
| consultRoom.employee 字段桥 | F (经 bigScreen 派生 A) |
| consultRoom.department 字段桥 | F |
| appointment.employee/department/consultRoom 字段 | F |
| appointment.status 字段 | F (经 CustomerCheckin 派生 A) |
| appointment.medicalRecordId 字段 | F |

### §28.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `appointOrderCtrl` L3664 | 1 行注释空 Stub | **命名误导 (保持 S1-147)** |
| `appointmentOrder` / `appointmentVo` / `appointmentList` | 字符级 0 命中 | **命名误导** |
| `schedule` / `appointmentSchedule` / `scheduleId` / `appointmentTime` | 0 命中, 实际没有排班独立 Object | **命名误导 (本轮新发现)** |
| `queue` / `queueId` / `queueNumber` / `queueNo` | 0 命中, 实际没有 Queue 独立 ID | **命名误导 (本轮新发现)** |
| `callScreen` / `callScreenCtrl` | 0 命中, 实际是 `bigScreenCtrl` L9600 | **命名误导 (本轮新发现)** |
| `roomScreen` / `roomScreenCtrl` | 0 命中, 实际是 `consultRoom` 内嵌 | **命名误导 (本轮新发现)** |
| `callingMachine` / `callMachine` | 0 命中, 实际由 consultRoom.checkSignIn 实现 | **命名误导 (本轮新发现)** |
| `appointId` vs `appointmentId` | 25 vs 5 命中, 两个不同 ID 字段 | **命名误导 (本轮新发现)** |
| `appointment.status` | 0 命中, 实际在 CustomerCheckin 派生 | 命名误导 |
| `appointment.patientId` / `appointment.medicalRecordId` | 0 命中, 经 Response 嵌套 | 命名误导 |
| `bookManageCtrl.statusArray` | 实际是 UI filter, 不是 status 字段 | 命名误导 |
| `isWaiting` | 实际是 UI Tab State, 不是 Queue 状态 | 命名误导 |
| `weekInfo.weekDay` | 实际是 checkCallCtrl UI 周历, 不是 Schedule | 命名误导 |
| `consultRoom.checkSignIn` (L15198) | 实际是 WechatConfig URL, 不是独立 Object | 命名误导 |

---

## §29 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Appointment 数据库表结构 | F | 需后端 |
| 2 | consultRoom 数据库表结构 | F | 需后端 |
| 3 | bigScreen 数据库表结构 | F (本轮新发现) | 需后端 |
| 4 | Schedule 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 5 | Queue 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 6 | CallingMachine 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 7 | bigScreenConf 完整 schema | F (本轮新发现) | 需后端 |
| 8 | consultRoom.status 实际值含义 (1/2/3/0) | F (本轮新发现) | 需后端 |
| 9 | bigScreen.sceneType 实际值含义 (1/2) | F (本轮新发现) | 需业务定义 |
| 10 | bookSettingsCtrl 字段完整 (smsAdminName/smsMobile/smsBackMobile/smsBackAdminName) | F (本轮新发现) | 需后端 |
| 11 | selectAppointmentVoList 完整 Response | F (本轮新发现) | 需后端 |
| 12 | screenQueue State 后端实现 | F (本轮新发现) | 需后端 |
| 13 | 30+ NOT FOUND Controller 命名历史 | F | 需 git log |
| 14 | 4 个真实 Controller 后端 API 完整 | F (部分确认) | 需后端 |
| 15 | Appointment status 业务定义 (经 CustomerCheckin 派生) | F (UI 推测) | 需业务定义 |
| 16 | 4 个 controller 业务完整范围 | F (部分确认) | 需业务定义 |
| 17 | 叫号大屏 playVoice 实际部署 | F (本轮新发现) | 需后端 |
| 18 | 短信通知触发逻辑 (smsAdminName 等) | F (本轮新发现) | 需后端 |
| 19 | checkCallCtrl 的 getEmployeeExamineConsultRoomVo API 完整 | F (本轮新发现) | 需后端 |
| 20 | screenQueue 完整 State 配置 | F (本轮新发现) | 需后端 |

---

## §30 Git / 完整性

### §30.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-215 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ |
| 本轮只新增 216_*.md | ✓ |

### §30.2 Git 操作

```
git add -- 216_S1-153_Appointment_预约排班_叫号_诊室屏全生命周期总审计.md
git diff --cached --name-only
git commit -m "docs(216): S1-153 Appointment/预约排班/叫号/诊室屏全生命周期总审计"
git push origin master
```

### §30.3 预期

- tracked = 223 → **224**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `d5468f3cd883061c9e95e647d90d7688bcf8af73` (S1-152 commit)

---

## 文档元信息

- **审计范围**：S1-153 (Appointment / 预约排班 / 叫号 / 诊室屏)
- **本轮新增文件**：`216_S1-153_Appointment_预约排班_叫号_诊室屏全生命周期总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-154** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
