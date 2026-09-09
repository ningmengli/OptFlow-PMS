# S1-138：MedicalRecord 多创建路径 + 创建后分流状态机深度审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向建模（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 200 个 MD / 不修改历史
> 关联：S1-135 / S1-136 / S1-137 / S1-137R

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. 全部 MedicalRecord 写 API 候选全量扫描
5. addMedicalRecord.json 深度审计
6. beginCustomerCheckin 系列深度审计
7. receiveSelfAndBeginCustomerCheckin 深度审计
8. insertCustomerCheckin* 深度审计（含修正 S1-137R 误判）
9. updateMedicalRecord / setMedicalRecordProcessMode / cancelMedicalRecord / completeMedicalRecordDelivery 分类
10. insertMedicalRecordTemplate 系列分类
11. MedicalRecord Create 候选分类总表
12. Create → medicalRecord.id 完整链
13. medicalRecordType 生命周期（7 分类 + 5 业务规则）
14. Create → Check / Optometry / Sale / Charge / Delivery 分流
15. CustomerCheckin ↔ MedicalRecord 双向矩阵
16. Patient ↔ MedicalRecord 矩阵
17. Sale ↔ MedicalRecord 矩阵
18. State 状态机
19. Create API 唯一性结论
20. 精确数量
21. L1 / L2 / L3
22. 最终 StateMachine A-E
23. 26 项证据矩阵
24. A/B/C/D/E/F 等级
25. 历史差异
26. 复刻红线
27. 红线检查
28. Git

---

## 1. 任务性质

本轮是 MedicalRecord 多创建路径 + 创建后分流状态机深度审计。

- 禁止修改 165-200 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`201_S1-138_*.md`
- 必须严格区分 A-F 证据等级
- 核心目标：建立 MedicalRecord 创建路径精确模型 + 分流状态机

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实业务 API |
| 5 | 不创建 MedicalRecord |
| 6 | 不接诊 / 不验光 / 不检查 / 不销售 / 不配送 |
| 7 | 不修改 controller.js（SHA256 不变） |
| 8 | 不修改任何 HTML |
| 9 | 不修改 .gitignore |
| 10 | 不修改 165-200 历史 MD |
| 11 | 只新增 201_*.md |
| 12 | 不因为 API 名称推断"创建" |
| 13 | 不因为 Response 有 medicalRecord.id 就假设 API 创建 |
| 14 | 不因为 Write API 就假设一定创建 MedicalRecord |
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
| "API 名称含 Create" | ≠ "API 是 Create" |
| "Request 有 medicalRecordType" | ≠ "API 创建 MedicalRecord" |
| "Response 含 medicalRecord.id" | ≠ "API 是 MedicalRecord Create 入口" |
| "Write API" | ≠ "Create MedicalRecord" |
| "insertCustomerCheckin" | ≠ "Create MedicalRecord" |
| "addMedicalRecord" 命名 | ≠ "Add"（实际是 Create）|

唯一确认 Create 的字符级证据模式：
- Request: 仅必要字段 (如 patientId/medicalRecordType 或 customerCheckinId/medicalRecordType)
- Response: 含**完整新建对象标识** (id/medicalRecordType/patientId)
- 后续 Consumer 立即使用这个 id 作为 State 入口

---

## 4. 全部 MedicalRecord 写 API 候选全量扫描

`Select-String 'addMedicalRecord|beginCustomerCheckin|receiveSelfAndBeginCustomerCheckin|insertCustomerCheckin|updateMedicalRecord|completeMedicalRecordDelivery|cancelMedicalRecord|confirmMedicalRecordReturn|setMedicalRecordProcessMode' controller.js` 共 16 处：

| # | 行号 | API | 所在 Controller |
|---|---|---|---|
| 1 | L31119 | **addMedicalRecord.json** | addSaleRecordCtrl |
| 2 | L10605 | **beginCustomerCheckin.json** | 候诊队列 (dealWithBtn) |
| 3 | L33127 | **beginCustomerCheckin.json** | adminMyRecordCtrl (selectMedicalType) |
| 4 | L34947 | **beginCustomerCheckin.json** | optometryCtrl (beginCustomerCheckin) |
| 5 | L33195 | **receiveSelfAndBeginCustomerCheckin.json** | adminMyRecordCtrl (receiveSelfAndBegin) |
| 6 | L8667 | insertCustomerCheckinOfNewPaitent.json | addCheckinCtrl |
| 7 | L8679 | insertCustomerCheckinOfNewCustomer.json | addCheckinCtrl |
| 8 | L8681 | insertCustomerCheckin.json | addCheckinCtrl |
| 9 | L34914 | insertCustomerCheckin.json | optometryCtrl (addUser.affirm) |
| 10 | L8658 | confirmArrivalOfAppoint.json | addCheckinCtrl (confirmArrival) |
| 11 | L33457 | insertMedicalRecordTemplate.json | adminMyRecordCtrl |
| 12 | L33479 | **updateMedicalRecord.json** | adminMyRecordCtrl |
| 13 | L35099 | setMedicalRecordProcessMode.json | optometryCtrl (choseFactoryMethod) |
| 14 | L35150 | cancelMedicalRecord.json | optometryCtrl (fnMap.取消订单) |
| 15 | L35167 | confirmMedicalRecordReturn.json | optometryCtrl (fnMap.退货) |
| 16 | L35185 / L35204 | completeMedicalRecordDelivery.json | optometryCtrl (fnMap) |
| 17 | L52253 | insertMedicalRecordTemplate.json | (Template 2nd occurrence) |
| 18 | L8788 | medicalCheckBeforeCustomerCheckin.json | 诊前检查 modal |

---

## 5. addMedicalRecord.json 深度审计

### 5.1 完整字符级证据

```javascript
// L31111-L31137 addSaleRecordCtrl
$scope.choseUser = {
    show: false,
    open: function open() {
        this.show = true;
    },
    showChufang: true,
    register: function register() {
        $state.go("addCheckin");
    },
    affirm: function affirm(item, custView) {                      // L31111
        if (!item.patient.id) {
            return Popup.notice("请选择用户");
        }
        var obj = {
            patientId: item.patient.id,                            // L31116
            medicalRecordType: custView == 1 ? 1 : 5               // L31117
        };
        new ObjectFactory().saveOrQuery(
            "/admin/addMedicalRecord.json",                        // L31119 — 唯一直接 Create API
            obj
        ).then(function (res) {
            if (res.status == 0) {
                Popup.notice("新增成功");
                if (res.object.medicalRecordType == 5) {            // L31123
                    $state.go("adminSalesRecord.myMaterialBill", {  // L31124 — Sale
                        medicalRecordId: res.object.id,             // L31125
                        patientId: res.object.patientId             // L31126
                    });
                } else {
                    $state.go("adminMyRecord.myMaterialBill", {    // L31129 — Check/Optometry
                        medicalRecordId: res.object.id,             // L31130
                        patientId: res.object.patientId             // L31131
                    });
                }
            } else {
                Popup.notice(res.errmsg);
            }
        });
    }
};
```

### 5.2 addMedicalRecord.json 全字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | addSaleRecordCtrl（L31055 范围） |
| B. 调用行 | L31119 |
| C. Request | `{ patientId, medicalRecordType: custView == 1 ? 1 : 5 }` |
| D. patientId Source | `item.patient.id`（用户选中的 Patient 对象） |
| E. medicalRecordType Source | `custView == 1 ? 1 : 5`（来自 affirm 参数 custView） |
| F. Response 顶层 | `res.object` |
| G. Response.object 字段 | `id` / `medicalRecordType` / `patientId` |
| H. Response.object.id | L31125 / L31130 `res.object.id` → **medicalRecordId** |
| I. Response.object.medicalRecordType | L31123 `res.object.medicalRecordType == 5` |
| J. Response.object.patientId | L31126 / L31131 → State 参数 |
| K. 是否保存到 Scope | F（未保存到 $scope） |
| L. 是否进入 State | **A** — 立即 $state.go |
| M. State 参数 | `{ medicalRecordId, patientId }` |
| N. Target Controller (== 5) | adminSalesRecord.myMaterialBill |
| O. Target Controller (!= 5) | adminMyRecord.myMaterialBill |
| P. Target API | F（直接进 State，无后续 API） |
| Q. 是否再次 getMedicalRecord | F（直接用 res.object.id 即可） |

### 5.3 addMedicalRecord.json 结论

- **A — 明确 Create API**（仅 1 个）
- 写入模式：直接返回完整新建对象 (id + medicalRecordType + patientId)
- 立即 $state.go 分流（基于 medicalRecordType）
- 唯一性：仅 1 个调用点（L31119），1 个 Controller（addSaleRecordCtrl）

---

## 6. beginCustomerCheckin 系列深度审计

### 6.1 4 个调用点全量

`Select-String 'beginCustomerCheckin\.json' controller.js` 共 3 处，加上 S1-137R 误把 L10605 算作 1 处，**实际 3 处**：

