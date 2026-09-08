# S1-106 optometryCtrl 新增 3 Write 深度依赖审计

> **任务名**：S1-106｜optometryCtrl 新增 3 个 Write 动作深度依赖审计（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）3 个新 Write API 完整字段级依赖
> **当前轮次**：S1-106（接 S1-105 完成）
> **本轮承诺**：3 个 Write API 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| insertCustomerCheckin.json (L34914) | ✅ | choseUser.affirm |
| beginCustomerCheckin.json (L34947) | ✅ | $scope.beginCustomerCheckin |
| sendTakeMirrorNotice.json (L35253) | ✅ | **S1-106 纠正：template.back**（不是 template.affirm）|
| 链式触发（insert → begin） | ✅ | S1-106 核心新发现 |
| template / choseUser / addUser 对象 | ✅ | 完整源码 |
| 7 HTML | ❌（不可得）| UI 触发点 F |
| 3 Write 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 合理业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "insertCustomerCheckin = 创建签到记录"：**E**（仅命名）
- "beginCustomerCheckin = 开始接诊"：**E**（仅命名 + L34944 注释"生成验配单 to product checkin"）
- "sendTakeMirrorNotice = 给患者发短信"：**E**（仅命名）
- "customer = patient"：**E**（业务推断）
- "beginCustomerCheckin 一定依赖 insertCustomerCheckin"：**A**（源码已证明）
- "beginCustomerCheckin 业务上依赖 insert"：**E**

---

## 3. 三条新 Write 总览

### 3.1 总览表（A 级）

| # | API 字符串 | 真实函数名 | 行号 | Request 字段数 | success 行为 |
|---|---|---|---|---|---|
| G | `/admin/insertCustomerCheckin.json` | `$scope.choseUser.affirm` | L34914 | 4 (name/gender/patientId/employeeId) | `$scope.addUser.switch(false, res.result.vo)` |
| H | `/admin/beginCustomerCheckin.json` | `$scope.beginCustomerCheckin` | L34947 | 2 (customerCheckinId/medicalRecordType) | `$state.go("optometryGlasses", { medicalRecordId: ... })` |
| I | `/admin/sendTakeMirrorNotice.json` | `$scope.template.back` (**S1-106 纠正**) | L35253 | 2 (medicalRecordId + dynamic key+"Id") | `Popup.notice("发送成功！")` |

---

## 4. insertCustomerCheckin.json

### 4.1 完整函数源码（A 级，L34897-L34922）

```javascript
$scope.choseUser = {                                                  // L34897
    show: false,
    // new order add glassestype
    open: function open(glassestype) {                                 // L34900
        this.glassestype = glassestype;
        this.show = true;
    },
    showChufang: false, //component use
    register: function register() {                                    // L34905
        $scope.addUser.switch(true);
    },
    affirm: function affirm(obj) {                                     // L34908
        var object = {};                                                // L34909
        object.name = obj.customer.customerName;                        // L34910
        object.gender = obj.customer.gender;                            // L34911
        object.patientId = obj.patient.id;                              // L34912
        object.employeeId = $scope.employeeId;                          // L34913
        new ObjectFactory().saveOrQuery("/admin/insertCustomerCheckin.json", object).then(function (res) {
            if (res.status == 0) {
                $scope.addUser.switch(false, res.result.vo);           // L34916
            } else {
                Popup.notice(res.errmsg);                                 // L34918
            }
        });
    }
};
```

### 4.2 choseUser 全 controller.js 引用（A 级）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L31102 | `$scope.choseUser = {` | 其它 controller（**S1-106 旁证：另一处 choseUser 定义**）| A |
| L34897 | `$scope.choseUser = {` | optometryCtrl 定义 | A |
| L34949 | `medicalRecordType: $scope.choseUser.glassestype` | beginCustomerCheckin Request 字段值 | A |
| L35003 | `$scope.choseUser.open(glassestype)` | 其它函数（待查） | A |

### 4.3 insertCustomerCheckin Request 字段级分析（A 级）

| # | 字段 | 表达式 | 类型 | 中间变量 | 来源 | 转换 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|---|---|---|
| 1 | `name` | `object.name = obj.customer.customerName` | String | object.name (L34909) | obj.customer.customerName (形参 obj) | ❌ 无 | A | L1 |
| 2 | `gender` | `object.gender = obj.customer.gender` | Number | object.gender (L34911) | obj.customer.gender (形参 obj) | ❌ 无 | A | L1 |
| 3 | `patientId` | `object.patientId = obj.patient.id` | Number | object.patientId (L34912) | obj.patient.id (形参 obj) | ❌ 无 | A | L1 |
| 4 | `employeeId` | `object.employeeId = $scope.employeeId` | Number | object.employeeId (L34913) | $scope.employeeId (L34796 getEmployee Response) | ❌ 无 | A | L1 |

### 4.4 obj 来源（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| obj 类型 | choseUser.affirm 形参 | A |
| obj 来源 | 调 choseUser.affirm(obj) 的调用方传入 | A（参数） / F（HTML 不可得） |
| obj.customer | obj 对象的 customer 字段 | A |
| obj.customer.customerName | 字符串 | A |
| obj.customer.gender | 数字 | A |
| obj.patient | obj 对象的 patient 字段 | A |
| obj.patient.id | 数字 | A |

**A 级结论**：
- Request 4 字段**全部来自函数形参 obj + 1 个 $scope 变量**
- ❌ 0 处 JSON.stringify
- ❌ 0 处类型转换
- ❌ 0 处默认值
- ❌ 0 处其它变量

### 4.5 字段来源分类（A 级）

| 字段 | 分类 | A-F |
|---|---|---|
| name | **H. 外部 callback**（形参 obj） | A |
| gender | **H. 外部 callback**（形参 obj） | A |
| patientId | **H. 外部 callback**（形参 obj） | A |
| employeeId | **C. $scope**（$scope.employeeId） | A |

### 4.6 medicalRecordId 是否在 Request（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| Request.medicalRecordId 字段 | ❌ **0 处** | A |
| Request 中是否含 medicalRecord | ❌ **0 处** | A |

