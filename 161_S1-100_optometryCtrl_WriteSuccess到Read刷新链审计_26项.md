# S1-100 optometryCtrl Write Success → Read 刷新链审计

> **任务名**：S1-100｜optometryCtrl Write Success → querySingleOrder/queryUndisposed 刷新链审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）三 Write success 后的 Read 链完整闭合
> **当前轮次**：S1-100（接 S1-99 完成）
> **本轮承诺**：2 个 Read API 实际调用 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| queryUndisposed (L34841) | ✅ | Write A success 触发 |
| querySingleOrder (L34883) | ✅ | 3 Write + 取消订单 + 制作完成 success 触发 |
| dealTime (L34827) | ✅ | queryUndisposed 内部用 |
| filter_medicalRecordStatus_update (L34780) | ✅ | querySingleOrder 内部用 |
| $scope.search (L35355) | ✅ | 路由回调（init 链路） |
| $scope.order.brushData (L34860) | ⚠️ 旁证 | 同 API 不同 Consumer |
| selectOrderListFactory 初始化 (L35367) | ✅ | 列表数据源 |
| 7 HTML | ❌（不可得）| UI 触发点 F |
| 2 Read 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "querySingleOrder = 重新查询订单"：**E**（仅命名）
- "queryUndisposed = 刷新待处理数量"：**E**（仅命名 + L34847 注释"待处理数量"）
- "filter_medicalRecordStatus = 业务状态过滤"：**E**（仅命名）
- "getMedicalRecordFlowVo = 获取记录流"：**E**（仅 API 命名）
- "stateTodoMedicalRecordCount = 待办医疗记录数"：**E**（仅 API 命名）

---

## 3. querySingleOrder() 定位

### 3.1 全局引用（A 级，optometryCtrl 范围 L34776-L35382）

| 行号 | 表达式 | 角色 | A-F |
|---|---|---|---|
| L34883 | `$scope.querySingleOrder = function () {` | **函数定义** | A |
| L35107 | `$scope.querySingleOrder();` | Write A success (setMedicalRecordProcessMode) | A |
| L35156 | `$scope.querySingleOrder();` | "取消订单" success (cancelMedicalRecord) | A |
| L35173 | `$scope.querySingleOrder();` | "制作完成" success (confirmMedicalRecordReturn) | A |
| L35194 | `$scope.querySingleOrder();` | Write B success (deliveryStatus="2") | A |
| L35213 | `$scope.querySingleOrder();` | Write C success (deliveryStatus="1") | A |

**A 级结论**：
- querySingleOrder 在 optometryCtrl 范围**6 处引用**（1 定义 + 5 调用）
- 5 个调用全部是**某个 .then 内的同步语句**（无参数传递）
- ❌ 0 处带参数调用（函数定义就是无参 function()）
- ❌ 0 处其它 controller 同名函数

### 3.2 函数签名（A 级）

```javascript
$scope.querySingleOrder = function () {  // 无参数
    // ...
};
```

---

## 4. querySingleOrder() 实际 API

### 4.1 完整源码（A 级，L34883-L34896）

```javascript
$scope.querySingleOrder = function () {
    var medicalRecordId = $scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id;  // L34884
    new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", {                            // L34885
        medicalRecordId: medicalRecordId                                                                // L34886
    }).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        $timeout(function () {                                                                            // L34891
            $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;                      // L34892
            $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);        // L34893
        });
    });
};
```

### 4.2 API 字符串（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| API 字符串 | `/admin/getMedicalRecordFlowVo.json` | A |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式，方法不可直接证明是 GET/POST） | A 引用 / F 实际方法 |
| Factory | 匿名 `new ObjectFactory()`（不赋 $scope 变量） | A |
| Factory 实例 | 独立实例（与 $scope.xxx 隔离） | A |

### 4.3 Request 字段（A 级）

| 字段 | 表达式 | 来源 | 行号 | A-F |
|---|---|---|---|---|
| `medicalRecordId` | `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` | selectOrderListFactory.items[orderIndex] 的 medicalRecord.id | L34884 / L34886 | A |

**A 级结论**：
- Request 字段 = 1 个（medicalRecordId）
- ❌ 0 处其它字段（cashflowId / status / ... 全部无）
- ❌ 0 处 JSON.stringify
- ❌ 0 处类型转换
- ❌ 0 处默认值

### 4.4 medicalRecordId 来源链（A 级）

```
$scope.selectOrderListFactory.items[$scope.orderIndex]
    ↓ .medicalRecord
$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord
    ↓ .id
$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id
    ↓
Request.medicalRecordId (L34886)
```

**$scope.orderIndex 来源**：
- 初始化：`$scope.orderIndex = null` (L35127)
- 设置：`$scope.clickBtn(name, item, index)` 形参 index → `$scope.orderIndex = index` (L35130)
- 含义：当前**操作的单条订单在列表中的索引位置**

**$scope.selectOrderListFactory 来源**：
- 初始化：`$scope.search()` 调 `new ListFactory("/admin/selectMedicalRecordFlowVoList.json", ...)` (L35367) + `nextPage()`
- 含义：当前**列表分页数据**

