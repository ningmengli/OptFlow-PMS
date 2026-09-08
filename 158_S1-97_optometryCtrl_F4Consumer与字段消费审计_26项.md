# S1-97 optometryCtrl F4 Consumer 与字段消费审计

> **任务名**：S1-97｜F4 getCanBeDeliverySkuInListOfProduct 第二 Consumer：optometryCtrl 全链路审计（26项）
> **审计范围**：controller.js 中 `optometryCtrl`（L34776-L35382）+ F4 调用完整链路 + 7 HTML 不可得检查
> **当前轮次**：S1-97（接 S1-96 完成）
> **本轮承诺**：F4 实际调用 = 0；Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| controller.js optometryCtrl（L34776-L35382） | ✅ | 核心审计对象 |
| controller.js optometryGlassesCtrl / optometryListCtrl | ❌ | 不同 controller，optometryCtrl 结束于 L35382 |
| controller.js deliveryInputCtrl（L3812-L4021） | ⚠️ 旁证 | 仅做对照 |
| 7 HTML | ✅（只读） | **0 处 optometry**（HTML 不可得） |
| 视光之家url.txt 中 optometry URL | ⚠️ 旁证 | 仅 URL，无 schema |
| F4 后端实现 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "同一 API = 同一业务流程"（E 升 A 禁止）
- "同一 API = 同一实例 / 同一共享数据"（E 升 A 禁止）
- "optometryCtrl 调用了 F4 = optometryCtrl 与 deliveryInputCtrl 共享业务对象"（E 升 A 禁止）
- deliveryInputCtrl ↔ optometryCtrl 必须严格区分：API / Factory / Request / Scope / Result / 中间对象 / Write API

---

## 3. optometryCtrl 定位

### 3.1 Controller 注册（A 级）

```javascript
// L34776
angular.module("bestvisionWeb").controller("optometryCtrl", [
    "$scope", "Popup", "$state", "ObjectFactory", "ListFactory", "$timeout", "DateUtilFactory",
    function ($scope, Popup, $state, ObjectFactory, ListFactory, $timeout, DateUtilFactory) {
        // ...
    }
]);
```

### 3.2 注入依赖（A 级）

| 依赖 | 用途 |
|---|---|
| $scope | Scope |
| Popup | 弹窗工具 |
| $state | 路由跳转 |
| **ObjectFactory** | 全部 saveOrQuery 用（17 处） |
| ListFactory | 1 处（L35367 selectMedicalRecordFlowVoList） |
| $timeout | L35113 setTimeout 包装 |
| DateUtilFactory | 时间工具（未在本轮使用） |

### 3.3 范围与终止（A 级）

| 维度 | 范围 |
|---|---|
| 起始行 | L34776 |
| 终止行 | L35382（下一 controller `optometryGlassesCtrl` 注册于 L35383） |
| 物理跨度 | **607 行** |
| 17 处 saveOrQuery | L34785/34795/34843/34862/34885/34914/34947/35054/35099/35150/35167/35185/35204/35253/35281/35319/35342 |
| 1 处 ListFactory | L35367 selectMedicalRecordFlowVoList.json |
| $stateParams | **❌ 未注入** |

### 3.4 StateParams（A 级）

- `optometryCtrl` **未注入** `$stateParams`
- 范围 L34776-L35382 全文**无** `$stateParams` 引用
- 含义：optometryCtrl 不通过 URL 参数接收 medicalRecordId / cashflowId 等业务键（由 caller 通过 $scope 传入）
- 与 deliveryInputCtrl（注入 `$stateParams`，L3812 L3814 接收 cashflowId）形成**结构差异**

### 3.5 HTML 模板可得性（A 级）

| 检查 | 结果 |
|---|---|
| 7 untracked HTML 中是否含 optometry | **❌ 0 处**（已 grep 验证） |
| 全仓其它资源中是否含 optometry HTML | **❌ 0 处**（仅审计 MD 中有 optometry 文字） |
| 视光之家url.txt 中 optometry URL | URL 列表中无 optometry 入口（仅 `optometryGlasses` 提到一次） |

**A 级结论**：optometryCtrl 对应 HTML **资源范围内不可得** → UI 边界全部保持 F。

---

## 4. F4 调用完整定位

### 4.1 F4 调用点（A 级）

**唯一 1 处 F4 调用**：L35054

```javascript
// L35048-L35082
$scope.concatMedicalProductStock = function (item) {
    return new Promise(function (resolve) {
        var medicalProductIdArray = [];
        item.medicalProductVoList.forEach(function (medical) {
            medicalProductIdArray.push(medical.medicalProduct.id);
        });
        new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", {
            medicalProductIdArray: medicalProductIdArray
        }).then(function (result) {
            // ...
        });
    });
};
```

### 4.2 关键差异（与 deliveryInputCtrl L3885 对比，A 级）

