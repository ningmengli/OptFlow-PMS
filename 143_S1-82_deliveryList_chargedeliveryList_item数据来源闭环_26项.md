# S1-82 deliveryList `chargedeliveryList` / item 数据来源闭环

> 审计对象：`sessionStorage` key `chargedeliveryList` + `deliveryListCtrl` 初始化链 + `memberFactory.items` → HTML `item.*` → 3 个 state 跳转 cashflowId
> 任务来源：S1-82（基于 S1-81 已确认 deliveryListCtrl 不读 $stateParams，HTML item 字段直接消费）
> 审计立场：**只按源码 + 只读 HTML 证据；不凭"缓存"语义推断；不混淆 storage item 与 API item**

---

## 1. 核心结论（50 字以内）

**`chargedeliveryList` 仅 deliveryListCtrl 自身读写；item 数据来自 `memberFactory.items`（API Response）；3 个 state 跳转 cashflowId 100% 来自 `item.cashflow.id`。**

---

## 2. 证据范围

| 维度 | 范围 | 备注 |
|---|---|---|
| sessionStorage 全仓 | controller.js | working dir untracked，git tracked 中无 |
| deliveryInputCtrl L3812-4021 | 0 处 sessionStorage | 本轮关键 |
| deliveryListCtrl L4075-4233 | 3 处 sessionStorage | 1 读 + 2 写 |
| deliveryList.html | 344 行（只读）| SHA256 已快照 |
| 其它 9 untracked HTML | 0 处 sessionStorage 引用 | — |
| 跨 controller sessionStorage 共享 | **0 处** | 严格边界 |
| 后端 API 完整 Response 字段 | **不可得** | F 边界 |
| sessionStorage 跨 session 行为 | **不可得** | F 边界 |

---

## 3. sessionStorage 全仓清单

### 3.1 全仓 sessionStorage 操作（27 处）

| 行号 | 操作 | key | 上下文 |
|---|---|---|---|
| L4076 | getItem | `chargedeliveryList` | deliveryListCtrl 读取 |
| L4190 | setItem | `chargedeliveryList` | deliveryListCtrl search 内 |
| L4203 | setItem | `chargedeliveryList` | deliveryListCtrl pagination callback |
| L14099 | setItem | `userInfo` | 某 controller |
| L14123 | setItem | `loginInfo` | 某 controller |
| L14274 | setItem | `loginInfo` | 某 controller |
| L15975 | getItem | `companyStockList` | 某 controller |
| L15994 | setItem | `companyStockList` | 某 controller |
| L16005 | setItem | `companyStockList` | 某 controller |
| L17745 | setItem | `memberStore` | 某 controller |
| L17747 | getItem | `memberStore` | 某 controller |
| L21147 | 注释 | `materialDeliveryType` | 注释 |
| L22247 | 注释 | `materialDeliveryType` | 注释 |
| L24766 | getItem | `chooseTime` | 某 controller |
| L24803 | setItem | `chooseTime` | 某 controller |
| L24969 | getItem | `chooseTime` | 某 controller |
| L25005 | setItem | `chooseTime` | 某 controller |
| L26187 | getItem | `materialDeliveryType` | 某 controller |
| L26241 | setItem | `materialDeliveryType` | 某 controller |
| L27580 | getItem | `backGoodsStatus` | 某 controller |
| L27623 | getItem | `chooseTime2` | 某 controller |
| L27658 | setItem | `chooseTime2` | 某 controller |
| L27659 | setItem | `backGoodsStatus` | 某 controller |
| L27791 | getItem | `materialReceiptsType` | 某 controller |
| L27832 | setItem | `materialReceiptsType` | 某 controller |
| L37787 | getItem | `reportActive` | 某 controller |
| L37792 | setItem | `reportActive` | 某 controller |

**A**：全仓 27 处 sessionStorage 操作分布于 **多种业务 key**（11 种不同 key）。

### 3.2 removeItem 全仓清单

| 行号 | 操作 | key | 备注 |
|---|---|---|---|
| L1167 | localStorage.removeItem | `$scope.corpid + "_userCert"` | localStorage |
| L1277 | localStorage.removeItem | `$scope.corpid + "_userCert"` | localStorage |
| L47348 | StorageFactory.removeItem | `screenlist` | 自定义 StorageFactory |
| L50702 | sessionStorage.removeItem | `customerCharge` | sessionStorage |

**A**：
- **sessionStorage.removeItem 仅 1 处**（L50702 `customerCharge`）
- **chargedeliveryList 全仓 0 处 removeItem**（A）
- sessionStorage 与 localStorage 在 controller.js 中**是不同 API**（不可混淆）

---

## 4. `chargedeliveryList` 写入点

### 4.1 全仓 setItem 出现位置

| 行号 | 完整语句 | 上下文 |
|---|---|---|
| L4190 | `sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));` | `search()` 函数内 |
| L4203 | `sessionStorage.setItem("chargedeliveryList", JSON.stringify($scope.obj));` | pagination callback 内 |

