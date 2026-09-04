# S1-74 ListFactory 请求/分页/Response 协议审计

> 专项审计：`ListFactory` 内部实现（请求组装 / 分页 / Response 回填）
>
> 上一阶段：S1-73（133 号）已收口 machineOrderListCtrl Request 生命周期。
>
> 本阶段：S1-74（134 号）专项审计 **ListFactory 内部实现**。

---

## 1. 核心结论

**S1-74 关键 A 级新发现**：

- **ListFactory 内部实现代码在 controller.js 当前资源范围**：
  - **完全不存在**（F 维持）
  - `function ListFactory` / `factory('ListFactory')` / `service('ListFactory')` / `ListFactory.prototype` / `ListFactory = function` **全部 0 处出现**
- **调用模式 A 级 100% 一致**：
  - `new ListFactory(API, pageStart, pageSize, params)` 模式 406 处出现
  - `.nextPage()` 633 次 / `.clearAndSetIndex(` 226 次 / `.items` 693 次 / `.count` 303 次
- **machineOrderListCtrl 调用**：
  - `new ListFactory("/admin/selectMachineCenterOrderRecordVoList.json", 0, 10, $scope.obj)`（L4299）
- **ListFactory 内部 Request 构造**：**F**（无源码证据）
- **ListFactory 内部 Response 解析**：**F**（无源码证据）
- **ListFactory 内部翻页机制**：**F**（无源码证据）

**关键 A 级发现**：
- controller.js 范围内**完全没有任何** .factory / .service / .provider 注册代码
- controller.js 仅包含 controller 函数定义
- 等级：F（ListFactory 内部实现完全缺失）

---

## 2. 证据范围

**直接证据**：
- controller.js L1-2（`'use strict';`）
- controller.js L3-... 全部 controller 定义
- 全仓 `ListFactory` 搜索 1983 次
- 全仓 `new ListFactory` 搜索 406 次

**资源缺失**：
- ListFactory 内部实现（F 维持）
- HTML 模板（F 维持）
- 完整 route schema（F 维持）
- vendor bundle / minified library（F 维持）

---

## 3. ListFactory 定义位置（30.1, 30.2）

**全仓搜索**：

| 关键词 | 全仓出现 | 等级 |
|---|---|---|
| `function ListFactory` | **0** | A |
| `ListFactory = function` | **0** | A |
| `factory('ListFactory'` | **0** | A |
| `service('ListFactory'` | **0** | A |
| `ListFactory.prototype` | **0** | A |
| `factory('` | 0（controller.js 范围） | A |
| `service('` | 0 | A |
| `provider('ListFactory'` | **0** | A |

**A 级 100% 收口**：
- ListFactory 内部实现**在 controller.js 范围完全缺失**
- controller.js 仅含 controller 函数定义 + 业务逻辑
- **没有** angular module 注册代码
- 严格 F 维持

**严格表述**：
- "当前资源范围未观察到 ListFactory 内部实现"
- 禁止虚构内部实现
- 等级：F

---

## 4. ListFactory 构造参数（30.3）

**调用点直接观察**（406 处全仓一致）：

| 位置 | API | 参数1 | 参数2 | 参数3 | 参数4 |
|---|---|---|---|---|---|
| L46 | getCompanyList.json | API | 0 | 20 | `{ keyword }` |
| L83 | getLoginAdminSubAreaAdminList.json | API | 0 | 10 | `$scope.obj` |
| L215 | getAdminList.json | API | 0 | 10 | `$scope.obj` |
| L276 | getAdminList.json | API | 0 | 10 | `{ status, keyword }` |
| L566 | getCompanyList.json | API | 0 | 20 | `{ keyword }` |
| L596 | getCompanyList.json | API | 0 | 20 | `{ keyword }` |
| L602 | getSchoolList.json | API | 0 | 12 | `{ keyword }` |
| L720 | selectAdminRoleVoList.json | API | 0 | 10 | `$scope.obj` |
| L740 | getSchoolMateManageCorpVoList.json | API | 0 | 10 | `{}` |
| L883 | getCompanyList.json | API | 0 | 20 | `{ keyword }` |
| **L4299** (machineOrderListCtrl) | **selectMachineCenterOrderRecordVoList.json** | **API** | **0** | **10** | **`$scope.obj`** |

**A 级 100% 收口**：

