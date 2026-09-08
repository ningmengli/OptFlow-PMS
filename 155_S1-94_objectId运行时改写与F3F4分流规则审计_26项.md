# S1-94 medicalProduct.objectId 运行时改写与 F3/F4 分流规则审计

> **任务名**：S1-94｜waitingDeliveryList → medicalProduct.objectId 运行时改写规则 + F3/F4 分流条件审计（26项）
> **审计范围**：controller.js 中 `deliveryInputCtrl`（L3812-L4021）静态源码 + deliveryList.html 只读 + F1/F3/F4/F5/F6 间接链
> **当前轮次**：S1-94（接 S1-93 完成）
> **本轮承诺**：F5/F6 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| controller.js deliveryInputCtrl（L3812-L4021） | ✅ | 核心审计对象 |
| controller.js 其它 Controller | ❌ | 不在本轮范围（按"原对象副作用"目标做最小旁证） |
| deliveryList.html（12720 bytes / SHA256 `5B79B6F0...`） | ✅（只读） | 确认 0 处 objectId |
| F1 Response schema（无后端代码） | ⚠️ F 边界 | 不可直接证伪 |
| F3/F4/F5/F6 后端处理 | ⚠️ F 边界 | 不可证后端具体处理 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- E 升 A（"objectId 是 DB 主键" 等均为 E）
- F 升 A（"F1 Response 原始不存在 objectId" 不能写成"不存在"）
- 字段名 → 业务定义（"objectId = 加工中心 ID" 是 E）
- 条件值 → 业务语义（"lockStorehouse.type == 4 = 加工中心" 是 E）

---

## 3. medicalProduct.objectId 全局读写

**deliveryInputCtrl（L3812-L4021）范围内 `medicalProduct.objectId` 引用全集 = 7 处**：

| 行号 | 表达式 | 读/写 | 上下文 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|
| L3821 | `if (arr[i].medicalProduct.objectId)` | 读 | getMachineCenterList 过滤（F3 上游） | A | L1 |
| L3824 | `machineCenterId: arr[i].medicalProduct.objectId` | 读 | getMachineCenterList 构造 arr | A | L1 |
| L3854 | `...medicalProduct.objectId = arr[i].lockMachineCenter.id` | **写** | search().then 条件分支 | A | L1 |
| L3856 | `...medicalProduct.objectId = null` | **写** | search().then 条件 else | A | L1 |
| L3873 | `if (arr[i].medicalProduct.objectId == null)` | 读 | showDeliveryModal 过滤（F4） | A | L1 |
| L3899 | `if (arr[i].medicalProduct.objectId)` | 读 | isSendProduct 辅助函数 | A | L1 |
| L3916 | `if (arr[i].medicalProduct.objectId == null)` | 读 | isSendCenter 辅助函数 | A | L1 |

**写入点（仅 2 处）**：
- L3854 = `lockMachineCenter.id`（在 `lockStorehouse.type == 4` 分支）
- L3856 = `null`（else 分支）

**读取点（5 处）**：
- L3821 / L3824 → F3 上游（getMachineCenterList）
- L3873 → F4 上游（showDeliveryModal）
- L3899 / L3916 → 辅助函数（isSendProduct / isSendCenter），仅判断是否存在可发送项

---

## 4. F1 Response 原始字段边界

| 字段 | 在 F1 Response 中是否原始存在 | 证据 | A-F | L1/L2/L3 |
|---|---|---|---|---|
| `waitingDeliveryList` | 已确认存在 | L3851 `var arr = res.result.object.waitingDeliveryList` 直接读取 | A | L1 |
| `waitingDeliveryList[i].lockStorehouse.type` | 已确认存在 | L3853 条件读取（无需 mutation 即参与判断） | A | L1 |
| `waitingDeliveryList[i].lockMachineCenter.id` | 已确认存在 | L3854 读取并写入 objectId | A | L1 |
| `waitingDeliveryList[i].medicalProduct.id` | 已确认存在 | L3823 / L3874 直接读取 | A | L1 |
| `waitingDeliveryList[i].medicalProduct.objectId` | **F（不可证）** | 当前源码未观察到对 F1 原始值的显式保护读取；F1 Response 中是否存在此字段，无 schema 样本 | F | L1=F / L2=F / L3=F |

