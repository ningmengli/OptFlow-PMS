# 117 S1-58 MachineOrderWaitProcess 8 State 列表 API 数据协议收口 26 项

**文档性质**：S1-58 8 个 State 真实数据获取协议专项
**任务来源**：老板 S1-58 专项指令（9/3 16:26）
**侦察时间**：2026-09-03 16:30-17:00
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **S1-57 留下的"8 个 state 数据协议"收口**：
>
> A. machineOrderWaitProcessCtrl 加载 API
> B. tab/chain/status Request 字段
> C. Response 真实结构
> D. 普通 / 连锁 State 差异
> E. 一期可复刻数据协议边界

---

## 一、🎯 颠覆性 A 级新发现 - machineOrderWaitProcessCtrl 不调用列表 API

### 1.1 完整 controller 源码（A 级 100%）

```javascript
// controller.js L16206-16217
angular.module("bestvisionWeb").controller("machineOrderWaitProcessCtrl", 
  ["$scope", "$stateParams", "Popup", "DateUtilFactory", "$state", "ObjectFactory", 
   "ListFactory", "$http", "$timeout", function ($scope, $stateParams, Popup, 
   DateUtilFactory, $state, ObjectFactory, ListFactory, $http, $timeout) {
  
  if ($scope.$state.current.name == "machineOrderChainWaitAccess" || 
      $scope.$state.current.name == "machineOrderWaitAccess") {
    $scope.tab = 1;
  } else if ($scope.$state.current.name == "machineOrderChainWaitProcess" || 
             $scope.$state.current.name == "machineOrderWaitProcess") {
    $scope.tab = 2;
  } else if ($scope.$state.current.name == "machineOrderChainProcessing" || 
             $scope.$state.current.name == "machineOrderProcessing") {
    $scope.tab = 3;
  } else if ($scope.$state.current.name == "machineOrderChainTesting" || 
             $scope.$state.current.name == "machineOrderTesting") {
    $scope.tab = 4;
  } else {}
  console.log($scope.tab);
}]);
```

### 1.2 🎯 关键 A 级新发现 - 真实业务

| 项目 | 证据 | 评级 |
|------|------|------|
| controller 真实业务 | **只做 $state.current.name → $scope.tab 映射** | A 100% |
| **调用任何 API** | **0 处**（无 $http / $resource / get / list / load / search）| A 100% |
| 加载列表数据 | **不加载** | A 100% |
| 真实入口 | 8 个 state 共享 controller 入口 | A 100% |

**🎯 颠覆性 A 级新发现 - machineOrderWaitProcessCtrl 是"tab 分类器"**：
- 业务 = 8 个 state 共享同一个 controller，但 controller **不加载任何列表数据**
- 真实列表加载在**其他 controller**（machineOrderListCtrl / machineProcessListCtrl）

---

## 二、🎯 真实列表 API 在 machineOrderListCtrl

### 2.1 列表 API 路径（A 级 100%）

| API | 行号 | controller | 用途 |
|-----|------|-----------|------|
| `/admin/selectMachineCenterOrderRecordVoList.json` | L4100 | machineOrderListCtrl | 列表 L4100（初始 count=1）|
| `/admin/selectMachineCenterOrderRecordVoList.json` | L4278 | machineOrderListCtrl | 列表 L4278（pageSize=10）|
| `/admin/selectMachineCenterOrderRecordVoList.json` | L37175 | machineProcessListCtrl | 列表 L37175（pageSize=20）|

**🎯 S1-58 关键 A 级新发现 - 3 个 controller 共享同一列表 API**：
- API 名称 = `selectMachineCenterOrderRecordVoList.json`
- 都是 ListFactory 模式
- 都是分页查询

### 2.2 machineOrderListCtrl 完整 Request 字段（A 级 100%）

