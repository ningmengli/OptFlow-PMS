# S1-108 optometryGlassesCtrl API、medicalRecordId 数据链与 State 出口审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML（无 optometry 模板，F 边界）
> - Controller 范围：L35383 – L35959（577 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-107（HEAD=9942a6c）
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD / 修改 7 HTML / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **Controller 源**：`optometryGlassesCtrl`，注册于 `controller.js` L35383
- **行范围**：L35383 – L35959（577 行）
  - L35383：`.controller("optometryGlassesCtrl", [ ... ])` 注册
  - L35958：`$scope.getMedicalRecord();`（Init 末尾调用）
  - L35959：`}]);`（Controller 闭合）
  - L35960：`"use strict";`（下一个 module 边界）
- **审计目标**：
  1. 完整 Controller 业务/API DAG
  2. medicalRecordId 数据链全量闭合
  3. State 出口全量审计
- **资源边界**：
  - 7 untracked HTML 中 0 处 optometry 模板（F 边界）
  - 0 处 `.state()` 注册（State 配置不在 controller.js 内，F 边界）
  - deliveryList.html 12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）

---

## 2. Controller 注册与 DI

| 项 | 证据 | A-F |
|---|---|---|
| Controller 名 | `optometryGlassesCtrl`（L35383 字符串字面量） | A |
| 所属 module | `bestvisionWeb`（L35383 `angular.module("bestvisionWeb").controller(...)`） | A |
| 注册位置 | `controller.js` L35383 | A |
| 注册次数 | 1 次（grep `optometryGlassesCtrl` 在 controller.js 全局唯一出现 L35383 + L35383 内部 DI 列表中的 "optometryGlassesCtrl" 字符串名） | A |
| DI 列表 | `["$scope", "Popup", "utilFactory", "ObjectFactory", "ListFactory", "$timeout", "$stateParams"]` | A |
| DI 形参 | `function ($scope, Popup, utilFactory, ObjectFactory, ListFactory, $timeout, $stateParams)` | A |
| 是否注入 `$state` | **否**（与 optometryCtrl L34776 不同；optometryCtrl 注入 `$state`，本 Controller 不注入） | A |
| 是否注入 `$stateParams` | 是（L35383） | A |
| 是否注入 `HttpFactory` | 否（区别于 optometryListCtrl L35962） | A |
| 是否注入 `$rootScope` | 否 | A |

**关键观察**：
- 本 Controller **不注入 `$state`**，与 S1-105 锁定的 optometryCtrl（L34776 注入 `$state`）形成对比。
- 因此本 Controller 内**无法**直接调用 `$state.go(...)`，需要通过其他方式离开页面（F 边界：HTML 可能通过 `<a ui-sref>` 或其它路由机制跳转）。
- 实际代码中**确证 0 处 `$state.go`**（A 级，grep 结果见第 16 节）。

---

## 3. StateParams 全量审计

| 行号 | 参数名 | 赋值对象 | 后续 Consumer | A-F |
|---:|---|---|---|---|
| 35388 | `medicalRecordId` | `$scope.medicalRecordId` | L35417 / L35425 / L35605 / L35640 / L35653 / L35686 / L35816 / L35842 / L35947（9 处） | A |
| 35389 | `edit` | `$scope.edit`（强比较 `=== "true"`） | L35409（`$scope.showOtherStore = $scope.edit`） | A |

**派生规则**：

```javascript
// L35388
$scope.medicalRecordId = $stateParams.medicalRecordId;
// L35389
$scope.edit = $stateParams.edit === "true";
```

- `medicalRecordId`：直接赋值，**不**做类型转换（可能为字符串也可能为数值，依赖调用方传值）
- `edit`：**强比较字符串** `"true"`。若 `$stateParams.edit` 为 `undefined` / `null` / `"false"` / `1` 等，$scope.edit 均为 `false`

**StateParams 字段使用全集**：
- 仅 `medicalRecordId` 与 `edit` 2 个
- **0 处**直接读取 `$stateParams.xxx`（除 L35388/L35389）
- 这 2 个参数在进入 Controller 1 行之内立即被复制到 `$scope`，后续无再次读取 `$stateParams`

**S1-107 对齐**：
- S1-107 已确认 optometryCtrl 出口 `$state.go("optometryGlasses", { medicalRecordId: ... })` 的两个入口：
  1. `beginCustomerCheckin` success callback
  2. `fnMap` "修改" 动作
- 本 Controller 作为这两个入口的**接收方**，消费 `medicalRecordId`（必传）与 `edit`（仅"修改"入口传 `"true"`）

---

## 4. 初始化执行链

### 4.1 注册即执行（DAG 顺序）

按源码位置从 L35383 → L35958 排列，识别**注册即执行**的语句（不依赖函数被调用）：

| # | 行号 | 语句 | 类型 | 证据 |
|---:|---:|---|---|---|
| 1 | 35384 | `$scope.enableNegativeStock = false;` | Scope 初始化 | A |
| 2 | 35385-35387 | `window.getStockSet(ObjectFactory, "enableNegativeStock").then(...)` | 异步 Read | A |
| 3 | 35388 | `$scope.medicalRecordId = $stateParams.medicalRecordId;` | StateParams 复制 | A |
| 4 | 35389 | `$scope.edit = $stateParams.edit === "true";` | StateParams 转换 | A |
| 5 | 35390 | `$scope.medicalRecord = {};` | Scope 初始化 | A |
| 6 | 35391 | `$scope.tip = function () {};` | 函数占位 | A |
| 7 | 35392-35407 | `$scope.prevent = function (event) { ... }` | 函数定义 | A |
| 8 | 35409 | `$scope.showOtherStore = $scope.edit;` | Scope 派生 | A |
| 9 | 35410-35412 | `$scope.upOther = function (key) { ... }` | 函数定义 | A |
| 10 | 35413 | `$scope.showPerfectInfo = false;` | Scope 初始化 | A |
| 11 | 35414 | `$scope.userInfo = {};` | Scope 初始化 | A |
| 12 | 35415-35470 | `$scope.getMedicalRecord = function () { ... }` | 函数定义（含内嵌 getPatientInfo + getCustomerVo 隐式 Read） | A |
| 13 | 35471-35477 | `$scope.dateCom = { ... }` | 对象初始化 | A |
| 14 | 35478-35480 | `$scope.showCommon = function () { ... }` | 函数定义 | A |
| 15 | 35481-35491 | `$scope.upimg = { ... }` | 对象初始化 | A |
| 16 | 35492-35495 | `$scope.updateImg = function () { return; ... }` | 函数定义（空实现） | A |
| 17 | 35496-35543 | `$scope.updatePatient = function () { ... }` | 函数定义（含隐式 Write savePatientInfo + saveCustomerInfo） | A |
| 18 | 35547-35554 | 工具变量赋值（$scope.qiuJingArr, $scope.eyeDistanceArr 等） | Scope 派生 | A |
| 19 | 35555-35572 | `var saleInfo = { ... }`（局部变量） | 局部变量初始化 | A |
| 20 | 35573-35601 | `$scope.object = { right15, left15, right14, ... }` | Scope 初始化（大量 right*/left* 字段，27 字段） | A |
| 21 | 35603-35622 | `$scope.GetMethodGlassRecordVo = function () { ... }` | 函数定义 | A |
| 22 | 35623 | `$scope.GetMethodGlassRecordVo();` | **Init 立即执行** | A |
| 23 | 35624-35630 | `$scope.update = function (...)` | 函数定义 | A |
| 24 | 35631-35634 | `$scope.update2 = function (key) { ... }` | 函数定义 | A |
| 25 | 35635-35649 | `$scope.saveChufang = function () { ... }` | 函数定义（含 updateMethodGlassRecord Write） | A |
| 26 | 35650-35657 | `$scope.printChufang = { ... }` | 对象初始化 | A |
| 27 | 35660 | 注释 | - | - |
| 28 | 35661-35671 | `$scope.queryStorehouseId = function (companyId) { ... }` | 函数定义 | A |
| 29 | 35672 | `$scope.tempShop = [];` | Scope 初始化 | A |
| 30 | 35674-35681 | `$scope.queryCompanyName = function () { ... }` | 函数定义 | A |
| 31 | 35682 | `$scope.queryCompanyName();` | **Init 立即执行** | A |
| 32 | 35683-35728 | `$scope.GetMedicalProductVoList = function () { ... }` | 函数定义 | A |
| 33 | 35729-35754 | `$scope.processBasicData = function () { ... }` | 函数定义 | A |
| 34 | 35755 | `$scope.GetMedicalProductVoList();` | **Init 立即执行** | A |
| 35 | 35756-35767 | `$scope.glassesInfo = { ... }` | Scope 初始化 | A |
| 36 | 35768-35773 | `$scope.showsupplierList = function (...)` | 函数定义 | A |
| 37 | 35774-35804 | `$scope.searchProductList = function (...)` | 函数定义（含 getProductSkuExistCountVoList ListFactory） | A |
| 38 | 35805-35809 | `$scope.setProduct = function (product, key) { ... }` | 函数定义 | A |
| 39 | 35810 | 注释 | - | - |
| 40 | 35812 | 注释 | - | - |
| 41 | 35813 | `$scope.stockInSkuList = [];` | Scope 初始化 | A |
| 42 | 35814-35823 | `$scope.addStore = { ... }` | 对象初始化 | A |
| 43 | 35824-35835 | `$scope.deleteReceipt = function (...)` | 函数定义（含 checkBeforeDeleteMedicalProduct 隐式 Read） | A |
| 44 | 35836-35847 | `$scope.printShoufei = { ... }` | 对象初始化 | A |
| 45 | 35848-35909 | `$scope.queryStore = function (key, key2) { ... }` | 函数定义（含 getProductSkuExistCountVoList ObjectFactory） | A |
| 46 | 35910 | 注释 | - | - |
| 47 | 35911-35957 | `$scope.save = function () { ... }` | 函数定义（含 saveMedicalProductListOfSmallVersion Write） | A |
| 48 | 35958 | `$scope.getMedicalRecord();` | **Init 立即执行** | A |
| 49 | 35959 | `}]);` | Controller 闭合 | A |

### 4.2 初始化 Read DAG

按**真实执行顺序**（Init 立即调用 + then 链）：

