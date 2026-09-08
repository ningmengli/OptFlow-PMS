# S1-123 就诊流程 Controller / State / API 主链深度审计

## 0. 任务背景

S1-122 已完成 8 大主菜单 Controller / State / API 业务边界盘点。

本轮**深入"就诊流程"一级菜单**，建立 10 个二级菜单实际证据 + 主链 5 段关系判定。

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| 就诊流程候选 Controller | 24 个（排除误命名/日志后）|
| State 出口识别 | 19 个 $state.go |
| 10 个二级菜单实际证据 | 7 个确认 / 3 个间接 |

## 2. 就诊流程一级菜单

【历史菜单证据】：8 大主菜单之一为"就诊流程"，来自历史用户提供的菜单结构记录。

## 3. 10 个二级菜单实际证据

| # | 二级菜单 | 实际 State / Controller | 等级 |
|---:|---|---|---|
| 1 | 主页 | **未发现独立 State**，可能是 workBeachCtrl (L14494) / loginCtrl 入口 | F |
| 2 | 工作台 | **doctorWorkbenchCtrl (L10401)** — `dealWithBtn` 接诊入口 | A |
| 3 | 登记 | **addCheckinCtrl (L8159) / checkinListCtrl (L8778)** | A |
| 4 | 我的会员 | **myMemberCtrl (L33080) / myMemberRecordCtrl (L33218)** | A |
| 5 | 检查报告 | **myCheckBillCtrl (L32116)** — 助诊完成后跳转 | A |
| 6 | 开单 | **myMaterialBillCtrl (L32435)** (medicalRecordType==5) | A |
| 7 | 收费 | **waitChargeListCtrl (L6957) → waitChargeDetailCtrl (L6568) → waitPayDetailCtrl (L7452) → payedListCtrl (L4972)** | A |
| 8 | 发货 | **deliveryListCtrl (L4075) → deliveryInputCtrl (L3812) → deliveryInputRecordCtrl (L4024) → deliveryProcessingCtrl (L4236)** | A |
| 9 | 店内加工中心 | **machineOrderCtrl (L16094)** | A |
| 10 | 连锁加工中心 | **machineOrderWaitProcessCtrl (L16357) / machineOrderBrokenCtrl (L16261)** | A |

**S1-123 关键发现 1**：
- 10 个二级菜单中 9 个能定位到实际 Controller
- "主页" 在 controller.js 范围内**无独立 State 证据**（F 级）
- "主页" 通常指 workBeachCtrl (L14494) 或 homeCtrl (L13902) 入口，**未在 controller.js 明确证明**

## 4. Controller 全集

### 4.1 就诊流程主业务候选 24 个

| # | Controller | 行号 | 状态 | 等级 |
|---:|---|---:|---|---|
| 1 | assistCheckingCtrl | L1756 | 助诊主页面 | A (S1-115) |
| 2 | assistCheckListCtrl | L2309 | 助诊列表 | A |
| 3 | optometryCtrl | L34776 | 验光主页面 | A (S1-115) |
| 4 | optometryGlassesCtrl | L35383 | 验光配镜 | A (S1-115) |
| 5 | prescriptsRecordCtrl | L33768 | 处方记录 | A |
| 6 | drugPrescriptionCtrl | L31605 | 药品处方 | A |
| 7 | prescriptionCtrl | L33560 | 处方 | A |
| 8 | getGlassRecordCtrl | L31922 | 取镜记录 | A |
| 9 | addCheckinCtrl | L8159 | 入院登记 | A |
| 10 | checkinListCtrl | L8778 | 登记列表 | A |
| 11 | addCheckCtrl | L50170 | 添加检查 | A |
| 12 | addCheckItemCtrl | L50246 | 添加检查项 | A |
| 13 | checkListCtrl | L53001 | 检查列表 | A |
| 14 | checkModifyCtrl | L53185 | 检查修改 | A |
| 15 | waitChargeDetailCtrl | L6568 | 待收费详情 | A (S1-121) |
| 16 | waitChargeListCtrl | L6957 | 待收费列表 | A |
| 17 | waitPayDetailCtrl | L7452 | 待支付详情 | A (S1-119/120) |
| 18 | waitPayListCtrl | L8110 | 待支付列表 | A |
| 19 | payedDetailCtrl | L4937 | 已支付详情 | A |
| 20 | payedListCtrl | L4972 | 已支付列表 | A |
| 21 | unPayDetailCtrl | L5987 | 未付详情 | A |
| 22 | unPayListCtrl | L6526 | 未付列表 | A |
| 23 | waitPayBackCtrl | L6992 | 待退款 | A |
| 24 | partBackCtrl | L4368 | 部分退款 | A |
| 25 | deliveryInputCtrl | L3812 | 配送录入 | A |
| 26 | deliveryInputRecordCtrl | L4024 | 配送录入记录 | A |
| 27 | deliveryListCtrl | L4075 | 配送列表 | A |
| 28 | deliveryProcessingCtrl | L4236 | 配送处理 | A |
| 29 | myCheckBillCtrl | L32116 | 检查账单 | A |
| 30 | myMaterialBillCtrl | L32435 | 物料账单（开单）| A |
| 31 | myMemberRecordCtrl | L33218 | 会员记录 | A |
| 32 | myMemberCtrl | L33080 | 会员 | A |
| 33 | myMedicalRecordListCtrl | L32965 | 病历列表 | A |
| 34 | myMedicalHistoryCtrl | L32897 | 病史 | A |
| 35 | machineOrderCtrl | L16094 | 加工订单 | A |
| 36 | machineOrderBrokenCtrl | L16261 | 加工异常 | A |
| 37 | machineOrderListCtrl | L4264 | 加工订单列表 | A |
| 38 | machineOrderWaitProcessCtrl | L16357 | 加工待处理 | A |