**A**：`chargedeliveryList` 全仓 **2 处 setItem**，**全部在 deliveryListCtrl**（A）。
**A**：写入 value = `JSON.stringify($scope.obj)`（A）。

### 4.2 写入触发时机

| 触发点 | 时机 |
|---|---|
| L4190 | 用户调用 `search()` 函数（包括初始化 L4210 + 翻页 + tab 切换 + fee 切换 + keyword 变化）|
| L4203 | pagination callback（点击页码）|

**A**：写入由 search 函数统一触发，**$scope.obj 在 search 时被持久化**（A）。

### 4.3 写入方 Controller

**A**：写入方 = **deliveryListCtrl**（仅 1 个 controller，A）。
**A**：**deliveryInputCtrl 不写 chargedeliveryList**（L3812-4021 范围 0 处 sessionStorage，A）。

---

## 5. `chargedeliveryList` 读取点

### 5.1 全仓 getItem 出现位置

| 行号 | 完整语句 | 上下文 |
|---|---|---|
| L4076 | `var store = JSON.parse(sessionStorage.getItem("chargedeliveryList"));` | deliveryListCtrl 初始化 |

**A**：`chargedeliveryList` 全仓 **1 处 getItem**（A）。

### 5.2 读取方 Controller

**A**：读取方 = **deliveryListCtrl**（仅 1 个 controller，A）。
**A**：**deliveryInputCtrl 不读 chargedeliveryList**（A）。
**A**：**deliveryListCtrl 是 chargedeliveryList 唯一的读写方**（A）。

---

## 6. storage value 真实结构

### 6.1 写入值

```javascript
JSON.stringify($scope.obj)
```

### 6.2 $scope.obj 字段全集

| 字段 | 类型 | 初始化 | 写入 |
|---|---|---|---|
| `startTime` | Date | L4081 `moment().add(-3, 'months')._d` / L4079 恢复 | L4168-4172 处理 |
| `endTime` | Date | — | L4174-4179 派生 |
| `rightTimer` | Date | L4086 `new Date()` / L4084 恢复 | L4174-4176 处理 |
| `deliveryStatus` | number/null | L4088-4100 默认 null | L4129-4143 切换 |
| `toBeProcess` | number/null | 同上 | L4130-4142 切换 |
| `refundStatus` | number | L4104 默认 0 | L4149 setFee 切换 |
| `keyword` | string | — | L4192 同步到 countObj |
| `productKeyword` | string | — | (HTML L102-110) |
| `batchNoKeyword` | string | — | (HTML L113-121) |
| `page` | number | — | L4189/L4202/L4213 |
| `refundStatusArray` | array | — | L4158/L4160/L4185/L4187（局部转换）|

### 6.3 $scope.obj 不包含的业务字段

- ❌ `cashflow`（**不存在**）
- ❌ `medicalProduct`（**不存在**）
- ❌ `patient`（**不存在**）
- ❌ `customer`（**不存在**）
- ❌ `waitingDeliveryList`（**不存在**）
- ❌ `deliveryedList`（**不存在**）
- ❌ `sendToMachineCenterList`（**不存在**）
- ❌ `medicalProductDelivery`（**不存在**）
- ❌ `cashflowId`（**不存在**）

**A**：storage value = **查询参数对象**（仅 11 个查询 / 状态字段），**不包含任何业务数据字段**（A）。

---

## 7. JSON.stringify / JSON.parse 模式

| 操作 | 模式 | 行号 |
|---|---|---|
| setItem | `JSON.stringify($scope.obj)` | L4190 / L4203 |
| getItem | `JSON.parse(sessionStorage.getItem(...))` | L4076 |

**A**：
- setItem **100%** 使用 `JSON.stringify` 包装对象
- getItem **100%** 使用 `JSON.parse` 解析字符串
- **无 raw 字符串** 或 **其他序列化**形式

---

## 8. deliveryListCtrl 初始化完整顺序

```javascript
// L4075-4233 严格按代码顺序
1. L4076-4077  读取 sessionStorage, $scope.obj = store ? store : {}
2. L4078-4086  startTime / rightTimer 恢复（Date 转换 + 默认值）
3. L4088-4100  deliveryStatus / toBeProcess 默认映射 → $scope.deliveryStatus
4. L4101-4105  refundStatus 默认值
5. L4107-4125  grantAuth → getAdminList = new ListFactory(...)
6. L4127-4146  setTab function 定义
7. L4148-4151  setFee function 定义
8. L4152      $scope.countObj = {}
9. L4153-4164  searchCount function 定义
10. L4166-4209 search function 定义
11. L4210      $scope.search()  ← 立即调用（同步触发 3 个 API + 写 storage）
12. L4212-4215 clearPage function 定义
13. L4216-4232 printFahuoqingdan object 定义
```

**A**：初始化顺序 = **sessionStorage 读取 → 默认值填充 → 异步 grantAuth → 同步 search 立即执行**（A）。

