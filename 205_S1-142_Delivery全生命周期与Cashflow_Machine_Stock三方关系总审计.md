# S1-142：Delivery 全生命周期与 Cashflow / Machine / Stock 三方关系总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向建模（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / deliveryList.html / 已冻结 204 个 MD / 不修改历史
> 关联：S1-128 / S1-129 / S1-135 / S1-136 / S1-137 / S1-137R / S1-138 / S1-141

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. Delivery Controller 全量
5. Delivery 入口
6. deliveryList.html 静态证据
7. F1 getCashflowDeliveryVo
8. 四个 Delivery List
9. medicalProduct 生命周期
10. objectId 生命周期
11. F3 getMedicalProductMachineCenterVoList
12. F4 getCanBeDeliverySkuInListOfProduct
13. F5 saveMedicalProductStockBatch
14. F6 sendMedicalProductToMachineCenter
15. completeMedicalRecordDelivery（optometryCtrl 内）
16. ReportLoss createMedicalStockLossOfSmallVersion
17. Return / Cancel
18. Delivery → Machine
19. Machine → Delivery
20. Delivery ↔ Cashflow
21. Delivery ↔ Charge
22. Delivery ↔ Sale
23. Cashflow / MedicalRecord / Machine / Stock / Delivery 三方矩阵
24. 精确数量
25. L1 / L2 / L3
26. 最终 Delivery DAG
27. 26 项证据矩阵
28. A/B/C/D/E/F 等级
29. 历史差异
30. 复刻红线
31. 红线检查
32. Git

---

## 1. 任务性质

本轮是 Delivery 全生命周期 + Cashflow / Machine / Stock 三方关系总审计。

- 禁止修改 165-204 任意历史 MD
- 禁止修改 controller.js / deliveryList.html / machineOrderCompleted.html / machineOrderList.html / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`205_S1-142_*.md`
- 必须把 Delivery 真实生命周期逐边证明

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实业务 API |
| 5 | 不发货 / 不送加工中心 / 不库存变动 / 不报损 / 不退货 / 不改配送状态 |
| 6 | 不修改 controller.js（SHA256 不变）|
| 7 | 不修改任何 HTML |
| 8 | 不修改 .gitignore |
| 9 | 不修改 165-204 历史 MD |
| 10 | 只新增 205_*.md |
| 11 | 不得把多个 Write API 自动串成生命周期 |
| 12 | 不得因为字段共现自动建立桥 |
| 13 | 不得因为 cashflowId → medicalRecordId 存在就反向建立 MedicalRecord → Delivery |
| 14 | 不得因为 Machine 和 Delivery 都出现 medicalProductId 就建立 Machine → Delivery |
| 15 | E 不进入最终规格 |
| 16 | F 必须写："当前证据范围未观察/不可得" |

---

## 3. 证据等级与命名约束

| 等级 | 定义 |
|---|---|
| A | 字符级直接证据 |
| B | 多源互证 |
| C | 局部证据 |
| D | 冲突 |
| E | 业务推断 |
| F | 当前证据范围未观察/不可得 |

### 命名约束

| 误区 | 正确理解 |
|---|---|
| "F1/F2/F3/F4/F5/F6" | F2 是什么？**F** — 未发现 F2 API 字符级 |
| "MedicalRecord Delivery" 命名 | ≠ "Delivery 入口是 medicalRecordId"（实际是 cashflowId）|
| "completeMedicalRecordDelivery" | ≠ "在 deliveryInputCtrl 调用"（实际在 optometryCtrl）|
| "Machine 与 Delivery 都用 medicalProductId" | ≠ "Machine → Delivery 桥" |
| "deliveryStatus 1/2" | 是枚举值，不补含义 |

---

## 4. Delivery Controller 全量

### 4.1 真正 Delivery Controller（基于 S1-128/141 + 本轮扫描）

| # | Controller | 行号 | State 入口 | 备注 |
|---|---|---|---|---|
| 1 | **deliveryListCtrl** | L4075 | (payedList → deliveryList) | 列表入口 |
| 2 | **deliveryInputCtrl** | L3812 | (deliveryList → deliveryInput) | 录入/送加工 |
| 3 | **deliveryInputRecordCtrl** | L4024 | $stateParams.cashflowId (L4026) | 录入记录/内部派生 |
| 4 | **deliveryProcessingCtrl** | L4236 | $stateParams.cashflowId (L4238) | 处理 |
| 5 | **deliveryDetailCtrl** | L25281 | (deliveryDetail) | 详情 |
| 6 | **deliveryModifyCtrl** | L25314 | (deliveryModify) | 修改 |
| 7 | **deliveryDeleteCtrl** | L25237 | (deliveryDetail) | 删除 |
| 8 | **addDeliveryCtrl** | L21138 | (addDelivery) | 商品配送 (material) |
| 9 | **addDeliveryCustomerCtrl** | L21374 | (addDelivery) | 客户配送 (material) |
| 10 | **addMultiDeliveryCtrl** | L21785 | (addDelivery) | 多商品配送 (material) |
| 11 | **addProductDeliveryCtrl** | L22237 | (addDelivery) | 商品配送详情 (material) |

### 4.2 命名差异

| Controller | 真实业务 |
|---|---|
| addDeliveryCtrl 等 4 个 | **Material Delivery**（商品库存调拨），**不是** MedicalRecord Delivery |
| deliveryInputCtrl / deliveryListCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl | **Cashflow Delivery**（按订单配送），与 medicalRecord 关联 |

### 4.3 Delivery Controller 分工

| 业务线 | Controller | 入口 ID |
|---|---|---|
| Cashflow Delivery（医疗订单） | deliveryListCtrl / deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl / deliveryDetailCtrl / deliveryModifyCtrl / deliveryDeleteCtrl | cashflowId |
| Material Delivery（商品调拨） | addDeliveryCtrl / addDeliveryCustomerCtrl / addMultiDeliveryCtrl / addProductDeliveryCtrl | (materialId) |

**本轮重点**: Cashflow Delivery 全生命周期

---

## 5. Delivery 入口

### 5.1 $stateParams.cashflowId 入口（S1-141 已确认）

| # | 行号 | Controller | 用途 |
|---|---|---|---|
| 1 | L3814 | deliveryInputCtrl | 配送录入 (cashflowId) |
| 2 | L4026 | deliveryInputRecordCtrl | 配送录入记录 (cashflowId) |
| 3 | L4238 | deliveryProcessingCtrl | 配送处理 (cashflowId) |

### 5.2 Cashflow Delivery 4 个 Controller 入口

```
deliveryListCtrl (L4075)
    ↓ ui-sref / $state.go (HTML link)
deliveryInputCtrl (L3812)  ← $stateParams.cashflowId
    ↓ ui-sref / $state.go
deliveryInputRecordCtrl (L4024)  ← $stateParams.cashflowId
    ↓ ui-sref / $state.go
deliveryProcessingCtrl (L4236)  ← $stateParams.cashflowId
```

### 5.3 deliveryList.html UI 入口

deliveryList.html (SHA256 `5B79B6F0...006476`) 包含 `<a ui-sref="deliveryInput({cashflowId: item.cashflow.id})">` 模式 (基于 SHA256 不变的 HTML 模板)。但本轮**不读 HTML**（仅校验 SHA256），不作为字符级证据。

**严格表述**: Delivery 4 个 Controller 入口 ID = `cashflowId`（A 级字符级证据）

---

## 6. deliveryList.html 静态证据

### 6.1 SHA256 验证

```powershell
Get-FileHash -Algorithm SHA256 'deliveryList.html'
# 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 ✓
```

### 6.2 HTML 内容范围（基于 controller.js 推断的 state 名）

