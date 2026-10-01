# 04｜模块 memberManage 会员管理

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/memberManage/` |
| 中文名 | 会员管理 |
| 开发波次 | W3 |
| 页面数 | **33** |
| 端点数（去重） | **90** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addMemberTag` | `/addMemberTag` | `views/memberManage/addMemberTag.html` | `addMemberTagCtrl` | 0 |
| 2 | `addPromotion` | `/addPromotion` | `views/memberManage/addPromotion.html` | `addPromotionCtrl` | 0 |
| 3 | `addRecommend` | `/addRecommend` | `views/memberManage/addRecommend.html` | `addRecommendCtrl` | 0 |
| 4 | `addSecKillProduct` | `/addSecKillProduct?promotionId` | `views/memberManage/addSecKillProduct.html` | `addSecKillProductCtrl` | 4 |
| 5 | `branchMember` | `/branchMember` | `views/memberManage/branchMember.html` | `memberCtrl` | 28 |
| 6 | `chargeList` | `/chargeList?customerId` | `views/memberManage/chargeList.html` | `chargeListCtrl` | 0 |
| 7 | `groupSend` | `/groupSend?taskTemplateBatchSendId` | `views/memberManage/groupSend.html` | `groupSendCtrl` | 11 |
| 8 | `groupSendLook` | `/groupSendLook?taskTemplateBatchSendId` | `views/memberManage/groupSendLook.html` | `groupSendLookCtrl` | 1 |
| 9 | `member` | `/member?tagId` | `views/memberManage/member.html` | `memberCtrl` | 28 |
| 10 | `memberCard` | `/memberCard?customerId` | `views/memberManage/memberCard.html` | `memberCardCtrl` | 0 |
| 11 | `memberPoint` | `/memberPoint?customerId` | `views/memberManage/memberPoint.html` | `memberPointCtrl` | 0 |
| 12 | `memberRecyle` | `/memberRecyle?type&companyId` | `views/memberManage/memberRecyle.html` | `memberRecyleCtrl` | 11 |
| 13 | `memberTag` | `/memberTag` | `views/memberManage/memberTag.html` | `memberTagCtrl` | 0 |
| 14 | `modifyPromotion` | `/modifyPromotion?promotionId` | `views/memberManage/modifyPromotion.html` | `modifyPromotionCtrl` | 0 |
| 15 | `modifyRecommend` | `/modifyRecommend?promotionId` | `views/memberManage/modifyRecommend.html` | `modifyRecommendCtrl` | 0 |
| 16 | `modifySecKillProduct` | `/modifySecKillProduct?seckillProductId` | `views/memberManage/modifySecKillProduct.html` | `modifySecKillProductCtrl` | 13 |
| 17 | `myCoupon` | `/myCoupon?customerId` | `views/memberManage/myCoupon.html` | `myCouponCtrl` | 0 |
| 18 | `orderDetail` | `/orderDetail?orderId` | `views/memberManage/orderDetail.html` | `orderDetailCtrl` | 0 |
| 19 | `patientList` | `/patientList?customerId` | `views/memberManage/patientList.html` | `patientListCtrl` | 0 |
| 20 | `productOrder` | `/productOrder?seckillProductId` | `views/memberManage/productOrder.html` | `productOrderCtrl` | 0 |
| 21 | `promotionDetail` | `/promotionDetail?id` | `views/memberManage/promotionDetail.html` | `promotionDetailCtrl` | 0 |
| 22 | `recommendCustomer` | `/recommendCustomer` | `views/memberManage/recommendCustomer.html` | `recommendCustomerCtrl` | 0 |
| 23 | `recommendDetail` | `/recommendDetail` | `views/memberManage/recommendDetail.html` | `recommendDetailCtrl` | 4 |
| 24 | `recommendPhoneList` | `/recommendPhoneList` | `views/memberManage/recommendPhoneList.html` | `recommendPhoneListCtrl` | 12 |
| 25 | `recommendTable` | `/recommendTable` | `views/memberManage/recommendTable.html` | `recommendTableCtrl` | 3 |
| 26 | `requirement` | `/requirement` | `views/memberManage/requirement.html` | `requirementCtrl` | 3 |
| 27 | `requirementStatus` | `/requirementStatus?id` | `views/memberManage/requirementStatus.html` | `requirementStatusCtrl` | 2 |
| 28 | `secKillProductDetail` | `/secKillProductDetail?seckillProductId` | `views/memberManage/secKillProductDetail.html` | `secKillProductDetailCtrl` | 12 |
| 29 | `secKillProductList` | `/secKillProductList?promotionId` | `views/memberManage/secKillProductList.html` | `secKillProductListCtrl` | 0 |
| 30 | `secKillPromotionList` | `/secKillPromotionList` | `views/memberManage/secKillPromotionList.html` | `secKillPromotionListCtrl` | 0 |
| 31 | `selectOrderList` | `/selectOrderList?keyword` | `views/memberManage/selectOrderList.html` | `selectOrderListCtrl` | 0 |
| 32 | `sendPlatform` | `/sendPlatform` | `views/memberManage/sendPlatform.html` | `sendPlatformCtrl` | 2 |
| 33 | `updateMember` | `/updateMember?customerId` | `views/memberManage/updateMember.html` | `updateMemberCtrl` | 7 |

## §2 端点清单（去重 90 个）

- `POST /admin/activeSeckillProduct.json`
- `POST /admin/assignRecommendPhoneList.json`
- `POST /admin/cancelSmsRequirement.json`
- `POST /admin/cancelTemplateBatchSendTask.json`
- `POST /admin/changeCustomerMember.json`
- `POST /admin/commitCustomerPointLog.json`
- `POST /admin/commitRefundOrderLog.json`
- `POST /admin/createBatchFileTask.json`
- `POST /admin/createCustomerBatchFileTask.json`
- `POST /admin/createRefundOrderLog.json`
- `POST /admin/createSeckillProduct.json`
- `POST /admin/createTemplateBatchSendTask.json`
- `POST /admin/deleteSmsRequirement.json`
- `POST /admin/deleteTag.json`
- `POST /admin/deliveryOrder.json`
- `POST /admin/disBandingWechatByCustomerId.json`
- `POST /admin/disableCustomers.json`
- `POST /admin/enableCustomers.json`
- `POST /admin/getBandingWechatQrcode.json`
- `POST /admin/getCompanyListOfMine.json`
- `POST /admin/getCorpPointRule.json`
- `POST /admin/getCustomerCard.json`
- `POST /admin/getCustomerCashflowDataPage.json`
- `POST /admin/getCustomerCouponVo.json`
- `POST /admin/getCustomerMember.json`
- `POST /admin/getCustomerMemberDataList.json`
- `POST /admin/getCustomerMemberDataListOfCompany.json`
- `POST /admin/getCustomerPoint.json`
- `POST /admin/getCustomerVo.json`
- `POST /admin/getDefaultSchoolPlanByAdminId.json`
- `POST /admin/getFundusCheckRecordListOfCustomer.json`
- `POST /admin/getHospitalInfo.json`
- `POST /admin/getMemberList.json`
- `POST /admin/getOrderBrandList.json`
- `POST /admin/getOrderCategoryList.json`
- `POST /admin/getOrderVo.json`
- `POST /admin/getPatientMemberDataList.json`
- `POST /admin/getPatientVoList.json`
- `POST /admin/getPromotionQrcode.json`
- `POST /admin/getPromotionVo.json`
- `POST /admin/getRecommendPhoneVo.json`
- `POST /admin/getRequirementOrderVo.json`
- `POST /admin/getSchoolClassList.json`
- `POST /admin/getSchoolMateCheckVoOfCustomer.json`
- `POST /admin/getSchoolMateCheckVoOfRecommendPhone.json`
- `POST /admin/getSeckillProductVo.json`
- `POST /admin/getSmsRequirement.json`
- `POST /admin/getTag.json`
- `POST /admin/getTaskTemplateBatchSendVo.json`
- `POST /admin/giveFirstReward.json`
- `POST /admin/giveSecondReward.json`
- `POST /admin/initAddCustomerPoint.json`
- `POST /admin/initSubCustomerPoint.json`
- `POST /admin/insertCustomerTags.json`
- `POST /admin/insertTag.json`
- `POST /admin/invalidSeckillProduct.json`
- `POST /admin/isBandingWechat.json`
- `POST /admin/linkRecommendPhone.json`
- `POST /admin/pickUpOrder.json`
- `POST /admin/saveCustomerInfo.json`
- `POST /admin/selectCorpSmsByCorpId.json`
- `POST /admin/selectCorpVoiceByCorpId.json`
- `POST /admin/selectCouponVoList.json`
- `POST /admin/selectCustomerCouponVoList.json`
- `POST /admin/selectCustomerPointLogVoList.json`
- `POST /admin/selectEmployeeVoListOfMyCompany.json`
- `POST /admin/selectInYearListBySchoolPlan.json`
- `POST /admin/selectLatestRecord.json`
- `POST /admin/selectOrderVoListByCorpId.json`
- `POST /admin/selectOrderVoListByCustomerId.json`
- `POST /admin/selectOrderVoListOfSeckillProduct.json`
- `POST /admin/selectPromotionVoList.json`
- `POST /admin/selectRecommendPhoneVoList.json`
- `POST /admin/selectSchoolIntentionVoList.json`
- `POST /admin/selectSeckillProductVoList.json`
- `POST /admin/selectSmsRequirementList.json`
- `POST /admin/selectTagByName.json`
- `POST /admin/selectTagList.json`
- `POST /admin/selectTaskTemplateBatchSendList.json`
- `POST /admin/selectTaskTemplateBatchSendLogVoList.json`
- `POST /admin/selectWecomTagList.json`
- `POST /admin/sendCoupon.json`
- `POST /admin/statCustomerCouponStatus.json`
- `POST /admin/updateCustomerTags.json`
- `POST /admin/updateExtCardNo.json`
- `POST /admin/updatePromotion.json`
- `POST /admin/updateSeckillProduct.json`
- `POST /admin/updateTagName.json`
- `POST /admin/useCoupon.json`
- `POST /auth/isAdminTokenOk.json`

