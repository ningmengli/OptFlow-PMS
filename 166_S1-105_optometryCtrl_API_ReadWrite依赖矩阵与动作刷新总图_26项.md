# S1-105 optometryCtrl API Read/Write 依赖矩阵与动作刷新总图

> **任务名**：S1-105｜optometryCtrl 全 API Read/Write 依赖矩阵与动作刷新总图（26项）
> **审计范围**：controller.js optometryCtrl（L34776-L35382）全 API 调用 + 依赖关系
> **当前轮次**：S1-105（接 S1-104 完成）
> **本轮承诺**：18 个 API call site 实际执行 = 0；controller.js / deliveryList.html / 历史 MD 修改 = 0

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| optometryCtrl (L34776-L35382) | ✅ | 全部 API 调用 |
| 17 ObjectFactory + 1 ListFactory | ✅ | 18 API call site |
| 6 个 fnMap 动作 | ✅ | S1-99/S1-104 已审 |
| 3 个新 Write API（S1-105 新发现） | ✅ | choseUser.affrim / beginCustomerCheckin / template.affrim |
| 7 HTML | ❌（不可得）| UI 触发点 F |
| 8 个 API 后端 | ⚠️ F 边界 | 无后端代码 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 合理业务推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "同 API = 同数据"：**E**（禁止升级 A）
- "同 medicalRecordId = 同一数据库对象"：**E**
- "Write 成功 = 业务完成"：**E**
- 自动添加未观察的 API：**D**（禁止补）

---

## 3. optometryCtrl API 全量清单

### 3.1 全部 18 个 API call site（A 级，全 controller.js 范围内穷举 optometryCtrl）

| # | 行号 | API 字符串 | Factory 模式 | 触发函数 | Read/Write |
|---|---|---|---|---|---|
| 1 | L34785 | `/admin/getCompanyOfMine.json` | 匿名 ObjectFactory | $scope.queryCompanyName | **Read** |
| 2 | L34795 | `/admin/getLoginEmployee.json` | 匿名 ObjectFactory | $scope.getEmployee | **Read** |
| 3 | L34843 | `/admin/stateTodoMedicalRecordCount.json` | 匿名 ObjectFactory | $scope.queryUndisposed | **Read** |
| 4 | L34862 | `/admin/getMedicalRecordFlowVo.json` | 匿名 ObjectFactory | $scope.order.brushData | **Read** |
| 5 | L34885 | `/admin/getMedicalRecordFlowVo.json` | 匿名 ObjectFactory | $scope.querySingleOrder | **Read** |
| 6 | L34914 | `/admin/insertCustomerCheckin.json` | 匿名 ObjectFactory | $scope.choseUser.affirm | **Write** |
| 7 | L34947 | `/admin/beginCustomerCheckin.json` | 匿名 ObjectFactory | $scope.beginCustomerCheckin | **Write** |
| 8 | L35054 | `/admin/getCanBeDeliverySkuInListOfProduct.json` | 匿名 ObjectFactory | $scope.concatMedicalProductStock (F4) | **Read** |
| 9 | L35099 | `/admin/setMedicalRecordProcessMode.json` | 匿名 ObjectFactory | choseFactoryMethod (Write A) | **Write** |
| 10 | L35150 | `/admin/cancelMedicalRecord.json` | 匿名 ObjectFactory | fnMap["取消订单"] | **Write** |
| 11 | L35167 | `/admin/confirmMedicalRecordReturn.json` | 匿名 ObjectFactory | fnMap["制作完成"] | **Write** |
| 12 | L35185 | `/admin/completeMedicalRecordDelivery.json` (deliveryStatus="2") | 匿名 ObjectFactory | fnMap["到店取镜"] (Write B) | **Write** |
| 13 | L35204 | `/admin/completeMedicalRecordDelivery.json` (deliveryStatus="1") | 匿名 ObjectFactory | fnMap["快递发货"] (Write C) | **Write** |
| 14 | L35253 | `/admin/sendTakeMirrorNotice.json` | 匿名 ObjectFactory | $scope.template.affrim | **Write** |
| 15 | L35281 | `/admin/getAdminInfo.json` | 匿名 ObjectFactory | $scope.modal.changeOrder | **Read** |
| 16 | L35319 | `/admin/selectMedicalProductStockList.json` | 匿名 ObjectFactory | $scope.modal.affrim | **Read** |
| 17 | L35342 | `/admin/createMedicalStockLossOfSmallVersion.json` | 匿名 ObjectFactory | $scope.modal.affrim | **Write** |
| 18 | L35367 | `/admin/selectMedicalRecordFlowVoList.json` | **ListFactory** (赋值 $scope.selectOrderListFactory) | $scope.search | **Read** |

### 3.2 统计（A 级）

| 维度 | 数值 | A-F |
|---|---|---|
| API call site 总数 | **18** | A |
| API unique 数 | **17** | A |
| Read call site 数 | **9** | A |
| Write call site 数 | **9** | A |
| Read unique 数 | **9** | A |
| Write unique 数 | **8** | A |
| ListFactory call site 数 | **1** (L35367) | A |
| ObjectFactory call site 数 | **17** (除 ListFactory) | A |
| 同一 API 多次调用 | getMedicalRecordFlowVo.json (2 处) + completeMedicalRecordDelivery.json (2 处) | A |

### 3.3 17 unique API 完整列表（A 级）

| # | API | 类型 | 唯一调用位置数 |
|---|---|---|---|
| 1 | getCompanyOfMine.json | Read | 1 |
| 2 | getLoginEmployee.json | Read | 1 |
| 3 | stateTodoMedicalRecordCount.json | Read | 1 |
| 4 | getMedicalRecordFlowVo.json | Read | 2（brushData + querySingleOrder）|
| 5 | insertCustomerCheckin.json | **Write** | 1 |
| 6 | beginCustomerCheckin.json | **Write** | 1 |
| 7 | getCanBeDeliverySkuInListOfProduct.json | Read (F4) | 1 |
| 8 | setMedicalRecordProcessMode.json | **Write** | 1 |
| 9 | cancelMedicalRecord.json | **Write** | 1 |
| 10 | confirmMedicalRecordReturn.json | **Write** | 1 |
| 11 | completeMedicalRecordDelivery.json | **Write** | 2（deliveryStatus="2"/"1"）|
| 12 | sendTakeMirrorNotice.json | **Write** | 1 |
| 13 | getAdminInfo.json | Read | 1 |
| 14 | selectMedicalProductStockList.json | Read | 1 |
| 15 | createMedicalStockLossOfSmallVersion.json | **Write** | 1 |
| 16 | selectMedicalRecordFlowVoList.json | Read (ListFactory) | 1 |
| 17 | (实际 16 - 待确认 - S1-105 完整) | — | — |

**注**：重数后 = 16 unique。重新核对：

| 类型 | unique API |
|---|---|
| Read | 8（getCompanyOfMine, getLoginEmployee, stateTodoMedicalRecordCount, getMedicalRecordFlowVo, getCanBeDeliverySkuInListOfProduct, getAdminInfo, selectMedicalProductStockList, selectMedicalRecordFlowVoList）|
| Write | 8（insertCustomerCheckin, beginCustomerCheckin, setMedicalRecordProcessMode, cancelMedicalRecord, confirmMedicalRecordReturn, completeMedicalRecordDelivery, sendTakeMirrorNotice, createMedicalStockLossOfSmallVersion）|
| **总计** | **16 unique API** |

---

## 4. Read API 详细

### 4.1 Read API 完整表（A 级）

| API | call site | 函数 | 触发时机 | A-F |
|---|---|---|---|---|
| getCompanyOfMine.json | L34785 | queryCompanyName | **Init** | A |
| getLoginEmployee.json | L34795 | getEmployee | **Init** | A |
| stateTodoMedicalRecordCount.json | L34843 | queryUndisposed | Init + 3 调用点 (search success L35376 / Write A success L35108 / 取消订单 success L35157) | A |
| getMedicalRecordFlowVo.json | L34862 | order.brushData | "报损" click 链路 | A |
| getMedicalRecordFlowVo.json | L34885 | querySingleOrder | Write success (5 处) + 取消 success + 制作完成 success | A |
| getCanBeDeliverySkuInListOfProduct.json (F4) | L35054 | concatMedicalProductStock | Write A/B/C 前置 (3 处) | A |
| getAdminInfo.json | L35281 | modal.changeOrder | "报损" click 链路 | A |
| selectMedicalProductStockList.json | L35319 | modal.affrim | "报损" 链路 | A |
| selectMedicalRecordFlowVoList.json | L35367 | $scope.search (ListFactory) | **Init** + 路由回调 | A |

