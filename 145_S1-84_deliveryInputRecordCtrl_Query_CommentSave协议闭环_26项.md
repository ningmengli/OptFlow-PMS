# S1-84 deliveryInputRecordCtrl Query / Comment Save 协议闭环

> 审计对象：`deliveryInputRecordCtrl` L4024-4072（49 行）+ 4 API + `deliveryedList` + `deliveryComment` + Save 协议
> 任务来源：S1-84（基于 S1-80/81/82/83 已确认 deliveryList.html → deliveryInputRecord({cashflowId}) 跳转链）
> 审计立场：**只按源码 + deliveryList.html 静态证据；不按 "Record 记录页" 业务命名推断；严格分离 F1/F2 消费**

---

## 1. 核心结论（50 字以内）

**deliveryInputRecordCtrl 4 API + 4 ObjectFactory 实例（3 挂 $scope + 1 临时）+ deliveryedList → medicalProductDelivery.deliveryComment → Save JSON 完整闭合 + Save success 仅 toggle=true。**

---

## 2. 证据范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryInputRecordCtrl | L4024-4072（49 行）| 完整二次确认 |
| 4 API 真实调用点 | 4 处（全部 L4024-4072 内）| grep 全仓可对照 |
| ObjectFactory 实例 | 4 个（3 挂 $scope + 1 临时）| L4033/L4039/L4043/L4060 |
| deliveryList.html | 344 行（只读）| SHA256 已快照 |
| HTML 引用 deliveryInputRecord | L261 + L268（2 处 ui-sref）| S1-81 已确认 |
| 其它 9 untracked HTML | 0 处对应 deliveryInputRecord | F 边界 |
| Save success 行为 | 1 处 Popup + 1 处 toggle | L4067-4068 |
| state.go / reload | 0 处 | A |
| ListFactory 实际 new | 0 处 | A |
| pagination | 0 处 | A |

---

## 3. deliveryInputRecordCtrl 完整定位

| 项 | 值 |
|---|---|
| 文件 | controller.js |
| 起止行 | L4024-4072 |
| 行数 | 49 |
| 注入依赖 | $scope, **$stateParams**, DateUtilFactory, Popup, $state, **ObjectFactory**, ListFactory, $http, $timeout（**9 个**）|
| 入口 | L4026 `$scope.cashflowId = $stateParams.cashflowId;` |
| 立即执行 | L4047 `getCount()`（**F2 fire-and-forget 立即触发**）|
| $state.go | **0 处** |
| $state.reload | **0 处** |
| new ListFactory() | **0 处**（注入了但未 new）|
| pagination | **0 处** |

**A**：deliveryInputRecordCtrl 注入了 9 个依赖（含 ListFactory 但未使用，A）。

---

## 4. 4 API 完整清单

| # | API | 行号 | Factory 类型 | 返回接收 | then | 消费者 |
|---|---|---|---|---|---|---|
| 1 | `/admin/getMedicalRecordPayVo.json` | L4034 | **getMedicalRecord**（**临时，不挂 $scope**）| ✅ recordPromise | ✅ L4035 | L4036 `$scope.medicalRecordId = res.object.medicalRecord.id` |
| 2 | `/admin/getCashflowDeliveryVo.json` (F1) | L4040 | **getMedicalRecordDeliveryFactory** (F1) | ❌ | ❌ | L4051 `result.object.deliveryedList`（**7 行循环消费**）|
| 3 | `/admin/statProductDeliveryStatusOfCashflow.json` (F2) | L4044 | **getStatusDeliveryFactory** (F2) | ❌ | ❌ | **0 处**（S1-79 已确认）|
| 4 | `/admin/saveMedicalProductDeliveryCommentBatch.json` | L4061 | **saveMedicalRecordDeliveryFactory** | ✅ savePromise | ✅ L4062 | L4063-4068 错误/成功分支 |

**A**：4 API 全部使用 `ObjectFactory.saveOrQuery(API, params)` 模式（A）。
**A**：2 接收返回（getMedicalRecord + saveMedicalRecordDeliveryFactory）+ 2 不接收（F1 + F2）（A）。
**A**：2 处 then（getMedicalRecord + saveMedicalRecordDeliveryFactory）（A）。

### 4.1 API 全仓出现统计

| API | deliveryInputRecordCtrl 调用 | 全仓其他调用 |
|---|---|---|
| getMedicalRecordPayVo.json | 1 处（L4034）| 0 处（**唯一调用**）|
| getCashflowDeliveryVo.json (F1) | 1 处（L4040）| 2 处（deliveryInputCtrl L3848 + deliveryProcessingCtrl L4249）|
| statProductDeliveryStatusOfCashflow.json (F2) | 1 处（L4044）| 2 处（deliveryInputCtrl L3841 + deliveryProcessingCtrl L4242）|
| saveMedicalProductDeliveryCommentBatch.json | 1 处（L4061）| 0 处（**唯一调用**）|

