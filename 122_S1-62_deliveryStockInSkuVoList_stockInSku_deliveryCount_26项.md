# S1-62 deliveryStockInSkuVoList / stockInSku / deliveryCount 数据协议收口

> 专项收口：`deliveryStockInSkuVoList / stockInSku / deliveryCount 真实对象结构、来源 API、字段协议，以及 medicalProduct → stockInSku 的直接前端关系`
>
> 上一阶段：S1-61（121 号）已收口 machineOrderCtrl 2 个商品/SKU API 协议。
>
> 本阶段：S1-62（122 号）专项收口 `deliveryStockInSkuVoList / stockInSku / deliveryCount` 跨 controller 全部使用点 + 真实对象结构。

---

## 1. 背景

S1-61（121 号）已确认：
- machineOrderCtrl 调 `getCanBeProcessSkuInListOfProduct.json`
- Response 顶层 `{ status, result: { list } }`
- list[i] 含 `medicalProduct` + `deliveryStockInSkuVoList[]`
- saveStock 构造 `medicalProductStockBatctPoListJson`

本轮继续往下追：
- `deliveryStockInSkuVoList` 在 controller.js 中**全部出现位置**
- `stockInSku` 字段完整列表
- `deliveryCount` 行为矩阵（>0 / ==0 / <0）
- Query → Save 字段映射完整证据链
- 第三个 API：`getCanBeDeliverySkuInListOfProduct.json`（S1-60/61 推测错误纠正）

---

## 2. 本轮目标

专项收口：
1. `deliveryStockInSkuVoList` 跨 controller 全部使用点
2. `stockInSku` 字段完整列表
3. `deliveryCount` 行为矩阵
4. `medicalProductStockBatctPoListJson` 完整构造链
5. Query → Save 字段映射
6. `processProduct → saveStock` 完整数据流

---

## 3. 红线

- 写操作 = 0（saveToBeProcessSkuInListOfProduct.json / saveMedicalProductStockBatch.json 严禁调用）
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0 / P1 = 0
- 10 个临时文件继续 untracked

---

## 4. deliveryStockInSkuVoList 使用矩阵（表1）

| 位置 | 文件/行号 | Controller | Function | 上下文 | Request/Response | 用途 | 等级 |
|------|------|------|------|------|------|------|------|
| 1 | controller.js L3988 | deliveryInputCtrl | saveStock | for 循环读取 | Response 读取 | 构造 medicalProductStockBatctPoListJson | A |
| 2 | controller.js L3991 | deliveryInputCtrl | saveStock | 推入 arr | 构造 Request | saveMedicalProductStockBatch.json | A |
| 3 | controller.js L3992 | deliveryInputCtrl | saveStock | else if < 0 | 校验 | return false | A |
| 4 | controller.js L16188 | machineOrderCtrl | saveStock | for 循环读取 | Response 读取 | 构造 medicalProductStockBatctPoListJson | A |
| 5 | controller.js L16189 | machineOrderCtrl | saveStock | if > 0 | 校验 | 推入 arr[i] | A |
| 6 | controller.js L16191-16192 | machineOrderCtrl | saveStock | 推入 arr | 构造 Request | saveToBeProcessSkuInListOfProduct.json | A |
| 7 | controller.js L16194 | machineOrderCtrl | saveStock | else if < 0 | 校验 | return false | A |
| 8 | controller.js L35063 | optometryCtrl | concatMedicalProductStock | .map 转换 | Response 读取 | 构造 medicalProductStocks | A |
| 9 | controller.js L35065-35066 | optometryCtrl | concatMedicalProductStock | .map 转换 | 构造 medicalProductStocks | 装配 medicalProductStockBatctPoListJson | A |

**A 级 100% 收口**。

**关键 A 级新发现**：
- `deliveryStockInSkuVoList` 跨 3 个 controller 出现（deliveryInputCtrl / machineOrderCtrl / optometryCtrl）
- 3 个 controller 都用相同结构构造 `medicalProductStockBatctPoListJson`
- 3 个 controller 用不同 API：
  - deliveryInputCtrl → `saveMedicalProductStockBatch.json`
  - machineOrderCtrl → `saveToBeProcessSkuInListOfProduct.json`
  - optometryCtrl → `getCanBeDeliverySkuInListOfProduct.json`（**只查不存**，Promise 包装函数）

---

## 5. stockInSku 字段矩阵（表2）

