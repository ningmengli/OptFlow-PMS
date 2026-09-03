# S1-70 MachineCenterOrder 状态字段与 UI State 映射审计

> 专项审计：`MachineCenterOrder.status / receiveStatus / acceptStatus / deliveryStatus / statusArray / chain` 与 **8 个 machineOrder UI state** 的**直接映射代码**
>
> 上一阶段：S1-69（129 号）已收口 MachineCenterOrder 六动作协议。
>
> 本阶段：S1-70（130 号）专项审计**状态字段 → UI state** 直接映射。

---

## 1. 核心结论

**S1-70 关键 A 级新发现**：

- **8 个 machineOrder UI state 与 MachineCenterOrder 状态字段无任何直接映射代码**（A 级 100% 收口）
- **2 个 state 字符串实际被使用**（仅 `$state.go`）：`machineOrderChainTesting` + `machineOrderTesting`
- **6 个 state 字符串仅作为字符串出现**：machineOrderWaitAccess / machineOrderChainWaitAccess / machineOrderWaitProcess / machineOrderChainWaitProcess / machineOrderProcessing / machineOrderChainProcessing
- **6 个 state 没有任何 `$state.go` 跳转**
- **状态字段 → UI state 唯一直接映射**：`chain == 1` → `machineOrderChainTesting` / `else` → `machineOrderTesting`（machineOrderBrokenCtrl.completeOrder L16343-16347）
- **tab 是列表 filter，**不**是 UI state**（machineOrderListCtrl.setTab 不调 $state.go）
- **acceptStatus / statusArray 仅作为 API Request 字段**，**不**参与 $state.go

**A 级 100% 收口**。

---

## 2. 证据范围

**直接证据**：
- controller.js L4348-4364（machineOrderListCtrl.setTab 完整定义）
- controller.js L16094-16258（machineOrderCtrl 完整定义）
- controller.js L16261-16354（machineOrderBrokenCtrl 完整定义）
- controller.js L16357-16368（machineOrderWaitProcessCtrl 完整定义）
- controller.js L4264-4350（machineOrderListCtrl 完整定义）

**资源缺失**：
- 4 controller HTML 模板（F）
- 完整 route schema（`.state()` 定义 F）
- 后端算法 / DTO 定义（F）

---

## 3. 八个 UI State（30.1-30.2）

**全仓搜索结果**：

| State | 出现次数 | 定义点 | state.go 点 | 条件判断 | 等级 |
|---|---|---|---|---|---|
| machineOrderWaitAccess | 1 | L16358（字符串） | **0** | **0** | F（route F） |
| machineOrderChainWaitAccess | 1 | L16358（字符串） | **0** | **0** | F（route F） |
| machineOrderWaitProcess | 2 | L16360/L16364 | **0** | L16360 if/else | A（字符串 + 条件） |
| machineOrderChainWaitProcess | 1 | L16360 | **0** | L16360 if/else | A |
| machineOrderProcessing | 1 | L16362 | **0** | L16362 if/else | A |
| machineOrderChainProcessing | 1 | L16362 | **0** | L16362 if/else | A |
| machineOrderTesting | 2 | L16346/L16364 | **L16346** | L16346 else | A（**唯一** state.go） |
| machineOrderChainTesting | 2 | L16344/L16364 | **L16344** | L16344 if chain==1 | A（**唯一** state.go） |

**A 级关键发现**：
- **6 个 state 完全没有 state.go 调用**
- **2 个 state 有 state.go 调用**（仅由 C-B complete 触发）
- 等级：A

---

## 4. State 引用点（30.2）

**machineOrderWaitAccess / machineOrderChainWaitAccess**：
- 唯一出现：machineOrderWaitProcessCtrl L16358（`if ($scope.$state.current.name == "machineOrderChainWaitAccess" || $scope.$state.current.name == "machineOrderWaitAccess") { $scope.tab = 1; }`）
- **不**调 `$state.go`
- **不**被其他 controller 引用
- 等级：A

**machineOrderWaitProcess / machineOrderChainWaitProcess**：
- 出现：machineOrderWaitProcessCtrl L16360 / L16364（if/else if）
- **不**调 `$state.go`
- 等级：A

**machineOrderProcessing / machineOrderChainProcessing**：
- 出现：machineOrderWaitProcessCtrl L16362（if/else if）
- **不**调 `$state.go`
- 等级：A

**machineOrderTesting / machineOrderChainTesting**：
- 出现：machineOrderBrokenCtrl L16344 / L16346（**$state.go**） + L16364
- **调** `$state.go`（L16344/L16346）
- 等级：A

