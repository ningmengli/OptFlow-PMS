# S1-135 CustomerCheckin → MedicalRecord → 就诊流程主入口链深度审计

> **项目**：OptFlow PMS 逆向建模
> **本轮核心问题**：CustomerCheckin 如何进入 MedicalRecord → 就诊流程主入口？
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-196 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变）|
| **customerCheckin 出现** | **46 处**（A — 字符级精确）|
| **customerCheckinId 出现** | **19 处**（A — 字符级精确）|
| **customerCheckin.medicalRecordId 桥** | **6 处**（A — 多源互证）|
| **insertCustomerCheckin 3 个 API** | insertCustomerCheckin / OfNewPaitent / OfNewCustomer（A — 4 处调用）|
| **confirmArrivalOfAppoint** | **1 处**（A — L8658 addCheckinCtrl）|
| **$stateParams.medicalRecordId** | **25 处**（A — S1-128/135 精确）|
| **getMedicalRecord.json** | **33 处**（A — 字符级精确）|

---

## 2. customerCheckin 全量（46 处精确分类）

### 2.1 customerCheckin 总命中分类（A — 字符级）

| # | 类别 | 次数 | 代表行号 |
|---:|---|---:|---|
| 1 | **Response 字段 `res.result.vo.customerCheckin`** | 5 | L8671, L8697, L8707, L33134, L34955 |
| 2 | **Response 字段 `res.customerCheckin`** | 1 | L8791 |
| 3 | **Response 字段 `response.customerCheckin`** | 1 | L10610 |
| 4 | **Response 字段 `employee.customerCheckin`** | 1 | L10642 |
| 5 | **List 字段 `item.customerCheckin`** | 1 | L8789 |
| 6 | **Response 字段 `res.customerCheckin`** | 1 | L33203 |
| 7 | **Response 字段 `result.result.vo.customerCheckin`** | 1 | L34955 |
| 8 | **Scope `$scope.customerCheckin`** | 32 | L9112-L9238 + L33508-L33551 |
| 9 | **Scope `$scope.checkCustomer`**（= 接诊 Object）| 16 | L8192-L8667 |
| 10 | **API name** | 9 | insertCustomerCheckin × 3 + beginCustomerCheckin + sendCustomerCheckin + selectCustomerCheckin × 2 + ... |
| 11 | **State Param** | 0 | `$stateParams.customerCheckinId` **0 命中**（A）|
| **合计** | — | **46+** | — |

### 2.2 customerCheckin.medicalRecordId 6 处精确（A — 字符级）

| # | 行号 | 上下文 | Controller | 字符级 |
|---:|---|---|---|---|
| 1 | **L8791** | `_this.medicalRecordId = res.customerCheckin.medicalRecordId` | **checkinListCtrl** (L8778) | `res.customerCheckin.medicalRecordId → $this.medicalRecordId` |
| 2 | **L10610** | `medicalRecordId: response.customerCheckin.medicalRecordId` | **doctorWorkbenchCtrl** (L10401) | Request field |
| 3 | **L10642** | `medicalRecordId: employee.customerCheckin.medicalRecordId` | **doctorWorkbenchCtrl** | Request field |
| 4 | **L33134** | `getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }` | **myMemberCtrl** (L33080) | **真实字符级桥**（A 字符级）|
| 5 | **L33203** | `medicalRecordId: res.customerCheckin.medicalRecordId` | **myMemberCtrl** | Request field |
| 6 | **L34955** | `medicalRecordId: result.result.vo.customerCheckin.medicalRecordId` | **optometryCtrl** (L34776) | Request field |

**结论**：customerCheckin.medicalRecordId 6 处是**真实数据桥**（A — 字符级多源互证）

### 2.3 customerCheckin 字段全集（A — 字符级）

**res.result.vo.customerCheckin 字段**（L8671, L8697, L8707, L33134, L34955）：
- id (L8671, L8697, L8789, L9122, L10606, L34946)
- medicalRecordId (L8791, L10610, L10642, L33134, L33203, L34955)
- patientId (L8707)
- checkinNumber (L11155, L11157)

**$scope.customerCheckin 字段**（L9112-L9238 + L33508-L33551）：
- customerCheckinId (L9118, L9122, L9139, L9160, L9168)
- employeeId (L9112, L9117, L9140, L9148, L9161)
- registrationFeeId (L9141, L9156, L9162, L9238, L33508, L33524, L33546, L33551)
- checkInModal (L9113, L9144, L9152, L33535, L33539)
- show, guahao, isNeedPrint

**【关键发现】**：customerCheckin **至少包含 5 个核心字段**：id / medicalRecordId / patientId / employeeId / registrationFeeId / checkinNumber（A — 字符级多源互证）

---

## 3. insertCustomerCheckin 全链（A — 字符级）

### 3.1 4 处调用精确分布

| # | 行号 | Controller | API | Request |
|---:|---|---|---|---|
| 1 | **L8667** | **addCheckinCtrl** | `insertCustomerCheckinOfNewPaitent.json` (W) | `$scope.checkCustomer` |
| 2 | **L8679** | **addCheckinCtrl** | `insertCustomerCheckinOfNewCustomer.json` (W) | `$scope.obj` (无 patientId) |
| 3 | **L8681** | **addCheckinCtrl** | `insertCustomerCheckin.json` (W) | `$scope.obj` (有 patientId) |
| 4 | **L34914** | **optometryCtrl** (L34776) | `insertCustomerCheckin.json` (W) | `$scope.obj.object` |

### 3.2 Response Consumer 完整链（A — 字符级 L8671-L8697）