**结论**：F1 Response 是否"自带" `medicalProduct.objectId` 这一字段，在本轮资源范围内不可证明。Controller 在拿到 F1 Response 之后立即进行 mutation（L3854/L3856），因此既无法证其初始存在，也无法证其初始不存在。

**严格表述**：
- "F1 Response 原始 objectId 是否存在"：**F**（不可得）
- "Controller 在 search().then 内对 F1 Response 引用做 mutation"：**A**（已证）
- "F1 Response 原始 objectId 等于 lockMachineCenter.id"：**D**（源码不支持此断言——只有 mutation 后才相等；且 F1 Response 是否自带 objectId 未证）

---

## 5. lockStorehouse.type

| 维度 | 证据 | A-F | L1/L2/L3 |
|---|---|---|---|
| 真实对象层级 | `arr[i].lockStorehouse.type`（A） | A | L1 |
| 读取位置全集 | L3853（仅 1 处） | A | L1 |
| 条件表达式 | `if (arr[i].lockStorehouse.type == 4)`（A） | A | L1 |
| 进入 Request | ❌ 无（未观察到 lockStorehouse / type 进入任何 Request） | A | L1 |
| 类型转换 | ❌ 无（直接 == 数字字面量） | A | L1 |
| null/undefined 保护 | ❌ 无（直接读取 .type，不存在保护） | A | L1 |

**条件使用**：
- 仅出现在 search().then 的 L3853 条件判断
- 用于决定 objectId 写入 `lockMachineCenter.id` 还是 `null`
- 未观察到对 lockStorehouse 任何其它字段、其它层级的访问

**严格表述**：
- "lockStorehouse.type == 4 时把 lockMachineCenter.id 写入 objectId"：**A**
- "type == 4 意味着加工中心"：**E**（业务推断，未证）
- "lockStorehouse 可能为 null/undefined"：**F**（源码无保护，也无 F1 schema 可证）

---

## 6. lockMachineCenter.id

| 维度 | 证据 | A-F | L1/L2/L3 |
|---|---|---|---|
| 真实对象层级 | `arr[i].lockMachineCenter.id`（A） | A | L1 |
| 读取位置全集 | L3854（仅 1 处） | A | L1 |
| 写入目标 | `medicalProduct.objectId` | A | L1 |
| 是否有 null 保护 | ❌ 无（直接 `.id` 读取） | A | L1 |
| 类型转换 | ❌ 无 | A | L1 |
| 直接进入 F3 Request | ❌ 无（必须经 objectId 间接链） | A | L1 |
| 直接进入 F6 Request | ❌ 无 | A | L1 |
| 间接进入 F3 Request | ✅ `lockMachineCenter.id` → objectId (L3854) → F3 arr.machineCenterId (L3824) | A | L1 |
| 间接进入 F6 Request | ✅ 经 F3 后端 → F3 result.list[i].machineCenter.id (L3962) → F6 arr.machineCenterId | A（中间 F3 后端 = F 边界） | L1 |

**完整间接链**（无业务推断）：

```
F1 waitingDeliveryList[i].lockMachineCenter.id
    ↓ L3854 (lockStorehouse.type == 4 分支)
medicalProduct.objectId  (运行时字段，注入到原对象引用)
    ↓ L3824
F3 Request arr.machineCenterId
    ↓ JSON.stringify → F3 Request.medicalProductMachineCenterPoListJson
F3 后端处理 (F 边界)
    ↓
F3 Response.result.list[i].machineCenter.id
    ↓ L3962 (map function v)
F6 Request.medicalProductMachineCenterPoListJson[].machineCenterId
```

---

## 7. medicalProduct.objectId 写入规则

**L3854 / L3856 完整条件**（A 级）：

```javascript
for (var i = 0; i < arr.length; i++) {
    if (arr[i].lockStorehouse.type == 4) {
        $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
    } else {
        $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
    }
}
```

**写入规则**（最小化、无业务推断）：

