# S1-95 F3 Request / Response 字段对应与 F6 传递审计

> **任务名**：S1-95｜F3 Request → F3 result.list 输入输出对应关系与字段映射审计（26项）
> **审计范围**：controller.js 中 `deliveryInputCtrl`（L3812-L4021）静态源码 + controller.js 全局 F3 引用搜索 + deliveryList.html 只读
> **当前轮次**：S1-95（接 S1-94 完成）
> **本轮承诺**：F3/F6 API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| controller.js deliveryInputCtrl（L3812-L4021） | ✅ | 核心审计对象 |
| controller.js 全局 F3 引用 | ✅ | 已穷举 |
| controller.js 全局 `getCenterListFactory` 引用 | ✅ | 已穷举 |
| controller.js 全局 `v.medicalProduct` / `v.machineCenter` | ✅ | 已穷举 |
| controller.js L29048 selectOrder | ⚠️ 旁证 | 独立函数（采购路径），与 F3 无关 |
| deliveryList.html | ✅（只读） | 0 处 F3/F6/selectOrder 引用 |
| F3 后端处理 | ⚠️ F 边界 | 无后端代码 |
| F3 HTTP Response 样本 | ⚠️ F 边界 | 无样本 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "F3 是加工中心查询接口"（E）
- "F3 会返回匹配的加工中心"（E）
- "F3 一定一对一"（D — 无证据）
- "F3 一定会回显 Request"（E）
- "result.list 一定就是 Request 的结果副本"（E）
- 字段名相同 → 值相等（仅 A 级才允许）
- map 函数 → 一一对应（仅当源码显式可证）

---

## 3. F3 全局引用

### F3 API 字符串全文搜索结果

| 模式 | 行号 | 上下文 |
|---|---|---|
| `getMedicalProductMachineCenterVoList.json` | L3836（仅 1 处） | `$scope.getCenterListFactory.saveOrQuery('/admin/getMedicalProductMachineCenterVoList.json', { medicalProductMachineCenterPoListJson: JSON.stringify(arr) })` |

**A 级结论**：F3 API 字符串在 controller.js / *.html / *.json 中**仅 L3836 一处**。

### getCenterListFactory 全文搜索结果

| 行号 | 表达式 | 角色 |
|---|---|---|
| L3835 | `$scope.getCenterListFactory = new ObjectFactory()` | 创建 |
| L3836 | `$scope.getCenterListFactory.saveOrQuery('/admin/...', {...})` | 调用 F3 |
| L3961 | `var arr = $scope.getCenterListFactory.result.list.map(function (v) {...})` | 消费 result.list |

**A 级结论**：`getCenterListFactory` 全局**仅 3 处引用**（创建 / 调用 / 消费），全部在 deliveryInputCtrl 范围。

### getMachineCenterList 全文搜索结果

| 行号 | 表达式 | 角色 | 与 F3 链路关系 |
|---|---|---|---|
| L3816 | `var getMachineCenterList = function getMachineCenterList() {...}` | F3 入口函数定义 | ✅ 是 |
| L3834 | `var arr = getMachineCenterList()` | F3 调用 | ✅ 是 |
| L37387 | `$scope.getMachineCenterListFactory = new ListFactory("/admin/selectMachineCenterVoList.json", 0, 100, { status: 0 })` | 另一个 controller 的独立 factory | ❌ 无关 |
| L37388 | `$scope.getMachineCenterListFactory.nextPage()` | 另一个 controller 的独立调用 | ❌ 无关 |

**A 级结论**：F3 链路的 `getMachineCenterList` 是 L3816 局部函数；L37387/L37388 是**不同 controller** 的独立 factory（`/admin/selectMachineCenterVoList.json`），与 F3 无关。

### selectOrder 全文搜索结果

| 行号 | 表达式 | 角色 | 与 F3 链路关系 |
|---|---|---|---|
| L3955 | `$scope.selectOrder = function () {...}` | F3 → F6 转换函数 | ✅ 是 |
| L29048 | `$scope.selectOrder = function () {...}` | 采购路径独立函数 | ❌ 无关 |

