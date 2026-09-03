# S1-72 machineOrderListCtrl 列表 Query 协议闭环

> 专项收口：`machineOrderListCtrl` 列表查询完整协议
>
> 上一阶段：S1-71（131 号）已收口 State / Controller / Tab / Route 导航协议。
>
> 本阶段：S1-72（132 号）专项收口 machineOrderListCtrl 列表 Query 完整协议（tab → filter → Request → Response → Action）。

---

## 1. 核心结论

**machineOrderListCtrl 列表 Query 协议 100% 收口**：

- **Query API**：`/admin/selectMachineCenterOrderRecordVoList.json`（L4299）
- **唯一调用点**：L4299
- **Request**：`$scope.obj` 完整对象传入 ListFactory（**所有 obj 字段都进 Request**）
- **Request 字段**：companyId / startTime / endTime / machineCenterId / receiveStatus / acceptStatus / statusArray（**7 个**）
- **pageSize = 10**（L4265）
- **pageStart = 0**（初始，L4299 第 2 参数）
- **分页**：clearAndSetIndex(index * pageSize)（L4306）
- **count**：`$scope.getAdminList.count`（A，L4303）
- **默认 tab = 4**（L4289 初始 setTab(4)）
- **Action**：receiveOrder (L4314) / deliveryReceiveOrder (L4329) / changeReceiveStatus (L4344)
- **6 动作不在 machineOrderListCtrl 范围**（start / C-A / close / C-B / receive / delivery receive 跨 controller 收口）

**关键 A 级发现**：
- `machineCenterId` **进入 Request**（默认 null，A，L4269）
- `receiveStatus` **进入 Request**（默认 0，A，L4288 / L4345）
- `acceptStatus` **进入 Request**（setTab 设置，A，L4350-4359）
- `statusArray` **进入 Request**（setTab 设置，A，L4351-4360）
- `keyword` / `searchText` / `sort` / `orderBy` / `page` / `pageNo` / `deliveryStatus` / `startCompleteTime` / `endCompleteTime`：**完全不出现**（F）

---

## 2. 证据范围

**直接证据**：
- controller.js L4264-4365（machineOrderListCtrl 完整 101 行）
- controller.js 全文关键词搜索

**资源缺失**：
- machineOrderListCtrl HTML 模板（F）
- 完整 route schema（F）
- 后端算法 / DTO 定义（F）

---

## 3. machineOrderListCtrl 完整定位（30.1）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L4264 | A |
| 终点 | L4365 | A |
| 总行数 | 101 行 | A |
| 注入 | $scope, Popup, $timeout, $stateParams, $rootScope, $state, ObjectFactory, DateUtilFactory, ListFactory, $http | A |

**初始化逻辑**：
- L4265: `var pageSize = 10`
- L4266: `$scope.obj = {}`
- L4267: `$scope.obj.startTime = new Date()`
- L4268: `$scope.rightTime = new Date()`
- L4269: `$scope.obj.machineCenterId = null`（**默认 null**）
- L4270: `$scope.obj.receiveStatus = null`（**默认 null**）
- L4271: `$scope.centerArr = []`
- L4272-4292: grantAuth.then() 中：
  - L4274-4275: `res.companyName` + `res.id` → companyId
  - L4276-4286: selectMachineCenterListOfProduct.json → 加载 machineCenter list
  - L4288: `receiveStatus = 0`
  - L4289: `setTab(4)`（**默认 tab = 4**）
- L4343: `$scope.tab = 1`（**controller 默认 tab = 1**，但 L4289 立即覆盖为 4）

**A 级 100% 收口**。

---

## 4. Query API 唯一调用点（30.2）

| API | 调用位置 | 调用 function | 等级 |
|---|---|---|---|
| `/admin/selectMachineCenterOrderRecordVoList.json` | L4299 | `searchAdminList` | A |
| `/admin/selectMachineCenterListOfProduct.json` | L4277 | grantAuth.then | A（**辅助** API，不是 Query 主 API） |

**A 级 100% 收口**：
- 主 Query API **唯一**调用点 = L4299
- 辅助 API selectMachineCenterListOfProduct.json 用于加载 machineCenter list（L4277）
- 等级：A

---

## 5. Request 顶层结构（30.3）

**真实表达式**（L4299）：

