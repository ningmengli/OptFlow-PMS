# S1-99 optometryCtrl 三 Write 动作入口与参数来源审计

> **任务名**：S1-99｜optometryCtrl 三 Write 动作入口 + medicalRecordId/toBeProcess/deliveryNo 来源审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）+ clickBtn fnMap + choseFactoryMethod + concatMedicalProductStock 全链路
> **当前轮次**：S1-99（接 S1-98 完成）
> **本轮承诺**：3 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| setMedicalRecordProcessMode.json 调用点 L35099 | ✅ | Write A |
| completeMedicalRecordDelivery.json 调用点 L35185 / L35204 | ✅ | Write B / Write C |
| clickBtn (L35128) + fnMap (L35131-L35224) | ✅ | 动作入口 |
| choseFactoryMethod (L35084-L35125) | ✅ | Write A 入口链 |
| concatMedicalProductStock (L35048-L35082) | ⚠️ 旁证 | S1-98 已审 |
| $scope.hint (L35010-L35030) | ✅ | Write B 入口弹窗 |
| $scope.express (L35032-L35046) | ✅ | Write C 入口弹窗 |
| querySingleOrder / queryUndisposed (L34883 / L34841) | ✅ | success 后 Read |
| medicalRecordType / toBeProcess 全部引用 | ✅ | toBeProcess 生命周期 |
| 7 HTML | ❌（不可得）| UI 触发点 F |
| 3 Write 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "加工 = 不加工/店内加工"：**E**（仅 L35088 HTML 弹窗文字 + L35101 源码注释）
- "deliveryStatus='1'/'2' = 快递发货/到店取镜"：**E**（仅上下文 + 命名巧合）
- "medicalRecordId = 数据库主键"：**E**（未证）
- "deliveryNo = 快递单号"：**E**（未证，仅 $scope.express 弹窗文字"快递单号"）
- "medicalRecordType 6/7 业务含义"：**E**（仅 L35087 字段映射数字）
- "clickBtn 由 ng-click 触发"：**E**（未证 HTML）

---

## 3. 三 Write 全局引用

### 3.1 setMedicalRecordProcessMode.json 全仓命中（A 级）

| 文件 | 行号 | 性质 |
|---|---|---|
| controller.js | L35099 | **唯一真实调用** |
| 158_S1-97_*.md | L359/L382/L400/L468/L515/L663/L676 | 历史 MD 引用 |
| 159_S1-98_*.md | L183/L200/L420/L649/L807/L821 | 历史 MD 引用 |

**A 级结论**：setMedicalRecordProcessMode.json 在 controller.js **仅 1 处真实调用**（L35099）；7 HTML 0 处；其它历史 MD 均为审计引用。

### 3.2 completeMedicalRecordDelivery.json 全仓命中（A 级）

| 文件 | 行号 | 性质 |
|---|---|---|
| controller.js | L35185 | **真实调用 1（deliveryStatus="2"）** |
| controller.js | L35204 | **真实调用 2（deliveryStatus="1"）** |
| 158_S1-97_*.md | L360/L361/L382/L400/L468/L516/L664/L665/L676 | 历史 MD 引用 |
| 159_S1-98_*.md | L278/L282/L298/L323/L430/L441/L649/L809/L811/L822/L823 | 历史 MD 引用 |

**A 级结论**：completeMedicalRecordDelivery.json 在 controller.js **2 处真实调用**（L35185/L35204）；7 HTML 0 处；其它历史 MD 均为审计引用。

### 3.3 其它 Consumer 检查（A 级）

| 检查项 | 结果 |
|---|---|
| 其它 controller 是否调用 setMedicalRecordProcessMode | **❌ 0 处**（全 controller.js 仅 L35099） |
| 其它 controller 是否调用 completeMedicalRecordDelivery | **❌ 0 处**（全 controller.js 仅 L35185/L35204） |
| 7 HTML 是否含两个 API 字符串 | **❌ 0 处** |

**A 级结论**：两个 API 在当前仓库资源范围内**仅 optometryCtrl 是 Consumer**。

---

## 4. Write Controller/函数定位

### 4.1 3 Write 入口函数链（A 级）

| Write | API | 行号 | 调用函数 | 调用函数行号 | 上游触发 |
|---|---|---|---|---|---|
| **A** | setMedicalRecordProcessMode.json | L35099 | choseFactoryMethod → 弹窗确认回调内 saveOrQuery | L35084-L35125 | clickBtn "加工" (L35161-L35162) |
| **B** | completeMedicalRecordDelivery.json (deliveryStatus="2") | L35185 | clickBtn "到店取镜" → hint(2, fn) 内 saveOrQuery | L35180-L35198 | clickBtn(name, item, index) (L35128) |
| **C** | completeMedicalRecordDelivery.json (deliveryStatus="1") | L35204 | clickBtn "快递发货" → express(fn) 内 saveOrQuery | L35199-L35217 | clickBtn(name, item, index) (L35128) |

### 4.2 clickBtn 完整定义（A 级，L35128-L35226）

```javascript
$scope.orderIndex = null;
$scope.clickBtn = function (name, item, index) {
    $scope.orderIndex = index;   // L35130
    var fnMap = {
        退费: function _() { $state.go("payedList"); },                       // L35132-35134
        修改: function _() { $state.go("optometryGlasses", { medicalRecordId: item.medicalRecord.id, edit: "true" }); },  // L35135-35140
        收费: function _() { if (!item.medicalProductVoList.length) { return Popup.notice("请添加商品！"); } $state.go("waitChargeList"); },  // L35141-35146
        取消订单: function _() { $scope.hint(1, function () { /* cancelMedicalRecord */ }); },  // L35147-35160
        加工: function _() { $scope.choseFactoryMethod(item); },              // L35161-35163
        制作完成: function _() { $scope.hint(3, function () { /* confirmMedicalRecordReturn */ }); },  // L35164-35176
        报损: function _() { $scope.order.show(true, item.medicalRecord.id); },  // L35177-35179
        到店取镜: function _() { $scope.hint(2, function () { /* completeMedicalRecordDelivery "2" */ }); },  // L35180-35198
        快递发货: function _() { $scope.express(function (deliveryNo) { /* completeMedicalRecordDelivery "1" */ }); },  // L35199-35117
        查看单号: function _() { $scope.express(function () {}, item.medicalRecordDelivery.deliveryNo); },  // L35218-35220
        通知: function _() { $scope.template.medicalRecord = item.medicalRecord.id; $scope.template.openPopout(true); }  // L35221-35224
    };
    fnMap[name] && fnMap[name]();  // L35225-35226
};
```