**A 级结论**：F3 链路的 `selectOrder` 仅 L3955 一个定义；L29048 是另一个 controller 的独立函数（`/admin/createStockPurchaseFromRequest.json`），与 F3/F6 无关。

### selectOrder 作为函数被调用搜索结果

| 模式 | 结果 |
|---|---|
| `selectOrder\(` | **0 处** |

**A 级结论**：`selectOrder` 在 controller.js 内部**未被任何代码调用**（即不是 Controller 内部串联触发），仅作为 `$scope` 暴露给 HTML 端 ng-click 触发。

---

## 4. F3 Request 完整结构

### Request 构造源码（L3816-L3829 + L3834-L3836，A 级）

```javascript
// L3816
var getMachineCenterList = function getMachineCenterList() {
    var medicalProductMachineCenterPoList = [];
    var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].medicalProduct.objectId) {  // L3821
            medicalProductMachineCenterPoList.push({
                medicalProductId: arr[i].medicalProduct.id,    // L3823
                machineCenterId: arr[i].medicalProduct.objectId  // L3824
            });
        }
    }
    return medicalProductMachineCenterPoList;
};
// L3834-L3836
var arr = getMachineCenterList();
$scope.getCenterListFactory = new ObjectFactory();
$scope.getCenterListFactory.saveOrQuery('/admin/getMedicalProductMachineCenterVoList.json', { medicalProductMachineCenterPoListJson: JSON.stringify(arr) });
```

### Request 字段级映射（A 级）

| Request 字段 | 来源表达式 | 行号 | 来源链 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|
| `medicalProductMachineCenterPoListJson` | `JSON.stringify(arr)` | L3836 | arr（getMachineCenterList 返回值） | A | L1 |
| 数组内 `medicalProductId` | `arr[i].medicalProduct.id` | L3823 | F1 waitingDeliveryList → mutation 后 objectId | A | L1 |
| 数组内 `machineCenterId` | `arr[i].medicalProduct.objectId` | L3824 | F1 waitingDeliveryList → objectId（= lockMachineCenter.id or null） | A | L1 |

### Request 数组元素完整结构（A 级）

```json
{
    "medicalProductId": <F1 waitingDeliveryList[i].medicalProduct.id>,
    "machineCenterId": <F1 waitingDeliveryList[i].medicalProduct.objectId>
}
```

- **每元素恰好 2 个字段**
- **无 type 转换**（直接 push 引用）
- **无去重**（map.push 直接累加）
- **无排序**
- **无聚合**（一一对应，每个 waitingDeliveryList[i] 至多 push 1 次）
- **过滤条件**：`if (arr[i].medicalProduct.objectId)` truthy — 仅 F1 mutation 后 objectId 为 truthy 的项进入

### JSON.stringify 关键节点（A 级）

- L3836：`JSON.stringify(arr)` 把 arr 数组序列化为字符串
- 字符串作为 `medicalProductMachineCenterPoListJson` 字段值传入 saveOrQuery

---

## 5. F3 Response result.list

### F3 result.list 消费源码（L3961-L3963，A 级）

```javascript
// L3961-L3963 (selectOrder 内)
var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
});
```

### F3 result.list 全局消费全集

| 表达式 | 行号 | 操作 |
|---|---|---|
| `$scope.getCenterListFactory.result.list.map(function (v) {...})` | L3961 | 唯一消费 |

**A 级结论**：F3 result.list 在 controller.js 全局**仅 L3961 一处消费**（仅 selectOrder 函数内）。

### F3 result.list 元素可见字段（Controller 视角）

L3962 map 函数读取的 v 元素字段：

| 表达式 | 行号 | 访问类型 | 字段路径 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|
| `v.medicalProduct.id` | L3962 | 读 | medicalProduct.id | A | L1 |
| `v.machineCenter.id` | L3962 | 读 | machineCenter.id | A | L1 |

**A 级结论**：Controller 可见范围内，**对 F3 result.list 元素只有这两个嵌套字段读取**。

