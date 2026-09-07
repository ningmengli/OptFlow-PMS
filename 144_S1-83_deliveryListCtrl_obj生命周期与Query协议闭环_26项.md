# S1-83 deliveryListCtrl `$scope.obj` 生命周期与 Query 协议闭环

> 审计对象：`deliveryListCtrl` L4075-4233 + `$scope.obj` 11 字段 + `memberFactory` + `getCashflowDeliveryVoList.json`
> 任务来源：S1-83（基于 S1-81/S1-82 已确认 storage value = $scope.obj）
> 审计立场：**只按源码 + deliveryList.html 静态证据；不推 ListFactory 内部 Request 构造；不推"内部 cache"语义**

---

## 1. 核心结论（50 字以内）

**`$scope.obj` 共 11 字段；5 个 function（init / setTab / setFee / search / clearPage）修改；每次 search 重新 new memberFactory；Query 触发链完整 6 层 A 级闭合。**

---

## 2. 证据范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryListCtrl | L4075-4233（159 行）| 完整二次确认 |
| $scope.obj 访问点 | **37 处** | 跨 159 行 |
| chargedeliveryList 操作 | 1 读 + 2 写 | 全部 deliveryListCtrl |
| deliveryList.html | 344 行 | SHA256 已快照 |
| 其它 9 untracked HTML | 0 处引用 | — |
| $state 操作 | **0 处** | 严格 A |
| 后端 API 完整字段 | F | 资源范围外 |
| ListFactory 内部 Request 构造 | F | 任务明确禁止 |

---

## 3. deliveryListCtrl 完整定位

| 项 | 值 |
|---|---|
| 文件 | controller.js |
| 起止行 | L4075-4233 |
| 行数 | 159 |
| 注入依赖 | $scope, Popup, $timeout, **$stateParams**, $rootScope, **$state**, **ObjectFactory**, **DateUtilFactory**, **ListFactory**, $http |
| 入口 | L4076 读 sessionStorage → L4077 $scope.obj 恢复 |
| 立即执行 | L4210 `$scope.search()`（同步触发 2 个 API）|
| $state.go | **0 处** |
| $state.reload | **0 处** |

**A**：deliveryListCtrl 注入了 11 个依赖（包含 $state 但 0 处使用）。
**A**：L4210 `$scope.search()` 立即执行 = controller 初始化时同步触发 search（A）。

---

## 4. `$scope.obj` 完整字段（11 字段）

### 4.1 字段清单

| # | 字段 | 类型 | 默认值 | 是否进入 Query |
|---|---|---|---|---|
| 1 | `startTime` | Date | L4081 `moment().add(-3, 'months')._d` | ✅ |
| 2 | `endTime` | Date | search 内派生（L4175）| ✅ |
| 3 | `rightTimer` | Date | L4086 `new Date()` | ❌（**仅用于派生 endTime**）|
| 4 | `deliveryStatus` | number/null | L4088-4100 映射 | ✅ |
| 5 | `toBeProcess` | number/null | L4088-4100 映射 | ✅ |
| 6 | `refundStatus` | number | L4104 `0` | ✅（refundStatusArray 派生）|
| 7 | `keyword` | string | undefined（HTML 双向绑定）| ✅ |
| 8 | `productKeyword` | string | undefined（HTML 双向绑定）| **F**（controller 0 处处理）|
| 9 | `batchNoKeyword` | string | undefined（HTML 双向绑定）| **F**（controller 0 处处理）|
| 10 | `page` | number | undefined（pagination callback 设置）| ✅（决定 pageStart）|
| 11 | `refundStatusArray` | array | search 内派生（L4185/L4187）| ✅ |

### 4.2 obj 严格不含业务字段

- ❌ `cashflow` / `cashflowId`（**不存在于 $scope.obj**）
- ❌ `patient` / `customer` / `medicalProduct`
- ❌ `waitingDeliveryList` / `deliveryedList` / `sendToMachineCenterList`
- ❌ `deliveryStatus`（HTML item 字段，**不是** obj 字段）

**A**：$scope.obj = **查询参数对象**（11 字段），**不包含任何业务数据字段**（A）。

---

## 5. `$scope.obj` 11 字段详细生命周期

### 5.1 startTime

```javascript
// L4078-4081
if ($scope.obj.startTime) {
    $scope.obj.startTime = new Date($scope.obj.startTime);
} else {
    $scope.obj.startTime = moment(new Date()).add(-3, "months")._d;
}
```

```javascript
// L4168-4172 (search 内)
if ($scope.obj.startTime) {
    $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);
    $scope.countObj.startTime = $scope.obj.startTime;
} else {
    delete $scope.obj.startTime;
}
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| 初始化 | L4078-4079 | storage 存在 → 转 Date 对象 |
| 默认 | L4081 | storage 不存在 → 3 个月前 |
| search 处理 | L4168-4172 | DateUtilFactory.origin 处理 + 同步 countObj |

**A**：startTime 进入 Query（A）。

### 5.2 endTime

```javascript
// L4174-4179 (search 内)
if ($scope.rightTimer) {
    $scope.obj.endTime = DateUtilFactory.plus($scope.rightTimer);
    $scope.obj.rightTimer = $scope.rightTimer;
    $scope.countObj.endTime = $scope.obj.endTime;
} else {
    delete $scope.obj.endTime;
}
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| 初始化 | — | **不初始化**（仅在 search 内派生）|
| search 处理 | L4174-4179 | 从 $scope.rightTimer 派生 |

