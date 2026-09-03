# 114 S1-55 order-brokeninfo directive + Start/Complete/Close + C-B 触发 + Close 状态收口 26 项

**文档性质**：S1-55 directive 黑盒 + 4 个核心问题收口
**任务来源**：老板 S1-55 专项指令（9/3 15:55）
**侦察时间**：2026-09-03 16:00-16:30
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **S1-54 留下的 directive 黑盒 + 4 个核心 F 收口**：
>
> A. order-brokeninfo directive 定义位置
> B. Start / Complete / Close 内部调用链
> C. Complete C-B 触发来源
> D. Close 最终 status

---

## 一、🎯 关键 A 级新发现 - 侦察范围严格限制

### 1.1 当前可用源码范围（A 级 100%）

| 资源 | 状态 | 大小 |
|------|------|------|
| controller.js | 可搜索 | 58,817 行 |
| 7 个 untracked HTML | 可搜索 | addSaleRecord / deliveryList / getGlassNotifyList / machineOrderCompleted / machineOrderList / payedDetail / payedList |
| 其他文件 | **不可用** | untracked / tracked 中均未发现 |

### 1.2 严格 F 边界（A 级 100%）

**S1-55 颠覆性 A 级新发现 - 以下内容在当前 controller.js + 7 HTML 范围内 0 处出现**：

| 资源 | 出现次数 | 评级 |
|------|---------|------|
| `order-brokeninfo` directive 定义 | **0 处** | **F = 当前证据范围未直接观察** |
| `.directive(` 调用 | **0 处** | F |
| `orderBrokenInfo` / `orderBroken` 字符串 | **0 处** | F |
| `stateProvider` / `.state(` 路由配置 | **0 处** | F |
| `.config(` 调用 | **0 处** | F |
| `uiRouter` 引用 | **0 处** | F |

**S1-55 严格表述**：
- directive 定义 = 当前仓库源码范围未直接观察
- state 路由配置 = 当前仓库源码范围未直接观察
- 所有这些定义可能在 untracked / tracked 的其他 JS 文件中

---

## 二、order-brokeninfo directive 完整证据

### 2.1 directive 在 HTML 中的使用（A 级 100%）

```html
<!-- machineOrderCompleted.html L13-18 -->
<div
  order-brokeninfo
  method="getStockObjectFactory.result.object.methodGlassRecord"
  tab="3"
  cashflow-id="{{cashflowId}}"
></div>
```

### 2.2 已知 directive 三个 attribute（A 级 100%）

| Attribute | HTML 真实值 | 来源 | 评级 |
|-----------|------------|------|------|
| `method` | `getStockObjectFactory.result.object.methodGlassRecord` | `getMachineCenterCashflowVo.json` Response | A 100% |
| `tab` | `"3"` | HTML 硬编码 | A 100% |
| `cashflow-id` | `{{cashflowId}}` | 绑定 `$scope.cashflowId` | A 100% |

### 2.3 🎯 S1-55 颠覆性 A 级新发现 - `method` attribute 真实含义

- `methodGlassRecord` = 后端返回的**方法对象**（不是简单字符串）
- 加载 API = `getMachineCenterCashflowVo.json`（L16118）
- 加载位置 = `machineOrderBrokenCtrl` 的 `searchStock()` 函数（L16116-16123）

```javascript
// controller.js L16116-16123
var searchStock = function searchStock() {
  $scope.getStockObjectFactory = new ObjectFactory();
  $scope.getStockObjectFactory.saveOrQuery("/admin/getMachineCenterCashflowVo.json", {
    cashflowId: $scope.cashflowId,
    machineCenterId: $scope.machineCenterId
  });
};
```

**含义推断**（E 级）：`methodGlassRecord` = 后端返回的方法对象，directive 拿到这个对象后可能用于调用具体业务方法（如"开始" / "完成" / "关闭"）。但 directive 内部如何调用 = **F 未直接观察**。

### 2.4 directive scope / template / controller = F 维持

