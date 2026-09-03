# S1-61 machineOrderCtrl / ProductSku / 可加工SKU 数据协议收口

> 专项收口：`machineOrderCtrl → 商品 / SKU / 可加工 SKU 数据协议与操作边界`
>
> 上一阶段：S1-60（119 号）已收口 machineOrderCtrl 列表 API 数据协议。
>
> 本阶段：S1-61（121 号）专项收口 machineOrderCtrl 内部的 2 个商品/SKU 相关 API。

---

## 1. 背景

S1-60（119 号）已确认：
- machineOrderCtrl = L16094-16258
- 列表 API = `/admin/selectInStoreMachineCenterCashflowVoList.json`
- 5 个写 API = startMachineCenterOrder / completeMachineCenterOrder / closeMachineCenterOrder / **getCanBeProcessSkuInListOfProduct** / **saveToBeProcessSkuInListOfProduct**

本轮继续往下追：
- getCanBeProcessSkuInListOfProduct.json 完整数据协议
- saveToBeProcessSkuInListOfProduct.json 完整数据协议
- 2 个 API 与商品 / MedicalProduct / SKU / MachineCenterOrder 关系

---

## 2. 本轮目标

专项收口：
1. `getCanBeProcessSkuInListOfProduct.json` 完整调用链
2. `saveToBeProcessSkuInListOfProduct.json` 完整调用链
3. processProduct / saveStock 完整定义
4. SKU 对象真实结构
5. 商品 / MedicalProduct / SKU 边界

---

## 3. 红线

- 写操作 = 0（saveToBeProcessSkuInListOfProduct 是写 API，严禁调用）
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0 / P1 = 0
- 10 个临时文件继续 untracked

---

## 4. getCanBeProcessSkuInListOfProduct.json（表1）

| 项目 | 证据 | 等级 |
|------|------|------|
| API | `/admin/getCanBeProcessSkuInListOfProduct.json` | A |
| function | `$scope.processProduct`（controller.js L16173-16179） | A |
| controller | `machineOrderCtrl`（L16094-16258） | A |
| Request | `{ cashflowId: cashflowId }`（L16175） | A |
| 参数来源 | cashflowId = function 参数；idx = function 参数（未使用） | A |
| Response | `$scope.getProcessFactory.result.list`（L16185 间接证据） | A（顶层结构）/ F（ListFactory 内部） |
| UI 用途 | （HTML 模板未观察） | F |
| 后续调用 | `$scope.stockDetail = true`（L16177） | A |
| 等级 | A | - |

**关键 A 级新发现**：
- 唯一调用点：controller.js L16175
- 唯一 controller：machineOrderCtrl
- 唯一调用 function：$scope.processProduct
- Request 仅 1 个字段：cashflowId
- 响应后只设置 $scope.stockDetail = true（打开"库存详情"模态框/区域）

---

## 5. Query Request 逐字段（表2）

| 参数 | 原始表达式 | 来源对象 | API | Request/Response | 等级 |
|------|------|------|------|------|------|
| cashflowId | `{ cashflowId: cashflowId }` | function 参数 | getCanBeProcessSku | Request | A |
| productId | **未出现** | - | - | - | F |
| productSkuId | **未出现** | - | - | - | F |
| medicalProductId | **未出现** | - | - | - | F |
| skuId | **未出现** | - | - | - | F |
| objectId | **未出现** | - | - | - | F |

**关键 A 级新发现**：
- 唯一 Request 字段 = `cashflowId`
- 没有任何 productId / productSkuId / skuId / objectId 字段直接进入 Request
- **S1-60 推测错误纠正**：本轮严格按 controller.js 源代码确认

---

## 6. Query Response 结构（表3）

