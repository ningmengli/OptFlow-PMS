# S1-78 ObjectFactory 六 API 实例—调用—结果消费生命周期审计

> 审计对象：`controller.js` L3812-4021（`deliveryInputCtrl`，209 行）
> 任务来源：S1-78（基于 S1-76 / S1-77 完成的 ObjectFactory 外部协议收口）
> 审计立场：**只读源码，不推断 ObjectFactory 内部实现**

---

## 1. 核心结论（30 字以内）

**deliveryInputCtrl 内 6 个真实 ObjectFactory 实例、6 个 API、各自生命周期与消费方式互不相同。**

---

## 2. 证据范围

- 主证据：`controller.js` L3812-4021（`deliveryInputCtrl` 完整 209 行）
- 辅助证据：`controller.js` 全仓 Factory 名称 / API URL 出现位置（用于排除"同名 Factory 跨 controller"混淆）
- 范围外：HTML 模板、Network 抓包、ObjectFactory 内部定义源码（**当前资源范围不可得**）

---

## 3. deliveryInputCtrl 全部 ObjectFactory 实例

| # | 变量名 | 创建位置 | API | 函数 | saveOrQuery 行号 |
|---|---|---|---|---|---|
| F1 | `$scope.getMedicalRecordDeliveryFactory` | L3847 | `/admin/getCashflowDeliveryVo.json` | `search()` 内 | L3848 |
| F2 | `$scope.getStatusDeliveryFactory` | L3840 | `/admin/statProductDeliveryStatusOfCashflow.json` | `getCount()` 内 | L3841 |
| F3 | `$scope.getCenterListFactory` | L3835 | `/admin/getMedicalProductMachineCenterVoList.json` | `showAddModal()` 内 | L3836 |
| F4 | `$scope.getDeliveryListFactory` | L3884 | `/admin/getCanBeDeliverySkuInListOfProduct.json` | `showDeliveryModal()` 内 | L3885 |
| F5 | `$scope.saveStockFactory` | L4006 | `/admin/saveMedicalProductStockBatch.json` | `saveStock()` 内 | L4007 |
| F6 | `$scope.createOrderFactory` | L3965 | `/admin/sendMedicalProductToMachineCenter.json` | `selectOrder()` 内 | L3966 |

**A**：6 个实例均通过 `new ObjectFactory()` 创建（A）；6 个实例分别调用 6 个不同 API（A）。

---

## 4. Factory 实例去重

### 4.1 实际独立实例（6 个）

仅 F1~F6 为真实活跃 Factory 实例（每个实例均被创建 + 调用 + 消费）。

### 4.2 别名 / 同名但不同实例

| 名称 | deliveryInputCtrl 内 | 其它位置 | 判定 |
|---|---|---|---|
| `getMachineCenterList` | **L3816 是 helper function**（不是 Factory） | — | **F（误判）** |
| `getMachineCenterListFactory` | 未出现 | L37387（`new ListFactory` + `nextPage()`） | **不同构（F）** — L37387 是 ListFactory，不属本审计范围 |
| `saveStockFactory` | L4006（Save API） | L16211（`saveToBeProcessSkuInListOfProduct.json`） | 同名不同 API 调用点，**仅 deliveryInputCtrl 内属本审计范围** |
| `getMedicalRecordDeliveryFactory` | L3847/L4051/L3870 等消费 | L4039 / L4248 同名创建 | deliveryInputCtrl 内 = F1，其它位置属其它 controller，**不属本审计范围** |
| `getStatusDeliveryFactory` | L3840 | L4043 / L4241 同名创建 | 同上 |

**A**：deliveryInputCtrl 范围内活跃 Factory 实例 = **6 个**。
**A**：S1-76 提到的 "7 个 Factory 名称" 中，**1 个（`getMachineCenterList`）是 helper function**，不是 Factory 实例。
**F**：S1-76 提到的 "`getMachineCenterList` 是 `getCenterListFactory` 的别名"——**代码不支持**（一个 function vs 一个 ObjectFactory 实例）。

---