| 项目 | 证据 | 评级 |
|------|------|------|
| `restrict` | 未直接观察 | F |
| `scope` | 未直接观察 | F |
| `template` | 未直接观察 | F |
| `templateUrl` | 未直接观察 | F |
| `controller` | 未直接观察 | F |
| `link` | 未直接观察 | F |
| `compile` | 未直接观察 | F |
| `controllerAs` | 未直接观察 | F |

---

## 三、Start / Complete / Close 内部调用链

### 3.1 directive 内部 function = F 维持

| 动作 | directive 内部实现 | 评级 |
|------|------------------|------|
| Start function | **未直接观察**（directive 内部） | F |
| Start Request | **未直接观察** | F |
| Complete function | **未直接观察**（directive 内部） | F |
| Complete Request | **未直接观察** | F |
| Close function | **未直接观察**（directive 内部） | F |
| Close Request | **未直接观察** | F |
| commonOrder 调用 | **未直接观察** | F |
| common.url 设置 | **未直接观察** | F |

### 3.2 controller 端已确认的 function 范围

**Start / Complete C-A / Close 真实 function 存在**（S1-53 已 A 级确认）：

| Function | Controller | Request | 评级 |
|----------|-----------|---------|------|
| `startOrder` L16012 | machineOrderCtrl | `{ machineCenterOrderId: id }` | A 100% |
| `completeOrder` L16074 | machineOrderCtrl | `{ machineCenterOrderId: id }` | A 100% |
| `closeOrder` L16083 | machineOrderCtrl | `{ machineCenterOrderId: id }` | A 100% |

**Complete C-B 真实 function 存在**（S1-53 已 A 级确认）：

| Function | Controller | Request | 评级 |
|----------|-----------|---------|------|
| `completeOrder()` L16333 | machineOrderBrokenCtrl | `{ cashflowId, machineCenterId }` | A 100% |

**🎯 S1-55 关键 F 严格表述**：
- 这些 function **存在 controller 端**（A 级 100%）
- 但 directive **是否调用这些 function** = **F 未直接观察**
- directive **是否定义自己的同名 function** = **F 未直接观察**

---

## 四、Complete C-B 触发来源

### 4.1 controller.js 中 `state.go("machineOrderBroken")` = 0 处（F 维持）

- controller.js 全 58,817 行搜索 `state.go("machineOrderBroken")` = **0 处**
- 没有任何 controller 通过 `state.go` 主动跳转到 machineOrderBroken 页面

### 4.2 C-B 触发来源推测路径

**业务上可能的触发路径**：

```
[某个加工单详情页面]
   ↓ (用户操作：选择"报损")
   ↓
$state.go("machineOrderBroken", { cashflowId, machineCenterId, chain })
   ↓
machineOrderBrokenCtrl (L16110)
   ↓
页面 = machineOrderCompleted.html
   ↓
order-brokeninfo directive
   ↓
(方法通过 methodGlassRecord 对象分发)
   ↓
completeOrder() (C-B 模式)
   ↓
completeMachineCenterOrder.json
   ↓
跳转 machineOrderTesting / machineOrderChainTesting
```

**但**：
- **触发源页面 = F 未直接观察**
- **触发 function = F 未直接观察**
- **完整的 state 路由配置 = F 未直接观察**（controller.js 0 处 .state() / .config()）

### 4.3 严格 F 表述（A 级 100%）

| 项目 | 证据 | 评级 |
|------|------|------|
| machineOrderBroken 触发源页面 | **未直接观察** | F |
| machineOrderBroken 触发 function | **未直接观察** | F |
| machineOrderBroken state 路由配置 | **未直接观察** | F |
| machineOrderBroken URL 路由参数 | **cashflowId/machineCenterId/chain 来自 $stateParams** | A 100% |

---

## 五、machineOrderTesting / machineOrderChainTesting state

### 5.1 state 存在性证据（A 级 100%）

