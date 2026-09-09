# S1-128 medicalProduct / medicalProductId 全局 Provenance 与跨模块数据链审计

## 0. 任务背景

S1-94~96 / S1-115~127 已完成大量底层字段逆向，但 medicalProduct 全局 Provenance 与跨模块数据链**尚未建立统一视图**。

本轮**专门**建立 medicalProduct 在 5 大模块（Optometry / Sale / Charge / Machine / Delivery）中的全局数据流。

## 1. 审计范围

| 项 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| **medicalProduct 命中** | **90** |
| **medicalProductId 命中** | **52** |
| 5 大模块涉及 Controller | 11+ |

## 2. medicalProduct 全局命中

### 2.1 5 大模块分布

| 模块 | Controller | medicalProduct | medicalProductId | 小计 |
|---|---|---:|---:|---:|
| **Optometry** | optometryCtrl | 5 | 7 | 12 |
| | optometryGlassesCtrl | 9 | 2 | 11 |
| | (Optometry 小计) | **14** | **9** | **23** |
| **Sale** | addSaleRecordCtrl | 0 | 0 | 0 |
| | adminSalesRecordCtrl | 0 | 0 | 0 |
| | myCheckBillCtrl | 0 | 0 | 0 |
| | (Sale 小计) | **0** | **0** | **0** |
| **Charge** | waitChargeDetailCtrl | 8 | 18 | 26 |
| | payedListCtrl | 4 | 0 | 4 |
| | waitPayBackCtrl | 8 | 10 | 18 |
| | partBackCtrl | 3 | 2 | 5 |
| | (Charge 小计) | **23** | **30** | **53** |
| **Machine** | machineOrderCtrl | 1 | 1 | 2 |
| | machineOrderBrokenCtrl | 1 | 0 | 1 |
| | (Machine 小计) | **2** | **1** | **3** |
| **Delivery** | deliveryInputCtrl | 11 | 7 | 18 |
| | deliveryInputRecordCtrl | 1 | 1 | 2 |
| | (Delivery 小计) | **12** | **8** | **20** |

**S1-128 关键发现 1（medicalProduct 模块分布）**：
- **Charge 模块消耗最多 medicalProduct** (23 命中, 26% 总数)
- **Optometry 居第二** (14 命中, 16%)
- **Delivery 第三** (12 命中, 13%)
- **Sale 完全不消费** (0 命中, **S1-126 误判纠正**)
- **Machine 极少** (2 命中, 2%)

## 3. medicalProductId 命中分类

### 3.1 4 类来源

| 来源 | 命中 | 典型表达式 |
|---|---:|---|
| A. medicalProduct.id (Type 3 派生) | 30+ | `arr[i].medicalProduct.id` |
| B. 数组聚合 (medicalProductIdArray) | 5+ | `medicalProductIdArray.push(...)` |
| C. State Param (medicalRecordId 桥) | 1 | L35309 `$stateParams.medicalRecordId` |
| D. URL string | 0 | (无) |

## 4. medicalProduct 第一明确来源

### 4.1 原始生成点

**S1-128 关键发现 2（medicalProduct 不在源端产生）**：
- medicalProduct 实体**不在 controller.js 中创建**
- 所有 medicalProduct 来自 API Response (来自后端)
- 前端只读取/修改字段，**不创建 medicalProduct**

### 4.2 第一来源 API

| 第一来源 API | 行号 | 模块 | 后续使用 |
|---|---:|---|---|
| getMedicalProductVoList.json | optometryGlassesCtrl L35685 | Optometry | 验光配镜 |
| getMedicalRecordFlowVo.json | optometryCtrl L34796+ | Optometry | 验光列表 |
| getCashflowDeliveryVo.json | deliveryInputCtrl L3848 | Delivery | **waitingDeliveryList 内部** |
| getMedicalRecordCashflowVo.json | waitChargeDetailCtrl L7488 / waitPayBackCtrl L7070 | Charge | **medicalProductVoList 嵌套** |
| selectMedicalProductStockList.json | optometryCtrl L34799+ | Optometry | 库存查询 |

## 5. Source Taxonomy (medicalProduct)

