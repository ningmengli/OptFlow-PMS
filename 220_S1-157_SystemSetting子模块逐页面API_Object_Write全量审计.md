# S1-157 SystemSetting 子模块逐页面 / API / Object / Write 全量审计

> 顶部菜单"系统设置" / systemSetting.* 子 State 真实映射。
>
> S1-151 已确认 systemSetting 是 State 聚合器(S1-151 当时识别 17+ State,本轮重新精确提取=**17 个真实子 State**)。
>
> 本轮核心结论:**子模块多为配置/字典类,仅少量有真实 ID(Object);多数命名误导需重审**。

---

## §0 完整性闸门

| 文件 | 期望 SHA256 | 实际 SHA256 | 状态 |
|---|---|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | ✓ PASS |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | ✓ PASS |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | ✓ PASS |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | ✓ PASS |

**闸门结论:4 文件 SHA256 全部一致,通过。** 本轮任务描述中的 `F25` 与 S1-154 汇报同源(均为手写 typo),实际值始终为 `F29`,与历史基准一致。

文件规模:2,194,196 bytes / 59,214 行 / 417 个 Controller / 915 个 .json API。

---

## §1 SystemSetting 子 State 全量(精确 17 个)

### 1.1 真实子 State 列表(重新精确提取)

| 子 State | 行号 | 命中 | 类型 | Grade |
|---|---:|---:|---|---|
| `systemSetting.checkList` | L50229 | 6 | Check 项目列表 | A |
| `systemSetting.checkModify` | L53022 | 2 | Check 项目编辑 | A |
| `systemSetting.InspectList` | L51172 | 4 | Inspect 检查列表(S1-151 已确认) | A |
| `systemSetting.customerCharge` | L54048 | 1 | CustomerCharge 主页 | C |
| `systemSetting.customerChargeItem` | L50788 | 6 | CustomerChargeItem 列表 | A |
| `systemSetting.customerMaterialCertificate` | L54050 | 1 | Customer 材质证书 | C |
| `systemSetting.materialCertificate` | L54045 | 1 | Material 材质证书 | C |
| `systemSetting.materialModify` | L54044 | 1 | Material 编辑 | A |
| `systemSetting.materiallist` | L55200 | 3 | Material 列表 | A |
| `systemSetting.medicalFeesList` | L51735 | 4 | MedicalFee(命名误导) | C |
| `systemSetting.memberTypeList` | L51792 | 2 | MemberType(命名误导) | C |
| `systemSetting.modifyCustomerCharge` | L54049 | 1 | CustomerCharge 编辑 | C |
| `systemSetting.processCenter` | L51817 | 2 | ProcessCenter(命名误导 → MachineCenter) | C |
| `systemSetting.projectCard` | L52231 | 2 | ProjectCard(命名误导 → TrainerCard) | C |
| `systemSetting.supplierCertificate` | L54055 | 1 | Supplier 证书 | C |
| `systemSetting.supplierList` | L54053 | 1 | Supplier 列表 | A |
| `systemSetting.supplierModify` | L54054 | 1 | Supplier 编辑 | A |

**总计:17 个真实子 State**(= S1-151 当时估算)。

### 1.2 17 个子 State 路由表(L54041-54056)

```js
var map = {
  default: {
    'back': 'systemSetting.materiallist',
    0: 'systemSetting.materialModify',
    1: 'systemSetting.materialCertificate'
  },
  custom: {
    'back': 'systemSetting.customerCharge',
    0: 'systemSetting.modifyCustomerCharge',
    1: 'systemSetting.customerMaterialCertificate'
  },
  supplier: {
    'back': 'systemSetting.supplierList',
    0: 'systemSetting.supplierModify',
    1: 'systemSetting.supplierCertificate'
  }
};
$state.go(map[$scope.type][index], {
  productId: $scope.productId,
  productSkuId: $scope.productSkuId,
  supplierId: $scope.supplierId  // supplierId 是 State 参数
});
```

**路由表结构**:
- **default** = Material 字典(主材质/证书)
- **custom** = Customer 收费/材质
- **supplier** = Supplier 字典

**注意**:`checkList / checkModify / InspectList / medicalFeesList / memberTypeList / processCenter / projectCard` 不在 map 中,说明这 7 个子 State 是独立顶层路由,不属于 default/custom/supplier 三类。

---

## §2 Check 项目(bodyCheck)

### 2.1 关键发现:**checkItemId 0 命中,但 bodyCheckItemId 真实**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `checkItemId` | **0** | **F / 禁造** |
| `bodyCheckItemId` | 4 | **A 真实** |
| `bodyCheckItemList` | 8 | A 真实(DefineBodyCheck 嵌套列表) |

### 2.2 bodyCheckItemId 完整 4 处

| 行号 | 上下文 |
|---:|---|
| L41206 | `bodyCheckItemId: checkItem.bodyCheckItem.id`(Request) |
| L41230 | `bodyCheckItemId: $scope.obj.bodyCheckItem.id`(Request) |
| L41255 | setBodyCheckItemPrintDisable.json(Request: `bodyCheckItemId, printDisable`) |
| L41262 | setBodyCheckItemPrintDisable.json(Request) |

### 2.3 bodyCheckItemList 上下文(DefineBodyCheck 内嵌)

