# S1-104 optometryCtrl 取消订单 / 制作完成 两 Write 动作闭合审计

> **任务名**：S1-104｜optometryCtrl "取消订单" / "制作完成" 两个 Write 动作入口与 Request→Success→Read 闭合审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）clickBtn fnMap 中"取消订单"和"制作完成"两个 action
> **当前轮次**：S1-104（接 S1-103 完成）
> **本轮承诺**：2 个 Write API + 2 个 Read API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| cancelMedicalRecord.json (L35150) | ✅ | 取消订单 Write |
| confirmMedicalRecordReturn.json (L35167) | ✅ | 制作完成 Write |
| fnMap "取消订单" (L35147-L35160) | ✅ | 入口 |
| fnMap "制作完成" (L35164-L35176) | ✅ | 入口 |
| $scope.hint (L35010-L35030) | ✅ | 弹窗实现（S1-99 已读） |
| item.medicalRecord.id 来源 | ✅ | clickBtn 形参 |
| querySingleOrder / queryUndisposed | ⚠️ 旁证 | S1-100 已审 |
| 7 HTML | ❌（不可得）| UI 触发点 F |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 合理业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "取消订单 = 取消医疗记录"：**E**（仅命名 + 1 个 L35016 注释"确定要取消此订单吗"）
- "制作完成 = 完成加工/制作"：**E**（仅命名 + 1 个 L35018 注释"确认是否已经制作完成"）
- "cancelMedicalRecord = 删除数据库记录"：**E**（未证）
- "confirmMedicalRecordReturn = 确认回库"：**E**（未证）
- 自动加 orderId / cashflowId / status / remark 等字段：**D**（禁止升级）

---

## 3. 取消订单入口

### 3.1 完整源码（A 级，L35147-L35160）

```javascript
取消订单: function _() {                                                          // L35147
    $scope.hint(1, function () {                                                   // L35148
        var medicalRecordId = item.medicalRecord.id;                                // L35149
        new ObjectFactory().saveOrQuery("/admin/cancelMedicalRecord.json", {        // L35150
            medicalRecordId: medicalRecordId                                          // L35151
        }).then(function (result) {
            if (result.status) {                                                     // L35153
                return Popup.notice(result.errmsg);                                  // L35154
            }
            $scope.querySingleOrder();                                                // L35156
            $scope.queryUndisposed();                                                 // L35157
        });
    });
}
```

### 3.2 入口链（A 级）

```
HTML ng-click (F 边界)
    ↓
fnMap["取消订单"]() (L35147)  ← clickBtn 内 fnMap 字典查找
    ↓
$scope.hint(1, fn) (L35148)  ← window.popout_tip 弹窗 (index=1 → "确定要取消此订单吗？")
    ↓ res truthy
fn (L35149-L35158) 内联回调
    ↓
Write /admin/cancelMedicalRecord.json (L35150)
    ↓ [F 边界: HTTP + 后端]
result
    ↓ if (result.status) return Popup
    ↓
$scope.querySingleOrder() (L35156)
$scope.queryUndisposed() (L35157)
```

### 3.3 关键事实（A 级）
- fnMap["取消订单"] 是 **clickBtn 内 fnMap 字典**的 1 个 key（L35147）
- ❌ 0 处 if/else/switch 分支
- ❌ 0 处 fnMap 外部调用
- ❌ 0 处 HTML 端 ng-click 证据（HTML 不可得）
- ❌ 0 处 闭包外的 cancelMedicalRecord 调用
- $scope.hint(1, fn) 中 index=1 的语义：**$scope.hint 内的 contentInfo 字典**（L35015-L35018）映射到"确定要取消此订单吗？"

---

## 4. 取消订单 Write

### 4.1 API 字符串（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| API 字符串 | `/admin/cancelMedicalRecord.json` | A |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式） | A 引用 / F 实际 |
| Factory | 匿名 `new ObjectFactory()` | A |
| Factory 实例 | 独立实例 | A |
| 全 controller.js 调用 | **1 处唯一**（L35150） | A |
| 7 HTML 调用 | ❌ 0 处 | A |

### 4.2 完整 Request 字段（A 级）

```javascript
{
    medicalRecordId: medicalRecordId
}
```

| 字段 | 表达式 | 来源 | 行号 | A-F |
|---|---|---|---|---|
| `medicalRecordId` | `medicalRecordId` | `var medicalRecordId = item.medicalRecord.id` (L35149) | L35149 / L35151 | A |

**A 级结论**：
- Request 字段 = **1 个**（medicalRecordId）
- ❌ 0 处其它字段（orderId / cashflowId / status / remark / reason 全部**不进入**）
- ❌ 0 处类型转换
- ❌ 0 处默认值

### 4.3 medicalRecordId 来源链（A 级）

```
clickBtn(name, item, index) (L35128)
    ↓
item = clickBtn 形参（来自 HTML ng-click "clickBtn(name, item, index)"）
    ↓
fnMap["取消订单"]() (L35147)
    ↓
item.medicalRecord.id (L35149)
    ↓
medicalRecordId 局部变量
    ↓ L35151
Request.medicalRecordId
```

