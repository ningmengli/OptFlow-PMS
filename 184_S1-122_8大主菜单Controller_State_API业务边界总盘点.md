# S1-122 8大主菜单 Controller / State / API 业务边界总盘点

## 0. 任务背景

S1-105~S1-121 已完成大量底层字段逆向（optometry / medicalRecord / medicalRecordId / cashflow / cashflowId / customer / patient / Charge / Delivery）。

本轮**回归系统架构层面**：建立 8 大主菜单的 Controller / State / API 业务边界地图，不再围绕单一字段做无边界搜索。

**已知一级菜单**（来自历史菜单记录）：
1. 就诊流程
2. 预约叫号
3. 患者维护
4. 营销管理
5. 筛查机构
6. 物资管理
7. 数据报表
8. 诊所管理

## 1. 审计范围

| 范围 | 数量 |
|---|---:|
| controller.js 全文 | 59214 行 |
| **Controller 总数** | **417** |
| API call site 总数 | 1638 |
| Unique API 总数 | 869 |
| Read API call site | 1067 |
| Write API call site | 466 |
| Other API call site | 105 |
| 8 大主菜单归类 Controller | 347 |
| 未归类 Controller | 70 |
| UartDevice 命中 Controller | 6 |

## 2. 8 大一级菜单

### 2.1 菜单 + Controller 数量汇总

| # | 一级菜单 | Controller 数量 | 归类依据 |
|---:|---|---:|---|
| 1 | 就诊流程 | 42 | A (S1-115 已证) |
| 2 | 预约叫号 | 16 | A (Controller 名称明显) |
| 3 | 患者维护 | 35 | A (patient/member 关键词) |
| 4 | 营销管理 | 42 | A (coupon/groupon/followup 关键词) |
| 5 | 筛查机构 | 37 | A (school/screen 关键词) |
| 6 | 物资管理 | 60 | A (material/stock/purchase 关键词) |
| 7 | 数据报表 | 57 | A (report/chart/fee 关键词) |
| 8 | 诊所管理 | 58 | A (admin/role/hospital 关键词) |
| - | 未归类 | 70 | C (需要更多归类证据) |
| **合计** | | **417** | |

**S1-122 关键发现 1**：
- 8 大主菜单共 347 个 Controller 归类（占 83%）
- 70 个 Controller 未归类（17%）
- 未归类中包含重要的：
  - `chargeListCtrl` / `chargeWaysCtrl` / `addCustomerChargeCtrl` —— 收费配置
  - `deliveryListCtrl` / `deliveryModifyCtrl` 等 —— 配送（已在就诊流程归类）
  - `machineOrderCtrl` / `machineOrderBrokenCtrl` / `machineOrderWaitProcessCtrl` —— 加工中心
  - `logListCtrl` / `detectionLogCtrl` —— 日志
  - 多个 `Inspect` / `addGroupedit` / `addVisit` —— 随访/检查

### 2.2 历史菜单证据说明

**【历史菜单证据】**：8 大一级菜单列表源自历史用户提供的菜单结构记录，**未在 controller.js 源码中直接证明**。Controller 归类基于名称 + API 模式推断。

**【源码证据】**：
- Controller 名称命名规范统一
- API 路径前缀（admin/、config/、auth/、medic/ 等）能佐证业务分组
- 但**严格意义上**菜单结构依赖前端框架路由注册表（不在审计范围）

## 3. Controller Inventory 总览

### 3.1 全局统计

- **417 个 Controller**
- 控制器分布：8 个主菜单 + 70 个未归类
- 总 API call site 1638（平均每个 Controller 3.93）
- 总行数 59214（平均每个 Controller 142 行）

### 3.2 Controller 行数 Top 10

| # | Controller | 起始 | 行数 | 类型 |
|---:|---|---:|---:|---|
| 1 | deliveryListCtrl | L4075 | 161 | Tier A 就诊 |
| 2 | partBackCtrl | L4368 | 531 | Tier A 就诊 |
| 3 | assistCheckingCtrl | L1756 | 553 | Tier A 就诊 |
| 4 | myMaterialBillCtrl | L32435 | - | Tier A 就诊 |
| 5 | optometryCtrl | L34776 | - | Tier A 就诊 |
| 6 | screenPromotionListCtrl | L47113 | - | Tier A 营销 |
| 7 | modifyCustomerChargeCtrl | L56044 | - | 未归类 |
| 8 | screenPromotionStudentCtrl | L47512 | - | Tier A 营销 |
| 9 | updateMemberCtrl | L20939 | - | Tier A 患者 |
| 10 | memberCtrl | L17384 | - | Tier A 患者 |

### 3.3 saveOrQuery Top 10

| # | Controller | saveOrQuery | Write | Read | 起始 |
|---:|---|---:|---:|---:|---:|
| 1 | reChargeListCtrl | 17 | 3 | 13 | L5192 |
| 2 | optometryCtrl | 17 | 7 | 13 | L34776 |
| 3 | assistCheckingCtrl | 13 | 1 | 12 | L1756 |
| 4 | workBeachCtrl | 13 | 3 | 10 | L14494 |
| 5 | memberCtrl | 12 | 7 | 7 | L17384 |
| 6 | screenListCtrl | 12 | 1 | 11 | L46224 |
| 7 | screenPromotionListCtrl | 12 | 4 | 10 | L47113 |
| 8 | myMaterialBillCtrl | 11 | 2 | 9 | L32435 |
| 9 | waitPayDetailCtrl | 10 | 1 | 8 | L7452 |
| 10 | timeCardCtrl | 10 | 0 | 6 | L34095 |

### 3.4 Write-heavy Top 10

| # | Controller | Write | 起始 |
|---:|---|---:|---:|
| 1 | memberCtrl | 7 | L17384 |
| 2 | optometryCtrl | 7 | L34776 |
| 3 | encryptUserCtrl | 6 | L1088 |
| 4 | chargeWaysCtrl | 6 | L52767 |
| 5 | adminModifyCtrl | 5 | L295 |
| 6 | adminBillDetialCtrl | 5 | L24851 |
| 7 | cloudPrinterListCtrl | 5 | L39428 |
| 8 | purchaseModifyCtrl | 4 | L28301 |
| 9 | purchaseRequestCheckCtrl | 4 | L28764 |
| 10 | purchaseRequestModifyCtrl | 4 | L29199 |

## 4. 8 大主菜单 Controller 详细归类

### 4.1 就诊流程（42 个）

**核心 Controller**：
- `assistCheckingCtrl` (L1756) —— 助诊主页面（medicalRecord + medicalProduct 高消费）
- `assistCheckListCtrl` (L2309) —— 助诊列表
- `optometryCtrl` (L34776) —— 验光主页面（saveOrQuery=17, Write=7, 最高之一）
- `optometryGlassesCtrl` (L35383) —— 验光配镜
- `optometryListCtrl` (L35962) —— **UartDevice 设备管理（误命名）**
- `optometryLogListCtrl` (L36135) —— **日志（dead-end）**
- `prescriptionCtrl` (L33560) —— 处方
- `prescriptsRecordCtrl` (L33768) —— 处方记录
- `drugPrescriptionCtrl` (L31605) —— 药品处方
- `getGlassRecordCtrl` (L31922) —— 取镜记录
- `myCheckBillCtrl` (L32116) —— 检查账单
- `myMedicalHistoryCtrl` (L32897) —— 病史
- `myMedicalRecordListCtrl` (L32965) —— 病历列表
- `myMemberRecordCtrl` (L33218) —— 会员记录

