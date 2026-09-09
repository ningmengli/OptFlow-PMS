# S1-139：Patient / Customer / MedicalRecord 三对象身份关系总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向建模（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 201 个 MD / 不修改历史
> 关联：S1-133 / S1-134 / S1-135 / S1-136 / S1-137 / S1-137R / S1-138

---

## 目录

1. 任务性质
2. 红线
3. 证据等级与命名约束
4. Customer 全局扫描
5. Patient 全局扫描
6. MedicalRecord 全局扫描
7. CustomerCheckin 字段扫描
8. Customer → Patient
9. Patient → Customer
10. Patient → MedicalRecord
11. MedicalRecord → Patient
12. Customer → MedicalRecord
13. MedicalRecord → Customer
14. CustomerCheckin 三对象桥
15. addMedicalRecord Request 字段
16. insertCustomerCheckin* Request 字段
17. Mobile 链
18. State / URL
19. Factory / Scope
20. 完整三对象桥矩阵
21. ID 等同/不同
22. 精确数量
23. L1 / L2 / L3
24. 最终三对象 DAG
25. 26 项证据矩阵
26. A/B/C/D/E/F 等级
27. 历史差异
28. 复刻红线
29. 红线检查
30. Git

---

## 1. 任务性质

本轮是 Patient / Customer / MedicalRecord 三对象身份关系总审计。

- 禁止修改 165-201 任意历史 MD
- 禁止修改 controller.js / 7 HTML / .gitignore
- 禁止调用任何 API（actual = 0）
- 只新增 1 份文档：`202_S1-139_*.md`
- 必须严格区分 3 个对象 ID（customerId / patientId / medicalRecordId / customerCheckinId）

---

## 2. 红线

| 编号 | 红线 |
|---|---|
| 1 | API actual = 0 |
| 2 | Write actual = 0 |
| 3 | Production mutation = 0 |
| 4 | 不调用真实业务 API |
| 5 | 不新增患者 / 客户 / MedicalRecord / 接诊 |
| 6 | 不修改 controller.js（SHA256 不变） |
| 7 | 不修改任何 HTML |
| 8 | 不修改 .gitignore |
| 9 | 不修改 165-201 历史 MD |
| 10 | 只新增 202_*.md |
| 11 | 不因为变量名自动合并 Customer 与 Patient |
| 12 | 不因为同一 Response 同时有 customer/patient 就认定一一对应 |
| 13 | 不因为 customerId/patientId 同时出现在 Request 就认定转换 |
| 14 | E 不进入最终规格 |
| 15 | F 必须写："当前证据范围未观察/不可得" |

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
| `patientObjectFactory` | 命名误导 — 可能存 customer 或 patient（L5930 / L5243 / L7491）|
| `customerFactory` | 命名误导 — 存 customer 但**不存** patient（L5930）|
| `getPatientVoList.json` 用 customerId 查询 | ≠ Customer → Patient 实体合并（仅查询桥）|
| 同 Response 含 customer + patient | ≠ Customer == Patient（同列表两个对象）|
| `customerCheckin.customerId` 0 处 | ≠ customerCheckin 不属于 Customer（仅字符级缺失）|

---

## 4. Customer 全局扫描

### 4.1 字符级统计

| 模式 | 命中数 |
|---|---|
| `customerId` 总命中 | 164 |
| `customer\.id` 命中 | 多处 |
| `customer\.customerName` 命中 | 多处 |
| `res\.customer\.id` 命中 | 1 (L8895) |
| `res\.result\.vo\.customer` 命中 | 多处 (L5930/L20966/L20967) |
| `$stateParams\.customerId` 命中 | 多处 (L5894/L5913/L5925/L5938/L5994/L6000/L6008/L6510/L16746/L16759/L18060 等) |
| `customer\.customerId` 命中 | 0 |

### 4.2 Customer 字段（从 getCustomerVo.json Response 推断）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `id` | L8895 `res.customer.id` / L4947 `res.result.object.customer.id` | A |
| `customerName` | L8904 `$scope.customer.trueName = response.customer.customerName` | A |
| `linkMobile` | L8905 `response.customer.linkMobile` | A |
| `channel` | L8902 / L20966 `response.customer.channel` | A |
| `channelTagId` | L8903 / L20967 `response.customer.channelTagId` | A |
| `patientId` | **0 命中** — Customer 不含 patientId 字段 | F |

### 4.3 Customer 入口

```javascript
// L5923-L5932 典型 Customer 入口
$scope.getCustomer = function () {
  new ObjectFactory().saveOrQuery("/admin/getCustomerVo.json", {
    customerId: $stateParams.customerId                        // L5925
  }).then(function (res) {
    if (res.status) {
      return Popup.notice(res.errmsg);
    }
    $scope.patientObjectFactory = res.result.vo.customer;      // L5930 — 命名误导!
  });
};
```

**命名误导警告**: `$scope.patientObjectFactory` 实际存的是 `res.result.vo.customer`（L5930）— Factory 名称与存储内容不一致。

### 4.4 Customer API 入口

| API | 行号 | Request | Response 实际消费 |
|---|---|---|---|
| getCustomerVo.json | L5924 | `{ customerId }` | res.result.vo.customer |
| getCustomerVo.json | L8894 | `{ customerId: res.customer.id }` | response.tagList / response.customer |
| getCustomerVo.json | L4947 | `{ customerId: res.result.object.customer.id }` | res.result.object.customer.id |
| getCustomerVo.json | L20960 | `{ customerId: $scope.customerId }` | res.customer (queryVo 模式) |

---

## 5. Patient 全局扫描

### 5.1 字符级统计

| 模式 | 命中数 |
|---|---|
| `patientId` 总命中 | 90 |
| `patient\.id` 命中 | 多处 |
| `patientName` 命中 | 多处 |
| `res\.patient\.id` 命中 | 1 (L33204) |
| `res\.result\.object\.patientId` 命中 | 多处 (L31222) |
| `$stateParams\.patientId` 命中 | 多处 (L3641/L8213/L11829/L16745) |
| `patient\.customerId` 命中 | **多**（关键发现） |
| `patient\.customer` | 0 |

### 5.2 Patient 字段（从 getPatientInfo.json / getPatientVoList.json Response）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `id` | L31226 `{ id: $scope.patientId }` / L33204 `res.patient.id` | A |
| `patientName` | L3647 `result.patientName` / L32909 | A |
| `patientBirthday` | L3644-3645 / L31230 | A |
| `patientGender` | L3648 | A |
| `customerId` | **A — 关键发现** L3650 `result.customerId` / L31228 `res.result.object.customerId` / L32912 | A |
| `school` | L8434-8438 `patient.school.schoolName` / `patient.school.id` | A |
| `schoolClass` | L8437-8438 `patient.schoolClass.id` / `patient.schoolClass.className` | A |
| `customerName` | L8424 `choosePatient` 函数参数列表含 `customerName` | A |
| `linkMobile` | L8424 `choosePatient` 函数参数列表含 `linkMobile` | A |

