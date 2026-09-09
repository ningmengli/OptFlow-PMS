# S1-149：Product / SKU / MedicalProduct / Stock / Brand / Category 物资域总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 211 个 MD / 不修改历史
> 关联：S1-129 / S1-142 / S1-143 / S1-145 / S1-146 / S1-148

---

## 目录

- §0 审计范围
- §1 Product 全量
- §2 SKU / StockInSku
- §3 MedicalProduct
- §4 Stock / MedicalProductStock
- §5 F3-F6 4 个 API 完整链
- §6 Brand / Category
- §7 MachineCenter / objectId runtime mutation
- §8 字段矩阵
- §9 对象交叉桥
- §10 Product/SKU ↔ Sale
- §11 ↔ Cashflow
- §12 ↔ Delivery
- §13 ↔ Machine
- §14 Write 生命周期
- §15 Source Trace
- §16 Object Type 分类
- §17 生命周期 DAG
- §18 Controller 消费矩阵
- §19 26 项证据矩阵
- §20 历史差异
- §21 V4.4 物资域规格
- §22 F / 未确认
- §23 Git / 完整性

---

## §0 审计范围

本轮把 Product / SKU / MedicalProduct / Stock / Brand / Category / MachineCenter 物资域
作为**前端可证明的对象、字段、Request、Response、State、API 和桥接关系**进行完整只读审计：

- 区分 **Product (普通商品)** vs **MedicalProduct (医疗商品)** 严格分开
- 验证 F3-F6 4 个 API 完整字段链
- 验证 `medicalProduct.objectId` 是 **runtime mutation**（非原始 Response 字段）
- 8+ Controller 消费矩阵
- 多个 NOT FOUND Controller 命名误导识别
- 26 项证据矩阵
- 历史 S1-129/142/143/145/146/148 误判核对

---

## §1 Product 全量

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `product` (全词) | **250** | A |
| `productId` | **58** | A |
| `productName` | **101** | A |
| `productType` | **94** | A |
| `productModel` | **7** | A |
| `productVo` | **0** | A |
| `productUnit` | 0 | A |

**重要发现**：`productVo` 字符级 0 命中（同 customerVo/patientVo/cashflowVo/medicalProductVo 模式）。
Product 实际通过 `res.product.*` / `item.product.*` 形式被消费。

### §1.2 Product API 全量

| API | 命中数 | R/W |
|---|---:|---|
| `getProduct*.json` | **33** | R |
| `getProductVo*.json` | 8 | R |
| `selectProduct*.json` | 5 | R |
| `updateProduct*.json` | 3 | W |
| `createProduct*.json` | 5 | W |
| `deleteProduct*.json` | 2 | W |
| `saveProduct*.json` | 1 | W |

### §1.3 Product 真实字段（顶层，排除 medicalProduct）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `product.id` | 12 命中 | A |
| `product.brand` | 1 命中 | A |
| `product.category` | 1 命中 | A |
| `product.productType` | 3 命中 | A |
| `product.name` | 0 命中 | F |
| `product.price` | 0 命中 | F |
| `product.brandId` | 0 命中 | F |
| `product.categoryId` | 0 命中 | F |
| `product.skuList` | 0 命中 | F |
| `product.productModel` | 0 命中 | F |

**关键发现**：
- `product.brand` / `product.category` 各 1 命中 — **Object 引用存在**
- `product.brandId` / `product.categoryId` 0 命中 — **ID 字段不存在**
- Product 实际没有顶层 brandId/categoryId 字段桥，是 Object 引用

---

## §2 SKU / StockInSku

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `skuId` | **122** | A |
| `skuVo` | 2 | A |
| `skuList` | **143** | A |
| `stockInSku` | **95** | A |
| `stockInSkuId` | **76** | A |
| `stockInSkuVoList` | **39** | A |
| `stockInSkuList` (UI) | **216** | A (Scope) |
| `deliveryStockInSkuVoList` | 11 | A |
| `getSku*.json` | 2 | A |

### §2.2 SKU Object 字段级

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `stockInSku.id` | L3989/L3991/L16191/L35063 (F4 Response) | A |
| `stockInSku.stockInSkuId` | 派生 | A |
| `skuVo` | 2 命中（命名误导？需复验） | C |

**重要发现**：
- `stockInSku.id` 是 SKU 实际主键（A）
- **`stockInSkuId` ≠ `skuId`** — `stockInSkuId` 是 stockInSku 表的 ID（Request 字段），`skuId` 是 Product 维度 SKU ID
- **`deliveryStockInSkuVoList[].stockInSku.id` 是 F4 Response 主入口**（A）

### §2.3 stockInSkuList 是 UI 临时数组

- **216 命中**（最高频）— 但**全部是 Scope UI 临时数组**
- L21170 / L22270 / L24355 / L24578 等：4 个 stockIn/Out Controller 大量 `$scope.stockInSkuList = []`
- L21317 / L21527 / L22403 / L24503: `for (var i = 0; i < $scope.stockInSkuList.length; i++)` 遍历
- L21318: `stockOutSkuListJson[i].outCount = $scope.stockInSkuList[i].outCount`
- L22405/L22406: `outCount / productSkuId` (字段写入)
- L22411: `console.log($scope.stockInSkuList)` (调试)
- L21341/L21546/L22432/L24525: `splice` (删除)
- L23510: `$scope.obj.stockInSkuListJson = JSON.stringify(stockListJson)` (序列化输出)
- **本质**：stockInSkuList 是 **UI 临时数组**，不是独立 Object

### §2.4 SKU 真实身份

- `skuId` 在 controller.js 中**大部分是 product.sku 上下文的 .id 派生**（实际是 stockInSku.id）
- **`stockInSkuId` = 76 命中** — 是 StockInSku 表 ID（数据库语义更强）
- **`skuId` = 122 命中** — 是 Product 维度 SKU ID（业务语义更强）
- **两者不能合并**

### §2.5 SKU 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `stockInSkuId`, `skuId` | A |
| B. Response VO | `stockInSkuVoList`, `deliveryStockInSkuVoList` | A |
| C. Request | `medicalProductIdArray` (F4), `medicalProductMachineCenterPoListJson` (F3/F6) | A |
| D. State | - | F |
| E. UI | `$scope.stockInSkuList` (216 命中, Scope 临时) | A (UI) |
| F. Runtime | - | F |

---

## §3 MedicalProduct

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `medicalProduct` (全词) | **96** | A |
| `medicalProductId` | **24** | A |
| `medicalProductName` | **0** | A |
| `medicalProductModel` | 0 | A |
| `medicalProductVo` | **0** | A |
| `medicalProductVoList` | **21** | A |
| `medicalProductVoListOfModel` | 17 | A |
| `medicalProductStock` | 0 | A |
| `medicalProductStockId` | **4** | A (Request) |
| `medicalProductStockBatctPoListJson` | **28** | A (Request) |
| `medicalProductDelivery` | 7 | A |
| `medicalProductDeliveryVoList` | 0 | A |

**重要发现**：
- **`medicalProductVo` 0 命中**（同 productVo / customerVo 模式）
- **`medicalProductName` 0 命中**（保持 S1-145 修正）
- **`medicalProductStock` 0 命中**（但 medicalProductStockId=4 命中 — Request 字段）
- `medicalProductStockBatctPoListJson` = 28 — F5 / F4 主要 Request 字段