### 4.2 Read 唯一性（A 级）

| API | 唯一调用位置 | 是否 optometryCtrl 唯一 Consumer |
|---|---|---|
| getCompanyOfMine.json | queryCompanyName | ❌ 0 处确认（optometryCtrl 内仅 1 处） |
| getLoginEmployee.json | getEmployee | ❌ 0 处确认（optometryCtrl 内仅 1 处） |
| stateTodoMedicalRecordCount.json | queryUndisposed | ❌ 0 处确认（optometryCtrl 内仅 1 处） |
| getMedicalRecordFlowVo.json | 2 处 (brushData + querySingleOrder) | optometryCtrl **2 个 Consumer**（**S1-101 已确认**）|
| getCanBeDeliverySkuInListOfProduct.json (F4) | concatMedicalProductStock | optometryCtrl **1 个 Consumer**（deliveryInputCtrl 1 个 → **2 个 Consumer**）|
| getAdminInfo.json | modal.changeOrder | optometryCtrl 1 处（controller.js 5 处：其它 4 处无关）|
| selectMedicalProductStockList.json | modal.affrim | optometryCtrl **1 个 Consumer**（**S1-103 已确认**）|
| selectMedicalRecordFlowVoList.json | $scope.search (ListFactory) | ❌ 0 处确认（optometryCtrl 内仅 1 处）|

### 4.3 双 Consumer API（A 级）

| API | Consumer 1 | Consumer 2 | 同 Factory? | 同 result? | 同 Scope? |
|---|---|---|---|---|---|
| getMedicalRecordFlowVo.json | querySingleOrder (L34885) | order.brushData (L34862) | ❌ 独立匿名 | ❌ 独立 | ❌ 独立 |
| getCanBeDeliverySkuInListOfProduct.json | deliveryInputCtrl concatMedicalProductStock | optometryCtrl concatMedicalProductStock | ❌ 不同 controller | ❌ 独立 | ❌ 独立 |

**A 级结论**：
- 同 API **不等于** 同 Factory / 同 result / 同 Scope / 同业务流程
- 2 个 Consumer 各自独立 ObjectFactory 实例

---

## 5. Write API 详细

### 5.1 Write API 完整表（A 级，S1-105 全部 8 个）

| # | API | call site | 入口函数 | 触发 | Request 字段数 | A-F |
|---|---|---|---|---|---|---|
| 1 | setMedicalRecordProcessMode.json | L35099 | choseFactoryMethod → fnMap["加工"] | "加工" 弹窗确认 | 3 字段 (medicalRecordId/toBeProcess/medicalProductStockBatctPoListJson) | A |
| 2 | completeMedicalRecordDelivery.json (deliveryStatus="2") | L35185 | fnMap["到店取镜"] | "到店取镜" 弹窗确认 | 4 字段 (medicalRecordId/deliveryStatus/deliveryNo/medicalProductStockBatctPoListJson) | A |
| 3 | completeMedicalRecordDelivery.json (deliveryStatus="1") | L35204 | fnMap["快递发货"] | "快递发货" 弹窗确认 | 4 字段 | A |
| 4 | createMedicalStockLossOfSmallVersion.json | L35342 | modal.affrim | "报损" 链路 | 4 outer + 4 inner (JSON 字符串) | A |
| 5 | cancelMedicalRecord.json | L35150 | fnMap["取消订单"] | "取消订单" 弹窗确认 | 1 字段 (medicalRecordId) | A |
| 6 | confirmMedicalRecordReturn.json | L35167 | fnMap["制作完成"] | "制作完成" 弹窗确认 | 1 字段 (medicalRecordId) | A |
| 7 | insertCustomerCheckin.json | L34914 | $scope.choseUser.affirm (S1-105 新发现) | 客户登记确认 | 4 字段 (name/gender/patientId/employeeId) | A |
| 8 | beginCustomerCheckin.json | L34947 | $scope.beginCustomerCheckin (S1-105 新发现) | addUser.switch 链路 | 2 字段 (customerCheckinId/medicalRecordType) | A |
| 9 | sendTakeMirrorNotice.json | L35253 | $scope.template.affrim (S1-105 新发现) | 模板发送 | 2 字段 (medicalRecordId/dynamic key+Id) | A |

**注**：实际 Write unique API = 8（completeMedicalRecordDelivery.json 是 1 个 unique API 但 2 处调用）

### 5.2 S1-105 关键新发现 3 个 Write API

#### 5.2.1 insertCustomerCheckin.json（A 级，L34908-L34921）

```javascript
choseUser.affirm: function affirm(obj) {
    var object = {};
    object.name = obj.customer.customerName;          // L34910
    object.gender = obj.customer.gender;                // L34911
    object.patientId = obj.patient.id;                  // L34912
    object.employeeId = $scope.employeeId;              // L34913
    new ObjectFactory().saveOrQuery("/admin/insertCustomerCheckin.json", object).then(function (res) {
        if (res.status == 0) {
            $scope.addUser.switch(false, res.result.vo);  // L34916
        } else {
            Popup.notice(res.errmsg);
        }
    });
}
```

| 字段 | 来源 | A-F |
|---|---|---|
| name | obj.customer.customerName | A |
| gender | obj.customer.gender | A |
| patientId | obj.patient.id | A |
| employeeId | $scope.employeeId | A |
| success 行为 | $scope.addUser.switch(false, res.result.vo) | A |
| success 弹窗 | ❌ 无 | A |
| success querySingleOrder | ❌ 无 | A |
| success queryUndisposed | ❌ 无 | A |

**S1-105 关键新发现**：
- choseUser.affirm success 触发 `$scope.addUser.switch(false, res.result.vo)`
- `$scope.addUser.switch(true, info)` **会触发** `$scope.beginCustomerCheckin(info)` (L34929) → 又触发 Write `/admin/beginCustomerCheckin.json`
- 形成**链式触发**：choseUser.affirm → addUser.switch → beginCustomerCheckin → Write 2

#### 5.2.2 beginCustomerCheckin.json（A 级，L34945-L34958）

```javascript
$scope.beginCustomerCheckin = function (info) {
    var customerCheckinId = info.customerCheckin.id;       // L34946
    new ObjectFactory().saveOrQuery("/admin/beginCustomerCheckin.json", {
        customerCheckinId: customerCheckinId,                // L34948
        medicalRecordType: $scope.choseUser.glassestype    // L34949
    }).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        $state.go("optometryGlasses", {                    // L34954
            medicalRecordId: result.result.vo.customerCheckin.medicalRecordId
        });
    });
};
```

| 字段 | 来源 | A-F |
|---|---|---|
| customerCheckinId | info.customerCheckin.id | A |
| medicalRecordType | $scope.choseUser.glassestype | A |
| success 行为 | `$state.go("optometryGlasses", { medicalRecordId: ... })` | A |
| success querySingleOrder | ❌ 无 | A |
| success queryUndisposed | ❌ 无 | A |

**S1-105 关键新发现**：
- beginCustomerCheckin success 触发 `$state.go`（路由跳转），**不调** querySingleOrder / queryUndisposed
- 跳转后**离开 optometryCtrl scope**，进入 optometryGlasses controller

#### 5.2.3 sendTakeMirrorNotice.json（A 级，L35243-L35261）

```javascript
// L35243-L35261 (从更广上下文读)
affrim: function affrim(type, id) {
    if (!id) {
        return Popup.notice("请选择" + type + "模板消息");
    }
    var medicalRecordId = this.medicalRecord;             // L35252
    new ObjectFactory().saveOrQuery("/admin/sendTakeMirrorNotice.json", _defineProperty({
        medicalRecordId: medicalRecordId                   // L35254
    }, key + "Id", id)).then(function (result) {
        if (result.status) {
            return Popup.notice(result.errmsg);
        }
        Popup.notice("发送成功！");                          // L35259
    });
}
```

| 字段 | 来源 | A-F |
|---|---|---|
| medicalRecordId | this.medicalRecord | A |
| 动态 key (type+"Id") | 形参 `id` | A |
| success 行为 | `Popup.notice("发送成功！")` | A |
| success querySingleOrder | ❌ 无 | A |
| success queryUndisposed | ❌ 无 | A |

**S1-105 关键新发现**：
- template.affrim success **仅 Popup**，不调任何 Read
- Request 用 `_defineProperty` 动态加 key（**A 级：编译器辅助**）