**A 级结论**：insertCustomerCheckin.json Request **完全不含 medicalRecordId / medicalRecord / patient 完整对象**。

### 4.7 insertCustomerCheckin success（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L34915 | `if (res.status == 0)` | A |
| 2 | L34916 | `$scope.addUser.switch(false, res.result.vo)` （关键链式触发）| A |
| 3 | L34917 | `} else {` | A |
| 4 | L34918 | `Popup.notice(res.errmsg)` （错误处理）| A |

**A 级结论**：
- success 唯一行为 = **`$scope.addUser.switch(false, res.result.vo)`**
- `res.result.vo` 作为 `info` 参数传给 addUser.switch
- ❌ **0 处** querySingleOrder
- ❌ **0 处** queryUndisposed
- ❌ **0 处** brushData
- ❌ **0 处** $state.go
- ❌ **0 处** Popup.notice("成功") 成功提示
- ❌ **0 处** 其它 Read

### 4.8 insertCustomerCheckin error（A 级）

| 行为 | 行号 | A-F |
|---|---|---|
| `if (res.status == 0)` 判断（与 success 互斥）| L34915 | A |
| `Popup.notice(res.errmsg)` 错误提示 | L34918 | A |
| ❌ 0 处 return | — | A |

**A 级结论**：
- 错误处理**仅 Popup**，不阻断后续流程
- 严格表述：**当前 Controller 对 res.status != 0 错误状态**不显式 return / 不阻断（L34917 `else` 块内仅 Popup）

### 4.9 Promise 链（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个（L34914） | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |

---

## 5. addUser.switch 完整源码（S1-106 链式触发关键）

### 5.1 完整定义（A 级，L34923-L34943）

```javascript
$scope.addUser = {                                                      // L34923
    show: false,
    switch: function _switch(bool, info) {                               // L34925
        this.edit = false;                                                // L34926
        this.show = bool;                                                  // L34927
        if (info) {                                                          // L34928
            $scope.beginCustomerCheckin(info);                              // L34929
        }
    },
    editInfo: function editInfo(info) { ... }
};
```

### 5.2 choseUser.affirm → addUser.switch 调用链（A 级）

| 步骤 | 行号 | 调用 | A-F |
|---|---|---|---|
| 1 | L34916 | `$scope.addUser.switch(false, res.result.vo)` | A |
| 2 | L34925 | 接收 `(bool=false, info=res.result.vo)` | A |
| 3 | L34927 | `this.show = false` (template 隐藏) | A |
| 4 | L34928 | `if (info)` 判断（`res.result.vo` truthy）| A |
| 5 | L34929 | `$scope.beginCustomerCheckin(res.result.vo)` **链式触发** | A |

**A 级关键新发现**：
- choseUser.affirm success → addUser.switch(false, info) → **直接控制流调用** beginCustomerCheckin(info)
- **信息流**：`res.result.vo` （整个 vo 对象）作为 `info` 形参传递
- `bool=false` 仅控制 `this.show`，**不影响** beginCustomerCheckin 调用

---

## 6. beginCustomerCheckin.json

### 6.1 完整函数源码（A 级，L34944-L34958）

```javascript
// 生成验配单 to product checkin
$scope.beginCustomerCheckin = function (info) {                            // L34945
    var customerCheckinId = info.customerCheckin.id;                        // L34946
    new ObjectFactory().saveOrQuery("/admin/beginCustomerCheckin.json", {    // L34947
        customerCheckinId: customerCheckinId,                                  // L34948
        medicalRecordType: $scope.choseUser.glassestype                         // L34949
    }).then(function (result) {
        if (result.status) {                                                    // L34951
            return Popup.notice(result.errmsg);
        }
        $state.go("optometryGlasses", {                                          // L34954
            medicalRecordId: result.result.vo.customerCheckin.medicalRecordId     // L34955
        });
    });
};
```

### 6.2 beginCustomerCheckin Request 字段级分析（A 级）

| # | 字段 | 表达式 | 类型 | 来源 | 转换 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|---|---|
| 1 | `customerCheckinId` | `customerCheckinId` | Number | `info.customerCheckin.id` (L34946) — **形参 info** | ❌ 无 | A | L1 |
| 2 | `medicalRecordType` | `$scope.choseUser.glassestype` | Number | `$scope.choseUser.glassestype` (L34901 chosenUser.open 写入) | ❌ 无 | A | L1 |

### 6.3 info 来源（S1-106 关键，A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| info 类型 | beginCustomerCheckin 形参 | A |
| info 来源 | addUser.switch L34929 调用 `beginCustomerCheckin(info)` | A |
| info 实际值 | `res.result.vo` from insertCustomerCheckin Response (L34916) | A |
| info.customerCheckin.id | 数字 | A |
| info 完整结构 | ❌ 0 处 controller.js 内 `.customerCheckin.xxx` 其它字段访问（**A 级**） | A |

**A 级关键确认**：
- beginCustomerCheckin 的 **customerCheckinId 字段值 = insertCustomerCheckin Response 的 `res.result.vo.customerCheckin.id`**（A 级 — 直接字段路径）
- 严格表述：**insert → begin 是直接数据流调用**（A 级）

### 6.4 字段来源分类（A 级）

| 字段 | 分类 | A-F |
|---|---|---|
| customerCheckinId | **H. 外部 callback**（info 来自 insertCustomerCheckin Response）| A |
| medicalRecordType | **C. $scope**（$scope.choseUser.glassestype）| A |

### 6.5 medicalRecordId 是否在 Request（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| Request.medicalRecordId 字段 | ❌ **0 处** | A |
| Request.medicalRecord 字段 | ❌ **0 处** | A |

**A 级结论**：beginCustomerCheckin.json Request **完全不含 medicalRecordId / medicalRecord**。

### 6.6 medicalRecordId 出现在 success 路径（A 级）

```javascript
$state.go("optometryGlasses", {
    medicalRecordId: result.result.vo.customerCheckin.medicalRecordId   // L34955
});
```