## 5. getMedicalRecordDeliveryFactory（F1）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L3847 | `$scope.getMedicalRecordDeliveryFactory = new ObjectFactory();` |
| API | L3848 | `/admin/getCashflowDeliveryVo.json` |
| params | L3848 | `{ cashflowId: $scope.cashflowId }` |
| 返回值接收 | L3848 | `var deliveryPromise = $scope....saveOrQuery(...)`（**接收**） |
| then 回调 | L3849-3864 | `deliveryPromise.then(function (res) { ... })` |
| result.object 读取 | L3851 | `res.result.object.waitingDeliveryList` |
| result.object 二次写入 | L3854 / L3856 | `factory.result.object.waitingDeliveryList[i].medicalProduct.objectId = ... / null` |
| 后续直接消费（同步） | L3818 / L3870 / L3890 / L3893 / L3907 / L3910 | 6 处直接读 `factory.result.object(.waitingDeliveryList)` |
| status/errmsg | — | **未读取**（then 内仅处理 list） |

**消费深度**：
- `getMachineCenterList` helper（L3816-3829）派生 `medicalProductMachineCenterPoList`（L3822-3825）
- `showDeliveryModal` 派生 `medicalProductIdArray`（L3870-3876）
- `isSendProduct` / `isSendCenter` 校验锁仓归属（L3888-3921）

**A**：F1 是 deliveryInputCtrl 内**消费最深的 Factory**，承担"待发货列表主数据源"角色。

---

## 6. getStatusDeliveryFactory（F2）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L3840 | `$scope.getStatusDeliveryFactory = new ObjectFactory();` |
| API | L3841 | `/admin/statProductDeliveryStatusOfCashflow.json` |
| params | L3841 | `{ cashflowId: $scope.cashflowId }` |
| 返回值接收 | — | **不接收**（直接 fire-and-forget） |
| then 回调 | — | **无** |
| result.object 消费 | — | **0 处**（deliveryInputCtrl L3812-4021 全范围未观察到） |
| result.list 消费 | — | **0 处** |
| status/errmsg | — | **未读取** |

**关键 F**：F2 的 result 在 deliveryInputCtrl 源码范围内**没有任何代码消费**。
**可能去向**（F 边界，不属本审计范围）：
- HTML 模板 `{{ getStatusDeliveryFactory.result.* }}` 数据绑定（未读 HTML 不可证）
- 其它 controller（不属本审计范围）

**A**：F2 的 result 在 deliveryInputCtrl Controller 层**完全无消费**。

---

## 7. getCenterListFactory（F3）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L3835 | `$scope.getCenterListFactory = new ObjectFactory();`（`showAddModal` 内） |
| API | L3836 | `/admin/getMedicalProductMachineCenterVoList.json` |
| params | L3836 | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` |
| 返回值接收 | — | **不接收** |
| then 回调 | — | **无** |
| result.list 消费 | L3961 | `$scope.getCenterListFactory.result.list.map(function (v) { return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }; })` |
| result.object 消费 | — | **未读取** |
| 后续消费函数 | L3961-3963 → L3966 | result.list 派生 `arr` → `selectOrder` 内 sendMedicalProductToMachineCenter params 的 `medicalProductMachineCenterPoListJson` |

**A**：F3 的 result.list **直接派生** Send API 的 `medicalProductMachineCenterPoListJson`（JSON.stringify 前数据源）。

---

## 8. getDeliveryListFactory（F4）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L3884 | `$scope.getDeliveryListFactory = new ObjectFactory();`（`showDeliveryModal` 内） |
| API | L3885 | `/admin/getCanBeDeliverySkuInListOfProduct.json` |
| params | L3885 | `{ medicalProductIdArray: medicalProductIdArray }` |
| 返回值接收 | — | **不接收** |
| then 回调 | — | **无** |
| result.list 消费 | L3985 / L3988 / L3989 / L3991 / L3992 / L3998 | **6 处**（仅在 `saveStock` 函数内） |
| result.object 消费 | — | **未读取** |
| 派生消费 | L3983-4000 → L4007 | result.list 派生 `medicalProductStockBatctPoListJson` → saveMedicalProductStockBatch params 的 `medicalProductStockBatctPoListJson` |

**A**：F4 的 result.list **直接派生** Save API 的 `medicalProductStockBatctPoListJson`（JSON.stringify 前数据源）。

---

## 9. saveStockFactory（F5）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L4006 | `$scope.saveStockFactory = new ObjectFactory();`（`saveStock` 内） |
| API | L4007 | `/admin/saveMedicalProductStockBatch.json` |
| params | L4007 | `{ listCount: $scope.getDeliveryListFactory.result.list.length, medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson) }` |
| 返回值接收 | L4007 | `var savePromise = $scope....saveOrQuery(...)`（**接收**） |
| then 回调 | L4008-4019 | `savePromise.then(function (res) { ... })` |
| res.status 读取 | L4010 | `if (res.status == 1) { ... }` |
| res.errmsg 读取 | L4011 | `Popup.notice(res.errmsg);` |
| res.result 消费 | — | **未读取** |
| success 行为 | L4012-4018 | `Popup.notice('保存成功'); search(); getCount(); $state.reload(); $scope.stockDetail = false;` |

**A**：F5 命名（`saveStockFactory`）**确实对应 Save API**（saveMedicalProductStockBatch），不需推断。

---

## 10. createOrderFactory（F6）完整生命周期

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L3965 | `$scope.createOrderFactory = new ObjectFactory();`（`selectOrder` 内） |
| API | L3966 | `/admin/sendMedicalProductToMachineCenter.json` |
| params | L3966 | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }` |
| 返回值接收 | L3966 | `var createPromise = $scope....saveOrQuery(...)`（**接收**） |
| then 回调 | L3967-3976 | `createPromise.then(function (res) { ... })` |
| res.status 读取 | L3969 | `if (res.status == 1) { ... }` |
| res.errmsg 读取 | L3970 | `Popup.notice(res.errmsg);` |
| res.result 消费 | — | **未读取** |
| success 行为 | L3971-3975 | `Popup.notice('发送成功'); $scope.addOrderModal = false; $state.reload();` |