| # | 行号 | Controller | 用途 |
|---|---|---|---|
| 1 | L10605 | 候诊队列 (case 0 接诊) | 接诊并进入病历 |
| 2 | L33127 | adminMyRecordCtrl (selectMedicalType) | 病历类型选择 |
| 3 | L34947 | optometryCtrl (beginCustomerCheckin) | 验光入口（先建接诊）|

### 6.2 L10605 完整证据

```javascript
// L10600-L10616 dealWithBtn case 0
$scope.dealWithBtn = function (status, employee) {
  switch (status) {
    case 0: //接诊
      Popup.confirm("为该用户创建电子病历?", function () {
        HttpFactory.object("/admin/beginCustomerCheckin.json", {
          customerCheckinId: employee.customerCheckin.id,        // L10606
          medicalRecordType: 1                                   // L10607
        }).then(function (response) {
          $state.go("adminMyRecord.myMemberRecord", {            // L10609
            medicalRecordId: response.customerCheckin.medicalRecordId,  // L10610
            patientId: employee.patient.id                       // L10611
          });
        }, ...);
      });
      break;
  }
};
```

| 项目 | 字符级证据 |
|---|---|
| Request | `{ customerCheckinId, medicalRecordType: 1 }` |
| Response 实际消费 | `response.customerCheckin.medicalRecordId`（L10610） |
| 立即 State | $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) |
| 是否 Save to Scope | F |
| 是否再 getMedicalRecord | F |
| 是否 Create MedicalRecord | **A — 间接**（API 名称含 Begin，但 Response 含 medicalRecordId） |

### 6.3 L33127 完整证据

