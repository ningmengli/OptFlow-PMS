# S1-159 全局核心 Object / ID / API / Write / State 交叉一致性审计

> **收口轮次**:S1-128 ~ S1-158 共 32 份历史 MD 文档交叉一致性审计。
>
> 本轮**不**以单页面扫描为主,而是:**全局去重 + 冲突定位 + 最终 ID / API / Write Allowlist & Denylist 冻结**。
>
> 全部结论以当前 controller.js 字符级证据为准;历史 MD 中的过时被本轮纠偏,但**不修改历史文档**。

---

## §0 完整性闸门

| 文件 | 期望 SHA256 | 实际 SHA256 | 状态 |
|---|---|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | ✓ PASS |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | ✓ PASS |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | ✓ PASS |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | ✓ PASS |

**闸门结论:4 文件 SHA256 全部一致,通过。**

文件规模:2,142,219 bytes / **59,214 行** / 417 个 Controller 注册 / **915 个 .json API**。

---

## §1 历史文档索引(S1-128 ~ S1-158 共 32 份)

### 1.1 S1-128(前置):医疗产品全局 Provenance

- `190_S1-128_medicalProduct全局Provenance跨模块数据链审计.md`

### 1.2 S1-129 ~ S1-134(局部逆向)

| 文档 | S1 任务 | 主题 |
|---|---|---|
| 191 | S1-129 | medicalProduct / Machine / Delivery 加工链深度 |
| 192 | S1-130 | 诊所管理 / 系统设置边界 |
| 193 | S1-131 | 权限 / 角色 / 员工 / 公司 / 诊所身份 |
| 194 | S1-132 | 筛查机构 / schoolId |
| 195 | S1-133 | SchoolMate ↔ Patient / Customer / MedicalRecord |
| 196 | S1-134 | SchoolMate → Appointment 入口汇合链 |

### 1.3 S1-135 ~ S1-158(全业务域总审计,共 24 份)

| 文档 | S1 任务 | 主题 |
|---|---|---|
| 197 | S1-135 | CustomerCheckin → MedicalRecord 主入口链 |
| 198 | S1-136 | MedicalRecord → Check/Optometry/Sale/Charge 主业务分流 |
| 199 | S1-137 | MedicalRecord 多入口 + medicalRecordType |
| 200 | S1-137R | MedicalRecord 主链纠偏(关键) |
| 201 | S1-138 | MedicalRecord 多创建路径 + 状态机 |
| 202 | S1-139 | Patient / Customer / MedicalRecord 身份 |
| 203 | S1-140 | Customer ↔ Patient 直接桥 |
| 204 | S1-141 | Cashflow / Charge 收费生命周期 |
| 205 | S1-142 | Delivery 全生命周期 |
| 206 | S1-143 | Sale 就诊开单边界 |
| 207 | S1-144 | Check / Optometry 与 medicalRecordType 分支 |
| 208 | S1-145 | MedicalExamine / VisionRecord / MethodGlassRecord / MedicalProduct |
| 209 | S1-146 | MedicalRecord 核心主对象 |
| 210 | S1-147 | Customer / Patient / CustomerCheckin 身份链 |
| 211 | S1-148 | Cashflow / Charge / Payment / Refund |
| 212 | S1-149 | Product / SKU / MedicalProduct / Stock 物资域 |
| 213 | S1-150 | MachineCenter / MachineOrder / MachineProcessing |
| 214 | S1-151 | Clinic / Company / Shop / Department / Employee / Role / SystemSetting |
| 215 | S1-152 | School / SchoolMate / SchoolMateCheck / Screening |
| 216 | S1-153 | Appointment / 预约排班 / 叫号 / 诊室屏 |
| 217 | S1-154 | CustomerFollowUp / Member / FollowUp 患者维护 |
| 218 | S1-155 | Marketing / Order / Coupon / Point / Group / Seckill / Lead / Referral |
| 219 | S1-156 | DataReport / Statistics / Print / Export |
| 220 | S1-157 | SystemSetting 子模块逐页面 |
| 221 | S1-158 | 诊所管理子模块 |

---

## §2 Object 去重

### 2.1 候选 Object 总表(基于历史 + 当前源码)

| 候选 Object | A 独立 ID | B VO/Payload | C State | D 误导 | F 未观察 | 当前最终结论 |
|---|:-:|:-:|:-:|:-:|:-:|---|
| **MedicalRecord** | ✓ medicalRecordId(161) | ✓ | ✓ | – | – | **A 真实核心** |
| **Customer** | ✓ customerId(128) | ✓ | ✓ | – | – | **A 真实核心** |
| **Patient** | ✓ patientId(89) | ✓ | ✓ | – | – | **A 真实核心** |
| **CustomerCheckin** | ✓ customerCheckinId(19) | ✓ | ✓ | – | – | **A 真实核心** |
| **Cashflow** | ✓ cashflowId(73) | ✓ | ✓ | – | – | **A 真实核心** |
| **PrintCheckin** | ✓ printCheckinId(9) | ✓ | ✓ | – | – | **A 真实**(S1-148)|
| **Product** | ✓ productId(42) | ✓ | ✓ | – | – | **A 真实核心** |
| **SKU** | ✓ skuId(85) + productSkuId(69) | ✓ | ✓ | – | – | **A 真实核心** |
| **MedicalProduct** | ✓ medicalProductId(20) | ✓ | ✓ | – | – | **A 真实核心** |
| **Stock** | ✓ stockInSkuId(60) | ✓ | ✓ | – | – | **A 真实核心** |
| **Supplier** | ✓ supplierId(99) | ✓ | ✓ | – | – | **A 真实核心** |
| **mainSupplier** | ✓ mainSupplierId(25) | ✓ | ✓ | – | – | **A 真实**(Stock 内嵌)|
| **MachineCenter** | ✓ machineCenterId(18) | ✓ | ✓ | – | – | **A 真实核心** |
| **MachineCenterOrder** | ✓ machineCenterOrderId(7) | ✓ | ✓ | – | – | **A 真实核心** |
| **ConsultRoom** | ✓ consultRoomId(22) | ✓ | ✓ | – | – | **A 真实核心** |
| **Appointment** | ✓ appointId(18) + appointmentId(4) | ✓ | ✓ | – | – | **A 真实核心** |
| **BigScreen** | ✓ bigScreenId(14) | ✓ | ✓ | – | – | **A 真实** |
| **School** | ✓ schoolId(205) | ✓ | ✓ | – | – | **A 真实核心** |
| **SchoolClass** | ✓ classId(131) | ✓ | ✓ | – | – | **A 真实核心** |
| **SchoolMate** | ✓ schoolMateId(19) | ✓ | ✓ | – | – | **A 真实核心** |
| **SchoolMateCheck** | ✓ schoolMateCheckId(16) | ✓ | ✓ | – | – | **A 真实核心** |
| **FollowUp** | ✓ followUpId(20) | ✓ | ✓ | – | – | **A 真实** |
| **CustomerOrder** | ✓ orderId(6) | ✓ | ✓ | – | – | **A 真实** |
| **Coupon** | ✓ couponId(9) | ✓ | ✓ | – | – | **A 真实核心** |
| **CustomerCoupon** | ✓ customerCouponId(17) | ✓ | ✓ | – | – | **A 真实核心** |
| **RecommendPhone(Referral)** | ✓ recommendPhoneId(12) | ✓ | ✓ | – | – | **A 真实** |
| **GrouponProduct** | ✓ grouponProductId(6) | ✓ | ✓ | – | – | **A 真实** |
| **SeckillProduct** | ✓ seckillProductId(14) | ✓ | ✓ | – | – | **A 真实** |
| **Promotion** | ✓ promotionId(43) | ✓ | ✓ | – | – | **A 真实** |
| **TrainerCard(计次卡)** | ✓ trainerCardId(5) | ✓ | ✓ | – | – | **A 真实核心** |
| **CustomerTrainerCard** | ✓ customerTrainerCardId(15) | ✓ | ✓ | – | – | **A 真实** |
| **Company** | ✓ companyId(102) | ✓ | ✓ | – | – | **A 真实核心** |
| **Employee** | ✓ employeeId(35) | ✓ | ✓ | – | – | **A 真实核心** |
| **Admin** | ✓ adminId(21) | ✓ | ✓ | – | – | **A 真实** |
| **AdminRole** | ✓ adminRoleId(29) | ✓ | ✓ | – | – | **A 真实** |
| **Role(generic)** | ✓ roleId(4) | ✓ | ✓ | – | – | **A 真实** |
| **Department** | ✓ departmentId(1,弱) | ✓ | ✓ | – | – | **A 弱**(仅 id 弱命中)|
| **CompanyCashConf** | ✓ companyCashConfId(3) | ✓ | ✓ | – | – | **A 真实** |
| **CorpTypeConf** | ✓ corpTypeId(2) | ✓ | ✓ | – | – | **A 真实** |
| **Examine** | ✓ examineId(24) | ✓ | ✓ | – | – | **A 真实**(S1-158 新发现)|
| **BodyCheckItem** | ✓ bodyCheckItemId(4) | ✓ | ✓ | – | – | **A 真实** |
| **MedicalCheckItem** | ✓ medicalCheckItem.id | ✓ | ✓ | – | – | **A 真实**(S1-158 新发现)|
| **TemplateBatchSendTask** | ✓ taskTemplateBatchSendId(11) | ✓ | ✓ | – | – | **A 真实** |
| **CouponBatchSendTask** | ✓ taskCouponBatchSendId(3) | ✓ | ✓ | – | – | **A 真实** |
| **ScreenTemplateBatchSendTask** | ✓ taskScreenTemplateBatchSendId(9) | ✓ | ✓ | – | – | **A 真实** |
| **fundusCheckRecord** | ✗(0 命中 fundusCheckRecordId)| ✓ fundusCheckRecord.h5 | ✓ | – | – | **B**(S1-156)|
| **corpReportConf** | ✗(0 命中 corpReportConfId)| ✓ | ✓ | – | – | **B**(S1-156)|
| **corpAppointmentConf** | ✗(0 命中 corpAppointmentConfId)| ✓ | ✓ | – | – | **B**(S1-153)|
| **corpAppointConf** | ✗(0 命中 corpAppointConfId)| ✓ | ✓ | – | – | **B**(S1-153)|
| **corpPointRule** | ✗(0 命中 corpPointRuleId)| ✓ | ✓ | ✓ | – | **B**(S1-155)|
| **CustomerPoint** | ✗(0 命中 pointId)| ✓(Customer 字段) | ✓ | – | – | **C**(S1-155)|
| **CustomerWallet** | ✗(0 命中 walletId)| ✓ | ✓ | ✓ | – | **C**(S1-158)|
| **Member** | ✗(0 命中 memberId)| ✓(Member 库配置) | ✓ | – | – | **C**(S1-154)|
| **RefundOrderLog** | ✗ refundOrderLogId(3) | ✓ commitId | ✓ | ✓ | – | **C**(临时 commitId,S1-155)|

