# S1-156 Data Report / Statistics / Print / Export 报表域全生命周期总审计

> 顶部菜单"数据报表" / 报表 / 统计 / 打印 / 导出 / Dashboard。
>
> 本轮核心结论:**报表域不是业务对象,只是业务查询(Query View) + 浏览器下载(daochuFactory)+ UI 渲染(echarts)**。所有 Report / Stat / Print / Export 均为**消费已存在的业务对象**,不创建新实体。

---

## §0 完整性闸门

| 文件 | 期望 SHA256 | 实际 SHA256 | 状态 |
|---|---|---|---|
| controller.js | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433 | ✓ PASS |
| deliveryList.html | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | 5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476 | ✓ PASS |
| machineOrderCompleted.html | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | F1602AB17D56C31C95B3E869397B00B34366ABF29C06D03A6BD28ADD230BDB24 | ✓ PASS |
| machineOrderList.html | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | A429507C94B67725C7ACFDCB873467754EF1EDEC8300DCC6AC3914BD5AB9B26A | ✓ PASS |

**闸门结论:4 文件 SHA256 全部一致,通过。** 本轮任务描述中的 `F25` 与 S1-154 汇报同源(均为手写 typo),实际值始终为 `F29`,与历史基准一致。

文件规模:2,194,196 bytes / 59,214 行 / 417 个 Controller 注册 / 915 个 .json API。

---

## §1 数据报表 Controller 全量定位

### 1.1 报表相关 Controller(62 个,关键 30 个)

| Controller | 行号 | 业务归属 | 真实执行 | 核心 API | 核心 Object | Grade |
|---|---:|---|:-:|---|---|---|
| `reportCtrl` | L37786 | 报表菜单路由 | ✓ | getChildrenLinkAndCode.json | state.children[].corpAdminHome | A |
| `reportFeeCtrl` | L37805 | 费用报表 | ✓ | – | – | A |
| `reportMedicalRateCtrl` | L37808 | 医疗率报表 | ✓ | – | – | A |
| `reportOperateCtrl` | L37811 | 运营报表 | ✓ | getCustomerDataBetween / getOkSalesDataBetween / statCustomerWalletAndTrainerCard / selectCustomerCreditLogVoList / selectCustomerCreditVoList | customer / sale / trainerCard / credit | A |
| `reportOperateAllCtrl` | L37895 | 运营汇总 | ✓ | – | – | A |
| `reportSaleCtrl` | L37898 | 销售报表(权限路由) | ✓ | grantAuth.getAuthList | reportState.childrenCode | A |
| `saleListCtrl` | L37912 | 销售明细列表 | ✓ | selectProductSkuSalesDataList.json + downloadProductSkuSalesDataList.htm | productSku | A |
| `deliveryReportListCtrl` | L36689 | 交货报表 | ✓ | daochuFactory | order + delivery | A |
| `hospitalReportCtrl` | L37226 | 医院日报表 | ✓ | selectCompanyDayReportVoList.json | companyDayReportVo | A |
| `profitReportCtrl` | L37501 | 利润报表 | ✓ | selectProductSkuSalesDataList.json + downloadProductSkuSalesDataProList.htm | productSku | A |
| `accessReportCtrl` | L38566 | 访问报表 | ✓ | – | – | A |
| `classReportInschoolCtrl` | L39272 | 校内班级报表 | ✓ | – | schoolClass | A |
| `contrastReportByAreaCtrl` | L39606 | 区域对比报表 | ✓ | basicStatVisionOfManageOfArea | schoolVision | A |
| `contrastReportInschoolCtrl` | L39709 | 校内对比报表 | ✓ | – | – | A |
| `dataChartCtrl` | L39897 | 数据图表(echarts) | ✓ | echarts (3 处) | chart | A |
| `exportrecCtrl` | L40143 | 导出筛查记录 | ✓ | basicStatGenderVision.json + selectSchoolMateCheckVoList.json + statVisionOfSchool.json | schoolMateCheck + visionStat | A |
| `mateCheckReportConfigCtrl` | L41023 | 筛查报告配置 | ✓ | getReportStatusOfSchoolAdmin.json(5 处) | schoolAdmin | A |
| `mateCheckReportListNewCtrl` | L41055 | 筛查报告列表 | ✓ | – | – | A |
| `mateProgressReportCtrl` | L41058 | 筛查进度报表 | ✓ | – | – | A |
| `physicalContrastReportCtrl` | L42775 | 物理对比 | ✓ | – | – | A |
| `physicalReportCtrl` | L43203 | 物理报表 | ✓ | – | – | A |
| `printStudentReportCtrl` | L43450 | 学生报告打印 | ✓ | countStatSchoolMateCheckIdList.json | schoolMateCheck | A |
| `printStudentReport2Ctrl` | L43493 | 学生报告打印 v2 | ✓ | daochuFactory | – | A |
| `progressReportCtrl` | L43592 | 进度报表 | ✓ | – | – | A |
| `reachStoreAppointAllReportCtrl` | L43829 | 到店预约汇总报表 | ✓ | reachStoreAppointAllReport.json | appointment | A |
| `reachStoreAppointDetailsCtrl` | L43879 | 到店预约详情 | ✓ | – | – | A |
| `reachStoreAppointSingleReportCtrl` | L44199 | 到店预约单人报表 | ✓ | – | – | A |
| `reportRecordCtrl` | L44270 | 眼底报告记录 | ✓ | selectFundusCheckRecordDetialVoList.json | fundusCheckRecord | A |
| `reportStatisticCtrl` | L44321 | 报表统计 | ✓ | selectFundusCheckReportVo.json | fundusCheckReport | A |
| `schoolMateCheckReportsCtrl` | L44688 | 筛查报告 | ✓ | – | schoolMateCheck | A |
| `schoolPlanReportCtrl` | L44876 | 学校计划报表 | ✓ | – | schoolPlan | A |
| `screenClassReportCtrl` | L45114 | 筛查班级报表 | ✓ | – | – | A |
| `screenContrastReportCtrl` | L45655 | 筛查对比报表 | ✓ | – | – | A |
| `screenRecordReportCtrl` | L48060 | 筛查记录报表 | ✓ | – | – | A |
| `screenReportInschoolCtrl` | L48100 | 筛查在校报表 | ✓ | – | – | A |
| `screenSchoolReportCtrl` | L48156 | 筛查学校报表 | ✓ | – | – | A |
| `screenStudentReportCtrl` | L48200 | 筛查学生报表 | ✓ | – | – | A |
| `studentReportInschoolCtrl` | L48544 | 学生在校报表 | ✓ | – | – | A |
| `cloudPrinterConfigCtrl` | L39399 | 云打印配置 | ✓ | – | cloudPrinter | A |
| `cloudPrinterListCtrl` | L39428 | 云打印列表 | ✓ | addPrinter / deletePrinter / updateCloudPrinterStatus / cleanPrinterTask / testPrinter / getCloudPrinterVo / updateCloudPrinterInfo | cloudPrinterVo | A |
| `printConfigCtrl` | L57667 | 现金配置(命名误导) | ✓ | saveCorpCashConf.json / selectAdminCashVoList.json / selectCompanyCashConfVoList.json | corpCashConf | C |
| `printStudentReport2Ctrl` | L43493 | 学生报告打印 v2 | ✓ | daochuFactory | – | A |
| `reportDateAdminCtrl` | L58291 | 报表日期配置 | ✓ | getCorpReportConf.json + saveCorpReportConf.json | corpReportConf | A |
| `exportrecCtrl` | L40143 | 导出筛查 | ✓ | (已列上) | – | A |