### 8.1 同步触发的 API

| API | 触发位置 | 类型 |
|---|---|---|
| getAdminList (L4121) | grantAuth.then 回调内 | 异步 |
| checkCountFactory (L4163) | $scope.search() → searchCount() 内 | 同步 |
| memberFactory (L4195) | $scope.search() 内 | 同步 |

**A**：search() 同步触发 checkCountFactory + memberFactory（2 个 API）+ 同步 setItem storage（A）。

---

## 9. deliveryListCtrl item 数据来源

### 9.1 item 来自 memberFactory.items

```javascript
// L4195-4196
$scope.memberFactory = new ListFactory("/admin/getCashflowDeliveryVoList.json", pageStart, pageSize, obj);
var promise = $scope.memberFactory.nextPage();
```

```html
<!-- deliveryList.html L202 -->
<div ng-repeat="item in memberFactory.items">
```

**A**：
- `$scope.memberFactory.items` = 后端 `getCashflowDeliveryVoList.json` Response 的 items 数组（A）
- HTML `item` = `memberFactory.items[i]`（A）
- deliveryListCtrl 自身 **0 处直接读 `memberFactory.items[i].xxx`**（controller 仅初始化 + 分页 + storage，A）

### 9.2 storage item vs API item

| 维度 | storage item | API item |
|---|---|---|
| 名称 | `chargedeliveryList` | `memberFactory.items` |
| 来源 | 写入：`$scope.obj` (L4190/L4203) | 后端 Response |
| 字段 | 11 个查询参数字段 | 业务数据字段（patient / medicalRecord / customer / cashflow / waitingDeliveryList / ...）|
| 读取 | deliveryListCtrl $scope.obj 恢复 | HTML `item` 渲染 |
| 跨 controller 共享 | ❌（仅 deliveryListCtrl）| ❌（仅 deliveryListCtrl）|
| 是否同一 collection | **否** | — |

**A**：
- storage `chargedeliveryList` 存储的是 **$scope.obj 查询参数**
- API `memberFactory.items` 返回的是 **业务数据 item 数组**
- **两者结构完全不同**（查询参数 vs 业务数据），**不可视为同一来源**（A）
- **storage item 概念不成立**（storage 不存 item 列表）

---

## 10. memberFactory 完整 API 链

| 步骤 | 行号 | 证据 |
|---|---|---|
| 创建 | L4195 | `new ListFactory("/admin/getCashflowDeliveryVoList.json", pageStart, pageSize, obj)` |
| params = obj | L4181 / L4195 | `var obj = angular.copy($scope.obj);` |
| nextPage | L4196 | `var promise = $scope.memberFactory.nextPage();` |
| 返回 then | L4197 | `promise.then(function (data) { ... })` |
| count 消费 | L4198 | `$("#Pagination").pagination($scope.memberFactory.count, ...)` |
| items 消费 | HTML L202 | `ng-repeat="item in memberFactory.items"` |
| 翻页 | L4204-4205 | `clearAndSetIndex` + `nextPage` |

**A**：
- API = `getCashflowDeliveryVoList.json`（A）
- 4 参数 ListFactory（API / pageStart / pageSize / params）（A）
- params = `angular.copy($scope.obj)`（A）
- pageSize = 12（A）
- pageStart = `$scope.obj.page * pageSize`（A）
- Response 含 `items[]` + `count` 字段（A，由 HTML 渲染 + jQuery pagination 证明）

---

## 11. `getCashflowDeliveryVoList.json` API 完整记录

| 维度 | 值 | 证据 |
|---|---|---|
| API 路径 | `/admin/getCashflowDeliveryVoList.json` | L4195 |
| List 协议 | ListFactory 4 参数 | L4195 |
| Request params | `obj = angular.copy($scope.obj)` | L4181 |
| pageSize | 12 | L4167 |
| Response 字段（已观察）| `items[]` + `count` | HTML L202 + L4198 |
| Response 字段（F）| 完整 item 字段结构 | 不可得 |

### 11.1 request 字段全集

obj 字段（继承 $scope.obj）：
- startTime / endTime / rightTimer
- deliveryStatus / toBeProcess
- refundStatus / refundStatusArray
- keyword / productKeyword / batchNoKeyword
- page

**A**：request = 查询参数 object（A）。

### 11.2 response items[i] 字段（HTML 观察）