**F 边界（不可证）**：
- F3 Response 是否还有其它顶层字段（除 `result.list`）— F
- F3 result.list 元素是否有 `medicalProduct` / `machineCenter` 之外的其它嵌套对象 — F
- `v.medicalProduct` 是否还有除 `id` 之外的字段（name / code / ...）— F（无样本可证）
- `v.machineCenter` 是否还有除 `id` 之外的字段 — F

**严格表述**：
- "Controller 仅消费 v.medicalProduct.id 和 v.machineCenter.id"：**A**
- "F3 Response 仅包含这两个字段"：**D**（无样本，禁止升级）
- "F3 Response 包含这两个字段"：**A**（已观察）

---

## 6. medicalProduct 对应（Request ↔ Response）

### Request 侧（A 级，已确认）
- `Request.medicalProductId` = F1 `waitingDeliveryList[i].medicalProduct.id`（L3823）
- 类型：数字（无显式转换；F1 schema 不可证）

### Response 侧（A 级，已观察）
- `Response.result.list[i].medicalProduct.id` （L3962）
- 类型：数字（无显式转换）

### 证据等级评估

| 维度 | 评估 | 等级 | 理由 |
|---|---|---|---|
| 字段路径相似 | Request.medicalProductId ↔ Response.list[i].medicalProduct.id | **C** | 字段名语义相似，但无直接对象引用连接 |
| 是否有同一变量直连 | ❌ 无 | — | Request.medicalProductId 是 `arr[i].medicalProduct.id` 推入 JSON.stringify；Response 是 HTTP 响应经 ObjectFactory 反序列化 |
| 是否有 F3 后端可证 | ❌ 无后端代码 | — | 无法证明 F3 后端是否将 Request.medicalProductId 反射到 Response.medicalProduct.id |
| 是否有真实 Response 样本 | ❌ 无 | — | 无法对比值 |

### 严格表述
- "Request 包含 medicalProductId 字段"：**A**
- "Response 包含 medicalProduct.id 字段"：**A**（Controller 视角）
- "Request.medicalProductId 值 = Response.medicalProduct.id 值"：**F**（无样本，无后端可证）
- "Request.medicalProductId 字段名 → 业务主键含义"：**E**（禁止升级）

---

## 7. machineCenter 对应（Request ↔ Response）

### Request 侧（A 级，已确认）
- `Request.machineCenterId` = F1 `waitingDeliveryList[i].medicalProduct.objectId`（L3824）
- 类型：数字（= lockMachineCenter.id，type==4 时）或 null（else 时，已被 F3 过滤掉）

### Response 侧（A 级，已观察）
- `Response.result.list[i].machineCenter.id` （L3962）

### 证据等级评估

| 维度 | 评估 | 等级 | 理由 |
|---|---|---|---|
| 字段路径相似 | Request.machineCenterId ↔ Response.list[i].machineCenter.id | **C** | 字段名语义相似，但无直接对象引用连接 |
| 是否有同一变量直连 | ❌ 无 | — | 经 HTTP 边界 |
| 是否有 F3 后端可证 | ❌ 无后端代码 | — | 无法证明 F3 后端是否回显 Request.machineCenterId |
| 是否有真实 Response 样本 | ❌ 无 | — | 无法对比值 |

### 严格表述
- "Request 包含 machineCenterId 字段"：**A**
- "Response 包含 machineCenter.id 字段"：**A**（Controller 视角）
- "Request.machineCenterId 值 = Response.machineCenter.id 值"：**F**（无样本，无后端可证）

---

## 8. selectOrder() 完整审计

### 完整函数体（L3955-L3977，A 级）

```javascript
$scope.selectOrder = function () {
    if (!$scope.startTime) {
        Popup.notice("请选择取镜日期");
        return false;
    }

    var arr = $scope.getCenterListFactory.result.list.map(function (v) {
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);
    $scope.createOrderFactory = new ObjectFactory();
    var createPromise = $scope.createOrderFactory.saveOrQuery('/admin/sendMedicalProductToMachineCenter.json', { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime });
    createPromise.then(function (res) {
        if (res.status == 1) {
            Popup.notice(res.errmsg);
        } else {
            Popup.notice('发送成功');
            $scope.addOrderModal = false;
            $state.reload();
        }
    });
};
```