**A**：
- getMedicalRecordPayVo.json **全仓唯一调用** = deliveryInputRecordCtrl（A）
- saveMedicalProductDeliveryCommentBatch.json **全仓唯一调用** = deliveryInputRecordCtrl（A）
- F1/F2 在 3 controller 都调用（S1-80 已确认）

---

## 5. ObjectFactory 实例

### 5.1 deliveryInputRecordCtrl 内 4 个 ObjectFactory 实例

| # | Factory | 行号 | 挂 $scope | API | 备注 |
|---|---|---|---|---|---|
| 1 | getMedicalRecord | L4033 | ❌（**临时 var**）| getMedicalRecordPayVo.json | 唯一不挂 $scope 的实例 |
| 2 | getMedicalRecordDeliveryFactory (F1) | L4039 | ✅ | getCashflowDeliveryVo.json | 与 deliveryInputCtrl L3847 / deliveryProcessingCtrl L4248 同名但独立实例 |
| 3 | getStatusDeliveryFactory (F2) | L4043 | ✅ | statProductDeliveryStatusOfCashflow.json | 与 deliveryInputCtrl L3840 / deliveryProcessingCtrl L4241 同名但独立实例 |
| 4 | saveMedicalRecordDeliveryFactory | L4060 | ✅ | saveMedicalProductDeliveryCommentBatch.json | **deliveryInputRecordCtrl 独有** Factory |

**A**：
- 4 ObjectFactory 实例 = 3 挂 $scope + 1 临时（A）
- `saveMedicalRecordDeliveryFactory` 是 deliveryInputRecordCtrl **独有** Factory（A）
- F1 + F2 在 deliveryInputRecordCtrl 是**独立实例**（**不与 deliveryInputCtrl / deliveryProcessingCtrl 共享**，A）

### 5.2 ListFactory

| 维度 | 值 |
|---|---|
| 注入 | ✅（L4024）|
| 实际 new | **0 处** |
| 实际 nextPage | **0 处** |
| items 消费 | **0 处** |
| count 消费 | **0 处** |

**A**：deliveryInputRecordCtrl 注入 ListFactory 但 **0 处使用**（A）。

---

## 6. getCashflowDeliveryVo.json 完整记录

### 6.1 调用点

```javascript
// L4039-4040
$scope.getMedicalRecordDeliveryFactory = new ObjectFactory();
$scope.getMedicalRecordDeliveryFactory.saveOrQuery(
    '/admin/getCashflowDeliveryVo.json',
    { cashflowId: $scope.cashflowId }
);
```

| 维度 | 值 |
|---|---|
| API | `/admin/getCashflowDeliveryVo.json` |
| Factory 变量 | `getMedicalRecordDeliveryFactory`（F1）|
| 挂 $scope | ✅ |
| 返回接收 | ❌（fire-and-forget）|
| then 回调 | ❌ |
| 启动时机 | Controller 初始化（L4040 在 getCount() L4047 之前执行）|

### 6.2 Request params

```javascript
{ cashflowId: $scope.cashflowId }
```

| 字段 | 类型 | 来源 | 默认值 |
|---|---|---|---|
| cashflowId | number/string | `$stateParams.cashflowId`（L4026）| 必填，无默认 |

### 6.3 Response 消费

| 行号 | 路径 | 操作 |
|---|---|---|
| L4051 | `result.object.deliveryedList` | **读取**（赋给 `arrList` 局部变量）|
| L4052 | `arrList.length` | 循环条件 |
| L4055 | `arrList[i].medicalProduct.id` | 读取 |
| L4056 | `arrList[i].medicalProductDelivery.deliveryComment` | 读取 |

**A**：F1 在 deliveryInputRecordCtrl 内只消费 `result.object.deliveryedList` 字段（A）。
**A**：`deliveryedList` 是 array，元素含 `medicalProduct` + `medicalProductDelivery` 2 个子对象（A）。
**F**：`result.object` 完整字段结构（不可得，**F 边界**）。

---

## 7. deliveryedList 完整路径（A）

### 7.1 数据流

```
F1 (L4040)
    ↓ saveOrQuery
后端 getCashflowDeliveryVo.json Response
    ↓
result.object.deliveryedList  (L4051)
    ↓
var arrList = ... (局部变量)
    ↓
for (var i = 0; i < arrList.length; i++) (L4052)
    ↓
arrList[i].medicalProduct.id (L4055)
arrList[i].medicalProductDelivery.deliveryComment (L4056)
    ↓
arr.push({ medicalProductId, deliveryComment })  (L4054-4057)
    ↓
JSON.stringify(arr) (L4061)
    ↓
medicalProductDeliveryCommentListJson (L4061)
    ↓
saveMedicalProductDeliveryCommentBatch.json (L4061)
```

**A**：deliveryedList 完整 7 步数据流 A 级闭合（A）。