### §3.2 MedicalProduct 真实字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `medicalProduct.id` | **27 命中** (含 .id) | A |
| `medicalProduct.objectId` | **7 命中** (runtime mutation) | A |
| `medicalProduct.rateFee` | 2 命中 | A |
| `medicalProduct.medicalRecordId` | 1 命中 | A (L16191 派生) |
| `medicalProduct.name` | 0 命中 | F |
| `medicalProduct.price` | 0 命中 | F |
| `medicalProduct.brand` | 0 命中 | F |
| `medicalProduct.category` | 0 命中 | F |
| `medicalProduct.machineCenterId` | 0 命中 (顶层) | F |
| `medicalProduct.productId` | 0 命中 | F |
| `medicalProduct.deliveryCount` | 0 命中 (顶层) | F |

### §3.3 MedicalProduct API 全量

| API | 命中数 | R/W |
|---|---:|---|
| `saveMedicalProduct*.json` | 6 | W |
| `getMedicalProduct*.json` | 6 | R |
| `selectMedicalProduct*.json` | 5 | R |
| `getMedicalProductModelList.json` | 1 | R |
| `getMedicalProductVoList.json` | 4 | R |
| F3 `getMedicalProductMachineCenterVoList.json` | 1 | R |
| F4 `getCanBeDeliverySkuInListOfProduct.json` | 2 | R |
| F5 `saveMedicalProductStockBatch.json` | 1 | W |
| F6 `sendMedicalProductToMachineCenter.json` | 1 | W |

### §3.4 MedicalProduct 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `medicalProductId`, `medicalProduct.id` | A |
| B. Response VO | `medicalProductVoList`, `medicalProductVoListOfModel` | A |
| C. Request | `medicalProductStockBatctPoListJson`, `medicalProductMachineCenterPoListJson`, `medicalProductIdArray` | A |
| D. State | - | F |
| E. UI | - | F |
| F. Runtime Mutation | `medicalProduct.objectId` (L3854) | A |

---

## §4 Stock / MedicalProductStock

### §4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `stock` (全词) | **45** | A |
| `stockId` | **2** | A |
| `stockIn` | 14 | A |
| `stockOut` | 18 | A |
| `stockInSkuList` | **216** | A (Scope) |
| `stockBatch` | **0** | A |
| `stockBatchId` | **0** | A |
| `medicalProductStock` | **0** | A |
| `medicalProductStockId` | 4 | A (Request) |
| `stockCount` | 0 | A |

**重要发现**：
- **`stockBatch` / `stockBatchId` 0 命中** — StockBatch 概念在 controller.js 中**不存在**（命名误导）
- **`medicalProductStock` 0 命中** — 但 medicalProductStockId=4 命中（Request 字段）
- `stockId` 仅 2 命中 — Stock 实际不是独立 ID 实体
- `stockInSkuList` 216 命中（Scope UI 临时）

### §4.2 Stock API 全量

| API | 命中数 | R/W |
|---|---:|---|
| `getStock*.json` | **60** | R |
| `createStock*.json` | 19 | W |
| `updateStock*.json` | 15 | W |
| `deleteStock*.json` | 7 | W |
| `saveStock*.json` | 2 | W |
| `selectStock*.json` | 3 | R |
| `createMedicalStock*.json` | 2 | W |
| F5 `saveMedicalProductStockBatch.json` | 1 | W |
| F6 `sendMedicalProductToMachineCenter.json` | 1 | W |
| `createMedicalStockLossOfSmallVersion.json` | 1 | W (ReportLoss) |

### §4.3 Stock 真实字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `stockInSkuList[].outCount` | L21318/L21528/L22405 | A |
| `stockInSkuList[].productSkuId` | L22406 | A |
| `stockInSkuList[].transferCount` | L24504 | A |
| `stockOutSkuListJson[i].outCount` | L21318 | A |
| `obj.stockInSkuListJson` | L23510 | A |
| `stockId` | 2 命中（独立 ID 证据弱） | C |
| `stockCount` | 0 命中 | F |

### §4.4 MedicalProductStock 结论

- **`medicalProductStock` 0 命中** — 实际不存在独立 Object
- `medicalProductStockId` 4 命中 — 实际是 **Request 字段**（不是 Object 主键）
- F5 `saveMedicalProductStockBatch` 实际是 **MedicalProductStockBatch 持久化**（不是单一 stock）
- `medicalProductStockBatctPoListJson` 28 命中 — 是 F4/F5 Request 核心字段
- **结论**：MedicalProductStock 是 **Request Payload**，不是独立 ID 实体

### §4.5 Stock 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `stockInSkuId`, `stockId` (弱) | A / C |
| B. Response VO | `stockInSkuVoList`, `deliveryStockInSkuVoList` | A |
| C. Request | `medicalProductStockBatctPoListJson`, `obj.stockInSkuListJson` | A |
| D. State | - | F |
| E. UI | `$scope.stockInSkuList` (216 命中) | A (UI) |
| F. Runtime | - | F |

---

## §5 F3-F6 4 个 API 完整链

### §5.1 F3: getMedicalProductMachineCenterVoList.json (L3836)

| 项 | 值 |
|---|---|
| API | `/admin/getMedicalProductMachineCenterVoList.json` |
| Controller | deliveryInputCtrl (L3812) |
| Request | `{ medicalProductMachineCenterPoListJson: JSON.stringify(arr) }` |
| 字段源 | `medicalProductMachineCenterPoList` 数组 (L3817-L3828) |
| 每个 item | `{ medicalProductId: arr[i].medicalProduct.id, machineCenterId: arr[i].medicalProduct.objectId }` |
| Response | `getCenterListFactory.result.object` (machineCenterVoList) |
| 等级 | A |

**F3 核心字段源**：
```
$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i]
  ├── medicalProduct.id           (A 真实字段)
  └── medicalProduct.objectId     (A runtime mutation from lockMachineCenter.id)
```

### §5.2 F4: getCanBeDeliverySkuInListOfProduct.json (L3885/L35054)

| 项 | 值 |
|---|---|
| API | `/admin/getCanBeDeliverySkuInListOfProduct.json` |
| Controller | deliveryInputCtrl (L3812) + optometryCtrl (L34776) |
| Request | `{ medicalProductIdArray: medicalProductIdArray }` |
| 字段源 | `arr[i].medicalProduct.id` (L3873 当 objectId==null 时 push) |
| Response | `result.result.list[].deliveryStockInSkuVoList[].stockInSku.id + deliveryCount` |
| 等级 | A |

**F4 完整链**：
```
medicalProductIdArray (筛选)
  → F4 getCanBeDeliverySkuInListOfProduct
  → result.result.list[].deliveryStockInSkuVoList[]
       ├── stockInSku.id
       └── deliveryCount
  → medicalProductStockBatctPoListJson
  → saveMedicalProductStockBatch (F5)
```

### §5.3 F5: saveMedicalProductStockBatch.json (L4007)

| 项 | 值 |
|---|---|
| API | `/admin/saveMedicalProductStockBatch.json` |
| Controller | deliveryInputRecordCtrl (L4024) |
| Request | `{ listCount: ..., medicalProductStockBatctPoListJson: ... }` |
| 字段源 | F4 Response `getDeliveryListFactory.result.list[].deliveryStockInSkuVoList[]` |
| 每个 item | `{ stockInSkuId: ..., deliveryCount: ... }` |
| Response | 成功 Popup.notice('保存成功') + search() + $state.reload() |
| 等级 | A |

**F5 实际写入字段**（L3989-L3991 派生）：
```javascript
arr[i].push({
    stockInSkuId: $scope.getDeliveryListFactory.result.list[i]
                  .deliveryStockInSkuVoList[j].stockInSku.id,
    deliveryCount: $scope.getDeliveryListFactory.result.list[i]
                  .deliveryStockInSkuVoList[j].deliveryCount
});
```

### §5.4 F6: sendMedicalProductToMachineCenter.json (L3966)

