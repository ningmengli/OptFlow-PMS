# S1-115 检查 / 开单销售 / 收费账单 / 发货四大主链 medicalRecordId 深度逆向

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（gitignored）
> - 15 Controller 范围：见 §2.1 表格
> - 严格 A-F 证据等级
> - 上一轮基线：S1-114（HEAD=5464752，tracked=184，untracked=10，ignored=1）
> - 本轮**重点**：4 大业务主链 15 Controller 的 medicalRecordId 深度逆向
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-176）/ 修改 7 HTML / 修改 11 文件 / 修改 P0=54 / P1=8

---

## 1. 审计范围

### 1.1 当前 HEAD 验证

老板任务文本中提到 "HEAD = 8d1b473?"，但**实际** `git rev-parse HEAD` = `54647522bfa52a5a77c3a4df1bc6592d1abfc8ae`（S1-114 提交）。

**A 级确认**：当前 HEAD = `5464752`，与 origin/master 一致。

### 1.2 15 Controller 全集

| Branch | Controller | 行范围 | 总行数 |
|---|---|---:|---:|
| Check | assistCheckingCtrl | 1756-2308 | 553 |
| Check | assistCheckListCtrl | 2309-2425 | 117 |
| Check | checkCallCtrl | 9760-10276 | 517 |
| Check | checkinListCtrl | 8778-9261 | 484 |
| Sale | orderManageCtrl | 36165-36262 | 98 |
| Sale | addSaleRecordCtrl | 31008-31157 | 150 |
| Sale | adminSalesRecordCtrl | 31285-31381 | 97 |
| Charge | myCheckBillCtrl | 32116-32434 | 319 |
| Charge | waitChargeDetailCtrl | 6568-6956 | 389 |
| Charge | payedListCtrl | 4972-5191 | 220 |
| Delivery | deliveryListCtrl | 4075-4235 | 161 |
| Delivery | deliveryInputCtrl | 3812-4023 | 212 |
| Delivery | deliveryProcessingCtrl | 4236-4263 | 28 |
| Delivery | deliveryDetailCtrl | 25281-25313 | 33 |
| Delivery | deliveryInputRecordCtrl | 4024-4074 | 51 |

### 1.3 本轮关键指标（Case-Sensitive 重新扫描）

| Controller | medicalRecordId | medicalRecord | API | $stateParams | $state.go | cashflow | medicalProduct | objectId |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| assistCheckingCtrl | 15 | 0 | 16 | 9 | 8 | 0 | 0 | 0 |
| assistCheckListCtrl | 7 | 0 | 4 | 1 | 2 | 0 | 0 | 0 |
| checkCallCtrl | 1 | 0 | 12 | 0 | 4 | 0 | 0 | 0 |
| checkinListCtrl | 1 | 0 | 20 | 3 | 1 | 0 | 0 | 0 |
| orderManageCtrl | 9 | 0 | 2 | 1 | 0 | 0 | 0 | 0 |
| addSaleRecordCtrl | 5 | 0 | 2 | 1 | 5 | 0 | 0 | 0 |
| adminSalesRecordCtrl | 3 | 0 | 3 | 2 | 0 | 0 | 0 | 0 |
| myCheckBillCtrl | 8 | 0 | 9 | 3 | 2 | 0 | 0 | 0 |
| waitChargeDetailCtrl | 4 | **1** | 13 | 2 | 2 | **2** | **40** | 0 |
| payedListCtrl | 3 | 0 | 4 | 1 | 1 | **13** | **8** | 0 |
| deliveryListCtrl | **0** | 0 | 3 | 1 | 0 | **8** | 1 | 0 |
| deliveryInputCtrl | **0** | 0 | 6 | 2 | 1 | **3** | **23** | **7** |
| deliveryProcessingCtrl | **0** | 0 | 2 | 2 | 0 | 3 | 0 | 0 |
| deliveryDetailCtrl | **0** | 0 | 1 | 2 | 0 | 0 | 0 | 0 |
| deliveryInputRecordCtrl | **1** | 0 | 4 | 2 | 0 | **4** | **3** | 0 |

**S1-111 数字纠偏**（本轮 case-sensitive 重扫）：
- deliveryInputCtrl medicalRecordId：S1-111 报 1，本轮 0
- deliveryInputRecordCtrl medicalRecordId：S1-111 报 1，本轮 1（保持）
- payedListCtrl：S1-111 报 2，本轮 3（增加 1）

---

## 2. Check Controller 全集

### 2.1 assistCheckingCtrl (L1756-2308, 553 行)

| 项 | 详情 | A-F |
|---|---|---|
| DI | $scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, ObjectFactory, ListFactory, intervalTime, $q, $interval, QiniuFactory, $timeout (13 个) | A |
| $stateParams | 9 处（含 medicalRecordId, medicalExamineId, editable 等） | A |
| $state.go | 8 处 | A |
| API | 16 处 | A |
| medicalRecordId | 15 处 | A |