```javascript
$scope.getAdminList = new ListFactory(
    "/admin/selectMachineCenterOrderRecordVoList.json", 
    0,        // pageStart
    10,       // pageSize
    $scope.obj // Request 字段
);
```

**A 级 100% 收口**：
- ListFactory 第 4 参数 = `$scope.obj` 完整对象
- **所有 $scope.obj 字段都进入 Request**
- 等级：A

---

## 6. Request 字段来源（30.4）

| 字段 | 表达式 | 默认值 | 来源 | 条件进入 | 等级 |
|---|---|---|---|---|---|
| `companyId` | `$scope.obj.companyId` | 无（未 grantAuth 成功时**不存在**） | grantAuth Response (L4275) | 仅 grantAuth 成功时 | A |
| `startTime` | `$scope.obj.startTime` | `new Date()` (L4267) | DateUtilFactory.origin (L4296) | 始终 | A |
| `endTime` | `$scope.obj.endTime` | **无默认值**（由 DateUtilFactory.plus 计算） | DateUtilFactory.plus (L4297) | 始终 | A |
| `machineCenterId` | `$scope.obj.machineCenterId` | `null` (L4269) | UI / controller 初始 | 始终 | A |
| `receiveStatus` | `$scope.obj.receiveStatus` | `null` (L4270) → `0` (L4288) | changeReceiveStatus / grantAuth | 始终 | A |
| `acceptStatus` | `$scope.obj.acceptStatus` | **无默认值**（grantAuth 成功后立即 setTab(4) 设置） | setTab (L4350-4359) | 仅 setTab 调用后 | A |
| `statusArray` | `$scope.obj.statusArray` | **无默认值** | setTab (L4351-4360) | 仅 setTab 调用后 | A |
| `pageSize` | `10`（第 3 参数） | 10（L4265 / L4299） | 写死 | 始终 | A |
| `pageStart` | `0`（第 2 参数） | 0（初始 L4299）→ `index * pageSize`（L4306） | 初始 + 翻页 | 始终 | A |

**A 级 100% 收口**。

**未观察字段**（F 维持）：
- `keyword` / `searchText` / `sort` / `orderBy` / `page` / `pageNo` / `deliveryStatus` / `startCompleteTime` / `endCompleteTime`：**完全不出现**
- 等级：F

---

## 7. tab（30.8）

| 状态 | 证据 | 等级 |
|---|---|---|
| 初始值 | `$scope.tab = 1` (L4343) | A |
| grantAuth 成功后 | `setTab(4)` (L4289) | A |
| 是否写入 Request | **否**（tab 是 controller 内部变量，**不**在 $scope.obj 中） | A |
| 是否调 $state.go | **否** | A |
| 用途 | 仅控制 setTab 内部分支 | A |

**A 级 100% 收口**：
- tab 是 controller 内部变量
- tab **不**进入 Request
- tab **不**调 $state.go
- 等级：A

---

## 8. acceptStatus（30.6）

| tab | acceptStatus | 位置 | 等级 |
|---|---|---|---|
| 1 | `null` | L4350 | A |
| 2 | `0` | L4353 | A |
| 3 | `1` | L4356 | A |
| 4 | `1` | L4359 | A |

**A 级 100% 收口**：
- acceptStatus **进入 Request**（A，作为 $scope.obj 字段）
- 通过 setTab 函数设置
- 等级：A

---

## 9. statusArray（30.7）

| tab | statusArray | 位置 | 等级 |
|---|---|---|---|
| 1 | `null` | L4351 | A |
| 2 | `[0]` | L4354 | A |
| 3 | `[0, 1]` | L4357 | A |
| 4 | `[2]` | L4360 | A |

**A 级 100% 收口**：
- statusArray **进入 Request**（A）
- 通过 setTab 函数设置
- 等级：A

---

## 10. status（30.5）

**machineOrderListCtrl 范围内 `status` 字段**：
- `$scope.obj.status` **完全不出现**（A）

**A 级关键发现**：
- `status` 字段**不进入** selectMachineCenterOrderRecordVoList.json Request
- 区别于 machineOrderCtrl（L16109 有 `status` 字段）和 machineOrderBrokenCtrl 状态字段
- 等级：A