| 项 | 值 |
|---|---|
| API | `/admin/sendMedicalProductToMachineCenter.json` |
| Controller | deliveryInputCtrl (L3812) |
| Request | `{ medicalProductMachineCenterPoListJson: ... }` |
| 字段源 | 同一 `medicalProductMachineCenterPoList` 数组 (L3817-L3828) |
| Response | 成功 Popup.notice('发送成功') + $state.reload() |
| 等级 | A |

### §5.5 F3-F6 完整数据流

```
waitingDeliveryList[].medicalProduct
    ↓ (F3/F6 字段源)
medicalProductMachineCenterPoList
  ├── { medicalProductId, machineCenterId=objectId }
    ↓ JSON.stringify
F3 getMedicalProductMachineCenterVoList → machineCenterVoList
F6 sendMedicalProductToMachineCenter → 工厂下单
    
    ↓ (F4 字段源)
medicalProductIdArray
    ↓
F4 getCanBeDeliverySkuInListOfProduct → result.result.list[].deliveryStockInSkuVoList
    ↓
medicalProductStockBatctPoListJson (F5 Request)
    ↓
F5 saveMedicalProductStockBatch → Stock 扣减
```

### §5.6 F3-F6 关键发现

1. **F3 与 F6 共享同一 `medicalProductMachineCenterPoList` 数组**（A）
2. **F4 派生 `medicalProductStockBatctPoListJson` 直接喂 F5**（A）
3. **F4 不会返回 medicalProduct.machineCenterId**（实际是 `deliveryStockInSkuVoList[]`）
4. **medicalProduct.objectId 是 machineCenterId 的派生来源**（A runtime mutation）

---

## §6 Brand / Category

### §6.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `brand` (全词) | **42** | A |
| `brandId` | **57** | A |
| `brandName` | **66** | A |
| `brandVo` | **0** | A |
| `category` (全词) | **36** | A |
| `categoryId` | **94** | A |
| `categoryName` | **77** | A |
| `productCategory` | 0 | A |
| `medicalProductCategory` | 0 | A |
| `getBrand*.json` | **20** | A |
| `getCategory*.json` | **18** | A |
| `selectBrand*.json` | 1 | A |

**重要发现**：
- **`brandVo` / `categoryVo` 0 命中**（同 productVo / medicalProductVo 模式）
- **0 命中 productCategory / medicalProductCategory** — Product 不直接含 category 字段
- 0 命中 saveBrand / saveCategory — 没有独立 Write
- 0 命中 selectCategory — 但 selectBrand=1

### §6.2 Brand / Category API 全量

| API | 命中 | R/W |
|---|---:|---|
| `getBrand*.json` | **20** | R |
| `getCategory*.json` | **18** | R |
| `selectBrand*.json` | 1 | R |
| `saveBrand*.json` | 0 | F |
| `saveCategory*.json` | 0 | F |
| `selectCategory*.json` | 0 | F |
| `updateBrand*.json` | 0 | F |
| `updateCategory*.json` | 0 | F |

### §6.3 Brand / Category 真实身份

- **Brand 实际是 列表/筛选器**（不是独立 ID 实体）：
  - `getBrand*.json` 20 命中 — 用于品牌下拉/筛选
  - `brandId` 57 命中 — 是 Request 字段（不是 Response 顶层 brandVo 字段）
  - `brandName` 66 命中 — 是 UI label
- **Category 实际是 列表/筛选器**（不是独立 ID 实体）：
  - `getCategory*.json` 18 命中 — 用于类别下拉/筛选
  - `categoryId` 94 命中 — 是 Request 字段
  - `categoryName` 77 命中 — 是 UI label

### §6.4 Product ↔ Brand/Category 字段

- `product.brand` = 1 命中 — Object 引用（A）
- `product.category` = 1 命中 — Object 引用（A）
- `product.brandId` = 0 命中 — 顶层 ID 字段 F
- `product.categoryId` = 0 命中 — 顶层 ID 字段 F

**重要**：Product 不通过 ID 字段引用 brand/category（Object 引用才是真实桥）。

### §6.5 13 类/50+ 品牌的运行时观察 vs 当前源码

- "13 类 / 50+ 品牌" 是**历史运行时数据**（不是当前源码事实）
- 本轮只承认 **`getBrand*.json` 20 调用 + `getCategory*.json` 18 调用**为字符级 A 级证据
- 实际类目/品牌数量需要 L3 后端验证（F）

---

## §7 MachineCenter / objectId runtime mutation

### §7.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `machineCenter` (全词) | **9** | A |
| `machineCenterId` | **26** | A |
| `objectId` | **7** | A (Runtime) |
| `lockMachineCenter` | **1** | A (Runtime) |

### §7.2 objectId 全部位置（7 命中 — S1-142 runtime mutation 完整保持）

| # | 行号 | 代码 | 等级 |
|---|---|---|---|
| 1 | L3821 | `if (arr[i].medicalProduct.objectId) {` | A |
| 2 | L3824 | `machineCenterId: arr[i].medicalProduct.objectId` | A (F3/F6 字段源) |
| 3 | L3854 | `$scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;` | **A ★ Runtime Mutation** |
| 4 | L3856 | `... = null;` (else branch) | A |
| 5 | L3873 | `if (arr[i].medicalProduct.objectId == null) { medicalProductIdArray.push(arr[i].medicalProduct.id); }` | A (F4 字段源) |
| 6 | L3899 | `if (arr[i].medicalProduct.objectId) { return false; }` | A |
| 7 | L3916 | `if (arr[i].medicalProduct.objectId == null) { return false; }` | A |

### §7.3 lockMachineCenter 完整位置（1 命中 — 不是 Object）

| 行号 | 代码 | 等级 |
|---|---|---|
| L3854 | `arr[i].lockMachineCenter.id` (作为 medicalProduct.objectId 的 source) | A |

**重大发现**：
- `lockMachineCenter` 仅 1 处 — 实际**不是独立 Object 容器**
- 它只是 `arr[i].lockMachineCenter.id` 单个字段访问
- 实际是 if/else 分支中的临时变量（machineOrder 列表项里的字段）

### §7.4 objectId runtime mutation 完整链（S1-142 保持）

```
arr[i] (waitingDeliveryList item)
  ├── lockMachineCenter.id (if has order)
  │     ↓
  │   medicalProduct.objectId = lockMachineCenter.id
  │     ↓
  │   后续: F3/F6 machineCenterId = objectId
  │
  └── lockMachineCenter 不存在 (else)
        ↓
      medicalProduct.objectId = null
        ↓
      后续: F4 medicalProductIdArray.push(medicalProduct.id)
```

### §7.5 MachineCenter 真实身份

- `machineCenter` 9 命中（顶层）
- `machineCenterId` 26 命中（Request 字段）
- **0 命中**：`machineCenterVo` / `machineCenterVoList`（但 F3 getMedicalProductMachineCenterVoList 是 medicalProductMachineCenterVoListJson）
- **0 命中**：独立 machineCenterListCtrl（NOT FOUND）
- **MachineCenter 实际不是独立 ID 实体**，是 F3/F6 Request 字段

### §7.6 Machine Controller 消费矩阵

| Controller | 行号 | product | medicalProduct | sku | stock | brand | category | mc | 等级 |
|---|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| machineOrderCtrl (L16094) | 16094 | 0 | 2 | 1 | 0 | 2 | 2 | 1 | A |
| machineOrderListCtrl (L4264) | 4264 | 5 | **26** | 0 | 0 | 0 | 0 | 0 | A |
| machineOrderCompletedCtrl | **NOT FOUND** | - | - | - | - | - | - | - | F |
| machineOrderWaitProcessCtrl (L16357) | 16357 | 8 | 0 | 5 | 6 | 3 | 3 | 1 | A |
| machineOrderBrokenCtrl (L16261) | 16261 | 4 | 1 | 0 | 3 | 3 | 3 | 1 | A |