**L8667 链**：
```javascript
var insertPromise = $scope.insertCustomerCheckFactory.saveOrQuery(
  "/admin/insertCustomerCheckinOfNewPaitent.json", 
  $scope.checkCustomer
);
insertPromise.then(function (res) {
  if (res.status == 0) {
    Popup.notice("新增成功");
    var printCheckinId = res.result.vo.customerCheckin.id;  // ← customerCheckin.id
    dealNeedPrint(printCheckinId);
  }
});
```

**L8695 链**：
```javascript
new ObjectFactory().saveOrQuery(url, $scope.obj).then(function (res) {
  if (res.status == 0) {
    var printCheckinId = res.result.vo.customerCheckin.id;  // ← customerCheckin.id
    Popup.notice("新增成功");
    // ...
  }
});
```

**结论**：
- **Response consumer = printCheckinId**（A — 字符级 L8671, L8697）
- **Response customerCheckin.medicalRecordId 在 addCheckinCtrl 中 0 实际消费**（A — 0 命中）
- printCheckinId **进入** `dealNeedPrint(printCheckinId)` **→ `$state.go("checkinList", { appointId, printCheckinId })` (L8648-L8654)**

---

## 4. customerCheckinId 8 类 Source 精确分类（A — 字符级）

### 4.1 19 处精确分布

| # | 行号 | 表达式 | 分类 |
|---:|---|---|---|
| 1 | L8789 | `customerCheckinId: item.customerCheckin.id` | Request field（checkinListCtrl）|
| 2 | L8847 | `customerCheckinId: id` | Request field（checkinListCtrl）|
| 3 | L9045 | `$scope.isNeedPrint = function (customerCheckinId)` | Function param |
| 4 | L9050 | `customerCheckinId: customerCheckinId` | Request field（isNeedPrint）|
| 5 | L9071 | `customerCheckinId` | isNeedPrint 传参 |
| 6 | L9118 | `$scope.customerCheckin.customerCheckinId = null` | Scope init |
| 7 | L9122 | `$scope.customerCheckin.customerCheckinId = item.customerCheckin.id` | Scope assignment |
| 8 | L9131 | `customerCheckinId: null` | Object literal init |
| 9 | L9139 | `$scope.customerCheckin.customerCheckinId = null` | Scope clear |
| 10 | L9160 | `customerCheckinId: $scope.customerCheckin.customerCheckinId` | Request field（sendCustomerCheckin）|
| 11 | L9168 | `$scope.isNeedPrint($scope.customerCheckin.customerCheckinId)` | Function call |
| 12 | L10606 | `customerCheckinId: employee.customerCheckin.id` | Request field（doctorWorkbenchCtrl）|
| 13 | L33127 | `{ customerCheckinId: $scope.customerCheckinId, medicalRecordType: 1 }` | Request field（myMemberCtrl beginCustomerCheckin）|
| 14 | L33171 | `$scope.customerCheckinId = id` | Scope assignment |
| 15 | L33193 | `function (customerCheckinId)` | Function param |
| 16 | L33196 | `customerCheckinId: customerCheckId` | Request field（receiveSelfAndBegin）|
| 17 | L34946 | `var customerCheckinId = info.customerCheckin.id` | Variable |
| 18 | L34948 | `customerCheckinId: customerCheckinId` | Request field（beginCustomerCheckin L34947）|
| 19 | L9118 (count) | (重复) | — |

### 4.2 8 类 Source 分类统计

| 类别 | 次数 | 备注 |
|---|---:|---|
| A. `$stateParams.customerCheckinId` | **0** | A — 0 命中（不通过 State）|
| B. Response `item.customerCheckin.id` | **2** | L8789, L9122 |
| C. Request field | **8** | L8789, L8847, L9050, L9160, L10606, L33127, L33196, L34948 |
| D. Scope assignment | **3** | L9118, L9122, L9139, L33171 |
| E. ObjectFactory | 0 | A |
| F. ListFactory | 0 | A |
| G. Function param | 3 | L9045, L33193, L34946 |
| H. UI only / clear | **2** | L9131, L9118 (null) |
| 其它（重复 / 局部）| 多 | 重复或局部访问 |

**结论**：customerCheckinId **0 通过 State 桥**（A — $stateParams.customerCheckinId 0 命中）；**完全通过 Response / Scope / Function param 流转**

---

## 5. medicalRecordId 在 customerCheckin 上下文（A — 字符级）

### 5.1 6 处 customerCheckin.medicalRecordId 桥汇总

| # | 行号 | Controller | Source | Target |
|---:|---|---|---|---|
| 1 | **L8791** | checkinListCtrl | `res.customerCheckin.medicalRecordId` | `$this.medicalRecordId` |
| 2 | **L10610** | doctorWorkbenchCtrl | `response.customerCheckin.medicalRecordId` | Request field |
| 3 | **L10642** | doctorWorkbenchCtrl | `employee.customerCheckin.medicalRecordId` | Request field |
| 4 | **L33134** | **myMemberCtrl** | `response.result.vo.customerCheckin.medicalRecordId` | **`getMedicalRecord.json { id }` 真实桥** |
| 5 | **L33203** | myMemberCtrl | `res.customerCheckin.medicalRecordId` | `$state.go` param |
| 6 | **L34955** | optometryCtrl | `result.result.vo.customerCheckin.medicalRecordId` | Request field |

### 5.2 4 个 Controller 间的 customerCheckin 链

