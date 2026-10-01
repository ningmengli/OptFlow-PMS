# 20｜模块 couponAdmin 优惠券

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/couponAdmin/` |
| 中文名 | 优惠券 |
| 开发波次 | W3 |
| 页面数 | **4** |
| 端点数（去重） | **13** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addCoupon` | `/addCoupon` | `views/couponAdmin/addCoupon.html` | `addCouponCtrl` | 6 |
| 2 | `couponHistory` | `/couponHistory` | `views/couponAdmin/couponHistory.html` | `couponHistoryCtrl` | 0 |
| 3 | `couponList` | `/couponList` | `views/couponAdmin/couponList.html` | `couponListCtrl` | 4 |
| 4 | `modifyCoupon` | `/modifyCoupon?couponId` | `views/couponAdmin/modifyCoupon.html` | `modifyCouponCtrl` | 6 |

## §2 端点清单（去重 13 个）

- `POST /admin/activeCoupon.json`
- `POST /admin/createCoupon.json`
- `POST /admin/getCouponVo.json`
- `POST /admin/getCustomerCouponVo.json`
- `POST /admin/invalidCoupon.json`
- `POST /admin/selectCouponVoList.json`
- `POST /admin/selectCustomerCouponVoList.json`
- `POST /admin/selectCustomerList.json`
- `POST /admin/updateActiveCoupon.json`
- `POST /admin/updateCreatingCoupon.json`
- `POST /admin/updateNews.json`
- `POST /admin/useCoupon.json`
- `POST /auth/isAdminTokenOk.json`

## §3 逐页字段规格

### 20.1 `addCoupon`

- **URL**：`/addCoupon`
- **模板**：`views/couponAdmin/addCoupon.html`
- **控制器**：`addCouponCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createCoupon` | `POST /admin/createCoupon.json` |
| `getCustomerCouponVo` | `POST /admin/getCustomerCouponVo.json` |
| `selectCustomerCouponVoList` | `POST /admin/selectCustomerCouponVoList.json` |
| `selectCustomerList` | `POST /admin/selectCustomerList.json` |
| `useCoupon` | `POST /admin/useCoupon.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**必填项**

| 标签 |
|---|
| * 优惠券名称： |
| * 优惠券颜色： |
| * 类型： |
| * 发放量： |
| * 面额： |
| * 折扣： |
| * 商家备注： |

**表单标签**

| 标签 |
|---|
| * 优惠券名称： |
| * 优惠券颜色： |
| * 类型： |
| 抵用券 |
| 折扣券 |
| * 发放量： |
| * 面额： |
| * 折扣： |
| * 商家备注： |
| 订单金额： |
| 不限 |
| 购满 |
| 每人限领 |
| 限领 |
| 积分兑换 |
| 使用积分兑换 |
| 生效日期 |
| 固定日期： |
| 自定义领取后： |
| 失效日期 |
| 发送到期提醒短信 |
| （失效日期前7天短信提醒顾客） |
| 每人限领： |
| 商品数量： |
| 使用场景： |
| 线上使用 |
| {{corpInfo. companyTitle}}使用 |
| 使用说明： |
| 允许退货： |
| 不允许 |
| 允许 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.couponName` |
| `obj.couponType` |
| `obj.couponTotalCount` |
| `obj.couponValue` |
| `obj.couponRate` |
| `obj.couponRemark` |
| `overMoney` |
| `obj.useOverMoney` |
| `obj.useTimeStartType` |
| `obj.useTimeStart` |
| `obj.useTimeStartDays` |
| `obj.useTimeEnd` |
| `obj.useTimeEndDays` |
| `overReceive` |
| `obj.receiveLimit` |
| `overCount` |
| `obj.useOverCount` |
| `obj.useScene` |
| `obj.useContent` |
| `obj.permissionToReturn` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `corpInfo.` |
| `companyTitle` |
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `obj.couponName` |
| `obj.couponValue` |
| `obj.couponRate` |
| `discount` |
| `obj.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.useTimeStartDays` |
| `obj.useTimeEnd` |
| `obj.useTimeEndDays` |
| `obj.receiveLimit` |
| `obj.useOverMoney` |
| `obj.useOverCount` |
| `obj.useScene` |
| `useScene` |
| `obj.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `colorModal= false;` |
| `showColorModal($event)` |
| `chooseColor(item,$index)` |
| `clearDay()` |
| `open1()` |
| `clearDate()` |
| `open2()` |
| `obj.sendExpireMsg=!obj.sendExpireMsg` |
| `createCoupon()` |

**跳转到**：`couponList`

### 20.2 `couponHistory`

- **URL**：`/couponHistory`
- **模板**：`views/couponAdmin/couponHistory.html`
- **控制器**：`couponHistoryCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 优惠券名称 |
| 2 | 类型/面额 |
| 3 | 优惠券劵码 |
| 4 | 状态 |
| 5 | 领取时间 |
| 6 | 会员 |
| 7 | 核销人 |
| 8 | 核销时间 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.customerKeyword` |
| `obj.status` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.coupon.couponName` |
| `item.coupon.couponType` |
| `couponType` |
| `item.couponValue` |
| `item.customerCoupon.couponCode` |
| `item.customerCoupon.status` |
| `couponStatus` |
| `item.customerCoupon.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
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
| `useScene` |
| `getCouponVoFactory.object.coupon.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchTab(2)` |
| `showCouponModify(item.customerCoupon.id,$event)` |
| `hideCouponModal()` |
| `modifycoupon()` |

**下拉数据源（ng-options）**

```
x.id as x.name for x in status
```

### 20.3 `couponList`

- **URL**：`/couponList`
- **模板**：`views/couponAdmin/couponList.html`
- **控制器**：`couponListCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `invalidCoupon` | `POST /admin/invalidCoupon.json` |
| `selectCouponVoList` | `POST /admin/selectCouponVoList.json` |
| `selectCustomerCouponVoList` | `POST /admin/selectCustomerCouponVoList.json` |
| `updateNews` | `POST /admin/updateNews.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 优惠券名称 |
| 2 | 类型/面额 |
| 3 | 使用/发放/库存 |
| 4 | 有效期 |
| 5 | 限制条件 |
| 6 | 到期提醒短信 |
| 7 | 状态 |
| 8 | 使用说明 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.coupon.couponName` |
| `item.coupon.couponType` |
| `couponType` |
| `item.couponValue` |
| `item.coupon.couponUseCount` |
| `item.coupon.couponSendCount` |
| `item.coupon.couponTotalCount` |
| `item.coupon.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.coupon.useTimeStartDays` |
| `item.coupon.useTimeEnd` |
| `item.coupon.useTimeEndDays` |
| `item.coupon.useScene` |
| `useScene` |
| `item.coupon.useOverMoney` |
| `item.coupon.useOverCount` |
| `item.coupon.sendExpireMsg` |
| `sendExpireMsg` |
| `item.couponStatus` |
| `couponMakeStatus` |
| `item.coupon.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `searchTab(2)` |
| `unActive(item.coupon.id)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addCoupon`, `couponHistory`

### 20.4 `modifyCoupon`

- **URL**：`/modifyCoupon?couponId`
- **模板**：`views/couponAdmin/modifyCoupon.html`
- **控制器**：`modifyCouponCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `activeCoupon` | `POST /admin/activeCoupon.json` |
| `getCouponVo` | `POST /admin/getCouponVo.json` |
| `selectCustomerList` | `POST /admin/selectCustomerList.json` |
| `updateActiveCoupon` | `POST /admin/updateActiveCoupon.json` |
| `updateCreatingCoupon` | `POST /admin/updateCreatingCoupon.json` |
| `isAdminTokenOk` | `POST /auth/isAdminTokenOk.json` |