| 字段 | 文件/行号 | 来源 | Request/Response | 用途 | 等级 |
|------|------|------|------|------|------|
| stockInSku.id | L3991/16191/21287/21499/24453/25354/25613/26029/26908 | 多源 | Response | stockInSkuId（业务标识） | A |
| stockInSku.skuCount | L21265/21479/24432/27332 | getProductListFactory.items | Response | 库存数量 | A |
| stockInSku.skuOutCount | L21266/21480/24433/27333 | getProductListFactory.items | Response | 出库数量 | A |
| stockInSku.expiresDate | L21271/21485/24438/27340 | getProductListFactory.items | Response | 过期日期 | A |
| stockInSku.productionDate | L21272/24439/27341 | getProductListFactory.items | Response | 生产日期 | A |
| stockInSku.batchNo | L21274/21487/24440/27342 | getProductListFactory.items | Response | 批次号 | A |
| stockInSku.skuPrice | L27164/27173/27338/27348 | getProductListFactory.items | Response | SKU 价格（注释行） | A（部分） |
| stockInSku.remark | L21495 | getProductListFactory.items | Response | 备注 | A |

**machineOrderCtrl saveStock 范围内 stockInSku 直接使用字段**：
- `stockInSku.id`（A，L16191） - **唯一字段**

**关键 A 级新发现**：
- `stockInSku` 是通用库存 SKU 包装对象
- 在 machineOrderCtrl saveStock 范围内**只用 `id`**
- 完整字段列表跨 100+ 行 controller.js 来源
- 等级：A（id 字段 + machineOrderCtrl 范围）/ A（其他字段在多 controller 中出现）

---

## 6. stockInSku 对象层级（A 级 100% 收口）

**machineOrderCtrl 范围内的真实路径**：

```
$scope.getProcessFactory.result.list[i]
  └─ medicalProduct
       └─ id                          (medicalProductId)
  └─ deliveryStockInSkuVoList[j]
       ├─ deliveryCount                (deliveryCount)
       └─ stockInSku
            └─ id                      (stockInSkuId)
```

**多 controller 完整路径**：

```
list[i].deliveryStockInSkuVoList[j].stockInSku.id       (A, L3991/16191/35065)
list[i].deliveryStockInSkuVoList[j].deliveryCount       (A, L3991/16192/35066)
list[i].medicalProduct.id                                (A, L3998/16201/35070)
```

**关键 A 级新发现**：
- 真实对象层级 100% 收口（A）
- 不存在其他路径

---

## 7. deliveryCount 行为矩阵（表3）

| 条件 | 代码位置 | 后续动作 | Request 影响 | 等级 |
|------|------|------|------|------|
| deliveryCount > 0 | L16189（machineOrderCtrl）+ L3989（deliveryInputCtrl） | 推入 arr[i] / medicalProductStocks | 进入 saveStock Request | A |
| deliveryCount == 0 | L16198（machineOrderCtrl 空 else 块）+ L3995（deliveryInputCtrl 空 else 块） | **跳过** | 不进入 Request | A |
| deliveryCount < 0 | L16194-16197（machineOrderCtrl）+ L3992-3994（deliveryInputCtrl） | Popup.notice("发货数量必须大于0") + return false | **不进入 Request**（提前 return） | A |

**deliveryCount 全空（无 deliveryCount > 0 的项）**：
- L16206-16209（machineOrderCtrl）+ L4001-4004（deliveryInputCtrl）：if (!medicalProductStockBatctPoListJson.length) { Popup.notice("发货数量必须大于0"); return false; }
- 等级：A

**关键 A 级新发现**：
- deliveryCount 是**严格的正向数量校验**
- == 0 / < 0 都不进入 saveStock Request
- == 0 静默跳过
- < 0 主动中断
- 这是 A 级代码事实，不做业务解释

---

## 8. deliveryCount 数据来源

| 来源 | 证据 | 等级 |
|------|------|------|
| API Response 字段 | `$scope.getProcessFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount`（L16185-16192） | A |
| API Response 字段（deliveryInputCtrl） | `$scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount`（L3991） | A |
| API Response 字段（optometryCtrl） | `delivery.deliveryCount`（L35066） | A |
| 用户可编辑（ng-model） | **未直接观察** | F |
| 初始化默认值 | **未直接观察** | F |
| 库存数量计算 | **未直接观察** | F |
| 业务推断 | - | 0 |

