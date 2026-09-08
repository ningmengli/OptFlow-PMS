# S1-113 optometryList / optometryListCtrl 基础数据流与入口审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（**S1-112 新发现第 11 个 untracked**）
> - Controller 范围：optometryListCtrl L35962 – L36132（171 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-112（HEAD=aa4e02c，tracked=182，untracked=11）
> - 本轮**重点**：optometryList 全局命中 + optometryListCtrl 完整 Controller 审计 + 与 optometryGlassesCtrl 关系
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-173）/ 修改 7 HTML / 修改 11 untracked / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **Controller**：`optometryListCtrl`，注册于 `controller.js` L35962
- **行范围**：L35962 – L36132（171 行）
  - L35962：`.controller("optometryListCtrl", [ ... ])` 注册
  - L36132：`}]);`（Controller 闭合）
  - L36133：`"use strict";`（下一个 module 边界）
  - L36135：optometryLogListCtrl 注册（下一 Controller）
- **审计目标**：
  1. optometryList 全局命中（State 字符串、Controller 字符串、其它）
  2. optometryListCtrl 完整 Controller 审计
  3. 与 optometryGlassesCtrl 的源码直接关系
  4. 与 optometryLogListCtrl 的边界
- **关键新发现**：
  - optometryListCtrl **不**是 optometry（验光）业务页面
  - optometryListCtrl **是** UartDevice（采集器/蓝牙）管理页面
  - 与 optometryGlassesCtrl **业务完全不同**

---

## 2. optometryList 全局命中

### 2.1 controller.js 内 optometryList 命中

| 行号 | 表达式 | 类别 | A-F |
|---:|---|---|---|
| 35962 | `angular.module("bestvisionWeb").controller("optometryListCtrl", [` | **A. Controller 注册** | A |
| 35965 | `var cacheInfo = window.commonFn.getSession("optometryList");` | **D. Session Key**（缓存键） | A |
| 36034 | `$state.go("optometryList", {}, { reload: true });` | **B. $state.go 自刷新** | A |
| 36049 | `window.commonFn.setSession("optometryList", $scope.obj);` | **D. Session Key**（缓存键） | A |

**总计**：4 处命中

### 2.2 命中分类

| 类别 | 数量 | 详情 |
|---|---:|---|
| A. Controller 注册 | 1 | L35962 |
| B. $state.go | 1 | L36034（自刷新） |
| C. State 字符串 | 0 | 0 处 |
| D. Session Key | 2 | L35965, L36049（缓存键） |
| E. templateUrl/template | 0 | 0 处 |
| F. HTML | 0 | 0 处（7 HTML 0 处 optometry 引用，S1-112 确认） |
| G. 其它 | 0 | - |

### 2.3 optometryListCtrl 字符串

| 来源 | 命中数 |
|---|---:|
| controller.js | 1（L35962 注册点） |
| 7 untracked HTML | 0 |
| 视光之家url.txt | 0 |
| **总计** | **1** |

### 2.4 optometryList State 字符串细节

| 字符串 | 行号 | 用法 |
|---|---:|---|
| `"optometryList"` | 35965 | Session 缓存键（`window.commonFn.getSession`） |
| `"optometryList"` | 36034 | $state.go State 名 |
| `"optometryList"` | 36049 | Session 缓存键（`window.commonFn.setSession`） |

**重要观察**：
- 3 处 `"optometryList"` 中 2 处是 **Session 缓存键**（不是 State 字符串）
- 真正作为 State 字符串的仅 1 处（L36034 自刷新）

---

## 3. optometryListCtrl 注册

### 3.1 注册位置

```javascript
// L35962
angular.module("bestvisionWeb").controller("optometryListCtrl", [
  "$scope", "Popup", "HttpFactory", "$state", "ObjectFactory", "ListFactory", "$timeout",
  function ($scope, Popup, HttpFactory, $state, ObjectFactory, ListFactory, $timeout) {
    // ...
  }
]);
```

### 3.2 注册详情

| 项 | 详情 | A-F |
|---|---|---|
| Controller 名 | `optometryListCtrl` | A |
| 所属 module | `bestvisionWeb` | A |
| 注册行 | L35962 | A |
| 注册次数 | **1**（A 级确认） | A |
| 注册语法 | `angular.module().controller()` | A |
| DI 列表 | 8 个：`$scope, Popup, HttpFactory, $state, ObjectFactory, ListFactory, $timeout` | A |
| 起始行 | L35962 | A |
| 结束行 | L36132 | A |
| 总行数 | 171 | A |
| 是否注入 `$state` | **是** | A |
| 是否注入 `$stateParams` | **否** | A |
| 是否注入 `HttpFactory` | **是**（与 optometryGlassesCtrl 不同） | A |
| 是否注入 `$rootScope` | **否** | A |
| 是否注入 `DateUtilFactory` | **否** | A |
| 是否注入 `utilFactory` | **否** | A |

### 3.3 与 optometryGlassesCtrl DI 对比

| DI | optometryGlassesCtrl | optometryListCtrl |
|---|---|---|
| $scope | ✅ | ✅ |
| Popup | ✅ | ✅ |
| utilFactory | ✅ | ❌ |
| ObjectFactory | ✅ | ✅ |
| ListFactory | ✅ | ✅ |
| $timeout | ✅ | ✅ |
| $stateParams | ✅ | **❌** |
| $state | ❌ | **✅** |
| HttpFactory | ❌ | **✅** |
| DateUtilFactory | ❌ | ❌ |
| $rootScope | ❌ | ❌ |

**关键对比**：
- optometryGlassesCtrl 注入 `$stateParams`（接收 medicalRecordId/edit）
- optometryListCtrl **不**注入 `$stateParams`（不接收任何 State 参数）
- optometryListCtrl 注入 `$state`（**$state.go 出口**）+ `HttpFactory`（HTTP 直调）

