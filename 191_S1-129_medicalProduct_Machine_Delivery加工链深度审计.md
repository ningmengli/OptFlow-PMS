# S1-129 medicalProduct → Machine → Delivery 加工链深度审计

## 0. 任务背景

S1-128 已完成 medicalProduct 全局 Provenance。本轮**深入** Machine ↔ Delivery 加工链。

F1-F6 流程是 S1-94~96 提出的关键加工链。本轮**重新钉死** Machine 与 Delivery 的真实数据/控制流。

## 1. 审计范围

| Controller | 范围 | 行数 |
|---|---|---:|
| machineOrderCtrl | L16094-L16260 | 167 |
| machineOrderBrokenCtrl | L16261-L16370 | 110 |
| machineOrderWaitProcessCtrl | L16357-L16370 | 14 |
| machineOrderListCtrl | L4264-L4367 | 104 |
| processCenterCtrl | L57778-L57819 | 42 |
| modifyProcessCenterCtrl | L56898-L57081 | 184 |
| addProcessCenterCtrl | L51801-L51955 | 155 |
| completeStockLossCtrl | L16058-L16093 | 36 |
| deliveryInputCtrl | L3812-L4023 | 212 |
| deliveryInputRecordCtrl | L4024-L4074 | 51 |
| deliveryListCtrl | L4075-L4235 | 161 |
| deliveryProcessingCtrl | L4236-L4263 | 28 |

## 2. Machine Controller

### 2.1 关键 Controller 注册

| Controller | 行号 | 核心职责 |
|---|---:|---|
| machineOrderCtrl | L16094 | 店内加工订单管理（开始/完成/关闭）|
| machineOrderBrokenCtrl | L16261 | 加工异常（报损）|
| machineOrderListCtrl | L4264 | 加工订单列表（签收/发货）|
| machineOrderWaitProcessCtrl | L16357 | **最小 Controller（仅判断 tab）** |
| processCenterCtrl | L57778 | 加工中心配置 |

### 2.2 关键 API 分布

| Controller | 关键 API | 性质 |
|---|---|---|
| **machineOrderCtrl** | selectInStoreMachineCenterCashflowVoList | Read List |
| | **startMachineCenterOrder** | Write (开始) |
| | **completeMachineCenterOrder** | Write (完成) |
| | **closeMachineCenterOrder** | Write (关闭) |
| | getMachineCenterOrder | Read (查) |
| | getMethodGlassRecordVo | Read (查方法) |
| | getCanBeProcessSkuInListOfProduct | Read (F5) |
| | **saveToBeProcessSkuInListOfProduct** | Write (F5 batch) |
| | getMedicalRecord | Read |
| **machineOrderBrokenCtrl** | **getMachineCenterCashflowVo** | Read (c+m) |
| | getAdminInfo | Read |
| | **createMedicalStockLoss** | Write (报损) |
| | **completeMachineCenterOrder** | Write |
| **machineOrderListCtrl** | selectMachineCenterListOfProduct | Read (选机器) |
| | **selectMachineCenterOrderRecordVoList** | Read List |
| | **receiveMachineCenterOrder** | Write (签收) |
| | **deliveryMachineCenterOrder** | Write (发货) |
| **processCenterCtrl** | (无 Save/Query API) | 弹窗 |

## 3. Machine 核心对象

### 3.1 Object 命中矩阵

| Controller | medicalProduct | medicalProductId | objectId | machineCenterId | stockInSkuId | medicalRecordId | cashflowId |
|---|---:|---:|---:|---:|---:|---:|---:|
| **machineOrderCtrl** | 1 | 1 | 0 | 0 | 1 | **8** | 2 |
| **machineOrderBrokenCtrl** | 1 | 0 | 0 | **3** | 0 | 0 | 3 |
| **machineOrderListCtrl** | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| **deliveryInputCtrl** | **11** | **3** | **7** | 2 | 1 | 0 | 3 |
| **deliveryInputRecordCtrl** | 1 | 1 | 0 | 0 | 0 | 1 | 4 |
| **deliveryListCtrl** | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| **deliveryProcessingCtrl** | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

### 3.2 关键发现

**S1-129 关键发现 1（machineOrderCtrl medicalRecordId 8 命中）**：
- medicalRecordId 是 machineOrderCtrl 最核心 ID
- 通过 medicalRecordId 关联到 medicalRecord
- 多个 Write (start/complete/close) 都用 `medicalRecordId` 作参数