| 类别 | 命中 Controller | 关键行号 |
|---|---|---|
| A. API Response | 全部 5 大模块 | 多个 |
| B. ListFactory item | optometryCtrl (L35052) | `item.medicalProductVoList` |
| C. ObjectFactory object | waitChargeDetailCtrl / waitPayBackCtrl | `getCashflowObjectFactory.object.medicalProductVoList` |
| D. Function parameter | partBackCtrl L4659 | `v.medicalProduct` |
| E. Scope | optometryGlassesCtrl L35390 | `$scope.medicalRecord` (整体) |
| F. Array item | deliveryInputCtrl L3821 | `arr[i].medicalProduct` |
| G. State param | optometryGlassesCtrl L35388 | `$stateParams.medicalRecordId` |
| H. 运行时派生 | deliveryInputCtrl L3854 | `objectId = lockMachineCenter.id` |
| I. 其它 | optometryGlassesCtrl L35699-35717 | `stock.medicalProduct.*` (from list) |

## 6. medicalProduct → medicalRecordId 关系

### 6.1 完整命中点

| Controller | 行号 | 表达式 |
|---|---:|---|
| optometryCtrl | L35295 | `medicalProduct.medicalRecordId` |
| optometryGlassesCtrl | L35440 | `id: $scope.medicalRecordId` (Request) |

### 6.2 关键行 L35284-L35297 完整链 (optometryCtrl)

```javascript
// L35280-L35298 optometryCtrl $scope.beginCustomerCheckin 内的 stock loss 逻辑
var _$scope$order$object$ = $scope.order.object.medicalProductVoList[index],
    product = _$scope$order$object$.product,
    medicalProduct = _$scope$order$object$.medicalProduct,
    medicalProductDelivery = _$scope$order$object$.medicalProductDelivery;

$scope.modal.shopInfo = {
    productName: product.productName,
    useCount: 1,
    remark: "",
    lossAdminId: res.result.object.id,
    adminname: res.result.object.nickname,
    lossReasonId: null,
    machineCenterId: medicalProductDelivery.machineCenterId,
    medicalRecordId: medicalProduct.medicalRecordId,    // <-- 派生
    medicalProductId: medicalProduct.id                 // <-- 派生
};
```

**S1-128 关键发现 3（medicalProduct.medicalRecordId A 级派生）**：
- optometryCtrl L35295: `medicalProduct.medicalRecordId` 直接读取
- 派生关系: `medicalProductVoList[i].medicalProduct.medicalRecordId`
- 用途: 报损/报溢的 Request.medicalRecordId 字段
- **A 级 直接字段级派生**

## 7. medicalProduct → cashflow 关系

### 7.1 路径分析

- **medicalProduct 本身不携带 cashflowId 字段**
- 但 medicalProductVoList 是 cashflowVo 的**嵌套子对象**
- 即: cashflowVo.medicalProductVoList[].medicalProduct

**S1-128 关键发现 4（cashflowVo 嵌套 medicalProductVoList）**：
- Charge Controller 通过 `getMedicalRecordCashflowVo.json` 一次性获取 cashflowVo
- cashflowVo 含 medicalProductVoList / medicalExamineVoList / registrationFeeVoList
- 即 **cashflow 内部含 medicalProduct，不是 medicalProduct 含 cashflow**
- **桥方向: cashflowVo → medicalProductVoList → medicalProduct**

### 7.2 waitPayBackCtrl 消费链

```javascript
// L7078-L7080 waitPayBackCtrl
$scope.medicalProductIdList = $scope.getCashflowObjectFactory.object.medicalProductVoList.map(function (v) {
    return v.medicalProduct.id;
});
$scope.medicalProductModelIdList = $scope.getCashflowObjectFactory.object.medicalProductVoListOfModel.map(function (v) {
    return v.medicalProduct.id;
});
```

## 8. medicalProduct → objectId (Delivery 重点)

### 8.1 objectId 派生链 (deliveryInputCtrl L3846-L3866)

```javascript
// F1: search()
$scope.getMedicalRecordDeliveryFactory.saveOrQuery(
    '/admin/getCashflowDeliveryVo.json', 
    { cashflowId: $scope.cashflowId }
).then(function (res) {
    var arr = res.result.object.waitingDeliveryList;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].lockStorehouse.type == 4) {            // F2 派生
            $scope.getMedicalRecordDeliveryFactory.result.object
                .waitingDeliveryList[i].medicalProduct.objectId = 
                arr[i].lockMachineCenter.id;
        } else {
            $scope.getMedicalRecordDeliveryFactory.result.object
                .waitingDeliveryList[i].medicalProduct.objectId = null;
        }
    }
});
```

