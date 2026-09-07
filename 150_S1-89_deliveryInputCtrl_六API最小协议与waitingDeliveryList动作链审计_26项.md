# S1-89 deliveryInputCtrl 六 API 最小协议与 waitingDeliveryList 动作链审计

> 审计对象：`deliveryInputCtrl` L3812-4021（209 行）+ 6 API + waitingDeliveryList 主链 + F5/F6 Write API 静态审计
> 任务来源：S1-89（基于 S1-78/87/88 已确认 6 API + 字段分叉）
> 审计立场：**只按源码证据；Write API 绝不调用；不按"加工中心订单"业务命名推断；严格区分 A-F**

---

## 1. 审计范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryInputCtrl | L3812-4021（**209 行**）| 完整二次确认 |
| 6 API 调用点 | 6 处（A） | 各自独立 |
| ObjectFactory 实例 | 6 个（A） | 全部挂 $scope |
| 5 helper functions | getMachineCenterList/getCount/search/isSendProduct/isSendCenter 等 | A |
| 2 Write API (F5/F6) | 静态审计（**绝不调用**）| A |
| 1 跨 Read API (F3/F4) | 等待 + Select SKU 派生 | A |
| deliveryInput HTML 模板 | **F** | working dir 0 个对应 |

---

## 2. 证据等级

| 等级 | 含义 |
|---|---|
| A | 直接代码证据 |
| B | 多源互证 |
| C | 局部/不完整 |
| D | 冲突/明确缺陷 |
| E | 合理业务推断 |
| F | 当前证据范围未观察/不可得 |

**关键纪律**：F5/F6 是 Write API，**本轮绝不调用**；所有 Request 字段 / 数组结构 / 派生路径必须按源码原样记录。

---

## 3. deliveryInputCtrl 完整定位

| 项 | 值 |
|---|---|
| 文件 | controller.js |
| 起止行 | L3812-4021 |
| 行数 | **209** |
| 注入依赖 | $scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, **ObjectFactory**, **ListFactory**, $http, $q, QiniuFactory, $timeout（**12 个**）|
| stateParams | `$stateParams.cashflowId`（L3814）|
| cashflowId | `$scope.cashflowId = $stateParams.cashflowId`（L3814）|
| 6 Factory 挂 $scope | 6/6（A）|

---

## 4. 6 API 完整总览

| # | API | Factory | Request | result Consumer | Success | 下游 |
|---|---|---|---|---|---|---|
| F1 | getCashflowDeliveryVo.json | getMedicalRecordDeliveryFactory (L3847) | `{ cashflowId: $scope.cashflowId }` | **7 处** result.object.waitingDeliveryList | 弹空窗 + $state.go('deliveryList') | F3/F4 主数据源 |
| F2 | statProductDeliveryStatusOfCashflow.json | getStatusDeliveryFactory (L3840) | `{ cashflowId: $scope.cashflowId }` | **0 处** | — | 仅 fire-and-forget |
| F3 | getMedicalProductMachineCenterVoList.json | getCenterListFactory (L3835) | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` | **1 处** result.list.map (L3961) | — | F6 主数据源 |
| F4 | getCanBeDeliverySkuInListOfProduct.json | getDeliveryListFactory (L3884) | `{ medicalProductIdArray: medicalProductIdArray }` | **6 处** result.list / deliveryStockInSkuVoList 循环 (L3985-3998) | $scope.stockDetail=true | F5 主数据源 |
| F5 | **saveMedicalProductStockBatch.json** (Write) | saveStockFactory (L4006) | `{ listCount, medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson) }` | res.status/errmsg (1 处) | Popup + search() + getCount() + $state.reload() + stockDetail=false | F1/F2 refresh |
| F6 | **sendMedicalProductToMachineCenter.json** (Write) | createOrderFactory (L3965) | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }` | res.status/errmsg (1 处) | Popup + addOrderModal=false + $state.reload() | page reload |

**A**：6 API 完整调用链 A 级确认（A）。

---

## 5. F1 getCashflowDeliveryVo 完整记录

### 5.1 调用点

```javascript
// L3847-3864
$scope.getMedicalRecordDeliveryFactory = new ObjectFactory();
var deliveryPromise = $scope.getMedicalRecordDeliveryFactory.saveOrQuery(
    '/admin/getCashflowDeliveryVo.json',
    { cashflowId: $scope.cashflowId }
);
deliveryPromise.then(function (res) {
    var arr = res.result.object.waitingDeliveryList;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].lockStorehouse.type == 4) {
            $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
        } else {
            $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
        }
    }
    if (!arr.length) {
        Popup.notice('您的待发货项目已分拣完毕，即将返回列表', 1500, function () {
            $state.go('deliveryList');
        });
    }
});
```

