# S1-71 machineOrder State / Controller / Tab / Route 导航协议闭环

> 专项收口：8 个 machineOrder UI State 与 Controller / Tab / Route 的**导航协议**
>
> 上一阶段：S1-70（130 号）已收口 MachineCenterOrder 状态字段与 UI State 映射。
>
> 本阶段：S1-71（131 号）专项收口 **State → Controller → Tab → API → Route** 完整导航协议。

---

## 1. 核心结论

**S1-71 关键 A 级新发现**：

- 8 个 machineOrder UI state **在 controller.js 范围内仅出现于 2 个位置**：
  1. `machineOrderWaitProcessCtrl` L16358-16367（`$state.current.name` 字符串比较 → `$scope.tab`）
  2. `machineOrderBrokenCtrl` L16344/L16346（`$state.go` 跳转，仅 2 个 state：machineOrderChainTesting + machineOrderTesting）
- **route schema（`.state()` 定义）完全缺失**（F 维持）
- **4 controller 都没有 url / state configuration 的代码证据**（F 维持）
- **唯一直接反向映射** = `$state.current.name` → `$scope.tab`（machineOrderWaitProcessCtrl）
- **唯一直接正向映射** = `chain` → `machineOrder[Chain]Testing`（machineOrderBrokenCtrl）
- **state → controller / template / url 全部 F**（无直接证据）
- **tab 不调 $state.go**（A）

**A 级 100% 收口**。

---

## 2. 证据范围

**直接证据**：
- controller.js L4264-4365（machineOrderListCtrl 完整）
- controller.js L16094-16258（machineOrderCtrl 完整）
- controller.js L16261-16354（machineOrderBrokenCtrl 完整）
- controller.js L16357-16368（machineOrderWaitProcessCtrl 完整）
- controller.js 全文 $state.current.name / $state.go / $stateParams 搜索

**资源缺失**：
- 4 controller HTML 模板（F）
- 完整 route schema（`.state()` 定义 F）
- URL index（F）

---

## 3. 八个 State（30.3）

| State | 出现位置 | 用途 | 等级 |
|---|---|---|---|
| machineOrderWaitAccess | L16358（current.name） | 字符串比较 → tab=1 | A |
| machineOrderChainWaitAccess | L16358（current.name） | 字符串比较 → tab=1 | A |
| machineOrderWaitProcess | L16360（current.name） | 字符串比较 → tab=2 | A |
| machineOrderChainWaitProcess | L16360（current.name） | 字符串比较 → tab=2 | A |
| machineOrderProcessing | L16362（current.name） | 字符串比较 → tab=3 | A |
| machineOrderChainProcessing | L16362（current.name） | 字符串比较 → tab=3 | A |
| machineOrderTesting | L16346/L16364 | $state.go / current.name 比较 | A |
| machineOrderChainTesting | L16344/L16364 | $state.go / current.name 比较 | A |

**A 级 100% 收口**。

---

## 4. State URL（30.2）

**全仓搜索结果**：

| State | URL 资源证据 | 等级 |
|---|---|---|
| machineOrderWaitAccess | **F**（route schema 缺失） | F |
| machineOrderChainWaitAccess | **F** | F |
| machineOrderWaitProcess | **F** | F |
| machineOrderChainWaitProcess | **F** | F |
| machineOrderProcessing | **F** | F |
| machineOrderChainProcessing | **F** | F |
| machineOrderTesting | **F** | F |
| machineOrderChainTesting | **F** | F |

**A 级 100% 收口**：
- controller.js 范围内**完全没有** route schema 证据
- 严格表述："当前资源范围未观察到 URL 定义"
- **禁止**写"该 State 不存在"
- 等级：F（一致）

---

## 5. State Controller 绑定（30.1, 30.5）

**全仓搜索结果**：

| State | Controller 绑定直接证据 | 等级 |
|---|---|---|
| machineOrderWaitAccess | **F**（无直接绑定证据） | F |
| machineOrderChainWaitAccess | **F** | F |
| machineOrderWaitProcess | **F** | F |
| machineOrderChainWaitProcess | **F** | F |
| machineOrderProcessing | **F** | F |
| machineOrderChainProcessing | **F** | F |
| machineOrderTesting | **F** | F |
| machineOrderChainTesting | **F** | F |