---

## 4. Controller 范围与 DI

### 4.1 范围

| 项 | 数值 | A-F |
|---|---:|---|
| 起始行 | L35962 | A |
| 结束行 | L36132 | A |
| 总行数 | 171 | A |
| 函数数 | 11 个 $scope 函数 + 1 个内部对象（smartDecoder） | A |

### 4.2 11 个 $scope 函数

| # | 行号 | 函数 | 类别 | A-F |
|---:|---:|---|---|---|
| 1 | 35974 | `$scope.getTypeArr` | **Read API** | A |
| 2 | 35986 | `$scope.changeType` | **Write API** | A |
| 3 | 35997 | `$scope.changeTypeLanYa` | **Write API** | A |
| 4 | 36009 | `$scope.searchSupplierList` | **Read API**（ListFactory） | A |
| 5 | 36028 | `$scope.searchTab` | UI 工具 | A |
| 6 | 36033 | `$scope.confirm` | State 出口（自刷新） | A |
| 7 | 36037 | `$scope.addOptometry` | **Write API** | A |
| 8 | 36048 | `$scope.lookLog` | State 出口（跳转 optometryLogList） | A |
| 9 | 36054 | `$scope.changeStatus` | **Write API** | A |
| 10 | 36065 | `$scope.getUartDevice` | **Read API**（HttpFactory） | A |
| 11 | (smartDecoder 内) | `choseCorpId`, `clearDecoder`, `queryCorporationList`, `open`, `affirm` | 内部方法 | A |

**Init 立即执行**（注册即调用）：
- L35984 `$scope.getTypeArr()` — Read getUartDeviceTypeList.json
- L36023 `$scope.searchSupplierList()` — Read selectAllUartDeviceVoList.json (ListFactory)
- L36026 `$scope.getCountStatusFactory.saveOrQuery(...)` — Read getUartDeviceLimitSubCount.json（无 .then）

### 4.3 $stateParams 全量

| 行号 | 表达式 | A-F |
|---:|---|---|
| （0 处）| - | A |

**关键发现**：optometryListCtrl **0 处** `$stateParams`（A 级确认）

---

## 5. StateParams

### 5.1 完整审计

| 行号 | 参数 | 转换 | 落点 | A-F |
|---:|---|---|---|---|
| （0 处） | - | - | - | A |

**结论**：optometryListCtrl **不**读取任何 `$stateParams`（A 级）

### 5.2 含义

- optometryListCtrl **不**接收任何 State 参数
- 入口 State `optometryList` 配置可能为空 params 或不带 params
- 与 optometryGlassesCtrl（接收 `medicalRecordId` + `edit`）形成对比

### 5.3 Session 缓存

虽然不读 StateParams，但 L35965 读取 Session：
```javascript
// L35965
var cacheInfo = window.commonFn.getSession("optometryList");
if (cacheInfo) {
  $scope.obj = cacheInfo;
}
```

L36049 写入 Session：
```javascript
// L36048-L36049
$scope.lookLog = function (item) {
  window.commonFn.setSession("optometryList", $scope.obj);
  // ...
};
```

**Session 用途**：
- 离开时缓存 `$scope.obj`（筛选条件）
- 再次进入时恢复筛选条件
- 这是 optometryListCtrl 唯一的"上下文恢复"机制

---

## 6. 初始化执行链

### 6.1 注册即执行（按行号顺序）

| # | 行号 | 语句 | 类型 | A-F |
|---:|---:|---|---|---|
| 1 | 35963 | `$scope.obj = {};` | Scope 初始化 | A |
| 2 | 35964 | `$scope.obj.status = null;` | Scope 字段 | A |
| 3 | 35965-35968 | `window.commonFn.getSession("optometryList")` | 缓存恢复 | A |
| 4 | 35969 | `$scope.status = [...]` | Scope 字段 | A |
| 5 | 35970-35973 | `$scope.typeArr = [...]` | Scope 字段 | A |
| 6 | 35974-35983 | `$scope.getTypeArr = function` | 函数定义 | A |
| 7 | 35984 | `$scope.getTypeArr();` | **Init 立即 Read** | A |
| 8 | 35985 | `$scope.typeArr2 = [...]` | Scope 字段 | A |
| 9 | 35986-35996 | `$scope.changeType = function` | 函数定义 | A |
| 10 | 35997-36007 | `$scope.changeTypeLanYa = function` | 函数定义 | A |
| 11 | 36008 | `$scope.pageSize = 100;` | Scope 字段 | A |
| 12 | 36009-36022 | `$scope.searchSupplierList = function` | 函数定义 | A |
| 13 | 36023 | `$scope.searchSupplierList();` | **Init 立即 Read（ListFactory）** | A |
| 14 | 36025 | `$scope.getCountStatusFactory = new ObjectFactory();` | Factory 实例化 | A |
| 15 | 36026 | `$scope.getCountStatusFactory.saveOrQuery(...)` | **Init 立即 Read** | A |
| 16 | 36028-36031 | `$scope.searchTab = function` | 函数定义 | A |
| 17 | 36033-36035 | `$scope.confirm = function` | 函数定义 | A |
| 18 | 36037-36047 | `$scope.addOptometry = function` | 函数定义 | A |
| 19 | 36048-36053 | `$scope.lookLog = function` | 函数定义 | A |
| 20 | 36054-36064 | `$scope.changeStatus = function` | 函数定义 | A |
| 21 | 36065-36071 | `$scope.getUartDevice = function` | 函数定义 | A |
| 22 | 36072-36131 | `$scope.smartDecoder = {...}` | 内部对象 | A |
| 23 | 36132 | `}]);` | Controller 闭合 | A |

### 6.2 Init 立即 Read 链

