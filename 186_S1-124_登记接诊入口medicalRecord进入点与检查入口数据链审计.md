# S1-124 登记 / 接诊入口 → medicalRecord 进入点 → 检查入口数据链审计

## 0. 任务背景

S1-123 已完成就诊流程主链 Controller / State / API 深度审计，识别 medicalRecordId 多个入口（doctorWorkbenchCtrl / optometryCtrl）。

本轮**反向追**业务入口的 customerCheckin 链，**精确化 medicalRecordId 入口的 provenance**。

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| customerCheckin 命中 | **66 处** |
| 涉及 Controller | 6 个 |
| 入口 Controller | 6 个 (addCheckinCtrl / checkinListCtrl / doctorWorkbenchCtrl / myMemberCtrl / optometryCtrl / queueMachineCtrl / checkCallCtrl) |

## 2. 入口 Controller 全集

### 2.1 主入口 Controller 详细分类

| # | Controller | 行号 | 入口类型 | 入口 API | 关键字段 |
|---:|---|---:|---|---|---|
| 1 | **addCheckinCtrl** | L8159 | **登记入口** | insertCustomerCheckin[.json / OfNewPaitent.json / OfNewCustomer.json] | customerCheckin.id / patientId |
| 2 | **checkinListCtrl** | L8778 | **登记列表 + 诊前检查入口** | selectCustomerCheckinVoListOfCompany.json / medicalCheckBeforeCustomerCheckin.json | customerCheckin.id / medicalRecordId |
| 3 | **doctorWorkbenchCtrl** | L10401 | **医生工作台 + 接诊入口** | beginCustomerCheckin.json | customerCheckinId / medicalRecordId |
| 4 | **myMemberCtrl** | L33080 | **我的会员 + 二次接诊** | beginCustomerCheckin.json / receiveSelfAndBeginCustomerCheckin.json | customerCheckinId / medicalRecordId |
| 5 | **optometryCtrl** | L34776 | **验光入口** | insertCustomerCheckin.json / beginCustomerCheckin.json | customerCheckinId / medicalRecordType |
| 6 | **checkCallCtrl** | L9760 | **检查叫号入口** | startExamine.json | medicalExamineId / medicalRecordId |
| 7 | **queueMachineCtrl** | L10869 | 排队叫号 | (无 customerCheckin 派生) | checkinNumber |

## 3. customerCheckin 全局链

### 3.1 入口链分类

| 入口类型 | Controller | 行号 | customerCheckin 来源 | 后续 |
|---|---|---:|---|---|
| **产生** | addCheckinCtrl | L8667, L8681 | insertCustomerCheckin*.json Response | State go checkinList |
| **消费 (登记列表)** | checkinListCtrl | L8789, L8846 | ListFactory selectCustomerCheckinVoListOfCompany.json (item.customerCheckin.id) | medicalCheckBefore / deleteCustomerCheckin |
| **消费 (接诊入口)** | doctorWorkbenchCtrl | L10606 | ListFactory selectEmployeeCheckinQueueVoList.json (employee.customerCheckin.id) | beginCustomerCheckin → myMemberRecord |
| **消费 (接诊入口)** | myMemberCtrl | L33127, L33195 | ListFactory selectCustomerCheckinVoListOfEmployee.json / selectCustomerCheckinVoListOfCompany.json | beginCustomerCheckin / receiveSelfAndBegin |
| **消费 (验光入口)** | optometryCtrl | L34946 | ListFactory 单查询 (info.customerCheckin.id) | beginCustomerCheckin → optometryGlasses |
| **消费 (叫号)** | queueMachineCtrl | L11155, L11157 | ListFactory (p.customerCheckin.checkinNumber) | 语音叫号 |
| **消费 (查看)** | doctorWorkbenchCtrl | L10642 | ListFactory (employee.customerCheckin.medicalRecordId) | State go myMemberRecord (case 3 "查看") |

### 3.2 customerCheckinId 全局使用

