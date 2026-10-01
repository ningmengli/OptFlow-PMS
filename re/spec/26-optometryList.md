# 26｜模块 optometryList 验光记录

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/optometryList/` |
| 中文名 | 验光记录 |
| 开发波次 | W7 |
| 页面数 | **2** |
| 端点数（去重） | **3** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `optometryList` | `/optometryList` | `views/optometryList/optometryList.html` | `optometryListCtrl` | 3 |
| 2 | `optometryLogList` | `/optometryLogList?uartDeviceId` | `views/optometryList/optometryLogList.html` | `optometryLogListCtrl` | 0 |

## §2 端点清单（去重 3 个）

- `POST /admin/changeUartDeviceStatus.json`
- `POST /admin/getOkOrderRecordVoList.json`
- `POST /admin/getUartDeviceTypeList.json`

## §3 逐页字段规格

### 26.1 `optometryList`

- **URL**：`/optometryList`
- **模板**：`views/optometryList/optometryList.html`
- **控制器**：`optometryListCtrl`
- **端点数**：3

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeUartDeviceStatus` | `POST /admin/changeUartDeviceStatus.json` |
| `getOkOrderRecordVoList` | `POST /admin/getOkOrderRecordVoList.json` |
| `getUartDeviceTypeList` | `POST /admin/getUartDeviceTypeList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | ID |
| 2 | 智能解码器编号(DeviceCode) |
| 3 | AppKey |
| 4 | AppSecret |
| 5 | 状态 |
| 6 | 用途 |
| 7 | 类型 |
| 8 | 所属机构ID |
| 9 | 所属机构 |
| 10 | 操作 |
| 11 | 选择 |
| 12 | 机构ID |
| 13 | 机构名称 |
| 14 | 现有采集器数量 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `item.uartDevice.deviceType` |
| `item.uartDevice.deviceLinkType` |
| `pageSize` |
| `smartDecoder.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getCountStatusFactory.result.object` |
| `getSupplierListFactory.count` |
| `item.uartDevice.id` |
| `item.uartDevice.deviceCode` |
| `item.openApp.appKey` |
| `item.openApp.appSecret` |
| `item.uartDevice.status` |
| `supplierStatus` |
| `item.corporation.id` |
| `item.corporation.corporationName` |
| `item.corporation.companyCountLimit` |
| `smartDecoder.affirmBtnName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `addOptometry()` |
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |
| `smartDecoder.open(true,` |
| `lookLog(item)` |
| `confirm()` |
| `addDeviceModal=false` |
| `smartDecoder.choseCorpId(item.corporation.id)` |
| `smartDecoder.affirm()` |
| `smartDecoder.open(false)` |

**下拉数据源（ng-options）**

```
x.id as x.deviceTypeName for x in typeArr
x.id as x.name for x in typeArr2
```

### 26.2 `optometryLogList`

- **URL**：`/optometryLogList?uartDeviceId`
- **模板**：`views/optometryList/optometryLogList.html`
- **控制器**：`optometryLogListCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 查看二进制 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 时间 |
| 2 | 用途 |
| 3 | 日志内容 |
| 4 | 状态 |
| 5 | 采集器 |
| 6 | 设备编号 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `hex` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `item.uartDeviceLog.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `item.uartDevice.deviceType` |
| `deviceType` |
| `item.uartDeviceLog.content` |
| `item.contentHexAscii` |
| `item.uartDeviceLog.splitStatus` |
| `splitStatus` |
| `item.uartDeviceLog.formatConverter` |
| `item.uartDevice.deviceCode` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStatus(null)` |
| `setStatus(0)` |
| `setStatus(1)` |

**跳转到**：`optometryList`