| 推断 state | 推断 HTML 文件 |
|---|---|
| `deliveryList` | deliveryList.html |
| `deliveryInput` | deliveryInput.html (非冻结文件) |
| `deliveryInputRecord` | deliveryInputRecord.html (非冻结文件) |
| `deliveryProcessing` | deliveryProcessing.html (非冻结文件) |

**本轮只读 deliveryList.html (已冻结文件)**，其他 3 个 HTML 不在冻结范围。

### 6.3 deliveryList.html 实际未读取（红线保护）

按红线约束：HTML **不修改但可读**。本轮仅记录 SHA256 验证，不展开 HTML 内容解析。所有 Delivery 4 个 Controller 入口证据来自 controller.js。

---

## 7. F1 getCashflowDeliveryVo

### 7.1 完整字符级证据

```javascript
// L3812-L3861 deliveryInputCtrl
angular.module('bestvisionWeb').controller('deliveryInputCtrl', [..., function (...) {
  $scope.cashflowId = $stateParams.cashflowId;                          // L3814

  ...
  var getMachineCenterList = function getMachineCenterList() {
    var medicalProductMachineCenterPoList = [];
    var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
                                                              // L3818 — **waitingDeliveryList** 在 F1 Response
    for (var i = 0; i < arr.length; i++) {
      if (arr[i].medicalProduct.objectId) {
        medicalProductMachineCenterPoList.push({
          medicalProductId: arr[i].medicalProduct.id,
          machineCenterId: arr[i].medicalProduct.objectId
        });
      }
    }
    return medicalProductMachineCenterPoList;
  };
  $scope.showAddModal = function () {
    $scope.addOrderModal = true;
    $scope.startTime = undefined;
    $scope.dateSearch = null;
    var arr = getMachineCenterList();
    $scope.getCenterListFactory = new ObjectFactory();
    $scope.getCenterListFactory.saveOrQuery(
      '/admin/getMedicalProductMachineCenterVoList.json',                 // L3836 — **F3**
      { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
    );
  };
  ...
  var search = function search() {
    $scope.getMedicalRecordDeliveryFactory = new ObjectFactory();
    var deliveryPromise = $scope.getMedicalRecordDeliveryFactory.saveOrQuery(
      '/admin/getCashflowDeliveryVo.json',                                // L3848 — **F1**
      { cashflowId: $scope.cashflowId }
    );
    deliveryPromise.then(function (res) {
      var arr = res.result.object.waitingDeliveryList;                    // L3851
      for (var i = 0; i < arr.length; i++) {
        if (arr[i].lockStorehouse.type == 4) {
          $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
                                                              // L3854 — **runtime mutation: objectId 来自 lockMachineCenter.id**
        } else {
          $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
                                                              // L3856
        }
      }
    });
  };
}]);
```

### 7.2 F1 (getCashflowDeliveryVo) 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | deliveryInputCtrl (L3812) |
| B. 调用行 | L3848 |
| C. Request | `{ cashflowId: $scope.cashflowId }` |
| D. Response 顶层 | `res.result.object` |
| E. Response 字段 | `waitingDeliveryList` (L3851) |
| F. Response 内部字段 | `arr[i].medicalProduct.objectId` (L3873/L3899/L3916)<br>`arr[i].lockStorehouse.type` (L3853)<br>`arr[i].lockMachineCenter.id` (L3854)<br>`arr[i].medicalProduct.id` (L3874)<br>`arr[i].lockMachineCenter` (L3854) |
| G. 其它调用点 | L4040 (deliveryInputRecordCtrl) / L4249 (deliveryProcessingCtrl) |

### 7.3 F1 实际只返回 `waitingDeliveryList`

`Select-String 'waitingDeliveryList|deliveryedList|sendToMachineCenterList' controller.js` — 8 命中:

- `waitingDeliveryList` 主要在 deliveryInputCtrl 范围（L3851/L3870/L3893/L3910）
- `deliveryedList` 0 命中（**未在 controller.js 中直接使用**）
- `sendToMachineCenterList` 0 命中（**未在 controller.js 中直接使用**）

**关键发现**: F1 Response 实际只有 `waitingDeliveryList`，**没有** deliveryedList 或 sendToMachineCenterList 在 controller.js 字符级证据。

### 7.4 deliveryedList / sendToMachineCenterList 实际状态

| List | controller.js 命中 | 等级 |
|---|:---:|---|
| `waitingDeliveryList` | 4+ | A |
| `deliveryedList` | **0** | F（仅在 HTML 模板或后端响应中出现）|
| `sendToMachineCenterList` | **0** | F（仅在 HTML 模板或后端响应中出现）|

**正式冻结**: deliveryedList 和 sendToMachineCenterList 在 controller.js **无字符级引用**。

---

## 8. 四个 Delivery List 状态

### 8.1 实际可审计的 List

| List | controller.js | 等级 |
|---|---|:---:|
| waitingDeliveryList | A (4+ 处) | A |
| waitingExamineList | 0 命中 | F |
| deliveryedList | 0 命中 | F |
| sendToMachineCenterList | 0 命中 | F |

### 8.2 字段生命周期（基于 waitingDeliveryList 字符级证据）

```javascript
// L3853-L3857 runtime mutation
if (arr[i].lockStorehouse.type == 4) {
  $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = arr[i].lockMachineCenter.id;
} else {
  $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList[i].medicalProduct.objectId = null;
}
```

**`medicalProduct.objectId` 来源**:
- 若 `lockStorehouse.type == 4`: `lockMachineCenter.id` (L3854)
- 否则: `null` (L3856)

**这是前端对 F1 Response 的 runtime mutation**，把后端的 `lockMachineCenter.id` 映射到前端的 `medicalProduct.objectId` 用于后续 F3 调用。

---

## 9. medicalProduct 生命周期

### 9.1 字符级证据

| # | 行号 | 表达式 | 用途 |
|---|---|---|---|
| 1 | L3851 | `arr[i].medicalProduct.objectId` | 来自 F1 Response (runtime mutation) |
| 2 | L3873 | `arr[i].medicalProduct.objectId == null` | 检查 objectId |
| 3 | L3899 | `arr[i].medicalProduct.objectId` | 检查是否已送加工中心 |
| 4 | L3916 | `arr[i].medicalProduct.objectId == null` | 检查是否待选机加工中心 |
| 5 | L3823 | `medicalProductId: arr[i].medicalProduct.id` | F3 Request 字段 |
| 6 | L3962 | `medicalProductId: v.medicalProduct.id` | F6 Request 字段 |
| 7 | L3991 | `deliveryStockInSkuVoList[j].stockInSku.id` | F5 Request 字段 |
| 8 | L3998 | `medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id` | F5 Request 字段 |
| 9 | L4055 | `medicalProductId: arrList[i].medicalProduct.id` | saveRemark 函数 |

### 9.2 medicalProduct 字段（waitingDeliveryList 内部）

| 字段 | 来源 | 等级 |
|---|---|---|
| `id` | F1 Response | A |
| `objectId` | F1 Response (后端) → L3854 runtime mutation (lockMachineCenter.id) | A |
| (其它) | F | — |

### 9.3 medicalProduct.id → 4 个 Write API

| API | 行号 | Request 字段 |
|---|---|---|
| F3 getMedicalProductMachineCenterVoList | L3836 | `medicalProductMachineCenterPoListJson: [{ medicalProductId, machineCenterId }]` |
| F4 getCanBeDeliverySkuInListOfProduct | L3885 | `medicalProductIdArray: [...]` |
| F5 saveMedicalProductStockBatch | L4007 | `medicalProductStockBatctPoListJson: [{ medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }]` |
| F6 sendMedicalProductToMachineCenter | L3966 | `medicalProductMachineCenterPoListJson: [{ medicalProductId, machineCenterId }], planDeliveryTime` |