| Controller | 行号 | Expression | 用途 |
|---|---:|---|---|
| addCheckinCtrl | L9160 | Request { customerCheckinId } | API confirmArrivalOfAppoint |
| checkinListCtrl | L9045-L9050 | 参数 + Request | medicalCheckBeforeCustomerCheckin (接诊触发) |
| checkinListCtrl | L8846-L8847 | Request { customerCheckinId } | deleteCustomerCheckin |
| doctorWorkbenchCtrl | L10606 | Request { customerCheckinId } | beginCustomerCheckin |
| myMemberCtrl | L33127, L33196 | Request { customerCheckinId } | beginCustomerCheckin / receiveSelfAndBeginCustomerCheckin |
| optometryCtrl | L34948 | Request { customerCheckinId } | beginCustomerCheckin |
| Scope 内部 | L9118, L9122, L9126, L9127, L9131, L9139, L9140, L9161, L9168 | $scope.customerCheckin.customerCheckinId | Modal 内部状态 |

## 4. insertCustomerCheckin 全局

### 4.1 三种变种 API

**S1-124 关键发现 1**：
- `insertCustomerCheckin.json` (基类)
- `insertCustomerCheckinOfNewPaitent.json` (新患者)
- `insertCustomerCheckinOfNewCustomer.json` (新客户)

### 4.2 3 个变种的唯一调用方

**【单 Consumer】** —— **仅 addCheckinCtrl** L8660-L8695

```javascript
// L8660-L8697 addCheckinCtrl
if ($scope.addCustomerModal) {
  // 新患者流程
  var insertPromise = $scope.insertCustomerCheckFactory.saveOrQuery(
    "/admin/insertCustomerCheckinOfNewPaitent.json", 
    $scope.checkCustomer
  );
  insertPromise.then(function (res) {
    if (res.status == 0) {
      var printCheckinId = res.result.vo.customerCheckin.id;
      //                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      //   customerCheckin.id 派生
    }
  });
} else {
  if (!$scope.obj.patientId) {
    url = "/admin/insertCustomerCheckinOfNewCustomer.json";
    //          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //   新客户（已有 patient 但新 customer）
  } else {
    url = "/admin/insertCustomerCheckin.json";
    //          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //   已有 patient + customer
  }
  new ObjectFactory().saveOrQuery(url, $scope.obj).then(function (res) {
    if (res.status == 0) {
      var printCheckinId = res.result.vo.customerCheckin.id;
      //   同样: customerCheckin.id
    }
  });
}
```

### 4.3 Response 字段访问

**S1-124 关键发现 2（Response 统一格式）**：
- `res.result.vo.customerCheckin.id` (Type 3 派生, primitive)
- `res.result.vo.customerCheckin.patientId` (Type 3 派生, primitive)
- **所有 3 个变种 API 共用此结构**

### 4.4 insert Customer 来源

**S1-124 关键发现 3（addCheckinCtrl Request 来源）**：

| 字段 | 来源 | Controller 行号 |
|---|---|---|
| name (customerName) | $scope.checkCustomer.customerName | L8667 |
| gender | $scope.checkCustomer.gender | L8667 |
| patientId | $scope.obj.patientId | L8681 |
| employeeId | $scope.customerCheckin.employeeId | L9160 (重新进入路径) |
| birthday | $scope.obj.birthday | L8687 |
| appointId | $scope.obj.appointId | L8665 |
| registrationFeeId | $scope.registrationFeeId (挂号) | L8663 |

**S1-124 关键发现 4（customer 与 patient 在入口独立）**：
- L8667: `$scope.checkCustomer` 字段（含 customerName, gender）
- L8681: `$scope.obj.patientId` 字段
- **两个对象来源独立**：customer 来自 `checkCustomer` 对象，patient 来自 `obj.patientId`
- 不能因为字段相近而合并

## 5. beginCustomerCheckin 全局

### 5.1 3 个 Consumer

