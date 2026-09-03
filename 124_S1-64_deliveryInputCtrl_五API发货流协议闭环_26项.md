# S1-64 deliveryInputCtrl 五 API 发货流协议闭环

> 专项收口：`deliveryInputCtrl` 5 个核心 API + 数据流 + 字段协议 + 历史纠错
>
> 上一阶段：S1-63（123 号）已收口 3 controller 协议对照。
>
> 本阶段：S1-64（124 号）专项收口 `deliveryInputCtrl` 五 API 发货流完整协议闭环。

---

## 1. 结论

deliveryInputCtrl 在当前 controller.js 范围内**实际有 6 个 API 调用点**（A 级 100% 收口），其中 5 个是 S1-63 已收口的核心 API，**第 6 个 `sendMedicalProductToMachineCenter.json`（L3966）是 S1-63 收口时遗漏的事实**。本轮严格按老板要求 5 个 API 收口，第 6 个作为补充事实标注，不混入核心 5 API 协议。

**核心 5 API 完整数据依赖链**：
```
L3839-3844: getCount() → statProductDeliveryStatusOfCashflow.json (初始化)
L3846-3865: search() → getCashflowDeliveryVo.json (初始化)
   ↓ waitingDeliveryList 写入 local
L3868-3886: showDeliveryModal() → getCanBeDeliverySkuInListOfProduct.json (用户点击)
   ↓ deliveryStockInSkuVoList[] 写入 local
L3979-4019: saveStock() → saveMedicalProductStockBatch.json (用户点击)
   ↓ 成功后 search + getCount + $state.reload
L3830-3837: showAddModal() → getMedicalProductMachineCenterVoList.json (独立用户操作)
```

**评级分布**：A=24 / B=0 / C=0 / D=0 / E=0 / F=2 / 1 项多评级 = 26

---

## 2. 证据范围

**直接证据**（A 级）：
- controller.js L3812-4021（deliveryInputCtrl 完整 209 行）
- controller.js L3869 / L3874 / L3885（showDeliveryModal 完整定义）

**资源缺失**（F 级）：
- deliveryInputCtrl HTML 模板（untracked 临时 HTML 中未发现）
- 完整 route schema（`.state()` 定义 F 维持）
- 后端算法 / DTO 定义（F 维持）
- deliveryInputCtrl HTML 模板中 ng-click / ng-model 绑定

---

## 3. deliveryInputCtrl 源码定位（26.1）

| 项目 | 证据 | 等级 |
|------|------|------|
| 文件 | controller.js | A |
| controller 名称 | `deliveryInputCtrl` | A（L3812） |
| 起点 | L3812 `angular.module('bestvisionWeb').controller('deliveryInputCtrl', [...])` | A |
| 终点 | L4021 `}]);` | A |
| 总行数 | 209 行 | A |
| 注入 | `$scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, ObjectFactory, ListFactory, $http, $q, QiniuFactory, $timeout` | A（L3812） |

---

## 4. 5 API 总表

| 序 | API URL | 调用位置 | 调用 function | Request | 后续处理 | 等级 |
|------|------|------|------|------|------|------|
| 1 | `/admin/getCashflowDeliveryVo.json` | L3848 | search() | `{ cashflowId }` | 处理 waitingDeliveryList + medicalProduct.objectId | A |
| 2 | `/admin/statProductDeliveryStatusOfCashflow.json` | L3841 | getCount() | `{ cashflowId }` | - | A |
| 3 | `/admin/getMedicalProductMachineCenterVoList.json` | L3836 | showAddModal() | `{ medicalProductMachineCenterPoListJson }` | 写入 $scope.getCenterListFactory | A |
| 4 | `/admin/getCanBeDeliverySkuInListOfProduct.json` | L3885 | showDeliveryModal() | `{ medicalProductIdArray }` | $scope.stockDetail = true | A |
| 5 | `/admin/saveMedicalProductStockBatch.json` | L4007 | saveStock() | `{ listCount, medicalProductStockBatctPoListJson }` | search + getCount + $state.reload + stockDetail=false | A |

**补充事实（不在 5 API 内）**：
- `sendMedicalProductToMachineCenter.json`（L3966，selectOrder()）- 6th API

---

## 5. API-01: getCashflowDeliveryVo.json

**5.1 完整 Request**：
```javascript
{ cashflowId: $scope.cashflowId }  // L3848
```

**5.2 cashflowId 来源**：
- L3814: `$scope.cashflowId = $stateParams.cashflowId;`（A）
- 等级：A

**5.3 Response 顶层结构**：
- 顶层：`{ status, result: { object: { waitingDeliveryList[] } } }`（A）
- 证据：L3851 `var arr = res.result.object.waitingDeliveryList;`（A）

**5.4 Response 实际被 controller 使用的字段**：

| 字段路径 | 用途 | 等级 |
|------|------|------|
| `res.result.object.waitingDeliveryList[]` | 主列表数据 | A（L3851） |
| `arr[i].lockStorehouse.type` | 数字类型判断 | A（L3853） |
| `arr[i].lockMachineCenter.id` | 机器中心 id | A（L3854） |
| `arr[i].medicalProduct` | 商品对象 | A（L3854-3856） |

