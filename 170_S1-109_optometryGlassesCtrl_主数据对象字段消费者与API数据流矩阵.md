# S1-109 optometryGlassesCtrl 主数据对象、字段消费者与 API 数据流矩阵

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML（无 optometry 模板，F 边界）
> - Controller 范围：L35383 – L35959（577 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-108（HEAD=c10f296，tracked=178）
> - 本轮**重新从源码统计**，不直接继承 S1-108 数字
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD / 修改 7 HTML / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **Controller 源**：`optometryGlassesCtrl`，注册于 `controller.js` L35383
- **行范围**：L35383 – L35959（577 行，A 级重新确认）
  - L35383：`.controller("optometryGlassesCtrl", [ ... ])` 注册
  - L35958：`$scope.getMedicalRecord();`（Init 末尾调用）
  - L35959：`}]);`（Controller 闭合）
  - L35960：`"use strict";`（下一个 module 边界）
- **审计目标**：本轮**仅研究 medicalRecord 被读取以后，optometryGlassesCtrl 内部生成/消费了哪些主数据对象**，不重复 S1-108 的 Controller 注册、State 注册、optometryCtrl 全量 API 等内容。
- **本轮新增发现**：S1-108 中标注的 F 边界（`$scope.lockStorehouseId` 来源）**已被本轮闭合**（见 §10 Read Response 落点）。

---

## 2. Controller 范围

| 项 | 数值 | A-F |
|---|---:|---|
| 起始行 | L35383 | A |
| 结束行 | L35959 | A |
| 总行数 | 577 | A |
| `$scope.xxx = function` 数量 | 21 | A |
| API call site 数量（saveOrQuery + FN_promiseCall + ListFactory） | 14 | A |
| unique API 数量 | 14 | A |
| unique $scope 标识符 | 49（去重） | A |
| Read unique API | 9 | A |
| Write unique API | 5 | A |
| `$state.go` 数量 | 0 | A |
| `$stateParams` 访问 | 2 | A |

### 2.1 21 个 $scope 函数清单

| # | 行号 | 函数 | 类别 | A-F |
|---:|---:|---|---|---|
| 1 | 35391 | `$scope.tip` | 其它（空实现） | A |
| 2 | 35392 | `$scope.prevent` | UI 工具（关闭 supplierList 浮层） | A |
| 3 | 35410 | `$scope.upOther` | UI 工具（toggle） | A |
| 4 | 35415 | `$scope.getMedicalRecord` | API Read（Init 立即 + 外部入口） | A |
| 5 | 35478 | `$scope.showCommon` | UI 工具（modal 切换） | A |
| 6 | 35492 | `$scope.updateImg` | 其它（空实现，return） | A |
| 7 | 35496 | `$scope.updatePatient` | API Write（隐式 savePatientInfo + saveCustomerInfo） | A |
| 8 | 35603 | `$scope.GetMethodGlassRecordVo` | API Read（Init 立即 + 外部入口） | A |
| 9 | 35624 | `$scope.update` | 数据转换 + API helper（queryStore + saveChufang） | A |
| 10 | 35631 | `$scope.update2` | 数据转换 + API helper（saveChufang） | A |
| 11 | 35635 | `$scope.saveChufang` | **API Write**（updateMethodGlassRecord） | A |
| 12 | 35661 | `$scope.queryStorehouseId` | API Read（被 queryCompanyName 调用） | A |
| 13 | 35674 | `$scope.queryCompanyName` | API Read（Init 立即） | A |
| 14 | 35684 | `$scope.GetMedicalProductVoList` | API Read（Init 立即 + 外部入口） | A |
| 15 | 35729 | `$scope.processBasicData` | 数据转换（被 GetMedicalProductVoList 调用） | A |
| 16 | 35768 | `$scope.showsupplierList` | UI 工具 + API helper（searchProductList） | A |
| 17 | 35774 | `$scope.searchProductList` | API Read（ListFactory） | A |
| 18 | 35805 | `$scope.setProduct` | 数据转换 + API helper（queryStore） | A |
| 19 | 35824 | `$scope.deleteReceipt` | API Read（checkBeforeDeleteMedicalProduct） | A |
| 20 | 35848 | `$scope.queryStore` | API Read（getProductSkuExistCountVoList） | A |
| 21 | 35911 | `$scope.save` | **API Write**（saveMedicalProductListOfSmallVersion） | A |

**Init 立即执行**（注册即调用）：
- L35623 `$scope.GetMethodGlassRecordVo()`
- L35682 `$scope.queryCompanyName()`
- L35755 `$scope.GetMedicalProductVoList()`
- L35958 `$scope.getMedicalRecord()`

---

## 3. API 全量

### 3.1 saveOrQuery call site（10 处）

| # | 行号 | API | 类型 | 调用函数 | Request 主要字段 | Response 主要落点 |
|---:|---:|---|---|---|---|---|
| 1 | 35416 | `/admin/getMedicalRecord.json` | Read | `getMedicalRecord` | `id: $scope.medicalRecordId` | `$scope.medicalRecord = response.object`; `saleInfo.fn/inputVal/id`; `$scope.saleInfo = saleInfo`; `FN_promiseCall(getPatientInfo, getCustomerVo)` → `$scope.userInfo` |
| 2 | 35604 | `/admin/getMethodGlassRecordVo.json` | Read | `GetMethodGlassRecordVo` | `medicalRecordId: $scope.medicalRecordId` | for-in `$scope.object` 覆盖（+ Date 转换） |
| 3 | 35644 | `/admin/updateMethodGlassRecord.json` | **Write** | `saveChufang` | `$scope.object`（含 27+ right*/left* 字段 + medicalRecordId + secondDoctorId + lastRxTime） | （空 then） |
| 4 | 35662 | `/admin/selectStorehouseListOfCompany.json` | Read | `queryStorehouseId` | `companyId, mcTypeSortType: "ASC"` | `$scope.lockStorehouseId = res.result.list[0].id`（仅当 res.result.count truthy） |
| 5 | 35675 | `/admin/getCompanyOfMine.json` | Read | `queryCompanyName` | （无参数） | `$scope.companyName = res.object.companyName` + `$scope.queryStorehouseId(res.object.id)` |
| 6 | 35685 | `/admin/getMedicalProductVoList.json` | Read | `GetMedicalProductVoList` | `medicalRecordId: $scope.medicalRecordId` | 分流：`stock.medicalProductSign` truthy → `tempShop`；falsy → `list`（19 字段映射）→ `$scope.stockInSkuList` + `$scope.processBasicData()` → `$scope.glassesInfo` 覆盖 |
| 7 | 35797 | `/admin/getProductSkuExistCountVoList.json` (ListFactory) | Read | `searchProductList` | `parmas { keyword, status: 0, brandId, productType: 1, priceFromInclude, priceToInclude, model1, model2, model1Keyword: "", model2Keyword: "" [, categoryId: 1] }` | （无显式 then）|
| 8 | 35827 | `/admin/checkBeforeDeleteMedicalProduct.json` | Read | `deleteReceipt` | `medicalProductId` | `$scope["" + key].splice(index, 1)` |
| 9 | 35884 | `/admin/getProductSkuExistCountVoList.json` | Read | `queryStore` | `store { keyword, model1, model2 [, brandId, model1Keyword: "", model2Keyword: "", status: 0, index: 0, length: 1] }`（`key === "3"` 时 delete model1/model2） | 分流：count truthy → 4 字段写 glassesInfo；falsy → 5 字段写 undefined/null |
| 10 | 35950 | `/admin/saveMedicalProductListOfSmallVersion.json` | **Write** | `save` | `obj { medicalRecordId: $scope.medicalRecordId, medicalProductParamListJson: JSON.stringify(medicalProductParamListJson) }` | `$scope.GetMedicalProductVoList()` 刷新 |

### 3.2 window.FN_promiseCall call site（3 组）

| # | 行号 | URL | 类型 | 调用上下文 | Request | Success |
|---:|---:|---|---|---|---|---|
| 1 | 35422-35431 | `updateMedicalRecord` | **Write** | `saleInfo.fn`（局部 saleInfo 对象的 fn 字段） | `{ id: $scope.medicalRecordId, secondDoctorId: $scope.object.secondDoctorId }` | `$scope.saveChufang()` |
| 2 | 35437-35468 | `getPatientInfo`, `getCustomerVo` | Read | getMedicalRecord success | `{ id: response.object.patientId }`, `{ customerId: response.object.customerId }` | `$scope.userInfo` 15 字段 |
| 3 | 35532-35542 | `savePatientInfo`, `saveCustomerInfo` | **Write** | `updatePatient` | `patient`（L35509-L35516）, `customer`（L35517-L35523） | `Popup.notice("修改成功!")` |

### 3.3 唯一 API 清单（14 个）

| # | URL | 类型 | call site |
|---:|---|---|---:|
| 1 | `/admin/getMedicalRecord.json` | Read | 1 |
| 2 | `updateMedicalRecord`（FN_promiseCall） | **Write** | 1 |
| 3 | `getPatientInfo`（FN_promiseCall） | Read | 1 |
| 4 | `getCustomerVo`（FN_promiseCall） | Read | 1 |
| 5 | `savePatientInfo`（FN_promiseCall） | **Write** | 1 |
| 6 | `saveCustomerInfo`（FN_promiseCall） | **Write** | 1 |
| 7 | `/admin/getMethodGlassRecordVo.json` | Read | 1 |
| 8 | `/admin/updateMethodGlassRecord.json` | **Write** | 1 |
| 9 | `/admin/selectStorehouseListOfCompany.json` | Read | 1 |
| 10 | `/admin/getCompanyOfMine.json` | Read | 1 |
| 11 | `/admin/getMedicalProductVoList.json` | Read | 1 |
| 12 | `/admin/getProductSkuExistCountVoList.json` | Read | 2（ListFactory + ObjectFactory） |
| 13 | `/admin/checkBeforeDeleteMedicalProduct.json` | Read | 1 |
| 14 | `/admin/saveMedicalProductListOfSmallVersion.json` | **Write** | 1 |

**Read unique**：9
**Write unique**：5
**call site 总数**：14（10 saveOrQuery + 5 FN_promiseCall URL - 1 重复 = 14；其中 getProductSkuExistCountVoList 被调 2 次）

---

## 4. Factory 全量

### 4.1 ObjectFactory（9 个，匿名实例）

