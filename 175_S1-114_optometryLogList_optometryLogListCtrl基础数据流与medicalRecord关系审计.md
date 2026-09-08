# S1-114 optometryLogList / optometryLogListCtrl 基础数据流与 medicalRecord 关系审计

> **审计依据**：
> - 资源范围：`controller.js`（working dir 内唯一 JS 源）+ 7 untracked HTML + 视光之家url.txt（**gitignored**）
> - Controller 范围：optometryLogListCtrl L36135 – L36162（28 行）
> - 严格 A-F 证据等级
> - 上一轮基线：S1-113（HEAD=8d1b473，tracked=183，untracked=10，ignored=1）
> - 本轮**重点**：optometryLogList 入口 + optometryLogListCtrl 完整 Controller + medicalRecord 关系
> - 严禁：Write API 实际调用 / 修改 controller.js / 修改历史 MD（165-174）/ 修改 7 HTML / 修改 11 文件 / 修改 P0=54 / P1=8

---

## 1. 审计范围

- **Controller**：`optometryLogListCtrl`，注册于 `controller.js` L36135
- **行范围**：L36135 – L36162（28 行）— 本 Controller **极小**
  - L36135：`.controller('optometryLogListCtrl', [ ... ])` 注册
  - L36162：`}]);`（Controller 闭合）
  - L36163：`'use strict';`（下一个 module 边界）
  - L36165：orderManageCtrl 注册（下一 Controller）
- **审计目标**：
  1. optometryLogList 全局命中
  2. optometryLogListCtrl 完整 Controller 审计
  3. 入口参数 provenance（来自哪个 Controller）
  4. medicalRecord / medicalRecordId 关系
- **S1-114 关键纠偏**：
  - **S1-107/108/110/111 错误**：L36050 `$state.go("optometryLogList", ...)` 被报告为"在 optometryGlassesCtrl 范围内"
  - **S1-114 真实**：L36050 **在 optometryListCtrl 范围内**（L35962-L36132）

---

## 2. optometryLogList 全局命中

### 2.1 controller.js 内 optometryLogList 命中

| 行号 | 表达式 | 所在 Controller | 类别 | A-F |
|---:|---|---|---|---|
| 36050 | `$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id });` | **optometryListCtrl** (L35962-L36132) | **B. $state.go** | A |
| 36135 | `angular.module('bestvisionWeb').controller('optometryLogListCtrl', [` | optometryLogListCtrl | **A. Controller 注册** | A |

**总计**：2 处命中

### 2.2 命中分类

| 类别 | 数量 | 详情 |
|---|---:|---|
| A. Controller 注册 | 1 | L36135 |
| B. $state.go | 1 | L36050（在 optometryListCtrl 范围内） |
| C. State 字符串 | 0 | - |
| D. templateUrl/template | 0 | - |
| E. HTML | 0 | 7 untracked HTML 0 处 optometry 引用 |
| F. 注释 | 0 | - |
| G. 其它 | 0 | - |

### 2.3 optometryLogListCtrl 字符串

| 来源 | 命中数 |
|---|---:|
| controller.js | 1（L36135 注册点） |
| 7 untracked HTML | 0 |
| 视光之家url.txt | 0 |
| **总计** | **1** |

### 2.4 S1-107/108/110/111 错误纠正

| 报告 | 实际情况 |
|---|---|
| S1-107 报告：`optometryLogList` 入口在 optometryGlassesCtrl | **错误** — 实际在 optometryListCtrl (L36050) |
| S1-108 报告：L36050 在 optometryGlassesCtrl 范围内 | **错误** |
| S1-110 报告：optometryGlassesCtrl 与 optometryLogList 双向关系 | **错误** — L36050 在 optometryListCtrl |
| S1-111 报告：L36050 在 optometryListCtrl | **正确**（S1-111 已修正） |

**纠偏来源**：
- S1-111 全局 Controller 映射时已正确分类
- S1-114 本轮重新校验：L36050 在 optometryListCtrl (L35962-L36132) 范围内（A 级）
- **optometryGlassesCtrl 实际 0 处 $state.go("optometryLogList", ...)**（S1-107/108 报告错误）

---

## 3. optometryLogListCtrl 注册

### 3.1 注册位置

```javascript
// L36135
angular.module('bestvisionWeb').controller('optometryLogListCtrl', [
  '$scope', 'Popup', '$stateParams', '$interval', '$rootScope', '$state', 'ObjectFactory', 'ListFactory',
  function ($scope, Popup, $stateParams, $interval, $rootScope, $state, ObjectFactory, ListFactory) {
    // ...
  }
]);
```

### 3.2 注册详情