### 4.3 完整入口链（A 级）

```
HTML ng-click (F 不可得)
    ↓ clickBtn(name, item, index)
$scope.orderIndex = index
    ↓
fnMap[name]()
    ↓
[A] "加工" → $scope.choseFactoryMethod(item)
    ↓
window.popout_tip (L35090) 弹窗 Promise
    ↓ res truthy
$scope.concatMedicalProductStock(medical).then(...)
    ↓ medicalProductStockBatctPoListJson
new ObjectFactory().saveOrQuery("/admin/setMedicalRecordProcessMode.json", { medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson })
    ↓ [F 边界: setMedicalRecordProcessMode 后端]

[B] "到店取镜" → $scope.hint(2, function () { ... })
    ↓
window.popout_tip (L35022) 弹窗 Promise
    ↓ res truthy
$scope.concatMedicalProductStock(item).then(...)
    ↓
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { medicalRecordId, deliveryStatus: "2", deliveryNo: undefined, medicalProductStockBatctPoListJson })
    ↓ [F 边界: completeMedicalRecordDelivery 后端]

[C] "快递发货" → $scope.express(function (deliveryNo) { ... })
    ↓
window.popout_cb (L35038) 弹窗 Promise
    ↓ res truthy (deliveryNo = 输入框 value)
$scope.concatMedicalProductStock(item).then(...)
    ↓
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { medicalRecordId, deliveryStatus: "1", deliveryNo: deliveryNo, medicalProductStockBatctPoListJson })
    ↓ [F 边界: completeMedicalRecordDelivery 后端]
```

---

## 5. medicalRecordId

### 5.1 三个 Write medicalRecordId 精确来源（A 级）

| Write | 表达式 | 来源链 | 行号 | A-F |
|---|---|---|---|---|
| **A** (setMedicalRecordProcessMode) | `medicalRecordId: medicalRecordId` | `var medicalRecordId = medical.medicalRecord.id` (L35085) — choseFactoryMethod 形参 medical | L35085 / L35100 | A |
| **B** (deliveryStatus="2") | `medicalRecordId: medicalRecordId` | `var medicalRecordId = item.medicalRecord.id` (L35182) — clickBtn 形参 item | L35182 / L35186 | A |
| **C** (deliveryStatus="1") | `medicalRecordId: medicalRecordId` | `var medicalRecordId = item.medicalRecord.id` (L35201) — clickBtn 形参 item | L35201 / L35205 | A |

### 5.2 medical / item 来源（A 级）

| 形参 | 来源 | 层级 | A-F |
|---|---|---|---|
| `medical` (choseFactoryMethod 形参) | clickBtn "加工" action L35162 `$scope.choseFactoryMethod(item)` — 即 **item = clickBtn 形参** | 同一 item | A |
| `item` (clickBtn 形参) | HTML ng-click `clickBtn(name, item, index)` — 由 selectOrderListFactory.items[index] 提供 | 一致 selectOrderListFactory.items[index] | A（参数名） / F（HTML 不可得） |

### 5.3 medicalRecordId 同源判定（A 级）

**A 级结论**：
- 3 Write 的 medicalRecordId 表达式**最终都来自** `$scope.selectOrderListFactory.items[index].medicalRecord.id`（经过 clickBtn 形参 item 传递）
- choseFactoryMethod 路径：`selectOrderListFactory.items[index].medicalRecord.id` → item.medicalRecord.id → medical.medicalRecord.id → medicalRecordId
- 到店取镜 / 快递发货路径：`selectOrderListFactory.items[index].medicalRecord.id` → item.medicalRecord.id → medicalRecordId
- **3 Write 的 medicalRecordId 表达式来源相同**（A 级 — Controller 表达式层）
- **不能证明** 3 Write 的 medicalRecordId 字段值一定相同（依赖运行时 item 和 index 状态）
- **不能证明** 后端是否为同一数据库对象（L3 = F）

### 5.4 medicalRecordId 校验（A 级）

| 检查 | 结果 |
|---|---|
| `if (medicalRecordId)` | ❌ 0 处 |
| `if (!medicalRecordId)` | ❌ 0 处 |
| 类型校验 | ❌ 0 处 |
| 范围校验 | ❌ 0 处 |
| 长度校验 | ❌ 0 处 |

**A 级结论**：3 Write **均无 medicalRecordId 校验**（直接透传）。

---

## 6. toBeProcess 完整生命周期

### 6.1 toBeProcess 全部 5 处（A 级，已穷举 optometryCtrl 范围）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L34806 | `params: { toBeProcess: 2, deleted: 0 }` | **另一处独立使用**（非 choseFactoryMethod，statProductDeliveryStatusOfCashflow 之类的 params，可能是 query 参数） | A |
| L35087 | `var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType];` | choseFactoryMethod 初始化 | A |
| L35088 | `... + (toBeProcess == 0 ? "singleChoose_true" : "") + ...` | 弹窗 HTML 模板（判 == 0） | A |
| L35088 | `... + (toBeProcess == 1 ? "singleChoose_true" : "") + ...` | 弹窗 HTML 模板（判 == 1） | A |
| L35101 | `toBeProcess: toBeProcess, // 0 不加工  1  加工` | setMedicalRecordProcessMode Request 字段 | A |
| L35121 | `toBeProcess = index;` | $timeout jQuery 弹窗点击覆盖 | A |

### 6.2 toBeProcess 初始化（A 级，L35086-L35087）

