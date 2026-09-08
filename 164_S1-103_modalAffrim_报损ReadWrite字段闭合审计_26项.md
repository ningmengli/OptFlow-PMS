# S1-103 modal.affrim 报损 Read/Write 字段闭合审计

> **任务名**：S1-103｜modal.affrim 报损链：selectMedicalProductStockList → createMedicalStockLossOfSmallVersion 字段级闭合审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）modal.affrim 完整字段链
> **当前轮次**：S1-103（接 S1-102 完成）
> **本轮承诺**：1 Read + 1 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| selectMedicalProductStockList.json (L35319) | ✅ | modal.affrim 唯一 Read |
| createMedicalStockLossOfSmallVersion.json (L35342) | ✅ | modal.affrim 唯一 Write |
| getAdminInfo.json (L35281) | ✅ | lossAdminId 来源 |
| modal.affrim (L35301-L35353) | ✅ | 核心函数 |
| modal.shopInfo 4 outer 字段 | ✅ | medicalRecordId/machineCenterId/lossAdminId + medicalStockLossSkuListJson |
| medicalStockLossSkuListJson 4 inner 字段 | ✅ | medicalProductStockId/lossCount/lossReasonId/remark |
| L16287 (其它 controller 报损链路) | ⚠️ 旁证 | 另一套实现，非本轮范围 |
| 7 HTML | ❌（不可得） | UI 边界 F |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "lossCount = 报损数量"：**E**（仅命名）
- "lossReasonId = 报损原因主键"：**E**（仅命名）
- "lossAdminId = 操作管理员 ID"：**E**（仅命名）
- "medicalProductStockId = 库存主键"：**E**（仅命名）
- "remark = 备注"：**E**（仅命名）
- 字段名相似 → 同源字段：**D**（禁止升级 A）
- L16287 的 `$scope.loss` 报损链路 ≠ modal.affrim：**A**（不同 controller / 不同实现 / 不同字段路径）

---

## 3. selectMedicalProductStockList 全局引用

### 3.1 controller.js 全部引用（A 级，已穷举）

| 行号 | Controller | 函数 | Factory | 角色 |
|---|---|---|---|---|
| L35319 | optometryCtrl | modal.affrim | 匿名 `new ObjectFactory()` | **唯一真实调用** |

**A 级结论**：
- selectMedicalProductStockList.json 在 controller.js **仅 1 处真实调用**
- ❌ 0 处其它 controller
- ❌ 0 处 7 HTML

### 3.2 createMedicalStockLossOfSmallVersion 全局引用（A 级）

| 行号 | Controller | 函数 | Factory | 角色 |
|---|---|---|---|---|
| L35342 | optometryCtrl | modal.affrim | 匿名 `new ObjectFactory()` | **唯一真实调用** |

**A 级结论**：
- createMedicalStockLossOfSmallVersion.json 在 controller.js **仅 1 处真实调用**
- ❌ 0 处其它 controller
- ❌ 0 处 7 HTML

### 3.3 getAdminInfo.json 全局引用（A 级，已穷举）

| 行号 | Controller | 角色 | A-F |
|---|---|---|---|
| L13774 | (其它) | 其它 controller 1 | A |
| L14315 | (其它) | 其它 controller 2 | A |
| L16287 | (其它) | 其它 controller 3（**S1-103 旁证：$scope.loss.lossAdminId**） | A |
| L31781 | (其它) | 其它 controller 4 | A |
| L35281 | optometryCtrl | **modal.changeOrder (本轮相关)** | A |

**A 级结论**：
- getAdminInfo.json 在 controller.js **5 处调用**
- 仅 L35281 与 modal.affrim / shopInfo.lossAdminId 链相关
- L16287 是 **另一套**"报损"实现（$scope.loss.* 路径），**非本轮范围**

---

## 4. selectMedicalProductStockList Request 完整结构

### 4.1 完整源码（A 级，L35319-L35321）

```javascript
new ObjectFactory().saveOrQuery("/admin/selectMedicalProductStockList.json", {
    medicalProductId: medicalProductId
}).then(function (res) { ... });
```

### 4.2 Request 字段级映射（A 级）

| 字段 | 表达式 | 来源 | 行号 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|
| `medicalProductId` | `medicalProductId` | modal.affrim 形参（来自 $scope.modal.shopInfo.medicalProductId） | L35320 | A | L1 |
| 其它字段 | ❌ 无 | — | — | A | — |

### 4.3 medicalProductId 完整来源链（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34884
medicalProduct (= medicalProductVoList[index].medicalProduct)
    ↓ L34896
medicalProduct.id
    ↓ L34887
$scope.modal.shopInfo.medicalProductId
    ↓ L35309