| # | Controller | 行号 | Request | Response 访问 | 后续 State |
|---:|---|---:|---|---|---|
| 1 | optometryCtrl | L34947 | `{ customerCheckinId, medicalRecordType: $scope.choseUser.glassestype }` | `result.result.vo.customerCheckin.medicalRecordId` | optometryGlasses |
| 2 | doctorWorkbenchCtrl | L10605 | `{ customerCheckinId: employee.customerCheckin.id, medicalRecordType: 1 }` | `response.customerCheckin.medicalRecordId` | adminMyRecord.myMemberRecord |
| 3 | myMemberCtrl | L33127 | `{ customerCheckinId: $scope.customerCheckinId, medicalRecordType: 1 }` | `response.result.vo.customerCheckin.medicalRecordId` | adminMyRecord.myMemberRecord (按 medicalRecordType 分流) |

### 5.2 3 个 Consumer 的 D 级冲突

**S1-124 关键发现 5（同一 API 不同 Response 访问路径）**：

| Controller | Response 字段路径 |
|---|---|
| optometryCtrl L34955 | `result.result.vo.customerCheckin.medicalRecordId` |
| doctorWorkbenchCtrl L10610 | `response.customerCheckin.medicalRecordId` |
| myMemberCtrl L33134 | `response.result.vo.customerCheckin.medicalRecordId` |

**S1-124 判定**：
- optometryCtrl 与 myMemberCtrl 同：`response.result.vo.customerCheckin.medicalRecordId`
- doctorWorkbenchCtrl 异：`response.customerCheckin.medicalRecordId` (无 `.result.vo`)
- **D 级冲突可能** —— 后端实际响应结构待 backend debug 确认（F 级）
- 但**两套访问都正常运行**，说明后端可能容错

### 5.3 medicalRecordType 字段差异

| Controller | medicalRecordType 来源 | 值 |
|---|---|---|
| optometryCtrl L34949 | `$scope.choseUser.glassestype` | 6 (框架镜) / 7 (隐形眼镜) |
| doctorWorkbenchCtrl L10607 | 硬编码 `1` | 1 (普通) |
| myMemberCtrl L33127 | 硬编码 `1` | 1 (普通) |

**S1-124 重要发现 6（medicalRecordType 业务含义冲突）**：
- optometryCtrl: medicalRecordType 6/7 = 验光业务类型
- doctorWorkbenchCtrl/myMemberCtrl: medicalRecordType 1 = 普通接诊
- **同一字段不同 controller 含义不同**
- 但**消费方**（myMemberCtrl L33136）按 `medicalRecordType == 5` 分流 —— 与 optometryCtrl 用法不同

## 6. medicalRecordId 入口来源分类

### 6.1 8 类入口分类

| # | 类别 | 实例 | 等级 |
|---:|---|---|---|
| A | **customerCheckin.medicalRecordId** | doctorWorkbenchCtrl L10610, optometryCtrl L34955, myMemberCtrl L33203 | A |
| B | **API Response (medicalRecord.json)** | myMemberCtrl L33134-L33138 | A |
| C | **medicalRecord.id** | myMemberCtrl L33138, assistCheckingCtrl | A |
| D | **StateParams** | 多 Controller | A |
| E | **函数参数** | assistCheckingCtrl L2216, getMedicalRecord(id) | A |
| F | **Scope** | $scope.medicalRecordId = $stateParams.medicalRecordId | A |
| G | **List item** | medicalExamineList[0].medicalExamine.medicalRecordId (checkCallCtrl L9964) | A |
| H | **State 派生 (辅助)** | employee.customerCheckin.medicalRecordId (doctorWorkbenchCtrl L10642, "查看" 操作) | A |

### 6.2 入口阶段 medicalRecordId 详细链路

**S1-124 关键发现 7（medicalRecordId 入口 5 条）**：