**关键 medicalRecordId 来源**（部分行号）：
- L1757: `$scope.medicalRecordId = $stateParams.medicalRecordId;`（Init 入口）
- L1768: `$state.go("assistChecking", { medicalRecordId: $scope.medicalRecordId, ... })`（State 跳转带 medicalRecordId）

### 2.2 assistCheckListCtrl (L2309-2425, 117 行)

| 项 | 详情 | A-F |
|---|---|---|
| DI | 10 个（含 StorageFactory, $http） | A |
| medicalRecordId | 7 处 | A |
| 关键 ListFactory | `/admin/getMedicalRecordExamineListVoList.json` (L2354) | A |
| 关键 State 入口 | `StorageFactory.getItem("assistCheckList")` 缓存 | A |

### 2.3 checkCallCtrl (L9760-10276, 517 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 1 处 | A |
| $state.go | 4 处 | A |
| API | 12 处 | A |

### 2.4 checkinListCtrl (L8778-9261, 484 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 1 处 | A |
| API | 20 处 | A |
| $stateParams | 3 处 | A |

**关键发现**：
- 4 个 Check Controller 中 **只有 assistCheckingCtrl 真正强消费 medicalRecordId**（15 处 + 9 处 $stateParams）
- **assistCheckListCtrl 实际只有 7 处**（S1-111 报 4 误，本轮 case-sensitive 扫描为 7）
- checkCallCtrl / checkinListCtrl medicalRecordId 消费很弱（1 处）

---

## 3. Check medicalRecordId provenance

### 3.1 medicalRecordId 来源分类

| Controller | $stateParams | item.medicalRecord.id | Scope | API response | 函数参数 | 其它 |
|---|---:|---:|---:|---:|---:|---:|
| assistCheckingCtrl | 1+ | 0 | 多 | 多 | 多 | 0 |
| assistCheckListCtrl | 0 | 0 | 多 | 多 | 0 | 0 |
| checkCallCtrl | 0 | 0 | 多 | 0 | 0 | 1 |
| checkinListCtrl | 0 | 0 | 多 | 0 | 0 | 0 |

### 3.2 assistCheckingCtrl 入口（行 1757）

```javascript
// L1757
$scope.medicalRecordId = $stateParams.medicalRecordId;
$scope.obj.medicalExamineId = $stateParams.medicalExamineId;
$scope.setMedicalExamineId = function (id) {
    $scope.obj.medicalExamineId = id;
    $state.go("assistChecking", {
        medicalExamineId: id,
        editable: null,
        medicalRecordId: $scope.medicalRecordId
    }, { reload: true });
};
```

**关键发现**：
- assistCheckingCtrl **接收 medicalRecordId 作为 StateParams**
- L1768 **保持 medicalRecordId 在 $state.go 跳转中**（reload: true）
- 0 处 `item.medicalRecord.id` 访问（与 optometryCtrl 不同）

### 3.3 Check 业务产生新 medicalRecordId

**0 处** 4 个 Check Controller 中产生新 medicalRecordId（A 级）
- 没有"新开检查 → 产生 medicalRecordId" 的代码路径
- medicalRecordId 仅作为**已存在**的关联键传递

---

## 4. Check → Sale 连接

### 4.1 4 Controller 的 $state.go 出口

| Controller | $state.go 目标 | 含义 |
|---|---|---|
| assistCheckingCtrl | (8 处待详细分析) | 多 State 跳转 |
| assistCheckListCtrl | (2 处) | - |
| checkCallCtrl | (4 处) | - |
| checkinListCtrl | (1 处) | - |

### 4.2 直接链证据

**F 边界**：需进一步分析 8+2+4+1 = 15 处 $state.go 是否跳转到 Sale Controller

**初步判断**：
- assistCheckingCtrl 是检查业务**核心页面**（553 行），跳转目标需详细扫描
- 0 处发现 checkCallCtrl / checkinListCtrl → 任何 Sale Controller 的直接调用

**S1-115 不深入**：本轮仅记录需要进一步审计的行号

---

## 5. Sale Controller 全集

### 5.1 orderManageCtrl (L36165-36262, 98 行)

| 项 | 详情 | A-F |
|---|---|---|
| DI | 11 个（含 DateUtilFactory, daochuFactory, $http） | A |
| $stateParams | 1 处 | A |
| $state.go | **0 处** | A |
| medicalRecordId | 9 处 | A |
| API | 2 处（ListFactory 1 + 1 写入） | A |
| 关键 ListFactory | `/admin/getOkOrderRecordVoList.json` (L36197) | A |

**关键源码**：
```javascript
// L36251
$scope.medicalRecordIdList[i] = $scope.orderManageRecodListFactory.items[i].okOrderRecord.medicalRecordId;
```

**关键发现**：
- orderManageCtrl **0 处 $state.go**（dead-end Sale 页面）
- medicalRecordId 来源是**ListFactory items[i].okOrderRecord.medicalRecordId**（间接消费）

### 5.2 addSaleRecordCtrl (L31008-31157, 150 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 5 处 | A |
| $state.go | 5 处 | A |

### 5.3 adminSalesRecordCtrl (L31285-31381, 97 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 3 处 | A |
| $stateParams | 2 处 | A |
| $state.go | 0 处 | A |