modal.affrim 局部变量 medicalProductId (L35320 Request 字段值)
```

**A 级结论**：
- medicalProductId 字段值 = `medicalProductVoList[index].medicalProduct.id`（**A 级** 完整字段链）
- ❌ 不与 `selectOrderListFactory.items[index].medicalRecord.id` 同源（**A 级**：不同字段路径）
- ❌ 不与 F4 (getCanBeDeliverySkuInListOfProduct) 的 medicalProductIdArray 字段路径**有任何代码连接**（A 级）

---

## 5. selectMedicalProductStockList Response 字段消费

### 5.1 完整消费源码（A 级，L35321-L35324 + L35326-L35328）

```javascript
.then(function (res) {
    if (res.status) {                                  // L35322
        return Popup.notice(res.errmsg);                // L35323
    }
    var medicalStockLossSkuListJson = [];              // L35325
    res.object.forEach(function (medical) {             // L35326
        medicalStockLossSkuListJson.push({              // L35327
            medicalProductStockId: medical.id,           // L35328
            lossCount: useCount,                        // L35329
            lossReasonId: lossReasonId,                 // L35330
            remark: remark                              // L35331
        });
    });
    // ... 后续 Write
});
```

### 5.2 Response 字段消费全集（A 级，optometryCtrl 范围 modal.affrim 路径）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `res.status` | L35322 | 错误判断（if） | — | A |
| `res.errmsg` | L35323 | Popup.notice 弹窗 | — | A |
| `res.object` | L35326 | 整体 forEach（数组遍历） | — | A |
| `res.object[i].id` | L35328 | 字段读取（每个元素） | medicalStockLossSkuListJson[i].medicalProductStockId | A |
| 其它字段 | ❌ 0 处 | — | — | F |

### 5.3 严格表述（A 级）
- "res.object 是数组（forEach 遍历）"：**A**
- "res.object[i].id 是 Controller 可见的**唯一**字段级访问"：**A**
- "res.object 完整字段集合"：**F**（无样本可证）
- "res.object.length"：**A 未观察**（仅 forEach，无 length 读取）

---

## 6. medicalProductStockId 来源链

### 6.1 完整来源链（A 级）

```
selectMedicalProductStockList.json Response
    ↓ [F 边界: HTTP + 后端]
res.object
    ↓ L35326 forEach
res.object[i]
    ↓ L35328
res.object[i].id
    ↓
medicalStockLossSkuListJson[i].medicalProductStockId
    ↓ L35338
JSON.stringify(medicalStockLossSkuListJson)
    ↓
medicalStockLossSkuListJson (字符串)
    ↓
createMedicalStockLossOfSmallVersion.json Request.medicalStockLossSkuListJson
```

### 6.2 字段级闭合（A 级）

| 节点 | 表达式 | 行号 | A-F |
|---|---|---|---|
| Read Request 字段 | `medicalProductId` | L35320 | A |
| Read Response 可见字段 | `res.object[i].id` | L35328 | A |
| Write Request inner 字段 | `medicalProductStockId: medical.id` | L35328 | A |
| Write Request 整体 | `medicalStockLossSkuListJson: JSON.stringify(...)` | L35338 | A |

**A 级结论**：
- Read Response `.id` → Write Request `.medicalProductStockId`（**A 级**：L35328 直接赋值）
- 这是 Controller 内部跨字段**值复制**（非 F 边界，但**后端 DTO 同一性** = E / L3=F）
- 严格表述：**当前 Controller 实现 Read Response.id 复制到 Write Request.medicalProductStockId**（A 级）

---

## 7. useCount 完整来源

### 7.1 useCount 全部 controller.js 引用（A 级，已穷举 modal.affrim 路径）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35289 | `useCount: 1` | modal.changeOrder 初始化 $scope.modal.shopInfo.useCount | A |
| L35305 | `useCount = _$scope$modal$shopInf.useCount` | modal.affrim 局部变量赋值 | A |
| L35329 | `lossCount: useCount` | medicalStockLossSkuListJson[i].lossCount | A |

### 7.2 useCount 来源链（A 级）

```
modal.changeOrder (L35278)
    ↓ L35287
$scope.modal.shopInfo = { ... }
    ↓ L35289
$scope.modal.shopInfo.useCount = 1
    ↓ [HTML 端可能修改]  (F 边界)
    ↓
modal.affrim (L35301)
    ↓ L35305
var useCount = $scope.modal.shopInfo.useCount
    ↓ L35329
medicalStockLossSkuListJson[i].lossCount = useCount
```

### 7.3 关键事实（A 级）
- **useCount 初始值 = 1**（modal.changeOrder L35289 字面量）
- ❌ **0 处** Controller 内对 useCount 的修改
- ❌ **0 处** useCount 参与转换（Number / parseInt / String）
- ⚠️ **HTML 端可能修改** `$scope.modal.shopInfo.useCount`（F 边界，HTML 不可得）
- 严格表述：**Controller 视角 useCount 初值 = 1，最终值依赖 HTML 端是否修改**（A + F）

### 7.4 useCount → lossCount 字段复制（A 级）

| 节点 | 表达式 | 行号 | A-F |
|---|---|---|---|
| 源 | `useCount` (modal.affrim 局部) | L35305 | A |
| 目标 | `lossCount` (medicalStockLossSkuListJson[i]) | L35329 | A |
| 转换 | ❌ 0 处 | — | A |
| 复用 | ✅ 同一个 useCount 用于**所有** res.object 元素 | L35326-L35333 | A |

---

## 8. lossReasonId 完整来源

### 8.1 lossReasonId 全部 controller.js 引用（A 级，modal.affrim 路径）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35293 | `lossReasonId: null` | modal.changeOrder 初始化 | A |
| L35304 | `lossReasonId = _$scope$modal$shopInf.lossReasonId` | modal.affrim 局部 | A |
| L35315 | `if (!lossReasonId) { Popup.notice("请选择报损原因"); return false; }` | modal.affrim 校验 | A |
| L35330 | `lossReasonId: lossReasonId` | medicalStockLossSkuListJson[i].lossReasonId | A |

### 8.2 lossReasonId 来源链（A 级）

```
modal.changeOrder (L35278)
    ↓ L35287
$scope.modal.shopInfo = { ... }
    ↓ L35293
$scope.modal.shopInfo.lossReasonId = null
    ↓ [HTML 端必须设置]  (F 边界 — 否则 L35315 校验失败)
    ↓