**A 级结论**：
- medicalRecordId 字段值 = `item.medicalRecord.id`（**A 级**）
- item 来自 clickBtn 形参，**A 级**
- item.medicalRecord.id **与 selectOrderListFactory.items[index].medicalRecord.id 同源**（A 级 — 表达式层同源；值层 F）

### 4.4 完整 Request 字段级闭合（A 级）

| 入口参数 | 中间变量 | Request 字段 | A-F |
|---|---|---|---|
| `item` (clickBtn 形参) | `item.medicalRecord.id` (L35149) | `medicalRecordId` (L35151) | A |

---

## 5. 取消订单 medicalRecordId 来源精确追踪

### 5.1 item 来源（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| item 类型 | clickBtn 形参 | A |
| item 实际值 | HTML ng-click 传入 `$scope.selectOrderListFactory.items[index]` | A（参数） / F（HTML 不可得） |
| item.medicalRecord.id 来源链 | selectOrderListFactory.items[index].medicalRecord.id | A（表达式层） |

### 5.2 关键事实（A 级）
- medicalRecordId 字段路径 = `item.medicalRecord.id`（A 级）
- ❌ **不是** `medicalProduct.medicalRecordId`（modal.affrim 路径不同）
- ❌ **不是** `order.object...`（brushData 路径不同）
- 严格表述：**取消订单的 medicalRecordId 字段路径 = selectOrderListFactory.items[index].medicalRecord.id**（A 级）

---

## 6. 取消订单前置 / 弹窗

### 6.1 前置 Read 检查（A 级）

| API | 触发 | A-F |
|---|---|---|
| querySingleOrder | ❌ 不在 Write 前调 | A |
| queryUndisposed | ❌ 不在 Write 前调 | A |
| getMedicalRecordFlowVo | ❌ 不在 Write 前调 | A |
| F1 / F3 / F4 | ❌ 不在 Write 前调 | A |
| 报损链 selectMedicalProductStockList | ❌ 不在 Write 前调 | A |

**A 级结论**：取消订单**直接调 Write**，**0 处前置 Read**。

### 6.2 弹窗 / confirm / Popup（A 级）

| 操作 | 行号 | 行为 | A-F |
|---|---|---|---|
| `$scope.hint(1, fn)` | L35148 | window.popout_tip 弹窗（index=1 → "确定要取消此订单吗？"） | A |
| 弹窗取消 | L35027 `res && fn()` 短路 | 用户取消 → fn 不调 → Write 不执行 | A |
| 弹窗确认 | L35028 `res && fn()` 调 fn | 用户确认 → fn 执行 → Write 执行 | A |
| Popup 错误处理 | L35154 `Popup.notice(result.errmsg)` | 错误时弹窗 | A |
| alert / native confirm | ❌ 0 处 | — | A |

### 6.3 A 级结论
- 取消订单前有 **1 个 popout_tip 弹窗**（$scope.hint）
- 弹窗取消 → 流程终止
- 弹窗确认 → 进入 Write
- ❌ 0 处原生 confirm / alert
- ❌ 0 处前置 Read

---

## 7. 取消订单 success

### 7.1 success 完整源码（A 级，L35152-L35158）

```javascript
.then(function (result) {
    if (result.status) {                          // L35153
        return Popup.notice(result.errmsg);        // L35154
    }
    $scope.querySingleOrder();                    // L35156
    $scope.queryUndisposed();                     // L35157
});
```

### 7.2 success 行为精确分层（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L35153 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | L35156 | `$scope.querySingleOrder()` （无参数） | A |
| 3 | L35157 | `$scope.queryUndisposed()` （无参数） | A |
| 4 | — | ❌ **0 处** Popup.notice("取消成功") | A |
| 5 | — | ❌ 0 处 $state.reload() | A |
| 6 | — | ❌ 0 处 $state.go() | A |
| 7 | — | ❌ 0 处 modal 关闭 | A |
| 8 | — | ❌ 0 处 scope flag 复位 | A |

### 7.3 success 后 Read 链（A 级）

```
Write success
    ↓
$scope.querySingleOrder()  // L35156
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界: HTTP + 后端]
    ↓
$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object
$scope.medicalRecordStatus[$scope.orderIndex] = window.filter_medicalRecordStatus(result.object, "button")

$scope.queryUndisposed()  // L35157
    ↓ saveOrQuery (Read: stateTodoMedicalRecordCount.json)
    ↓ [F 边界: HTTP + 后端]
    ↓
$scope.toPayCount = result.result.object
```

### 7.4 关键事实（A 级）
- 取消订单 success **调 querySingleOrder + queryUndisposed**（2 个 Read）
- ❌ 0 处 success Popup（无"取消成功"提示）
- querySingleOrder 和 queryUndisposed 都是**同步调用**（不等待对方完成）
- ❌ 0 处 .catch 保护
- 错误处理仅 Popup + return

---

## 8. 制作完成入口

### 8.1 完整源码（A 级，L35164-L35176）

```javascript
制作完成: function _() {                                                          // L35164
    $scope.hint(3, function () {                                                   // L35165
        var medicalRecordId = item.medicalRecord.id;                                // L35166
        new ObjectFactory().saveOrQuery("/admin/confirmMedicalRecordReturn.json", { // L35167
            medicalRecordId: medicalRecordId                                          // L35168
        }).then(function (result) {
            if (result.status) {                                                     // L35170
                return Popup.notice(result.errmsg);                                  // L35171
            }
            $scope.querySingleOrder();                                                // L35173
        });
    });
}
```

