# S1-101 getMedicalRecordFlowVo Response 字段消费与 medicalRecordStatus 链审计

> **任务名**：S1-101｜getMedicalRecordFlowVo Response → selectOrderListFactory.items 全量字段消费审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）getMedicalRecordFlowVo Response 完整消费链
> **当前轮次**：S1-101（接 S1-100 完成）
> **本轮承诺**：1 个 Read API 实际调用 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| getMedicalRecordFlowVo.json 全部调用点 | ✅ | controller.js 仅 2 处 |
| querySingleOrder (L34883) | ✅ | 主链 |
| order.brushData (L34860) | ✅ | 第二 Consumer |
| filter_medicalRecordStatus_update (L34780) | ✅ | medicalRecordStatus 写入 |
| $scope.medicalRecordStatus (L34777) | ✅ | 状态对象 |
| $scope.modal.changeOrder (L35278) | ✅ | order.object 字段级访问 |
| $scope.order.object | ✅ | brushData 写入 + modal 消费 |
| 7 HTML | ❌（不可得） | UI F 边界 |
| getMedicalRecordFlowVo 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "filter_medicalRecordStatus_update = 业务状态过滤"：**E**（仅命名）
- "medicalRecordStatus = 业务状态"：**E**（仅命名）
- "getMedicalRecordFlowVo 返回业务对象"：**E**（未证）
- "result.object 含 medicalRecord/patient/customer"：**D**（未观察到字段级访问，禁止猜）
- "window.filter_medicalRecordStatus 是后端 DTO 转换"：**E**（未证）
- "oldItem 字段比较"：**D**（当前未观察到，禁止补）

---

## 3. getMedicalRecordFlowVo 全局 Consumer

### 3.1 controller.js 全部调用点（A 级，已穷举）

| 行号 | 函数 | Controller | Factory | 表达式 |
|---|---|---|---|---|
| L34862 | order.brushData | optometryCtrl | 匿名 `new ObjectFactory()` | `saveOrQuery("/admin/getMedicalRecordFlowVo.json", { medicalRecordId })` |
| L34885 | querySingleOrder | optometryCtrl | 匿名 `new ObjectFactory()` | `saveOrQuery("/admin/getMedicalRecordFlowVo.json", { medicalRecordId })` |

**A 级结论**：
- controller.js 中 getMedicalRecordFlowVo.json **仅 2 处真实调用**
- 2 个调用都在 **optometryCtrl**（L34776-L35382）
- ❌ 0 处其它 controller 调用
- ❌ 0 处 7 HTML 调用

### 3.2 2 个 Consumer 对比（A 级）