modal.affrim (L35301)
    ↓ L35315 校验
    ↓
if (lossReasonId) {
    L35304 读取
    L35330 写入 inner object
}
```

### 8.3 关键事实（A 级）
- **lossReasonId 初始值 = null**（modal.changeOrder L35293 字面量）
- **modal.affrim 强制要求 lossReasonId 非空**（L35315：null → return false + Popup）
- ❌ **0 处** Controller 内对 lossReasonId 的赋值（除 modal.changeOrder 初始化为 null）
- ⚠️ **HTML 端必须设置** `$scope.modal.shopInfo.lossReasonId`（F 边界）
- lossReasonId **同一个值**用于 medicalStockLossSkuListJson 所有 inner 元素（L35326-L35333 复用）
- 严格表述：**Controller 视角 lossReasonId 必须由 HTML 端设置，否则 modal.affrim 不会进入 Write**（A + F）

---

## 9. remark 完整来源

### 9.1 remark 全部 controller.js 引用（A 级，modal.affrim 路径）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35290 | `remark: ""` | modal.changeOrder 初始化 | A |
| L35306 | `remark = _$scope$modal$shopInf.remark` | modal.affrim 局部 | A |
| L35331 | `remark: remark` | medicalStockLossSkuListJson[i].remark | A |

### 9.2 remark 来源链（A 级）

```
modal.changeOrder (L35278)
    ↓ L35287
$scope.modal.shopInfo = { ... }
    ↓ L35290
$scope.modal.shopInfo.remark = ""  // 空字符串字面量
    ↓ [HTML 端可修改]  (F 边界)
    ↓
modal.affrim (L35301)
    ↓
L35306 读取
    ↓
L35331 写入 inner object
```

### 9.3 关键事实（A 级）
- **remark 初始值 = ""**（空字符串字面量）
- ❌ **0 处** Controller 内对 remark 的修改
- ❌ **0 处** remark 参与 trim / String 转换
- ❌ **0 处** remark 校验（modal.affrim 允许空字符串）
- ⚠️ **HTML 端可修改** remark（F 边界）
- remark **同一个值**用于 medicalStockLossSkuListJson 所有 inner 元素

---

## 10. lossAdminId 完整来源

### 10.1 lossAdminId 全部 controller.js 引用（A 级，modal.affrim 路径）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35291 | `lossAdminId: res.result.object.id` | modal.changeOrder 写 $scope.modal.shopInfo.lossAdminId | A |
| L35303 | `lossAdminId = _$scope$modal$shopInf.lossAdminId` | modal.affrim 局部 | A |
| L35311 | `if (!lossAdminId) { Popup.notice("请选择报损责任人"); return false; }` | modal.affrim 校验 | A |
| L35337 | `lossAdminId: lossAdminId, //报损责任人` | Write Request 字段 | A |

### 10.2 getAdminInfo → shopInfo → lossAdminId → Write 完整链（A 级）

```
[HTML ng-click]  F 边界
    ↓
modal.changeOrder(true, index)  (L35278)
    ↓ L35281
new ObjectFactory().saveOrQuery("/admin/getAdminInfo.json")  (无 Request body)
    ↓ [F 边界: HTTP + 后端]
res.result.object
    ↓ L35291
$scope.modal.shopInfo.lossAdminId = res.result.object.id
    ↓ L35292
$scope.modal.shopInfo.adminname = res.result.object.nickname
    ↓ [HTML 端可能修改 lossAdminId 选其它 admin]  F 边界
    ↓
modal.affrim (L35301)
    ↓ L35311 校验
    ↓
L35303 读取 $scope.modal.shopInfo.lossAdminId
    ↓
L35337 写入 createMedicalStockLossOfSmallVersion.json Request.lossAdminId
```

### 10.3 getAdminInfo Response 字段消费全集（A 级，modal.changeOrder 范围）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `res.result.object.id` | L35291 | 字段读取 | $scope.modal.shopInfo.lossAdminId | A |
| `res.result.object.nickname` | L35292 | 字段读取 | $scope.modal.shopInfo.adminname | A |
| 其它字段 | ❌ 0 处 | — | — | F |

### 10.4 关键事实（A 级）
- **getAdminInfo.json 在 modal.changeOrder 路径上**仅消费 2 字段（`res.result.object.id` + `res.result.object.nickname`）
- **lossAdminId 必填**（modal.affrim L35311 校验，null → return false + Popup）
- lossAdminId **进入 Write Request**（L35337）
- ❌ 0 处 lossAdminId 修改（除 modal.changeOrder 初始化）

---

## 11. medicalRecordId 完整来源

### 11.1 完整来源链（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34884
medicalProduct (= medicalProductVoList[index].medicalProduct)
    ↓ L34895
medicalProduct.medicalRecordId
    ↓ L34887
$scope.modal.shopInfo.medicalRecordId
    ↓ L35307