## §3 逐页字段规格

### 4.1 `addMemberTag`

- **URL**：`/addMemberTag`
- **模板**：`views/memberManage/addMemberTag.html`
- **控制器**：`addMemberTagCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`net`

### 4.2 `addPromotion`

- **URL**：`/addPromotion`
- **模板**：`views/memberManage/addPromotion.html`
- **控制器**：`addPromotionCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： * 图片 点击上传 |

**表单标签**

| 标签 |
|---|
| * 活动名称： * 图片 点击上传 |
| 地址： |
| 备注： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `obj.address` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.thumb` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseImg()` |
| `create()` |

**跳转到**：`secKillPromotionList`

### 4.3 `addRecommend`

- **URL**：`/addRecommend`
- **模板**：`views/memberManage/addRecommend.html`
- **控制器**：`addRecommendCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： * 图片 点击上传 |

**表单标签**

| 标签 |
|---|
| * 活动名称： * 图片 点击上传 |
| 备注： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.thumb` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseImg()` |
| `create()` |

**跳转到**：`recommendCustomer`

### 4.4 `addSecKillProduct`

- **URL**：`/addSecKillProduct?promotionId`
- **模板**：`views/memberManage/addSecKillProduct.html`
- **控制器**：`addSecKillProductCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `activeSeckillProduct` | `POST /admin/activeSeckillProduct.json` |
| `createSeckillProduct` | `POST /admin/createSeckillProduct.json` |
| `getCustomerCashflowDataPage` | `POST /admin/getCustomerCashflowDataPage.json` |
| `selectLatestRecord` | `POST /admin/selectLatestRecord.json` |

**必填项**

| 标签 |
|---|
| * 商品名称： |
| * 图片： |
| * 规格： |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |

**表单标签**

| 标签 |
|---|
| * 商品名称： |
| * 图片： |
| 点击上传 |
| 描述： |
| * 规格： |
| 无规格 |
| 一种规格 |
| 两种规格 |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |
| 允许退货： |
| 不允许 |
| 允许 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.modelPicture` |
| `obj.description` |
| `obj.modelType` |
| `obj.model1Name` |
| `obj.model1` |
| `obj.model2Name` |
| `obj.model2` |
| `marketPrice` |
| `seckillPrice` |
| `obj.totalCount` |
| `obj.startTime` |
| `startTime` |
| `obj.endTime` |
| `endTime` |
| `obj.permissionToReturn` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item` |
| `modelName.id` |
| `modelName.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideModal()` |
| `chooseImg()` |
| `deleteImg($index)` |
| `setFirst(item,$index)` |
| `changeType(obj.modelType)` |
| `open1()` |
| `open2()` |
| `addSecKill()` |
| `active()` |

### 4.5 `branchMember`

- **URL**：`/branchMember`
- **模板**：`views/memberManage/branchMember.html`
- **控制器**：`memberCtrl`
- **端点数**：28

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeCustomerMember` | `POST /admin/changeCustomerMember.json` |
| `commitCustomerPointLog` | `POST /admin/commitCustomerPointLog.json` |
| `createBatchFileTask` | `POST /admin/createBatchFileTask.json` |
| `createCustomerBatchFileTask` | `POST /admin/createCustomerBatchFileTask.json` |
| `disableCustomers` | `POST /admin/disableCustomers.json` |
| `enableCustomers` | `POST /admin/enableCustomers.json` |
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `getCorpPointRule` | `POST /admin/getCorpPointRule.json` |
| `getCustomerCard` | `POST /admin/getCustomerCard.json` |
| `getCustomerMember` | `POST /admin/getCustomerMember.json` |
| `getCustomerMemberDataList` | `POST /admin/getCustomerMemberDataList.json` |
| `getCustomerMemberDataListOfCompany` | `POST /admin/getCustomerMemberDataListOfCompany.json` |
| `getCustomerPoint` | `POST /admin/getCustomerPoint.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getOrderBrandList` | `POST /admin/getOrderBrandList.json` |
| `getOrderCategoryList` | `POST /admin/getOrderCategoryList.json` |
| `getTag` | `POST /admin/getTag.json` |
| `initAddCustomerPoint` | `POST /admin/initAddCustomerPoint.json` |
| `initSubCustomerPoint` | `POST /admin/initSubCustomerPoint.json` |
| `insertCustomerTags` | `POST /admin/insertCustomerTags.json` |
| `insertTag` | `POST /admin/insertTag.json` |
| `selectCustomerCouponVoList` | `POST /admin/selectCustomerCouponVoList.json` |
| `selectCustomerPointLogVoList` | `POST /admin/selectCustomerPointLogVoList.json` |
| `selectTagByName` | `POST /admin/selectTagByName.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `selectWecomTagList` | `POST /admin/selectWecomTagList.json` |
| `updateExtCardNo` | `POST /admin/updateExtCardNo.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 基本信息 |
| 2 | 城市 |
| 3 | 会员卡 |
| 4 | 消费频次 只计产品消费频次 ,不计检查消费,包含退费次数 |
| 5 | 消费金额 只计产品费用,不计检查费用,含退费 |
| 6 | 实付金额 |
| 7 | 最近一次消费 |
| 8 | 会员标签 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.memberId` |
| `obj.startTime` |
| `rightTimer` |
| `dateSearch` |
| `obj.checkinStartTime` |
| `obj.checkinEndTime` |
| `dateSearch2` |
| `orderPayment` |
| `orderCount` |
| `orderCount2` |
| `obj.hasMobile` |
| `obj.hasWechat` |
| `categoryIdArray[$index]` |
| `brandIdArray[$index]` |
| `newTagIdArray[$index]` |
| `tagIdArray[$index]` |
| `tagName` |
| `memberClass.allStatus` |
| `item.isChose` |
| `change.memberId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `basic.schoolName` |
| `Referrer.name` |
| `Referrer.tip` |
| `Transactor.name` |
| `Transactor.tip` |
| `Maintainer.name` |
| `Maintainer.tip` |
| `item.id` |
| `item.memberName` |
| `item.categoryName` |
| `item.brandName` |
| `item.tagName` |
| `memberFactory.allData.customerPaymentData.totalOrderPrice` |
| `memberFactory.allData.customerPaymentData.totalOrderPayment` |
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.wechatCustomer.city` |
| `item.customer.platformCode` |
| `item.customerRmfData.orderCount` |
| `item.customerRmfData.orderPrice` |
| `item.customerRmfData.orderPayment` |
| `iten.tagName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePatient()` |
| `openSchoolPop()` |
| `clearBasicSchool()` |
| `Referrer.show = true` |
| `Referrer.close($event)` |
| `Transactor.show = true` |
| `Transactor.close($event)` |
| `Maintainer.show = true` |
| `Maintainer.close($event)` |
| `open1()` |
| `open2()` |
| `searchDate(3)` |
| `searchDate(1)` |
| `searchDate(2)` |
| `open3()` |
| `open4()` |
| `searchDate(3,` |
| `searchDate(1,` |
| `searchDate(2,` |
| `search()` |
| `searchAllCateId()` |
| `searchAllBrandId()` |
| `searchAllTagId()` |
| `tagModal=true` |
| `addLabel=true` |
| `insertTag()` |
| `hideTagModal($event)` |
| `deleteAll()` |
| `toRecovery(true)` |
| `recyleAll()` |
| `toRecovery(false)` |
| `memberClass.choseAll()` |
| `memberClass.choseSingle()` |
| `showDetails(item)` |
| `updateMenber(item.customer.id,$event)` |
| `showMemberInfo(item.customer.id)` |
| `recharge(item.customer.id)` |
| `recyleAll(item.customer.id)` |
| `saveMemberType()` |