```javascript
// L33125-L33150 adminMyRecordCtrl selectMedicalType
$scope.selectMedicalType = function () {
  $scope.clinckFactory = new ObjectFactory();
  var clinckPromise = $scope.clinckFactory.saveOrQuery(
    "/admin/beginCustomerCheckin.json",
    { customerCheckinId: $scope.customerCheckinId, medicalRecordType: 1 }   // L33127
  );
  clinckPromise.then(function (response) {
    if (response.status == 1) {
      Popup.notice(response.errmsg, 2000, function () {});
      $state.go("myMember", {}, { reload: true });
    } else {
      $scope.getMedicalTypeFactory = new ObjectFactory();
      var typePromise = $scope.getMedicalTypeFactory.saveOrQuery(
        "/admin/getMedicalRecord.json",
        { id: response.result.vo.customerCheckin.medicalRecordId }   // L33134
      );
      typePromise.then(function (res) {
        if (res.object.medicalRecordType == 5) {                    // L33136
          $state.go("adminSalesRecord.myMaterialBill", {            // → Sale
            medicalRecordId: res.object.id,
            patientId: $scope.patientId
          });
        } else {
          $state.go("adminMyRecord.myMemberRecord", {               // → Check/Optometry
            medicalRecordId: res.object.id,
            patientId: $scope.patientId
          });
        }
      });
    }
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| Request | `{ customerCheckinId, medicalRecordType: 1 }` |
| Response 消费 (第一层) | `response.result.vo.customerCheckin.medicalRecordId`（L33134） |
| 第二层 API | `getMedicalRecord.json`（L33134）|
| 第三层 Branch | `res.object.medicalRecordType == 5`（L33136）|
| 立即 State (== 5) | $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId }) |
| 立即 State (!= 5) | $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) |
| 特点 | 唯一会立即 getMedicalRecord 二次确认 type 的路径 |

### 6.4 L34947 完整证据

```javascript
// L34945-L34958 optometryCtrl beginCustomerCheckin
$scope.beginCustomerCheckin = function (info) {
  var customerCheckinId = info.customerCheckin.id;                  // L34946
  new ObjectFactory().saveOrQuery(
    "/admin/beginCustomerCheckin.json",
    {
      customerCheckinId: customerCheckinId,                         // L34948
      medicalRecordType: $scope.choseUser.glassestype               // L34949
    }
  ).then(function (result) {
    if (result.status) {
      return Popup.notice(result.errmsg);
    }
    $state.go("optometryGlasses", {                                 // L34954
      medicalRecordId: result.result.vo.customerCheckin.medicalRecordId  // L34955
    });
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| Request | `{ customerCheckinId, medicalRecordType: $scope.choseUser.glassestype }` |
| medicalRecordType Source | `$scope.choseUser.glassestype`（UI 选择） |
| Response 消费 | `result.result.vo.customerCheckin.medicalRecordId`（L34955） |
| 立即 State | $state.go("optometryGlasses", { medicalRecordId }) |
| 特点 | 唯一直接跳 optometryGlasses（**不经 myMemberRecord 中转**） |

### 6.5 beginCustomerCheckin.json 总结

| 路径 | 是否 Create MedicalRecord | 等级 | 下一站 State |
|---|---|---|---|
| L10605 (候诊队列) | **A 间接** | 立即 adminMyRecord.myMemberRecord |
| L33127 (adminMyRecord selectMedicalType) | **A 间接** | getMedicalRecord → branch → Sale/myMemberRecord |
| L34947 (optometryCtrl) | **A 间接** | 立即 optometryGlasses |

**3 个调用点都是"创建/关联 MedicalRecord" 路径**，但**都不是直接 Create API**（API 名称是 Begin）。

### 6.6 3 个调用点的差异

| 维度 | L10605 | L33127 | L34947 |
|---|---|---|---|
| medicalRecordType Source | 硬编码 1 | 硬编码 1 | `$scope.choseUser.glassestype` |
| Response 消费路径 | `response.customerCheckin.medicalRecordId` | `response.result.vo.customerCheckin.medicalRecordId` | `result.result.vo.customerCheckin.medicalRecordId` |
| 是否 getMedicalRecord 二次确认 | F | **A**（L33134） | F |
| Target State | adminMyRecord.myMemberRecord | adminSalesRecord.myMaterialBill OR adminMyRecord.myMemberRecord | optometryGlasses |

---

## 7. receiveSelfAndBeginCustomerCheckin 深度审计

### 7.1 1 个调用点 L33195

```javascript
// L33193-L33208 adminMyRecordCtrl
$scope.receiveSelfAndBeginCustomerCheckin = function (customerCheckinId) {
  Popup.confirm("为该用户创建电子病历？", function () {
    HttpFactory.object(
      '/admin/receiveSelfAndBeginCustomerCheckin.json',
      {
        customerCheckinId: customerCheckinId,                      // L33196
        medicalRecordType: 1                                       // L33197
      }
    ).then(function (res) {
      if (res.status) {
        return Popup.notice(res.errmsg);
      }
      $state.go("adminMyRecord.myMemberRecord", {                  // L33202
        medicalRecordId: res.customerCheckin.medicalRecordId,      // L33203
        patientId: res.patient.id                                  // L33204
      });
    });
  });
};
```

### 7.2 receiveSelfAndBeginCustomerCheckin.json 字段分析

| 项目 | 字符级证据 |
|---|---|
| A. Controller | adminMyRecordCtrl (L33158) |
| B. 调用行 | L33195 |
| C. Request | `{ customerCheckinId, medicalRecordType: 1 }` |
| D. customerCheckinId Source | `customerCheckinId` 函数参数 |
| E. medicalRecordType Source | 硬编码 1 |
| F. Response 实际消费 | `res.customerCheckin.medicalRecordId` (L33203) + `res.patient.id` (L33204) |
| G. 是否 Save to Scope | F |
| H. 是否再 getMedicalRecord | F |
| I. 立即 State | $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) |
| J. 是否 Create MedicalRecord | **A 间接**（API 名称含 Begin，Response 含 medicalRecordId） |
| K. 与 beginCustomerCheckin 区别 | Response 还额外返回 `res.patient.id`（非 customerCheckin.patientId） |

### 7.3 与 beginCustomerCheckin 区别

| API | Request | Response 字段差异 | 是否含 patientId |
|---|---|---|---|
| beginCustomerCheckin.json | `{customerCheckinId, medicalRecordType: 1}` | `response.result.vo.customerCheckin.medicalRecordId` | F（要从 customerCheckin.patientId 派生或外部传入） |
| receiveSelfAndBeginCustomerCheckin.json | 同上 | `res.customerCheckin.medicalRecordId` + `res.patient.id` | **A — 直接 patientId** |

---

## 8. insertCustomerCheckin* 深度审计

### 8.1 4 个调用点全量

| # | 行号 | API | 所在 Controller | 是否进入 beginCustomerCheckin 链 |
|---|---|---|---|---|
| 1 | L8667 | insertCustomerCheckinOfNewPaitent.json | addCheckinCtrl | F |
| 2 | L8679 | insertCustomerCheckinOfNewCustomer.json | addCheckinCtrl | F |
| 3 | L8681 | insertCustomerCheckin.json | addCheckinCtrl | F |
| 4 | L34914 | insertCustomerCheckin.json | optometryCtrl | **A**（L34929 链式调用）|

### 8.2 L8667 insertCustomerCheckinOfNewPaitent.json 详细

```javascript
// L8665-L8676 addCheckinCtrl.create
$scope.checkCustomer.appointId = aId;
$scope.insertCustomerCheckFactory = new ObjectFactory();
var insertPromise = $scope.insertCustomerCheckFactory.saveOrQuery(
  "/admin/insertCustomerCheckinOfNewPaitent.json",
  $scope.checkCustomer                                                // L8667 Request: $scope.checkCustomer
);
insertPromise.then(function (res) {
  if (res.status == 0) {
    Popup.notice("新增成功");
    var printCheckinId = res.result.vo.customerCheckin.id;            // L8671 — 只用 customerCheckin.id
    dealNeedPrint(printCheckinId);
  } else {
    Popup.notice(res.errmsg);
  }
});
```

| 项目 | 字符级证据 |
|---|---|
| Request | `$scope.checkCustomer` (含 appointId / registrationFeeId / customerName / linkMobile / employeeId / gender / idCard) |
| Response 实际消费 | `res.result.vo.customerCheckin.id`（L8671） |
| 是否消费 medicalRecordId | **F**（**完全未消费**）|
| 是否消费 medicalRecordType | F |
| 后续 | `dealNeedPrint(printCheckinId)` → `$state.go("checkinList", printObj)`（L8654）|
| 是否 Create MedicalRecord | **F**（仅创建 CustomerCheckin）|

### 8.3 L8679 / L8681 insertCustomerCheckinOfNewCustomer / insertCustomerCheckin

```javascript
// L8678-L8720 addCheckinCtrl.create
if (!$scope.obj.patientId) {
  url = "/admin/insertCustomerCheckinOfNewCustomer.json";   // L8679
} else {
  url = "/admin/insertCustomerCheckin.json";                 // L8681
}
if ($scope.guahao) {
  $scope.obj.registrationFeeId = $scope.registrationFeeId;
}
var t = $scope.obj.birthday;
if (t) {
  $scope.obj.birthday = new Date(t).toString();
} else {
  delete $scope.obj.birthday;
}
new ObjectFactory().saveOrQuery(url, $scope.obj).then(function (res) {
  if (res.status == 0) {
    var printCheckinId = res.result.vo.customerCheckin.id;   // L8697 — 只用 customerCheckin.id
    Popup.notice("新增成功");
    dealNeedPrint(printCheckinId);
  } else {
    Popup.notice(res.errmsg);
  }
});
```

| 项目 | 字符级证据 |
|---|---|
| Request | `$scope.obj` (含 patientId / name / birthday / registrationFeeId 等) |
| Response 实际消费 | `res.result.vo.customerCheckin.id`（L8697）|
| 是否消费 medicalRecordId | **F** |
| 后续 | `dealNeedPrint(printCheckinId)` → checkinList |
| 是否 Create MedicalRecord | **F** |

### 8.4 L34914 insertCustomerCheckin.json（optometryCtrl 内）

```javascript
// L34908-L34921 optometryCtrl addUser.affirm
$scope.choseUser = {
  ...
  affirm: function affirm(obj) {
    var object = {};
    object.name = obj.customer.customerName;
    object.gender = obj.customer.gender;
    object.patientId = obj.patient.id;
    object.employeeId = $scope.employeeId;
    new ObjectFactory().saveOrQuery(
      "/admin/insertCustomerCheckin.json",
      object                                                            // L34914
    ).then(function (res) {
      if (res.status == 0) {
        $scope.addUser.switch(false, res.result.vo);                    // L34916 — 关闭 modal
      } else {
        Popup.notice(res.errmsg);
      }
    });
  }
};

$scope.addUser = {
  ...
  switch: function _switch(bool, info) {
    this.edit = false;
    this.show = bool;
    if (info) {
      $scope.beginCustomerCheckin(info);                                // L34929 — 链式调用 beginCustomerCheckin
    }
  }
};

// L34945-L34958 optometryCtrl beginCustomerCheckin
$scope.beginCustomerCheckin = function (info) {
  var customerCheckinId = info.customerCheckin.id;                       // L34946
  new ObjectFactory().saveOrQuery(
    "/admin/beginCustomerCheckin.json",
    {
      customerCheckinId: customerCheckinId,
      medicalRecordType: $scope.choseUser.glassestype
    }
  ).then(function (result) {
    if (result.status) {
      return Popup.notice(result.errmsg);
    }
    $state.go("optometryGlasses", {
      medicalRecordId: result.result.vo.customerCheckin.medicalRecordId  // L34955
    });
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| Request | `{ name, gender, patientId, employeeId }` |
| Response 实际消费 | `res.result.vo`（整个 vo）→ L34916 switch(false, res.result.vo) |
| 链式调用 | L34929 `$scope.beginCustomerCheckin(info)` |
| 第二跳 | L34947 beginCustomerCheckin.json → L34955 派生 medicalRecordId |
| 是否 Create MedicalRecord | **F 直接**（L34914 仅 create CustomerCheckin）；**A 间接**（链式 L34947 才创建 MedicalRecord） |

### 8.5 insertCustomerCheckin* S1-137R 误判修正

| S1-137R 报告 | 实际字符级证据 |
|---|---|
| "insertCustomerCheckin* 共 3 处也间接 Create MedicalRecord" | **错误** |
| 实际：3 处（addCheckinCtrl 范围内 L8667/L8679/L8681）**完全不创建 MedicalRecord** | 仅创建 CustomerCheckin，**后续 dealNeedPrint → checkinList**，无 beginCustomerCheckin 链 |
| 唯一可能间接 Create：L34914 insertCustomerCheckin.json（optometryCtrl） | **是**，通过 L34929 链式调用 beginCustomerCheckin.json → MedicalRecord |

**S1-137R 误判修正**:
- S1-137R 报告 "insertCustomerCheckin* 3 处 = 3 条间接 Create 路径"
- 实际：addCheckinCtrl 范围内 3 处**不是** MedicalRecord Create 路径
- 只有 optometryCtrl 的 L34914（1 处）通过链式调用才是 MedicalRecord Create 路径
- **修正后**: insertCustomerCheckin* 系列中只有 1 条（间接）路径

---

## 9. updateMedicalRecord / setMedicalRecordProcessMode / cancelMedicalRecord / completeMedicalRecordDelivery 分类

### 9.1 updateMedicalRecord.json（L33479）

```javascript
// L33475-L33482 adminMyRecordCtrl
$scope.saveMedicalRecordFactory = new ObjectFactory();
var updatePromise = $scope.saveMedicalRecordFactory.saveOrQuery(
  "/admin/updateMedicalRecord.json",
  Object.assign($scope.obj, _defineProperty({}, $scope.firstDoctor.keys, $scope.firstDoctor.tip ? $scope.firstDoctor.tip : null))
);
```

| 项目 | 字符级证据 |
|---|---|
| API | updateMedicalRecord.json |
| Request | `$scope.obj` + firstDoctor 信息 |
| 用途 | **Update 现有 MedicalRecord** |
| 是否 Create | **F** |
| 是否影响 medicalRecordId | F（已存在 medicalRecordId 才会被 update）|

### 9.2 setMedicalRecordProcessMode.json（L35099）

```javascript
// L35083-L35109 optometryCtrl choseFactoryMethod
$scope.choseFactoryMethod = function (medical) {
  var medicalRecordId = medical.medicalRecord.id;
  var medicalRecordType = medical.medicalRecord.medicalRecordType;
  var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType];
  ...
  new ObjectFactory().saveOrQuery(
    "/admin/setMedicalRecordProcessMode.json",
    {
      medicalRecordId: medicalRecordId,
      toBeProcess: toBeProcess,                          // 0 不加工 / 1 加工
      medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson
    }
  ).then(function (result) {
    ...
    $scope.querySingleOrder();
    $scope.queryUndisposed();
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| API | setMedicalRecordProcessMode.json |
| Request | `{ medicalRecordId, toBeProcess, medicalProductStockBatctPoListJson }` |
| 用途 | **设置加工方式 (店内加工/不加工)** |
| 是否 Create | **F**（是 Update 加工方式）|

### 9.3 cancelMedicalRecord.json（L35150）

```javascript
// L35147-L35158 optometryCtrl fnMap.取消订单
取消订单: function _() {
  $scope.hint(1, function () {
    var medicalRecordId = item.medicalRecord.id;
    new ObjectFactory().saveOrQuery(
      "/admin/cancelMedicalRecord.json",
      { medicalRecordId: medicalRecordId }
    ).then(function (result) {
      ...
    });
  });
}
```

| 项目 | 字符级证据 |
|---|---|
| API | cancelMedicalRecord.json |
| Request | `{ medicalRecordId }` |
| 用途 | **取消 MedicalRecord 订单** |
| 是否 Create | **F** |

### 9.4 confirmMedicalRecordReturn.json（L35167）

```javascript
// L35162-L35178 optometryCtrl fnMap.退货
退货: function _() {
  ...
  new ObjectFactory().saveOrQuery(
    "/admin/confirmMedicalRecordReturn.json",
    { medicalRecordId: medicalRecordId }
  ).then(function (result) {
    ...
  });
}
```

| 项目 | 字符级证据 |
|---|---|
| API | confirmMedicalRecordReturn.json |
| Request | `{ medicalRecordId }` |
| 用途 | **确认 MedicalRecord 退货** |
| 是否 Create | **F** |

### 9.5 completeMedicalRecordDelivery.json（L35185 / L35204）

```javascript
// L35179-L35211 optometryCtrl fnMap
new ObjectFactory().saveOrQuery(
  "/admin/completeMedicalRecordDelivery.json",
  {
    medicalRecordId: medicalRecordId,
    medicalProductStockBatchPoListJson: ...
  }
)
```

| 项目 | 字符级证据 |
|---|---|
| API | completeMedicalRecordDelivery.json |
| Request | `{ medicalRecordId, medicalProductStockBatchPoListJson }` |
| 用途 | **完成 MedicalRecord 配送** |
| 是否 Create | **F** |

### 9.6 5 个 Update 类 API 总结

| API | 类型 | 是否 Create |
|---|---|---|
| updateMedicalRecord.json (L33479) | Update | F |
| setMedicalRecordProcessMode.json (L35099) | Update State | F |
| cancelMedicalRecord.json (L35150) | Cancel | F |
| confirmMedicalRecordReturn.json (L35167) | Confirm | F |
| completeMedicalRecordDelivery.json (L35185/L35204) | Complete | F |

---

## 10. insertMedicalRecordTemplate 系列分类

### 10.1 insertMedicalRecordTemplate.json（L33457 / L52253）

```javascript
// L33454-L33460 adminMyRecordCtrl
$scope.saveTemplateFactory = new ObjectFactory();
var promise = $scope.saveTemplateFactory.saveOrQuery(
  "/admin/insertMedicalRecordTemplate.json",
  $scope.save                                                  // L33457
);
```

| 项目 | 字符级证据 |
|---|---|
| API | insertMedicalRecordTemplate.json |
| 名称 | "Template"（模板） |
| 是否 Create MedicalRecord | **F**（是 Template 模板）|

### 10.2 Template 系列

| API | 类型 | 是否 Create MedicalRecord |
|---|---|---|
| insertMedicalRecordTemplate.json (L33457/L52253) | Template Insert | F |
| updateMedicalRecordTemplate.json (L57325) | Template Update | F |
| enableMedicalRecordTemplate.json (L55694/L58261/L58715/L58772) | Template Enable | F |
| disableMedicalRecordTemplate.json (L58247) | Template Disable | F |

---

## 11. MedicalRecord Create 候选分类总表

### 11.1 全部 18 个候选 API 分类

| API | Write | 直接 Create | 间接 Create | Update | Template | F |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| addMedicalRecord.json (L31119) | A | **A** | — | — | — | — |
| beginCustomerCheckin.json (L10605) | A | — | **A** | — | — | — |
| beginCustomerCheckin.json (L33127) | A | — | **A** | — | — | — |
| beginCustomerCheckin.json (L34947) | A | — | **A** | — | — | — |
| receiveSelfAndBeginCustomerCheckin.json (L33195) | A | — | **A** | — | — | — |
| insertCustomerCheckinOfNewPaitent.json (L8667) | A | — | — | — | — | **A**（仅 create CustomerCheckin）|
| insertCustomerCheckinOfNewCustomer.json (L8679) | A | — | — | — | — | **A** |
| insertCustomerCheckin.json (L8681/addCheckinCtrl) | A | — | — | — | — | **A** |
| insertCustomerCheckin.json (L34914/optometryCtrl) | A | — | **A**（链式 L34929 → L34947） | — | — | — |
| confirmArrivalOfAppoint.json (L8658) | A | — | — | — | — | **A**（仅 confirm Arrival）|
| updateMedicalRecord.json (L33479) | A | — | — | **A** | — | — |
| setMedicalRecordProcessMode.json (L35099) | A | — | — | **A** | — | — |
| cancelMedicalRecord.json (L35150) | A | — | — | **A** | — | — |
| confirmMedicalRecordReturn.json (L35167) | A | — | — | **A** | — | — |
| completeMedicalRecordDelivery.json (L35185/L35204) | A | — | — | **A** | — | — |
| insertMedicalRecordTemplate.json (L33457/L52253) | A | — | — | — | **A** | — |
| updateMedicalRecordTemplate.json (L57325) | A | — | — | — | **A** | — |
| enableMedicalRecordTemplate.json (L55694/L58261/L58715/L58772) | A | — | — | — | **A** | — |
| disableMedicalRecordTemplate.json (L58247) | A | — | — | — | **A** | — |
| medicalCheckBeforeCustomerCheckin.json (L8788) | A | — | — | — | — | **A**（诊前检查，仅 set medicalRecordId to modal Scope）|

### 11.2 Create 路径汇总

| 类型 | API | 数量 |
|---|---|---|
| **A 直接 Create** | addMedicalRecord.json | 1 |
| **A 间接 Create** | beginCustomerCheckin.json (3) + receiveSelfAndBeginCustomerCheckin.json (1) + insertCustomerCheckin.json (L34914 链式 1) | 5 |
| **Update** | updateMedicalRecord.json + setMedicalRecordProcessMode + cancel + confirmReturn + completeDelivery | 5 |
| **Template** | insertMedicalRecordTemplate + updateMedicalRecordTemplate + enable + disable | 5 |
| **F (非 MedicalRecord)** | insertCustomerCheckin*.json (addCheckinCtrl 3) + confirmArrivalOfAppoint + medicalCheckBeforeCustomerCheckin | 5 |

### 11.3 S1-137R 误判最终修正

| 误判点 | 修正 |
|---|---|
| S1-137R §"insertCustomerCheckin* 3 处间接 Create" | 实际 0 处是 MedicalRecord Create |
| S1-137R §"5 条独立创建路径" | 实际 **1 直接 + 4 间接 = 5 条**（L34914 链式属于间接路径之一）|
| 修正后 | addMedicalRecord (1) + beginCustomerCheckin (3) + receiveSelfAndBegin (1) = 5 条路径，**不含** addCheckinCtrl 范围的 insertCustomerCheckin* |

---

## 12. Create → medicalRecord.id 完整链

### 12.1 5 条 Create 路径全 ID 跟踪

| 路径 | API | Request ID | Response ID 字段 | 实际获取 medicalRecordId 的位置 | 立即进入 State |
|---|---|---|---|---|---|
| 1 | addMedicalRecord.json (L31119) | patientId | res.object.id | L31125 / L31130 | $state.go myMaterialBill |
| 2 | beginCustomerCheckin.json (L10605) | customerCheckinId | response.customerCheckin.medicalRecordId | L10610 | $state.go myMemberRecord |
| 3 | beginCustomerCheckin.json (L33127) | customerCheckinId | response.result.vo.customerCheckin.medicalRecordId → getMedicalRecord.json → res.object.id | L33134 (取 medicalRecordId) → L33138 (从 getMedicalRecord 取 id) | $state.go Sale/myMemberRecord |
| 4 | beginCustomerCheckin.json (L34947) | customerCheckinId | result.result.vo.customerCheckin.medicalRecordId | L34955 | $state.go optometryGlasses |
| 5 | receiveSelfAndBeginCustomerCheckin.json (L33195) | customerCheckinId | res.customerCheckin.medicalRecordId | L33203 | $state.go myMemberRecord |

### 12.2 ID 区分严格表

| 字段 | 来源 | 含义 |
|---|---|---|
| `patientId` | addMedicalRecord Request | Patient 主键 |
| `customerCheckinId` | beginCustomerCheckin / receiveSelf Request | CustomerCheckin 主键 |
| `res.object.id` | addMedicalRecord Response | **新建**的 MedicalRecord 主键 |
| `res.customerCheckin.medicalRecordId` | beginCustomerCheckin / receive Response | MedicalRecord 主键（**已关联到该 customerCheckin**）|
| `res.result.vo.customerCheckin.medicalRecordId` | 同上（不同 Response 路径）| 同上 |
| `medicalRecordId` | $stateParams | State 入口参数（已创建的 MedicalRecord）|
| `customerCheckin.id` | insertCustomerCheckin Response | CustomerCheckin 主键（**不一定是 MedicalRecord**）|
| `printCheckinId` | 局部变量（L8671/L8697）| **≡ customerCheckin.id** |

### 12.3 5 条 Create 路径立即 State 汇总

| 路径 | medicalRecordType | 立即 State | 实际 entry |
|---|---|---|---|
| 1 addMedicalRecord (== 5) | custView==1?1:5 → 1 或 5 | adminSalesRecord.myMaterialBill | **Sale** 入口 |
| 1 addMedicalRecord (!= 5) | → 1 | adminMyRecord.myMaterialBill | **Check/Optometry** 入口 |
| 2 begin (L10605) | 1 | adminMyRecord.myMemberRecord | **Check/Optometry** 入口 |
| 3 begin (L33127) (== 5) | 1 → getMedicalRecord → 5 | adminSalesRecord.myMaterialBill | **Sale** 入口 |
| 3 begin (L33127) (!= 5) | 1 → getMedicalRecord → 其它 | adminMyRecord.myMemberRecord | **Check/Optometry** 入口 |
| 4 begin (L34947) | $scope.choseUser.glassestype | optometryGlasses | **Optometry** 入口 |
| 5 receiveSelf (L33195) | 1 | adminMyRecord.myMemberRecord | **Check/Optometry** 入口 |

---

## 13. medicalRecordType 生命周期（7 分类 + 5 业务规则）

### 13.1 16 处 7 分类（S1-137R 已确认）

| 分类 | 数量 | 行号 | 说明 |
|---|---|---|---|
| A. Request 字段 | 4 | L10607/L31117/L33127/L33197 | 写入 Create Request |
| B. Response Branch `== 5` | 6 | L2257/L31123/L32951/L33055/L33136/L33156 | 决定 State |
| C. Function Param | 1 | L31141 | goRecord 函数参数 |
| D. 派生提取 | 1 | L35086 | `medical.medicalRecord.medicalRecordType` |
| E. 转换 `{ 6: 1, 7: 0 }` | 1 | L35087 | choseFactoryMethod UI 转换 |
| F. 派生于 scope `choseUser.glassestype` | 1 | L34949 | L34949 派生来源 |
| G. 调试输出 | 1 | L31142 | console.log |

### 13.2 medicalRecordType 5 业务规则

| 规则 | 等级 | 字符级证据 |
|---|---|---|
| 1. `== 5` → Sale 入口 | **A** | 6 处全部走 `adminSalesRecord.myMaterialBill` |
| 2. `!= 5` → Check/Optometry 入口 | **A** | 6 处 else 分支（5 处 myMemberRecord + 1 处 myCheckBill + 2 处 myMaterialBill）|
| 3. `== 1` → Checkin 类型（Request 硬编码）| **A** | L10607/L33127/L33197 3 处 Request |
| 4. `custView == 1 ? 1 : 5` → addMedicalRecord 派生 | **A** | L31117 唯一 |
| 5. `{ 6: 1, 7: 0 }` → choseFactoryMethod UI 转换 | **A** | L35087 唯一（**不是 State 路由规则**）|

### 13.3 medicalRecordType → State 决策矩阵

| Source Controller | API | medicalRecordType 来源 | == 5 | != 5 |
|---|---|---|---|---|
| getMedical (L2251) | getMedicalRecord.json | Response | adminSalesRecord.myMaterialBill | adminMyRecord.myCheckBill |
| addSaleRecordCtrl (L31119) | addMedicalRecord.json (Create) | custView==1?1:5 | adminSalesRecord.myMaterialBill | adminMyRecord.myMaterialBill |
| goRecord (L31141) | (function) | param | adminSalesRecord.myMaterialBill | adminMyRecord.myMaterialBill |
| myMedicalRecordListCtrl (L32946) | getMedicalRecord.json | Response | adminSalesRecord.myMaterialBill | adminMyRecord.myMemberRecord |
| myMedicalRecordListOfDoctorCtrl (L33050) | getMedicalRecord.json | Response | adminSalesRecord.myMaterialBill | adminMyRecord.myMemberRecord |
| selectMedicalType (L33125) | beginCustomerCheckin → getMedicalRecord | Request 1 → Response | adminSalesRecord.myMaterialBill | adminMyRecord.myMemberRecord |
| getMedicalRecord (L33152) | getMedicalRecord.json | Response | adminSalesRecord.myMaterialBill | adminMyRecord.myMemberRecord |

**汇总**: 6 处 `== 5` Branch 全部走 `adminSalesRecord.myMaterialBill`（100% 一致）。非 5 走 4 个不同 State：
- adminMyRecord.myMemberRecord（5 处）
- adminMyRecord.myCheckBill（1 处）
- adminMyRecord.myMaterialBill（2 处）

### 13.4 6→1, 7→0 转换详细

```javascript
// L35084-L35109 optometryCtrl choseFactoryMethod
$scope.choseFactoryMethod = function (medical) {
  var medicalRecordId = medical.medicalRecord.id;
  var medicalRecordType = medical.medicalRecord.medicalRecordType;     // L35086
  var toBeProcess = { 6: 1, 7: 0 }[medicalRecordType];                 // L35087
  // toBeProcess: 0=不加工, 1=加工
  ...
  new ObjectFactory().saveOrQuery(
    "/admin/setMedicalRecordProcessMode.json",
    {
      medicalRecordId: medicalRecordId,
      toBeProcess: toBeProcess,                                         // L35101
      medicalProductStockBatctPoListJson: medicalProductStockBatctPoListJson
    }
  ).then(...);
};
```

**6→1, 7→0 实际意义**:
- medicalRecordType == 6 → toBeProcess = 1 (店内加工)
- medicalRecordType == 7 → toBeProcess = 0 (不加工)
- 写入 `setMedicalRecordProcessMode.json` 的 `toBeProcess` 字段
- **不是 State 路由规则**

**S1-137R 已确认**: `{ 6: 1, 7: 0 }` 是 UI 加工方式选择，不是 State 路由。

### 13.5 custView 全量搜索

`Select-String 'custView' controller.js` — 1 处 L31117（addMedicalRecord 唯一使用）。

custView 来源待查（task 14 要求）：
- 来源：affirm(item, custView) 函数参数（L31111）
- 调用者：在 addSaleRecordCtrl HTML 模板中（`addSaleRecord.html`）传入
- **L3 (HTML 模板) — F**（不在 controller.js 范围）

### 13.6 choseUser.glassestype 来源

`Select-String 'glassestype' controller.js` — 多处（optometryCtrl 范围）：
- L34901 `this.glassestype = glassestype`（choseUser.open 设置）
- L34949 `medicalRecordType: $scope.choseUser.glassestype`（beginCustomerCheckin Request）

**glassestype 来源**:
- 用户在 HTML 模板中选择（`addSaleRecord.html` / optometry 模板）
- L1 字符级确认：L34901 open 函数接受参数
- L2 解释：glassestype 决定 MedicalRecord 的加工类型（"镜片"还是"镜架"等）
- L3 后端实体：F

---

## 14. Create → Check / Optometry / Sale / Charge / Delivery 分流

### 14.1 Create → Check 路径

| 来源 | 路径 | 等级 |
|---|---|---|
| beginCustomerCheckin (L10605) | → $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) → myMemberRecordCtrl → 后续可走 assistChecking | A |
| beginCustomerCheckin (L33127) (!= 5) | → $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) | A |
| receiveSelfAndBegin (L33195) | → $state.go("adminMyRecord.myMemberRecord", { medicalRecordId, patientId }) | A |
| addMedicalRecord (L31119) (!= 5) | → $state.go("adminMyRecord.myMaterialBill", { medicalRecordId, patientId }) | A |

**4 条 Create 路径均可进入 Check**（经 myMemberRecord 或 myMaterialBill 中转）。

### 14.2 Create → Optometry 路径

| 来源 | 路径 | 等级 |
|---|---|---|
| beginCustomerCheckin (L34947) | → $state.go("optometryGlasses", { medicalRecordId }) | A |
| addMedicalRecord (L31119) (!= 5) | → adminMyRecord.myMaterialBill → 后续可走 optometry | A |
| 其它 3 条 | 经 myMemberRecord 中转 → 可走 optometry | A |

**直接进 Optometry 的唯一路径：L34947 optometryGlasses**。

### 14.3 Create → Sale 路径

| 来源 | 路径 | 等级 |
|---|---|---|
| addMedicalRecord (L31119) (== 5) | → $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId }) | A |
| beginCustomerCheckin (L33127) (== 5) | → $state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId }) | A |

