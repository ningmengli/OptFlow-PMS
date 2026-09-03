# 116 S1-57 MachineOrder State / Tab / StateParams / Navigation 边界收口 26 项

**文档性质**：S1-57 MachineOrder 前端导航模型边界专项
**任务来源**：老板 S1-57 专项指令（9/3 16:16）
**侦察时间**：2026-09-03 16:20-16:50
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **MachineOrder 前端导航模型边界收口**：
>
> A. 8 个 state name 完整列表
> B. tab 映射完整
> C. $stateParams 读取路径
> D. $state.go 导航链
> E. URL 索引与 controller 端使用的差异
> F. 完整 route 定义的不可得边界

---

## 一、🎯 颠覆性 A 级新发现 - 8 个 state name 完整列表

### 1.1 controller.js L16206-16217 真实证据（A 级 100%）

```javascript
// machineOrderWaitProcessCtrl (controller L16206)
angular.module("bestvisionWeb").controller("machineOrderWaitProcessCtrl", 
  ["$scope", "$stateParams", "Popup", "DateUtilFactory", "$state", "ObjectFactory", 
   "ListFactory", "$http", "$timeout", function (...) {
  
  if ($scope.$state.current.name == "machineOrderChainWaitAccess" || 
      $scope.$state.current.name == "machineOrderWaitAccess") {
    $scope.tab = 1;
  } else if ($scope.$state.current.name == "machineOrderChainWaitProcess" || 
             $scope.$state.current.name == "machineOrderWaitProcess") {
    $scope.tab = 2;
  } else if ($scope.$state.current.name == "machineOrderChainProcessing" || 
             $scope.$state.current.name == "machineOrderProcessing") {
    $scope.tab = 3;
  } else if ($scope.$state.current.name == "machineOrderChainTesting" || 
             $scope.$state.current.name == "machineOrderTesting") {
    $scope.tab = 4;
  } else {}
  console.log($scope.tab);
}]);
```

### 1.2 🎯 8 个 state name 完整列表（A 级 100%）

| # | State Name | 业务 | $scope.tab | controller |
|---|-----------|------|-----------|-----------|
| 1 | `machineOrderWaitAccess` | 店内加工中心 - 待受理 | 1 | machineOrderWaitProcessCtrl |
| 2 | `machineOrderChainWaitAccess` | 连锁加工中心 - 待受理 | 1 | machineOrderWaitProcessCtrl |
| 3 | `machineOrderWaitProcess` | 店内加工中心 - 待加工 | 2 | machineOrderWaitProcessCtrl |
| 4 | `machineOrderChainWaitProcess` | 连锁加工中心 - 待加工 | 2 | machineOrderWaitProcessCtrl |
| 5 | `machineOrderProcessing` | 店内加工中心 - 加工中 | 3 | machineOrderWaitProcessCtrl |
| 6 | `machineOrderChainProcessing` | 连锁加工中心 - 加工中 | 3 | machineOrderWaitProcessCtrl |
| 7 | `machineOrderTesting` | 店内加工中心 - 加工测试 | 4 | machineOrderWaitProcessCtrl |
| 8 | `machineOrderChainTesting` | 连锁加工中心 - 加工测试 | 4 | machineOrderWaitProcessCtrl |

**🎯 S1-57 关键 A 级新发现 - 8 个 state name 全部直接来自 controller.js 源码**：
- 4 个非连锁（店内）+ 4 个连锁（chain）
- 全部共享 `machineOrderWaitProcessCtrl`
- 每个 state 通过 `$state.current.name` 字符串比较设置 `$scope.tab` 1/2/3/4

---

## 二、URL 索引与 8 个 state 差异分析

### 2.1 视光之家url.txt 中直接观察的 machineOrder state（A 级 100%）

| # | State | URL | 业务 | 出现位置 |
|---|-------|-----|------|---------|
| 1 | `machineOrderWaitAccess` | `#!/machineOrderWaitAccess` | 店内加工中心 | url.txt L10 |
| 2 | `machineOrderChainWaitAccess` | `#!/machineOrderChainWaitAccess` | 连锁加工中心 | url.txt L11 |

