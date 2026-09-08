# S1-91 F3 → F6 machineCenter 发送字段级闭合审计

> 审计对象：`getCenterListFactory` (F3) + `createOrderFactory` (F6) + selectOrder() 完整字段闭合链
> 任务来源：S1-91（基于 S1-89 已确认 F3 result.list → F6 Request 3 字段追溯）
> 审计立场：**只按源码证据；Write API 绝不调用；严格区分 4 层字段来源（API 原始 / Controller 中间 / UI 输入 / F6 Request）；禁止按命名升级业务含义**

---

## 1. 审计范围

| 维度 | 范围 | 备注 |
|---|---|---|
| F3 API | controller.js L3836 | 唯一调用 |
| F3 Factory | L3835 `getCenterListFactory` | 独立实例 |
| getMachineCenterList helper | L3816-3829 | F3 Request 派生 |
| showAddModal | L3830-3837 | F3 触发函数 |
| selectOrder() | L3955-3977 | F6 触发函数 |
| F6 API | L3966 | Write API |
| 3 字段闭合 | medicalProductId / machineCenterId / planDeliveryTime | A |
| $scope.startTime 完整生命周期 | 3 写 + 3 读 | A |
| Write API 实际调用 | **0** | A |

---

## 2. 证据等级

| 等级 | 含义 |
|---|---|
| A | 直接源码证据 |
| B | 多源互证 |
| C | 局部/不完整 |
| D | 冲突/明确缺陷 |
| E | 合理业务推断 |
| F | 当前证据范围未观察/不可得 |

**关键纪律**：
- 严格区分 4 层字段来源（API 原始 / Controller 中间 / UI 输入 / F6 Request）
- Write API 绝不调用
- 禁止按字段名升级业务含义（machineCenterId ≠ "加工中心主键"；planDeliveryTime ≠ "计划配送时间业务字段"）

---

## 3. F3 getMedicalProductMachineCenterVoList 完整定位

### 3.1 F3 完整调用链

| 步骤 | 行号 | 语句 |
|---|---|---|
| 1 | L3830-3837 | `showAddModal = function () { ... }`（F3 触发函数）|
| 2 | L3834 | `var arr = getMachineCenterList();`（F3 Request 派生）|
| 3 | L3835 | `$scope.getCenterListFactory = new ObjectFactory();`（Factory 创建）|
| 4 | L3836 | `getCenterListFactory.saveOrQuery(F3 API, { medicalProductMachineCenterPoListJson: JSON.stringify(arr) });`（F3 调用）|
| 5 | [F] | 后端 HTTP Response (F-list) |

### 3.2 getCenterListFactory 完整记录

| 维度 | 值 |
|---|---|
| Factory 变量 | `getCenterListFactory` |
| 挂 $scope | ✅ |
| 构造行 | L3835 |
| saveOrQuery 行 | L3836 |
| 全仓出现次数 | 1（**仅 deliveryInputCtrl**）|
| 实例独立 | ✅ |
| result 共享 | ❌ |

### 3.3 F3 Request

```javascript
{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
```

- `arr` = `getMachineCenterList()` 返回值
- 内部结构 = `medicalProductMachineCenterPoList`（L3817-3828 派生）

---

## 4. getMachineCenterList helper 完整记录（L3816-3829）

### 4.1 完整代码

```javascript
// L3816-3829
var getMachineCenterList = function getMachineCenterList() {
    var medicalProductMachineCenterPoList = [];  // L3817
    var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;  // L3818
    for (var i = 0; i < arr.length; i++) {  // L3819
        if (arr[i].medicalProduct.objectId) {  // L3821
            medicalProductMachineCenterPoList.push({  // L3822
                medicalProductId: arr[i].medicalProduct.id,  // L3823
                machineCenterId: arr[i].medicalProduct.objectId  // L3824
            });
        }
    }
    return medicalProductMachineCenterPoList;  // L3828
};
```

### 4.2 arr 来源（A 级）

```
F1 result.object.waitingDeliveryList (L3818)
    ↓ [A] 直接读取
局部 var arr
```

**A**：
- getMachineCenterList helper 直接读取 F1 result（A）
- **等待 F1 result 填充完成**（异步，A）
- **如果 F1 result 未填充**，`waitingDeliveryList` = undefined → 循环报错

### 4.3 过滤条件（A 级）