| 字段路径 | HTML 行号 | 上下文 |
|---|---|---|
| `item.patient.avatar` | L211 | img src |
| `item.patient.patientName` | L215 | 文本 |
| `item.patient.patientGender` | L218 | filter |
| `item.patient.patientBirthday` | L219 | filter |
| `item.medicalRecord.medicalRecordType` | L223 | filter |
| `item.medicalRecord.medicalCode` | L224 | 文本 |
| `item.productNames` | L226 | 文本 |
| `item.deliveryStatus` | L229 | filter + L206 ng-class |
| `item.waitingSeconds` | L232 | filter |
| `item.medicalRecord.doctorName` | L235 | 文本 |
| `item.customer.customerName` | L237 | 文本 |
| `item.customer.linkMobile` | L243 | filter |
| `item.waitingDeliveryList` | L251 | ng-if length |
| `item.deliveryedList` | L260/L267/L283 | ng-if length |
| `item.sendToMachineCenterList` | L275 | ng-show length |
| `item.cashflow.id` | L253/L261/L268/L274/L285 | state param / print arg |
| `item.medicalRecord.id` | L293 | ng-show |
| `item.waitingExamineList[].medicalExamine.id` | L308 | ng-true-value |
| `item.waitingExamineList[].medicalExamine.examineName` | L310 | text |
| `item.waitingExamineList[].medicalExamine.payedStatus` | L312 | filter |
| `item.patient.id` | L319 | savePatient arg |

**A**：HTML 至少消费 18 个 item 字段路径（A）。
**F**：后端 items 完整字段（HTML 未列全的可能更多）。

---

## 12. 3 个 list 字段 HTML 消费详细

### 12.1 `item.waitingDeliveryList` 完整路径

```html
<!-- L251-258 -->
<li ng-if="item.waitingDeliveryList.length" 
    class="text-align_center flex-item cursor-pointer"
    ui-sref="deliveryInput({cashflowId:item.cashflow.id})">
    待发货<span class="red">({{item.waitingDeliveryList.length}})</span>
</li>
```

**A**：
- HTML 消费：`item.waitingDeliveryList.length`（A）
- 条件：length > 0 显示
- 跳转：`deliveryInput({cashflowId:item.cashflow.id})`
- 按钮文案："待发货 N"

### 12.2 `item.deliveryedList` 完整路径

```html
<!-- L260-272 -->
<li ng-if="item.deliveryedList.length && item.waitingDeliveryList.length"
    ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"
    class="text-align_center flex-item cursor-pointer border">
    已发货<span class="red">({{item.deliveryedList.length}})</span>
</li>
<li ng-if="item.deliveryedList.length && !item.waitingDeliveryList.length"
    ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"
    class="text-align_center flex-item cursor-pointer">
    已发货<span class="red">({{item.deliveryedList.length}})</span>
</li>
```

**A**：
- HTML 消费：`item.deliveryedList.length`（A）
- 2 个独立 ng-if 分支（与 waitingDeliveryList 互斥 / 共存）
- 跳转：`deliveryInputRecord({cashflowId:item.cashflow.id})` × 2
- 按钮文案："已发货 N"

### 12.3 `item.sendToMachineCenterList` 完整路径

```html
<!-- L273-281 -->
<li ui-sref="deliveryProcessing({cashflowId:item.cashflow.id})"
    ng-show="item.sendToMachineCenterList.length"
    class="text-align_center flex-item border cursor-pointer">
    加工中<span class="red">({{item.sendToMachineCenterList.length}})</span>
</li>
```

**A**：
- HTML 消费：`item.sendToMachineCenterList.length`（A）
- 条件：length > 0 显示
- 跳转：`deliveryProcessing({cashflowId:item.cashflow.id})`
- 按钮文案："加工中 N"

---

## 13. `item.deliveryStatus` 完整路径

### 13.1 HTML 消费

| 行号 | 形式 | 用途 |
|---|---|---|
| L206 | `ng-class="{'waiting-status':item.deliveryStatus==2,'examined-status':item.deliveryStatus==1}"` | 卡片样式 |
| L229 | `{{item.deliveryStatus \| deliveryStatus}}` | 文本渲染（filter）|

### 13.2 deliveryListCtrl deliveryStatus（scope 变量，非 item）

| 行号 | 形式 | 用途 |
|---|---|---|
| L4091 | `$scope.deliveryStatus = 1` | tab 状态 |
| L4095 | `$scope.deliveryStatus = 2` | tab 状态 |
| L4099 | `$scope.deliveryStatus = 3` | tab 状态 |
| L4131 | `$scope.deliveryStatus = 1`（setTab(1)）| tab 状态 |
| L4135 | `$scope.deliveryStatus = 2`（setTab(2)）| tab 状态 |
| L4139 | `$scope.deliveryStatus = 3`（setTab(3)）| tab 状态 |
| L4143 | `$scope.deliveryStatus = null`（setTab else）| tab 状态 |
| L130/L138/L149/L160 | `ng-class` based on `deliveryStatus==null/1/2/3` | tab 选中样式 |

**A**：
- `item.deliveryStatus`（HTML item 字段）≠ `$scope.deliveryStatus`（controller tab 状态变量）
- 2 个不同字段路径（A）
- 严格不可混淆

---

## 14. `item.cashflow.id` 完整路径

### 14.1 HTML 4 处出现