modal.affrim 局部 medicalRecordId (L35335 Request 字段值)
```

### 11.2 关键事实（A 级）
- **medicalRecordId 字段值 = `medicalProductVoList[index].medicalProduct.medicalRecordId`**（A 级 完整字段链）
- **❌ 不是** `selectOrderListFactory.items[index].medicalRecord.id`（**A 级**：不同字段路径）
- ❌ 0 处 controller.js 内有 `medicalProduct.medicalRecordId == medicalRecord.id` 比较
- 严格表述：**modal.affrim 使用的 medicalRecordId 字段路径与 selectOrderListFactory.items 的 medicalRecordId 字段路径不同源**（A 级）

### 11.3 Write Request.medicalRecordId 完整来源（A 级）

| 节点 | 表达式 | 行号 | A-F |
|---|---|---|---|
| 源 | modal.shopInfo.medicalRecordId | L35295 | A |
| 中间 | modal.affrim 局部 medicalRecordId | L35307 | A |
| 目标 | createMedicalStockLossOfSmallVersion.json Request.medicalRecordId | L35335 | A |
| 转换 | ❌ 0 处 | — | A |
| 校验 | ❌ 0 处 | — | A |

---

## 12. machineCenterId 完整来源

### 12.1 完整来源链（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34885
medicalProductDelivery (= medicalProductVoList[index].medicalProductDelivery)
    ↓ L34894
medicalProductDelivery.machineCenterId
    ↓ L34887
$scope.modal.shopInfo.machineCenterId
    ↓ L35308
modal.affrim 局部 machineCenterId (L35336 Request 字段值)
```

### 12.2 machineCenterId 关键事实（A 级）
- **machineCenterId 字段值 = `medicalProductVoList[index].medicalProductDelivery.machineCenterId`**（A 级 完整字段链）
- **❌ 不是** `lockMachineCenter.id`（S1-94 deliveryInputCtrl 链路字段）
- **❌ 不进入** selectMedicalProductStockList.json Request（**0 处**）
- **❌ 不进入** F3 (getMedicalProductMachineCenterVoList.json) Request（**0 处**）
- **❌ 不进入** F6 (sendMedicalProductToMachineCenter.json) Request（**0 处**）
- 严格表述：**modal.affrim 的 machineCenterId 与 Delivery F3/F6 的 machineCenterId 字段路径不同源，无任何代码连接**（A 级）

### 12.3 关键字段不进入 Read Request（A 级）

| Read API | Request.machineCenterId 字段 | A-F |
|---|---|---|
| selectMedicalProductStockList.json (L35319) | ❌ **0 处**（Request 只有 medicalProductId） | A |
| getAdminInfo.json (L35281) | ❌ **0 处**（无 Request body） | A |

**A 级结论**：modal.affrim 路径上 `medicalProductDelivery.machineCenterId` **不进入任何 Read Request**，仅进入 Write Request (L35336)。

---

## 13. medicalStockLossSkuListJson 完整构造

### 13.1 完整构造源码（A 级，L35325-L35333）

```javascript
var medicalStockLossSkuListJson = [];                                                  // L35325
res.object.forEach(function (medical) {                                                 // L35326
    medicalStockLossSkuListJson.push({                                                  // L35327
        medicalProductStockId: medical.id,                                              // L35328
        lossCount: useCount,                                                            // L35329
        lossReasonId: lossReasonId,                                                    // L35330
        remark: remark                                                                  // L35331
    });
});
```

### 13.2 数组构造步骤（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L35325 | `var medicalStockLossSkuListJson = [];`（初始化空数组） | A |
| 2 | L35326 | `res.object.forEach(...)`（遍历 Response 数组） | A |
| 3 | L35327 | `medicalStockLossSkuListJson.push({...})`（每次 push 1 个 inner object） | A |
| 4 | L35328 | inner.medicalProductStockId = medical.id | A |
| 5 | L35329 | inner.lossCount = useCount（外层 scope 变量） | A |
| 6 | L35330 | inner.lossReasonId = lossReasonId（外层 scope 变量） | A |
| 7 | L35331 | inner.remark = remark（外层 scope 变量） | A |

### 13.3 JSON.stringify（A 级，L35338）

```javascript
medicalStockLossSkuListJson: JSON.stringify(medicalStockLossSkuListJson)
```

- ✅ 整体数组序列化为字符串
- ❌ 0 处额外处理（无加密 / 编码 / 转换）

### 13.4 inner object 完整结构（A 级）

```json
{
  "medicalProductStockId": <res.object[i].id>,
  "lossCount": <useCount>,
  "lossReasonId": <lossReasonId>,
  "remark": <remark>
}
```

### 13.5 数组长度关系（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 数组元素数 = res.object.length | ✅ 是（forEach 一一对应 push） | A |
| 是否 1:1 对应 | ✅ 是（每个 res.object 元素 → 1 个 inner object） | A |
| 是否 1:多 | ❌ 否 | A |
| 是否过滤 | ❌ 0 处 | A |
| 是否去重 | ❌ 0 处 | A |
| 是否排序 | ❌ 0 处 | A |

**A 级结论**：
- medicalStockLossSkuListJson 元素数 = res.object 元素数（**A** 1:1）
- 严格表述：**一个 res.object 元素对应一个 loss item**（A 级）

---

## 14. 多库存对象关系（A 级）

### 14.1 res.object 数组遍历方式（A 级）

| 模式 | 是否使用 | A-F |
|---|---|---|
| for 循环 (i++) | ❌ 0 处 | A |
| forEach | ✅ L35326 | A |
| map | ❌ 0 处 | A |
| filter | ❌ 0 处 | A |
| some / every | ❌ 0 处 | A |
| for-in | ❌ 0 处 | A |
| while | ❌ 0 处 | A |
| 数组解构 | ❌ 0 处 | A |

### 14.2 res.object 长度检查（A 级）

| 检查 | 是否存在 | A-F |
|---|---|---|
| res.object.length | ❌ 0 处 | A |
| if (!res.object.length) 判空 | ❌ 0 处 | A |
| if (res.object.length === 0) 判空 | ❌ 0 处 | A |
| if (medicalStockLossSkuListJson.length === 0) 判空 | ❌ 0 处 | A |