```javascript
var medicalRecordType = medical.medicalRecord.medicalRecordType;  // L35086
var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType];              // L35087
```

| medicalRecordType | toBeProcess 初值 | A-F |
|---|---|---|
| 6 | 1 | A |
| 7 | 0 | A |
| 其它（0/1/2/3/4/5/8/9/...） | **undefined** | A |
| `medical.medicalRecord.medicalRecordType` 不存在 | TypeError | A（无保护） |

**A 级结论**：
- toBeProcess 初值由 medicalRecordType 6/7 二选一决定
- 其它 medicalRecordType → toBeProcess = undefined
- 写字段时**不校验** undefined，**直接** `toBeProcess: toBeProcess`（即 undefined 传入 Request）

### 6.3 toBeProcess UI index 覆盖（A 级，L35113-L35124）

```javascript
$timeout(function () {
    var factor = $("#factor li");        // L35114
    var factor_p = $("#factor li p");    // L35115
    factor.click(function () {            // L35116
        for (var i = 0; i < factor_p.length; i++) {
            factor_p[i].classList.remove("singleChoose_true");
        }
        var index = $(this).index();     // L35120
        toBeProcess = index;             // L35121
        factor_p[index].classList.add("singleChoose_true");
    });
});
```

| 行为 | A-F |
|---|---|
| 通过 $timeout 注册 jQuery 弹窗 click 监听 | A |
| 监听 `#factor li` click | A |
| `toBeProcess = index` 覆盖 | A |
| `index` 取值：0 / 1（仅 2 个 li） | A |
| 监听注册时机：$timeout（异步） | A |

**A 级结论**：
- choseFactoryMethod 同步执行：`var toBeProcess = ...` 初值（基于 medicalRecordType）
- choseFactoryMethod **同时**注册 $timeout，弹窗点击会**异步覆盖** toBeProcess
- 用户**不点**弹窗 → toBeProcess = 初值（依赖 medicalRecordType ∈ {6, 7}）
- 用户**点**弹窗 li 0 → toBeProcess = 0
- 用户**点**弹窗 li 1 → toBeProcess = 1
- 写字段时取**最终值**（用户可能点击过 → 0/1；用户未点击 → undefined 或初值）

### 6.4 toBeProcess 最终使用（A 级，L35101）

```javascript
new ObjectFactory().saveOrQuery("/admin/setMedicalRecordProcessMode.json", {
    medicalRecordId: medicalRecordId,
    toBeProcess: toBeProcess, // 0 不加工  1  加工
    medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson
});
```

| 维度 | 评估 | A-F |
|---|---|---|
| 使用 | setMedicalRecordProcessMode Request 字段 | A |
| 注释 | L35101 `// 0 不加工  1  加工` | A |
| 其它使用 | ❌ 0 处（不进入其它 API / 不进入 scope） | A |

### 6.5 toBeProcess 类型转换（A 级）

| 操作 | 是否存在 | A-F |
|---|---|---|
| `Number()` | ❌ 0 处 | A |
| `parseInt()` | ❌ 0 处 | A |
| `String()` | ❌ 0 处 | A |
| 类型检查 | ❌ 0 处 | A |

**A 级结论**：toBeProcess 是数字字面量（来自 `{6:1, 7:0}` 映射或 jQuery index 0/1），**无任何类型转换或校验**。

### 6.6 toBeProcess 非法值校验（A 级）

- ❌ 0 处 if 校验
- ❌ 0 处医疗记录类型不在 {6, 7} 时拒绝
- ❌ 0 处 medicalRecord 缺失保护
- ❌ 0 处 toBeProcess === undefined 判空

**A 级结论**：toBeProcess **完全无校验**。

---

## 7. deliveryStatus 完整入口

### 7.1 deliveryStatus 全部引用（A 级，optometryCtrl 范围）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35187 | `deliveryStatus: "2"` | Write B Request 字段 | A |
| L35206 | `deliveryStatus: "1"` | Write C Request 字段 | A |

**A 级结论**：deliveryStatus 在 optometryCtrl 范围**仅 2 处**（L35187 / L35206），**全部是字符串字面量**。

### 7.2 deliveryStatus 全局搜索（A 级）

```
全 controller.js 搜索 deliveryStatus：
- L35187 字面量 "2"
- L35206 字面量 "1"
- (无其它命中)
```

**A 级结论**：全 controller.js 中 deliveryStatus **仅 2 处**（已穷举），无任何外部传入、变量读取、用户输入。

### 7.3 deliveryStatus 来源链（A 级）

| 字段值 | 表达式层级 | A-F |
|---|---|---|
| "2" (L35187) | 字面量 → saveOrQuery 第二个参数对象字面量 → Request body 字段 | A |
| "1" (L35206) | 同上 | A |

**A 级结论**：
- deliveryStatus **0 处** 外部变量
- deliveryStatus **0 处** function parameter
- deliveryStatus **0 处** $scope.deliveryStatus
- deliveryStatus **0 处** item.deliveryStatus
- deliveryStatus **0 处** 用户输入

### 7.4 deliveryStatus 分支关系（A 级）

| Write | deliveryStatus | 触发动词 | 触发动词来源 |
|---|---|---|---|
| A | N/A | "加工" | fnMap |
| B | "2" | "到店取镜" | fnMap |
| C | "1" | "快递发货" | fnMap |

**A 级结论**：
- 3 Write 入口是 fnMap 的 3 个不同 key（"加工" / "到店取镜" / "快递发货"）
- fnMap 字典查找：`fnMap[name] && fnMap[name]()` (L35225-L35226)
- **完全独立** 3 个 action 函数（不是 if/else 共享）
- ❌ 0 处 if/else/switch 分支

---

## 8. deliveryNo 完整来源

### 8.1 deliveryNo 全部引用（A 级，optometryCtrl 范围）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35188 | `deliveryNo: undefined` | Write B Request 字段 | A |
| L35207 | `deliveryNo: deliveryNo` | Write C Request 字段（弹窗回调参数） | A |

### 8.2 $scope.express 实现（A 级，L35032-L35046）