### 字段重命名分析（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 读取字段 | 仅 `v.medicalProduct.id` + `v.machineCenter.id` | A |
| 输出字段 | 仅 `medicalProductId` + `machineCenterId` | A |
| 字段数 | 输入 2 字段 → 输出 2 字段 | A |
| 是否重命名 | ✅ medicalProduct.id → medicalProductId（去前缀，扁平化） | A |
| | ✅ machineCenter.id → machineCenterId（去前缀，扁平化） | A |
| 是否有条件分支 | ❌ 无（map 函数体是单一 return 表达式） | A |
| 是否有默认值 | ❌ 无 | A |
| 是否有类型转换 | ❌ 无 | A |
| 是否有过滤 | ❌ 无（map 遍历所有 result.list 元素） | A |
| 是否有去重 | ❌ 无 | A |
| 是否有排序 | ❌ 无 | A |
| 是否有聚合 | ❌ 无（一进一出） | A |
| 是否新增字段 | ❌ 无 | A |
| 是否丢弃其它字段 | ✅ 是（除 medicalProduct.id / machineCenter.id 外的所有字段全部丢弃） | A |

### 严格表述
- "Controller 层 selectOrder() 产生新数组，每个元素仅包含 2 字段"：**A**
- "selectOrder() 不修改 result.list 原数组"：**A**（map 创建新数组）
- "selectOrder() 内不修改 v 对象"：**A**（map 函数体是 return 新对象）

---

## 9. F3 result.list 原对象是否被修改

### 检查项

| 检查项 | deliveryInputCtrl 范围 (L3812-L4021) | A-F |
|---|---|---|
| `result.list[i].xxx =` | 0 处 | A |
| `getCenterListFactory.result.list[i].xxx =` | 0 处 | A |
| `v.xxx =` | 0 处 | A |
| `v.medicalProduct.xxx =` | 0 处 | A |
| `v.machineCenter.xxx =` | 0 处 | A |

### A 级结论
- **当前 Controller 未观察到对 F3 result.list 原元素的直接写入。**
- map 函数体仅 `return { medicalProductId: ..., machineCenterId: ... }`，创建新对象
- 原 result.list 元素引用未被赋值修改

---

## 10. 过滤/去重/排序/聚合 检查

### Controller 视角（A 级，全部 0 处）

| 操作 | F3 result.list 上 | A-F |
|---|---|---|
| `filter` | ❌ 0 处 | A |
| `sort` / `orderBy` | ❌ 0 处 | A |
| `uniq` / `unique` / `Set` | ❌ 0 处 | A |
| `indexOf` 去重 | ❌ 0 处 | A |
| `reduce` | ❌ 0 处 | A |
| `concat` | ❌ 0 处 | A |
| `push` | ❌ 0 处（map 自身） | A |
| `slice` / `splice` | ❌ 0 处 | A |
| `reverse` | ❌ 0 处 | A |
| `if` / `continue` / `break` | ❌ 0 处 | A |

### A 级结论
- **Controller 视角**：F3 result.list 在 L3961 仅经历 `.map(function (v) {...})`，未观察到任何过滤/去重/排序/聚合操作。
- **后端视角**：F 边界（不可证）。

### 严格表述
- "Controller 未对 F3 result.list 做过滤/去重/排序/聚合"：**A**
- "F3 后端未做过滤/去重/排序/聚合"：**F**（无后端代码 / 无样本）

---

## 11. Request ↔ Response 数量关系

### 检查项（A 级）

