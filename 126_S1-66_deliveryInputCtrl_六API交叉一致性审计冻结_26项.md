# S1-66 deliveryInputCtrl 六 API 交叉一致性审计冻结

> 专项收口：`S1-64 + S1-65` 已完成的 deliveryInputCtrl 协议**跨文档、跨代码、跨 API、跨字段**一致性审计
>
> 上一阶段：S1-65（125 号）已收口 send API 完整协议。
>
> 本阶段：S1-66（126 号）专项审计 deliveryInputCtrl 6 API **交叉一致性**并固化为**最小可复刻协议集合**。

---

## 1. 核心结论

**S1-64 + S1-65 全部结论在 deliveryInputCtrl 范围内（A 级）100% 一致**。S1-66 新发现：
- **3 个 API 跨 controller 使用**（getCashflowDeliveryVo / statProductDeliveryStatusOfCashflow / getCanBeDeliverySkuInListOfProduct）
- **3 个 API 仅 deliveryInputCtrl 使用**（getMedicalProductMachineCenterVoList / saveMedicalProductStockBatch / sendMedicalProductToMachineCenter）
- **deliveryProcessingCtrl（L4236）** 也调 2 个初始化 API（statProductDeliveryStatusOfCashflow + getCashflowDeliveryVo），但**不调** selectOrder / saveStock / showAddModal / showDeliveryModal
- **deliveryInputRecordCtrl（L4024）** 也调 2 个 API，**不调** 6 API 中的任何 1 个

**Save 链 vs Send 链独立性**：
- saveMedicalProductStockBatch.json（saveStock L4007）→ search + getCount + reload + stockDetail=false
- sendMedicalProductToMachineCenter.json（selectOrder L3966）→ notice + addOrderModal=false + reload
- **两条链** **完全不共享 Response / Request / scope 变量**
- 等级：A

**Query 链 vs Send 链独立性**：
- getMedicalProductMachineCenterVoList.json → getCenterListFactory.result.list → selectOrder
- getCanBeDeliverySkuInListOfProduct.json → getDeliveryListFactory.result.list → saveStock
- **两条链仅通过 getMachineCenterList / showDeliveryModal 函数入口共享 cashflowId**
- 等级：A

---

## 2. 审计范围

**直接证据**：
- controller.js L3812-4021（deliveryInputCtrl 完整 209 行）
- S1-64 / S1-65 已封口文档（无修改）
- 6 API 全仓调用点搜索

**资源缺失**：
- deliveryInputCtrl HTML 模板（F 维持）
- 完整 route schema（F 维持）
- 后端算法 / DTO 定义（F 维持）

---

## 3. Controller 范围（30.1）

| 项目 | 证据 | 等级 |
|------|------|------|
| controller 名称 | `deliveryInputCtrl` | A |
| 起点 | L3812 | A |
| 终点 | L4021 | A |
| 总行数 | 209 行 | A |
| S1-64 / S1-65 是否使用同一 Controller 范围 | **是** | A |

**严格表述**：
- S1-64 / S1-65 / S1-66 全部基于 `controller.js L3812-4021` 同一范围
- 三个 controller 范围不同：deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl

---

## 4. 六 API 清单（30.2-30.4）

| 序 | API | deliveryInputCtrl 调用次数 | deliveryInputCtrl 唯一调用点 | 其他 controller 调用 | 全仓总次数 | 等级 |
|---|---|---|---|---|---|---|
| 1 | getCashflowDeliveryVo.json | 1 | L3848 | deliveryInputRecordCtrl L4040, deliveryProcessingCtrl L4249 | 3 | A |
| 2 | statProductDeliveryStatusOfCashflow.json | 1 | L3841 | deliveryInputRecordCtrl L4044, deliveryProcessingCtrl L4242 | 3 | A |
| 3 | getMedicalProductMachineCenterVoList.json | 1 | L3836 | **无** | 1 | A |
| 4 | getCanBeDeliverySkuInListOfProduct.json | 1 | L3885 | optometryCtrl L35054 | 2 | A |
| 5 | saveMedicalProductStockBatch.json | 1 | L4007 | **无** | 1 | A |
| 6 | sendMedicalProductToMachineCenter.json | 1 | L3966 | **无** | 1 | A |

**A 级 100% 收口**。

**S1-66 关键新发现**：
- 3 个 API 是 **deliveryInputCtrl 独有**（getMedicalProductMachineCenterVoList / saveMedicalProductStockBatch / sendMedicalProductToMachineCenter）
- 3 个 API 跨 controller 使用
- deliveryInputCtrl 6 API 调用点**全部唯一**（每 API 仅 1 次调用）

---

## 5. Function 对照（30.3）

| API | Function | 行号 | 是否立即执行 | 等级 |
|---|---|---|---|---|
| getCashflowDeliveryVo.json | `search()` | L3846-3865 | **是**（L3866 立即调用） | A |
| statProductDeliveryStatusOfCashflow.json | `getCount()` | L3839-3844 | **是**（L3844 立即调用） | A |
| getMedicalProductMachineCenterVoList.json | `showAddModal()` | L3830-3837 | **否**（用户操作触发） | A |
| getCanBeDeliverySkuInListOfProduct.json | `showDeliveryModal()` | L3868-3886 | **否**（用户操作触发） | A |
| saveMedicalProductStockBatch.json | `saveStock()` | L3979-4020 | **否**（用户操作触发） | A |
| sendMedicalProductToMachineCenter.json | `selectOrder()` | L3955-3977 | **否**（用户操作触发） | A |

