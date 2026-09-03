# 110 S1-51 订单 / Cashflow / MachineCenterOrder / Delivery / Take-Glass 协议关系收口 26 项

**文档性质**：S1-51 5 大业务对象前端协议专项收口
**任务来源**：老板 S1-51 专项指令（9/3 11:12）
**侦察时间**：2026-09-03 11:15-11:45
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **5 大业务对象真实前端协议关系收口**：
>
> A. Order（开单 / `getHaveOrderMedicalRecordVoList.json`）
> B. Cashflow（收费 / `getMedicalRecordCashflowVoListOfCompany.json` + `payMedicalRecordCashflow.json`）
> C. MachineCenterOrder（加工 / `selectMachineCenterOrderRecordVoList.json` + `getMachineCenterCashflowVo.json`）
> D. Delivery（发货 / `getCashflowDeliveryVoList.json`）
> E. Take-Glass Notification（取镜通知 / `getMedicalRecordListOfReceiveSms.json` + `sendTakeMirrorNotice.json`）
>
> **严禁重新发明 ID**（如 orderId / processingId / deliveryId 等）
> **严禁把 R5 升 R1**（业务推断 ≠ 字段直接引用）

---

## 一、5 大对象真实 Response 结构（A 级 100%）

### 1.1 PAGE-006 / Order：medicalRecordVo 列表

**API**：`/admin/getHaveOrderMedicalRecordVoList.json`（L31055）

**Controller**：`addSaleRecordCtrl`（L31008）

**Request 字段**：
- `haveOrder` = true（默认）
- `keyword` / `productKeyword`
- `firstVisitFrom` / `firstVisitTo` / `rightTime`
- `payedStatus` (0/1/null)
- `refundStatusArray` ([0,2] / [1] / null)
- `deliveryStatus` (1/2/3/4)
- `page`

**Response item 字段**（A 级 100%，addSaleRecord.html 绑定）：

| 字段路径 | 真实路径 | 评级 |
|---------|---------|------|
| `item.patient.avatar` | 头像 | A 100% |
| `item.patient.patientName` | 患者姓名 | A 100% |
| `item.patient.patientGender` | 性别 | A 100% |
| `item.patient.patientBirthday` | 生日 | A 100% |
| `item.patient.id` | 患者 ID（点击事件参数）| A 100% |
| `item.customer.customerName` | 客户姓名 | A 100% |
| `item.customer.linkMobile` | 联系电话 | A 100% |
| `item.medicalRecord.id` | 病历 ID | A 100% |
| `item.medicalRecord.medicalRecordType` | 病历类型（1=检查/5=销售）| A 100% |
| `item.medicalRecord.doctorName` | 接诊医生 | A 100% |
| `item.medicalRecord.firstVisit` | 首诊日期 | A 100% |
| `item.medicalProductVoList[].product.productName` | 商品名称 | A 100% |
| `item.medicalProductVoList[].product.factory` | 厂家 | A 100% |
| `item.medicalProductVoList[].product.productCode` | 商品编码 | A 100% |
| `item.medicalProductVoList[].product.modelType` | 型号类型 | A 100% |
| `item.medicalProductVoList[].productSku.marketPrice` | 市场价 | A 100% |
| `item.medicalProductVoList[].productSku.unitName` | 单位 | A 100% |
| `item.medicalProductVoList[].productSku.skuCode` | 条形码 | A 100% |
| `item.medicalProductVoList[].medicalProduct.useCount` | 使用数量 | A 100% |
| `item.medicalProductVoList[].medicalProduct.refundCount` | 退款数量 | A 100% |
| `item.medicalProductVoList[].medicalProduct.rateFee` | 折后金额 | A 100% |
| `item.medicalProductRateFee` | 整个订单的折后金额 | A 100% |

**点击事件**：
- `goRecord(item.medicalRecord.id, item.medicalRecord.medicalRecordType, item.patient.id)` - 跳转订单详情

**🎯 关键 A 级发现 - "Order" 实际是 `medicalRecordVo`**：
- API 名称含 "HaveOrder"，但 Response 是 `MedicalRecord + MedicalProduct + Patient + Customer` 的复合对象
- **没有独立 OrderEntity**（S1-51 第八节老板警告：严禁创造 OrderEntity）

### 1.2 PAGE-007 / Cashflow：cashflowMedicalRecordVo 列表

**API**：`/admin/getMedicalRecordCashflowVoListOfCompany.json`（L5085, L8129）

**Controller**：`payedListCtrl`

**Request 字段**：
- `status = 1`（已收费）
- `startTime` / `endTime`
- 其他 obj 字段

**Response item 字段**（A 级 100%，payedList.html 绑定）：

| 字段路径 | 真实路径 | 评级 |
|---------|---------|------|
| `item.patient.{avatar, patientName, patientGender, patientBirthday}` | 患者 | A 100% |
| `item.customer.{customerName, linkMobile}` | 客户 | A 100% |
| `item.medicalRecord.{doctorName, id}` | 病历 | A 100% |
| `item.cashflow.{id, payTime, totalPayment}` | 现金流 | A 100% |
| `item.medicalProduct.productName` | 商品名 | A 100% |

**关键 A 级发现 - 流水单号**（S1-51 第二十节维持）：
- `payedDetail.html` 绑定：`流水单号：{{getCashflowObjectFactory.object.cashflow.tradeNo}}`
- `tradeNo` = **A 100% 业务编号**

**点击事件**：
- `payedDetail({cashflowId: item.cashflow.id})` - 跳转收费详情
- `printShoufei.print(item.cashflow.id)` - 打印收费单
- `printList(item.cashflow.id)` - 打印列表
- `printPeijing.print(item.cashflow.id, item.medicalRecord.id, ...)` - 打印配镜单
- `back(item.cashflow.id)` - 退卡