```javascript
$scope.express = function (fn) {
    var orderNo = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : "";
    var disabled = !!orderNo ? "disabled" : "";
    var content = "...<p>快递单号<span class='asterisk'>*</span></p>\n<input ... " + disabled + " value=\"" + orderNo + "\" id=\"cb\" type=\"text\" />...";
    var foot = (!orderNo ? "<button class='btn btn-default ml10' id='close'>取消</button>" : "") + "<button class='btn btn-primary ml10' ... id='affirm'>确定</button>";
    window.popout_cb({
        content: content,
        title: "发货",
        foot: foot,
        border_radus: 3
    }).then(function (res) {
        res && fn(res);
    });
};
```

| 维度 | 评估 | A-F |
|---|---|---|
| 参数 1 (fn) | 必填，回调函数 | A |
| 参数 2 (orderNo) | 可选，默认 ""（arguments 校验） | A |
| 弹窗实现 | window.popout_cb（**F 边界**） | A 引用 / F 实现 |
| 输入框 disabled 条件 | `!!orderNo`（orderNo 非空字符串 → disabled） | A |
| 输入框 value 初值 | orderNo（第二参数） | A |
| 确认回调 | `fn(res)`（res = popout_cb resolve 值 = 输入框 value） | A |
| 取消回调 | fn 不调用（`res && fn(res)` 短路） | A |
| 取消按钮显示 | `!orderNo`（orderNo 为空字符串时显示） | A |
| 输入校验 | ❌ 0 处（HTML required 属性、JS 校验） | A |

### 8.3 deliveryNo 触发对比（A 级）

| 调用 | 第二参数 | disabled | 取消按钮 | deliveryNo 来源 |
|---|---|---|---|---|
| L35200 `$scope.express(function (deliveryNo) {...})`（快递发货） | **未传** | **false**（可编辑） | **显示** | 用户输入框 value |
| L35219 `$scope.express(function () {}, item.medicalRecordDelivery.deliveryNo)`（查看单号） | **已传** | **true**（只读） | **隐藏** | 已存在的 deliveryNo（不进入 Write） |

### 8.4 Write C deliveryNo 完整来源链（A 级）

```
L35199 clickBtn "快递发货" action:
    function _() {
        $scope.express(function (deliveryNo) {                    // L35200: fn = 内联函数
            var medicalRecordId = item.medicalRecord.id;          // L35201
            $scope.concatMedicalProductStock(item).then(function (medicalProductStockBatctPoListJson) {
                if (!medicalProductStockBatctPoListJson) return;
                new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", {
                    medicalRecordId: medicalRecordId,
                    deliveryStatus: "1",                          // L35206
                    deliveryNo: deliveryNo,                        // L35207 ← 弹窗回调参数
                    medicalProductStockBatctPoListJson: ...
                })
            });
        });  // L35216
    }
```

**deliveryNo 完整来源链**：
```
window.popout_cb (F 边界，弹窗)
    ↓ Promise resolve
$scope.express 内 .then callback (L35043)
    ↓ res
fn(res) (L35044)
    ↓ deliveryNo = res
clickBtn "快递发货" 内的 fn (L35200)
    ↓
new ObjectFactory().saveOrQuery Request body (L35207)
```

**A 级结论**：
- deliveryNo = popout_cb resolve 值 = 输入框 value
- popout_cb 内部实现 = **F 边界**（无源码）
- ❌ 0 处 JS 层 deliveryNo 校验
- ❌ 0 处 trim / String 转换
- ❌ 0 处空字符串拒绝

---

## 9. 三 Write 分支关系

### 9.1 函数定义（A 级）

| Write | 函数定义 | 行号 |
|---|---|---|
| A | choseFactoryMethod | L35084 |
| B | clickBtn "到店取镜" action | L35180 |
| C | clickBtn "快递发货" action | L35199 |

### 9.2 分支关系判定（A 级）

| 检查 | 结果 |
|---|---|
| if / else if / else | ❌ 0 处（3 写之间无互斥条件） |
| switch | ❌ 0 处 |
| 同一函数内 3 个分支 | ❌ 否（3 个完全独立 action） |
| fnMap 字典查找 | ✅ 是（clickBtn 内 fnMap 字典） |
| fnMap[name] && fnMap[name]() | L35225-L35226（A 级） |

**A 级结论**：
- 3 Write 是**三个完全独立函数**（A 级）
- 通过 clickBtn 的 fnMap **字典查找**路由到其中一个
- **不是** if/else 互斥分支
- **不是** 同一函数的不同分支
- fnMap 互斥性由 HTML 端 UI 决定（哪个按钮 click → 哪个 name 参数 → 哪个 action）→ **F 边界**

### 9.3 fnMap 全集（A 级，L35131-L35224）

| Key | 行为 | 含 Write |
|---|---|---|
| 退费 | $state.go("payedList") | ❌ |
| 修改 | $state.go("optometryGlasses", { medicalRecordId, edit: "true" }) | ❌ |
| 收费 | 判空 + $state.go("waitChargeList") | ❌ |
| 取消订单 | hint(1, cancel) | ❌ |
| **加工** | **choseFactoryMethod(item)** | **✅ Write A** |
| 制作完成 | hint(3, confirmMedicalRecordReturn) | ❌ |
| 报损 | order.show | ❌ |
| **到店取镜** | **hint(2, completeMedicalRecordDelivery "2")** | **✅ Write B** |
| **快递发货** | **express(completion, completeMedicalRecordDelivery "1")** | **✅ Write C** |
| 查看单号 | express(callback, item.medicalRecordDelivery.deliveryNo) | ❌ |
| 通知 | template.openPopout | ❌ |

**A 级结论**：3 Write 仅占用 fnMap 的 3 个独立 key，相互不互斥（用户可点任意 key，但通常 UI 仅展示有效 key）。

---

## 10. concatMedicalProductStock 调用链

### 10.1 concatMedicalProductStock 全部引用（A 级）

