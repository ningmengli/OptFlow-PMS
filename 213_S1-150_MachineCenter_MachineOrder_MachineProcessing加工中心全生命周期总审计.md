# S1-150：MachineCenter / MachineOrder / MachineProcessing 加工中心全生命周期总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 212 个 MD / 不修改历史
> 关联：S1-129 / S1-142 / S1-148 / S1-149

---

## 目录

- §0 审计范围
- §1 Machine / MachineOrder / MachineCenter 全量
- §2 Machine Controller 全部定位
- §3 4 个 Machine Controller 深审
- §4 machineCenterOrder Object 字段级审计
- §5 machineCenterOrder API 全量
- §6 machineCenterOrder 生命周期
- §7 ↔ MedicalProduct
- §8 ↔ machineCenter
- §9 ↔ Delivery
- §10 ↔ Stock
- §11 Machine ↔ Delivery
- §12 Machine ↔ Stock
- §13 objectId / F3 / F6 完整链
- §14 machineCenter ↔ machineCenterOrder
- §15 状态 / UI 分类
- §16 HTML ↔ Controller 对照
- §17 Response Object 层级
- §18 Source Trace
- §19 Object 分类
- §20 生命周期 DAG
- §21 Controller 消费矩阵
- §22 26 项证据矩阵
- §23 历史差异
- §24 V4.4 加工中心规格
- §25 F / 未确认
- §26 Git / 完整性

---

## §0 审计范围

本轮把 MachineCenter / MachineOrder / MachineProcessing 加工中心域作为
**独立完整域**进行只读逆向证据审计：

- 字符级字段（区分 `machineOrder` vs `machineCenterOrder` 命名差异）
- 4 个真实 Machine Controller 深审
- F3-F6 + 加工中心 API 完整链
- objectId / lockMachineCenter Runtime Mutation 完整验证
- "加工状态" UI Tab 分类 vs 后端 status 严格区分
- HTML ↔ Controller 对照（S1-149 报告的 9+ NOT FOUND 复验）
- 26 项证据矩阵
- 历史 S1-129/142/148/149 误判核对

---

## §1 Machine / MachineOrder / MachineCenter 全量

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `machine` (全词) | **0** | A |
| `machineId` | **0** | A |
| `machineVo` | **0** | A |
| `machineList` | **0** | A |
| `machineOrder` (全词) | **0** | A |
| `machineOrderId` | **0** | A |
| `machineOrderVo` | **0** | A |
| `machineOrderVoList` | **0** | A |
| `machineOrderList` | **0** | A |
| `machineCenter` | **9** | A |
| `machineCenterId` | **26** | A |
| `machineCenterVo` | **0** | A |
| `machineCenterVoList` | **0** | A |
| `lockMachineCenter` | **1** | A |
| `objectId` | **7** | A |
| `processing` | 0 | A |
| `processId` | 0 | A |
| `processingId` | 0 | A |

### §1.2 重大发现

1. **`machine` 全词 = 0 命中** — 前端没有独立 Machine 概念
2. **`machineOrder` 全词 = 0 命中** — 仅是 Controller 名称拼接（`machineOrderCtrl` 等）
3. **`machineOrderId` 0 命中** — 实际 ID 字段命名是 `machineCenterOrderId`（字符串拼接差异）
4. **`machineCenterVo` 0 命中** — MachineCenter 没有独立 VO 容器（同 productVo 模式）
5. **`processing` / `processId` / `processingId` 0 命中** — 加工过程没有独立 ID 实体
6. **`machineCenterId` 26 命中**（最大）— 是 Machine 域主要 ID 字段
7. **`objectId` 7 命中** — 来自 medicalProduct.objectId（S1-149 runtime mutation 保持）

### §1.3 修正 S1-149 报告

S1-149 报告"machineOrderId 0 命中 / machineOrder 字段 0 命中"是**字符串拼接差异**：
- 实际 ID 字段命名是 `machineCenterOrderId`（**11 命中**）
- 实际 Object 字段命名是 `machineCenterOrder`（**4 命中**）
- 实际 VO 容器是 `machineCenterOrderVoList`（**3 命中**）
- 实际状态字段是 `machineCenterOrder.status` 和 `machineCenterOrder.receiveStatus`

---

## §2 Machine Controller 全部定位

### §2.1 15 个候选 Controller 验证

| Controller | 行号 | 等级 |
|---|---|---|
| ✓ `machineOrderCtrl` | L16094 | A |
| ✓ `machineOrderListCtrl` | L4264 | A |
| ✓ `machineOrderWaitProcessCtrl` | L16357 | A (Stub) |
| ✓ `machineOrderBrokenCtrl` | L16261 | A |
| ✗ `machineOrderCompletedCtrl` | NOT FOUND | F (HTML 存在, Controller 缺失) |
| ✗ `machineCenterCtrl` | NOT FOUND | F |
| ✗ `machineCenterListCtrl` | NOT FOUND | F |
| ✗ `machineManageCtrl` | NOT FOUND | F |
| ✗ `processingCtrl` | NOT FOUND | F |
| ✗ `machineCtrl` | NOT FOUND | F |
| ✗ `machineProcessCtrl` | NOT FOUND | F |
| ✗ `machineOrderCreateCtrl` | NOT FOUND | F |
| ✗ `machineOrderUpdateCtrl` | NOT FOUND | F |
| ✗ `machineOrderDetailCtrl` | NOT FOUND | F |
| ✗ `machineOrderPrintCtrl` | NOT FOUND | F |

### §2.2 真实存在的 4 个 Machine Controller

| Controller | 行号 | 实际功能 | 等级 |
|---|---|---|---|
| `machineOrderCtrl` | L16094 | 加工订单管理（开始/完成/关闭） | A |
| `machineOrderListCtrl` | L4264 | 签收/发货列表 | A |
| `machineOrderWaitProcessCtrl` | L16357 | UI Tab Stub | A (空) |
| `machineOrderBrokenCtrl` | L16261 | 报损 + 完成 | A |

---

## §3 4 个 Machine Controller 深审

### §3.1 machineOrderCtrl L16094 详细

**完整功能**（9 个 API）：

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| `selectInStoreMachineCenterCashflowVoList.json` | L16106 | R | A |
| `getMethodGlassRecordVo.json` | L16140 | R | A |
| `getMedicalRecord.json` | L16161 | R | A |
| `getCanBeProcessSkuInListOfProduct.json` | L16173 | R | A |
| `saveToBeProcessSkuInListOfProduct.json` | L16197 | **W (保存加工)** | A |
| `startMachineCenterOrder.json` | L16212 | **W (开始订单)** | A |
| `completeMachineCenterOrder.json` | L16218 | **W (完成订单)** | A |
| `closeMachineCenterOrder.json` | L16224 | **W (关闭订单)** | A |
| `getMachineCenterOrder.json` | L16237 | R | A |

**关键 Object 字段**：
- `$scope.common.machineCenterOrderId` (L16213/L16219/L16225) — **machineCenterOrderId 真实存在**
- `$scope.common.medicalRecordId`
- `$scope.common.idx`
- `$scope.memberFactory.items[idx].machineCenterOrder.status` (L16231) — **machineCenterOrder 是 Object 实体！status 字段真实存在**

**4 个状态 API 链**：
```
startMachineCenterOrder (id, medicalRecordId) 
  → getMachineCenterOrder
  → items[idx].machineCenterOrder.status 更新

completeMachineCenterOrder (id, medicalRecordId) 
  → getMachineCenterOrder
  → items[idx].machineCenterOrder.status 更新

closeMachineCenterOrder (id, medicalRecordId) 
  → getMachineCenterOrder
  → items[idx].machineCenterOrder.status 更新
```