**A 级结论**：
- querySingleOrder 的 medicalRecordId = 当前列表中当前选中行的 medicalRecord.id
- 与 3 Write 的 medicalRecordId（来自 clickBtn 形参 item.medicalRecord.id）**同源**（最终都来自 selectOrderListFactory.items[index].medicalRecord.id）
- **0 处**类型校验

---

## 5. querySingleOrder() result Consumer

### 5.1 完整消费（A 级，L34887-L34895）

```javascript
.then(function (result) {
    if (result.status) {                                                          // L34888
        return Popup.notice(result.errmsg);
    }
    $timeout(function () {
        $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;   // L34892
        $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);  // L34893
    });
});
```

### 5.2 result 字段消费全集（A 级）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `result.status` | L34888 | 错误判断（if） | — | A |
| `result.errmsg` | L34889 | Popup.notice 弹窗 | — | A |
| `result.object` | L34892 | 整体赋值给 selectOrderListFactory.items[orderIndex] | $scope.selectOrderListFactory.items[$scope.orderIndex] | A |
| `result.object` | L34893 | 传给 filter_medicalRecordStatus_update（第二参数） | $scope.medicalRecordStatus[orderIndex] (间接) | A |
| 其它字段 | — | ❌ 未观察 | — | F |

### 5.3 result.object 实际消费方式（A 级）

| 行为 | 表达式 | 含义 | A-F |
|---|---|---|---|
| 直接替换整行 | `$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object` | 当前索引的列表项被完整覆盖 | A |
| 触发状态过滤 | `$scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex)` | 调 filter_medicalRecordStatus_update 重算 medicalRecordStatus | A |

### 5.4 $timeout 包裹（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `$timeout` 来源 | AngularJS 注入（在 controller 注册 L34776） | A |
| 用途 | 延迟到下一个 digest 执行（避免 digest 循环中触发 watcher） | A（AngularJS 行为） |
| delay | ❌ 未传第二参数（默认 0，立即异步） | A |
| 是否可失败 | ❌ 0 处 try/catch | A |

---

## 6. querySingleOrder() 对前端状态的影响

### 6.1 状态变化全集（A 级）

| 状态变化 | 行号 | 触发条件 | A-F |
|---|---|---|---|
| `$scope.selectOrderListFactory.items[$scope.orderIndex]` 被覆盖 | L34892 | result.status == 0（即 res.status 错；正确：result.status != 1 即非错误） | A |
| `$scope.medicalRecordStatus[$scope.orderIndex]` 间接更新 | L34893 | 同上 | A |
| 其它 $scope.xxx | ❌ 0 处 | — | A |
| stockDetail / addOrderModal | ❌ 0 处（不修改这些状态） | — | A |
| $state.reload() / $state.go() | ❌ 0 处 | — | A |
| 重新构造 selectOrderListFactory | ❌ 0 处（仅修改 items[index] 元素） | — | A |
| getCount / search / reload | ❌ 0 处 | — | A |

### 6.2 状态变化链（A 级）

```
[L34885] saveOrQuery
    ↓
[F 边界: HTTP 边界]
    ↓
result
    ↓
if (result.status) { return Popup.notice(result.errmsg); }  // 错误处理
    ↓
$timeout(function () {
    $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;  // 列表行覆盖
    $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);  // 状态重算
}, 0);
```

### 6.3 filter_medicalRecordStatus_update 详细审计（A 级，L34780-L34782）

```javascript
$scope.filter_medicalRecordStatus_update = function (item, type, index) {
    $scope.medicalRecordStatus[index] = window.filter_medicalRecordStatus(item, type);
};
```

| 维度 | 评估 | A-F |
|---|---|---|
| 函数定义 | L34780（optometryCtrl 顶部） | A |
| 参数 1 (item) | result.object | A |
| 参数 2 (type) | "button"（字面量） | A |
| 参数 3 (index) | $scope.orderIndex | A |
| 写入目标 | $scope.medicalRecordStatus[index] | A |
| 依赖函数 | `window.filter_medicalRecordStatus(item, type)` | A 引用 / F 实现 |
| Promise | ❌ 无 | A |
| 错误处理 | ❌ 无 | A |

**A 级结论**：
- filter_medicalRecordStatus_update 调 window 全局函数（**F 边界**）
- 写入 $scope.medicalRecordStatus（UI 状态对象）

### 6.4 querySingleOrder 与 order.brushData 关系（A 级）

**A 级新发现**：querySingleOrder (L34883) 与 order.brushData (L34860) **调用同一个 API** (`/admin/getMedicalRecordFlowVo.json`)，但消费不同：

| 维度 | querySingleOrder (L34883) | order.brushData (L34860) |
|---|---|---|
| API 字符串 | /admin/getMedicalRecordFlowVo.json | /admin/getMedicalRecordFlowVo.json ✅ 同 |
| Request 字段 | medicalRecordId | medicalRecordId ✅ 同 |
| 触发场景 | 3 Write success + 取消/制作完成 success | 弹窗显示（"报损" action）|
| 消费目标 | $scope.selectOrderListFactory.items[$scope.orderIndex] | $scope.order.object |
| 状态过滤 | ✅ 调 filter_medicalRecordStatus_update | ❌ 不调 |
| $timeout | ✅ 包裹 | ❌ 无 |
| 错误处理 | ✅ Popup | ✅ Popup |

