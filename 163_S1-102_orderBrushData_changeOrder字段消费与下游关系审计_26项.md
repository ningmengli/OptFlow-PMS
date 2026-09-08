# S1-102 order.brushData → changeOrder 字段消费与下游关系审计

> **任务名**：S1-102｜order.brushData → $scope.order.object → modal.changeOrder 字段消费与下游关系审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）"报损"业务端到端链路
> **当前轮次**：S1-102（接 S1-101 完成）
> **本轮承诺**：2 个 Read API + 1 个 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| $scope.order (L34857) | ✅ | 含 isShow/object/brushData/show |
| order.brushData (L34860) | ✅ | 主入口 |
| order.show (L34871) | ✅ | 触发器 |
| $scope.modal (L35275) | ✅ | 含 show/shopInfo/changeOrder/affrim |
| modal.changeOrder (L35278) | ✅ | 字段消费入口 |
| modal.affrim (L35301) | ✅ | **S1-102 新发现：含 Read + Write** |
| 7 HTML | ❌（不可得）| UI 触发点 F |
| 2 个新 API 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "order.object = 订单对象"：**E**（仅命名）
- "medicalProduct = 数据库实体"：**E**
- "medicalProductDelivery = 配送记录"：**E**
- "machineCenterId = 加工中心主键"：**E**
- "medicalRecordId = 数据库主键"：**E**
- 字段名相似 → 同源字段：**D**（禁止升级）
- modal.affrim 的 modal.affrim 字段 = 数据库字段：**D**

---

## 3. $scope.order 完整定义

### 3.1 完整源码（A 级，L34857-L34880）

```javascript
$scope.order = {                                                                              // L34857
    isShow: false,                                                                            // L34858
    object: {},                                                                               // L34859
    brushData: function brushData(medicalRecordId) {                                          // L34860
        $scope.order.object = {};                                                             // L34861
        new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", {              // L34862
            medicalRecordId: medicalRecordId                                                    // L34863
        }).then(function (result) {
            if (result.status) {                                                                // L34865
                return Popup.notice(result.errmsg);
            }
            $scope.order.object = result.object;                                                 // L34868
        });
    },
    show: function show(bol, medicalRecordId) {                                                // L34871
        this.isShow = bol;                                                                       // L34872
        if (bol) {
            window.commonFn.openMaskFun();                                                        // L34874
            this.brushData(medicalRecordId);                                                       // L34875
        } else {
            window.commonFn.closeMaskFun();                                                       // L34877
        }
    }
};
```

### 3.2 完整属性/方法表（A 级）

| 名称 | 类型 | 初始值 | A-F |
|---|---|---|---|
| isShow | Boolean | false | A |
| object | Object | {} | A |
| brushData | function(medicalRecordId) | — | A |
| show | function(bol, medicalRecordId) | — | A |

---

## 4. order.brushData 完整审计

### 4.1 函数签名（A 级）

```javascript
brushData: function brushData(medicalRecordId) { }
```

| 维度 | 评估 | A-F |
|---|---|---|
| 形参 | `medicalRecordId` | A |
| 返回值 | 无（undefined） | A |
| 所属 | $scope.order 对象方法 | A |

### 4.2 完整行为（A 级，L34860-L34870）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L34861 | `$scope.order.object = {};`（整体重置为 {}） | A |
| 2 | L34862 | 调 Read `getMedicalRecordFlowVo.json` | A |
| 3 | L34863 | Request = `{ medicalRecordId: medicalRecordId }` | A |
| 4 | L34864 | `.then(function (result) { ... })` | A |
| 5 | L34865 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 6 | L34868 | `$scope.order.object = result.object`（整体对象引用替换） | A |
| 7 | L34869 | `});` | A |

### 4.3 Factory / Promise（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| Factory | 匿名 `new ObjectFactory()` | A |
| HTTP 方法 | saveOrQuery（ObjectFactory 模式） | A 引用 / F 实际 |
| .then | ✅ 1 个 | A |
| .catch | ❌ 0 处 | A |
| .finally | ❌ 0 处 | A |
| $timeout 包裹 | ❌ 0 处（与 querySingleOrder 不同） | A |

### 4.4 关键事实（A 级）
- brushData 内部**先重置** `$scope.order.object = {}` (L34861) 再发起 Read
- Read 成功 → **整体引用替换** `$scope.order.object = result.object` (L34868)
- ❌ 0 处字段级 merge / extend
- ❌ 0 处 oldItem 比较
- ❌ 0 处 .catch 保护

---

## 5. $scope.order.object 全部 Consumer（A 级）

### 5.1 全 controller.js 引用（3 处，已穷举）

| 行号 | 表达式 | 角色 | A-F |
|---|---|---|---|
| L34861 | `$scope.order.object = {};` | brushData 初始化（整体重置）| A |
| L34868 | `$scope.order.object = result.object;` | brushData 写 result.object（整体引用替换） | A |
| L35282 | `var _$scope$order$object$ = $scope.order.object.medicalProductVoList[index],` | modal.changeOrder 内字段级读 | A |

**A 级结论**：
- $scope.order.object 在 controller.js **仅 3 处**引用
- 写入 = 2 处（L34861 初始化 / L34868 整体替换）
- 字段级读取 = 1 处（L35282）
- ❌ 0 处 7 HTML 引用
- ❌ 0 处其它 controller 引用

### 5.2 严格表述（A 级）
- "$scope.order.object 仅 3 处引用"：**A**
- "字段级读取仅 1 处（modal.changeOrder）"：**A**
- "7 HTML 是否消费 order.object"：**F**（HTML 不可得）

---