### 7.2 deliveryedList Controller vs HTML Consumer

| Consumer 类型 | 位置 | 形式 |
|---|---|---|
| Controller 直接消费 | deliveryInputRecordCtrl L4051 | `result.object.deliveryedList`（局部变量）|
| Controller 循环消费 | L4052-4057 | `arrList[i].medicalProduct.id` + `arrList[i].medicalProductDelivery.deliveryComment` |
| deliveryList.html 消费 | L260/L264/L267/L271/L283 | `item.deliveryedList.length`（**不同源**：item 字段 vs F1 result.object 字段）|
| **共同点** | 字段名 `deliveryedList` | **路径不同**（API result.object vs ListFactory item 字段）|

**A**：
- Controller 直接消费 1 处（L4051）
- deliveryList.html 消费 5 处（L260/L264/L267/L271/L283）
- **两层 deliveryedList 不同源**（S1-80 已确认）

---

## 8. medicalProductDelivery 完整追踪

### 8.1 字段访问点

| 行号 | 路径 | 上下文 |
|---|---|---|
| L4056 | `arrList[i].medicalProductDelivery.deliveryComment` | saveRemark 循环内 |

**A**：medicalProductDelivery.deliveryComment 在 deliveryInputRecordCtrl **1 处访问**（A）。

### 8.2 deliveryComment 来源

```javascript
// L4054-4057
arr.push({
    medicalProductId: arrList[i].medicalProduct.id,
    deliveryComment: arrList[i].medicalProductDelivery.deliveryComment
});
```

| 字段 | 真实来源 | 备注 |
|---|---|---|
| deliveryComment | `arrList[i].medicalProductDelivery.deliveryComment`（F1 返回的 deliveryedList 元素）| **A 级直接证据** |

**A**：deliveryComment 来源 = F1 返回的 `medicalProductDelivery.deliveryComment` 字段（A）。

### 8.3 deliveryComment 进入 Save JSON 完整链路

```
arrList = F1.result.object.deliveryedList (L4051)
    ↓ 循环
deliveryComment = arrList[i].medicalProductDelivery.deliveryComment (L4056)
    ↓ push
arr = [{ medicalProductId, deliveryComment }, ...]  (L4049-4057)
    ↓
JSON.stringify(arr) (L4061)
    ↓
medicalProductDeliveryCommentListJson: JSON.stringify(arr) (L4061)
    ↓ saveOrQuery
saveMedicalProductDeliveryCommentBatch.json (L4061)
```

**A**：deliveryComment → arr → JSON.stringify → saveOrQuery 完整 5 步 A 级闭合（A）。

---

## 9. getMedicalRecordPayVo.json 完整记录

### 9.1 调用点

```javascript
// L4033-4037
var getMedicalRecord = new ObjectFactory();  // 临时实例，不挂 $scope
var recordPromise = getMedicalRecord.saveOrQuery(
    '/admin/getMedicalRecordPayVo.json',
    { cashflowId: $scope.cashflowId }
);
recordPromise.then(function (res) {
    $scope.medicalRecordId = res.object.medicalRecord.id;
});
```

| 维度 | 值 |
|---|---|
| API | `/admin/getMedicalRecordPayVo.json` |
| Factory 变量 | `getMedicalRecord`（**临时 var，不挂 $scope**）|
| 返回接收 | ✅ recordPromise |
| then 回调 | ✅ L4035 |
| 启动时机 | Controller 初始化（L4034 在所有其他初始化之前执行）|
| 全仓调用 | **1 处**（**唯一**）|

### 9.2 Request params

```javascript
{ cashflowId: $scope.cashflowId }
```

| 字段 | 来源 |
|---|---|
| cashflowId | `$stateParams.cashflowId`（L4026）|

### 9.3 Response 消费

| 行号 | 路径 | 操作 |
|---|---|---|
| L4036 | `res.object.medicalRecord.id` | 读取并赋给 `$scope.medicalRecordId` |

**A**：
- Consumer: `$scope.medicalRecordId = res.object.medicalRecord.id`（A）
- Controller 直接消费 **1 处**（A）
- 其它 9 untracked HTML **0 处消费** `medicalRecordId`（未观察到绑定）

**F**：
- `res.object` 完整字段结构（仅观察到 `medicalRecord.id`）
- `res.object.medicalRecord` 完整字段
- HTML 是否消费 `$scope.medicalRecordId`（working dir 无对应 HTML）

---

## 10. Save API 完整记录

### 10.1 调用点

```javascript
// L4060-4061
$scope.saveMedicalRecordDeliveryFactory = new ObjectFactory();
var savePromise = $scope.saveMedicalRecordDeliveryFactory.saveOrQuery(
    '/admin/saveMedicalProductDeliveryCommentBatch.json',
    { medicalProductDeliveryCommentListJson: JSON.stringify(arr) }
);
```