| 行号 | 表达式 | 上下文 |
|---|---|---|
| L35048 | `$scope.concatMedicalProductStock = function (item) { ... }` | 函数定义 |
| L35097 | `$scope.concatMedicalProductStock(medical).then(...)` | choseFactoryMethod 内 |
| L35183 | `$scope.concatMedicalProductStock(item).then(...)` | "到店取镜" action 内 |
| L35202 | `$scope.concatMedicalProductStock(item).then(...)` | "快递发货" action 内 |

### 10.2 调用参数对比（A 级）

| 调用 | 参数 | 来源 |
|---|---|---|
| L35097 | `medical` | choseFactoryMethod 形参（来自 L35162 `$scope.choseFactoryMethod(item)`） |
| L35183 | `item` | clickBtn 闭包形参 |
| L35202 | `item` | clickBtn 闭包形参 |

**A 级结论**：
- L35097 / L35183 / L35202 三个调用**形式上**不同（medical vs item），但实际**同一个对象**：
  - clickBtn L35162: `$scope.choseFactoryMethod(item)` → 内部 medical 参数 = item
  - clickBtn L35183 / L35202: 直接传 item
- **3 个调用共享同一 item 引用**（同一次 clickBtn 触发的 action 链中）

### 10.3 Promise reject 检查（A 级）

| 检查 | concatMedicalProductStock | A-F |
|---|---|---|
| Promise reject 处理 | ❌ 0 处（new Promise 内仅 resolve，无 reject 分支） | A |
| 调用方 catch | ❌ 0 处（3 个调用都仅 .then，无 .catch） | A |
| 异常传播 | 若 Promise 内抛错（异步），then chain **不会**接住 | A |

**A 级结论**：
- concatMedicalProductStock 的 Promise **没有 reject 分支**（仅 resolve(false) 用于业务失败）
- 3 个调用方**均未 .catch**（即无错误处理）
- 若 F4 result 抛出未预期异常（如 res.result 缺失），异常会**未捕获**传播到 AngularJS 异常处理

### 10.4 concatMedicalProductStock 在 optometryCtrl 之外（A 级）

- 全 controller.js 搜索 concatMedicalProductStock：**仅 optometryCtrl 4 处**（L35048/L35097/L35183/L35202）
- 其它 controller：**0 处调用**
- 7 HTML：**0 处调用**

**A 级结论**：concatMedicalProductStock **仅 optometryCtrl 使用**。

---

## 11. Write 前置校验

### 11.1 各 Write 前置校验检查（A 级）

| 校验项 | Write A (setMedicalRecordProcessMode) | Write B (deliveryStatus="2") | Write C (deliveryStatus="1") |
|---|---|---|---|
| medicalRecordId 校验 | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 |
| toBeProcess 校验 | ❌ 0 处 | N/A | N/A |
| deliveryStatus 校验 | N/A | ❌ 0 处 | ❌ 0 处 |
| deliveryNo 校验 | N/A | ❌ 0 处（字面量 undefined） | ❌ 0 处（弹窗输入无 JS 校验） |
| medicalProductStockBatctPoListJson 校验 | ✅ L35098 `if (!medicalProductStockBatctPoListJson) return;` | ✅ L35184 同 | ✅ L35203 同 |
| F4 result.status 校验 | ✅ L35057 concatMedicalProductStock 内 | ✅ 同 | ✅ 同 |
| F4 result.list 空校验 | ✅ L35074 concatMedicalProductStock 内 `if (!medicalProductStockBatctPoListJson.length)` | ✅ 同 | ✅ 同 |
| 弹窗确认 | ✅ L35096 `if (res)` (popout_tip res) | ✅ L35181 `$scope.hint(2, fn)` 自动确认 | ✅ L35200 `$scope.express(fn)` 隐含确认（fn 被弹窗确定按钮调用）|
| F4 之前是否存在校验 | ❌ 0 处（concatMedicalProductStock 同步） | ❌ 0 处 | ❌ 0 处 |

### 11.2 concatMedicalProductStock 内部校验（A 级）

| 行号 | 校验 | 失败行为 |
|---|---|---|
| L35057 | `if (result.status)` | Popup.notice(result.errmsg) + return resolve(false) |
| L35074 | `if (!medicalProductStockBatctPoListJson.length)` | Popup.notice("未找到商品信息！") + return resolve(false) |

**A 级结论**：
- 校验集中在 concatMedicalProductStock 内部（F4 result 处理）
- 3 个 Write 调用方仅判 medicalProductStockBatctPoListJson 是否为 truthy
- 字段级校验（medicalRecordId/toBeProcess/deliveryStatus/deliveryNo）**0 处**

---

## 12. Write 前置 Read

### 12.1 各 Write 前置 Read 检查（A 级）

| Write | 直接前置 Read | 上游链 Read | success 后 Read |
|---|---|---|---|
| A (setMedicalRecordProcessMode) | F4 (concatMedicalProductStock 内部) | ❌ 无其它前置 | querySingleOrder + queryUndisposed |
| B (deliveryStatus="2") | F4 (concatMedicalProductStock 内部) | ❌ 无其它前置 | querySingleOrder |
| C (deliveryStatus="1") | F4 (concatMedicalProductStock 内部) | ❌ 无其它前置 | querySingleOrder |

### 12.2 A 级结论
- 3 Write **直接前置 Read** 仅 F4（在 concatMedicalProductStock 内部）
- 3 Write **success 后 Read**：querySingleOrder（getMedicalRecordFlowVo.json） / queryUndisposed（stateTodoMedicalRecordCount.json，**仅 Write A**）
- **0 处** 其它前置 Read（不包含 success 后）

---

## 13. UI / 弹窗边界

### 13.1 弹窗实现（F 边界）

| 弹窗 API | 行号 | 实现源码 | A-F |
|---|---|---|---|
| `window.popout_tip` | L35022 / L35090 | 全局函数 | F（无源码） |
| `window.popout_cb` | L35038 | 全局函数 | F（无源码） |
| `window.popout_tip` 内部 `res` | L35028 / L35095 | Promise resolve 值 | F |

### 13.2 弹窗触发后行为（A 级）