### 8.2 入口链（A 级）

```
HTML ng-click (F 边界)
    ↓
fnMap["制作完成"]() (L35164)  ← clickBtn 内 fnMap 字典查找
    ↓
$scope.hint(3, fn) (L35165)  ← window.popout_tip 弹窗 (index=3 → "确认是否已经制作完成？")
    ↓ res truthy
fn (L35166-L35174) 内联回调
    ↓
Write /admin/confirmMedicalRecordReturn.json (L35167)
    ↓ [F 边界: HTTP + 后端]
result
    ↓ if (result.status) return Popup
    ↓
$scope.querySingleOrder() (L35173)
（不调 queryUndisposed）
```

### 8.3 关键事实（A 级）
- fnMap["制作完成"] 是 **clickBtn 内 fnMap 字典**的 1 个 key（L35164）
- ❌ 0 处 if/else/switch 分支
- ❌ 0 处 fnMap 外部调用
- $scope.hint(3, fn) 中 index=3 的语义：**$scope.hint 内的 contentInfo 字典**（L35015-L35018）映射到"确认是否已经制作完成？"

---

## 9. 制作完成 Write

### 9.1 API 字符串（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| API 字符串 | `/admin/confirmMedicalRecordReturn.json` | A |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式） | A 引用 / F 实际 |
| Factory | 匿名 `new ObjectFactory()` | A |
| Factory 实例 | 独立实例 | A |
| 全 controller.js 调用 | **1 处唯一**（L35167） | A |
| 7 HTML 调用 | ❌ 0 处 | A |

### 9.2 完整 Request 字段（A 级）

```javascript
{
    medicalRecordId: medicalRecordId
}
```

| 字段 | 表达式 | 来源 | 行号 | A-F |
|---|---|---|---|---|
| `medicalRecordId` | `medicalRecordId` | `var medicalRecordId = item.medicalRecord.id` (L35166) | L35166 / L35168 | A |

**A 级结论**：
- Request 字段 = **1 个**（medicalRecordId）
- ❌ 0 处其它字段（orderId / cashflowId / status / remark / completeStatus 全部**不进入**）
- ❌ 0 处类型转换
- ❌ 0 处默认值

### 9.3 medicalRecordId 来源链（A 级）

```
clickBtn(name, item, index) (L35128)
    ↓
item = clickBtn 形参
    ↓
fnMap["制作完成"]() (L35164)
    ↓
item.medicalRecord.id (L35166)
    ↓
medicalRecordId 局部变量
    ↓ L35168
Request.medicalRecordId
```

**A 级结论**：
- medicalRecordId 字段值 = `item.medicalRecord.id`（**A 级**）
- ❌ **不是** `medicalProduct.medicalRecordId`
- ❌ **不是** `order.object...`
- 严格表述：**制作完成的 medicalRecordId 字段路径 = selectOrderListFactory.items[index].medicalRecord.id**（A 级，与取消订单**完全同源**）

---

## 10. 制作完成 medicalRecordId 来源精确追踪

### 10.1 item 来源（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| item 类型 | clickBtn 形参 | A |
| item 实际值 | HTML ng-click 传入 `$scope.selectOrderListFactory.items[index]` | A（参数） / F（HTML 不可得） |

### 10.2 关键事实（A 级）
- medicalRecordId 字段路径 = `item.medicalRecord.id`（A 级）
- ❌ 不是 `medicalProduct.medicalRecordId`
- ❌ 不是 `order.object...`
- 严格表述：**制作完成的 medicalRecordId 字段路径与取消订单完全相同**（A 级）

---

## 11. 制作完成前置 / 弹窗

### 11.1 前置 Read 检查（A 级）

| API | 触发 | A-F |
|---|---|---|
| querySingleOrder | ❌ 不在 Write 前调 | A |
| queryUndisposed | ❌ 不在 Write 前调 | A |
| getMedicalRecordFlowVo | ❌ 不在 Write 前调 | A |
| F1 / F3 / F4 | ❌ 不在 Write 前调 | A |
| 报损链 selectMedicalProductStockList | ❌ 不在 Write 前调 | A |

**A 级结论**：制作完成**直接调 Write**，**0 处前置 Read**。

### 11.2 弹窗 / confirm / Popup（A 级）

| 操作 | 行号 | 行为 | A-F |
|---|---|---|---|
| `$scope.hint(3, fn)` | L35165 | window.popout_tip 弹窗（index=3 → "确认是否已经制作完成？"） | A |
| 弹窗取消 | L35027 `res && fn()` 短路 | 用户取消 → fn 不调 → Write 不执行 | A |
| 弹窗确认 | L35028 `res && fn()` 调 fn | 用户确认 → fn 执行 → Write 执行 | A |
| Popup 错误处理 | L35171 `Popup.notice(result.errmsg)` | 错误时弹窗 | A |
| alert / native confirm | ❌ 0 处 | — | A |

---

## 12. 制作完成 success

### 12.1 success 完整源码（A 级，L35169-L35174）