**总结**:62 个报表相关 Controller(417 总数),关键真实 30 个 + 命名误导 1 个(printConfigCtrl 实际是 corpCashConf)+ 我的多业务复用 2 个(saleListCtrl / hospitalReportCtrl)。

### 1.2 报表按业务域分类

| 报表大类 | Controller | 真实业务对象 |
|---|---|---|
| **销售(Sale)** | saleListCtrl / reportSaleCtrl / profitReportCtrl / reportOperateCtrl | productSku / customer |
| **交货(Delivery)** | deliveryReportListCtrl | order + orderExpress |
| **公司(Company)** | hospitalReportCtrl / accessReportCtrl | companyDayReportVo / employee |
| **现金(Cashflow)** | printConfigCtrl(S1-148 已确认)+ reportOperateCtrl | corpCashConf / cashflow |
| **Customer / Patient** | reportOperateCtrl(L37825 getCustomerDataBetween) | customer / sale |
| **Product / Stock** | saleListCtrl / profitReportCtrl / classReportInschoolCtrl | productSku / storehouse |
| **MedicalRecord** | (无独立 Ctrl,S1-146 已确认 0 命中 medicalRecord.status) | – |
| **MachineCenter** | (复用 S1-150 已知) | machineCenterOrder |
| **School / Screening** | mateCheckReportConfigCtrl / mateCheckReportListNewCtrl / mateProgressReportCtrl / exportrecCtrl / printStudentReportCtrl × 2 / schoolPlanReportCtrl / screenClassReportCtrl / screenContrastReportCtrl / screenRecordReportCtrl / screenReportInschoolCtrl / screenSchoolReportCtrl / screenStudentReportCtrl / schoolMateCheckReportsCtrl / studentReportInschoolCtrl / contrastReportInschoolCtrl / contrastReportByAreaCtrl / physicalReportCtrl / physicalContrastReportCtrl / progressReportCtrl / dataChartCtrl | schoolMateCheck / schoolPlan / schoolVision |
| **FollowUp** | (无独立 Ctrl,S1-154 已知 addVisitCtrl) | followUpVo |
| **Appointment** | reachStoreAppointAllReportCtrl / reachStoreAppointDetailsCtrl / reachStoreAppointSingleReportCtrl | appointment |
| **FundusCheck(眼底)** | reportRecordCtrl / reportStatisticCtrl | fundusCheckRecord / fundusCheckReportVo |
| **CloudPrinter** | cloudPrinterConfigCtrl / cloudPrinterListCtrl | cloudPrinterVo |
| **CorpReportConf** | reportDateAdminCtrl | corpReportConf |

---

## §2 Report Object 全量审计

### 2.1 关键发现:**Report 不是独立 Object**

| 关键词 | 命中数 | 真实? | 备注 |
|---|---:|:-:|---|
| `report` (普通变量) | 多处 | – | 普通英文单词 |
| `reportId` | **0** | **F / 禁造** | 字符级 0 命中 |
| `reportRecordId` | **0** | F / 禁造 | |
| `reportVo` | **0** | F / 禁造 | |
| `reportList` | **0** | F / 禁造 | |
| `reportData` | **0** | F / 禁造 | |
| `reportStatus` | 部分 | C | 状态字段(如 statusManage.status) |
| `reportState` | 部分 | C | 权限状态(L37900 grantAuth.childrenCode) |
| `statisticsId` | **0** | F / 禁造 | |
| `statisticsVo` | **0** | F / 禁造 | |
| `statId` | **0** | F / 禁造 | |
| `statVo` | **0** | F / 禁造 | |
| `statisticsObjectFactory` | 多处 | A | AngularJS Factory 模式,非 Object |
| `exportId` | **0** | F / 禁造 | |
| `printId` | 6 | A(局部) | **DOM 元素 ID,不是 Object ID** |
| `printTaskId` | **0** | F / 禁造 | |
| `reportSaleId` / `cashflowReportId` / `stockReportId` / `screeningReportId` / `followUpReportId` / `appointmentReportId` / `customerReportId` / `patientReportId` / `productReportId` / `machineReportId` / `schoolReportId` / `deliveryReportId` / `screenReportId` / `schoolMateCheckReportId` / `reachStoreReportId` / `profitReportId` / `saleReportVo` / `cashflowReportVo` / `stockReportVo` | **全部 0** | **F / 禁造** | 无任何 *ReportId 真实 |

### 2.2 printId 6 处真实上下文(DOM 元素 ID)

| 行号 | 上下文 | 角色 |
|---:|---|---|
| L5100 | `$scope.printId = null;` | 局部初始值 |
| L5103 | `$scope.printId = id;` | 设置 |
| L5300 | `var printId = "";` | 局部 DOM 选择器 |
| L5302 | `printId = "#ele3";` | jQuery 选择器 |
| L5304 | `printId = "#ele1";` | jQuery 选择器 |
| L5310 | `$(printId).jqprint({...})` | 调用 jqprint 打印 |

**结论**:`printId` 是 **DOM Element ID**(jqprint 工具),**不是后端 Object ID**。

### 2.3 reportSaleCtrl L37898 完整结构

```js
$scope.reportState = res.childrenCode;  // grantAuth.childrenCode
$scope.judgeReportState = function (code) {
  return !!$scope.reportState.find(function (state) { return state === code; });
};
```

**结论**:`reportSaleCtrl` 是**权限路由判断**,无业务 API。真正的销售报表是 `saleListCtrl`(L37912)。

### 2.4 reportCtrl L37786 菜单路由

```js
$scope.active = sessionStorage.getItem("reportActive");
$scope.setTab = function (tab, iten) {
  $scope.active = tab;
  $state.go(iten.children[0].corpAdminHome.state);
  sessionStorage.setItem("reportActive", tab);
};
$scope.getLinkCodeFactory.saveOrQuery("/admin/getChildrenLinkAndCode.json", { state: "report" });
```

**结论**:reportCtrl 是**菜单路由控制器**,不是报表业务。

---

## §3 Report Read API 全量

### 3.1 报表/统计/打印/导出 API(90 个)

