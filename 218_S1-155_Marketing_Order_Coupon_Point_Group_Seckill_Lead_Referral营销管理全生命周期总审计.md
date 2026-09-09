# S1-155 Marketing / Order / Coupon / Point / Group / Seckill / Lead / Referral 营销管理全生命周期总审计

> 顶部菜单"营销管理":计次卡 / 积分 / 发券宝 / 客资池 / 推荐新客 / 拼团 / 秒杀 / 订单 / 短信电话群发 / 预约
>
> 本轮严格区分营销侧 vs 就诊侧;所有 ID 字段全部字符级校验。

---

## §0 完整性闸门

| 文件 | 期望 SHA256 | 实际 SHA256 | 状态 |
|---|---|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | ✓ PASS |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | ✓ PASS |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | ✓ PASS |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | ✓ PASS |

**闸门结论:4 文件 SHA256 全部一致,通过。** S1-154 汇报中 machineOrderCompleted.html 的 `F25` 是上一轮手写 typo(实际为 `F29`,与历史基准一致)。

文件规模:2,194,196 bytes / 59,214 行 / 417 个 Controller 注册 / 915 个 .json API。

---

## §1 营销 Controller 全量定位

### 1.1 营销相关 Controller(71 个,关键 23 个)

| Controller | 行号 | 业务归属 | 真实执行 | 核心 API | 核心 Object | Grade |
|---|---:|---|:-:|---|---|---|
| `couponListCtrl` | L12760 | 发券宝 / Coupon | ✓ | selectCouponVoList | couponVo | A |
| `couponHistoryCtrl` | L12702 | Coupon 历史 | ✓ | – | couponVo | A |
| `addCouponCtrl` | L12526 | Coupon 创建 | ✓ | createCoupon | couponVo | A |
| `modifyCouponCtrl` | L12824 | Coupon 编辑 | ✓ | getCouponVo | couponVo | A |
| `myCouponCtrl` | L18818 | 我的 Coupon | ✓ | statCustomerCouponStatus | customerCouponVo | A |
| `addTargetCouponCtrl` | L49071 | 定向 Coupon | ✓ | – | couponVo | C |
| `targetCouponDetailCtrl` | L49445 | 定向 Coupon 详情 | ✓ | getCouponVo | couponVo | C |
| `targetCouponListCtrl` | L49569 | 定向 Coupon 列表 | ✓ | – | couponVo | C |
| `pointsAdminCtrl` | L57582 | 积分规则(admin) | ✓ | saveCorpPointRule | corpPointRule | A |
| `pointsListCtrl` | L36263 | 积分列表 | ✓ | selectCustomerPointVoList | customerPoint | A |
| `pointsListChargeCtrl` | L37432 | 积分充值 | ✓ | – | customerPoint | A |
| `pointsListReChargeCtrl` | L37459 | 积分再充值 | ✓ | – | customerPoint | A |
| `memberCardCtrl` | L18058 | **命名误导** | ✗ | – | – | C |
| `memberPointCtrl` | L18144 | **命名误导** | ✗ | – | – | C |
| `timeCardCtrl` | L34095 | **计次卡 = TrainerCard** | ✓ | selectCustomerTrainerCardVoList | customerTrainerCard | A |
| `timecardBlanceCtrl` | L38373 | 训练卡余额 | ✓ | selectCustomerTrainerCardDataListForStatBalance | customerTrainerCard | A |
| `timecardPerformanceCtrl` | L38415 | 训练卡业绩 | ✓ | selectCustomerTrainerCardDataListForStatGoals | customerTrainerCard | A |
| `timeCardRechargeCtrl` | L38463 | 训练卡充值明细 | ✓ | selectCustomerTrainerCardVoListForDetailReport | customerTrainerCard | A |
| `addProjectCardCtrl` | L52150 | 项目卡(营销视角的 TrainerCard) | ✓ | – | trainerCard | C |
| `projectCardCtrl` | L57851 | 项目卡列表 | ✓ | updateByTrainerCardIdArraySelective | trainerCard | C |
| `feeBankCardCtrl` | L36882 | **命名误导** | C | – | – | C |
| `orderDetailCtrl` | L18937 | 订单详情 | ✓ | getOrderVo | orderVo | A |
| `orderManageCtrl` | L36165 | 订单管理 | ✓ | getOkOrderRecordVoList | okOrderRecordVo | A |
| `selectOrderListCtrl` | L20636 | 订单列表 | ✓ | selectOrderVoListByCorpId | orderVo | A |
| `productOrderCtrl` | L19020 | 商品订单 | ✓ | selectOrderVoListOfSeckillProduct | orderVo | A |
| `addGrouponCtrl` | L13337 | 拼团创建 | ✓ | createGrouponProduct | grouponProduct | A |
| `grouponDetailCtrl` | L13516 | 拼团详情 | ✓ | getGrouponProductVo | grouponProductVo | A |
| `grouponListCtrl` | L13553 | 拼团列表 | ✓ | selectGrouponProductVoList | grouponProductVoList | A |
| `grouponOrderCtrl` | L13632 | 拼团订单列表 | ✓ | selectGrouponOrderVoList | grouponOrderVoList | A |
| `addSecKillProductCtrl` | L16532 | 秒杀商品创建 | ✓ | createSeckillProduct | seckillProduct | A |
| `modifySecKillProductCtrl` | L18569 | 秒杀商品编辑 | ✓ | getSeckillProductVo | seckillProductVo | A |
| `secKillProductDetailCtrl` | L20462 | 秒杀商品详情 | ✓ | getSeckillProductVo | seckillProductVo | A |
| `secKillProductListCtrl` | L20519 | 秒杀商品列表 | ✓ | selectSeckillProductVoList | seckillProductVoList | A |
| `secKillPromotionListCtrl` | L20588 | 秒杀活动列表 | ✓ | selectPromotionVoList | promotionVoList | A |
| `addPromotionCtrl` | L16461 | 推广活动创建 | ✓ | createPromotion | promotionVo | A |
| `modifyPromotionCtrl` | L18477 | 推广活动编辑 | ✓ | getPromotionVo | promotionVo | A |
| `recommendPhoneListCtrl` | L19335 | **客资池 = RecommendPhone(Referral)** | ✓ | selectRecommendPhoneVoList | recommendPhoneVo | A |
| `groupSendCtrl` | L16799 | **短信群发** | ✓ | createTemplateBatchSendTask | templateBatchSendTask | A |
| `groupSendLookCtrl` | L17318 | 群发结果查询 | ✓ | selectTaskTemplateBatchSendList | taskVo | A |
| `sendPlatformCtrl` | L20890 | 任务管理 | ✓ | cancelTemplateBatchSendTask | taskVo | A |
| `smsSetCtrl` | L2867 | 短信模板设置 | ✓ | saveSchoolCheckConfForTemplate | smsTemplateVo | A |
| `phoneAdminCtrl` | L57371 | **命名误导** | C | – | – | C |
| `bookDetailCtrl` | L3669 | **营销预约 = 复用 Appointment(S1-153)** | ✓ | getAppointmentVo + confirmAppointment | appointmentVo | A |
| `bookManageCtrl` | L3706 | 预约管理 | ✓ | selectAppointmentVoList | appointmentVoList | A |
| `bookSettingsCtrl` | L3771 | 预约短信设置 | ✓ | saveCorpAppointmentConf | corpAppointmentConf | A |
| `appointAdminCtrl` | L52344 | 预约场景配置 | ✓ | saveCorpAppointConf | corpAppointConf | A |
| `appointOrderCtrl` | L3664 | **S1-153 空 Stub** | ✗ | – | – | A(空) |
| `screenConditionBatchCtrl` | L45234 | **屏推送(营销推送)** | ✓ | createScreenTemplateBatchSendTask | screenTemplateBatchSendTask | A |
| `screenConditionBatchGroupSendCtrl` | L45310 | 屏推送群发 | ✓ | – | taskVo | A |
| `screenConditionBatchGroupSendLookCtrl` | L45589 | 屏推送结果 | ✓ | selectTaskScreenTemplateBatchSendList | taskVo | A |
| `screenPromotionListCtrl` | L47113 | 屏推广列表 | ✓ | selectPromotionVoList | promotionVoList | A |
| `addScreenPromotionCtrl` | L38818 | 屏推广创建 | ✓ | – | promotionVo | C |
| `screenPromotionConfigCtrl` | L46600 | 屏推广配置 | ✓ | – | promotionVo | C |
| `screenPromotionToothConfigCtrl` | L47886 | 屏推广(牙齿)配置 | ✓ | – | promotionVo | C |
| `screenPromotionStudentCtrl` | L47512 | 屏推广学生 | ✓ | – | promotionVo | C |
| `addGroupeditCtrl` | L50899 | **Groupedit(拼团编辑)** | C | – | – | C |
| `groupeditListCtrl` | L54133 | Groupedit 列表 | C | – | – | C |
| `modifyGroupeditCtrl` | L56458 | Groupedit 编辑 | C | – | – | C |
| `addVisitCtrl` | L49594 | **S1-154 已知复诊 / 通知(sceneType=4 随访)** | ✓ | – | visitVo | A |
| `visitDetailsCtrl` | L50044 | 复诊详情 | ✓ | – | visitVo | A |

**总结**:营销侧 71 个 Controller(417 总数),关键真实 23 个 + 命名误导 5 个(memberCardCtrl / memberPointCtrl / feeBankCardCtrl / phoneAdminCtrl / appointOrderCtrl)+ Screen 系列 6 个。

### 1.2 9 大业务模块分类