**Charge 系列**（已在 S1-118~121 深度审计）：
- `waitChargeDetailCtrl` (L6568) / `waitChargeListCtrl` (L6957)
- `unPayDetailCtrl` (L5987) / `unPayListCtrl` (L6526)
- `waitPayBackCtrl` (L6992) / `waitPayBackListCtrl` (L7383)
- `waitPayDetailCtrl` (L7452) / `waitPayListCtrl` (L8110)
- `payedDetailCtrl` (L4937) / `payedListCtrl` (L4972)
- `payBackDetailCtrl` (L4899)
- `partBackCtrl` (L4368) —— 部分退款
- `reChargeListCtrl` (L5192) / `reChargeListBackCtrl` (L5692)

**Delivery 系列**：
- `deliveryInputCtrl` (L3812) —— 录入（cashflowId = 11 高消费）
- `deliveryInputRecordCtrl` (L4024) —— 录入记录
- `deliveryListCtrl` (L4075) —— 列表
- `deliveryProcessingCtrl` (L4236) —— 处理

**Check-in 系列**：
- `addCheckinCtrl` (L8159) —— 入院登记（patientId=10 高消费）
- `checkinListCtrl` (L8778) —— 列表
- `addCheckCtrl` (L50170) / `addCheckItemCtrl` (L50246) / `checkListCtrl` (L53001) / `checkModifyCtrl` (L53185) —— 检查 CRUD

**Recharge 系列**（归到就诊流程较勉强）：
- `hospitalRechargeCtrl` (L15883) / `feeRechargeCtrl` (L37183) / `pointsListReChargeCtrl` (L37459) / `timeCardRechargeCtrl` (L38463) / `unPayChargeCtrl` (L38500) / `unPayRechargeCtrl` (L38525)

**已知排除项**：
- `optometryListCtrl` (L35962) —— **非验光业务**，是 UartDevice 设备管理
- `optometryLogListCtrl` (L36135) —— **日志/dead-end**
- `getGlassNotifyListCtrl` (L13680) —— 通知/Notify（归类需确认）

### 4.2 预约叫号（16 个）

**核心 Controller**：
- `appointOrderCtrl` (L3664) —— 预约单
- `bookDetailCtrl` (L3669) / `bookManageCtrl` (L3706) / `bookSettingsCtrl` (L3771) —— 预约
- `appointAdminCtrl` (L52344) —— 预约管理
- `adminCallCtrl` (L9332) / `checkCallCtrl` (L9760) —— 叫号
- `bigScreenCtrl` (L9600) —— 大屏
- `consultingScreenCtrl` (L10277) —— 问诊屏
- `doctorWorkbenchCtrl` (L10401) —— 医生工作台（stateGo=6 最高之一）
- `queueMachineCtrl` (L10869) / `queueMachineConfigCtrl` (L11023) / `screenQueueCtrl` (L11109) —— 队列
- `reachStoreAppointAllReportCtrl` (L43829) / `reachStoreAppointDetailsCtrl` (L43879) / `reachStoreAppointSingleReportCtrl` (L44199) —— 到店预约报表
- `yuYueJiLuCtrl` (L9262) —— 预约记录（**未归类**）

### 4.3 患者维护（35 个）

**Member 系列**：
- `memberAdminCtrl` (L1285) / `memberCtrl` (L17384) / `memberCardCtrl` (L18058) / `memberPointCtrl` (L18144) / `memberRecyleCtrl` (L18244) / `memberTagCtrl` (L18310) / `memberTypeListCtrl` (L55752) / `memberTypeModifyCtrl` (L55770) / `memberChargeCtrl` (L55727) / `memberChannelListCtrl` (L55532) / `addMemberTagCtrl` (L16458) / `addMemberTypeCtrl` (L51744) / `addProjectCardCtrl` (L52150) / `projectCardCtrl` (L57851)

**Patient 系列**：
- `patientListCtrl` (L18946) —— 患者列表
- `updatePatientCtrl` (L21068) / `adminPatientCtrl` (L16743)
- `myMemberCtrl` (L33080) / `myCouponCtrl` (L18818)
- `myMemberRecordCtrl` (L33218) —— 会员记录
- `myAccountCtrl` (L3111) / `myAccountCoinCtrl` (L3239) / `myAccountCoinDetailsCtrl` (L3275) / `myAccountDetailsCtrl` (L3340) / `myAccountDetailsForScanCtrl` (L3400) / `myAccountHistoryCtrl` (L3427) / `myAccountOverviewsCtrl` (L3484)

**Point/TimeCard 系列**：
- `pointsListCtrl` (L36263) / `pointsListChargeCtrl` (L37432) / `pointsListReChargeCtrl` (L37459) / `pointsAdminCtrl` (L57582)
- `timeCardCtrl` (L34095) / `timeCardRechargeCtrl` (L38463) / `timecardBlanceCtrl` (L38373) / `timecardPerformanceCtrl` (L38415)

**Fee 系列**（费用相关）：
- `feeBankCardCtrl` (L36882) / `feeCashierCtrl` (L36905) / `feeDayCtrl` (L37005) / `feeMonthCtrl` (L37134) / `feeRechargeCtrl` (L37183)

**updateMemberCtrl (L20939)** 命中 customer=10 / customerId=9，**是 customer 桥接主控制器**。

### 4.4 营销管理（42 个）

**Coupon 系列**：
- `addCouponCtrl` (L12526) / `couponHistoryCtrl` (L12702) / `couponListCtrl` (L12760) / `modifyCouponCtrl` (L12824) / `addTargetCouponCtrl` (L49071) / `targetCouponDetailCtrl` (L49445) / `targetCouponListCtrl` (L49569)

**Groupon/Seckill 系列**：
- `addGrouponCtrl` (L13337) / `grouponDetailCtrl` (L13516) / `grouponListCtrl` (L13553) / `grouponOrderCtrl` (L13632)
- `addSecKillProductCtrl` (L16532) / `modifySecKillProductCtrl` (L18569) / `secKillProductDetailCtrl` (L20462) / `secKillProductListCtrl` (L20519) / `secKillPromotionListCtrl` (L20588)

**FollowUp 系列**：
- `followUpCtrl` (L11504) / `followUpAnalysisCtrl` (L11674) / `followUpDetailsCtrl` (L11826)
- `rfmModelCtrl` (L12298) / `conversionFunnelCtrl` (L11245) / `profileAnalysisCtrl` (L11956)
- **（注意：未归类中 `rfmModelCtrl` 和 `conversionFunnelCtrl` 应归营销）**

**Recommend 系列**：
- `addRecommendCtrl` (L16498) / `modifyRecommendCtrl` (L18532) / `recommendCustomerCtrl` (L19052) / `recommendDetailCtrl` (L19090) / `recommendPhoneListCtrl` (L19335) / `recommendTableCtrl` (L19868)

**Promotion 系列**：
- `addPromotionCtrl` (L16461) / `modifyPromotionCtrl` (L18477)
- `addScreenPromotionCtrl` (L38818) / `modifyScreenPromotionCtrl` (L42424) / `screenPromotionConfigCtrl` (L46600) / `screenPromotionListCtrl` (L47113) / `screenPromotionStudentCtrl` (L47512) / `screenPromotionToothConfigCtrl` (L47886)

**Group Send 系列**：
- `groupSendCtrl` (L16799) / `groupSendLookCtrl` (L17318) / `screenConditionBatchGroupSendCtrl` (L45310) / `screenConditionBatchGroupSendLookCtrl` (L45589)