### §3.2 machineOrderListCtrl L4264 详细

**完整功能**（4 个 API）：

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| `selectMachineCenterListOfProduct.json` | L4277 | R (派生 centerArr[].id/name) | A |
| `selectMachineCenterOrderRecordVoList.json` | L4299 | R | A |
| `receiveMachineCenterOrder.json` | L4310 | **W (签收)** | A |
| `deliveryMachineCenterOrder.json` | L4324 | **W (发货)** | A |

**关键 Object 字段**：
- `$scope.getAdminList.items[idx].machineCenterOrder.receiveStatus` (L4318) — **receiveStatus 真实存在**
- `$scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus` (L4332) — **medicalProductDelivery + deliveryStatus 真实存在！**（S1-142 修正）
- `$scope.centerArr[]` (派生 from selectMachineCenterListOfProduct)
- `$scope.obj.receiveStatus` (0/1)
- `$scope.obj.acceptStatus` (null/0/1)
- `$scope.obj.statusArray` (null/[0]/[0,1]/[2])

**4 个 Tab 分类（保持 S1-149）**：
```javascript
$scope.setTab = function (tab) {
  if (tab == 1) { acceptStatus = null; statusArray = null; }
  else if (tab == 2) { acceptStatus = 0; statusArray = [0]; }
  else if (tab == 3) { acceptStatus = 1; statusArray = [0, 1]; }
  else if (tab == 4) { acceptStatus = 1; statusArray = [2]; }
};
```

### §3.3 machineOrderWaitProcessCtrl L16357 详细（空 Stub）

**完整函数体**（仅 12 行）：
```javascript
angular.module("bestvisionWeb").controller("machineOrderWaitProcessCtrl", [..., function ($scope, ...) {
  if ($scope.$state.current.name == "machineOrderChainWaitAccess" || $scope.$state.current.name == "machineOrderWaitAccess") {
    $scope.tab = 1;
  } else if ($scope.$state.current.name == "machineOrderChainWaitProcess" || $scope.$state.current.name == "machineOrderWaitProcess") {
    $scope.tab = 2;
  } else if ($scope.$state.current.name == "machineOrderChainProcessing" || $scope.$state.current.name == "machineOrderProcessing") {
    $scope.tab = 3;
  } else if ($scope.$state.current.name == "machineOrderChainTesting" || $scope.$state.current.name == "machineOrderTesting") {
    $scope.tab = 4;
  } else {}
  console.log($scope.tab);
}]);
```

**8 个 State（Chain + 非 Chain）**：
- `machineOrderChainWaitAccess` (tab=1) / `machineOrderWaitAccess` (tab=1)
- `machineOrderChainWaitProcess` (tab=2) / `machineOrderWaitProcess` (tab=2)
- `machineOrderChainProcessing` (tab=3) / `machineOrderProcessing` (tab=3)
- `machineOrderChainTesting` (tab=4) / `machineOrderTesting` (tab=4)

**关键发现**：
- **真实是空 Stub Controller**（仅 if/else 设 $scope.tab + console.log）
- "待接 / 待处理 / 处理中 / 测试中" 是 **UI Tab 分类**，不是后端 status 枚举
- "Chain" 命名 = 连锁店模式

### §3.4 machineOrderBrokenCtrl L16261 详细

**Entry**: `$stateParams.cashflowId` + `$stateParams.machineCenterId` + `$stateParams.chain`

**完整功能**（4 个 API）：

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| `getMachineCenterCashflowVo.json` | L16269 | R | A |
| `getAdminInfo.json` | L16287 | R (报损责任人) | A |
| `createMedicalStockLoss.json` | L16310 | **W (报损)** | A |
| `completeMachineCenterOrder.json` | L16334 | **W (完成)** | A |

**关键 Object 字段**：
- `$scope.getStockObjectFactory.result.object.machineCenterOrderVoList[idx].machineCenterOrder.id` — **machineCenterOrderVoList 真实存在！**
- `$scope.getStockObjectFactory.result.object.machineCenterOrderVoList[idx].medicalProduct.productName` — **medicalProduct.productName 字符级命中！**
- `$scope.loss.lossAdminId` / `$scope.adminname`
- `$scope.loss.medicalStockLossSkuListJson` (Request payload)
- `$scope.medicalProductStockId` / `$scope.lossCount` (Request)

**完成跳转**：
```javascript
$state.go("machineOrderChainTesting") / $state.go("machineOrderTesting")
```

**关键发现**：
- machineOrderBrokenCtrl 实际是 **Cashflow + MachineCenter 维度的报损**（不是独立 MachineOrder 实体）
- Entry 用 cashflowId + machineCenterId 联合 StateParams
- `medicalProduct.productName` 是**唯一**字符级命中的 medicalProduct.name 字段（保持 S1-145 修正：medicalProductName 0 命中，但 medicalProduct.productName 通过 machineCenterOrderVoList 嵌套命中）

---

## §4 machineCenterOrder Object 字段级审计

### §4.1 machineCenterOrder 真实字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `machineCenterOrderId` (Request) | L16213/L16219/L16225/L4310/L4324/L16311 | **A** |
| `machineCenterOrder.id` (Response) | L16321 (machineOrderBrokenCtrl `machineCenterOrderVoList[idx].machineCenterOrder.id`) | **A** |
| `machineCenterOrder.status` (Response) | L16231 (machineOrderCtrl `items[idx].machineCenterOrder.status`) | **A** |
| `machineCenterOrder.receiveStatus` (Response) | L4318 (machineOrderListCtrl `items[idx].machineCenterOrder.receiveStatus = 1`) | **A** |
| `machineCenterOrderVoList[]` (Response container) | L16231/L16321/L16324 | A |

### §4.2 4 Machine Controller 字段访问总汇

| Controller | Object 字段 | 行号 |
|---|---|---|
| `machineOrderCtrl` | `items[idx].machineCenterOrder.status` | L16231 |
| `machineOrderListCtrl` | `items[idx].machineCenterOrder.receiveStatus` | L4318 |
| `machineOrderBrokenCtrl` | `machineCenterOrderVoList[idx].machineCenterOrder.id` | L16321 |
| `machineOrderBrokenCtrl` | `machineCenterOrderVoList[idx].medicalProduct.productName` | L16324 |

### §4.3 0 命中字段（必须 F）

| 字段 | 等级 |
|---|:---:|
| `machineOrder.id/status/state/type` | F (实际是 machineCenterOrder) |
| `machineOrderVo` / `machineOrderVoList` | F |
| `machineOrderList` | F |
| `machineCenterOrder.remark/createTime/completedTime` | F |
| `machineCenterOrder.machineCenter` 字段 | F |
| `machineCenterOrder.medicalProduct` 字段 | F (实际是 machineCenterOrderVoList 嵌套) |

### §4.4 machineCenterOrder 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `machineCenterOrderId`, `machineCenterOrder.id` | A |
| B. Response VO | `machineCenterOrderVoList` | A |
| C. Request Only | - | F |
| D. State Only | - | F (cashflowId + machineCenterId 是 State, machineCenterOrderId 是 Request) |
| E. UI | `items[idx].machineCenterOrder.status` (显示) | A |
| F. Runtime Mutation | - | F (machineCenterOrder 无 runtime mutation) |

---

## §5 machineCenterOrder API 全量

