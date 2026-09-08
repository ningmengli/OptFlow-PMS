# S1-93 F1 waitingDeliveryList → F3/F4 入口字段级闭合审计

> 审计对象：`deliveryInputCtrl` L3812-4021（209 行）+ F1 waitingDeliveryList → F3/F4 Request 入口字段级闭合
> 任务来源：S1-93（基于 S1-89/90/91/92 已完成 F3/F4/F5/F6 字段级闭合）
> 审计立场：**只按源码证据；严格区分同一 waitingDeliveryList 不同入口字段消费差异；禁止按命名升级业务含义；Write API 绝不调用**

---

## 1. 审计范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryInputCtrl | L3812-4021（**209 行**）| 完整二次确认 |
| F1 waitingDeliveryList 全仓消费 | **7 处**（L3818/L3851/L3854/L3856/L3870/L3893/L3910）| A |
| F3 Request 入口（getMachineCenterList）| L3816-3829 + L3834-3836 | A |
| F4 Request 入口（showDeliveryModal）| L3868-3886 | A |
| F1 原对象修改 | L3854/L3856（**2 处写入**）| A |
| 过滤/去重/排序/类型转换 | ❌ 0 处 | A |
| UI 触发 | F（HTML 不可得）| F |
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
- 严格区分"F1 waitingDeliveryList 二次写入前/后"的字段值
- F3/F4 过滤条件**互补**（A 级 L3821 vs L3873）
- 不按字段名升级业务含义
- Write API 绝不调用

---

## 3. F1 waitingDeliveryList 来源（A 级）

### 3.1 F1 调用链

```javascript
// L3846-3866
var search = function search() {
    $scope.getMedicalRecordDeliveryFactory = new ObjectFactory();  // L3847
    var deliveryPromise = $scope.getMedicalRecordDeliveryFactory.saveOrQuery(  // L3848
        '/admin/getCashflowDeliveryVo.json',
        { cashflowId: $scope.cashflowId }
    );
    deliveryPromise.then(function (res) {  // L3849
        var arr = res.result.object.waitingDeliveryList;  // L3851
        for (var i = 0; i < arr.length; i++) {
            if (arr[i].lockStorehouse.type == 4) {  // L3853
                $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;  // L3854
            } else {
                $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;  // L3856
            }
        }
        if (!arr.length) {  // L3859
            Popup.notice('您的待发货项目已分拣完毕，即将返回列表', 1500, function () {
                $state.go('deliveryList');
            });
        }
    });
};
search();  // L3866
```

### 3.2 F1 waitingDeliveryList 唯一来源

**A**：
- F1 waitingDeliveryList 唯一来源 = `res.result.object.waitingDeliveryList`（L3851）
- F1 API = `getCashflowDeliveryVo.json`（L3848）
- Factory = `getMedicalRecordDeliveryFactory`（L3847）
- Request = `{ cashflowId: $scope.cashflowId }`（L3848）

### 3.3 F1 waitingDeliveryList 数据流

```
F1 API (getCashflowDeliveryVo.json)
    ↓ [A] (L3848 saveOrQuery)
getMedicalRecordDeliveryFactory = new ObjectFactory()
    ↓ [A] (L3849 .then)
res (F1 Response)
    ↓ [A] (L3851)
res.result.object.waitingDeliveryList
    ↓ [A] (L3853-3857 二次写入)
$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList
        （**被 controller 修改后的值**）
    ↓ [A] (L3866 search() 立即执行)
    ↓ [A] (后续 7 处消费)
```

**A**：F1 waitingDeliveryList 完整数据流 5 步 A 级（A）。

---

## 4. waitingDeliveryList 全部 7 处 Consumer

### 4.1 完整 Consumer 矩阵（A 级）

| # | 行号 | 表达式 | 读/写 | 用途 | 关联 Request |
|---|---|---|---|---|---|
| 1 | L3818 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | **读** | getMachineCenterList helper | **F3 Request 入口** |
| 2 | L3851 | `res.result.object.waitingDeliveryList` | 读 | search().then（局部 var arr）| 二次写入准备 |
| 3 | L3854 | `result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id` | **写** | then 回调二次写入 | — |
| 4 | L3856 | `result.object.waitingDeliveryList[i].medicalProduct.objectId = null` | **写** | then 回调二次写入 | — |
| 5 | L3870 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | 读 | showDeliveryModal | **F4 Request 入口** |
| 6 | L3893 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | 读 | isSendProduct | UI 校验 |
| 7 | L3910 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | 读 | isSendCenter | UI 校验 |

**A**：F1 waitingDeliveryList **7 处访问**（A），5 读 + 2 写。

### 4.2 7 处访问字段路径详表（A 级）