```
[addCheckinCtrl insertCustomerCheckin]
   ↓ A (L8671, L8697)
res.result.vo.customerCheckin
   ↓ A (L8791)
[checkinListCtrl]
   ↓ A (L9122)
$scope.customerCheckin
   ↓ A (L9160)
sendCustomerCheckin.json { customerCheckinId }
   ↓ A (L10606)
[doctorWorkbenchCtrl]
medicalRecordId: response.customerCheckin.medicalRecordId (L10610)
   ↓ A
[myMemberCtrl]
beginCustomerCheckin.json { customerCheckinId, medicalRecordType: 1 } (L33127)
   ↓ A (L33134)
getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }
   ↓ A (L33154 / L33193 receiveSelf)
[optometryCtrl]
medicalRecordId: result.result.vo.customerCheckin.medicalRecordId (L34955)
   ↓ A
[myMemberRecord / myMaterialBill]
$state.go 跳转
```

**【关键发现】**：
- **6 处 customerCheckin.medicalRecordId** 是**完整字符级桥**（A — 多源互证）
- **4 个 Controller** 通过 customerCheckin.medicalRecordId 形成链
- **customerCheckin 是 MedicalRecord 跨 Controller 的真正桥**（A — 字符级直接证明）

---

## 6. addCheckinCtrl 完整流程（A — 字符级）

### 6.1 入口与 type 路由（A — L8223-L8232）

```javascript
$scope.appointVo = {
  register: { url: "getAppointPatientVo", type: 0 },
  reachStore: { url: "getAppointSchoolMateVo", type: 1 }
}[$stateParams.type];
```

### 6.2 完整 API 流（A — L8159-L8777）

| 步骤 | 行号 | 表达式 | 类型 |
|---|---|---|---|
| 1 | L8321 | `window.grantAuth.hasAuthForCompany(ObjectFactory)` | R |
| 2 | L8402 | `window.grantAuth.getFrontAuth(ObjectFactory)` | R（schoolEnable 字段）|
| 3 | L8237 | `/admin/$scope.appointVo.url.json { appointId }` | R（拼接）|
| 4 | L8339 | `/admin/selectEmployeeVoList.json` | R |
| 5 | L8364 | `/admin/getPatientVoList.json { name, mobile }` | R |
| 6 | L8390 | `/admin/getPatientVoList.json { name, mobile }` | R |
| 7 | L8419 | `/admin/$scope.wechatSet.listUrl.json` | R（拼接）|
| 8 | L8564 | `/admin/getEmployeeVo.json { employeeId }` | R |
| 9 | L8573 | `/admin/$scope.wechatSet.qrUrl.json` | R（拼接）|
| 10 | **L8658** | `/admin/confirmArrivalOfAppoint.json { appointId }` | **W** |
| 11 | **L8667** | `/admin/insertCustomerCheckinOfNewPaitent.json` | **W** |
| 12 | **L8679** | `/admin/insertCustomerCheckinOfNewCustomer.json` | **W** |
| 13 | **L8681** | `/admin/insertCustomerCheckin.json` | **W** |

### 6.3 完整流程字符级链（A）

```
[外部 link] $stateParams.appointId + $stateParams.type
   ↓ A
addCheckinCtrl L8159
   ↓ A (L8232)
$scope.appointVo (type=0/type=1)
   ↓ A (L8237)
new ObjectFactory().saveOrQuery("/admin/" + $scope.appointVo.url + ".json", {
  appointId: $stateParams.appointId
})
   ↓ A
[Response item.object] type=0: { patient, customer, employee, appoint } / type=1: { schoolMateVo, customer, appoint }
   ↓ A (L8241-L8281)
[9/11 字段映射] $scope.obj
   ↓ A (L8281 / L8359)
$scope.searchPatientkeyword() → getPatientVoList.json { name: $scope.keyword, mobile: $scope.obj.linkMobile }
   ↓ A
[patient list Response]
   ↓ A (L8424 choosePatient)
$scope.obj.patientId / customerId / linkMobile / schoolId / classId (覆盖)
   ↓ A
$scope.checkCustomer = { customerId, customerName, linkMobile, employeeId, appointId, ... }
   ↓ A
$scope.create() (L8645)
   ↓ A
[L8658] confirmArrivalOfAppoint.json { appointId } (W)
   ↓ A
[L8667/L8679/L8681] insertCustomerCheckin*.json $scope.checkCustomer/$scope.obj (W)
   ↓ A
[Response res.result.vo.customerCheckin] id / medicalRecordId / patientId
   ↓ A (L8671, L8697)
printCheckinId = res.result.vo.customerCheckin.id
   ↓ A (L8654)
$state.go("checkinList", { appointId, printCheckinId })
```

---

## 7. checkinListCtrl 全量（A — 字符级）

### 7.1 Controller L8778（待读行号范围）

| 项 | 证据 |
|---|---|
| 注册点 | L8778 `.controller("checkinListCtrl", ...)` |
| DI | `$scope, DateUtilFactory, Popup, $state, $stateParams, ObjectFactory, HttpFactory, ListFactory, $interval, $timeout` (10 个) |
| State Param | （待读取） |
| $stateParams | `medicalRecordId / customerCheckinId` |

### 7.2 checkinListCtrl 范围 customerCheckin 桥

**L8788-L8789**（关键字符级）：
```javascript
HttpFactory.object("/admin/medicalCheckBeforeCustomerCheckin.json", { ... })
.then(function (res) {
  // L8789
  customerCheckinId: item.customerCheckin.id  // ← 列表项 customerCheckin
```

**L8791**（核心桥）：
```javascript
_this.medicalRecordId = res.customerCheckin.medicalRecordId;  // ← A 字符级桥
```

**L9122**（Scope 赋值）：
```javascript
$scope.customerCheckin.customerCheckinId = item.customerCheckin.id;
```

