# S1-98 optometryCtrl F4 → 3 Write Request 字段级闭合审计

> **任务名**：S1-98｜optometryCtrl F4 Result → 3 个 Write API Request 字段级闭合审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）F4 → medicalProductStockBatctPoListJson → 3 Write 全链路
> **当前轮次**：S1-98（接 S1-97 完成）
> **本轮承诺**：3 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| concatMedicalProductStock（L35048-L35082） | ✅ | F4 result 消费函数 |
| choseFactoryMethod（L35083-L35125） | ✅ | setMedicalRecordProcessMode caller |
| clickBtn "到店取镜"（L35180-L35198） | ✅ | completeMedicalRecordDelivery "2" caller |
| clickBtn "快递发货"（L35199-L35217） | ✅ | completeMedicalRecordDelivery "1" caller |
| $scope.hint / $scope.express（L35010-L35046） | ✅ | 弹窗工具 |
| querySingleOrder / queryUndisposed（L34841 / L34883） | ✅ | success 后 Read |
| 3 Write 后端处理 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "completeMedicalRecordDelivery 是完成发货/取镜接口"：**E**（未证，仅 API 名）
- "deliveryStatus='1' 是快递发货"：**E**（未证，仅是字面量 + 上下文）
- "deliveryStatus='2' 是到店取镜"：**E**（同上）
- "setMedicalRecordProcessMode 是选加工方式"：**E**
- "toBeProcess 0=不加工 1=加工"：**仅 L35101 源码注释**（A），但**禁止升级**为业务规则
- "deliveryNo 来自用户输入"：**A**（弹窗输入框，但**禁止升级**为"用户可手动改单号"）

---

## 3. concatMedicalProductStock() 完整函数

### 3.1 函数签名（A 级，L35048-L35082）

```javascript
$scope.concatMedicalProductStock = function (item) {
    return new Promise(function (resolve) {
        // L35050-L35053: 构造 Request.medicalProductIdArray
        var medicalProductIdArray = [];
        item.medicalProductVoList.forEach(function (medical) {
            medicalProductIdArray.push(medical.medicalProduct.id);
        });

        // L35054-L35056: F4 调用
        new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", {
            medicalProductIdArray: medicalProductIdArray
        }).then(function (result) {
            // L35057-L35060: result.status 检查
            if (result.status) {
                Popup.notice(result.errmsg);
                return resolve(false);
            }

            // L35061-L35073: 构造 medicalProductStockBatctPoListJson
            var medicalProductStockBatctPoListJson = [];
            result.result.list.forEach(function (medical) {
                var medicalProductStocks = medical.deliveryStockInSkuVoList.map(function (delivery) {
                    return {
                        stockInSkuId: delivery.stockInSku.id,
                        deliveryCount: delivery.deliveryCount
                    };
                });
                medicalProductStockBatctPoListJson.push({
                    medicalProductId: medical.medicalProduct.id,
                    medicalProductStocks: medicalProductStocks
                });
            });

            // L35074-L35077: 长度判空
            if (!medicalProductStockBatctPoListJson.length) {
                Popup.notice("未找到商品信息！");
                return resolve(false);
            }

            // L35078: 序列化
            medicalProductStockBatctPoListJson = JSON.stringify(medicalProductStockBatctPoListJson);

            // L35079: 传出
            return resolve(medicalProductStockBatctPoListJson);
        });
    });
};
```

### 3.2 函数节点表（A 级）

| 行号 | 节点 | 操作 | 输入 | 输出 |
|---|---|---|---|---|
| L35048 | 函数定义 | `$scope.concatMedicalProductStock = function (item)` | item.medicalProductVoList | — |
| L35050 | 数组初始化 | `var medicalProductIdArray = []` | — | 空数组 |
| L35051 | 遍历 item | `item.medicalProductVoList.forEach(...)` | item.medicalProductVoList | — |
| L35052 | push id | `medicalProductIdArray.push(medical.medicalProduct.id)` | medical.medicalProduct.id | 累积数组 |
| L35054 | F4 调用 | `new ObjectFactory().saveOrQuery(getCanBeDeliverySkuInListOfProduct.json, { medicalProductIdArray })` | medicalProductIdArray | F4 Promise |
| L35057 | status 检查 | `if (result.status)` | result.status | resolve(false) |
| L35061 | 数组初始化 | `var medicalProductStockBatctPoListJson = []` | — | 空数组 |
| L35062 | 遍历 F4 result | `result.result.list.forEach(...)` | F4 result.list | — |
| L35063 | 二级 map | `medical.deliveryStockInSkuVoList.map(...)` | deliveryStockInSkuVoList[] | medicalProductStocks 数组 |
| L35064-L35067 | 二级元素构造 | `{ stockInSkuId: delivery.stockInSku.id, deliveryCount: delivery.deliveryCount }` | delivery.stockInSku.id, delivery.deliveryCount | 新对象 |
| L35069-L35072 | push 元素 | `medicalProductStockBatctPoListJson.push({ medicalProductId: medical.medicalProduct.id, medicalProductStocks: medicalProductStocks })` | medical.medicalProduct.id, medicalProductStocks | 累积数组 |
| L35074 | 长度判空 | `if (!medicalProductStockBatctPoListJson.length)` | 数组 | resolve(false) |
| L35078 | 序列化 | `medicalProductStockBatctPoListJson = JSON.stringify(medicalProductStockBatctPoListJson)` | 数组 | 字符串 |
| L35079 | Promise 传出 | `return resolve(medicalProductStockBatctPoListJson)` | 字符串 | resolve |