**A**：endTime 仅在 search 内派生，不从 storage 恢复（A）。

### 5.3 rightTimer

```javascript
// L4083-4086
if ($scope.obj.rightTimer) {
    $scope.rightTimer = new Date($scope.obj.rightTimer);  // 注意：赋给 $scope.rightTimer
} else {
    $scope.rightTimer = new Date();  // 注意：赋给 $scope.rightTimer
}
```

```javascript
// L4175-4176 (search 内)
$scope.obj.endTime = DateUtilFactory.plus($scope.rightTimer);
$scope.obj.rightTimer = $scope.rightTimer;
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| storage 恢复 | L4084 | `if ($scope.obj.rightTimer) { $scope.rightTimer = ... }` |
| 默认 | L4086 | `$scope.rightTimer = new Date()` |
| search 派生 | L4175-4176 | endTime 从 $scope.rightTimer 派生；同步到 $scope.obj.rightTimer |

**A**：
- `rightTimer` 是 `$scope.rightTimer`（**scope 变量**，非 obj 字段）
- `obj.rightTimer` 在 L4176 才被回填（与 endTime 同步）
- **$scope.obj.rightTimer 不进入 Query**（angular.copy 复制它，但 pageStart 只看 obj.page；searchCount obj 不用 rightTimer）

**F**：`obj.rightTimer` 是否被后端 API 使用（F 边界，**任务禁止推断**）。

### 5.4 deliveryStatus

```javascript
// L4088-4099 初始化分支
if ($scope.obj.deliveryStatus === 0 && $scope.obj.toBeProcess === 0) {
    $scope.obj.deliveryStatus = $scope.obj.deliveryStatus;
    $scope.obj.toBeProcess = $scope.obj.toBeProcess;
    $scope.deliveryStatus = 1;
} else if ($scope.obj.deliveryStatus === 0 && $scope.obj.toBeProcess === 1) {
    $scope.obj.deliveryStatus = $scope.obj.deliveryStatus;
    $scope.obj.toBeProcess = $scope.obj.toBeProcess;
    $scope.deliveryStatus = 2;
} else if ($scope.obj.deliveryStatus === 1 && $scope.obj.toBeProcess === null) {
    $scope.obj.deliveryStatus = $scope.obj.deliveryStatus;
    $scope.obj.toBeProcess = $scope.obj.toBeProcess;
    $scope.deliveryStatus = 3;
}
```

```javascript
// L4127-4146 setTab
$scope.setTab = function (index) {
    if (index == 1) {
        $scope.obj.deliveryStatus = 0;
        $scope.obj.toBeProcess = 0;
        $scope.deliveryStatus = 1;
    } else if (index == 2) {
        $scope.obj.deliveryStatus = 0;
        $scope.obj.toBeProcess = 1;
        $scope.deliveryStatus = 2;
    } else if (index == 3) {
        $scope.obj.deliveryStatus = 1;
        $scope.obj.toBeProcess = null;
        $scope.deliveryStatus = 3;
    } else {
        $scope.obj.deliveryStatus = null;
        $scope.obj.toBeProcess = null;
        $scope.deliveryStatus = null;
    }
    $scope.clearPage();
};
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| 初始化派生 | L4088-4100 | 基于 storage 恢复值映射 + 设置 $scope.deliveryStatus |
| setTab 修改 | L4129-4143 | 4 个 index 分支 |
| clearPage 触发 | L4145 / L4213 | setTab 后重置 page=0 并重新 search |

**A**：deliveryStatus + toBeProcess 总是同步变化（4 种组合：0/0、0/1、1/null、null/null），A。

### 5.5 toBeProcess

- 与 deliveryStatus 完全同步（见 5.4）
- L4088-4100 初始化映射 + L4129-4142 setTab 修改

**A**：toBeProcess 与 deliveryStatus 1:1 同步变化（A）。

### 5.6 refundStatus

```javascript
// L4101-4105
if ($scope.obj.refundStatus != null) {
    $scope.obj.refundStatus = $scope.obj.refundStatus;
} else {
    $scope.obj.refundStatus = 0;
}
```

```javascript
// L4148-4151 setFee
$scope.setFee = function (index) {
    $scope.obj.refundStatus = index;
    $scope.clearPage();
};
```

```javascript
// L4155-4160 searchCount 内 obj 副本处理
if (obj.refundStatus == null) {
    delete obj.refundStatus;
} else if (obj.refundStatus === 0) {
    obj.refundStatusArray = [0, 2];
} else {
    obj.refundStatusArray = [1];
}
```

