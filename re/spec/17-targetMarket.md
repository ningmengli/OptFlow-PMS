# 17｜模块 targetMarket 精准营销

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/targetMarket/` |
| 中文名 | 精准营销 |
| 开发波次 | W3 |
| 页面数 | **3** |
| 端点数（去重） | **15** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addTargetCoupon` | `/addTargetCoupon` | `views/targetMarket/addTargetCoupon.html` | `addTargetCouponCtrl` | 10 |
| 2 | `targetCouponDetail` | `/targetCouponDetail?taskCouponBatchSendId` | `views/targetMarket/targetCouponDetail.html` | `targetCouponDetailCtrl` | 9 |
| 3 | `targetCouponList` | `/targetCouponList` | `views/targetMarket/targetCouponList.html` | `targetCouponListCtrl` | 0 |

## §2 端点清单（去重 15 个）

- `POST /admin/createCouponBatchSendTask.json`
- `POST /admin/getBatchSendCustomerCouponVoList.json`
- `POST /admin/getCouponVo.json`
- `POST /admin/getCustomerCouponVo.json`
- `POST /admin/getCustomerMemberDataList.json`
- `POST /admin/getMemberList.json`
- `POST /admin/getOrderBrandList.json`
- `POST /admin/getOrderCategoryList.json`
- `POST /admin/getTag.json`
- `POST /admin/getTaskCouponBatchSendVo.json`
- `POST /admin/selectCouponVoList.json`
- `POST /admin/selectTagList.json`
- `POST /admin/selectTaskCouponBatchSendVoList.json`
- `POST /admin/selectWecomTagList.json`
- `POST /admin/useCoupon.json`

## §3 逐页字段规格

### 17.1 `addTargetCoupon`