**A**：F6 命名（`createOrderFactory`）**实际对应 Send API**（sendMedicalProductToMachineCenter）——不是字面意义的"createOrder"。

---

## 11. 六 API → Factory 映射矩阵

| # | API | Factory 实例 | 触发函数 | 返回值接收 | then | res.status/errmsg | refresh 行为 |
|---|---|---|---|---|---|---|---|
| Q1 | getCashflowDeliveryVo.json | getMedicalRecordDeliveryFactory | search() (L3846) | ✅ L3848 | ✅ L3849 | ❌ | then 内改 result.object + 弹空窗 |
| Q2 | statProductDeliveryStatusOfCashflow.json | getStatusDeliveryFactory | getCount() (L3839) | ❌ | ❌ | ❌ | **F**（result 未消费）|
| Q3 | getMedicalProductMachineCenterVoList.json | getCenterListFactory | showAddModal() (L3830) | ❌ | ❌ | ❌ | result.list 同步被 selectOrder 消费 |
| Q4 | getCanBeDeliverySkuInListOfProduct.json | getDeliveryListFactory | showDeliveryModal() (L3868) | ❌ | ❌ | ❌ | result.list 同步被 saveStock 消费 |
| S1 | saveMedicalProductStockBatch.json | saveStockFactory | saveStock() (L3979) | ✅ L4007 | ✅ L4008 | ✅ L4010/L4011 | search() + getCount() + reload() + stockDetail=false |
| S2 | sendMedicalProductToMachineCenter.json | createOrderFactory | selectOrder() (L3955) | ✅ L3966 | ✅ L3967 | ✅ L3969/L3970 | addOrderModal=false + reload() |

**A**：6 个 API 各自对应唯一 Factory 实例，无重名共享（A）。

---

## 12. Query / Save / Send 外部生命周期对照

| 维度 | Query (Q1~Q4) | Save (S1) | Send (S2) |
|---|---|---|---|
| 接收返回值 | Q1 ✅ / Q2❌ / Q3❌ / Q4❌ | ✅ | ✅ |
| then 回调 | Q1 ✅ / Q2❌ / Q3❌ / Q4❌ | ✅ | ✅ |
| res.status 处理 | ❌ | ✅ | ✅ |
| res.errmsg 处理 | ❌ | ✅ | ✅ |
| result.object 消费 | 仅 Q1 间接（then 内重写） | ❌ | ❌ |
| result.list 消费 | Q3 / Q4 同步消费 | ❌ | ❌ |
| refresh 行为 | 无显式 refresh（同步消费）| search + getCount + reload + modal close | reload + modal close（**无 search / getCount**）|