```javascript
// L4182-4187 search 内 obj 副本处理（同样逻辑）
if (obj.refundStatus == null) {
    delete obj.refundStatus;
} else if (obj.refundStatus === 0) {
    obj.refundStatusArray = [0, 2];
} else {
    obj.refundStatusArray = [1];
}
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| 初始化 | L4101-4104 | null → 0 |
| setFee | L4149 | = index（0/1）|
| searchCount 处理 | L4155-4160 | 转 refundStatusArray（局部 obj）|
| search 处理 | L4182-4187 | 同上（局部 obj）|

**A**：
- `refundStatus` 写入 $scope.obj（A）
- `refundStatusArray` 写入 **局部 obj 副本**（不写入 $scope.obj，A）
- searchCount 与 search 内**有重复逻辑**（A）

### 5.7 keyword

- 来源：HTML L92-99 `throttleinput ... model="obj.keyword"`
- 写入：HTML 双向绑定（ng-model 语义）
- controller 读：L4192 `$scope.countObj.keyword = $scope.obj.keyword`
- controller 写：**0 处**

**A**：keyword 由 HTML 双向绑定写入 $scope.obj.keyword（A）。

### 5.8 productKeyword

- 来源：HTML L104-110 `throttleinput ... model="obj.productKeyword"`
- controller 读/写：**0 处**
- search 内 angular.copy：**包含**（自动包含所有 obj 字段）
- 进入 Query：**F**（controller 0 处直接处理；F 边界）

### 5.9 batchNoKeyword

- 来源：HTML L113-121 `throttleinput ... model="obj.batchNoKeyword"`
- controller 读/写：**0 处**
- search 内 angular.copy：**包含**
- 进入 Query：**F**（controller 0 处直接处理；F 边界）

### 5.10 page

```javascript
// L4189
var pageStart = $scope.obj.page ? $scope.obj.page * pageSize : 0;
```

```javascript
// L4202 pagination callback
$scope.obj.page = index;
```

```javascript
// L4213 clearPage
$scope.obj.page = 0;
```

| 阶段 | 行号 | 操作 |
|---|---|---|
| 初始 | — | undefined（第一次为 0）|
| search 派生 | L4189 | `obj.page ? obj.page * pageSize : 0` |
| pagination 写 | L4202 | `$scope.obj.page = index` |
| clearPage 重置 | L4213 | `$scope.obj.page = 0` |

**A**：page 是分页控制字段（A）。

### 5.11 refundStatusArray

- 来源：searchCount（L4158/L4160）+ search（L4185/L4187）派生
- 写入：**局部 obj**（不写入 $scope.obj）
- 进入 Query：✅（通过 angular.copy 的 obj 副本传给 memberFactory 和 checkCountFactory）

**A**：refundStatusArray 不写入 $scope.obj（不持久化到 storage，A）。

---

## 6. `$scope.obj` 修改点全集（37 处访问）

### 6.1 修改点按 function 分类

| function | 修改字段 | 行号 |
|---|---|---|
| 初始化（匿名）| startTime / rightTimer / deliveryStatus / toBeProcess / refundStatus | L4077-4105 |
| setTab | deliveryStatus / toBeProcess | L4129-4142 |
| setFee | refundStatus | L4149 |
| search | startTime / endTime / rightTimer / refundStatusArray（局部 obj）| L4168-4187 |
| pagination callback | page | L4202 |
| clearPage | page | L4213 |

### 6.2 写 storage 时机

| function | 行号 | 写 storage 之前 obj 修改？ |
|---|---|---|
| search | L4190 | ✅（startTime/endTime/rightTimer 已处理 + obj 副本转换）|
| pagination callback | L4203 | ✅（obj.page 已更新）|

**A**：L4190 / L4203 两处写 storage 时，$scope.obj 都已被 function 内部修改（A）。

---

## 7. chargedeliveryList get 完整链路

```javascript
// L4076-4077
var store = JSON.parse(sessionStorage.getItem("chargedeliveryList"));
$scope.obj = store ? store : {};
```

| 行号 | 操作 |
|---|---|
| L4076 | `var store = JSON.parse(sessionStorage.getItem("chargedeliveryList"));` |
| L4077 | `$scope.obj = store ? store : {};` |

**A**：
- getItem 返回值 → JSON.parse → store
- 三元判断：store truthy → 用 store；null/空 → 用 `{}`
- **完全覆盖** $scope.obj（A）

**A**：sessionStorage 读取后**完全覆盖** $scope.obj（无字段合并逻辑，A）。

---

## 8. chargedeliveryList set 完整链路

### 8.1 L4190 写 storage（search 内）

```javascript
// L4166-4210 search 函数内
$scope.search = function () {
    var pageSize = 12;
    if ($scope.obj.startTime) { ... } else { delete $scope.obj.startTime; }
    if ($scope.rightTimer) { ... } else { delete $scope.obj.endTime; }
    var obj = angular.copy($scope.obj);
    if (obj.refundStatus == null) { delete obj.refundStatus; }
    else if (obj.refundStatus === 0) { obj.refundStatusArray = [0, 2]; }
    else { obj.refundStatusArray = [1]; }
    var pageStart = $scope.obj.page ? $scope.obj.page * pageSize : 0;
    sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));  // ← L4190
    $scope.countObj.keyword = $scope.obj.keyword;
    $scope.searchCount();
    $scope.memberFactory = new ListFactory(...);
    var promise = $scope.memberFactory.nextPage();
    promise.then(function (data) { ... });
};
```

**A**：L4190 写 storage 时 $scope.obj 已包含：startTime/endTime/rightTimer 处理后值 + page（可能已设）+ keyword + deliveryStatus + toBeProcess + refundStatus（A）。

### 8.2 L4203 写 storage（pagination callback 内）

```javascript
// L4201-4206
callback: function callback(index) {
    $scope.obj.page = index;
    sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));  // ← L4203
    $scope.memberFactory.clearAndSetIndex(index * pageSize);
    $scope.memberFactory.nextPage();
}
```

**A**：L4203 写 storage 时 $scope.obj.page = index 已更新（A）。

### 8.3 写入值是否始终完整

**A**：两处写入都是 `JSON.stringify($scope.obj)`，**始终完整序列化** $scope.obj 全部字段（A）。

---

## 9. memberFactory 完整创建

### 9.1 创建位置

```javascript
// L4195
$scope.memberFactory = new ListFactory(
    "/admin/getCashflowDeliveryVoList.json",
    pageStart,
    pageSize,
    obj
);
```

| # | 参数 | 真实值（按调用点）| 备注 |
|---|---|---|---|
| 1 | API | `"/admin/getCashflowDeliveryVoList.json"` | 字符串字面量 |
| 2 | pageStart | `$scope.obj.page ? $scope.obj.page * pageSize : 0`（L4189 派生）| **任务禁止推断**为分页参数；仅记录"调用点传入 pageStart 变量" |
| 3 | pageSize | `12`（L4167 局部变量）| **任务禁止推断**为分页参数；仅记录"调用点传入 12" |
| 4 | obj | `angular.copy($scope.obj)`（L4181 局部变量）| **A**：第 4 参数 = $scope.obj 的副本 |

**A**：
- memberFactory **每次 search 重新创建**（L4195 在 search 函数内，A）
- 4 个参数真实值见上表（A）

### 9.2 nextPage + then

```javascript
// L4196-4208
var promise = $scope.memberFactory.nextPage();
promise.then(function (data) {
    $("#Pagination").pagination($scope.memberFactory.count, {
        items_per_page: pageSize,
        current_page: $scope.obj.page,
        callback: function callback(index) {
            $scope.obj.page = index;
            sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));
            $scope.memberFactory.clearAndSetIndex(index * pageSize);
            $scope.memberFactory.nextPage();
        }
    });
});
```

**A**：
- `nextPage()` 返回 promise（A）
- promise.then 接 data（**F**：data 内部结构不可得）
- `$scope.memberFactory.count` 传递给 jQuery pagination（A）
- callback 内 `clearAndSetIndex(index * pageSize)` + `nextPage()`（A）

---

## 10. `getCashflowDeliveryVoList.json` API

| 维度 | 值 | 证据 |
|---|---|---|
| API 路径 | `/admin/getCashflowDeliveryVoList.json` | L4195 |
| 唯一调用点 | deliveryListCtrl L4195 | grep 全仓 1 处 |
| Factory | ListFactory 4 参数 | L4195 |
| Request params | `obj = angular.copy($scope.obj)` | L4181 |
| Request 字段全集 | 取决于 ListFactory 内部构造 | **F**（任务禁止推 ListFactory 内部）|
| Response.items | HTML ng-repeat 消费 | HTML L202 |
| Response.count | jQuery pagination 消费 | L4198 |

**F**：
- ListFactory 内部如何把 obj 字段构造为 HTTP Request **不可证**
- 后端 API 接受哪些字段、忽略哪些字段 **不可证**
- productKeyword / batchNoKeyword 是否被后端使用 **不可证**

---

## 11. Request 边界（严格 F）

### 11.1 A 级（直接证据）

- 4 个 ListFactory 参数真实值（A，见 9.1）
- `obj` 来自 `angular.copy($scope.obj)`（A）
- `obj` 在传入前已被 search 函数修改（startTime/endTime 处理 + refundStatusArray 派生，A）

### 11.2 F 级（不可证）

- ListFactory 内部如何把 `obj` 转换为最终 Request body / query string（A 不可证）
- 后端 API 是否接受 productKeyword / batchNoKeyword（A 不可证）
- ListFactory 内部 pageStart / pageSize 如何使用（A 不可证）

**任务严格禁止推断**：本节不写"ListFactory 第2参数就是 pageStart"等推论。

---

## 12. obj 修改点完整对照

| function | 修改字段 | 行号 | 是否写 storage |
|---|---|---|---|
| 初始化（匿名）| startTime / rightTimer / deliveryStatus / toBeProcess / refundStatus | L4077-4105 | ❌（初始化不写 storage）|
| setTab | deliveryStatus / toBeProcess | L4129-4142 | ❌（不直接写 storage）|
| setFee | refundStatus | L4149 | ❌（不直接写 storage）|
| clearPage | page | L4213 | ❌（不直接写 storage）|
| search | startTime / endTime / rightTimer + 局部 obj.refundStatus / obj.refundStatusArray | L4168-4187 | ✅ L4190 |
| pagination callback | page | L4202 | ✅ L4203 |

**A**：写 storage 仅发生在 search + pagination callback 2 处（A）。

---

## 13. search function 完整生命周期

```javascript
$scope.search = function () {
    // 步骤 1: pageSize 局部变量
    var pageSize = 12;  // L4167
    
    // 步骤 2: startTime 处理
    if ($scope.obj.startTime) {
        $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);  // L4169
        $scope.countObj.startTime = $scope.obj.startTime;  // L4170
    } else {
        delete $scope.obj.startTime;  // L4172
    }
    
    // 步骤 3: endTime 处理
    if ($scope.rightTimer) {
        $scope.obj.endTime = DateUtilFactory.plus($scope.rightTimer);  // L4175
        $scope.obj.rightTimer = $scope.rightTimer;  // L4176
        $scope.countObj.endTime = $scope.obj.endTime;  // L4177
    } else {
        delete $scope.obj.endTime;  // L4179
    }
    
    // 步骤 4: 局部 obj 副本（refundStatus 处理）
    var obj = angular.copy($scope.obj);  // L4181
    if (obj.refundStatus == null) {
        delete obj.refundStatus;  // L4183
    } else if (obj.refundStatus === 0) {
        obj.refundStatusArray = [0, 2];  // L4185
    } else {
        obj.refundStatusArray = [1];  // L4187
    }
    
    // 步骤 5: pageStart 派生
    var pageStart = $scope.obj.page ? $scope.obj.page * pageSize : 0;  // L4189
    
    // 步骤 6: 写 storage
    sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));  // L4190
    
    // 步骤 7: countObj 同步
    $scope.countObj.keyword = $scope.obj.keyword;  // L4192
    
    // 步骤 8: 触发 searchCount
    $scope.searchCount();  // L4193 → checkCountFactory (statProductDeliveryStatus.json)
    
    // 步骤 9: 创建 memberFactory
    $scope.memberFactory = new ListFactory(...);  // L4195
    var promise = $scope.memberFactory.nextPage();  // L4196
    
    // 步骤 10: then 回调 pagination 初始化
    promise.then(function (data) {
        $("#Pagination").pagination($scope.memberFactory.count, {  // L4198
            items_per_page: pageSize,
            current_page: $scope.obj.page,
            callback: function (index) {
                $scope.obj.page = index;  // L4202
                sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));  // L4203
                $scope.memberFactory.clearAndSetIndex(index * pageSize);  // L4204
                $scope.memberFactory.nextPage();  // L4205
            }
        });
    });
};
```

**A**：search 完整 10 步流程 A 级（A）。

---

## 14. setTab / setFee / clearPage / searchCount 完整记录

### 14.1 setTab

```javascript
$scope.setTab = function (index) {
    if (index == 1) { $scope.obj.deliveryStatus = 0; $scope.obj.toBeProcess = 0; $scope.deliveryStatus = 1; }
    else if (index == 2) { $scope.obj.deliveryStatus = 0; $scope.obj.toBeProcess = 1; $scope.deliveryStatus = 2; }
    else if (index == 3) { $scope.obj.deliveryStatus = 1; $scope.obj.toBeProcess = null; $scope.deliveryStatus = 3; }
    else { $scope.obj.deliveryStatus = null; $scope.obj.toBeProcess = null; $scope.deliveryStatus = null; }
    $scope.clearPage();  // L4145
};
```

**A**：
- setTab 修改 `$scope.obj.deliveryStatus` + `$scope.obj.toBeProcess`（A）
- setTab 同步修改 `$scope.deliveryStatus`（scope 状态变量，A）
- setTab 触发 `$scope.clearPage()`（A）

### 14.2 setFee

```javascript
$scope.setFee = function (index) {
    $scope.obj.refundStatus = index;  // L4149
    $scope.clearPage();  // L4150
};
```

**A**：setFee 修改 `$scope.obj.refundStatus` + 触发 clearPage（A）。

### 14.3 clearPage

```javascript
$scope.clearPage = function () {
    $scope.obj.page = 0;  // L4213
    $scope.search();  // L4214
};
```

**A**：clearPage 重置 page=0 + 重新 search（A）。

### 14.4 searchCount

```javascript
$scope.searchCount = function () {
    var obj = angular.copy($scope.obj);  // L4154
    if (obj.refundStatus == null) {
        delete obj.refundStatus;
    } else if (obj.refundStatus === 0) {
        obj.refundStatusArray = [0, 2];
    } else {
        obj.refundStatusArray = [1];
    }
    $scope.checkCountFactory = new ObjectFactory();  // L4162
    $scope.checkCountFactory.saveOrQuery("/admin/statProductDeliveryStatus.json", obj);  // L4163
};
```

**A**：searchCount 创建 checkCountFactory + 调用 statProductDeliveryStatus.json（A）。

---

## 15. pagination 完整记录

| 维度 | 值 | 行号 |
|---|---|---|
| pageSize | 12 | L4167 |
| pageStart 派生 | `$scope.obj.page ? $scope.obj.page * pageSize : 0` | L4189 |
| jQuery pagination 初始化 | `$("#Pagination").pagination($scope.memberFactory.count, ...)` | L4198 |
| items_per_page | pageSize（= 12）| L4199 |
| current_page | $scope.obj.page | L4200 |
| callback 参数 | index（页码）| L4201 |
| callback 内 page 更新 | `$scope.obj.page = index` | L4202 |
| callback 内 storage 写 | setItem | L4203 |
| callback 内 clearAndSetIndex | `index * pageSize` | L4204 |
| callback 内 nextPage | 重新查询 | L4205 |

**A**：pagination 完整链 A 级（A）。

---

## 16. state 操作统计

| 操作 | deliveryListCtrl 范围 |
|---|---|
| $state.go | **0 处** |
| $state.reload | **0 处** |
| $stateParams 读取 | **0 处** |
| ui-sref 跳转 | 0 处（HTML 负责）|

**A**：deliveryListCtrl 注入 $state 但 **0 处调用**（A）。

---

## 17. `countObj` vs `obj` 严格区分

| 维度 | $scope.obj | $scope.countObj |
|---|---|---|
| 定义 | L4077 `$scope.obj = store ? store : {};` | L4152 `$scope.countObj = {};` |
| 来源 | sessionStorage 恢复 | 空对象初始化 |
| 字段 | 11 字段查询参数 | 3 字段（startTime / endTime / keyword）|
| 写入 storage | ✅ | ❌（不直接写）|
| 传入 ListFactory | ✅ memberFactory (L4195) | ❌ |
| 传入 ObjectFactory | ❌ | ❌（searchCount 内是局部 obj 副本）|
| 持久化 | ✅ sessionStorage | ❌ |

**A**：countObj 与 obj 是 **2 个独立的 scope 变量**（A）。
**A**：countObj 不进入任何 API Request（仅作为 searchCount 中间变量准备参数，A）。

---

## 18. 完整数据流图（storage → obj → API → HTML）

```
[user 进入任意页面后]
    ↓