### 2.2 F 全部 / 禁造 Object

| Object | 历史判断 | 当前证据 | 当前最终 |
|---|---|---|---|
| **Sale** | F(S1-143)| 0 命中 saleId/saleVo | F |
| **MedicalProductStock** | F(S1-149)| 0 命中 stockBatchId | F |
| **SaleVo** | F | 0 命中 | F |
| **SystemSetting** | F(S1-151)| 0 命中 settingId/systemSettingId | F(State 聚合器)|
| **CheckItem** | F(S1-157)| 0 命中 checkItemId | F |
| **ChargeItem** | F | 0 命中 | F |
| **CustomerChargeItem** | F(S1-158)| 0 命中 | F |
| **Material** | F(S1-157)| 0 命中 materialId | F |
| **MedicalFee** | F(S1-157)| 0 命中 medicalFeeId/feeId | F |
| **MemberType** | F(S1-154)| 0 命中 memberTypeId | F |
| **ProcessCenter** | F(S1-157)| 0 命中 processCenterId | F(= MachineCenter)|
| **ProjectCard** | F(S1-157)| 0 命中 projectCardId | F(= TrainerCard)|
| **Clinic** | F(S1-158)| 0 命中 clinicId/clinicName/clinicVo | F |
| **ClinicImage** | F | 0 命中 clinicImageId | F |
| **Settlement** | F | 0 命中 settlementId | F |
| **Cost** | F | 0 命中 costId | F |
| **Expense** | F | 0 命中 expenseId | F |
| **BankCard** | F | 0 命中 bankCardId/feeBankCardId | F |
| **Payment** | F | 0 命中 paymentId | F |
| **Charge(独立)** | F | 0 命中 chargeId | F |
| **Refund(独立)** | F(S1-148)| 0 命中 refundId(Object ID),仅局部变量 | F(独立 Object)|
| **VisionRecord** | F | 0 命中 visionRecordId | F |
| **Prescription** | F | 0 命中 prescriptionId | F |
| **MethodGlassRecord** | F | 0 命中 methodGlassRecordId | F |
| **MarketingOrder** | F(S1-155)| 0 命中 marketingOrderId | F |
| **Group** | F | 0 命中 groupId | F |
| **Seckill(独立)** | F | 0 命中 seckillId | F |
| **SmsTask** | F | 0 命中 smsId | F |
| **ExportTask** | F | 0 命中 exportId | F |
| **PrintTask** | F | 0 命中 printTaskId | F |
| **Dashboard** | F | 0 命中 | F |
| **Lead** | F(S1-155)| 0 命中 leadId | F(= RecommendPhone)|
| **MarketingReferral** | F | 0 命中 referralId | F(= RecommendPhone)|
| **MarketingLead** | F | 0 命中 customerLeadId | F |
| **MarketingCard** | F | 0 命中 cardId | F(= TrainerCard)|
| **MarketingPoint** | F | 0 命中 pointId | F(= Customer 字段)|
| **ShopMember** | F | 0 命中 | F |
| **MemberLibrary** | F | 0 命中 | F |
| **CustomerAsset** | F | 0 命中 customerAssetId | F |
| **Machine** | F | 0 命中 machineId | F |
| **MachineOrder** | F | 0 命中 machineOrderId | F |
| **Schedule** | F | 0 命中 scheduleId | F |
| **Queue** | F | 0 命中 queueId/queueNumber | F |
| **CallingMachine** | F | 0 命中 | F |
| **CheckConfig** | F | 0 命中 checkConfigId | F |

**总计:46 个禁造 Object**。

### 2.3 Object 去重核心结论

- **历史声称**:"S1-150 真实 ID = machineOrderOrderId",本轮 grep **0 命中**,**纠偏**:真实 ID 是 `machineCenterOrderId`(7 处)
- **历史声称**:"S1-150 machineCenterOrderVoList 2 处",本轮确认 ✓
- **历史声称**:"S1-155 RefundId 是 ID",本轮发现 `refundId` 仅 4 处**局部变量**,`refundOrderLogId` 3 处是 commitId,**无 Object ID**
- **新增** examineId(24)+ medicalCheckItem.id(多) = S1-158 新发现

---

## §3 全局 ID 主表

### 3.1 V4.4 Global ID Allowlist(45 个 A 真实 ID)