```
[0] window.getStockSet(ObjectFactory, "enableNegativeStock")
    └─ then: $scope.enableNegativeStock = !!enableNegativeStock; (L35386)
[1] $scope.GetMethodGlassRecordVo()  (L35623)
    └─ Read: /admin/getMethodGlassRecordVo.json {medicalRecordId: $scope.medicalRecordId}
       └─ then: for-in $scope.object 覆盖 (L35613-L35620)
[2] $scope.queryCompanyName()  (L35682)
    └─ Read: /admin/getCompanyOfMine.json
       └─ then: $scope.company = res.result.object (L35681)
[3] $scope.GetMedicalProductVoList()  (L35755)
    └─ Read: /admin/getMedicalProductVoList.json {medicalRecordId: $scope.medicalRecordId}
       ├─ then: $scope.tempShop = tempList (L35723)
       ├─ then: $scope.stockInSkuList = list (L35724)
       └─ then: $scope.processBasicData()  (L35725 → L35729)
            └─ forEach $scope.tempShop → $scope.glassesInfo 覆盖 (L35741-L35752)
[4] $scope.getMedicalRecord()  (L35958)
    └─ Read: /admin/getMedicalRecord.json {id: $scope.medicalRecordId}
       ├─ then: $scope.medicalRecord = response.object (L35419)
       ├─ then: saleInfo.fn = ...  (L35420-L35432)  ← saleInfo 是 fnMap 风格的可调用对象
       ├─ then: saleInfo.inputVal = $scope.medicalRecord.secondDoctorName (L35433)
       ├─ then: saleInfo.id = $scope.medicalRecord.secondDoctorId (L35434)
       ├─ then: $scope.object.secondDoctorId = saleInfo.id (L35435)
       ├─ then: $scope.saleInfo = saleInfo (L35436)
       └─ then: window.FN_promiseCall(ObjectFactory, [
            { url: "getPatientInfo", param: { id: response.object.patientId } },
            { url: "getCustomerVo", param: { customerId: response.object.customerId } }
          ])  (L35437-L35447)
            └─ then: $scope.userInfo = { ... 15 字段 ... } (L35451-L35466)
```

**关键观察**：
- 4 个 Init 立即执行调用 + 1 个 Init 立即异步调用（`window.getStockSet`）
- `getMedicalRecord` 是**最后**执行的 Init 立即调用（L35958），它依赖 `$scope.medicalRecordId` 已被 L35388 设置
- Init Read 的 4 个主要 Read 之间**无显式依赖关系**（除 medicalRecordId 共同来源）
- `$scope.saleInfo` 与 `$scope.userInfo` 是 `getMedicalRecord` success 内部派生，与 Init 时序无关

---

## 5. API 全量清单

### 5.1 全量 saveOrQuery call site（10 处）

| # | 行号 | API | 类型 | 调用函数 | Request | Success 主要动作 |
|---:|---:|---|---|---|---|---|
| 1 | 35416 | `/admin/getMedicalRecord.json` | Read | `$scope.getMedicalRecord` | `{ id: $scope.medicalRecordId }` | `$scope.medicalRecord = response.object`; `$scope.saleInfo = saleInfo`; `$scope.userInfo = { ... 15 字段 ... }` |
| 2 | 35604 | `/admin/getMethodGlassRecordVo.json` | Read | `$scope.GetMethodGlassRecordVo` | `{ medicalRecordId: $scope.medicalRecordId }` | for-in `$scope.object` 覆盖（含 Date 转换） |
| 3 | 35644 | `/admin/updateMethodGlassRecord.json` | **Write** | `$scope.saveChufang` | `$scope.object`（含 `.medicalRecordId`） | （success 为空，源码 L35645-L35648 注释） |
| 4 | 35662 | `/admin/selectStorehouseListOfCompany.json` | Read | `$scope.queryStorehouseId` | `{ companyId, mcTypeSortType: "ASC" }` | （success 内部细节见 L35663-L35670） |
| 5 | 35675 | `/admin/getCompanyOfMine.json` | Read | `$scope.queryCompanyName` | （无参数） | `$scope.company = res.result.object` |
| 6 | 35685 | `/admin/getMedicalProductVoList.json` | Read | `$scope.GetMedicalProductVoList` | `{ medicalRecordId: $scope.medicalRecordId }` | 分流：`stock.medicalProductSign` truthy → `tempList`；falsy → `list`（含 19 字段映射）；最终 `$scope.tempShop` / `$scope.stockInSkuList` + `$scope.processBasicData()` |
| 7 | 35797 | `/admin/getProductSkuExistCountVoList.json` (ListFactory) | Read | `$scope.searchProductList` | `parmas { keyword, status: 0, brandId, productType: 1, priceFromInclude, priceToInclude, model1, model2, model1Keyword: "", model2Keyword: "" [, categoryId: 1] }` | 无显式 then（仅 nextPage 内 count==0 时 Popup.notice） |
| 8 | 35827 | `/admin/checkBeforeDeleteMedicalProduct.json` | Read | `$scope.deleteReceipt` | `{ medicalProductId }` | `$scope[key].splice(index, 1)` |
| 9 | 35884 | `/admin/getProductSkuExistCountVoList.json` | Read | `$scope.queryStore` | `store { keyword, model1, model2 [, brandId, model1Keyword: "", model2Keyword: "", status: 0, index: 0, length: 1] }`（注：`store.model1`/`store.model2` 当 `key === "3"` 时被 delete） | 分流：count truthy → `$scope.glassesInfo["..."+key]` 写入 4 字段；falsy → 5 字段写 undefined/null |
| 10 | 35950 | `/admin/saveMedicalProductListOfSmallVersion.json` | **Write** | `$scope.save` | `{ medicalRecordId: $scope.medicalRecordId, medicalProductParamListJson: JSON.stringify(...) }` | `$scope.GetMedicalProductVoList()`（刷新 Read） |

### 5.2 全量 window.FN_promiseCall（3 组，共 6 个 API）

| # | 行号 | API | 类型 | 调用上下文 | Request | Success |
|---:|---:|---|---|---|---|---|
| 1 | 35422-35431 | `updateMedicalRecord` | **Write** | `saleInfo.fn`（saleInfo 是 getMedicalRecord success 内的局部 saleInfo 对象的 fn 字段） | `{ id: $scope.medicalRecordId, secondDoctorId: $scope.object.secondDoctorId }` | `$scope.saveChufang()`（链式触发另一 Write） |
| 2 | 35437-35468 | `getPatientInfo` | Read | getMedicalRecord success | `{ id: response.object.patientId }` | `$scope.userInfo.patientId / avatar / patientName / patientGender / patientBirthday / patientRemark / name / gender`（8 字段从 patient） |
| 3 | 35437-35468 | `getCustomerVo` | Read | getMedicalRecord success | `{ customerId: response.object.customerId }` | `$scope.userInfo.customerId / linkMobile / channel / channelTagId / mobile`（5 字段从 customer.customer，$scope.userInfo 共 13 字段去重） |
| 4 | 35532-35542 | `savePatientInfo` | **Write** | `$scope.updatePatient` | `patient`（局部变量，由 $scope.userInfo 分解构造） | `Popup.notice("修改成功!")` |
| 5 | 35532-35542 | `saveCustomerInfo` | **Write** | `$scope.updatePatient` | `customer`（局部变量） | `Popup.notice("修改成功!")`（同一 then） |

### 5.3 API unique 总数

| 类型 | unique 数 | API 列表 |
|---|---:|---|
| Read | 10 | `getMedicalRecord`, `getPatientInfo`, `getCustomerVo`, `getMethodGlassRecordVo`, `selectStorehouseListOfCompany`, `getCompanyOfMine`, `getMedicalProductVoList`, `getProductSkuExistCountVoList` (×2 call sites，1 ListFactory + 1 ObjectFactory), `checkBeforeDeleteMedicalProduct` |
| Write | 5 | `updateMedicalRecord`, `savePatientInfo`, `saveCustomerInfo`, `updateMethodGlassRecord`, `saveMedicalProductListOfSmallVersion` |
| **总计** | **15** | （注：与 call site 10+5 关系 = 10 saveOrQuery + 5 隐式，但 2 个 saveOrQuery 共享 `getProductSkuExistCountVoList`；FN_promiseCall 实际调 5 个 URL：1 个 updateMedicalRecord + 2 个 get* + 2 个 save*） |

**唯一 URL 清单**（无重复）：
1. `/admin/getMedicalRecord.json`
2. `updateMedicalRecord`（无 `.json` 后缀，FN_promiseCall 内部处理）
3. `getPatientInfo`（同上）
4. `getCustomerVo`（同上）
5. `savePatientInfo`（同上）
6. `saveCustomerInfo`（同上）
7. `/admin/getMethodGlassRecordVo.json`
8. `/admin/updateMethodGlassRecord.json`
9. `/admin/selectStorehouseListOfCompany.json`
10. `/admin/getCompanyOfMine.json`
11. `/admin/getMedicalProductVoList.json`
12. `/admin/getProductSkuExistCountVoList.json`
13. `/admin/checkBeforeDeleteMedicalProduct.json`
14. `/admin/saveMedicalProductListOfSmallVersion.json`

**Read/Write 分布**：
- Read unique：9（getMedicalRecord, getPatientInfo, getCustomerVo, getMethodGlassRecordVo, selectStorehouseListOfCompany, getCompanyOfMine, getMedicalProductVoList, getProductSkuExistCountVoList, checkBeforeDeleteMedicalProduct）
- Write unique：5（见上）

### 5.4 call site vs unique 区分

| 维度 | 数量 |
|---|---:|
| saveOrQuery call site | 10 |
| FN_promiseCall call site | 3 组（5 个 URL） |
| ListFactory 构造 | 1（L35797） |
| **call site 总数** | **14** |
| unique API | 14 |
| 重复 API | 1（`getProductSkuExistCountVoList` 在 L35797 ListFactory + L35884 ObjectFactory 两次调用） |

---

## 6. Factory 全量

### 6.1 ObjectFactory