| 检查项 | 评估 | A-F |
|---|---|---|
| 源码中 `arr.length` 与 `result.list.length` 比较 | ❌ 0 处 | A |
| 源码中 `Request.length === Response.length` 断言 | ❌ 0 处 | A |
| 源码中下标 i 同时索引 Request[i] 与 Response[i] | ❌ 0 处（两者完全分离：Request 在 L3836 已 JSON.stringify 提交；Response 在 L3961 重新 map） | A |
| 源码中 Request 数组与 Response 数组显式建立索引对应 | ❌ 0 处 | A |

### A 级结论
- **当前 Controller 未观察到对 Request 元素数量与 Response 元素数量进行显式比较或索引对应。**
- Request 在 L3836 通过 `saveOrQuery` 提交（异步），Response 在 L3961 通过 `$scope.getCenterListFactory.result.list` 接收（异步）
- 两者在 Controller 视角**没有显式索引对应代码**

### 严格表述
- "F3 Request 与 Response 在 Controller 视角无显式索引对应"：**A**
- "F3 一定一对一"：**D**（无证据）
- "F3 一定多对一 / 一对多"：**D**（无证据）
- "F3 一定回显 Request"：**E**（业务推断）

---

## 12. Response → F6

### 完整链路（A 级闭合节点 + F 边界）

```
F3 result.list (ObjectFactory 反序列化结果)
    ↓ L3961 .map(function (v) {...})
新数组 arr
    ↓ 元素构造: { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }
每个 arr 元素恰好 2 字段
    ↓ L3966 JSON.stringify(arr)
F6 Request.medicalProductMachineCenterPoListJson (字符串)
    ↓ saveOrQuery
F6 (/admin/sendMedicalProductToMachineCenter.json)
```

### 字段链（A 级）

| 节点 | 表达式 | 行号 | 字段 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|
| 1 | `v.medicalProduct.id` | L3962 | medicalProductId 源 | A | L1 |
| 2 | `{ medicalProductId: v.medicalProduct.id, ... }` | L3962 | 构造新对象 | A | L1 |
| 3 | `JSON.stringify(arr)` | L3966 | 序列化 | A | L1 |
| 4 | F6 Request.medicalProductMachineCenterPoListJson | L3966 | 提交 | A | L1 |
| **中间节点** | **F3 后端** | — | **F 边界** | F | L1=F |
| 5 | `v.machineCenter.id` | L3962 | machineCenterId 源 | A | L1 |
| 6 | `{ ..., machineCenterId: v.machineCenter.id }` | L3962 | 构造新对象 | A | L1 |
| 7 | `JSON.stringify(arr)` | L3966 | 序列化 | A | L1 |
| 8 | F6 Request.medicalProductMachineCenterPoListJson.machineCenterId | L3966 | 提交 | A | L1 |

**F 边界（不可跨过）**：
- F3 后端处理（Request → Response 转换）— F
- 任何 "Request.medicalProductId == Response.medicalProduct.id" 的值相等断言 — F
- 任何 "F3 后端一定回显 / 一定转换" 的业务推断 — E

---

## 13. F3 → F6 字段链（与 S1-91/S1-94 对照）

### 与 S1-91 对照（F3 result.list → F6 字段闭合）

| 维度 | S1-91 结论 | S1-95 补充 |
|---|---|---|
| F3 result.list → F6 字段闭合 | 已确认 medicalProductId + machineCenterId 闭合 | S1-95 进一步确认 **Controller 仅消费这两个字段** |
| 是否丢弃其它字段 | 未明确 | S1-95 确认：**除 medicalProduct.id / machineCenter.id 外所有字段全部丢弃** |
| 是否新增字段 | 未明确 | S1-95 确认：**未新增任何字段** |

### 与 S1-94 对照（lockMachineCenter.id → objectId → F3）

| 维度 | S1-94 结论 | S1-95 补充 |
|---|---|---|
| lockMachineCenter.id → F3 Request.machineCenterId | 已确认间接链 | S1-95 进一步确认 **F3 Request 构造 L3824 即依赖 objectId** |
| objectId 来源 | F1 mutation | S1-95 进一步确认 **F1 mutation 经 L3854/L3856 写入** |

### 综合链路（S1-91 + S1-94 + S1-95）