| # | 行号 | 完整字段路径 |
|---|---|---|
| 1 | L3818 | `result.object.waitingDeliveryList`（读）|
| 2 | L3851 | `res.result.object.waitingDeliveryList`（读）|
| 3 | L3854 | `result.object.waitingDeliveryList[i].medicalProduct.objectId`（**写**）|
| 4 | L3856 | `result.object.waitingDeliveryList[i].medicalProduct.objectId`（**写**）|
| 5 | L3870 | `result.object.waitingDeliveryList`（读）|
| 6 | L3893 | `result.object.waitingDeliveryList`（读）|
| 7 | L3910 | `result.object.waitingDeliveryList`（读）|

**A**：F1 waitingDeliveryList **完整访问路径**A 级（A）。

### 4.3 L3854/L3856 二次写入详细（A 级关键发现）

**A**：
- L3854 写入条件：`arr[i].lockStorehouse.type == 4`
- L3854 写入值：`arr[i].lockMachineCenter.id`（注：**写入的是 lockMachineCenter.id，不是 medicalProduct.objectId 自身**）
- L3856 写入条件：else（lockStorehouse.type != 4）
- L3856 写入值：`null`

**A**：F1 waitingDeliveryList **被 controller 修改 medicalProduct.objectId 字段**（L3854/L3856 写，A）。

**F**：
- 业务上 "lockStorehouse.type == 4 表示某种状态" = **F 边界**（无 L3 证据）
- 业务上 "lockMachineCenter.id 是某种 ID" = **F 边界**
- 严格禁止按命名升级

---

## 5. F3 Request 入口：getMachineCenterList 完整审计

### 5.1 完整代码

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

### 5.2 getMachineCenterList 完整特征

| 维度 | 值 |
|---|---|
| 函数定义 | L3816 |
| 函数结束 | L3829 |
| 行数 | 13 |
| 参数 | ❌ 无 |
| 触发来源 | L3834 `var arr = getMachineCenterList();`（showAddModal 内）|
| 数据源 | F1 waitingDeliveryList（L3818）|
| 过滤条件 | `arr[i].medicalProduct.objectId` truthy（L3821）|
| 读取字段 | `arr[i].medicalProduct.id` + `arr[i].medicalProduct.objectId` |
| 输出字段 | `medicalProductId` + `machineCenterId` |
| 去重 | **❌ 0 处** |
| 排序 | **❌ 0 处** |
| 类型转换 | **❌ 0 处** |
| 一对多展开 | **❌ 0 处**（每 i 仅 push 0/1 元素）|

### 5.3 F3 Request 构造

```javascript
// L3834-3837
var arr = getMachineCenterList();  // L3834
$scope.getCenterListFactory = new ObjectFactory();  // L3835
$scope.getCenterListFactory.saveOrQuery(  // L3836
    '/admin/getMedicalProductMachineCenterVoList.json',
    { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
);
```

**A**：F3 Request 字段 = `medicalProductMachineCenterPoListJson: JSON.stringify(arr)`（A）。

### 5.4 F3 medicalProductId 字段级闭合

```
F1 waitingDeliveryList[i].medicalProduct.id
        ↓ [A] (L3818 读取 waitingDeliveryList)
        ↓ [A] (L3823 arr[i].medicalProduct.id 直接读取)
medicalProductMachineCenterPoList[].medicalProductId
        ↓ [A] (L3834 var arr = getMachineCenterList())
        ↓ [A] (L3836 JSON.stringify)
F3 Request.medicalProductMachineCenterPoListJson
```

**A**：F3 medicalProductId 4 步 A 级完全闭合（A）。

### 5.5 F3 machineCenterId 字段级闭合

```
F1 waitingDeliveryList[i].medicalProduct.objectId
        ↓ [A] (L3818)
        ↓ [A] (L3824 arr[i].medicalProduct.objectId 直接读取)
medicalProductMachineCenterPoList[].machineCenterId
        ↓ [A] (L3834)
        ↓ [A] (L3836 JSON.stringify)
F3 Request.medicalProductMachineCenterPoListJson
```

**A**：F3 machineCenterId 4 步 A 级完全闭合（A）。

**重要说明**：`machineCenterId` 字段值来源 = **`medicalProduct.objectId` 字段**（不是 `lockMachineCenter.id` 字段），A 级。

### 5.6 F3 过滤条件深度分析

```javascript
if (arr[i].medicalProduct.objectId) {  // L3821
```

**A**：
- 过滤条件 = `medicalProduct.objectId` truthy（A）
- **依赖 L3854/L3856 二次写入**（A）
- 二次写入后，`objectId` = `lockMachineCenter.id`（type==4 分支）或 `null`（else 分支）
- 过滤后 `objectId truthy` 的项进入 F3 Request
- 过滤后 `objectId == null` 的项**不进入** F3 Request（**进入 F4 Request**）

**A**：F3 过滤 = `objectId truthy`（L3821）。

---

## 6. F4 Request 入口：showDeliveryModal 完整审计

### 6.1 完整代码