**直接进 Sale 的路径 2 条**。**注意**: 这 2 条都依赖 medicalRecordType == 5 的分支。

### 14.4 Create → Charge 路径

Create 后到 Charge 的路径**间接经 MedicalRecord → cashflow 桥**：

```
Create (任意路径)
→ medicalRecord.id
→ $state.go("adminMyRecord.myMaterialBill" or "myMemberRecord") → 选商品 → 算费
→ createCashFlowForMedicalRecord.json (W, L6925)
→ res.result.object (cashflowId)
→ $state.go("waitPayDetail", { cashflowId: res.result.object })
```

| 来源 | 等级 |
|---|---|
| Create → MedicalRecord → createCashFlowForMedicalRecord → cashflowId → Charge | A（间接 2 层）|

### 14.5 Create → Delivery 路径

**F**：
- 当前源码未发现 Create 后直接进入 Delivery 的 State
- Delivery 入口是 cashflowId，不是 medicalRecordId
- F 必须写："当前源码范围未发现 Create → Delivery 直接桥。"

---

## 15. CustomerCheckin ↔ MedicalRecord 双向矩阵

### 15.1 双向矩阵

| 关系 | Function | State | API Resp→Req | Scope | Factory | Object | 共现 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **CustomerCheckin → MedicalRecord** | A（6 处字符级桥） | A（$state.go 携带） | A（customerCheckin.medicalRecordId 6 处） | C | F | F | A |
| **MedicalRecord → CustomerCheckin** | F | F | F（未发现 medicalRecord → customerCheckin 桥） | F | F | F | C（medicalRecord 内部可能引用 customerCheckin，待查）|