```javascript
.then(function (result) {
    if (result.status) {                          // L35170
        return Popup.notice(result.errmsg);        // L35171
    }
    $scope.querySingleOrder();                    // L35173
});
```

### 12.2 success 行为精确分层（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L35170 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | L35173 | `$scope.querySingleOrder()` （无参数） | A |
| 3 | — | ❌ **不调** `$scope.queryUndisposed()` | A |
| 4 | — | ❌ 0 处 Popup.notice("制作成功") | A |
| 5 | — | ❌ 0 处 $state.reload() | A |
| 6 | — | ❌ 0 处 $state.go() | A |
| 7 | — | ❌ 0 处 modal 关闭 | A |
| 8 | — | ❌ 0 处 scope flag 复位 | A |

### 12.3 success 后 Read 链（A 级）

```
Write success
    ↓
$scope.querySingleOrder()  // L35173
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界]
    ↓
$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object
$scope.medicalRecordStatus[$scope.orderIndex] = window.filter_medicalRecordStatus(...)
（不调 queryUndisposed）
```

### 12.4 关键事实（A 级）
- 制作完成 success **只调 querySingleOrder**（1 个 Read）
- ❌ **不调** queryUndisposed
- ❌ 0 处 success Popup
- querySingleOrder 同步调用
- ❌ 0 处 .catch 保护

---

## 13. 两动作 Request 对照（A 级）

### 13.1 完整字段对照表（A 级）

| 字段 | 取消订单 (L35147-L35160) | 制作完成 (L35164-L35176) | 是否相同 |
|---|---|---|---|
| **API 字符串** | `/admin/cancelMedicalRecord.json` (L35150) | `/admin/confirmMedicalRecordReturn.json` (L35167) | ❌ **不同** |
| **Factory 模式** | 匿名 `new ObjectFactory()` | 匿名 `new ObjectFactory()` | ✅ 相同 |
| **Request 字段** | `{ medicalRecordId }` | `{ medicalRecordId }` | ✅ **完全相同** |
| `medicalRecordId` 来源 | `item.medicalRecord.id` (L35149) | `item.medicalRecord.id` (L35166) | ✅ 相同 |
| **弹窗 index** | 1 (L35148) | 3 (L35165) | ❌ **不同** |
| **success 错误处理** | if (result.status) return Popup | if (result.status) return Popup | ✅ 相同 |
| **success Popup** | ❌ 无 | ❌ 无 | ✅ 相同 |
| **success querySingleOrder** | ✅ L35156 | ✅ L35173 | ✅ 相同 |
| **success queryUndisposed** | ✅ L35157 | ❌ **不调** | ❌ **不同** |
| **前置 Read** | ❌ 无 | ❌ 无 | ✅ 相同 |
| **concatMedicalProductStock 调用** | ❌ 无 | ❌ 无 | ✅ 相同 |
| **JSON.stringify** | ❌ 无 | ❌ 无 | ✅ 相同 |
| **类型转换** | ❌ 无 | ❌ 无 | ✅ 相同 |
| **默认值** | ❌ 无 | ❌ 无 | ✅ 相同 |

### 13.2 严格表述（A 级）
- "两动作 Request 字段**完全相同**（仅 `{ medicalRecordId }`）"：**A**
- "两动作 medicalRecordId 来源**完全相同**（`item.medicalRecord.id`）"：**A**
- "两动作 Factory 模式**完全相同**（匿名 `new ObjectFactory()`）"：**A**
- "两动作 success 错误处理**完全相同**（if (result.status) return Popup）"：**A**
- "两动作 API 字符串**不同**"：**A**
- "两动作 success 是否调 queryUndisposed **不同**（取消调，制作不调）"：**A**
- "两动作弹窗 index **不同**（1 vs 3）"：**A**

### 13.3 结构对称性（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 函数结构 | 完全对称（5 行核心） | A |
| 弹窗模式 | 完全对称（$scope.hint） | A |
| Request 结构 | 完全对称（1 字段） | A |
| 错误处理 | 完全对称 | A |
| querySingleOrder 调用 | 完全对称 | A |
| **API 字符串** | **不同** | A |
| **queryUndisposed 调用** | **不同** | A |
| **弹窗 index** | **不同** | A |

**A 级结论**：两动作结构**高度对称**，唯一 3 处差异 = API 字符串 / 弹窗 index / success 是否调 queryUndisposed。

---

## 14. F4 / F3 / 报损 边界（A 级）

### 14.1 取消订单与 F1/F3/F4/F5/F6 连接（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| 调 F4 (getCanBeDeliverySkuInListOfProduct) | ❌ 0 处 | A |
| 调 F3 (getMedicalProductMachineCenterVoList) | ❌ 0 处 | A |
| 调 F1 (getCashflowDeliveryVo) | ❌ 0 处 | A |
| 调 F5 (saveMedicalProductStockBatch) | ❌ 0 处 | A |
| 调 F6 (sendMedicalProductToMachineCenter) | ❌ 0 处 | A |
| concatMedicalProductStock 调用 | ❌ 0 处 | A |
| medicalProductStockBatctPoListJson 字段路径 | ❌ 0 处 | A |