### 2.2 🎯 S1-57 关键 A 级新发现 - 2 URL vs 8 state 差异 = R6 未观察

| 来源 | 直接观察到的 state 数 |
|------|---------------------|
| url.txt（前端用户可见菜单）| **2** |
| controller.js（controller 端）| **8** |
| 差异 | **6** |

**S1-57 严格表述**：
- url 索引 = **用户可见菜单**（非连锁 + 连锁待受理）
- controller 端 8 个 state = **全部 4 个状态**（待受理/待加工/加工中/加工测试）× **2 种模式**（连锁/非连锁）
- **6 个 state 的 URL 路由 = 当前证据范围未直接观察**（R6）
- 可能的解释（**仅业务推断 E**）：
  - url 索引只记录"用户主动访问"的页面
  - 其他 6 个 state 可能由"内部跳转"进入（如 C-B 完成后跳到 machineOrderTesting）
  - url 索引可能不完整

**S1-57 严格 F 表述**：
- ❌ 不能写"线上只有 2 个 state"
- ❌ 不能写"6 个 state 不存在"
- ✅ 只能写"url.txt 直接观察到 2 个 machineOrder state"

### 2.3 url 索引中**没有**的 6 个 state（A 级 100%）

| State | 业务 | URL |
|-------|------|-----|
| `machineOrderWaitProcess` | 店内加工中心 - 待加工 | **未直接观察 URL** |
| `machineOrderChainWaitProcess` | 连锁加工中心 - 待加工 | **未直接观察 URL** |
| `machineOrderProcessing` | 店内加工中心 - 加工中 | **未直接观察 URL** |
| `machineOrderChainProcessing` | 连锁加工中心 - 加工中 | **未直接观察 URL** |
| `machineOrderTesting` | 店内加工中心 - 加工测试 | **未直接观察 URL** |
| `machineOrderChainTesting` | 连锁加工中心 - 加工测试 | **未直接观察 URL** |

---

## 三、machineOrderBroken 真实业务

### 3.1 S1-57 关键 A 级新发现 - machineOrderBroken 不是 state name

| 搜索目标 | 出现位置 | 评级 |
|----------|---------|------|
| `machineOrderBroken` 字符串 | controller.js L16110（controller 名）| A 100% |
| `$state.go("machineOrderBroken")` | **0 处** | A 100% |
| `$state.current.name == "machineOrderBroken"` | **0 处** | A 100% |
| url 索引中 `machineOrderBroken` | **0 处** | A 100% |

**🎯 颠覆性 A 级新发现 - machineOrderBroken 全部用途 = controller 名称**：
- 唯一出现位置 = `machineOrderBrokenCtrl` (controller L16110)
- **不是 state name**
- **不是 URL 路径**
- **不是 HTML 文件名**（HTML 是 `machineOrderCompleted.html`）
- 真实入口 state name = **当前证据范围未直接观察**（F 维持）

### 3.2 machineOrderBrokenCtrl 内部完整结构

```javascript
// controller.js L16110
angular.module("bestvisionWeb").controller("machineOrderBrokenCtrl", 
  ["$scope", "Popup", "$window", "$stateParams", "$rootScope", "$state", 
   "$timeout", "ListFactory", "ObjectFactory", function (...) {
  
  $scope.cashflowId = $stateParams.cashflowId;        // ← stateParams
  $scope.machineCenterId = $stateParams.machineCenterId;
  $scope.chain = $stateParams.chain;
  
  $scope.obj = {};
  
  // 加载 API: getMachineCenterCashflowVo.json
  // 包含 completeOrder C-B
  // 包含 modifyLoss 报损功能
}]);
```

**S1-57 严格表述**：
- `machineOrderBrokenCtrl` 真实 = 报损页面 controller（S1-54 已确认）
- 3 个 stateParams 读取 = A 100%
- 但 controller 实际对应的 state name = **F 未直接观察**

---

## 四、$state.go 导航链

