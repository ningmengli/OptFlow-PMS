# 23｜模块 grouponAdmin 团购

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/grouponAdmin/` |
| 中文名 | 团购 |
| 开发波次 | W3 |
| 页面数 | **4** |
| 端点数（去重） | **8** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addGroupon` | `/addGroupon` | `views/grouponAdmin/addGroupon.html` | `addGrouponCtrl` | 8 |
| 2 | `grouponDetail` | `/grouponDetail?grouponProductId` | `views/grouponAdmin/grouponDetail.html` | `grouponDetailCtrl` | 0 |
| 3 | `grouponList` | `/grouponList` | `views/grouponAdmin/grouponList.html` | `grouponListCtrl` | 0 |
| 4 | `grouponOrder` | `/grouponOrder?grouponProductId` | `views/grouponAdmin/grouponOrder.html` | `grouponOrderCtrl` | 0 |

## §2 端点清单（去重 8 个）

- `POST /admin/createGrouponProduct.json`
- `POST /admin/deleteGrouponProduct.json`
- `POST /admin/getAdminInfo.json`
- `POST /admin/getGrouponProductVo.json`
- `POST /admin/invalidGrouponProduct.json`
- `POST /admin/selectGrouponOrderVoList.json`
- `POST /admin/selectGrouponProductVoList.json`
- `POST /admin/updateAdminInfo.json`

## §3 逐页字段规格

### 23.1 `addGroupon`

- **URL**：`/addGroupon`
- **模板**：`views/grouponAdmin/addGroupon.html`
- **控制器**：`addGrouponCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createGrouponProduct` | `POST /admin/createGrouponProduct.json` |
| `deleteGrouponProduct` | `POST /admin/deleteGrouponProduct.json` |
| `getAdminInfo` | `POST /admin/getAdminInfo.json` |
| `getGrouponProductVo` | `POST /admin/getGrouponProductVo.json` |
| `invalidGrouponProduct` | `POST /admin/invalidGrouponProduct.json` |
| `selectGrouponOrderVoList` | `POST /admin/selectGrouponOrderVoList.json` |
| `selectGrouponProductVoList` | `POST /admin/selectGrouponProductVoList.json` |
| `updateAdminInfo` | `POST /admin/updateAdminInfo.json` |

**必填项**

| 标签 |
|---|
| * 商品名称： * 图片： 点击上传 |
| * 规格： 无规格 一种规格 两种规格 * |
| * 请选择 {{modelName.name}} SKU码： |
| * 单位名称： |
| * 市场价： |
| * 成团价格： |
| * 成团人数： |
| * 活动名称： |
| * 开始时间： * 结束时间： * 模拟成团： 开启模拟成团 |
| * 活动限购： 不限 限购 次 / 人 * 提货方式： 到店自提 |

**表单标签**

| 标签 |
|---|
| * 商品名称： * 图片： 点击上传 |
| 描述： |
| * 规格： 无规格 一种规格 两种规格 * |
| * 请选择 {{modelName.name}} SKU码： |
| * 单位名称： |
| * 市场价： |
| * 成团价格： |
| * 成团人数： |
| * 活动名称： |
| * 开始时间： * 结束时间： * 模拟成团： 开启模拟成团 |
| * 活动限购： 不限 限购 次 / 人 * 提货方式： 到店自提 |
| 快递收费 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.productName` |
| `obj.description` |
| `obj.modelType` |
| `obj.model1Name` |
| `obj.model1` |
| `obj.model2Name` |
| `obj.model2` |
| `obj.skuCode` |
| `obj.unitName` |
| `marketPrice` |
| `seckillPrice` |
| `obj.minimumGrouponMembers` |
| `obj.promotionName` |
| `obj.startTime` |
| `startTime` |
| `obj.endTime` |
| `endTime` |
| `obj.simulateGroupon` |
| `maximumPurchaseFrequency` |
| `obj.maximumPurchaseFrequency` |
| `obj.expressType` |
| `obj.address` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.modelPicture` |
| `modelName.id` |
| `modelName.name` |
| `unitName.id` |
| `unitName.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideModal()` |
| `chooseImg()` |
| `showModal(item,$event)` |
| `changeType(obj.modelType)` |
| `open1()` |
| `open2()` |
| `set()` |
| `addSecKill()` |

**跳转到**：`grouponList`

### 23.2 `grouponDetail`