| # | 行号 | API | 调用函数 | 备注 |
|---:|---:|---|---|---|
| 1 | 35416 | getMedicalRecord.json | getMedicalRecord | 匿名 |
| 2 | 35604 | getMethodGlassRecordVo.json | GetMethodGlassRecordVo | 匿名 |
| 3 | 35644 | updateMethodGlassRecord.json | saveChufang | 匿名 |
| 4 | 35662 | selectStorehouseListOfCompany.json | queryStorehouseId | 匿名 |
| 5 | 35675 | getCompanyOfMine.json | queryCompanyName | 匿名 |
| 6 | 35685 | getMedicalProductVoList.json | GetMedicalProductVoList | 匿名 |
| 7 | 35827 | checkBeforeDeleteMedicalProduct.json | deleteReceipt | 匿名 |
| 8 | 35884 | getProductSkuExistCountVoList.json | queryStore | 匿名 |
| 9 | 35950 | saveMedicalProductListOfSmallVersion.json | save | 匿名 |

**ObjectFactory 复用**：**0**（每次 new 实例，无 1 处命名）
**ObjectFactory 实例隔离**：**全隔离**（每次 new 都是独立实例，不共享状态）

### 4.2 ListFactory（1 个，命名实例）

| # | 行号 | Factory 名 | API | Request | pageStart | pageSize | 备注 |
|---:|---:|---|---|---|---|---:|---|
| 1 | 35797 | `$scope.getCorpListFactory` | getProductSkuExistCountVoList.json | parmas (10 字段) | 0 | 30 | 命名；调用 `.nextPage().then(...)` |

**ListFactory 复用**：**0**（仅在 searchProductList 内重建，不被其它函数使用）
**分页参数**：pageStart=0, pageSize=30（A 级确认）

### 4.3 FN_promiseCall（3 组，共 5 个 URL）

| # | 行号 | Factory 引用 | URL | 数量 |
|---:|---:|---|---|---:|
| 1 | 35422 | `ObjectFactory`（DI 注入） | updateMedicalRecord | 1 |
| 2 | 35437 | 同上 | getPatientInfo + getCustomerVo | 2 |
| 3 | 35532 | 同上 | savePatientInfo + saveCustomerInfo | 2 |

**FN_promiseCall URL 总数**：5（与 call site 14 重叠；3 个 FN_promiseCall 调用组中实际触发 5 个 URL）
**注**：S1-108 中"5 个 Write"的统计包括 4 个 FN_promiseCall URL（updateMedicalRecord, savePatientInfo, saveCustomerInfo）+ 1 个 saveOrQuery（updateMethodGlassRecord, saveMedicalProductListOfSmallVersion 共 2 个）+ 1 个新发现（详见 §15）。

---

## 5. StateParams

| 行号 | 参数 | 转换 | 落点 |
|---:|---|---|---|
| 35388 | `medicalRecordId` | 直接赋值 | `$scope.medicalRecordId` |
| 35389 | `edit` | `=== "true"` 强比较 | `$scope.edit` |

**唯一访问次数**：2（A 级确认）
**0 处**直接读取 `$stateParams.xxx`（除 L35388/L35389）
**0 处** `$state.go`（A 级确认）

---

## 6. medicalRecordId

### 6.1 $scope.medicalRecordId 全部 Consumer（10 处）

| 行号 | 表达式 | 用途 | 类别 |
|---:|---|---|---|
| 35388 | `= $stateParams.medicalRecordId` | Init 初始化 | State 入口 |
| 35417 | `id: $scope.medicalRecordId` | getMedicalRecord Request | Read |
| 35425 | `id: $scope.medicalRecordId` | updateMedicalRecord Request | Write |
| 35605 | `medicalRecordId: $scope.medicalRecordId` | getMethodGlassRecordVo Request | Read |
| 35640 | `$scope.object.medicalRecordId = $scope.medicalRecordId` | $scope.object 复制 | Write prep |
| 35653 | `$scope.printChufang.medicalRecordId = $scope.medicalRecordId` | 打印处方对象 | Object init |
| 35686 | `medicalRecordId: $scope.medicalRecordId` | getMedicalProductVoList Request | Read |
| 35816 | `$scope.addStore.medicalRecordId = $scope.medicalRecordId` | "其他商品"弹窗对象 | Object init |
| 35842 | `param: { medicalRecordId: $scope.medicalRecordId, payedStatus: 0 }` | printShoufei.options 静态定义 | Object init |
| 35947 | `medicalRecordId: $scope.medicalRecordId` | saveMedicalProductListOfSmallVersion Request | Write |

### 6.2 全局 medicalRecordId 路径增量

S1-108 已锁定 5 类路径（optometryCtrl 范围）：

1. `item.medicalRecord.id`（fnMap 5 动作 + template.back）
2. `selectOrderListFactory.items[orderIndex].medicalRecord.id`（querySingleOrder）
3. `medicalProduct.medicalRecordId`（modal.changeOrder 报损）
4. `customerCheckin.medicalRecordId`（beginCustomerCheckin success）
5. `$stateParams.medicalRecordId`（optometryGlassesCtrl 入口）

S1-109 在 optometryGlassesCtrl 范围内**未发现**新的 medicalRecordId 字段路径：

| # | 候选路径 | 是否在 optometryGlassesCtrl 出现 | 备注 |
|---:|---|---|---|
| 6 | `item.medicalRecord.id` (optometryGlassesCtrl 内) | 否 | 0 处 |
| 7 | `medicalProduct.medicalRecordId` (optometryGlassesCtrl 内) | 否 | $scope.lockStorehouseId 不是 medicalRecordId；stock.medicalProduct.id 在 GetMedicalProductVoList 内被读但不复制为 medicalRecordId |
| 8 | `response.object.medicalRecordId` (getMedicalRecord success) | 否 | getMedicalRecord Request 用 `id`，未直接读 response.object.medicalRecordId |
| 9 | `methodGlassRecord.medicalRecordId` (getMethodGlassRecordVo success) | 否 | for-in 覆盖 $scope.object 字段，但 medicalRecordId 由 L35640 显式注入 |
| 10 | `res.result.list[].medicalProduct.id` | 否 | 映射到 stockInSkuList.id，不作为 medicalRecordId |
| 11 | `customerCheckin.medicalRecordId` (optometryGlassesCtrl 内) | 否 | 0 处 |

**S1-109 结论**：optometryGlassesCtrl 内的 medicalRecordId **全部源自 `$stateParams.medicalRecordId`**，无新路径。

**5 类路径仍是 5 类**，未扩展。

---

## 7. $scope.medicalRecord

### 7.1 全部出现位置（5 处）

| 行号 | 表达式 | 类别 | A-F |
|---:|---|---|---|
| 35390 | `$scope.medicalRecord = {};` | Init 初始化 | A |
| 35416 | `new ObjectFactory().saveOrQuery("/admin/getMedicalRecord.json", {` | Read API 调用 | A |
| 35419 | `$scope.medicalRecord = response.object;` | Read 赋值 | A |
| 35433 | `saleInfo.inputVal = $scope.medicalRecord.secondDoctorName;` | 派生到 saleInfo.inputVal | A |
| 35434 | `saleInfo.id = $scope.medicalRecord.secondDoctorId;` | 派生到 saleInfo.id | A |

### 7.2 整体赋值历史

| 阶段 | 行号 | 赋值表达式 | 备注 |
|---|---|---|---|
| Init | 35390 | `$scope.medicalRecord = {};` | 空对象 |
| getMedicalRecord success | 35419 | `$scope.medicalRecord = response.object;` | **唯一整体赋值**，整个对象覆盖 |

**关键发现**：
- `$scope.medicalRecord` 仅有 1 次整体赋值（getMedicalRecord success L35419）
- **0 次**字段级赋值（`$scope.medicalRecord.xxx = ...` 全部不存在）
- **0 次**重新赋值（不再次整体替换）
- **0 次**clone/copy（angular.copy 等不存在）
- **0 次**清空（不再次设为 `{}` 或 `null`）

### 7.3 medicalRecord 字段消费（仅 2 字段）

| 字段 | 消费位置 | 消费方式 | 落点 | A-F |
|---|---|---|---|---|
| `.secondDoctorName` | L35433 | 读取 | `saleInfo.inputVal`（局部 saleInfo） | A |
| `.secondDoctorId` | L35434 | 读取 | `saleInfo.id`（局部 saleInfo） | A |

**字段消费统计**：
- 实际消费字段：**2 个**（secondDoctorName, secondDoctorId）
- 理论上 response.object 包含更多字段，但本 Controller 范围内**仅消费这 2 个**
- `$scope.medicalRecord` 在 L35419 赋值后**作为整体 Scope 长期保留**，但 575 行内仅有 2 处字段访问

---

## 8. medicalRecord 字段全集

### 8.1 本 Controller 实际消费字段（2 字段）

| 字段 | 类型 | 消费位置 | 派生链 | A-F |
|---|---|---|---|---|
| `medicalRecord.secondDoctorName` | String | L35433 | → `saleInfo.inputVal` → `$scope.saleInfo.inputVal` | A |
| `medicalRecord.secondDoctorId` | Number/String | L35434 | → `saleInfo.id` → `$scope.saleInfo.id` → `$scope.object.secondDoctorId` (L35435) | A |

### 8.2 间接消费（通过 response.object 其它字段）

虽然不是 medicalRecord 本身的字段，但 getMedicalRecord response.object 内的其它字段被消费：

| 字段 | 消费位置 | 用途 | A-F |
|---|---|---|---|
| `response.object.patientId` | L35440 | FN_promiseCall `getPatientInfo` Request | A |
| `response.object.customerId` | L35445 | FN_promiseCall `getCustomerVo` Request | A |
| `response.object.firstVisit` | L35427（**注释**） | 未启用 | A |

**注释关键发现**：
- L35427 `// firstVisit: new Date(response.object.firstVisit)` 是**注释**状态，未实际执行
- 这表明源码存在一个**未启用的功能**：把 firstVisit 字段作为 updateMedicalRecord 的额外参数
- 字段 `response.object.firstVisit` **未**实际被消费

### 8.3 推断字段（response.object 包含但本 Controller 未消费）

**严禁推断**。本轮不展开 response.object 实际字段集，因为：
1. response.object 来自 getMedicalRecord.json 接口，**Response 字段定义不在源码范围**（F 边界）
2. 实际字段需要在生产环境或文档中确认（A 级无证据）
3. 本 Controller 仅访问已知的 patientId, customerId, secondDoctorName, secondDoctorId 4 个字段

**已访问字段**：`patientId, customerId, secondDoctorName, secondDoctorId`（4 个，A 级确认）
**未访问但可能存在**：`id, firstVisit, ...` 等（**F 边界**）

---

## 9. medicalRecord 派生对象

### 9.1 派生链