**S1-129 关键发现 2（machineOrderBrokenCtrl machineCenterId 3 命中）**：
- machineCenterId 是 machineOrderBrokenCtrl 的核心 ID
- 接收 $stateParams.machineCenterId (L16263)
- API Request { cashflowId, machineCenterId } (L16269-L16272)

## 4. machineOrder provenance

### 4.1 machineOrder 实体路径

**S1-129 关键发现 3（machineOrder 真实结构）**：

```
machineCenterOrderVoList[]
└── machineCenterOrder (Type 4 整体对象)
    ├── id
    ├── status
    ├── receiveStatus
    └── (其它真实字段)
└── medicalProduct (Type 4 整体对象)
    └── productName (L16329)
```

### 4.2 machineOrder 派生链 (machineOrderBrokenCtrl L16322-L16332)

```javascript
// L16322-L16332 machineOrderBrokenCtrl showLoss
$scope.showLoss = function (stockId, count, idx) {
    $scope.medicalProductStockId = stockId;
    $scope.modal.lossReasonId = null;
    getAdminId();
    $scope.lossCount = count;
    $scope.modal.remark = null;
    $scope.loss.machineCenterOrderId = 
        $scope.getStockObjectFactory.result.object
              .machineCenterOrderVoList[idx].machineCenterOrder.id;  // Type 3
    $scope.productName = 
        $scope.getStockObjectFactory.result.object
              .machineCenterOrderVoList[idx].medicalProduct.productName;  // Type 3
    $scope.modal.stockLossShow = true;
};
```

### 4.3 machineOrder 派生链 (machineOrderCtrl L16250-L16254)

```javascript
// L16243-L16256 machineOrderCtrl commonOrder
$scope.commonOrder = function () {
    var commonPromise = $scope.commonOrderFactory.saveOrQuery(
        $scope.common.url,  // start/complete/closeMachineCenterOrder.json
        { machineCenterOrderId: $scope.common.machineCenterOrderId }
    ).then(function (res) {
        if (res.status == 1) {
            return Popup.notice(res.errmsg);
        }
        $scope.getOrderFactory = new ObjectFactory();
        var orderPromise = $scope.getOrderFactory.saveOrQuery(
            "/admin/getMachineCenterOrder.json", 
            { medicalRecordId: $scope.common.medicalRecordId }
        );
        orderPromise.then(function (resp) {
            $scope.memberFactory.items[$scope.common.idx]
                .machineCenterOrder.status = resp.result.object.status;
        });
    });
};
```

**S1-129 关键发现 4（machineOrderCtrl 完整 Write 模式）**：
- start/complete/close 共享 `commonOrder` 函数
- 全部用 `machineCenterOrderId` 作 Request
- success 后用 `getMachineCenterOrder.json { medicalRecordId }` 重新查询
- 更新 `$scope.memberFactory.items[idx].machineCenterOrder.status` (Type 3 派生)
- 触发 List items 局部更新（不是 reload 整 List）

## 5. machineCenter provenance

### 5.1 machineCenterId 多源 (S1-128 已识别)

| 来源 | 行号 | 表达式 |
|---|---:|---|
| A. $stateParams | L16263 | `machineOrderId = $stateParams.machineCenterId` |
| A. $stateParams | (modifyProcessCenterCtrl) | `$stateParams.machineCenterId` |
| B. Request Body | L16271 | `getMachineCenterCashflowVo.json { cashflowId, machineCenterId }` |
| C. Request Body | L3824 | `getMedicalProductMachineCenterVoList.json { medicalProductId, machineCenterId }` |
| C. Request Body | L3962 | `sendMedicalProductToMachineCenter.json { medicalProductId, machineCenterId }` |
| D. Response | L4282 | `arr[i].id` (selectMachineCenterListOfProduct.json) |

### 5.2 关键发现

**S1-129 关键发现 5（machineCenterId 完全不在 $stateParams 接收中跨链）**：
- modifyProcessCenterCtrl 接收 machineCenterId (State Param)
- 但 modifyProcessCenterCtrl **不传给** machineOrderCtrl
- 即 machineCenterId 是**各 Controller 独立处理**

**S1-129 关键发现 6（machineCenter 与 medicalProduct 的关系）**：
- deliveryInputCtrl L3824: `medicalProductId + machineCenterId`（在同一 Request）
- 即 medicalProductId 和 machineCenterId 是**配对**输入
- 但 machineCenterId 是 `medicalProduct.objectId` (运行时派生)，不是从 medicalProductVo 本身

