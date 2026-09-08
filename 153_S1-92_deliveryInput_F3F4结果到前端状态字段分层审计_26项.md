# S1-92 deliveryInput F3/F4 Result → 前端状态字段分层审计

> 审计对象：`deliveryInputCtrl` L3812-4021（209 行）+ F3/F4 Response → Controller 中间对象 → F5/F6 Request 字段分层
> 任务来源：S1-92（基于 S1-90/91 已完成 F4→F5 / F3→F6 字段级闭合）
> 审计立场：**只按源码证据；严格区分 3 层字段（API 原始 / Controller 中间 / F5-F6 Request）；禁止把 UI 临时状态当 API Schema；Write API 绝不调用**

---

## 1. 审计范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryInputCtrl | L3812-4021（**209 行**）| 完整二次确认 |
| F3/F4 Response 消费 | 9 处 F4 + 1 处 F3 | A |
| 4 字段状态性质 | medicalProductId / machineCenterId / stockInSkuId / deliveryCount / listCount / planDeliveryTime | A |
| 前端临时状态 | stockDetail / addOrderModal + 0 处 selected/checked | A |
| 跨层转换 | F3→F6 + F4→F5 | A |
| UI 触发 | **F**（HTML 不可得）| F |
| Write API 实际调用 | **0** | A |

---

## 2. 证据等级

| 等级 | 含义 |
|---|---|
| A | 直接源码证据 |
| B | 多源互证 |
| C | 局部/不完整 |
| D | 冲突/明确缺陷 |
| E | 合理业务推断 |
| F | 当前证据范围未观察/不可得 |

**关键纪律**：
- 严格区分 3 层：API 原始字段 / Controller 中间对象 / F5-F6 Request 字段
- 同名字段 ≠ 同一对象（**S1-91 已确认字段名多次重命名**）
- 禁止把 deliveryCount / stockInSkuId / machineCenterId 解释为"用户输入/选择"（除非 HTML 不可证）
- Write API 绝不调用

---

## 3. 3 层字段分类总表

### 3.1 字段层级定义

| 层级 | 含义 | 典型形式 |
|---|---|---|
| **L1-API** | 后端 API Response 原始字段 | `res.list[i].xxx` / `res.object.xxx` |
| **L1-Controller** | Controller 新建/派生的中间对象 | `arr` / `arr[i]` / `medicalProductStockBatctPoListJson` / `medicalProductStocks` |
| **L1-Request** | 最终 F5/F6 Request 字段 | `{ listCount, medicalProductStockBatctPoListJson }` / `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` |
| **F-UI** | HTML 内 ng-model / input / select 等 | （F 边界，HTML 不可得）|

### 3.2 6 关键字段层级分类