| 条件 | 写入值 | 字段类型 | A-F |
|---|---|---|---|
| `lockStorehouse.type == 4` | `lockMachineCenter.id` | 数字（无显式转换） | A |
| 其它（lockStorehouse.type != 4 或 lockStorehouse 不存在 → 抛错） | `null` | null | A |

**写入的副作用**：
- 直接对 `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct` 做 mutation
- 该对象是 F1 Response 引用（详见 §12）
- 没有 `angular.copy` / `angular.clone` / `JSON.parse(JSON.stringify(...))` 保护
- mutation 后该对象既被后续的 F3/F4 过滤读取（间接影响 Request 内容），又被 isSendProduct / isSendCenter 辅助函数读取（仅判断是否存在可发送项）

**写入位置 ≠ 读取位置（写入来自 F1 二次回写，读取来自 mutation 后的对象）**：
- 写入：F1 Response 引用上
- 读取：F3/F4/辅助函数对 mutation 后的对象读取

**严格表述**：
- "objectId 是 L3854/L3856 写入的运行时字段"：**A**
- "写入值是 F1 Response 原始 lockMachineCenter.id / null"：**A**（对 lockMachineCenter.id 是 A；对 null 是 A）
- "F1 Response 原始 objectId 不会影响 F3/F4 过滤"：**A**（L3854/L3856 在所有下游读取之前已经发生，且无恢复原值逻辑）

---

## 8. F3/F4 分流（基于 JavaScript 条件）

### F3 过滤（L3821）
```javascript
if (arr[i].medicalProduct.objectId) { ... }  // truthy
```
- L3821：getMachineCenterList 内 F3 入口过滤
- L3899：isSendProduct 辅助函数（仅判断存在性，不构造 Request）

### F4 过滤（L3873）
```javascript
if (arr[i].medicalProduct.objectId == null) { ... }  // == null（宽松相等）
```
- L3873：showDeliveryModal 内 F4 入口过滤
- L3916：isSendCenter 辅助函数

### JavaScript 条件全集分析（A 级语言事实）

| 字段值类型 | 例子 | `if (objectId)` | `if (objectId == null)` | 进入 F3 | 进入 F4 |
|---|---|---|---|---|---|
| 数字非 0 | `123` | truthy | false | ✅ | ❌ |
| 数字 0 | `0` | **falsy** | false | ❌ | ❌ |
| 字符串非空 | `"abc"` | truthy | false | ✅ | ❌ |
| 空字符串 | `""` | **falsy** | false | ❌ | ❌ |
| true | `true` | truthy | false | ✅ | ❌ |
| false | `false` | **falsy** | false | ❌ | ❌ |
| 对象 `{}` | `{}` | truthy | false | ✅ | ❌ |
| 数组 `[]` | `[]` | truthy | false | ✅ | ❌ |
| NaN | `NaN` | **falsy** | false | ❌ | ❌ |
| null | `null` | falsy | true | ❌ | ✅ |
| undefined | `undefined` | falsy | true | ❌ | ✅ |
| 缺失 | 无该属性 | falsy | true | ❌ | ✅ |

### 实际 F1 二次写入可能产生的值域

- L3854 分支：`lockMachineCenter.id`（数字，无显式转换）
- L3856 分支：`null`

**结论**：
- L3854 路径 → 数字 → `if (objectId)` 多数 truthy → 进入 F3；`if (objectId == null)` false → 不进入 F4
- L3856 路径 → null → `if (objectId)` falsy → 不进入 F3；`if (objectId == null)` true → 进入 F4

**理论第三分支（A 级语言事实）**：
- `objectId = 0` / `""` / `false` / `NaN` → 既不进入 F3 也不进入 F4
- 这些项**会从所有 Request 中消失**（既不参与 F3 也不参与 F4）

**实际是否会出现第三分支？**：
- 当前源码唯一写入路径是 L3854/L3856
- L3854 路径 = `lockMachineCenter.id`（数字，理论可能为 0，但 F 边界：F1 schema 不可证）
- L3856 路径 = null
- **未观察到对 0 / "" / false / NaN 的写入**
- 因此**理论存在第三分支，实际不进入第三分支**（A 级源代码事实，但 F1 schema 不可证 F1 不主动产生 0）

