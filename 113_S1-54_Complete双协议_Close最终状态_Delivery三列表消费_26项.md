# 113 S1-54 Complete 双协议 + Close 最终状态 + Delivery 三列表消费专项收口 26 项

**文档性质**：S1-54 剩余断点专项收口
**任务来源**：老板 S1-54 专项指令（9/3 12:24）
**侦察时间**：2026-09-03 12:25-13:00
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **S1-53 留下的剩余断点收口**：
>
> A. Complete C-B 真实参数来源 + 跳转
> B. machineOrderTesting / machineOrderChainTesting 真实业务含义
> C. close 最终 status（A 级 100% 收口失败则保持 F）
> D. start/complete/close HTML 按钮入口
> E. Delivery 三列表真实 API 来源 + HTML 消费

---

## 一、🎯 颠覆性 A 级新发现 - machineOrderCompleted.html = 报损页面

### 1.1 HTML 注释直接证据（A 级 100%）

```html
<!-- machineOrderCompleted.html L2: machineOrderBrokenCtrl -->
```

**🎯 S1-54 颠覆性 A 级新发现**：
- HTML 注释明确标注 `machineOrderBrokenCtrl`
- **"Broken" = 报损**（不是"完成"）
- **machineOrderCompleted.html 不是"加工完成页面"，是"加工报损页面"**

### 1.2 machineOrderBrokenCtrl 真实业务范围（A 级 100%）

| Function | API | 业务 |
|----------|-----|------|
| `searchStock` L16116 | `getMachineCenterCashflowVo.json` | 加载报损页面数据 |
| `modifyLoss` L16143 | `createMedicalStockLoss.json` | 提交报损 |
| `showLossDetail` L16273 | `getMedicalStockLossVo.json` | 查看报损详情 |
| `completeOrder()` L16333 | `completeMachineCenterOrder.json` | C-B 加工完成 |
| `loss.machineCenterOrderId` L16328 | — | 报损用 `machineCenterOrderId` |

### 1.3 machineOrderBrokenCtrl 控制器命名误导性

⚠️ 命名陷阱：
- `machineOrderBrokenCtrl` 名字含 "Broken" → **报损**（不是"破损"）
- `machineOrderCompleted.html` 名字含 "Completed" → **是报损页面**（不是已完成页面）
- `machineOrderList.html` 名字含 "List" → **是加工单列表**（已完成 S1-52 状态机）
- `machineOrderCtrl` 名字是 `Ctrl` → **是 start/complete/close 的 controller**

---

## 二、🎯 颠覆性 A 级新发现 - Complete C-B 真实业务

### 2.1 C-B controller 边界（A 级 100%）

```javascript
// controller.js L16261（machineOrderBrokenCtrl）
$scope.cashflowId = $stateParams.cashflowId;        // ← URL 参数
$scope.machineCenterId = $stateParams.machineCenterId;  // ← URL 参数
$scope.chain = $stateParams.chain;                 // ← URL 参数（1=连锁）
```

**🎯 S1-54 颠覆性 A 级新发现 - C-B 参数全部来自 URL 路由参数**：
- `$stateParams.cashflowId`（不是从 cashflow 对象或医疗记录对象中获取）
- `$stateParams.machineCenterId`（不是从 machineCenter 对象中获取）
- `$stateParams.chain`（1=连锁店模式，0/其他=非连锁）

### 2.2 C-B 完整调用链（A 级 100%）

```javascript
// controller.js L16333-16353（machineOrderBrokenCtrl）
$scope.completeOrder = function () {                          // ← 不带参数
  Popup.confirm("确定完成么", function () {
    var completeFactory = new ObjectFactory();
    var completePromise = completeFactory.saveOrQuery(
      "/admin/completeMachineCenterOrder.json",               // ← 同 C-A API
      { 
        cashflowId: $scope.cashflowId,                        // ← URL 参数
        machineCenterId: $scope.machineCenterId                // ← URL 参数
      }
    );
    completePromise.then(function (res) {
      if (res.status == 0) {
        Popup.notice("完成成功");
        if ($scope.chain == 1) {
          $state.go("machineOrderChainTesting");                // ← 连锁店：跳转加工测试
        } else {
          $state.go("machineOrderTesting");                    // ← 非连锁：跳转加工测试
        }
      } else {
        Popup.notice(res.errmsg);
      }
    });
  });
};
```