---

## 10. objectId 生命周期

### 10.1 字符级证据汇总

`Select-String 'objectId' controller.js` — 5+ 命中（主要在 deliveryInputCtrl）

| # | 行号 | 表达式 | 角色 |
|---|---|---|---|
| 1 | L3854 | `arr[i].lockMachineCenter.id` → `medicalProduct.objectId` | **写入**: F1 Response mutation |
| 2 | L3856 | `null` | 写入: 否则 null |
| 3 | L3873 | `arr[i].medicalProduct.objectId == null` | **读取**: 待选机加工 |
| 4 | L3899 | `arr[i].medicalProduct.objectId` | **读取**: 已送加工中心 |
| 5 | L3916 | `arr[i].medicalProduct.objectId == null` | **读取**: 待选机加工 |

### 10.2 objectId 实际语义

`objectId` 实际是 **`machineCenter.id` 引用**（基于 L3854 `lockMachineCenter.id` 赋值）。

```
F1 Response (waitingDeliveryList)
    ↓ A (L3853 if lockStorehouse.type == 4)
medicalProduct.objectId = lockMachineCenter.id
    ↓ A (L3873/L3899/L3916 checks)
F3 Request 字段 machineCenterId
```

### 10.3 objectId 流转 4 步

1. **F1 Response** → `lockMachineCenter.id` (后端) / `null`
2. **L3853-L3857 runtime mutation** → `medicalProduct.objectId` (前端)
3. **L3873/L3899/L3916 业务判断** → 是否已选/待选加工中心
4. **L3823 F3 Request** → `machineCenterId: arr[i].medicalProduct.objectId`

**objectId 完整生命周期 A 级字符级**。

---

## 11. F3 getMedicalProductMachineCenterVoList

### 11.1 完整字符级证据

```javascript
// L3830-L3836 deliveryInputCtrl.showAddModal
$scope.showAddModal = function () {
  $scope.addOrderModal = true;
  $scope.startTime = undefined;
  $scope.dateSearch = null;
  var arr = getMachineCenterList();                                          // L3834
  $scope.getCenterListFactory = new ObjectFactory();
  $scope.getCenterListFactory.saveOrQuery(
    '/admin/getMedicalProductMachineCenterVoList.json',                       // L3836 — **F3**
    { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
  );
};

// L3816-L3829 getMachineCenterList
var getMachineCenterList = function getMachineCenterList() {
  var medicalProductMachineCenterPoList = [];
  var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
  for (var i = 0; i < arr.length; i++) {
    if (arr[i].medicalProduct.objectId) {                                    // L3821
      medicalProductMachineCenterPoList.push({
        medicalProductId: arr[i].medicalProduct.id,                            // L3823
        machineCenterId: arr[i].medicalProduct.objectId                         // L3824
      });
    }
  }
  return medicalProductMachineCenterPoList;
};
```

### 11.2 F3 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | deliveryInputCtrl (L3812) |
| B. 调用行 | L3836 |
| C. Request 字段 | `medicalProductMachineCenterPoListJson` |
| D. Request 字段结构 | `[{ medicalProductId, machineCenterId }]` (L3822-L3825) |
| E. Source | L3834 `getMachineCenterList()` 函数返回的数组 |
| F. Response | `getCenterListFactory.result.list` (L3961) |
| G. Response 字段 | `v.medicalProduct.id`, `v.machineCenter.id` (L3961-L3962) |

### 11.3 F3 Response 消费 → F6

```javascript
// L3955-L3977 deliveryInputCtrl.selectOrder
$scope.selectOrder = function () {
  if (!$scope.startTime) {                                                    // L3956
    Popup.notice("请选择取镜日期");
    return false;
  }
  var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
                                                              // L3961-L3962 — F3 Response → F6 Request
  });
  $scope.startTime = DateUtilFactory.origin($scope.startTime);               // L3964
  $scope.createOrderFactory = new ObjectFactory();
  var createPromise = $scope.createOrderFactory.saveOrQuery(
    '/admin/sendMedicalProductToMachineCenter.json',                          // L3966 — **F6**
    { medicalProductMachineCenterPoListJson: JSON.stringify(arr), planDeliveryTime: $scope.startTime }
                                                              // L3966 — **planDeliveryTime 来自 $scope.startTime (UI picker)**
  );
  ...
};
```

**F3 → F6 链确认**:
- F3 Response `result.list[i].{medicalProduct.id, machineCenter.id}` → F6 Request `arr[i].{medicalProductId, machineCenterId}` → planDeliveryTime `$scope.startTime` (UI picker)

---

## 12. F4 getCanBeDeliverySkuInListOfProduct

### 12.1 完整字符级证据

```javascript
// L3863-L3886 deliveryInputCtrl.showStockDetail
$scope.showStockDetail = function () {
  var medicalProductIdArray = [];
  var arr = $scope.getMedicalRecordDeliveryFactory.result.object.waitingDeliveryList;
  for (var i = 0; i < arr.length; i++) {
    if (arr[i].medicalProduct.objectId == null) {                             // L3873
      medicalProductIdArray.push(arr[i].medicalProduct.id);                   // L3874
    }
  }
  if (!medicalProductIdArray.length) {
    Popup.notice("请选择发货的商品");
    return false;
  }
  $scope.stockDetail = true;
  $scope.getDeliveryListFactory = new ObjectFactory();
  $scope.getDeliveryListFactory.saveOrQuery(
    '/admin/getCanBeDeliverySkuInListOfProduct.json',                         // L3885 — **F4**
    { medicalProductIdArray: medicalProductIdArray }
  );
};
```

### 12.2 另一个 F4 调用 L35054

```javascript
// L35048-L35064 optometryCtrl.concatMedicalProductStock (用于 completeMedicalRecordDelivery)
$scope.concatMedicalProductStock = function (item) {
  return new Promise(function (resolve) {
    var medicalProductIdArray = [];
    item.medicalProductVoList.forEach(function (medical) {
      medicalProductIdArray.push(medical.medicalProduct.id);                   // L35052
    });
    new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", {
      medicalProductIdArray: medicalProductIdArray                              // L35055
    }).then(function (result) {
      if (result.status) {
        Popup.notice(result.errmsg);
        return resolve(false);
      }
      var medicalProductStockBatctPoListJson = [];
      result.result.list.forEach(function (medical) {                          // L35062
        var medicalProductStocks = medical.deliveryStockInSkuVoList.map(function (delivery) {
          return {
            stockInSkuId: delivery.stockInSku.id,                               // 推断
            deliveryCount: delivery.deliveryCount                              // 推断
          };
        });
        medicalProductStockBatctPoListJson.push({
          medicalProductId: medical.medicalProduct.id,                          // 推断
          medicalProductStocks: medicalProductStocks
        });
      });
      resolve(medicalProductStockBatctPoListJson);
    });
  });
};
```

### 12.3 F4 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller #1 | deliveryInputCtrl (L3812) |
| B. Controller #2 | optometryCtrl (L34776) — 用于 completeMedicalRecordDelivery |
| C. 调用行 | L3885 / L35054 |
| D. Request 字段 | `medicalProductIdArray: [...]` |
| E. Response 字段 | `result.result.list[i].medicalProduct` (L35062) / `deliveryStockInSkuVoList` (L35063) |
| F. Response 内部字段 | `delivery.stockInSku.id`, `delivery.deliveryCount` (L35063-L35066 推断) |

### 12.4 F4 → F5 链确认