```javascript
// L3868-3886
$scope.showDeliveryModal = function () {
    var medicalProductIdArray = [];  // L3869
    var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;  // L3870
    for (var i = 0; i < arr.length; i++) {  // L3871
        if (arr[i].medicalProduct.objectId == null) {  // L3873
            medicalProductIdArray.push(arr[i].medicalProduct.id);  // L3874
        }
    }
    if (!medicalProductIdArray.length) {  // L3878
        Popup.notice("请选择发货的商品");
        return false;
    }
    $scope.stockDetail = true;  // L3882
    $scope.getDeliveryListFactory = new ObjectFactory();  // L3884
    $scope.getDeliveryListFactory.saveOrQuery(  // L3885
        '/admin/getCanBeDeliverySkuInListOfProduct.json',
        { medicalProductIdArray: medicalProductIdArray }
    );
};
```

### 6.2 showDeliveryModal 完整特征

| 维度 | 值 |
|---|---|
| 函数定义 | L3868 |
| 函数结束 | L3886 |
| 行数 | 19 |
| 参数 | ❌ 无 |
| 触发来源 | **F 边界**（HTML 不可得）|
| 数据源 | F1 waitingDeliveryList（L3870）|
| 过滤条件 | `arr[i].medicalProduct.objectId == null`（L3873）|
| 读取字段 | 仅 `arr[i].medicalProduct.id`（L3874）|
| 输出字段 | `medicalProductId`（仅 id）|
| 去重 | **❌ 0 处** |
| 排序 | **❌ 0 处** |
| 类型转换 | **❌ 0 处** |
| 一对多展开 | **❌ 0 处** |
| 提前返回 | `if (!medicalProductIdArray.length) { Popup + return false; }`（L3878-3881）|

### 6.3 F4 Request 构造

```javascript
{ medicalProductIdArray: medicalProductIdArray }  // L3885
```

- `medicalProductIdArray` = number[] 数组
- 数组元素 = `arr[i].medicalProduct.id`（L3874）

**A**：F4 Request 字段 = `medicalProductIdArray: number[]`（A）。

### 6.4 F4 medicalProductIdArray 字段级闭合

```
F1 waitingDeliveryList[i].medicalProduct.id
        ↓ [A] (L3870 读取 waitingDeliveryList)
        ↓ [A] (L3874 arr[i].medicalProduct.id 直接读取)
medicalProductIdArray[n]
        ↓ [A] (L3885 saveOrQuery 第 2 参数)
F4 Request.medicalProductIdArray
```

**A**：F4 medicalProductIdArray 3 步 A 级完全闭合（A）。

### 6.5 F4 过滤条件深度分析

```javascript
if (arr[i].medicalProduct.objectId == null) {  // L3873
```

**A**：
- 过滤条件 = `medicalProduct.objectId == null`（A）
- **依赖 L3854/L3856 二次写入**（A）
- 过滤后 `objectId == null` 的项进入 F4 Request
- 过滤后 `objectId truthy` 的项**不进入** F4 Request（**进入 F3 Request**）

**A**：F4 过滤 = `objectId == null`（L3873）。

### 6.6 F4 提前返回条件

```javascript
if (!medicalProductIdArray.length) {  // L3878
    Popup.notice("请选择发货的商品");
    return false;
}
```

**A**：
- 若 F4 过滤后 `medicalProductIdArray` 为空 → 弹"请选择发货的商品" + return false（**不调 F4 API**）
- 这是 **F4 调用的硬条件**（A）

---

## 7. F3 vs F4 关键差异（A 级）

### 7.1 F3 与 F4 完整对比表

| 维度 | F3 (getMachineCenterList) | F4 (showDeliveryModal) |
|---|---|---|
| 函数定义 | L3816 | L3868 |
| 行数 | 13 | 19 |
| 数据源 | F1 waitingDeliveryList (L3818) | F1 waitingDeliveryList (L3870) |
| **同一对象** | ✅ 是 | ✅ 是 |
| 触发时机 | showAddModal 触发 (L3834) | showDeliveryModal 触发 (L3868) |
| **过滤条件** | `medicalProduct.objectId` **truthy** (L3821) | `medicalProduct.objectId` **== null** (L3873) |
| **过滤关系** | **A 分支** | **B 分支**（**与 F3 互补**）|
| 读取字段 1 | `medicalProduct.id` (L3823) | `medicalProduct.id` (L3874) |
| 读取字段 2 | `medicalProduct.objectId` (L3824) | ❌ 不读 |
| 输出字段 1 | `medicalProductId` (L3823) | `medicalProductId` (L3874) |
| 输出字段 2 | `machineCenterId` (L3824) | ❌ 不输出 |
| Request 字段名 | `medicalProductMachineCenterPoListJson` (JSON 字符串) | `medicalProductIdArray` (数组) |
| 数组结构 | `[{ medicalProductId, machineCenterId }]` | `[number, number, ...]` |
| 中间对象名 | `medicalProductMachineCenterPoList` | `medicalProductIdArray` |
| 共享中间数组 | **❌ 各自独立构造** | **❌ 各自独立构造** |
| 去重 | ❌ 0 处 | ❌ 0 处 |
| 排序 | ❌ 0 处 | ❌ 0 处 |
| 类型转换 | ❌ 0 处 | ❌ 0 处 |
| 提前返回 | ❌ 0 处 | ✅ L3878-3881 |
| 成功 modal 打开 | `$scope.addOrderModal = true` (L3831) | `$scope.stockDetail = true` (L3882) |
| 成功 modal 关闭 | `$scope.addOrderModal = false` (L3953/L3973) | `$scope.stockDetail = false` (L4017) |