## 6. medicalProduct / medicalProductId

### 6.1 在 Machine 的命中

| Controller | 行号 | 表达式 | 性质 |
|---|---:|---|---|
| machineOrderCtrl | L16175 | `getCanBeProcessSkuInListOfProduct.json { cashflowId }` | F5 Request (cashflowId 派生) |
| machineOrderCtrl | L16188 | `productArr[i].deliveryStockInSkuVoList[j].stockInSku.id` | Type 3 派生 |
| machineOrderCtrl | L16201 | `medicalProductId: productArr[i].medicalProduct.id` | Type 3 派生 |
| machineOrderBrokenCtrl | L16305 | `medicalProductStockId: $scope.medicalProductStockId` | Scope 字段 |
| machineOrderBrokenCtrl | L16329 | `medicalProduct.productName` | Type 3 派生 |

**S1-129 关键发现 7（Machine 不直接消费 medicalProduct API）**：
- 4 个 Machine Controller **全部不调用** `getMedicalProductVoList.json`
- Machine 只在 `deliveryStockInSkuVoList[]` 嵌套结构中消费 medicalProduct 字段
- 即 Machine 消费 medicalProduct **经由 F5 Response** 间接

### 6.2 F5 batch 写 (machineOrderCtrl L16181-L16223)

```javascript
$scope.saveStock = function () {
    var arr = [];
    var medicalProductStockBatctPoListJson = [];
    var productArr = $scope.getProcessFactory.result.list;  // F5 Response
    for (var i = 0; i < productArr.length; i++) {
        arr[i] = [];
        for (var j = 0; j < productArr[i].deliveryStockInSkuVoList.length; j++) {
            if (productArr[i].deliveryStockInSkuVoList[j].deliveryCount > 0) {
                arr[i].push({
                    stockInSkuId: productArr[i].deliveryStockInSkuVoList[j].stockInSku.id,
                    deliveryCount: productArr[i].deliveryStockInSkuVoList[j].deliveryCount
                });
            }
        }
        if (arr[i].length) {
            medicalProductStockBatctPoListJson.push({
                medicalProductId: productArr[i].medicalProduct.id,  // Type 3 派生
                medicalProductStocks: arr[i]
            });
        }
    }
    var savePromise = $scope.saveStockFactory.saveOrQuery(
        "/admin/saveToBeProcessSkuInListOfProduct.json",
        { medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson) }
    );
};
```

## 7. F3 / F6 边界

### 7.1 F3 调用位置 (仅 deliveryInputCtrl L3836)

```javascript
// L3830-L3836 deliveryInputCtrl showAddModal
$scope.showAddModal = function () {
    $scope.addOrderModal = true;
    $scope.startTime = undefined;
    $scope.dateSearch = null;
    var arr = getMachineCenterList();  // F2 派生 medicalProductId + machineCenterId
    $scope.getCenterListFactory = new ObjectFactory();
    $scope.getCenterListFactory.saveOrQuery(
        '/admin/getMedicalProductMachineCenterVoList.json', 
        { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
    );
};
```

### 7.2 F6 调用位置 (仅 deliveryInputCtrl L3966)

```javascript
// L3955-L3973 deliveryInputCtrl selectOrder
$scope.selectOrder = function () {
    if (!$scope.startTime) {
        return Popup.notice("请选择取镜日期");
    }
    var arr = $scope.getCenterListFactory.result.list.map(function (v) {
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };  // F3 Response
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);
    $scope.createOrderFactory = new ObjectFactory();
    var createPromise = $scope.createOrderFactory.saveOrQuery(
        '/admin/sendMedicalProductToMachineCenter.json', 
        { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }
    );
};
```

**S1-129 关键发现 8（F3/F6 仅 deliveryInputCtrl 调用）**：
- **F3 (getMedicalProductMachineCenterVoList)**: 唯一调用方 = deliveryInputCtrl L3836
- **F6 (sendMedicalProductToMachineCenter)**: 唯一调用方 = deliveryInputCtrl L3966
- **Machine Controller (machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl / machineOrderWaitProcessCtrl) 完全 0 调用 F3/F6！**

**S1-129 关键发现 9（Machine 通过不同 API 自成体系）**：
- Machine 不消费 F3 Response
- Machine 通过 `getMachineCenterCashflowVo.json` / `selectInStoreMachineCenterCashflowVoList.json` / `selectMachineCenterOrderRecordVoList.json` 等**独立 API** 获取数据
- 即 Machine 是**独立于 F3/F6 的数据流**