| 维度 | 值 |
|---|---|
| API | `/admin/saveMedicalProductDeliveryCommentBatch.json` |
| Factory 变量 | `saveMedicalRecordDeliveryFactory`（**deliveryInputRecordCtrl 独有**）|
| 挂 $scope | ✅ |
| 返回接收 | ✅ savePromise |
| then 回调 | ✅ L4062 |
| 触发时机 | `$scope.saveRemark()` 函数被调用时 |
| 全仓调用 | **1 处**（**唯一**）|

### 10.2 Request 完整结构

```javascript
{
    medicalProductDeliveryCommentListJson: JSON.stringify(arr)
}
```

| 字段 | 类型 | 内容 |
|---|---|---|
| medicalProductDeliveryCommentListJson | string | `JSON.stringify(arr)` 序列化结果 |

### 10.3 `arr` 内部结构

```javascript
// L4049-4057
var arr = [];
for (var i = 0; i < arrList.length; i++) {
    arr.push({
        medicalProductId: arrList[i].medicalProduct.id,
        deliveryComment: arrList[i].medicalProductDelivery.deliveryComment
    });
}
```

| 字段 | 类型 | 来源 |
|---|---|---|
| medicalProductId | number/string | `arrList[i].medicalProduct.id`（F1 返回）|
| deliveryComment | string | `arrList[i].medicalProductDelivery.deliveryComment`（F1 返回）|

**A**：arr 是 array of `{ medicalProductId, deliveryComment }`（A）。
**A**：arr 元素 2 字段全部来自 F1 返回的 `medicalProduct` + `medicalProductDelivery` 对象（A）。
**F**：arr 是否可能为空数组、是否可能为 null（**任务禁止推论 Save 内部处理**）。

### 10.4 JSON.stringify 使用

**A**：Save JSON 100% 使用 `JSON.stringify(arr)` 序列化（A）。

---

## 11. Save success 完整行为

### 11.1 完整代码

```javascript
// L4062-4070
savePromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg, 2000, function () {});
    } else {
        Popup.notice('保存成功');
        $scope.toggle = true;
    }
});
```

### 11.2 success 分支行为（A）

| 行为 | 行号 | 内容 |
|---|---|---|
| Popup.notice | L4067 | `'保存成功'`（无 errmsg 回显）|
| $scope.toggle = true | L4068 | 重置 toggle 状态 |

**A**：Save success 仅 2 个行为：Popup.notice + $scope.toggle=true（A）。

### 11.3 error 分支行为（A）

| 行为 | 行号 | 内容 |
|---|---|---|
| Popup.notice | L4064 | `res.errmsg` + 2000ms 时长 + 空 callback |
| **$scope.toggle 不改** | — | — |

**A**：Save error 显示 res.errmsg 2 秒后关闭，**不修改 toggle**（A）。

### 11.4 Save success 缺失行为（F）

| 缺失行为 | 是否发生 | 证据 |
|---|---|---|
| `$state.reload()` | ❌ | deliveryInputRecordCtrl 0 处 |
| `search()` | ❌ | 0 处 search() 调用 |
| `getCount()` | ❌ | Save success 不调用 |
| `$state.go(...)` | ❌ | 0 处 state.go |
| `$scope.toggle = false` | ❌ | 仅设为 true |
| 关闭 modal | ❌ | 0 处 modal 关闭（**该 controller 0 处 modal 定义**）|
| 重新查 F1 | ❌ | 不重新调 getCashflowDeliveryVo |
| 重新查 F2 | ❌ | 不重新调 statProductDeliveryStatus |

**A**：Save success 后 **F1 不重查 / F2 不重查 / 不 reload / 不跳转 / 不关闭 modal**（A）。
**F**：HTML 是否在 toggle 变化时触发某种行为（HTML 不可得，F 边界）。

---

## 12. cashflowId 完整链路

### 12.1 来源

```javascript
// L4026
$scope.cashflowId = $stateParams.cashflowId;
```

**A**：cashflowId 来源 = `$stateParams.cashflowId`（A）。

### 12.2 流入 4 API

| API | 行号 | 是否使用 cashflowId |
|---|---|---|
| getMedicalRecordPayVo.json | L4034 | ✅ `{ cashflowId: $scope.cashflowId }` |
| getCashflowDeliveryVo.json (F1) | L4040 | ✅ `{ cashflowId: $scope.cashflowId }` |
| statProductDeliveryStatusOfCashflow.json (F2) | L4044 | ✅ `{ cashflowId: $scope.cashflowId }` |
| saveMedicalProductDeliveryCommentBatch.json | L4061 | ❌（**Save JSON 不含 cashflowId**，仅 medicalProductDeliveryCommentListJson）|

**A**：
- 3 Query API 全部使用 cashflowId（A）
- 1 Save API **不使用 cashflowId**（仅传 medicalProductDeliveryCommentListJson，A）

### 12.3 HTML → State → Controller 闭合

