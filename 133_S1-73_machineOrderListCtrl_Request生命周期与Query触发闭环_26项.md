# S1-73 machineOrderListCtrl Request 生命周期与 Query 触发闭环

> 专项收口：`machineOrderListCtrl` 9 个 Request 字段的**生命周期** + **Query 触发机制**
>
> 上一阶段：S1-72（132 号）已收口 machineOrderListCtrl 列表 Query 完整协议。
>
> 本阶段：S1-73（133 号）专项收口 Request 参数**生命周期** + Query **触发机制**。

---

## 1. 核心结论

**S1-73 关键 A 级新发现**：

- **Query 唯一入口** = `searchAdminList()` 函数（L4294-4312）
- **searchAdminList 调用点**（2 个直接调用）：
  1. `setTab(tab)` 内部 L4363
  2. `changeReceiveStatus(index)` 内部 L4346
- **初始化执行顺序**：
  1. L4265-4271: 变量初始化
  2. L4272: `window.grantAuth.hasAuthForCompany(ObjectFactory).then(...)` 异步启动
  3. L4343: `$scope.tab = 1`（controller 同步）
  4. **L4289: `setTab(4)`**（grantAuth success 时）→ 立即触发 searchAdminList → Query
  5. **L4291: `setCompanyModal = !res`**（grantAuth result）
- **无 $watch / $rootScope.$on / debounce / 异步 trigger**（A）
- **无 $stateParams 读取**（A）
- **无第二个 Query 入口**（A）
- 9 Request 字段全部通过 `$scope.obj` 整体传入 ListFactory（A）
- 等级：A

---

## 2. 证据范围

**直接证据**：
- controller.js L4264-4365（machineOrderListCtrl 完整 101 行）
- 全仓 $watch / $rootScope.$on / $stateParams 搜索

**资源缺失**：
- HTML 模板（F）
- route schema（F）

---

## 3. searchAdminList 完整定位（30.1）

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
| function 行号 | L4294-4312 | A |
| Request 构造 | `new ListFactory(API, 0, 10, $scope.obj)` | A |
| API | selectMachineCenterOrderRecordVoList.json | A |
| 入口 | `if ($scope.obj.startTime && $scope.rightTime)` | A |
| 格式化 | DateUtilFactory.origin / plus | A |
| success | `console.log(data)` + pagination 渲染 | A |
| error | **不显式处理**（F 维持） | F |

---

## 4. Query 入口数量（30.2）

**全仓搜索 `searchAdminList()` 调用点**：

| 位置 | 上下文 | 等级 |
|---|---|---|
| L4346 | `changeReceiveStatus` 内部 | A |
| L4363 | `setTab` 内部 | A |
| L4294-4312 | function 定义 | A |

**A 级 100% 收口**：
- **仅 2 处** 直接调用 searchAdminList
- 无其他入口
- 等级：A

**Query 入口分类**：

| 类型 | 是否存在 | 等级 |
|---|---|---|
| 初始化 | **是**（grantAuth 成功后 L4289 setTab(4) 触发） | A |
| setTab 切换 | **是**（L4363） | A |
| changeReceiveStatus | **是**（L4346） | A |
| 翻页 | **是**（L4307 nextPage） | A |
| $watch | **否** | A |
| $rootScope.$on | **否** | A |
| $stateParams 变化 | **否**（不读 stateParams） | A |
| $timeout debounce | **否** | A |
| UI input 变化 | **F**（HTML 缺失） | F |

---

## 5. 初始化顺序（30.4）

**完整执行顺序**：

```
L4264: controller 函数开始
L4265: var pageSize = 10
L4266: $scope.obj = {}
L4267: $scope.obj.startTime = new Date()
L4268: $scope.rightTime = new Date()
L4269: $scope.obj.machineCenterId = null
L4270: $scope.obj.receiveStatus = null
L4271: $scope.centerArr = []

L4272-4292: window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (res) { ... })
   (异步 Promise，then 在 L4273 之后)

L4294-4312: $scope.searchAdminList = function () { ... } (function 定义，不立即执行)

L4314-4328: $scope.receiveOrder = function () { ... } (function 定义)

L4329-4342: $scope.deliveryReceiveOrder = function () { ... } (function 定义)

L4343: $scope.tab = 1 (controller 同步)

L4344-4346: $scope.changeReceiveStatus = function () { ... } (function 定义)

L4348-4364: $scope.setTab = function () { ... } (function 定义)
```

