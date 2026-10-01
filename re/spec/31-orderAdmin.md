# 31｜模块 orderAdmin 开单

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/orderAdmin/` |
| 中文名 | 开单 |
| 开发波次 | W5 |
| 页面数 | **4** |
| 端点数（去重） | **0** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addOrder` | `/addOrder` | `views/orderAdmin/addOrder.html` | `addOrderCtrl` | 0 |
| 2 | `dealRecord` | `/dealRecord?orderId&merchantId` | `views/orderAdmin/dealRecord.html` | `dealRecordCtrl` | 0 |
| 3 | `deliveryRecord` | `/deliveryRecord?orderId&merchantId` | `views/orderAdmin/deliveryRecord.html` | `deliveryRecordCtrl` | 0 |
| 4 | `modifyOrder` | `/modifyOrder?orderId&merchantId` | `views/orderAdmin/modifyOrder.html` | `modifyOrderCtrl` | 0 |

## §2 端点清单（去重 0 个）


## §3 逐页字段规格

### 31.1 `addOrder`

- **URL**：`/addOrder`
- **模板**：`views/orderAdmin/addOrder.html`
- **控制器**：`addOrderCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 31.2 `dealRecord`

- **URL**：`/dealRecord?orderId&merchantId`
- **模板**：`views/orderAdmin/dealRecord.html`
- **控制器**：`dealRecordCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 31.3 `deliveryRecord`

- **URL**：`/deliveryRecord?orderId&merchantId`
- **模板**：`views/orderAdmin/deliveryRecord.html`
- **控制器**：`deliveryRecordCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `

### 31.4 `modifyOrder`

- **URL**：`/modifyOrder?orderId&merchantId`
- **模板**：`views/orderAdmin/modifyOrder.html`
- **控制器**：`modifyOrderCtrl`
- **端点数**：0
- ⚠️ **模板抓取失败**：`fail:HTTP Error 404: `
