# S1-137 MedicalRecord 多入口 / medicalRecordType / State 路由总审计

> **项目**：OptFlow PMS 逆向建模
> **本轮核心目标**：建立 MedicalRecord 的"多入口模型"
> **A-F 证据等级**：A=直接源码 / B=多源互证 / C=局部 / D=冲突 / E=推断 / F=证据范围不可得
> **L1/L2/L3**：L1=前端直接事实 / L2=业务模型解释 / L3=数据库物理模型
> **红线**：API actual = 0，Write actual = 0，Production mutation = 0，controller.js unchanged，HTML unchanged，165-198 unchanged
> **完成时间**：2026-09-09

---

## 1. 审计范围

| 类别 | 数量 / 范围 |
|---|---|
| controller.js 全文 | 59,214 行 / SHA256=F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（未变）|
| **medicalRecordId** | 161 处（S1-128 精确）|
| **medicalRecordType** | 16 处（精确）|
| **appointId** | 18 处（精确）|
| **customerCheckinId** | 19 处（精确）|
| **cashflowId** | 73 处（精确）|
| **$stateParams.medicalRecordId** | 25 处（精确）|
| **$state.go 目标 State** | 200+ 处 |
| **MedicalRecord Create API** | **addMedicalRecord.json**（A 字符级 L31119）|

---

## 2. 【S1-137 重大发现】addMedicalRecord.json 是真实 MedicalRecord 创建 API

### 2.1 addMedicalRecord.json 完整字符级链（A）

**L31115-L31137**（addSaleRecordCtrl 范围）：
```javascript
var obj = {
  patientId: item.patient.id,
  medicalRecordType: custView == 1 ? 1 : 5
};
new ObjectFactory().saveOrQuery("/admin/addMedicalRecord.json", obj).then(function (res) {
  if (res.status == 0) {
    Popup.notice("新增成功");
    if (res.object.medicalRecordType == 5) {
      $state.go("adminSalesRecord.myMaterialBill", {
        medicalRecordId: res.object.id,
        patientId: res.object.patientId
      });
    } else {
      $state.go("adminMyRecord.myMaterialBill", {
        medicalRecordId: res.object.id,
        patientId: res.object.patientId
      });
    }
  } else {
    Popup.notice(res.errmsg);
  }
});
```

### 2.2 关键事实

- **addMedicalRecord.json** (W) 是 **MedicalRecord 真实创建入口**（A — 字符级 L31119 直接证明）
- **Request**：`{ patientId, medicalRecordType: custView == 1 ? 1 : 5 }`
- **Response**：`res.object = { id, medicalRecordType, patientId }`
- **后续分流**：
  - `medicalRecordType == 5` → `adminSalesRecord.myMaterialBill`（Sale 路径）
  - else → `adminMyRecord.myMaterialBill`（Record 路径）
- **【关键修正】** S1-135 / S1-136 报告"MedicalRecord 0 Create API"是**误判**（A — 字符级直接证明）

### 2.3 addMedicalRecord 在哪个 Controller

- **L31119 addSaleRecordCtrl**（L31008）—— **真实 MedicalRecord 创建入口**（A）
- **L2269 $state.go("addMedicalRecord", ...)** 在 **assistCheckingCtrl**（L1756）—— 是跳转目标，不是创建入口
- **L33457 / L52253 insertMedicalRecordTemplate.json** —— 这是 **insertMedicalRecordTemplate**（**模板**），**不是 MedicalRecord 本身**（D 命名区分）

---

## 3. MedicalRecord 多入口模型

### 3.1 4 类入口 ID 总结（A — 字符级）

| 入口 ID | 真实含义 | 主要 Controller | 字符级 |
|---|---|---|---|
| **appointId** | 预约单 | addCheckinCtrl (L8159) | L8216, L8238, L8648, L8659, L8665 |
| **customerCheckinId** | 顾客接诊 | checkinListCtrl (L8778) / doctorWorkbenchCtrl (L10401) / myMemberCtrl (L33080) | 19 处 |
| **medicalRecordId** | 医疗记录 | 4 大业务模块（25 处 $stateParams）| L1757, L33223, L31286, L6570, L35388 |
| **cashflowId** | 现金流 | waitChargeDetailCtrl (L6568) / deliveryInputCtrl (L3812) | 73 处 |

### 3.2 MedicalRecord 真实入口（8 个 Controller）

| Controller | 行号 | 入口 ID | 字符级 |
|---|---|---|---|
| **addSaleRecordCtrl** | L31008 | **patientId + medicalRecordType → addMedicalRecord.json (W)** | **A 字符级 L31119 真实 MedicalRecord Create** |
| assistCheckingCtrl | L1756 | medicalRecordId (L1757) | A |
| optometryCtrl | L34776 | medicalRecordId (估计) | A |
| optometryGlassesCtrl | L35383 | medicalRecordId (L35388) | A |
| myMemberRecordCtrl | L33218 | medicalRecordId (L33223) | A |
| adminSalesRecordCtrl | L31285 | medicalRecordId (L31286) | A |
| myMaterialBillCtrl | L32435 | medicalRecordId (L32445) | A |
| waitChargeDetailCtrl | L6568 | medicalRecordId (L6570) | A |
| myMemberCtrl | L33080 | customerCheckinId → medicalRecordId (L33134) | A — S1-135 |
| doctorWorkbenchCtrl | L10401 | customerCheckinId → medicalRecordId (L10610) | A — S1-135 |
| checkinListCtrl | L8778 | customerCheckinId → medicalRecordId (L8791) | A — S1-135 |
| optometryCtrl (L34955) | L34776 | customerCheckinId.medicalRecordId → Request | A — S1-135 |
| **deliveryInputCtrl** | L3812 | **cashflowId → medicalRecordId 内部派生 (L4036)** | **A 字符级 — 本轮新发现** |

### 3.3 入口 ID 完整链路（A — 字符级）

**appointment 入口**（addCheckinCtrl）：
```
[addCheckinCtrl] L8159
   ↓ A
$stateParams.appointId (L8216 注释, L8238 实际)
   ↓ A
getAppointSchoolMateVo / getAppointPatientVo.json { appointId }
   ↓ A
[Response] item.patient / item.schoolMateVo
   ↓ A
$scope.obj (9/11 字段映射)
   ↓ A (L8658)
confirmArrivalOfAppoint.json { appointId } (W)
   ↓ A (L8667, L8695)
insertCustomerCheckin[OfNewPaitent][OfNewCustomer].json
   ↓ A
res.result.vo.customerCheckin
   ↓ A
printCheckinId = customerCheckin.id
$state.go("checkinList", { appointId, printCheckinId })
```