## 6. modal.changeOrder 完整审计

### 6.1 完整源码（A 级，L35278-L35300）

```javascript
$scope.modal = {                                                                              // L35275
    show: false,                                                                              // L35276
    shopInfo: {},                                                                             // L35277
    changeOrder: function changeOrder(bol, index) {                                           // L35278
        this.show = bol;                                                                      // L35279
        if (bol) {
            new ObjectFactory().saveOrQuery("/admin/getAdminInfo.json").then(function (res) {  // L35281
                var _$scope$order$object$ = $scope.order.object.medicalProductVoList[index],  // L35282
                    product = _$scope$order$object$.product,                                  // L35283
                    medicalProduct = _$scope$order$object$.medicalProduct,                    // L35284
                    medicalProductDelivery = _$scope$order$object$.medicalProductDelivery;    // L35285

                $scope.modal.shopInfo = {                                                      // L35287
                    productName: product.productName,                                          // L35288
                    useCount: 1,                                                               // L35289
                    remark: "",                                                                 // L35290
                    lossAdminId: res.result.object.id,                                          // L35291
                    adminname: res.result.object.nickname,                                      // L35292
                    lossReasonId: null,                                                        // L35293
                    machineCenterId: medicalProductDelivery.machineCenterId,                  // L35294
                    medicalRecordId: medicalProduct.medicalRecordId,                          // L35295
                    medicalProductId: medicalProduct.id                                          // L35296
                };
            });
        }
    },
    // ...
};
```

### 6.2 函数签名（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 形参 1 (bol) | 显示/隐藏标志（true/false） | A |
| 形参 2 (index) | 数组索引 | A |
| 返回值 | 无 | A |

### 6.3 index 来源（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| modal.changeOrder(index) 调用方 | ❌ controller.js **0 处**显式 index 传入 | A |
| index 由谁传 | HTML ng-click 传入 → **F 边界** | F |
| index 用途 | `medicalProductVoList[index]` 访问 | A |

**A 级结论**：
- modal.changeOrder 的 **index 形参** 在 controller.js **0 处**被显式传入
- 仅在 modal.affrim success L35345 `$scope.modal.changeOrder(false)` 调用（不传 index）
- index 真实来源 = HTML ng-click（**F 边界**）

### 6.4 完整字段消费表（A 级）

| 行号 | 读取表达式 | 写入目标 | 字段值来源 | A-F |
|---|---|---|---|---|
| L35279 | `this.show = bol` | $scope.modal.show | bol 形参 | A |
| L35281 | `saveOrQuery("/admin/getAdminInfo.json")` (无参) | — | — | A |
| L35282 | `$scope.order.object.medicalProductVoList[index]` | 局部变量 | order.object 数组 index 位置 | A |
| L35283 | `.product` | 局部 `product` | medicalProductVoList[index] 元素 | A |
| L35284 | `.medicalProduct` | 局部 `medicalProduct` | medicalProductVoList[index] 元素 | A |
| L35285 | `.medicalProductDelivery` | 局部 `medicalProductDelivery` | medicalProductVoList[index] 元素 | A |
| L35287 | `$scope.modal.shopInfo = {...}` | $scope.modal.shopInfo 整体替换 | — | A |
| L35288 | `productName: product.productName` | $scope.modal.shopInfo.productName | `medicalProductVoList[index].product.productName` | A |
| L35289 | `useCount: 1` | $scope.modal.shopInfo.useCount | 字面量 1 | A |
| L35290 | `remark: ""` | $scope.modal.shopInfo.remark | 字面量空字符串 | A |
| L35291 | `lossAdminId: res.result.object.id` | $scope.modal.shopInfo.lossAdminId | getAdminInfo Response | A |
| L35292 | `adminname: res.result.object.nickname` | $scope.modal.shopInfo.adminname | getAdminInfo Response | A |
| L35293 | `lossReasonId: null` | $scope.modal.shopInfo.lossReasonId | 字面量 null | A |
| L35294 | `machineCenterId: medicalProductDelivery.machineCenterId` | $scope.modal.shopInfo.machineCenterId | `medicalProductVoList[index].medicalProductDelivery.machineCenterId` | A |
| L35295 | `medicalRecordId: medicalProduct.medicalRecordId` | $scope.modal.shopInfo.medicalRecordId | `medicalProductVoList[index].medicalProduct.medicalRecordId` | A |
| L35296 | `medicalProductId: medicalProduct.id` | $scope.modal.shopInfo.medicalProductId | `medicalProductVoList[index].medicalProduct.id` | A |

### 6.5 Read API 字符串（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| API | /admin/getAdminInfo.json (Read) | A |
| Request body | ❌ 无（saveOrQuery 无第二参数） | A |
| Factory | 匿名 new ObjectFactory() | A |
| 全局 Consumer 数 | ❌ 0 处 controller.js 其它调用 | A（仅 L35281） |

### 6.6 A 级结论
- modal.changeOrder 是一个**双 Read 入口**（getMedicalRecordFlowVo 间接经 brushData + getAdminInfo 直接）
- 6 个字段从 medicalProductVoList[index] 读取 → 写入 $scope.modal.shopInfo
- 3 个字段是字面量（useCount=1, remark="", lossReasonId=null）
- 2 个字段来自 getAdminInfo Response（lossAdminId, adminname）
- ❌ 0 处字段验证
- ❌ 0 处 modal 关闭逻辑（changeOrder(false) 仅在 modal.affrim success 调）

---

## 7. medicalProductVoList 来源与字段消费

### 7.1 medicalProductVoList 来源链（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868 (整体对象引用替换)
$scope.order.object
    ↓