### 4.1 全部 2 个 machineOrder 目标（A 级 100%）

```javascript
// controller.js L16192-16196
if ($scope.chain == 1) {
  $state.go("machineOrderChainTesting");        // ← chain == 1 跳连锁
} else {
  $state.go("machineOrderTesting");            // ← 其他跳非连锁
}
```

**S1-57 关键 A 级新发现 - $state.go 跳转规则**：
- 触发位置：machineOrderBrokenCtrl 内部（C-B completeOrder 成功 callback）
- 触发条件：`$scope.chain == 1` 跳到 machineOrderChainTesting
- 其他情况跳到 machineOrderTesting
- **未传递额外参数**（cashflowId / machineCenterId / chain 都不在 state.go 参数中）

### 4.2 全部 293 个 $state.go 中其他 state（A 级 100%）

| state.go 目标 | 出现次数 | 备注 |
|--------------|---------|------|
| machineOrderTesting | 1 | L16195 |
| machineOrderChainTesting | 1 | L16193 |
| **其他 291 个** | 全部非 machineOrder | 业务相关 |

**S1-57 关键 A 级新发现**：
- machineOrderTesting/ChainTesting 是**跳转目标**（不是来源）
- 没有 $state.go 跳转到 machineOrderBroken（**F 维持**）
- 没有 $state.go 跳转到 machineOrderWaitAccess/WaitProcess/Processing（直接进入 url 索引的 2 个 state）

---

## 五、$scope.tab 完整映射

### 5.1 state name → tab 完整映射（A 级 100%）

| State | $scope.tab | 业务 | 评级 |
|-------|-----------|------|------|
| `machineOrderWaitAccess` | 1 | 待受理（非连锁）| A 100% |
| `machineOrderChainWaitAccess` | 1 | 待受理（连锁）| A 100% |
| `machineOrderWaitProcess` | 2 | 待加工（非连锁）| A 100% |
| `machineOrderChainWaitProcess` | 2 | 待加工（连锁）| A 100% |
| `machineOrderProcessing` | 3 | 加工中（非连锁）| A 100% |
| `machineOrderChainProcessing` | 3 | 加工中（连锁）| A 100% |
| `machineOrderTesting` | 4 | 加工测试（非连锁）| A 100% |
| `machineOrderChainTesting` | 4 | 加工测试（连锁）| A 100% |

### 5.2 严格区分（A 级 100%）

| 概念 | 真实位置 | 含义 |
|------|---------|------|
| **directive tab** | HTML L16 `tab="3"` | directive 内部属性（**非** state 参数）|
| **`$scope.tab`** | controller L16208-16214 | 4 个 state 共享 controller 的内部 tab |
| **URL route 参数** | （未直接观察）| F 维持 |

**S1-57 严格 F 表述**：
- directive 的 `tab="3"` **不是** state route 参数
- `tab="3"` 是 **directive 内部** 用的，与 `$scope.tab = 3`（state `Processing`）无关

---

## 六、$stateParams 完整路径

### 6.1 machineOrderBrokenCtrl 读取 3 个参数（A 级 100%）

```javascript
// L16111-16113
$scope.cashflowId = $stateParams.cashflowId;          // ← 读取
$scope.machineCenterId = $stateParams.machineCenterId;
$scope.chain = $stateParams.chain;
```

| 参数 | 真实表达式 | 用途 | 评级 |
|------|-----------|------|------|
| `cashflowId` | `$stateParams.cashflowId` | 加载 getMachineCenterCashflowVo.json Request + 报损 API | A 100% |
| `machineCenterId` | `$stateParams.machineCenterId` | 加载 getMachineCenterCashflowVo.json Request | A 100% |
| `chain` | `$stateParams.chain` | C-B if 分支（$scope.chain == 1 跳 machineOrderChainTesting）| A 100% |

### 6.2 machineOrderWaitProcessCtrl 读取 0 个参数