| 维度 | deliveryInputCtrl L3885 | optometryCtrl L35054 |
|---|---|---|
| API | `getCanBeDeliverySkuInListOfProduct.json` | `getCanBeDeliverySkuInListOfProduct.json` ✅ 同 |
| **Factory 实例** | `$scope.getDeliveryListFactory = new ObjectFactory()`（**赋给 $scope 变量**） | `new ObjectFactory()`（**匿名 new，未赋给 $scope**） |
| **保存为 $scope** | ✅ 是 | ❌ 否 |
| **跨调用 result 复用** | ✅ 复用（`$scope.getDeliveryListFactory.result.list`） | ❌ 不可能（无 $scope 引用） |
| Request body 字段 | `medicalProductIdArray: medicalProductIdArray` | `medicalProductIdArray: medicalProductIdArray` ✅ 同 |
| Request 来源 | `var arr = ...; if (objectId == null) { push(medicalProduct.id) }`（L3870-L3874 显式循环） | `item.medicalProductVoList.forEach(medical => push(medical.medicalProduct.id))`（L35051-L35052） |
| then 体内是否调 Write | ❌ 否（仅 set $scope.stockDetail = true） | ✅ **是**（resolve 字符串 → 3 个 Write API caller） |
| 二次处理 | ❌ 直接 $scope.getDeliveryListFactory.result.list（无 map） | ✅ `result.result.list.forEach(...)` 构造 medicalProductStockBatctPoListJson |

### 4.3 关键发现（A 级）

1. **optometryCtrl 的 F4 Factory 是匿名 new ObjectFactory()**，没有赋给 $scope 变量
2. **optometryCtrl 的 F4 result 通过 Promise resolve 传出函数**（不是直接赋 $scope.xxx）
3. **optometryCtrl 的 F4 result 立即被消费生成 medicalProductStockBatctPoListJson 字符串**，再被 3 个 caller 接收
4. **optometryCtrl 的 F4 与 deliveryInputCtrl 的 F4 完全是两个独立 ObjectFactory 实例**（不同 $scope、不同 controller、不同生命周期）

---

## 5. F4 Request

### 5.1 Request 完整结构（A 级）

```javascript
// L35054-L35056
new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", {
    medicalProductIdArray: medicalProductIdArray
})
```

| 维度 | 评估 | A-F |
|---|---|---|
| API 字符串 | `/admin/getCanBeDeliverySkuInListOfProduct.json` | A |
| Request 字段 | `medicalProductIdArray`（数组，元素为 medicalProduct.id） | A |
| 其它字段 | ❌ 无 | A |
| JSON.stringify | ❌ 无（直接传数组） | A |
| 类型转换 | ❌ 无 | A |

### 5.2 medicalProductIdArray 来源链（A 级）

```javascript
// L35050-L35053
var medicalProductIdArray = [];  // 局部变量
item.medicalProductVoList.forEach(function (medical) {
    medicalProductIdArray.push(medical.medicalProduct.id);
});
```

| 节点 | 表达式 | 行号 | A-F |
|---|---|---|---|
| 起点 | `item.medicalProductVoList`（concatMedicalProductStock 形参 item 的属性） | L35051 | A |
| 中间 | `.forEach(function (medical) {...})` | L35051 | A |
| 字段读取 | `medical.medicalProduct.id` | L35052 | A |
| 累积 | `medicalProductIdArray.push(medical.medicalProduct.id)` | L35052 | A |
| 终态 | `medicalProductIdArray`（数组） | L35050 | A |

### 5.3 item 来源（A 级）

`item` 是 `concatMedicalProductStock(item)` 的**形参**，由 3 个 caller 传入：
- L35097: `$scope.concatMedicalProductStock(medical)` — medical 来自 choseFactoryMethod 形参
- L35183: `$scope.concatMedicalProductStock(item)` — item 来自"到店取镜" action 函数外层闭包
- L35202: `$scope.concatMedicalProductStock(item)` — item 来自"快递发货" action 函数外层闭包

**A 级结论**：
- `item.medicalProductVoList` 包含若干 medicalProduct 对象
- 每个 medicalProduct 有 `.id` 字段
- 3 个 caller 都不直接操作 medicalProductIdArray
- 真实来源链：`caller 的 item.medicalProductVoList` → `medicalProductIdArray` → F4 Request

### 5.4 与 deliveryInputCtrl 对比（A 级）

| 维度 | deliveryInputCtrl | optometryCtrl |
|---|---|---|
| 数组名 | `medicalProductIdArray` | `medicalProductIdArray` ✅ 同 |
| 字段来源 | `arr[i].medicalProduct.id`（来自 F1 waitingDeliveryList） | `medical.medicalProduct.id`（来自 item.medicalProductVoList） |
| 上游来源 | F1 二次 mutation | $scope.action menu item（来自 selectOrderListFactory.result.list） |
| push 条件 | `if (objectId == null)` truthy 过滤 | **无** 过滤（全部 push） |
| 类型转换 | ❌ 无 | ❌ 无 |
| 元素数 | 0 ~ waitingDeliveryList.length | 0 ~ item.medicalProductVoList.length |