| 项 | 详情 | A-F |
|---|---|---|
| Controller 名 | `optometryLogListCtrl` | A |
| 所属 module | `bestvisionWeb` | A |
| 注册行 | L36135 | A |
| 注册次数 | **1**（A 级确认） | A |
| 注册语法 | `angular.module().controller()`（单引号风格，与 optometryListCtrl 一致） | A |
| DI 列表 | **9 个**：`$scope, Popup, $stateParams, $interval, $rootScope, $state, ObjectFactory, ListFactory` | A |
| 起始行 | L36135 | A |
| 结束行 | L36162 | A |
| 总行数 | **28**（最小 Controller） | A |
| 是否注入 `$state` | **是** | A |
| 是否注入 `$stateParams` | **是** | A |
| 是否注入 `$interval` | **是**（optometryGlassesCtrl 没有） | A |
| 是否注入 `$rootScope` | **是**（optometryGlassesCtrl 没有） | A |
| 是否注入 `HttpFactory` | **否** | A |
| 是否注入 `DateUtilFactory` | **否** | A |

### 3.3 与 optometryListCtrl / optometryGlassesCtrl DI 对比

| DI | optometryGlassesCtrl | optometryListCtrl | optometryLogListCtrl |
|---|---|---|---|
| $scope | ✅ | ✅ | ✅ |
| Popup | ✅ | ✅ | ✅ |
| ObjectFactory | ✅ | ✅ | ✅ |
| ListFactory | ✅ | ✅ | ✅ |
| $timeout | ✅ | ✅ | **❌** |
| utilFactory | ✅ | ❌ | ❌ |
| $stateParams | ✅ | ❌ | **✅** |
| $state | ❌ | ✅ | ✅ |
| HttpFactory | ❌ | ✅ | ❌ |
| $interval | ❌ | ❌ | **✅** |
| $rootScope | ❌ | ❌ | **✅** |
| DateUtilFactory | ❌ | ❌ | ❌ |

**关键差异**：
- optometryLogListCtrl 注入 `$stateParams`（接收 uartDeviceId）
- optometryLogListCtrl 注入 `$interval`（无显式使用）
- optometryLogListCtrl 注入 `$rootScope`（无显式使用）
- 0 处 `$interval` / `$rootScope` 在 Controller 范围内被实际使用（A 级）

---

## 4. Controller 范围与 DI

### 4.1 范围

| 项 | 数值 | A-F |
|---|---:|---|
| 起始行 | L36135 | A |
| 结束行 | L36162 | A |
| 总行数 | **28** | A |
| 函数数 | 2 个 $scope 函数 | A |

### 4.2 2 个 $scope 函数

| # | 行号 | 函数 | 类别 | A-F |
|---:|---:|---|---|---|
| 1 | 36141 | `$scope.searchSupplierList` | **Read API**（ListFactory） | A |
| 2 | 36158 | `$scope.setStatus` | UI 工具 | A |

**Init 立即执行**：
- L36156 `$scope.searchSupplierList()` — Read /config/selectUartDeviceLogVoList.json

### 4.3 $stateParams 全量

| 行号 | 表达式 | A-F |
|---:|---|---|
| 36138 | `$scope.obj.uartDeviceId = $stateParams.uartDeviceId;` | A |

**关键发现**：optometryLogListCtrl **1 处** `$stateParams` 访问（A 级确认）
- 参数名：`uartDeviceId`（不是 medicalRecordId）
- 首个 Consumer：L36138
- 写入：`$scope.obj.uartDeviceId`
- 后续：`$scope.obj` 作为 ListFactory Request 字段（L36142）

---

## 5. StateParams

### 5.1 完整审计

| 行号 | 参数 | 转换 | 落点 | 首个 Consumer | A-F |
|---:|---|---|---|---|---|
| 36138 | `uartDeviceId` | 直接赋值 | `$scope.obj.uartDeviceId` | L36142 (ListFactory Request) | A |

### 5.2 唯一 StateParams 字段

- `uartDeviceId`（**不是** medicalRecordId）
- 来源：optometryListCtrl L36050 `$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id })`

### 5.3 与 optometryGlassesCtrl 对照

| Controller | StateParams 字段 |
|---|---|
| optometryGlassesCtrl | `medicalRecordId`, `edit` |
| optometryLogListCtrl | `uartDeviceId` |
| optometryListCtrl | 0 处 |

**关键发现**：optometryLogListCtrl **不**接收 medicalRecordId（与 optometryGlassesCtrl **完全无关**）

---

## 6. optometryGlassesCtrl 入口

### 6.1 S1-107/108/110/111 报告 vs S1-114 实际