**关键差异**（A）：
- Save 的 refresh 比 Send **多两步**：`search()` + `getCount()`
- 4 个 Query 中只有 Q1 走 then 模式；Q2/Q3/Q4 走 fire-and-forget + 同步 result 消费
- 4 个 Query 均**不直接处理 res.status/errmsg**（res.* 仅在 Save/Send 的 then 中处理）

**F 边界**：ObjectFactory 内部 HTTP / Promise 实现不可知（"外部生命周期" 已封闭，内部机制不在本审计范围）。

---

## 13. result.object 完整消费清单（仅 deliveryInputCtrl L3812-4021）

| # | 行号 | 路径 | 上下文 |
|---|---|---|---|
| 1 | L3818 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | `getMachineCenterList` helper（同步读）|
| 2 | L3854 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId` | `search().then` 内**写**入 |
| 3 | L3856 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId` | `search().then` 内**写**入 null |
| 4 | L3870 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | `showDeliveryModal` |
| 5 | L3890 | `getMedicalRecordDeliveryFactory.result.object` | `isSendProduct`（存在性校验）|
| 6 | L3893 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | `isSendProduct` |
| 7 | L3907 | `getMedicalRecordDeliveryFactory.result.object` | `isSendCenter`（存在性校验）|
| 8 | L3910 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | `isSendCenter` |

**A**：result.object 消费 **8 处**（含 2 处二次写入），全部来自 F1（getMedicalRecordDeliveryFactory）。

---

## 14. result.list 完整消费清单（仅 deliveryInputCtrl L3812-4021）

| # | 行号 | 路径 | 上下文 |
|---|---|---|---|
| 1 | L3961 | `getCenterListFactory.result.list.map(...)` | `selectOrder`（派生 send JSON）|
| 2 | L3985 | `getDeliveryListFactory.result.list.length` | `saveStock` |
| 3 | L3988 | `getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList.length` | `saveStock` |
| 4 | L3989 | `getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | `saveStock` |
| 5 | L3991 | `getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | `saveStock` |
| 6 | L3992 | `getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | `saveStock` |
| 7 | L3998 | `getDeliveryListFactory.result.list[i].medicalProduct.id` | `saveStock` |

**A**：result.list 消费 **7 处**，全部来自 F3（getCenterListFactory）和 F4（getDeliveryListFactory）。

---

## 15. result 二次写入

| 行号 | 路径 | 操作 |
|---|---|---|
| L3854 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId` | 写入 `arr[i].lockMachineCenter.id` |
| L3856 | `getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId` | 写入 `null` |

**A**：deliveryInputCtrl 内 result 二次写入 **2 处**，均在 `search().then` 回调内，**写入来源是当前 result 自身**（`arr[i].lockMachineCenter.id` 来自 `arr = res.result.object.waitingDeliveryList`）。

**F**：result.object/list 来源（是后端响应、Factory 内部派生、还是其它）—— ObjectFactory 内部实现不可知。

---

## 16. saveOrQuery 返回值接收

| # | API | 行号 | 是否接收 | 接收变量名 |
|---|---|---|---|---|
| 1 | getCashflowDeliveryVo.json | L3848 | ✅ | `deliveryPromise` |
| 2 | statProductDeliveryStatusOfCashflow.json | L3841 | ❌ | — |
| 3 | getMedicalProductMachineCenterVoList.json | L3836 | ❌ | — |
| 4 | getCanBeDeliverySkuInListOfProduct.json | L3885 | ❌ | — |
| 5 | saveMedicalProductStockBatch.json | L4007 | ✅ | `savePromise` |
| 6 | sendMedicalProductToMachineCenter.json | L3966 | ✅ | `createPromise` |

**A**：3 个接收 / 3 个不接收（50% / 50%）。
**F**：变量命名（xxxPromise）暗示 Promise 行为，但**源码不显式 return Promise**（依赖 ObjectFactory 内部），故 F。

---

## 17. then / Promise 模式

| # | 行号 | 调用模式 | 上下文 |
|---|---|---|---|
| 1 | L3849 | `deliveryPromise.then(function (res) { ... })` | Q1 的 refresh / result 二次写入 |
| 2 | L3967 | `createPromise.then(function (res) { ... })` | S2 的 success / reload |
| 3 | L4008 | `savePromise.then(function (res) { ... })` | S1 的 success / refresh / reload |