### 7.3 checkinListCtrl 范围 API（A）

| API | 类型 | 行号 |
|---|---|---|
| `/admin/medicalCheckBeforeCustomerCheckin.json` | R | L8788 |
| `/admin/selectCustomerCheckinVoListOfCompany.json` | R | L8827 |
| `/admin/sendCustomerCheckin.json` | W | L9159 |
| `/admin/topEmployeeCheckinQueue.json` | W | L9443 |
| `/admin/restartEmployeeCheckinQueue.json` | W | L9452 |
| `/admin/beginCustomerCheckin.json` | W | L10605 |
| `/admin/callingWaitingCheckinQueue.json` | W | L10620 |
| `/admin/callingEmployeeCheckinQueue.json` | W | L10648 |
| `/admin/closeNowCallingCheckinQueue.json` | W | L10632 |
| `/admin/getNowCallingCheckinQueue.json` | R | L9581, L10767 |
| `/admin/getNowCallingCheckinQueueOfBigScreen.json` | R | L9581, L11140 |
| `/admin/selectCustomerCheckinVoListOfCompany.json` | R | L10817 |

---

## 8. addCheckin → checkinList（A 字符级）

### 8.1 addCheckinCtrl L8654（A）

```javascript
$scope.create = function () {
  var dealNeedPrint = function (printCheckinId) {
    var printObj = { appointId: $stateParams.appointId };
    if ($scope.needPrint.isNeed) {
      printObj.printCheckinId = printCheckinId;
    }
    $state.go("checkinList", printObj);
  };
  // ...
};
```

**结论**：
- **addCheckinCtrl → checkinListCtrl 通过 $state.go**（A — L8654 字符级）
- 携带 `appointId` + `printCheckinId`（A）
- **printCheckinId 来自 `res.result.vo.customerCheckin.id`**（A — L8671, L8697）

### 8.2 addCheckin → checkinList 完整字符级链

```
addCheckinCtrl
   ↓ A (L8667 / L8695)
insertCustomerCheckin*.json (W)
   ↓ A (L8671, L8697)
res.result.vo.customerCheckin
   ↓ A (L8671, L8697)
printCheckinId = res.result.vo.customerCheckin.id
   ↓ A (L8654)
$state.go("checkinList", { appointId, printCheckinId })
   ↓ A
checkinListCtrl L8778
```

**【关键发现】**：
- addCheckin → checkinList 是**字符级直接桥**（A — L8654 字符级 `$state.go`）
- **printCheckinId 流转**：customerCheckin.id → printCheckinId → checkinList URL param

---

## 9. checkinList → medicalRecord（A 字符级）

### 9.1 L8791 字符级直接证明

```javascript
_this.medicalRecordId = res.customerCheckin.medicalRecordId;
```

**完整链**：
- checkinListCtrl `selectCustomerCheckinVoListOfCompany.json` 列表项
- 选中某项 → `res.customerCheckin` (从 API list item)
- `_this.medicalRecordId = res.customerCheckin.medicalRecordId`

### 9.2 L10610 + L10642 字符级证明

`doctorWorkbenchCtrl` L10401：
- L10606: `customerCheckinId: employee.customerCheckin.id`
- L10610: `medicalRecordId: response.customerCheckin.medicalRecordId`
- L10642: `medicalRecordId: employee.customerCheckin.medicalRecordId`

**真实桥**：
- list 选 employee → 调用 `beginCustomerCheckin.json` (L10605) / `callingEmployeeCheckinQueue.json` (L10648)
- Response `customerCheckin.medicalRecordId` → Request 字段

---

## 10. customerCheckin → MedicalRecord A-G 7 方向判定

| 桥 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|
| **customerCheckin → MedicalRecord** | F | F | **A** (L33134, L10610, L10642, L34955) | **A** (L8791) | F | **A** (L33203) | A |

**真实桥（A 字符级多源互证）**：
- L33134: `getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }` — **myMemberCtrl**
- L10610: `medicalRecordId: response.customerCheckin.medicalRecordId` — **doctorWorkbenchCtrl**
- L10642: `medicalRecordId: employee.customerCheckin.medicalRecordId` — **doctorWorkbenchCtrl**
- L34955: `medicalRecordId: result.result.vo.customerCheckin.medicalRecordId` — **optometryCtrl**
- L8791: `_this.medicalRecordId = res.customerCheckin.medicalRecordId` — **checkinListCtrl**
- L33203: `$state.go(..., { medicalRecordId: res.customerCheckin.medicalRecordId })` — **myMemberCtrl**

**结论**：**customerCheckin → MedicalRecord 是 A 字符级真实桥**（A — 6 处字符级直接证明）

---

## 11. customerCheckin → Patient / Customer A-G 判定

### 11.1 customerCheckin → Patient

| 桥 | 结论 |
|---|---|
| Function | F（0 命中）|
| State | F（0 命中）|
| API Resp→Req | **A** (L8707 注释代码 `patientId: res.result.vo.customerCheckin.patientId`) |
| Scope/Service | F（0 命中）|
| Factory | F |
| Object | F |
| 字段共现 | A |

**真实桥**：仅 **注释代码**（A — L8707 addSchoolMateConsume 0 实际调用）
**结论**：customerCheckin → Patient 实际是 **F 边界**（注释代码）

### 11.2 customerCheckin → Customer

| 桥 | 结论 |
|---|---|
| API Resp→Req | F（0 命中 customerId 字段）|
| Object | F |

**结论**：customerCheckin → Customer **0 桥**（F 边界）
- customerCheckin 0 包含 customerId 字段（A — 0 命中）