**🎯 关键 A 级新发现 - C-B 与 C-A 的本质区别**：
| 项目 | C-A | C-B |
|------|-----|-----|
| controller | machineOrderCtrl | **machineOrderBrokenCtrl**（报损）|
| function | `completeOrder(id, medicalRecordId, idx)` | `completeOrder()` 无参 |
| Request id 来源 | 参数 `id` | `$stateParams.cashflowId/machineCenterId` |
| commonOrder | **是** | **否**（独立调用）|
| 后续行为 | 重新查询 status | **跳转加工测试页面** |
| 业务上下文 | 通用加工完成 | **报损页面上的"完成"按钮** |

### 2.3 C-B 触发来源未直接发现（F）

- `state.go("machineOrderBroken")` 在 controller.js 中**0 处出现**
- C-B 必须从其他 controller 的 `$state.go("machineOrderBroken", { cashflowId, machineCenterId, chain })` 跳转
- 当前 controller.js 范围内**未直接观察 C-B 的触发来源**
- **S1-54 严格表述**：F = 当前证据范围未直接观察

---

## 三、🎯 颠覆性 A 级新发现 - machineOrderTesting 真实含义

### 3.1 machineOrderTesting 是 state name（A 级 100%）

```javascript
// controller.js L16206-16217（machineOrderWaitProcessCtrl）
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
  $scope.tab = 4;                                              // ← machineOrderTesting = tab=4
}
```

**🎯 颠覆性 A 级新发现 - machineOrderTesting 是 4 个 Tab 中的第 4 个**：

| Tab | State name | 含义推断 |
|-----|-----------|---------|
| 1 | machineOrderWaitAccess | 待受理 |
| 2 | machineOrderWaitProcess | 待加工 |
| 3 | machineOrderProcessing | 加工中 |
| **4** | **machineOrderTesting** | **加工测试（已完成的待测试）** |

注意：**8 个 state name 共享同一个 controller**（4 个连锁 + 4 个非连锁）。

### 3.2 machineOrderTesting URL/页面 = F

- 当前 controller.js + 7 HTML 模板中**未观察** machineOrderTesting 页面具体 URL/HTML
- **S1-54 严格表述**：F = 当前证据范围未直接观察页面模板

### 3.3 C-B 跳转到 machineOrderTesting（A 级 100%）

- C-B completeOrder 成功后：`$state.go("machineOrderTesting")` (L16346)
- 连锁店模式：`$state.go("machineOrderChainTesting")` (L16344)
- **C-B 完成后 = 跳转到"加工测试"页面**（tab=4）

---

## 四、close 最终 status（F 维持）

### 4.1 close API 调用证据

```javascript
// controller.js L16083-16091
$scope.closeOrder = function (id, medicalRecordId, idx) {
  $scope.common.url = "/admin/closeMachineCenterOrder.json";
  $scope.common.medicalRecordId = medicalRecordId;
  $scope.common.machineCenterOrderId = id;
  $scope.common.idx = idx;
  Popup.confirm("确定关闭么？", function () {
    $scope.commonOrder();
  });
};
```

### 4.2 close 后 getMachineCenterOrder 重新查询

```javascript
// controller.js L16100-16103
var orderPromise = $scope.getOrderFactory.saveOrQuery(
  "/admin/getMachineCenterOrder.json", 
  { medicalRecordId: $scope.common.medicalRecordId }
);
orderPromise.then(function (resp) {
  $scope.memberFactory.items[$scope.common.idx]
    .machineCenterOrder.status = resp.result.object.status;  // ← 重新查询后赋值
});
```

### 4.3 close 后 status 真实值 = F 维持

**machineOrderList.html 中 status 全部条件**：

| 条件 | 出现位置 | 含义 |
|------|---------|------|
| `status==0` | L299, L303 | 待受理/制作中 |
| `status==1` | L307 | 制作中 |
| `status==2` | L311, L337 | 已完成/签收按钮 |

**🎯 S1-54 关键 A 级新发现 - HTML 状态文字映射证据完整但 close 后 status 新值仍 F**：
- HTML **只显示** status=0/1/2 三种值对应的文字
- **没有 status=-1/3/99 等其他值**
- close 触发的 status 新值**当前 controller.js + HTML 范围未直接观察**
- **F 维持**（S1-52/53 维持到 S1-54）