**重要发现**：
- `machineOrderCompletedCtrl` NOT FOUND — `machineOrderCompleted.html` 存在但**没有对应 Controller 定义**
- `machineOrderListCtrl` 是 Machine 域最大 medicalProduct 消费者（26 命中）
- **Machine → Stock 字段桥 = 0**（machineOrderWaitProcessCtrl/3, machineOrderBrokenCtrl/3 但都是 controller 内部使用）

---

## §8 字段矩阵

### §8.1 Product 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `id` | A | A | A | A | - | A |
| `name` | F | F | - | - | - | F |
| `price` | F | F | - | - | - | F |
| `brand` | A (1 命中) | - | - | A | - | A |
| `category` | A (1 命中) | - | - | A | - | A |
| `brandId` | F | F | - | F | - | F |
| `categoryId` | F | F | - | F | - | F |
| `productType` | A (3 命中) | - | - | A | - | A |
| `productModel` | F | F | - | F | - | F |
| `skuList` | F | F | - | F | - | F |

### §8.2 SKU 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `stockInSku.id` | A | A | A | A | - | A |
| `stockInSkuId` | - | A | A | A | - | A |
| `skuId` | F | A | A | A | - | C |
| `skuList` (F4 Response) | A | - | - | A | - | A |
| `stockInSkuList` (UI) | - | - | - | A | - | A (UI) |
| `deliveryStockInSkuVoList` | A | - | - | A | - | A |
| `deliveryCount` | A | A | - | A | - | A |
| `productSkuId` | - | A | - | A | - | A |
| `outCount` | - | A | - | A | - | A |
| `transferCount` | - | A | - | A | - | A |

### §8.3 MedicalProduct 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `id` | A | A | A | A | - | A |
| `objectId` | - | - | - | A | A (L3854) | **A (Runtime)** |
| `medicalRecordId` | F | F | F | F | - | F (顶层) |
| `name` / `price` / `brand` / `category` | F | F | F | F | - | F |
| `productId` | F | F | F | F | - | F |
| `machineCenterId` | F (顶层) | A (F3/F6) | F | F | - | A (Request) |
| `rateFee` | A | A | - | A | - | A |
| `deliveryCount` | F (顶层) | A (F5) | F | F | - | A (Request) |
| `medicalProductStockBatctPoListJson` | - | A (F5) | - | A | - | A |

### §8.4 Stock 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `stockId` | F (顶层 0) | C (2 命中) | F | F | - | C (弱) |
| `stockCount` | F | F | F | F | - | F |
| `stockIn` | A | A | A | A | - | A (UI) |
| `stockOut` | A | A | A | A | - | A (UI) |
| `outCount` | - | A | - | A | - | A |
| `transferCount` | - | A | - | A | - | A |
| `productSkuId` | - | A | - | A | - | A |
| `stockInSkuListJson` | - | A | - | A | - | A |
| `stockBatch` | F | F | F | F | - | F |

### §8.5 Brand / Category 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `brandId` | F (顶层 0) | A | A | A | - | A |
| `brandName` | A | - | - | A | - | A |
| `categoryId` | F (顶层 0) | A | A | A | - | A |
| `categoryName` | A | - | - | A | - | A |
| `product.brand` | A | - | - | A | - | A (Object 引用) |
| `product.category` | A | - | - | A | - | A (Object 引用) |

### §8.6 MachineCenter 字段矩阵

| Field | Response | Request | State | Scope | Runtime | Grade |
|---|---|---|---|---|---|---|
| `machineCenterId` | F (顶层 0) | A (F3/F6) | A | A | - | A |
| `objectId` (源) | - | - | - | A | A (L3854) | **A (Runtime)** |
| `lockMachineCenter.id` (源) | A | - | - | A | - | A |
| `medicalProductMachineCenterPoListJson` | - | A (F3/F6) | - | A | - | A |

---

## §9 对象交叉桥

### §9.1 15 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Product | SKU | 0 命中 `product.skuList` | F | - | **F** | F |
| Product | MedicalProduct | 0 命中 | F | - | **F** | F |
| Product | Brand | `product.brand` (Object 引用) | A 字段桥 (弱) | (1 命中) | **C** | C |
| Product | Category | `product.category` (Object 引用) | A 字段桥 (弱) | (1 命中) | **C** | C |
| Product | Stock | 0 命中 | F | - | **F** | F |
| Product | Sale | myMaterialBillCtrl (A 派生, product=44) | A 派生 | L32435 | **A** | A |
| SKU | Stock | `stockInSku.id` ↔ `stockInSkuId` 共享 | A 字段桥 (id 共享) | 多处 | **A** | A |
| SKU | MedicalProduct | 0 命中 (stockInSkuVoList[].stockInSku 是 F4 Response) | A 派生 | L3989 | **A** | A |
| SKU | Sale | myMaterialBillCtrl / addSaleRecordCtrl (stockInSkuList) | A 派生 | 多处 | **A** | A |
| MedicalProduct | Stock | F5 `saveMedicalProductStockBatch` | A Request Bridge | L4007 | **A** | A |
| MedicalProduct | Delivery | F3/F4/F5/F6 Request 完整链 | A Request Bridge | L3836/L3885/L4007/L3966 | **A** | A |
| MedicalProduct | MachineCenter | F3/F6 `machineCenterId=objectId` (Runtime) | A Request Bridge (Runtime) | L3824 | **A** | A |
| MedicalProduct | Cashflow | `getMedicalRecordCashflowVo` 派生 | A 派生 (S1-148) | L7070 | **A** | A |
| MedicalProduct | Sale | `medicalProductVoList` myMaterialBillCtrl (S1-148) | A 派生 | L32435 | **A** | A |
| Brand | Category | 0 命中 | F | - | **F** | F |
| Brand | Product | `product.brand` Object 引用 | C | (1 命中) | **C** | C |
| Category | Product | `product.category` Object 引用 | C | (1 命中) | **C** | C |
| MachineCenter | MedicalProduct | `medicalProduct.objectId=lockMachineCenter.id` (Runtime) | A Runtime 字段桥 | L3854 | **A** | A |
| Stock | Delivery | F5 `saveMedicalProductStockBatch` | A Request Bridge | L4007 | **A** | A |

### §9.2 关系等级汇总

| 等级 | 数量 | 关系 |
|---|---:|---|
| A | 11 | SKU→Stock / SKU→MedicalProduct / SKU→Sale / MedicalProduct→Stock / MedicalProduct→Delivery / MedicalProduct→MachineCenter / MedicalProduct→Cashflow / MedicalProduct→Sale / Stock→Delivery / MachineCenter→MedicalProduct / Product→Sale |
| C | 3 | Product→Brand / Product→Category / Brand→Product / Category→Product |
| F | 5 | Product→SKU / Product→MedicalProduct / Product→Stock / Brand→Category / MedicalProduct 顶层 name/price/brand/category 字段 |

---

## §10 Product/SKU ↔ Sale

### §10.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Sale | Product | myMaterialBillCtrl / addSaleRecordCtrl / adminSalesRecordCtrl 消费 product=62 | A 派生 | L32435/L31008 | **A** | A |
| Sale | SKU | myMaterialBillCtrl / addSaleRecordCtrl 消费 skuList=1 | A 派生 | L32435 | **A** | A |
| Sale | MedicalProduct | myMaterialBillCtrl 消费 medicalProductVoList | A 派生 (S1-148) | L32435 | **A** | A |
| Product | Sale | 0 命中 `product.sale` 字段 | F | - | **F** | F |
| SKU | Sale | 0 命中 `sku.sale` 字段 | F | - | **F** | F |