### 3.3 函数特征（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 参数 | `item`（含 item.medicalProductVoList） | A |
| F4 调用 | L35054 唯一 1 处 | A |
| result 处理 | status 检查 + result.list 消费 | A |
| 中间对象 | medicalProductStockBatctPoListJson（数组 → JSON 字符串） | A |
| 传出 | Promise resolve(字符串) | A |
| 失败处理 | result.status 非 0 或数组空 → resolve(false) | A |
| 成功处理 | resolve(JSON 字符串) | A |
| 原对象 mutation | ❌ 0 处（F4 result 元素未被赋值） | A |
| angular.copy / clone | ❌ 0 处 | A |
| 类型转换 | ❌ 0 处（直接 push 引用 / 直接 JSON.stringify） | A |

---

## 4. medicalProductStockBatctPoListJson 全局审计

### 4.1 controller.js 中 medicalProductStockBatctPoListJson 全部引用（21 处）

| 行号 | 表达式 | 角色 | 是否本轮审计对象 |
|---|---|---|---|
| L3983 | `var medicalProductStockBatctPoListJson = []` | deliveryInputCtrl saveStock 初始化 | ❌ |
| L3998 | `medicalProductStockBatctPoListJson.push({...})` | deliveryInputCtrl push | ❌ |
| L4001 | `if (!medicalProductStockBatctPoListJson.length)` | deliveryInputCtrl 判空 | ❌ |
| L4007 | `medicalProductStockBatctPoListJson: JSON.stringify(...)` | deliveryInputCtrl F5 Request | ❌ |
| L16183 | `var medicalProductStockBatctPoListJson = []` | machineOrderCtrl saveStock 初始化 | ❌ |
| L16200 | `medicalProductStockBatctPoListJson.push({...})` | machineOrderCtrl push | ❌ |
| L16206 | `if (!medicalProductStockBatctPoListJson.length)` | machineOrderCtrl 判空 | ❌ |
| L16213 | `medicalProductStockBatctPoListJson: JSON.stringify(...)` | machineOrderCtrl F5 Request | ❌ |
| **L35061** | **`var medicalProductStockBatctPoListJson = []`** | **optometryCtrl concatMedicalProductStock 初始化** | **✅ 本轮** |
| **L35069** | **`medicalProductStockBatctPoListJson.push({...})`** | **optometryCtrl push** | **✅ 本轮** |
| **L35074** | **`if (!medicalProductStockBatctPoListJson.length)`** | **optometryCtrl 判空** | **✅ 本轮** |
| **L35078** | **`medicalProductStockBatctPoListJson = JSON.stringify(...)`** | **optometryCtrl 序列化** | **✅ 本轮** |
| **L35079** | **`return resolve(medicalProductStockBatctPoListJson)`** | **optometryCtrl 传出** | **✅ 本轮** |
| **L35097** | **`$scope.concatMedicalProductStock(medical).then(function (medicalProductStockBatctPoListJson) {...})`** | **choseFactoryMethod 接参** | **✅ 本轮** |
| **L35098** | **`if (!medicalProductStockBatctPoListJson) return;`** | **choseFactoryMethod 判空** | **✅ 本轮** |
| **L35102** | **`medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson`** | **setMedicalRecordProcessMode Request** | **✅ 本轮** |
| **L35183** | **`$scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {...})`** | **到店取镜 接参** | **✅ 本轮** |
| **L35184** | **`if (!medicalProductStockBatctPoListJson) return;`** | **到店取镜 判空** | **✅ 本轮** |
| **L35189** | **`medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson`** | **到店取镜 Request** | **✅ 本轮** |
| **L35202** | **`$scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {...})`** | **快递发货 接参** | **✅ 本轮** |
| **L35203** | **`if (!medicalProductStockBatctPoListJson) return;`** | **快递发货 判空** | **✅ 本轮** |
| **L35208** | **`medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson`** | **快递发货 Request** | **✅ 本轮** |

### 4.2 medicalProductStockBatctPoListJson 在 optometryCtrl 中的 3 实例（A 级）

**A 级结论**：optometryCtrl 中有 **3 个独立的 medicalProductStockBatctPoListJson 局部变量**：
- 实例 1：concatMedicalProductStock 内部（L35061-L35079）— 数组 → JSON 字符串 → resolve 传出
- 实例 2：choseFactoryMethod 的 .then 回调参数（L35097）— 接 resolve 字符串
- 实例 3：到店取镜的 .then 回调参数（L35183）— 接 resolve 字符串
- 实例 4：快递发货的 .then 回调参数（L35202）— 接 resolve 字符串

### 4.3 3 实例的相互关系（A 级）

| 实例 | 来源 | 生命周期 | 共享？ |
|---|---|---|---|
| L35061-L35079 | concatMedicalProductStock 内部 var | 函数内 | ❌ 不传出 |
| L35097 then(medicalProductStockBatctPoListJson) | concatMedicalProductStock(medical) resolve | choseFactoryMethod 同步链 | ❌ 独立 |
| L35183 then(medicalProductStockBatctPoListJson) | concatMedicalProductStock(item) resolve | 到店取镜同步链 | ❌ 独立 |
| L35202 then(medicalProductStockBatctPoListJson) | concatMedicalProductStock(item) resolve | 快递发货同步链 | ❌ 独立 |

**A 级结论**：
- 3 个 Write 调用**各自独立触发** concatMedicalProductStock(item)
- 每次 concatMedicalProductStock 调用都**重新生成** F4 Request + F4 Response 消费 + JSON 字符串
- 3 个 Write **不共享同一字符串实例**
- 3 个字符串可能**值相同**（若 item 相同 + 时序无 F4 后端状态变化），但**实例独立**

---

## 5. setMedicalRecordProcessMode.json