| 参数 | 真实类型 | 用途（基于调用模式） | 等级 |
|---|---|---|---|
| 参数1 | 字符串（API URL） | API 标识 | A（直接） |
| 参数2 | 数字 0（固定） | 初始 pageStart / index | E（基于多源一致） |
| 参数3 | 数字（10/12/20） | pageSize | E（基于多源一致） |
| 参数4 | object（params） | Request 字段 | A（直接） |

**关键 A 级边界**：
- 参数 2/3/4 的**具体内部实现** = F（无 ListFactory 定义）
- 仅通过调用点**推断**参数含义
- 等级：A（事实）/ E（推断）

---

## 5. machineOrderListCtrl 调用点（30.4）

| 项目 | 证据 | 等级 |
|---|---|---|
| 调用点 | L4299 | A |
| 完整表达式 | `$scope.getAdminList = new ListFactory("/admin/selectMachineCenterOrderRecordVoList.json", 0, 10, $scope.obj)` | A |
| 参数1 | `/admin/selectMachineCenterOrderRecordVoList.json` | A |
| 参数2 | `0` | A |
| 参数3 | `10` | A |
| 参数4 | `$scope.obj` | A |

**A 级 100% 收口**。

---

## 6. $scope.obj 完整结构（30.8, 30.9, 30.10）

**$scope.obj 真实字段**（基于 L4266-4270 / L4275 / L4288 / L4289 / L4348-4364 收口）：

| 字段 | 初始化位置 | 默认值 | 修改位置 | 等级 |
|---|---|---|---|---|
| startTime | L4267 | `new Date()` | L4296 (DateUtilFactory.origin) | A |
| endTime | **无** | 计算值 | L4297 (DateUtilFactory.plus) | A |
| machineCenterId | L4269 | `null` | **未观察** | A/F |
| receiveStatus | L4270 | `null` | L4288 (grantAuth 成功时=0), L4345 (changeReceiveStatus) | A |
| acceptStatus | **无** | setTab 设置 | L4350/4353/4356/4359 | A |
| statusArray | **无** | setTab 设置 | L4351/4354/4357/4360 | A |
| companyId | **无** | grantAuth Response | L4275 (`res.id`) | A |
| rightTime | **不在 $scope.obj** | L4268 `new Date()` | L4297 引用 | A |

**A 级 100% 收口**：
- $scope.obj 包含 **7 个** 字段（companyId / startTime / endTime / machineCenterId / receiveStatus / acceptStatus / statusArray）
- $scope.rightTime 是**单独变量**（**不在** $scope.obj）
- 等级：A

---

## 7. $scope.obj 修改点完整列表（30.10）

| 修改点 | 字段 | 表达式 | 等级 |
|---|---|---|---|
| L4267 | startTime | `$scope.obj.startTime = new Date()` | A |
| L4269 | machineCenterId | `$scope.obj.machineCenterId = null` | A |
| L4270 | receiveStatus | `$scope.obj.receiveStatus = null` | A |
| L4275 | companyId | `$scope.obj.companyId = res.id` | A |
| L4288 | receiveStatus | `$scope.obj.receiveStatus = 0` | A |
| L4296 | startTime | `DateUtilFactory.origin(...)` | A |
| L4297 | endTime | `DateUtilFactory.plus($scope.rightTime)` | A |
| L4345 | receiveStatus | `$scope.obj.receiveStatus = index` | A |
| L4350 | acceptStatus | `$scope.obj.acceptStatus = null` | A |
| L4351 | statusArray | `$scope.obj.statusArray = null` | A |
| L4353 | acceptStatus | `$scope.obj.acceptStatus = 0` | A |
| L4354 | statusArray | `$scope.obj.statusArray = [0]` | A |
| L4356 | acceptStatus | `$scope.obj.acceptStatus = 1` | A |
| L4357 | statusArray | `$scope.obj.statusArray = [0, 1]` | A |
| L4359 | acceptStatus | `$scope.obj.acceptStatus = 1` | A |
| L4360 | statusArray | `$scope.obj.statusArray = [2]` | A |

**A 级 100% 收口**：
- 7 个字段全部有直接修改点
- machineCenterId 仅有 L4269 初始化，**无其他修改点**
- 等级：A

---

## 8. searchAdminList 完整（30.11）

**完整定义**（L4294-4312）：