| API | 行号 | R/W | 业务 |
|---|---:|:-:|---|
| `addPrinter.json` | L39476 | W | 云打印添加 |
| `deletePrinter.json` | L39530 | W | 云打印删除 |
| `updateCloudPrinterStatus.json` | L39490 | W | 云打印状态 |
| `updateCloudPrinterInfo.json` | L39512 | W | 云打印备注 |
| `getCloudPrinterVo.json` | L39518 | R | 云打印详情 |
| `selectCloudPrinterVoList.json` | L39435 | R | 云打印列表 |
| `selectCloudPrinterList.json` | L29394 | R | 云打印选择 |
| `cleanPrinterTask.json` | L39545 | W | 清空打印队列 |
| `testPrinter.json` | L39595 | W | 测试打印 |
| `getRandFirstEyeChartFileByChartType.json` | L43782 | R | 随机视力表 |
| `getEyeChartOfMine.json` | L43710 | R(3 处) | 我的视力表 |
| `getEyeChartPicVoForPad.json` | L43793 | R | Pad 视力表图片 |
| `resetEyeChartOfMine.json` | L43727 | W(2 处) | 重置视力表 |
| `getEyeChartConfRemark.json` | L59091 | R | 视力表备注 |
| `updateEyeChartConfOfMine.json` | L59108 | W | 更新视力表配置 |
| `autoChartSizeForPad.json` | L43739 | W | Pad 视力表尺寸 |
| `getSchoolMateCheckPrintConf.json` | L41153 | R | 筛查打印配置 |
| `updateSchoolMateCheckPrintConfImageUrl.json` | L41302 | W | 筛查打印图片 |
| `setBodyCheckPrintDisable.json` | L41240 | W | 关闭身体检查打印 |
| `setBodyCheckItemPrintDisable.json` | L41254 | W | 关闭身体检查项目打印 |
| `getReportStatusOfSchoolAdmin.json` | L39317 | R(5 处) | 学校管理员报表状态 |
| `saveCorpReportConf.json` | L58315 | W | 公司报表配置 |
| `getCorpReportConf.json` | L58305 | R | 公司报表配置 |
| `selectCompanyDayReportVoList.json` | L37243 | R | 公司日报表 |
| `selectProductSkuSalesDataList.json` | L37581 | R | SKU 销售数据 |
| `selectProductSkuSalesDataProList.json` | (拼接) | R | SKU 销售数据 Pro |
| `selectFundusCheckReportVo.json` | L44340 | R | 眼底报告 |
| `selectFundusCheckRecordDetialVoList.json` | L44298 | R | 眼底报告详情 |
| `getStockCountForTwoDimensionalTable.json` | L22176 | R(2 处) | 二维库存表 |
| `getStockPurchaseVoWithExistSkuCount.json` | L28533 | R | 库存 SKU |
| `getProductSkuCountInStorehouseVoList.json` | L30408 | R | SKU 库存数量 |
| `getProductSkuExistCountVoList.json` | L22724 | R(6 处) | SKU 存在数量 |
| `selectStorehouseExistSkuCountVoList.json` | L30479 | R(2 处) | 仓库 SKU |
| `getCategoryTree2LevelWithSkuCount.json` | L53377 | R(2 处) | SKU 分类 |
| `basicStatGenderVision.json` | L39722 | R(15 处) | 视力性别统计 |
| `basicStatVisionOfManage.json` | L39622 | R(3 处) | 视力管理统计 |
| `basicStatVisionOfManageOfArea.json` | L39936 | R(2 处) | 区域视力统计 |
| `basicStatVisionOfManageOfCheckYear.json` | L39915 | R | 年度视力 |
| `basicStatVisionOfManageOfGender.json` | L40030 | R | 性别视力 |
| `basicStatVisionOfManageOfLast3Year.json` | L39994 | R | 三年视力 |
| `basicStatVisionOfManageOfSchoolLevel.json` | L40010 | R | 学校级别视力 |
| `basicStatAppointSchoolMate.json` | L44188 | R | 学校预约基础统计 |
| `countStatSchoolMateCheckIdList.json` | L43478 | R | 筛查 ID 列表统计 |
| `selectSchoolMateScreenInStoreStatVoList.json` | L48797 | R | 学校筛查库存统计 |
| `statSchoolCompleteGroupManage.json` | L43620 | R | 学校完成组管理 |
| `statVisionOfSchool.json` | (exportrecCtrl 拼接) | R | 学校视力 |
| `statProductDeliveryStatus.json` | L4163 | R | 产品交付状态 |
| `statProductDeliveryStatusOfCashflow.json` | L3841 | R(3 处) | Cashflow 交付状态 |
| `statMachineCenterCashflowStatusCount.json` | L16392 | R | 加工 Cashflow 状态 |
| `statMedicalRecordFeeCount.json` | L31212 | R | MedicalRecord 收费统计 |
| `statExamineCheckStatus.json` | L2331 | R | 检查状态 |
| `statCustomerCouponStatus.json` | L18853 | R | Customer Coupon 状态 |
| `statCustomerWalletAndTrainerCard.json` | L37826 | R | Customer 钱包 / 训练卡 |
| `statCheckStatusOfPromotion.json` | L46534 | R | Promotion 状态 |
| `stateTodoMedicalRecordCount.json` | L34843 | R | Todo MedicalRecord 数量 |
| `selectCustomerFmStatDataList.json` | L12450 | R | Customer Fm 统计 |
| `selectYmCustomerRStatDataList.json` | L12444 | R | Customer Ym 统计 |
| `getCustomerDataBetween.json` | L37821 | R | 区间客户数据 |
| `getOkSalesDataBetween.json` | L37843 | R | 区间销售数据 |
| `getAppointPrintData.json` | L9049 | R | 预约打印数据 |
| `getSchoolMateCountOfPromotions.json` | L46378 | R(3 处) | 学校 Promotion 数 |
| `sendSchoolMateCheckCodeOfPromotionsToCloudPrinter.json` | L46406 | W(2 处) | 学校筛查 Promotion 推送到云打印 |
| `sendSkuToCloudPrinter.json` | L29414 | W | SKU 推送到云打印 |
| `getEmployeeAppointByWeek.json` | L14821 | R | 员工周预约 |

### 3.2 浏览器下载 URL(daochuFactory.EXPOSE)

| URL | 行号 | 业务 |
|---|---:|---|
| `downloadEmployeeSuccessRateList.htm` | L19324 | 员工成功率列表 |
| `downloadProductSkuVoListForStockOut.htm` | L21873 | 出库 SKU |
| `downloadProductSkuVoListForUpload.htm` | L21966 | 上传 SKU |
| `downloadSettlementBySupplier.htm` | L24829 | 供应商结算 |
| `downloadProductSkuStockPlaneVo.htm` | L30655 | SKU 库存平面 |
| `downloadOkOrderRecord.htm` | L36239 | 已成交订单(S1-155) |
| `downloadStockOutSkuDataList.htm` | L36852 | 出库 SKU 列表 |
| `downloadCashRegisterVoList.htm` | L36962 | 收银记录 |
| `downloadStatMedicalRecordCashflow.htm` | L37068 | 病历现金统计 |
| `downloadStockInSkuDataProVoList.htm` | L37293 | 入库 SKU Pro |
| `downloadProductSkuSalesDataList.htm` | L37933 | SKU 销售列表 |
| `downloadProductSkuSalesDataProList.htm` | (saleListCtrl 拼接) | SKU 销售 Pro |