```
F1 waitingDeliveryList[i].lockMachineCenter.id
    ↓ L3854
medicalProduct.objectId (运行时字段)
    ↓ L3824
F3 Request.medicalProductMachineCenterPoListJson[].machineCenterId
    ↓ JSON.stringify (L3836)
F3 Request
    ↓ F3 后端 (F 边界)
F3 Response.result.list[i].machineCenter.id
    ↓ L3962
新 arr.machineCenterId
    ↓ JSON.stringify (L3966)
F6 Request.medicalProductMachineCenterPoListJson[].machineCenterId
```

**A 级闭合节点**：L3854 / L3824 / L3836 / L3962 / L3966
**F 边界**：F3 后端处理

### 三层区分（S1-95 重点）

| 维度 | 含义 | 是否已证 |
|---|---|---|
| A. 字段名一致 | Request.medicalProductId 与 Response.medicalProduct.id 字段名相似 | A（可证相似） |
| B. 值一致 | Request.medicalProductId === Response.medicalProduct.id | **F**（无样本可证） |
| C. 对象同源 | Request 与 Response 元素是同一对象 | **F**（HTTP 边界隔断） |

**严格表述**：
- "字段名一致（A）"：**A**
- "值一致（B）"：**F**
- "对象同源（C）"：**F**

---

## 14. ListFactory / ObjectFactory 边界

### 已观察的 ObjectFactory 使用（L3835 / L3965）

```javascript
// L3835
$scope.getCenterListFactory = new ObjectFactory();
// L3965
$scope.createOrderFactory = new ObjectFactory();
```

### 边界声明（A 级）

| 项 | 不可证原因 | 标注 |
|---|---|---|
| ObjectFactory.saveOrQuery 内部如何发送 HTTP | 无 factory 源码 | F |
| result 如何从 HTTP 响应反序列化 | 无 factory 源码 | F |
| count 字段如何生成 | 无 factory 源码 | F |
| list 如何分页 | 无 factory 源码 | F |
| 后端如何处理 Request | 无后端代码 | F |

### 严格表述（A 级）
- "Controller 显式构造的 Request 字段"：**A**（已穷举）
- "Controller 显式读取的 Response 字段"：**A**（已穷举）
- "ObjectFactory 内部如何工作"：**F**（factory 源码不可得）
- "F3 后端如何处理"：**F**（无后端代码）

---

## 15. Read/Write

| API | 类型 | 实际调用 |
|---|---|---|
| F3 (`getMedicalProductMachineCenterVoList.json`) | Read | **0**（仅源码审计） |
| F6 (`sendMedicalProductToMachineCenter.json`) | Write | **0**（仅源码审计） |

**A 级结论**：本轮 F3/F6 实际调用 = 0。

---