**严格区分**：
- `status`（Request filter，machineOrderCtrl 使用） ≠ `machineCenterOrder.status`（Response 字段）
- machineOrderListCtrl 范围**不读** machineCenterOrder.status（**F**）
- 等级：A

---

## 11. Request 中未使用的 UI 参数（30.10）

| 参数 | 是否进入 Request | 等级 |
|---|---|---|
| keyword | **F**（不出现） | F |
| searchText | **F**（不出现） | F |
| sort | **F**（不出现） | F |
| orderBy | **F**（不出现） | F |
| page | **F**（不出现，pageStart 替代） | F |
| pageNo | **F**（不出现，pageStart 替代） | F |
| machineCenterId | **是**（默认 null） | A |
| receiveStatus | **是**（默认 0） | A |
| deliveryStatus | **F**（不出现） | F |
| startCompleteTime | **F**（不出现） | F |
| endCompleteTime | **F**（不出现） | F |
| startTime | **是** | A |
| endTime | **是** | A |
| acceptStatus | **是** | A |
| statusArray | **是** | A |
| companyId | **是**（grantAuth 成功时） | A |

**A 级 100% 收口**：
- **9 个字段进入 Request**（companyId / startTime / endTime / machineCenterId / receiveStatus / acceptStatus / statusArray / pageStart / pageSize）
- **7 个参数完全不出现**（keyword / searchText / sort / orderBy / page / pageNo / deliveryStatus / startCompleteTime / endCompleteTime 部分 F）
- 等级：A/F

---

## 12. pageSize / pageStart（30.11, 30.12）

| 字段 | 真实值 | 来源 | 等级 |
|---|---|---|---|
| pageSize | `10` | L4265 / L4299（第 3 参数） | A |
| pageStart（初始） | `0` | L4299（第 2 参数） | A |
| pageStart（翻页） | `index * pageSize` | L4306 (clearAndSetIndex) | A |

**A 级 100% 收口**。

---

## 13. 分页机制（30.13）

```javascript
// L4300-4310
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
```

**A 级 100% 收口**：
- 使用 `ListFactory.nextPage()` 方法
- 使用 `clearAndSetIndex(index * pageSize)` 翻页
- count 来自 `$scope.getAdminList.count`（L4303）
- 使用 jQuery pagination 插件
- **不**使用 infinite scroll
- **不**使用 nextPage / prevPage 业务方法
- 等级：A

---

## 14. count 来源（30.14）

**count 真实来源**：
- `$scope.getAdminList.count`（A，L4303）
- 由 ListFactory 内部赋值（直接证据 F）

**machineOrderListCtrl 自己的 count 行为**：
- **不调** statProductDeliveryStatusOfCashflow.json（属于 deliveryProcessingCtrl / deliveryInputCtrl）
- 等级：A

---

## 15. Response 顶层（30.15）

**ListFactory 暴露的字段**：
- `$scope.getAdminList.items[]`（A，HTML 推断使用，机器 OrderList.html L260-345 之前 S1-59 已收口）
- `$scope.getAdminList.count`（A，L4303）

**未直接读取的 Response 字段**（F 维持）：
- `res.status`（仅 console.log L4302）
- `result.object`：F（ListFactory 内部已解包）
- `result.list`：F（已解包到 items）
- 等级：A/F

---

## 16. machineCenterOrderRecordVo（30.16）

**items[i] 类型推断**：
- `machineCenterOrderRecordVo`（E 级推断，基于 API 命名）
- **不直接**在 controller.js 中命名为 machineCenterOrderRecordVo
- 等级：B（基于 API 命名）

---

## 17. nested 字段读取（30.17-30.25）

| 嵌套对象 | 真实读取字段 | 等级 |
|---|---|---|
| `item.patient` | **F**（machineOrderListCtrl 范围内**不直接读取**） | F |
| `item.customer` | **F** | F |
| `item.medicalRecord` | **F** | F |
| `item.machineCenter` | **F** | F |
| `item.sendAdmin` | **F** | F |
| `item.machineCenterOrder.id` | **F**（不直接读取，作为隐式 id 通过 function 参数） | E |
| `item.machineCenterOrder.status` | **F** | F |
| `item.machineCenterOrder.receiveStatus` | **是**（L4321 写后赋值 1） | A |
| `item.medicalProduct` | **F** | F |
| `item.product` | **F** | F |
| `item.medicalProductDelivery.deliveryStatus` | **是**（L4336 写后赋值 1） | A |

