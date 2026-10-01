# 30｜模块 newsAdmin 新闻公告

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/newsAdmin/` |
| 中文名 | 新闻公告 |
| 开发波次 | W3 |
| 页面数 | **3** |
| 端点数（去重） | **0** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addNew` | `/addNew` | `views/newsAdmin/addNew.html` | `addNewCtrl` | 0 |
| 2 | `modifyNew` | `/modifyNew?id` | `views/newsAdmin/modifyNew.html` | `modifyNewCtrl` | 0 |
| 3 | `newsList` | `/newsList` | `views/newsAdmin/newsList.html` | `newsListCtrl` | 0 |

## §2 端点清单（去重 0 个）


## §3 逐页字段规格

### 30.1 `addNew`

- **URL**：`/addNew`
- **模板**：`views/newsAdmin/addNew.html`
- **控制器**：`addNewCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 上传图片 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `rootid` |
| `obj.newsCategoryId` |
| `obj.newsTitle` |
| `obj.newsAuthor` |
| `editor` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.newsPicture` |

**页面动作（ng-click）**

| 动作 |
|---|
| `uploadimg()` |
| `addNew()` |

**下拉数据源（ng-options）**

```
x.root.id as x.root.categoryName for x in arr
x.root.id as x.root.categoryName for x in arrTree
```

### 30.2 `modifyNew`

- **URL**：`/modifyNew?id`
- **模板**：`views/newsAdmin/modifyNew.html`
- **控制器**：`modifyNewCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 上传图片 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.newsTitle` |
| `obj.newsAuthor` |
| `editor` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.newsPicture` |

**页面动作（ng-click）**

| 动作 |
|---|
| `uploadimg()` |
| `modifyNew()` |

### 30.3 `newsList`

- **URL**：`/newsList`
- **模板**：`views/newsAdmin/newsList.html`
- **控制器**：`newsListCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 新闻名称 |
| 2 | 新闻作者 |
| 3 | 新闻时间 |
| 4 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `rootid` |
| `categoryId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `x.root.id` |
| `x.root.categoryName` |
| `item.newsTitle` |
| `item.newsAuthor` |
| `item.gmtUpdate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteNew(item.id)` |

**跳转到**：`addNew`

**下拉数据源（ng-options）**

```
x.root.id as x.root.categoryName for x in arr
x.root.id as x.root.categoryName for x in arrTree
```