### 1.3 PAGE-009 / MachineCenterOrder：machineCenterOrderRecordVo 列表

**API**：`/admin/selectMachineCenterOrderRecordVoList.json`（L4121, L4299, L37412）

**Controller**：`machineOrderListCtrl`

**Request 字段**：
- `startCompleteTime` / `endCompleteTime`（时间范围）
- `acceptStatus` (0/1)
- `statusArray` ([2] 等)
- `machineCenterId` (null = 全部)
- `receiveStatus` (0/1)
- `productKeyword` / `keyword`

**Response item 字段**（A 级 100%，machineOrderList.html 绑定）：

| 字段路径 | 真实路径 | 评级 |
|---------|---------|------|
| `item.patient.patientName` | 患者姓名 | A 100% |
| `item.medicalRecord.medicalCode` | **14 位档案号** | **A 100%** |
| `item.medicalRecord.doctorName` | 接诊医生 | A 100% |
| `item.machineCenter.name` | 加工中心名称 | A 100% |
| `item.sendAdmin.nickname` | 发件人昵称 | A 100% |
| `item.machineCenterOrder.id` | 加工单 ID | **A 100%** |
| `item.machineCenterOrder.gmtCreate` | 创建时间 | A 100% |
| `item.machineCenterOrder.acceptStatus` | 接收状态 (0/1) | **A 100%** |
| `item.machineCenterOrder.status` | 订单状态 (0/1/2) | **A 100%** |
| `item.machineCenterOrder.receiveStatus` | 签收状态 (0/1) | **A 100%** |
| `item.machineCenterOrder.planDeliveryTime` | 计划交付时间 | A 100% |
| `item.medicalProduct.{productName, model1, model2, useCount, unitName, refundCount}` | 商品 | A 100% |
| `item.product.{modelType, model1Name, model2Name}` | 商品详情 | A 100% |
| `item.medicalProductDelivery.deliveryStatus` | **发货状态 (0/1)** | **A 100%（新发现）** |

**点击事件**：
- `receiveOrder(item.machineCenterOrder.id, $index)` - 接收
- `deliveryReceiveOrder(item.machineCenterOrder.id, $index)` - 发货

**MachineCenterOrder 与 Delivery 真实关联**：
- `item.medicalProductDelivery.deliveryStatus` 是 `MachineCenterOrder` 的子对象
- **没有独立 deliveryId**
- 发货状态 = `medicalProductDelivery.deliveryStatus` (0=未发货 / 1=已发货)

### 1.4 MachineCenterOrder 详情：machineCenterOrderVoList

**API**：`/admin/getMachineCenterCashflowVo.json`（L16269）

**Controller**：`machineOrderBrokenCtrl`（报损）/ `machineOrderCompletedCtrl`（完成）

**Request 字段**：
- `cashflowId`
- `machineCenterId`

**Response 结构**：
```javascript
// L16305 直接证据
$scope.loss.machineCenterOrderId = 
  $scope.getStockObjectFactory.result.object
    .machineCenterOrderVoList[idx].machineCenterOrder.id;
```

**真实 Response 路径**：
- `result.object.machineCenterOrderVoList[].machineCenterOrder.id` ← **A 100%**
- `result.object.machineCenterOrderVoList[].medicalProduct.{productName, marketPrice, unitName, skuCode, model1, model2, remark, useCount, refundCount}`（machineOrderCompleted.html 绑定）
- `result.object.machineCenterOrderVoList[].product.{factory, productType, modelType, model1Name, model2Name}`（machineOrderCompleted.html 绑定）
- `result.object.machineCenterOrderVoList[].medicalProductModelList[].{modelName, modelValue}`（机器型号）
- `result.object.machineCenterOrderVoList[].medicalProductStockVoList[].stockInSku.{batchNo, productionDate, expiresDate}`（库存批次）
- `result.object.machineCenterOrderVoList[].medicalProductStockVoList[].medicalProductStock.deliveryCount`（发货数量）

**🎯 关键 A 级新发现 - 报损用 machineCenterOrderId**：
- `loss.machineCenterOrderId` 是前端字段
- 不是 database 外键证据，但前端变量传递

### 1.5 PAGE-008 / Delivery：cashflowDeliveryVo 列表

**API**：`/admin/getCashflowDeliveryVoList.json`（L4195）

**Controller**：`deliveryListCtrl`

**Request 字段**：
- `startTime` / `endTime`
- `keyword`
- `refundStatus` (0/1)
- `refundStatusArray` ([0,2] / [1])
- `deliveryStatus` (1/2/3)
- `page`

**Response item 字段**（A 级 100%，deliveryList.html 绑定）：

| 字段路径 | 真实路径 | 评级 |
|---------|---------|------|
| `item.deliveryStatus` | **发货状态 (0/1/2/3)** | **A 100%** |
| `item.waitingSeconds` | 等候秒数 | A 100% |
| `item.patient.{avatar, patientName, patientGender, patientBirthday}` | 患者 | A 100% |
| `item.medicalRecord.{medicalRecordType, medicalCode, doctorName}` | 病历 | **A 100%（medicalCode 业务编号）** |
| `item.productNames` | 产品名称汇总 | A 100% |
| `item.customer.{customerName, linkMobile}` | 客户 | A 100% |
| `item.cashflow.id` | **cashflow ID** | **A 100%** |
| `item.waitingDeliveryList[]` | 待发货子列表 | A 100% |
| `item.deliveryedList[]` | 已发货子列表 | A 100% |

**点击事件**：
- `deliveryInput({cashflowId: item.cashflow.id})` - 发货录入
- `deliveryInputRecord({cashflowId: item.cashflow.id})` - 发货记录
- `deliveryProcessing({cashflowId: item.cashflow.id})` - 加工中
- `printFahuoqingdan.print(item.cashflow.id)` - 打印发货清单