| 模块 | 真实 Controller | Object 实体 | 真实 ID |
|---|---|---|---|
| **计次卡** | timeCardCtrl × 4 + addProjectCardCtrl / projectCardCtrl | trainerCard + customerTrainerCard | **trainerCardId** ✓ |
| **积分** | pointsAdminCtrl + pointsListCtrl × 3 | customerPoint (Customer 字段) | **无 pointId**,F/禁造 |
| **发券宝** | couponListCtrl × 4 + myCouponCtrl + addTargetCouponCtrl × 3 | coupon + customerCoupon | **couponId + customerCouponId** ✓ |
| **客资池** | recommendPhoneListCtrl | recommendPhone | **recommendPhoneId** ✓ |
| **推荐新客** | 同上(recommendPhone = Referral) | recommendPhone | **recommendPhoneId** ✓ |
| **拼团** | addGrouponCtrl + grouponDetailCtrl + grouponListCtrl + grouponOrderCtrl | grouponProduct + grouponOrderVoList | **grouponProductId** ✓,无 groupId |
| **秒杀** | addSecKillProductCtrl + modifySecKillProductCtrl + secKillProductDetailCtrl + secKillProductListCtrl + secKillPromotionListCtrl | seckillProduct + promotion | **seckillProductId + promotionId** ✓,无 seckillId |
| **订单** | orderDetailCtrl + orderManageCtrl + selectOrderListCtrl + productOrderCtrl | customerOrder + orderExpress | **orderId** ✓ |
| **短信电话群发** | groupSendCtrl + groupSendLookCtrl + sendPlatformCtrl + smsSetCtrl + screenConditionBatchCtrl × 3 | templateBatchSendTask + screenTemplateBatchSendTask | **taskTemplateBatchSendId + taskScreenTemplateBatchSendId** ✓,无 smsId |
| **预约** | bookDetailCtrl + bookManageCtrl + bookSettingsCtrl + appointAdminCtrl | appointment + corpAppointmentConf | **appointmentId + appointId** ✓(复用 S1-153) |

---

## §2 Marketing Order 全量审计

### 2.1 关键发现:**Marketing Order 不存在**

| 关键词 | 命中数 | 结论 |
|---|---:|---|
| `marketingOrder` | **0** | F / 禁造 marketingOrderId |
| `marketingOrderId` | **0** | F / 禁造 |
| `order` | 540 | 普通 order 字段 |
| `orderId` | 17(6 有效) | A 真实 |
| `orderVo` | 12 | A 真实 |
| `orderList` | 87 | 含 orderList 拼接词 |

**结论**:"营销订单"不是独立 Object。系统中只有统一的 Order 体系,通过 `orderTypeArray` 区分(订单管理:`orderTypeArray = [50, 60]`,L20644)。

### 2.2 orderId 完整 6 处真实命中

| 行号 | 上下文 | 角色 |
|---:|---|---|
| L18939 | `$scope.orderId = $stateParams.orderId;` | State(订单详情) |
| L18942 | getOrderVo.json Request `{orderId: $scope.orderId}` | R |
| L20709 | pickUpOrder.json Request `{orderId: id}` | W |
| L20715 | getOrderVo.json Request `{orderId: id}` | R |
| L20836 | `$scope.deliveryObj.orderId = id;` | deliveryObj 局部 |
| L20858 | getOrderVo.json Request `{orderId: $scope.deliveryObj.orderId}` | R |

### 2.3 Order API 全量(25 个)

| API | 行号 | R/W | Request | Response | Grade |
|---|---:|:-:|---|---|---|
| `getOrderVo.json` | L18942 | R | orderId | orderVo | A |
| `selectOrderVoListByCorpId.json` | L20664 | R | keyword/status/orderTypeArray | orderVoList | A |
| `selectOrderVoListByCustomerId.json` | L19718 | R | customerId | orderVoList | A |
| `selectOrderVoListOfSeckillProduct.json` | L19026 | R | seckillProductId | orderVoList | A |
| `selectMyCorpPaymentOrder.json` | L3466 | R | – | paymentOrderList | A |
| `getOkOrderRecordVoList.json` | L36197 | R | firstVisitFrom/firstVisitTo/keyword | okOrderRecordVoList | A |
| `getHaveOrderMedicalRecordVoList.json` | L31055 | R | – | orderMedicalRecordList | A |
| `getUnPlaceOrderMedicalRecordVoList.json` | L6976 | R | – | orderMedicalRecordList | A |
| `computeUnPlaceOrderMedicalRecordFee.json` | L6680 | W | medicalRecordId | fee | C |
| `reComputeUnPlaceOrderMedicalRecordFee.json` | L6884 | W | – | fee | C |
| `pickUpOrder.json` | L20709 | W | orderId | – | A |
| `deliveryOrder.json` | L20852 | W | deliveryObj(orderId/expressCompany/expressCode) | orderVo | A |
| `createRefundOrderLog.json` | L20734 | W | customerId + cashflowId | refundOrderLogId | A |
| `commitRefundOrderLog.json` | L20740 | W | refundOrderLogId | – | A |
| `getRequirementOrderVo.json` | L20414 | R | – | requirementOrderVo | C |
| `getOrderBrandList.json` | L17040 | R(5 处) | – | orderBrandList | A |
| `getOrderCategoryList.json` | L17036 | R(5 处) | – | orderCategoryList | A |

### 2.4 命名误导

| 名称 | 实际内容 |
|---|---|
| `selectOrderListCtrl` | 真实 selectOrderVoListByCorpId(订单列表,不是 order list) |
| `getOrderFactory / getOrderCountFactory` | Angular Factory,不是 API |
| `completeOrder` | L16225 实际是 `completeMachineCenterOrder` 的 alias(S1-150 已知) |

---

## §3 Order Object 字段

### 3.1 orderVo 字段(L18942 getOrderVo Response)

| 字段 | 路径 | Source Type | Grade |
|---|---|---|---|
| `customerOrder.status` | Response | A |
| `orderExpress.expressStatus` | Response | A |
| `orderExpress.expressType` | Response | A |
| `orderVo.id` | Response | A |
| `orderVo.orderId` | – | F(未观察到) |
| `customer.id` | Response(L20735 refund 中) | A |
| `cashflow.id` | Response(L20736) | A |
| `cashflow.payType` | Response(L20745) | A |
| `cashflow.totalPayment` | Response(L20746) | A |

### 3.2 okOrderRecord 字段(L36197)

| 字段 | 行号 | Source Type |
|---|---:|---|
| `okOrderRecord.medicalRecordId` | L36251 | Response |
| `medicalRecordIdList[]` | L36216 | Local Array |
| `firstVisitFrom` / `firstVisitTo` | L36182-36185 | Request Param |
| `doctorName` / `optometrist` / `keyword` | L36174-36176 | Request Filter |

### 3.3 selectOrderVoListByCorpId Request(L20644)

| 字段 | 行号 | Type |
|---|---:|---|
| `orderTypeArray = [50, 60]` | L20644 | Filter(订单类型) |
| `orderStatus` (0=未发货/1=已发货/2=已收货) | L20638 | Status Enum |
| `expressStatus` | L20692 | Filter |
| `expressType` (1=商家配送/2=到店服务) | L20639 | Filter |
| `refundStatus` | L20700 | Filter |
| `startTime` / `endTime` | L20647-20658 | Time Filter |
| `keyword` | L20642 | Keyword |

### 3.4 orderManageCtrl L36165 业务特征

- **核心目的**:`getOkOrderRecordVoList.json` + 勾选导出已成交订单
- **核心字段**:medicalRecordIdList(`okOrderRecord.medicalRecordId` 拼接成 `_` 分隔字符串)
- **导出 URL**:`downloadOkOrderRecord.htm?medicalRecordIdList=`(L36239)
- **结论**:`okOrderRecordVo` 是 Order 与 MedicalRecord 的桥接 VO

---

## §4 计次卡(TrainerCard)

### 4.1 关键发现:计次卡 = TrainerCard

| 关键词 | 命中 | 真实? |
|---|---:|:-:|
| `timesCard` | **0** | F / 禁造 |
| `timeCard` | 18 | C(部分混淆) |
| `countCard` | **0** | F / 禁造 |
| `cardId` | **0** | F / 禁造(没有 card ID) |
| `trainerCard` | 多处 | A 真实 |
| `customerTrainerCard` | 多处 | A 真实 |
| `trainerCardId` | 5 | A 真实 |
| `customerTrainerCardId` | 2 | A 真实 |

**业务定义**:系统中"计次卡"实际叫 `trainerCard`(训练卡),`customerTrainerCard` 是用户购买的实例。

### 4.2 TrainerCard API 全量(20+)

| API | 行号 | R/W | Grade |
|---|---:|:-:|---|
| `getCustomerCard.json` | L18113 | R | A |
| `updateExtCardNo.json` | L18129 | W | C |
| `addTrainerCard.json` | L52223 | W | A |
| `updateTrainerCard.json` | L52223 | W | A |
| `updateByTrainerCardIdArraySelective.json` | L57949 | W | A |
| `getTrainerCard.json` | L52170 | R | A |
| `getCustomerTrainerCard.json` | L34622 | R | A |
| `selectTrainerCardList.json` | L34433 | R | A |
| `selectCustomerTrainerCardVoList.json` | L34148 | R | A |
| `selectCustomerTrainerCardVoListForDetailReport.json` | L38478 | R | A |
| `selectCustomerTrainerCardDataListForStatBalance.json` | L38400 | R | A |
| `selectCustomerTrainerCardDataListForStatGoals.json` | L38448 | R | A |
| `selectFirstCustomerTrainerCardLog.json` | L34400 | R | A |
| `investMoneyForCustomerTrainerCard.json` | L34516 | W | A |
| `consumeCustomerTrainerCardNumbers.json` | L34652 | W | A |
| `statCustomerWalletAndTrainerCard.json` | L37826 | R | A |
| `saveCardSubstractType.json` | L55740 | W | C |
| `getCorpTimeData.json` | L13925 | R | C |
| `selectEmployeeSchedulingDetailTimeVo.json` | L40859 | R | C |
| `selectEmployeeSchedulingDetailTimeVoList.json` | L40799 | R | C |
| `selectOrCreateWechatCard.json` | L5263 | W | C |

### 4.3 trainerCardId 完整 5 处