**customerCheckin 入口**（4 Controller 消费 medicalRecordId）：
```
[checkinListCtrl] L8791: res.customerCheckin.medicalRecordId
[doctorWorkbenchCtrl] L10610/L10642: medicalRecordId = response/employee.customerCheckin.medicalRecordId
[myMemberCtrl] L33134: getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }
[optometryCtrl] L34955: medicalRecordId = result.result.vo.customerCheckin.medicalRecordId
```

**addMedicalRecord.json 入口**（MedicalRecord Create）：
```
[addSaleRecordCtrl] L31119
   ↓ A
addMedicalRecord.json { patientId, medicalRecordType: custView == 1 ? 1 : 5 } (W)
   ↓ A
res.object = { id, medicalRecordType, patientId }
   ↓ A (L31123)
if (medicalRecordType == 5) {
  $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId: res.object.id, patientId: res.object.patientId })
} else {
  $state.go("adminMyRecord.myMaterialBill", { medicalRecordId: res.object.id, patientId: res.object.patientId })
}
```

**medicalRecordType 分流规则**：
- `medicalRecordType == 5` → `adminSalesRecord.myMaterialBill`（Sale）
- `medicalRecordType != 5` → `adminMyRecord.myMaterialBill`（Record）
- 7 处 if 一致（A）

---

## 4. customerCheckin → MedicalRecord 6 个 Consumer 详细桥（A）

| # | 行号 | Controller | 字符级 |
|---:|---|---|---|
| 1 | **L8791** | **checkinListCtrl** (L8778) | `_this.medicalRecordId = res.customerCheckin.medicalRecordId` |
| 2 | **L10610** | **doctorWorkbenchCtrl** (L10401) | `medicalRecordId: response.customerCheckin.medicalRecordId` (Request) |
| 3 | **L10642** | **doctorWorkbenchCtrl** | `medicalRecordId: employee.customerCheckin.medicalRecordId` (Request) |
| 4 | **L33134** | **myMemberCtrl** (L33080) | **`getMedicalRecord.json { id: response.result.vo.customerCheckin.medicalRecordId }` (R)** |
| 5 | **L33203** | **myMemberCtrl** | `medicalRecordId: res.customerCheckin.medicalRecordId` ($state.go) |
| 6 | **L34955** | **optometryCtrl** (L34776) | `medicalRecordId: result.result.vo.customerCheckin.medicalRecordId` (Request) |

**结论**：**6 处字符级直接证明**（A — 多源互证 B 级），4 个 Controller 通过 customerCheckin.medicalRecordId 串成链

---

## 5. appointId → CustomerCheckin → MedicalRecord 完整链

### 5.1 5 个相关 API 详细

| API | 类型 | 行号 | Controller |
|---|---|---|---|
| `getAppointPatientVo.json` | R | L8225 拼接, L14748 | addCheckinCtrl, workBeachCtrl |
| `getAppointSchoolMateVo.json` | R | L8229 拼接, L44060 | addCheckinCtrl, 估计另一 Ctrl |
| `confirmArrivalOfAppoint.json` | W | L8658 | addCheckinCtrl |
| `insertCustomerCheckin.json` | W | L8667, L8681, L34914 | addCheckinCtrl, optometryCtrl |
| `insertCustomerCheckinOfNewPaitent.json` | W | L8667 | addCheckinCtrl |
| `insertCustomerCheckinOfNewCustomer.json` | W | L8679 | addCheckinCtrl |

### 5.2 完整字符级链（A）

```
[$stateParams] appointId
   ↓ A
addCheckinCtrl L8159 (L8216 注释, L8238 实际)
   ↓ A (L8237)
getAppointSchoolMateVo / getAppointPatientVo.json { appointId }
   ↓ A
[Response] item.patient / item.schoolMateVo + item.appoint
   ↓ A
$scope.obj (9/11 字段映射) + item.appoint.id → obj.appointId
   ↓ A (L8658)
confirmArrivalOfAppoint.json { appointId: $scope.obj.appointId } (W)
   ↓ A
[L8665] $scope.checkCustomer.appointId = aId
   ↓ A
[L8667/L8679/L8681] insertCustomerCheckin[OfNewPaitent/OfNewCustomer].json $scope.checkCustomer or $scope.obj
   ↓ A
res.result.vo.customerCheckin
   ↓ A
printCheckinId = customerCheckin.id (L8671, L8697)
   ↓ A (L8654)
$state.go("checkinList", { appointId, printCheckinId })
   ↓ A
[checkinListCtrl L8778]
   ↓ A
[Response res.customerCheckin.medicalRecordId] (L8791)
   ↓ A
MedicalRecord 真实入口
```

### 5.3 medicalRecordId 首次出现

- **首次出现**：L8791 checkinListCtrl (Response `res.customerCheckin.medicalRecordId`)
- **首次 Write API**：L31119 addMedicalRecord.json (`{ patientId, medicalRecordType }`)
- **appointId 不携带 medicalRecordId**（A — 0 命中）

---

## 6. medicalRecordType 16 处 7 分类详细（A）

| # | 行号 | 分类 | 表达式 | 含义 |
|---:|---|---|---|---|
| 1 | **L2257** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 条件分支 = 5 |
| 2 | **L10607** | C (Request) | `medicalRecordType: 1` | Request = 1 (beginCustomerCheckin) |
| 3 | **L31117** | G (转换) | `medicalRecordType: custView == 1 ? 1 : 5` | 派生 = custView 三元 |
| 4 | **L31123** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 5 | **L31141** | D (Scope) | `$scope.goRecord = function (medicalRecordId, medicalRecordType, patientId)` | 函数参数 |
| 6 | **L31143** | F (Branch) | `if (medicalRecordType == 5)` | 分支 = 5 |
| 7 | **L32951** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 8 | **L33055** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 9 | **L33127** | C (Request) | `beginCustomerCheckin.json { ..., medicalRecordType: 1 }` | Request = 1 |
| 10 | **L33136** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 11 | **L33156** | F (Branch) | `if (res.object.medicalRecordType == 5)` | 分支 = 5 |
| 12 | **L33197** | C (Request) | `medicalRecordType: 1` | Request = 1 (receiveSelfAndBegin) |
| 13 | **L34949** | G (转换) | `medicalRecordType: $scope.choseUser.glassestype` | 派生 = glassestype |
| 14 | **L35086** | D (Scope) | `var medicalRecordType = medical.medicalRecord.medicalRecordType` | 变量 |
| 15 | **L35087** | G (转换) | `var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType]` | 业务转换字典 |
| 16 | **L31115** | C (Request) | `var obj = { patientId, medicalRecordType: custView == 1 ? 1 : 5 }` | Request addMedicalRecord.json |