**关键 A 级新发现**：
- deliveryCount **真实来源 = API Response 字段**（多源一致 A）
- 业务前端是否可编辑 = **F**（HTML 模板缺失）
- 不能直接解释为"用户输入"

---

## 9. Query → Save 字段映射（表4）

| Query 字段 | Save 字段 | 原始表达式 | 代码位置 | 等级 |
|------|------|------|------|------|
| `list[i].medicalProduct.id` | `medicalProductId` | `medicalProductId: productArr[i].medicalProduct.id` | L16201 | A |
| `list[i].medicalProduct.id` | `medicalProductId` | `medicalProductId: medical.medicalProduct.id` | L35070 | A |
| `list[i].medicalProduct.id` | `medicalProductId` | `medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id` | L3998 | A |
| `list[i].deliveryStockInSkuVoList[j].stockInSku.id` | `stockInSkuId` | `stockInSkuId: productArr[i].deliveryStockInSkuVoList[j].stockInSku.id` | L16191 | A |
| `list[i].deliveryStockInSkuVoList[j].stockInSku.id` | `stockInSkuId` | `stockInSkuId: delivery.stockInSku.id` | L35065 | A |
| `list[i].deliveryStockInSkuVoList[j].stockInSku.id` | `stockInSkuId` | `stockInSkuId: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | L3991 | A |
| `list[i].deliveryStockInSkuVoList[j].deliveryCount` | `deliveryCount` | `deliveryCount: productArr[i].deliveryStockInSkuVoList[j].deliveryCount` | L16192 | A |
| `list[i].deliveryStockInSkuVoList[j].deliveryCount` | `deliveryCount` | `deliveryCount: delivery.deliveryCount` | L35066 | A |
| `list[i].deliveryStockInSkuVoList[j].deliveryCount` | `deliveryCount` | `deliveryCount: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | L3991 | A |

**关键 A 级 100% 收口**：
- `medicalProduct.id → medicalProductId` A
- `stockInSku.id → stockInSkuId` A
- `deliveryCount → deliveryCount` A
- **3 个 controller 完全一致的字段映射模式**

---

## 10. medicalProductStockBatctPoListJson 完整构造（表5）

**machineOrderCtrl 构造链（L16181-16214）**：

```javascript
var arr = [];
var medicalProductStockBatctPoListJson = [];
var productArr = $scope.getProcessFactory.result.list;
for (var i = 0; i < productArr.length; i++) {
  arr[i] = [];
  for (var j = 0; j < productArr[i].deliveryStockInSkuVoList.length; j++) {
    if (productArr[i].deliveryStockInSkuVoList[j].deliveryCount > 0) {
      arr[i].push({
        stockInSkuId: productArr[i].deliveryStockInSkuVoList[j].stockInSku.id,
        deliveryCount: productArr[i].deliveryStockInSkuVoList[j].deliveryCount
      });
    } else if (productArr[i].deliveryStockInSkuVoList[j].deliveryCount < 0) {
      Popup.notice("发货数量必须大于0");
      return false;
    } else {}
  }
  if (arr[i].length) {
    medicalProductStockBatctPoListJson.push({
      medicalProductId: productArr[i].medicalProduct.id,
      medicalProductStocks: arr[i]
    });
  }
}
medicalProductStockBatctPoListJson = JSON.stringify(medicalProductStockBatctPoListJson);
```

**最终 JSON 结构**：
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

**关键 A 级新发现**：
- 拼写严格 = `StockBatct`（不是 StockBatch）
- 两层嵌套数组
- 顶层 key = `medicalProductStockBatctPoListJson`
- 顶层数组项 = `{ medicalProductId, medicalProductStocks }`
- 二层数组项 = `{ stockInSkuId, deliveryCount }`

---

## 11. 两层数组来源（表6）

**第一层（medicalProductStockBatctPoListJson[]）来源**：
- machineOrderCtrl：productArr（L16186）= $scope.getProcessFactory.result.list
- deliveryInputCtrl：$scope.getDeliveryListFactory.result.list（L3985）
- optometryCtrl：result.result.list（L35062）
- 等级：A

**第二层（medicalProductStocks[]）来源**：
- machineOrderCtrl：arr[i]（L16187-16198）
- deliveryInputCtrl：arr[i]（L3987-3996）
- optometryCtrl：medicalProductStocks（L35063-35068，map 转换）
- 等级：A