| 层级 | 真实路径 | 类型 | 字段 | 用途 | 等级 |
|------|------|------|------|------|------|
| Response 顶层 | `res.status` | number | - | 成功/失败 | A |
| result | `res.result.list` | array | - | 列表主对象 | A（L16185 间接证据） |
| list[i] | `productArr[i]` | object | - | 商品项 | A |
| list[i].medicalProduct | `productArr[i].medicalProduct` | object | - | MedicalProduct 包装 | A（L16185-16204） |
| list[i].medicalProduct.id | `productArr[i].medicalProduct.id` | number | - | MedicalProduct id | A（L16201） |
| list[i].deliveryStockInSkuVoList | `productArr[i].deliveryStockInSkuVoList` | array | - | 库存 SKU VO 列表 | A（L16188） |
| list[i].deliveryStockInSkuVoList[j] | `productArr[i].deliveryStockInSkuVoList[j]` | object | - | 库存 SKU 项 | A |
| list[i].deliveryStockInSkuVoList[j].deliveryCount | `productArr[i].deliveryStockInSkuVoList[j].deliveryCount` | number | - | 发货数量 | A（L16189/16194） |
| list[i].deliveryStockInSkuVoList[j].stockInSku | `productArr[i].deliveryStockInSkuVoList[j].stockInSku` | object | - | 库存 SKU 包装 | A（L16191） |
| list[i].deliveryStockInSkuVoList[j].stockInSku.id | `productArr[i].deliveryStockInSkuVoList[j].stockInSku.id` | number | - | 库存 SKU id | A（L16191） |

**关键 A 级新发现**：
- Response 顶层是 `{ status, result: { list: [...] } }`（ObjectFactory 模式）
- list 项 = MedicalProduct 包装对象（含 `medicalProduct` + `deliveryStockInSkuVoList[]`）
- deliveryStockInSkuVoList 是**库存 SKU VO 列表**（不是 SKU 列表）
- 每项含 `stockInSku.id`（库存 SKU 标识）+ `deliveryCount`（发货数量）
- **list 项不是"可加工 SKU"，是"MedicalProduct + 其下库存 SKU + 待发数量"**

---

## 7. SKU 字段（表5）

| 字段 | 所属对象 | 类型 | 用途 | 等级 |
|------|------|------|------|------|
| medicalProduct.id | medicalProduct | number | MedicalProduct 业务标识 | A |
| stockInSku.id | stockInSku | number | 库存 SKU 业务标识 | A |
| deliveryCount | deliveryStockInSkuVoList[j] | number | 发货数量 | A |

**关键 A 级新发现**：
- 整个 controller.js 范围内，machineOrderCtrl SKU 相关字段只有 3 个：
  1. `medicalProduct.id`（medicalProduct 业务标识）
  2. `stockInSku.id`（库存 SKU 业务标识）
  3. `deliveryCount`（发货数量）
- 没有 skuCode / model1 / model2 / modelType / model1Name / model2Name / productCode / placeOrderStatus / useCount / refundCount

---

## 8. saveToBeProcessSkuInListOfProduct.json（表4）

| 项目 | 证据 | 等级 |
|------|------|------|
| API | `/admin/saveToBeProcessSkuInListOfProduct.json` | A |
| function | `$scope.saveStock`（controller.js L16181-16223） | A |
| controller | `machineOrderCtrl`（L16094-16258） | A |
| Request | `{ medicalProductStockBatctPoListJson: JSON.stringify(...) }`（L16212-16214） | A |
| 参数来源 | 遍历 `$scope.getProcessFactory.result.list`（L16185） | A |
| Response | `res.status`（L16216） | A |
| 保存对象 | medicalProductStockBatchPo[]（数组） | A |
| 成功后 | `Popup.notice("保存成功")` + `$scope.stockDetail = false`（L16219-16220） | A |
| 刷新 | **不调用** getCanBeProcessSku / selectInStoreMachineCenterCashflowVoList；不修改 memberFactory.items | A |
| 等级 | A | - |