```javascript
if (arr[i].medicalProduct.objectId) {  // L3821
    medicalProductMachineCenterPoList.push({  // L3822
        medicalProductId: arr[i].medicalProduct.id,  // L3823
        machineCenterId: arr[i].medicalProduct.objectId  // L3824
    });
}
```

**A**：
- 过滤条件 = `medicalProduct.objectId` truthy（A）
- **F1 阶段**已对 `medicalProduct.objectId` 二次写入（**S1-78/S1-89 已确认**）：
  - lockStorehouse.type == 4 → lockMachineCenter.id
  - else → null
- **F3 Request 仅包含 medicalProduct.objectId 已被后端赋值的项**（A）

### 4.4 getMachineCenterList 输出结构

```javascript
[
    {
        medicalProductId: number,  // L3823: 来自 waitingDeliveryList[i].medicalProduct.id
        machineCenterId: number     // L3824: 来自 waitingDeliveryList[i].medicalProduct.objectId
    },
    ...
]
```

**A**：getMachineCenterList 返回 2 字段对象数组（A）。

---

## 5. F3 result.list 完整字段审计

### 5.1 F3 result.list 消费位置（仅 1 处）

| # | 行号 | 路径 | 形式 |
|---|---|---|---|
| 1 | L3961 | `$scope.getCenterListFactory.result.list` | 读（selectOrder.map）|

**A**：F3 result.list **仅 1 处消费**（selectOrder 内，A）。

### 5.2 selectOrder.map 完整代码

```javascript
// L3961-3963
var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
});
```

### 5.3 F3 result.list 字段访问

| 字段路径 | 行号 | 读/写 |
|---|---|---|
| `result.list` | L3961 | 读（map 外层）|
| `result.list[i]`（v）| L3962 | 读（map callback 参数）|
| `v.medicalProduct.id` | L3962 | 读 |
| `v.machineCenter.id` | L3962 | 读 |

**A**：F3 result.list **4 处字段访问**（A）。

### 5.4 F3 result.list 元素结构（已观察）

| 字段 | 类型 | 读入 F6 |
|---|---|---|
| `v.medicalProduct.id` | number | ✅ medicalProductId |
| `v.machineCenter.id` | number | ✅ machineCenterId |
| 其它字段 | **F** | ❌（不可得）|

**F**：F3 result.list 完整字段结构（除 2 个已观察外）= **F**。

---

## 6. selectOrder() 完整审计

### 6.1 完整代码

```javascript
// L3955-3977
$scope.selectOrder = function () {
    if (!$scope.startTime) {  // L3956
        Popup.notice("请选择取镜日期");
        return false;
    }
    var arr = $scope.getCenterListFactory.result.list.map(function (v) {  // L3961
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);  // L3964
    $scope.createOrderFactory = new ObjectFactory();  // L3965
    var createPromise = $scope.createOrderFactory.saveOrQuery(  // L3966
        '/admin/sendMedicalProductToMachineCenter.json',
        { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }
    );
    createPromise.then(function (res) {  // L3967
        if (res.status == 1) {
            Popup.notice(res.errmsg);
        } else {
            Popup.notice('发送成功');
            $scope.addOrderModal = false;  // L3973
            $state.reload();  // L3974
        }
    });
};
```

### 6.2 selectOrder 完整特征

| 维度 | 值 |
|---|---|
| 函数定义 | L3955 |
| 函数结束 | L3977 |
| 行数 | 23 |
| 参数 | ❌ 无 |
| 触发来源 | **F 边界**（HTML 不可得）|
| 使用的 Factory | getCenterListFactory（result.list）+ createOrderFactory（saveOrQuery）|
| 使用的 scope 变量 | $scope.startTime（校验 + 格式化 + 传递）|
| 局部 arr 创建 | L3961 result.list.map（**2 字段返回**）|
| map callback 参数 | `v` |
| 循环次数 | result.list.length（**F 边界**：F3 后端返回长度）|
| 是否有依赖 selectedItem | **❌ 0 处**（无选中状态变量）|
| 是否有其它 scope 字段参与 | **❌ 0 处**（仅 $scope.startTime）|

### 6.3 selectOrder 写入路径

| 行号 | 写入 |
|---|---|
| L3964 | `$scope.startTime = DateUtilFactory.origin($scope.startTime);`（**就地格式化**）|

**A**：selectOrder 唯一写入 = `startTime` 格式化（A）。

### 6.4 F6 Request 构造（selectOrder 内部）