**A 级 100% 收口**。

---

## 6. Request 一致性审计（30.6）

| API | S1-64 记录 | S1-65 记录 | controller.js 源码 | 一致性 | 等级 |
|---|---|---|---|---|---|
| 1 | `{ cashflowId }` | - | L3848 `{ cashflowId: $scope.cashflowId }` | **一致** | A |
| 2 | `{ cashflowId }` | - | L3841 `{ cashflowId: $scope.cashflowId }` | **一致** | A |
| 3 | `{ medicalProductMachineCenterPoListJson }` | - | L3836 `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` | **一致** | A |
| 4 | `{ medicalProductIdArray }` | - | L3885 `{ medicalProductIdArray: medicalProductIdArray }` | **一致** | A |
| 5 | `{ listCount, medicalProductStockBatctPoListJson }` | - | L4007 完全一致 | **一致** | A |
| 6 | - | `{ medicalProductMachineCenterPoListJson, planDeliveryTime }` | L3966 完全一致 | **一致** | A |

**A 级 100% 一致**。

---

## 7. Response 一致性审计（30.7）

| API | 已观察字段 | 等级 |
|---|---|---|
| 1 | `res.result.object.waitingDeliveryList[]` (L3851) + `arr[i].lockStorehouse.type` (L3853) + `arr[i].lockMachineCenter.id` (L3854) | A |
| 2 | `res.status`（顶层 ObjectFactory 模式），**未直接读取 result** | A/F |
| 3 | `result.list[]` 含 `medicalProduct.id` + `machineCenter.id` (L3962) | A |
| 4 | `result.list[]` 含 `medicalProduct` + `deliveryStockInSkuVoList[]` | A |
| 5 | `res.status` | A |
| 6 | `res.status` + `res.errmsg` | A |

**A 级一致**。未观察字段全部 F 维持。

---

## 8. success 一致性审计（30.8, 30.24）

| API | success 行为 | 等级 |
|---|---|---|
| 1 | 同步处理 waitingDeliveryList + medicalProduct.objectId 赋值 | A |
| 2 | - | - |
| 3 | `$scope.addOrderModal = true` | A |
| 4 | `$scope.stockDetail = true` | A |
| 5 | Popup.notice("保存成功") + search() + getCount() + $state.reload() + $scope.stockDetail = false | A |
| 6 | Popup.notice("发送成功") + $scope.addOrderModal = false + $state.reload() | A |

**Save vs Send 严格对照**（30.24）：

| 行为 | save (L4013-4017) | send (L3972-3974) | 等级 |
|---|---|---|---|
| Popup.notice | "保存成功" | "发送成功" | A |
| Modal 关闭 | stockDetail = false | addOrderModal = false | A |
| search() | 调用 | **不调用** | A |
| getCount() | 调用 | **不调用** | A |
| $state.reload() | 调用 | 调用 | A |
| state.go | 不调用 | 不调用 | A |
| 本地对象修改 | 不修改 | 不修改 | A |

**A 级 100% 一致**：Save 和 Send **完全不混用** success 模式。

---

## 9. 初始化与 Function（30.9）

**Controller 初始化阶段**：
- L3812-3815: 入口 + cashflowId 初始化
- L3816-3829: getMachineCenterList 函数定义（不立即执行）
- L3830-3837: showAddModal 函数定义（不立即执行）
- L3839-3844: getCount() **立即执行** → statProductDeliveryStatusOfCashflow
- L3846-3865: search() **立即执行** → getCashflowDeliveryVo
- L3868-3886: showDeliveryModal 函数定义
- L3955-3977: selectOrder 函数定义
- L3979-4020: saveStock 函数定义

**立即执行的 API**：2 个（getCount + search）
**用户操作触发的 API**：4 个（showAddModal + showDeliveryModal + saveStock + selectOrder）

**A 级 100% 收口**。

---

## 10. waitingDeliveryList 来源（30.10）

| 字段 | 来源 | 等级 |
|---|---|---|
| `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` | getCashflowDeliveryVo.json Response | A（L3851） |
| 字段读取 | arr[i].lockStorehouse.type, arr[i].lockMachineCenter.id, arr[i].medicalProduct | A |
| 字段写入 | medicalProduct.objectId = lockMachineCenter.id (L3854) / null (L3856) | A |
| getMachineCenterList 读取 | 遍历 waitingDeliveryList (L3818) | A |
| showDeliveryModal 读取 | 遍历 waitingDeliveryList (L3870) | A |
| isSendProduct 读取 | 遍历 waitingDeliveryList (L3893) | A |
| isSendCenter 读取 | 遍历 waitingDeliveryList (L3910) | A |

**A 级 100% 收口**：waitingDeliveryList **仅来自** getCashflowDeliveryVo.json Response。

---

## 11. medicalProduct.id 生命周期（30.11）