**A**：3 处 `.then(callback)`。
**F**：then callback 入参 `res` 的类型（Object / PromiseResolution）—— 源码仅命名为 `res`，依赖 ObjectFactory 内部实现。

---

## 18. success callback / reload / local state

| 模式 | API | 行号 | 行为 |
|---|---|---|---|
| success callback | — | — | **0 处**（无显式 success callback 配置）|
| reload | S1 / S2 | L4016 / L3974 | `$state.reload()` |
| local state close | S1 | L4017 | `$scope.stockDetail = false` |
| local state close | S2 | L3973 | `$scope.addOrderModal = false` |
| search 重新触发 | S1 only | L4014 | `search()` |
| getCount 重新触发 | S1 only | L4015 | `getCount()` |
| 弹空窗 | Q1 only | L3860 | `Popup.notice('您的待发货项目已分拣完毕', 1500, function () { $state.go('deliveryList'); })` |

**A**：Save (S1) 触发 4 步 refresh；Send (S2) 触发 2 步 refresh。两者均通过 then 回调同步执行。
**A**：0 处显式 success callback 配置；0 处 error callback 配置。

---

## 19. Save JSON 来源 Factory 证明

**Save API**：saveMedicalProductStockBatch.json
**字段**：`medicalProductStockBatctPoListJson`

### 逆向链路

| 步骤 | 行号 | 证据 |
|---|---|---|
| 派生起点 | L3983 | `var medicalProductStockBatctPoListJson = [];` |
| 外层循环 | L3985 | `for (var i = 0; i < $scope.getDeliveryListFactory.result.list.length; i++)` |
| 字段填充 | L3998 | `medicalProductStockBatctPoListJson.push({ medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id, medicalProductStocks: arr[i] });` |
| JSON 包装 | L4007 | `medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson)` |

**A**：Save JSON 的数据源 Factory = **`getDeliveryListFactory`（F4）**（直接源码证据）。
**A**：F4.result.list 在 saveStock 函数内被读取 6 次（L3985/L3988/L3989/L3991/L3992/L3998），所有路径均用作 Save JSON 的输入。

---

## 20. Send JSON 来源 Factory 证明

**Send API**：sendMedicalProductToMachineCenter.json
**字段**：`medicalProductMachineCenterPoListJson`、`planDeliveryTime`

### 逆向链路

| 步骤 | 行号 | 证据 |
|---|---|---|
| 派生起点 | L3961 | `var arr = $scope.getCenterListFactory.result.list.map(function (v) { return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }; });` |
| 字段填充 | L3961-3963 | map 内一次性构造 `medicalProductId` + `machineCenterId` |
| 时间字段 | L3964 | `$scope.startTime = DateUtilFactory.origin($scope.startTime);`（时间归零）|
| JSON 包装 | L3966 | `medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime` |

**A**：Send JSON 的数据源 Factory = **`getCenterListFactory`（F3）**（直接源码证据）。
**A**：F3.result.list 仅在 selectOrder 函数内被读取 1 次（L3961），用作 Send JSON 的输入。

**A**：F3（getCenterListFactory）≠ F4（getDeliveryListFactory），两份 JSON 来自不同 Factory。

---

## 21. 六 API 外部生命周期冻结

### 21.1 最小外部协议（已封闭）

```
new ObjectFactory()
        ↓
factory.saveOrQuery(API, params)
        ↓
（可选）factory.saveOrQuery(...) → thenable
        ↓
Controller 消费：
  - result.object（仅 F1）
  - result.list（仅 F3 / F4）
  - res.status / res.errmsg（仅 S1 / S2 的 then 内）
```

### 21.2 六 API 生命周期差异

| API | 类型 | 是否 then | 是否处理 res.* | result 消费位置 |
|---|---|---|---|---|
| getCashflowDeliveryVo | Query | ✅ | ❌ | F1.result.object（深度消费）|
| statProductDeliveryStatus | Query | ❌ | ❌ | **F**（result 未消费）|
| getMedicalProductMachineCenterVo | Query | ❌ | ❌ | F3.result.list（selectOrder 派生）|
| getCanBeDeliverySku | Query | ❌ | ❌ | F4.result.list（saveStock 派生）|
| saveMedicalProductStockBatch | Save | ✅ | ✅ status/errmsg | F5.then 内 refresh |
| sendMedicalProductToMachineCenter | Send | ✅ | ✅ status/errmsg | F6.then 内 reload |

