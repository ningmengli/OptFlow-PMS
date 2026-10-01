# 25｜模块 hospitalRecharge 门店充值

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/hospitalRecharge/` |
| 中文名 | 门店充值 |
| 开发波次 | W3 |
| 页面数 | **1** |
| 端点数（去重） | **5** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `hospitalRecharge` | `/hospitalRecharge` | `views/hospitalRecharge/hospitalRecharge.html` | `hospitalRechargeCtrl` | 5 |

## §2 端点清单（去重 5 个）

- `POST /admin/commitAddHospitalBanlance.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getHospitalInfo.json`
- `POST /admin/getHospitalWallet.json`
- `POST /admin/initAddHospitalBanlance.json`

## §3 逐页字段规格

### 25.1 `hospitalRecharge`

- **URL**：`/hospitalRecharge`
- **模板**：`views/hospitalRecharge/hospitalRecharge.html`
- **控制器**：`hospitalRechargeCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitAddHospitalBanlance` | `POST /admin/commitAddHospitalBanlance.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getHospitalInfo` | `POST /admin/getHospitalInfo.json` |
| `getHospitalWallet` | `POST /admin/getHospitalWallet.json` |
| `initAddHospitalBanlance` | `POST /admin/initAddHospitalBanlance.json` |

**表单标签**

| 标签 |
|---|
| {{corpInfo. companyTitle}}名称： |
| 本金余额： |
| 赠送余额： |
| 充值金额： |
| 赠送金额： |
| 备注： |
| 选择支付方式： |
| 现金 |
| 银行卡 |
| 微信 |
| 支付宝 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `balance.addTrueMoney` |
| `balance.addGiftMoney` |
| `balance.remark` |
| `balance.payChannel` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `item.picture` |
| `item.companyName` |
| `item.address` |
| `item.phone` |
| `item.city` |
| `updateHospitalFactory.object.companyName` |
| `getWalletObejctFactory.object.trueBalance` |
| `getWalletObejctFactory.object.giftBalance` |

**页面动作（ng-click）**

| 动作 |
|---|
| `recharge(item.id)` |
| `updateMenber(item.customer.id,$event)` |
| `showMemberInfo(item.customer.id)` |
| `recharge(item.customer.id)` |
| `saveWallet()` |
| `hidePatient()` |