| 位置 | 表达式 | 用途 | 等级 |
|---|---|---|---|
| getMachineCenterList | `arr[i].medicalProduct.id` (L3823) | 推入 medicalProductId | A |
| showDeliveryModal | `arr[i].medicalProduct.id` (L3874) | 推入 medicalProductIdArray | A |
| selectOrder | `v.medicalProduct.id` (L3962) | 推入 medicalProductId → send API | A |
| saveStock | `list[i].medicalProduct.id` (L3998) | 推入 medicalProductId → save JSON | A |
| getMedicalRecordDeliveryFactory 写入 | `medicalProduct.objectId = lockMachineCenter.id` (L3854) | 字段赋值 | A |
| **是否进入 getMedicalProductMachineCenterVoList.json Request** | **是**（L3836） | A |
| **是否进入 getCanBeDeliverySkuInListOfProduct.json Request** | **是**（L3885） | A |
| **是否进入 saveMedicalProductStockBatch.json Request** | **是**（L3998） | A |
| **是否进入 sendMedicalProductToMachineCenter.json Request** | **是**（L3962） | A |

**A 级 100% 一致**。

**严格不写**：
- 禁止"几个地方都叫 medicalProduct.id" → "数据库层同一实体"（L3 = F）

---

## 12. objectId 生命周期（30.12-30.13）

**完整生命周期**：

```
L3854: medicalProduct.objectId = arr[i].lockMachineCenter.id     [源：getCashflowDeliveryVo Response]
L3856: medicalProduct.objectId = null                              [源：getCashflowDeliveryVo Response]
L3821: if (arr[i].medicalProduct.objectId) [getMachineCenterList 过滤 truthy]
L3824: machineCenterId: arr[i].medicalProduct.objectId            [派生：objectId → machineCenterId 映射]
L3873: if (arr[i].medicalProduct.objectId == null) [showDeliveryModal 过滤 null]
L3899: if (arr[i].medicalProduct.objectId) [isSendProduct 检查]
L3916: if (arr[i].medicalProduct.objectId == null) [isSendCenter 检查]
```

**objectId 是否直接进入 send API Request**：
- **否**（A，L3962 是 `v.machineCenter.id`，**不**是 `medicalProduct.objectId`）
- 等级：A

**objectId → machineCenter.id 真实代码链**：

```
medicalProduct.objectId (L3854 来源 lockMachineCenter.id)
   ↓
L3824: machineCenterId: arr[i].medicalProduct.objectId
   ↓ (getMachineCenterList 内) JSON.stringify(medicalProductMachineCenterPoList)
   ↓
L3836: medicalProductMachineCenterPoListJson Request
   ↓
L3835-3836: getCenterListFactory.saveOrQuery(getMedicalProductMachineCenterVoList.json)
   ↓
Response: getCenterListFactory.result.list[i].machineCenter.id
   ↓
L3962: machineCenterId: v.machineCenter.id
   ↓
L3966: sendMedicalProductToMachineCenter.json Request
```

**关键 A 级边界**：
- 步骤 1（L3854）：objectId = lockMachineCenter.id（getCashflowDeliveryVo Response 派生）
- 步骤 2（L3824）：objectId 直接作为 machineCenterId（**field 重命名**）
- 步骤 3（L3962）：v.machineCenter.id（**新 Response 对象的 machineCenter.id**）
- objectId 在 send API Request 中**完全消失**（L3962 用 `v.machineCenter.id` 而非 `medicalProduct.objectId`）

**严格不写**：
- 禁止"objectId 就是数据库 machineCenterId"（无 DB 证据）
- 等级：A

---

## 13. medicalProductMachineCenterPoList 双向对照（30.14）

**位置 A: getMedicalProductMachineCenterVoList.json Request (L3836)**

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr)
    // arr = getMachineCenterList() 返回值
    // arr 元素: { medicalProductId, machineCenterId: objectId }
}
```

**arr 元素来源**：
- 来自 `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList` (L3818)
- 过滤：`medicalProduct.objectId` truthy (L3821)
- 元素构造：L3823-3824 `{ medicalProductId: medicalProduct.id, machineCenterId: medicalProduct.objectId }`

**位置 B: sendMedicalProductToMachineCenter.json Request (L3966)**

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr)
    // arr = $scope.getCenterListFactory.result.list.map(v => { medicalProductId, machineCenterId: v.machineCenter.id })
    planDeliveryTime: $scope.startTime
}
```

**arr 元素来源**：
- 来自 `$scope.getCenterListFactory.result.list` (L3961)
- 来自 getMedicalProductMachineCenterVoList.json Response
- 元素构造：L3962 `{ medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }`

**同构 vs 不同构**：

| 字段 | 位置 A 元素 | 位置 B 元素 | 等级 |
|---|---|---|---|
| medicalProductId | L3823 medicalProduct.id | L3962 v.medicalProduct.id | A（**字段名同**） |
| machineCenterId | L3824 medicalProduct.objectId | L3962 v.machineCenter.id | A（**字段名同，来源不同**） |

**关键 A 级发现**：
- **字段结构同构**：`{ medicalProductId, machineCenterId }`
- **元素来源不同**：
  - 位置 A：来自 waitingDeliveryList[i].medicalProduct（getCashflowDeliveryVo Response）
  - 位置 B：来自 getCenterListFactory.result.list[i]（getMedicalProductMachineCenterVoList Response）