---

## 6. F4 Factory

### 6.1 Factory 实例化（A 级）

| 行号 | 表达式 | 模式 |
|---|---|---|
| L35054 | `new ObjectFactory().saveOrQuery(...)` | **匿名 new**（未赋给 $scope.xxx） |

### 6.2 Factory 与 deliveryInputCtrl 对比（A 级）

| 维度 | deliveryInputCtrl L3884-3885 | optometryCtrl L35054 |
|---|---|---|
| Factory 类型 | `new ObjectFactory()` | `new ObjectFactory()` ✅ 同 |
| 变量名 | `$scope.getDeliveryListFactory` | **无变量名**（匿名） |
| **实例是否独立** | ✅ 是（独立 ObjectFactory 实例） | ✅ 是（独立 ObjectFactory 实例） |
| **是否共享 result** | ❌ 否（独立 $scope） | ❌ 否（无 $scope 引用） |
| **是否共享 scope** | ❌ 否（$scope 是 controller 隔离的） | ❌ 否 |
| **是否共享 service singleton** | ❌ 否（ObjectFactory 是 function，每次 new 返回新实例） | ❌ 否 |

**A 级结论**：
- 两个 controller 的 F4 Factory 是**两个独立 ObjectFactory 实例**
- 没有任何代码连接两个实例
- 仅共享 API 字符串 + Request 字段名 + Response 字段路径，**不**共享数据

### 6.3 ObjectFactory 内部（A 级边界）

- 全部 17 处 optometryCtrl 内 `new ObjectFactory()` 都是匿名 new
- 没有一处赋给 $scope.xxx 或局部变量（除了 $scope.concatMedicalProductStock 这种函数定义）
- ObjectFactory 内部实现 **F**（factory 源码不可得）

---

## 7. F4 result.list

### 7.1 result.list 消费全集（A 级）

**optometryCtrl 范围内 result.list 消费唯一 1 处**：L35062

```javascript
// L35061-L35073
var medicalProductStockBatctPoListJson = [];
result.result.list.forEach(function (medical) {
    var medicalProductStocks = medical.deliveryStockInSkuVoList.map(function (delivery) {
        return {
            stockInSkuId: delivery.stockInSku.id,
            deliveryCount: delivery.deliveryCount
        };
    });
    medicalProductStockBatctPoListJson.push({
        medicalProductId: medical.medicalProduct.id,
        medicalProductStocks: medicalProductStocks
    });
});
```

### 7.2 result.list 元素字段消费全集（A 级）

| 字段路径 | 行号 | 访问类型 | 用途 | A-F |
|---|---|---|---|---|
| `result.list[i].medicalProduct.id` | L35070 | 读（push.medicalProductId） | 构造 medicalProductId | A |
| `result.list[i].deliveryStockInSkuVoList` | L35063 | 读（map 遍历） | 二级数组遍历 | A |
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | L35065 | 读（map.stockInSkuId） | 构造 stockInSkuId | A |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | L35066 | 读（map.deliveryCount） | 构造 deliveryCount | A |
| 其它字段 | — | ❌ 未观察 | — | F |

**A 级结论**：
- Controller 可见范围内，optometryCtrl 仅读取 F4 result.list 元素的 **3 个字段路径**：
  - `medicalProduct.id`
  - `deliveryStockInSkuVoList[].stockInSku.id`
  - `deliveryStockInSkuVoList[].deliveryCount`
- 是否有其它字段：**F**（无样本可证）

### 7.3 与 deliveryInputCtrl 字段对比（B 级互证）

| 字段 | deliveryInputCtrl L3985-3991 | optometryCtrl L35062-35073 | 是否一致 |
|---|---|---|---|
| `result.list[].medicalProduct.id` | ✅ L3998 | ✅ L35070 | ✅ **B（双源互证）** |
| `result.list[].deliveryStockInSkuVoList[].stockInSku.id` | ✅ L3991 | ✅ L35065 | ✅ **B（双源互证）** |
| `result.list[].deliveryStockInSkuVoList[].deliveryCount` | ✅ L3991 | ✅ L35066 | ✅ **B（双源互证）** |

**B 级结论**：
- 3 字段路径在 2 Consumer 完全一致
- S1-96 已确认 B 级多源互证；S1-97 重新验证一致

### 7.4 result.list.length（A 级）

| 表达式 | 行号 | 用途 | A-F |
|---|---|---|---|
| ❌ **未观察到** `result.list.length` 直接访问 | — | — | A |