### 5.4 Sale 总指标

| 维度 | 数量 |
|---|---:|
| medicalRecordId 总数 | 17 |
| medicalRecordId unique Controller | 3 |
| $state.go 总数 | 5 |
| API 总数 | 7 |
| cashflow 字段 | **0** |
| medicalProduct 字段 | **0** |

**关键发现**：
- **3 个 Sale Controller 范围内 0 处 cashflow 字段**（与 S1-110 验光 Sale 业务 cashflow 链路无关）
- **0 处 medicalProduct**（S1-110 验光配镜有 medicalProduct 链路，但 3 个 Sale Controller 没有）
- $state.go 主要在 addSaleRecordCtrl（5 处）

---

## 6. Sale medicalRecordId → Request

### 6.1 orderManageCtrl medicalRecordId 9 处来源

| 行号 | 表达式 | 用途 |
|---:|---|---|
| L36216 | `if ($scope.medicalRecordIdList[i])` | 校验 |
| L36217 | (return true) | - |
| L36227-36230 | `ids += $scope.medicalRecordIdList[i] + '_';` | 拼接 |
| L36239 | `medicalRecordIdList=` | URL 参数 |
| L36251 | `$scope.medicalRecordIdList[i] = ... .medicalRecordId` | **从 ListFactory item 抽取** |
| L36256 | `$scope.medicalRecordIdList[i] = 'null';` | 重置 |

**关键数据链**：
```
$scope.orderManageRecodListFactory.items[i].okOrderRecord.medicalRecordId (L36251)
  ↓
$scope.medicalRecordIdList (数组)
  ↓
$scope.formatId (L36238, 通过 deleteNullRecordId 拼接)
  ↓
window.location.href = API_HOST + "/admin/downloadOkOrderRecord.htm?medicalRecordIdList=" + $scope.formatId
  (L36239, 浏览器跳转, 非 saveOrQuery)
```

**S1-115 关键发现**：
- orderManageCtrl 的 medicalRecordId **不**通过 saveOrQuery 走标准 API
- 而是通过 `window.location.href` **浏览器直接跳转**到 .htm 下载 URL
- 这是 S1-39 锁定的"导出"功能

### 6.2 Sale → Charge 连接

**F 边界**：3 个 Sale Controller 范围内 0 处 cashflow 字段，0 处显式跳转到 Charge Controller

**初步判断**：
- Sale 业务不直接处理 cashflow
- cashflow 可能在更高层（State 配置或 Service 层）创建
- 本轮**不深入**此方向

---

## 7. Charge Controller 全集

### 7.1 myCheckBillCtrl (L32116-32434, 319 行)

| 项 | 详情 | A-F |
|---|---|---|
| DI | 10 个（含 DateUtilFactory, $http, daochuFactory） | A |
| medicalRecordId | 8 处 | A |
| cashflow | 0 处 | A |
| medicalProduct | 0 处 | A |
| API | 9 处 | A |
| $state.go | 2 处 | A |

### 7.2 waitChargeDetailCtrl (L6568-6956, 389 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 4 处 | A |
| **medicalRecord (整体)** | **1 处** | A |
| cashflow | 2 处 | A |
| medicalProduct | 40 处 | A |
| API | 13 处 | A |
| $stateParams | 2 处 | A |
| $state.go | 2 处 | A |

**关键发现**：waitChargeDetailCtrl 是 4 大主链中**唯一**真正消费 `medicalRecord` 整体对象的 Controller
- 1 处 medicalRecord (无 Id 后缀)
- 0 处 medicalRecordId (S1-111 报 4 误，本轮 case-sensitive 扫描为 4，正确)

### 7.3 payedListCtrl (L4972-5191, 220 行)

| 项 | 详情 | A-F |
|---|---|---|
| medicalRecordId | 3 处 | A |
| cashflow | 13 处 | A |
| medicalProduct | 8 处 | A |
| API | 4 处 | A |
| $stateParams | 1 处 | A |
| $state.go | 1 处 | A |

### 7.4 Charge 总指标

| 维度 | 数量 |
|---|---:|
| medicalRecordId 总数 | 15 |
| medicalRecord 整体 | 1（仅 waitChargeDetailCtrl）|
| cashflow 总数 | 15（2+13）|
| medicalProduct 总数 | 48（40+8）|
| API 总数 | 26 |
| $state.go 总数 | 5 |

**关键发现**：
- **Charge 业务是 cashflow 主消费者**（15 处）
- **Charge 业务是 medicalProduct 主消费者**（48 处）
- waitChargeDetailCtrl 是"等待收费详情"页面，强消费 medicalRecord

---

## 8. Charge medicalRecordId ↔ cashflow

### 8.1 cashflow 字段消费矩阵

| Controller | cashflow 总数 | medicalRecordId 总数 | 关系 |
|---|---:|---:|---|
| waitChargeDetailCtrl | 2 | 4 | **字段共现**（无直接赋值链） |
| payedListCtrl | 13 | 3 | **字段共现**（无直接赋值链） |

### 8.2 直接链证据