| # | 行号 | 调用 | Factory 实例 | 复用 | 匿名 |
|---:|---:|---|---|---|---|
| 1 | 35416 | getMedicalRecord | `new ObjectFactory()` | 否 | 是 |
| 2 | 35604 | getMethodGlassRecordVo | `new ObjectFactory()` | 否 | 是 |
| 3 | 35644 | updateMethodGlassRecord | `new ObjectFactory()` | 否 | 是 |
| 4 | 35662 | selectStorehouseListOfCompany | `new ObjectFactory()` | 否 | 是 |
| 5 | 35675 | getCompanyOfMine | `new ObjectFactory()` | 否 | 是 |
| 6 | 35685 | getMedicalProductVoList | `new ObjectFactory()` | 否 | 是 |
| 7 | 35827 | checkBeforeDeleteMedicalProduct | `new ObjectFactory()` | 否 | 是 |
| 8 | 35884 | getProductSkuExistCountVoList (queryStore) | `new ObjectFactory()` | 否 | 是 |
| 9 | 35950 | saveMedicalProductListOfSmallVersion | `new ObjectFactory()` | 否 | 是 |

**ObjectFactory 总结**：9 个，全部为匿名 new，每次实例隔离，**无 1 处赋值给 `$scope.xxxFactory`**。

### 6.2 ListFactory

| # | 行号 | 调用 | Factory 实例 | 赋值 | 行号 |
|---:|---:|---|---|---|---|
| 1 | 35797 | getProductSkuExistCountVoList | `new ListFactory("/admin/getProductSkuExistCountVoList.json", 0, 30, parmas)` | `$scope.getCorpListFactory` | 35797 |

**ListFactory 总结**：1 个，命名 `$scope.getCorpListFactory`。

### 6.3 FN_promiseCall 隐式

| # | 行号 | 调用 | 引用 Factory |
|---:|---:|---|---|
| 1 | 35422 | updateMedicalRecord | `ObjectFactory`（DI 注入的） |
| 2 | 35437 | getPatientInfo + getCustomerVo | `ObjectFactory` |
| 3 | 35532 | savePatientInfo + saveCustomerInfo | `ObjectFactory` |

注：`ObjectFactory` 是 DI 注入的同名变量名（来自 L35383 DI 列表），不是 `new ObjectFactory()`。

### 6.4 复用 vs 隔离

- **无 1 个 Factory 被复用**：每次 API 调用均 `new ObjectFactory()` 或 `new ListFactory()`
- **0 处**命名 ObjectFactory 实例（除 L35814 `$scope.addStore` 是对象不是 Factory）
- 唯一的命名 Factory 是 `$scope.getCorpListFactory`（ListFactory 命名）
- 每次调用实例隔离，**不会跨调用共享状态**（pagination/loading 状态等由 ListFactory 内部管理，每次重建）

---

## 7. medicalRecordId 数据链

### 7.1 完整字段路径（5 类，全部 A 级）

| # | 字段路径 | 来源 | 行号 | A-F |
|---:|---|---|---:|---|
| 1 | `$stateParams.medicalRecordId` | optometryCtrl $state.go（beginCustomerCheckin success + fnMap 修改） | L35388 读取 | A |
| 2 | `$scope.medicalRecordId` | StateParams 复制 | L35388 写入 | A |
| 3 | `$scope.object.medicalRecordId` | `=` $scope.medicalRecordId 复制 | L35640 写入 | A |
| 4 | `$scope.printChufang.medicalRecordId` | `=` $scope.medicalRecordId 复制 | L35653 写入 | A |
| 5 | `$scope.addStore.medicalRecordId` | `=` $scope.medicalRecordId 复制 | L35816 写入 | A |

**S1-107 5 类路径回顾（optometryCtrl 范围）**：
1. `item.medicalRecord.id` (fnMap 5 动作 + template.back)
2. `selectOrderListFactory.items[orderIndex].medicalRecord.id` (querySingleOrder)
3. `medicalProduct.medicalRecordId` (modal.changeOrder 报损)
4. `customerCheckin.medicalRecordId` (beginCustomerCheckin success)
5. `$stateParams.medicalRecordId` (optometryGlassesCtrl 入口) ← **本 Controller 入口**

**S1-108 新增路径**（optometryGlassesCtrl 范围内）：
- 路径 2 衍生：`$scope.medicalRecordId`（Controller 入口复制）
- 路径 3 衍生：`$scope.object.medicalRecordId`（用于 updateMethodGlassRecord Write Request）
- 路径 4 衍生：`$scope.printChufang.medicalRecordId`（用于打印处方对象）
- 路径 5 衍生：`$scope.addStore.medicalRecordId`（用于"其他商品"弹窗对象）

### 7.2 $scope.medicalRecordId 全部 Consumer（10 处）

| 行号 | 表达式 | 用途 | A-F |
|---:|---|---|---|
| 35388 | `= $stateParams.medicalRecordId` | 初始化（写入） | A |
| 35417 | `id: $scope.medicalRecordId` | getMedicalRecord.json Request 字段 | A |
| 35425 | `id: $scope.medicalRecordId` | updateMedicalRecord FN_promiseCall Request 字段 | A |
| 35605 | `medicalRecordId: $scope.medicalRecordId` | getMethodGlassRecordVo.json Request 字段 | A |
| 35640 | `$scope.object.medicalRecordId = $scope.medicalRecordId` | $scope.object 复制 | A |
| 35653 | `$scope.printChufang.medicalRecordId = $scope.medicalRecordId` | 打印处方对象复制 | A |
| 35686 | `medicalRecordId: $scope.medicalRecordId` | getMedicalProductVoList.json Request 字段 | A |
| 35816 | `$scope.addStore.medicalRecordId = $scope.medicalRecordId` | "其他商品"弹窗对象复制 | A |
| 35842 | `param: { medicalRecordId: $scope.medicalRecordId, payedStatus: 0 }` | printShoufei.options 静态对象 param 字段 | A |
| 35947 | `medicalRecordId: $scope.medicalRecordId` | saveMedicalProductListOfSmallVersion Request 字段 | A |

### 7.3 medicalRecordId 数据链 DAG

```
[外部入口]
optometryCtrl.beginCustomerCheckin success
  └─ $state.go("optometryGlasses", { medicalRecordId: ... })
       (S1-107 锁定)

optometryCtrl.fnMap "修改"
  └─ $state.go("optometryGlasses", { medicalRecordId: item.medicalRecord.id, edit: "true" })
       (S1-107 锁定)

↓

[Controller 入口]
$stateParams.medicalRecordId (L35388 读取)
  ↓
$scope.medicalRecordId (L35388 写入)
  ↓
  ├─→ $scope.object.medicalRecordId (L35640 写入) → updateMethodGlassRecord Request (L35644)
  ├─→ $scope.printChufang.medicalRecordId (L35653 写入) → 打印处方对象
  ├─→ $scope.addStore.medicalRecordId (L35816 写入) → "其他商品"弹窗
  ├─→ $scope.printShoufei.options[0].param.medicalRecordId (L35842 静态定义) → 收费计算
  └─→ 5 个 Read/Write Request 字段:
       ├─ L35417 getMedicalRecord.json Request
       ├─ L35425 updateMedicalRecord FN_promiseCall Request
       ├─ L35605 getMethodGlassRecordVo.json Request
       ├─ L35686 getMedicalProductVoList.json Request
       └─ L35947 saveMedicalProductListOfSmallVersion Request
```

---

## 8. $scope.medicalRecord 全部 Consumer（4 处）

| 行号 | 表达式 | 用途 | A-F |
|---:|---|---|---|
| 35390 | `$scope.medicalRecord = {};` | Init 初始化为空对象 | A |
| 35419 | `$scope.medicalRecord = response.object;` | getMedicalRecord success 写入完整对象 | A |
| 35433 | `saleInfo.inputVal = $scope.medicalRecord.secondDoctorName;` | 注入到局部 saleInfo 对象 inputVal | A |
| 35434 | `saleInfo.id = $scope.medicalRecord.secondDoctorId;` | 注入到局部 saleInfo 对象 id | A |

**字段消费**（`.` 访问）：
- L35433 `.secondDoctorName`
- L35434 `.secondDoctorId`

**关键观察**：
- `$scope.medicalRecord` 仅 2 个字段被消费：`secondDoctorName` 和 `secondDoctorId`
- 这 2 个字段被立即复制到**局部变量** `saleInfo`（L35555-L35572 定义），**$scope 上不再保留**
- `getMedicalRecord` 返回对象（理论上包含更多字段），但**本 Controller 范围内仅消费这 2 个字段**
- `$scope.medicalRecord` 作为"持久状态"的唯一作用：让 `$scope.saleInfo` 在 success 完成后可被外部（HTML）调用 `saleInfo.fn()` 触发 updateMedicalRecord

**与 optometryCtrl 区别**：
- optometryCtrl 中 `selectOrderListFactory.items[i].medicalRecord` 是**数组元素中的 medicalRecord 字段**，每个元素独立
- 本 Controller 中 `$scope.medicalRecord` 是**单值 Scope**，由 StateParams.medicalRecordId 单点决定

---

## 9. medicalRecordId 派生

### 9.1 Controller 内部派生链

| 层级 | 字段 | 写入位置 | 读取位置 |
|---:|---|---|---|
| L0 | `$stateParams.medicalRecordId` | optometryCtrl $state.go | L35388 |
| L1 | `$scope.medicalRecordId` | L35388 | 9 处（见 7.2） |
| L2 | `$scope.object.medicalRecordId` | L35640 | L35644 Request |
| L2 | `$scope.printChufang.medicalRecordId` | L35653 | （弹窗内部，未追踪） |
| L2 | `$scope.addStore.medicalRecordId` | L35816 | （弹窗内部，未追踪） |
| L2 | `$scope.printShoufei.options[0].param.medicalRecordId` | L35842 | （options 静态） |

**派生规则**：所有 L2 派生都是**Init 立即执行**（L35640 / L35653 / L35816 / L35842 均在 Controller 注册时执行），不依赖任何 Read 完成。

**唯一例外**：L35640 `$scope.object.medicalRecordId = $scope.medicalRecordId` 在 `saveChufang` 函数内部，**调用时**才执行，而非 Init。

### 9.2 与 S1-107 5 类路径的关系