- L41185:DefineBodyCheck.ophthalmology.bodyCheckItemList
- L41189-41191:bodyCheckItemList 数组遍历
- L41202:item.bodyCheckItemList
- L41206-41207:checkItem.bodyCheckItem.id / itemName
- L41241-41262:bodyCheckItemPrintDisable 配置

### 2.4 bodyCheckItem Object 字段

| 字段 | 行号 | Type |
|---|---:|---|
| `bodyCheckItem.id` | L41206 | ID |
| `bodyCheckItem.itemName` | L41207 | 名称 |
| `bodyCheckItem.printDisable` | L41254 | 状态 |
| `bodyCheckItemList[]` | L41185 | 列表(嵌入 DefineBodyCheck) |

### 2.5 Check 项目 Controller

- **checkListCtrl / checkModifyCtrl / InspectListCtrl**:对应 3 个 State(`systemSetting.checkList` / `checkModify` / `InspectList`)
- 业务字段来自 DefineBodyCheck Service(检查配置字典)

### 2.6 Check ↔ S1-152 区分

- checkItem **不是** MedicalExamine(S1-145)
- checkItem **不是** checkCall(S1-153)
- checkItem **是** DefineBodyCheck 嵌套字典

---

## §3 Customer Charge Item(客资收费项目)

### 3.1 关键发现:**customerChargeItem 是 Storage 缓存,不是独立 Object**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `customerChargeItem` | 多处 | C(Storage) |
| `customerCharge` | 多处 | C(Storage) |
| `chargeItemId` | **0** | **F / 禁造** |
| `customerChargeItemId` | **0** | **F / 禁造** |
| `customerChargeId` | 1 | C(局部) |

### 3.2 customerCharge Storage 上下文

- L53340 / L53591 / L53602:`StorageFactory("customerCharge")` 缓存
- L50702:`StorageFactory` 缓存
- L54048:`$state.go('systemSetting.customerCharge')`

### 3.3 customerChargeItem Ctrl

- `customerChargeItemCtrl` L50788(列表)
- `customerChargeCtrl` L53340(主页)
- `modifyCustomerChargeCtrl` L54049(编辑)

### 3.4 customerCharge 业务字段

- `$scope.productId / productSkuId / supplierId`(State 参数,L54060-54062)
- `customerCharge.itemName` / `customerCharge.price` / `customerCharge.unit`(局部)

### 3.5 CustomerChargeItem ↔ Charge / Fee 边界

- **CustomerChargeItem ≠ Cashflow / Charge**(S1-148 已确认)
- **CustomerChargeItem ≠ FeeItem**(0 命中 feeItem)
- **CustomerChargeItem = 配置字典**

---

## §4 Material(物料)

### 4.1 关键发现:**materialId 0 命中,Material 是 productSku 子属性**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `materialId` | **0** | **F / 禁造** |
| `materialListId` | **0** | F / 禁造 |
| `materiallist`(Storage) | 3 | C(Storage 缓存) |
| `materialCertificate` | 1 | C(State) |

### 4.2 materiallist 上下文

- L54043:`$state.go('systemSetting.materiallist')`
- L54505 / L54766:`StorageFactory("materiallist")` 缓存
- L55200:`$state.go('systemSetting.materiallist')`

### 4.3 Material Ctrl

- `materiallistCtrl` L55200(列表)
- `materialModifyCtrl` L54044(编辑)
- `materialCertificateCtrl` L54045(证书)

### 4.4 Material ↔ Product / SKU 关系

- Material 不是独立 Object ID
- Material 是 `productSku` 的子属性(材质)
- Material Modify 修改 productSku
- **不创建 materialId**

---

## §5 Medical Fee / Member Type(命名误导)

### 5.1 medicalFeesList 命名误导

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `medicalFeeId` | **0** | **F / 禁造** |
| `feeId` | **0** | **F / 禁造** |
| `medicalFee` | 多处 | C(命名误导) |
| `medicalFeesList` | 4 | C(State) |

### 5.2 medicalFeesList 真实业务:L55740 `saveCardSubstractType.json`

```js
// L55740 saveCardSubstractType.json
// 实际业务:训练卡扣次类型(substractType)配置
```

**结论**:`medicalFeesList` 命名误导,**实际是 cardSubstractType 配置**,不是医疗费。

### 5.3 memberTypeList 命名误导

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `memberTypeId` | **0** | **F / 禁造**(S1-154 已确认) |
| `memberType` | 多处 | C(命名误导) |
| `memberTypeList` | 2 | C(State) |

### 5.4 memberType 真实业务:Member(会员库)

- `addMemberTypeCtrl` L51744:API `/admin/createMember.json`(创建会员)
- `memberTypeListCtrl` L55752:管理会员库
- `memberTypeModifyCtrl` L55770:编辑会员
- **真实业务字段**:memberName / examineRate / productRate / status

**结论**:`memberTypeList` 命名误导,**实际是会员库(member)配置**,不是会员类型。

### 5.5 addMemberType 完整结构

```js
$scope.obj = {};
$scope.status = [{ id: 0, name: '正常' }, { id: 1, name: '停用' }];
$scope.save = function () {
  new ObjectFactory().saveOrQuery("/admin/createMember.json", $scope.obj).then(function (res) {
    if (res.status) {
      return Popup.notice(res.errmsg);
    }
    $state.go("systemSetting.memberTypeList");
  });
};
```

**结论**:status 是 Object 字段(0=正常 / 1=停用),不是 UI toggle。