### 14.3 严格表述（A 级）
- "res.object 支持多元素"：**A**（forEach 支持任意长度）
- "Controller 不限制 res.object 元素数"：**A**
- "实际后端返回多少条 = F"：**F**（无样本可证）
- "Controller 构造 1:1 关系"：**A**（每元素 → 1 inner object）

---

## 15. 过滤/去重/排序 检查（A 级）

### 15.1 modal.affrim 范围操作检查（A 级）

| 操作 | 是否存在 | A-F |
|---|---|---|
| `filter` | ❌ 0 处 | A |
| `sort` | ❌ 0 处 | A |
| `uniq` / `unique` | ❌ 0 处 | A |
| `indexOf` 去重 | ❌ 0 处 | A |
| `Set` 去重 | ❌ 0 处 | A |
| `reduce` | ❌ 0 处 | A |
| `concat` | ❌ 0 处 | A |
| `splice` / `slice` | ❌ 0 处 | A |
| `reverse` | ❌ 0 处 | A |
| `if (...) continue` | ❌ 0 处 | A |
| `if (...) break` | ❌ 0 处 | A |

**A 级结论**：
- res.object → medicalStockLossSkuListJson 之间**0 处过滤/去重/排序**操作
- Controller **完全保留** res.object 元素顺序和数量
- 严格表述：**当前 Controller 对 res.object 元素 1:1 全部构造 inner object，无任何过滤/去重/排序**（A 级）

---

## 16. useCount / lossReasonId / remark 是否复用（A 级）

### 16.1 内层 forEach 闭包行为（A 级）

```javascript
res.object.forEach(function (medical) {     // L35326
    medicalStockLossSkuListJson.push({
        medicalProductStockId: medical.id,    // L35328 — 每个元素取自己 .id
        lossCount: useCount,                  // L35329 — **所有元素共用外层 useCount**
        lossReasonId: lossReasonId,           // L35330 — **所有元素共用外层 lossReasonId**
        remark: remark                        // L35331 — **所有元素共用外层 remark**
    });
});
```

### 16.2 复用分析（A 级）

| 字段 | 是否所有 inner item 复用同一外层值 | A-F |
|---|---|---|
| `medicalProductStockId` | ❌ 否（每个元素取自己 .id） | A |
| `lossCount` | ✅ **是**（所有元素共用 useCount） | A |
| `lossReasonId` | ✅ **是**（所有元素共用 lossReasonId） | A |
| `remark` | ✅ **是**（所有元素共用 remark） | A |

### 16.3 严格表述（A 级）
- "3 个字段（lossCount / lossReasonId / remark）所有 inner item 复用同一外层值"：**A**
- "1 个字段（medicalProductStockId）每个 inner item 取自己 .id"：**A**
- ❌ **0 处** Controller 内对每个 inner item 单独设置这 3 个字段
- ❌ **0 处** Controller 内根据 res.object 元素动态计算这 3 个字段

---

## 17. Write Request 完整字段级闭合（A 级）

### 17.1 4 字段 Read Response → Write Request 闭合矩阵（A 级）

| 字段 | Read 端 | 转换 | Write 端 | A-F |
|---|---|---|---|---|
| `medicalProductStockId` | `res.object[i].id` (L35328) | ❌ 无 | `medicalProductStockId: medical.id` (L35328) | **A** |
| `lossCount` | `useCount` (L35329) — 来自 $scope.modal.shopInfo.useCount = 1 (L35289) | ❌ 无 | `lossCount: useCount` (L35329) | **A** |
| `lossReasonId` | `lossReasonId` (L35330) — 来自 $scope.modal.shopInfo.lossReasonId (HTML 必须设置) | ❌ 无 | `lossReasonId: lossReasonId` (L35330) | **A** |
| `remark` | `remark` (L35331) — 来自 $scope.modal.shopInfo.remark = "" (L35290) | ❌ 无 | `remark: remark` (L35331) | **A** |

### 17.2 4 outer 字段来源闭合（A 级）

| 字段 | 来源 | 转换 | Write 端 | A-F |
|---|---|---|---|---|
| `medicalRecordId` | `$scope.modal.shopInfo.medicalRecordId` (L35307) — 来自 `medicalProduct.medicalRecordId` (L34895) | ❌ 无 | `medicalRecordId: medicalRecordId` (L35335) | **A** |
| `machineCenterId` | `$scope.modal.shopInfo.machineCenterId` (L35308) — 来自 `medicalProductDelivery.machineCenterId` (L34894) | ❌ 无 | `machineCenterId: machineCenterId` (L35336) | **A** |
| `lossAdminId` | `$scope.modal.shopInfo.lossAdminId` (L35303) — 来自 `res.result.object.id` of getAdminInfo (L35291) | ❌ 无 | `lossAdminId: lossAdminId` (L35337) | **A** |
| `medicalStockLossSkuListJson` | `JSON.stringify(medicalStockLossSkuListJson)` (L35338) — 4 inner 字段 | ✅ JSON.stringify | `medicalStockLossSkuListJson: ...` (L35338) | **A** |

### 17.3 8 字段全部闭合状态（A 级）

| # | 字段 | 是否闭合 | A-F |
|---|---|---|---|
| 1 | medicalRecordId | ✅ | A |
| 2 | machineCenterId | ✅ | A |
| 3 | lossAdminId | ✅ | A |
| 4 | medicalStockLossSkuListJson | ✅ | A |
| 5 | (inner) medicalProductStockId | ✅ | A |
| 6 | (inner) lossCount | ✅ | A |
| 7 | (inner) lossReasonId | ✅（依赖 HTML 端设置） | A + F |
| 8 | (inner) remark | ✅（依赖 HTML 端可选设置） | A + F |