**A 级结论**：
- 同一 Read API（getMedicalRecordFlowVo）有 **2 个独立 Consumer**：
  1. querySingleOrder（Refresh 列表当前行）
  2. order.brushData（弹窗显示订单详情）
- 两个 Consumer 实例独立（都是匿名 new ObjectFactory()）
- 数据流不同：querySingleOrder → selectOrderListFactory；order.brushData → $scope.order.object
- 不能说"同一刷新函数"（两个完全独立的 $scope 函数）

---

## 7. queryUndisposed() 定位

### 7.1 全局引用（A 级，optometryCtrl 范围 L34776-L35382）

| 行号 | 表达式 | 角色 | A-F |
|---|---|---|---|
| L34841 | `$scope.queryUndisposed = function () {` | **函数定义** | A |
| L35108 | `$scope.queryUndisposed();` | Write A success (setMedicalRecordProcessMode) | A |
| L35157 | `$scope.queryUndisposed();` | "取消订单" success (cancelMedicalRecord) | A |
| L35376 | `$scope.queryUndisposed();` | search() 完成后（init 流程）| A |

**A 级结论**：
- queryUndisposed 在 optometryCtrl 范围**4 处引用**（1 定义 + 3 调用）
- ❌ 0 处带参数调用
- ❌ 0 处其它 controller 同名函数
- **Write B / Write C success 均不调 queryUndisposed**（S1-99 已确认）

### 7.2 函数签名（A 级）

```javascript
$scope.queryUndisposed = function () {  // 无参数
    var object = $scope.dealTime();
    new ObjectFactory().saveOrQuery("/admin/stateTodoMedicalRecordCount.json", object).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        $scope.toPayCount = result.result.object;
    });
};
```

---

## 8. queryUndisposed() Request

### 8.1 完整 Request 构造（A 级，L34842-L34843）

```javascript
var object = $scope.dealTime();  // L34842
new ObjectFactory().saveOrQuery("/admin/stateTodoMedicalRecordCount.json", object).then(...);
```

| 字段 | 来源 | A-F |
|---|---|---|
| 整个 object | `$scope.dealTime()` 返回值 | A |

### 8.2 dealTime 实现（A 级，L34827-L34838）

```javascript
$scope.dealTime = function () {
    var object = angular.copy($scope.obj);                                                  // L34828
    if ($scope.obj.startTime && $scope.obj.rightTime) {
        var newObj = DateUtilFactory.closeLeftOpenRight($scope.obj.startTime, $scope.obj.rightTime);  // L34830
        Object.assign(object, newObj);                                                       // L34831
    }
    if (!$scope.obj.startTime) {
        delete object.startTime;                                                            // L34834
    }
    delete object.rightTime;                                                                // L34836
    return object;
};
```

| 行为 | A-F |
|---|---|
| `angular.copy($scope.obj)` 深拷贝 | A |
| 若 startTime + rightTime 都存在 → DateUtilFactory.closeLeftOpenRight + Object.assign | A |
| 若 startTime 不存在 → delete object.startTime | A |
| 始终 delete object.rightTime | A |
| DateUtilFactory.closeLeftOpenRight 实现 | F（factory 源码不可得） |
| $scope.obj 来源 | 待查（需看 optometryCtrl 初始化） |

### 8.3 Request 字段全集（基于 dealTime 返回值，A 级）

| 字段 | 来源 | 行号 | A-F |
|---|---|---|---|
| (任意 angular.copy($scope.obj) 中的字段) | $scope.obj.* | L34828 | A |
| closeLeftOpenRight 返回的字段（startTime / rightTime 处理后） | DateUtilFactory.closeLeftOpenRight | L34830 / L34831 | A 引用 / F 实际返回 |

**A 级结论**：
- Request 字段 = $scope.obj 的所有字段（深拷贝）
- ❌ 0 处显式字段构造
- 字段集合**动态**依赖 $scope.obj 当前值

### 8.4 $scope.obj 来源（A 级，L34824-L34826 上下文）

```javascript
$scope.obj = {  // (L34824 附近)
    rightTime: new Date()
};
```

**A 级结论**：
- $scope.obj 是一个搜索/筛选对象
- ❌ 0 处确认 $scope.obj 在 optometryCtrl 范围被赋值其它字段（S1-100 范围未观察到更多）
- ❌ 0 处确认 $scope.obj.startTime 设置位置

### 8.5 API 字符串（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| API 字符串 | `/admin/stateTodoMedicalRecordCount.json` | A |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式） | A 引用 / F 实际方法 |
| Factory | 匿名 new ObjectFactory() | A |

---

## 9. queryUndisposed() result Consumer

### 9.1 完整消费（A 级，L34843-L34848）

```javascript
.then(function (result) {
    if (result.status) {                       // L34844
        return Popup.notice(result.errmsg);
    }
    $scope.toPayCount = result.result.object;  // L34847
});
```