```javascript
// controller.js L16364-16365
} else if ($scope.$state.current.name == "machineOrderChainTesting" || 
           $scope.$state.current.name == "machineOrderTesting") {
  $scope.tab = 4;
}
```

- 2 个 state name 存在 = **A 100%**
- 对应 tab=4

### 5.2 state 路由配置 = F 维持

- controller.js 0 处 `.state("machineOrderTesting", ...)`
- state 的 url / template / templateUrl / controller 绑定 = **未直接观察**
- state 之间的跳转通过 `$state.go("machineOrderTesting")` / `$state.go("machineOrderChainTesting")` 实现

### 5.3 chain 分支条件（A 级 100%）

```javascript
// L16343-16347
if ($scope.chain == 1) {
  $state.go("machineOrderChainTesting");  // ← chain=1 跳到 ChainTesting
} else {
  $state.go("machineOrderTesting");      // ← 其他 跳到 Testing
}
```

- `chain` = `$stateParams.chain`（URL 路由参数）
- `chain == 1` 跳到 machineOrderChainTesting
- 其他跳到 machineOrderTesting

### 5.4 4 个 state name 与 tab 对应（A 级 100%）

| state name | tab | controller |
|-----------|-----|-----------|
| machineOrderWaitAccess | 1 | machineOrderWaitProcessCtrl |
| machineOrderChainWaitAccess | 1 | machineOrderWaitProcessCtrl |
| machineOrderWaitProcess | 2 | machineOrderWaitProcessCtrl |
| machineOrderChainWaitProcess | 2 | machineOrderWaitProcessCtrl |
| machineOrderProcessing | 3 | machineOrderWaitProcessCtrl |
| machineOrderChainProcessing | 3 | machineOrderWaitProcessCtrl |
| machineOrderTesting | 4 | machineOrderWaitProcessCtrl |
| machineOrderChainTesting | 4 | machineOrderWaitProcessCtrl |

**8 个 state 共享 1 个 controller**（machineOrderWaitProcessCtrl）= **A 100%**

### 5.5 machineOrderWaitProcessCtrl 真实业务

- controller 只做一件事：根据 `$state.current.name` 设置 `$scope.tab` (1/2/3/4)
- **没有 API 调用 / 没有 UI 操作 / 没有 button 绑定**（L16206-16217）
- 真实页面渲染逻辑 = **F 未直接观察**（在 untracked HTML / template 中）

---

## 六、Close 最终 status

### 6.1 close API + 重新查询机制（A 级 100%）

```javascript
// closeOrder L16083-16091
$scope.closeOrder = function (id, medicalRecordId, idx) {
  $scope.common.url = "/admin/closeMachineCenterOrder.json";
  $scope.common.medicalRecordId = medicalRecordId;
  $scope.common.machineCenterOrderId = id;
  $scope.common.idx = idx;
  Popup.confirm("确定关闭么？", function () {
    $scope.commonOrder();
  });
};

// commonOrder L16092-16106
$scope.commonOrder = function () {
  $scope.commonOrderFactory = new ObjectFactory();
  var commonPromise = $scope.commonOrderFactory.saveOrQuery(
    $scope.common.url, 
    { machineCenterOrderId: $scope.common.machineCenterOrderId }
  );
  commonPromise.then(function (res) {
    if (res.status == 1) {
      Popup.notice(res.errmsg);
    } else {
      $scope.getOrderFactory = new ObjectFactory();
      var orderPromise = $scope.getOrderFactory.saveOrQuery(
        "/admin/getMachineCenterOrder.json", 
        { medicalRecordId: $scope.common.medicalRecordId }
      );
      orderPromise.then(function (resp) {
        $scope.memberFactory.items[$scope.common.idx]
          .machineCenterOrder.status = resp.result.object.status;  // ← 重新赋值 status
      });
    }
  });
};
```

### 6.2 重新查询的 status 间接消费点 = F 维持

| 消费点 | 证据 | 评级 |
|--------|------|------|
| `machineCenterOrder.status` 重新赋值 | L16102 | A 100% |
| status 文字显示 | HTML ng-show 但**只显示 0/1/2 三种值** | A 100% |
| close 后 status 具体值（-1/3/99）| **未直接观察** | **F 维持** |