$scope.order.object.medicalProductVoList  (modal.changeOrder L35282)
```

### 7.2 medicalProductVoList 访问全集（A 级，optometryCtrl 范围）

| 行号 | 表达式 | 操作 | A-F |
|---|---|---|---|
| L35282 | `$scope.order.object.medicalProductVoList[index]` | 索引访问 | A |
| 其它访问 | ❌ 0 处 | — | A |

**A 级结论**：
- $scope.order.object.medicalProductVoList 在 optometryCtrl **仅 1 处访问**（L35282）
- 仅按 index 访问（不读取 length / 不 forEach / 不 map）
- ❌ 0 处 length 检查
- ❌ 0 处 if (medicalProductVoList) 判空
- ❌ 0 处 forEach / map / filter
- ❌ 0 处 7 HTML 引用

### 7.3 medicalProductVoList 元素实际字段消费全集（A 级）

| 字段路径 | 行号 | 消费方式 | 写入目标 | A-F |
|---|---|---|---|---|
| `medicalProductVoList[index].product` | L35283 | 局部变量 `product` | （间接）$scope.modal.shopInfo.productName | A |
| `medicalProductVoList[index].product.productName` | L35288 | 字段读取 | $scope.modal.shopInfo.productName | A |
| `medicalProductVoList[index].medicalProduct` | L35284 | 局部变量 `medicalProduct` | （间接）3 字段 | A |
| `medicalProductVoList[index].medicalProduct.id` | L35296 | 字段读取 | $scope.modal.shopInfo.medicalProductId | A |
| `medicalProductVoList[index].medicalProduct.medicalRecordId` | L35295 | 字段读取 | $scope.modal.shopInfo.medicalRecordId | A |
| `medicalProductVoList[index].medicalProductDelivery` | L35285 | 局部变量 `medicalProductDelivery` | （间接）1 字段 | A |
| `medicalProductVoList[index].medicalProductDelivery.machineCenterId` | L35294 | 字段读取 | $scope.modal.shopInfo.machineCenterId | A |
| 其它字段 | ❌ 0 处 | — | — | F |

**A 级结论**：
- Controller 视角 medicalProductVoList 元素可见字段 = **6 个**（product.productName / medicalProduct.id / medicalProduct.medicalRecordId / medicalProductDelivery.machineCenterId + 3 个对象引用）
- ❌ 0 处其它字段访问
- 真实字段集合 = **F**（无样本可证）

---

## 8. 三个关键对象引用

### 8.1 product（A 级，L35283）

```javascript
var _$scope$order$object$ = $scope.order.object.medicalProductVoList[index],
    product = _$scope$order$object$.product,
```

| 维度 | 评估 | A-F |
|---|---|---|
| 引用对象 | medicalProductVoList[index].product | A |
| 字段读取 | .productName (L35288) | A |
| 字段写入 | ❌ 0 处 | A |
| 字段其它消费 | ❌ 0 处（仅 productName） | A |
| 用途 | 仅显示用（HTML 不可得） | A 引用 / F 显示 |
| 是否进入 Request | ❌ 0 处 | A |
| 是否进入 Write | ❌ 0 处 | A |

### 8.2 medicalProduct（A 级，L35284）

```javascript
medicalProduct = _$scope$order$object$.medicalProduct,
```

| 维度 | 评估 | A-F |
|---|---|---|
| 引用对象 | medicalProductVoList[index].medicalProduct | A |
| 字段读取 | .id (L35296) / .medicalRecordId (L35295) | A |
| 字段写入 | ❌ 0 处 | A |
| 字段其它消费 | ❌ 0 处 | A |
| 用途 | 2 字段提供 | A |
| **是否进入 F4 medicalProductIdArray** | ❌ **0 处**（无代码连接 modal.changeOrder 内部字段到 F4） | A |
| **是否进入 F3 Request** | ❌ **0 处** | A |
| **是否进入 F5/F6 Request** | ❌ **0 处** | A |
| 是否进入 modal.affrim Request | ✅ **是**（经 $scope.modal.shopInfo.medicalProductId → L35320 / L35336） | A |

### 8.3 medicalProductDelivery（A 级，L35285）

```javascript
medicalProductDelivery = _$scope$order$object$.medicalProductDelivery,
```

| 维度 | 评估 | A-F |
|---|---|---|
| 引用对象 | medicalProductVoList[index].medicalProductDelivery | A |
| 字段读取 | .machineCenterId (L35294) | A |
| 字段写入 | ❌ 0 处 | A |
| 字段其它消费 | ❌ 0 处 | A |
| 用途 | 1 字段提供 | A |
| **是否进入 F3 Request** | ❌ **0 处直接代码连接** | A |
| **是否进入 F6 Request** | ❌ **0 处直接代码连接** | A |
| 是否进入 modal.affrim Request | ✅ **是**（经 $scope.modal.shopInfo.machineCenterId → L35336） | A |
| **是否与 S1-94 lockMachineCenter.id 同源** | **❌ 否**（无直接代码连接） | A |

### 8.4 严格表述（A 级）
- "modal.changeOrder 内部 6 字段"：**A**（product.productName / medicalProduct.id / medicalProduct.medicalRecordId / medicalProductDelivery.machineCenterId + 3 局部对象引用）
- "3 字段进入 modal.affrim Request"：**A**（medicalRecordId / machineCenterId / medicalProductId）
- "medicalProductDelivery.machineCenterId 与 F3 Request.machineCenterId 同源"：**❌ 否**（无代码连接，禁止合并）

---

## 9. 关键字段完整来源链

### 9.1 productName（A 级）

```
getMedicalRecordFlowVo.result.object  [F 边界: 完整字段未知]
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34883
product (= medicalProductVoList[index].product)
    ↓ L34888