**A 级结论**：
- optometryCtrl 中仅 `forEach` 遍历 result.list
- **未观察到** `result.list.length` 直接读取
- 也**未观察到** `arr.length == 0` 判空（与 deliveryInputCtrl L3878 `if (!medicalProductIdArray.length)` 的 Request 判空不同；optometryCtrl 仅判 `medicalProductStockBatctPoListJson.length` 判空 L35074，是 result 消费后判空，不是 Request 前的判空）

### 7.5 result 完整性处理（A 级）

```javascript
// L35056-L35060
.then(function (result) {
    if (result.status) {
        Popup.notice(result.errmsg);
        return resolve(false);  // F4 result.status 非 0 时立即 resolve(false)
    }
    // ... 仅 result.status == 0 才进入 result.result.list 消费
});
```

**A 级结论**：
- optometryCtrl F4 result 检查 `result.status`（A）
- `result.status` 非 0（错误）→ 弹窗 + return false
- `result.status == 0`（成功）→ 进入 result.result.list 消费
- 与 deliveryInputCtrl F4 调用模式对比：

| 维度 | deliveryInputCtrl L3885 | optometryCtrl L35054 |
|---|---|---|
| result.status 检查 | ❌ 无 | ✅ L35057 |
| result 错误处理 | ❌ 无 | ✅ Popup.notice + return false |
| result 成功处理 | $scope.stockDetail = true (L3882) | 进入 list 消费 + JSON.stringify + resolve |

---

## 8. 二次转换（map/filter/forEach/push/reduce/sort/uniq）

### 8.1 optometryCtrl F4 result 二次转换（A 级）

| 操作 | 行号 | 用途 | A-F |
|---|---|---|---|
| `result.result.list.forEach` | L35062 | 遍历 result.list 元素 | A |
| `medical.deliveryStockInSkuVoList.map` | L35063 | 二级数组 map → { stockInSkuId, deliveryCount } | A |
| `medicalProductStockBatctPoListJson.push` | L35069 | 累积 { medicalProductId, medicalProductStocks } | A |
| `medicalProductIdArray.push` | L35052 | 累积 medicalProduct.id | A |
| `JSON.stringify` | L35078 | 整体序列化 | A |
| `Promise.resolve(...)` | L35079 | 传出 Promise | A |

### 8.2 二次转换与 deliveryInputCtrl 对比（A 级）

| 维度 | deliveryInputCtrl | optometryCtrl |
|---|---|---|
| F4 result 直接赋 $scope | ✅ $scope.getDeliveryListFactory.result.list | ❌ 无 $scope 引用 |
| F4 result 进入中间对象 | ❌ 否（直接由 saveStock 消费） | ✅ medicalProductStockBatctPoListJson 数组 |
| 中间对象 JSON 序列化 | ❌ 否 | ✅ L35078 JSON.stringify |
| 中间对象 Promise 传出 | ❌ 否 | ✅ L35079 resolve |
| F4 result 是否被原 array mutation | ❌ 0 处 | ❌ 0 处 |
| map / filter / sort | ❌ 0 处 | ❌ 仅 map（不改变原 result.list） |

### 8.3 严格表述（A 级）
- "optometryCtrl F4 result 不修改原 result.list 元素"：**A**（仅读取，未赋值）
- "optometryCtrl F4 result 进入新的 medicalProductStockBatctPoListJson 数组"：**A**
- "optometryCtrl F4 result 经过 Promise resolve 传出"：**A**

---

## 9. F4 → Write API 完整链条（**S1-97 新发现**）

### 9.1 concatMedicalProductStock 的 3 个 caller（A 级）

| # | 行号 | 上下文 | Write API | 字段 | 角色 |
|---|---|---|---|---|---|
| 1 | L35097 | choseFactoryMethod（选择加工方式） | `/admin/setMedicalRecordProcessMode.json` | medicalRecordId + toBeProcess + **medicalProductStockBatctPoListJson** | 选加工方式 |
| 2 | L35183 | "到店取镜" action | `/admin/completeMedicalRecordDelivery.json` | medicalRecordId + deliveryStatus="2" + deliveryNo=undefined + **medicalProductStockBatctPoListJson** | 完成到店取镜 |
| 3 | L35202 | "快递发货" action | `/admin/completeMedicalRecordDelivery.json` | medicalRecordId + deliveryStatus="1" + deliveryNo=deliveryNo + **medicalProductStockBatctPoListJson** | 完成快递发货 |

### 9.2 完整链路（A 级闭合节点 + F 边界）

```
F4 result.list (ObjectFactory 反序列化结果)
    ↓ L35062 forEach
新数组 medicalProductStockBatctPoListJson
    ↓ 每元素 { medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }
    ↓ L35078 JSON.stringify
字符串
    ↓ L35079 Promise resolve
concatMedicalProductStock.then(medicalProductStockBatctPoListJson => {...})
    ↓ 3 个 caller (L35097/L35183/L35202)
3 个 Write API 之一的 Request.medicalProductStockBatctPoListJson
    ↓ saveOrQuery (Write)
后端处理 (F 边界)
```