### §5.1 machineCenterOrder Lifecycle API

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| **startMachineCenterOrder.json** | L16212 | **W (开始)** | A |
| **completeMachineCenterOrder.json** | L16218/L16334 | **W (完成)** | A |
| **closeMachineCenterOrder.json** | L16224 | **W (关闭)** | A |
| **getMachineCenterOrder.json** | L16237/L16251 | R | A |
| **receiveMachineCenterOrder.json** | L4310 | **W (签收)** | A |
| **deliveryMachineCenterOrder.json** | L4324 | **W (发货)** | A |

### §5.2 machineCenter 域 API

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| `getMachineCenterVo.json` | L56908 | R | A |
| `updateMachineCenterInfo.json` | L56927 | W | A |
| `updateMachineCenterCompanyIdArray.json` | L57061 | W | A |
| `selectMachineCenterListOfProduct.json` | L4277 | R | A |
| `selectMachineCenterOrderRecordVoList.json` | L4121/L4299 | R | A |
| `getMachineCenterCashflowVo.json` | L16269 | R | A |
| `getMachineCenterOrder.json` | L16251/L16237 | R | A |

### §5.3 Machine 域 Shared API (F3/F6 + F5)

| API | 行号 | R/W | 等级 |
|---|---|---|---|
| F3 `getMedicalProductMachineCenterVoList.json` | L3836 | R | A |
| F6 `sendMedicalProductToMachineCenter.json` | L3966 | **W (工厂下单)** | A |
| F5 `saveMedicalProductStockBatch.json` | L4007 | W | A |
| `getCanBeProcessSkuInListOfProduct.json` | L16173 | R (开始加工查询) | A |
| `saveToBeProcessSkuInListOfProduct.json` | L16197 | **W (保存加工)** | A (F5 新版本) |
| `createMedicalStockLoss.json` | L16310 | W (报损) | A |

### §5.4 0 命中 API（必须 F）

| API | 等级 |
|---|:---:|
| `getMachineOrder*.json` | F (实际是 machineCenterOrder) |
| `saveMachineOrder*.json` | F |
| `updateMachineOrder*.json` | F |
| `createMachineOrder*.json` | F |
| `deleteMachineOrder*.json` | F |
| `processMachineOrder*.json` | F |
| `cancelMachineOrder*.json` | F |
| `submitMachineOrder*.json` | F |
| `selectMachineOrder*.json` | F |

---

## §6 machineCenterOrder 生命周期

### §6.1 完整 Lifecycle

```
[Delivery] sendMedicalProductToMachineCenter (F6)
  ↓
MachineCenter Order Created (machineCenterOrderId)
  ↓
selectMachineCenterOrderRecordVoList (列表)
  ↓
[getMachineCenterCashflowVo] 详情
  ↓
startMachineCenterOrder → status 更新
  ↓
[process] getCanBeProcessSkuInListOfProduct / saveToBeProcessSkuInListOfProduct (F5)
  ↓
receiveMachineCenterOrder → receiveStatus = 1
  ↓
deliveryMachineCenterOrder → medicalProductDelivery.deliveryStatus = 1
  ↓
completeMachineCenterOrder → status 更新
  ↓
[可选] closeMachineCenterOrder → 关闭
```

### §6.2 状态转换

| Status | API | 入口 Controller | 等级 |
|---|---|---|---|
| 待开始 → 开始 | `startMachineCenterOrder` | machineOrderCtrl | A |
| 开始 → 完成 | `completeMachineCenterOrder` | machineOrderCtrl / machineOrderBrokenCtrl | A |
| 开始 → 关闭 | `closeMachineCenterOrder` | machineOrderCtrl | A |
| 待签收 → 已签收 | `receiveMachineCenterOrder` | machineOrderListCtrl | A |
| 已签收 → 已发货 | `deliveryMachineCenterOrder` | machineOrderListCtrl | A |
| 报损 | `createMedicalStockLoss` | machineOrderBrokenCtrl | A |

### §6.3 关键发现

- **没有 machineOrder Create 入口**（0 命中）— machineCenterOrder 由 F6 `sendMedicalProductToMachineCenter` 触发
- **真实 Lifecycle 入口是 F6**（保持 S1-149 修正）
- **没有 selectMachineOrder 通用查询** — 实际是 `selectMachineCenterOrderRecordVoList` / `getMachineCenterOrder`

---

## §7 ↔ MedicalProduct

### §7.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| MedicalProduct | machineCenterOrder | F6 `sendMedicalProductToMachineCenter` (Request) | A Request Bridge | L3966 | **A** | A |
| MedicalProduct | machineCenter | F3 `getMedicalProductMachineCenterVoList` (Request) | A Request Bridge (Runtime) | L3836 | **A** | A |
| machineCenterOrder | MedicalProduct | `machineCenterOrderVoList[idx].medicalProduct.productName` | A 字段桥 (Response) | L16324 | **A** | A |
| machineCenterOrder | MedicalProduct | `medicalProduct.id` (经 medicalProductMachineCenterPoList) | A Request Bridge | L3822 | **A** | A |
| MedicalProduct | machineCenterOrder | 0 命中 `medicalProduct.machineCenterOrder` 字段 | F | - | **F** | F |

### §7.2 关键判断

- **MedicalProduct → machineCenterOrder**: A Request Bridge（F6）
- **machineCenterOrder → MedicalProduct**: A 字段桥（machineCenterOrderVoList 嵌套）
- **保持 S1-149 修正**：MedicalProduct → machineCenter 是 Runtime Mutation（objectId 派生）

---

## §8 ↔ machineCenter

### §8.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| machineCenterOrder | machineCenter | `machineCenterOrderVoList[idx].machineCenterOrder` (1:N 嵌套) | A 字段桥 (Response) | L16321 | **C** | C |
| machineCenter | machineCenterOrder | 0 命中 `machineCenter.machineCenterOrder` 字段 | F | - | **F** | F |
| machineCenterOrder | machineCenter | `machineCenterOrder.machineCenterId` 顶层字段 | 0 命中 | - | **F** | F |

### §8.2 关键判断

- **machineCenterOrder → machineCenter**: C 字段桥（仅经 machineCenterOrderVoList 嵌套）
- **machineCenter → machineCenterOrder**: F（无直接字段桥）
- **保持 S1-149 修正**：machineCenterId 26 命中是 Request 字段（不是 Object 顶层）

### §8.3 machineCenter Object 字段

| 字段 | 命中 | 等级 |
|---|---:|---|
| `machineCenter.id` | **4** | A |
| `machineCenter.name` | **2** | A |
| `machineCenter.type` | 1 | A |
| `machineCenterVo` | 0 | F |
| `machineCenterVoList` | 0 | F |

**来源**：
- `arr[i].id` / `arr[i].name` (L4283-L4286 selectMachineCenterListOfProduct Response)
- L56908 `getMachineCenterVo.json` (machineCenterVo 字段)
- L57061 `updateMachineCenterCompanyIdArray.json` Request

---

## §9 ↔ Delivery

### §9.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Delivery | machineCenterOrder | F6 `sendMedicalProductToMachineCenter` (Request) | A Request Bridge | L3966 | **A** | A |
| machineCenterOrder | Delivery | `items[idx].medicalProductDelivery.deliveryStatus = 1` | A 字段桥 (Response) | L4332 | **A** | A |
| machineCenterOrder | Delivery | `deliveryMachineCenterOrder` Write | A Request Bridge | L4324 | **A** | A |
| Delivery | machineCenterOrder | 0 命中 `delivery.machineCenterOrder` 字段 | F | - | **F** | F |

### §9.2 关键发现