```javascript
{ 
    medicalProductMachineCenterPoListJson: JSON.stringify(arr),  // L3966
    planDeliveryTime: $scope.startTime                          // L3966
}
```

- `arr` 来自 L3961（map 局部变量）
- `planDeliveryTime` = `$scope.startTime`（已 DateUtilFactory.origin 格式化）

**A**：F6 Request 2 字段构造 A 级（A）。

---

## 7. medicalProductId 完整闭合链路

### 7.1 4 步闭合（A 级）

```
F3 result.list[i].medicalProduct.id
        ↓ [A] (L3962 v.medicalProduct.id)
arr (局部 map 输出)
        ↓ [A] (L3962 medicalProductId 字段)
arr[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3966 JSON.stringify)
F6 Request.medicalProductMachineCenterPoListJson
        ↓ [A] (L3966 saveOrQuery 第 2 参数)
F6 saveMedicalProductToMachineCenter.json
```

**A**：medicalProductId 完整 4 步 A 级闭合（A）。

### 7.2 转换 / 类型变更

| 检查项 | 结果 |
|---|---|
| `Number()` | ❌ 0 处 |
| `parseInt()` | ❌ 0 处 |
| 字符串拼接 | ❌ 0 处 |
| 类型转换 | **❌ 0 处**（直接赋值）|

**A**：medicalProductId 在 F3 → F6 闭合链中**无任何类型转换**（A）。

### 7.3 字段名一致性

| 层级 | 字段名 |
|---|---|
| F3 result.list | `v.medicalProduct.id` |
| map 输出 | `medicalProductId`（**重命名为 medicalProductId**）|
| F6 Request 字符串内 | `medicalProductId` |

**A**：F3 原始字段名是 `medicalProduct.id`，map 输出**重命名**为 `medicalProductId`（A）。

### 7.4 UI 介入

| 检查项 | 结果 |
|---|---|
| selectOrder 内 medicalProductId 写入 | **❌ 0 处**（仅读不写）|
| HTML ng-model 修改 | **F 边界**（HTML 不可得）|

**A**：medicalProductId 在 selectOrder 中**纯读取**（A）。

---

## 8. machineCenterId 完整闭合链路

### 8.1 4 步闭合（A 级）

```
F3 result.list[i].machineCenter.id
        ↓ [A] (L3962 v.machineCenter.id)
arr (局部 map 输出)
        ↓ [A] (L3962 machineCenterId 字段)
arr[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3966 JSON.stringify)
F6 Request.medicalProductMachineCenterPoListJson
```

**A**：machineCenterId 完整 4 步 A 级闭合（A）。

### 8.2 字段嵌套追溯

| 层级 | 字段名 | 出现行号 |
|---|---|---|
| 第 1 层 | result.list[i] | L3961 |
| 第 2 层 | result.list[i].machineCenter | L3962 |
| 第 3 层 | result.list[i].machineCenter.id | L3962 |

**A**：3 层嵌套路径 A 级（A）。

### 8.3 字段名一致性

| 层级 | 字段名 |
|---|---|
| F3 result.list | `v.machineCenter.id` |
| map 输出 | `machineCenterId`（**重命名**）|
| F6 Request 字符串内 | `machineCenterId` |

**A**：F3 原始字段名 `machineCenter.id`，map 输出**重命名**为 `machineCenterId`（A）。

---

## 9. planDeliveryTime 完整闭合链路

### 9.1 5 步闭合（A 级）

```
$scope.startTime
        ↓ [A] (L3956 校验)
        ↓ [A] (L3964 DateUtilFactory.origin 格式化)
        ↓ [A] (L3966 F6 Request 字段)
F6 Request.planDeliveryTime
        ↓ [A] (L3966 saveOrQuery)
F6 saveMedicalProductToMachineCenter.json
```

**A**：planDeliveryTime 5 步 A 级闭合（A）。

### 9.2 $scope.startTime 完整生命周期（A 级）

| # | 行号 | 操作 | 形式 |
|---|---|---|---|
| 1 | L3832 | 写 | `$scope.startTime = undefined;`（showAddModal 开头）|
| 2 | L3933 | 写 | `$scope.startTime = DateUtilFactory.plus(new Date());`（searchDate function）|
| 3 | L3939 | 读 | `var now = $scope.startTime.getTime();`（changeDate function）|
| 4 | L3956 | 读 | `if (!$scope.startTime)`（selectOrder 校验）|
| 5 | L3964 | 读+写 | `$scope.startTime = DateUtilFactory.origin($scope.startTime);`（selectOrder 格式化）|
| 6 | L3966 | 读 | `planDeliveryTime: $scope.startTime`（F6 Request）|