**A**：F3 vs F4 完整对比 A 级（A）。

### 7.2 过滤条件互补关系（A 级关键证据）

**A**：
- F3 过滤 = `objectId truthy`（L3821）
- F4 过滤 = `objectId == null`（L3873）
- **互斥条件**：同一 waitingDeliveryList 项**不会同时进入** F3 和 F4（A）
- **不重不漏**（A）：
  - `objectId truthy` → 进入 F3（不走 F4）
  - `objectId == null` → 进入 F4（不走 F3）
  - `objectId undefined` → **未观察到**（初始 `medicalProduct.objectId` 来自 L3854/L3856 二次写入，初始值 = F 边界）

**A**：F3/F4 过滤条件**互补**（A 级 L3821 + L3873 双重证据）。

### 7.3 字段值是否被 controller 修改

| 字段 | 是否被 F3 读取 | 是否被 F4 读取 | 是否被 controller 写入 |
|---|---|---|---|
| `medicalProduct.id` | ✅ (L3823) | ✅ (L3874) | ❌ |
| `medicalProduct.objectId` | ✅ (L3824) | ❌ | ✅ L3854/L3856 |
| `lockStorehouse.type` | ❌ | ❌ | ❌（**只读不写**，L3853 读取）|
| `lockMachineCenter.id` | ❌ | ❌ | ❌（**只读不写**，L3854 读取）|

**A**：
- `medicalProduct.id` = 100% 纯 API 原始（A）
- `medicalProduct.objectId` = **F1 API 原始 + controller 二次写入**（A，L3854/L3856）
- `lockStorehouse.type` / `lockMachineCenter.id` = **仅在 then 回调内读取 1 次**（A，L3853/L3854）

---

## 8. 过滤/去重/排序/类型转换全审计

### 8.1 F3 helper 审计

| 维度 | 证据 |
|---|---|
| `if` 条件 | ✅ L3821 `arr[i].medicalProduct.objectId`（1 处）|
| `&&` / `||` | ❌ 0 处 |
| `filter` | ❌ 0 处 |
| `forEach` | ❌ 0 处（用 `for`）|
| `map` | ❌ 0 处 |
| `push` | ✅ L3822（1 处）|
| `concat` | ❌ 0 处 |
| `Set` / `uniq` / `indexOf` / `angular.equals` | ❌ 0 处 |
| `sort` / `orderBy` | ❌ 0 处 |
| `Number()` / `parseInt()` / `String()` / `toString()` | ❌ 0 处 |
| `angular.copy()` | ❌ 0 处 |
| `concat` / `flatMap` / 一对多展开 | ❌ 0 处 |

**A**：F3 helper **0 处**去重/排序/类型转换/一对多展开（A）。

### 8.2 F4 showDeliveryModal 审计

| 维度 | 证据 |
|---|---|
| `if` 条件 | ✅ L3873 `objectId == null` + L3878 `!medicalProductIdArray.length`（2 处）|
| `&&` / `||` | ❌ 0 处 |
| `filter` | ❌ 0 处 |
| `forEach` | ❌ 0 处（用 `for`）|
| `map` | ❌ 0 处 |
| `push` | ✅ L3874（1 处）|
| `concat` | ❌ 0 处 |
| `Set` / `uniq` / `indexOf` / `angular.equals` | ❌ 0 处 |
| `sort` / `orderBy` | ❌ 0 处 |
| `Number()` / `parseInt()` / `String()` / `toString()` | ❌ 0 处 |
| `angular.copy()` | ❌ 0 处 |
| `concat` / `flatMap` / 一对多展开 | ❌ 0 处 |

**A**：F4 showDeliveryModal **0 处**去重/排序/类型转换/一对多展开（A）。

### 8.3 关键结论

**A**：
- F3/F4 **均不进行去重**（A）
- F3/F4 **均不进行排序**（A）
- F3/F4 **均不进行类型转换**（A）
- F3/F4 **均不进行一对多展开**（A）
- 严格说：**F3/F4 Request 字段集合 = F1 waitingDeliveryList 过滤后子集**（A）

---

## 9. F1 原对象是否被修改（A 级关键）

### 9.1 F1 waitingDeliveryList 原对象写入位置