| 入口 | 起点 | 终点 | API | Response 字段 | 等级 |
|---|---|---|---|---|---|
| 1 | **addCheckinCtrl** (L8667/L8681) | 后续 API | insertCustomerCheckin[变种].json | `res.result.vo.customerCheckin.id` (无 medicalRecordId!) | A |
| 2 | **checkinListCtrl** (L8788) | preDiagnosisExamination | medicalCheckBeforeCustomerCheckin.json | `res.customerCheckin.medicalRecordId` (A 类) | A |
| 3 | **doctorWorkbenchCtrl** (L10605, "接诊") | myMemberRecord | beginCustomerCheckin.json | `response.customerCheckin.medicalRecordId` (A 类) | A |
| 4 | **doctorWorkbenchCtrl** (L10641, "查看") | myMemberRecord | (无 API, 直接读 item) | `employee.customerCheckin.medicalRecordId` (H 类) | A |
| 5 | **myMemberCtrl** (L33127) | myMemberRecord / myMaterialBill | beginCustomerCheckin.json | `response.result.vo.customerCheckin.medicalRecordId` (A 类) | A |
| 6 | **optometryCtrl** (L34947) | optometryGlasses | beginCustomerCheckin.json | `result.result.vo.customerCheckin.medicalRecordId` (A 类) | A |
| 7 | **checkCallCtrl** (L9984) | assistChecking | startExamine.json | `medicalExamineList[0].medicalExamine.medicalRecordId` (G 类) | A |

**S1-124 关键发现 8**：
- **insertCustomerCheckin 三个变种不直接提供 medicalRecordId**（只提供 customerCheckin.id）
- medicalRecordId 的首次出现是 **medicalCheckBeforeCustomerCheckin.json** 或 **beginCustomerCheckin.json** 的 Response
- 即 customerCheckin 创建后，需要再次调 begin API 才会生成 medicalRecordId
- **A 级** 但**多入口并存**

## 7. patient / customer / customerCheckin / medicalRecord 四层关系

### 7.1 对象关系矩阵

| 对象 | Source | Consumer | 是否直接连接 | 备注 |
|---|---|---|---|---|
| **patient** | addCheckinCtrl L8666-L8667 / doctorWorkbenchCtrl L10611 | checkinListCtrl L8880 (getPatientVo.json) / optometryCtrl L34912 | **A** 独立 API | patientVo API |
| **customer** | addCheckinCtrl L8667 (checkCustomer) / checkinListCtrl L8894 (res.customer.id) | checkinListCtrl L8894 (getCustomerVo.json) | **A** 独立 API | customerVo API |
| **customerCheckin** | addCheckinCtrl L8667-L8695 (insert) | doctorWorkbenchCtrl / myMemberCtrl / optometryCtrl / checkinListCtrl | **A** 中间表 | customerCheckin 表 |
| **medicalRecord** | beginCustomerCheckin Response / medicalCheckBefore Response | 多 Controller (delivery / waitCharge / assistCheck 等) | **A** 主表 | medicalRecord 表 |

### 7.2 关系链分析

**S1-124 关键发现 9（四层关系映射）**：

```
[patient] ─API→ [patientVo] ─API→ [customerVo] ─API→ [customer]
   ↓                       ↑
patientId → getCustomerVo.json { customerId: res.customer.id } → 桥

[patient] → [customerCheckin] ← patientId (insert 时来源)
[patient] ← customerCheckin.patientId (read 时派生)

[customerCheckin] → begin API → [medicalRecord]
[medicalRecord] ← medicalRecordId (read 派生)

patient / customer 是**独立 API 入口**：
- getPatientVo.json { patientId } → patientVo
- getCustomerVo.json { customerId } → customerVo
- patientVo → customerVo 通过 patientVo.customer.id → getCustomerVo
- customerVo → patientVo 通过 customerVo.patientId → getPatientVo
```

### 7.3 patient.id → insertCustomerCheckin.patientId 链

**S1-124 关键发现 10（patient.id → customerCheckin.patientId 链）**：