### 9.3 3 个 Write API 完整对比（A 级）

| 维度 | L35099 setMedicalRecordProcessMode.json | L35185 completeMedicalRecordDelivery.json (到店取镜) | L35204 completeMedicalRecordDelivery.json (快递发货) |
|---|---|---|---|
| 业务动作 | 选择加工方式 | 完成到店取镜 | 完成快递发货 |
| 触发函数 | choseFactoryMethod | "到店取镜" action | "快递发货" action |
| 触发位置 | 弹窗 confirm | 弹窗 hint | 弹窗 express |
| medicalRecordId | ✅ | ✅ | ✅ |
| toBeProcess | ✅ (0/1) | ❌ | ❌ |
| deliveryStatus | ❌ | ✅ "2" | ✅ "1" |
| deliveryNo | ❌ | ✅ undefined | ✅ deliveryNo |
| **medicalProductStockBatctPoListJson** | ✅ | ✅ | ✅ |
| 来源 | F4 result.list via concatMedicalProductStock | 同 | 同 |
| then 行为 | $scope.querySingleOrder() + $scope.queryUndisposed() | $scope.querySingleOrder() | $scope.querySingleOrder() |

### 9.4 与 deliveryInputCtrl F4→F5 链对比（A 级）

| 维度 | deliveryInputCtrl | optometryCtrl |
|---|---|---|
| **F4 result 消费终点** | `$scope.getDeliveryListFactory.result.list`（直接暴露给 saveStock 消费） | `medicalProductStockBatctPoListJson` JSON 字符串（Promise 传出） |
| **进入 Write API 数量** | 1（saveMedicalProductStockBatch.json，F5） | 3（setMedicalRecordProcessMode.json + completeMedicalRecordDelivery.json ×2） |
| **F4 result 是否原 array 引用** | ✅（直接复用 result.list） | ❌（已 map/forEach 转换） |
| **是否 JSON.stringify 一次** | ❌ 否（saveStock 自己 JSON.stringify L4007） | ✅ 是（L35078） |
| **Write API 业务动作** | 保存发货库存 | 选加工方式 + 完成取镜/发货 |

**A 级结论**：
- 两个 controller 的 F4 result **完全不同**的 Write 路径
- 字段名都是 `medicalProductStockBatctPoListJson`（命名巧合 / 业务规范），但**结构可能不同**（F 边界：F4 后端不可证）
- deliveryInputCtrl 的 Write 是"保存发货库存"，optometryCtrl 的 Write 是"完成流程节点"

---

## 10. UI 边界

### 10.1 optometryCtrl 对应 HTML（A 级）

| 资源 | 是否含 optometry | 备注 |
|---|---|---|
| 7 untracked HTML（addSaleRecord/deliveryList/getGlassNotifyList/machineOrderCompleted/machineOrderList/payedDetail/payedList） | **❌ 0 处** | 已 grep 验证 |
| 视光之家url.txt | 含 `optometryGlasses` URL（`/admin/.../optometryGlasses`），无 optometryCtrl 模板 | URL 列表无 templateUrl |
| 其它 | ❌ | 全仓无 optometry HTML |

**A 级结论**：optometryCtrl 对应 HTML **资源范围内不可得** → UI 边界全部保持 F。

### 10.2 deliveryCount / stockInSku / medicalProductId UI 绑定（A 级）

由于 HTML 不可得，**全部保持 F**：
- ❌ 是否存在 `ng-model="...deliveryCount"` UI 输入绑定：**F**
- ❌ 是否存在 `ng-click="concatMedicalProductStock(...)"` UI 触发：**F**
- ❌ 是否存在 `ng-repeat` 遍历 F4 result：**F**
- ❌ 是否存在 `ng-model` / `ng-change` 影响 medicalProductIdArray：**F**

**A 级结论**：
- Controller 源码中未观察到 UI 绑定（HTML 不可得）
- Controller 内部**未观察到**直接修改 deliveryCount 的代码
- 仅观察到 deliveryCount 作为 F4 result 字段被读取并 push 到 medicalProductStocks

### 10.3 Controller 内部状态变更（A 级）

| 操作 | 行号 | 备注 |
|---|---|---|
| $scope.queryCompanyName() | L34792 | 调用 getCompanyOfMine |
| $scope.getEmployee() | L34799 | 调用 getLoginEmployee |
| $scope.concatMedicalProductStock(item) | L35048 | 含 F4 + Write 链 |
| $scope.modal.changeOrder | L35278 | 含 getAdminInfo |
| $scope.appearLossModal | L35316+ | 无关 F4 |

**A 级结论**：optometryCtrl 内部**无**直接修改 F4 result 字段的代码（仅读取 + 重新构造中间对象）。

---

## 11. 与 deliveryInputCtrl F4 对照（**核心**）

### 11.1 维度对照（A 级）