product.productName
    ↓ L34887
$scope.modal.shopInfo.productName
    ↓ [HTML 显示]  F 边界
```

### 9.2 medicalProduct.id（A 级）

```
getMedicalRecordFlowVo.result.object  [F 边界]
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34884
medicalProduct (= medicalProductVoList[index].medicalProduct)
    ↓ L34896
medicalProduct.id
    ↓ L34887
$scope.modal.shopInfo.medicalProductId
    ↓ L35309
modal.affrim 局部 medicalProductId
    ↓ L35320
selectMedicalProductStockList.json Request.medicalProductId
    ↓ L35336
createMedicalStockLossOfSmallVersion.json Request.medicalProductId
```

### 9.3 medicalProduct.medicalRecordId（A 级）

```
getMedicalRecordFlowVo.result.object  [F 边界]
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34884
medicalProduct
    ↓ L34895
medicalProduct.medicalRecordId
    ↓ L34887
$scope.modal.shopInfo.medicalRecordId
    ↓ L35307
modal.affrim 局部 medicalRecordId
    ↓ L35335
createMedicalStockLossOfSmallVersion.json Request.medicalRecordId
```

**A 级新发现**：
- modal.affrim 使用的 medicalRecordId **不是** `medicalRecord.id`，而是 `medicalProduct.medicalRecordId`
- 这是**完全不同**的字段路径
- ❌ 0 处 controller.js 内有 `medicalProduct.medicalRecordId == medicalRecord.id` 比较

### 9.4 medicalProductDelivery.machineCenterId（A 级）

```
getMedicalRecordFlowVo.result.object  [F 边界]
    ↓ L34868
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L34885
medicalProductDelivery (= medicalProductVoList[index].medicalProductDelivery)
    ↓ L34894
medicalProductDelivery.machineCenterId
    ↓ L34887
$scope.modal.shopInfo.machineCenterId
    ↓ L35308
modal.affrim 局部 machineCenterId
    ↓ L35336
createMedicalStockLossOfSmallVersion.json Request.machineCenterId
```

### 9.5 严格表述（A 级）
- "modal.changeOrder 6 字段 → modal.shopInfo → modal.affrim 局部 → Write Request"：**A**（完整字段链）
- "modal.affrim 的 medicalRecordId = medicalProduct.medicalRecordId"：**A**
- "modal.affrim 的 medicalRecordId = medicalRecord.id"：**D**（无直接证据，禁止升级 A）
- "modal.affrim 的 machineCenterId = lockMachineCenter.id（S1-94 链路）"：**D**（无直接证据，禁止升级 A）

---

## 10. order.object mutation 检查（A 级）

### 10.1 optometryCtrl 范围 order.object.xxx 写入检查

| 操作 | 表达式 | 行号 | A-F |
|---|---|---|---|
| `$scope.order.object = {}` | 整体重置 | L34861 | A |
| `$scope.order.object = result.object` | 整体替换 | L34868 | A |
| `$scope.order.object.xxx = ...` | ❌ 0 处 | — | A |
| `$scope.order.object.xxx.push(...)` | ❌ 0 处 | — | A |
| `delete $scope.order.object.xxx` | ❌ 0 处 | — | A |

### 10.2 A 级结论
- **$scope.order.object 仅被整体重置和整体替换**
- ❌ **0 处字段级写入**
- ❌ 0 处 push / delete
- ❌ 0 处属性 mutation
- 严格表述：**当前 Controller 未观察到对 $scope.order.object 原对象的字段级直接写入**

---

## 11. modal.affrim 完整审计（**S1-102 关键新发现**）

### 11.1 完整源码（A 级，L35301-L35353）

```javascript
affrim: function affrim() {                                                                  // L35301
    var _$scope$modal$shopInf = $scope.modal.shopInfo,                                       // L35302
        lossAdminId = _$scope$modal$shopInf.lossAdminId,                                     // L35303
        lossReasonId = _$scope$modal$shopInf.lossReasonId,                                  // L35304
        useCount = _$scope$modal$shopInf.useCount,                                           // L35305
        remark = _$scope$modal$shopInf.remark,                                               // L35306
        medicalRecordId = _$scope$modal$shopInf.medicalRecordId,                            // L35307
        machineCenterId = _$scope$modal$shopInf.machineCenterId,                             // L35308
        medicalProductId = _$scope$modal$shopInf.medicalProductId;                          // L35309

    if (!lossAdminId) {                                                                       // L35311
        Popup.notice("请选择报损责任人");
        return false;
    }
    if (!lossReasonId) {                                                                      // L35315
        Popup.notice("请选择报损原因");
        return false;
    }
    new ObjectFactory().saveOrQuery("/admin/selectMedicalProductStockList.json", {          // L35319 (Read)
        medicalProductId: medicalProductId                                                     // L35320
    }).then(function (res) {
        if (res.status) {                                                                      // L35322
            return Popup.notice(res.errmsg);
        }
        var medicalStockLossSkuListJson = [];                                                  // L35325
        res.object.forEach(function (medical) {                                                // L35326
            medicalStockLossSkuListJson.push({                                                  // L35327
                medicalProductStockId: medical.id,                                              // L35328
                lossCount: useCount,                                                            // L35329
                lossReasonId: lossReasonId,                                                    // L35330
                remark: remark                                                                  // L35331
            });
        });
        var object = {                                                                          // L35334
            medicalRecordId: medicalRecordId,                                                   // L35335
            machineCenterId: machineCenterId,                                                   // L35336
            lossAdminId: lossAdminId,                                                           // L35337
            medicalStockLossSkuListJson: JSON.stringify(medicalStockLossSkuListJson)          // L35338
        };
        new ObjectFactory().saveOrQuery("/admin/createMedicalStockLossOfSmallVersion.json", object).then(function (res) {  // L35342 (Write)
            if (res.status == 0) {
                Popup.notice("报损成功");
                $scope.modal.changeOrder(false);                                                // L35345
                $scope.order.brushData(medicalRecordId);                                        // L35346
            } else {
                Popup.notice(res.errmsg);
            }
        });
    });
    return;                                                                                    // L35352
}
```

### 11.2 字段消费全集（A 级）

#### 11.2.1 $scope.modal.shopInfo 读取字段（A 级）

| 字段 | 行号 | 用途 | A-F |
|---|---|---|---|
| lossAdminId | L35303 + L35311 + L35337 | 校验 + Write Request | A |
| lossReasonId | L35304 + L35315 + L35330 | 校验 + 每个 SKU 元素 | A |
| useCount | L35305 + L35329 | 每个 SKU 元素 | A |
| remark | L35306 + L35331 | 每个 SKU 元素 | A |
| medicalRecordId | L35307 + L35335 + L35346 | Write Request + 重新 brushData | A |
| machineCenterId | L35308 + L35336 | Write Request | A |
| medicalProductId | L35309 + L35320 | Read Request | A |

#### 11.2.2 Read API 响应字段消费（A 级）

| 字段路径 | 行号 | 消费方式 | A-F |
|---|---|---|---|
| `res.status` | L35322 | 错误判断 | A |
| `res.errmsg` | L35323 | Popup 错误 | A |
| `res.object` | L35326 | 整体 forEach | A |
| `res.object[i].id` | L35328 | 字段读取（每个元素） | A |
| 其它字段 | ❌ 0 处 | — | F |

#### 11.2.3 Write API Request 完整字段（A 级）

| 字段 | 来源表达式 | 行号 | A-F |
|---|---|---|---|
| `medicalRecordId` | modal 局部 | L35335 | A |
| `machineCenterId` | modal 局部 | L35336 | A |
| `lossAdminId` | modal 局部 | L35337 | A |
| `medicalStockLossSkuListJson` | JSON.stringify(medicalStockLossSkuListJson) | L35338 | A |

**medicalStockLossSkuListJson 元素结构**：
```json
{
  "medicalProductStockId": <res.object[i].id>,
  "lossCount": <useCount>,
  "lossReasonId": <lossReasonId>,
  "remark": <remark>
}
```

#### 11.2.4 success 行为（A 级）

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (res.status == 0)` | A |
| 2 | `Popup.notice("报损成功")` | A |
| 3 | `$scope.modal.changeOrder(false)` — 关闭 modal | A |
| 4 | `$scope.order.brushData(medicalRecordId)` — 重新刷 data | A |