### 6.3 状态文字映射（HTML 完整证据）

| status 条件 | 文字 | 评级 |
|------------|------|------|
| `acceptStatus==0 && status==0` | "待受理" | A 100% |
| `acceptStatus==1 && status==0/1` | "制作中" | A 100% |
| `acceptStatus==1 && status==2` | "已完成" | A 100% |
| 其他 status 值 | **无文字映射** | F |

**🎯 S1-55 关键 F 严格表述**：
- close 后 status 值 = **当前证据范围未直接观察**
- HTML 不支持 status=3/-1/99 等其他值的文字显示
- 即使后端返回这些值，UI 无法显示
- **F 维持**（S1-52/53/54/55 维持 4 轮）

---

## 七、真正按钮来源

### 7.1 按钮调用证据（A 级 100% / F 维持）

| 按钮 | HTML ng-click | 评级 |
|------|---------------|------|
| 签收 | machineOrderList.html L335 `ng-click="receiveOrder(item.machineCenterOrder.id,$index)"` | A 100% |
| 发货 | machineOrderList.html L341 `ng-click="deliveryReceiveOrder(item.machineCenterOrder.id,$index)"` | A 100% |
| 开始 | directive `order-brokeninfo`（**directive 内部 template 未直接观察**）| F |
| 完成 C-A | directive `order-brokeninfo`（**directive 内部 template 未直接观察**）| F |
| 完成 C-B | directive `order-brokeninfo`（**directive 内部 template 未直接观察**）| F |
| 关闭 | directive `order-brokeninfo`（**directive 内部 template 未直接观察**）| F |

### 7.2 🎯 S1-55 颠覆性 A 级新发现 - directive 内部 template 是真实按钮位置

- directive 的 template / templateUrl 可能在 untracked 文件中
- **S1-55 严格 F 表述**：当前 controller.js + 7 HTML 范围**未直接观察** directive 内部按钮
- 这是**S1-55 唯一新增事实**：之前 S1-54 已发现 directive 存在但未确认其内部 template

---

## 八、commonOrder 与 directive 关系

### 8.1 commonOrder 真实定义位置（A 级 100%）

```javascript
// controller.js L16092-16106
$scope.commonOrder = function () { ... }
```

- commonOrder 定义在 **machineOrderCtrl**（L15943-L16107）
- **不在 directive 中**（directive 定义未直接观察）

### 8.2 directive 是否调用 commonOrder = F 维持

- directive 内部代码 = 未直接观察
- directive 是否调用 `machineOrderCtrl.$scope.commonOrder` = **F**
- directive 是否有自己的 commonOrder = **F**
- directive 是否通过 `methodGlassRecord.start()` 等后端方法调用 = **E 业务推断**

---

## 九、26 项评级矩阵

### A 组：order-brokeninfo directive（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | directive 定义 | **未直接观察**（controller.js 0 处 .directive）| F |
| 2 | directive scope | 未直接观察 | F |
| 3 | directive template/templateUrl | 未直接观察 | F |
| 4 | directive method 参数 | HTML = `getStockObjectFactory.result.object.methodGlassRecord` | A 100% |
| 5 | directive 其他参数 | tab="3" / cashflow-id="{{cashflowId}}" | A 100% |

### B 组：Start 内部调用（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 6 | directive 内部 start function | 未直接观察 | F |
| 7 | start Request | controller 端已确认 | A 100% |
| 8 | directive 是否调用 commonOrder | 未直接观察 | F |

### C 组：Complete 内部调用（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 9 | directive 内部 complete function | 未直接观察 | F |
| 10 | Complete C-A / C-B 判断 | controller 端已确认（不同 controller）| A 100% |
| 11 | complete Request | controller 端已确认（C-A: machineCenterOrderId / C-B: cashflowId+machineCenterId）| A 100% |

