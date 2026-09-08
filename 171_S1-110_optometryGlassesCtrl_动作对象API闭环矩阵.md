# S1-110 optometryGlassesCtrl 动作—对象—API 闭环矩阵

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML（无 optometry 模板，F 边界）
> - Controller 范围：L35383 – L35959（577 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-109（HEAD=99bbdb5，tracked=179）
> - 本轮**重点**：三维闭环（Action × Object × API），不复述 S1-108/109 的 API 计数和路径统计
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-170）/ 修改 7 HTML / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **Controller 源**：`optometryGlassesCtrl`，注册于 `controller.js` L35383
- **行范围**：L35383 – L35959（577 行）
- **本轮目标**：把"动作"与"对象"与"API"做三维闭环，最终形成【optometryGlassesCtrl 动作—对象—API DAG】
- **S1-108/109 错误纠正**（本轮新增）：
  - S1-108/109 标记 saveOrQuery call site 为 **10**
  - S1-110 重新扫描确认为 **9**（详见 §3 错误纠正）
  - S1-108/109 标记 call site 总数为 **14**
  - S1-110 重新扫描确认为 **13**（9 saveOrQuery + 1 ListFactory + 3 FN_promiseCall = 13 call sites；触发的 URL 总数 15；unique API 仍 14）

---

## 2. Controller 动作全集

### 2.1 全部 21 个 $scope 函数（按行号）

| # | 行号 | 函数名 | 类型 | 外部入口 | 直接调用 API | 间接调用函数 | A-F |
|---:|---:|---|---|---|---|---|---|
| 1 | 35391 | `$scope.tip` | 其它（空实现） | HTML 触发（F 边界） | 无 | 无 | A |
| 2 | 35392 | `$scope.prevent` | UI 工具（关闭 supplierList 浮层） | HTML 触发（F 边界） | 无 | 无 | A |
| 3 | 35410 | `$scope.upOther` | UI 工具（toggle） | HTML 触发（F 边界） | 无 | 无 | A |
| 4 | 35415 | `$scope.getMedicalRecord` | **Read API** | Init 立即执行（L35958） | getMedicalRecord.json | FN_promiseCall (getPatientInfo + getCustomerVo + updateMedicalRecord in saleInfo.fn) | A |
| 5 | 35478 | `$scope.showCommon` | UI 工具（modal 切换） | HTML 触发（F 边界） | 无 | 无 | A |
| 6 | 35492 | `$scope.updateImg` | 其它（空实现，return） | HTML 触发（F 边界） | 无 | 无 | A |
| 7 | 35496 | `$scope.updatePatient` | **Write API**（隐式 FN_promiseCall） | HTML 触发（F 边界） | savePatientInfo + saveCustomerInfo (FN) | 无 | A |
| 8 | 35603 | `$scope.GetMethodGlassRecordVo` | **Read API** | Init 立即执行（L35623） | getMethodGlassRecordVo.json | 无 | A |
| 9 | 35624 | `$scope.update` | 数据转换 + API helper | HTML 触发（F 边界） | saveMethodGlassRecord (via saveChufang) | $scope.queryStore, $scope.saveChufang | A |
| 10 | 35631 | `$scope.update2` | 数据转换 + API helper | HTML 触发（F 边界） | saveMethodGlassRecord (via saveChufang) | $scope.saveChufang | A |
| 11 | 35635 | `$scope.saveChufang` | **Write API** | HTML 触发（F 边界）/ 隐式触发（saleInfo.fn L35430） | updateMethodGlassRecord.json | 无 | A |
| 12 | 35661 | `$scope.queryStorehouseId` | **Read API** | 内部调用（queryCompanyName L35678） | selectStorehouseListOfCompany.json | 无 | A |
| 13 | 35674 | `$scope.queryCompanyName` | **Read API** | Init 立即执行（L35682） | getCompanyOfMine.json | $scope.queryStorehouseId | A |
| 14 | 35684 | `$scope.GetMedicalProductVoList` | **Read API** | Init 立即执行（L35755）+ save success（L35955） | getMedicalProductVoList.json | $scope.processBasicData | A |
| 15 | 35729 | `$scope.processBasicData` | 数据转换 | 内部调用（GetMedicalProductVoList L35725） | 无 | 无 | A |
| 16 | 35768 | `$scope.showsupplierList` | UI 工具 + API helper | HTML 触发（F 边界） | getProductSkuExistCountVoList.json (via searchProductList) | $scope.prevent, $scope.searchProductList | A |
| 17 | 35774 | `$scope.searchProductList` | **Read API**（ListFactory） | HTML 触发（F 边界） | getProductSkuExistCountVoList.json | $scope.getCorpListFactory.nextPage() | A |
| 18 | 35805 | `$scope.setProduct` | 数据转换 + API helper | HTML 触发（F 边界） | getProductSkuExistCountVoList.json (via queryStore) | $scope.queryStore | A |
| 19 | 35824 | `$scope.deleteReceipt` | **Read API** | HTML 触发（F 边界） | checkBeforeDeleteMedicalProduct.json | 无 | A |
| 20 | 35848 | `$scope.queryStore` | **Read API** | HTML 触发（F 边界） | getProductSkuExistCountVoList.json | 无 | A |
| 21 | 35911 | `$scope.save` | **Write API** | HTML 触发（F 边界） | saveMedicalProductListOfSmallVersion.json | $scope.GetMedicalProductVoList (success) | A |

**Init 立即执行**（注册即调用，无外部触发）：
- L35385 `window.getStockSet(...)`（异步，then 写入 $scope.enableNegativeStock）
- L35623 `$scope.GetMethodGlassRecordVo()`
- L35682 `$scope.queryCompanyName()`
- L35755 `$scope.GetMedicalProductVoList()`
- L35958 `$scope.getMedicalRecord()`

### 2.2 21 个函数分类

| 类型 | 数量 | 函数 |
|---|---:|---|
| Read API（直接调用 saveOrQuery/FN_promiseCall/ListFactory） | 10 | getMedicalRecord, GetMethodGlassRecordVo, queryStorehouseId, queryCompanyName, GetMedicalProductVoList, searchProductList, deleteReceipt, queryStore, updatePatient (FN), getMedicalRecord 内嵌的 FN_promiseCall Read (getPatientInfo + getCustomerVo) |
| Write API（直接调用 saveOrQuery/FN_promiseCall） | 5 | updatePatient, saveChufang, save, saleInfo.fn (FN, 隐式), updatePatient 内嵌的 FN_promiseCall Write (savePatientInfo + saveCustomerInfo) |
| API helper（间接调用 API） | 4 | update, update2, setProduct, showsupplierList |
| 数据转换 | 1 | processBasicData |
| UI 工具 | 4 | prevent, upOther, showCommon, tip |
| 其它 | 1 | updateImg（空实现） |

**注**：updatePatient 内嵌 1 个 FN_promiseCall Read（getPatientInfo + getCustomerVo）和 1 个 FN_promiseCall Write（savePatientInfo + saveCustomerInfo），因此 1 个函数实际触发 2 个 URL。

### 2.3 内部嵌套函数 / callback

| 位置 | 函数/对象 | 类型 | A-F |
|---|---|---|---|
| L35420-L35432 | `saleInfo.fn` | 局部 saleInfo 对象 fn 字段（fnMap 风格） | A |
| L35566-L35570 | `saleInfo.reset` | 局部 saleInfo 对象 reset 方法 | A |
| L35485-L35490 | `$scope.upimg.call` | 弹窗对象 callback | A |
| L35817-L35819 | `$scope.addStore.switch` | 弹窗对象方法 | A |
| L35820-L35822 | `$scope.addStore.callback` | 弹窗对象 callback | A |
| L35654-L35656 | `$scope.printChufang.print` | 弹窗对象方法 | A |
| L35844-L35846 | `$scope.printShoufei.print` | 弹窗对象方法 | A |
| L35798-L35803 | `$scope.getCorpListFactory.nextPage().then(...)` | ListFactory callback | A |
| L35447-L35468 | getMedicalRecord success → FN_promiseCall then | 嵌套 callback | A |
| L35429-L35431 | updateMedicalRecord success → $scope.saveChufang | Write success callback | A |
| L35422-L35428 | `saleInfo.fn` 内 FN_promiseCall updateMedicalRecord | 局部 saleInfo.fn 内部 Write | A |

**总计**：12 个内部嵌套函数/callback

---

## 3. 动作→API 完整矩阵

### 3.1 直接 API 调用矩阵

| 动作函数 | 行号 | 调用的 API（按顺序） | API 类型 | 同步/异步 | A-F |
|---|---:|---|---|---|---|
| `$scope.getMedicalRecord` | 35415-35470 | getMedicalRecord.json → FN_promiseCall [getPatientInfo, getCustomerVo] | Read | 异步链 | A |
| `$scope.GetMethodGlassRecordVo` | 35603-35622 | getMethodGlassRecordVo.json | Read | 异步 | A |
| `$scope.saveChufang` | 35635-35649 | updateMethodGlassRecord.json | **Write** | 异步 | A |
| `$scope.queryStorehouseId` | 35661-35671 | selectStorehouseListOfCompany.json | Read | 异步 | A |
| `$scope.queryCompanyName` | 35674-35681 | getCompanyOfMine.json | Read | 异步 | A |
| `$scope.GetMedicalProductVoList` | 35684-35728 | getMedicalProductVoList.json | Read | 异步 | A |
| `$scope.searchProductList` | 35774-35804 | getProductSkuExistCountVoList.json (ListFactory) | Read | 异步 | A |
| `$scope.deleteReceipt` | 35824-35835 | checkBeforeDeleteMedicalProduct.json | Read | 异步 | A |
| `$scope.queryStore` | 35848-35909 | getProductSkuExistCountVoList.json | Read | 异步 | A |
| `$scope.save` | 35911-35957 | saveMedicalProductListOfSmallVersion.json | **Write** | 异步 | A |
| `$scope.updatePatient` | 35496-35543 | FN_promiseCall [savePatientInfo, saveCustomerInfo] | **Write** | 异步 | A |
| `saleInfo.fn`（局部） | 35420-35432 | FN_promiseCall [updateMedicalRecord] | **Write** | 异步 | A |
| `$scope.update` | 35624-35630 | （不直接 API）→ $scope.queryStore + $scope.saveChufang | API helper | 异步链 | A |
| `$scope.update2` | 35631-35634 | （不直接 API）→ $scope.saveChufang | API helper | 异步链 | A |
| `$scope.setProduct` | 35805-35809 | （不直接 API）→ $scope.queryStore | API helper | 异步链 | A |
| `$scope.showsupplierList` | 35768-35773 | （不直接 API）→ $scope.searchProductList | API helper | 异步链 | A |