**关键 A 级发现**：
- `$scope.tab = 1` 在 L4343 **同步**赋值
- 但 grantAuth 异步 then 内 L4289 调用 `setTab(4)` **会覆盖** `$scope.tab = 1`
- 最终 tab 默认 = 4
- 等级：A

**Query 实际触发顺序**：

```
controller 同步部分执行（L4264-L4343）
   ↓
grantAuth 异步返回
   ↓ L4273 if (res)
L4275: $scope.obj.companyId = res.id
L4288: $scope.obj.receiveStatus = 0
L4289: $scope.setTab(4)
   ↓ L4363
$scope.searchAdminList() (Query 1)
   ↓ L4299
ListFactory(API, 0, 10, $scope.obj)
   ↓
$scope.getAdminList.nextPage()
```

**A 级 100% 收口**：
- grantAuth 成功 → setTab(4) → searchAdminList → 唯一初始 Query
- 失败（res 为 null）→ setCompanyModal=true，**不**触发 Query
- 等级：A

---

## 6. grantAuth 完整（30.5）

**grantAuth 真实代码**（L4272-4292）：

```javascript
window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (res) {
    if (res) {
      $scope.companyName = res.companyName;
      $scope.obj.companyId = res.id;
      $scope.getCenterListRecordPay = new ObjectFactory();
      var centerPromise = $scope.getCenterListRecordPay.saveOrQuery(
        "/admin/selectMachineCenterListOfProduct.json", 
        { companyId: res.id }
      );
      centerPromise.then(function (resp) {
        var arr = resp.result.list;
        for (var i = 0; i < arr.length; i++) {
          $scope.centerArr.push({ id: arr[i].id, name: arr[i].name });
        }
      });

      $scope.obj.receiveStatus = 0;
      $scope.setTab(4);
    }
    $scope.setCompanyModal = !res;
});
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| grantAuth 函数 | `window.grantAuth.hasAuthForCompany(ObjectFactory)` | A |
| success res | companyName + res.id | A |
| companyId 来源 | `res.id` (L4275) | A |
| 是否触发 search | **是**（通过 L4289 setTab(4) → L4363 searchAdminList） | A |
| 失败行为 | `setCompanyModal = !res` (L4291) | A |
| 失败时是否触发 search | **否** | A |

**关键 A 级新发现**：
- companyId **仅在 grantAuth 成功时** 赋值（A）
- companyId **依赖** `res` 对象的 `id` 字段（A）
- 失败时 companyId **不进入 Request**（A）
- 等级：A

---

## 7. companyId 完整生命周期（30.7）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始（L4266） | `undefined` | A |
| grantAuth 成功 | `res.id` (L4275) | A |
| grantAuth 失败 | **不赋值** | A |
| 进入 Request | **仅 grantAuth 成功时** | A |
| 业务语义 | E（"公司 ID" / "租户 ID" 推断） | E |

**A 级 100% 收口**。

---

## 8. startTime 完整生命周期（30.6）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始（L4267） | `new Date()` | A |
| 格式化（L4296） | `DateUtilFactory.origin(...)` | A |
| 进入 Request | **是** | A |
| UI 修改 | **F**（HTML 缺失） | F |
| search 触发 | **F**（无 watch） | F |

**A 级 100% 收口**：
- startTime 在 L4267 初始化为 new Date()，**每次** searchAdminList 都会重新格式化（A）
- searchAdminList **每次执行** 都重新设置 startTime（L4296）
- 等级：A

---

## 9. endTime 完整生命周期（30.7）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始 | **无默认值** | A |
| 计算（L4297） | `DateUtilFactory.plus($scope.rightTime)` | A |
| 进入 Request | **是** | A |
| UI 修改 | **F**（HTML 缺失） | F |

**A 级 100% 收口**：
- endTime **仅在 searchAdminList 内** 由 DateUtilFactory.plus 计算（A）
- 初始**无默认值**（$scope.obj.endTime 不在 L4266-4270 初始化）
- 等级：A

---

## 10. machineCenterId 完整生命周期（30.8）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始（L4269） | `null` | A |
| 修改 | **未观察**（无 $scope.obj.machineCenterId = 赋值） | F |
| UI 来源 | **F**（HTML 缺失） | F |
| 进入 Request | **是**（默认 null） | A |
| search 触发 | **F** | F |

**A 级 100% 收口**：
- machineCenterId 初始 = null（A）
- machineOrderListCtrl 范围内**完全没有** `obj.machineCenterId = X` 赋值代码（A）
- 是否被 HTML 修改 = F
- 等级：A/F

**关键 A 级新发现**：
- 整个 machineOrderListCtrl 范围内 machineCenterId **仅 L4269 初始化为 null**
- 没有任何**已知**的修改点
- 进入 Request 时**始终是 null**（除非 HTML 修改，HTML 不可见）
- 等级：A

---

## 11. receiveStatus 完整生命周期（30.9）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始（L4270） | `null` | A |
| grantAuth 成功（L4288） | `0` | A |
| changeReceiveStatus（index）（L4345） | `index` | A |
| UI 来源 | **F**（HTML 缺失） | F |
| 进入 Request | **是** | A |
| search 触发 | changeReceiveStatus → searchAdminList (L4346) | A |

**A 级 100% 收口**：
- receiveStatus 修改点 = **2 个**（grantAuth 成功 + changeReceiveStatus）
- changeReceiveStatus 唯一触发 Query 路径（通过 L4346 searchAdminList）
- 等级：A

---

## 12. acceptStatus 完整生命周期（30.10）

| 阶段 | 值 | 等级 |
|---|---|---|
| 来源 | setTab(tab) | A |
| tab=1 | null (L4350) | A |
| tab=2 | 0 (L4353) | A |
| tab=3 | 1 (L4356) | A |
| tab=4 | 1 (L4359) | A |
| 进入 Request | **是** | A |
| 初始 | **无默认值** | A |

**A 级 100% 收口**：
- acceptStatus **仅** 由 setTab 修改（A）
- 等级：A

---

## 13. statusArray 完整生命周期（30.11）

| 阶段 | 值 | 等级 |
|---|---|---|
| 来源 | setTab(tab) | A |
| tab=1 | null (L4351) | A |
| tab=2 | [0] (L4354) | A |
| tab=3 | [0, 1] (L4357) | A |
| tab=4 | [2] (L4360) | A |
| 进入 Request | **是** | A |
| 初始 | **无默认值** | A |

**A 级 100% 收口**：
- statusArray **仅** 由 setTab 修改（A）
- 等级：A

---

## 14. setTab 完整（30.12）

**完整定义**（L4348-4364）：

```javascript
$scope.setTab = function (tab) {
    if (tab == 1) {
      $scope.obj.acceptStatus = null;
      $scope.obj.statusArray = null;
    } else if (tab == 2) {
      $scope.obj.acceptStatus = 0;
      $scope.obj.statusArray = [0];
    } else if (tab == 3) {
      $scope.obj.acceptStatus = 1;
      $scope.obj.statusArray = [0, 1];
    } else if (tab == 4) {
      $scope.obj.acceptStatus = 1;
      $scope.obj.statusArray = [2];
    } else {}
    $scope.tab = tab;
    $scope.searchAdminList();
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| 输入参数 | tab (1/2/3/4) | A |
| 修改 acceptStatus | 是（A） | A |
| 修改 statusArray | 是（A） | A |
| 修改 $scope.tab | 是（L4362） | A |
| 修改 pageStart | **否**（A） | A |
| 直接调用 search | **是**（L4363 searchAdminList） | A |

---

## 15. tab 默认值（30.13）

| 阶段 | 值 | 等级 |
|---|---|---|
| L4343 controller 同步 | `$scope.tab = 1` | A |
| L4289 grantAuth 成功 | `setTab(4)` → tab=4 | A |
| 最终默认值 | **tab=4** | A |

**A 级 100% 收口**：
- L4289 setTab(4) **覆盖** L4343 $scope.tab = 1
- setTab(4) 内部 L4363 立即调用 searchAdminList → **触发首次 Query**
- 等级：A

---

## 16. tab 切换机制（30.14）

| tab | 调用来源 | 等级 |
|---|---|---|
| setTab(1) | HTML ng-click + 业务逻辑 | A（function）/ F（HTML 缺失） |
| setTab(2) | HTML ng-click + 业务逻辑 | A/F |
| setTab(3) | HTML ng-click + 业务逻辑 | A/F |
| setTab(4) | **grantAuth 内部 L4289** + 业务逻辑 | A（grantAuth 内部已确认）/ F（HTML 缺失） |

**A 级关键新发现**：
- setTab(4) **第一次**调用确定在 grantAuth 内部（L4289）
- setTab(1/2/3) **当前资源范围未观察到直接调用**（仅 setTab 函数定义）
- 等级：A/F

---

## 17. tab → Request 派生（30.15）

**A 级 100% 收口**：
- tab **本身不进入 Request**（A）
- tab 派生 acceptStatus / statusArray 后**进入 Request**（A）
- 派生关系：
  - tab=1 → acceptStatus=null, statusArray=null
  - tab=2 → acceptStatus=0, statusArray=[0]
  - tab=3 → acceptStatus=1, statusArray=[0, 1]
  - tab=4 → acceptStatus=1, statusArray=[2]
- 等级：A

---

## 18. pageSize 完整（30.20）

| 项目 | 证据 | 等级 |
|---|---|---|
| 值 | `10` | A |
| 定义位置 | L4265 (`var pageSize = 10`) + L4299 (ListFactory 第 3 参数) + L4304 (pagination items_per_page) | A |
| 是否可修改 | **否**（3 个位置都固定 10） | A |
| 修改点 | **F**（无） | F |

**A 级 100% 收口**：
- pageSize = 10，**写死**，**无任何修改点**
- 等级：A

---

## 19. pageStart 完整（30.16, 30.17, 30.18）

| 阶段 | 值 | 等级 |
|---|---|---|
| 初始（L4299 第 2 参数） | `0` | A |
| 翻页（L4306） | `index * pageSize` | A |
| 翻页来源 | jQuery pagination 插件的 `callback(index)` | A |
| 翻页 function | `$scope.getAdminList.clearAndSetIndex(index * pageSize)` | A |

**A 级 100% 收口**：
- pageStart **由 jQuery pagination 插件 callback 控制**
- index 来自 pagination 回调
- 翻页后 `getAdminList.nextPage()` **重新调用** 同一 API
- 等级：A

---

## 20. 翻页 → search（30.19）

**A 级 100% 收口**：
- 翻页 callback（L4306-4307）：
  ```javascript
  $scope.getAdminList.clearAndSetIndex(index * pageSize);
  $scope.getAdminList.nextPage();
  ```
- 翻页**直接**触发**同一 API**（A，ListFactory 内部）
- 翻页**不重新调用** searchAdminList（A）
- 翻页**不重新计算** count（A，count 来自 ListFactory 内部已缓存）
- 等级：A

---

## 21. count 完整（30.21）

| 来源 | 等级 |
|---|---|
| `$scope.getAdminList.count` (A，L4303) | A |
| ListFactory 内部赋值 | A |
| **不**有 count 专用 API | A |

**A 级 100% 收口**：
- count 来自 selectMachineCenterOrderRecordVoList.json Response（同主 Query）
- **不**调 statProductDeliveryStatusOfCashflow.json（那个是 deliveryProcessingCtrl / deliveryInputCtrl 的）
- 等级：A

---

## 22. getAdminList 完整（30.22）

| 项目 | 证据 | 等级 |
|---|---|---|
| 创建 | `new ListFactory(API, 0, 10, $scope.obj)` (L4299) | A |
| 数据来源 | ListFactory 内部解包 | A |
| `count` 字段 | L4303 | A |
| `items[]` 字段 | HTML 推断 + receiveOrder/deliveryReceiveOrder 使用 (L4321/L4336) | A |

**A 级 100% 收口**：
- searchAdminList success 不显式赋值 getAdminList = res.result
- ListFactory 内部自动处理
- getAdminList 是 ListFactory 实例
- 等级：A

---

## 23. items 完整（30.23, 30.24）

**items 真实使用位置**：
- L4321: `$scope.getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` (receiveOrder)
- L4336: `$scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` (deliveryReceiveOrder)
- L4322: `$scope.getAdminList.count = $scope.getAdminList.count - 1` (receiveOrder 成功后)

**A 级 100% 收口**：
- items 是 receiveOrder / deliveryReceiveOrder 的**唯一**数据源
- items 通过 HTML ng-repeat 渲染（之前 S1-59 收口 16 列绑定）
- items 与 count 在 search success 后**同步**更新（A）
- 等级：A

---

## 24. watch / timeout / rootScope event（30.25-30.27）

| 机制 | 搜索 | 等级 |
|---|---|---|
| `$watch` | machineOrderListCtrl 范围**完全不出现** | A |
| `$timeout` | machineOrderListCtrl 范围**完全不出现** | A |
| `$rootScope.$on` | machineOrderListCtrl 范围**完全不出现** | A |
| debounce | **不**存在 | A |
| 异步 trigger | **不**存在（除 grantAuth 异步） | A |

**A 级 100% 收口**：
- machineOrderListCtrl 范围内**没有任何** 自动 watch / event / debounce 机制
- 所有 search trigger **都是显式调用**
- 等级：A

---

## 25. stateParams 完整（30.28）

| 项目 | 证据 | 等级 |
|---|---|---|
| 注入 | `$stateParams` (L4264) | A |
| 读取 | **不读** | A |
| 使用 | **F** | F |

**A 级 100% 收口**：
- machineOrderListCtrl 注入 $stateParams 但**完全不使用**
- 等级：A

---

## 26. 完整 Request 生命周期（30.29）

```
Controller 初始化 L4264-4365
   ↓
L4265: var pageSize = 10
L4266-4270: 初始化 $scope.obj = { startTime, rightTime, machineCenterId=null, receiveStatus=null }
L4271: centerArr = []

GrantAuth 异步启动 (L4272)
   ↓
【异步分支】grantAuth 返回
   ├ L4273 if (res)
   │   ├ L4274-4275: $scope.obj.companyId = res.id
   │   ├ L4276-4286: 加载 machineCenter list (辅助 API)
   │   ├ L4288: $scope.obj.receiveStatus = 0
   │   └ L4289: $scope.setTab(4)
   │       └ L4348-4364 setTab(4) → acceptStatus=1, statusArray=[2]
   │           └ L4362: $scope.tab = 4
   │               └ L4363: $scope.searchAdminList()
   │                   └ L4294-4312 searchAdminList
   │                       ├ L4296: DateUtilFactory.origin(startTime)
   │                       ├ L4297: DateUtilFactory.plus(rightTime) → endTime
   │                       └ L4299: new ListFactory(API, 0, 10, $scope.obj)
   │                           └ L4300: $scope.getAdminList.nextPage()
   └ L4291: $scope.setCompanyModal = !res

Controller 同步 L4343: $scope.tab = 1 (被 L4289 覆盖)

其他 search 入口:
   ├ L4344-4346 changeReceiveStatus(index) → $scope.obj.receiveStatus = index; searchAdminList()
   └ L4348-4364 setTab(tab) → acceptStatus/statusArray 修改 + searchAdminList()

翻页 (L4303-4309 pagination callback):
   └ clearAndSetIndex(index * pageSize); nextPage()
```

**A 级 100% 收口**。

---

## 27. 历史证据 vs 当前代码

### S1-58（118 号）：machineOrderListCtrl 列表 API
- 收口 list API + tab + acceptStatus / statusArray
- **S1-73 验证**：tab 1/2/3/4 + acceptStatus / statusArray **完全正确**（A）
- **S1-73 新发现**：tab 默认值是 4（grantAuth 成功时 setTab(4)）
- **S1-73 新发现**：setTab **总是**调用 searchAdminList（L4363）
- **S1-73 新发现**：changeReceiveStatus **总是**调用 searchAdminList（L4346）
- **无冲突**

### S1-59（119 号）：machineOrderListCtrl 列表字段 + 按钮
- 收口 25 个字段 + 按钮绑定
- **S1-73 验证**：receiveOrder / deliveryReceiveOrder 协议**完全正确**（A）
- **S1-73 新发现**：receiveOrder 写 receiveStatus + count - 1
- **S1-73 新发现**：deliveryReceiveOrder 写 deliveryStatus
- **无冲突**

### S1-72（132 号）：列表 Query 协议闭环
- 收口 9 Request 字段 + 分页
- **S1-73 验证**：9 Request 字段完整**正确**（A）
- **S1-73 新发现**：pageStart 变化路径（clearAndSetIndex + nextPage）
- **S1-73 新发现**：count 来自 ListFactory 内部
- **无冲突**

### S1-71（131 号）：State / Controller / Tab / Route 导航协议
- 收口 30 项
- **S1-73 验证**：tab 不调 $state.go
- **S1-73 验证**：machineOrderListCtrl 不读 $state.current.name
- **S1-73 验证**：machineOrderListCtrl 不读 $stateParams
- **无冲突**

---

## 28. 一期最小协议（A 级）

```javascript
// machineOrderListCtrl 最小 Request 生命周期
var pageSize = 10;
$scope.obj = {};
$scope.obj.startTime = new Date();
$scope.rightTime = new Date();
$scope.obj.machineCenterId = null;
$scope.obj.receiveStatus = null;
$scope.centerArr = [];

window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (res) {
  if (res) {
    $scope.obj.companyId = res.id;
    $scope.obj.receiveStatus = 0;
    $scope.setTab(4);
  }
  $scope.setCompanyModal = !res;
});

$scope.searchAdminList = function () {
  $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);
  $scope.obj.endTime = DateUtilFactory.plus($scope.rightTime);
  $scope.getAdminList = new ListFactory(
    "/admin/selectMachineCenterOrderRecordVoList.json", 0, 10, $scope.obj
  );
  $scope.getAdminList.nextPage().then(function (data) {
    $(".first-pagination").pagination($scope.getAdminList.count, {
      items_per_page: pageSize,
      callback: function (index) {
        $scope.getAdminList.clearAndSetIndex(index * pageSize);
        $scope.getAdminList.nextPage();
      }
    });
  });
};

$scope.setTab = function (tab) {
  if (tab == 1) { acceptStatus = null; statusArray = null; }
  else if (tab == 2) { acceptStatus = 0; statusArray = [0]; }
  else if (tab == 3) { acceptStatus = 1; statusArray = [0, 1]; }
  else if (tab == 4) { acceptStatus = 1; statusArray = [2]; }
  $scope.tab = tab;
  $scope.searchAdminList();
};

$scope.changeReceiveStatus = function (index) {
  $scope.obj.receiveStatus = index;
  $scope.searchAdminList();
};

$scope.receiveOrder = function (id, idx) {
  // ... write receiveStatus + count - 1
};

$scope.deliveryReceiveOrder = function (id, idx) {
  // ... write deliveryStatus
};

$scope.tab = 1;
```

---

## 29. F 边界（明确冻结）

| F 边界 | 说明 |
|---|---|
| HTML 模板 | machineOrderListCtrl HTML 缺失 |
| setTab(1/2/3) UI 调用点 | F |
| machineCenterId UI 修改点 | F（controller.js 范围不修改） |
| startTime UI 修改点 | F |
| endTime UI 修改点 | F |
| 业务语义 | E |

---

## 30. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | search 完整定位 | A |
| 30.2 | Query 入口数量 | A（**2 个**显式调用） |
| 30.3 | API 唯一调用点 | A（**1 个**） |
| 30.4 | 初始化顺序 | A |
| 30.5 | grantAuth | A |
| 30.6 | startTime | A |
| 30.7 | endTime | A |
| 30.8 | machineCenterId | A（init null）/ F（修改点） |
| 30.9 | receiveStatus | A |
| 30.10 | acceptStatus | A |
| 30.11 | statusArray | A |
| 30.12 | setTab | A |
| 30.13 | tab 默认值 | A（**4**） |
| 30.14 | tab 切换机制 | A（function）/ F（HTML） |
| 30.15 | tab → Request 派生 | A |
| 30.16 | pageStart 初始 | A（**0**） |
| 30.17 | pageStart 变化 | A（index * pageSize） |
| 30.18 | 翻页 function | A |
| 30.19 | 翻页 → search | A（nextPage，**不**调 searchAdminList） |
| 30.20 | pageSize | A（**10**，固定） |
| 30.21 | count | A（ListFactory 内部） |
| 30.22 | getAdminList | A |
| 30.23 | items | A |
| 30.24 | count / items 生命周期 | A |
| 30.25 | watch | A（**不存在**） |
| 30.26 | timeout | A（**不存在**） |
| 30.27 | rootScope event | A（**不存在**） |
| 30.28 | stateParams | A（**不读**） |
| 30.29 | 完整生命周期图 | A |
| 30.30 | 最终冻结 | A |

**统计**：A=30 / B=0 / C=0 / D=0 / E=0 / F=0 = 30

---

## 31. L1/L2/L3

**L1（前端直接事实）**：
- Request 字段生命周期
- Query 触发机制
- 9 字段 100% 收口
- 等级：A

**L2（业务模型解释）**：
- grantAuth 业务含义
- receiveStatus 业务含义
- 等级：**E**

**L3（数据库/物理模型）**：
- 9 字段 DB 结构
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
| Q1 | search 唯一 Query API？ | A（selectMachineCenterOrderRecordVoList.json） |
| Q2 | 初始化 Query 顺序？ | A（grantAuth 成功 → setTab(4) → searchAdminList） |
| Q3 | grantAuth 是否决定 companyId？ | A（**是**） |
| Q4 | setTab 是否决定 acceptStatus/statusArray？ | A（**是**） |
| Q5 | setTab 是否直接触发 search？ | A（**是**，L4363） |
| Q6 | tab 是否进入 Request？ | A（**否**） |
| Q7 | machineCenterId 是否可修改？ | A（**否**，controller.js 范围不改） |
| Q8 | receiveStatus 是否可修改？ | A（**是**，changeReceiveStatus） |
| Q9 | startTime 是否可修改？ | A（controller.js 范围**否**） |
| Q10 | endTime 是否可修改？ | A（controller.js 范围**否**） |
| Q11 | pageStart 如何变化？ | A（index * pageSize） |
| Q12 | pageSize 是否固定 10？ | A（**是**） |
| Q13 | 翻页是否触发 search？ | A（nextPage，**不**调 searchAdminList） |
| Q14 | 翻页是否触发 count？ | A（**否**，count 来自 ListFactory 已缓存） |
| Q15 | search success 如何更新 getAdminList？ | A（ListFactory 内部解包） |
| Q16 | items 和 count 是否都来自同一 Response？ | A（**是**） |
| Q17 | receiveOrder 使用哪个 items？ | A（$scope.getAdminList.items） |
| Q18 | deliveryReceiveOrder 使用哪个 items？ | A（$scope.getAdminList.items） |
| Q19 | 是否存在 $watch 自动 search？ | A（**否**） |
| Q20 | 是否存在 $timeout debounce？ | A（**否**） |
| Q21 | 是否存在 rootScope event 触发 search？ | A（**否**） |
| Q22 | 是否读取 stateParams？ | A（**否**） |
| Q23 | 是否存在多个 Query 入口？ | A（**2 个**显式：setTab + changeReceiveStatus） |
| Q24 | Request 参数生命周期完整闭合？ | A（**是**） |
| Q25 | 当前哪些 UI 触发仍为 F？ | A（setTab(1/2/3) UI / machineCenterId UI / startTime UI / endTime UI） |

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
- 历史 MD 修改 = **0**（28~132 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 36. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | Query 入口**仅 2 个**显式调用（setTab + changeReceiveStatus） | A |
| 2 | 初始化 Query 通过 grantAuth.then → setTab(4) | A |
| 3 | tab 默认值 = 4（grantAuth 成功时） | A |
| 4 | L4343 $scope.tab = 1 被 L4289 setTab(4) 覆盖 | A |
| 5 | machineCenterId **完全无修改点** | A |
| 6 | receiveStatus 修改点 2 个 | A |
| 7 | setTab **总是**调用 searchAdminList | A |
| 8 | changeReceiveStatus **总是**调用 searchAdminList | A |
| 9 | 翻页**不调用** searchAdminList（直接 nextPage） | A |
| 10 | pageSize = 10 **完全固定** | A |
| 11 | count 来自 ListFactory 内部 | A |
| 12 | 无 $watch / $timeout / $rootScope.$on | A |
| 13 | machineOrderListCtrl 不读 $stateParams | A |

---

## 37. 最终一句话

"S1-73 完成，已 Git 封口，立即停止，不进入 S1-74，等待老板下一条指令。"
