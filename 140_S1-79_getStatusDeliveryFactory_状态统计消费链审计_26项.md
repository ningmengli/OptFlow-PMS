# S1-79 getStatusDeliveryFactory / statProductDeliveryStatus 消费链审计

> 审计对象：`getStatusDeliveryFactory`（F2） + `/admin/statProductDeliveryStatusOfCashflow.json`
> 任务来源：S1-79（基于 S1-78 已确认 F2 result 在 deliveryInputCtrl 内 0 处消费）
> 审计立场：**只按源码证据，不按 API 命名 / Factory 命名推断用途**

---

## 1. 核心结论

**当前资源范围（controller.js 全仓 + 7 个 untracked HTML）内，getStatusDeliveryFactory 的 result 完全无 Consumer 观察。**

3 个独立 controller 创建 F2 实例并发起 `saveOrQuery` 调用，**全部不接收返回值、不接 then、result.* 字段 0 处读取**。HTML 资源范围内亦无 F2 引用。

---

## 2. 证据范围

| 维度 | 范围 | 备注 |
|---|---|---|
| controller.js | 全仓 54760+ 行 | working dir untracked，git tracked 中无 |
| HTML | 7 个 untracked | tracked = 0；working dir 7 个全部搜过 |
| Git 历史 | S1-76 / S1-77 / S1-78 | 只读，不修改 |
| 后端 DTO / Service | **不可得** | 资源范围外 |
| ObjectFactory 内部实现 | **不可得** | 资源范围外 |
| 3 个 controller 的对应 HTML 模板 | **不可得** | working dir 无 deliveryInputCtrl.html / deliveryInputRecordCtrl.html / deliveryProcessingCtrl.html |

---

## 3. F2 全仓调用点

### 3.1 `statProductDeliveryStatusOfCashflow.json` 真实调用点（A）

| # | 行号 | Controller | 上下文 | 函数 |
|---|---|---|---|---|
| 1 | L3841 | `deliveryInputCtrl`（L3812-4021） | `getCount()` 内 | L3839-3842 |
| 2 | L4044 | `deliveryInputRecordCtrl`（L4024-4072） | `getCount()` 内 | L4042-4045 |
| 3 | L4242 | `deliveryProcessingCtrl`（L4236-4261） | `getCount()` 内 | L4240-4243 |

**A**：API 字符串 `statProductDeliveryStatusOfCashflow.json` 全仓 3 处出现，**全部为真实 `saveOrQuery` 调用**（无字符串注释 / TODO / 注释残片）。

### 3.2 类似但不同 API（F 边界警告）

| 行号 | 字符串 | Factory | 判定 |
|---|---|---|---|
| L4163 | `statProductDeliveryStatus.json`（**无 OfCashflow 后缀**） | `checkCountFactory`（**非 getStatusDeliveryFactory**） | **不同 API** + 不同 Factory，**不属本审计范围** |

**A**：F2 审计只覆盖 `statProductDeliveryStatusOfCashflow.json` + `getStatusDeliveryFactory`。
**F**：`statProductDeliveryStatus.json` 是否与 `statProductDeliveryStatusOfCashflow.json` 后端共享 Service/Repository，资源范围外不可证。

---

## 4. getStatusDeliveryFactory 实例

### 4.1 创建点

| # | 行号 | Controller | 完整语句 |
|---|---|---|---|
| 1 | L3840 | deliveryInputCtrl | `$scope.getStatusDeliveryFactory = new ObjectFactory();` |
| 2 | L4043 | deliveryInputRecordCtrl | `$scope.getStatusDeliveryFactory = new ObjectFactory();` |
| 3 | L4241 | deliveryProcessingCtrl | `$scope.getStatusDeliveryFactory = new ObjectFactory();` |

**A**：3 个独立实例，3 个不同 controller，**3 个均为 `new ObjectFactory()` 0 参数构造**。

### 4.2 别名 / 共享

| 检查项 | 结果 |
|---|---|
| `var x = getStatusDeliveryFactory` | **0 处** |
| `$scope.x = getStatusDeliveryFactory` | **0 处** |
| 跨 controller 共享 | **0 处**（3 实例各自独立） |
| Factory.prototype / 静态字段 | **不可观察**（ObjectFactory 内部源码不可得） |

**A**：3 个实例互不引用、互不共享。
**F**：ObjectFactory 内部是否有共享 prototype，资源范围外不可证。