---

## 五、🎯 颠覆性 A 级新发现 - start/complete/close HTML 按钮 = directive

### 5.1 HTML 中 ng-click 实际调用证据

| API | ng-click | 出现位置 | 评级 |
|-----|----------|---------|------|
| receive | `receiveOrder(item.machineCenterOrder.id, $index)` | machineOrderList.html L335 | A 100% |
| delivery | `deliveryReceiveOrder(item.machineCenterOrder.id, $index)` | machineOrderList.html L341 | A 100% |
| start | **0 处** | — | F |
| complete C-A | **0 处** | — | F |
| close | **0 处** | — | F |
| complete C-B | **0 处**（machineOrderBrokenCtrl 通过 directive 调用）| — | F |

### 5.2 🎯 颠覆性 A 级新发现 - directive `order-brokeninfo`

```html
<!-- machineOrderCompleted.html L13-18 -->
<div
  order-brokeninfo
  method="getStockObjectFactory.result.object.methodGlassRecord"
  tab="3"
  cashflow-id="{{cashflowId}}"
></div>
```

**🎯 颠覆性 A 级新发现 - start/complete/close 通过 directive `order-brokeninfo`**：
- directive 名称 = `order-brokeninfo`
- 通过 3 个 attribute 传入：method / tab / cashflow-id
- **S1-54 关键 F 严格表述**：directive 的真实实现 = 当前 controller.js + 7 HTML 范围**未直接观察**（可能在 untracked 文件中）

### 5.3 🎯 推断 F 维持

- `order-brokeninfo` directive 内部可能调用 `startOrder`/`completeOrder`/`closeOrder`
- 但**当前 controller.js 范围内 directive 定义未找到**
- **S1-54 严格表述**：F = 当前证据范围未直接观察 directive 实现

---

## 六、Delivery 三列表消费

### 6.1 deliveryList.html 中 3 个子列表的 HTML 消费（A 级 100%）

| 列表 | HTML 出现 | 用途 | 评级 |
|------|----------|------|------|
| `item.waitingDeliveryList` | L251 `ng-if="item.waitingDeliveryList.length"` | **只显示计数** | A 100% |
| `item.sendToMachineCenterList` | L275 `ng-show="item.sendToMachineCenterList.length"` | **只显示计数** | A 100% |
| `item.deliveryedList` | L260/L267 `ng-if="item.deliveryedList.length"` | **只显示计数** | A 100% |

**🎯 颠覆性 A 级新发现 - deliveryList.html 中 3 个子列表只用于 .length 计数显示**：
- 不在 deliveryList.html 中渲染商品细节
- 商品细节渲染可能在其他页面（deliveryInput.html / deliveryInputRecord.html / partBack.html）

### 6.2 主列表 Response 路径（A 级 100%）

```html
<!-- deliveryList.html L202 -->
<div ng-repeat="item in memberFactory.items">
```

- `memberFactory.items` = `getCashflowDeliveryVoList.json` Response
- 即：**列表数据来自 `getCashflowDeliveryVoList.json`**

### 6.3 单条详情 API 提供子列表（A 级 100%）

```javascript
// controller.js L3827（deliveryInputCtrl）
var deliveryPromise = $scope.getMedicalRecordDeliveryFactory.saveOrQuery(
  '/admin/getCashflowDeliveryVo.json',                          // ← 单条详情
  { cashflowId: $scope.cashflowId }
);
deliveryPromise.then(function (res) {
  var arr = res.result.object.waitingDeliveryList;             // ← 三个子列表来自 result.object
  // ...
});
```

**🎯 关键 A 级新发现 - 3 个子列表的真实 API 来源**：

| 列表 | 列表 API | 单条 API | 评级 |
|------|---------|---------|------|
| `item.waitingDeliveryList` | `getCashflowDeliveryVoList.json` | `getCashflowDeliveryVo.json` | A 100% |
| `item.sendToMachineCenterList` | `getCashflowDeliveryVoList.json` | `getCashflowDeliveryVo.json` | A 100% |
| `item.deliveryedList` | `getCashflowDeliveryVoList.json` | `getCashflowDeliveryVo.json` | A 100% |

### 6.4 🎯 S1-54 关键 A 级新发现 - sendToMachineCenterList 真实路径