| Source | Target | 表达式 | 行号 | 上游 | 落点 | A-F |
|---|---|---|---|---|---|---|
| `$scope.medicalRecord.secondDoctorName` | `saleInfo.inputVal`（局部） | `saleInfo.inputVal = $scope.medicalRecord.secondDoctorName` | 35433 | getMedicalRecord | → `$scope.saleInfo.inputVal`（HTML 可能消费） | A |
| `$scope.medicalRecord.secondDoctorId` | `saleInfo.id`（局部） | `saleInfo.id = $scope.medicalRecord.secondDoctorId` | 35434 | getMedicalRecord | → `$scope.saleInfo.id` | A |
| `saleInfo.id` | `$scope.object.secondDoctorId` | `$scope.object.secondDoctorId = saleInfo.id` | 35435 | getMedicalRecord | → updateMethodGlassRecord Request → updateMedicalRecord Request | A |
| `response.object.patientId` | `FN_promiseCall` URL `getPatientInfo` param.id | `{ id: response.object.patientId }` | 35440 | getMedicalRecord | → getPatientInfo Request | A |
| `response.object.customerId` | `FN_promiseCall` URL `getCustomerVo` param.customerId | `{ customerId: response.object.customerId }` | 35445 | getMedicalRecord | → getCustomerVo Request | A |

### 9.2 派生层级

```
getMedicalRecord (L35416)
  └─ response.object (L35419: $scope.medicalRecord)
       ├─ response.object.patientId (L35440) → getPatientInfo Request
       ├─ response.object.customerId (L35445) → getCustomerVo Request
       ├─ response.object.secondDoctorName (L35433) → saleInfo.inputVal
       └─ response.object.secondDoctorId (L35434) → saleInfo.id → $scope.object.secondDoctorId
            └─ updateMethodGlassRecord Request (L35644)
            └─ updateMedicalRecord Request (L35422-L35431)
```

### 9.3 $scope 派生汇总

| Scope 字段 | 派生自 | 表达式 | 行号 |
|---|---|---|---|
| `$scope.saleInfo` | 局部 saleInfo 对象 | `$scope.saleInfo = saleInfo` | 35436 |
| `$scope.saleInfo.inputVal` | `$scope.medicalRecord.secondDoctorName` | `saleInfo.inputVal = ...` | 35433 |
| `$scope.saleInfo.id` | `$scope.medicalRecord.secondDoctorId` | `saleInfo.id = ...` | 35434 |
| `$scope.object.secondDoctorId` | `saleInfo.id` | `$scope.object.secondDoctorId = saleInfo.id` | 35435 |
| `$scope.userInfo` | `getPatientInfo` + `getCustomerVo` | `$scope.userInfo = { ... 15 字段 ... }` | 35451-35466 |

---

## 10. Read Response 落点

### 10.1 getMedicalRecord.json (L35416)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `response.object` | `$scope.medicalRecord`（整体） | L35433, L35434（仅 2 字段消费） | A |
| `response.object.patientId` | FN_promiseCall getPatientInfo Request id | getPatientInfo → $scope.userInfo.patient* | A |
| `response.object.customerId` | FN_promiseCall getCustomerVo Request customerId | getCustomerVo → $scope.userInfo.customer* | A |
| `response.object.secondDoctorName` | `saleInfo.inputVal` → `$scope.saleInfo.inputVal` | HTML 消费（F 边界） | A |
| `response.object.secondDoctorId` | `saleInfo.id` → `$scope.saleInfo.id` → `$scope.object.secondDoctorId` | updateMethodGlassRecord + updateMedicalRecord Request | A |
| `response.object.firstVisit` | 注释（未启用） | 无 | A |

### 10.2 getMethodGlassRecordVo.json (L35604)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.result.vo.methodGlassRecord` | `methodGlassRecord`（局部） | for-in `$scope.object` 覆盖 | A |
| 详细字段（如 right15, left15, ...） | `$scope.object[i] = methodGlassRecord[i]` | updateMethodGlassRecord Request（L35644） | A |
| `methodGlassRecord.lastRxTime` | `$scope.object.lastRxTime = new Date(...)` | updateMethodGlassRecord Request | A |

**关键发现**：for-in 循环覆盖 $scope.object 的 27+ 字段（A 级确认 L35613-L35620）

### 10.3 updateMethodGlassRecord.json (L35644) — **Write**

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| （无显式 then） | 无 | 无 | A |

### 10.4 selectStorehouseListOfCompany.json (L35662)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.result.count` | 分流判断 | `!count` → Popup.notice | A |
| `res.result.list[0].id` | **`$scope.lockStorehouseId`** | **`save` (L35919) → saveMedicalProductListOfSmallVersion Request** | A |

**S1-108 错误纠正**：
- S1-108 将 `$scope.lockStorehouseId` 标注为 **F 边界**（来源不可得）
- S1-109 **闭合**：来源为 `selectStorehouseListOfCompany.json` 的 `res.result.list[0].id`（L35669）

### 10.5 getCompanyOfMine.json (L35675)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.status == 0` | 分流判断 | 否则无操作 | A |
| `res.object.companyName` | `$scope.companyName` | HTML 消费（F 边界） | A |
| `res.object.id` | `queryStorehouseId(res.object.id)` 入参 | → selectStorehouseListOfCompany Request | A |

**关键发现**：queryCompanyName success 链式触发 queryStorehouseId（A 级确认 L35678）

### 10.6 getMedicalProductVoList.json (L35685)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.result.count` | 分流判断 | `!count` → 无操作（不进入 forEach） | A |
| `res.result.list` | `res.result.list.forEach(function (stock) { ... })` | 见下 | A |
| 派生 `list` 数组 | `$scope.stockInSkuList` | `save` (L35929) → saveMedicalProductListOfSmallVersion Request；`addStore.callback` (L35821) push；`deleteReceipt` (L35833) splice | A |
| 派生 `tempList` 数组 | `$scope.tempShop` | `processBasicData` (L35730) → `$scope.glassesInfo` 覆盖 | A |

**list 元素结构**（L35698-L35720 19 字段映射）：
```javascript
{
  id, brandName, categoryName, factory, marketPrice, model1, model1Name,
  model2, model2Name, productName, skuCode, unitName, unLockExistSkuCount,
  lockStorehouseId, productSkuId, remark, storeName, useCount, memberRate,
  skuDuplicate, kpiPrice
}
```

**tempList 元素**（直接 push 整个 stock，L35696）— 包含 stock.medicalProduct, stock.brand, stock.category, stock.product, stock.productSku, stock.medicalProductSign, stock.unLockExistSkuCount, stock.lockStorehouse 等原始字段

### 10.7 getProductSkuExistCountVoList.json (L35797) — ListFactory

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.count == 0` | `Popup.notice("没有该规格的商品")` | 无 | A |
| `res.result.list` | ListFactory 内部管理 | 外部 HTML 通过 `$scope.getCorpListFactory.items` 消费（F 边界） | A |

**关键发现**：ListFactory 实例化后，源码中**0 处**对 `getCorpListFactory.items` 或 nextPage 后的 list 消费（F 边界：HTML 可能消费）

### 10.8 checkBeforeDeleteMedicalProduct.json (L35827)

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.status == 1` | `Popup.notice(res.errmsg)` | 无 | A |
| （无 result consumer） | 无 | `$scope[key].splice(index, 1)`（L35833） | A |