| 维度 | deliveryInputCtrl | optometryCtrl | 是否相同 |
|---|---|---|---|
| **API** | getCanBeDeliverySkuInListOfProduct.json | getCanBeDeliverySkuInListOfProduct.json | ✅ 同 |
| **Factory 类型** | new ObjectFactory() | new ObjectFactory() | ✅ 同 |
| **Factory 实例** | $scope.getDeliveryListFactory | **匿名 new，无变量名** | ❌ 异 |
| **Factory 是否赋 $scope** | ✅ 是 | ❌ 否 | ❌ 异 |
| **Request 字段** | medicalProductIdArray | medicalProductIdArray | ✅ 同 |
| **medicalProductIdArray 来源** | F1 waitingDeliveryList[i].medicalProduct.id（filter objectId==null） | item.medicalProductVoList[].medicalProduct.id（无 filter） | ❌ 异 |
| **F4 触发函数** | showDeliveryModal (L3868) | concatMedicalProductStock (L35048) | ❌ 异 |
| **F4 调用** | L3885 | L35054 | ❌ 异 |
| **F4 result 直接处理** | ❌ 无（仅 $scope.stockDetail=true） | ✅ result.status 检查 + result.result.list 消费 | ❌ 异 |
| **result.list 元素读取字段** | medicalProduct.id / deliveryStockInSkuVoList[].stockInSku.id / deliveryCount | 同 | ✅ 同（B 级互证）|
| **中间对象** | ❌ 无（saveStock 直接消费 result.list） | medicalProductStockBatctPoListJson JSON 字符串 | ❌ 异 |
| **进入 Write API 数量** | 1（saveMedicalProductStockBatch.json / F5） | 3（setMedicalRecordProcessMode.json + completeMedicalRecordDelivery.json ×2） | ❌ 异 |
| **Write API 业务动作** | 保存发货库存 | 选加工方式 + 完成取镜/发货 | ❌ 异 |
| **JSON.stringify** | ❌（saveStock L4007 自做） | ✅ L35078 | ❌ 异 |
| **Promise 传出** | ❌ 无 | ✅ L35079 | ❌ 异 |
| **HTML 模板** | deliveryInputCtrl 模板（不可得，7 HTML 0 处匹配） | 不可得（7 HTML 0 处 optometry） | ✅ 同（都不可得）|
| **UI 绑定** | F | F | ✅ 同（F） |
| **StateParams** | ✅ 注入 $stateParams | ❌ 未注入 | ❌ 异 |
| **F4 result 互证** | B 级 | B 级 | ✅ 同（B 级） |

### 11.2 关键结论（A 级）

1. **同 API 不同实例**：两个 controller 调同一个 API，但 Factory 实例、Scope、Result 全部独立
2. **同字段不同流程**：F4 result 字段路径一致（B 级互证），但消费终点完全不同
3. **F4 result 在 optometryCtrl 经 Promise → 3 个 Write API**；在 deliveryInputCtrl 经 saveStock → 1 个 Write API（F5）
4. **HTML 都不可得** → UI 边界全 F
5. **StateParams 注入不同** → 业务触发机制不同

---

## 12. Factory / Scope / Result 共享与隔离

### 12.1 检查项（A 级）

| 项 | deliveryInputCtrl | optometryCtrl | 共享？ |
|---|---|---|---|
| ObjectFactory 函数 | ObjectFactory | ObjectFactory | ✅ 同一函数（service） |
| ObjectFactory 实例 | L3884 $scope.getDeliveryListFactory | L35054 匿名 new | ❌ 不同实例 |
| $scope | deliveryInputCtrl 的 $scope | optometryCtrl 的 $scope | ❌ AngularJS controller 隔离 |
| F4 result | $scope.getDeliveryListFactory.result | Promise resolve 字符串 | ❌ 不共享 |
| $rootScope | ❌ 未观察到 F4 result 写入 $rootScope | ❌ 同 | ❌ |
| window | ❌ | ❌ | ❌ |
| sessionStorage / localStorage | ❌ | ❌ | ❌ |

### 12.2 A 级结论

- **F4 在两个 controller 中完全独立**：实例 / scope / result / storage 全部隔离
- 唯一的"共享"是 ObjectFactory 函数本身（service singleton）和 API 字符串（HTTP 端点）
- 这与"共享业务对象"无关

---

## 13. Read / Write 实际调用

| API | 类型 | deliveryInputCtrl 实际调用 | optometryCtrl 实际调用 | 本轮实际 |
|---|---|---|---|---|
| F4 (getCanBeDeliverySkuInListOfProduct.json) | Read | 0 | 0 | 0 |
| F5 (saveMedicalProductStockBatch.json) | Write | 0 | — | 0 |
| setMedicalRecordProcessMode.json | Write | — | 0 | 0 |
| completeMedicalRecordDelivery.json | Write | — | 0 | 0 |

**A 级结论**：本轮所有 Read / Write 实际执行 = 0。