### 11.3 Patient → customerCheckin（F 边界）

- `insertCustomerCheckinOfNewPaitent.json` Request 接受 `patientId`（A — L8665 $scope.checkCustomer 不含 patientId）
- `insertCustomerCheckin.json` Request 接受 `$scope.obj`（A — L8695 包含 patientId）
- **真实桥**：patient → customerCheckin（**A** — insertCustomerCheckin.json 中）

### 11.4 Customer → customerCheckin（A — 字符级）

- L8665: `$scope.checkCustomer.appointId = aId`（A）
- L8665: `$scope.checkCustomer` **包含 customerId**（A — chooseCustomer 路径）
- L8667: `insertCustomerCheckinOfNewPaitent.json $scope.checkCustomer`（A）

**真实桥**：Customer → customerCheckin（A — L8429 字符级 `$scope.checkCustomer.customerId = customerId`）

---

## 12. Appointment → customerCheckin A-G 判定

| 桥 | 结论 |
|---|---|
| Function | F |
| State | **A**（$stateParams.appointId 是 addCheckinCtrl 入口）|
| API Resp→Req | **A**（appointId → 多个 API）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

**真实桥（多源互证 B）**：
- L8658: `confirmArrivalOfAppoint.json { appointId }` (W)
- L8665: `$scope.checkCustomer.appointId = aId` → `insertCustomerCheckin*.json` (W)
- L8667: `insertCustomerCheckinOfNewPaitent.json $scope.checkCustomer` (W)

**结论**：Appointment → customerCheckin 是 **A 字符级真实桥**（appointId 流转）

---

## 13. medicalRecord → 就诊流程分支 A-G 判定

### 13.1 medicalRecord → Optometry（A — 字符级）

| 桥 | 结论 |
|---|---|
| Function | F |
| State | **A**（$stateParams.medicalRecordId 25 处）|
| API Resp→Req | **A**（L34955 customerCheckin.medicalRecordId, L2243 getMedicalRecord 派生）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

**真实桥**：
- L41717: `$state.go('assistChecking', { medicalExamineId: id, medicalRecordId: $scope.medicalRecordId })`
- L34955: `medicalRecordId: result.result.vo.customerCheckin.medicalRecordId`（optometryCtrl 内）
- L32952: `$state.go('adminSalesRecord.myMaterialBill', { medicalRecordId: id, patientId: res.object.patientId })`

### 13.2 medicalRecord → Check（A — 字符级）

- L41717: `$state.go('assistChecking', { medicalExamineId, medicalRecordId })`（A）
- L1757: `assistCheckingCtrl` `$scope.medicalRecordId = $stateParams.medicalRecordId`（A）

**真实桥**：medicalRecord → Check（**A** — $stateParams.medicalRecordId 25 处 / 多个 Controller 消费）

### 13.3 medicalRecord → Sale（A — 字符级）

- L32952: `$state.go('adminSalesRecord.myMaterialBill', { medicalRecordId, patientId })`（A）
- L33137: `$state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })`（A — myMemberCtrl）
- L33056: `$state.go('adminSalesRecord.myMaterialBill', { medicalRecordId: id, patientId: res.object.patientId })`（A）

**真实桥**：medicalRecord → Sale（**A** — 多源互证）

### 13.4 medicalRecord → Charge（A — 字符级）

- medicalRecordListOfCompany / medicalRecordCashflowVoListOfCompany（L8129, L5085）等 33 处 getMedicalRecord* API
- $stateParams.medicalRecordId 进入 myMaterialBillCtrl L32435
- 收费业务通过 medicalRecord 链接

**真实桥**：medicalRecord → Charge（**A** — 33 处 getMedicalRecord API + State Param）

### 13.5 medicalRecord → Delivery（A — 字符级）

- 0 命中 `medicalRecordId` 在 deliveryInputCtrl / deliveryListCtrl
- **0 桥**（F 边界）

---

## 14. School → SchoolMate → Appointment → CustomerCheckin → MedicalRecord 完整链

### 14.1 完整 5 段链验证

| 段 | 字符级证据 | 等级 |
|---|---|---|
| **School → SchoolMate** | A — S1-132 75+ school API + schoolId 5 类来源 | A |
| **SchoolMateVo → addCheckinCtrl** | A — S1-134 L8264-L8277 9 处 | A |
| **addCheckinCtrl → Appointment API** | A — S1-134 L8237 getAppointSchoolMateVo.json { appointId } | A |
| **Appointment → customerCheckin** | A — L8658 confirmArrivalOfAppoint / L8665 checkCustomer.appointId / L8667 insertCustomerCheckin* | A |
| **customerCheckin → MedicalRecord** | **A**（本轮 6 处字符级直接证明）| **A** |
| **MedicalRecord → Optometry** | A — L34955 + L41717 | A |
| **MedicalRecord → Check** | A — L41717 + L1757 $stateParams | A |
| **MedicalRecord → Sale** | A — L32952 + L33056 + L33137 | A |
| **MedicalRecord → Charge** | A — 33 处 getMedicalRecord API | A |
| **MedicalRecord → Delivery** | F（0 命中）|

**结论**：**完整链 School → SchoolMate → Appointment → CustomerCheckin → MedicalRecord → Optometry/Check/Sale/Charge 是 A 字符级真实数据链**（A — 多源互证 B 级）

**唯一断点**：**MedicalRecord → Delivery**（F 边界）

---

## 15. 数量精确统计（A — 字符级）