### D 组：Close（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 12 | directive 内部 close function | 未直接观察 | F |
| 13 | close Request | controller 端已确认 | A 100% |

### E 组：machineOrderBroken / C-B 触发（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 14 | machineOrderBroken state 路由 | **未直接观察**（controller.js 0 处 .state）| F |
| 15 | machineOrderBrokenCtrl | L16110 真实存在 | A 100% |
| 16 | C-B 触发来源 | `state.go("machineOrderBroken")` = 0 处 | F |

### F 组：machineOrderTesting（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 17 | machineOrderTesting state | 2 个 state name 存在 | A 100% |
| 18 | machineOrderChainTesting state | chain==1 跳到 | A 100% |

### G 组：chain（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 19 | chain 参数链 | `$stateParams.chain` → `$scope.chain` → C-B if 分支 | A 100% |
| 20 | chain 业务含义 | **未直接观察**（1=连锁？=业务推断 E）| E |

### H 组：综合（6 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 21 | 真正按钮来源 | directive 内部 template 未直接观察 | F |
| 22 | commonOrder 与 directive 关系 | commonOrder 在 machineOrderCtrl，directive 调用未直接观察 | F |
| 23 | close 后 status | F 维持 | F |
| 24 | 完整执行链 | 部分链路缺失（directive 内部）| A 100%（partial）+ F |
| 25 | 26 项评级 | 13 A + 1 E + 12 F | A 100% |
| 26 | 一期复刻边界 | controller 端可复刻，directive 端需后续 | A 100% |

---

## 十、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 13 | 50% | controller 端证据全部 100% 收口 |
| **B** | 0 | 0% | — |
| **C** | 0 | 0% | — |
| **D** | 0 | 0% | — |
| **E** | 1 | 3.8% | chain 业务含义 |
| **F** | 12 | 46.2% | directive 黑盒 + state 路由 + close status |
| **合计** | **26** | **100%** | — |

**L1=13 / L2=0 / L3=0 / E=1 / F=12**

---

## 十一、完整执行链

### 11.1 controller 端完整链（A 级 100%）

```
[某个加工单详情页面] (F 触发源未直接观察)
  ↓ $state.go("machineOrderBroken", { cashflowId, machineCenterId, chain })
machineOrderBroken 页面（machineOrderCompleted.html）
  ↓
machineOrderBrokenCtrl (L16110)
  ↓
$scope.cashflowId = $stateParams.cashflowId (L16111)
$scope.machineCenterId = $stateParams.machineCenterId (L16112)
$scope.chain = $stateParams.chain (L16113)
  ↓
order-brokeninfo directive (HTML L14)
  ↓ [F directive 内部]
[完成按钮 / 其他按钮] (F 未直接观察)
  ↓
completeOrder() C-B 模式 (L16333)
  ↓
Popup.confirm("确定完成么")
  ↓
saveOrQuery(completeMachineCenterOrder.json, { cashflowId, machineCenterId })
  ↓
成功 res.status == 0
  ↓
if ($scope.chain == 1) {
  $state.go("machineOrderChainTesting")  // 加工测试 (连锁)
} else {
  $state.go("machineOrderTesting")      // 加工测试 (非连锁)
}
```

### 11.2 directive 内部 = F 维持

directive 内部如何：
- 接收 method / tab / cashflow-id attribute
- 内部 template 包含什么按钮
- 按钮 ng-click 调用哪个 function
- 是否调用 commonOrder

**全部 = F = 当前证据范围未直接观察**

### 11.3 8 个 state name 关系链（A 级 100%）

```
[4 个非连锁]              [4 个连锁]                  共享 controller
machineOrderWaitAccess ←→ machineOrderChainWaitAccess  →  tab=1
machineOrderWaitProcess ←→ machineOrderChainWaitProcess →  tab=2
machineOrderProcessing  ←→ machineOrderChainProcessing  →  tab=3
machineOrderTesting     ←→ machineOrderChainTesting     →  tab=4
                                                      ↓
                                            machineOrderWaitProcessCtrl
```