### 10.9 getProductSkuExistCountVoList.json (L35884) — ObjectFactory

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.status == 1` | `Popup.notice(res.errmsg)` | 无 | A |
| `res.result.count == truthy` | `$scope.glassesInfo["unLockExistSkuCount"+key] = unLockExistSkuCount`; `"marketPrice"+key = productSku.marketPrice`; `"productSkuId"+key = productSku.id`; `"productSkuKpiPrice"+key = productSku.kpiPrice`; `"data"+key = false` | `save` (L35915, L35925) → saveMedicalProductListOfSmallVersion Request | A |
| `res.result.count == falsy` | `$scope.glassesInfo["unLockExistSkuCount"+key] = undefined`; `"marketPrice"+key = undefined`; `"productSkuId"+key = null`; `"productSkuKpiPrice"+key = null`; `"data"+key = true` | 无 | A |

### 10.10 saveMedicalProductListOfSmallVersion.json (L35950) — **Write**

| Response 路径 | 落点 | 后续 Consumer | A-F |
|---|---|---|---|
| `res.status == 1` | `Popup.notice(res.errmsg)` | 无 | A |
| `res.status != 1` | `Popup.notice("保存成功!")` + `$scope.GetMedicalProductVoList()` 刷新 | getMedicalProductVoList 重新执行 | A |

### 10.11 FN_promiseCall 组

**getPatientInfo + getCustomerVo (L35437)**：
- `res[0].object` → `patient`（局部）→ `$scope.userInfo` 8 字段（patientId, avatar, patientName, patientGender, patientBirthday, patientRemark, name, gender）
- `res[1].result.vo` → `customer`（局部）→ `$scope.userInfo` 5 字段（customerId, linkMobile, channel, channelTagId, mobile）
- `$scope.userInfo` 共 13 字段去重（实际 15 字段 = 8 + 5 + 2 共有，源码 13 个不同键）

**updateMedicalRecord (L35422)**：
- success → `$scope.saveChufang()` 链式触发 updateMethodGlassRecord

**savePatientInfo + saveCustomerInfo (L35532)**：
- success → `$timeout(Popup.notice("修改成功!"))` 无后续 Refresh

---

## 11. API 对象分类

按 Request/Response 实际字段做对象分类（A 级确认，**仅按源码出现**）：

### 11.1 A. medicalRecord

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| getMedicalRecord.json | Read | `id` Request → `response.object` Response（含 patientId/customerId/secondDoctorName/secondDoctorId 等） | A |
| updateMethodGlassRecord.json | Write | `$scope.object` Request（含 medicalRecordId 字段） | A |
| updateMedicalRecord (FN) | Write | `{ id, secondDoctorId }` Request | A |

### 11.2 B. patient/customer

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| getPatientInfo (FN) | Read | `{ id: response.object.patientId }` Request → `res[0].object` Response | A |
| getCustomerVo (FN) | Read | `{ customerId: response.object.customerId }` Request → `res[1].result.vo` Response | A |
| savePatientInfo (FN) | Write | `patient` Request（id, patientName, patientGender, patientBirthday, patientRemark） | A |
| saveCustomerInfo (FN) | Write | `customer` Request（id, channelTagId, channel, linkMobile, trueName） | A |

### 11.3 C. prescription (处方/MethodGlassRecord)

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| getMethodGlassRecordVo.json | Read | `{ medicalRecordId }` Request → `res.result.vo.methodGlassRecord` Response | A |
| updateMethodGlassRecord.json | Write | `$scope.object` Request（27+ right*/left* 字段） | A |

### 11.4 D. product (商品)

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| getMedicalProductVoList.json | Read | `{ medicalRecordId }` Request → `res.result.list` Response（每个元素含 brand/category/product/productSku/medicalProduct/lockStorehouse/medicalProductSign/unLockExistSkuCount/skuDuplicate） | A |
| getProductSkuExistCountVoList.json (ListFactory) | Read | `parmas` Request (10 字段) → `res` Response | A |
| getProductSkuExistCountVoList.json (ObjectFactory) | Read | `store` Request (5-8 字段) → `res.result.list[0].productSku/unLockExistSkuCount` Response | A |

### 11.5 E. inventory (库存/Storehouse)

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| selectStorehouseListOfCompany.json | Read | `{ companyId, mcTypeSortType: "ASC" }` Request → `res.result.list[0].id` Response | A |
| checkBeforeDeleteMedicalProduct.json | Read | `{ medicalProductId }` Request → 无显式 result consumer | A |

### 11.6 F. organization (公司/Company)

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| getCompanyOfMine.json | Read | （无参数）Request → `res.object.companyName/id` Response | A |

### 11.7 G. productListSku (商品 SKU 保存)

| API | 类型 | 字段 | A-F |
|---|---|---|---|
| saveMedicalProductListOfSmallVersion.json | Write | `{ medicalRecordId, medicalProductParamListJson }` Request | A |

### 11.8 不可分类

- `computeMedicalRecordFee`（在 `$scope.printShoufei.options[0].url`，非 saveOrQuery 调用，是 popup 内部 URL）：F 边界

---

## 12. Read → Read

### 12.1 直接 Read → Read 链

**链 1**：getCompanyOfMine → queryStorehouseId
- L35674-35681 `queryCompanyName` success:
  - `res.object.id` → `queryStorehouseId(res.object.id)` → Read selectStorehouseListOfCompany.json
- **A 级确认**

### 12.2 隐式 Read → Read（通过 success 链式）

**链 2**：getMedicalRecord → FN_promiseCall (getPatientInfo + getCustomerVo)
- L35418-35468 `getMedicalRecord` success:
  - `response.object.patientId` → FN_promiseCall getPatientInfo param.id → Read
  - `response.object.customerId` → FN_promiseCall getCustomerVo param.customerId → Read
- **A 级确认**

### 12.3 隐式 Read → Read（通过 success 链式 + 局部 saleInfo.fn）

**链 3**：getMedicalRecord → saleInfo.fn → updateMedicalRecord → saveChufang → updateMethodGlassRecord
- L35420-35431 `saleInfo.fn` 内部：FN_promiseCall updateMedicalRecord → success → `$scope.saveChufang()` → Read/Write
- 注：此链是 **Read → Write → Write**（不是 Read → Read）
- **A 级确认**

### 12.4 无直接 Read → Read 数据依赖

- getMethodGlassRecordVo / getMedicalProductVoList / getProductSkuExistCountVoList / checkBeforeDeleteMedicalProduct 之间**无 success 链式触发其它 Read**（A 级确认）
- 每个 Read 都是**独立调用**

### 12.5 总结

| 关系 | 数量 | 详情 |
|---|---:|---|
| 直接 Read → Read 链 | 1 | getCompanyOfMine → queryStorehouseId |
| 隐式 Read → Read 链（FN_promiseCall） | 1 | getMedicalRecord → getPatientInfo + getCustomerVo |
| Read → Write 链 | 1 | getMedicalRecord → updateMedicalRecord (FN) + saleInfo.fn → saveChufang |
| Read → Write 链 | 4 | 5 个 Write 至少有一个上游 Read |
| 无直接 Read → Read 依赖 | 6 | 其余 6 个 Read 互相独立 |

---

## 13. Read → Write

### 13.1 字段级闭合

| Write | Request 字段 | 上游 Read | 中间变量 | A-F |
|---|---|---|---|---|
| **updateMethodGlassRecord (L35644)** | `$scope.object`（27+ right*/left* 字段） | getMethodGlassRecordVo (L35604) | for-in 覆盖 $scope.object | A |
| | `$scope.object.medicalRecordId` | StateParams | Init 复制（L35640 in saveChufang） | A |
| | `$scope.object.secondDoctorId` | getMedicalRecord (L35416) | response.object.secondDoctorId → saleInfo.id → $scope.object.secondDoctorId (L35435) | A |
| | `$scope.object.lastRxTime` | getMethodGlassRecordVo | for-in 覆盖 + Date 转换（L35617） | A |
| **updateMedicalRecord (FN, L35422)** | `id` | StateParams | `$scope.medicalRecordId` | A |
| | `secondDoctorId` | getMedicalRecord | `$scope.object.secondDoctorId` (L35435) | A |
| **savePatientInfo (FN, L35532)** | `patient.id` (L35510) | getPatientInfo (FN) | `$scope.userInfo.patientId` (L35499) | A |
| | `patient.patientName` | getPatientInfo | `$scope.userInfo.patientName` (L35500) | A |
| | `patient.patientGender` | getPatientInfo | `$scope.userInfo.patientGender` (L35501) | A |
| | `patient.patientBirthday` | getPatientInfo | `$scope.userInfo.patientBirthday` (L35502)；if falsy delete (L35525) | A |
| | `patient.patientRemark` | getPatientInfo | `$scope.userInfo.patientRemark` (L35503) | A |
| **saveCustomerInfo (FN, L35532)** | `customer.id` (L35518) | getCustomerVo (FN) | `$scope.userInfo.customerId` (L35504) | A |
| | `customer.channelTagId` | getCustomerVo | `$scope.userInfo.channelTagId` (L35505) | A |
| | `customer.channel` | getCustomerVo | `$scope.userInfo.channel` (L35506) | A |
| | `customer.linkMobile` | getCustomerVo | `$scope.userInfo.linkMobile` (L35507) | A |
| | `customer.trueName` | getPatientInfo | `patientName` (L35500 → L35522) | A |
| **saveMedicalProductListOfSmallVersion (L35950)** | `obj.medicalRecordId` | StateParams | `$scope.medicalRecordId` (L35947) | A |
| | `obj.medicalProductParamListJson` | 混合 | 见下表 | A |
| | `medicalProductParamListJson[i].lockStorehouseId` (L35919) | **selectStorehouseListOfCompany (L35662)** | **`$scope.lockStorehouseId`** (L35669) | **A**（S1-108 错误纠正） |
| | `medicalProductParamListJson[i].productSkuId` (L35920) | getProductSkuExistCountVoList (L35884) | `$scope.glassesInfo["productSkuId"+i]` (L35915) | A |
| | `medicalProductParamListJson[i].kpiPrice` (L35925) | getProductSkuExistCountVoList (L35884) | `$scope.glassesInfo["productSkuKpiPrice"+i]` (L35915) | A |
| | `medicalProductParamListJson[i].remark` (L35923) | getMedicalProductVoList (L35685) | `$scope.glassesInfo["remark"+i]` (via processBasicData L35747) | A |
| | `medicalProductParamListJson[i].signType` (L35924) | window.optionsObj | `window.optionsObj.glassesSignType[i]` | A |
| | `medicalProductParamListJson[].lockStorehouseId` (stock) (L35933) | getMedicalProductVoList | `stock.lockStorehouseId` (L35712) | A |
| | `medicalProductParamListJson[].productSkuId` (L35934) | getMedicalProductVoList | `stock.productSkuId` (L35713) | A |
| | `medicalProductParamListJson[].memberRate` (L35935) | getMedicalProductVoList | `stock.memberRate` (L35717) | A |
| | `medicalProductParamListJson[].useCount` (L35936) | getMedicalProductVoList | `stock.useCount` (L35716) | A |
| | `medicalProductParamListJson[].remark` (L35937) | getMedicalProductVoList | `stock.remark` (L35714) | A |
| | `medicalProductParamListJson[].kpiPrice` (L35938) | getMedicalProductVoList | `stock.kpiPrice` (L35719) | A |
| | `medicalProductParamListJson[].id` (L35932) | getMedicalProductVoList | `stock.id` (L35699) | A |

### 13.2 关键发现：S1-108 错误纠正

**S1-108 错误**：
> F 边界说明：$scope.lockStorehouseId 在 $scope.save 函数中作为 lockStorehouseId 字段写入 Request（L35919），但本 Controller 范围内**0 处赋值**给 $scope.lockStorehouseId

**S1-109 闭合证据**：
- L35661-35671 `$scope.queryStorehouseId` 函数
- L35669 **`$scope.lockStorehouseId = res.result.list[0].id;`** （A 级确认）
- L35675-35681 `$scope.queryCompanyName` success
- L35678 `$scope.queryStorehouseId(res.object.id);` 链式触发
- L35682 `$scope.queryCompanyName();` Init 立即执行

**完整闭合链**：
```
Init (L35682)
  → queryCompanyName (L35674)
    → Read getCompanyOfMine.json (L35675)
      → success (L35676-35680):
         ├─ $scope.companyName = res.object.companyName (L35677)
         └─ $scope.queryStorehouseId(res.object.id) (L35678)
            → Read selectStorehouseListOfCompany.json (L35662)
              → success (L35665-35670):
                 ├─ if !res.result.count → Popup.notice("没有仓库!") (L35666-35668)
                 └─ $scope.lockStorehouseId = res.result.list[0].id (L35669)
                    → save (L35911) 触发时使用
                      → saveMedicalProductListOfSmallVersion Request (L35919)