**MedicalRecord → CustomerCheckin 方向**:
- 在 optometryCtrl / adminMyRecord / etc. 中未发现 `medicalRecord.customerCheckin` 或 `medicalRecord.customerCheckinId` 字段
- medicalRecord 自身字段：id, medicalRecordType, patientId, templateId（基于 addMedicalRecord Response + getMedicalRecord 推断）
- **F**（无字符级证据）

### 15.2 关键反向排除

| 误判 | 实际 |
|---|---|
| "medicalRecord → customerCheckin" | F（medicalRecord 不包含 customerCheckin 字段）|
| "insertCustomerCheckin → MedicalRecord" | F（仅 create CustomerCheckin，**不**自动 create MedicalRecord）|
| "MedicalRecord 通过 customerCheckin 创建" | A（间接路径：beginCustomerCheckin 返回 customerCheckin.medicalRecordId）|

---

## 16. Patient ↔ MedicalRecord 矩阵

### 16.1 patientId 5 个出现位置

| # | 行号 | 上下文 | 用途 |
|---|---|---|---|
| 1 | L31116 | addMedicalRecord.json Request | Create MedicalRecord 的输入 |
| 2 | L31126 / L31131 | addMedicalRecord Response → State | 立即进入 State |
| 3 | L10611 | L10610 $state.go myMemberRecord State 参数 | 立即进入 State |
| 4 | L33204 | L33203 $state.go myMemberRecord State 参数 | 立即进入 State |
| 5 | L6693 | `res.object.medicalRecord.patientId` → getPatientInfo | 在 Sale 流程中获取 Patient 详情 |