| ID | 命中 | 业务 | 来自 |
|---|---:|---|---|
| `medicalRecordId` | 161 | MedicalRecord | S1-146 ✓ |
| `patientId` | 89 | Patient | S1-147 ✓ |
| `customerId` | 128 | Customer | S1-147 ✓ |
| `customerCheckinId` | 19 | CustomerCheckin | S1-147 ✓ |
| `cashflowId` | 73 | Cashflow | S1-148 ✓ |
| `printCheckinId` | 9 | PrintCheckin | S1-148 ✓ |
| `productId` | 42 | Product | S1-149 ✓ |
| `skuId` | 85 | SKU | S1-149 ✓ |
| `productSkuId` | 69 | SKU | S1-149 ✓ |
| `stockInSkuId` | 60 | Stock | S1-149 ✓ |
| `medicalProductId` | 20 | MedicalProduct | S1-149 ✓ |
| `supplierId` | 99 | Supplier | S1-157 ✓ |
| `mainSupplierId` | 25 | mainSupplier | S1-149 ✓ |
| `machineCenterId` | 18 | MachineCenter | S1-150 ✓ |
| `machineCenterOrderId` | 7 | MachineCenterOrder | S1-150 ✓ |
| `appointId` | 18 | Appointment | S1-153 ✓ |
| `appointmentId` | 4 | Appointment(同实体另一命名)| S1-153/155 ✓ |
| `consultRoomId` | 22 | ConsultRoom | S1-158 ✓ |
| `bigScreenId` | 14 | BigScreen | S1-153 ✓ |
| `schoolId` | 205 | School | S1-152 ✓ |
| `classId` | 131 | SchoolClass | S1-152 ✓ |
| `schoolMateId` | 19 | SchoolMate | S1-152 ✓ |
| `schoolMateCheckId` | 16 | SchoolMateCheck | S1-152 ✓ |
| `followUpId` | 20 | FollowUp | S1-154 ✓ |
| `orderId` | 6 | CustomerOrder | S1-155 ✓ |
| `couponId` | 9 | Coupon | S1-155 ✓ |
| `customerCouponId` | 17 | CustomerCoupon | S1-155 ✓ |
| `recommendPhoneId` | 12 | RecommendPhone | S1-155 ✓ |
| `grouponProductId` | 6 | GrouponProduct | S1-155 ✓ |
| `seckillProductId` | 14 | SeckillProduct | S1-155 ✓ |
| `promotionId` | 43 | Promotion | S1-155 ✓ |
| `trainerCardId` | 5 | TrainerCard | S1-157 ✓ |
| `customerTrainerCardId` | 15 | CustomerTrainerCard | S1-155 ✓ |
| `companyId` | 102 | Company | S1-158 ✓ |
| `employeeId` | 35 | Employee | S1-158 ✓ |
| `adminId` | 21 | Admin | S1-158 ✓ |
| `adminRoleId` | 29 | AdminRole | S1-158 ✓ |
| `roleId` | 4 | Role | S1-158 ✓ |
| `departmentId` | 1(弱) | Department | S1-158 ✓(弱)|
| `companyCashConfId` | 3 | CompanyCashConf | S1-156/157 ✓ |
| `corpTypeId` | 2 | CorpTypeConf | S1-158 ✓ |
| `examineId` | 24 | Examine | S1-158 ✓ |
| `bodyCheckItemId` | 4 | BodyCheckItem | S1-157 ✓ |
| `taskTemplateBatchSendId` | 11 | TemplateBatchSendTask | S1-155 ✓ |
| `taskCouponBatchSendId` | 3 | CouponBatchSendTask | S1-155 ✓ |
| `taskScreenTemplateBatchSendId` | 9 | ScreenTemplateBatchSendTask | S1-155 ✓ |

**新增 medicalCheckItem.id** 真实(等同 bodyCheckItemId,S1-158 新发现)

### 3.2 V4.4 Global ID Denylist(46 个 F 禁造 ID)

| ID | 命中 | 禁造原因 |
|---|---:|---|
| `saleId` | 0 | Sale 不是独立 Entity |
| `saleVo` | 0 | 同上 |
| `settingId` | 0 | SystemSetting 是 State 聚合器 |
| `systemSettingId` | 0 | 同上 |
| `checkItemId` | 0 | checkItem 真实叫 bodyCheckItem |
| `checkConfigId` | 0 | CheckConfig 不存在 |
| `chargeItemId` | 0 | ChargeItem 不存在 |
| `materialId` | 0 | Material 是 productSku 子属性 |
| `feeId` | 0 | Fee 不存在 |
| `medicalFeeId` | 0 | 同上 |
| `memberTypeId` | 0 | MemberType 是 Member 库 |
| `processCenterId` | 0 | ProcessCenter = MachineCenter |
| `projectCardId` | 0 | ProjectCard = TrainerCard |
| `corpAppointmentConfId` | 0 | Configuration,无独立 ID |
| `corpAppointConfId` | 0 | 同上 |
| `corpCashConfId` | 0 | 实际是 companyCashConfId |
| `corpReportConfId` | 0 | 同上 |
| `corpPointRuleId` | 0 | 同上 |
| `clinicId` | 0 | Clinic 不是独立 Object |
| `clinicName` | 0 | 同上 |
| `clinicVo` | 0 | 同上 |
| `clinicImageId` | 0 | ClinicImage 不存在 |
| `imageId` | 0 | 同上 |
| `companyVo` | 0 | VO 不存在 |
| `employeeVo` | 0 | VO 不存在 |
| `departmentName` | 0 | 实际是 departDesc |
| `departmentVo` | 0 | 同上 |
| `roleVo` | 0 | VO 不存在 |
| `consultRoomStatus` | 0 | 实际是 status 字段 |
| `settlementId` | 0 | Settlement 不存在 |
| `costId` | 0 | Cost 不存在 |
| `expenseId` | 0 | Expense 不存在 |
| `bankCardId` | 0 | BankCard 不存在 |
| `feeBankCardId` | 0 | feeBankCardCtrl 是 Wallet |
| `cashConfigId` | 0 | 实际是 companyCashConfId |
| `machineId` | 0 | Machine 不存在 |
| `machineOrderId` | 0 | 实际是 machineCenterOrderId |
| `scheduleId` | 0 | Schedule 不存在 |
| `queueId` | 0 | Queue 不存在 |
| `queueNumber` | 0 | 同上 |
| `visionRecordId` | 0 | VisionRecord 不存在 |
| `prescriptionId` | 0 | Prescription 不存在 |
| `methodGlassRecordId` | 0 | MethodGlassRecord 不存在 |
| `paymentId` | 0 | Payment 不存在 |
| `chargeId` | 0 | Charge 不存在 |
| `customerAssetId` | 0 | 不存在 |
| `leadId` | 0 | Lead 不存在 |
| `referralId` | 0 | Referral = RecommendPhone |
| `groupId` | 0 | Group = GrouponProduct |
| `seckillId` | 0 | Seckill = SeckillProduct |
| `smsId` | 0 | 用 taskXxxBatchSendId |
| `marketingOrderId` | 0 | 实际是 orderId |
| `pointId` | 0 | Point 是 Customer 字段 |
| `cardId` | 0 | Card = TrainerCard |
| `customerLeadId` | 0 | 不存在 |
| `reportId` | 0 | Report 不存在 |
| `statisticsId` | 0 | Statistics 不存在 |
| `exportId` | 0 | Export 不存在 |
| `printTaskId` | 0 | Print 不存在 |
| `materialListId` | 0 | 不存在 |
| `stockBatchId` | 0 | 不存在(S1-149 已确认)|
| `customerChargeItemId` | 0 | 不存在 |

### 3.3 新发现(本轮全局复跑)

| ID | 命中 | 来源 | 处理 |
|---|---:|---|---|
| `refundId` | 4 | L4904 / L7190 / L7195 / L7274 | **C(局部变量,非 Object ID)** |
| `refundOrderLogId` | 3 | L20739 / L20741 / L20752 | **A(临时 commitId,S1-155 Order 退款流程)** |
| `medicalCheckItem.id` | 多 | L50265 / L50270 / L50279 | **A(等同 bodyCheckItemId,S1-158)** |
| `departmentId` | 1 | L15691 | **A 弱(仅 State 参数)** |