**A 级结论**：
- 4 outer 字段**全部 A 级闭合**
- 4 inner 字段**全部 A 级闭合**（含 HTML 端依赖 F 边界）
- **总闭合率 = 8/8 = 100%**（A 级，Controller 视角）

---

## 18. Write success → brushData 闭环（A 级）

### 18.1 success 完整源码（A 级，L35342-L35350）

```javascript
new ObjectFactory().saveOrQuery("/admin/createMedicalStockLossOfSmallVersion.json", object).then(function (res) {
    if (res.status == 0) {                        // L35343
        Popup.notice("报损成功");                   // L35344
        $scope.modal.changeOrder(false);            // L35345 — 关闭 modal
        $scope.order.brushData(medicalRecordId);    // L35346 — 重新刷 data
    } else {
        Popup.notice(res.errmsg);
    }
});
```

### 18.2 success 行为精确分层（A 级）

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (res.status == 0)` | A |
| 2 | `Popup.notice("报损成功")` | A |
| 3 | `$scope.modal.changeOrder(false)`（关闭 modal） | A |
| 4 | `$scope.order.brushData(medicalRecordId)`（重新刷 data） | A |
| 5 | 错误时 `Popup.notice(res.errmsg)` | A |
| 6 | 错误时**不**调 brushData | A |
| 7 | 错误时**不**调 changeOrder(false) | A |

### 18.3 brushData 参数来源（A 级）

```javascript
$scope.order.brushData(medicalRecordId)
```

| 维度 | 评估 | A-F |
|---|---|---|
| 形参 | `medicalRecordId` | A |
| 来源 | modal.affrim 局部变量 L35307 | A |
| 实际值 | $scope.modal.shopInfo.medicalRecordId = medicalProduct.medicalRecordId | A |
| 校验 | ❌ 0 处 | A |
| 转换 | ❌ 0 处 | A |

### 18.4 闭环完整链路（A 级）

```
modal.affrim success
    ↓ L35346
$scope.order.brushData(medicalRecordId)
    ↓
brushData()  (L34860)
    ↓
$scope.order.object = {}  (L34861)
Read /admin/getMedicalRecordFlowVo.json
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868
$scope.order.object = result.object
    ↓