**关键 A 级新发现**：
- 唯一调用点：controller.js L16212
- 唯一 controller：machineOrderCtrl
- 唯一调用 function：$scope.saveStock
- saveStock **不调用** getCanBeProcessSku（保存后不重新查 SKU）
- saveStock **不调用** selectInStoreMachineCenterCashflowVoList（保存后不重新查列表）
- saveStock **不修改** memberFactory.items（不影响 machineOrderOrder 状态）
- saveStock **只修改** $scope.stockDetail = false（关闭模态框）

---

## 9. Save API Request 完整结构（A 级 100% 收口）

L16181-16214 实际 Request 构造：

```
{
  medicalProductStockBatctPoListJson: JSON.stringify([
    {
      medicalProductId: productArr[i].medicalProduct.id,        // L16201
      medicalProductStocks: [
        {
          stockInSkuId: productArr[i].deliveryStockInSkuVoList[j].stockInSku.id,  // L16191
          deliveryCount: productArr[i].deliveryStockInSkuVoList[j].deliveryCount  // L16189
        }
      ]
    }
  ])
}
```

**关键 A 级新发现**：
- 实际 Request 是 JSON 字符串（JSON.stringify）
- 顶层 key = `medicalProductStockBatctPoListJson`（注意拼写 **StockBatctPo**，不是 StockBatchPo）
- 数组结构：medicalProductStockBatctPoListJson[]
- 每项 = `{ medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }`
- 是**两层嵌套数组**（按 medicalProduct 分组，每组下按 stockInSku 列）

**A 级新发现**：
- **没有任何 productId / productSkuId / skuId 字段**
- 字段命名严格：medicalProductId / stockInSkuId
- deliveryCount > 0 才推入（L16189）
- deliveryCount < 0 提示"发货数量必须大于0"并 return false（L16194-16197）
- deliveryCount == 0 跳过（L16198 空块）

---

## 10. Save Response（A 级 100% 收口）

- Response 顶层：`{ status, ... }`（L16216 直接证据）
- `res.status == 1` 失败：`Popup.notice(res.errmsg)`（L16217）
- `res.status != 1` 成功：`Popup.notice("保存成功")` + `$scope.stockDetail = false`（L16219-16220）
- 等级：A

---

## 11. Save 后刷新（A 级 100% 收口）

| 行为 | 是否执行 | 证据 | 等级 |
|------|------|------|------|
| 重新调用 getCanBeProcessSkuInListOfProduct.json | **否** | L16181-16223 全部源码中未出现 | A |
| 重新调用 selectInStoreMachineCenterCashflowVoList.json | **否** | L16181-16223 全部源码中未出现 | A |
| 修改 memberFactory.items | **否** | L16181-16223 全部源码中未出现 | A |
| 修改 getProcessFactory | **否** | L16181-16223 全部源码中未出现 | A |
| 修改 $scope.stockDetail | **是** | L16220 `stockDetail = false` | A |

**关键 A 级新发现**：
- saveToBeProcessSku 保存后**不刷新**任何 list / order 数据
- 唯一副作用：$scope.stockDetail = false（关闭 UI 模态）
- 一期复刻时必须严格按此协议实现

---

## 12. processProduct（A 级 100% 收口）

| 项目 | 证据 | 等级 |
|------|------|------|
| function | `$scope.processProduct(cashflowId, idx)`（L16173） | A |
| 参数 | (cashflowId, idx) | A |
| cashflowId 来源 | function 参数 | A |
| idx 来源 | function 参数（**未使用**） | A |
| 查询 SKU | `/admin/getCanBeProcessSkuInListOfProduct.json`（L16175） | A |
| 保存 SKU | **不调用** saveToBeProcessSku | A |
| Product | 通过 Response list 项暴露 | A |
| MedicalProduct | `list[i].medicalProduct.id`（L16201） | A |
| MachineCenterOrder | **不直接相关**（不修改 memberFactory.items） | A |
| MachineCenter | **不直接相关**（Request/Response 无 machineCenterId） | A |