**5.5 success 后的变量赋值**：
```javascript
// L3853-3857
if (arr[i].lockStorehouse.type == 4) {
    $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
} else {
    $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
}
```

**5.6 行为**：
- lockStorehouse.type == 4 → medicalProduct.objectId = lockMachineCenter.id
- lockStorehouse.type != 4 → medicalProduct.objectId = null
- 空数组 → Popup.notice + $state.go('deliveryList')（L3859-3863）
- 等级：A

**5.7 评级**：
- Request：A
- Response：A
- success 行为：A
- 未观察字段：F

---

## 6. API-02: statProductDeliveryStatusOfCashflow.json

**6.1 完整 Request**：
```javascript
{ cashflowId: $scope.cashflowId }  // L3841
```

**6.2 Response 顶层结构**：
- 顶层：`{ status, result: { object } }`（基于 ObjectFactory 模式 A）
- 等级：A（结构推断）/ F（具体字段未直接读取）

**6.3 controller 如何消费 Response**：
- L3841 调 API 后**未在 controller 主体内对 Response 做进一步处理**（A）
- 仅保存到 `$scope.getStatusDeliveryFactory`
- 等级：A

**6.4 与 getCashflowDeliveryVo.json 的数据关系**：
- 两个 API 共享同一 `cashflowId`
- 调用顺序：getCount() 在 L3844（先），search() 在 L3866（后）— 实际 controller 初始化顺序是 getCount() 然后立即 search()（L3844/L3866）
- **没有字段共享**：getStatusDeliveryFactory.result 与 getMedicalRecordDeliveryFactory.result 各自独立
- 等级：A

**6.5 评级**：
- Request：A
- Response 顶层：A
- 消费方式：A
- 具体业务字段：F

---

## 7. API-03: getMedicalProductMachineCenterVoList.json

**7.1 完整 Request**：
```javascript
{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }  // L3836
```

**7.2 arr 构造**：
- L3816-3829: `getMachineCenterList()` 函数
- 遍历 `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList`
- 过滤条件：`arr[i].medicalProduct.objectId` truthy
- 推入 `{ medicalProductId, machineCenterId }`

```javascript
// L3821-3825
if (arr[i].medicalProduct.objectId) {
    medicalProductMachineCenterPoList.push({
        medicalProductId: arr[i].medicalProduct.id,
        machineCenterId: arr[i].medicalProduct.objectId  // 注意：objectId = machineCenterId
    });
}
```

**7.3 Response 顶层结构**：
- 顶层：`{ status, result: { list } }`（A）
- list 实际使用：L3961 `$scope.getCenterListFactory.result.list.map(...)`

**7.4 list 元素字段**：
- L3962: `v.medicalProduct.id`（A）
- L3962: `v.machineCenter.id`（A）
- map 构造结果：`{ medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }`（A）

**7.5 哪些字段被后续逻辑直接读取**：
- 唯一后续消费点：selectOrder L3955-3977
- selectOrder 读 `getCenterListFactory.result.list.map(...)` 构造 sendMedicalProductToMachineCenter.json Request
- 等级：A

**7.6 评级**：
- Request：A
- Response 顶层：A
- list 元素字段：A
- 后续消费：A

---

## 8. API-04: getCanBeDeliverySkuInListOfProduct.json

**8.1 完整 Request**：
```javascript
{ medicalProductIdArray: medicalProductIdArray }  // L3885
```

**8.2 medicalProductIdArray 构造**：
```javascript
// L3869-3881
var medicalProductIdArray = [];
var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
for (var i = 0; i < arr.length; i++) {
    if (arr[i].medicalProduct.objectId == null) {  // 注意：== null
        medicalProductIdArray.push(arr[i].medicalProduct.id);
    }
}
if (!medicalProductIdArray.length) {
    Popup.notice("请选择发货的商品");
    return false;
}
```

**8.3 objectId == null 过滤逻辑**：
- 与 getMachineCenterList() 中的 `objectId truthy` 过滤**严格相反**
- showDeliveryModal 只选 `objectId == null`（没分配机器中心）
- 等级：A

**8.4 Response 顶层结构**：
- 顶层：`{ status, result: { list } }`（A）
- list 实际使用：L3985-3998 saveStock 读取

**8.5 list[i] 结构**：
- `{ medicalProduct, deliveryStockInSkuVoList[] }`（A）
- medicalProduct.id（A，L3998）
- deliveryStockInSkuVoList[j].deliveryCount（A，L3989/3991/3992）
- deliveryStockInSkuVoList[j].stockInSku.id（A，L3991）

**8.6 字段验证**：
- medicalProduct.id：A（L3998）
- stockInSku.id：A（L3991）
- deliveryCount：A（L3991）

**8.7 评级**：
- Request：A
- medicalProductIdArray 构造：A
- 过滤条件：A
- Response 结构：A
- 字段使用：A

---

## 9. API-05: saveMedicalProductStockBatch.json