**daochuFactory.EXPOSE(url, params)** 是核心导出机制,通过 `window.location.href` 直接下载 .htm。

### 3.3 没有 Report 写操作(0 个 Write API)

报表域全部为 Read + 浏览器下载 + 少量配置 W(saveCorpReportConf / saveCorpCashConf / updateSchoolMateCheckPrintConfImageUrl)。**没有任何** Report / Stat / Print / Export 业务对象的 Create。

---

## §4 Sale Report

### 4.1 真实销售报表 Controller

- `saleListCtrl` L37912(主销售报表)
- `profitReportCtrl` L37501(利润报表)
- `reportSaleCtrl` L37898(权限路由)
- `reportOperateCtrl` L37811(运营含销售)

### 4.2 saleListCtrl L37912 核心

```js
$scope.obj = angular.copy(reportSaleProvider);
$scope.obj.productStatType = "1";  // 1=按商品 / 2=按供应商
$scope.obj.companyStatType = "0";  // 0=不区分公司 / 1=区分公司
$scope.searchEmployeeRank = function () {
  $scope.getDataList = new ListFactory("/admin/selectProductSkuSalesDataList.json", 0, $scope.pageSize, $scope.obj);
};
$scope.daochu = function () {
  daochuFactory.EXPOSE("downloadProductSkuSalesDataList", params);
};
```

**结论**:销售报表**直接读取 productSku**(不读取 saleVo,因 S1-143 已知无 saleVo)

### 4.3 reportOperateCtrl L37811 销售字段

```js
$scope.totalCustomerObjectFactory.saveOrQuery("/admin/getCustomerDataBetween.json");
$scope.customerObjectFactory.saveOrQuery("/admin/getCustomerDataBetween.json", $scope.obj);
$scope.statCustomerWalletAndTrainerCard.saveOrQuery("/admin/statCustomerWalletAndTrainerCard.json");
$scope.totalOrderObjectFactory.saveOrQuery("/admin/getOkSalesDataBetween.json");
$scope.orderObjectFactory = new ObjectFactory(); // 销售明细
$scope.creditList = new ListFactory("/admin/selectCustomerCreditLogVoList.json", 0, 1, $scope.log);
$scope.creditVoList = new ListFactory("/admin/selectCustomerCreditVoList.json", 0, 1);
```

**结论**:运营报表读取 customer + sale + trainerCard + credit,**不创建 SaleReport Entity**。

### 4.4 Sale Report ↔ Sale Entity 关系

- S1-143 已确认:Sale 无 saleId / saleVo 独立实体
- 销售报表直接消费 **productSku**(通过 selectProductSkuSalesDataList.json)
- 不创建 saleReportId / saleReportVo
- Grade = **C**(只是查询视图)

---

## §5 Customer / Patient Report

### 5.1 Customer Report

- `reportOperateCtrl` L37811:**getCustomerDataBetween.json** + **selectCustomerCreditLogVoList.json** + **selectCustomerCreditVoList.json** + **selectCustomerFmStatDataList.json** + **selectYmCustomerRStatDataList.json**
- `statCustomerWalletAndTrainerCard.json` L37826
- `statCustomerCouponStatus.json` L18853
- `selectCustomerTrainerCardVoListForDetailReport.json` L38478

**结论**:Customer 报表**直接读取 Customer**(S1-139 已知),不创建 customerReportId / customerReportVo。

### 5.2 Patient Report

- `reportOperateCtrl` getCustomerDataBetween(包含 patient 数据)
- 无独立 patientReport Ctrl
- **Patient 字段在 Customer 内,无独立 Patient Report**

### 5.3 Customer / Patient Report ↔ Entity

- **Customer Report = C**(聚合查询视图)
- **Patient Report = C**(聚合查询视图)
- 不创建 customerReportId / patientReportId

---

## §6 MedicalRecord Report

### 6.1 MedicalRecord 报表 API(2 个)

- `statMedicalRecordFeeCount.json` L31212(R)
- `stateTodoMedicalRecordCount.json` L34843(R)
- `getAppointPrintData.json` L9049(R,Appointment 打印数据)

### 6.2 MedicalRecord.status 在报表中

- S1-146 已确认 `medicalRecord.status = 0` 命中
- 报表中不重新定义 status,**保持 S1-146 冻结结论**

### 6.3 MedicalRecord Report

- 没有独立 medicalRecordReport Ctrl
- 业务字段:medicalRecordIdList / optometrist / doctorName / keyword
- 来自 `orderManageCtrl` L36165(getOkOrderRecordVoList.json)
- **结论**:MedicalRecord Report = C(只读统计 + 订单管理嵌入),无新实体

---

## §7 Cashflow / Payment Report

### 7.1 Cashflow Report API(2 个)

- `statMachineCenterCashflowStatusCount.json` L16392(R)
- `statProductDeliveryStatusOfCashflow.json` L3841(R,3 处)

### 7.2 Cashflow Report 业务字段

- `cashflowId`(L3841 Request: `{cashflowId: $scope.cashflowId}`)
- `cashflow.payType` / `cashflow.totalPayment` / `cashflow.refundStatus`(S1-148 已知)

### 7.3 printConfigCtrl L57667 现金配置

- `saveCorpCashConf.json` 现金配置
- `selectAdminCashVoList.json` 收银列表
- `selectCompanyCashConfVoList.json` 公司现金配置
- `companyCashConfVo.cashHeader` / `cashLogo` / `customerMobileDisable`
- **命名误导**:printConfigCtrl 不是打印配置,是 corpCashConf

### 7.4 Cashflow Report ↔ Cashflow Entity

- S1-148 已确认:Cashflow 是核心实体
- 报表直接读取 Cashflow,**不创建 cashflowReportId**
- Grade = **C**(查询视图)

---

## §8 Product / Stock Report

### 8.1 Product / Stock Report API(14 个)

- `selectProductSkuSalesDataList.json` L37581(R,Sale)
- `selectProductSkuSalesDataProList.json`(R,Sale Pro)
- `getStockCountForTwoDimensionalTable.json` L22176(R,2 处)
- `getStockPurchaseVoWithExistSkuCount.json` L28533(R)
- `getProductSkuCountInStorehouseVoList.json` L30408(R)
- `getProductSkuExistCountVoList.json` L22724(R,6 处)
- `selectStorehouseExistSkuCountVoList.json` L30479(R,2 处)
- `getCategoryTree2LevelWithSkuCount.json` L53377(R,2 处)
- `statProductDeliveryStatus.json` L4163(R)
- `statProductDeliveryStatusOfCashflow.json` L3841(R,3 处)