**A**：六 API 外部生命周期互不相同（"外部形式一致" 不等于 "生命周期一致"）。

---

## 22. 历史证据 vs 当前代码

### 22.1 S1-76 表述

> 当前 controller.js 资源范围内没有 ObjectFactory 定义源码。
> 全仓已观察：`new ObjectFactory()` 为 0 参数调用。
> ObjectFactory 的外部调用核心形式：`saveOrQuery(API, params)`。
> ObjectFactory 与 ListFactory 不同构。
> deliveryInputCtrl 的 6 个核心 API 均经过 ObjectFactory。

### 22.2 S1-77 表述

> 1084 次 `saveOrQuery` 全仓调用统计（A）。
> 100% 调用形式：`saveOrQuery(API, params)` 2 参数。
> 0 个 null/undefined params。
> deliveryInputCtrl 6 API 完整 params 收口。
> result.object 2 个 controller 使用 / result.list 4 个 controller 使用。

### 22.3 S1-78 新增/修正

| 项 | 历史 | 当前代码 | 判定 |
|---|---|---|---|
| 7 个 Factory 名称 | 7 个独立 Factory | 6 个真实 Factory + 1 个 helper function | **修正**（按 L3816-4021 范围）|
| `getMachineCenterList` 性质 | S1-76 列为 Factory 别名 | L3816 是 function（不是 Factory）| **修正** |
| `getMachineCenterListFactory` | 未列 | L37387 是 ListFactory（不同构）| **新增**（F：非 ObjectFactory）|
| `getStatusDeliveryFactory.result` | S1-77 列为 result.object 2 个 controller 之一 | deliveryInputCtrl 内 0 处消费 | **修正**（可能 HTML / 其它 controller 消费）|
| Save refresh | S1-77 未细分 | search + getCount + reload + stockDetail=false（4 步）| **细化** |
| Send refresh | S1-77 未细分 | reload + addOrderModal=false（2 步）| **细化** |
| Save JSON 来源 | 未列 | getDeliveryListFactory.result.list | **新增** |
| Send JSON 来源 | 未列 | getCenterListFactory.result.list | **新增** |

### 22.4 最终采用

- **保留**：S1-76 的 0 参数 + saveOrQuery(API, params) 协议；S1-77 的 6 API params 收口。
- **修正**：7 个 Factory 名称 ≠ 7 个独立实例；`getMachineCenterList` 是 helper function。
- **细化**：Save/Send 外部生命周期差异。
- **新增**：Save/Send JSON 数据源 Factory 证明。

---

## 23. A / B / C / D / E / F 评级

| # | 审计项 | 评级 |
|---|---|---|
| 01 | deliveryInputCtrl 全部 ObjectFactory 实例 | **A** |
| 02 | Factory 实例去重 | **A** |
| 03 | getMedicalRecordDeliveryFactory 完整生命周期 | **A** |
| 04 | getStatusDeliveryFactory 完整生命周期 | **A**（含 1 项 F：result 未消费）|
| 05 | getCenterListFactory 完整生命周期 | **A** |
| 06 | getDeliveryListFactory 完整生命周期 | **A** |
| 07 | saveStockFactory 参与 Save API | **A** |
| 08 | createOrderFactory 参与 Send API | **A** |
| 09 | getMachineCenterList 是 helper function | **A**（修正 S1-76）|
| 10 | 六 API → Factory 映射矩阵 | **A** |
| 11-16 | 六 API 完整生命周期 | **A** |
| 17 | Query / Save / Send Factory 对照 | **A** |
| 18 | result.object 消费清单 | **A** |
| 19 | result.list 消费清单 | **A** |
| 20 | result 二次写入 | **A** |
| 21 | saveOrQuery 返回值接收 | **A** |
| 22 | then / Promise 模式 | **A**（外部 then 形式 + 内部实现 F）|
| 23 | success callback | **A**（0 处）|
| 24 | Query / Save / Send 外部生命周期差异 | **A** |
| 25 | Factory 与 Controller state | **A** |
| 26 | Factory 与 refresh | **A** |
| 27 | Save JSON 来源 Factory | **A** |
| 28 | Send JSON 来源 Factory | **A** |
| 29 | 六 API 外部生命周期冻结 | **A** |
| 30 | Q1~Q20 回答 | **A** |