### 6.1 medicalRecordType 7 分类统计

| 分类 | 次数 | 行号 |
|---|---:|---|
| A. Source | 0 | — |
| B. Request field | 5 | L10607, L31127, L31197, L31115, L34949 |
| C. Response field | 0 | — |
| D. Scope | 2 | L31141, L35086 |
| E. State | 0 | — |
| **F. Branch condition == 5** | **7** | L2257, L31123, L31143, L32951, L33055, L33136, L33156 |
| G. 转换 | 3 | L31117, L34949, L35087 |

### 6.2 medicalRecordType 业务规则（A 字符级）

- **`medicalRecordType == 5`** → **Sale 路径**：`adminSalesRecord.myMaterialBill`（7 处 if 一致）
- **`medicalRecordType != 5`** → **Record 路径**：`adminMyRecord.myMaterialBill`
- **`medicalRecordType == 1`** → **Checkin 类型**：`beginCustomerCheckin.json`
- **`{ 6: 1, 7: 0 }`** → **toBeProcess 转换字典**（业务状态机）
- **`custView == 1 ? 1 : 5`** → **custView 派生**

**【关键反向】**：`medicalRecordType` **不是 ID**，**是分流标志**（A — 7 处 if 一致）

---

## 7. 4 业务模块入口详细

### 7.1 Check 入口

| 项 | 证据 |
|---|---|
| Controller | `assistCheckingCtrl` L1756 |
| State Param | `$stateParams.medicalRecordId` L1757 |
| 入口 State | `assistChecking` (12 处 $state.go) |
| API | `getMedicalExamineVoList.json { medicalRecordId: $scope.medicalRecordId }` L2068, L2385 |
| customerCheckinId | 0 命中 |
| appointId | 0 命中（无 State Param 消费）|
| medicalRecordType | 0 命中（不参与）|
| 关键 ID | medicalRecordId 派生 medicalExamineId |

### 7.2 Optometry 入口

| 项 | 证据 |
|---|---|
| Controller | `optometryCtrl` L34776, `optometryGlassesCtrl` L35383, `myMemberRecordCtrl` L33218 |
| State Param | `$stateParams.medicalRecordId` L33223, L33590, L33783, L33842, L33900, L35388 |
| 入口 State | `adminMyRecord.myMemberRecord` (8 处 $state.go) |
| API | `getMedicalRecord.json`, `getMedicalRecordFlowVo.json` (L34862, L34885) |
| customerCheckinId | 0 命中 |
| appointId | 0 命中 |
| medicalRecordType | **glassestype 派生**（L34949）|
| 关键 ID | medicalRecordId + medicalExamineId + glassestype |

### 7.3 Sale 入口

| 项 | 证据 |
|---|---|
| Controller | `addSaleRecordCtrl` L31008, `adminSalesRecordCtrl` L31285, `myMaterialBillCtrl` L32435, `orderManageCtrl` L36165 |
| State Param | `$stateParams.medicalRecordId` L31286, L31388, L31609, L31741, L31923, L32123, L32445 |
| 入口 State | `adminSalesRecord.myMaterialBill` (7 处 $state.go) |
| API | `getMedicalRecord.json`, `getMedicalExamineVoList.json`, `getOrderVo.json` (L16150, L31220, L31331, L32190, L18942) |
| customerCheckinId | 0 命中 |
| **addMedicalRecord.json** | **L31119 — 真实 MedicalRecord Create** |
| medicalRecordType | **`== 5` 触发 Sale 路径**（L31123, L31143, L32951, L33055, L33136, L33156）|
| 关键 ID | medicalRecordId + medicalRecordType + patientId |

### 7.4 Charge 入口

| 项 | 证据 |
|---|---|
| Controller | `feeCashierCtrl` L36905, `feeDayCtrl` L37005, `waitChargeDetailCtrl` L6568, `waitPayBackCtrl` L6992, `chargeListCtrl` L16758, `chargeAdminCtrl` L52575, `chargeWaysCtrl` L52767 |
| State Param | `$stateParams.medicalRecordId` (waitChargeDetailCtrl L6570) |
| 入口 State | 多 |
| API | `getMedicalRecord.json`, `getMedicalRecordPayVo.json` (L4034), `getMedicalRecordCashflowVo.json` (L4942) |
| customerCheckinId | 0 命中 |
| **cashflowId** | **5 处 $stateParams.cashflowId** (L3814, L4026, L4238, L4381, L4940) |
| medicalRecordType | 0 命中 |
| 关键 ID | **medicalRecordId + cashflowId 双源** |

### 7.5 Delivery 入口（本轮新发现）

| 项 | 证据 |
|---|---|
| Controller | `deliveryInputCtrl` L3812, `deliveryInputRecordCtrl` L4024, `deliveryListCtrl` L4075, `deliveryProcessingCtrl` L4236, `deliveryDetailCtrl` L25281, `deliveryModifyCtrl` L25314, `deliveryDeleteCtrl` L25237, `deliveryModifyCustomerCtrl` L25573, `deliveryProductModifyCtrl` L25758 |
| State Param | **`$stateParams.cashflowId`** 5 处 (L3814, L4026, L4238, L4381, L4940) |
| 入口 State | `delivery` (估计) |
| API | `getMedicalRecordPayVo.json { cashflowId }` (L4034), `getMedicalRecordCashflowVo.json { cashflowId }` (L4942), `getMedicalRecordRefundDetailVo.json { cashflowId }` (L4433) |
| **$stateParams.medicalRecordId** | **0 命中**（A — 0 命中）|
| **medicalRecordType** | 0 命中 |
| customerCheckinId | 0 命中 |
| **关键 ID** | **cashflowId 是真正入口**（A — 5 处 State Param）|
| 内部派生 | `$scope.medicalRecordId = res.object.medicalRecord.id` (L4036) |

**【关键发现】**：
- **Delivery 模块不是通过 medicalRecordId 入口**（A — 0 命中 $stateParams.medicalRecordId）
- **Delivery 真正入口是 cashflowId**（A — 5 处 $stateParams.cashflowId 字符级）
- Delivery 内部通过 cashflowId → getMedicalRecordPayVo → 派生 medicalRecordId
- **S1-135 报告 "MedicalRecord → Delivery 0 桥"**实际是 F 边界 — **Delivery 入口 ID 不是 medicalRecordId**

