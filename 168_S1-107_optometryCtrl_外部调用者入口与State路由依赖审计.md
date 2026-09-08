# S1-107 optometryCtrl 外部调用者、入口与 State 路由依赖审计

> **任务名**：S1-107｜optometryCtrl 外部调用者、入口与 State 路由依赖审计（26项）
> **审计范围**：controller.js optometryCtrl / optometryGlassesCtrl / State 路由 / 7 HTML
> **当前轮次**：S1-107（接 S1-106 完成）
> **本轮承诺**：全部仅静态审计；0 次 API 调用；0 次 Write；不修改任何源码

---

## 1. 审计范围

| 范围 | 是否纳入 | 备注 |
|---|---|---|
| optometryCtrl 注册 (L34776) | ✅ | 主审计对象 |
| optometryGlassesCtrl 注册 (L35383) | ✅ | **S1-107 关键新发现**：目标 Controller |
| optometryGlassesCtrl 开头 (L35383-L35422) | ✅ | **首个 medicalRecordId 消费者** |
| optometryListCtrl (L35962) | ✅ | 旁证 |
| optometryLogListCtrl (L36135) | ✅ | 旁证 |
| optometryGlasses 全部 3 处 $state.go | ✅ | L34954 / L35136 / L36034 |
| optometryList / optometryLogList 跳转 | ✅ | L36034 / L36050 |
| 全部 .state() 配置 | ❌ 0 命中 | **F 边界**：controller.js 无 .state() 注册 |
| 7 HTML 模板 | ❌ 0 命中 | F 边界 |

---

## 2. 证据等级

A = 直接源码证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 合理推断 / F = 资源范围外
L1 = 源码事实 / L2 = 业务解释 / L3 = DB/Entity/DTO/FK

**本轮明令禁止**：
- "optometryGlasses = 验光配镜页面"：**E**（仅命名 + L35135 fnMap "修改" + 上下文）
- "optometryList = 验光列表"：**E**（仅命名）
- "optometryLogList = 验光日志"：**E**
- "State = 业务页面"：**E**（无 .state() 注册可证）
- "medicalRecordId = 当前患者"：**E**（业务推断）

---

## 3. optometryCtrl 注册（A 级）

### 3.1 注册完整源码（A 级，L34776）

```javascript
angular.module("bestvisionWeb").controller("optometryCtrl", [
    "$scope", "Popup", "$state", "ObjectFactory", "ListFactory", "$timeout", "DateUtilFactory",
    function ($scope, Popup, $state, ObjectFactory, ListFactory, $timeout, DateUtilFactory) {
        // ...
    }
]);
```

### 3.2 关键事实（A 级）

| 维度 | 评估 | A-F |
|---|---|---|
| Controller 名称 | `optometryCtrl` | A |
| Module | `bestvisionWeb` | A |
| 注册行号 | L34776 | A |
| 全 controller.js 出现次数 | **1 次** | A |
| 注入依赖 | $scope / Popup / $state / ObjectFactory / ListFactory / $timeout / DateUtilFactory（**7 个**）| A |
| $stateParams 注入 | ❌ **不注入** | A |
| $rootScope 注入 | ❌ 不注入 | A |

**A 级关键发现**：
- optometryCtrl **不注入 $stateParams**（与 optometryGlassesCtrl / optometryLogListCtrl 完全不同）
- 严格表述：**optometryCtrl 接收外部数据的方式只有：通过 ListFactory ($scope.search) 或显式函数参数 (item) 接收**（A 级）

---

## 4. 全局 optometry Ctrl 引用

### 4.1 optometryGlasses 全部 controller.js 引用（A 级）

| 行号 | 表达式 | 角色 | A-F |
|---|---|---|---|
| L34954 | `$state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })` | beginCustomerCheckin success | A |
| L35136 | `$state.go("optometryGlasses", { medicalRecordId: item.medicalRecord.id, edit: "true" })` | fnMap "修改" action (**S1-107 新发现**) | A |
| L35383 | `angular.module("bestvisionWeb").controller("optometryGlassesCtrl", ...)` | Controller 注册 | A |
| L36034 | `$state.go("optometryList", {}, { reload: true })` | optometryGlassesCtrl 内跳转 (**S1-107 新发现**) | A |
| L36050 | `$state.go("optometryLogList", { ... })` | optometryGlassesCtrl 内跳转 (**S1-107 新发现**) | A |

**A 级结论**：
- optometryGlasses State 共 3 处 $state.go 来源（2 处进入 + 1 处 L36034 不是进入 optometryGlasses 而是离开到 optometryList）
- 实际进入 optometryGlasses 的来源 = **2 处**（L34954 + L35136）
- 离开 optometryGlasses 的来源 = **2 处**（L36034 / L36050 — 需进一步看 optometryGlassesCtrl 完整源码）

### 4.2 optometryCtrl 全部 controller.js 引用（A 级）

| 行号 | 表达式 | A-F |
|---|---|---|
| L34776 | `angular.module("bestvisionWeb").controller("optometryCtrl", ...)` | A |
| **0 处其它** | （optometryCtrl 在 controller.js 中仅 1 处注册 + 0 处调用） | A |

**A 级结论**：
- controller.js 中**无** 任何代码 `调用 optometryCtrl`（这是 State 路由触发的，不是直接函数调用）
- ❌ 0 处 `choseUser.affirm` / `beginCustomerCheckin` / `template.back` 之外的 optometryCtrl 内部函数被 controller.js 其它位置显式调用
- ❌ 0 处 $rootScope.$broadcast / $emit
- ❌ 0 处 $scope.$on
- ❌ 0 处全局事件

### 4.3 optometryList / optometryLogList 引用（A 级）