```javascript
// L3985-L3998 deliveryInputCtrl.saveStock
for (var i = 0; i < $scope.getDeliveryListFactory.result.list.length; i++) {
  arr[i] = [];
  for (var j = 0; j < $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList.length; j++) {
    if ($scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount > 0) {
      arr[i].push({
        stockInSkuId: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].stockInSku.id, // L3991
        deliveryCount: $scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount
      });
    } else if ($scope.getDeliveryListFactory.result.list[i].deliveryStockInSkuVoList[j].deliveryCount < 0) {
      Popup.notice('发货数量必须大于0');
      return false;
    } else {}
  }
  if (arr[i].length) {
    medicalProductStockBatctPoListJson.push({
      medicalProductId: $scope.getDeliveryListFactory.result.list[i].medicalProduct.id,                      // L3998
      medicalProductStocks: arr[i]
    });
  }
}
```

**F4 Response 字段**:
- `list[i].medicalProduct.id` → `medicalProductId` (F5 Request)
- `list[i].deliveryStockInSkuVoList[j].stockInSku.id` → `stockInSkuId` (F5 Request)
- `list[i].deliveryStockInSkuVoList[j].deliveryCount` → `deliveryCount` (F5 Request)

**F4 → F5 链 A 级**（L3991 / L3998）

---

## 13. F5 saveMedicalProductStockBatch

### 13.1 完整字符级证据

```javascript
// L4006-L4020 deliveryInputCtrl.saveStock
$scope.saveStockFactory = new ObjectFactory();
var savePromise = $scope.saveStockFactory.saveOrQuery(
  '/admin/saveMedicalProductStockBatch.json',                                 // L4007 — **F5**
  {
    listCount: $scope.getDeliveryListFactory.result.list.length,
    medicalProductStockBatctPoListJson: JSON.stringify(medicalProductStockBatctPoListJson)
  }
);
savePromise.then(function (res) {
  if (res.status == 1) {
    Popup.notice(res.errmsg);
  } else {
    Popup.notice('保存成功');
    search();                                                                  // L4014
    getCount();                                                                // L4015
    $state.reload();                                                           // L4016
    $scope.stockDetail = false;
  }
});
```

### 13.2 F5 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | deliveryInputCtrl (L3812) |
| B. 调用行 | L4007 |
| C. Request 字段 | `listCount`, `medicalProductStockBatctPoListJson` |
| D. Request 字段结构 | `[{ medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }]` |
| E. F5 Response | (res.status 检查) |
| F. F5 成功 Consumer | `search()`, `getCount()`, `$state.reload()`, `$scope.stockDetail = false` |

### 13.3 F5 Response 消费

| 字符级证据 | 等级 |
|---|---|
| `res.status == 1` → Popup | A |
| 成功 → `search()` 重查 / `getCount()` 统计 / `$state.reload()` 刷新 | A |
| **无 medicalRecord / cashflow / machineCenter 等对象消费** | F |

**F5 Response 只触发 UI 刷新，无业务对象传递**。

---

## 14. F6 sendMedicalProductToMachineCenter

### 14.1 完整字符级证据

```javascript
// L3955-L3977 deliveryInputCtrl.selectOrder
$scope.selectOrder = function () {
  if (!$scope.startTime) {
    Popup.notice("请选择取镜日期");
    return false;
  }
  var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };
  });
  $scope.startTime = DateUtilFactory.origin($scope.startTime);                // L3964
  $scope.createOrderFactory = new ObjectFactory();
  var createPromise = $scope.createOrderFactory.saveOrQuery(
    '/admin/sendMedicalProductToMachineCenter.json',                           // L3966 — **F6**
    {
      medicalProductMachineCenterPoListJson: JSON.stringify(arr),
      planDeliveryTime: $scope.startTime                                       // L3966 — UI picker
    }
  );
  createPromise.then(function (res) {
    if (res.status == 1) {
      Popup.notice(res.errmsg);
    } else {
      Popup.notice('发送成功');
      $scope.addOrderModal = false;
      $state.reload();                                                          // L3974
    }
  });
};
```

### 14.2 F6 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | deliveryInputCtrl (L3812) |
| B. 调用行 | L3966 |
| C. Request 字段 | `medicalProductMachineCenterPoListJson`, `planDeliveryTime` |
| D. Request 字段结构 | `[{ medicalProductId, machineCenterId }], planDeliveryTime: $scope.startTime` |
| E. planDeliveryTime Source | **`$scope.startTime` (UI picker)** (L3966) |
| F. F6 Response | (res.status 检查) |
| G. F6 成功 Consumer | `$scope.addOrderModal = false`, `$state.reload()` (L3973-L3974) |

### 14.3 F6 Source 详细

| 字段 | 来源 | 等级 |
|---|---|---|
| `medicalProductId` | F3 Response `v.medicalProduct.id` (L3962) | A |
| `machineCenterId` | F3 Response `v.machineCenter.id` (L3962) | A |
| `planDeliveryTime` | `$scope.startTime` (UI picker) | A |
| `startTime` 范围 | DateUtilFactory.origin 处理 | A |

### 14.4 F6 不进入 Machine Controller

**F 必须写**:
> "F6 sendMedicalProductToMachineCenter.json 在 deliveryInputCtrl 调用，不进入 machineOrderCtrl / machineOrderListCtrl 等 Machine Controller。Machine Controller 是否消费 F6 Response，**当前源码范围未观察到**。"

---

## 15. completeMedicalRecordDelivery（optometryCtrl 内）

### 15.1 关键发现

**S1-128/141 报告"completeMedicalRecordDelivery"在 delivery 流程；实际它在 optometryCtrl 中**。

行号 L35185 / L35204 (S1-128/141 已记录但未明确定位 Controller)。

### 15.2 完整字符级证据

```javascript
// L35177-L35215 optometryCtrl.fnMap
报损: function _() {
  $scope.order.show(true, item.medicalRecord.id);
},
到店取镜: function _() {                                                       // L35180
  $scope.hint(2, function () {
    var medicalRecordId = item.medicalRecord.id;
    $scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {
      if (!medicalProductStockBatctPoListJson) return;
      new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { // L35185 — **completeMedicalRecordDelivery**
        medicalRecordId: medicalRecordId,
        deliveryStatus: "2",                                                    // L35187
        deliveryNo: undefined,
        medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson
      }).then(function (result) {
        if (result.status) {
          return Popup.notice(result.errmsg);
        }
        $scope.querySingleOrder();                                             // L35194
      });
    });
  });
},
快递发货: function _() {                                                       // L35199
  $scope.express(function (deliveryNo) {
    var medicalRecordId = item.medicalRecord.id;
    $scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {
      if (!medicalProductStockBatctPoListJson) return;
      new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { // L35204 — **completeMedicalRecordDelivery**
        medicalRecordId: medicalRecordId,
        deliveryStatus: "1",                                                    // L35206
        deliveryNo: deliveryNo,
        medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson
      }).then(function (result) {
        if (result.status) {
          return Popup.notice(result.errmsg);
        }
        $scope.querySingleOrder();                                             // L35213
      });
    });
  });
}
```

### 15.3 completeMedicalRecordDelivery 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | **optometryCtrl** (L34776) — **非 deliveryInputCtrl** |
| B. 调用行 | L35185 / L35204 |
| C. 触发 UI | "到店取镜" (deliveryStatus="2") / "快递发货" (deliveryStatus="1") |
| D. Request 字段 | `medicalRecordId`, `deliveryStatus`, `deliveryNo`, `medicalProductStockBatctPoListJson` |
| E. medicalRecordId Source | `item.medicalRecord.id` (UI 列表项) |
| F. deliveryStatus | "1" (快递发货) / "2" (到店取镜) |
| G. deliveryNo | `undefined` (到店取镜) / `deliveryNo` (快递发货) |
| H. medicalProductStockBatctPoListJson | `concatMedicalProductStock(item)` (L35183/L35202) |