| 行号 | 形式 | 用途 |
|---|---|---|
| L253 | `ui-sref="deliveryInput({cashflowId:item.cashflow.id})"` | 待发货跳转 |
| L261 | `ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"` | 已发货跳转 1 |
| L268 | `ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"` | 已发货跳转 2 |
| L274 | `ui-sref="deliveryProcessing({cashflowId:item.cashflow.id})"` | 加工中跳转 |
| L285 | `printFahuoqingdan.print(item.cashflow.id)` | 打印参数 |

**A**：4 处 ui-sref state 跳转 + 1 处 print 函数调用，**全部 cashflowId 来源 = `item.cashflow.id`**（A）。

### 14.2 item.cashflow 来源

```html
<!-- HTML L253 -->
ui-sref="deliveryInput({cashflowId:item.cashflow.id})"
```

**A**：`item.cashflow` = `memberFactory.items[i].cashflow`（A）。
**A**：`item.cashflow.id` = `memberFactory.items[i].cashflow.id`（A）。
**A**：item.cashflow **不是** sessionStorage 字段（storage 仅 $scope.obj，A）。
**A**：item.cashflow **不是** controller 派生变量（deliveryListCtrl 0 处访问 item，A）。

---

## 15. 3 个 state 跳转闭合链路

### 15.1 `deliveryInput` 跳转链路（A）

```
HTML L251: item.waitingDeliveryList.length > 0
    ↓
HTML L253: ui-sref="deliveryInput({cashflowId:item.cashflow.id})"
    ↓ (UI Router 跳转)
deliveryInput state
    ↓ (UI Router 解析)
deliveryInputCtrl (L3812)
    ↓
L3814: $scope.cashflowId = $stateParams.cashflowId
    ↓
6 API (F1-F6, L3836/L3841/L3848/L3885/L3966/L4007)
```

**A**：链路 **A 级闭合**（item.waitingDeliveryList → deliveryInput → F1 查询 waitingDeliveryList）。

### 15.2 `deliveryInputRecord` 跳转链路（A）

```
HTML L260/L267: item.deliveryedList.length > 0
    ↓
HTML L261/L268: ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"
    ↓ (UI Router 跳转)
deliveryInputRecord state
    ↓
deliveryInputRecordCtrl (L4024)
    ↓
L4026: $scope.cashflowId = $stateParams.cashflowId
    ↓
4 API (L4034/L4040/L4044/L4061)
```

**A**：链路 **A 级闭合**。

### 15.3 `deliveryProcessing` 跳转链路（A）

```
HTML L275: item.sendToMachineCenterList.length > 0
    ↓
HTML L274: ui-sref="deliveryProcessing({cashflowId:item.cashflow.id})"
    ↓ (UI Router 跳转)
deliveryProcessing state
    ↓
deliveryProcessingCtrl (L4236)
    ↓
L4238: $scope.cashflowId = $stateParams.cashflowId
    ↓
2 API (L4242/L4249)
```

**A**：链路 **A 级闭合**。

---

## 16. deliveryInputCtrl 与 storage 关系

### 16.1 deliveryInputCtrl 范围内 sessionStorage

```powershell
Where-Object { $_.LineNumber -ge 3812 -and $_.LineNumber -le 4021 }
```

**A**：**0 处匹配**（A）。

### 16.2 推论

**A**：
- deliveryInputCtrl **不读** chargedeliveryList（A）
- deliveryInputCtrl **不写** chargedeliveryList（A）
- deliveryInputCtrl L3861 `$state.go('deliveryList')` **不传 state params**（S1-81 已确认）
- deliveryInputCtrl L3861 **不写 storage**（本轮 A 级确认）
- 跳转到 deliveryList 后，deliveryListCtrl 读取的是 **user 之前操作留下的 storage**（**F**：具体什么操作留下不可证）

**A**：deliveryInputCtrl → deliveryList **不通过 storage 传任何数据**（A）。
**F**：storage 何时被首次写入不可证（**F 边界**：resource 不可得）。

---

## 17. deliveryListCtrl 完整数据流图