### 3.4 命名纠偏(关键冲突)

| 历史结论 | 当前证据 | 冲突原因 | 当前采用 |
|---|---|---|---|
| S1-150: machineOrderOrderId 真实 | **0 命中** | 命名误导 | `machineCenterOrderId`(7 处)|
| S1-150: machineCenterVo / machineOrderVo 真实 | **0 命中** | VO 命名 | `machineCenterOrderVoList`(2 处)|
| S1-150: machineOrderId 真实 | **0 命中** | 同上 | 同上 |
| S1-155: refundId 是 Refund Object ID | **4 处仅局部变量** | commitId 而非 Object ID | `refundOrderLogId`(3 处 commitId)|
| S1-155: sendCouponId | **0 命中** | 命名误导 | `customerCouponId` |
| S1-156: corpCashConfId | **0 命中** | 命名误导 | `companyCashConfId`(3 处)|
| S1-156: corpReportConfId | **0 命中** | 命名误导 | `corpReportConf` Configuration(无独立 ID)|

---

## §4 全局 API 主表

### 4.1 .json API 总数:**915 个**

### 4.2 已知核心域 API 分布

| 域 | API 数 | 来源 |
|---|---:|---|
| MedicalRecord | ~25 | S1-146 |
| Cashflow | ~12 | S1-148 |
| Delivery | ~10 | S1-142 |
| Product / SKU / Stock | ~80 | S1-149 |
| MachineCenter | ~15 | S1-150 |
| Appointment / BigScreen | ~15 | S1-153 |
| Screening | ~20 | S1-152 |
| Marketing | ~152 | S1-155 |
| Report / Stat / Print / Export | ~90 | S1-156 |
| SystemSetting | ~30 | S1-157 |
| Clinic Management | ~70 | S1-158 |

### 4.3 重要 API 验证(本轮复跑)

- `medicalRecordId` 在 161 处 API 中作为 Request 字段
- `cashflowId` 在 73 处 API 中作为 Request 字段
- `companyId` 在 102 处 API 中作为 Request/State 字段
- `consultRoomId` 在 22 处 API 中作为 Request 字段
- `customerCouponId` 在 17 处 API 中作为 Request 字段
- `taskTemplateBatchSendId` 在 11 处 API 中作为 Request 字段

### 4.4 API 归属冲突清单(无)

经本轮全局复跑,915 个 API 全部唯一命名,无跨域重复。但**有命名误导**:

| API 命名 | 实际业务 | 处理 |
|---|---|---|
| `corpCashConfId` (在 chargeAdminCtrl) | 实际参数为 `companyCashConfId` | 命名误导,**统一为 companyCashConfId** |
| `corpReportConfId` | 不存在 | 实际是 `defaultStartMonth / defaultStartDay` |
| `createOrderFactory / getOrderFactory` | AngularJS Factory | 不是 API |

---

## §5 WRITE MASTER

### 5.1 已知核心域 Write API 列表(基于 S1-135 ~ S1-158)

#### 5.1.1 MedicalRecord Create

| API | Controller | Request | Grade |
|---|---|---|---|
| `addMedicalRecord.json` | L3865 | – | A |
| `createCashFlowForMedicalRecord.json` | L4034 | medicalRecordId | A |
| `computeUnPlaceOrderMedicalRecordFee.json` | L6680 | medicalRecordId | A |
| `reComputeUnPlaceOrderMedicalRecordFee.json` | L6884 | – | A |

#### 5.1.2 Cashflow Write

| API | Controller | Request | Grade |
|---|---|---|---|
| `createCashFlowForMedicalRecord.json` | L4034 | medicalRecordId | A |
| `payMedicalRecordCashflow.json` | L4045 | – | A |
| `commitCustomerPointLog.json` | L18197 | – | A |
| `createRefundOrderLog.json` | L20734 | customerId + cashflowId | A |
| `commitRefundOrderLog.json` | L20740 | refundOrderLogId | A |

#### 5.1.3 Delivery Write

| API | Controller | Request | Grade |
|---|---|---|---|
| `completeMedicalRecordDelivery.json` | L4314 | medicalRecordId | A |
| `createMedicalStockLossOfSmallVersion.json` | L3997 | | (S1-142 命名误导)|
| `confirmMedicalRecordReturn.json` | L4361 | | (S1-142)|
| `cancelMedicalRecord.json` | L4398 | | (S1-142)|
| `deliveryOrder.json` | L20852 | deliveryObj | A |

#### 5.1.4 MachineCenter Write

| API | Controller | Request | Grade |
|---|---|---|---|
| `startMachineCenterOrder.json` | L4320 | – | A |
| `completeMachineCenterOrder.json` | L4324 | – | A |
| `closeMachineCenterOrder.json` | L4329 | – | A |
| `receiveMachineCenterOrder.json` | L4317 | machineCenterOrderId | A |
| `deliveryMachineCenterOrder.json` | L4332 | machineCenterOrderId | A |

#### 5.1.5 Product / SKU / Stock Write(S1-149 已汇总)

- `createStockOutAndSkuList.json` / `addTrainerCard.json` / `updateTrainerCard.json` / `addTrainerCardFactory` 等 80+

#### 5.1.6 Appointment Write(S1-153 已汇总)

- `confirmAppointment.json` / `confirmArrivalOfAppoint.json` / `beginCustomerCheckin.json` 等 15

#### 5.1.7 Screening Write(S1-152 已汇总)

- `createSchoolMateCheck.json` / `updateSchoolMateCheck.json` / `assignRecommendPhoneList.json` 等 20

#### 5.1.8 Marketing Write(S1-155 已汇总)

- `createCoupon.json` / `useCoupon.json` / `pickUpOrder.json` / `grouponProduct.json` 等 30+

#### 5.1.9 SystemSetting Write(S1-157 已汇总)

- `addTrainerCard.json` / `setBodyCheckItemPrintDisable.json` / `addSupplier.json` 等 17

#### 5.1.10 Clinic Write(S1-158 已汇总)

- `updateCorpInfo.json` / `addDepartment.json` / `updateDepartment.json` / `deleteDepartment.json` / `addConsultRoom.json` / `updateConsultRoomInfo.json` / `updateConsultRoomStatus.json` / `setDoctorApproved.json` / `setEmployeeRank.json` / `changeAdminRole.json` / `saveCorpCashConf.json` 等 31

### 5.2 Write Master 总结

- **总 Write API**:~250 个(基于 S1-135~S1-158 已审)
- **核心域 Write 完整覆盖**:MedicalRecord / Cashflow / Delivery / MachineCenter / Product / Appointment / Screening / Marketing / SystemSetting / Clinic 全部 ✓
- **遗漏检查**:本轮**未发现 Write 漏项**
- **新发现**:refundOrderLogId 3 处(S1-155 Order 退款临时 commitId),属局部变量,不入 Object 实体

---

## §6 State → Controller → API → Object 四层链

### 6.1 P0 领域四层链(精简)

#### MedicalRecord

```
State: addCheckinCtrl(L8159) / addVisitCtrl(L49594) / addSaleRecordCtrl / waitChargeDetailCtrl / myMedicalRecordListCtrl
Controller: optometryCtrl(L13798) / addVisitCtrl(L49594)
Read API: getMedicalRecordPayVo.json / getMedicalRecordCashflowVo.json / selectMedicalRecordVoList.json
Write API: addMedicalRecord.json / createCashFlowForMedicalRecord.json / computeUnPlaceOrderMedicalRecordFee.json
Object ID: medicalRecordId(161)
Source → Target: customerCheckinId → medicalRecordId → cashflowId
```