| 项 | S1-107/108/110 报告 | S1-111 报告 | S1-114 实际 |
|---|---|---|---|
| L36050 $state.go 所在 Controller | optometryGlassesCtrl | optometryListCtrl | **optometryListCtrl**（A 级） |
| 来源 | 误判 | 已修正 | A 级确认 |

### 6.2 S1-114 实际

**optometryGlassesCtrl → optometryLogList：0 处直接源码证据**

L36050 实际位于 optometryListCtrl（L35962-L36132）范围内：
```javascript
// L36048-L36053
$scope.lookLog = function (item) {
  window.commonFn.setSession("optometryList", $scope.obj);
  $state.go("optometryLogList", {
    uartDeviceId: item.uartDevice.id
  });
};
```

### 6.3 真实控制流

```
optometryListCtrl.lookLog(item) [L36048]
  ↓
$state.go("optometryLogList", { uartDeviceId: item.uartDevice.id }) [L36050]
  ↓
optometryLogListCtrl [L36135]
  ↓
$scope.obj.uartDeviceId = $stateParams.uartDeviceId [L36138]
```

**重要**：**optometryGlassesCtrl 与 optometryLogListCtrl 无任何直接源码关系**（S1-107/108/110 报告错误）

---

## 7. 入口参数 provenance

### 7.1 $state.go("optometryLogList", ...) 入口参数

| 参数 | 来源表达式 | 所在 Controller | 业务对象 | A-F |
|---|---|---|---|---|
| `uartDeviceId` | `item.uartDevice.id` | optometryListCtrl L36051 | UartDevice 字段 | A |

### 7.2 item 来源链

```
optometryListCtrl L36010 searchSupplierList
  └─ Read /config/selectAllUartDeviceVoList.json (ListFactory)
     └─ $scope.getSupplierListFactory.items  (数组)
        └─ item.uartDevice  (每个 item 包含 uartDevice 嵌套对象)
           └─ item.uartDevice.id  (L36051 访问)

optometryListCtrl.lookLog(item)  [L36048]
  └─ item.uartDevice.id  → uartDeviceId  → $state.go("optometryLogList", ...)
```

### 7.3 optometryLogListCtrl 内 uartDeviceId 消费

```javascript
// L36138
$scope.obj.uartDeviceId = $stateParams.uartDeviceId;

// L36142
$scope.getSupplierListFactory = new ListFactory(
  '/config/selectUartDeviceLogVoList.json',
  0,
  $scope.pageSize,
  $scope.obj  // 含 uartDeviceId
);
```

### 7.4 参数完整数据链

```
optometryListCtrl.searchSupplierList (L36009)
  ↓ Read
/config/selectAllUartDeviceVoList.json
  ↓ Response
$scope.getSupplierListFactory.items
  ↓ User trigger (HTML F 边界)
$scope.lookLog(item) (L36048)
  ↓ Access
item.uartDevice.id
  ↓ $state.go
"optometryLogList" + { uartDeviceId: item.uartDevice.id }
  ↓ optometryLogListCtrl receive
$stateParams.uartDeviceId (L36138)
  ↓ Scope
$scope.obj.uartDeviceId
  ↓ Read
/config/selectUartDeviceLogVoList.json (ListFactory)
```

---

## 8. 初始化执行链

### 8.1 注册即执行（按行号顺序）

| # | 行号 | 语句 | 类型 | A-F |
|---:|---:|---|---|---|
| 1 | 36137 | `$scope.obj = {};` | Scope 初始化 | A |
| 2 | 36138 | `$scope.obj.uartDeviceId = $stateParams.uartDeviceId;` | **StateParams 读取** | A |
| 3 | 36139 | `$scope.pageSize = 20;` | Scope 字段 | A |
| 4 | 36140 | `$scope.obj.splitStatus = null;` | Scope 字段 | A |
| 5 | 36141-36155 | `$scope.searchSupplierList = function` | 函数定义 | A |
| 6 | 36156 | `$scope.searchSupplierList();` | **Init 立即 Read**（ListFactory） | A |
| 7 | 36158-36161 | `$scope.setStatus = function` | 函数定义 | A |
| 8 | 36162 | `}]);` | Controller 闭合 | A |

### 8.2 Init 立即 Read 链

```
[唯一] $scope.searchSupplierList() (L36156)
    └─ Read /config/selectUartDeviceLogVoList.json (ListFactory)
       └─ $scope.getSupplierListFactory = new ListFactory(..., 0, 20, $scope.obj)
          └─ nextPage() → $("#Pagination").pagination($scope.getSupplierListFactory.count, ...)
```

### 8.3 Init 链特点