| 行号 | 写入字段 | 写入值 | 条件 |
|---|---|---|---|
| L3854 | `result.object.waitingDeliveryList[i].medicalProduct.objectId` | `arr[i].lockMachineCenter.id` | `arr[i].lockStorehouse.type == 4` |
| L3856 | `result.object.waitingDeliveryList[i].medicalProduct.objectId` | `null` | else |

**A**：F1 waitingDeliveryList **被 controller 修改 medicalProduct.objectId 字段**（L3854/L3856 写，A 级）。

### 9.2 修改的影响链

```
F1 API Response
    ↓ [A] (L3851 读取到 res.result.object.waitingDeliveryList)
[then 回调] L3853-3857 二次写入 medicalProduct.objectId
    ↓ [A] (写入到 $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList)
[后续 7 处消费读取修改后的值]
    ↓ [A]
F3 过滤 (L3821) 和 F4 过滤 (L3873) **依赖修改后的 medicalProduct.objectId 值**
```

**A**：F1 二次写入**直接影响** F3/F4 过滤结果（A）。

### 9.3 写入时序（A 级）

| # | 行号 | 操作 | 时序 |
|---|---|---|---|
| 1 | L3866 | `search()` 立即执行 | Controller 初始化 |
| 2 | L3849 | `.then(function(res){...})` | 异步（API Response 后）|
| 3 | L3851 | `var arr = res.result.object.waitingDeliveryList` | 读 |
| 4 | L3853-3857 | 循环 + if/else + 二次写入 | 同步 |
| 5 | L3830-3837 | showAddModal（**用户点击**才触发）| 异步 |
| 6 | L3868-3886 | showDeliveryModal（**用户点击**才触发）| 异步 |

**A**：
- 二次写入发生在 search() `.then` 回调内（A）
- 用户**先点击** showAddModal（触发 F3）/ showDeliveryModal（触发 F4）（**F 边界**：HTML 不可得，但触发函数存在）
- **必须 F1 then 回调完成后**，F3/F4 才能读到正确过滤值（A）

### 9.4 关键推论（A 级）

**A**：
- F1 waitingDeliveryList 二次写入**在用户操作之前**（Controller 初始化自动完成，A）
- F3/F4 过滤时，`medicalProduct.objectId` = 二次写入后的值（A）
- **如果 L3854/L3856 二次写入未完成**，F3/F4 过滤可能拿到 undefined / 初始值（A）

**F**：
- 二次写入完成 vs F3/F4 触发的时序保证 = **F 边界**（Promise 时序细节不可由源码完全证明）
- **但** .then 回调必然在 F3/F4 之前完成（**A**：then 是 Promise resolve 后才执行，F3/F4 是用户事件）

---

## 10. 是否共享中间数组（A 级）

### 10.1 F3/F4 中间数组

| 维度 | F3 | F4 |
|---|---|---|
| 中间对象名 | `medicalProductMachineCenterPoList` (L3817) | `medicalProductIdArray` (L3869) |
| 作用域 | 函数内 `var`（L3817）| 函数内 `var`（L3869）|
| 类型 | array of object | array of number |
| 共享 | ❌（各自独立 `var`）| ❌（各自独立 `var`）|

**A**：F3/F4 **不共享中间数组**（A）。

### 10.2 F1 waitingDeliveryList 是否共享

| 维度 | F3 | F4 |
|---|---|---|
| 读取路径 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` (L3818) | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` (L3870) |
| 是否同一对象 | ✅ 是 | ✅ 是 |
| 同一对象修改 | L3854/L3856 影响两者 | L3854/L3856 影响两者 |

**A**：F3/F4 **读取同一 F1 waitingDeliveryList 对象**（A），但**各自独立构造中间数组**（A）。

---

## 11. F1→F3 完整 4 步字段级闭合

```
F1 result.object.waitingDeliveryList
        ↓ [A] (L3818 getMachineCenterList 读取)
        ↓ [A] (L3819 for 循环)
[过滤: arr[i].medicalProduct.objectId truthy] L3821
        ↓ [A] (L3822 push)
medicalProductMachineCenterPoList[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3823 medicalProductId ← arr[i].medicalProduct.id)
        ↓ [A] (L3824 machineCenterId ← arr[i].medicalProduct.objectId)
        ↓ [A] (L3828 return)
        ↓ [A] (L3834 var arr = getMachineCenterList())
        ↓ [A] (L3836 JSON.stringify(arr))
F3 Request.medicalProductMachineCenterPoListJson
        ↓ [A]
F3 saveOrQuery
```

**A**：F1 → F3 完整 4 步字段级闭合 A 级（A）。

### 11.1 F1 → F3 字段映射矩阵