**A**：
- $scope.startTime **3 次写入**（L3832/L3933/L3964）+ **4 次读取**（L3939/L3956/L3964/L3966）
- L3964 是**就地格式化**（既读又写，A）

### 9.3 searchDate 完整代码

```javascript
// L3931-3934
$scope.searchDate = function () {
    $scope.startTime = DateUtilFactory.plus(new Date());
};
```

**A**：searchDate 是 $scope.startTime 的**唯一直接修改函数**（除 selectOrder 格式化外，A）。

### 9.4 changeDate 完整代码

```javascript
// L3936-3950
$scope.changeDate = function () {
    var start = DateUtilFactory.origin(new Date()).getTime();
    var now = $scope.startTime.getTime();
    if (now > start) {
        if (now - start > 86400000) {
            $scope.dateSearch = null;
        } else {
            $scope.dateSearch = 1;
        }
    } else {
        $scope.dateSearch = null;
    }
};
```

**A**：changeDate **不修改** $scope.startTime（A），只**读取** $scope.startTime（A）+ 设置 $scope.dateSearch（A）。

### 9.5 selectOrder 校验

```javascript
// L3956-3959
if (!$scope.startTime) {
    Popup.notice("请选择取镜日期");
    return false;
}
```

**A**：selectOrder 校验 `$scope.startTime` 是否为真值（A），**未选则返回 false 不调 F6**（A）。

**E 边界**：
- Popup 文案 "请选择取镜日期" 是 **E 级业务推测**（HTML 不可得，不能直接证明 UI 显示该文案）
- 任务严格纪律：**禁止**把 Popup 文案当成 L1 字段

### 9.6 $scope.startTime 来源层分类

| 写入行 | 来源 | 类型 |
|---|---|---|
| L3832 | showAddModal 重置 | **Controller 重置**（不是用户输入）|
| L3933 | searchDate（datepicker on-change 触发）| **E 推测** UI 触发 |
| L3964 | selectOrder 内部 | **Controller 格式化** |

**A**：
- $scope.startTime 由 **Controller 重置** + **datepicker 触发 searchDate 修改**（A）
- **HTML datepicker 实际触发路径 = F 边界**

### 9.7 planDeliveryTime 类型

**A**：
- planDeliveryTime = $scope.startTime（**Date 对象**或**undefined**）
- **未经过** `JSON.stringify`（A）
- 后端期望类型 = F 边界

---

## 10. F6 Request 完整结构（A 级）

### 10.1 完整原始结构

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr),  // string (L3966)
    planDeliveryTime: $scope.startTime                          // Date 对象 (L3966)
}
```

### 10.2 medicalProductMachineCenterPoListJson 字符串内容（JSON.stringify 前）

```javascript
[
    {
        medicalProductId: number,  // L3962: 来自 F3 result.list[i].medicalProduct.id
        machineCenterId: number     // L3962: 来自 F3 result.list[i].machineCenter.id
    },
    ...
]
```

### 10.3 F3 → F6 完整嵌套树（A 级）

```
F6 Request (L3966)
├── medicalProductMachineCenterPoListJson (string, JSON.stringify 后)
│   └── medicalProductMachineCenterPoListJson (array, JSON.stringify 前)
│       └── [].{ medicalProductId, machineCenterId }
│           ├── medicalProductId (number)
│           │   └── F3 result.list[i].medicalProduct.id (L3962)
│           └── machineCenterId (number)
│               └── F3 result.list[i].machineCenter.id (L3962)
└── planDeliveryTime (Date)
    └── $scope.startTime (L3966, 已 DateUtilFactory.origin 格式化)