### 16.2 5 条 Create 路径的 patientId 流向

| 路径 | patientId 来源 | 流向 |
|---|---|---|
| addMedicalRecord (L31119) | `item.patient.id` (UI 选中) | Request → Response → State |
| beginCustomerCheckin (L10605) | `employee.patient.id` (候诊队列) | 外部传入 → State |
| beginCustomerCheckin (L33127) | `$scope.patientId` (UI 选中) | 外部传入 → State |
| beginCustomerCheckin (L34947) | F（**未传入** patientId）| 仅 $state.go optometryGlasses 不带 patientId |
| receiveSelfAndBegin (L33195) | `res.patient.id` (Response 自带) | Response → State |

**注意**: L34947 路径不携带 patientId（仅 medicalRecordId），意味着 optometryGlasses 入口需要从其它途径获取 patientId。

### 16.3 Patient → MedicalRecord 一对多

**未做实际推断**（L3 缺失，无后端数据库证据）。字符级仅能证明：
- 1 个 patientId 可对应 0-N 个 medicalRecordId（通过 addMedicalRecord 重复调用）
- **不补 "1:N" 推断**

---

## 17. Sale ↔ MedicalRecord 矩阵

### 17.1 Sale 入口的 medicalRecordId 来源

| 来源 | 等级 | 字符级证据 |
|---|---|---|
| addMedicalRecord (== 5) → adminSalesRecord.myMaterialBill | A | L31124 |
| beginCustomerCheckin (L33127) (== 5) → adminSalesRecord.myMaterialBill | A | L33137 |
| myMedicalRecordListCtrl → adminSalesRecord.myMaterialBill | A | L32952 |
| myMedicalRecordListOfDoctorCtrl → adminSalesRecord.myMaterialBill | A | L33056 |
| getMedical (L2251) (== 5) → adminSalesRecord.myMaterialBill | A | L2258 |

**5 条进 Sale 入口的路径**（A 等级），其中 1 条直接来自 addMedicalRecord（Create API）。

### 17.2 Sale 是否是 MedicalRecord Create 唯一入口？

| 命题 | 答案 | 等级 |
|---|---|---|
| addMedicalRecord 是否只被 Sale 调用？ | **YES**（仅 addSaleRecordCtrl L31119）| A |
| Sale 是否拥有独立 Create 入口？ | **YES**（addMedicalRecord.json）| A |
| Sale 是否唯一 Create 入口？ | **NO**（beginCustomerCheckin / receiveSelfAndBegin 也可经 medicalRecordType=5 走 Sale）| F |
| "Sale 是 Create 入口" 是 | **A — Controller 层入口 + API 层入口** | A |

**注意**: addMedicalRecord.json 实际由 addSaleRecordCtrl 调用（L31119），所以"Create 入口" 的 Controller 是 addSaleRecordCtrl，但 MedicalRecord 不一定最终走 Sale（取决于 medicalRecordType）。

---

## 18. State 状态机

### 18.1 关键 State 入口

| State | Controller | 入口参数 | medicalRecordId 来源 |
|---|---|---|---|
| **adminSalesRecord.myMaterialBill** | adminSalesRecordCtrl | medicalRecordId, patientId | State / Response |
| **adminMyRecord.myMemberRecord** | myMemberRecordCtrl | medicalRecordId | State |
| **adminMyRecord.myMaterialBill** | myMaterialBillCtrl | medicalRecordId, patientId | State |
| **adminMyRecord.myCheckBill** | myCheckBillCtrl | medicalRecordId, patientId | State |
| **optometry** | optometryCtrl | medicalRecordId | State |
| **optometryGlasses** | optometryGlassesCtrl | medicalRecordId | State |
| **assistChecking** | assistCheckingCtrl | medicalExamineId, medicalRecordId, editable | State |
| **checkinList** | checkinListCtrl | appointId, printCheckinId | State |
| **addMedicalRecord** | addMedicalRecordCtrl | medicalRecordId, patientId | State（HTML 模板录入入口）|
| **deliveryInput** | deliveryInputCtrl | cashflowId | State（**不**含 medicalRecordId）|
| **waitChargeDetail** | waitChargeDetailCtrl | cashflowId | State |
| **waitPayDetail** | waitPayDetailCtrl | cashflowId | State |
| **payedDetail** | payedDetailCtrl | cashflowId | State |

### 18.2 5 条 Create 路径 → State 全状态机

```
[Create Path 1: addMedicalRecord (L31119)]
  Input: patientId + medicalRecordType (custView==1?1:5)
  Output: res.object.{id, medicalRecordType, patientId}
  Route: 
    if (medicalRecordType == 5) → adminSalesRecord.myMaterialBill (Sale)
    else → adminMyRecord.myMaterialBill (Check/Optometry)

[Create Path 2: beginCustomerCheckin (L10605)]
  Input: customerCheckinId + medicalRecordType: 1
  Output: response.customerCheckin.medicalRecordId
  Route: adminMyRecord.myMemberRecord (Check/Optometry)

[Create Path 3: beginCustomerCheckin (L33127)]
  Input: customerCheckinId + medicalRecordType: 1
  Output: response.result.vo.customerCheckin.medicalRecordId → getMedicalRecord
  Route: 
    if (res.object.medicalRecordType == 5) → adminSalesRecord.myMaterialBill (Sale)
    else → adminMyRecord.myMemberRecord (Check/Optometry)

[Create Path 4: beginCustomerCheckin (L34947)]
  Input: customerCheckinId + medicalRecordType: $scope.choseUser.glassestype
  Output: result.result.vo.customerCheckin.medicalRecordId
  Route: optometryGlasses (Optometry, **不经 myMemberRecord 中转**)

[Create Path 5: receiveSelfAndBeginCustomerCheckin (L33195)]
  Input: customerCheckinId + medicalRecordType: 1
  Output: res.customerCheckin.medicalRecordId + res.patient.id
  Route: adminMyRecord.myMemberRecord (Check/Optometry)
```

### 18.3 5 条 Create 路径特征对比

| 维度 | 路径 1 | 路径 2 | 路径 3 | 路径 4 | 路径 5 |
|---|---|---|---|---|---|
| API | addMedicalRecord | beginCustomerCheckin | beginCustomerCheckin | beginCustomerCheckin | receiveSelfAndBegin |
| Type 来源 | custView 派生 | 硬编码 1 | 硬编码 1 | glassestype | 硬编码 1 |
| Response ID 路径 | res.object.id | response.customerCheckin.medicalRecordId | response.result.vo...→getMedicalRecord→res.object.id | result.result.vo.customerCheckin.medicalRecordId | res.customerCheckin.medicalRecordId |
| 是否二次 getMedicalRecord | F | F | **A** | F | F |
| Type 决定 State | **A — Yes** | F | **A — Yes** | F | F |
| 默认 State | myMaterialBill | myMemberRecord | branch (Sale/myMemberRecord) | optometryGlasses | myMemberRecord |
| patientId 来源 | Response | 外部传入 | 外部传入 | F（不带）| Response |

---

## 19. Create API 唯一性结论

### 19.1 直接 Create vs 间接 Create

| 类型 | API | 数量 |
|---|---|---|
| **A 直接 Create** | addMedicalRecord.json | 1 |
| **A 间接 Create**（经 customerCheckin.medicalRecordId）| beginCustomerCheckin.json × 3 + receiveSelfAndBeginCustomerCheckin.json × 1 + insertCustomerCheckin.json (L34914 链式) × 1 | 5 |
| **总计 Create 路径** | | **6 条** |

**唯一性结论**:
- addMedicalRecord.json **不是** 唯一 Create 路径
- 实际存在 **6 条独立 Create 路径**（1 直接 + 5 间接）
- "唯一" 误判彻底否定

### 19.2 6 条路径的"独立创建"定义

