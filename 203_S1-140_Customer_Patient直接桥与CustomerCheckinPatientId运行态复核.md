# S1-140：Customer ↔ Patient 直接桥与 CustomerCheckin.patientId 运行态复核

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据复核（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 202 个 MD / 不修改历史
> 关联：S1-138 / S1-139

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. 关键 S1-139 误判点
5. 阶段一：getPatientVoList({customerId}) 来源追踪
6. 阶段二：Customer → Patient 七种桥复核
7. 阶段三：Patient → Customer 再确认
8. 阶段四：同 Response customer + patient 审计
9. 阶段五：CustomerCheckin.patientId 运行态复核
10. 阶段六：CustomerCheckin 与 Patient 的真实桥
11. 阶段七：insertCustomerCheckin* Request 精确复核
12. 阶段八：addMedicalRecord Request 复核
13. 阶段九：Mobile 不能偷换为身份桥
14. 阶段十：Patient → MedicalRecord 保留
15. 阶段十一：最终 ID 三角
16. 阶段十二：直接 vs 参数桥
17. 阶段十三：最终结论矩阵
18. 阶段十四：精确数量
19. 阶段十五：历史一致性
20. 阶段十六：L1 / L2 / L3
21. 阶段十七：26 项证据矩阵
22. 阶段十八：最终 DAG
23. 阶段十九：反向排除
24. 复刻红线
25. 红线检查
26. Git

---

## 1. 任务性质

本轮是证据复核 / 关键关系严谨化任务。

- 禁止修改 165-202 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`203_S1-140_*.md`
- 核心：必须区分 "API 接受 customerId 参数" vs "Customer 对象 → Patient 对象" 直接桥
- 核心：必须区分 "注释代码 patientId" vs "运行时 patientId"

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实业务 API |
| 5 | 不创建 Customer / Patient / MedicalRecord |
| 6 | 不接诊 / 不收费 / 不销售 / 不验光 / 不检查 |
| 7 | 不修改 controller.js（SHA256 不变）|
| 8 | 不修改任何 HTML |
| 9 | 不修改 .gitignore |
| 10 | 不修改 165-202 历史 MD |
| 11 | 只新增 203_*.md |
| 12 | 不因为 API 参数名推断对象来源 |
| 13 | 不因为字段名 customerId 自动认定 Customer → Patient |
| 14 | 不因为注释代码存在就认定运行时存在 |
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

### 命名约束（重要）

| 误区 | 正确理解 |
|---|---|
| "API 接受 customerId" | ≠ "Customer → Patient 直接桥" |
| "注释代码 patientId" | ≠ "运行时 patientId" |
| "L18981 getPatientVoList by customerId" | ≠ "Customer 对象 → Patient 对象桥"（实际 customerId 来自 $stateParams）|
| "patient 对象含 customerId 字段" | ≠ "Customer → Patient 直接桥"（实际是 Patient → Customer 方向）|
| "patientInfo 包含 customerId" | 是 Patient → Customer 方向的证据，不是 Customer → Patient |

**唯一确认 Customer → Patient 直接桥的字符级证据模式**:
- 字符 A: `customer.id`（从 Customer Response） → `getPatientVoList({customerId: ...})`
- 必须有 `customer.id`（来自 getCustomerVo Response）作为输入
- 不能只是 `$stateParams.customerId` 或 `$scope.customerId`（来自函数参数）

---

## 4. 关键 S1-139 误判点

S1-139 报告中有 **2 项关键误判**需要严格修正：

### 误判 1：Customer → Patient = A

**S1-139 表述**:
> "Customer → Patient（A 双向）— L18981 getPatientVoList.json by customerId"

**实际字符级证据**:
```javascript
// L18946-L18990 patientListCtrl
$scope.customerId = $stateParams.customerId;                    // L18949 — customerId 来自 URL/State
$scope.search = function (index, loadPagin) {
  HttpFactory.list('/admin/getPatientVoList.json', {
    customerId: $scope.customerId,                              // L18982 — 来自 $stateParams
    index: index,
    length: 9
  }).then(function (res) {
    $scope.patientList = res.list;                              // L18986
  });
};
```

**关键问题**: 
- L18949 `$scope.customerId = $stateParams.customerId` — customerId 来自 **URL/State 入口**
- L18982 `customerId: $scope.customerId` — 仍来自 URL
- **没有任何字符级证据** 证明 customerId 来自 Customer 对象 Response（`res.customer.id`）
- L8364 / L8390 也是用 `name + mobile` 搜索，**不是** customerId

**修正**: Customer → Patient **不是对象桥**，是 **参数桥 (C)**：
- 参数桥 (C): customerId 从 URL State 传递到 getPatientVoList 查询
- 对象桥 (A): Customer 对象 Response → Patient 对象 — **F**（无字符级证据）

### 误判 2：customerCheckin.patientId ≡ patientId（明确等同）

**S1-139 §18 表述**:
> "明确等同: customerCheckin.patientId ≡ patientId（A 字符级 L8707）"

**实际字符级证据**:
```javascript
// L8667-L8720 addCheckinCtrl.create()
new ObjectFactory().saveOrQuery("/admin/insertCustomerCheckinOfNewPaitent.json", $scope.checkCustomer)
  .then(function (res) {
    if (res.status == 0) {
      Popup.notice("新增成功");
      var printCheckinId = res.result.vo.customerCheckin.id;            // L8697
      /* if (
        !$scope.obj.patientId &&
        $scope.appointVo &&
        $scope.appointVo.type === 1
      ) {
        new ObjectFactory()
          .saveOrQuery("/admin/addSchoolMateConsume.json", {
            schoolMateCheckId: $scope.appointVo.schoolMateCheckId,
            patientId: res.result.vo.customerCheckin.patientId,          // L8707 ← 在注释内
          })
          .then(() => {
            dealNeedPrint(printCheckinId);
          });
      } else {
        dealNeedPrint(printCheckinId);
      } */
      dealNeedPrint(printCheckinId);                                       // L8715
    } else {
      Popup.notice(res.errmsg);
    }
    $scope.obj.birthday = t;
  });
```

**关键问题**:
- L8707 在 `/* ... */` **注释代码块** 内（L8699-L8714）
- 实际执行代码是 L8715 `dealNeedPrint(printCheckinId);`
- **L8707 customerCheckin.patientId 在运行时不执行**