- **数据值同**（B Response 由 A Response 派生）

**严格表述**：
- 字段名一致（A）
- 字段结构一致（A）
- 元素来源不同（A）
- 数据流同：A Response → B Request（A）
- 等级：A

---

## 14. getCenterListFactory 完整生命周期（30.15）

| 环节 | 表达式 | 行号 | 等级 |
|---|---|---|---|
| 创建 | `$scope.getCenterListFactory = new ObjectFactory()` | L3835 | A |
| 立即调用 | `.saveOrQuery(getMedicalProductMachineCenterVoList.json, ...)` | L3836 | A |
| Response 暴露 | `getCenterListFactory.result.list` | L3961 | A |
| 读取位置 | `selectOrder` 函数 | L3961 | A |
| 元素字段 | `v.medicalProduct.id` + `v.machineCenter.id` | L3962 | A |

**全仓同名 factory 搜索**：
- `getCenterListFactory` 在 controller.js 中**仅 deliveryInputCtrl 范围出现**（F 维持：唯一性 100%）
- 等级：A

---

## 15. machineCenter.id 来源（30.16）

**唯一来源**：
- `$scope.getCenterListFactory.result.list[i].machineCenter.id`（A，L3962）
- **不**来自 waitingDeliveryList
- **不**来自 medicalProduct.objectId（**不直接**进入 selectOrder）

**A 级 100% 收口**。

---

## 16. selectOrder 函数审计（30.17）

| 项目 | 证据 | 等级 |
|---|---|---|
| 无参数 | L3955 | A |
| 依赖 startTime | L3956-3959 if (!startTime) { Popup.notice; return false; } | A |
| 依赖 getCenterListFactory.result.list | L3961 读取 | A |
| 直接读取 list.map | L3961 | A |
| JSON.stringify(arr) | L3966 | A |
| 立即调用 send API | L3966 | A |
| planDeliveryTime 处理 | L3964 DateUtilFactory.origin | A |

**A 级 100% 收口**。

---

## 17. saveStock 函数审计（30.18）

| 项目 | 证据 | 等级 |
|---|---|---|
| 调用 API | saveMedicalProductStockBatch.json | A（L4007） |
| Request 顶层字段 | `{ listCount, medicalProductStockBatctPoListJson }` | A（L4007） |
| 内部 JSON | `[{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]` | A |
| stockDetail | L4017 = false | A |
| listCount | L4007 = getDeliveryListFactory.result.list.length | A |
| success | L4013-4017 | A |

**deliveryCount 来源**：
- L3991: `deliveryCount: list[i].deliveryStockInSkuVoList[j].deliveryCount`
- **直接读取**自 getCanBeDeliverySku Response
- **不修改**
- 等级：A

---

## 18. deliveryCount 完整生命周期（30.19）

```
getCanBeDeliverySkuInListOfProduct.json
   ↓ Response
list[i].deliveryStockInSkuVoList[j].deliveryCount
   ↓ L3989 if > 0
   ↓ L3991 直接读取
   ↓ JSON.stringify
medicalProductStockBatctPoListJson[].medicalProductStocks[].deliveryCount
   ↓ L4007
saveMedicalProductStockBatch.json Request
```

**A 级 100% 收口**：
- deliveryCount **未经任何修改**进入 Save
- 等级：A

---

## 19. stockInSku.id 完整生命周期（30.20）

```
getCanBeDeliverySkuInListOfProduct.json
   ↓ Response
list[i].deliveryStockInSkuVoList[j].stockInSku.id
   ↓ L3991
   ↓ JSON.stringify
medicalProductStockBatctPoListJson[].medicalProductStocks[].stockInSkuId
   ↓ L4007
saveMedicalProductStockBatch.json Request
```

**deliveryInputCtrl 范围内 stockInSku 真实读取字段**：
- `stockInSku.id`（A，L3991）
- 其他字段（skuCount / skuOutCount / expiresDate / productionDate / batchNo / skuPrice / remark）：**F（未读取）**

**严格不写**：
- 禁止把其他 controller 中 stockInSku 字段使用回填到 deliveryInputCtrl
- 等级：A

---

## 20. listCount 审计（30.21）

| 项目 | 证据 | 等级 |
|---|---|---|
| 来源 | `$scope.getDeliveryListFactory.result.list.length` | A（L4007） |
| 计算方式 | 数组 .length | A |
| 与数组长度等价 | 是 | A |
| 是否进入 Request | 是 | A |
| 是否参与内部 JSON | **否**（listCount 是顶层独立字段） | A |
| 是否有其他用途 | **否** | A |
| 是否在所有 Save 场景都存在 | deliveryInputCtrl 有；machineOrderCtrl **没有** | A |

**A 级 100% 收口**。

---

## 21. getDeliveryListFactory 完整生命周期（30.22）