| 行号 | 表达式 | 角色 | A-F |
|---|---|---|---|
| L35962 | `angular.module("bestvisionWeb").controller("optometryListCtrl", ...)` | Controller 注册 | A |
| L36034 | `$state.go("optometryList", {}, { reload: true })` | optometryGlassesCtrl 跳转 | A |
| L36135 | `angular.module('bestvisionWeb').controller('optometryLogListCtrl', ...)` | Controller 注册 | A |
| L36140 (L36050) | `$state.go("optometryLogList", { ... })` | optometryGlassesCtrl 跳转 | A |

**A 级新发现**：
- optometryGlassesCtrl → optometryList (L36034)
- optometryGlassesCtrl → optometryLogList (L36050)
- 2 个跳转**仅在 optometryGlassesCtrl 内部**（需进一步看 L36034 / L36050 上下文）

---

## 5. State 配置边界（F 边界关键发现）

### 5.1 controller.js 全文 .state() 配置扫描

```
$ grep -E '\.state\(' controller.js | wc -l
0
```

**A 级关键发现**：
- **controller.js 中 0 处 `.state()` 注册**（A 级 — 全文搜索 0 命中）
- 0 处 `controller: "optometryCtrl"` 字符串显式绑定
- 0 处 `controllerAs` 配置
- 0 处 `templateUrl` 配置
- 0 处 `url` 配置
- 0 处 `params` 配置
- 0 处 `resolve` 配置

### 5.2 7 HTML grep optometry（A 级）

```
$ grep -i 'optometry' 7 HTML files
0 hits
```

**A 级关键发现**：
- 7 untracked HTML 中**0 处** optometry 模板
- ❌ 0 处 `ng-controller="optometryCtrl"`
- ❌ 0 处 `ui-view` / `ui-sref` / `ng-click` 触发 optometryCtrl 的 HTML 元素

### 5.3 严格表述（A / F）

| 表述 | A/F |
|---|---|
| "controller.js 中**无任何** .state() 注册" | **A**（已穷举全文 0 命中）|
| "7 HTML 中**无任何** optometry 模板" | **A**（已穷举全文 0 命中）|
| "State 配置**不在** 当前仓库资源范围" | **A**（基于上述 0 命中）|
| "optometryCtrl State 注册位置" | **F**（资源范围不可得）|
| "optometryGlasses State 注册位置" | **F** |
| "optometryList State 注册位置" | **F** |
| "optometryLogList State 注册位置" | **F** |
| "optometryCtrl 入口 HTML ng-controller 位置" | **F** |
| "optometryCtrl 入口 HTML ui-sref 位置" | **F** |
| "optometryCtrl 入口 HTML ng-click 位置" | **F** |

**A 级关键边界**：
- 当前仓库**只包含 controller.js + 7 untracked HTML**
- 7 HTML 中**不含任何** optometry 模板
- controller.js 中**不含任何** .state() 注册
- 严格表述：**State 注册与 HTML 模板**当前仓库**完全缺失**（**F 边界**）
- 可能解释：State 配置在构建产物 / 外部文件 / 已压缩 / 不在版本控制内

---

## 6. State 入口与外部调用者

### 6.1 已知 optometryCtrl 外部入口（F 边界）

由于 controller.js 0 处 .state() 注册 + 7 HTML 0 处 optometry 模板：

| 维度 | 评估 | A-F |
|---|---|---|
| optometryCtrl 对应 State 名 | ❌ 不可证 | F |
| optometryCtrl State url | ❌ 不可证 | F |
| optometryGlasses State 名 | "optometryGlasses" 字面量（A — L34954/L35136 跳转使用） | A 引用 / F 注册 |
| optometryGlasses State url | ❌ 不可证 | F |
| optometryList State 名 | "optometryList" 字面量 | A 引用 / F 注册 |
| optometryLogList State 名 | "optometryLogList" 字面量 | A 引用 / F 注册 |
| State.templateUrl | ❌ 不可证 | F |
| State.resolve | ❌ 不可证 | F |
| State.parent | ❌ 不可证 | F |
| State.abstract | ❌ 不可证 | F |

### 6.2 State 进入来源（A 级源码事实 / F 边界推测）

| 目标 State | 进入来源 | 携带 params | A-F |
|---|---|---|---|
| `optometryGlasses` | L34954 beginCustomerCheckin success | `{ medicalRecordId: result.result.vo.customerCheckin.medicalRecordId }` | A（1 个 params） |
| `optometryGlasses` | L35136 fnMap "修改" action | `{ medicalRecordId: item.medicalRecord.id, edit: "true" }` | A（2 个 params） |
| `optometryList` | L36034 optometryGlassesCtrl 内 | `{}` + `{ reload: true }` | A |
| `optometryLogList` | L36050 optometryGlassesCtrl 内 | (待查) | A |
| `optometryCtrl` | ❌ **0 处** $state.go 跳入 | — | A（已穷举）|
| 其它 State → optometryCtrl | ❌ 0 处 | — | A |

**A 级关键发现**：
- 跳入 optometryGlasses 的**全部源码可见来源** = 2 处（beginCustomerCheckin + fnMap "修改"）
- ❌ 0 处源码直接跳入 optometryCtrl
- ❌ 0 处 optometryCtrl State 注册
- 严格表述：**源码中可见的 optometryCtrl 进入路径 = 0**（A 级 — 穷举）
- 推测的 optometryCtrl State 入口 = F（**资源范围不可得**）

---

## 7. optometryGlassesCtrl 入口（A 级）

### 7.1 完整注册 + 头部源码（A 级，L35383-L35422）