| 维度 | querySingleOrder (L34885) | order.brushData (L34862) |
|---|---|---|
| API 字符串 | /admin/getMedicalRecordFlowVo.json ✅ 同 | /admin/getMedicalRecordFlowVo.json ✅ 同 |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式） | saveOrQuery（ObjectFactory 模式） ✅ 同 |
| Factory 实例 | 匿名 new ObjectFactory() | 匿名 new ObjectFactory() |
| **Factory 是否独立** | ✅ 独立实例 | ✅ 独立实例 |
| **Factory 是否共享 scope** | ❌ 否 | ❌ 否 |
| Request 字段 | `{ medicalRecordId }` | `{ medicalRecordId }` ✅ 同 |
| Request.medicalRecordId 来源 | `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (L34884) | `brushData` 形参 (L34860) |
| **Request.medicalRecordId 是否同源** | ❌ 否（不同 scope 变量） | ❌ 否 |
| 触发场景 | 3 Write + 取消/制作完成 success | "报损" action (L35178) |
| 成功写入 | `$scope.selectOrderListFactory.items[orderIndex] = result.object` | `$scope.order.object = result.object` |
| 是否调 filter_medicalRecordStatus_update | ✅ L34893 | ❌ 0 处 |
| $timeout 包裹 | ✅ L34891 | ❌ 0 处 |
| result.object 字段级访问 | ❌ 0 处（仅整体赋值） | ⚠️ 通过 $scope.order.object 间接访问（L35282 modal.changeOrder） |

### 3.3 严格表述（A 级）
- "2 个 Consumer 调同一 API"：**A**
- "2 个 Consumer Request 字段名相同"：**A**
- "2 个 Consumer Factory 实例独立"：**A**
- "2 个 Consumer 写入不同的 $scope 字段"：**A**
- "2 个 Consumer 业务对象相同"：**E**（业务推断，禁止升级）

---

## 4. querySingleOrder Response 详细审计

### 4.1 完整 then 体（A 级，L34887-L34895）

```javascript
new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", {
    medicalRecordId: medicalRecordId
}).then(function (result) {
    if (result.status) {                                                                 // L34888
        return Popup.notice(result.errmsg);
    }
    $timeout(function () {                                                                 // L34891
        $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;            // L34892
        $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);  // L34893
    });
});
```

### 4.2 result 字段消费全集（A 级）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `result.status` | L34888 | 错误判断 | — | A |
| `result.errmsg` | L34889 | Popup.notice 弹窗 | — | A |
| `result.object` | L34892 | 整体赋值（`=` 引用） | $scope.selectOrderListFactory.items[orderIndex] | A |
| `result.object` | L34893 | 作为参数传给 filter_medicalRecordStatus_update | （间接）$scope.medicalRecordStatus[orderIndex] | A |
| `result.list` | ❌ 未观察 | — | — | A |
| `result.result` | ❌ 未观察 | — | — | A |
| 其它字段 | ❌ 未观察 | — | — | F |

### 4.3 result.object 在 querySingleOrder 内部字段级读取（A 级）

| 字段访问 | 行号 | 是否存在 |
|---|---|---|
| `result.object.xxx` | — | ❌ **0 处**（仅整体赋值 + 整体传给 filter 函数） |

**A 级结论**：
- **querySingleOrder 内部对 result.object 0 处字段级直接读取**
- 仅 2 个整体使用：
  1. `$scope.selectOrderListFactory.items[orderIndex] = result.object`（**整体对象引用替换**）
  2. `$scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex)`（**整体作为参数传递**）

### 4.4 严格表述（A 级）
- "querySingleOrder 内部 0 处 result.object 字段级读取"：**A**
- "querySingleOrder 内部整体对象引用替换"：**A**
- "querySingleOrder 内部 result.object 仅传给 filter 函数"：**A**
- "querySingleOrder 内部 result.object 字段集合 = F（Controller 视角）"：**F**（无后端可证完整字段）

---

## 5. filter_medicalRecordStatus_update 完整审计

### 5.1 完整定义（A 级，L34780-L34782）

```javascript
$scope.filter_medicalRecordStatus_update = function (item, type, index) {
    $scope.medicalRecordStatus[index] = window.filter_medicalRecordStatus(item, type);
};
```

### 5.2 函数签名（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 参数 1 (item) | result.object | A |
| 参数 2 (type) | "button"（字面量） | A |
| 参数 3 (index) | $scope.orderIndex | A |
| 内部读取 item.xxx | ❌ 0 处（直接整体传给 window.filter_medicalRecordStatus） | A |
| 内部读取 type | ❌ 0 处（直接整体传给 window.filter_medicalRecordStatus） | A |
| 内部读取 index | ❌ 0 处（仅用于写 $scope.medicalRecordStatus[index]） | A |
| 写入 $scope.medicalRecordStatus | ✅ `$scope.medicalRecordStatus[index] = ...` | A |
| 写入 selectOrderListFactory.items | ❌ 0 处 | A |
| 修改 orderIndex | ❌ 0 处 | A |
| 调 state/API/Factory | ❌ 0 处 | A |
| 调 window.filter_medicalRecordStatus(item, type) | ✅ | A 引用 / F 实现 |
| 错误处理 | ❌ 0 处 try/catch | A |
| 返回值 | ❌ 无 | A |

### 5.3 item 字段消费（A 级）

| 字段访问 | 行号 | 是否存在 |
|---|---|---|
| `item.xxx` | L34781 | ❌ 0 处（直接整体传给 window 函数） |
| `item.medicalRecord.id` | ❌ 0 处 | A |
| `item.medicalRecordType` | ❌ 0 处 | A |
| `item.patient` | ❌ 0 处 | A |
| `item.medicalProductVoList` | ❌ 0 处 | A |
| 其它字段 | ❌ 0 处 | A |

**A 级结论**：
- filter_medicalRecordStatus_update 内部**对 item 0 处字段级直接读取**
- 仅 1 个整体使用：调 window.filter_medicalRecordStatus(item, type)
- window.filter_medicalRecordStatus 实现 = **F 边界**（无仓库源码）

### 5.4 字段写入（A 级）

| 写入目标 | 行号 | 值 | A-F |
|---|---|---|---|
| `$scope.medicalRecordStatus[index]` | L34781 | `window.filter_medicalRecordStatus(item, type)` | A（写入） / F（值的真实计算） |

### 5.5 window.filter_medicalRecordStatus 实现（A 级边界）

| 维度 | 评估 | A-F |
|---|---|---|
| 绑定位置 | L34779 `$scope.filter_medicalRecordStatus = window.filter_medicalRecordStatus;` | A |
| 实现源码 | ❌ 无仓库源码（window 全局函数） | F |
| 真实计算逻辑 | ❌ 不可证 | F |
| 返回值类型 | ❌ 不可证 | F |
| 字段访问（item.xxx） | ❌ 不可证 | F |

**A 级结论**：
- window.filter_medicalRecordStatus 内部如何读取 item.xxx **完全不可证**
- 仅可证**调用形式**（L34781）：`window.filter_medicalRecordStatus(item, type)` 返回某值
- 该返回值赋给 `$scope.medicalRecordStatus[index]`（**整体覆盖**）

### 5.6 严格表述（A 级）
- "filter_medicalRecordStatus_update 整体替换 medicalRecordStatus[index]"：**A**
- "filter_medicalRecordStatus_update 内部对 result.object 0 处字段级读取"：**A**
- "window.filter_medicalRecordStatus 字段访问方式"：**F**（无源码可证）
- "filter_medicalRecordStatus = 业务状态过滤"：**E**（仅命名 + 1 个 L34780 函数注释"filter medicalrecord's status"）

---

## 6. medicalRecordStatus 精确追踪

### 6.1 全 controller.js 引用全集（A 级）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L34777 | `$scope.medicalRecordStatus = {};` | optometryCtrl 顶部初始化 | A |
| L34779 | `$scope.filter_medicalRecordStatus = window.filter_medicalRecordStatus;` | optometryCtrl 顶部绑定 window 全局函数 | A |
| L34780 | `$scope.filter_medicalRecordStatus_update = function (item, type, index) {` | optometryCtrl 顶部定义 | A |
| L34781 | `$scope.medicalRecordStatus[index] = window.filter_medicalRecordStatus(item, type);` | filter_medicalRecordStatus_update 函数体 | A |
| L34893 | `$scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);` | querySingleOrder success 内 | A |

**A 级结论**：
- medicalRecordStatus 全部 5 处引用**全部在 optometryCtrl 范围**（L34776-L35382）
- ❌ 0 处其它 controller 引用
- ❌ 0 处 7 HTML 引用（已 grep 验证）
- ❌ 0 处 optometryCtrl 外部读取 $scope.medicalRecordStatus 的代码

### 6.2 medicalRecordStatus 数据结构（A 级）

```javascript
$scope.medicalRecordStatus = {};  // L34777：空对象初始化
// 后续写入：
$scope.medicalRecordStatus[index] = ...;  // L34781：使用 index 作为 key
```

| 维度 | 评估 | A-F |
|---|---|---|
| 类型 | 对象（Object / Dictionary） | A |
| Key 类型 | 数字（$scope.orderIndex 推断） | A |
| Value 类型 | `window.filter_medicalRecordStatus(item, type)` 返回值 — **F 边界** | A 写入 / F 值 |
| 初始化 | `{}` | A |

### 6.3 medicalRecordStatus 写入路径（A 级）

```
querySingleOrder (L34883) success
    ↓