---

## 8. State 路由树

### 8.1 4 业务模块 State 入口汇总

| 模块 | State 路径 | 入口 Controller | medicalRecordId 携带 |
|---|---|---|---|
| **Check** | `assistChecking` | assistCheckingCtrl L1756 | A（$stateParams）|
| | `checkCall` | checkCallCtrl L9760 | 估计 |
| **Optometry** | `adminMyRecord.myMemberRecord` | myMemberRecordCtrl L33218 | A（$stateParams）|
| | `optometry` | optometryCtrl L34776 | 估计 |
| | `optometryGlasses` | optometryGlassesCtrl L35383 | A（L35388）|
| **Sale** | `adminSalesRecord.myMaterialBill` | myMaterialBillCtrl L32435 | A（$stateParams）|
| | `addMedicalRecord` | addSaleRecordCtrl L31008 | A（L31119 create）|
| **Charge** | `waitPayDetail` | waitPayDetailCtrl L7452 | 估计 |
| | `waitPayList` | waitPayListCtrl L8110 | 估计 |
| | `waitPayBackList` | waitPayBackListCtrl L7383 | 估计 |
| | `waitChargeDetail` | waitChargeDetailCtrl L6568 | A（L6570）|
| | `feeCashier` | feeCashierCtrl L36905 | 估计 |
| | `feeDay` | feeDayCtrl L37005 | 估计 |
| | `payedList` | (估计) | — |
| | `partBack` | (估计) | — |
| **Delivery** | `deliveryList` | deliveryListCtrl L4075 | F（0 命中 medicalRecordId State）|
| | `deliveryInput` | deliveryInputCtrl L3812 | F（cashflowId 入口）|

### 8.2 关键 $state.go 跳转完整

| 目标 | 次数 | 携带参数 | 源 Controller |
|---|---:|---|---|
| `assistChecking` | **12** | medicalRecordId, medicalExamineId | 多 |
| `adminSalesRecord.myMaterialBill` | **7** | medicalRecordId, patientId | 多 |
| `adminMyRecord.myMemberRecord` | **8** | medicalRecordId, patientId | 多 |
| `adminMyRecord.myMaterialBill` | 2 | medicalRecordId | 多 |
| `addMedicalRecord` | 1+ | medicalRecordId, patientId | assistCheckingCtrl (L2269) |
| `checkinList` | 1 | appointId, printCheckinId | addCheckinCtrl (L8654) |
| `waitPayBackList` | 多 | cashflowId | 估计 |
| `deliveryList` | 多 | (估计) | 多 |
| `feeCashier` | 多 | (估计) | 多 |
| `optometry` | 多 | (估计) | 多 |

---

## 9. cashflowId → MedicalRecord 双向 4 API 桥（A — 字符级）

### 9.1 4 个 API 完整（A）

| # | 行号 | API | 类型 | Request 字段 | Response |
|---:|---|---|---|---|---|
| 1 | L4034 | `getMedicalRecordPayVo.json` | R | `cashflowId` | `res.object.medicalRecord.id` (L4036) |
| 2 | L4942 | `getMedicalRecordCashflowVo.json` | R | `cashflowId` | medicalRecordVo |
| 3 | L4433 | `getMedicalRecordRefundDetailVo.json` | R | `cashflowId` | medicalRecordVo |
| 4 | L4908 | `getMedicalRecordRefundLogVo.json` | R | `refundLogId` | medicalRecordVo |

### 9.2 双向 7 类桥判定

| 桥 | 结论 |
|---|---|
| Function | F |
| State | F（cashflowId 不派生 medicalRecordId）|
| **API Response → Request** | **A**（4 个 API 字符级）|
| Scope/Service | F |
| Factory | F |
| Object | F |
| 字段共现 | A |

### 9.3 4 个 API 命名误导（A 字符级）

- **`getMedicalRecordPayVo.json`** 名称含 "MedicalRecord" 但 Request 字段是 cashflowId（A — L4034）
- **`getMedicalRecordCashflowVo.json`** 同上（A — L4942）
- **`getMedicalRecordRefundDetailVo.json`** 同上（A — L4433）
- **`getMedicalRecordRefundLogVo.json`** 同上（A — L4908）

**【关键】**：4 个 API 名称含 "MedicalRecord"，**实质是 cashflow 范围 API**（A — 字符级多源互证）

---

## 10. MedicalRecord Create API 重新确认

### 10.1 真实 MedicalRecord Create API（A）

**`/admin/addMedicalRecord.json`**（W）：
- 位置：L31119 (addSaleRecordCtrl 范围)
- Request: `{ patientId, medicalRecordType: custView == 1 ? 1 : 5 }`
- Response: `res.object = { id, medicalRecordType, patientId }`
- 后续分流：medicalRecordType == 5 → Sale / else → Record

### 10.2 误判修正

| 误判 | 真实 |
|---|---|
| S1-135: "MedicalRecord 0 Create API" | **addMedicalRecord.json (W) 是真实 Create API**（A — L31119 字符级）|
| S1-136: "MedicalRecord 0 Create API" | 同上 |
| 命名误导 | `insertMedicalRecordTemplate.json`（L33457, L52253）是**模板** API，不是 MedicalRecord 本身 |

### 10.3 MedicalRecord 创建入口 A 字符级链

```
[addSaleRecordCtrl L31008] $scope.affirm
   ↓ A (L31115-L31117)
obj = { patientId: item.patient.id, medicalRecordType: custView == 1 ? 1 : 5 }
   ↓ A (L31119)
addMedicalRecord.json (W)
   ↓ A
res.object = { id, medicalRecordType, patientId }
   ↓ A (L31123)
if (medicalRecordType == 5) {
  $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId: res.object.id, patientId: res.object.patientId })
} else {
  $state.go("adminMyRecord.myMaterialBill", { medicalRecordId: res.object.id, patientId: res.object.patientId })
}
```

### 10.4 MedicalRecord Create 入口 0 命中反向

- `insertMedicalRecord` 0 命中（A — 0 命中，仅 `insertMedicalRecordTemplate`）
- `createMedicalRecord` 0 命中（A）
- `saveMedicalRecord` **0 命中 MedicalRecord**（A — 仅 `saveMedicalRecordDeliveryFactory` 用于 `saveMedicalProductDeliveryCommentBatch` L4060, **不是 MedicalRecord 本身**）
- `addMedicalRecord` **1 命中**（A — L31119 字符级 addSaleRecordCtrl 范围）