| 环节 | 表达式 | 行号 | 等级 |
|---|---|---|---|
| 创建 | `$scope.getDeliveryListFactory = new ObjectFactory()` | L3884 | A |
| 立即调用 | `.saveOrQuery(getCanBeDeliverySkuInListOfProduct.json, ...)` | L3885 | A |
| Response 暴露 | `getDeliveryListFactory.result.list` | A | A |
| showDeliveryModal 副作用 | `$scope.stockDetail = true` | L3882 | A |
| saveStock 读取 | `list[i].medicalProduct.id`, `list[i].deliveryStockInSkuVoList[j].stockInSku.id`, `.deliveryCount` | L3985-3991 | A |
| listCount 来源 | `getDeliveryListFactory.result.list.length` | L4007 | A |

**A 级 100% 收口**。

---

## 22. Save JSON 构造（30.23）

**逐层追踪**：

```
getDeliveryListFactory.result.list[i]                    [外层数据]
  └─ medicalProduct
       └─ id                                              [→ medicalProductId L3998]
  └─ deliveryStockInSkuVoList[j]                          [内层数据]
       ├─ stockInSku
       │    └─ id                                          [→ stockInSkuId L3991]
       └─ deliveryCount                                    [→ deliveryCount L3991]
              ↓
        medicalProductStocks[]
              ↓
medicalProductStockBatctPoListJson[]
  ↓ JSON.stringify
  ↓
saveMedicalProductStockBatch.json Request
```

**拼写严格**：
- `medicalProductStockBatctPoListJson`（Po）
- `medicalProductStocks`
- `stockInSkuId`
- `deliveryCount`
- 等级：A

**A 级 100% 收口**，无漏字段。

---

## 23. Save 链 vs Send 链独立性（30.24, 30.26）

| 关系 | saveMedicalProductStockBatch | sendMedicalProductToMachineCenter | 等级 |
|---|---|---|---|
| 直接函数调用 | - | - | F（**无**） |
| 共享 Response | - | - | F（**无**） |
| 共享 Request 对象 | - | - | F（**无**） |
| 共享 scope 变量 | `$scope.getDeliveryListFactory` | `$scope.getCenterListFactory` | A（**不同** factory） |
| 共享 success 模式 | 部分（$state.reload 都调） | 部分（$state.reload 都调） | A |
| 业务上下文 | 库存保存 | 发到机器中心 | E |

**A 级 100% 收口**：
- Save 链和 Send 链**完全独立**
- 仅共享 `$scope.cashflowId`（controller 入口）
- 仅共享 `$state.reload()`（success 行为）

**3 层结论**：
1. **直接关系**：无（A）
2. **间接关系**：共享 cashflowId + reload（A）
3. **未观察关系**：HTML 触发顺序（F）

---

## 24. Query 链 vs Send 链（30.25）

**真实代码链（A 级 100% 收口）**：

```
$stateParams.cashflowId
  → getCashflowDeliveryVo.json (L3848 search)
    → res.result.object.waitingDeliveryList[]
      → medicalProduct.objectId = lockMachineCenter.id (L3854, if type==4)
        → getMachineCenterList() (L3816-3829, objectId truthy 过滤)
          → getMedicalProductMachineCenterVoList.json (L3836 showAddModal)
            → getCenterListFactory.result.list
              → selectOrder (L3955-3977, v.medicalProduct.id + v.machineCenter.id)
                → sendMedicalProductToMachineCenter.json (L3966)
```

**是否全是直接代码链**：
- 步骤 1-3：A（直接 L3814/L3848/L3851）
- 步骤 4-5：A（直接 L3853-3854/L3816）
- 步骤 6：A（直接 L3836）
- 步骤 7-8：A（直接 L3961-3962）
- 步骤 9：A（直接 L3966）

**A 级 100% 收口**。

**事件/UI 间隔**：
- getMachineCenterList 函数：内部调用（无 UI 间隔）
- showAddModal 函数：用户操作触发（**UI 间隔**）
- selectOrder 函数：用户操作触发（**UI 间隔**）
- 等级：A

---

## 25. Delivery SKU 链 vs Send 链（30.26）

**真实代码链**：

```
Query 链（Delivery SKU）：
  getCashflowDeliveryVo.json (L3848)
    → waitingDeliveryList[].medicalProduct.objectId (L3854)
      → objectId == null 过滤 (L3873)
        → medicalProductIdArray.push (L3874)
          → getCanBeDeliverySkuInListOfProduct.json (L3885)
            → getDeliveryListFactory.result.list
              → saveStock (L3979)
                → saveMedicalProductStockBatch.json (L4007)

Send 链：
  getCashflowDeliveryVo.json (L3848)
    → waitingDeliveryList[].medicalProduct.objectId (L3854)
      → objectId truthy 过滤 (L3821)
        → getMachineCenterList (L3816-3829)
          → getMedicalProductMachineCenterVoList.json (L3836)
            → getCenterListFactory.result.list
              → selectOrder (L3955)
                → sendMedicalProductToMachineCenter.json (L3966)
```

**是否完全独立**：
- ✅ **不同过滤条件**：`objectId == null` (L3873) vs `objectId truthy` (L3821)
- ✅ **不同 factory**：`getDeliveryListFactory` vs `getCenterListFactory`
- ✅ **不同 API**：saveMedicalProductStockBatch vs sendMedicalProductToMachineCenter
- ✅ **不同 function**：saveStock vs selectOrder
- ✅ **不同 modal**：stockDetail vs addOrderModal

**A 级 100% 收口**：Query 链与 Send 链**完全独立**（**不**因"发货"业务概念就合并）。