### 3.2 错误纠正：S1-108/109 call site 数字

**S1-108/109 数字**：
> call site 总数：14（10 saveOrQuery + 5 FN_promiseCall URL - 1 重复 = 14）

**S1-110 实际数字**（重新扫描）：

| 类型 | 行号清单 | 实际数 |
|---|---|---:|
| saveOrQuery call site | 35416, 35604, 35644, 35662, 35675, 35685, 35827, 35884, 35950 | **9**（S1-108/109 标 10，**错误**） |
| ListFactory call site | 35797 | 1 |
| FN_promiseCall call site (group) | 35422, 35437, 35532 | 3（每组 1-2 URL） |
| ajaxUrl 字符串引用 | 35557 | 1（saleInfo.ajaxUrl，未在本 Controller 实际调用） |
| **call site 总数** | 9 + 1 + 3 = **13** | 13（S1-108/109 标 14，**错误**） |

**触发的 URL 总数**：
- saveOrQuery 9 个 call site → 9 URL
- ListFactory 1 个 call site → 1 URL（getProductSkuExistCountVoList）
- FN_promiseCall 3 个 call site → 5 URL（1 + 2 + 2）
- **触发 URL 总数 = 15**

**unique API**：
- saveOrQuery URL：8 unique（getMedicalRecord, getMethodGlassRecordVo, updateMethodGlassRecord, selectStorehouseListOfCompany, getCompanyOfMine, getMedicalProductVoList, checkBeforeDeleteMedicalProduct, getProductSkuExistCountVoList, saveMedicalProductListOfSmallVersion = 9，**待确认**）
- ListFactory URL：1 unique（getProductSkuExistCountVoList，与 saveOrQuery 重复）
- FN_promiseCall URL：5 unique（updateMedicalRecord, getPatientInfo, getCustomerVo, savePatientInfo, saveCustomerInfo）
- **unique API 总数 = 9 + 5 - 1 = 13**（修正：S1-108/109 标 14 也需复核）

让我重新核对 saveOrQuery 触发的 unique URL：
1. /admin/getMedicalRecord.json
2. /admin/getMethodGlassRecordVo.json
3. /admin/updateMethodGlassRecord.json
4. /admin/selectStorehouseListOfCompany.json
5. /admin/getCompanyOfMine.json
6. /admin/getMedicalProductVoList.json
7. /admin/checkBeforeDeleteMedicalProduct.json
8. /admin/getProductSkuExistCountVoList.json
9. /admin/saveMedicalProductListOfSmallVersion.json

= 9 unique URL

加上 FN_promiseCall 5 unique = 14 unique。但 getProductSkuExistCountVoList 在 L35797 ListFactory 和 L35884 saveOrQuery 各调一次，unique 计数应去重。已去重后 = 14。

OK, unique API = 14 是正确的。

**S1-110 修正**：
- saveOrQuery call site: 9（不是 10）
- ListFactory call site: 1
- FN_promiseCall call site: 3
- call site 总数: 13（不是 14）
- unique API: 14（**不变**）

### 3.3 多 API 动作

| 动作函数 | 实际触发 API 数 | 详情 |
|---|---:|---|
| `$scope.getMedicalRecord` | 3 | getMedicalRecord → FN_promiseCall[getPatientInfo, getCustomerVo]（链式） |
| `$scope.updatePatient` | 2 | FN_promiseCall[savePatientInfo, saveCustomerInfo]（并行） |
| `saleInfo.fn`（局部） | 2 | FN_promiseCall[updateMedicalRecord] → success → $scope.saveChufang（链式） |
| `$scope.update` | 2 | queryStore + saveChufang（链式） |
| `$scope.update2` | 1 | saveChufang |
| `$scope.setProduct` | 1 | queryStore |
| `$scope.showsupplierList` | 1 | searchProductList → getProductSkuExistCountVoList |
| `$scope.queryCompanyName` | 2 | getCompanyOfMine + 链式 queryStorehouseId |
| `$scope.save` | 2 | saveMedicalProductListOfSmallVersion + success 触发 GetMedicalProductVoList 刷新 |

**总计**：触发 ≥ 2 API 的动作有 8 个

### 3.4 动作→API 异步链

```
getMedicalRecord
  └─ success: response.object
       └─ FN_promiseCall[getPatientInfo, getCustomerVo]
            └─ success: $scope.userInfo

queryCompanyName
  └─ success: res.object
       └─ $scope.queryStorehouseId(res.object.id)
            └─ success: $scope.lockStorehouseId

GetMedicalProductVoList
  └─ success: res.result.list
       └─ forEach
            └─ $scope.processBasicData()
                 └─ forEach tempShop → $scope.glassesInfo

updateMedicalRecord (FN)
  └─ success: $scope.saveChufang()
       └─ updateMethodGlassRecord

saveMedicalProductListOfSmallVersion
  └─ success: Popup + $scope.GetMedicalProductVoList()
       └─ forEach → processBasicData → $scope.glassesInfo
```

---

## 4. 动作→对象 完整矩阵

### 4.1 每个动作读/写的对象

| 动作函数 | 读对象 | 写对象 | A-F |
|---|---|---|---|
| `$scope.tip` | 无 | 无 | A |
| `$scope.prevent` | `$scope["supplierList" + i]` (1-3) | `$scope["supplierList" + i]` (1-3) | A |
| `$scope.upOther` | `$scope[key]` | `$scope[key]` | A |
| `$scope.getMedicalRecord` | `$scope.medicalRecordId`, `$stateParams.medicalRecordId` | `$scope.medicalRecord` (整体), `saleInfo.fn/inputVal/id` (局部), `$scope.saleInfo`, `$scope.object.secondDoctorId`, `$scope.userInfo` | A |
| `$scope.showCommon` | 无 | `$scope.userInfo.selectChannelModal` | A |
| `$scope.upimg.call` (callback) | `img` (param) | `$scope.userInfo.avatar` | A |
| `$scope.updateImg` | 无 | 无（return 空） | A |
| `$scope.updatePatient` | `$scope.userInfo` (15 字段分解) | `patient`, `customer` (局部对象) → FN_promiseCall | A |
| `$scope.GetMethodGlassRecordVo` | `$scope.medicalRecordId`, `methodGlassRecord` (局部) | `$scope.object` (for-in 覆盖) | A |
| `$scope.update` | `$scope.object[key]`, `$scope.glassesInfo["" + key2 + num]` | `$scope.glassesInfo["" + key2 + num]` | A |
| `$scope.update2` | 无 | `$scope.object[key]` | A |
| `$scope.saveChufang` | `$scope.object.secondDoctorId` (校验), `$scope.medicalRecordId`, `$scope.object.lastRxTime` | `$scope.object.medicalRecordId`, `delete $scope.object.lastRxTime` | A |
| `$scope.queryStorehouseId` | `companyId` (param) | `$scope.lockStorehouseId` | A |
| `$scope.queryCompanyName` | 无（无 Request 参数） | `$scope.companyName`, 调用 `$scope.queryStorehouseId` | A |
| `$scope.GetMedicalProductVoList` | `$scope.medicalRecordId`, `stock` (forEach), `medicalProductSign/brand/category/product/productSku/lockStorehouse/unLockExistSkuCount/skuDuplicate/medicalProduct` (解构) | `list` (局部), `tempList` (局部), `$scope.tempShop`, `$scope.stockInSkuList`, 调用 `$scope.processBasicData` | A |
| `$scope.processBasicData` | `$scope.tempShop` (forEach), `medicalProductSign.signType`, `medicalProduct.model1/model2/remark`, `product.productName`, `productSku.skuCode/marketPrice/kpiPrice/id`, `brand.id/brandName`, `unLockExistSkuCount` | `$scope.glassesInfo["..."+signType]` (12 字段) | A |
| `$scope.showsupplierList` | `event`, `key`, `num` (param) | `$scope["" + key + num]` = true, 调用 `$scope.prevent`, `$scope.searchProductList` | A |
| `$scope.searchProductList` | `keyword, num, event` (param), `$scope.glassesInfo["..."+num]` (7 字段) | `parmas` (局部), `$scope.getCorpListFactory` (新 ListFactory), `$scope["supplierList" + num]` | A |
| `$scope.setProduct` | `product, key` (param), `product.product.productName`, `product.productSku.skuCode` | `$scope.glassesInfo["keyword"+key]`, `$scope.glassesInfo["keywordvalue"+key]`, 调用 `$scope.queryStore` | A |
| `$scope.deleteReceipt` | `index, medicalProductId, key` (param) | `$scope["" + key]` (splice) | A |
| `$scope.printShoufei.print` (callback) | 无 | `this.show` = true | A |
| `$scope.printChufang.print` (callback) | 无 | `this.show` = true | A |
| `$scope.addStore.switch` (callback) | `bool` (param) | `this.show` = bool | A |
| `$scope.addStore.callback` (callback) | `info` (param) | `$scope.stockInSkuList.push(info)` | A |
| `saleInfo.fn` (局部) | `this.id` | `$scope.object.secondDoctorId` = this.id, 调用 FN_promiseCall updateMedicalRecord + $scope.saveChufang | A |

**总计**：26 个动作/回调/方法

### 4.2 动作—对象读/写统计