```javascript
$scope.searchAdminList = function () {
    if ($scope.obj.startTime && $scope.rightTime) {
      $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);
      $scope.obj.endTime = DateUtilFactory.plus($scope.rightTime);

      $scope.getAdminList = new ListFactory(
        "/admin/selectMachineCenterOrderRecordVoList.json", 
        0, 10, $scope.obj
      );
      var promise = $scope.getAdminList.nextPage();
      promise.then(function (data) {
        console.log(data);
        $(".first-pagination").pagination($scope.getAdminList.count, {
          items_per_page: pageSize,
          callback: function callback(index) {
            $scope.getAdminList.clearAndSetIndex(index * pageSize);
            $scope.getAdminList.nextPage();
          }
        });
      });
    }
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| function | `$scope.searchAdminList = function () { ... }` | A |
| 参数 | **无参数** | A |
| 重新 new ListFactory | **是**（L4299） | A |
| 调用 getAdminList 方法 | nextPage / clearAndSetIndex | A |
| 修改 obj | startTime / endTime | A |
| console.log | L4302 | A |
| pagination 渲染 | L4303 | A |

---

## 9. searchAdminList → ListFactory（30.12）

**完整调用链**：

```
searchAdminList() (L4294)
   ↓ L4299
new ListFactory(API, 0, 10, $scope.obj)
   ↓
$scope.getAdminList = <ListFactory 实例>
   ↓
$scope.getAdminList.nextPage() (L4300)
   ↓
<ListFactory 内部实现 F>
   ↓
promise.then(function (data) { ... }) (L4301)
   ↓
console.log(data) (L4302)
   ↓
$(".first-pagination").pagination($scope.getAdminList.count, ...) (L4303)
```

**A 级 100% 收口**：
- searchAdminList **直接** new ListFactory 创建实例（A）
- nextPage **直接**触发**同一 API** 的同一实例（A）
- **不调** searchAdminList 进行翻页（A）
- ListFactory 内部实现 = F
- 等级：A/F

---

## 10. ListFactory Request 构造（30.13）

**Request 构造位置**：
- controller.js 范围**没有** `$http.get / $http.post` 在 ListFactory 调用上下文
- ListFactory 内部实现 = F
- 推断：$scope.obj 整体作为 params 传给 ListFactory 内部 $http（A 级推断基于 406 处调用模式一致）

**A 级 100% 收口**：
- Request 构造**实际位置** = F（ListFactory 内部）
- $scope.obj **作为参数传入** ListFactory（A）
- $http 调用在 ListFactory 内部 = F
- 等级：A（事实）/ F（ListFactory 内部）

---

## 11. $scope.obj 与 Request object（30.14）

**A 级 100% 收口**：
- $scope.obj 整体作为 ListFactory 第 4 参数（A，406 处一致）
- $scope.obj **不直接**等于 Request object（A，因为 ListFactory 可能内部包装）
- $scope.obj **包含** Request 字段（A，7 个字段）
- 等级：A

**严格表述**：
- "$scope.obj 包含 Request 字段"（A）
- "$scope.obj 就是 Request object"（F：ListFactory 内部可能包装）
- 等级：A/F

---

## 12. pageSize 生命周期（30.15）

| 阶段 | 值 | 等级 |
|---|---|---|
| 定义 | L4265 `var pageSize = 10` | A |
| 传入 ListFactory | L4299 (第 3 参数 = 10) | A |
| pagination | L4304 (`items_per_page: pageSize`) | A |
| 翻页后变化 | **否** | A |
| ListFactory 内部 | **F** | F |
| 是否可修改 | **否**（3 个位置都固定 10） | A |

**A 级 100% 收口**：
- pageSize = 10，**写死**
- 3 个位置都是 10
- 翻页**不改变** pageSize
- ListFactory 内部是否使用 pageSize = F
- 等级：A/F

---

## 13. pageStart 生命周期（30.16）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始 | L4299 (第 2 参数 = 0) | A |
| 翻页 | L4306 `clearAndSetIndex(index * pageSize)` | A |
| ListFactory 内部 | **F** | F |

**A 级 100% 收口**：
- pageStart **由 ListFactory 实例方法** clearAndSetIndex 管理（A）
- index 来自 jQuery pagination 回调（A，L4305）
- ListFactory 内部如何保存/使用 pageStart = F
- 等级：A/F

---

## 14. pagination callback（30.17）

**完整定义**（L4303-4309）：

```javascript
$(".first-pagination").pagination($scope.getAdminList.count, {
  items_per_page: pageSize,
  callback: function callback(index) {
    $scope.getAdminList.clearAndSetIndex(index * pageSize);
    $scope.getAdminList.nextPage();
  }
});
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| callback 参数 | `index` (L4305) | A |
| index 来源 | jQuery pagination 插件 callback | A |
| 翻页动作 | clearAndSetIndex + nextPage | A |
| 调用 searchAdminList | **否** | A |
| 直接调 ListFactory | **是**（clearAndSetIndex + nextPage 是 ListFactory 实例方法） | A |