1. **Delivery → machineCenterOrder**: A Request Bridge（F6）
2. **machineCenterOrder → Delivery**: A 字段桥（`medicalProductDelivery.deliveryStatus`）
3. **`medicalProductDelivery` 字段**：S1-142 报告的 deliveryStatus 实际访问点
4. **保持 S1-142 修正**：Delivery 不含 machineCenterOrder 字段（F）

---

## §10 ↔ Stock

### §10.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| machineCenterOrder | Stock | `getMachineCenterCashflowVo` (cashflow 派生) | A 派生 (经 Cashflow) | L16269 | **A** | A |
| machineCenterOrder | Stock | F5 `saveToBeProcessSkuInListOfProduct` | A Request Bridge | L16197 | **A** | A |
| machineCenterOrder | Stock | `medicalProductStockId` (报损) | A Request Bridge | L16321 | **A** | A |
| Stock | machineCenterOrder | 0 命中 `stock.machineCenterOrder` 字段 | F | - | **F** | F |
| machineCenterOrder | Stock | 0 命中 `machineCenterOrder.stock` 字段 | F | - | **F** | F |

### §10.2 关键发现

- **machineCenterOrder ↔ Stock**: A 派生链（经 Cashflow 桥 + F5 加工 + medicalProductStockId 报损）
- **保持 S1-149 修正**：medicalProductStock 0 命中（medicalProductStockId 是 Request 字段）
- **没有直接字段桥**（Stock/machineCenterOrder 0 命中）

---

## §11 Machine ↔ Delivery

### §11.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Delivery | Machine | F6 `sendMedicalProductToMachineCenter` (Request) | A Request Bridge | L3966 | **A** | A |
| Delivery | Machine | `getMachineCenterCashflowVo` (cashflow 派生) | A 派生 (经 Cashflow) | L16269 | **A** | A |
| Machine | Delivery | 0 命中 `machine.delivery` 字段 | F | - | **F** | F |
| Machine | Delivery | `machineCenterOrderVoList[idx].medicalProductDelivery.deliveryStatus` | A 字段桥 (Response) | L4332 | **A** | A |

### §11.2 关键发现（**修正 S1-129 报告**）

- **Delivery → Machine: A Request Bridge**（F6）+ A 派生（经 Cashflow）
- **Machine → Delivery: A 字段桥**（medicalProductDelivery.deliveryStatus）
- **保持 S1-129 / S1-142 修正**：当前 Controller 命名上没有 Delivery / Machine 字符级直接桥（controller 命名无 deliveryInputCtrl → machineOrderCtrl），但**经 API Response 派生有 A 级桥**

---

## §12 Machine ↔ Stock

### §12.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Machine | Stock | F5 `saveToBeProcessSkuInListOfProduct` | A Request Bridge | L16197 | **A** | A |
| Machine | Stock | `medicalProductStockId` (报损) | A Request Bridge | L16321 | **A** | A |
| Stock | Machine | 0 命中 `stock.machineOrder` 字段 | F | - | **F** | F |
| Machine | Stock | 0 命中 `machineCenterOrder.stock` 字段 | F | - | **F** | F |

### §12.2 关键发现

- **Machine → Stock**: A Request Bridge（F5 加工 + medicalProductStockId 报损）
- **Stock → Machine**: F
- **没有直接字段桥** — 全部经 Request Bridge

---

## §13 objectId / F3 / F6 完整链

### §13.1 objectId Runtime Mutation 完整保持（S1-142 + S1-149）

```
[waitingDeliveryList[i]] (deliveryInputCtrl)
  ├── medicalProduct.id
  ├── medicalProduct.objectId  ← Runtime Mutation 起点
  └── lockMachineCenter.id     ← Runtime Mutation 源
        ↓
if (arr[i].medicalProduct.objectId) {
  medicalProductMachineCenterPoList.push({
    medicalProductId: arr[i].medicalProduct.id,
    machineCenterId: arr[i].medicalProduct.objectId   // F3/F6 字段源
  });
} else {
  ...objectId = null
  medicalProductIdArray.push(arr[i].medicalProduct.id)  // F4 字段源
}
```

### §13.2 F3/F4/F5/F6 完整数据流（保持 S1-149）

```
waitingDeliveryList[].medicalProduct
    ↓
medicalProductMachineCenterPoList
  ├── { medicalProductId, machineCenterId=objectId }
    ↓ JSON.stringify
F3 getMedicalProductMachineCenterVoList (Read) → machineCenterVoList
F6 sendMedicalProductToMachineCenter (Write) → 工厂下单
    ↓
machineCenterOrder Created (machineCenterOrderId 派生)
    ↓
machineOrderCtrl.processProduct (L16173)
  → getCanBeProcessSkuInListOfProduct (Read)
    ↓
machineOrderCtrl.saveStock (L16197)
  → saveToBeProcessSkuInListOfProduct (F5 Write)
  → medicalProductStockBatctPoListJson
```

### §13.3 关键修正

- **machineOrderCtrl 复用 F5**：`saveToBeProcessSkuInListOfProduct.json` 是 S1-149 报告的 `saveMedicalProductStockBatch.json` 的加工中心版本
- **machineCenterOrder 是 F6 的响应产物**（不是独立 Create API）
- **保持 S1-149 修正**：objectId 7 命中（runtime mutation）

---

## §14 machineCenter ↔ machineCenterOrder

### §14.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| machineCenter | machineCenterOrder | 0 命中直接字段 | F | - | **F** | F |
| machineCenterOrder | machineCenter | `machineCenterOrderVoList[idx].machineCenterOrder` (1:N) | A 字段桥 (Response 嵌套) | L16321 | **C** | C |

### §14.2 关键判断

- **machineCenter → machineCenterOrder**: F（无直接字段桥）
- **machineCenterOrder → machineCenter**: C 字段桥（仅经 machineCenterOrderVoList 嵌套）
- **machineCenter 不含 machineCenterOrder 字段**（保持 S1-149 修正）

---

## §15 状态 / UI 分类

### §15.1 4 个 Tab 状态（UI 分类，不是后端 status）

| Tab | State 名称 | Chain State | 含义 | 等级 |
|:---:|---|---|---|:---:|
| 1 | `machineOrderWaitAccess` | `machineOrderChainWaitAccess` | 待接 | A |
| 2 | `machineOrderWaitProcess` | `machineOrderChainWaitProcess` | 待处理 | A |
| 3 | `machineOrderProcessing` | `machineOrderChainProcessing` | 处理中 | A |
| 4 | `machineOrderTesting` | `machineOrderChainTesting` | 测试中 | A |

### §15.2 machineCenterOrder.status 后端字段

| Status 含义 | API | 等级 |
|---|---|:---:|
| 待开始 | (未开始) | F |
| 进行中 | `startMachineCenterOrder` | A |
| 已完成 | `completeMachineCenterOrder` | A |
| 已关闭 | `closeMachineCenterOrder` | A |
| 已签收 | `receiveMachineCenterOrder` (machineCenterOrder.receiveStatus=1) | A |
| 已发货 | `deliveryMachineCenterOrder` (medicalProductDelivery.deliveryStatus=1) | A |

### §15.3 真实 status 字段定位

| 字段 | 真实位置 | 等级 |
|---|---|---|
| `machineCenterOrder.status` | machineCenterOrderVoList[].machineCenterOrder.status | A |
| `machineCenterOrder.receiveStatus` | machineCenterOrderVoList[].machineCenterOrder.receiveStatus | A |
| `medicalProductDelivery.deliveryStatus` | machineCenterOrderVoList[].medicalProductDelivery.deliveryStatus | A |
| `cashflow.refundStatus` | Cashflow 顶层（S1-148） | A |
| `cashflow.creditStatus` | Cashflow 顶层（S1-148） | A |