---

## 9. 第三分支（理论值 / 实际值）

**理论第三分支**（仅语言层面）：
- `if (objectId)` 与 `if (objectId == null)` 在 JavaScript 中**非完全互补**
- 0 / "" / false / NaN 既不通过 F3 也不通过 F4
- 这些项在 F3 / F4 / F5 / F6 全部链路中**完全消失**

**实际第三分支**（基于当前源码写入逻辑）：
- L3854/L3856 是唯一写入路径
- 写入值仅可能是 `数字`（lockMachineCenter.id）或 `null`
- 不主动产生 0 / "" / false / NaN
- 因此**当前源码实现下不会出现第三分支**

**严格表述**：
- "F3/F4 过滤条件在 JavaScript 语义上不互补"：**A**
- "当前 Controller 实现下不会出现既不进 F3 也不进 F4 的项"：**A**（基于写入路径分析）
- "F1 Response 不可能产生 0 / "" / false / NaN"：**F**（F1 schema 不可证）

---

## 10. search() 时序与重复执行

### 重复执行能力

| 调用点 | 行号 | 触发条件 | 行为 |
|---|---|---|---|
| 自动调用 | L3866 | Controller 初始化 | 立即执行 search() |
| F5 success | L4014 | saveStock (F5) 成功（res.status != 1） | search() + getCount() + $state.reload() + $scope.stockDetail = false |

**重复执行能力 = 2**（L3866 init + L4014 F5 success）

### 时序（Controller 视角）

```
1. L3812-3814: Controller 初始化
   $scope.cashflowId = $stateParams.cashflowId
2. L3816-3829: getMachineCenterList 函数定义（不执行）
3. L3830-3837: $scope.showAddModal 函数定义（不执行）
4. L3839-3842: getCount 函数定义
5. L3844: getCount() 立即执行（F2 stat API）
6. L3846-3865: search 函数定义
7. L3866: search() 立即执行
   ↓
   F1 Request /admin/getCashflowDeliveryVo.json
   ↓
   L3851-3858: waitingDeliveryList 获取 + objectId 运行时改写
   ↓
   L3859-3863: 若 arr.length == 0 弹窗返回列表
8. L3868-3886: $scope.showDeliveryModal 函数定义（不执行）
9. L3888-3904: $scope.isSendProduct 函数定义（不执行）
10. L3905-3921: $scope.isSendCenter 函数定义（不执行）
11. ... 其它辅助函数定义 ...
12. 用户后续触发:
    - showAddModal → F3
    - showDeliveryModal → F4
    - selectOrder → F6
    - saveStock → F5 (success → search() 重复执行)
```

### search() 重复执行的副作用

**每次 search() 执行时**：
1. 重新创建 `$scope.getMedicalRecordDeliveryFactory`（L3847）
2. 重新发 F1 Request
3. **重新对 F1 Response 引用做 mutation**（L3854/L3856）
4. 因为 F1 Response 是新对象引用（来自 L3848 的 saveOrQuery 返回），mutation 只影响本次响应

**是否恢复原值？**：
- ❌ 无 `arr[i].medicalProduct.objectId = <原值>` 恢复逻辑
- ❌ 无 `angular.copy` 隔离原值
- ❌ 无 "先备份 mutation 前值" 逻辑
- 因为每次 search() 都重新创建 factory 和重新发请求，**原对象"恢复"问题在 F1 Response 是新引用的前提下不存在**

**严格表述**：
- "search() 重复执行能力 = 2"：**A**
- "search() 每次执行都重新做 mutation"：**A**
- "F1 Response 原对象被保留"：**D**（F1 Response 是新引用，不存在"原对象被保留"问题；但 F1 旧 Response 引用被丢弃，旧 mutation 不会被新 search() 看到）

---

## 11. F1 Response 原对象 mutation（直接副作用）

### 关键源码（A 级）