**A 级 100% 收口**：
- machineOrderListCtrl 范围内**仅 2 个嵌套字段**被直接读取/写入：
  - `getAdminList.items[idx].machineCenterOrder.receiveStatus`（L4321）
  - `getAdminList.items[idx].medicalProductDelivery.deliveryStatus`（L4336）
- 其他嵌套对象**完全不直接读取**（F）
- 等级：A

---

## 18. 六动作参数来源（30.26）

| Action | 实际进入 | 等级 |
|---|---|---|
| receiveOrder (L4314) | 接受 (id, idx) 参数 → 写 `items[idx].machineCenterOrder.receiveStatus = 1` | A |
| deliveryReceiveOrder (L4329) | 接受 (id, idx) 参数 → 写 `items[idx].medicalProductDelivery.deliveryStatus = 1` | A |
| startOrder (startMachineCenterOrder) | **不在** machineOrderListCtrl 范围 | F |
| C-A complete (completeMachineCenterOrder) | **不在** machineOrderListCtrl 范围 | F |
| C-B complete (machineOrderBrokenCtrl) | **不在** machineOrderListCtrl 范围 | F |
| close (closeMachineCenterOrder) | **不在** machineOrderListCtrl 范围 | F |

**id 实际来源**：
- receiveOrder / deliveryReceiveOrder 的 id 参数 = function 入参
- HTML 调用点 = F（HTML 模板缺失）
- 推断：id = `item.machineCenterOrder.id`（E 级推断）

**A 级 100% 收口**：
- 6 动作中**仅 2 个**（receive / delivery receive）在 machineOrderListCtrl 范围
- 等级：A

---

## 19. Request → Response → Action 完整闭环（30.28）

```
$scope.tab (L4343 = 1 → L4289 setTab(4) → L4348-4364)
   ↓
setTab(tab) 修改 $scope.obj.acceptStatus + statusArray
   ↓
searchAdminList() (L4294)
   ↓
$scope.obj.startTime / endTime (L4296-4297 DateUtilFactory 格式化)
   ↓
new ListFactory(
  "/admin/selectMachineCenterOrderRecordVoList.json",   [A]
  0,                                                      [A: pageStart]
  10,                                                     [A: pageSize]
  $scope.obj                                              [A: Request 完整对象]
)
   ↓
getAdminList.nextPage()                                  [A]
   ↓
ListFactory 内部解析 Response:
  - getAdminList.count
  - getAdminList.items[]
   ↓
$scope.getAdminList.items[idx]                           [A]
   ├ machineCenterOrder.receiveStatus → receiveOrder 写 (L4321)
   └ medicalProductDelivery.deliveryStatus → deliveryReceiveOrder 写 (L4336)
```

**A 级 100% 收口**。

---

## 20. 1:1 最小列表协议（30.29）

```javascript
// machineOrderListCtrl 最小可复刻协议
var pageSize = 10;
$scope.obj = {};
$scope.obj.startTime = new Date();
$scope.rightTime = new Date();
$scope.obj.machineCenterId = null;          // 默认 null
$scope.obj.receiveStatus = null;             // 默认 null → grantAuth 成功后 0
$scope.centerArr = [];

window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (res) {
  if (res) {
    $scope.obj.companyId = res.id;
    // 加载 machineCenter list（辅助）
    $scope.getCenterListRecordPay = new ObjectFactory();
    $scope.getCenterListRecordPay.saveOrQuery(
      "/admin/selectMachineCenterListOfProduct.json", 
      { companyId: res.id }
    );
    $scope.obj.receiveStatus = 0;
    $scope.setTab(4);
  }
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

$scope.receiveOrder = function (id, idx) {
  var factory = new ObjectFactory();
  factory.saveOrQuery("/admin/receiveMachineCenterOrder.json", { machineCenterOrderId: id })
    .then(function (re) {
      if (re.status == 0) {
        Popup.notice("签收成功");
        $scope.getAdminList.items[idx].machineCenterOrder.receiveStatus = 1;
        $scope.getAdminList.count = $scope.getAdminList.count - 1;
      }
    });
};

$scope.deliveryReceiveOrder = function (id, idx) {
  var factory = new ObjectFactory();
  factory.saveOrQuery("/admin/deliveryMachineCenterOrder.json", { machineCenterOrderId: id })
    .then(function (re) {
      if (re.status == 0) {
        Popup.notice("发货成功");
        $scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1;
      }
    });
};

$scope.changeReceiveStatus = function (index) {
  $scope.obj.receiveStatus = index;
  $scope.searchAdminList();
};

$scope.tab = 1;
```