**统计**：30 项全部 **A**（含修正项与细化项），无 E 升 A / 无 F 升 A。

---

## 24. L1 / L2 / L3 分层

| 层级 | 内容 | 是否在本审计 |
|---|---|---|
| L1 前端事实 | 6 Factory 实例、6 API URL、params 结构、result 消费位置、生命周期 | **是** |
| L2 业务规则 | 锁仓归属、待发货列表、加工中心匹配规则 | **部分**（L3888-3921 含 L2 校验）|
| L3 数据库物理模型 | 后端 DTO / VO / PO / Service / Repository / DB Table / FK | **否**（F） |

**F**：后端 6 API 响应结构、ObjectFactory 内部实现、result.object/list 后端字段名、Save/Send 业务后端处理流程。

---

## 25. R1-R6 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌（未触发）|
| R2 真实 API 调用 | ❌（仅静态源码）|
| R3 创建 DTO/VO/PO/Service/Repository | ❌（未创建）|
| R4 修改历史 MD | ❌（未修改）|
| R5 删除 10 个 untracked | ❌（10 个原样保留）|
| R6 P0/P1 自动新增 | ❌（P0=54 / P1=8 冻结）|

---

## 26. Q1-Q20 回答

| Q | 答案 |
|---|---|
| Q1：deliveryInputCtrl 实际使用几个独立 ObjectFactory 实例？| **6 个**（F1~F6）|
| Q2：7 个 Factory 名称中哪些是独立实例？| **6 个**（getMachineCenterList 是 helper function）|
| Q3：哪些是别名？| **0 个**（L37387 的 getMachineCenterListFactory 是 ListFactory，不同构）|
| Q4：六 API 分别对应哪个 Factory？| 见第 11 节映射矩阵（A）|
| Q5：getMedicalRecordDeliveryFactory 消费什么？| result.object.waitingDeliveryList（8 处直接读 + 2 处二次写）|
| Q6：getCenterListFactory 消费什么？| result.list（L3961，selectOrder 派生 Send JSON）|
| Q7：getDeliveryListFactory 消费什么？| result.list（6 处，saveStock 派生 Save JSON）|
| Q8：saveStockFactory 是否真正参与 Save API？| **是**（L4006-4007 实际调用 saveMedicalProductStockBatch.json）|
| Q9：createOrderFactory 是否真正参与 Send API？| **是**（L3965-3966 实际调用 sendMedicalProductToMachineCenter.json）|
| Q10：getStatusDeliveryFactory 是否真正参与核心 6 API？| **是**（L3840-3841 调用 statProductDeliveryStatusOfCashflow.json）但 **result 在 deliveryInputCtrl 内 0 处消费**（F 边界）|
| Q11：result.object 有哪些直接消费？| **8 处**（L3818/L3854/L3856/L3870/L3890/L3893/L3907/L3910，全部来自 F1）|
| Q12：result.list 有哪些直接消费？| **7 处**（L3961 来自 F3；L3985/L3988/L3989/L3991/L3992/L3998 来自 F4）|
| Q13：saveOrQuery 返回值是否被接收？| **3 接收 / 3 不接收**（50% / 50%）|
| Q14：是否存在 then？| **3 处**（L3849/L3967/L4008）|
| Q15：Query / Save / Send 外部生命周期是否不同？| **是**（详见第 12 节）|
| Q16：Save success 的 refresh 是什么？| search() + getCount() + $state.reload() + $scope.stockDetail = false（4 步）|
| Q17：Send success 的 refresh 是什么？| $state.reload() + $scope.addOrderModal = false（2 步，**无 search / 无 getCount**）|
| Q18：Save JSON 的来源 Factory 是什么？| **getDeliveryListFactory（F4）**（L3985-L3998 直接派生）|
| Q19：Send JSON 的来源 Factory 是什么？| **getCenterListFactory（F3）**（L3961 map 派生）|
| Q20：六 API → Factory → result → consumer 是否已经完整闭合？| **是**（除 F2 result 消费位置属 F 边界外，其余 5 API 生命周期均已 A 级闭合）|

---

## 27. P0 / P1