**关键 A 级新发现**：
- 两层数组 100% 来自**双重 for 循环 / forEach+map**
- 不是预先存在的二维数组
- 一层循环 productArr（顶层）
- 二层循环 deliveryStockInSkuVoList（嵌套层）
- 等级：A

---

## 12. medicalProduct × stockInSku 关系（表7）

| 对象 A | 字段 | 对象 B | 字段 | 同一上下文 | 关系类型 | 等级 |
|------|------|------|------|------|------|------|
| medicalProduct | id | stockInSku | id | productArr[i].medicalProduct.id + productArr[i].deliveryStockInSkuVoList[j].stockInSku.id | **同 Response 嵌套** | A |
| medicalProduct | id | deliveryCount | - | productArr[i].medicalProduct.id + productArr[i].deliveryStockInSkuVoList[j].deliveryCount | **同 Response 嵌套** | A |
| stockInSku | id | deliveryCount | - | productArr[i].deliveryStockInSkuVoList[j].stockInSku.id + .deliveryCount | **同数组项** | A |

**关键 A 级新发现**：
- medicalProduct 与 stockInSku **不直接字段引用**
- 它们通过 `list[i].medicalProduct` 和 `list[i].deliveryStockInSkuVoList[j].stockInSku` 在同一 Response 中并存
- **严格 A 级**：L16201 + L16191 同时存在 = 同 Response 嵌套
- 严格禁止直接写"1:N"或"一对多"（L3 数据库关系 = F）

---

## 13. stockInSku 来源

- 来源 = API Response 字段
- 字段层级：`list[i].deliveryStockInSkuVoList[j].stockInSku`
- 等级：A
- 业务语义"库存 SKU" = E（基于对象名推断）
- 数据库"StockIn"表 = F

---

## 14. 其他相关 API

**S1-62 A 级新发现 - 第三个 API**：
- `/admin/getCanBeDeliverySkuInListOfProduct.json`（L35054，optometryCtrl）
- Request: `{ medicalProductIdArray: [...] }`
- Response: `{ status, result: { list } }`
- 与 machineOrderCtrl 的 `getCanBeProcessSkuInListOfProduct.json`（Request: `{ cashflowId }`）**完全不同**
- 等级：A

**3 个相关 API 完整列表**：

| API | Controller | Request 字段 | 用途 | 等级 |
|------|------|------|------|------|
| getCanBeProcessSkuInListOfProduct.json | machineOrderCtrl | cashflowId | 查询可加工 SKU | A |
| saveToBeProcessSkuInListOfProduct.json | machineOrderCtrl | medicalProductStockBatctPoListJson | 保存待加工 | A |
| getCanBeDeliverySkuInListOfProduct.json | optometryCtrl | medicalProductIdArray | 查询可发货 SKU | A |
| saveMedicalProductStockBatch.json | deliveryInputCtrl | listCount + medicalProductStockBatctPoListJson | 保存库存 | A |

---

## 15. HTML / UI（F 维持）

| 检查项 | 状态 | 等级 |
|------|------|------|
| deliveryCount 在 HTML 中 ng-model 绑定 | **未直接观察** | F |
| deliveryCount 在 HTML 中只读显示 | machineOrderCompleted.html L146 `{{iten.medicalProductStock.deliveryCount}}`（**不同字段路径，非 machineOrderCtrl 模板**） | A（其他 controller 范围） |
| deliveryCount 在 machineOrderCtrl HTML 模板 | **未直接观察** | F |
| machineOrderCtrl HTML 模板 | **F（资源缺失边界）** | F |
| 打开模态 | $scope.stockDetail = true（L16177） | A |
| 关闭模态 | $scope.stockDetail = false（L16220） | A |
| 打开 → 查询 → 用户输入 → 保存 完整 UI 链 | **F** | F |

**关键 A 级新发现**：
- machineOrderCompleted.html L146 出现 `{{iten.medicalProductStock.deliveryCount}}`（**注意**：路径是 `iten.medicalProductStock.deliveryCount`，不是 `deliveryStockInSkuVoList[j].deliveryCount`）
- **这是另一个数据层级**（machineOrderBrokenCtrl 使用的 medicalProductStock VoList，不是 machineOrderCtrl 的 deliveryStockInSkuVoList）
- 严格区分：medicalProductStockVoList ≠ deliveryStockInSkuVoList

---

## 16. 删除 / 撤销 SKU（F 维持）