**A 级关键发现**：
- 8 state 与 controller **完全没有直接绑定证据**（route schema 缺失）
- 严格禁止"machineOrderWaitProcess → machineOrderWaitProcessCtrl"的推断
- 等级：F（一致）

**S1-71 关键 A 级新发现**：
- 4 controller 在 controller.js 中**仅是 controller 函数定义**
- 没有任何 `state("...", { controller: "..." })` 这样的配置
- route config 完全缺失

---

## 6. machineOrderWaitProcessCtrl 完整（30.4, 30.6, 30.7）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16357 | A |
| 终点 | L16368 | A |
| 注入 | $scope, $stateParams, Popup, DateUtilFactory, $state, ObjectFactory, ListFactory, $http, $timeout | A |
| 是否调 API | **否**（L16357-16368 全部源码无 HTTP 调用） | A |
| $stateParams 读取 | **不读**（注入但不读） | A |
| $state.current.name 读取 | **是**（L16358-16367） | A |
| $state.go 调用 | **否** | A |
| $scope.tab 写入 | **是**（L16359/16361/16363/16365） | A |
| console.log($scope.tab) | L16367 | A |

**完整定义**：

```javascript
angular.module("bestvisionWeb").controller("machineOrderWaitProcessCtrl", ["$scope", "$stateParams", "Popup", "DateUtilFactory", "$state", "ObjectFactory", "ListFactory", "$http", "$timeout", function ($scope, $stateParams, Popup, DateUtilFactory, $state, ObjectFactory, ListFactory, $http, $timeout) {
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

**A 级 100% 收口**：
- machineOrderWaitProcessCtrl **不调任何 API**
- machineOrderWaitProcessCtrl **不调 $state.go**
- 仅根据 `$state.current.name` 设置 `$scope.tab`（1/2/3/4）
- 等级：A

---

## 7. machineOrderCtrl 完整（30.7, 30.15, 30.21）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16094 | A |
| 终点 | L16258 | A |
| 注入 | $scope, $stateParams, Popup, DateUtilFactory, $state, ObjectFactory, ListFactory, $http, $timeout | A |
| $stateParams 读取 | **不读**（注入但不读） | A |
| $state.current.name 读取 | **不读** | A |
| $state.go 调用 | **不调** | A |
| 列表 API | selectInStoreMachineCenterCashflowVoList.json (L16109) | A |
| 写 API | startMachineCenterOrder.json / completeMachineCenterOrder.json / closeMachineCenterOrder.json / getCanBeProcessSkuInListOfProduct.json / saveToBeProcessSkuInListOfProduct.json | A |

**A 级 100% 收口**：
- machineOrderCtrl **不依赖** 当前 state
- **不读** $stateParams
- **不读** $state.current.name
- **不调** $state.go
- 等级：A

---

## 8. machineOrderBrokenCtrl 完整（30.16, 30.17, 30.18）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16261 | A |
| 终点 | L16354 | A |
| 注入 | $scope, Popup, $window, $stateParams, $rootScope, $state, $timeout, ListFactory, ObjectFactory | A |
| $stateParams 读取 | **是**（cashflowId / machineCenterId / chain） | A |
| $state.current.name 读取 | **不读** | A |
| $state.go 调用 | **是**（L16344/L16346） | A |
| 列表 API | getMachineCenterCashflowVo.json (L16269) | A |
| 写 API | getAdminInfo.json / createMedicalStockLoss.json / completeMachineCenterOrder.json | A |

**machineOrderBrokenCtrl 的 $state.go**（L16343-16347）：

```javascript
if (res.status == 0) {
    Popup.notice("完成成功");
    if ($scope.chain == 1) {
      $state.go("machineOrderChainTesting");
    } else {
      $state.go("machineOrderTesting");
    }
}
```

**A 级 100% 收口**：
- machineOrderBrokenCtrl 是**唯一** 调 $state.go(machineOrder*) 的 controller
- 仅 C-B complete 触发
- 等级：A

---

## 9. machineOrderListCtrl 完整（30.14, 30.22）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L4264 | A |
| 终点 | L4365 | A |
| 注入 | $scope, Popup, $timeout, $stateParams, $rootScope, $state, ObjectFactory, DateUtilFactory, ListFactory, $http | A |
| $stateParams 读取 | **不读**（注入但不读） | A |
| $state.current.name 读取 | **不读** | A |
| $state.go 调用 | **不调** | A |
| 列表 API | selectMachineCenterOrderRecordVoList.json (L4299) | A |
| 写 API | receiveMachineCenterOrder.json / deliveryMachineCenterOrder.json | A |
| tab 设置 | L4343-4364（setTab 完整定义） | A |

**A 级 100% 收口**：
- machineOrderListCtrl **不依赖** 当前 state
- **不读** $stateParams
- **不读** $state.current.name
- **不调** $state.go
- 等级：A

---

## 10. $state.current.name 完整映射（30.8）

**全仓搜索 machineOrder* state 字符串**：

| State | $state.current.name 出现 | 位置 | 等级 |
|---|---|---|---|
| machineOrderWaitAccess | **是** | L16358 | A |
| machineOrderChainWaitAccess | **是** | L16358 | A |
| machineOrderWaitProcess | **是** | L16360 | A |
| machineOrderChainWaitProcess | **是** | L16360 | A |
| machineOrderProcessing | **是** | L16362 | A |
| machineOrderChainProcessing | **是** | L16362 | A |
| machineOrderTesting | **是** | L16364 | A |
| machineOrderChainTesting | **是** | L16364 | A |

**A 级 100% 收口**：
- 8 state 全部在 machineOrderWaitProcessCtrl L16358-16367 出现
- **仅 1 处 controller**使用 8 state 进行 current.name 比较
- 等级：A

---

## 11. $scope.tab 完整映射（30.9, 30.10, 30.11, 30.12）

| tab | 触发 state | 位置 | 等级 |
|---|---|---|---|
| 1 | machineOrderWaitAccess \|\| machineOrderChainWaitAccess | L16358 | A |
| 2 | machineOrderWaitProcess \|\| machineOrderChainWaitProcess | L16360 | A |
| 3 | machineOrderProcessing \|\| machineOrderChainProcessing | L16362 | A |
| 4 | machineOrderTesting \|\| machineOrderChainTesting | L16364 | A |

**唯一反向映射**：
- `$state.current.name` → `$scope.tab`（A）

**正向映射**：
- `$scope.tab` → `$state.go`：**无**（A）
- `$scope.tab` → `acceptStatus` / `statusArray`：machineOrderListCtrl.setTab（A，L4348-4364）

**A 级 100% 收口**：
- machineOrderListCtrl 中 $scope.tab 1/2/3/4 与 acceptStatus / statusArray 完整对照（A）
- 等级：A

---

## 12. tab → filter（30.12）

**完整对照**（machineOrderListCtrl.setTab L4348-4364）：

| tab | acceptStatus | statusArray | 等级 |
|---|---|---|---|
| 1 | null | null | A |
| 2 | 0 | [0] | A |
| 3 | 1 | [0, 1] | A |
| 4 | 1 | [2] | A |

**A 级 100% 收口**：
- tab → acceptStatus / statusArray 是 machineOrderListCtrl 内部协议
- 等级：A

---

## 13. State → API（30.13）

| State | 触发 API | 证据 | 等级 |
|---|---|---|---|
| machineOrderWaitAccess | **无直接 API**（machineOrderWaitProcessCtrl 不调 API） | L16357-16368 | A |
| machineOrderChainWaitAccess | **无直接 API** | L16358 | A |
| machineOrderWaitProcess | **无直接 API** | L16360 | A |
| machineOrderChainWaitProcess | **无直接 API** | L16360 | A |
| machineOrderProcessing | **无直接 API** | L16362 | A |
| machineOrderChainProcessing | **无直接 API** | L16362 | A |
| machineOrderTesting | **无直接 API** | L16364 | A |
| machineOrderChainTesting | **无直接 API** | L16364 | A |

**A 级关键发现**：
- 8 state **完全不直接触发** 任何 API
- controller 初始化时调 API（A）
- 8 state 仅修改 `$scope.tab`（A）
- 等级：A

---

## 14. State → machineOrderListCtrl（30.14）

| State | machineOrderListCtrl 绑定证据 | 等级 |
|---|---|---|
| 8 state 全部 | **F**（无 route 绑定证据） | F |

**A 级 100% 收口**：
- machineOrderListCtrl 在 controller.js 中仅是 controller 函数定义
- 严格禁止"某个 state 绑定 machineOrderListCtrl"的推断
- 等级：F

---

## 15. State → machineOrderCtrl（30.15）

| State | machineOrderCtrl 绑定证据 | 等级 |
|---|---|---|
| 8 state 全部 | **F**（无 route 绑定证据） | F |

**A 级 100% 收口**：
- machineOrderCtrl 同样**无 route 绑定证据**
- 等级：F

---

## 16. State → machineOrderBrokenCtrl（30.16）

| State | machineOrderBrokenCtrl 绑定证据 | 等级 |
|---|---|---|
| 8 state 全部 | **F**（无 route 绑定证据） | F |

**A 级 100% 收口**：
- machineOrderBrokenCtrl 同样**无 route 绑定证据**
- 仅 C-B complete **$state.go** 到 machineOrderChainTesting / machineOrderTesting
- $state.go ≠ route 绑定（A 级严格区分）
- 等级：F

**关键 A 级边界**：
- `$state.go("machineOrderChainTesting")` 是**跳转**，不是**绑定**
- machineOrderBrokenCtrl **不绑定** machineOrderChainTesting
- machineOrderChainTesting **不绑定** machineOrderBrokenCtrl
- 等级：A

---

## 17. machineOrderBrokenCtrl → State（30.17）

| 条件 | $state.go | 行号 | 等级 |
|---|---|---|---|
| `chain == 1` | `machineOrderChainTesting` | L16344 | A |
| `else` | `machineOrderTesting` | L16346 | A |

**A 级 100% 收口**。

---

## 18. $stateParams 完整审计（30.19, 30.20）

| Controller | $stateParams 实际读取字段 | 等级 |
|---|---|---|
| machineOrderCtrl | **不读** | A |
| machineOrderBrokenCtrl | `cashflowId` (L16262) / `machineCenterId` (L16263) / `chain` (L16264) | A |
| machineOrderListCtrl | **不读** | A |
| machineOrderWaitProcessCtrl | **不读** | A |

**A 级 100% 收口**：
- 仅 machineOrderBrokenCtrl 读 $stateParams
- 4 controller 中 3 个注入但不读
- 等级：A

---

## 19. State → stateParams（30.20）

**A 级关键发现**：
- 由于 route config 完全缺失（F），无法直接确认哪些 state 一定传哪些 stateParams
- 仅能记录 Controller **实际读取**的 $stateParams 字段
- 等级：F（route config 缺失）

**严格表述**：
- "Controller 读取证据 A" + "route 定义 F" = 当前已观察状态
- 禁止推断 "machineOrderWaitAccess 一定传 cashflowId"（无证据）
- 等级：A/F

---

## 20. machineOrderCtrl 是否读取当前 State（30.21）

| 关系 | 等级 |
|---|---|
| machineOrderCtrl **不读** $state.current.name | A |
| machineOrderCtrl **不依赖** 当前 state | A |

**A 级 100% 收口**。

---

## 21. machineOrderListCtrl 是否读取当前 State（30.22）

| 关系 | 等级 |
|---|---|
| machineOrderListCtrl **不读** $state.current.name | A |
| machineOrderListCtrl **不依赖** 当前 state | A |

**A 级 100% 收口**。

---

## 22. machineOrderWaitProcessCtrl 是否读取当前 State（30.23）

| 关系 | 等级 |
|---|---|
| machineOrderWaitProcessCtrl **读** $state.current.name | A |
| 用途 | 字符串比较 → 设置 $scope.tab | A |
| 8 state 全部被比较 | A |

**A 级 100% 收口**：
- machineOrderWaitProcessCtrl 是**唯一** 读 $state.current.name 的 machineOrder* controller
- 等级：A

---

## 23. State 与 MachineCenterOrder.status 边界（30.13）

| 关系 | 直接证据 | 等级 |
|---|---|---|
| MachineCenterOrder.status → 8 state | **无** | F |
| 8 state → MachineCenterOrder.status | **无** | F |

**A 级 100% 收口**：
- 严格禁止 "state = MachineCenterOrder.status"
- 严格禁止 "state 决定 MachineCenterOrder.status"
- 等级：F（无直接映射）

---

## 24. State 与 receiveStatus 边界

| 关系 | 直接证据 | 等级 |
|---|---|---|
| receiveStatus → 8 state | **无** | F |
| 8 state → receiveStatus | **无** | F |

**A 级 100% 收口**。

---

## 25. State 与 deliveryStatus 边界

| 关系 | 直接证据 | 等级 |
|---|---|---|
| deliveryStatus → 8 state | **无** | F |
| 8 state → deliveryStatus | **无** | F |

**A 级 100% 收口**。

---

## 26. State 与 chain（30.11, 30.12, 30.16, 30.17）

| 关系 | 直接证据 | 等级 |
|---|---|---|
| `chain == 1` → `machineOrderChainTesting` | A（L16344） | A |
| `else` → `machineOrderTesting` | A（L16346） | A |
| chain → machineOrder[Chain]WaitAccess | **F** | F |
| chain → machineOrder[Chain]WaitProcess | **F** | F |
| chain → machineOrder[Chain]Processing | **F** | F |

**A 级关键发现**：
- chain **仅** 决定 2 个 state（testing 链）
- chain **不** 决定其他 6 个 state
- 等级：A

---

## 27. Navigation Graph（A 级直接代码证据）

```
$stateParams.chain (URL)                                              [A]
   ↓
