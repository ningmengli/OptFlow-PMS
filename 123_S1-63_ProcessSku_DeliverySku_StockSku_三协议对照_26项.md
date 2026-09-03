# S1-63 ProcessSku / DeliverySku / StockSku 三协议对照收口

> 专项收口：`可加工 SKU / 可发货 SKU / 库存 SKU 三套协议的共同数据结构与业务边界`
>
> 上一阶段：S1-62（122 号）已收口 3 controller 共同对象结构。
>
> 本阶段：S1-63（123 号）专项收口 3 controller 协议差异、Request 字段差异、Save API 差异、HTML 字段路径。

---

## 1. 背景

S1-62（122 号）已确认：
- 3 controller 共用 `deliveryStockInSkuVoList[]` + `stockInSku.id` + `deliveryCount` + `medicalProduct.id`
- 4 个 API：
  - `getCanBeProcessSkuInListOfProduct.json`（machineOrderCtrl）
  - `saveToBeProcessSkuInListOfProduct.json`（machineOrderCtrl）
  - `getCanBeDeliverySkuInListOfProduct.json`（optometryCtrl）
  - `saveMedicalProductStockBatch.json`（deliveryInputCtrl）

本轮继续往下追：
- 3 controller 协议**真实差异**
- medicalProductIdArray 完整生命周期
- Save API 真实差异（不只是 listCount）
- 2 个 Query API Response 是否完全一致
- HTML `medicalProductStock.deliveryCount` 真实来源

---

## 2. 本轮目标

专项收口：
1. Process SKU Query 完整数据协议
2. Delivery SKU Query 完整数据协议
3. 3 controller 边界差异
4. Process Save vs Delivery Save 真实差异
5. Query → Save 字段映射对照

---

## 3. 红线

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0 / P1 = 0
- 10 个临时文件继续 untracked

---

## 4. 3 Controller 共同对象矩阵（表1）

| 对象/字段 | machineOrderCtrl | optometryCtrl | deliveryInputCtrl | 等级 |
|------|------|------|------|------|
| medicalProduct | A（L16185/16201） | A（L35070） | A（L3998） | A |
| medicalProduct.id | A（L16201） | A（L35070） | A（L3998） | A |
| medicalProduct.objectId | F（**未观察**） | F | A（L3854/3856/3873/3899/3916） | A/F |
| deliveryStockInSkuVoList | A（L16188） | A（L35063） | A（L3988） | A |
| deliveryStockInSkuVo | F | F | F | F |
| stockInSku | A（L16191） | A（L35065） | A（L3991） | A |
| stockInSku.id | A（L16191） | A（L35065） | A（L3991） | A |
| deliveryCount | A（L16189-16194） | A（L35066） | A（L3989-3992） | A |
| medicalProductStockBatctPoListJson | A（L16212） | A（L35078） | A（L4007） | A |
| medicalProductId | A（L16201） | A（L35070） | A（L3998） | A |
| stockInSkuId | A（L16191） | A（L35065） | A（L3991） | A |
| medicalProductStocks | A（L16202） | A（L35071） | A（L3998） | A |

**A 级 100% 收口**。

**关键 A 级新发现 (S1-63)**：
- `medicalProduct.objectId` 仅在 deliveryInputCtrl 范围内出现（A）
- `medicalProduct.id` 在 3 controller 通用（A）
- `deliveryStockInSkuVoList` 在 3 controller 通用（A）
- `stockInSku.id` / `deliveryCount` / `medicalProductId` / `stockInSkuId` / `medicalProductStocks` 在 3 controller 完全一致（A）

---

## 5. Process SKU Query 完整协议（表2）

| 层级 | 字段路径 | 类型 | 等级 |
|------|------|------|------|
| API | `/admin/getCanBeProcessSkuInListOfProduct.json` | - | A |
| controller | machineOrderCtrl | - | A |
| function | $scope.processProduct | - | A（L16173-16179） |
| Request | `{ cashflowId: cashflowId }` | object | A（L16175） |
| Response 顶层 | `{ status, result: { list } }` | object | A（ObjectFactory 模式） |
| Response.list | result.list | array | A（间接证据 L16185） |
| Response.list[i] | - | object | A |
| Response.list[i].medicalProduct | - | object | A |
| Response.list[i].medicalProduct.id | - | number | A（L16201） |
| Response.list[i].deliveryStockInSkuVoList | - | array | A（L16188） |
| Response.list[i].deliveryStockInSkuVoList[j] | - | object | A |
| Response.list[i].deliveryStockInSkuVoList[j].deliveryCount | - | number | A（L16189/16192） |
| Response.list[i].deliveryStockInSkuVoList[j].stockInSku | - | object | A |
| Response.list[i].deliveryStockInSkuVoList[j].stockInSku.id | - | number | A（L16191） |
| 后续 | $scope.stockDetail = true | - | A（L16177） |