```
[用户访问任意 deliveryList 相关页面后]
    ↓
[再次进入 deliveryList state]
    ↓
deliveryListCtrl 初始化 (L4075)
    ↓ L4076
JSON.parse(sessionStorage.getItem("chargedeliveryList"))
    ↓ L4077
$scope.obj = store ? store : {}
    ↓ L4078-4105
字段恢复 + 默认值
    ↓ L4078-4086
$scope.obj.startTime / rightTimer (Date)
    ↓ L4088-4100
$scope.obj.deliveryStatus / toBeProcess / $scope.deliveryStatus
    ↓ L4101-4105
$scope.obj.refundStatus
    ↓ L4107-4125
grantAuth.then → getAdminList (ListFactory)
    ↓ L4121-4122
getAdminList.nextPage() → $scope.getAdminList.count
    ↓ L4210
$scope.search() 同步触发
    ↓ L4166-4209
    ├─ L4190 setItem("chargedeliveryList", JSON.stringify($scope.obj))  ← 持久化
    ├─ L4193 searchCount() → L4163 checkCountFactory.saveOrQuery(statProductDeliveryStatus.json, obj)
    └─ L4195-4196 memberFactory = new ListFactory(getCashflowDeliveryVoList.json, pageStart, pageSize, obj)
        ↓ nextPage()
        ↓ Response.items[] + Response.count
        ↓ L4197 promise.then
        └─ L4198 jQuery pagination($scope.memberFactory.count, ...)
    ↓
[HTML 渲染]
    ↓ L31
{{getAdminList.count}} ← 加工记录角标
    ↓ L144/L155/L166
{{checkCountFactory.object.{waitingDeliveryCount, sendToMachineCenterCount, deliveryedCount}}}
    ↓ L202
ng-repeat="item in memberFactory.items"
    ↓
[item 字段渲染]
    ├─ item.patient / item.medicalRecord / item.customer
    ├─ item.{productNames, deliveryStatus, waitingSeconds}
    ├─ item.{waitingDeliveryList, deliveryedList, sendToMachineCenterList}
    ├─ item.waitingExamineList[].medicalExamine.*
    └─ item.cashflow.id
    ↓
[state 跳转 (4 处 + 1 directive)]
    ├─ L253 ui-sref="deliveryInput({cashflowId:item.cashflow.id})"
    ├─ L261/L268 ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"
    ├─ L274 ui-sref="deliveryProcessing({cashflowId:item.cashflow.id})"
    ├─ L285 printFahuoqingdan.print(item.cashflow.id)
    └─ L338 <div print-fahuoqingdan ...>
    ↓
[3 个 detail controller]
    ├─ deliveryInputCtrl (L3812) - 6 API
    ├─ deliveryInputRecordCtrl (L4024) - 4 API
    └─ deliveryProcessingCtrl (L4236) - 2 API
```

**A**：完整 6 层链 A 级闭合（State → Controller → Factory → API → Response → Consumer）。

---

## 18. item 数据来源最终结论（A 级）

### 18.1 item = `memberFactory.items[i]`

- **A**：`item` 来自 `memberFactory.items[i]`
- **A**：`memberFactory.items` 来自 `getCashflowDeliveryVoList.json` Response
- **A**：item 字段 = 后端返回的 items 数组元素

### 18.2 item 字段来源

| 字段 | 来源 | 证据 |
|---|---|---|
| `item.patient.*` | 后端 Response | HTML L211-219 直接渲染 |
| `item.medicalRecord.*` | 后端 Response | HTML L223/L224/L235/L293 |
| `item.customer.*` | 后端 Response | HTML L237/L243 |
| `item.productNames` | 后端 Response | HTML L226 |
| `item.deliveryStatus` | 后端 Response | HTML L206/L229 |
| `item.waitingSeconds` | 后端 Response | HTML L232 |
| `item.waitingDeliveryList` | 后端 Response | HTML L251 |
| `item.deliveryedList` | 后端 Response | HTML L260/L267/L283 |
| `item.sendToMachineCenterList` | 后端 Response | HTML L275 |
| `item.waitingExamineList` | 后端 Response | HTML L303-310 |
| `item.cashflow` | 后端 Response | HTML L253/L261/L268/L274/L285 |
| `item.medicalRecord.id` | 后端 Response | HTML L293/L319 |

**A**：item 全部字段**唯一来源 = 后端 Response**（A）。

### 18.3 item 不来自 storage

**A**：`memberFactory.items` **不来自 storage**（A）。
**A**：storage 仅持久化 `$scope.obj`（查询参数），**不持久化 items**（A）。

---

## 19. 一期冻结事实

| 冻结 | 内容 |
|---|---|
| storage key 精确值 | `chargedeliveryList` |
| storage 读写方 | deliveryListCtrl 唯一（1 读 + 2 写）|
| setItem 触发 | search() + pagination callback |
| storage value | JSON.stringify($scope.obj)（11 字段查询参数）|
| stringify / parse | 100% JSON 包装 |
| removeItem | 0 处（无清理机制）|
| deliveryInputCtrl 是否读写 storage | **否**（L3812-4021 范围 0 处）|
| item 来源 | memberFactory.items（API Response）|
| storage item vs API item | **不同结构**，不可视为同一 collection |
| 3 个 state 跳转 cashflowId 来源 | 100% `item.cashflow.id`（API Response）|
| memberFactory API | getCashflowDeliveryVoList.json（4 参数 ListFactory）|
| pageSize | 12 |
| navigation 5 跳转 | deliveryInput / deliveryInputRecord × 2 / deliveryProcessing / machineOrderList + 1 directive |

---

## 20. 当前 F 边界