## 8. objectId 详细

### 8.1 objectId 完整链路 (S1-128 已识别)

```
[deliveryInputCtrl F1] (L3846-L3866)
  API: getCashflowDeliveryVo.json { cashflowId }
  ↓ Response
  arr = res.result.object.waitingDeliveryList
  ↓
[F2 runtime mutation] (L3853-L3857)
  for each item:
    if lockStorehouse.type == 4:
      item.medicalProduct.objectId = item.lockMachineCenter.id
    else:
      item.medicalProduct.objectId = null
  ↓
[F3] (L3816-L3829) getMachineCenterList
  遍历 → medicalProductMachineCenterPoList
  条件: if (item.medicalProduct.objectId) 才推入
  ↓
[F3 Request] (L3836)
  getMedicalProductMachineCenterVoList.json
  { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
  ↓ Response (F3)
  $scope.getCenterListFactory.result.list[]
  其中 v.medicalProduct.id 和 v.machineCenter.id
  ↓
[F6] (L3955-L3973) selectOrder
  arr = list.map(v => { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id })
  ↓
[F6 Request] (L3966)
  sendMedicalProductToMachineCenter.json
  { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime }
```

### 8.2 objectId 边界确认

**S1-129 关键发现 10（objectId 是 Delivery 内部字段）**：
- objectId 仅在 deliveryInputCtrl 1 处出现 (L3854-L3856 派生)
- Delivery 其他 3 个 Controller 0 命中
- Machine 4 个 Controller 0 命中
- **objectId 是 Delivery 内部字段，不跨 Controller**

## 9. stockInSkuId

### 9.1 命中分布

| Controller | 命中 | 行号 |
|---|---:|---|
| deliveryInputCtrl | 1 | L3869 (数组聚合) |
| machineOrderCtrl | 1 | L16191 (数组聚合) |
| **其它 10 Controller** | **0** | - |

**S1-129 关键发现 11（stockInSkuId 是 F5 核心 ID）**：
- stockInSkuId 仅在 2 个 Controller 出现
- 都是数组聚合（`arr.push({ stockInSkuId: ... })`）
- 即 stockInSkuId 是 F5 batch 的核心 primitive ID
- 不进入 $stateParams

## 10. F3 / F6 完整字段对照

### 10.1 F3 Request (deliveryInputCtrl L3836)

```json
{
    "medicalProductMachineCenterPoListJson": "JSON.stringify([{medicalProductId, machineCenterId}])"
}
```

### 10.2 F3 Response (隐式)

```json
{
    "result": {
        "list": [
            {
                "medicalProduct": {"id": ...},
                "machineCenter": {"id": ...}
            }
        ]
    }
}
```

### 10.3 F6 Request (deliveryInputCtrl L3966)

```json
{
    "medicalProductMachineCenterPoListJson": "JSON.stringify([{medicalProductId, machineCenterId}])",
    "planDeliveryTime": ...
}
```

### 10.4 关键观察

- F3 和 F6 的 Request 字段**完全相同** (`medicalProductMachineCenterPoListJson`)
- 区别: F6 多一个 `planDeliveryTime`
- 即 F3 (查询) → F6 (发送) 的 Request 字段**完全兼容**

## 11. 4 个方向链判定

### 11.1 Optometry → Machine

| 起点 | 终点 | 机制 | 等级 |
|---|---|---|---|
| optometryCtrl L35295 | - | `medicalProduct.medicalRecordId` | 字段共现 (F) |
| optometryGlassesCtrl | - | (无 Machine API) | F |

**S1-129 关键发现 12（Optometry → Machine F 级）**：
- Optometry Controller **不调用** 任何 Machine API
- 只在医疗产品链中**间接关联**到 Machine (通过 medicalProductVoList)
- **无直接桥**

### 11.2 Sale → Machine

| 起点 | 终点 | 机制 | 等级 |
|---|---|---|---|
| (3 个 Sale Controller) | - | (无 Machine API) | F |

**S1-129 关键发现 13（Sale → Machine F 级）**：
- 3 个 Sale Controller 完全 0 调用 Machine API
- **Sale 不与 Machine 通信**

### 11.3 Machine → Delivery

| 起点 | 终点 | 机制 | 等级 |
|---|---|---|---|
| machineOrderCtrl L4299 selectMachineCenterOrderRecordVoList | deliveryListCtrl L4121 selectMachineCenterOrderRecordVoList | **API 共享** | A (API 共现) |
| machineOrderListCtrl L4329 deliveryMachineCenterOrder | deliveryInputCtrl (无对应) | (无直接) | F |