- **URL**：`/grouponDetail?grouponProductId`
- **模板**：`views/grouponAdmin/grouponDetail.html`
- **控制器**：`grouponDetailCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 商品名称： |
| * 图片： |
| * 规格： |
| * |
| * SKU码： |
| * 单位名称： |
| * 市场价： |
| * 成团价格： |
| * 成团人数： |
| * 活动名称： |
| * 开始时间： |
| * 结束时间： |
| * 模拟成团： |
| * 活动限购： |
| * 提货方式： |
| * 提货地址： |

**表单标签**

| 标签 |
|---|
| * 商品名称： |
| * 图片： |
| 描述： |
| * 规格： |
| 无规格 |
| 一种规格 |
| 两种规格 |
| * |
| * SKU码： |
| * 单位名称： |
| * 市场价： |
| * 成团价格： |
| * 成团人数： |
| * 活动名称： |
| {{obj.promotionName}} |
| * 开始时间： |
| * 结束时间： |
| * 模拟成团： |
| 开启模拟成团 |
| * 活动限购： |
| * 提货方式： |
| * 提货地址： |
| {{unActiveFactory.result.object.promotion.address}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.modelType` |
| `obj.model1Name` |
| `obj.model1` |
| `obj.model2Name` |
| `obj.model2` |
| `obj.simulateGroupon` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.productName` |
| `obj.modelPicture` |
| `obj.description` |
| `modelName.id` |
| `modelName.name` |
| `obj.skuCode` |
| `obj.unitName` |
| `obj.marketPrice` |
| `obj.seckillPrice` |
| `obj.minimumGrouponMembers` |
| `obj.promotionName` |
| `obj.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `obj.endTime` |
| `obj.maximumPurchaseFrequency` |
| `unActiveFactory.result.object.promotion.expressType` |
| `expressType` |
| `unActiveFactory.result.object.promotion.address` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideModal()` |
| `changeType(obj.modelType)` |

**跳转到**：`grouponList`

### 23.3 `grouponList`

- **URL**：`/grouponList`
- **模板**：`views/grouponAdmin/grouponList.html`
- **控制器**：`grouponListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 活动名称 |
| 2 | 活动时间 |
| 3 | 状态 |
| 4 | 市场价/团购价 |
| 5 | 访客数 |
| 6 | 开团数 |
| 7 | 成团数 |
| 8 | 参团订单数 |
| 9 | 成团订单数 数据指标说明 访客数：浏览过该拼团的客户数 开团数：该活动成功支付开团的总团数 成团数：该活动拼团成功的总团数 参团订单数：该活动成功支付的订单总数 成团订单数：该活动成团（即订单状态为已成团）的订单总数 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `checkCountFactory.object.examiningCount` |
| `checkCountFactory.object.examinedCount` |
| `item.grouponProduct.modelPicture` |
| `modelPicture` |
| `item.promotion.title` |
| `item.expiredStatus` |
| `grouponStatus` |
| `item.grouponProduct.marketPrice` |
| `item.grouponProduct.seckillPrice` |
| `item.grouponProduct.minimumGrouponMembers` |
| `item.grouponProduct.visitCustCount` |
| `item.grouponPromotionData.openGrouponCount` |
| `item.grouponPromotionData.compleleGrouponCount` |
| `item.grouponPromotionData.openGrouponOrderCount` |
| `item.grouponPromotionData.compleleGrouponOrderCount` |
| `item.promotionURL` |
| `item.promotion.promotionUrlQrcode` |
| `item.promotion.promotionUrl` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideCode()` |
| `searchTab(null)` |
| `searchTab(10)` |
| `searchTab(11)` |
| `searchTab(2)` |
| `showCode(item.promotion.promotionUrl,$event)` |
| `unActive(item.grouponProduct.id)` |
| `deleteSec(item.grouponProduct.id)` |

**跳转到**：`addGroupon`, `secKillProductAdmin`

### 23.4 `grouponOrder`

- **URL**：`/grouponOrder?grouponProductId`
- **模板**：`views/grouponAdmin/grouponOrder.html`
- **控制器**：`grouponOrderCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.groupon.grouponCode` |
| `item.groupon.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.leftTime` |
| `item.grouponProduct.minimumGrouponMembers` |
| `item.groupon.leftHeadCount` |
| `iten.customer.avatar` |
| `iten.customer.customerName` |
| `iten.customer.linkMobile` |
| `iten.customerOrder.orderCode` |
| `iten.customerOrder.payTime` |
| `iten.cashflow.totalPayment` |