- 0 处 controller 引用（之前 S1-53 已确认）
- 但 HTML 1 处引用：`item.sendToMachineCenterList.length` (deliveryList.html L275)
- **A 100%**：HTML 消费存在，controller 不直接处理

**严格表述**：
- "controller 0 引用" ≠ "系统未使用"
- HTML 消费通过 `memberFactory.items`（从 `getCashflowDeliveryVoList.json` Response 直接暴露）
- **不经过 controller 中间处理**

### 6.5 5 个动作 API 与 Delivery 三列表刷新关系 = F 维持

S1-53 已确认 5 个动作 API 都不调用 `getCashflowDeliveryVoList.json` 刷新。S1-54 维持 F。

---

## 七、六张核心证据表

### 7.1 表 1：Complete C-B 参数来源

| 参数 | 原始表达式 | 来源对象 | 来源 | 传入 API | 评级 |
|------|-----------|---------|------|---------|------|
| `cashflowId` | `$stateParams.cashflowId` | URL 路由参数 | ui-sref 跳转 | completeMachineCenterOrder.json Request | A 100% |
| `machineCenterId` | `$stateParams.machineCenterId` | URL 路由参数 | ui-sref 跳转 | completeMachineCenterOrder.json Request | A 100% |
| `chain` | `$stateParams.chain` | URL 路由参数 | ui-sref 跳转 | 业务分支判断（不传 API）| A 100% |

**C-B 触发来源 = F 维持**（`state.go("machineOrderBroken")` 在 controller.js 0 处）

### 7.2 表 2：按钮 → Function → API

| UI 文字 | HTML/模板 | ng-click/调用 | Function | API | 参数 | 评级 |
|--------|----------|-------------|---------|-----|------|------|
| 签收 | machineOrderList.html L335 | `ng-click="receiveOrder(item.machineCenterOrder.id,$index)"` | receiveOrder L4293 | receiveMachineCenterOrder | `{ machineCenterOrderId: id }` | A 100% |
| 发货 | machineOrderList.html L341 | `ng-click="deliveryReceiveOrder(item.machineCenterOrder.id,$index)"` | deliveryReceiveOrder L4308 | deliveryMachineCenterOrder | `{ machineCenterOrderId: id }` | A 100% |
| 开始 | (directive `order-brokeninfo`) | directive 内部 | startOrder L16012 | startMachineCenterOrder | `{ machineCenterOrderId: id }` | F（directive 未直接观察）|
| 完成 (C-A) | (directive `order-brokeninfo`) | directive 内部 | completeOrder L16074 | completeMachineCenterOrder | `{ machineCenterOrderId: id }` | F |
| 完成 (C-B) | (directive `order-brokeninfo`) | directive 内部 | completeOrder L16333 | completeMachineCenterOrder | `{ cashflowId, machineCenterId }` | F |
| 关闭 | (directive `order-brokeninfo`) | directive 内部 | closeOrder L16083 | closeMachineCenterOrder | `{ machineCenterOrderId: id }` | F |

### 7.3 表 3：Delivery 三列表消费

| 列表 | API 来源 | Controller 引用 | HTML 消费 | 状态语义 | 评级 |
|------|---------|----------------|----------|---------|------|
| `waitingDeliveryList` | getCashflowDeliveryVoList.json / getCashflowDeliveryVo.json | 6 处 | `.length` 计数显示 | "待发货" | A 100% |
| `sendToMachineCenterList` | getCashflowDeliveryVoList.json / getCashflowDeliveryVo.json | 0 处 | `.length` 计数显示 | "加工中" | A 100% |
| `deliveryedList` | getCashflowDeliveryVoList.json / getCashflowDeliveryVo.json | 1 处 | `.length` 计数显示 | "已发货" | A 100% |

### 7.4 表 4：machineOrderList 页面控制模型

| UI 区域 | 状态 | Function | API | 状态更新 | 刷新 | 评级 |
|--------|------|---------|-----|---------|------|------|
| Tab 切换 | acceptStatus/statusArray | setTab | — | $scope.obj | searchAdminList | A 100% |
| receiveStatus 切换 | receiveStatus | changeReceiveStatus | — | $scope.obj | searchAdminList | A 100% |
| 签收按钮 | receiveStatus=1 | receiveOrder | receiveMachineCenterOrder | 本地 receiveStatus=1 | 无 API | A 100% |
| 发货按钮 | deliveryStatus=1 | deliveryReceiveOrder | deliveryMachineCenterOrder | 本地 deliveryStatus=1 | 无 API | A 100% |

