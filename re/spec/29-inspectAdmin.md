# 29｜模块 inspectAdmin 检查

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/inspectAdmin/` |
| 中文名 | 检查 |
| 开发波次 | W2 |
| 页面数 | **3** |
| 端点数（去重） | **0** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addInspect` | `/addInspect` | `views/inspectAdmin/addInspect.html` | `addInspectCtrl` | 0 |
| 2 | `inspectList` | `/inspectList` | `views/inspectAdmin/inspectList.html` | `InspectListCtrl` | 0 |
| 3 | `modifyInspect` | `/modifyInspect?id` | `views/inspectAdmin/modifyInspect.html` | `modifyInspectCtrl` | 0 |

## §2 端点清单（去重 0 个）


## §3 逐页字段规格

### 29.1 `addInspect`

- **URL**：`/addInspect`
- **模板**：`views/inspectAdmin/addInspect.html`
- **控制器**：`addInspectCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 项目名称 |

**表单标签**

| 标签 |
|---|
| * 项目名称 |
| 英文缩写 |
| 单位 |
| 定量 |
| 定性 |
| 可选项 |
| 单选 |
| 多选 |
| 特殊 |
| 临床意义 |
| 状态 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 可选项 单选 单选 多选 |
| 3 | 性别 |
| 4 | 年龄 |
| 5 | 参考值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.checkItemName` |
| `obj.checkItemEnglish` |
| `obj.checkItemUnitName` |
| `obj.checkItemType` |
| `choose` |
| `obj.singleValue` |
| `iten.rank1` |
| `iten.checkItemValue` |
| `obj.checkItemValueSample` |
| `obj.checkItemValueMin` |
| `obj.checkItemValueMax` |
| `except` |
| `iten.gender` |
| `iten.ageMin` |
| `iten.ageMax` |
| `iten.checkItemValueMin` |
| `iten.checkItemValueMax` |
| `obj.checkItemMeaning` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteValueItem($index)` |
| `addValueItem()` |
| `deleteItem($index)` |
| `addItem()` |
| `back()` |
| `addInspect()` |

### 29.2 `inspectList`

- **URL**：`/inspectList`
- **模板**：`views/inspectAdmin/inspectList.html`
- **控制器**：`InspectListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 项目名称 |
| 2 | 英文缩写 |
| 3 | 单位 |
| 4 | 数据类型 |
| 5 | 参考值 |
| 6 | 状态 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `item.medicalCheckItem.checkItemName` |
| `item.medicalCheckItem.checkItemEnglish` |
| `item.medicalCheckItem.checkItemUnitName` |
| `item.medicalCheckItem.checkItemValueSample` |
| `item.medicalCheckItem.status` |
| `supplierStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `searchTab(null)` |
| `searchTab(0)` |
| `searchTab(1)` |

**跳转到**：`addInspect`, `systemSetting.addInspect`

### 29.3 `modifyInspect`

- **URL**：`/modifyInspect?id`
- **模板**：`views/inspectAdmin/modifyInspect.html`
- **控制器**：`modifyInspectCtrl`
- **端点数**：0

**必填项**

| 标签 |
|---|
| * 项目名称 |

**表单标签**

| 标签 |
|---|
| * 项目名称 |
| 英文缩写 |
| 单位 |
| 定量 |
| 定性 |
| 可选项 |
| 单选 |
| 多选 |
| 特殊 |
| 临床意义 |
| 状态 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 可选项 单选 单选 多选 |
| 3 | 性别 |
| 4 | 年龄 |
| 5 | 参考值 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.checkItemName` |
| `obj.checkItemEnglish` |
| `obj.checkItemUnitName` |
| `obj.checkItemType` |
| `choose` |
| `obj.singleValue` |
| `iten.rank1` |
| `iten.checkItemValue` |
| `obj.checkItemValueSample` |
| `obj.checkItemValueMin` |
| `obj.checkItemValueMax` |
| `except` |
| `iten.gender` |
| `iten.ageMin` |
| `iten.ageMax` |
| `iten.checkItemValueMin` |
| `iten.checkItemValueMax` |
| `obj.checkItemMeaning` |
| `obj.status` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideBrandlist()` |
| `deleteValueItem($index)` |
| `addValueItem()` |
| `deleteItem($index)` |
| `addItem()` |
| `back()` |
| `updateInspect()` |