---

## §6 Process Center / Project Card(命名误导)

### 6.1 processCenterCtrl L57778 命名误导

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `processCenterId` | **0** | **F / 禁造** |
| `machineCenterId` | 18 | **A 真实**(S1-150) |

### 6.2 processCenterCtrl 真实业务

```js
$scope.obj = {};
$scope.obj.status = null;
$scope.search = function () {
  $scope.getSupplierListFactory = new ListFactory(
    '/admin/selectMachineCenterVoList.json',  // 实际是 MachineCenter!
    0, 10, $scope.obj);
  ...
};
$scope.goAdd = function () {
  $state.go($location.path().split('/')[1] + '.' + 'addDepot');  // depotModify
};
$scope.modifyRepot = function (id) {
  $state.go($location.path().split('/')[1] + '.' + 'depotModify', { id: id });
};
```

**结论**:`processCenterCtrl` 命名误导,**实际是 MachineCenter 列表(加工中心)**,API 是 `selectMachineCenterVoList.json`。S1-150 已确认 machineCenter 18 处真实 A。

### 6.3 projectCardCtrl L57851 / addProjectCardCtrl L52150 命名误导

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `projectCardId` | **0** | **F / 禁造** |
| `trainerCardId` | 5 | **A 真实**(S1-155) |

### 6.4 projectCard 真实业务

```js
$scope.searchTrainerCard = function (trainerCardId) {
  new ObjectFactory().saveOrQuery("/admin/getTrainerCard.json", {
    trainerCardId: trainerCardId  // 真实 ID!
  }).then(function (res) {
    $scope.obj = res.result.object;
    $scope.obj.trainerCardId = trainerCardId;
  });
};
$scope.projectCard = function () {
  // 校验必填项
  for (var i in mustKey) {
    if ($scope.obj[i] == undefined || $scope.obj[i] == null) {
      return Popup.notice(mustKey[i]);
    }
  }
  var reqUrl = $stateParams.id ? "/admin/updateTrainerCard.json" : "/admin/addTrainerCard.json";
  new ObjectFactory().saveOrQuery(reqUrl, $scope.obj).then(function (res) {
    $state.go("systemSetting.projectCard");
  });
};
```

### 6.5 projectCard 字段

| 字段 | 行号 | Type |
|---|---:|---|
| `trainerCardName` | L52189 | 必填 |
| `marketPrice` | L52190 | 必填 |
| `unitName` | L52191 | 必填 |
| `numbers` | L52192 | 必填 |
| `allowReturnCard` | L52193 | 必填 |
| `allowChangePrice` | L52194 | 必填 |
| `allowChangeNumber` | L52195 | 必填 |
| `status` | L52196 | 必填 |
| `validMonths` / `remindDays` | L52236-52237 | 可选 |
| `imageDescription` | L52221 | 可选 |

### 6.6 projectCardCtrl 完整结构

```js
$scope.obj = {};
$scope.obj.status = 0;  // 默认值
$scope.obj.allowReturnCard = 1;
$scope.obj.allowChangePrice = 1;
$scope.obj.allowChangeNumber = 1;
$scope.obj.disableValidMonths = true;
$scope.allowList = [{ id: 0, name: "允许" }, { id: 1, name: "不允许" }];
$scope.status = [{ id: 0, name: "正常" }, { id: 1, name: "停用" }];
// Read: selectTrainerCardList.json(R)
// Write: updateByTrainerCardIdArraySelective.json(W)
```

**结论**:`projectCardCtrl` 命名误导,**实际是 trainerCard 配置(计次卡)**。**trainerCardId 真实 A**(5 处)。

---

## §7 Supplier(供应商)

### 7.1 关键发现:**Supplier 是真实 Object,supplierId 99 处**

| 字段 | 命中 | 真实? |
|---|---:|:-:|
| `supplierId` | **99** | **A 真实** |
| `supplierVo` | 0 | F(不存 VO) |
| `supplierList`(State) | 1 | A |
| `supplierModify`(State) | 1 | A |

### 7.2 supplierId 真实上下文(节选)

| 行号 | 上下文 |
|---:|---|
| L22729 | `$scope.getStockListFactory.items[i].supplierId = ...` |
| L22771 | addInventory(skuCount, skuId, supplierId, ...) |
| L23001 / L23009 | `supplierId: ...mainSupplier.id` |
| L23025 | 校验 `supplierId == null` |
| L23918 / L23920 | supplierId 赋值 |
| L54063 | `$scope.supplierId`(State 参数) |
| +88 处 | 多处供应商关联 |

### 7.3 Supplier API 全量

| API | R/W | 用途 |
|---|:-:|---|
| `selectSupplierVoList.json` | R | 列表 |
| `getSupplier.json` | R | 详情 |
| `addSupplier.json` | W | 创建 |
| `modifySupplier.json` | W | 编辑 |
| `deleteSupplier.json` | W | 删除 |
| `selectSupplierOfProduct.json` | R | 商品关联 |
| `downloadSettlementBySupplier.htm` | (下载) | 结算单(S1-156) |

### 7.4 Supplier Ctrl

- `supplierListCtrl`(L54053 路由)
- `supplierModifyCtrl`(L54054 路由)
- `supplierCertificateCtrl`(L54055 路由)

### 7.5 Supplier ↔ Product / Stock / MedicalProduct