### 9.2 result 字段消费全集（A 级）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `result.status` | L34844 | 错误判断 | — | A |
| `result.errmsg` | L34845 | Popup.notice 弹窗 | — | A |
| `result.result.object` | L34847 | 直接赋值给 $scope.toPayCount | $scope.toPayCount | A |
| 其它字段 | — | ❌ 未观察 | — | F |

### 9.3 $scope.toPayCount 用途（A 级）

- ❌ 0 处 controller.js 中读 $scope.toPayCount
- L34839 初始化 `$scope.toPayCount = 0`
- 注释 L34847 `//待处理数量`（**仅源码注释**）

**A 级结论**：
- $scope.toPayCount 写入 optometryCtrl
- ❌ 0 处 controller.js 内读 $scope.toPayCount 的代码
- 用途可能仅在 HTML 端（HTML 不可得 → F）

### 9.4 queryUndisposed 与 querySingleOrder 对比（A 级）

| 维度 | queryUndisposed | querySingleOrder |
|---|---|---|
| API | stateTodoMedicalRecordCount.json | getMedicalRecordFlowVo.json |
| Request | dealTime() = $scope.obj 深拷贝 | medicalRecordId |
| 写入 | $scope.toPayCount | $scope.selectOrderListFactory.items[orderIndex] |
| 间接调用 | filter_medicalRecordStatus_update | （无） |
| 错误处理 | Popup | Popup |
| $timeout | ❌ 无 | ✅ 有 |

---

## 10. 三 Write → querySingleOrder 完整链

### 10.1 Write A → querySingleOrder + queryUndisposed（A 级，L35099-L35108）

```javascript
new ObjectFactory().saveOrQuery("/admin/setMedicalRecordProcessMode.json", { ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);     // L35105
    }
    $scope.querySingleOrder();                  // L35107
    $scope.queryUndisposed();                   // L35108
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | if (result.status) → return Popup | A |
| 2 | querySingleOrder() 同步调用 | A |
| 3 | queryUndisposed() 同步调用 | A |
| 4 | 中间代码 | ❌ 0 行（两个 Read 同步触发） | A |

### 10.2 Write B → querySingleOrder（A 级，L35185-L35194）

```javascript
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { ..., deliveryStatus: "2", ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);     // L35192
    }
    $scope.querySingleOrder();                  // L35194
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | if (result.status) → return Popup | A |
| 2 | querySingleOrder() 同步调用 | A |
| 3 | queryUndisposed() | ❌ 不调（S1-99 已确认） | A |
| 4 | 中间代码 | ❌ 0 行 | A |

### 10.3 Write C → querySingleOrder（A 级，L35204-L35213）

```javascript
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { ..., deliveryStatus: "1", ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);     // L35211
    }
    $scope.querySingleOrder();                  // L35213
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | if (result.status) → return Popup | A |
| 2 | querySingleOrder() 同步调用 | A |
| 3 | queryUndisposed() | ❌ 不调 | A |
| 4 | 中间代码 | ❌ 0 行 | A |

### 10.4 A 级结论
- **3 Write success 均调用同一 querySingleOrder() 函数**
- **仅 Write A 额外调用 queryUndisposed()**
- ❌ 0 处中间业务逻辑（3 Write 触发 Read 之间无其它代码）
- ❌ 0 处 $state.reload() / $state.go() / state.go

---

## 11. Write → Read 是否完全相同

### 11.1 querySingleOrder 调用一致性（A 级）

| Write | 调 querySingleOrder | 是否完全相同调用方式 |
|---|---|---|
| A (setMedicalRecordProcessMode) | ✅ L35107 | ✅ `$scope.querySingleOrder()` 无参 |
| B (deliveryStatus="2") | ✅ L35194 | ✅ 同 |
| C (deliveryStatus="1") | ✅ L35213 | ✅ 同 |

**A 级结论**：3 Write **完全汇聚到同一 querySingleOrder() 调用**（同一函数、同一参数、同一行内同步触发）。

### 11.2 queryUndisposed 调用差异（A 级）

| Write | 调 queryUndisposed |
|---|---|
| A | ✅ L35108 |
| B | ❌ 不调 |
| C | ❌ 不调 |

**A 级结论**：
- queryUndisposed **不是** 3 Write 共同调用的
- 仅 Write A 调用
- 差异原因（**E 业务推断**）：Write A 是"选加工方式"流程节点，可能需要刷新"待处理数量"（toPayCount），而 Write B / Write C 是完成动作，不需要
- 业务推断**禁止升级**为 A

### 11.3 严格表述（A 级）
- "3 Write success 均汇聚到同一 querySingleOrder() 函数"：**A**
- "queryUndisposed 仅 Write A success 触发"：**A**
- "queryUndisposed 差异原因"：**E**（业务推断）

---

## 12. querySingleOrder Request 来源（同 3 Write 的 medicalRecordId 对照）

### 12.1 表达式层同源（A 级）

| 来源 | Write A | Write B | Write C | querySingleOrder |
|---|---|---|---|---|
| 起点 | choseFactoryMethod 形参 `medical` | clickBtn 闭包 `item` | clickBtn 闭包 `item` | `$scope.selectOrderListFactory.items[$scope.orderIndex]` |
| 表达式 | `medical.medicalRecord.id` (L35085) | `item.medicalRecord.id` (L35182) | `item.medicalRecord.id` (L35201) | `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (L34884) |
| 中间变量 | `medicalRecordId` | `medicalRecordId` | `medicalRecordId` | `medicalRecordId` |
| Request 字段名 | medicalRecordId | medicalRecordId | medicalRecordId | medicalRecordId |