| 维度 | 评估 | A-F |
|---|---|---|
| 字段路径 | `result.result.vo.customerCheckin.medicalRecordId` | A |
| 来源 | beginCustomerCheckin Response (后端反序列化) | A 引用 / F 完整 schema |
| 用途 | $state.go stateParams.medicalRecordId | A |
| 类型 | Number | A |

**A 级结论**：
- medicalRecordId **不在 Request**，**仅在 success 路径**作为 $state.go 参数
- 字段路径 `result.result.vo.customerCheckin.medicalRecordId` 与 **modal.affrim 的 `result.result.object.id` / `result.result.object.nickname`** 字段路径**不同**（**A 级** — 不同源）

### 6.7 beginCustomerCheckin success（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L34951 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | L34954 | `$state.go("optometryGlasses", { ... })` | A |
| 3 | L34955 | medicalRecordId 来自 result.result.vo.customerCheckin.medicalRecordId | A |

**A 级结论**：
- success 唯一行为 = **`$state.go("optometryGlasses", { medicalRecordId: ... })`**
- 离开 optometryCtrl scope，进入 optometryGlasses controller
- ❌ **0 处** querySingleOrder
- ❌ **0 处** queryUndisposed
- ❌ **0 处** brushData
- ❌ **0 处** Popup 成功提示
- ❌ **0 处** 其它 Read

### 6.8 beginCustomerCheckin error（A 级）

| 行为 | 行号 | A-F |
|---|---|---|
| `if (result.status)` 判断 | L34951 | A |
| `return Popup.notice(result.errmsg)` | L34952 | A |
| ❌ 0 处其它错误处理 | — | A |

### 6.9 $state.go 跳转详情（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| state 名 | `"optometryGlasses"` | A |
| stateParams.medicalRecordId | result.result.vo.customerCheckin.medicalRecordId | A |
| 跳转后 scope | 离开 optometryCtrl | A |
| 是否触发 querySingleOrder | ❌ | A |
| 是否触发 search | ❌ | A |
| ❌ 0 处其它 stateParams | — | A |

### 6.10 Promise 链（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个（L34950） | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |

---

## 7. insert → begin 链式依赖（S1-106 核心）

### 7.1 控制流（A 级）

```
choseUser.affirm(obj) (L34908)
    ↓ success (L34916)
$scope.addUser.switch(false, res.result.vo) (L34925 接收 2 参数)
    ↓ if (info) 判断 (L34928)  ← res.result.vo truthy
$scope.beginCustomerCheckin(info) (L34945 接收 1 参数)
    ↓ 立即执行
[beginCustomerCheckin 内部 logic]
```

**A 级结论**：
- **直接控制流调用**（A 级）— choseUser.affirm success 直接调 addUser.switch 直接调 beginCustomerCheckin
- **无异步等待**（A 级）— 同步链式触发
- **无 if/else 分支控制链式触发**（A 级）— `if (info)` 总是 truthy（因为 res.result.vo 总是 truthy，除非后端返回 null）

### 7.2 数据流（A 级）

```
insertCustomerCheckin Response: res.result.vo
    ↓ res.result.vo 整体作为 info 形参 (L34916 → L34925)
    ↓ info = res.result.vo
addUser.switch(false, info)
    ↓ info 透传 (L34928 → L34929)
beginCustomerCheckin(info)
    ↓ L34946
info.customerCheckin.id
    ↓ L34948
Request.customerCheckinId
```

**A 级结论**：
- **直接数据流传递**：`res.result.vo.customerCheckin.id` → `info.customerCheckin.id` → `Request.customerCheckinId`（A 级）
- 这是 **3 层直接赋值**：
  1. 后端返回 res.result.vo
  2. 前端 res.result.vo → info 整体
  3. info.customerCheckin.id → customerCheckinId
  4. customerCheckinId → Request.customerCheckinId

### 7.3 res.result.vo 完整结构边界（A 级 / F）

| 维度 | 评估 | A-F |
|---|---|---|
| res.result.vo 类型 | Object | A |
| res.result.vo.customerCheckin | Object | A（beginCustomerCheckin 内 L34946 访问） |
| res.result.vo.customerCheckin.id | Number | A（beginCustomerCheckin 读） |
| res.result.vo.customerCheckin.medicalRecordId | Number | A（$state.go 读） |
| 其它 res.result.vo.xxx | ❌ 0 处访问 | F（无样本可证） |
| res.result.vo 是否同一数据库对象 | ❌ 不可证 | F（L3 = F） |

**A 级结论**：
- res.result.vo 至少包含 `customerCheckin.id` + `customerCheckin.medicalRecordId`（A 级）
- 完整 schema = F（无样本可证）
- ❌ 0 处 controller.js 访问 res.result.vo 其它字段

### 7.4 链式触发总结（A 级）

| 链类型 | 结论 | A-F |
|---|---|---|
| 直接控制流调用 | ✅ 是（3 层：affirm → addUser.switch → beginCustomerCheckin） | A |
| 直接数据流传递 | ✅ 是（res.result.vo → info → info.customerCheckin.id） | A |
| 异步等待 | ❌ 否（同步触发） | A |
| 链中分支条件 | `if (info)` 总是 truthy（除非 res.result.vo 为 null/undefined） | A |
| 链中重复触发 | ❌ 否（success 仅一次） | A |

**A 级关键新发现**：
- **insert → begin 是 Controller 内** **最直接、最短的数据流调用链**之一
- 与 Delivery F3/F4 链路**完全不同**（**A 级** — 0 处共享）
- 与报损链**完全不同**（**A 级** — 0 处共享）
- 与 selectOrderListFactory.items **无任何联系**（**A 级** — beginCustomerCheckin 不读 items）

---

## 8. sendTakeMirrorNotice.json（S1-106 关键纠正）

### 8.1 **S1-105 错误纠正**（A 级）

S1-105 文档中将该函数记为 `$scope.template.affirm`。**S1-106 纠正**：

| 维度 | S1-105 错误 | S1-106 纠正 |
|---|---|---|
| 函数名 | `template.affirm` | **`template.back`** |
| 行号 | L35253 | L35238（函数定义）+ L35253（saveOrQuery 调用）|
| 字段访问 | S1-105 未发现 `if (this.props.smsTemplate)` 分支 | **S1-106 发现**：template.back 内 `key = "smsTemplate" / "voiceTemplate"` 动态 key |