| 弹窗 | resolve(res) | res 含义 | 行为 |
|---|---|---|---|
| popout_tip (hint) | L35027 `res && fn()` | 用户点"确定"→ res 什么值取决于 popout_tip 实现 | 调 fn() |
| popout_tip (choseFactoryMethod) | L35095 `if (res) { concatMedicalProductStock(medical).then(...) }` | 同上 | 调 concatMedicalProductStock |
| popout_cb (express) | L35043 `res && fn(res)` | 输入框 value | 调 fn(deliveryNo) |

**A 级结论**：
- popout_tip / popout_cb 内部实现 **F 边界**（无仓库源码）
- res 含义**仅可证**为 truthy/falsy（因为 `if (res)` 行为）
- res **实际值** = F（popout_tip/popout_cb 实现不可得）

### 13.3 HTML 模板（optometryCtrl，F 边界）

- 7 HTML 中**0 处** optometry 模板
- 视光之家url.txt 中**0 处** optometry 入口（仅 optometryGlasses 提到一次）
- $scope.clickBtn 调用方（HTML ng-click）**F**
- $scope.optometry state 路由（**F** — URL 列表无 optometry state 名）

---

## 14. 重复提交防护

### 14.1 Controller 层防护检查（A 级）

| 检查项 | 3 Write | A-F |
|---|---|---|
| `disabled` 标志 | ❌ 0 处（$scope 中无 disabled 变量） | A |
| `loading` 标志 | ❌ 0 处 | A |
| `submitting` / `isSubmitting` | ❌ 0 处 | A |
| promise lock（自己挂的 lock） | ❌ 0 处 | A |
| debounce / throttle | ❌ 0 处 | A |
| setTimeout / $timeout 锁 | ❌ 0 处（$timeout 仅用于弹窗事件） | A |
| recursion | ❌ 0 处 | A |
| 循环中 saveOrQuery | ❌ 0 处 | A |
| 多次 saveOrQuery 防重 | ❌ 0 处 | A |
| UI 层 disabled（HTML 不可得） | F | F |

### 14.2 A 级结论
- 当前 Controller **未观察到** 任何重复提交防护逻辑
- 是否存在 UI 层 disabled 防重：**F**（HTML 不可得）
- 是否存在服务端幂等性：**F**（无后端代码）

---

## 15. 三 Write Request 对照

### 15.1 完整 Request 字段对照表（A 级）

| 字段 | A (setMedicalRecordProcessMode) | B (deliveryStatus="2") | C (deliveryStatus="1") | 来源 | A-F |
|---|---|---|---|---|---|
| **medicalRecordId** | ✅ 数字 | ✅ 数字 | ✅ 数字 | selectOrderListFactory.items[index].medicalRecord.id（经 clickBtn 形参 item 传递） | A |
| **toBeProcess** | ✅ 数字（0/1/undefined） | ❌ 无 | ❌ 无 | `{6:1, 7:0}[medical.medicalRecord.medicalRecordType]` 初值 + jQuery 弹窗 index 覆盖（Write A only） | A |
| **deliveryStatus** | ❌ 无 | ✅ 字符串 "2" | ✅ 字符串 "1" | 字面量（Write B/C only） | A |
| **deliveryNo** | ❌ 无 | ✅ undefined（字面量） | ✅ deliveryNo 回调参数 | 字面量（Write B）/ 弹窗回调（Write C） | A |
| **medicalProductStockBatctPoListJson** | ✅ JSON 字符串 | ✅ JSON 字符串 | ✅ JSON 字符串 | concatMedicalProductStock resolve 字符串 | A |
| 其它字段 | ❌ 无 | ❌ 无 | ❌ 无 | — | A |

### 15.2 严格表述（A 级）
- "3 Write 共同字段 = `medicalRecordId` + `medicalProductStockBatctPoListJson`"：**A**
- "Write A 唯一独有 = `toBeProcess`"：**A**
- "Write B / C 唯一独有 = `deliveryStatus` + `deliveryNo`"：**A**
- "Write B 与 Write C 差异 = `deliveryStatus` ('2' vs '1') + `deliveryNo` (undefined vs 回调)"：**A**

---

## 16. success 行为精确分层

### 16.1 Write A success（A 级，L35104-L35108）

```javascript
new ObjectFactory().saveOrQuery("/admin/setMedicalRecordProcessMode.json", { ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);
    }
    $scope.querySingleOrder();      // L35107
    $scope.queryUndisposed();      // L35108
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |
| 3 | `$scope.queryUndisposed()` | A |

### 16.2 Write B success（A 级，L35191-L35194）

```javascript
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);
    }
    $scope.querySingleOrder();      // L35194
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |
| 3 | （无 queryUndisposed） | A |

### 16.3 Write C success（A 级，L35210-L35213）

```javascript
new ObjectFactory().saveOrQuery("/admin/completeMedicalRecordDelivery.json", { ... }).then(function (result) {
    if (result.status) {
        return Popup.notice(result.errmsg);
    }
    $scope.querySingleOrder();      // L35213
});
```

| 步骤 | 行为 | A-F |
|---|---|---|
| 1 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | `$scope.querySingleOrder()` | A |
| 3 | （无 queryUndisposed） | A |

### 16.4 success 行为差异（A 级）

| 维度 | A | B | C |
|---|---|---|---|
| 错误处理 (Popup) | ✅ | ✅ | ✅ |
| querySingleOrder (Read) | ✅ | ✅ | ✅ |
| queryUndisposed (Read) | ✅ | ❌ | ❌ |
| reload | ❌ | ❌ | ❌ |
| state.go | ❌ | ❌ | ❌ |
| $scope.xxx 重置 | ❌ | ❌ | ❌ |
| modal 关闭 | ❌（popout_tip 自动关闭） | ❌ | ❌ |

**A 级结论**：
- 3 Write 共同 success 行为 = 错误弹窗 + querySingleOrder
- Write A 唯一额外行为 = queryUndisposed
- 3 Write **均无** $state.reload()（与 deliveryInputCtrl saveStock L4016 不同）