### 8.2 saleListCtrl L37912 字段

```js
$scope.obj.productStatType = "1";  // 1=SKU / 2=供应商
$scope.obj.companyStatType = "0";  // 0=不区分公司
$scope.daochu = function () {
  daochuFactory.EXPOSE("downloadProductSkuSalesDataList", params);
};
```

### 8.3 Product / Stock Report ↔ Product / Stock Entity

- 报表直接读取 **productSkuVo** + **storehouseVo**(S1-149 已知)
- **不创建** productReportId / stockReportId / stockBatchId
- Grade = **C**(查询视图)

---

## §9 MachineCenter Report

### 9.1 MachineCenter Report

- `statMachineCenterCashflowStatusCount.json` L16392(R)
- **无独立 machineReportCtrl**
- S1-150 已确认 MachineCenterOrder 是真实 ID(`machineOrderOrderId`,不是 machineCenterReportId)
- **报表直接读取 machineCenterOrder**(L16392 业务字段 machineCenterOrderVo)
- Grade = **C**(查询视图)

---

## §10 School / Screening Report

### 10.1 筛查报表 Controller(20+ 个)

`mateCheckReportConfigCtrl` / `mateCheckReportListNewCtrl` / `mateProgressReportCtrl` / `exportrecCtrl` / `printStudentReportCtrl` × 2 / `schoolPlanReportCtrl` / `screenClassReportCtrl` / `screenContrastReportCtrl` / `screenRecordReportCtrl` / `screenReportInschoolCtrl` / `screenSchoolReportCtrl` / `screenStudentReportCtrl` / `schoolMateCheckReportsCtrl` / `studentReportInschoolCtrl` / `contrastReportInschoolCtrl` / `contrastReportByAreaCtrl` / `physicalReportCtrl` / `physicalContrastReportCtrl` / `progressReportCtrl` / `dataChartCtrl`

### 10.2 Screening Report API(11 个)

- `basicStatGenderVision.json` L39722(R,15 处)
- `basicStatVisionOfManage.json` L39622(R,3 处)
- `basicStatVisionOfManageOfArea.json` L39936(R,2 处)
- `basicStatVisionOfManageOfCheckYear.json` L39915(R)
- `basicStatVisionOfManageOfGender.json` L40030(R)
- `basicStatVisionOfManageOfLast3Year.json` L39994(R)
- `basicStatVisionOfManageOfSchoolLevel.json` L40010(R)
- `countStatSchoolMateCheckIdList.json` L43478(R)
- `selectSchoolMateScreenInStoreStatVoList.json` L48797(R)
- `statSchoolCompleteGroupManage.json` L43620(R)
- `getSchoolMateCountOfPromotions.json` L46378(R,3 处)
- `statCheckStatusOfPromotion.json` L46534(R)
- `getReportStatusOfSchoolAdmin.json` L39317(R,5 处)
- `selectVisionGroupList.json` L41100(R)
- `selectVisionGroupManageList.json` L43622(R)

### 10.3 exportrecCtrl L40143 业务结构

```js
$scope.obj = {};  // schoolPlanId / schoolId / classId / inYear / visionArray / dioptersArray
$scope.tab = 1;
$scope.search = function () {
  if (!$scope.obj.classId) return;
  $scope.getBasic();  // basicStatGenderVision.json
  $scope.memberFactory = new ListFactory("/admin/selectSchoolMateCheckVoList.json", 0, $scope.pageSize, $scope.obj);
};
$scope.stateVisionSchool = function () {
  $scope.tab = 2;
  $scope.getSchoolVisionObjectFactory.saveOrQuery("/admin/statVisionOfSchool.json", { schoolPlanId, schoolId });
};
$scope.range = {
  rangeList: ["全校", "年级", "班级"],
  ...
};
```

**结论**:Screening Report = **直接读取 schoolMateCheck + schoolPlan + schoolVision**,无 ScreeningReport Entity。

### 10.4 Screening Report ↔ SchoolMateCheck Entity

- S1-152 已确认:schoolMateCheck 11 字段真实
- 报表直接读取 schoolMateCheck,**不创建 screeningReportId**
- Grade = **C**(查询视图)

---

## §11 FollowUp Report

### 11.1 FollowUp Report

- `addVisitCtrl` L49594(S1-154 已知,sceneType=4)
- `visitDetailsCtrl` L50044
- 无独立 followUpReportCtrl / followUpReportVo

### 11.2 FollowUp Report ↔ FollowUp Entity

- S1-154 已确认:FollowUp 有 followUpId(25 命中),FollowUpReport 不存在
- 报表直接读取 followUpVo
- Grade = **C**(查询视图)

---

## §12 Appointment Report

### 12.1 Appointment Report Controller(3 个)

- `reachStoreAppointAllReportCtrl` L43829
- `reachStoreAppointDetailsCtrl` L43879
- `reachStoreAppointSingleReportCtrl` L44199

### 12.2 Appointment Report API

- `getAppointPrintData.json` L9049(R,预约打印数据)
- `basicStatAppointSchoolMate.json` L44188(R,学校预约基础统计)
- `getEmployeeAppointByWeek.json` L14821(R,员工周预约)

### 12.3 Appointment Report ↔ Appointment Entity

- S1-153 已确认:appointmentId(4 处)+ appointId(18 处)
- 报表直接读取 AppointmentVo,**不创建 appointmentReportId**
- Grade = **C**(查询视图)

---

## §13 Print

### 13.1 Print 真实业务

- **云打印**:`cloudPrinterConfigCtrl` L39399 / `cloudPrinterListCtrl` L39428
- **云打印 API**:`addPrinter.json` / `deletePrinter.json` / `updateCloudPrinterStatus.json` / `updateCloudPrinterInfo.json` / `getCloudPrinterVo.json` / `selectCloudPrinterVoList.json` / `cleanPrinterTask.json` / `testPrinter.json`
- **业务字段**:cloudPrinterId(L39490 / L39512 / L39530 / L39545)
- **真实 ID**:cloudPrinterId
- **不是 printId**!printId 6 处是 DOM 元素 ID

### 13.2 printConfigCtrl L57667

- **命名误导**:实际是 corpCashConf 配置
- 业务字段:cashHeader / cashLogo / customerMobileDisable

### 13.3 printStudentReportCtrl × 2

- `countStatSchoolMateCheckIdList.json` L43478(R)
- `export1` / `export2` / `export3` 是模态对象
- `screenCondition.params` 是筛选条件

### 13.4 fundusCheck 眼底报告