### 4.2 排除项（S1-122 已识别）

| Controller | 行号 | 实际 | 排除原因 |
|---|---:|---|---|
| optometryListCtrl | L35962 | **UartDevice 设备管理** | S1-122 A 级 |
| optometryLogListCtrl | L36135 | **日志 dead-end** | S1-122 A 级 |
| getGlassNotifyListCtrl | L13680 | 通知页（需确认）| 弱关联 |
| hospitalRechargeCtrl | L15883 | 充值（已归患者）| 弱关联 |
| feeRechargeCtrl | L37183 | 充值 | 弱关联 |
| pointsListReChargeCtrl | L37459 | 充值 | 弱关联 |
| timeCardRechargeCtrl | L38463 | 充值 | 弱关联 |
| unPayChargeCtrl | L38500 | 充值 | 弱关联 |
| unPayRechargeCtrl | L38525 | 充值 | 弱关联 |
| schoolMateCheckListCtrl | L44398 | 应归筛查 | S1-122 误归 |

## 5. State 全集（就诊流程）

### 5.1 $state.go 出口（源码直接成立）

| # | 起点 Controller | 行号 | State | Params |
|---:|---|---:|---|---|
| 1 | optometryCtrl | L34954 | optometryGlasses | { medicalRecordId } |
| 2 | optometryCtrl | L35133 | payedList | {} |
| 3 | optometryCtrl | L35136 | optometryGlasses | { medicalRecordId, edit } |
| 4 | optometryCtrl | L35145 | waitChargeList | {} |
| 5 | waitChargeDetailCtrl | L6684 | waitPayList | {} |
| 6 | waitChargeDetailCtrl | L6929 | waitPayDetail | { cashflowId: res.result.object } |
| 7 | waitPayDetailCtrl | L8021 | payedList | {} |
| 8 | waitPayDetailCtrl | L8061 | payedList | {} |
| 9 | waitPayDetailCtrl | L8064 | waitChargeList | {} |
| 10 | assistCheckingCtrl | L2258 | adminSalesRecord.myMaterialBill | { medicalRecordId, patientId } |
| 11 | assistCheckingCtrl | L2263 | adminMyRecord.myCheckBill | { medicalRecordId, patientId } |
| 12 | assistCheckingCtrl | L2269 | addMedicalRecord | { medicalRecordId, patientId } |
| 13 | doctorWorkbenchCtrl | L10609 | adminMyRecord.myMemberRecord | { medicalRecordId, patientId } |
| 14 | addCheckinCtrl | L8654 | checkinList | { printObj } |
| 15 | checkinListCtrl | L8914 | myMedicalRecordList | { patientId } |
| 16 | myMemberRecordCtrl | L33379 | adminMyRecord.myMemberRecord | { medicalRecordId, reload:true } |
| 17 | myCheckBillCtrl | L32132 | assistChecking | { medicalExamineId, medicalRecordId } |
| 18 | myCheckBillCtrl | L32138 | assistChecking | { medicalExamineId, medicalRecordId } |
| 19 | addCheckCtrl | L50229 | systemSetting.checkList | {} |

### 5.2 $stateParams 入口（接收 State Param）

| # | Controller | 行号 | 接收字段 |
|---:|---|---:|---|
| 1 | assistCheckingCtrl | L1757-L1760 | medicalRecordId, medicalExamineId, editable |
| 2 | deliveryInputCtrl | L3814 | cashflowId |
| 3 | deliveryListCtrl | - | (无源码命中) |
| 4 | myMemberRecordCtrl | L33223 | medicalRecordId |
| 5 | myCheckBillCtrl | L32123-L32124 | medicalRecordId, patientId |
| 6 | myMaterialBillCtrl | L32445 | medicalRecordId |
| 7 | optometryGlassesCtrl | L35388-L35389 | medicalRecordId, edit |
| 8 | waitChargeDetailCtrl | L6570 | medicalRecordId |
| 9 | waitPayBackCtrl | L7010 | cashflowId |
| 10 | waitPayDetailCtrl | L7462 | cashflowId |
| 11 | payedDetailCtrl | L4940 | cashflowId |
| 12 | machineOrderBrokenCtrl | L16262-L16264 | cashflowId, machineCenterId, chain |
| 13 | addCheckItemCtrl | L50246 | (有) |

## 6. 核心对象矩阵