---

## 17. 与 F4 数据链（A 级）

```
F1 / selectOrderListFactory (OptFlow Read)
    ↓
$scope.selectOrderListFactory.items[index]  (单条订单，含 medicalRecord.medicalRecordType / medicalProductVoList[])
    ↓ HTML ng-click (F)
$scope.clickBtn(name, item, index)  (L35128)
    ↓
$scope.orderIndex = index  (L35130)
    ↓
fnMap[name]()  (L35225-L35226)
    ↓
[A] "加工" → choseFactoryMethod(item) (L35084)
    → medicalRecordType 映射 + jQuery 弹窗
    → concatMedicalProductStock(medical) (L35048)
        → F4 Request.medicalProductIdArray
        → [F 边界: F4 后端]
        → F4 result.list 消费
        → medicalProductStockBatctPoListJson 数组
        → JSON.stringify + Promise resolve
    → setMedicalRecordProcessMode { medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson } (L35099)
        → [F 边界: 后端]
        → success → querySingleOrder + queryUndisposed

[B] "到店取镜" → hint(2, fn) (L35148 模式)
    → popout_tip 弹窗
    → concatMedicalProductStock(item) (L35048)
    → completeMedicalRecordDelivery { medicalRecordId, deliveryStatus: "2", deliveryNo: undefined, medicalProductStockBatctPoListJson } (L35185)
        → [F 边界: 后端]
        → success → querySingleOrder

[C] "快递发货" → express(fn) (L35200)
    → popout_cb 弹窗
    → concatMedicalProductStock(item) (L35048)
    → completeMedicalRecordDelivery { medicalRecordId, deliveryStatus: "1", deliveryNo: <弹窗回调>, medicalProductStockBatctPoListJson } (L35204)
        → [F 边界: 后端]
        → success → querySingleOrder
```

---

## 18. 其它 Consumer

### 18.1 setMedicalRecordProcessMode.json（A 级）

| Controller | 调用行号 | A-F |
|---|---|---|
| optometryCtrl | L35099（**唯一**真实调用） | A |
| 其它 controller | 0 处 | A（已穷举 controller.js） |
| 7 HTML | 0 处 | A（已 grep） |

### 18.2 completeMedicalRecordDelivery.json（A 级）

| Controller | 调用行号 | A-F |
|---|---|---|
| optometryCtrl | L35185 / L35204（**2 处**真实调用） | A |
| 其它 controller | 0 处 | A（已穷举 controller.js） |
| 7 HTML | 0 处 | A（已 grep） |

### 18.3 concatMedicalRecordDelivery.json 之外？检查完整 delivery 关键词（A 级）

```
deliveryNo: 控制器内 2 处 (L35188/L35207)
deliveryStatus: 控制器内 2 处 (L35187/L35206)
completeDelivery / completeRecordDelivery: 控制器内仅 completeMedicalRecordDelivery.json 2 处
```

**A 级结论**：completeMedicalRecordDelivery 系列 API **仅 optometryCtrl 2 处**。

---

## 19. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | setMedicalRecordProcessMode 全局引用 | L35099 (controller.js 唯一) | A | L1 | |
| 02 | completeMedicalRecordDelivery 全局引用 | L35185/L35204 (controller.js 唯一 2 处) | A | L1 | |
| 03 | 三 Write Controller | optometryCtrl (L34776-L35382) | A | L1 | |
| 04 | 三 Write 函数 | choseFactoryMethod / clickBtn fnMap | A | L1 | |
| 05 | medicalRecordId A | `medical.medicalRecord.id` (L35085) | A | L1 | |
| 06 | medicalRecordId B | `item.medicalRecord.id` (L35182) | A | L1 | |
| 07 | medicalRecordId C | `item.medicalRecord.id` (L35201) | A | L1 | |
| 08 | 三者来源是否相同 | 表达式层同源（最终 selectOrderListFactory.items[index].medicalRecord.id） | A | L1 | |
| 09 | toBeProcess 初始化 | L35087 `{ 6: 1, 7: 0 }[medicalRecordType]` | A | L1 | |
| 10 | medicalRecordType 映射 | L35086-L35087 | A | L1 | |
| 11 | UI index 覆盖 | L35121 `toBeProcess = index` ($timeout jQuery) | A | L1 | |
| 12 | toBeProcess Write 使用 | L35101 | A | L1 | 仅 Write A |
| 13 | deliveryStatus "2" | L35187 字面量 | A | L1 | |
| 14 | deliveryStatus "1" | L35206 字面量 | A | L1 | |
| 15 | deliveryStatus 外部输入 | ❌ 0 处 | A | L1 | |
| 16 | deliveryNo undefined | L35188 字面量 | A | L1 | |
| 17 | deliveryNo callback | L35207 弹窗回调 | A | L1 | |
| 18 | express 来源 | L35032-L35046 | A | L1 | popout_cb 内部 F |
| 19 | 三 Write 分支关系 | 3 独立 action + fnMap 字典查找 | A | L1 | |
| 20 | concatMedicalProductStock 参数 | `item` / `medical`（同源 item 引用） | A | L1 | |
| 21 | Write 前置校验 | medicalProductStockBatctPoListJson (truthy) + F4 result (status + length) | A | L1 | |
| 22 | Write 前置 Read | F4 (concatMedicalProductStock 内) | A | L1 | success 后 Read 区分 |
| 23 | Write success A | error Popup + querySingleOrder + queryUndisposed | A | L1 | |
| 24 | Write success B/C | error Popup + querySingleOrder | A | L1 | 无 queryUndisposed |
| 25 | 重复提交防护 | ❌ 0 处 | A | L1 | Controller 层 |
| 26 | 三 Write 最小动作入口协议 | clickBtn fnMap → action 函数 → 弹窗 → concatMedicalProductStock → saveOrQuery | A | L1 | |

**统计**：
- **A：26 项（全部 A）**
- **F / E / D / B / C：0**
- **E/F 升 A：0**

---

## 20. L1/L2/L3

### L1（源码事实，可证）