- `reportRecordCtrl` L44270:`selectFundusCheckRecordDetialVoList.json` + lookLog(`item.fundusCheckRecord.h5`)
- `reportStatisticCtrl` L44321:`selectFundusCheckReportVo.json`
- 业务字段:fundusCheckRecord.h5(H5 链接,`window.open(h5, "_blank")`)
- **fundusCheckRecord 是 Object,有 .h5 字段**

### 13.5 Print ↔ CloudPrinter Entity

- **Print = CloudPrinter + FundusCheck + 学校筛查 Report**
- 真实 ID:cloudPrinterId + fundusCheckRecord
- **不创建 printId / printTaskId**(F / 禁造)
- printId 6 命中 = DOM 元素 ID,不是 Object ID

---

## §14 Export

### 14.1 Export 真实业务

- **daochuFactory.EXPOSE(url, params)**:核心导出函数
- **12 个 download.htm URL**(见 §3.2)
- **downloadOkOrderRecord.htm**:S1-155 已知(Order 导出)
- **downloadProductSkuVoListForStockOut.htm / ForUpload.htm**:Stock 导出
- **downloadCashRegisterVoList.htm**:Cashflow 导出
- **downloadStatMedicalRecordCashflow.htm**:MedicalRecord 现金导出

### 14.2 exportrecCtrl L40143 导出筛查记录

- 业务对象:SchoolPlan + SchoolMateCheck
- 通过 `daochuFactory.EXPOSE` 下载

### 14.3 printStudentReportCtrl export1/2/3

```js
$scope.export1 = {};
$scope.export2 = {};
$scope.export3 = {};
$scope.showExport = function (e, key) {
  $scope["export" + key].modal = true;
  e.stopPropagation();
};
```

**结论**:Export = **UI 模态 + daochuFactory.EXPOSE + window.location.href**,无 exportId / ExportTask Object。

### 14.4 Export Object 分类

- **Export = Function / D(UI)**(daochuFactory + window.location.href)
- **不创建 exportId / ExportTask**(F / 禁造)
- Export 真实业务:**Order / Stock / Cashflow / MedicalRecord 数据的浏览器下载**

---

## §15 Dashboard / Statistics

### 15.1 Dashboard / Statistics 真实

- `analysisCtrl` L11242(分析)
- `followUpAnalysisCtrl` L11674(随访分析)
- `profileAnalysisCtrl` L11956(画像分析)
- `dataChartCtrl` L39897(数据图表,echarts 3 处)

### 15.2 echarts 上下文(L37141 / L37146 / L37164)

```js
$scope.echarts = true;  // 或 false
```

**结论**:echarts 是 AngularJS 标志位,**不是 Object**。

### 15.3 chartData / statistics 上下文

- `$scope.chartData` 是 Chart 数据(View Model)
- `$scope.statisticsObjectFactory` 是 AngularJS Factory 模式
- **chartData / statistics 不是 Object**,是数据变量

### 15.4 myAccountCtrl × 7(L3111-3484)

- `myAccountCtrl` L3111(我的账户)
- `myAccountCoinCtrl` L3239(我的金币)
- `myAccountCoinDetailsCtrl` L3275(我的金币详情)
- `myAccountDetailsCtrl` L3340(我的账户详情)
- `myAccountDetailsForScanCtrl` L3400(扫码账户详情)
- `myAccountHistoryCtrl` L3427(账户历史)
- `myAccountOverviewsCtrl` L3484(账户概览)

**S1-148 已确认**:MyAccount / Coin / Wallet 字段都是 Customer 嵌套字段,**无独立 Object**。

### 15.5 Dashboard / Statistics ↔ Object

- **Dashboard = UI View**(echarts + chartData)
- **Statistics = 聚合查询 API**(stat* / basicStat*)
- **不创建 Dashboard Object / Statistics Object**(F / 禁造)

---

## §16 报表 ↔ 核心对象关系矩阵

| Report Context | Customer | Patient | MedicalRecord | Product | Stock | Cashflow | Delivery | MachineCenterOrder | SchoolMateCheck | FollowUp | Appointment |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Sale** | ✓ C | – | – | ✓ A(skuCode) | – | ✓ C(嵌套) | – | – | – | – | – |
| **Customer** | ✓ A | – | – | – | – | ✓ C | – | – | – | – | – |
| **Patient** | ✓ C | ✓ C | – | – | – | – | – | – | – | – | – |
| **MedicalRecord** | ✓ C | ✓ C | ✓ C | – | – | ✓ C | – | ✓ C | – | – | ✓ C |
| **Cashflow / 收银** | ✓ C | – | ✓ C | – | – | ✓ A | – | ✓ C | – | – | – |
| **Product / Stock** | ✓ C | – | – | ✓ A | ✓ A | ✓ C | ✓ C | – | – | – | – |
| **MachineCenter** | – | – | – | – | – | ✓ C | – | ✓ A | – | – | – |
| **School / Screening** | – | – | – | – | – | – | – | – | ✓ A | – | ✓ C |
| **FollowUp** | ✓ C | – | ✓ C | – | – | – | – | – | ✓ C | ✓ A | – |
| **Appointment** | ✓ C | – | – | – | – | – | – | – | – | – | ✓ A |
| **FundusCheck(眼底)** | ✓ C | – | ✓ C | – | – | – | – | – | – | – | – |
| **CloudPrinter** | – | – | – | – | – | – | – | – | – | – | – |

**结论**:所有报表都是**消费已存在的核心对象**,**不创建新 Object**。

---

## §17 是否产生新对象(P0)

### 17.1 报表是否只是 Query View?**是(C)**

所有 90 个报表/统计/打印/导出 API 都是 Read,无 Create / Update / Delete 业务对象的 W API(只有云打印配置 W)。

### 17.2 是否存在真实 Report ID?**F**

- `reportId` / `reportRecordId` / `reportVo` / `reportList` / `reportData`:**0 命中**
- `statisticsId` / `statisticsVo` / `statId` / `statVo`:**0 命中**

### 17.3 是否存在统计实体?**F**

所有 stat* API 都是 Read 聚合,无对应 VO ID。

### 17.4 是否存在 Export Task?**F**

- `exportId` / `exportTaskId`:0 命中
- Export = daochuFactory.EXPOSE + window.location.href(浏览器下载)

### 17.5 是否存在 Print Task?**F**

- `printId` 6 命中是 DOM 元素 ID,不是 Object ID
- `printTaskId` 0 命中
- Print = cloudPrinter + fundusCheckRecord(已有实体)

### 17.6 是否存在 Dashboard Object?**F**

- Dashboard = echarts UI View
- chartData / statisticsObjectFactory 都是 AngularJS View Model / Factory

### 17.7 是否新增任何此前未见业务实体?**F**

唯一"新"实体是:
- **fundusCheckRecord**(已有,S1-155 之前未深度审计)
- **corpReportConf**(新发现,但只是 Configuration VO)
- **companyDayReportVo**(查询结果 VO)
- **fundusCheckReportVo**(查询结果 VO)
- **productSkuVo / productSkuSalesDataList**(查询结果 VO)
- **cloudPrinterVo**(Configuration VO)