**A 级关键发现**：
- Write success 后**重新调 brushData(medicalRecordId)**（L35346）— 刷新 order.object
- medicalRecordId 传入 brushData = `$scope.modal.shopInfo.medicalRecordId` = `medicalProduct.medicalRecordId`（**不是** medicalRecord.id）

### 11.3 校验（A 级）

| 校验 | 行号 | 行为 | A-F |
|---|---|---|---|
| `if (!lossAdminId)` | L35311 | Popup + return false | A |
| `if (!lossReasonId)` | L35315 | Popup + return false | A |
| `if (res.status == 0)` | L35343 | success 分支 | A |
| 其它字段校验 | ❌ 0 处 | — | A |

### 11.4 A 级结论
- modal.affrim 是 "报损" 业务的**完整端到端执行函数**
- 内部有 **1 Read + 1 Write**（S1-99/100/101 都未审计到的 Write 路径）
- 校验仅 2 处（lossAdminId / lossReasonId），其它字段**不校验**
- Write success 后**重新刷 brushData** 形成闭环

---

## 12. "报损" 业务完整端到端链路（A 级 + F 边界）

### 12.1 完整链路图

```
[HTML ng-click] (F 边界)
    ↓
clickBtn "报损" (L35177-L35179)
    ↓ $scope.order.show(true, item.medicalRecord.id)
order.show (L34871)
    ↓
this.isShow = bol (L34872)
window.commonFn.openMaskFun() (F 边界 L34874)
this.brushData(medicalRecordId) (L34875)
    ↓
$scope.order.object = {} (L34861)
Read /admin/getMedicalRecordFlowVo.json (L34862)
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868
$scope.order.object = result.object (整体替换)
    ↓
[HTML 渲染 order.object 列表]  (F 边界)
    ↓
[用户点击 "换商品" 按钮] (F 边界: HTML ng-click)
    ↓
modal.changeOrder(true, index) (L35278)
    ↓
this.show = bol (L35279)
Read /admin/getAdminInfo.json (L35281)
    ↓ [F 边界]
res.result.object
    ↓ L35282-L35296
6 字段读取 from $scope.order.object.medicalProductVoList[index]
    ↓
$scope.modal.shopInfo = { 9 字段 } (L35287)
    ↓
[HTML 渲染 modal.shopInfo]  (F 边界)
    ↓
[用户选择 lossAdmin / lossReason + 点击确认]  (F 边界)
    ↓
modal.affrim() (L35301)
    ↓
校验 lossAdminId / lossReasonId (L35311/L35315)
    ↓
Read /admin/selectMedicalProductStockList.json { medicalProductId } (L35319)
    ↓ [F 边界]
res.object
    ↓ L35326
forEach → medicalStockLossSkuListJson
    ↓ L35334
object = { medicalRecordId, machineCenterId, lossAdminId, medicalStockLossSkuListJson }
    ↓
Write /admin/createMedicalStockLossOfSmallVersion.json (L35342)
    ↓ [F 边界: 后端处理]
res
    ↓ if (res.status == 0)
Popup.notice("报损成功") (L35344)
$scope.modal.changeOrder(false) (L35345) — 关闭 modal
$scope.order.brushData(medicalRecordId) (L35346) — 重新刷 data
```