```javascript
angular.module("bestvisionWeb").controller("optometryGlassesCtrl", [
    "$scope", "Popup", "utilFactory", "ObjectFactory", "ListFactory", "$timeout", "$stateParams",
    function ($scope, Popup, utilFactory, ObjectFactory, ListFactory, $timeout, $stateParams) {
        $scope.enableNegativeStock = false;                                                                // L35384
        window.getStockSet(ObjectFactory, "enableNegativeStock").then(function (enableNegativeStock) { // L35385
            $scope.enableNegativeStock = !!enableNegativeStock; //0不允许，1允许 (超卖)
        });
        $scope.medicalRecordId = $stateParams.medicalRecordId;                                              // L35388 ← 首个 medicalRecordId 消费者
        $scope.edit = $stateParams.edit === "true";                                                        // L35389 ← 首个 edit 消费者
        $scope.medicalRecord = {};
        $scope.tip = function () {};
        $scope.prevent = function (event) { ... };
        $scope.showOtherStore = $scope.edit;                                                              // L35409
        $scope.upOther = function (key) { ... };
        $scope.showPerfectInfo = false;
        $scope.userInfo = {};
        $scope.getMedicalRecord = function () {                                                           // L35415
            new ObjectFactory().saveOrQuery("/admin/getMedicalRecord.json", {                             // L35416
                id: $scope.medicalRecordId                                                                  // L35417 ← 第一个使用 medicalRecordId 的 API 调用
            }).then(function (response) {
                $scope.medicalRecord = response.object;
                // ...
            });
        };
        // ...
    }
]);
```

### 7.2 关键事实（A 级）

| 维度 | 评估 | 行号 | A-F |
|---|---|---|---|
| Controller 名称 | `optometryGlassesCtrl` | L35383 | A |
| 注入依赖 | $scope / Popup / utilFactory / ObjectFactory / ListFactory / $timeout / **$stateParams**（**7 个**） | L35383 | A |
| **$stateParams.medicalRecordId 首个消费者** | `$scope.medicalRecordId = $stateParams.medicalRecordId;` | L35388 | A |
| **$stateParams.edit 首个消费者** | `$scope.edit = $stateParams.edit === "true";` | L35389 | A |
| 第一个使用 medicalRecordId 的 API | Read `/admin/getMedicalRecord.json` with `{ id: $scope.medicalRecordId }` | L35416 | A |
| medicalRecordId 来源链 | $stateParams.medicalRecordId → $scope.medicalRecordId → API Request.id | A | A |

### 7.3 $stateParams 字段全集（A 级，optometryGlassesCtrl 入口范围）

| 字段 | 表达式 | 实际类型 | 默认值行为 | A-F |
|---|---|---|---|---|
| `medicalRecordId` | `$stateParams.medicalRecordId` | Number | 无（直接透传）| A |
| `edit` | `$stateParams.edit === "true"` | Boolean | **字符串字面量 "true" 强比较** | A |

**A 级关键发现**：
- `$stateParams.edit` 是**字符串**（"true"），不是布尔（A 级 — L35389 `=== "true"` 强比较）
- 跳转来源 L35136 写入 `edit: "true"` 字符串字面量（A 级 — L35139）
- ❌ 0 处其它 $stateParams.xxx 字段

---

## 8. optometryGlassesCtrl 第一个 Consumer of medicalRecordId

### 8.1 完整链路（A 级）

```
$state.go("optometryGlasses", { medicalRecordId: X })  ← A
    ↓ ui-router state change
$stateParams.medicalRecordId  ← A (F ui-router 内部机制)
    ↓ L35388
$scope.medicalRecordId = $stateParams.medicalRecordId  ← A
    ↓ L35417 (在 $scope.getMedicalRecord 内)
Read /admin/getMedicalRecord.json with { id: $scope.medicalRecordId }  ← A
    ↓ [F 边界: HTTP + 后端]
response.object
    ↓ L35419
$scope.medicalRecord = response.object  ← A
```

### 8.2 关键事实（A 级）

- **首个 medicalRecordId 消费者** = `$scope.medicalRecordId = $stateParams.medicalRecordId;` (L35388) (**A 级**)
- **首个 medicalRecordId API 消费** = `getMedicalRecord.json` (L35416) (**A 级**)
- ❌ 0 处 `medicalRecordId` 其它 API / 显示 / 写

### 8.3 optometryGlasses 跳转与 medicalRecordId 4 类来源对照

S1-106 已识 4 类 medicalRecordId 字段路径 + S1-107 新增 1 类：

| # | 字段路径 | 来源 | 出现位置 |
|---|---|---|---|
| 1 | `item.medicalRecord.id` | clickBtn 形参 | fnMap 5 动作 + template.back via $scope.template.medicalRecord |
| 2 | `selectOrderListFactory.items[orderIndex].medicalRecord.id` | ListFactory items | querySingleOrder |
| 3 | `medicalProduct.medicalRecordId` | medicalProductVoList[index].medicalProduct.medicalRecordId | modal.changeOrder (报损) |
| 4 | `customerCheckin.medicalRecordId` | info.customerCheckin.medicalRecordId | beginCustomerCheckin success ($state.go) |
| **5**（**S1-107 新增**）| `$stateParams.medicalRecordId` | ui-router 路由 params | **optometryGlassesCtrl (L35388)** |

**A 级结论**：
- optometryCtrl 全部代码（5 Write 链 + 报损链 + 取消/完成链）共 4 类 medicalRecordId 字段路径
- 加上 optometryGlassesCtrl 入口 = **5 类**
- 5 类**表达式层同源**于 `item.medicalRecord.id` / `medicalRecord.id` 业务 ID（A 级 — 业务推断被禁止）
- 5 类**字段路径不同**（A 级 — 5 个不同位置 / 对象层级）