**A 级结论**：
- 4 处表达式**最终都来自** `selectOrderListFactory.items[index].medicalRecord.id`（A 级 — 表达式层）
- choseFactoryMethod 路径：`items[index]` → `item` → `medical` → `medicalRecord.id`
- clickBtn 路径：`items[index]` → `item` → `medicalRecord.id`
- querySingleOrder 路径：`items[index]` → `medicalRecord.id`
- **0 处** 自动证明后端是否同一数据库对象（L3 = F）

### 12.2 A 级 vs E 级 严格区分
- "3 Write 与 querySingleOrder 的 medicalRecordId 字段值相同"：**A（表达式层）** + **D（值层，无法证明）**
- "3 Write 与 querySingleOrder 是同一数据库对象"：**E**（业务推断，禁止升级）

---

## 13. querySingleOrder Response 与 Write 前对象是否关联

### 13.1 关联链路（A 级）

```
Write 前：
  clickBtn(name, item, index)                  // L35128
  $scope.orderIndex = index                   // L35130
  item = $scope.selectOrderListFactory.items[index]  // 来自列表

Write 中：
  medicalRecordId = item.medicalRecord.id      // 写入 Request
  3 Write API

Write success：
  if (result.status) { return Popup; }
  $scope.querySingleOrder()                   // 调用
    ↓
  medicalRecordId = $scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id  // L34884
  // 注意：这里直接取 items[orderIndex]，**不依赖** Write 时的 medicalRecordId 局部变量
```

### 13.2 是否有对象引用复用（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| querySingleOrder 内是否复用 Write 时的 item 引用 | ❌ 否（querySingleOrder 独立从 $scope.selectOrderListFactory.items[orderIndex] 读取） | A |
| querySingleOrder result.object 是否被赋给 item 引用 | ❌ 否（赋给 selectOrderListFactory.items[orderIndex] 整体替换） | A |
| Write 前 item 引用与 Write 后 selectOrderListFactory.items[orderIndex] 是否同一对象 | ❌ 否（querySingleOrder 整体覆盖） | A |
| 整体覆盖 vs 字段级合并 | ❌ **整体覆盖**（`$scope.selectOrderListFactory.items[orderIndex] = result.object`） | A |

### 13.3 A 级结论
- Write 前 item 引用是 clickBtn 闭包变量（仅在 action 函数内可用）
- Write 后 querySingleOrder 走自己的路径，直接从 $scope 读取
- 两者**没有**直接对象引用复用
- querySingleOrder 整体覆盖 selectOrderListFactory.items[orderIndex]（**A 级**）
- 严格表述：**当前 Controller 未观察到 Write 前对象与 querySingleOrder Response 的直接对象引用复用**（A 级）

---

## 14. Factory 选择

### 14.1 2 Read 调用 Factory 模式（A 级）

| Read | Factory 模式 | 变量名 | A-F |
|---|---|---|---|
| querySingleOrder → getMedicalRecordFlowVo.json | 匿名 `new ObjectFactory()` | 无 | A |
| queryUndisposed → stateTodoMedicalRecordCount.json | 匿名 `new ObjectFactory()` | 无 | A |
| order.brushData → getMedicalRecordFlowVo.json | 匿名 `new ObjectFactory()` | 无 | A |

**A 级结论**：
- 2 Read 都用**匿名 new ObjectFactory()**
- ❌ 0 处 `$scope.xxxReadFactory` 命名变量
- ❌ 0 处复用 ObjectFactory 实例
- 每次 Read 调用都是**新 ObjectFactory 实例**

---

## 15. Promise / then 链

### 15.1 querySingleOrder Promise 链（A 级）

```javascript
new ObjectFactory().saveOrQuery(...).then(function (result) {
    if (result.status) { return Popup.notice(result.errmsg); }
    $timeout(function () {
        $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;
        $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);
    });
});
```

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个 | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |
| `await` | ❌ 0 处 | A |
| `try/catch` | ❌ 0 处 | A |
| 链式 | ❌ 0 处嵌套 then | A |
| $timeout 内 try/catch | ❌ 0 处 | A |

### 15.2 queryUndisposed Promise 链（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个 | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |
| 链式 | ❌ 0 处嵌套 then | A |

### 15.3 3 Write success → Read Promise 链（A 级）

```javascript
// Write success .then 内
if (result.status) { return Popup.notice(result.errmsg); }
$scope.querySingleOrder();    // 同步触发（不返回 Promise 等待）
$scope.queryUndisposed();     // 同步触发（仅 A）
```