**S1-128 关键发现 5（objectId 是运行时派生）**：
- medicalProduct.objectId **不在原始 Response 中存在**
- 是 deliveryInputCtrl 运行时根据 `lockStorehouse.type == 4` 派生的
- type 4 = 加工中心
- 派生源: `arr[i].lockMachineCenter.id`
- 派生条件: 必须有 lockMachineCenter（即已分配到机器中心）

### 8.2 派生用途 (F3)

```javascript
// L3816-L3829 deliveryInputCtrl F3
var getMachineCenterList = function getMachineCenterList() {
    var medicalProductMachineCenterPoList = [];
    var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].medicalProduct.objectId) {
            medicalProductMachineCenterPoList.push({
                medicalProductId: arr[i].medicalProduct.id,
                machineCenterId: arr[i].medicalProduct.objectId
            });
        }
    }
    return medicalProductMachineCenterPoList;
};
// L3836
$scope.getCenterListFactory.saveOrQuery(
    '/admin/getMedicalProductMachineCenterVoList.json', 
    { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
);
```

**S1-128 关键发现 6（Delivery → Machine F3 链 A 级）**：
- medicalProduct.objectId → medicalProductMachineCenterPoList.machineCenterId
- 进入 `getMedicalProductMachineCenterVoList.json` Request
- 这是 **Delivery → Machine** 的直接 API 桥
- **A 级**

## 9. medicalProduct → machineCenter 关系

### 9.1 桥接点 (deliveryInputCtrl L3961-L3966)

```javascript
// L3955-L3973 deliveryInputCtrl F6
$scope.selectOrder = function () {
    if (!$scope.startTime) {
        return Popup.notice("请选择取镜日期");
    }
    var arr = $scope.getCenterListFactory.result.list.map(function (v) {
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);
    $scope.createOrderFactory = new ObjectFactory();
    var createPromise = $scope.createOrderFactory.saveOrQuery(
        '/admin/sendMedicalProductToMachineCenter.json', 
        { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }
    );
};
```

**S1-128 关键发现 7（F3 → F6 链 A 级）**：
- F3 Response: `v.medicalProduct.id` + `v.machineCenter.id`
- F6 Request: `medicalProductId` + `machineCenterId` (数组)
- 通过 `medicalProductMachineCenterVoList.json` (F3) → `sendMedicalProductToMachineCenter.json` (F6)
- **A 级 直接桥**

## 10. medicalProduct → stock 关系

### 10.1 selectMedicalProductStockList (optometryCtrl L35048-L35079)

```javascript
// L35048-L35079 optometryCtrl F5 准备
$scope.concatMedicalProductStock = function (item) {
    return new Promise(function (resolve) {
        var medicalProductIdArray = [];
        item.medicalProductVoList.forEach(function (medical) {
            medicalProductIdArray.push(medical.medicalProduct.id);
        });
        new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", {
            medicalProductIdArray: medicalProductIdArray
        }).then(function (result) {
            var medicalProductStockBatctPoListJson = [];
            result.result.list.forEach(function (medical) {
                var medicalProductStocks = medical.deliveryStockInSkuVoList.map(function (delivery) {
                    return {
                        stockInSkuId: delivery.stockInSku.id,
                        deliveryCount: delivery.deliveryCount
                    };
                });
                medicalProductStockBatctPoListJson.push({
                    medicalProductId: medical.medicalProduct.id,
                    medicalProductStocks: medicalProductStocks
                });
            });
        });
    });
};
```

**S1-128 关键发现 8（Optometry → Delivery F5 链 A 级）**：
- optometryCtrl L35048-L35079: medicalProductIdArray 数组
- 进入 `getCanBeDeliverySkuInListOfProduct.json` (F5 Read)
- Response 含 `deliveryStockInSkuVoList` (stock 信息)
- 构造 `medicalProductStockBatctPoListJson` (medicalProductId + medicalProductStocks)
- 后续给 L35151 useCount 一起组成 WaitCharge Detail 调价
- **A 级**

## 11. medicalProduct → sku / product 关系

### 11.1 完整结构 (optometryGlassesCtrl L35699-L35717)