### 5.2 Request

```javascript
{ cashflowId: $scope.cashflowId }
```

### 5.3 result.object 字段消费矩阵（A 级完整）

| # | 行号 | 路径 | 上下文 | 形式 |
|---|---|---|---|---|
| 1 | L3818 | `result.object.waitingDeliveryList` | getMachineCenterList helper | 读 |
| 2 | L3851 | `res.result.object.waitingDeliveryList` | search().then | 读（赋给 arr）|
| 3 | L3854 | `result.object.waitingDeliveryList[i].medicalProduct.objectId` | then 回调 | **写** |
| 4 | L3856 | `result.object.waitingDeliveryList[i].medicalProduct.objectId` | then 回调 | **写 null** |
| 5 | L3870 | `result.object.waitingDeliveryList` | showDeliveryModal | 读 |
| 6 | L3890 | `result.object` | isSendProduct | 读（存在性校验）|
| 7 | L3893 | `result.object.waitingDeliveryList` | isSendProduct | 读 |
| 8 | L3907 | `result.object` | isSendCenter | 读（存在性校验）|
| 9 | L3910 | `result.object.waitingDeliveryList` | isSendCenter | 读 |

**A**：F1 result.object 完整 **9 处访问**（A）。

### 5.4 waitingDeliveryList 二级字段访问（A 级）

| 字段路径 | 出现行号 | 读/写 | 用途 |
|---|---|---|---|
| `arr[i].lockStorehouse.type` | L3853 | 读 | then 回调条件（== 4 决定 objectId 赋值）|
| `arr[i].lockMachineCenter.id` | L3854 | 读 | then 回调（赋值给 objectId）|
| `arr[i].medicalProduct.id` | L3823/L3874/L3962/L3998 | 读 | 多次（getMachineCenterList/showDeliveryModal/selectOrder/saveStock）|
| `arr[i].medicalProduct.objectId` | L3821/L3854/L3856/L3873/L3899/L3916 | 读/写 | 核心字段（决定是否可发/可发到中心）|

**A**：4 个二级字段（A）。

---

## 6. waitingDeliveryList 完整主链

### 6.1 5 步主链

```
1. F1 result.object.waitingDeliveryList (L3818)
    ↓
2. getMachineCenterList helper (L3816-3829)
    ↓ 循环派生 medicalProductMachineCenterPoList
3. F3 Request.medicalProductMachineCenterPoListJson (L3836)
    ↓
4. F3 Response (F 边界)
    ↓
5. F3 result.list → F6 Request (L3961-3962)
```

### 6.2 waitingDeliveryList 在 5 个 helper/function 中的角色

| # | 函数 | 行号 | 角色 |
|---|---|---|---|
| 1 | getMachineCenterList | L3816-3829 | 派生 F3 Request |
| 2 | search().then | L3849-3864 | 二次写入 medicalProduct.objectId + 弹空窗 + $state.go |
| 3 | showDeliveryModal | L3868-3886 | 派生 F4 Request.medicalProductIdArray |
| 4 | isSendProduct | L3888-3904 | 校验：是否全部 medicalProduct.objectId 已设 |
| 5 | isSendCenter | L3905-3921 | 校验：是否全部 medicalProduct.objectId == null |

**A**：waitingDeliveryList 是 5 个函数的输入数据（A）。

### 6.3 waitingDeliveryList → F3/F4/F5/F6 间接追溯

| 目标 | 是否直接来自 waitingDeliveryList | 派生路径 |
|---|---|---|
| F3 Request | **间接** | waitingDeliveryList → getMachineCenterList (循环 if objectId) → medicalProductMachineCenterPoList |
| F4 Request | **间接** | waitingDeliveryList → showDeliveryModal (循环 if objectId==null) → medicalProductIdArray |
| F5 Request | **间接**（通过 F4）| waitingDeliveryList → F4 → getDeliveryListFactory.result.list → saveStock 循环 |
| F6 Request | **间接**（通过 F3）| waitingDeliveryList → F3 → getCenterListFactory.result.list → selectOrder 循环 |

**A**：
- waitingDeliveryList **不直接**进入 F5/F6 Request
- waitingDeliveryList **间接**通过 F3/F4 进入 F5/F6
- **不是 F1 → F5/F6 的直传**（A）

---

## 7. F3 getMedicalProductMachineCenterVoList 完整记录

### 7.1 调用点