#### Customer

```
State: customerListCtrl / customerDetailCtrl / myCustomerCtrl / addCustomerCtrl
Controller: addCustomerCtrl / customerListCtrl
Read API: selectCustomerVoList.json / getCustomerVo.json
Write API: createCustomer.json / updateCustomer.json
Object ID: customerId(128)
```

#### Cashflow

```
State: waitPayDetailCtrl / waitChargeDetailCtrl / addVisitCtrl(L49594)
Controller: waitPayDetailCtrl(L36988)
Read API: getMedicalRecordPayVo.json / getMedicalRecordCashflowVo.json
Write API: payMedicalRecordCashflow.json / createCashFlowForMedicalRecord.json / createRefundOrderLog.json / commitRefundOrderLog.json
Object ID: cashflowId(73)
Source → Target: medicalRecordId → cashflowId
```

#### Appointment

```
State: addCheckinCtrl(L8159) / bookDetailCtrl(L3669) / bookManageCtrl(L3706)
Controller: addCheckinCtrl / bookDetailCtrl
Read API: getAppointPatientVo.json / getAppointSchoolMateVo.json / selectAppointmentVoList.json
Write API: confirmAppointment.json / confirmArrivalOfAppoint.json / beginCustomerCheckin.json / receiveSelfAndBeginCustomerCheckin.json
Object ID: appointId(18) + appointmentId(4)
```

#### MachineCenterOrder

```
State: machineOrderWaitProcessCtrl / machineOrderCompletedCtrl / machineOrderListCtrl
Controller: machineCenterCtrl / machineOrderCtrl
Read API: getMachineCenterOrderVo.json / selectMachineCenterOrderVoList.json
Write API: startMachineCenterOrder.json / completeMachineCenterOrder.json / closeMachineCenterOrder.json / receiveMachineCenterOrder.json / deliveryMachineCenterOrder.json
Object ID: machineCenterOrderId(7)(不是 machineOrderOrderId / machineOrderId)
Source → Target: medicalRecordId → machineCenterOrderId
```

#### CustomerOrder(Marketing)

```
State: orderDetailCtrl(L18937) / orderManageCtrl(L36165) / selectOrderListCtrl(L20636)
Controller: orderDetailCtrl / orderManageCtrl
Read API: getOrderVo.json / selectOrderVoListByCorpId.json
Write API: pickUpOrder.json / deliveryOrder.json / createRefundOrderLog.json
Object ID: orderId(6)
Source → Target: customerId → orderId → cashflowId(退款)
```

#### ConsultRoom

```
State: adminClinic(L15053)
Controller: adminClinicCtrl(命名误导,实际是 ConsultRoom)
Read API: selectConsultRoomVoListOfCompany.json / getConsultRoomVo.json
Write API: addConsultRoom.json / updateConsultRoomInfo.json / updateConsultRoomStatus.json
Object ID: consultRoomId(22)
Source → Target: companyId → consultRoomId → appointId / bigScreenId
```

#### Supplier

```
State: systemSetting.supplierList / supplierModify
Controller: supplierListCtrl / supplierModifyCtrl
Read API: selectSupplierVoList.json / getSupplier.json
Write API: addSupplier.json / modifySupplier.json / deleteSupplier.json
Object ID: supplierId(99)
Source → Target: mainSupplier.id → supplierId(Stock)
```

#### TrainerCard

```
State: systemSetting.projectCard / addProjectCardCtrl(L52150)
Controller: projectCardCtrl(L57851) / addProjectCardCtrl(命名误导)
Read API: selectTrainerCardList.json / getTrainerCard.json
Write API: addTrainerCard.json / updateTrainerCard.json / updateByTrainerCardIdArraySelective.json
Object ID: trainerCardId(5)
Source → Target: trainerCardId → customerTrainerCardVo / cashflow
```

### 6.2 全四层链完整性

| P0 Object | State | Controller | Read | Write | ID | 完整性 |
|---|---|---|---|---|:-:|:-:|
| MedicalRecord | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Customer | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Patient | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| CustomerCheckin | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Cashflow | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Product | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| SKU | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| MedicalProduct | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Stock | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| MachineCenter | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| MachineCenterOrder | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| ConsultRoom | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Appointment | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| BigScreen | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| School | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| SchoolMate | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| SchoolMateCheck | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| FollowUp | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| CustomerOrder | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Coupon | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| CustomerCoupon | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| RecommendPhone | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| GrouponProduct | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| SeckillProduct | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| TrainerCard | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Company | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Employee | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Department | ✓ | ✓ | ✓ | ✓ | ✓ | C(弱)|
| TemplateBatchSendTask | ✓ | ✓ | ✓ | ✓ | ✓ | A |
| Examine | ✓ | ✓ | ✓ | ✓ | ✓ | A |

---

## §7 全局关系矩阵(全部 A/B)

### 7.1 核心对象关系矩阵(50+ 条)

| 关系 | 真实? | Grade | 字符级证据 |
|---|:-:|:-:|---|
| **MedicalRecord ↔ Customer** | ✓ | A | selectCustomerVoList `{medicalRecordId}` |
| **MedicalRecord ↔ Patient** | ✓ | A | medicalRecord.patientId 89 命中 |
| **MedicalRecord ↔ CustomerCheckin** | ✓ | A | customerCheckin.medicalRecordId 19 |
| **MedicalRecord ↔ Cashflow** | ✓ | A | createCashFlowForMedicalRecord `{medicalRecordId}` |
| **MedicalRecord ↔ Delivery** | ✓ | A | completeMedicalRecordDelivery `{medicalRecordId}` |
| **MedicalRecord ↔ Sale** | ✓ | C | medicalProductVoList 嵌入 |
| **MedicalRecord ↔ MedicalExamine** | ✓ | A | S1-145 字段级 |
| **MedicalRecord ↔ MachineCenterOrder** | ✓ | A | startMachineCenterOrder `{medicalRecordId}` |
| **Customer ↔ Patient** | ✓ | A | customerObjectFactory `{patientId}` (S1-147)|
| **Customer ↔ CustomerCheckin** | ✓ | A | beginCustomerCheckin `{customerId}` |
| **Customer ↔ Cashflow** | ✓ | A | cashflow.customer |
| **Customer ↔ Coupon** | ✓ | A | sendCoupon `{customerId}` |
| **Customer ↔ TrainerCard** | ✓ | A | customerTrainerCardVo |
| **Customer ↔ RecommendPhone** | ✓ | A | linkRecommendPhone `{customerId}` |
| **CustomerCheckin ↔ Appointment** | ✓ | A | confirmArrivalOfAppoint `{appointId}` |
| **CustomerCheckin ↔ MedicalRecord** | ✓ | A | beginCustomerCheckin `{customerCheckinId}` |
| **CustomerCheckin ↔ SchoolMateCheck** | ✓ | A | S1-152 汇合链 |
| **Patient ↔ CustomerCheckin** | ✓ | A | customerCheckin.patientId(S1-140 注释)|
| **MedicalProduct ↔ Product** | ✓ | A | medicalProductVoList 嵌入(S1-149)|
| **MedicalProduct ↔ SKU** | ✓ | A | productSkuVo `{medicalProductId}` |
| **MedicalProduct ↔ Stock** | ✓ | A | stockInSkuVoList `{medicalProductId}` |
| **MedicalProduct ↔ Delivery** | ✓ | A | medicalProductDelivery |
| **MedicalProduct ↔ MachineCenter** | ✓ | A | sendMedicalProductToMachineCenter |
| **MachineCenterOrder ↔ MachineCenter** | ✓ | A | machineCenterOrderVoList |
| **MachineCenterOrder ↔ MedicalProduct** | ✓ | A | machineCenterOrder.medicalProductVoList |
| **MachineCenterOrder ↔ Delivery** | ✓ | A | deliveryMachineCenterOrder |
| **Product ↔ Supplier** | ✓ | A | mainSupplier.id |
| **Stock ↔ Supplier** | ✓ | A | stockInSkuVo.mainSupplier |
| **Appointment ↔ ConsultRoom** | ✓ | A | S1-153 bigScreenCtrl consultRoomId |
| **Appointment ↔ BigScreen** | ✓ | A | checkCallCtrl L10124 |
| **BigScreen ↔ ConsultRoom** | ✓ | A | S1-153 |
| **ConsultRoom ↔ MedicalExamine** | ✓ | A | adminClinicCtrl examineIdArray L15115 |
| **ConsultRoom ↔ Company** | ✓ | A | addConsultRoom `{companyId}` |
| **School ↔ SchoolMate** | ✓ | A | schoolMateVoList |
| **SchoolClass ↔ SchoolMate** | ✓ | A | classMateId(S1-152)|
| **SchoolMate ↔ Patient** | ✓ | A | schoolMateVo `{patientId}` |
| **SchoolMate ↔ CustomerCheckin** | ✓ | A | beginCustomerCheckin(S1-133)|
| **SchoolMateCheck ↔ SchoolMate** | ✓ | A | schoolMateCheckVoList |
| **SchoolMateCheck ↔ FollowUp** | ✓ | A | S1-152/154 |
| **Company ↔ Employee** | ✓ | A | selectEmployeeVoList `{companyId}` |
| **Company ↔ Department** | ✓ | A | getDepartmentList `{companyId}` |
| **Company ↔ ConsultRoom** | ✓ | A | selectConsultRoomVoListOfCompany |
| **Company ↔ TrainerCard** | ✓ | C | corpPointRule 公司级 |
| **Company ↔ MachineCenter** | ✓ | C | processCenterCtrl 公司级 |
| **Company ↔ CorpConfig** | ✓ | A | chargeAdminCtrl / reportDateAdminCtrl |
| **Employee ↔ Department** | ✗ | F | 0 命中 employee.departmentId |
| **Employee ↔ Role** | ✗ | F | 0 命中 employee.roleId |
| **Employee ↔ ConsultRoom** | ✗ | F | 0 命中 |
| **CustomerOrder ↔ Customer** | ✓ | A | orderVo.customer |
| **CustomerOrder ↔ MedicalRecord** | ✓ | C | okOrderRecordVoList.medicalRecordId |
| **CustomerOrder ↔ Cashflow** | ✓ | C | customerOrder.cashflow 嵌套 |
| **CustomerOrder ↔ Delivery** | ✓ | A | deliveryObj.orderId |
| **Coupon ↔ Order** | ✓ | A | computeUsableCustomerCoupon L6627 |
| **TrainerCard ↔ Cashflow** | ✓ | A | consumeCustomerTrainerCardNumbers |