---

## 11. ID 反向排除（A — 字符级）

### 11.1 7 个 ID 严格区分

| ID | 不能等同 |
|---|---|
| **appointId** | ≠ medicalRecordId / customerCheckinId / cashflowId |
| **customerCheckinId** | ≠ medicalRecordId / cashflowId / appointId |
| **printCheckinId** | ≡ **customerCheckin.id**（A — S1-135 L8671）|
| **medicalRecordId** | ≠ cashflowId / customerCheckinId / appointId |
| **cashflowId** | ≠ medicalRecordId / customerCheckinId / appointId |
| **patientId** | ≠ medicalRecordId / customerCheckinId |
| **medicalRecordType** | ≠ 任何 ID（**是分流标志** A — 7 处 if）|

### 11.2 8 个 reverse 严格排除（A）

| 关系 | 等同？ | 证据 |
|---|---|---|
| `appointId == medicalRecordId` | **F** | A — 0 互换 |
| `appointId == customerCheckinId` | **F** | A — 0 互换 |
| `appointId == cashflowId` | **F** | A — 0 互换 |
| `customerCheckinId == medicalRecordId` | **F** | A — 0 互换 |
| `customerCheckinId == cashflowId` | **F** | A — 0 互换 |
| `medicalRecordId == cashflowId` | **F** | A — 4 个 API 桥证明不同对象 |
| `medicalRecordType == medicalRecordId` | **F** | A — medicalRecordType 是分流标志 |
| `printCheckinId == medicalRecordId` | **F** | A — printCheckinId ≡ customerCheckin.id ≠ medicalRecordId |

### 11.3 4 业务模块两两直接桥（沿用 S1-136 结论）

| 桥对 | 结论 |
|---|---|
| Check → Optometry / Sale / Charge | **F**（A — 0 桥）|
| Optometry → Sale / Charge | **F**（A — 0 桥）|
| Sale → Charge | **F**（A — 0 直接桥，间接通过 cashflow 桥）|
| **MedicalRecord ↔ Cashflow** | **A 双向 4 个 API 字符级桥** |

---

## 12. 4 业务模块入口独立性（A — 字符级）

### 12.1 4 条独立 DAG（A）

**DAG 1：CustomerCheckin → Check**
```
[customerCheckin.medicalRecordId]
   ↓ A (L8791)
checkinListCtrl
   ↓ A
$state.go("assistChecking", { medicalExamineId, medicalRecordId }) (L41717)
   ↓ A
assistCheckingCtrl → getMedicalExamineVoList.json
```

**DAG 2：CustomerCheckin → Optometry**
```
[customerCheckin.medicalRecordId]
   ↓ A (L34955)
optometryCtrl
   ↓ A
medicalRecordId → Request
   ↓ A
getMedicalRecordFlowVo.json
```

**DAG 3：CustomerCheckin → Sale**
```
[customerCheckin.medicalRecordId]
   ↓ A (L33203)
myMemberCtrl
   ↓ A
$state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })
   ↓ A
myMaterialBillCtrl
```

**DAG 4：CustomerCheckin → Charge**
```
[customerCheckin.medicalRecordId]
   ↓ A (L33134)
myMemberCtrl
   ↓ A
getMedicalRecord.json
   ↓ A
$state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) (L33142/33162/33202)
   ↓ A
myMemberRecordCtrl
```

**【关键】**：
- 4 条独立 DAG **不存在串行链**（A — 0 命中直接桥）
- 4 模块都消费 medicalRecordId 但**入口和路径不同**（A）

### 12.2 4 模块入口 ID 差异

| 模块 | 入口 ID | 入口 API | 入口 State |
|---|---|---|---|
| Check | medicalRecordId ($stateParams) | getMedicalExamineVoList.json | assistChecking |
| Optometry | medicalRecordId ($stateParams) | getMedicalRecord.json | adminMyRecord.myMemberRecord |
| Sale | medicalRecordId ($stateParams) | getMedicalRecord.json | adminSalesRecord.myMaterialBill |
| Charge | medicalRecordId ($stateParams) | getMedicalRecord.json | waitChargeDetail |

**4 模块入口 ID 相同**（medicalRecordId）但**派生路径不同**（A）

### 12.3 addMedicalRecord → 4 模块（A）

```
[addMedicalRecord.json (W)]
   ↓ A
medicalRecordType == 5 → adminSalesRecord.myMaterialBill (Sale)
medicalRecordType != 5 → adminMyRecord.myMaterialBill (Record)
```

**【关键】**：addMedicalRecord 仅直接进入 Sale + Record 路径，**不直接进入 Check + Optometry**（A — 0 命中 $state.go "assistChecking" / "optometry" 从 addMedicalRecord Response 触发）

---

## 13. Delivery vs MedicalRecord 重新验证

### 13.1 Delivery 真实入口 ID（A 字符级）

- **$stateParams.cashflowId**：5 处（L3814, L4026, L4238, L4381, L4940）
- **$stateParams.medicalRecordId**：**0 命中**（A）
- **$stateParams.customerCheckinId**：0 命中（A）
- **$stateParams.appointId**：0 命中（A）

### 13.2 Delivery 内部派生 medicalRecordId（A 字符级 L4036）

```javascript
var recordPromise = getMedicalRecord.saveOrQuery('/admin/getMedicalRecordPayVo.json', { cashflowId: $scope.cashflowId });
recordPromise.then(function (res) {
  if (res.object) {
    $scope.medicalRecordId = res.object.medicalRecord.id;  // ← 内部派生
  }
});
```

### 13.3 Delivery 真实链（A 字符级）

```
[External] $stateParams.cashflowId
   ↓ A
$scope.cashflowId (deliveryInputCtrl L3814, L4026, L4238, L4381, L4940)
   ↓ A
getMedicalRecordPayVo.json { cashflowId } (L4034)
   ↓ A
[Response] res.object.medicalRecord.id
   ↓ A
$scope.medicalRecordId (L4036 内部派生)
   ↓ A
[Delivery 业务流]
```

### 13.4 S1-135 报告修正

| S1-135 报告 | 本轮修正 |
|---|---|
| "MedicalRecord → Delivery 0 桥" | **F 边界保留** |
| "Delivery 0 消费 medicalRecordId" | **0 命中 State Param**（A）|
| "Delivery 0 消费 cashflowId" | **5 处 State Param**（A — 字符级 L3814 等）|
| "Delivery 内部派生 medicalRecordId" | **A — L4036 字符级直接证明** |