### 12.2 API 总数（A 级）

| 类型 | API 字符串 | 行号 | 角色 |
|---|---|---|---|
| Read | /admin/getMedicalRecordFlowVo.json | L34862 | brushData |
| Read | /admin/getAdminInfo.json | L35281 | modal.changeOrder |
| Read | /admin/selectMedicalProductStockList.json | L35319 | modal.affrim |
| **Write** | **/admin/createMedicalStockLossOfSmallVersion.json** | **L35342** | **modal.affrim (新发现)** |

**A 级新发现**："报损"业务链路包含 **3 Read + 1 Write**，Write 是 **createMedicalStockLossOfSmallVersion.json**（与本轮 S1-99/S1-100/S1-101 审计的 3 个 Write API **完全不同**）。

---

## 13. 与 F3/F4/F5/F6 的直接连接检查

### 13.1 medicalProduct.id 与 F4 medicalProductIdArray（A 级）

| 检查 | 评估 | A-F |
|---|---|---|
| modal.changeOrder 内 medicalProduct.id → F4 Request.medicalProductIdArray | ❌ **0 处直接代码连接** | A |
| modal.affrim 内 medicalProductId → F4 Request | ❌ **0 处**（F4 Request 字段是 medicalProductIdArray 不是 medicalProductId） | A |
| F4 (getCanBeDeliverySkuInListOfProduct.json) 调点 | 仅 optometryCtrl concatMedicalProductStock L35054 | A |

**A 级结论**：
- modal.changeOrder / modal.affrim 的 medicalProduct.id **0 处直接进入 F4 Request**
- 完整路径是：medicalProduct.id → $scope.modal.shopInfo.medicalProductId → modal.affrim 局部 → **selectMedicalProductStockList** Request
- 与 F4 **完全不同路径**（F4 走 concatMedicalProductStock → medicalProductIdArray → F4）

### 13.2 medicalProductDelivery.machineCenterId 与 F3/F6（A 级）

| 检查 | 评估 | A-F |
|---|---|---|
| modal.changeOrder 内 machineCenterId → F3 Request.machineCenterId | ❌ **0 处直接代码连接** | A |
| modal.changeOrder 内 machineCenterId → F6 Request.machineCenterId | ❌ **0 处直接代码连接** | A |
| F3 (getMedicalProductMachineCenterVoList.json) 调点 | 仅 deliveryInputCtrl L3836 | A |
| F6 (sendMedicalProductToMachineCenter.json) 调点 | 仅 deliveryInputCtrl L3966 | A |
| S1-94 lockMachineCenter.id → objectId → F3 Request.machineCenterId | deliveryInputCtrl 内部 | A |

**A 级结论**：
- modal.changeOrder / modal.affrim 的 machineCenterId **0 处直接进入 F3 / F6 Request**
- 完整路径是：medicalProductDelivery.machineCenterId → $scope.modal.shopInfo.machineCenterId → modal.affrim 局部 → **createMedicalStockLossOfSmallVersion** Request
- 与 S1-94 的 lockMachineCenter.id 链路**完全不同**（不同 controller / 不同字段名 / 不同 API）

### 13.3 medicalProduct.medicalRecordId 与 deliveryInputCtrl F1（A 级）

| 检查 | 评估 | A-F |
|---|---|---|
| modal.changeOrder 内 medicalProduct.medicalRecordId → deliveryInputCtrl F1 cashflowId | ❌ **0 处直接代码连接** | A |
| F1 (getCashflowDeliveryVo.json) 调点 | 仅 deliveryInputCtrl L3848 | A |
| medicalProduct.medicalRecordId 与 F1 waitingDeliveryList[i].medicalProduct.medicalRecordId 是否同源 | **❌ 不可证**（无任何 controller 间直接代码连接） | A（无连接） / F（值层） |

**A 级结论**：
- modal.changeOrder / modal.affrim 的 medicalProduct.medicalRecordId **0 处直接进入 F1/F3/F4/F5/F6 Request**
- 与 deliveryInputCtrl 链路**完全独立**

### 13.4 严格表述（A 级 vs E/F）
- "modal.changeOrder 6 字段与 F3/F4/F5/F6 直接连接"：**❌ 0 处**（A 级）
- "modal.affrim Write 与 3 个 Write 同源"：**❌ 否**（createMedicalStockLossOfSmallVersion.json 完全不同 API）
- "modal.affrim Write 与 3 Write 同一业务流"：**E**（业务推断，禁止升级 A）

---

## 14. 与 selectOrderListFactory.items 连接检查

### 14.1 optometryCtrl 范围 $scope.order.object 与 $scope.selectOrderListFactory.items 关系（A 级）

| 检查 | 评估 | A-F |
|---|---|---|
| $scope.order.object = $scope.selectOrderListFactory.items[index] | ❌ 0 处 | A |
| $scope.order.object 直接读自 selectOrderListFactory.items | ❌ 0 处 | A |
| $scope.order.object 写回 selectOrderListFactory.items | ❌ 0 处 | A |
| $scope.order.object 与 selectOrderListFactory.items[index] 同对象引用 | ❌ **0 处** | A |