### 5.1 完整调用源码（A 级，L35084-L35125）

```javascript
// choseFactoryMethod (L35084-L35125)
$scope.choseFactoryMethod = function (medical) {
    var medicalRecordId = medical.medicalRecord.id;                                 // L35085
    var medicalRecordType = medical.medicalRecord.medicalRecordType;                // L35086
    var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType];                           // L35087
    var content = "\n...<p>请选择加工方式：</p>\n...";                              // L35088 (弹窗 HTML)
    var foot = "<button...id='close'>取消</button>...<button...id='affirm'>确定</button>"; // L35089
    window.popout_tip({ content, title: "提示", foot, border_radus: 3 })            // L35090
        .then(function (res) {
            if (res) {
                $scope.concatMedicalProductStock(medical).then(function (medicalProductStockBatctPoListJson) {
                    if (!medicalProductStockBatctPoListJson) return;
                    new ObjectFactory().saveOrQuery("/admin/setMedicalRecordProcessMode.json", {
                        medicalRecordId: medicalRecordId,                                                // L35100
                        toBeProcess: toBeProcess,                                                        // L35101
                        medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson            // L35102
                    }).then(function (result) {
                        if (result.status) {
                            return Popup.notice(result.errmsg);
                        }
                        $scope.querySingleOrder();
                        $scope.queryUndisposed();
                    });
                });
            }
        });
    $timeout(function () {
        var factor = $("#factor li");
        var factor_p = $("#factor li p");
        factor.click(function () {
            for (var i = 0; i < factor_p.length; i++) {
                factor_p[i].classList.remove("singleChoose_true");
            }
            var index = $(this).index();
            toBeProcess = index;                                                                          // L35121 (jQuery 弹窗点击覆盖)
            factor_p[index].classList.add("singleChoose_true");
        });
    });
};
```

### 5.2 完整 Request（A 级，L35099-L35103）

| 字段 | 表达式 | 来源 | 行号 | 是否来自 F4 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|---|
| `medicalRecordId` | `medicalRecordId` | choseFactoryMethod 形参 `medical.medicalRecord.id` | L35085 / L35100 | ❌ 否 | A | L1 |
| `toBeProcess` | `toBeProcess` | `{ 6: 1, 7: 0 }[medical.medicalRecord.medicalRecordType]`（初值 L35087）+ `$(...).index()`（jQuery 弹窗点击覆盖 L35121） | L35087 / L35121 | ❌ 否 | A | L1 |
| `medicalProductStockBatctPoListJson` | `medicalProductStockBatctPoListJson` | concatMedicalProductStock resolve 字符串 | L35078 / L35097 | ✅ **是**（F4 result → map/forEach → JSON） | A | L1 |

### 5.3 字段值类型（A 级）

| 字段 | JS 类型 | 实际值范围 | A-F |
|---|---|---|---|
| `medicalRecordId` | 数字（无显式转换） | `medical.medicalRecord.id` | A |
| `toBeProcess` | 数字 | `0` 或 `1`（来自 `{6:1, 7:0}` 映射 或 jQuery 弹窗点击 index 0/1） | A |
| `medicalProductStockBatctPoListJson` | 字符串 | JSON 字符串 `{ medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }` | A |

### 5.4 字段精确来源链（A 级）

```
medicalRecordId:
  choseFactoryMethod 形参 medical.medicalRecord.id
  → 局部变量 L35085
  → Request 字段 L35100
  → 字段值类型：数字

toBeProcess:
  medical.medicalRecord.medicalRecordType (medicalRecordType, L35086)
  → { 6: 1, 7: 0 }[medicalRecordType] (L35087)  // 初值
  → window.popout_tip 弹窗 promise (L35090)
  → jQuery click 事件覆盖 (L35121): toBeProcess = $(this).index()
  → Request 字段 L35101
  → 字段值类型：数字 0 或 1

medicalProductStockBatctPoListJson:
  item.medicalProductVoList.forEach → medicalProductIdArray (L35051-L35052)
  → F4 (getCanBeDeliverySkuInListOfProduct.json) (L35054)
  → [F 边界: F4 后端]
  → F4 result.result.list (L35062)
  → forEach result.list → medicalProductStocks (L35063 map)
  → push { medicalProductId, medicalProductStocks } (L35069-L35072)
  → JSON.stringify (L35078)
  → Promise resolve (L35079)
  → concatMedicalProductStock(medical).then 接参 (L35097)
  → Request 字段 L35102
  → 字段值类型：JSON 字符串
```

---

## 6. completeMedicalRecordDelivery.json

### 6.1 全局真实调用点（A 级）

`completeMedicalRecordDelivery.json` 在 optometryCtrl 范围（**L34776-L35382**）有 **2 处调用**：

| # | 行号 | 函数 | deliveryStatus | deliveryNo | 业务动作 |
|---|---|---|---|---|---|
| 1 | L35185 | clickBtn "到店取镜" | `"2"` | `undefined` | 完成到店取镜 |
| 2 | L35204 | clickBtn "快递发货" | `"1"` | `deliveryNo` (callback 参数) | 完成快递发货 |

### 6.2 调用 1 完整源码（A 级，L35180-L35198）

```javascript
// clickBtn "到店取镜"
function _() {
    $scope.hint(2, function () {  // L35181: hint 弹窗（index=2 → "确认顾客是否取走眼镜？"）
        var medicalRecordId = item.medicalRecord.id;  // L35182: 闭包 item
        $scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {
            if (!medicalProductStockBatctPoListJson) return;
            new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", {
                medicalRecordId: medicalRecordId,                                          // L35186
                deliveryStatus: "2",                                                        // L35187
                deliveryNo: undefined,                                                       // L35188
                medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson     // L35189
            }).then(function (result) {
                if (result.status) {
                    return Popup.notice(result.errmsg);
                }
                $scope.querySingleOrder();
            });
        });
    });
},
```