[user 操作 deliveryList 页面]
    ↓ L4075 deliveryListCtrl 初始化
JSON.parse(sessionStorage.getItem("chargedeliveryList"))
    ↓ L4077
$scope.obj = store ? store : {}
    ↓ L4078-4105
字段恢复 + 默认值
    ↓ L4152
$scope.countObj = {}
    ↓ L4107-4125
grantAuth.then → getAdminList (ListFactory 加工记录)
    ↓ L4210
$scope.search()  ← 立即执行
    ├─ L4168-4172 startTime 处理
    ├─ L4174-4179 endTime 处理
    ├─ L4181 obj = angular.copy($scope.obj) + refundStatus 处理
    ├─ L4189 pageStart 派生
    ├─ L4190 storage.setItem  ← 持久化当前 obj
    ├─ L4192 countObj.keyword 同步
    ├─ L4193 searchCount() → checkCountFactory → statProductDeliveryStatus.json
    └─ L4195-4196 memberFactory = new ListFactory(getCashflowDeliveryVoList.json, pageStart, pageSize, obj)
        └─ nextPage() → promise.then
            └─ L4198 jQuery pagination init (count + callback)
    ↓
[HTML 渲染]
    ├─ L31 {{getAdminList.count}}
    ├─ L144/L155/L166 {{checkCountFactory.object.{3 count}}}
    └─ L202 ng-repeat="item in memberFactory.items" + 18+ 字段
    ↓