| 对象 | 被读 | 被写 | 动作数 |
|---|---:|---:|---:|
| `$scope.medicalRecord` | 2 (L35433, L35434) | 2 (L35390 init, L35419 getMedicalRecord success) | 1 |
| `$scope.medicalRecordId` | 10 | 1 (Init L35388) | 9+ |
| `$scope.edit` | 1 (L35409) | 1 (Init L35389) | 1 |
| `$scope.object` | 多字段 | 多字段（含 medicalRecordId/secondDoctorId/lastRxTime 动态写入） | 6 |
| `$scope.glassesInfo` | 多字段 | 多字段 | 6 |
| `$scope.userInfo` | 15 字段（分解） | 4 字段（直接）+ 1 整体 | 3 |
| `$scope.tempShop` | 1 (forEach) | 1 (L35723) | 1 |
| `$scope.stockInSkuList` | 1 (L35929) | 3 (L35724, L35821, L35833) | 3 |
| `$scope.lockStorehouseId` | 1 (L35919) | 1 (L35669) | 2 |
| `$scope.companyName` | 0 | 1 (L35677) | 1 |
| `$scope.saleInfo` | 0 | 1 (L35436) | 1 |
| `saleInfo` (局部) | 多字段 | 整体 + 多字段 | 1 |
| `patient` (局部) | 0 | 整体（L35509-L35516） | 1 |
| `customer` (局部) | 0 | 整体（L35517-L35523） | 1 |
| `methodGlassRecord` (局部) | 多字段 | 0 | 1 |
| `parmas` (局部) | 0 | 整体（L35782-L35793） | 1 |
| `store` (局部) | 0 | 整体（L35863-L35883） | 1 |
| `medicalProductParamListJson` (局部) | 0 | 整体（L35912-L35945） | 1 |
| `list` (局部) | 0 | 整体（L35698-L35720） | 1 |
| `tempList` (局部) | 0 | 整体（L35693-L35697） | 1 |

---

## 5. 字段级闭环

### 5.1 Read 字段级闭环

| Read API | Request.Field | Request 来源 | Response.Field | 落点 | 后续 Consumer | A-F |
|---|---|---|---|---|---|---|
| getMedicalRecord.json | `id` | `$scope.medicalRecordId` | `response.object` (整体) | `$scope.medicalRecord = response.object` | L35433 `.secondDoctorName` → saleInfo.inputVal<br>L35434 `.secondDoctorId` → saleInfo.id → $scope.object.secondDoctorId<br>L35440 `.patientId` → getPatientInfo Request<br>L35445 `.customerId` → getCustomerVo Request | A |
| getMethodGlassRecordVo.json | `medicalRecordId` | `$scope.medicalRecordId` | `res.result.vo.methodGlassRecord` | for-in `$scope.object` (27+ 字段) | $scope.object 整体 → updateMethodGlassRecord Request | A |
| selectStorehouseListOfCompany.json | `companyId, mcTypeSortType` | queryCompanyName 传入 + 字面量 | `res.result.list[0].id` | `$scope.lockStorehouseId` | $scope.save (L35919) → saveMedicalProductListOfSmallVersion Request | A |
| getCompanyOfMine.json | (无) | - | `res.object.companyName`, `res.object.id` | `$scope.companyName` + 链式 `$scope.queryStorehouseId(res.object.id)` | $scope.companyName HTML 消费；queryStorehouseId 链式 | A |
| getMedicalProductVoList.json | `medicalRecordId` | `$scope.medicalRecordId` | `res.result.list` (forEach) | `$scope.tempShop` + `$scope.stockInSkuList` + 调用 processBasicData | $scope.glassesInfo 12 字段；$scope.save (L35929) 消费 stockInSkuList | A |
| getProductSkuExistCountVoList.json (ListFactory) | `parmas` 10 字段 | `$scope.glassesInfo[...+num]` 7 字段 + 字面量 | `res.count` | `$scope["supplierList" + num]` + Popup | HTML 通过 $scope.getCorpListFactory.items 消费（F 边界） | A |
| checkBeforeDeleteMedicalProduct.json | `medicalProductId` | 函数参数 | （无 result consumer） | `$scope[""+key].splice(index, 1)` | 无 | A |
| getProductSkuExistCountVoList.json (ObjectFactory) | `store` 5-8 字段 | `$scope.glassesInfo[...+key]` 5 字段 + 字面量 | `res.result.list[0].productSku/unLockExistSkuCount` | `$scope.glassesInfo[...+key]` 4 字段 (count truthy) / 5 字段 (count falsy) | $scope.save (L35915, L35925) 消费 | A |
| getPatientInfo (FN) | `id` | `response.object.patientId` (getMedicalRecord response) | `res[0].object` (整体) | `patient` (局部) → `$scope.userInfo` 8 字段 | $scope.updatePatient → savePatientInfo Request | A |
| getCustomerVo (FN) | `customerId` | `response.object.customerId` (getMedicalRecord response) | `res[1].result.vo` (整体) | `customer` (局部) → `$scope.userInfo` 5 字段 | $scope.updatePatient → saveCustomerInfo Request | A |

**10 个 Read 全部字段级闭环**（A 级）

### 5.2 Write 字段级闭环

| Write API | Request.Field | 表达式 | 上游 Read | 中间变量 | A-F |
|---|---|---|---|---|---|
| updateMethodGlassRecord.json | `$scope.object` 整体（27+ 字段） | `$scope.object` | getMethodGlassRecordVo (L35604) | for-in 覆盖 | A |
| | `medicalRecordId` | `$scope.object.medicalRecordId = $scope.medicalRecordId` (L35640) | StateParams | $scope.medicalRecordId | A |
| | `secondDoctorId` | `$scope.object.secondDoctorId` (L35637 校验) | getMedicalRecord (L35416) | saleInfo.id (L35435) | A |
| | `lastRxTime` | for-in 覆盖 + Date 转换（L35617） | getMethodGlassRecordVo (L35604) | - | A |
| saveMedicalProductListOfSmallVersion.json | `medicalRecordId` | `$scope.medicalRecordId` (L35947) | StateParams | - | A |
| | `medicalProductParamListJson[i].id: null` (L35918) | 字面量 | - | - | A |
| | `medicalProductParamListJson[i].lockStorehouseId` (L35919) | `$scope.lockStorehouseId` | selectStorehouseListOfCompany (L35662) | $scope.lockStorehouseId (L35669) | A |
| | `medicalProductParamListJson[i].productSkuId` (L35920) | `$scope.glassesInfo["productSkuId"+i]` (L35915) | getProductSkuExistCountVoList (L35884) | $scope.glassesInfo | A |
| | `medicalProductParamListJson[i].memberRate: null` (L35921) | 字面量 | - | - | A |
| | `medicalProductParamListJson[i].useCount: 1` (L35922) | 字面量 | - | - | A |
| | `medicalProductParamListJson[i].remark` (L35923) | `$scope.glassesInfo["remark"+i]` | getMedicalProductVoList (L35685) → processBasicData (L35747) | $scope.glassesInfo | A |
| | `medicalProductParamListJson[i].signType` (L35924) | `window.optionsObj.glassesSignType[i]` | - | 全局对象 | A |
| | `medicalProductParamListJson[i].kpiPrice` (L35925) | `$scope.glassesInfo["productSkuKpiPrice"+i]` | getProductSkuExistCountVoList (L35884) | $scope.glassesInfo | A |
| | `medicalProductParamListJson[].id: stock.id` (L35932) | stock.id | getMedicalProductVoList (L35685) → L35699 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].lockStorehouseId: stock.lockStorehouseId` (L35933) | stock.lockStorehouseId | getMedicalProductVoList (L35685) → L35712 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].productSkuId: stock.productSkuId` (L35934) | stock.productSkuId | getMedicalProductVoList (L35685) → L35713 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].memberRate: stock.memberRate` (L35935) | stock.memberRate | getMedicalProductVoList (L35685) → L35717 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].useCount: stock.useCount` (L35936) | stock.useCount | getMedicalProductVoList (L35685) → L35716 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].remark: stock.remark` (L35937) | stock.remark | getMedicalProductVoList (L35685) → L35714 | $scope.stockInSkuList | A |
| | `medicalProductParamListJson[].kpiPrice: stock.kpiPrice` (L35938) | stock.kpiPrice | getMedicalProductVoList (L35685) → L35719 | $scope.stockInSkuList | A |
| updateMedicalRecord (FN) | `id` | `$scope.medicalRecordId` (L35425) | StateParams | - | A |
| | `secondDoctorId` | `$scope.object.secondDoctorId` (L35426) | getMedicalRecord (L35416) | saleInfo.id (L35435) | A |
| savePatientInfo (FN) | `patient.id` | `patientId` (L35510) | getPatientInfo (L35437) | $scope.userInfo.patientId (L35499) | A |
| | `patient.patientName` | `patientName` (L35511) | getPatientInfo | $scope.userInfo.patientName (L35500) | A |
| | `patient.patientGender` | `patientGender` (L35512) | getPatientInfo | $scope.userInfo.patientGender (L35501) | A |
| | `patient.patientBirthday` | `patientBirthday` (L35513) | getPatientInfo | $scope.userInfo.patientBirthday (L35502) | A |
| | `patient.patientRemark` | `patientRemark` (L35514) | getPatientInfo | $scope.userInfo.patientRemark (L35503) | A |
| saveCustomerInfo (FN) | `customer.id` | `customerId` (L35518) | getCustomerVo (L35437) | $scope.userInfo.customerId (L35504) | A |
| | `customer.channelTagId` | `channelTagId` (L35519) | getCustomerVo | $scope.userInfo.channelTagId (L35505) | A |
| | `customer.channel` | `channel` (L35520) | getCustomerVo | $scope.userInfo.channel (L35506) | A |
| | `customer.linkMobile` | `linkMobile` (L35521) | getCustomerVo | $scope.userInfo.linkMobile (L35507) | A |
| | `customer.trueName` | `patientName` (L35522) | getPatientInfo (注意：来自 patientName 而非 customer) | $scope.userInfo.patientName (L35500) | A |

**5 个 Write 全部字段级 100% A 级**（与 S1-109 一致）

---

## 6. Read 闭环

### 6.1 每个 Read 完整闭环

```
[1] getMedicalRecord.json (Init 立即 L35958)
    Request: { id: $scope.medicalRecordId }
    Response: response.object
    Scope 落点: $scope.medicalRecord (整体)
    后续 Consumer:
      ├─ saleInfo.inputVal = $scope.medicalRecord.secondDoctorName (L35433)
      ├─ saleInfo.id = $scope.medicalRecord.secondDoctorId (L35434)
      ├─ $scope.object.secondDoctorId = saleInfo.id (L35435)
      ├─ $scope.saleInfo = saleInfo (L35436)
      └─ FN_promiseCall[getPatientInfo{ id: response.object.patientId }, getCustomerVo{ customerId: response.object.customerId }] (L35437)
           └─ $scope.userInfo (15 字段, L35451-L35466)
    是否参与 Write: 是（saleInfo.id → updateMethodGlassRecord + updateMedicalRecord）
    是否只是展示: 否