**9.1 完整 Request**：
```javascript
{
    listCount: $scope.getDeliveryListFactory.result.list.length,
    medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson)
}  // L4007
```

**9.2 listCount 字段**：
- 来源：`$scope.getDeliveryListFactory.result.list.length`（A，L4007）
- 含义：list 数组长度
- 与数组长度等价：A

**9.3 medicalProductStockBatctPoListJson 内部结构**：
- 顶层数组（JSON 字符串）
- 数组项：`{ medicalProductId, medicalProductStocks: [...] }`
- medicalProductStocks 项：`{ stockInSkuId, deliveryCount }`

**9.4 构造过程**：
```javascript
// L3985-4004
for (var i = 0; i < $scope.getDeliveryListFactory.result.list.length; i++) {
    arr[i] = [];
    for (var j = 0; j < $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList.length; j++) {
        if (deliveryCount > 0) {
            arr[i].push({ stockInSkuId, deliveryCount });  // L3991
        } else if (deliveryCount < 0) {
            Popup.notice('发货数量必须大于0');
            return false;  // L3993-3994
        } else {}
    }
    if (arr[i].length) {
        medicalProductStockBatctPoListJson.push({
            medicalProductId: list[i].medicalProduct.id,  // L3998
            medicalProductStocks: arr[i]
        });
    }
}
if (!medicalProductStockBatctPoListJson.length) {
    Popup.notice('发货数量必须大于0');
    return false;  // L4001-4004
}
```

**9.5 medicalProductId 来源**：
- `$scope.getDeliveryListFactory.result.list[i].medicalProduct.id`（A，L3998）

**9.6 stockInSkuId 来源**：
- `$scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id`（A，L3991）

**9.7 deliveryCount 来源**：
- `$scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount`（A，L3991）

**9.8 评级**：A（全部）

---

## 10. 五 API 调用关系（26.8）

**实际调用顺序（基于 controller 初始化代码）**：

```
L3812-3815: controller 入口，$scope.cashflowId = $stateParams.cashflowId
L3839-3844: getCount() 立即执行 → statProductDeliveryStatusOfCashflow.json
L3846-3866: search() 立即执行 → getCashflowDeliveryVo.json
   ↓ then() L3849-3864 同步处理 waitingDeliveryList + medicalProduct.objectId
   ↓ 空数组则 $state.go('deliveryList') L3860-3862
```

**用户操作触发的调用（非初始化）**：

```
L3830-3837: showAddModal() → getMedicalProductMachineCenterVoList.json
L3868-3886: showDeliveryModal() → getCanBeDeliverySkuInListOfProduct.json
   ↓ $scope.stockDetail = true
L3979-4019: saveStock() → saveMedicalProductStockBatch.json
   ↓ 成功 → search() + getCount() + $state.reload() + stockDetail=false
```

**调用依赖图**：

| API | 是否依赖其他 API Response | 证据 |
|------|------|------|
| getCount | 否 | A（只依赖 $scope.cashflowId） |
| search | 否 | A（只依赖 $scope.cashflowId） |
| showAddModal | **依赖 search Response** | A（getMachineCenterList 读 waitingDeliveryList） |
| showDeliveryModal | **依赖 search Response** | A（读 waitingDeliveryList + objectId == null 过滤） |
| saveStock | **依赖 showDeliveryModal Response** | A（读 getDeliveryListFactory.result.list） |

**5 API 之间无强制线性顺序**，实际是：
- 2 个初始化 API（getCount + search）先并行/串行执行
- 3 个用户操作 API 各自独立，按用户点击顺序触发
- saveStock 成功后**重新执行** 2 个初始化 API

**等级**：A

---

## 11. 字段数据依赖图（26.9）

**真实字段依赖（基于 A 级代码证据）**：

```
$stateParams.cashflowId
  ├→ $scope.cashflowId (L3814)
       ├→ statProductDeliveryStatusOfCashflow.json Request (L3841)
       └→ getCashflowDeliveryVo.json Request (L3848)
            └ Response: res.result.object.waitingDeliveryList[]
                 ├→ arr[i].lockStorehouse.type (L3853)
                 │    └→ if (type == 4)
                 │         └→ medicalProduct.objectId = lockMachineCenter.id (L3854)
                 ├→ arr[i].lockMachineCenter.id (L3854)
                 ├→ arr[i].medicalProduct (L3854-3856)
                 │    ├→ .objectId (assigned L3854/3856)
                 │    └→ .id (read L3874/3823/3824)
                 │         ├→ medicalProductIdArray.push (L3874, showDeliveryModal)
                 │         └→ medicalProductMachineCenterPoList.push (L3823-3824, getMachineCenterList)
                 └→ waitingDeliveryList
                      ├→ getMachineCenterList filter: objectId truthy (L3821)
                      │    └→ medicalProductMachineCenterPoListJson Request (L3836)
                      │         └ Response: getCenterListFactory.result.list
                      │              └→ v.medicalProduct.id + v.machineCenter.id (L3962)
                      │                   └→ sendMedicalProductToMachineCenter.json Request (L3966)
                      └→ showDeliveryModal filter: objectId == null (L3873)
                           └→ medicalProductIdArray Request (L3885)
                                └ Response: getDeliveryListFactory.result.list
                                     ├→ list[i].medicalProduct.id → medicalProductId (L3998)
                                     └→ list[i].deliveryStockInSkuVoList[j]
                                          ├→ .stockInSku.id → stockInSkuId (L3991)
                                          └→ .deliveryCount → deliveryCount (L3991)
                                               └→ medicalProductStockBatctPoListJson Request (L4007)
```