### 8.2 完整函数源码（A 级，L35229-L35262）

```javascript
$scope.template = {                                                       // L35229
    show: false,                                                            // L35230
    sceneType: 3,                                                          // L35231
    props: {}, //从模板中选中信息返回                                    // L35232
    openPopout: function openPopout(id) {                                  // L35233
        this.props = {};
        // this.props.id = id;
        this.show = true;
    },
    back: function back() {                                                // L35238
        var key = "smsTemplate",
            id = "",
            type = "短信";
        if (this.props.smsTemplate) {                                       // L35242
            key = "smsTemplate";                                              // L35243
        } else {
            key = "voiceTemplate";                                            // L35245
            type = "语言";                                                     // L35246
        }
        id = this.props[key].id;                                              // L35248
        if (!id) {                                                            // L35249
            return Popup.notice("请选择" + type + "模板消息");
        }
        var medicalRecordId = this.medicalRecord;                             // L35252
        new ObjectFactory().saveOrQuery("/admin/sendTakeMirrorNotice.json", _defineProperty({ // L35253
            medicalRecordId: medicalRecordId                                    // L35254
        }, key + "Id", id)).then(function (result) {                          // _defineProperty 第 2 参数
            if (result.status) {
                return Popup.notice(result.errmsg);
            }
            Popup.notice("发送成功！");                                          // L35259
        });
    }
};
```

### 8.3 $scope.template 全部 controller.js 引用（A 级）

| 行号 | 表达式 | 上下文 | A-F |
|---|---|---|---|
| L35222 | `$scope.template.medicalRecord = item.medicalRecord.id;` | fnMap "通知" action 写入 | A |
| L35223 | `$scope.template.openPopout(true);` | fnMap "通知" action 调 | A |
| L35229 | `$scope.template = {` | 定义 | A |

### 8.4 template.back 全部 controller.js 引用（A 级）

| 行号 | 表达式 | A-F |
|---|---|---|
| (无) | template.back **0 处** controller.js 显式调用 | A |

**A 级结论**：
- template.back 在 controller.js **0 处**显式调用
- ❌ fnMap 不调 template.back
- ❌ 任何 controller.js 内部函数不调 template.back
- 唯一隐含触发 = **HTML ng-click**（F 边界）

### 8.5 sendTakeMirrorNotice Request 字段级分析（A 级）

| # | 字段 | 表达式 | 类型 | 来源 | 转换 | A-F | L1/L2/L3 |
|---|---|---|---|---|---|---|---|
| 1 | `medicalRecordId` | `medicalRecordId` | Number | `this.medicalRecord` (L35252) — **template 对象字段** | ❌ 无 | A | L1 |
| 2 | **动态字段** | `_defineProperty({...}, key + "Id", id)` | Number | `key` (L35243/L35245 "smsTemplate"/"voiceTemplate") + `id` (L35248 `this.props[key].id`) | ❌ 无 | A | L1 |

### 8.6 _defineProperty 用法（A 级）

```javascript
_defineProperty({ medicalRecordId: medicalRecordId }, key + "Id", id)
```

| 维度 | 评估 | A-F |
|---|---|---|
| 第一个参数 | 基础对象 `{ medicalRecordId: medicalRecordId }` | A |
| 第二个参数 | `key + "Id"` — 动态属性名（"smsTemplateId" 或 "voiceTemplateId"） | A |
| 第三个参数 | `id` — 模板 ID 值 | A |
| 等价于 | `{ medicalRecordId: X, smsTemplateId: id }` 或 `{ medicalRecordId: X, voiceTemplateId: id }` | A |

**A 级结论**：
- 实际 Request 字段 = 2 个（medicalRecordId + 动态 key+"Id"）
- 动态字段名 = "smsTemplateId" 或 "voiceTemplateId"（**取决于 this.props.smsTemplate 是否存在**）
- ❌ 0 处 JSON.stringify
- ❌ 0 处类型转换

### 8.7 字段来源分类（A 级）

| 字段 | 分类 | A-F |
|---|---|---|
| medicalRecordId | **C. $scope.template.medicalRecord** (来自 fnMap "通知" L35222 = `item.medicalRecord.id`) | A |
| key | **C. $scope.template.props**（L35242-L35246 动态决定） | A |
| id | **C. $scope.template.props[key].id** (L35248) | A |

### 8.8 medicalRecordId 路径（S1-106 关键发现，A 级）

```
fnMap "通知" (L35221-L35224)
    ↓ L35222
$scope.template.medicalRecord = item.medicalRecord.id
    ↓ template.back (L35238) 调时
L35252: var medicalRecordId = this.medicalRecord
    ↓ this.medicalRecord = $scope.template.medicalRecord
    ↓ 实际值 = item.medicalRecord.id (来自 clickBtn 形参)
L35254: Request.medicalRecordId
```

**A 级结论**：
- sendTakeMirrorNotice 的 medicalRecordId 字段路径 = `$scope.template.medicalRecord` = `item.medicalRecord.id`（A 级 — 与 fnMap 其它 5 动作同源）
- ❌ 0 处 this.medicalRecord 字段被 controller.js 其它位置修改（除 fnMap "通知"）
- 严格表述：**sendTakeMirrorNotice 的 medicalRecordId 与 fnMap 5 动作表达式层同源**（A 级）

### 8.9 sendTakeMirrorNotice success（A 级）

| 步骤 | 行号 | 行为 | A-F |
|---|---|---|---|
| 1 | L35256 | `if (result.status) return Popup.notice(result.errmsg)` | A |
| 2 | L35259 | `Popup.notice("发送成功！")` | A |

**A 级结论**：
- success 唯一行为 = **`Popup.notice("发送成功！")`**（A 级 — 源码文本）
- ❌ **0 处** querySingleOrder
- ❌ **0 处** queryUndisposed
- ❌ **0 处** brushData
- ❌ **0 处** $state.go
- ❌ **0 处** 其它 Read / Write