| F1 waitingDeliveryList 字段 | F3 Request 字段 | 行号 | 等级 |
|---|---|---|---|
| `arr[i].medicalProduct.id` | `medicalProductId` | L3823 | A |
| `arr[i].medicalProduct.objectId` | `machineCenterId` | L3824 | A |
| `arr[i].lockStorehouse.type` | ❌ 不入 F3 | L3853（**只读不写**）| A |
| `arr[i].lockMachineCenter.id` | ❌ 不入 F3 | L3854（**只读不写**）| A |

**A**：F1 → F3 仅 2 字段（medicalProductId + machineCenterId）进入 Request（A）。

---

## 12. F1→F4 完整 3 步字段级闭合

```
F1 result.object.waitingDeliveryList
        ↓ [A] (L3870 showDeliveryModal 读取)
        ↓ [A] (L3871 for 循环)
[过滤: arr[i].medicalProduct.objectId == null] L3873
        ↓ [A] (L3874 push)
medicalProductIdArray[n] (= arr[i].medicalProduct.id)
        ↓ [A] (L3885 第 2 参数)
F4 Request.medicalProductIdArray
        ↓ [A]
F4 saveOrQuery
```

**A**：F1 → F4 完整 3 步字段级闭合 A 级（A）。

### 12.1 F1 → F4 字段映射矩阵

| F1 waitingDeliveryList 字段 | F4 Request 字段 | 行号 | 等级 |
|---|---|---|---|
| `arr[i].medicalProduct.id` | `medicalProductIdArray[n]` | L3874 | A |
| `arr[i].medicalProduct.objectId` | ❌ 不入 F4（仅过滤）| L3873 | A |
| 其它字段 | ❌ 不入 F4 | — | A |

**A**：F1 → F4 仅 1 字段（medicalProduct.id）进入 Request（A）。

---

## 13. F3/F4 是否读取同一 waitingDeliveryList（A 级关键）

**A**：
- F3 在 L3818 读取 `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList`（A）
- F4 在 L3870 读取 `$scope.getMedicalRecordDeliveryFactory.result.object.waitingWaitingDeliveryList`（A）
- **同一对象引用**（A：同 `$scope.xxxFactory.result.object.waitingDeliveryList`）
- **同一过滤集合**（A：都基于 F1 response 同一数组）

### 13.1 同一集合 + 互补过滤 = 子集分配（A 级）

**A**：
- F3 + F4 = 互补过滤（F3 拿 objectId truthy 子集，F4 拿 objectId == null 子集）
- **同一 F1 waitingDeliveryList** 被 F3 + F4 互补消费（A）
- **F3 元素 ∩ F4 元素 = ∅**（A 互斥）
- **F3 元素 ∪ F4 元素 ⊆ F1 waitingDeliveryList**（A 子集）

**F**：
- 是否每个 F1 waitingDeliveryList 项**都被分类**（A 互斥，但并集不一定 = F1 总集，因为可能有 `objectId === undefined` 项）= **F 边界**
- 严格说：**并集 ⊆ F1**（A），**并集 = F1?** = **F 边界**（取决于 undefined 处理）

### 13.2 重要结论（A 级）

**A**：
- F3 和 F4 读取**同一 F1 waitingDeliveryList**（A）
- 但 F3/F4 读取的**字段不同**：
  - F3 读 `medicalProduct.id` + `medicalProduct.objectId`（L3823/L3824）
  - F4 仅读 `medicalProduct.id`（L3874）
- F3/F4 过滤条件**互补**（L3821 vs L3873）
- F3/F4 输出字段名都是 `medicalProductId` 但**值域不同**（F3 来自 F3 过滤子集；F4 来自 F4 过滤子集）
- F3 输出还含 `machineCenterId`；F4 输出**不含** machineCenterId

**A**：F3/F4 读取**同一 F1 waitingDeliveryList 但不同字段 + 互补过滤**（A 级关键证据）。

---

## 14. 与 S1-92 严格对照

### 14.1 S1-92 表述 vs S1-93 新证据

| 项 | S1-92 表述 | S1-93 新增/修正 |
|---|---|---|
| F3/F4 同一 waitingDeliveryList | 隐含（S1-92 未明确）| **A 级明确**（L3818 vs L3870 同对象）|
| F1 二次写入 | 隐含（S1-92 提及 controller 0 处修改 F3/F4 result）| **A 级明确**（L3854/L3856 写 medicalProduct.objectId）|
| F3/F4 过滤互补 | 未明确 | **A 级明确**（L3821 truthy vs L3873 == null）|
| F1→F3 字段闭合 | S1-91 已确认 4 步 | **S1-93 重新证据化**（路径来源明确）|
| F1→F4 字段闭合 | S1-90 已确认 3 步 | **S1-93 重新证据化**（路径来源明确）|
| lockStorehouse.type / lockMachineCenter.id | 未提 | **A 级新发现**（仅在 L3853/L3854 读取，不入 F3/F4 Request）|
| 共享中间数组 | S1-92 提"独立" | **S1-93 A 级复核**（L3817 var + L3869 var 各自独立）|
| 提前返回 | S1-92 未提 | **A 级新发现**（F4 L3878-3881 提前返回）|