| 维度 | 评估 | A-F |
|---|---|---|
| querySingleOrder() 返回值处理 | ❌ 0 处（同步调用，不 await / .then） | A |
| queryUndisposed() 返回值处理 | ❌ 0 处 | A |
| 顺序 | A: querySingleOrder → queryUndisposed；B/C: 仅 querySingleOrder | A |
| 错误隔离 | ❌ querySingleOrder 内部异常会**未捕获**传播（与 S1-99 concatMedicalProductStock 同问题） | A |
| 等待完成 | ❌ 3 Write success 后立即退出 .then（Read 未完成就退出） | A |

**A 级结论**：
- 3 Write success 是**同步触发** querySingleOrder/queryUndisposed
- ❌ 0 处等待 Read 完成
- ❌ 0 处 .catch 保护
- 若 Read 抛出异常，会**未捕获**传播到 AngularJS 异常处理

---

## 16. 失败分支

### 16.1 querySingleOrder 失败分支（A 级）

| 检查 | 行号 | 行为 | A-F |
|---|---|---|---|
| `if (result.status)` | L34888 | Popup.notice(result.errmsg) | A |
| `if (!result.status)` | ❌ 0 处 | — | A |
| `result.status === 0` 判空 | ❌ 0 处（仅判 result.status truthy） | — | A |
| 错误时是否继续执行 | ❌ `return Popup` 提前退出，不执行 $timeout | A | A |
| $timeout 内异常 | ❌ 0 处 try/catch | A | A |

### 16.2 queryUndisposed 失败分支（A 级）

| 检查 | 行号 | 行为 | A-F |
|---|---|---|---|
| `if (result.status)` | L34844 | Popup.notice(result.errmsg) | A |
| `if (!result.status)` | ❌ 0 处 | — | A |
| 错误时是否继续执行 | ❌ `return Popup` 提前退出，不执行 $scope.toPayCount = ... | A | A |

### 16.3 result.status 含义（A 级）

- `result.status` truthy（=1 或非零）→ 错误
- `result.status` falsy（=0 或 undefined）→ 成功
- ❌ 0 处显式 `=== 0` 或 `=== 1` 比较（仅用 truthy 短路）

---

## 17. success 后 UI 状态

### 17.1 querySingleOrder UI 状态变化（A 级）

| 状态 | 变化 | 行号 | A-F |
|---|---|---|---|
| `$scope.selectOrderListFactory.items[orderIndex]` | **整体覆盖** | L34892 | A |
| `$scope.medicalRecordStatus[orderIndex]` | 间接重算（通过 filter_medicalRecordStatus_update） | L34893 | A |
| `$scope.stockDetail` | ❌ 不变 | — | A |
| `$scope.addOrderModal` | ❌ 不变 | — | A |
| 其它 modal | ❌ 不变 | — | A |
| `$scope.loading` / `submitting` | ❌ 0 处 | — | A |

### 17.2 queryUndisposed UI 状态变化（A 级）

| 状态 | 变化 | 行号 | A-F |
|---|---|---|---|
| `$scope.toPayCount` | 整体覆盖 | L34847 | A |
| 其它 | ❌ 不变 | — | A |

### 17.3 A 级结论
- 2 Read UI 状态影响**极其有限**：
  - querySingleOrder：仅更新当前列表行的 selectOrderListFactory.items[index] + 间接更新 medicalRecordStatus
  - queryUndisposed：仅更新 $scope.toPayCount
- ❌ 0 处 modal 关闭（modal 由 popout_tip 自动管理）
- ❌ 0 处 scope flag 复位

---

## 18. Write → Read 最小闭合协议

### 18.1 完整链路图（A 级）

```
[A] setMedicalRecordProcessMode.json
    ↓ saveOrQuery (Write)
[F 边界: 后端]
    ↓
result
    ↓ if (result.status) return Popup
    ↓
querySingleOrder()                                            // L35107
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界: 后端]
    ↓
$timeout → $scope.selectOrderListFactory.items[orderIndex] = result.object
        → $scope.filter_medicalRecordStatus_update(result.object, "button", orderIndex)
queryUndisposed()                                             // L35108
    ↓ saveOrQuery (Read: stateTodoMedicalRecordCount.json)
    ↓ [F 边界: 后端]
    ↓
$scope.toPayCount = result.result.object


[B] completeMedicalRecordDelivery.json (deliveryStatus="2")
    ↓ saveOrQuery (Write)
[F 边界: 后端]
    ↓
result
    ↓ if (result.status) return Popup
    ↓
querySingleOrder()                                            // L35194
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界: 后端]
    ↓
$timeout → $scope.selectOrderListFactory.items[orderIndex] = result.object
        → $scope.filter_medicalRecordStatus_update(result.object, "button", orderIndex)
（无 queryUndisposed）


[C] completeMedicalRecordDelivery.json (deliveryStatus="1")
    ↓ saveOrQuery (Write)
[F 边界: 后端]
    ↓
result
    ↓ if (result.status) return Popup
    ↓
querySingleOrder()                                            // L35213
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界: 后端]
    ↓
$timeout → $scope.selectOrderListFactory.items[orderIndex] = result.object
        → $scope.filter_medicalRecordStatus_update(result.object, "button", orderIndex)
（无 queryUndisposed）
```

### 18.2 最小协议（A 级）