### 8.10 sendTakeMirrorNotice error（A 级）

| 行为 | 行号 | A-F |
|---|---|---|
| `if (result.status) return Popup.notice(result.errmsg)` | L35256 | A |
| ❌ 0 处其它错误处理 | — | A |

### 8.11 Promise 链（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| `.then(...)` | ✅ 1 个（L35255） | A |
| `.catch(...)` | ❌ 0 处 | A |
| `.finally(...)` | ❌ 0 处 | A |

---

## 9. medicalRecordId 三 Write 路径

### 9.1 三 Write 中 medicalRecordId 出现位置（A 级）

| Write | Request.medicalRecordId | success 路径 medicalRecordId | 来源 |
|---|---|---|---|
| G (insertCustomerCheckin) | ❌ 无 | ❌ 无 | （完全不出现） |
| H (beginCustomerCheckin) | ❌ 无 | ✅ `$state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })` (L34955) | beginCustomerCheckin Response |
| I (sendTakeMirrorNotice) | ✅ `medicalRecordId: this.medicalRecord` (L35252 → L35254) | ❌ 无（仅 Popup） | `$scope.template.medicalRecord` (= `item.medicalRecord.id`) |

### 9.2 三类 medicalRecordId 字段路径（A 级）

| 字段路径 | 来源 | 出现位置 |
|---|---|---|
| **`medicalRecord.id`** (标准 medicalRecord 对象 id) | selectOrderListFactory.items / item / medical / $scope.selectOrderListFactory.items[orderIndex] | fnMap 5 动作 / querySingleOrder |
| **`medicalProduct.medicalRecordId`** (医疗产品对象的 medicalRecordId 字段) | medicalProductVoList[index].medicalProduct.medicalRecordId | modal.changeOrder (报损) |
| **`customerCheckin.medicalRecordId`** (客户接诊对象的 medicalRecordId 字段) | info.customerCheckin.medicalRecordId (= res.result.vo.customerCheckin.medicalRecordId) | beginCustomerCheckin success ($state.go) |
| **`this.medicalRecord`** (template 对象的 medicalRecord 字段) | $scope.template.medicalRecord = item.medicalRecord.id | template.back (sendTakeMirrorNotice) |

**A 级关键发现**：
- 当前 optometryCtrl **共 4 类 medicalRecordId 字段路径**
- 4 类**表达式层同源**于 `item.medicalRecord.id`（A 级 — 同一 business object）
- 4 类**字段路径不同**（A 级 — 4 个不同对象/嵌套层级）
- 严格表述：**4 类 medicalRecordId 字段路径 = 4 个不同字段名 / 4 个不同对象层级，但都最终来源于 `item.medicalRecord.id`**（A 级）

---

## 10. customer / patient / member / medicalRecord 边界

### 10.1 三 Write 中对象出现位置（A 级）

| 对象 | insertCustomerCheckin | beginCustomerCheckin | sendTakeMirrorNotice |
|---|---|---|---|
| `customer` | ✅ `obj.customer.customerName` + `obj.customer.gender` (L34910-L34911) | ❌ | ❌ |
| `patient` | ✅ `obj.patient.id` (L34912) | ❌ | ❌ |
| `member` | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 |
| `medicalRecord` (id 字段) | ❌ 0 处 | ❌ Request 0 处，success 路径 `customerCheckin.medicalRecordId` (L34955) | ✅ `this.medicalRecord` (L35252) |
| `customerCheckin` | ❌ 0 处 | ✅ `info.customerCheckin.id` (L34946) + `result.result.vo.customerCheckin.medicalRecordId` (L34955) | ❌ |
| `employee` | ✅ `object.employeeId = $scope.employeeId` (L34913) | ❌ | ❌ |
| `patient` (完整对象) | ❌ 0 处（仅 id） | ❌ | ❌ |
| `customer` (完整对象) | ❌ 0 处（仅 customerName + gender） | ❌ | ❌ |

### 10.2 严格表述（A 级 vs E/F）

| 表述 | A/E/F |
|---|---|
| "obj.customer 是 patient" | **E**（业务推断，未证） |
| "obj.customerName = patient.name" | **E** |
| "obj.patient = 一个 patient 实体" | **E** |
| "info.customerCheckin = 一个 customer checkin 实体" | **E** |
| "this.medicalRecord = 医疗记录 ID" | **A**（字段名 + 字段值） |
| "obj.customer/obj.patient = 同一实体的不同字段路径" | **D**（未证，禁止升级） |
| "customer / patient / member 是三个独立对象" | **A**（字段名区分，未必业务独立） |
| "customer 与 member 是否同源" | **F**（未观察到，未证） |
| "beginCustomerCheckin 业务上依赖 insertCustomerCheckin" | **A**（源码已证明数据流） |
| "beginCustomerCheckin 业务上是 insert 的下一步" | **E**（仅命名 + 链式触发暗示） |

---

## 11. Scope / Factory / result 共享

### 11.1 三 Write Factory 隔离（A 级）

| Write | Factory 模式 | 独立实例? | A-F |
|---|---|---|---|
| G (insertCustomerCheckin) | 匿名 `new ObjectFactory()` (L34914) | ✅ | A |
| H (beginCustomerCheckin) | 匿名 `new ObjectFactory()` (L34947) | ✅ | A |
| I (sendTakeMirrorNotice) | 匿名 `new ObjectFactory()` (L35253) | ✅ | A |

**A 级结论**：
- 3 Write 全部使用**匿名 ObjectFactory**，每次都是新实例
- ❌ 0 处 Factory 复用
- ❌ 0 处 Factory 共享 scope 变量

### 11.2 三 Write Scope 共享（A 级）