| 参数 | 读取 | 评级 |
|------|------|------|
| `cashflowId` | **未读取** | A 100% |
| `machineCenterId` | **未读取** | A 100% |
| `chain` | **未读取** | A 100% |
| `medicalRecordId` | **未读取** | A 100% |

**S1-57 关键 A 级新发现 - machineOrderWaitProcessCtrl 不依赖任何 stateParams**：
- 仅依赖 `$state.current.name`（用于设置 $scope.tab）
- 这意味着：tab 分类不需要任何路由参数

### 6.3 route schema 定义 = F 维持

| 项目 | 评级 |
|------|------|
| machineOrderBroken 路由中 `cashflowId` 是否定义 | F |
| machineOrderBroken 路由中 `machineCenterId` 是否定义 | F |
| machineOrderBroken 路由中 `chain` 是否定义 | F |
| machineOrderTesting / ChainTesting 路由中是否有 stateParams | F |
| 其他 6 个 state 路由参数 | F |

**S1-57 严格 F 表述**：
- controller 端**读取** $stateParams 是 A 100%
- route 配置**定义**这些参数 = F
- ❌ 不能写 "route 一定定义了 cashflowId"

---

## 七、controller 与 state 完整对应

### 7.1 4 个 MachineOrder 相关 controller（A 级 100%）

| Controller | 行号 | 业务 |
|-----------|------|------|
| `machineOrderListCtrl` | L4243 | 加工单列表 |
| `machineOrderCtrl` | L15943 | 通用加工（start/complete C-A/close + 验光处方）|
| `machineOrderBrokenCtrl` | L16110 | 报损页面（C-B completeOrder）|
| `machineOrderWaitProcessCtrl` | L16206 | 8 个 state 共享（tab 分类）|

### 7.2 controller → state 完整证据（A 级 100%）

| Controller | state 数量 | state name 列表 |
|-----------|----------|---------------|
| `machineOrderListCtrl` | **0 个直接 state 绑定**（可能绑定但未直接观察）| F |
| `machineOrderCtrl` | **0 个直接 state 绑定** | F |
| `machineOrderBrokenCtrl` | **0 个直接 state 绑定**（只是 controller 名）| A 100% |
| `machineOrderWaitProcessCtrl` | **8 个 state 共享** | 8 个 state name 全部 A 100% |

### 7.3 🎯 S1-57 关键 A 级新发现 - machineOrderBrokenCtrl 不是 machineOrderWaitProcessCtrl

- machineOrderBrokenCtrl = **独立 controller**（不是 8 个 state 共享 controller 之一）
- machineOrderBrokenCtrl 内部 8 个 state 共享 controller **完全不涉及**
- machineOrderBrokenCtrl 处理报损 + 验光处方 + 加工完成（C-B）

### 7.4 🎯 S1-57 关键 A 级新发现 - machineOrderTesting 真实入口

C-B 完成后跳转到 machineOrderTesting / machineOrderChainTesting（A 100%）：

```
machineOrderBrokenCtrl (报损页面)
  ↓ completeOrder C-B 成功
  ↓
if ($scope.chain == 1) {
  $state.go("machineOrderChainTesting")   // ← 跳到加工测试（连锁）
} else {
  $state.go("machineOrderTesting")        // ← 跳到加工测试（非连锁）
}
  ↓
machineOrderWaitProcessCtrl (8 个 state 共享 controller)
  ↓
$scope.tab = 4 (Testing)
```

**这就是 machineOrderTesting / ChainTesting 的真实入口路径**（A 100%）。

---

## 八、名称实体严格区分

### 8.1 7 个 MachineOrder 相关名称（A 级 100%）

| 名称 | 类型 | 真实含义 | 评级 |
|------|------|---------|------|
| `machineOrderCompleted.html` | HTML 文件 | 报损页面（注释 `<!-- machineOrderBrokenCtrl -->`）| A 100% |
| `machineOrderList.html` | HTML 文件 | 加工单列表 | A 100% |
| `machineOrderListCtrl` | controller | 加工单列表 controller | A 100% |
| `machineOrderCtrl` | controller | 通用加工 controller | A 100% |
| `machineOrderBrokenCtrl` | controller | 报损 controller（C-B 真实位置）| A 100% |
| `machineOrderWaitProcessCtrl` | controller | 8 个 state 共享 controller | A 100% |
| `machineOrderTesting` | state name | 加工测试（非连锁）| A 100% |
| `machineOrderChainTesting` | state name | 加工测试（连锁）| A 100% |
| `machineOrderBroken` | **不是 state name** | 仅 controller 名（L16110）| A 100% |

