# 21｜模块 authAdmin 账户/充值/积分

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/authAdmin/` |
| 中文名 | 账户/充值/积分 |
| 开发波次 | W3 |
| 页面数 | **12** |
| 端点数（去重） | **10** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `aioIntroduce` | `/aioIntroduce` | `views/authAdmin/aioIntroduce.html` | `aioIntroduceCtrl` | 0 |
| 2 | `coinRuleIntroduce` | `/coinRuleIntroduce` | `views/authAdmin/coinRuleIntroduce.html` | `coinRuleIntroduceCtrl` | 0 |
| 3 | `myAccount` | `/myAccount` | `views/authAdmin/myAccount.html` | `myAccountCtrl` | 3 |
| 4 | `myAccountCoin` | `/myAccountCoin` | `views/authAdmin/myAccountCoin.html` | `myAccountCoinCtrl` | 1 |
| 5 | `myAccountCoinDetails` | `/myAccountCoinDetails` | `views/authAdmin/myAccountCoinDetails.html` | `myAccountCoinDetailsCtrl` | 2 |
| 6 | `myAccountDetails` | `/myAccountDetails?payChannel` | `views/authAdmin/myAccountDetails.html` | `myAccountDetailsCtrl` | 2 |
| 7 | `myAccountDetailsForScan` | `/myAccountDetailsForScan` | `views/authAdmin/myAccountDetailsForScan.html` | `myAccountDetailsForScanCtrl` | 1 |
| 8 | `myAccountHistory` | `/myAccountHistory` | `views/authAdmin/myAccountHistory.html` | `myAccountHistoryCtrl` | 1 |
| 9 | `myAccountOverviews` | `/myAccountOverviews` | `views/authAdmin/myAccountOverviews.html` | `myAccountOverviewsCtrl` | 1 |
| 10 | `wechatAuth` | `/wechatAuth` | `views/authAdmin/wechatAuth.html` | `wechatAuthCtrl` | 3 |
| 11 | `wechatAuthFailed` | `/wechatAuthFailed` | `views/authAdmin/wechatAuthFailed.html` | `wechatAuthFailedCtrl` | 0 |
| 12 | `wechatAuthSuccess` | `/wechatAuthSuccess` | `views/authAdmin/wechatAuthSuccess.html` | `wechatAuthSuccessCtrl` | 0 |

## §2 端点清单（去重 10 个）

- `POST /admin/changeWechatAccount.json`
- `POST /admin/getAuthPage.json`
- `POST /admin/getCompanyListOfMine.json`
- `POST /admin/selectCorpCoinEventLogList.json`
- `POST /admin/selectCorpCoinStateList.json`
- `POST /admin/selectCorpCoinTradeLogList.json`
- `POST /admin/selectMyCorpPaymentOrder.json`
- `POST /admin/stateCorpCoin.json`
- `POST /admin/stateScanPayMonthTrade.json`
- `POST /auth/authInfo.json`

## §3 逐页字段规格

### 21.1 `aioIntroduce`

- **URL**：`/aioIntroduce`
- **模板**：`views/authAdmin/aioIntroduce.html`
- **控制器**：`aioIntroduceCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `aio.name` |
| `aioList` |
| `aioIndex` |
| `title` |
| `img` |

**页面动作（ng-click）**

| 动作 |
|---|
| `changeAioIndex($index)` |

### 21.2 `coinRuleIntroduce`

- **URL**：`/coinRuleIntroduce`
- **模板**：`views/authAdmin/coinRuleIntroduce.html`
- **控制器**：`coinRuleIntroduceCtrl`
- **端点数**：0

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.name` |
| `item.settle` |
| `item.coins` |

**页面动作（ng-click）**

| 动作 |
|---|
| `lookDetails()` |

### 21.3 `myAccount`

- **URL**：`/myAccount`
- **模板**：`views/authAdmin/myAccount.html`
- **控制器**：`myAccountCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCorpCoinStateList` | `POST /admin/selectCorpCoinStateList.json` |
| `stateCorpCoin` | `POST /admin/stateCorpCoin.json` |
| `stateScanPayMonthTrade` | `POST /admin/stateScanPayMonthTrade.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corp.corporationName` |
| `maxEndTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.icon` |
| `item.value` |
| `hiddenDecimal` |
| `item.title` |
| `detail.description` |
| `detail.stateType` |
| `stateType` |
| `detail.addCoinCount` |
| `detail.gmtCreate` |

**页面动作（ng-click）**

| 动作 |
|---|
| `closeDue()` |
| `getCorp()` |
| `jump(item)` |
| `nearbySixMonthMore()` |
| `coinDetailsMore()` |

### 21.4 `myAccountCoin`

- **URL**：`/myAccountCoin`
- **模板**：`views/authAdmin/myAccountCoin.html`
- **控制器**：`myAccountCoinCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCorpCoinEventLogList` | `POST /admin/selectCorpCoinEventLogList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 日期 |
| 2 | 具体事件 |
| 3 | 事件名称 |
| 4 | 金币 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `accountList.total.totalCoinCount` |
| `item.eventTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.remark` |
| `item.addCoinCount` |

**跳转到**：`myAccount`, `myAccountCoinDetails`

### 21.5 `myAccountCoinDetails`