---

## 14. Response 样本边界

| 项 | 是否发现 | 标注 |
|---|---|---|
| optometryCtrl 硬编码 F4 result 样本 | ❌ 0 处 | A |
| optometryCtrl test data | ❌ | A |
| optometryCtrl response fixture | ❌ | A |
| 全仓 F4 真实 Response 样本 | ❌ 0（S1-96 已普查） | F |
| F4 Request↔Response 完整 schema | F | F |

**A 级结论**：F4 Request↔Response 边界**保持 F**（F4 后端不可证）。

---

## 15. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | optometryCtrl 注册 | L34776 | A | L1 | |
| 02 | Controller 范围 | L34776-L35382 | A | L1 | 下一 controller L35383 |
| 03 | F4 API | L35054 | A | L1 | 同 deliveryInputCtrl |
| 04 | F4 Factory | L35054 匿名 new ObjectFactory() | A | L1 | 独立实例 |
| 05 | F4 Request | L35055 medicalProductIdArray | A | L1 | |
| 06 | medicalProductIdArray 来源 | L35051-35052 item.medicalProductVoList | A | L1 | 闭包 item |
| 07 | Request 类型转换 | ❌ 无 | A | L1 | |
| 08 | F4 result.list | L35062 forEach | A | L1 | 唯一消费点 |
| 09 | result.list 字段全集 | medicalProduct.id / stockInSku.id / deliveryCount | A | L1 | 3 字段 |
| 10 | medicalProduct.id | L35070 | A | L1 | |
| 11 | stockInSku.id | L35065 | A | L1 | |
| 12 | deliveryCount | L35066 | A | L1 | |
| 13 | result.list.length | ❌ 未观察 | A | L1 | Controller 视角 |
| 14 | 二级字段 | deliveryStockInSkuVoList[] | A | L1 | L35063 map 遍历 |
| 15 | map | L35063 | A | L1 | 不修改原 result.list |
| 16 | filter | ❌ 0 处 | A | L1 | |
| 17 | forEach | L35051/35062 | A | L1 | |
| 18 | push | L35052/35069 | A | L1 | 累积 |
| 19 | 其它转换 | JSON.stringify (L35078) + Promise resolve (L35079) | A | L1 | |
| 20 | F4→Write | L35099/L35185/L35204（3 Write API） | A | L1 | **S1-97 新发现** |
| 21 | deliveryCount UI | ❌ HTML 不可得 | F | L1 | |
| 22 | stockInSku UI | ❌ HTML 不可得 | F | L1 | |
| 23 | medicalProductId UI | ❌ HTML 不可得 | F | L1 | |
| 24 | 与 deliveryInputCtrl 对照 | 详见 §11 | A | L1 | API 同 / 流程异 |
| 25 | Factory / scope / result 共享 | ❌ 全部独立 | A | L1 | 详见 §12 |
| 26 | F4 全局最终结论 | 2 Consumer；B 级互证；F 边界保留 | A/B/F | L1 | |

**统计**：
- **A：24 项**
- **B：1 项**（#26 F4 互证 B 级 + #09 字段互证 B 级 — 已合并为 #26）
- **F：3 项**（#21/22/23 UI 边界）
- **D / C / E：0**
- **E/F 升 A：0**

---

## 16. L1/L2/L3

### L1（源码事实，可证）

- optometryCtrl 注册位置 L34776
- 范围 L34776-L35382
- 17 处 saveOrQuery + 1 处 ListFactory
- F4 调用 L35054
- 3 个 concatMedicalProductStock caller (L35097/L35183/L35202)
- F4 result.list 消费 1 处 L35062
- 3 字段读取（medicalProduct.id / stockInSku.id / deliveryCount）
- 2 次 JSON.stringify (L35078 in concatMedicalProductStock, L4007 in deliveryInputCtrl saveStock)
- Factory 实例独立

### L2（业务解释，未证）

- "optometryCtrl 是验光流程的 controller"：**E**（字段名仅是"optometry"，未证）
- "concatMedicalProductStock 是选择加工方式 / 完成取镜 / 完成发货的中间步骤"：**E**（源码仅是函数调用关系）
- "completeMedicalRecordDelivery 是发货完成接口"：**E**（API 名称仅是命名）
- "deliveryStatus=1 = 快递发货，=2 = 到店取镜"：**E**（数字字面量仅是字符串值）
- "medicalProductStockBatctPoListJson 是库存批次"：**E**（字段名仅是命名）
- "F4 result 与 deliveryInputCtrl 共享业务对象"：**E**（字段名相似 ≠ 共享数据）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 F4 后端实现）

---