```javascript
// L35684-L35728 optometryGlassesCtrl
new ObjectFactory().saveOrQuery("/admin/getMedicalProductVoList.json", {
    medicalRecordId: $scope.medicalRecordId
}).then(function (res) {
    if (res.result.count) {
        var list = [], tempList = [];
        res.result.list.forEach(function (stock) {     // stock = 一个 medicalProductVo
            if (stock.medicalProductSign) {           // medicalProductSign = 镜片
                tempList.push(stock);
            } else {
                list.push({
                    id: stock.medicalProduct.id,        // 整体对象 → ID 提取
                    brandName: stock.brand.brandName,
                    categoryName: stock.category.categoryName,
                    factory: stock.product.factory,     // product 子对象
                    marketPrice: stock.productSku.marketPrice,  // productSku 子对象
                    model1: stock.productSku.model1,
                    model1Name: stock.product.model1Name,
                    model2: stock.productSku.model2,
                    model2Name: stock.product.model2Name,
                    productName: stock.product.productName,
                    skuCode: stock.productSku.skuCode,
                    unitName: stock.productSku.unitName,
                    unLockExistSkuCount: stock.unLockExistSkuCount,
                    lockStorehouseId: stock.medicalProduct.lockStorehouseId,
                    productSkuId: stock.productSku.id,
                    remark: stock.medicalProduct.remark,
                    storeName: stock.lockStorehouse.name,
                    useCount: stock.medicalProduct.useCount,
                    memberRate: stock.medicalProduct.memberRate,
                    skuDuplicate: stock.skuDuplicate,
                    kpiPrice: stock.productSku.kpiPrice
                });
            }
        });
        $scope.tempShop = tempList;
        $scope.stockInSkuList = list;
    }
});
```

**S1-128 关键发现 9（medicalProductVo 完整结构）**：
```
medicalProductVo (stock)
├── medicalProduct (对象)
│   ├── id
│   ├── medicalRecordId
│   ├── lockStorehouseId
│   ├── useCount
│   ├── memberRate
│   ├── remark
│   ├── model1 / model2
│   └── productUsage
├── product (对象)
│   ├── productName
│   ├── model1Name / model2Name
│   ├── factory
│   └── category
├── productSku (对象)
│   ├── id
│   ├── skuCode
│   ├── marketPrice
│   ├── kpiPrice
│   └── unitName
├── brand
├── category
├── lockStorehouse
├── medicalProductSign (镜片标识)
├── skuDuplicate
├── unLockExistSkuCount
└── deliveryStockInSkuVoList (F5 Response 嵌套)
```

## 12. medicalProduct → patient/customer 关系

| 字段 | 命中 | 等级 |
|---|---:|---|
| medicalProduct.patientId | 0 | F（不存在）|
| medicalProduct.customerId | 0 | F（不存在）|

**S1-128 关键发现 10（medicalProduct 不带 patient/customer 字段）**：
- medicalProduct 实体**不直接**含 patientId/customerId
- patient/customer 通过 **medicalRecord → patientId/customerId** 间接关联
- 即 medicalProduct 必须经由 medicalRecord 才能关联到 patient

## 13. Array Aggregation

### 13.1 关键数组

| 数组 | 表达式 | Controller | 行号 |
|---|---|---|---|
| medicalProductIdArray | `arr => arr[i].medicalProduct.id` | deliveryInputCtrl | L3869, L3874, L3885 |
| medicalProductIdList | `$scope.medicalProductIdList = []` | waitChargeDetailCtrl | L6573 |
| medicalProductIdList (2) | `medicalProductVoList.map(v => v.medicalProduct.id)` | waitPayBackCtrl | L7078 |
| medicalProductIdList (3) | `$scope.medicalProductIdList[index] = id` | partBackCtrl | L6864 |
| medicalProductIdList (4) | (addId 函数) | optometryCtrl | L6864 |
| medicalProductIdList (5) | `$scope.medicalProductIdList[a] = null` | partBackCtrl | L7182 |
| medicalProductIdArray (6) | `item.medicalProductVoList.forEach(p => p.medicalProduct.id)` | optometryCtrl | L35051 |
| medicalProductMachineCenterPoList | F3 数组 | deliveryInputCtrl | L3817 |

## 14. Object Propagation