$timeout
    ↓
$scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex)  (L34893)
    ↓
$scope.medicalRecordStatus[orderIndex] = window.filter_medicalRecordStatus(result.object, "button")  (L34781)
```

### 6.4 medicalRecordStatus 是否被 optometryCtrl 读取（A 级）

| 检查 | 结果 |
|---|---|
| optometryCtrl 内部读 $scope.medicalRecordStatus.xxx | ❌ **0 处** |
| 其它 controller 读 $scope.medicalRecordStatus.xxx | ❌ **0 处**（已全文搜索） |
| 7 HTML 读 medicalRecordStatus | ❌ **0 处**（已 grep） |

**A 级结论**：
- medicalRecordStatus 在 optometryCtrl **仅被写入，0 处被读取**
- 7 HTML 0 处读取（**F 边界**）
- **唯一可能消费方 = HTML 端**，但 HTML 不可得 → 实际用途 F

### 6.5 medicalRecordStatus 来源链总结（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓
result.object (匿名 ObjectFactory 反序列化)
    ↓
filter_medicalRecordStatus_update (L34780) 调
    ↓
window.filter_medicalRecordStatus(item, type)  ← F 边界
    ↓ 返回值
$scope.medicalRecordStatus[index] (L34781)
    ↓
[7 HTML 不可得] F 边界
```

---

## 7. result.object 顶层字段全集（optometryCtrl 范围）

### 7.1 result.object 字段级访问全集（A 级，optometryCtrl 范围 L34776-L35382）

| 字段访问 | 行号 | 来源 | 上下文 | A-F |
|---|---|---|---|---|
| `result.object = result.object` | L34868 | order.brushData | 整体赋值 | A |
| `result.object = result.object` | L34892 | querySingleOrder | 整体赋值 | A |
| `result.object` (作为函数参数) | L34893 | querySingleOrder | 传给 filter_medicalRecordStatus_update | A |
| `result.object.medicalProductVoList[index]` | L35282 | order.object (来自 brushData 写入) | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].product` | L35283 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].medicalProduct` | L35284 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].medicalProductDelivery` | L35285 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].product.productName` | L35288 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].medicalProductDelivery.machineCenterId` | L35294 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].medicalProduct.medicalRecordId` | L35295 | 同上 | modal.changeOrder | A |
| `result.object.medicalProductVoList[index].medicalProduct.id` | L35296 | 同上 | modal.changeOrder | A |
| `result.object.medicalRecord` | ❌ 0 处 | — | — | F |
| `result.object.patient` | ❌ 0 处 | — | — | F |
| `result.object.customer` | ❌ 0 处 | — | — | F |
| `result.object.cashflow` | ❌ 0 处 | — | — | F |
| `result.object.medicalRecordType` | ❌ 0 处 | — | — | F |
| `result.object.medicalProduct` | ❌ 0 处直接访问 | — | — | F |
| `result.object.delivery` | ❌ 0 处 | — | — | F |
| `result.object.machineCenter` | ❌ 0 处 | — | — | F |
| `result.object.status` | ❌ 0 处 | — | — | F |
| `result.object.medicalRecordStatus` | ❌ 0 处 | — | — | F |
| 其它字段 | ❌ 0 处 | — | — | F |