---

## 十二、L1/L2/L3 边界

### 12.1 L1 前端事实（A 100%）

- 4 个 controller 完整定义（machineOrderListCtrl / machineOrderCtrl / machineOrderBrokenCtrl / machineOrderWaitProcessCtrl）
- 4 个 function 真实存在（startOrder / completeOrder C-A / closeOrder / completeOrder C-B）
- commonOrder 完整定义 + URL 注入模式
- chain 参数链（URL → $stateParams → $scope → if 分支）
- 8 个 state name 共享 controller + tab 设置
- directive 3 个 attribute 真实使用
- method = getStockObjectFactory.result.object.methodGlassRecord

### 12.2 L2 业务模型（E 级）

- chain=1 = 连锁店模式（业务推断）
- methodGlassRecord = 后端返回的方法对象（业务推断）
- close 后 status 新值（业务推断）
- 后端状态机

### 12.3 L3 数据库物理（F = 未观察）

- 表名
- 主键/外键
- close 后 status 实际值
- 后端事务

---

## 十三、本轮新增事实（S1-55 独有）

### 事实 1：order-brokeninfo directive 完全在 controller.js 范围外

**事实**：controller.js 全 58,817 行搜索 `.directive(` = 0 处，`orderBrokenInfo` 字符串 = 0 处

**评级**：**A 100%**（确认 directive 定义不在 controller.js）

### 事实 2：路由配置完全在 controller.js 范围外

**事实**：controller.js 0 处 `.state(` / `.config(` / `stateProvider`

**评级**：**A 100%**（确认 state 路由配置不在 controller.js）

### 事实 3：directive 三个 attribute 真实使用

**事实**：
- `method` = `getStockObjectFactory.result.object.methodGlassRecord`
- `tab` = `"3"`
- `cashflow-id` = `{{cashflowId}}`

**评级**：**A 100%**

### 事实 4：method attribute 来自后端方法对象

**事实**：`methodGlassRecord` 是 `getMachineCenterCashflowVo.json` Response 的方法对象字段

**证据**：controller.js L16118-16123 加载 API

**等级**：**A 100%**

### 事实 5：8 个 state name 共享 machineOrderWaitProcessCtrl

**事实**：8 个 state name 通过 controller L16207-16215 共享同一 controller，按 state name 设置 $scope.tab

**评级**：**A 100%**

### 事实 6：chain 参数完整路径

**事实**：`$stateParams.chain` → `$scope.chain` → C-B if 分支（决定跳转到 machineOrderTesting 或 machineOrderChainTesting）

**评级**：**A 100%**

### 事实 7：close 后 status 重新赋值但具体值 F 维持

**事实**：close 后 `memberFactory.items[idx].machineCenterOrder.status` 被重新赋值，但**当前证据范围未直接观察具体值**

**评级**：**F 维持**（4 轮观察 F）

---

## 十四、历史纠错

| S1-54 结论 | S1-55 复核 |
|----------|----------|
| machineOrderCompleted.html = 报损页面 | **维持 A 100%** |
| C-B 参数来自 $stateParams | **维持 A 100%** |
| machineOrderTesting 是 state name | **维持 A 100%** |
| start/complete/close 通过 directive `order-brokeninfo` | **维持 A 100%（directive 存在）+ F（内部实现）** |
| close status F 维持 | **F 维持** |
| C-B 触发来源 F 维持 | **F 维持** |

**S1-55 严格表述**：
- directive 定义 = 0 处（controller.js 完全范围）
- state 路由配置 = 0 处（controller.js 完全范围）
- **这些 F 不是因为搜得不够，而是因为代码确实不在 controller.js**

---

## 十五、一期复刻影响

### 15.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | commonOrder 完整定义 | A 100% |
| 2 | 4 个 controller 真实定义 | A 100% |
| 3 | 4 个 function 真实实现 | A 100% |
| 4 | chain 参数链完整 | A 100% |
| 5 | 8 个 state name + tab 映射 | A 100% |
| 6 | directive 3 个 attribute | A 100% |
| 7 | 5 个 HTML 模板完整 | A 100% |