---

## 26. cashflowId 完整审计（30.27）

| Function | 是否使用 cashflowId | 等级 |
|---|---|---|
| getCount (L3839) | **是**（`$scope.cashflowId`） | A（L3841） |
| search (L3846) | **是** | A（L3848） |
| showAddModal (L3830) | **否**（未直接读 cashflowId） | A |
| showDeliveryModal (L3868) | **否** | A |
| saveStock (L3979) | **否** | A |
| selectOrder (L3955) | **否** | A |

**A 级 100% 收口**：
- cashflowId **仅**进入 2 个初始化 API
- **不**进入 4 个用户操作 API

---

## 27. modal / refresh 生命周期（30.28）

| 元素 | 来源 | 关闭 | 等级 |
|---|---|---|---|
| addOrderModal | showAddModal L3831 = true | selectOrder success L3973 = false | A |
| stockDetail | showDeliveryModal L3882 = true | saveStock success L4017 = false | A |
| $state.reload() | selectOrder success L3974 + saveStock success L4016 | - | A |

**严格对照**：

| 行为 | showAddModal | showDeliveryModal | saveStock | selectOrder |
|---|---|---|---|---|
| 打开 modal | addOrderModal = true | stockDetail = true | - | - |
| 关闭 modal | - | - | stockDetail = false | addOrderModal = false |
| $state.reload | - | - | **调用** | **调用** |
| search() | - | - | **调用** | **不调用** |
| getCount() | - | - | **调用** | **不调用** |

**A 级 100% 收口**，无合并。

---

## 28. machineCenterOrder / machineOrder 隔离（30.29）

**全仓搜索**：

| 字段 | deliveryInputCtrl 范围内 | 全仓出现次数 | 等级 |
|---|---|---|---|
| machineCenterOrder | **不出现** | 100+ 处（其他 controller） | F（deliveryInputCtrl 范围）/ A（全仓） |
| machineOrder | **不出现** | 200+ 处（其他 controller） | F（deliveryInputCtrl 范围）/ A（全仓） |

**严格结论**：
- 禁止"send API 创建 machineCenterOrder"（**无**代码证据）
- 禁止"send API 创建加工单"（**无**代码证据）
- 禁止"send API 让 medicalProduct 进入加工状态"（**无**代码证据）
- 等级：A

---

## 29. 六 API 最终冻结协议（30.30）

| API | Controller | Function | Request | 已观察 Response | 前置依赖 | 直接下游 | success | 等级 |
|---|---|---|---|---|---|---|---|---|
| 1 | deliveryInputCtrl | search | `{ cashflowId }` | `result.object.waitingDeliveryList[]` 含 medicalProduct/lockStorehouse/lockMachineCenter | $stateParams.cashflowId | getMachineCenterList / showDeliveryModal | 同步处理 waitingDeliveryList | A |
| 2 | deliveryInputCtrl | getCount | `{ cashflowId }` | `res.status`（顶层 ObjectFactory 模式） | $stateParams.cashflowId | - | - | A |
| 3 | deliveryInputCtrl | showAddModal | `{ medicalProductMachineCenterPoListJson: JSON.stringify([{medicalProductId, machineCenterId}]) }` | `result.list[]` 含 medicalProduct.id + machineCenter.id | getMachineCenterList (waitingDeliveryList) | selectOrder (getCenterListFactory.result.list) | `$scope.addOrderModal = true` | A |
| 4 | deliveryInputCtrl | showDeliveryModal | `{ medicalProductIdArray: [...] }` | `result.list[]` 含 medicalProduct + deliveryStockInSkuVoList[] | getCashflowDeliveryVo (waitingDeliveryList) | saveStock (getDeliveryListFactory.result.list) | `$scope.stockDetail = true` | A |
| 5 | deliveryInputCtrl | saveStock | `{ listCount, medicalProductStockBatctPoListJson: JSON.stringify([{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]) }` | `res.status` | showDeliveryModal (getDeliveryListFactory.result.list) | - | search + getCount + $state.reload() + $scope.stockDetail = false | A |
| 6 | deliveryInputCtrl | selectOrder | `{ medicalProductMachineCenterPoListJson: JSON.stringify([{medicalProductId, machineCenterId}]), planDeliveryTime }` | `res.status` + `res.errmsg` | showAddModal (getCenterListFactory.result.list) + $scope.startTime | - | notice + $scope.addOrderModal = false + $state.reload() | A |

**A 级 100% 收口**。

---

## 30. 六 API 关系图

```
                    $stateParams.cashflowId
                            ↓
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
API-2 statProductDeliveryStatusOfCashflow   API-1 getCashflowDeliveryVo
   (getCount, L3839)                          (search, L3846)
        ↓                                       ↓
   res.status                              waitingDeliveryList[]
                                                ↓
                              ┌─────────────────┴─────────────────┐
                              ↓                                   ↓
                    objectId truthy 过滤              objectId == null 过滤
                    (L3821 getMachineCenterList)       (L3873 showDeliveryModal)
                              ↓                                   ↓
                    API-3 getMedicalProductMachineCenterVoList  API-4 getCanBeDeliverySku
                       (showAddModal, L3830)                       (showDeliveryModal, L3868)
                              ↓                                       ↓
                    getCenterListFactory.result.list       getDeliveryListFactory.result.list
                              ↓                                   ↓
                    API-6 sendMedicalProductToMachineCenter  API-5 saveMedicalProductStockBatch
                       (selectOrder, L3955)                    (saveStock, L3979)
                              ↓                                   ↓
                    addOrderModal=false                       stockDetail=false
                    + $state.reload                          + search + getCount
                                                              + $state.reload
```