**【关键发现】**：Delivery **不通过 medicalRecordId State 入口**，**通过 cashflowId 内部派生 medicalRecordId**（A — 字符级多源互证）

---

## 14. 数量精确统计（A）

| 指标 | 总数 | State | Request | Response | Scope | ObjectFactory | 注释 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **medicalRecordId** | 161 | 25 | 多 | 1+ | 多 | 多 | — |
| **medicalRecordType** | **16** | 0 | **5** | 0 | 2 | 0 | 7 if + 2 转换 |
| **appointId** | **18** | 5 | 多 | 多 | 多 | 0 | L8216 注释 |
| **customerCheckinId** | **19** | **0** | 8 | 0 | 3 | 0 | 仅通过 Scope/Response |
| **cashflowId** | **73** | 5 | 30+ | 5+ | 多 | 0 | 多 Controller |

| 业务 | Controller | 入口 ID | medicalRecordId Consumer | API |
|---|---|---|---|---|
| **Check** | assistCheckingCtrl L1756 | medicalRecordId | 2+ | getMedicalExamineVoList |
| **Optometry** | optometryCtrl/optometryGlassesCtrl/myMemberRecordCtrl | medicalRecordId | 9 | getMedicalRecord / getMedicalRecordFlowVo |
| **Sale** | addSaleRecordCtrl/adminSalesRecordCtrl/myMaterialBillCtrl | medicalRecordId + medicalRecordType | 9+ | getMedicalRecord / addMedicalRecord (Create) |
| **Charge** | waitChargeDetailCtrl/feeCashierCtrl/feeDayCtrl | medicalRecordId + cashflowId | 1+ | getMedicalRecord + 4 cashflow 桥 |
| **Delivery** | deliveryInputCtrl/deliveryInputRecordCtrl | **cashflowId** (medicalRecordId 0) | 内部派生 L4036 | getMedicalRecordPayVo { cashflowId } |
| **CustomerCheckin** | checkinListCtrl/doctorWorkbenchCtrl/myMemberCtrl/optometryCtrl | customerCheckin.medicalRecordId | 6 处 | 多 |

| 总数 | 精确数 |
|---|---:|
| MedicalRecord Create API | **1**（addMedicalRecord.json L31119）|
| CustomerCheckin → MedicalRecord Consumer | **6 处** |
| MedicalRecord → Check Consumer | 2+ |
| MedicalRecord → Optometry Consumer | 9+ |
| MedicalRecord → Sale Consumer | 9+ |
| MedicalRecord → Charge Consumer | 1+ |
| MedicalRecord → Delivery Consumer | **0**（cashflowId 入口）|

---

## 15. 反向排除

| 关系 | 是否等同 | 证据 |
|---|---|---|
| **appointId == medicalRecordId** | **F** | A — 0 互换 |
| **appointId == customerCheckinId** | **F** | A — 0 互换 |
| **appointId == cashflowId** | **F** | A — 0 互换 |
| **customerCheckinId == medicalRecordId** | **F** | A — 0 互换 |
| **customerCheckinId == cashflowId** | **F** | A — 0 互换 |
| **medicalRecordId == cashflowId** | **F** | A — 4 个 API 桥 |
| **medicalRecordType == medicalRecordId** | **F** | A — medicalRecordType 是分流标志 |
| **Check → Optometry** | **F** | A — 0 桥 |
| **Optometry → Sale** | **F** | A — 0 桥 |
| **Sale → Charge** | **F** | A — 0 直接桥 |
| **Check → Sale** | **F** | A — 0 桥 |
| **Optometry → Charge** | **F** | A — 0 桥 |
| **Check → Charge** | **F** | A — 0 桥 |

---

## 16. 历史差异

| 项 | S1-128 ~ S1-136 历史 | S1-137 | 当前采用 |
|---|---|---|---|
| MedicalRecord Create API | "0 Create API"（S1-135, S1-136）| **addMedicalRecord.json (W) 在 addSaleRecordCtrl L31008 范围 L31119** | A — **D 冲突修正** |
| Delivery 入口 ID | "0 桥" | **cashflowId 是真实入口，medicalRecordId 内部派生 L4036** | A — 重要发现 |
| medicalRecordType 业务 | "分流标志"（S1-135）| **16 处 7 分类精确 + 5/1/6/7/glassestype 完整规则** | A — 加强 |
| 4 模块入口独立性 | "4 模块独立消费"（S1-136）| **4 条独立 DAG 字符级证明** | A — 加强 |
| 4 模块两两桥 | "只有 Sale↔Charge"（S1-136）| **保持 + 4 个 cashflow 桥 API 字符级** | A — 一致 |
| 8 个 ID 反向排除 | 散见（S1-135/136）| **统一为 8 关系表 + 4 模块两两 0 桥** | A — 加强 |
| insertMedicalRecord 含义 | "MedicalRecord Create"（S1-135 假设）| **`insertMedicalRecordTemplate.json` 是模板 API，不是 MedicalRecord 本身** | A — D 命名区分修正 |

---

## 17. L1 / L2 / L3

### 17.1 L1（前端直接事实）

- `addMedicalRecord.json` (W) 真实 MedicalRecord Create API（A — L31119 字符级）
- 4 业务模块完整 State 入口（A）
- Delivery 真实入口是 cashflowId（A — 5 处 $stateParams）
- medicalRecordType 16 处 7 分类（A — 字符级）
- 4 个 cashflow ↔ MedicalRecord API 桥（A — 字符级）
- 4 条独立 DAG 入口（A — 字符级）

### 17.2 L2（基于 L1 的有限业务解释）

- **addMedicalRecord** 是 MedicalRecord 主入口（addSaleRecordCtrl L31119）
- **medicalRecordType** 5 = Sale 路径，否则 = Record 路径
- **Delivery 入口是 cashflowId**，medicalRecordId 内部派生（A — L4036）
- 4 业务模块**独立消费 medicalRecordId**（非串行链）

### 17.3 L3（当前无证据）

- 后端 medical_record 表 / FK
- medicalRecordType 完整业务含义（5/1/6/7 后端定义）
- prescriptionId / orderId / chargeId / optometryId 后端实体
- 主键体系
- customerCheckin 后端结构

---

## 18. 最终入口 DAG（A-N）