**修正**:
- customerCheckin.patientId 在**当前源码范围未观察到实际消费/赋值**
- 必须从"明确等同"降级为 **F**
- S1-139 §11 已经标注了 L8707 是"仅注释代码"，但 §18 误把它写成"明确等同"

---

## 5. 阶段一：getPatientVoList({customerId}) 来源追踪

### 5.1 4 个 getPatientVoList 调用点全量

`Select-String 'getPatientVoList\.json' controller.js` — 4 处:

| # | 行号 | Controller | Request | customerId Source | 等级 |
|---|---|---|---|---|---|
| 1 | L8364 | (addCheckinCtrl 范围 L8350+) | `{ name, mobile }` | **无 customerId** | C（name+mobile 搜索）|
| 2 | L8374 | (同上，注释代码)| `{ name, mobile }` | 无 customerId（**注释**）| F |
| 3 | L8390 | (同上)| `{ name, mobile }` | **无 customerId** | C（name+mobile 搜索）|
| 4 | L18981 | patientListCtrl | `{ customerId, index, length }` | `$scope.customerId = $stateParams.customerId`（L18949）| **C（参数桥）**|

### 5.2 L18981 customerId 完整字符级证据

```javascript
// L18946-L18990 patientListCtrl
angular.module('bestvisionWeb').controller('patientListCtrl', ['$scope', '$stateParams', '$timeout', '$state', 'ObjectFactory', 'Popup', 'HttpFactory', function ($scope, $stateParams, $timeout, $state, ObjectFactory, Popup, HttpFactory) {
    $scope.historyModal = false;
    $scope.patientId = null;
    $scope.customerId = $stateParams.customerId;                    // L18949 — 来自 URL
    ...
    $scope.search = function (index, loadPagin) {
        HttpFactory.list('/admin/getPatientVoList.json', {
            customerId: $scope.customerId,                          // L18982 — 仍来自 URL
            index: index,
            length: 9
        }).then(function (res) {
            $scope.patientList = res.list;                          // L18986
        });
    };
};
```

### 5.3 customerId Source 分类

| 行号 | 表达式 | 来源分类 | 等级 |
|---|---|---|---|
| L18949 | `$scope.customerId = $stateParams.customerId` | URL/State 入口 | A |
| L5273 | `$scope.customerId = customerId` | 函数参数 | A |
| L19676 | `$scope.customerId = customerId` | 函数参数 | A |
| L16746/L16759 | `$scope.customerId = $stateParams.customerId` | URL/State 入口 | A |
| L18060/L18145/L20940 | `$scope.customerId = $stateParams.customerId` | URL/State 入口 | A |
| L31228 | `$scope.customerId = res.result.object.customerId` | **Patient Response** | A |
| L18982 | `customerId: $scope.customerId` | (消费) | A |

**重要发现**: 整个 controller.js 中**没有任何** `customerId = res.customer.id` 或 `customerId = customer.id` 的赋值。

### 5.4 是否有"customer 对象 → customerId"路径

| 模式 | 命中 | 等级 |
|---|:---:|---|
| `customer.id → customerId` | 0 | F |
| `res.customer.id → customerId` | 0 | F |
| `customer.id → getPatientVoList` | 0 | F |

**正式冻结**: 当前源码范围未观察到 Customer 对象 Response → customerId 派生路径。

---

## 6. 阶段二：Customer → Patient 七种桥复核

### 6.1 七种桥逐一判定

| 桥类型 | 等级 | 字符级证据 | 备注 |
|---|:---:|---|---|
| A. Function | **C** | L8364 / L8390 `searchPatientkeyword` / `searchPatientMobile` 用 name+mobile 触发 | 不是 customer 对象桥 |
| B. State | **A** | L18949 `$stateParams.customerId` → L18982 getPatientVoList | 参数桥，不是对象桥 |
| C. API Response→Request | **C** | L18982 `customerId: $scope.customerId` 但 $scope.customerId 来自 URL | 参数桥 |
| D. Scope/Service | **C** | `$scope.customerId` 来自 URL/Patient Response | 不是 customer 对象 |
| E. Factory | F | — | — |
| F. Object | F | — | 无对象引用 |
| G. Field co-occurrence | C | customerId + patientId 同 Response 出现在 choosePatient (L8424) | 但 choosePatient 是 **Patient → Customer 方向**的证据 |

### 6.2 Customer → Patient 最终判定

| 命题 | 结论 | 等级 |
|---|---|---|
| Customer → Patient **对象桥**（Customer Response → Patient）| **F** | F（无字符级证据）|
| Customer → Patient **参数桥**（URL customerId → getPatientVoList 查询）| **A** | A（L18949 + L18982）|
| Customer → Patient **name/mobile 搜索桥** | **A** | A（L8364/L8390）|
| "Customer → Patient" 整体直接 A 桥 | **C** | C（参数桥和搜索桥，不是对象桥）|

**S1-139 §5.1 / §8 误判修正**:
- S1-139 报告"Customer → Patient = A 双向"
- 实际: **Customer → Patient 不是双向 A**
- 严格表述: **C (参数桥 + 搜索桥)**，**F (对象桥)**

---

## 7. 阶段三：Patient → Customer 再确认

### 7.1 6 个字符级证据（已确认）

`Select-String 'res\.result\.object\.customerId' controller.js` — 6 处:

| # | 行号 | 上下文 | 完整链 |
|---|---|---|---|
| 1 | L11915 | `CommonRequest.getCustomer(res.customerId, ...)` | patient → customer (A) |
| 2 | L31228 | `$scope.customerId = res.result.object.customerId` | getPatientInfo Response → customerId |
| 3 | L31234 | `getCustomerVo.json { customerId: res.result.object.customerId }` | patient.customerId → getCustomerVo (A) |
| 4 | L31338 | `$scope.customerId = res.result.object.customerId` | 同 L31228 |
| 5 | L31345 | `getCustomerVo.json { customerId: res.result.object.customerId }` | 同 L31234 |
| 6 | L32464 | `$scope.fee.customerId = res.result.object.customerId` | 同 L31228 |
| 7 | L32912 | `getCustomerVo.json { customerId: res.result.object.customerId }` | 同 L31234 |

### 7.2 L11915 CommonRequest.getCustomer 模式