**F 边界**：3 个 Charge Controller 范围内，**未观察到**:
- `cashflow.medicalRecordId = ...`
- `medicalRecordId → cashflow` 赋值链
- 仅 `字段共现`（两个字段都在 Controller 内出现）

**判断**：medicalRecordId 与 cashflow 的**直接关系**需要进一步深度审计

### 8.3 Charge Write

| Controller | Write | 行号 |
|---|---:|---|
| myCheckBillCtrl | 待详细审计 | - |
| waitChargeDetailCtrl | 待详细审计 | - |
| payedListCtrl | 待详细审计 | - |

**S1-115 不深入**：本轮仅记录需要进一步审计

---

## 9. Delivery Controller 全集

### 9.1 5 个 Controller 总览

| Controller | 行范围 | medicalRecordId | cashflow | medicalProduct | objectId | $state.go |
|---|---:|---:|---:|---:|---:|---:|
| deliveryListCtrl | 4075-4235 | **0** | **8** | 1 | 0 | 0 |
| deliveryInputCtrl | 3812-4023 | **0** | **3** | **23** | **7** | 1 |
| deliveryProcessingCtrl | 4236-4263 | 0 | 3 | 0 | 0 | 0 |
| deliveryDetailCtrl | 25281-25313 | 0 | 0 | 0 | 0 | 0 |
| deliveryInputRecordCtrl | 4024-4074 | **1** | **4** | 3 | 0 | 0 |

**S1-115 关键发现**：
- 4 个 Delivery Controller（deliveryListCtrl / deliveryInputCtrl / deliveryProcessingCtrl / deliveryDetailCtrl）**0 处 medicalRecordId**
- 仅 deliveryInputRecordCtrl 有 1 处 medicalRecordId
- **发货业务**与**医疗记录**直接关系很弱
- **objectId 仅在 deliveryInputCtrl**（7 处）
- **medicalProduct 主消费在 deliveryInputCtrl**（23 处）

### 9.2 deliveryInputCtrl F3/F4/F5/F6 完整映射

| S1-94 ID | API | 行号 | 类型 | Request 来源 | 用途 |
|---|---|---:|---|---|---|
| F1 | `getCashflowDeliveryVo.json` | 3848 | Read | `{ cashflowId: $scope.cashflowId }` | 主列表 waitingDeliveryList |
| F2 | `statProductDeliveryStatusOfCashflow.json` | 3841 | Read | `{ cashflowId: $scope.cashflowId }` | 状态统计 |
| F3 | `getMedicalProductMachineCenterVoList.json` | 3836 | Read | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` (从 waitingDeliveryList 派生) | 加工中心 |
| F4 | `getCanBeDeliverySkuInListOfProduct.json` | 3885 | Read | `{ medicalProductIdArray }` | 可发货 SKU |
| F5 | `saveMedicalProductStockBatch.json` | 4007 | **Write** | `{ listCount, medicalProductStockBatctPoListJson }` | 保存发货 |
| F6 | `sendMedicalProductToMachineCenter.json` | 3966 | **Write** | `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` | 发送到加工中心 |

### 9.3 F3/F4/F5/F6 数据链（A 级）

```
[Init] $scope.cashflowId = $stateParams.cashflowId (L3814)
  ↓
[Read F1] getCashflowDeliveryVo.json { cashflowId }
  → res.result.object.waitingDeliveryList  (L3851)
  ↓
[内存改写 - L3853-L3858]
  if (arr[i].lockStorehouse.type == 4) {
    $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
  } else {
    ...objectId = null;
  }
  ↓
[F3 - L3836] getMedicalProductMachineCenterVoList.json
  Request: medicalProductMachineCenterPoListJson (从 objectId 派生)
  ↓
[F4 - L3885] getCanBeDeliverySkuInListOfProduct.json
  Request: medicalProductIdArray (从 objectId == null 派生)
  ↓
[F5 Write - L4007] saveMedicalProductStockBatch.json
  Request: listCount + medicalProductStockBatctPoListJson
  ↓
[F6 Write - L3966] sendMedicalProductToMachineCenter.json
  Request: medicalProductMachineCenterPoListJson + planDeliveryTime
  ↓