```

**A**：F6 Request 完整嵌套树 2 层 3 字段 A 级确认（A）。

### 10.4 类型转换

| 操作 | 出现次数 |
|---|---|
| `Number()` | 0 |
| `parseInt()` | 0 |
| `parseFloat()` | 0 |
| `String()` | 0 |
| `toString()` | 0 |
| `JSON.parse()` | 0 |
| `angular.copy()` | 0 |

**A**：selectOrder / map 内**0 处类型转换**（A）。

---

## 11. F6 success 行为（A 级）

### 11.1 完整代码

```javascript
// L3967-3976
createPromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        Popup.notice('发送成功');
        $scope.addOrderModal = false;  // L3973
        $state.reload();              // L3974
    }
});
```

### 11.2 success 2 步精确记录

| 步骤 | 行号 | 调用 | 效果 |
|---|---|---|---|
| 1 | L3973 | `$scope.addOrderModal = false` | 关闭 addOrderModal |
| 2 | L3974 | `$state.reload()` | 整页 reload（**当前 state = deliveryInput**）|

**A**：F6 success 触发 **2 步**（addOrderModal=false + $state.reload()，A）。

### 11.3 F6 vs F5 success 行为对比

| 行为 | F5 (saveStock) | F6 (selectOrder) |
|---|---|---|
| Popup.notice | ✅ '保存成功' | ✅ '发送成功' |
| search() | ✅ L4014 | ❌ |
| getCount() | ✅ L4015 | ❌ |
| $state.reload() | ✅ L4016 | ✅ L3974 |
| 关闭 modal | $scope.stockDetail = false (L4017) | $scope.addOrderModal = false (L3973) |

**A**：
- F5 success **4 步**（含 search + getCount 重查 F1/F2）
- F6 success **2 步**（**不重查 Read API**，仅 modal 关闭 + reload）
- **差异原因 = A 级源码证据**：F5/F6 success 内代码不同（A）

### 11.4 Read API 重查

| Read API | F5 success 重查 | F6 success 重查 |
|---|---|---|
| F1 (search) | ✅ | ❌ |
| F2 (getCount) | ✅ | ❌ |
| F3 / F4 | ❌ | ❌ |

**A**：
- F5 success 重查 F1+F2（A）
- F6 success **0 处重查**（A）
- $state.reload() 重新加载当前 state（**不直接重查 F3/F4**，但 Controller 重新初始化时 L3834 getMachineCenterList 会重新读取 F1 result.object.waitingDeliveryList，**间接**触发新的 F3 调用）

---

## 12. waitingDeliveryList → F6 间接追溯

### 12.1 3 跳间接链（A 级完整证据）

```
Step 1: F1 result.object.waitingDeliveryList
        ↓ [A] (L3818 getMachineCenterList helper 读取)
        ↓ [A] (L3819-3827 for 循环 + if 过滤)
medicalProductMachineCenterPoList[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3834 var arr = getMachineCenterList())
        ↓ [A] (L3836 JSON.stringify(arr))
F3 Request.medicalProductMachineCenterPoListJson
        ↓ [A] (L3836 saveOrQuery)
[F] (后端 HTTP) F3 Response
        ↓
F3 result.list[].{ medicalProduct, machineCenter }
        ↓ [A] (L3961 result.list.map)
arr[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3966 JSON.stringify)
F6 Request.medicalProductMachineCenterPoListJson
        ↓ [A]