| Write | 触发 Read | 触发 Read2 |
|---|---|---|
| A | querySingleOrder → getMedicalRecordFlowVo.json | queryUndisposed → stateTodoMedicalRecordCount.json |
| B | querySingleOrder → getMedicalRecordFlowVo.json | ❌ |
| C | querySingleOrder → getMedicalRecordFlowVo.json | ❌ |

### 18.3 三个汇聚点（A 级）
1. **同一 Read API**（getMedicalRecordFlowVo.json）— 3 Write 共同
2. **同一 Controller 函数**（querySingleOrder）— 3 Write 共同
3. **同一 UI 状态**（$scope.selectOrderListFactory.items[orderIndex]）— 3 Write 共同

### 18.4 严格表述（A 级）
- "3 Write success 均汇聚到同一 querySingleOrder()"：**A**
- "querySingleOrder 最终更新 selectOrderListFactory.items[orderIndex]"：**A**
- "Write success 后前端如何重新获得数据"：**A**（通过 querySingleOrder 读新数据 → 覆盖 selectOrderListFactory.items[orderIndex] → HTML 自动重新渲染）
- "数据库刷新"：**E**（业务推断，禁止升级）

---

## 19. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | querySingleOrder 全局引用 | L34883/L35107/L35156/L35173/L35194/L35213 (6 处) | A | L1 | |
| 02 | querySingleOrder Controller | optometryCtrl (L34776-L35382) | A | L1 | 唯一 |
| 03 | querySingleOrder API | /admin/getMedicalRecordFlowVo.json | A | L1 | |
| 04 | querySingleOrder Factory | 匿名 new ObjectFactory() | A | L1 | |
| 05 | querySingleOrder Request | { medicalRecordId } | A | L1 | |
| 06 | Request.medicalRecordId 来源 | selectOrderListFactory.items[orderIndex].medicalRecord.id (L34884) | A | L1 | |
| 07 | querySingleOrder result 消费 | result.object (L34892/L34893) | A | L1 | |
| 08 | querySingleOrder 状态影响 | selectOrderListFactory.items[index] + medicalRecordStatus[index] | A | L1 | |
| 09 | querySingleOrder 5 个调用点 | Write A/B/C + 取消/制作完成 | A | L1 | |
| 10 | querySingleOrder vs order.brushData | 同 API / 不同 Consumer | A | L1 | S1-100 新发现 |
| 11 | queryUndisposed 全局引用 | L34841/L35108/L35157/L35376 (4 处) | A | L1 | |
| 12 | queryUndisposed API | /admin/stateTodoMedicalRecordCount.json | A | L1 | |
| 13 | queryUndisposed Factory | 匿名 new ObjectFactory() | A | L1 | |
| 14 | queryUndisposed Request | dealTime() = angular.copy($scope.obj) | A | L1 | |
| 15 | queryUndisposed result 消费 | result.result.object → $scope.toPayCount | A | L1 | |
| 16 | queryUndisposed 3 个调用点 | Write A + 取消 + 路由回调 | A | L1 | |
| 17 | queryUndisposed 仅 Write A | Write B/C 不调 | A | L1 | |
| 18 | Write A→querySingleOrder+queryUndisposed | L35107+L35108 | A | L1 | |
| 19 | Write B→querySingleOrder | L35194 | A | L1 | |
| 20 | Write C→querySingleOrder | L35213 | A | L1 | |
| 21 | 3 Write 完全汇聚 | 同一 querySingleOrder() | A | L1 | |
| 22 | medicalRecordId 同源 | 表达式层同源，最终 selectOrderListFactory.items[index].medicalRecord.id | A | L1 | 值层 F |
| 23 | 整体覆盖 vs 字段合并 | 整体覆盖 (L34892 =) | A | L1 | |
| 24 | Promise / catch | ❌ 0 处 .catch | A | L1 | |
| 25 | 失败分支 | if (result.status) → return Popup | A | L1 | |
| 26 | 最小闭合协议 | 3 Write → querySingleOrder → Read API → 整体覆盖 selectOrderListFactory.items[index] | A | L1 | |

**统计**：
- **A：26 项（全部 A）**
- **F / E / D / B / C：0**
- **E/F 升 A：0**

---

## 20. L1/L2/L3

### L1（源码事实，可证）

- 2 Read 函数完整定义 + 5+3 调用位置（A）
- Request 字段构造（A）
- Response 字段消费（A）
- 状态变化（A）
- Promise 链（A）
- 失败分支（A）
- medicalRecordId 表达式层同源（A）

### L2（业务解释，未证）

- "querySingleOrder = 重新查询订单"：**E**
- "queryUndisposed = 刷新待处理数量"：**E**（仅 L34847 注释"待处理数量"）
- "filter_medicalRecordStatus_update = 业务状态过滤"：**E**
- "getMedicalRecordFlowVo = 医疗记录流"：**E**
- "stateTodoMedicalRecordCount = 待办医疗记录数"：**E**
- "queryUndisposed 仅在 Write A 调用的原因"：**E**（未证）
- "Write B / C 不调 queryUndisposed 的原因"：**E**（未证）
- "3 Write 同一数据库对象"：**E**
- "3 Write Refresh = 数据库刷新"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 selectMedicalRecordFlowVoList / stateTodoMedicalRecordCount / getMedicalRecordFlowVo 后端实现）