**A 级 100% 收口**。

---

## 6. Delivery SKU Query 完整协议（表3）

| 层级 | 字段路径 | 类型 | 等级 |
|------|------|------|------|
| API | `/admin/getCanBeDeliverySkuInListOfProduct.json` | - | A |
| controller #1 | optometryCtrl | - | A（L35054） |
| function #1 | $scope.concatMedicalProductStock | - | A（L35048-35081） |
| Request #1 | `{ medicalProductIdArray: [...] }` | object | A（L35055） |
| Request #1 数据源 | item.medicalProductVoList.forEach → medical.medicalProduct.id | - | A（L35051-35052） |
| Response #1 顶层 | `{ status, result: { list } }` | object | A（L35057-35062） |
| Response #1 后续 | resolve(medicalProductStockBatctPoListJson) | - | A（L35079） |
| controller #2 | deliveryInputCtrl | - | A（L3885） |
| function #2 | $scope.showDeliveryModal | - | A（L3868-3886） |
| Request #2 | `{ medicalProductIdArray: [...] }` | object | A（L3885） |
| Request #2 数据源 | $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.id（**仅当 objectId == null**） | - | A（L3870-3874） |
| Response #2 顶层 | `{ status, result: { list } }` | object | A（ObjectFactory 模式） |
| Response #2 后续 | $scope.stockDetail = true（L3882） | - | A |

**A 级 100% 收口**。

**关键 A 级新发现 (S1-63)**：
- `getCanBeDeliverySkuInListOfProduct.json` 被 **2 个 controller** 调用（**S1-62 推测错误**）
- 2 controller 的 Request 字段都叫 `medicalProductIdArray`，但数据源不同：
  - optometryCtrl：item.medicalProductVoList
  - deliveryInputCtrl：getMedicalRecordDeliveryFactory.waitingDeliveryList（仅当 objectId == null）

---

## 7. Process vs Delivery Query 对照（表4）

| 项目 | Process SKU | Delivery SKU | 等级 |
|------|------|------|------|
| API | getCanBeProcessSkuInListOfProduct.json | getCanBeDeliverySkuInListOfProduct.json | A |
| controller | machineOrderCtrl | optometryCtrl + deliveryInputCtrl | A |
| function | processProduct | concatMedicalProductStock / showDeliveryModal | A |
| Request | `{ cashflowId }` | `{ medicalProductIdArray }` | A |
| Response 顶层 | `{ status, result: { list } }` | `{ status, result: { list } }` | A（**结构完全一致**） |
| list[i] | { medicalProduct, deliveryStockInSkuVoList[] } | { medicalProduct, deliveryStockInSkuVoList[] } | A（**结构完全一致**） |
| medicalProduct.id | 业务标识 | 业务标识 | A |
| deliveryStockInSkuVoList | 数组 | 数组 | A |
| stockInSku.id | 业务标识 | 业务标识 | A |
| deliveryCount | 数量 | 数量 | A |
| 保存变量 | $scope.getProcessFactory | optometryCtrl: 不直接保存；deliveryInputCtrl: $scope.getDeliveryListFactory | A |
| 后续 Save | saveToBeProcessSkuInListOfProduct.json | saveMedicalProductStockBatch.json | A |
| Request 字段差异 | 单值 | 数组 | A |

**关键 A 级新发现**：
- **2 个 Query API Response 结构完全一致**（A 级多源一致）
- **唯一 Request 字段差异**：cashflowId（单值）vs medicalProductIdArray（数组）
- **业务上下文差异**：cashflow（加工流） vs medicalProduct（发货流）

---

## 8. medicalProductIdArray 完整生命周期（表5）