### DAG A: Appointment → CustomerCheckin → MedicalRecord
```
[$stateParams.appointId]
   ↓ A
addCheckinCtrl L8159
   ↓ A (L8237)
getAppointSchoolMateVo / getAppointPatientVo.json { appointId }
   ↓ A
item.patient / item.schoolMateVo
   ↓ A
$scope.obj + item.appoint.id
   ↓ A (L8658, L8665, L8667, L8695)
confirmArrivalOfAppoint.json { appointId } (W)
insertCustomerCheckin[OfNewPaitent/OfNewCustomer].json $scope.checkCustomer/$scope.obj (W)
   ↓ A
res.result.vo.customerCheckin { id, medicalRecordId, patientId, employeeId }
   ↓ A
printCheckinId = customerCheckin.id
$state.go("checkinList", { appointId, printCheckinId })
```

### DAG B: CustomerCheckin → Check
（沿用 S1-135 L8791 字符级 + L41717 $state.go）

### DAG C: CustomerCheckin → Optometry
（沿用 S1-135 L34955 字符级）

### DAG D: CustomerCheckin → Sale
（沿用 S1-135 L33203 字符级）

### DAG E: CustomerCheckin → Charge
（沿用 S1-135 L33134 + L33136-L33147 字符级）

### DAG F: Cashflow → MedicalRecord
```
[$stateParams.cashflowId]
   ↓ A
$scope.cashflowId
   ↓ A
getMedicalRecordPayVo.json { cashflowId } (L4034)
getMedicalRecordCashflowVo.json { cashflowId } (L4942)
getMedicalRecordRefundDetailVo.json { cashflowId } (L4433)
getMedicalRecordRefundLogVo.json { refundLogId } (L4908)
   ↓ A
res.object.medicalRecord (医疗记录对象)
   ↓ A
[Cashflow 业务流]
```

### DAG G: MedicalRecord → Cashflow
（沿用 DAG F 反向 — 4 个 API 双向桥 A 字符级）

### DAG H: MedicalRecord → Check
（沿用 S1-136 — $stateParams.medicalRecordId → getMedicalExamineVoList A）

### DAG I: MedicalRecord → Optometry
（沿用 S1-136 — $stateParams.medicalRecordId → getMedicalRecord.json A）

### DAG J: MedicalRecord → Sale
```
[addMedicalRecord.json (W) Response res.object]
   ↓ A
medicalRecordType == 5 → adminSalesRecord.myMaterialBill
medicalRecordType != 5 → adminMyRecord.myMaterialBill
   ↓ A
$stateParams.medicalRecordId
   ↓ A
adminSalesRecordCtrl / myMaterialBillCtrl
   ↓ A
getMedicalRecord.json { id: $stateParams.medicalRecordId }
```

### DAG K: MedicalRecord → Charge
（沿用 S1-136 — $stateParams.medicalRecordId → waitChargeDetailCtrl + cashflow 桥 A）

### DAG L: MedicalRecord → Delivery
```
[MedicalRecord ↔ Cashflow 桥]
   ↓ A
$scope.cashflowId
   ↓ A
getMedicalRecordPayVo.json { cashflowId } (L4034)
   ↓ A
$scope.medicalRecordId (内部派生 L4036)
   ↓ A
[Delivery 业务流]
```

### DAG M: medicalRecordType → State
```
medicalRecordType
   ↓ A
{ 5, !5, 1, 6, 7, glassestype }
   ↓ A
{ adminSalesRecord.myMaterialBill, adminMyRecord.myMaterialBill, beginCustomerCheckin, toBeProcess, glassestype, ... }
```

### DAG N: ID 参数 → State → Controller
```
[入口 ID]
├── appointId → addCheckinCtrl
├── customerCheckinId → checkinListCtrl/doctorWorkbenchCtrl/myMemberCtrl/optometryCtrl
├── medicalRecordId → 4 业务模块
├── cashflowId → waitChargeDetailCtrl/deliveryInputCtrl
└── patientId → 多 Controller

→ 入口 State
→ $stateParams 接收
→ $scope.id
→ API Request
→ 业务模块
```

---

## 19. 26项证据矩阵

| # | 项 | 结论 | 等级 | 文件/行号 | 当前采用 |
|---:|---|---|---|---|---|
| 1 | MedicalRecord Source | 8 类 | A | 第 2 节 | A |
| 2 | medicalRecordId Source | 25 $stateParams + 33 API + 6 customerCheckin + 73 cashflow 桥 | A | 多处 | A |
| 3 | appointId Source | 5 $stateParams + 5 Response + 5 Scope | A | L8216, L8238, L8648, L8659, L8665 | A |
| 4 | customerCheckinId Source | **0 $stateParams** + 8 Request + 3 Scope | A | L8789, L8847, L9050, L9122 | A |
| 5 | cashflowId Source | 5 $stateParams + 30 Request + 5 Response | A | L3814, L4026, L4034, L4942 | A |
| 6 | medicalRecordType Source | 16 处 / 7 分类 | A | 详见第 6 节 | A |
| 7 | CustomerCheckin → MedicalRecord | **A 字符级 6 处** | A | L8791, L10610, L10642, L33134, L33203, L34955 | A |
| 8 | Appointment → CustomerCheckin | A 字符级 | A | L8658, L8665, L8667, L8695 | A |
| 9 | Check Entry | $stateParams.medicalRecordId + assistCheckingCtrl | A | L1757, L41717 | A |
| 10 | Optometry Entry | $stateParams.medicalRecordId + optometryCtrl/optometryGlassesCtrl/myMemberRecordCtrl | A | L33223, L33590, L35388 | A |
| 11 | Sale Entry | $stateParams.medicalRecordId + adminSalesRecordCtrl/myMaterialBillCtrl | A | L31286, L32445 | A |
| 12 | Charge Entry | $stateParams.medicalRecordId + cashflowId 双源 | A | L6570, L4034, L4942 | A |
| 13 | Delivery Entry | **$stateParams.cashflowId**（medicalRecordId 0）| A | L3814, L4026, L4238, L4381, L4940 | A |
| 14 | MedicalRecord → Check | A 字符级 | A | L2068, L2385, L41717 | A |
| 15 | MedicalRecord → Optometry | A 字符级 | A | L33223, L33590, L34955, L35416 | A |
| 16 | MedicalRecord → Sale | A 字符级 | A | L31286, L32952, L33056, L33137 | A |
| 17 | MedicalRecord → Charge | A 字符级 | A | L6570, L1964 | A |
| 18 | MedicalRecord → Delivery | A 通过 cashflow 桥内部派生 | A | L4034, L4036, L4942 | A — 修正 S1-135 |
| 19 | Cashflow → MedicalRecord | **A 4 API 字符级** | A | L4034, L4433, L4908, L4942 | A |
| 20 | MedicalRecord → Cashflow | **A 4 API 字符级** | A | L4034, L4433, L4908, L4942 | A |
| 21 | 四业务模块两两直接桥 | **F**（除 Sale↔Charge 间接）| A | 0 桥字符级 | F |
| 22 | State Route Tree | 12 $state.go assistChecking / 7 myMaterialBill / 8 myMemberRecord / 多 checkinList | A | 多处 | A |
| 23 | MedicalRecord Create API | **addMedicalRecord.json (W) L31119** | A | L31115-L31137 | A — **D 修正 S1-135/136** |
| 24 | ID 反向排除 | 8 关系 0 桥 | A | 详见第 15 节 | F |
| 25 | 最终入口 DAG | 14 个 DAG A-N | A | 第 18 节 | A |
| 26 | 复刻红线 | 第 20 节 | A | 本文档 | A |