```

**S1-108 F 边界 → S1-109 A 级闭合**。

### 13.3 隐式 Write 链

`updateMedicalRecord`（FN，隐式）→ `saveChufang`（显式）→ `updateMethodGlassRecord`（显式）

链式触发（不依赖 Read）：
- saleInfo.fn 触发（L35420-L35432）
- updateMedicalRecord success → saveChufang 调用（L35430）
- saveChufang 内执行 updateMethodGlassRecord Write（L35644）

---

## 14. Write → Read

| Write | success 行为 | 触发的 Read | 行号 |
|---|---|---|---|
| updateMethodGlassRecord | （空 then） | 无 | L35644-L35648 |
| saveMedicalProductListOfSmallVersion | `Popup.notice("保存成功!")` + `$scope.GetMedicalProductVoList()` | **getMedicalProductVoList (L35685)** | L35950-L35955 |
| updateMedicalRecord (FN) | `$scope.saveChufang()`（链式 Write） | 无 | L35429-L35430 |
| savePatientInfo (FN) | （$timeout 内 Popup.notice） | 无 | L35538-L35541 |
| saveCustomerInfo (FN) | （$timeout 内 Popup.notice） | 无 | L35538-L35541 |

**Write → Read 链**：1 条（saveMedicalProductListOfSmallVersion → GetMedicalProductVoList）
**Write → Write 链**：1 条（updateMedicalRecord → saveChufang）
**Write → State 链**：0 条

---

## 15. Write Request 字段 provenance

### 15.1 updateMethodGlassRecord (L35644)

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `$scope.object` 整体（27+ 字段） | `new ObjectFactory().saveOrQuery("/admin/updateMethodGlassRecord.json", $scope.object)` | Init 定义 + for-in 覆盖 | getMethodGlassRecordVo (L35604) | A |
| `medicalRecordId` | `$scope.object.medicalRecordId = $scope.medicalRecordId`（L35640，saveChufang 内） | Init 复制 | StateParams (L35388) | A |
| `secondDoctorId` | `$scope.object.secondDoctorId = saleInfo.id`（L35435） | saleInfo.id | getMedicalRecord (L35416) | A |
| `lastRxTime` | for-in 覆盖 + Date 转换（L35617） | `$scope.object.lastRxTime` | getMethodGlassRecordVo (L35604) | A |

**字段计数**：27 个 right*/left* 字段 + medicalRecordId + secondDoctorId + lastRxTime = 30 字段（A 级）
**A-F 分布**：全部 A 级

### 15.2 updateMedicalRecord (L35422-L35431, FN)

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `id` | `$scope.medicalRecordId`（L35425） | Init 复制 | StateParams (L35388) | A |
| `secondDoctorId` | `$scope.object.secondDoctorId`（L35426） | saleInfo.id → $scope.object | getMedicalRecord (L35416) | A |

### 15.3 savePatientInfo (L35532, FN)

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `patient.id` | `patientId`（L35510） | `$scope.userInfo.patientId`（L35499） | getPatientInfo (FN, L35437) | A |
| `patient.patientName` | `patientName`（L35511） | `$scope.userInfo.patientName`（L35500） | getPatientInfo (FN, L35437) | A |
| `patient.patientGender` | `patientGender`（L35512） | `$scope.userInfo.patientGender`（L35501） | getPatientInfo (FN, L35437) | A |
| `patient.patientBirthday` | `patientBirthday`（L35513）；if !falsy delete（L35525） | `$scope.userInfo.patientBirthday`（L35502） | getPatientInfo (FN, L35437) | A |
| `patient.patientRemark` | `patientRemark`（L35514） | `$scope.userInfo.patientRemark`（L35503） | getPatientInfo (FN, L35437) | A |

**注意**：L35515 `// avatar,` 注释表明 avatar 字段被**故意排除**在 savePatientInfo Request 之外

### 15.4 saveCustomerInfo (L35532, FN)

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `customer.id` | `customerId`（L35518） | `$scope.userInfo.customerId`（L35504） | getCustomerVo (FN, L35437) | A |
| `customer.channelTagId` | `channelTagId`（L35519） | `$scope.userInfo.channelTagId`（L35505） | getCustomerVo (FN, L35437) | A |
| `customer.channel` | `channel`（L35520） | `$scope.userInfo.channel`（L35506） | getCustomerVo (FN, L35437) | A |
| `customer.linkMobile` | `linkMobile`（L35521） | `$scope.userInfo.linkMobile`（L35507） | getCustomerVo (FN, L35437) | A |
| `customer.trueName` | `patientName`（L35522） | `$scope.userInfo.patientName`（L35500） | getPatientInfo (FN, L35437)（注意：是 patientName 不是 customerName） | A |

**关键发现**：`trueName` 来自 **patient.patientName** 而非 customer（**字段错位**），这可能是业务上的有意设计

### 15.5 saveMedicalProductListOfSmallVersion (L35950)

#### 15.5.1 obj 结构（L35946-L35948）

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `obj.medicalRecordId` | `$scope.medicalRecordId`（L35947） | Init 复制 | StateParams (L35388) | A |
| `obj.medicalProductParamListJson` | `JSON.stringify(medicalProductParamListJson)`（L35945） | 局部数组 | 混合（见下） | A |

#### 15.5.2 medicalProductParamListJson[0-2]（1-3 循环，L35913-L35928）

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `id: null`（L35918） | 字面量 | 无 | 无 | A |
| `lockStorehouseId: $scope.lockStorehouseId`（L35919） | `$scope.lockStorehouseId` | Init 派生 | **selectStorehouseListOfCompany (L35662)** | **A**（S1-109 新闭合） |
| `productSkuId`（L35920） | `$scope.glassesInfo["productSkuId" + i]` | `$scope.glassesInfo` | getProductSkuExistCountVoList (L35884) | A |
| `memberRate: null`（L35921） | 字面量 | 无 | 无 | A |
| `useCount: 1`（L35922） | 字面量 | 无 | 无 | A |
| `remark`（L35923） | `$scope.glassesInfo["remark" + i]` | `$scope.glassesInfo` | getMedicalProductVoList (L35685) → processBasicData (L35729) → L35747 | A |
| `signType`（L35924） | `window.optionsObj.glassesSignType[i]` | 全局对象 | 无 | A |
| `kpiPrice`（L35925） | `$scope.glassesInfo["productSkuKpiPrice" + i]` | `$scope.glassesInfo` | getProductSkuExistCountVoList (L35884) | A |

#### 15.5.3 medicalProductParamListJson[]（stockInSkuList，L35929-L35941）

| Request 字段 | 表达式 | 中间变量 | 上游 Read | A-F |
|---|---|---|---|---|
| `id: stock.id`（L35932） | `stock.id` | 来自 $scope.stockInSkuList 元素 | getMedicalProductVoList (L35685) → L35699 | A |
| `lockStorehouseId: stock.lockStorehouseId`（L35933） | `stock.lockStorehouseId` | 同上 | getMedicalProductVoList (L35685) → L35712 | A |
| `productSkuId: stock.productSkuId`（L35934） | `stock.productSkuId` | 同上 | getMedicalProductVoList (L35685) → L35713 | A |
| `memberRate: stock.memberRate`（L35935） | `stock.memberRate` | 同上 | getMedicalProductVoList (L35685) → L35717 | A |
| `useCount: stock.useCount`（L35936） | `stock.useCount` | 同上 | getMedicalProductVoList (L35685) → L35716 | A |
| `remark: stock.remark`（L35937） | `stock.remark` | 同上 | getMedicalProductVoList (L35685) → L35714 | A |
| `kpiPrice: stock.kpiPrice`（L35938） | `stock.kpiPrice` | 同上 | getMedicalProductVoList (L35685) → L35719 | A |

**字段计数**：A 字段 8 + 7 = 15 字段（A 级）

---

## 16. edit

### 16.1 $scope.edit 全部 Consumer（2 处）

| 行号 | 表达式 | 类型 | A-F |
|---:|---|---|---|
| 35389 | `$scope.edit = $stateParams.edit === "true";` | Init 转换（写入） | A |
| 35409 | `$scope.showOtherStore = $scope.edit;` | 复制到 showOtherStore | A |

### 16.2 对 API / State / Init 的影响

| 影响项 | 是否影响 | 证据 |
|---|---|---|
| API Request 字段 | **否** | grep `$scope.edit` 0 处出现在 Request 构造中 |
| API 类型 | **否** | 0 处 if-else 基于 $scope.edit |
| 初始化流程 | **否** | Init 立即执行函数无 $scope.edit 分支 |
| 页面数据 | **否** | $scope.showOtherStore 在 Controller 内 0 引用 |
| Write 字段 | **否** | 5 个 Write 的 Request 字段无 1 处来自 $scope.edit |
| State 出口 | **否** | 0 处 $state.go（已确认） |

### 16.3 与入口的对应关系

| 入口 | $stateParams.edit | $scope.edit | 实际行为 |
|---|---|---|---|
| beginCustomerCheckin success | **未传** | false | （optometryCtrl $state.go 不传 edit） |
| fnMap "修改" | **"true"** | true | （optometryCtrl $state.go 传 edit: "true"） |

**关键发现**：
- `$scope.edit` 是**纯标记字段**，**Controller 内 0 引用**（除复制到 showOtherStore）
- HTML 可能基于此分流 UI（F 边界）

### 16.4 是否存在"新增 vs 修改" API 分流

**否**（S1-108 结论保持）。

- 5 个 Write 均不依赖 $scope.edit
- 4 个主要 Read 均不依赖 $scope.edit
- 业务逻辑**对称处理**

---

## 17. Scope 共享

### 17.1 $scope.medicalRecord 共享图

| 共享者 | 引用方式 | 行号 | A-F |
|---|---|---|---|
| `getMedicalRecord` (Read API) | 整体赋值（写入） | L35419 | A |
| `saleInfo.inputVal`（派生） | `$scope.medicalRecord.secondDoctorName` | L35433 | A |
| `saleInfo.id`（派生） | `$scope.medicalRecord.secondDoctorId` | L35434 | A |
| `saleInfo.fn` 内部（FN_promiseCall 入参） | `response.object.patientId`/`customerId`（实际不用 $scope.medicalRecord.xxx） | L35440, L35445 | A |

**关键观察**：
- `$scope.medicalRecord` 仅有 2 个**字段级** Consumer
- 没有**对象整体共享**（除 1 次整体赋值）

### 17.2 $scope.medicalRecordId 共享图

| 共享者 | 引用方式 | 行号 | A-F |
|---|---|---|---|
| `getMedicalRecord` Request | `{ id: $scope.medicalRecordId }` | L35417 | A |
| `updateMedicalRecord` FN Request | `{ id: $scope.medicalRecordId }` | L35425 | A |
| `getMethodGlassRecordVo` Request | `{ medicalRecordId: $scope.medicalRecordId }` | L35605 | A |
| `GetMethodGlassRecordVo` Request | 同上 | L35605 | A |
| `saveChufang` 函数内（派生） | `$scope.object.medicalRecordId = $scope.medicalRecordId` | L35640 | A |
| `printChufang` 对象（派生） | `$scope.printChufang.medicalRecordId = $scope.medicalRecordId` | L35653 | A |
| `getMedicalProductVoList` Request | `{ medicalRecordId: $scope.medicalRecordId }` | L35686 | A |
| `GetMedicalProductVoList` Request | 同上 | L35686 | A |
| `addStore` 对象（派生） | `$scope.addStore.medicalRecordId = $scope.medicalRecordId` | L35816 | A |
| `printShoufei.options[0].param`（静态定义） | `{ medicalRecordId: $scope.medicalRecordId, payedStatus: 0 }` | L35842 | A |
| `save` Request | `{ medicalRecordId: $scope.medicalRecordId, ... }` | L35947 | A |

**共享统计**：11 处下游使用（10 直接 + Init）

### 17.3 $scope.edit 共享图

| 共享者 | 引用方式 | 行号 | A-F |
|---|---|---|---|
| Init | `= $stateParams.edit === "true"` | L35389 | A |
| `showOtherStore`（派生） | `$scope.showOtherStore = $scope.edit` | L35409 | A |

**共享统计**：1 字段级派生（Controller 内 0 处实际使用 $scope.showOtherStore）

### 17.4 $scope.object 共享图