**A 级结论**：
- 取消订单**与 F1/F3/F4/F5/F6 链路 0 处直接代码连接**
- ❌ 0 处共享中间对象
- 严格表述：**取消订单是与 Delivery 链路完全独立的 Write 路径**（A 级）

### 14.2 制作完成与 F1/F3/F4/F5/F6 连接（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| 调 F4 (getCanBeDeliverySkuInListOfProduct) | ❌ 0 处 | A |
| 调 F3 / F1 / F5 / F6 | ❌ 0 处 | A |
| concatMedicalProductStock 调用 | ❌ 0 处 | A |
| medicalProductStockBatctPoListJson 字段路径 | ❌ 0 处 | A |

**A 级结论**：
- 制作完成**与 F1/F3/F4/F5/F6 链路 0 处直接代码连接**
- 严格表述：**制作完成是与 Delivery 链路完全独立的 Write 路径**（A 级）

### 14.3 报损链连接（A 级）

| 检查 | 取消订单 | 制作完成 |
|---|---|---|
| 调 selectMedicalProductStockList | ❌ 0 处 | ❌ 0 处 |
| 调 createMedicalStockLossOfSmallVersion | ❌ 0 处 | ❌ 0 处 |
| 调 getAdminInfo | ❌ 0 处 | ❌ 0 处 |
| 调 order.brushData | ❌ 0 处 | ❌ 0 处 |
| 调 modal.affrim | ❌ 0 处 | ❌ 0 处 |
| 调 modal.changeOrder | ❌ 0 处 | ❌ 0 处 |
| $scope.modal.shopInfo 访问 | ❌ 0 处 | ❌ 0 处 |

**A 级结论**：
- 两动作**与报损链路 0 处直接代码连接**
- 严格表述：**取消订单 + 制作完成 是与报损链完全独立的 Write 路径**（A 级）

---

## 15. selectOrderListFactory.items 连接（A 级）

### 15.1 取消订单 / 制作完成 与 selectOrderListFactory 关系（A 级）

| 检查 | 取消订单 | 制作完成 |
|---|---|---|
| Request 字段值直接来自 selectOrderListFactory.items[index] | ✅ item.medicalRecord.id | ✅ item.medicalRecord.id |
| Request 字段值回写 selectOrderListFactory.items[index] | ❌ 0 处 | ❌ 0 处 |
| success 后调 querySingleOrder 更新 selectOrderListFactory.items[index] | ✅ L35156 | ✅ L35173 |

**A 级结论**：
- 两动作 Request 字段**表达式层同源**于 selectOrderListFactory.items[index]（A 级）
- 两动作 success 都触发 querySingleOrder → 整体覆盖 selectOrderListFactory.items[orderIndex]（A 级）
- 严格表述：**两动作与 selectOrderListFactory.items 形成 Request→Response 闭环**（A 级）

### 15.2 闭环路径（A 级）

```
fnMap["取消订单"/"制作完成"]() (L35147/L35164)
    ↓
item.medicalRecord.id  ←  $scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id (A 级表达式层同源)
    ↓
Write cancelMedicalRecord / confirmMedicalRecordReturn
    ↓ [F 边界: HTTP + 后端]
result
    ↓
$scope.querySingleOrder() (L35156/L35173)
    ↓ saveOrQuery (Read: getMedicalRecordFlowVo.json)
    ↓ [F 边界]
    ↓
$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object  (L34892 整体覆盖)
```

---

## 16. 重复提交防护（A 级）

### 16.1 Controller 层防护检查（A 级）

| 检查项 | 取消订单 | 制作完成 | A-F |
|---|---|---|---|
| disabled 标志 | ❌ 0 处 | ❌ 0 处 | A |
| loading 标志 | ❌ 0 处 | ❌ 0 处 | A |
| submitting / isSubmitting | ❌ 0 处 | ❌ 0 处 | A |
| promise lock（自己挂） | ❌ 0 处 | ❌ 0 处 | A |
| debounce / throttle | ❌ 0 处 | ❌ 0 处 | A |
| $timeout 锁 | ❌ 0 处 | ❌ 0 处 | A |
| recursion | ❌ 0 处 | ❌ 0 处 | A |
| 循环中 saveOrQuery | ❌ 0 处 | ❌ 0 处 | A |
| UI 层 disabled（HTML 不可得） | F | F | F |

**A 级结论**：
- 2 动作都**0 处重复提交防护**（Controller 层）
- UI 层是否防重：**F**（HTML 不可得）
- 服务端幂等性：**F**（无后端代码）

### 16.2 弹窗防重机制（A 级）

| 机制 | 是否存在 | A-F |
|---|---|---|
| popout_tip 弹窗关闭前不可重复触发 | ❌ 0 处显式代码控制 | A |
| 弹窗 callback 互斥 | ❌ 0 处 | A |

**A 级结论**：
- ❌ 当前 Controller 未观察到**明确**的重复提交防护逻辑
- 唯一隐含防重 = popout_tip 弹窗打开期间用户不能再次点同一按钮（**E 业务推断**，非源码事实）
- 严格表述：**当前 Controller 未观察到明确重复提交防护逻辑**（A 级）

---

## 17. 其它 Consumer（A 级）

### 17.1 cancelMedicalRecord.json 全局 Consumer（A 级，已穷举）