- **极简**：仅 1 个 Init 立即 Read
- **依赖**：依赖 `$stateParams.uartDeviceId`（必须由入口 State 提供）
- **无 fallback**：如果 `$stateParams.uartDeviceId` 不存在，Request 字段为 undefined

---

## 9. API 全量

### 9.1 完整 API 清单

| # | 行号 | API | 类型 | Factory | 调用函数 | A-F |
|---:|---:|---|---|---|---|---|
| 1 | 36142 | `/config/selectUartDeviceLogVoList.json` | Read | **ListFactory** ($scope.getSupplierListFactory) | searchSupplierList | A |

**唯一 API**：1 个
**call site**：1 个

### 9.2 关键观察

- optometryLogListCtrl **仅 1 个 API**（ListFactory 形式的 Read）
- **0 个** saveOrQuery
- **0 个** ObjectFactory 实例
- **0 个** HttpFactory 调用
- **0 个** Write API
- **0 个** $state.go 出口

### 9.3 三个 optometry* Controller API 对比

| Controller | unique API | call site | Read | Write | Factory 类型 |
|---|---:|---:|---:|---:|---|
| optometryGlassesCtrl | 14 | 13 | 9 | 5 | ObjectFactory(9) + ListFactory(1) + FN(3) |
| optometryListCtrl | 11 | 10 | 6 | 5 | ObjectFactory(6) + ListFactory(1) + HttpFactory(3) |
| optometryLogListCtrl | **1** | **1** | **1** | **0** | ListFactory(1) |

**关键观察**：optometryLogListCtrl 是 3 个 optometry* Controller 中**最小**的（仅 28 行 + 1 API）

---

## 10. ListFactory

### 10.1 唯一 ListFactory

| 行号 | Factory 变量 | API | Request | pageStart | pageSize | A-F |
|---:|---|---|---|---:|---:|---|
| 36142 | `$scope.getSupplierListFactory` | `/config/selectUartDeviceLogVoList.json` | `$scope.obj` (uartDeviceId, splitStatus) | 0 | **20** | A |

### 10.2 ListFactory 行为