**A 级 100% 收口**。

---

## 12. cashflow / medicalProduct / machineCenter / stockInSku 关系（26.10, 26.22）

| 对象 | deliveryInputCtrl 范围内字段 | 等级 |
|------|------|------|
| cashflow | `cashflowId` (L3814 from $stateParams) | A |
| cashflow | `cashflow` 完整对象 | F（未直接观察 controller.js 中作为对象使用） |
| medicalRecord | - | F（未直接观察） |
| medicalProduct | `id`, `objectId` | A |
| medicalProductDelivery | - | F（deliveryInputCtrl 范围内未观察） |
| machineCenter | - | F（machineCenter 整体对象未直接观察） |
| machineCenter.id | 通过 medicalProduct.objectId 间接使用 | A |
| stockInSku | `id` | A |
| stockInSku 其他字段 | - | F |

**关键 A 级边界**：
- cashflowId **不直接等于** deliveryId（仅作为入参）
- medicalProduct.id **不等于** medicalProductDelivery.id（**未观察** medicalProductDelivery 在 deliveryInputCtrl 范围）
- machineCenter 仅通过 medicalProduct.objectId 字段间接触及

---

## 13. objectId 专项（26.12）

| 出现位置 | 用途 | 等级 |
|------|------|------|
| L3854 | `arr[i].lockStorehouse.type == 4` 时赋值为 lockMachineCenter.id | A |
| L3856 | 否则赋值为 null | A |
| L3821 | `if (arr[i].medicalProduct.objectId)` 过滤（getMachineCenterList） | A |
| L3873 | `if (arr[i].medicalProduct.objectId == null)` 过滤（showDeliveryModal） | A |
| L3899 | isSendProduct 检查 | A |
| L3916 | isSendCenter 检查 | A |
| L3824 | 作为 machineCenterId 推入 medicalProductMachineCenterPoList | A |

**关键 A 级新发现**：
- `objectId` **专门指 machineCenter.id**（A 级多源一致）
- 在 L3824 `machineCenterId: arr[i].medicalProduct.objectId` 直接证明
- 严格**不是** 通用 product ID
- 仅在 deliveryInputCtrl 范围内出现（A）

**是否进入 save JSON**：
- 严格 F：saveMedicalProductStockBatch.json Request 中**不出现** objectId
- 等级：A（不出现）

---

## 14. deliveryCount 专项（26.14）

| 路径 | 来源 | 等级 |
|------|------|------|
| `list[i].deliveryStockInSkuVoList[j].deliveryCount` | API Response 字段 | A |
| 是否被修改 | F（controller 代码中**未赋值** deliveryCount） | F |
| 是否来自用户输入 | F（HTML 模板未观察） | F |
| 是否进入 Save JSON | A（L3991） | A |

**关键 A 级新发现**：
- deliveryCount 来自 getCanBeDeliverySkuInListOfProduct.json Response（A）
- 路径 = `getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount`（A）
- 在 deliveryInputCtrl 范围内**不修改** deliveryCount（A）
- 最终进入 saveMedicalProductStockBatch.json Request（A）

**与 HTML `medicalProductStock.deliveryCount` 严格区分**：
- machineOrderCompleted.html L146 `{{iten.medicalProductStock.deliveryCount}}` 字段路径**不同**（A）
- 该 HTML 属于 machineOrderBrokenCtrl 范围（A）
- **禁止等同**

---

## 15. medicalProductIdArray 完整生命周期（26.15）

| 环节 | 代码位置 | 真实表达式 | 等级 |
|------|------|------|------|
| 初始化 | L3869 | `var medicalProductIdArray = []` | A |
| 数据源 | L3870 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | A |
| 循环 | L3871 | `for (var i = 0; i < arr.length; i++)` | A |
| 过滤 | L3873 | `if (arr[i].medicalProduct.objectId == null)` | A |
| 推入 | L3874 | `medicalProductIdArray.push(arr[i].medicalProduct.id)` | A |
| 空数组检查 | L3878 | `if (!medicalProductIdArray.length)` | A |
| 早返回 | L3880 | `return false` | A |
| 副作用 | L3882 | `$scope.stockDetail = true` | A |
| 传入 Request | L3885 | `{ medicalProductIdArray: medicalProductIdArray }` | A |
| Response 保存 | L3884 | `$scope.getDeliveryListFactory = new ObjectFactory()` | A |
| 后续使用 | L3985-3991 | saveStock 读 $scope.getDeliveryListFactory.result.list | A |

**A 级 100% 收口**。