### 14.2 $scope.order.object 真实来源（A 级）

```
brushData(medicalRecordId)
    ↓
$scope.order.object = result.object  (L34868)
```

**$scope.order.object 来源 = 单独 Read getMedicalRecordFlowVo.json**（与 selectOrderListFactory.items **完全独立**）

### 14.3 A 级结论
- $scope.order.object 与 $scope.selectOrderListFactory.items **完全独立**
- 两者**不共享**数据来源（前者 brushData / 后者 ListFactory + querySingleOrder）
- 两者**不共享**对象引用
- 严格表述：**当前 Controller 未观察到 $scope.order.object 与 $scope.selectOrderListFactory.items 之间的直接赋值或对象引用复用**

### 14.4 medicalRecordId 是否同源（A 级）

| 表达式 | 来源 |
|---|---|
| `$scope.order.object` 中的 medicalRecordId | `medicalProduct.medicalRecordId` (modal.changeOrder L35295) |
| `$scope.selectOrderListFactory.items[index]` 中的 medicalRecordId | `medicalRecord.id` (L34884 querySingleOrder) |
| **是否同源字段** | **❌ 否**（不同字段路径） |

**A 级结论**：
- $scope.order.object 内的 medicalRecordId 字段路径 = `medicalProduct.medicalRecordId`
- $scope.selectOrderListFactory.items 内的 medicalRecordId 字段路径 = `medicalRecord.id`
- **两个 medicalRecordId 是不同字段**（即使最终可能是同一业务对象 ID）
- 严格表述：**两个 medicalRecordId 表达式不同源**（A 级），**值是否相等 = F**（无后端可证）

---

## 15. HTML 边界（F）

| 触发点 | 是否可得 | A-F |
|---|---|---|
| clickBtn "报损" 按钮 ng-click | F | F |
| modal.changeOrder(index) index 来源 | F | F |
| modal.affrim 确认按钮 ng-click | F | F |
| lossAdmin 选择 UI | F | F |
| lossReason 选择 UI | F | F |
| modal 关闭按钮 | F | F |
| 7 HTML 是否含 optometry 模板 | ❌ 0 处 | F |

**A 级结论**：
- optometryCtrl HTML **资源范围内不可得**
- 全部 UI 触发点保持 F
- Controller 内部已观察的函数调用 + 字段消费 全部按 A 处理

---

## 16. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | order.brushData 定义 | L34860-L34870 | A | L1 | |
| 02 | order.brushData 调用 | order.show L34875 / modal.affrim L35346 | A | L1 | |
| 03 | API | /admin/getMedicalRecordFlowVo.json | A | L1 | |
| 04 | Request | { medicalRecordId } | A | L1 | |
| 05 | Factory | 匿名 new ObjectFactory() | A | L1 | |
| 06 | result.status | L34865 | A | L1 | |
| 07 | result.object | L34868 | A | L1 | |
| 08 | order.object 写入 | L34861/L34868 | A | L1 | |
| 09 | order.object 全局 Consumer | 3 处（L34861/L34868/L35282） | A | L1 | |
| 10 | changeOrder 定位 | L35278-L35300 | A | L1 | |
| 11 | changeOrder 参数 | (bol, index) | A | L1 | |
| 12 | index 来源 | HTML ng-click（F 边界） | F | L1 | |
| 13 | medicalProductVoList | 1 处访问 L35282 | A | L1 | |
| 14 | medicalProductVoList index | 直接 [index] | A | L1 | |
| 15 | product | 局部 L35283 | A | L1 | |
| 16 | product.productName | L35288 | A | L1 | |
| 17 | medicalProduct | 局部 L35284 | A | L1 | |
| 18 | medicalProduct.id | L35296 | A | L1 | |
| 19 | medicalProduct.medicalRecordId | L35295 | A | L1 | |
| 20 | medicalProductDelivery | 局部 L35285 | A | L1 | |
| 21 | medicalProductDelivery.machineCenterId | L35294 | A | L1 | |
| 22 | order.object mutation | ❌ 0 处 | A | L1 | |
| 23 | changeOrder API 调用 | getAdminInfo.json (L35281) | A | L1 | |
| 24 | changeOrder 是否进入 Write | ❌ 0 处 | A | L1 | |
| 25 | 与 F3/F4/F5/F6 直接连接 | ❌ 0 处 | A | L1 | |
| 26 | 最小字段消费链 | brushData → order.object → changeOrder → shopInfo → affrim → Read+Write | A | L1 | |

**统计**：
- **A：25 项**
- **F：1 项**（#12 index 来源 HTML 不可得）
- **D / C / B / E：0**
- **E/F 升 A：0**

---

## 17. L1/L2/L3

### L1（源码事实，可证）

- order.brushData / order.show / modal.changeOrder / modal.affrim 完整定义（A）
- 4 个 API 字符串（A）
- 6 字段级读取路径（A）
- 3 Read + 1 Write 完整链路（A）
- modal.shopInfo 9 字段值（A）
- order.object 0 处 mutation（A）
- 与 F3/F4/F5/F6 0 处直接连接（A）
- 与 selectOrderListFactory 0 处直接连接（A）

### L2（业务解释，未证）

- "order.object = 订单对象"：**E**（仅命名）
- "medicalProduct = 数据库实体"：**E**
- "medicalProductDelivery = 配送记录"：**E**
- "machineCenterId = 加工中心主键"：**E**
- "medicalRecordId = 数据库主键"：**E**
- "lossAdminId = 报损责任人"：**E**（仅命名）
- "medicalProduct.medicalRecordId = medicalRecord.id"：**E**（业务推断，未证）
- "modal.affrim Write 与 3 Write 同一业务流"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 4 个 API 后端实现）