**跳转到**：`memberTag`

**下拉数据源（ng-options）**

```
x.id as x.memberName for x in getMemberListFactory.items
```

### 4.6 `chargeList`

- **URL**：`/chargeList?customerId`
- **模板**：`views/memberManage/chargeList.html`
- **控制器**：`chargeListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 基本信息 |
| 2 | 联系人 |
| 3 | 收费信息 |
| 4 | 费用合计 |
| 5 | 已收费用 |
| 6 | 已退费用 |
| 7 | 支付状态 |
| 8 | 付款方式 |
| 9 | {{corpInfo. companyTitle}} |
| 10 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `item.basicInfo` |
| `item.customerName` |
| `item.customerMobile` |
| `item.payInfo` |
| `item.totalPayment` |
| `item.receivedPayment` |
| `item.refundPayment` |
| `pay` |
| `item.companyName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `bindLook(item)` |

### 4.7 `groupSend`

- **URL**：`/groupSend?taskTemplateBatchSendId`
- **模板**：`views/memberManage/groupSend.html`
- **控制器**：`groupSendCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createTemplateBatchSendTask` | `POST /admin/createTemplateBatchSendTask.json` |
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getOrderBrandList` | `POST /admin/getOrderBrandList.json` |
| `getOrderCategoryList` | `POST /admin/getOrderCategoryList.json` |
| `getPatientMemberDataList` | `POST /admin/getPatientMemberDataList.json` |
| `getTaskTemplateBatchSendVo` | `POST /admin/getTaskTemplateBatchSendVo.json` |
| `selectCorpSmsByCorpId` | `POST /admin/selectCorpSmsByCorpId.json` |
| `selectCorpVoiceByCorpId` | `POST /admin/selectCorpVoiceByCorpId.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 类型 |
| 2 | 使用场景 |
| 3 | 内容 |
| 4 | 操作 |
| 5 | 姓名 |
| 6 | 生日 |
| 7 | 手机号 |
| 8 | 消费频次 |
| 9 | 消费金额 |
| 10 | 最近一次消费 |
| 11 | 已购品类 |
| 12 | 已购品牌 |
| 13 | 会员标签 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.birthdayStartTime` |
| `obj.birthdayEndTime` |
| `obj.startTime` |
| `obj.rightTimer` |
| `dateSearch` |
| `obj.checkinStartTime` |
| `obj.rightTimer2` |
| `dateSearch2` |
| `orderPayment` |
| `orderCount` |
| `obj.memberId` |
| `item.time` |
| `obj.taskName` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `isFilterPage` |
| `memberFactory.count` |
| `item.id` |
| `item.memberName` |
| `item.name` |
| `item.count` |
| `item.unit` |
| `choseTable.smsInfo.smsTemplate.marketType` |
| `marketType` |
| `choseTable.smsInfo.smsTemplate.title` |
| `choseTable.smsInfo.smsTemplate.example` |
| `choseTable.voiceInfo.voiceTemplate.marketType` |
| `choseTable.voiceInfo.voiceTemplate.title` |
| `choseTable.voiceInfo.voiceTemplate.example` |
| `item.patient.patientName` |
| `item.patient.patientBirthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.customer.linkMobile` |
| `item.patientRmfData.orderCount` |
| `item.patientRmfData.orderPrice` |
| `item.patientRmfData.categoryNames` |
| `item.patientRmfData.brandNames` |
| `iten.tagName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `open5()` |
| `open6()` |
| `searchDate(3)` |
| `searchDate(1)` |
| `searchDate(2)` |
| `open3()` |
| `open4()` |
| `searchDate2(3)` |
| `searchDate2(1)` |
| `searchDate2(2)` |
| `custom(` |
| `search()` |
| `choseMessage($index,$event)` |
| `choseTable.openPopout(` |
| `yulan()` |
| `sendTimeInfo.click(item.status)` |
| `sendTimeInfo.groupList[0].addOne()` |
| `sendTimeInfo.groupList[0].subOne($index)` |
| `sendTask()` |
| `hideCouponModal()` |

**跳转到**：`sendPlatform`

### 4.8 `groupSendLook`

- **URL**：`/groupSendLook?taskTemplateBatchSendId`
- **模板**：`views/memberManage/groupSendLook.html`
- **控制器**：`groupSendLookCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectTaskTemplateBatchSendLogVoList` | `POST /admin/selectTaskTemplateBatchSendLogVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 类型 |
| 3 | 内容 |
| 4 | 开始发送时间 |
| 5 | 发送时间 |
| 6 | 类型 |
| 7 | 会员 |
| 8 | 手机号 |
| 9 | 内容 |
| 10 | 发送状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `paramsObj.taskTemplateBatchSend.taskName` |
| `paramsObj.smsTemplate.example` |
| `paramsObj.voiceTemplate.example` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.model` |
| `item.patient.patientName` |
| `item.customer.linkMobile` |
| `item.content` |

### 4.9 `member`