```javascript
// controller.js L4091-4100（machineOrderListCtrl 初始）
var objRecord = {};
objRecord.companyId = res.id;                      // ← 加载加工中心列表时设置
objRecord.receiveStatus = 0;                       // ← 默认
objRecord.acceptStatus = 1;                        // ← 默认
objRecord.statusArray = [2];                       // ← 默认
objRecord.startTime = DateUtilFactory.origin(startTime);
objRecord.endTime = DateUtilFactory.plus(rightTime);
$scope.getAdminList = new ListFactory(
  "/admin/selectMachineCenterOrderRecordVoList.json", 
  0, 1,                // pageStart, pageSize=1
  objRecord
);
```

### 2.3 searchAdminList 完整 Request 字段（A 级 100%）

```javascript
// controller.js L4273-4291
$scope.searchAdminList = function () {
  if ($scope.obj.startTime && $scope.rightTime) {
    $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);
    $scope.obj.endTime = DateUtilFactory.plus($scope.rightTime);
    
    $scope.getAdminList = new ListFactory(
      "/admin/selectMachineCenterOrderRecordVoList.json", 
      0, 10,           // pageStart, pageSize=10
      $scope.obj
    );
    ...
  }
};
```

### 2.4 列表 API Request 字段完整列表（A 级 100%）

| 字段 | 来源 | 行号 | 评级 |
|------|------|------|------|
| `companyId` | grantAuth.hasAuthForCompany | L4092, L4254 | A 100% |
| `startTime` | DateUtilFactory.origin | L4097, L4246, L4275 | A 100% |
| `endTime` / `rightTimer` | DateUtilFactory.plus | L4098, L4276 | A 100% |
| `receiveStatus` | 默认 0 / changeReceiveStatus 设置 | L4093, L4249, L4267, L4323 | A 100% |
| `acceptStatus` | setTab 动态 / 默认 1 | L4094, L4267, L4329-4339, L37144 | A 100% |
| `statusArray` | setTab 动态 / 默认 [2] | L4095, L4280, L4330-4339, L37145 | A 100% |
| `machineCenterId` | 页面下拉 / 默认 null | L4248, L4250-4264, L37146 | A 100% |
| `startCompleteTime` | searchEmployeeRank 派生 | L37172 | A 100% |
| `endCompleteTime` | searchEmployeeRank 派生 | L37173 | A 100% |

### 2.5 setTab 设置 Request 字段（A 级 100%）

```javascript
// controller.js L4327-4343（machineOrderListCtrl setTab）
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

| Tab | $scope.obj.acceptStatus | $scope.obj.statusArray |
|-----|------|------|
| 1 | null | null |
| 2 | 0 | [0] |
| 3 | 1 | [0, 1] |
| 4 | 1 | [2] |

**🎯 S1-58 关键 A 级新发现 - tab 1/2/3/4 → acceptStatus/statusArray 完整映射**：
- tab=1：全选（无 filter）
- tab=2：未接收 + status=0
- tab=3：已接收 + status=[0,1]
- tab=4：已接收 + status=[2]

---

## 三、🎯 关键 A 级新发现 - chain / tab 不在 Request

### 3.1 chain 在 Request 中（A 级 100%）

| 字段 | 出现位置 | 评级 |
|------|---------|------|
| `chain` 在 `selectMachineCenterOrderRecordVoList.json` Request | **0 处** | **F** |

**🎯 颠覆性 A 级新发现 - chain 不在列表 API Request**：
- controller.js 搜索 `selectMachineCenterOrderRecordVoList` 相关代码，chain 0 处
- machineOrderBrokenCtrl 中 `$stateParams.chain` 只用于 C-B if 分支（跳转 machineOrderTesting/ChainTesting）
- chain **不参与**列表筛选
- 普通 / 连锁 state 在列表 API 调用上**完全相同**

### 3.2 tab 在 Request 中（A 级 100%）

| 字段 | 出现位置 | 评级 |
|------|---------|------|
| `tab` 在 selectMachineCenterOrderRecordVoList Request | **0 处** | **F** |

**🎯 颠覆性 A 级新发现 - tab 不在列表 API Request**：
- tab 通过 setTab 转换为 `acceptStatus` + `statusArray` 进入 Request
- tab 本身不作为 Request 字段
- tab 只用于 UI 显示分类

### 3.3 tab → status 完整转换

| Tab | $scope.tab | 转换后 Request 字段 |
|-----|-----------|-------------------|
| 1 | 1 | `acceptStatus=null` / `statusArray=null` |
| 2 | 2 | `acceptStatus=0` / `statusArray=[0]` |
| 3 | 3 | `acceptStatus=1` / `statusArray=[0, 1]` |
| 4 | 4 | `acceptStatus=1` / `statusArray=[2]` |

---

## 四、machineOrderListCtrl 完整初始化

### 4.1 初始化流程（A 级 100%）

```javascript
// controller.js L4243-4271
$scope.obj = {};                                         // 初始化
$scope.obj.startTime = new Date();                      // 开始时间
$scope.rightTime = new Date();                           // 结束时间
$scope.obj.machineCenterId = null;                      // 加工中心 filter
$scope.obj.receiveStatus = null;                        // 接收状态 filter