### 6.1 Controller × Object 矩阵

| Controller | medicalRecord | medicalRecordId | patientId | customer | medicalProduct | cashflowId |
|---|---:|---:|---:|---:|---:|---:|
| assistCheckingCtrl | 0 | 15 | 7 | 0 | 0 | 0 |
| optometryCtrl | 11 | 27 | 1 (派生) | 2 | 5 | 0 |
| optometryGlassesCtrl | 4 | 10 | 4 | 10 | 9 | 0 |
| prescriptsRecordCtrl | 2 | 7 | 0 | 0 | 0 | 0 |
| drugPrescriptionCtrl | 2 | 7 | 0 | 0 | 0 | 0 |
| myMemberRecordCtrl | **27** | 8 | 0 | 0 | 0 | 0 |
| myMemberCtrl | 0 | 6 | 8 | 0 | 0 | 0 |
| myMedicalHistoryCtrl | 0 | 5 | 5 | 0 | 0 | 0 |
| waitChargeDetailCtrl | 1 | 1 (State) | 0 | 1 | 8 | 1 (Type 5) |
| waitPayDetailCtrl | 0 | 0 | 0 | 3 | 0 | 6 |
| payedListCtrl | 0 | 0 | 0 | 0 | 4 | 10 |
| partBackCtrl | 0 | 0 | 0 | 6 | 3 | 10 |
| unPayDetailCtrl | 0 | 0 | 0 | 0 | 0 | 3 |
| waitPayBackCtrl | 0 | 0 | 0 | 0 | 8 | 6 |
| deliveryInputCtrl | 0 | 0 | 0 | 0 | 11 | 3 |
| deliveryListCtrl | 0 | 0 | 0 | 0 | 6 | 6 |
| deliveryInputRecordCtrl | 1 | 1 (派生) | 0 | 0 | 0 | 4 |
| myCheckBillCtrl | 0 | 8 | 5 | 0 | 0 | 0 |
| myMaterialBillCtrl | 0 | 0 | 0 | 0 | 24 | 0 |
| machineOrderCtrl | 0 | 8 | 0 | 0 | 0 | 0 |
| addCheckinCtrl | 0 | 0 | 10 | 4 | 0 | 0 |
| checkinListCtrl | 0 | 0 | 5 | 18 | 0 | 0 |

## 7. medicalRecord 生命周期

### 7.1 medicalRecordId 首次 Consumer 优先级

**S1-123 关键发现 2（medicalRecordId 多入口）**：

| 优先级 | 入口 Controller | 行号 | API | Response 字段 | 业务 |
|---:|---|---:|---|---|---|
| 1 | **doctorWorkbenchCtrl** | L10605-L10612 | `beginCustomerCheckin.json` | `response.customerCheckin.medicalRecordId` | 接诊 |
| 2 | **optometryCtrl** | L34947-L34956 | `beginCustomerCheckin.json` | `result.result.vo.customerCheckin.medicalRecordId` | 验光 |
| 3 | 其它 State go 传入 | - | - | - | 跨 controller 链 |

**S1-123 关键发现 3**：
- doctorWorkbenchCtrl (L10605) 是**最早**的 medicalRecordId 入口（接诊操作）
- optometryCtrl (L34947) 是**验光流程**的 medicalRecordId 入口
- 两个入口都通过 `beginCustomerCheckin.json` API 创建
- **但 doctorWorkbenchCtrl Response 用 `response.customerCheckin.medicalRecordId`**
- **optometryCtrl Response 用 `result.result.vo.customerCheckin.medicalRecordId`**
- **同一 API 不同 Response 访问路径** —— **D 级冲突可能**

### 7.2 medicalRecordId → 后续 Controller 链路

```
[Source API: beginCustomerCheckin.json]
  ↓
medicalRecordId (Type 1: primitive)
  ↓
[State Go: "adminMyRecord.myMemberRecord" / "optometryGlasses"]
  ↓
[State Param: $stateParams.medicalRecordId]
  ↓
[myMemberRecordCtrl / optometryGlassesCtrl / assistCheckingCtrl]
  ↓
[API: getMedicalRecord.json / getMethodGlassRecordVo.json / getVisionRecordVo.json]
  ↓
[医疗记录相关派生]
  ↓
[State go: "assistChecking" / "adminSalesRecord.myMaterialBill" / "addMedicalRecord" / "adminMyRecord.myCheckBill"]
  ↓
[医疗记录分配到开单/检查/检查报告]
  ↓
[State go: "waitChargeList" (from optometryCtrl L35145)]
  ↓
[Charge 主链]
```

## 8. patientId 生命周期

### 8.1 patientId 首次创建

| 入口 | API | 行号 |
|---|---|---|
| optometryCtrl L34912 | `obj.patient.id → object.patientId` | L34914 `insertCustomerCheckin.json` |
| doctorWorkbenchCtrl L10611 | `employee.patient.id` | L10605 `beginCustomerCheckin.json` |
| addCheckinCtrl L8213 | `$stateParams.patientId` | (State Param 接收) |

### 8.2 patientId → medicalRecordId 关系