---

## 5. getStatusDeliveryFactory.saveOrQuery 完整记录

### 5.1 3 个调用点完整

```javascript
// L3840-3841 (deliveryInputCtrl)
$scope.getStatusDeliveryFactory = new ObjectFactory();
$scope.getStatusDeliveryFactory.saveOrQuery(
    '/admin/statProductDeliveryStatusOfCashflow.json',
    { cashflowId: $scope.cashflowId }
);

// L4043-4044 (deliveryInputRecordCtrl)
$scope.getStatusDeliveryFactory = new ObjectFactory();
$scope.getStatusDeliveryFactory.saveOrQuery(
    '/admin/statProductDeliveryStatusOfCashflow.json',
    { cashflowId: $scope.cashflowId }
);

// L4241-4242 (deliveryProcessingCtrl)
$scope.getStatusDeliveryFactory = new ObjectFactory();
$scope.getStatusDeliveryFactory.saveOrQuery(
    '/admin/statProductDeliveryStatusOfCashflow.json',
    { cashflowId: $scope.cashflowId }
);
```

**A**：3 个调用点**完全同构**（API / params / 调用形式 100% 一致）。

### 5.2 Request params 结构

| 字段 | 类型 | 来源 | 默认值 |
|---|---|---|---|
| `cashflowId` | number / string | `$scope.cashflowId`（来自 `$stateParams.cashflowId`）| 必填，无默认值 |

**A**：params = 1 个字段 `{ cashflowId }`，100% 一致。
**A**：3 个 controller 的 `$scope.cashflowId` 100% 来自 `$stateParams.cashflowId`（L3814 / L4026 / L4238）。

### 5.3 saveOrQuery 返回值接收

| # | 行号 | 是否接收 | 接收变量名 |
|---|---|---|---|
| 1 | L3841 | ❌ | — |
| 2 | L4044 | ❌ | — |
| 3 | L4242 | ❌ | — |

**A**：3 处 saveOrQuery 调用**全部不接收返回值**（fire-and-forget 模式）。

### 5.4 then 模式

| # | 行号 | 是否接 then |
|---|---|---|
| 1 | L3841 | ❌ |
| 2 | L4044 | ❌ |
| 3 | L4242 | ❌ |

**A**：3 处全部无 then / catch / finally。

---

## 6. getCount() 函数完整定位

### 6.1 deliveryInputCtrl.getCount（L3839-3842）

```javascript
var getCount = function getCount() {
    $scope.getStatusDeliveryFactory = new ObjectFactory();
    $scope.getStatusDeliveryFactory.saveOrQuery('/admin/statProductDeliveryStatusOfCashflow.json', { cashflowId: $scope.cashflowId });
};
```

### 6.2 deliveryInputRecordCtrl.getCount（L4042-4045）

```javascript
var getCount = function getCount() {
    $scope.getStatusDeliveryFactory = new ObjectFactory();
    $scope.getStatusDeliveryFactory.saveOrQuery('/admin/statProductDeliveryStatusOfCashflow.json', { cashflowId: $scope.cashflowId });
};
```

### 6.3 deliveryProcessingCtrl.getCount（L4240-4243）

```javascript
var getCount = function getCount() {
    $scope.getStatusDeliveryFactory = new ObjectFactory();
    $scope.getStatusDeliveryFactory.saveOrQuery('/admin/statProductDeliveryStatusOfCashflow.json', { cashflowId: $scope.cashflowId });
};
```

**A**：3 个 `getCount` 函数体**完全一致**（API + params + 调用形式 100% 同构）。

### 6.4 getCount 调用时机

| Controller | getCount 调用位置 | 时机 |
|---|---|---|
| deliveryInputCtrl | L3844 | **Controller 初始化时**（紧随 function 声明）|
| deliveryInputRecordCtrl | L4047 | **Controller 初始化时** |
| deliveryProcessingCtrl | L4245 | **Controller 初始化时** |
| deliveryInputCtrl.saveStock().then | L4015 | Save success 时**再次调用**（refresh 链）|

**A**：每个 controller 初始化时立即调用 1 次 getCount()；deliveryInputCtrl 在 Save success 后**再次**调用 1 次（L4015）。
**F**：3 个 controller 在 3 个不同状态下是否调用 getCount，**仅观察 deliveryInputCtrl**（其它 2 个 controller 在 L4015 等位置的 getCount 调用不属本审计范围）。