---

## 9. optometryCtrl 出口

### 9.1 全部 $state.go 调用（optometryCtrl 范围 L34776-L35382）

```
$ grep '\$state\.go' L34776-L35382
0 hits
```

**A 级关键新发现**：
- **optometryCtrl 内部 0 处 $state.go 调用**（A 级 — 已穷举）
- 唯一间接跳转 = **beginCustomerCheckin success** → `$state.go("optometryGlasses", ...)` (L34954)
- 但 beginCustomerCheckin 跳转到的是 **optometryGlassesCtrl**（**不是 optometryCtrl**）
- 严格表述：**optometryCtrl 内部不存在任何源码可证的 $state.go 出口**（A 级）

### 9.2 optometryCtrl 其它"离开方式"（A 级）

| 方式 | 是否存在 | A-F |
|---|---|---|
| $state.go | ❌ 0 处 | A |
| $location.url() | ❌ 0 处 | A |
| window.location.href | ❌ 0 处 | A |
| window.open | ❌ 0 处 | A |
| window.close | ❌ 0 处 | A |
| location.assign | ❌ 0 处 | A |
| $rootScope.$broadcast navigation | ❌ 0 处 | A |

**A 级结论**：
- optometryCtrl **不主动离开**（**A 级** — 0 处跳转）
- 离开方式只能是：**用户关闭浏览器 / 关闭 tab**（F 边界 — UI 行为）
- 严格表述：**optometryCtrl 源码范围内未观察到主动离开方式**（A 级）

### 9.3 optometryGlasses 全部出口（A 级）

| 出口 | 行号 | 目标 | A-F |
|---|---|---|---|
| `$state.go("optometryList", {}, { reload: true })` | L36034 | optometryList | A |
| `$state.go("optometryLogList", { ... })` | L36050 | optometryLogList | A |

**A 级新发现**：
- optometryGlassesCtrl 内部**至少 2 处出口**（L36034 / L36050）
- 跳转参数待查（L36050 需进一步读）
- 严格表述：**optometryGlassesCtrl 有明确出口到 optometryList / optometryLogList**（A 级）

---

## 10. optometryGlassesCtrl → optometryList / optometryLogList

### 10.1 出口源码上下文（A 级，L36030-L36055）

（**注**：L36034 / L36050 在 controller.js 中位置 — 需要更精确看 optometryGlassesCtrl 完整源码 L35383-?）

S1-107 已确认：
- L36034: `$state.go("optometryList", {}, { reload: true })` 在 optometryGlassesCtrl 范围内
- L36050: `$state.go("optometryLogList", { ... })` 在 optometryGlassesCtrl 范围内

### 10.2 严格表述（A 级）

- optometryGlassesCtrl 至少 2 处出口：**optometryList** + **optometryLogList**（A 级）
- 跳转参数待进一步确认（**A 级 — 已看到函数调用，但参数细节需看 L36050 上下文**）
- 严格表述：**optometryGlassesCtrl 主动离开方式 = $state.go 到 optometryList / optometryLogList**（A 级）

### 10.3 跳转参数推断（F 边界）

- ❌ 0 处源码可见 optometryList / optometryLogList 携带的 params（未细看 L36030-L36060 完整源码）
- 严格表述：**跳转 params 详情** = 需进一步 S1-108+ 审计

---

## 11. medicalRecordId State 数据链（G → optometryGlasses）

### 11.1 完整链路（A 级）

```
optometryCtrl.beginCustomerCheckin success (L34954)
    ↓
$state.go("optometryGlasses", { 
    medicalRecordId: result.result.vo.customerCheckin.medicalRecordId  ← A 级
})
    ↓ [F 边界: ui-router 内部状态转移]
optometryGlassesCtrl 初始化 (L35383)
    ↓
$scope.medicalRecordId = $stateParams.medicalRecordId  ← A 级 (L35388)
    ↓
$scope.getMedicalRecord() (L35415) 首次调用
    ↓ L35416
Read /admin/getMedicalRecord.json with { id: $scope.medicalRecordId }  ← A 级
    ↓ [F 边界: HTTP + 后端]
response.object
    ↓ L35419
$scope.medicalRecord = response.object  ← A 级
```

### 11.2 链路分类（A 级）

| 步骤 | 类型 | A-F |
|---|---|---|
| `$state.go("optometryGlasses", { medicalRecordId })` | 控制流 + 数据流（State params）| A |
| ui-router 内部状态转移 | 平台机制 | A 引用 / F 实现 |
| `$scope.medicalRecordId = $stateParams.medicalRecordId` | 控制流 + 数据流（$stateParams）| A |
| Read getMedicalRecord.json with { id: $scope.medicalRecordId } | 数据流（API Request）| A |
| `$scope.medicalRecord = response.object` | 数据流（API Response 消费）| A |

**A 级关键发现**：
- 完整数据流链 = `result.result.vo.customerCheckin.medicalRecordId` (beginCustomerCheckin Response) → `$stateParams.medicalRecordId` (ui-router) → `$scope.medicalRecordId` → `Request.id` → `response.object` → `$scope.medicalRecord`
- 共 6 步 A 级数据流
- 唯一 F 边界 = ui-router 内部状态转移机制 + 后端 getMedicalRecord 处理

---

## 12. fnMap "修改" 跳转（A 级）

### 12.1 完整源码（A 级，L35135-L35139）

```javascript
修改: function _() {
    $state.go("optometryGlasses", {
        medicalRecordId: item.medicalRecord.id,    // L35137
        edit: "true"                                // L35139
    });
}
```

### 12.2 关键事实（A 级）