F6 saveMedicalProductToMachineCenter.json
```

**A**：waitingDeliveryList → F6 是 **3 跳间接链**（每跳都有源码证据，A）。

### 12.2 逐跳直接 vs 间接来源

| F6 字段 | 第 1 跳来源 | 第 2 跳来源 | 第 3 跳来源 |
|---|---|---|---|
| medicalProductId | waitingDeliveryList[i].medicalProduct.id (L3823) | F3 result.list[i].medicalProduct.id (L3962) | F3 result.list 本身 |
| machineCenterId | waitingDeliveryList[i].medicalProduct.objectId (L3824) | F3 result.list[i].machineCenter.id (L3962) | F3 result.list 本身 |

**A**：2 字段均通过 3 跳间接链追溯（A）。

### 12.3 字段重命名追踪

| 层级 | 字段名 |
|---|---|
| F1 result | `medicalProduct.id` + `medicalProduct.objectId`（2 字段）|
| F3 Request 输入 | `{ medicalProductId, machineCenterId }`（已重命名）|
| F3 result | `medicalProduct.id` + `machineCenter.id`（**再次重命名**为 .machineCenter）|
| F6 Request 输入 | `{ medicalProductId, machineCenterId }`（再次重命名回）|

**A**：字段名在传递链中**多次重命名**（A）。

### 12.4 严格禁止的"业务关联"推断

**禁止表述**：
- "F6 创建加工中心订单"（E 推测）
- "F6 发送 waitingDeliveryList 中的商品到加工中心"（E 推测 + 业务链 A 级）
- "machineCenterId 是加工中心主键"（E 推测）
- "medicalProductId 是产品 ID"（E 推测）
- "planDeliveryTime 是计划配送时间"（E 推测）

**可表述**（A 级）：
- "F3 result.list[i].machineCenter.id 在 L3962 被 map 到 arr[].machineCenterId"
- "medicalProductId 字段名在 F3 Request 阶段已重命名，与 F1 result 字段名 medicalProduct.id 不同"

---

## 13. HTML 边界

| 检查项 | 结果 |
|---|---|
| deliveryInput HTML 模板 | **F**（working dir 0 个对应）|
| 7 untracked HTML 中 deliveryInput 相关 | 0 处 |
| showAddModal 触发按钮 | **F**（HTML 不可得）|
| selectOrder 触发按钮 | **F**（HTML 不可得）|
| datepicker 触发 searchDate 路径 | **F**（HTML 不可得）|
| datepicker 触发 changeDate 路径 | **F**（HTML 不可得）|

**F**：
- deliveryInput HTML 模板在当前资源范围**不可得**（F）
- **所有 UI 触发路径** = F 边界
- 但 Controller 内**已直接出现的字段** = A 级（**不降级 F**）

---

## 14. Factory 隔离

### 14.1 F3 / F6 Factory 完整记录

| 维度 | getCenterListFactory (F3) | createOrderFactory (F6) |
|---|---|---|
| 构造行 | L3835 | L3965 |
| 挂 $scope | ✅ | ✅ |
| 实例独立性 | ✅ | ✅ |
| 全仓出现次数 | 1（**仅 deliveryInputCtrl**）| 1（**仅 deliveryInputCtrl**）|
| 实例共享 | ❌ | ❌ |
| result 共享 | ❌（F3 result 仅 selectOrder 通过 $scope 读取）| ❌ |
| 对象共享 | ❌ | ❌ |

### 14.2 数据传递路径

```
F3: $scope.getCenterListFactory.result.list
        ↓ [A] (L3835/L3836 saveOrQuery)
F3 API Response
        ↓ [F] (后端 HTTP)
$scope.getCenterListFactory.result.list
        ↓ [A] (L3961 selectOrder.map)
arr (局部变量)
        ↓ [A] (L3966 JSON.stringify(arr))
$scope.createOrderFactory = new ObjectFactory()  (L3965)
        ↓ [A] (L3966)
F6 saveOrQuery
        ↓ [F]