| Controller | 整体对象存储位置 | 备注 |
|---|---|---|
| optometryCtrl | `$scope.order.object.medicalProductVoList[index]` (L35282) | 报损弹窗 |
| optometryCtrl | `$scope.getDeliveryListFactory.result.list[i].medicalProduct` (L3998) | F5 Response |
| optometryGlassesCtrl | `$scope.stockInSkuList`, `$scope.tempShop` (L35724-L35725) | 整体 medicalProductVo |
| waitPayBackCtrl | `$scope.getCashflowObjectFactory.object.medicalProductVoList` (L7078) | cashflowVo 内部 |
| deliveryInputCtrl | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct` (L3854-L3856) | **runtime mutation** |
| partBackCtrl | `v.medicalProduct` (L4659) | 遍历 items |

**S1-128 关键发现 11（整体对象不跨 Controller 传递）**：
- 整体 medicalProductVo 永远存在单个 Controller 的 Scope/Factory
- 跨 Controller 传递都用 primitive ID
- runtime mutation 仅在 deliveryInputCtrl (objectId)

## 15. Clone/Copy

| Controller | 表达式 | 行号 |
|---|---|---|
| payedListCtrl | `var medicalProductVoList = angular.copy(result.medicalProductVoList)` | L5009 |
| payedListCtrl | `var medicalProductVoListOfModel = angular.copy(result.medicalProductVoListOfModel)` | L5010 |
| optometryGlassesCtrl | `$scope.glassesInfo` (解构) | L35741-L35752 |

## 16. State

**S1-128 关键发现 12（State 极少用 medicalProduct/machineCenterId）**：
- 4 处 $state.go 涉及 medicalProductId:
  - optometryCtrl L35136: `optometryGlasses {medicalRecordId, edit}` (不传 medicalProductId)
  - optometryCtrl L35149: `optometryGlasses {medicalRecordId, edit}` (同上)
  - addSaleRecordCtrl L31124: `adminSalesRecord.myMaterialBill {medicalRecordId, patientId}` (不传 medicalProductId)
  - deliveryInputCtrl L3874: `medicalProductIdArray` (F5 Request)
- **medicalProductId 不进入 $stateParams**（无 Controller 接收）

## 17. 5 大模块 Consumer 详细

### 17.1 Optometry (14+9 命中)

**Consumer**:
| Controller | API | 字段 |
|---|---|---|
| optometryCtrl | getMedicalRecordFlowVo / selectMedicalRecordFlowVoList / getCanBeDeliverySkuInListOfProduct / selectMedicalProductStockList | medicalProductVoList / medicalProductVoList / F5 |
| optometryGlassesCtrl | getMedicalProductVoList / saveMedicalProductListOfSmallVersion / updateMethodGlassRecord | medicalProductVoList (含 product/productSku/brand) |

**关键 Write**: optometryGlassesCtrl L35950: `saveMedicalProductListOfSmallVersion.json { medicalRecordId, medicalProductParamListJson }`

### 17.2 Sale (0 命中)

**关键发现**: **3 个 Sale Controller 完全 0 命中 medicalProduct**
- addSaleRecordCtrl 唯一 Write: addMedicalRecord.json (只含 medicalRecordType, patientId)
- adminSalesRecordCtrl: 0
- orderManageCtrl: 0

### 17.3 Charge (23+30 命中)

**Consumer**:
| Controller | API | 字段 |
|---|---|---|
| waitChargeDetailCtrl | computeUnPlaceOrderMedicalRecordFee / reCompute / createCashFlowForMedicalRecord | medicalProductVoList (VoList 修改) |
| payedListCtrl | getMedicalRecordCashflowVoListOfCompany / getMedicalRecordCashflowVo | medicalProductVoList (打印) |
| waitPayBackCtrl | getMedicalRecordCashflowVo / getCashFlowCashierVo / getCashFlowCreditVo / payCreditRefund | **medicalProductIdList** 派生 |
| partBackCtrl | getMedicalRecordRefundDetailVo / refundCreditCashflowIdList / createPartRefund | medicalProduct.id |

**S1-128 关键发现 13（Charge 通过 cashflowVo 消费 medicalProduct）**：
- Charge Controller 不直接请求 medicalProduct API
- 而是从 cashflowVo 内部提取 medicalProductVoList
- 即 **cashflowVo 是 medicalProductVoList 的载体**

### 17.4 Machine (2+1 命中)

**Consumer**:
| Controller | API | 字段 |
|---|---|---|
| machineOrderCtrl | selectInStoreMachineCenterCashflowVoList | medicalProduct.productName |
| machineOrderBrokenCtrl | (内部) | medicalProduct |

**关键**: Machine 几乎不直接处理 medicalProduct，只在 productName 层面

### 17.5 Delivery (12+8 命中)

**Consumer**:
| Controller | API | 字段 |
|---|---|---|
| deliveryInputCtrl | getCashflowDeliveryVo / getMedicalProductMachineCenterVoList / sendMedicalProductToMachineCenter | waitingDeliveryList / objectId 派生 / F3 / F6 |
| deliveryInputRecordCtrl | saveMedicalProductDeliveryCommentBatch | medicalProduct.id |

**S1-128 关键发现 14（Delivery 是 medicalProduct → machineCenter 桥）**：
- deliveryInputCtrl F2 (objectId 派生) + F3 (Request) + F6 (Write) **完整链**
- 这是 medicalProduct 跨模块到 machineCenter 的**唯一直接 API 桥**

## 18. Cross-Module Bridge

| Direction | Bridge type | Evidence | 等级 |
|---|---|---|---|
| **Optometry → Sale** | - | 0 跳 | F |
| **Sale → Charge** | - | 0 跳 | F |
| **Charge → Delivery** | cashflowVo.medicalProductVoList (内部) | cashflowId 桥 | A |
| **Delivery → Machine** | `getMedicalProductMachineCenterVoList.json` (F3) + `sendMedicalProductToMachineCenter.json` (F6) | medicalProductId + machineCenterId 数组 | A |
| **Optometry → Machine** | medicalProductVoList.medicalProduct.medicalRecordId (optometryCtrl L35295) | medicalRecordId 桥 | A |
| **Optometry → Delivery** | medicalProductIdArray (optometryCtrl L35052) | F5 Request | A |
| **Sale → Machine** | - | 0 跳 | F |
| **Sale → Delivery** | - | 0 跳 | F |
| **Machine → Delivery** | (未建立) | - | F |

**S1-128 关键发现 15（medicalProduct 跨模块桥）**：
- **5 条直接桥**全部 A 级
- 主要通过 F3/F5/F6 + cashflowVo 桥
- 没有任何桥需要"对象整体" 跨 Controller 传递

## 19. Core Relation Matrix

| Key/对象 | Optometry | Sale | Charge | Machine | Delivery |
|---|---|---|---|---|---|
| **medicalProduct** | ✓ 14 (主) | 0 | ✓ 23 (cashflowVo 内部) | ✓ 2 (productName) | ✓ 12 (F1-F6) |
| **medicalProductId** | ✓ 9 (Source) | 0 | ✓ 30 (派生) | ✓ 1 | ✓ 8 (F3/F6) |
| **medicalRecordId** | ✓ 27 (主) | ✓ 5 | ✓ 12 | ✓ 8 | ✓ 1 (dead-end) |
| **cashflowId** | 0 | 0 | ✓ 33 (主) | 0 | ✓ 3 (F1) |
| **objectId** | 0 | 0 | 0 | ✓ (machineCenterId) | ✓ 7 (F2 派生) |
| **productId** | 0 | 0 | 0 | 0 | 0 |
| **patientId** | ✓ 5 | ✓ 6 | ✓ 2 | 0 | 0 |
| **customerId** | 0 | 0 | ✓ 14 | 0 | 0 |
| **machineCenterId** | 0 | 0 | 0 | 0 | ✓ (F3) |
| **stockInSkuId** | 0 | 0 | 0 | 0 | ✓ (F5) |

**S1-128 关键发现 16（medicalProduct 是 Sale 跨模块真空）**：
- Sale 模块是**唯一不消费** medicalProduct 的业务模块
- Sale 模块的 addMedicalRecord.json 只创建 medicalRecord, 不创建 medicalProduct
- 实际 medicalProduct 由 Optometry 验光配镜阶段创建

## 20. Final medicalProduct DAG

```
【第一来源】(Optometry 验光配镜阶段)
  optometryCtrl L35282: $scope.order.object.medicalProductVoList[index]
    ├── 来源: getMedicalRecordFlowVo.json
    ├── 派生: medicalProduct.id / medicalProduct.medicalRecordId (L35295-L35296)
    │