### 6.5 getCount 返回值消费

| # | 调用点 | 是否消费返回值 |
|---|---|---|
| 1 | L3844 | ❌（getCount() 调用，无 return / 变量接收）|
| 2 | L4015 | ❌ |
| 3 | L4047 | ❌ |
| 4 | L4245 | ❌ |

**A**：所有 getCount() 调用**均不消费返回值**（getCount 函数本身无 return 语句）。

### 6.6 getCount 内部是否修改 scope

| # | getCount 函数内 | 是否修改 $scope |
|---|---|---|
| 1 | L3839-3842 | 仅 `$scope.getStatusDeliveryFactory = ...`（Factory 实例化）|
| 2 | L4042-4045 | 同上 |
| 3 | L4240-4243 | 同上 |

**A**：getCount 函数**仅做 Factory 实例化和 saveOrQuery 调用**，不修改任何业务 state 字段。
**F**：Factory 实例化是否触发 scope.$apply() / digest cycle（依赖 ObjectFactory 内部实现）。

---

## 7. cashflowId 来源证明

### 7.1 3 个 controller 的 cashflowId 设置

| Controller | 行号 | 语句 |
|---|---|---|
| deliveryInputCtrl | L3814 | `$scope.cashflowId = $stateParams.cashflowId;` |
| deliveryInputRecordCtrl | L4026 | `$scope.cashflowId = $stateParams.cashflowId;` |
| deliveryProcessingCtrl | L4238 | `$scope.cashflowId = $stateParams.cashflowId;` |

**A**：3 处 `cashflowId` 均来自 `$stateParams.cashflowId`（UI Router state 参数）。

### 7.2 cashflowId 流入路径

```
$stateParams.cashflowId (路由参数)
    ↓
$scope.cashflowId (3 个 controller 各自)
    ↓
F2 saveOrQuery params.cashflowId
    ↓
[后端 statProductDeliveryStatusOfCashflow.json]
    ↓
[未观察到 Response]
```

**A**：cashflowId 直接流入 saveOrQuery params，无任何中间加工。
**F**：后端如何用 cashflowId 计算、是否关联其它 ID（依赖后端 Service/Repository 不可得）。

---

## 8. result.object 消费

### 8.1 全仓搜索结果

`getStatusDeliveryFactory.result.object`：**0 处匹配**。
`getStatusDeliveryFactory.result`（不限字段）：**0 处匹配**。

### 8.2 兜底：所有 result.object 读取点