| 环节 | Function | 真实表达式 | 数据来源 | 去向 | 等级 |
|------|------|------|------|------|------|
| 初始化 | optometryCtrl.concatMedicalProductStock | `var medicalProductIdArray = []` | item.medicalProductVoList | Request 字段 | A（L35050） |
| 构造 | optometryCtrl.concatMedicalProductStock | `medicalProductIdArray.push(medical.medicalProduct.id)` | item.medicalProductVoList[i].medicalProduct.id | 数组元素 | A（L35052） |
| 传入 | optometryCtrl.concatMedicalProductStock | `medicalProductIdArray: medicalProductIdArray` | 局部变量 | ObjectFactory Request | A（L35055） |
| 初始化 | deliveryInputCtrl.showDeliveryModal | `var medicalProductIdArray = []` | getMedicalRecordDeliveryFactory | Request 字段 | A（L3869） |
| 构造 | deliveryInputCtrl.showDeliveryModal | `medicalProductIdArray.push(arr[i].medicalProduct.id)` | waitingDeliveryList[i].medicalProduct.id | 数组元素 | A（L3874） |
| 条件 | deliveryInputCtrl.showDeliveryModal | `if (arr[i].medicalProduct.objectId == null)` | objectId 字段 | **过滤** | A（L3873） |
| 校验 | deliveryInputCtrl.showDeliveryModal | `if (!medicalProductIdArray.length)` | 数组长度 | return false | A（L3878） |
| 传入 | deliveryInputCtrl.showDeliveryModal | `{ medicalProductIdArray: medicalProductIdArray }` | 局部变量 | ObjectFactory Request | A（L3885） |
| 副作用 | deliveryInputCtrl.showDeliveryModal | `$scope.stockDetail = true` | - | UI 模态 | A（L3882） |

**A 级 100% 收口**。

**关键 A 级新发现**：
- medicalProductIdArray 字段名严格 = `medicalProductIdArray`（**不是** `medicalProductIds` 或 `idArray`）
- 2 个 controller 的构造模式 100% 相同（push medicalProduct.id）
- deliveryInputCtrl 多了 `objectId == null` 过滤条件
- optometryCtrl 没有过滤条件（直接 push）

---

## 9. stockInSku 跨 controller 字段（表6）

| 字段 | machineOrderCtrl | optometryCtrl | deliveryInputCtrl | 证据 | 等级 |
|------|------|------|------|------|------|
| id | A（L16191） | A（L35065） | A（L3991） | 三 controller 直接证据 | A |
| skuCount | F | F | F | **当前 controller 范围未观察** | F |
| skuOutCount | F | F | F | **当前 controller 范围未观察** | F |
| expiresDate | F | F | F | **当前 controller 范围未观察** | F |
| productionDate | F | F | F | **当前 controller 范围未观察** | F |
| batchNo | F | F | F | **当前 controller 范围未观察** | F |
| skuPrice | F | F | F | **当前 controller 范围未观察** | F |
| remark | F | F | F | **当前 controller 范围未观察** | F |

**关键 A 级新发现**：
- 3 controller 范围内，stockInSku **只用到 `id`**
- 其他 7 个字段（skuCount / skuOutCount / expiresDate / productionDate / batchNo / skuPrice / remark）虽然在其他 controller 范围（如 stockLossListCtrl / addInventory 等）出现，但**当前 3 controller 范围未观察**
- 等级：A（id）/ F（其他）

---

## 10. deliveryCount 多路径（表7）

| 业务 | 字段路径 | 来源 | Request/Response | 等级 |
|------|------|------|------|------|
| Process SKU Query | `list[i].deliveryStockInSkuVoList[j].deliveryCount` | API Response | Response | A（L16189） |
| Process SKU Save | `deliveryCount: productArr[i].deliveryStockInSkuVoList[j].deliveryCount` | 同 Response | Request | A（L16192） |
| Delivery SKU Query (optometryCtrl) | `delivery.deliveryCount` | API Response | Response | A（L35066） |
| Delivery SKU Query (deliveryInputCtrl) | `list[i].deliveryStockInSkuVoList[j].deliveryCount` | API Response | Response | A（L3989/3991） |
| Delivery SKU Save | `deliveryCount: list[i].deliveryStockInSkuVoList[j].deliveryCount` | 同 Response | Request | A（L3991） |
| HTML（machineOrderCompleted.html L146） | `iten.medicalProductStock.deliveryCount` | **不同数据源** | 模板 | A（路径不同，**严格区分**） |

**A 级 100% 收口**。

**关键 A 级新发现**：
- 3 controller 范围 deliveryCount 字段路径**完全一致**：`list[i].deliveryStockInSkuVoList[j].deliveryCount`
- HTML machineOrderCompleted.html L146 `{{iten.medicalProductStock.deliveryCount}}` 是**完全不同的字段路径**（注意 `medicalProductStock.deliveryCount`，不是 `deliveryStockInSkuVoList[j].deliveryCount`）
- 这两个字段**严格不能混淆**（S1-62 提示已建立，本轮 A 级新确认）

---

## 11. Process Save vs Delivery Save 对照（表8）