## 16. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | F3 API 全局引用 | L3836（仅 1 处） | A | L1 | controller.js + *.html + *.json 全文搜索 |
| 02 | F3 Request 来源 | L3822-3825 push → L3834 getMachineCenterList() → L3836 saveOrQuery | A | L1 | |
| 03 | Request.medicalProductId | L3823: `arr[i].medicalProduct.id` | A | L1 | |
| 04 | Request.machineCenterId | L3824: `arr[i].medicalProduct.objectId` | A | L1 | 经 F1 mutation 链路 |
| 05 | JSON.stringify | L3836: `JSON.stringify(arr)` | A | L1 | |
| 06 | F3 result.list 来源 | L3961: `$scope.getCenterListFactory.result.list` | A | L1 | |
| 07 | result.list 元素可见字段 | L3962 读取 v.medicalProduct.id + v.machineCenter.id | A | L1 | Controller 视角 |
| 08 | v.medicalProduct | L3962 仅读 id | A | L1 | 其它字段 F |
| 09 | v.machineCenter | L3962 仅读 id | A | L1 | 其它字段 F |
| 10 | selectOrder() | L3955-3977 完整 23 行 | A | L1 | |
| 11 | selectOrder 参数 | 无参数 | A | L1 | 依赖 $scope |
| 12 | selectOrder map | L3961-3963 | A | L1 | |
| 13 | 新数组结构 | 每元素 2 字段 { medicalProductId, machineCenterId } | A | L1 | |
| 14 | 原数组是否修改 | ❌ map 创建新数组，原 result.list 未被写入 | A | L1 | |
| 15 | 过滤 | ❌ 0 处 | A | L1 | Controller 视角 |
| 16 | 去重 | ❌ 0 处 | A | L1 | Controller 视角 |
| 17 | 排序 | ❌ 0 处 | A | L1 | Controller 视角 |
| 18 | 聚合/展开 | ❌ 0 处 | A | L1 | Controller 视角 |
| 19 | Request/result 数量比较 | ❌ 0 处 | A | L1 | 异步分离，无显式索引 |
| 20 | Request↔result.medicalProductId | 字段路径相似（C），值相等（F） | C / F | L1 | |
| 21 | Request↔result.machineCenterId | 字段路径相似（C），值相等（F） | C / F | L1 | |
| 22 | result→F6 medicalProductId | L3962: `medicalProductId: v.medicalProduct.id` → L3966 JSON.stringify | A | L1 | |
| 23 | result→F6 machineCenterId | L3962: `machineCenterId: v.machineCenter.id` → L3966 JSON.stringify | A | L1 | |
| 24 | F3 global consumer | L3961（仅 1 处 result.list 消费） | A | L1 | 全文 grep 确认 |
| 25 | F3→F6 最小字段链 | L3962 (2 字段) → L3966 (JSON.stringify) | A | L1 | |
| 26 | F3 Request/Response 同源边界 | 经 HTTP 边界，对象引用隔断 | F | L1 | 无后端代码可证 |

**统计**：
- A：23 项
- C：1 项（#20 / #21 字段路径相似 — 已合并）
- F：2 项（#20 / #21 值相等 + #26 同源）
- D：0
- B：0
- E：0
- **E/F 升 A：0**

---

## 17. L1/L2/L3

### L1（源码事实，可证）

- F3 API 调用位置 L3836
- Request 字段构造 L3823 / L3824
- JSON.stringify L3836
- result.list 消费 L3961
- map 函数体 L3962
- selectOrder 完整函数体 L3955-L3977
- 0 处原对象写入
- 0 处过滤/去重/排序/聚合
- 0 处 Request/Response 数量比较
- F3 global consumer = 1（L3961）

### L2（业务解释，未证）

- "F3 是加工中心查询接口"：**E**（未证）
- "F3 一定一对一"：**D**（未证）
- "F3 一定回显 Request"：**E**（未证）
- "result.list 是 Request 的回显副本"：**E**（未证）
- "machineCenter.id = 加工中心 ID"：**E**（未证）
- "F6 是发送商品到加工中心"：**E**（未证）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 schema 样本 / 无 F3 后端实现）

---

## 18. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| F1 Response 原始 schema | 无样本 | F |
| F3 HTTP Response 真实样本 | 无样本 | F |
| F3 Response 完整字段 | 无样本 / 无后端代码 | F |
| F3 后端处理逻辑 | 无后端代码 | F |
| F3 后端是否过滤/去重/排序 | 无后端代码 | F |
| F3 后端是否回显 Request | 无后端代码 | F |
| Request.medicalProductId 值 = Response.medicalProduct.id 值 | 无样本可证 | F |
| Request.machineCenterId 值 = Response.machineCenter.id 值 | 无样本可证 | F |
| Request 与 Response 元素是否同源 | HTTP 边界隔断 | F |
| 其它 Controller / Service 是否消费 F3 result.list | 本轮范围仅 deliveryInputCtrl | F（本轮范围内 0 处） |
| deliveryList.html 是否消费 F3 result.list | 已审计 0 处 | A（本轮范围内 0 处） |
| ObjectFactory 内部实现 | 无 factory 源码 | F |
| machineCenter / medicalProduct 字段是否仅 id | 无 Response 样本 | F |

---