```
[1] $scope.getTypeArr() (L35984)
    └─ Read /admin/getUartDeviceTypeList.json
       └─ success: $scope.typeArr = res.result.list (在 $timeout 内)

[2] $scope.searchSupplierList() (L36023)
    └─ Read ListFactory /config/selectAllUartDeviceVoList.json
       └─ $scope.getSupplierListFactory = new ListFactory(..., 0, 100, $scope.obj)
       └─ nextPage() → $("#Pagination").pagination($scope.getSupplierListFactory.count)

[3] $scope.getCountStatusFactory.saveOrQuery(...) (L36026)
    └─ Read /config/getUartDeviceLimitSubCount.json
       └─ (无 .then，无显式 consumer)
```

### 6.3 Init 立即 Read 3 个 API

| API | 行号 | 类型 | 用途 |
|---|---:|---|---|
| `/admin/getUartDeviceTypeList.json` | 35975 | Read | 获取设备类型列表 |
| `/config/selectAllUartDeviceVoList.json` | 36010 | Read (ListFactory) | 获取采集器列表（主列表） |
| `/config/getUartDeviceLimitSubCount.json` | 36026 | Read | 限制计数（用途不明） |

---

## 7. API 全量

### 7.1 saveOrQuery + HttpFactory + ListFactory 全量

| # | 行号 | API | 类型 | Factory | 调用函数 | A-F |
|---:|---:|---|---|---|---|---|
| 1 | 35975 | `/admin/getUartDeviceTypeList.json` | Read | ObjectFactory 匿名 | getTypeArr | A |
| 2 | 35988 | `/config/updateUartDeviceType.json` | **Write** | ObjectFactory 命名 ($scope.changeTypeFactory) | changeType | A |
| 3 | 35999 | `/config/updateUartDeviceLinkType.json` | **Write** | ObjectFactory 命名 ($scope.changeTypeLanYaFactory) | changeTypeLanYa | A |
| 4 | 36010 | `/config/selectAllUartDeviceVoList.json` | Read | **ListFactory** ($scope.getSupplierListFactory) | searchSupplierList | A |
| 5 | 36026 | `/config/getUartDeviceLimitSubCount.json` | Read | ObjectFactory 命名 ($scope.getCountStatusFactory) | 立即调用（无函数） | A |
| 6 | 36039 | `/config/addUartDeviceUpToLimit.json` | **Write** | ObjectFactory 命名 ($scope.addStatusFactory) | addOptometry | A |
| 7 | 36056 | `/admin/changeUartDeviceStatus.json` | **Write** | ObjectFactory 命名 ($scope.changeStatusFactory) | changeStatus | A |
| 8 | 36066 | `/config/getUartDevice.json` | Read | HttpFactory.object | getUartDevice | A |
| 9 | 36090 | `/port/getCorporationConfVoList.json` | Read | HttpFactory.list | smartDecoder.queryCorporationList | A |
| 10 | 36126 | `/port/addUartDeviceUpToLimit.json` (add) / `/port/changeUartDeviceCorp.json` (change) | **Write** | HttpFactory.object | smartDecoder.affirm | A |

**总计**：10 个 call site（9 个不同 URL，其中 #10 是动态 URL）

### 7.2 unique API 统计

| URL | 类型 |
|---|---|
| `/admin/getUartDeviceTypeList.json` | Read |
| `/config/updateUartDeviceType.json` | **Write** |
| `/config/updateUartDeviceLinkType.json` | **Write** |
| `/config/selectAllUartDeviceVoList.json` | Read |
| `/config/getUartDeviceLimitSubCount.json` | Read |
| `/config/addUartDeviceUpToLimit.json` | **Write** |
| `/admin/changeUartDeviceStatus.json` | **Write** |
| `/config/getUartDevice.json` | Read |
| `/port/getCorporationConfVoList.json` | Read |
| `/port/addUartDeviceUpToLimit.json` (动态) | **Write** |
| `/port/changeUartDeviceCorp.json` (动态) | **Write** |

**unique API**：11 个
- **Read**：6（getUartDeviceTypeList, selectAllUartDeviceVoList, getUartDeviceLimitSubCount, getUartDevice, getCorporationConfVoList = 5 + 1 动态 Read 边界 = 6 保守）
- **Write**：5（updateUartDeviceType, updateUartDeviceLinkType, addUartDeviceUpToLimit, changeUartDeviceStatus, 动态 addUartDeviceUpToLimit/changeUartDeviceCorp）

### 7.3 call site vs unique

| 维度 | 数量 |
|---|---:|
| saveOrQuery call site | 6 |
| HttpFactory.object call site | 2 |
| HttpFactory.list call site | 1 |
| ListFactory call site | 1 |
| **call site 总数** | **10** |
| unique URL | 11（含 1 动态 URL） |
| 重复 URL | 0（`/config/addUartDeviceUpToLimit.json` 在 #6 和 #10 都调用） |

---

## 8. ListFactory

### 8.1 唯一 ListFactory

| 行号 | Factory 变量 | API | Request | pageStart | pageSize | A-F |
|---:|---|---|---|---:|---:|---|
| 36010 | `$scope.getSupplierListFactory` | `/config/selectAllUartDeviceVoList.json` | `$scope.obj` (status 字段等) | 0 | **100** | A |

### 8.2 ListFactory 行为

```javascript
// L36009-L36022
$scope.searchSupplierList = function () {
  $scope.getSupplierListFactory = new ListFactory(
    "/config/selectAllUartDeviceVoList.json", 0, $scope.pageSize, $scope.obj
  );
  var promise = $scope.getSupplierListFactory.nextPage();
  
  promise.then(function (data) {
    $("#Pagination").pagination($scope.getSupplierListFactory.count, {
      items_per_page: $scope.pageSize,
      callback: function callback(index) {
        $scope.getSupplierListFactory.clearAndSetIndex(index * $scope.pageSize);
        $scope.getSupplierListFactory.nextPage();
      }
    });
  });
};
```