```javascript
// L11910-L11917 Controller
CommonRequest.getPatient($scope.patientId, function (res) {       // L11910 — getPatient
    $scope.patientInfo = res;                                    // L11911
    if (res.patientBirthday) {
        $scope.date.birthday = res.patientBirthday;               // L11913
    }
    CommonRequest.getCustomer(res.customerId, function (res2) {  // L11915 — getCustomer by patient.customerId
        $scope.customerInfo = res2;
    });
});
```

| 项目 | 字符级证据 |
|---|---|
| Patient Response 有 `res.customerId` 字段 | L11915 |
| 立即调 getCustomer(patient.customerId) | L11915 |
| 链式: Patient → Customer | A |

### 7.3 Patient → Customer 完整链

```
Patient (Patient Object)
  ↓ A — res.customerId (getPatient Response)
  ↓ A — res.result.object.customerId (getPatientInfo Response)
  ↓ A — patient.customerId (L8424 choosePatient 参数)
  ↓ A — patient.customerName (L8424 choosePatient 参数)
Customer (Customer Object)
```

**Patient → Customer = A 直接桥成立**（多源互证 + 字符级）

### 7.4 Patient → Customer 最终判定

| 命题 | 结论 | 等级 |
|---|---|---|
| Patient 实体有 `customerId` 字段 | **YES** | A（7 处）|
| `patient.customerId → getCustomerVo` 直接桥 | **A** | A（L31234/L31345/L32912/L3650）|
| `CommonRequest.getPatient → getCustomer` 链 | **A** | A（L11915）|
| Patient → Customer 直接 A 桥 | **A** | A |

**S1-139 §9.4 结论保留**: Patient → Customer = A **确认无误**

---

## 8. 阶段四：同 Response customer + patient 审计

### 8.1 全文搜索同 Response

`Select-String 'res\.customer\.|res\.patient\.' controller.js`:

| 模式 | 命中 | 行号 |
|---|:---:|---|
| `res\.customer\.id` | 1 | L8895 |
| `res\.customer\.name` 等 | 多 | L8887-L8905 范围 |
| `res\.patient\.id` | 1 | L33204 |

### 8.2 L8894-L8906 完整上下文

```javascript
// L8880-L8907 (某 Controller)
HttpFactory.object("/admin/getPatientVo.json", { patientId: patientId }).then(function (res) {
  ...
  HttpFactory.object("/admin/getCustomerVo.json", {
    customerId: res.customer.id                                  // L8895
  }).then(function (response) {
    $scope.oldCustomerIdArr = response.tagList.map(function (v) {
      return v.id;
    });
    $scope.memberArrayStatus.show = true;
    $scope.customer.id = response.customer.id;                  // L8901
    $scope.customer.channel = response.customer.channel;
    $scope.customer.channelTagId = response.customer.channelTagId;
    $scope.customer.trueName = response.customer.customerName;
    $scope.customer.linkMobile = response.customer.linkMobile;
  });
});
```

**关键**: 
- **getPatientVo Response 包含 customer 对象**（L8895 `res.customer.id`）
- 这意味着 **Patient 实体包含 customer 引用**（A 级）
- 但这是 **Patient → Customer 方向** 的证据，不是 Customer → Patient 方向

### 8.3 L33204 完整上下文

```javascript
// L33193-L33208 receiveSelfAndBeginCustomerCheckin
$scope.receiveSelfAndBeginCustomerCheckin = function (customerCheckinId) {
  Popup.confirm("为该用户创建电子病历？", function () {
    HttpFactory.object(
      '/admin/receiveSelfAndBeginCustomerCheckin.json',
      {
        customerCheckinId: customerCheckinId,
        medicalRecordType: 1
      }
    ).then(function (res) {
      if (res.status) {
        return Popup.notice(res.errmsg);
      }
      $state.go("adminMyRecord.myMemberRecord", {
        medicalRecordId: res.customerCheckin.medicalRecordId,      // L33203
        patientId: res.patient.id                                  // L33204 — 同 Response 含 patient
      });
    });
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| receiveSelfAndBegin Response | 含 `res.customerCheckin.medicalRecordId` + `res.patient.id` |
| `res.patient.id` → `$state.go` State 参数 | L33204 |
| **是 patient 对象的 ID，不是 Patient 实体** | 注意：res.patient.id 是 patient 引用，patient 对象本身**不包含 customer 字段**（已 S1-139 确认）|

### 8.4 同 Response customer + patient 分类

| Response | customer | patient | 类型 |
|---|:---:|:---:|---|
| getPatientVo (L8895) | A (res.customer.id) | A (res.id/patientName 等) | Patient 含 customer 引用（**Patient → Customer 方向**）|
| receiveSelfAndBegin (L33204) | F | A (res.patient.id) | customerCheckin 含 patient 引用（**CustomerCheckin → Patient 方向**）|

**结论**: 
- 同一 Response 含 customer + patient 存在（getPatientVo L8895），但**这是 Patient → Customer 方向**
- **没有**字符级证据证明 customer 对象 + patient 对象在同一 Response 中是兄弟对象（**Customer ↔ Patient 直接对象桥 F**）

---

## 9. 阶段五：CustomerCheckin.patientId 运行态复核

### 9.1 全部 customerCheckin.patientId 命中

`Select-String 'customerCheckin\.patientId' controller.js` — **1 处**:

| 行号 | 上下文 | 分类 |
|---|---|---|
| L8707 | addCheckinCtrl.create() 注释代码块内 | **注释**（L8699-L8714 `/* */`）|

### 9.2 L8707 严格分类

```javascript
// L8667-L8720 addCheckinCtrl.create()
new ObjectFactory().saveOrQuery("/admin/insertCustomerCheckinOfNewPaitent.json", $scope.checkCustomer)
  .then(function (res) {
    if (res.status == 0) {
      Popup.notice("新增成功");
      var printCheckinId = res.result.vo.customerCheckin.id;          // L8697 (执行)
      /* if (                                                            // L8699 — 注释开始
        !$scope.obj.patientId &&
        $scope.appointVo &&
        $scope.appointVo.type === 1
      ) {
        new ObjectFactory()
          .saveOrQuery("/admin/addSchoolMateConsume.json", {
            schoolMateCheckId: $scope.appointVo.schoolMateCheckId,
            patientId: res.result.vo.customerCheckin.patientId,        // L8707 ← 注释内
          })
          .then(() => {
            dealNeedPrint(printCheckinId);
          });
      } else {
        dealNeedPrint(printCheckinId);
      } */                                                              // L8714 — 注释结束
      dealNeedPrint(printCheckinId);                                     // L8715 (执行)
    } else {
      Popup.notice(res.errmsg);
    }
    $scope.obj.birthday = t;
  });