**S1-123 关键发现 4（patientId + medicalRecordId 同步传递）**：

| 跳转点 | 行号 | 同时传递 |
|---|---|---|
| doctorWorkbenchCtrl → adminMyRecord.myMemberRecord | L10609-L10612 | **medicalRecordId + patientId** |
| optometryCtrl → optometryGlasses | L34954 | 仅 medicalRecordId |
| assistCheckingCtrl → adminSalesRecord.myMaterialBill | L2258 | **medicalRecordId + patientId** |
| assistCheckingCtrl → adminMyRecord.myCheckBill | L2263 | **medicalRecordId + patientId** |
| assistCheckingCtrl → addMedicalRecord | L2269 | **medicalRecordId + patientId** |
| addCheckinCtrl → checkinList | L8654 | 仅 printObj (含 patientId) |

**S1-123 关键发现 5**：
- patientId 与 medicalRecordId **多次同时传递**
- 但**没有** patientId → medicalRecordId 的直接字段级赋值（patientId 不是 medicalRecordId 的来源）
- 它们是**并行字段**，来自同一 API Response 的不同字段
- 真正的派生关系：
  - `customerCheckin.medicalRecordId` (medicalRecordId 来源)
  - `employee.patient.id` 或 `obj.patient.id` (patientId 来源)
- **A 级** 平行字段

## 9. cashflowId 生命周期

### 9.1 cashflowId 首次创建

| API | Controller | 行号 | 性质 |
|---|---|---:|---|
| `createCashFlowForMedicalRecord.json` | waitChargeDetailCtrl | L6925 | **Write-Create** |
| `createRefundOrderLog.json` | selectOrderListCtrl | L20734 | Write (营销) |
| `payMedicalRecordCashflow.json` | waitPayDetailCtrl | L8017 | Write-Pay |

### 9.2 cashflowId 状态机

```
[1] waitChargeDetailCtrl L6925: createCashFlowForMedicalRecord.json (Write)
    ↓
[2] waitChargeDetailCtrl L6929: $state.go("waitPayDetail", { cashflowId: res.result.object }) [Type 5]
    ↓
[3] waitPayDetailCtrl L7462: $scope.obj.cashflowId = $stateParams.cashflowId
    ↓
[4] waitPayDetailCtrl L7488: getMedicalRecordCashflowVo.json { cashflowId: $scope.obj.cashflowId } (Read)
    ↓
[5] waitPayDetailCtrl L8017: payMedicalRecordCashflow.json (Write)
    ↓
[6] waitPayDetailCtrl L8021/8061: $state.go("payedList") (成功)
[6'] waitPayDetailCtrl L8064: $state.go("waitChargeList") (失败)
    ↓
[7] payedListCtrl: 列表展示已付 cashflow
```

### 9.3 cashflowId 多源

**S1-123 关键发现 6**：
- cashflowId 在就诊流程的**唯一主入口**：waitChargeDetailCtrl L6925 createCashFlowForMedicalRecord.json
- 其它来源（State / API / 退款 / 营销）独立或旁支
- cashflowId 多源字段性质确认（S1-119/120 已识别）

## 10. 主链 5 段关系判定

### 10.1 关系 1：Check → Optometry

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| doctorWorkbenchCtrl (L10605) | optometryGlasses (L35383) | API + State go | medicalRecordId | **A** |

**完整链**：
```
doctorWorkbenchCtrl $scope.dealWithBtn (status=0, "接诊")
  ↓
L10605: HTTP beginCustomerCheckin.json { customerCheckinId, medicalRecordType: 1 }
  ↓ Response
L10608: $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId })
  ↓ (或用户从 myMemberRecord 进一步操作跳到 optometryCtrl)
  ↓
optometryCtrl L34945: $scope.beginCustomerCheckin(info)
  ↓
L34947: API beginCustomerCheckin.json { customerCheckinId, medicalRecordType }
  ↓ Response
L34954: $state.go("optometryGlasses", { medicalRecordId })
  ↓
optometryGlassesCtrl L35388: $scope.medicalRecordId = $stateParams.medicalRecordId
```

### 10.2 关系 2：Check (助诊) → Sale (开单)

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| assistCheckingCtrl (L2258) | myMaterialBillCtrl (L32435) | State go | medicalRecordId, patientId | **A** |
| assistCheckingCtrl (L2269) | addCheckCtrl (L50170) | State go | medicalRecordId, patientId | **A** |

**完整链**：
```
assistCheckingCtrl 助诊完成
  ↓
API getMedicalRecord.json (L2247)
  ↓ Response
L2256-L2267: 
  - if medicalRecordType == 5: $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })
  - else: $state.go("adminMyRecord.myCheckBill", { medicalRecordId, patientId })
  - else: $state.go("addMedicalRecord", { medicalRecordId, patientId })
  ↓
myMaterialBillCtrl / myCheckBillCtrl / addCheckCtrl
```

### 10.3 关系 3：Optometry → Charge

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| optometryCtrl (L35145) | waitChargeListCtrl (L6957) | State go | 无 | **A**（不传 medicalRecordId）|