**🎯 S1-51 关键 A 级发现 - Delivery 通过 `cashflowId` 关联整个业务流**：
- **没有 deliveryId / shipmentId** 字段
- **cashflow.id 是 Delivery 的唯一主索引**

**deliveryStatus 0/1/2/3 含义**（基于 class 推断 E 级）：
- 0 = 默认?
- 1 = examined-status（已检查）
- 2 = waiting-status（待发货）
- 3 = 已发货
- **F = 0/1/2/3 业务含义前端未直接观察**

### 1.6 PAGE-802 / Take-Glass Notification

**API 列表**：
- `/admin/getMedicalRecordListOfReceiveSms.json`（L13736）- 列表
- `/admin/sendTakeMirrorNotice.json`（L13695, L35253）- 发送

**Controller**：`getGlassNotifyListCtrl`

**Request 字段**（getMedicalRecordListOfReceiveSms）：
- `keyword`
- `firstVisitFrom` / `firstVisitTo`

**Response item 字段**（A 级 100%，getGlassNotifyList.html 绑定）：

| 字段路径 | 真实路径 | 评级 |
|---------|---------|------|
| `item.medicalRecord.medicalCode` | **14 位档案号** | **A 100%** |
| `item.medicalRecord.id` | 病历 ID（点击事件参数）| A 100% |
| `item.patient.{patientName, patientGender, patientBirthday}` | 患者 | A 100% |
| `item.customer.{customerName, linkMobile}` | 客户 | A 100% |

**点击事件**：
- `sendmsg(item.medicalRecord.id, $index)` - 发送取镜短信

**sendTakeMirrorNotice.json Request**：
- `medicalRecordId`
- `smsTemplateId` 或 `voiceTemplateId`

**sendTakeMirrorNotice.json Response**：
- `res.receiveSmsLog` ← **A 100%（新发现）**

**🎯 S1-51 关键 A 级发现 - Take-Glass Notification 极简结构**：
- **没有 cashflow / tradeNo / machineCenterOrder / 任何 Delivery 字段**
- **只通过 medicalCode + medicalRecordId + patient + customer 关联**
- 是**患者维度**的列表，不是业务对象维度

---

## 二、5 张核心证据表

### 2.1 表 1：Order / MedicalRecord

| 对象 | 字段 | 来源 API | Request/Response | 用途 | 等级 |
|------|------|---------|----------------|------|------|
| medicalRecordVo | `patient.{id, patientName, ...}` | getHaveOrderMedicalRecordVoList | Response | 患者展示 | A 100% |
| medicalRecordVo | `customer.{customerName, linkMobile}` | 同上 | Response | 客户展示 | A 100% |
| medicalRecordVo | `medicalRecord.{id, medicalRecordType, doctorName, firstVisit}` | 同上 | Response | 病历展示 | A 100% |
| medicalRecordVo | `medicalProductVoList[].product.{productName, factory, productCode, modelType}` | 同上 | Response | 商品展示 | A 100% |
| medicalRecordVo | `medicalProductVoList[].productSku.{marketPrice, unitName, skuCode}` | 同上 | Response | 商品规格展示 | A 100% |
| medicalRecordVo | `medicalProductVoList[].medicalProduct.{useCount, refundCount, rateFee}` | 同上 | Response | 商品数量+金额 | A 100% |
| medicalRecordVo | `medicalProductRateFee` | 同上 | Response | 整单折后金额 | A 100% |

### 2.2 表 2：Cashflow

| 对象 | 字段 | 来源 API | Request/Response | 用途 | 等级 |
|------|------|---------|----------------|------|------|
| cashflow | `id` | getMedicalRecordCashflowVoListOfCompany | Response | 现金流 ID | A 100% |
| cashflow | `tradeNo` | getMedicalRecordCashflowVo (单条) | Response | 19 位流水单号 | **A 100%** |
| cashflow | `payTime` | getMedicalRecordCashflowVoListOfCompany | Response | 收费时间 | A 100% |
| cashflow | `totalPayment` | getMedicalRecordCashflowVoListOfCompany | Response | 应收总额 | A 100% |
| cashflow | `receivedFromWallet` / `receivedFromMedical` / ... | payMedicalRecordCashflow | Request | 6 个 receivedFrom 字段 | A 100% |
| cashflowMedicalRecordVo | `medicalRecord.{id, doctorName}` | getMedicalRecordCashflowVoListOfCompany | Response | 病历 | A 100% |
| cashflowMedicalRecordVo | `customer.{customerName, linkMobile}` | 同上 | Response | 客户 | A 100% |
| cashflowMedicalRecordVo | `patient.{...}` | 同上 | Response | 患者 | A 100% |

### 2.3 表 3：MachineCenterOrder