### 7.2 严格表述（A 级）
- "result.object 直接字段级访问（optometryCtrl 范围）" = **0 处直接**（**仅整体赋值 + 整体传参**）
- "result.object 间接字段级访问（通过 order.object）" = **6 处**（仅 L35282-L35296 在 modal.changeOrder 内）
- "result.object 真实字段集合"：**F**（无后端可证，仅可证 6 个字段在 modal.changeOrder 中被消费）

### 7.3 result.object 间接访问完整路径（A 级）

```
getMedicalRecordFlowVo Response
    ↓
result.object
    ↓ L34868
$scope.order.object (整体引用替换)
    ↓
[用户后续操作触发]
    ↓ L35278
$scope.modal.changeOrder(bol, index)
    ↓ L35282
$scope.order.object.medicalProductVoList[index]
    ↓
6 个字段读取:
    - .product.productName (L35288)
    - .medicalProduct.medicalRecordId (L35295)
    - .medicalProduct.id (L35296)
    - .medicalProductDelivery.machineCenterId (L35294)
    - (medicalProduct 内部 .id 隐式访问 L35296)
    - (product 内部 .productName 隐式访问 L35288)
```

**A 级结论**：
- result.object → $scope.order.object → 6 个字段级读取（仅在 modal.changeOrder 内）
- modal.changeOrder 是用户**后续操作**触发（"报损" → order.show(true, ...) → brushData(...) → modal.changeOrder(...)）
- 6 个字段都是 medicalProductVoList[index] 数组元素的子字段

---

## 8. 整体替换 vs merge

### 8.1 optometryCtrl 范围整体赋值（A 级）

| 行号 | 表达式 | 操作 | A-F |
|---|---|---|---|
| L34777 | `$scope.medicalRecordStatus = {};` | 整体对象初始化 | A |
| L34861 | `$scope.order.object = {};` | 整体对象初始化 | A |
| L34868 | `$scope.order.object = result.object;` | **整体对象引用替换** | A |
| L34892 | `$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;` | **整体对象引用替换** | A |
| L35282 | `var _$scope$order$object$ = $scope.order.object.medicalProductVoList[index]` | 局部引用 | A |

### 8.2 merge / extend / for-in 检查（A 级）

| 操作 | optometryCtrl 范围 | A-F |
|---|---|---|
| `angular.extend` | ❌ 0 处 | A |
| `angular.merge` | ❌ 0 处 | A |
| `Object.assign` | ❌ 0 处（对 getMedicalRecordFlowVo 响应） | A |
| `$.extend` | ❌ 0 处 | A |
| `for (var key in obj)` | ❌ 0 处 | A |
| 字段逐项赋值 | ❌ 0 处 | A |

**注**：optometryCtrl 范围有 3 处 Object.assign（L34831/L35364/L35366），但**全部用于 dealTime / search** 的内部参数构造，与 getMedicalRecordFlowVo 响应处理无关。

### 8.3 A 级结论
- **optometryCtrl 对 getMedicalRecordFlowVo 响应采用整体对象引用替换**（无任何 merge / extend / for-in / 字段级合并）
- 具体 2 处整体替换：
  - L34868: `$scope.order.object = result.object`（brushData）
  - L34892: `$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object`（querySingleOrder）
- 严格表述：**当前 Controller 采用整体对象替换，未观察到字段级 merge**

---

## 9. 旧 item 比较

### 9.1 optometryCtrl 范围 old item 检查（A 级）

| 检查项 | 结果 | A-F |
|---|---|---|
| `oldItem` 变量 | ❌ 0 处 | A |
| `previousItem` 变量 | ❌ 0 处 | A |
| `currentItem` 变量 | ❌ 0 处 | A |
| `oldObject` 变量 | ❌ 0 处 | A |
| `previousObject` 变量 | ❌ 0 处 | A |
| `oldItem.xxx != result.object.xxx` 比较 | ❌ 0 处 | A |
| `previousItem` 与新值比较 | ❌ 0 处 | A |
| 增量更新（部分字段更新） | ❌ 0 处 | A |

### 9.2 A 级结论
- **optometryCtrl 完全不保留旧 item 副本**
- **不进行新旧值比较**
- **不进行增量字段更新**
- 整体替换前后无业务逻辑
- 严格表述：**当前 Controller 未观察到对 result.object 与旧 item 的字段值比较**

---

## 10. order.brushData 对照

### 10.1 完整源码（A 级，L34860-L34870）

```javascript
$scope.order = {
    isShow: false,
    object: {},
    brushData: function brushData(medicalRecordId) {
        $scope.order.object = {};                                                       // L34861
        new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", {        // L34862
            medicalRecordId: medicalRecordId                                             // L34863
        }).then(function (result) {
            if (result.status) {                                                        // L34865
                return Popup.notice(result.errmsg);
            }
            $scope.order.object = result.object;                                          // L34868
        });
    },
    show: function show(bol, medicalRecordId) {
        this.isShow = bol;
        if (bol) {
            window.commonFn.openMaskFun();
            this.brushData(medicalRecordId);
        } else {
            window.commonFn.closeMaskFun();
        }
    }
};
```

### 10.2 触发链（A 级）