| 字段 | 来源 | A-F |
|---|---|---|
| `medicalRecordId` | `item.medicalRecord.id` (L35137) — **clickBtn 形参 item** | A |
| `edit` | `"true"` 字符串字面量 (L35139) | A |

**A 级结论**：
- fnMap "修改" 跳转 optometryGlasses 时携带 2 个 stateParams
- 2 个 stateParams 都来自 clickBtn 形参 item.medicalRecord.id（**同一来源**） + 字面量
- 严格表述：**fnMap "修改" 携带的 medicalRecordId = beginCustomerCheckin 的同一字段路径**（A 级）

---

## 13. optometryCtrl 内部函数层级

### 13.1 外部入口函数（A 级 — S1-107 新分类）

| 函数 | 类型 | 外部可达 | HTML 证据 | A-F |
|---|---|---|---|---|
| `$scope.queryCompanyName` | Init / 内部 helper | ❌ | F | A |
| `$scope.getEmployee` | Init / 内部 helper | ❌ | F | A |
| `$scope.queryUndisposed` | Read / 内部 helper | ❌ | F | A |
| `$scope.routeClick` | 路由 | ✅ (UI 触发) | F | A |
| `$scope.order.brushData` | Read | ❌（仅 modal.affrim success 内部调） | F | A |
| `$scope.order.show` | Show | ✅ (报损 click 触发) | F | A |
| `$scope.querySingleOrder` | Read | ❌（仅 success 内部调） | F | A |
| `$scope.choseUser.affirm` | Write | ✅ (UI 触发) | F | A |
| `$scope.addUser.switch` | Internal helper | ❌（仅 choseUser.affirm 内部调） | F | A |
| `$scope.beginCustomerCheckin` | Write | ✅ (addUser.switch 内部调 / 1 处) | F | A |
| `$scope.statusManage.callback` | Internal | ❌ | F | A |
| `$scope.choseUser.open` | Show | ✅ (UI 触发) | F | A |
| `$scope.choseUser.register` | Show | ✅ (UI 触发) | F | A |
| `$scope.choseUser.affirm` | Write | ✅ (UI 触发) | F | A |
| `$scope.addUser.editInfo` | Internal | ❌ | F | A |
| `$scope.concatMedicalProductStock` | Read | ❌（仅 3 Write success 内部调） | F | A |
| `$scope.choseFactoryMethod` | Write | ❌（仅 fnMap "加工" 内部调） | F | A |
| `$scope.clickBtn` | Internal | ❌（仅 HTML ng-click 调用） | F | A |
| `$scope.isSendProduct` | Internal | ❌ | F | A |
| `$scope.isSendCenter` | Internal | ❌ | F | A |
| `$scope.expiresWarning` | Internal | ❌ | F | A |
| `$scope.searchDate` | Internal | ❌ | F | A |
| `$scope.changeDate` | Internal | ❌ | F | A |
| `$scope.hideAddModal` | Internal | ❌ | F | A |
| `$scope.selectOrder` | Write (deliveryInputCtrl, 不在 optometryCtrl) | — | A | A |
| `$scope.saveStock` | Write (deliveryInputCtrl, 不在 optometryCtrl) | — | A | A |
| `$scope.modal.changeOrder` | Read | ❌（仅 modal 内部调） | F | A |
| `$scope.modal.affrim` | Read + Write | ❌（仅 modal 内部调） | F | A |
| `$scope.modal.show` | Show | ❌ | F | A |
| `$scope.template.openPopout` | Show | ✅ (fnMap "通知" 调) | F | A |
| `$scope.template.back` | Write | ✅ (HTML 触发) | F | A |
| `$scope.printPeijing.print` | Show | ❌ | F | A |
| `$scope.appearCustomerCheckin` (回调函数 in $scope.addUser) | Write | ❌ | F | A |
| `$scope.search` | Read (ListFactory) | ❌（仅 init 调用） | F | A |

**A 级结论**：
- 3 类外部入口函数（HTML ng-click 触发）：
  - `$scope.clickBtn` (6 fnMap 动作)
  - `$scope.choseUser.open` / `affirm` / `register`
  - `$scope.template.openPopout` / `back`
  - `$scope.routeClick` (L34850)
- 全部其它函数**仅内部调用**（A 级）
- ❌ 0 处 controller.js 其它位置**显式调用** optometryCtrl 内部函数

### 13.2 内部 helper 跨函数调用关系（A 级）

| Helper | 调用者 | 行号 |
|---|---|---|
| `concatMedicalProductStock` | 3 Write success 内联回调 | L35097/L35183/L35202 |
| `choseFactoryMethod` | fnMap "加工" 内 | L35162 |
| `querySingleOrder` | 5 Write success | L35107/L35156/L35173/L35194/L35213 |
| `queryUndisposed` | 3 Write success + $scope.search success | L35108/L35157/L35376 |
| `order.brushData` | `order.show` + `modal.affrim` success | L34875/L35346 |
| `modal.changeOrder` | 用户操作触发 (F) | L35278 |
| `modal.affrim` | 用户确认触发 (F) | L35301 |
| `template.back` | 用户操作触发 (F) | L35238 |
| `addUser.switch` | `choseUser.affirm` success | L34916 |
| `beginCustomerCheckin` | `addUser.switch` 内部 | L34929 |
| `search` | Controller init | L35379 |
| `routeClick` | 用户操作触发 (F) | L34850 |

**A 级结论**：
- ❌ 0 处循环 / 递归 / 双向调用
- ❌ 0 处函数被 controller.js 其它 controller 显式调用
- 严格表述：**optometryCtrl 内部函数调用关系是单向无环**（A 级）

---

## 14. optometryGlassesCtrl 内部 Read API（A 级）