[HTML 重新渲染]  (F 边界)
```

### 18.5 严格表述（A 级）
- "Write success → brushData 闭环"：**A**
- "brushData 参数 = medicalProduct.medicalRecordId"：**A**
- "brushData 不携带任何其它上下文（不带 index / 数组）"：**A**
- "brushData 内部重置 $scope.order.object = {} 再发起 Read"：**A**（L34861）

---

## 19. Promise / 失败分支（A 级）

### 19.1 Read (selectMedicalProductStockList) Promise（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ L35321 | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |

### 19.2 Write (createMedicalStockLossOfSmallVersion) Promise（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ L35342 | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |
| 嵌套 then | ✅ Read .then 内含 Write .then | A |

### 19.3 失败分支（A 级）

| API | result.status 检查 | 行为 | A-F |
|---|---|---|---|
| selectMedicalProductStockList (L35322) | if (res.status) | Popup + return | A |
| createMedicalStockLossOfSmallVersion (L35343) | if (res.status == 0) | success 分支 | A |
| getAdminInfo (S1-102) | ❌ 0 处 | 不检查 status（只读 .id / .nickname） | A |

### 19.4 严格表述（A 级）
- 2 API 都有错误 Popup 处理
- ❌ 0 处 .catch 保护
- ❌ 0 处 try-catch

---

## 20. 与 Delivery 链是否直接连接（A 级）

### 20.1 modal.affrim 字段与 F1/F3/F4/F5/F6 检查（A 级）

| 字段 | 进入 F1? | 进入 F3? | 进入 F4? | 进入 F5? | 进入 F6? | A-F |
|---|---|---|---|---|---|---|
| `medicalProduct.id` (modal.changeOrder L35296 → shopInfo) | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | A |
| `medicalProduct.medicalRecordId` (modal.changeOrder L35295 → shopInfo → modal.affrim) | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | A |
| `medicalProductDelivery.machineCenterId` (modal.changeOrder L35294 → shopInfo → modal.affrim) | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | A |
| `medicalProductStockId` (modal.affrim inner) | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | A |
| `lossCount` / `lossReasonId` / `lossAdminId` / `remark` | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 | A |

**A 级结论**：
- modal.affrim 全部 8 字段与 F1/F3/F4/F5/F6 链路**0 处直接代码连接**
- ❌ 字段名相似（`medicalRecordId` / `machineCenterId` / `medicalProductId`）**不等于**直接连接
- 严格表述：**modal.affrim 是与 Delivery 链路完全独立的"报损"业务支路**（A 级）

---

## 21. 与 selectOrderListFactory.items 是否直接连接（A 级）

### 21.1 modal.shopInfo 与 selectOrderListFactory.items 关系（A 级）

| 检查 | 评估 | A-F |
|---|---|---|
| `$scope.modal.shopInfo = $scope.selectOrderListFactory.items[index]` | ❌ 0 处 | A |
| `$scope.modal.shopInfo.xxx = $scope.selectOrderListFactory.items[index].xxx` | ❌ 0 处 | A |
| `$scope.selectOrderListFactory.items[index] = $scope.modal.shopInfo` | ❌ 0 处 | A |
| `$scope.modal.shopInfo` 任何字段直接读自 `selectOrderListFactory.items` | ❌ 0 处 | A |
| `$scope.modal.shopInfo` 任何字段直接写回 `selectOrderListFactory.items` | ❌ 0 处 | A |

### 21.2 严格表述（A 级）
- "$scope.modal.shopInfo 与 $scope.selectOrderListFactory.items **0 处直接连接**"：**A**
- 两者字段路径不同源（详见 §11 / §12）

---

## 22. Factory 隔离（A 级）

### 22.1 3 个 Read + 1 个 Write Factory 模式（A 级）

| API | 行号 | Factory 模式 | 变量名 | 独立实例？ | A-F |
|---|---|---|---|---|---|
| /admin/getMedicalRecordFlowVo.json | L34862 | 匿名 `new ObjectFactory()` | ❌ 无 | ✅ | A |
| /admin/getAdminInfo.json | L35281 | 匿名 `new ObjectFactory()` | ❌ 无 | ✅ | A |
| /admin/selectMedicalProductStockList.json | L35319 | 匿名 `new ObjectFactory()` | ❌ 无 | ✅ | A |
| /admin/createMedicalStockLossOfSmallVersion.json | L35342 | 匿名 `new ObjectFactory()` | ❌ 无 | ✅ | A |

**A 级结论**：
- 4 个 API 调用全部使用**匿名 `new ObjectFactory()`**
- ❌ 0 处 `$scope.xxxFactory` 命名变量
- ❌ 0 处复用 ObjectFactory 实例
- 每次 API 调用都是**新 ObjectFactory 实例**
- 严格表述：**4 个 API 调用各自独立 ObjectFactory 实例，无任何共享**（A 级）

---

## 23. Response 样本边界（A 级 / F）

| 项 | 状态 | 标注 |
|---|---|---|
| getMedicalRecordFlowVo.json 真实 Response | ❌ 无样本 | F |
| getAdminInfo.json 真实 Response | ❌ 无样本 | F |
| selectMedicalProductStockList.json 真实 Response | ❌ 无样本 | F |
| createMedicalStockLossOfSmallVersion.json 真实 Response | ❌ 无样本 | F |
| Controller 可见字段集合 | ✅ 4 outer + 4 inner = 8 字段 | A |
| 完整 Response schema | ❌ 不可写（无样本） | F |
| 后端 DTO 字段定义 | ❌ 不可写 | L3 = F |

---

## 24. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | selectMedicalProductStockList 全局引用 | L35319 唯一 | A | L1 | |
| 02 | Controller | optometryCtrl | A | L1 | |
| 03 | Factory | 匿名 new ObjectFactory() | A | L1 | |
| 04 | Request | { medicalProductId } | A | L1 | |
| 05 | Request 字段 | medicalProductId 1 个 | A | L1 | |
| 06 | Response result.status | L35322 | A | L1 | |
| 07 | Response result.object | L35326 forEach | A | L1 | |
| 08 | Response 可见字段 | res.object[i].id 唯一 | A | L1 | |
| 09 | res.object[i].id | L35328 | A | L1 | |
| 10 | medicalProductStockId | L35328 `medical.id` | A | L1 | |
| 11 | useCount 定义 | L35289 字面量 1 | A | L1 | |
| 12 | useCount 来源 | $scope.modal.shopInfo.useCount | A | L1 | |
| 13 | useCount → lossCount | L35329 复制 | A | L1 | |
| 14 | lossReasonId 来源 | $scope.modal.shopInfo.lossReasonId (HTML 必须设置) | A + F | L1 | |
| 15 | lossReasonId → Request | L35330 复制 | A | L1 | |
| 16 | remark 来源 | $scope.modal.shopInfo.remark = "" | A | L1 | |
| 17 | remark → Request | L35331 复制 | A | L1 | |
| 18 | lossAdminId 来源 | $scope.modal.shopInfo.lossAdminId (from getAdminInfo) | A | L1 | |
| 19 | getAdminInfo → shopInfo | L35291 / L35292 | A | L1 | |
| 20 | medicalRecordId 来源 | medicalProduct.medicalRecordId | A | L1 | |
| 21 | machineCenterId 来源 | medicalProductDelivery.machineCenterId | A | L1 | |
| 22 | medicalStockLossSkuListJson 构造 | L35325-L35333 forEach push | A | L1 | |
| 23 | 多库存对象 | forEach 支持任意长度 + 1:1 push | A | L1 | |
| 24 | 过滤/去重/排序 | ❌ 0 处 | A | L1 | |
| 25 | Write success → brushData | L35346 | A | L1 | |
| 26 | 报损最小协议 | 8 字段全部 A 级闭合 | A | L1 | |

**统计**：
- **A：25 项**
- **F：1 项**（#14 lossReasonId HTML 端必须设置）
- **D / C / B / E：0**
- **E/F 升 A：0**

---

## 25. L1/L2/L3

### L1（源码事实，可证）

- 2 API 调用位置 + 完整 Request/Response 链（A）
- 4 outer 字段 + 4 inner 字段全部来源（A）
- 字段复制操作（A）
- JSON.stringify 操作（A）
- forEach 遍历行为（A）
- 0 处过滤/去重/排序（A）
- 0 处 F1/F3/F4/F5/F6 直接连接（A）
- 0 处 selectOrderListFactory.items 直接连接（A）
- 4 API Factory 独立（A）
- success → brushData 闭环（A）

### L2（业务解释，未证）

- "lossCount = 报损数量"：**E**
- "lossReasonId = 报损原因主键"：**E**
- "lossAdminId = 操作管理员 ID"：**E**
- "medicalProductStockId = 库存主键"：**E**
- "remark = 备注"：**E**
- "res.object 完整字段 = 库存列表"：**E**
- "lossReasonId HTML 端 = 报损原因下拉"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 4 个 API 后端实现 / 无 DTO schema 样本）

---

## 26. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 4 个 API 后端处理 | 无后端代码 | F |
| 4 个 API Response 完整 schema | 无样本 | F |
| res.object 完整字段集合 | 无样本 | F |
| res.object[i] 除 .id 外其它字段 | 无样本 | F |
| useCount HTML 端是否修改 | HTML 不可得 | F |
| lossReasonId HTML 端设置值 | HTML 不可得 | F |
| remark HTML 端是否修改 | HTML 不可得 | F |
| lossAdminId HTML 端是否修改 | HTML 不可得 | F |
| 7 HTML 触发点 | 不可得 | F |
| window.commonFn 实现 | 全局函数 | F |
| modal.affrim HTML ng-click | 不可得 | F |
| 业务语义（E）| — | E |

---

## 27. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 1 Read + 1 Write 全部仅静态审计 |
| selectMedicalProductStockList 实际调用 = 0 | ✅ | |
| createMedicalStockLossOfSmallVersion 实际调用 = 0 | ✅ | |
| getAdminInfo 实际调用 = 0 | ✅ | |
| getMedicalRecordFlowVo 实际调用 = 0 | ✅ | |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 164 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 164_*.md |
| 文件编号连续 | ✅ | 163 已被 S1-102 占用，本轮使用 164 |

---

## 28. 最终结论

### 28.1 报损最小协议（A 级，8 字段全闭合）

```javascript
// Read Request (selectMedicalProductStockList.json)
{
    medicalProductId: medicalProductVoList[index].medicalProduct.id  // A 级完整链
}