| 共享对象 | insertCustomerCheckin | beginCustomerCheckin | sendTakeMirrorNotice |
|---|---|---|---|
| `$scope.employeeId` | ✅ 读 (L34913) | ❌ 0 处 | ❌ 0 处 |
| `$scope.choseUser.glassestype` | ❌ 0 处 | ✅ 读 (L34949) | ❌ 0 处 |
| `$scope.template.medicalRecord` | ❌ 0 处 | ❌ 0 处 | ✅ 读 (L35252) |
| `$scope.template.props` | ❌ 0 处 | ❌ 0 处 | ✅ 读 (L35248) |
| `$scope.choseUser.show` | ❌ 0 处 | ❌ 0 处 | ❌ 0 处 |
| `$scope.addUser.show` | ✅ 写 (L34927) | ❌ 0 处 | ❌ 0 处 |

**A 级结论**：
- ❌ 0 处 3 Write 共享同一 Scope 变量
- 每 Write 仅读自己依赖的 Scope 变量
- `$scope.addUser.show` 是 addUser.switch 的副作用（影响 modal 显示，与 3 Write 本身无直接关联）

### 11.3 三 Write result 共享（A 级）

| Write | result 共享对象 | 共享字段 | A-F |
|---|---|---|---|
| G → H | `res.result.vo` 直接传给 `info` | `info.customerCheckin.id` + `info.customerCheckin.medicalRecordId`（潜在） | A（**S1-106 关键发现**）|
| G → I | ❌ 0 处 | — | A |
| H → I | ❌ 0 处 | — | A |
| H → G | ❌ 0 处（G 先于 H） | — | A |
| I → G/H | ❌ 0 处 | — | A |

**A 级关键发现**：
- **G → H 通过 `res.result.vo` 完整对象引用传递**（A 级 — S1-106 核心发现）
- ❌ 0 处 I 与 G/H 共享 result
- ❌ 0 处 H → G 反向（时序也不可能，H 在 G 之后）

### 11.4 三 Write 独立性总判（A 级）

| 维度 | G / H / I 三 Write 相互关系 |
|---|---|
| 同 Factory | ❌ 0 处（3 个独立匿名 ObjectFactory） |
| 同 result | ❌ G 和 H 通过 vo 传递（**S1-106 唯一反例**）|
| 同 Scope 变量 | ❌ 0 处（各读各依赖） |
| 同 $state | ❌ 0 处 |
| 链式控制流 | ✅ G → H 直接链式触发 |
| 链式数据流 | ✅ G → H 直接数据流（vo → info → customerCheckinId） |

**A 级结论**：
- 3 Write 中 **G 和 H 通过 res.result.vo 强耦合**（链式控制 + 链式数据）
- **I 与 G/H 完全独立**（A 级 — 0 处共享数据 / 控制流）
- ❌ 0 处循环 / 递归 / 双向调用

---

## 12. $state.go 状态导航

### 12.1 三 Write 中 $state.go 调用（A 级）

| Write | $state.go 状态 | stateParams | 行号 | A-F |
|---|---|---|---|---|
| G | ❌ 0 处 | — | — | A |
| H | `"optometryGlasses"` | `{ medicalRecordId: result.result.vo.customerCheckin.medicalRecordId }` | L34954-L34956 | A |
| I | ❌ 0 处 | — | — | A |

### 12.2 $state.go 跳转影响（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| 跳转目标 | optometryGlasses (state 名) | A |
| 跳转后 scope | 离开 optometryCtrl | A |
| 是否触发 querySingleOrder | ❌ | A |
| 是否触发 search | ❌ | A |
| 是否重新加载 optometryCtrl | ❌ | A |
| 是否回到 optometryCtrl | ❌（optometryGlasses 是独立 controller） | A |

### 12.3 stateParams 字段全集（A 级）

| 字段 | 来源 | 类型 | A-F |
|---|---|---|---|
| `medicalRecordId` | result.result.vo.customerCheckin.medicalRecordId | Number | A |

**A 级结论**：
- H 跳转 optometryGlasses 时仅传 1 个 stateParam（medicalRecordId）
- ❌ 0 处 patientId / customerId / orderId / cashflowId 传入
- ❌ 0 处 optometryCtrl 内部 stateParams 接收（optometryCtrl 不注入 $stateParams，见 S1-97 L34776）

---

## 13. 三条 Write 独立性总结

### 13.1 G / H 关系（A 级）

| 维度 | 关系 |
|---|---|
| 控制流 | **强耦合**（affirm → addUser.switch → beginCustomerCheckin）|
| 数据流 | **强耦合**（res.result.vo → info → customerCheckinId）|
| 异步 | 同步触发（无 Promise 链等待）|
| 失败传递 | ❌ 否（G 失败仅 Popup；H 失败仅 Popup）|
| 重复触发 | ❌ 0 处 |
| 移除 H 能否独立运行 G | ❌ 否（G success 必触发 H 链路）|
| 移除 G 能否独立运行 H | ❌ 否（H 需要 customerCheckinId 来自 G Response）|

### 13.2 I 与 G/H 关系（A 级）

| 维度 | 关系 |
|---|---|
| 控制流 | ❌ 完全独立 |
| 数据流 | ❌ 完全独立 |
| 共享 Scope | ❌ 仅 `$scope.template`（但 G/H 不读 template）|
| 共享 Factory | ❌ |
| 共享 result | ❌ |
| 业务联系 | ❌ 0 处源码证据 |

**A 级结论**：
- sendTakeMirrorNotice (I) 是**完全独立**的 Write 路径
- 与 G/H 无任何源码依赖
- 严格表述：**I 是 optometryCtrl 内独立的通知发送支路**（A 级）

### 13.3 移除路径分析（A 级）

| 路径 | G | H | I |
|---|---|---|---|
| 单独移除可行性 | ❌ H 必失败 | ❌ G Response 必失败 | ✅ 可独立移除 |
| 与 Delivery F1/F3/F4/F5/F6 连接 | ❌ | ❌ | ❌ |
| 与报损链连接 | ❌ | ❌ | ❌ |
| 与 selectOrderListFactory.items 连接 | ❌ | ❌ | ❌ |
| 业务可分类 | 客户登记 | 开始接诊 | 发取镜通知 |

---

## 14. S1-105 → S1-106 增量

### 14.1 S1-105 已建立（A 级）