```javascript
// L36141-L36155
$scope.searchSupplierList = function () {
    $scope.getSupplierListFactory = new ListFactory(
        '/config/selectUartDeviceLogVoList.json', 0, $scope.pageSize, $scope.obj
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

### 10.3 ListFactory 关键参数

| 参数 | 值 | A-F |
|---|---:|---|
| URL | `/config/selectUartDeviceLogVoList.json` | A |
| pageStart | 0 | A |
| pageSize | 20（$scope.pageSize） | A |
| filter object | `$scope.obj` (含 uartDeviceId, splitStatus) | A |
| items 消费者 | 无显式 consumer | A |
| 分页 | jQuery `$("#Pagination").pagination(count, ...)` | A |
| 自动调用 | **是**（`nextPage()` 自动调 API） | A |

### 10.4 与 optometryListCtrl 的 ListFactory 对比

| 维度 | optometryListCtrl | optometryLogListCtrl |
|---|---|---|
| Factory 变量 | `$scope.getSupplierListFactory` | `$scope.getSupplierListFactory` |
| URL | `/config/selectAllUartDeviceVoList.json` | `/config/selectUartDeviceLogVoList.json` |
| pageSize | 100 | 20 |
| 业务 | UartDevice 主列表 | UartDevice 日志列表 |

**两 Controller 共享 `$scope.getSupplierListFactory` 变量名**（同名 Factory 实例，A 级）

---

## 11. ObjectFactory / HttpFactory

### 11.1 ObjectFactory

**0 个**（A 级）

### 11.2 HttpFactory

**0 个**（A 级）

### 11.3 Factory 总计

| Factory 类型 | 数量 |
|---|---:|
| ObjectFactory | 0 |
| ListFactory | 1 |
| HttpFactory | 0 |
| **总 Factory 调用** | **1** |

**关键观察**：optometryLogListCtrl 是 3 个 optometry* Controller 中**Factory 最少**的

---

## 12. 日志主对象

### 12.1 主对象

| 对象 | 来源 | 字段 | Consumer | 行号 | A-F |
|---|---|---|---|---|---|
| `$scope.getSupplierListFactory.items` | `/config/selectUartDeviceLogVoList.json` Response | 数组（具体字段未访问） | 无显式 consumer | 36142 | A |
| `$scope.obj` | Init 派生（含 uartDeviceId, splitStatus） | Object | ListFactory Request | 36137-36140 | A |

### 12.2 items 字段（未知）

**F 边界**：Controller 范围内**0 处** `item.xxx` 访问
- 无法确定 items 实际字段
- 必须**严禁** 推断 items 字段

### 12.3 obj 字段

| 字段 | 来源 | 行号 |
|---|---|---|
| `uartDeviceId` | `$stateParams.uartDeviceId` (L36138) | A |
| `splitStatus` | `null` (L36140) | A |

**注意**：源码**不**显示 obj 有任何其它字段（虽然 `obj = {}` 之后只赋了 2 个字段）

---

## 13. Response → items

### 13.1 主 Response

| API | Response 路径 | 落点 | Consumer | A-F |
|---|---|---|---|---|
| `/config/selectUartDeviceLogVoList.json` | ListFactory 内部管理 | `$scope.getSupplierListFactory.items` | jQuery pagination（无显式 item 访问） | A |

### 13.2 关键观察

- 0 处显式 items 访问
- 仅 jQuery pagination 使用 `count`
- Controller 范围内**不读取**任何 item 字段

---

## 14. medicalRecord

### 14.1 medicalRecord 全量搜索

```powershell
# 0 处 medicalRecord 字符串 in L36135-L36162
```

**关键发现**：optometryLogListCtrl **0 处** `medicalRecord` 字符串（A 级确认）

### 14.2 含义

- optometryLogListCtrl **不**处理 medicalRecord
- 与 optometryGlassesCtrl 完全不同
- 与 optometryListCtrl 业务一致（UartDevice 设备日志）

### 14.3 item 中是否含 medicalRecord

**F 边界**：optometryLogListCtrl 0 处 item 访问，无法确定

---

## 15. medicalRecordId

### 15.1 medicalRecordId 全量搜索

```powershell
# 0 处 medicalRecordId 字符串 in L36135-L36162
```

**关键发现**：optometryLogListCtrl **0 处** `medicalRecordId` 字符串（A 级确认）

### 15.2 含义

- optometryLogListCtrl **不**使用 medicalRecordId
- 与 optometryGlassesCtrl 完全不同
- 与 optometryListCtrl 业务一致

### 15.3 medicalRecordId 路径增量

optometryLogListCtrl 范围内**未发现**新路径
- **无 medicalRecordId 任何来源**
- **无 medicalRecordId 参与 Read**
- **无 medicalRecordId 参与 Write**
- **无 medicalRecordId 参与 State**

**S1-108 + S1-111 锁定的 9 类路径在 optometryLogListCtrl 范围 0 处出现**

### 15.4 与医疗记录链的关系

**optometryLogListCtrl 与医疗记录链无任何源码直接关系**
- 0 处 medicalRecord
- 0 处 medicalRecordId
- 0 处 patient / customer / customerCheckin
- 0 处 optometry 验光业务字段
- 唯一字段：uartDeviceId, splitStatus, pageSize

---

## 16. 页面动作

### 16.1 2 个 $scope 函数分类

| 函数 | 行号 | 类别 | A-F |
|---|---|---|---|
| `$scope.searchSupplierList` | 36141 | **B. 查询**（ListFactory 立即） | A |
| `$scope.setStatus` | 36158 | **C. 列表操作**（修改 splitStatus） | A |

**总计**：2 个函数
- Init 立即：1 个（searchSupplierList）
- 用户动作：1 个（setStatus）

### 16.2 详细行为

```
[Init 立即] $scope.searchSupplierList() (L36156)
    └─ Read /config/selectUartDeviceLogVoList.json (ListFactory)
       └─ $scope.getSupplierListFactory.items

[用户动作] $scope.setStatus(idx) (L36158)
    └─ $scope.obj.splitStatus = idx
       └─ $scope.searchSupplierList() (触发 Read 刷新)