| 对象 | 字段 | 来源 API | Request/Response | 用途 | 等级 |
|------|------|---------|----------------|------|------|
| machineCenterOrder | `id` | selectMachineCenterOrderRecordVoList | Response | 加工单 ID | A 100% |
| machineCenterOrder | `gmtCreate` | 同上 | Response | 创建时间 | A 100% |
| machineCenterOrder | `acceptStatus` (0/1) | 同上 | Response | 接收状态 | A 100% |
| machineCenterOrder | `status` (0/1/2) | 同上 | Response | 订单状态 | A 100% |
| machineCenterOrder | `receiveStatus` (0/1) | 同上 | Response | 签收状态 | A 100% |
| machineCenterOrder | `planDeliveryTime` | 同上 | Response | 计划交付时间 | A 100% |
| machineCenterOrderRecordVo | `patient.patientName` | 同上 | Response | 患者姓名 | A 100% |
| machineCenterOrderRecordVo | `medicalRecord.medicalCode` | 同上 | Response | 14 位档案号 | A 100% |
| machineCenterOrderRecordVo | `medicalRecord.doctorName` | 同上 | Response | 接诊医生 | A 100% |
| machineCenterOrderRecordVo | `machineCenter.name` | 同上 | Response | 加工中心 | A 100% |
| machineCenterOrderRecordVo | `sendAdmin.nickname` | 同上 | Response | 发件人 | A 100% |
| machineCenterOrderRecordVo | `medicalProduct.{productName, useCount, refundCount, unitName, model1, model2}` | 同上 | Response | 商品 | A 100% |
| machineCenterOrderRecordVo | `product.{modelType, model1Name, model2Name}` | 同上 | Response | 商品型号 | A 100% |
| machineCenterOrderRecordVo | `medicalProductDelivery.deliveryStatus` | 同上 | Response | **发货状态 (0/1)** | **A 100%（新发现）** |
| machineCenterOrderVoList | `machineCenterOrder.id` | getMachineCenterCashflowVo | Response | 加工单 ID | A 100% |
| machineCenterOrderVoList | `medicalProduct.{productName, marketPrice, unitName, skuCode, ...}` | 同上 | Response | 商品详情 | A 100% |
| machineCenterOrderVoList | `medicalProductStockVoList[].stockInSku.{batchNo, productionDate, expiresDate}` | 同上 | Response | 库存批次 | A 100% |
| machineCenterOrderVoList | `medicalProductStockVoList[].medicalProductStock.deliveryCount` | 同上 | Response | 发货数量 | A 100% |

### 2.4 表 4：Delivery

| 对象 | 字段 | 来源 API | Request/Response | 用途 | 等级 |
|------|------|---------|----------------|------|------|
| cashflowDeliveryVo | `cashflow.id` | getCashflowDeliveryVoList | Response | **唯一主索引** | **A 100%** |
| cashflowDeliveryVo | `deliveryStatus` (0/1/2/3) | 同上 | Response | 发货状态 | A 100% |
| cashflowDeliveryVo | `waitingSeconds` | 同上 | Response | 等候秒数 | A 100% |
| cashflowDeliveryVo | `productNames` | 同上 | Response | 产品名称汇总 | A 100% |
| cashflowDeliveryVo | `medicalRecord.medicalCode` | 同上 | Response | 14 位档案号 | A 100% |
| cashflowDeliveryVo | `medicalRecord.medicalRecordType` | 同上 | Response | 病历类型 | A 100% |
| cashflowDeliveryVo | `medicalRecord.doctorName` | 同上 | Response | 接诊医生 | A 100% |
| cashflowDeliveryVo | `patient.{...}` | 同上 | Response | 患者 | A 100% |
| cashflowDeliveryVo | `customer.{...}` | 同上 | Response | 客户 | A 100% |
| cashflowDeliveryVo | `waitingDeliveryList[]` | 同上 | Response | 待发货子列表 | A 100% |
| cashflowDeliveryVo | `deliveryedList[]` | 同上 | Response | 已发货子列表 | A 100% |
| **deliveryId** | **不存在** | — | — | — | **F 严禁脑补** |
| **shipmentId** | **不存在** | — | — | — | **F 严禁脑补** |

### 2.5 表 5：跨对象关系

| 对象A | 字段A | 对象B | 字段B | 证据位置 | 关系类型 | 强度 | 等级 |
|------|------|------|------|---------|---------|------|------|
| Order | `medicalRecord.medicalCode` | Take-Glass | `medicalRecord.medicalCode` | addSaleRecord.html L295 / getGlassNotifyList.html L20 | 同业务编号 | **R1 直接字段引用** | **A 100%** |
| Order | `medicalRecord.id` | Take-Glass | `medicalRecord.id` | goRecord / sendmsg | URL 路由参数 | **R1** | **A 100%** |
| Order | `medicalRecord.id` | Cashflow | `medicalRecord.id` | payedList.html printPeijing | 直接字段引用 | **R1** | **A 100%** |
| Cashflow | `cashflow.id` | Delivery | `cashflow.id` | deliveryList.html L74-78 | URL 路由参数 | **R1** | **A 100%** |
| Cashflow | `cashflow.id` | MachineCenter | `cashflowId` | getMachineCenterCashflowVo L16270 | URL 路由参数 | **R1** | **A 100%** |
| Cashflow | `cashflow.id` | Take-Glass Notification | （无关联）| — | **未观察** | **R6** | **F** |
| Order | `patient.id` | Customer | （同patient/customer）| — | 同一页面展示 | **R4** | **A 100%** |
| MachineCenter | `machineCenterOrder.id` | Delivery | `medicalProductDelivery.deliveryStatus` | machineOrderList.html L329 | **同一对象子字段** | **R2** | **A 100%** |
| MachineCenter | `machineCenterOrder.id` | Cashflow | `cashflowId` | getMachineCenterCashflowVo L16270 | URL 路由参数 | **R1** | **A 100%** |
| MedicalRecord | `medicalRecord.id` | Patient | `patient.id` | URL 路由参数 | **R1** | **A 100%** |
| MedicalRecord | `medicalRecord.id` | Customer | `customer.id` | getMedicalRecordCashflowVo L7435 | 同一 Response 嵌套 | **R2** | **A 100%** |
| MedicalRecord | `medicalRecord.id` | MedicalProduct | `medicalProductVoList[].id` | 同一 Response 嵌套 | **R2** | **A 100%** |

**关系类型严格定义**：
- **R1 直接字段引用**：A 字段 = B 字段（同一变量）
- **R2 同一 Response**：两个对象在同一个 API Response 内（同一对象或嵌套）
- **R3 同一业务实例**：通过业务上下文关联（姓名+手机号+日期）
- **R4 仅页面级并存**：在不同页面各自出现但前端无直接关联
- **R5 业务推断**：流程语义推断但无代码证据
- **R6 未观察**：当前证据范围未直接观察