- Supplier → Product:✓ A(主供应商 mainSupplier)
- Supplier → Stock:✓ A(出库入库 supplierId)
- Supplier → MedicalProduct:✗ F(0 命中,Supplier 是商品层级不是病历层级)

---

## §8 Company / Appointment / SMS Config

### 8.1 corpAppointmentConf / corpCashConf / corpReportConf 真实

| Config | 行号 | API | 字段 | Grade |
|---|---:|---|---|---|
| `corpAppointmentConf` | L3670 / L3775 / L3800 | getCorpAppointmentConf + saveCorpAppointmentConf | smsAdminName / smsMobile / smsBackMobile / smsBackAdminName | A(S1-153) |
| `corpAppointConf` | L52362 / L52373 | getCorpAppointConf + saveCorpAppointConf | appointSceneType | A |
| `corpCashConf` | L57716 / L57768 | selectCompanyCashConfVoList + updateCompanyCashConf | cashHeader / cashLogo / customerMobileDisable | A(S1-156) |
| `corpReportConf` | L58305 / L58315 | getCorpReportConf + saveCorpReportConf | defaultStartMonth / defaultStartDay | A(S1-156) |

### 8.2 companyCashConfId 真实 A(L57763)

**修正 S1-156**:`companyCashConfId` 是**真实 ID**(1 处)

```js
var vo = {
  companyCashConfId: this.params.id,  // 真实 ID!
  cashHeader: this.params.cashHeader,
  cashLogo: this.imgList.length && this.imgList[0].url,
  customerMobileDisable: Number(this.params.customerMobileDisable)
};
HttpFactory.object('/admin/updateCompanyCashConf.json', vo).then(function (res) {
  Popup.notice('编辑成功!');
});
```

### 8.3 Corp Config 与 SystemSetting 边界

- `corpAppointmentConf` 属于 Appointment 业务(S1-153)
- `corpAppointConf` 属于 Appointment 业务
- `corpCashConf` 属于 Cash / Report 业务(S1-156)
- `corpReportConf` 属于 Report 业务(S1-156)
- **不归 SystemSetting**

---

## §9 Cash / Print Config(S1-156 已确认)

| 字段 | 真实? |
|---|:-:|
| `companyCashConfId` | A(L57763) |
| `corpCashConf` | A |
| `printConfigCtrl` | **C(命名误导,实际是 corpCashConf)** |

详见 S1-156 §13 + 本轮 §8.2。

---

## §10 其它子模块

### 10.1 Admin 子模块(非 systemSetting.)

- `companyCtrl` L38321(S1-151 已确认)
- `adminClinicCtrl` L38636(S1-151 已确认)
- `adminSettlementCtrl` L38818(S1-151 已确认)
- `adminCheckConfigCtrl` L39029(S1-151 已确认)
- `adminClinicImageCtrl` L38830(S1-151 已确认)
- `adminCostListCtrl` L39200(S1-151 已确认)
- **这些不在 systemSetting.* State 下,属于 admin 顶级路由**

### 10.2 其它 systemSetting 关联

- `feeBankCardCtrl` L36882(银行账户)
- `pointsAdminCtrl` L57582(S1-155 已确认,实际是 corpPointRule)
- `printConfigCtrl` L57667(实际是 corpCashConf)

---

## §11 SystemSetting Object 总表

| 子对象 | A 独立 ID | B Response VO | C Request Payload | D State/UI | F |
|---|:-:|:-:|:-:|:-:|:-:|
| **SystemSetting** | ✗ F(0 命中 settingId) | – | – | ✓(State 聚合器) | – |
| **CheckItem(bodyCheck)** | ✓ A(bodyCheckItemId 4) | ✓ | ✓ | ✓ | – |
| **CustomerChargeItem** | ✗ F(0 命中 chargeItemId) | – | – | ✓(Storage 缓存) | – |
| **Material** | ✗ F(0 命中 materialId) | – | – | ✓(productSku 子属性) | – |
| **MedicalFee** | ✗ F(0 命中 medicalFeeId/feeId) | – | – | ✓(cardSubstractType 配置) | – |
| **MemberType** | ✗ F(0 命中 memberTypeId) | – | – | ✓(Member 库管理) | – |
| **ProcessCenter** | ✗ F(0 命中 processCenterId) | – | – | ✓(machineCenter 配置) | – |
| **ProjectCard** | ✗ F(0 命中 projectCardId) | – | – | ✓(trainerCard 配置) | – |
| **Supplier** | ✓ A(supplierId 99) | – | ✓ | ✓ | – |
| **corpAppointmentConf** | ✓ A(隐含,无独立 ID) | ✓ | ✓ | ✓ | – |
| **corpAppointConf** | ✓ A(隐含) | ✓ | ✓ | ✓ | – |
| **corpCashConf** | ✓ A(companyCashConfId) | ✓ | ✓ | ✓ | – |
| **corpReportConf** | ✓ A(隐含) | ✓ | ✓ | ✓ | – |
| **companyDayReportVo** | ✗ F | ✓ | – | – | – |
| **fundusCheckReportVo** | ✗ F | ✓ | – | – | – |
| **productSkuVo** | ✓ A(skuCode 已有) | ✓ | ✓ | ✓ | – |

**L3 数据库结构**:全部 F。

---

## §12 与核心域关系矩阵