---

## 6. API → 函数 完整映射

### 6.1 全部 18 个 call site 映射表（A 级）

| API | 函数 | 行号 | 触发时机 | A-F |
|---|---|---|---|---|
| getCompanyOfMine.json | queryCompanyName | L34785 | Init | A |
| getLoginEmployee.json | getEmployee | L34795 | Init | A |
| stateTodoMedicalRecordCount.json | queryUndisposed | L34843 | Init + 3 success | A |
| getMedicalRecordFlowVo.json | order.brushData | L34862 | "报损" click | A |
| getMedicalRecordFlowVo.json | querySingleOrder | L34885 | 5 success 触发 | A |
| insertCustomerCheckin.json | choseUser.affirm | L34914 | 客户登记确认 | A |
| beginCustomerCheckin.json | beginCustomerCheckin | L34947 | addUser.switch 链 | A |
| getCanBeDeliverySkuInListOfProduct.json (F4) | concatMedicalProductStock | L35054 | Write A/B/C 前置 | A |
| setMedicalRecordProcessMode.json | choseFactoryMethod | L35099 | "加工" 弹窗确认 | A |
| cancelMedicalRecord.json | fnMap["取消订单"] | L35150 | "取消订单" 弹窗确认 | A |
| confirmMedicalRecordReturn.json | fnMap["制作完成"] | L35167 | "制作完成" 弹窗确认 | A |
| completeMedicalRecordDelivery.json (deliveryStatus="2") | fnMap["到店取镜"] | L35185 | "到店取镜" 弹窗确认 | A |
| completeMedicalRecordDelivery.json (deliveryStatus="1") | fnMap["快递发货"] | L35204 | "快递发货" 弹窗确认 | A |
| sendTakeMirrorNotice.json | template.affrim | L35253 | 模板发送 | A |
| getAdminInfo.json | modal.changeOrder | L35281 | "报损" 弹窗 + 用户操作 | A |
| selectMedicalProductStockList.json | modal.affrim | L35319 | "报损" 链路 | A |
| createMedicalStockLossOfSmallVersion.json | modal.affrim | L35342 | "报损" 链路 | A |
| selectMedicalRecordFlowVoList.json | $scope.search (ListFactory) | L35367 | Init + 路由回调 | A |

### 6.2 触发时机分类（A 级）

| 触发时机 | API |
|---|---|
| **Init** | getCompanyOfMine / getLoginEmployee / search (ListFactory) |
| **动作入口前置** | getCanBeDeliverySkuInListOfProduct (F4) / getMedicalRecordFlowVo (brushData) / getAdminInfo (changeOrder) / selectMedicalProductStockList (affrim) |
| **Write success** | querySingleOrder (5 触发) / queryUndisposed (3 触发) / brushData (1 触发) / template.affrim Popup / $state.go (beginCustomerCheckin) |
| **链式触发** | insertCustomerCheckin → addUser.switch → beginCustomerCheckin |

---

## 7. 函数 → API 完整映射

### 7.1 重要函数 API 依赖（A 级）

| 函数 | 调用 API | 行号 | A-F |
|---|---|---|---|
| queryCompanyName | getCompanyOfMine.json | L34785 | A |
| getEmployee | getLoginEmployee.json | L34795 | A |
| choseUser.affirm | insertCustomerCheckin.json | L34914 | A |
| beginCustomerCheckin | beginCustomerCheckin.json | L34947 | A |
| addUser.switch | **不直接调 API**（通过 beginCustomerCheckin 链式触发） | L34929 | A |
| concatMedicalProductStock (F4) | getCanBeDeliverySkuInListOfProduct.json | L35054 | A |
| choseFactoryMethod | setMedicalRecordProcessMode.json | L35099 | A |
| fnMap["取消订单"] | cancelMedicalRecord.json | L35150 | A |
| fnMap["制作完成"] | confirmMedicalRecordReturn.json | L35167 | A |
| fnMap["到店取镜"] | completeMedicalRecordDelivery.json (deliveryStatus="2") | L35185 | A |
| fnMap["快递发货"] | completeMedicalRecordDelivery.json (deliveryStatus="1") | L35204 | A |
| showDeliveryModal | (无直接 API，但内部调 concatMedicalProductStock + getCanBeDeliverySkuInListOfProduct via Save) | — | A |
| selectOrder (Write C) | sendMedicalProductToMachineCenter.json | ❌ **不在 optometryCtrl**（在 deliveryInputCtrl L3966） | A |
| saveStock (Write F5) | saveMedicalProductStockBatch.json | ❌ **不在 optometryCtrl**（在 deliveryInputCtrl L4007） | A |
| template.affrim | sendTakeMirrorNotice.json | L35253 | A |
| modal.changeOrder | getAdminInfo.json | L35281 | A |
| modal.affrim | selectMedicalProductStockList.json + createMedicalStockLossOfSmallVersion.json | L35319 + L35342 | A |
| order.brushData | getMedicalRecordFlowVo.json | L34862 | A |
| querySingleOrder | getMedicalRecordFlowVo.json | L34885 | A |
| queryUndisposed | stateTodoMedicalRecordCount.json | L34843 | A |
| $scope.search | selectMedicalRecordFlowVoList.json (ListFactory) | L35367 | A |

### 7.2 完整 optometryCtrl 内部函数列表（A 级，已穷举）

| 函数 | 包含 API? | A-F |
|---|---|---|
| queryCompanyName (L34784) | ✅ getCompanyOfMine | A |
| getEmployee (L34794) | ✅ getLoginEmployee | A |
| queryUndisposed (L34841) | ✅ stateTodoMedicalRecordCount | A |
| routeClick (L34850) | ❌ 无 | A |
| $scope.order (含 brushData + show) (L34857) | ✅ getMedicalRecordFlowVo (brushData) | A |
| querySingleOrder (L34883) | ✅ getMedicalRecordFlowVo | A |
| choseUser (L34897) | ✅ insertCustomerCheckin (affirm) | A |
| $scope.addUser (L34923) | ❌ 无（链式触发 beginCustomerCheckin） | A |
| $scope.modal (含 changeOrder + affrim) (L35275) | ✅ getAdminInfo (changeOrder) + selectMedicalProductStockList + createMedicalStockLossOfSmallVersion (affrim) | A |
| $scope.statusManage (L34959) | ❌ 无 | A |
| $scope.choseUser (L34905 - register) | ❌ 无 | A |
| $scope.beginCustomerCheckin (L34945) | ✅ beginCustomerCheckin.json | A |
| $scope.template (L35243) | ✅ sendTakeMirrorNotice (affrim) | A |
| $scope.printPeijing (L35263) | ❌ 无 | A |
| $scope.concatMedicalProductStock (L35048) | ✅ getCanBeDeliverySkuInListOfProduct | A |
| fnMap 6 动作 + choseFactoryMethod | 6 Write | A |
| $scope.search (L35355) | ✅ selectMedicalRecordFlowVoList (ListFactory) | A |

---

## 8. 初始化 Read DAG

### 8.1 optometryCtrl 初始化时序（A 级）

```
L34777: $scope.medicalRecordStatus = {};
L34779: $scope.filter_medicalRecordStatus = window.filter_medicalRecordStatus;
L34780: filter_medicalRecordStatus_update 函数定义
L34784: queryCompanyName 函数定义
L34792: queryCompanyName()  ← **Init 同步执行**
    ↓ L34785
    Read /admin/getCompanyOfMine.json
    ↓ res.status == 0
    $scope.companyName = res.object.companyName
    $scope.companyid = res.object.id

L34794: getEmployee 函数定义
L34799: getEmployee()  ← **Init 同步执行**
    ↓ L34795
    Read /admin/getLoginEmployee.json
    ↓
    $scope.employeeId = res.object.id

L34800: $scope.routeIndex = 0;
L34827: $scope.dealTime 函数定义
L34839: $scope.toPayCount = 0;
L34841: queryUndisposed 函数定义

L34857: $scope.order 对象定义
L34881: $scope.order_show = false;
L34883: querySingleOrder 函数定义

L34897: $scope.choseUser 对象定义
L34923: $scope.addUser 对象定义
L34945: beginCustomerCheckin 函数定义
L34959: $scope.statusManage 对象定义
...
L35048: concatMedicalProductStock 函数定义
L35084: choseFactoryMethod 函数定义
L35127: $scope.orderIndex = null;
L35128: clickBtn 函数定义
L35225-L35226: $scope.statusManage.callback 等等
L35243: $scope.template 对象定义
L35275: $scope.modal 对象定义
L35355: $scope.search 函数定义
L35379: $scope.search()  ← **Init 同步执行**
    ↓ L35367-L35374
    new ListFactory("/admin/selectMedicalRecordFlowVoList.json")
    nextPage() → $scope.selectOrderListFactory.items
    pagination
    $scope.queryUndisposed()  ← L35376
        ↓ L34843
        Read /admin/stateTodoMedicalRecordCount.json
        ↓
        $scope.toPayCount = result.result.object
```