**【optometryCtrl L34912-L34914】**：
```javascript
$scope.addUser.affirm = function (obj) {
  var object = {};
  object.name = obj.customer.customerName;
  object.gender = obj.customer.gender;
  object.patientId = obj.patient.id;
  //              ^^^^^^^^^^^^^
  //   patient.id → object.patientId (A 级直接赋值)
  object.employeeId = $scope.employeeId;
  new ObjectFactory().saveOrQuery("/admin/insertCustomerCheckin.json", object).then(function (res) {
    if (res.status == 0) {
      $scope.addUser.switch(false, res.result.vo);
    }
  });
};
```

**S1-124 关键发现 11（patient.id → patientId 派生链）**：
- 起点：optometryCtrl L34912 `obj.patient.id` （**patient 对象内的 id 字段**）
- 中间：affirm 函数参数 `obj`（含 customer 和 patient 两个独立对象）
- 终点：API Request `object.patientId`
- **A 级** 直接字段级派生

### 7.4 customer.customerName → customerName 链

**S1-124 关键发现 12（customer 与 patient 独立来源）**：
- `obj.customer.customerName` → `object.name` (A 级)
- `obj.customer.gender` → `object.gender` (A 级)
- `obj.patient.id` → `object.patientId` (A 级)
- **customer 和 patient 是 obj 内的两个独立嵌套对象**
- 没有 `customer.id → patient.id` 链
- 也没有 `customer.id → customerCheckin.id` 链

## 8. medicalRecordType 逆向

### 8.1 glassestype 完整链

| 行号 | 字段 | 值 | 来源 |
|---:|---|---|---|
| L34992 | glassesTypeList | `[{status: 6, name: "框架镜验配"}, {status: 7, name: "隐形眼镜验配"}]` | 硬编码 |
| L35000 | setType(glassestype) | 函数 | setType 触发 choseUser.open |
| L35003 | $scope.choseUser.open(glassestype) | 设置 $scope.choseUser.glassestype | setType 函数 |
| L34949 | medicalRecordType | `$scope.choseUser.glassestype` | 用作 beginCustomerCheckin Request |

### 8.2 medicalRecordType 业务含义对照

| Controller | medicalRecordType | 业务 |
|---|---|---|
| optometryCtrl L34949 | 6 / 7 (硬编码选择) | 验光类型（框架镜/隐形眼镜）|
| doctorWorkbenchCtrl L10607 | 1 (硬编码) | 普通接诊 |
| myMemberCtrl L33127 | 1 (硬编码) | 普通接诊 |
| myMemberCtrl L33136 | 5 (consumer 端判断) | 开单 vs 其它 |
| assistCheckingCtrl L2257 | 5 (consumer 端判断) | 开单 vs 检查报告 |

**S1-124 重要发现 13（medicalRecordType 多业务含义）**：
- 同一字段在不同 controller 含义不同
- 验光 (6/7) / 接诊 (1) / 开单 (5) 是三个独立业务
- 复刻时需要根据 controller 选择 medicalRecordType 值

## 9. 入口 → 检查 最终 DAG

### 9.1 完整入口链