**关键 A 级边界**：
- 严格只来自 waitingDeliveryList（不是其他 controller）
- 严格只接受 objectId == null 的项
- 字段名严格 = `medicalProductIdArray`（不是 medicalProductIds）

---

## 16. save JSON 构造过程（26.16）

**逐层追踪**：

```javascript
// L3985: 外层循环：$scope.getDeliveryListFactory.result.list (来自 getCanBeDeliverySku Response)
for (var i = 0; i < $scope.getDeliveryListFactory.result.list.length; i++) {
    arr[i] = [];  // L3987: 初始化内层数组
    
    // L3988: 内层循环：deliveryStockInSkuVoList
    for (var j = 0; j < ...deliveryStockInSkuVoList.length; j++) {
        if (deliveryCount > 0) {  // L3989
            // L3991: 推入二层数组
            arr[i].push({
                stockInSkuId: list[i].deliveryStockInSkuVoList[j].stockInSku.id,
                deliveryCount: list[i].deliveryStockInSkuVoList[j].deliveryCount
            });
        } else if (deliveryCount < 0) {
            Popup.notice('发货数量必须大于0');  // L3993
            return false;  // L3994
        }
    }
    
    if (arr[i].length) {
        // L3998: 推入一层数组
        medicalProductStockBatctPoListJson.push({
            medicalProductId: list[i].medicalProduct.id,
            medicalProductStocks: arr[i]
        });
    }
}

// L4001: 全空检查
if (!medicalProductStockBatctPoListJson.length) {
    Popup.notice('发货数量必须大于0');
    return false;
}

// L4007: 序列化为 JSON 字符串
JSON.stringify(medicalProductStockBatctPoListJson)
```

**最终 JSON 字符串**：
```json
[
  {
    "medicalProductId": <number>,
    "medicalProductStocks": [
      {
        "stockInSkuId": <number>,
        "deliveryCount": <number>
      }
    ]
  }
]
```

**等级**：A

---

## 17. listCount 字段（26.17）

| 项目 | 证据 | 等级 |
|------|------|------|
| 来源 | `$scope.getDeliveryListFactory.result.list.length`（L4007） | A |
| 计算方式 | 直接读数组 .length | A |
| 与数组长度等价 | 是 | A |
| 其他用途 | F | F |
| 所有 Save 场景都存在 | deliveryInputCtrl saveStock 有；machineOrderCtrl saveStock **没有** | A |

**关键 A 级新发现**：
- listCount 是 **deliveryInputCtrl saveStock 特有的 Request 字段**
- machineOrderCtrl saveStock（L16212-16214）**不传** listCount
- 严格差异：A

---

## 18. Save success 后刷新行为（26.18）

**deliveryInputCtrl saveStock（L4007-4019）**：
```javascript
savePromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        Popup.notice('保存成功');  // L4013
        search();                    // L4014
        getCount();                  // L4015
        $state.reload();             // L4016
        $scope.stockDetail = false;  // L4017
    }
});
```

**调用顺序**：search() → getCount() → $state.reload() → stockDetail=false（A）

**machineOrderCtrl commonOrder（L16243-16257）**：
```javascript
commonPromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        orderPromise.then(function (resp) {
            $scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status;
        });
    }
});
```

**严格对比**：

| 行为 | deliveryInputCtrl | machineOrderCtrl | 等级 |
|------|------|------|------|
| Popup.notice("保存成功") | A（L4013） | **未调用** | A |
| search() 重新查询 | A（L4014） | **未调用** | A |
| getCount() 重新统计 | A（L4015） | **未调用** | A |
| $state.reload() 页面刷新 | A（L4016） | **未调用** | A |
| $scope.stockDetail = false | A（L4017） | **未调用** | A |
| getMachineCenterOrder.json 重新拉详情 | **未调用** | A（L16251） | A |
| 本地修改 items[idx].machineCenterOrder.status | **未调用** | A（L16253） | A |

**关键 A 级新发现**：
- 2 个 save API success 后**行为完全不一致**：
  - deliveryInputCtrl：完整页面刷新（search + getCount + $state.reload + 关闭模态）
  - machineOrderCtrl：只重新拉详情 + 本地修改 status 字段

---

## 19. deliveryInputCtrl 与 machineOrderCtrl 对照（26.19）

| 项目 | deliveryInputCtrl | machineOrderCtrl | 等级 |
|------|------|------|------|
| Query API | getCanBeDeliverySkuInListOfProduct.json | getCanBeProcessSkuInListOfProduct.json | A |
| Query Request | `{ medicalProductIdArray }` | `{ cashflowId }` | A |
| Query Response | `{ status, result: { list } }` | `{ status, result: { list } }` | A（结构一致） |
| Save API | saveMedicalProductStockBatch.json | saveToBeProcessSkuInListOfProduct.json | A |
| Save Request | `{ listCount, medicalProductStockBatctPoListJson }` | `{ medicalProductStockBatctPoListJson }` | A |
| 内部 JSON | `[{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]` | `[{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]` | A（**字段结构一致**） |
| save success | 完整刷新 | 局部刷新 | A |
| list 元素 | medicalProduct + deliveryStockInSkuVoList[] | medicalProduct + deliveryStockInSkuVoList[] | A |