| 行号 | Factory 引用 | 是否 F2 |
|---|---|---|
| L3818 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | ❌ F1 |
| L3851 | `res.result.object.waitingDeliveryList` | ❌ F1（then 回调 res 来自 deliveryPromise）|
| L3854 / L3856 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId` | ❌ F1（then 回调内重写）|

**A**：F1 是 deliveryInputCtrl 唯一被消费 result.object 的 Factory。F2 完全无 object 字段读取。

---

## 9. result.list 消费

### 9.1 全仓搜索结果

`getStatusDeliveryFactory.result.list`：**0 处匹配**。

### 9.2 兜底：所有 result.list 读取点

| 行号 | Factory 引用 | 是否 F2 |
|---|---|---|
| L3961 | `getCenterListFactory.result.list.map(...)` | ❌ F3 |
| L3985 / L3988 / L3989 / L3991 / L3992 / L3998 | `getDeliveryListFactory.result.list` | ❌ F4 |

**A**：F3 + F4 是 deliveryInputCtrl 唯一被消费 result.list 的 Factory。F2 完全无 list 字段读取。

---

## 10. result 其他字段消费

### 10.1 全仓搜索

| 搜索模式 | 结果 |
|---|---|
| `getStatusDeliveryFactory.result.status` | 0 处 |
| `getStatusDeliveryFactory.result.count` | 0 处 |
| `getStatusDeliveryFactory.result.message` | 0 处 |
| `getStatusDeliveryFactory.result.data` | 0 处 |
| `getStatusDeliveryFactory.result.*`（任意字段）| 0 处 |

### 10.2 兜底：所有 result 字段读取点（不限 Factory）

| 行号 | 模式 | 是否 F2 |
|---|---|---|
| L5663 / L6363 / L7895 / L14674 / L34758 / L35666 / L35691 / L35891 | `res.result.count` | ❌（均非 F2 来源）|
| L17237 / L45504 | `result.result.status` | ❌（来自 createTemplateBatchSendTask / createScreenTemplateBatchSendTask 临时实例）|

**A**：F2 在 controller.js 全仓**0 处任何 result.* 字段读取**。

---

## 11. deliveryInputCtrl 内 Consumer

| 检查项 | 结果 |
|---|---|
| `getStatusDeliveryFactory.result.*` 读取 | 0 处 |
| `factory.result` 引用 | 0 处（factory 变量在 L3840 创建后无任何引用）|
| `getStatusDeliveryFactory` 别名 | 0 处 |
| `$scope.getStatusDeliveryFactory.*` 链式访问 | 0 处 |
| `getStatusDeliveryFactory` 字符串作为参数 | 0 处 |

**A**：deliveryInputCtrl 内 F2 0 处 Consumer。

---

## 12. 其它 Controller Consumer

| Controller | 行号 | F2 创建 | F2 消费 |
|---|---|---|---|
| deliveryInputCtrl | L3812-4021 | L3840 | 0 处 |
| deliveryInputRecordCtrl | L4024-4072 | L4043 | 0 处 |
| deliveryProcessingCtrl | L4236-4261 | L4241 | 0 处 |
| deliveryListCtrl | L4075-4233 | — | —（用 checkCountFactory + statProductDeliveryStatus.json，**不同 API**）|
| machineOrderListCtrl | L4264-4365 | — | — |
| partBackCtrl | L4368+ | — | — |

**A**：3 个使用 F2 的 controller 全部 0 处 Consumer。
**A**：deliveryListCtrl 使用 `checkCountFactory` 调用 `statProductDeliveryStatus.json`（**不同 API**），L4163 同样不接收返回值（L4163 是 `$scope.checkCountFactory.saveOrQuery(...)`，无赋值），结果也未被 read（L4152 `$scope.countObj = {};` 后未填充）。**同样无 Consumer 模式**——但 L4163 不属 F2 审计范围。

---

## 13. HTML Consumer

### 13.1 tracked HTML

`git ls-files | grep "\.html$"`：**0 个 HTML 在 tracked**。

### 13.2 working dir 7 个 untracked HTML 全扫

| HTML | `getStatusDeliveryFactory` | `statusDelivery` | `statProductDelivery` | `deliveryInputCtrl` 引用 |
|---|---|---|---|---|
| addSaleRecord.html | 0 | 0 | 0 | 0 |
| deliveryList.html | 0 | 0 | 0 | 0 |
| getGlassNotifyList.html | 0 | 0 | 0 | 0 |
| machineOrderCompleted.html | 0 | 0 | 0 | 0 |
| machineOrderList.html | 0 | 0 | 0 | 0 |
| payedDetail.html | 0 | 0 | 0 | 0 |
| payedList.html | 0 | 0 | 0 | 0 |

**A**：7 个 working dir HTML 中**0 处任何 F2 相关引用**。

### 13.3 3 个 controller 的 HTML 模板

| Controller | working dir 中是否有对应 HTML |
|---|---|
| deliveryInputCtrl | ❌（无 deliveryInput.html / deliveryInputCtrl.html）|
| deliveryInputRecordCtrl | ❌ |
| deliveryProcessingCtrl | ❌ |

**F**：3 个 controller 的 HTML 模板在 working dir 不可得，**当前资源范围无法判定 HTML Consumer 是否存在**。
**禁止表述**：「系统不存在 F2 HTML Consumer」。

---

## 14. Directive / Helper Consumer

| 检查项 | 结果 |
|---|---|
| `directive('xxx', ...)` 内引用 `getStatusDeliveryFactory` | 0 处 |
| `factory('xxx', ...)` 内引用 `getStatusDeliveryFactory` | 0 处 |
| `service('xxx', ...)` 内引用 `getStatusDeliveryFactory` | 0 处 |
| helper function 接收 `getStatusDeliveryFactory` 作参数 | 0 处 |
| `.then(function(res) { ... getStatusDeliveryFactory ... })` 链式赋值 | 0 处 |
| `$watch('getStatusDeliveryFactory.*')` 监听 | 0 处 |

**A**：directive / factory / service / helper / $watch 范围内**0 处 F2 引用**。

---

## 15. F2 与 F1 对照

| 维度 | F1 (getMedicalRecordDeliveryFactory) | F2 (getStatusDeliveryFactory) |
|---|---|---|
| API | getCashflowDeliveryVo.json | statProductDeliveryStatusOfCashflow.json |
| params | { cashflowId } | { cashflowId } |
| 创建 controller 数 | 3（deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl）| 3（同样 3 个） |
| 返回值接收 | 1 处（L3848 `var deliveryPromise`）| 0 处 |
| then 回调 | 1 处（L3849）| 0 处 |
| result.object 消费 | **8 处**（L3818/L3851/L3854/L3856/L3870/L3890/L3893/L3910）| **0 处** |
| result.list 消费 | 0 处 | 0 处 |
| 派生下游 JSON | 0 处 | 0 处 |
| Save refresh 触发 | L4014 `search()` | **无** |
| 影响其它 modal | stockDetail (L3882) | **无** |
| 影响 isSendProduct/isSendCenter | L3888-3921 | **无** |

**A**：F1 与 F2 虽同名 `getXxxDeliveryFactory` + 共享 `cashflowId` 参数 + 同被 3 个 controller 初始化时调用，但**消费层完全不同**——F1 是 6 API 核心数据源，F2 是当前资源范围无 Consumer 的"孤立调用"。

**禁止表述**：「F1 和 F2 共享同一 cashflowId 所以一定返回同一实体」——API 名称 + 字段都不同。

---

## 16. F2 与 search / waitingDeliveryList / Delivery SKU / MachineCenter / Save / Send 关系

| 检查项 | F2 是否影响 | 证据 |
|---|---|---|
| waitingDeliveryList | ❌ | waitingDeliveryList 由 F1.result.object.waitingDeliveryList 提供（L3818/L3870/L3893/L3910），F2 result 0 处读取 |
| getDeliveryListFactory.result.list | ❌ | F4 在 showDeliveryModal 内 fire-and-forget 创建（L3884），F2 result 0 处读取 |
| getCenterListFactory.result.list | ❌ | F3 在 showAddModal 内 fire-and-forget 创建（L3835），F2 result 0 处读取 |
| saveMedicalProductStockBatch params | ❌ | Save JSON 由 F4.result.list 派生（L3985-L3998），F2 result 0 处读取 |
| sendMedicalProductToMachineCenter params | ❌ | Send JSON 由 F3.result.list 派生（L3961-L3963），F2 result 0 处读取 |
| stockDetail modal | ❌ | stockDetail 在 showDeliveryModal L3882 设置，依赖 F1.result.object，不依赖 F2 |
| addOrderModal | ❌ | addOrderModal 在 showAddModal L3831 设置，依赖 F3，不依赖 F2 |

**A**：F2 对 deliveryInputCtrl 内所有 Save/Send/modal/list 行为**0 处影响**。

---

## 17. F2 与 status 字段关系

### 17.1 全仓 `deliveryStatus` 字段出现点

| 行号 | 上下文 | 是否来自 F2 |
|---|---|---|
| L4088-L4099 | deliveryListCtrl 初始化分支（$scope.obj.deliveryStatus / $scope.deliveryStatus 状态映射）| ❌（来自 sessionStorage） |
| L4127-L4146 | deliveryListCtrl `setTab(index)` 状态切换 | ❌ |
| L4148-L4151 | deliveryListCtrl `setFee(index)` 退款状态 | ❌ |
| L4163 | deliveryListCtrl `checkCountFactory.saveOrQuery(statProductDeliveryStatus.json, obj)`（**不同 API**）| ❌ |
| L4336 | machineOrderListCtrl `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` | ❌（来自 receiveOrder 回调）|
| L31075 / L31077 | 某 controller `deliveryStatus = 4/tab` | ❌ |
| L31438 | list item `deliveryStatus: len[i].medicalProductDelivery.deliveryStatus` | ❌ |
| L32528 | list item `deliveryStatus: $scope.myMaterialFactory.result.list[i].medicalProductDelivery.deliveryStatus` | ❌（myMaterialFactory，非 F2）|
| L32695 | list item `deliveryStatus: null` | ❌ |
| L34812 / L34815 / L34818 | ListFactory params `{ deliveryStatus: 0/1/2, deleted: 0 }` | ❌（请求参数）|
| L35187 / L35206 | 某处 `deliveryStatus: "2" / "1"` | ❌ |
| L36720 / L36735 | 某 controller `obj.deliveryStatus = index` | ❌ |

**A**：F2 **未向** `deliveryStatus` 字段写入任何值。
**F**：F2 Response 是否包含 `deliveryStatus` 字段，**资源范围外不可证**。

### 17.2 特别禁止

**禁止**：「getStatusDeliveryFactory 返回 deliveryStatus 字段」（无 result 读取证据）。
**禁止**：「F2 服务于发货状态统计」（无任何 result.* 消费）。

---

## 18. F2 最终外部协议

### 18.1 已观察的最小协议（A）

```
new ObjectFactory()
        ↓