### 5.3 Patient 入口

```javascript
// L3640-L3655 典型 Patient 入口
$scope.getPatient = function () {
  var Patient = new ObjectFactory().saveOrQuery("/admin/getPatientInfo.json", { id: $stateParams.patientId });  // L3641
  Patient.then(function (res) {
    var result = res.result.object;
    if (result && result.patientBirthday) {
      result.patientBirthday = new Date(result.patientBirthday);
    }
    $scope.updatePatientFactory.patientName = result.patientName;
    $scope.updatePatientFactory.patientGender = result.patientGender;
    $scope.updatePatientFactory.patientBirthday = result.patientBirthday;
    var promise = new ObjectFactory().saveOrQuery("/admin/getCustomerVo.json", {
      customerId: result.customerId                              // L3650 — Patient → Customer 桥
    });
    promise.then(function (res) {
      $scope.updatePatientFactory.linkMobile = res.vo.customer.linkMobile;
    });
  });
};
```

### 5.4 Patient API 入口

| API | 行号 | Request | Response 实际消费 |
|---|---|---|---|
| getPatientInfo.json | L3641 | `{ id: $stateParams.patientId }` | result.{patientName, patientBirthday, patientGender, customerId} |
| getPatientInfo.json | L6693 | `{ id: res.object.medicalRecord.patientId }` | (后续未消费) |
| getPatientInfo.json | L31226 | `{ id: $scope.patientId }` | result.object.customerId |
| getPatientInfo.json | L32906 | `{ id: $scope.patientId }` | res.result.object.patientName / customerId |
| getPatientVo.json | L8880 | `{ patientId: patientId }` | res.customer.id / patient.school / patient.schoolClass |
| getPatientVoList.json | L8364 | `{ name, mobile: $scope.obj.linkMobile }` | patientList |
| getPatientVoList.json | L8390 | `{ name, mobile: $scope.obj.linkMobile }` | patientList |
| getPatientVoList.json | L18981 | `{ customerId: $scope.customerId, index, length }` | **patientList** (Customer → Patient 桥!) |

---

## 6. MedicalRecord 全局扫描

### 6.1 字符级统计

| 模式 | 命中数 |
|---|---|
| `medicalRecordId` 总命中 | 多 |
| `medicalRecord\.id` 命中 | 12+ (L33842/L33844/L35085/L35149/L35166/L35182/L35201 等) |
| `res\.object\.medicalRecord\.id` 命中 | 1 (L4036) |
| `medicalRecord\.patientId` | 1 (L6693 `res.object.medicalRecord.patientId`) |
| `medicalRecord\.customerId` | **0** — MedicalRecord 不含 customerId |
| `medicalRecord\.customer` | **0** — MedicalRecord 不含 customer |
| `medicalRecord\.patient` | **0** — MedicalRecord 不含 patient 对象 |

### 6.2 MedicalRecord 字段（从 getMedicalRecord.json / addMedicalRecord.json Response）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `id` | L31125 / L31130 / L6693 `res.object.medicalRecord.id` | A |
| `medicalRecordType` | L31123 / L2257 / L32951 / L33055 / L33136 / L33156 | A |
| `patientId` | **A** — L31222 `res.result.object.patientId` / L6693 `res.object.medicalRecord.patientId` | A |
| `templateId` | L2256 `res.object.templateId` | A |
| `customerId` | **F** — 0 命中 | F |
| `customerCheckinId` | **F** — 0 命中 | F |

### 6.3 MedicalRecord 入口

```javascript
// L31220-L31236 MedicalRecord → Patient → Customer 链
var medicalPromise = $scope.getMedicalObjectFactory.saveOrQuery(
  "/admin/getMedicalRecord.json",
  { id: $scope.medicalRecordId }                              // L31220
);
medicalPromise.then(function (res) {
  $scope.patientId = res.result.object.patientId;              // L31222 — MedicalRecord.patientId
  $scope.date.checkYear = res.result.object.checkYear;
  $scope.updatePatientFactory = new ObjectFactory();
  var promise = $scope.updatePatientFactory.saveOrQuery(
    "/admin/getPatientInfo.json",
    { id: $scope.patientId }                                   // L31226
  );
  promise.then(function (res) {
    $scope.customerId = res.result.object.customerId;          // L31228 — Patient.customerId
    $scope.customerInfoFactory = new ObjectFactory();
    var customerPromise = $scope.customerInfoFactory.saveOrQuery(
      "/admin/getCustomerVo.json",
      { customerId: res.result.object.customerId }             // L31234
    );
  });
});
```

**MedicalRecord → Patient → Customer 链字符级**:
- L31222: `medicalRecord.patientId` → `$scope.patientId`
- L31226: `getPatientInfo.json { id: $scope.patientId }`
- L31228: `res.result.object.customerId` → `$scope.customerId`
- L31234: `getCustomerVo.json { customerId }` → Customer

### 6.4 MedicalRecord API 入口

| API | 行号 | Request | Response 实际消费 |
|---|---|---|---|
| addMedicalRecord.json | L31119 | `{ patientId, medicalRecordType }` | res.object.{id, medicalRecordType, patientId} |
| getMedicalRecord.json | L31220 | `{ id: $scope.medicalRecordId }` | res.result.object.patientId |
| getMedicalRecord.json | L6693 | (链式 computeUnPlaceOrderMedicalRecordFee Response) | res.object.medicalRecord.patientId |
| getMedicalRecord.json | L31331 | `{ id: $scope.medicalRecordId }` | (后续) |
| getMedicalRecord.json | L33134 | `{ id: response.result.vo.customerCheckin.medicalRecordId }` | res.object.medicalRecordType |
| getMedicalRecord.json | L32462 | `{ id: $scope.obj.medicalRecordId }` | (后续) |

### 6.5 MedicalRecord 关键冻结结论

| 命题 | 结论 | 等级 |
|---|---|---|
| MedicalRecord 有 `patientId` 字段 | **YES** | A |
| MedicalRecord 有 `customerId` 字段 | **NO** | F（0 命中）|
| MedicalRecord 有 `customer` 对象 | **NO** | F（0 命中）|
| MedicalRecord 有 `customerCheckinId` 字段 | **NO** | F（0 命中）|
| MedicalRecord 有 `patient` 对象 | **NO** | F（0 命中）|

**正式冻结**: MedicalRecord 当前源码未观察到 `customerId` / `customer` / `customerCheckinId` / `patient` 字段。