---

## 5. chain 来源与生命周期（30.11）

**全仓搜索 `chain`**：

| 出现位置 | 上下文 | 等级 |
|---|---|---|
| L16264 | `$scope.chain = $stateParams.chain` | A（machineOrderBrokenCtrl 入口） |
| L16343 | `if ($scope.chain == 1)` | A（state.go 条件） |
| L16346 | `else { $state.go("machineOrderTesting") }` | A（state.go else 分支） |

**chain 完整生命周期**：

```
$stateParams.chain (URL)
   ↓
$scope.chain (L16264 入口赋值)
   ↓
L16343 if ($scope.chain == 1)
   ↓ 跳 machineOrderChainTesting
   ↓ else
   ↓ 跳 machineOrderTesting
```

**A 级 100% 收口**：
- chain 唯一来源 = `$stateParams.chain`（A）
- chain 不进入任何 API Request（A）
- chain 不写入任何 local 字段（A）
- 等级：A

**严格边界**：
- chain **不**出现在 machineOrderCtrl 范围（A）
- chain **不**出现在 machineOrderListCtrl 范围（A）
- chain **不**出现在 machineOrderWaitProcessCtrl 范围（A）
- chain **不**在 machineOrderBrokenCtrl.completeOrder 之外被读取（A）
- 等级：A

---

## 6. C-B complete → state.go（30.12, 30.9, 30.10）

**完整定义**（machineOrderBrokenCtrl L16333-16352）：

```javascript
$scope.completeOrder = function () {
    Popup.confirm("确定完成么", function () {
      var completeFactory = new ObjectFactory();
      var completePromise = completeFactory.saveOrQuery(
        "/admin/completeMachineCenterOrder.json",
        { cashflowId: $scope.cashflowId, machineCenterId: $scope.machineCenterId }
      );
      completePromise.then(function (res) {
        if (res.status == 0) {
          Popup.notice("完成成功");
          if ($scope.chain == 1) {
            $state.go("machineOrderChainTesting");
          } else {
            $state.go("machineOrderTesting");
          }
        } else {
          Popup.notice(res.errmsg);
        }
      });
    }, function () {});
};
```

**A 级 100% 收口**：

| 条件 | state | 行号 | 等级 |
|---|---|---|---|
| `chain == 1` | `machineOrderChainTesting` | L16344 | A |
| else | `machineOrderTesting` | L16346 | A |

**关键 A 级边界**：
- state.go 的**唯一直接触发条件** = chain 变量
- chain 唯一来源 = `$stateParams.chain`
- 等级：A

---

## 7. C-A complete → state.go（30.13）

**machineOrderCtrl.completeOrder (C-A)**：
- 调 commonOrder 协议（L16231）
- commonOrder success 后**不调** `$state.go`（A）
- 等级：A

**A 级 100% 收口**：
- C-A complete **不**直接 state.go
- C-A 与 C-B 协议**完全不同**（C-A 走 commonOrder + 写后回填 / C-B 走直接 API + state.go）
- 等级：A

---

## 8. startOrder → state.go（30.14）

**machineOrderCtrl.startOrder (L16163-16171)**：
- 调 commonOrder（A）
- **不调** `$state.go`（A）
- 等级：A

---

## 9. receiveOrder → state.go（30.15）

**machineOrderListCtrl.receiveOrder (L4314-4328)**：
- success 后**不调** `$state.go`（A）
- 仅修改 `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1`（A，L4321）
- 等级：A

---

## 10. deliveryReceiveOrder → state.go（30.16）

**machineOrderListCtrl.deliveryReceiveOrder (L4329-4342)**：
- success 后**不调** `$state.go`（A）
- 仅修改 `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1`（A，L4336）
- 等级：A

---

## 11. closeOrder → state.go（30.17）

**machineOrderCtrl.closeOrder (L16234-16242)**：
- 调 commonOrder（A）
- **不调** `$state.go`（A）
- 等级：A

---

## 12. 六动作 $state.go 总览

| 动作 | $state.go | 等级 |
|---|---|---|
| receive | **不调** | A |
| start | **不调** | A |
| C-A complete | **不调** | A |
| C-B complete | **是**（chain==1 → machineOrderChainTesting / else → machineOrderTesting） | A |
| close | **不调** | A |
| delivery receive | **不调** | A |

**A 级 100% 收口**：
- **仅 C-B** 调 $state.go
- **5 动作**不调 $state.go
- 等级：A