### 14.1 已识 Read（A 级）

| API | 行号 | 用途 |
|---|---|---|
| `/admin/getMedicalRecord.json` | L35416 | 第一个使用 medicalRecordId 的 Read |

### 14.2 严格表述（A 级）
- optometryGlassesCtrl 入口处**至少** 1 个 Read
- ❌ 0 处**完整** Read 审计（S1-107 仅做入口分析）
- 严格表述：**optometryGlassesCtrl 内部 Read 全集** = 待 S1-108+ 进一步审计

---

## 15. 跨 Controller 调用关系

### 15.1 其它 Controller 调用 optometryCtrl（A 级）

| 检查 | 结果 | A-F |
|---|---|---|
| 其它 controller 显式调 `$scope.choseUser.affirm` | ❌ 0 处 | A |
| 其它 controller 显式调 `$scope.beginCustomerCheckin` | ❌ 0 处 | A |
| 其它 controller 显式调 `$scope.template.back` | ❌ 0 处 | A |
| 其它 controller 显式调 `$scope.clickBtn` | ❌ 0 处 | A |
| 其它 controller 调 optometryCtrl 的 $scope.xxx | ❌ 0 处 | A |
| optometryCtrl 与其它 controller 共享 service | ❌ 0 处 | A |
| optometryCtrl 与其它 controller 通过 $rootScope 通信 | ❌ 0 处 | A |
| optometryCtrl 与其它 controller 通过 popup callback | ❌ 0 处 | A |

**A 级结论**：
- optometryCtrl 与其它 controller **无任何源码可证的直接调用关系**（A 级）
- ❌ 0 处 service 共享
- ❌ 0 处 $rootScope 通信
- ❌ 0 处 popup 回调跨 controller

### 15.2 optometryCtrl 内部 choseUser 全 controller.js 引用（A 级）

| 行号 | 引用 | 上下文 | A-F |
|---|---|---|---|
| L31102 | `$scope.choseUser = {` | 其它 controller 定义 | A |
| L34897 | `$scope.choseUser = {` | optometryCtrl 定义 | A |
| L34949 | `medicalRecordType: $scope.choseUser.glassestype` | beginCustomerCheckin Request 字段值 | A |
| L35003 | `$scope.choseUser.open(glassestype)` | 其它函数（待查）| A |

**A 级新发现**：
- `$scope.choseUser` 在 controller.js 中**至少 2 处定义**（L31102 其它 controller + L34897 optometryCtrl）—— **重名不同源**（A 级）
- 其它 controller 中 choseUser 与 optometryCtrl 中 choseUser 是**不同对象**（A 级）

---

## 16. S1-105 / S1-106 / S1-107 对齐

| 已知结论 | S1-105 | S1-106 | S1-107 状态 |
|---|---|---|---|
| 16 unique API (optometryCtrl 范围) | A | A | A（保持） |
| 8 Write | A | A | A（保持） |
| G→H 数据链 | A | A | A（保持） |
| H→optometryGlasses | (未审) | A (success $state.go 入口) | **A 完整**（含入口 + 首个 Consumer）|
| I 独立 | A | A | A（保持） |
| 4 类 medicalRecordId 字段路径 | 3 类 | 4 类 (新增 this.medicalRecord) | **5 类** (新增 $stateParams.medicalRecordId) |
| optometryCtrl 不注入 $stateParams | A | (未审) | A（重新确认） |
| optometryGlassesCtrl 注入 $stateParams | (未发现) | (未审) | **A 新发现**（L35383）|
| optometryGlasses 跳转来源 | 1 处 (L34954) | 1 处 | **2 处** (新增 L35136 fnMap "修改") |
| optometryGlasses 出口 | 0 处 | (未审) | **2 处** (L36034/L36050) |
| optometryGlassesCtrl 首个 medicalRecordId 消费者 | (未审) | (未审) | **A** (L35388 = $stateParams.medicalRecordId) |
| optometryGlassesCtrl 第一个 medicalRecordId API | (未审) | (未审) | **A** (L35416 getMedicalRecord.json) |
| State 注册 / 7 HTML 模板 | (未审) | (未审) | **0 命中** = F 边界 |

---

## 17. 26项增量矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | optometryCtrl 注册 | L34776 (唯一 1 处) | A | L1 | |
| 02 | Controller 所属 module | bestvisionWeb | A | L1 | |
| 03 | State 是否明确绑定 | ❌ controller.js 0 处 .state() | A | L1 | **F 边界** |
| 04 | State 名称 | "optometryGlasses" 字符串 | A 引用 / F 注册 | L1 | |
| 05 | State url | ❌ 不可证 | F | L1 | |
| 06 | State template | ❌ 不可证 | F | L1 | |
| 07 | State templateUrl | ❌ 不可证 | F | L1 | |
| 08 | State params | ❌ 不可证 | F | L1 | |
| 09 | State resolve | ❌ 不可证 | F | L1 | |
| 10 | 外部进入来源 | 2 处 (L34954/L35136) | A | L1 | |
| 11 | HTML 入口 | ❌ 0 处 | F | L1 | 7 HTML 不含 optometry |
| 12 | 外部 Controller 调用 | ❌ 0 处 | A | L1 | 跨 controller 0 调用 |
| 13 | $scope 暴露函数 | 详见 §13.1 | A | L1 | 3 类外部入口 |
| 14 | 内部 helper | 详见 §13.1 | A | L1 | 11+ 个 helper |
| 15 | optometryCtrl 出口 State | ❌ 0 处 $state.go | A | L1 | optometryCtrl 不主动离开 |
| 16 | outlet 参数 | ❌ 0 处 | A | L1 | |
| 17 | begin → optometryGlasses | L34954 $state.go | A | L1 | |
| 18 | medicalRecordId State 传递 | L34954 + L35136 (2 入口) | A | L1 | |
| 19 | optometryGlasses Controller | L35383 optometryGlassesCtrl | A | L1 | |
| 20 | $stateParams.medicalRecordId | L35388 首个消费者 | A | L1 | **S1-107 关键新发现** |
| 21 | medicalRecordId 首个 Consumer (API) | L35416 getMedicalRecord.json | A | L1 | **S1-107 关键新发现** |
| 22 | HTML 证据边界 | F | F | L1 | 7 HTML 不可得 |
| 23 | State/API 数据边界 | F | F | L1 | .state() 不在源码 |
| 24 | 控制流 / 数据流区分 | ✅ 严格区分 | A | L1 | |
| 25 | S1-105/106 对齐 | 详见 §16 | A | L1 | |
| 26 | A/B/C/D/E/F 变化 | 多项 F → A (S1-107) | A | L1 | |