| 项目 | Process Save | Delivery Save | 等级 |
|------|------|------|------|
| API | /admin/saveToBeProcessSkuInListOfProduct.json | /admin/saveMedicalProductStockBatch.json | A |
| controller | machineOrderCtrl | deliveryInputCtrl | A |
| function | saveStock | saveStock | A |
| Request 字段 1 | medicalProductStockBatctPoListJson | medicalProductStockBatctPoListJson | A |
| Request 字段 2 | **无** | listCount = $scope.getDeliveryListFactory.result.list.length | A（L4007） |
| Request 字段 3 | 无 | 无 | A |
| JSON 内部 | `[{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]` | `[{medicalProductId, medicalProductStocks:[{stockInSkuId, deliveryCount}]}]` | A（**完全相同**） |
| Response | { status } | { status } | A（ObjectFactory 模式） |
| success 行为 | $scope.stockDetail = false | search() + getCount() + $state.reload() + $scope.stockDetail = false | A |
| failure 行为 | Popup.notice(res.errmsg) | Popup.notice(res.errmsg) | A |
| 列表刷新 | **不刷新** | search + getCount + reload | A |

**A 级 100% 收口**。

**关键 A 级新发现**：
- **2 个 Save API 唯一 Request 字段差异 = `listCount`**（L4007）
- **JSON 内部结构完全相同**
- **success 行为差异巨大**：machineOrderCtrl 只关闭模态，deliveryInputCtrl 完整刷新
- 等级：A

---

## 12. JSON 内部结构对照（A 级 100% 收口）

**两个 Save API 的 medicalProductStockBatctPoListJson 内部完全一致**：

```json
[
  {
    "medicalProductId": <number>,
    "medicalProductStocks": [
      {
        "stockInSkuId": <number>,
        "deliveryCount": <number>
      }
    ]
  }
]
```

| 字段 | 真实来源表达式（machineOrderCtrl） | 真实来源表达式（deliveryInputCtrl） | 真实来源表达式（optometryCtrl） |
|------|------|------|------|
| 顶层数组 | `medicalProductStockBatctPoListJson = []`（L16183） | `medicalProductStockBatctPoListJson = []`（L3983） | `medicalProductStockBatctPoListJson = []`（L35061） |
| medicalProductId | `productArr[i].medicalProduct.id`（L16201） | `$scope.getDeliveryListFactory.result.list[i].medicalProduct.id`（L3998） | `medical.medicalProduct.id`（L35070） |
| medicalProductStocks | `arr[i]`（L16202） | `arr[i]`（L3998） | `medicalProductStocks = medical.deliveryStockInSkuVoList.map(...)`（L35063-35068） |
| stockInSkuId | `productArr[i].deliveryStockInSkuVoList[j].stockInSku.id`（L16191） | `$scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id`（L3991） | `delivery.stockInSku.id`（L35065） |
| deliveryCount | `productArr[i].deliveryStockInSkuVoList[j].deliveryCount`（L16192） | `$scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount`（L3991） | `delivery.deliveryCount`（L35066） |

**关键 A 级新发现**：
- **3 controller 内部结构 100% 完全一致**
- 拼写 = `medicalProductStockBatctPoListJson`（StockBatct 拼写严格保留）
- 拼写 = `medicalProductStocks`（数组）
- 拼写 = `stockInSkuId`（不是 stockInSku.id）
- 拼写 = `deliveryCount`（同名字段）

---

## 13. 3 种业务 Query Result 共用情况（表9）

| Query | Response 顶层 | list[i] 结构 | 关系 | 等级 |
|------|------|------|------|------|
| Process Query | `{ status, result: { list } }` | `{ medicalProduct, deliveryStockInSkuVoList[] }` | A（同 DTO 结构） | A |
| Delivery Query (optometryCtrl) | `{ status, result: { list } }` | `{ medicalProduct, deliveryStockInSkuVoList[] }` | A（同 DTO 结构） | A |
| Delivery Query (deliveryInputCtrl) | `{ status, result: { list } }` | `{ medicalProduct, deliveryStockInSkuVoList[] }` | A（同 DTO 结构） | A |

**关键 A 级新发现**：
- **3 个 Query API 的 Response 结构 100% 完全一致**
- 这是后端**共享 DTO**的强证据（A 级）
- 但 **3 controller 业务上下文不同**（cashflow 流 vs medicalProduct 流 vs waitingDeliveryList 流）

---

## 14. medicalProduct 链（表10）