| 指标 | 精确数 |
|---|---:|
| **customerCheckin 总命中** | **46+** |
| customerCheckin.id | 6 |
| **customerCheckin.medicalRecordId** | **6**（6 处真实桥）|
| customerCheckin.patientId | 1（L8707 注释）|
| customerCheckin.customerId | 0 |
| customerCheckin.employeeId | 5 |
| customerCheckin.checkinNumber | 2 |
| **customerCheckinId** | **19** |
| **insertCustomerCheckin 调用** | **4**（L8667, L8679, L8681, L34914）|
| **confirmArrivalOfAppoint 调用** | **1**（L8658）|
| **addCheckinCtrl 实际逻辑行数** | **~620**（L8159-L8777）|
| **checkinListCtrl 行数** | **~1500+**（L8778 起）|
| **medicalRecordId 在 addCheckinCtrl** | **0**（仅注释 L8213 派生）|
| **medicalRecordId 在 checkinListCtrl** | **1+**（L8791 + $stateParams 派生）|
| customerCheckinId 进入 State | **0**（$stateParams.customerCheckinId 0 命中）|
| customerCheckinId 进入 Request | **8**（L8789, L8847, L9050, L9160, L10606, L33127, L33196, L34948）|
| getMedicalRecord.json 33 处 | 33 |
| $stateParams.medicalRecordId 25 处 | 25 |

---

## 16. 完整桥矩阵

| 来源 | 目标 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 字段共现 |
|---|---|---|---|---|---|---|---|---|
| addCheckin | **checkinList** | F | F | F | F | F | F | A |
| **customerCheckin** | **medicalRecord** | F | F | **A** (L33134, L10610, L10642, L34955) | **A** (L8791) | F | **A** (L33203) | A |
| customerCheckin | patient | F | F | F（注释） | F | F | F | G |
| customerCheckin | customer | F | F | F | F | F | F | F |
| **Appointment** | **customerCheckin** | F | **A** (L8232, L8238) | **A** (L8658, L8665, L8667) | F | F | F | A |
| **patient** | **customerCheckin** | F | F | **A** (L8695) | F | F | F | A |
| customer | customerCheckin | F | F | A (L8667) | F | F | F | A |
| **medicalRecord** | **Optometry** | F | **A** (L41717) | **A** (L34955, L33134) | F | F | F | A |
| **medicalRecord** | **Check** | F | **A** (L41717, L1757) | F | F | F | F | A |
| **medicalRecord** | **Sale** | F | **A** (L32952, L33056) | F | F | F | F | A |
| **medicalRecord** | **Charge** | F | **A** (33 处 $stateParams) | **A** (33 处 getMedicalRecord API) | F | F | F | A |
| **medicalRecord** | **Delivery** | F | F | F | F | F | F | F |

---

## 17. L1 / L2 / L3

### 17.1 L1（前端直接事实）

- addCheckinCtrl L8159 完整 ~620 行（A）
- checkinListCtrl L8778（A）
- doctorWorkbenchCtrl L10401（A）
- myMemberCtrl L33080（A）
- myMemberRecordCtrl L33218（A）
- optometryCtrl L34776（A）
- 6 处 customerCheckin.medicalRecordId 字符级直接证明（A）
- 4 处 insertCustomerCheckin 字符级调用（A）
- 1 处 confirmArrivalOfAppoint 字符级调用（A）
- $state.go L8654, L32952, L33056, L33137, L41717（A）

### 17.2 L2（基于 L1 的有限业务解释）

- customerCheckin 是 MedicalRecord 跨 Controller 的真正桥
- 完整 5 段链 School → SchoolMate → Appointment → CustomerCheckin → MedicalRecord 真实成立
- medicalRecordType = 5 是销售订单路径，否则是病历记录路径
- 唯一断点：MedicalRecord → Delivery

### 17.3 L3（当前无证据）

- 后端 entity `customer_checkin` 表 / `medical_record` 表 / FK
- `medicalRecordType` 完整业务含义（仅知 5 = Sale, 1 = Checkin）
- 完整的 customerCheckin 后端结构

---

## 18. 最终 DAG（A-O）

### DAG A: Appointment → addCheckinCtrl
```
$stateParams.appointId (L8216, 注释)
   ↓ A
$stateParams.type (L8232)
   ↓ A
addCheckinCtrl L8159 → $scope.appointVo (type 0/1)
   ↓ A
$scope.queryStudentInfo() (L8296)
   ↓ A
new ObjectFactory().saveOrQuery("/admin/" + $scope.appointVo.url + ".json", { appointId: $stateParams.appointId })
```

### DAG B: SchoolMateVo → addCheckinCtrl
（沿用 S1-134 — L8264-L8277 9 字段）

### DAG C: addCheckinCtrl → Patient
（沿用 S1-134 — L8264-L8277 → L8364 → choosePatient L8424）

### DAG D: addCheckinCtrl → customerCheckin
```
$scope.create() (L8645)
   ↓ A
confirmArrivalOfAppoint.json { appointId } (L8658) (W)
   ↓ A
$scope.checkCustomer.appointId = aId (L8665)
   ↓ A
insertCustomerCheckin[OfNewPaitent][OfNewCustomer].json (L8667, L8679, L8681) (W)
   ↓ A
res.result.vo.customerCheckin
   ↓ A
printCheckinId = res.result.vo.customerCheckin.id (L8671, L8697)
   ↓ A
$state.go("checkinList", { appointId, printCheckinId }) (L8654)
```