### 6.3 调用 2 完整源码（A 级，L35199-L35217）

```javascript
// clickBtn "快递发货"
function _() {
    $scope.express(function (deliveryNo) {  // L35200: express 弹窗（无第二参数 → 用户可输入单号）
        var medicalRecordId = item.medicalRecord.id;  // L35201: 闭包 item
        $scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {
            if (!medicalProductStockBatctPoListJson) return;
            new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", {
                medicalRecordId: medicalRecordId,                                          // L35205
                deliveryStatus: "1",                                                        // L35206
                deliveryNo: deliveryNo,                                                      // L35207
                medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson     // L35208
            }).then(function (result) {
                if (result.status) {
                    return Popup.notice(result.errmsg);
                }
                $scope.querySingleOrder();
            });
        });
    });
},
```

### 6.4 两个调用 Request 字段级对比（A 级）

| 字段 | 调用 1 (deliveryStatus="2") | 调用 2 (deliveryStatus="1") | 是否相同 |
|---|---|---|---|
| `medicalRecordId` | `item.medicalRecord.id` (L35182/L35186) | `item.medicalRecord.id` (L35201/L35205) | ✅ 相同 |
| **`deliveryStatus`** | **`"2"`** (L35187) | **`"1"`** (L35206) | ❌ **不同** |
| **`deliveryNo`** | **`undefined`** (L35188) | **`deliveryNo` 回调参数** (L35207) | ❌ **不同** |
| `medicalProductStockBatctPoListJson` | concatMedicalProductStock resolve 字符串 | concatMedicalProductStock resolve 字符串 | ✅ 相同字段名 |
| 其它字段 | ❌ 无 | ❌ 无 | — |

### 6.5 deliveryStatus 精确来源（A 级）

| 调用 | deliveryStatus 表达式 | 实际值 | A-F |
|---|---|---|---|
| 1 | `deliveryStatus: "2"` | **字符串字面量 "2"** | A |
| 2 | `deliveryStatus: "1"` | **字符串字面量 "1"** | A |

**A 级结论**：
- deliveryStatus 全部为**字符串字面量**
- ❌ **0 处**外部变量传入 deliveryStatus
- ❌ **0 处** $scope.deliveryStatus 读取
- ❌ **0 处** function parameter 接收
- ❌ **0 处** item.deliveryStatus 读取
- deliveryStatus 取值完全**硬编码**在 saveOrQuery 调用点

### 6.6 deliveryNo 精确来源（A 级）

| 调用 | deliveryNo 表达式 | 实际值 | 来源链 | A-F |
|---|---|---|---|---|
| 1 | `deliveryNo: undefined` | **undefined** | 字面量 | A |
| 2 | `deliveryNo: deliveryNo` | **express 弹窗回调参数** | `$scope.express(function (deliveryNo) {...})` (L35200) → `res && fn(res)` (L35044) | A |

**A 级结论**：
- deliveryNo 两种来源：**字面量 undefined**（调用 1）/ **弹窗回调参数**（调用 2）
- 弹窗回调参数来自 `window.popout_cb` Promise resolve（具体实现 F 边界）

### 6.7 $scope.express 实现（A 级，L35032-L35046）

```javascript
$scope.express = function (fn) {
    var orderNo = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "";
    var disabled = !!orderNo ? "disabled" : "";
    var content = "\n...<p>快递单号<span class='asterisk'>*</span></p>\n<input class='form-control mt10' " + disabled + " value=\"" + orderNo + "\" id=\"cb\" type=\"text\" />\n...";
    var foot = (!orderNo ? "<button class='btn btn-default ml10' id='close'>取消</button>" : "") + "<button class='btn btn-primary ml10' style=\"width:100px\" id='affirm'>确定</button>";
    window.popout_cb({ content, title: "发货", foot, border_radus: 3 })
        .then(function (res) {
            res && fn(res);
        });
};
```

| 维度 | 评估 | A-F |
|---|---|---|
| 参数 1 | `fn`（回调函数） | A |
| 参数 2 | `orderNo`（默认 ""，第 2 个参数） | A |
| disabled 行为 | 若 orderNo 非空 → input disabled，否则可编辑 | A |
| 回调返回 | `fn(res)` 其中 res = popout_cb resolve 值（即输入框 value） | A |
| L35200 调用 | `$scope.express(function (deliveryNo) {...})` — **无第二参数** → orderNo="" → input 不 disabled → 用户可输入 | A |
| L35219 调用（"查看单号"） | `$scope.express(function () {}, item.medicalRecordDelivery.deliveryNo)` — **有第二参数** → orderNo 非空 → input disabled → 用户只读 | A |

**A 级结论**：
- 快递发货路径下，deliveryNo 来自用户输入框（用户可编辑）
- 查看单号路径下，deliveryNo 仅显示（用户不可编辑）
- 弹窗实现细节（popout_cb）= **F 边界**（无源码）

### 6.8 medicalRecordId 精确来源（A 级）

| 调用 | medicalRecordId 表达式 | 来源 | A-F |
|---|---|---|---|
| 1 (L35185) | `medicalRecordId: medicalRecordId` (L35186) | `var medicalRecordId = item.medicalRecord.id` (L35182) | A |
| 2 (L35204) | `medicalRecordId: medicalRecordId` (L35205) | `var medicalRecordId = item.medicalRecord.id` (L35201) | A |