### 8.2 初始化阶段 4 个 Read（A 级）

| # | API | 触发点 | 行号 | 同步/异步 |
|---|---|---|---|---|
| 1 | getCompanyOfMine.json | queryCompanyName() | L34792 | 同步 |
| 2 | getLoginEmployee.json | getEmployee() | L34799 | 同步 |
| 3 | selectMedicalRecordFlowVoList.json (ListFactory) | $scope.search() | L35379 | 同步启动 |
| 4 | stateTodoMedicalRecordCount.json | $scope.queryUndisposed() in search success | L35376 | 异步 |

**A 级结论**：
- optometryCtrl 初始化阶段共 4 个 Read 触发
- 2 个同步（queryCompanyName + getEmployee）
- 1 个同步启动 + 异步 list 加载（search + ListFactory）
- 1 个异步（queryUndisposed 在 search success 内）

---

## 9. 6 Write 动作前 Read

### 9.1 8 Write 动作前 Read 完整检查（A 级）

| Write | 动作前 Read |
|---|---|
| A (setMedicalRecordProcessMode) | ✅ F4 (concatMedicalProductStock) (L35097) |
| B (completeMedicalRecordDelivery "2") | ✅ F4 (concatMedicalProductStock) (L35183) |
| C (completeMedicalRecordDelivery "1") | ✅ F4 (concatMedicalProductStock) (L35202) |
| D (createMedicalStockLossOfSmallVersion) | ✅ getMedicalRecordFlowVo (brushData L34862) + getAdminInfo (modal.changeOrder L35281) + selectMedicalProductStockList (modal.affrim L35319) |
| E (cancelMedicalRecord) | ❌ 0 处 |
| F (confirmMedicalRecordReturn) | ❌ 0 处 |
| G (insertCustomerCheckin) | ❌ 0 处 |
| H (beginCustomerCheckin) | ❌ 0 处 |
| I (sendTakeMirrorNotice) | ❌ 0 处 |

**A 级结论**：
- A/B/C = 各 1 个动作前 Read（F4）
- D = 3 个动作前 Read（getMedicalRecordFlowVo + getAdminInfo + selectMedicalProductStockList）
- E/F/G/H/I = **0 动作前 Read**（直接调 Write）

---

## 10. Write Success 后 Read 完整检查

### 10.1 9 Write success 行为精确分层（A 级）

| # | Write | 错误处理 | success Read 1 | success Read 2 | success Popup | success State | success $scope 变化 |
|---|---|---|---|---|---|---|---|
| A | setMedicalRecordProcessMode | if (result.status) return Popup | querySingleOrder (L35107) | queryUndisposed (L35108) | ❌ 无 | ❌ 无 | items[orderIndex]/toPayCount |
| B | completeMedicalRecordDelivery "2" | if (result.status) return Popup | querySingleOrder (L35194) | ❌ 无 | ❌ 无 | ❌ 无 | items[orderIndex] |
| C | completeMedicalRecordDelivery "1" | if (result.status) return Popup | querySingleOrder (L35213) | ❌ 无 | ❌ 无 | ❌ 无 | items[orderIndex] |
| D | createMedicalStockLossOfSmallVersion | if (res.status == 0) | brushData (L35346) | ❌ 无 | "报损成功" | ❌ 无 | $scope.modal.changeOrder(false) + $scope.order.brushData |
| E | cancelMedicalRecord | if (result.status) return Popup | querySingleOrder (L35156) | queryUndisposed (L35157) | ❌ 无 | ❌ 无 | items[orderIndex]/toPayCount |
| F | confirmMedicalRecordReturn | if (result.status) return Popup | querySingleOrder (L35173) | ❌ 无 | ❌ 无 | ❌ 无 | items[orderIndex] |
| G | insertCustomerCheckin | if (res.status == 0) | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | $scope.addUser.switch(false, res.result.vo) |
| H | beginCustomerCheckin | if (result.status) return Popup | ❌ 无 | ❌ 无 | ❌ 无 | $state.go("optometryGlasses", ...) | — |
| I | sendTakeMirrorNotice | if (result.status) return Popup | ❌ 无 | ❌ 无 | "发送成功！" | ❌ 无 | ❌ 无 |

### 10.2 success 行为差异（A 级）

| 行为 | 触发 Write |
|---|---|
| success querySingleOrder | A / B / C / E / F (5 Write) |
| success queryUndisposed | A / E (2 Write) |
| success brushData | D (1 Write) |
| success Popup | D / I (2 Write) |
| success $state.go | H (1 Write) |
| success $scope 变化 | A / B / C / D / E / F (6 Write, items/medicalRecordStatus/toPayCount/order.object) |
| 链式触发 | G → $scope.addUser.switch → beginCustomerCheckin (1 Write) |

---

## 11. Read → Write 数据依赖

### 11.1 全部 Read → Write 数据链（A 级）