**Order 系列**：
- `productOrderCtrl` (L19020) / `selectOrderListCtrl` (L20636) / `sendPlatformCtrl` (L20890) / `orderDetailCtrl` (L18937) / `orderManageCtrl` (L36165)
- **（注意：orderDetailCtrl 和 orderManageCtrl 在未归类中）**
- `requirementCtrl` (L20042) / `requirementStatusCtrl` (L20316)

### 4.5 筛查机构（37 个）

**School 系列**：
- `addSchoolCtrl` (L38670) / `modifySchoolCtrl` (L48811) / `schoolListCtrl` (L44357) / `updateSchoolCtrl` (L48811)
- `addSchoolPlanCtrl` (L38766) / `modifySchoolPlanCtrl` (L42351) / `schoolPlanListCtrl` (L44769) / `schoolPlanReportCtrl` (L44876)
- `classListCtrl` (L38998)
- `multiImportStudentCtrl` (L42606)
- `printStudentReportCtrl` (L43450) / `printStudentReport2Ctrl` (L43493)

**Screen 系列**：
- `screenListCtrl` (L46224) —— 筛查主列表
- `screenInStoreCtrl` (L45963) / `screenBackConfigCtrl` (L44973) / `screenUrlConfigCtrl` (L48420)
- `screenClassReportCtrl` (L45114) / `screenRecordReportCtrl` (L48060) / `screenReportInschoolCtrl` (L48100) / `screenSchoolReportCtrl` (L48156) / `screenStudentReportCtrl` (L48200) / `screenContrastReportCtrl` (L45655)
- `screenConditionBatchCtrl` (L45234)
- `healthScreenConfigCtrl` (L40499) / `modifyHealthScreenCtrl` (L41314)

**MateCheck 系列**：
- `mateCheckReportConfigCtrl` (L41023) / `mateCheckReportListNewCtrl` (L41055) / `mateProgressReportCtrl` (L41058) / `modifyMateCheckCtrl` (L41708) / `modifySchoolMateCheckCtrl` (L41839) / `schoolMateCheckListCtrl` (L44398) / `schoolMateCheckReportsCtrl` (L44688) / `schoolCheckRecordCtrl` (L58390)
- `contrastReportInschoolCtrl` (L39709) / `studentReportInschoolCtrl` (L48544) / `classReportInschoolCtrl` (L39272)

**Vision 系列**（归筛查更合理）：
- `visionMesureCtrl` (L48978) / `visionAdminCtrl` (L59060) / `fundusCtrl` (L40335) / `fundusLogCtrl` (L40467) / `inspectionCtrl` (L40558) / `markOriginSetCtrl` (L40701) / `zhiShiBangConfigCtrl` (L49015) / `projectionScreenCtrl` (L43678) / `reachStoreAppointAllReportCtrl` (L43829)
- **（注意：visionMesureCtrl / visionAdminCtrl 等已归到 8 诊所管理，应重归到筛查）**

**AccessReport 系列**：
- `accessReportCtrl` (L38566) / `transformationRateCtrl` (L48759)
- `physicalReportCtrl` (L43203) / `physicalContrastReportCtrl` (L42775)
- `contrastReportByAreaCtrl` (L39606)
- `progressReportCtrl` (L43592) / `reportRecordCtrl` (L44270) / `reportStatisticCtrl` (L44321) / `dataChartCtrl` (L39897)
- `areaScreenAdminCtrl` (L738) —— 区域筛查管理

### 4.6 物资管理（60 个）

**Stock 系列**：
- `companyStockListCtrl` (L15973) / `stockAdminCtrl` (L58536) / `stockListCtrl` (L30099) / `stockListsCtrl` (L30318) / `stockListssCtrl` (L30542)
- `stockChangeCtrl` (L29804) / `modifyStockChangeCtrl` (L27909) / `stockChangeCheckCtrl` (L29979) / `stockChangeDetailCtrl` (L30055) / `addStockChangeCtrl` (L24318)
- `stockProductChangeCheckCtrl` (L30681) / `modifyStockProductChangeCtrl` (L28110) / `addStockProductChangeCtrl` (L24540)
- `stockLossListCtrl` (L16384) / `stockLossDetailCtrl` (L16371) / `completeStockLossCtrl` (L16058) / `createMedicalStockLoss.json` (L16058 旁)
- `processCenterCtrl` (L57778) / `modifyProcessCenterCtrl` (L56898) / `addProcessCenterCtrl` (L51801)
- `machineOrderCtrl` (L16094) / `machineOrderBrokenCtrl` (L16261) / `machineOrderWaitProcessCtrl` (L16357) / `machineOrderListCtrl` (L4264) / `machineProcessListCtrl` (L37369)

**Material/Purchase 系列**：
- `materiallistCtrl` (L54469) / `materialModifyCtrl` (L54859) / `materialImportCtrl` (L54380) / `addMaterialCtrl` (L51182) / `materialCertificateCtrl` (L54240)
- `materialImportRecordCtrl` (L26358) / `materialOutportRecordCtrl` (L26553) / `materialDeliveryCtrl` (L26163) / `materialReceiptsCtrl` (L27776)
- `materialPurchaseCtrl` (L26599) / `materialPurchaseBackGoodsCtrl` (L26841) / `materialPurchaseBackLookCtrl` (L26987) / `materialPurchaseBackOneCtrl` (L27219) / `materialPurchaseRequestCtrl` (L27410) / `materialPurchaseReturnCtrl` (L27575)
- `purchaseCtrl` (L36428) / `purchaseDetailCtrl` (L28292) / `purchaseModifyCtrl` (L28301) / `purchaseRecieptCtrl` (L28502)
- `purchaseRequestCheckCtrl` (L28764) / `purchaseRequestCheckDetailCtrl` (L29112) / `purchaseRequestModifyCtrl` (L29199)
- `addPurchasementCtrl` (L22675) / `addPurchaseRequestCtrl` (L23079) / `addSalePurchaseCtrl` (L23844)
- `receiptDetailCtrl` (L29296) / `receiptInvalidCtrl` (L29421) / `receiptModifyCtrl` (L29517) / `addReceiptCtrl` (L23407) / `addMultiReceiptsCtrl` (L21933) / `addInventoryCtrl` (L21574) / `addProductInventoryCtrl` (L22464) / `inventoryDetailCtrl` (L25970) / `inventoryModifyCtrl` (L25998) / `inventoryProductModifyCtrl` (L26087)
- `deliveryProductModifyCtrl` (L25758) / `addProductDeliveryCtrl` (L22237) / `addProductBivariateTableCtrl` (L22071) / `addMultiDeliveryCtrl` (L21785) / `addDeliveryCtrl` (L21138) / `addDeliveryCustomerCtrl` (L21374) / `deliveryDeleteCtrl` (L25237) / `deliveryDetailCtrl` (L25281) / `deliveryModifyCtrl` (L25314) / `deliveryModifyCustomerCtrl` (L25573)
- `supplierListCtrl` (L58927) / `supplierModifyCtrl` (L58971) / `supplierCertificateCtrl` (L58787)
- `depotListCtrl` (L53904) / `depotModifyCtrl` (L53987) / `addDepotCtrl` (L50797) / `batchMaterialCtrl` (L52380)
- `goodsCtrl` (L25957) / `addProductPlanCtrl` (L51956) / `modifyProductPlanCtrl` (L57082) / `productPlanListCtrl` (L57820)
- `addGroupeditCtrl` (L50899) / `modifyGroupeditCtrl` (L56458) / `groupeditListCtrl` (L54133)