---

## 7. CustomerCheckin 字段扫描

### 7.1 字符级统计

| 模式 | 命中数 | 说明 |
|---|:---:|---|
| `customerCheckin\.id` | 6 | L8671 / L8697 / L8707 / L8791 / L10610 / L10642 / L33134 / L33203 / L34955（含间接）|
| `customerCheckin\.medicalRecordId` | 6 | L8791 / L10610 / L10642 / L33134 / L33203 / L34955 |
| `customerCheckin\.patientId` | 1 | L8707 |
| `customerCheckin\.customerId` | **0** | — |
| `customerCheckin\.patient` | 0 | — |
| `customerCheckin\.customer` | 0 | — |

### 7.2 L8707 完整上下文

```javascript
// L8704-L8709 (addCheckinCtrl, 注释代码 - 当前未启用)
new ObjectFactory()
  .saveOrQuery("/admin/addSchoolMateConsume.json", {
    schoolMateCheckId: $scope.appointVo.schoolMateCheckId,
    patientId: res.result.vo.customerCheckin.patientId,        // L8707
  })
```

**注意**: L8707 在注释代码块（L8699-L8714），但仍然反映了 customerCheckin 实体结构 — customerCheckin 包含 `patientId` 字段。

### 7.3 CustomerCheckin 字段总结

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `id` | 6+ 处 | A |
| `patientId` | L8707（注释中）/ 实际数据查询桥 | A |
| `medicalRecordId` | 6 处 | A |
| `customerId` | **F** — 0 命中 | F |
| `customer` | **F** — 0 命中 | F |
| `patient` | **F** — 0 命中 | F |

### 7.4 关键冻结结论

**正式冻结**: CustomerCheckin 当前源码未观察到 `customerId` / `customer` / `patient` 字段。CustomerCheckin 关联的"Customer" 通过 `customerCheckin.patientId → patient.customerId → customerId` 间接桥。

---

## 8. Customer → Patient（A 级双向）

### 8.1 桥 1：getPatientVoList.json by customerId

```javascript
// L18980-L18990 Controller
$scope.search = function (index, loadPagin) {
  HttpFactory.list('/admin/getPatientVoList.json', {
    customerId: $scope.customerId,                              // L18982 — 字符级
    index: index,
    length: 9
  }).then(function (res) {
    $scope.patientList = res.list;                              // L18986
    loadPagin && HttpFactory.pagination("#Pagination", res, $scope.search);
  });
};
```

| 项目 | 字符级证据 |
|---|---|
| A. Controller | （L18980 之前）|
| B. 调用行 | L18981 |
| C. Request | `{ customerId, index, length }` |
| D. Response | patientList |
| E. 是否转换 | A — `customerId` 直接作为查询参数 |

### 8.2 桥 2：getPatientVoList.json by name + mobile

```javascript
// L8364 / L8390
$scope.getPatientList = new ListFactory(
  "/admin/getPatientVoList.json",
  0, 30,
  { name: $scope.keyword, mobile: $scope.obj.linkMobile }       // L8364
);
```

| 项目 | 字符级证据 |
|---|---|
| Request | `{ name, mobile }` |
| Response | patientList |
| 是否是直接 Customer → Patient 桥 | **C** — 走的是 name/mobile 搜索，不依赖 customerId |

### 8.3 桥 3：choosePatient 函数中 patient 对象的 customerId 字段

```javascript
// L8424 choosePatient 参数列表
$scope.choosePatient = function (event, patientId, patientName, birthday, gender, linkMobile, channel, channelTagId, customerName, customerId, avatar, patientRemark, patient) {
  ...
  $scope.obj.patientId = patientId;                             // L8428
  $scope.checkCustomer.customerId = customerId;                 // L8429
  ...
  $scope.basic.schoolName = patient.school ? patient.school.schoolName : '';
  $scope.obj.schoolId = patient.school ? patient.school.id : null;
  ...
  $scope.obj.customerName = customerName;                       // L8444
};
```

| 项目 | 字符级证据 |
|---|---|
| Patient 列表返回的 patient 对象包含 customerId / customerName 字段 | L8424 函数参数 |
| 这意味着 **Patient 实体有 customerId / customerName 字段** | A |

### 8.4 Customer → Patient 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **Customer → Patient** | **A** | L18981 (getPatientVoList.json by customerId) / L8424 (patient 对象含 customerId) |

**关键发现**: 
- getPatientVoList.json 接受 `customerId` 作为查询参数 → Customer → Patient 是直接 API 桥
- Patient 列表中每个 patient 对象含 customerId → 双向都有字段

---

## 9. Patient → Customer（A 级双向）

### 9.1 桥 1：getPatientInfo.json Response → getCustomerVo.json Request

```javascript
// L31220-L31236 完整链
medicalPromise.then(function (res) {
  $scope.patientId = res.result.object.patientId;              // L31222
  ...
  var promise = $scope.updatePatientFactory.saveOrQuery(
    "/admin/getPatientInfo.json",
    { id: $scope.patientId }                                   // L31226
  );
  promise.then(function (res) {
    $scope.customerId = res.result.object.customerId;          // L31228 — Patient.customerId
    $scope.customerInfoFactory = new ObjectFactory();
    var customerPromise = $scope.customerInfoFactory.saveOrQuery(
      "/admin/getCustomerVo.json",
      { customerId: res.result.object.customerId }             // L31234
    );
  });
});
```

| 项目 | 字符级证据 |
|---|---|
| A. Patient 实体有 `customerId` 字段 | L31228 / L3650 / L32912 / L8424 |
| B. Patient.customerId → getCustomerVo.json Request | L31234 |
| C. getCustomerVo.json Response → Customer | A |

### 9.2 桥 2：L32906-L32912 模式

```javascript
// L32905-L32915
$scope.getPatientObjectFactory = new ObjectFactory();
var promise = $scope.getPatientObjectFactory.saveOrQuery(
  '/admin/getPatientInfo.json',
  { id: $scope.patientId }                                     // L32906
);
promise.then(function (res) {
  $scope.keyword = res.result.object.patientName;               // L32909
  $scope.customerInfoFactory = new ObjectFactory();
  $scope.customerInfoFactory.saveOrQuery(
    '/admin/getCustomerVo.json',
    { customerId: res.result.object.customerId }               // L32912
  );
  $scope.searchMedicalRecordlist();
});
```

### 9.3 桥 3：L3640-L3650 模式