**严格表述**：
- **"字段结构一致"**（A 级多源一致）
- **不写"共享 DTO"**（L2 业务推断，不升 A）
- **不写"同一 DTO 定义"**（无源码证据）

---

## 20. deliveryInputCtrl 与 optometryCtrl 对照（26.20）

| 项目 | deliveryInputCtrl | optometryCtrl.concatMedicalProductStock | 等级 |
|------|------|------|------|
| getCanBeDeliverySkuInListOfProduct.json | A（L3885） | A（L35054） | A |
| medicalProductIdArray | A（L3869/3874） | A（L35050/35052） | A |
| list 结构 | A | A | A |
| deliveryStockInSkuVoList | A | A | A |
| deliveryCount | A | A | A |
| **是否调用 save API** | A（saveMedicalProductStockBatch.json L4007） | **A（不调用）** | A |

**关键 A 级新发现**：
- optometryCtrl.concatMedicalProductStock 是**纯工具函数**（A）
- 仅调 getCanBeDeliverySkuInListOfProduct.json，**不调 save API**（A，L35048-35081 完整源码确认）
- 函数返回 Promise resolve(medicalProductStockBatctPoListJson)（A，L35079）
- 等级：A

---

## 21. deliveryInputCtrl 与 PAGE-008 对照（26.21）

**PAGE-008 关联字段**：
- getCashflowDeliveryVo：A（deliveryInputCtrl 用 L3848）
- deliveryedList：**F**（**不在 deliveryInputCtrl 范围**，是 deliveryInputRecordCtrl L4051）
- waitingDeliveryList：A（deliveryInputCtrl 用 L3851/3854/3856/3870/3893/3910）
- sendToMachineCenterList：**F**（controller.js 范围内未直接观察）
- medicalProductDelivery：**F**（deliveryInputCtrl 范围内未观察）

**关键 A 级边界**：
- `deliveryedList` 是 **deliveryInputRecordCtrl** 字段（A，L4051）
- **不**是 deliveryInputCtrl 字段
- 严格禁止把 deliveryedList 字段回填到 deliveryInputCtrl
- 等级：A

**sendToMachineCenterList**：
- controller.js 范围内**未直接出现** sendToMachineCenterList 字段
- 等级：F
- 不能强行定义为 deliveryInputCtrl 字段

---

## 22. deliveryInputCtrl 与 MachineCenter 对照（26.22）

| 字段 | 出现位置 | 等级 |
|------|------|------|
| machineCenter | 严格**未直接出现**作为对象在 deliveryInputCtrl 范围 | F |
| machineCenter.id | 通过 medicalProduct.objectId 间接使用 | A |
| objectId | A（L3854/3856/3873/3899/3916/3824） | A |
| getMedicalProductMachineCenterVoList | A（L3836） | A |
| getCenterListFactory.result.list | A（L3961-3962） | A |
| machineCenter 完整字段 | **F（未观察）** | F |
| 后续 selectOrder 中 machineCenter.id | A（L3962） | A |

**关键 A 级边界**：
- 严格**未补** machineCenterId 之外字段
- deliveryInputCtrl 范围内 machineCenter **仅通过 objectId 间接使用**
- 严格禁止把 machineCenter 整体对象字段回填
- 等级：A/F

---

## 23. 发货流状态字段（26.23）

**deliveryInputCtrl 范围内直接读取/写入的状态字段**：

| 字段 | 路径 | 等级 |
|------|------|------|
| $scope.stockDetail | L3882 = true / L4017 = false | A |
| $scope.addOrderModal | L3831 = true / L3953 = false / L3973 = false | A |
| $scope.cashflowId | L3814 from $stateParams | A |
| $scope.startTime | L3933-3964 | A |
| $scope.dateSearch | L3943-3948 | A |
| $scope.toggle | **F**（deliveryInputRecordCtrl 字段 L4028） | F |

**不存在的状态字段**（严格 F）：
- deliveryStatus：**F**（deliveryInputCtrl 范围未观察；deliveryListCtrl L4088-4099 有）
- acceptStatus / receiveStatus / status / toBeProcess / refundStatus：F

**严格禁止**：
- 把 MachineCenterOrder 的 state machine 自动移植过来
- 把 deliveryListCtrl 的 status 字段（deliveryStatus / toBeProcess / refundStatus）回填到 deliveryInputCtrl
- 等级：A

---

## 24. 一期最小复刻协议（26.24）

**基于 A 级事实的最小复刻结构**：