### §10.2 关键判断

- **Sale → Product/SKU/MedicalProduct**: A 派生（3 个 Sale Controller 都消费 product/medicalProduct）
- **Product/SKU → Sale**: F（无直接字段桥）
- **保持 S1-143 修正**：saleId=0 / saleVo=0

---

## §11 Product/SKU/MedicalProduct ↔ Cashflow

### §11.1 Cashflow → MedicalProduct 桥

- `getMedicalRecordCashflowVo` (L7070) Response:
  - `object.cashflow`
  - `object.medicalExamineVoList[].medicalExamine.id`
  - `object.registrationFeeVoList[].medicalExamine.id`
  - **`object.medicalProductVoList[].medicalProduct.id`** → `$scope.medicalProductIdList`
  - **`object.medicalProductVoListOfModel[].medicalProduct.id`** → `$scope.medicalProductModelIdList`
- **Cashflow → MedicalProduct = A 派生**（保持 S1-148 修正）

### §11.2 Cashflow → Product / SKU 桥

- `cashflow.product` 字段 = 0 命中（F）
- `cashflow.sku` 字段 = 0 命中（F）
- **Product/SKU 不直接进入 Cashflow**（F）

### §11.3 Product/SKU/MedicalProduct → Cashflow 桥

- `medicalProduct.cashflow` 字段 = 0 命中（F）
- **MedicalProduct 不含 cashflow 字段**（F，保持 S1-148 修正）

---

## §12 MedicalProduct ↔ Delivery

### §12.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| MedicalProduct | Delivery | F3/F4/F5/F6 Request 完整链 | A Request Bridge | L3836/L3885/L4007/L3966 | **A** | A |
| MedicalProduct | Delivery | `medicalProduct.delivery` 字段 | 0 命中 | - | **F** | F |
| Delivery | MedicalProduct | `waitingDeliveryList[].medicalProduct` 嵌套 | A 字段桥 | L3817-L3856 | **A** | A |
| Delivery | MedicalProduct | `delivery.medicalProduct` 字段 | 0 命中 (顶层) | - | **F** | F |

### §12.2 关键判断

- **MedicalProduct → Delivery**: A Request Bridge（F3-F6 完整链）
- **Delivery → MedicalProduct**: A 字段桥（`waitingDeliveryList[].medicalProduct` 嵌套）
- **保持 S1-142 修正**：MedicalProduct 不含 delivery 字段（F），Delivery 不含 medicalProduct 字段（F），桥全部经 list item 嵌套

---

## §13 MedicalProduct ↔ MachineCenter / Machine

### §13.1 双向关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| MedicalProduct | MachineCenter | F3/F6 `machineCenterId=objectId` | A Request Bridge (Runtime) | L3824 | **A** | A |
| MedicalProduct | MachineCenter | `medicalProduct.machineCenterId` 字段 | 0 命中 (顶层) | - | **F** | F |
| MachineCenter | MedicalProduct | `medicalProduct.objectId=lockMachineCenter.id` | A Runtime Mutation | L3854 | **A** | A |
| MedicalProduct | Machine | machineOrderListCtrl (medicalProduct=26) | A 派生 | L4264 | **A** | A |
| MedicalProduct | Machine | `machineOrder.medicalProduct` 字段 | 0 命中 | - | **F** | F |

### §13.2 关键判断

- **MedicalProduct → MachineCenter**: A Request Bridge (Runtime)
- **MachineCenter → MedicalProduct**: A Runtime Mutation
- **保持 S1-129 / S1-142 修正**：
  - 前端目前能证明 MedicalProduct → MachineCenter = Request Bridge
  - 不能证明 MedicalProduct 表 → MachineCenter 表 FK（L3 F）

---

## §14 Write 生命周期

### §14.1 F3-F6 4 个 Write/Read API 链

```
F3 (Read): medicalProductMachineCenterPoListJson
    ↓
F6 (Write): sendMedicalProductToMachineCenter (machineCenterId 工厂下单)
    
F4 (Read): medicalProductIdArray → deliveryStockInSkuVoList[]
    ↓
F5 (Write): saveMedicalProductStockBatch (Stock 扣减)
```

### §14.2 Stock Write API 全量

| API | 用途 | 行号 | 等级 |
|---|---|---|---|
| `saveMedicalProductStockBatch.json` | F5: Stock 批量入库 | L4007 | A |
| `sendMedicalProductToMachineCenter.json` | F6: 工厂下单 | L3966 | A |
| `createMedicalStockLossOfSmallVersion.json` | ReportLoss 报损 | L35342 | A |
| `createStock*.json` (19 命中) | 通用 stock 创建 | 多处 | A |
| `updateStock*.json` (15 命中) | 通用 stock 更新 | 多处 | A |
| `deleteStock*.json` (7 命中) | 通用 stock 删除 | 多处 | A |
| `saveStock*.json` (2 命中) | stock 保存 | 多处 | A |

### §14.3 Product/MedicalProduct Write API

| API | 用途 | 行号 | 等级 |
|---|---|---|---|
| `saveMedicalProduct*.json` (6 命中) | MedicalProduct 保存 | 多处 | A |
| `createProduct*.json` (5 命中) | Product 创建 | 多处 | A |
| `updateProduct*.json` (3 命中) | Product 更新 | 多处 | A |
| `deleteProduct*.json` (2 命中) | Product 删除 | 多处 | A |
| `saveProduct*.json` (1 命中) | Product 保存 | 多处 | A |

### §14.4 重要发现

- **0 命中 `createBrand*.json` / `createCategory*.json`** — Brand/Category 没有独立 Create
- **0 命中 `createSKU*.json` / `createStockInSku*.json`** — SKU 没有独立 Create
- **0 命中 `createMachineCenter*.json`** — MachineCenter 没有独立 Create

---

## §15 Source Trace

### §15.1 关键字段溯源

#### productId
- **Source A**: `arr[i].medicalProduct.id` (L3822 F3)
- **Source B**: `medicalProductIdArray.push(arr[i].medicalProduct.id)` (L3873 F4)
- **Source C**: `getMedicalProductVoList Response`
- **等级**: A

#### skuId
- **Source A**: `productArr[i].deliveryStockInSkuVoList[j].stockInSku.id` (L16191)
- **Source B**: `$scope.stockInSkuList[].productSkuId` (L22406)
- **Target**: `stockInSkuId` (F5 Request)
- **等级**: A

#### stockInSkuId
- **Source**: F4 Response `deliveryStockInSkuVoList[].stockInSku.id` (L3989/L16191)
- **Transform**: `stockInSku.id` → `stockInSkuId` (F5 Request payload)
- **Target**: F5 `saveMedicalProductStockBatch`
- **等级**: A

#### medicalProductId
- **Source A**: `arr[i].medicalProduct.id` (L3822/L3873)
- **Source B**: `medicalProductId` (F3 Request)
- **Source C**: `getMedicalProductVoList` Response
- **等级**: A

#### medicalProductStockId
- **Source**: 0 命中 (medicalProductStock 0 命中)
- **Target**: F4/F5 Request 字段 (medicalProductStockBatctPoListJson)
- **等级**: A (Request) / F (Object)

#### stockId
- **Source**: 2 命中（独立 ID 证据弱）
- **等级**: C (弱)

#### brandId / categoryId
- **Source**: Request 字段（多命中）
- **Target**: getBrand / getCategory Request
- **等级**: A (Request 字段, 但不是 Object 主键)

#### machineCenterId
- **Source A**: F3/F6 Request `machineCenterId: arr[i].medicalProduct.objectId` (L3824)
- **Source B**: lockMachineCenter 派生
- **等级**: A