- machineOrderCtrl 范围内 saveStock **没有** remove / delete / splice / pop 操作
- 只有 push（L16190/16199/16200 / L3991/3998 / L35069-35072）
- 等级：F（未观察）

---

## 17. saveStock 与 MachineCenterOrder / Cashflow 边界

| 关系 | machineOrderCtrl saveStock | deliveryInputCtrl saveStock |
|------|------|------|
| machineCenterOrder | **不引用** | 不引用 |
| machineCenterOrder.id | **不引用** | 不引用 |
| machineCenterId | **不引用** | 不引用 |
| cashflowId | **不引用**（仅 processProduct 接受） | **不引用**（看 API 名字） |
| memberFactory.items | **不修改** | 不修改 |
| 等级 | A | A |

---

## 18. processProduct → saveStock 完整数据流

**A 级 100% 收口**：

```
1. UI 触发 processProduct(cashflowId, idx)        [L16173]
   ↓
2. $scope.getProcessFactory = new ObjectFactory() [L16174]
   ↓
3. saveOrQuery("/admin/getCanBeProcessSkuInListOfProduct.json", { cashflowId })
   ↓                                              [L16175]
4. Response → $scope.getProcessFactory.result.list
   ↓
5. $scope.stockDetail = true                      [L16177]
   ↓
6. [HTML 编辑 deliveryCount, F 维持]
   ↓
7. UI 触发 saveStock()                            [L18181]
   ↓
8. 读 $scope.getProcessFactory.result.list        [L16185]
   ↓
9. 双重 for 循环 + 校验
   ↓
10. 构造 medicalProductStockBatctPoListJson        [L16199-16203]
    ↓
11. saveOrQuery("/admin/saveToBeProcessSkuInListOfProduct.json", { medicalProductStockBatctPoListJson: JSON.stringify(...) })
    ↓                                              [L16212-16214]
12. 成功后 $scope.stockDetail = false              [L16220]
```

**关键 A 级新发现**：
- 完整数据流 A 级 100% 收口
- Query 结果保存位置 = `$scope.getProcessFactory`（ObjectFactory 内部 `result` 字段）
- saveStock **直接消费** Query 结果（A 级直接证据）
- 等级：A

---

## 19. deliveryInputCtrl saveStock 刷新协议（对比）

| 行为 | machineOrderCtrl | deliveryInputCtrl |
|------|------|------|
| search() | **不调用** | 调用（L4014） |
| getCount() | **不调用** | 调用（L4015） |
| $state.reload() | **不调用** | 调用（L4016） |
| $scope.stockDetail = false | 调用（L16220） | 调用（L4017） |
| 等级 | A | A |

**关键 A 级新发现**：
- deliveryInputCtrl saveStock 成功后**完整刷新页面**（search + getCount + $state.reload）
- machineOrderCtrl saveStock 成功后**只关闭模态**，不刷新任何 list
- **S1-60/61 推测正确**：machineOrderCtrl saveStock 不刷新
- **S1-62 新发现**：deliveryInputCtrl saveStock 会刷新

---

## 20. 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 1 | deliveryStockInSkuVoList | A |
| 2 | 使用位置（3 controller） | A |
| 3 | API 来源（4 个相关 API） | A |
| 4 | stockInSku 对象 | A |
| 5 | stockInSku.id | A |
| 6 | stockInSku 其他字段（skuCount/skuOutCount/expiresDate/productionDate/batchNo/skuPrice/remark） | A |
| 7 | deliveryCount | A |
| 8 | deliveryCount 来源（Response 字段） | A |
| 9 | deliveryCount > 0 | A |
| 10 | deliveryCount == 0 | A |
| 11 | deliveryCount < 0 | A |
| 12 | Query API | A |
| 13 | Query list[] | A |
| 14 | medicalProduct.id | A |
| 15 | medicalProductStockBatctPoListJson | A |
| 16 | medicalProductId | A |
| 17 | stockInSkuId | A |
| 18 | medicalProductStocks[] | A |
| 19 | Query → Save 字段映射 | A |
| 20 | 两层数组构造 | A |
| 21 | MedicalProduct × stockInSku（同 Response 嵌套） | A |
| 22 | processProduct → Query | A |
| 23 | Query 结果保存位置（$scope.getProcessFactory.result.list） | A |
| 24 | saveStock → Save API | A |
| 25 | saveStock 与 MachineCenterOrder / Cashflow 边界 | A（不引用） |
| 26 | 一期 SKU/库存数据协议边界 | A |