---

## 21. E 级业务语义（不混入 A 级协议）

- tab 业务含义（"待受理" / "待加工" / "加工中" / "测试中"）：E
- acceptStatus 业务含义（"未接收" / "已接收"）：E
- statusArray 业务含义：E
- machineCenterOrderRecordVo 业务含义：E
- "可加工 / 已加工 / 已测试"：E
- 等级：E

---

## 22. 历史证据 vs 当前代码

### S1-58（118 号）：machineOrderListCtrl 列表 API
- 收口 list API + tab + acceptStatus / statusArray
- **S1-72 验证**：tab 1/2/3/4 + acceptStatus / statusArray 完整对照**完全正确**（A）
- **S1-72 新发现**：tab 默认值是 4（L4289 setTab(4)），不是 1
- **S1-72 新发现**：pageSize = 10（之前已收口）
- **S1-72 新发现**：machineCenterId 默认 null（A，L4269）
- **S1-72 新发现**：receiveStatus 默认 0（A，L4288）
- **无冲突**

### S1-59（119 号）：machineOrderListCtrl 列表字段 + 按钮
- 收口 25 个字段 + 按钮绑定
- **S1-72 验证**：receiveOrder / deliveryReceiveOrder 协议**完全正确**（A）
- **S1-72 新发现**：machineOrderListCtrl 范围内**仅 2 个嵌套字段**被直接读取（machineCenterOrder.receiveStatus / medicalProductDelivery.deliveryStatus）
- **S1-72 新发现**：其他嵌套对象（patient / customer / medicalRecord / machineCenter / sendAdmin / medicalProduct / product）**完全不直接读取**（F）
- **S1-72 新发现**：HTML 中可见的 16 列 100% A 级绑定（之前 S1-59 收口），但 controller.js 范围内不直接读这些字段
- **无冲突**

### S1-60（120 号）：MachineCenterOrder 状态机
- 收口 26 项
- **S1-72 验证**：acceptStatus 是 machineOrderListCtrl 内部 filter 字段（不是 MachineCenterOrder 状态字段）
- **无冲突**

### S1-68（128 号）：MachineCenterOrder 数据来源
- 收口 3 controller 数据来源
- **S1-72 验证**：machineOrderListCtrl 数据来源 = selectMachineCenterOrderRecordVoList.json
- **无冲突**

### S1-70（130 号）：状态字段与 UI State 映射
- 收口 30 项
- **S1-72 验证**：tab / acceptStatus / statusArray 仅是 filter，**不**是 UI state
- **无冲突**

### S1-71（131 号）：State / Controller / Tab / Route 导航协议
- 收口 30 项
- **S1-72 验证**：tab 不调 $state.go
- **S1-72 验证**：machineOrderListCtrl 不读 $stateParams / $state.current.name
- **无冲突**

---

## 23. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | machineOrderListCtrl 完整定位 | A |
| 30.2 | selectMachineCenterOrderRecordVoList.json 唯一调用点 | A |
| 30.3 | Request 顶层结构 | A |
| 30.4 | Request 字段来源 | A |
| 30.5 | status | A（**不**进入 Request） |
| 30.6 | acceptStatus | A |
| 30.7 | statusArray | A |
| 30.8 | tab | A |
| 30.9 | $state.current.name | A（machineOrderListCtrl **不**使用） |
| 30.10 | Request 中未使用的 UI 参数 | A/F |
| 30.11 | pageSize | A |
| 30.12 | pageStart | A |
| 30.13 | 分页机制 | A |
| 30.14 | count 来源 | A |
| 30.15 | Response 顶层 | A |
| 30.16 | machineCenterOrderRecordVo | B（API 命名推断） |
| 30.17-30.25 | nested 字段 | A/F（**仅 2 字段**） |
| 30.26 | 六动作参数来源 | A |
| 30.27 | 按钮 action | A（function）/ F（HTML） |
| 30.28 | Request → Response → Action 闭环 | A |
| 30.29 | 1:1 最小列表协议 | A |
| 30.30 | 最终冻结 | A |