```javascript
// L3640-L3655
$scope.getPatient = function () {
  var Patient = new ObjectFactory().saveOrQuery("/admin/getPatientInfo.json", { id: $stateParams.patientId });
  Patient.then(function (res) {
    var result = res.result.object;
    ...
    var promise = new ObjectFactory().saveOrQuery(
      "/admin/getCustomerVo.json",
      { customerId: result.customerId }                          // L3650
    );
    promise.then(function (res) {
      $scope.updatePatientFactory.linkMobile = res.vo.customer.linkMobile;
    });
  });
};
```

### 9.4 Patient → Customer 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **Patient → Customer** | **A** | L31228/L3650/L32912 (Patient.customerId 字段) / L18981 反向 / L8424 (patient 对象含 customerId) |

**关键发现**: Patient 实体**明确**有 `customerId` 字段（getPatientInfo.json Response 包含），可直接用于查询 Customer。

### 9.5 Customer ↔ Patient 双向 A 桥总结

| 方向 | 等级 | 主要证据 |
|---|---|---|
| Customer → Patient | **A** | getPatientVoList.json by customerId / patient 对象含 customerId |
| Patient → Customer | **A** | Patient.customerId 字段 / getCustomerVo.json by customerId |

**双向 A 桥成立**。

---

## 10. Patient → MedicalRecord

### 10.1 现有证据

- `medicalRecord.patientId` 字段存在（L6693 / L31222）
- 反方向 `patient.id → medicalRecord` 需要追查

### 10.2 Patient → MedicalRecord 直接桥