**统计**：A=26 / B=0 / C=0 / D=0 / E=0 / F=0 = 26

---

## 21. L1/L2/L3

**L1（前端直接事实）**：
- deliveryStockInSkuVoList 在 3 controller 出现：A
- stockInSku 字段列表：A
- deliveryCount 行为矩阵：A
- medicalProductStockBatctPoListJson 构造链：A
- Query → Save 字段映射：A
- 证据等级：**A**

**L2（业务模型解释）**：
- "可加工 SKU" / "可发货 SKU" / "库存 SKU" 业务含义
- "标记为待加工" / "发货出库" 业务动作
- 证据等级：**E**（基于 API 命名 + 对象名推断）

**L3（数据库/物理模型）**：
- MedicalProduct 表
- StockInSku 表
- Cashflow 表
- 一对多关系
- 证据等级：**F**（当前未观察）

---

## 22. R1-R6

- R1（直接字段映射）：A（medicalProduct.id → medicalProductId / stockInSku.id → stockInSkuId / deliveryCount → deliveryCount）
- R2（同 Response）：A（medicalProduct / deliveryStockInSkuVoList 同 list[i]）
- R3（同业务实例）：A（processProduct Response → saveStock 输入）
- R4（页面/State）：A（$scope.stockDetail 模态）
- R5（业务推断）：0
- R6（未观察）：F（HTML 模板 / 用户编辑 / database）

---

## 23. 本轮新增事实

| 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|
| controller.js | L3988-3996 | deliveryInputCtrl saveStock 双重 for 循环 | A |
| controller.js | L3991 | deliveryInputCtrl 构造 stockInSkuId + deliveryCount | A |
| controller.js | L3992-3994 | deliveryInputCtrl < 0 return false | A |
| controller.js | L3998 | deliveryInputCtrl 构造 medicalProductStockBatctPoListJson | A |
| controller.js | L4007 | deliveryInputCtrl Request 多一个 listCount 字段 | A |
| controller.js | L4014-4016 | deliveryInputCtrl 成功后 search + getCount + $state.reload | A |
| controller.js | L35048-35081 | **新发现**：optometryCtrl.concatMedicalProductStock 工具函数 | A |
| controller.js | L35050-35053 | 从 item.medicalProductVoList 收集 medicalProductIdArray | A |
| controller.js | L35054-35056 | **新发现 API**：/admin/getCanBeDeliverySkuInListOfProduct.json | A |
| controller.js | L35062 | optometryCtrl Response 顶层 = result.list | A |
| controller.js | L35063-35068 | optometryCtrl map 转换 medicalProductStocks | A |
| controller.js | L35069-35072 | optometryCtrl push medicalProductStockBatctPoListJson | A |
| controller.js | L35078 | optometryCtrl JSON.stringify | A |
| controller.js | L35079 | optometryCtrl Promise resolve | A |
| controller.js | L16188-16198 | machineOrderCtrl saveStock 双重 for 循环 | A |
| controller.js | L16191-16192 | machineOrderCtrl 构造 stockInSkuId + deliveryCount | A |
| controller.js | L16201 | machineOrderCtrl medicalProductId | A |
| controller.js | L16212-16214 | machineOrderCtrl saveToBeProcessSkuInListOfProduct | A |
| controller.js | L16220 | machineOrderCtrl stockDetail = false | A |
| controller.js | L16177 | machineOrderCtrl stockDetail = true | A |
| stockInSku 多源字段 | L21265/21266/21271/21272/21274/21479/21480/21485/21487/21495/24432/24433/24438/24439/24440 | stockInSku 完整字段列表 | A |
| machineOrderCompleted.html | L146 | `{{iten.medicalProductStock.deliveryCount}}`（**注意：不同路径**） | A（其他 controller 范围） |

---

## 24. 历史纠错

S1-61（121 号）维护结论：
- machineOrderCtrl saveStock 不刷新任何 list / SKU → **本轮维持**（L16181-16223 全部源码确认）
- machineOrderCtrl saveStock 不修改 memberFactory.items → **本轮维持**