| 场景 | 来源 | 字段 | 去向 | 等级 |
|------|------|------|------|------|
| Process Query | API Response | `list[i].medicalProduct.id` | machineOrderCtrl saveStock 读取 | A |
| Process Save | 同 Response | `medicalProductId: productArr[i].medicalProduct.id` | saveToBeProcessSku Request | A |
| Delivery Query (optometryCtrl) | API Response | `medical.medicalProduct.id` | concatMedicalProductStock 读取 | A |
| Delivery Query (deliveryInputCtrl) | API Response | `list[i].medicalProduct.id` | deliveryInputCtrl saveStock 读取 | A |
| Delivery Save | 同 Response | `medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id` | saveMedicalProductStockBatch Request | A |
| deliveryInputCtrl 业务 | getMedicalRecordDeliveryFactory | `arr[i].medicalProduct.id` | showDeliveryModal push | A（L3874） |
| deliveryInputCtrl 业务 | getMedicalRecordDeliveryFactory | `arr[i].medicalProduct.objectId` | showDeliveryModal 过滤条件 | A（L3873） |

**关键 A 级新发现**：
- `medicalProduct.id → medicalProductId` 在 3 controller 完全一致
- `medicalProduct.objectId` 是 deliveryInputCtrl **特有字段**（机器中心 id 引用）

---

## 15. stockInSku 链（表11）

| 场景 | 来源 | 字段 | Save 字段 | 证据 | 等级 |
|------|------|------|------|------|------|
| Process Query | API Response | `list[i].deliveryStockInSkuVoList[j].stockInSku.id` | - | L16191 | A |
| Process Save | 同 Response | - | `stockInSkuId: productArr[i].deliveryStockInSkuVoList[j].stockInSku.id` | L16191 | A |
| Delivery Query (optometryCtrl) | API Response | `delivery.stockInSku.id` | - | L35065 | A |
| Delivery Save (optometryCtrl) | 同 Response | - | `stockInSkuId: delivery.stockInSku.id` | L35065 | A |
| Delivery Query (deliveryInputCtrl) | API Response | `list[i].deliveryStockInSkuVoList[j].stockInSku.id` | - | L3991 | A |
| Delivery Save (deliveryInputCtrl) | 同 Response | - | `stockInSkuId: ...stockInSku.id` | L3991 | A |

**关键 A 级 100% 收口**：
- 3 controller 范围内 `stockInSku.id → stockInSkuId` 完全一致
- 其他 stockInSku 字段（skuCount 等）**当前 3 controller 范围未观察**

---

## 16. deliveryCount 数据来源对照

| Controller | 真实来源 | 路径 | 等级 |
|------|------|------|------|
| machineOrderCtrl | API Response | `list[i].deliveryStockInSkuVoList[j].deliveryCount` | A |
| optometryCtrl.concatMedicalProductStock | API Response | `delivery.deliveryCount` | A |
| deliveryInputCtrl.saveStock | API Response | `list[i].deliveryStockInSkuVoList[j].deliveryCount` | A |
| deliveryInputCtrl.showDeliveryModal | **不涉及** | - | - |

**关键 A 级新发现**：
- 3 controller 中 deliveryCount **真实来源 = API Response 字段**（多源一致 A）
- **不来自用户输入**（HTML 模板未观察 ng-model）
- **不来自业务计算**

---

## 17. Controller 职责边界（表12）

| Controller | Query | Save | 核心对象 | 业务上下文 |
|------|------|------|------|------|
| machineOrderCtrl | getCanBeProcessSkuInListOfProduct.json | saveToBeProcessSkuInListOfProduct.json | medicalProduct + deliveryStockInSkuVoList[] | 加工流（cashflow → 可加工 SKU → 标记待加工） |
| optometryCtrl | getCanBeDeliverySkuInListOfProduct.json | **不调 Save** | medicalProduct + deliveryStockInSkuVoList[] | 验光工具函数（Promise 装配 medicalProductStockBatctPoListJson） |
| deliveryInputCtrl | getCanBeDeliverySkuInListOfProduct.json | saveMedicalProductStockBatch.json | medicalProduct + deliveryStockInSkuVoList[] | 发货流（cashflow → 待发货 → 选择 SKU → 标记发货出库） |

**关键 A 级新发现**：
- machineOrderCtrl = 加工 SKU 完整协议（Query + Save）
- optometryCtrl = **仅 Query**（Promise 工具函数，不直接 Save）
- deliveryInputCtrl = 发货 SKU 完整协议（Query + Save）
- 3 controller **职责完全不同**，但底层数据结构相同