- **URL**：`/addTargetCoupon`
- **模板**：`views/targetMarket/addTargetCoupon.html`
- **控制器**：`addTargetCouponCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createCouponBatchSendTask` | `POST /admin/createCouponBatchSendTask.json` |
| `getCouponVo` | `POST /admin/getCouponVo.json` |
| `getCustomerMemberDataList` | `POST /admin/getCustomerMemberDataList.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getOrderBrandList` | `POST /admin/getOrderBrandList.json` |
| `getOrderCategoryList` | `POST /admin/getOrderCategoryList.json` |
| `getTag` | `POST /admin/getTag.json` |
| `selectCouponVoList` | `POST /admin/selectCouponVoList.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `selectWecomTagList` | `POST /admin/selectWecomTagList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 基本信息 |
| 2 | 城市 |
| 3 | 消费频次 |
| 4 | 消费金额 |
| 5 | 最近一次消费 |
| 6 | 家庭成员 |
| 7 | 已购品类 |
| 8 | 已购品牌 |
| 9 | 会员标签 |
| 10 | 优惠券名称 |
| 11 | 种类/面额 |
| 12 | 有效期 |
| 13 | 限制条件 |
| 14 | 使用说明 |
| 15 | 剩余库存 |
| 16 | 到期提醒短信 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.startTime` |
| `rightTimer` |
| `dateSearch` |
| `orderPayment` |
| `orderCount` |
| `obj.hasMobile` |
| `obj.hasWechat` |
| `obj.memberId` |
| `categoryIdArray[$index]` |
| `brandIdArray[$index]` |
| `newTagIdArray[$index]` |
| `smsWechatEnable` |
| `obj.wechatContent` |
| `obj.taskName` |
| `keyword` |
| `obj.couponId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `item.id` |
| `item.memberName` |
| `item.categoryName` |
| `item.brandName` |
| `item.tagName` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.wechatCustomer.city` |
| `item.customerRmfData.orderCount` |
| `item.customerRmfData.orderPrice` |
| `item.customerRmfData.categoryNames` |
| `item.customerRmfData.brandNames` |
| `iten.tagName` |
| `getCouponFactory.result.object.coupon.couponName` |
| `getCouponFactory.result.object.couponValue` |
| `getCouponFactory.result.object.coupon.useTimeStartDays` |
| `getCouponFactory.result.object.coupon.useTimeEndDays` |
| `getCouponFactory.result.object.coupon.useScene` |
| `useScene` |
| `getCouponFactory.result.object.coupon.useOverMoney` |
| `getCouponFactory.result.object.coupon.useOverCount` |
| `getCouponFactory.result.object.coupon.useContent` |
| `chosePerson.wechatSendName` |
| `item.coupon.id` |
| `item.coupon.couponName` |
| `item.coupon.couponType` |
| `couponType` |
| `item.couponValue` |
| `item.coupon.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.coupon.useTimeStartDays` |
| `item.coupon.useTimeEnd` |
| `item.coupon.useTimeEndDays` |
| `item.coupon.useScene` |
| `item.coupon.useOverMoney` |
| `item.coupon.useOverCount` |
| `item.coupon.useContent` |
| `item.coupon.couponTotalCount` |
| `item.coupon.couponSendCount` |
| `item.coupon.sendExpireMsg` |
| `sendExpireMsg` |

**页面动作（ng-click）**

| 动作 |
|---|
| `yulan()` |
| `open1()` |
| `open2()` |
| `searchDate()` |
| `search()` |
| `setEnable(` |
| `searchAllCateId()` |
| `searchAllBrandId()` |
| `searchAllTagId()` |
| `hideCouponModal()` |
| `showSendModal()` |
| `setEnable2(true,true)` |
| `setEnable2(true,false)` |
| `chosePerson.setShow(true)` |
| `sendTask()` |
| `modify()` |

**跳转到**：`targetCouponList`

### 17.2 `targetCouponDetail`

- **URL**：`/targetCouponDetail?taskCouponBatchSendId`
- **模板**：`views/targetMarket/targetCouponDetail.html`
- **控制器**：`targetCouponDetailCtrl`
- **端点数**：9

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBatchSendCustomerCouponVoList` | `POST /admin/getBatchSendCustomerCouponVoList.json` |
| `getCustomerCouponVo` | `POST /admin/getCustomerCouponVo.json` |
| `getMemberList` | `POST /admin/getMemberList.json` |
| `getOrderBrandList` | `POST /admin/getOrderBrandList.json` |
| `getOrderCategoryList` | `POST /admin/getOrderCategoryList.json` |
| `getTaskCouponBatchSendVo` | `POST /admin/getTaskCouponBatchSendVo.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |
| `selectTaskCouponBatchSendVoList` | `POST /admin/selectTaskCouponBatchSendVoList.json` |
| `useCoupon` | `POST /admin/useCoupon.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 优惠券名称 |
| 2 | 类型/面额 |
| 3 | 有效期 |
| 4 | 限制条件 |
| 5 | 使用说明 |
| 6 | 库存 |
| 7 | 优惠券劵码 |
| 8 | 状态 |
| 9 | 领取时间 |
| 10 | 会员 |
| 11 | 核销人 |
| 12 | 核销时间 |
| 13 | 核销 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.customerKeyword` |
| `obj.customerCouponStatus` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCouponFactory.result.object.coupon.couponName` |
| `getCouponFactory.result.object.coupon.couponType` |
| `couponType` |
| `getCouponFactory.result.object.coupon.couponValue` |
| `getCouponFactory.result.object.coupon.couponRate` |
| `getCouponFactory.result.object.coupon.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getCouponFactory.result.object.coupon.useTimeStartDays` |
| `getCouponFactory.result.object.coupon.useTimeEnd` |
| `getCouponFactory.result.object.coupon.useTimeEndDays` |
| `getCouponFactory.result.object.coupon.useScene` |
| `useScene` |
| `getCouponFactory.result.object.coupon.useOverMoney` |
| `getCouponFactory.result.object.coupon.useOverCount` |
| `getCouponFactory.result.object.coupon.useContent` |
| `getCouponFactory.result.object.couponValue` |
| `getCouponFactory.result.object.customerMemberParam.keyword` |
| `getCouponFactory.result.object.customerMemberParam.orderPriceFrom` |
| `getCouponFactory.result.object.customerMemberParam.orderPriceTo` |
| `getCouponFactory.result.object.customerMemberParam.orderCountFrom` |
| `getCouponFactory.result.object.customerMemberParam.orderCountTo` |
| `item.memberName` |
| `getCouponFactory.result.object.customerMemberParam.channel` |
| `item.categoryName` |
| `cateNameStr` |
| `item.brandName` |
| `brandNameStr` |
| `tagNameStr` |
| `getCouponFactory.result.object.taskCouponBatchSend.sendCustomerCount` |
| `getCouponFactory.result.object.couponUseCount` |
| `item.customerCoupon.couponCode` |
| `item.customerCoupon.status` |
| `couponStatus` |
| `item.customerCoupon.gmtCreate` |
| `HH` |
| `mm` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerCoupon.checkPerson` |
| `item.customerCoupon.useTime` |
| `getCouponVoFactory.object.coupon.couponType` |
| `getCouponVoFactory.object.couponValue` |
| `getCouponVoFactory.object.customerCoupon.useTimeTo` |
| `getCouponVoFactory.object.coupon.useOverMoney` |
| `getCouponVoFactory.object.coupon.useOverCount` |
| `getCouponVoFactory.object.coupon.useScene` |
| `getCouponVoFactory.object.coupon.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `showCouponModify(item.customerCoupon.id,$event)` |
| `hideCouponModal()` |
| `modifycoupon()` |

### 17.3 `targetCouponList`

- **URL**：`/targetCouponList`
- **模板**：`views/targetMarket/targetCouponList.html`
- **控制器**：`targetCouponListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 目标人群 |
| 3 | 投放人数 |
| 4 | 成功发放 |
| 5 | 发放状态 |
| 6 | 开始发券时间 |
| 7 | 使用人数 |
| 8 | 到期提醒短信 |
| 9 | 发送到期短信时间 |
| 10 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.taskCouponBatchSend.taskName` |
| `item.taskCouponBatchSend.totalCustomerCount` |
| `item.taskCouponBatchSend.sendCustomerCount` |
| `item.batchFileTask.status` |
| `importStatus` |
| `item.batchFileTask.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.couponUseCount` |
| `item.coupon.sendExpireMsg` |
| `sendExpireMsg` |
| `item.coupon.useTimeEnd` |