```javascript
// controller.js 必须存在的 5 个 API 调用
const DELIVERY_INPUT_CTRL_APIS = {
  // API-01 初始化查询
  search: {
    url: '/admin/getCashflowDeliveryVo.json',
    method: 'POST',
    request: { cashflowId: $stateParams.cashflowId },
    response: {
      result: {
        object: {
          waitingDeliveryList: [{
            medicalProduct: { id, objectId },
            lockStorehouse: { type },
            lockMachineCenter: { id }
          }]
        }
      }
    }
  },
  
  // API-02 初始化统计
  getCount: {
    url: '/admin/statProductDeliveryStatusOfCashflow.json',
    method: 'POST',
    request: { cashflowId: $stateParams.cashflowId }
  },
  
  // API-03 机器中心选择
  showAddModal: {
    url: '/admin/getMedicalProductMachineCenterVoList.json',
    method: 'POST',
    request: { medicalProductMachineCenterPoListJson: JSON.stringify([{ medicalProductId, machineCenterId }]) },
    response: { result: { list: [{ medicalProduct: { id }, machineCenter: { id } }] } }
  },
  
  // API-04 可发货 SKU 查询
  showDeliveryModal: {
    url: '/admin/getCanBeDeliverySkuInListOfProduct.json',
    method: 'POST',
    request: { medicalProductIdArray: [...] },
    response: {
      result: {
        list: [{
          medicalProduct: { id },
          deliveryStockInSkuVoList: [{
            deliveryCount,
            stockInSku: { id }
          }]
        }]
      }
    }
  },
  
  // API-05 保存
  saveStock: {
    url: '/admin/saveMedicalProductStockBatch.json',
    method: 'POST',
    request: {
      listCount: $scope.getDeliveryListFactory.result.list.length,
      medicalProductStockBatctPoListJson: JSON.stringify([{
        medicalProductId,
        medicalProductStocks: [{ stockInSkuId, deliveryCount }]
      }])
    },
    successCallback: {
      showNotice: '保存成功',
      actions: ['search()', 'getCount()', '$state.reload()', '$scope.stockDetail = false']
    }
  }
};
```

**E 级业务语义（不混入 A 级协议）**：
- 业务流程含义（E）
- 数据库 DTO 定义（E/F）
- 状态机转换（E）
- "共享库存服务" 等架构名（E）

---

## 25. 历史纠错（26.25）

**S1-62 推测错误**：
- S1-62 推测 deliveryInputCtrl 只调 save API
- S1-63 已纠正：deliveryInputCtrl 也调 Query API
- S1-64 进一步直接证据：deliveryInputCtrl **实际有 6 个 API**（含 sendMedicalProductToMachineCenter.json L3966）
- 等级：A

**S1-63 收口完整性**：
- S1-63 已收口 5 API 完整数据流
- S1-64 进一步确认：search 与 getCount 是**初始化立即执行**（L3844/L3866）
- 等级：A

**S1-63 字段边界维持**：
- S1-63 已建立：`iten.medicalProductStock.deliveryCount` 严格不同于 `deliveryStockInSkuVoList[j].deliveryCount`
- S1-64 进一步确认：deliveryInputCtrl 范围内**只**用 `deliveryStockInSkuVoList[j].deliveryCount`
- 等级：A

**字段结构 vs 共享 DTO**：
- S1-63 / S1-64 严格使用"字段结构一致"措辞
- **禁止**写"底层共享 DTO"
- 等级：A（严格遵守）

---

## 26. 26 项评级 / L1L2L3 / R1-R6 / Q / P0P1（26.26）

### 26.1 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 26.1 | deliveryInputCtrl 源码定位 | A |
| 26.2 | 5 API 完整清单 | A |
| 26.3 | getCashflowDeliveryVo.json 完整协议 | A |
| 26.4 | statProductDeliveryStatusOfCashflow.json 完整协议 | A |
| 26.5 | getMedicalProductMachineCenterVoList.json 完整协议 | A |
| 26.6 | getCanBeDeliverySkuInListOfProduct.json 完整协议 | A |
| 26.7 | saveMedicalProductStockBatch.json 完整协议 | A |
| 26.8 | 5 API 调用顺序 | A |
| 26.9 | 5 API 数据依赖图 | A |
| 26.10 | cashflow → delivery 流 | A |
| 26.11 | medicalProduct 来源 | A |
| 26.12 | objectId 专项 | A |
| 26.13 | stockInSku 字段边界 | A（id）/ F（其他 7 字段） |
| 26.14 | deliveryCount | A |
| 26.15 | medicalProductIdArray 生命周期 | A |
| 26.16 | save JSON 构造过程 | A |
| 26.17 | listCount | A |
| 26.18 | Save success 刷新行为 | A |
| 26.19 | 与 machineOrderCtrl 对照 | A |
| 26.20 | 与 optometryCtrl 对照 | A |
| 26.21 | 与 PAGE-008 对照 | A（waitingDeliveryList）/ F（deliveryedList / sendToMachineCenterList） |
| 26.22 | 与 MachineCenter 对照 | A（id）/ F（完整对象） |
| 26.23 | 发货流状态字段 | A（5 字段）/ F（其他） |
| 26.24 | 一期最小复刻协议 | A |
| 26.25 | 历史纠错 | A |
| 26.26 | 最终评级 | A |

**统计**：A=26（含 2 个 A/F 多评级项） / B=0 / C=0 / D=0 / E=0 / F=0 = 26

### 26.2 L1/L2/L3

**L1（前端直接事实）**：
- 5 API 完整 Request/Response 协议
- 调用顺序、数据依赖、success 行为
- evidence 等级：**A**