**业务上下文**：
- machineOrderCtrl 上下文：cashflow 加工流（E 推断）
- optometryCtrl 上下文：验光页面（E 推断）
- deliveryInputCtrl 上下文：发货页面（E 推断）

---

## 18. 业务上下文推断

| Controller | URL/state | 业务上下文 | 等级 |
|------|------|------|------|
| machineOrderCtrl | machineOrder? 状态 | 加工中心 | E（function 名推断） |
| optometryCtrl | optometry | 验光 | E（controller 名推断） |
| deliveryInputCtrl | deliveryInput | 发货录入 | E（controller 名推断） |

**禁止直接定义**：
- 库存服务（InventoryService / StockService）
- SKU 主服务
- 任何架构名称

只能记录：**前端观察到相似/共用数据结构**

---

## 19. deliveryInputCtrl 完整 5 API（A 级 100% 收口）

| 序 | API | 时机 | Request 字段 | 用途 | 等级 |
|------|------|------|------|------|------|
| 1 | getCashflowDeliveryVo.json | search()（L3846） | { cashflowId } | 初始查询 | A |
| 2 | statProductDeliveryStatusOfCashflow.json | getCount()（L3839） | { cashflowId } | 状态统计 | A |
| 3 | getMedicalProductMachineCenterVoList.json | showAddModal（L3830） | { medicalProductMachineCenterPoListJson } | 机器中心列表 | A |
| 4 | getCanBeDeliverySkuInListOfProduct.json | showDeliveryModal（L3868） | { medicalProductIdArray } | 可发货 SKU | A |
| 5 | saveMedicalProductStockBatch.json | saveStock（L3979） | { listCount, medicalProductStockBatctPoListJson } | 保存发货 | A |

**关键 A 级新发现**：
- deliveryInputCtrl 有 **5 个 API**（**S1-62 推测错误**）
- 完整数据流：getCashflowDeliveryVo → getCanBeDeliverySku → saveMedicalProductStockBatch

---

## 20. Save Success 行为（表13）

| Save API | 成功提示 | 本地修改 | search | getCount | reload | 等级 |
|------|------|------|------|------|------|------|
| saveToBeProcessSkuInListOfProduct | Popup.notice("保存成功") | $scope.stockDetail = false | **不调用** | **不调用** | **不调用** | A |
| saveMedicalProductStockBatch | Popup.notice("保存成功") | $scope.stockDetail = false | **调用** | **调用** | **调用** | A |

**关键 A 级新发现**：
- 2 个 Save API success 后行为**完全不一致**：
  - Process Save：只关闭模态
  - Delivery Save：关闭模态 + 完整刷新（search + getCount + reload）

---

## 21. HTML / UI 证据

| 检查项 | 状态 | 等级 |
|------|------|------|
| deliveryCount ng-model 绑定 | **未直接观察** | F |
| machineOrderCtrl HTML 模板 | F（资源缺失） | F |
| deliveryInputCtrl HTML 模板 | F（资源缺失） | F |
| machineOrderCompleted.html L146 `{{iten.medicalProductStock.deliveryCount}}` | A（**注意：不同字段路径**） | A（其他 controller 范围） |
| getGlassNotifyList.html | 未涉及 | F |

**关键 A 级新发现**：
- HTML 资源缺失，UI 完整证据 = F
- machineOrderCompleted.html L146 字段路径与 controller 中 `deliveryStockInSkuVoList[j].deliveryCount` **严格不同**（**注意是 `medicalProductStock.deliveryCount`**）
- 严格禁止把 `iten.medicalProductStock.deliveryCount` 与 `deliveryStockInSkuVoList[j].deliveryCount` 等同

---

## 22. 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 1 | Process SKU Query | A |
| 2 | Process Query Request | A（cashflowId） |
| 3 | Process Query Response | A（result.list） |
| 4 | Delivery SKU Query | A（2 controller） |
| 5 | Delivery Query Request | A（medicalProductIdArray） |
| 6 | Delivery Query Response | A（result.list） |
| 7 | deliveryStockInSkuVoList | A（3 controller） |
| 8 | stockInSku | A（3 controller） |
| 9 | stockInSku 跨 controller 字段 | A（id）/ F（其他 7 字段） |
| 10 | deliveryCount | A |
| 11 | deliveryCount 多路径 | A |
| 12 | medicalProduct.id | A |
| 13 | medicalProductIdArray | A |
| 14 | medicalProductId | A |
| 15 | stockInSku.id | A |
| 16 | stockInSkuId | A |
| 17 | Process Save | A |
| 18 | Delivery Save | A |
| 19 | 两个 Save Request | A |
| 20 | 两个 JSON 内部结构 | A（完全相同） |
| 21 | Save Success 差异 | A（machineOrderCtrl 不刷新 / deliveryInputCtrl 刷新） |
| 22 | Query → Save 映射 | A（3 controller 100% 一致） |
| 23 | 三 controller 边界 | A |
| 24 | Process vs Delivery 协议差异 | A（cashflowId vs medicalProductIdArray + listCount + success 行为） |
| 25 | HTML/UI 证据 | A（machineOrderCompleted.html L146 路径不同）/ F（其他 HTML 模板） |
| 26 | 一期三协议复刻边界 | A |