| Read Response | 中间变量 | Write Request | Write |
|---|---|---|---|
| F4 (getCanBeDeliverySkuInListOfProduct).result.list[].medicalProduct.id | medicalProductStockBatctPoListJson[].medicalProductId (L35070) | createMedicalStockLossOfSmallVersion 间接 + medicalProductStockBatctPoListJson (L35338) | A/B/C (S1-98) |
| F4.result.list[].deliveryStockInSkuVoList[].stockInSku.id / .deliveryCount | medicalProductStockBatctPoListJson[].medicalProductStocks[].{stockInSkuId, deliveryCount} (L35063-L35068) | medicalProductStockBatctPoListJson | A/B/C (S1-98) |
| getMedicalRecordFlowVo.result.object | $scope.order.object = result.object (L34868) | （不再进入 Write） | D (S1-102, brushData 仅刷新 order.object，不直接写） |
| getAdminInfo.result.object.id | $scope.modal.shopInfo.lossAdminId (L35291) | createMedicalStockLossOfSmallVersion Request.lossAdminId (L35337) | D (S1-103) |
| getAdminInfo.result.object.nickname | $scope.modal.shopInfo.adminname (L35292) | ❌ 不进入 Write | D (S1-103) |
| selectMedicalProductStockList.result.object[].id | medicalStockLossSkuListJson[].medicalProductStockId (L35328) | createMedicalStockLossOfSmallVersion Request.medicalStockLossSkuListJson (L35338) | D (S1-103) |

**A 级结论**：
- **F4 → A/B/C**：medicalProductId + stockInSkuId + deliveryCount 跨字段复制（S1-98）
- **getMedicalRecordFlowVo → D (brushData)**：整体对象引用替换（不直接写 Write）
- **getAdminInfo → D**：lossAdminId 跨字段复制（S1-103）
- **selectMedicalProductStockList → D**：medicalProductStockId 跨字段复制（S1-103）

### 11.2 Write → Read 数据刷新依赖（A 级）

| Write | success 调 Read | Read Request 字段 | 来源 |
|---|---|---|---|
| A | querySingleOrder | medicalRecordId | selectOrderListFactory.items[orderIndex].medicalRecord.id |
| B | querySingleOrder | medicalRecordId | selectOrderListFactory.items[orderIndex].medicalRecord.id |
| C | querySingleOrder | medicalRecordId | selectOrderListFactory.items[orderIndex].medicalRecord.id |
| D | brushData (L35346) | medicalRecordId | $scope.modal.shopInfo.medicalRecordId = medicalProduct.medicalRecordId (L35295) |
| E | querySingleOrder | medicalRecordId | selectOrderListFactory.items[orderIndex].medicalRecord.id |
| F | querySingleOrder | medicalRecordId | selectOrderListFactory.items[orderIndex].medicalRecord.id |
| G | (链式触发 H) | — | — |
| H | (无) | — | — |
| I | (无) | — | — |

---

## 12. medicalRecordId 表达式全集

### 12.1 optometryCtrl 范围全部 medicalRecordId 表达式（A 级，已穷举）

| 表达式 | 来源函数 | 写入目标 | A-F |
|---|---|---|---|
| `medical.medicalRecord.id` (L35085) | choseFactoryMethod | Write A Request.medicalRecordId | A |
| `item.medicalRecord.id` (L35149) | fnMap["取消订单"] | Write E Request.medicalRecordId | A |
| `item.medicalRecord.id` (L35166) | fnMap["制作完成"] | Write F Request.medicalRecordId | A |
| `item.medicalRecord.id` (L35182) | fnMap["到店取镜"] | Write B Request.medicalRecordId | A |
| `item.medicalRecord.id` (L35201) | fnMap["快递发货"] | Write C Request.medicalRecordId | A |
| `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (L34884) | querySingleOrder | Read Request.medicalRecordId | A |
| `medicalProduct.medicalRecordId` (L35295) | modal.changeOrder | shopInfo.medicalRecordId (L35307) → Write D Request.medicalRecordId (L35335) + brushData 参数 (L35346) | A |
| `this.medicalRecord` (L35252) | template.affrim | Write I Request.medicalRecordId | A |

**A 级结论**：
- 8 处表达式（不含 selectOrderListFactory 的 1 处 Read 入口）
- ❌ 0 处 `this.medicalRecordId` 字段路径
- ❌ 0 处 `result.medicalRecordId` 字段路径

### 12.2 表达式同源 / 不同源判定（A 级）

| 表达式 | 同源判定 |
|---|---|
| `medical.medicalRecord.id` (choseFactoryMethod) | 与 `item.medicalRecord.id` 同源（medical = item） |
| `item.medicalRecord.id` (5 处 fnMap) | 5 处 fnMap 同源（全部来自 clickBtn 形参 item） |
| `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (querySingleOrder) | 与 fnMap 表达式同源（最终 selectOrderListFactory.items[index]）|
| `medicalProduct.medicalRecordId` (modal.changeOrder) | **❌ 不同源**（医疗产品对象的字段，非 medicalRecord.id）|
| `this.medicalRecord` (template.affrim) | **❌ 不同源**（template 对象的 medicalRecord 字段，非 medicalRecord.id）|

**A 级结论**：
- 7 处 medicalRecord.id 系列表达式**同源**（A 级）
- 1 处 medicalProduct.medicalRecordId **不同源**（A 级）
- 1 处 this.medicalRecord **不同源**（A 级 — 来自 template 对象的 medicalRecord 字段）
- 严格表述：**8 处表达式形成 3 类不同源字段路径**（A 级）

---

## 13. Factory 依赖

### 13.1 18 个 call site Factory 模式（A 级）

| 模式 | 数量 | A-F |
|---|---|---|
| 匿名 `new ObjectFactory()` | 17 | A |
| `new ListFactory(...)` 赋给 $scope.selectOrderListFactory | 1 (L35367) | A |

### 13.2 Factory 实例独立性（A 级）

- 17 个匿名 `new ObjectFactory()` **每次都是新实例**（无复用）
- ❌ 0 处 `$scope.xxxFactory` 命名变量保存 ObjectFactory 实例
- 仅 1 处命名变量：`$scope.selectOrderListFactory` (ListFactory) (L35367)
- 严格表述：**所有 18 个 API 调用的 Factory 实例完全独立**（A 级）

### 13.3 Factory 类型差异（A 级）

- 17 ObjectFactory：单条数据获取/操作（无分页）
- 1 ListFactory (L35367)：列表分页加载（selectMedicalRecordFlowVoList.json）
- 严格表述：**Factory 类型选择由 API 性质决定，非随机**（A 级 — 列表用 ListFactory，单条用 ObjectFactory）

---

## 14. Scope 共享

### 14.1 跨函数共享的 Scope 变量（A 级）

| 变量 | 定义位置 | 共享函数 | 写入者 | 读取者 |
|---|---|---|---|---|
| `$scope.companyName` (L34787) | queryCompanyName | 显示用 | queryCompanyName | (HTML) |
| `$scope.companyid` (L34788) | queryCompanyName | 显示用 | queryCompanyName | (HTML) |
| `$scope.employeeId` (L34796) | getEmployee | 跨 Write 共享 | getEmployee | choseUser.affirm (L34913) + appearCustomerCheckin (L34949) |
| `$scope.dealTime` (L34827) | Init | 多处 | (Init) | queryUndisposed (L34842) + $scope.search (L35358) |
| `$scope.toPayCount` (L34839 + L34847) | queryUndisposed | UI 共享 | queryUndisposed | (HTML) |
| `$scope.orderIndex` (L35127 + L35130) | clickBtn | 跨 Read 共享 | clickBtn (L35130) | querySingleOrder (L34884/L34892/L34893) |
| `$scope.selectOrderListFactory` (L35367) | $scope.search | 跨 Read 共享 | $scope.search | querySingleOrder |
| `$scope.order.object` (L34859 + L34861 + L34868) | $scope.order | 报损链 | order.brushData | modal.changeOrder (L35282) |
| `$scope.medicalRecordStatus` (L34777) | Init | 跨 Read 共享 | Init | querySingleOrder (L34893) |
| `$scope.modal.shopInfo` (L35277 + L35287) | $scope.modal | 报损链 | modal.changeOrder (L35287) | modal.affrim (L35302-L35309) |
| `$scope.modal.show` (L35279) | $scope.modal | 显示用 | modal.changeOrder (L35279) | (HTML) |
| `$scope.order.isShow` (L34872) | $scope.order | 显示用 | order.show (L34872) | (HTML) |
| `$scope.filter_medicalRecordStatus` (L34779) | Init | 全局 | Init | filter_medicalRecordStatus_update (L34781) |
| `$scope.routeIndex` (L34800 + L34851) | routeClick | 路由 | routeClick (L34851) | $scope.search (L35359) |
| `$scope.statusManage` (L34959) | Init | UI/状态 | Init | routeClick (L34853) + $scope.search (L35360-L35364) |
| `$scope.appearLossModal` (L35316) | Init | 报损 | Init | (HTML 不可得) |
| `$scope.choseUser.glassestype` (L34901 + L34949) | choseUser.open | 接诊 | choseUser.open (L34901) | beginCustomerCheckin (L34949) |
| `$scope.medicalRecordId` ($scope.stateParams?) | (Optflow entry) | 全局 | (Init) | (Optflow state) |

### 14.2 严格表述（A 级）
- ❌ 0 处**同一变量**在 fnMap 6 动作之间被"共用状态"（每次 clickBtn 重置 $scope.orderIndex）
- ❌ 0 处**同一变量**在 modal.affrim 和 fnMap 动作之间被共享
- $scope.employeeId 是 optometryCtrl 内**真正的**跨函数共享变量（Init 写入 → 多处读）
- $scope.selectOrderListFactory 是 optometryCtrl 内**真正的**跨函数共享数据结构（Init 写入 → querySingleOrder 读 + 整体覆盖）
- $scope.modal.shopInfo 是**报损链**专用的共享数据结构
- 严格表述：**Scope 共享按功能分桶**（Init 全局 / 报损链 / 列表刷新链），**不跨业务混合共享**（A 级）

---

## 15. API 共用 vs 数据共用

### 15.1 API 共用与数据共用对比矩阵（A 级）

| API | 共享 Consumer | 同 Factory? | 同 result? | 同 Scope 变量? | 同业务流程? |
|---|---|---|---|---|---|
| getMedicalRecordFlowVo.json | querySingleOrder + order.brushData | ❌ 独立匿名 | ❌ 独立 | ❌ 不同（items[orderIndex] vs order.object）| ❌ 独立 |
| getCanBeDeliverySkuInListOfProduct.json (F4) | deliveryInputCtrl + optometryCtrl concatMedicalProductStock | ❌ 跨 controller | ❌ 独立 | ❌ 跨 controller | ❌ 独立 |
| stateTodoMedicalRecordCount.json | 仅 optometryCtrl queryUndisposed | — | — | $scope.toPayCount | — |
| getAdminInfo.json | optometryCtrl modal.changeOrder + 其它 4 controller | ❌ 跨 controller | ❌ 独立 | ❌ 独立 | ❌ 独立 |
| selectMedicalProductStockList.json | 仅 optometryCtrl modal.affrim | — | — | medicalStockLossSkuListJson | — |
| createMedicalStockLossOfSmallVersion.json | 仅 optometryCtrl modal.affrim | — | — | — | — |
| 其余 10 个 API | 仅 optometryCtrl 1 处 | — | — | — | — |

**A 级结论**：
- **同 API ≠ 同 Factory**（A）
- **同 API ≠ 同 result**（A）
- **同 API ≠ 同 Scope 变量**（A）
- **同 API ≠ 同业务流程**（A）
- 严格表述：**只有"同 API"是源码可证，其余共享性全部按独立处理**（A）

---

## 16. F4 双 Consumer 详解

### 16.1 F4 在 optometryCtrl 和 deliveryInputCtrl 的差异（A 级）

| 维度 | optometryCtrl (L35054) | deliveryInputCtrl (L3836) |
|---|---|---|
| API 字符串 | `/admin/getCanBeDeliverySkuInListOfProduct.json` ✅ 同 | 同 |
| Request body | `{ medicalProductIdArray: medicalProductIdArray }` ✅ 同 | 同 |
| Request.medicalProductIdArray 来源 | `item.medicalProductVoList[].medicalProduct.id` (L35051-L35052) | `arr[i].medicalProduct.id` (filtered by `if (objectId == null)`) (L3821-L3824) |
| result.object 字段消费 | medicalProduct.id / stockInSku.id / deliveryCount (L35065-L35070) | v.medicalProduct.id / v.machineCenter.id (L3962) |
| result.object → 下一跳 | `medicalProductStockBatctPoListJson` (L35078) | 直接 map → F6 Request (L3966) |
| Factory | 匿名 new ObjectFactory() | 匿名 new ObjectFactory() |
| success 行为 | resolve 字符串 → 3 caller 接收 | 直接 enter 下一阶段 |

**A 级结论**：
- 2 Consumer **同 API + 同 Request 字段名**
- ❌ 0 处直接代码连接（不同 controller / 不同 scope / 不同 result 消费）
- Request.medicalProductIdArray **不同源**（optometryCtrl 来自 item.medicalProductVoList，deliveryInputCtrl 来自 waitingDeliveryList）
- result.object 消费**完全不同**（optometryCtrl 3 字段，deliveryInputCtrl 2 字段）
- 严格表述：**2 Consumer 仅"同 API"，其它全部独立**（A 级）

---

## 17. getMedicalRecordFlowVo 双 Consumer 详解

### 17.1 querySingleOrder vs order.brushData（A 级）

| 维度 | querySingleOrder (L34883) | order.brushData (L34860) |
|---|---|---|
| API 字符串 | `/admin/getMedicalRecordFlowVo.json` ✅ 同 | 同 |
| Request.medicalRecordId 来源 | `$scope.selectOrderListFactory.items[$scope.orderIndex].medicalRecord.id` (L34884) | brushData 形参 (来自 order.show 调用) |
| result.object 写入 | `$scope.selectOrderListFactory.items[$scope.orderIndex]` (L34892) | `$scope.order.object` (L34868) |
| 额外副作用 | `$scope.filter_medicalRecordStatus_update(result.object, "button", orderIndex)` (L34893) | $scope.order.object = {} 重置 (L34861) |
| $timeout 包裹 | ✅ L34891 | ❌ 无 |
| 触发场景 | Write success | "报损" click |
| 间接字段级读取 (modal.changeOrder) | ❌ 无 | ✅ L35282-L35296 (6 字段) |
| Factory 实例 | 独立 | 独立 |

**A 级结论**：
- 2 Consumer **同 API + 同 Request 字段名**
- result.object **写入不同 $scope 字段**
- querySingleOrder 额外**更新 medicalRecordStatus**（L34893）
- order.brushData 额外**重置 order.object = {}**（L34861）
- 严格表述：**2 Consumer 仅"同 API" + 同 Request 字段名，其它全部独立**（A 级）

---

## 18. 独立分支识别

### 18.1 optometryCtrl 5 大业务分支（A 级）

| 分支 | 入口 | 触发 API | 链路 | 备注 |
|---|---|---|---|---|
| **A. 加工/配送分支** | fnMap "加工" / "到店取镜" / "快递发货" | setMedicalRecordProcessMode / completeMedicalRecordDelivery (×2) | F4 → Write A/B/C | 完整端到端 |
| **B. 报损分支** | clickBtn "报损" → order.show → brushData → modal.changeOrder → modal.affrim | getMedicalRecordFlowVo + getAdminInfo + selectMedicalProductStockList + createMedicalStockLossOfSmallVersion | 3 Read + 1 Write | 完整端到端 |
| **C. 取消订单分支** | fnMap "取消订单" | cancelMedicalRecord | Write → querySingleOrder + queryUndisposed | 单 Write |
| **D. 制作完成分支** | fnMap "制作完成" | confirmMedicalRecordReturn | Write → querySingleOrder | 单 Write |
| **E. 客户接诊分支（S1-105 新发现）** | choseUser.affirm → addUser.switch → beginCustomerCheckin | insertCustomerCheckin + beginCustomerCheckin | 链式触发 + $state.go 跳转 | 跨 controller |
| **F. 模板通知分支（S1-105 新发现）** | $scope.template.affrim | sendTakeMirrorNotice | Write → Popup | 单 Write |

### 18.2 分支间独立性（A 级）

| 检查 | 结论 | A-F |
|---|---|---|
| 6 个分支共享同一 optometryCtrl scope | ✅ 是 | A |
| 6 个分支共享同一 selectOrderListFactory | ❌ 仅 C/D 分支用 | A |
| 6 个分支共享同一 $scope.order | ❌ 仅 B 分支用 | A |
| 6 个分支共享同一 $scope.modal | ❌ 仅 B 分支用 | A |
| 6 个分支共享同一 $scope.choseUser | ❌ 仅 E 分支用 | A |
| 6 个分支共享同一 $scope.template | ❌ 仅 F 分支用 | A |

**A 级结论**：
- 6 个分支**Scope 分桶**，互不干扰
- ❌ 0 处跨分支直接状态共享
- ❌ 0 处跨分支 Write 后互相依赖（除 D 触发 brushData → 触发新分支 B 的入口，但 brushData 内部不调 Write）

---

## 19. 重复提交防护

### 19.1 Controller 层防护检查（A 级）

| 检查项 | 8 Write 全部 | A-F |
|---|---|---|
| disabled 标志 | ❌ 0 处 | A |
| loading 标志 | ❌ 0 处 | A |
| submitting / isSubmitting | ❌ 0 处 | A |
| promise lock（自挂） | ❌ 0 处 | A |
| debounce / throttle | ❌ 0 处 | A |
| $timeout 锁 | ❌ 0 处 | A |
| recursion | ❌ 0 处 | A |
| 循环中 saveOrQuery | ❌ 0 处 | A |
| 弹窗打开期间互斥 | ✅ 隐含（popout_tip 弹窗期间） | E 推断 |

**A 级结论**：
- **8 Write 都 0 处 Controller 层重复提交防护**（A 级）
- 唯一隐含防重 = popout_tip 弹窗打开期间（**E 业务推断**，非源码事实）
- UI 层防重：**F**（HTML 不可得）
- 服务端幂等性：**F**（无后端代码）

---

## 20. API 重复调用统计

### 20.1 同一 API 多次调用（A 级）

| API | call site 数 | 触发函数 | A-F |
|---|---|---|---|
| getMedicalRecordFlowVo.json | 2 | querySingleOrder + order.brushData | A |
| completeMedicalRecordDelivery.json | 2 | fnMap "到店取镜" + fnMap "快递发货" | A |
| 其它 14 API | 1 | 单一函数 | A |

### 20.2 querySingleOrder 重复调用（A 级）

| 调用位置 | 触发 |
|---|---|
| L35107 | Write A (setMedicalRecordProcessMode) success |
| L35156 | Write E (cancelMedicalRecord) success |
| L35173 | Write F (confirmMedicalRecordReturn) success |
| L35194 | Write B (deliveryStatus="2") success |
| L35213 | Write C (deliveryStatus="1") success |
| **总计** | **5 次 call** |

### 20.3 queryUndisposed 重复调用（A 级）

| 调用位置 | 触发 |
|---|---|
| L35108 | Write A (setMedicalRecordProcessMode) success |
| L35157 | Write E (cancelMedicalRecord) success |
| L35376 | $scope.search success（init / 路由回调）|
| **总计** | **3 次 call** |

### 20.4 order.brushData 重复调用（A 级）

| 调用位置 | 触发 |
|---|---|
| L34861 | order.show 内部（"报损" click 链路） |
| L35346 | modal.affrim success（"报损" 提交成功后）|
| **总计** | **2 次 call** |

---

## 21. 刷新覆盖策略

### 21.1 整体对象引用替换（A 级）

| 目标 | 操作 | 行号 | 覆盖策略 |
|---|---|---|---|
| `$scope.selectOrderListFactory.items[orderIndex]` | `=` result.object | L34892 | **整体引用替换** |
| `$scope.medicalRecordStatus[orderIndex]` | `=` window.filter_medicalRecordStatus(...) | L34781 | **整体引用替换**（window 函数计算后）|
| `$scope.order.object` | `=` result.object | L34868 | **整体引用替换** |
| `$scope.modal.shopInfo` | `=` {...}（构造新对象）| L35287 | **整体引用替换** |

### 21.2 严格表述（A 级）
- optometryCtrl 对 API Response 的处理**全部采用整体对象引用替换**（A 级）
- ❌ 0 处 angular.extend / Object.assign / for-in / 字段级合并
- ❌ 0 处 oldItem 保留
- ❌ 0 处增量更新
- 整体替换后无业务逻辑（无数据验证 / 字段同步 / 异常补偿）

---

## 22. HTML 边界（F）

| 触发点 | A-F |
|---|---|
| clickBtn 6 动作 ng-click | F |
| popout_tip 弹窗 | F（仅 res truthy 可证，res 实际值 F）|
| popout_cb 弹窗 | F |
| window.commonFn.openMaskFun/closeMaskFun | F |
| querySingleOrder/modal.changeOrder 等 ng-click | F |
| $scope.modal.show 显示控制 | F |

**A 级结论**：optometryCtrl HTML 资源范围内**不可得**，全部 UI 触发点保持 F。

---

## 23. Response 边界（F）

| 边界 | A-F |
|---|---|
| 17 unique API 后端处理 | F |
| 17 unique API Response schema | F |
| DB schema / Entity / DTO | F |
| HTTP method 实际（GET/POST） | F（仅 saveOrQuery 模式可证）|
| 业务语义 | E |

---

## 24. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | optometryCtrl 全 API unique 数 | 16 | A | L1 | 已穷举 |
| 02 | API call site 总数 | 18 | A | L1 | |
| 03 | Read unique 数 | 8 | A | L1 | |
| 04 | Write unique 数 | 8 | A | L1 | |
| 05 | Read API 清单 | 8 个 | A | L1 | |
| 06 | Write API 清单 | 8 个 | A | L1 | |
| 07 | API → 函数 | 18 call site 全部映射 | A | L1 | 详见 §6.1 |
| 08 | 函数 → API | 全部函数映射 | A | L1 | 详见 §7 |
| 09 | 初始化 Read | 4 个 Read (queryCompanyName + getEmployee + search + queryUndisposed in search) | A | L1 | 详见 §8 |
| 10 | 动作前 Read | A/B/C=1个F4 / D=3个 / E/F/G/H/I=0 | A | L1 | 详见 §9 |
| 11 | Write success → Read | 5 success→querySingleOrder / 2 success→queryUndisposed / 1 brushData / 1 $state.go / 1 Popup | A | L1 | 详见 §10 |
| 12 | Read → Write 数据链 | F4→A/B/C / getAdminInfo→D / selectMedicalProductStockList→D | A | L1 | 详见 §11 |
| 13 | getMedicalRecordFlowVo 双 Consumer | querySingleOrder + order.brushData | A | L1 | 详见 §17 |
| 14 | F4 双 Consumer | deliveryInputCtrl + optometryCtrl | A | L1 | 详见 §16 |
| 15 | Factory 隔离 | 17 匿名 ObjectFactory 独立 + 1 ListFactory 命名 | A | L1 | 详见 §13 |
| 16 | Scope 共享 | $scope.employeeId / $scope.selectOrderListFactory / $scope.modal.shopInfo 等 | A | L1 | 详见 §14 |
| 17 | result 共享 | 同 API ≠ 同 result | A | L1 | 详见 §15 |
| 18 | medicalRecordId 表达式全集 | 8 处表达式 / 3 类不同源 | A | L1 | 详见 §12 |
| 19 | F4 → 3 Write | medicalProductStockBatctPoListJson | A | L1 | |
| 20 | getAdminInfo → 报损 | shopInfo.lossAdminId | A | L1 | |
| 21 | selectMedicalProductStockList → 报损 | medicalStockLossSkuListJson[].medicalProductStockId | A | L1 | |
| 22 | cancel → Read | querySingleOrder + queryUndisposed | A | L1 | |
| 23 | confirm → Read | querySingleOrder | A | L1 | |
| 24 | 重复提交防护 | ❌ 0 处（Controller 层） | A | L1 | |
| 25 | API 重复调用 | querySingleOrder×5 / queryUndisposed×3 / brushData×2 | A | L1 | 详见 §20 |
| 26 | optometryCtrl 最小 API DAG | 详见 §28 | A | L1 | |

**统计**：
- **A：26 项（全部 A）**
- **F / E / D / C / B：0**
- **E/F 升 A：0**

---

## 25. L1/L2/L3

### L1（源码事实，可证）

- 18 个 API call site 全部（A）
- 16 unique API 全部（A）
- Read/Write 分类（A）
- 8 个 Write success 行为精确分层（A）
- 8 处 medicalRecordId 表达式 / 3 类不同源（A）
- 4 个初始化 Read（A）
- 5 大业务分支识别（A）
- 整体对象引用替换模式（A）
- 0 处重复提交防护（A）

### L2（业务解释，未证）

- "加工 = 选择加工方式"：**E**
- "到店取镜 / 快递发货"：**E**
- "报损 = 创建库存报损"：**E**
- "取消订单 = 取消医疗记录"：**E**
- "制作完成 = 确认回库"：**E**
- "客户接诊 = 创建客户登记"：**E**
- "发取镜通知 = 发送微信模板"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 16 unique API 全部无后端实现）

---

## 26. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| 16 unique API 后端处理 | 无后端代码 | F |
| 16 unique API Response schema | 无样本 | F |
| 8 Write 真实行为 | 仅源码审计 | F |
| HTML 全部 UI 触发点 | HTML 不可得 | F |
| 业务语义 | 命名 + 注释 | E |
| DB schema | 无后端 | F |
| 字段值是否后端 DTO 同一 | 无后端 | F |
| 弹窗 popout_tip / popout_cb 实现 | window 全局 | F |
| 8 Write 后端幂等性 | 无后端 | F |

---

## 27. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 任何 API 实际调用 = 0 | ✅ | 18 个 call site 全部仅静态审计 |
| 8 个 Write 实际执行 = 0 | ✅ | |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 166 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 166_*.md |
| 文件编号连续 | ✅ | 165 已被 S1-104 占用，本轮使用 166 |

---

## 28. 最终 API DAG

### 28.1 optometryCtrl 初始化 Read DAG（A 级）

```
Controller Init (L34776-L35379)
    ↓
L34792: $scope.queryCompanyName() 同步
    ↓
Read /admin/getCompanyOfMine.json (Read)
    ↓ [F 边界]
$scope.companyName / $scope.companyid

L34799: $scope.getEmployee() 同步
    ↓
Read /admin/getLoginEmployee.json (Read)
    ↓ [F 边界]
$scope.employeeId

L35379: $scope.search() 同步启动
    ↓
new ListFactory("/admin/selectMedicalRecordFlowVoList.json")
    ↓ [F 边界]
$scope.selectOrderListFactory.items[] (列表加载)
    ↓ success
L35376: $scope.queryUndisposed()
    ↓
Read /admin/stateTodoMedicalRecordCount.json (Read)
    ↓ [F 边界]
$scope.toPayCount
```

### 28.2 6 大业务分支 DAG（A 级）

#### A. 加工/配送分支

```
fnMap "加工" / "到店取镜" / "快递发货"
    ↓ [popout_tip 弹窗]
$scope.concatMedicalProductStock(item)
    ↓
Read /admin/getCanBeDeliverySkuInListOfProduct.json (F4, Read)
    ↓ [F 边界]
result.result.list
    ↓ forEach + map
medicalProductStockBatctPoListJson (JSON 字符串)
    ↓ resolve

choseFactoryMethod
    ↓
Write /admin/setMedicalRecordProcessMode.json (Write A)
    ↓ success (L35107-L35108)
$scope.querySingleOrder() ──→ Read /admin/getMedicalRecordFlowVo.json → 整体覆盖 selectOrderListFactory.items[orderIndex] + medicalRecordStatus[orderIndex]
$scope.queryUndisposed() ──→ Read /admin/stateTodoMedicalRecordCount.json → $scope.toPayCount

fnMap "到店取镜" (deliveryStatus="2")
    ↓
Write /admin/completeMedicalRecordDelivery.json
    ↓ success (L35194)
$scope.querySingleOrder() ──→ [同上]

fnMap "快递发货" (deliveryStatus="1")
    ↓
Write /admin/completeMedicalRecordDelivery.json
    ↓ success (L35213)
$scope.querySingleOrder() ──→ [同上]
```

#### B. 报损分支

```
clickBtn "报损" → $scope.order.show(true, medicalRecordId)
    ↓
window.commonFn.openMaskFun()  [F 边界]
$scope.order.brushData(medicalRecordId)
    ↓ L34861
$scope.order.object = {} (重置)
Read /admin/getMedicalRecordFlowVo.json (Read)
    ↓ [F 边界]
result.object
    ↓ L34868
$scope.order.object = result.object (整体引用替换)

[HTML 渲染 order.object]

[用户点击"换商品"]
    ↓
$scope.modal.changeOrder(true, index)
    ↓
Read /admin/getAdminInfo.json (Read)
    ↓ [F 边界]
res.result.object
    ↓
$scope.modal.shopInfo = { ... 9 字段 ... } (整体引用替换)
    ↓ [其中 6 字段来自 $scope.order.object.medicalProductVoList[index]]

[用户选择 lossAdmin + lossReason + 点击确认]
    ↓
$scope.modal.affrim()
    ↓ L35311/L35315 校验 lossAdminId/lossReasonId
Read /admin/selectMedicalProductStockList.json (Read)
    ↓ [F 边界]
res.object
    ↓ forEach
medicalStockLossSkuListJson[]
    ↓
Write /admin/createMedicalStockLossOfSmallVersion.json (Write D)
    ↓ success (L35343)
Popup.notice("报损成功")
$scope.modal.changeOrder(false) (关闭 modal)
$scope.order.brushData(medicalRecordId)  ← 重新刷 data
    ↓
Read /admin/getMedicalRecordFlowVo.json (Read)
    ↓ [F 边界]
$scope.order.object = result.object
```

#### C. 取消订单分支

```
fnMap "取消订单"
    ↓ $scope.hint(1, fn)
Write /admin/cancelMedicalRecord.json (Write E)
    ↓ success (L35156-L35157)
$scope.querySingleOrder() ──→ Read /admin/getMedicalRecordFlowVo.json → 整体覆盖 selectOrderListFactory.items[orderIndex] + medicalRecordStatus[orderIndex]
$scope.queryUndisposed() ──→ Read /admin/stateTodoMedicalRecordCount.json → $scope.toPayCount
```

#### D. 制作完成分支

```
fnMap "制作完成"
    ↓ $scope.hint(3, fn)
Write /admin/confirmMedicalRecordReturn.json (Write F)
    ↓ success (L35173)
$scope.querySingleOrder() ──→ [同上]
（不调 queryUndisposed）
```

#### E. 客户接诊分支（S1-105 新发现）

```
choseUser.affirm(obj)
    ↓ L34914
Write /admin/insertCustomerCheckin.json (Write G)
    ↓ success (L34916)
$scope.addUser.switch(false, res.result.vo)
    ↓
$scope.addUser.switch(true, info) [链式触发 if info]
    ↓ L34929
$scope.beginCustomerCheckin(info)
    ↓
Write /admin/beginCustomerCheckin.json (Write H)
    ↓ success (L34954)
$state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })
[跳转离开 optometryCtrl scope]
```

#### F. 模板通知分支（S1-105 新发现）

```
$scope.template.affrim(type, id)
    ↓ L35253
Write /admin/sendTakeMirrorNotice.json (Write I)
    ↓ success (L35259)
Popup.notice("发送成功！")
（不调任何 Read）
```

### 28.3 optometryCtrl 完整 API DAG 图（A 级）

```
[Init]
  ↓
  ├── queryCompanyName() ──────────── Read getCompanyOfMine.json
  ├── getEmployee() ────────────────── Read getLoginEmployee.json
  └── search() ────────────────────── Read selectMedicalRecordFlowVoList.json (ListFactory)
                                            ↓ success
                                          queryUndisposed() ──── Read stateTodoMedicalRecordCount.json

[Branch A: 加工/配送]
  fnMap "加工" / "到店取镜" / "快递发货"
    ↓ [popout_tip]
  concatMedicalProductStock ────────── Read F4 (getCanBeDeliverySkuInListOfProduct.json)
    ↓
  choseFactoryMethod / clickBtn fnMap
    ↓
  Write A (setMedicalRecordProcessMode) / B (deliveryStatus="2") / C (deliveryStatus="1")
    ↓ success
  querySingleOrder ──────────────────── Read getMedicalRecordFlowVo.json
  queryUndisposed (仅 A) ──────────────── Read stateTodoMedicalRecordCount.json

[Branch B: 报损]
  clickBtn "报损" → order.show → brushData ─ Read getMedicalRecordFlowVo.json
    ↓
  modal.changeOrder ──────────────────── Read getAdminInfo.json
    ↓
  modal.affrim ────────────────────────── Read selectMedicalProductStockList.json
    ↓
  Write D (createMedicalStockLossOfSmallVersion)
    ↓ success
  Popup + modal.changeOrder(false) + brushData ── Read getMedicalRecordFlowVo.json

[Branch C: 取消订单]
  fnMap "取消订单" → Write E (cancelMedicalRecord)
    ↓ success
  querySingleOrder + queryUndisposed

[Branch D: 制作完成]
  fnMap "制作完成" → Write F (confirmMedicalRecordReturn)
    ↓ success
  querySingleOrder

[Branch E: 客户接诊] (S1-105 新发现)
  choseUser.affirm → Write G (insertCustomerCheckin)
    ↓ success
  addUser.switch → beginCustomerCheckin → Write H (beginCustomerCheckin)
    ↓ success
  $state.go (离开 scope)

[Branch F: 模板通知] (S1-105 新发现)
  $scope.template.affrim → Write I (sendTakeMirrorNotice)
    ↓ success
  Popup.notice("发送成功！")
```

---

## 29. 最终结论

### 29.1 optometryCtrl 实际 API 地图（S1-105 更新版）

**A 级关键事实**：
1. **optometryCtrl 实际共 16 unique API**（不是 6 个 Write）
2. **共 18 个 API call site**（2 个 API 各有 2 处调用）
3. **共 8 Write API**（S1-105 新发现 3 个：insertCustomerCheckin / beginCustomerCheckin / sendTakeMirrorNotice）
4. **共 8 Read API**（ListFactory 1 个 + ObjectFactory 7 个）
5. **共 6 大业务分支**（A 加工配送 / B 报损 / C 取消订单 / D 制作完成 / E 客户接诊 / F 模板通知）

### 29.2 S1-105 关键新发现

1. **3 个新 Write API 之前完全未审计**：
   - insertCustomerCheckin.json (choseUser.affirm, L34914)
   - beginCustomerCheckin.json (beginCustomerCheckin, L34947)
   - sendTakeMirrorNotice.json (template.affrim, L35253)
2. **链式触发**：choseUser.affirm → addUser.switch → beginCustomerCheckin → Write 2
3. **beginCustomerCheckin success 触发 $state.go 跳转**（离开 optometryCtrl scope）
4. **template.affrim success 仅 Popup**（不调任何 Read）
5. **8 Write 共 4 种 success 模式**：
   - querySingleOrder + queryUndisposed（A、E）
   - 仅 querySingleOrder（B、C、F）
   - brushData（D）
   - 仅 Popup 或 $state.go（G、H、I）

### 29.3 严格表述（A 级 vs E/F）

- "optometryCtrl 实际 API unique = 16"：**A**
- "共 8 个 Write API"：**A**
- "8 个 Write success 行为差异 = 4 种模式"：**A**
- "同 API ≠ 同 Factory / 同 result / 同 Scope / 同业务流程"：**A**
- "3 类 medicalRecordId 字段路径（id / medicalRecordId / this.medicalRecord）"：**A**
- "0 处重复提交防护"：**A**（Controller 层）
- "业务语义"：**E**（禁止升级 A）
- "HTML UI 触发"：**F**
- "后端实现"：**F**

### 29.4 不可在本轮升级为 A 的项

- 16 unique API 后端处理（F）
- 16 unique API Response schema（F）
- HTML 全部 UI 触发点（F）
- 业务语义（E）
- 字段值在 3 处是否完全相同（F）
- DB/Entity/DTO/FK（L3 = F）
- 弹窗 popout_tip / popout_cb 内部实现（F）
- 8 Write 后端幂等性（F）

---

**审计结束**。