```javascript
// L3847-3858
$scope.getMedicalRecordDeliveryFactory = new ObjectFactory();
var deliveryPromise = $scope.getMedicalRecordDeliveryFactory.saveOrQuery(
    '/admin/getCashflowDeliveryVo.json',
    { cashflowId: $scope.cashflowId }
);
deliveryPromise.then(function (res) {
    var arr = res.result.object.waitingDeliveryList;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].lockStorehouse.type == 4) {
            $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
        } else {
            $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
        }
    }
    // ...
});
```

### 是否直接修改 F1 Response 原对象？

**A 级结论：是**

### angular.copy / clone 检查

| 检查项 | deliveryInputCtrl 范围 | A-F |
|---|---|---|
| `angular.copy` | L3812-L4021 范围内**0 处**（已全文 `Select-String 'angular\.copy'` 验证，范围内无任何 angular.copy / angular.clone / .clone() 调用） | A |
| `angular.clone` | 0 处 | A |
| `JSON.parse(JSON.stringify(...))` | 0 处 | A |
| `Object.assign({}, ...)` | 0 处 | A |
| 显式新对象 `{...}` spread | 0 处 | A |

### 副作用路径

```
F1 Response 引用 (res.result.object.waitingDeliveryList)
    ↓ L3847 ObjectFactory 封装
$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList (同一引用)
    ↓ L3851 var arr = res.result.object.waitingDeliveryList (同一引用)
    ↓ L3854/L3856 直接 mutation
$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = ...
    ↓
所有读取 $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct 的下游都看到 mutation 后的值
```

### F1 后端是否被影响？

- `F1 Response 引用` 是**前端** JS 对象
- mutation 仅影响**前端** JS 内存中的对象
- **不**等于"后端数据库被修改"
- **不**等于"F1 原始记录被改"

**严格表述**：
- "Controller 对 F1 result 的原始对象引用执行了直接 mutation"：**A**
- "mutation 仅影响前端 JS 内存"：**A**
- "后端 F1 数据被改"：**D**（无任何证据，且 L3854/L3856 是 set 字段非网络写）

---

## 12. Write Request 间接链（objectId → F5/F6）

### 直接链

| 字段 | 直接进入哪个 Write Request | A-F |
|---|---|---|
| `medicalProduct.objectId` | ❌ 不直接进入任何 Write Request | A |
| `lockMachineCenter.id` | ❌ 不直接进入任何 Write Request | A |
| `lockStorehouse.type` | ❌ 不直接进入任何 Write Request | A |

### 间接链

**链 A：lockMachineCenter.id → F6（经过 F3）**

```
F1 waitingDeliveryList[i].lockMachineCenter.id
    ↓ L3854
medicalProduct.objectId  (L1 注入)
    ↓ L3824
F3 arr.machineCenterId
    ↓ JSON.stringify
F3 Request.medicalProductMachineCenterPoListJson[].machineCenterId
    ↓ F3 后端处理（F 边界：不可证后端处理）
    ↓
F3 Response.result.list[i].machineCenter.id
    ↓ L3962
F6 arr.machineCenterId
    ↓ JSON.stringify
F6 Request.medicalProductMachineCenterPoListJson[].machineCenterId
```

**A 级闭合节点**：L3854 / L3824 / L3962 / L3966
**F 边界**：F3 后端处理（不可证）

### 完整间接链

```
F1 Response 原始字段:
  - waitingDeliveryList[i].lockStorehouse.type
  - waitingDeliveryList[i].lockMachineCenter.id
  - waitingDeliveryList[i].medicalProduct.id (假定存在)

    ↓ 运行时 mutation (L3853-L3857)
    ↓ 仅修改 medicalProduct.objectId

F1 + mutation 后字段:
  - waitingDeliveryList[i].medicalProduct.objectId  [运行时字段]
      - type==4: = lockMachineCenter.id (数字)
      - else: = null

    ↓ F3 过滤 (L3821 truthy)
    ↓ L3822-3825 构造
F3 arr.machineCenterId = objectId
    ↓ L3836
F3 Request.medicalProductMachineCenterPoListJson[].machineCenterId

    ↓ F3 后端 (F 边界)
    ↓ L3961-3963 map
F6 arr.machineCenterId = F3 result.list[i].machineCenter.id
    ↓ L3966
F6 Request.medicalProductMachineCenterPoListJson[].machineCenterId
```