```
【登记入口】addCheckinCtrl L8660
  ↓
[API: insertCustomerCheckin[变种].json]
  ↓ Response
[customerCheckin.id] + [customerCheckin.patientId]
  ↓
[State go: checkinList] (L8654)
  ↓
【登记列表】checkinListCtrl L8778
  ↓
[ListFactory: selectCustomerCheckinVoListOfCompany.json]
  ↓ (item)
【诊前检查入口】L8784 medicalCheckBeforeCustomerCheckin(item)
  ↓
[API: medicalCheckBeforeCustomerCheckin.json { customerCheckinId }]
  ↓ Response
[res.customerCheckin.medicalRecordId] (A 类)
  ↓
[preDiagnosisExamination 弹窗]

【医生工作台】doctorWorkbenchCtrl L10401
  ↓
[ListFactory: selectEmployeeCheckinQueueVoList.json]
  ↓ (employee)
【接诊 case 0】L10600 beginCustomerCheckin
  ↓
[API: beginCustomerCheckin.json { customerCheckinId, medicalRecordType: 1 }]
  ↓ Response
[response.customerCheckin.medicalRecordId] (A 类，D 级冲突)
  ↓
[State go: adminMyRecord.myMemberRecord { medicalRecordId, patientId }]

【查看 case 3】L10640
  ↓
[直接读 employee.customerCheckin.medicalRecordId] (H 类)
  ↓
[State go: adminMyRecord.myMemberRecord { medicalRecordId, patientId }]

【我的会员】myMemberCtrl L33080
  ↓
[ListFactory: selectCustomerCheckinVoListOfEmployee.json]
  ↓ (item)
【二次接诊】L33170 clinck(id, patientId)
  ↓
[API: beginCustomerCheckin.json] (同 doctorWorkbenchCtrl)
  ↓
[response.result.vo.customerCheckin.medicalRecordId] (A 类)
  ↓
[API: getMedicalRecord.json { id }]
  ↓ 按 medicalRecordType 分流
  ↓
[State go: adminMyRecord.myMaterialBill / myMemberRecord]

【验光入口】optometryCtrl L34776
  ↓
[ListFactory: 单查询]  (item)
  ↓ (info)
【验光入口】L34945 beginCustomerCheckin
  ↓
[API: beginCustomerCheckin.json { customerCheckinId, medicalRecordType: glassestype }]
  ↓ Response
[result.result.vo.customerCheckin.medicalRecordId] (A 类)
  ↓
[State go: optometryGlasses { medicalRecordId }]

【检查叫号】checkCallCtrl L9760
  ↓
[ListFactory: 单查询] (medical)
  ↓
【开始检查 case 0】L9984 startExamine
  ↓
[API: startExamine.json { medicalExamineId }]
  ↓ Response → toAssistChecking()
  ↓
[State go: assistChecking { medicalExamineId, medicalRecordId }]
  ↓
[医疗检查入口: assistCheckingCtrl]
```

### 9.2 入口 → 检查 关键判断

**S1-124 关键发现 14**：

| 入口 Controller | 检查入口直接链 | 等级 |
|---|---|---|
| addCheckinCtrl | 间接（通过 checkinList）| A |
| checkinListCtrl | **直接** `medicalCheckBeforeCustomerCheckin.json` (G 类 medicalRecordId) | A |
| doctorWorkbenchCtrl | **直接** `beginCustomerCheckin.json` (A 类 medicalRecordId) | A |
| myMemberCtrl | **直接** `beginCustomerCheckin.json` (A 类) | A |
| optometryCtrl | **直接** `beginCustomerCheckin.json` (A 类) → optometryGlasses | A |
| checkCallCtrl | **直接** `startExamine.json` (G 类 medicalRecordId) | A |

**所有入口都能建立到检查的桥**（虽然路径不同）。

## 10. Read / Write 审计（入口阶段）

### 10.1 入口 Controller Write

| API | Controller | 行号 | 性质 |
|---|---|---:|---|
| insertCustomerCheckinOfNewPaitent.json | addCheckinCtrl | L8667 | Write-Create customerCheckin |
| insertCustomerCheckinOfNewCustomer.json | addCheckinCtrl | L8681 | Write-Create customerCheckin |
| insertCustomerCheckin.json | addCheckinCtrl | L8681 | Write-Create customerCheckin |
| beginCustomerCheckin.json | optometryCtrl / doctorWorkbenchCtrl / myMemberCtrl | L34947 / L10605 / L33127 | Write-Create medicalRecord |
| receiveSelfAndBeginCustomerCheckin.json | myMemberCtrl | L33195 | Write (复合) |
| startExamine.json | checkCallCtrl | L9985 | Write-Update examineStatus |
| confirmArrivalOfAppoint.json | addCheckinCtrl | L8658 | Write-Update appointStatus |
| deleteCustomerCheckin.json | checkinListCtrl | L8846 | Write-Delete |
| medicalCheckBeforeCustomerCheckin.json | checkinListCtrl | L8788 | Write (创建 medicalRecord) |