[2] getMethodGlassRecordVo.json (Init 立即 L35623)
    Request: { medicalRecordId: $scope.medicalRecordId }
    Response: res.result.vo.methodGlassRecord
    Scope 落点: for-in $scope.object 覆盖（27+ 字段）
    后续 Consumer: $scope.object 整体 → updateMethodGlassRecord Request
    是否参与 Write: 是
    是否只是展示: 否

[3] selectStorehouseListOfCompany.json (queryCompanyName 链式 L35678)
    Request: { companyId: res.object.id (getCompanyOfMine response), mcTypeSortType: "ASC" }
    Response: res.result.list[0].id
    Scope 落点: $scope.lockStorehouseId
    后续 Consumer: $scope.save (L35919) → saveMedicalProductListOfSmallVersion Request
    是否参与 Write: 是
    是否只是展示: 否

[4] getCompanyOfMine.json (Init 立即 L35682)
    Request: (无)
    Response: res.object (整体)
    Scope 落点: $scope.companyName + 链式 $scope.queryStorehouseId
    后续 Consumer: queryStorehouseId 链式 → selectStorehouseListOfCompany
    是否参与 Write: 是（间接通过 lockStorehouseId）
    是否只是展示: 部分（companyName 展示；id 链式）

[5] getMedicalProductVoList.json (Init 立即 L35755 + save success L35955)
    Request: { medicalRecordId: $scope.medicalRecordId }
    Response: res.result.list
    Scope 落点: $scope.tempShop + $scope.stockInSkuList + 调用 processBasicData → $scope.glassesInfo
    后续 Consumer: $scope.save (L35929) → saveMedicalProductListOfSmallVersion Request
    是否参与 Write: 是
    是否只是展示: 否

[6] getProductSkuExistCountVoList.json (ListFactory, L35797)
    Request: parmas (10 字段)
    Response: res.count
    Scope 落点: $scope["supplierList"+num] + Popup
    后续 Consumer: HTML 列表展示（F 边界）
    是否参与 Write: 否
    是否只是展示: 是

[7] checkBeforeDeleteMedicalProduct.json (L35827)
    Request: { medicalProductId }
    Response: 无 result consumer
    Scope 落点: $scope[""+key].splice(index, 1)
    后续 Consumer: 无
    是否参与 Write: 否（仅删除操作）
    是否只是展示: 否

[8] getProductSkuExistCountVoList.json (ObjectFactory, L35884)
    Request: store (5-8 字段)
    Response: res.result.list[0].productSku/unLockExistSkuCount
    Scope 落点: $scope.glassesInfo["..."+key] (4-5 字段)
    后续 Consumer: $scope.save (L35915, L35925)
    是否参与 Write: 是
    是否只是展示: 否

[9] getPatientInfo (FN, L35437)
    Request: { id: response.object.patientId }
    Response: res[0].object
    Scope 落点: patient 局部 → $scope.userInfo (8 字段)
    后续 Consumer: $scope.updatePatient → savePatientInfo Request
    是否参与 Write: 是
    是否只是展示: 否

[10] getCustomerVo (FN, L35437)
    Request: { customerId: response.object.customerId }
    Response: res[1].result.vo
    Scope 落点: customer 局部 → $scope.userInfo (5 字段)
    后续 Consumer: $scope.updatePatient → saveCustomerInfo Request
    是否参与 Write: 是
    是否只是展示: 否