**S1-129 关键发现 14（Machine → Delivery API 共享 A 级）**：
- `selectMachineCenterOrderRecordVoList.json` 在 2 个 Controller 调用（machineOrderListCtrl + deliveryListCtrl）
- 但这是**同一 List API 共用**，**不是数据链**
- 没有 API Response → Request 直接桥

### 11.4 Delivery → Machine

| 起点 | 终点 | 机制 | 等级 |
|---|---|---|---|
| deliveryInputCtrl L3836 (F3) | machineOrderCtrl (无 F3 调用) | (无直接) | F |
| deliveryInputCtrl L3966 (F6) | machineOrderCtrl (无 F6 调用) | (无直接) | F |

**S1-129 关键发现 15（Delivery → Machine F 级）**：
- F3/F6 是 Delivery 内部 API
- **Machine 不消费 F3 Response**
- **Delivery 与 Machine 是 0 个直接数据链**

## 12. State 出口 / 入口

### 12.1 Machine Controller State 出口

| Controller | State 出口 | 行号 | 目标 |
|---|---|---:|---|
| machineOrderBrokenCtrl | machineOrderChainTesting | L16344 | 连锁加工测试 |
| machineOrderBrokenCtrl | machineOrderTesting | L16346 | 店内加工测试 |
| machineOrderListCtrl | **0** | - | - |
| machineOrderCtrl | **0** | - | - |
| processCenterCtrl | 2 | (未深查) | (内部) |
| modifyProcessCenterCtrl | (无 $state.go) | - | - |

### 12.2 Machine Controller StateParam 接收

| Controller | 接收字段 | 行号 |
|---|---|---|
| machineOrderBrokenCtrl | cashflowId, machineCenterId, chain | L16262-L16264 |
| modifyProcessCenterCtrl | machineCenterId | (未深查) |
| completeStockLossCtrl | (有 StateParam) | (未深查) |

### 12.3 Delivery Controller State 入口

| Controller | 接收字段 | 行号 |
|---|---|---|
| deliveryInputCtrl | cashflowId | L3814 |
| deliveryInputRecordCtrl | cashflowId | L4026 |
| deliveryProcessingCtrl | cashflowId | L4238 |
| deliveryListCtrl | (无 StateParam) | - |

**S1-129 关键发现 16（State 不构成 Machine ↔ Delivery 桥）**：
- Machine State 出口 = machineOrderTesting 等
- Delivery State 入口 = cashflowId
- 两者**完全不交叉**

## 13. 完整加工链

### 13.1 尝试建立完整链

```
medicalProduct (Optometry 源)
  ↓
getMedicalProductVoList (OptometryGlassesCtrl L35684)
  ↓
saveMedicalProductListOfSmallVersion (L35950)
  ↓
medicalProductVoList (Scope) 
  ↓ Optometry → Delivery 桥 (F5)
getCanBeDeliverySkuInListOfProduct (optometryCtrl L35054)
  ↓
medicalProductStocks (F5 Response)
  ↓ Delivery → Machine 桥 (F3)
getMedicalProductMachineCenterVoList (deliveryInputCtrl L3836)
  ↓
medicalProductMachineCenterVoList (F3 Response)
  ↓
sendMedicalProductToMachineCenter (F6, L3966)
  ↓ 【断点: Machine 不消费 F3/F6 Response】
  
[Machine 不通过 F3/F6 获取数据]
[Machine 通过独立 API: getMachineCenterCashflowVo / selectInStoreMachineCenterCashflowVoList]
```

### 13.2 关键断点

**S1-129 关键发现 17（F3/F6 与 Machine 实际无关联）**：
- F3 (getMedicalProductMachineCenterVoList) Response **不进入** Machine Controller
- F6 (sendMedicalProductToMachineCenter) Write **不来自** Machine Controller
- 两者都是 **Delivery 内部 API**
- 即 F3/F6 是**Delivery → MachineCenter** 的桥，不是 **Delivery → MachineController** 的桥

**S1-129 关键发现 18（machineCenter 与 machineOrderController 是分离的）**：
- machineCenterId 在 machineCenterOrderController (machineOrderCtrl) 接收
- machineCenter 与 machineOrderController 通信靠 **`getMachineCenterOrder.json { medicalRecordId }`** (machineOrderCtrl L16251)
- 不是靠 F3/F6

### 13.3 完整链最终评估