| F 项 | 原因 |
|---|---|
| 后端 getCashflowDeliveryVoList.json 完整 Response 字段 | 资源范围外 |
| 后端 items 元素是否按 cashflow 分组 | 不可得 |
| storage 跨 session 持久化周期 | 浏览器行为不可得 |
| storage 何时被首次写入 | 不可得（可能是更早的 deliveryList 访问）|
| 3 个 controller 对应 HTML 模板 | working dir 不可得 |
| 路由表 state → URL 映射 | 资源范围外 |
| directive（throttleinput / print-fahuoqingdan / set-modal / nav-bar）实现 | 资源范围外 |
| filter（gender / howoldFilter / medicalRecordType / deliveryStatus / waitingTime / hidePhone / payedStatus）实现 | 资源范围外 |
| savePatient / hidePatient / hideBrandlist / open1 / open2 函数定义 | controller.js 0 处观察 |
| item 字段与 controller result 字段是否对应同一后端业务实体 | E 推测，无代码直接证据 |

---

## 21. A / B / C / D / E / F 评级

| # | 审计项 | 评级 |
|---|---|---|
| 01 | setItem 全仓 | A（2 处全部 deliveryListCtrl）|
| 02 | getItem 全仓 | A（1 处 deliveryListCtrl）|
| 03 | removeItem | A（全仓 0 处）|
| 04 | storage key 精确值 | A（`chargedeliveryList`）|
| 05 | 写入值结构 | A（11 字段查询参数）|
| 06 | 写入来源 Controller | A（deliveryListCtrl）|
| 07 | 写入对象字段 | A（11 字段）|
| 08 | stringify / parse | A（100% JSON）|
| 09 | deliveryListCtrl 读取位置 | A（L4076）|
| 10 | item 来源 | A（memberFactory.items）|
| 11 | memberFactory vs storage | A（不同结构）|
| 12 | memberFactory 完整追踪 | A |
| 13 | getCashflowDeliveryVoList.json | A |
| 14 | memberFactory.items 消费 | A（HTML 18+ 字段）|
| 15 | item.waitingDeliveryList | A（HTML L251）|
| 16 | item.deliveryedList | A（HTML L260/L267/L283）|
| 17 | item.sendToMachineCenterList | A（HTML L275）|
| 18 | item.deliveryStatus | A（HTML L206/L229）|
| 19 | item.cashflow.id | A（4 处跳转 + 1 print）|
| 20 | item.cashflow 来源 | A（API Response）|
| 21 | deliveryInputCtrl 写 storage | A（**否**，0 处）|
| 22 | deliveryInputCtrl state.go 前后 | A（不写 storage）|
| 23 | storage vs state.go 顺序 | A（**不写**，只跳）|
| 24 | deliveryListCtrl 初始化顺序 | A（sessionStorage → API → HTML）|
| 25 | memberFactory.items → HTML | A（直接 ng-repeat）|
| 26 | deliveryInput state | A（item.waitingDeliveryList → deliveryInput 闭合）|
| 27 | deliveryInputRecord state | A（item.deliveryedList → deliveryInputRecord 闭合）|
| 28 | deliveryProcessing state | A（item.sendToMachineCenterList → deliveryProcessing 闭合）|
| 29 | 完整 item 数据图 | A（6 层 A 级闭合）|
| 30 | Q1-Q30 回答 | A |

**统计**：30 项全部 **A** 级（无 E 升 A / 无 F 升 A）。

---

## 22. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | sessionStorage key / 读写 / value 结构 / item 来源 / 3 state 跳转 cashflowId | **是** |
| L2 业务规则 | "已发货" / "加工中" / "待发货"业务语义 | **E**（基于 HTML 文案）|
| L3 数据库物理模型 | 后端 Response DTO | **F**（资源范围外）|

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
| Q1：chargedeliveryList 是否存在 setItem？| **是**（2 处 L4190/L4203）|
| Q2：chargedeliveryList 是否存在 getItem？| **是**（1 处 L4076）|
| Q3：chargedeliveryList 是否存在 removeItem？| **否**（全仓 0 处）|
| Q4：storage key 精确名称？| **`chargedeliveryList`** |
| Q5：写入值是什么？| `JSON.stringify($scope.obj)`（11 字段查询参数）|
| Q6：是否 JSON.stringify？| **是**（100%）|
| Q7：读取是否 JSON.parse？| **是**（L4076）|
| Q8：写入 Controller 是谁？| **deliveryListCtrl**（唯一）|
| Q9：读取 Controller 是谁？| **deliveryListCtrl**（唯一）|
| Q10：deliveryListCtrl item 来自哪里？| `memberFactory.items`（API Response）|
| Q11：memberFactory 的 API？| `/admin/getCashflowDeliveryVoList.json`（ListFactory 4 参数）|
| Q12：memberFactory.items 是什么？| 后端 Response 的 items 数组 |
| Q13：item.waitingDeliveryList 来源？| API Response（HTML L251）|
| Q14：item.deliveryedList 来源？| API Response（HTML L260/L267/L283）|
| Q15：item.sendToMachineCenterList 来源？| API Response（HTML L275）|
| Q16：item.deliveryStatus 来源？| API Response（HTML L206/L229）|
| Q17：item.cashflow.id 来源？| API Response（HTML 4 处跳转 + 1 print）|
| Q18：deliveryInput state 参数来源？| `item.cashflow.id`（HTML L253）|
| Q19：deliveryInputRecord state 参数来源？| `item.cashflow.id`（HTML L261/L268）|
| Q20：deliveryProcessing state 参数来源？| `item.cashflow.id`（HTML L274）|
| Q21：deliveryInputCtrl 是否写 chargedeliveryList？| **否**（L3812-4021 范围 0 处）|
| Q22：deliveryInputCtrl state.go 前后是否写 storage？| **否**（不写）|
| Q23：deliveryListCtrl 是否同时消费 storage + API？| **是**（storage 恢复 $scope.obj，API 返回 items）|
| Q24：storage item 与 API item 是否可证同一来源？| **否**（不同结构，不可证同一来源）|
| Q25：waitingDeliveryList → deliveryInput 是否闭合？| **是**（item.waitingDeliveryList.length > 0 → ui-sref → deliveryInputCtrl）|
| Q26：deliveryedList → deliveryInputRecord 是否闭合？| **是** |
| Q27：sendToMachineCenterList → deliveryProcessing 是否闭合？| **是** |
| Q28：三个跳转中的 cashflowId 是否都来自 item.cashflow.id？| **是**（100%）|
| Q29：当前 item 数据来源链是否完全闭合？| **是**（6 层 A 级闭合）|
| Q30：当前哪些内容必须 F？| 后端 Response 完整字段 / storage 跨 session 行为 / 3 controller HTML / 路由表 / directive / filter / 未定义函数 / item 字段与 controller result 字段的语义对应（E）|