- **URL**：`/myAccountCoinDetails`
- **模板**：`views/authAdmin/myAccountCoinDetails.html`
- **控制器**：`myAccountCoinDetailsCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectCorpCoinTradeLogList` | `POST /admin/selectCorpCoinTradeLogList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 日期 |
| 2 | 所属门店 |
| 3 | 类型 |
| 4 | 渠道 |
| 5 | 金额 |
| 6 | 金币 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `accountList.total.totalMoney` |
| `accountList.total.totalCoinCount` |
| `item.corpCoinTradeLog.tradeTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.company.companyName` |
| `item.corpCoinTradeLog.tradeType` |
| `tradeType` |
| `item.corpCoinTradeLog.payChannel` |
| `payChannel` |

**跳转到**：`myAccount`, `myAccountCoin`

### 21.6 `myAccountDetails`

- **URL**：`/myAccountDetails?payChannel`
- **模板**：`views/authAdmin/myAccountDetails.html`
- **控制器**：`myAccountDetailsCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getCompanyListOfMine` | `POST /admin/getCompanyListOfMine.json` |
| `selectCorpCoinTradeLogList` | `POST /admin/selectCorpCoinTradeLogList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 日期 |
| 2 | 所属门店 |
| 3 | 类型 |
| 4 | 渠道 |
| 5 | 金额 |
| 6 | 金币 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `data.startTime` |
| `data.rightTimer` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `accountList.total.totalMoney` |
| `accountList.total.totalCoinCount` |
| `item.corpCoinTradeLog.tradeTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.company.companyName` |
| `item.corpCoinTradeLog.tradeType` |
| `tradeType` |
| `item.corpCoinTradeLog.payChannel` |
| `payChannel` |

**跳转到**：`myAccount`

### 21.7 `myAccountDetailsForScan`

- **URL**：`/myAccountDetailsForScan`
- **模板**：`views/authAdmin/myAccountDetailsForScan.html`
- **控制器**：`myAccountDetailsForScanCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `stateScanPayMonthTrade` | `POST /admin/stateScanPayMonthTrade.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 月份/类型 |
| 2 | 微信扫码赠送 |
| 3 | 支付宝扫码赠送 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item` |
| `tradeInfo.total.wechatTrade` |
| `tradeInfo.total.alipayTrade` |
| `Date` |
| `reviewtab` |
| `item.month` |
| `paddingZero` |
| `item.wechatTrade` |
| `item.alipayTrade` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setDate(item,$index)` |

**跳转到**：`myAccount`

### 21.8 `myAccountHistory`

- **URL**：`/myAccountHistory`
- **模板**：`views/authAdmin/myAccountHistory.html`
- **控制器**：`myAccountHistoryCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectMyCorpPaymentOrder` | `POST /admin/selectMyCorpPaymentOrder.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 时间 |
| 2 | 订单号 |
| 3 | 类型 |
| 4 | 说明 |
| 5 | 原价 |
| 6 | 优惠 |
| 7 | 实付金额 |
| 8 | 付款方式 |
| 9 | 到期时间 |
| 10 | 操作人 |
| 11 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.corpPaymentVo.corpPayment.payTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `item.corpPaymentVo.corpPayment.recordNo` |
| `item.corpPaymentVo.corpPayment.sceneType` |
| `stateType2` |
| `item.remark` |
| `item.corpPaymentVo.corpPayment.orderAmount` |
| `item.corpPaymentVo.corpPayment.discountAmount` |
| `item.corpPaymentVo.corpPayment.payAmount` |
| `filterPayment` |
| `item.corpPaymentVo.corpPaymentChannelList` |
| `item.endTime` |
| `item.createName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `lock.openLock(item)` |

**跳转到**：`myAccount`

### 21.9 `myAccountOverviews`

- **URL**：`/myAccountOverviews`
- **模板**：`views/authAdmin/myAccountOverviews.html`
- **控制器**：`myAccountOverviewsCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `selectCorpCoinStateList` | `POST /admin/selectCorpCoinStateList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 日期 |
| 2 | 事件名称 |
| 3 | 金额 |
| 4 | 金币 |
| 5 | 具体事件 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `accountList.total.totalMoney` |
| `accountList.total.totalCoinCount` |
| `item.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stateType` |
| `stateType` |
| `item.addMoney` |
| `item.addCoinCount` |
| `item.description` |

**跳转到**：`myAccount`

### 21.10 `wechatAuth`

- **URL**：`/wechatAuth`
- **模板**：`views/authAdmin/wechatAuth.html`
- **控制器**：`wechatAuthCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeWechatAccount` | `POST /admin/changeWechatAccount.json` |
| `getAuthPage` | `POST /admin/getAuthPage.json` |
| `authInfo` | `POST /auth/authInfo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 微信菜单 |
| 2 | 连接 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `state.stateName` |
| `state.stateUrl` |
| `codeHospital` |
| `corpInfo.employeeTitle` |
| `codeFindDoctor` |
| `codeMedicalRecord` |
| `codeMyCoupon` |
| `codeMyAppointment` |
| `codeMyremind` |
| `codeSaiChaDangAn` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideTab()` |
| `create()` |
| `getWXQYCode()` |
| `showQrcode($event,$index+1)` |
| `showQrcode($event,2)` |
| `showQrcode($event,3)` |
| `showQrcode($event,4)` |
| `showQrcode($event,5)` |
| `showQrcode($event,6)` |
| `showQrcode($event,7)` |
| `showQrcode($event,8)` |
| `move()` |

### 21.11 `wechatAuthFailed`

- **URL**：`/wechatAuthFailed`
- **模板**：`views/authAdmin/wechatAuthFailed.html`
- **控制器**：`wechatAuthFailedCtrl`
- **端点数**：0

### 21.12 `wechatAuthSuccess`

- **URL**：`/wechatAuthSuccess`
- **模板**：`views/authAdmin/wechatAuthSuccess.html`
- **控制器**：`wechatAuthSuccessCtrl`
- **端点数**：0