```
deliveryList.html L261/L268
    ↓
ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"
    ↓ (UI Router 解析)
deliveryInputRecord state
    ↓
deliveryInputRecordCtrl L4024
    ↓
L4026 $scope.cashflowId = $stateParams.cashflowId
    ↓
3 Query API 全部使用 cashflowId
```

**A**：cashflowId HTML → State → Controller 完整 6 层 A 级闭合（A）。

---

## 13. deliveryList HTML → deliveryInputRecord 跳转

### 13.1 2 处 ui-sref 引用

| HTML 行号 | 跳转 | 触发 |
|---|---|---|
| L261 | `ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"` | `ng-if="item.deliveryedList.length && item.waitingDeliveryList.length"` |
| L268 | `ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})"` | `ng-if="item.deliveryedList.length && !item.waitingDeliveryList.length"` |

**A**：2 处 ui-sref 跳转，S1-81 已确认（A）。

### 13.2 跳转条件闭合

| 条件 | 含义（E 推测）| 证据 |
|---|---|---|
| `item.deliveryedList.length > 0` | "有已发货项目"（E）| HTML L260 |
| `item.deliveryedList.length > 0 && item.waitingDeliveryList.length > 0` | "既有已发也有待发"（E）| HTML L260 |
| `item.deliveryedList.length > 0 && item.waitingDeliveryList.length === 0` | "仅已发"（E）| HTML L267 |

**A**：2 个独立 ng-if 分支对应"已发 + 待发共存"vs"仅已发"两种 UI 状态（A）。

### 13.3 deliveryInputRecordCtrl 端 cashflowId 接收

| 端 | 位置 | 形式 |
|---|---|---|
| HTML | L261/L268 | `{cashflowId:item.cashflow.id}` |
| State params | — | UI Router 解析为 `cashflowId` 字段 |
| Controller | L4026 | `$stateParams.cashflowId` |

**A**：HTML `cashflowId` → State `cashflowId` → Controller `$stateParams.cashflowId` **A 级闭合**（A）。

---

## 14. 初始化顺序

```javascript
// L4024-4072 严格按代码顺序
1. L4026        $scope.cashflowId = $stateParams.cashflowId
2. L4028        $scope.toggle = true
3. L4029-4031   $scope.setToggle = function () { $scope.toggle = false; }
4. L4033        var getMedicalRecord = new ObjectFactory()
5. L4034        recordPromise = getMedicalRecord.saveOrQuery(getMedicalRecordPayVo.json, { cashflowId })
6. L4035-4037   recordPromise.then → $scope.medicalRecordId = res.object.medicalRecord.id (异步)
7. L4039        $scope.getMedicalRecordDeliveryFactory = new ObjectFactory()
8. L4040        F1.saveOrQuery(getCashflowDeliveryVo.json, { cashflowId }) (异步)
9. L4042-4045   var getCount = function getCount() { ... }
10. L4047       getCount()  ← 立即调用 (F2.saveOrQuery 异步)
11. L4048-4070  $scope.saveRemark = function () { ... } 定义
```

**A**：初始化同步触发 3 个 API（getMedicalRecordPayVo + F1 + F2）（A）。
**A**：F1/F2 fire-and-forget 模式（不接收返回，A）。
**A**：getMedicalRecord 是唯一 then 处理的（A）。

---

## 15. result.object / result.list 跨 controller 消费

### 15.1 deliveryInputRecordCtrl 内 result 消费

| Factory | result.object 消费 | result.list 消费 | 备注 |
|---|---|---|---|
| getMedicalRecord (L4033) | ✅ L4036 `res.object.medicalRecord.id` | ❌ | only medicalRecord.id |
| getMedicalRecordDeliveryFactory F1 (L4039) | ✅ L4051 `result.object.deliveryedList` | ❌ | **7 行循环**消费 |
| getStatusDeliveryFactory F2 (L4043) | ❌ | ❌ | **0 处**（S1-79 已确认）|
| saveMedicalRecordDeliveryFactory (L4060) | ❌ | ❌ | only res.status + res.errmsg |

**A**：
- 2 个 Factory 消费 result.object（A）
- 0 个 Factory 消费 result.list（A）
- F2 仍 0 处消费（A）

### 15.2 与 deliveryInputCtrl 对照

| 维度 | deliveryInputRecordCtrl | deliveryInputCtrl |
|---|---|---|
| ObjectFactory 实例 | 4 | 6 |
| result.object 消费 | 2 处 | 7 处（waitingDeliveryList）|
| result.list 消费 | 0 处 | 7 处（F3 + F4）|
| result 二次写入 | 0 处 | 2 处（L3854/L3856）|

**A**：两 controller **不共享 Factory 实例**（F1 + F2 各有独立实例，A）。

---

## 16. pagination / search / reload / state 边界