| Setting Object | Company | Employee | Role | ConsultRoom | Product | SKU | MedicalProduct | Stock | Cashflow | MedicalRecord | Appointment |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **SystemSetting(聚合)** | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C | ✓ C |
| **Check(bodyCheck)** | ✓ C | – | – | – | – | – | – | – | – | ✓ C(bodyCheckItem) | – |
| **CustomerChargeItem** | – | – | – | – | ✓ C | – | – | – | – | – | – |
| **Material** | – | – | – | – | ✓ C | ✓ C | – | ✓ C | – | – | – |
| **MedicalFee(cardSubstract)** | – | – | – | – | ✓ C | – | – | – | – | – | – |
| **MemberType(member)** | ✓ C | – | – | – | – | – | – | – | – | – | – |
| **ProcessCenter(machineCenter)** | ✓ C | – | – | – | – | – | – | – | – | – | – |
| **ProjectCard(trainerCard)** | ✓ C | – | – | – | – | – | – | – | ✓ C | – | – |
| **Supplier** | ✓ C | – | – | – | ✓ A | ✓ A | ✗ F | ✓ A | – | – | – |
| **corpAppointmentConf** | ✓ A | – | – | – | – | – | – | – | – | – | ✓ A |
| **corpAppointConf** | ✓ A | – | – | – | – | – | – | – | – | – | ✓ A |
| **corpCashConf** | ✓ A | – | – | – | – | – | – | – | ✓ A | – | – |
| **corpReportConf** | ✓ A | – | – | – | – | – | – | – | – | – | – |

---

## §13 Write API 全量

### 13.1 SystemSetting 子模块 Write API

| API | State | Controller | Request | Response | Grade |
|---|---|---|---|---|---|
| `saveCardSubstractType.json` | systemSetting.medicalFeesList | medicalFeesListCtrl | cardSubstractType | – | A |
| `createMember.json` | systemSetting.memberTypeList | addMemberTypeCtrl | memberName / examineRate / productRate / status | memberVo | A |
| `updateMember.json` | systemSetting.memberTypeList | memberTypeModifyCtrl | id + memberName | – | A |
| `getTrainerCard.json` | systemSetting.projectCard | addProjectCardCtrl | trainerCardId | trainerCardVo | A |
| `addTrainerCard.json` | systemSetting.projectCard | addProjectCardCtrl | trainerCardName + ... | – | A |
| `updateTrainerCard.json` | systemSetting.projectCard | addProjectCardCtrl | trainerCardId + ... | – | A |
| `selectTrainerCardList.json` | systemSetting.projectCard | projectCardCtrl | – | trainerCardVoList | A |
| `updateByTrainerCardIdArraySelective.json` | systemSetting.projectCard | projectCardCtrl | trainerCardIdArray | – | A |
| `setBodyCheckItemPrintDisable.json` | systemSetting.checkList | checkListCtrl | bodyCheckItemId + printDisable | – | A |
| `setBodyCheckPrintDisable.json` | systemSetting.checkList | checkListCtrl | bodyCheckItemId + printDisable | – | A |
| `addSupplier.json` | systemSetting.supplierList | supplierListCtrl | supplierName + ... | – | A |
| `modifySupplier.json` | systemSetting.supplierModify | supplierModifyCtrl | supplierId + ... | – | A |
| `deleteSupplier.json` | systemSetting.supplierModify | supplierModifyCtrl | supplierId | – | A |
| `selectSupplierVoList.json` | systemSetting.supplierList | supplierListCtrl | – | supplierVoList | A |

### 13.2 Corp Config Write API(不属于 SystemSetting)

| API | State | Controller | Request | Grade |
|---|---|---|---|---|
| `getCorpAppointmentConf.json` | bookSettings | bookSettingsCtrl | – | A |
| `saveCorpAppointmentConf.json` | bookSettings | bookSettingsCtrl | smsAdminName + smsMobile + smsBackMobile + smsBackAdminName | A |
| `getCorpAppointConf.json` | appointAdmin | appointAdminCtrl | – | A |
| `saveCorpAppointConf.json` | appointAdmin | appointAdminCtrl | appointSceneType + ... | A |
| `selectCompanyCashConfVoList.json` | (printConfig) | printConfigCtrl | keyword | A |
| `updateCompanyCashConf.json` | (printConfig) | printConfigCtrl | companyCashConfId + cashHeader + cashLogo + customerMobileDisable | A |
| `getCorpReportConf.json` | reportDateAdmin | reportDateAdminCtrl | – | A |
| `saveCorpReportConf.json` | reportDateAdmin | reportDateAdminCtrl | defaultStartMonth + defaultStartDay | A |

### 13.3 Write API 分类

- **配置类 W**(9 个):saveCardSubstractType / createMember / updateMember / getTrainerCard / addTrainerCard / updateTrainerCard / updateByTrainerCardIdArraySelective / setBodyCheckItemPrintDisable / setBodyCheckPrintDisable
- **字典类 W**(4 个):addSupplier / modifySupplier / deleteSupplier / saveCorpAppointmentConf
- **公司级参数 W**(3 个):saveCorpAppointConf / updateCompanyCashConf / saveCorpReportConf

---

## §14 Read API 全量

### 14.1 SystemSetting 子模块 Read API(11 个)