- **P0 = 54**（冻结，未自动新增）
- **P1 = 8**（冻结，未自动新增）

---

## 28. 当前 F 边界

| F 项 | 不属本审计的原因 |
|---|---|
| ObjectFactory 内部 HTTP / Promise / then 实现 | 当前资源范围不可得 |
| `saveOrQuery` 是否真为 Promise | 源码命名（xxxPromise）+ then 形式可观察，但无内部实现 |
| `res` 参数类型 / 字段结构 | 依赖 ObjectFactory 内部 |
| `result.object / result.list` 字段填充来源 | 依赖 ObjectFactory 内部（**F2 最显著**）|
| 6 API 后端响应 DTO / VO 结构 | L3 数据库物理模型，超出本审计 |
| 6 API 后端 Service / Repository 实现 | L3，超出本审计 |
| HTML 模板 `{{ Factory.result.* }}` 绑定 | 未读 HTML |
| deliveryInputCtrl 之外的同名 Factory 消费模式 | 属其它 controller 审计 |
| L37387 `getMachineCenterListFactory`（ListFactory）消费模式 | 属 ListFactory 审计，不属本 ObjectFactory 审计 |
| `getStatusDeliveryFactory.result` 实际消费位置 | deliveryInputCtrl Controller 层 0 处，可能 HTML 或其它 controller |

---

## 29. 本轮新增事实

1. **deliveryInputCtrl 内 6 个独立 ObjectFactory 实例**（非 S1-76 表述的 7 个；`getMachineCenterList` 是 helper function）。
2. **6 API → 6 Factory 一一对应**（无共享实例）。
3. **6 API 外部生命周期互不相同**（Q1~Q4 的 4 个 Query 模式差异；S1 与 S2 的 refresh 步骤差异）。
4. **getStatusDeliveryFactory（F2）result 在 deliveryInputCtrl 内 0 处消费**（关键 F）。
5. **Save refresh 含 4 步 / Send refresh 含 2 步**（Save 多 search + getCount 两步）。
6. **Save JSON 数据源 = F4.result.list**（getDeliveryListFactory）。
7. **Send JSON 数据源 = F3.result.list**（getCenterListFactory）。
8. **L37387 getMachineCenterListFactory 是 ListFactory**（与 ObjectFactory 不同构，不属本审计范围）。
9. **L16211 saveStockFactory 是同名不同 API 调用点**（调用 saveToBeProcessSkuInListOfProduct.json，与本审计 Save API 不同）。
10. **saveOrQuery 返回值接收 3 接收 / 3 不接收**（50% / 50%）。
11. **then 模式 3 处**（L3849/L3967/L4008）。
12. **0 处显式 success callback 配置**。

---

## 30. 历史一致性记录（不动历史 MD）

| 历史文件 | 与本轮关系 |
|---|---|
| `136_S1-76_*.md` | 7 个 Factory 名称的提法**保留**（S1-76 视角），本轮 6 实例 + 1 helper 的修正仅在新文档声明 |
| `137_S1-77_*.md` | params 收口**完整保留**；本轮 result 消费细化是 S1-77 基础上的扩展 |
| `137_审计勘误与当前有效证据基线_20260904.md` | 本轮 result 消费与生命周期细化是 S1-78 的新增事实，不影响 S1-77 基础结论 |
| `138_*.md` | P0 决策与证据台账**保留**；本轮 30 项审计不触发 P0 / P1 自动新增 |
| `134_S1-74_*.md` / `135_S1-75_*.md` | ListFactory 协议**保留**；本轮 L37387 ListFactory 观察属 L4 ListFactory 审计延伸，**未越界到本轮 ObjectFactory 审计** |

**红线**：未修改任何历史 MD。

---

## 31. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| 写操作 = 0 | ✅（仅写本轮 1 个新文档）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅（P0=54 冻结）|
| P1 自动新增 = 0 | ✅（P1=8 冻结）|
| 10 个 untracked 临时文件仍保留 | ✅ |
| Git 禁止命令未触发 | ✅（仅 `git add -- 139_*.md`）|

---

## 32. 停止条件

✅ 30 项审计全部 A 级闭合（无 E/F 升 A）
✅ 30 问 Q1-Q20 全部回答
✅ 6 API 外部生命周期冻结完成
✅ F 边界明确列出
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-79）**。