| 位置 | Controller | 函数 | A-F |
|---|---|---|---|
| L35150 | optometryCtrl | fnMap["取消订单"] | A |
| ❌ 0 处其它 | — | — | A |

**A 级结论**：cancelMedicalRecord.json 在 controller.js **仅 1 处唯一调用**（optometryCtrl）。

### 17.2 confirmMedicalRecordReturn.json 全局 Consumer（A 级，已穷举）

| 位置 | Controller | 函数 | A-F |
|---|---|---|---|
| L35167 | optometryCtrl | fnMap["制作完成"] | A |
| ❌ 0 处其它 | — | — | A |

**A 级结论**：confirmMedicalRecordReturn.json 在 controller.js **仅 1 处唯一调用**（optometryCtrl）。

### 17.3 7 HTML Consumer（A 级）

- 7 HTML 中**0 处**含 cancelMedicalRecord / confirmMedicalRecordReturn 字符串
- 7 HTML 中**0 处**含 "取消订单" / "制作完成" 文字
- 严格表述：**当前资源范围无 7 HTML Consumer**（F 边界：HTML 不可得）

---

## 18. 动作后数据刷新

### 18.1 取消订单完整链路（A 级）

```
[HTML ng-click] (F 边界)
    ↓
fnMap["取消订单"]() (L35147)
    ↓
$scope.hint(1, fn) (L35148)  ← popout_tip 弹窗
    ↓ res truthy
fn (L35149-L35158)
    ↓
var medicalRecordId = item.medicalRecord.id (L35149)
    ↓
Write /admin/cancelMedicalRecord.json { medicalRecordId } (L35150-L35151)
    ↓ [F 边界: HTTP + 后端]
result
    ↓ if (result.status) return Popup (L35153-L35154)
    ↓
$scope.querySingleOrder() (L35156)  ← 调 Read getMedicalRecordFlowVo.json
    ↓
$scope.selectOrderListFactory.items[orderIndex] = result.object
$scope.medicalRecordStatus[orderIndex] = window.filter_medicalRecordStatus(result.object, "button")

$scope.queryUndisposed() (L35157)  ← 调 Read stateTodoMedicalRecordCount.json
    ↓
$scope.toPayCount = result.result.object
```

### 18.2 制作完成完整链路（A 级）

```
[HTML ng-click] (F 边界)
    ↓
fnMap["制作完成"]() (L35164)
    ↓
$scope.hint(3, fn) (L35165)  ← popout_tip 弹窗
    ↓ res truthy
fn (L35166-L35174)
    ↓
var medicalRecordId = item.medicalRecord.id (L35166)
    ↓
Write /admin/confirmMedicalRecordReturn.json { medicalRecordId } (L35167-L35168)
    ↓ [F 边界: HTTP + 后端]
result
    ↓ if (result.status) return Popup (L35170-L35171)
    ↓
$scope.querySingleOrder() (L35173)  ← 调 Read getMedicalRecordFlowVo.json
    ↓
$scope.selectOrderListFactory.items[orderIndex] = result.object
$scope.medicalRecordStatus[orderIndex] = window.filter_medicalRecordStatus(result.object, "button")

（不调 queryUndisposed）
```

### 18.3 严格表述（A 级）
- "取消订单 success → querySingleOrder + queryUndisposed"：**A**
- "制作完成 success → querySingleOrder"：**A**
- "两动作 success 都直接刷新 selectOrderListFactory.items[index]"：**A**
- "两动作 success 不调 $state.reload() / state.go / 弹窗关闭"：**A**

---

## 19. optometryCtrl 动作地图（S1-104 更新版）

### 19.1 optometryCtrl 已直接确认的 Write API（A 级，已穷举）

| # | Write API 字符串 | 入口函数 | 行号 | 触发动作 | Request 字段 | A-F |
|---|---|---|---|---|---|---|
| 1 | `/admin/setMedicalRecordProcessMode.json` | choseFactoryMethod → fnMap["加工"] | L35099 | 选加工方式 | { medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson } | A |
| 2 | `/admin/completeMedicalRecordDelivery.json` (deliveryStatus="2") | clickBtn "到店取镜" | L35185 | 完成到店取镜 | { medicalRecordId, deliveryStatus: "2", deliveryNo: undefined, medicalProductStockBatctPoListJson } | A |
| 3 | `/admin/completeMedicalRecordDelivery.json` (deliveryStatus="1") | clickBtn "快递发货" | L35204 | 完成快递发货 | { medicalRecordId, deliveryStatus: "1", deliveryNo: deliveryNo, medicalProductStockBatctPoListJson } | A |
| 4 | `/admin/createMedicalStockLossOfSmallVersion.json` | modal.affrim (clickBtn "报损" → order.show → brushData → modal.changeOrder → modal.affrim) | L35342 | 报损 | { medicalRecordId, machineCenterId, lossAdminId, medicalStockLossSkuListJson } | A |
| 5 | **`/admin/cancelMedicalRecord.json`** | **fnMap["取消订单"]** | **L35150** | **取消订单** | **{ medicalRecordId }** | **A** |
| 6 | **`/admin/confirmMedicalRecordReturn.json`** | **fnMap["制作完成"]** | **L35167** | **制作完成** | **{ medicalRecordId }** | **A** |