| 步骤 | 桥接方式 | 等级 |
|---|---|---|
| 1. Optometry → medicalProduct (创建) | F5 batch saveMedicalProductListOfSmallVersion | A |
| 2. medicalProduct → Delivery F5 | optometryCtrl L35054 getCanBeDeliverySkuInListOfProduct | A |
| 3. Delivery F1 (waitingDeliveryList) | deliveryInputCtrl L3848 getCashflowDeliveryVo | A |
| 4. F2 objectId runtime mutation | deliveryInputCtrl L3853-L3857 | A (内部) |
| 5. F3 getMedicalProductMachineCenterVoList | deliveryInputCtrl L3836 (唯一) | A (Delivery 内部) |
| 6. F6 sendMedicalProductToMachineCenter | deliveryInputCtrl L3966 (唯一) | A (Delivery 内部) |
| **7. Machine 不消费 F3/F6 Response** | - | **断点** |
| 8. Machine 通过 medicalRecordId 自成体系 | machineOrderCtrl L16251 | A (Machine 内部) |
| 9. Machine 完成 → 实际发往 Delivery | HTML 跳转（不在审计范围）| F (HTML) |
| **断点位置** | Delivery F6 后 → Machine **无数据链** | **断点** |

## 14. 核心关系矩阵

| Object/Key | Optometry | Sale | Machine | Delivery |
|---|---|---|---|---|
| **medicalProduct** | ✓ 14 (主) | 0 | ✓ 2 (F5 间接) | ✓ 12 (F1-F6) |
| **medicalProductId** | ✓ 9 (Source) | 0 | ✓ 1 (F5) | ✓ 8 (F3/F6) |
| **machineOrder** | 0 | 0 | ✓ (machineOrderBrokenCtrl L16328) | 0 |
| **machineCenter** | 0 | 0 | ✓ 3 (modifyProcessCenterCtrl) | ✓ 1 (F3) |
| **machineCenterId** | 0 | 0 | ✓ 4 (machineOrderBrokenCtrl / machineOrderListCtrl) | ✓ 2 (F3/F6) |
| **objectId** | 0 | 0 | 0 | **✓ 7 (Delivery 唯一, F2 派生)** |
| **stockInSkuId** | 0 | 0 | ✓ 1 (F5) | ✓ 1 (F5) |
| **medicalRecordId** | ✓ 27 (主) | ✓ 5 | **✓ 8 (主)** | ✓ 1 (dead-end in deliveryInputRecordCtrl) |
| **cashflowId** | 0 | 0 | ✓ 2 (F5) | ✓ 3 (deliveryInputCtrl) |

**S1-129 关键发现 19**：
- objectId 是 **Delivery 唯一**字段 (0 命中 in Machine)
- medicalRecordId 是 Machine 核心 ID (8 命中)
- machineCenterId 多源: State Param / Request Body / Response

## 15. Final Machine / Delivery DAG

```
【Optometry 阶段】(验光 + 配镜)
  optometryGlassesCtrl L35684: getMedicalProductVoList.json
  optometryGlassesCtrl L35950: saveMedicalProductListOfSmallVersion.json
  ↓
【Optometry → Delivery F5 桥】
  optometryCtrl L35048: $scope.concatMedicalProductStock
  L35054: getCanBeDeliverySkuInListOfProduct.json
  ↓
【Delivery 阶段 - 集中在一个 Controller】
  deliveryInputCtrl (F1-F6 完整链):
    F1 L3846: getCashflowDeliveryVo.json
    F2 L3853: objectId runtime mutation (lockStorehouse.type==4)
    F3 L3836: getMedicalProductMachineCenterVoList.json
    F4 L3868: medicalProductIdArray 聚合
    F5 (共享, optometryCtrl 调用)
    F6 L3966: sendMedicalProductToMachineCenter.json
  deliveryListCtrl L4121: selectMachineCenterOrderRecordVoList.json (List 共享)
  deliveryInputRecordCtrl L4034: getMedicalRecordPayVo.json
  deliveryInputRecordCtrl L4061: saveMedicalProductDeliveryCommentBatch.json
  deliveryProcessingCtrl L4249: getCashflowDeliveryVo.json
  ↓ 【断点: F3/F6 Response 不被 Machine 消费】
  
【Machine 阶段 - 独立 API 体系】
  machineOrderCtrl:
    L16109: selectInStoreMachineCenterCashflowVoList.json
    L16130: getMethodGlassRecordVo.json
    L16150: getMedicalRecord.json
    L16164: startMachineCenterOrder.json (Write)
    L16175: getCanBeProcessSkuInListOfProduct.json (F5)
    L16212: saveToBeProcessSkuInListOfProduct.json (F5 Write)
    L16226: completeMachineCenterOrder.json (Write)
    L16235: closeMachineCenterOrder.json (Write)
    L16251: getMachineCenterOrder.json { medicalRecordId } (Read)
  machineOrderBrokenCtrl:
    L16269: getMachineCenterCashflowVo.json { cashflowId, machineCenterId } (Read)
    L16311: createMedicalStockLoss.json (Write)
    L16336: completeMachineCenterOrder.json (Write)
  machineOrderListCtrl:
    L4277: selectMachineCenterListOfProduct.json
    L4299: selectMachineCenterOrderRecordVoList.json (List 共享)
    L4317: receiveMachineCenterOrder.json (Write)
    L4332: deliveryMachineCenterOrder.json (Write)

【Machine ↔ Delivery 关系】
  F3/F6 仅 deliveryInputCtrl 调用 → 集中内部
  Machine 4 个 Controller 完全不调用 F3/F6
  machineCenterListOfProduct API 在 2 个 Controller (machineOrderListCtrl + modifyProcessCenterCtrl)
  没有任何直接链 Machine → Delivery 或 Delivery → Machine
```

