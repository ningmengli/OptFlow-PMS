# 28｜模块 purchase 采购

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/purchase/` |
| 中文名 | 采购 |
| 开发波次 | W5 |
| 页面数 | **1** |
| 端点数（去重） | **2** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `purchase` | `/purchase` | `views/purchase/purchase.html` | `purchaseCtrl` | 2 |

## §2 端点清单（去重 2 个）

- `POST /admin/getChildrenLinkAndCode.json`
- `POST /admin/getPurchaseRequestVoList.json`

## §3 逐页字段规格

### 28.1 `purchase`

- **URL**：`/purchase`
- **模板**：`views/purchase/purchase.html`
- **控制器**：`purchaseCtrl`
- **端点数**：2

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getPurchaseRequestVoList` | `POST /admin/getPurchaseRequestVoList.json` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `purchase.corpAdminHome.state` |
| `purchase.corpAdminHome.stateName` |
| `count` |