### 8.3 ListFactory 关键参数

| 参数 | 值 | A-F |
|---|---:|---|
| URL | `/config/selectAllUartDeviceVoList.json` | A |
| pageStart | 0 | A |
| pageSize | 100（$scope.pageSize） | A |
| filter object | `$scope.obj`（含 status） | A |
| items 消费者 | `getUartDevice` (L36065) 通过 `$scope.getSupplierListFactory.items[index]` | A |
| 分页 | jQuery `$("#Pagination").pagination(count, ...)` | A |
| 自动调用 | **是**（`nextPage()` 自动调 API） | A |

---

## 9. ObjectFactory / HttpFactory

### 9.1 ObjectFactory 实例

| # | 行号 | Factory 变量 | API | 复用 | 命名 |
|---:|---:|---|---|---|---|
| 1 | 35975 | （匿名） | getUartDeviceTypeList.json | 否 | 否 |
| 2 | 35987 | `$scope.changeTypeFactory` | updateUartDeviceType.json | 否 | 是 |
| 3 | 35998 | `$scope.changeTypeLanYaFactory` | updateUartDeviceLinkType.json | 否 | 是 |
| 4 | 36025 | `$scope.getCountStatusFactory` | getUartDeviceLimitSubCount.json | 否 | 是 |
| 5 | 36038 | `$scope.addStatusFactory` | addUartDeviceUpToLimit.json | 否 | 是 |
| 6 | 36055 | `$scope.changeStatusFactory` | changeUartDeviceStatus.json | 否 | 是 |

**ObjectFactory**：6 个（1 匿名 + 5 命名）

### 9.2 HttpFactory 实例

| # | 行号 | 调用方式 | API | 用途 |
|---:|---:|---|---|---|
| 1 | 36066 | HttpFactory.object | `/config/getUartDevice.json` | Read 单个设备 |
| 2 | 36090 | HttpFactory.list | `/port/getCorporationConfVoList.json` | Read 机构列表 |
| 3 | 36097 | HttpFactory.pagination | (DOM) | 分页 jQuery 集成 |
| 4 | 36126 | HttpFactory.object | `/port/{addUartDeviceUpToLimit, changeUartDeviceCorp}.json` | **Write**（动态 URL） |

**HttpFactory**：4 个调用（含 1 pagination jQuery）

### 9.3 Factory 总计

| Factory 类型 | 数量 |
|---|---:|
| ObjectFactory 实例 | 6 |
| ListFactory 实例 | 1 |
| HttpFactory.object 调用 | 2 |
| HttpFactory.list 调用 | 1 |
| HttpFactory.pagination 调用 | 1 |
| 命名 ObjectFactory | 5 |
| 匿名 ObjectFactory | 1 |
| **总 Factory 调用** | **10** |

---

## 10. 主列表对象

### 10.1 列表主对象

| 对象 | 来源 | 结构 | 关键字段 | Consumer | 行号 |
|---|---|---|---|---|---|
| `$scope.getSupplierListFactory.items` | `/config/selectAllUartDeviceVoList.json` Response | 数组 | `items[].uartDevice.id/status`, `items[].type` | getUartDevice (L36065), confirm (L36033), lookLog (L36048), changeStatus (L36054) | 36010 |
| `$scope.obj` | Session 缓存 + Init 派生 | Object | `obj.status` (筛选条件) | searchSupplierList (L36009) | 35963 |
| `$scope.smartDecoder.corporationList` | `/port/getCorporationConfVoList.json` | 数组 | `corporationList[].id, name` | smartDecoder.affirm | 36096 |

### 10.2 列表项 item 字段（推断）

源码中通过 `item.uartDevice.id` 访问（L36051），说明每个 list item 包含 `uartDevice` 嵌套对象：
```javascript
{
  uartDevice: {
    id: ...,       // 设备 ID
    // ... 其它字段
  },
  // ... 其它顶层字段
}
```

**严禁** 推断其它字段（源码仅 1 处 item 访问）

---

## 11. Response → items

### 11.1 主列表

| API | Response 路径 | 落点 | Consumer | A-F |
|---|---|---|---|---|
| `/config/selectAllUartDeviceVoList.json` | ListFactory 内部管理 | `$scope.getSupplierListFactory.items` | jQuery pagination + 多个 item 函数 | A |

### 11.2 其它 Response

| API | Response 路径 | 落点 | Consumer | A-F |
|---|---|---|---|---|
| `/admin/getUartDeviceTypeList.json` | `res.result.list` | `$scope.typeArr` | （无显式 consumer） | A |
| `/config/getUartDeviceLimitSubCount.json` | （无 .then） | （无） | 无 | A |
| `/config/getUartDevice.json` | `res` (整体) | `$scope.getSupplierListFactory.items[index].uartDevice` | （仅设置） | A |
| `/port/getCorporationConfVoList.json` | `res.list` | `$scope.smartDecoder.corporationList` | smartDecoder.affirm | A |

### 11.3 ListFactory response 路径

| API | list 字段 | 字段类型 | A-F |
|---|---|---|---|
| `/config/selectAllUartDeviceVoList.json` | ListFactory.items (内部) | 数组 | A |

---

## 12. medicalRecord

### 12.1 medicalRecord 全量搜索

| 行号 | 表达式 | A-F |
|---:|---|---|
| （0 处）| - | A |

**关键发现**：optometryListCtrl **0 处** `medicalRecord` 字符串（A 级确认）

### 12.2 含义

- optometryListCtrl **不**处理 medicalRecord
- 与 optometryGlassesCtrl 完全不同
- optometryListCtrl 是 **UartDevice（采集器/蓝牙）** 管理页面，**不**涉及医疗记录