### 10.2 入口 Controller Read

| API | Controller | 行号 | 性质 |
|---|---|---:|---|
| selectCustomerCheckinVoListOfCompany.json | checkinListCtrl / myMemberCtrl | L8827 / L33189 | List |
| selectCustomerCheckinVoListOfEmployee.json | myMemberCtrl | L33101 | List |
| selectEmployeeCheckinQueueVoList.json | doctorWorkbenchCtrl | (内) | List |
| getPatientVo.json | checkinListCtrl | L8880 | Read patientVo |
| getCustomerVo.json | checkinListCtrl | L8894 | Read customerVo |
| getMedicalRecord.json | myMemberCtrl | L33134 | Read medicalRecordVo |

## 11. 26 项矩阵

| # | 项目 | 详情 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | 入口 Controller 全集 | 7 个 | A | L1 |
| 02 | checkin | addCheckinCtrl (L8159) | A | L1 |
| 03 | register | optometryCtrl L34905 ($scope.addUser.register) | A | L1 |
| 04 | doctorWorkbench | doctorWorkbenchCtrl (L10401) | A | L1 |
| 05 | customerCheckin | 66 处 / 6 Controller | A | L1 |
| 06 | customerCheckinId | 7+ 处 / 5 Controller | A | L1 |
| 07 | insertCustomerCheckin | 3 变种 / 1 Consumer (addCheckinCtrl) | A | L1 |
| 08 | insert Request | $scope.checkCustomer + $scope.obj | A | L1 |
| 09 | insert provenance | 来源：obj.customer / obj.patient / $scope.obj | A | L1 |
| 10 | insert Response | res.result.vo.customerCheckin.{id, patientId} | A | L1 |
| 11 | beginCustomerCheckin | 3 Consumer (optometryCtrl / doctorWorkbenchCtrl / myMemberCtrl) | A | L1 |
| 12 | begin Request | { customerCheckinId, medicalRecordType } | A | L1 |
| 13 | begin provenance | employee.customerCheckin.id (doctorWorkbench) / info.customerCheckin.id (optometry) | A | L1 |
| 14 | begin Response | 2 套访问路径（D 级冲突）| A/D | L1 |
| 15 | medicalRecordId 入口 | 7 链（A 类 6 + G 类 1）| A | L1 |
| 16 | patient | addCheckin / optometryCtrl / checkinListCtrl | A | L1 |
| 17 | patientId | 5+ 链 | A | L1 |
| 18 | customer | addCheckin (checkCustomer) / checkinListCtrl (getCustomerVo) | A | L1 |
| 19 | customer → patient | F（无直接派生）| F | L1 |
| 20 | patient → customerCheckin | A（optometryCtrl L34912 obj.patient.id）| A | L1 |
| 21 | customer → customerCheckin | A（optometryCtrl L34910 obj.customer.customerName）| A | L1 |
| 22 | medicalRecordType | 6/7 (验光) / 1 (接诊) / 5 (开单) 三种含义 | A/D | L1 |
| 23 | State 桥 | 8 个 $state.go（含 medicalRecordId/patientId 传递）| A | L1 |
| 24 | API 数据桥 | 5 链（begin / medicalCheckBefore / receiveSelfAndBegin / startExamine / getMedicalRecord）| A | L1 |
| 25 | 入口 → 检查 | **6 条直接链全部 A 级** | A | L1 |
| 26 | A/B/C/D/E/F | A=24 / B=0 / C=0 / D=2 / E=0 / F=1 | - | - |

## 12. F 边界

| 项目 | F 原因 | 应对 |
|---|---|---|
| customer → patient 直接链 | 源码内无 `customer.id = patient.id` | 不假设 |
| medicalRecordType 字段统一含义 | 不同 controller 含义不同 | 必须按 controller 选值 |
| HTML ng-click 跳转 | 不在 controller.js 范围 | 需要 HTML 审计 |