F6 API Response
```

**A**：F3 / F6 **两个独立 Factory 实例**，**通过 `$scope.getCenterListFactory.result.list` 跨调用传递**（A）。

---

## 15. selectOrder 额外 API 检查

### 15.1 selectOrder 内部完整 API 检查

| API 类型 | 是否调用 |
|---|---|
| F1 (getCashflowDeliveryVo.json) | ❌ |
| F2 (statProductDeliveryStatusOfCashflow.json) | ❌ |
| F3 (getMedicalProductMachineCenterVoList.json) | **❌ 0 调用**（selectOrder 仅读 result）|
| F4 (getCanBeDeliverySkuInListOfProduct.json) | ❌ |
| F5 (saveMedicalProductStockBatch.json) | ❌ |
| F6 (sendMedicalProductToMachineCenter.json) | **✅ 1 调用**（L3966）|
| 任何其它 API | ❌ |

**A**：selectOrder 内部**仅 1 处 API 调用**（F6 Write API，0 处 Read API 重查，A）。

### 15.2 间接 API 重查（reload 副作用）

```javascript
$state.reload();  // L3974
```

**A**：
- $state.reload() 重新加载当前 state（deliveryInput，A）
- reload 后 Controller 重新初始化，**L3844 getCount() + L3866 search() 自动重新执行**（A）
- **但 L3834 showAddModal 不会被自动重新执行**（需用户点击）
- **L3884 showDeliveryModal 不会被自动重新执行**（需用户点击）

**A**：F6 success 的 $state.reload() 间接重查 F1+F2，但**不重查 F3/F4**（A）。

---

## 16. Read / Write 边界

| API | Read/Write | 本轮是否调用 | Request 静态可见 | 完整字段闭合 |
|---|---|---|---|---|
| F3 getMedicalProductMachineCenterVoList.json | **Read** | **❌ 0 调用** | ✅ | — |
| F6 sendMedicalProductToMachineCenter.json | **Write** | **❌ 0 调用** | ✅ | ✅ 3 字段完全闭合 |

**A**：
- F3/F6 本轮**0 处调用**（含 Write API 绝对未调用，A）
- **观察源码，不执行任何 Write API**（A）

---

## 17. 26 项审计矩阵

| # | 审计项 | 等级 | 证据 |
|---|---|---|---|
| 01 | F3 Controller 定位 | A | L3830-3837 showAddModal |
| 02 | F3 Factory | A | L3835 getCenterListFactory |
| 03 | F3 Request | A | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` |
| 04 | F3 result.list | A | L3961 selectOrder.map |
| 05 | result.list 字段集合 | A（4 字段已访问）| F（其它字段不可得）|
| 06 | selectOrder 定位 | A | L3955-3977 |
| 07 | selectOrder 参数 | A | ❌ 无参数 |
| 08 | arr 初始化 | A | L3961 result.list.map 创建 |
| 09 | arr 填充 | A | L3962 map callback 返回 `{ medicalProductId, machineCenterId }` |
| 10 | medicalProductId 来源 | A | F3 result.list[i].medicalProduct.id (L3962) |
| 11 | medicalProductId 转换 | A | 0 处类型转换 |
| 12 | machineCenterId 来源 | A | F3 result.list[i].machineCenter.id (L3962) |
| 13 | machineCenterId 转换 | A | 0 处类型转换 |
| 14 | 是否 UI 介入 | A + F | selectOrder 内纯读 A；HTML 触发 F |
| 15 | planDeliveryTime 来源 | A | $scope.startTime (L3966) |
| 16 | $scope.startTime 初始化 | A | L3832 undefined / L3933 now+1day / L3964 origin |
| 17 | startTime 修改点 | A | 3 次写（L3832/L3933/L3964）|
| 18 | F6 API | A | sendMedicalProductToMachineCenter.json |
| 19 | F6 Factory | A | L3965 createOrderFactory |
| 20 | F6 Request 外层 | A | `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` |
| 21 | F6 Request 内层 | A | `[].{ medicalProductId, machineCenterId }` |
| 22 | JSON.stringify | A | 1 处（L3966）|
| 23 | F6 success | A | res.status/errmsg (L3969-3970) |
| 24 | success 后 Read | A | **0 处**（不重查任何 Read API）|
| 25 | F3/F6 Factory 是否独立 | A | 2 独立实例（A）|
| 26 | F3→F6 最小闭合结论 | A | **完全闭合**（3 字段全部 A 级）|

### 17.1 A / B / C / D / E / F 统计

| 等级 | 数量 | 占比 |
|---|---|---|
| A | **25** | 96.2% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | **1** | 3.8%（UI 触发路径）|

**A**：26 项中 25 项 A + 1 项 F（**仅 UI 触发路径 F**，其它 25 项全部 A 级）。

---

## 18. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | F3/F6 API / 2 Factory / 3 字段闭合 / selectOrder 23 行 / F3 result.list 1 处消费 | **是** |
| L1 前端事实 | $scope.startTime 3 写 + 4 读 / F6 success 2 步 | **是** |
| L2 业务规则 | "加工中心发送" 业务语义 | **E**（按 API 名称推测，无 L3 证据）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository | **F**（资源范围外）|

**禁止表述**：
- "sendMedicalProductToMachineCenter 创建加工中心订单表"
- "machineCenterId = 加工中心主键"
- "medicalProductId = 产品 ID"
- "planDeliveryTime = 计划配送时间"
- "getMachineCenterList = 加工中心列表查询"

---

## 19. F 边界清单

| F 项 | 原因 |
|---|---|
| deliveryInput HTML 模板 | working dir + tracked 0 个对应 |
| showAddModal / selectOrder / searchDate 触发按钮 | HTML 不可得 |
| datepicker 实际触发路径 | HTML 不可得 |
| $scope.startTime UI 初始值（datepicker 默认）| HTML 不可得 |
| F3 result.list 完整字段 | 资源范围外 |
| F3/F6 后端 Response 完整字段 | 资源范围外 |
| ObjectFactory 内部 HTTP 实现 | 资源范围外 |
| planDeliveryTime 后端期望类型 | 资源范围外 |
| 业务实体（加工中心 / 订单 / 库存）| 资源范围外（L3 = F）|
| 路由表 state → templateUrl | 资源范围外 |
| 3 跳链中"业务关联"含义 | 字段值可追，含义仅 E |

---