#### objectId (Runtime Mutation)
- **Source A**: `lockMachineCenter.id` (L3854, runtime mutation)
- **Source B**: null (L3856, else branch)
- **Transform**: runtime mutation 写入 `medicalProduct.objectId`
- **Target**: F3/F6 Request `machineCenterId=objectId`
- **等级**: **A (Runtime)**

#### deliveryCount
- **Source A**: F4 Response `deliveryStockInSkuVoList[].deliveryCount` (L3989/L16192)
- **Source B**: UI 临时 `$scope.deliveryCount`
- **Target**: F5 Request
- **等级**: A

---

## §16 Object Type 分类

### §16.1 9 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Product** | ✓ (productId) | ✗ (无 productVo) | ✓ (saveProduct* / updateProduct* / createProduct* / deleteProduct*) | - | A (弱) |
| **SKU** | ✓ (stockInSkuId) | ✓ (stockInSkuVoList / deliveryStockInSkuVoList) | ✓ (F4/F5) | ✓ ($scope.stockInSkuList) | A |
| **MedicalProduct** | ✓ (medicalProductId) | ✗ (无 medicalProductVo) | ✓ (F3-F6, 28 medicalProductStockBatctPoListJson) | - | A |
| **Stock** | ✗ (stockId 仅 2 命中) | ✗ | ✓ (60 getStock / 19 createStock / 15 updateStock) | ✓ ($scope.stockInSkuList) | A (Request 为主) |
| **MedicalProductStock** | ✗ (medicalProductStock 0 命中) | ✗ | ✓ (F4/F5, medicalProductStockBatctPoListJson) | - | C (Request Payload) |
| **StockInSku** | ✓ (stockInSkuId) | ✓ (stockInSkuVoList) | ✓ (F4/F5) | ✓ ($scope.stockInSkuList) | A |
| **Brand** | ✓ (brandId) | ✗ (无 brandVo) | ✗ (0 命中 saveBrand) | - | A (ID + 列表) |
| **Category** | ✓ (categoryId) | ✗ (无 categoryVo) | ✗ (0 命中 saveCategory) | - | A (ID + 列表) |
| **MachineCenter** | ✓ (machineCenterId) | ✗ (无 machineCenterVo) | ✓ (F3/F6 Request) | - | A (Request + ID) |

### §16.2 关键结论

- **9 个对象中 6 个是独立 ID 实体** (Product / SKU / MedicalProduct / StockInSku / Brand / Category)
- **3 个 Request/State 主导** (Stock / MedicalProductStock / MachineCenter)
- **`productVo` / `medicalProductVo` / `brandVo` / `categoryVo` / `stockBatch` 全部 0 命中**（同 customerVo/patientVo 模式）
- **`stockBatch` / `stockBatchId` 0 命中**（StockBatch 概念不存在）
- **`medicalProductStock` 0 命中**（实际是 Request Payload）

---

## §17 生命周期 DAG

### §17.1 物资域完整 DAG

```
[Brand/Category] (列表/筛选)
    ↓ Object 引用 (C)
[Product] (普通商品)
    ↓ ???
[SKU/StockInSku] (库存单元)
    ↓ ???
[MedicalProduct] (医疗商品, medicalRecordType 路由)
    ↓
    ├── F3/F6: machineCenterId=objectId (Runtime) → MachineCenter → Machine
    ├── F4: medicalProductIdArray → deliveryStockInSkuVoList[] → F5
    ├── F5: saveMedicalProductStockBatch → Stock 扣减
    └── getMedicalRecordCashflowVo → medicalProductVoList[] → Cashflow
```

### §17.2 边汇总（仅 A/B/C）

| Source | Target | 等级 | 边 | 行号 |
|---|---|---|---|---|
| MedicalProduct | MachineCenter | A | F3/F6 `machineCenterId=objectId` (Runtime) | L3824 |
| MedicalProduct | Stock | A | F5 `saveMedicalProductStockBatch` | L4007 |
| MedicalProduct | Delivery | A | F3/F4/F5/F6 Request 完整链 | L3836/L3885/L4007/L3966 |
| MedicalProduct | Cashflow | A | getMedicalRecordCashflowVo 派生 | L7070 |
| MedicalProduct | Sale | A | myMaterialBillCtrl 派生 | L32435 |
| MachineCenter | MedicalProduct | A | `medicalProduct.objectId=lockMachineCenter.id` (Runtime) | L3854 |
| Stock | Delivery | A | F5 `saveMedicalProductStockBatch` | L4007 |
| StockInSku | MedicalProduct | A | F4 `deliveryStockInSkuVoList[].stockInSku.id` | L3989 |
| Product | Brand | C | `product.brand` Object 引用 | (1 命中) |
| Product | Category | C | `product.category` Object 引用 | (1 命中) |

### §17.3 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Product → SKU 直接 | F (无 product.skuList) |
| Product → MedicalProduct 直接 | F |
| Product → Stock 直接 | F |
| MedicalProduct → Brand/Category 字段 | F |
| Product → Sale 字段 | F |
| MedicalProduct → Cashflow 字段 | F |
| cashflow.medicalProductVoList = cashflow.product FK | F (VO ≠ FK) |
| medicalProductStockBatctPoListJson = medicalProductStock.medicalProductId FK | F (Request Bridge) |

---

## §18 Controller 消费矩阵

### §18.1 22 个 Controller 物资域消费矩阵

| Controller | product | medicalProduct | sku | stock | brand | category | mc | 等级 |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| **myMaterialBillCtrl** (L32435) | 44 | 40 | 1 | 49 | 8 | 4 | 0 | A |
| **addSaleRecordCtrl** (L31008) | **62** | **54** | 1 | **88** | 10 | 7 | 0 | A |
| **adminSalesRecordCtrl** (L31285) | 62 | 54 | 1 | 88 | 10 | 7 | 0 | A |
| **deliveryInputCtrl** (L3812) | 5 | **38** | 1 | 0 | 0 | 0 | **8** | A |
| deliveryInputRecordCtrl (L4024) | 5 | 27 | 0 | 0 | 0 | 0 | 0 | A |
| deliveryProcessingCtrl (L4236) | 5 | 26 | 0 | 0 | 0 | 0 | 0 | A |
| optometryCtrl (L34776) | 15 | 16 | 1 | **38** | 5 | 2 | 0 | A |
| **machineOrderCtrl** (L16094) | 0 | 2 | 1 | 0 | 2 | 2 | 1 | A |
| **machineOrderListCtrl** (L4264) | 5 | **26** | 0 | 0 | 0 | 0 | 0 | A |
| ~~machineOrderCompletedCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| machineOrderWaitProcessCtrl (L16357) | 8 | 0 | 5 | 6 | 3 | 3 | 1 | A |
| machineOrderBrokenCtrl (L16261) | 4 | 1 | 0 | 3 | 3 | 3 | 1 | A |
| **brandListCtrl** (L2426) | 5 | 38 | 1 | 0 | **8** | 0 | 8 | A |
| ~~productListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~productDetailCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~productUpdateCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~stockInListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~stockOutListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~stockManageCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~skuListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~categoryListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |
| ~~machineCenterListCtrl~~ | **NOT FOUND** | - | - | - | - | - | - | F |

### §18.2 核心观察