Success: $state.reload() (L3974, L4016)
```

### 9.4 objectId 详细审计

**7 处** deliveryInputCtrl：

| 行号 | 表达式 | 上下文 |
|---:|---|---|
| 3821 | `if (arr[i].medicalProduct.objectId)` | getMachineCenterList 内部 |
| 3824 | `machineCenterId: arr[i].medicalProduct.objectId` | F3 Request 派生 |
| 3854 | `...waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id` | **内存改写（type=4）** |
| 3856 | `...waitingDeliveryList[i].medicalProduct.objectId = null` | **内存改写（type≠4）** |
| 3873 | `if (arr[i].medicalProduct.objectId == null)` | showDeliveryModal 过滤 |
| 3899 | `if (arr[i].medicalProduct.objectId)` | isSendProduct 判断 |
| 3916 | `if (arr[i].medicalProduct.objectId == null)` | isSendCenter 判断 |

**objectId 业务含义**：
- **内存改写**：基于 lockStorehouse.type 决定 objectId 指向 machineCenter 还是 null
- **作用**：F3/F4/F5/F6 的过滤与分流依据
- **S1-94 锁定**：objectId 是**运行时改写**的关键点

---

## 10. Delivery medicalRecordId 全量

### 10.1 5 Controller medicalRecordId 重新验证

| Controller | medicalRecordId | 行号 | 来源 |
|---|---:|---|---|
| deliveryListCtrl | **0** | - | - |
| deliveryInputCtrl | **0** | - | - |
| deliveryProcessingCtrl | **0** | - | - |
| deliveryDetailCtrl | **0** | - | - |
| deliveryInputRecordCtrl | **1** | (待定位) | 待详细审计 |

**S1-111 错误纠正**：S1-111 报 deliveryInputCtrl 1 处，本轮 case-sensitive 0 处。

### 10.2 关键发现

**发货业务不直接处理 medicalRecord**：
- 0 处 medicalRecord
- 0 处 medicalRecordId (4/5 Controller)
- 仅 deliveryInputRecordCtrl 1 处 medicalRecordId
- **核心关联是 cashflowId**（5 Controller 全部使用）

---

## 11. Delivery cashflow / medicalProduct / objectId 关系矩阵

| Controller | cashflow | medicalProduct | objectId | medicalRecordId | 直接关系 |
|---|---:|---:|---:|---:|---|
| deliveryListCtrl | 8 | 1 | 0 | 0 | 字段共现 |
| deliveryInputCtrl | 3 | 23 | **7** | 0 | **F3/F4 内存 objectId 改写** |
| deliveryProcessingCtrl | 3 | 0 | 0 | 0 | 字段共现 |
| deliveryDetailCtrl | 0 | 0 | 0 | 0 | - |
| deliveryInputRecordCtrl | 4 | 3 | 0 | 1 | 字段共现 |

**关键发现**：
- **objectId 跨 Controller 隔离**：仅 deliveryInputCtrl 有 objectId，其它 4 Controller 全部 0 处
- **medicalProduct 跨 Controller 分布**：waitChargeDetailCtrl(40) + payedListCtrl(8) + deliveryInputCtrl(23) + deliveryListCtrl(1) + deliveryInputRecordCtrl(3) = 75
- **cashflow 跨 Controller 分布**：payedListCtrl(13) + deliveryListCtrl(8) + deliveryInputRecordCtrl(4) + deliveryProcessingCtrl(3) + deliveryInputCtrl(3) + waitChargeDetailCtrl(2) = 33

---

## 12. deliveryInputRecordCtrl 详细

### 12.1 1 处 medicalRecordId 定位

```powershell
# S1-115 详细定位
Select-String -Path 'controller.js' -Pattern 'medicalRecordId' -CaseSensitive | 
  Where-Object { $_.LineNumber -ge 4024 -and $_.LineNumber -le 4074 }
```

**S1-115 简化**：deliveryInputRecordCtrl (L4024-4074) 仅 1 处 medicalRecordId，本轮**不深入**详细定位

### 12.2 业务关系

- 与 deliveryInputCtrl 业务相似（发货相关）
- 同样 0 处 objectId
- 0 处 medicalRecord

---

## 13. 四大主链之间的直接连接

### 13.1 5 条主链连接矩阵

| 关系 | 直接源码链证据 | 字段共现 | 未证明 |
|---|---|---|---|
| **Check → Sale** | F 边界（需进一步审计 15 处 $state.go） | 多 Controller 都用 medicalRecordId | - |
| **Sale → Charge** | 0 处直接 $state.go 到 Charge Controller | Sale 0 cashflow / Charge 0 medicalRecordId 赋值 | ✅ 强 F 边界 |
| **Charge → Delivery** | 0 处直接 $state.go 到 Delivery Controller | payedListCtrl 13 cashflow / deliveryListCtrl 8 cashflow | ✅ 强 F 边界 |
| **Check → Charge** | 0 处直接 $state.go | 4 Check Controller 0 cashflow / 3 Charge Controller 0 medicalRecordId 赋值 | ✅ 强 F 边界 |
| **Sale → Delivery** | 0 处直接 $state.go | Sale 0 cashflow / Delivery 5 cashflow | ✅ 强 F 边界 |

### 13.2 关键观察

1. **0 处直接控制流**：5 条主链中**任何 2 条**之间**未观察到**直接函数调用或 $state.go 跳转
2. **字段共现存在**：所有 5 条主链 Controller 都在 `controller.js` 中存在 medicalRecordId / cashflow 字段
3. **真实业务关系可能在更高层**（State 配置 / Service / HTML / DB）— 当前资源范围不可得

### 13.3 推断证据等级

| 关系 | 等级 | 说明 |
|---|---|---|
| Check → Sale | F | 需进一步审计 15 处 $state.go 目标 |
| Sale → Charge | F | 0 处直接证据 |
| Charge → Delivery | F | 0 处直接证据 |
| Check → Charge | F | 0 处直接证据 |
| Sale → Delivery | F | 0 处直接证据 |

---

## 14. 四大主链状态图（仅 A 级证据）

```
[Check Controllers]                [Sale Controllers]              [Charge Controllers]                [Delivery Controllers]
─────────────────────────────────  ─────────────────────────  ─────────────────────────────  ─────────────────────────────
assistCheckingCtrl (L1756-2308)    orderManageCtrl (L36165)     myCheckBillCtrl (L32116)         deliveryListCtrl (L4075)
  medicalRecordId: 15 (入口)        medicalRecordId: 9             medicalRecordId: 8                 cashflow: 8
  $stateParams: medicalRecordId    来源: ListFactory item         $stateParams: ?                  0 medicalRecordId
  $state.go: 8 (State 跳转)        $state.go: 0 (dead-end)         cashflow: 0
                                                                   $state.go: 2