## 17. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| F4 Response 完整 schema | 无样本 | F |
| F4 后端处理 | 无后端代码 | F |
| F4 Response 与 Request 值相等 | 无样本 | F |
| F4 Response 与 Request 元素数量关系 | 无后端代码 | F |
| medicalProduct / stockInSku 其它字段 | 无样本 | F |
| optometryCtrl HTML 模板 | 7 HTML 0 处匹配 | F（本轮范围） |
| deliveryCount / stockInSku / medicalProductId UI 绑定 | HTML 不可得 | F |
| 其它 API 同源 DTO | 字段名相似 ≠ 同源 | F |

---

## 18. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| F4 实际调用 = 0 | ✅ | 仅静态审计 |
| F5/F6/其它 Write 实际调用 = 0 | ✅ | 未触发 |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 158 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 158_*.md |
| 文件编号连续 | ✅ | 157 已被 S1-96 占用，本轮使用 158 |

---

## 19. 最终结论

### 19.1 optometryCtrl F4 全链路（最小事实，A 级）

```
optometryCtrl (L34776-L35382)
    ↓ concatMedicalProductStock(item) (L35048)
    ↓ Promise 包装
item.medicalProductVoList
    ↓ forEach (L35051)
medicalProductIdArray
    ↓ F4 Request.medicalProductIdArray (L35055)
new ObjectFactory() (匿名)
    ↓ saveOrQuery (L35054)
F4 (getCanBeDeliverySkuInListOfProduct.json)
    ↓ [F 边界: F4 后端]
F4 Response.result.list
    ↓ forEach (L35062)
medicalProductStockBatctPoListJson
    ↓ JSON.stringify (L35078)
字符串
    ↓ Promise resolve (L35079)
.then(medicalProductStockBatctPoListJson => {...})
    ↓ 3 个 caller:
    ↓   L35097: choseFactoryMethod → setMedicalRecordProcessMode.json
    ↓   L35183: 到店取镜 → completeMedicalRecordDelivery.json (deliveryStatus="2")
    ↓   L35202: 快递发货 → completeMedicalRecordDelivery.json (deliveryStatus="1")
3 个 Write API 之一的 Request
    ↓ saveOrQuery (Write)
后端处理 (F 边界)
```

### 19.2 F4 全局 Consumer 现状（A 级）

| Consumer | Controller 范围 | F4 result 进入的 Write API |
|---|---|---|
| deliveryInputCtrl | L3812-L4021 | saveMedicalProductStockBatch.json (F5) |
| optometryCtrl | L34776-L35382 | setMedicalRecordProcessMode.json + completeMedicalRecordDelivery.json ×2 |

**A 级结论**：F4 当前资源范围内**仍为 2 Consumer**（无新发现第 3 个）。

### 19.3 F4 Response 字段互证（B 级）

| 字段 | deliveryInputCtrl | optometryCtrl | B 级 |
|---|---|---|---|
| `result.list[].medicalProduct.id` | ✅ L3998 | ✅ L35070 | **B** |
| `result.list[].deliveryStockInSkuVoList[].stockInSku.id` | ✅ L3991 | ✅ L35065 | **B** |
| `result.list[].deliveryStockInSkuVoList[].deliveryCount` | ✅ L3991 | ✅ L35066 | **B** |

### 19.4 与 deliveryInputCtrl 关键差异（A 级）

| 维度 | deliveryInputCtrl | optometryCtrl |
|---|---|---|
| 共享数据 | ❌ 否 | ❌ 否 |
| 共享 Factory 实例 | ❌ 否 | ❌ 否 |
| 共享 scope | ❌ 否（controller 隔离） | ❌ 否 |
| 共享 storage | ❌ 否 | ❌ 否 |
| 共享业务对象 | ❌ 否（仅字段名相似） | ❌ 否 |
| **同一 API** | ✅ 是 | ✅ 是 |
| **同字段路径** | ✅ 是 | ✅ 是 |
| **同业务流程** | ❌ 否（不同 Write 路径） | ❌ 否 |

### 19.5 S1-97 关键新发现

1. **optometryCtrl 的 F4 Factory 是匿名 new**，未赋 $scope 变量（与 deliveryInputCtrl 的 $scope.getDeliveryListFactory 不同）
2. **optometryCtrl 的 F4 result 通过 Promise resolve 字符串传出**（与 deliveryInputCtrl 直接 $scope 暴露不同）
3. **F4 result 在 optometryCtrl 经中间对象 medicalProductStockBatctPoListJson 进入 3 个 Write API**（S1-96 未发现）
4. **3 个 Write API 各自业务不同**：setMedicalRecordProcessMode + completeMedicalRecordDelivery(deliveryStatus="1"/"2")
5. **HTML 不可得** → UI 边界全 F

### 19.6 不可在本轮升级为 A 的项

- F4 后端处理（F）
- F4 Response 完整 schema（F）
- F4 Response ↔ Request 值相等（F）
- F4 Response ↔ Request 元素数量（F）
- optometryCtrl HTML 模板（F，本轮范围）
- medicalProduct / stockInSku 其它字段（F）
- 业务语义（E，禁止升级）

---

**审计结束**。