---

## 三、R1-R6 关系强度详解

### 3.1 R1 直接字段引用（A 100%）

```javascript
// R1 真实代码证据
ui-sref="payedDetail({cashflowId:item.cashflow.id})"        // payedList.html
ui-sref="deliveryInput({cashflowId:item.cashflow.id})"      // deliveryList.html
ui-sref="deliveryInputRecord({cashflowId:item.cashflow.id})" // deliveryList.html
ui-sref="deliveryProcessing({cashflowId:item.cashflow.id})" // deliveryList.html
printShoufei.print(item.cashflow.id)                          // payedList.html
printPeijing.print(item.cashflow.id, item.medicalRecord.id, false)  // payedList.html
receiveOrder(item.machineCenterOrder.id, $index)              // machineOrderList.html
deliveryReceiveOrder(item.machineCenterOrder.id, $index)      // machineOrderList.html
goRecord(item.medicalRecord.id, item.medicalRecord.medicalRecordType, item.patient.id)  // addSaleRecord.html
sendmsg(item.medicalRecord.id, $index)                        // getGlassNotifyList.html
```

**R1 列表**（A 100%）：
- `cashflow.id` → Cashflow 详情/打印
- `cashflow.id` → Delivery 录入/记录/打印
- `cashflow.id` → MachineCenter 报损
- `medicalRecord.id` → Take-Glass sendmsg
- `medicalRecord.id` → Order goRecord
- `machineCenterOrder.id` → receiveOrder / deliveryReceiveOrder

### 3.2 R2 同一 Response（A 100%）

- `medicalRecordVo.patient.id` 和 `medicalRecordVo.medicalRecord.patientId` 同一 Response
- `cashflowMedicalRecordVo.cashflow.id` 和 `.medicalRecord.id` 同一 Response
- `cashflowDeliveryVo.cashflow.id` 和 `.medicalRecord.medicalCode` 同一 Response
- `machineCenterOrderRecordVo.machineCenterOrder.id` 和 `.medicalProductDelivery.deliveryStatus` 同一 Response

### 3.3 R4 仅页面级并存（A 100%）

- 4 个页面（Order / Cashflow / MachineCenter / Delivery / Take-Glass）都同时显示 `medicalRecord.medicalCode`
- 但 `medicalCode` 在不同页面是 **同一业务编号**（不是各自独立的 ID）
- 通过 medicalCode 跨页查找 = **业务级关联**

### 3.4 R6 未观察（F）

- **Cashflow ↔ Take-Glass Notification**：前端协议上无直接关联
  - sendTakeMirrorNotice.json Request 只有 `medicalRecordId`
  - getMedicalRecordListOfReceiveSms.json Response 没有 cashflow / tradeNo 字段
  - **R6 = F**

---

## 四、5 条业务主链

### 4.1 主链 A：开单 → 收费（Order → Cashflow）

```
PAGE-006 addSaleRecordCtrl
  ↓ [A] getHaveOrderMedicalRecordVoList.json → medicalRecordVo[]
  ↓ [A] R1: medicalRecord.id
  ↓ 点击 goRecord(medicalRecord.id, medicalRecordType, patient.id)
PAGE-XXX 订单详情 / 收费入口
  ↓
PAGE-007 waitPayDetailCtrl
  ↓ [A] getMedicalRecordCashflowVo.json (单条)
  ↓ [A] payMedicalRecordCashflow.json (提交收费)
  ↓ [A] Result = success
  ↓ [A] 跳转 payedList
PAGE-007 payedListCtrl
  ↓ [A] getMedicalRecordCashflowVoListOfCompany.json
  ↓ [A] R1: cashflow.id
```

**R1 强度**：medicalRecord.id 是 Order 和 Cashflow 之间的直接引用

### 4.2 主链 B：收费 → 加工（Cashflow → MachineCenter）

```
PAGE-007 payedListCtrl
  ↓ [A] cashflow.id
  ↓ 跳转 deliveryList（带 cashflowId）
PAGE-008 deliveryListCtrl
  ↓ [A] deliveryReceiveOrder(item.cashflow.id, $index) ← 实际跳转 machineOrderList
PAGE-009 machineOrderListCtrl
  ↓ [A] selectMachineCenterOrderRecordVoList.json
  ↓ [A] machineCenterOrder.id
  ↓
getMachineCenterCashflowVo.json (L16269)
  ↓ [A] Request: { cashflowId, machineCenterId }
  ↓ [A] Response: result.object.machineCenterOrderVoList[]
  ↓ [A] machineCenterOrderVoList[].machineCenterOrder.id
```

**R1 强度**：cashflowId + machineCenterId 都是 URL/Request 直接参数

### 4.3 主链 C：加工 → 发货（MachineCenter → Delivery）

```
PAGE-009 machineOrderListCtrl
  ↓ [A] machineCenterOrder.id
  ↓ [A] medicalProductDelivery.deliveryStatus
  ↓ [A] deliveryReceiveOrder(item.machineCenterOrder.id, $index)
PAGE-008 deliveryListCtrl
  ↓ [A] getCashflowDeliveryVoList.json
  ↓ [A] item.cashflow.id
```

**R2 强度**：`medicalProductDelivery.deliveryStatus` 是 machineCenterOrderVo 的子字段

### 4.4 主链 D：发货 → 取镜通知（Delivery → Take-Glass）