// Read Response 可见字段
res.object[i].id  // 唯一字段级读取

// Write Request (createMedicalStockLossOfSmallVersion.json)
{
    medicalRecordId: medicalProductVoList[index].medicalProduct.medicalRecordId,  // A 级
    machineCenterId: medicalProductVoList[index].medicalProductDelivery.machineCenterId,  // A 级
    lossAdminId: $scope.modal.shopInfo.lossAdminId = getAdminInfo().result.object.id,  // A 级
    medicalStockLossSkuListJson: JSON.stringify([
        {
            medicalProductStockId: res.object[i].id,  // 复制 Read Response
            lossCount: useCount = shopInfo.useCount = 1,  // 初始 1
            lossReasonId: lossReasonId = shopInfo.lossReasonId,  // HTML 必须设置
            remark: remark = shopInfo.remark = ""  // 初始空
        }
    ])
}

// success 行为
if (res.status == 0) {
    Popup.notice("报损成功");
    $scope.modal.changeOrder(false);  // 关闭 modal
    $scope.order.brushData(medicalRecordId);  // 重新刷 data
}
```

### 28.2 关键事实（A 级）

1. **8 字段全部 A 级闭合**（4 outer + 4 inner，Controller 视角）
2. **medicalProductStockId = res.object[i].id 跨字段复制**（A 级 — Read Response → Write Request）
3. **lossCount / lossReasonId / remark 复用同一外层值**（A 级 — 3 字段对所有 inner item 共享）
4. **res.object 元素数 = medicalStockLossSkuListJson 元素数**（A 级 1:1）
5. **0 处过滤/去重/排序**（A 级）
6. **0 处与 F1/F3/F4/F5/F6 直接代码连接**（A 级）
7. **0 处与 selectOrderListFactory.items 直接代码连接**（A 级）
8. **4 API Factory 各自独立**（A 级）
9. **Write success → brushData 闭环**（A 级 — brushData(medicalProduct.medicalRecordId)）
10. **2 处强制校验**（lossAdminId / lossReasonId 在 modal.affrim 入口）

### 28.3 S1-103 关键新发现

1. **报损完整 4 API 链路 = 3 Read + 1 Write 端到端**（getMedicalRecordFlowVo + getAdminInfo + selectMedicalProductStockList + createMedicalStockLossOfSmallVersion）
2. **4 inner 字段** 完整来源链闭合（其中 3 个字段来源依赖 HTML 端）
3. **3 字段复用**（lossCount / lossReasonId / remark）对所有 res.object 元素共享
4. **lossReasonId 是必填项**（modal.affrim 强制校验）
5. **0 处与 Delivery 链路 / selectOrderListFactory 直接连接**（独立"报损"业务支路）

### 28.4 严格表述（A 级 vs E/F）

- "8 字段全部闭合（Controller 视角）"：**A**
- "字段值是否在后端 DTO 中同源"：**F**（无后端可证）
- "lossReasonId / remark / lossAdminId HTML 端真实值"：**F**（HTML 不可得）
- "lossCount / lossReasonId / remark 业务含义"：**E**（禁止升级 A）
- "res.object 完整字段 = 库存列表"：**E**
- "modal.affrim 业务独立于 Delivery"：**A**（无代码连接）

### 28.5 不可在本轮升级为 A 的项

- 4 个 API 后端处理（F）
- 4 个 API Response 完整 schema（F）
- res.object 完整字段集合（F）
- HTML 端 useCount / lossReasonId / remark / lossAdminId 修改（F）
- modal.affrim HTML ng-click 触发点（F）
- 业务语义（E）
- modal.affrim 与 L16287 $scope.loss 报损链路是否同源（**A**：不同 controller / 不同实现 / 不同字段路径）

---

**审计结束**。