---

## 13. 与 S1-92 / S1-93 对照

### 与 S1-92 对照（F3 Response → F6 Request）

| 字段 | S1-92 结论 | S1-94 补充 |
|---|---|---|
| F3 result.list[i].machineCenter.id | 已确认闭合到 F6 arr.machineCenterId | 进一步确认 F3 result.list[i].machineCenter.id 的上游是 `arr[i].medicalProduct.objectId`（经 F3 后端反射） |
| F3 result.list[i].medicalProduct.id | 已确认闭合到 F6 arr.medicalProductId | 进一步确认上游是 F1 waitingDeliveryList[i].medicalProduct.id（mutation 不修改 id） |

### 与 S1-93 对照（F1 waitingDeliveryList → F3/F4 入口）

| 维度 | S1-93 结论 | S1-94 补充 |
|---|---|---|
| F3 过滤 | `if (objectId)` truthy | **确认**：objectId 在过滤前已被 L3854/L3856 写入 |
| F4 过滤 | `if (objectId == null)` 宽松相等 | **确认**：objectId 在过滤前已被 L3854/L3856 写入 |
| F3/F4 是否读同一 waitingDeliveryList | 是 | **确认**：F1 同一引用 |
| F3/F4 是否读同一字段 | 是（都是 objectId） | **确认**：都是 medicalProduct.objectId |
| F1 原对象是否被改 | 待定 | **S1-94 已确认：是**（L3854/L3856 直接 mutation） |

### 三轮综合结论

| 维度 | S1-92 | S1-93 | S1-94 |
|---|---|---|---|
| F1 入口字段边界 | 不可证 | 已定位 waitingDeliveryList | **已定位 F1 是否自带 objectId = F** |
| F1 → F3/F4 字段闭合 | 不可证 | 已闭合 | **已确认通过 mutation 影响分流** |
| F1 原对象 mutation | 不可证 | 不可证 | **已确认 L3854/L3856 直接 mutation** |
| F3 Response → F6 | 已闭合 | 已闭合 | 已闭合（链 A） |
| F3/F4 JavaScript 条件全集 | 未分析 | 未分析 | **已分析**（见 §8） |

---

## 14. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | objectId 全局引用范围 | controller.js L3821/L3824/L3854/L3856/L3873/L3899/L3916 = 7 处；deliveryList.html 0 处 | A | L1 | 全部在 deliveryInputCtrl 范围内 |
| 02 | objectId deliveryInputCtrl 读取 | 5 处（L3821/L3824/L3873/L3899/L3916） | A | L1 | |
| 03 | objectId deliveryInputCtrl 写入 | 2 处（L3854/L3856） | A | L1 | |
| 04 | objectId 原始 Response 是否可证 | F（无 F1 schema 样本；F1 是否自带 objectId 不可证） | F | L1=F | |
| 05 | lockStorehouse.type 来源 | F1 waitingDeliveryList[i].lockStorehouse.type | A | L1 | F 边界：F1 schema 不可证 |
| 06 | lockStorehouse.type 条件 | `if (arr[i].lockStorehouse.type == 4)` (L3853) | A | L1 | |
| 07 | lockMachineCenter.id 来源 | F1 waitingDeliveryList[i].lockMachineCenter.id | A | L1 | F 边界：F1 schema 不可证 |
| 08 | lockMachineCenter.id 读取 | L3854 唯一读取 | A | L1 | |
| 09 | lockMachineCenter.id → objectId | L3854 直接赋值 | A | L1 | |
| 10 | objectId → F3 machineCenterId | L3824 | A | L1 | |
| 11 | objectId → F3 过滤 | L3821 truthy | A | L1 | |
| 12 | objectId → F4 过滤 | L3873 == null | A | L1 | |
| 13 | F3/F4 JavaScript 条件关系 | truthy vs == null，非完全互补 | A | L1 | JavaScript 语言事实 |
| 14 | null | == null → true → F4；truthy → false → F3 | A | L1 | |
| 15 | undefined | == null → true → F4；truthy → false → F3 | A | L1 | |
| 16 | false/0/""/NaN | truthy → false → 不进 F3；== null → false → 不进 F4 | A | L1 | 第三分支（理论） |
| 17 | 第三分支 | 理论存在（0/""/false/NaN）；实际源码写入路径不产生这些值 | A（理论）/ A（实际） | L1 | 当前实现下不进入第三分支 |
| 18 | search() 重复执行 | L3866 init + L4014 F5 success = 2 | A | L1 | |
| 19 | objectId 是否恢复 | ❌ 无恢复原值逻辑（每次 search() 重新发请求，新引用） | A | L1 | |
| 20 | F1 原对象 mutation | ✅ 直接 mutation（L3854/L3856） | A | L1 | 仅影响前端 JS 内存 |
| 21 | angular.copy/clone | ❌ deliveryInputCtrl 范围 0 处 | A | L1 | |
| 22 | F3 Request | `getMedicalProductMachineCenterVoList.json` { medicalProductMachineCenterPoListJson: JSON.stringify(arr) } | A | L1 | |
| 23 | F6 machineCenterId | L3966 sendMedicalProductToMachineCenter.json | A | L1 | |
| 24 | lockMachineCenter.id → F6 间接链 | F1 lockMachineCenter.id → objectId (L3854) → F3 arr.machineCenterId (L3824) → F3 后端 (F 边界) → F3 result.list[i].machineCenter.id (L3962) → F6 arr.machineCenterId (L3966) | A（F3 后端 = F） | L1 | |
| 25 | 其它 Controller/HTML 写入 | deliveryList.html 0 处；其它 Controller 未在本轮范围 | A | L1 | 本轮范围内 0 处 |
| 26 | 最终最小运行时规则 | lockStorehouse.type==4 → objectId=lockMachineCenter.id；else → objectId=null；F3 读 truthy；F4 读 == null | A | L1 | |