**A 级结论**：
- 两次都来自 clickBtn 外层闭包 `item.medicalRecord.id`
- `item` 是 clickBtn(name, item, index) 形参
- 实际 clickBtn 调用方（HTML ng-click 不可得）= **F 边界**

---

## 7. 三个 Request 全字段对比

### 7.1 setMedicalRecordProcessMode.json（A 级）

```javascript
{
    medicalRecordId: medicalRecordId,                                       // L35100
    toBeProcess: toBeProcess,                                               // L35101
    medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson  // L35102
}
```

### 7.2 completeMedicalRecordDelivery.json deliveryStatus="2"（A 级）

```javascript
{
    medicalRecordId: medicalRecordId,                                       // L35186
    deliveryStatus: "2",                                                    // L35187
    deliveryNo: undefined,                                                  // L35188
    medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson  // L35189
}
```

### 7.3 completeMedicalRecordDelivery.json deliveryStatus="1"（A 级）

```javascript
{
    medicalRecordId: medicalRecordId,                                       // L35205
    deliveryStatus: "1",                                                    // L35206
    deliveryNo: deliveryNo,                                                 // L35207
    medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson  // L35208
}
```

### 7.4 字段差异矩阵（A 级）

| 字段 | Write A (setMedicalRecordProcessMode) | Write B (deliveryStatus="2") | Write C (deliveryStatus="1") |
|---|---|---|---|
| medicalRecordId | ✅ | ✅ | ✅ |
| toBeProcess | ✅ | ❌ 无 | ❌ 无 |
| deliveryStatus | ❌ 无 | ✅ "2" | ✅ "1" |
| deliveryNo | ❌ 无 | ✅ undefined | ✅ deliveryNo (callback) |
| medicalProductStockBatctPoListJson | ✅ | ✅ | ✅ |

### 7.5 严格表述（A 级）

- "3 个 Write 共同字段 = `medicalRecordId` + `medicalProductStockBatctPoListJson`"：**A**
- "3 个 Write 唯一差异 = `toBeProcess` / `deliveryStatus` + `deliveryNo`"：**A**
- "setMedicalRecordProcessMode 不传 deliveryStatus/deliveryNo"：**A**
- "completeMedicalRecordDelivery 不传 toBeProcess"：**A**

---

## 8. F4 字段是否再次加工（**关键反证**）

### 8.1 concatMedicalProductStock 内部再次加工检查（A 级）

| 字段 | concatMedicalProductStock 内是否再次修改 | A-F |
|---|---|---|
| `medicalProductStockBatctPoListJson[i].medicalProductId` | ❌ 0 处（仅 push 新对象） | A |
| `medicalProductStockBatctPoListJson[i].medicalProductStocks[j].stockInSkuId` | ❌ 0 处（仅 push 新对象） | A |
| `medicalProductStockBatctPoListJson[i].medicalProductStocks[j].deliveryCount` | ❌ 0 处（仅 push 新对象） | A |
| 整个 medicalProductStockBatctPoListJson | ❌ 0 处 map/filter/sort/concat/parse | A |

### 8.2 3 个 Write 调用点再次加工检查（A 级）

| 字段 | 3 Write 调用点是否再次修改 | A-F |
|---|---|---|
| medicalProductStockBatctPoListJson（变量） | ❌ 0 处（仅作为 Request 字段值传入） | A |
| `obj.deliveryCount =` | ❌ 0 处 | A |
| `obj.stockInSkuId =` | ❌ 0 处 | A |
| `obj.medicalProductId =` | ❌ 0 处 | A |
| JSON.parse | ❌ 0 处 | A |
| JSON.stringify | ❌ 0 处（已在 concatMedicalProductStock 完成） | A |
| Number / parseInt / String | ❌ 0 处 | A |
| angular.copy | ❌ 0 处 | A |
| concat / 拼接 / 替换 | ❌ 0 处 | A |

### 8.3 A 级结论
- **F4 result.list → medicalProductStockBatctPoListJson 字符串 → 3 个 Write Request** 全程**0 处再次加工**
- 中间对象 medicalProductStockBatctPoListJson 仅经过：
  - concatMedicalProductStock 内的 L35069 push + L35078 JSON.stringify
  - resolve 传出
  - 3 个 caller 的 .then 接参
  - 直接作为 Request 字段值传入 saveOrQuery

---

## 9. 其它 Read API 检查

### 9.1 3 Write 前后 Read API（A 级）

| 时机 | Read API | 行号 | 角色 |
|---|---|---|---|
| choseFactoryMethod 调用前 | ❌ 无 Read | — | 仅 click 触发 |
| 到店取镜 调用前 | ❌ 无 Read | — | 仅 click 触发 |
| 快递发货 调用前 | ❌ 无 Read | — | 仅 click 触发 |
| concatMedicalProductStock 内部 | `/admin/getCanBeDeliverySkuInListOfProduct.json` (F4) | L35054 | 唯一 Read |
| 弹窗交互 | window.popout_tip / popout_cb | L35022 / L35038 | 浏览器 DOM（**非**项目 Read API） |
| setMedicalRecordProcessMode success | `/admin/getMedicalRecordFlowVo.json` (querySingleOrder) + `/admin/stateTodoMedicalRecordCount.json` (queryUndisposed) | L35107 / L35108 | 刷新 Read |
| completeMedicalRecordDelivery "2" success | `/admin/getMedicalRecordFlowVo.json` (querySingleOrder) | L35194 | 刷新 Read |
| completeMedicalRecordDelivery "1" success | `/admin/getMedicalRecordFlowVo.json` (querySingleOrder) | L35213 | 刷新 Read |

### 9.2 querySingleOrder 实现（A 级，L34883-L34895）