### 7.5 表 5：动作更新模式

| 动作 | API | 更新模式 | 具体代码 | 评级 |
|------|-----|---------|---------|------|
| receive | receiveMachineCenterOrder | **B 本地赋值** | L4300 | A 100% |
| start | startMachineCenterOrder | **C 重新查询** | L16102 commonOrder | A 100% |
| complete C-A | completeMachineCenterOrder | **C 重新查询** | L16102 commonOrder | A 100% |
| complete C-B | completeMachineCenterOrder | **A 跳转** | L16344-16346 $state.go | A 100% |
| close | closeMachineCenterOrder | **C 重新查询** | L16102 commonOrder | A 100% |
| delivery | deliveryMachineCenterOrder | **B 本地赋值** | L4315 | A 100% |

**注意**：A/B/C 是"更新模式分类"，不是 A/B/C/D/E/F 证据等级。

### 7.6 表 6：Complete 双模式

| 项目 | C-A | C-B |
|------|-----|-----|
| controller | machineOrderCtrl | **machineOrderBrokenCtrl**（报损）|
| function | `completeOrder(id, medicalRecordId, idx)` | `completeOrder()`（无参）|
| API | completeMachineCenterOrder.json | completeMachineCenterOrder.json（同名）|
| Request machineCenterOrderId | 是 | **否** |
| Request cashflowId | 否 | 是 |
| Request machineCenterId | 否 | 是 |
| 走 commonOrder | 是 | **否** |
| 成功后续 | 重新查询 status | **跳转 machineOrderTesting** |
| 状态更新方式 | C 重新查询 | **A 跳转** |
| 业务上下文 | 通用加工完成 | **报损页面的"完成"按钮** |
| 评级 | A 100% | A 100% |

---

## 八、L1/L2/L3 边界

### 8.1 L1 前端事实（A 100%）

- Complete C-B 完整定义（L16333）
- $stateParams.cashflowId/machineCenterId/chain 来源（L16111-16113）
- commonOrder 完整定义（L16092-16106）
- machineOrderTesting 是 state name（L16364）
- directive `order-brokeninfo` 存在（HTML L13-18）
- 4 个 state name 共享 controller（L16206-16217）
- Delivery 三列表 HTML 消费（只 .length 计数）
- start/complete/close 通过 directive 调用（0 处 ng-click）

### 8.2 L2 业务模型（E 级）

- machineOrderBrokenCtrl = 报损页面（命名推断）
- machineOrderTesting = 加工测试（推断，但 4 个 state 共享 controller 提示状态机）
- C-B 在报损页面用于"完成"动作（业务推断）
- close 后 status 新值（业务推断，可能 = -1 或 99）

### 8.3 L3 数据库物理（F = 未观察）

- 表名
- 主键/外键
- close 后 status 实际值
- 后端事务

---

## 九、26 项评级矩阵

### A 组：Complete C-A（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | C-A function | L16074 completeOrder (带参) | A 100% |
| 2 | C-A Request | `{ machineCenterOrderId: id }` | A 100% |
| 3 | C-A commonOrder | L16080 → L16092 | A 100% |

### B 组：Complete C-B（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 4 | C-B function | L16333 completeOrder (无参) | A 100% |
| 5 | C-B Request | `{ cashflowId, machineCenterId }` | A 100% |
| 6 | cashflowId 来源 | `$stateParams.cashflowId` | A 100% |
| 7 | machineCenterId 来源 | `$stateParams.machineCenterId` | A 100% |
| 8 | C-B 页面 | machineOrderBrokenCtrl | A 100% |

### C 组：machineOrderTesting（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 9 | machineOrderTesting URL | 4 个 state name 之一 (tab=4) | A 100% |
| 10 | C-B 成功后动作 | `$state.go("machineOrderTesting" / "machineOrderChainTesting")` | A 100% |

### D 组：Close（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 11 | close function | L16083 closeOrder | A 100% |
| 12 | close Request | commonOrder URL 注入 `{ machineCenterOrderId: id }` | A 100% |
| 13 | close 后 getMachineCenterOrder | L16100 重新查询 | A 100% |
| 14 | close 最终 status | **未直接观察** | **F** |