| S1-107 路径 | 出现位置 | 是否在 optometryGlassesCtrl 出现 | 备注 |
|---|---|---|---|
| `item.medicalRecord.id` | optometryCtrl fnMap 5 动作 | 否 | 离开 optometryCtrl 前使用 |
| `selectOrderListFactory.items[].medicalRecord.id` | optometryCtrl querySingleOrder | 否 | 同上 |
| `medicalProduct.medicalRecordId` | optometryCtrl modal.changeOrder 报损 | 否 | 同上 |
| `customerCheckin.medicalRecordId` | optometryCtrl beginCustomerCheckin success | 否 | 作为 $state.go 参数进入 optometryGlasses State |
| `$stateParams.medicalRecordId` | optometryGlassesCtrl 入口 | **是** | 本 Controller 唯一入口 |

**进入 Controller 后**，5 类路径简化为 1 类入口（`$stateParams.medicalRecordId`），其余均为内部派生。

---

## 10. edit 模式

### 10.1 $scope.edit 全部 Consumer（2 处）

| 行号 | 表达式 | 用途 | A-F |
|---:|---|---|---|
| 35389 | `$scope.edit = $stateParams.edit === "true";` | Init 转换 | A |
| 35409 | `$scope.showOtherStore = $scope.edit;` | 复制到 showOtherStore | A |

### 10.2 是否影响 API？

**否**。

证据：
- 全 Controller 搜索 `$scope.edit` 仅 2 处（L35389 定义 + L35409 复制）
- L35409 复制到 `$scope.showOtherStore`，但 Controller 内**无任何代码读取 `$scope.showOtherStore`**（grep 结果 0 处）
- 这意味着 `edit === "true"` 在 Controller 代码层面**仅作为一个标记字段**存在，不影响任何 Read/Write/State 行为
- 实际 UI 行为（显示"其他商品"按钮等）依赖 HTML，但 HTML 当前不可得（F 边界）

### 10.3 与 optometryCtrl 入口的关系

- optometryCtrl 的 fnMap "修改" 动作 → `$state.go("optometryGlasses", { medicalRecordId, edit: "true" })`
- optometryCtrl 的 beginCustomerCheckin success → `$state.go("optometryGlasses", { medicalRecordId })`（**不带 edit**）
- 因此 `$scope.edit === true` 表示用户从"修改"入口进入，`false` 表示从"新增接诊"入口进入
- 但 Controller 业务逻辑并未基于此分流（无任何 if-分支依赖 $scope.edit）

### 10.4 是否存在"新增 vs 修改"的 API 分流？

**否**。

- Controller 5 个 Write（updateMedicalRecord, savePatientInfo, saveCustomerInfo, updateMethodGlassRecord, saveMedicalProductListOfSmallVersion）均**不依赖 $scope.edit**
- 4 个主要 Read（getMedicalRecord, getMethodGlassRecordVo, getMedicalProductVoList, getCompanyOfMine）均**不依赖 $scope.edit**
- $scope.edit 仅影响 `$scope.showOtherStore` 单一字段，且该字段在 Controller 中**0 引用**

**S1-108 关键发现**：optometryCtrl 用 `edit: "true"` 区分入口，optometryGlassesCtrl **未基于此做任何业务分流**。两个 Controller 通过 State 路由形成链式触发，但 optometryGlassesCtrl 内部对"新增"和"修改"是**对称处理**的（除非 HTML 中有 ng-if 分流，F 边界）。

---

## 11. 用户动作函数

### 11.1 分类总览

| 类型 | 函数 | 行号 | 外部入口/内部 helper |
|---|---|---:|---|
| **A. 页面入口** | 无（全部由 StateParams 触发的 Init Read 启动） | - | - |
| **B. 用户动作** | `$scope.tip` | 35391 | 外部入口（HTML ng-click 等） |
| | `$scope.prevent` | 35392-35407 | 外部入口 |
| | `$scope.upOther` | 35410-35412 | 外部入口 |
| | `$scope.showCommon` | 35478-35480 | 外部入口 |
| | `$scope.upimg.call` | 35485-35490 | 外部入口 |
| | `$scope.updateImg` | 35492-35495 | 外部入口（空实现） |
| | `$scope.updatePatient` | 35496-35543 | 外部入口（隐式 Write 触发） |
| | `$scope.update` | 35624-35630 | 外部入口 |
| | `$scope.update2` | 35631-35634 | 外部入口 |
| | `$scope.saveChufang` | 35635-35649 | 外部入口（Write） |
| | `$scope.printChufang.print` | 35658 | 外部入口 |
| | `$scope.queryStorehouseId` | 35661-35671 | 外部入口 |
| | `$scope.queryCompanyName` | 35674-35681 | 外部入口 |
| | `$scope.GetMedicalProductVoList` | 35683-35728 | 外部入口（Init 立即执行 1 次） |
| | `$scope.processBasicData` | 35729-35754 | 内部 helper（被 GetMedicalProductVoList 调用） |
| | `$scope.showsupplierList` | 35768-35773 | 外部入口 |
| | `$scope.searchProductList` | 35774-35804 | 外部入口 |
| | `$scope.setProduct` | 35805-35809 | 外部入口 |
| | `$scope.addStore.switch` | 35817-35819 | 外部入口 |
| | `$scope.addStore.callback` | 35820-35822 | 外部入口（弹窗回调） |
| | `$scope.deleteReceipt` | 35824-35835 | 外部入口（Read 触发） |
| | `$scope.printShoufei.print` | 35844-35846 | 外部入口 |
| | `$scope.queryStore` | 35848-35909 | 外部入口 |
| | `$scope.save` | 35911-35957 | 外部入口（Write） |
| | `$scope.getMedicalRecord` | 35415-35470 | 外部入口（Init 立即执行 1 次） |
| **C. 数据查询** | （同 B，统称 Read 函数） | - | - |
| **D. 数据转换** | `$scope.processBasicData` | 35729-35754 | 内部 helper |
| **E. API helper** | （无独立 helper，每个 Read/Write 都直接调 ObjectFactory） | - | - |
| **F. State 导航** | **0 处** | - | - |
| **G. success helper** | `saleInfo.fn` | 35420-35432 | 内部 helper（saleInfo 是 fnMap 风格） |

**用户动作函数总数**：27 个（不含 saleInfo.fn 与局部 saleInfo 对象）

### 11.2 saleInfo 局部对象详解

```javascript
// L35555-L35572 局部变量定义
var saleInfo = {
  idName: "saleInfo",
  ...
};

// L35420-L35436 getMedicalRecord success 内重新赋值
saleInfo.fn = function () {
  $scope.object.secondDoctorId = this.id;
  window.FN_promiseCall(ObjectFactory, [{
    url: "updateMedicalRecord",
    param: {
      id: $scope.medicalRecordId,
      secondDoctorId: $scope.object.secondDoctorId
    }
  }]).then(function () {
    $scope.saveChufang();
  });
};
saleInfo.inputVal = $scope.medicalRecord.secondDoctorName;
saleInfo.id = $scope.medicalRecord.secondDoctorId;
$scope.object.secondDoctorId = saleInfo.id; //视光师id
$scope.saleInfo = saleInfo;
```

**关键观察**：
- `saleInfo` 是 fnMap 风格对象（`idName: "saleInfo"`），由外部 HTML 通过 `saleInfo.fn()` 触发
- `saleInfo.fn()` 触发时执行 `updateMedicalRecord`（隐式 Write）+ `saveChufang`（显式 Write 链式触发）
- 链式：`saleInfo.fn()` → `updateMedicalRecord` success → `saveChufang()` → `updateMethodGlassRecord.json`

---

## 12. Read → Write

### 12.1 字段级闭合

| Read | Read Result | Write | Write Request 字段来源 | A-F |
|---|---|---|---|---|
| getMedicalRecord | `response.object` | updateMedicalRecord | `id: $scope.medicalRecordId` (源自 StateParams); `secondDoctorId: $scope.object.secondDoctorId` (源自 getMedicalRecord 嵌套 .secondDoctorId) | A |
| getMedicalRecord | `response.object.patientId`, `response.object.customerId` | （无直接 Write 后续，但触发） | - | - |
| getPatientInfo | `res[0].object` | savePatientInfo | `patient`（局部变量，由 $scope.userInfo 分解构造） | A |
| getCustomerVo | `res[1].result.vo` | saveCustomerInfo | `customer`（局部变量） | A |
| getMethodGlassRecordVo | `methodGlassRecord` (for-in $scope.object) | updateMethodGlassRecord | `$scope.object`（含 27+ right*/left* 字段） + `$scope.object.medicalRecordId` (Init L35640 注入) | A |
| getMedicalProductVoList | `res.result.list` (转 $scope.stockInSkuList / $scope.tempShop) | saveMedicalProductListOfSmallVersion | `$scope.medicalRecordId` + `medicalProductParamListJson` (从 $scope.glassesInfo["productSkuId"+i] 1-3 + $scope.stockInSkuList 派生) | A |
| getProductSkuExistCountVoList (queryStore) | `res.result.list[0].productSku` | saveMedicalProductListOfSmallVersion | `$scope.glassesInfo["productSkuKpiPrice"+key]` 写入 medicalProductParamListJson[i].kpiPrice | A |
| selectStorehouseListOfCompany | （未消费到 $scope） | （无） | - | A |
| getCompanyOfMine | `$scope.company` | （无） | - | A |
| checkBeforeDeleteMedicalProduct | （无 Read result 消费） | （无） | - | A |
| getProductSkuExistCountVoList (ListFactory) | （未消费到 $scope） | （无） | - | A |

### 12.2 直接数据链（Read → Scope → Write）

```
[1] getMedicalRecord (L35416)
    └─ $scope.medicalRecord = response.object (L35419)
       └─ $scope.medicalRecord.secondDoctorId → $scope.object.secondDoctorId (L35435)
          └─ updateMedicalRecord Request (L35422-L35431)
             └─ success → $scope.saveChufang() (L35430)
                └─ updateMethodGlassRecord Request (L35644) [Write #2]
                   └─ success (空) (L35645-L35648)

[2] getMethodGlassRecordVo (L35604)
    └─ for-in $scope.object = methodGlassRecord (L35613-L35620)
       └─ $scope.object.medicalRecordId = $scope.medicalRecordId (L35640, in saveChufang)
          └─ updateMethodGlassRecord Request (L35644) [Write 包含]

[3] getMedicalProductVoList (L35685)
    └─ $scope.tempShop + $scope.stockInSkuList (L35723-L35724)
       └─ $scope.processBasicData() (L35725)
          └─ $scope.glassesInfo["..."+signType] = ... (L35741-L35752)
             └─ $scope.save() (L35911-L35957)
                └─ saveMedicalProductListOfSmallVersion Request (L35950) [Write]
                   └─ $scope.medicalRecordId + medicalProductParamListJson (从 glassesInfo + stockInSkuList 派生)
                   └─ success → $scope.GetMedicalProductVoList() (L35955, 刷新 Read)

[4] getPatientInfo + getCustomerVo (L35437-L35447)
    └─ $scope.userInfo (L35451-L35466, 15 字段)
       └─ $scope.updatePatient() (L35496-L35543)
          └─ 分解 userInfo → patient + customer (L35498-L35523)
             └─ savePatientInfo + saveCustomerInfo Request (L35532-L35538) [Write #4 + #5]
                └─ success → Popup.notice("修改成功!") (L35540)
```