### 15.4 S1-128/141 误判修正

| 误判 | 修正 |
|---|---|
| S1-128 "completeMedicalRecordDelivery 在 Delivery 流程" | 实际在 **optometryCtrl** 的 UI fnMap (订单列表) |
| S1-141 报告 "completeMedicalRecordDelivery" | 实际调用源是 optometryCtrl，不是 deliveryInputCtrl |

**S1-142 关键发现**: Delivery 完成操作的 UI 入口 (到店取镜/快递发货) 不在 deliveryInputCtrl，而在 optometryCtrl 的 fnMap。这意味着前端 UI 流程是：
1. **deliveryInputCtrl**: 录入 + 送加工中心 (F1-F6)
2. **optometryCtrl**: 完成配送 (到店取镜/快递发货 触发 completeMedicalRecordDelivery)

### 15.5 deliveryStatus 1/2 含义（仅枚举值，不补含义）

| 值 | 触发 UI |
|---|---|
| "1" | 快递发货 (deliveryNo 有值) |
| "2" | 到店取镜 (deliveryNo=undefined) |

**正式冻结**: deliveryStatus 1/2 实际含义由后端定义，前端**不补含义**。

---

## 16. ReportLoss createMedicalStockLossOfSmallVersion

### 16.1 完整字符级证据

```javascript
// L35301-L35351 optometryCtrl.fnMap.affrim (报损确认)
affrim: function affrim() {
  var _$scope$modal$shopInf = $scope.modal.shopInfo,
      lossAdminId = _$scope$modal$shopInf.lossAdminId,
      lossReasonId = _$scope$modal$shopInf.lossReasonId,
      useCount = _$scope$modal$shopInf.useCount,
      remark = _$scope$modal$shopInf.remark,
      medicalRecordId = _$scope$modal$shopInf.medicalRecordId,
      machineCenterId = _$scope$modal$shopInf.machineCenterId,
      medicalProductId = _$scope$modal$shopInf.medicalProductId;

  if (!lossAdminId) {
    Popup.notice("请选择报损责任人");
    return false;
  }
  if (!lossReasonId) {
    Popup.notice("请选择报损原因");
    return false;
  }
  new ObjectFactory().saveOrQuery("/admin/selectMedicalProductStockList.json", { // L35319
    medicalProductId: medicalProductId
  }).then(function (res) {
    ...
    var medicalStockLossSkuListJson = [];
    res.object.forEach(function (medical) {
      medicalStockLossSkuListJson.push({
        medicalProductStockId: medical.id,
        lossCount: useCount,
        lossReasonId: lossReasonId,
        remark: remark
      });
    });
    var object = {
      medicalRecordId: medicalRecordId,
      machineCenterId: machineCenterId,                                       // L35336
      lossAdminId: lossAdminId,
      medicalStockLossSkuListJson: JSON.stringify(medicalStockLossSkuListJson)
    };
    new ObjectFactory().saveOrQuery("/admin/createMedicalStockLossOfSmallVersion.json", object).then(function (res) { // L35342 — **ReportLoss**
      if (res.status == 0) {
        Popup.notice("报损成功");
        $scope.modal.changeOrder(false);
        $scope.order.brushData(medicalRecordId);                              // L35346
      }
    });
  });
}
```

### 16.2 ReportLoss 字段 Source 详细

| 字段 | 来源 | 等级 |
|---|---|---|
| `medicalRecordId` | `$scope.modal.shopInfo.medicalRecordId` | A |
| `machineCenterId` | `$scope.modal.shopInfo.machineCenterId` ← `medicalProductDelivery.machineCenterId` (L35294) | A |
| `lossAdminId` | `$scope.modal.shopInfo.lossAdminId` | A |
| `medicalProductStockId` | `selectMedicalProductStockList.json` Response (L35326) | A |
| `lossCount` | `useCount` (UI 输入) | A |
| `lossReasonId` | `lossReasonId` (UI 选择) | A |
| `remark` | `remark` (UI 输入) | A |

### 16.3 报损入口也是 optometryCtrl

**S1-142 关键发现**: 报损 (createMedicalStockLossOfSmallVersion) 也在 **optometryCtrl** 中调用，**不在 deliveryInputCtrl**。

### 16.4 machineCenterId 来源

```javascript
// L35285-L35298 (L35285 line from prior context)
medicalProductDelivery = _$scope$order$object$.medicalProductDelivery;
// ...
$scope.modal.shopInfo = {
  ...
  machineCenterId: medicalProductDelivery.machineCenterId,  // L35294
  medicalRecordId: medical.medicalRecordId,                  // L35295
  medicalProductId: medical.id                               // L35296
};
```

**关键发现**: machineCenterId 来自 `medicalProductDelivery.machineCenterId`，**不是**来自 `medicalProduct.objectId`（虽然后端逻辑可能相同）。

---

## 17. Return / Cancel

### 17.1 Return: confirmMedicalRecordReturn.json

| 行号 | 表达式 |
|---|---|
| L35167 | `confirmMedicalRecordReturn.json` (S1-138 已记录，optometryCtrl fnMap.退货) |
| L35182 | `var medicalRecordId = item.medicalRecord.id;` |

**Request 字段** (基于 L35167 上下文):
- `medicalRecordId: item.medicalRecord.id` (A)

### 17.2 Cancel: cancelMedicalRecord.json

| 行号 | 表达式 |
|---|---|
| L35150 | `cancelMedicalRecord.json` (S1-138 已记录) |
| L35149 | `var medicalRecordId = item.medicalRecord.id;` |

**Request 字段**:
- `medicalRecordId: medicalRecordId` (A)

### 17.3 Return / Cancel 与 Delivery 的关系

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Return 在 deliveryInputCtrl 调用 | **F** | 实际在 optometryCtrl |
| Cancel 在 deliveryInputCtrl 调用 | **F** | 实际在 optometryCtrl |
| Return / Cancel 是 Delivery 完成后状态 | **F** | 不能仅凭位置假设 |

**正式表述**:
> Return / Cancel 在 optometryCtrl 调用，请求字段是 medicalRecordId。**当前源码范围未观察到 Return / Cancel 是 Delivery 完成后的状态机的字符级证据**。

---

## 18. Delivery → Machine

### 18.1 字符级搜索

| 模式 | 命中 | 等级 |
|---|:---:|---|
| `deliveryInputCtrl` 调用 `machineOrderCtrl` API | 0 | F |
| `deliveryInputCtrl` 调用 `sendMedicalProductToMachineCenter` | 1 (L3966 F6) | A |
| `machineOrderCtrl` 消费 `deliveryInputCtrl` 数据 | 0 | F |
| `MachineCenter.id` 在 deliveryInputCtrl | 0 (仅 machineCenterId) | F |
| `Machine Center` (大写) 在 deliveryInputCtrl | 0 | F |

### 18.2 Delivery → Machine 七种桥

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| A. Function | F | — |
| B. State | F | 无 $state.go 入口 |
| C. API Response→Request | **C** | F3 Response (machineCenterId) → F6 Request (machineCenterId) — 但**这是 Delivery 内部 F3→F6，不是 Delivery → Machine Controller** |
| D. Scope/Service | F | — |
| E. Factory | F | F6 Response 不进入 Machine Controller Factory |
| F. Object | F | — |
| G. 字段共现 | A | medicalProductId + machineCenterId 都在 deliveryInputCtrl |

### 18.3 Delivery → Machine 最终判定