1. **addSaleRecordCtrl 是最大 Stock 消费者** (stock=88) — 销售环节使用 Stock
2. **deliveryInputCtrl 是最大 MachineCenter 消费者** (mc=8) — 配送环节使用 MachineCenter
3. **addSaleRecordCtrl / adminSalesRecordCtrl 是最大 Product/MedicalProduct 消费者** (62/54)
4. **myMaterialBillCtrl 是大综合消费** (product=44 / medicalProduct=40 / stock=49)
5. **brandListCtrl 是大综合消费** (product=5 / medicalProduct=38 / brand=8 / mc=8) — 命名误导实际是混用
6. **9+ NOT FOUND Controller** — 实际命名误导：
   - productListCtrl / productDetailCtrl / productUpdateCtrl
   - stockInListCtrl / stockOutListCtrl / stockManageCtrl
   - skuListCtrl / categoryListCtrl / machineCenterListCtrl
   - machineOrderCompletedCtrl（machineOrderCompleted.html 存在但无 Controller）

---

## §19 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 22 Controllers 范围 | A | - | 全部 | A |
| 2 | Controller | 13 Controllers + 9 NOT FOUND | A | - | 全部 | A |
| 3 | State | cashflowId / medicalRecordId / productId | A | - | 多处 | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | productId / medicalProductId / stockInSkuId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | brandId / categoryId | A | - | 多处 | A |
| 10 | Status | (Stock 状态字段 0 命中) | F | - | - | F |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=12/20/30 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | medicalProductId (F3/F4) | A | - | L3822 | A |
| 15 | Default | medicalRecordType=1/5 | A | - | L10605 | A |
| 16 | Data Source | F3-F6 4 API + 30+ Stock/Product API | A | - | 全部 | A |
| 17 | Object | product.id / medicalProduct.id / stockInSku.id | A | - | 全部 | A |
| 18 | Request | { medicalProductId } / { stockInSkuId } / { machineCenterId } | A | - | L3822/L3989 | A |
| 19 | Response | res.object.medicalProduct.id / .stockInSku.id | A | - | L3822/L3989 | A |
| 20 | Function | getDeliveryListFactory / getCenterListFactory | A | - | 多处 | A |
| 21 | State Bridge | medicalProductId (F3/F4) | A | - | 全部 | A |
| 22 | Object Bridge | medicalProduct.objectId = lockMachineCenter.id (Runtime) | A | - | L3854 | A (Runtime) |
| 23 | API Bridge | F3-F6 4 API 完整链 | A | - | L3836/L3885/L4007/L3966 | A |
| 24 | Business Interpretation | MedicalProduct 是物资域核心对象 | A | - | - | A (派生) |
| 25 | Evidence Grade | 20 A / 3 C / 0 D / 0 E / 6 F | - | - | - | - |
| 26 | V4.4 Decision | MedicalProduct/SKU/Brand/Category 必保留, StockInSku Runtime Mutation 必保留 | A | - | - | A |

---

## §20 历史差异

### §20.1 S1-129/142/143/145/146/148 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-129: Machine/Delivery 无直接桥 | 实际 machineOrderListCtrl (L4264) 消费 medicalProduct=26 | 部分保持 | **保持 (Machine → MedicalProduct 派生 A)** |
| S1-142: medicalProduct.objectId 是 Runtime | 7 命中, L3854 `lockMachineCenter.id` 写入 | 保持 | **保持 S1-142 修正** |
| S1-142: Stock → Delivery F | F5 `saveMedicalProductStockBatch` 实际是 A Request Bridge | 保持 | **保持 S1-142 修正** |
| S1-143: Sale 独立 saleVo | 0 命中 saleVo/saleId | 保持 | **保持 S1-143 修正** |
| S1-145: MedicalProduct 独立 ID | medicalProduct.id=27 / medicalProductId=24 | 保持 | **保持 S1-145 修正** |
| S1-145: medicalProductName | 0 命中 | 保持 | **保持 S1-145 修正** |
| S1-146: MedicalRecord 不含 medicalProductVoList 嵌套 | 0 命中 | 保持 | **保持 S1-146 修正** |
| S1-148: cashflow.medicalProductVoList 是 VO | L7070 派生 ID 数组, 不是 cashflow 字段 | 保持 | **保持 S1-148 修正** |

### §20.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~StockBatch 概念存在~~ | stockBatch=0 / stockBatchId=0 | 应改 | **F (StockBatch 概念不存在)** |
| ~~MedicalProductStock 是独立 ID 实体~~ | medicalProductStock=0 / medicalProductStockId=4 (Request) | 应改 | **F (Request Payload)** |
| ~~productListCtrl / productDetailCtrl / stockInListCtrl / categoryListCtrl 存在~~ | 0 命中 Controller 定义 | 应改 | **F NOT FOUND (9 个命名误导)** |
| ~~lockMachineCenter 是独立 Object 容器~~ | 1 命中, 仅 `arr[i].lockMachineCenter.id` 字段访问 | 应改 | **F (不是 Object, 是临时变量)** |
| ~~product.brandId / product.categoryId 是字段~~ | 0 命中, 实际是 product.brand / product.category Object 引用 | 应改 | **F (字段不存在, Object 引用 C)** |
| ~~Brand/Category 独立 Create 入口~~ | 0 命中 createBrand / createCategory | 应改 | **F (只有 Read API)** |
| ~~medicalProductVo / productVo / brandVo / categoryVo 独立 VO 容器~~ | 字符级 0 命中 | 应改 | **F (用 res.product / item.product 等)** |
| ~~productUnit / productModel 字段~~ | 0 命中 | 应改 | **F** |
| ~~stockCount 字段~~ | 0 命中 | 应改 | **F** |

### §20.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 211_S1-148 全部保持原样
- 本文档 212_*.md 单独记录物资域完整闭环

---

## §21 V4.4 物资域规格

### §21.1 必实现 (A 级)

| 项 | 行号 | 必实现 |
|---|---|---|
| productId 独立 ID | 58 命中 | ✓ |
| medicalProductId 独立 ID | 24 命中 | ✓ |
| stockInSkuId 独立 ID | 76 命中 | ✓ |
| brandId / brandName | 57/66 命中 | ✓ |
| categoryId / categoryName | 94/77 命中 | ✓ |
| machineCenterId | 26 命中 | ✓ |
| medicalProduct.id / .objectId / .rateFee | 27/7/2 命中 | ✓ |
| medicalProductVoList / medicalProductVoListOfModel | 21/17 命中 | ✓ |
| stockInSkuList (Scope UI) | 216 命中 | ✓ |
| F3 `getMedicalProductMachineCenterVoList.json` | L3836 | ✓ |
| F4 `getCanBeDeliverySkuInListOfProduct.json` | L3885/L35054 | ✓ |
| F5 `saveMedicalProductStockBatch.json` | L4007 | ✓ |
| F6 `sendMedicalProductToMachineCenter.json` | L3966 | ✓ |
| `medicalProduct.objectId` Runtime Mutation | L3854 | ✓ (关键) |
| 13 个有效 Controller 消费 | 全部 | ✓ |
| `lockMachineCenter.id → objectId` 链 | L3854 | ✓ |
| `deliveryStockInSkuVoList[].stockInSku.id + deliveryCount` | L3989 | ✓ |
| `medicalProductMachineCenterPoListJson` Request payload | L3817-L3828 | ✓ |
| `medicalProductStockBatctPoListJson` Request payload | 28 命中 | ✓ |