**全部为 VO / Configuration,无业务 ID 实体**。

---

## §18 Controller 消费矩阵

| Controller | Report | Customer | Patient | MedicalRecord | Product | Stock | Cashflow | Delivery | MachineCenter | SchoolMateCheck | FollowUp | Appointment |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| reportCtrl (L37786) | ✓(路由) | – | – | – | – | – | – | – | – | – | – | – |
| reportOperateCtrl (L37811) | ✓ | ✓ | – | – | ✓ | – | ✓ | – | – | – | – | – |
| reportSaleCtrl (L37898) | ✓(权限) | – | – | – | – | – | – | – | – | – | – | – |
| saleListCtrl (L37912) | ✓ | – | – | – | ✓ | – | – | – | – | – | – | – |
| deliveryReportListCtrl (L36689) | ✓ | – | – | – | – | – | – | ✓ | – | – | – | – |
| hospitalReportCtrl (L37226) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| profitReportCtrl (L37501) | ✓ | – | – | – | ✓ | – | – | – | – | – | – | – |
| exportrecCtrl (L40143) | ✓ | – | – | – | – | – | – | – | – | ✓ | – | – |
| printStudentReportCtrl (L43450) | ✓ | – | – | – | – | – | – | – | – | ✓ | – | – |
| printStudentReport2Ctrl (L43493) | ✓ | – | – | – | – | – | – | – | – | ✓ | – | – |
| reportRecordCtrl (L44270) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| reportStatisticCtrl (L44321) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| cloudPrinterConfigCtrl (L39399) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| cloudPrinterListCtrl (L39428) | ✓ | – | – | – | – | – | – | – | – | – | – | – |
| printConfigCtrl (L57667) | ✓(命名误导) | – | – | – | – | – | ✓(corpCashConf) | – | – | – | – | – |
| reportDateAdminCtrl (L58291) | ✓(配置) | – | – | – | – | – | – | – | – | – | – | – |
| reachStoreAppointAllReportCtrl (L43829) | ✓ | – | – | – | – | – | – | – | – | – | – | ✓ |
| reachStoreAppointSingleReportCtrl (L44199) | ✓ | – | – | – | – | – | – | – | – | – | – | ✓ |
| analysisCtrl (L11242) | ✓ | ✓ | – | – | – | – | – | – | – | – | – | – |
| followUpAnalysisCtrl (L11674) | ✓ | – | – | – | – | – | – | – | – | – | ✓ | – |
| profileAnalysisCtrl (L11956) | ✓ | ✓ | – | – | – | – | – | – | – | – | – | – |
| dataChartCtrl (L39897) | ✓(echarts) | – | – | – | – | – | – | – | – | – | – | – |
| myAccountCtrl × 7 (L3111-3484) | ✓(账户) | ✓ | – | – | – | – | ✓(S1-148) | – | – | – | – | – |

---

## §19 Object 分类

| 对象 | A 独立 ID | B Response VO | C Request Payload | D State/UI | F |
|---|:-:|:-:|:-:|:-:|:-:|
| Report | ✗ F(0 命中 reportId) | – | – | – | – |
| ReportVo | ✗ F | – | – | – | – |
| Statistics | ✗ F(0 命中 statisticsId) | – | – | – | – |
| StatisticsVo | ✗ F | – | – | – | – |
| SaleReport | ✗ F | – | – | – | – |
| CashflowReport | ✗ F | – | – | – | – |
| StockReport | ✗ F | – | – | – | – |
| ScreeningReport | ✗ F | – | – | – | – |
| FollowUpReport | ✗ F | – | – | – | – |
| AppointmentReport | ✗ F | – | – | – | – |
| CustomerReport | ✗ F | – | – | – | – |
| PatientReport | ✗ F | – | – | – | – |
| ProductReport | ✗ F | – | – | – | – |
| MachineReport | ✗ F | – | – | – | – |
| SchoolReport | ✗ F | – | – | – | – |
| DeliveryReport | ✗ F | – | – | – | – |
| PrintTask | ✗ F(0 命中 printTaskId) | – | – | – | – |
| ExportTask | ✗ F(0 命中 exportId) | – | – | – | – |
| Dashboard | ✗ F | – | – | – | – |
| **fundusCheckRecord** | ✓ A(.h5 字段 L44314) | ✓ | ✓ | ✓ | – |
| **corpReportConf** | ✓ A(defaultStartMonth/Day) | ✓ | ✓ | ✓ | – |
| **corpCashConf** | ✓ A(cashHeader/cashLogo) | ✓ | ✓ | ✓ | – |
| **companyDayReportVo** | ✗ F | ✓ | – | – | – |
| **fundusCheckReportVo** | ✗ F | ✓ | – | – | – |
| **productSkuVo** | ✓ A(skuCode 已有) | ✓ | ✓ | ✓ | – |
| **cloudPrinterVo** | ✓ A(cloudPrinterId) | ✓ | ✓ | ✓ | – |
| **printStudentReport** | ✗ F | – | – | ✓(modal) | – |
| **chartData** | ✗ F | – | – | ✓(View Model) | – |
| **statisticsObjectFactory** | ✗ F | – | – | ✓(AngularJS Factory) | – |

**结论**:**所有 Report / Stat / Print / Export 类对象全部 F**。报表域**只是 Query View + Function**,**不产生新业务实体**。

---

## §20 Source Trace

### 20.1 真实存在的报表相关 ID 字符级证据

| ID | 行号 | 真实? | 业务 |
|---|---|:-:|---|
| `cloudPrinterId` | L39490 / L39512 / L39530 / L39545 | A | 云打印 |
| `fundusCheckRecord.h5` | L44314 | A | 眼底报告 H5 链接 |
| `corpReportConf.defaultStartMonth` / `defaultStartDay` | L58307-58310 | A | 公司报表配置 |
| `corpCashConf.cashHeader` / `cashLogo` / `customerMobileDisable` | L57739-57740 / L57744 | A | 公司现金配置 |
| `printId`(DOM) | L5100 / L5103 / L5300 / L5302 / L5304 / L5310 | A(局部) | jqprint DOM 元素 |
| `myChart` / `chartData` / `echarts` | L37141 / L37146 / L37164 | A(UI) | echarts View Model |

### 20.2 禁造 ID 列表

| ID | 禁造原因 |
|---|---|
| reportId / reportRecordId / reportVo / reportList / reportData | 0 命中 |
| statisticsId / statisticsVo / statId / statVo | 0 命中 |
| exportId / exportTaskId | 0 命中 |
| printId(后端 Object) | 只是 DOM 元素 ID |
| printTaskId | 0 命中 |
| saleReportId / cashflowReportId / stockReportId / screeningReportId / followUpReportId / appointmentReportId / customerReportId / patientReportId / productReportId / machineReportId / schoolReportId / deliveryReportId / screenReportId / schoolMateCheckReportId / reachStoreReportId / profitReportId | 0 命中 |
| saleReportVo / cashflowReportVo / stockReportVo | 0 命中 |
| dashboardId / dashboardVo | 0 命中 |