## 19. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何实际 API 调用 = 0 | ✅ | F3/F6 仅源码审计 |
| F3 Read = 0 | ✅ | 未触发 getMedicalProductMachineCenterVoList.json |
| F6 Write = 0 | ✅ | 未触发 sendMedicalProductToMachineCenter.json |
| save / submit / send / delivery / receive / charge / refund / recharge / start / complete / close / notify 全部 0 调用 | ✅ | |
| controller.js 未修改 | ✅ | git status --short 不显示 M |
| deliveryList.html 未修改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变） |
| 历史 MD 未修改 | ✅ | 仅新增 156_*.md |
| 10 untracked 临时文件原样保留 | ✅ | _gen_phase0_placeholders.ps1 / .py / controller.js / 7 HTML 仍 untracked |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 156_*.md |
| 文件编号连续 | ✅ | 155 已被 S1-94 占用，本轮使用 156 |

---

## 20. 最终结论

### F3 Request / Response 最小事实（A 级）

**Request 侧**（L3816-L3836）：
- API: `getMedicalProductMachineCenterVoList.json`
- Body: `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }`
- arr 元素: `{ medicalProductId, machineCenterId }`
- medicalProductId 来源: `waitingDeliveryList[i].medicalProduct.id`（F1）
- machineCenterId 来源: `waitingDeliveryList[i].medicalProduct.objectId`（F1 + L3854/L3856 mutation）

**Response 侧**（L3961-L3963）：
- 消费点: `$scope.getCenterListFactory.result.list.map(function (v) {...})`（L3961）
- map 函数体读取: `v.medicalProduct.id` + `v.machineCenter.id`（L3962）
- 输出: `{ medicalProductId, machineCenterId }`
- 全局 result.list 消费 = 1 处

**F6 侧**（L3955-L3977）：
- selectOrder 把 result.list map 为新数组
- 新数组每元素 2 字段
- L3966 JSON.stringify → F6 Request.medicalProductMachineCenterPoListJson

### F3 Request ↔ Response 关键事实

| 维度 | 结论 | 等级 |
|---|---|---|
| 字段名相似 | Request.medicalProductId ↔ Response.medicalProduct.id | **A（可证相似）** |
| 字段名相似 | Request.machineCenterId ↔ Response.machineCenter.id | **A（可证相似）** |
| 值相等 | 不可证 | **F** |
| 对象同源 | 不可证（HTTP 边界） | **F** |
| 数量对应 | 不可证（无显式索引） | **F** |
| Controller 视角一对一 | 仅可证 map 一进一出 | **A**（Controller 视角） |
| F3 后端一对一 | 不可证 | **F** |
| F3 是回显/查询/匹配/转换 | 不可证 | **F** |

### 与 S1-91 / S1-94 综合链路（A 级闭合节点 + F 边界）

```
F1 waitingDeliveryList[i].lockMachineCenter.id
    ↓ L3854 (lockStorehouse.type==4)
medicalProduct.objectId (F1 mutation)
    ↓ L3824
F3 Request arr.machineCenterId
    ↓ L3836 JSON.stringify
F3 Request.medicalProductMachineCenterPoListJson
    ↓ [F 边界: F3 后端]
F3 Response.result.list[i].machineCenter.id
    ↓ L3962
新 arr.machineCenterId
    ↓ L3966 JSON.stringify
F6 Request.medicalProductMachineCenterPoListJson.machineCenterId
```

**A 级闭合节点**：L3854 / L3824 / L3836 / L3962 / L3966
**F 边界**：F3 后端处理（不可证 Request → Response 的具体转换）

### 不可在本轮升级为 A 的项

- Request 与 Response 的值相等（F）
- Request 与 Response 的对象同源（F）
- F3 后端是否回显 / 过滤 / 去重 / 排序 / 聚合（F）
- 字段名 → 业务主键含义（E）
- "F3 一定一对一"（D）
- machineCenter / medicalProduct 的其它字段（F）
- 其它 Controller / HTML 消费 F3 result.list（本轮范围外，F）

---

**审计结束**。