| 共享者 | 引用方式 | 行号 | A-F |
|---|---|---|---|
| `getMedicalRecord` success（写入 secondDoctorId） | `$scope.object.secondDoctorId = saleInfo.id` | L35435 | A |
| `getMethodGlassRecordVo` for-in 覆盖 | `for (var i in $scope.object) { $scope.object[i] = methodGlassRecord[i]; }` | L35613-L35620 | A |
| `update` 函数 | `$scope.object[key]` | L35625 | A |
| `update2` 函数 | `$scope.object[key] = ""` | L35632 | A |
| `saveChufang` 函数（写入 medicalRecordId） | `$scope.object.medicalRecordId = $scope.medicalRecordId` | L35640 | A |
| `saveChufang` 函数（删除 lastRxTime） | `delete $scope.object.lastRxTime` | L35642 | A |
| `saveChufang` 函数（Request 字段级） | `$scope.object.secondDoctorId` | L35637 | A |
| `updateMethodGlassRecord` Write Request | `saveOrQuery("...", $scope.object)` | L35644 | A |
| `glassesInfo` Init（派生自 object 字段） | `model1Keyword1: $scope.object.right15` 等 | L35763-L35766 | A |

**共享统计**：9 处下游使用 / 4 处写入

### 17.5 $scope.glassesInfo 共享图

| 共享者 | 引用方式 | 行号 | A-F |
|---|---|---|---|
| `processBasicData`（写入 12 字段） | `$scope.glassesInfo["brandId" + signType] = brand.id` 等 | L35741-L35752 | A |
| `glassesInfo` Init（写入 model1Keyword/model2Keyword） | `model1Keyword1: $scope.object.right15` 等 | L35763-L35766 | A |
| `searchProductList`（读取 7 字段） | `$scope.glassesInfo["brandId" + num]` 等 | L35778-L35793 | A |
| `setProduct`（写入 2 字段） | `$scope.glassesInfo["keyword" + key] = product.product.productName` | L35806-L35807 | A |
| `queryStore`（读取 5 字段 + 写入 5-9 字段） | `$scope.glassesInfo["..."+key]` | L35849-L35907 | A |
| `save`（读取 4 字段） | `$scope.glassesInfo["productSkuId" + i]` 等 | L35915-L35925 | A |

**共享统计**：6 处下游使用 / 3 处写入

### 17.6 $scope.tempShop 共享图

| 共享者 | 引用方式 | 行号 |
|---|---|---|
| `GetMedicalProductVoList` 派生（写入） | `$scope.tempShop = tempList` | L35723 |
| `processBasicData` 消费（读取） | `$scope.tempShop.forEach(function (v) {...})` | L35730 |

### 17.7 $scope.stockInSkuList 共享图

| 共享者 | 引用方式 | 行号 |
|---|---|---|
| Init 空数组 | `$scope.stockInSkuList = []` | L35813 |
| `GetMedicalProductVoList` 派生（写入） | `$scope.stockInSkuList = list` | L35724 |
| `addStore.callback` 消费 | `$scope.stockInSkuList.push(info)` | L35821 |
| `deleteReceipt` 消费 | `$scope["" + key].splice(index, 1)`（`key = "stockInSkuList"` 默认） | L35833 |
| `save` 消费 | `$scope.stockInSkuList.forEach(...)` | L35929 |

### 17.8 $scope.userInfo 共享图

| 共享者 | 引用方式 | 行号 |
|---|---|---|
| Init 空对象 | `$scope.userInfo = {}` | L35414 |
| `getMedicalRecord` FN_promiseCall success（写入 15 字段） | `$scope.userInfo = { ... }` | L35451-L35466 |
| `showCommon` 写入 | `$scope.userInfo.selectChannelModal = true` | L35479 |
| `upimg.call` 写入 | `$scope.userInfo.avatar = img` | L35487 |
| `updatePatient` 消费（分解为局部变量） | `var _$scope$userInfo = $scope.userInfo, ...` | L35498-L35507 |

### 17.9 同值 ≠ 同对象

**关键判断**：
- `$scope.medicalRecord` 和 `$scope.userInfo` **不同对象**（前者是 medicalRecord，后者是 patient+customer 合并体）
- `$scope.lockStorehouseId` 和 `stockInSkuList[].lockStorehouseId` **不同对象**（前者是单值，后者是 productVoList 元素字段）
- `$scope.object.medicalRecordId` 和 `$scope.medicalRecordId` **不同值**（前者来自 Init 复制，但**写入时机不同**：saveChufang 调用时；后者 Init 即时）
- `$scope.object.secondDoctorId` 两次写入：
  - L35435 写入 saleInfo.id（getMedicalRecord success 时）
  - L35421 saleInfo.fn 内部 `$scope.object.secondDoctorId = this.id`（saleInfo 触发时覆盖）

### 17.10 same Scope reference / copied object 区分

| Scope | 类别 | 备注 |
|---|---|---|
| `$scope.medicalRecord` | same reference | L35419 整体赋值后保持 |
| `$scope.medicalRecordId` | primitive only | 字符串/数字字面量 |
| `$scope.edit` | primitive only | Boolean |
| `$scope.object` | same reference + field mutation | for-in 覆盖字段，saleInfo.fn 覆盖字段 |
| `$scope.glassesInfo` | same reference + field mutation | processBasicData 写入 12 字段，glassesInfo Init 写入 4 字段 |
| `$scope.tempShop` | same reference（数组） | forEach 不修改 |
| `$scope.stockInSkuList` | same reference（数组） | push/splice 修改 |
| `$scope.userInfo` | same reference + field mutation | 整体赋值后字段读写 |
| `$scope.lockStorehouseId` | primitive only | 数字/字符串 |
| `$scope.companyName` | primitive only | 字符串 |

---

## 18. clone / copy

### 18.1 搜索结果

```powershell
Select-String -Path 'controller.js' -Pattern 'angular\.copy|Object\.assign|JSON\.parse\(JSON|clone|copy' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

### 18.2 结论

**当前 Controller 未观察到对象 clone/copy 机制**。

- 0 处 `angular.copy(...)` 调用
- 0 处 `Object.assign(...)` 调用
- 0 处 `JSON.parse(JSON.stringify(...))` 调用
- 0 处 `.clone()` 方法调用
- 0 处 `.copy()` 方法调用

### 18.3 实际数据传递方式

| 传递方式 | 实际用法 | 行号 |
|---|---|---|
| 整体赋值 | `$scope.medicalRecord = response.object` | L35419 |
| 字段级复制 | `$scope.object.medicalRecordId = $scope.medicalRecordId` | L35640 |
| 派生（局部变量） | `saleInfo.inputVal = $scope.medicalRecord.secondDoctorName` | L35433 |
| 派生（局部对象构造） | `var patient = { id: patientId, ... }` | L35509-L35516 |
| for-in 复制 | `for (var i in $scope.object) { $scope.object[i] = methodGlassRecord[i]; }` | L35613-L35620 |
| 解构 | `var { unLockExistSkuCount, productSku } = res.result.list[0]` | L35893-L35895 |

**注**：`for-in` 循环和 `var {...} = ...` 解构是字段级复制/解构，**不构成对象整体 clone**。

---

## 19. Popup

### 19.1 Popup.notice 全部调用（11 处）

| 行号 | 触发函数 | 消息 | 条件 | 后续 |
|---:|---|---|---|---|
| 35530 | updatePatient | "请输入正确的手机号" | `customer.linkMobile && !window.Win_VerifyMobile(customer.linkMobile)` | return |
| 35608 | GetMethodGlassRecordVo | `res.errmsg` | `res.status == 1` | return |
| 35638 | saveChufang | "请选择视光师!" | `!$scope.object.secondDoctorId` | return |
| 35667 | queryStorehouseId | "没有仓库!" | `!res.result.count` | return |
| 35689 | GetMedicalProductVoList | `res.errmsg` | `res.status == 1` | return |
| 35801 | searchProductList | "没有该规格的商品" | `!res.count` | return |
| 35831 | deleteReceipt | `res.errmsg` | `res.status == 1` | return |
| 35886 | queryStore | `res.errmsg` | `res.status == 1` | return |
| 35943 | save | "请添加商品！" | `!medicalProductParamListJson.length` | return |
| 35952 | save | `res.errmsg` | `res.status == 1` | return |
| 35954 | save | "保存成功!" | （success 路径） | + `$scope.GetMedicalProductVoList()` |
| 35540 | updatePatient (FN_promiseCall success) | "修改成功!" | （success 路径，$timeout 内） | 无 |

**总计**：12 处（其中 L35540 在 $timeout 内）

### 19.2 Popup 形式

全部为 `Popup.notice(msg, ?, ?)`：
- 大多数为 1 参数（msg）
- 0 处 callback（无第 3 参数调用）
- 0 处 duration（第 2 参数显式值，源码未提供）

---

## 20. timeout / callback

### 20.1 $timeout 调用（3 处）

| 行号 | 触发函数 | 内容 | 用途 | A-F |
|---:|---|---|---|---|
| 35448-35467 | getMedicalRecord FN_promiseCall success | `$scope.userInfo = { ... }` | 延迟 userInfo 赋值 | A |
| 35486-35489 | upimg.call | `$scope.userInfo.avatar = img` | 延迟 avatar 赋值 | A |
| 35539-35541 | updatePatient FN_promiseCall success | `Popup.notice("修改成功!")` | 延迟 Popup | A |

**$timeout 形式**：全部为 `$timeout(fn)` 1 参数，0 处显式 delay（默认 0ms）

### 20.2 callback

| 位置 | 形式 | 用途 | A-F |
|---|---|---|---|
| L35820 `$scope.addStore.callback` | 弹窗 callback（外部触发） | push info 到 $scope.stockInSkuList | A |
| saleInfo.fn | 局部 saleInfo 对象 fn 字段 | HTML 触发 → updateMedicalRecord + saveChufang | A |

### 20.3 .then 链

10 处 saveOrQuery + 1 处 ListFactory + 3 处 FN_promiseCall = 14 处 `.then(...)` 链

### 20.4 window. 全部调用

| 行号 | 调用 | 用途 | A-F |
|---:|---|---|---|
| 35385 | `window.getStockSet(ObjectFactory, "enableNegativeStock")` | 读取库存设置 | A |
| 35422 | `window.FN_promiseCall(ObjectFactory, [{...}])` | 隐式 Write | A |
| 35437 | `window.FN_promiseCall(ObjectFactory, [{...}, {...}])` | 隐式 Read | A |
| 35529 | `window.Win_VerifyMobile(customer.linkMobile)` | 手机号校验 | A |
| 35532 | `window.FN_promiseCall(ObjectFactory, [{...}, {...}])` | 隐式 Write | A |
| 35547-35554 | `window.optionsObj.getQiuJing/getEyeDistance/sightArr` | 工具变量初始化 | A |
| 35924 | `window.optionsObj.glassesSignType[i]` | save Write Request 字段 | A |

---

## 21. State 出口

### 21.1 $state.go 全量

```powershell
Select-String -Path 'controller.js' -Pattern '\$state\.go' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