---

## 25. P0 / P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）

---

## 26. 历史证据 vs 当前代码

### 26.1 S1-81 表述

> deliveryListCtrl 用 sessionStorage 'chargedeliveryList' 恢复 $scope.obj
> deliveryListCtrl 不读 $stateParams.cashflowId
> HTML 4 处 item.cashflow.id 跳转

### 26.2 当前代码（S1-82）

| 项 | S1-81 表述 | 当前代码 | 判定 |
|---|---|---|---|
| storage 读写方 | deliveryListCtrl | **deliveryListCtrl 唯一**（1 读 + 2 写）| **细化** |
| deliveryInputCtrl 是否写 storage | 未提 | **否**（L3812-4021 范围 0 处）| **新增** |
| storage value | 持久化 $scope.obj | 11 字段查询参数 object | **细化** |
| item 来源 | memberFactory.items | memberFactory.items（API Response）| **保留** |
| item.cashflow.id | 4 处跳转来源 | 4 处 + 1 print 共 5 处 | **细化** |
| navigation 5 跳转 | 5 state 跳转 + 1 directive | 同 | **保留** |
| storage item vs API item | 未提 | **不同结构** | **新增** |

### 26.3 最终采用

- **保留**：S1-81 的 5 跳转 + 6 层链
- **新增**：storage 读写方唯一 = deliveryListCtrl（deliveryInputCtrl 不参与）
- **细化**：storage value 是 11 字段查询参数（不包含业务字段）
- **新增**：storage item 与 API item 不可视为同一 collection
- **细化**：4+1 处 item.cashflow.id 全部来自 API Response

---

## 27. 本轮新增事实

1. **`chargedeliveryList` 全仓 3 处全部在 deliveryListCtrl**（1 读 + 2 写，0 处 removeItem）
2. **deliveryInputCtrl L3812-4021 范围 0 处 sessionStorage 操作**（不读不写）
3. **storage value = $scope.obj 序列化**（11 字段查询参数 object）
4. **storage value 不含任何业务字段**（cashflow / patient / waitingDeliveryList / deliveryedList / sendToMachineCenterList 等均不在 storage 内）
5. **JSON.stringify / JSON.parse 100% 使用**
6. **item 唯一来源 = memberFactory.items**（API Response，不来自 storage）
7. **storage item 与 API item 不是同一 collection**（结构完全不同）
8. **4 处 ui-sref 跳转 + 1 处 print 调用 cashflowId 100% 来自 `item.cashflow.id`**
9. **3 个 list 字段（waitingDeliveryList / deliveryedList / sendToMachineCenterList）A 级闭合到 3 个 detail controller**
10. **deliveryListCtrl 自身 0 处访问 `memberFactory.items[i].xxx`**（仅初始化 + 分页 + storage）
11. **完整 6 层数据流图（State→Controller→Factory→API→Response→Consumer）A 级闭合**
12. **9 项 F 边界明确列出**

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
| Git 禁止命令未触发 | ✅（仅 `git add -- 143_*.md`）|

---

## 29. 停止条件

✅ 30 项审计完成（全部 A 级）
✅ 30 问 Q1-Q30 全部回答
✅ 6 层数据流图 A 级闭合
✅ 3 个 list 字段 A 级闭合到 3 个 detail controller
✅ 4+1 处 cashflow.id 来源 A 级确认
✅ storage item vs API item 严格区分
✅ 9 项 F 边界明确列出
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-83）**。