- **URL**：`/member?tagId`
- **模板**：`views/memberManage/member.html`
- **控制器**：`memberCtrl`
- **端点数**：28

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeCustomerMember` | `POST /admin/changeCustomerMember.json` |
| `commitCustomerPointLog` | `POST /admin/commitCustomerPointLog.json` |
| `createBatchFileTask` | `POST /admin/createBatchFileTask.json` |
| `createCustomerBatchFileTask` | `POST /admin/createCustomerBatchFileTask.json` |
| `disableCustomers` | `POST /admin/disableCustomers.json` |
| `enableCustomers` | `POST /admin/enableCustomers.json` |
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `getCorpPointRule` | `POST /admin/getCorpPointRule.json` |
| `getCustomerCard` | `POST /admin/getCustomerCard.json` |
| `getCustomerMember` | `POST /admin/getCustomerMember.json` |
| `getCustomerMemberDataList` | `POST /admin/getCustomerMemberDataList.json` |
| `getCustomerMemberDataListOfCompany` | `POST /admin/getCustomerMemberDataListOfCompany.json` |
| `getCustomerPoint` | `POST /admin/getCustomerPoint.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getOrderBrandList` | `POST /admin/getOrderBrandList.json` |
| `getOrderCategoryList` | `POST /admin/getOrderCategoryList.json` |
| `getTag` | `POST /admin/getTag.json` |
| `initAddCustomerPoint` | `POST /admin/initAddCustomerPoint.json` |
| `initSubCustomerPoint` | `POST /admin/initSubCustomerPoint.json` |
| `insertCustomerTags` | `POST /admin/insertCustomerTags.json` |
| `insertTag` | `POST /admin/insertTag.json` |
| `selectCustomerCouponVoList` | `POST /admin/selectCustomerCouponVoList.json` |
| `selectCustomerPointLogVoList` | `POST /admin/selectCustomerPointLogVoList.json` |
| `selectTagByName` | `POST /admin/selectTagByName.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `selectWecomTagList` | `POST /admin/selectWecomTagList.json` |
| `updateExtCardNo` | `POST /admin/updateExtCardNo.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**表单标签**

| 标签 |
|---|
| 公众号 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 基本信息 |
| 2 | 城市 |
| 3 | 会员卡 |
| 4 | 消费频次 只计产品消费频次 ,不计检查消费,包含退费次数 |
| 5 | 消费金额 只计产品费用,不计检查费用,含退费 |
| 6 | 实付金额 |
| 7 | 最近一次消费 |
| 8 | 家庭成员 |
| 9 | 会员标签 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.memberId` |
| `obj.startTime` |
| `rightTimer` |
| `dateSearch` |
| `obj.checkinStartTime` |
| `obj.checkinEndTime` |
| `dateSearch2` |
| `orderPayment` |
| `orderCount` |
| `orderCount2` |
| `obj.hasMobile` |
| `obj.hasWechat` |
| `categoryIdArray[$index]` |
| `brandIdArray[$index]` |
| `obj.channel` |
| `newTagIdArray[$index]` |
| `tagIdArray[$index]` |
| `tagName` |
| `memberClass.allStatus` |
| `item.isChose` |
| `change.memberId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `getTagDetailFactory.result.object.tagName` |
| `basic.schoolName` |
| `Referrer.name` |
| `Referrer.tip` |
| `Transactor.name` |
| `Transactor.tip` |
| `Maintainer.name` |
| `Maintainer.tip` |
| `item.id` |
| `item.memberName` |
| `item.categoryName` |
| `item.brandName` |
| `item.tagName` |
| `memberFactory.allData.customerPaymentData.totalOrderPrice` |
| `memberFactory.allData.customerPaymentData.totalOrderPayment` |
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.wechatCustomer.city` |
| `item.customer.platformCode` |
| `item.customerRmfData.orderCount` |
| `item.customerRmfData.orderPrice` |
| `item.customerRmfData.orderPayment` |
| `iten.tagName` |
| `data.filepath` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hidePatient()` |
| `showMemberStore($event)` |
| `showWechatModal($event)` |
| `clearTagId()` |
| `openSchoolPop()` |
| `clearBasicSchool()` |
| `Referrer.show = true` |
| `Referrer.close($event)` |
| `Transactor.show = true` |
| `Transactor.close($event)` |
| `Maintainer.show = true` |
| `Maintainer.close($event)` |
| `open1()` |
| `open2()` |
| `searchDate(3,` |
| `searchDate(1,` |
| `searchDate(2,` |
| `open3()` |
| `open4()` |
| `search()` |
| `searchAllCateId()` |
| `searchAllBrandId()` |
| `searchAllTagId()` |
| `tagModal=true` |
| `addLabel=true` |
| `insertTag()` |
| `hideTagModal($event)` |
| `deleteAll()` |
| `showDaochu($event,false)` |
| `toRecovery(true)` |
| `recyleAll()` |
| `toRecovery(false)` |
| `memberClass.choseAll()` |
| `memberClass.choseSingle()` |
| `showDetails(item)` |
| `updateMenber(item.customer.id,$event)` |
| `showMemberInfo(item.customer.id)` |
| `recharge(item.customer.id)` |
| `recyleAll(item.customer.id)` |
| `saveMemberType()` |
| `saveWeChat()` |
| `createTask()` |
| `importModal=false` |

**跳转到**：`memberTag`

**下拉数据源（ng-options）**

```
x.id as x.memberName for x in getMemberListFactory.items
```

### 4.10 `memberCard`

- **URL**：`/memberCard?customerId`
- **模板**：`views/memberManage/memberCard.html`
- **控制器**：`memberCardCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 关联实卡： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.bandingExt` |
| `obj.extCardNo` |
| `change.memberId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `membername` |
| `getCardFactory.result.object.cardNo` |
| `getCardFactory.result.object.extCardNo` |
| `getPointFactory.result.object.point` |
| `havenotFactory.count` |

**页面动作（ng-click）**

| 动作 |
|---|
| `bindCard()` |

**下拉数据源（ng-options）**

```
x.id as x.memberName for x in getMemberListFactory.items
```

### 4.11 `memberPoint`

- **URL**：`/memberPoint?customerId`
- **模板**：`views/memberManage/memberPoint.html`
- **控制器**：`memberPointCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 增加 减少 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 变动类型 |
| 2 | 时间 |
| 3 | 积分变动 |
| 4 | 积分余额 |
| 5 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `pointType` |
| `point` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPointFactory.result.object.point` |
| `getPointFactory.result.object.historyPoint` |
| `item.customerPointLog.channelType` |
| `pointChannel` |
| `item.customerPointLog.gmtUpdate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customerPointLog.addPoint` |
| `item.customerPointLog.pointBalance` |
| `item.customerPointLog.remark` |
| `getInitPointFactory.result.object.payPoint` |
| `getInitPointFactory.result.object.toMoney` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showModel()` |
| `hideCancelModal()` |
| `commitPoint()` |

### 4.12 `memberRecyle`

- **URL**：`/memberRecyle?type&companyId`
- **模板**：`views/memberManage/memberRecyle.html`
- **控制器**：`memberRecyleCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteTag` | `POST /admin/deleteTag.json` |
| `enableCustomers` | `POST /admin/enableCustomers.json` |
| `getCustomerMemberDataList` | `POST /admin/getCustomerMemberDataList.json` |
| `getCustomerMemberDataListOfCompany` | `POST /admin/getCustomerMemberDataListOfCompany.json` |
| `getPromotionQrcode` | `POST /admin/getPromotionQrcode.json` |
| `getPromotionVo` | `POST /admin/getPromotionVo.json` |
| `insertTag` | `POST /admin/insertTag.json` |
| `selectTagByName` | `POST /admin/selectTagByName.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `updatePromotion` | `POST /admin/updatePromotion.json` |
| `updateTagName` | `POST /admin/updateTagName.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 基本信息 |
| 2 | 城市 |
| 3 | 会员卡 |
| 4 | 消费频次 只计产品消费频次 ,不计检查消费,包含退费次数 |
| 5 | 消费金额 只计产品费用,不计检查费用,含退费 |
| 6 | 折后金额 |
| 7 | 最近一次消费 |
| 8 | 家庭成员 |
| 9 | 会员标签 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `memberClass.allStatus` |
| `item.isChose` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.customer.avatar` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.wechatCustomer.city` |
| `item.customer.platformCode` |
| `item.customerRmfData.orderCount` |
| `item.customerRmfData.orderPrice` |
| `item.customerRmfData.orderPayment` |
| `iten.tagName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setRecyle()` |
| `recyleAll()` |
| `memberClass.choseAll()` |
| `memberClass.choseSingle()` |
| `recyleAll(item.customer.id)` |

### 4.13 `memberTag`

- **URL**：`/memberTag`
- **模板**：`views/memberManage/memberTag.html`
- **控制器**：`memberTagCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 标签名称 |
| 2 | 会员数量 |
| 3 | 创建时间 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.keyword` |
| `modify.tagName` |
| `obj.tagName` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.tagName` |
| `item.useCount` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showAddMember()` |
| `searchUsecountList(1)` |
| `searchUsecountList(2)` |
| `searchDateList(1)` |
| `searchDateList(2)` |
| `showModify(item.tagName,item.id)` |
| `$event.stopPropagation()` |
| `modifyTag(item.id,$event,$index)` |
| `cancel($event)` |
| `deleteContent=true` |
| `deleteTag(item.id)` |
| `$event.stopPropagation();deleteContent=false` |
| `addMemberTag()` |
| `hideAddMember()` |

### 4.14 `modifyPromotion`

- **URL**：`/modifyPromotion?promotionId`
- **模板**：`views/memberManage/modifyPromotion.html`
- **控制器**：`modifyPromotionCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： * 海报： 点击上传 |
| * 提货方式： 到店自提 |

**表单标签**

| 标签 |
|---|
| * 活动名称： * 海报： 点击上传 |
| * 提货方式： 到店自提 |
| 快递发货 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `obj.expressType` |
| `obj.address` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.promotionURL` |
| `getPromotionFactory.result.object.promotion.promotionUrlQrcode` |
| `qrcodeImg` |
| `getPromotionFactory.result.object.promotion.promotionUrl` |
| `obj.thumb` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideCode()` |
| `showCode(getPromotionFactory.result.object.promotion.promotionUrl,$event)` |
| `chooseImg()` |
| `modify()` |

**跳转到**：`secKillProductAdmin`, `secKillPromotionList`

### 4.15 `modifyRecommend`

- **URL**：`/modifyRecommend?promotionId`
- **模板**：`views/memberManage/modifyRecommend.html`
- **控制器**：`modifyRecommendCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 活动名称： |
| * 海报： |

**表单标签**

| 标签 |
|---|
| * 活动名称： |
| * 海报： |
| 点击上传 |
| 活动说明： |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.title` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.thumb` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseImg()` |
| `modify()` |

**跳转到**：`recommendCustomer`

### 4.16 `modifySecKillProduct`

- **URL**：`/modifySecKillProduct?seckillProductId`
- **模板**：`views/memberManage/modifySecKillProduct.html`
- **控制器**：`modifySecKillProductCtrl`
- **端点数**：13

**调用的端点**

| 动作 | 端点 |
|---|---|
| `activeSeckillProduct` | `POST /admin/activeSeckillProduct.json` |
| `getCustomerCouponVo` | `POST /admin/getCustomerCouponVo.json` |
| `getOrderVo` | `POST /admin/getOrderVo.json` |
| `getPatientVoList` | `POST /admin/getPatientVoList.json` |
| `getSeckillProductVo` | `POST /admin/getSeckillProductVo.json` |
| `selectCouponVoList` | `POST /admin/selectCouponVoList.json` |
| `selectCustomerCouponVoList` | `POST /admin/selectCustomerCouponVoList.json` |
| `selectOrderVoListOfSeckillProduct` | `POST /admin/selectOrderVoListOfSeckillProduct.json` |
| `selectPromotionVoList` | `POST /admin/selectPromotionVoList.json` |
| `sendCoupon` | `POST /admin/sendCoupon.json` |
| `statCustomerCouponStatus` | `POST /admin/statCustomerCouponStatus.json` |
| `updateSeckillProduct` | `POST /admin/updateSeckillProduct.json` |
| `useCoupon` | `POST /admin/useCoupon.json` |

**必填项**

| 标签 |
|---|
| * 商品名称： |
| * 图片 |
| * 图片： |
| * 规格： |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |

**表单标签**

| 标签 |
|---|
| * 商品名称： |
| * 图片 |
| 点击上传 |
| * 图片： |
| 描述： |
| * 规格： |
| 无规格 |
| 一种规格 |
| 两种规格 |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |
| 允许退货： |
| 不允许 |
| 允许 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.modelPicture` |
| `obj.description` |
| `obj.modelType` |
| `obj.model1Name` |
| `obj.model1` |
| `obj.model2Name` |
| `obj.model2` |
| `marketPrice` |
| `seckillPrice` |
| `obj.totalCount` |
| `obj.startTime` |
| `momentDate` |
| `startTime` |
| `obj.endTime` |
| `endTime` |
| `obj.permissionToReturn` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.modelPicture` |
| `item` |
| `modelName.id` |
| `modelName.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `colorModal= false;` |
| `hideModal()` |
| `chooseImg()` |
| `deleteImg($index)` |
| `setFirst(item,$index)` |
| `changeType(obj.modelType)` |
| `open1()` |
| `open2()` |
| `goBack()` |
| `addSecKill()` |
| `active()` |

### 4.17 `myCoupon`

- **URL**：`/myCoupon?customerId`
- **模板**：`views/memberManage/myCoupon.html`
- **控制器**：`myCouponCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 优惠券名称 |
| 2 | 优惠券码 |
| 3 | 类型/面额 |
| 4 | 领取时间 |
| 5 | 使用场景 |
| 6 | 状态 |
| 7 | 操作 |
| 8 | 优惠券名称 |
| 9 | 种类/面额 |
| 10 | 有效期 |
| 11 | 限制条件 |
| 12 | 使用说明 |
| 13 | 剩余库存 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.status` |
| `obj.keyword` |
| `keyword` |
| `couponIdList[$index]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCount.object.status0` |
| `getCount.object.status1` |
| `selectFactory.count` |
| `item.coupon.couponName` |
| `item.customerCoupon.couponCode` |
| `item.coupon.couponType` |
| `couponType` |
| `item.coupon.couponValue` |
| `item.coupon.couponRate` |
| `item.customerCoupon.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.coupon.useScene` |
| `useScene` |
| `item.coupon.useOverMoney` |
| `item.coupon.useOverCount` |
| `item.customerCoupon.status` |
| `couponStatus` |
| `item.coupon.id` |
| `item.coupon.useTimeStart` |
| `item.coupon.useTimeStartDays` |
| `item.coupon.useTimeEnd` |
| `item.coupon.useTimeEndDays` |
| `item.coupon.useContent` |
| `item.coupon.couponTotalCount` |
| `item.coupon.couponSendCount` |
| `getCouponVoFactory.object.coupon.couponType` |
| `getCouponVoFactory.object.coupon.couponValue` |
| `getCouponVoFactory.object.coupon.couponRate` |
| `getCouponVoFactory.object.customerCoupon.useTimeTo` |
| `getCouponVoFactory.object.coupon.useOverMoney` |
| `getCouponVoFactory.object.coupon.useOverCount` |
| `getCouponVoFactory.object.coupon.useScene` |
| `getCouponVoFactory.object.coupon.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSendModal()` |
| `showCouponModify(item.customerCoupon.id,$event)` |
| `modify()` |
| `hideCouponModal()` |
| `modifycoupon()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 4.18 `orderDetail`

- **URL**：`/orderDetail?orderId`
- **模板**：`views/memberManage/orderDetail.html`
- **控制器**：`orderDetailCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getOrderDetailFactory.result.object.cashflow.totalPayment` |
| `getOrderDetailFactory.result.object.customerOrder.priceExpress` |
| `getOrderDetailFactory.result.object.customerOrder.priceReduction` |
| `getOrderDetailFactory.result.object.customerOrder.pricePayment` |
| `getOrderDetailFactory.result.object.customerOrder.orderCode` |
| `getOrderDetailFactory.result.object.orderExpress.receivePerson` |
| `getOrderDetailFactory.result.object.orderExpress.receivePhone` |
| `getOrderDetailFactory.result.object.orderExpress.receiveAddress` |

### 4.19 `patientList`

- **URL**：`/patientList?customerId`
- **模板**：`views/memberManage/patientList.html`
- **控制器**：`patientListCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.patient.avatar` |
| `item.patient.relationShip` |
| `item.patient.patientName` |
| `item.patient.patientBirthday` |
| `howoldFilter` |
| `item.patient.patientGender` |
| `gender` |
| `item.patient.patientRemark` |
| `item.medicalRecordCount` |
| `item.cashflowReceivedFromCashier` |

**页面动作（ng-click）**

| 动作 |
|---|
| `openHistory(item.patient.id)` |
| `showPatientModal(item.patient.id,$index)` |
| `addUser.editInfo(item)` |
| `hideHistory()` |

### 4.20 `productOrder`

- **URL**：`/productOrder?seckillProductId`
- **模板**：`views/memberManage/productOrder.html`
- **控制器**：`productOrderCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 顾客信息 |
| 2 | 订单编号 |
| 3 | 下单时间 |
| 4 | 实付金额 |
| 5 | 订单状态 |
| 6 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.customer.customerName` |
| `item.customerOrder.orderCode` |
| `item.customerOrder.payTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.customerOrder.pricePayment` |

### 4.21 `promotionDetail`

- **URL**：`/promotionDetail?id`
- **模板**：`views/memberManage/promotionDetail.html`
- **控制器**：`promotionDetailCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 4.22 `recommendCustomer`

- **URL**：`/recommendCustomer`
- **模板**：`views/memberManage/recommendCustomer.html`
- **控制器**：`recommendCustomerCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 活动海报 |
| 3 | 活动说明 |
| 4 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.promotion.title` |
| `item.promotion.thumb` |
| `item.promotion.promotionUrlQrcode` |
| `item.promotion.promotionUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showCode(item.promotion.promotionUrl,$event)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addRecommend`, `firstDoctorList`

### 4.23 `recommendDetail`

- **URL**：`/recommendDetail`
- **模板**：`views/memberManage/recommendDetail.html`
- **控制器**：`recommendDetailCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |
| `selectSchoolIntentionVoList` | `POST /admin/selectSchoolIntentionVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{tab.name}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |
| `pageSize` |
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `tab.name` |
| `item.school.schoolName` |
| `item.schoolClass.className` |
| `item.schoolMateCheck.classMateName` |
| `item.schoolMateCheck.gender` |
| `gender` |
| `item.schoolMateCheck.birthday` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.schoolMateCheck.schoolMateCode` |
| `item.schoolMateCheck.customerMobile` |
| `item.schoolMateCheck.checkStatus` |
| `checkScreenStatus` |
| `item.schoolMateCheck.right1` |
| `vision` |
| `item.schoolMateCheck.left1` |
| `item.schoolMateCheck.right167` |
| `newCheckResult` |
| `item.schoolMateCheck.left167` |
| `item.schoolMateCheck.right2` |
| `item.schoolMateCheck.left2` |
| `item.schoolMateCheck.left87` |
| `item.schoolMateCheck.right15` |
| `item.schoolMateCheck.left15` |
| `item.schoolMateCheck.right14` |
| `item.schoolMateCheck.left14` |
| `item.schoolMateCheck.right13` |
| `item.schoolMateCheck.left13` |
| `item.schoolMateCheck.right265` |
| `quCheckResult` |
| `item.schoolMateCheck.left265` |
| `item.activeStatus` |
| `hasActive` |
| `item.recommendPhone` |
| `item.recommendPhone.intention` |
| `item.recommendPhone.phone` |
| `item.recommendPhone.intentionRemark` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `daochu()` |
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool($event)` |
| `showSatisfyModal(item,$index)` |

**跳转到**：`areaRoleAdmin`, `recommendDetail`, `recommendTable`

### 4.24 `recommendPhoneList`

- **URL**：`/recommendPhoneList`
- **模板**：`views/memberManage/recommendPhoneList.html`
- **控制器**：`recommendPhoneListCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `assignRecommendPhoneList` | `POST /admin/assignRecommendPhoneList.json` |
| `getCorpPointRule` | `POST /admin/getCorpPointRule.json` |
| `getFundusCheckRecordListOfCustomer` | `POST /admin/getFundusCheckRecordListOfCustomer.json` |
| `getRecommendPhoneVo` | `POST /admin/getRecommendPhoneVo.json` |
| `getSchoolMateCheckVoOfCustomer` | `POST /admin/getSchoolMateCheckVoOfCustomer.json` |
| `getSchoolMateCheckVoOfRecommendPhone` | `POST /admin/getSchoolMateCheckVoOfRecommendPhone.json` |
| `giveFirstReward` | `POST /admin/giveFirstReward.json` |
| `giveSecondReward` | `POST /admin/giveSecondReward.json` |
| `linkRecommendPhone` | `POST /admin/linkRecommendPhone.json` |
| `selectEmployeeVoListOfMyCompany` | `POST /admin/selectEmployeeVoListOfMyCompany.json` |
| `selectOrderVoListByCustomerId` | `POST /admin/selectOrderVoListByCustomerId.json` |
| `selectRecommendPhoneVoList` | `POST /admin/selectRecommendPhoneVoList.json` |

**表单标签**

| 标签 |
|---|
| 比较有兴趣，或愿意到店 很感兴趣，也觉得平台可以，或可以来公司约谈的 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 客资 |
| 2 | 跟进情况 |
| 3 | 推荐人 |
| 4 | 推荐日期 |
| 5 | 客户 |
| 6 | 性别 |
| 7 | 来源 |
| 8 | 来源备注 |
| 9 | 意向度 |
| 10 | 备注 |
| 11 | 状态 |
| 12 | 执行人 |
| 13 | 分配人 |
| 14 | 分配日期 |
| 15 | 计划执行人 |
| 16 | 分配状态 |
| 17 | 操作 |
| 18 | 推荐人 |
| 19 | 奖励 |
| 20 | 检查日期 |
| 21 | 姓名 |
| 22 | 性别 |
| 23 | 筛查计划 |
| 24 | 机构名称 |
| 25 | 视力筛查结果 |
| 26 | 商品信息 单价 数量 备注 |
| 27 | 收货信息 |
| 28 | 实付金额 |
| 29 | 订单状态 |
| 30 | 操作 |
| 31 | 检查编号 |
| 32 | 检查日期 |
| 33 | 姓名 |
| 34 | 性别 |
| 35 | 检查结果 |
| 36 | 检查日期 |
| 37 | 姓名 |
| 38 | 性别 |
| 39 | 筛查计划 |
| 40 | 机构名称 |
| 41 | 视力筛查结果 |
| 42 | 推荐日期 |
| 43 | 客户名称 |
| 44 | 联系号码 |
| 45 | 来源 |
| 46 | 分配状态 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `searchTime.startTime` |
| `searchTime.endTime` |
| `data.intention` |
| `data.intentionRemark` |
| `data.point` |
| `secondPoint` |
| `taskGood.saveReqInfoDate.startTime` |
| `taskGood.saveReqInfoDate.endTime` |
| `taskGood.isAll` |
| `taskGood.recommendArray[$index]` |
| `taskGood.pageSize` |
| `obj.recommendKeyword` |
| `obj.customerKeyword` |
| `obj.remarkKeyword` |
| `taskGood.saveReqInfo.recommendKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `item.recommendPhone.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.recommendPhone.name` |
| `item.recommendPhone.phone` |
| `item.recommendPhone.sex` |
| `gender` |
| `item.recommendPhone.type` |
| `recommendType` |
| `item.recommendPhone.remark` |
| `item.recommendPhone.intentionRemark` |
| `item.recommendPhone.status` |
| `recommendStatus` |
| `item.recommendPhone.lastLinkPerson` |
| `item.assignAdmin` |
| `item.assignAdmin.nickname` |
| `item.recommendPhone.planAssignedTime` |
| `item.planExcuteDoctor` |
| `item.planExcuteDoctor.employeeName` |
| `item.recommendPhone.planStatus` |
| `planStatusFilter` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `item.recommendCustomer.rewardContent` |
| `item.recommendCustomer.secondRewardContent` |
| `mateCheckObject.schoolMateCheck.classMateName` |
| `mateCheckObject.schoolMateCheck.gender` |
| `mateCheckObject.schoolMateCheck` |
| `howoldMatecheck` |
| `mateCheckObject.schoolPlan.planName` |
| `mateCheckObject.school.schoolName` |
| `mateCheckObject.schoolClass.className` |
| `mateCheckObject.schoolMateCheck.right1` |
| `vision` |
| `mateCheckObject.schoolMateCheck.right64` |
| `mateCheckObject.schoolMateCheck.left1` |
| `mateCheckObject.schoolMateCheck.left167` |
| `newCheckResult` |
| `mateCheckObject.schoolMateCheck.left64` |
| `mateCheckObject.schoolMateCheck.left68` |
| `item.customerOrder.orderCode` |
| `iten.modelPicture` |
| `modelPicture` |
| `iten.productName` |
| `iten.model1` |
| `iten.model2` |
| `iten.productSkuId` |
| `iten.marketPrice` |
| `iten.useCount` |
| `iten.discountedRemark` |
| `iten.remark` |
| `item.orderExpress.expressType` |
| `expressType` |
| `item.orderExpress.receiveAddress` |
| `item.orderExpress.receivePerson` |
| `item.orderExpress.receivePhone` |
| `item.cashflow.totalPayment` |
| `item` |
| `orderAndExpressStatus` |
| `item.medicalRecordNo` |
| `item.checkDate` |
| `HH` |
| `mm` |
| `ss` |
| `item.name` |
| `item.gender` |
| `schoolMateCheckVoOfRecommendPhone.schoolMateCheck.classMateName` |
| `schoolMateCheckVoOfRecommendPhone.schoolPlan.planName` |
| `schoolMateCheckVoOfRecommendPhone.school.schoolName` |
| `schoolMateCheckVoOfRecommendPhone.schoolClass.className` |
| `schoolMateCheckVoOfRecommendPhone.schoolMateCheck.right64` |
| `schoolMateCheckVoOfRecommendPhone.schoolMateCheck.left64` |
| `schoolMateCheckVoOfRecommendPhone.schoolMateCheck.left68` |
| `getInitPointFactory.result.object.payPoint` |
| `getInitPointFactory.result.object.toMoney` |
| `username` |
| `nowDate` |
| `item.recommendPhone.id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `taskGoods()` |
| `openPop(` |
| `showDetailModal(item)` |
| `showSatisfyModal(item.recommendPhone.id,item.recommendPhone.intention,item.recommendPhone.intentionRemark,$index)` |
| `showRewardModal(item.recommendPhone.id,$index)` |
| `showSecondRewardModal(item.recommendPhone.id,$index)` |
| `hideModal()` |
| `modifySatisfy()` |
| `setTab(1)` |
| `setTab(3)` |
| `setTab(0)` |
| `setTab(2)` |
| `jump(item.pdf)` |
| `jump(item.h5)` |
| `reward()` |
| `secondReward()` |
| `openPoptaskGood(` |
| `taskGood.checkAll()` |
| `setLabelBtn()` |
| `closeTaskGood()` |
| `addTaskGood()` |

**跳转到**：`areaRoleAdmin`, `recommendTable`

### 4.25 `recommendTable`

- **URL**：`/recommendTable`
- **模板**：`views/memberManage/recommendTable.html`
- **控制器**：`recommendTableCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getDefaultSchoolPlanByAdminId` | `POST /admin/getDefaultSchoolPlanByAdminId.json` |
| `getSchoolClassList` | `POST /admin/getSchoolClassList.json` |
| `selectInYearListBySchoolPlan` | `POST /admin/selectInYearListBySchoolPlan.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inYear` |
| `obj.classId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.planName` |
| `obj.schoolName` |
| `inyear` |
| `inyear.id` |
| `inyear.className` |
| `getStatOperationReport` |
| `filterkey` |
| `schoolPlan.planName` |
| `schoolName` |
| `inYear` |
| `className` |
| `getStatOperationReport.schoolMateCount` |
| `getStatOperationReport.examinedSchoolMateCount` |
| `getStatOperationReport.activedCount` |
| `getStatOperationReport.activedRate` |
| `toFixed` |
| `getStatOperationReport.visitedCount` |
| `getStatOperationReport.visitedRate` |
| `getStatOperationReport.oneStarIntentionCount` |
| `getStatOperationReport.oneStarIntentionRate` |
| `getStatOperationReport.twoStarIntentionCount` |
| `getStatOperationReport.twoStarIntentionRate` |
| `getStatOperationReport.threeStarIntentionCount` |
| `getStatOperationReport.fourStarIntentionCount` |
| `getStatOperationReport.fiveStarIntentionCount` |
| `item.schoolName` |
| `item.inYear` |
| `item.className` |
| `item.schoolMateCount` |
| `item.examinedSchoolMateCount` |
| `item.activedCount` |
| `item.activedRate` |
| `item.visitedCount` |
| `item.visitedRate` |
| `item.oneStarIntentionCount` |
| `item.oneStarIntentionRate` |
| `item.twoStarIntentionCount` |
| `item.twoStarIntentionRate` |
| `item.threeStarIntentionCount` |
| `item.threeStarIntentionRate` |
| `item.fourStarIntentionCount` |
| `item.fourStarIntentionRate` |
| `item.fiveStarIntentionCount` |
| `item.fiveStarIntentionRate` |
| `obj.schoolPlanId` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showSelectPlan()` |
| `showSelectSchool()` |
| `clearSchool($event)` |

**跳转到**：`areaRoleAdmin`, `recommendDetail`, `recommendTable`

### 4.26 `requirement`

- **URL**：`/requirement`
- **模板**：`views/memberManage/requirement.html`
- **控制器**：`requirementCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteSmsRequirement` | `POST /admin/deleteSmsRequirement.json` |
| `getSmsRequirement` | `POST /admin/getSmsRequirement.json` |
| `selectSmsRequirementList` | `POST /admin/selectSmsRequirementList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 发布时间 |
| 2 | 发布人 |
| 3 | 类型 |
| 4 | 标题 |
| 5 | 内容 |
| 6 | 备注 |
| 7 | 审核状态 |
| 8 | 支付状态 |
| 9 | 开发状态 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `insertSmsRequirement.params.content` |
| `auditSmsRequirement.params.content` |
| `obj.keyword` |
| `insertSmsRequirement.params.title` |
| `auditSmsRequirement.params.title` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.smsRequirement.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.admin.nickname` |
| `item.smsRequirement.requirementType` |
| `requirementTypeFilter` |
| `item.smsRequirement.title` |
| `item.smsRequirement.content` |
| `index` |
| `remarkFilter` |
| `remark.remarkContent` |
| `handleStatus.handleStatusJudge` |
| `item.smsRequirement` |
| `name` |
| `item.smsRequirement.payStatus` |
| `payStatus` |
| `item.smsRequirement.productStatus` |
| `productStatus` |
| `insertSmsRequirement.title` |
| `insertSmsRequirement.modelTypeMap` |
| `insertSmsRequirement.requirementType` |
| `auditSmsRequirement.params.requirementType` |
| `auditSmsRequirement.params.notAcceptReason` |

**页面动作（ng-click）**

| 动作 |
|---|
| `insertSmsRequirement.showTypeOpen(false,$event)` |
| `vipTip.close()` |
| `showPhoto=true` |
| `insertSmsRequirement.showTypeOpen(true,$event)` |
| `insertSmsRequirement.setType(2)` |
| `insertSmsRequirement.setType(0)` |
| `insertSmsRequirement.setType(1)` |
| `requirement.pay(item.smsRequirement.id)` |
| `requirement.look(item.smsRequirement.id)` |
| `requirement.delete(item.smsRequirement.id,$index)` |
| `insertSmsRequirement.close()` |
| `insertSmsRequirement.affirm()` |
| `auditSmsRequirement.close()` |

### 4.27 `requirementStatus`

- **URL**：`/requirementStatus?id`
- **模板**：`views/memberManage/requirementStatus.html`
- **控制器**：`requirementStatusCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelSmsRequirement` | `POST /admin/cancelSmsRequirement.json` |
| `getRequirementOrderVo` | `POST /admin/getRequirementOrderVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 类型 |
| 2 | 标题 |
| 3 | 内容 |
| 4 | 审核状态 |
| 5 | 未采纳原因 |
| 6 | 开始开发时间 |
| 7 | 预计开发周期 |
| 8 | 金额 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `accept.params.cancelReason` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `requirementVo.smsRequirement.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `requirementVo.admin.nickname` |
| `requirementVo.admin.mobile` |
| `requirementVo.smsRequirement.payStatus` |
| `payStatus` |
| `requirementVo.smsRequirement.notAcceptReason` |
| `requirementVo.smsRequirement.requirementType` |
| `requirementTypeFilter` |
| `requirementVo.smsRequirement.title` |
| `requirementVo.smsRequirement.content` |
| `handleStatus.handleStatusJudge` |
| `requirementVo.smsRequirement` |
| `name` |
| `requirementVo.smsRequirement.productStartTime` |
| `requirementVo.smsRequirement.productDays` |
| `requirementVo.smsRequirement.productPrice` |
| `item.name` |
| `item.amount` |
| `corpExchangeCode.exchangeCode` |
| `requirementVo.smsRequirement.demoImage` |
| `item` |

**页面动作（ng-click）**

| 动作 |
|---|
| `accept.openPay()` |
| `accept.open(true)` |
| `accept.open(false)` |
| `accept.affirm()` |

### 4.28 `secKillProductDetail`

- **URL**：`/secKillProductDetail?seckillProductId`
- **模板**：`views/memberManage/secKillProductDetail.html`
- **控制器**：`secKillProductDetailCtrl`
- **端点数**：12

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitRefundOrderLog` | `POST /admin/commitRefundOrderLog.json` |
| `createRefundOrderLog` | `POST /admin/createRefundOrderLog.json` |
| `deliveryOrder` | `POST /admin/deliveryOrder.json` |
| `getOrderVo` | `POST /admin/getOrderVo.json` |
| `getPromotionQrcode` | `POST /admin/getPromotionQrcode.json` |
| `getPromotionVo` | `POST /admin/getPromotionVo.json` |
| `getSeckillProductVo` | `POST /admin/getSeckillProductVo.json` |
| `invalidSeckillProduct` | `POST /admin/invalidSeckillProduct.json` |
| `pickUpOrder` | `POST /admin/pickUpOrder.json` |
| `selectOrderVoListByCorpId` | `POST /admin/selectOrderVoListByCorpId.json` |
| `selectPromotionVoList` | `POST /admin/selectPromotionVoList.json` |
| `selectSeckillProductVoList` | `POST /admin/selectSeckillProductVoList.json` |

**必填项**

| 标签 |
|---|
| * 商品名称： |
| * 图片 |
| * 图片： |
| * 规格： |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |

**表单标签**

| 标签 |
|---|
| * 商品名称： |
| * 图片 |
| * 图片： |
| 描述： |
| * 规格： |
| 无规格 |
| 一种规格 |
| 两种规格 |
| * |
| * 市场价： |
| * 秒杀价： |
| * 发放数量： |
| * 开始时间： |
| * 结束时间： |
| 允许退货： |
| 不允许 |
| 允许 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.modelPicture` |
| `obj.description` |
| `obj.modelType` |
| `obj.model1Name` |
| `obj.model1` |
| `obj.model2Name` |
| `obj.model2` |
| `marketPrice` |
| `seckillPrice` |
| `obj.totalCount` |
| `obj.startTime` |
| `momentDate` |
| `startTime` |
| `obj.endTime` |
| `endTime` |
| `obj.permissionToReturn` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.productName` |
| `obj.modelPicture` |
| `item` |
| `obj.description` |
| `modelName.id` |
| `modelName.name` |
| `marketPrice` |
| `seckillPrice` |
| `obj.totalCount` |
| `startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `endTime` |

**页面动作（ng-click）**

| 动作 |
|---|
| `colorModal= false;` |
| `open1()` |
| `open2()` |
| `goBack()` |

### 4.29 `secKillProductList`

- **URL**：`/secKillProductList?promotionId`
- **模板**：`views/memberManage/secKillProductList.html`
- **控制器**：`secKillProductListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 商品图片 |
| 2 | 商品名称 |
| 3 | 规格 |
| 4 | 市场价/秒杀价 |
| 5 | 总数/剩余 |
| 6 | 访客/参与/订单 |
| 7 | 有效期限 |
| 8 | 状态 |
| 9 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPromotionFactory.result.object.promotion.thumb` |
| `getPromotionFactory.result.object.promotion.title` |
| `getPromotionFactory.result.object.promotion.remark` |
| `item.promotionURL` |
| `getPromotionFactory.result.object.promotion.promotionUrlQrcode` |
| `qrcodeImg` |
| `getPromotionFactory.result.object.promotion.promotionUrl` |
| `checkCountFactory.object.waitingExamineCount` |
| `checkCountFactory.object.examiningCount` |
| `checkCountFactory.object.examinedCount` |
| `item.seckillProduct.modelPicture` |
| `modelPicture` |
| `item.seckillProduct.productName` |
| `item.seckillProduct.model1Name` |
| `item.seckillProduct.model1` |
| `item.seckillProduct.model2Name` |
| `item.seckillProduct.model2` |
| `item.seckillProduct.marketPrice` |
| `item.seckillProduct.seckillPrice` |
| `item.seckillProduct.totalCount` |
| `item.seckillProduct.remainCount` |
| `item.visitCount` |
| `item.pushCount` |
| `item.orderCount` |
| `item.seckillProduct.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.seckillProduct.endTime` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideCode()` |
| `showCode(getPromotionFactory.result.object.promotion.promotionUrl,$event)` |
| `search(null)` |
| `search(0)` |
| `search(1)` |
| `search(2)` |
| `unActive(item.seckillProduct.id)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`secKillProductAdmin`, `secKillPromotionList`

### 4.30 `secKillPromotionList`

- **URL**：`/secKillPromotionList`
- **模板**：`views/memberManage/secKillPromotionList.html`
- **控制器**：`secKillPromotionListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 活动海报 |
| 3 | 提货地址 |
| 4 | 活动说明 |
| 5 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `promotionType` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.promotion.title` |
| `item.promotion.thumb` |
| `item.promotion.address` |
| `item.promotion.remark` |
| `qrcodeImg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideCode()` |
| `showCode(item.promotion.promotionUrl,item.promotion.id,$event)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addPromotion`

**下拉数据源（ng-options）**

```
x.id as x.name for x in statusArr
```

### 4.31 `selectOrderList`

- **URL**：`/selectOrderList?keyword`
- **模板**：`views/memberManage/selectOrderList.html`
- **控制器**：`selectOrderListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 商品信息 单价 数量 备注 |
| 2 | 收货信息 |
| 3 | 实付金额 |
| 4 | 支付方式 |
| 5 | 订单状态 |
| 6 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTime` |
| `obj.ladingCode` |
| `obj.expressType` |
| `obj.expressStatus` |
| `selectedId` |
| `deliveryObj.expressCode` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `item.customerOrder.orderCode` |
| `item.cashflow.tradeNo` |
| `item.cashflow.transactionId` |
| `iten.modelPicture` |
| `modelPicture` |
| `iten.productName` |
| `iten.model1` |
| `iten.model2` |
| `iten.productSkuId` |
| `iten.marketPrice` |
| `iten.useCount` |
| `iten.discountedRemark` |
| `iten.remark` |
| `item.orderExpress.expressType` |
| `expressType` |
| `item.orderExpress.receiveAddress` |
| `item.orderExpress.receivePerson` |
| `item.orderExpress.receivePhone` |
| `item.cashflow.totalPayment` |
| `item.cashflow.payType` |
| `payType` |

**页面动作（ng-click）**

| 动作 |
|---|
| `clearKeyword()` |
| `open1()` |
| `open2()` |
| `search()` |
| `searchType(null)` |
| `searchType(1)` |
| `searchType(2)` |
| `searchOrder(null)` |
| `searchOrder(0)` |
| `searchOrder(1)` |
| `searchOrder(2)` |
| `searchExpress(null)` |
| `searchExpress(0)` |
| `searchExpress(1)` |
| `searchExpress(2)` |
| `setRefundStatus(null)` |
| `setRefundStatus(0)` |
| `setRefundStatus(1)` |
| `pickUp(item.customerOrder.id,$index)` |
| `showDelivery(item.customerOrder.id,$index)` |
| `refund(item,$index)` |
| `deliveryModal=false` |
| `deliveryGood()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in expressCompany
x.id as x.name for x in statusArr
x.id as x.name for x in typeArr
```

### 4.32 `sendPlatform`

- **URL**：`/sendPlatform`
- **模板**：`views/memberManage/sendPlatform.html`
- **控制器**：`sendPlatformCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelTemplateBatchSendTask` | `POST /admin/cancelTemplateBatchSendTask.json` |
| `selectTaskTemplateBatchSendList` | `POST /admin/selectTaskTemplateBatchSendList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 目标人群 |
| 3 | 预计投放人数 |
| 4 | 发送成功 |
| 5 | 发送状态 |
| 6 | 异常原因 |
| 7 | 开始发送时间 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.taskName` |
| `item.totalPatientCount` |
| `item.sendPatientCount` |
| `item.status` |
| `smsStatus` |
| `item.failReason` |
| `item.taskStartTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |

**页面动作（ng-click）**

| 动作 |
|---|
| `newAddGroup()` |
| `lookCondition(item.id)` |
| `lookDetails(item.id)` |
| `cancelTask(item.id,$index)` |

### 4.33 `updateMember`

- **URL**：`/updateMember?customerId`
- **模板**：`views/memberManage/updateMember.html`
- **控制器**：`updateMemberCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `disBandingWechatByCustomerId` | `POST /admin/disBandingWechatByCustomerId.json` |
| `getBandingWechatQrcode` | `POST /admin/getBandingWechatQrcode.json` |
| `getCustomerVo` | `POST /admin/getCustomerVo.json` |
| `isBandingWechat` | `POST /admin/isBandingWechat.json` |
| `saveCustomerInfo` | `POST /admin/saveCustomerInfo.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `updateCustomerTags` | `POST /admin/updateCustomerTags.json` |

**必填项**

| 标签 |
|---|
| * 会员姓名 |

**表单标签**

| 标签 |
|---|
| 会员姓名： |
| 手机号： |
| 会员来源： |
| 保存修改 |
| * 会员姓名 |
| 手机号 |
| 会员来源 |
| 微信绑定管理 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `customerFactory.vo.customer.customerName` |
| `customerFactory.vo.customer.linkMobile` |
| `customerFactory.vo.customer.channel` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.employeeTitle` |
| `customerFactory.vo.wechatCustomer.nickName` |
| `imgSrc` |

**页面动作（ng-click）**

| 动作 |
|---|
| `saveCustomerInfo()` |
| `connectWeixin()` |
| `hidePatient()` |