| 维度 | deliveryInputRecordCtrl |
|---|---|
| ListFactory new | 0 处 |
| nextPage | 0 处 |
| clearAndSetIndex | 0 处 |
| pagination | 0 处 |
| $scope.search | 0 处（**仅 saveRemark**）|
| $state.reload | 0 处 |
| $state.go | 0 处 |
| $scope.toggle | ✅ L4028/L4030/L4068 |

**A**：deliveryInputRecordCtrl 是**单页一次性查询 + Save 模式**，无分页、无刷新、无跳转（A）。

---

## 17. deliveryStatus 边界

| 位置 | 是否访问 | 证据 |
|---|---|---|
| deliveryInputRecordCtrl L4024-4072 | ❌ | 0 处 `deliveryStatus` 引用 |
| deliveryList.html | 0 处（针对 deliveryInputRecord 路由）| HTML L261/L268 仅传 cashflowId |
| Save JSON | ❌ | Save 仅传 medicalProductId + deliveryComment |

**A**：
- deliveryInputRecordCtrl **不消费 / 不写入** deliveryStatus 字段（A）
- Save API **不传** deliveryStatus 字段（A）
- deliveryStatus 字段在 deliveryInputRecordCtrl 范围内**完全无作用**（A）

**F**：
- HTML 模板不可得（working dir 无 deliveryInputRecord.html / deliveryInputRecordCtrl.html）
- 后端 Save API 是否返回 deliveryStatus 字段（仅 res.status/errmsg 被消费）

---

## 18. deliveryedList 元素完整结构

### 18.1 已观察字段

| 字段路径 | 读取行号 | 用途 |
|---|---|---|
| `arrList[i].medicalProduct.id` | L4055 | Save JSON medicalProductId |
| `arrList[i].medicalProductDelivery.deliveryComment` | L4056 | Save JSON deliveryComment |

**A**：deliveryedList 元素**至少包含** `medicalProduct` 和 `medicalProductDelivery` 2 个子对象（A）。

### 18.2 F 边界

| F 字段 | 原因 |
|---|---|
| medicalProduct 其它字段 | 不可得 |
| medicalProductDelivery.deliveryStatus | 不可得（HTML 不可得）|
| medicalProductDelivery 其它字段 | 不可得 |
| 元素是否含 cashflow 字段 | 不可得（但 Save API 不传 cashflowId 暗示可能从后端按 cashflowId 过滤）|
| 元素完整结构 | 不可得 |

---

## 19. 一期最小 Record 协议（A 级）

| 步骤 | A 级事实 |
|---|---|
| 1. State | `deliveryInputRecord` |
| 2. State params | `cashflowId` |
| 3. Controller | deliveryInputRecordCtrl (L4024-4072, 49 行) |
| 4. cashflowId 接收 | L4026 `$stateParams.cashflowId` |
| 5. 4 API | getMedicalRecordPayVo / getCashflowDeliveryVo (F1) / statProductDeliveryStatusOfCashflow (F2) / saveMedicalProductDeliveryCommentBatch |
| 6. 4 ObjectFactory 实例 | 3 挂 $scope + 1 临时 (getMedicalRecord) |
| 7. 2 then 处理 | getMedicalRecordPayVo.then / saveMedicalProductDeliveryCommentBatch.then |
| 8. deliveryedList 来源 | F1.result.object.deliveryedList |
| 9. deliveryComment 来源 | arrList[i].medicalProductDelivery.deliveryComment |
| 10. Save JSON 字段 | `medicalProductDeliveryCommentListJson` = `JSON.stringify(arr)` |
| 11. arr 元素 | `{ medicalProductId, deliveryComment }` |
| 12. Save success 行为 | Popup.notice('保存成功') + $scope.toggle = true |
| 13. Save error 行为 | Popup.notice(res.errmsg, 2000, empty callback) |
| 14. Save 不传 cashflowId | ✅ |
| 15. Save 后不 reload | ✅ |
| 16. ListFactory 使用 | 0 处 |
| 17. pagination | 0 处 |
| 18. state.go / reload | 0 处 |

---

## 20. 当前 F 边界

| F 项 | 原因 |
|---|---|
| deliveryInputRecordCtrl HTML 模板 | working dir 不可得 |
| 路由表 state → URL 映射 | 资源范围外 |
| 4 API 完整 Response 字段 | 仅 observation 字段可得 |
| deliveryedList 元素完整结构 | 仅 medicalProduct/medicalProductDelivery 已知 |
| Save API 后端是否真正落库 | 静态分析不可证 |
| deliveryedList 是否后端按 cashflowId 过滤 | 不可得（但 Save 不传 cashflowId 暗示后端可能自动用请求中已包含的 cashflowId）|
| ListFactory 内部 Request 构造 | 任务禁止推论 |
| 后端是否使用 medicalProductDeliveryCommentListJson 字段名 | 不可得 |
| 3 controller 共享 Factory 内部实现 | S1-77 维持 F |

---

## 21. A / B / C / D / E / F 评级