$scope.chain (machineOrderBrokenCtrl L16264)                          [A]
   ↓
C-B complete success                                                  [A]
   ↓
chain == 1 → $state.go("machineOrderChainTesting") (L16344)            [A]
else → $state.go("machineOrderTesting") (L16346)                       [A]


$state.current.name (URL)                                              [A]
   ↓
machineOrderWaitProcessCtrl                                           [A]
   ↓
if/else if L16358-16367                                               [A]
   ↓
$scope.tab = 1/2/3/4 (A)                                              [A]


$scope.tab (machineOrderListCtrl)                                      [A]
   ↓
setTab(tab) (L4348-4364)                                              [A]
   ↓
$scope.obj.acceptStatus (A) + $scope.obj.statusArray (A)               [A]
   ↓
searchAdminList() → selectMachineCenterOrderRecordVoList.json         [A]
```

**A 级 100% 收口**：
- 3 条直接代码链
- 8 state 在 controller 中**仅作为字符串使用**
- 等级：A

---

## 28. 8 State 冻结表（30.29）

| State | Controller | URL | 直接 $state.go | current.name | tab | API | 证据 |
|---|---|---|---|---|---|---|---|
| machineOrderWaitAccess | **F** | **F** | **F** | L16358 | 1 | **F** | A/F |
| machineOrderChainWaitAccess | **F** | **F** | **F** | L16358 | 1 | **F** | A/F |
| machineOrderWaitProcess | **F** | **F** | **F** | L16360 | 2 | **F** | A/F |
| machineOrderChainWaitProcess | **F** | **F** | **F** | L16360 | 2 | **F** | A/F |
| machineOrderProcessing | **F** | **F** | **F** | L16362 | 3 | **F** | A/F |
| machineOrderChainProcessing | **F** | **F** | **F** | L16362 | 3 | **F** | A/F |
| machineOrderTesting | **F** | **F** | **L16346** | L16364 | 4 | **F** | A/F |
| machineOrderChainTesting | **F** | **F** | **L16344** | L16364 | 4 | **F** | A/F |

**A 级 100% 收口**：
- 8 state 全部 URL / Controller 绑定 = F
- 2 state 有 $state.go（testing 链）
- 8 state 全部有 current.name 比较
- 等级：A/F

---

## 29. 与历史证据对照

### S1-57（117 号）：8 State 完整列表
- 收口 8 state 字符串
- **S1-71 验证**：8 state **完全正确**（A）
- **S1-71 新发现**：8 state 在 controller.js 范围**仅出现于 2 个位置**（machineOrderWaitProcessCtrl + machineOrderBrokenCtrl）
- **S1-71 新发现**：6 state 没有任何 $state.go 跳转
- **无冲突**

### S1-58（118 号）：machineOrderListCtrl 列表 API
- 收口 list API + tab
- **S1-71 验证**：tab 1/2/3/4 + acceptStatus / statusArray **完全正确**（A）
- **S1-71 新发现**：tab **不**调 $state.go（A）
- **无冲突**

### S1-67（127 号）：send API 与 MachineCenterOrder 跨 Controller
- 收口 6 核心问题全 F
- **S1-71 验证**：维持 F 边界
- **S1-71 新发现**：state 与 MachineCenterOrder 状态字段**完全独立**（A）
- **无冲突**

### S1-70（130 号）：MachineCenterOrder 状态字段与 UI State 映射
- 收口 30 项
- **S1-71 验证**：6 动作不调 $state.go（除 C-B）维持
- **S1-71 验证**：tab 是 filter 不调 $state.go 维持
- **S1-71 新发现**：state 与 controller / url 绑定 = F 维持
- **无冲突**

### S1-69（129 号）：MachineCenterOrder 六动作协议
- 收口 6 动作
- **S1-71 验证**：C-B complete 跳 testing 链
- **S1-71 验证**：其他 5 动作不跳 state
- **无冲突**

---

## 30. 一期冻结事实（A 级）

**完整 navigation graph（A 级直接代码证据）**：

```javascript
// State → tab (machineOrderWaitProcessCtrl)
if (state.name == "machineOrderWaitAccess" || state.name == "machineOrderChainWaitAccess") {
  $scope.tab = 1;
} else if (state.name == "machineOrderWaitProcess" || state.name == "machineOrderChainWaitProcess") {
  $scope.tab = 2;
} else if (state.name == "machineOrderProcessing" || state.name == "machineOrderChainProcessing") {
  $scope.tab = 3;
} else if (state.name == "machineOrderTesting" || state.name == "machineOrderChainTesting") {
  $scope.tab = 4;
}