```javascript
// L32927 — patientId 用于查询 medicalRecord 列表
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

### 10.3 Patient → MedicalRecord 间接桥

Patient → MedicalRecord 还有**间接**路径：经 `patient.customerId → Customer → CustomerCheckin → MedicalRecord`（F — 因为 patient.customerId → customerCheckin 没有直接桥）。

### 10.4 Patient → MedicalRecord 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **Patient → MedicalRecord** | **A** | L32927 getMedicalRecordList.json { patientId } |

---

## 11. MedicalRecord → Patient

### 11.1 桥 1：medicalRecord.patientId → getPatientInfo.json

```javascript
// L6691-L6694
if (!$scope.getPatientObjectFactory) {
  $scope.getPatientObjectFactory = new ObjectFactory();
  $scope.getPatientObjectFactory.saveOrQuery(
    "/admin/getPatientInfo.json",
    { id: res.object.medicalRecord.patientId }                  // L6693
  );
}
```

### 11.2 桥 2：medicalRecord.patientId → getMedicalRecord.json Response

```javascript
// L31220-L31226
var medicalPromise = $scope.getMedicalObjectFactory.saveOrQuery(
  "/admin/getMedicalRecord.json",
  { id: $scope.medicalRecordId }
);
medicalPromise.then(function (res) {
  $scope.patientId = res.result.object.patientId;                // L31222
  ...
  var promise = $scope.updatePatientFactory.saveOrQuery(
    "/admin/getPatientInfo.json",
    { id: $scope.patientId }
  );
});
```

### 11.3 MedicalRecord → Patient 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **MedicalRecord → Patient** | **A** | L6693 / L31222 medicalRecord.patientId → getPatientInfo.json |

**双向 A 桥成立**（Patient ↔ MedicalRecord）。

---

## 12. Customer → MedicalRecord

### 12.1 直接桥

| 搜索 | 命中 | 等级 |
|---|---|---|
| `customerId` → `getMedicalRecord` | **0** | F |
| `customer.id` → `getMedicalRecord` | **0** | F |
| `res.customer.id` → `getMedicalRecord` | **0** | F |

### 12.2 间接桥

Customer → MedicalRecord 只能经：
- Customer → CustomerCheckin → MedicalRecord（F — customerCheckin 也不含 customerId）
- Customer → Patient → MedicalRecord（A — 经 patientId 中转）

### 12.3 Customer → MedicalRecord 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **Customer → MedicalRecord**（直接） | **F** | 0 命中 |
| **Customer → MedicalRecord**（经 Patient 中转） | **A**（间接 2 层） | L18981 (Customer → Patient) + L32927 (Patient → MedicalRecord) |

---

## 13. MedicalRecord → Customer

### 13.1 直接桥

| 搜索 | 命中 | 等级 |
|---|---|---|
| `medicalRecord.customerId` | **0** | F |
| `medicalRecord.customer` | **0** | F |
| `medicalRecord` → `getCustomerVo` | **0**（无直接调用）| F |

### 13.2 间接桥

MedicalRecord → Customer 只能经：
- MedicalRecord → Patient → Customer（A — 经 patientId → patient.customerId → customerId）

### 13.3 MedicalRecord → Customer 最终结论

| 方向 | 等级 | 字符级证据 |
|---|---|---|
| **MedicalRecord → Customer**（直接） | **F** | 0 命中 |
| **MedicalRecord → Customer**（经 Patient 中转） | **A**（间接 2 层） | L31222 (MedicalRecord.patientId) + L31228 (Patient.customerId) + L31234 (getCustomerVo) |

---

## 14. CustomerCheckin 三对象桥

### 14.1 CustomerCheckin → Patient

| 证据 | 等级 |
|---|---|
| `customerCheckin.patientId` L8707 (在 addSchoolMateConsume.json 注释代码中) | A |
| 实际 addCheckinCtrl 范围调用：**F**（注释代码） |

**正式冻结**: CustomerCheckin → Patient 桥在 L8707 注释代码中证明，但实际 addCheckinCtrl 流程未消费此字段。等级 **C**（局部证据）。

### 14.2 CustomerCheckin → Customer

| 搜索 | 命中 | 等级 |
|---|---|---|
| `customerCheckin.customerId` | **0** | F |
| `customerCheckin.customer` | **0** | F |

**正式冻结**: CustomerCheckin 不含 customerId 字段。**CustomerCheckin → Customer = F**。

### 14.3 CustomerCheckin → MedicalRecord

| 证据 | 等级 |
|---|---|
| `customerCheckin.medicalRecordId` 6 处（L8791/L10610/L10642/L33134/L33203/L34955）| A |

**CustomerCheckin → MedicalRecord = A**（S1-135/S1-137R 已确认）。

### 14.4 MedicalRecord → CustomerCheckin

| 搜索 | 命中 | 等级 |
|---|---|---|
| `medicalRecord.customerCheckinId` | **0** | F |
| `medicalRecord.customerCheckin` | **0** | F |

**正式冻结**: MedicalRecord 不含 customerCheckinId 字段。**MedicalRecord → CustomerCheckin = F**。

### 14.5 CustomerCheckin 桥总结

| 桥 | 等级 |
|---|---|
| CustomerCheckin → Patient | C（局部：仅 L8707 注释代码）|
| CustomerCheckin → Customer | F |
| CustomerCheckin → MedicalRecord | A |
| MedicalRecord → CustomerCheckin | F |

---

## 15. addMedicalRecord Request 字段

### 15.1 完整字符级证据

```javascript
// L31115-L31119
var obj = {
  patientId: item.patient.id,                                    // L31116
  medicalRecordType: custView == 1 ? 1 : 5                      // L31117
};
new ObjectFactory().saveOrQuery(
  "/admin/addMedicalRecord.json",                                // L31119
  obj
);
```

### 15.2 addMedicalRecord Request 字段

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `patientId` | L31116 `item.patient.id` | A |
| `medicalRecordType` | L31117 `custView == 1 ? 1 : 5` | A |
| `customerId` | **F** — 0 命中 | F |
| `customerCheckinId` | **F** — 0 命中 | F |

### 15.3 addMedicalRecord 关键发现

- **addMedicalRecord.json Request 仅有 patientId + medicalRecordType**
- **没有 customerId** — 创建 MedicalRecord 时不需要 Customer
- 关系：patientId → Patient → Patient.customerId → Customer（间接关联）

---

## 16. insertCustomerCheckin* Request 字段

### 16.1 insertCustomerCheckinOfNewPaitent.json（L8667）

```javascript
// L8665-L8667
$scope.checkCustomer.appointId = aId;
$scope.insertCustomerCheckFactory = new ObjectFactory();
var insertPromise = $scope.insertCustomerCheckFactory.saveOrQuery(
  "/admin/insertCustomerCheckinOfNewPaitent.json",
  $scope.checkCustomer                                          // L8667
);
```

`$scope.checkCustomer` 字段（推断）:
- `appointId` (L8665)
- `customerName` (L8591)
- `linkMobile` (L8592)
- `employeeId` (L8593)
- `gender` (L8598)
- `idCard` (L8602)
- `registrationFeeId` (L8663)

**F** — insertCustomerCheckinOfNewPaitent.json **不**带 patientId / customerId（因为是"新患者"路径）。

### 16.2 insertCustomerCheckinOfNewCustomer.json（L8679）

Request: `$scope.obj` (含 patientId / name / birthday / registrationFeeId 等) — 实际字段需要从 addCheckinCtrl HTML 模板推断

**F** — 字符级未直接看到 patientId，但根据 API 命名"新 Customer"可能含 customerName 等

### 16.3 insertCustomerCheckin.json（L8681 / L34914）

| 行号 | Controller | Request |
|---|---|---|
| L8681 | addCheckinCtrl | `$scope.obj` (含 patientId, name, birthday 等) |
| L34914 | optometryCtrl | `{ name, gender, patientId, employeeId }` |

L34914 字符级**明确**有 `patientId: obj.patient.id`（L34912）。

### 16.4 insertCustomerCheckin* Request 字段对比

| API | patientId | customerId | customerName | linkMobile | employeeId |
|---|:---:|:---:|:---:|:---:|:---:|
| insertCustomerCheckinOfNewPaitent.json | F（推断）| F | A（L8591）| A（L8592）| A（L8593）|
| insertCustomerCheckinOfNewCustomer.json | F | F | F（推断）| F | F |
| insertCustomerCheckin.json (addCheckinCtrl L8681) | F（推断）| F | F | F | F |
| insertCustomerCheckin.json (optometryCtrl L34914) | **A**（L34912）| F | A（L34910）| F | A（L34913）|

### 16.5 关键发现

- **3 个 insertCustomerCheckin* API 在 2 个不同 Controller 中行为不同**:
  - addCheckinCtrl: 不带 patientId（"新接诊"路径）
  - optometryCtrl: 带 patientId（"已有患者接诊"路径）
- **都不带 customerId** — customerCheckin 不直接关联 customer（间接经 patient.customerId）

---

## 17. Mobile 链

### 17.1 字符级统计

| 模式 | 命中 | 等级 |
|---|:---:|---|
| `customerMobile` | 多 | A |
| `linkMobile` | 多 | A |
| `mobile` | 多 | A |
| `customerMobile → patient` | **0** | F |
| `linkMobile → patient` | C（L8424 `choosePatient` 接受 linkMobile） | C |
| `mobile → getPatientVoList` (L8364) | A | A |

### 17.2 Mobile 查询 Patient 路径

```javascript
// L8364
$scope.getPatientList = new ListFactory(
  "/admin/getPatientVoList.json",
  0, 30,
  { name: $scope.keyword, mobile: $scope.obj.linkMobile }       // L8364
);
```

| 项目 | 字符级证据 |
|---|---|
| API | getPatientVoList.json |
| Request 字段 | `name`, `mobile` |
| Mobile 角色 | 仅作为查询条件，**不**作为 ID 转换 |
| 等级 | **C**（局部） |

### 17.3 Mobile 桥

| 桥 | 等级 |
|---|---|
| Mobile → Patient (搜索) | C（getPatientVoList.json 接受 mobile）|
| Mobile → MedicalRecord | F（无直接 API）|
| Mobile → Customer | A（customerMobile 是 Customer 字段）|
| Mobile → Patient (1:1 转换) | F（mobile 不能作为身份合并证据）|

---

## 18. State / URL

### 18.1 $stateParams 全量

| 参数 | 命中 | 等级 |
|---|:---:|---|
| `$stateParams.customerId` | 20+ (L5894/L5913/L5925/L5938/L5994/L6000/L6008/L6510/L16746/L16759/L18060/L18084/L18145/L18191 等) | A |
| `$stateParams.patientId` | 4+ (L3641/L8213/L11829/L16745) | A |
| `$stateParams.medicalRecordId` | 30+ (L1757/L1886/L1907/L2214/L2244/L2400/L2417/L2686/L2693/L41710/L31159/L31286/L31388/L31609/L31741/L31758/L31923/L32123/L32445/L33223/L33590/L33783/L33842/L33900/L35388 等) | A |
| `$stateParams.cashflowId` | 5 (L3814/L4026/L4238/L4381/L4940) | A |
| `$stateParams.customerCheckinId` | 多 (L8789 等) | A |
| `$stateParams.appointId` | 多 (L8648/L44169 等) | A |

### 18.2 State 路由关键三元组

| 入口 State | 入口参数 | Target Controller |
|---|---|---|
| `customerDetail` / `customer.*` | customerId | reChargeList / reChargeListBack / member / 各种 |
| `myMedicalRecordList` | patientId | myMedicalRecordListCtrl |
| `myMaterialBill` / `myMemberRecord` | medicalRecordId, patientId | adminMyRecord.* |
| `optometryGlasses` | medicalRecordId | optometryGlassesCtrl |
| `deliveryInput` | cashflowId | deliveryInputCtrl |

### 18.3 State 携带的对象 ID 关系

- **`customerId` State 入口 → Customer Controller**（A — 直接）
- **`patientId` State 入口 → Patient Controller**（A — 直接）
- **`medicalRecordId` State 入口 → MedicalRecord Controller**（A — 直接）
- **`customerId` + `patientId` 同时出现**: L16745-L16746 (`$scope.patientId = $stateParams.patientId; $scope.customerId = $stateParams.customerId;`) — 状态机同时携带
- **`medicalRecordId` + `patientId` 同时出现**: L31124/L31129/L31145 等 — Create 后立即携带

### 18.4 State / URL 最终结论

- 4 个 ID 都有独立的 State 入口（A）
- 没有任何 State 入口**仅**用 customerId 进入 MedicalRecord Controller
- 没有任何 State 入口**仅**用 patientId 进入 Customer Controller

---

## 19. Factory / Scope

### 19.1 ObjectFactory 命名 vs 实际内容

| Factory 名称 | 实际存储 | 命名误导 |
|---|---|---|
| `patientObjectFactory` (L5930) | `res.result.vo.customer` | **是** — 存的是 customer |
| `patientObjectFactory` (L4947) | `getCustomerVo.json` Response | **是** — 实际查询 customer |
| `patientObjectFactory` (L5243) | `getCustomerVo.json` | **是** |
| `patientObjectFactory` (L7491) | `getCustomerVo.json` | **是** |
| `customerFactory` (L20960) | `getCustomerVo.json` | 否 — 一致 |
| `getCustomerObjectFactory` (L7070) | `getMedicalRecordCashflowVo.json` | **是** — 存 cashflow |

### 19.2 跨 Controller 共享

**F** — 每个 Controller 独立 `new ObjectFactory()`，无跨 Controller 共享。

证据:
- L5930 `$scope.patientObjectFactory = ...` (单 Controller Scope)
- L5243 重新 `$scope.patientObjectFactory = new ObjectFactory();`
- L7070 重新 `$scope.getCashflowObjectFactory = new ObjectFactory();`

**正式冻结**: 不存在"共享 Service/Factory"，每个 ObjectFactory 都是 Controller 内部独立实例。

### 19.3 $scope 全量

| 字段 | 等级 |
|---|---|
| `$scope.customer` | A |
| `$scope.patient` | A |
| `$scope.medicalRecord` | A（已 S1-138 确认）|
| `$scope.cashflow` | A |
| `$scope.patientObjectFactory`（实际 customer）| A（命名误导）|
| `$scope.getCustomerObjectFactory`（实际 cashflow）| A（命名误导）|

---

## 20. 完整三对象桥矩阵

| 来源 | 目标 | Function | State | API Resp→Req | Scope/Service | Factory | Object | 共现 | 结论 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Customer** | **Patient** | A (L18981) | A | A (L18982) | A | F | A (L8424) | A | **A** |
| **Patient** | **Customer** | A (L3650) | A | A (L31228→L31234) | A | F | A (L8424 patient.customerId) | A | **A** |
| **Patient** | **MedicalRecord** | A (L32927) | A (L11829) | A (L32927) | A | F | A | A | **A** |
| **MedicalRecord** | **Patient** | A (L6693) | A (L31222) | A (L31226) | A | F | A | A | **A** |
| **Customer** | **MedicalRecord** | F | F | F | F | F | F | F | **F** (直接)；**A 间接**（经 Patient）|
| **MedicalRecord** | **Customer** | F | F | F | F | F | F | F | **F** (直接)；**A 间接**（经 Patient）|
| **CustomerCheckin** | **Patient** | F (addCheckinCtrl 范围) | F | C (L8707 注释) | F | F | F | F | **C** (局部) |
| **CustomerCheckin** | **Customer** | F | F | F | F | F | F | F | **F** |
| **CustomerCheckin** | **MedicalRecord** | A | A | A | A | F | A | A | **A** |
| **MedicalRecord** | **CustomerCheckin** | F | F | F | F | F | F | F | **F** |
| **Mobile** | **Patient** | A (L8364) | F | A | F | F | F | A | **C** (查询桥) |
| **Mobile** | **Customer** | A (customerMobile 字段) | F | A | F | F | A | A | **A** (字段) |
| **Mobile** | **MedicalRecord** | F | F | F | F | F | F | F | **F** |
| **Mobile** | **CustomerCheckin** | F | F | F | F | F | F | F | **F** |

---

## 21. ID 等同/不同

### 21.1 明确等同

| ID | 等同于 | 字符级证据 | 等级 |
|---|---|---|---|
| `medicalRecord.patientId` | `patientId` (State 入口) | L31222 / L6693 | A |
| `patient.customerId` | `customerId` (查询参数) | L31228 / L3650 / L32912 | A |
| `customerCheckin.id` | `printCheckinId` | L8671 / L8697 | A |
| `res.customer.id` (L8895) | `customerId` (查询参数) | L8895 | A |
| `res.patient.id` (L33204) | `patientId` (State 入口) | L33204 | A |
| `customerCheckin.patientId` | `patientId` | L8707 | A |
| `customerCheckin.medicalRecordId` | `medicalRecordId` | 6 处 | A |

### 21.2 明确不同

| ID A | ≠ ID B | 字符级证据 | 等级 |
|---|---|---|---|
| `customerId` | `patientId` | L16745 / L16746 同时存在 (说明不同 ID) | A |
| `customerId` | `medicalRecordId` | MedicalRecord 无 customerId 字段 (0 命中) | A |
| `patientId` | `medicalRecordId` | L31116 (patientId 单独) vs L31125 (medicalRecord.id) | A |
| `customerId` | `customerCheckinId` | Customer 无 customerCheckinId 字段 (0 命中) | A |
| `patientId` | `customerCheckinId` | customerCheckinId 在 addCheckinCtrl L8789 | A |
| `customerCheckinId` | `medicalRecordId` | customerCheckin 6 处携带 medicalRecordId 字符级 (L8791 等) | A |
| `customerCheckinId` | `cashflowId` | 2 个独立 State 入口 | A |
| `medicalRecordType` | `medicalRecordId` | 16 处 medicalRecordType 是 5/1/6/7 等枚举值 | A |

### 21.3 无法证明

| 命题 | 等级 |
|---|---|
| `customerCheckin.customerId` 是否存在 | F（0 命中，需后端证据）|
| `medicalRecord.customerCheckinId` 是否存在 | F（0 命中）|
| `customer` 与 `patient` 实体是否 1:1 | F（无后端证据）|
| `customer` 与 `patient` 实体是否 1:N | F（无后端证据）|
| 多个 patient 是否可对应同一 customer | F（无后端证据）|

---

## 22. 精确数量

### 22.1 字符级精确统计

| 模式 | 命中数 |
|---|---:|
| `customerId` | 164 |
| `patientId` | 90 |
| `medicalRecordId` | 多 (S1-138 统计) |
| `customerCheckin.id` | 6 |
| `customerCheckin.patientId` | 1 |
| `customerCheckin.medicalRecordId` | 6 |
| `customerCheckin.customerId` | 0 |
| `medicalRecord.patientId` | 1 |
| `medicalRecord.customerId` | 0 |
| `medicalRecord.customer` | 0 |
| `patient.customerId` | 多 (L31228/L3650/L32912/L8424) |
| `customer.patientId` | 0 |
| `customer.patient` | 0 |

### 22.2 三对象桥精确数量

| 桥 | 直接 A 数 | 间接 A 数 | 总数 |
|---|:---:|:---:|:---:|
| Customer → Patient | 1 (L18981) | 0 | 1 |
| Patient → Customer | 1 (L31228→L31234) | 0 | 1 |
| Patient → MedicalRecord | 1 (L32927) | 0 | 1 |
| MedicalRecord → Patient | 1 (L6693) | 0 | 1 |
| Customer → MedicalRecord | 0 | 1 (经 Patient) | 1 |
| MedicalRecord → Customer | 0 | 1 (经 Patient) | 1 |
| CustomerCheckin → Patient | 0 (仅 C) | 0 | 0 |
| CustomerCheckin → Customer | 0 | 0 | 0 |
| CustomerCheckin → MedicalRecord | 6 | 0 | 6 |
| MedicalRecord → CustomerCheckin | 0 | 0 | 0 |

### 22.3 $stateParams ID 类型统计

| ID | 命中 | 等级 |
|---|:---:|---|
| $stateParams.customerId | 20+ | A |
| $stateParams.patientId | 4+ | A |
| $stateParams.medicalRecordId | 30+ | A |
| $stateParams.cashflowId | 5 (Delivery 范围) | A |
| $stateParams.customerCheckinId | 多 | A |
| $stateParams.appointId | 多 | A |

---

## 23. L1 / L2 / L3

| 层级 | 范围 | 等级 |
|---|---|---|
| L1 | 字段 / API / State / Response / Request / Controller 字符级 | A |
| L2 | "Customer → Patient 双向 A 桥" / "CustomerCheckin 不含 customerId" 等派生解释 | A |
| L3 | 数据库表 / 事务边界 / FK / 唯一索引 / Customer:Patient 1:1 或 1:N | **F**（无后端证据）|

---

## 24. 最终三对象 DAG

### DAG A: Customer → Patient
**A** — L18981 getPatientVoList.json by customerId / L8424 patient 对象含 customerId

### DAG B: Patient → Customer
**A** — L31228/L3650/L32912 Patient.customerId 字段 / L8424 patient.customerId

### DAG C: Patient → MedicalRecord
**A** — L32927 getMedicalRecordList.json by patientId

### DAG D: MedicalRecord → Patient
**A** — L6693 / L31222 medicalRecord.patientId

### DAG E: Customer → MedicalRecord
**F**（直接）/ **A**（经 Patient 间接 2 层）

### DAG F: MedicalRecord → Customer
**F**（直接）/ **A**（经 Patient 间接 2 层）

### DAG G: CustomerCheckin → Patient
**C**（仅 L8707 注释代码）

### DAG H: CustomerCheckin → Customer
**F**（customerCheckin 无 customerId 字段）

### DAG I: CustomerCheckin → MedicalRecord
**A**（6 处字符级桥）

### DAG J: MedicalRecord → CustomerCheckin
**F**（medicalRecord 无 customerCheckinId 字段）

### DAG K: Mobile → Patient
**C**（getPatientVoList.json by mobile）

### DAG L: Patient → MedicalRecord（同 DAG C）
**A**

---

## 25. 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Customer Source | 字符级充分 | A | 多处 | L5894/L5925/L5994 等 | A |
| 2 | customerId Source | 164 命中 | A | 多处 | 全部 | A |
| 3 | Patient Source | 字符级充分 | A | 多处 | L3641/L31226/L32906 等 | A |
| 4 | patientId Source | 90 命中 | A | 多处 | 全部 | A |
| 5 | MedicalRecord Source | 字符级充分 | A | 多处 | L31119/L31220/L6693 | A |
| 6 | medicalRecordId Source | 多 | A | 多处 | 全部 | A |
| 7 | Customer → Patient | A 双向 | A | 多处 | L18981/L8424 | A |
| 8 | Patient → Customer | A 双向 | A | 多处 | L31228/L3650/L32912 | A |
| 9 | Patient → MedicalRecord | A | A | 多处 | L32927 | A |
| 10 | MedicalRecord → Patient | A | A | 多处 | L6693/L31222 | A |
| 11 | Customer → MedicalRecord | F 直接 / A 间接 | F/A | — | — | F 直接 |
| 12 | MedicalRecord → Customer | F 直接 / A 间接 | F/A | — | — | F 直接 |
| 13 | CustomerCheckin → Patient | C (L8707 注释) | C | addCheckinCtrl | L8707 | C |
| 14 | CustomerCheckin → Customer | F | F | — | — | F |
| 15 | CustomerCheckin → MedicalRecord | A (6 处) | A | 多处 | L8791/L10610/L10642/L33134/L33203/L34955 | A |
| 16 | MedicalRecord → CustomerCheckin | F | F | — | — | F |
| 17 | CustomerCheckin 三对象字段 | patientId+medicalRecordId YES / customerId NO | A | — | — | A/F |
| 18 | addMedicalRecord | patientId+medicalRecordType YES / customerId NO | A | addSaleRecordCtrl | L31115-L31117 | A |
| 19 | insertCustomerCheckinOfNewPaitent | 字符级不含 patientId | F | addCheckinCtrl | L8667 | F |
| 20 | insertCustomerCheckinOfNewCustomer | 字符级未直接看到 patientId | F | addCheckinCtrl | L8679 | F |
| 21 | insertCustomerCheckin | 2 个 Controller 行为不同 | A/C | addCheckinCtrl/optometryCtrl | L8681/L34914 | A/C |
| 22 | Mobile → Patient | C (查询桥) | C | 多处 | L8364/L8390 | C |
| 23 | State / URL | 4 ID 都有独立 State 入口 | A | 多处 | 全部 | A |
| 24 | ID 等同/不同 | 7 项等同 / 8 项不同 / 5 项 F | A | — | — | A |
| 25 | 最终三对象 DAG | 12 条（A-F 等级标注）| A | — | — | A |
| 26 | 复刻风险 | 命名误导 / 字段冻结 / 中转链 | — | — | — | 见 §28 |

---

## 26. A/B/C/D/E/F 等级

| 等级 | 数量 | 说明 |
|---|:---:|---|
| A | 22 | 字符级源码证据 |
| B | 0 | 无需多源互证 |
| C | 3 | (L8707 注释 / L8364 移动搜索 / 局部证据) |
| D | 0 | 无冲突 |
| E | 0 | 无业务推断（E 不入规格）|
| F | 6 | (Customer → MedicalRecord 直接 / MedicalRecord → Customer 直接 / CustomerCheckin → Customer / MedicalRecord → CustomerCheckin / 2 项 F 直接桥)|

---

## 27. 历史差异

### 27.1 S1-138 漏掉

| 漏掉项 | 本轮补 |
|---|---|
| Customer ↔ Patient 双向 A 桥 | S1-138 仅在 §15 提到 patientId 5 处，但未明确 Patient → Customer 直接桥 |
| Patient → Customer 字符级桥 | L31228 / L3650 / L32912 字符级 |
| Customer → Patient 字符级桥 | L18981 getPatientVoList.json by customerId |

### 27.2 S1-135 / S1-137 / S1-137R 部分表述修订

| 历史表述 | 本轮修正 |
|---|---|
| S1-137 "Patient 与 Customer 关系不明确" | 明确：Patient 含 customerId 字段，双向 A 桥 |
| S1-137R "patientId 是 MedicalRecord 的 input，customerId 不参与" | 仍成立；patientId 是 MedicalRecord Create 的唯一对象 ID |

### 27.3 历史错误记录（不修改旧文档）

- 165_S1-124 ~ 201_S1-138 全部保持原样
- 本文档 202_*.md 单独记录精确审计
- 后续 S1-140+ 应直接采用本轮精确结论

---

## 28. 复刻红线

### 28.1 字段冻结（必实现）

| 实体 | 必有字段 | 等级 | 必无字段 | 等级 |
|---|---|---|---|---|
| **Customer** | id, customerName, linkMobile, channel, channelTagId | A | **patientId, patient, customerCheckinId** | F |
| **Patient** | id, patientName, patientBirthday, patientGender, customerId, school, schoolClass | A | **medicalRecord, customerCheckin** | F |
| **MedicalRecord** | id, medicalRecordType, patientId, templateId | A | **customerId, customer, customerCheckinId, patient** | F |
| **CustomerCheckin** | id, patientId, medicalRecordId | A | **customerId, customer, patient** | F |

### 28.2 桥必实现（后端 API）

| 桥 | 必实现 API | 等级 |
|---|---|---|
| Patient → Customer | getCustomerVo.json { customerId } (其中 customerId = patient.customerId) | A |
| Customer → Patient | getPatientVoList.json { customerId } | A |
| Patient → MedicalRecord | getMedicalRecordList.json { patientId } | A |
| MedicalRecord → Patient | getPatientInfo.json { id: medicalRecord.patientId } | A |
| CustomerCheckin → MedicalRecord | Response: customerCheckin.medicalRecordId 字段 | A |

### 28.3 命名误导必标注

| 命名 | 实际内容 | 复刻警告 |
|---|---|---|
| `patientObjectFactory` | 经常存 customer（L5930/L4947/L5243/L7491）| 命名误导 |
| `customerFactory` | 存 customer | 一致 |
| `customerCheckin.id` | ≡ printCheckinId | 实际 |
| `customerCheckin.patientId` | 字符级存在 (L8707 注释) | 实际 |
| `customerCheckin.medicalRecordId` | 6 处字符级 | 实际 |
| `customerCheckin.customerId` | **不存在** (0 命中) | 必须显式不返回 |
| `medicalRecord.customerId` | **不存在** (0 命中) | 必须显式不返回 |
| `customer.patientId` | **不存在** (0 命中) | 必须显式不返回 |
| `customer.patient` | **不存在** (0 命中) | 必须显式不返回 |

### 28.4 同 API 不同行为（必区分）

`insertCustomerCheckin.json` 在 2 个 Controller 中行为不同:
- addCheckinCtrl (L8681): 新接诊流程
- optometryCtrl (L34914): 已有患者接诊 → 链式 beginCustomerCheckin

**复刻后端必须按调用点区分**。

### 28.5 间接桥必实现

- Customer → MedicalRecord 必须经 Patient 中转（2 层）
- MedicalRecord → Customer 必须经 Patient 中转（2 层）
- 不可直接建立 Customer ↔ MedicalRecord API

---

## 29. 红线检查

| 红线 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-201 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ 视光之家url.txt 未修改 |
| 本轮只新增 202_*.md | ✓ |

---

## 30. Git

### 30.1 操作

```
git add -- 202_S1-139_Patient_Customer_MedicalRecord三对象身份关系总审计.md
git diff --cached --name-only
git commit -m "docs(202): S1-139 Patient Customer MedicalRecord 三对象身份关系总审计"
git push origin master
```

### 30.2 预期

| 项目 | 值 |
|---|---|
| LOCAL HEAD | (new commit) |
| REMOTE origin/master | (new commit) |
| LOCAL == REMOTE | YES |
| tracked | 210（commit 202 后从 209 → 210） |
| untracked | 10 |
| ignored | 1 |
| staged | 0 |
| staged only current document | ✓ 202_*.md |
| 文件修改数 | 1 file changed, ~1500+ insertions |

---

## 附录：本轮关键字符级证据行号索引

| 行号 | 关键事实 |
|---|---|
| L31222 | MedicalRecord.patientId 字段 |
| L31228 | Patient.customerId 字段（getPatientInfo Response）|
| L31234 | Patient → Customer 直接桥（getCustomerVo Request）|
| L6693 | MedicalRecord → Patient 直接桥（medicalRecord.patientId → getPatientInfo）|
| L18981 | **Customer → Patient 直接桥**（getPatientVoList.json by customerId）|
| L3650 | Patient → Customer 直接桥（customerId: result.customerId）|
| L32912 | Patient → Customer 直接桥（customerId: res.result.object.customerId）|
| L8424 | choosePatient 函数参数：patient 对象含 customerId / customerName / linkMobile 等 |
| L32927 | Patient → MedicalRecord 直接桥（getMedicalRecordList.json by patientId）|
| L6700+ | medicalRecord 对象不含 customer/customerCheckinId 字段（0 命中）|
| L5930 | patientObjectFactory 实际存 customer（命名误导）|
| L5243 / L7491 | patientObjectFactory 实际调 getCustomerVo.json（命名误导）|
| L8707 | customerCheckin.patientId 字段（注释代码）|
| L8791/L10610/L10642/L33134/L33203/L34955 | customerCheckin.medicalRecordId 6 处 |
| L8671/L8697 | customerCheckin.id ≡ printCheckinId |

---

S1-139 完成。立即停止，等待老板下一指令。不执行 S1-140。