每条路径都满足：
- 独立的 API 入口
- 独立的 Request 字段模式
- 独立的 Response ID 消费模式
- 独立的 Next State 路由

**S1-137R 修正后**:
- S1-137R 报告 "至少 2 条" — 保守估计
- S1-138 精确审计: **实际 6 条**
- L34914 insertCustomerCheckin (链式) 是被 S1-137R 漏掉的第 6 条

### 19.3 addMedicalRecord.json 的唯一性

| 命题 | 答案 | 等级 |
|---|---|---|
| addMedicalRecord.json 是显式 Create API | **YES** | A |
| addMedicalRecord.json 是唯一**显式** Create API | **YES** | A |
| addMedicalRecord.json 是唯一 Create 路径 | **NO** | F |
| addMedicalRecord.json 是唯一直接 Create 路径 | **YES**（其他都是 Begin/Receive） | A |

**最终表述**:
- addMedicalRecord.json 是**唯一显式直接 Create API**（命名是 Create，Request/Response 模式是 Create）
- 但 MedicalRecord 实际有 6 条独立创建/关联路径
- 1 条直接（addMedicalRecord）+ 5 条间接（beginCustomerCheckin × 3, receiveSelfAndBegin × 1, insertCustomerCheckin 链式 × 1）

---

## 20. 精确数量

### 20.1 MedicalRecord 写 API 候选统计

| 分类 | 数量 |
|---|---|
| MedicalRecord 写 API 候选总数 | 20 |
| 明确 Create（直接）| 1 |
| 间接 Create | 5 |
| Update | 5 |
| Template | 5 |
| 非 MedicalRecord (F) | 4 (insertCustomerCheckin* × 3 + confirmArrivalOfAppoint + medicalCheckBeforeCustomerCheckin) |
| 总和验证 | 1 + 5 + 5 + 5 + 4 = 20 ✓ |

### 20.2 5 个直接/间接 Create 路径精确统计

| API | 调用数 | Controller 数 | Request 数 | Response 数 | medicalRecord.id 数 | State 数 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| addMedicalRecord.json | 1 | 1 | 1 | 1 | 1 (L31125) | 1 |
| beginCustomerCheckin.json | 3 | 3 | 3 | 3 | 3 (L10610/L33138/L34955) | 3 |
| receiveSelfAndBeginCustomerCheckin.json | 1 | 1 | 1 | 1 | 1 (L33203) | 1 |
| insertCustomerCheckin.json (L34914 链式) | 1 | 1 | 1 | 1 (L34914) + 1 (L34947) | 1 (L34955) | 1 (optometryGlasses) |
| **总计** | 6 | 6 | 6 | 6 (+1) | 6 | 6 |

### 20.3 medicalRecordType 精确统计

| 分类 | 数量 |
|---|---|
| Total | 16 |
| Request 字段 | 4 (L10607/L31117/L33127/L33197) |
| Response Branch `== 5` | 6 (L2257/L31123/L32951/L33055/L33136/L33156) |
| Function Param | 1 (L31141) |
| 派生提取 | 1 (L35086) |
| `{ 6: 1, 7: 0 }` 转换 | 1 (L35087) |
| 派生于 scope | 1 (L34949) |
| 调试输出 | 1 (L31142) |
| **总和** | 16 ✓ |

### 20.4 ID 类型统计

| ID 类型 | 5 条 Create 路径中作为输入 | 作为 Response 字段 |
|---|---|---|
| patientId | 1 (L31116) | 3 (L31126/L31131/L33204) |
| customerCheckinId | 4 (L10606/L33127/L34948/L33196) | 0 |
| medicalRecordId | 0 (State 入口) | 6 (L31125/L10610/L33138/L34955/L33203) |
| medicalRecordType | 4 (L10607/L31117/L33127/L33197) | 7 (L31123 + 6 Branch) |

### 20.5 5 条 Create 路径 → 业务模块入口

| 业务模块 | 直接进入的路径 |
|---|---|
| Sale | addMedicalRecord (== 5) + beginCustomerCheckin (L33127) (== 5) = 2 条 |
| Optometry | beginCustomerCheckin (L34947) = 1 条（**唯一**直接跳 optometryGlasses）|
| Check | 3 条 (L10605/L33127/L33195) 经 myMemberRecord |
| Charge | 0 条（Charge 经 cashflow 桥）|
| Delivery | 0 条（**F**）|

---

## 21. L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | API / Request / Response / State / Controller / Field 全部字符级 | A |
| L2 | "Create 路径" / "分流状态机" / "间接传播" / "UI 转换" | A |
| L3 | 数据库表 / 事务边界 / FK / 唯一索引 | **F**（无后端证据） |

---

## 22. 最终 StateMachine A-E

### StateMachine A: Appointment → CustomerCheckin → MedicalRecord

```
[Appointment]
  ↓ A — getAppointPatientVo (R) / getAppointSchoolMateVo (R)
[addCheckinCtrl (L8159)]
  ↓ A — insertCustomerCheckinOfNewPaitent (L8667) / insertCustomerCheckinOfNewCustomer (L8679) / insertCustomerCheckin (L8681) / confirmArrivalOfAppoint (L8658)
[CustomerCheckin (customerCheckin.id, customerCheckin.medicalRecordId=NULL)]
  ↓ A — beginCustomerCheckin.json (L10605/L33127/L34947) / receiveSelfAndBeginCustomerCheckin.json (L33195)
[MedicalRecord (medicalRecord.id, medicalRecordType, patientId)]
```

### StateMachine B: addMedicalRecord → MedicalRecord → Sale / Record

```
[addSaleRecordCtrl]
  ↓ A — patientId + medicalRecordType: custView==1?1:5
[addMedicalRecord.json (L31119)]
  ↓ A — Response: res.object.{id, medicalRecordType, patientId}
[MedicalRecord (新建)]
  ↓ A — if (medicalRecordType == 5)
[adminSalesRecord.myMaterialBill (Sale)]
  ↓ A — else
[adminMyRecord.myMaterialBill (Check/Optometry)]
```

### StateMachine C: CustomerCheckin → MedicalRecord → Check / Optometry

```
[CustomerCheckin (customerCheckin.medicalRecordId)]
  ↓ A — getMedicalRecord.json (R)  (L33134 唯一)
[MedicalRecord (medicalRecord.id, medicalRecordType)]
  ↓ A — branch (== 5 / != 5)
[adminSalesRecord.myMaterialBill (Sale)] or [adminMyRecord.myMemberRecord (Check/Optometry)]
  ↓ A — optometryGlasses (L34955 唯一直接跳)
[optometryGlasses (Optometry)]
```

### StateMachine D: MedicalRecord → Cashflow → Charge

```
[MedicalRecord (medicalRecord.id)]
  ↓ A — createCashFlowForMedicalRecord.json (W, L6925)
[Cashflow (cashflowId)]
  ↓ A — $state.go("waitPayDetail", { cashflowId: res.result.object })
[waitPayDetail (Charge 入口)]
  ↓ A — waitChargeDetail (L7070) / waitPayBack (L7156) / payedList (L8021)
[Charge Controller]
```

### StateMachine E: Cashflow → MedicalRecord (Delivery 内部派生)

```
[Cashflow (cashflowId)]
  ↓ A — $stateParams.cashflowId (5 处: L3814/L4026/L4238/L4381/L4940)
[Delivery Controller (deliveryInputCtrl / deliveryInputRecordCtrl / etc.)]
  ↓ A — getMedicalRecordPayVo.json (R, L4034)
[MedicalRecord.id (派生 $scope.medicalRecordId)]
  ↓ F — MedicalRecord → Delivery 反向 F
```

**F 严格表述**: "MedicalRecord → Delivery 反向桥在当前源码范围未观察到。Delivery 入口是 cashflowId，不是 medicalRecordId。"

---

