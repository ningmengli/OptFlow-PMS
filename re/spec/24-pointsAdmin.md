# 24｜模块 pointsAdmin 积分

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/pointsAdmin/` |
| 中文名 | 积分 |
| 开发波次 | W3 |
| 页面数 | **1** |
| 端点数（去重） | **7** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `pointsList` | `/pointsList` | `views/pointsAdmin/pointsList.html` | `pointsListCtrl` | 7 |

## §2 端点清单（去重 7 个）

- `POST /admin/clearCustomerPoint.json`
- `POST /admin/commitCustomerPointLog.json`
- `POST /admin/getCorpPointRule.json`
- `POST /admin/getCustomerPoint.json`
- `POST /admin/selectCustomerPointLogVoList.json`
- `POST /admin/selectCustomerPointVoList.json`
- `POST /admin/selectTagList.json`

## §3 逐页字段规格

### 24.1 `pointsList`

- **URL**：`/pointsList`
- **模板**：`views/pointsAdmin/pointsList.html`
- **控制器**：`pointsListCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `clearCustomerPoint` | `POST /admin/clearCustomerPoint.json` |
| `commitCustomerPointLog` | `POST /admin/commitCustomerPointLog.json` |
| `getCorpPointRule` | `POST /admin/getCorpPointRule.json` |
| `getCustomerPoint` | `POST /admin/getCustomerPoint.json` |
| `selectCustomerPointLogVoList` | `POST /admin/selectCustomerPointLogVoList.json` |
| `selectCustomerPointVoList` | `POST /admin/selectCustomerPointVoList.json` |
| `selectTagList` | `POST /admin/selectTagList.json` |

**表单标签**

| 标签 |
|---|
| 只显示有积分用户 |
| 增加 减少 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 姓名 |
| 2 | 手机号 |
| 3 | 积分 |
| 4 | 操作 |
| 5 | 变动类型 |
| 6 | 时间 |
| 7 | 积分 |
| 8 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `params.hasPoint` |
| `credits.allStatus` |
| `item.isChose` |
| `params.length` |
| `pointType` |
| `point` |
| `obj.remark` |
| `params.keyword` |
| `params.pointFrom` |
| `params.pointTo` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPointObjectFactory.result.object.payMoney` |
| `getPointObjectFactory.result.object.toPoint` |
| `getPointObjectFactory.result.object.payPoint` |
| `getPointObjectFactory.result.object.toMoney` |
| `item.customer.customerName` |
| `item.customer.linkMobile` |
| `hidePhone` |
| `item.customerPoint.point` |
| `getPointFactory.result.object.point` |
| `getInitPointFactory.result.object.payPoint` |
| `getInitPointFactory.result.object.toMoney` |
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
| `item.customerPointLog.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `ClearCredits()` |
| `credits.choseAll()` |
| `credits.choseSingle()` |
| `showPoint(item.customer.id)` |
| `showRecord(item.customer.id)` |
| `hideCancelModal()` |
| `commitPoint()` |