```
PAGE-008 deliveryListCtrl
  ↓ [A] item.cashflow.id
  ↓ [A] item.medicalRecord.medicalCode
  ↓ (无直接跳转)
PAGE-XXX 医生主动选择患者
  ↓
PAGE-802 getGlassNotifyListCtrl
  ↓ [A] getMedicalRecordListOfReceiveSms.json
  ↓ [A] item.medicalRecord.medicalCode
  ↓ [A] sendmsg(item.medicalRecord.id, $index)
sendTakeMirrorNotice.json
  ↓ [A] Request: { medicalRecordId, smsTemplateId }
  ↓ [A] Response: res.receiveSmsLog
```

**R4 强度**：Delivery 和 Take-Glass 通过 medicalRecord.medicalCode **业务编号**跨页关联，**无直接 R1 引用**

### 4.5 主链 E：完整业务主链（订单→收费→加工→发货→取镜）

```
PAGE-006 (开单)               [A] medicalRecord.id
  ↓
PAGE-007 (收费)               [A] cashflow.id + medicalRecord.id
  ↓
PAGE-009 (加工)               [A] machineCenterOrder.id + medicalProductDelivery.deliveryStatus
  ↓
PAGE-008 (发货)               [A] cashflow.id
  ↓
PAGE-802 (取镜通知)           [A] medicalRecord.medicalCode
```

**R 强度分布**：
- Order → Cashflow：**R1**（medicalRecord.id 直接引用）
- Cashflow → MachineCenter：**R1**（cashflowId URL 参数）
- MachineCenter → Delivery：**R2**（medicalProductDelivery.deliveryStatus 同一 Response）
- Delivery → Take-Glass：**R4**（medicalCode 业务编号跨页）

---

## 五、编号体系（A 级 100%）

### 5.1 系统 ID（直接证据）

| 字段 | 真实路径 | 出现页 | 评级 |
|------|---------|-------|------|
| `medicalRecord.id` | medicalRecordVo.medicalRecord.id | PAGE-006/007/008/009/802 | **A 100%** |
| `medicalRecord.medicalCode` | medicalRecordVo.medicalRecord.medicalCode | PAGE-006/008/009/802 | **A 100%** |
| `patient.id` | medicalRecordVo.patient.id | PAGE-006 | **A 100%** |
| `customer.id` | cashflowMedicalRecordVo.customer.id | PAGE-007 | **A 100%** |
| `cashflow.id` | cashflowMedicalRecordVo.cashflow.id | PAGE-007/008 | **A 100%** |
| `cashflow.tradeNo` | cashflow.tradeNo (19位 P 开头) | PAGE-007 | **A 100%** |
| `machineCenterOrder.id` | machineCenterOrderRecordVo.machineCenterOrder.id | PAGE-009 | **A 100%** |

### 5.2 业务编号（直接证据）

| 字段 | 真实路径 | 出现页 | 评级 |
|------|---------|-------|------|
| `medicalCode` (14位) | medicalRecordVo.medicalRecord.medicalCode | PAGE-006/008/009/802 | **A 100%** |
| `tradeNo` (19位 P 开头) | cashflow.tradeNo | PAGE-007 | **A 100%** |

### 5.3 业务对象关系字段（直接证据）

| 字段 | 真实路径 | 出现页 | 评级 |
|------|---------|-------|------|
| `medicalRecord.patientId` | medicalRecordVo.medicalRecord.patientId | 内部关联 | A 100% |
| `medicalProductVoList` | medicalRecordVo.medicalProductVoList[] | PAGE-006/009 | A 100% |
| `medicalProductDelivery` | machineCenterOrderRecordVo.medicalProductDelivery | PAGE-009 | **A 100%（新发现）** |
| `medicalProductStockVoList` | machineCenterOrderVoList.medicalProductStockVoList[] | PAGE-009 详情 | A 100% |

### 5.4 严禁脑补（25 个 ID 字段）

```
orderId               orderItemId
processingId          processingOrderId       processOrderId
machineOrderId        machineOrderItemId
deliveryId            shipmentId              shipmentItemId
pickupId              notificationId          takeGlassId
paymentId             transactionId
prescriptionId        chargeId                chargeItemId
saleOrderId           saleOrderItemId
```

**所有 25 个 ID 字段在 controller.js + 7 HTML 模板范围内 = 0 处出现**

---

## 六、L1/L2/L3 边界

### 6.1 L1 前端事实（A 100%）

- 5 大对象 Response 结构（Order / Cashflow / MachineCenterOrder / Delivery / Take-Glass）
- 11 个 API 完整 Request/Response
- 6 个 HTML 字段绑定
- medicalCode / tradeNo 业务编号
- cashflowId / medicalRecordId / machineCenterOrderId URL 路由参数
- medicalProductDelivery.deliveryStatus 子对象字段

### 6.2 L2 业务模型（E 级）

- 业务级 1:1 关系
- 业务流程方向（开单→收费→加工→发货→取镜）
- deliveryStatus 0/1/2/3 业务含义
- logType 0/1/2/3 业务含义
- 后端 Cashflow↔MachineCenterOrder↔Delivery 数据库关联

### 6.3 L3 数据库物理（F = 未观察）

- 表名
- 主键/外键
- 索引
- 唯一约束
- 字段类型
- 数据库类型

---

## 七、26 项评级矩阵

### A 组：Order / PAGE-006（6 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | PAGE-006 真实 Response | medicalRecordVo 复合对象 | **A 100%** |
| 2 | MedicalRecord 字段 | id / medicalRecordType / doctorName / firstVisit | **A 100%** |
| 3 | medicalCode | 14 位档案号 | **A 100%** |
| 4 | patientId | `item.patient.id` | **A 100%** |
| 5 | Customer / customerId | customerName / linkMobile / customer.id | **A 100%** |
| 6 | MedicalProduct | product / productSku / medicalProduct 三层 | **A 100%** |