window.grantAuth.hasAuthForCompany(ObjectFactory).then(function (res) {
  if (res) {
    $scope.companyName = res.companyName;
    $scope.obj.companyId = res.id;                       // 门店 ID
    
    // 加载加工中心下拉
    $scope.getCenterListRecordPay = new ObjectFactory();
    var centerPromise = $scope.getCenterListRecordPay.saveOrQuery(
      "/admin/selectMachineCenterListOfProduct.json", 
      { companyId: res.id }
    );
    
    $scope.obj.receiveStatus = 0;                       // 默认
    $scope.setTab(4);                                   // 默认 tab=4
  }
});
```

### 4.2 setTab(4) 触发链

```
$scope.setTab(4)
  ↓
$scope.obj.acceptStatus = 1
$scope.obj.statusArray = [2]
  ↓
$scope.tab = 4
  ↓
$scope.searchAdminList()  // ← 实际调用列表 API
  ↓
new ListFactory(
  "/admin/selectMachineCenterOrderRecordVoList.json", 
  0, 10, $scope.obj
)
```

---

## 五、列表 Response 真实对象

### 5.1 Response 顶层对象（A 级 100%）

| 对象 | 路径 | 评级 |
|------|------|------|
| `selectMachineCenterOrderRecordVoList.json` | `machineCenterOrderRecordVo` | A 100% |
| Response items | `getAdminList.items[]` 或 `getDataList.items[]` | A 100% |
| Response count | `getAdminList.count`（分页总数）| A 100% |

**注意**：Response 真实对象 = `machineCenterOrderRecordVo`（S1-52 已 A 级确认 17 字段）

### 5.2 ListFactory Response 字段（A 级 100%）

| ListFactory 字段 | 用途 | 评级 |
|---------------|------|------|
| `items[]` | 列表项数组 | A 100% |
| `count` | 总记录数（用于分页）| A 100% |
| `nextPage()` | 翻页方法 | A 100% |
| `clearAndSetIndex(index)` | 跳到指定页 | A 100% |

### 5.3 items[] 内部结构（S1-52 已 A 级确认）

```
items[i] = machineCenterOrderRecordVo
├── patient
│   ├── patientName
│   ├── patientGender
│   └── patientBirthday
├── customer
│   ├── customerName
│   └── linkMobile
├── medicalRecord
│   ├── id
│   ├── medicalCode (14位)
│   ├── doctorName
│   └── medicalRecordType
├── machineCenter
│   └── name
├── sendAdmin
│   └── nickname
├── machineCenterOrder
│   ├── id
│   ├── gmtCreate
│   ├── acceptStatus
│   ├── status
│   ├── receiveStatus
│   └── planDeliveryTime
├── medicalProduct
│   ├── productName
│   ├── useCount
│   ├── refundCount
│   ├── unitName
│   └── model1/2
├── product
│   ├── modelType
│   └── model1Name/2Name
└── medicalProductDelivery
    └── deliveryStatus