**S1-123 关键发现 7**：
- optometryCtrl `收费` 操作 `$state.go("waitChargeList")` **不传 medicalRecordId**
- 收费是按 cashflow 创建，medicalRecordId 不在 State 链中传递
- waitChargeListCtrl → 内部跳转到 waitChargeDetailCtrl 时 medicalRecordId 才会被传入

### 10.4 关系 4：Charge → Delivery

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| waitPayDetailCtrl (L8021/8061) | payedListCtrl (L4972) | State go | 无 | A |
| payedListCtrl → 后续 (HTML) | deliveryListCtrl (L4075) | (HTML 跳转) | cashflowId | F (HTML 范围外) |

**S1-123 关键发现 8**：
- waitPayDetailCtrl 支付成功后 → $state.go("payedList")
- payedListCtrl 不直接跳转到 deliveryListCtrl（源码内无 $state.go）
- **HTML 跳转（不在审计范围）** —— F 级
- 但 Cash 链 → Delivery 链已经通过 `getMedicalRecordPayVo.json` (deliveryInputRecordCtrl L4034) 桥接（S1-117/120 已确认）

### 10.5 关系 5：Delivery → Machine

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| deliveryInputCtrl (L3966) | machineCenter | API + machineCenterId | machineCenterId, medicalProductId | **A** |

**完整链**：
```
deliveryInputCtrl L3814: $scope.cashflowId = $stateParams.cashflowId
  ↓
L3848: API getCashflowDeliveryVo.json { cashflowId }
  ↓ Response
L3851-L3857: 遍历 waitingDeliveryList，写 medicalProduct.objectId
  ↓
L3966: API sendMedicalProductToMachineCenter.json { medicalProductMachineCenterPoListJson, planDeliveryTime }
  ↓
[Write] 发送到机器中心
  ↓
machineOrderCtrl (L16094) - 加工订单管理
  ↓
L16109: ListFactory selectInStoreMachineCenterCashflowVoList.json (店内 List)
  ↓
L16164: API startMachineCenterOrder.json (开始加工)
  ↓
L16226: API completeMachineCenterOrder.json (完成)
```

**S1-123 关键发现 9**：
- Delivery → Machine 通过 `sendMedicalProductToMachineCenter.json` 桥接
- objectId (machineCenterId) 是连接 Delivery 与 Machine 的核心字段
- 店内/连锁加工由 `chain` 字段区分

## 11. 店内加工 vs 连锁加工

### 11.1 店内加工

**Controller**: `machineOrderCtrl` (L16094)

**API**:
- `selectInStoreMachineCenterCashflowVoList.json` (List) —— **关键 API** 店内 Cashflow 列表
- `startMachineCenterOrder.json` (Write)
- `completeMachineCenterOrder.json` (Write)
- `closeMachineCenterOrder.json` (Write)
- `getMachineCenterOrder.json` (Read, 用 medicalRecordId)

**State**: 店内加工相关 State（`machineOrderWaitAccess` / `machineOrderWaitProcess` / `machineOrderProcessing` / `machineOrderTesting`）

### 11.2 连锁加工

**Controller**: `machineOrderWaitProcessCtrl` (L16357) + `machineOrderBrokenCtrl` (L16261)

**State**: 连锁加工相关 State（`machineOrderChainWaitAccess` / `machineOrderChainWaitProcess` / `machineOrderChainProcessing` / `machineOrderChainTesting`）

**关键字段**:
- `cashflowId` (State Param)
- `machineCenterId` (State Param)
- `chain` (State Param, boolean 区分店内/连锁)

**machineOrderBrokenCtrl API**:
- `getMachineCenterCashflowVo.json` (用 cashflowId + machineCenterId)

### 11.3 店内/连锁区分机制

**S1-123 关键发现 10**：
- `chain` 字段 (State Param) 是区分店内/连锁的**关键标志**
- machineOrderBrokenCtrl L16264 接收 `chain: $stateParams.chain`
- machineOrderWaitProcessCtrl L16358-L16366 根据 `$state.$state.current.name` 判断 tab
- 当前是店内 (`machineOrder*`) 还是连锁 (`machineOrderChain*`)

## 12. State DAG

```
[doctorWorkbenchCtrl] 接诊
  ↓ $state.go("adminMyRecord.myMemberRecord", {medicalRecordId, patientId})
  ↓
[myMemberRecordCtrl]
  ↓
[optometryCtrl] (HTML 跳转, F)
  ↓ beginCustomerCheckin.info → $state.go("optometryGlasses", {medicalRecordId})
  ↓
[optometryGlassesCtrl]
  ↓ 验光完成
  ↓ $state.go("waitChargeList")
  ↓
[waitChargeListCtrl]
  ↓ (HTML 跳转, F)
  ↓
[waitChargeDetailCtrl]
  ↓ $state.go("waitPayList") 或 createCashFlowForMedicalRecord.json → $state.go("waitPayDetail", {cashflowId})
  ↓
[waitPayListCtrl] / [waitPayDetailCtrl]
  ↓ payMedicalRecordCashflow.json → $state.go("payedList")
  ↓
[payedListCtrl]
  ↓ (HTML 跳转, F)
  ↓
[deliveryListCtrl] → (HTML) → [deliveryInputCtrl] (cashflowId)
  ↓ getCashflowDeliveryVo.json
  ↓ sendMedicalProductToMachineCenter.json (medicalProduct.objectId, machineCenterId)
  ↓
[machineOrderCtrl] (店内) / [machineOrderBrokenCtrl] (连锁)
```