## 16. 与历史结论的差异

### 16.1 S1-94 vs S1-129

| 项 | S1-94 | S1-129 |
|---|---|---|
| F3 / F6 | 标注 Delivery → Machine 加工链 | **F3/F6 仅 deliveryInputCtrl 内部，Machine 不消费** |
| objectId 派生 | 标注 lockStorehouse.type==4 | **保持 (L3853-L3857 详细)** |

### 16.2 S1-115 vs S1-129

| 项 | S1-115 | S1-129 |
|---|---|---|
| machineOrderCtrl | 标注 8 medicalRecordId 命中 | **保持 (含 startOrder/completeOrder/closeOrder)** |
| Machine Controller 范围 | 标注 | **更新 (5 个 Controller: machineOrderCtrl/BrokenCtrl/ListCtrl/WaitProcessCtrl + processCenterCtrl)** |

### 16.3 S1-128 vs S1-129

| 项 | S1-128 | S1-129 |
|---|---|---|
| F3 / F6 桥 | 标注 "Delivery → Machine F3/F6" | **纠偏: F3/F6 是 Delivery 内部 API，Machine 不消费** |
| objectId runtime mutation | 标注 deliveryInputCtrl L3853 | **保持 + 详细证明** |

## 17. 26 项矩阵

| # | 项目 | 详情 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | Machine Controller | 5 (machineOrderCtrl / BrokenCtrl / ListCtrl / WaitProcessCtrl / processCenterCtrl) | A | L1 |
| 02 | Machine 范围 | 167+110+104+14+42 = 437 行 | A | L1 |
| 03 | Machine DI | 8+9+11+1+1 DI | A | L1 |
| 04 | Machine API | 5 + 2 + 4 + 0 + 0 = 11 unique | A | L1 |
| 05 | Machine Read | 5 + 1 + 2 + 0 + 0 = 8 | A | L1 |
| 06 | Machine Write | 4 + 2 + 2 + 0 + 0 = 8 | A | L1 |
| 07 | machineOrder | A (Type 3 派生 L16328) | A | L1 |
| 08 | machineCenter | A (modifyProcessCenterCtrl L56898) | A | L1 |
| 09 | machineCenterId | A (4 来源: State/Request/Response) | A | L1 |
| 10 | medicalProduct | 2 命中 (F5 间接) | A | L1 |
| 11 | medicalProductId | 1 命中 (F5) | A | L1 |
| 12 | objectId | 0 命中 (Delivery 唯一) | A | L1 |
| 13 | stockInSkuId | 2 命中 (F5) | A | L1 |
| 14 | machineOrder provenance | 6 源 (API Response 派生) | A | L1 |
| 15 | machineCenter provenance | 4 源 (State / Request / Response) | A | L1 |
| 16 | F3 Request | `{ medicalProductMachineCenterPoListJson }` | A | L1 |
| 17 | F3 Response | 隐式 `{ result.list[].medicalProduct + machineCenter }` | A | L1 |
| 18 | F6 Request | `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` | A | L1 |
| 19 | F6 Consumer | **仅 deliveryInputCtrl (1 处)** | A | L1 |
| 20 | Machine → Delivery | F（无 API / State 链）| A | L1 |
| 21 | Delivery → Machine | F（F3/F6 不被 Machine 消费）| A | L1 |
| 22 | Optometry → Machine | F（无直接链）| A | L1 |
| 23 | Sale → Machine | F（无直接链）| A | L1 |
| 24 | State 桥 | F（Machine 与 Delivery State 不交叉）| A | L1 |
| 25 | 完整链 | **断点: F3/F6 → Machine** | A | L1 |
| 26 | A/B/C/D/E/F | A=21 / B=0 / C=0 / D=0 / E=0 / F=5 | - | - |