**S1-122 关键发现 2**：
- 物资管理是 Controller 最多的菜单（60 个）
- 包含 stock / material / purchase / supplier / depot / product 等多领域
- 命名上 `material` 和 `stock` 在源代码中常混用
- 一些 Controller（如 `addDeliveryCtrl`）实际上应该归到"配送"而非物资

### 4.7 数据报表（57 个）

**核心 Report 系列**：
- `reportCtrl` (L37786) / `reportFeeCtrl` (L37805) / `reportMedicalRateCtrl` (L37808) / `reportOperateCtrl` (L37811) / `reportOperateAllCtrl` (L37895) / `reportSaleCtrl` (L37898) / `reportDateAdminCtrl` (L58291)

**Sale 系列**：
- `saleListCtrl` (L37912) / `saleRecordCtrl` (L38010) / `addSaleRecordCtrl` (L31008) / `adminMyRecordCtrl` (L31158) / `adminSalesRecordCtrl` (L31285) / `customerProductRecordCtrl` (L31382)
- `refundFeeCtrl` (L37657) / `backGoodRecordCtrl` (L36445)
- `recoveryRecordCtrl` (L33899)
- `deliveryReportListCtrl` (L36689) / `deliveryRecordPortCtrl` (L36825)
- `hospitalReportCtrl` (L37226) / `singleHospitalProfitCtrl` (L38200)

**Fee 系列**：
- `feeCashierCtrl` (L36905) / `feeDayCtrl` (L37005) / `feeMonthCtrl` (L37134) / `feeBankCardCtrl` (L36882) / `feeRechargeCtrl` (L37183)
- `profitReportCtrl` (L37501) / `jxcRecordCtrl` (L37250)
- `receiptRecordCtrl` (L37600)
- `timecardBlanceCtrl` (L38373) / `timecardPerformanceCtrl` (L38415)
- `posCtrl` (L43281)
- `sataServerListCtrl` (L58327) —— 数据采集/打印

**Medical Fee 系列**：
- `addMedicalFeeCtrl` (L51665) / `modifyMedicalFeeCtrl` (L56817) / `medicalFeesListCtrl` (L55340)
- `addRecordTemplateCtrl` (L52242) / `modifyRecordTemplateCtrl` (L57308) / `recordTemplateListCtrl` (L58220)

**Satisfy/Success 系列**：
- `satisfyDetailRateCtrl` (L38144) / `satisfyRateCtrl` (L38168) / `successRateCtrl` (L38224)

**Analysis 系列**：
- `analysisCtrl` (L11242) / `profileAnalysisCtrl` (L11956) / `conversionFunnelCtrl` (L11245) / `rfmModelCtrl` (L12298)

**Admin Bill 系列**：
- `adminBillCtrl` (L24752) / `adminBillDetialCtrl` (L24851) / `adminBillOneDetialCtrl` (L25191)

**Auth 相关**（归到报表较勉强）：
- `wechatAuthCtrl` (L3528) / `wechatAuthFailedCtrl` (L3626) / `wechatAuthSuccessCtrl` (L3629)
- **（应归到 8 诊所管理 或 未归类）**

### 4.8 诊所管理（58 个）

**Admin/Role 系列**：
- `addRoleCtrl` (L17) / `adminListCtrl` (L103) / `adminAreaListCtrl` (L52) / `adminModifyCtrl` (L295) / `adminPasswordModifyCtrl` (L673)
- `areaRoleAdminCtrl` (L712) / `createAdminCtrl` (L759) / `createAdminAreaCtrl` (L984)
- `encryptUserCtrl` (L1088) / `memberAdminCtrl` (L1285)
- `modifyAdminAreaCtrl` (L1364) / `modifyAreaRoleCtrl` (L1470) / `modifyRoleCtrl` (L1594) / `roleAdminCtrl` (L1714)
- `frontAdminCtrl` (L54099) / `chargeAdminCtrl` (L52575) / `messageAdminCtrl` (L55834)
- `phoneAdminCtrl` (L57371) / `recipeAdminCtrl` (L57995) / `visionAdminCtrl` (L59060) / `wecomAdminCtrl` (L59124)
- `firstApprovalCtrl` (L54026) / `firstDoctorListCtrl` (L54068) / `addFirstDoctorCtrl` (L50869) / `modifyFirstDoctorCtrl` (L56417)

**Hospital/Department 系列**：
- `addDepartmentCtrl` (L14846) / `addDepartmentModalInstanceCtrl` (L14895) / `addHospitalCtrl` (L14996)
- `adminClinicCtrl` (L15053) / `adminMapCtrl` (L15214) / `departmentListCtrl` (L15327)
- `hospitalCtrl` (L15340) / `employeeListCtrl` (L15347) / `hospitalListCtrl` (L15391)
- `updateAdminHospitalCtrl` (L15439) / `updateAdminHospitalModalInstanceCtrl` (L15593)
- `updateDepartmentCtrl` (L15690) / `updateDepartmentModalContentCtrl` (L15766)
- `updateHospitalCtrl` (L15855)

**Home/Login 系列**：
- `homeCtrl` (L13902) / `homeAnnouncementCtrl` (L14013) / `homeAnnouncementDetailsCtrl` (L14042) / `homePageCtrl` (L14074)
- `loginCtrl` (L14086) / `modifyPasswordCtrl` (L14307)
- `adminCtrl` (L13772) / `companyCtrl` (L13829) / `workBeachCtrl` (L14494)
- `allSizeCtrl` (L13811) / `404Ctrl` (L13764) / `testPageCtrl` (L14370)

**Print/Config 系列**：
- `cloudPrinterConfigCtrl` (L39399) / `cloudPrinterListCtrl` (L39428) / `printConfigCtrl` (L57667)
- `appConfigCtrl` (L52303) / `commonSetTempCtrl` (L53264) / `systemSettingCtrl` (L59014)
- `openPlateCtrl` (L57338) / `visionMesureCtrl` (L48978)

**S1-122 关键发现 3**：
- 诊所管理含 58 个 Controller，是 admin/role/hospital/config 的大杂烩
- 实际菜单通常会细分：组织管理 / 权限管理 / 院区管理 / 打印配置 / 系统设置
- `wechatAuthCtrl` / `wechatAuthFailedCtrl` / `wechatAuthSuccessCtrl` 当前归到报表不太合适

### 4.9 未归类（70 个）