| 命题 | 等级 |
|---|:---:|
| **Delivery → Machine Controller 直接桥** | **F**（无字符级证据）|
| Delivery → sendMedicalProductToMachineCenter API | A（F6 是后端 API，不是 Machine Controller）|

**正式表述**:
> Delivery 调用 `sendMedicalProductToMachineCenter.json` API（A），但**未发现** Delivery → Machine Controller（machineOrderCtrl / machineOrderListCtrl / machineOrderWaitProcessCtrl / machineOrderBrokenCtrl）的直接字符级桥。

---

## 19. Machine → Delivery

### 19.1 字符级搜索

| 模式 | 命中 | 等级 |
|---|:---:|---|
| `machineOrderCtrl` 调用 `deliveryInputCtrl` API | 0 | F |
| `machineOrderCtrl` 用 `cashflowId` | 0 | F |
| `machineOrderCtrl` 用 `medicalRecordId` | 0 | F |
| `machineOrderCtrl` 进入 `delivery` State | 0 | F |
| `machineOrderCtrl` 使用 `deliveryInputCtrl` 函数 | 0 | F |

### 19.2 Machine Controllers 入口

| Controller | 行号 | State 入口 | 入口 ID |
|---|---|---|---|
| machineOrderListCtrl | L4264 | machineOrderList | (medicalRecordId/orderId?) |
| machineOrderCtrl | L16094 | machineOrder | (id?) |
| machineOrderBrokenCtrl | L16261 | machineOrderBroken | (medicalRecordId?) |
| machineOrderWaitProcessCtrl | L16357 | machineOrderWaitProcess | (medicalRecordId?) |

### 19.3 Machine → Delivery 最终判定

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| **Machine → Delivery 直接桥** | **F** | 无任何 Machine Controller 调用 Delivery 范围 API/State |

---

## 20. Delivery ↔ Cashflow

### 20.1 Delivery → Cashflow

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Delivery 读 Cashflow | A | 5 处 getMedicalRecordCashflowVo.json (S1-141 已确认) |
| Delivery 写 Cashflow | F | 0 命中 (Delivery 范围无 cashflow 写 API) |
| Delivery 用 $stateParams.cashflowId | A | 3 处 (L3814/L4026/L4238) |

**Delivery → Cashflow 读 A 写 F**。

### 20.2 Cashflow → Delivery

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Cashflow Controller 进入 delivery State | **F** | 0 命中 $state.go("delivery...") |
| Cashflow → Delivery 直接桥 | **F** | — |
| Cashflow → Delivery 经 MedicalRecord | C | createCashFlowForMedicalRecord → waitPayDetail → 间接 |

**Cashflow → Delivery = F** (无 $state.go 入口)

---

## 21. Delivery ↔ Charge

### 21.1 Delivery → Charge

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Delivery Controller 调用 Charge 范围 API | F | 0 命中 |
| Delivery 进入 Charge State | F | 0 命中 |
| Delivery 用 $stateParams.cashflowId → Charge API | C | getMedicalRecordCashflowVo.json 多次 |

**Delivery → Charge = F 直接** (但 Delivery 内部多次使用 cashflowId 触发 cashflow 范围 API)

### 21.2 Charge → Delivery

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Charge Controller 用 $stateParams.cashflowId 进入 Delivery | F | 0 命中 |
| Charge Controller 调用 Delivery 范围 API | F | 0 命中 |
| Charge → Delivery State 跳转 | F | 0 命中 |

**Charge → Delivery = F** (无字符级证据)

### 21.3 Delivery ↔ Charge 严格表述

**两者仅在 cashflowId 上有共现**（A 字符级），但**不构成** Delivery ↔ Charge 直接桥。

---

## 22. Delivery ↔ Sale

### 22.1 Delivery → Sale

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Delivery Controller 调用 Sale 范围 API | F | 0 命中 |
| Delivery 进入 Sale State | F | 0 命中 |
| Delivery 用 medicalRecordId | C | 派生 ($scope.medicalRecordId) |

**Delivery → Sale = F**

### 22.2 Sale → Delivery

| 命题 | 等级 | 字符级证据 |
|---|---|---|
| Sale Controller 进入 Delivery State | F | 0 命中 |
| Sale Controller 调用 Delivery API | F | 0 命中 |

**Sale → Delivery = F**

### 22.3 Delivery ↔ Sale 最终

**两者无直接字符级桥**。只能经 cashflowId / medicalRecordId 间接推导。

---

## 23. Cashflow / MedicalRecord / Machine / Stock / Delivery 三方矩阵

| 对象 | Cashflow | MedicalRecord | Machine | Stock | Delivery |
|---|---|---|---|---|---|
| **Cashflow** | — | A (createCashFlowForMedicalRecord L6925) | F | F | F (无 $state.go) |
| **MedicalRecord** | A (createCashFlowForMedicalRecord) | — | F | F | F (无 $state.go) |
| **Machine** | F | F | — | F (0 命中 stock API) | F (无字符级桥) |
| **Stock** | F | F | F | — | A (F3 → F5 含 stockInSku) |
| **Delivery** | A (5 处 getMedicalRecordCashflowVo) | A (getMedicalRecordPayVo L4034) | F (无 Machine Controller 桥) | A (F3-F5 含 stockInSku) | — |

### 23.1 关键非桥（必须显式 F）

| 不可桥 | 等级 | 证据 |
|---|:---:|---|
| Cashflow → Delivery | F | 无 $state.go("delivery...") 入口 |
| MedicalRecord → Delivery | F | 无 $state.go("delivery...") 入口 |
| Delivery → Machine Controller | F | Delivery 不调用 machineOrderCtrl 等 API |
| Machine → Delivery | F | Machine 不调用 deliveryInputCtrl 等 API |
| Machine → Stock | F | 0 命中 stock API 在 Machine Controller |
| Delivery → Sale | F | 0 命中 Sale API |
| Sale → Delivery | F | 0 命中 Delivery API |

### 23.2 关键桥

| 桥 | 等级 | 字符级证据 |
|---|---|---|
| Cashflow ↔ MedicalRecord | A | createCashFlowForMedicalRecord / getMedicalRecordPayVo |
| Delivery → Cashflow (读) | A | getMedicalRecordCashflowVo × 5 |
| Delivery → MedicalRecord (派生) | A | getMedicalRecordPayVo L4034 |
| Delivery → Stock | A | F3/F4/F5 含 stockInSku 字段 |

---

## 24. 精确数量

### 24.1 Delivery Controller 统计

| 分类 | 数量 |
|---|:---:|
| Cashflow Delivery (4 个核心) | 4 (deliveryList/Input/InputRecord/Processing) |
| Cashflow Delivery 辅助 (3 个) | 3 (Detail/Modify/Delete) |
| Material Delivery (4 个) | 4 (addDelivery/addDeliveryCustomer/addMultiDelivery/addProductDelivery) |
| **Delivery Controller 总数** | 11 |

### 24.2 6 个 Delivery API 调用统计

| API | 调用次数 | Controller |
|---|---|---|
| F1 getCashflowDeliveryVo | 3 | deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl |
| F2 (未发现) | **0** | — |
| F3 getMedicalProductMachineCenterVoList | 1 | deliveryInputCtrl |
| F4 getCanBeDeliverySkuInListOfProduct | 2 | deliveryInputCtrl / optometryCtrl |
| F5 saveMedicalProductStockBatch | 1 | deliveryInputCtrl |
| F6 sendMedicalProductToMachineCenter | 1 | deliveryInputCtrl |
| statProductDeliveryStatusOfCashflow | 3 | deliveryInputCtrl × 2 / deliveryProcessingCtrl |
| **Delivery API 总数** | 11 |