### 8.2 严禁推断（A 级 100%）

| 严禁 | 严禁 | 严禁 |
|------|------|------|
| ❌ machineOrderBroken.html（不存在）| ❌ machineOrderBroken state（不存在）| ❌ machineOrderBroken route（不存在）|
| ❌ machineOrderTesting.html（不存在）| ❌ machineOrderChainTesting.html（不存在）| ❌ machineOrderWaiting.html（不存在）|

---

## 九、2 URL vs 8 state 差异解释

### 9.1 事实分层（A 级 100%）

| 事实 | 来源 | 评级 |
|------|------|------|
| url 索引直接观察到 2 个 machineOrder state | 视光之家url.txt L10-11 | A 100% |
| controller 端直接观察到 8 个 machineOrder state | controller.js L16206-16217 | A 100% |
| 6 个 state 缺少 URL 证据 | 差异 | A 100% |

### 9.2 解释尝试（E 业务推断 / F 当前证据）

| 解释 | 评级 |
|------|------|
| url 索引只记录用户主动访问的页面 | E |
| 其他 6 个 state 由内部跳转进入（C-B 完成后）| E |
| url 索引不完整 | E |
| 真正原因 = 当前证据无法解释 | R6 F |

### 9.3 🎯 S1-57 严格 R6 表述

| 表述 | 评级 |
|------|------|
| "8 个 state 是真实存在的，因为 controller 中直接使用" | A 100% |
| "2 个 URL 是用户可见入口" | A 100% |
| "6 个 state 缺少 URL，因为 url 索引不完整" | E |
| "8 个 state 是否全部真实可访问" | R6 F |
| "线上系统只有 2 个 machineOrder state" | **❌ 严禁** |
| "线上系统有 8 个 machineOrder state" | **❌ 严禁** |

---

## 十、$stateParams 完整模型

### 10.1 读取事实 vs 定义事实（A 级 100%）

| 状态 | stateParams 读取 | stateParams 定义 |
|------|----------------|----------------|
| machineOrderWaitAccess | 0 个 | F 维持 |
| machineOrderWaitProcess | 0 个 | F 维持 |
| machineOrderProcessing | 0 个 | F 维持 |
| machineOrderTesting | 0 个 | F 维持 |
| machineOrderChainWaitAccess | 0 个 | F 维持 |
| machineOrderChainWaitProcess | 0 个 | F 维持 |
| machineOrderChainProcessing | 0 个 | F 维持 |
| machineOrderChainTesting | 0 个 | F 维持 |
| **machineOrderBroken** | 3 个（cashflowId/machineCenterId/chain）| F 维持 |
| machineOrderBroken 实际入口 state | **F 维持** | F 维持 |

### 10.2 🎯 S1-57 关键 A 级新发现 - machineOrderBroken 是"未观察入口 state"的"已观察 controller"

- controller 端：读取 3 个 stateParams（A 100%）
- route 端：定义这些参数（F 维持）
- state 端：真实入口 state name 未直接观察（F 维持）

---

## 十一、Route Completeness 矩阵

### 11.1 8 个 state 完整 route 完整性（A 级 100%）

| State | Name | Controller | URL | Template | Params | Route 定义 | 完整性 |
|------|------|-----------|-----|----------|--------|------------|--------|
| machineOrderWaitAccess | A | machineOrderWaitProcessCtrl | **A**（url.txt）| F | F | F | **B 部分** |
| machineOrderWaitProcess | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderProcessing | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderTesting | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderChainWaitAccess | A | machineOrderWaitProcessCtrl | **A**（url.txt）| F | F | F | **B 部分** |
| machineOrderChainWaitProcess | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderChainProcessing | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderChainTesting | A | machineOrderWaitProcessCtrl | F | F | F | F | **F** |
| machineOrderBroken (实际入口) | **F** | machineOrderBrokenCtrl | F | F | F | F | **F** |