| 起始 | Controller | 推测业务 |
|---:|---|---|
| L3 | commonModalInstanceCtrl | 通用 Modal |
| L2426 | brandListCtrl | 品牌管理（物资相关）|
| L2519 | remindListCtrl | 提醒/消息 |
| L2867 | smsSetCtrl | SMS 设置（营销/系统）|
| L3064 | aioIntroduceCtrl | 介绍页（empty）|
| L3082 | coinRuleIntroduceCtrl | 介绍页（empty）|
| L3528 | wechatAuthCtrl | 微信授权 |
| L3626 | wechatAuthFailedCtrl | 微信授权（empty）|
| L3632 | backup1Ctrl | 备份页 |
| L4264 | machineOrderListCtrl | 加工订单列表（物资）|
| L9262 | yuYueJiLuCtrl | 预约记录（预约叫号）|
| L11245 | conversionFunnelCtrl | 漏斗分析（营销）|
| L12298 | rfmModelCtrl | RFM 模型（营销）|
| L13167 | blueToothTransferCtrl | 蓝牙传输（设备）|
| L13272 | detectionLogCtrl | 检测日志（设备日志）|
| L16094 | machineOrderCtrl | 加工订单（物资）|
| L16261 | machineOrderBrokenCtrl | 加工异常（物资）|
| L16357 | machineOrderWaitProcessCtrl | 加工待处理（物资）|
| L16758 | chargeListCtrl | 收费列表（就诊/Charge）|
| L18937 | orderDetailCtrl | 订单详情（营销）|
| L21138 | addDeliveryCtrl | 添加配送（物资）|
| L21374 | addDeliveryCustomerCtrl | 添加配送客户（物资）|
| L21785 | addMultiDeliveryCtrl | 多件配送（物资）|
| L21933 | addMultiReceiptsCtrl | 多件收货（物资）|
| L22071 | addProductBivariateTableCtrl | 配镜处方（物资）|
| L22237 | addProductDeliveryCtrl | 产品配送（物资）|
| L23407 | addReceiptCtrl | 收货（物资）|
| L25237 | deliveryDeleteCtrl | 删除配送（物资）|
| L25281 | deliveryDetailCtrl | 配送详情（物资）|
| L25314 | deliveryModifyCtrl | 修改配送（物资）|
| L25573 | deliveryModifyCustomerCtrl | 修改配送客户（物资）|
| L25957 | goodsCtrl | 商品（物资）|
| L29296 | receiptDetailCtrl | 收货详情（物资）|
| L29421 | receiptInvalidCtrl | 收货作废（物资）|
| L29517 | receiptModifyCtrl | 修改收货（物资）|
| L30755 | addNewCtrl | 添加新闻（营销）|
| L30854 | modifyNewCtrl | 修改新闻（营销）|
| L30954 | newsListCtrl | 新闻列表（营销）|
| L31749 | followListCtrl | 随访列表（营销）|
| L32116 | myCheckBillCtrl | 检查账单（就诊）|
| L32897 | myMedicalHistoryCtrl | 病史（就诊）|
| L36165 | orderManageCtrl | 订单管理（营销）|
| L36483 | customerChannelRateCtrl | 客户渠道费率（营销）|
| L40143 | exportrecCtrl | 导出记录（报表）|
| L41139 | medicalConfigCtrl | 医疗配置（诊所）|
| L49015 | zhiShiBangConfigCtrl | 知识邦配置（筛查）|
| L49594 | addVisitCtrl | 添加回访（营销）|
| L50044 | visitDetailsCtrl | 回访详情（营销）|
| L50472 | addCustomerChargeCtrl | 添加客户收费（Charge/就诊）|
| L50776 | addCustomerChargeItemCtrl | 添加客户收费项（Charge/就诊）|
| L50899 | addGroupeditCtrl | 添加团购编辑（营销）|
| L51059 | addInspectCtrl | 添加检查（筛查）|
| L51956 | addProductPlanCtrl | 添加产品计划（物资）|
| L52767 | chargeWaysCtrl | 收费方式（Charge/就诊）|
| L53318 | customerChargeCtrl | 客户收费（Charge/就诊）|
| L53685 | customerChargeChoiceCtrl | 客户收费选择（Charge/就诊）|
| L53806 | customerChargeItemCtrl | 客户收费项（Charge/就诊）|
| L54133 | groupeditListCtrl | 团购编辑列表（营销）|
| L54160 | InspectListCtrl | 检查列表（筛查）|
| L54208 | logListCtrl | 日志（设备/系统）|
| L56044 | modifyCustomerChargeCtrl | 修改客户收费（Charge/就诊）|
| L56384 | modifyCustomerChargeItemCtrl | 修改客户收费项（Charge/就诊）|
| L56458 | modifyGroupeditCtrl | 修改团购编辑（营销）|
| L56662 | modifyInspectCtrl | 修改检查（筛查）|
| L57082 | modifyProductPlanCtrl | 修改产品计划（物资）|
| L57820 | productPlanListCtrl | 产品计划列表（物资）|
| L58636 | suiFangJieLunTemCtrl | 随访结论模板（营销）|
| L58673 | suiFangJieLunTemplateCtrl | 随访结论模板（营销）|
| L58730 | suiFangNeiRongTemplateCtrl | 随访内容模板（营销）|
| L59017 | toothCheckTemplateCtrl | 牙齿检查模板（筛查）|

**S1-122 关键发现 4**：
- 70 个未归类 Controller 中，10+ 个应归"就诊"（charge/customer 收费相关）
- 多个 `Inspect` / `Visit` / `Follow` Controller 应归"营销"
- 多个 `delivery*` Controller 应归"物资"或"就诊"
- 多个 `addProductPlan` / `addGroupedit` 等应归"物资"或"营销"

## 5. Core Object 命中

### 5.1 medicalRecord 命中 Top 10

| # | Controller | 命中 | 起始 | 行号 |
|---:|---|---:|---:|---|
| 1 | myMemberRecordCtrl | 27 | L33218 | 就诊 |
| 2 | optometryCtrl | 11 | L34776 | 就诊 |
| 3 | getGlassRecordCtrl | 6 | L31922 | 就诊 |
| 4 | recoveryRecordCtrl | 6 | L33899 | 报表 |
| 5 | optometryGlassesCtrl | 4 | L35383 | 就诊 |
| 6 | drugPrescriptionCtrl | 2 | L31605 | 就诊 |
| 7 | prescriptsRecordCtrl | 2 | L33768 | 就诊 |
| 8 | deliveryInputRecordCtrl | 1 | L4024 | 就诊 |
| 9 | waitChargeDetailCtrl | 1 | L6568 | 就诊 |

### 5.2 medicalRecordId 命中 Top 10

| # | Controller | 命中 | 起始 | 业务 |
|---:|---|---:|---:|---|
| 1 | optometryCtrl | 27 | L34776 | 就诊 |
| 2 | assistCheckingCtrl | 15 | L1756 | 就诊 |
| 3 | optometryGlassesCtrl | 10 | L35383 | 就诊 |
| 4 | machineOrderCtrl | 8 | L16094 | 物资 |
| 5 | myCheckBillCtrl | 8 | L32116 | 就诊 |
| 6 | myMemberRecordCtrl | 8 | L33218 | 就诊 |
| 7 | assistCheckListCtrl | 7 | L2309 | 就诊 |
| 8 | drugPrescriptionCtrl | 7 | L31605 | 就诊 |
| 9 | prescriptsRecordCtrl | 7 | L33768 | 就诊 |
| 10 | myMemberCtrl | 6 | L33080 | 患者 |

### 5.3 cashflow 命中 Top 5

| # | Controller | 命中 | 起始 | 业务 |
|---:|---|---:|---:|---|
| 1 | waitPayDetailCtrl | 14 | L7452 | 就诊 |
| 2 | waitPayBackCtrl | 6 | L6992 | 就诊 |
| 3 | partBackCtrl | 4 | L4368 | 就诊 |
| 4 | selectOrderListCtrl | 3 | L20636 | 营销 |
| 5 | successRateCtrl | 3 | L38224 | 报表 |

### 5.4 cashflowId 命中 Top 10