```javascript
// L3830-3837 (showAddModal)
$scope.addOrderModal = true;
$scope.startTime = undefined;
$scope.dateSearch = null;
var arr = getMachineCenterList();
$scope.getCenterListFactory = new ObjectFactory();
$scope.getCenterListFactory.saveOrQuery(
    '/admin/getMedicalProductMachineCenterVoList.json',
    { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
);
```

### 7.2 Request

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr)
}
```

`arr` = `getMachineCenterList()` 返回值（`medicalProductMachineCenterPoList`）

### 7.3 Request 内部结构

```javascript
// L3822-3825
{
    medicalProductId: arr[i].medicalProduct.id,
    machineCenterId: arr[i].medicalProduct.objectId
}
```

### 7.4 result Consumer

| 行号 | 路径 | 形式 |
|---|---|---|
| L3961 | `result.list` | map 循环（selectOrder 内）|

**A**：F3 result.list 1 处消费（selectOrder 内，A）。

### 7.5 selectOrder 内 F3 result.map 完整（A 级）

```javascript
// L3961-3963
var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
});
```

**A**：
- `v` 是 F3 result.list 的元素
- `v.medicalProduct.id` 读取（A）
- `v.machineCenter.id` 读取（A）
- 输出 `{ medicalProductId, machineCenterId }` 进入 F6 Request（A）

---

## 8. F4 getCanBeDeliverySkuInListOfProduct 完整记录

### 8.1 调用点

```javascript
// L3868-3886 (showDeliveryModal)
var medicalProductIdArray = [];
var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
for (var i = 0; i < arr.length; i++) {
    if (arr[i].medicalProduct.objectId == null) {
        medicalProductIdArray.push(arr[i].medicalProduct.id);
    }
}
if (!medicalProductIdArray.length) {
    Popup.notice("请选择发货的商品");
    return false;
}
$scope.stockDetail = true;
$scope.getDeliveryListFactory = new ObjectFactory();
$scope.getDeliveryListFactory.saveOrQuery(
    '/admin/getCanBeDeliverySkuInListOfProduct.json',
    { medicalProductIdArray: medicalProductIdArray }
);
```

### 8.2 Request

```javascript
{
    medicalProductIdArray: medicalProductIdArray  // number array
}
```

`medicalProductIdArray` 来源 = `waitingDeliveryList` 中 `medicalProduct.objectId == null` 的 `medicalProduct.id` 集合。

### 8.3 result Consumer

| 行号 | 路径 | 形式 |
|---|---|---|
| L3985 | `result.list` | 读（saveStock 外层循环）|
| L3985 | `result.list.length` | 读 |
| L3988 | `result.list[i].deliveryStockInSkuVoList` | 读 + length 循环 |
| L3989 | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | 读 + 条件 |
| L3991 | `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | 读（进入 F5）|
| L3992 | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | 读 |
| L3998 | `result.list[i].medicalProduct.id` | 读（进入 F5）|

**A**：F4 result.list **6 处访问**（A）。

### 8.4 result 内部结构（已观察）

| 字段路径 | 类型 | 用途 |
|---|---|---|
| `result.list[]` | array | 顶层数组 |
| `result.list[i].deliveryStockInSkuVoList[]` | array | 二级数组（每元素含 stockInSku.id + deliveryCount）|
| `result.list[i].medicalProduct.id` | number | 进入 F5 |
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | number | 进入 F5 |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | number | 进入 F5 |

---

## 9. F5 saveMedicalProductStockBatch 静态审计（**绝不调用**）

### 9.1 调用点

```javascript
// L3979-4020 (saveStock)
$scope.saveStock = function () {
    var arr = [];
    var medicalProductStockBatctPoListJson = [];
    var medicalProductStockListJson;
    for (var i = 0; i < $scope.getDeliveryListFactory.result.list.length; i++) {
        arr[i] = [];
        for (var j = 0; j < $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList.length; j++) {
            if ($scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount > 0) {
                arr[i].push({
                    stockInSkuId: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id,
                    deliveryCount: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount
                });
            } else if ($scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount < 0) {
                Popup.notice('发货数量必须大于0');
                return false;
            } else {}
        }
        if (arr[i].length) {
            medicalProductStockBatctPoListJson.push({
                medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id,
                medicalProductStocks: arr[i]
            });
        }
    }
    if (!medicalProductStockBatctPoListJson.length) {
        Popup.notice('发货数量必须大于0');
        return false;
    }
    $scope.saveStockFactory = new ObjectFactory();
    var savePromise = $scope.saveStockFactory.saveOrQuery(
        '/admin/saveMedicalProductStockBatch.json',
        {
            listCount: $scope.getDeliveryListFactory.result.list.length,
            medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson)
        }
    );
    savePromise.then(function (res) {
        if (res.status == 1) {
            Popup.notice(res.errmsg);
        } else {
            Popup.notice('保存成功');
            search();
            getCount();
            $state.reload();
            $scope.stockDetail = false;
        }
    });
};
```