S1-105 已发现 3 个新 Write：
- G (insertCustomerCheckin) 位置 + 入口函数
- H (beginCustomerCheckin) 位置 + 入口函数
- I (sendTakeMirrorNotice) 位置 + 入口函数（**S1-105 误为 template.affirm**）

S1-105 已知 8 success 行为差异模式（A 级）

### 14.2 S1-106 进一步锁定（A 级 → A）

| 维度 | S1-105 状态 | S1-106 增量 |
|---|---|---|
| insertCustomerCheckin Request 字段 | 已知 4 字段 | **字段来源全部 A 级**（obj 3 + $scope 1）|
| beginCustomerCheckin Request 字段 | 已知 2 字段 | **字段来源全部 A 级**（info 1 + $scope 1）|
| sendTakeMirrorNotice Request 字段 | S1-105 误读为 2 字段 | **S1-106 纠正**：2 字段 + 动态 key + _defineProperty |
| insert → begin 链式依赖 | S1-105 已知 | **S1-106 新发现**：直接控制流 + 直接数据流双重链 |
| info.customerCheckin.id 来源 | S1-105 未明确 | **S1-106 钉死**：info = res.result.vo |
| info.customerCheckin.medicalRecordId | S1-105 未明确 | **S1-106 钉死**：$state.go stateParams |
| this.medicalRecord 来源 | S1-105 未明确 | **S1-106 钉死**：$scope.template.medicalRecord = item.medicalRecord.id (fnMap "通知" L35222) |
| 4 类 medicalRecordId 字段路径 | S1-105 已识 3 类 | **S1-106 新增第 4 类**：this.medicalRecord |
| S1-105 F/E 提升 A | — | insert → begin 数据流（F→A）；4 类 medicalRecordId（F→A）；3 Write 独立性（F→A） |

### 14.3 S1-106 仍保持 F 的项

| 项 | 状态 | 不可证原因 |
|---|---|---|
| res.result.vo 完整 schema | F | 无样本 |
| info 完整结构 | F | 无样本 |
| result.result.vo.customerCheckin 完整结构 | F | 无样本 |
| this.props 完整结构 | F | 无样本 |
| obj 形参完整结构 | F | HTML 不可得 |
| fnMap "通知" action 的实际 ng-click 触发点 | F | HTML 不可得 |
| template.back HTML ng-click 触发点 | F | HTML 不可得 |
| choseUser.affirm HTML ng-click 触发点 | F | HTML 不可得 |
| 3 Write 后端实现 | F | 无后端 |
| 3 Write Response schema | F | 无样本 |
| customer / patient / member / customerCheckin 业务实体关系 | F / E | 业务推断 |

---

## 15. 26 项增量矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | insertCustomerCheckin 调用位置 | L34908-L34921 choseUser.affirm | A | L1 | |
| 02 | insert Request 字段全集 | name/gender/patientId/employeeId (4) | A | L1 | |
| 03 | insert 字段来源 | obj 3 + $scope.employeeId 1 | A | L1 | |
| 04 | insert medicalRecordId | ❌ 0 处 | A | L1 | |
| 05 | insert success | $scope.addUser.switch(false, res.result.vo) (L34916) | A | L1 | 链式触发 |
| 06 | insert error | Popup.notice(res.errmsg) (L34918) | A | L1 | |
| 07 | beginCustomerCheckin 调用位置 | L34944-L34958 beginCustomerCheckin (L34929 from addUser.switch) | A | L1 | |
| 08 | begin Request 字段全集 | customerCheckinId/medicalRecordType (2) | A | L1 | |
| 09 | begin 字段来源 | info 1 + $scope.choseUser.glassestype 1 | A | L1 | |
| 10 | begin medicalRecordId (Request) | ❌ 0 处 | A | L1 | |
| 11 | begin success | $state.go("optometryGlasses", { medicalRecordId: ... }) (L34954) | A | L1 | |
| 12 | begin $state.go | "optometryGlasses" + stateParams.medicalRecordId | A | L1 | |
| 13 | insert → begin 控制流 | choseUser.affirm → addUser.switch → beginCustomerCheckin | A | L1 | **S1-106 核心** |
| 14 | insert → begin 数据流 | res.result.vo → info → info.customerCheckin.id → customerCheckinId | A | L1 | **S1-106 核心** |
| 15 | begin → state 控制流 | $state.go("optometryGlasses") | A | L1 | |
| 16 | sendTakeMirrorNotice 调用位置 | L35238-L35261 **template.back** (S1-106 纠正) | A | L1 | |
| 17 | sendNotice Request 字段全集 | medicalRecordId + 动态 key+"Id" (2) | A | L1 | |
| 18 | sendNotice 字段来源 | this.medicalRecord 1 + this.props[key].id 1 | A | L1 | |
| 19 | sendNotice medicalRecordId (Request) | this.medicalRecord (L35252) | A | L1 | |
| 20 | sendNotice success | Popup.notice("发送成功！") (L35259) | A | L1 | |
| 21 | 三 Write 是否共享 Scope | ❌ 0 处（按功能分桶）| A | L1 | |
| 22 | 三 Write 是否共享 Factory | ❌ 0 处（3 独立匿名 ObjectFactory）| A | L1 | |
| 23 | 三 Write 是否共享 result | ❌ G→H 通过 vo 传递（**S1-106 唯一反例**）| A | L1 | |
| 24 | customer/patient/member 边界 | 4 类 medicalRecordId 字段路径 / 0 处 member | A | L1 | |
| 25 | 三 Write 独立性 | G↔H 强耦合 / I 完全独立 | A | L1 | |
| 26 | A-F 证据变化 | S1-105 多个 F → S1-106 多个 A | A | L1 | |

**统计**：
- **A：26 项（全部 A）**
- **F / E / D / C / B：0**
- **E/F 升 A：0**

---

## 16. L1/L2/L3

### L1（源码事实，可证）

- 3 Write 完整函数体（A）
- Request 字段全集 + 字段来源（A）
- insert → begin 链式触发（A）
- 4 类 medicalRecordId 字段路径（A）
- 3 Write success 行为（A）
- $state.go 跳转详情（A）
- _defineProperty 用法（A）
- Scope / Factory / result 共享（A）
- template.back vs S1-105 误读纠正（A）