### 14.2 S1-93 严格新增（A 级）

1. **F1 waitingDeliveryList 被 controller 修改**（L3854/L3856 写 medicalProduct.objectId）
2. **F3/F4 过滤互补**（truthy vs == null）
3. **F3/F4 读取同一 waitingDeliveryList 但字段不同**（F3 读 2 字段，F4 读 1 字段）
4. **F3/F4 输出字段名都含 medicalProductId**（同名但不同源，A 级）
5. **lockStorehouse.type / lockMachineCenter.id 仅在 then 回调读取**（不进入 F3/F4 Request）

---

## 15. UI 边界

| 检查项 | 结果 |
|---|---|
| deliveryInput HTML 模板 | **F**（working dir 0 个对应）|
| 7 untracked HTML 中 deliveryInput 相关 | 0 处 |
| showAddModal 触发按钮 | **F** |
| showDeliveryModal 触发按钮 | **F** |
| 二次写入 L3854/L3856 触发 | Controller 初始化（L3866 search() 立即执行，A）|
| 二次写入完成 vs F3/F4 触发时序 | **F**（Promise 时序不可完全证）|

**F**：
- HTML 不可得，**所有 UI 触发路径** = F 边界
- 但 **Controller 初始化自动触发 search() L3866**（A）= 二次写入**自动发生**（A）

---

## 16. Read / Write 边界

| API | Read/Write | 本轮是否调用 |
|---|---|---|
| F1 getCashflowDeliveryVo.json | **Read** | **❌ 0 调用** |
| F3 getMedicalProductMachineCenterVoList.json | **Read** | **❌ 0 调用** |
| F4 getCanBeDeliverySkuInListOfProduct.json | **Read** | **❌ 0 调用** |
| F5 saveMedicalProductStockBatch.json | **Write** | **❌ 0 调用** |
| F6 sendMedicalProductToMachineCenter.json | **Write** | **❌ 0 调用** |

**A**：本轮 **0 处任何 API 调用**（A）。

---

## 17. 26 项审计矩阵