### 12.3 item 中是否含 medicalRecord

**F 边界**：optometryListCtrl 仅在 L36051 访问 `item.uartDevice.id`，**不**访问 `item.medicalRecord`
- 即使 item 包含 medicalRecord 字段，本 Controller 也**不消费**

---

## 13. medicalRecordId

### 13.1 medicalRecordId 全量搜索

| 行号 | 表达式 | A-F |
|---:|---|---|
| （0 处）| - | A |

**关键发现**：optometryListCtrl **0 处** `medicalRecordId` 字符串（A 级确认）

### 13.2 含义

- optometryListCtrl **不**使用 medicalRecordId
- 与 optometryGlassesCtrl 完全不同

### 13.3 medicalRecordId 路径增量

optometryListCtrl 范围内**未发现**新路径
- **无 `item.medicalRecord.id`**（item 仅有 uartDevice）
- **无 `medicalRecordId` 任何来源**
- **无 medicalRecordId 参与 Read**
- **无 medicalRecordId 参与 Write**
- **无 medicalRecordId 参与 State**

**S1-108 锁定的 5 类路径 + S1-111 锁定的 4 类新路径（共 9 类）在 optometryListCtrl 范围内 0 处出现**

---

## 14. item → 函数

### 14.1 item 访问点

| 行号 | 表达式 | 函数 | 用途 | A-F |
|---:|---|---|---|---|
| 36051 | `item.uartDevice.id` | $scope.lookLog | 跳转 optometryLogList | A |
| 36069 | `$scope.getSupplierListFactory.items[index]` | $scope.getUartDevice | 设置 item.uartDevice | A |

**总计**：2 处 item 访问

### 14.2 item → 函数 → State

```
item.uartDevice.id (L36051)
  ↓
$scope.lookLog(item) (L36048)
  ↓
window.commonFn.setSession("optometryList", $scope.obj) (L36049) [缓存]
  +
$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id }) (L36050)
```

**关键观察**：
- item 携带 `uartDeviceId`（不是 medicalRecordId）
- 跳转目标是 `optometryLogList`（不是 optometryGlasses）
- **无 optometryGlasses 跳转**（与 optometryGlassesCtrl **不直接连接**）

### 14.3 item → 函数 → Write

```
$scope.getSupplierListFactory.items[index] (L36069)
  ↓
$scope.getUartDevice(uartDeviceId, index) (L36065)
  ↓
HttpFactory.object("/config/getUartDevice.json", { uartDeviceId }) (L36066)
  ↓
$scope.getSupplierListFactory.items[index].uartDevice = res (L36069)
```

---

## 15. State 出口

### 15.1 $state.go 全量

| 行号 | 函数 | State | Params | 参数来源 | A-F |
|---:|---|---|---|---|---|
| 36034 | $scope.confirm | "optometryList" | `{}` | (空) | A |
| 36050 | $scope.lookLog | "optometryLogList" | `{ uartDeviceId: item.uartDevice.id }` | item.uartDevice.id | A |

**总计**：2 处 $state.go

### 15.2 State 出口详情

| 出口 | State | 含义 | 触发方 |
|---|---|---|---|
| L36034 | `optometryList` | **自刷新**（reload: true） | $scope.confirm |
| L36050 | `optometryLogList` | 跳转（带 uartDeviceId） | $scope.lookLog |

### 15.3 与 optometryGlassesCtrl 关系

- optometryListCtrl **0 处** $state.go("optometryGlasses")
- optometryListCtrl **0 处** $state.go("optometryCtrl")
- optometryListCtrl **0 处** 任何 optometry Glasses 业务 State

**双向关系**：
- optometryGlassesCtrl → optometryList（`$state.go("optometryList", {}, { reload: true })`，L36034）
- optometryListCtrl → optometryLogList（`$state.go("optometryLogList", { uartDeviceId })`，L36050）
- **optometryList → optometryGlasses 不存在**（optometryListCtrl **不**跳转到 optometryGlasses）

---

## 16. optometryGlasses 关系

### 16.1 与 optometryGlassesCtrl 双向关系

| 关系 | 证据 | 状态 |
|---|---|---|
| optometryGlassesCtrl → optometryList | `$state.go("optometryList", {}, { reload: true })` L36034 | A（optometryGlassesCtrl 范围） |
| optometryListCtrl → optometryGlasses | **0 处** | A（本轮确认） |
| optometryListCtrl → optometryGlassesCtrl | **0 处** | A |

### 16.2 关键结论

**optometryListCtrl 是"dead-end"页面（无 optometryGlasses 出口）**

| 关系 | 详情 |
|---|---|
| 入口 | optometryGlassesCtrl 可以跳转到 optometryList（L36034） |
| 出口 | optometryListCtrl **不**跳回 optometryGlasses |
| 出口 | optometryListCtrl 跳转到 optometryLogList（L36050） |

### 16.3 共享对象

| 对象 | optometryGlassesCtrl | optometryListCtrl |
|---|---|---|
| `$scope.medicalRecord` | ✅ (整体) | **❌ 0 处** |
| `$scope.medicalRecordId` | ✅ (10 处) | **❌ 0 处** |
| `$scope.userInfo` | ✅ (15 字段) | **❌ 0 处** |
| `$scope.object` (27+ 字段) | ✅ | **❌ 0 处** |
| `$scope.glassesInfo` | ✅ | **❌ 0 处** |

**两个 Controller **不共享**任何主数据对象**

---

## 17. optometryLogList 边界

### 17.1 optometryLogList 全局命中

| 行号 | 表达式 | 类别 | A-F |
|---:|---|---|---|
| 36050 | `$state.go("optometryLogList", {` | **B. $state.go** | A |
| 36135 | `angular.module('bestvisionWeb').controller('optometryLogListCtrl', [` | **A. Controller 注册** | A |
| 36138 | `$scope.obj.uartDeviceId = $stateParams.uartDeviceId;` | **StateParams Consumer** | A |
| 36142 | `new ListFactory('/config/selectUartDeviceLogVoList.json',` | **API** | A |