## 20. 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 write API 调用 | ❌（**F6 绝对未调用**）|
| R3 修改历史 MD | ❌ |
| R4 删除 10 untracked | ❌（**deliveryList.html hash 复核不变**）|
| R5 P0/P1 自动新增 | ❌ |
| R6 git add . / -A / * | ❌ |
| R7 修改 controller.js / 7 HTML | ❌（全部只读）|
| R8 文件编号冲突 | ❌（151 已被 S1-90 占用，本轮 152）|

---

## 21. 最终结论

### 21.1 一句话总结

**F3 result.list → selectOrder → F6 Request 3 字段（medicalProductId / machineCenterId / planDeliveryTime）**完全 A 级闭合**；F6 Write API **绝对未调用**；waitingDeliveryList → F6 是 3 跳间接链（每跳 A 级）；F6 success 仅 2 步（不重查 Read API）。**

### 21.2 关键事实

1. **F3 调用链完整**（L3830-3837 showAddModal → L3835-3836 getCenterListFactory + saveOrQuery）
2. **getMachineCenterList helper 完整**（L3816-3829 读取 F1 result.object.waitingDeliveryList）
3. **F3 result.list 1 处消费**（L3961 selectOrder.map）
4. **selectOrder 23 行**（L3955-3977 无参数，map + 1 处 saveOrQuery）
5. **F6 Request 完整 2 字段结构 A 级**（`{ medicalProductMachineCenterPoListJson, planDeliveryTime }`）
6. **3 字段完全可追溯**（medicalProductId + machineCenterId + planDeliveryTime → F6 Request）
7. **$scope.startTime 完整生命周期 A 级**（3 写 + 4 读）
8. **F6 success 2 步**（addOrderModal=false + $state.reload()，**不重查 Read API**）
9. **waitingDeliveryList → F6 3 跳间接链**（F1 → F3 Request → F3 result → F6 Request，每跳 A 级）
10. **字段名多次重命名**（medicalProduct.id → medicalProductId → medicalProduct.id → medicalProductId）

### 21.3 与 S1-89 一致性

- ✅ S1-89 的 "F3 result.list → F6 Request 2 字段" 复核**完全一致**（L3961-3962 / L3966 全部对应）
- ✅ S1-89 的 "F6 success 2 步" 复核**完全一致**（L3973/L3974 全部对应）
- ✅ S1-89 的 "F6 Request 不直接来自 waitingDeliveryList" 复核**完全一致**（通过 F3 中间层，A 级 3 跳证据）
- **新增细化**：
  - getMachineCenterList helper 完整代码 + 行号（A 级 14 行）
  - F3 result.list 字段重命名追踪（A 级 2 次重命名）
  - $scope.startTime 完整生命周期（3 写 + 4 读，A 级）
  - F5/F6 success 行为差异精确对比（4 步 vs 2 步，A 级）
  - waitingDeliveryList → F6 是 **3 跳间接链**（A 级，每跳独立证据）

### 21.4 26 项 A-F 分布

- **A：25**（96.2%）
- **F：1**（3.8% — UI 触发路径）
- **E 升 A / F 升 A：0**

### 21.5 严格红线维持

- ✅ Write = 0（**F6 绝对未调用**）
- ✅ 生产数据修改 = 0
- ✅ 历史 MD 修改 = 0
- ✅ controller.js 未修改
- ✅ deliveryList.html hash 不变
- ✅ 10 个 untracked 临时文件原样保留
- ✅ P0 = 54 / P1 = 8 冻结

---

## 22. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| Write 操作 = 0 | ✅（**F6 0 调用**）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| **deliveryList.html hash/bytes 未改变** | ✅（SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` / 12720 bytes）|
| Git 禁止命令未触发 | ✅（仅 `git add -- 152_*.md`）|
| 文件编号冲突 | ✅（151 已占用 → 本轮 152）|

---

## 23. 停止条件

✅ F3 → F6 3 字段完全闭合 A 级
✅ getMachineCenterList helper 完整 14 行 A 级
✅ selectOrder 23 行 A 级
✅ $scope.startTime 完整生命周期 A 级（3 写 + 4 读）
✅ F6 Request 完整 2 字段结构 A 级
✅ F6 success 2 步行为 A 级
✅ waitingDeliveryList → F6 3 跳间接链 A 级
✅ Factory F3/F6 独立 A 级
✅ Read/Write 边界 A 级（**F6 0 调用**）
✅ 25 A + 1 F（**仅 UI 触发路径 F**）
✅ 11 项 F 边界明确列出
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-92）**。