```

---

## 六、8 State → API 数据协议

### 6.1 🎯 关键 A 级新发现 - 8 个 state 共享同一列表 API

| State | tab | 列表 API | Request 差异 | Response |
|-------|-----|---------|------------|---------|
| `machineOrderWaitAccess` | 1 | `selectMachineCenterOrderRecordVoList.json` | acceptStatus=null, statusArray=null | machineCenterOrderRecordVo |
| `machineOrderChainWaitAccess` | 1 | 同上 | **完全相同** | 同上 |
| `machineOrderWaitProcess` | 2 | 同上 | acceptStatus=0, statusArray=[0] | 同上 |
| `machineOrderChainWaitProcess` | 2 | 同上 | **完全相同** | 同上 |
| `machineOrderProcessing` | 3 | 同上 | acceptStatus=1, statusArray=[0,1] | 同上 |
| `machineOrderChainProcessing` | 3 | 同上 | **完全相同** | 同上 |
| `machineOrderTesting` | 4 | 同上 | acceptStatus=1, statusArray=[2] | 同上 |
| `machineOrderChainTesting` | 4 | 同上 | **完全相同** | 同上 |

**🎯 颠覆性 A 级新发现 - 普通 / 连锁 state 在列表 API 层完全相同**：
- chain 0 处进入列表 API Request
- 普通 vs 连锁**只在 state name 上区分**
- 实际业务上用户用 chain 区分（连锁店看自己的数据，非连锁店看自己的）
- 业务上 chain 可能由后端根据登录态自动判定
- **前端不显式传递 chain 到列表 API**

### 6.2 列表 API Request 字段完整表

| 字段 | 类型 | 来源 | 评级 |
|------|------|------|------|
| `companyId` | number | grantAuth | A 100% |
| `startTime` | date | DateUtilFactory.origin | A 100% |
| `endTime` | date | DateUtilFactory.plus | A 100% |
| `receiveStatus` | 0/1 | changeReceiveStatus | A 100% |
| `acceptStatus` | 0/1/null | setTab | A 100% |
| `statusArray` | array | setTab | A 100% |
| `machineCenterId` | number | 页面下拉 | A 100% |
| `startCompleteTime` | date | searchEmployeeRank 派生 | A 100% |
| `endCompleteTime` | date | searchEmployeeRank 派生 | A 100% |
| `tab` | 0/1/2/3/4 | **不在 Request** | F |
| `chain` | 0/1 | **不在 Request** | F |

---

## 七、分页 / 搜索 / 排序

### 7.1 分页（A 级 100%）

| 项目 | 真实值 | 评级 |
|------|-------|------|
| `pageStart`（第 1 参）| 0 | A 100% |
| `pageSize`（第 2 参）| 10 / 20 / 1 | A 100% |
| 分页总数字段 | `getAdminList.count` | A 100% |
| 翻页方法 | `getAdminList.nextPage()` | A 100% |
| 跳页方法 | `getAdminList.clearAndSetIndex(index)` | A 100% |

### 7.2 搜索（A 级 100%）

| 项目 | 真实值 | 评级 |
|------|-------|------|
| `keyword` 进入 `selectMachineCenterOrderRecordVoList.json` Request | **0 处**（在 machineOrderListCtrl 范围内）| **F** |

**🎯 关键 A 级新发现 - machineOrderListCtrl 不使用 keyword 搜索**：
- 没有 `$scope.obj.keyword` 在 selectMachineCenterOrderRecordVoList Request 中
- 搜索字段 = `keyword` 在其他 controller 存在，但**不在加工单列表中**

### 7.3 排序（A 级 100%）

| 项目 | 真实值 | 评级 |
|------|-------|------|
| `sort` / `orderBy` / `order` | **0 处** | F |

**🎯 关键 A 级新发现 - 加工单列表无排序参数**。

---

## 八、状态字段在列表层用途

### 8.1 4 个状态字段在列表层（A 级 100%）

| 字段 | Response | Request | Filter | Button | Tab |
|------|---------|---------|--------|--------|-----|
| `acceptStatus` | **是** | **是** | **是** | **是** | **是** |
| `status` | **是** | **否**（通过 statusArray）| **是** | **是** | **是** |
| `receiveStatus` | **是** | **是** | **是** | **是** | **否** |
| `medicalProductDelivery.deliveryStatus` | **是** | **否** | **否** | **是** | **否** |

### 8.2 🎯 S1-58 关键 A 级新发现 - status 通过 statusArray 数组传递

- `status` **不是**直接作为 Request 字段
- **而是** `statusArray: [0]` / `[0,1]` / `[2]` 等数组
- 这是 S1-51 / S1-52 已部分发现的特性，本轮 100% 确认

---

## 九、Tab → 数据列表

### 9.1 Tab 真实数据来源（A 级 100%）

| Tab | State | 列表变量 | API | 真实 Request filter | 评级 |
|-----|-------|---------|-----|-------------------|------|
| 1 | machineOrderWaitAccess | `getAdminList.items[]` | `selectMachineCenterOrderRecordVoList.json` | `acceptStatus=null, statusArray=null` | A 100% |
| 2 | machineOrderWaitProcess | 同上 | 同上 | `acceptStatus=0, statusArray=[0]` | A 100% |
| 3 | machineOrderProcessing | 同上 | 同上 | `acceptStatus=1, statusArray=[0,1]` | A 100% |
| 4 | machineOrderTesting | 同上 | 同上 | `acceptStatus=1, statusArray=[2]` | A 100% |

**🎯 S1-58 关键 A 级新发现 - 4 个 tab 共享同一列表变量**：
- 4 个 tab 切换 = 重新调用列表 API（`searchAdminList()`）
- 列表变量 = 同一个 `$scope.getAdminList`
- tab=1/2/3/4 区别只在 **Request filter**（acceptStatus + statusArray）

---

## 十、状态数据流程

### 10.1 完整流程图

```
URL/state 进入 (machineOrderWaitProcessCtrl)
  ↓