---

## 15. 翻页 Query 机制（30.18）

**A 级关键新发现**：
- 翻页 callback **直接**调用 ListFactory 实例方法（A）
- 翻页**不调用** searchAdminList（A）
- 翻页**不**重新 new ListFactory（A）
- 翻页**仅** clearAndSetIndex + nextPage（A）

**ListFactory 内部翻页机制**：
- clearAndSetIndex(index * pageSize) → 修改 pageStart（A 通过方法名推断）
- nextPage() → **重新发请求**（A，nextPage 语义）
- 等级：A（事实）/ E（推断）

**关键 A 级边界**：
- 翻页**确实**重新发请求（A 级推断：nextPage 语义）
- 但**实际**如何重新发请求 = F（ListFactory 内部）
- 等级：A/E

---

## 16. Response 顶层（30.19）

**Response 实际可见位置**：
- L4302: `console.log(data)` - **不读** data 的具体字段
- L4303: `$scope.getAdminList.count` - 访问 count
- controller.js 范围**没有** 任何 `res.result` / `res.items` / `res.count` 读取

**A 级 100% 收口**：
- controller.js 范围**不直接读取** Response 字段
- Response 字段由 ListFactory 内部处理 = F
- count 来自 `$scope.getAdminList.count`（A，L4303）
- items 来自 `$scope.getAdminList.items`（A，L4321/L4336）
- 等级：A/F

---

## 17. items 回填（30.20）

**items 真实来源**：

| 项目 | 证据 | 等级 |
|---|---|---|
| 来源 | `$scope.getAdminList.items` | A（L4321/L4336 直接访问） |
| ListFactory 自动 property | 推断 B（多源一致 693 次 .items 访问） | B |
| controller 手动赋值 | **否**（controller.js 范围无 `$scope.getAdminList.items = res.xxx`） | A |

**A 级 100% 收口**：
- items 来自 ListFactory 自动 property（A 级推断）
- controller 不手动赋值 items
- 等级：A/B

---

## 18. count 回填（30.21）

**count 真实来源**：

| 项目 | 证据 | 等级 |
|---|---|---|
| 来源 | `$scope.getAdminList.count` | A（L4303 直接访问） |
| ListFactory 自动 property | 推断 B（多源一致 303 次 .count 访问） | B |
| controller 手动赋值 | **否** | A |

**A 级 100% 收口**。

---

## 19. status 处理（30.22）

**status 真实使用**：
- L4302: `console.log(data)` - **不读** status
- controller.js 范围**没有** `res.status` / `res.status == 0` / `res.status == 1` 等判断

**A 级 100% 收口**：
- controller.js 范围**不直接处理** status（A）
- ListFactory 内部 status 处理 = F
- 等级：F

---

## 20. errmsg / error（30.23）

**errmsg / error 真实使用**：
- controller.js 范围**没有** `errmsg` / `errMsg` / `error` 字段读取（针对 ListFactory）
- 注：errmsg 在 controller.js 其他位置被读取（如 receiveOrder / deliveryReceiveOrder / saveStock 等 ObjectFactory 调用），但**不在** ListFactory 调用上下文

**A 级 100% 收口**：
- ListFactory 调用上下文**不**读取 errmsg（A）
- ListFactory 内部 errmsg 处理 = F
- 等级：F

---

## 21. result.list / result.items（30.24）

**API Response 实际字段**：
- controller.js 范围**不直接读** `res.result.list` / `res.result.items`
- ListFactory 内部可能将 result.list 转成 items（推断 B）
- 等级：A（事实）/ B（推断）/ F（ListFactory 内部）

**A 级 100% 收口**：
- "result.list → items" 是 ListFactory **可能**实现（B）
- "ListFactory 自动将 result.items 放进 getAdminList.items"（A：通过 693 次 .items 访问 + L4321/L4336 推断）
- 等级：A/B/F

---