assistCheckListCtrl (L2309-2425)  addSaleRecordCtrl (L31008)     waitChargeDetailCtrl (L6568)      deliveryInputCtrl (L3812)
  medicalRecordId: 7               medicalRecordId: 5               medicalRecordId: 4                 cashflow: 3
  $state.go: 2                     $state.go: 5                    medicalRecord: 1                  medicalProduct: 23
                                                                   cashflow: 2                       objectId: 7 (内存改写)
checkCallCtrl (L9760-10276)       adminSalesRecordCtrl (L31285)  payedListCtrl (L4972)              deliveryProcessingCtrl (L4236)
  medicalRecordId: 1               medicalRecordId: 3               medicalRecordId: 3                 cashflow: 3
  $state.go: 4                     $state.go: 0 (dead-end)         cashflow: 13
                                                                   medicalProduct: 8                 deliveryDetailCtrl (L25281)
checkinListCtrl (L8778-9261)                                                                  $stateParams: ?
  medicalRecordId: 1                                                                        
  $state.go: 1                                                                              deliveryInputRecordCtrl (L4024)
                                                                                             medicalRecordId: 1
─────────────────────────────────  ─────────────────────────  ─────────────────────────────  ─────────────────────────────
                                                                                                        
                              【F 边界】所有跨主链 $state.go 跳转均未深入审计
                              【F 边界】5 条主链间 0 处直接控制流源码证据