**A 级确认**：optometryGlassesCtrl 范围内 **0 处 `$state.go`**。

### 21.2 optometryGlassesCtrl 离开页面的其它机制

| 机制 | 出现次数 | 备注 |
|---|---:|---|
| `$state.go` | 0 | - |
| `window.open` | 0 | - |
| `location.href` | 0 | - |
| `window.location` | 0 | - |
| `window.location.href` | 0 | - |
| `window.location.assign` | 0 | - |

**F 边界**：离开方式由 HTML 决定（`<a ui-sref>`、浏览器后退等），不可得

---

## 22. optometryList / optometryLogList

### 22.1 引用扫描

```powershell
Select-String -Path 'controller.js' -Pattern 'optometryList|optometryLogList' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

**A 级确认**：optometryGlassesCtrl 范围内 **0 处** 引用 optometryList 或 optometryLogList。

### 22.2 S1-108 / S1-107 一致性

S1-108 已确认：
- L36034 `$state.go("optometryList", {}, { reload: true })` 在 optometryListCtrl 范围内
- L36050 `$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })` 在 optometryListCtrl 范围内
- optometryGlassesCtrl **0 个** State 出口

S1-109 重新确认：A 级，**0 处**。

### 22.3 接收方 Controller（仅参考，不展开）

| State | Controller | 注册位置 | 第一个 $stateParams Consumer |
|---|---|---:|---|
| optometryList | optometryListCtrl | L35962 | （L35962+ 范围，本轮不展开） |
| optometryLogList | optometryLogListCtrl | L35899 | `L35902 $scope.obj.uartDeviceId = $stateParams.uartDeviceId;` |

---

## 23. 主数据对象 DAG

### 23.1 入口链（StateParams → $scope → Read → $scope.medicalRecord → 派生 → Write）

```
[外部入口]
optometryCtrl.beginCustomerCheckin success
  → $state.go("optometryGlasses", { medicalRecordId: ... })
optometryCtrl.fnMap "修改"
  → $state.go("optometryGlasses", { medicalRecordId: ..., edit: "true" })
  (S1-106/107 锁定)

↓

[Controller 入口 - optometryGlassesCtrl L35383]
$stateParams.medicalRecordId (L35388) → $scope.medicalRecordId
$stateParams.edit (L35389) → $scope.edit (= "true" or false)

↓

[Init 立即执行 - 5 个]

[1] window.getStockSet (L35385) 异步
    └─ $scope.enableNegativeStock

[2] GetMethodGlassRecordVo (L35623)
    Read /admin/getMethodGlassRecordVo.json
      Request: { medicalRecordId: $scope.medicalRecordId }
    └─ for-in $scope.object 覆盖 27+ 字段
    └─ processBasicData($scope.object → $scope.glassesInfo[...+signType])

[3] queryCompanyName (L35682)
    Read /admin/getCompanyOfMine.json
      Request: (无)
    └─ $scope.companyName = res.object.companyName (L35677)
    └─ $scope.queryStorehouseId(res.object.id) (L35678) ───┐
                                                          │
[4] queryStorehouseId (L35662)                          │
    Read /admin/selectStorehouseListOfCompany.json  ←────┘
      Request: { companyId, mcTypeSortType: "ASC" }
    └─ $scope.lockStorehouseId = res.result.list[0].id (L35669)

[5] GetMedicalProductVoList (L35755)
    Read /admin/getMedicalProductVoList.json
      Request: { medicalRecordId: $scope.medicalRecordId }
    └─ res.result.list.forEach(stock)
         ├─ stock.medicalProductSign → tempList → $scope.tempShop (L35723)
         └─ else → list (19 字段映射) → $scope.stockInSkuList (L35724)
    └─ $scope.processBasicData()
         └─ $scope.tempShop.forEach → $scope.glassesInfo 12 字段

[6] getMedicalRecord (L35958) ← 最后执行
    Read /admin/getMedicalRecord.json
      Request: { id: $scope.medicalRecordId }
    └─ $scope.medicalRecord = response.object (L35419)
       ├─ response.object.secondDoctorName → saleInfo.inputVal (L35433)
       ├─ response.object.secondDoctorId → saleInfo.id (L35434) → $scope.object.secondDoctorId (L35435)
       ├─ $scope.saleInfo = saleInfo (L35436)
       └─ window.FN_promiseCall(ObjectFactory, [
            { url: "getPatientInfo", param: { id: response.object.patientId } },
            { url: "getCustomerVo", param: { customerId: response.object.customerId } }
          ]) (L35437)
            └─ $scope.userInfo = { 15 字段 } (L35451-L35466)

↓

[派生 / 中间对象]

$saleInfo (saleInfo fnMap 风格)
  ├─ .fn = function() { updateMedicalRecord + saveChufang }
  ├─ .inputVal = medicalRecord.secondDoctorName
  ├─ .id = medicalRecord.secondDoctorId
  └─ (HTML 触发 fn 调用)

$scope.saleInfo = saleInfo (L35436)

$scope.userInfo = { patientId, avatar, patientName, patientGender, 
                    patientBirthday, patientRemark, customerId, 
                    linkMobile, channel, channelTagId, name, gender, mobile }

$scope.object = { 27+ right*/left* 字段, medicalRecordId, secondDoctorId, lastRxTime }
  来源: Init 定义 + for-in 覆盖 + saveChufang 注入

$scope.glassesInfo = { brandName1-3, brandId1-3, model1Keyword1-2, model2Keyword1-2, ... }
  来源: Init + processBasicData + queryStore

$scope.lockStorehouseId = 数字
  来源: queryStorehouseId (L35669)

$scope.companyName = 字符串
  来源: queryCompanyName (L35677)

$scope.tempShop = Array<stock>
  来源: GetMedicalProductVoList (L35723)

$scope.stockInSkuList = Array<19-字段stock>
  来源: GetMedicalProductVoList (L35724) + addStore.callback (L35821)

↓

[用户动作 → Write]