---

## 18. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 4 个 API 后端处理 | 无后端代码 | F |
| getMedicalRecordFlowVo Response 完整 schema | 无样本 | F |
| getAdminInfo Response 完整 schema | 无样本 | F |
| selectMedicalProductStockList Response 完整 schema | 无样本 | F |
| createMedicalStockLossOfSmallVersion 真实 Response | 无样本 | F |
| modal.changeOrder(bol, index) index 来源 | HTML 不可得 | F |
| 7 HTML UI 触发 | 不可得 | F |
| window.commonFn.openMaskFun / closeMaskFun 实现 | 全局函数 | F |
| medicalProduct.medicalRecordId 值是否 = medicalRecord.id | 无后端 | F |
| medicalProductDelivery.machineCenterId 与 lockMachineCenter.id 关系 | 无后端 | F |

---

## 19. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 3 Read + 1 Write 全部仅静态审计 |
| 3 个本轮 0 触发 Write 实际执行 = 0 | ✅ | createMedicalStockLossOfSmallVersion.json 仅源码审计 |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 163 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 163_*.md |
| 文件编号连续 | ✅ | 162 已被 S1-101 占用，本轮使用 163 |

---

## 20. 最终结论

### 20.1 最小字段消费链（A 级）

```
getMedicalRecordFlowVo.json Response
    ↓ [F 边界: HTTP + 后端]
result.object
    ↓ L34868 (整体引用替换)
$scope.order.object
    ↓ L34882
$scope.order.object.medicalProductVoList[index]
    ↓ L35283/L35284/L35285
3 局部对象引用: product / medicalProduct / medicalProductDelivery
    ↓ L35288/L35295/L35296
3 字段直接读取: product.productName / medicalProduct.medicalRecordId / medicalProduct.id
    ↓ L35291/L35292 (来自 getAdminInfo)
2 字段直接读取: res.result.object.id / res.result.object.nickname
    ↓ L35287 (整体对象引用替换)
$scope.modal.shopInfo
    ↓ L35307/L35308/L35309
modal.affrim 3 字段读取: medicalRecordId / machineCenterId / medicalProductId
    ↓ L35311/L35315
2 校验: lossAdminId / lossReasonId
    ↓ L35319 (Read: selectMedicalProductStockList.json)
    ↓ L35326
res.object.forEach → medicalStockLossSkuListJson[]
    ↓ L35334
object = { medicalRecordId, machineCenterId, lossAdminId, medicalStockLossSkuListJson }
    ↓ L35342 (Write: createMedicalStockLossOfSmallVersion.json)
    ↓ if (res.status == 0) success
Popup.notice("报损成功")
$scope.modal.changeOrder(false) — 关闭 modal
$scope.order.brushData(medicalRecordId) — 重新刷 data
```

### 20.2 关键事实（A 级）

1. **"报损"业务 = 3 Read + 1 Write 完整端到端链路**
2. **6 字段从 $scope.order.object.medicalProductVoList[index] 读取**（product.productName / medicalProduct.id / medicalProduct.medicalRecordId / medicalProductDelivery.machineCenterId + 3 局部引用）
3. **$scope.modal.shopInfo = 9 字段整体对象引用替换**（3 来自 order.object + 2 来自 getAdminInfo + 3 字面量 + 1 null）
4. **modal.affrim Write 字段 = { medicalRecordId, machineCenterId, lossAdminId, medicalStockLossSkuListJson }**
5. **medicalStockLossSkuListJson 每元素 = { medicalProductStockId, lossCount, lossReasonId, remark }**
6. **0 处字段级 mutation**（order.object / modal.shopInfo 都仅整体引用替换）
7. **0 处与 F3/F4/F5/F6 直接代码连接**
8. **0 处与 selectOrderListFactory.items 直接代码连接**
9. **modal.affrim success 后调 brushData(medicalRecordId) 形成闭环**（medicalRecordId 来自 medicalProduct.medicalRecordId）
10. **2 个新 API 是 S1-99/S1-100/S1-101 都未审计到的**（selectMedicalProductStockList.json + createMedicalStockLossOfSmallVersion.json）

### 20.3 S1-102 关键新发现

1. **modal.affrim 是新发现的 Write 路径**（createMedicalStockLossOfSmallVersion.json）— 与 S1-99/100/101 的 3 Write 完全不同
2. **"报损"业务完整 3 Read + 1 Write 端到端链路**已闭合
3. **$scope.modal.shopInfo.medicalRecordId 字段路径 = medicalProduct.medicalRecordId**（不是 medicalRecord.id）— 与 selectOrderListFactory.items 的 medicalRecord.id 字段路径**不同**
4. **$scope.modal.shopInfo.medicalProductId 字段路径 = medicalProduct.id**（不进入 F4 medicalProductIdArray）
5. **$scope.modal.shopInfo.machineCenterId 字段路径 = medicalProductDelivery.machineCenterId**（不进入 F3 Request.machineCenterId）
6. **modal.affrim success 后调 brushData(medicalRecordId) 重新刷 data**（形成闭环）

### 20.4 不可在本轮升级为 A 的项

- 4 个 API 后端处理（F）
- Response 完整 schema（F）
- index 来源（F，HTML 不可得）
- medicalProduct.medicalRecordId = medicalRecord.id 值层（F）
- medicalProductDelivery.machineCenterId = lockMachineCenter.id 值层（F）
- 业务语义（E）
- optometryCtrl HTML 模板（F）
- window.commonFn 实现（F）

---

**审计结束**。