---

## 13. Write → Read

### 13.1 全部 Write success 行为

| Write | 行号 | Success 主要动作 | 触发的后续 Read | A-F |
|---|---:|---|---|---|
| updateMethodGlassRecord | 35644 | （空 then，无显式 success 处理，源码 L35645-L35648 注释） | 无 | A |
| saveMedicalProductListOfSmallVersion | 35950 | `Popup.notice("保存成功!")` (L35954) + `$scope.GetMedicalProductVoList()` (L35955) | getMedicalProductVoList (L35685) 刷新 | A |
| updateMedicalRecord | 35422-35431 | `$scope.saveChufang()` (L35430) | updateMethodGlassRecord (L35644) 链式 | A |
| savePatientInfo + saveCustomerInfo | 35532-35538 | `$timeout(() => Popup.notice("修改成功!"), )` (L35539-L35541) | 无 | A |

### 13.2 链式触发

- `updateMedicalRecord` success → `saveChufang` → `updateMethodGlassRecord` 是**链式 2 Write**
- `saveMedicalProductListOfSmallVersion` success → `GetMedicalProductVoList` 是**Write → Read 刷新**

### 13.3 完整 Write → Read 链 DAG

```
[Write #1] updateMedicalRecord (L35422)
  └─ success (L35429) → $scope.saveChufang() (L35430)
       └─ [Write #2] updateMethodGlassRecord (L35644)
            └─ success (空) (L35645-L35648)

[Write #3] savePatientInfo + saveCustomerInfo (L35532)
  └─ success (L35538) → $timeout(Popup.notice) (L35539-L35541)
       └─ 无后续 Read

[Write #4] saveMedicalProductListOfSmallVersion (L35950)
  └─ success (L35950) → Popup.notice (L35954) + $scope.GetMedicalProductVoList() (L35955)
       └─ [Read] getMedicalProductVoList (L35685) 刷新数据
```

---

## 14. Write Request 字段来源矩阵

### 14.1 updateMedicalRecord (L35422-L35431)

| Request 字段 | 来源表达式 | 间接来源 | A-F |
|---|---|---|---|
| `id` | `$scope.medicalRecordId` | `$stateParams.medicalRecordId` (optometryCtrl $state.go) | A |
| `secondDoctorId` | `$scope.object.secondDoctorId` | `$scope.medicalRecord.secondDoctorId` (getMedicalRecord Read) → L35434 → L35435 | A |

### 14.2 savePatientInfo (L35532)

| Request 字段（patient 局部对象） | 来源表达式 | 间接来源 | A-F |
|---|---|---|---|
| `patient` 完整对象 | `patient = { id, name, gender, birthday, avatar, patientRemark }` (L35509-L35516) | `$scope.userInfo.patientId / patientName / patientGender / patientBirthday / avatar / patientRemark` (源自 getPatientInfo Read) | A |

### 14.3 saveCustomerInfo (L35532)

| Request 字段（customer 局部对象） | 来源表达式 | 间接来源 | A-F |
|---|---|---|---|
| `customer` 完整对象 | `customer = { id, linkMobile, channel, channelTagId, name, mobile }` (L35517-L35523) | `$scope.userInfo.customerId / linkMobile / channel / channelTagId / name / mobile` (源自 getCustomerVo Read) | A |

### 14.4 updateMethodGlassRecord (L35644)

| Request 字段（$scope.object） | 来源表达式 | 间接来源 | A-F |
|---|---|---|---|
| `$scope.object` 整体 | Init L35573-L35601 定义（27 right*/left* 字段）+ L35613-L35620 for-in 覆盖（源自 getMethodGlassRecordVo） | Init + Read | A |
| `$scope.object.medicalRecordId` | L35640 `= $scope.medicalRecordId`（在 saveChufang 函数内，调用时执行） | `$stateParams.medicalRecordId` | A |
| `$scope.object.secondDoctorId` | L35435 `= saleInfo.id`（来自 getMedicalRecord Read） | `response.object.secondDoctorId` | A |
| `$scope.object.lastRxTime` | L35641-L35642 若空则 delete | Init L35573-L35601 定义 | A |

### 14.5 saveMedicalProductListOfSmallVersion (L35950)

| Request 字段 | 来源表达式 | 间接来源 | A-F |
|---|---|---|---|
| `medicalRecordId` | L35947 `$scope.medicalRecordId` | `$stateParams.medicalRecordId` | A |
| `medicalProductParamListJson` (1-3) | L35913-L35928 循环 1-3，`productSkuId` truthy 时 push `{ id: null, lockStorehouseId: $scope.lockStorehouseId, productSkuId, memberRate: null, useCount: 1, remark: $scope.glassesInfo["remark"+i], signType: window.optionsObj.glassesSignType[i], kpiPrice: $scope.glassesInfo["productSkuKpiPrice"+i] }` | 1. `$scope.lockStorehouseId` 来自 queryStorehouseId 衍生（**注：L35848-L35909 queryStore 内部未消费到 $scope.lockStorehouseId**；**F 边界**）<br>2. `productSkuId` 来自 queryStore Read（L35899）<br>3. `window.optionsObj.glassesSignType[i]` 来自全局对象<br>4. `kpiPrice` 来自 queryStore Read（L35900）<br>5. `remark` 来自 processBasicData（L35747） | A + 1 F |
| `medicalProductParamListJson` (其他) | L35929-L35941 `$scope.stockInSkuList.forEach`，push `{ id: stock.id, lockStorehouseId: stock.lockStorehouseId, productSkuId: stock.productSkuId, memberRate: stock.memberRate, useCount: stock.useCount, remark: stock.remark, kpiPrice: stock.kpiPrice }` | `$scope.stockInSkuList` 来自 GetMedicalProductVoList Read（L35724） | A |

**F 边界说明**：
- `$scope.lockStorehouseId` 在 `$scope.save` 函数中作为 `lockStorehouseId` 字段写入 Request（L35919），但本 Controller 范围内**0 处赋值给 `$scope.lockStorehouseId`**（grep 结果 0 处）。
- 可能的来源：HTML ng-init / 父 Controller / 全局 window 变量（**F 边界**）。
- 唯一与"storehouseId"相关的语句是 L35862 注释 `// let storehouseId = $scope.glassesInfo['storehouseId${key}'];`（注释，未启用）。

---

## 15. Popup / callback / timeout

### 15.1 Popup.notice 全部调用（9 处）

| 行号 | 触发函数 | 消息 | 条件 | A-F |
|---:|---|---|---|---|
| 35301 | （optometryListCtrl 范围外） | - | - | - |
| 35530 | `$scope.updatePatient` | "请输入正确的手机号" | `customer.linkMobile && !window.Win_VerifyMobile(customer.linkMobile)` | A |
| 35608 | `$scope.GetMethodGlassRecordVo` | `res.errmsg` | `res.status == 1` | A |
| 35638 | `$scope.saveChufang` | "请选择视光师!" | `!$scope.object.secondDoctorId` | A |
| 35645-35648 | `$scope.saveChufang` | （注释，源码未实际执行） | - | - |
| 35667 | `$scope.queryStorehouseId` | "没有仓库!" | `!res.result.list` | A |
| 35689 | `$scope.GetMedicalProductVoList` | `res.errmsg` | `res.status == 1` | A |
| 35801 | `$scope.searchProductList` | "没有该规格的商品" | `!res.count` | A |
| 35831 | `$scope.deleteReceipt` | `res.errmsg` | `res.status == 1` | A |
| 35886 | `$scope.queryStore` | `res.errmsg` | `res.status == 1` | A |
| 35943 | `$scope.save` | "请添加商品！" | `!medicalProductParamListJson.length` | A |
| 35952 | `$scope.save` | `res.errmsg` | `res.status == 1` | A |
| 35954 | `$scope.save` | "保存成功!" | success | A |
| 35540 | `$scope.updatePatient` | "修改成功!" | success（L35539-L35541 `$timeout` 内） | A |

**Popup.notice 总结**：13 处（9 函数 + 2 处与上一轮 optometryListCtrl 混淆，**实际 optometryGlassesCtrl 范围内 11 处**）。

### 15.2 $timeout 调用（3 处）

| 行号 | 触发函数 | 内容 | 用途 | A-F |
|---:|---|---|---|---|
| 35448-35467 | `$scope.getMedicalRecord` (success) | `$scope.userInfo = { ... }` | 延迟赋值（与 saleInfo 类似） | A |
| 35486-35490 | `$scope.upimg.call` | （img 处理） | 延迟触发 img callback | A |
| 35539-35541 | `$scope.updatePatient` (success) | `Popup.notice("修改成功!")` | 延迟提示 | A |

### 15.3 window.FN_promiseCall 全部调用（3 组）

| 行号 | URL | 类型 | 行号细节 | A-F |
|---:|---|---|---|---|
| 35422-35431 | `updateMedicalRecord` | **Write** | L35422 启动，L35429 then → $scope.saveChufang() | A |
| 35437-35468 | `getPatientInfo`, `getCustomerVo` | Read | L35437 启动，L35447 then → $scope.userInfo | A |
| 35532-35542 | `savePatientInfo`, `saveCustomerInfo` | **Write** | L35532 启动，L35538 then → Popup.notice | A |

### 15.4 window. 其它调用

| 行号 | 调用 | 用途 | A-F |
|---:|---|---|---|
| 35385 | `window.getStockSet(ObjectFactory, "enableNegativeStock")` | 读取全局库存设置 | A |
| 35529 | `window.Win_VerifyMobile(customer.linkMobile)` | 手机号校验 | A |
| 35547-35554 | `window.optionsObj.getQiuJing / getEyeDistance / sightArr` | 工具变量初始化 | A |
| 35924 | `window.optionsObj.glassesSignType[i]` | 写入 saveMedicalProductListOfSmallVersion Request | A |