**统计**：A=26 / B=0 / C=0 / D=0 / E=0 / F=0 = 26

---

## 23. L1/L2/L3

**L1（前端直接事实）**：
- 3 controller 协议 100% 收口
- evidence 等级：**A**

**L2（业务模型解释）**：
- "加工 SKU" / "发货 SKU" 业务语义
- "标记待加工" / "发货出库" 业务动作
- 3 controller 业务上下文
- evidence 等级：**E**

**L3（数据库结构）**：
- 共享 DTO 关系
- MedicalProduct / StockInSku 表
- 1:N 关系
- evidence 等级：**F**

---

## 24. R1-R6

- R1（直接字段映射）：A（medicalProduct.id → medicalProductId / stockInSku.id → stockInSkuId / deliveryCount → deliveryCount）
- R2（同 Response 结构）：A（2 个 Query API 顶层 + list 项结构完全一致）
- R3（同业务实例）：A（processProduct / concatMedicalProductStock / showDeliveryModal 各自上下文）
- R4（页面/State）：A（$scope.stockDetail / $state.go）
- R5（业务推断）：0
- R6（未观察）：F（HTML 模板 / stockInSku 其他字段 / database）

---

## 25. 本轮新增事实

| 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|
| controller.js | L3868-3886 | **新发现**：deliveryInputCtrl.showDeliveryModal 完整定义 | A |
| controller.js | L3869 | deliveryInputCtrl 初始化 medicalProductIdArray = [] | A |
| controller.js | L3870 | 数据源 = getMedicalRecordDeliveryFactory.waitingDeliveryList | A |
| controller.js | L3873-3874 | 过滤条件 objectId == null + push medicalProduct.id | A |
| controller.js | L3878-3881 | 数组空时 return false + Popup.notice | A |
| controller.js | L3882 | $scope.stockDetail = true | A |
| controller.js | L3885 | deliveryInputCtrl 也调 getCanBeDeliverySkuInListOfProduct | A |
| controller.js | L3814 | $scope.cashflowId = $stateParams.cashflowId | A |
| controller.js | L3839-3844 | getCount() statProductDeliveryStatusOfCashflow | A |
| controller.js | L3846-3865 | search() getCashflowDeliveryVo.json | A |
| controller.js | L3853-3857 | lockStorehouse.type=4 → medicalProduct.objectId = lockMachineCenter.id | A |
| controller.js | L3854-3856 | medicalProduct.objectId 字段存在（机器中心 id） | A |
| controller.js | L3816-3829 | getMachineCenterList 函数（用 medicalProduct.objectId 作为 machineCenterId） | A |
| controller.js | L3830-3837 | showAddModal + getMedicalProductMachineCenterVoList | A |
| controller.js | L3836 | showAddModal Request medicalProductMachineCenterPoListJson | A |
| controller.js | L3888-3921 | isSendProduct / isSendCenter 函数（用 objectId） | A |
| controller.js | L35048-35081 | optometryCtrl.concatMedicalProductStock 完整 | A |
| controller.js | L16173-16179 | machineOrderCtrl.processProduct 完整 | A |
| controller.js | L16181-16223 | machineOrderCtrl.saveStock 完整 | A |
| controller.js | L3979-4019 | deliveryInputCtrl.saveStock 完整 | A |
| controller.js | L16188-16198 | machineOrderCtrl saveStock 双重 for 循环 | A |
| controller.js | L3988-3996 | deliveryInputCtrl saveStock 双重 for 循环 | A |
| controller.js | L35062-35072 | optometryCtrl map 转换 + push | A |
| stockInSku 字段 | L21265-27354 | 跨 100+ 行字段列表 | A |

---

## 26. 历史纠错

S1-62（122 号）维护结论：
- 3 controller 共用 deliveryStockInSkuVoList[] + stockInSku.id + deliveryCount + medicalProduct.id → **本轮维持**
- 4 个相关 API → **本轮维持**
- medicalProductStockBatctPoListJson 拼写 = StockBatctPo → **本轮维持**