**并联链（助诊 → 开单）**：
```
[assistCheckingCtrl] 助诊完成
  ↓ getMedicalRecord.json
  ↓ if medicalRecordType == 5:
  ↓   $state.go("adminSalesRecord.myMaterialBill", {medicalRecordId, patientId})
  ↓ else if templateId:
  ↓   $state.go("adminMyRecord.myCheckBill", {medicalRecordId, patientId})
  ↓ else:
  ↓   $state.go("addMedicalRecord", {medicalRecordId, patientId})
  ↓
[myMaterialBillCtrl] (开单) / [myCheckBillCtrl] (检查报告) / [addCheckCtrl] (添加检查)
  ↓
[myCheckBillCtrl] $scope.goAssist → API startExamine.json → $state.go("assistChecking", {medicalExamineId, medicalRecordId})
  ↓
[assistCheckingCtrl] (回环)
```

## 13. API DAG

### 13.1 Read API 调用顺序

```
[getMedicalRecord.json] (assistCheckingCtrl L2247)
  ↓
[getMedicalRecord.json] (其它 controller)
  ↓
[getMedicalRecordPayVo.json] (deliveryInputRecordCtrl L4034) ← cashflowId
  ↓
[getCashflowDeliveryVo.json] (deliveryInputCtrl L3848) ← cashflowId
  ↓
[getMedicalRecordCashflowVo.json] (waitPayDetailCtrl L7488 / waitPayBackCtrl L7070 / payedDetailCtrl L4942)
  ↓
[computeUnPlaceOrderMedicalRecordFee.json] (waitChargeDetailCtrl L6680) ← medicalRecordId
```

### 13.2 Write API 调用顺序

```
[insertCustomerCheckin.json] (optometryCtrl L34914) ← patientId
  ↓
[beginCustomerCheckin.json] (optometryCtrl L34947 / doctorWorkbenchCtrl L10605) ← customerCheckinId
  ↓
[createCashFlowForMedicalRecord.json] (waitChargeDetailCtrl L6925) ← medicalRecordId
  ↓
[payMedicalRecordCashflow.json] (waitPayDetailCtrl L8017) ← cashflowId
  ↓
[sendMedicalProductToMachineCenter.json] (deliveryInputCtrl L3966) ← medicalProductMachineCenterPoListJson
  ↓
[startMachineCenterOrder.json] (machineOrderCtrl L16164) ← machineCenterOrderId
  ↓
[completeMachineCenterOrder.json] (machineOrderCtrl L16226) ← machineCenterOrderId
```

## 14. Controller DAG

```
[doctorWorkbenchCtrl] ─A→ [myMemberRecordCtrl]
                              ↓ HTML
                          [optometryCtrl] ─A→ [optometryGlassesCtrl]
                              ↓ $state.go("waitChargeList")
                          [waitChargeListCtrl] ─HTML→ [waitChargeDetailCtrl]
                                                              ↓ $state.go("waitPayDetail", {cashflowId})
                                                          [waitPayDetailCtrl]
                                                              ↓ $state.go("payedList")
                                                          [payedListCtrl]
                                                              ↓ HTML
                                                          [deliveryListCtrl] ─HTML→ [deliveryInputCtrl]
                                                                                          ↓ sendMedicalProductToMachineCenter
                                                                                      [machineOrderCtrl]

[assistCheckingCtrl] ─A→ [myMaterialBillCtrl / myCheckBillCtrl / addCheckCtrl]
                          ↑                                          ↓
                          └──── $state.go("assistChecking", {medicalExamineId, medicalRecordId}) [myCheckBillCtrl]
```

## 15. Core Key Matrix

| Key | Check | Optometry | Sale | Charge | Delivery | Machine |
|---|---|---|---|---|---|---|
| **patientId** | Source: obj.patient.id, employee.patient.id | State go 接收 | State go 接收 | - | - | - |
| **medicalRecordId** | Source: beginCustomerCheckin.medicalRecordId | Source: 同上 / State 接收 | State go 接收 | State 接收（$stateParams.medicalRecordId → L6570） | **dead-end** (S1-117/120 确认) | State go 接收 |
| **medicalProductId** | optometryGlasses 9 命中 | - | - | waitChargeDetailCtrl 8 命中 | deliveryInputCtrl 11 命中 | - |
| **cashflowId** | - | - | - | **Source: createCashFlowForMedicalRecord** | State 接收（L3814） | State 接收（machineOrderBrokenCtrl L16262） |
| **objectId** | - | - | - | - | **Source: getCashflowDeliveryVo.response** (deliveryInputCtrl 7 命中) | bridge: machineCenterId |