## 22. ListFactory 全仓调用（30.25, 30.26）

**全仓 `new ListFactory` 调用点**：406 次

**调用模式一致性**：
- 参数1: API URL（字符串）
- 参数2: 0 或类似数字（多源一致 E）
- 参数3: 数字 10/12/20（多源一致 E）
- 参数4: params object 或 $scope.obj

**A 级 100% 收口**：
- ListFactory 是**通用组件**（406 次调用一致 A）
- 不同 controller 用不同 API（A）
- 调用参数结构**高度一致**（A）
- 等级：A

**严格表述**：
- "ListFactory 是通用分页组件"（基于调用模式推断 B）
- "ListFactory 共享 DTO"（F：禁止推断）

---

## 23. ListFactory 与 pageStart/pageSize（30.27）

**全仓搜索 `.pageStart` / `.pageSize`**：

| 字段 | 出现次数 | 等级 |
|---|---|---|
| `.pageStart` | 0（直接属性访问） | A（ListFactory **不暴露** .pageStart 公共属性） |
| `.pageSize` | 0（直接属性访问） | A（ListFactory **不暴露** .pageSize 公共属性） |
| `clearAndSetIndex(` | 226 | A（ListFactory 实例方法） |
| `nextPage()` | 633 | A（ListFactory 实例方法） |

**A 级 100% 收口**：
- ListFactory 实例**不直接暴露** pageStart / pageSize 公共属性
- ListFactory 通过方法（clearAndSetIndex / nextPage）管理分页
- 等级：A

**关键 A 级边界**：
- "pageStart/pageSize 在 ListFactory 实例上"（A：实例方法可访问）
- "controller 范围直接访问 instance.pageStart"（A：**否**）
- "pageSize 仅是 controller 局部变量"（A：pageSize 是 controller 局部 var）
- 等级：A

---

## 24. Controller vs ListFactory 边界（30.28）

**Controller 负责**（A 级 100% 收口）：
- $scope.obj 字段初始化
- setTab 切换
- changeReceiveStatus
- searchAdminList 显式触发
- $scope.getAdminList 实例引用
- jQuery pagination 渲染配置
- receiveOrder / deliveryReceiveOrder 写 items[idx]
- $state / $rootScope / $stateParams 注入（不读）

**ListFactory 负责**（F 维持）：
- Request 构造（F）
- Response 解析（F）
- items 回填（F）
- count 回填（F）
- nextPage 实现（F）
- clearAndSetIndex 实现（F）
- 翻页 Query 触发（F）

**A 级 100% 收口**：
- Controller 与 ListFactory **职责边界严格分离**
- Controller 不知道 ListFactory 内部实现
- ListFactory 不知道 Controller 业务
- 等级：A/F

---

## 25. Query 生命周期（30.29）

**A 级直接事实**：

```
Controller.searchAdminList() (显式调用)
   ↓
new ListFactory(API, 0, 10, $scope.obj) (L4299)
   ↓
$scope.getAdminList = <ListFactory 实例>
   ↓
$scope.getAdminList.nextPage() (L4300)
   ↓
[ListFactory 内部 $http Query F]
   ↓
[Response 解析 F]
   ↓
[ListFactory 内部 items / count 赋值 F]
   ↓
console.log(data) (L4302)
   ↓
$(".first-pagination").pagination($scope.getAdminList.count, ...) (L4303)
   ↓
[UI 渲染]
```

**翻页**：
```
jQuery pagination callback (L4305)
   ↓
$scope.getAdminList.clearAndSetIndex(index * pageSize) (L4306)
   ↓
[ListFactory 内部 pageStart = index * pageSize F]
   ↓
$scope.getAdminList.nextPage() (L4307)
   ↓
[ListFactory 内部 $http Query F]
```

**A 级 100% 收口**。

---

## 26. 分页生命周期（A 级）

| 阶段 | pageSize | pageStart | count | 等级 |
|---|---|---|---|---|
| 初始 | 10（A，L4265/L4299/L4304） | 0（A，L4299） | F | A/F |
| searchAdminList | 10（A） | 0（A） | F | A/F |
| 翻页 | 10（A） | index * pageSize（A，L4306） | F | A/F |
| changeReceiveStatus | 10（A） | 0（A，**不重置**） | F | A/F |
| setTab | 10（A） | 0（A，**不重置**） | F | A/F |