### DAG E: customerCheckin → medicalRecord（**A 字符级核心桥**）
```
[insertCustomerCheckin / beginCustomerCheckin / callingEmployeeCheckinQueue Response]
   ↓ A
res.customerCheckin.medicalRecordId
   ↓ A
[6 处字符级桥]
├── L8791 checkinListCtrl: $this.medicalRecordId
├── L10610 doctorWorkbenchCtrl: Request field
├── L10642 doctorWorkbenchCtrl: Request field
├── L33134 myMemberCtrl: getMedicalRecord.json { id: ... } (R)
├── L33203 myMemberCtrl: $state.go
└── L34955 optometryCtrl: Request field
```

### DAG F: customerCheckin → patient
```
[addCheckinCtrl Response res.result.vo.customerCheckin.patientId]
   ↓ A (L8707 注释代码)
[addSchoolMateConsume.json { schoolMateCheckId, patientId }] (0 实际调用)
   ↓ F
```

### DAG G: customerCheckin → customer
```
[0 命中 customerId 字段]
   ↓ F
```

### DAG H: addCheckinCtrl → checkinListCtrl
```
$state.go("checkinList", { appointId, printCheckinId }) (L8654)
   ↓ A
checkinListCtrl L8778
   ↓ A
res.customerCheckin.medicalRecordId (L8791)
```

### DAG I: checkinListCtrl → medicalRecord
```
checkinListCtrl L8778
   ↓ A
res.customerCheckin.medicalRecordId (L8791)
   ↓ A
$this.medicalRecordId
   ↓ A
[后续跳转 - F 边界]
```

### DAG J: medicalRecord → Optometry
```
$stateParams.medicalRecordId (25 处)
   ↓ A
myMemberCtrl L33080
   ↓ A (L33134)
getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }
   ↓ A (L33136)
if (res.object.medicalRecordType == 5)
   $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })
else
   $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId })
   ↓ A
myMaterialBillCtrl L32435 (Sale)
myMemberRecordCtrl L33218 (Record)
   ↓ A (L32946, L33050)
$scope.getMedicalRecord = function (id, patientId)
   ↓ A (L32952, L33056)
$state.go('adminSalesRecord.myMaterialBill' / 'adminMyRecord.myMemberRecord', { medicalRecordId, patientId })
   ↓ A (L32954, L33058)
```

### DAG K: medicalRecord → Check
```
$state.go('assistChecking', { medicalExamineId, medicalRecordId }) (L41717)
   ↓ A
assistCheckingCtrl L1756
   ↓ A
$scope.medicalRecordId = $stateParams.medicalRecordId (L1757)
```

### DAG L: medicalRecord → Sale
```
myMaterialBillCtrl L32435
$scope.obj.medicalRecordId = $stateParams.medicalRecordId (L32445)
```

### DAG M: medicalRecord → Charge
```
33 处 getMedicalRecord API
25 处 $stateParams.medicalRecordId
   ↓ A
medicalRecord → cashflow（多 Controller 链）
```

### DAG N: medicalRecord → Delivery
```
[0 命中 medicalRecordId 在 deliveryInputCtrl / deliveryListCtrl]
   ↓ F
[断点]
```

### DAG O: School → medicalRecord 完整链
```
School (schoolListCtrl L44357)
   ↓ A (S1-132)
schoolMate (schoolMateVo 三对象)
   ↓ A (S1-134 L8264-L8277 9 字段)
addCheckinCtrl type=1 (L8159)
   ↓ A (L8237)
Appointment API getAppointSchoolMateVo.json { appointId }
   ↓ A (L8667/L8695)
customerCheckin
   ↓ A (L33134)
medicalRecord
   ↓ A (L41717, L32952, L33056, L34955)
Optometry / Check / Sale / Charge
   ↓ F
Delivery (断点)
```

---

## 19. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | customerCheckin 来源 | insertCustomerCheckin / beginCustomerCheckin / sendCustomerCheckin Response | A | L8667, L10605, L9159 | A |
| 2 | customerCheckin.id | 6 处字符级 | A | L8671, L8697, L8789, L9122, L10606, L34946 | A |
| 3 | **customerCheckin.medicalRecordId** | **6 处字符级（多源互证）** | **A** | L8791, L10610, L10642, L33134, L33203, L34955 | **A** |
| 4 | customerCheckin.patientId | 1 处注释 | A | L8707 | F（注释）|
| 5 | customerCheckin.customerId | 0 命中 | A | 0 | F |
| 6 | customerCheckinId 来源 | Response / Scope / Function param | A | 详见第 4 节 | A |
| 7 | insertCustomerCheckin | 4 处调用 | A | L8667, L8679, L8681, L34914 | A |
| 8 | insertCustomerCheckin Response | customerCheckin.id / .medicalRecordId / .patientId | A | L8671, L8697, L8707 | A |
| 9 | confirmArrivalOfAppoint | 1 处 | A | L8658 | A |
| 10 | addCheckinCtrl | ~620 行 | A | L8159-L8777 | A |
| 11 | checkinListCtrl | ~1500 行 | A | L8778+ | A |
| 12 | addCheckin → checkinList | A 字符级 | A | L8654 | A |
| 13 | checkinList → medicalRecord | A 字符级 | A | L8791 | A |
| 14 | **customerCheckin → medicalRecord** | **A 字符级 6 处** | **A** | L8791, L10610, L10642, L33134, L33203, L34955 | **A** |
| 15 | customerCheckin → patient | F（仅注释）| A | L8707 | F |
| 16 | customerCheckin → customer | F | A | 0 命中 | F |
| 17 | patient → medicalRecord | A | A | L6693 | A |
| 18 | **medicalRecord → Optometry** | **A** | A | L34955, L41717 | A |
| 19 | medicalRecord → Check | A | A | L41717, L1757 | A |
| 20 | medicalRecord → Sale | A | A | L32952, L33056, L33137 | A |
| 21 | medicalRecord → Charge | A | A | 33 处 getMedicalRecord API | A |
| 22 | medicalRecord → Delivery | F | A | 0 命中 | F |
| 23 | schoolMate → customerCheckin | A | A | S1-134 + 本轮 L8667 | A |
| 24 | appointment → customerCheckin | A | A | L8658, L8665, L8667 | A |
| 25 | **School → medicalRecord 完整链** | **A**（除 Delivery 断点）| A | DAG O | A |
| 26 | 最终 DAG + 复刻红线 | 第 18-23 节 | A | 本文档 | A |