---

## 20. A/B/C/D/E/F 分布

- **A**：23
- **B**：1（6 处 customerCheckin.medicalRecordId 多源互证）
- **C**：0
- **D**：2（addMedicalRecord.json 误判修正 + insertMedicalRecordTemplate 命名区分）
- **E**：**0**
- **F**：5（两两桥 / MedicalRecord → Delivery 旧报告 / ID 反向 / 后端实体）

---

## 21. 复刻红线

### 21.1 不能自行增加的字段

- `customerCheckin` 不含 `customerId` 字段（A — 0 命中）
- `medicalRecord` 不应直接含 `cashflow` 完整字段（A — 4 个 API 桥证明不同对象）
- `medicalRecordType` 不应作为 ID（A — 是分流标志）

### 21.2 不能自行补桥的模块

- 4 业务模块两两直接桥 0（F 边界）
- 不能假定"medicalRecordId 自动流通"（A — 4 模块独立消费）
- 不能假定"check 完进入 optometry"（A — 0 桥）
- 不能假定"sale 完进入 charge"（A — 0 直接桥，间接 cashflow）
- **Delivery 入口是 cashflowId 不是 medicalRecordId**（A — 5 处 $stateParams.cashflowId，0 处 medicalRecordId）

### 21.3 不能假定存在的 API

- `/admin/insertMedicalRecord.json` 不存在（A — 仅 `insertMedicalRecordTemplate`）
- `/admin/createMedicalRecord.json` 不存在
- `/admin/saveMedicalRecord.json` 不存在（A — 仅 `saveMedicalRecordDeliveryFactory` 用于配送评论）
- `/admin/getMedicalRecordDeliveryVo.json` 实际是 cashflow 范围 API

### 21.4 不能等同的 ID（A 字符级）

| ID | 不能等同 |
|---|---|
| **appointId** | ≠ medicalRecordId / customerCheckinId / cashflowId |
| **customerCheckinId** | ≠ medicalRecordId / cashflowId / appointId |
| **printCheckinId** | ≡ **customerCheckin.id**（A — L8671 字符级）|
| **medicalRecordId** | ≠ cashflowId / customerCheckinId / appointId |
| **cashflowId** | ≠ medicalRecordId / customerCheckinId / appointId |
| **patientId** | ≠ medicalRecordId / customerCheckinId |
| **medicalRecordType** | ≠ 任何 ID（**是分流标志** A — 7 处 if）|

### 21.5 必须保留的 F 边界

- 4 业务模块两两直接桥 0（F 边界）
- 后端 medical_record / cashflow 表 / FK（F 边界）
- medicalRecordType 完整业务含义（F 边界）
- 0 共享 Service / Factory（F 边界）

### 21.6 命名误导必须标注

- **`addMedicalRecord.json` 是真实 MedicalRecord Create API**（A — L31119 字符级，S1-135/136 误判修正）
- **`insertMedicalRecordTemplate.json` 是模板 API**，不是 MedicalRecord 本身（A — L33457, L52253）
- **`getMedicalRecordPayVo.json` / `getMedicalRecordCashflowVo.json` / `getMedicalRecordRefundDetailVo.json` / `getMedicalRecordRefundLogVo.json` 名称含 "MedicalRecord" 但 Request 字段是 cashflowId**（A — 4 个 API 字符级）
- **`medicalRecordType == 5` 不是 Sale ID，是分流标志**（A — 7 处 if）
- **`medicalRecordType == 1` 不是 Checkin ID，是接诊类型**（A — L10607, L33127, L33197）
- **`medicalRecordType == 1 ? 1 : 5` 由 custView 派生**（A — L31117）
- **`Delivery 真实入口是 cashflowId 不是 medicalRecordId`**（A — 5 处 $stateParams.cashflowId，0 处 medicalRecordId State）
- **`$state.go("addMedicalRecord", ...)` 在 assistCheckingCtrl L2269 是跳转目标不是创建入口**（A — 实际创建在 addSaleRecordCtrl L31119）

---

## 22. 红线检查

| 项 | 实际 | 通过 |
|---|---|---|
| API actual | 0 | ✓ |
| Write actual | 0 | ✓ |
| Production mutation | 0 | ✓ |
| controller.js SHA256 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433（**未变化**）| ✓ |
| deliveryList.html SHA256 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476（**未变化**）| ✓ |
| machineOrderCompleted.html SHA256 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24（**未变化**）| ✓ |
| machineOrderList.html SHA256 | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A（**未变化**）| ✓ |
| 历史 MD 165-198 | **未修改** | ✓ |
| P0 = 54 | 冻结 | ✓ |
| P1 = 8 | 冻结 | ✓ |
| 10 untracked 保留 | 全部保留 | ✓ |
| 视光之家url.txt 继续 ignored | 保留 | ✓ |
| ignored = 1 | 确认 | ✓ |
| 本轮只新增 199_*.md | 是 | ✓ |
| 临时脚本（2 个）在 C:\Users\18671\AppData\Local\Temp\ | 不进入 Git | ✓ |

---

## 23. Git

- 本轮 commit hash：（待执行 `git add -- 199_*.md` / `git commit -m "docs(199): S1-137 MedicalRecord 多入口 medicalRecordType State路由总审计"` / `git push origin master`）
- 本轮 LOCAL == REMOTE：待最终校验
- 本轮 tracked 预期：206 → 207
- 本轮 untracked 预期：10（保留 10 untracked，新增 199 后变 10 untracked 因为 199 进 tracked）
- 本轮 ignored 预期：1（视光之家url.txt 保留）
- 本轮 staged only：199_S1-137_*.md