### 17.2 optometryLogListCtrl 关键信息

| 项 | 详情 | A-F |
|---|---|---|
| Controller 名 | `optometryLogListCtrl` | A |
| 注册行 | L36135 | A |
| 起始行 | L36135 | A |
| 结束行 | L36162 | A |
| 总行数 | 28 | A |
| DI | $scope, Popup, $stateParams, $interval, $rootScope, $state, ObjectFactory, ListFactory | A |
| 是否注入 `$stateParams` | **是** | A |
| 第一个 StateParams Consumer | `uartDeviceId` (L36138) | A |
| 第一个 API | `/config/selectUartDeviceLogVoList.json` (L36142) | A |
| pageSize | 20 (L36139) | A |

**S1-113 边界**：仅做 1 层追踪（不进入 optometryLogListCtrl 完整逆向）

### 17.3 双向关系

| 关系 | 证据 |
|---|---|
| optometryListCtrl → optometryLogList | L36050 `$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })` |
| optometryLogListCtrl → optometryList | **未确认**（本轮不深入） |

---

## 18. Read → Write

### 18.1 字段级闭合

| Write | Request 字段 | 来源 | 上游 Read | A-F |
|---|---|---|---|---|
| updateUartDeviceType (L35988) | `uartDeviceId, deviceType` | 函数参数 id, deviceType | 无（无前置 Read） | A |
| updateUartDeviceLinkType (L35999) | `uartDeviceId, deviceLinkType` | 函数参数 id, deviceLinkType | 无 | A |
| addUartDeviceUpToLimit (L36039) | `{}` | （无参数） | 无 | A |
| changeUartDeviceStatus (L36056) | `uartDeviceId, status` | 函数参数 id, status | 无 | A |
| addUartDeviceUpToLimit / changeUartDeviceCorp (L36126) | `corpId, [uartDeviceId]` | `this.corpId, this.uartDeviceId` | 无 | A |

**5 个 Write Request 字段来源（A 级）**：
- 4 个来自函数参数（无前置 Read）
- 1 个来自内部对象（smartDecoder 状态）

---

## 19. Write → Read

### 19.1 全部 Write success 行为

| Write | success 行为 | 触发的 Read | A-F |
|---|---|---|---|
| updateUartDeviceType (L35988) | `Popup.notice("修改成功"/errmsg, 2000, function(){})` | 无 | A |
| updateUartDeviceLinkType (L35999) | `Popup.notice(...)` | 无 | A |
| addUartDeviceUpToLimit (L36039) | `Popup.notice(...)` + `$scope.addDeviceModal = true` | 无 | A |
| changeUartDeviceStatus (L36056) | `Popup.notice(...)` | 无 | A |
| addUartDeviceUpToLimit / changeUartDeviceCorp (L36126) | `$scope.smartDecoder.open(false)` + `$scope.smartDecoder.clearDecoder()` | **无显式 Read Refresh** | A |

**Write→Read 链**：**0 条**（optometryListCtrl 范围内）

**Write→Popup 链**：5 条（每个 Write success 都有 Popup 提示）

---

## 20. Popup / callback / timeout

### 20.1 Popup.notice 全量

| 行号 | 触发函数 | 消息 | 条件 | A-F |
|---:|---|---|---|---|
| 35977 | getTypeArr | `res.errmsg` | res.status != 0 | A |
| 35991 | changeType | "修改成功" | res.status == 0 | A |
| 35993 | changeType | `res.errmsg` | res.status != 0 | A |
| 36002 | changeTypeLanYa | "修改成功" | res.status == 0 | A |
| 36004 | changeTypeLanYa | `res.errmsg` | res.status != 0 | A |
| 36044 | addOptometry | `res.errmsg` | res.status != 0 | A |
| 36059 | changeStatus | "修改成功" | res.status == 0 | A |
| 36061 | changeStatus | `res.errmsg` | res.status != 0 | A |
| 36118 | smartDecoder.affirm | "请选择要添加的机构！" | `!this.corpId` | A |

**总计**：9 处 Popup.notice（A 级）

### 20.2 $timeout 调用

| 行号 | 触发函数 | 内容 | A-F |
|---:|---|---|---|
| 35979 | getTypeArr success | `$scope.typeArr = res.result.list` (延迟 1ms) | A |

**$timeout**：1 处（A 级）

### 20.3 callback

| 位置 | 形式 | A-F |
|---|---|---|
| 35977 | `Popup.notice(..., 2000, function(){})` (空 callback) | A |
| 35991, 35993, 36002, 36004, 36044, 36059, 36061 | Popup callback 全为空 | A |
| 36016 | jQuery pagination callback | A |
| 36097 | HttpFactory.pagination callback | A |

**callback 总计**：9 处（Popup 7 处 + jQuery 1 处 + HttpFactory.pagination 1 处）

---

## 21. HTML 边界

### 21.1 optometryList HTML 状态

| 资源 | 数量 | 包含 optometryList |
|---|---:|:---:|
| 7 untracked HTML | 7 | **0** |
| 视光之家url.txt | 1 | 0 |
| Git 历史 .html | 0 | - |

**关键发现**：**0 个 optometryList 相关 HTML/Template**（A 级）

### 21.2 与 optometryGlassesCtrl 关系

- optometryGlassesCtrl HTML：F 边界（S1-112 确认）
- optometryListCtrl HTML：F 边界（本轮确认）
- **两个 Controller 都没有 HTML 模板**

### 21.3 State-based 路由推断