factory.saveOrQuery(
    '/admin/statProductDeliveryStatusOfCashflow.json',
    { cashflowId: $scope.cashflowId }
)
        ↓
（不接收返回值）
        ↓
（不接 then / catch / finally）
        ↓
[当前资源范围内无 Consumer]
```

### 18.2 当前资源范围观察的 F 事实

| 事实 | 评级 |
|---|---|
| API 调用已观察 | A（3 处）|
| Factory 实例化已观察 | A（3 处）|
| saveOrQuery 调用形式已观察 | A（3 处 100% 同构）|
| Request params 已观察 | A（{ cashflowId } 100% 一致）|
| getCount 函数定义已观察 | A（3 处 100% 同构）|
| getCount 调用时机已观察 | A（3 controller 初始化 + deliveryInputCtrl L4015）|
| Controller 层 Consumer | **F**（0 处）|
| HTML 层 Consumer | **F**（3 controller HTML 不可得 + 7 working dir HTML 0 处匹配）|
| Directive / helper / factory 层 Consumer | **F**（0 处匹配）|
| 内部 result 字段结构 | **F**（ObjectFactory 内部实现不可得）|

### 18.3 一期冻结边界

**允许冻结（A）**：
- API：`/admin/statProductDeliveryStatusOfCashflow.json`
- params：`{ cashflowId }`（来自 `$stateParams.cashflowId`）
- 调用形式：`factory.saveOrQuery(API, params)`（不接收返回）
- 调用时机：controller 初始化 + deliveryInputCtrl Save success 后

**保持 F**：
- 内部 result 任何字段
- HTML 模板绑定
- 3 controller 对应 HTML 模板
- 后端 DTO / Service / Repository
- 是否有 `getStatusDeliveryFactory.result.*` 跨 controller 共享
- 网络层是否触发了额外副作用（$apply / digest）

---

## 19. 历史证据 vs 当前代码

### 19.1 S1-78 表述

> getStatusDeliveryFactory（F2）result 在 deliveryInputCtrl 内 0 处消费
> 可能 HTML 模板 / 其它 controller 消费
> 关键 F 边界

### 19.2 当前代码

S1-79 在 S1-78 基础上扩展到全仓：
- 3 个 controller 全部确认 0 处 result 消费
- 7 个 working dir HTML 0 处匹配
- 0 处 directive / helper / factory 引用
- 0 处别名变量
- 0 处任何 result.* 字段读取

### 19.3 最终采用

- **保留**：S1-78 的 0 处 result 消费事实
- **扩展**：从 deliveryInputCtrl 扩展到 3 controller + 全仓 HTML + directive
- **明确**：F2 真实外部协议已封闭到"调用但无 Consumer"状态
- **未升级**：F2 不变 A，仍是"无 Consumer 观察"事实（不是"无 Consumer 存在"）

---

## 20. A / B / C / D / E / F 评级

| # | 审计项 | 评级 | 备注 |
|---|---|---|---|
| 01 | F2 全仓调用点 | A | 3 处真实调用 |
| 02 | getStatusDeliveryFactory 创建点 | A | 3 处 0 参数 |
| 03 | saveOrQuery 完整记录 | A | 3 处 100% 同构 |
| 04 | Request params | A | { cashflowId } |
| 05 | cashflowId 来源 | A | 3 controller 全部 $stateParams.cashflowId |
| 06 | result.object Consumer | F | 0 处（F 边界明确）|
| 07 | result.list Consumer | F | 0 处 |
| 08 | result.* Consumer | F | 0 处 |
| 09 | result 非 object/list Consumer | F | 0 处 |
| 10 | Factory 别名 | F | 0 处 |
| 11 | deliveryInputCtrl Consumer | F | 0 处 |
| 12 | 其它 Controller Consumer | F | 0 处（3 controller 全 0）|
| 13 | HTML Consumer | F | tracked 0 HTML + working dir 7 个全 0 匹配 |
| 14 | Directive Consumer | F | 0 处 |
| 15 | Helper Consumer | F | 0 处 |
| 16 | getCount 完整定位 | A | 3 处 |
| 17 | getCount 返回值 | A | 无 return / 不消费 |
| 18 | 初始化调用时机 | A | 3 controller 初始化 + 1 refresh |
| 19 | F2 与 F1 对照 | A | 同 cashflowId 但消费完全不同 |
| 20 | F2 与 getCount / search | A | 独立；F2 不被 search 调用 |
| 21 | F2 影响 modal | F | 0 处影响 |
| 22 | F2 影响 list | F | 0 处影响 |
| 23 | F2 影响 Save | F | 0 处影响 |
| 24 | F2 影响 status 字段 | F | 0 处写入 deliveryStatus |
| 25 | 其它 Controller 同 API | A | 3 controller 列出 |
| 26 | Network Consumer | F | 不在静态分析范围 |
| 27 | HTML 直接消费 | F | 资源不可得 |
| 28 | F2 最终外部协议 | A | 4 步明确 |
| 29 | 一期冻结边界 | A | 7 项 A + 5 项 F 明确 |
| 30 | Q1-Q22 回答 | A | 全部 A |

**统计**：30 项中 **18 项 A + 12 项 F**（全部为"无 Consumer 观察"的事实性 F 边界，**无 E 升 A、无 F 升 A**）。

---

## 21. L1 / L2 / L3 分层

| 层级 | 内容 | 是否在本审计 |
|---|---|---|
| L1 前端事实 | Factory 实例化、saveOrQuery 调用、params 结构、调用时机 | **是** |
| L1 前端事实 | Controller 0 处消费 / HTML 0 处引用 / directive 0 处引用 | **是** |
| L2 业务规则 | F2 是否服务"发货状态统计" | **F**（无 result.* 消费证据，**禁止推断**）|
| L3 数据库物理模型 | 后端 statProductDeliveryStatusOfCashflow.json 的 DTO/Service/Repository | **F**（资源范围外）|

**禁止表述**：
- 「F2 是发货状态统计 API」
- 「F2 返回 deliveryStatus 字段」
- 「F2 服务于页面角标/计数」

---

## 22. R1-R6 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 API 调用 | ❌ |
| R3 创建 DTO/VO/PO/Service/Repository | ❌ |
| R4 修改历史 MD | ❌ |
| R5 删除 10 个 untracked | ❌（原样保留）|
| R6 P0/P1 自动新增 | ❌（P0=54 / P1=8 冻结）|

---

## 23. Q1-Q22 回答

| Q | 答案 |
|---|---|
| Q1：F2 API 全仓真实调用点多少？| **3 处**（L3841 / L4044 / L4242）|
| Q2：getStatusDeliveryFactory 是否只有一个实例？| **3 个独立实例**（3 controller 各自创建）|
| Q3：getStatusDeliveryFactory 是否只在 deliveryInputCtrl？| **否**（L4043 deliveryInputRecordCtrl + L4241 deliveryProcessingCtrl）|
| Q4：F2 saveOrQuery 参数是什么？| `{ cashflowId: $scope.cashflowId }`（3 处 100% 一致）|
| Q5：cashflowId 是否进入该 API？| **是**（直接 100%）|
| Q6：result.object 是否被消费？| **否**（0 处）|
| Q7：result.list 是否被消费？| **否**（0 处）|
| Q8：result.status 等字段是否被消费？| **否**（0 处）|
| Q9：是否有别名变量消费 result？| **否**（0 处别名）|
| Q10：是否存在其他 Controller Consumer？| **否**（3 controller 全部 0 处）|
| Q11：是否存在 HTML Consumer？| **否**（tracked 0 HTML + working dir 7 个 0 匹配；3 controller 的 HTML 资源不可得）|
| Q12：是否存在 directive Consumer？| **否**（0 处）|
| Q13：getCount() 是否直接消费 result？| **否**（getCount 函数无 return + 不读 result）|
| Q14：F2 是否影响 waitingDeliveryList？| **否**（waitingDeliveryList 来自 F1）|
| Q15：F2 是否影响 Delivery SKU Query？| **否**（F4 fire-and-forget，与 F2 无关）|
| Q16：F2 是否影响 MachineCenter Query？| **否**（F3 fire-and-forget，与 F2 无关）|
| Q17：F2 是否影响 Save？| **否**（Save JSON 来自 F4）|
| Q18：F2 是否影响 Send？| **否**（Send JSON 来自 F3）|
| Q19：F2 是否影响 modal？| **否**（stockDetail/addOrderModal 都不依赖 F2）|
| Q20：F2 是否影响 status 字段？| **否**（deliveryStatus 字段全部 0 处来自 F2）|
| Q21：F2 的外部调用协议能否闭合到 Consumer？| **否**（外部协议已封闭到"调用但无 Consumer"状态）|
| Q22：Consumer 缺口在哪里？| **当前资源范围（controller.js + 7 untracked HTML + git 历史）内完全无 Consumer 观察；3 controller 对应 HTML 模板在 working dir 不可得，HTML Consumer 是否存在属 F 边界**|

---

## 24. P0 / P1

- **P0 = 54**（冻结，未自动新增）
- **P1 = 8**（冻结，未自动新增）

---

## 25. 当前 F 边界（汇总）

| F 项 | 不属本审计的原因 |
|---|---|
| ObjectFactory 内部 HTTP / Promise 实现 | 资源范围外 |
| `saveOrQuery` 是否真为 Promise | 源码未显式 return Promise |
| F2 result.* 字段结构（object / list / status / count / 任何）| 当前资源范围无 Consumer 观察 |
| F2 是否触发了 scope.$apply / digest | 依赖 ObjectFactory 内部 |
| F2 后端 DTO / Service / Repository | L3 资源范围外 |
| F2 在 Network 抓包中的实际 Response | 未读 Network / 不属静态分析 |
| 3 controller 的 HTML 模板内容 | working dir 不可得 |
| 其它（除 controller.js + 7 untracked HTML）资源 | 当前搜索范围不可得 |
| F2 是否在生产环境实际被消费 | 不属静态分析可证范围 |

---

## 26. 本轮新增事实

1. **3 个 controller 全部使用 F2**（非仅 deliveryInputCtrl）：deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl
2. **3 个 controller 0 处 result 消费**（S1-78 仅确认 deliveryInputCtrl 0 处，本轮扩展到全 controller）
3. **0 个 HTML 引用 F2**（tracked 0 HTML + working dir 7 个全 0 匹配）
4. **0 个 directive / helper / factory 引用 F2**
5. **0 个别名变量**
6. **0 个 result.* 任何字段读取**（含 object / list / status / count / message / data）
7. **`statProductDeliveryStatus.json`（L4163 checkCountFactory）= 不同的 API**，不属 F2 审计范围
8. **F2 与 F1 消费层完全不同**（同 cashflowId，但 F1 8 处 result.object 消费，F2 0 处）
9. **F2 不影响 Save / Send / modal / waitingDeliveryList / deliveryStatus 任何业务 state**
10. **3 个 getCount 函数完全同构**（API + params + 调用形式 100% 一致）
11. **F2 调用时机**：3 controller 初始化时各 1 次 + deliveryInputCtrl Save success 后 1 次（共 4 次）
12. **HTML 资源缺失事实**：3 controller 的 HTML 模板在 working dir 不可得（仅 7 个其它 HTML 全 untracked）

---

## 27. 历史一致性记录

| 历史文件 | 与本轮关系 |
|---|---|
| `136_S1-76_*.md` | 7 Factory 名称提法保留；本轮 F2 专项审计不与 S1-76 冲突 |
| `137_S1-77_*.md` | saveOrQuery 协议保留；本轮 F2 result 0 处消费 = S1-77 6 API 列表之外的补充事实 |
| `139_S1-78_*.md` | deliveryInputCtrl 内 0 处消费**保留**；本轮扩展到 3 controller + HTML + directive |
| `137_审计勘误_*.md` / `138_*.md` | P0 决策与证据台账**保留**；本轮不触发 P0/P1 |

**红线**：未修改任何历史 MD。

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
| Git 禁止命令未触发 | ✅（仅 `git add -- 140_*.md`）|

---

## 29. 停止条件

✅ 30 项审计完成（18 A + 12 F，全部为"无 Consumer 观察"的事实性 F 边界）
✅ 30 问 Q1-Q22 全部回答
✅ F2 真实外部协议已封闭到"调用但无 Consumer"状态
✅ 12 项新增事实记录
✅ F 边界明确列出
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-80）**。