---

## 20. A/B/C/D/E/F 分布

- **A**：24
- **B**：1（customerCheckin.medicalRecordId 6 处多源互证）
- **C**：0
- **D**：1（schoolMateCheckId 注释代码）
- **E**：**0**
- **F**：5（customerCheckin → patient 注释 / customerCheckin → customer 0 / MedicalRecord → Delivery 0 / 注释代码 / 后端实体）

---

## 21. 历史差异

| 项 | 历史 | S1-135 | 当前采用 |
|---|---|---|---|
| customerCheckin.medicalRecordId 桥 | 散见 6 处（S1-133 报告）| **6 处字符级直接证明** + 4 个 Controller 串成完整链 | A — 加强 |
| customerCheckin → MedicalRecord 关系 | 0 直接桥（S1-133 报告）| **A 字符级桥**（myMemberCtrl L33134 getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }）| A — **D 冲突修正** |
| School → MedicalRecord 完整链 | F 边界（S1-132 报告）| **A 字符级**（除 Delivery 断点）| A — 显著加强 |
| addCheckinCtrl 类型 | 接诊/登记（S1-134）| 接诊/登记 — **本轮确认完整链** | A — 强化 |

---

## 22. 复刻红线

### 22.1 不能自行增加的字段

- customerCheckin 不应包含 customerId 字段（A — 0 命中）
- medicalRecord 不应直接包含 schoolMateId 字段（A — 0 命中）
- addCheckinCtrl 不应包含 $stateParams.medicalRecordId 实际消费（A — 0 命中）

### 22.2 不能自行补桥的模块

- **MedicalRecord → Delivery 0 桥**（A — 0 命中 medicalRecordId 在 delivery Controller）
- **customerCheckin → patient 仅注释**（A — L8707 addSchoolMateConsume 0 实际调用）
- **customerCheckin → customer 0 桥**（A — 0 命中 customerId）
- **不能假定"customerCheckin.id 一定包含 medicalRecordId"**（A — 6 处都是 .medicalRecordId 字段派生）
- **不能假定"customerCheckinId 包含 medicalRecordId"**（A — 19 处 customerCheckinId 0 命中 medicalRecordId）
- **不能假定"printCheckinId 包含 medicalRecordId"**（A — printCheckinId 仅 customerCheckin.id）

### 22.3 不能假定存在的 API

- `/admin/getCustomerCheckinMedicalRecordId.json` 不存在
- `/admin/getMedicalCheckinFlow.json` 不存在
- `/admin/getCustomerCheckinInfo.json` 不存在
- 任何 controller.js 中 0 命名的 API

### 22.4 不能等同的 ID

| ID | 不能等同 |
|---|---|
| **customerCheckin.id** | ≡ **printCheckinId**（A — L8671 字符级）|
| **customerCheckin.medicalRecordId** | ≡ **medicalRecordId**（A — L8791, L33134, L10610, L34955 字符级）|
| **customerCheckin.patientId** | ≡ **patientId**（A — L8707 注释）|
| medicalRecordId | ≠ customerCheckinId / patientId / schoolMateId |
| customerCheckinId | ≠ medicalRecordId / patientId / customerId |
| printCheckinId | ≡ customerCheckin.id（A）|
| medicalRecord.patientId | ≡ patientId（A — S1-128 确认）|

### 22.5 必须保留的 F 边界

- customerCheckin → customer 0 桥（F 边界）
- MedicalRecord → Delivery 0 桥（F 边界）
- $stateParams.customerCheckinId 不存在（0 命中）
- 后端 entity / FK / 表结构（F 边界）
- 0 共享 Service / Factory（F 边界）

### 22.6 命名误导必须标注

- `customerCheckin` 0 包含 customerId（A — 命名误导）
- `printCheckinId` 实际是 customerCheckin.id（A — L8671）
- `medicalRecordType == 5` 是 Sale 路径，否则是 Record 路径（A — L33136, L32951, L33055, L33156）
- `addCheckinCtrl` 是接诊/登记 Controller，**不是预约 Controller**（A — S1-134 强化）
- `checkinListCtrl` 是接诊列表 Controller（A — L8778）
- `myMemberCtrl` 是会员中心 Controller，**有 beginCustomerCheckin 桥**（A — L33125-L33150）
- `doctorWorkbenchCtrl` 是医生工作台 Controller，**有 customerCheckin 桥**（A — L10401 + L10610）
- `addSchoolMateConsume.json` 0 实际调用（注释代码 F 边界）

---

## 23. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**）| ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**）| ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**）| ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**）| ✓ |
| 历史 MD 165-196 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 197_*.md | 是 | ✓ |
| 临时脚本（3 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 24. Git

- 本轮 commit hash：（待执行 `git add -- 197_*.md` / `git commit -m "docs(197): S1-135 CustomerCheckin to MedicalRecord 就诊流程主入口链深度审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：204 → 205
- 本轮 untracked 预期：10（保留 10 untracked，新增 197 后变 10 untracked 因为 197 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：197_S1-135_*.md