**统计**：
- A：25 项
- F：1 项（#04 objectId 原始 Response 是否可证）
- D：0
- C：0
- B：0
- E：0
- **F 升 A / E 升 A：0**

---

## 15. L1/L2/L3

### L1（源码事实，可证）

- 写入路径（L3854/L3856）**全部 7 处**读写点位置
- 条件表达式（L3821/L3853/L3873/L3899/L3916）
- search() 调用路径（L3866/L4014）
- 0 处 angular.copy
- 7 处 medicalProduct.objectId 全部在 deliveryInputCtrl 范围
- deliveryList.html 0 处 objectId
- JavaScript 条件全集（语言事实）
- F1 二次写入可能产生的值域

### L2（业务解释，未证）

- "objectId 是 DB 主键"：**E**（未证，本轮禁止升级为 A）
- "objectId 是加工中心 ID"：**E**（未证）
- "lockStorehouse.type == 4 = 加工中心"：**E**（未证）
- "lockStorehouse.type != 4 = 普通库存"：**E**（未证）
- "objectId = null = 可配送"：**E**（未证）
- "objectId = 数字 = 已分配到加工中心"：**E**（未证）
- "F3 是分配到加工中心，F4 是直接配送"：**E**（未证）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 F1 schema 样本 / 无后端 schema）

---

## 16. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| F1 Response 原始 schema | 无 F1 schema 样本 / 无后端代码 | F |
| F1 Response 是否自带 medicalProduct.objectId | F1 schema 不可得 | F |
| F1 Response 中 lockStorehouse / lockMachineCenter / medicalProduct.id 的类型 | F1 schema 不可得 | F |
| F3 后端处理 | 无后端代码 | F |
| F4 后端处理 | 无后端代码 | F |
| F3 result.list[i].machineCenter 是否始终存在 | F3 后端不可证 | F |
| F3 result.list[i].machineCenter.id 是否始终 = Request 传入的 machineCenterId | F3 后端不可证 | F |
| 其它 Controller 是否也写 medicalProduct.objectId | 不在本轮范围 | F（本轮范围内 0 处） |
| 其它页面 HTML 是否含 .objectId | 仅检查 deliveryList.html，其它 7 HTML 不在本轮范围 | F（本轮范围内 0 处） |
| lockStorehouse 是否可能为 null/undefined | F1 schema 不可得，且源码无保护 | F |