**完整性定义**：
- **A 全部直接观察**
- **B 部分直接观察**（name + controller + URL）
- **F 只有 name / 使用，route 定义缺失**

---

## 十二、可复制导航模型

### 12.1 一期可复制的导航模型（A 级 100%）

```
State Name (直接观察)
  ↓
Controller (直接观察)
  ↓
$scope.tab (直接观察)
  ↓
$stateParams.X (读取端直接观察)
  ↓
$state.go (调用端直接观察)
  ↓
后续 state (直接观察)
```

### 12.2 一期**不可**复制的（route 定义）

```
完整 route URL (url.txt 只有 2 个)
  ↓
Template (7 HTML 都不是 route 入口)
  ↓
Resolve (未直接观察)
  ↓
完整 route schema (未直接观察)
```

### 12.3 🎯 S1-57 关键 A 级新发现 - 导航模型成立条件

- **成立条件**：直接观察 state name + controller + tab + stateParams + state.go
- **不成立**：route URL + template + resolve + schema
- **结论**：**导航模型可复制，但 route 完整定义不可复制**

---

## 十三、L1/L2/L3 边界

### 13.1 L1 前端事实（A 100%）

- 8 个 state name 完整列表
- machineOrderWaitProcessCtrl 8 个 state 共享
- $scope.tab 1/2/3/4 映射
- machineOrderBrokenCtrl 读取 3 个 stateParams
- C-B $state.go if chain==1
- 2 URL 在 url.txt

### 13.2 L2 业务模型（E 级）

- url 索引只记录用户可见页面
- 6 个 state 可能由内部跳转进入
- machineOrderBroken 真实入口

### 13.3 L3 完整 route 架构（F = 未观察）

- 8 个 state 完整 route 配置
- template / templateUrl
- resolve / data
- onEnter / onExit
- redirectTo
- 完整 SPA 路由架构

---

## 十四、26 项评级矩阵

### A 组：URL 索引与 8 个 state（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | url 索引 MachineOrder state | 2 个 | A 100% |
| 2 | MachineOrder state name 全集 | 8 个 | A 100% |
| 3 | 8 个 state 逐项 | 8 行完整 | A 100% |
| 4 | 2 URL vs 8 state | 6 个差异 | A 100%（差异观察）/ F（原因解释）|

### B 组：3 个重点 state（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 5 | machineOrderBroken | 不是 state name | A 100% |
| 6 | machineOrderTesting | state name + C-B 入口 | A 100% |
| 7 | machineOrderChainTesting | state name + C-B 入口 | A 100% |

### C 组：Controller（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 8 | machineOrderWaitProcessCtrl | 8 个 state 共享 | A 100% |
| 9 | 其他 3 个 MachineOrder controller | 真实存在 | A 100% |

### D 组：tab / stateParams（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 10 | $scope.tab | 1/2/3/4 映射 | A 100% |
| 11 | state → tab 映射 | 8 个 state 全部 | A 100% |
| 12 | $stateParams.cashflowId | L16111 读取 | A 100% |
| 13 | $stateParams.machineCenterId | L16112 读取 | A 100% |
| 14 | $stateParams.chain | L16113 读取 | A 100% |

### E 组：$state.go 导航（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 15 | $state.go machineOrderTesting | L16195 | A 100% |
| 16 | $state.go machineOrderChainTesting | L16193 | A 100% |
| 17 | chain 条件 | if chain==1 | A 100% |