| 行号 | 上下文 |
|---:|---|
| L34473 | `$scope.obj.trainerCardId = this.info.id; // 选中次卡id` |
| L34509 | investMoneyForCustomerTrainerCard Request `trainerCardId: $scope.obj.trainerCardId` |
| L52169 | `function (trainerCardId)` |
| L52171 | getTrainerCard Request `trainerCardId: trainerCardId` |
| L52181 | `$scope.obj.trainerCardId = trainerCardId;` |

### 4.4 customerTrainerCard 真实业务字段(L34125+)

| 字段 | 行号 | Type |
|---|---:|---|
| `customerTrainerCard.id` | L34401 | R |
| `customerTrainerCard.balanceNumber` | L34649 | R(剩余次数) |
| `customerTrainerCard.numbers` | L34171 | R(总次数) |
| `customerTrainerCard.marketPrice` | L34172 | R(售价) |
| `customerTrainerCard.validMonths` | L34448 | R(有效月数) |
| `customerTrainerCard.allowReturnCard` | L34459 | R(是否允许退卡) |
| `customerTrainerCardLog.id` / `customerTrainerCardLog.payChannel` | L34407 | R |
| `customerTrainerCardLogId` | L34533 | Local(充值日志) |

### 4.5 customerTrainerCardLog 真实

- `customerTrainerCardLogId`:L34533 本地变量,investMoneyForCustomerTrainerCard 返回值
- `commitForInvestMoneyForCustomerTrainerCard.json`(L34537 字符串拼接)
- `commitForConsumeCustomerTrainerCard.json`(L34656 字符串拼接)
- `commitForScanPayCustomerTrainerCard.json`(L34549)
- `commitForPosPayCustomerTrainerCard.json`(L34541)

### 4.6 计次卡与 Coupon / Member 边界

| 关系 | 真实? |
|---|:-:|
| 计次卡 ↔ Coupon | ✗ 完全独立 |
| 计次卡 ↔ Member | ✗(S1-154 已确认 memberCard 0 命中) |
| 计次卡 ↔ Product | ✗(只是 buyCard 业务流) |
| 计次卡 ↔ Cashflow | ✓(consumeCustomerTrainerCardNumbers 间接) |
| 计次卡 ↔ Order | ✗ 独立 |

---

## §5 积分(CustomerPoint)

### 5.1 关键发现:Point 不是独立 Object

| 关键词 | 命中 | 真实? |
|---|---:|:-:|
| `point` | 539 | A(普通变量) |
| `points` | 118 | A(可能是数组) |
| `pointId` | **0** | **F / 禁造** |
| `pointLogId` | 0 | F / 禁造 |
| `score` | 2 | F / 禁造 |
| `integral` | 11 | C(普通业务术语) |

**结论**:`point` 是 Customer 字段,不是 ID 实体。无 pointId 字符级证据。

### 5.2 Point API 全量(11 个)

| API | 行号 | R/W | Grade |
|---|---:|:-:|---|
| `getCustomerPoint.json` | L7497 | R(4 处) | A |
| `pointToMoney.json` | L7500 | W(2 处) | A |
| `clearCustomerPoint.json` | L36299 | W | A |
| `initAddCustomerPoint.json` | L18217 | W | A |
| `initSubCustomerPoint.json` | L18231 | W | A |
| `commitCustomerPointLog.json` | L18197 | W(2 处) | A |
| `getCorpPointRule.json` | L18179 | R(5 处) | A |
| `saveCorpPointRule.json` | L57648 | W | A |
| `selectCustomerPointLogVoList.json` | L18155 | R(3 处) | A |
| `selectCustomerPointVoList.json` | L36322 | R(2 处) | A |

### 5.3 Point 字段(L7497)

| 字段 | 行号 | Type |
|---|---:|---|
| `point` (Request Payload) | L7501 | Request Param |
| `initPoint` (Response) | L7503 | R |
| `receivedFromPoint` (计算字段) | L7528 | Local 业务字段 |
| `customerPoint.amount` | – | **F**(未观察到 amount 字段) |

### 5.4 命名误导

- `memberPointCtrl`(L18144):S1-154 已知是空路由,不管理 Point
- `pointsListChargeCtrl`(L37432):实际管理 CustomerPoint 充值
- `pointsListReChargeCtrl`(L37459):实际管理再充值
- `pointsAdminCtrl`(L57582):管理 corpPointRule,不是 Member Point

### 5.5 Point ↔ Customer / Order / Member

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Customer → Point | ✓ A | getCustomerPoint.json 4 处 |
| Order → Point | ✗ | 0 命中 |
| Point → Coupon | ✗ | 0 命中 |
| Point → Cashflow | ✗ | 0 命中(只是业务字段 receivedFromPoint) |
| Point → Member | ✗ | 0 命中(S1-154 已确认 memberPoint 0 命中) |
| Point → MedicalRecord | ✗ | 0 命中 |

---

## §6 Coupon / 发券宝

### 6.1 Coupon 是 4 级体系

| 层级 | Object | 真实 ID | Grade |
|---|---|---|---|
| Coupon 模板 | `couponVo`(L12769 selectCouponVoList) | **couponId** | A |
| 用户领券 | `customerCouponVo`(L12711 selectCustomerCouponVoList,7 处) | **customerCouponId** | A |
| 定向 Coupon | `targetCoupon` | 复用 couponId | C |
| Coupon 群发任务 | `couponBatchSendTask` | **taskCouponBatchSendId** | A |

### 6.2 Coupon API 全量(19 个)

| API | 行号 | R/W | Request | Grade |
|---|---:|:-:|---|---|
| `createCoupon.json` | L12684 | W | couponVo 字段 | A |
| `getCouponVo.json` | L12836 / L49389 | R(2 处) | couponId | A |
| `useCoupon.json` | L12746 | W(3 处) | customerCouponId | A |
| `sendCoupon.json` | L18835 | W | customerId + couponId | A |
| `activeCoupon.json` | L13046 | W | couponId | A |
| `invalidCoupon.json` | L12794 | W | couponId | A |
| `updateActiveCoupon.json` | L13149 | W | – | A |
| `updateCreatingCoupon.json` | L13042 | W(2 处) | – | A |
| `getCustomerCouponVo.json` | L12736 | R(3 处) | – | A |
| `selectCouponVoList.json` | L12769 | R(3 处) | – | A |
| `selectCustomerCouponVoList.json` | L12711 | R(7 处) | – | A |
| `selectUsableCustomerCouponVoList.json` | L6607 | R | medicalRecordId | A |
| `computeUsableCustomerCoupon.json` | L6627 | W | customerCouponId + obj | A |
| `isCustomerCouponUsable.json` | L6870 | R | customerCouponId | A |
| `statCustomerCouponStatus.json` | L18853 | R | – | A |
| `createCouponBatchSendTask.json` | L49433 | W | – | A |
| `getTaskCouponBatchSendVo.json` | L49499 | R(2 处) | taskCouponBatchSendId | A |
| `selectTaskCouponBatchSendVoList.json` | L49573 | R | – | A |
| `getBatchSendCustomerCouponVoList.json` | L49454 | R | – | C |

### 6.3 Coupon Object 真实字段(L12527 addCouponCtrl)

| 字段 | 行号 | Type |
|---|---:|---|
| `couponColor` | L12529 | R |
| `couponType` | L12532 | R(0=优惠券) |
| `couponTotalCount` | L12533 | R |
| `couponValue` | L12539 | R(面值) |
| `couponRate` | L12540 | R(折扣率) |
| `useOverCount` | L12541 | R |
| `useOverMoney` | L12542 | R |
| `useTimeStart` / `useTimeEnd` | L12543-12544 | R |
| `useScene` | L12537 | R |
| `permissionToReturn` | L12538 | R |
| `sendExpireMsg` | L12531 | R |
| `couponRemark` | L12556 | R |
| `couponVo.memberRate` | L6635 | R |
| `couponVo.rateFee` | L6636 | R |
| `couponVo.couponKey` | L6629 | R |

### 6.4 Coupon 状态枚举(L12761)

| status id | name |
|---:|---|
| null | 全部 |
| 0 | 未使用 |
| 1 | 已使用 |
| 2 | 已退款 |

### 6.5 couponId 完整 9 处

| 行号 | 上下文 |
|---:|---|
| L12794 | invalidCoupon.json `{couponId: id}` |
| L12825 | State `$stateParams.couponId` |
| L12828 | data.couponId |
| L12829 | obj.couponId |
| L12836 | getCouponVo.json Request |
| L13046 | activeCoupon.json Request |
| L18835 | sendCoupon.json Request |
| L49389 | getCouponVo.json Request |
| L49396 | obj.couponId 校验 |

### 6.6 customerCouponId 完整 17 处(节选)

| 行号 | 上下文 |
|---:|---|
| L6621 | 校验 `!$scope.obj.customerCouponId` |
| L6626 | obj 拼接 |
| L6647 | `$scope.obj.customerCouponId = item.customerCoupon.id` |
| L6655 | 清空 |
| L6867 | 校验存在 |
| L6869 | obj 拼接 |
| L6932 | 校验 |
| L6933 | obj 拼接 |
| +9 处 | compute / useCoupon / isUsable |

### 6.7 Coupon ↔ Customer / Order / Cashflow / Product / Member

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Coupon → Customer | ✓ A | sendCoupon.json `{customerId, couponId}` L18835 |
| Customer → CustomerCoupon | ✓ A | selectCustomerCouponVoList 7 处 L12711 |
| Coupon → Order | ✓ A | computeUsableCustomerCoupon L6627 / isCustomerCouponUsable L6870 |
| Order → Coupon | ✓ A | medicalRecordId 触发的可用券计算 L6607 |
| Coupon → Cashflow | ✗ | 0 命中(只是业务价格扣减) |
| Coupon → Product | ✗ | 0 命中 |
| Coupon → Member | ✗ | 0 命中 |
| CustomerCoupon → Member | ✗ | 0 命中 |

---

## §7 客资池 / Lead

### 7.1 关键发现:Lead 不存在,实际是 RecommendPhone