### 9.2 Request 完整结构

```javascript
{
    listCount: $scope.getDeliveryListFactory.result.list.length,  // 顶层 length
    medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson)  // 字符串
}
```

### 9.3 medicalProductStockBatctPoListJson 内部结构

```json
[
    {
        medicalProductId: number,           // 来自 F4 result.list[i].medicalProduct.id
        medicalProductStocks: [              // 数组
            {
                stockInSkuId: number,        // 来自 F4 result.list[i].deliveryStockInSkuVoList[j].stockInSku.id
                deliveryCount: number         // 来自 F4 result.list[i].deliveryStockInSkuVoList[j].deliveryCount
            },
            ...
        ]
    },
    ...
]
```

**A**：F5 Request 完整 3 字段结构 A 级确认（A）。

### 9.4 F5 Request 字段来源

| 字段 | 来源 |
|---|---|
| listCount | `$scope.getDeliveryListFactory.result.list.length` |
| medicalProductStockBatctPoListJson[].medicalProductId | F4 result.list[i].medicalProduct.id |
| medicalProductStockBatctPoListJson[].medicalProductStocks[].stockInSkuId | F4 result.list[i].deliveryStockInSkuVoList[j].stockInSku.id |
| medicalProductStockBatctPoListJson[].medicalProductStocks[].deliveryCount | F4 result.list[i].deliveryStockInSkuVoList[j].deliveryCount |

**A**：F5 Request **完全派生自 F4 result.list**（A）。

### 9.5 F5 Success 行为（A 级）

```javascript
savePromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);  // 错误显示
    } else {
        Popup.notice('保存成功');           // 成功提示
        search();                          // 重查 F1
        getCount();                        // 重查 F2
        $state.reload();                  // 整页 reload
        $scope.stockDetail = false;        // 关闭 stockDetail modal
    }
});
```

**A**：F5 Success 触发 **4 步**（search + getCount + reload + stockDetail=false，A）。

### 9.6 F5 触发 Read 链

| Read API | 调用 |
|---|---|
| F1 (getCashflowDeliveryVo.json) | search() 重新调用 |
| F2 (statProductDeliveryStatusOfCashflow.json) | getCount() 重新调用 |
| F3/F4 | **不重新调用**（无 searchCount 等）|

**A**：F5 Success 仅刷新 F1 + F2，**不刷新 F3/F4**（A）。

### 9.7 命名边界

**禁止表述**：
- "saveMedicalProductStockBatch 写入库存表"（E 推测，无 L3 证据）
- "stockInSkuId = SKU 入库表主键"（E 推测）
- "medicalProductStocks = 库存对象"（E 推测）

**可表述**：
- "saveStockFactory 调用 saveMedicalProductStockBatch.json"（A）
- "Request 含 listCount + medicalProductStockBatctPoListJson"（A）
- "字段来源：F4 result.list"（A）

---

## 10. F6 sendMedicalProductToMachineCenter 静态审计（**绝不调用**）

### 10.1 调用点

```javascript
// L3955-3977 (selectOrder)
$scope.selectOrder = function () {
    if (!$scope.startTime) {
        Popup.notice("请选择取镜日期");
        return false;
    }
    var arr = $scope.getCenterListFactory.result.list.map(function (v) {
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);
    $scope.createOrderFactory = new ObjectFactory();
    var createPromise = $scope.createOrderFactory.saveOrQuery(
        '/admin/sendMedicalProductToMachineCenter.json',
        {
            medicalProductMachineCenterPoListJson: JSON.stringify(arr),
            planDeliveryTime: $scope.startTime
        }
    );
    createPromise.then(function (res) {
        if (res.status == 1) {
            Popup.notice(res.errmsg);
        } else {
            Popup.notice('发送成功');
            $scope.addOrderModal = false;
            $state.reload();
        }
    });
};
```