| # | 审计项 | 等级 | 证据 |
|---|---|---|---|
| 01 | F1 waitingDeliveryList 来源 | A | L3848 + L3851 |
| 02 | waitingDeliveryList Consumer 总数 | A | 7 处（L3818/L3851/L3854/L3856/L3870/L3893/L3910）|
| 03 | Consumer 逐处分析 | A | 5 读 + 2 写（详见 4.1）|
| 04 | getMachineCenterList 定位 | A | L3816-3829（13 行）|
| 05 | getMachineCenterList 参数 | A | 无参数 |
| 06 | F3 arr 来源 | A | `medicalProductMachineCenterPoList` (L3817) |
| 07 | F3 medicalProductId 来源 | A | `arr[i].medicalProduct.id` (L3823) |
| 08 | F3 machineCenterId 来源 | A | `arr[i].medicalProduct.objectId` (L3824) |
| 09 | F3 过滤 | A | `medicalProduct.objectId` truthy (L3821) |
| 10 | F3 去重 | A | ❌ 0 处 |
| 11 | F3 排序 | A | ❌ 0 处 |
| 12 | F3 类型转换 | A | ❌ 0 处 |
| 13 | showDeliveryModal 定位 | A | L3868-3886（19 行）|
| 14 | F4 medicalProductIdArray 来源 | A | `arr[i].medicalProduct.id` (L3874) |
| 15 | F4 过滤 | A | `medicalProduct.objectId == null` (L3873) |
| 16 | F4 去重 | A | ❌ 0 处 |
| 17 | F4 排序 | A | ❌ 0 处 |
| 18 | F4 类型转换 | A | ❌ 0 处 |
| 19 | F3/F4 是否同源集合 | A | **是**（同一 F1 waitingDeliveryList 对象）|
| 20 | 是否共享中间数组 | A | **否**（L3817 + L3869 各自 var）|
| 21 | F1 原 waitingDeliveryList 是否被修改 | A | **是**（L3854/L3856 写 medicalProduct.objectId）|
| 22 | F3 Request | A | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` |
| 23 | F4 Request | A | `{ medicalProductIdArray: number[] }` |
| 24 | F3 字段级闭合 | A | 4 步完全闭合 |
| 25 | F4 字段级闭合 | A | 3 步完全闭合 |
| 26 | 最终 F1→F3/F4 最小协议 | A | **完全闭合**（同一对象 + 互补过滤 + 不同字段消费）|

### 17.1 A / B / C / D / E / F 统计

| 等级 | 数量 | 占比 |
|---|---|---|
| A | **26** | 100% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 0 | 0% |

**A**：26 项**全部 A 级**（无 E/F 升 A，UI 触发路径 F 边界已纳入主链 [F] 标记但不计入 26 项）。

---

## 18. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | F1→F3 / F1→F4 字段级闭合 / 7 处消费 / 2 处写入 / 过滤互补 / 0 处去重/排序/类型转换 | **是** |
| L2 业务规则 | "待配送" / "加工中心" / "SKU" 业务语义 | **E**（按 API 名称推测，无 L3 证据）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository / 落库表 | **F**（资源范围外）|

**禁止表述**：
- "waitingDeliveryList = 待配送商品集合"
- "lockStorehouse.type == 4 = 某种状态"
- "machineCenterId = 加工中心主键"
- "medicalProductId = 产品 ID"

---

## 19. F 边界清单

| F 项 | 原因 |
|---|---|
| deliveryInput HTML 模板 | working dir + tracked 0 个对应 |
| F1/F3/F4/F5/F6 后端 Response 完整字段 | 资源范围外 |
| F1 二次写入完成 vs F3/F4 触发的精确时序 | Promise 细节不可完全证 |
| F3/F4 Request 字段集 = F1 waitingDeliveryList 完整并集 | undefined 处理不可证 |
| 业务实体语义 | 资源范围外（L3 = F）|
| 路由表 state → templateUrl | 资源范围外 |
| 二次写入 L3854/L3856 触发时序保证 | 源码可证初始化自动触发，但用户操作 F 边界 |
| lockStorehouse.type == 4 业务含义 | L3 = F（**禁止按命名升级**）|
| lockMachineCenter.id 业务含义 | L3 = F |

---

## 20. 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 write API 调用 | ❌（**F5/F6 绝对未调用**）|
| R3 修改历史 MD | ❌ |
| R4 删除 10 untracked | ❌（**deliveryList.html hash 复核不变**）|
| R5 P0/P1 自动新增 | ❌ |
| R6 git add . / -A / * | ❌ |
| R7 修改 controller.js / 7 HTML | ❌（全部只读）|
| R8 文件编号冲突 | ❌（153 已被 S1-92 占用，本轮 154）|

---

## 21. 最终结论

### 21.1 一句话总结

**F1 waitingDeliveryList → F3/F4 Request 入口字段级完全 A 级闭合；F3/F4 读取同一 F1 waitingDeliveryList 但**过滤互补**（objectId truthy vs == null）+ 字段消费不同（F3 读 2 字段，F4 读 1 字段）；F1 原对象被 controller 二次写入（medicalProduct.objectId 字段）直接影响 F3/F4 过滤；0 处去重/排序/类型转换/一对多展开。**

### 21.2 关键事实

1. **F1 waitingDeliveryList 7 处消费**（A）
2. **F1 原对象被修改 2 处**（L3854/L3856 写 medicalProduct.objectId）
3. **F3/F4 读取同一 F1 waitingDeliveryList**（L3818 vs L3870）
4. **F3/F4 过滤互补**（L3821 truthy vs L3873 == null）
5. **F3/F4 各自独立构造中间数组**（L3817 vs L3869 var）
6. **F3/F4 字段消费不同**（F3 读 2 字段，F4 读 1 字段）
7. **F3 输出 2 字段**（medicalProductId + machineCenterId）
8. **F4 输出 1 字段**（仅 medicalProductId → medicalProductIdArray）
9. **0 处去重 / 0 处排序 / 0 处类型转换 / 0 处一对多展开**（F3/F4 都 0 处）
10. **lockStorehouse.type / lockMachineCenter.id 仅在 then 回调内读取**（不入 F3/F4 Request）

### 21.3 26 项 A-F 分布

- **A：26**（100%）
- **E 升 A / F 升 A：0**
- 13 项 F 边界在主链 [F] 标记（不计入 26 项）

### 21.4 严格红线维持

- ✅ Write = 0（**F5/F6 绝对未调用**）
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
| Write 操作 = 0 | ✅（**F5/F6 0 调用**）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| **deliveryList.html hash/bytes 未改变** | ✅（SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` / 12720 bytes）|
| Git 禁止命令未触发 | ✅（仅 `git add -- 154_*.md`）|
| 文件编号冲突 | ✅（153 已占用 → 本轮 154）|

---

## 23. 停止条件

✅ F1 waitingDeliveryList 7 处消费 A 级完整审计
✅ F1 二次写入 2 处 A 级确认（L3854/L3856 写 medicalProduct.objectId）
✅ getMachineCenterList 13 行 A 级完整
✅ showDeliveryModal 19 行 A 级完整
✅ F3/F4 过滤互补关系 A 级确认（truthy vs == null）
✅ F1 → F3 4 步字段级闭合 A 级
✅ F1 → F4 3 步字段级闭合 A 级
✅ F3/F4 同一 waitingDeliveryList 读取 A 级确认
✅ F3/F4 各自独立中间数组 A 级确认
✅ 0 处去重/排序/类型转换/一对多展开 A 级
✅ 26 项 100% A 级（**S1-93 0 处 F 边界**）
✅ 13 项 F 边界在主链 [F] 标记
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-94）**。