**关键 A 级新发现**：
- processProduct 只做"打开可加工 SKU 列表"动作
- 实际选 SKU + 设置 deliveryCount + 保存 由 saveStock 完成
- 业务流程：processProduct → 用户编辑 deliveryCount → saveStock

---

## 13. saveStock（A 级 100% 收口）

| 项目 | 证据 | 等级 |
|------|------|------|
| function | `$scope.saveStock()`（L16181） | A |
| 参数 | 无（**不接受参数**） | A |
| 数据源 | `$scope.getProcessFactory.result.list`（L16185） | A |
| 读 MedicalProduct | `productArr[i].medicalProduct.id`（L16201） | A |
| 读 SKU | `productArr[i].deliveryStockInSkuVoList[j].stockInSku.id`（L16191） | A |
| 读 deliveryCount | `productArr[i].deliveryStockInSkuVoList[j].deliveryCount`（L16189） | A |
| 保存 API | `/admin/saveToBeProcessSkuInListOfProduct.json`（L16212） | A |
| 成功 | `$scope.stockDetail = false`（L16220） | A |
| 失败 | `Popup.notice(res.errmsg)`（L16217） | A |

**关键 A 级新发现**：
- saveStock **不接受参数**（不传 cashflowId / machineCenterId / idx）
- saveStock 全部数据从 processProduct Response 读取
- 业务动作 = "把 processProduct 返回的 SKU 发货数量持久化"

---

## 14. Product 对象边界（表6）

| 对象 | 已观察字段 | API | 用途 | 与 SKU 直接关系 | 等级 |
|------|------|------|------|------|------|
| MedicalProduct | id（L16201） | 嵌套在 list[i] | medicalProductId | 包含 deliveryStockInSkuVoList[] | A |
| Product | **未直接出现** | - | - | - | F |
| SKU | stockInSku.id（L16191）、deliveryCount（L16189） | 嵌套在 deliveryStockInSkuVoList[j] | stockInSkuId | 是 deliveryStockInSkuVoList 项 | A |

**关键 A 级新发现**：
- controller.js 范围内，machineOrderCtrl 完全没有出现 `Product` 对象
- 只有 `MedicalProduct`（含 id）和 `stockInSku`（含 id）
- "Product" 概念在本轮范围内 = **F（未观察）**
- "SKU" 实际 = `stockInSku`（库存 SKU）
- 业务关系：MedicalProduct → deliveryStockInSkuVoList[]（库存 SKU 列表）→ 标记为"待加工"

---

## 15. SKU → MachineCenterOrder 关系（表7/9）

| 起点 | 字段 | 终点 | 字段 | 关系 | 等级 |
|------|------|------|------|------|------|
| MedicalProduct.id | L16201 | MachineCenterOrder | - | **未直接引用** | F |
| Product | - | MachineCenterOrder | - | **未直接引用** | F |
| stockInSku.id | L16191 | MachineCenterOrder | - | **未直接引用** | F |
| medicalProductStockBatchPo[].medicalProductId | L16201 | MachineCenterOrder | - | **未直接引用** | F |

**关键 A 级新发现**：
- saveToBeProcessSkuInListOfProduct.json **完全不引用** MachineCenterOrder
- saveStock 不修改 memberFactory.items（不影响 machineCenterOrder.status）
- 推断业务语义：保存的是"库存出库 + 标记待加工"，**不是"开始加工订单"**
- "可加工 SKU" ≠ "可以开始加工的订单"
- "保存到待加工" ≠ "开始加工"

---

## 16. machineCenter 关系（F 维持）

- processProduct Request **不带** machineCenterId
- saveStock Request **不带** machineCenterId
- saveToBeProcessSkuInListOfProduct.json **不带** machineCenterId
- 等级：F（直接证据未观察）