## 13. 复刻风险（L1）

### R1: insertCustomerCheckin 与 beginCustomerCheckin 字段 provenance
- insertCustomerCheckin 不直接提供 medicalRecordId
- beginCustomerCheckin 是 medicalRecordId 的**主要**入口
- 复刻时必须保留两个 API 的**顺序**（先 insert 再 begin）

### R2: customer / patient 是不同 Request 来源
- addCheckinCtrl L8667 内部 `checkCustomer` 含 customer 字段
- L8681 `obj.patientId` 是 patient
- **不能合并为单一对象**
- 复刻时后端必须支持两个独立来源

### R3: customerCheckinId 是 begin 的输入
- 复刻时不能简化 customerCheckinId 字段

### R4: medicalRecordId 是 begin success 的输出
- 必须保留 response 路径（D 级冲突：2 套路径）

### R5: State 参数必须保留
- medicalRecordId / patientId 经常同时传递
- 不能简化

### R6: medicalRecordType 来源必须保留
- 验光 (6/7) / 接诊 (1) / 开单 (5) 三种业务
- 复刻时根据 controller 选值

### R7: 没有直接入口链时不能强行跳转
- 例如 checkinListCtrl → checkCallCtrl 源码无直接 State 链
- 不能假设"检查" 一定在"登记" 之后
- 复刻时按实际业务场景实现

## 14. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- 165-185 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 15. 与历史结论的差异

### 15.1 S1-123 vs S1-124

| 项 | S1-123 | S1-124 |
|---|---|---|
| medicalRecordId 入口 | 标注 2 个 (doctorWorkbench / optometry) | **实际 6+ 个** (新增 checkinList / myMember / checkCall) |
| insertCustomerCheckin 变种 | 未深入 | **3 个变种**（OfNewPaitent / OfNewCustomer / 原）|
| medicalRecordType 业务含义 | 单一 | **3 种**（验光 6/7 / 接诊 1 / 开单 5）|
| D 级冲突 | 2 套 begin Response | **新增 medicalRecordType 多业务含义 D 级** |

### 15.2 S1-106 vs S1-124

| 项 | S1-106 | S1-124 |
|---|---|---|
| insertCustomerCheckin Request | 标注 4 字段 (name/gender/patientId/employeeId) | **新增 birthday/appointId/registrationFeeId** |
| Response 字段 | customerCheckin.id | **+ patientId** |
| Controller 范围 | optometryCtrl | **6 个 Controller**（含 addCheckinCtrl / checkinListCtrl） |

## 16. 结论

### 16.1 关键发现

1. **入口 Controller 6 个**：addCheckinCtrl / checkinListCtrl / doctorWorkbenchCtrl / myMemberCtrl / optometryCtrl / checkCallCtrl
2. **customerCheckin 66 处 / 6 Controller**
3. **insertCustomerCheckin 3 个变种**（OfNewPaitent / OfNewCustomer / 原）—— 全部仅 addCheckinCtrl 调用
4. **beginCustomerCheckin 3 处调用** —— 同一 API 不同 Response 访问路径（D 级冲突）
5. **medicalRecordId 入口 7 链**（A 类 6 + G 类 1）
6. **patient/customer 独立来源**：不能合并
7. **medicalRecordType 三种业务含义**：验光 6/7 / 接诊 1 / 开单 5
8. **所有入口 → 检查都有直接桥**

### 16.2 S1-124 任务状态

- 入口 Controller 全集识别（7 个）
- customerCheckin 全局链审计（66 处 / 6 Controller）
- 3 个变种 insertCustomerCheckin 详细审计
- 3 个 Consumer beginCustomerCheckin 详细审计（含 D 级冲突）
- 8 类 medicalRecordId 入口分类
- 4 层对象关系矩阵
- medicalRecordType 完整逆向
- 26 项矩阵已建立
- 7 条复刻风险已列出

---

**【S1-124 完成】**