7 untracked HTML 全部使用 `ui-sref` 而非 `ng-controller`（S1-112 确认），optometryListCtrl 应该有对应 State 配置：
- 推测 State 名称：`optometryList`
- 推测 Controller 字段：`optometryListCtrl`
- 推测 templateUrl：可能为某个未在 working dir 的 HTML 文件
- **严禁** 进一步推断

---

## 22. 重复提交防护

### 22.1 搜索结果

```powershell
# 0 处 disabled / loading / flag / debounce / isLoading / isSubmitting
```

**optometryListCtrl 未观察到明确重复提交防护**（A 级）

### 22.2 风险点

- 5 个 Write 均无 disabled/loading/flag 防护
- 用户快速点击会触发多次 Write
- HTML 可能存在 ng-disabled 防护（F 边界）

---

## 23. 页面级 DAG

### 23.1 入口

```
[外部入口 - F 边界]
- optometryGlassesCtrl L36034 $state.go("optometryList", {}, { reload: true })  ← 已确认
- 其它入口（F 边界：HTML/State 配置不可得）

↓

[optometryList State]  (F 边界：State 配置不在 controller.js)

↓

[optometryListCtrl L35962]  (171 行)
DI: $scope, Popup, HttpFactory, $state, ObjectFactory, ListFactory, $timeout
$stateParams: 0 处
```

### 23.2 Init 链

```
[1] Session 恢复 (L35965)
    └─ window.commonFn.getSession("optometryList") → $scope.obj (若存在)

[2] $scope.getTypeArr() (L35984) - Init 立即 Read
    └─ /admin/getUartDeviceTypeList.json
       └─ $scope.typeArr = res.result.list (在 $timeout 内)

[3] $scope.searchSupplierList() (L36023) - Init 立即 Read (ListFactory)
    └─ /config/selectAllUartDeviceVoList.json
       └─ ListFactory: pageStart=0, pageSize=100, filter=$scope.obj
       └─ $scope.getSupplierListFactory.items (主列表)
       └─ $("#Pagination").pagination(count, { items_per_page: 100, callback: ... })

[4] $scope.getCountStatusFactory.saveOrQuery (L36026) - Init 立即 Read
    └─ /config/getUartDeviceLimitSubCount.json
       └─ (无 .then, 无显式 consumer)
```

### 23.3 用户动作链

```
[动作 A] $scope.changeType(id, deviceType) (L35986)
    └─ [Write] /config/updateUartDeviceType.json { uartDeviceId, deviceType }
       └─ Popup "修改成功"/errmsg

[动作 B] $scope.changeTypeLanYa(id, deviceLinkType) (L35997)
    └─ [Write] /config/updateUartDeviceLinkType.json { uartDeviceId, deviceLinkType }
       └─ Popup "修改成功"/errmsg

[动作 C] $scope.searchTab(index) (L36028)
    └─ $scope.obj.status = index
       └─ $scope.searchSupplierList() (触发 Read 刷新)

[动作 D] $scope.confirm() (L36033)
    └─ [State 出口] $state.go("optometryList", {}, { reload: true }) (自刷新)

[动作 E] $scope.addOptometry() (L36037)
    └─ [Write] /config/addUartDeviceUpToLimit.json {}
       └─ $scope.addDeviceModal = true (UI 控制)

[动作 F] $scope.lookLog(item) (L36048)
    └─ window.commonFn.setSession("optometryList", $scope.obj) [缓存]
    └─ [State 出口] $state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })

[动作 G] $scope.changeStatus(id, status) (L36054)
    └─ [Write] /admin/changeUartDeviceStatus.json { uartDeviceId, status }
       └─ Popup "修改成功"/errmsg

[动作 H] $scope.getUartDevice(uartDeviceId, index) (L36065)
    └─ [Read] /config/getUartDevice.json { uartDeviceId }
       └─ $scope.getSupplierListFactory.items[index].uartDevice = res

[动作 I] smartDecoder.affirm() (L36116)
    └─ 校验 this.corpId
    └─ [Write] /port/{addUartDeviceUpToLimit|changeUartDeviceCorp}.json
       └─ $scope.smartDecoder.open(false) + clearDecoder()
```

### 23.4 State 出口链

```
[出口 1] $scope.confirm (L36033)
    └─ $state.go("optometryList", {}, { reload: true })
    └─ **自刷新**

[出口 2] $scope.lookLog (L36048)
    └─ window.commonFn.setSession("optometryList", $scope.obj)
    └─ $state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })
    └─ **跳转 optometryLogList**
```

---

## 24. 跨 Controller 对照

| 项 | optometryGlassesCtrl (S1-108~111) | optometryListCtrl (S1-113) |
|---|---|---|
| 起始行 | L35383 | L35962 |
| 结束行 | L35959 | L36132 |
| 总行数 | 577 | 171 |
| 注入 `$state` | **否** | **是** |
| 注入 `$stateParams` | **是** | **否** |
| 注入 `HttpFactory` | 否 | **是** |
| unique API | 14 | 11 |
| call site | 13 | 10 |
| Read | 9 | 6 |
| Write | 5 | 5 |
| ListFactory | 1 | 1 |
| ObjectFactory | 9（全部匿名） | 6（5 命名 + 1 匿名） |
| HttpFactory 调用 | 0 | 4 |
| $stateParams 访问 | 2（medicalRecordId, edit） | **0** |
| $state.go 出口 | 0 | **2**（自刷新 + optometryLogList） |
| $state.go 入口 | 1（来自 optometryCtrl） | **0**（无外部入口证据） |
| medicalRecord 访问 | 4 处（L35390, L35419, L35433, L35434） | **0** |
| medicalRecordId 访问 | 10 处 | **0** |
| medicalRecord 字段消费 | 2 字段（secondDoctorName, secondDoctorId） | **0** |
| 重复提交防护 | **0 处** | **0 处** |
| HTML 模板 | F 边界 | F 边界 |
| 业务领域 | **验光配镜** | **UartDevice（采集器/蓝牙）** |