```

| 项目 | 字符级证据 |
|---|---|
| L8707 所在行 | 在 `/* ... */` 注释块内（L8699-L8714）|
| 实际执行代码 | L8715 `dealNeedPrint(printCheckinId);` |
| 实际消费字段 | `customerCheckin.id`（L8697 → printCheckinId）|
| **运行时不消费 patientId** | A |

### 9.3 CustomerCheckin 字段实际运行时消费

`Select-String 'customerCheckin\.(id|patientId|medicalRecordId|customerId)' controller.js`:

| 字段 | 运行时消费处 | 等级 |
|---|---|---|
| `customerCheckin.id` | 6+ 处 (L8671/L8697/L8789/L18929 etc.) | A |
| `customerCheckin.medicalRecordId` | 6 处 (L8791/L10610/L10642/L33134/L33203/L34955) | A |
| `customerCheckin.patientId` | **0 处运行时代码** | F |
| `customerCheckin.customerId` | 0 处 | F |

### 9.4 CustomerCheckin.patientId 最终结论

| 命题 | 结论 | 等级 |
|---|---|---|
| `customerCheckin.patientId` 字段在运行时被消费 | **NO** | F |
| `customerCheckin.patientId` 字段在注释代码中 | YES (L8707) | A |
| `customerCheckin.patientId` 字段在 addSchoolMateConsume.json Request 中出现 | F（仅注释） | F |
| `customerCheckin.patientId ≡ patientId`（明确等同）| **NO**（必须从 S1-139 §18 删除） | F |

**S1-139 §18 误判修正**:
- S1-139 §18 把"customerCheckin.patientId ≡ patientId"列为"明确等同 A"
- 实际: **L8707 在注释代码块内**，运行时不执行
- 必须从"明确等同"降级为 **F（当前源码范围未观察到运行时消费）**

### 9.5 CustomerCheckin.patientId 是否真的"存在"于实体？

| 命题 | 等级 | 说明 |
|---|---|---|
| 实体存在 customerCheckin.patientId 字段 | **F**（无运行时代码证明）| 仅有注释代码间接证明 |
| 实体有 customerCheckin.id 字段 | A（6+ 处实际消费）| 字符级确认 |
| 实体有 customerCheckin.medicalRecordId 字段 | A（6 处实际消费）| 字符级确认 |
| 实体有 customerCheckin.customerId 字段 | F（0 处）| 0 命中 |
| 实体有 customerCheckin.patient 对象 | F（0 处）| 0 命中 |

**严格表述**:
- `customerCheckin.patientId` 在**当前源码范围未观察到实际消费**
- `customerCheckin.medicalRecordId` 在运行时**有 A 级消费**
- `customerCheckin.id` 在运行时**有 A 级消费**
- `customerCheckin.customerId` 在**当前源码范围未观察到任何引用**

---

## 10. 阶段六：CustomerCheckin 与 Patient 的真实桥

### 10.1 CustomerCheckin → Patient 复核

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| `customerCheckin.patientId` 字段 | **F** | 仅 L8707 注释代码 |
| `customerCheckin.id → patientId` 转换 | F | 0 命中 |
| `customerCheckin → getPatientVo` | F | 0 命中 |
| **CustomerCheckin → Patient 整体** | **F** | 无运行字符级证据 |

**S1-139 §11 误判修正**:
- S1-139 §11 把 CustomerCheckin → Patient 列为 C
- 实际: **F（运行时无任何证据）**

### 10.2 Patient → CustomerCheckin 复核

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| `patient.customerCheckinId` 字段 | F | 0 命中 |
| `patient → getCustomerCheckinVo` | F | 0 命中 |
| **Patient → CustomerCheckin 整体** | **F** | 无字符级证据 |

**保持 F**（S1-139 同样结论）

### 10.3 CustomerCheckin → MedicalRecord 保持 A

| 桥 | 等级 | 字符级证据 |
|---|:---:|---|
| `customerCheckin.medicalRecordId` 字段 | A | 6 处 (L8791/L10610/L10642/L33134/L33203/L34955) |
| CustomerCheckin → MedicalRecord | A | — |

**保持 A**（S1-135/S1-137R/S1-139 已确认）

### 10.4 MedicalRecord → CustomerCheckin 保持 F

| 桥 | 等级 |
|---|:---:|
| `medicalRecord.customerCheckinId` 字段 | F（0 命中）|
| MedicalRecord → CustomerCheckin | F |

### 10.5 CustomerCheckin 4 方向总结

| 方向 | 等级 |
|---|:---:|
| CustomerCheckin → Patient | **F**（S1-139 §11 误判修正）|
| Patient → CustomerCheckin | F |
| CustomerCheckin → Customer | F |
| Customer → CustomerCheckin | F |
| CustomerCheckin → MedicalRecord | A |
| MedicalRecord → CustomerCheckin | F |

**CustomerCheckin 在 3 对象关系中只与 MedicalRecord 有 A 桥**。

---

## 11. 阶段七：insertCustomerCheckin* Request 精确复核

### 11.1 4 个调用点 Request 字段

| API | 行号 | Controller | Request | 实际字段 | 注释/执行 |
|---|---|---|---|---|---|
| insertCustomerCheckinOfNewPaitent.json | L8667 | addCheckinCtrl | `$scope.checkCustomer` | appointId, registrationFeeId, customerName, linkMobile, employeeId, gender, idCard | **执行** |
| insertCustomerCheckinOfNewCustomer.json | L8679 | addCheckinCtrl | `$scope.obj` | patientId, name, birthday, registrationFeeId | **执行**（条件分支）|
| insertCustomerCheckin.json | L8681 | addCheckinCtrl | `$scope.obj` | patientId, name, birthday, registrationFeeId | **执行**（条件分支）|
| insertCustomerCheckin.json | L34914 | optometryCtrl | `{ name, gender, patientId, employeeId }` | **A 字符级 patientId: obj.patient.id (L34912)** | **执行** |

### 11.2 patientId / customerId 实际发送

| API | patientId 发送 | customerId 发送 |
|---|:---:|:---:|
| insertCustomerCheckinOfNewPaitent.json | F | F |
| insertCustomerCheckinOfNewCustomer.json | C（推断 $scope.obj.patientId）| F |
| insertCustomerCheckin.json (addCheckinCtrl) | C（推断 $scope.obj.patientId）| F |
| insertCustomerCheckin.json (optometryCtrl) | **A**（L34912 字符级）| F |

**重要发现**: optometryCtrl 范围内的 insertCustomerCheckin.json **确实**发送 patientId（A），addCheckinCtrl 范围**不发送** patientId。

### 11.3 customerId 在 insertCustomerCheckin* 中

| 模式 | 命中 | 等级 |
|---|:---:|---|
| `insertCustomerCheckin*` Request 中 customerId | 0 | F |
| insertCustomerCheckin* Response customerCheckin.customerId | 0 | F |

**正式冻结**: insertCustomerCheckin* **不发送 customerId**，**不消费 customerCheckin.customerId**。

---

## 12. 阶段八：addMedicalRecord Request 复核

### 12.1 addMedicalRecord.json 完整链

```javascript
// L31111-L31137 addSaleRecordCtrl
$scope.choseUser = {
    ...
    affirm: function affirm(item, custView) {                       // L31111
        if (!item.patient.id) {
            return Popup.notice("请选择用户");
        }
        var obj = {
            patientId: item.patient.id,                             // L31116 — patientId 来自 item.patient.id
            medicalRecordType: custView == 1 ? 1 : 5                // L31117
        };
        new ObjectFactory().saveOrQuery(
            "/admin/addMedicalRecord.json",                         // L31119
            obj
        ).then(function (res) {
            if (res.status == 0) {
                Popup.notice("新增成功");
                if (res.object.medicalRecordType == 5) {            // L31123
                    $state.go("adminSalesRecord.myMaterialBill", {  // L31124
                        medicalRecordId: res.object.id,             // L31125
                        patientId: res.object.patientId             // L31126
                    });
                } else {
                    $state.go("adminMyRecord.myMaterialBill", {    // L31129
                        medicalRecordId: res.object.id,             // L31130
                        patientId: res.object.patientId             // L31131
                    });
                }
            }
        });
    }
};
```

### 12.2 patientId / customerId 在 addMedicalRecord.json

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `patientId` (Request) | L31116 `item.patient.id` | A |
| `medicalRecordType` (Request) | L31117 `custView == 1 ? 1 : 5` | A |
| `customerId` (Request) | **0 命中** | F |
| `patientId` (Response → State) | L31126 / L31131 | A |

### 12.3 Customer → addMedicalRecord 独立判定

| 命题 | 结论 | 等级 |
|---|---|---|
| addMedicalRecord.json Request 包含 customerId | **NO** | F |
| addMedicalRecord.json Request 包含 patientId | YES | A |
| patientId 来源 (item.patient.id) | 来自**用户选中的 patient 对象** | A |
| Customer 对象直接进入 addMedicalRecord | **NO** | F |
| Customer → addMedicalRecord 桥 | **F**（无 customerId 字段）| F |

**S1-138 §15 / S1-139 §15 结论保留**: addMedicalRecord.json 仅使用 patientId，不使用 customerId。

---

## 13. 阶段九：Mobile 不能偷换为身份桥

### 13.1 Mobile 字段全量

| 字段 | 命中 | 字符级 |
|---|:---:|---|
| `customerMobile` | 多 | A |
| `linkMobile` | 多 | A |
| `mobile` | 多 | A |
| `customer\.mobile` | F | 0 命中（用 linkMobile 代替）|
| `customer\.linkMobile` | A | L8905 / L20967 |

### 13.2 Mobile 查询桥

| API | Request 字段 | 行号 | 等级 |
|---|---|---|---|
| getPatientVoList.json | `{ name, mobile }` | L8364 / L8390 | A |
| getCustomerVo.json | `{ customerId }` (不用 mobile) | L5924 | — |
| getPatientVoList.json (by customerId) | `{ customerId }` | L18981 | A（参数桥）|

### 13.3 Mobile 桥严格表述

| 命题 | 等级 | 说明 |
|---|:---:|---|
| `customerMobile → Patient query` | A | 字符级 mobile 字段作为查询参数 |
| `mobile 相同 = Customer/Patient 身份相同` | F | 字段值相同不等于实体身份相同 |
| `Customer.mobile → Patient.mobile 1:1` | F | 无后端证据 |
| `linkMobile = customerMobile` | C | 都是 mobile 字段但不一定等同 |
| `Mobile → Patient` 搜索桥 | C | 仅作为查询条件 |

**严格表述**:
- mobile 字段可作为 Patient 查询条件（C 局部）
- mobile 字段值相同**不能**自动证明 Customer/Patient 身份合并
- 复刻后端不应把 mobile 作为身份合并主键

---

## 14. 阶段十：Patient → MedicalRecord 保留

### 14.1 Patient → MedicalRecord 直接桥

```javascript
// L32927
$scope.getMedicalRecordListFactory = new ListFactory(
  '/admin/getMedicalRecordList.json',
  0, pageSize,
  { patientId: $scope.patientId }                              // L32927
);
```

| 项目 | 字符级证据 |
|---|---|
| API | getMedicalRecordList.json |
| Request | `{ patientId }` |
| Response | medicalRecordList |
| 等级 | **A** |

### 14.2 MedicalRecord → Patient 直接桥

```javascript
// L6693
$scope.getPatientObjectFactory.saveOrQuery(
  "/admin/getPatientInfo.json",
  { id: res.object.medicalRecord.patientId }                    // L6693
);
```

| 项目 | 字符级证据 |
|---|---|
| API | getPatientInfo.json |
| Request | `{ id: medicalRecord.patientId }` |
| 等级 | **A** |

### 14.3 Patient ↔ MedicalRecord 最终判定

| 方向 | 等级 | 字符级证据 |
|---|:---:|---|
| **Patient → MedicalRecord** | **A** | L32927 getMedicalRecordList.json by patientId |
| **MedicalRecord → Patient** | **A** | L6693 medicalRecord.patientId → getPatientInfo |

**双向 A 桥成立，无变化**（S1-139 同样结论）

---

## 15. 阶段十一：最终 ID 三角

### 15.1 4 个 ID 严格区分

| ID | 来源分类 | 字符级证据 |
|---|---|---|
| `customerId` | Customer 主键 | L8895 res.customer.id / L18949 $stateParams.customerId |
| `patientId` | Patient 主键 | L31222 medicalRecord.patientId / L3641 $stateParams.patientId |
| `medicalRecordId` | MedicalRecord 主键 | L31119 addMedicalRecord → res.object.id / L31220 getMedicalRecord |
| `cashflowId` | Cashflow 主键 | L3814 $stateParams.cashflowId / L4034 getMedicalRecordPayVo |
| `customerCheckinId` | CustomerCheckin 主键 | L8671 res.result.vo.customerCheckin.id / L8789 medicalCheckBeforeCustomerCheckin |

### 15.2 ID 不同（A 级 100% 字符级证据）

| ID A | ≠ ID B | 字符级证据 |
|---|---|---|
| customerId | patientId | L16745-L16746 同时存在 (说明不同) |
| customerId | medicalRecordId | MedicalRecord 不含 customerId 字段 |
| patientId | medicalRecordId | L31116 (patientId 单独) vs L31125 (medicalRecord.id) |
| customerId | customerCheckinId | Customer 不含 customerCheckinId 字段 |
| patientId | customerCheckinId | patientId L16745 vs customerCheckinId L8789 |
| customerCheckinId | medicalRecordId | customerCheckin 6 处携带 medicalRecordId |
| customerCheckinId | cashflowId | 2 个独立 State 入口 |
| medicalRecordType | medicalRecordId | 16 处 medicalRecordType 是枚举值 |
| patientId | cashflowId | 不同 State 入口 |

### 15.3 ID 三角

```
customerId
    ↓ ??