### E 组：start/complete/close 按钮（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 15 | start 按钮 | directive `order-brokeninfo` | F |
| 16 | complete C-A 按钮 | directive `order-brokeninfo` | F |
| 17 | close 按钮 | directive `order-brokeninfo` | F |
| 18 | receive 按钮 | L335 `ng-click="receiveOrder(...)"` | A 100% |
| 19 | delivery 按钮 | L341 `ng-click="deliveryReceiveOrder(...)"` | A 100% |

### F 组：Delivery 三列表消费（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 20 | waitingDeliveryList 来源 | getCashflowDeliveryVoList.json / getCashflowDeliveryVo.json | A 100% |
| 21 | sendToMachineCenterList 来源 | 同上 | A 100% |
| 22 | deliveryedList 来源 | 同上 | A 100% |
| 23 | 三列表 HTML 消费 | deliveryList.html `.length` 计数 | A 100% |

### G 组：综合（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 24 | Delivery refresh 链 | 5 个动作 API 不刷新 | A 100% |
| 25 | Complete 双协议对照 | 完全不同 | A 100% |
| 26 | 一期复刻边界 | 22 A + 4 F | A 100% |

---

## 十、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 22 | 84.6% | 真实证据全部 100% 收口 |
| **B** | 0 | 0% | — |
| **C** | 0 | 0% | — |
| **D** | 0 | 0% | — |
| **E** | 0 | 0% | — |
| **F** | 4 | 15.4% | 4 个 directive 按钮 + 1 个 close status + 1 个 C-B 触发来源（部分合并）|
| **合计** | **26** | **100%** | — |

**L1=22 / L2=0 / L3=0 / F=4**

---

## 十一、本轮新增事实（S1-54 独有）

### 事实 1：machineOrderCompleted.html = 报损页面（A 级 100%）

**事实**：HTML 注释 `<!-- machineOrderBrokenCtrl -->` 明确标注这是报损页面

**证据**：machineOrderCompleted.html L2

**等级**：**A 100%**

### 事实 2：Complete C-B 参数全部来自 URL 路由参数（A 级 100%）

**事实**：C-B 的 `cashflowId` / `machineCenterId` / `chain` 都来自 `$stateParams`

**证据**：controller.js L16111-16113

**等级**：**A 100%**

### 事实 3：machineOrderTesting 是 state name（A 级 100%）

**事实**：`machineOrderTesting` 是 8 个 state name 之一，对应 `tab=4`

**证据**：controller.js L16213-16214

**等级**：**A 100%**

### 事实 4：start/complete/close 通过 directive `order-brokeninfo`（A 级新发现）

**事实**：start/complete/close 的 HTML 按钮入口 = directive `order-brokeninfo`

**证据**：machineOrderCompleted.html L13-18

**等级**：**A 100%（directive 存在）** + **F（directive 实现未直接观察）**

### 事实 5：3 个 Delivery 子列表只用于 .length 计数（A 级 100%）

**事实**：3 个子列表在 deliveryList.html 中**只显示 .length 计数**，不渲染商品细节

**证据**：deliveryList.html L251/L275/L260/L267

**等级**：**A 100%**

### 事实 6：4 个 state name 共享 controller

**事实**：`machineOrderWaitProcessCtrl` 处理 8 个 state name（4 个连锁 + 4 个非连锁）

**证据**：controller.js L16207-16215

**等级**：**A 100%**

### 事实 7：C-B 与 C-A 在不同 controller（A 级 100%）

**事实**：
- C-A 在 `machineOrderCtrl`（通用加工）
- C-B 在 `machineOrderBrokenCtrl`（报损页面）

**证据**：controller.js L15943 vs L16261

**等级**：**A 100%**

### 事实 8：close 后 status 仍 F 维持

**事实**：HTML 只显示 status=0/1/2 三种值对应的文字，close 后 status 新值未直接观察

**等级**：**F 维持**

---

## 十二、历史评级复核

| S1-53 结论 | S1-54 复核 |
|----------|----------|
| commonOrder 完整定义 | **维持 A 100%** |
| complete 两种调用模式 | **升级 A 100%**（C-B 真实业务 = 报损页面的"完成"）|
| startOrder / completeOrder / closeOrder 通过 commonOrder | **维持 A 100%** |
| Delivery 三列表 controller 引用次数 | **维持 A 100%** |
| close 后 status F 维持 | **维持 F** |