**A 级结论**：
- optometryCtrl 范围内**共 6 个 Write API 真实调用**（6 个独立 API 字符串）
- 6 个 Write 都**仅 1 处调用**
- 6 个 Write 都由**clickBtn fnMap** 或 **choseFactoryMethod** 触发
- ❌ 0 处 HTML 端 ng-click 直接证据

### 19.2 optometryCtrl 间接触发的 Write API（A 级）

- 通过 `modal.affrim` 触发的 `/admin/createMedicalStockLossOfSmallVersion.json`（**已计入 #4**）

### 19.3 optometryCtrl 全部 Read API（A 级，已穷举）

| # | Read API 字符串 | 行号 | 触发 | A-F |
|---|---|---|---|---|
| 1 | `/admin/getCompanyOfMine.json` | L34785 | L34792 queryCompanyName() init | A |
| 2 | `/admin/getLoginEmployee.json` | L34795 | L34799 getEmployee() init | A |
| 3 | `/admin/getMedicalRecordFlowVo.json` | L34862 | order.brushData() | A |
| 4 | `/admin/getMedicalRecordFlowVo.json` | L34885 | querySingleOrder() | A |
| 5 | `/admin/getAdminInfo.json` | L35281 | modal.changeOrder() | A |
| 6 | `/admin/selectMedicalRecordFlowVoList.json` | L35367 | ListFactory init | A |
| 7 | `/admin/selectMedicalProductStockList.json` | L35319 | modal.affrim() | A |
| 8 | `/admin/stateTodoMedicalRecordCount.json` | L34843 | queryUndisposed() | A |
| 9 | `/admin/getCashflowDeliveryVo.json` | L34862 (另一处 brushData) | ❌ 不在 optometryCtrl | A |
| 10 | `/admin/getCanBeDeliverySkuInListOfProduct.json` | L35054 | concatMedicalProductStock() (F4) | A |
| 11 | `/admin/statProductDeliveryStatusOfCashflow.json` | L34843 (delivered) | ❌ 不在 optometryCtrl | A |

---

## 20. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | 取消订单入口 | L35147 fnMap["取消订单"] | A | L1 | |
| 02 | 取消订单函数 | L35147-L35160 | A | L1 | |
| 03 | 取消订单 API | /admin/cancelMedicalRecord.json | A | L1 | 唯一调用 |
| 04 | 取消订单 Factory | 匿名 new ObjectFactory() | A | L1 | |
| 05 | 取消订单 Request | { medicalRecordId } | A | L1 | |
| 06 | 取消订单 Request 字段 | medicalRecordId 1 个 | A | L1 | |
| 07 | 取消订单 medicalRecordId | item.medicalRecord.id (L35149) | A | L1 | |
| 08 | 取消订单前置 Read | ❌ 0 处 | A | L1 | |
| 09 | 取消订单 success | if (result.status) return Popup + querySingleOrder + queryUndisposed | A | L1 | |
| 10 | 取消订单→querySingleOrder | ✅ L35156 | A | L1 | |
| 11 | 取消订单→queryUndisposed | ✅ L35157 | A | L1 | |
| 12 | 制作完成入口 | L35164 fnMap["制作完成"] | A | L1 | |
| 13 | 制作完成函数 | L35164-L35176 | A | L1 | |
| 14 | 制作完成 API | /admin/confirmMedicalRecordReturn.json | A | L1 | 唯一调用 |
| 15 | 制作完成 Factory | 匿名 new ObjectFactory() | A | L1 | |
| 16 | 制作完成 Request | { medicalRecordId } | A | L1 | |
| 17 | 制作完成 Request 字段 | medicalRecordId 1 个 | A | L1 | |
| 18 | 制作完成 medicalRecordId | item.medicalRecord.id (L35166) | A | L1 | |
| 19 | 制作完成前置 Read | ❌ 0 处 | A | L1 | |
| 20 | 制作完成 success | if (result.status) return Popup + querySingleOrder | A | L1 | |
| 21 | 制作完成→querySingleOrder | ✅ L35173 | A | L1 | |
| 22 | 制作完成→queryUndisposed | ❌ 0 处 | A | L1 | |
| 23 | 两动作 Request 对照 | API 字符串 + 弹窗 index + queryUndisposed 不同 | A | L1 | |
| 24 | F4/F3/报损边界 | 0 处直接代码连接 | A | L1 | |
| 25 | 重复提交防护 | ❌ 0 处 | A | L1 | Controller 层 |
| 26 | 两动作最小协议 | Action → popout_tip 弹窗 → Write { medicalRecordId } → success → querySingleOrder | A | L1 | |

**统计**：
- **A：26 项（全部 A）**
- **F / E / D / C / B：0**
- **E/F 升 A：0**

---

## 21. L1/L2/L3

### L1（源码事实，可证）

- 2 个 API 字符串 + 调用位置（A）
- 2 段完整源码（L35147-L35160 / L35164-L176）（A）
- Request 字段（仅 medicalRecordId）（A）
- medicalRecordId 来源（item.medicalRecord.id）（A）
- 弹窗调用（$scope.hint(1/3, fn)）（A）
- success 行为差异（queryUndisposed 调用）（A）
- 0 处前置 Read（A）
- 0 处重复提交防护（A）