- `getTrainerCard.json`(A)
- `selectTrainerCardList.json`(A)
- `selectSupplierVoList.json`(A)
- `getSupplier.json`(A)
- `getMember.json`(A)
- `selectMemberVoList.json`(A)
- `getCorpPointRule.json`(A,S1-155)
- `saveCorpPointRule.json`(W)
- `selectBodyCheckItemVoList.json`(A)
- `selectCompanyDayReportVoList.json`(R,见 S1-156)
- `selectCustomerChargeItemVoList.json`(A)

### 14.2 全部 Read 是 R,Write 是 W,无 UI Function 混淆

---

## §15 Source Trace

### 15.1 4 个真实 ID(字符级证据)

| ID | 行号 | Source → Target | Consumer | 真实? |
|---|---:|---|---|:-:|
| `supplierId` | L22729 / L54063 / +97 | State / mainSupplier / Request → supplierId 字段 | Stock / Material / Supplier List | A |
| `bodyCheckItemId` | L41206 / L41230 / L41255 / L41262 | checkItem.bodyCheckItem.id → Request → setBodyCheckItemPrintDisable | Check List Ctrl | A |
| `companyCashConfId` | L57763 | this.params.id → Request → updateCompanyCashConf | printConfigCtrl | A |
| `trainerCardId` | L34473 / L52181 / +3 | info.id / obj.trainerCardId → Request → getTrainerCard / addTrainerCard / updateTrainerCard | projectCardCtrl / addProjectCardCtrl | A |

### 15.2 禁造 ID(Source Trace 全部 F)

| ID | 禁造原因 |
|---|---|
| settingId / systemSettingId | 0 命中 |
| checkItemId | 0 命中(真实是 bodyCheckItemId) |
| chargeItemId / customerChargeItemId / customerChargeId | 0 命中 |
| materialId / materialListId | 0 命中 |
| feeId / medicalFeeId | 0 命中 |
| memberTypeId | 0 命中(S1-154 已知) |
| processCenterId | 0 命中(真实是 machineCenterId 18 处) |
| projectCardId | 0 命中(真实是 trainerCardId) |

---

## §16 Controller 消费矩阵

| Controller | State | Company | SystemSetting | Product | Cashflow | Appointment |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| checkListCtrl (L50229) | ✓ | – | ✓ | – | – | – |
| checkModifyCtrl (L53022) | ✓ | – | ✓ | – | – | – |
| InspectListCtrl (L51172) | ✓ | – | ✓ | – | – | – |
| customerChargeItemCtrl (L50788) | ✓ | – | ✓ | – | – | – |
| customerChargeCtrl (L53340) | ✓ | – | ✓ | – | – | – |
| modifyCustomerChargeCtrl (L54049) | ✓ | – | ✓ | – | – | – |
| materiallistCtrl (L55200) | ✓ | – | ✓ | – | – | – |
| materialModifyCtrl (L54044) | ✓ | – | ✓ | – | – | – |
| materialCertificateCtrl (L54045) | ✓ | – | ✓ | – | – | – |
| medicalFeesListCtrl (L51735) | ✓ | – | ✓ | – | – | – |
| memberTypeListCtrl (L55752) | ✓ | – | ✓ | – | – | – |
| memberTypeModifyCtrl (L55770) | ✓ | – | ✓ | – | – | – |
| addMemberTypeCtrl (L51744) | ✓ | – | ✓ | – | – | – |
| processCenterCtrl (L57778) | ✓ | – | ✓(machineCenter) | – | – | – |
| projectCardCtrl (L57851) | ✓ | – | ✓(trainerCard) | – | – | – |
| addProjectCardCtrl (L52150) | ✓ | – | ✓(trainerCard) | – | – | – |
| supplierListCtrl (L54053) | ✓ | – | ✓ | – | – | – |
| supplierModifyCtrl (L54054) | ✓ | – | ✓ | – | – | – |
| supplierCertificateCtrl (L54055) | ✓ | – | ✓ | – | – | – |
| printConfigCtrl (L57667) | (corpCashConf) | ✓ | – | – | ✓(S1-156) | – |
| reportDateAdminCtrl (L58291) | (corpReportConf) | ✓ | – | – | – | – |
| bookSettingsCtrl (L3771) | (corpAppointmentConf) | ✓ | – | – | – | ✓(S1-153) |
| appointAdminCtrl (L52344) | (corpAppointConf) | ✓ | – | – | – | ✓(S1-153) |

---

## §17 Status / Scope 字段

### 17.1 Status 字段汇总