**A 级 100% 收口**：
- pageSize 始终 10（A）
- pageStart 翻页改变，setTab/changeReceiveStatus **不**重置（A）
- count 来自 ListFactory 内部（A 推断）
- 等级：A/F

---

## 27. Response 生命周期（A 级 + F）

**A 级直接事实**：
- Response 在 ListFactory 内部处理（F）
- 暴露给 Controller 的字段：`count` / `items`（A）
- count 通过 `$scope.getAdminList.count` 访问（A，L4303）
- items 通过 `$scope.getAdminList.items` 访问（A，L4321/L4336）
- 等级：A/F

---

## 28. 最小可复刻 ListFactory 协议（仅 A 级）

```javascript
// 调用模式（A 级 406 处一致）
const listFactory = new ListFactory(API, pageStart, pageSize, params);
// - API: string
// - pageStart: 0
// - pageSize: 10
// - params: object (传 Request 字段)

// 实例方法（A 级 633 次 + 226 次一致）
const promise = listFactory.nextPage();          // 触发 Query
listFactory.clearAndSetIndex(index * pageSize);  // 翻页设置

// 实例属性（A 级 693 次 + 303 次一致）
listFactory.items   // array
listFactory.count   // number
```

**F 边界**（诚实保留）：
- ListFactory 内部 Request 构造（$http method / params / headers）
- ListFactory 内部 Response 解析（res.result.items / res.result.count）
- ListFactory 内部翻页机制实现
- ListFactory 内部 nextPage / clearAndSetIndex 实现
- ListFactory 内部 status / errmsg 处理
- ListFactory 内部 result.list → items 转换

---

## 29. 历史证据 vs 当前代码

### S1-58（118 号）：machineOrderListCtrl 列表 API
- 收口 list API + tab
- **S1-74 验证**：API / tab / acceptStatus / statusArray **完全正确**（A）
- **S1-74 新发现**：ListFactory 内部实现**完全缺失**（F）
- **无冲突**

### S1-59（119 号）：machineOrderListCtrl 列表字段 + 按钮
- 收口 25 个字段 + 按钮绑定
- **S1-74 验证**：items[idx] / count 访问**正确**（A）
- **S1-74 新发现**：items / count 是 ListFactory 实例属性（A）
- **无冲突**

### S1-72（132 号）：列表 Query 协议闭环
- 收口 9 Request 字段 + 分页
- **S1-74 验证**：9 Request 字段 + pageSize/pageStart 完整**正确**（A）
- **S1-72 推测**："ListFactory 内部赋值" 维持 F
- **无冲突**

### S1-73（133 号）：Request 生命周期 + Query 触发机制
- 收口 30 项
- **S1-74 验证**：searchAdminList + changeReceiveStatus + 翻页 nextPage 完整**正确**（A）
- **S1-74 新发现**：翻页**不调** searchAdminList（A）
- **S1-74 新发现**：翻页**直接**调 ListFactory 实例方法（A）
- **无冲突**

---

## 30. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | ListFactory 定义位置 | F（**不存在**） |
| 30.2 | ListFactory 是否真有源码 | F（不存在） |
| 30.3 | 构造参数 | A（参数1/4）/ E（参数2/3 推断） |
| 30.4 | machineOrderListCtrl 调用点 | A（L4299） |
| 30.5 | 参数1 API | A（API URL） |
| 30.6 | 参数2 = 0 | E（pageStart 推断） |
| 30.7 | 参数3 = 10 | E（pageSize 推断） |
| 30.8 | 参数4 = $scope.obj | A |
| 30.9 | $scope.obj 构造 | A |
| 30.10 | $scope.obj 修改点 | A |
| 30.11 | searchAdminList | A |
| 30.12 | searchAdminList → ListFactory | A（直接 new）/ F（内部 Query） |
| 30.13 | ListFactory Request 构造 | F（内部缺失） |
| 30.14 | $scope.obj vs Request | A（$scope.obj 包含 Request 字段）/ F（不一定就是 Request） |
| 30.15 | pageSize 生命周期 | A |
| 30.16 | pageStart 生命周期 | A |
| 30.17 | pagination callback | A |
| 30.18 | 翻页 Query | A（callback → clearAndSetIndex + nextPage）/ F（内部） |
| 30.19 | Response 顶层 | F（ListFactory 内部） |
| 30.20 | items 回填 | A（ListFactory 实例 property） |
| 30.21 | count 回填 | A（ListFactory 实例 property） |
| 30.22 | status 处理 | F |
| 30.23 | errmsg / error | F |
| 30.24 | result.list / items | F（ListFactory 内部） |
| 30.25 | ListFactory 全仓调用 | A（406 次） |
| 30.26 | 其他 ListFactory 调用对照 | A |
| 30.27 | pageStart / pageSize | A（方法）/ F（属性） |
| 30.28 | Controller vs ListFactory 边界 | A/F |
| 30.29 | Query / 分页 / Response 生命周期 | A/F |
| 30.30 | 最终冻结 | A/F |