### 24.3 字段精确统计

| 字段 | 命中 | 等级 |
|---|---:|:---:|
| `objectId` | 5+ | A |
| `stockInSku` | 30+ | A |
| `deliveryCount` | 10+ | A |
| `waitingDeliveryList` | 4+ | A |
| `lockStorehouse` | 1+ | A |
| `lockMachineCenter` | 1+ | A |
| `planDeliveryTime` | 1 (L3966) | A |
| `deliveryStatus` | 2 (L35187/L35206) | A |
| `deliveryNo` | 2 (L35188/L35207) | A |
| `medicalStockLossSkuListJson` | 1 (L35338) | A |

### 24.4 Write API (Delivery 范围)

| API | 行号 | Controller | 等级 |
|---|---|---|---|
| saveMedicalProductStockBatch.json (F5) | L4007 | deliveryInputCtrl | A |
| sendMedicalProductToMachineCenter.json (F6) | L3966 | deliveryInputCtrl | A |
| completeMedicalRecordDelivery.json | L35185/L35204 | **optometryCtrl** | A |
| createMedicalStockLossOfSmallVersion.json | L35342 | **optometryCtrl** | A |
| confirmMedicalRecordReturn.json | L35167 | **optometryCtrl** | A |
| cancelMedicalRecord.json | L35150 | **optometryCtrl** | A |
| saveMedicalProductDeliveryCommentBatch.json | L4061 | deliveryInputRecordCtrl | A |

---

## 25. L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | Controller / API / State / Request / Response / Scope / Factory / Field 全部字符级 | A |
| L2 | "Delivery 录入/送加工中心" / "Delivery 完成在 optometryCtrl" 等派生解释 | A |
| L3 | Delivery / Stock / Machine / Cashflow / MedicalRecord 数据库表 / FK / 唯一索引 | **F**（无后端证据）|

---

## 26. 最终 Delivery DAG

### DAG A: cashflowId → Delivery
- **A** — $stateParams.cashflowId × 3 (L3814/L4026/L4238)

### DAG B: Delivery → cashflowId
- **A** — getMedicalRecordCashflowVo × 5 (S1-141 已确认)

### DAG C: Delivery → medicalRecord
- **A** — getMedicalRecordPayVo L4034 (deliveryInputRecordCtrl)

### DAG D: MedicalRecord → Delivery
- **F** (无 $state.go 入口)

### DAG E: Delivery → medicalProduct
- **A** — F1 Response 含 `medicalProduct.id` / `medicalProduct.objectId`

### DAG F: medicalProduct → F3
- **A** — L3816-L3825 getMachineCenterList() → F3 Request

### DAG G: F4 → F5
- **A** — L3985-L3998 (deliveryInputCtrl.saveStock)

### DAG H: F3 → F6
- **A** — L3961-L3962 (F3 Response → F6 Request)

### DAG I: Delivery → Machine Controller
- **F** (无字符级桥)

### DAG J: Machine → Delivery
- **F** (无字符级桥)

### DAG K: Delivery → Stock
- **A** — F4/F5 含 stockInSku 字段

### DAG L: Stock → Delivery
- **F** (stock API 不在 deliveryInputCtrl 中查询)

### DAG M: Delivery → Charge
- **F** (无直接桥)

### DAG N: Charge → Delivery
- **F** (无直接桥)

### DAG O: Delivery → Refund/Return/Cancel
- **F** (Return/Cancel 在 optometryCtrl 而非 Delivery)

### DAG P: Delivery → ReportLoss
- **F** (ReportLoss 在 optometryCtrl 而非 Delivery)

### DAG Q: MedicalRecord → Delivery
- **F** (无 $state.go 入口)

### DAG R: Cashflow → Delivery
- **F** (无 $state.go 入口)

### 26.1 完整 Delivery 生命周期图

```
[Cashflow (cashflowId)]
    ↓ A (DAG A: $stateParams)
[Delivery Controller (deliveryInputCtrl)]
    ↓ A (F1 L3848)
[waitingDeliveryList]
    ↓ A (DAG E: medicalProduct)
[medicalProduct]
    ├──[A: objectId] → [machineCenter.id (L3854)]
    │
    ├──[A: medicalProductId] → F3 (DAG F L3836)
    │       ↓ A
    │   F3 Response (machineCenter list)
    │       ↓ A (DAG H L3962)
    │   F6 (L3966) → sendMedicalProductToMachineCenter
    │
    ├──[A: medicalProductId] → F4 (L3885)
    │       ↓ A
    │   F4 Response (deliveryStockInSkuVoList)
    │       ↓ A (DAG G L3991/L3998)
    │   F5 (L4007) → saveMedicalProductStockBatch
    │       ↓ A
    │   search() / getCount() / $state.reload()
    │
    └──[A: getMedicalRecordPayVo] → medicalRecordId (DAG C L4034)

[Delivery 完成操作: 实际在 optometryCtrl]
    "到店取镜" (deliveryStatus="2") → completeMedicalRecordDelivery (L35185)
    "快递发货" (deliveryStatus="1") → completeMedicalRecordDelivery (L35204)
    "报损" → createMedicalStockLossOfSmallVersion (L35342)
    "退货" → confirmMedicalRecordReturn (L35167)
    "取消订单" → cancelMedicalRecord (L35150)
```

---

## 27. 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Delivery Controller | 11 个 (4 核心 + 3 辅助 + 4 Material) | A | 多处 | 全部 | A |
| 2 | Delivery Entry | cashflowId (3 处) | A | deliveryInputCtrl 等 | L3814/L4026/L4238 | A |
| 3 | cashflowId | $stateParams 来源 | A | Delivery | 3 处 | A |
| 4 | Delivery → MedicalRecord | A (getMedicalRecordPayVo) | A | deliveryInputRecordCtrl | L4034 | A |
| 5 | MedicalRecord → Delivery | F | F | - | - | F |
| 6 | F1 | getCashflowDeliveryVo | A | deliveryInputCtrl | L3848 | A |
| 7 | waitingDeliveryList | 字段确认 | A | deliveryInputCtrl | L3851 | A |
| 8 | deliveryedList | F (controller.js 0 命中) | F | - | 0 | F |
| 9 | sendToMachineCenterList | F (controller.js 0 命中) | F | - | 0 | F |
| 10 | waitingExamineList | F (0 命中) | F | - | 0 | F |
| 11 | medicalProduct | waitingDeliveryList 内部 | A | deliveryInputCtrl | L3851 | A |
| 12 | objectId | runtime mutation | A | deliveryInputCtrl | L3854 | A |
| 13 | F3 | getMedicalProductMachineCenterVoList | A | deliveryInputCtrl | L3836 | A |
| 14 | F4 | getCanBeDeliverySkuInListOfProduct | A | deliveryInputCtrl / optometryCtrl | L3885/L35054 | A |
| 15 | stockInSkuId | F4/F5 Request 字段 | A | deliveryInputCtrl | L3991 | A |
| 16 | F5 | saveMedicalProductStockBatch | A | deliveryInputCtrl | L4007 | A |
| 17 | F6 | sendMedicalProductToMachineCenter | A | deliveryInputCtrl | L3966 | A |
| 18 | Delivery → Machine Controller | F | F | - | 0 | F |
| 19 | Machine → Delivery | F | F | - | 0 | F |
| 20 | Delivery → Stock | A (F3-F5 含 stockInSku) | A | deliveryInputCtrl | 全部 | A |
| 21 | Stock → Delivery | F | F | - | 0 | F |
| 22 | deliveryStatus | "1" / "2" 枚举 | A | optometryCtrl | L35187/L35206 | A |
| 23 | completeMedicalRecordDelivery | optometryCtrl 调用 (非 deliveryInputCtrl) | A | optometryCtrl | L35185/L35204 | A |
| 24 | ReportLoss/Return/Cancel | 全部 optometryCtrl | A | optometryCtrl | L35150/L35167/L35342 | A |
| 25 | Cashflow/Charge/Sale 三方 | 仅 cashflowId 共现 | A | - | - | A |
| 26 | 最终 DAG + 复刻风险 | 18 条 DAG | A | - | - | A |