| 字段 | L1-API 原始 | L1-Controller 中间 | L1-Request 最终 |
|---|---|---|---|
| `medicalProductId` (F4→F5) | `result.list[i].medicalProduct.id` (L3998) | 隐式复制 | F5 medicalProductStockBatctPoListJson[].medicalProductId |
| `medicalProductId` (F3→F6) | `result.list[i].medicalProduct.id` (L3962) | map 重命名为 medicalProductId (L3962) | F6 medicalProductMachineCenterPoListJson[].medicalProductId |
| `stockInSkuId` (F4→F5) | `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` (L3991) | 隐式复制 | F5 medicalProductStockBatctPoListJson[].medicalProductStocks[].stockInSkuId |
| `deliveryCount` (F4→F5) | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` (L3989/L3991/L3992) | 隐式复制 | F5 medicalProductStockBatctPoListJson[].medicalProductStocks[].deliveryCount |
| `listCount` (F4→F5) | `result.list.length` (L4007) | 直接计算 | F5 listCount |
| `machineCenterId` (F3→F6) | `result.list[i].machineCenter.id` (L3962) | map 重命名为 machineCenterId (L3962) | F6 medicalProductMachineCenterPoListJson[].machineCenterId |
| `planDeliveryTime` (F3→F6) | ❌ 不存在 API 字段 | `$scope.startTime` (L3966) | F6 planDeliveryTime |

**A**：6 字段完整层级分类 A 级（A）。

---

## 4. F3 result.list 字段全集

### 4.1 F3 result.list 字段访问

| 字段路径 | 行号 | 形式 | 消费 |
|---|---|---|---|
| `result.list` | L3961 | 读（map 外层）| selectOrder.map |
| `result.list[i]` (v) | L3962 | 读（map callback 参数）| selectOrder.map |
| `v.medicalProduct.id` | L3962 | 读 | F6 medicalProductId |
| `v.machineCenter.id` | L3962 | 读 | F6 machineCenterId |

**A**：F3 result.list **4 字段访问**（A）。

### 4.2 F3 result.list 元素结构（已观察）

| 字段 | 类型 | 读入 F6 | 等级 |
|---|---|---|---|
| `medicalProduct.id` | number | ✅ | A |
| `machineCenter.id` | number | ✅ | A |
| 其它字段 | **F** | — | F |

**F**：F3 result.list 完整字段（除 2 个已观察外）= **F 边界**（资源范围外）。

### 4.3 F3 result.list 是否被 controller 修改

| 检查项 | 结果 |
|---|---|
| `v.xxx = ...` | ❌ 0 处 |
| `item.xxx = ...` | ❌ 0 处 |
| `result.list[i].xxx = ...` | ❌ 0 处 |
| `arr[i].medicalProductId = v.medicalProduct.id` | ❌ 0 处（map 创建新对象）|
| `arr[i].machineCenterId = v.machineCenter.id` | ❌ 0 处（map 创建新对象）|

**A**：F3 result.list **0 处被 controller 修改**（map 创建新对象，源对象保留，A）。

---

## 5. selectOrder() 完整审计

### 5.1 完整代码（再确认）

```javascript
// L3955-3977
$scope.selectOrder = function () {
    if (!$scope.startTime) {  // L3956
        Popup.notice("请选择取镜日期");
        return false;
    }
    var arr = $scope.getCenterListFactory.result.list.map(function (v) {  // L3961
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);  // L3964
    $scope.createOrderFactory = new ObjectFactory();  // L3965
    var createPromise = $scope.createOrderFactory.saveOrQuery(  // L3966
        '/admin/sendMedicalProductToMachineCenter.json',
        { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }
    );
    createPromise.then(function (res) {  // L3967
        if (res.status == 1) {
            Popup.notice(res.errmsg);
        } else {
            Popup.notice('发送成功');
            $scope.addOrderModal = false;  // L3973
            $state.reload();  // L3974
        }
    });
};
```

### 5.2 selectOrder 中间对象

| 局部变量 | 行号 | 类型 | 用途 |
|---|---|---|---|
| `arr` | L3961 | array | map 输出的新对象数组 |

**A**：
- selectOrder 内部**仅 1 个局部变量**：`arr`（A）
- `arr` 元素 = `{ medicalProductId, machineCenterId }`（2 字段，A）
- `arr` 通过 JSON.stringify 序列化后进入 F6 Request（A）

### 5.3 selectOrder 字段重命名

| 层级 | 字段名 | 出现位置 |
|---|---|---|
| F3 result.list | `medicalProduct.id` / `machineCenter.id` | L3962（v 读取）|
| L1-Controller (arr) | `medicalProductId` / `machineCenterId` | L3962（map 返回）|
| L1-Request (F6) | `medicalProductId` / `machineCenterId` | L3966 |

**A**：
- F3 字段名 `medicalProduct.id` → L1-Controller 重命名 `medicalProductId`（A）
- F3 字段名 `machineCenter.id` → L1-Controller 重命名 `machineCenterId`（A）
- L1-Controller → L1-Request 字段名**保持一致**（A）

### 5.4 F3 result.list 在 selectOrder 中 0 处修改

**A**：selectOrder 内**仅读取** F3 result.list，**0 处写入**（map 创建新对象，A）。

---

## 6. F4 result.list 字段全集

### 6.1 F4 result.list 字段访问（saveStock 内 9 处）

| 字段路径 | 行号 | 形式 |
|---|---|---|
| `result.list` | L3985 | 读（外层 for）|
| `result.list.length` | L3985 | 读（外层 length）|
| `result.list[i].deliveryStockInSkuVoList` | L3988 | 读（内层 for）|
| `result.list[i].deliveryStockInSkuVoList.length` | L3988 | 读（内层 length）|
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount > 0` | L3989 | 读（条件）|
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | L3991 | 读 |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | L3991 | 读 |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount < 0` | L3992 | 读（条件）|
| `result.list[i].medicalProduct.id` | L3998 | 读 |

**A**：F4 result.list **9 处访问**（A）。

### 6.2 F4 result.list 元素结构（已观察）

| 字段路径 | 类型 | 读入 F5 | 等级 |
|---|---|---|---|
| `result.list[i].medicalProduct.id` | number | ✅ medicalProductId | A |
| `result.list[i].deliveryStockInSkuVoList.length` | number | ❌（仅循环用）| A |
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | number | ✅ stockInSkuId | A |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | number | ✅ deliveryCount | A |

### 6.3 F4 result.list 元素结构（未观察）

| 字段路径 | 是否访问 | 等级 |
|---|---|---|
| `result.list[i].medicalProduct.objectId` | ❌ saveStock 内不读 | F（saveStock 不依赖此字段）|
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.xxx`（除 .id 外）| ❌ saveStock 内不读 | F |
| 其它顶层字段 | **F 边界** | F |

**A**：saveStock 内访问的 F4 result.list 字段**仅 4 个**（A）；其它字段 = F 边界。

### 6.4 F4 result.list 是否被 controller 修改

| 检查项 | 结果 |
|---|---|
| `result.list[i].xxx = ...` | ❌ 0 处 |
| `arr[i][j].stockInSkuId = ...` | ❌ 0 处（push 创建新对象）|
| `arr[i][j].deliveryCount = ...` | ❌ 0 处（push 创建新对象）|
| `medicalProductStockBatctPoListJson[i].xxx = ...` | ❌ 0 处（push 创建新对象）|

**A**：F4 result.list **0 处被 controller 修改**（saveStock 全部 push 创建新对象，A）。

---

## 7. saveStock() 中间对象完整审计

### 7.1 saveStock 内部所有临时变量

| 变量 | 行号 | 类型 | 来源 | 进入 F5? |
|---|---|---|---|---|
| `arr` | L3981 | array | 新建 `[]` | ❌（中间对象）|
| `arr[i]` | L3987 | array | 新建 `[]` | ❌（中间对象）|
| `medicalProductStockBatctPoListJson` | L3983 | array | 新建 `[]` | ✅（最终 Request 字段）|
| `medicalProductStockListJson` | L3984 | undefined | 声明（**未使用，D 残留**）| ❌ |

### 7.2 数组操作汇总

| 操作 | 行号 | 形式 |
|---|---|---|
| `var arr = []` | L3981 | 初始化 |
| `var medicalProductStockBatctPoListJson = []` | L3983 | 初始化 |
| `var medicalProductStockListJson` | L3984 | 声明（**D 残留**）|
| `arr[i] = []` | L3987 | 二维数组初始化 |
| `arr[i].push({stockInSkuId, deliveryCount})` | L3991 | 内层 push |
| `medicalProductStockBatctPoListJson.push({medicalProductId, medicalProductStocks: arr[i]})` | L3998 | 外层 push |
| `JSON.stringify(medicalProductStockBatctPoListJson)` | L4007 | 序列化 |

**A**：saveStock 内部**4 个 array 操作**（A）。

### 7.3 类型转换 / 复制

| 操作 | 出现次数 |
|---|---|
| `Number()` | 0 |
| `parseInt()` | 0 |
| `parseFloat()` | 0 |
| `String()` | 0 |
| `toString()` | 0 |
| `JSON.parse()` | 0 |
| `angular.copy()` | 0 |
| `Array.from()` | 0 |

**A**：saveStock 内**0 处类型转换或复制**（A）。

---

## 8. 4 字段状态性质详细分析

### 8.1 medicalProductId 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | `result.list[i].medicalProduct.id` (F3/F4 同一字段名) | F3 L3962 / F4 L3998 | A |
| L1-Controller (F3→F6) | `medicalProductId` | L3962（map 重命名）| A |
| L1-Controller (F4→F5) | `medicalProductId` | L3998（直接 push）| A |
| L1-Request (F6) | `medicalProductId` | L3966 | A |
| L1-Request (F5) | `medicalProductId` | L3998 → L4007 | A |
| F-UI (ng-model) | ❌ 0 处 | controller 不写入 | F |

**A**：medicalProductId 状态 = **纯 API 原始**（A）。**F-UI 介入 = F 边界**。

### 8.2 machineCenterId 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | `result.list[i].machineCenter.id` (F3) | L3962 | A |
| L1-Controller | `machineCenterId` | L3962（map 重命名）| A |
| L1-Request (F6) | `machineCenterId` | L3966 | A |
| F-UI (ng-model) | ❌ 0 处 | controller 不写入 | F |

**A**：machineCenterId 状态 = **纯 API 原始 + Controller 重命名**（A）。**F-UI 介入 = F 边界**。

**F**：
- 业务上 "用户选择 machineCenter" 的证据 = **F 边界**（HTML 不可得）
- 不能写"用户在 UI 选择 machineCenterId"

### 8.3 stockInSkuId 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` (F4) | L3991 | A |
| L1-Controller | `stockInSkuId` | L3991（push 重命名）| A |
| L1-Request (F5) | `stockInSkuId` | L3991 → L4007 | A |
| F-UI (ng-model) | ❌ 0 处 | controller 不写入 | F |

**A**：stockInSkuId 状态 = **纯 API 原始 + Controller 重命名**（A）。**F-UI 介入 = F 边界**。

### 8.4 deliveryCount 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` (F4) | L3989/L3991/L3992 | A |
| L1-Controller | `deliveryCount` | L3991（隐式复制）| A |
| L1-Request (F5) | `deliveryCount` | L3991 → L4007 | A |
| F-UI (ng-model) | ❌ 0 处（**HTML 不可得**）| controller 不写入 | F |

**A**：
- deliveryCount 在 controller 内**纯读不写**（A）
- saveStock 内 0 处 `arr[i][j].deliveryCount = ...`（A）
- deliveryCount 字段名**4 层复用**（F4 result / arr / medicalProductStockBatctPoListJson / F5 Request，A）

**F**：
- 业务上"用户输入 deliveryCount"的证据 = **F 边界**（HTML 不可得）
- 不能写"用户在 UI 修改 deliveryCount"
- **但 saveStock 0 处 Controller 写入是 A 级证据**（controller 不会修改 deliveryCount）

### 8.5 listCount 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | `result.list.length` (F4) | L4007 | A |
| L1-Controller | 直接读取，无中间对象 | — | A |
| L1-Request (F5) | `listCount` | L4007 | A |
| F-UI (ng-model) | ❌ 0 处 | controller 不写入 | F |

**A**：listCount = **直接 L1-API → L1-Request**（无 Controller 中间对象，A）。

### 8.6 planDeliveryTime 状态性质

| 层级 | 字段名 | 出现位置 | 等级 |
|---|---|---|---|
| L1-API | ❌ 不存在（F3 不返回 planDeliveryTime）| — | A |
| L1-Controller | `$scope.startTime` | L3933/L3832/L3964 | A |
| L1-Request (F6) | `planDeliveryTime` | L3966 | A |
| F-UI (datepicker ng-model) | **❓ F 边界** | HTML 不可得 | F |

**A**：
- planDeliveryTime **不存在于任何 API Response**（A）
- planDeliveryTime 来源 = **$scope.startTime**（A）
- $scope.startTime 写入点：L3832 (Controller 重置) / L3933 (searchDate) / L3964 (selectOrder 格式化)（A）
- $scope.startTime UI 来源 = **F 边界**（HTML 不可得）

**E 边界**：
- Popup 文案"请选择取镜日期"（L3957）= **E 推测**（HTML 不可得，不能直接证明 UI 显示该文案）

### 8.7 4 字段状态性质汇总

| 字段 | 状态性质 | UI 介入 |
|---|---|---|
| medicalProductId | **API 原始** | ❌ F 边界 |
| machineCenterId | **API 原始 + Controller 重命名** | ❌ F 边界 |
| stockInSkuId | **API 原始 + Controller 重命名** | ❌ F 边界 |
| deliveryCount | **API 原始**（saveStock 0 处 Controller 写入）| ❌ F 边界 |
| listCount | **API 派生**（length）| ❌ F 边界 |
| planDeliveryTime | **$scope.startTime**（不存在 API 字段）| ⚠️ F 边界（datepicker）|

**A**：4 字段（medicalProductId / machineCenterId / stockInSkuId / deliveryCount / listCount）= **100% 纯 API 来源**（A）。
**A**：deliveryCount **saveStock 内 0 处写入**是 **A 级关键证据**（即使 HTML 不可得，也证明 controller 不会修改 deliveryCount）。
**F**：6 字段的 UI ng-model 绑定 = F 边界（HTML 不可得）。

---

## 9. stockDetail 完整生命周期（A 级）

### 9.1 stockDetail 全部出现位置

| 行号 | 操作 | 形式 |
|---|---|---|
| L3882 | 写 | `$scope.stockDetail = true;`（showDeliveryModal 末尾）|
| L4017 | 写 | `$scope.stockDetail = false;`（F5 success）|

**A**：stockDetail **仅 2 处访问**（A）。

### 9.2 stockDetail 状态机

```
初始: undefined / false (Controller 启动时未设置)
    ↓ [A] (L3882)
showDeliveryModal 触发
    → stockDetail = true  (modal 打开)
    ↓ [A]
[HTML 渲染期，stockDetail 决定 modal 可见性]
    ↓ [A] (L4017)
F5 saveStock success
    → stockDetail = false  (modal 关闭)
```

**A**：stockDetail = **modal 可见性状态变量**（A）。

### 9.3 stockDetail 与 Save API 关系

| Save API | stockDetail 写入 | 状态变化 |
|---|---|---|
| F5 (saveMedicalProductStockBatch) | L4017 `$scope.stockDetail = false` | success 时关闭 modal |
| F6 (sendMedicalProductToMachineCenter) | ❌ 0 处 | — |

**A**：stockDetail **仅 F5 success 关闭**（A）。

### 9.4 F-UI（HTML ng-show/ng-if）

| 检查项 | 结果 |
|---|---|
| HTML ng-show=stockDetail | **F 边界**（HTML 不可得）|
| HTML ng-if=stockDetail | **F 边界**（HTML 不可得）|
| controller 内对 stockDetail 读取 | ❌ 0 处（**仅写入**，不读）|

**A**：stockDetail 在 controller 内**只写不读**（A）；UI 内读取 = F 边界。

---

## 10. addOrderModal 完整生命周期（A 级）

### 10.1 addOrderModal 全部出现位置

| 行号 | 操作 | 形式 |
|---|---|---|
| L3831 | 写 | `$scope.addOrderModal = true;`（showAddModal 开头）|
| L3953 | 写 | `$scope.addOrderModal = false;`（hideAddModal）|
| L3973 | 写 | `$scope.addOrderModal = false;`（F6 success）|

**A**：addOrderModal **3 处访问**（A）。

### 10.2 addOrderModal 状态机

```
初始: undefined / false (Controller 启动时未设置)
    ↓ [A] (L3831)
showAddModal 触发
    → addOrderModal = true  (modal 打开)
    ↓ [A]
[HTML 渲染期，addOrderModal 决定 modal 可见性]
    ↓ [A] (L3953) - hideAddModal 调用
    → addOrderModal = false  (modal 关闭)
    OR ↓ [A] (L3973) - F6 success
    → addOrderModal = false  (modal 关闭)
```

**A**：addOrderModal = **modal 可见性状态变量**（A）。

### 10.3 addOrderModal 关闭路径

| 触发 | 行号 | 操作 |
|---|---|---|
| 用户点击关闭按钮（hideAddModal）| L3953 | `$scope.addOrderModal = false` |
| F6 selectOrder success | L3973 | `$scope.addOrderModal = false` |

**A**：addOrderModal **2 条关闭路径**（A）。

### 10.4 hideAddModal 完整代码

```javascript
// L3952-3954
$scope.hideAddModal = function () {
    $scope.addOrderModal = false;
};
```

**A**：hideAddModal 唯一作用 = 关闭 addOrderModal（A）。

### 10.5 F-UI

| 检查项 | 结果 |
|---|---|
| HTML ng-show=addOrderModal | **F 边界** |
| HTML ng-if=addOrderModal | **F 边界** |
| controller 内对 addOrderModal 读取 | ❌ 0 处（**仅写入**，不读）|

**A**：addOrderModal 在 controller 内**只写不读**（A）；UI 内读取 = F 边界。

---

## 11. 其它临时状态变量全仓搜索

### 11.1 deliveryInputCtrl 范围内的状态变量

| 变量 | 出现次数 | 用途 |
|---|---|---|
| `addOrderModal` | 3 处 | modal 可见性（F3 关联）|
| `stockDetail` | 2 处 | modal 可见性（F4 关联）|
| `addOrderModal` 关联 modal 内容 | showAddModal selectOrder 流程 | F3+F6 |
| `stockDetail` 关联 modal 内容 | showDeliveryModal saveStock 流程 | F4+F5 |
| `dateSearch` | 4 处 | L3943/L3945/L3948/L3948（changeDate 设置）|
| `searchDate` (function) | 1 处定义（L3931）+ 0 处直接调用 | datepicker 触发 |

### 11.2 全仓 0 处的状态变量

| 变量 | 出现次数 | 等级 |
|---|---|---|
| `selected` | 0 处 | A |
| `checked` | 0 处 | A |
| `current` | 0 处 | A |
| `active` | 0 处 | A |
| `choose` | 0 处 | A |
| `disabled` | 0 处 | A |
| `medicalRecordId` | 0 处（deliveryInputCtrl 内）| A |
| `medicalExamineIdArray` | 0 处（deliveryInputCtrl 内）| A |

**A**：deliveryInputCtrl 范围内**0 处** `selected` / `checked` / `current` / `active` / `choose` / `disabled` / `medicalRecordId` / `medicalExamineIdArray`（A）。

**注**：
- `medicalRecordId` 在 **deliveryInputRecordCtrl**（L4036）和 **deliveryListCtrl 不存在**，但**不在 deliveryInputCtrl 范围**
- 0 处 `selectedXXX` / `checkedXXX` 中间状态变量

---

## 12. UI → Controller 边界

### 12.1 deliveryInput HTML 状态

| 检查项 | 结果 |
|---|---|
| templateUrl | **F**（controller.js 0 处）|
| 7 untracked HTML 中 deliveryInput 相关 | 0 处 |
| 路由表 state → templateUrl | F（资源范围外）|

**F**：
- deliveryInput HTML 模板在当前资源范围**不可得**（F）
- **所有 UI 触发路径** = F 边界

### 12.2 F-UI 不可得的字段含义

| 字段 | Controller 层事实 | UI 介入证据 |
|---|---|---|
| `deliveryCount` | saveStock 0 处写入 | **F 边界**（HTML 不可得）|
| `stockInSkuId` | saveStock 0 处写入 | **F 边界** |
| `machineCenterId` | selectOrder 0 处写入 | **F 边界** |
| `medicalProductId` | saveStock 0 处写入 | **F 边界** |
| `listCount` | 0 处写入 | **F 边界** |
| `planDeliveryTime` | `$scope.startTime` 写入 3 处 | **部分 A**（L3933 searchDate 是 controller 内 datepicker on-change 触发，HTML ng-model 绑定 F）|

**A**：4 字段在 controller 内**0 处 Controller 写入**（A）；UI ng-model 绑定 = F 边界。

### 12.3 "用户输入" 严格边界

**禁止表述**（任务纪律）：
- "用户输入 deliveryCount"
- "用户选择 stockInSkuId"
- "用户选择 machineCenterId"
- "用户选择计划配送日期"
- "用户切换 tab"

**可表述**（A 级）：
- "deliveryCount 字段在 saveStock 内 0 处被 controller 写入"
- "stockInSkuId 字段在 saveStock 内 0 处被 controller 写入"
- "$scope.startTime 由 searchDate / showAddModal 重置 / selectOrder 格式化修改"

---

## 13. F3 → F6 中间对象链路（A 级完整）

```
F3 result.list[i].{ medicalProduct, machineCenter }
        ↓ [A] (L3962 v.medicalProduct.id / v.machineCenter.id)
局部 arr (L3961 map output)
        ↓ [A] (L3962 map callback return)
arr[].{ medicalProductId, machineCenterId }
        ↓ [A] (L3966 JSON.stringify)
F6 Request.medicalProductMachineCenterPoListJson (string)
        +
F6 Request.planDeliveryTime = $scope.startTime (L3966)
        ↓ [A]
F6 saveMedicalProductToMachineCenter.json
```

**A**：F3 → F6 中间对象链 4 步 A 级闭合（A）。

### 13.1 中间字段统计

| 层级 | 字段 | 出现位置 |
|---|---|---|
| L1-API | `medicalProduct.id` | F3 L3962 |
| L1-API | `machineCenter.id` | F3 L3962 |
| L1-Controller (arr) | `medicalProductId` | L3962 |
| L1-Controller (arr) | `machineCenterId` | L3962 |
| L1-Controller ($scope) | `$scope.startTime` | L3933/L3956/L3964/L3966 |
| L1-Request | `medicalProductMachineCenterPoListJson[].medicalProductId` | L3966 |
| L1-Request | `medicalProductMachineCenterPoListJson[].machineCenterId` | L3966 |
| L1-Request | `planDeliveryTime` | L3966 |

**A**：F3 → F6 涉及 8 个字段 A 级记录（A）。

---

## 14. F4 → F5 中间对象链路（A 级完整）

```
F4 result.list[i].{ medicalProduct, deliveryStockInSkuVoList[j].{ stockInSku, deliveryCount } }
        ↓ [A] (L3991/L3998/L4007)
局部 arr (L3981)
        ↓ [A]
arr[i][].{ stockInSkuId, deliveryCount }  (L3991 push)
        ↓ [A] (L3998)
medicalProductStockBatctPoListJson[].{ medicalProductId, medicalProductStocks: arr[i] }  (L3998)
        ↓ [A] (L4007 JSON.stringify)
F5 Request.medicalProductStockBatctPoListJson (string)
        +
F5 Request.listCount = result.list.length (L4007)
        ↓ [A]
F5 saveMedicalProductStockBatch.json
```

**A**：F4 → F5 中间对象链 4 步 A 级闭合（A）。

### 14.1 中间字段统计

| 层级 | 字段 | 出现位置 |
|---|---|---|
| L1-API | `result.list[i].medicalProduct.id` | F4 L3998 |
| L1-API | `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | F4 L3991 |
| L1-API | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | F4 L3989/L3991/L3992 |
| L1-Controller (arr) | `arr[i][]` | L3981/L3987 |
| L1-Controller (arr[i]) | `stockInSkuId` | L3991 |
| L1-Controller (arr[i]) | `deliveryCount` | L3991 |
| L1-Controller (medicalProductStockBatctPoListJson) | `medicalProductId` | L3998 |
| L1-Controller (medicalProductStockBatctPoListJson) | `medicalProductStocks` | L3998 |
| L1-Request | `listCount` | L4007 |
| L1-Request | `medicalProductStockBatctPoListJson[].medicalProductId` | L4007 |
| L1-Request | `medicalProductStockBatctPoListJson[].medicalProductStocks[].stockInSkuId` | L4007 |
| L1-Request | `medicalProductStockBatctPoListJson[].medicalProductStocks[].deliveryCount` | L4007 |

**A**：F4 → F5 涉及 12 个字段 A 级记录（A）。

---

## 15. API 原始 / Controller 中间 / Request 三层分离（A 级）

### 15.1 6 关键字段三层映射

| 字段 | L1-API | L1-Controller | L1-Request |
|---|---|---|---|
| `medicalProductId` (F4) | `result.list[i].medicalProduct.id` (L3998 读取) | ❌ 隐式复制（无中间对象）| `medicalProductStockBatctPoListJson[].medicalProductId` (L4007) |
| `medicalProductId` (F3) | `result.list[i].medicalProduct.id` (L3962 v 读取) | `arr[].medicalProductId` (L3962 map 重命名) | `medicalProductMachineCenterPoListJson[].medicalProductId` (L3966) |
| `stockInSkuId` (F4) | `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` (L3991) | `arr[i][].stockInSkuId` (L3991 push 重命名) | `medicalProductStockBatctPoListJson[].medicalProductStocks[].stockInSkuId` (L4007) |
| `deliveryCount` (F4) | `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` (L3989/L3991/L3992) | `arr[i][].deliveryCount` (L3991 push) | `medicalProductStockBatctPoListJson[].medicalProductStocks[].deliveryCount` (L4007) |
| `listCount` (F4) | `result.list.length` (L4007) | ❌ 无中间对象 | `listCount` (L4007) |
| `machineCenterId` (F3) | `result.list[i].machineCenter.id` (L3962 v 读取) | `arr[].machineCenterId` (L3962 map 重命名) | `medicalProductMachineCenterPoListJson[].machineCenterId` (L3966) |
| `planDeliveryTime` (F6) | ❌ 不存在 F3 API 字段 | `$scope.startTime` (L3966) | `planDeliveryTime` (L3966) |

**A**：7 个字段（含 medicalProductId 跨 2 API）完整三层分离 A 级（A）。

### 15.2 同名 ≠ 同源 原则（A 级）

| 字段名 | F3 出现 | F4 出现 | 是否同源 |
|---|---|---|---|
| `medicalProductId` | ✅ (F3→F6 路径) | ✅ (F4→F5 路径) | **❌ 不同源**（不同 API / 不同 Controller 路径）|
| `deliveryCount` | ❌ | ✅ (F4→F5 路径) | 仅 F4 |
| `stockInSkuId` | ❌ | ✅ (F4→F5 路径) | 仅 F4 |
| `listCount` | ❌ | ✅ (F4→F5 路径) | 仅 F4 |
| `machineCenterId` | ✅ (F3→F6 路径) | ❌ | 仅 F3 |
| `planDeliveryTime` | ❌（不存在）| ❌（不存在）| 仅 F6 ($scope.startTime) |

**A**：字段名仅同名，**不证明同源**（A）。

### 15.3 严格禁止的 Schema 升级

**禁止**（任务纪律）：
- 把 `deliveryCount` 当成"前端必填 UI 字段"
- 把 `stockInSkuId` 当成"用户选择字段"
- 把 `machineCenterId` 当成"用户选择字段"
- 把 `selected` / `checked` / `choose` 假想为 deliveryInputCtrl 的中间状态

**A**：deliveryInputCtrl 内**0 处** `selected` / `checked` / `choose` 状态变量（A）。

---

## 16. Read / Write 边界

| API | Read/Write | 本轮是否调用 | Request 静态可见 | 完整字段闭合 |
|---|---|---|---|---|
| F3 getMedicalProductMachineCenterVoList.json | **Read** | **❌ 0 调用** | ✅ | ✅ 2 字段（medicalProductId + machineCenterId）|
| F4 getCanBeDeliverySkuInListOfProduct.json | **Read** | **❌ 0 调用** | ✅ | ✅ 4 字段（medicalProductId + stockInSkuId + deliveryCount + listCount）|
| F5 saveMedicalProductStockBatch.json | **Write** | **❌ 0 调用** | ✅ | ✅ 4 字段完全闭合（S1-90 已确认）|
| F6 sendMedicalProductToMachineCenter.json | **Write** | **❌ 0 调用** | ✅ | ✅ 3 字段完全闭合（S1-91 已确认）|

**A**：
- F3/F4 Read API **0 调用**（A）
- F5/F6 Write API **0 调用**（A）
- 本轮**0 处任何 API 调用**（A）

---

## 17. 26 项审计矩阵

| # | 审计项 | 等级 | 证据 |
|---|---|---|---|
| 01 | F3 result.list 字段全集 | A（4 字段）+ F（完整结构）| L3961/L3962 |
| 02 | F3 v 来源 | A | result.list[i] (L3961 map callback) |
| 03 | F3 medicalProduct | A | v.medicalProduct.id (L3962) |
| 04 | F3 machineCenter | A | v.machineCenter.id (L3962) |
| 05 | F3 result.list 是否被修改 | A（0 处）| saveStock/selectOrder 0 处写入 |
| 06 | selectOrder() | A | L3955-3977（23 行）|
| 07 | selectOrder map | A | L3961-3963（2 字段输出）|
| 08 | selectOrder 中间对象 | A | arr 局部变量（L3961）|
| 09 | medicalProductId 状态性质 | A | API 原始 + Controller 重命名 |
| 10 | machineCenterId 状态性质 | A | API 原始 + Controller 重命名 |
| 11 | F4 result.list 字段全集 | A（9 处访问）| L3985-3998 |
| 12 | F4 deliveryStockInSkuVoList | A | L3988 |
| 13 | F4 stockInSku | A | stockInSku.id (L3991) |
| 14 | F4 deliveryCount 原始来源 | A | L3989/L3991/L3992 |
| 15 | F4 result.list 是否被修改 | A（0 处）| saveStock 0 处写入 |
| 16 | saveStock() 定位 | A | L3979-4020（41 行）|
| 17 | F4 中间对象 | A | arr / arr[i] / medicalProductStockBatctPoListJson |
| 18 | stockInSkuId 状态性质 | A | API 原始 + Controller 重命名 |
| 19 | deliveryCount 状态性质 | A | API 原始（saveStock 0 处写入）|
| 20 | listCount 状态性质 | A | API 派生（length）|
| 21 | 前端 selected/checked 等临时状态 | A（0 处）+ F（HTML 不可得）| 全仓 0 处 |
| 22 | stockDetail 生命周期 | A | L3882 (true) / L4017 (false) |
| 23 | addOrderModal 生命周期 | A | L3831 (true) / L3953 (false) / L3973 (false) |
| 24 | F3→F6 中间字段 | A | 4 步完全闭合 |
| 25 | F4→F5 中间字段 | A | 4 步完全闭合 |
| 26 | API原始/Controller/Request 三层结论 | A | 7 字段完整三层映射 |

### 17.1 A / B / C / D / E / F 统计

| 等级 | 数量 | 占比 |
|---|---|---|
| A | **25** | 96.2% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | **1** | 3.8%（仅 UI 触发路径 / 完整字段）|

**A**：26 项中 25 项 A + 1 项 F（**仅 UI 触发路径**）。

---

## 18. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | 6 字段三层映射 / F3/F4 result 字段消费 / saveStock + selectOrder 中间对象 / stockDetail + addOrderModal 完整生命周期 | **是** |
| L2 业务规则 | "配送数量" / "SKU 选择" / "加工中心选择" 业务语义 | **E**（按 API 名称推测，无 L3 证据）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository | **F**（资源范围外）|

**禁止表述**：
- "deliveryCount = 配送数量业务字段"
- "stockInSkuId = SKU 入库主键"
- "machineCenterId = 加工中心主键"
- "planDeliveryTime = 计划配送时间"

---

## 19. F 边界清单

| F 项 | 原因 |
|---|---|
| deliveryInput HTML 模板 | working dir + tracked 0 个对应 |
| 6 字段 UI ng-model 绑定 | HTML 不可得 |
| 业务实体语义（产品/SKU/加工中心/订单）| L3 = F（资源范围外）|
| F3/F4/F5/F6 后端 Response 完整字段 | 资源范围外 |
| ObjectFactory 内部 HTTP 实现 | 资源范围外 |
| 路由表 state → templateUrl | 资源范围外 |
| deliveryCount 业务语义 | 资源范围外 |
| planDeliveryTime 后端期望类型 | 资源范围外 |
| 业务上 "用户输入" / "用户选择" 行为 | HTML 不可得 = F |
| F3/F4 result.list 完整字段结构 | 资源范围外（仅已观察 4 字段 / 4 字段）|

---

## 20. 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 write API 调用 | ❌（**F5/F6 绝对未调用**）|
| R3 修改历史 MD | ❌ |
| R4 删除 10 untracked | ❌（**deliveryList.html hash 复核不变**）|
| R5 P0/P1 自动新增 | ❌ |
| R6 git add . / -A / * | ❌ |
| R7 修改 controller.js / 7 HTML | ❌（全部只读）|
| R8 文件编号冲突 | ❌（152 已被 S1-91 占用，本轮 153）|

---

## 21. 最终结论

### 21.1 一句话总结

**F3/F4 Response → Controller 中间对象 → F5/F6 Request 字段 3 层完全 A 级分离；4 字段状态性质 = 100% 纯 API 原始（saveStock/selectOrder 0 处 Controller 写入）；stockDetail + addOrderModal 完整生命周期 A 级确认；0 处 selected/checked/choose 假想中间状态；UI 触发路径 = F 边界。**

### 21.2 关键事实

1. **3 层字段分离 A 级**：L1-API / L1-Controller / L1-Request（A）
2. **6 字段状态性质 100% API 原始**：4 字段（medicalProductId / machineCenterId / stockInSkuId / deliveryCount）+ listCount（A）
3. **planDeliveryTime 唯一非 API 字段**：来源 = $scope.startTime（A）
4. **F3/F4 result.list 0 处被 controller 修改**（全部 push 创建新对象，A）
5. **saveStock 0 处修改 deliveryCount**（controller 纯读，A）
6. **selectOrder 0 处修改 machineCenterId**（map 创建新对象，A）
7. **stockDetail 仅 2 处**（L3882 true / L4017 false，A）
8. **addOrderModal 仅 3 处**（L3831/L3953/L3973，A）
9. **0 处 selected/checked/current/active/choose/disabled/medicalRecordId** 在 deliveryInputCtrl（A）
10. **medicalProductStockListJson 残留代码**（L3984 声明但未使用，D 缺陷）

### 21.3 26 项 A-F 分布

- **A：25**（96.2%）
- **F：1**（3.8% — 仅 UI 触发路径）
- **E 升 A / F 升 A：0**

### 21.4 与 S1-90/S1-91 一致性

- ✅ S1-90 的 F4→F5 4 字段闭合（medicalProductId / stockInSkuId / deliveryCount / listCount）本轮**再次 A 级复核**（行号一致）
- ✅ S1-91 的 F3→F6 3 字段闭合（medicalProductId / machineCenterId / planDeliveryTime）本轮**再次 A 级复核**（行号一致）
- **新增 S1-92 价值**：
  - 4 字段状态性质严格分层（API 原始 / Controller / Request / UI）
  - **deliveryCount 0 处 controller 写入** = A 级关键证据（即使 HTML 不可得也能确定 controller 不修改）
  - stockDetail + addOrderModal 完整生命周期（写入点、关闭路径、UI 介入 = F）
  - 0 处 selected/checked 中间状态确认（避免任务列出的"假想中间变量"误判）
  - 同名 ≠ 同源原则严格执行（medicalProductId 在 F3/F4 中不同源）

### 21.5 严格红线维持

- ✅ Write = 0（**F5/F6 绝对未调用**）
- ✅ 生产数据修改 = 0
- ✅ 历史 MD 修改 = 0
- ✅ controller.js 未修改
- ✅ deliveryList.html hash 不变
- ✅ 10 个 untracked 临时文件原样保留
- ✅ P0 = 54 / P1 = 8 冻结

---

## 22. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| Write 操作 = 0 | ✅（**F5/F6 0 调用**）|
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| **deliveryList.html hash/bytes 未改变** | ✅（SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476` / 12720 bytes）|
| Git 禁止命令未触发 | ✅（仅 `git add -- 153_*.md`）|
| 文件编号冲突 | ✅（152 已占用 → 本轮 153）|

---

## 23. 停止条件

✅ F3/F4 result.list 字段全集 A 级
✅ 4 字段状态性质 100% API 原始（controller 0 写入）A 级
✅ F3 result.list 0 处 controller 修改 A 级
✅ F4 result.list 0 处 controller 修改 A 级
✅ stockDetail 完整生命周期 A 级（L3882/L4017）
✅ addOrderModal 完整生命周期 A 级（L3831/L3953/L3973）
✅ 0 处 selected/checked 中间状态 A 级
✅ 7 字段三层完整映射 A 级
✅ F3→F6 / F4→F5 中间对象链路 A 级
✅ medicalProductStockListJson 残留代码 D 缺陷发现
✅ 25 A + 1 F（仅 UI 触发路径）
✅ 10 项 F 边界明确列出
✅ deliveryList.html hash 复核不变
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-93）**。