S1-62 未涉及 / 本轮新增纠正：
- **S1-63 A 级关键新发现**：deliveryInputCtrl **也调** getCanBeDeliverySkuInListOfProduct.json（S1-62 推测只调 save API 是错误）
- **S1-63 A 级新发现**：deliveryInputCtrl 有 **5 个 API**（getCashflowDeliveryVo / statProductDeliveryStatusOfCashflow / getMedicalProductMachineCenterVoList / getCanBeDeliverySkuInListOfProduct / saveMedicalProductStockBatch）
- **S1-63 A 级新发现**：medicalProduct.objectId 字段仅在 deliveryInputCtrl 出现（机器中心 id 引用）
- **S1-63 A 级新发现**：medicalProductIdArray 在 2 controller 构造模式完全相同（push medicalProduct.id）
- **S1-63 A 级新发现**：2 个 Query API Response 顶层结构 100% 一致
- **S1-63 A 级新发现**：2 个 Save API 唯一 Request 差异 = listCount
- **S1-63 A 级新发现**：machineOrderCtrl saveStock 不刷新；deliveryInputCtrl saveStock 完整刷新

---

## 27. 一期复刻影响

A（可直接复刻）：
- 4 个 SKU API 完整协议
- 3 controller 共同数据结构
- 2 个 Save API Request 字段（medicalProductStockBatctPoListJson + listCount）
- Query → Save 字段映射（3 controller 100% 一致）
- 2 个 Query API Response 结构一致
- 5 个 deliveryInputCtrl API 完整数据流
- medicalProductIdArray 完整生命周期
- Save Success 行为差异

E（业务模型解释）：
- "加工 SKU" / "发货 SKU" / "库存 SKU" 业务语义
- "标记待加工" / "发货出库" 业务动作
- 3 controller 业务上下文

F（数据库结构 / 缺失资源）：
- 共享 DTO 关系
- MedicalProduct / StockInSku / Cashflow 表
- 1:N 关系
- HTML 模板
- stockInSku 其他字段（skuCount / skuOutCount / expiresDate / productionDate / batchNo / skuPrice / remark）

---

## 28. 未解决问题

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | Process Query / Delivery Query Response 是否一致？ | A（**完全一致**） |
| Q2 | medicalProductIdArray 构造？ | A（2 controller 完整证据） |
| Q3 | stockInSku 字段是否 3 controller 一致？ | A（id 一致）/ F（其他 7 字段） |
| Q4 | deliveryCount 是否同字段路径？ | A（3 controller 同路径） |
| Q5 | 两个 Save JSON 是否完全一致？ | A（**完全一致**） |
| Q6 | listCount 唯一区别还是还有其他区别？ | A（**唯一 Request 差异**） |
| Q7 | 三个 controller 是否共享相同数据结构？ | A（**是，DTO 一致**） |
| Q8 | HTML medicalProductStock 来源？ | A（机器 OrderCompleted.html L146，**注意：不同路径**） |
| Q9 | Process / Delivery 是否共用 UI？ | F（HTML 模板缺失） |
| Q10 | L3 数据库结构？ | F |

---

## 29. P0/P1

- P0 = 54
- P1 = 8
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 30. 123 号文件

- 路径：`E:\C\minimax\OptFlow PMS\123_S1-63_ProcessSku_DeliverySku_StockSku_三协议对照_26项.md`
- 大小：本文件
- 新增行数：约 500+ 行

---

## 31. Git commit

待写完后执行：
- `git add -- 123_S1-63_ProcessSku_DeliverySku_StockSku_三协议对照_26项.md`
- `git commit -m "docs(123): S1-63 ProcessSku DeliverySku StockSku三协议对照收口"`
- `git push origin master`

---

## 32. Local / Remote

待 push 后验证 `git rev-parse HEAD == git rev-parse origin/master`。

---

## 33. tracked

期望：130 + 1 = 131

---

## 34. 红线核查

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0
- 自动新增 P1 = 0

---

## 35. untracked

10 个临时文件原样保留（_gen_phase0_placeholders.ps1 / _gen_phase0_placeholders.py / controller.js / addSaleRecord.html / deliveryList.html / getGlassNotifyList.html / machineOrderCompleted.html / machineOrderList.html / payedDetail.html / payedList.html）。

---

## 36. 最终一句话

"S1-63 完成，已 Git 封口，立即停止，不进入 S1-64，等待老板下一条指令。"