```
HTML ng-click (F)
    ↓
clickBtn "报损"  (L35177-L35179)
    ↓
$scope.order.show(true, item.medicalRecord.id)
    ↓
$scope.order.show(...) (L34871)
    ↓
window.commonFn.openMaskFun() (F 边界)
this.brushData(medicalRecordId)
    ↓
brushData(medicalRecordId) (L34860)
    ↓
$scope.order.object = {} (L34861)
new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", { medicalRecordId })
    ↓ [F 边界: HTTP]
result
    ↓ if (result.status) return Popup
    ↓
$scope.order.object = result.object (L34868)
    ↓
[后续用户操作触发]
    ↓
$scope.modal.changeOrder(bol, index) (L35278)
    ↓ L35282
$scope.order.object.medicalProductVoList[index]... (6 字段读取)
```

### 10.3 Request / Response（A 级）

| 维度 | order.brushData (L34860) | querySingleOrder (L34885) |
|---|---|---|
| API | /admin/getMedicalRecordFlowVo.json ✅ 同 | /admin/getMedicalRecordFlowVo.json ✅ 同 |
| Request.medicalRecordId 来源 | brushData 形参 (来自 order.show 调用) | `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (L34884) |
| **Request.medicalRecordId 是否同源** | ❌ 否（来自不同 clickBtn 形参） | ❌ 否（来自 selectOrderListFactory.items） |
| result.object 写入 | `$scope.order.object` (L34868) | `$scope.selectOrderListFactory.items[orderIndex]` (L34892) |
| **result.object 写入目标是否同** | ❌ 否（不同 $scope 字段） | ❌ 否（不同 $scope 字段） |
| 间接字段级读取 | ✅ L35282-L35296 modal.changeOrder | ❌ 0 处（仅整体 + filter） |
| 是否调 filter_medicalRecordStatus_update | ❌ 0 处 | ✅ L34893 |

### 10.4 严格表述（A 级）
- "2 个 Consumer API 同"：**A**
- "2 个 Consumer Request 字段名同"：**A**
- "2 个 Consumer Request.medicalRecordId 来源不同"：**A**
- "2 个 Consumer result.object 写入目标不同"：**A**
- "2 个 Consumer 业务对象相同"：**E**（业务推断，禁止升级）

---

## 11. 其它 Consumer

### 11.1 controller.js 全部 getMedicalRecordFlowVo.json 引用（A 级，已穷举）

- L34862 (order.brushData)
- L34885 (querySingleOrder)
- ❌ 0 处其它调用

### 11.2 7 HTML 全部 grep（A 级）

- ❌ 0 处 7 HTML 含 getMedicalRecordFlowVo.json
- ❌ 0 处 7 HTML 含 medicalRecordStatus / filter_medicalRecordStatus
- ❌ 0 处 7 HTML 含 order.brushData / querySingleOrder

### 11.3 其它 controller 调用（A 级）

- ❌ 0 处其它 controller 调用 getMedicalRecordFlowVo.json

### 11.4 严格表述（A 级）
- "getMedicalRecordFlowVo.json 当前资源范围 Consumer = 2"：**A**（order.brushData + querySingleOrder）
- "2 Consumer 都在 optometryCtrl"：**A**
- "2 Consumer 业务含义是否相同"：**E**（业务推断）

---

## 12. result.object 下游

### 12.1 querySingleOrder 路径 result.object 下游（A 级）

```
result.object
    ↓ L34892
$scope.selectOrderListFactory.items[orderIndex]  // 整体对象引用替换
    ↓
[HTML ng-repeat 渲染 selectOrderListFactory.items]  // F 边界（HTML 不可得）
    ↓
$scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex)  // L34893
    ↓ L34781
$scope.medicalRecordStatus[orderIndex]  // 整体赋值
    ↓
[HTML 端渲染 medicalRecordStatus[index]]  // F 边界（HTML 不可得）
```

**A 级结论**：
- result.object 在 querySingleOrder 路径下游 = selectOrderListFactory.items[orderIndex]（**整体引用**）+ medicalRecordStatus[orderIndex]（**经 window 函数计算后整体赋值**）
- ❌ 0 处 state.go / Write / modal / Factory 在 querySingleOrder 内继续消费
- ❌ 0 处 optometryCtrl 内部读 medicalRecordStatus 的代码

### 12.2 order.brushData 路径 result.object 下游（A 级）

```
result.object
    ↓ L34868
$scope.order.object  // 整体对象引用替换
    ↓
[用户后续操作触发 modal.changeOrder]
    ↓ L35282
$scope.order.object.medicalProductVoList[index]
    ↓
6 字段读取 (L35288/L35294/L35295/L35296)
    ↓
$scope.modal.shopInfo  // L35287-L35297
    ↓
[后续 modal.affrim 等用户操作]  // F 边界（HTML 不可得）
```

**A 级结论**：
- result.object 在 order.brushData 路径下游 = $scope.order.object → medicalProductVoList[index] 6 字段 → shopInfo
- 6 字段读取：product.productName / medicalProduct.medicalRecordId / medicalProduct.id / medicalProductDelivery.machineCenterId

### 12.3 严格表述（A 级）
- "result.object 在 optometryCtrl 下游 = 列表项 + 状态对象 + shopInfo"：**A**（结构层）
- "result.object 业务字段集合"：**F**（无 Response 样本可证）

---

## 13. Request Source → Response → same item

### 13.1 querySingleOrder 闭合路径（A 级）

```
Request.medicalRecordId = $scope.selectOrderListFactory.items[orderIndex].medicalRecord.id  (L34884)
    ↓