**必填项**

| 标签 |
|---|
| * 优惠券名称： |
| * 类型： |
| * 发放量： |
| * 面额： |
| * 折扣： |
| * 商家备注： |
| * 优惠券颜色： |
| * 发送到期提醒短信 |
| 优惠券名称 * |
| 优惠券颜色 * |
| 发放量 * |
| 商家备注 * |

**表单标签**

| 标签 |
|---|
| * 优惠券名称： |
| * 类型： |
| 抵用券 |
| 折扣券 |
| * 发放量： |
| * 面额： |
| * 折扣： |
| * 商家备注： |
| 订单金额： |
| 不限 |
| 购满 |
| 每人限领 |
| 限领 |
| 积分兑换 |
| 使用积分兑换 |
| 生效时间 |
| 固定日期： |
| 自定义领取后： |
| 失效时间 |
| 发送到期提醒短信 |
| （失效日期前7天短信提醒顾客） |
| 每人限领： |
| 商品数量： |
| 使用场景： |
| 线上使用 |
| {{corpInfo. companyTitle}}使用 |
| 使用说明： |
| 允许退货： |
| 不允许 |
| 允许 |
| * 优惠券颜色： |
| * 发送到期提醒短信 |
| 已发放量： |
| 优惠券名称 * |
| 优惠券颜色 * |
| 发放量 * |
| 使用说明 |
| 商家备注 * |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.couponName` |
| `obj.couponType` |
| `obj.couponTotalCount` |
| `obj.couponValue` |
| `obj.couponRate` |
| `obj.couponRemark` |
| `overMoney` |
| `obj.useOverMoney` |
| `obj.useTimeStartType` |
| `obj.useTimeStart` |
| `obj.useTimeStartDays` |
| `obj.useTimeEnd` |
| `obj.useTimeEndDays` |
| `overReceive` |
| `obj.receiveLimit` |
| `overCount` |
| `obj.useOverCount` |
| `obj.useScene` |
| `obj.useContent` |
| `obj.permissionToReturn` |
| `data.couponName` |
| `data.couponTotalCount` |
| `data.couponRemark` |
| `data.useContent` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `memberFactory.count` |
| `corpInfo.` |
| `companyTitle` |
| `data.couponSendCount` |
| `homeFactory.result.corp.logo` |
| `homeFactory.result.corp.corporationName` |
| `obj.couponName` |
| `obj.couponValue` |
| `obj.couponRate` |
| `discount` |
| `obj.useTimeStart` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.useTimeStartDays` |
| `obj.useTimeEnd` |
| `obj.useTimeEndDays` |
| `obj.receiveLimit` |
| `obj.useOverMoney` |
| `obj.useOverCount` |
| `obj.useScene` |
| `useScene` |
| `obj.useContent` |
| `data.couponName` |
| `data.couponTotalCount` |
| `data.useContent` |

**页面动作（ng-click）**

| 动作 |
|---|
| `colorModal= false;` |
| `clearDay()` |
| `open1()` |
| `clearDate()` |
| `open2()` |
| `obj.sendExpireMsg=!obj.sendExpireMsg` |
| `showColorModal($event)` |
| `chooseColor(item,$index)` |
| `modifyActive()` |
| `modify()` |
| `activeCoupon()` |

**跳转到**：`couponList`