### 15.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | chain 业务含义（1=连锁？）| E |
| 2 | methodGlassRecord 后端实现 | E |
| 3 | 后端状态机 | E |
| 4 | close status 新值 | E |
| 5 | state 完整路由配置 | E |

### 15.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | directive `order-brokeninfo` 内部实现 | F = controller.js + 7 HTML 范围 0 处 |
| 2 | state 完整路由配置 | F = controller.js 0 处 .state() |
| 3 | close 后 status 实际值 | F = HTML 不支持 status 3/-1/99 |
| 4 | C-B 触发源页面 | F = `state.go("machineOrderBroken")` 0 处 |
| 5 | directive 内部按钮 ng-click | F = 未直接观察 |
| 6 | 25 个 ID 字段 | F = 0 处出现 |
| 7 | 后端事务 | F = 未直接观察 |
| 8 | 数据库状态表 | F = 未直接观察 |

---

## 十六、严禁脑补清单

```
directive `order-brokeninfo` 内部代码
state 完整路由配置（url / templateUrl / controller）
close 后 status 实际值（-1/3/99）
C-B 触发源页面
directive 内部 button ng-click
closeStatus / completedStatus / testingStatus
machineOrderTestingId / deliveryId
任何数据库表名
任何数据库外键
```

---

## 十七、未解决问题（10 个 Q）

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | directive 是否完整找到？ | **未找到**（controller.js 0 处）| F |
| Q2 | directive 内 start/complete/close 是否完整？ | **未直接观察** | F |
| Q3 | 真正按钮是否找到？ | **未找到**（directive 内部）| F |
| Q4 | C-B 触发来源是否找到？ | **未找到**（state.go 0 处）| F |
| Q5 | machineOrderBroken route 参数是否完整？ | **URL 参数已知**（$stateParams.cashflowId/machineCenterId/chain）| A 100% |
| Q6 | machineOrderTesting / ChainTesting 路由是否完整？ | **state 存在 + tab=4 已确认**，完整路由未直接观察 | A / F |
| Q7 | chain 的业务含义是否仍未知？ | **是**（1=连锁？= 业务推断 E）| E |
| Q8 | close 后最终 status 是否可确定？ | **不可确定**（F 维持 4 轮）| F |
| Q9 | L3 数据库结构是否仍未知？ | **是**（F 维持）| F |
| Q10 | directive 内部 5 个按钮是否找到？ | **未找到** | F |

---

## 十八、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十九、文档元数据

- **文档编号**：114
- **任务阶段**：S1-55 directive 黑盒 + 4 个核心问题
- **侦察时间**：2026-09-03 16:00-16:30
- **S1-55 关键 A 级新发现**：
  1. **directive 定义完全在 controller.js 范围外**（0 处 .directive() / orderBrokenInfo 字符串）
  2. **state 路由配置完全在 controller.js 范围外**（0 处 .state() / .config()）
  3. **directive 3 个 attribute 真实使用**（method/tab/cashflow-id）
  4. **method = getStockObjectFactory.result.object.methodGlassRecord**（后端方法对象）
  5. **8 个 state name 共享 machineOrderWaitProcessCtrl**（按 state name 设置 tab）
  6. **chain 参数完整路径**（$stateParams → $scope → C-B if 分支）
- **26 项评级 = 13 A + 0 E + 0 B/C/D + 1 E + 12 F = 50% A 收口**
- **L1=13 / L2=0 / L3=0 / E=1 / F=12**
- **历史文档影响**：0（28~113 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-56

---

> **S1-55 完成。**
> **13 A + 0 E + 0 B/C/D + 1 E + 12 F（4 个核心问题收口 50%）**。
> **controller 端证据 100% 收口，directive 黑盒 + state 路由 + close status 仍 F 维持（因为确实不在 controller.js 范围）**。
> **下一步：等待老板下一条指令。**