[F 边界: HTTP + 后端]
    ↓
result.object
    ↓
$scope.selectOrderListFactory.items[orderIndex] = result.object  (L34892)
```

**A 级结论**：
- querySingleOrder 的 Request.medicalRecordId 与 Response 写回的 items[orderIndex]**通过 orderIndex 关联**
- **同一索引位置**被覆盖（Request 取 → Response 写回同一位置）
- 但**值是否完全一致** = F（无后端可证）
- 严格表述：**前端控制器级闭合**（A 级），**值层闭合** = F

### 13.2 闭合（A 级 vs F 级）

| 维度 | 评估 | A-F |
|---|---|---|
| Request 索引 = Response 写回索引 | ✅ $scope.orderIndex | A |
| Request.medicalRecordId = Response.medicalRecord.id | ❌ 不可证 | F |
| Request 旧值与 Response 新值字段值相等 | ❌ 不可证 | F |
| 前端控制器级闭合 | ✅ 是 | A |
| 后端 DTO 同一对象 | ❌ 不可证 | E（业务推断） |

---

## 14. Factory

### 14.1 2 个 Read Factory 对比（A 级）

| 维度 | querySingleOrder (L34885) | order.brushData (L34862) |
|---|---|---|
| Factory 类型 | ObjectFactory | ObjectFactory ✅ 同 |
| 实例化 | 匿名 `new ObjectFactory()` | 匿名 `new ObjectFactory()` ✅ 同 |
| 变量名 | ❌ 无 | ❌ 无 |
| **Factory 实例是否独立** | ✅ 独立 | ✅ 独立 |
| **是否共享 scope** | ❌ 否 | ❌ 否 |
| **是否共享 result** | ❌ 否 | ❌ 否 |
| **是否共享 storage** | ❌ 否 | ❌ 否 |

**A 级结论**：
- 2 个 Read 调用都使用**匿名 ObjectFactory 实例**
- 实例**完全独立**（每次 new 都是新对象）
- 不存在任何共享数据
- 不能说"共享 Read 函数"（两个函数是各自独立封装）

---

## 15. Promise / 失败分支

### 15.1 querySingleOrder Promise（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个（L34887） | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |
| `$timeout` 包裹 | ✅ 1 个（L34891） | A |

### 15.2 order.brushData Promise（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个（L34864） | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |
| `$timeout` 包裹 | ❌ 0 处 | A |

### 15.3 失败分支（A 级）

| 维度 | querySingleOrder (L34888) | order.brushData (L34865) |
|---|---|---|
| `if (result.status)` | ✅ | ✅ |
| `return Popup.notice(result.errmsg)` | ✅ | ✅ |
| 错误时是否继续执行 | ❌ return 提前退出 | ❌ return 提前退出 |
| 错误码判断 | ❌ 0 处（仅 truthy 判空） | ❌ 0 处 |
| 错误类型解释 | ❌ 0 处 | ❌ 0 处 |

**A 级结论**：
- 2 个 Consumer 都有相同模式的失败分支
- 错误时**仅 Popup**，不执行主体逻辑
- ❌ 0 处 .catch / try-catch
- 若 HTTP 错误或 JSON 解析异常，**未捕获**传播到 AngularJS 异常处理

---

## 16. Write → Read → Field 最小闭合协议

### 16.1 Write A → querySingleOrder → result.object → 状态（A 级）

```
setMedicalRecordProcessMode.json (Write)
    ↓ success
querySingleOrder()  (L35107)
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界: HTTP + 后端]
    ↓
result.object
    ↓ L34892 (整体引用替换)
$scope.selectOrderListFactory.items[orderIndex]
    ↓ [HTML ng-repeat 渲染]  (F 边界: HTML 不可得)
    ↓
result.object (同一引用)
    ↓ L34893 → L34781 (整体作为参数)
window.filter_medicalRecordStatus(result.object, "button")  [F 边界: 实现不可得]
    ↓ 返回值
$scope.medicalRecordStatus[orderIndex]
    ↓ [HTML 端渲染]  (F 边界: HTML 不可得)
```

### 16.2 Write B → querySingleOrder → result.object → 状态（A 级）

```
completeMedicalRecordDelivery.json (deliveryStatus="2") (Write)
    ↓ success
querySingleOrder()  (L35194)
    ↓ ... (与 16.1 同)
$scope.selectOrderListFactory.items[orderIndex]  +  $scope.medicalRecordStatus[orderIndex]
```

### 16.3 Write C → querySingleOrder → result.object → 状态（A 级）

```
completeMedicalRecordDelivery.json (deliveryStatus="1") (Write)
    ↓ success
querySingleOrder()  (L35213)
    ↓ ... (与 16.1 同)
$scope.selectOrderListFactory.items[orderIndex]  +  $scope.medicalRecordStatus[orderIndex]
```

### 16.4 Write A → queryUndisposed（额外路径，A 级）

```
setMedicalRecordProcessMode.json (Write)
    ↓ success