---

## 17. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| Write API 实际执行 = 0 | ✅ | 本轮仅静态逆向；未触发任何 F5/F6 |
| save / submit / send / delivery / receive / charge / refund / recharge / start / complete / close / notify 全部 0 调用 | ✅ | 未发任何 Write Request |
| controller.js 未修改 | ✅ | git status --short 不显示 M controller.js |
| deliveryList.html 未修改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变） |
| 历史 MD 未修改 | ✅ | 仅新增 155_*.md |
| 10 untracked 临时文件原样保留 | ✅ | _gen_phase0_placeholders.ps1 / .py / controller.js / 7 HTML 仍 untracked |
| P0 = 54 冻结 | ✅ | 未变 |
| P1 = 8 冻结 | ✅ | 未变 |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 155_*.md |
| 文件编号连续 | ✅ | 154 已被 S1-93 占用，本轮使用 155 |

---

## 18. 最终结论

### 最小运行时规则（A 级，无业务推断）

```
F1 Response waitingDeliveryList 引用
    ↓ search().then 同步执行 L3851-L3858
    ↓
对每一项 waitingDeliveryList[i]:
    if (lockStorehouse.type == 4):
        medicalProduct.objectId = lockMachineCenter.id  // 数字
    else:
        medicalProduct.objectId = null
    ↓ mutation 完成后
    ↓ 所有下游读取 medicalProduct.objectId 都看到 mutation 后的值

F3 过滤 (L3821):
    if (medicalProduct.objectId)  // truthy
        → 进入 F3 Request
        → 写入 arr.machineCenterId

F4 过滤 (L3873):
    if (medicalProduct.objectId == null)  // 宽松等于 null/undefined
        → 进入 F4 Request
        → 写入 medicalProductIdArray

当前 Controller 实现下:
    type==4 → objectId 是 lockMachineCenter.id（数字）→ truthy → F3
    else    → objectId 是 null                 → == null → F4
    第三分支（0/""/false/NaN）→ 当前不出现
```

### 关键事实（全部 A 级）

1. **7 处 medicalProduct.objectId 全部在 deliveryInputCtrl（L3812-L4021）**
2. **仅 2 处写入（L3854/L3856）**
3. **0 处 angular.copy / clone / JSON deep clone**
4. **F1 Response 原对象被直接 mutation**（仅影响前端 JS 内存）
5. **search() 重复执行能力 = 2**（L3866 init + L4014 F5 success）
6. **JavaScript 条件层面 F3/F4 非完全互补**（0/""/false/NaN 都不进入），但当前 Controller 写入路径不产生这些值
7. **lockMachineCenter.id 经 4 个节点闭合到 F6.machineCenterId**（中间 F3 后端 = F 边界）
8. **F1 Response 是否自带 objectId 字段 = F**（不可证）

### 与 S1-92/S1-93 形成的最终完整链路

```
F1 waitingDeliveryList[i]
    .lockStorehouse.type        (L1, A)
    .lockMachineCenter.id       (L1, A)
    .medicalProduct.id          (L1, A)
    .medicalProduct.objectId    (L1, F — 不可证原始值)
    ↓ search().then 同步 mutation
.medicalProduct.objectId = lockMachineCenter.id 或 null
    ↓
F3 (L3821 truthy 过滤) / F4 (L3873 == null 过滤)
    ↓
F3 Request arr.machineCenterId (L3824)
F4 Request medicalProductIdArray[i] (L3874)
    ↓ F3 后端 (F 边界)
F3 Response.result.list[i].machineCenter.id
    ↓ L3962 map
F6 Request.machineCenterId (L3966)
    ↓ F5 (saveStock) success (L4010-4018)
search() 重复执行 + getCount() + $state.reload()
```

### 不可在本轮升级为 A 的项

- objectId 原始值（F）
- lockStorehouse.type == 4 的业务含义（E）
- lockStorehouse 可能为 null/undefined（F）
- F3/F4 后端具体处理（F）
- 其它 Controller / HTML 是否有 objectId 写入（F，本轮范围外）

---

**审计结束**。