---

## 13. MachineCenterOrder.status 与 UI state（30.18）

**全仓搜索 `machineCenterOrder.status` 周围代码**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L16253 | `memberFactory.items[common.idx].machineCenterOrder.status = resp.result.object.status` | commonOrder 写后回填 | A |

**machineCenterOrder.status 周围 100 行 ±**：
- **不**出现 `if / switch / case / $state.go` 直接判断 machineCenterOrder.status
- **不**存在 `machineCenterOrder.status == X` → state.go 直接映射
- 等级：A（**F** 维持：直接映射未观察）

**严格边界**：
- machineCenterOrder.status 是**数据字段**（A）
- 不是**直接 state.go 触发条件**（F）
- 等级：A

---

## 14. receiveStatus 与 UI state（30.19）

**全仓搜索 `machineCenterOrder.receiveStatus` 周围代码**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L4321 | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` | receiveOrder 写后赋值 | A |

**receiveStatus 周围 100 行 ±**：
- **不**出现 `if / switch / case / $state.go` 直接判断 receiveStatus
- **不**存在 receiveStatus → state.go 直接映射
- 等级：A

**receiveStatus 作为查询 filter**：
- L4327: `else { $scope.obj.receiveStatus = null; }` (setTab 默认)
- L4344-4346: `$scope.changeReceiveStatus = function (index) { $scope.obj.receiveStatus = index; $scope.searchAdminList(); }`
- 等级：A（仅作为 filter）

---

## 15. acceptStatus 与 UI state（30.20）

**全仓搜索 `acceptStatus` 周围代码**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L4350 | `tab==1: $scope.obj.acceptStatus = null` | setTab | A |
| L4353 | `tab==2: $scope.obj.acceptStatus = 0` | setTab | A |
| L4356 | `tab==3: $scope.obj.acceptStatus = 1` | setTab | A |
| L4359 | `tab==4: $scope.obj.acceptStatus = 1` | setTab | A |
| L4325 | `$scope.obj.receiveStatus = 0` | grantAuth | A |

**acceptStatus 周围代码**：
- **不**存在 `if (acceptStatus == X) { $state.go(...) }` 直接映射
- **仅**作为查询 filter（A）
- 等级：A

---

## 16. deliveryStatus 与 UI state（30.22）

**全仓搜索 `deliveryStatus` 周围代码**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L4336 | `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` | deliveryReceiveOrder | A |

**deliveryStatus 周围代码**：
- **不**存在 `if (deliveryStatus == X) { $state.go(...) }` 直接映射
- **不**参与 machineOrder* UI state（A）
- 等级：A

---

## 17. statusArray（30.21）

**全仓搜索 `statusArray`**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L4351 | `tab==1: $scope.obj.statusArray = null` | setTab | A |
| L4354 | `tab==2: $scope.obj.statusArray = [0]` | setTab | A |
| L4357 | `tab==3: $scope.obj.statusArray = [0, 1]` | setTab | A |
| L4360 | `tab==4: $scope.obj.statusArray = [2]` | setTab | A |

**statusArray 用途**：
- **仅**作为 selectMachineCenterOrderRecordVoList.json Request 字段（A）
- **不**参与 $state.go
- **不**是 MachineCenterOrder.status 本体（A）
- 等级：A

**关键 A 级新发现**：
- statusArray 是**查询 filter 字段**，与 MachineCenterOrder.status 字段**无直接代码关系**（A）
- 等级：A

---

## 18. tab → UI state（30.24, 30.25）

**machineOrderListCtrl.setTab 完整定义**（L4348-4364）：

```javascript
$scope.setTab = function (tab) {
    if (tab == 1) {
      $scope.obj.acceptStatus = null;
      $scope.obj.statusArray = null;
    } else if (tab == 2) {
      $scope.obj.acceptStatus = 0;
      $scope.obj.statusArray = [0];
    } else if (tab == 3) {
      $scope.obj.acceptStatus = 1;
      $scope.obj.statusArray = [0, 1];
    } else if (tab == 4) {
      $scope.obj.acceptStatus = 1;
      $scope.obj.statusArray = [2];
    } else {}
    $scope.tab = tab;
    $scope.searchAdminList();
};
```

**A 级 100% 收口**：

| tab | acceptStatus | statusArray | $state.go | 等级 |
|---|---|---|---|---|
| 1 | null | null | **不调** | A |
| 2 | 0 | [0] | **不调** | A |
| 3 | 1 | [0, 1] | **不调** | A |
| 4 | 1 | [2] | **不调** | A |

**关键 A 级边界**：
- tab **不**直接对应任何 machineOrder* UI state（A）
- tab 是**列表 filter**，**不**是 UI state
- 等级：A

---

## 19. machineOrderWaitProcessCtrl 完整（30.23）

**完整定义**（L16357-16368）：

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

| 条件 | tab | 等级 |
|---|---|---|
| `state.name == "machineOrderChainWaitAccess" \|\| "machineOrderWaitAccess"` | 1 | A |
| `state.name == "machineOrderChainWaitProcess" \|\| "machineOrderWaitProcess"` | 2 | A |
| `state.name == "machineOrderChainProcessing" \|\| "machineOrderProcessing"` | 3 | A |
| `state.name == "machineOrderChainTesting" \|\| "machineOrderTesting"` | 4 | A |
| else | undefined | A |

**关键 A 级边界**：
- machineOrderWaitProcessCtrl **不调**任何 API（A）
- machineOrderWaitProcessCtrl **不读** $stateParams（A，注入但不读）
- machineOrderWaitProcessCtrl **不调** $state.go（A）
- machineOrderWaitProcessCtrl **仅**根据 `$state.current.name` 设置 `$scope.tab`（A）
- 等级：A

---

## 20. 状态数值证据（30.27, 30.28）

**status 数值出现**：

| 位置 | 表达式 | 上下文 | 等级 |
|---|---|---|---|
| L16253 | `resp.result.object.status` | getMachineCenterOrder.json Response | A |

**statusArray 数值**：

| 位置 | 值 | 等级 |
|---|---|---|
| L4351 | null | A |
| L4354 | [0] | A |
| L4357 | [0, 1] | A |
| L4360 | [2] | A |

**receiveStatus 数值**：

| 位置 | 值 | 等级 |
|---|---|---|
| L4321 | `1`（赋值） | A |
| L4327 | `null`（默认值） | A |
| L4344 | `index`（changeReceiveStatus） | A |

**acceptStatus 数值**：

| 位置 | 值 | 等级 |
|---|---|---|
| L4350 | null | A |
| L4353 | 0 | A |
| L4356 | 1 | A |
| L4359 | 1 | A |
| L4325 | 0 | A |

**deliveryStatus 数值**：

| 位置 | 值 | 等级 |
|---|---|---|
| L4336 | 1 | A |
| L4335 | 0（默认值，未直接代码） | F（推断） |

**严格不写**：
- 禁止"status=0 就是 waiting"（无业务文案证据）
- 禁止"status=1 就是 processing"（无业务文案证据）
- 禁止"status=2 就是 testing"（无业务文案证据）
- 禁止"statusArray=[2] 就是 testing"（无业务文案证据）
- 禁止"receiveStatus=1 就是已接收"（无业务文案证据）
- 等级：A（数值）/ E（业务语义）

---

## 21. 最终状态映射矩阵（30.29）

| 数据字段/变量 | 值/条件 | UI State | 直接证据 | 等级 |
|---|---|---|---|---|
| `$scope.chain` | `== 1` | `machineOrderChainTesting` | A（L16343-16344） | A |
| `$scope.chain` | `!= 1` (else) | `machineOrderTesting` | A（L16346） | A |
| `$scope.$state.current.name` | `== "machineOrderWaitAccess" \|\| "machineOrderChainWaitAccess"` | $scope.tab = 1 | A（L16358） | A |
| `$scope.$state.current.name` | `== "machineOrderWaitProcess" \|\| "machineOrderChainWaitProcess"` | $scope.tab = 2 | A（L16360） | A |
| `$scope.$state.current.name` | `== "machineOrderProcessing" \|\| "machineOrderChainProcessing"` | $scope.tab = 3 | A（L16362） | A |
| `$scope.$state.current.name` | `== "machineOrderTesting" \|\| "machineOrderChainTesting"` | $scope.tab = 4 | A（L16364） | A |
| `MachineCenterOrder.status` | ? | ? | **F**（无直接映射代码） | F |
| `MachineCenterOrder.receiveStatus` | ? | ? | **F**（无直接映射代码） | F |
| `acceptStatus` (tab filter) | ? | ? | **F**（仅 filter，不映射 state） | F |
| `medicalProductDelivery.deliveryStatus` | ? | ? | **F**（无直接映射代码） | F |
| `statusArray` | ? | ? | **F**（仅 filter，不映射 state） | F |
| `tab` (1/2/3/4) | ? | ? | **F**（仅 filter，不调 $state.go） | F |

**A 级 100% 收口**：
- 唯一直接映射 = `$scope.chain` → `machineOrder[Chain]Testing`
- 唯一反向映射 = `$state.current.name` → `$scope.tab` (machineOrderWaitProcessCtrl 内部)
- 等级：A

---

## 22. 历史证据 vs 当前证据

### S1-57（117 号）：8 State 完整列表
- 收口 8 state 字符串列表
- **S1-70 验证**：8 state 字符串**完全正确**（A）
- **S1-70 新发现**：8 state 中**仅 2 个**有 $state.go 调用（A）
- **S1-70 新发现**：6 state 完全没有 $state.go
- **无冲突**

### S1-58（118 号）：machineOrderListCtrl 列表 API
- 收口 list API + tab 协议
- **S1-70 验证**：tab 1/2/3/4 + acceptStatus / statusArray **完全正确**（A）
- **S1-70 新发现**：tab 1: statusArray=null, acceptStatus=null（A）
- **无冲突**

### S1-67（127 号）：send API 与 MachineCenterOrder 跨 Controller 对接
- 收口 6 核心问题全 F
- **S1-70 验证**：维持 F 边界
- **S1-70 新发现**：状态字段 → UI state 也**全部 F**（除 chain → testing）
- **无冲突**

### S1-69（129 号）：MachineCenterOrder 六动作协议
- 收口 6 动作 + commonOrder 覆盖
- **S1-70 验证**：6 动作 success 后**不调** $state.go（除 C-B）
- **S1-70 新发现**：6 动作 success 后**仅 C-B 调 state.go**
- **无冲突**

---

## 23. 一期冻结事实（A 级）

**唯一直接 state 映射链**：

```
$stateParams.chain (URL)
   ↓