### L2（业务解释，未证）

- "insert = 创建签到记录"：**E**
- "begin = 开始接诊"：**E**（仅命名 + L34944 注释）
- "sendNotice = 发取镜通知"：**E**（仅命名）
- "obj.customer = patient"：**E**
- "customerCheckin = 接诊实体"：**E**
- "begin 业务上是 insert 下一步"：**E**（仅链式触发暗示）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 3 Write 后端无实现）

---

## 17. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 3 Write 后端 | 无后端代码 | F |
| 3 Write Response schema | 无样本 | F |
| res.result.vo 完整结构 | 无样本 | F |
| info 完整结构 | 无样本 | F |
| this.props 完整结构 | 无样本 | F |
| obj 形参完整结构 | HTML 不可得 | F |
| 3 触发函数 HTML ng-click | HTML 不可得 | F |
| customer / patient / member 业务实体关系 | 业务推断 | E |
| 字段值后端 DTO 同一性 | 无后端 | F |

---

## 18. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 3 Write 全部仅静态审计 |
| insertCustomerCheckin 实际调用 = 0 | ✅ | |
| beginCustomerCheckin 实际调用 = 0 | ✅ | |
| sendTakeMirrorNotice 实际调用 = 0 | ✅ | |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 167 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 167_*.md |
| 文件编号连续 | ✅ | 166 已被 S1-105 占用，本轮使用 167 |

---

## 19. 最终依赖图

### 19.1 G → H 链式依赖（**S1-106 核心发现**）

```
choseUser.affirm(obj)  [fnMap 触发, F 边界 HTML]
    ↓ 4 字段 Request
Write /admin/insertCustomerCheckin.json { name, gender, patientId, employeeId }
    ↓ [F 边界: HTTP + 后端]
result
    ↓ if (res.status == 0)
    ↓ L34916 关键: success
$scope.addUser.switch(false, res.result.vo)  ← res.result.vo 整体作为 info
    ↓ L34925 接收 (bool, info)
    ↓ L34927: this.show = bool
    ↓ L34928: if (info) ← res.result.vo truthy
$scope.beginCustomerCheckin(info)  ← 直接控制流调用
    ↓ L34946: var customerCheckinId = info.customerCheckin.id  ← 直接数据流访问
Write /admin/beginCustomerCheckin.json { customerCheckinId, medicalRecordType }
    ↓ [F 边界]
result
    ↓ if (result.status) return Popup
    ↓ L34954 关键: success
$state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })
[跳转离开 optometryCtrl scope]
```

### 19.2 I 独立路径

```
$scope.template.back()  [HTML ng-click 触发, F 边界]
    ↓ 2 字段 Request (1 固定 + 1 动态)
Write /admin/sendTakeMirrorNotice.json { medicalRecordId, <key>Id }
    ↓ [F 边界]
result
    ↓ if (result.status) return Popup
Popup.notice("发送成功！")
[不调 Read / 不跳转 / 不刷 data]
```

### 19.3 4 类 medicalRecordId 字段路径图

```
item.medicalRecord.id
    ↓ [4 个不同消费方]
    ├── A. fnMap 5 动作 (cancel/制作完成/到店取镜/快递发货) ──→ Write Request.medicalRecordId
    ├── B. querySingleOrder ──→ Read Request.medicalRecordId
    ├── C. modal.changeOrder ──→ medicalProduct.medicalRecordId ──→ shopInfo.medicalRecordId ──→ modal.affrim (报损 Write) Request.medicalRecordId + brushData 参数
    ├── D. beginCustomerCheckin ──→ customerCheckin.medicalRecordId ──→ $state.go stateParams.medicalRecordId
    └── E. fnMap "通知" ──→ $scope.template.medicalRecord ──→ template.back (sendNotice Write) Request.medicalRecordId
```

---

## 20. 最终结论

### 20.1 关键事实（A 级）

1. **3 Write Request 字段全集 + 来源**全部 A 级闭合
2. **insert → begin 链式触发**（双重强耦合）：
   - 直接控制流（affirm → addUser.switch → beginCustomerCheckin）
   - 直接数据流（res.result.vo → info → info.customerCheckin.id → customerCheckinId）
3. **sendTakeMirrorNotice 与 G/H 完全独立**（0 处共享）
4. **medicalRecordId 4 类字段路径全部 A 级**（item.medicalRecord.id / medicalProduct.medicalRecordId / customerCheckin.medicalRecordId / this.medicalRecord）
5. **S1-105 错误纠正**：`template.back` 不是 `template.affirm`
6. **template.back 在 controller.js 0 处显式调用**（HTML ng-click 触发，F 边界）
7. **0 处 customer/patient/member 业务实体关系可证**（仅字段名区分）

### 20.2 严格表述（A 级 vs E/F）

- "insert → begin 链式触发"：**A**
- "G/H 同 result"：**A**（链式 vo 传递）
- "I 与 G/H 完全独立"：**A**
- "4 类 medicalRecordId 字段路径"：**A**
- "obj.customer = patient"：**E**（禁止升级 A）
- "begin = 业务上开始接诊"：**E**
- "sendNotice = 发微信短信"：**E**
- "3 Write 后端实现"：**F**
- "res.result.vo 完整 schema"：**F**

### 20.3 S1-106 增量贡献

- ✅ S1-105 误读纠正（template.back）
- ✅ insert → begin 双重链式依赖钉死（**S1-105 仅识别为"链式触发"，S1-106 钉死为"直接数据流"**）
- ✅ 4 类 medicalRecordId 字段路径全部 A 级
- ✅ 8 字段全集（4+2+2）+ 字段来源全部 A 级
- ✅ 3 Write 独立性 / 共享性 全部 A 级
- ✅ F → A 提升：3 个 F 边界项提升为 A

### 20.4 不可在本轮升级为 A 的项

- 3 Write 后端处理（F）
- 3 Write Response schema（F）
- res.result.vo 完整结构（F）
- HTML ng-click 触发点（F）
- 业务实体关系（E / F）

---

**审计结束**。