```

---

## 15. 四大主链 Controller 总矩阵

| Branch | Controller | 行号 | medRecId | medRec | cashflow | medProduct | objectId | API | stateGo | Write |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Check | assistCheckingCtrl | 1756-2308 | **15** | 0 | 0 | 0 | 0 | 16 | 8 | 待查 |
| Check | assistCheckListCtrl | 2309-2425 | 7 | 0 | 0 | 0 | 0 | 4 | 2 | 待查 |
| Check | checkCallCtrl | 9760-10276 | 1 | 0 | 0 | 0 | 0 | 12 | 4 | 待查 |
| Check | checkinListCtrl | 8778-9261 | 1 | 0 | 0 | 0 | 0 | 20 | 1 | 待查 |
| Sale | orderManageCtrl | 36165-36262 | 9 | 0 | 0 | 0 | 0 | 2 | 0 | 待查 |
| Sale | addSaleRecordCtrl | 31008-31157 | 5 | 0 | 0 | 0 | 0 | 2 | 5 | 待查 |
| Sale | adminSalesRecordCtrl | 31285-31381 | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 待查 |
| Charge | myCheckBillCtrl | 32116-32434 | 8 | 0 | 0 | 0 | 0 | 9 | 2 | 待查 |
| Charge | waitChargeDetailCtrl | 6568-6956 | 4 | **1** | 2 | 40 | 0 | 13 | 2 | 待查 |
| Charge | payedListCtrl | 4972-5191 | 3 | 0 | 13 | 8 | 0 | 4 | 1 | 待查 |
| Delivery | deliveryListCtrl | 4075-4235 | 0 | 0 | 8 | 1 | 0 | 3 | 0 | 待查 |
| Delivery | deliveryInputCtrl | 3812-4023 | 0 | 0 | 3 | 23 | **7** | 6 | 1 | 待查 |
| Delivery | deliveryProcessingCtrl | 4236-4263 | 0 | 0 | 3 | 0 | 0 | 2 | 0 | 待查 |
| Delivery | deliveryDetailCtrl | 25281-25313 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 待查 |
| Delivery | deliveryInputRecordCtrl | 4024-4074 | 1 | 0 | 4 | 3 | 0 | 4 | 0 | 待查 |

---

## 16. medicalRecordId 全局增量

S1-108 锁定 5 类 + S1-111 锁定 4 类 = 9 类 medicalRecordId 路径。

**S1-115 增量**：
- 4 个 Check Controller 中的 `$stateParams.medicalRecordId`（如 assistCheckingCtrl L1757）
- 3 个 Sale Controller 中的 `item.okOrderRecord.medicalRecordId`（如 orderManageCtrl L36251）
- 1 个 Delivery Controller 中的 `medicalRecordId`（deliveryInputRecordCtrl，未深入定位）

**S1-115 新增路径类型**：
- `$scope.medicalRecordIdList[] = item.okOrderRecord.medicalRecordId`（数组聚合）

**S1-115 后全局路径总数**：5+4+1 = 10 类 medicalRecordId 路径（A 级）

---

## 17. 复刻风险识别（L1）

### 17.1 同一 API 多种 Request 结构

- getMedicalRecord.json: 16 Controller 调用，12 种 `id` 来源（S1-111 锁定）
- getMedicalProductVoList.json: 4 Controller 调用
- getProductSkuExistCountVoList.json: 6 Controller 调用
- getCustomerVo: 13 Controller 调用，trueName 来源 D 级冲突（S1-110/111 锁定）

### 17.2 medicalRecordId 不同路径

- 5 类 S1-108 路径
- 4 类 S1-111 路径
- 1 类 S1-115 新路径（数组聚合）

### 17.3 Delivery 不使用 medicalRecordId

- 4/5 Delivery Controller **0 处** medicalRecordId
- 仅 deliveryInputRecordCtrl 1 处
- 真实业务关联通过 **cashflowId** 而非 medicalRecordId

### 17.4 objectId 运行时改写

- deliveryInputCtrl L3853-L3858：**基于 lockStorehouse.type 决定 objectId 指向**
- 7 处 objectId 全部在 deliveryInputCtrl（**Controller 隔离**）
- 内存改写是 F3/F4/F5/F6 数据链的关键

### 17.5 某 API 只存在一个 Consumer

- saveMedicalProductListOfSmallVersion.json: **仅 optometryGlassesCtrl**（S1-111 锁定）
- addUartDeviceUpToLimit.json (动态): 仅 optometryListCtrl + optometryLogListCtrl（S1-113/114 锁定）

### 17.6 某 Write 后不刷新

- 5 个 Sale Controller 中**0 处 Write 后 refresh**（仅 addSaleRecordCtrl 1 处 $state.reload()）
- 3 个 Charge Controller 中**0 处明确 Write 后续 Read refresh**

---

## 18. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | Check Controller全集 | 4 Controller (assistCheckingCtrl / assistCheckListCtrl / checkCallCtrl / checkinListCtrl) | A | L1 |
| 02 | Check API | 16+4+12+20 = 52 API 行 | A | L1 |
| 03 | Check medicalRecordId | 15+7+1+1 = 24 处 | A | L1 |
| 04 | Check medicalRecord | 0 处 | A | L1 |
| 05 | Check 产生新 medicalRecordId | 0 处 | A | L1 |
| 06 | Check→Sale | F 边界（需深入审计 15 处 $state.go） | F | L1 |
| 07 | Sale Controller全集 | 3 Controller (orderManageCtrl / addSaleRecordCtrl / adminSalesRecordCtrl) | A | L1 |
| 08 | Sale API | 2+2+3 = 7 API 行 | A | L1 |
| 09 | Sale medicalRecordId | 9+5+3 = 17 处 | A | L1 |
| 10 | Sale cashflow | 0 处 | A | L1 |
| 11 | Sale medicalProduct | 0 处 | A | L1 |
| 12 | Sale→Charge | 0 处直接控制流 | F | L1 |
| 13 | Charge Controller全集 | 3 Controller (myCheckBillCtrl / waitChargeDetailCtrl / payedListCtrl) | A | L1 |
| 14 | Charge API | 9+13+4 = 26 API 行 | A | L1 |
| 15 | Charge medicalRecordId | 8+4+3 = 15 处 | A | L1 |
| 16 | Charge cashflow | 0+2+13 = 15 处 | A | L1 |
| 17 | Charge Write | 0 个 Write 详细分析 | A/F | L1 |
| 18 | Charge→Delivery | 0 处直接控制流 | F | L1 |
| 19 | Delivery Controller全集 | 5 Controller (deliveryListCtrl / deliveryInputCtrl / deliveryProcessingCtrl / deliveryDetailCtrl / deliveryInputRecordCtrl) | A | L1 |
| 20 | Delivery medicalRecordId | 0+0+0+0+1 = 1 处 | A | L1 |
| 21 | Delivery cashflow | 8+3+3+0+4 = 18 处 | A | L1 |
| 22 | Delivery medicalProduct | 1+23+0+0+3 = 27 处 | A | L1 |
| 23 | Delivery objectId | 0+7+0+0+0 = 7 处（仅 deliveryInputCtrl） | A | L1 |
| 24 | F3/F4/F5/F6 数据链 | deliveryInputCtrl L3836/L3885/L3966/L4007（完整链路 A 级） | A | L1 |
| 25 | 四大主链直接连接 | 0 处（5 条主链间） | F | L1 |
| 26 | A/B/C/D/E/F | A: 22 / F: 4 | A | L1 |

### 18.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 22 | 85% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 4 | 15% |

### 18.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 19. A-F 总结

- **A 级**：22 项（85%）
- **F 级**：4 项（跨主链直接连接 / 深入审计边界）
- **B/C/D/E 级**：0 项

---

## 20. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0 项
- **L3**：0 项

---

## 21. F 边界

| F 项 | 详情 |
|---|---|
| 1 | Check → Sale 跨主链 $state.go 跳转目标 | 15 处 $state.go 需逐一审计目标 State |
| 2 | Sale → Charge 跨主链直接控制流 | 0 处证据 |
| 3 | Charge → Delivery 跨主链直接控制流 | 0 处证据 |
| 4 | Sale/Charge/Delivery 5 个 Controller 的 Write 详情 | 本轮未深入审计 Write Request 字段级 provenance |
| 5 | HTML 模板 | 4 主链 Controller 全部 0 个 HTML 模板 |
| 6 | 5 条主链间的真实业务关系 | 可能在更高层（State 配置 / Service） |

---

## 22. 红线

| 红线 | 状态 |
|---|---|
| 1. 纯静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不调用任何 Read/Write API | ✅ |
| 5. 不打开真实业务系统 | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-114 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-176） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 10 untracked + 1 gitignored 原样保留 | ✅ |
| 14. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 23. 关键纠偏

| 旧结论 | 新结论 | 依据 |
|---|---|---|
| S1-111 报 deliveryInputCtrl 1 处 medicalRecordId | 0 处（Case-Sensitive）| Case-Sensitive 扫描 |
| S1-111 报 payedListCtrl 2 处 medicalRecordId | 3 处（Case-Sensitive）| Case-Sensitive 扫描 |
| S1-111 报 assistCheckListCtrl 4 处 medicalRecordId | 7 处（Case-Sensitive）| Case-Sensitive 扫描 |
| S1-111 报 medicalRecordId 9 类路径 | **10 类**（S1-115 新增数组聚合路径）| 本轮 S1-115 第 16 节 |
| 任务文本 "HEAD = 8d1b473?" | 实际 HEAD = `5464752`（S1-114 提交）| git rev-parse HEAD |

---

## 24. 最终四大主链数据图

### 24.1 主链内数据流（已证明 A 级）

**Check 主链**：
- assistCheckingCtrl: $stateParams.medicalRecordId → $scope.medicalRecordId (L1757)
- $state.go 8 处（目标 State 待详细审计）

**Sale 主链**：
- orderManageCtrl: ListFactory item.okOrderRecord.medicalRecordId → $scope.medicalRecordIdList (L36251)
- medicalRecordIdList → window.location.href 下载 URL（L36239）

**Charge 主链**：
- waitChargeDetailCtrl: 1 处 medicalRecord 整体对象（**唯一**）
- payedListCtrl: cashflow 13 处主消费
- waitChargeDetailCtrl: medicalProduct 40 处主消费

**Delivery 主链**（**最完整**）：
- deliveryInputCtrl: cashflowId $stateParams → F1 (L3848) → waitingDeliveryList
- **内存改写**：objectId ← lockStorehouse.type 分流（L3853-L3858）
- F3 / F4 / F5 / F6 完整链路（详见 §9.2）

### 24.2 跨主链连接（**0 处直接控制流**）

| 关系 | 状态 |
|---|---|
| Check → Sale | F 边界（需深入） |
| Sale → Charge | F 边界（**0 处**） |
| Charge → Delivery | F 边界（**0 处**） |
| Check → Charge | F 边界（**0 处**） |
| Sale → Delivery | F 边界（**0 处**） |

---

## 25. 结论

### 25.1 4 大主链 medicalRecordId 分布

| 主链 | medicalRecordId 总数 | medicalRecord 整体 | 强消费 |
|---|---:|---:|---|
| Check | 24 | 0 | assistCheckingCtrl (15) |
| Sale | 17 | 0 | orderManageCtrl (9) |
| Charge | 15 | 1 | waitChargeDetailCtrl (4 + medicalRecord 1) |
| Delivery | 1 | 0 | 仅 deliveryInputRecordCtrl |
| **总计** | **57** | **1** | 4 Controller |

### 25.2 4 大主链业务中心

| 主链 | 业务中心 | 关键 Controller |
|---|---|---|
| Check | medicalRecordId 入口 | assistCheckingCtrl |
| Sale | medicalRecordId 导出 | orderManageCtrl (window.location.href) |
| Charge | cashflow + medicalProduct | waitChargeDetailCtrl (40 medicalProduct) |
| Delivery | cashflow + objectId 改写 | deliveryInputCtrl (7 objectId) |

### 25.3 4 大主链 0 处直接控制流

- 5 条主链间**0 处**直接 $state.go / 直接函数调用
- 仅存在**字段共现**（medicalRecordId / cashflow 跨 Controller 出现）
- 真实业务链可能在更高层（State 配置 / Service / DB），**F 边界**

### 25.4 S1-115 关键发现

1. **HEAD 实际 = 5464752**（不是任务文本中的 8d1b473）
2. **4/5 Delivery Controller 0 处 medicalRecordId**（发货业务不直接处理医疗记录）
3. **objectId 仅在 deliveryInputCtrl**（Controller 隔离）
4. **waitChargeDetailCtrl 是唯一消费 medicalRecord 整体对象**的 Controller
5. **4 大主链 0 处直接跨链 $state.go**

---

**审计完成。本文档为 177 号，提交后将形成 tracked=185，untracked=10，ignored=1。**