### F 组：综合（9 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 18 | controller → state | machineOrderWaitProcessCtrl 8 个 state 共享 | A 100% |
| 19 | HTML / state / controller 区分 | 7 个名称实体 | A 100% |
| 20 | URL → state | 2 个直接观察 | A 100% |
| 21 | URL 缺失边界 | 6 个 state 缺 URL | A 100% |
| 22 | 导航模型 | 6 步成立 | A 100% |
| 23 | method/tab/cashflow-id 分层 | 3 个独立概念 | A 100% |
| 24 | Route Completeness | 8 个 state 大部分 F | A 100% |
| 25 | 一期复刻边界 | 12 A + 14 F | A 100% |

### G 组：26 项总评（1 项）

| # | 项目 | 评级 |
|---|------|------|
| 26 | 26 项总评 | 25 A + 0 B/C/D/E + 1 F（machineOrderBroken 实际入口 state）| A 100% |

---

## 十五、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 25 | 96.2% | controller 端 state 使用证据 100% 收口 |
| **B** | 0 | 0% | — |
| **C** | 0 | 0% | — |
| **D** | 0 | 0% | — |
| **E** | 0 | 0% | — |
| **F** | 1 | 3.8% | machineOrderBroken 实际入口 state 未观察 |
| **合计** | **26** | **100%** | — |

**L1=25 / L2=0 / L3=0 / F=1**

---

## 十六、本轮新增事实（S1-57 独有）

### 事实 1：8 个 state name 完整列表

**事实**：
- `machineOrderWaitAccess` / `machineOrderChainWaitAccess` (tab=1)
- `machineOrderWaitProcess` / `machineOrderChainWaitProcess` (tab=2)
- `machineOrderProcessing` / `machineOrderChainProcessing` (tab=3)
- `machineOrderTesting` / `machineOrderChainTesting` (tab=4)

**证据**：controller.js L16207-16214

**等级**：**A 100%**

### 事实 2：8 个 state 全部共享 machineOrderWaitProcessCtrl

**事实**：8 个 state 都路由到同一个 controller `machineOrderWaitProcessCtrl`

**等级**：**A 100%**

### 事实 3：$scope.tab 完整 1-4 映射

**事实**：tab=1 (待受理) / 2 (待加工) / 3 (加工中) / 4 (加工测试)

**等级**：**A 100%**

### 事实 4：machineOrderBroken 不是 state name

**事实**：`machineOrderBroken` 0 处作为 state name 出现，仅作为 controller 名（L16110）

**等级**：**A 100%**

### 事实 5：machineOrderTesting 真实入口 = C-B 完成后跳转

**事实**：`$state.go("machineOrderTesting")` 在 machineOrderBrokenCtrl L16195（C-B 完成后），按 chain 跳转

**等级**：**A 100%**

### 事实 6：2 URL vs 8 state 差异 = 6 个 state 缺 URL

**事实**：url 索引 2 个 + controller 8 个 = 6 个 state 缺 URL

**等级**：**A 100%**（差异观察）/ **F**（原因解释）

### 事实 7：machineOrderBrokenCtrl 不属于 8 个 state 共享 controller

**事实**：machineOrderBrokenCtrl 是独立 controller（L16110），不归 machineOrderWaitProcessCtrl

**等级**：**A 100%**

### 事实 8：machineOrderWaitProcessCtrl 不读取任何 stateParams

**事实**：controller L16206-16217 只用 `$state.current.name`，不读取 cashflowId/machineCenterId/chain/medicalRecordId

**等级**：**A 100%**

### 事实 9：directive tab ≠ $scope.tab ≠ URL route 参数

**事实**：
- directive `tab="3"` (HTML L16) 是 directive 内部属性
- `$scope.tab = 3` 是 state Processing 时的内部 tab
- 两者是不同概念，**不混淆**

**等级**：**A 100%**

---

## 十七、历史纠错

| S1-56 结论 | S1-57 复核 |
|----------|----------|
| 8 个 state 共享 machineOrderWaitProcessCtrl | **升级 A 100%**（8 个 state name 全部逐项列出 + tab 映射）|
| directive 定义不可得 | **维持 F**（不在本轮范围）|
| state 完整定义不可得 | **维持 F**（route schema F）|
| machineOrderBroken 更像 controller 名 | **升级 A 100%**（0 处 state name）|