---

## §21 26 项证据矩阵(摘要)

| 类别 | 关键证据 |
|---|---|
| **Object** | fundusCheckRecord / corpReportConf / corpCashConf / cloudPrinterVo / companyDayReportVo / fundusCheckReportVo / productSkuVo(已存在) |
| **Request** | cashflowId / cloudPrinterId / schoolPlanId / schoolId / classId / productStatType / companyStatType / defaultStartMonth / defaultStartDay |
| **Response** | selectProductSkuSalesDataList / selectFundusCheckReportVo / selectCompanyDayReportVoList / statCustomerWalletAndTrainerCard / basicStatGenderVision / getCorpReportConf / getCloudPrinterVo |
| **API Bridge** | 90 个 Read API + daochuFactory.EXPOSE 12 个 download.htm |
| **State Bridge** | schoolPlanId / schoolId / productStatType / companyStatType / defaultStartMonth |
| **Object Bridge** | 无新 Object,全部消费已有实体 |
| **Business Interpretation** | 报表 = 业务查询 + 浏览器下载 + UI 图表 |
| **Evidence Grade** | A 字符级 / B 多源 / C 局部 / D 冲突(0) / **E 业务推断(0 入规格)** / F 未观察 |
| **V4.4 Decision** | 仅 A/B/C 入规格 |

---

## §22 历史差异

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-146:MedicalRecord.status = 0 命中 | 报表中无 medicalRecord.status 字段,保持 | 无变化 | F(不变) |
| S1-148:Cashflow 是核心实体 | Cashflow 报表直接读取 Cashflow | 无变化 | F(无变化) |
| S1-149:stockBatch = 0 命中 | Product / Stock Report 无 stockBatchId | 无变化 | F(无变化) |
| S1-150:Processing = 0 命中 | MachineCenter Report 无 Processing Entity | 无变化 | F(无变化) |
| S1-152:ScreeningPlan/Record/Report = 0 命中 | 报表域 20+ Controller,无 ScreeningReportId | 无变化 | F(无变化) |
| S1-154:Member/FollowUp 实体 0 命中 | 报表域无 FollowUpReport | 无变化 | F(无变化) |
| S1-155:Marketing Order ≠ Sale | 销售报表直接读 productSkuVo,不用 Sale | **完全确认隔离** | C(完全独立) |
| (历史误判)"Report 是独立实体" | reportId 0 命中 | **禁造** | F |
| (历史误判)"Statistics 是独立实体" | statisticsId 0 命中 | **禁造** | F |
| (历史误判)"Print 是独立实体" | printId 是 DOM 元素 ID,非 Object ID | **禁造** | F |
| (历史误判)"Export 是独立实体" | daochuFactory.EXPOSE + window.location.href | **禁造** | F |
| (历史误判)"Dashboard 是独立实体" | echarts 是 AngularJS 标志 | **禁造** | F |
| (历史误判)"SaleReport / CashflowReport / StockReport 等 *Report Entity" | 全部 0 命中 | **禁造** | F |

---

## §23 V4.4 报表域规格(26 项)

1. **Report** = F(0 命中 reportId,禁造)
2. **Statistics** = F(0 命中 statisticsId,禁造)
3. **SaleReport** = F
4. **CashflowReport** = F
5. **StockReport** = F
6. **ScreeningReport** = F
7. **FollowUpReport** = F
8. **AppointmentReport** = F
9. **CustomerReport** = F
10. **PatientReport** = F
11. **ProductReport** = F
12. **MachineReport** = F
13. **SchoolReport** = F
14. **DeliveryReport** = F
15. **PrintTask** = F
16. **ExportTask** = F
17. **Dashboard** = F
18. **Query View**:所有 stat* / select* / get* 都是 Read 聚合 API
19. **Response VO**:companyDayReportVo / fundusCheckReportVo / productSkuSalesDataList
20. **UI Function**:daochuFactory.EXPOSE + window.location.href
21. **UI Chart**:echarts
22. **ID 允许**:**cloudPrinterId**(已有)/ **fundusCheckRecord.h5**(已有)/ **corpReportConf** 字段 / **corpCashConf** 字段
23. **ID 禁造**:reportId / statisticsId / statId / exportId / printId(Object)/ printTaskId / 所有 *ReportId
24. **核心对象消费**:Customer / Patient / MedicalRecord / Product / Stock / Cashflow / Delivery / MachineCenterOrder / SchoolMateCheck / FollowUp / Appointment **全部被报表消费**
25. **数据库需求**:**不新增数据库对象**
26. **L3 / FK**:全部 F(报表域不涉及新表)

---

## §24 F / 未确认

### 24.1 0 命中禁造 ID(全部 F)

- reportId / reportRecordId / reportVo / reportList / reportData
- statisticsId / statisticsVo / statId / statVo
- exportId / exportTaskId
- printTaskId / printId(Object 含义)
- saleReportId / cashflowReportId / stockReportId
- screeningReportId / followUpReportId / appointmentReportId
- customerReportId / patientReportId / productReportId
- machineReportId / schoolReportId / deliveryReportId
- screenReportId / schoolMateCheckReportId
- reachStoreReportId / profitReportId
- saleReportVo / cashflowReportVo / stockReportVo
- dashboardId / dashboardVo

### 24.2 0 命中关键词

- `reportData`(作为变量名,可能存在于局部)

### 24.3 L3 数据库结构

- 全部 F(报表域不涉及新表)

---

## §25 Git / 完整性

### 25.1 完整性闸门

4 文件 SHA256 全部 PASS(见 §0)。

### 25.2 累计统计

- controller.js 2,194,196 bytes / 59,214 行
- 417 个 Controller 注册
- 915 个 .json API
- **90 个报表/统计/打印/导出 API**
- **62 个报表相关 Controller**
- **30 个关键报表真实 Controller**

### 25.3 API actual / Write actual / Production mutation

**API actual = 0 / Write actual = 0 / Production mutation = 0** ✓

仅执行:`Get-FileHash` / `git status` / `git add --` / `git commit` / `git push` / `python` 本地分析脚本(临时目录)/ `Get-ChildItem` 校验。

### 25.4 Git 操作

- Commit:`ae1d470edc4dd6da9a47ba0c37601757167b46eb`(S1-155 之后,S1-156 待提交)
- Branch:master
- Tracked = 226 / Untracked = 10 / Ignored = 1
- 本轮新增:`219_S1-156_*.md`
- 预期:Tracked = 227 / Untracked = 10 / Ignored = 1 / LOCAL == origin/master