```

**Read 闭环统计**：
- 10 个 Read 全部有完整闭环（A 级）
- 9 个参与 Write
- 1 个仅展示（getProductSkuExistCountVoList ListFactory）
- 1 个仅删除操作（checkBeforeDeleteMedicalProduct）

---

## 7. Write 闭环

### 7.1 每个 Write 完整闭环

```
[Write #1] updateMedicalRecord (FN, saleInfo.fn 触发 L35422)
    Input: $scope.medicalRecordId (StateParams), $scope.object.secondDoctorId (源自 getMedicalRecord)
    Request: { id: $scope.medicalRecordId, secondDoctorId: $scope.object.secondDoctorId }
    Success: $scope.saveChufang() (L35430, 链式 Write)
    Refresh: 无
    State: 无
    Popup: 无

[Write #2] updateMethodGlassRecord (L35644, saveChufang 触发)
    Input: $scope.object (含 27+ right*/left* 字段, medicalRecordId, secondDoctorId, lastRxTime)
    Request: $scope.object
    Success: (空 then)
    Refresh: 无
    State: 无
    Popup: 无

[Write #3] savePatientInfo (FN, updatePatient 触发 L35532)
    Input: $scope.userInfo (8 字段分解) → patient 局部对象
    Request: patient (id, patientName, patientGender, patientBirthday, patientRemark)
    Success: $timeout(Popup.notice("修改成功!"))
    Refresh: 无
    State: 无
    Popup: "修改成功!"

[Write #4] saveCustomerInfo (FN, updatePatient 触发 L35532)
    Input: $scope.userInfo (5 字段分解) → customer 局部对象
    Request: customer (id, channelTagId, channel, linkMobile, trueName)
    Success: $timeout(Popup.notice("修改成功!"))
    Refresh: 无
    State: 无
    Popup: "修改成功!"

[Write #5] saveMedicalProductListOfSmallVersion (L35950, save 触发)
    Input: medicalProductParamListJson (1-3 循环 + stockInSkuList)
    Request: { medicalRecordId: $scope.medicalRecordId, medicalProductParamListJson: JSON.stringify(...) }
    Success: Popup.notice("保存成功!") + $scope.GetMedicalProductVoList() (L35955, Refresh)
    Refresh: getMedicalProductVoList.json (刷新 $scope.tempShop + $scope.stockInSkuList + $scope.glassesInfo)
    State: 无
    Popup: "保存成功!"
```

**Write 闭环统计**：
- 5 个 Write 全部有完整闭环（A 级）
- 1 个 Write 有 Refresh（saveMedicalProductListOfSmallVersion → GetMedicalProductVoList）
- 1 个 Write 有 Popup 提示（saveMedicalProductListOfSmallVersion "保存成功!"）
- 2 个 Write 有 Popup 提示（savePatientInfo + saveCustomerInfo 同一 then "修改成功!"）
- 0 个 Write 有 State 出口

### 7.2 链式 Write 触发

```
saleInfo.fn() (L35420-L35432)
  └─ FN_promiseCall updateMedicalRecord (L35422-L35428)
       └─ success (L35429)
            └─ $scope.saveChufang() (L35430)
                 └─ updateMethodGlassRecord (L35644)
                      └─ (空 success)
```

**链式 Write 数量**：1 条

---

## 8. medicalRecord 闭环

### 8.1 medicalRecord 回读检查

**S1-110 重点检查**：

| 位置 | 是否回读 medicalRecord | 证据 |
|---|---:|---|
| L35958 `$scope.getMedicalRecord()` | **Init 立即执行 1 次** | 唯一调用点 |
| L35419 `$scope.medicalRecord = response.object` | 1 次整体赋值 | 唯一写入点 |
| Write success | **无回读** | 0 处 `$scope.getMedicalRecord()` 在 success 中 |
| 任何 then/callback | **无回读** | 0 处 |

**关键发现**：
- `getMedicalRecord` 在 optometryGlassesCtrl 范围内**仅被调用 1 次**（L35958 Init）
- **0 个** Write success / Read success / 任何 callback 中**回读** medicalRecord
- 意味着：5 个 Write 完成后，**Controller 不会**重新拉取 medicalRecord 完整数据
- medicalRecord 整体在 L35419 赋值后**保持不变**，直到 Controller 销毁

### 8.2 medicalRecord 完整生命周期

```
Init (L35383)
  ├─ $scope.medicalRecord = {} (L35390) ← 初始空对象
  ├─ $scope.medicalRecordId = $stateParams.medicalRecordId (L35388)
  └─ $scope.edit = $stateParams.edit === "true" (L35389)

Init Read (L35958)
  └─ $scope.getMedicalRecord() ← 唯一调用
       └─ Read /admin/getMedicalRecord.json {id: $scope.medicalRecordId}
            └─ success (L35418)
                 └─ $scope.medicalRecord = response.object (L35419) ← 整体赋值
                      └─ $scope.medicalRecord.secondDoctorName → saleInfo.inputVal (L35433)
                      └─ $scope.medicalRecord.secondDoctorId → saleInfo.id → $scope.object.secondDoctorId (L35434-L35435)

Write 阶段
  ├─ updateMethodGlassRecord (L35644) → $scope.object (含 27+ 字段, 但 medicalRecord 本身不变)
  ├─ updateMedicalRecord (L35422, 隐式) → 修改 secondDoctorId，但医疗记录的其它字段不变
  ├─ saveMedicalProductListOfSmallVersion (L35950) → medicalRecord 无关
  └─ savePatientInfo + saveCustomerInfo (L35532, 隐式) → 修改 patient + customer，不修改 medicalRecord

Controller 销毁
  └─ $scope.medicalRecord 被销毁（Angular scope lifecycle）
```

### 8.3 medicalRecord 字段再访问检查

**S1-109 + S1-110 联合确认**：
- $scope.medicalRecord 字段访问总次数：**2**（L35433 `.secondDoctorName` + L35434 `.secondDoctorId`）
- 整体赋值次数：**2**（L35390 `= {}` + L35419 `= response.object`）
- **0 次**再读

**结论**：medicalRecord 在本 Controller 内是"读一次"模式。

---

## 9. State 出口

### 9.1 State 出口全量

```powershell
Select-String -Path 'controller.js' -Pattern '\$state\.go' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

**A 级确认**：optometryGlassesCtrl 范围内 **0 处 `$state.go`**

### 9.2 State 出口 provenance

| State | Params | 参数来源 | 上游函数 | 上游对象 | 行号 |
|---|---|---|---|---|---|
| （无） | - | - | - | - | - |

**F 边界**：离开方式由 HTML 决定（`<a ui-sref>`、浏览器后退等），不可得

---

## 10. edit 模式

### 10.1 edit 全部 Consumer

| 行号 | 表达式 | 影响对象 | 影响 API | 影响 Init | 影响 State | A-F |
|---:|---|---|---|---|---|---|
| 35389 | `$scope.edit = $stateParams.edit === "true";` | Init 派生 | 无 | Init 时计算 | 无 | A |
| 35409 | `$scope.showOtherStore = $scope.edit;` | $scope.showOtherStore | 无 | 无 | 无 | A |

**$scope.showOtherStore 在 Controller 内 0 引用**（A 级）

### 10.2 edit 模式差异分析

| 差异项 | edit = false | edit = true | 是否真实产生差异 | A-F |
|---|---|---|---|---|
| API Request 字段 | 无变化 | 无变化 | 否 | A |
| API 类型 | 无变化 | 无变化 | 否 | A |
| 初始化流程 | 无变化 | 无变化 | 否 | A |
| 页面数据（Controller 侧） | 无变化 | 无变化 | 否 | A |
| Write 字段 | 无变化 | 无变化 | 否 | A |
| State 出口 | 0 | 0 | 否 | A |
| 弹窗行为 | 无变化 | 无变化 | 否 | A |

**edit 在 Controller 业务逻辑层面**对**任何**运行时行为**都**没有**影响（A 级 100% 确认）。

**唯一可能**：HTML 基于 $scope.edit 或 $scope.showOtherStore 切换 UI（F 边界）

### 10.3 edit 与入口的对应

| 入口 | $stateParams.edit | $scope.edit | 实际 Controller 行为 |
|---|---|---|---|
| beginCustomerCheckin success | **未传** | false | 无差异 |
| fnMap "修改" | **"true"** | true | 无差异 |

---

## 11. 页面入口模式

### 11.1 入口对比

| 入口 | $stateParams.medicalRecordId | $stateParams.edit | $scope.medicalRecordId | $scope.edit | Controller 行为差异 |
|---|---|---|---|---|---|
| beginCustomerCheckin success | 有 | **无（未传）** | 有 | **false**（强比较 "true" 失败） | 无 |
| fnMap "修改" | 有 | **有（"true"）** | 有 | **true** | 无 |

**A 级确认**：两个入口在 Controller 业务逻辑上**完全等价**，0 差异

### 11.2 入口字段（已锁定）

- `medicalRecordId`：必传（来自 optometryCtrl $state.go）
- `edit`：仅 fnMap "修改" 传 "true"（S1-107 锁定）

### 11.3 Controller 接收逻辑

```javascript
$scope.medicalRecordId = $stateParams.medicalRecordId;  // L35388
$scope.edit = $stateParams.edit === "true";             // L35389
```

---

## 12. 输入容器

### 12.1 Controller 侧输入容器审计

按源码实际存在的输入相关 Scope：

| 容器 | 类型 | 字段 | 行号 | A-F |
|---|---|---|---|---|
| `$scope.userInfo` | Object | patientId, avatar, patientName, patientGender, patientBirthday, patientRemark, customerId, linkMobile, channel, channelTagId, name, gender, mobile, selectChannelModal | 35414/35451/35479 | A |
| `$scope.object` | Object | right15, left15, right14, left14, right13, left13, right24, left24, right81, left81, right12, left12, right1, left1, right83, right85, left83, left85, right82, left82, right45, left45, left67, right91, left91, rxCount, lastRxTime, medicalRecordId, secondDoctorId | 35573-35601 | A |
| `$scope.glassesInfo` | Object | brandName1, brandName2, brandName3, brandId1, brandId2, brandId3, model1Keyword1, model2Keyword1, model1Keyword2, model2Keyword2 + 12 processBasicData 字段 + queryStore 字段 | 35756-35767 | A |
| `$scope.saleInfo` | Object | idName, ajaxUrl, isshow, id, inputVal, inputPlaceHolder, info, key, key2, fn, reset, type | 35436 (L35555-L35572 init in local) | A |
| `$scope.printChufang` | Object | show, hiddenLen, medicalRecordId, print | 35650-35657 | A |
| `$scope.addStore` | Object | show, medicalRecordId, switch, callback | 35814-35823 | A |
| `$scope.printShoufei` | Object | show, title, daishou, options[0].url, options[0].param, print | 35836-35847 | A |
| `$scope.dateCom` | Object | show, open | 35471-35477 | A |
| `$scope.upimg` | Object | show, img, call | 35481-35491 | A |

### 12.2 容器在 Write 中的角色

| 容器 | 写入方 | 读出方（Write Request 来源） |
|---|---|---|
| `$scope.userInfo` | getPatientInfo + getCustomerVo (L35451), showCommon (L35479), upimg.call (L35487) | updatePatient → savePatientInfo + saveCustomerInfo (L35498-L35507) |
| `$scope.object` | Init (L35573), GetMethodGlassRecordVo (L35613), update (L35625), update2 (L35632), saveChufang (L35640, L35642), glassesInfo Init (L35763) | saveChufang → updateMethodGlassRecord (L35644) |
| `$scope.glassesInfo` | Init (L35756), processBasicData (L35741), setProduct (L35806), queryStore (L35849, L35892, L35897) | save → saveMedicalProductListOfSmallVersion (L35915, L35925) |
| `$scope.saleInfo` | Init (L35436) | HTML 触发 saleInfo.fn() → updateMedicalRecord + saveChufang (F 边界) |
| `$scope.printChufang` | Init (L35650) | HTML 触发 print.print() (F 边界) |
| `$scope.addStore` | Init (L35814) | 弹窗内部逻辑（F 边界） |
| `$scope.printShoufei` | Init (L35836) | HTML 触发 print.print() (F 边界) |

---

## 13. clone / copy / 引用

### 13.1 搜索结果

```powershell
Select-String -Path 'controller.js' -Pattern 'angular\.copy|Object\.assign|JSON\.parse\(JSON|clone|copy' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

### 13.2 实际数据传递方式

| 方式 | 用法 | 行号 | 类别 |
|---|---|---|---|
| 整体赋值 | `$scope.medicalRecord = response.object` | L35419 | A. 同一引用（如果 response.object 是引用类型） |
| 字段级复制 | `$scope.object.medicalRecordId = $scope.medicalRecordId` | L35640 | D. primitive assignment |
| 派生（局部变量） | `saleInfo.inputVal = $scope.medicalRecord.secondDoctorName` | L35433 | A. 同一引用（如果字符串是 primitive） |
| 派生（局部对象构造） | `var patient = { id: patientId, ... }` | L35509-L35516 | B. 浅/显式复制（新对象） |
| for-in 复制 | `for (var i in $scope.object) { $scope.object[i] = methodGlassRecord[i]; }` | L35613-L35620 | D. primitive assignment（按字段） |
| 解构 | `var { unLockExistSkuCount, productSku } = res.result.list[0]` | L35893-L35895 | A. 同一引用（解构后仍是引用） |
| JSON.stringify | `JSON.stringify(medicalProductParamListJson)` | L35945 | C. JSON 深复制（仅用于序列化） |

### 13.3 主对象引用类型分析

| 对象 | 引用类型 | 备注 |
|---|---|---|
| `$scope.medicalRecord` | A. same reference | 整体赋值后保持 |
| `$scope.medicalRecordId` | D. primitive | 字符串/数字 |
| `$scope.edit` | D. primitive | Boolean |
| `$scope.object` | A. same reference + 字段 mutation | 多次字段写入 |
| `$scope.glassesInfo` | A. same reference + 字段 mutation | processBasicData + queryStore 多次写入 |
| `$scope.userInfo` | A. same reference + 字段 mutation | 整体赋值后字段读写 |
| `$scope.lockStorehouseId` | D. primitive | 数字/字符串 |
| `$scope.companyName` | D. primitive | 字符串 |
| `$scope.tempShop` | A. same reference (Array) | 整体替换 |
| `$scope.stockInSkuList` | A. same reference (Array) | push/splice |
| `$scope.saleInfo` | A. same reference | 整体赋值 |

---

## 14. 异步边界

### 14.1 异步类型

| 类型 | 数量 | 位置 |
|---|---:|---|
| `ObjectFactory().saveOrQuery(...).then(...)` | 9 | 详见 §3.1 |
| `ListFactory.nextPage().then(...)` | 1 | L35798 |
| `window.FN_promiseCall(...).then(...)` | 3 | L35422, L35437, L35532 |
| `$timeout(fn)` | 3 | L35448, L35486, L35539 |
| `window.getStockSet(...).then(...)` | 1 | L35385 |
| `Promise.all` | 0 | - |
| `$q.all` | 0 | - |
| `async/await` | 0 | - |

### 14.2 API 链式（API success → API）

| 链 | 详情 | A-F |
|---|---|---|
| 1 | getMedicalRecord success → FN_promiseCall[getPatientInfo, getCustomerVo] | A |
| 2 | getCompanyOfMine success → $scope.queryStorehouseId → selectStorehouseListOfCompany | A |
| 3 | updateMedicalRecord success → $scope.saveChufang → updateMethodGlassRecord | A |
| 4 | saveMedicalProductListOfSmallVersion success → $scope.GetMedicalProductVoList → getMedicalProductVoList | A |

**API success → API 链**：4 条

### 14.3 callback 后继续

| 位置 | 详情 | A-F |
|---|---|---|
| `$scope.addStore.callback` (L35820) | 弹窗 callback → $scope.stockInSkuList.push(info) | A |
| `saleInfo.fn` (L35420-L35432) | HTML 触发 → FN_promiseCall updateMedicalRecord → $scope.saveChufang | A |
| `$scope.upimg.call` (L35485-L35490) | 弹窗 callback → $scope.userInfo.avatar = img | A |

### 14.4 timeout 后继续

| 位置 | 详情 | A-F |
|---|---|---|
| L35448-L35467 | $timeout 内 $scope.userInfo 赋值（getMedicalRecord success 内） | A |
| L35486-L35489 | $timeout 内 $scope.userInfo.avatar = img | A |
| L35539-L35541 | $timeout 内 Popup.notice("修改成功!") | A |

### 14.5 独立异步

| 位置 | 详情 |
|---|---|
| `window.getStockSet` (L35385) | 与其它异步无依赖 |

### 14.6 异步边界 — 关键风险点

- 4 个 Init 立即执行（`GetMethodGlassRecordVo`, `queryCompanyName`, `GetMedicalProductVoList`, `getMedicalRecord`）**无顺序保证**
- `getMedicalRecord` 在最后（L35958），但 success 内的 `saleInfo.inputVal` 可能在 `queryStorehouseId` 之前完成
- **未观察到**任何时序控制（如 `$q.all` / `Promise.all`）

---

## 15. 重复提交防护

### 15.1 搜索结果

```powershell
Select-String -Path 'controller.js' -Pattern 'disabled|loading|debounce|submit.*guard|flag|lock\(|saving\(|isLoading|isSubmitting' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**输出**：（无匹配）

### 15.2 结论

**当前 Controller 未观察到明确重复提交防护**。

- 0 处 `disabled` 标志
- 0 处 `loading` 标志
- 0 处 `debounce` 限流
- 0 处 `lock()` 互斥
- 0 处 `isLoading` / `isSubmitting` / `saving()` 状态
- 0 处 promise guard
- 0 处 disabled 样式控制

### 15.3 风险点

- `$scope.save` 多次快速点击 → 多次 saveMedicalProductListOfSmallVersion 调用
- `$scope.saveChufang` 多次快速点击 → 多次 updateMethodGlassRecord 调用
- `$scope.updatePatient` 多次快速点击 → 多次 savePatientInfo + saveCustomerInfo 调用
- `saleInfo.fn` 多次触发 → 链式多次 updateMedicalRecord + updateMethodGlassRecord

**F 边界**：HTML 可能有 `ng-disabled` 或 UI 层防护（源码不可得）

---

## 16. 主对象分类（仅按源码出现）

### 16.1 实际存在的对象

按源码实际命名 / 字段名归类：

| 对象类别 | 出现位置 | 备注 |
|---|---|---|
| `medicalRecord` | L35390, L35416, L35419, L35433, L35434 | getMedicalRecord 主体 |
| `patient` | L35449, L35510-L35516 | getPatientInfo 返回 + 局部对象 |
| `customer` | L35450, L35517-L35523 | getCustomerVo 返回 + 局部对象 |
| `methodGlassRecord` | L35611 | getMethodGlassRecordVo 嵌套字段 |
| `product` / `productSku` / `brand` / `category` / `medicalProduct` / `medicalProductSign` / `lockStorehouse` | L35694-L35737, L35893-L35895 | getMedicalProductVoList 返回元素嵌套 |
| `stock` | L35694, L35893 | 同上 |
| `parmas` / `store` / `list` / `tempList` / `patient` / `customer` / `methodGlassRecord` / `medicalProductParamListJson` | 局部对象 | 临时变量 |
| `company` (`.id`, `.companyName`) | L35677, L35678 | getCompanyOfMine 返回 |
| `employee` (saleInfo.key) | L35564 | fnMap 风格对象字段名 |

**未出现的对象**（**严禁虚构**）：
- `examination`
- `prescription`（虽 methodGlassRecord 是处方相关，但源码未命名 prescription）
- `machine` / `machineCenter` / `machineOrder`
- `template`
- `customerCheckin`
- `order`
- `lockStorehouse`（仅作为响应字段，未独立对象化）

### 16.2 object 对象命名

`$scope.object` 命名（源码实际命名）：
- L35573 注释：无
- 包含字段：right15, left15, right14, left14, right13, left13, right24, left24, right81, left81, right12, left12, right1, left1, right83, right85, left83, left85, right82, left82, right45, left45, left67, right91, left91, rxCount, lastRxTime
- 动态添加：medicalRecordId (L35640), secondDoctorId (L35435)
- 业务含义：**未明确命名**，源码仅用 object

---

## 17. 对象→API 矩阵

| 对象 | Consumer 函数 | 触发的 API | 类型 | A-F |
|---|---|---|---|---|
| `$scope.medicalRecord` | getMedicalRecord (写) | getMedicalRecord.json | Read | A |
| `$scope.medicalRecord` | getMedicalRecord success | FN_promiseCall[getPatientInfo, getCustomerVo] | Read | A |
| `$scope.medicalRecord.secondDoctorName` | getMedicalRecord success | （不直接 API）→ saleInfo.inputVal | （无 API） | A |
| `$scope.medicalRecord.secondDoctorId` | getMedicalRecord success | （不直接 API）→ saleInfo.id → $scope.object.secondDoctorId → updateMethodGlassRecord + updateMedicalRecord | Write | A |
| `$scope.medicalRecordId` | getMedicalRecord, GetMethodGlassRecordVo, GetMedicalProductVoList, saveChufang, save | 5 个 API Request 字段 | Read + Write | A |
| `$scope.medicalRecordId` | saveChufang, addStore, printChufang, printShoufei | 4 个对象派生 | （无 API） | A |
| `$scope.object` | saveChufang | updateMethodGlassRecord.json | **Write** | A |
| `$scope.object` | GetMethodGlassRecordVo, update, update2, saveChufang, glassesInfo Init | 5 个对象操作 | （无 API） | A |
| `$scope.glassesInfo` | save | saveMedicalProductListOfSmallVersion.json (字段来源) | **Write** | A |
| `$scope.glassesInfo` | searchProductList, setProduct, queryStore, processBasicData | 4 个操作 | Read (parmas 来源) | A |
| `$scope.userInfo` | updatePatient | FN_promiseCall[savePatientInfo, saveCustomerInfo] | **Write** | A |
| `$scope.userInfo` | getMedicalRecord FN success, showCommon, upimg.call | 3 个对象操作 | （无 API） | A |
| `$scope.tempShop` | processBasicData | （不直接 API）→ $scope.glassesInfo 派生 | （无 API） | A |
| `$scope.stockInSkuList` | save | saveMedicalProductListOfSmallVersion.json (字段来源) | **Write** | A |
| `$scope.stockInSkuList` | addStore.callback, deleteReceipt | 2 个操作 | Read | A |
| `$scope.lockStorehouseId` | save | saveMedicalProductListOfSmallVersion.json (字段来源) | **Write** | A |
| `$scope.lockStorehouseId` | queryStorehouseId | selectStorehouseListOfCompany.json (写入) | Read | A |
| `$scope.companyName` | （无） | （无 API） | （仅展示） | A |
| `$scope.saleInfo` | saleInfo.fn (HTML 触发) | FN_promiseCall updateMedicalRecord | **Write** | A |
| `company.id` (getCompanyOfMine 返回) | queryCompanyName success | queryStorehouseId 链式 | Read (链式) | A |
| `patient` (局部) | updatePatient | savePatientInfo | **Write** | A |
| `customer` (局部) | updatePatient | saveCustomerInfo | **Write** | A |
| `methodGlassRecord` (局部) | GetMethodGlassRecordVo | for-in $scope.object | （无 API） | A |
| `list` (局部) | GetMedicalProductVoList | $scope.stockInSkuList | （无 API） | A |
| `tempList` (局部) | GetMedicalProductVoList | $scope.tempShop | （无 API） | A |
| `parmas` (局部) | searchProductList | ListFactory 构造 | Read | A |
| `store` (局部) | queryStore | getProductSkuExistCountVoList.json Request | Read | A |
| `medicalProductParamListJson` (局部) | save | saveMedicalProductListOfSmallVersion.json Request | **Write** | A |
| `stock` (局部) | GetMedicalProductVoList forEach | $scope.stockInSkuList 元素 | （无 API） | A |
| `product.productSku` / `productSku` (局部) | setProduct, processBasicData, queryStore | $scope.glassesInfo 字段 | （无 API） | A |

**对象→API 矩阵**：27 个对象关系

---

## 18. API—对象矩阵

| API | Request 对象 | Response 对象 | Scope 落点 | 后续 Write | 后续 State | A-F |
|---|---|---|---|---|---|---|
| getMedicalRecord.json | `{ id: $scope.medicalRecordId }` | `response.object` | `$scope.medicalRecord = response.object` | updateMethodGlassRecord (L35644), updateMedicalRecord (L35422) | 无 | A |
| getMethodGlassRecordVo.json | `{ medicalRecordId: $scope.medicalRecordId }` | `res.result.vo.methodGlassRecord` | for-in `$scope.object` 覆盖 | updateMethodGlassRecord (L35644) | 无 | A |
| selectStorehouseListOfCompany.json | `{ companyId, mcTypeSortType: "ASC" }` | `res.result.list[0].id` | `$scope.lockStorehouseId = res.result.list[0].id` | saveMedicalProductListOfSmallVersion (L35919) | 无 | A |
| getCompanyOfMine.json | (无) | `res.object.{companyName, id}` | `$scope.companyName` + 链式 queryStorehouseId | saveMedicalProductListOfSmallVersion (间接通过 lockStorehouseId) | 无 | A |
| getMedicalProductVoList.json | `{ medicalRecordId: $scope.medicalRecordId }` | `res.result.list` | `$scope.tempShop` + `$scope.stockInSkuList` + `$scope.glassesInfo` (via processBasicData) | saveMedicalProductListOfSmallVersion (L35929) | 无 | A |
| getProductSkuExistCountVoList.json (ListFactory) | `parmas` 10 字段 | `res.count` | `$scope["supplierList"+num]` + Popup | 无 | 无 | A |
| checkBeforeDeleteMedicalProduct.json | `{ medicalProductId }` | (无 result consumer) | `$scope[""+key].splice(index, 1)` | 无 | 无 | A |
| getProductSkuExistCountVoList.json (ObjectFactory) | `store` 5-8 字段 | `res.result.list[0].productSku/unLockExistSkuCount` | `$scope.glassesInfo["..."+key]` 4-5 字段 | saveMedicalProductListOfSmallVersion (L35915, L35925) | 无 | A |
| getPatientInfo (FN) | `{ id: response.object.patientId }` | `res[0].object` | `patient` 局部 → `$scope.userInfo` 8 字段 | savePatientInfo (L35532) | 无 | A |
| getCustomerVo (FN) | `{ customerId: response.object.customerId }` | `res[1].result.vo` | `customer` 局部 → `$scope.userInfo` 5 字段 | saveCustomerInfo (L35532) | 无 | A |
| updateMethodGlassRecord.json | `$scope.object` (27+ 字段) | (空) | (无) | (无 Refresh) | 无 | A |
| saveMedicalProductListOfSmallVersion.json | `{ medicalRecordId, medicalProductParamListJson }` | `res` | (无) | Refresh: $scope.GetMedicalProductVoList() | 无 | A |
| updateMedicalRecord (FN) | `{ id, secondDoctorId }` | (空) | (无) | $scope.saveChufang (链式) | 无 | A |
| savePatientInfo (FN) | `patient` 整体 | (空) | (无) | $timeout(Popup) | 无 | A |
| saveCustomerInfo (FN) | `customer` 整体 | (空) | (无) | $timeout(Popup) | 无 | A |

**API—对象矩阵**：14 个 API + 1 个 ajaxUrl 引用 (saleInfo.ajaxUrl /admin/selectEmployeeVoListOfMyCompany.json, **未在本 Controller 实际调用**)

---

## 19. 26 项矩阵

| # | 审计项 | 文件 | 行号 | A-F | L1/L2/L3 | 备注 |
|---:|---|---|---|---|---|---|
| 01 | 动作全集 | controller.js | 见 §2.1 | A | L1 | 21 个 $scope 函数 + 12 个内部 callback |
| 02 | 用户动作候选 | controller.js | 见 §2.2 | A | L1 | 8 个用户动作 + 5 个 Init |
| 03 | 动作→函数 | controller.js | 见 §2.1 | A | L1 | 21 映射 |
| 04 | 动作→API | controller.js | 见 §3.1 | A | L2 | 16 映射 |
| 05 | 动作→对象 | controller.js | 见 §4.1 | A | L2 | 26 动作/回调 |
| 06 | 字段级输入 | controller.js | 见 §12 | A | L3 | 8 个输入容器 |
| 07 | 对象→API | controller.js | 见 §17 | A | L2 | 27 个对象关系 |
| 08 | 对象传播 | controller.js | 见 §17 | A | L3 | 7 个对象传播链 |
| 09 | Read 闭环 | controller.js | 见 §6.1 | A | L2 | 10 个 Read 全部 A 级闭环 |
| 10 | Write 闭环 | controller.js | 见 §7.1 | A | L2 | 5 个 Write 全部 A 级闭环 |
| 11 | Write Request 字段 | controller.js | 见 §5.2 | A | L3 | 100% A 级（30+ 字段） |
| 12 | Write Success | controller.js | 见 §7 | A | L2 | 5 个 Write 全部明确 |
| 13 | Write→Read | controller.js | L35955 → L35685 | A | L2 | 1 条（save → GetMedicalProductVoList） |
| 14 | Write→State | controller.js | 0 处 | A | L1 | 0 条 |
| 15 | medicalRecord 闭环 | controller.js | 见 §8 | A | L2 | 1 次 Init，无回读 |
| 16 | medicalRecordId | controller.js | 见 §4.1 | A | L1 | 10 处消费，5 类路径无新增 |
| 17 | edit 模式 | controller.js | L35389, L35409 | A | L1 | 0 影响 |
| 18 | edit→API | controller.js | 0 处 | A | L1 | 0 影响 |
| 19 | 页面入口模式 | controller.js | L35388, L35389 | A | L1 | 2 入口，0 差异 |
| 20 | 输入容器 | controller.js | 见 §12 | A | L2 | 8 个 |
| 21 | clone/copy | controller.js | 0 处 | A | L1 | 0 处 |
| 22 | 引用共享 | controller.js | 见 §13.3 | A | L2 | 11 个对象引用类型 |
| 23 | async | controller.js | 见 §14 | A | L2 | 17 异步 + 4 API 链 |
| 24 | 重复提交防护 | controller.js | 0 处 | A | L1 | **未观察到**（A 级） |
| 25 | 对象—动作矩阵 | controller.js | 见 §17 | A | L3 | 27 行 |
| 26 | API—对象矩阵 | controller.js | 见 §18 | A | L3 | 14 API 行 |

### 19.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 26 | 100% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0%（严禁 E 升 A） |
| F | 0 | 0% |

### 19.2 L1/L2/L3 分布

| 级别 | 含义 | 数量 | 项 |
|---|---|---:|---|
| L1 | Controller 注册层（动作、入口、State、edit、clone） | 9 | 01, 02, 03, 14, 16, 17, 18, 19, 21, 24 |
| L2 | Controller 内部层（动作→API、对象→API、闭环） | 9 | 04, 05, 07, 09, 10, 12, 13, 15, 20, 22, 23 |
| L3 | 字段级层（容器、字段、对象传播、provenance、矩阵） | 6 | 06, 08, 11, 25, 26 |

注：部分项横跨多个级别，按主要维度归类。

### 19.3 F 边界

| # | F 项 | 详情 |
|---:|---|---|
| 1 | HTML 触发函数 | 7 untracked HTML 中 0 处 optometry 模板 |
| 2 | 离开 optometryGlassesCtrl 方式 | 0 处 $state.go / window.open / location.href |
| 3 | `response.object` 实际字段集 | 仅访问 4 字段 |
| 4 | ListFactory items 消费者 | 0 处显式消费，HTML 可能消费 |
| 5 | HTML 重复提交防护 | 可能由 ng-disabled 控制（源码不可得） |
| 6 | optometryGlasses State 配置 | 0 处 .state() 注册 |
| 7 | `saleInfo.ajaxUrl` 是否实际触发 | 字符串定义但未在 Controller 实际调用（可能在 HTML 弹窗） |

---

## 20. 三级数据边界

| 级别 | 含义 | 本轮处理 |
|---|---|---|
| L1 | Controller / API / Scope / State | **本轮主要范围** |
| L2 | 业务流程解释 | 仅在已有源码证据下记录 |
| L3 | DB / Entity / FK | **F 边界**（无后端证据） |

### 20.1 L1（本轮完成）

- Controller 注册 / DI / 行范围
- API 调用 / Factory / Read / Write
- Scope 字段 / 派生 / 共享
- State 出口
- 异步链 / 重复提交防护（缺失）

### 20.2 L2（部分记录）

- medicalRecord 字段消费（2 字段）
- patient + customer 字段消费
- methodGlassRecord 字段消费
- product / stock 字段消费

### 20.3 L3（不进入）

- medicalRecord 数据库主键
- patient / customer 表关系
- methodGlassRecord 表结构
- product / medicalProduct 表结构
- medicalRecordId 外键关系

**L3 全部 F 边界**（无 controller.js 范围内的后端证据）

---

## 21. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态源码分析 | ✅ |
| 2. API actual | 0（无任何 F5/F6/FN_promiseCall 实际调用） |
| 3. Write actual | 0 |
| 4. 不打开真实业务页面 | ✅ |
| 5. 不执行业务动作 | ✅ |
| 6. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-109 一致） |
| 7. 不修改 7 HTML | ✅ |
| 8. 不修改历史 MD（154-170） | ✅（**165/166/167/168/169/170 全部未改**） |
| 9. P0 = 54 冻结 | ✅ |
| 10. P1 = 8 冻结 | ✅ |
| 11. 10 untracked 原样保留 | ✅ |
| 12. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 22. 最终三维 DAG

### 22.1 动作—对象—API 三维矩阵

```
[动作]                       [对象]                          [API]
─────────────────────────────────────────────────────────────────
$scope.getMedicalRecord     $scope.medicalRecord           getMedicalRecord.json
                            $scope.medicalRecordId         FN_promiseCall[getPatientInfo, getCustomerVo]

$scope.GetMethodGlassRecordVo  $scope.object               getMethodGlassRecordVo.json

$scope.queryCompanyName     $scope.companyName             getCompanyOfMine.json
                            → $scope.queryStorehouseId    → selectStorehouseListOfCompany.json
                              $scope.lockStorehouseId

$scope.GetMedicalProductVoList  $scope.tempShop            getMedicalProductVoList.json
                               $scope.stockInSkuList      → $scope.processBasicData
                               $scope.glassesInfo         → $scope.save

$scope.searchProductList    $scope.glassesInfo             getProductSkuExistCountVoList.json (ListFactory)
                            $scope.getCorpListFactory

$scope.deleteReceipt        $scope.stockInSkuList          checkBeforeDeleteMedicalProduct.json

$scope.queryStore           $scope.glassesInfo             getProductSkuExistCountVoList.json (ObjectFactory)

$scope.updatePatient        $scope.userInfo                FN_promiseCall[savePatientInfo, saveCustomerInfo]

$scope.saveChufang          $scope.object                  updateMethodGlassRecord.json

$scope.save                 $scope.glassesInfo             saveMedicalProductListOfSmallVersion.json
                            $scope.stockInSkuList        → Popup + $scope.GetMedicalProductVoList (Refresh)
                            $scope.lockStorehouseId
                            $scope.medicalRecordId

saleInfo.fn (局部)          $scope.object.secondDoctorId   FN_promiseCall[updateMedicalRecord]
                                                          → $scope.saveChufang (链式)
```

### 22.2 完整 DAG（含链式）

```
[外部入口]
optometryCtrl.beginCustomerCheckin success
  → $state.go("optometryGlasses", { medicalRecordId })  [edit 未传]
optometryCtrl.fnMap "修改"
  → $state.go("optometryGlasses", { medicalRecordId, edit: "true" })

↓

[optometryGlassesCtrl Init L35383]

$stateParams.medicalRecordId (L35388) → $scope.medicalRecordId
$stateParams.edit (L35389) → $scope.edit
$scope.medicalRecord = {} (L35390)

↓

[Init 异步链 1] window.getStockSet (L35385) [独立异步]
  └─ $scope.enableNegativeStock (L35386)

[Init 立即 1] $scope.GetMethodGlassRecordVo() (L35623)
  └─ Read getMethodGlassRecordVo.json { medicalRecordId: $scope.medicalRecordId }
     └─ for-in $scope.object 覆盖 27+ 字段
     └─ processBasicData (未触发，等待 tempShop)

[Init 立即 2] $scope.queryCompanyName() (L35682)
  └─ Read getCompanyOfMine.json
     └─ success: $scope.companyName + $scope.queryStorehouseId(res.object.id)
        └─ Read selectStorehouseListOfCompany.json { companyId, mcTypeSortType: "ASC" }
           └─ success: $scope.lockStorehouseId

[Init 立即 3] $scope.GetMedicalProductVoList() (L35755)
  └─ Read getMedicalProductVoList.json { medicalRecordId: $scope.medicalRecordId }
     └─ forEach res.result.list
        ├─ tempList → $scope.tempShop
        └─ list (19 字段映射) → $scope.stockInSkuList
     └─ $scope.processBasicData()
        └─ forEach $scope.tempShop → $scope.glassesInfo (12 字段)

[Init 立即 4] $scope.getMedicalRecord() (L35958) ← 最后执行
  └─ Read getMedicalRecord.json { id: $scope.medicalRecordId }
     └─ success: $scope.medicalRecord = response.object (L35419)
        ├─ saleInfo.inputVal = $scope.medicalRecord.secondDoctorName
        ├─ saleInfo.id = $scope.medicalRecord.secondDoctorId
        ├─ $scope.object.secondDoctorId = saleInfo.id
        ├─ $scope.saleInfo = saleInfo
        └─ FN_promiseCall[getPatientInfo{ id: response.object.patientId }, getCustomerVo{ customerId: response.object.customerId }]
           └─ $scope.userInfo (15 字段, 在 $timeout 内)

↓

[外部 HTML 触发 - F 边界]
HTML → saleInfo.fn() (L35420)
  └─ [Write #1] FN_promiseCall updateMedicalRecord { id, secondDoctorId }
     └─ success: $scope.saveChufang()
        └─ [Write #2] updateMethodGlassRecord { $scope.object }
           └─ (空 success)

HTML → $scope.updatePatient() (L35496)
  └─ 校验 customer.linkMobile (L35529)
  └─ 构造 patient + customer 局部对象
  └─ [Write #3 + #4] FN_promiseCall[savePatientInfo{patient}, saveCustomerInfo{customer}]
     └─ success: $timeout(Popup.notice("修改成功!"))

HTML → $scope.saveChufang() (L35635) [直接触发或 saleInfo.fn 链式触发]
  └─ 校验 $scope.object.secondDoctorId
  └─ $scope.object.medicalRecordId = $scope.medicalRecordId
  └─ delete $scope.object.lastRxTime if empty
  └─ [Write #2] updateMethodGlassRecord { $scope.object }

HTML → $scope.save() (L35911)
  └─ 构造 medicalProductParamListJson (1-3 循环 + stockInSkuList)
  └─ 校验非空
  └─ [Write #5] saveMedicalProductListOfSmallVersion { medicalRecordId, medicalProductParamListJson }
     └─ success: Popup.notice("保存成功!") + $scope.GetMedicalProductVoList() (Refresh)
        └─ Read getMedicalProductVoList.json (再次执行 Init 立即 3 流程)

HTML → $scope.deleteReceipt(index, medicalProductId) (L35824)
  └─ [Read] checkBeforeDeleteMedicalProduct.json { medicalProductId }
     └─ success: $scope[""+key].splice(index, 1)

HTML → $scope.queryStore(key, key2) (L35848)
  └─ [Read] getProductSkuExistCountVoList.json { store }
     └─ success: $scope.glassesInfo["..."+key] 4-5 字段

HTML → $scope.searchProductList(keyword, num) (L35774)
  └─ 构造 parmas
  └─ [Read] getProductSkuExistCountVoList.json (ListFactory)

HTML → $scope.setProduct(product, key) (L35805)
  └─ $scope.glassesInfo 写入 2 字段
  └─ $scope.queryStore(key) (链式)

HTML → $scope.showsupplierList(event, key, num) (L35768)
  └─ $scope.prevent(false)
  └─ $scope[""+key+num] = true
  └─ $scope.searchProductList("", num) (链式)

HTML → $scope.update(key, key2, num) (L35624)
  └─ 条件分支
  └─ $scope.glassesInfo[""+key2+num] = $scope.object[key]
  └─ $scope.queryStore(num) (条件)
  └─ $scope.saveChufang()

HTML → $scope.update2(key) (L35631)
  └─ $scope.object[key] = ""
  └─ $scope.saveChufang()

HTML → $scope.printChufang.print() (L35654) [F 边界：弹窗行为]
HTML → $scope.printShoufei.print() (L35844) [F 边界：弹窗行为]
HTML → $scope.addStore.switch(bool) (L35817) [F 边界：弹窗行为]
HTML → $scope.addStore.callback(info) (L35820) [F 边界：弹窗 callback]

↓

[State 出口: 0 处]
[F 边界：HTML 决定离开方式]
```

---

## 23. 关键发现

### 23.1 S1-108/109 错误纠正

| 项 | S1-108/109 | S1-110 实际 | 差异 |
|---|---|---|---|
| saveOrQuery call site | 10 | **9** | 减少 1 |
| call site 总数 | 14 | **13** | 减少 1 |
| unique API | 14 | 14 | 一致 |
| 触发 URL 总数 | （未明确） | **15** | 新增 |

**原因**：S1-108/109 把 9 个 saveOrQuery 误数成 10，把 13 个 call site 误数成 14。S1-110 用 Select-String 重新扫描确认：

```powershell
Select-String -Path 'controller.js' -Pattern 'saveOrQuery' | 
  Where-Object { $_.LineNumber -ge 35383 -and $_.LineNumber -le 35959 }
```

**实际 9 个 saveOrQuery call site**（按行号）：
- 35416, 35604, 35644, 35662, 35675, 35685, 35827, 35884, 35950

### 23.2 medicalRecord 回读闭环

- **0 处回读**：5 个 Write success 后均不回读 medicalRecord
- 1 次 Init 整体赋值（L35419）后**保持不变**
- medicalRecord 是"读一次"模式

### 23.3 重复提交防护

- **0 处** disabled / loading / debounce / lock / flag / isLoading / isSubmitting
- 当前 Controller **未观察到**任何重复提交防护
- HTML 可能存在 ng-disabled（F 边界）

### 23.4 edit 模式再确认

- edit = false 与 edit = true 在 Controller 业务逻辑上**完全等价**
- 0 处影响 API / State / Init / 页面数据
- 唯一可能差异在 HTML UI（F 边界）

### 23.5 异步边界

- 17 个异步调用（9 saveOrQuery + 1 ListFactory + 3 FN_promiseCall + 3 $timeout + 1 window.getStockSet）
- 4 条 API success → API 链
- 0 处 `$q.all` / `Promise.all` / `async/await`
- 4 个 Init 立即执行**无顺序保证**（潜在风险点）

### 23.6 主对象分类

按源码实际命名：
- medicalRecord（getMedicalRecord 主体）
- patient + customer（FN_promiseCall 派生）
- methodGlassRecord（getMethodGlassRecordVo 嵌套）
- product / productSku / brand / category / medicalProduct / medicalProductSign / lockStorehouse（getMedicalProductVoList 嵌套）
- company（getCompanyOfMine 返回）
- employee（saleInfo.key，仅字段名）

**未出现**（严禁虚构）：
- examination / prescription / machine / machineCenter / template / customerCheckin / order

---

## 24. 与 S1-108/109 一致性

| 项 | S1-108 | S1-109 | S1-110 | 变化 |
|---|---|---|---|---|
| Controller 范围 | L35383-L35959 | L35383-L35959 | L35383-L35959 | 一致 |
| DI | 7 个 | 7 个 | 7 个 | 一致 |
| unique API | 14 | 14 | 14 | 一致 |
| call site | 14 | 14 | **13** | S1-110 纠正 |
| saveOrQuery call site | 10 | 10 | **9** | S1-110 纠正 |
| Read unique | 9 | 9 | 9 | 一致 |
| Write unique | 5 | 5 | 5 | 一致 |
| $state.go | 0 | 0 | 0 | 一致 |
| $scope.lockStorehouseId 来源 | F | A | A | S1-109 闭合 |
| medicalRecordId 路径 | 5 类 | 5 类 | 5 类 | 一致（无新路径） |
| edit 模式 | 0 影响 | 0 影响 | 0 影响 | 一致 |
| medicalRecord 字段消费 | 2 字段 | 2 字段 | 2 字段 | 一致 |
| medicalRecord 回读 | 0 次 | 0 次 | 0 次 | 一致（首次显式记录） |
| 重复提交防护 | （未检查） | （未检查） | **0 处** | S1-110 新增 |

---

## 25. 最终结论

### 25.1 三维闭环完整性

- 动作：21 个 $scope 函数 + 12 个内部 callback（共 33 个动作点）
- 对象：11 个 $scope 字段/对象 + 11 个局部对象
- API：9 saveOrQuery + 1 ListFactory + 3 FN_promiseCall = 13 call site（14 unique API）

**三维闭环完成度**：100% A 级

### 25.2 关键风险

1. **重复提交防护缺失**：5 个 Write 均无 disabled/loading/flag 防护（A 级）
2. **medicalRecord 无回读**：5 个 Write 后不回读 medicalRecord，UI 可能有数据陈旧风险
3. **edit 模式 0 影响**：入口"新增"和"修改"在 Controller 业务逻辑上等价（F 边界：HTML 可能差异）
4. **异步顺序未保证**：4 个 Init 立即执行无时序控制

### 25.3 闭环健康度

- 9 个 Read 全部有 Scope 落点 + 后续 Consumer
- 5 个 Write 全部有完整字段级 provenance
- 1 条 Write→Read 刷新链（save → GetMedicalProductVoList）
- 1 条 Write→Write 链式（updateMedicalRecord → saveChufang → updateMethodGlassRecord）
- 0 条 Write→State 链

---

**审计完成。本文档为 171 号，提交后将形成 tracked=180。**