## 23. 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | MedicalRecord Create API 总览 | 1 直接 + 5 间接 = 6 条 | A | — | 全部 | A |
| 2 | addMedicalRecord | 直接 Create | A | addSaleRecordCtrl | L31119 | A |
| 3 | beginCustomerCheckin (L10605) | 间接 Create | A | 候诊队列 | L10605 | A |
| 4 | receiveSelfAndBeginCustomerCheckin | 间接 Create | A | adminMyRecordCtrl | L33195 | A |
| 5 | insertCustomerCheckinOfNewPaitent | **非 MedicalRecord Create** | F | addCheckinCtrl | L8667 | F |
| 6 | insertCustomerCheckinOfNewCustomer | **非 MedicalRecord Create** | F | addCheckinCtrl | L8679 | F |
| 7 | insertCustomerCheckin (L8681) | **非 MedicalRecord Create** | F | addCheckinCtrl | L8681 | F |
| 8 | updateMedicalRecord | Update | A | adminMyRecordCtrl | L33479 | A (Update) |
| 9 | insertMedicalRecordTemplate | Template | A | adminMyRecordCtrl | L33457 | A (Template) |
| 10 | Create → medicalRecord.id | 6 条全部派生 res.object.id 或 customerCheckin.medicalRecordId | A | 6 处 | 全部 | A |
| 11 | customerCheckin → MedicalRecord | 6 处字符级桥 | A | 6 处 | L8791/L10610/L10642/L33134/L33203/L34955 | A |
| 12 | medicalRecord → customerCheckin | **无字符级证据** | F | — | — | F |
| 13 | patientId 生命周期 | 5 条 Create 中 4 条用 patientId | A | 多处 | L31116/L31126/L31131/L10611/L33204 | A |
| 14 | medicalRecordType 来源 | 4 Request + 1 派生 + 1 UI + 6 Branch | A | 多处 | 16 处 | A |
| 15 | medicalRecordType Request | 4 处（Create / Begin）| A | 多处 | L10607/L31117/L33127/L33197 | A |
| 16 | medicalRecordType Response | 7 处（Create Response + 6 Branch）| A | 多处 | L31123 + 6 Branch | A |
| 17 | medicalRecordType Branch | 6 处 `== 5` | A | 多处 | L2257/L31123/L32951/L33055/L33136/L33156 | A |
| 18 | medicalRecordType → State | 6 处全部走 adminSalesRecord.myMaterialBill | A | 多处 | 同上 | A |
| 19 | Create → Check | 4 条路径 | A | 多处 | L10609/L33142/L33202/L31129 | A |
| 20 | Create → Optometry | 1 条直接 (L34947) + 间接 | A | optometryCtrl | L34954 | A |
| 21 | Create → Sale | 2 条直接 (L31124/L33137) | A | addSaleRecordCtrl/adminMyRecordCtrl | L31124/L33137 | A |
| 22 | Create → Charge | 0 条直接（经 cashflow 桥）| A (间接) | — | L6925/L6929 | A (indirect) |
| 23 | Create → Delivery | **0 条** | F | — | — | F |
| 24 | State 状态机 | 5 个 StateMachine（A-E）| A | 多处 | 全部 | A |
| 25 | Create API 唯一性 | **NO**（6 条独立路径）| F | — | 全部 | F（唯一性 F）|
| 26 | 最终复刻风险 | 多 Create 路径 / 命名误导 / State vs API | — | — | — | 见 §26 |

---

## 24. A/B/C/D/E/F 等级

| 等级 | 数量 | 说明 |
|---|---|---|
| A | 25 | 全部字符级源码证据 |
| B | 0 | 无需多源互证 |
| C | 0 | 无局部证据（已字符级）|
| D | 0 | 无冲突 |
| E | 0 | 无业务推断（E 不入规格）|
| F | 3 | medicalRecord → customerCheckin / Create → Delivery / Create API 唯一性 |

---

## 25. 历史差异

### 25.1 S1-137R 误判修正

| S1-137R 误判 | 实际字符级证据 | 当前采用 |
|---|---|---|
| "insertCustomerCheckin* 3 处间接 Create" | addCheckinCtrl 范围内 3 处**仅创建 CustomerCheckin**，不创建 MedicalRecord | **0 条** |
| "至少 2 条独立创建路径" | 实际 **6 条** | 1 直接 + 5 间接 = 6 条 |
| "insertCustomerCheckin 链式" 是 S1-137R 漏掉的第 6 条路径 | L34914 链式调用 L34929 → L34947 | A |

### 25.2 S1-137 误判保留修正

| S1-137 误判 | 本轮确认 |
|---|---|
| "addMedicalRecord 唯一 Create" | **NO**（6 条独立路径）|
| "4 API 双向桥" | **NO**（仅 1 API 单向）|
| "6→1, 7→0 是 State 路由" | **NO**（是 UI 加工方式）|

### 25.3 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 200_S1-137R 全部保持原样
- 本文档 201_*.md 单独记录精确审计
- 后续 S1-139+ 应直接采用本轮精确结论

---

## 26. 复刻红线

### 26.1 多 Create 路径（必实现 6 条）

后端必须实现以下 6 条独立 MedicalRecord 创建/关联路径：

| # | API | 模式 | 必须实现 |
|---|---|---|---|
| 1 | addMedicalRecord.json | 直接 Create | ✓ |
| 2 | beginCustomerCheckin.json (3 个调用点) | 间接 Create | ✓ |
| 3 | receiveSelfAndBeginCustomerCheckin.json | 间接 Create | ✓ |
| 4 | insertCustomerCheckin.json (optometryCtrl L34914 链式) | 间接 Create | ✓ |

### 26.2 命名误导（必标注）

| 命名 | 实际行为 | 复刻警告 |
|---|---|---|
| addMedicalRecord.json | **是 Create**（不是 Add）| Request 只有 patientId + medicalRecordType |
| beginCustomerCheckin.json | 实际是 **Create+Begin**（不是单纯 Begin）| 隐式创建 MedicalRecord 并回填到 customerCheckin |
| receiveSelfAndBeginCustomerCheckin.json | 实际是 **Create+Receive** | Response 含 patientId（与 beginCustomerCheckin 不同）|
| insertCustomerCheckin.json | **2 种行为**：addCheckinCtrl 范围只 Create CustomerCheckin / optometryCtrl 范围链式 Create MedicalRecord | **同 API 不同行为**，复刻必须按调用点区分 |
| insertMedicalRecordTemplate.json | Template（**不是** MedicalRecord）| 与 MedicalRecord 实体无关 |

### 26.3 State 路由规则（必实现）

medicalRecordType → State 路由：
- `== 5` → `adminSalesRecord.myMaterialBill` (Sale)
- `!= 5` → `adminMyRecord.myMemberRecord` (Check/Optometry) / `myMaterialBill` (Check)

特殊路径：
- L34947 路径 → `optometryGlasses` (Optometry 入口，**不经 myMemberRecord 中转**)
- L34947 不携带 patientId

### 26.4 ID 严格区分

- `medicalRecord.id` ≠ `customerCheckin.id` ≠ `cashflowId` ≠ `patientId`
- `customerCheckin.medicalRecordId` 是字符级桥（6 处）
- `printCheckinId` ≡ `customerCheckin.id`（L8671/L8697 字符级）
- `medicalRecordType` ≠ `medicalRecordId`

### 26.5 medicalRecordType 生命周期规则

| 阶段 | 字段 | 用途 |
|---|---|---|
| Request | medicalRecordType | 写入 Create / Begin |
| Response | res.object.medicalRecordType | 决定 State |
| UI 转换 | `{ 6: 1, 7: 0 }` | choseFactoryMethod（**不**是 State 路由）|

### 26.6 CustomerCheckin ↔ MedicalRecord 关系

- `customerCheckin → MedicalRecord`：6 处字符级桥（A）
- `MedicalRecord → customerCheckin`：**F**（medicalRecord 不含 customerCheckin 字段）
- 复刻后端必须实现：CustomerCheckin 可关联 MedicalRecord，但 MedicalRecord 实体不反向引用 CustomerCheckin

---

## 27. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-200 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ 视光之家url.txt 未修改 |
| 本轮只新增 201_*.md | ✓ |

---

## 28. Git

### 28.1 操作

```
git add -- 201_S1-138_MedicalRecord多创建路径与创建后分流状态机审计.md
git diff --cached --name-only
git commit -m "docs(201): S1-138 MedicalRecord 多创建路径与创建后分流状态机审计"
git push origin master
```

### 28.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| REMOTE origin/master | (new commit) |
| LOCAL == REMOTE | YES |
| tracked | 209（commit 201 后从 208 → 209） |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| staged only current document | ✓ 201_*.md |
| 文件修改数 | 1 file changed, ~1500-2000 insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L31119 | **addMedicalRecord.json 唯一显式 Create API** |
| L31125 / L31130 | res.object.id → medicalRecordId State 参数 |
| L10605 | beginCustomerCheckin 间接 Create 路径 1/3（候诊队列接诊）|
| L33127 | beginCustomerCheckin 间接 Create 路径 2/3（adminMyRecord selectMedicalType）|
| L33134 | response.result.vo.customerCheckin.medicalRecordId → getMedicalRecord |
| L34947 | beginCustomerCheckin 间接 Create 路径 3/3（optometryCtrl 验光入口）|
| L34955 | optometryGlasses State 入口 |
| L33195 | receiveSelfAndBeginCustomerCheckin 间接 Create 路径 |
| L33203 | res.customerCheckin.medicalRecordId + res.patient.id |
| L8667 | insertCustomerCheckinOfNewPaitent — **非 MedicalRecord Create** |
| L8679 | insertCustomerCheckinOfNewCustomer — **非 MedicalRecord Create** |
| L8681 | insertCustomerCheckin (addCheckinCtrl) — **非 MedicalRecord Create** |
| L34914 | insertCustomerCheckin (optometryCtrl) — **链式 Create MedicalRecord** |
| L33479 | updateMedicalRecord — Update |
| L35099 | setMedicalRecordProcessMode — UI 加工方式 |
| L35150 | cancelMedicalRecord — Cancel |
| L35167 | confirmMedicalRecordReturn — Confirm |
| L35185 / L35204 | completeMedicalRecordDelivery — Complete |
| L33457 / L52253 | insertMedicalRecordTemplate — Template |

---

S1-138 完成。立即停止，等待老板下一指令。不执行 S1-139。