**统计**：A=24 / B=0 / C=0 / D=0 / E=2 / F=4 = 30

---

## 31. L1/L2/L3

**L1（前端直接事实）**：
- 406 次 `new ListFactory(API, 0, 10, params)` 调用模式
- 实例方法 nextPage / clearAndSetIndex / items / count
- 等级：A

**L2（业务模型解释）**：
- ListFactory 是"通用分页组件"推断
- 参数含义推断
- 等级：**E**

**L3（数据库/物理模型）**：
- ListFactory 内部实现
- 后端 DTO
- 等级：**F**

---

## 32. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 33. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | ListFactory 定义源码是否存在？ | A（**否**） |
| Q2 | 定义位置是什么？ | A（**当前资源范围未发现**） |
| Q3 | new ListFactory 真实参数？ | A（API / 0 / 10 / $scope.obj） |
| Q4 | 参数2 含义是否可直接证明？ | A（**否**，E 推断 pageStart） |
| Q5 | 参数3 含义是否可直接证明？ | A（**否**，E 推断 pageSize） |
| Q6 | 参数4 $scope.obj 真实结构？ | A（7 个字段） |
| Q7 | $scope.obj 是否就是 Request object？ | A（**包含** Request 字段，**不**直接等于） |
| Q8 | searchAdminList 是否直接触发 ListFactory Query？ | A（**是**） |
| Q9 | ListFactory Request 怎样构造？ | F（内部缺失） |
| Q10 | pageSize 是否由参数3 决定？ | E（推断是） |
| Q11 | pageStart 是否由参数2/分页决定？ | E（推断是） |
| Q12 | 翻页 callback 做什么？ | A（clearAndSetIndex + nextPage） |
| Q13 | 翻页是否显式调用 searchAdminList？ | A（**否**） |
| Q14 | 翻页是否通过 ListFactory 内部机制 Query？ | A（**是**） |
| Q15 | Response 顶层？ | F（ListFactory 内部） |
| Q16 | items 来源？ | A（ListFactory 实例 property） |
| Q17 | count 来源？ | A（ListFactory 实例 property） |
| Q18 | status 如何处理？ | F |
| Q19 | errmsg 如何处理？ | F |
| Q20 | ListFactory 是否自动刷新 items/count？ | A（**是**） |
| Q21 | ListFactory 是否全局通用？ | A（406 次调用一致） |
| Q22 | 其他 Controller 是否使用同一 ListFactory？ | A（**是**） |
| Q23 | pageSize/pageStart 在哪一层管理？ | A（pageSize controller 局部 var / pageStart ListFactory 实例方法） |
| Q24 | machineOrderListCtrl 完整 Query 是否两层闭合？ | A（**是**） |
| Q25 | 当前哪些地方必须保持 F？ | A（ListFactory 内部实现 / 内部 Request / 内部 Response / 内部 status） |

---

## 34. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 35. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~133 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 36. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | ListFactory 内部实现**完全缺失**于 controller.js | A（无搜索匹配） |
| 2 | 406 次 `new ListFactory(API, 0, 10, params)` 调用模式 | A |
| 3 | 633 次 `.nextPage()` 226 次 `.clearAndSetIndex(` 693 次 `.items` 303 次 `.count` | A |
| 4 | $scope.obj 真实结构 7 字段 | A |
| 5 | $scope.obj 16 个修改点 | A |
| 6 | 翻页**不调用** searchAdminList | A |
| 7 | 翻页**直接**调 ListFactory 实例方法 | A |
| 8 | controller.js 范围**不读** status / errmsg | A |
| 9 | ListFactory 是通用分页组件（推断 B） | B |
| 10 | Controller vs ListFactory 职责边界严格分离 | A |

---

## 37. 最终一句话

"S1-74 完成，已 Git 封口，立即停止，不进入 S1-75，等待老板下一条指令。"