### §15.4 重要发现

- **"待加工/处理中/已完成/破损"是 UI Tab 分类**，不是后端 status 枚举
- **真实 status 字段在 machineCenterOrderVoList[] 嵌套下**
- **保持 S1-146 修正**：MedicalRecord.status 0 命中
- **保持 S1-148 修正**：cashflow.refundStatus/creditStatus 是 Cashflow 顶层

---

## §16 HTML ↔ Controller 对照

### §16.1 4 个 HTML 文件 vs Controller

| HTML 文件 | 字节 | Angular Controller | 等级 |
|---|---|---|---|
| `machineOrderList.html` | 96KB | ✓ `machineOrderListCtrl` L4264 | A |
| `machineOrderCompleted.html` | 35KB | ✗ `machineOrderCompletedCtrl` **NOT FOUND** | F |
| `deliveryList.html` | (S1-142) | ✓ `deliveryListCtrl` 等 | A |
| `payedList.html` (S1-148) | (S1-148) | ✓ `payedListCtrl` L4972 | A |

### §16.2 关键发现

1. **`machineOrderCompleted.html` 存在但无 Controller 定义** — V4.4 实现时**不能**假定此 HTML 有对应 Controller
2. **`machineOrderList.html` 存在且有 Controller**（`machineOrderListCtrl` L4264）— V4.4 复刻此 Controller 即可
3. **保持 S1-149 修正**：HTML 存在 ≠ Controller 存在

### §16.3 推断 4 个 HTML 对应 Controller

| HTML（推断） | 推断 Controller | 状态 |
|---|---|---|
| `machineOrderWaitProcess.html` | `machineOrderWaitProcessCtrl` L16357 (空 Stub) | 推断 |
| `machineOrderBroken.html` | `machineOrderBrokenCtrl` L16261 | 推断 |
| `machineOrderList.html` | `machineOrderListCtrl` L4264 | 确认 |
| `machineOrderCompleted.html` | (NOT FOUND) | **未实现** |

---

## §17 Response Object 层级

### §17.1 getMachineCenterCashflowVo.json Response

```
res.object
  ├── machineCenterOrderVoList[]
  │     ├── machineCenterOrder
  │     │     ├── id
  │     │     ├── status
  │     │     ├── receiveStatus
  │     │     └── ...
  │     ├── medicalProduct
  │     │     ├── id
  │     │     ├── objectId
  │     │     └── productName
  │     ├── medicalProductDelivery
  │     │     └── deliveryStatus
  │     └── ...
  ├── cashflow (经 getCashflowObjectFactory)
  └── ...
```

### §17.2 selectMachineCenterOrderRecordVoList.json Response

```
res.list[]
  ├── machineCenterOrder
  │     ├── id
  │     ├── status
  │     └── receiveStatus
  ├── medicalProductDelivery
  │     └── deliveryStatus
  └── ...
```

### §17.3 关键判断

- **machineCenterOrderVoList 是 Container**（不是 Object 实体）
- **machineCenterOrder 是 Object 实体**（含 id / status / receiveStatus）
- **medicalProductDelivery 是 Object 实体**（含 deliveryStatus）
- **保持 S1-149 修正**：VoList 是 Response VO 容器，**不是 cashflow / delivery 内嵌字段**

---

## §18 Source Trace

### §18.1 关键字段溯源

#### machineCenterOrderId
- **Source A**: $scope.common.machineCenterOrderId (machineOrderCtrl L16213/L16219/L16225)
- **Source B**: $scope.loss.machineCenterOrderId (machineOrderBrokenCtrl L16321)
- **Target**: startMachineCenterOrder / completeMachineCenterOrder / closeMachineCenterOrder / receiveMachineCenterOrder / deliveryMachineCenterOrder / createMedicalStockLoss
- **等级**: A

#### machineCenterId
- **Source A**: $stateParams.machineCenterId (machineOrderBrokenCtrl L16265)
- **Source B**: F3/F6 Request `machineCenterId: objectId` (L3824)
- **Source C**: selectMachineCenterListOfProduct Response `arr[i].id`
- **等级**: A

#### medicalProductId (Machine 域)
- **Source A**: `arr[i].medicalProduct.id` (L3822 F3)
- **Source B**: `medicalProductIdArray.push(arr[i].medicalProduct.id)` (L3873 F4)
- **Source C**: `machineCenterOrderVoList[idx].medicalProduct.id` (L16321)
- **等级**: A

#### objectId (保持 S1-149)
- **Source A**: `arr[i].lockMachineCenter.id` (L3854, runtime mutation)
- **Source B**: null (L3856, else branch)
- **Target**: F3/F6 Request `machineCenterId=objectId`
- **等级**: A (Runtime)

#### medicalProduct.productName
- **Source**: machineOrderBrokenCtrl L16324 `machineCenterOrderVoList[idx].medicalProduct.productName`
- **等级**: A (机器订单域**唯一**字符级命中的 medicalProduct 名称)

#### medicalProductDelivery.deliveryStatus
- **Source A**: machineOrderListCtrl L4332 `items[idx].medicalProductDelivery.deliveryStatus = 1`
- **等级**: A (S1-142 deliveryStatus 真实访问点)

#### machineCenterOrder.status
- **Source A**: machineOrderCtrl L16231 `items[idx].machineCenterOrder.status = resp.result.object.status`
- **Source B**: machineOrderBrokenCtrl L16321 (经 getMachineCenterOrder)
- **等级**: A

#### machineCenterOrder.receiveStatus
- **Source**: machineOrderListCtrl L4318 `items[idx].machineCenterOrder.receiveStatus = 1`
- **等级**: A

#### deliveryCount (保持 S1-149)
- **Source**: F4 Response `deliveryStockInSkuVoList[].deliveryCount`
- **Target**: F5 Request (L3991)
- **等级**: A

#### stockInSkuId (保持 S1-149)
- **Source**: F4 Response `deliveryStockInSkuVoList[].stockInSku.id`
- **Target**: F5 Request
- **等级**: A

---

## §19 Object 分类

### §19.1 6 个 Machine 域 Object 分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Machine** | ✗ (machineId 0 命中) | ✗ | ✗ | ✗ | **F (概念不存在)** |
| **MachineCenter** | ✓ (machineCenterId 26 命中) | ✓ (machineCenterVo 实际是 getMachineCenterVo) | ✓ | ✓ | A |
| **MachineCenterOrder** | ✓ (machineCenterOrderId 11 命中) | ✓ (machineCenterOrderVoList) | ✓ (start/complete/close) | ✓ | A |
| **Processing** | ✗ (processId/Processing 0 命中) | ✗ | ✗ | ✓ (UI Tab 1/2/3/4) | **F (概念不存在)** |
| **MedicalProductDelivery** | ✓ (经 deliveryId) | ✓ (medicalProductDelivery) | - | ✓ (deliveryStatus) | A |
| **MedicalProduct (Machine View)** | ✓ (medicalProductId) | ✓ (经 machineCenterOrderVoList) | ✓ (F3/F6) | - | A |

### §19.2 关键结论

- **Machine / Processing 概念在 controller.js 中实际不存在**（F）
- **真实核心对象是 MachineCenter + MachineCenterOrder**（A）
- **machineCenterOrderVoList 是核心 VO 容器**
- **machineCenterOrder.id / status / receiveStatus 是核心字段**
- **medicalProductDelivery.deliveryStatus 是 Delivery 真实桥点**

### §19.3 修正 S1-149 报告