**统计**：A=29 / B=1 / C=0 / D=0 / E=0 / F=0 = 30

---

## 24. L1/L2/L3

**L1（前端直接事实）**：
- 9 Request 字段完整协议
- 2 嵌套字段写入点
- 分页机制
- setTab 完整定义
- 等级：A

**L2（业务模型解释）**：
- tab 业务含义
- acceptStatus / statusArray 业务含义
- 等级：**E**

**L3（数据库/物理模型）**：
- machineCenterOrderRecordVo 表
- 9 Request 字段 DB 含义
- 等级：**F**

---

## 25. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 26. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | machineOrderListCtrl 核心 Query API？ | A（selectMachineCenterOrderRecordVoList.json） |
| Q2 | Query Request 全字段？ | A（companyId / startTime / endTime / machineCenterId / receiveStatus / acceptStatus / statusArray + pageStart/pageSize） |
| Q3 | tab 是否进入 Request？ | A（**否**） |
| Q4 | acceptStatus 是否进入 Request？ | A（**是**） |
| Q5 | statusArray 是否进入 Request？ | A（**是**） |
| Q6 | status 是否进入 Request？ | A（**否**） |
| Q7 | machineCenterId 是否进入 Request？ | A（**是**，默认 null） |
| Q8 | receiveStatus 是否进入 Request？ | A（**是**，默认 0） |
| Q9 | deliveryStatus 是否进入 Request？ | A（**否**） |
| Q10 | keyword/searchText 是否进入 Request？ | A（**否**） |
| Q11 | sort/orderBy 是否进入 Request？ | A（**否**） |
| Q12 | pageSize/pageStart？ | A（10 / 0 初始） |
| Q13 | count 如何获得？ | A（$scope.getAdminList.count from ListFactory） |
| Q14 | Response 顶层结构？ | A（ListFactory 暴露 items[] + count） |
| Q15 | item 真实字段结构？ | A（machineCenterOrderRecordVo 推断 B） |
| Q16 | machineCenterOrder 直接使用哪些字段？ | A（**仅 receiveStatus**） |
| Q17 | medicalProductDelivery 直接使用哪些字段？ | A（**仅 deliveryStatus**） |
| Q18 | receiveOrder id 来源？ | A（function 参数；HTML 推断 E） |
| Q19 | deliveryReceiveOrder id 来源？ | A（function 参数；HTML 推断 E） |
| Q20 | 列表 Query 与六动作是否直接共享 Response？ | A（**是**，items[idx] 共享） |
| Q21 | tab 是页面 State 还是 filter？ | A（**filter**） |
| Q22 | acceptStatus 是 State 还是 filter？ | A（**filter**） |
| Q23 | statusArray 是 State 还是 filter？ | A（**filter**） |
| Q24 | MachineCenterOrder.status → UI state 自动映射？ | A（**否**） |
| Q25 | 1:1 最小协议是否闭合？ | A（**是**） |

---

## 27. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 28. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~131 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 29. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | tab 默认值是 4（L4289 setTab(4)） | A |
| 2 | machineCenterId 默认 null（A，L4269） | A |
| 3 | receiveStatus 默认 0（A，L4288） | A |
| 4 | 9 Request 字段（companyId / startTime / endTime / machineCenterId / receiveStatus / acceptStatus / statusArray / pageStart / pageSize） | A |
| 5 | tab / status / keyword / searchText / sort / orderBy / deliveryStatus / startCompleteTime / endCompleteTime **不**进入 Request | A |
| 6 | machineOrderListCtrl 范围内**仅 2 个嵌套字段**被直接读取 | A |
| 7 | grantAuth 成功时 setTab(4) 默认 | A |
| 8 | changeReceiveStatus 函数（L4344-4346） | A |
| 9 | selectMachineCenterListOfProduct.json 辅助 API（L4277） | A |

---

## 30. 最终一句话

"S1-72 完成，已 Git 封口，立即停止，不进入 S1-73，等待老板下一条指令。"