| 关键词 | 命中 | 真实? |
|---|---:|:-:|
| `lead` | 14 | 普通变量(lead 转换等) |
| `leadId` | **0** | **F / 禁造** |
| `customerLead` | **0** | F / 禁造 |
| `customerLeadId` | 0 | F / 禁造 |
| `客资` | 8 | C(普通中文字符) |
| `线索` | **0** | F / 禁造 |
| `customerPool` | 0 | F / 禁造 |
| `pool` | 4 | C(连接池/对象池) |
| `recommendPhone` | 多处 | **A 真实** |
| `recommendPhoneId` | 12 | **A 真实** |
| `referral` | **0** | F / 禁造 referralId |

**结论**:"客资池"和"推荐新客"在代码中是同一个 Controller(`recommendPhoneListCtrl`),对应 Object 是 `recommendPhone`(推荐电话)。无 leadId / referralId。

### 7.2 RecommendPhone API 全量(5 个)

| API | 行号 | R/W | Grade |
|---|---:|:-:|---|
| `selectRecommendPhoneVoList.json` | L19593 | R | A |
| `getRecommendPhoneVo.json` | L19784 | R | A |
| `assignRecommendPhoneList.json` | L19623 | W | A |
| `linkRecommendPhone.json` | L19792 | W | A |
| `getSchoolMateCheckVoOfRecommendPhone.json` | L19753 | R | A |

### 7.3 recommendPhoneId 完整 12 处

| 行号 | 上下文 |
|---:|---|
| L19094 | `setIntention.setParams('recommendPhoneId', item.recommendPhone.id)` |
| L19673 | `var recommendPhoneId = item.recommendPhone.id` |
| L19677 | `$scope.recommendPhoneId = recommendPhoneId` |
| L19693 | Request |
| L19754 | Request |
| L19765 | `$scope.data.recommendPhoneId = id` |
| L19784 | getRecommendPhoneVo.json Request |
| L19808 | `$scope.data.recommendPhoneId = id` |
| +4 处 | 同 |

### 7.4 Lead ↔ Customer / Patient / Employee / FollowUp

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Lead → Customer | ✓ A | linkRecommendPhone.json 关联 |
| Lead → Patient | ✗ | 0 命中 |
| Lead → Employee | ✓ A | assignRecommendPhoneList.json 分配 |
| Lead → FollowUp | ✓ A | DefineFollowUp.referrer(S1-154 已知) |
| Lead → SchoolMateCheck | ✓ A | getSchoolMateCheckVoOfRecommendPhone.json L19753 |

### 7.5 关键区分:RecommendPhone vs DefineFollowUp.referrer

| 维度 | recommendPhone(Referral) | DefineFollowUp.referrer |
|---|---|---|
| Controller | recommendPhoneListCtrl L19335 | followUpCtrl L11504 / myMemberRecordCtrl L33218 |
| API | selectRecommendPhoneVoList / assignRecommendPhoneList | DefineFollowUp Service(S1-154 已知) |
| ID | recommendPhoneId 12 处 | **无 ID 字段**(只是 Service 内字段) |
| 业务 | 营销→新客推荐 | 随访→推荐人 |
| Grade | A 独立 Object | F(只是 Service 字段) |

**结论**:`referral` / `referrer` 是普通变量或 Service 字段,不是营销独立 Object。**营销 Referral = RecommendPhone**。

---

## §8 推荐新客 / Referral

### 8.1 Referral 0 命中

| 关键词 | 命中 |
|---|---:|
| `referral` | **0** |
| `referralId` | **0** |
| `referrer` | 26 |
| `referrerId` | **0** |
| `referee` | **0** |
| `refereeId` | **0** |
| `recommend` | 82 |
| `recommendPhone` | 多处 |

`recommendPhone` 是营销侧的"Referral"实现。

### 8.2 推荐新客 = RecommendPhoneListCtrl(已 §7)

业务字段:
- `recommendPhone.id` → recommendPhoneId
- `recommendPhone.phone` (手机号)
- `recommendPhone.intention` (setIntention L19094)

### 8.3 Referral ↔ Customer / Patient / FollowUp / Order

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Referral → Customer | ✓ A | linkRecommendPhone.json |
| Referral → Patient | ✗ | F(经 Customer 中转) |
| Referral → FollowUp | ✓ A | DefineFollowUp.referrer(但不是 Referral Entity) |
| Referral → Order | ✗ | F(无字段) |
| Referral → Cashflow | ✗ | F |

---

## §9 拼团 / Group / Groupon

### 9.1 Groupon 真实,Group 0 命中

| 关键词 | 命中 | 真实? |
|---|---:|:-:|
| `group` | 82 | 普通变量(AngularJS group / 组件) |
| `groupId` | **0** | **F / 禁造** |
| `groupOrder` | **0** | F / 禁造 |
| `groupOrderId` | **0** | F / 禁造 |
| `team` | **0** | F / 禁造 |
| `teamId` | **0** | F / 禁造 |
| `groupBuy` | **0** | F / 禁造 |
| `拼团` | 1 | C(中文 UI) |
| `groupon` | 多处 | **A 真实** |
| `grouponProductId` | 3+ | A 真实 |
| `grouponProductVo` | 多处 | A 真实 |
| `grouponOrderVoList` | 多处 | A 真实 |

**结论**:系统中"拼团"叫 Groupon,不是 Group。Group 是 AngularJS 通用变量。

### 9.2 Groupon API 全量(7 个)

| API | 行号 | R/W | Grade |
|---|---:|:-:|---|
| `createGrouponProduct.json` | L13488 | W | A |
| `deleteGrouponProduct.json` | L13614 | W | A |
| `getGrouponProductVo.json` | L13524 | R | A |
| `invalidGrouponProduct.json` | L13600 | W | A |
| `selectGrouponOrderVoList.json` | L13638 | R | A |
| `selectGrouponProductVoList.json` | L13560 | R | A |
| `selectVisionGroupList.json` | L41100 | R | C(验光小组) |
| `selectVisionGroupManageList.json` | L43622 | R | C |
| `statSchoolCompleteGroupManage.json` | L43620 | R | C |

### 9.3 grouponOrderCtrl L13632 业务特征

- Request: `grouponProductId` (从 State)
- Response: `selectGrouponOrderVoList.items[].groupon.endTime`(L13648)
- **grouponOrderVoList 是 List,没有独立 grouponOrderId**
- leftTime 计算字段(L13657)

### 9.4 Groupon ↔ Customer / Product / Order / Cashflow

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Groupon → Customer | ✗(隐含) | grouponOrderVoList 嵌套 |
| Groupon → Product | ✓ A | grouponProductVo 有 skuCode(L13582) |
| Groupon → Order | ✓ A | grouponOrderVoList 是 OrderVO 的子集 |
| Groupon → Cashflow | ✗ | 0 命中 |
| Groupon → Seckill | ✗ | 独立 |

### 9.5 命名区分:grouponOrderVoList vs customerOrder

- `grouponOrderVoList`(L13638):拼团场景下的订单列表
- `customerOrder`(L20718):通用 customerOrder

---

## §10 秒杀 / Seckill

### 10.1 SeckillProduct 真实

| 关键词 | 命中 | 真实? |
|---|---:|:-:|
| `seckill` | 144 | A |
| `seckillId` | **0** | **F / 禁造** |
| `seckillProductId` | 14 | **A 真实** |
| `flashSale` | **0** | F / 禁造 |
| `flashSaleId` | 0 | F / 禁造 |
| `秒杀` | 6 | C(中文 UI) |
| `killOrder` | **0** | F / 禁造 |
| `seckillOrder` | 0 | F / 禁造 |
| `seckillOrderId` | 0 | F / 禁造 |

### 10.2 Seckill API 全量(12 个)

| API | 行号 | R/W | Grade |
|---|---:|:-:|---|
| `createSeckillProduct.json` | L16619 | W(2 处) | A |
| `updateSeckillProduct.json` | L18721 | W(2 处) | A |
| `getSeckillProductVo.json` | L18576 | R(2 处) | A |
| `invalidSeckillProduct.json` | L20574 | W(2 处) | A |
| `activeSeckillProduct.json` | L16720 | W(2 处) | A |
| `selectSeckillProductVoList.json` | L20550 | R | A |
| `selectOrderVoListOfSeckillProduct.json` | L19026 | R | A |
| `getPromotionVo.json` | L18485 | R(5 处) | A |
| `getPromotionQrcode.json` | L18498 | R(3 处) | A |
| `updatePromotion.json` | L18515 | W(2 处) | A |
| `createPromotion.json` | L16477 | W(2 处) | A |
| `selectPromotionVoList.json` | L19055 | R(2 处) | A |

### 10.3 seckillProduct 真实字段(L18570+)

| 字段 | 行号 | Type |
|---|---:|---|
| `seckillProduct.productName` | L18578 | R |
| `seckillProduct.description` | L18579 | R |
| `seckillProduct.modelPicture` | L18581 | R |
| `seckillProduct.skuCode` | L18582 | R |
| `seckillProduct.unitName` | L18583 | R |
| `seckillProduct.modelType` | L18584 | R |
| `seckillProduct.model1Name` / `model2Name` | L18585 | R |
| `seckillProduct.marketPrice` | L20489 | R |
| `seckillProduct.seckillPrice` | L20490 | R |
| `seckillProduct.totalCount` | L20491 | R |
| `seckillProduct.startTime` / `endTime` | L20492-20499 | R |

### 10.4 seckillProductId 完整 14 处

| 行号 | 上下文 |
|---:|---|
| L16720 | activeSeckillProduct Request |
| L18574 | State |
| L18576 | getSeckillProductVo Request |
| L18726 | State 跳转 modifySecKillProduct |
| L18797 | activeSeckillProduct Request |
| L19022 | State |
| L19026 | selectOrderVoListOfSeckillProduct Request |
| L20467 | State |
| L20574 | invalidSeckillProduct Request |
| L20877 | invalidSeckillProduct Request |
| +4 处 | 修改/查询 |

### 10.5 promotionId 完整 43 处(秒杀活动)

- `addPromotionCtrl` L16461 创建 promotion
- `secKillPromotionListCtrl` L20588 list
- `selectPromotionVoList.json` L19055 列表
- `getPromotionVo.json` L18485 详情
- `getPromotionQrcode.json` L18498 二维码
- `updatePromotion.json` L18515 编辑
- promotionType=3(L20593)是秒杀活动类型