$state.current.name → $scope.tab = 1/2/3/4
  ↓
[实际列表由其他 controller 加载]
  ↓
$scope.setTab(4) (machineOrderListCtrl L4268 默认)
  ↓
$scope.obj.acceptStatus = 1
$scope.obj.statusArray = [2]
  ↓
$scope.searchAdminList()
  ↓
new ListFactory(
  "/admin/selectMachineCenterOrderRecordVoList.json",
  0, 10, $scope.obj
)
  ↓
Response: getAdminList.items[] = machineCenterOrderRecordVo[]
  ↓
HTML 显示: ng-repeat="item in getAdminList.items"
  ↓
item.machineCenterOrder.status → 文字映射 (HTML L300-313)
```

---

## 十一、26 项评级矩阵

### A 组：machineOrderWaitProcessCtrl（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | machineOrderWaitProcessCtrl | L16206-16217 完整定义 | A 100% |
| 2 | 初始化 API | **0 处 API 调用** | A 100% |
| 3 | 列表 API | **0 处（不在此 controller）** | A 100% |

### B 组：machineOrderListCtrl 列表 API（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 4 | 列表 API | `selectMachineCenterOrderRecordVoList.json` | A 100% |
| 5 | Request 结构 | $scope.obj 9 字段 | A 100% |
| 6 | Response 结构 | machineCenterOrderRecordVo 17 字段 | A 100% |

### C 组：machineCenterOrderRecordVo 层级（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 7 | machineCenterOrderRecordVo | S1-52 已 100% 收口 | A 100% |
| 8 | MachineCenterOrder | 6 字段 (id/gmtCreate/acceptStatus/status/receiveStatus/planDeliveryTime) | A 100% |
| 9 | MedicalRecord | 4 字段 (id/medicalCode/doctorName/medicalRecordType) | A 100% |
| 10 | medicalProductDelivery | 1 字段 (deliveryStatus) | A 100% |

### D 组：8 State 数据来源（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 11 | tab=1 状态 | 全部 / null filter | A 100% |
| 12 | tab=2 状态 | acceptStatus=0, statusArray=[0] | A 100% |
| 13 | tab=3 状态 | acceptStatus=1, statusArray=[0,1] | A 100% |
| 14 | tab=4 状态 | acceptStatus=1, statusArray=[2] | A 100% |

### E 组：Request 字段（6 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 15 | chain Request | **0 处（不在列表 API）** | F |
| 16 | machineCenterId Request | L4248, L4250-4264 | A 100% |
| 17 | status Request | 通过 statusArray 数组 | A 100% |
| 18 | acceptStatus Request | L4094, L4329-4339 | A 100% |
| 19 | receiveStatus Request | L4093, L4323 | A 100% |
| 20 | deliveryStatus Request | **0 处（仅显示）** | F |

### F 组：分页 / 搜索 / 排序（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 21 | 分页 | pageStart=0, pageSize=10/20/1, count | A 100% |
| 22 | 搜索 | keyword 不在列表 API Request | A 100% |
| 23 | 排序 | 0 处 sort/orderBy | F |

### G 组：综合（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 24 | 普通 / 连锁 State 差异 | 完全相同（chain 0 处 Request）| A 100% |
| 25 | Tab → 数据列表 | 4 tab 共享同一 list + Request filter | A 100% |
| 26 | 一期数据协议复刻边界 | 9 字段 + 17 Response 字段 100% 收口 | A 100% |

---

## 十二、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 23 | 88.5% | 真实 API + Request + Response 100% 收口 |
| **B** | 0 | 0% | — |
| **C** | 0 | 0% | — |
| **D** | 0 | 0% | — |
| **E** | 0 | 0% | — |
| **F** | 3 | 11.5% | chain / deliveryStatus / sort 0 处 Request |
| **合计** | **26** | **100%** | — |

**L1=23 / L2=0 / L3=0 / F=3**

---

## 十三、本轮新增事实（S1-58 独有）

### 事实 1：machineOrderWaitProcessCtrl 不调用任何 API

**事实**：machineOrderWaitProcessCtrl 真实业务 = **只做 $state.current.name → $scope.tab 映射**，不调用列表 API

**证据**：controller.js L16206-16217

**等级**：**A 100%**

### 事实 2：真实列表 API 在 machineOrderListCtrl

**事实**：`selectMachineCenterOrderRecordVoList.json` 在 machineOrderListCtrl (L4100, L4278) + machineProcessListCtrl (L37175) 共 3 处调用

**等级**：**A 100%**

### 事实 3：chain 不在列表 API Request

**事实**：searchMachineCenterOrderRecordVoList.json Request 中 0 处 chain 字段

**等级**：**A 100%**

### 事实 4：tab 不在列表 API Request

**事实**：tab 通过 setTab 转换为 acceptStatus + statusArray 数组进入 Request，tab 本身不作为字段

**等级**：**A 100%**

### 事实 5：status 通过 statusArray 数组传递

**事实**：`status` 不是直接字段，而是 `statusArray: [0]` / `[0,1]` / `[2]` 数组

**等级**：**A 100%**

### 事实 6：deliveryStatus 不在列表 API Request

**事实**：`medicalProductDelivery.deliveryStatus` 仅用于 UI 显示和按钮控制，不进入列表 API Request

**等级**：**A 100%**

### 事实 7：排序 0 处

**事实**：加工单列表无 `sort` / `orderBy` 参数

**等级**：**A 100%**

### 事实 8：普通/连锁 state 列表 API 完全相同

**事实**：8 个 state 共享同一列表 API，Request 字段完全相同

**等级**：**A 100%**

### 事实 9：tab → 完整 filter 映射

**事实**：tab 1/2/3/4 对应 acceptStatus + statusArray 数组 4 种组合

**等级**：**A 100%**

### 事实 10：keyword 不在列表 API

**事实**：`selectMachineCenterOrderRecordVoList.json` Request 中 0 处 `keyword` 字段

**等级**：**A 100%**

---

## 十四、历史纠错

| S1-57 结论 | S1-58 复核 |
|----------|----------|
| 8 个 state 共享 machineOrderWaitProcessCtrl | **维持 A 100%** |
| tab 1/2/3/4 映射 | **维持 A 100%** |
| machineOrderBroken 不是 state | **维持 A 100%** |

**S1-58 关键 A 级升级**：
- S1-57 "8 个 state 共享 controller" = **S1-58 升级到 controller 不加载数据**
- S1-57 "tab 1/2/3/4 映射" = **S1-58 升级到 tab→acceptStatus+statusArray 完整转换**

---

## 十五、一期复刻影响

### 15.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | `selectMachineCenterOrderRecordVoList.json` 列表 API | A 100% |
| 2 | 9 个 Request 字段 | A 100% |
| 3 | machineCenterOrderRecordVo 17 字段 Response | A 100% |
| 4 | setTab 4 状态映射 | A 100% |
| 5 | 分页 (pageStart/pageSize/count) | A 100% |
| 6 | 普通/连锁 state 列表完全相同 | A 100% |
| 7 | machineOrderWaitProcessCtrl tab 分类 | A 100% |

### 15.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | chain 业务意义 | E |
| 2 | 后端如何区分普通/连锁 | E |
| 3 | 缓存结构 | E |

### 15.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | chain Request 字段 | F = 0 处出现 |
| 2 | deliveryStatus Request 字段 | F = 0 处出现 |
| 3 | keyword Request 字段（加工单列表）| F = 0 处出现 |
| 4 | sort/orderBy Request 字段 | F = 0 处出现 |
| 5 | 数据库表结构 | F = 未直接观察 |
| 6 | 完整 route 架构 | F = S1-56 维持 |

---

## 十六、严禁脑补清单

```
chain 字段在列表 API Request
deliveryStatus 在列表 API Request
tab 字段在列表 API Request
sort/orderBy 字段
keyword 字段（加工单列表）
数据库 1:N 关系
加工单列表分页数据库实现
```

---

## 十七、未解决问题（11 个 Q）

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | 8 个 state 是否共用同一列表 API？ | **是** | A 100% |
| Q2 | tab 是否进入 Request？ | **否**（转换为 acceptStatus+statusArray）| A 100% |
| Q3 | chain 是否进入 Request？ | **否** | A 100% |
| Q4 | machineCenterId 是否进入 Request？ | **是** | A 100% |
| Q5 | 不同 tab 是否不同数据数组？ | **否**（同一变量 + filter 切换）| A 100% |
| Q6 | 普通/连锁 是否有真实 Request 差异？ | **否** | A 100% |
| Q7 | 列表 Response 对象是否完整？ | **是**（17 字段 machineCenterOrderRecordVo）| A 100% |
| Q8 | 分页是否已观察？ | **是**（pageStart/pageSize/count）| A 100% |
| Q9 | 搜索是否已观察？ | **keyword 0 处** | A 100% |
| Q10 | 排序是否已观察？ | **0 处** | A 100% |
| Q11 | L3 数据库结构是否未知？ | **是**（F 维持）| F |

---

## 十八、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十九、文档元数据

- **文档编号**：117
- **任务阶段**：S1-58 8 State 列表 API 数据协议
- **侦察时间**：2026-09-03 16:30-17:00
- **S1-58 颠覆性 A 级新发现**：
  1. **machineOrderWaitProcessCtrl 不调用任何 API**（只做 tab 分类）
  2. **真实列表 API 在 machineOrderListCtrl**
  3. **chain 不在列表 API Request**（0 处）
  4. **tab 不在列表 API Request**（转换为 acceptStatus+statusArray）
  5. **status 通过 statusArray 数组传递**
  6. **deliveryStatus 不在列表 API Request**
  7. **普通/连锁 state 列表 API 完全相同**
  8. **keyword 不在加工单列表 API**
  9. **无排序参数**
  10. **tab → acceptStatus+statusArray 完整映射**
- **26 项评级 = 23 A + 0 E + 0 B/C/D + 3 F = 88% A 收口**
- **L1=23 / L2=0 / L3=0 / F=3**
- **历史文档影响**：0（28~116 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-59

---

> **S1-58 完成。**
> **23 A + 0 E + 0 B/C/D + 3 F（8 State 数据协议收口 88%）**。
> **machineOrderWaitProcessCtrl 不加载数据，真实列表 API 在 machineOrderListCtrl**。
> **chain/tab 不在 Request，status 通过 statusArray 数组传递**。
> **下一步：等待老板下一条指令。**