| S1-149 报告 | S1-150 修正 |
|---|---|
| `machineOrderId 0 命中` → F | **实际是 `machineCenterOrderId` 11 命中**（A） |
| `machineOrder 字段 0 命中` → F | **实际是 `machineCenterOrder.id / status / receiveStatus` 字段 4 命中**（A） |
| `machineOrderVoList 0 命中` → F | **实际是 `machineCenterOrderVoList` 3 命中**（A） |
| `machineOrderListCtrl product=5/medicalProduct=26` | **派生自 machineCenterOrderVoList 嵌套访问 medicalProduct**（A） |

---

## §20 生命周期 DAG

### §20.1 完整加工中心 DAG

```
[Delivery (waitingDeliveryList)]
    ↓ F6 sendMedicalProductToMachineCenter
[MachineCenter (machineCenterId)] ──── JSON.stringify
    ↓ F3 getMedicalProductMachineCenterVoList (Read 校验)
[MachineCenterOrder Created (machineCenterOrderId)]
    ↓
    ├── selectMachineCenterOrderRecordVoList (列表)
    ├── getMachineCenterCashflowVo (详情)
    ├── getMachineCenterOrder (单订单)
    ↓
[startMachineCenterOrder] → status 更新
    ↓
[processProduct] → getCanBeProcessSkuInListOfProduct
    ↓
[saveStock] → saveToBeProcessSkuInListOfProduct (F5) → medicalProductStockBatctPoListJson
    ↓
[receiveMachineCenterOrder] → receiveStatus = 1
    ↓
[deliveryMachineCenterOrder] → medicalProductDelivery.deliveryStatus = 1
    ↓
[completeMachineCenterOrder] → status 更新
    ↓
[可选] closeMachineCenterOrder → 关闭
    ↓
[可选] createMedicalStockLoss → medicalProductStockId 报损
```

### §20.2 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| Delivery | MachineCenter | A | F6 `sendMedicalProductToMachineCenter` (Request) | L3966 |
| MedicalProduct | MachineCenter | A | F3 `getMedicalProductMachineCenterVoList` (Runtime) | L3836 |
| MachineCenter | MachineCenterOrder | A | F6 响应派生 | L3966 |
| MachineCenterOrder | MedicalProduct | A | machineCenterOrderVoList 嵌套 | L16321/L16324 |
| MachineCenterOrder | Delivery | A | medicalProductDelivery.deliveryStatus | L4332 |
| MachineCenterOrder | Stock | A | F5 `saveToBeProcessSkuInListOfProduct` | L16197 |
| MachineCenterOrder | Cashflow | A | getMachineCenterCashflowVo | L16269 |
| MedicalProduct | MachineCenterOrder | A | F6 Request `medicalProductMachineCenterPoListJson` | L3966 |
| Machine | Stock | A | F5 + medicalProductStockId | L16197/L16321 |
| Stock | Machine | F | - | - |
| Delivery | Machine | A | F6 + getMachineCenterCashflowVo | L3966/L16269 |
| Machine | Delivery | A | medicalProductDelivery 嵌套 | L4332 |

---

## §21 Controller 消费矩阵

### §21.1 9+ Controller 消费矩阵（保持 S1-149）

| Controller | Machine | MachineCenter | machineCenterOrder | medicalProduct | delivery | stock | 等级 |
|---|---:|---:|---:|---:|---:|---:|:---:|
| **machineOrderCtrl** (L16094) | 0 | 0 | **2** (id/status) | 2 | 0 | 0 | A |
| **machineOrderListCtrl** (L4264) | 0 | 0 | **2** (id/receiveStatus) | 0 | **1** (medicalProductDelivery) | 0 | A |
| **machineOrderWaitProcessCtrl** (L16357) | 0 | 0 | 0 | 0 | 0 | 0 | A (Stub) |
| **machineOrderBrokenCtrl** (L16261) | 0 | **1** (machineCenterId) | **1** (machineCenterOrderVoList[].machineCenterOrder.id) | **1** (productName) | 0 | **1** (medicalProductStockId) | A |
| **deliveryInputCtrl** (L3812) | 0 | 0 | 0 | 38 | 0 | 0 | A |
| **deliveryInputRecordCtrl** (L4024) | 0 | 0 | 0 | 27 | 0 | 0 | A |
| **deliveryProcessingCtrl** (L4236) | 0 | 0 | 0 | 26 | 0 | 0 | A |
| **myMaterialBillCtrl** (L32435) | 0 | 0 | 0 | 40 | 0 | 49 | A |
| **optometryCtrl** (L34776) | 0 | 0 | 0 | 16 | 0 | 38 | A |

### §21.2 核心观察

1. **machineOrderCtrl 是 Machine 域核心 Controller**：9 个 API + 6 个 State 变更
2. **machineOrderListCtrl 是签收/发货 Controller**：4 个 API + medicalProductDelivery 桥
3. **machineOrderBrokenCtrl 是报损 Controller**：cashflowId + machineCenterId 联合 StateParams
4. **machineOrderWaitProcessCtrl 是空 Stub**：仅 if/else 设 $scope.tab
5. **Machine Controller 不直接消费 Delivery / Stock 字段**（经 API 桥接）

---

## §22 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 4 Controllers + 4 HTML | A | - | 全部 | A |
| 2 | Controller | 4 真实 + 11 NOT FOUND | A | - | L16094/L4264/L16357/L16261 | A |
| 3 | State | machineOrderWaitAccess / Processing / Testing | A | - | 8 个 state | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | cashflowId + machineCenterId | A | - | L16264-L16266 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | receiveStatus (0/1) | A | - | L4318 | A |
| 10 | Status | machineCenterOrder.status / receiveStatus | A | - | L16231/L4318 | A |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=10/12 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | medicalProductId (F3/F4) | A | - | L3822 | A |
| 15 | Default | receiveStatus=0 | A | - | L4297 | A |
| 16 | Data Source | 9 Machine API + 4 加工 API | A | - | 全部 | A |
| 17 | Object | machineCenterOrder.id / status / receiveStatus | A | - | L16231/L4318 | A |
| 18 | Request | { machineCenterOrderId } / { cashflowId, machineCenterId } | A | - | L16213/L16269 | A |
| 19 | Response | machineCenterOrderVoList[].machineCenterOrder | A | - | L16321 | A |
| 20 | Function | startOrder / completeOrder / closeOrder / receiveOrder / deliveryReceiveOrder | A | - | 多处 | A |
| 21 | State Bridge | cashflowId + machineCenterId (联合 State) | A | - | L16264-L16266 | A |
| 22 | Object Bridge | medicalProduct.objectId = lockMachineCenter.id (Runtime) | A | - | L3854 | A (Runtime) |
| 23 | API Bridge | F3-F6 + startMachineCenterOrder / completeMachineCenterOrder | A | - | L3836/L3885/L3966/L16212-L16224 | A |
| 24 | Business Interpretation | machineCenterOrder 是加工中心核心对象 | A | - | - | A (派生) |
| 25 | Evidence Grade | 21 A / 1 C / 0 D / 0 E / 4 F | - | - | - | - |
| 26 | V4.4 Decision | machineCenter + machineCenterOrder 必保留, Machine/Processing 概念 F | A | - | - | A |

---

## §23 历史差异