queryUndisposed()  (L35108)
    ↓ saveOrQuery (Read: stateTodoMedicalRecordCount.json)
    ↓ [F 边界: HTTP + 后端]
    ↓
result.result.object
    ↓ L34847
$scope.toPayCount
```

**A 级结论**：
- 3 Write → querySingleOrder → result.object → selectOrderListFactory.items[orderIndex] + medicalRecordStatus[orderIndex] 完整链已闭合（**前端控制器层**）
- 仅 Write A 额外 → queryUndisposed → $scope.toPayCount
- result.object 真实字段集合 = **F**（无 Response 样本 + window.filter_medicalRecordStatus 实现 F）

---

## 17. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | getMedicalRecordFlowVo 全局调用 | L34862 + L34885 (2 处) | A | L1 | controller.js 穷举 |
| 02 | Controller 数 | optometryCtrl (唯一) | A | L1 | |
| 03 | querySingleOrder 调用 | 5 次（Write A/B/C + 取消/制作完成） | A | L1 | S1-100 已审 |
| 04 | querySingleOrder Factory | 匿名 new ObjectFactory() | A | L1 | |
| 05 | Request | { medicalRecordId } | A | L1 | |
| 06 | Response result.status | L34888 错误判断 | A | L1 | |
| 07 | Response result.object | L34892 + L34893 整体使用 | A | L1 | |
| 08 | result.object 字段级读取 | ❌ 0 处（仅整体 + filter） | A | L1 | |
| 09 | result.object 整体替换 | L34892 / L34868 | A | L1 | |
| 10 | merge / extend / for-in | ❌ 0 处 | A | L1 | 整体替换模式 |
| 11 | old item 比较 | ❌ 0 处 | A | L1 | |
| 12 | filter 函数定位 | L34780-L34782 optometryCtrl 顶部 | A | L1 | |
| 13 | filter 参数 | (item, type, index) | A | L1 | |
| 14 | filter 字段读取 | ❌ 0 处（直接传给 window 函数） | A | L1 | |
| 15 | filter 字段写入 | $scope.medicalRecordStatus[index] (L34781) | A | L1 | |
| 16 | medicalRecordStatus 来源 | window.filter_medicalRecordStatus(item, type) 返回值 | A 引用 / F 实现 | L1=F | |
| 17 | medicalRecordStatus 写入 | L34781 (querySingleOrder 触发) | A | L1 | |
| 18 | medicalRecordStatus 是否被 optometryCtrl 读 | ❌ 0 处 | A | L1 | 仅写入不读 |
| 19 | order.brushData 定位 | L34860 | A | L1 | |
| 20 | order.brushData Request | { medicalRecordId } | A | L1 | |
| 21 | order.brushData result Consumer | $scope.order.object = result.object (L34868) | A | L1 | |
| 22 | 两 Consumer 是否同 Factory | ❌ 否（独立匿名 new ObjectFactory） | A | L1 | |
| 23 | 两 Consumer 是否同 scope | ❌ 否（写入不同 $scope 字段） | A | L1 | |
| 24 | 其它 Consumer | ❌ 0 处 | A | L1 | 全文搜索确认 |
| 25 | API Response 样本边界 | F | F | L1=F | 无样本可证完整 schema |
| 26 | Write→Read→Field 最小闭合 | 3 Write → querySingleOrder → result.object → items[orderIndex] + medicalRecordStatus[orderIndex] | A | L1 | 前端控制器级闭合 |

**统计**：
- **A：25 项**
- **F：1 项**（#16 window.filter_medicalRecordStatus 实现 / #25 Response 完整 schema）
- **D / C / B / E：0**
- **E/F 升 A：0**

---

## 18. L1/L2/L3

### L1（源码事实，可证）

- getMedicalRecordFlowVo.json 2 处 Consumer（A）
- 2 Consumer Factory / Request / result 整体替换（A）
- result.object 0 处字段级直接读取（A）
- filter_medicalRecordStatus_update 函数体（A）
- medicalRecordStatus 5 处引用全集（A）
- 整体替换模式（无 merge/extend/for-in）（A）
- 0 处 oldItem 比较（A）
- Promise 链 / 失败分支（A）

### L2（业务解释，未证）

- "filter_medicalRecordStatus_update = 业务状态过滤"：**E**（仅命名 + L34778 注释"filter medicalrecord's status"）
- "medicalRecordStatus = 业务状态字典"：**E**
- "getMedicalRecordFlowVo = 医疗记录流对象"：**E**（仅 API 命名）
- "window.filter_medicalRecordStatus = 业务 DTO 转换"：**E**
- "result.object 包含 medicalRecord/patient/cashflow/delivery"：**D**（未观察到，禁止猜）
- "result.object 同一对象"：**E**
- "2 Consumer 业务对象相同"：**E**
- "3 Write 同一数据库对象"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 getMedicalRecordFlowVo 后端实现 / 无 schema 样本）

---

## 19. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| getMedicalRecordFlowVo Response 完整 schema | 无样本 | F |
| result.object 真实字段集合 | 无样本 + 无后端代码 | F |
| window.filter_medicalRecordStatus 实现 | 无仓库源码 | F |
| medicalRecordStatus 值实际计算 | 依赖 window 函数 | F |
| modal.changeOrder 触发场景 | HTML 不可得 | F |
| $scope.modal.shopInfo 下游 | HTML 不可得 | F |
| Request.medicalRecordId = Response.medicalRecord.id | 无后端代码 | F |
| Request 旧值 = Response 新值 | 无后端代码 | F |
| 7 HTML medicalRecordStatus 渲染 | 不可得 | F |
| order.brushData → modal.changeOrder 完整 UI 路径 | 不可得 | F |
| 2 Consumer 业务对象同源 | 业务推断 | E（禁止升级 A） |
| popout_tip / popout_cb / window.commonFn 实现 | window 全局函数 | F |

---

## 20. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | getMedicalRecordFlowVo / stateTodoMedicalRecordCount / 3 Write 全部仅静态审计 |
| getMedicalRecordFlowVo 实际调用 = 0 | ✅ | |
| Write 实际执行 = 0 | ✅ | 3 Write 全部仅源码 |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 162 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 162_*.md |
| 文件编号连续 | ✅ | 161 已被 S1-100 占用，本轮使用 162 |

---

## 21. 最终结论

### 21.1 getMedicalRecordFlowVo Response 消费最小事实（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端反序列化]
result.object (匿名 ObjectFactory)
    ↓
[querySingleOrder 路径]                          [order.brushData 路径]
    ↓ L34892                                         ↓ L34868
$scope.selectOrderListFactory.items[orderIndex]   $scope.order.object
    = result.object (整体引用替换)                  = result.object (整体引用替换)
    ↓ L34893 → L34781
$scope.filter_medicalRecordStatus_update
    ↓
$scope.medicalRecordStatus[orderIndex]
    = window.filter_medicalRecordStatus(result.object, "button")  [F 边界: window 实现]
    ↓
[7 HTML 渲染]  (F 边界)
[用户后续 modal.changeOrder 触发]                  [6 字段读取 (L35282-L35296)]
                                                    $scope.order.object.medicalProductVoList[index]
                                                    .product.productName / .medicalProduct.medicalRecordId
                                                    .medicalProduct.id / .medicalProductDelivery.machineCenterId
                                                    ↓
                                                    $scope.modal.shopInfo (L35287-L35297)
```