**关键 A 级新发现**：
- saveToBeProcessSkuInListOfProduct.json **不传** machineCenterId
- 与 machineOrderBrokenCtrl（L16336-16339 用 cashflowId + machineCenterId）形成对比
- 推断：本 API 是"按 medicalProduct 分组的库存操作"，不依赖 machineCenter

---

## 17. cashflowId 关系（A 级 100% 收口）

- processProduct Request **带** cashflowId（L16175）
- saveStock Request **不带** cashflowId
- 等级：A

**关键 A 级新发现**：
- 业务流程：cashflow → 查询可加工 SKU → 编辑 → 保存（不传 cashflowId）
- 推断：后端通过 stockInSku → medicalProduct → cashflow 反向关联

---

## 18. medicalRecordId 关系（F 维持）

- processProduct Request **不带** medicalRecordId
- saveStock Request **不带** medicalRecordId
- 等级：F（直接证据未观察）

---

## 19. 批量结构（A 级 100% 收口）

**saveStock 实际 Request 结构**：

```
JSON.stringify([
  {
    medicalProductId: <number>,           // L16201
    medicalProductStocks: [
      {
        stockInSkuId: <number>,            // L16191
        deliveryCount: <number>            // L16189
      },
      ...
    ]
  },
  ...
])
```

**关键 A 级新发现**：
- 顶层数组：按 medicalProduct 分组（L16186-16204）
- 二层数组：medicalProductStocks[] 按 stockInSku 分组（L16188-16198）
- 仅当 deliveryCount > 0 才推入（L16189）
- deliveryCount < 0 直接 return false（L16194-16197）
- deliveryCount == 0 跳过（空 else 块 L16198）
- 全部 medicalProductStockBatchPo 为空时 `Popup.notice("发货数量必须大于0")` 并 return false（L16206-16209）

---

## 20. ID 边界（表8）

| 字段 | 所属对象 | 类型 | 是否主键 | 是否业务编号 | 证据 |
|------|------|------|------|------|------|
| medicalProduct.id | medicalProduct | number | F（未直接观察主键） | A（业务标识） | L16201 |
| stockInSku.id | stockInSku | number | F（未直接观察主键） | A（业务标识） | L16191 |
| cashflowId | （function 参数） | number | F | A | L16175 |
| productId | - | - | F | F | **未出现** |
| productSkuId | - | - | F | F | **未出现** |
| skuCode | - | - | F | F | **未出现** |

**关键 A 级新发现**：
- 整个 controller.js 范围内，SKU 相关字段 ID 只有 `medicalProduct.id` + `stockInSku.id` + `cashflowId`
- 没有 productId / productSkuId / skuCode 字段
- 字段命名严格遵循"medicalProductId" / "stockInSkuId"（不是 productId / skuId）

---

## 21. SKU API 成功后行为（表7）

| API | success | 本地赋值 | 重新查询 | 查询 API | 页面刷新 | 等级 |
|------|------|------|------|------|------|------|
| getCanBeProcessSkuInListOfProduct | `$scope.stockDetail = true` | stockDetail = true | 否 | - | 模态打开 | A |
| saveToBeProcessSkuInListOfProduct | `$scope.stockDetail = false` | stockDetail = false | 否 | - | 模态关闭 | A |

**关键 A 级新发现**：
- 两个 API 都不触发"重新查询列表"或"重新查询 SKU"
- 只控制 $scope.stockDetail 标志（UI 模态开关）
- 一期复刻时必须严格按此行为实现

---