### 15.5 callback / promise

- `Popup.notice(msg, duration, callback)` 形式未在本 Controller 出现（所有 Popup.notice 都是 1 参数或 2 参数）
- $timeout(fn, 0) 用于延迟（3 处，见 15.2）
- `ObjectFactory.saveOrQuery().then(...)` 链式 10 处
- `ListFactory.nextPage().then(...)` 链式 1 处
- `window.FN_promiseCall(ObjectFactory, [...]).then(...)` 链式 3 处

---

## 16. State 出口

### 16.1 optometryGlassesCtrl 范围内 $state.go 搜索

**0 处**。

证据：
```powershell
Select-String -Path 'controller.js' -Pattern '\$state\.go|\$stateParams' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

输出（精简）：
```
35383: angular.module("bestvisionWeb").controller("optometryGlassesCtrl", [...])
35388: $scope.medicalRecordId = $stateParams.medicalRecordId;
35389: $scope.edit = $stateParams.edit === "true";
```

**0 个 $state.go** + **2 个 $stateParams**（仅 Init 时读取）。

### 16.2 离开页面的其它机制（F 边界）

本 Controller 范围内**0 处**：
- `$state.go`（已验证 0）
- `window.open`
- `location.href`
- `window.location`

可能的离开机制（**F 边界**，HTML 不可得）：
- HTML 中 `<a ui-sref="...">` 链接
- HTML 中 `ng-click="$state.go(...)"`（不可能，因为 Controller 内无 $state 注入）
- HTML 中 `window.location.href = ...`

### 16.3 optometryList / optometryLogList 在 optometryGlassesCtrl 范围内

**0 处**。

证据：
```powershell
Select-String -Path 'controller.js' -Pattern 'optometryList|optometryLogList' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

输出：（无）

**S1-107 错误纠正**：
- S1-107 矩阵第 23 项曾将 L36034 / L36050 列为 optometryGlassesCtrl 出口
- S1-108 重新审计：L36034 / L36050 **在 optometryListCtrl 范围内**（L35962+），**不在 optometryGlassesCtrl 范围内**（L35383-L35959）
- optometryGlassesCtrl **0 个 State 出口**（A 级确认）

---

## 17. optometryList

### 17.1 接收方 Controller

- Controller 名：`optometryListCtrl`
- 注册位置：`controller.js` L35962
- DI：`$scope, Popup, HttpFactory, $state, ObjectFactory, ListFactory, $timeout`
- 与 optometryGlassesCtrl 区别：注入 `$state` 和 `HttpFactory`，不注入 `$stateParams`

### 17.2 在 optometryGlassesCtrl 范围

**0 处**（见 16.3）。

optometryGlassesCtrl 不调用 `optometryList` State。

### 17.3 S1-107 锁定内容（S1-108 不再展开）

S1-107 已确认：
- L36034 `$state.go("optometryList", {}, { reload: true })` 在 `$scope.confirm`（optometryListCtrl 内部）
- 这是 optometryListCtrl **自跳转**（refresh），不是从 optometryGlassesCtrl 进入

**S1-108 边界**：不进入 optometryListCtrl 内部 API 逆向，仅确认 optometryGlassesCtrl → optometryList 链 0 处。

---

## 18. optometryLogList

### 18.1 接收方 Controller

- Controller 名：`optometryLogListCtrl`
- 注册位置：`controller.js` L35899
- DI：`$scope, Popup, $stateParams, $interval, $rootScope, $state, ObjectFactory, ListFactory`
- 第一个 `$stateParams` Consumer：L35902 `$scope.obj.uartDeviceId = $stateParams.uartDeviceId;`

### 18.2 在 optometryGlassesCtrl 范围

**0 处**（见 16.3）。

optometryGlassesCtrl 不调用 `optometryLogList` State。

### 18.3 S1-107 锁定内容（S1-108 不再展开）

S1-107 已确认：
- L36050 `$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })` 在 `$scope.lookLog`（optometryListCtrl 内部）
- 这是 optometryListCtrl → optometryLogList 单向跳转

**S1-108 边界**：不进入 optometryLogListCtrl 内部 API 逆向，仅确认 optometryGlassesCtrl → optometryLogList 链 0 处。

---

## 19. Scope 分桶

按功能将 `$scope.xxx` 分桶：

### 19.1 A. 主数据

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.medicalRecord` | 35390, 35419, 35433, 35434 | Object | 2 字段被消费（secondDoctorName, secondDoctorId） |
| `$scope.medicalRecordId` | 35388 + 9 处 | String/Number | 9 处下游消费 |
| `$scope.company` | 35681 | Object | getCompanyOfMine success 赋值 |

### 19.2 B. 编辑状态

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.edit` | 35389, 35409 | Boolean | 仅复制到 showOtherStore，0 引用 |
| `$scope.showOtherStore` | 35409 | Boolean | 0 引用（F 边界：HTML 可能消费） |
| `$scope.showPerfectInfo` | 35413 | Boolean | 0 引用（F 边界：HTML 可能消费） |
| `$scope.enableNegativeStock` | 35384, 35386 | Boolean | window.getStockSet 异步赋值；0 引用（F 边界） |

### 19.3 C. 页面列表

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.tempShop` | 35672, 35723, 35730 | Array | GetMedicalProductVoList 写入；processBasicData 消费 |
| `$scope.stockInSkuList` | 35724, 35813, 35821, 35833 | Array | save Request 来源 |
| `$scope.glassesInfo` | 35741-35767, 35792 等 | Object | 大量 `"..." + signType/num` 键 |
| `$scope.userInfo` | 35414, 35451-35466 | Object | 15 字段；updatePatient 消费 |
| `$scope.object` | 35421, 35426, 35435, 35573-35601, 35613-35620, 35625, 35626, 35632, 35637, 35640, 35641, 35763-35766 | Object | 27+ right*/left* 字段 + medicalRecordId + secondDoctorId + lastRxTime；updateMethodGlassRecord Request |
| `$scope.saleInfo` | 35436 | Object（fnMap 风格） | 由 HTML 触发 saleInfo.fn() |

### 19.4 D. 表单/检查/产品

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.qiuJingArr` | 35547 | Array | window.optionsObj.getQiuJing 派生 |
| `$scope.eyeDistanceArr` | 35550 | Array | 同上 |
| `$scope.eyeDistanceArr2` | 35551 | Array | 同上 |
| `$scope.sightArr` | 35552 | Array | window.optionsObj.sightArr |
| `$scope.odArr` | 35553 | Array | 同上 |
| `$scope.tallArr` | 35554 | Array | 同上 |