### L2（业务解释，未证）

- "取消订单 = 取消医疗记录"：**E**（仅命名 + L35016 注释）
- "制作完成 = 完成加工/制作"：**E**（仅命名 + L35018 注释）
- "cancelMedicalRecord = 软删除/硬删除"：**E**
- "confirmMedicalRecordReturn = 确认回库"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 2 个 API 后端实现）

---

## 22. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 2 个 API 后端处理 | 无后端代码 | F |
| 2 个 API 真实 Response | 无样本 | F |
| HTML ng-click 触发点 | 不可得 | F |
| 弹窗 res 实际值 | popout_tip 实现 F | F |
| 弹窗期间重复点击防重 | UI 层 F | F |
| 服务端幂等性 | 无后端 | F |
| 业务语义 | 命名 + 注释 | E |
| medicalRecordId 字段值在 3 处是否完全相同 | 无后端 | F |

---

## 23. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 2 Write + 2 Read 全部仅静态审计 |
| cancelMedicalRecord 实际调用 = 0 | ✅ | |
| confirmMedicalRecordReturn 实际调用 = 0 | ✅ | |
| querySingleOrder 实际调用 = 0 | ✅ | |
| queryUndisposed 实际调用 = 0 | ✅ | |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 165 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 165_*.md |
| 文件编号连续 | ✅ | 164 已被 S1-103 占用，本轮使用 165 |

---

## 24. 最终结论

### 24.1 两动作最小协议（A 级）

#### 取消订单
```javascript
// 入口
fnMap["取消订单"]() (L35147)
    ↓
$scope.hint(1, fn) (L35148)  // popout_tip 弹窗 "确定要取消此订单吗？"
    ↓
fn: {
    var medicalRecordId = item.medicalRecord.id (L35149)
    ↓
    Write /admin/cancelMedicalRecord.json { medicalRecordId } (L35150-L35151)
    ↓ [F 边界]
    result
    ↓ if (result.status) return Popup
    ↓
    $scope.querySingleOrder() (L35156)  → 刷新列表
    $scope.queryUndisposed() (L35157)   → 刷新待处理数
}
```

#### 制作完成
```javascript
// 入口
fnMap["制作完成"]() (L35164)
    ↓
$scope.hint(3, fn) (L35165)  // popout_tip 弹窗 "确认是否已经制作完成？"
    ↓
fn: {
    var medicalRecordId = item.medicalRecord.id (L35166)
    ↓
    Write /admin/confirmMedicalRecordReturn.json { medicalRecordId } (L35167-L35168)
    ↓ [F 边界]
    result
    ↓ if (result.status) return Popup
    ↓
    $scope.querySingleOrder() (L35173)  → 刷新列表
    // ❌ 不调 queryUndisposed
}
```

### 24.2 关键事实（A 级）

1. **结构高度对称**（2 动作 5 行核心结构相同）
2. **Request 字段完全相同**（仅 `{ medicalRecordId }`）
3. **medicalRecordId 来源完全相同**（`item.medicalRecord.id`）
4. **唯一 3 处差异**：
   - API 字符串（cancelMedicalRecord.json vs confirmMedicalRecordReturn.json）
   - 弹窗 index（1 vs 3）
   - success 是否调 queryUndisposed（取消调，制作不调）
5. **0 处前置 Read**（直接调 Write）
6. **0 处前置 concatMedicalProductStock / F4 调用**
7. **0 处与 F1/F3/F4/F5/F6 链路直接代码连接**
8. **0 处与报损链路直接代码连接**
9. **0 处重复提交防护**
10. **0 处 success 成功提示 Popup**（仅错误时 Popup）

### 24.3 optometryCtrl 动作地图更新（A 级）

**optometryCtrl 共 6 个直接 Write API 调用**（S1-104 全部穷举）：
1. setMedicalRecordProcessMode.json (S1-99)
2. completeMedicalRecordDelivery.json deliveryStatus="2" (S1-99)
3. completeMedicalRecordDelivery.json deliveryStatus="1" (S1-99)
4. createMedicalStockLossOfSmallVersion.json (S1-102)
5. **cancelMedicalRecord.json (S1-104 新增)**
6. **confirmMedicalRecordReturn.json (S1-104 新增)**

### 24.4 严格表述（A 级 vs E/F）

- "两动作 Request 字段 = 仅 medicalRecordId"：**A**
- "两动作 medicalRecordId 来源 = item.medicalRecord.id"：**A**
- "两动作 success 行为差异 = queryUndisposed"：**A**
- "两动作与 Delivery / 报损 / selectOrderListFactory 闭环"：**A**（仅 selectOrderListFactory 闭环，其它 0 连接）
- "业务语义"：**E**（禁止升级 A）
- "0 处重复提交防护"：**A**（Controller 层）

### 24.5 不可在本轮升级为 A 的项

- 2 个 API 后端处理（F）
- 2 个 API 真实 Response schema（F）
- HTML ng-click 触发点（F）
- 弹窗重复点击防重（F）
- 服务端幂等性（F）
- 业务语义（E）
- 字段值在 3 处是否完全相同（F）

---

**审计结束**。