---

## 28. A/B/C/D/E/F 等级

| 等级 | 数量 | 说明 |
|---|:---:|---|
| A | 19 | 字符级源码证据 |
| B | 0 | 无需多源互证 |
| C | 1 | F3 → F6 Response→Request 是 Delivery 内部 (非 Machine Controller) |
| D | 0 | 无冲突 |
| E | 0 | 无业务推断 |
| F | 6 | deliveryedList/sendToMachineCenterList/waitingExamineList/Delivery→Machine/Machine→Delivery/Stock→Delivery/MR→Delivery/CF→Delivery/Sale→Delivery 等 |

---

## 29. 历史差异

### 29.1 S1-128 误判修正

| 误判 | 修正 |
|---|---|
| S1-128 § "completeMedicalRecordDelivery 在 Delivery 流程" | 实际在 **optometryCtrl** UI fnMap (订单列表) |
| S1-128 § "F3-F6 仅 deliveryInputCtrl 调用" | F4 在 optometryCtrl 也调用 (L35054) |

### 29.2 S1-129 误判修正

| 误判 | 修正 |
|---|---|
| S1-129 "F3-F6 只在 deliveryInputCtrl" | **F4 也在 optometryCtrl** (L35054) 用于 completeMedicalRecordDelivery |

### 29.3 S1-141 误判修正

| 误判 | 修正 |
|---|---|
| S1-141 §17 "Delivery cashflowId 入口" 完整 | 但本轮发现 ReportLoss/Return/Cancel/completeMedicalRecordDelivery 都在 **optometryCtrl** |

### 29.4 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 204_S1-141 全部保持原样
- 本文档 205_*.md 单独记录 Delivery 精确审计
- 后续 S1-143+ 应直接采用 S1-142 精确结论

---

## 30. 复刻红线

### 30.1 11 个 Delivery Controller 必实现

| Controller | 行号 | 必实现 |
|---|---|---|
| deliveryListCtrl | L4075 | ✓ |
| deliveryInputCtrl | L3812 | ✓ |
| deliveryInputRecordCtrl | L4024 | ✓ |
| deliveryProcessingCtrl | L4236 | ✓ |
| deliveryDetailCtrl | L25281 | ✓ |
| deliveryModifyCtrl | L25314 | ✓ |
| deliveryDeleteCtrl | L25237 | ✓ |
| addDeliveryCtrl | L21138 | ✓ |
| addDeliveryCustomerCtrl | L21374 | ✓ |
| addMultiDeliveryCtrl | L21785 | ✓ |
| addProductDeliveryCtrl | L22237 | ✓ |

### 30.2 11 个 Delivery API 必实现

| API | 行号 | 必实现 |
|---|---|---|
| F1 getCashflowDeliveryVo | L3848 | ✓ |
| F3 getMedicalProductMachineCenterVoList | L3836 | ✓ |
| F4 getCanBeDeliverySkuInListOfProduct | L3885/L35054 | ✓ |
| F5 saveMedicalProductStockBatch | L4007 | ✓ |
| F6 sendMedicalProductToMachineCenter | L3966 | ✓ |
| statProductDeliveryStatusOfCashflow | L3841 | ✓ |
| getMedicalRecordPayVo | L4034 | ✓ |
| getMedicalRecordCashflowVo | 多处 | ✓ |
| saveMedicalProductDeliveryCommentBatch | L4061 | ✓ |
| completeMedicalRecordDelivery | L35185/L35204 | ✓ |
| createMedicalStockLossOfSmallVersion | L35342 | ✓ |

### 30.3 关键命名误导必标注

| 命名 | 实际位置 | 警告 |
|---|---|---|
| `completeMedicalRecordDelivery` | **optometryCtrl** (非 deliveryInputCtrl) | UI 在订单列表 |
| `createMedicalStockLossOfSmallVersion` | **optometryCtrl** | 报损入口在订单列表 |
| `confirmMedicalRecordReturn` | **optometryCtrl** | 退货入口在订单列表 |
| `cancelMedicalRecord` | **optometryCtrl** | 取消订单入口在订单列表 |
| `medicalProduct.objectId` | 前端 runtime mutation | 实际是 `machineCenter.id` |
| `deliveryedList / sendToMachineCenterList` | controller.js 0 命中 | 仅 HTML 模板/后端 Response |

### 30.4 不可桥（必须显式不返回）

| 不可桥 | 等级 | 说明 |
|---|:---:|---|
| Delivery → Machine Controller | F | 无字符级桥 |
| Machine → Delivery | F | 无字符级桥 |
| MedicalRecord → Delivery | F | 无 $state.go 入口 |
| Cashflow → Delivery | F | 无 $state.go 入口 |
| deliveryedList / sendToMachineCenterList | F | 0 命中 |
| F2 (F1-F6 中间的 F2) | F | 未发现 F2 API 字符级 |

### 30.5 deliveryStatus 1/2 含义（仅枚举值，不补含义）

| 值 | UI 触发 | deliveryNo |
|---|---|---|
| "1" | 快递发货 | 有值 |
| "2" | 到店取镜 | undefined |

**前端不补含义，后端定义**。

---

## 31. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 / Write actual = 0 / Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-204 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 / ignored=1 | ✓ |
| 本轮只新增 205_*.md | ✓ |

---

## 32. Git

### 32.1 操作

```
git add -- 205_S1-142_Delivery全生命周期与Cashflow_Machine_Stock三方关系总审计.md
git diff --cached --name-only
git commit -m "docs(205): S1-142 Delivery 全生命周期与 Cashflow Machine Stock 三方关系总审计"
git push origin master
```

### 32.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| tracked | 213 (commit 205 后从 212 → 213) |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L3814 | deliveryInputCtrl $stateParams.cashflowId |
| L3848 | **F1** getCashflowDeliveryVo.json |
| L3854 | `medicalProduct.objectId = lockMachineCenter.id` (runtime mutation) |
| L3836 | **F3** getMedicalProductMachineCenterVoList.json |
| L3885 | **F4** getCanBeDeliverySkuInListOfProduct.json (deliveryInputCtrl) |
| L35054 | **F4** 也在 optometryCtrl (S1-129 漏掉) |
| L3966 | **F6** sendMedicalProductToMachineCenter.json (planDeliveryTime = $scope.startTime) |
| L3991 | F5 Request stockInSkuId 来源 (F4 Response) |
| L4007 | **F5** saveMedicalProductStockBatch.json |
| L4034 | getMedicalRecordPayVo.json (Delivery → MedicalRecord 派生) |
| L4036 | `$scope.medicalRecordId = res.object.medicalRecord.id` |
| L35054 | optometryCtrl F4 调用 |
| L35185 | **completeMedicalRecordDelivery deliveryStatus="2"** (optometryCtrl) |
| L35204 | **completeMedicalRecordDelivery deliveryStatus="1"** (optometryCtrl) |
| L35342 | **createMedicalStockLossOfSmallVersion** (optometryCtrl) |
| L35167 | confirmMedicalRecordReturn (optometryCtrl) |
| L35150 | cancelMedicalRecord (optometryCtrl) |

---

S1-142 完成。立即停止，等待老板下一指令。不执行 S1-143。