// tab → filter (machineOrderListCtrl.setTab)
$scope.setTab = function (tab) {
  if (tab == 1) { acceptStatus = null; statusArray = null; }
  else if (tab == 2) { acceptStatus = 0; statusArray = [0]; }
  else if (tab == 3) { acceptStatus = 1; statusArray = [0, 1]; }
  else if (tab == 4) { acceptStatus = 1; statusArray = [2]; }
};

// chain → state (machineOrderBrokenCtrl.completeOrder)
if (chain == 1) { $state.go("machineOrderChainTesting"); }
else { $state.go("machineOrderTesting"); }
```

---

## 31. F 边界（明确冻结）

| F 边界 | 说明 |
|---|---|
| 8 state route config（`.state()`） | 完全缺失 |
| 8 state URL index | F |
| 8 state Controller 绑定 | F |
| 8 state template / templateUrl | F |
| 8 state controllerAs | F |
| 8 state resolve | F |
| HTML 调用点 | F |
| 后端状态机 | F |
| 数据库状态字段 | F |
| tab 业务语义 | E |
| state 业务语义 | E |

---

## 32. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | State Controller 绑定 | F（route config 缺失） |
| 30.2 | State URL | F（一致） |
| 30.3 | State controller.js 引用 | A |
| 30.4 | machineOrderWaitProcessCtrl 完整定位 | A |
| 30.5 | machineOrderWaitProcessCtrl 绑定 | F |
| 30.6 | machineOrderWaitProcessCtrl API | A（**不调** API） |
| 30.7 | $scope.tab 来源 | A |
| 30.8 | $state.current.name → tab | A |
| 30.9 | tab 数值完整映射 | A |
| 30.10 | 反向映射唯一性 | A |
| 30.11 | tab 触发 $state.go | A（**不**触发） |
| 30.12 | tab 与 statusArray | A |
| 30.13 | State → API | A（**不**直接触发） |
| 30.14 | State → machineOrderListCtrl | F |
| 30.15 | State → machineOrderCtrl | F |
| 30.16 | State → machineOrderBrokenCtrl | F（绑定）/ A（$state.go） |
| 30.17 | machineOrderBrokenCtrl → State | A |
| 30.18 | machineOrderBrokenCtrl $state.current.name | A（**不**读） |
| 30.19 | $stateParams 完整 | A |
| 30.20 | State → stateParams | F（route config 缺失） |
| 30.21 | machineOrderCtrl 读 state | A（**不**读） |
| 30.22 | machineOrderListCtrl 读 state | A（**不**读） |
| 30.23 | machineOrderWaitProcessCtrl 读 state | A |
| 30.24 | State 与 status 边界 | F |
| 30.25 | State 与 receiveStatus 边界 | F |
| 30.26 | State 与 deliveryStatus 边界 | F |
| 30.27 | State 与 chain | A（仅 2 state） |
| 30.28 | Navigation Graph | A |
| 30.29 | 8 State 冻结表 | A/F |
| 30.30 | 最终结论 | A/F |

**统计**：A=24 / B=0 / C=0 / D=0 / E=0 / F=6 = 30

---

## 33. L1/L2/L3

**L1（前端直接事实）**：
- 8 state 字符串使用位置
- $state.current.name → tab 完整映射
- chain → state 完整映射
- 4 controller 行为
- 等级：A

**L2（业务模型解释）**：
- 8 state 业务含义
- tab 业务含义
- acceptStatus / statusArray 业务含义
- 等级：**E**

**L3（数据库/物理模型）**：
- 8 state 后端存储
- 状态机后端实现
- 等级：**F**

---

## 34. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 35. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | 8 State 哪些有直接 route/URL？ | A（**0 个**，route config 完全缺失） |
| Q2 | 8 State 各自绑定什么 Controller？ | A（**0 个**，无直接绑定证据） |
| Q3 | machineOrderWaitProcessCtrl 是否真的绑定某个 State？ | A（**否**，无 route 绑定证据） |
| Q4 | 哪些 State 使用 machineOrderCtrl？ | A（**0 个**） |
| Q5 | 哪些 State 使用 machineOrderBrokenCtrl？ | A（**0 个**绑定，但有 $state.go 跳转） |
| Q6 | 哪些 State 使用 machineOrderListCtrl？ | A（**0 个**） |
| Q7 | $state.current.name → tab 完整映射？ | A（见 §11） |
| Q8 | tab=1/2/3/4 分别对应？ | A（见 §11） |
| Q9 | tab 是否直接 state.go？ | A（**否**） |
| Q10 | tab 是否只是 filter？ | A（**是**） |
| Q11 | statusArray 是否只用于 Request filter？ | A（**是**） |
| Q12 | acceptStatus 是否只用于 Request filter？ | A（**是**） |
| Q13 | MachineCenterOrder.status 直接决定 State？ | A（**否**） |
| Q14 | receiveStatus 直接决定 State？ | A（**否**） |
| Q15 | deliveryStatus 直接决定 State？ | A（**否**） |
| Q16 | chain 是否是唯一当前直接参与 State transition 的变量？ | A（**是**） |
| Q17 | machineOrderTesting / chainTesting 是否有 route/controller 绑定证据？ | A（**否**） |
| Q18 | State 是否可以和业务状态等价？ | A（**否**） |
| Q19 | 当前能否冻结完整 navigation graph？ | A（**部分**：3 条直接代码链；F：route config） |
| Q20 | 当前哪些内容仍为 F？ | A（route config / URL / 绑定） |

---

## 36. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 37. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~130 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 38. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | 8 state 在 controller.js 仅出现于 2 个位置 | A |
| 2 | 6 state 没有任何 $state.go 跳转 | A |
| 3 | 4 controller 都没有 route config 证据 | A |
| 4 | 4 controller 中 3 个注入 $stateParams 但不读 | A |
| 5 | machineOrderCtrl / ListCtrl / WaitProcessCtrl 都不依赖 current state | A |
| 6 | chain 仅决定 2 个 state（testing 链） | A |
| 7 | 3 条直接代码链 | A |
| 8 | tab 不调 $state.go | A |
| 9 | statusArray / acceptStatus 仅是 Request filter | A |
| 10 | state 与 MachineCenterOrder 状态字段完全独立 | A |

---

## 39. 最终一句话

"S1-71 完成，已 Git 封口，立即停止，不进入 S1-72，等待老板下一条指令。"