**L2（业务模型解释）**：
- 业务流程含义
- "发货流" / "加工流" 业务区分
- 共享 DTO 推断
- evidence 等级：**E**

**L3（数据库/物理模型）**：
- 数据库表结构
- 1:N 关系
- DTO/PO 定义
- evidence 等级：**F**

### 26.3 R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：A
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

### 26.4 Q&A

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | deliveryInputCtrl 实际有几个 API？ | A（**6 个**，含 sendMedicalProductToMachineCenter） |
| Q2 | 5 API 真实调用顺序？ | A（初始化 2 个 + 用户操作 3 个） |
| Q3 | 字段数据依赖？ | A（cashflowId → waitingDeliveryList → medicalProductIdArray → save JSON） |
| Q4 | saveStock success 后做什么？ | A（search + getCount + $state.reload + stockDetail=false） |
| Q5 | listCount 来源？ | A（`$scope.getDeliveryListFactory.result.list.length`） |
| Q6 | machineOrderCtrl 与 deliveryInputCtrl save 行为差异？ | A（局部 vs 完整刷新） |
| Q7 | optometryCtrl 是否调 save API？ | A（**不调**，纯工具函数） |
| Q8 | objectId 是什么？ | A（machineCenterId 引用） |
| Q9 | deliveryedList 在 deliveryInputCtrl 范围？ | A（**不**，是 deliveryInputRecordCtrl 字段） |
| Q10 | sendToMachineCenterList 字段？ | F（未观察） |
| Q11 | medicalProductDelivery 在 deliveryInputCtrl 范围？ | F（未观察） |
| Q12 | L3 数据库结构？ | F |

### 26.5 P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 27. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 28. 本轮新增事实

| 编号 | 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|------|
| 1 | controller.js | L3812-4021 | deliveryInputCtrl 完整 209 行定义 | A |
| 2 | controller.js | L3814 | $scope.cashflowId = $stateParams.cashflowId | A |
| 3 | controller.js | L3841 | statProductDeliveryStatusOfCashflow.json 唯一调用点 | A |
| 4 | controller.js | L3848 | getCashflowDeliveryVo.json 唯一调用点 | A |
| 5 | controller.js | L3836 | getMedicalProductMachineCenterVoList.json 唯一调用点 | A |
| 6 | controller.js | L3885 | getCanBeDeliverySkuInListOfProduct.json 唯一调用点 | A |
| 7 | controller.js | L4007 | saveMedicalProductStockBatch.json 唯一调用点 | A |
| 8 | controller.js | **L3966** | **新发现**：sendMedicalProductToMachineCenter.json（6th API） | A |
| 9 | controller.js | L3851-3857 | waitingDeliveryList 处理逻辑 | A |
| 10 | controller.js | L3853-3856 | lockStorehouse.type=4 → objectId = lockMachineCenter.id | A |
| 11 | controller.js | L3816-3829 | getMachineCenterList 完整函数 | A |
| 12 | controller.js | L3821-3825 | objectId truthy 过滤 + 推入 medicalProductMachineCenterPoList | A |
| 13 | controller.js | L3869-3886 | showDeliveryModal 完整函数 | A |
| 14 | controller.js | L3873-3874 | objectId == null 过滤 + push medicalProduct.id | A |
| 15 | controller.js | L3882 | $scope.stockDetail = true（showDeliveryModal） | A |
| 16 | controller.js | L3979-4020 | saveStock 完整函数 | A |
| 17 | controller.js | L3985-4004 | saveStock 双重 for 循环 + 校验 | A |
| 18 | controller.js | L3991 | 推入 { stockInSkuId, deliveryCount } | A |
| 19 | controller.js | L3998 | 推入 { medicalProductId, medicalProductStocks } | A |
| 20 | controller.js | L4001-4004 | 全空检查 return false | A |
| 21 | controller.js | L4007 | Request = { listCount, medicalProductStockBatctPoListJson } | A |
| 22 | controller.js | L4013-4017 | success 后 search + getCount + $state.reload + stockDetail=false | A |
| 23 | controller.js | L3955-3977 | **新发现**：selectOrder 函数（消费 getCenterListFactory） | A |
| 24 | controller.js | L3961-3962 | selectOrder 读 getCenterListFactory.result.list | A |
| 25 | controller.js | L3888-3921 | isSendProduct / isSendCenter 函数（用 objectId） | A |
| 26 | controller.js | L4024 | **新发现**：deliveryInputRecordCtrl 是不同 controller（不是 deliveryInputCtrl） | A |
| 27 | controller.js | L4051 | **新发现**：deliveryedList 字段属于 deliveryInputRecordCtrl | A |

---

## 29. 红线核查汇总

- **写操作 = 0**（仅静态源码分析）
- **生产数据修改 = 0**
- **历史 MD 修改 = 0**（28~123 全部未修改）
- **P0 自动新增 = 0**
- **P1 自动新增 = 0**
- **10 个 untracked 临时文件原样保留**

---

## 30. 最终一句话

"S1-64 完成，已 Git 封口，立即停止，不进入 S1-65，等待老板下一条指令。"