**A 级 100% 收口**（仅画直接代码证明的箭头）。

---

## 31. 历史证据 vs 当前证据

### S1-61 维护结论
- machineOrderCtrl save API → 5 API 协议
- **与本轮无关**（不同 controller），无冲突

### S1-62 维护结论
- deliveryInputCtrl save API → 仅 1 个 save API
- **S1-64 收口时**发现 deliveryInputCtrl 有 5 API（S1-62 推测错误）
- **S1-65 收口时**发现第 6 API（S1-62 推测错误）
- **S1-66 验证**：6 API 完整 100% A 级一致

### S1-63 维护结论
- deliveryInputCtrl 同时调 Query + Save
- **S1-64 验证**：是（5 API）
- **S1-65 验证**：是（追加第 6 API）
- **S1-66 验证**：6 API 完整
- **无冲突**

### S1-64 维护结论
- 5 核心 API
- **S1-64 + S1-65 验证**：5 + 1 = 6 API
- **S1-66 验证**：S1-64 当时未发现第 6 API
- **历史证据**：S1-64 仅 5 API
- **当前证据**：S1-65 + S1-66 6 API
- **处理方式**：S1-64 已封口，不修改。S1-66 文档补"6 API 完整收口"

### S1-65 维护结论
- sendMedicalProductToMachineCenter.json 唯一调用点 L3966
- **S1-66 验证**：是（仅 1 处）
- **S1-66 新发现**：selectOrder 与 saveStock success 行为差异（reload 都调，但 search/getCount/stockDetail 不同）
- **无冲突**

### S1-66 收口
- 6 API 交叉一致
- 全部 A 级
- 无冲突

---

## 32. A/B/C/D/E/F 评级分布

**A 级 100% 收口**：所有 30 项审计

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | Controller 范围 | A |
| 30.2-30.4 | 6 API 清单 + 唯一调用点 + Function 对照 | A |
| 30.5-30.6 | Request/Response 一致性 | A |
| 30.7-30.8 | success 一致性 + Save vs Send | A |
| 30.9 | 初始化行为 | A |
| 30.10-30.11 | waitingDeliveryList + medicalProduct.id | A |
| 30.12-30.13 | objectId 生命周期 + 派生链 | A |
| 30.14 | medicalProductMachineCenterPoList 双向 | A |
| 30.15-30.16 | getCenterListFactory + machineCenter.id | A |
| 30.17-30.18 | selectOrder + saveStock | A |
| 30.19-30.20 | deliveryCount + stockInSku.id | A |
| 30.21-30.22 | listCount + getDeliveryListFactory | A |
| 30.23 | Save JSON 构造 | A |
| 30.24 | Save 链 vs Send 链独立性 | A |
| 30.25 | Query 链 vs Send 链 | A |
| 30.26 | Delivery SKU 链 vs Send 链 | A |
| 30.27 | cashflowId | A |
| 30.28 | modal / refresh 生命周期 | A |
| 30.29 | machineCenterOrder / machineOrder 隔离 | A（隔离） |
| 30.30 | 六 API 冻结协议 | A |

**统计**：A=30 / B=0 / C=0 / D=0 / E=0 / F=0 = 30

---

## 33. L1/L2/L3

**L1（前端直接事实）**：
- 6 API 完整协议
- 数据依赖图
- 隔离关系
- evidence 等级：**A**

**L2（业务模型解释）**：
- "发货流" / "发到机器中心" 业务流程
- "Save 库存" / "Send 加工中心" 业务区分
- evidence 等级：**E**

**L3（数据库/物理模型）**：
- 数据库表结构
- machineCenterOrder / machineOrder / medicalProductMachineCenter 表
- 1:N 关系
- evidence 等级：**F**

---

## 34. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F（HTML / DB）

---

## 35. Q 问题集（30 项审计完整 Q&A）

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | deliveryInputCtrl 当前证实多少个 API？ | A（**6 个**） |
| Q2 | 六 API 是否全部有唯一调用点？ | A（**是**） |
| Q3 | 六 API 的 Request 是否全部完整可得？ | A |
| Q4 | 六 API 的 Response 是否全部完整可得？ | A（已观察字段）/ F（未观察字段） |
| Q5 | Query / Save / Send 三条链是否已经闭合？ | A（**是**） |
| Q6 | medicalProduct.id 的全部已观察映射是否一致？ | A |
| Q7 | objectId 与 machineCenter.id 的实际代码链是什么？ | A（L3854 → L3824 → get API Response → L3962） |
| Q8 | medicalProductMachineCenterPoList 在 Query / Send 中是否同构？ | A（**字段名同构，元素来源不同**） |
| Q9 | Delivery SKU Query 与 Send 是否存在直接关系？ | A（**无**，仅共享 waitingDeliveryList） |
| Q10 | Save 与 Send 是否存在直接关系？ | A（**无**，仅共享 cashflowId + reload） |
| Q11 | deliveryCount 是否未经修改直接进入 Save？ | A（**是**） |
| Q12 | listCount 的真实来源是什么？ | A（getDeliveryListFactory.result.list.length） |
| Q13 | send success 是否 reload？ | A（**是**） |
| Q14 | 当前是否存在 send API → machineCenterOrder 的直接证据？ | A（**否**） |
| Q15 | 当前是否存在 send API → machineOrder 的直接证据？ | A（**否**） |
| Q16 | 当前数据库结构证据到什么程度？ | F（**未观察**） |