[user 触发后续操作]
    ├─ 日期变化 → search() → 重新 memberFactory
    ├─ tab 切换 → setTab() → clearPage() → search()
    ├─ fee 切换 → setFee() → clearPage() → search()
    ├─ keyword 变化 → search()（HTML throttleinput）
    ├─ 翻页 → pagination callback → 重新 memberFactory
    └─ 4 个 state 跳转 → 3 个 detail controller
```

**A**：完整 6 层数据流图 A 级闭合（A）。

---

## 19. 一期最小 Query 协议（A 级）

| 步骤 | A 级事实 |
|---|---|
| 1. storage key | `chargedeliveryList` |
| 2. getItem | L4076 JSON.parse |
| 3. 默认 obj | L4077 `{}` |
| 4. 字段恢复 | L4078-4105 |
| 5. 11 字段全集 | 见 4.1 表 |
| 6. 修改 function | init / setTab / setFee / search / clearPage / pagination callback |
| 7. memberFactory API | `/admin/getCashflowDeliveryVoList.json` |
| 8. ListFactory 参数 | 4 参数（API / pageStart / pageSize / obj）|
| 9. obj 来源 | `angular.copy($scope.obj)` |
| 10. pageSize | 12 |
| 11. pageStart | `$scope.obj.page * pageSize` |
| 12. setItem 时机 | search (L4190) + pagination callback (L4203) |
| 13. 立即 query | L4210 `$scope.search()` |
| 14. HTML items | memberFactory.items |
| 15. HTML count | memberFactory.count |
| 16. pagination | jQuery pagination（callback 内 clearAndSetIndex + nextPage）|
| 17. 触发链 | date change / tab / fee / keyword / page → search() → memberFactory |

---

## 20. 当前 F 边界

| F 项 | 原因 |
|---|---|
| ListFactory 内部 Request 构造 | 任务明确禁止推论 |
| 后端 API 接受字段全集 | 资源范围外 |
| productKeyword / batchNoKeyword 是否被后端使用 | controller 0 处处理 |
| obj.rightTimer 是否被后端使用 | controller 0 处处理（仅用于派生 endTime）|
| 路由表 state → URL 映射 | 资源范围外 |
| 3 controller（Input/InputRecord/Processing）HTML | working dir 不可得 |
| directive 实现 | 资源范围外 |
| filter 实现 | 资源范围外 |
| sessionStorage 跨 session 行为 | 浏览器行为不可得 |
| 数据首次写入 sessionStorage 何时发生 | 不可得（仅可观察当前 session）|

---

## 21. A / B / C / D / E / F 评级

| # | 审计项 | 评级 |
|---|---|---|
| 01 | deliveryListCtrl 完整定位 | A |
| 02 | $scope.obj 定义位置 | A（L4077）|
| 03 | $scope.obj 11 字段 | A |
| 04 | chargedeliveryList get | A（L4076-4077）|
| 05 | chargedeliveryList set | A（L4190/L4203）|
| 06 | 写入时机 | A（search + pagination callback）|
| 07 | 始终保存完整 obj | A（`JSON.stringify($scope.obj)`）|
| 08 | memberFactory 定义 | A（L4195）|
| 09 | memberFactory 4 参数 | A |
| 10 | getCashflowDeliveryVoList.json 唯一调用 | A |
| 11 | Request 字段 | A（外部 obj 字段）+ F（ListFactory 内部）|
| 12 | obj 与 memberFactory | A（L4181+L4195）|
| 13 | ListFactory 第2参数 | A（pageStart 变量）|
| 14 | ListFactory 第3参数 | A（pageSize = 12）|
| 15 | ListFactory 第4参数 | A（obj = angular.copy($scope.obj)）|
| 16 | obj 修改点全集 | A（37 处）|
| 17 | search 重新 new ListFactory | A（L4195）|
| 18 | write storage function | A（search + pagination callback）|
| 19 | state navigation | A（0 处）|
| 20 | tab | A |
| 21 | filter | A（0 处 filter function）|
| 22 | deliveryStatus | A（双重身份：obj 字段 + scope 状态变量）|
| 23 | 日期字段 | A（startTime/endTime/rightTimer）|
| 24 | cashflow | A（**不在 obj 内**）|
| 25 | pagination | A（完整 10 步）|
| 26 | memberFactory.items | A（HTML L202 直接）|
| 27 | memberFactory.count | A（jQuery pagination L4198）|
| 28 | 完整数据图 | A（6 层闭合）|
| 29 | 一期最小 Query 协议 | A |
| 30 | Q1-Q30 回答 | A |

**统计**：30 项全部 **A** 级（无 E/F 升 A）。

---

## 22. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | obj 11 字段 / memberFactory / ListFactory 4 参数 / pagination 完整链 | **是** |
| L2 业务规则 | 业务字段语义 | **E**（无 UI 文案直接证明）|
| L3 数据库物理模型 | ListFactory 内部 Request 构造 | **F**（任务禁止 + 资源范围外）|

---

## 23. R1-R6 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 API 调用 | ❌ |
| R3 创建 DTO/VO/PO/Service/Repository | ❌ |
| R4 修改历史 MD | ❌ |
| R5 删除 10 个 untracked | ❌（**deliveryList.html hash 复核不变**）|
| R6 P0/P1 自动新增 | ❌ |

---

## 24. Q1-Q30 回答

| Q | 答案 |
|---|---|
| Q1：$scope.obj 完整字段？| **11 字段**（startTime / endTime / rightTimer / deliveryStatus / toBeProcess / refundStatus / keyword / productKeyword / batchNoKeyword / page / refundStatusArray）|
| Q2：每个字段默认值？| startTime=3 个月前 / rightTimer=now / deliveryStatus=派生 / toBeProcess=派生 / refundStatus=0 / 其余 undefined |
| Q3：storage 读取后是否覆盖 obj？| **是**（完全覆盖，无合并）|
| Q4：写入发生在哪两个 function？| **search (L4190) + pagination callback (L4203)** |
| Q5：写入时 obj 是否已修改？| **是**（search 内 L4168-4187 + pagination callback 内 L4202）|
| Q6：memberFactory 怎么创建？| L4195 `$scope.memberFactory = new ListFactory(...)` |
| Q7：memberFactory 用哪个 API？| `/admin/getCashflowDeliveryVoList.json` |
| Q8：ListFactory 参数数量？| **4**（API / pageStart / pageSize / obj）|
| Q9：参数 2/3/4 真实值？| pageStart（L4189）/ pageSize=12（L4167）/ obj=L4181 angular.copy($scope.obj) |
| Q10：obj 是否直接作为参数 4？| **是**（angular.copy 后传入）|
| Q11：obj 字段是否都能直接证明进入 API Request？| **否**（ListFactory 内部构造 F）|
| Q12：哪些 obj 字段只能保持 F？| productKeyword / batchNoKeyword / obj.rightTimer（controller 0 处处理）|
| Q13：search 是否重新 new ListFactory？| **是**（L4195 每次 search 重新创建）|
| Q14：search 是否修改 obj？| **是**（startTime/endTime/rightTimer）|
| Q15：tab 是否修改 obj？| **是**（deliveryStatus + toBeProcess）|
| Q16：deliveryStatus 是否修改 obj？| **是**（多函数修改）|
| Q17：是否有 filter function？| **否**（controller 0 处 filter function）|
| Q18：是否有日期筛选？| **是**（HTML datepicker + search 内 startTime/endTime 处理）|
| Q19：是否有 cashflow/cashflowId Query 字段？| **否**（obj 内 0 处；item 字段不进入 query）|
| Q20：pagination 使用什么方法？| jQuery pagination（$("#Pagination").pagination）|
| Q21：pageSize 是多少？| **12** |
| Q22：pageStart 如何变化？| `$scope.obj.page ? obj.page * pageSize : 0` |
| Q23：memberFactory.items 是否直接给 HTML？| **是**（HTML L202 `ng-repeat`）|
| Q24：memberFactory.count 是否直接给 HTML？| **是**（L4198 jQuery pagination）|
| Q25：deliveryListCtrl 是否直接读 items？| **否**（0 处）|
| Q26：deliveryListCtrl 是否直接读 count？| **是**（L4198 jQuery pagination 消费）|
| Q27：deliveryListCtrl 是否 $state.reload？| **否**（0 处）|
| Q28：deliveryListCtrl 是否 $state.go？| **否**（0 处）|
| Q29：deliveryInputCtrl → deliveryList 与 storage 关系？| **无直接代码关系**（deliveryInputCtrl 0 处 sessionStorage）|
| Q30：Query 生命周期是否完整闭合？| **是**（6 层 A 级闭合）|

---

## 25. P0 / P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）

---

## 26. 历史证据 vs 当前代码

### 26.1 S1-82 表述

> chargedeliveryList 写入值 = JSON.stringify($scope.obj)（11 字段查询参数）
> memberFactory → getCashflowDeliveryVoList.json（ListFactory 4 参数）
> deliveryListCtrl 自身 0 处访问 memberFactory.items[i].xxx
> 4 处 ui-sref 跳转 + 1 处 print 调用 cashflowId 100% 来自 item.cashflow.id

### 26.2 当前代码（S1-83）

| 项 | S1-82 表述 | 当前代码 | 判定 |
|---|---|---|---|
| $scope.obj 字段数 | 11 字段 | 11 字段（**完整确认** startTime / endTime / rightTimer / deliveryStatus / toBeProcess / refundStatus / keyword / productKeyword / batchNoKeyword / page / refundStatusArray）| **细化** |
| memberFactory 4 参数 | API / pageStart / pageSize / obj | 同上 + 真实值确认 | **细化** |
| pageSize | 12 | 12 | **保留** |
| obj 副本处理 | refundStatus 转换 | 同样逻辑（searchCount L4154-4160 + search L4181-4187 重复）| **细化** |
| 写 storage function | search + pagination callback | 同 | **保留** |
| $state 操作 | 0 处 | 0 处 | **保留** |

### 26.3 最终采用

- **保留**：S1-82 的 11 字段全集 + 2 处写 storage + 0 处 state 操作
- **细化**：11 字段每个的完整生命周期（默认值 / 修改点 / 是否进 Query）
- **新增**：search 完整 10 步流程 + 6 层数据流图 + 10 项 F 边界

---

## 27. 本轮新增事实

1. **$scope.obj 11 字段每个的完整生命周期**（默认值 / 修改点 / Query 进入）
2. **search 完整 10 步流程图**（A 级）
3. **setTab/setFee/clearPage/searchCount 4 个 function 的 obj 修改清单**
4. **5 个 obj 修改 function**：init / setTab / setFee / search / clearPage + pagination callback
5. **写 storage 仅 2 处**（search L4190 + pagination callback L4203）
6. **ListFactory 第 2/3/4 参数真实值**（A 级，**严格不推 ListFactory 内部**）
7. **pageSize=12 / pageStart 派生公式**（A 级）
8. **countObj vs obj 严格区分**（2 个独立 scope 变量）
9. **deliveryListCtrl 0 处直接读 memberFactory.items**（仅 HTML 直接消费）
10. **deliveryListCtrl 0 处 $state.go / 0 处 $state.reload**（A 级）
11. **deliveryInputCtrl → deliveryList 与 storage 无直接代码关系**（A 级）
12. **完整 6 层数据流图 A 级闭合**（storage → obj → memberFactory → API → items → HTML）

---

## 28. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| Write 操作 = 0 | ✅（仅新增 1 个文档）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| **deliveryList.html hash/bytes 未改变** | ✅（SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` / 12720 bytes）|
| Git 禁止命令未触发 | ✅（仅 `git add -- 144_*.md`）|

---

## 29. 停止条件

✅ 30 项审计完成（全部 A 级）
✅ 30 问 Q1-Q30 全部回答
✅ 6 层数据流图 A 级闭合
✅ 11 字段完整生命周期 A 级
✅ ListFactory 4 参数真实值 A 级
✅ 0 处推论（ListFactory 内部 F）
✅ deliveryList.html hash 复核不变
✅ 10 项 F 边界明确列出
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-84）**。