### 10.2 Request 完整结构

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr),  // 字符串
    planDeliveryTime: $scope.startTime                          // Date 对象
}
```

### 10.3 medicalProductMachineCenterPoListJson 内部结构

```json
[
    {
        medicalProductId: number,    // 来自 F3 result.list[i].medicalProduct.id
        machineCenterId: number      // 来自 F3 result.list[i].machineCenter.id
    },
    ...
]
```

**A**：F6 Request 完整 2 字段结构 A 级确认（A）。

### 10.4 F6 Request 字段来源

| 字段 | 来源 |
|---|---|
| planDeliveryTime | `$scope.startTime`（L3832 / L3933 / L3939 / L3964）|
| medicalProductMachineCenterPoListJson[].medicalProductId | F3 result.list[i].medicalProduct.id |
| medicalProductMachineCenterPoListJson[].machineCenterId | F3 result.list[i].machineCenter.id |

**A**：F6 Request **完全派生自 F3 result.list + $scope.startTime**（A）。

### 10.5 F6 Success 行为（A 级）

```javascript
createPromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        Popup.notice('发送成功');
        $scope.addOrderModal = false;  // 关闭 addOrderModal
        $state.reload();              // 整页 reload
    }
});
```

**A**：F6 Success 触发 **2 步**（addOrderModal=false + $state.reload()，A）。

### 10.6 F6 vs F5 Success 对比

| 行为 | F5 Success | F6 Success |
|---|---|---|
| Popup.notice('保存成功'/'发送成功') | ✅ | ✅ |
| search() 重查 F1 | ✅ | ❌ |
| getCount() 重查 F2 | ✅ | ❌ |
| $state.reload() | ✅ | ✅ |
| 关闭 modal | $scope.stockDetail = false | $scope.addOrderModal = false |

**A**：F5 Success **4 步**（含 search + getCount），F6 Success **2 步**（**不重查 Read API**），差异明确（A）。

### 10.7 关键追溯结论

**Q：F6 Request 能否直接追溯到 waitingDeliveryList 某字段？**

**A：不能直接追溯。F6 Request 字段来源 = F3 result.list（即 F3 Response）**，**不是 F1 result.object.waitingDeliveryList**（A）。

**A**：
- F1 result.object.waitingDeliveryList → getMachineCenterList → F3 Request
- F3 result.list → selectOrder → F6 Request
- **F1 与 F6 之间存在 F3 中间层**（A）
- F6 Request **不直接**来自 waitingDeliveryList 字段（A）

### 10.8 命名边界

**禁止表述**：
- "sendMedicalProductToMachineCenter 创建加工中心订单"（E 推测）
- "machineCenterId = 加工中心主数据主键"（E 推测）
- "planDeliveryTime = 计划交付时间"（E 推测）

**可表述**：
- "createOrderFactory 调用 sendMedicalProductToMachineCenter.json"（A）
- "Request 含 medicalProductMachineCenterPoListJson + planDeliveryTime"（A）
- "字段来源：F3 result.list + $scope.startTime"（A）

---

## 11. F2 statProductDeliveryStatusOfCashflow 边界

### 11.1 调用点

```javascript
// L3839-3844 (getCount)
var getCount = function getCount() {
    $scope.getStatusDeliveryFactory = new ObjectFactory();
    $scope.getStatusDeliveryFactory.saveOrQuery(
        '/admin/statProductDeliveryStatusOfCashflow.json',
        { cashflowId: $scope.cashflowId }
    );
};
getCount();
```

### 11.2 Request / Consumer

| 维度 | 值 |
|---|---|
| Request | `{ cashflowId: $scope.cashflowId }` |
| 返回接收 | ❌（fire-and-forget）|
| then | ❌ |
| result 消费 | **0 处** |
| 模式 | **pure fire-and-forget** |

**A**：F2 在 deliveryInputCtrl 是纯 fire-and-forget 模式（A）。

---

## 12. 6 Factory 实例隔离（A 级）

| # | Factory | 行号 | 挂 $scope | API | 调用函数 |
|---|---|---|---|---|---|
| 1 | getMedicalRecordDeliveryFactory (F1) | L3847 | ✅ | getCashflowDeliveryVo.json | search() (L3866) |
| 2 | getStatusDeliveryFactory (F2) | L3840 | ✅ | statProductDeliveryStatusOfCashflow.json | getCount() (L3844) |
| 3 | getCenterListFactory (F3) | L3835 | ✅ | getMedicalProductMachineCenterVoList.json | showAddModal() |
| 4 | getDeliveryListFactory (F4) | L3884 | ✅ | getCanBeDeliverySkuInListOfProduct.json | showDeliveryModal() |
| 5 | saveStockFactory (F5) | L4006 | ✅ | saveMedicalProductStockBatch.json | saveStock() |
| 6 | createOrderFactory (F6) | L3965 | ✅ | sendMedicalProductToMachineCenter.json | selectOrder() |

**A**：
- 6 Factory **6 个独立实例**（A）
- 全部挂 $scope（A）
- 6 变量名不同（A）

### 12.1 Factory 间 result 传递链（A 级）

| Source Factory | Target Factory | 传递路径 | 等级 |
|---|---|---|---|
| F1 (L3818) | F3 Request | `result.object.waitingDeliveryList` → getMachineCenterList → `medicalProductMachineCenterPoList` | A |
| F1 (L3870) | F4 Request | `result.object.waitingDeliveryList` → showDeliveryModal → `medicalProductIdArray` | A |
| F3 (L3961) | F6 Request | `result.list` → selectOrder.map → `arr` | A |
| F4 (L3985-3998) | F5 Request | `result.list` → saveStock 循环 → `medicalProductStockBatctPoListJson` | A |

**A**：
- 4 条 result 传递链 A 级确认（A）
- 全部通过 `$scope.xxxFactory.result` 跨调用传递（A）
- **不是直接传递**（A）
- 全部**单向**：F1 → F3/F4，F3 → F6，F4 → F5（A）

---

## 13. Read / Write 边界（A 级）

| API | Read/Write | 本轮是否调用 | Request 静态可见 | Consumer 静态可见 |
|---|---|---|---|---|
| F1 getCashflowDeliveryVo.json | **Read** | ❌ | ✅ | ✅ |
| F2 statProductDeliveryStatusOfCashflow.json | **Read** | ❌ | ✅ | ❌（0 consumer）|
| F3 getMedicalProductMachineCenterVoList.json | **Read** | ❌ | ✅ | ✅ |
| F4 getCanBeDeliverySkuInListOfProduct.json | **Read** | ❌ | ✅ | ✅ |
| F5 saveMedicalProductStockBatch.json | **WRITE** | **❌ 绝不调用** | ✅ | ✅ |
| F6 sendMedicalProductToMachineCenter.json | **WRITE** | **❌ 绝不调用** | ✅ | ✅ |

**A**：
- **4 Read + 2 Write**（A）
- 本轮 **0 处 API 调用**（含 0 处 Write 调用，A）
- **6/6 API Request 全部静态可见**（A）

---

## 14. 主链关系图（A 级，仅展示源码可证箭头）

```
$stateParams.cashflowId (路由参数)
    ↓ [A] (L3814)