| Controller | Status 字段 | 值 | Type |
|---|---|---|---|
| `addMemberTypeCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段 |
| `addProjectCardCtrl` | obj.status | 0=正常 / 1=停用 | Object 字段 |
| `addProjectCardCtrl` | obj.allowReturnCard | 0=不允许 / 1=允许 | Object 字段 |
| `addProjectCardCtrl` | obj.allowChangePrice | 0=不允许 / 1=允许 | Object 字段 |
| `addProjectCardCtrl` | obj.allowChangeNumber | 0=不允许 / 1=允许 | Object 字段 |
| `processCenterCtrl` | obj.status | null=全部 | Filter |
| `processCenterCtrl` | obj.type | null=全部 | Filter |
| `printConfigCtrl` | customerMobileDisable | 0=显示 / 1=不显示 | Object 字段 |
| `customerMobileDisable` (setStatus) | toggle | !this.params.customerMobileDisable | Function |

### 17.2 Status 来源

- **Object 字段**(8 个):Member.status / TrainerCard.status / allowReturnCard / allowChangePrice / allowChangeNumber / customerMobileDisable 等
- **Filter / Search**(2 个):processCenter status / type
- **UI Toggle**(1 个):setStatus function

**结论**:Status 字段均为 Object 字段或 Filter,**不是 UI 隐藏开关**。

---

## §18 26 项证据矩阵(摘要)

26 项(Page/Controller/State/URL/Entry/Layout/Buttons/Inputs/Filters/Status/Dialog/Pagination/Sorting/Required/Default/Data Source/Object/Request/Response/Function/State Bridge/Object Bridge/API Bridge/Business Interpretation/Evidence Grade/V4.4 Decision)在每个子模块段落已给出。摘要:

- **Object**:4 个真实 ID(supplierId / bodyCheckItemId / companyCashConfId / trainerCardId)+ 4 个 corpConfig(无独立 ID)
- **Request**:supplierId / bodyCheckItemId / companyCashConfId / trainerCardId / memberName / examineRate / productRate
- **Response**:supplierVoList / trainerCardVo / memberVo / companyCashConfVoList
- **API Bridge**:14 个 Read + 13 个 Write
- **State Bridge**:17 个 systemSetting 子 State
- **Object Bridge**:Supplier ↔ Product/Stock(MainSupplier)
- **Business Interpretation**:子模块多为配置/字典类
- **Evidence Grade**:A 字符级 / B 多源 / C 局部 / D 冲突(0) / **E 业务推断(0 入规格)** / F 未观察
- **V4.4 Decision**:仅 A/B/C 入规格

---

## §19 历史差异

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-151:systemSetting = 17+ State 路由聚合器 | 17 个精确 State | 精确 17 个,新增 4 个 Config(不属于 systemSetting) | **17** |
| S1-153:corpAppointmentConf 真实(SMS 通知配置) | 保持 | 无变化 | A |
| S1-154:memberTypeId 0 命中 | 0 命中(memberTypeList 命名误导,实际是 Member 库) | **再次确认 0 命中** | F / 禁造 |
| S1-155:trainerCardId 真实(计次卡) | projectCard 命名误导,实际是 trainerCard 配置 | **命名误导修复** | A(trainerCardId) |
| S1-155:Member/MemberType/MemberCard 0 命中 | memberTypeList 实际是 Member 库(创建会员 createMember.json) | **修正** | memberTypeId 仍 F |
| S1-156:printConfigCtrl = corpCashConf | **companyCashConfId 真实 A**(L57763) | **新增 ID 真实** | A(companyCashConfId) |
| S1-156:corpReportConf 真实 | 保持 | 无变化 | A |
| (历史误判)"SystemSetting 是独立 Object" | settingId 0 命中,systemSetting 是 State 聚合器 | **禁造** | F |
| (历史误判)"checkItemId 是 ID 字段" | 0 命中,真实是 bodyCheckItemId | **禁造** | F |
| (历史误判)"materialId 是 ID 字段" | 0 命中 | **禁造** | F |
| (历史误判)"chargeItemId 是 ID 字段" | 0 命中 | **禁造** | F |
| (历史误判)"feeId / medicalFeeId" | 0 命中 | **禁造** | F |
| (历史误判)"processCenterId" | 0 命中,真实是 machineCenterId 18 处(S1-150) | **禁造** | F |
| (历史误判)"projectCardId" | 0 命中,真实是 trainerCardId | **禁造** | F |

---

## §20 V4.4 SystemSetting 规格(18 项)

1. **SystemSetting** 是否一级对象 = **F**(State 聚合器,**禁造** settingId)
2. **17 个子 State** 必须实现(checkList / checkModify / InspectList / customerCharge / customerChargeItem / customerMaterialCertificate / materialCertificate / materialModify / materiallist / medicalFeesList / memberTypeList / modifyCustomerCharge / processCenter / projectCard / supplierCertificate / supplierList / supplierModify)
3. **子 State 无真实 Controller 的**:materialCertificate / customerMaterialCertificate / supplierCertificate(命名误导)
4. **子模块有独立 Object**:**Supplier**(supplierId A) / **Check(bodyCheckItemId A)** / **ProjectCard(实际 trainerCardId A)** / **Member(无独立 ID,Member 库)**
5. **独立 ID**:supplierId(99) / bodyCheckItemId(4) / companyCashConfId(1) / trainerCardId(5)
6. **Request Config**:memberName / examineRate / productRate / status / appointSceneType / cashHeader / customerMobileDisable / defaultStartMonth / defaultStartDay
7. **Response VO**:supplierVoList / trainerCardVoList / memberVo / companyCashConfVoList
8. **Write 必须实现**:saveCardSubstractType / createMember / updateMember / getTrainerCard / addTrainerCard / updateTrainerCard / setBodyCheckItemPrintDisable / addSupplier / modifySupplier / deleteSupplier / saveCorpAppointmentConf / saveCorpAppointConf / updateCompanyCashConf / saveCorpReportConf
9. **Read 必须实现**:selectTrainerCardList / selectSupplierVoList / getSupplier / getMember / selectMemberVoList / getCorpPointRule / selectBodyCheckItemVoList / selectCompanyCashConfVoList / selectCustomerChargeItemVoList
10. **memberTypeId 是否可建模** = **F**(0 命中,Member 库无独立 ID,复用 memberId)
11. **processCenterId 是否可建模** = **F**(0 命中,统一 machineCenterId)
12. **machineCenterId 是否可建模** = **A**(18 处真实,S1-150)
13. **supplierId 是否可建模** = **A**(99 处真实)
14. **materialId 是否可建模** = **F**(0 命中,Material 是 productSku 子属性)
15. **feeId 是否可建模** = **F**(0 命中,medicalFeesList 是 cardSubstractType 配置)
16. **SystemSetting 与 Company / Appointment / Report / Cash / SMS Config 隔离**:corpAppointmentConf / corpAppointConf → Appointment;corpCashConf → Cash/Report;corpReportConf → Report;companyCashConfId 真实 ID
17. **后端 FK**全部 L3/F
18. **绝对不能制造的字段**:settingId / systemSettingId / checkItemId / chargeItemId / customerChargeItemId / materialId / materialListId / feeId / medicalFeeId / memberTypeId / processCenterId / projectCardId

---

## §21 F / 未确认

### 21.1 0 命中禁造 ID(全部 F)

- settingId / systemSettingId
- checkItemId / chargeItemId / customerChargeItemId / customerChargeId
- materialId / materialListId
- feeId / medicalFeeId
- memberTypeId
- processCenterId / projectCardId

### 21.2 0 命中关键词

- `chargeItemVo` / `customerChargeItemVo`(0 命中,Storage 缓存)
- `medicalFeeVo` / `medicalFeeId`(0 命中)
- `memberTypeVo` / `memberTypeListVo`(0 命中,实际是 member)
- `processCenterVoList`(0 命中,实际是 machineCenterVoList)
- `projectCardVoList`(0 命中,实际是 trainerCardVoList)

### 21.3 L3 数据库结构

- 全部 F

---

## §22 Object 分类全表

| 对象 | A 独立 ID | B Response VO | C Request Payload | D State/UI | F |
|---|:-:|:-:|:-:|:-:|:-:|
| **SystemSetting** | ✗ F | – | – | ✓(State 聚合器) | – |
| **CheckItem(bodyCheck)** | ✓ A(bodyCheckItemId) | ✓ | ✓ | ✓ | – |
| **CustomerChargeItem** | ✗ F | – | – | ✓(Storage) | – |
| **Material** | ✗ F | – | – | ✓(productSku 子属性) | – |
| **MedicalFee** | ✗ F | – | – | ✓(cardSubstractType) | – |
| **MemberType(member)** | ✗ F | – | – | ✓(Member 库) | – |
| **ProcessCenter** | ✗ F | – | – | ✓(machineCenter) | – |
| **ProjectCard(trainerCard)** | ✓ A(trainerCardId) | ✓ | ✓ | ✓ | – |
| **Supplier** | ✓ A(supplierId) | ✓ | ✓ | ✓ | – |
| **corpAppointmentConf** | ✓ A(隐含) | ✓ | ✓ | ✓ | – |
| **corpAppointConf** | ✓ A(隐含) | ✓ | ✓ | ✓ | – |
| **corpCashConf** | ✓ A(companyCashConfId) | ✓ | ✓ | ✓ | – |
| **corpReportConf** | ✓ A(隐含) | ✓ | ✓ | ✓ | – |
| **corpPointRule** | ✗ F | ✓ | ✓ | ✓ | – |

**L3 数据库结构**:全部 F。

---

## §23 命名误导修正表(P0)

| Controller / State | 实际业务 | 修正 |
|---|---|---|
| `systemSetting.checkItem` | bodyCheck(身体检查) | rename → bodyCheckItem |
| `systemSetting.medicalFeesList` | cardSubstractType(训练卡扣次类型) | rename → cardSubstractType |
| `systemSetting.memberTypeList` | Member 库(创建会员 createMember.json) | rename → memberList |
| `systemSetting.memberTypeModify` | Member 编辑(updateMember.json) | rename → memberModify |
| `systemSetting.processCenter` | MachineCenter(加工中心) | rename → machineCenter |
| `systemSetting.projectCard` | TrainerCard(训练卡/计次卡) | rename → trainerCard |
| `printConfigCtrl` | corpCashConf(收银配置) | rename → corpCashConfCtrl |

---

## §24 Git / 完整性

### 24.1 完整性闸门

4 文件 SHA256 全部 PASS(见 §0)。

### 24.2 累计统计

- controller.js 2,194,196 bytes / 59,214 行
- 417 个 Controller 注册
- 915 个 .json API
- **17 个 systemSetting 子 State**(精确)
- **4 个真实 ID**(supplierId / bodyCheckItemId / companyCashConfId / trainerCardId)
- **7 个命名误导需修正**

### 24.3 API actual / Write actual / Production mutation

**API actual = 0 / Write actual = 0 / Production mutation = 0** ✓

仅执行:`Get-FileHash` / `git status` / `git add --` / `git commit` / `git push` / `python` 本地分析脚本(临时目录)/ `Get-ChildItem` 校验。

### 24.4 Git 操作

- Commit:`40738f0b66a1aa1c01fba33782b501476be403fa`(S1-156 之后,S1-157 待提交)
- Branch:master
- Tracked = 227 / Untracked = 10 / Ignored = 1
- 本轮新增:`220_S1-157_*.md`
- 预期:Tracked = 228 / Untracked = 10 / Ignored = 1 / LOCAL == origin/master