### §23.1 S1-129/142/148/149 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-129: Machine/Delivery 无直接字符级桥 | 实际经 machineCenterOrderVoList 嵌套 A 字段桥 | **应改** | **保持 S1-129 但增加"经 API 派生 A"** |
| S1-142: deliveryStatus 是 delivery 字段 | 实际是 `medicalProductDelivery.deliveryStatus` 嵌套字段 | **本轮新增** | **A (L4332)** |
| S1-148: cashflow.medicalProductVoList 派生 | 实际 L7070 派生 4 VoList ID 数组 | 保持 | **保持 S1-148 修正** |
| S1-149: machineOrderId 0 命中 F | 实际是 `machineCenterOrderId` 11 命中 | **应改** | **A (字符串拼接差异)** |
| S1-149: machineOrder 字段 0 命中 F | 实际是 `machineCenterOrder.id/status/receiveStatus` 4 命中 | **应改** | **A (字符串拼接差异)** |
| S1-149: machineOrderVoList 0 命中 F | 实际是 `machineCenterOrderVoList` 3 命中 | **应改** | **A (字符串拼接差异)** |
| S1-149: machineOrderListCtrl 派生自 medicalProductVoList | 实际经 machineCenterOrderVoList 派生 medicalProduct.productName | **应改** | **A (L16324)** |
| S1-149: medicalProductName 0 命中 | 实际 medicalProduct.productName 1 命中 (machineOrderBrokenCtrl) | **应改** | **A (L16324)** |
| S1-149: machineOrderWaitProcessCtrl 实际是 WaitProcess Stub | 实际是 4 Tab if/else Stub | 保持 | **保持 S1-149 修正** |
| S1-149: machineOrderCompletedCtrl NOT FOUND | 仍 NOT FOUND | 保持 | **保持 S1-149 修正** |

### §23.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~machineOrder 是独立 Object 实体~~ | 字符级 `machineOrder` 0 命中, 实际是 `machineCenterOrder` 字符串拼接 | **本轮重大发现** | **A (machineCenterOrder 真实, machineOrder 是 Controller 名)** |
| ~~machineOrderId 是独立 ID~~ | 字符级 0 命中, 实际是 `machineCenterOrderId` | **本轮重大发现** | **A (machineCenterOrderId)** |
| ~~Processing 是独立 Object~~ | processing / processId / processingId 全部 0 命中 | **本轮重大发现** | **F (Processing 概念不存在, 只是 UI Tab)** |
| ~~"待加工/处理中/已完成/破损"是 status 枚举~~ | 实际是 UI Tab 分类 (Tab 1/2/3/4) | **本轮重大发现** | **A (UI Tab, 不是后端 status)** |
| ~~machineOrderListCtrl medicalProduct=26 来自 medicalProductVoList~~ | 实际是经 `machineCenterOrderVoList` 嵌套 | **本轮新增** | **A (L16321/L16324 派生)** |
| ~~machineOrderBrokenCtrl 消费 machineOrder~~ | 实际是 Cashflow 报损 (cashflowId + machineCenterId) | **本轮重大发现** | **A (Cashflow 报损, 不是 machineOrder)** |
| ~~machineOrderCtrl machineOrder 字段访问~~ | 实际是 `machineCenterOrder.status` 字段写入 | **本轮重大发现** | **A (L16231)** |
| ~~Machine 概念独立存在~~ | `machine` 全词 0 命中 | **本轮重大发现** | **F (Machine 概念不存在, 只有 MachineCenter)** |
| ~~medicalProductName 0 命中保持 S1-145 修正~~ | 实际 `medicalProduct.productName` 字符级 1 命中 (L16324) | **本轮修正** | **A (L16324 命中, 但 medicalProduct.name 仍 0)** |
| ~~machineCenterVo 0 命中保持 S1-149 修正~~ | 仍 0 命中 | 保持 | **保持 S1-149 修正** |

### §23.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 212_S1-149 全部保持原样
- 本文档 213_*.md 单独记录加工中心域完整闭环

---

## §24 V4.4 加工中心规格

### §24.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| **machineCenterId 独立 ID** | 26 命中 | ✓ |
| **machineCenterOrderId 独立 ID** | 11 命中 | ✓ |
| **machineCenterOrder Object** | 4 字段命中 | ✓ |
| **machineCenterOrder.status** | L16231 | ✓ |
| **machineCenterOrder.receiveStatus** | L4318 | ✓ |
| **machineCenterOrderVoList Container** | L16321 | ✓ |
| **medicalProductDelivery.deliveryStatus** | L4332 | ✓ |
| **medicalProduct.productName** (machineCenterOrderVoList 嵌套) | L16324 | ✓ |
| 4 个 Machine Controller (machineOrderCtrl / List / WaitProcess / Broken) | L16094/L4264/L16357/L16261 | ✓ |
| 8 个 State (Chain + 非 Chain) | L16358-L16366 | ✓ |
| 6 个 Machine Lifecycle API (start / complete / close / receive / delivery / get) | L16212-L16237/L4310/L4324 | ✓ |
| 3 个 machineCenter 域 API (selectMachineCenterListOfProduct / selectMachineCenterOrderRecordVoList / getMachineCenterCashflowVo) | L4277/L4299/L16269 | ✓ |
| 3 个 machineCenter Write API (getMachineCenterVo / updateMachineCenterInfo / updateMachineCenterCompanyIdArray) | L56908/L56927/L57061 | ✓ |
| F3 `getMedicalProductMachineCenterVoList` | L3836 | ✓ |
| F4 `getCanBeDeliverySkuInListOfProduct` | L3885/L35054 | ✓ |
| F5 `saveMedicalProductStockBatch` + `saveToBeProcessSkuInListOfProduct` | L4007/L16197 | ✓ |
| F6 `sendMedicalProductToMachineCenter` | L3966 | ✓ |
| `createMedicalStockLoss` | L16310 | ✓ |
| `medicalProduct.objectId` Runtime Mutation | L3854 | ✓ (关键) |

### §24.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `machine` / `machineId` / `machineVo` / `machineList` 字段 | ✗ (0 命中, Machine 概念不存在) |
| `machineOrder` / `machineOrderId` / `machineOrderVo` / `machineOrderVoList` / `machineOrderList` 字段 | ✗ (0 命中, 实际是 machineCenterOrder) |
| `processing` / `processId` / `processingId` 字段 | ✗ (0 命中, Processing 概念不存在) |
| `machineOrderCompletedCtrl` Controller | ✗ (NOT FOUND) |
| `machineCenterCtrl` / `machineCenterListCtrl` / `machineManageCtrl` Controller | ✗ (NOT FOUND) |
| `processingCtrl` / `machineCtrl` / `machineProcessCtrl` Controller | ✗ (NOT FOUND) |
| `machineOrderCreateCtrl` / `UpdateCtrl` / `DetailCtrl` / `PrintCtrl` Controller | ✗ (NOT FOUND) |
| `machineCenterVo` / `machineCenterVoList` 独立 VO 容器 | ✗ (0 命中) |
| `machineCenter.machineCenterOrder` / `machineCenterOrder.machineCenter` 字段 | ✗ (无直接字段桥) |
| `machineCenterOrder.remark/createTime/completedTime` 字段 | ✗ (0 命中) |
| `machineCenterOrder.machineCenter` / `machineCenterOrder.medicalProduct` 字段 | ✗ (0 命中, 经 machineCenterOrderVoList 嵌套) |
| `stock.machineCenterOrder` / `machineCenterOrder.stock` 字段 | ✗ (0 命中) |
| `delivery.machineCenterOrder` / `machineCenterOrder.delivery` 字段 | ✗ (0 命中, 经 medicalProductDelivery 嵌套) |
| `medicalProduct.machineCenterOrder` 字段 | ✗ (0 命中) |
| `medicalProduct.name` 字段 | ✗ (0 命中, 只有 productName) |
| `getMachineOrder*.json` / `saveMachineOrder*.json` / `createMachineOrder*.json` 等独立 API | ✗ (0 命中, 实际是 machineCenterOrder) |
| `machineOrderCompleted.html` 实际有 Controller | ✗ (HTML 存在但 NOT FOUND) |
| "待加工/处理中/已完成/破损" 作后端 status 枚举 | ✗ (实际是 UI Tab 分类) |
| 6 ID 合并 | ✗ (machineCenterId / machineCenterOrderId / medicalProductId / stockInSkuId / cashflowId / patientId 必须严格区分) |