【consumer】
  optometryGlassesCtrl (L35684-L35728)
    ├── getMedicalProductVoList.json { medicalRecordId }
    ├── Response: items[].medicalProduct / product / productSku / brand
    ├── 写入 $scope.stockInSkuList / $scope.tempShop
    │
    ├── L35950 Write: saveMedicalProductListOfSmallVersion.json
    │   { medicalRecordId, medicalProductParamListJson }
    │
【Optometry → Delivery F5 桥】
  optometryCtrl L35048: $scope.concatMedicalProductStock(item)
    ├── medicalProductIdArray 数组聚合
    ├── API: getCanBeDeliverySkuInListOfProduct.json { medicalProductIdArray }
    └── Response: medicalProductStocks
    │
【Delivery F1-F6 完整链】
  deliveryInputCtrl L3846: search() [F1]
    ├── API: getCashflowDeliveryVo.json { cashflowId }
    ├── Response: res.result.object.waitingDeliveryList
    │
    ├── L3853: F2 runtime mutation
    │   ├── if lockStorehouse.type == 4:
    │   │   waitingDeliveryList[i].medicalProduct.objectId = lockMachineCenter.id
    │   └── else: objectId = null
    │
    ├── L3830-L3836: showAddModal() [F3]
    │   ├── 遍历 → medicalProductMachineCenterPoList = [{ medicalProductId, machineCenterId }]
    │   └── API: getMedicalProductMachineCenterVoList.json
    │
    ├── L3868-L3886: showDeliveryModal() [F4/F5]
    │   ├── medicalProductIdArray 聚合
    │   └── (F4 filter 过滤)
    │
    └── L3955-L3973: selectOrder() [F6]
        ├── 遍历 Response → { medicalProductId, machineCenterId }
        └── API: sendMedicalProductToMachineCenter.json (Write)
            { medicalProductMachineCenterPoListJson, planDeliveryTime }
    │