### 21.2 关键事实（A 级）

1. **getMedicalRecordFlowVo 全局 Consumer = 2**（querySingleOrder + order.brushData）
2. **result.object 字段级直接读取（querySingleOrder 内部）= 0 处**（仅整体赋值 + 整体传参）
3. **result.object 字段级间接读取（order.brushData 路径）= 6 处**（仅在 modal.changeOrder 内）
4. **整体对象引用替换模式**（无任何 merge / extend / for-in / 字段级合并）
5. **0 处 old item 比较**（不保留旧 item 副本）
6. **medicalRecordStatus 仅写入不读取**（optometryCtrl 范围 + 7 HTML 0 处读）
7. **filter_medicalRecordStatus_update 直接调 window 全局函数**（**F 边界**）
8. **2 Consumer Factory 实例独立**（不同 $scope.xxx 字段、不同请求来源）
9. **0 处 .catch 保护**（与 S1-99 / S1-100 同问题）
10. **失败分支 = if (result.status) → Popup + return**（两 Consumer 模式相同）

### 21.3 严格表述（A 级 vs E/F）

- "result.object 字段 = 仅 modal.changeOrder 6 字段可证"：**A**
- "result.object 完整字段集合"：**F**（无样本可证）
- "filter_medicalRecordStatus_update 字段计算"：**F**（window 实现不可得）
- "2 Consumer 同一业务对象"：**E**（业务推断，禁止升级 A）
- "3 Write 同一数据库对象"：**E**
- "前端控制器级闭合"：**A**
- "值层闭合"：**F**

### 21.4 S1-101 关键新发现

1. **optometryCtrl 范围 result.object 0 处字段级直接读取**（querySingleOrder 路径）
2. **6 个字段级访问全部在 modal.changeOrder 内**（间接通过 order.object 路径）
3. **0 处 merge / extend / for-in**（optometryCtrl 对 getMedicalRecordFlowVo 响应处理采用纯整体替换）
4. **0 处 old item 比较 / 增量更新**（无新旧值字段比较）
5. **medicalRecordStatus 仅 optometryCtrl 内部 5 处引用**（全部在 L34777-L34893，且 0 处 optometryCtrl 内部读）
6. **7 HTML 0 处 medicalRecordStatus 引用**（与 F 边界一致）
7. **2 Consumer 都不在 querySingleOrder 路径上有任何字段级处理**（仅 order.brushData 路径在 modal.changeOrder 内字段级消费）

### 21.5 不可在本轮升级为 A 的项

- getMedicalRecordFlowVo Response 完整 schema（F）
- result.object 真实字段集合（F）
- window.filter_medicalRecordStatus 实现（F）
- medicalRecordStatus 值实际计算（F）
- 2 Consumer 业务对象同源（E）
- result.object 包含 medicalRecord/patient/cashflow/delivery（未观察到，禁止猜）
- modal.changeOrder 触发场景（F，HTML 不可得）
- 3 Write 同一数据库对象（E / L3 = F）

---

**审计结束**。