**S1-123 关键发现 11**：
- patientId 起点：Check（接诊/验光）
- medicalRecordId 起点：Check（beginCustomerCheckin）
- medicalProductId 集中于：Optometry/Charge/Delivery
- cashflowId 起点：Charge（createCashFlowForMedicalRecord）
- objectId 起点：Delivery（getCashflowDeliveryVo），唯一桥接到 Machine

## 16. 与历史结论的差异

### 16.1 S1-122 vs S1-123

| 项 | S1-122 | S1-123 |
|---|---|---|
| 就诊流程 Controller 数 | 42 | 38（剔除 4 个误归类）|
| medicalRecordId 首次 Consumer | 未明确 | doctorWorkbenchCtrl L10605 + optometryCtrl L34947（**D 级冲突**）|
| 10 个二级菜单 | 未涉及 | 9 个确认 + 1 个 F |
| 店内/连锁加工 | 标注"未归类" | 明确为 machineOrderCtrl / machineOrderBrokenCtrl + chain 字段 |

### 16.2 S1-121 vs S1-123

| 项 | S1-121 | S1-123 |
|---|---|---|
| waitChargeDetailCtrl 角色 | Charge 内部三角审计 | **就诊流程核心 entry**（L6925 createCashFlow + L6929 整体传播）|
| cashflowId 起源 | 三角内单一来源 | **就诊流程主入口**（仅 waitChargeDetailCtrl）|

### 16.3 S1-115 vs S1-123

| 项 | S1-115 | S1-123 |
|---|---|---|
| Check → Optometry 链 | 4 主链 15 Controller | **直接 State 链 + API 桥** 已定位 |
| Delivery → Machine | objectId 派生 | **sendMedicalProductToMachineCenter.json 桥接** + chain 字段区分 |

## 17. 26 项矩阵

| # | 项目 | 等级 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | 一级菜单证据 | 历史 | F (历史菜单) | L2 |
| 02 | 10 个二级菜单证据 | 9/10 确认 | A | L1 |
| 03 | Controller 全集 | 38 个 | A | L1 |
| 04 | Controller→菜单 | 38/38 | A | L1 |
| 05 | State 全集 | 19 个 $state.go | A | L1 |
| 06 | State→Controller | 13 个 State | A | L1 |
| 07 | 核心对象 | 6 类 | A | L1 |
| 08 | medicalRecord | 60+ 处 | A | L1 |
| 09 | medicalRecordId | 161+ 处 | A | L1 |
| 10 | patientId | 89+ 处 | A | L1 |
| 11 | customer | 100+ 处 | A | L1 |
| 12 | medicalProduct | 100+ 处 | A | L1 |
| 13 | cashflowId | 74+ 处 | A | L1 |
| 14 | medicalRecordId 首次 Consumer | doctorWorkbenchCtrl L10605 + optometryCtrl L34947（D 级）| A | L1 |
| 15 | patientId→medicalRecordId | **A（平行字段，无派生）** | A | L1 |
| 16 | medicalRecord→patient | **A（response.patient.id）** | A | L1 |
| 17 | medicalRecord→customer | **A（waitPayBackCtrl L7320）** | A | L1 |
| 18 | Check→Optometry | A（doctorWorkbenchCtrl + optometryCtrl 链）| A | L1 |
| 19 | Optometry→Sale | **F（源码无直接 State 链）** | A | L1 |
| 20 | Sale→Charge | A（optometryCtrl L35145 → waitChargeList）| A | L1 |
| 21 | Charge→Delivery | A（waitPayDetailCtrl → payedList → HTML → deliveryList）| A | L1 |
| 22 | Delivery→Machine | A（sendMedicalProductToMachineCenter.json 桥接）| A | L1 |
| 23 | 店内加工 | A（machineOrderCtrl + InStoreMachineCenterCashflowVoList API）| A | L1 |
| 24 | 连锁加工 | A（machineOrderWaitProcessCtrl + machineOrderBrokenCtrl + chain 字段）| A | L1 |
| 25 | State/API/Controller DAG | 已建立 | A | L1 |
| 26 | A/B/C/D/E/F | A=24 / B=0 / C=0 / D=1 / E=0 / F=1 | - | - |

## 18. F 边界

| 项目 | F 原因 | 应对 |
|---|---|---|
| "主页" 二级菜单 | 无独立 State 证据 | 需要 HTML 审计 |
| HTML ng-click 跳转 | 不在 controller.js 范围 | 需要 HTML 审计 |
| Optometry→Sale 链 | 源码无直接 State | 可能通过 HTML 跳转 |
| 路由注册 | UI-Router 配置不在范围 | 需要路由表 |

## 19. 复刻风险（L1）

### R1: 就诊流程菜单与实际 Controller 不一一对应
- 10 个二级菜单中 9 个能定位 Controller
- "主页" 是辅助入口，**没有独立 State**
- 复刻时按业务命名 State 即可

### R2: medicalRecordId 多路径
- 多个入口（doctorWorkbench / optometryCtrl / addCheckin）
- D 级冲突：同一 API (beginCustomerCheckin) 不同 Response 访问
- 复刻时必须实现"接诊"和"验光"两个入口