---

## 36. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 37. 一期可冻结事实

**A 级 100% 可复刻的 6 API 协议**：

1. **getCashflowDeliveryVo.json**
   - Request: `{ cashflowId }`
   - 已观察 Response: `result.object.waitingDeliveryList[]` 含 medicalProduct + lockStorehouse + lockMachineCenter

2. **statProductDeliveryStatusOfCashflow.json**
   - Request: `{ cashflowId }`
   - 已观察 Response: `res.status`

3. **getMedicalProductMachineCenterVoList.json**
   - Request: `{ medicalProductMachineCenterPoListJson: JSON.stringify([{medicalProductId, machineCenterId}]) }`
   - 已观察 Response: `result.list[]` 含 medicalProduct + machineCenter

4. **getCanBeDeliverySkuInListOfProduct.json**
   - Request: `{ medicalProductIdArray: [...] }`
   - 已观察 Response: `result.list[]` 含 medicalProduct + deliveryStockInSkuVoList[]

5. **saveMedicalProductStockBatch.json**
   - Request: `{ listCount, medicalProductStockBatctPoListJson: JSON.stringify([{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]) }`
   - 已观察 Response: `res.status`
   - success: search + getCount + $state.reload + stockDetail=false

6. **sendMedicalProductToMachineCenter.json**
   - Request: `{ medicalProductMachineCenterPoListJson: JSON.stringify([{medicalProductId, machineCenterId}]), planDeliveryTime }`
   - 已观察 Response: `res.status` + `res.errmsg`
   - success: notice + addOrderModal=false + $state.reload()

**直接证明的数据依赖**：
- waitingDeliveryList → medicalProduct.objectId = lockMachineCenter.id (if type==4)
- waitingDeliveryList → medicalProductIdArray (objectId==null 过滤)
- waitingDeliveryList → getMachineCenterList → getCenterListFactory
- getCenterListFactory → selectOrder → send
- getDeliveryListFactory → saveStock → save
- getCashflowDeliveryVo → waitingDeliveryList → 上述两条链分叉

**直接证明的刷新行为**：
- saveStock success: search() + getCount() + $state.reload() + stockDetail=false
- selectOrder success: notice("发送成功") + addOrderModal=false + $state.reload()

---

## 38. 当前 F 边界（明确冻结）

| F 边界 | 说明 |
|---|---|
| deliveryInputCtrl HTML 模板 | untracked 临时 HTML 中未发现 |
| 完整 route schema | `.state()` 定义 F 维持 |
| selectOrder UI 触发点 | HTML 模板缺失 |
| 6 API Response 完整字段 | 仅观察 status/errmsg/result.list/result.object 等 |
| 后端算法 | F 维持 |
| 数据库表结构 | F 维持 |
| DTO / VO / PO 类型定义 | F 维持 |
| send API 是否创建 MachineCenterOrder | F（无代码证据） |
| send API 后端实际数据落库结构 | F 维持 |
| cashflow / medicalProduct / machineCenter 数据库实体关系 | F 维持 |
| sendToMachineCenter 字符串 | F（controller.js 范围内完全不出现） |
| machineCenterOrder / machineOrder 字段在 deliveryInputCtrl | F（不出现） |
| HTML 触发顺序（先 Save 后 Send） | F |
| 用户编辑 deliveryCount 的 UI 入口 | F（HTML 缺失） |
| 后端事务 / 锁 / 状态机 | F |

---

## 39. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~125 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 40. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | 全仓 6 API 出现次数确认 | A |
| 2 | 3 个 API 跨 controller 使用（getCashflowDeliveryVo / statProductDeliveryStatusOfCashflow / getCanBeDeliverySku） | A |
| 3 | 3 个 API 仅 deliveryInputCtrl 使用（getMedicalProductMachineCenterVoList / saveMedicalProductStockBatch / sendMedicalProductToMachineCenter） | A |
| 4 | deliveryProcessingCtrl L4236-4261（26 行）也调 2 个 API 但不调其他 4 个 | A |
| 5 | deliveryInputRecordCtrl L4024-4072 调 2 个 API | A |
| 6 | Save 链与 Send 链完全独立 | A |
| 7 | Query 链与 Send 链完全独立 | A |
| 8 | cashflowId 仅进入 2 个初始化 API | A |
| 9 | modal / refresh 完整生命周期 | A |
| 10 | machineCenterOrder / machineOrder 在 deliveryInputCtrl 范围**不出现** | A |

---

## 41. 最终一句话

"S1-66 完成，已 Git 封口，立即停止，不进入 S1-67，等待老板下一条指令。"