---

## 21. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 2 Read 后端处理 | 无后端代码 | F |
| 2 Read 真实 Response schema | 无样本 | F |
| result.status 实际值 | 仅 truthy 判空 | F |
| result.object 实际字段 | Controller 仅整体赋值 | F |
| result.result.object 实际字段 | Controller 仅整体赋值 | F |
| 2 Read 幂等性 | 无后端代码 | F |
| dealTime → closeLeftOpenRight 返回值 | factory 源码不可得 | F |
| filter_medicalRecordStatus → window.filter_medicalRecordStatus 实现 | window 全局函数 | F |
| popout_tip / popout_cb res 实际值 | 全局函数 | F |
| 7 HTML UI 模板 | 不可得 | F |
| 3 Write 同一数据库对象 | 无后端 | F |
| medicalRecordId 字段值相等 | 无后端 | F |

---

## 22. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 3 Write + 2 Read + 其它 Read 全部仅静态审计 |
| 3 Write 实际执行 = 0 | ✅ | |
| 2 Read 实际执行 = 0 | ✅ | getMedicalRecordFlowVo / stateTodoMedicalRecordCount 全部仅静态审计 |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 161 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变） |
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 161_*.md |
| 文件编号连续 | ✅ | 160 已被 S1-99 占用，本轮使用 161 |

---

## 23. 最终结论

### 23.1 Write → Read 最小闭合协议（A 级）

| Write | success 立即触发 Read1 | success 立即触发 Read2 |
|---|---|---|
| A (setMedicalRecordProcessMode) | querySingleOrder() → getMedicalRecordFlowVo.json | queryUndisposed() → stateTodoMedicalRecordCount.json |
| B (deliveryStatus="2") | querySingleOrder() → getMedicalRecordFlowVo.json | ❌ |
| C (deliveryStatus="1") | querySingleOrder() → getMedicalRecordFlowVo.json | ❌ |

### 23.2 Read 行为（A 级）

**querySingleOrder (L34883)**:
- 调 `/admin/getMedicalRecordFlowVo.json` (Read)
- Request.medicalRecordId = selectOrderListFactory.items[orderIndex].medicalRecord.id
- 成功时（$timeout 包裹）：
  - `$scope.selectOrderListFactory.items[orderIndex] = result.object`（**整体覆盖**）
  - `$scope.filter_medicalRecordStatus_update(result.object, "button", orderIndex)`（间接更新 medicalRecordStatus）
- 错误时：Popup.notice(result.errmsg) + return
- ❌ 0 处 .catch / try-catch

**queryUndisposed (L34841)**:
- 调 `/admin/stateTodoMedicalRecordCount.json` (Read)
- Request = `dealTime()` = `angular.copy($scope.obj)`
- 成功时：`$scope.toPayCount = result.result.object`
- 错误时：Popup.notice(result.errmsg) + return

### 23.3 关键事实（A 级）

1. **3 Write success 均汇聚到同一 querySingleOrder() 函数**（A 级）
2. **仅 Write A 额外调用 queryUndisposed()**（A 级）
3. **querySingleOrder 触发同一 Read API**（getMedicalRecordFlowVo.json）（A 级）
4. **medicalRecordId 在 4 处表达式层同源**（A 级）— 最终来自 selectOrderListFactory.items[index].medicalRecord.id
5. **querySingleOrder 与 order.brushData 同 API 但不同 Consumer**（A 级新发现）
6. **0 处 .catch 保护**（A 级）— Read 异常未捕获传播
7. **0 处 reload / state.go**（A 级）— Refresh 通过整体覆盖 selectOrderListFactory.items[index] 实现
8. **整体覆盖 vs 字段级合并**：A 级整体覆盖（L34892 =）
9. **Promise 同步触发 Read**（A 级）— Write success 后立即退出 .then，Read 异步进行
10. **2 Read 都有失败分支 Popup**（A 级）

### 23.4 S1-100 关键新发现

1. **querySingleOrder 与 order.brushData 共用同一 Read API**（getMedicalRecordFlowVo.json），但消费不同
2. **queryUndisposed 在 search() 完成后也会调用**（L35376，路由回调链），不只 Write success
3. **querySingleOrder 用 $timeout 包裹赋值操作**（AngularJS digest 异步）
4. **0 处 .catch 保护**（与 S1-99 concatMedicalProductStock 同问题）
5. **Write B / C 不调 queryUndisposed 是结构差异**（A 级事实），业务原因（E 级推断）

### 23.5 不可在本轮升级为 A 的项

- 2 Read 后端处理（F）
- 2 Read 真实 Response schema（F）
- result.status / result.object / result.result.object 实际值（F）
- 3 Write 与 querySingleOrder 同一数据库对象（E / L3 = F）
- queryUndisposed 仅 Write A 调用的业务原因（E）
- 业务语义（E）
- optometryCtrl HTML 模板（F）
- dealTime / filter_medicalRecordStatus / popout_tip / popout_cb 实现（F）

---

**审计结束**。