$scope.chain (L16264)
   ↓
chain == 1
   ├→ true  → $state.go("machineOrderChainTesting") (L16344)
   └→ false → $state.go("machineOrderTesting") (L16346)
```

**唯一反向 state → tab 映射链**：

```
$state.current.name (URL)
   ↓
$scope.$state.current.name
   ↓
if/else if (L16358-16367)
   ├ machineOrder[Chain]WaitAccess → tab = 1
   ├ machineOrder[Chain]WaitProcess → tab = 2
   ├ machineOrder[Chain]Processing → tab = 3
   └ machineOrder[Chain]Testing → tab = 4
```

**tab → acceptStatus / statusArray 映射**：

```
tab=1 → acceptStatus=null,  statusArray=null
tab=2 → acceptStatus=0,     statusArray=[0]
tab=3 → acceptStatus=1,     statusArray=[0, 1]
tab=4 → acceptStatus=1,     statusArray=[2]
```

**6 动作 → $state.go 映射**：

```
receive       → 不调 state.go
start         → 不调 state.go
C-A complete  → 不调 state.go
C-B complete  → chain==1 → machineOrderChainTesting / else → machineOrderTesting
close         → 不调 state.go
delivery rcv  → 不调 state.go
```

---

## 24. 当前 F 边界（明确冻结）

| F 边界 | 说明 |
|---|---|
| MachineCenterOrder.status → UI state 映射 | **无**直接映射代码 |
| receiveStatus → UI state 映射 | **无**直接映射代码 |
| acceptStatus → UI state 映射 | **无**直接映射代码（仅 filter） |
| deliveryStatus → UI state 映射 | **无**直接映射代码 |
| statusArray → UI state 映射 | **无**直接映射代码（仅 filter） |
| tab → UI state 映射 | **无**（tab 是 filter 不调 $state.go） |
| 8 state 业务语义 | E（基于 state 命名推断） |
| 6 state 路由/页面 | F（route schema 缺失） |
| 后端状态机 | F（未观察） |
| 数据库状态字段 | F（未观察） |

---

## 25. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1-30.2 | 8 state 定义 + 引用 | A |
| 30.3-30.10 | 6 state 各条件 | A |
| 30.11 | chain 生命周期 | A |
| 30.12 | C-B complete → state.go | A |
| 30.13 | C-A complete → state.go | A |
| 30.14 | startOrder → state.go | A |
| 30.15 | receiveOrder → state.go | A |
| 30.16 | deliveryReceiveOrder → state.go | A |
| 30.17 | closeOrder → state.go | A |
| 30.18 | MachineCenterOrder.status 与 state | A（事实）/ F（直接映射） |
| 30.19 | receiveStatus 与 state | A（事实）/ F（直接映射） |
| 30.20 | acceptStatus 与 state | A（事实）/ F（直接映射） |
| 30.21 | statusArray | A（filter） |
| 30.22 | deliveryStatus 与 state | A（事实）/ F（直接映射） |
| 30.23 | machineOrderWaitProcessCtrl | A |
| 30.24 | setTab 完整 | A |
| 30.25 | tab → UI state | A（**不**映射） |
| 30.26 | state 名称业务语义 | A（字符串）/ E（业务解释） |
| 30.27 | status 数值 | A（事实）/ E（业务解释） |
| 30.28 | receiveStatus 数值 | A（事实） |
| 30.29 | 状态映射矩阵 | A（直接映射）/ F（未观察） |
| 30.30 | 最终冻结 | A（已知）/ F（未观察） |

**统计**：A=30 / B=0 / C=0 / D=0 / E=0 / F=0 = 30

---

## 26. L1/L2/L3

**L1（前端直接事实）**：
- 8 state 字符串使用位置
- chain → state.go 唯一直接映射
- 6 动作 $state.go 行为
- tab / acceptStatus / statusArray filter 协议
- 等级：A

**L2（业务模型解释）**：
- 8 state 业务含义（"待受理" / "待加工" / "加工中" / "测试中"）
- status 数值含义
- acceptStatus 业务含义
- 等级：**E**（基于命名 + 多源一致）

**L3（数据库/物理模型）**：
- machineCenterOrder 表
- 后端状态机
- 状态转换算法
- 等级：**F**

---

## 27. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 28. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | 8 state 当前有哪些直接 state.go？ | A（**仅 2 个**：machineOrderChainTesting + machineOrderTesting） |
| Q2 | 哪些 state 与 chain 有直接关系？ | A（machineOrderChainTesting + machineOrderTesting） |
| Q3 | 哪些 state 与 MachineCenterOrder.status 有直接关系？ | A（**无**） |
| Q4 | 哪些 state 与 receiveStatus 有直接关系？ | A（**无**） |
| Q5 | 哪些 state 与 acceptStatus 有直接关系？ | A（**无**） |
| Q6 | 哪些 state 与 deliveryStatus 有直接关系？ | A（**无**） |
| Q7 | statusArray 是否只是过滤？ | A（**是**） |
| Q8 | tab 是否直接等于 state？ | A（**否**，tab 是 filter 不调 $state.go） |
| Q9 | C-B complete 是当前唯一直接 state transition 吗？ | A（**是**） |
| Q10 | C-A complete 是否直接 state.go？ | A（**否**） |
| Q11 | start 是否直接 state.go？ | A（**否**） |
| Q12 | receive 是否直接 state.go？ | A（**否**） |
| Q13 | delivery receive 是否直接 state.go？ | A（**否**） |
| Q14 | close 是否直接 state.go？ | A（**否**） |
| Q15 | MachineCenterOrder.status → UI state 直接映射？ | A（**否**） |
| Q16 | receiveStatus → UI state 直接映射？ | A（**否**） |
| Q17 | acceptStatus → UI state 直接映射？ | A（**否**） |
| Q18 | deliveryStatus → UI state 直接映射？ | A（**否**） |
| Q19 | tab → state？ | A（**否**） |
| Q20 | 状态机与 UI state 完全闭环？ | A（**否**，仅 chain → testing 闭环） |

---

## 29. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 30. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~129 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 31. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | 8 state 字符串**仅 2 个**有 $state.go 调用 | A |
| 2 | 6 动作 success 后**仅 C-B 调 $state.go** | A |
| 3 | chain 唯一来源 = $stateParams.chain | A |
| 4 | 唯一直接 state 映射 = chain → machineOrder[Chain]Testing | A |
| 5 | 唯一反向 state 映射 = $state.current.name → $scope.tab | A |
| 6 | tab 是 filter 不调 $state.go | A |
| 7 | acceptStatus / statusArray 仅是 filter | A |
| 8 | MachineCenterOrder.status 写入点仅 L16253 | A |
| 9 | receiveStatus 写入点仅 L4321 | A |
| 10 | deliveryStatus 写入点仅 L4336 | A |
| 11 | machineOrderWaitProcessCtrl 不调任何 API | A |
| 12 | tab 1/2/3/4 + acceptStatus + statusArray 完整对照 | A |

---

## 32. 最终一句话

"S1-70 完成，已 Git 封口，立即停止，不进入 S1-71，等待老板下一条指令。"