## 22. 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 1 | getCanBeProcessSku API | A |
| 2 | 调用 function | A（processProduct） |
| 3 | Controller | A（machineOrderCtrl） |
| 4 | Query Request | A（cashflowId） |
| 5 | productId | F（未观察） |
| 6 | productSkuId | F（未观察） |
| 7 | sku/skuCode | F（未观察） |
| 8 | Query Response | A（result.list 顶层结构）/ A（item 结构） |
| 9 | SKU 对象 | A（stockInSku 包装） |
| 10 | SKU 字段 | A（stockInSku.id + deliveryCount + medicalProduct.id） |
| 11 | saveToBeProcessSku API | A |
| 12 | Save function | A（saveStock） |
| 13 | Save Request | A（medicalProductStockBatctPoListJson） |
| 14 | Save 字段 | A（medicalProductId + medicalProductStocks[stockInSkuId+deliveryCount]） |
| 15 | Save Response | A（res.status） |
| 16 | Save 后刷新 | A（不刷新） |
| 17 | processProduct | A |
| 18 | cashflowId 关系 | A（Request 带） |
| 19 | MedicalProduct 关系 | A（medicalProduct.id 唯一证据） |
| 20 | Product 关系 | F（未观察） |
| 21 | MachineCenterOrder 关系 | F（未直接引用） |
| 22 | machineCenterId 关系 | F（未参与） |
| 23 | SKU 批量结构 | A（两层嵌套数组） |
| 24 | SKU ID 边界 | A（medicalProduct.id + stockInSku.id） |
| 25 | Product / MedicalProduct / SKU 对象边界 | A（MedicalProduct + stockInSku 存在；Product 不存在） |
| 26 | 一期 SKU 数据协议边界 | A |

**统计**：A=22 / F=4 / B=0 / C=0 / D=0 / E=0 = 26

---

## 23. L1/L2/L3

- L1（controller / API / Request / Response / HTML）：A
- L2（业务语义）：E（"可加工 SKU" + "标记待加工"是基于 API 命名的推断）
- L3（数据库表 / 主键 / 索引）：F

---

## 24. R1-R6

- R1（直接字段引用）：A（medicalProduct.id / stockInSku.id / cashflowId / deliveryCount）
- R2（同 Response 对象）：A（list[i] 同 response.result.list）
- R3（同一业务实例）：A（processProduct → saveStock 同 getProcessFactory.result.list）
- R4（页面/State 导航）：A（$scope.stockDetail 模态开关）
- R5（业务推断）：0（未使用业务推断）
- R6（未观察）：F（Product / skuCode / machineCenterId / medicalRecordId）

---

## 25. 本轮新增事实

| 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|
| controller.js | L16173-16179 | processProduct 完整定义 | A |
| controller.js | L16175 | getCanBeProcessSkuInListOfProduct.json 唯一调用点 | A |
| controller.js | L16175 | Request = { cashflowId: cashflowId } | A |
| controller.js | L16177 | 成功后 $scope.stockDetail = true | A |
| controller.js | L16181-16223 | saveStock 完整定义 | A |
| controller.js | L16185 | 数据源 = $scope.getProcessFactory.result.list | A |
| controller.js | L16188 | productArr[i].deliveryStockInSkuVoList 数组 | A |
| controller.js | L16189 | deliveryCount > 0 推入 | A |
| controller.js | L16191 | stockInSku.id 库存 SKU id | A |
| controller.js | L16194 | deliveryCount < 0 return false | A |
| controller.js | L16201 | medicalProduct.id medicalProduct id | A |
| controller.js | L16206 | 空数组时 return false | A |
| controller.js | L16212-16214 | saveToBeProcessSku Request | A |
| controller.js | L16216 | res.status 响应处理 | A |
| controller.js | L16220 | 成功后 stockDetail = false | A |
| controller.js | L16212 | 不调用 getCanBeProcessSku / selectInStoreMachineCenterCashflowVoList | A |
| controller.js | L16220 | 不修改 memberFactory.items | A |

---

## 26. 历史纠错

S1-60（119 号）维护结论：
- machineOrderCtrl 包含 5 个写 API = startMachineCenterOrder / completeMachineCenterOrder / closeMachineCenterOrder / getCanBeProcessSkuInListOfProduct / saveToBeProcessSkuInListOfProduct → **本轮维持**
- getCanBeProcessSkuInListOfProduct 仅 1 个调用点（L16175） → **本轮维持**
- saveToBeProcessSkuInListOfProduct 仅 1 个调用点（L16212） → **本轮维持**