patientId
    ↓ A (双向)
medicalRecordId

customerCheckinId
    ↓ A
medicalRecordId
```

- patientId ↔ medicalRecordId: **双向 A**
- customerCheckinId → medicalRecordId: **A**
- customerId ↔ patientId: **不是双向 A**（仅 Patient → Customer 是 A）

---

## 16. 阶段十二：直接 vs 参数桥

### 16.1 直接 vs 参数桥分类

| 证据 | 是否等于对象桥 | 等级 |
|---|---|---|
| `getPatientVoList({customerId})` | **NO**（customerId 来自 URL，不是 Customer 对象）| C（参数桥）|
| `patient.customerId → getCustomerVo` | **YES** | A（Patient → Customer 对象桥）|
| `patientId → getMedicalRecordList` | **YES** | A（Patient → MedicalRecord 对象桥）|
| `medicalRecord.patientId → getPatientInfo` | **YES** | A（MedicalRecord → Patient 对象桥）|
| `customerCheckin.patientId` (L8707 注释) | **NO**（注释代码）| F |
| `customerCheckin.medicalRecordId` | **YES** | A（CustomerCheckin → MedicalRecord 对象桥）|
| `customerId: $scope.customerId` (L18982) | **NO**（参数传递）| C |
| `customerId: res.result.object.customerId` (L31228) | **YES**（Patient → Customer 方向）| A |
| `CommonRequest.getCustomer(res.customerId)` (L11915) | **YES** | A |

### 16.2 S1-139 vs S1-140 严格区分

| 关系 | S1-139 报告 | S1-140 复核 | 当前采用 |
|---|---|---|---|
| Customer → Patient | A（双向）| C（参数桥，不是对象桥）| **C** |
| Patient → Customer | A（双向）| A（对象桥，6+ 处）| **A** |
| CustomerCheckin → Patient | C | F（仅注释）| **F** |
| CustomerCheckin → MedicalRecord | A | A | A |
| CustomerCheckin.customerId | F | F | F |

---

## 17. 阶段十三：最终结论矩阵

### 17.1 最终结论矩阵

| 关系 | S1-139 | S1-140 | 当前采用 | 等级 |
|---|---|---|---|---|
| **Customer → Patient** | A | C（参数桥） | **C** | C |
| **Patient → Customer** | A | A | **A** | A |
| **CustomerCheckin → Patient** | C | F（仅 L8707 注释） | **F** | F |
| **Patient → CustomerCheckin** | F | F | **F** | F |
| **Customer → MedicalRecord** | F / A 间接 | F / A 间接 | **F** / **A 间接** | F / A |
| **MedicalRecord → Customer** | F / A 间接 | F / A 间接 | **F** / **A 间接** | F / A |
| **Patient → MedicalRecord** | A | A | **A** | A |
| **MedicalRecord → Patient** | A | A | **A** | A |
| **Mobile → Patient** | C | C（搜索桥） | **C** | C |
| **Mobile → Customer** | A | A | **A** | A |

### 17.2 关键修正摘要

| S1-139 误判 | S1-140 修正 |
|---|---|
| Customer → Patient = A（双向）| **Customer → Patient = C（参数桥）** |
| customerCheckin.patientId ≡ patientId（明确等同 A）| **customerCheckin.patientId = F（仅注释代码）** |
| CustomerCheckin → Patient = C | **CustomerCheckin → Patient = F** |

---

## 18. 阶段十四：精确数量

### 18.1 getPatientVoList 调用统计

| 统计项 | 数量 |
|---|:---:|
| getPatientVoList.json 调用总次数 | 4 |
| 其中用 customerId 参数 | 1 (L18981) |
| 其中用 name+mobile 参数 | 2 (L8364/L8390) |
| 注释代码 | 1 (L8374) |
| **customerId 来自 Customer 对象的次数** | **0** |
| **customerId 来自 $stateParams 的次数** | 1 (L18949 → L18982) |

### 18.2 customerCheckin 字段统计

| 统计项 | 数量 |
|---|:---:|
| customerCheckin.id 运行时代码 | 6+ |
| customerCheckin.medicalRecordId 运行时代码 | 6 |
| customerCheckin.patientId **执行代码** | **0** |
| customerCheckin.patientId 注释代码 | 1 (L8707) |
| customerCheckin.customerId | 0 |

### 18.3 patient.customerId 统计

| 统计项 | 数量 |
|---|:---:|
| `patient.customerId` 直接字段名 | 0 |
| `res.result.object.customerId` (getPatientInfo) | 6 (L31228/L31234/L31338/L31345/L32464/L32912) |
| `res.customerId` (CommonRequest.getPatient) | 1 (L11915) |
| `patient.customerId` 作为函数参数 | 1 (L8424 choosePatient) |
| **patient 实体 customerId 字段总计** | **8 处 A 级字符级证据** |

### 18.4 customerId 赋值路径统计

| 路径 | 命中 | 等级 |
|---|:---:|---|
| `customerId = res.customer.id` (Customer Response) | 0 | F |
| `customerId = $stateParams.customerId` (URL) | 多 (L18949/L16746/L16759/L18060/L18145/L20940) | A |
| `customerId = res.result.object.customerId` (Patient Response) | 1 (L31228) | A |
| `customerId = customerId` (函数参数) | 2 (L5273/L19676) | A |

---

## 19. 阶段十五：历史一致性

### 19.1 S1-139 误判确认

| S1-139 表述 | S1-140 证据 | 修正 |
|---|---|---|
| §5.1 "Customer → Patient = A 双向" | L18949 `$scope.customerId = $stateParams.customerId` | 降级 C |
| §11 "CustomerCheckin → Patient = C" | L8707 在 `/* */` 注释块内 | 降级 F |
| §18 "customerCheckin.patientId ≡ patientId 明确等同 A" | L8707 在注释块内 | 删除等同表述，降级 F |
| §9.4 "Patient → Customer = A" | 6+ 处 A 级字符级证据 | **保持 A** |
| §10 "Patient → MedicalRecord = A" | L32927 字符级 | **保持 A** |
| §11 "MedicalRecord → Patient = A" | L6693 字符级 | **保持 A** |

### 19.2 S1-138 / S1-137R 关联验证

| 历史文档 | 关键结论 | S1-140 影响 |
|---|---|---|
| S1-138 §15 "Sale 不是唯一 Create 入口" | 字符级 | 无影响 |
| S1-138 §12 "5 条 Create 路径" | 字符级 | 无影响 |
| S1-137R §5 "MedicalRecord → Cashflow = F" | 字符级 | 无影响 |

### 19.3 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 202_S1-139 全部保持原样
- 本文档 203_*.md 单独记录 S1-139 2 项误判修正
- 后续 S1-141+ 应直接采用 S1-140 精确结论

---

## 20. 阶段十六：L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | 字段 / API / Request / Response / State / Controller / 注释 字符级 | A |
| L2 | "Customer → Patient 是参数桥不是对象桥" / "L8707 在注释块内" 等派生解释 | A |
| L3 | 数据库表 / 事务边界 / FK / 唯一索引 | **F**（无后端证据）|

---

## 21. 阶段十七：26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | customerId Source | 4 类: $stateParams / 函数参数 / Patient Response / (无 Customer Response) | A | 多处 | L18949/L5273/L31228 | A |
| 2 | customerId Consumer | 30+ 处 getCustomerVo / getCustomerMember / getCustomerPoint 等 | A | 多处 | 全部 | A |
| 3 | patientId Source | $stateParams / 函数参数 / 链式派生 | A | 多处 | L3641/L11829/L16745 | A |
| 4 | patientId Consumer | getMedicalRecordList / getPatientInfo 等 | A | 多处 | 全部 | A |
| 5 | medicalRecordId Source | $stateParams / addMedicalRecord Response / getMedicalRecord | A | 多处 | L31119/L31220 | A |
| 6 | medicalRecordId Consumer | $stateParams / getMedicalRecord | A | 多处 | 30+ | A |
| 7 | Customer → Patient 参数桥 | L18982 customerId from $stateParams | A | patientListCtrl | L18982 | A (参数) |
| 8 | Customer → Patient 对象桥 | **F**（无 Customer.id → patientId 路径）| F | — | — | F |
| 9 | Patient → Customer | res.result.object.customerId → getCustomerVo | A | 多处 | L31228/L31234/L32912 | A |
| 10 | Patient → MedicalRecord | getMedicalRecordList by patientId | A | myMedicalRecordList | L32927 | A |
| 11 | MedicalRecord → Patient | medicalRecord.patientId → getPatientInfo | A | myMaterialBill | L6693 | A |
| 12 | Customer → MedicalRecord | F 直接 / A 间接经 Patient | F/A | — | — | F / A 间接 |
| 13 | MedicalRecord → Customer | F 直接 / A 间接经 Patient | F/A | — | — | F / A 间接 |
| 14 | customerCheckin.patientId | **F**（仅 L8707 注释） | F | addCheckinCtrl | L8707 (注释) | F |
| 15 | customerCheckin.customerId | F (0 命中) | F | — | — | F |
| 16 | customerCheckin.medicalRecordId | A (6 处) | A | 多处 | L8791/L10610/L10642/L33134/L33203/L34955 | A |
| 17 | insertCustomerCheckin Request | optometryCtrl 范围有 patientId, addCheckinCtrl 范围无 | A/C | 2 Controller | L34914/L8667 | A/C |
| 18 | addMedicalRecord Request | patientId YES / customerId NO | A/F | addSaleRecordCtrl | L31115-L31117 | A/F |
| 19 | mobile 查询桥 | getPatientVoList by mobile | A | 多处 | L8364/L8390 | A |
| 20 | 同 Response customer/patient | getPatientVo Response 含 customer.id (Patient→Customer 方向) | A | — | L8895 | A |
| 21 | Factory 桥 | 无跨 Controller 共享 | F | — | — | F |
| 22 | Scope 桥 | $scope.customerId 来自 URL, 不是 Customer 对象 | A/C | — | L18949 | A/C |
| 23 | State 桥 | 4 ID 都有独立 State 入口 | A | 多处 | 全部 | A |
| 24 | 四 ID 区分 | customerId ≠ patientId ≠ medicalRecordId ≠ customerCheckinId | A | — | — | A |
| 25 | 最终直接/间接图 | 详见 §22 | A | — | — | A |
| 26 | 复刻风险 | 见 §24 | — | — | — | 见 §24 |

---

## 22. 阶段十八：最终 DAG

### DAG A: Customer → Patient
- **C**（参数桥: L18982 from $stateParams）
- **F**（对象桥: 无 Customer.id → patient 路径）

### DAG B: Patient → Customer
- **A**（res.result.object.customerId → getCustomerVo, 6+ 处）
- **A**（CommonRequest.getPatient → getCustomer, L11915）

### DAG C: Patient → MedicalRecord
- **A**（L32927 getMedicalRecordList by patientId）

### DAG D: MedicalRecord → Patient
- **A**（L6693 / L31222 medicalRecord.patientId → getPatientInfo）

### DAG E: Customer → MedicalRecord
- **F**（直接）
- **A**（间接经 Patient 2 层）

### DAG F: MedicalRecord → Customer
- **F**（直接）
- **A**（间接经 Patient 2 层）

### DAG G: CustomerCheckin → Patient
- **F**（L8707 在注释块内，运行时无证据）

### DAG H: CustomerCheckin → MedicalRecord
- **A**（6 处字符级桥）

### DAG I: Mobile → Patient
- **C**（搜索桥）

### DAG J: patient.customerId → Customer
- **A**（Patient 实体有 customerId 字段，7 处字符级证据）

---

## 23. 阶段十九：反向排除

### 23.1 ID 严格不同

| ID A | ≠ ID B | 等级 |
|---|---|---|
| customerId | ≠ patientId | A |
| customerId | ≠ medicalRecordId | A |
| patientId | ≠ medicalRecordId | A |
| customerCheckinId | ≠ medicalRecordId | A |
| customerId | ≠ customerCheckinId | A |
| patientId | ≠ customerCheckinId | A |
| customerCheckinId | ≠ cashflowId | A |
| medicalRecordType | ≠ medicalRecordId | A |

### 23.2 字段不存在反向排除

| 不存在字段 | 等级 | 说明 |
|---|:---:|---|
| `customerCheckin.patientId` 在运行时 | F | 仅 L8707 注释代码 |
| `customerCheckin.customerId` | F | 0 命中 |
| `medicalRecord.customerId` | F | 0 命中 |
| `medicalRecord.customer` | F | 0 命中 |
| `medicalRecord.customerCheckinId` | F | 0 命中 |
| `customer.patientId` | F | 0 命中 |
| `customer.patient` | F | 0 命中 |

### 23.3 不能桥

| 命题 | 等级 | 原因 |
|---|:---:|---|
| `customer.id → patientId` 自动赋值 | F | 无字符级证据 |
| `mobile 相等 = 身份相同` | F | 字段值相同不等于实体身份 |
| `L18981 customerId = Customer.id` | F | 实际来自 $stateParams |
| `L8707 patientId = 运行时 patientId` | F | 实际在注释块内 |

---

## 24. 复刻红线

### 24.1 字段冻结（必实现 vs 必不返回）

| 实体 | 必有字段 | 必不返回字段 |
|---|---|---|
| Customer | id, customerName, linkMobile, channel, channelTagId | **patientId, patient, customerCheckinId** |
| Patient | id, patientName, patientBirthday, patientGender, **customerId**, school, schoolClass, customerName | **medicalRecord, customerCheckin** |
| MedicalRecord | id, medicalRecordType, patientId, templateId | **customerId, customer, customerCheckinId, patient** |
| CustomerCheckin | id, **medicalRecordId** | **customerId, customer, patient**（**注意：customerCheckin.patientId 在当前源码无运行时证据，但实体结构可能存在**）|

### 24.2 桥必实现

| 桥 | 必实现 | 等级 |
|---|---|---|
| Patient → Customer | getCustomerVo { customerId } (customerId 来自 patient.customerId) | A |
| Patient → MedicalRecord | getMedicalRecordList { patientId } | A |
| MedicalRecord → Patient | getPatientInfo { id: medicalRecord.patientId } | A |
| CustomerCheckin → MedicalRecord | Response: customerCheckin.medicalRecordId | A |

### 24.3 不可桥（必须显式不返回）

| 不可桥 | 等级 | 说明 |
|---|:---:|---|
| Customer → Patient 对象桥 | F | 仅 URL 参数桥可用 |
| CustomerCheckin → Patient | F | 当前源码无运行时证据 |
| MedicalRecord → Customer 直接 | F | 必须经 Patient.customerId 中转 |
| customerCheckin.customerId 字段 | F | 0 命中，必须不返回 |

### 24.4 命名误导必标注

| 命名 | 实际 | 复刻警告 |
|---|---|---|
| `customerId` State 参数 | 来自 URL | 不一定来自 Customer 对象 |
| `customerCheckin.patientId` | 注释代码 | 实体可能存在但当前运行时不消费 |

### 24.5 S1-139 误判清单（不复刻）

1. **不复刻 "Customer → Patient = A 双向"**（仅 C 参数桥）
2. **不复刻 "customerCheckin.patientId ≡ patientId 明确等同"**（仅 F 注释代码）

---

## 25. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-202 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ 视光之家url.txt 未修改 |
| 本轮只新增 203_*.md | ✓ |

---

## 26. Git

### 26.1 操作

```
git add -- 203_S1-140_Customer_Patient直接桥与CustomerCheckinPatientId运行态复核.md
git diff --cached --name-only
git commit -m "docs(203): S1-140 Customer Patient直接桥与CustomerCheckinPatientId运行态复核"
git push origin master
```

### 26.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| REMOTE origin/master | (new commit) |
| LOCAL == REMOTE | YES |
| tracked | 211（commit 203 后从 210 → 211） |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| staged only current document | ✓ 203_*.md |
| 文件修改数 | 1 file changed, ~1200-1500 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L18949 | **$scope.customerId = $stateParams.customerId**（customerId 来自 URL，不是 Customer 对象）|
| L18982 | getPatientVoList.json { customerId: $scope.customerId }（**Customer → Patient 实际是参数桥**）|
| L8707 | customerCheckin.patientId 字段（**在 `/* */` 注释块内 L8699-L8714**）|
| L8715 | 实际执行代码 `dealNeedPrint(printCheckinId);` |
| L31228 | `$scope.customerId = res.result.object.customerId`（Patient → Customer 方向）|
| L31234 | `getCustomerVo.json { customerId: res.result.object.customerId }` |
| L11915 | `CommonRequest.getCustomer(res.customerId, ...)`（Patient → Customer 方向）|
| L32927 | `getMedicalRecordList.json { patientId }`（Patient → MedicalRecord）|
| L6693 | `getPatientInfo.json { id: res.object.medicalRecord.patientId }`（MedicalRecord → Patient）|
| L8895 | `getPatientVo Response.customer.id`（Patient 含 customer 引用）|
| L33204 | `res.patient.id`（receiveSelfAndBegin Response）|

---

S1-140 完成。立即停止，等待老板下一指令。不执行 S1-141。