```javascript
$scope.querySingleOrder = function () {
    var medicalRecordId = $scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id;
    new ObjectFactory().saveOrQuery("/admin/getMedicalRecordFlowVo.json", {
        medicalRecordId: medicalRecordId
    }).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        $timeout(function () {
            $scope.selectOrderListFactory.items[$scope.orderIndex] = result.object;
            $scope.filter_medicalRecordStatus_update(result.object, "button", $scope.orderIndex);
        });
    });
};
```

**A 级结论**：
- querySingleOrder 是 Read API
- 修改 `$scope.selectOrderListFactory.items[$scope.orderIndex] = result.object`（**前端** mutation）
- 依赖 `$scope.selectOrderListFactory` 和 `$scope.orderIndex` 之前已被设置（clickBtn L35130 设置）

### 9.3 queryUndisposed 实现（A 级，L34841-L34849）

```javascript
$scope.queryUndisposed = function () {
    var object = $scope.dealTime();
    new ObjectFactory().saveOrQuery("/admin/stateTodoMedicalRecordCount.json", object).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        $scope.toPayCount = result.result.object;
    });
};
```

**A 级结论**：
- queryUndisposed 是 Read API
- 写入 `$scope.toPayCount = result.result.object`（**前端** mutation）

---

## 10. success 行为对照

### 10.1 setMedicalRecordProcessMode success（A 级，L35104-L35108）

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |
| 3 | `$scope.queryUndisposed()` | A |

**后续 Read 调用**：
- querySingleOrder → `/admin/getMedicalRecordFlowVo.json`（Read，刷新单条订单）
- queryUndisposed → `/admin/stateTodoMedicalRecordCount.json`（Read，刷新待处理数量）

### 10.2 completeMedicalRecordDelivery "2" success（A 级，L35191-L35194）

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |

**后续 Read 调用**：
- querySingleOrder → `/admin/getMedicalRecordFlowVo.json`（Read，刷新单条订单）

### 10.3 completeMedicalRecordDelivery "1" success（A 级，L35210-L35213）

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |

**后续 Read 调用**：
- querySingleOrder → `/admin/getMedicalRecordFlowVo.json`（Read，刷新单条订单）

### 10.4 success 行为差异（A 级）

| 维度 | Write A (setMedicalRecordProcessMode) | Write B (deliveryStatus="2") | Write C (deliveryStatus="1") |
|---|---|---|---|
| Popup 错误处理 | ✅ | ✅ | ✅ |
| querySingleOrder | ✅ | ✅ | ✅ |
| queryUndisposed | ✅ | ❌ | ❌ |
| reload | ❌ | ❌ | ❌ |
| state.go | ❌ | ❌ | ❌ |
| $scope flag 重置 | ❌ | ❌ | ❌ |
| modal 关闭 | ❌ | ❌ | ❌ |

**A 级结论**：
- 3 Write 共同 success 行为 = 错误弹窗 + querySingleOrder
- 唯一差异：setMedicalRecordProcessMode 额外触发 queryUndisposed

---

## 11. 重复提交防护（A 级）

| 检查项 | optometryCtrl 3 Write | A-F |
|---|---|---|
| debounce | ❌ 0 处 | A |
| disabled 标志 | ❌ 0 处（Controller 内部；HTML 不可得） | A |
| promise lock | ❌ 0 处 | A |
| 互斥锁 | ❌ 0 处 | A |
| 节流 / throttle | ❌ 0 处 | A |
| recursion | ❌ 0 处 | A |
| 循环提交 | ❌ 0 处（每个 Write 在 clickBtn fnMap 内单次触发） | A |
| 异步等待 | ❌ 0 处（依赖 then chain） | A |

**A 级结论**：
- 当前 Controller 范围内**未观察到**重复提交防护逻辑
- 是否存在 UI 层面（HTML 按钮 disabled）防重：**F**（HTML 不可得）
- 是否存在服务端（API 幂等性）防重：**F**（无后端代码）

---

## 12. 与 deliveryInputCtrl F4 → F5 链对照

### 12.1 维度对照（A 级）

| 维度 | deliveryInputCtrl F4 → F5 | optometryCtrl F4 → 3 Write |
|---|---|---|
| **F4 API** | getCanBeDeliverySkuInListOfProduct.json | getCanBeDeliverySkuInListOfProduct.json ✅ 同 |
| **F4 Request 字段** | medicalProductIdArray | medicalProductIdArray ✅ 同 |
| **F4 result.list 消费** | L3985-3991（直接读 result.list 元素） | L35062-35073（构造 medicalProductStockBatctPoListJson） |
| **中间对象** | ❌ 无（saveStock 直接消费 result.list） | medicalProductStockBatctPoListJson（数组 → JSON 字符串） |
| **JSON.stringify 次数** | 1（saveStock L4007） | 1（concatMedicalProductStock L35078） |
| **进入 Write API 数** | 1 | 3 |
| **Write API 名** | saveMedicalProductStockBatch.json | setMedicalRecordProcessMode.json + completeMedicalRecordDelivery.json ×2 |
| **Write API 业务动作** | 保存发货库存 | 选加工方式 + 完成取镜 + 完成快递发货 |
| **字段复用** | 4 字段（medicalProductId + stockInSkuId + deliveryCount + listCount） | 共享 2 字段（medicalRecordId + medicalProductStockBatctPoListJson） |
| **deliveryStatus 字段** | ❌ 无 | ✅ "1" / "2"（字面量） |
| **deliveryNo 字段** | ❌ 无 | ✅ undefined / 弹窗回调参数 |
| **toBeProcess 字段** | ❌ 无 | ✅ 0/1（medicalRecordType 映射 + 弹窗覆盖） |
| **success 行为** | $state.reload() + ...（deliveryInputCtrl saveStock L4014-L4017） | querySingleOrder + queryUndisposed / 仅 querySingleOrder |
| **是否 reload** | ✅ | ❌ |