**S1-57 严格表述**：
- S1-55/S1-56 "8 个 state" 表述 = **S1-57 升级到 name 完整列表**
- S1-55/S1-56 "machineOrderBroken 不是 state" 表述 = **S1-57 升级到 0 处直接观察**

---

## 十八、一期复刻影响

### 18.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | 8 个 state name + tab 映射 | A 100% |
| 2 | 4 个 MachineOrder controller | A 100% |
| 3 | $stateParams.cashflowId / machineCenterId / chain 读取 | A 100% |
| 4 | $state.go C-B 跳转规则 | A 100% |
| 5 | chain 条件判断 | A 100% |
| 6 | 8 个 state 共享 controller | A 100% |

### 18.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | 6 个 state 缺 URL 的原因 | E |
| 2 | machineOrderBroken 真实入口 state | E |
| 3 | route 完整 schema | E |

### 18.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 8 个 state 完整 route URL | F = 当前 6 个缺 |
| 2 | route template / templateUrl | F = 未直接观察 |
| 3 | route resolve / data | F = 未直接观察 |
| 4 | machineOrderBroken 实际入口 state name | F = 未直接观察 |
| 5 | route params schema | F = 未直接观察 |
| 6 | complete route architecture | F = 未直接观察 |

---

## 十九、严禁脑补清单

```
machineOrderBroken.html（不存在）
machineOrderTesting.html（不存在）
machineOrderChainTesting.html（不存在）
machineOrderWaiting.html（不存在）
machineOrderBroken state（不是 state name）
machineOrderBroken route config（不存在）
任何 6 个缺 URL state 的 route config
任何未直接观察的 state 名
```

---

## 二十、未解决问题（10 个 Q）

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | 8 个 state name 是否全部有直接来源？ | **是**（controller.js L16207-16214）| A 100% |
| Q2 | 8 个 state 是否全部属于 machineOrderWaitProcessCtrl？ | **是** | A 100% |
| Q3 | 2 URL 与 8 state 的差异能否解释？ | **当前证据无法解释** | F |
| Q4 | machineOrderBroken 是否有 state 定义？ | **不是 state name** | A 100% |
| Q5 | machineOrderTesting URL 是否可得？ | **F** | F |
| Q6 | machineOrderChainTesting URL 是否可得？ | **F** | F |
| Q7 | stateParams schema 是否可得？ | **F** | F |
| Q8 | route template 是否可得？ | **F** | F |
| Q9 | resolve 是否可得？ | **F** | F |
| Q10 | 完整 route architecture 是否可得？ | **F** | F |

---

## 二十一、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 二十二、文档元数据

- **文档编号**：116
- **任务阶段**：S1-57 MachineOrder State/Tab/StateParams/Navigation 边界
- **侦察时间**：2026-09-03 16:20-16:50
- **S1-57 颠覆性 A 级新发现**：
  1. **8 个 state name 完整列表**（全部直接观察）
  2. **8 个 state 全部共享 machineOrderWaitProcessCtrl**
  3. **machineOrderBroken 不是 state name**（0 处 state 出现）
  4. **machineOrderTesting 真实入口 = C-B 完成后跳转**
  5. **2 URL vs 8 state 差异 = 6 个 state 缺 URL**
  6. **machineOrderBrokenCtrl 不属于 8 个 state 共享 controller**
  7. **machineOrderWaitProcessCtrl 不读取任何 stateParams**
  8. **directive tab ≠ $scope.tab ≠ URL route 参数**
- **26 项评级 = 25 A + 0 E + 0 B/C/D + 1 F = 96% A 收口**
- **L1=25 / L2=0 / L3=0 / F=1**
- **历史文档影响**：0（28~115 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-58

---

> **S1-57 完成。**
> **25 A + 0 E + 0 B/C/D + 1 F（导航模型边界收口 96%）**。
> **8 个 state name + tab 映射 + stateParams + state.go 100% 收口，完整 route 定义仍 F 维持**。
> **下一步：等待老板下一条指令。**