### 19.5 E. 弹窗

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.dateCom` | 35471-35477 | Object | show/open 函数 |
| `$scope.upimg` | 35481-35491 | Object | show/img/call 函数 |
| `$scope.printChufang` | 35650-35657 | Object | show/hiddenLen/medicalRecordId/print |
| `$scope.addStore` | 35814-35823 | Object | show/medicalRecordId/switch/callback |
| `$scope.printShoufei` | 35836-35847 | Object | show/title/daishou/options/print |

### 19.6 F. 工具/其它

| 字段 | 行号 | 类型 | 备注 |
|---|---|---|---|
| `$scope.tip` | 35391 | Function | 空实现 |
| `$scope.prevent` | 35392-35407 | Function | 内部循环 supplierList |
| `$scope.upOther` | 35410-35412 | Function | key 操作 |
| `$scope.showCommon` | 35478-35480 | Function | 切换 show 状态 |
| `$scope.updateImg` | 35492-35495 | Function | 空实现 |
| `$scope.showsupplierList` | 35768-35773 | Function | 触发 searchProductList |
| `$scope.searchProductList` | 35774-35804 | Function | ListFactory 调用 |
| `$scope.setProduct` | 35805-35809 | Function | 触发 queryStore |
| `$scope.getCorpListFactory` | 35797 | ListFactory 实例 | 命名 |

**总计**：约 30+ $scope 字段/对象/函数。

---

## 20. Scope 共享

### 20.1 共享 Scope 字段

| Scope | 共享函数（在本 Controller 调用） | 行号 | A-F |
|---|---|---|---|
| `$scope.medicalRecordId` | getMedicalRecord (L35417), updateMedicalRecord (L35425), getMethodGlassRecordVo (L35605), GetMethodGlassRecordVo (L35605), $scope.object.medicalRecordId (L35640), $scope.printChufang.medicalRecordId (L35653), GetMedicalProductVoList (L35686), $scope.addStore.medicalRecordId (L35816), printShoufei (L35842), save (L35947) | 见 7.2 | A |
| `$scope.medicalRecord` | 仅 4 处（init + getMedicalRecord success + 2 字段消费） | 35390, 35419, 35433, 35434 | A |
| `$scope.edit` | 仅 2 处（init + showOtherStore 复制） | 35389, 35409 | A |
| `$scope.object` | getMedicalRecord success (L35421, 35426, 35435), GetMethodGlassRecordVo (L35613-35620), update (L35625, 35626), update2 (L35632), saveChufang (L35637, 35640, 35641), glassesInfo (L35763-L35766) | 多处 | A |
| `$scope.glassesInfo` | processBasicData (L35741-L35752), searchProductList (L35778-L35793), setProduct (L35806-L35807), queryStore (L35849-L35907), save (L35915-L35925) | 多处 | A |
| `$scope.tempShop` | GetMedicalProductVoList (L35723), processBasicData (L35730) | 2 处 | A |
| `$scope.stockInSkuList` | GetMedicalProductVoList (L35724), addStore.callback (L35821), deleteReceipt (L35833), save (L35929) | 4 处 | A |
| `$scope.userInfo` | getMedicalRecord success (L35451-L35466), updatePatient (L35498-L35507) | 2 处 | A |
| `$scope.company` | queryCompanyName (L35681) | 1 处 | A |
| `$scope.saleInfo` | getMedicalRecord success (L35436) → 外部 HTML 触发 saleInfo.fn() | 1 处写 | A |

### 20.2 不共享 Scope 的局部变量

| 局部变量 | 行号 | 用途 | A-F |
|---|---|---|---|
| `saleInfo`（局部） | 35555-35572 | L35420-L35436 重新赋值的 `fn/inputVal/id/fn` 字段 | A |
| `patient`（局部） | 35509-35516 | updatePatient 内构造，传给 savePatientInfo | A |
| `customer`（局部） | 35517-35523 | updatePatient 内构造，传给 saveCustomerInfo | A |
| `parmas` | 35782-35793 | searchProductList 内构造，传给 ListFactory | A |
| `store` | 35863-35883 | queryStore 内构造，传给 ObjectFactory | A |
| `medicalProductParamListJson` | 35912-35945 | save 内构造，JSON.stringify 后传给 Write | A |
| `list` | 35692, 35698-35720 | GetMedicalProductVoList 内 forEach 派生 | A |
| `tempList` | 35693, 35695-35697 | 同上 | A |
| `stock` | 35694-35722 | 同上 | A |
| `brand`, `medicalProduct`, `medicalProductSign`, `unLockExistSkuCount`, `lockStorehouse`, `product`, `productSku` | 35731-35737 | processBasicData 内 forEach 解构 | A |
| `signType` | 35739-35752 | processBasicData 内计算 | A |
| `unLockExistSkuCount`, `productSku` | 35893-35900 | queryStore 内解构 | A |

**关键观察**：
- `$scope.medicalRecordId` 是**核心共享字段**，被 9 处下游函数/对象引用
- `$scope.medicalRecord` 是**窄共享**：仅 2 字段（secondDoctorName, secondDoctorId）被消费
- `$scope.edit` 是**极窄共享**：仅复制到 showOtherStore（F 边界）
- 局部变量严格隔离：每个函数/区块使用独立的局部变量，不跨函数共享（除 saleInfo 由 L35555 局部定义 + L35420 重新赋值）

---

## 21. optometryCtrl vs optometryGlassesCtrl

| 项目 | optometryCtrl (S1-105/106/107) | optometryGlassesCtrl (S1-108) | A-F |
|---|---|---|---|
| 注册位置 | L34776 | L35383 | A |
| 所属 module | bestvisionWeb | bestvisionWeb | A |
| DI 列表 | `$scope, Popup, $state, ObjectFactory, ListFactory, $timeout, DateUtilFactory`（7 个） | `$scope, Popup, utilFactory, ObjectFactory, ListFactory, $timeout, $stateParams`（7 个） | A |
| 是否注入 `$state` | 是 | **否** | A |
| 是否注入 `$stateParams` | **否** | 是 | A |
| 是否注入 `DateUtilFactory` | 是 | **否** | A |
| 是否注入 `utilFactory` | **否** | 是 | A |
| `$stateParams` 出现次数 | 0 | 2 | A |
| `$state.go` 出现次数 | 多处（含 optometryGlasses 出口） | **0** | A |
| unique API | 16 | **14** | A |
| Read unique | 8 | **9** | A |
| Write unique | 8 | **5** | A |
| medicalRecordId 来源 | customerCheckin.medicalRecordId / item.medicalRecord.id | **$stateParams.medicalRecordId** | A |
| 主数据对象 | `$scope.order` / `$scope.medicalRecord` (optometryCtrl 内层级) | `$scope.medicalRecord`（单值）/ `$scope.object` | A |
| State 入口 | optometryList（外部） | **optometryGlasses**（外部） | A |
| State 出口 | `optometryGlasses` (beginCustomerCheckin success) | **0** | A |
| 隐式 Write 机制 | template.back (`sendTakeMirrorNotice`) | **saleInfo.fn (`updateMedicalRecord`)** | A |
| 写新文档编号 | 154-168（S1-87~S1-107） | 169 (S1-108) | - |

**关键对比**：
- 两个 Controller 互为上下游：
  - optometryCtrl → `$state.go("optometryGlasses", { medicalRecordId })` → optometryGlassesCtrl
  - optometryGlassesCtrl → （0 个 $state.go 出口）
- optometryGlassesCtrl 接收 medicalRecordId 后进行**单值定位**（基于 ID 加载完整医疗记录）
- optometryCtrl 接收的是**数组上下文**（selectOrderListFactory.items 列表）

**共同点**：
- 同一 module `bestvisionWeb`
- 注入 `Popup, ObjectFactory, ListFactory, $timeout`
- 5 个以上 API 调用
- 隐式 Write 机制（template.back / saleInfo.fn）

**区别点**：
- optometryCtrl 注入 `$state` 和 `DateUtilFactory`；optometryGlassesCtrl 注入 `$stateParams` 和 `utilFactory`
- optometryCtrl 16 API（8 Read + 8 Write）；optometryGlassesCtrl 14 API（9 Read + 5 Write）
- optometryCtrl 有出口；optometryGlassesCtrl 无出口（**单向接收**）

---

## 22. 页面级完整 DAG

### 22.1 入口链

```
[optometryCtrl beginCustomerCheckin success]            (S1-106 锁定)
  ↓ $state.go("optometryGlasses", { medicalRecordId })
[optometryCtrl fnMap "修改"]                              (S1-107 锁定)
  ↓ $state.go("optometryGlasses", { medicalRecordId, edit: "true" })

↓

[optometryGlasses State]  (F 边界：State 配置不在 controller.js)
  ↓

[optometryGlassesCtrl]    (L35383, DI: $stateParams)
  ├─ $stateParams.medicalRecordId → $scope.medicalRecordId (L35388)
  ├─ $stateParams.edit === "true" → $scope.edit (L35389)
  └─ $scope.medicalRecord = {} (L35390)
```

### 22.2 Init Read 链

```
[1] window.getStockSet (L35385) 异步
    └─ $scope.enableNegativeStock (L35386)

[2] $scope.GetMethodGlassRecordVo() (L35623 立即)
    └─ Read: getMethodGlassRecordVo.json
       └─ for-in $scope.object 覆盖 (L35613)

[3] $scope.queryCompanyName() (L35682 立即)
    └─ Read: getCompanyOfMine.json
       └─ $scope.company (L35681)

[4] $scope.GetMedicalProductVoList() (L35755 立即)
    └─ Read: getMedicalProductVoList.json
       ├─ $scope.tempShop (L35723)
       ├─ $scope.stockInSkuList (L35724)
       └─ $scope.processBasicData() (L35725)
            └─ $scope.glassesInfo 覆盖 (L35741-L35752)

[5] $scope.getMedicalRecord() (L35958 立即)
    └─ Read: getMedicalRecord.json
       ├─ $scope.medicalRecord (L35419)
       ├─ saleInfo.fn (L35420-L35432)  ← 隐式 Write 触发器
       ├─ saleInfo.inputVal/id (L35433-L35434)
       ├─ $scope.object.secondDoctorId (L35435)
       ├─ $scope.saleInfo (L35436)
       └─ window.FN_promiseCall getPatientInfo + getCustomerVo (L35437)
            └─ $scope.userInfo (L35451-L35466)