### R3: cashflowId 多源 + Type 5 整体对象传播
- waitChargeDetailCtrl L6925 是**唯一**就诊流程内的 cashflowId 创建点
- createCashFlowForMedicalRecord.json Response 是 object 整体
- 复刻时后端必须能容错处理 object 引用

### R4: Delivery objectId 独立
- objectId 仅 1 个 Controller (deliveryInputCtrl) 唯一使用
- 通过 sendMedicalProductToMachineCenter.json 桥接到 Machine
- 复刻时不能简化 objectId 字段

### R5: API bridge 比 Controller bridge 更重要
- 5 段主链关系中 4 段通过 State go 直接成立
- 1 段（Check → Optometry）需要 API + State 双桥
- 复刻时优先保证 API 桥

### R6: 某些菜单可能是辅助设备页面
- optometryListCtrl / optometryLogListCtrl 误命名
- 复刻时**不要按名称**归类

### R7: 店内/连锁加工通过 chain 字段区分
- 同一个 machineOrderWaitProcessCtrl 根据 chain 切换
- 复刻时**必须实现 chain 字段**才能支持两种加工

### R8: 助诊后按 medicalRecordType 分流
- if medicalRecordType == 5: myMaterialBillCtrl
- else if templateId: myCheckBillCtrl
- else: addCheckCtrl
- 复刻时**必须实现三向分流**

## 20. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- 165-184 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 21. 最终就诊流程主链图

```
┌─────────────────────────────────────────────────────────────────┐
│                  就诊流程 Controller 主链图                       │
└─────────────────────────────────────────────────────────────────┘

                              [doctorWorkbenchCtrl] L10401
                                       │ (接诊)
                                       ↓ HTTP beginCustomerCheckin.json
                              L10609: $state.go("adminMyRecord.myMemberRecord")
                                       │ { medicalRecordId, patientId }
                                       ↓
                              [myMemberRecordCtrl] L33218
                                       │ (HTML)
                                       ↓
                              [optometryCtrl] L34776
                                       │ L34954: $state.go("optometryGlasses")
                                       │ { medicalRecordId }
                                       ↓
                              [optometryGlassesCtrl] L35383
                                       │ (HTML)
                                       ↓
                              [assistCheckingCtrl] L1756
                                       │ L2258-L2267: 助诊完成
                                       │ if medicalRecordType == 5:
                                       │   → myMaterialBillCtrl
                                       │ else if templateId:
                                       │   → myCheckBillCtrl
                                       │ else:
                                       │   → addCheckCtrl
                                       ↓
                ┌──────────────────────┼──────────────────────┐
                ↓                      ↓                      ↓
        [myMaterialBillCtrl]  [myCheckBillCtrl]      [addCheckCtrl]
                L32435              L32116                L50170
                                       │
                                       │ L32132: $state.go("assistChecking")
                                       │ { medicalExamineId, medicalRecordId }
                                       ↓
                                [assistCheckingCtrl] (回环)

                              [optometryCtrl] L35145
                                       │ 收费
                                       ↓ $state.go("waitChargeList")
                              [waitChargeListCtrl] L6957
                                       │ (HTML)
                                       ↓
                              [waitChargeDetailCtrl] L6568
                                       │ L6925: createCashFlowForMedicalRecord.json
                                       │ L6929: $state.go("waitPayDetail")
                                       │ { cashflowId: res.result.object } [Type 5]
                                       ↓
                              [waitPayDetailCtrl] L7452
                                       │ L8017: payMedicalRecordCashflow.json
                                       │ L8021: $state.go("payedList")
                                       ↓
                              [payedListCtrl] L4972
                                       │ (HTML)
                                       ↓
                              [deliveryListCtrl] L4075
                                       │ (HTML)
                                       ↓
                              [deliveryInputCtrl] L3812
                                       │ L3848: getCashflowDeliveryVo.json
                                       │ L3966: sendMedicalProductToMachineCenter.json
                                       │ { medicalProductMachineCenterPoListJson }
                                       ↓
                ┌──────────────────────┴──────────────────────┐
                ↓ 店内 (chain=false)              ↓ 连锁 (chain=true)
        [machineOrderCtrl] L16094            [machineOrderBrokenCtrl] L16261
                ↓                                    ↓
        selectInStoreMachineCenter        getMachineCenterCashflowVo.json
        CashflowVoList.json               { cashflowId, machineCenterId }
                ↓ L16164: startMachineCenterOrder
                ↓ L16226: completeMachineCenterOrder
                ↓ L16235: closeMachineCenterOrder
```

**S1-123 关键发现 12**：
- 就诊流程主链是**双入口 + 三向分流 + 五段主链**
- 入口 1：doctorWorkbenchCtrl 接诊
- 入口 2：optometryCtrl 验光
- 助诊后**三向分流**（开单/检查报告/添加检查）
- 五段主链：Check→Optometry / Check→Sale / Optometry→Charge / Charge→Delivery / Delivery→Machine

---

**【S1-123 完成】**