- 3 Write API 调用点（A）
- 3 Write Request 字段（A）
- medicalRecordId 三处表达式来源（A）
- toBeProcess 5 处引用（A）
- deliveryStatus 2 处字面量（A）
- deliveryNo 2 处（A）
- $scope.hint / $scope.express 实现（A）
- clickBtn fnMap 11 个 key（A）
- concatMedicalProductStock 4 处引用（A）
- 校验点 7 处（A）
- success 行为（A）
- 0 处重复提交防护（A）

### L2（业务解释，未证）

- "加工 = 不加工/店内加工"：**E**（仅 L35088 弹窗文字 + L35101 注释）
- "deliveryStatus='1' = 快递发货"：**E**
- "deliveryStatus='2' = 到店取镜"：**E**
- "medicalRecordId = 数据库主键"：**E**
- "deliveryNo = 快递单号"：**E**（仅 $scope.express 弹窗文字"快递单号"）
- "medicalRecordType 6/7 业务含义"：**E**
- "clickBtn 由 ng-click 触发"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 setMedicalRecordProcessMode/completeMedicalRecordDelivery 后端实现）

---

## 21. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 3 Write 后端处理 | 无后端代码 | F |
| 3 Write Response schema | 无样本 | F |
| 3 Write 幂等性 | 无后端代码 | F |
| popout_tip / popout_cb 实现 | 无源码（window 全局函数） | F |
| 弹窗 res 实际值 | popout 实现不可得 | F（仅 res truthy 行为可证） |
| optometryCtrl HTML 模板 | 7 HTML 0 处 | F |
| clickBtn HTML ng-click | HTML 不可得 | F |
| UI 按钮 disabled 防重 | HTML 不可得 | F |
| selectOrderListFactory 何时被设置 | 需追溯到 optometryCtrl 入口初始化（L35367 ListFactory） | F（本轮范围） |
| medicalRecordType 业务含义 | 无业务字典 | F |
| deliveryStatus/deliveryNo 后端语义 | 无后端代码 | F |
| medicalRecordId 后端处理 | 无后端代码 | F |

---

## 22. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 3 Write + F4 + querySingleOrder + queryUndisposed 全部仅静态审计 |
| 3 Write 实际执行 = 0 | ✅ | setMedicalRecordProcessMode / completeMedicalRecordDelivery ×2 全部仅源码 |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 160 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 160_*.md |
| 文件编号连续 | ✅ | 159 已被 S1-98 占用，本轮使用 160 |

---

## 23. 最终结论

### 23.1 三 Write 动作入口最小协议（A 级）

```
HTML ng-click (F)
    ↓ clickBtn(name, item, index)
fnMap[name]()
    ↓
[A] "加工" → choseFactoryMethod(item) → popout_tip 弹窗 → concatMedicalProductStock → setMedicalRecordProcessMode
[B] "到店取镜" → hint(2, fn) → popout_tip 弹窗 → concatMedicalProductStock → completeMedicalRecordDelivery ("2")
[C] "快递发货" → express(fn) → popout_cb 弹窗 → concatMedicalProductStock → completeMedicalRecordDelivery ("1")
```

### 23.2 medicalRecordId 三处同源（A 级）

```
$scope.selectOrderListFactory.items[index].medicalRecord.id
    ↓ clickBtn 形参 item
    ↓
[A] item → medical → medicalRecordId (L35085)
[B] item → medicalRecordId (L35182)
[C] item → medicalRecordId (L35201)
```

### 23.3 toBeProcess 完整生命周期（A 级）

```
choseFactoryMethod(medical) 调用
    ↓ L35086
var medicalRecordType = medical.medicalRecord.medicalRecordType
    ↓ L35087
var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType]  // 初值
    ↓ L35090-35095
window.popout_tip 弹窗（同步）
    ↓ L35113-35124
$timeout jQuery click 监听（异步覆盖）
    ↓ toBeProcess = $(this).index()  // 0 或 1
    ↓ L35097
concatMedicalProductStock(medical).then(...)
    ↓ L35101
toBeProcess: toBeProcess  // 最终值
    ↓
setMedicalRecordProcessMode Request
```

### 23.4 deliveryStatus 入口（A 级）

- **"2" (L35187)** / **"1" (L35206)**：**字符串字面量**
- **0 处** 外部变量
- **0 处** 用户输入
- 唯一差异 = 触发动词 fnMap key（"到店取镜" / "快递发货"）

### 23.5 deliveryNo 入口（A 级）

- **Write B (L35188)** = `undefined` 字面量
- **Write C (L35207)** = popout_cb 弹窗回调参数 `deliveryNo`
- popout_cb 实现 **F 边界**（无仓库源码）
- ❌ 0 处 JS 层 deliveryNo 校验

### 23.6 S1-99 关键新发现

1. **3 Write 入口是 3 个完全独立 action**（A 级）— 不是 if/else 共享分支
2. **3 Write 通过 fnMap 字典查找路由**（A 级 L35225-L35226）
3. **3 Write medicalRecordId 表达式同源**（A 级）— 最终来自 selectOrderListFactory.items[index]
4. **toBeProcess 初值由 medicalRecordType 6/7 决定**（A 级）— 其它值 → undefined
5. **toBeProcess 通过 $timeout jQuery click 异步覆盖**（A 级）
6. **concatMedicalProductStock Promise 无 reject 分支**（A 级）— 异常未捕获
7. **3 Write 0 处字段级校验**（A 级）— medicalRecordId / deliveryStatus / deliveryNo 全部直接透传
8. **3 Write 共同 success 行为 + Write A 额外 queryUndisposed**（A 级）
9. **0 处重复提交防护**（A 级 Controller 层）

### 23.7 不可在本轮升级为 A 的项

- 3 Write 后端处理（F）
- popout_tip / popout_cb 内部实现（F）
- 3 Write 业务语义（E）
- medicalRecordId / deliveryNo / medicalRecordType 业务含义（E）
- optometryCtrl HTML 模板（F）
- UI 层防重（F）

---

**审计结束**。