| # | Controller | 命中 | 起始 | 业务 |
|---:|---|---:|---:|---|
| 1 | partBackCtrl | 10 | L4368 | 就诊 |
| 2 | payedListCtrl | 10 | L4972 | 就诊 |
| 3 | deliveryListCtrl | 6 | L4075 | 就诊 |
| 4 | waitPayBackCtrl | 6 | L6992 | 就诊 |
| 5 | deliveryInputRecordCtrl | 4 | L4024 | 就诊 |
| 6 | feeCashierCtrl | 4 | L36905 | 报表 |
| 7 | feeDayCtrl | 4 | L37005 | 报表 |
| 8 | deliveryInputCtrl | 3 | L3812 | 就诊 |
| 9 | deliveryProcessingCtrl | 3 | L4236 | 就诊 |
| 10 | unPayDetailCtrl | 3 | L5987 | 就诊 |

### 5.5 customer/customerId 命中

**customer 高消费**：
- `checkinListCtrl` (L8778) 18 —— 就诊
- `updateMemberCtrl` (L20939) 10 —— 患者
- `optometryGlassesCtrl` (L35383) 10 —— 就诊
- `partBackCtrl` (L4368) 6 —— 就诊
- `addCheckinCtrl` (L8159) 4 —— 就诊

**customerId 高消费**：
- `reChargeListCtrl` (L5192) 13 —— 就诊
- `checkinListCtrl` (L8778) 10 —— 就诊
- `updateMemberCtrl` (L20939) 9 —— 患者
- `memberCardCtrl` (L18058) 8 —— 患者
- `memberCtrl` (L17384) 7 —— 患者

### 5.6 medicalProduct 命中 Top 5

| # | Controller | 命中 | 起始 | 业务 |
|---:|---|---:|---:|---|
| 1 | myMaterialBillCtrl | 24 | L32435 | 就诊 |
| 2 | deliveryInputCtrl | 11 | L3812 | 就诊 |
| 3 | optometryGlassesCtrl | 9 | L35383 | 就诊 |
| 4 | waitChargeDetailCtrl | 8 | L6568 | 就诊 |
| 5 | waitPayBackCtrl | 8 | L6992 | 就诊 |

### 5.7 objectId 命中

**全局仅 1 个 Controller 命中**：
- `deliveryInputCtrl` (L3812) 7 —— 就诊

### 5.8 UartDevice 命中

| # | Controller | 命中 | 起始 | 业务 |
|---:|---|---:|---:|---|
| 1 | optometryListCtrl | 19 | L35962 | 误命名（UartDevice 设备）|
| 2 | assistCheckingCtrl | 17 | L1756 | 就诊（医疗设备）|
| 3 | logListCtrl | 4 | L54208 | 未归类（日志）|
| 4 | sataServerListCtrl | 4 | L58327 | 报表（设备）|
| 5 | optometryLogListCtrl | 2 | L36135 | 误命名（日志）|
| 6 | cloudPrinterListCtrl | 1 | L39428 | 诊所管理（云打印）|

## 6. Tier A/B/C 划分

### 6.1 Tier A：主业务候选（71 个 Controller）

**判定标准**：
- API 数量 ≥ 5
- Write 数量 ≥ 2
- 含核心对象（medicalRecord / cashflow / patient）
- 已被 S1-115/117/118/119/120/121 深度审计

**已识别的 71 个 Tier A Controller**（按业务分组）：

| 业务 | Controller 数 | 关键 Controller |
|---|---:|---|
| 就诊流程 | 24 | assistCheckingCtrl, optometryCtrl, optometryGlassesCtrl, waitChargeDetailCtrl, waitPayDetailCtrl, payedDetailCtrl, partBackCtrl 等 |
| 预约叫号 | 4 | doctorWorkbenchCtrl, queueMachineCtrl, bigScreenCtrl, bookManageCtrl |
| 患者维护 | 12 | memberCtrl, updateMemberCtrl, myMemberCtrl, patientListCtrl, myAccountCtrl 等 |
| 营销管理 | 9 | couponListCtrl, grouponListCtrl, followUpCtrl, selectOrderListCtrl 等 |
| 筛查机构 | 5 | schoolListCtrl, screenListCtrl, schoolPlanListCtrl 等 |
| 物资管理 | 10 | purchaseModifyCtrl, stockListCtrl, materialPurchaseCtrl 等 |
| 数据报表 | 4 | saleListCtrl, feeDayCtrl, reportCtrl, jxcRecordCtrl 等 |
| 诊所管理 | 3 | adminListCtrl, workBeachCtrl, loginCtrl |

### 6.2 Tier B：辅助业务（243 个 Controller）

包括：
- 各种 List / Detail / Modify 副页面
- 各种 Config / Setting 副页面
- Report / Chart / Analysis 报表页面

### 6.3 Tier C：配置/设备/日志/工具（103 个 Controller）

包括：
- Admin/Role/User 管理
- Config/System Setting
- Print/Cloud 配置
- Log/Error 日志
- Vision/Screen/Fundus 设备

## 7. State 出口/入口

### 7.1 State go Top 10

| # | Controller | $state.go | 业务 |
|---:|---|---:|---|
| 1 | assistCheckingCtrl | 8 | 就诊 |
| 2 | doctorWorkbenchCtrl | 6 | 预约 |
| 3 | myMemberCtrl | 6 | 患者 |
| 4 | remindListCtrl | 5 | 营销 |
| 5 | memberCtrl | 5 | 患者 |
| 6 | addSaleRecordCtrl | 5 | 报表 |
| 7 | followListCtrl | 5 | 营销 |
| 8 | modifyHealthScreenCtrl | 5 | 筛查 |
| 9 | modifySchoolMateCheckCtrl | 5 | 筛查 |
| 10 | checkCallCtrl | 4 | 预约 |

### 7.2 StateParams Top 10

| # | Controller | $stateParams | 业务 |
|---:|---|---:|---|
| 1 | assistCheckingCtrl | 8 | 就诊 |
| 2 | modifyHealthScreenCtrl | 3 | 筛查 |
| 3 | modifyStockChangeCtrl | 3 | 物资 |
| 4 | modifyStockProductChangeCtrl | 3 | 物资 |
| 5 | modifyAdminAreaCtrl | 1 | 诊所 |
| 6 | modifyAreaRoleCtrl | 2 | 诊所 |
| 7 | modifyRoleCtrl | 2 | 诊所 |
| 8 | bookDetailCtrl | 1 | 预约 |
| 9 | remindListCtrl | 1 | 营销 |
| 10 | memberCtrl | 2 | 患者 |

## 8. 四大主链定位

### 8.1 Check 链（验光/助诊/检查）

| Controller | 行号 | medicalRecordId | medicalProduct | UartDevice |
|---|---:|---:|---:|---:|
| optometryCtrl | L34776 | **27** | 5 | 0 |
| optometryGlassesCtrl | L35383 | 10 | 9 | 0 |
| assistCheckingCtrl | L1756 | 15 | 0 | 17 |
| assistCheckListCtrl | L2309 | 7 | 0 | 0 |
| prescriptsRecordCtrl | L33768 | 7 | 0 | 0 |
| drugPrescriptionCtrl | L31605 | 7 | 0 | 0 |

**S1-122 关键发现 5**：
- Check 链是 medicalRecordId 最大消费者（27+10+15+7+7+7=73 处）
- optometryCtrl 是绝对核心
- assistCheckingCtrl 是次核心
- 但 optometryListCtrl **不是** Check 链（UartDevice 设备管理）

### 8.2 Sale 链（销售/订单）