### 12.2 关键差异（A 级）

1. **F4 result 消费模式不同**：
   - deliveryInputCtrl：直接读 result.list 元素（L3985-L3991）
   - optometryCtrl：先 map/forEach 构造新数组，再 JSON.stringify
2. **Write 字段命名不同**：
   - deliveryInputCtrl：4 字段（medicalProductId / stockInSkuId / deliveryCount / listCount）
   - optometryCtrl：medicalProductStockBatctPoListJson（**整体** JSON 字符串）+ medicalRecordId + 各自业务字段
3. **Write 业务不同**：
   - deliveryInputCtrl：保存库存批次（F5）
   - optometryCtrl：完成流程节点（选加工/完成取镜/完成发货）
4. **success 行为不同**：
   - deliveryInputCtrl：search() + getCount() + $state.reload()
   - optometryCtrl：querySingleOrder() + (queryUndisposed 仅 setMedicalRecordProcessMode)

### 12.3 A 级结论
- 两个 controller 的 F4 → Write 链**完全不同**
- 唯一共同点 = API 字符串 + Request.medicalProductIdArray 字段名 + F4 result 字段路径
- 不能说"同一 F4 流程" — 它们是**两个独立业务流**，共享 API 但数据结构/字段/下游均不同

---

## 13. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | concatMedicalProductStock 定位 | L35048-L35082 | A | L1 | |
| 02 | 参数 | `item`（含 item.medicalProductVoList） | A | L1 | |
| 03 | F4 result 来源 | L35054 | A | L1 | 唯一 Read |
| 04 | forEach/map | L35051 / L35062 / L35063 | A | L1 | |
| 05 | medicalProductId | L35070 `medical.medicalProduct.id` | A | L1 | |
| 06 | stockInSkuId | L35065 `delivery.stockInSku.id` | A | L1 | |
| 07 | deliveryCount | L35066 `delivery.deliveryCount` | A | L1 | |
| 08 | 中间数组 | medicalProductStockBatctPoListJson（数组） | A | L1 | L35061 |
| 09 | JSON.stringify | L35078 | A | L1 | |
| 10 | Promise.resolve | L35079 / L35044 (express) | A | L1 | |
| 11 | 变量定义 | L35061 / L35097 / L35183 / L35202 (4 实例) | A | L1 | 详见 §4.2 |
| 12 | setMedicalRecordProcessMode API | L35099 | A | L1 | Write A |
| 13 | Factory | 匿名 `new ObjectFactory()` | A | L1 | |
| 14 | Request 全字段 | { medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson } | A | L1 | 详见 §5.2 |
| 15 | Request 中 F4 字符串 | medicalProductStockBatctPoListJson (L35102) | A | L1 | F4 result 衍生 |
| 16 | deliveryStatus 来源 | L35187/L35206 字面量 "2"/"1" | A | L1 | **0 处外部传入** |
| 17 | completeMedicalRecordDelivery 调用 1 | L35180-L35198 | A | L1 | deliveryStatus="2" |
| 18 | 调用 1 Request | L35185-L35189 | A | L1 | 详见 §6.2 |
| 19 | completeMedicalRecordDelivery 调用 2 | L35199-L35217 | A | L1 | deliveryStatus="1" |
| 20 | 调用 2 Request | L35204-L35208 | A | L1 | 详见 §6.3 |
| 21 | 两个 Request 差异 | deliveryStatus / deliveryNo | A | L1 | 详见 §6.4 |
| 22 | 其它 Read API | querySingleOrder / queryUndisposed | A | L1 | success 后调用 |
| 23 | 三 Write 是否复用同一字符串 | ❌ 否（4 独立实例） | A | L1 | 详见 §4.2 |
| 24 | F4 三字段是否再次修改 | ❌ 0 处 | A | L1 | 详见 §8 |
| 25 | success 行为 | { 错误弹窗 + querySingleOrder, +queryUndisposed（仅 A）} | A | L1 | 详见 §10 |
| 26 | F4→3 Write 最小协议 | concatMedicalProductStock resolve 字符串 → 3 Write Request.medicalProductStockBatctPoListJson | A | L1 | |

**统计**：
- **A：26 项**（全部 A，无 E/F/D）
- **F：0**（仅 26 项矩阵表内）
- **E：0**
- **D：0**
- **B：0**
- **E/F 升 A：0**

---

## 14. L1/L2/L3

### L1（源码事实，可证）

- 3 Write API 字符串 + 行号（A）
- 3 Write API Request 字段 + 来源（A）
- deliveryStatus / deliveryNo / toBeProcess 字面量或参数（A）
- concatMedicalProductStock 函数体 35 行完整（A）
- medicalProductStockBatctPoListJson 4 实例（A）
- F4 字段 0 处再次加工（A）
- success 行为 3 套各自完整（A）
- 0 处重复提交防护（A）
- querySingleOrder / queryUndisposed Read 性质（A）

### L2（业务解释，未证）

- "deliveryStatus='1' = 快递发货"：**E**（未证）
- "deliveryStatus='2' = 到店取镜"：**E**（未证）
- "setMedicalRecordProcessMode = 选加工方式"：**E**（未证）
- "toBeProcess 0=不加工 1=加工"：**仅 L35101 源码注释**（A），但**禁止升级**为业务规则
- "completeMedicalRecordDelivery = 完成取镜/发货"：**E**（未证）
- "medicalProductStockBatctPoListJson = 库存批次"：**E**（未证）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 3 Write 后端实现）