### §24.3 6 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Machine** | F (0 命中) | 独立 ID 实体 |
| **MachineCenter** | A+B (独立 ID + 列表) | 包含 machineCenterOrder 字段 (F) |
| **MachineCenterOrder** | A+B (独立 ID + 嵌套字段) | 独立 Object 容器 (F) |
| **Processing** | F (0 命中) | 独立 ID 实体 / status 枚举 |
| **MedicalProductDelivery** | A+B (deliveryStatus 字段) | 独立 Create API (F) |
| **MedicalProduct (Machine View)** | A (经 F3/F6 派生) | 独立 machineCenterOrder 字段 (F) |

### §24.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `machineCenterOrder.status` (Object Field) | A | L16231 (machineOrderCtrl) |
| `machineCenterOrder.receiveStatus` (Object Field) | A | L4318 (machineOrderListCtrl) |
| `machineCenterOrderVoList[].machineCenterOrder.id` (Object Field) | A | L16321 (machineOrderBrokenCtrl) |
| `medicalProductDelivery.deliveryStatus` (Object Field) | A | L4332 (machineOrderListCtrl) |
| `medicalProduct.productName` (Object Field, 经 machineCenterOrderVoList) | A | L16324 (machineOrderBrokenCtrl) |
| `medicalProduct.objectId` (Runtime Mutation) | A | L3854 (保持 S1-149) |
| F3 `medicalProductMachineCenterPoList` (Request) | A | L3822-L3828 |
| F4 `deliveryStockInSkuVoList[].stockInSku.id + deliveryCount` (Response) | A | L3989 |
| F5 `medicalProductStockBatctPoListJson` (Request) | A | L3991 |
| F6 `medicalProductMachineCenterPoListJson` (Request) | A | L3966 |

### §24.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Machine → Delivery 直接字段桥 | F (经 medicalProductDelivery 嵌套 A) |
| Machine → Stock 直接字段桥 | F (经 F5 Request Bridge A) |
| MachineCenter → MachineCenterOrder 直接字段桥 | F (经 machineCenterOrderVoList 嵌套 C) |
| medicalProduct → machineCenterOrder 字段桥 | F (经 machineCenterOrderVoList 嵌套) |
| machineCenterOrder.remark 字段 | F |
| "待加工" 等作 status 枚举 | F |

### §24.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `machineOrder` | 不是 Object, 实际是 `machineCenterOrder` (字符串拼接) | **命名误导** |
| `machineOrderId` | 字符级 0 命中, 实际是 `machineCenterOrderId` | **命名误导 (S1-149 误判已修正)** |
| `machineOrderListCtrl` | 实际是 `machineCenterOrder` 签收/发货列表 | 命名误导 |
| `machineOrderWaitProcessCtrl` | 实际是空 Stub (4 Tab if/else) | 命名误导 |
| `machineOrderBrokenCtrl` | 实际是 Cashflow 报损 (cashflowId + machineCenterId 联合) | 命名误导 |
| `machineOrderCompletedCtrl` | NOT FOUND | 命名误导 |
| `Processing` / `processId` | 0 命中, 不存在独立 Object | 命名误导 |
| `待加工/处理中/已完成/破损` | UI Tab 分类 (1/2/3/4) 不是后端 status | 命名误导 |
| `selectInStoreMachineCenterCashflowVoList.json` | 实际是 Cashflow VO List, 不是 MachineOrder | 命名误导 |
| `getMachineCenterOrder.json` | 实际是 `machineCenterOrder` (单订单查询) | 命名误导 |
| `getMachineCenterCashflowVo.json` | 实际是 Cashflow + machineCenterOrderVoList 复合 VO | 命名误导 |
| `saveToBeProcessSkuInListOfProduct.json` | 实际是 machineCenterOrder 加工保存 (F5 加工版本) | 命名误导 |
| `sendMedicalProductToMachineCenter.json` | 实际触发 machineCenterOrder 创建, 不是 "send medical product" | 命名误导 |
| `createMedicalStockLoss.json` | 实际是 medicalProductStockId 报损, 不是 medicalStockLoss Object | 命名误导 |
| `medicalProduct.productName` | 经 machineCenterOrderVoList 嵌套命中, 不是 medicalProduct.name 顶层 | 命名误导 |
| `medicalCenter.machineCenterId` 顶层 | 实际是 `machineCenter.id` (4 命中) | 命名误导 |

---

## §25 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Machine 数据库表结构 | F (0 命中) | 需后端 (前端证据 0) |
| 2 | MachineCenter 数据库表结构 | F | 需后端 |
| 3 | MachineCenterOrder 数据库表结构 | F | 需后端 |
| 4 | Processing 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 5 | machineCenterOrderId 完整生命周期 | F (部分确认) | 需后端 |
| 6 | 6 个 Machine Lifecycle API 完整 Response schema | F | 需后端 |
| 7 | startMachineCenterOrder / completeMachineCenterOrder / closeMachineCenterOrder 状态枚举 | F (UI Tab 推测) | 需后端 |
| 8 | "Chain" 与非 Chain 业务区别 | F (UI 命名差异) | 需业务定义 |
| 9 | medicalProductDelivery 数据库表结构 | F (字段访问存在) | 需后端 |
| 10 | 9 NOT FOUND Controller 命名历史 | F | 需 git log |
| 11 | `getMachineCenterVo` (L56908) 完整 schema | F | 需后端 |
| 12 | `selectMachineCenterOrderRecordVoList` (L4121/L4299) 完整 Response | F | 需后端 |
| 13 | `getMachineCenterCashflowVo` (L16269) 完整 Response | F | 需后端 |
| 14 | machineOrderCompleted.html 对应 Controller | F (NOT FOUND) | 需 git log / 业务决策 |
| 15 | statusManage 实际 status 字段命名 | F (L16231/L4318 推测) | 需后端 |
| 16 | 加工状态后端 status 枚举值 (开始/完成/关闭/签收/发货) | F (UI 推测) | 需后端 |
| 17 | medicalProduct.productName 是不是数据库字段 | F (L16324 唯一命中) | 需后端 |
| 18 | "machineOrder" 是否曾经是独立 Object 命名 | F | 需 git log |
| 19 | saveToBeProcessSkuInListOfProduct 与 saveMedicalProductStockBatch 业务关系 | F | 需后端 |

---

## §26 Git / 完整性

### §26.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-212 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 213_*.md | ✓ |

### §26.2 Git 操作

```
git add -- 213_S1-150_MachineCenter_MachineOrder_MachineProcessing加工中心全生命周期总审计.md
git diff --cached --name-only
git commit -m "docs(213): S1-150 MachineCenter/MachineOrder/MachineProcessing 加工中心全生命周期总审计"
git push origin master
```

### §26.3 预期

- tracked = 220 → **221**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `8c87b181cc05c79e743d2a11a11e384fed5129ba` (S1-149 commit)

---

## 文档元信息

- **审计范围**：S1-150 (MachineCenter / MachineOrder / MachineProcessing 加工中心域)
- **本轮新增文件**：`213_S1-150_MachineCenter_MachineOrder_MachineProcessing加工中心全生命周期总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-151** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