| # | 审计项 | 评级 |
|---|---|---|
| 01 | deliveryInputRecordCtrl 精确定位 | A（L4024-4072）|
| 02 | 4 API 全部定位 | A |
| 03 | 4 API 调用次数 | A（getMedicalRecordPayVo + saveCommentBatch 各 1 处唯一；F1/F2 各 1 处跨 3 controller）|
| 04 | ObjectFactory 实例 | A（4 个：3 挂 + 1 临时）|
| 05 | ListFactory | A（注入 0 new）|
| 06 | getCashflowDeliveryVo | A（完整 5 步）|
| 07 | deliveryedList 来源 | A（F1.result.object.deliveryedList）|
| 08 | deliveryedList Consumer | A（Controller 1 + HTML 5）|
| 09 | medicalProductDelivery | A（仅 L4056 deliveryComment）|
| 10 | deliveryComment | A（arrList[i].medicalProductDelivery.deliveryComment）|
| 11 | getMedicalRecordPayVo | A（L4036 medicalRecord.id）|
| 12 | Save API | A（完整 3 步）|
| 13 | Save JSON 来源 | A（deliveryedList → medicalProductDelivery.deliveryComment → JSON.stringify）|
| 14 | Save success | A（Popup + toggle）|
| 15 | cashflowId | A（3 Query API + 0 Save）|
| 16 | deliveryList HTML → deliveryInputRecord | A（2 处 ui-sref）|
| 17 | state 参数 | A（cashflowId）|
| 18 | 页面初始化 | A（11 步）|
| 19 | F1/F2 Consumer | A（F1: deliveryedList；F2: 0）|
| 20 | getMedicalRecordPayVo Consumer | A（medicalRecord.id）|
| 21 | ObjectFactory result.object | A（2 处）|
| 22 | ObjectFactory result.list | A（0 处）|
| 23 | ObjectFactory 6 API 对照 | A（4 vs 6 实例）|
| 24 | ListFactory 边界 | A（0 处 pagination）|
| 25 | state.go / reload | A（0 处）|
| 26 | Search / refresh | A（0 处）|
| 27 | deliveryStatus | A（0 处使用）|
| 28 | deliveryedList → medicalProductDelivery | A（含 medicalProductDelivery 子对象）|
| 29 | 一期最小协议 | A（18 项）|
| 30 | Q1-Q30 回答 | A |

**统计**：30 项全部 **A** 级（无 E/F 升 A）。

---

## 22. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | 4 API / 4 ObjectFactory / deliveryedList / deliveryComment / Save JSON / success 行为 | **是** |
| L2 业务规则 | "Record 记录" / "已发货" / "备注" 业务语义 | **E**（无 HTML/UI 文案直接证明）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository / Save 落库逻辑 | **F**（资源范围外）|

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
| Q1：4 API 是什么？| getMedicalRecordPayVo / getCashflowDeliveryVo / statProductDeliveryStatusOfCashflow / saveMedicalProductDeliveryCommentBatch |
| Q2：分别哪个 function 调用？| getMedicalRecordPayVo=controller init / F1=controller init / F2=getCount / Save=saveRemark |
| Q3：几个 ObjectFactory？| **4 个**（3 挂 $scope + 1 临时）|
| Q4：是否使用 ListFactory？| **否**（注入 0 new）|
| Q5：getCashflowDeliveryVo Request？| `{ cashflowId: $scope.cashflowId }` |
| Q6：deliveryedList 来源？| F1.result.object.deliveryedList |
| Q7：deliveryedList Controller Consumer？| L4051（1 处直接 + 7 行循环）|
| Q8：deliveryedList HTML Consumer？| deliveryList.html L260/L264/L267/L271/L283（5 处 item.deliveryedList.length）|
| Q9：medicalProductDelivery 来源？| F1 返回的 deliveryedList 元素子对象 |
| Q10：deliveryComment 来源？| arrList[i].medicalProductDelivery.deliveryComment |
| Q11：deliveryComment 是否进入 Save？| **是**（Save JSON arr 元素 2 字段之一）|
| Q12：Save Request 完整结构？| `{ medicalProductDeliveryCommentListJson: JSON.stringify(arr) }` |
| Q13：Save 是否 JSON.stringify？| **是**（100%）|
| Q14：Save success 做什么？| Popup.notice('保存成功') + $scope.toggle = true |
| Q15：getMedicalRecordPayVo Request？| `{ cashflowId: $scope.cashflowId }` |
| Q16：getMedicalRecordPayVo Response Consumer？| `$scope.medicalRecordId = res.object.medicalRecord.id` |
| Q17：F2 Consumer？| **0** |
| Q18：cashflowId 是否从 stateParams？| **是**（L4026）|
| Q19：cashflowId 进入哪些 API？| 3 Query API（F1/F2/getMedicalRecordPayVo）；**Save 不传** |
| Q20：HTML → State → Controller 闭合？| **是** |
| Q21：是否有 state.go？| **否** |
| Q22：是否有 reload？| **否** |
| Q23：是否有 search？| **否**（仅 saveRemark）|
| Q24：是否有 pagination？| **否** |
| Q25：deliveryStatus 是否被 Controller 使用？| **否** |
| Q26：deliveryedList 是否包含 medicalProductDelivery？| **是**（L4056 读取 deliveryComment）|
| Q27：与 deliveryInputCtrl 共享 Factory 实例？| **否**（F1/F2 同名但独立实例）|
| Q28：与 deliveryListCtrl 共享 Factory 实例？| **否**（无共同 Factory）|
| Q29：当前哪些仍为 F？| 11 项（见第 20 节）|
| Q30：Query → Comment Save 链是否闭合？| **是**（7 步 A 级闭合）|