---

## §8 命名归一化

### 8.1 命名误导修复总表

| 旧名 | 实际 Object | 证据 | 处理 |
|---|---|---|---|
| `machineOrderOrderId` | machineCenterOrderId | grep 0 命中,S1-150 误称 | **改: machineCenterOrderId** |
| `machineOrderId` | machineCenterOrderId | grep 0 命中 | **改: machineCenterOrderId** |
| `machineCenterVo` | machineCenterOrderVoList | grep 0 命中 | **改: machineCenterOrderVoList** |
| `machineOrderVo` | machineCenterOrderVoList | grep 0 命中 | **改: machineCenterOrderVoList** |
| `machineCenterVoList` | machineCenterOrderVoList | grep 0 命中 | **改: machineCenterOrderVoList** |
| `corpCashConfId` | companyCashConfId | grep 0 命中 | **改: companyCashConfId** |
| `corpCashConf` | companyCashConf | 真实命名 | **统一: companyCashConf** |
| `refundId` | refundOrderLogId | 4 处仅局部 | **改: refundOrderLogId** |
| `projectCardId` | trainerCardId | 0 命中 | **改: trainerCardId** |
| `processCenterId` | machineCenterId | 0 命中 | **改: machineCenterId** |
| `memberTypeId` | 无 | 0 命中 | **删: MemberType 是 Member 库** |
| `checkItemId` | bodyCheckItemId | 0 命中 | **改: bodyCheckItemId** |
| `medicalFeeId` | 无 | 0 命中 | **删: medicalFeesList = Examine** |
| `addCheckCtrl` | addExamineCtrl | 实际是 Examine | **改: addExamineCtrl** |
| `addCheckItemCtrl` | addMedicalCheckItemCtrl | 实际是 medicalCheckItem | **改: addMedicalCheckItemCtrl** |
| `checkListCtrl` | examineVoListCtrl | 实际是 Examine 列表 | **改: examineVoListCtrl** |
| `medicalFeesListCtrl` | examineListCtrl | 实际是 Examine | **改: examineListCtrl** |
| `memberTypeListCtrl` | memberListCtrl | 实际是 Member 库 | **改: memberListCtrl** |
| `adminClinicCtrl` | ConsultRoomCtrl | 实际是 ConsultRoom | **改: ConsultRoomCtrl** |
| `feeBankCardCtrl` | feeWalletCtrl | 实际是 Customer Wallet | **改: feeWalletCtrl** |
| `chargeAdminCtrl` | cashConfigCtrl | 实际是 corpCashConf | **改: cashConfigCtrl** |
| `printConfigCtrl` | cashConfigCtrl | 实际是 corpCashConf | **改: cashConfigCtrl** |
| `appointOrderCtrl` | (空 Stub)| S1-153 空 Stub | **删: 不存在** |
| `memberCardCtrl` | (空路由)| 命名误导 | **删: 不存在** |
| `memberPointCtrl` | (空路由)| 命名误导 | **删: 不存在** |
| `phoneAdminCtrl` | (命名误导待确认)| | **待: S1-159 标记** |
| `sendCouponId` | customerCouponId | 0 命中 | **改: customerCouponId** |
| `seckillId` | seckillProductId | 0 命中 | **改: seckillProductId** |
| `groupId` | grouponProductId | 0 命中 | **改: grouponProductId** |
| `smsId` / `smsTaskId` | taskXxxBatchSendId | 0 命中 | **改: taskXxxBatchSendId** |
| `marketingOrderId` | orderId | 0 命中 | **改: orderId** |
| `leadId` | recommendPhoneId | 0 命中 | **改: recommendPhoneId** |
| `referralId` | recommendPhoneId | 0 命中 | **改: recommendPhoneId** |
| `pointId` | 无 | 0 命中 | **删: Customer 字段** |
| `cardId` | trainerCardId | 0 命中 | **改: trainerCardId** |
| `materialId` | 无 | 0 命中 | **删: productSku 子属性** |

---

## §9 Status / Scope / Toggle 全局分类

### 9.1 真实业务状态(Object Field)

| 字段 | 命中 | 含义 | 业务 |
|---|---:|---|---|
| `refundStatus` | 20 | 0=未退款 / 1=已退款 / 2=部分退 | S1-148 / S1-155 |
| `deliveryStatus` | 30 | 0=未发货 / 1=已发货 / 2=已收货 | S1-155 |
| `cancelStatus` | 6 | 0=未取消 / 1=已取消 | S1-142 |
| `receiveStatus` | 6 | 0=未收货 / 1=已收货 | S1-142 |
| `creditStatus` | 6 | 0=未欠 / 1=已欠 | S1-148 |
| `examineType` | 多 | 1 / 2 类型 | S1-158 |
| `status` | 549 | 多义通用 | 业务态 |
| `substractType` | 1 | 训练卡扣次类型 | S1-157 |
| `appointSceneType` | 4 | 预约场景类型 | S1-153 |
| `sceneType` | 23 | 场景类型(通用)| S1-154 |
| `allowReturnCard` | 4 | 是否允许退卡 | S1-157 |
| `allowChangePrice` | 3 | 是否允许改价 | S1-157 |
| `allowChangeNumber` | 3 | 是否允许改次 | S1-157 |