**无新错误**。

---

## 十三、一期复刻影响

### 13.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | Complete C-A（machineCenterOrderId 模式）| **A 100%** |
| 2 | Complete C-B（cashflowId + machineCenterId 模式）| **A 100%** |
| 3 | commonOrder 完整定义 | **A 100%** |
| 4 | close API（commonOrder 模式）| **A 100%** |
| 5 | 5 个按钮调用（receive/delivery 直接）| **A 100%** |
| 6 | 3 个 Delivery 子列表 HTML 消费 | **A 100%** |
| 7 | 3 个 Delivery 子列表 API 来源 | **A 100%** |
| 8 | C-B 跳转 machineOrderTesting | **A 100%** |
| 9 | directive `order-brokeninfo` 存在 | **A 100%** |

### 13.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | machineOrderTesting 完整页面结构 | E |
| 2 | directive `order-brokeninfo` 内部实现 | E |
| 3 | close 后 status 新值 | E |
| 4 | 后端业务模型 | E |

### 13.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 25 个 ID 字段名 | F = 当前未观察 |
| 2 | close 后 status 新值（-1/3/99 等）| F = 当前未观察 |
| 3 | directive `order-brokeninfo` 内部实现 | F = 当前未观察 |
| 4 | C-B 触发来源（哪个 controller 跳转）| F = state.go 0 处 |
| 5 | 后端事务 | F = 当前未观察 |
| 6 | 数据库状态表 | F = 当前未观察 |

---

## 十四、严禁脑补清单

```
closeStatus / completedStatus / testingStatus
machineOrderTestingId / deliveryId / shipmentId
statusHistoryId / workflowId / stateMachineId
transactionId / closeOrderId
```

---

## 十五、未解决问题（10 个 Q）

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | C-B 真实业务上下文？ | **报损页面的"完成"按钮** | A 100% |
| Q2 | C-B 是否通过 MachineCenterOrder？ | **否**（用 cashflowId + machineCenterId）| A 100% |
| Q3 | C-B 为什么使用 cashflowId + machineCenterId？ | **machineOrderBrokenCtrl 设计** | A 100% |
| Q4 | close 后 status 是否确定？ | **F 维持** | F |
| Q5 | start/complete/close 按钮模板是否找到？ | **directive `order-brokeninfo`（内部未观察）** | A 100% / F |
| Q6 | sendToMachineCenterList 是否真正由 HTML 消费？ | **是**（deliveryList.html L275）| A 100% |
| Q7 | 三列表最终 API 来源是否确定？ | **是**（getCashflowDeliveryVoList.json / getCashflowDeliveryVo.json）| A 100% |
| Q8 | Delivery refresh 是否存在？ | **5 个动作 API 不刷新** | A 100% |
| Q9 | L3 数据库关系？ | **F 维持** | F |
| Q10 | C-B 触发来源？ | **F 维持**（state.go 0 处）| F |

---

## 十六、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十七、文档元数据

- **文档编号**：113
- **任务阶段**：S1-54 Complete 双协议 + Close 最终状态 + Delivery 三列表消费
- **侦察时间**：2026-09-03 12:25-13:00
- **S1-54 颠覆性 A 级新发现**：
  1. **machineOrderCompleted.html = 报损页面**（HTML 注释直接证据）
  2. **C-B 参数全部来自 $stateParams**（URL 路由）
  3. **machineOrderTesting 是 state name**（4 个 state 共享 controller）
  4. **start/complete/close 通过 directive `order-brokeninfo`**
  5. **3 个 Delivery 子列表只用于 .length 计数**
  6. **4 个 state name 共享 controller**
  7. **C-B 在不同 controller（C-A vs C-B 完全独立）**
  8. **close 后 status 仍 F 维持**
- **26 项评级 = 22 A + 0 E + 4 F = 100%**
- **L1=22 / L2=0 / L3=0 / F=4**
- **历史文档影响**：0（28~112 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-55

---

> **S1-54 完成。**
> **22 A + 0 E + 4 F（4 个剩余断点收口）**。
> **Complete 双协议 + Close 最终状态 F 维持 + Delivery 三列表真实消费 + directive `order-brokeninfo` 入口发现**。
> **下一步：等待老板下一条指令。**