[Write #1] saleInfo.fn() (外部 HTML 触发)
    └─ $scope.object.secondDoctorId = this.id (L35421)
    └─ FN_promiseCall updateMedicalRecord
         └─ $scope.saveChufang()

[Write #2] $scope.saveChufang() (外部 HTML 触发 / saleInfo.fn 链式)
    └─ $scope.object.medicalRecordId = $scope.medicalRecordId (L35640)
    └─ delete $scope.object.lastRxTime if empty (L35641-L35642)
    └─ saveOrQuery updateMethodGlassRecord.json
         Request: $scope.object
         Success: (空)

[Write #3] $scope.updatePatient() (外部 HTML 触发)
    └─ 校验 linkMobile
    └─ 构造 patient + customer 局部对象
    └─ FN_promiseCall savePatientInfo + saveCustomerInfo
         Success: $timeout(Popup.notice("修改成功!"))

[Write #4] $scope.save() (外部 HTML 触发)
    └─ 构造 medicalProductParamListJson (1-3 循环 + stockInSkuList)
    └─ saveOrQuery saveMedicalProductListOfSmallVersion.json
         Request: { medicalRecordId, medicalProductParamListJson }
         Success: Popup.notice + $scope.GetMedicalProductVoList() (Refresh)

↓

[State 出口]
0 处
```

### 23.2 主数据对象关系图

```
                     [optometryGlasses State]
                              │
                              ↓
                     $stateParams.medicalRecordId
                              ↓
                     $scope.medicalRecordId
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
        getMedicalRecord  GetMethodGlass  GetMedicalProductVoList
        (L35416)         RecordVo        (L35685)
                          (L35604)
        $scope.medicalRecord  $scope.object  $scope.tempShop
        (整体赋值)         (for-in 覆盖)  $scope.stockInSkuList
                │             │
                ↓             ↓
        $scope.saleInfo  $scope.glassesInfo
        (fnMap 风格)     (processBasicData 派生)
                │             │
        saleInfo.fn      queryStore (L35884)
                │             │
                ↓             ↓
        updateMedicalRecord  glassesInfo 字段更新
        (FN 隐式 Write)     (unLockExist, marketPrice, kpiPrice)
                │
        $scope.saveChufang()
                │
        updateMethodGlassRecord.json
                │
                ↓
        (Write 链式完成)
                │
        ┌───────┴───────┐
        ↓               ↓
        $scope.userInfo  $scope.lockStorehouseId
        (patient+customer) (queryStorehouseId 派生)
        │               │
        ↓               ↓
        updatePatient    $scope.save
        (FN 隐式 Write)  (saveMedicalProductListOfSmallVersion)
        │               │
        ↓               ↓
        savePatientInfo  medicalProductParamListJson
        saveCustomerInfo  │
                          ↓
                          [Write 链式完成 + Refresh]
                          ($scope.GetMedicalProductVoList 刷新)
```

---

## 24. 26 项增量矩阵

| # | 审计项 | 文件 | 行号 | A-F | L1/L2/L3 |
|---:|---|---|---|---|---|
| 01 | Controller 范围 | controller.js | L35383-L35959 | A | L1 |
| 02 | API unique | controller.js | 见 §3.3 | A | L2 |
| 03 | API call site | controller.js | 见 §3.1, §3.2 | A | L2 |
| 04 | Read unique | controller.js | 见 §3.3 | A | L2 |
| 05 | Write unique | controller.js | 见 §3.3 | A | L2 |
| 06 | ObjectFactory | controller.js | 见 §4.1 | A | L2 |
| 07 | ListFactory | controller.js | L35797 | A | L2 |
| 08 | $scope.medicalRecord | controller.js | L35390, L35416, L35419, L35433, L35434 | A | L2 |
| 09 | medicalRecord 字段全集 | controller.js | L35433-L35434 | A | L3 |
| 10 | medicalRecord 派生对象 | controller.js | L35433-L35436, L35440, L35445 | A | L3 |
| 11 | Read Response 落点 | controller.js | 见 §10 | A | L3 |
| 12 | API 对象分类 | controller.js | 见 §11 | A | L2 |
| 13 | Read→Read | controller.js | L35678 → L35662, L35437 → L35437 | A | L3 |
| 14 | Read→Write | controller.js | 见 §13 | A | L3 |
| 15 | Write→Read | controller.js | L35955 → L35685 | A | L3 |
| 16 | Write Request 字段来源 | controller.js | 见 §15 | A | L3 |
| 17 | medicalRecordId 新路径 | controller.js | 0 处新增 | A | L2 |
| 18 | edit Consumer | controller.js | L35389, L35409 | A | L2 |
| 19 | edit 对 API 影响 | controller.js | 0 处 | A | L2 |
| 20 | Scope 共享 | controller.js | 见 §17 | A | L3 |
| 21 | clone/copy | controller.js | 0 处 | A | L2 |
| 22 | Popup | controller.js | 见 §19.1 | A | L2 |
| 23 | timeout/callback | controller.js | 见 §20 | A | L2 |
| 24 | State 出口 | controller.js | 0 处 $state.go | A | L1 |
| 25 | optometryList/optometryLogList 边界 | controller.js | 0 处 | A | L1 |
| 26 | 最终主数据 DAG | controller.js | 见 §23 | A | L3 |

### 24.1 A-F 分布

| 等级 | 项数 | 备注 |
|---|---:|---|
| A | 26 | 全部 A 级 |
| B | 0 | - |
| C | 0 | - |
| D | 0 | - |
| E | 0 | 严禁 E 升 A |
| F | 0 | **S1-108 的 F 边界 1 项已闭合（$scope.lockStorehouseId 来源）** |

### 24.2 L1/L2/L3 分布

| 级别 | 项数 | 项 |
|---|---:|---|
| L1 | 4 | 01, 17, 24, 25 |
| L2 | 10 | 02, 03, 04, 05, 06, 07, 12, 18, 19, 21, 22, 23 |
| L3 | 12 | 08, 09, 10, 11, 13, 14, 15, 16, 20, 26 |

### 24.3 F 边界（与 S1-108 对比）

| F 项 | S1-108 | S1-109 |
|---|---|---|
| `$scope.lockStorehouseId` 来源 | F（不可得） | **A 级闭合**（queryStorehouseId 派生） |
| optometryGlasses State 配置 | F | F（无变化） |
| HTML 触发函数 | F | F（无变化） |
| `$scope.showOtherStore` 等 UI 字段消费 | F | F（无变化） |
| 离开 optometryGlassesCtrl 方式 | F | F（无变化） |
| `response.object` 实际字段集 | F | F（无变化） |

**S1-109 关键贡献**：F 边界从 5 项减至 5 项（仅减少 1 项），但已闭合的是 S1-108 中影响 Write Request 完整性的关键 F 项

---

## 25. A-F 总结

| 等级 | 数量 | 比例 | 备注 |
|---|---:|---:|---|
| A | 26 | 100% | 所有 26 项均为 A 级直接源码证据 |
| B | 0 | 0% | - |
| C | 0 | 0% | - |
| D | 0 | 0% | - |
| E | 0 | 0% | 严禁 E 升 A |
| F | 0 | 0% | 5 项 S1-108 标记的 F 中有 1 项已闭合 |

---

## 26. L1/L2/L3 总结

| 级别 | 含义 | 数量 | 项 |
|---|---|---:|---|
| L1 | Controller 注册层（入口、出口、Controller 边界） | 4 | 01, 17, 24, 25 |
| L2 | Controller 内部层（API、Factory、StateParams、Popup、timeout） | 10 | 02, 03, 04, 05, 06, 07, 12, 18, 19, 21, 22, 23 |
| L3 | 字段级层（Scope 字段、字段消费、派生、provenance） | 12 | 08, 09, 10, 11, 13, 14, 15, 16, 20, 26 |

---

## 27. F 边界（与 S1-108 对比）

| # | F 项 | S1-108 状态 | S1-109 状态 | 备注 |
|---:|---|---|---|---|
| 1 | optometryGlasses State 配置 | F | F | controller.js 0 处 `.state()` 注册 |
| 2 | HTML 触发函数 | F | F | 7 untracked HTML 中 0 处 optometry 模板 |
| 3 | `$scope.showOtherStore` / `$scope.showPerfectInfo` / `$scope.enableNegativeStock` 消费 | F | F | Controller 内 0 引用 |
| 4 | 离开 optometryGlassesCtrl 的具体方式 | F | F | 0 处 $state.go / window.open / location.href |
| 5 | `response.object` 实际字段集 | F | F | 仅访问 4 字段（patientId/customerId/secondDoctorName/secondDoctorId） |
| 6 | `$scope.lockStorehouseId` 来源 | **F（不可得）** | **A 级闭合** | queryStorehouseId L35669 派生 |

**S1-108 → S1-109 F 边界变化**：1 项 F → A（$scope.lockStorehouseId 来源）

---

## 28. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态源码分析 | ✅ |
| 2. API actual | 0（无任何 F5/F6/FN_promiseCall 实际调用） |
| 3. Write actual | 0 |
| 4. 不打开真实业务页面 | ✅ |
| 5. 不执行业务动作 | ✅ |
| 6. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-108 一致） |
| 7. 不修改 7 HTML | ✅ |
| 8. 不修改历史 MD（154-169） | ✅（**165/166/167/168/169 全部未改**） |
| 9. P0 = 54 冻结 | ✅ |
| 10. P1 = 8 冻结 | ✅ |
| 11. 10 untracked 原样保留 | ✅ |
| 12. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 29. 最终结论

### 29.1 核心发现

1. **Controller 范围与统计**：
   - L35383-L35959（577 行）
   - 14 unique API（9 Read + 5 Write）
   - 14 call site（10 saveOrQuery + 5 FN_promiseCall URL - 1 重复 = 14）
   - 21 个 $scope 函数
   - 0 个 $state.go 出口

2. **medicalRecord 数据链**：
   - 入口：`$stateParams.medicalRecordId` → `$scope.medicalRecordId` (L35388) → getMedicalRecord (L35416) → `$scope.medicalRecord = response.object` (L35419)
   - **实际消费字段仅 2 个**：`.secondDoctorName` (L35433) + `.secondDoctorId` (L35434)
   - 整体赋值 1 次（L35419），**0 次** clone/copy
   - 派生到：saleInfo.inputVal/id, $scope.saleInfo, $scope.object.secondDoctorId, $scope.userInfo（通过 FN_promiseCall getPatientInfo + getCustomerVo 链式）

3. **API 数据流闭合**：
   - **Read→Read 链 2 条**：getCompanyOfMine → queryStorehouseId；getMedicalRecord → getPatientInfo + getCustomerVo
   - **Read→Write 链 4 条**：5 个 Write 全部有上游 Read 来源
   - **Write→Read 链 1 条**：saveMedicalProductListOfSmallVersion → GetMedicalProductVoList 刷新
   - **Write→Write 链 1 条**：updateMedicalRecord → saveChufang → updateMethodGlassRecord

4. **S1-108 错误纠正（重要）**：
   - S1-108 标记 `$scope.lockStorehouseId` 为 F 边界（来源不可得）
   - S1-109 闭合：来源为 `selectStorehouseListOfCompany.json` 的 `res.result.list[0].id`（L35669）
   - 完整派生链：queryCompanyName (L35682 Init) → queryStorehouseId (L35678) → selectStorehouseListOfCompany (L35662) → $scope.lockStorehouseId (L35669) → save (L35919) → saveMedicalProductListOfSmallVersion Request

5. **medicalRecordId 路径增量**：
   - S1-108 已锁定 5 类路径（S1-105~S1-107 来源）
   - S1-109 在 optometryGlassesCtrl 范围内**未发现**新路径
   - 5 类路径保持不变

6. **edit 模式**：
   - 2 处出现（Init + showOtherStore 复制）
   - **0 处**对 API/State/Init/页面数据有影响
   - Controller 内 0 处使用 $scope.showOtherStore
   - HTML 可能基于此分流 UI（F 边界）

7. **Scope 共享与 clone/copy**：
   - 0 处 `angular.copy` / `Object.assign` / `JSON.parse(JSON.stringify(...))` / `.clone()` / `.copy()`
   - 数据传递主要靠：整体赋值、字段级复制、局部变量派生、for-in 复制、解构
   - 0 处同对象跨函数共享（除 $scope.xxx 整体引用）

8. **Factory 复用**：
   - 9 个 ObjectFactory：全部匿名 new，**0 处复用**
   - 1 个 ListFactory：命名 `$scope.getCorpListFactory`，**0 处复用**（仅在 searchProductList 内重建）
   - 3 处 FN_promiseCall：使用 DI 注入的 ObjectFactory 引用

### 29.2 与 S1-108 对比

| 项 | S1-108 | S1-109 | 变化 |
|---|---|---|---|
| API unique | 14 | 14 | 一致 |
| API call site | 14 | 14 | 一致 |
| Read unique | 9 | 9 | 一致 |
| Write unique | 5 | 5 | 一致 |
| Factory 数量 | 9 OF + 1 LF | 9 OF + 1 LF | 一致 |
| State 出口 | 0 | 0 | 一致 |
| `$scope.lockStorehouseId` 来源 | F | **A** | **闭合** |
| medicalRecord 字段消费 | 2 字段 | 2 字段 | 一致 |
| medicalRecordId 路径 | 5 类 | 5 类 | 一致（无新路径） |

### 29.3 S1-108 错误纠正详细记录

**S1-108 第 14.5 节**：
> F 边界说明：$scope.lockStorehouseId 在 $scope.save 函数（L35919）作为 lockStorehouseId 字段被引用，但本 Controller 范围内**0 处赋值**。可能来源：HTML ng-init / 父 Controller / 全局 window 变量。

**S1-109 闭合证据**：
- `controller.js` L35661-L35671 `$scope.queryStorehouseId` 函数定义
- `controller.js` L35669 `$scope.lockStorehouseId = res.result.list[0].id;`（**A 级源码证据**）
- `controller.js` L35675-L35681 `$scope.queryCompanyName` 函数定义
- `controller.js` L35678 `$scope.queryStorehouseId(res.object.id);`（链式触发）
- `controller.js` L35682 `$scope.queryCompanyName();`（Init 立即执行）

**S1-108 → S1-109 修正结论**：
- `$scope.lockStorehouseId` 的来源是 **`getCompanyOfMine.json` → `selectStorehouseListOfCompany.json` 双层 Read 链**（A 级确认）
- 不依赖 HTML ng-init / 父 Controller / 全局 window 变量
- save (L35911) 触发时，$scope.lockStorehouseId 已被 Init 流程设置

**注**：本轮**不修改 S1-108 文档**（绝对红线 8：154-169 全部不修改），仅在本轮 170 文档中记录 S1-108 错误纠正。

### 29.4 不再发散

- **不进入** optometryListCtrl 内部 API 逆向（仅确认 0 引用）
- **不进入** optometryLogListCtrl 内部 API 逆向（仅确认 0 引用）
- **不修改** 历史 MD（154-169）
- **不重新审计** optometryCtrl（已在 S1-105/106/107/108 完成）

### 29.5 关键修复点

S1-109 修复了 S1-108 的 1 个关键 F 边界：`$scope.lockStorehouseId` 来源已闭合。这使得：

- `saveMedicalProductListOfSmallVersion` Request 字段 provenance **100% A 级**（不再有 F）
- 4 条 Read→Write 链全部 A 级
- 5 个 Write 的所有 Request 字段**全部可溯源**

---

**审计完成。本文档为 170 号，提交后将形成 tracked=179。**