### 9.2 Scope 字段

| 字段 | 命中 | 含义 |
|---|---:|---|
| `companyId` | 102 | 公司作用域 |
| `companyIdArray` | 13 | 公司 ID 数组(Request) |
| `schoolIdArray` | 5 | 学校 ID 数组(Admin Scope,S1-152)|
| `isClinicAdmin` | 4 | 是否是诊所 Admin(bool) |
| `adminRoleId` | 29 | Admin 角色作用域 |

### 9.3 锁定字段

| 字段 | 命中 | 业务 |
|---|---:|---|
| `lockStorehouse` | 9 | 仓库锁(S1-149) |
| `lockMachineCenter` | 1 | 加工中心锁(S1-150)|

### 9.4 UI Toggle / 局部变量

| 字段 | 含义 |
|---|---|
| `tab` 549 命中 | UI 标签,不是 DB 字段 |
| `isActive` 0 命中 | 不存在 |
| `enabled` 0 命中 | 不存在 |

### 9.5 区分原则

- **真实业务状态**:DB 字段,S1-148/155 等已确认
- **Filter / Search**:`examineType / status / substractType` 等
- **Scope**:`companyId / schoolIdArray` 等公司/学校作用域
- **UI Toggle**:`tab / isActive`
- **派生字段**:`receivedFromPoint` 等计算字段

---

## §10 V4.4 Global ID Allowlist(45 个 A)

见 §3.1。

---

## §11 V4.4 Global ID Denylist(46+ 个 F)

见 §3.2。

---

## §12 READ MASTER

基于 S1-135 ~ S1-158,核心域 Read API 总数:**~250 个**。

代表性:
- MedicalRecord:getMedicalRecordPayVo / getMedicalRecordCashflowVo / selectMedicalRecordVoList 等
- Cashflow:getMedicalRecordCashflowVo / getMedicalRecordPayVo
- Product / SKU:selectProductSku... / get... 多个
- Appointment:getAppointmentVo / selectAppointmentVoList / getAppointPatientVo / getAppointSchoolMateVo
- Screening:getSchoolMateCheckVo / selectSchoolMateCheckVoList / selectSchoolMateScreenInStoreStatVoList
- Marketing:getOrderVo / getCouponVo / getFollowUpVo / getTrainerCard
- Clinic:getCorpInfo / getDepartmentList / getConsultRoomVo / getExamineVo

---

## §13 WRITE MASTER

基于 S1-135 ~ S1-158,核心域 Write API 总数:**~250 个**。

代表性见 §5。

---

## §14 F / 未验证 API

凡未在 S1-135 ~ S1-158 任意文档中明确出现的 API,本轮**不主动添加**。

---

## §15 全局 26 项一致性矩阵

### 15.1 全局 P0 Object 26 项摘要

| Object | ID | State | Ctrl | Entry | Read | Write | Req | Resp | Field | Status | Scope | Grade |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| MedicalRecord | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | F(0) | – | A |
| Customer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| Patient | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| CustomerCheckin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| Cashflow | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(refundStatus 20)| – | A |
| Product | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| SKU | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| MedicalProduct | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| Stock | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(lockStorehouse) | A |
| Supplier | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| MachineCenter | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(lockMachineCenter) | A |
| MachineCenterOrder | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| ConsultRoom | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(0/1)| ✓(companyId) | A |
| Appointment | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(appointSceneType) | A |
| BigScreen | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(consultRoomId) | A |
| School | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(schoolIdArray) | A |
| SchoolMate | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| SchoolMateCheck | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| FollowUp | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓(sceneType) | A |
| CustomerOrder | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(deliveryStatus 30)| ✓(cashflow) | A |
| Coupon | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(0/1/2)| – | A |
| CustomerCoupon | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(0/1/2)| ✓(couponId) | A |
| RecommendPhone | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| GrouponProduct | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| SeckillProduct | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| TrainerCard | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(allowReturnCard / allowChangePrice / allowChangeNumber)| – | A |
| Company | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓(corpTypeId) | – | A |
| Employee | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |
| Department | ✓(弱) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | C |
| TemplateBatchSendTask | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – | A |

**未观察项**(必须 F):medicalRecord.status / corpXxxConfId / 等等(详见 §3.2)

---

## §16 历史冲突清单

### 16.1 已发现冲突(本轮定位)

| # | 类别 | 历史口径 | 当前源码 | 冲突根因 | 当前采用 |
|---|---|---|---|---|---|
| 1 | ID | S1-150: machineOrderOrderId | 0 命中 | 命名错误 | **machineCenterOrderId**(7)|
| 2 | ID | S1-150: machineOrderId | 0 命中 | 命名错误 | **machineCenterOrderId** |
| 3 | ID | S1-150: machineCenterVo | 0 命中 | VO 命名错误 | **machineCenterOrderVoList**(2)|
| 4 | ID | S1-150: machineOrderVo | 0 命中 | 同上 | **machineCenterOrderVoList** |
| 5 | ID | S1-155: refundId | 4 处局部变量 | commitId 而非 Object ID | **F(独立 Object)** |
| 6 | ID | S1-155: sendCouponId | 0 命中 | 命名错误 | **customerCouponId** |
| 7 | ID | S1-156: corpCashConfId | 0 命中 | 命名错误 | **companyCashConfId**(3)|
| 8 | ID | S1-156: corpReportConfId | 0 命中 | 同上 | **F(无独立 ID)** |
| 9 | ID | S1-154: memberTypeId | 0 命中 | MemberType 是 Member 库 | **F** |
| 10 | ID | S1-157: processCenterId | 0 命中 | ProcessCenter = MachineCenter | **machineCenterId**(18)|
| 11 | ID | S1-157: projectCardId | 0 命中 | ProjectCard = TrainerCard | **trainerCardId**(5)|
| 12 | ID | S1-157: checkItemId | 0 命中 | checkItem = bodyCheckItem | **bodyCheckItemId**(4)|
| 13 | Ctrl | S1-158: adminClinicCtrl | adminClinicCtrl = ConsultRoom | 命名误导 | **ConsultRoomCtrl** |
| 14 | Ctrl | S1-158: feeBankCardCtrl | feeBankCardCtrl = Customer Wallet | 同上 | **feeWalletCtrl** |
| 15 | Ctrl | S1-158: chargeAdminCtrl | chargeAdminCtrl = corpCashConf | 同上 | **cashConfigCtrl** |
| 16 | Ctrl | S1-158: printConfigCtrl | printConfigCtrl = corpCashConf | 同上 | **cashConfigCtrl** |
| 17 | Ctrl | S1-157: medicalFeesListCtrl | medicalFeesListCtrl = Examine | 同上 | **examineListCtrl** |
| 18 | Ctrl | S1-157: memberTypeListCtrl | memberTypeListCtrl = Member 库 | 同上 | **memberListCtrl** |
| 19 | Ctrl | S1-157: addCheckCtrl | addCheckCtrl = Examine | 同上 | **addExamineCtrl** |
| 20 | Ctrl | S1-157: addCheckItemCtrl | addCheckItemCtrl = medicalCheckItem | 同上 | **addMedicalCheckItemCtrl** |
| 21 | Ctrl | S1-157: checkListCtrl | checkListCtrl = Examine 列表 | 同上 | **examineVoListCtrl** |
| 22 | Ctrl | S1-155: memberCardCtrl | 空路由 | 命名误导 | **F(不存在)** |
| 23 | Ctrl | S1-155: memberPointCtrl | 空路由 | 同上 | **F(不存在)** |
| 24 | Ctrl | S1-153: appointOrderCtrl | 空 Stub | 已确认 | **F(不存在)** |
| 25 | Object | (误判)SaleEntity | 0 命中 saleId/saleVo | S1-143 已确认 | **F** |
| 26 | Object | (误判)SystemSetting Entity | 0 命中 settingId | S1-151 已确认 | **F(State 聚合器)** |
| 27 | Object | (误判)Marketing Order Entity | 0 命中 marketingOrderId | S1-155 已确认 | **F(= orderId)** |
| 28 | Object | (误判)Lead Entity | 0 命中 leadId | S1-155 已确认 | **F(= RecommendPhone)** |
| 29 | Object | (误判)Referral Entity | 0 命中 referralId | S1-155 已确认 | **F(= RecommendPhone)** |
| 30 | Object | (误判)Group Entity | 0 命中 groupId | S1-155 已确认 | **F(= GrouponProduct)** |
| 31 | Object | (误判)Seckill Entity | 0 命中 seckillId | S1-155 已确认 | **F(= SeckillProduct)** |
| 32 | Object | (误判)SmsTask Entity | 0 命中 smsId | S1-155/156 已确认 | **F(= taskXxxBatchSendId)** |
| 33 | Object | (误判)Clinic Entity | 0 命中 clinicId | S1-158 已确认 | **F** |
| 34 | Object | (误判)Report Entity | 0 命中 reportId | S1-156 已确认 | **F** |
| 35 | Object | (误判)Material Entity | 0 命中 materialId | S1-157 已确认 | **F** |
| 36 | Object | (误判)MedicalFee Entity | 0 命中 medicalFeeId | S1-157 已确认 | **F** |
| 37 | Object | (误判)CheckItem Entity | 0 命中 checkItemId | S1-157 已确认 | **F(= bodyCheckItem)** |