```

### 16.3 与 optometryListCtrl 关系

- optometryListCtrl 中 `$scope.lookLog(item)` 跳转 optometryLogList
- optometryLogListCtrl 中 `$scope.setStatus(idx)` 触发 Read 刷新
- **两个 Controller 通过 uartDeviceId 间接连接**

---

## 17. Write

### 17.1 Write 全量

| API | 数量 | A-F |
|---|---:|---|
| saveOrQuery Write | **0** | A |
| ObjectFactory Write | **0** | A |
| HttpFactory Write | **0** | A |
| FN_promiseCall Write | **0** | A |
| **总计** | **0** | A |

### 17.2 关键观察

- optometryLogListCtrl 是 3 个 optometry* Controller 中**唯一无 Write** 的
- 整个 Controller 是**只读**日志列表
- 0 处 Write API

### 17.3 "只读页面"判断

**A 级确认**：optometryLogListCtrl 是只读 Controller，**不执行业务动作**
- 0 处 Write API
- 仅 1 个 ListFactory Read
- 0 处 $state.go 出口
- 0 处 Popup.notice

---

## 18. Read → Write

### 18.1 字段级闭合

**无 Write**，故 Read → Write 链**不适用**

| Read | 后续 Write | 详情 |
|---|---|---|
| selectUartDeviceLogVoList.json | **无** | ListFactory Read 无 Write 后续 |

---

## 19. Write → Read

### 19.1 全部 Write success 行为

**无 Write**，故 Write → Read 链**不适用**

---

## 20. Popup / callback / timeout

### 20.1 Popup.notice 全量

```powershell
# 0 处 Popup.notice in L36135-L36162
```

**关键发现**：optometryLogListCtrl **0 处** Popup.notice（A 级确认）

### 20.2 $timeout 调用

```powershell
# 0 处 $timeout in L36135-L36162
```

**0 处** $timeout（A 级）

### 20.3 callback

| 位置 | 形式 | A-F |
|---|---|---|
| 36149 | jQuery pagination callback | A |

**callback 总计**：1 处（jQuery pagination）

### 20.4 关键观察

- optometryLogListCtrl 是 3 个 optometry* Controller 中**最静默**的
- 0 处 Popup
- 0 处 $timeout
- 仅 1 处 jQuery callback

---

## 21. State 出口

### 21.1 $state.go 全量

```powershell
# 0 处 $state.go in L36135-L36162
```

**关键发现**：optometryLogListCtrl **0 处** $state.go（A 级确认）

### 21.2 含义

- optometryLogListCtrl 是 "dead-end" 页面
- 用户进入后**无法**通过 Controller 离开
- 离开方式：浏览器后退 / 其它机制（F 边界）

### 21.3 与 optometryListCtrl 关系

- optometryListCtrl → optometryLogList ✅（L36050）
- optometryLogListCtrl → optometryList **0 处**（"dead-end"）

### 21.4 与 optometryGlassesCtrl 关系

- optometryGlassesCtrl → optometryLogList **0 处**（S1-114 纠偏）
- optometryLogListCtrl → optometryGlasses **0 处**

**optometryLogListCtrl 与 optometryGlassesCtrl 无任何 State 双向关系**

---

## 22. optometryList 对照

### 22.1 业务对象对比

| State | Controller | medicalRecord | $stateParams | 业务对象 |
|---|---|---|---|---|
| `optometryList` | optometryListCtrl | **0 处** | **0 处** | **UartDevice** |
| `optometryLogList` | optometryLogListCtrl | **0 处** | `uartDeviceId` | **UartDevice 日志** |
| `optometryGlasses` | optometryGlassesCtrl | 4 处 | `medicalRecordId, edit` | **医疗记录（验光）** |

### 22.2 关键发现

1. **optometryList 与 optometryLogList 业务一致**（UartDevice 设备管理）
2. **optometryGlasses 与前两者业务完全不同**（验光配镜）
3. **optometryList Ctrl 跳转 optometryLogList**（带 uartDeviceId）
4. **optometryLogList 不返回 optometryList**（dead-end）
5. **3 个 Controller 都不共享 medicalRecord/medicalRecordId**

### 22.3 名称相似 ≠ 业务相关

| 共同点 | 差异点 |
|---|---|
| 名称都含 "optometry" | 业务完全不同（UartDevice vs 验光） |
| 都在 bestvisionWeb module | medicalRecord 处理完全分离 |
| 都用 ListFactory 列表 | 跳转链独立 |

---

## 23. HTML 边界

### 23.1 optometryLogList HTML 状态

| 资源 | 数量 | 包含 optometryLogList |
|---|---:|:---:|
| 7 untracked HTML | 7 | **0** |
| 视光之家url.txt | 1 | 0 |
| Git 历史 .html | 0 | - |

**关键发现**：**0 个 optometryLogList 相关 HTML/Template**（A 级）

### 23.2 与 optometryList/optometryGlassesCtrl 关系

| Controller | HTML 模板 |
|---|---|
| optometryGlassesCtrl | F 边界（S1-112） |
| optometryListCtrl | F 边界（S1-113） |
| optometryLogListCtrl | F 边界（本轮） |

**3 个 Controller 都没有 HTML 模板**（A 级穷举确认）

---

## 24. 26 项矩阵

| # | 审计项 | 证据 | A-F | L1/L2/L3 |
|---:|---|---|---|---|
| 01 | optometryLogList 全局命中 | controller.js 2 处（注册 + $state.go） | A | L1 |
| 02 | optometryLogListCtrl 全局命中 | controller.js 1 处（L36135） | A | L1 |
| 03 | Controller 注册 | L36135，bestvisionWeb module | A | L1 |
| 04 | Controller 范围 | L36135-L36162（28 行） | A | L1 |
| 05 | DI | 9 个（$scope/Popup/$stateParams/$interval/$rootScope/$state/ObjectFactory/ListFactory） | A | L1 |
| 06 | StateParams | 1 处（L36138 uartDeviceId） | A | L1 |
| 07 | optometryGlassesCtrl 入口 | **0 处**（S1-114 纠偏） | A | L1 |
| 08 | 入口参数全集 | `uartDeviceId` 1 个 | A | L1 |
| 09 | medicalRecordId | **0 处** | A | L1 |
| 10 | 初始化链 | Session 恢复 + 1 个 Init Read (searchSupplierList) | A | L1 |
| 11 | API unique | 1 个（selectUartDeviceLogVoList.json） | A | L1 |
| 12 | API call site | 1 个 | A | L1 |
| 13 | Read | 1 个 | A | L1 |
| 14 | Write | **0 个** | A | L1 |
| 15 | ListFactory | 1 个（$scope.getSupplierListFactory） | A | L1 |
| 16 | ObjectFactory | **0 个** | A | L1 |
| 17 | 日志主对象 | $scope.getSupplierListFactory.items | A | L1 |
| 18 | Response→items | ListFactory 内部管理 | A | L1 |
| 19 | medicalRecord Consumer | **0 处** | A | L1 |
| 20 | medicalRecordId Consumer | **0 处** | A | L1 |
| 21 | 页面动作 | 2 个函数（searchSupplierList, setStatus） | A | L1 |
| 22 | State 出口 | **0 处 $state.go**（dead-end） | A | L1 |
| 23 | Write→Read | 不适用（无 Write） | A | L1 |
| 24 | Popup/timeout/callback | 0 Popup + 0 $timeout + 1 jQuery callback | A | L1 |
| 25 | HTML 边界 | 0 个 optometryLogList HTML | A/F | L1 |
| 26 | A/B/C/D/E/F | A: 25 / F: 1 | A | L1 |

### 24.1 A-F 分布

| 等级 | 数量 | 比例 |
|---|---:|---:|
| A | 25 | 96% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 0 | 0% |
| E | 0 | 0% |
| F | 1 | 4% |

### 24.2 L1/L2/L3 分布

| 级别 | 数量 |
|---|---:|
| L1 | 26 |
| L2 | 0 |
| L3 | 0 |

---

## 25. A-F 总结

- **A 级**：25 项（96%）
- **F 级**：1 项（HTML 边界）
- **B/C/D/E 级**：0 项

---

## 26. L1/L2/L3 总结

- **L1**：26 项（100%）
- **L2**：0 项
- **L3**：0 项

---

## 27. F 边界

| F 项 | 详情 |
|---|---|
| 1 | optometryLogList HTML 模板 | 0 个 untracked HTML 含 optometryLogList 引用 |
| 2 | optometryLogList State 配置 | 0 处 `.state(` in controller.js |
| 3 | UI 触发函数 | 0 个 optometry 引用 in 7 HTML |
| 4 | 离开方式 | 0 处 $state.go + 0 处 HTML |
| 5 | optometryLogList items 字段 | Controller 0 处 item 访问 |

---

## 28. 红线

| 红线 | 状态 |
|---|---|
| 1. 仅静态分析 | ✅ |
| 2. API actual | 0 |
| 3. Write actual | 0 |
| 4. 不打开真实系统 | ✅ |
| 5. 不调用任何 API | ✅ |
| 6. 不修改生产数据 | ✅ |
| 7. 不修改 controller.js | ✅（SHA256 = `F40589FF0C56DE60BF4785A0B6C5B0A33519B75A30A15D988B0E1BDCF0A19433` 与 S1-113 一致） |
| 8. 不修改 7 HTML | ✅ |
| 9. 不修改 视光之家url.txt | ✅（SHA256 = `7C2D0681964FCADB12E82804A1C499B22092479FD1A78A8FD61FFC38CF009C4C`） |
| 10. 不修改历史 MD（165-174） | ✅ |
| 11. P0 = 54 冻结 | ✅ |
| 12. P1 = 8 冻结 | ✅ |
| 13. 10 untracked 原样保留 | ✅ |
| 14. 1 gitignored 原样保留 | ✅ |
| 15. deliveryList.html hash 不变 | ✅（12720 bytes / SHA256 `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`） |

---

## 29. 最终页面 DAG

### 29.1 入口链

```
[外部入口 - F 边界：HTML/State 配置不可得]
- optometryListCtrl.lookLog(item) [L36048] (已确认 S1-113)
- 其它入口（F 边界）

↓

[optometryLogList State]  (F 边界：State 配置不在 controller.js)

↓

[optometryLogListCtrl L36135]  (28 行)
DI: $scope, Popup, $stateParams, $interval, $rootScope, $state, ObjectFactory, ListFactory
$stateParams: 1 处（uartDeviceId）
```

### 29.2 Init 链

```
[1] $scope.obj = {} (L36137)
[2] $scope.obj.uartDeviceId = $stateParams.uartDeviceId (L36138)
[3] $scope.pageSize = 20 (L36139)
[4] $scope.obj.splitStatus = null (L36140)
[5] $scope.searchSupplierList() (L36156) - Init 立即 Read
    └─ Read /config/selectUartDeviceLogVoList.json (ListFactory)
       └─ $scope.getSupplierListFactory = new ListFactory(..., 0, 20, $scope.obj)
       └─ nextPage() → $("#Pagination").pagination($scope.getSupplierListFactory.count, ...)
```

### 29.3 用户动作链

```
[用户动作] $scope.setStatus(idx) (L36158)
    └─ $scope.obj.splitStatus = idx
       └─ $scope.searchSupplierList() (触发 Read 刷新)
```

### 29.4 完整控制流（含跨 Controller）

```
optometryListCtrl.searchSupplierList (L36009)
  ↓ Read
/config/selectAllUartDeviceVoList.json
  ↓ Response
$scope.getSupplierListFactory.items (optometryListCtrl)
  ↓ User trigger (HTML F 边界)
optometryListCtrl.lookLog(item) (L36048)
  ↓ Access item.uartDevice.id
  ↓ $state.go
optometryLogList State { uartDeviceId: item.uartDevice.id } (L36050)
  ↓ Controller routing
optometryLogListCtrl (L36135)
  ↓ StateParams
$scope.obj.uartDeviceId = $stateParams.uartDeviceId (L36138)
  ↓ Init Read
/config/selectUartDeviceLogVoList.json (L36142)
  ↓ Response
$scope.getSupplierListFactory.items (optometryLogListCtrl)
  ↓ User action
$scope.setStatus(idx) (L36158) → 重新查询
  ↓ Dead-end
[0 处 $state.go 出口]
```

---

## 30. 最终结论

### 30.1 S1-114 核心发现

1. **optometryLogListCtrl 是最小 optometry* Controller**（28 行 + 1 API）
2. **S1-107/108/110 错误纠正**：L36050 `$state.go("optometryLogList", ...)` 实际在 **optometryListCtrl**（不在 optometryGlassesCtrl）
3. **0 处 medicalRecord / medicalRecordId**（A 级确认）
4. **0 处 Write**（A 级确认）
5. **0 处 $state.go 出口**（dead-end 页面）
6. **$stateParams 仅 1 个字段**：`uartDeviceId`
7. **与 optometryGlassesCtrl 无任何直接源码关系**
8. **与 optometryListCtrl 业务一致**（UartDevice 设备日志）

### 30.2 三个 optometry* Controller 关系图

```
                     optometryCtrl (L34776)
                              │
                              │ $state.go("optometryGlasses", { medicalRecordId })
                              ↓
                    optometryGlassesCtrl (L35383, 577 行)
                              │
                              │ $state.go("optometryList", { reload: true }) (L36034)
                              ↓
                      optometryListCtrl (L35962, 171 行)
                              │
                              │ $state.go("optometryLogList", { uartDeviceId }) (L36050)
                              ↓
                   optometryLogListCtrl (L36135, 28 行)
                              │
                              ↓
                          (dead-end, 0 $state.go)
```

### 30.3 业务分层

| Controller | 业务领域 | medicalRecord | 是否终点 |
|---|---|---|---|
| optometryCtrl | 验光列表 | ✅ | 否（→ optometryGlasses） |
| optometryGlassesCtrl | 验光配镜 | ✅ | 否（→ optometryList） |
| optometryListCtrl | **UartDevice** | ❌ | 否（→ optometryLogList） |
| optometryLogListCtrl | **UartDevice 日志** | ❌ | **是（dead-end）** |

### 30.4 与医疗记录链的关系

**optometryListCtrl + optometryLogListCtrl 与医疗记录链无任何源码直接关系**（A 级）
- 0 处 medicalRecord
- 0 处 medicalRecordId
- 0 处 patient / customer
- 名称相似 ≠ 业务相关

### 30.5 F 边界最终结论

**optometryLogListCtrl 的 UI 层证据（HTML/State 配置）在当前 working dir + Git 历史 + 7 untracked HTML + 视光之家url.txt 范围内完全不可得**（A 级穷举 + F 边界保持）

---

**审计完成。本文档为 175 号，提交后将形成 tracked=184，untracked=10，ignored=1。**