### §21.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `productVo` / `medicalProductVo` / `brandVo` / `categoryVo` 独立 VO 命名 | ✗ (0 命中) |
| `stockBatch` / `stockBatchId` | ✗ (0 命中) |
| `medicalProductStock` 独立 Object | ✗ (0 命中) |
| `product.brandId` / `product.categoryId` 顶层字段 | ✗ (0 命中) |
| `product.skuList` / `product.name` / `product.price` / `product.productModel` 字段 | ✗ (0 命中) |
| `medicalProduct.name` / `.price` / `.brand` / `.category` / `.productId` / `.machineCenterId` / `.medicalRecordId` 顶层 | ✗ (0 命中) |
| `stockId` 独立 ID | ✗ (仅 2 命中, 弱) |
| `productListCtrl` / `productDetailCtrl` / `productUpdateCtrl` | ✗ (NOT FOUND) |
| `stockInListCtrl` / `stockOutListCtrl` / `stockManageCtrl` | ✗ (NOT FOUND) |
| `skuListCtrl` / `categoryListCtrl` / `machineCenterListCtrl` | ✗ (NOT FOUND) |
| `machineOrderCompletedCtrl` | ✗ (NOT FOUND) |
| `lockMachineCenter` 独立 Object 容器 | ✗ (1 命中, 临时变量) |
| `cashflow.medicalProductVoList` = cashflow.product FK | ✗ (VO ≠ FK) |
| 13 类/50+ 品牌作为 V4.4 数量 | ✗ (历史运行时, 需 L3) |

### §21.3 9 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Product** | A+C (独立 ID + 列表 + 多 Write) | 独立 VO 容器 (F) |
| **SKU** | A+B+C+D (独立 ID + Response VO + Request + UI) | 独立 Object (同 Product 衍生) |
| **MedicalProduct** | A+C (独立 ID + Request) | 独立 VO 容器 (F) |
| **Stock** | A+C (Request 为主) | 独立 ID 实体 (弱) |
| **MedicalProductStock** | C (Request Payload) | 独立 ID 实体 (F) |
| **StockInSku** | A+B+C+D | - |
| **Brand** | A+D (独立 ID + 列表/筛选) | 独立 Create 入口 (F) |
| **Category** | A+D (独立 ID + 列表/筛选) | 独立 Create 入口 (F) |
| **MachineCenter** | A+C (独立 ID + Request) | 独立 Object 容器 (F) |

### §21.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `medicalProduct.objectId = lockMachineCenter.id` (Runtime) | **A** | L3854 |
| F3 `medicalProductMachineCenterPoListJson` (medicalProductId + machineCenterId) | A | L3822 |
| F4 `deliveryStockInSkuVoList[].stockInSku.id + deliveryCount` | A | L3989 |
| F5 `medicalProductStockBatctPoListJson` (stockInSkuId + deliveryCount) | A | L3991 |
| Cashflow `medicalProductVoList[]` (S1-148 派生) | A | L7070 |
| Sale `myMaterialBillCtrl` 派生 (A) | A | L32435 |
| `getMedicalProductVoList` Response (productVoList 容器) | A | 4 调用 |

### §21.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Product → SKU 字段桥 (无 product.skuList) | F |
| Product → MedicalProduct 字段桥 | F |
| Product → Stock 字段桥 | F |
| MedicalProduct 顶层 brand/category 字段 | F |
| MedicalProduct → Sale 字段桥 (saleVo 0 命中) | F |
| medicalProductStock.medicalProductId DB FK (L3) | F |
| cashflow.medicalProductVoList = medicalProduct FK (L3) | F |
| stockBatch 概念 | F |

### §21.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `lockMachineCenter` | 不是 Object, 仅 `arr[i].lockMachineCenter.id` 字段访问 | **命名误导** |
| `medicalProductStockBatctPoListJson` | 实际是 F4/F5 Request 字段, 不是 medicalProductStock Object | 命名误导 |
| `medicalProduct.objectId` | Runtime Mutation from lockMachineCenter.id, 不是原始 Response 字段 | **命名误导 (S1-142)** |
| `productListCtrl` / `productDetailCtrl` | **NOT FOUND** | 命名误导 |
| `stockInListCtrl` / `stockOutListCtrl` / `stockManageCtrl` | **NOT FOUND** | 命名误导 |
| `skuListCtrl` / `categoryListCtrl` / `machineCenterListCtrl` | **NOT FOUND** | 命名误导 |
| `machineOrderCompletedCtrl` | NOT FOUND (html 存在) | 命名误导 |
| `productVo` / `medicalProductVo` / `brandVo` / `categoryVo` | 字符级 0 命中 | 命名误导 (同 customerVo/patientVo 模式) |
| `brandListCtrl` (L2426) | 实际是 mix Controller, 消费 product/medicalProduct/mc | 命名误导 |
| `getMedicalProductMachineCenterVoList.json` | 实际不返回 machineCenterVo, 是 medicalProductMachineCenterVoListJson | 命名误导 |
| `saveMedicalProductStockBatch.json` | 实际保存 Stock 扣减, 不是 medicalProductStock Object | 命名误导 |
| `sendMedicalProductToMachineCenter.json` | Request 字段是 `medicalProductMachineCenterPoListJson` 不是 machineCenterId | 命名误导 |
| `product.brandId` / `product.categoryId` | 0 命中, 实际是 product.brand / product.category Object 引用 | 命名误导 |
| `stockBatch` / `stockBatchId` | 0 命中, StockBatch 概念不存在 | 命名误导 |
| `stockInSkuList` | 实际是 Scope UI 临时数组, 不是独立 Object | 命名误导 |
| `medicalProductStockId` | 4 命中, 实际是 Request 字段不是 Object 主键 | 命名误导 |

---

## §22 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Product 数据库表结构 | F | 需后端源码 |
| 2 | SKU 数据库表结构 | F | 需后端 |
| 3 | MedicalProduct 数据库表结构 | F | 需后端 |
| 4 | Stock 数据库表结构 | F | 需后端 |
| 5 | Brand 数据库表结构 | F | 需后端 |
| 6 | Category 数据库表结构 | F | 需后端 |
| 7 | MachineCenter 数据库表结构 | F | 需后端 |
| 8 | StockInSku 数据库表结构 | F | 需后端 |
| 9 | MedicalProductStock 数据库表结构 | F | 需后端 |
| 10 | 13 类/50+ 品牌实际数量 | F (历史运行时) | 需后端 + 当前查询 |
| 11 | `productVo` / `medicalProductVo` 命名历史 | F | 需 git log |
| 12 | 9+ NOT FOUND Controller 命名历史 | F | 需 git log |
| 13 | `lockMachineCenter` Object 容器历史 | F | 需 git log |
| 14 | `medicalProduct.objectId` 原始 Response 字段历史 | F (S1-142 已是 Runtime) | 需 git log |
| 15 | F3-F6 API 完整 Response schema | F | 需后端 |
| 16 | medicalProductMachineCenterVoListJson 完整 schema | F | 需后端 |
| 17 | deliveryStockInSkuVoList 完整 schema | F | 需后端 |
| 18 | medicalProductStockBatctPoListJson 完整 schema | F | 需后端 |
| 19 | `medicalProductStockId` 与 `medicalProductStock` 关系 | F (medicalProductStock 0 命中) | 需后端 |
| 20 | `product.brand` / `product.category` 是否 productVoList 容器 | F (1 命中, 弱) | 需后端 |

---

## §23 Git / 完整性

### §23.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-211 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 212_*.md | ✓ |

### §23.2 Git 操作

```
git add -- 212_S1-149_Product_SKU_MedicalProduct_Stock_Brand_Category物资域总审计.md
git diff --cached --name-only
git commit -m "docs(212): S1-149 Product/SKU/MedicalProduct/Stock/Brand/Category 物资域总审计"
git push origin master
```

### §23.3 预期

- tracked = 219 → **220**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `6fc158a4d6579dc68ee4d4e52a3be3e73c79bb8e` (S1-148 commit)

---

## 文档元信息

- **审计范围**：S1-149 (Product / SKU / MedicalProduct / Stock / Brand / Category / MachineCenter 物资域)
- **本轮新增文件**：`212_S1-149_Product_SKU_MedicalProduct_Stock_Brand_Category物资域总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-150** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