### 16.2 总冲突数

**37 项历史冲突定位**

### 16.3 修正影响 V4.4 的项

- ID 重命名 9 项
- Ctrl 命名误导 11 项
- Object 误判 15 项
- API 命名误导 2 项

**总计 37 项需要 V4.4 最终规格采纳**

---

## §17 L1 / L2 / L3

### L1 源码直接事实

- 32 份历史 MD
- 915 个 .json API
- 417 个 Controller 注册
- 45 个真实 ID
- 46+ 个禁造 ID
- ~250 个 Read API
- ~250 个 Write API

### L2 有限业务解释

- OptFlow PMS 是**单门店 → 多门店 SaaS** 视光门诊管理系统
- 包含 **12 个核心域**(已审计):Customer / Patient / MedicalRecord / Cashflow / Product / MachineCenter / Screening / Appointment / Marketing / Report / SystemSetting / Clinic
- **不允许**:
  - 凭业务经验创造 Entity
  - 凭中文菜单名创造 Object
  - 凭前端变量名推断 DB 表

### L3 数据库结构 / FK / 索引

- **全部 F / 未验证**
- 严禁:
  - 从 medicalRecordId 推断 DB FK
  - 从 companyId 推断 Company 表
  - 从任何前端 ID 推导数据库结构

---

## §18 API actual / Write actual / Production mutation

**API actual = 0 / Write actual = 0 / Production mutation = 0** ✓

仅执行:`Get-FileHash` / `git status` / `git add --` / `git commit` / `git push` / `python` 本地分析脚本(临时目录)/ `Get-ChildItem` 校验。

---

## §19 SHA256

| 文件 | SHA256 |
|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A |

---

## §20 Git 操作

- Commit:`b63e4f5dbf3d83e5469fa6555696727875cd5ca7`(S1-158 之后,S1-159 待提交)
- Branch:master
- Tracked = 229 / Untracked = 10 / Ignored = 1
- 本轮新增:`222_S1-159_*.md`
- 预期:Tracked = 230 / Untracked = 10 / Ignored = 1 / LOCAL == origin/master

---

## §21 V4.4 最终冻结红线

### 21.1 真实核心 Object 域(45 个 A ID)

| 域 | 数量 | ID 列表 |
|---|---:|---|
| 客户域 | 4 | customerId / patientId / customerCheckinId / printCheckinId |
| 病历域 | 1 | medicalRecordId |
| 收费域 | 1 | cashflowId |
| 商品域 | 7 | productId / skuId / productSkuId / stockInSkuId / medicalProductId / supplierId / mainSupplierId |
| 加工域 | 2 | machineCenterId / machineCenterOrderId |
| 预约域 | 4 | appointId / appointmentId / consultRoomId / bigScreenId |
| 筛查域 | 4 | schoolId / classId / schoolMateId / schoolMateCheckId |
| 随访域 | 1 | followUpId |
| 营销域 | 8 | orderId / couponId / customerCouponId / recommendPhoneId / grouponProductId / seckillProductId / promotionId / trainerCardId / customerTrainerCardId |
| 诊所域 | 7 | companyId / employeeId / adminId / adminRoleId / roleId / departmentId(弱) / corpTypeId |
| 配置域 | 4 | companyCashConfId / examineId / bodyCheckItemId / medicalCheckItem.id |
| 群发域 | 3 | taskTemplateBatchSendId / taskCouponBatchSendId / taskScreenTemplateBatchSendId |

### 21.2 禁造 Object / ID 域(46+ 个 F)

见 §3.2 / §11 完整列表。

### 21.3 命名归一化(37 项)

见 §8 / §16.1 完整列表。

### 21.4 命名误导最终修复

- `adminClinicCtrl` → ConsultRoomCtrl
- `feeBankCardCtrl` → feeWalletCtrl
- `chargeAdminCtrl` / `printConfigCtrl` → cashConfigCtrl
- `medicalFeesListCtrl` / `addMedicalFeeCtrl` / `modifyMedicalFeeCtrl` → examineListCtrl / addExamineCtrl / modifyExamineCtrl
- `memberTypeListCtrl` / `memberTypeModifyCtrl` / `addMemberTypeCtrl` → memberListCtrl / memberModifyCtrl / addMemberCtrl
- `addCheckCtrl` / `addCheckItemCtrl` / `checkListCtrl` / `checkModifyCtrl` → addExamineCtrl / addMedicalCheckItemCtrl / examineVoListCtrl / examineVoModifyCtrl
- `processCenterCtrl` → machineCenterCtrl
- `projectCardCtrl` / `addProjectCardCtrl` → trainerCardCtrl / addTrainerCardCtrl
- `appointOrderCtrl` → 删
- `memberCardCtrl` / `memberPointCtrl` → 删
- `corpCashConfId` → companyCashConfId
- `refundId` → refundOrderLogId
- `machineOrderOrderId` / `machineOrderId` → machineCenterOrderId
- `machineCenterVo` / `machineOrderVo` / `machineCenterVoList` → machineCenterOrderVoList

### 21.5 Admin ≠ Employee 永久红线

- `adminId` 21 真实 / `employeeId` 35 真实
- 两者**完全独立 Object**,不可合并
- Employee → Department / Role / ConsultRoom 均无 FK

### 21.6 Department 弱业务永久红线

- departmentId 1 命中(仅 State 参数)
- departmentName 0 命中,字段是 `departDesc`
- Employee → Department **无 FK**

### 21.7 L3 数据库结构永久 F

- 不能从前端变量名推断数据库表名
- 所有 FK / 索引 / 表结构 = F

### 21.8 API actual / Write actual / Production mutation

**必须永远保持 0**

---

## §22 最终交付清单

- **新文档**:`E:\C\minimax\OptFlow PMS\222_S1-159_全局核心Object_ID_API_Write_State交叉一致性审计.md`
- **历史 MD(190~221)**:32 份,**未修改任何**
- **controller.js / HTML**:**未修改**
- **tracked = 230 / untracked = 10 / ignored = 1 / LOCAL == origin/master**