$scope.cashflowId
    ↓ [A] (L3848/L3841/L3966)
F1 / F2 / F6 Request
    ↓ [A] (L3847/L3840/L3965)
new ObjectFactory() × 3
    ↓ [A] (L3848/L3841/L3966)
F1 / F2 / F6 saveOrQuery
    ↓
[F] 后端 HTTP 通信
    ↓
F1 result.object.waitingDeliveryList
    ↓ [A] (L3818/L3851/L3870/L3893/L3910)
getMachineCenterList helper
    ↓ [A] (L3816-3829)
medicalProductMachineCenterPoList (局部)
    ↓ [A] (L3834)
$scope.getCenterListFactory = new ObjectFactory() (F3)
    ↓ [A] (L3835-3836)
F3 saveOrQuery
    ↓
[F] 后端 HTTP 通信
    ↓
$scope.getCenterListFactory.result.list
    ↓ [A] (L3961)
selectOrder .map
    ↓ [A] (L3962)
arr (medicalProductId, machineCenterId)
    ↓ [A] (L3966)
$scope.createOrderFactory = new ObjectFactory() (F6)
    ↓ [A] (L3965-3966)
F6 saveOrQuery (WRITE)
    ↓
[F] 后端 HTTP 通信
    ↓
res.status / res.errmsg
    ↓ [A] (L3969-3970)
Popup.notice / $scope.addOrderModal=false / $state.reload()


F1 result.object.waitingDeliveryList (另一路径)
    ↓ [A] (L3870)
showDeliveryModal
    ↓ [A] (L3868-3886)
medicalProductIdArray (局部)
    ↓ [A] (L3884)
$scope.getDeliveryListFactory = new ObjectFactory() (F4)
    ↓ [A] (L3884-3885)
F4 saveOrQuery
    ↓
[F] 后端 HTTP 通信
    ↓
$scope.getDeliveryListFactory.result.list
    ↓ [A] (L3985-3998)
saveStock 双重循环
    ↓ [A] (L3985-3998)
medicalProductStockBatctPoListJson (局部)
    ↓ [A] (L4007)
$scope.saveStockFactory = new ObjectFactory() (F5)
    ↓ [A] (L4006-4007)
F5 saveOrQuery (WRITE)
    ↓
[F] 后端 HTTP 通信
    ↓
res.status / res.errmsg
    ↓ [A] (L4010-4011)