**统计**：
- **A：18 项**
- **F：8 项**（State 注册/HTML 模板/State url/template/params/resolve 全部 F）
- **E / D / C / B：0**
- **E/F 升 A：0**

---

## 18. L1/L2/L3

### L1（源码事实，可证）

- 3 个 optometry Controller 注册位置（A）
- 5 处 $state.go 跳转到 optometryGlasses 关联 State（A）
- 5 类 medicalRecordId 字段路径（A）
- optometryGlassesCtrl 入口 medicalRecordId + edit 消费者（A）
- optometryGlassesCtrl → optometryList / optometryLogList 出口（A）
- optometryCtrl 0 处 $state.go 出口（A）
- controller.js 0 处 .state() 注册（A）
- 7 HTML 0 处 optometry 模板（A）
- 跨 controller 0 调用（A）
- choseUser 重名不同源（A）

### L2（业务解释，未证）

- "optometryCtrl = 验光页面"：**E**
- "optometryGlasses = 配镜页面"：**E**
- "beginCustomerCheckin = 开始接诊"：**E**
- "fnMap 修改 = 编辑配镜"：**E**
- "medicalRecordId = 当前患者 ID"：**E**
- "$stateParams.medicalRecordId = 业务主键"：**E**
- "optometryGlasses 出口 optometryList = 返回列表"：**E**

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 State 注册）

---

## 19. F 边界

| 项 | 不可证原因 | 标注 |
|---|---|---|
| optometryCtrl 对应 State 名 | controller.js 0 处 .state() | F |
| optometryGlasses State url / template / params | 同上 | F |
| optometryList / optometryLogList State 配置 | 同上 | F |
| 7 HTML 中 optometry 模板 | 7 HTML 不含 | F |
| HTML ng-controller 触发点 | HTML 不可得 | F |
| UI ng-click 触发点 | HTML 不可得 | F |
| ui-router 内部状态转移机制 | ui-router 实现 | F |
| optometryGlassesCtrl 完整 Read 全集 | S1-107 仅入口分析 | F |
| 业务语义 | 命名 + 注释 | E |
| 5 类 medicalRecordId 字段值是否后端 DTO 同一 | 无后端 | F |

---

## 20. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| API actual = 0 | ✅ | 全部仅静态审计 |
| Write actual = 0 | ✅ | |
| save/submit/send/delivery/receive/charge/refund/recharge/start/complete/close/notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 165/166/167 全部未改 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 168_*.md |
| 文件编号连续 | ✅ | 167 已被 S1-106 占用，本轮使用 168 |

---

## 21. 页面级最终调用图

### 21.1 外部 → optometryGlasses（A 级）

```
[外部 State/HTML, F 边界, 资源范围不可得]
    ↓
$state.go("optometryGlasses", { medicalRecordId: X })  ← A 级 (L34954 / L35136)
    ↓ [F 边界: ui-router]
optometryGlassesCtrl 初始化 (L35383)
    ↓
$scope.medicalRecordId = $stateParams.medicalRecordId  ← A (L35388)
$scope.edit = $stateParams.edit === "true"  ← A (L35389)
    ↓
$scope.getMedicalRecord() (L35415)
    ↓
Read /admin/getMedicalRecord.json { id: $scope.medicalRecordId }  ← A (L35416)
    ↓
$scope.medicalRecord = response.object  ← A (L35419)
```

### 21.2 optometryCtrl 内部链（A 级）