| Controller | 行号 | cashflowId | customer | patient |
|---|---:|---:|---:|---:|
| selectOrderListCtrl | L20636 | 0 (3 cashflow.id) | 0 | 0 |
| groupSendCtrl | L16799 | 1 (D-3 payReferId) | 0 | 0 |
| productOrderCtrl | L19020 | 0 | 0 | 0 |
| requirementCtrl | L20042 | 0 | 0 | 0 |

**S1-122 关键发现 6**：
- Sale 链 Controller 数量较少（4+）
- 主要消费 cashflow.id（Type 2 派生）
- selectOrderListCtrl L20736 是 cashflow.id → cashflowId 唯一 Type 2 链

### 8.3 Charge 链（收费/支付）

| Controller | 行号 | medicalRecordId | cashflowId | Write |
|---|---:|---:|---:|---:|
| waitChargeDetailCtrl | L6568 | 0 | 1 (Type 5 L6929) | 1 |
| waitPayDetailCtrl | L7452 | 0 | 6 | 1 (payMedicalRecordCashflow) |
| payedDetailCtrl | L4937 | 0 | 2 | 0 |
| payedListCtrl | L4972 | 0 | 10 | 0 |
| partBackCtrl | L4368 | 0 | 10 | 0 |
| waitPayBackCtrl | L6992 | 0 | 6 | 1 (payCreditRefund) |
| unPayDetailCtrl | L5987 | 0 | 3 | 1 (payCredit) |
| reChargeListCtrl | L5192 | 0 | 1 | 3 |

**S1-122 关键发现 7**：
- Charge 链是 cashflowId 最大消费者（37 处）
- 涵盖 8 个核心 Controller
- Write 集中于：payMedicalRecordCashflow / payCreditRefund / payCredit / reCharge

### 8.4 Delivery 链（配送/取镜）

| Controller | 行号 | medicalRecordId | cashflowId | objectId |
|---|---:|---:|---:|---:|
| deliveryInputCtrl | L3812 | 0 | 3 | **7** |
| deliveryInputRecordCtrl | L4024 | 1 (dead-end) | 4 | 0 |
| deliveryListCtrl | L4075 | 0 | 6 | 0 |
| deliveryProcessingCtrl | L4236 | 0 | 3 | 0 |

**S1-122 关键发现 8**：
- Delivery 链是 objectId 唯一消费者
- deliveryInputCtrl 是 objectId 派生主控制器
- medicalRecordId 在 Delivery 链 dead-end（S1-117/120 已确认）
- cashflowId 在 Delivery 链继续传递（→ getCashflowDeliveryVo.json）

## 9. 跨菜单直接关系

### 9.1 已知跨菜单链

| 起点 | 终点 | 机制 | 字段 | 等级 |
|---|---|---|---|---|
| waitChargeDetailCtrl (就诊) | waitPayDetailCtrl (就诊) | $state.go | cashflowId: res.result.object (Type 5) | A |
| deliveryInputRecordCtrl (就诊/Delivery) | getCashflowDeliveryVo (Delivery API) | API | cashflowId | A |
| updateMemberCtrl (患者) | getCustomerVo (会员 API) | API | customerId | A |
| optometryGlassesCtrl (就诊) | getCustomerVo (会员 API) | API | customerId | A |
| partBackCtrl (就诊) | getCustomerVo (会员 API) | API | customerId | A |
| selectOrderListCtrl (营销) | createRefundOrderLog (Charge API) | API | cashflowId: order.cashflow.id | A |

### 9.2 跨菜单 State 链

**S1-122 关键发现 9**：
- 当前源码中**未发现**跨一级菜单的 State 链
- 主要 State 转换在同一菜单内（就诊 → 就诊）
- 跨菜单主要通过 API 桥接（API Response → 下一个 API Request）

### 9.3 跨菜单无直接连接

**S1-122 关键发现 10**：
- 物资管理 → 就诊流程：当前无直接源码连接（通过 medicalProduct 字段共现，但无赋值链）
- 营销管理 → 患者维护：通过 customerId/customer 字段共现
- 筛查机构 → 就诊流程：通过 visionMesureCtrl 可能有间接联系
- 数据报表 → 全部：通过 Read API 间接连接所有菜单

## 10. 已知排除项

### 10.1 误命名 Controller

| Controller | 行号 | 实际业务 | 归类建议 |
|---|---:|---|---|
| `optometryListCtrl` | L35962 | **UartDevice 设备管理** | 诊所管理 / 设备 |
| `optometryLogListCtrl` | L36135 | **UartDevice 日志** | 诊所管理 / 设备 |
| `visionMesureCtrl` | L48978 | 视力测量（可能关联筛查）| 筛查 / 诊所 |
| `fundusCtrl` / `fundusLogCtrl` | L40335/40467 | 眼底检查 / 日志 | 筛查 / 设备 |

### 10.2 dead-end / 最小 Controller

| Controller | 行号 | 行数 | 备注 |
|---|---:|---:|---|
| `aioIntroduceCtrl` | L3064 | 18 | 介绍页（无 API）|
| `coinRuleIntroduceCtrl` | L3082 | 29 | 介绍页（无 API）|
| `wechatAuthFailedCtrl` | L3626 | 3 | 占位 |
| `wechatAuthSuccessCtrl` | L3629 | 3 | 占位 |
| `appointOrderCtrl` | L3664 | 5 | 占位 |
| `backup1Ctrl` | L3632 | 32 | 备份页 |
| `optometryLogListCtrl` | L36135 | - | 日志 dead-end |

### 10.3 误归类需修正

- `optometryListCtrl` 当前归"就诊流程"但**实际是设备管理**
- `optometryLogListCtrl` 当前归"就诊流程"但**实际是日志**
- `wechatAuthCtrl` / `wechatAuthFailedCtrl` / `wechatAuthSuccessCtrl` 当前归"报表"但**应归"诊所管理"**
- `getGlassNotifyListCtrl` (L13680) 当前归"就诊流程"但**实际是通知页**
- `visionMesureCtrl` 当前归"诊所管理"但**应归"筛查"**
- `fundusCtrl` / `fundusLogCtrl` 当前归"报表"但**应归"筛查"**
- `inspectionCtrl` / `markOriginSetCtrl` 当前归"报表"但**应归"筛查"**

## 11. 26 项矩阵

| # | 项目 | 数量 | Controller 数 | A-F | L1/L2/L3 |
|---:|---|---:|---:|---|---|
| 01 | 一级菜单全集 | 8 | - | A (历史菜单) | L2 |
| 02 | 二级菜单证据 | 0 (未在源码中证明) | - | F | L3 |
| 03 | Controller 全集 | **417** | 417 | A | L1 |
| 04 | Controller 范围 | 59214 行 | 417 | A | L1 |
| 05 | Controller→菜单归类 | 347 / 70 (未归) | 417 | C (基于命名) | L1 |
| 06 | API 规模 | 1638 call site | - | A | L1 |
| 07 | Read 统计 | 1067 (65%) | - | A | L1 |
| 08 | Write 统计 | 466 (28%) | - | A | L1 |
| 09 | call site 平均 | 3.93 / Controller | - | A | L1 |
| 10 | Core object 命中 | 12 类 | - | A | L1 |
| 11 | medicalRecord | 60 处 | 9 | A | L1 |
| 12 | medicalRecordId | 161 处 | 10+ | A | L1 |
| 13 | cashflowId | 74 处 / 20 Controller | 10+ | A | L1 |
| 14 | patient/customer | 89+ 处 / 30+ Controller | 30+ | A | L1 |
| 15 | medicalProduct | 50+ 处 | 10+ | A | L1 |
| 16 | objectId | **1 Controller 唯一** | 1 | A | L1 |
| 17 | UartDevice | 6 Controller | 6 | A | L1 |
| 18 | State 出口 | 700+ 处 | 200+ Controller | A | L1 |
| 19 | StateParams | 100+ 处 | 30+ Controller | A | L1 |
| 20 | Tier A/B/C | 71 / 243 / 103 | 417 | A (Tier A) / C (B/C) | L1 |
| 21 | 主业务候选 | 71 个 Tier A | - | A | L1 |
| 22 | UartDevice 排除 | optometryListCtrl 等 | 2 | A | L1 |
| 23 | 日志排除 | logListCtrl 等 | 5+ | A | L1 |
| 24 | 四大主链 | 4 链 | 30+ | A | L1 |
| 25 | 跨菜单直接关系 | 6 已知 + 0 State 链 | - | A | L2 |
| 26 | A/B/C/D/E/F | A=24 / B=0 / C=1 / D=0 / E=0 / F=1 | - | - | - |