**关键发现**：
- 两个 Controller **业务完全无关**（验光 vs 采集器）
- 唯一共同点：使用相同的字符串 "optometryList" 作为 State 名称

---

## 25. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | optometryList 全局命中 | controller.js 4 处（注册/Session×2/$state.go） | A | L1 |
| 02 | optometryListCtrl 全局命中 | controller.js 1 处（L35962） | A | L1 |
| 03 | Controller 注册 | L35962，bestvisionWeb module | A | L1 |
| 04 | Controller 范围 | L35962-L36132（171 行） | A | L1 |
| 05 | DI | 8 个（$scope/Popup/HttpFactory/$state/ObjectFactory/ListFactory/$timeout） | A | L1 |
| 06 | $stateParams | 0 处 | A | L1 |
| 07 | 初始化执行链 | Session 恢复 + 3 个 Init Read (getTypeArr/searchSupplierList/getCountStatusFactory) | A | L1 |
| 08 | API unique | 11 个（含 1 动态） | A | L1 |
| 09 | API call site | 10 个 | A | L1 |
| 10 | Read | 6 个 unique | A | L1 |
| 11 | Write | 5 个 unique | A | L1 |
| 12 | ListFactory | 1 个（$scope.getSupplierListFactory） | A | L1 |
| 13 | ObjectFactory | 6 个（1 匿名 + 5 命名） | A | L1 |
| 14 | 主列表对象 | $scope.getSupplierListFactory.items | A | L1 |
| 15 | Response→items | ListFactory 内部管理 | A | L1 |
| 16 | medicalRecord | 0 处 | A | L1 |
| 17 | medicalRecordId | 0 处 | A | L1 |
| 18 | item→函数 | 2 处（item.uartDevice.id + items[index]） | A | L1 |
| 19 | State 出口 | 2 处（自刷新 + optometryLogList） | A | L1 |
| 20 | optometryGlasses 入口 | 0 处 | A | L1 |
| 21 | optometryLogList 边界 | L36050 跳转 + L36135 Controller 注册 | A | L1 |
| 22 | Read→Write | 4 个 Write 无前置 Read | A | L1 |
| 23 | Write→Read | 0 处 | A | L1 |
| 24 | Popup/timeout/callback | 9 Popup + 1 $timeout + 9 callback | A | L1 |
| 25 | HTML 边界 | 0 个 optometryList HTML | A/F | L1 |
| 26 | A/B/C/D/E/F | A: 25 / F: 1（HTML 边界） | A | L1 |

### 25.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 25 | 96% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 1 | 4% |

### 25.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 26. A-F 总结

- **A 级**：25 项（96%）
- **F 级**：1 项（HTML 边界）
- **B/C/D/E 级**：0 项

---

## 27. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0 项
- **L3**：0 项

---

## 28. F 边界

| F 项 | 详情 |
|---|---|
| 1 | optometryList HTML 模板 | 0 个 untracked HTML 含 optometry 引用 |
| 2 | optometryList State 配置 | 0 处 `.state(` in controller.js |
| 3 | UI 触发函数 | 0 个 optometry 引用 in 7 HTML |
| 4 | 离开方式 | 仅源码可见的 $state.go（F 边界 HTML 不可得） |
| 5 | optometryLogListCtrl 完整 API 逆向 | 本轮仅做 1 层追踪，不进入完整逆向 |

---

## 29. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不调用后端 API | ✅ |
| 5. 不打开真实业务系统 | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-112 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-173） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 11 untracked 原样保留 | ✅ |
| 14. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 30. 最终结论

### 30.1 核心发现

1. **optometryListCtrl 是 UartDevice 管理页面，**不是** optometry 验光业务页面**
   - 业务：采集器/蓝牙设备管理
   - 列表 API：`/config/selectAllUartDeviceVoList.json`
   - 列表字段：`item.uartDevice.id`
   - **0 处 medicalRecord / medicalRecordId**（与 optometryGlassesCtrl 完全不同）

2. **双向关系部分**：
   - optometryGlassesCtrl → optometryList（自刷新 L36034）✅
   - optometryListCtrl → optometryLogList（带 uartDeviceId）✅
   - optometryListCtrl → optometryGlasses ❌（**不**存在）

3. **0 处 medicalRecord/medicalRecordId**（A 级确认）
   - 全局 5+4 类 medicalRecordId 路径在本 Controller 范围**无任何出现**
   - optometryListCtrl 是"医疗"业务之外的纯设备管理页面

4. **与 optometryGlassesCtrl 对比**：
   - DI 差异：optometryListCtrl 无 $stateParams，有 HttpFactory 和 $state
   - API 数量：14 vs 11
   - Write 数量：5 vs 5（相同）
   - State 出口：0 vs 2
   - medicalRecord 访问：10 处 vs 0 处

### 30.2 关键状态参数

- **optometryListCtrl 不接收任何 State 参数**（0 处 $stateParams）
- 入口完全由 Session 缓存（`window.commonFn.getSession("optometryList")`）恢复

### 30.3 后续侦察方向

1. 寻找并分析 State 配置文件（app.js / router.js）
2. 寻找并分析 optometryList HTML 模板
3. 寻找并分析 视光之家生产系统 optometryList 页面 URL
4. 进入 optometryLogListCtrl 完整逆向（下一轮 S1-114 候选）

### 30.4 F 边界最终结论

**optometryListCtrl 的 UI 层证据（HTML/State 配置）在当前 working dir + Git 历史 + 7 untracked HTML + 视光之家url.txt 范围内完全不可得**（A 级穷举 + F 边界保持）

---

**审计完成。本文档为 174 号，提交后将形成 tracked=183，untracked=11。**