S1-60 未涉及 / 本轮新增：
- **本轮 A 级新发现**：saveStock 不调用任何 list / SKU 重新查询
- **本轮 A 级新发现**：saveStock 不修改 memberFactory.items（不影响 machineCenterOrder）
- **本轮 A 级新发现**：saveStock Request 字段严格 = medicalProductStockBatctPoListJson（JSON 字符串，两层嵌套数组）
- **本轮 A 级新发现**：medicalProductStockBatctPoListJson 拼写是 StockBatctPo（不是 StockBatchPo）
- **本轮 A 级新发现**：productArr[i].deliveryStockInSkuVoList 是核心数据结构
- **本轮 A 级新发现**：Product / skuCode / productId / productSkuId 在本轮范围全部 F

---

## 27. 一期复刻影响

A（可直接复刻）：
- 真实 2 个 API（getCanBeProcessSku / saveToBeProcessSku）
- 真实 Request / Response
- 真实 saveStock 数据结构（medicalProductStockBatctPoListJson 两层嵌套）
- 真实 processProduct / saveStock 完整定义
- 真实 $scope.stockDetail 模态开关协议
- 真实 ID 字段（medicalProduct.id / stockInSku.id / cashflowId）
- 真实 批量结构（按 medicalProduct 分组 + 按 stockInSku 分组）

E（业务语义抽象）：
- "可加工 SKU" 业务含义
- "标记待加工" 业务含义
- "MedicalProduct → 库存 SKU" 业务关系

F（数据库结构 / 缺失资源）：
- productId / productSkuId / skuCode 字段
- Product 对象
- 完整 route URL
- 数据库表 / 主键
- 后端算法
- 缺失 HTML 模板（machineOrderCtrl 页面 HTML）

---

## 28. 未解决问题

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | 可加工 SKU 查询 API 的完整 Request？ | A（cashflowId） |
| Q2 | 可加工 SKU Response？ | A（result.list + item 结构） |
| Q3 | productId / productSkuId 是否直接存在？ | F（未出现） |
| Q4 | SKU 真实标识是什么？ | A（stockInSku.id） |
| Q5 | save API Request？ | A（medicalProductStockBatctPoListJson JSON 字符串） |
| Q6 | 保存后的刷新？ | A（不刷新，只改 stockDetail） |
| Q7 | processProduct 与 SKU 的直接关系？ | A（processProduct 调 getCanBeProcessSku API） |
| Q8 | MedicalProduct ↔ SKU？ | A（medicalProduct → deliveryStockInSkuVoList[]） |
| Q9 | Product ↔ SKU？ | F（Product 未出现） |
| Q10 | MachineCenterOrder ↔ SKU？ | F（未直接引用） |
| Q11 | machineCenterId 是否参与？ | F（不参与） |
| Q12 | L3 数据库结构？ | F |

---

## 29. P0/P1

- P0 = 54
- P1 = 8
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 30. 121 号文件

- 路径：`E:\C\minimax\OptFlow PMS\121_S1-61_machineOrderCtrl_ProductSku_可加工SKU_数据协议_26项.md`
- 大小：本文件
- 新增行数：约 400+ 行

---

## 31. Git commit

待写完后执行：
- `git add -- 121_S1-61_machineOrderCtrl_ProductSku_可加工SKU_数据协议_26项.md`
- `git commit -m "docs(121): S1-61 machineOrderCtrl ProductSku可加工SKU数据协议收口"`
- `git push origin master`

---

## 32. Local / Remote

待 push 后验证 `git rev-parse HEAD == git rev-parse origin/master`。

---

## 33. tracked

期望：128 + 1 = 129

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

"S1-61 完成，已 Git 封口，立即停止，不进入 S1-62，等待老板下一条指令。"