## 12. F 边界

以下信息**当前静态审计无法确认**：

| 项目 | F 原因 | 应对 |
|---|---|---|
| 8 大主菜单的二级菜单 | 路由注册表不在审计范围 | 需要 router config 审计 |
| Controller 实际注册路由 | UI-Router state 注册表 | 需要 HTML 审计 |
| 部分 Controller 实际业务 | 仅基于命名归类 | 需要 controller.js 字段深挖 |
| HTML 绑定 | 不在 controller.js 范围 | 需要 HTML 审计 |
| 实际访问菜单与 Controller 关系 | 用户行为不在审计范围 | 需要运行追踪 |

## 13. 红线

- API actual = 0
- Write actual = 0
- Production mutation = 0
- Historical MD = 0
- controller.js unchanged ✓ (SHA256 F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433)
- deliveryList.html unchanged ✓ (SHA256 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476)
- 165-183 unchanged ✓
- 10 untracked preserved ✓
- 视光之家url.txt preserved (gitignored) ✓
- ignored = 1 ✓
- P0 = 54 冻结 ✓
- P1 = 8 冻结 ✓

## 14. Final Controller Boundary Map

```
【OptFlow PMS Controller Boundary】

8 大主菜单（基于命名归类）
├── 1. 就诊流程 (42)
│   ├── Check 链: optometryCtrl, optometryGlassesCtrl, assistCheckingCtrl
│   ├── Charge 链: waitChargeDetailCtrl, waitPayDetailCtrl, payedDetailCtrl, partBackCtrl
│   ├── Delivery 链: deliveryInputCtrl, deliveryInputRecordCtrl, deliveryListCtrl
│   ├── Check-in 链: addCheckinCtrl, checkinListCtrl
│   └── Prescription: drugPrescriptionCtrl, prescriptsRecordCtrl
│
├── 2. 预约叫号 (16)
│   ├── Appoint: appointOrderCtrl, bookDetailCtrl, bookManageCtrl
│   ├── Queue: queueMachineCtrl, bigScreenCtrl, screenQueueCtrl
│   ├── Call: adminCallCtrl, checkCallCtrl
│   └── Doctor: doctorWorkbenchCtrl
│
├── 3. 患者维护 (35)
│   ├── Member: memberCtrl, memberCardCtrl, memberPointCtrl
│   ├── Patient: patientListCtrl, updatePatientCtrl
│   ├── Account: myAccountCtrl, myMemberCtrl
│   └── Point/TimeCard: pointsListCtrl, timeCardCtrl
│
├── 4. 营销管理 (42)
│   ├── Coupon: addCouponCtrl, couponListCtrl
│   ├── Groupon: addGrouponCtrl, grouponListCtrl
│   ├── FollowUp: followUpCtrl, followUpAnalysisCtrl
│   ├── Seckill: addSecKillProductCtrl, secKillProductListCtrl
│   ├── Recommend: addRecommendCtrl, recommendCustomerCtrl
│   └── Order: selectOrderListCtrl, productOrderCtrl
│
├── 5. 筛查机构 (37)
│   ├── School: schoolListCtrl, addSchoolCtrl, schoolPlanListCtrl
│   ├── Screen: screenListCtrl, screenInStoreCtrl
│   ├── MateCheck: schoolMateCheckListCtrl, modifyMateCheckCtrl
│   └── Vision: visionMesureCtrl, fundusCtrl
│
├── 6. 物资管理 (60)
│   ├── Stock: stockListCtrl, stockChangeCtrl, stockLossListCtrl
│   ├── Material: materiallistCtrl, materialImportCtrl, materialPurchaseCtrl
│   ├── Purchase: purchaseCtrl, purchaseRequestCheckCtrl
│   ├── Supplier: supplierListCtrl, supplierModifyCtrl
│   └── Delivery: addDeliveryCtrl, deliveryModifyCtrl
│
├── 7. 数据报表 (57)
│   ├── Report: reportCtrl, reportFeeCtrl, reportSaleCtrl
│   ├── Sale: saleListCtrl, saleRecordCtrl, addSaleRecordCtrl
│   ├── Fee: feeCashierCtrl, feeDayCtrl, feeMonthCtrl
│   ├── Profit: profitReportCtrl, singleHospitalProfitCtrl
│   └── Statistic: dataChartCtrl, analysisCtrl
│
├── 8. 诊所管理 (58)
│   ├── Admin/Role: adminListCtrl, roleAdminCtrl
│   ├── Hospital: hospitalListCtrl, departmentListCtrl
│   ├── Home: homeCtrl, loginCtrl
│   └── Config: appConfigCtrl, systemSettingCtrl, cloudPrinterListCtrl
│
└── 未归类 (70)
    ├── 营销（应归）: rfmModelCtrl, conversionFunnelCtrl, followListCtrl, newsListCtrl, addVisitCtrl, visitDetailsCtrl, suiFang*Ctrl
    ├── 筛查（应归）: InspectListCtrl, addInspectCtrl, modifyInspectCtrl, zhiShiBangConfigCtrl, visionAdminCtrl
    ├── 物资（应归）: machineOrderCtrl/BrokenCtrl/WaitProcessCtrl, machineOrderListCtrl, addProductPlanCtrl, addGroupeditCtrl, modifyGroupeditCtrl, groupeditListCtrl, productPlanListCtrl
    ├── 收费（应归就诊）: chargeListCtrl, chargeWaysCtrl, customerChargeCtrl, addCustomerChargeCtrl 等 7 个
    ├── 设备/日志（应归 Tier C）: optometryListCtrl, optometryLogListCtrl, logListCtrl, detectionLogCtrl, blueToothTransferCtrl
    └── 占位/介绍: aioIntroduceCtrl, coinRuleIntroduceCtrl, backup1Ctrl, wechatAuthCtrl, wechatAuthFailedCtrl, wechatAuthSuccessCtrl, commonModalInstanceCtrl
```

**S1-122 关键结论**：
- 417 个 Controller 分布到 8 大主菜单
- 8 大主菜单归类覆盖 83%（347/417）
- 17%（70）需要进一步归类修正
- 4 大主链（Check/Sale/Charge/Delivery）就核心 Controller 数 ~ 30+
- Tier A 主业务候选 71 个 Controller
- 误命名 Controller 已识别（optometryListCtrl = 设备）
- 跨菜单主要通过 API 桥接（无 State 链）

---

**【S1-122 完成】**