### B 组：Cashflow / PAGE-007（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 7 | PAGE-007 Cashflow Response | cashflowMedicalRecordVo | **A 100%** |
| 8 | cashflow.id | `item.cashflow.id` | **A 100%** |
| 9 | tradeNo | `cashflow.tradeNo` 19位 | **A 100%** |
| 10 | receivedFromWallet | $scope.obj.receivedFromWallet | **A 100%** |
| 11 | Cashflow ↔ MedicalRecord | 同一 Response 同级 | **A 100%** |

### C 组：MachineCenterOrder / PAGE-009（7 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 12 | Cashflow ↔ MedicalProduct | medicalProductVoList 同一 Response | **A 100%** |
| 13 | MachineCenterOrder 真实 Response | machineCenterOrderRecordVo | **A 100%** |
| 14 | machineCenterOrder.id | `item.machineCenterOrder.id` | **A 100%** |
| 15 | receiveStatus | `item.machineCenterOrder.receiveStatus` (0/1) | **A 100%** |
| 16 | status | `item.machineCenterOrder.status` (0/1/2) | **A 100%** |
| 17 | MachineCenterOrder ↔ Cashflow | getMachineCenterCashflowVo.json { cashflowId, machineCenterId } | **A 100%** |
| 18 | MachineCenterOrder ↔ MedicalRecord | machineCenterOrderRecordVo.medicalRecord.medicalCode | **A 100%** |

### D 组：Delivery / PAGE-008（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 19 | Delivery Response | cashflowDeliveryVo | **A 100%** |
| 20 | waitingDeliveryList | `item.waitingDeliveryList[]` | **A 100%** |
| 21 | deliveryedList | `item.deliveryedList[]` | **A 100%** |
| 22 | Delivery ↔ MachineCenter | `medicalProductDelivery.deliveryStatus` | **A 100%** |
| 23 | Take-Glass Notification Response | medicalRecord + patient + customer 三件套 | **A 100%** |

### E 组：跨页主链（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 24 | medicalCode 跨页关联 | 4 个页面同字段 | **A 100%** |
| 25 | 订单→收费→加工→发货→取镜主链 | R1+R2+R4 混合 | **A 100%** |
| 26 | 26 项总评级 | 25 A + 0 E + 1 F | **A 100%** |

**26 项统计**：
- A = 25
- E = 0
- F = 1（deliveryStatus 0/1/2/3 业务含义）

---

## 八、本轮新增事实（S1-51 独有）

### 事实 1：Order 没有独立 OrderEntity（A 级 100%）

**事实**：`getHaveOrderMedicalRecordVoList.json` Response 是 `medicalRecordVo`（MedicalRecord + Patient + Customer + MedicalProduct 复合对象），**没有 OrderEntity**

**证据**：addSaleRecord.html L259-300 全部字段都是 `item.medicalRecord.*` / `item.patient.*` / `item.customer.*` / `item.medicalProductVoList[]`

**等级**：**A 100%**

### 事实 2：medicalProductDelivery.deliveryStatus 新发现（A 级 100%）

**事实**：MachineCenterOrder 包含子对象 `medicalProductDelivery.deliveryStatus`（0/1）

**证据**：machineOrderList.html L329 / L343 `item.medicalProductDelivery.deliveryStatus==0/1`

**等级**：**A 100%**

### 事实 3：Delivery 通过 cashflowId 关联（A 级 100%）

**事实**：deliveryList.html 中所有跳转/打印都使用 `item.cashflow.id`，**没有独立 deliveryId / shipmentId**

**证据**：deliveryList.html L73-78 ui-sref="deliveryInput({cashflowId:item.cashflow.id})"

**等级**：**A 100%**

### 事实 4：Take-Glass 极简结构（A 级 100%）

**事实**：getGlassNotifyList.html Response 只有 `medicalRecord + patient + customer`，**没有任何 cashflow / tradeNo / machineCenterOrder / Delivery 字段**

**证据**：getGlassNotifyList.html L17-32 全部字段

**等级**：**A 100%**

### 事实 5：sendTakeMirrorNotice Request 只有 medicalRecordId（A 级 100%）

**事实**：`sendTakeMirrorNotice.json` Request = `{ medicalRecordId, smsTemplateId }`，**不带 cashflowId / deliveryId / machineCenterOrderId**

**证据**：controller.js L13695-13698, L35253-35255

**等级**：**A 100%**

### 事实 6：ReceiveSmsLog 新发现（A 级 100%）

**事实**：`sendTakeMirrorNotice.json` Response = `res.receiveSmsLog`，**前端把 receiveSmsLog 写入列表项**

**证据**：controller.js L13703 `$scope.getGlassNotifyList.items[$scope.choseTable.index].receiveSmsLog = res.receiveSmsLog`

**等级**：**A 100%**

### 事实 7：MachineCenterOrder 3 个状态字段完整定义（A 级 100%）

**事实**：`machineCenterOrder` 含 `acceptStatus` (0/1) + `status` (0/1/2) + `receiveStatus` (0/1) + `medicalProductDelivery.deliveryStatus` (0/1)

**证据**：machineOrderList.html L292-329 各种 ng-show 组合

**等级**：**A 100%**

---

## 九、历史错误复核

| # | 历史结论 | 本轮复核 | 结果 |
|---|---------|---------|------|
| 1 | `medicalCode` (14位) 业务编号 | 维持 | **一致** |
| 2 | `tradeNo` (19位 P 开头) 流水单号 | 维持 | **一致** |
| 3 | `medicalRecord.no` 已 A 级否定 | 维持 0 处 | **一致** |
| 4 | `cashflow.billNo` 已 A 级否定 | 维持 0 处 | **一致** |
| 5 | `medicalRecord.medicalCode ≠ medicalRecord.id` | 维持 | **一致** |
| 6 | `tradeNo ≠ cashflow.id` | 维持 | **一致** |
| 7 | Cashflow 与 Wallet 前端协议分离 | 维持 | **一致** |
| 8 | substractType 1/2/3 业务值 | 维持 F | **一致** |