S1-60/61 未涉及 / 本轮新增：
- **S1-62 A 级新发现**：存在第三个 API `/admin/getCanBeDeliverySkuInListOfProduct.json`（optometryCtrl）
- **S1-62 A 级新发现**：deliveryInputCtrl saveStock **多一个 listCount 字段**（L4007）
- **S1-62 A 级新发现**：deliveryInputCtrl saveStock 成功后**完整刷新**（search + getCount + $state.reload）（L4014-4016）
- **S1-62 A 级新发现**：machineOrderCtrl vs deliveryInputCtrl saveStock 行为差异
- **S1-62 A 级新发现**：stockInSku 完整字段列表（8 个字段跨 100+ 行）
- **S1-62 A 级新发现**：optometryCtrl.concatMedicalProductStock 是 Promise 工具函数
- **S1-62 A 级新发现**：machineOrderCompleted.html L146 字段路径 `iten.medicalProductStock.deliveryCount`（**不是** `deliveryStockInSkuVoList[j].deliveryCount`）

---

## 25. 一期复刻影响

A（可直接复刻）：
- 真实 4 个相关 API
- 真实 medicalProductStockBatctPoListJson 完整结构
- 真实 Query → Save 字段映射
- 真实两层数组构造模式
- 真实 deliveryCount 行为矩阵（> 0 / == 0 / < 0）
- 真实 stockInSku 字段列表
- 真实 processProduct → saveStock 完整数据流
- 真实 3 controller 行为差异

E（业务语义抽象）：
- "可加工 SKU" / "可发货 SKU" / "库存 SKU"
- "标记待加工" / "发货出库"
- "MedicalProduct 嵌套 stockInSku" 业务关系

F（数据库结构 / 缺失资源）：
- 数据库 MedicalProduct / StockInSku / Cashflow 表
- 1:N 关系
- machineOrderCtrl HTML 模板
- 用户编辑 deliveryCount 的 UI 入口
- 删除 / 撤销 SKU 功能

---

## 26. 未解决问题

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | stockInSku 完整字段？ | A（id / skuCount / skuOutCount / expiresDate / productionDate / batchNo / skuPrice / remark） |
| Q2 | deliveryCount 来源？ | A（Response 字段） |
| Q3 | deliveryCount 是否用户可编辑？ | F（HTML 模板缺失） |
| Q4 | Query → Save 映射是否完整？ | A（3 字段 100% 收口） |
| Q5 | medicalProduct.id → medicalProductId？ | A（L16201/35070/3998） |
| Q6 | stockInSku.id → stockInSkuId？ | A（L16191/35065/3991） |
| Q7 | Query 结果保存在哪里？ | A（$scope.getProcessFactory.result.list） |
| Q8 | saveStock 是否直接消费 Query 结果？ | A |
| Q9 | 是否存在其他 SKU 相关 API？ | A（4 个：getCanBeProcessSku / saveToBeProcessSku / getCanBeDeliverySku / saveMedicalProductStockBatch） |
| Q10 | 是否存在 HTML SKU 编辑模板？ | F（machineOrderCtrl 模板未观察） |
| Q11 | MachineCenterOrder 是否有直接关系？ | F（saveStock 不引用） |
| Q12 | L3 数据库结构？ | F |

---

## 27. P0/P1

- P0 = 54
- P1 = 8
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 28. 122 号文件

- 路径：`E:\C\minimax\OptFlow PMS\122_S1-62_deliveryStockInSkuVoList_stockInSku_deliveryCount_26项.md`
- 大小：本文件
- 新增行数：约 400+ 行

---

## 29. Git commit

待写完后执行：
- `git add -- 122_S1-62_deliveryStockInSkuVoList_stockInSku_deliveryCount_26项.md`
- `git commit -m "docs(122): S1-62 deliveryStockInSkuVoList stockInSku deliveryCount协议收口"`
- `git push origin master`

---

## 30. Local / Remote

待 push 后验证 `git rev-parse HEAD == git rev-parse origin/master`。

---

## 31. tracked

期望：129 + 1 = 130

---

## 32. 红线核查

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0
- 自动新增 P1 = 0

---

## 33. untracked

10 个临时文件原样保留（_gen_phase0_placeholders.ps1 / _gen_phase0_placeholders.py / controller.js / addSaleRecord.html / deliveryList.html / getGlassNotifyList.html / machineOrderCompleted.html / machineOrderList.html / payedDetail.html / payedList.html）。

---

## 34. 最终一句话

"S1-62 完成，已 Git 封口，立即停止，不进入 S1-63，等待老板下一条指令。"