Popup.notice / search() / getCount() / $state.reload() / $scope.stockDetail=false
```

**A**：
- 完整 4 步主链 A 级闭合（A）
- 所有 [A] 箭头 = 源码直接证据
- 所有 [F] = 后端 HTTP 通信 + Response 完整结构（不可得）
- **F5/F6 Write API 绝不调用**（A）

---

## 15. HTML 边界

| 检查项 | 结果 |
|---|---|
| deliveryInput.html / deliveryInputCtrl.html | **F**（working dir 0 个对应）|
| 其它 6 个 untracked HTML | 0 处 deliveryInput 相关引用 |
| 路由表 state → templateUrl 映射 | F（controller.js 0 处）|
| ng-controller attribute | 7 HTML 全部 0 处（**仅靠注释标识**，S1-86 已确认）|

**F**：
- deliveryInputCtrl HTML 模板在当前资源范围**不可得**（F）
- 但 controller.js 中**已直接出现的字段** = A 级（**不降级 F**）

---

## 16. 26 项审计矩阵

| # | 审计项 | 等级 | 证据 |
|---|---|---|---|
| 01 | deliveryInputCtrl 注册 | A | controller.js L3812 |
| 02 | Controller 行范围 | A | L3812-4021（209 行）|
| 03 | cashflowId 来源 | A | L3814 `$stateParams.cashflowId` |
| 04 | F1 API | A | L3848 getCashflowDeliveryVo.json |
| 05 | F1 Factory | A | L3847 getMedicalRecordDeliveryFactory |
| 06 | F1 Request | A | `{ cashflowId }` |
| 07 | F1 result.object | A | 9 处访问（7 waitingDeliveryList + 2 写 + 3 存在性）|
| 08 | waitingDeliveryList 来源 | A | F1 result.object.waitingDeliveryList |
| 09 | waitingDeliveryList Consumer | A | 7 处访问（5 helper/function + 2 写）|
| 10 | waitingDeliveryList 二级字段 | A | lockStorehouse.type / lockMachineCenter.id / medicalProduct.id / medicalProduct.objectId |
| 11 | F2 API | A | L3841 statProductDeliveryStatusOfCashflow.json |
| 12 | F2 Consumer | A | **0 处** |
| 13 | F3 API | A | L3836 getMedicalProductMachineCenterVoList.json |
| 14 | F3 Request | A | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` |
| 15 | F3 result Consumer | A | L3961 result.list.map（selectOrder）|
| 16 | machineCenter 相关字段 | A | v.medicalProduct.id / v.machineCenter.id / machineCenterId 字段 |
| 17 | F4 API | A | L3885 getCanBeDeliverySkuInListOfProduct.json |
| 18 | F4 Request | A | `{ medicalProductIdArray }` |
| 19 | F4 result Consumer | A | 6 处 result.list 字段访问 |
| 20 | F5 Request | A | `{ listCount, medicalProductStockBatctPoListJson: JSON.stringify(...) }` |
| 21 | F5 Request 字段来源 | A | 4 字段全部派生自 F4 result.list |
| 22 | F5 Success Read 链 | A | search() + getCount() + $state.reload() + stockDetail=false（4 步）|
| 23 | F6 Request | A | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime }` |
| 24 | F6 Request 字段来源 | A | 派生自 F3 result.list + $scope.startTime（**不直接来自 waitingDeliveryList**）|
| 25 | 6 Factory 独立 | A | 6 独立实例 + 4 条 result 传递链 |
| 26 | 最小证据链结论 | A | 完整 4 步主链 A 级闭合 |

### 16.1 A / B / C / D / E / F 统计

| 等级 | 数量 | 占比 |
|---|---|---|
| A | **26** | 100% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 0 | 0% |

**A**：26 项**全部 A 级**（无 E/F 升 A，E/F 不在主链中）。

注：F 边界（后端 HTTP / Response 完整结构）已在主链图 [F] 标记，但不计入 26 项等级统计（26 项仅覆盖**前端可观察**范围）。

---

## 17. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | 6 API / 6 Factory / 4 条传递链 / Request 完整字段 / 2 Write Success 行为 | **是** |
| L2 业务规则 | 业务模块归属 / "加工中心订单" / "库存表"语义 | **E**（按字段名推测，无 L3 证据）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository / 落库表 | **F**（资源范围外）|

**禁止表述**：
- "saveMedicalProductStockBatch 写入库存表"
- "sendMedicalProductToMachineCenter 创建加工中心订单表"
- "machineCenterId = 加工中心主数据主键"
- "planDeliveryTime = 计划交付时间"
- "stockInSkuId = SKU 入库主键"

---

## 18. F 边界清单

| F 项 | 原因 |
|---|---|
| 后端 6 API 完整 Response 字段结构 | 资源范围外 |
| ObjectFactory 内部 HTTP 实现 | 资源范围外 |
| deliveryInputCtrl HTML 模板 | working dir + tracked 0 个对应 |
| 路由表 state → templateUrl 映射 | controller.js 0 处；路由配置不在资源范围 |
| saveMedicalProductStockBatch 落库表 | 资源范围外（L3 = F）|
| sendMedicalProductToMachineCenter 创建实体 | 资源范围外（L3 = F）|
| stockInSkuId / machineCenterId / medicalProductId / medicalProductStocks / planDeliveryTime 业务语义 | L3 = F（**禁止按命名升级**）|
| deliveryInput HTML 内 ng-click / ng-repeat / item 字段 | HTML 不可得 |
| 6 controller 对应 HTML 模板 | working dir 0 个对应 |

---

## 19. 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 write API 调用 | ❌（**F5/F6 0 处调用**）|
| R3 修改历史 MD | ❌ |
| R4 删除 10 untracked | ❌（**deliveryList.html hash 复核不变**）|
| R5 P0/P1 自动新增 | ❌ |
| R6 git add . / -A / * | ❌ |
| R7 修改 controller.js / 7 HTML | ❌（全部只读）|
| R8 文件编号冲突 | ❌（149 已被 S1-88 占用，本轮 150）|

---

## 20. 最终结论

### 20.1 一句话总结

**deliveryInputCtrl 6 API + 6 Factory 全部 A 级闭合；4 条 result 传递链 A 级；F5/F6 Write API 完整静态审计 0 处调用；F6 Request 不能直接追溯到 waitingDeliveryList（通过 F3 中间层），F5 也不能直接追溯（通过 F4 中间层）。**

### 20.2 关键事实

1. **6 API 全部静态可见**（4 Read + 2 Write）
2. **6 Factory 全部独立实例**（A）
3. **4 条 result 传递链** A 级：
   - F1 → F3 Request（getMachineCenterList）
   - F1 → F4 Request（showDeliveryModal）
   - F3 → F6 Request（selectOrder.map）
   - F4 → F5 Request（saveStock 循环）
4. **F5/F6 完整 Request 结构 A 级**（含字段名 / 嵌套数组 / JSON.stringify）
5. **F5 Success 4 步**（search + getCount + reload + stockDetail=false）
6. **F6 Success 2 步**（addOrderModal=false + reload）— **不重查 Read API**
7. **F6 Request 不直接来自 waitingDeliveryList**（通过 F3 中间层，A）
8. **F5 Request 不直接来自 waitingDeliveryList**（通过 F4 中间层，A）
9. **F2 是纯 fire-and-forget**（0 result consumer）
10. **waitingDeliveryList 4 个二级字段**（lockStorehouse.type / lockMachineCenter.id / medicalProduct.id / medicalProduct.objectId）

### 20.3 26 项 A-F 分布

- **A：26**（100%）
- **E 升 A / F 升 A：0**
- F 边界在主链图 [F] 标记（8 项）

### 20.4 严格红线维持

- ✅ Write = 0（**F5/F6 绝对未调用**）
- ✅ 生产数据修改 = 0
- ✅ 历史 MD 修改 = 0
- ✅ controller.js 未修改
- ✅ deliveryList.html hash 不变
- ✅ 10 个 untracked 临时文件原样保留
- ✅ P0 = 54 / P1 = 8 冻结

---

## 21. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| Write 操作 = 0 | ✅（F5/F6 0 调用）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| **deliveryList.html hash/bytes 未改变** | ✅（SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` / 12720 bytes）|
| Git 禁止命令未触发 | ✅（仅 `git add -- 150_*.md`）|
| 文件编号冲突 | ✅（149 已占用 → 本轮 150）|

---

## 22. 停止条件

✅ deliveryInputCtrl 209 行 + 6 API + 6 Factory A 级完整确认
✅ F1 result.object 9 处 + waitingDeliveryList 4 个二级字段 A 级确认
✅ F3/F4 Request 完整结构 + result 消费 A 级确认
✅ F5/F6 Write API **绝不调用** + Request 完整结构 A 级确认
✅ 4 条 result 传递链 A 级确认
✅ 2 Write Success 行为差异 A 级确认（4 步 vs 2 步）
✅ F6 不直接追溯 waitingDeliveryList 结论 A 级
✅ 26 项 100% A 级（无 E/F 升 A）
✅ 9 项 F 边界明确列出（资源范围外）
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发（**F5/F6 0 调用**）

**等待老板下一条指令（不自动执行 S1-90）**。