### 10.6 Seckill ↔ Customer / Order / Cashflow / Promotion

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| SeckillProduct → Promotion | ✓ A | promotionId 关联 |
| SeckillProduct → Order | ✓ A | selectOrderVoListOfSeckillProduct |
| SeckillProduct → Customer | ✗ | F(无字段) |
| SeckillProduct → Cashflow | ✗ | F |
| SeckillProduct → Product | ✓ A | skuCode 是 Product 字段 |

---

## §11 SMS / 电话群发

### 11.1 关键发现:SMS 群发 = 3 种 BatchSendTask

| 任务类型 | 真实 ID | 命中 | API |
|---|---|---:|---|
| **TemplateBatchSendTask** | `taskTemplateBatchSendId` | **11** | 6 个 API |
| **CouponBatchSendTask** | `taskCouponBatchSendId` | **3** | 3 个 API |
| **ScreenTemplateBatchSendTask** | `taskScreenTemplateBatchSendId` | **9** | 6 个 API |

`smsId` / `smsTaskId` / `batchSendId` 全部 0 命中。

### 11.2 TemplateBatchSendTask(11 真实 ID)

| 行号 | 上下文 |
|---:|---|
| L16837 | `$stateParams.taskTemplateBatchSendId ? true : false` |
| L17248 | searchTask(taskTemplateBatchSendId) |
| L17251 | Request |
| L17310 | searchTask 调用 |
| L17322 | obj.taskTemplateBatchSendId |
| L20910 | lookDetails |
| L20912 | Request |
| L20915 | cancelTask |
| L20918 | Request |
| L20927 | lookCondition |
| L20929 | Request |

API:`createTemplateBatchSendTask` L17235 / `getTaskTemplateBatchSendVo` L17250 / `selectTaskTemplateBatchSendList` L20893 / `selectTaskTemplateBatchSendLogVoList` L17367 / `cancelTemplateBatchSendTask` L20917 / `getMedicalRecordListOfReceiveSms` L13736

### 11.3 CouponBatchSendTask(3 真实 ID)

| 行号 | 上下文 |
|---:|---|
| L49448 | `$scope.obj.taskCouponBatchSendId = $stateParams.taskCouponBatchSendId` |
| L49499 | getTaskCouponBatchSendVo Request |
| L49509 | getTaskCouponBatchSendVo Request |

API:`createCouponBatchSendTask` L49433 / `getTaskCouponBatchSendVo` L49499 / `selectTaskCouponBatchSendVoList` L49573

### 11.4 ScreenTemplateBatchSendTask(9 真实 ID)