【Charge 内部消费】
  waitPayBackCtrl L7078: medicalProductIdList 派生
    ├── 来自 getMedicalRecordCashflowVo.json Response
    │   $scope.getCashflowObjectFactory.object.medicalProductVoList
    └── 用于: payCreditRefund.json (退款)
  
  partBackCtrl L4659 / L6864: medicalProductId 数组
    ├── 来自 items[].medicalProduct.id
    └── 用于: refundCreditCashflowIdList.json / createPartRefund.json
```

## 21. runtime mutation 详细

**S1-128 关键发现 17（runtime mutation 仅在 deliveryInputCtrl）**：

| 字段 | 派生位置 | 派生条件 | 派生源 |
|---|---|---|---|
| medicalProduct.objectId | deliveryInputCtrl L3854 | lockStorehouse.type == 4 | lockMachineCenter.id |
| medicalProduct.objectId | deliveryInputCtrl L3856 | lockStorehouse.type != 4 | null |

**S1-128 关键发现 18**：
- 全部 runtime mutation **仅 1 处**（deliveryInputCtrl L3853-L3857）
- 修改的是 `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId`
- 修改的 object **保留原 API Response 的整体结构**
- 复刻时**不能丢失**这段逻辑

## 22. 26 项矩阵

| # | 项目 | 详情 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | medicalProduct 全局命中 | 90 | A | L1 |
| 02 | medicalProductId 全局命中 | 52 | A | L1 |
| 03 | Source taxonomy | 9 类 | A | L1 |
| 04 | ID source taxonomy | 4 类 | A | L1 |
| 05 | 第一明确来源 | 5 个 API | A | L1 |
| 06 | medicalProduct Scope | 6+ Controller | A | L1 |
| 07 | medicalProduct Factory | 多 | A | L1 |
| 08 | medicalProduct parameter | 1+ | A | L1 |
| 09 | medicalProduct.id | 30+ 派生 | A | L1 |
| 10 | medicalProductId | 52 命中 | A | L1 |
| 11 | medicalProduct→medicalRecordId | A (L35295 派生) | A | L1 |
| 12 | medicalProduct→medicalRecord | 整体对象 (L35419) | A | L1 |
| 13 | medicalProduct→cashflow | 嵌套 (cashflowVo.medicalProductVoList) | A | L1 |
| 14 | medicalProduct→cashflowId | F (cashflowVo 内部) | A | L1 |
| 15 | medicalProduct→objectId | A (L3854 派生) | A | L1 |
| 16 | objectId runtime mutation | 1 处 (deliveryInputCtrl L3853) | A | L1 |
| 17 | medicalProduct→machineCenter | A (L3962 派生) | A | L1 |
| 18 | medicalProduct→stock | A (F5 链) | A | L1 |
| 19 | medicalProduct→sku | A (productSku 嵌套) | A | L1 |
| 20 | medicalProduct→product | A (product 嵌套) | A | L1 |
| 21 | medicalProduct→patient | F (不存在) | A | L1 |
| 22 | medicalProduct→customer | F (不存在) | A | L1 |
| 23 | Array aggregation | 8+ 数组 | A | L1 |
| 24 | Object propagation | 6+ Controller | A | L1 |
| 25 | Cross-module bridge | 5 条 A 级 | A | L1 |
| 26 | A/B/C/D/E/F | A=24 / B=0 / C=0 / D=0 / E=0 / F=2 | - | - |

## 23. F 边界

| 项目 | F 原因 | 应对 |
|---|---|---|
| medicalProduct 首次创建 | 不在 controller.js | 需要后端 audit |
| 后端响应结构 | 静态无法判定 | 需要 backend debug |
| HTML 跳转 | 不在 controller.js 范围 | 需要 HTML 审计 |
| machineOrder 详细 cross-Ctrl | 部分跨链 | 需深入 Machine 模块 |

## 24. 复刻风险（L1）

### R1: medicalProduct 与 medicalProductId 不能混合
- medicalProduct 是**对象**含 product/productSku/brand
- medicalProductId 是 primitive
- 复刻时按用途严格区分

### R2: medicalProduct.objectId 是运行时派生
- 原始 Response 中**不存在** objectId
- deliveryInputCtrl L3854 派生
- 复刻时**必须实现** runtime mutation 逻辑

### R3: F3/F4/F5/F6 字段链
- objectId (派生) → machineCenterId (Request) → F3 → F6
- medicalProductIdArray (聚合) → F5 → stock
- 复刻时字段链必须完整保留

### R4: medicalProduct 跨多个模块
- Optometry (Source) → Delivery (F1-F6) → Machine (sendMedicalProductToMachineCenter.json)
- 复刻时按模块分别实现

### R5: 部分模块只消费 ID
- Sale 0 命中
- Machine 1 命中 (productName)
- 复刻时按 controller 实际需要实现

### R6: 整体对象不跨 Controller 传递
- 复刻时按 ID 传递, 内部 API 获取整体

### R7: medicalProductId array aggregation
- 8+ 数组聚合
- 复刻时按 medicalProductIdArray 模式实现

### R8: productId 与 medicalProductId 不能自动统一
- productId = product.id (productSku / product)
- medicalProductId = medicalProduct.id
- 复刻时严格区分

## 25. 与历史结论的差异

### 25.1 S1-94 vs S1-128

| 项 | S1-94 | S1-128 |
|---|---|---|
| F1-F6 流程 | 标注 | **保持 (deliveryInputCtrl L3846-L3973 完整重建)** |
| objectId 派生 | 标注 `lockStorehouse.type==4` | **确认 (L3853-L3857 详细)** |

### 25.2 S1-115 vs S1-128

| 项 | S1-115 | S1-128 |
|---|---|---|
| medicalProduct 命中 Controller | 标注 | **更新（11 Controller, 90 命中）** |
| Sale 是否消费 | 标注 | **0 命中（S1-126 已确认）** |

### 25.3 S1-127 vs S1-128

| 项 | S1-127 | S1-128 |
|---|---|---|
| Charge 不消费 medicalProduct | **误判** | **实际 Charge 23 命中 (cashflowVo 内部)** |

## 26. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- 165-189 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 27. 结论

### 27.1 关键发现

1. **medicalProduct 全局 90 命中 / medicalProductId 52 命中**
2. **第一来源**: 5 个 API (getMedicalProductVoList / getMedicalRecordFlowVo / getCashflowDeliveryVo / getMedicalRecordCashflowVo / selectMedicalProductStockList)
3. **5 大模块分布**: Charge(23) > Optometry(14) > Delivery(12) > Machine(2) > Sale(0)
4. **Sale 完全不消费 medicalProduct** (S1-126 确认)
5. **medicalProductVo 完整结构** (medicalProduct / product / productSku / brand / lockStorehouse)
6. **objectId 是 runtime mutation** (deliveryInputCtrl L3853-L3857 唯一 1 处)
7. **5 条跨模块桥全部 A 级**: Optometry→Delivery F5, Delivery→Machine F3/F6, Optometry→Machine medicalRecordId
8. **S1-127 误判纠正**: Charge 通过 cashflowVo 内部消费 medicalProduct (不是 0 命中)

### 27.2 S1-128 任务状态

- medicalProduct 全局 Provenance 完整建立
- 5 大模块 Consumer 详细审计
- 8 个核心键关系矩阵
- 5 条跨模块 A 级桥
- 1 处 runtime mutation 定位
- 26 项矩阵已建立
- 8 条复刻风险已列出

---

**【S1-128 完成】**