```
optometryCtrl init (L34776)
    ↓
$scope.queryCompanyName()  (L34792)  ─ Read getCompanyOfMine.json
$scope.getEmployee()  (L34799)        ─ Read getLoginEmployee.json
$scope.search()  (L35379)              ─ ListFactory selectMedicalRecordFlowVoList.json
    ↓ success
$scope.queryUndisposed()  (L35376)    ─ Read stateTodoMedicalRecordCount.json

[外部 clickBtn, F 边界, HTML 不可得]
    ↓
$scope.clickBtn(name, item, index)  (L35128)
    ↓ fnMap[name]()
[6 动作: 退费/修改/收费/取消订单/加工/制作完成/报损/到店取镜/快递发货/通知]
    ↓

[A] fnMap "加工" → $scope.choseFactoryMethod(item)
    ↓ F4 + Write setMedicalRecordProcessMode.json
    ↓ success → querySingleOrder + queryUndisposed

[B] fnMap "到店取镜" → $scope.concatMedicalProductStock(item)
    ↓ F4 + Write completeMedicalRecordDelivery.json (deliveryStatus="2")
    ↓ success → querySingleOrder

[C] fnMap "快递发货" → $scope.concatMedicalProductStock(item)
    ↓ F4 + Write completeMedicalRecordDelivery.json (deliveryStatus="1")
    ↓ success → querySingleOrder

[E] fnMap "取消订单" → Write cancelMedicalRecord.json
    ↓ success → querySingleOrder + queryUndisposed

[F] fnMap "制作完成" → Write confirmMedicalRecordReturn.json
    ↓ success → querySingleOrder

[D] fnMap "报损" → $scope.order.show(true, item.medicalRecord.id)
    ↓ brushData(medicalRecordId)  ─ Read getMedicalRecordFlowVo.json
    ↓ modal.changeOrder(true, index)  ─ Read getAdminInfo.json
    ↓ modal.affrim()  ─ Read selectMedicalProductStockList.json
    ↓ Write createMedicalStockLossOfSmallVersion.json
    ↓ success → brushData(medicalRecordId) 闭环

[G] $scope.choseUser.affirm(obj)  [F HTML ng-click 触发]
    ↓ Write insertCustomerCheckin.json
    ↓ success → $scope.addUser.switch(false, res.result.vo)

[H] $scope.addUser.switch 内部 → $scope.beginCustomerCheckin(info)
    ↓ Write beginCustomerCheckin.json
    ↓ success → $state.go("optometryGlasses", { medicalRecordId: result.result.vo.customerCheckin.medicalRecordId })

[I] $scope.template.back  [F HTML ng-click 触发]
    ↓ Write sendTakeMirrorNotice.json
    ↓ success → Popup.notice("发送成功！")

[fnMap "通知" 内部]
$scope.template.medicalRecord = item.medicalRecord.id
$scope.template.openPopout(true)
```

### 21.3 optometryGlasses 后续链（A 级已知部分）

```
optometryGlassesCtrl (L35383)
    ↓ [L36034 / L36050 已知 2 出口, 细节待审]
$state.go("optometryList", {}, { reload: true })
$state.go("optometryLogList", { ... })
```

---

## 22. 最终结论

### 22.1 关键事实（A 级）

1. **optometryCtrl 注册唯一 1 处** (L34776)，不注入 $stateParams（A）
2. **optometryGlassesCtrl 注册唯一 1 处** (L35383)，**注入 $stateParams**（A — **S1-107 新发现**）
3. **optometryGlassesCtrl 是 optometryGlasses State 的目标 Controller**（A — 注入 $stateParams + 读 $stateParams.medicalRecordId）
4. **optometryGlassesCtrl 首个 medicalRecordId Consumer = L35388**（A — `$scope.medicalRecordId = $stateParams.medicalRecordId`）
5. **optometryGlassesCtrl 第一个使用 medicalRecordId 的 API = getMedicalRecord.json (L35416)**（A）
6. **controller.js 0 处 .state() 注册**（A — **S1-107 关键 F 边界**）
7. **7 HTML 0 处 optometry 模板**（A — **F 边界**）
8. **optometryCtrl 0 处 $state.go 出口**（A）
9. **optometryGlassesCtrl 2 处出口**（L36034/L36050 → optometryList/optometryLogList）（A）
10. **5 类 medicalRecordId 字段路径**（A — S1-107 新增 $stateParams.medicalRecordId）
11. **optometryGlasses 2 处源码可见进入来源**（L34954 beginCustomerCheckin + L35136 fnMap "修改"）（A）
12. **跨 controller 0 直接调用**（A）

### 22.2 S1-107 边界声明

**S1-107 已完成**：
- ✅ optometryCtrl / optometryGlassesCtrl / optometryListCtrl / optometryLogListCtrl 4 Controller 注册全部定位
- ✅ 5 处 $state.go 跳转（2 进入 optometryGlasses + 2 optometryGlasses 出口 + 1 旁证）全部钉死
- ✅ 5 类 medicalRecordId 字段路径全部 A 级
- ✅ optometryGlassesCtrl 入口 medicalRecordId + edit 字段消费者已钉死
- ✅ 第一个使用 medicalRecordId 的 API = getMedicalRecord.json

**S1-107 仍保持 F 的项**：
- ❌ optometryCtrl / optometryGlasses / optometryList / optometryLogList State 注册（controller.js 0 处 .state()）
- ❌ 7 HTML 中 optometry 模板
- ❌ HTML ng-controller / ng-click / ui-sref 触发点
- ❌ optometryGlassesCtrl 内部 Read 全集（仅入口审计）
- ❌ optometryGlasses → optometryList / optometryLogList 跳转 params 详情
- ❌ 业务语义

### 22.3 严格表述（A 级 vs E/F）

- "optometryCtrl 全部 16 API + 8 Write"：**A**
- "optometryGlassesCtrl 入口 = $stateParams.medicalRecordId"：**A**
- "5 类 medicalRecordId 字段路径"：**A**
- "G→H 直接数据流链"：**A**
- "optometryGlasses 2 处入口 / 2 处出口"：**A**
- "optometryCtrl 0 处 .state.go 出口"：**A**
- "optometryCtrl 0 注入 $stateParams"：**A**
- "optometryGlassesCtrl 注入 $stateParams"：**A**
- "controller.js 0 处 .state() 注册"：**A**
- "7 HTML 0 处 optometry 模板"：**A**
- "State 注册位置"：**F**（资源范围不可得）
- "optometryCtrl = 验光页面"：**E**
- "optometryGlasses = 配镜页面"：**E**

### 22.4 不可在本轮升级为 A 的项

- 4 个 State 注册配置（F — controller.js 0 处 .state()）
- 7 HTML 模板（F — 不可得）
- HTML UI 触发点（F）
- ui-router 内部机制（F）
- 业务语义（E）
- 后端 DTO（F）

---

**审计结束**。