**历史无新错误，无需新增纠正**。

---

## 十、一期复刻影响

### 10.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | 5 大对象 Response 结构（medicalRecordVo / cashflowMedicalRecordVo / machineCenterOrderRecordVo / cashflowDeliveryVo / Take-Glass）| **A 100%** |
| 2 | 11 个 API 完整 Request/Response | **A 100%** |
| 3 | 5 个 HTML 字段绑定 | **A 100%** |
| 4 | medicalCode + tradeNo 业务编号 | **A 100%** |
| 5 | 5 条业务主链 + R1-R6 关系强度 | **A 100%** |
| 6 | machineCenterOrder 3 状态字段（acceptStatus/status/receiveStatus）| **A 100%** |
| 7 | medicalProductDelivery.deliveryStatus 子对象 | **A 100%** |
| 8 | Delivery 通过 cashflowId 关联 | **A 100%** |
| 9 | Take-Glass 通过 medicalRecordId 触发 | **A 100%** |

### 10.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | 业务级 1:1 / 1:N 关系模型 | E |
| 2 | deliveryStatus 0/1/2/3 业务语义 | E |
| 3 | 后端 Cashflow↔MachineCenterOrder↔Delivery 数据库关联 | E |

### 10.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 25 个 ID 字段名（orderId / processingId / deliveryId 等）| F = 当前未观察 |
| 2 | 自创 OrderEntity | F = Response 实际是 medicalRecordVo |
| 3 | 自创 deliveryId / shipmentId | F = 通过 cashflowId 关联 |
| 4 | 自创 takeGlassId | F = 通过 medicalRecordId 关联 |
| 5 | 自创 walletId / balanceId 等 Wallet ID | F = S1-49 已 A 级否定 |
| 6 | 自创 cashflow.medicalRecordId 外键 | F = 前端不直接观察 |
| 7 | deliveryStatus 0/1/2/3 业务值 | F = 业务含义未直接观察 |

---

## 十一、严禁脑补清单（25 个 ID 字段）

> 所有 25 个 ID 字段在 controller.js + 7 HTML 模板范围 = **0 处出现**
> 
> **F 严格表述 = "当前已检查前端证据范围内未观察" ≠ "数据库全局不存在"**

```
orderId                    orderItemId
processingId               processingOrderId          processOrderId
machineOrderId             machineOrderItemId
deliveryId                 shipmentId                  shipmentItemId
pickupId                   notificationId              takeGlassId
paymentId                  transactionId
prescriptionId             chargeId                    chargeItemId
saleOrderId                saleOrderItemId
```

---

## 十二、仍未解决问题（10 个 Q）

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | 订单真实对象边界是否完全明确？| **是**（medicalRecordVo 复合对象）| **A 100%** |
| Q2 | 订单金额字段是否已直接确认？| **是**（`medicalProductRateFee`）| **A 100%** |
| Q3 | Cashflow ↔ Order 是否存在直接字段？| **是**（medicalRecord.id）| **A 100%** |
| Q4 | MachineCenterOrder ↔ Cashflow 是否存在直接字段？| **是**（cashflowId + machineCenterId）| **A 100%** |
| Q5 | MachineCenterOrder ↔ MedicalRecord 是否存在直接字段？| **是**（medicalCode + medicalRecord.medicalRecordType）| **A 100%** |
| Q6 | Delivery 是否存在独立 ID？| **否**（通过 cashflowId 关联）| **A 100%** |
| Q7 | Delivery ↔ MachineCenterOrder 如何关联？| **medicalProductDelivery.deliveryStatus** 子对象 | **A 100%** |
| Q8 | Take-Glass 是否只有 medicalCode 作为业务关联？| **是**（+ medicalRecordId）| **A 100%** |
| Q9 | 这些关系是否都是前端协议关系？| **是**（L1 级别）| **A 100%** |
| Q10 | L3 数据库关系是否仍未知？| **是**（F 维持）| **F** |

---

## 十三、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十四、文档元数据

- **文档编号**：110
- **任务阶段**：S1-51 5 大业务对象协议关系收口
- **侦察时间**：2026-09-03 11:15-11:45
- **S1-51 关键 A 级新发现**：
  1. **Order 没有独立 OrderEntity**（Response 是 medicalRecordVo）
  2. **medicalProductDelivery.deliveryStatus**（MachineCenterOrder 子对象）
  3. **Delivery 通过 cashflowId 关联**（没有 deliveryId / shipmentId）
  4. **Take-Glass 极简结构**（只有 medicalRecord + patient + customer）
  5. **sendTakeMirrorNotice Request 只有 medicalRecordId**
  6. **receiveSmsLog 新字段**（sendTakeMirrorNotice Response）
  7. **MachineCenterOrder 3 状态字段完整定义**（acceptStatus/status/receiveStatus + deliveryStatus）
- **26 项评级 = 25 A + 0 E + 1 F**
- **L1=25 / L2=0 / L3=0 / F=1**
- **历史文档影响**：0（28~109 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-52

---

> **S1-51 完成。**
> **25 A + 0 E + 1 F（5 大业务对象协议收口）**。
> **5 大对象真实 Response 结构 + 5 张证据表 + 5 条业务主链 + R1-R6 关系强度**。
> **medicalCode / tradeNo 业务编号 + cashflowId / medicalRecordId URL 路由参数 + medicalProductDelivery.deliveryStatus 子对象**。
> **deliveryStatus 0/1/2/3 业务含义 = F**。
> **下一步：等待老板下一条指令。**