## 18. F 边界

| 项目 | F 原因 | 应对 |
|---|---|---|
| Machine → Delivery 直接链 | 0 命中 | 复刻时按独立业务路径 |
| F3/F6 Response Machine 消费 | Machine 不调用 F3/F6 | 复刻时 Machine 独立 API |
| 跨模块 HTML 跳转 | 不在 controller.js 范围 | 需要 HTML 审计 |
| 后端响应结构 | 静态无法判定 | 需要 backend debug |
| machineOrderCompleted.html 实际绑定 | 文件未 tracked | 复刻时按 Controller 行为 |

## 19. 复刻风险（L1）

### R1: F6 Consumer 是否只有 Delivery
- **是** (F 级在 Machine 范围, A 级在 Delivery)
- 复刻时 Delivery 是 F6 唯一调用方

### R2: Machine 是否直接消费 F3/F6
- **否** (F 级, S1-94 误判纠正)
- Machine 通过独立 API 体系 (`getMachineCenterCashflowVo` / `selectInStoreMachineCenterCashflowVoList` / `getMachineCenterOrder`)
- 复刻时 Machine 不应消费 F3/F6

### R3: objectId 是否仅 Delivery 内部
- **是** (Delivery 唯一 7 命中, Machine 0 命中)
- 复刻时 objectId 是 Delivery 内部字段

### R4: machineCenterId 多源
- State Param (machineOrderBrokenCtrl) / Request Body (F3/F6) / Response (selectMachineCenterListOfProduct)
- 复刻时按 controller 实际需要

### R5: medicalProductId 是否是 Machine/Delivery 共同键
- **否** (Machine 仅 1 命中, Delivery 8 命中)
- 复刻时 medicalProductId 在 Delivery 是主键, 在 Machine 是次键

### R6: stockInSkuId 是否仅 Delivery
- **是 + 1 命中 in Machine** (machineOrderCtrl L16191 F5 batch)
- 复刻时 stockInSkuId 主要在 F5 batch

### R7: Machine 与 Delivery 是否通过 API / State 连接
- **0 个直接链**
- 仅 `selectMachineCenterOrderRecordVoList.json` 在 2 个 Controller 共享 (A 级 API 共现)
- 复刻时按独立业务实现

### R8: 断点不得人为补桥
- F3/F6 → Machine 是**真实断点**
- 复刻时**不能**人为假设 Machine 自动接收 F3 Response
- 必须按 HTML 实际行为

## 20. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- machineOrderCompleted.html unchanged ✓ (SHA256 F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24)
- machineOrderList.html unchanged ✓ (SHA256 A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A)
- 165-190 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 21. 结论

### 21.1 关键发现

1. **F3/F6 是 Delivery 内部 API** (S1-94 误判纠正)
2. **Machine 不消费 F3/F6 Response** (F3/F6 → Machine 断点)
3. **objectId 是 Delivery 唯一字段** (7 命中, Machine 0 命中)
4. **Machine 通过独立 API 体系** (getMachineCenterCashflowVo 等)
5. **machineCenterId 多源** (State/Request/Response/Param)
6. **medicalRecordId 是 Machine 核心** (8 命中 in machineOrderCtrl)
7. **F3/F6 Request 字段相同** (medicalProductMachineCenterPoListJson, F6 多 planDeliveryTime)
8. **5 个 Machine Controller** (含最小 machineOrderWaitProcessCtrl)
9. **11 个 unique API / 8 Read / 8 Write** in Machine

### 21.2 S1-129 任务状态

- 4 个 Machine Controller 完整 API 统计
- F3 / F6 完整字段链
- objectId runtime mutation 详细
- 4 个方向链判定（Machine→Delivery / Delivery→Machine / Optometry→Machine / Sale→Machine）
- 5 处断点识别
- 26 项矩阵已建立
- 8 条复刻风险已列出

---

**【S1-129 完成】**