```

### 22.3 用户动作 → Read/Write 链

```
[动作 A] HTML 触发 saleInfo.fn() (外部 HTML，F 边界)
    └─ [Write #1] updateMedicalRecord (L35422)
         └─ success → $scope.saveChufang() (L35430)
              └─ [Write #2] updateMethodGlassRecord (L35644)

[动作 B] HTML 触发 $scope.updatePatient() (外部 HTML，F 边界)
    └─ 校验 customer.linkMobile (L35529)
    └─ 构造 patient + customer 局部对象 (L35509-L35523)
    └─ [Write #3] savePatientInfo (L35532)
    └─ [Write #4] saveCustomerInfo (L35532)
         └─ success → Popup.notice("修改成功!") (L35540)

[动作 C] HTML 触发 $scope.save() (外部 HTML，F 边界)
    └─ 构造 medicalProductParamListJson (L35912-L35945)
    └─ [Write #5] saveMedicalProductListOfSmallVersion (L35950)
         └─ success → Popup.notice (L35954) + $scope.GetMedicalProductVoList() (L35955)
              └─ [Read] getMedicalProductVoList 刷新

[动作 D] HTML 触发 $scope.saveChufang() (外部 HTML，F 边界)
    └─ 校验 $scope.object.secondDoctorId (L35637)
    └─ $scope.object.medicalRecordId = $scope.medicalRecordId (L35640)
    └─ [Write #2] updateMethodGlassRecord (L35644)

[动作 E] HTML 触发 $scope.deleteReceipt(index, medicalProductId) (外部 HTML，F 边界)
    └─ [Read] checkBeforeDeleteMedicalProduct (L35827)
         └─ $scope[key].splice(index, 1) (L35833)

[动作 F] HTML 触发 $scope.queryStore(key) (外部 HTML，F 边界)
    └─ [Read] getProductSkuExistCountVoList (L35884)
         └─ $scope.glassesInfo 覆盖 4-5 字段 (L35897-L35906)

[动作 G] HTML 触发 $scope.searchProductList(keyword, num) (外部 HTML，F 边界)
    └─ 构造 parmas (L35782-L35793)
    └─ [ListFactory] getProductSkuExistCountVoList (L35797)
         └─ then: !res.count → Popup.notice (L35799-L35802)

[动作 H] HTML 触发 $scope.setProduct(product, key) (外部 HTML，F 边界)
    └─ $scope.glassesInfo 写入 (L35806-L35807)
    └─ $scope.queryStore(key) (L35808)
```

### 22.4 State 出口

**0 处**（A 级确认）。

可能离开方式（**F 边界**）：
- HTML `<a ui-sref="...">` 链接
- HTML ng-click 触发全局函数 / 父 Controller 函数
- 浏览器后退按钮

---

## 23. 26 项增量矩阵

| # | 审计项 | 文件 | 行号 | 证据等级 | L1/L2/L3 | 备注 |
|---:|---|---|---:|---|---|---|
| 01 | Controller 注册 | controller.js | 35383 | A | L1 | `optometryGlassesCtrl` 注册 |
| 02 | DI | controller.js | 35383 | A | L1 | 7 个 DI（$scope/Popup/utilFactory/ObjectFactory/ListFactory/$timeout/$stateParams） |
| 03 | Controller 行范围 | controller.js | 35383-35959 | A | L1 | 577 行 |
| 04 | $stateParams 全集 | controller.js | 35388, 35389 | A | L1 | 2 处（medicalRecordId, edit） |
| 05 | medicalRecordId 初始化 | controller.js | 35388 | A | L1 | `= $stateParams.medicalRecordId` |
| 06 | edit 初始化 | controller.js | 35389 | A | L1 | `=== "true"` 强比较 |
| 07 | 初始化 Read | controller.js | 35623, 35682, 35755, 35958 | A | L1 | 4 个 Init 立即执行 + 1 个 Init 异步（window.getStockSet） |
| 08 | API unique | controller.js | 见 5.3 | A | L2 | 14 unique |
| 09 | API call site | controller.js | 见 5.1, 5.2 | A | L2 | 14 call site |
| 10 | Read unique | controller.js | 见 5.3 | A | L2 | 9 unique |
| 11 | Write unique | controller.js | 见 5.3 | A | L2 | 5 unique |
| 12 | Factory 总量 | controller.js | 见 6.1, 6.2 | A | L2 | 9 ObjectFactory + 1 ListFactory + 3 FN_promiseCall |
| 13 | medicalRecord Scope | controller.js | 35390, 35419, 35433, 35434 | A | L2 | 4 处（init + getMedicalRecord success + 2 字段消费） |
| 14 | medicalRecord Consumer | controller.js | 35433, 35434 | A | L3 | 2 字段（secondDoctorName, secondDoctorId） |
| 15 | medicalRecordId 派生 | controller.js | 见 7.2 | A | L2 | 5 类路径（5 个 L2 派生） |
| 16 | edit Consumer | controller.js | 35409 | A | L2 | 1 字段（showOtherStore），0 引用 |
| 17 | 用户动作函数 | controller.js | 见 11.1 | A | L2 | 27 个 |
| 18 | Write 字段来源 | controller.js | 见 14 | A | L3 | 5 个 Write 全部字段闭合 |
| 19 | Read → Write | controller.js | 见 12 | A | L3 | 4 条直接数据链 |
| 20 | Write → Read | controller.js | 见 13 | A | L3 | 1 条 Write → Read 刷新（save → GetMedicalProductVoList） |
| 21 | Popup/callback | controller.js | 见 15.1, 15.5 | A | L2 | 11 处 Popup.notice + 0 处 callback（3 Popup） |
| 22 | $timeout | controller.js | 35448, 35486, 35539 | A | L2 | 3 处 |
| 23 | State 出口 | controller.js | 0 处 | A | L1 | **0 个 $state.go**（A 级确认） |
| 24 | optometryList | controller.js | 0 处 | A | L1 | optometryGlassesCtrl 内 0 引用 |
| 25 | optometryLogList | controller.js | 0 处 | A | L1 | optometryGlassesCtrl 内 0 引用 |
| 26 | A/B/C/D/E/F | - | - | A: 26 / B: 0 / C: 0 / D: 0 / E: 0 / F: 3 | - | F 项见 26.1 |

### 23.1 F 项汇总

| F 项 | 原因 |
|---|---|
| `$scope.lockStorehouseId` 来源 | 本 Controller 范围内 0 处赋值（L35919 引用但无写入），F 边界 |
| optometryGlasses State 配置 | controller.js 0 处 `.state()` 注册，State 配置不在本资源范围 |
| HTML 触发函数 | 7 untracked HTML 中 0 处 optometry 模板 |

### 23.2 A/B/C/D/E 分布

- **A 级**：26 项中的 23 项（除 26.1 F 项）
- **B 级**：0 项
- **C 级**：0 项
- **D 级**：0 项
- **E 级**：0 项（**严禁 E 升 A**）
- **F 级**：3 项

---

## 24. A-F

按矩阵编号简表：

| # | 项 | 等级 |
|---:|---|---|
| 01 | Controller 注册 | A |
| 02 | DI | A |
| 03 | Controller 行范围 | A |
| 04 | $stateParams 全集 | A |
| 05 | medicalRecordId 初始化 | A |
| 06 | edit 初始化 | A |
| 07 | 初始化 Read | A |
| 08 | API unique | A |
| 09 | API call site | A |
| 10 | Read unique | A |
| 11 | Write unique | A |
| 12 | Factory 总量 | A |
| 13 | medicalRecord Scope | A |
| 14 | medicalRecord Consumer | A |
| 15 | medicalRecordId 派生 | A |
| 16 | edit Consumer | A |
| 17 | 用户动作函数 | A |
| 18 | Write 字段来源 | A |
| 19 | Read → Write | A |
| 20 | Write → Read | A |
| 21 | Popup/callback | A |
| 22 | $timeout | A |
| 23 | State 出口 | A |
| 24 | optometryList | A |
| 25 | optometryLogList | A |
| 26 | A/B/C/D/E/F | A |

---

## 25. L1/L2/L3

| 级别 | 含义 | 项数 | 项 |
|---|---|---:|---|
| L1 | Controller 注册层（行范围、DI、$stateParams 入口、State 出口） | 5 | 01, 02, 03, 04, 23, 24, 25 |
| L2 | Controller 内部层（API、Factory、Scope、用户动作、Popup、timeout） | 13 | 05, 06, 07, 08, 09, 10, 11, 12, 13, 15, 16, 17, 21, 22 |
| L3 | 字段级层（medicalRecord 字段、Write 字段、Read→Write、Write→Read） | 4 | 14, 18, 19, 20 |

---

## 26. F 边界

| F 项 | 详情 |
|---|---|
| 1 | `$scope.lockStorehouseId` 在 `save` 函数（L35919）作为 Write Request 字段被引用，但本 Controller 范围内**0 处赋值**。可能来源：HTML ng-init / 父 Controller / 全局 window 变量 |
| 2 | optometryGlasses State 配置（url / template / templateUrl / params / resolve）不在 controller.js 资源范围 |
| 3 | 7 untracked HTML 中 0 处 optometry 模板，HTML 触发函数（`saleInfo.fn()` / `$scope.updatePatient()` / `$scope.save()` / `$scope.saveChufang()` / `$scope.deleteReceipt()` / `$scope.queryStore()` / `$scope.searchProductList()` / `$scope.setProduct()` 等）证据不可得 |
| 4 | `$scope.showOtherStore` / `$scope.showPerfectInfo` / `$scope.enableNegativeStock` 在 Controller 范围内 0 引用，可能由 HTML ng-if / ng-show 消费 |
| 5 | 离开 optometryGlassesCtrl 的具体方式（`<a ui-sref>` / `window.location` / 浏览器后退）不可得 |

---

## 27. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态审计 | ✅ |
| 2. API actual | 0（无任何 F5/F6/FN_promiseCall 实际调用） |
| 3. Write actual | 0 |
| 4. 不打开真实业务页面 | ✅ |
| 5. 不执行业务动作 | ✅ |
| 6. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-107 一致） |
| 7. 不修改 7 HTML | ✅ |
| 8. 不修改历史 MD（154-168） | ✅ |
| 9. P0 = 54 冻结 | ✅ |
| 10. P1 = 8 冻结 | ✅ |
| 11. 10 untracked 原样保留 | ✅ |
| 12. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 28. 最终结论

### 28.1 核心发现

1. **Controller 边界确认**：
   - optometryGlassesCtrl 范围 L35383-L35959（577 行）
   - DI 7 个：$scope, Popup, utilFactory, ObjectFactory, ListFactory, $timeout, $stateParams
   - 注入 `$stateParams`（与 optometryCtrl 的 `$state` 区别明显）

2. **API 矩阵**：
   - unique API 14 个
   - call site 14 个
   - Read 9 unique / Write 5 unique
   - 与 optometryCtrl（16 unique / 8 Read + 8 Write）对比：Read 略多（+1），Write 减少（-3）

3. **medicalRecordId 数据链完整闭合**：
   - 入口：`$stateParams.medicalRecordId` (L35388) → `$scope.medicalRecordId` (L35388)
   - 9 处下游消费（5 个 Read/Write Request + 4 个对象派生）
   - 5 类派生路径全部 A 级
   - 与 S1-107 的 5 类路径关系清晰（optometryCtrl 内部 4 类 + optometryGlassesCtrl 入口 1 类）

4. **edit 模式对称处理**：
   - `$scope.edit` 仅复制到 `$scope.showOtherStore`，**不影响任何 API/State 行为**
   - "新增" vs "修改" 入口业务逻辑对称（F 边界：HTML 可能基于此分流 UI）

5. **隐式 Write 机制**：
   - `saleInfo.fn()` 触发 `updateMedicalRecord`（隐式 Write）→ `saveChufang`（显式 Write 链式）
   - `updatePatient()` 触发 `savePatientInfo` + `saveCustomerInfo`（隐式 Write）

6. **State 出口 0 处（A 级确认）**：
   - 全 Controller 范围 0 处 `$state.go`
   - S1-107 错误纠正：L36034 / L36050 `$state.go` 在 optometryListCtrl 范围内（L35962+），不在 optometryGlassesCtrl 范围内（L35383-L35959）
   - optometryGlassesCtrl 是**单向接收** Controller，离开方式由 HTML 决定（F 边界）

7. **F 边界 5 项**：
   - `$scope.lockStorehouseId` 来源
   - optometryGlasses State 配置
   - HTML 触发函数
   - `$scope.showOtherStore` / `$scope.showPerfectInfo` / `$scope.enableNegativeStock` 消费
   - 离开页面的具体方式

### 28.2 与前序 S1-* 关系

| S1-* | 关系 | 本轮贡献 |
|---|---|---|
| S1-105 | optometryCtrl API 矩阵 | 对比：optometryGlassesCtrl 14 unique vs optometryCtrl 16 unique |
| S1-106 | 3 个新 Write 锁定 | 验证：beginCustomerCheckin → optometryGlasses 链在本 Controller 入口闭合 |
| S1-107 | optometryCtrl 外部调用者 | 验证：optometryGlassesCtrl 接收方 0 个 State 出口 |
| S1-108 | optometryGlassesCtrl 完整 Controller 审计 | **本轮** |

### 28.3 不再发散

- **不进入** optometryListCtrl 内部 API 逆向（仅确认 0 引用）
- **不进入** optometryLogListCtrl 内部 API 逆向（仅确认 0 引用）
- **不重新审计** optometryCtrl（已在 S1-105/106/107 完成）
- **不修改** 历史 MD（154-168）

---

**审计完成。本文档为 169 号，提交后将形成 tracked=178。**