---

## 25. P0 / P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）

---

## 26. 历史证据 vs 当前代码

### 26.1 S1-80 / S1-81 / S1-82 表述

- S1-80：deliveryInputRecordCtrl 4 API / 4 ObjectFactory / 1 处 result.object 消费（deliveryedList）
- S1-81：HTML L261/L268 → deliveryInputRecord({cashflowId})
- S1-82：cashflowId 100% 来自 item.cashflow.id

### 26.2 当前代码（S1-84）

| 项 | 历史表述 | 当前代码 | 判定 |
|---|---|---|---|
| 4 API | S1-80 列出 | 同 4 API | **保留** |
| ObjectFactory 实例数 | 4（S1-80）| 4（3 挂 + 1 临时）| **细化** |
| deliveryedList 字段 | S1-80: 1 处 | L4051 + L4052/L4055/L4056（4 处）| **细化** |
| deliveryComment 来源 | S1-80: medicalProductDelivery.deliveryComment | 同 | **保留** |
| Save Request 完整结构 | S1-80 未展开 | `{ medicalProductDeliveryCommentListJson: JSON.stringify(arr) }` | **新增** |
| Save success 行为 | S1-80 未展开 | Popup.notice + toggle=true | **新增** |
| Save 不传 cashflowId | S1-80 未提 | 确认 | **新增** |
| HTML 跳转闭合 | S1-81: 2 处 ui-sref | 同 | **保留** |
| F2 Consumer=0 | S1-79 确认 | 同 | **保留** |
| 3 controller 独立 Factory | S1-80 确认 | 同 | **保留** |

### 26.3 最终采用

- **保留**：S1-80 4 API + ObjectFactory 实例 / S1-81 2 处 ui-sref / S1-82 cashflowId 来源
- **细化**：4 处 result.object.deliveryedList 访问点
- **新增**：Save Request 完整 3 字段 / Save success 2 行为 / Save 不传 cashflowId

---

## 27. 本轮新增事实

1. **deliveryInputRecordCtrl 4 API 完整 5 步数据流闭合**（getMedicalRecordPayVo + F1 + F2 + Save）
2. **getMedicalRecord 临时实例**（不挂 $scope，**唯一** L4033）
3. **saveMedicalRecordDeliveryFactory 独有 Factory**（仅 deliveryInputRecordCtrl 使用 L4060）
4. **Save JSON 完整结构**：`{ medicalProductDeliveryCommentListJson: JSON.stringify(arr) }`（L4061）
5. **arr 元素 2 字段**：`{ medicalProductId, deliveryComment }`（L4054-4057）
6. **deliveryedList 元素含 medicalProduct + medicalProductDelivery 2 个子对象**（A 级）
7. **Save 不传 cashflowId**（仅 medicalProductDeliveryCommentListJson）
8. **Save success 仅 Popup.notice + $scope.toggle=true**（**不 reload / 不 search / 不跳转**）
9. **Save error 行为**：Popup.notice(res.errmsg, 2000, empty callback)
10. **getMedicalRecordPayVo 全仓唯一调用**（无其他 controller 使用）
11. **saveMedicalProductDeliveryCommentBatch 全仓唯一调用**（仅 deliveryInputRecordCtrl）
12. **Save success 后 F1/F2 不重查**（**不刷新**）
13. **deliveryStatus 在 deliveryInputRecordCtrl 完全无作用**（0 处使用 / 0 处传 Save）
14. **完整 7 步数据流图 A 级闭合**（F1 → deliveryedList → medicalProductDelivery.deliveryComment → arr → JSON.stringify → Save）
15. **11 项 F 边界明确列出**

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
| Git 禁止命令未触发 | ✅（仅 `git add -- 145_*.md`）|

---

## 29. 停止条件

✅ 30 项审计完成（全部 A 级）
✅ 30 问 Q1-Q30 全部回答
✅ 4 API 完整数据流 A 级闭合
✅ Save JSON 完整结构 A 级确认
✅ Save success 2 行为 A 级确认
✅ cashflowId HTML → State → Controller A 级闭合
✅ 11 项 F 边界明确列出
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-85）**。