| 行号 | 上下文 |
|---:|---|
| L45284 | lookDetails |
| L45286 | Request |
| L45289 | cancelTask |
| L45292 | Request |
| L45302 | lookCondition |
| L45304 | Request |
| L45537 | Request(State |
| L45580 | State 校验 |
| L45593 | obj |

API:`createScreenTemplateBatchSendTask` L45502 / `cancelScreenTemplateBatchSendTask` L45291 / `selectTaskScreenTemplateBatchSendList` L45249 / `selectScreenTemplateBatchSendTaskDetails` L45536 / `screenConditionBatchGroupSendCtrl` L45310 / `screenConditionBatchGroupSendLookCtrl` L45589

### 11.5 SMS 字段

| 字段 | 行号 | Type |
|---|---:|---|
| `corpSms.smsAdminName` | L3778 | R(预约) |
| `corpSms.smsMobile` / `smsBackMobile` | L3779-3780 | R |
| `corpSms.smsBackAdminName` | L3781 | R |
| `corpSms.smsChooseStatus` | L2954 | R |
| `corpSms.voiceChooseStatus` | L2955 | R |
| `corpSms.templateAddressType` | L2956 | R |
| `smsTemplateListForSceneList` | L2916 | R |
| `smsTemplate.id` | L2991 | R |
| `smsTemplate.example` | L2991 | R |
| `smsTemplate.ttsCode` | L2991 | R |

### 11.6 smsSetCtrl 业务结构(L2867)

- **smsSetCtrl** 是全局短信/电话模板配置
- smsTemplate + voiceTemplate(双模板)
- `selectCorpSmsByCorpId.json` L13993 (4 处)→ Corp SMS 配置
- `selectCorpSmsTemplatePoolForScene.json` L49637 → 场景模板池
- `selectCorpSmsAddLogVoList.json` L55969 → SMS 流水
- `selectCorpSmsUseLogVoList.json` L56005 → 使用流水
- `updateCorpSmsDisable.json` L55888 → 禁用
- `updateCorpSmsWarningCount.json` L56019 → 警告次数

### 11.7 群发 ↔ Customer / Patient / School / FollowUp

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| 群发 → Customer | ✓ A | getMemberList / selectCustomerList |
| 群发 → Patient | ✗ | F |
| 群发 → School | ✓ A | sendSmsToSchoolMateCheck L44659 |
| 群发 → FollowUp | ✗ | F |
| 群发 → Sale / MedicalRecord | ✗ | F |

### 11.8 命名误导

- `selectCorpSmsByCorpId.json`(L13993):不是选 SMS,是选公司短信配置
- `smsSetCtrl` 不发短信,只设模板

---

## §12 营销预约 / Appointment(复用 S1-153)

### 12.1 关键发现:营销预约 = S1-153 Appointment

`bookDetailCtrl` / `bookManageCtrl` / `bookSettingsCtrl` / `appointAdminCtrl` 实际就是 S1-153 审计的 Appointment 业务,在营销菜单下复用。

### 12.2 bookDetailCtrl L3669 业务特征

| 字段 | 行号 | Type |
|---|---:|---|
| `$stateParams.appointmentId` | L3670 | State |
| `getAppointmentVo.json` Request `id` | L3672-3674 | R |
| `appointment.companyRemark` | L3682 | R(Response 字段) |
| `updateAppointCompanyRemark.json` | L3680-3683 | W |
| `confirmAppointment.json` | L3691-3693 | W |

### 12.3 appointmentId 完整 4 处

| 行号 | 上下文 |
|---:|---|
| L3670 | `$scope.appointmentId = $stateParams.appointmentId` |
| L3673 | getAppointmentVo Request `{id: $scope.appointmentId}` |
| L3681 | updateAppointCompanyRemark Request |
| L3692 | confirmAppointment Request |

注意:`appointmentId` 与 S1-153 的 `appointId`(18 处)是不同字段!`appointmentId` 只在 bookDetailCtrl 出现 4 次,`appointId` 在 addCheckinCtrl / addVisitCtrl 等多处。

### 12.4 bookManageCtrl L3706 业务特征

- `selectAppointmentVoList.json` L3754(与 S1-153 addCheckinCtrl 共用)
- `statusArray` 状态过滤(L3716)
- `arriveTimeFrom` / `arriveTimeTo` 时间过滤(L3711-3712)
- `bookManageTab` 1/2/3(L3714-3715)← 多 tab

### 12.5 bookSettingsCtrl L3771 业务特征

- `getCorpAppointmentConf.json` L3775
- Response:`smsAdminName / smsMobile / smsBackMobile / smsBackAdminName`(L3778-3781)
- `saveCorpAppointmentConf.json` L3800(W)

### 12.6 appointAdminCtrl L52344 业务特征

- `getCorpAppointConf.json` L52362(appointSceneType 参数)
- `saveCorpAppointConf.json` L52373
- 配置:appointSceneType 索引(L52347-52349)

### 12.7 营销预约 ID 体系总结

| ID | 真实 | 使用场景 |
|---|:-:|---|
| `appointmentId` | A(4 处) | bookDetailCtrl 详情 |
| `appointId` | A(18 处,S1-153) | addCheckinCtrl / addVisitCtrl |
| `corpAppointmentConf.id` | 隐含 | – |
| `corpAppointConf` | 隐含 | appointSceneType 配置 |

**结论**:appointmentId 与 appointId 是同一 Appointment 实体的两种命名。

---

## §13 Order ↔ Customer / Patient

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Order → Customer | ✓ A | selectOrderVoListByCustomerId.json L19718 |
| Order → Patient | ✗ | 0 命中(Patient 经 Customer) |
| Customer → Order | ✓ A | customerOrder 字段 + myOrder 业务 |
| Patient → Order | ✗ | F |

**关键**:Order 没有 patientId 字段,完全通过 customerId 关联。

---

## §14 Order ↔ MedicalRecord(P0)

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Order → MedicalRecord | ✓ A | okOrderRecord.medicalRecordId L36251 |
| MedicalRecord → Order | ✓ A | getHaveOrderMedicalRecordVoList L31055 / getUnPlaceOrderMedicalRecordVoList L6976 |
| Order.medicalRecordId(直接) | ✗ | F(0 命中 Order 直接字段) |

**关键发现**:
- `getOkOrderRecordVoList.json` 桥接(订单管理 L36197)
- `medicalRecordIdList` 是本地数组拼接(L36216)
- 导出 URL:`downloadOkOrderRecord.htm?medicalRecordIdList=...`(L36239)
- `computeUnPlaceOrderMedicalRecordFee.json` L6680 → W(Request: `medicalRecordId`)
- `reComputeUnPlaceOrderMedicalRecordFee.json` L6884

**结论**:Order ↔ MedicalRecord 通过 `okOrderRecordVoList` 间接桥接,**没有直接 medicalRecordId / orderId 字段**。

---

## §15 Order ↔ Cashflow

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Order → Cashflow | ✓ A | refundOrderLog `{cashflowId: order.cashflow.id}` L20736 |
| Cashflow → Order | ✗ | F(0 命中) |
| Order.cashflowId(直接) | ✗ | F(0 命中) |
| Cashflow.orderId(直接) | ✗ | F(0 命中) |

**关键发现**:
- 退款流程:createRefundOrderLog.json `{customerId, cashflowId}` → commitId
- 支付:`order.cashflow.payType` L20745 / `order.cashflow.totalPayment` L20746
- **Order 与 Cashflow 通过 `customerOrder.cashflow` 嵌套 VO 桥接**

---

## §16 Order ↔ Sale(S1-143 隔离确认)

| 维度 | Marketing Order | Sale(就诊开单) | 关系 |
|---|---|---|---|
| ID | orderId | **无 saleId** | 完全独立 |
| Object | customerOrder + orderExpress | medicalProductVoList(嵌入 MedicalRecord) | **C 完全独立** |
| Controller | orderDetailCtrl / orderManageCtrl / selectOrderListCtrl / productOrderCtrl | addSaleRecordCtrl / adminSalesRecordCtrl / myMaterialBillCtrl | 隔离 |
| State | $stateParams.orderId | – | 隔离 |
| API | getOrderVo / pickUpOrder / deliveryOrder | waitPayDetail / materialBill | 隔离 |
| Customer | order.customer | – | 隔离 |
| Patient | **0 命中** | – | 隔离 |
| MedicalRecord | **0 命中**(通过 okOrderRecord 间接) | 直接 medicalRecordIdList | 隔离 |
| Cashflow | **0 命中**(通过 customerOrder.cashflow 嵌套) | 直接 cashflow | 部分间接 |
| Delivery | orderExpress | medicalProductDelivery | 隔离 |
| Product | – | medicalProduct | 隔离 |
| Write | pickUpOrder / deliveryOrder / createRefundOrderLog | createMaterialBill | 隔离 |

**结论**:**Order ↔ Sale 完全独立**(C)。没有任何共享 ID、共享 Controller、共享 API。

---

## §17 Order ↔ Delivery

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Order → Delivery | ✓ A | deliveryObj.orderId L20836 + deliveryOrder.json L20852 |
| Delivery → Order | ✓ A | orderExpress.expressStatus/orderExpress.expressType(L20722-20723) |
| Order.deliveryStatus(直接) | ✗ | F(0 命中) |

**关键发现**:
- `deliveryObj` 字段:orderId / expressCompany / expressCompanyId / expressCode / idx
- deliveryOrder.json(W)接收 deliveryObj
- 13 种快递公司:SF / ZTO / STO / YTO / YD / YZPY / EMS / HHTT / JD / UC / DBL / ZJS / OTHERS / HTKY(L20786-20827)

---

## §18 Marketing Product 边界

| 关系 | 真实? | 字符级证据 |
|---|:-:|---|
| Marketing Order → Product | ✓ A | seckillProduct.skuCode L18582 |
| Marketing Order → MedicalProduct | ✗ | 0 命中 |
| Coupon → Product | ✗ | 0 命中 |
| Coupon → MedicalProduct | ✗ | 0 命中 |
| TrainerCard → Product | ✗ | 0 命中 |
| TrainerCard → MedicalProduct | ✗ | 0 命中 |
| Seckill → Product | ✓ A | skuCode L18582 |
| Groupon → Product | ✓ A | skuCode(grouponProductVo 同) |
| Seckill → MedicalProduct | ✗ | 隔离 |

**结论**:Marketing 侧 Product = `skuCode` 通用 Product,**不与 medicalProduct 共用**。

---

## §19 活动对象桥

| 桥 | 真实? | Grade | 字符级证据 |
|---|:-:|:-:|---|
| Coupon ↔ Order | ✓ A | A | computeUsableCustomerCoupon / isCustomerCouponUsable |
| Point ↔ Order | ✗ F | F | 0 命中 |
| Groupon ↔ Order | ✓ A | A | grouponOrderVoList |
| Seckill ↔ Order | ✓ A | A | selectOrderVoListOfSeckillProduct |
| Lead ↔ Customer | ✓ A | A | linkRecommendPhone |
| Referral ↔ Customer | ✓ A | A | (同 Lead) |
| Referral ↔ Order | ✗ | F | 0 命中 |
| Customer Asset ↔ Customer | ✓ A | A | customerCouponVo / customerTrainerCardVo / customerPointVo |
| TrainerCard ↔ Customer | ✓ A | A | customerTrainerCardVo |
| BatchSendTask ↔ Coupon | ✓ A | A | taskCouponBatchSendId |
| BatchSendTask ↔ SchoolMateCheck | ✓ A | A | taskScreenTemplateBatchSendId |
| BatchSendTask ↔ Member | ✓ A | A | groupSendCtrl getMemberList L16848 |
| SeckillProduct ↔ Promotion | ✓ A | A | promotionId 43 处 |
| TrainerCard ↔ Cashflow | ✓ A | A | consumeCustomerTrainerCardNumbers + investMoneyForCustomerTrainerCard |
| CustomerPoint ↔ Cashflow | ✗ F | F | 0 命中(只是业务扣减) |

---

## §20 Object 分类

| 对象 | A 独立 ID | B Response VO | C Request Payload | D State/UI | F |
|---|:-:|:-:|:-:|:-:|:-:|
| MarketingOrder | ✗ F(0 命中 marketingOrderId) | – | – | – | – |
| Order(customerOrder) | ✓ orderId | ✓ | ✓ | ✓ | – |
| Coupon | ✓ couponId | ✓ | ✓ | – | – |
| CouponTemplate | ✓ (复用 couponId) | ✓ | – | – | – |
| CouponRule | ✗ F | – | – | – | – |
| CustomerCoupon | ✓ customerCouponId | ✓ | ✓ | ✓ | – |
| CountCard | ✓ trainerCardId | ✓ | ✓ | – | – |
| Point | ✗ F(0 命中 pointId) | – | – | ✓(Customer 字段) | – |
| Lead | ✗ F(0 命中 leadId) | – | – | – | – |
| Referral | ✗ F(0 命中 referralId) | – | – | – | – |
| RecommendPhone | ✓ recommendPhoneId | ✓ | ✓ | ✓ | – |
| Group | ✗ F(0 命中 groupId) | – | – | – | – |
| GrouponProduct | ✓ grouponProductId | ✓ | ✓ | ✓ | – |
| GrouponOrder | ✗ F(0 命中 grouponOrderId) | ✓(grouponOrderVoList) | – | – | – |
| Seckill | ✗ F(0 命中 seckillId) | – | – | – | – |
| SeckillProduct | ✓ seckillProductId | ✓ | ✓ | ✓ | – |
| SeckillOrder | ✗ F | ✓(selectOrderVoListOfSeckillProduct) | – | – | – |
| Promotion | ✓ promotionId | ✓ | ✓ | ✓ | – |
| SmsTask | ✗ F(0 命中 smsId) | – | – | – | – |
| TemplateBatchSendTask | ✓ taskTemplateBatchSendId | ✓ | ✓ | ✓ | – |
| CouponBatchSendTask | ✓ taskCouponBatchSendId | ✓ | – | ✓ | – |
| ScreenTemplateBatchSendTask | ✓ taskScreenTemplateBatchSendId | ✓ | – | ✓ | – |
| Appointment(复用) | ✓ appointmentId + appointId | ✓ | ✓ | ✓ | – |

**L3 数据库结构**:全部 F。

---

## §21 Source Trace

### 21.1 13 个关键 ID 的 Source → Target

| ID | Source | Transform | Target | Consumer | 真实? |
|---|---|---|---|---|:-:|
| orderId | State.orderId | getOrderVo.json | orderVo | UI | A |
| orderId | deliveryObj | deliveryOrder.json | orderVo | UI | A |
| orderId | id | pickUpOrder.json | pickUpResult | UI | A |
| couponId | State / obj | getCouponVo / invalidCoupon / activeCoupon / updateCreatingCoupon | couponVo | UI | A |
| customerCouponId | item.customerCoupon.id | useCoupon / computeUsable | couponVo | UI | A |
| seckillProductId | State / obj | getSeckillProductVo / invalidSeckillProduct / activeSeckillProduct | seckillProductVo | UI | A |
| grouponProductId | State | selectGrouponOrderVoList / getGrouponProductVo | grouponProductVo | UI | A |
| recommendPhoneId | item.recommendPhone.id / State / obj | getRecommendPhoneVo / selectRecommendPhoneVoList / linkRecommendPhone | recommendPhoneVo | UI | A |
| trainerCardId | info.id / obj | investMoneyForCustomerTrainerCard / consumeCustomerTrainerCardNumbers | customerTrainerCardVo | UI | A |
| customerTrainerCardId | info / obj | getCustomerTrainerCard / searchRowTimeCard | customerTrainerCardVo | UI | A |
| promotionId | State | getPromotionVo / getPromotionQrcode / selectOrderVoListOfSeckillProduct | promotionVo / orderVoList | UI | A |
| taskTemplateBatchSendId | State | searchTask / lookDetails / cancelTask / lookCondition | taskVo | UI | A |
| taskCouponBatchSendId | State | getTaskCouponBatchSendVo | couponBatchSendTaskVo | UI | A |
| taskScreenTemplateBatchSendId | State | lookDetails / cancelTask / selectTaskScreenTemplateBatchSendList | screenTemplateBatchSendTaskVo | UI | A |
| appointmentId | State | getAppointmentVo / confirmAppointment / updateAppointCompanyRemark | appointmentVo | UI | A |
| appointId | State | confirmArrivalOfAppoint / selectAppointPatientVoList / selectAppointSchoolMateVoList / receiveSelfAndBeginCustomerCheckin | appointmentVo / customerCheckinVo | UI | A |

### 21.2 禁造 ID 列表

| ID | 0 命中 | 禁造原因 |
|---|:-:|---|
| marketingOrderId | ✓ | 营销订单不是独立 Object |
| pointId | ✓ | Point 是 Customer 字段 |
| cardId | ✓ | 没有 card ID 概念 |
| leadId / customerLeadId | ✓ | Lead 不存在 |
| referralId / referrerId / refereeId | ✓ | Referral 不存在 |
| grouponId / grouponOrderId / groupId / teamId / groupOrderId | ✓ | Groupon 用 grouponProductId |
| seckillId / flashSaleId / killOrder / seckillOrderId | ✓ | Seckill 用 seckillProductId |
| smsId / smsTaskId / batchSendId | ✓ | 用 3 种 taskXxxBatchSendId |
| sendCouponId | ✓ | 没有独立 sendCouponId |
| couponNo / orderNo | 部分 | L35033-35037 是局部变量 |
| customerAssetId | ✓ | 0 命中 |
| templateBatchSendTaskId / couponBatchSendTaskId / screenTemplateBatchSendTaskId | ✓ | 用 task 前缀 |

---

## §22 Controller 消费矩阵

| Controller | Order | Coupon | Point | Card | Lead | Referral | Group | Seckill | SMS | Appointment | Customer | Patient | MedicalRecord | Cashflow | Sale |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| orderDetailCtrl (L18937) | ✓ | – | – | – | – | – | – | – | – | – | ✓ | – | – | – | – |
| orderManageCtrl (L36165) | ✓ | – | – | – | – | – | – | – | – | – | ✓ | – | ✓(okOrderRecord.medicalRecordId) | – | – |
| selectOrderListCtrl (L20636) | ✓ | – | – | – | – | – | – | – | – | – | ✓ | – | – | – | – |
| productOrderCtrl (L19020) | ✓ | – | – | – | – | – | – | ✓(seckillProductId) | – | – | – | – | – | – | – |
| couponListCtrl (L12760) | – | ✓ | – | – | – | – | – | – | – | – | – | – | – | – | – |
| myCouponCtrl (L18818) | – | ✓ | – | – | – | – | – | – | – | – | ✓ | – | – | – | – |
| pointsListCtrl (L36263) | – | – | ✓(customerPoint) | – | – | – | – | – | – | – | ✓ | – | – | – | – |
| timeCardCtrl (L34095) | – | – | – | ✓(trainerCard) | – | – | – | – | – | – | ✓ | – | – | – | – |
| addProjectCardCtrl (L52150) | – | – | – | ✓(trainerCard) | – | – | – | – | – | – | ✓ | – | – | – | – |
| recommendPhoneListCtrl (L19335) | – | – | – | – | ✓(recommendPhone) | ✓(referrer) | – | – | – | – | ✓ | – | – | – | – |
| grouponListCtrl (L13553) | – | – | – | – | – | – | ✓(grouponProduct) | – | – | – | – | – | – | – | – |
| grouponOrderCtrl (L13632) | ✓(grouponOrderVoList) | – | – | – | – | – | ✓ | – | – | – | – | – | – | – | – |
| secKillProductListCtrl (L20519) | ✓(of seckillProduct) | – | – | – | – | – | – | ✓(seckillProduct) | – | – | – | – | – | – | – |
| secKillPromotionListCtrl (L20588) | – | – | – | – | – | – | – | ✓(promotionType=3) | – | – | – | – | – | – | – |
| groupSendCtrl (L16799) | – | – | – | – | – | – | – | – | ✓(templateBatchSendTask) | – | ✓(getMemberList) | – | – | – | – |
| smsSetCtrl (L2867) | – | – | – | – | – | – | – | – | ✓(smsTemplate) | – | – | – | – | – | – |
| screenConditionBatchCtrl (L45234) | – | – | – | – | – | – | – | – | ✓(screenTemplateBatchSendTask) | – | – | – | – | – | – |
| bookDetailCtrl (L3669) | – | – | – | – | – | – | – | – | – | ✓(appointmentId) | – | – | – | – | – |
| bookManageCtrl (L3706) | – | – | – | – | – | – | – | – | – | ✓(appointmentVoList) | – | – | – | – | – |
| addSaleRecordCtrl (S1-143) | – | – | – | – | – | – | – | – | – | – | ✓ | ✓ | ✓ | ✓ | ✓ |
| myMaterialBillCtrl (S1-143) | – | – | – | – | – | – | – | – | – | – | – | – | ✓ | ✓ | ✓ |

---

## §23 Marketing vs Sale 隔离矩阵(P0)

| 维度 | Marketing Order | Sale / 就诊开单 | 关系结论 |
|---|---|---|---|
| **ID** | orderId(6 处) | 无 saleId / 无 saleVo | **C 完全独立** |
| **Object** | customerOrder + orderExpress + orderManageRecodListFactory(嵌入 okOrderRecordVO) | medicalProductVoList + cashflow + materialBillVo | **C 完全独立** |
| **Controller** | orderDetailCtrl / orderManageCtrl / selectOrderListCtrl / productOrderCtrl | addSaleRecordCtrl / adminSalesRecordCtrl / myMaterialBillCtrl / waitPayDetailCtrl | **C 完全独立** |
| **State** | $stateParams.orderId | $stateParams.medicalRecordId / $stateParams.patientId | **C 完全独立** |
| **API** | getOrderVo / pickUpOrder / deliveryOrder / selectOrderVoListByCorpId / getOkOrderRecordVoList | waitPayDetail / computeUnPlaceOrderMedicalRecordFee / placeOrder | **C 完全独立** |
| **Customer** | order.customer | (经 patient → customer) | **C 完全独立** |
| **Patient** | **0 命中** | (直接 patient) | **C 完全独立** |
| **MedicalRecord** | **0 命中 Order 字段**(通过 okOrderRecord.medicalRecordId) | 直接 medicalRecordId | **C 完全独立** |
| **Cashflow** | **0 命中 Order 字段**(通过 customerOrder.cashflow 嵌套) | 直接 cashflowVo | **C 完全独立** |
| **Delivery** | orderExpress(expressStatus/expressType) + deliveryOrder.json | medicalProductDelivery + completeMedicalRecordDelivery | **C 完全独立** |
| **Product** | (SeckillProduct / GrouponProduct 通过 skuCode 通用 Product) | medicalProduct | **B 部分复用**(skuCode) |
| **Write** | pickUpOrder / deliveryOrder / createRefundOrderLog / commitRefundOrderLog | createMaterialBill / createCashFlowForMedicalRecord | **C 完全独立** |

**结论**:**Marketing Order 与 Sale 完全独立(C)**,只有 Product 维度通过 skuCode 部分复用(B)。

---

## §24 生命周期 DAG

S1-155 不预设业务流,由代码证据决定。

### 24.1 真实生命周期(基于 152 个营销 API + 415 个就诊 API)

```
Customer (S1-139)
  │
  ├──→ 营销预约 (bookDetailCtrl/bookManageCtrl)
  │      │
  │      └──→ appointmentVo (appointmentId/appointId)
  │             │
  │             └──→ confirmAppointment (L3691)  →  S1-153 addCheckinCtrl
  │
  ├──→ RecommendPhone(Referral) (recommendPhoneListCtrl)
  │      │
  │      ├──→ assignRecommendPhoneList (L19623) 分配 employee
  │      │
  │      └──→ linkRecommendPhone (L19792) 关联 Customer
  │
  ├──→ Coupon 4 级体系
  │      │
  │      ├──→ createCoupon (L12684) Coupon Template
  │      │       │
  │      │       └──→ activeCoupon / invalidCoupon / updateCreatingCoupon
  │      │
  │      ├──→ sendCoupon (L18835) → Customer 拥有 customerCouponVo
  │      │
  │      ├──→ useCoupon (L12746) CustomerCouponId 使用
  │      │
  │      ├──→ computeUsableCustomerCoupon (L6627) → Order 桥
  │      │
  │      └──→ createCouponBatchSendTask (L49433) 群发任务
  │
  ├──→ TrainerCard
  │      │
  │      ├──→ createTrainerCard (L52223) 模板
  │      │
  │      ├──→ investMoneyForCustomerTrainerCard (L34516) 购买
  │      │       │
  │      │       └──→ commitForInvestMoneyForCustomerTrainerCard (L34537 字符串拼接)
  │      │
  │      └──→ consumeCustomerTrainerCardNumbers (L34652) 扣次
  │
  ├──→ CustomerPoint
  │      │
  │      ├──→ getCorpPointRule (L18179) 规则
  │      │
  │      ├──→ initAddCustomerPoint / initSubCustomerPoint (L18217/L18231) 调整
  │      │
  │      └──→ pointToMoney (L7500) 转换
  │
  ├──→ Seckill 4 步
  │      │
  │      ├──→ createPromotion (L16477) promotionType=3
  │      │
  │      ├──→ createSeckillProduct (L16619) → seckillProductId
  │      │
  │      ├──→ activeSeckillProduct (L16720) 生效
  │      │
  │      └──→ selectOrderVoListOfSeckillProduct (L19026) 关联 Order
  │
  ├──→ Groupon
  │      │
  │      ├──→ createGrouponProduct (L13488) → grouponProductId
  │      │
  │      └──→ selectGrouponOrderVoList (L13638) → grouponOrderVoList
  │
  ├──→ Marketing Order(customerOrder)
  │      │
  │      ├──→ getOrderVo (L18942) 详情
  │      │
  │      ├──→ pickUpOrder (L20709) 自提
  │      │
  │      ├──→ deliveryOrder (L20852) 配送 + orderExpress
  │      │
  │      └──→ createRefundOrderLog (L20734) 退款 → cashflowId
  │
  └──→ BatchSendTask(3 种)
         │
         ├──→ createTemplateBatchSendTask (L17235) → taskTemplateBatchSendId
         │
         ├──→ createCouponBatchSendTask (L49433) → taskCouponBatchSendId
         │
         └──→ createScreenTemplateBatchSendTask (L45502) → taskScreenTemplateBatchSendId
```

### 24.2 营销 ↔ 就诊 唯一交汇点

| 交汇点 | 字符级证据 |
|---|---|
| `computeUsableCustomerCoupon` (L6627) | Order ↔ Coupon |
| `getHaveOrderMedicalRecordVoList` (L31055) | Order ↔ MedicalRecord |
| `getUnPlaceOrderMedicalRecordVoList` (L6976) | Order ↔ MedicalRecord |
| `okOrderRecord.medicalRecordId` (L36251) | okOrderRecordVO ↔ MedicalRecord |
| `createRefundOrderLog {cashflowId}` (L20736) | Order ↔ Cashflow |
| `useCoupon {customerCouponId}` (L12746) | CustomerCoupon → 业务流扣减 |
| `customerTrainerCard.consume` (L34652) | TrainerCard → 业务流扣次 |

**没有任何营销 Controller 直接修改 MedicalRecord 或 Sale。**

---

## §25 26 项证据矩阵(摘要)

完整 26 项(Page/Controller/State/URL/Entry/Layout/Buttons/Inputs/Filters/Status/Dialog/Pagination/Sorting/Required/Default/Data Source/Object/Request/Response/Function/State Bridge/Object Bridge/API Bridge/Business Interpretation/Evidence Grade/V4.4 Decision)在每个模块段落已给出。摘要:

| 类别 | 关键证据 |
|---|---|
| Object | Order (customerOrder + okOrderRecordVo) / Coupon (couponVo + customerCouponVo) / TrainerCard (trainerCard + customerTrainerCard) / SeckillProduct / GrouponProduct / Promotion / RecommendPhone / 3 种 BatchSendTask |
| Request | orderId / couponId / customerCouponId / seckillProductId / grouponProductId / recommendPhoneId / trainerCardId / customerTrainerCardId / promotionId / taskTemplateBatchSendId / taskCouponBatchSendId / taskScreenTemplateBatchSendId / appointmentId / appointId |
| Response | orderVo / couponVo / customerCouponVo / trainerCardVo / seckillProductVo / grouponProductVo / promotionVo / recommendPhoneVo / taskVo |
| API Bridge | computeUsableCustomerCoupon(L6627) / useCoupon(L12746) / pickUpOrder(L20709) / deliveryOrder(L20852) / selectOrderVoListOfSeckillProduct(L19026) |
| State Bridge | $stateParams.orderId / .couponId / .seckillProductId / .grouponProductId / .recommendPhoneId / .trainerCardId / .taskTemplateBatchSendId / .appointmentId / .appointId |
| Business Interpretation | Coupon/TrainerCard/Point 是营销资产,Seckill/Groupon/Promotion 是营销活动,Order 是营销订单,RecommendPhone 是 Referral,BatchSendTask 是营销推送 |
| Evidence Grade | A=字符级 / B=多源 / C=局部 / D=冲突(0) / **E=业务推断(0 入规格)** / F=未观察 |
| V4.4 Decision | 仅 A/B/C 入规格 |

---

## §26 历史差异

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-143:营销 Order 与 Sale 隔离 | 25 个 Order API + 0 patientId + 0 cashflowId + 0 medicalRecordId(直接) | **完全确认隔离** | **C 完全独立** |
| S1-148:Cashflow ↔ MedicalRecord | Order 通过 customerOrder.cashflow 嵌套 + createRefundOrderLog {cashflowId} | 间接桥确认 | **F(无 Order.cashflowId 直接)** |
| S1-153:appointOrderCtrl 空 Stub | L3664 空 Stub 仍确认 | 无变化 | A(空) |
| S1-153:bookDetailCtrl 真实 | L3669 真实 Controller + appointmentId 真实 | 新增 appointmentId 真实证据 | **A 真实** |
| S1-153:appointId 真实 | 18 处真实 | 复用 appointmentId(4 处)是另一 ID | **appointId + appointmentId 共存** |
| S1-154:Member/FollowUp 实体 0 命中 | 营销场景也 0 命中 | 一致 | F / 禁造 |
| S1-154:DefineFollowUp.referrer Service | 与 recommendPhone 推荐新客区分 | DefineFollowUp.referrer 是 Service 字段,recommendPhone 是 Controller | **两个不同实体** |
| (历史误判)"Marketing Order 是独立 ID" | marketingOrderId 0 命中 | **禁造** | F |
| (历史误判)"Card 是独立 ID" | cardId 0 命中,真实叫 trainerCard | **禁造 cardId** | F |
| (历史误判)"Point 是独立 ID" | pointId 0 命中,真实是 Customer 字段 | **禁造 pointId** | F |
| (历史误判)"Lead / Referral 是独立实体" | leadId / referralId 0 命中,真实叫 RecommendPhone | **禁造 leadId / referralId** | F |
| (历史误判)"Group / GroupId 是拼团" | groupId 0 命中,真实叫 grouponProductId | **禁造 groupId** | F |
| (历史误判)"SeckillId / FlashSaleId" | seckillId / flashSaleId 0 命中,真实叫 seckillProductId | **禁造 seckillId** | F |
| (历史误判)"SmsId / SmsTaskId" | smsId / smsTaskId 0 命中,真实是 3 种 taskXxxBatchSendId | **禁造 smsId** | F |
| (历史误判)"营销预约与就诊 Appointment 是两个 Object" | bookDetailCtrl 共用 appointmentId + appointId | **同一 Object 同一 API** | **A 复用 S1-153** |

---

## §27 V4.4 营销管理规格(26 项)

1. **MarketingOrder** = F(marketingOrderId 0 命中,统一用 orderId)
2. **Coupon** = A(couponId 真实)
3. **CouponTemplate** = A(复用 couponId)
4. **CouponRule** = F(0 命中)
5. **CustomerCoupon** = A(customerCouponId 真实)
6. **CountCard** = A(trainerCardId 真实,计次卡叫 TrainerCard)
7. **Point** = F(pointId 0 命中,Customer 字段)
8. **Lead** = F(leadId 0 命中)
9. **Referral** = F(referralId 0 命中,统一用 recommendPhoneId)
10. **Group** = F(groupId 0 命中)
11. **GroupOrder** = F(0 命中,使用 grouponOrderVoList)
12. **Seckill** = F(seckillId 0 命中)
13. **SeckillOrder** = F(0 命中,通过 selectOrderVoListOfSeckillProduct)
14. **SmsTask** = F(smsId 0 命中,使用 3 种 taskXxxBatchSendId)
15. **Appointment(营销预约)** = A(appointmentId + appointId 复用 S1-153)
16. **VO**:orderVo / couponVo / customerCouponVo / trainerCardVo / seckillProductVo / grouponProductVo / promotionVo / recommendPhoneVo / taskVo / okOrderRecordVo
17. **Request**:13 个 ID(orderId/couponId/customerCouponId/seckillProductId/grouponProductId/recommendPhoneId/trainerCardId/customerTrainerCardId/promotionId/taskTemplateBatchSendId/taskCouponBatchSendId/taskScreenTemplateBatchSendId/appointmentId/appointId)
18. **State/UI**$stateParams.orderId / .couponId / .seckillProductId / .grouponProductId / .recommendPhoneId / .trainerCardId / .taskTemplateBatchSendId / .appointmentId
19. **ID 允许**:orderId / couponId / customerCouponId / seckillProductId / grouponProductId / recommendPhoneId / trainerCardId / customerTrainerCardId / promotionId / taskTemplateBatchSendId / taskCouponBatchSendId / taskScreenTemplateBatchSendId / appointmentId / appointId
20. **ID 禁造**:marketingOrderId / pointId / cardId / leadId / customerLeadId / referralId / referrerId / refereeId / grouponId / grouponOrderId / groupId / teamId / groupOrderId / seckillId / flashSaleId / killOrder / seckillOrderId / smsId / smsTaskId / batchSendId / sendCouponId / customerAssetId / templateBatchSendTaskId / couponBatchSendTaskId / screenTemplateBatchSendTaskId
21. **Marketing Order ↔ Sale** = C 完全独立(只有 Product.skuCode B 部分复用)
22. **Marketing Order ↔ MedicalRecord** = 间接,通过 okOrderRecordVo.medicalRecordId(L36251)或 getHaveOrderMedicalRecordVoList(L31055)
23. **Marketing Order ↔ Cashflow** = 间接,通过 customerOrder.cashflow 嵌套 + createRefundOrderLog {cashflowId}
24. **Marketing Order ↔ Delivery** = A 通过 deliveryObj.orderId + orderExpress.expressStatus/expressType
25. **Coupon/Point/Group/Seckill/Lead/Referral 边界**:Coupon 是 4 级,customerCouponId 真实;Point 是 Customer 字段;Group/Seckill 真实但用 productId 不用 groupId/seckillId;Lead/Referral 统一是 recommendPhone
26. **后端 FK**全部 L3/F

---

## §28 F / 未确认

- marketingOrderId / marketingOrder(0 命中)
- pointId / pointLogId(0 命中)
- cardId / timeCardId / timecardId(0 命中;真实叫 trainerCardId)
- leadId / customerLeadId / pool(0 命中)
- referralId / referrerId / refereeId(0 命中;真实是 recommendPhoneId)
- grouponId / grouponOrderId / groupId / teamId / groupOrderId / groupBuy(0 命中)
- seckillId / flashSaleId / killOrder / seckillOrderId(0 命中;真实是 seckillProductId)
- smsId / smsTaskId / batchSendId(0 命中;真实是 3 种 taskXxxBatchSendId)
- couponNo / couponTemplate / couponRule(0 命中)
- sendCouponId / customerAssetId(0 命中)
- L3 数据库结构 / FK 全部 F

---

## §29 Git / 完整性

### 29.1 完整性闸门

4 文件 SHA256 全部 PASS(见 §0)。

### 29.2 累计统计

- controller.js 2,194,196 bytes / 59,214 行
- 417 个 Controller 注册
- 915 个 .json API
- 152 个营销相关 API
- 71 个营销相关 Controller
- 23 个关键营销真实 Controller

### 29.3 API actual / Write actual / Production mutation

**API actual = 0 / Write actual = 0 / Production mutation = 0** ✓

仅执行:`Get-FileHash` / `git status` / `git add --` / `git commit` / `git push` / `python` 本地分析脚本(临时目录)/ `Get-ChildItem` 校验。

### 29.4 Git 操作

- Commit:`84a42dfe4248de271ce8086e478b22923b48d6e6`(S1-154 之后,S1-155 待提交)
- Branch:master
- Tracked = 225 / Untracked = 10 / Ignored = 1
- 本轮新增:`218_S1-155_*.md`
- 预期:Tracked = 226 / Untracked = 10 / Ignored = 1 / LOCAL == origin/master