---

## 15. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 3 Write 后端处理 | 无后端代码 | F |
| 3 Write 真实 Response schema | 无样本 | F |
| 3 Write 幂等性 | 无后端代码 | F |
| 3 Write 实际字段命名是否后端能识别 | 无后端代码 | F |
| deliveryStatus / deliveryNo 后端具体语义 | 无后端代码 / 仅字面量 | F |
| 弹窗 popout_tip / popout_cb 内部实现 | 无源码 | F |
| optometryCtrl HTML 模板 | 7 HTML 0 处匹配 | F |
| HTML 按钮 disabled 防重 | HTML 不可得 | F |
| $scope.popout_tip / popout_cb 完整定义 | 全文搜可能存在外部 JS | F（需进一步检查） |
| medicalRecordType 6/7 业务含义 | 无业务字典 | F |
| item 来源（clickBtn 调用方） | HTML 不可得 | F |

---

## 16. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 3 Write 实际调用 = 0 | ✅ | 未触发 setMedicalRecordProcessMode / completeMedicalRecordDelivery |
| 任何 save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 159 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 159_*.md |
| 文件编号连续 | ✅ | 158 已被 S1-97 占用，本轮使用 159 |

---

## 17. 最终结论

### 17.1 完整链路（A 级闭合节点 + F 边界）

```
item.medicalProductVoList (clickBtn 闭包 item)
    ↓ forEach (L35051)
medicalProductIdArray
    ↓ F4 Request (L35054-L35056)
[ F 边界: F4 后端 ]
    ↓
F4 result.result.list
    ↓ forEach (L35062) + map (L35063)
medicalProductStockBatctPoListJson (数组)
    { medicalProductId, medicalProductStocks: [{ stockInSkuId, deliveryCount }] }
    ↓ JSON.stringify (L35078)
medicalProductStockBatctPoListJson (字符串)
    ↓ Promise resolve (L35079)
.then(medicalProductStockBatctPoListJson => {...})
    ↓ 3 caller 分流:
    ↓
[A] setMedicalRecordProcessMode.json (L35099)
    { medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson }
[B] completeMedicalRecordDelivery.json (L35185, deliveryStatus="2")
    { medicalRecordId, deliveryStatus: "2", deliveryNo: undefined, medicalProductStockBatctPoListJson }
[C] completeMedicalRecordDelivery.json (L35204, deliveryStatus="1")
    { medicalRecordId, deliveryStatus: "1", deliveryNo: deliveryNo (callback), medicalProductStockBatctPoListJson }
    ↓ saveOrQuery (Write)
[ F 边界: 3 Write 后端处理 ]
```

### 17.2 三个 Write Request 最小协议（A 级）

| Write | API | Request 字段 |
|---|---|---|
| **A** | setMedicalRecordProcessMode.json | `{ medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson }` |
| **B** | completeMedicalRecordDelivery.json | `{ medicalRecordId, deliveryStatus: "2", deliveryNo: undefined, medicalProductStockBatctPoListJson }` |
| **C** | completeMedicalRecordDelivery.json | `{ medicalRecordId, deliveryStatus: "1", deliveryNo: <callback>, medicalProductStockBatctPoListJson }` |

### 17.3 关键事实（A 级）

1. **F4 是 concatMedicalProductStock 内部唯一 Read**
2. **medicalProductStockBatctPoListJson 在 optometryCtrl 范围有 4 个独立实例**（concatMedicalProductStock 内部 + 3 个 .then 接参）
3. **3 Write 不共享同一字符串实例**（每次 concatMedicalProductStock 调用都重新生成）
4. **F4 result 三字段（medicalProductId / stockInSkuId / deliveryCount）在 concatMedicalProductStock 之后 0 处再次加工**
5. **deliveryStatus 是字符串字面量**（"1"/"2"），**0 处外部传入**
6. **deliveryNo 在 deliveryStatus="2" 时 = undefined 字面量**；在 deliveryStatus="1" 时 = 弹窗回调参数
7. **toBeProcess 来源**：medicalRecordType 映射 `{ 6: 1, 7: 0 }` + jQuery 弹窗点击覆盖
8. **3 Write 共同 success 行为**：错误弹窗 + querySingleOrder；setMedicalRecordProcessMode 额外调 queryUndisposed
9. **0 处重复提交防护**

### 17.4 与 S1-97 对照

| 维度 | S1-97 | S1-98 |
|---|---|---|
| F4 链路 | 端到端（含 3 Write 入口） | 字段级闭合（逐 Request 逐字段） |
| Write 数 | 3（已发现） | 3（精确） |
| Request 字段 | 列表 | **完整字段映射 + 来源链** |
| deliveryStatus 来源 | 提到 "1"/"2" | **精确：字面量，0 处外部** |
| deliveryNo 来源 | 提到 callback | **精确：弹窗实现 + disabled 行为** |
| medicalProductStockBatctPoListJson 实例 | 1 描述 | **4 独立实例** |
| success 行为 | 简单列表 | **3 套各自完整 + 差异** |
| 重复提交 | 未审 | **0 处防护** |
| 与 deliveryInputCtrl 对照 | 简述 | **逐维度精确对比** |

### 17.5 不可在本轮升级为 A 的项

- 3 Write 后端处理（F）
- 3 Write 真实 Response schema（F）
- 3 Write 幂等性（F）
- deliveryStatus 业务语义（E）
- deliveryNo 业务语义（E）
- toBeProcess 业务语义（仅 L35101 注释，禁止升级）
- optometryCtrl HTML 模板（F）
- UI 防重（F）

---

**审计结束**。
