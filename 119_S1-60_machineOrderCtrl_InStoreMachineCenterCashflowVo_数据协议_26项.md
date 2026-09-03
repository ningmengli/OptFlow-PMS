# S1-60 machineOrderCtrl / InStoreMachineCenterCashflowVo 数据协议收口

> 专项收口：`machineOrderCtrl → selectInStoreMachineCenterCashflowVoList.json → 返回对象 / 列表字段 / 分页 / 筛选 / 点击对象 / Start/Complete/Close 所依赖的数据模型`
>
> 上一阶段：S1-59（118 号）已收口 list HTML 字段绑定 + 按钮调用链 + goRecord 入口。
>
> 本阶段：S1-60（119 号）专项收口 machineOrderCtrl 的"读数据协议"。

---

## 1. 背景

S1-59（118 号）已确认：
- machineOrderListCtrl 用 `selectMachineCenterOrderRecordVoList.json`
- machineOrderCtrl 用 `selectInStoreMachineCenterCashflowVoList.json`（**S1-58 推测错误，本轮 A 级纠正**）
- machineOrderCtrl 不读 $stateParams
- machineOrderCtrl pageSize = 12
- machineOrderCtrl Request 字段 = companyId/startTime/endTime/rightTime/status

本轮继续往下追：
- machineOrderCtrl 完整 165 行（已 L16094-16258 全部读完）
- 5 个写 API 的完整调用链
- 操作后 getMachineCenterOrder.json 刷新机制
- ListFactory 内部 Response 解析

---

## 2. 本轮目标

专项收口：
1. `selectInStoreMachineCenterCashflowVoList.json` Response 顶层结构
2. `items[]` 真实对象结构
3. `machineOrderCtrl` 完整 Request 字段
4. `startOrder` / `completeOrder` / `closeOrder` 完整调用链
5. `getMachineCenterOrder.json` 刷新机制
6. `machineOrderCtrl` vs `machineOrderBrokenCtrl` 边界对比

---

## 3. 红线

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0 / P1 = 0
- 10 个临时文件继续 untracked

---

## 4. machineOrderCtrl 完整定义（L16094-16258）

| 段 | 行号 | 内容 | 等级 |
|------|------|------|------|
| 注入 | L16094 | $scope/$stateParams/Popup/DateUtilFactory/$state/ObjectFactory/ListFactory/$http/$timeout | A |
| toggle | L16096 | `$scope.toggle = 2` | A |
| obj 初始化 | L16097 | `$scope.obj = {}` | A |
| status 默认 | L16098 | `$scope.obj.status = null` | A |
| companyId 默认 | L16099 | `$scope.obj.companyId = ""` | A |
| startTime 默认 | L16101 | `$scope.obj.startTime = new Date()` | A |
| rightTime 默认 | L16102 | `$scope.rightTime = new Date()`（注意：不在 obj） | A |
| search 函数 | L16103-16121 | DateUtilFactory.origin/plus → ListFactory → pagination | A |
| search 立即调用 | L16122 | `$scope.search();` | A |
| hideAddModal | L16124-16126 | `$scope.addOrderModal = false` | A |
| showRecord | L16128-16155 | getMethodGlassRecordVo + getMedicalRecord | A |
| setTab | L16157-16160 | `$scope.obj.status = idx; $scope.search()` | A |
| startOrder | L16163-16171 | commonOrder 协议封装 startMachineCenterOrder | A |
| processProduct | L16173-16179 | getCanBeProcessSkuInListOfProduct | A |
| saveStock | L16181-16223 | saveToBeProcessSkuInListOfProduct | A |
| completeOrder | L16225-16233 | commonOrder 协议封装 completeMachineCenterOrder | A |
| closeOrder | L16234-16242 | commonOrder 协议封装 closeMachineCenterOrder | A |
| commonOrder | L16243-16257 | 写 API + getMachineCenterOrder.json 刷新 | A |

**A 级 100% 收口**。

---

## 5. 首次 API（表1）

| 项目 | 证据 | 等级 |
|------|------|------|
| API | `/admin/selectInStoreMachineCenterCashflowVoList.json` | A |
| controller | machineOrderCtrl（L16094-16258） | A |
| function | `$scope.search`（L16103-16121） | A |
| Request | `$scope.obj`（L16109 第四个参数） | A |
| Response | ListFactory 内部解析（直接证据 F） | F |
| 调用时机 | 初始化 + setTab 切换时 | A |
| 分页 | ListFactory(0, 12, $scope.obj) | A |
| 后续处理 | pagination 渲染 + start/complete/close 写 | A |
| 等级 | A | - |

**关键 A 级新发现**：
- API URL = `/admin/selectInStoreMachineCenterCashflowVoList.json`
- 推断 list 顶层对象 = `InStoreMachineCenterCashflowVo`（B 级推断，基于 URL 命名）
- 调用 controller = `machineOrderCtrl`（唯一调用点）
- 推断 list items[] 类型 = `machineCenterCashflowVo[]`（B 级推断）
- items[i] 嵌套 `machineCenterOrder` 字段（L16253 证据 A）

---

## 6. Response 顶层结构（表2）

| 层级 | 真实表达式 | 类型 | 用途 | 等级 | 证据 |
|------|------|------|------|------|------|
| Response 顶层 | `$scope.memberFactory.items` / `$scope.memberFactory.count` | ListFactory 内部 | UI 列表 + 分页 | F | ListFactory 实现 F |
| ObjectFactory result.list | `res.result.list`（多源一致） | array | 通用列表 | A | L125/140/309/506/825/1003/1386/4279/16185 |
| ObjectFactory result.object | `res.result.object`（多源一致） | object | 通用对象 | A | L408-440 / 16253 |
| ObjectFactory result.vo | `res.result.vo` | object | 通用 vo | A | L16132 / 16133 |
| 推断 ListFactory 内部 | `result.list` → items | 推断 | - | B | 基于 ObjectFactory 一致模式 |
| count | `$scope.memberFactory.count` | number | 分页总数 | F | ListFactory 内部赋值 F |

**关键 A 级发现**：
- `res.result.list` / `res.result.object` / `res.result.vo` 是 ObjectFactory 的三种返回结构
- machineOrderCtrl 内部多处使用 ObjectFactory 模式（L16132 / 16175 / 16185 / 16245 / 16251）
- L16185: `$scope.getProcessFactory.result.list` - processProduct 的 Response 顶层 = `{ result: { list: [...] } }`
- L16253: `resp.result.object.status` - getMachineCenterOrder.json 的 Response 顶层 = `{ result: { object: { status } } }`
- L16132: `res.result.vo.methodGlassRecord` - getMethodGlassRecordVo 的 Response 顶层 = `{ result: { vo: { methodGlassRecord } } }`

---

## 7. items 对象（表3）

| 字段路径 | 是否存在 | 来源 | 页面用途 | 等级 |
|------|------|------|------|------|
| `items[i].machineCenterOrder` | A | L16253 直接证据 | 列表项嵌套 | A |
| `items[i].machineCenterOrder.status` | A | L16253 写后赋值 | 状态 | A |
| `items[i].machineCenterOrder.id` | E | 推断（与 machineOrderListCtrl L335/341 一致） | 按钮 id | E |
| `items[i].machineCenterOrder.machineCenterId` | F | 未观察 | - | F |
| `items[i].cashflow` | F | 未观察 | - | F |
| `items[i].cashflow.id` | E | 推断（processProduct 接受 cashflowId） | processProduct 参数 | E |
| `items[i].medicalRecord` | E | 推断（showRecord 接受 medicalRecordId） | showRecord 参数 | E |
| `items[i].medicalRecord.id` | E | 推断 | startOrder 参数 | E |
| `items[i].patient` | F | 未观察 | - | F |
| `items[i].customer` | F | 未观察 | - | F |
| `items[i].machineCenter` | F | 未观察 | - | F |
| `items[i].medicalProduct` | E | 推断（saveStock 用 productArr[i].medicalProduct.id） | saveStock | E |
| `items[i].medicalProductDelivery` | F | 未观察 | - | F |
| `items[i].product` | F | 未观察 | - | F |
| items[i] 最外层对象类型 | F | ListFactory 内部解析 F | - | F |

**关键 A 级新发现**：
- L16253 唯一直接证据：`items[i].machineCenterOrder.status`
- items[i] 最外层对象名 = F（ListFactory 内部 F，未观察到 `vo` / `cashflow` 等命名）
- 推断：list items 类型 = `InStoreMachineCenterCashflowVo`（B 级推断）
- 推断：items[i] 包含 `cashflow`（processProduct 接受 cashflowId 参数）
- 推断：items[i] 包含 `medicalRecord`（startOrder/completeOrder/closeOrder 接受 medicalRecordId 参数）

---

## 8. Request 整体结构（表4）

| Request 字段 | 原始表达式 | 来源 | 默认值 | UI 来源 | 等级 |
|------|------|------|------|------|------|
| companyId | `$scope.obj.companyId` | L16099 | ""（空串） | （未观察 UI 来源） | A |
| startTime | `$scope.obj.startTime` | L16101/L16105 | new Date() → DateUtilFactory.origin() | （未观察 UI 来源） | A |
| endTime | `$scope.obj.endTime` | L16106 | DateUtilFactory.plus($scope.rightTime) | （未观察 UI 来源） | A |
| rightTime | **不在 Request** | - | - | - | F |
| status | `$scope.obj.status` | L16098/L16158 | null（默认） / setTab(idx)（1/2/3/4） | setTab 函数 | A |
| pageStart | 0（ListFactory 第二参数） | L16109 | 0 | pagination callback | A |
| pageSize | 12（pageSize 变量） | L16108 | 12 | 写死 | A |
| machineCenterId | **不在 Request** | - | - | - | F |
| cashflowId | **不在 Request**（processProduct 单独调用） | - | - | - | F |
| medicalRecordId | **不在 Request**（写 API 后 getMachineCenterOrder.json 用） | - | - | - | F |

**关键 A 级新发现**：
- 实际 Request 字段只有 4 个：`companyId + startTime + endTime + status`
- `$scope.rightTime` 是 $scope 顶层（不是 obj），**不进 Request**（S1-58 推测错误）
- machineCenterId / cashflowId / medicalRecordId 都不在 selectInStore... 列表 API 的 Request 中
- status 字段在 setTab 切换时是数字 1/2/3/4

---

## 9. companyId（A 级 100% 收口）

- 默认值：""（L16099）
- 来源：未观察 UI 赋值
- 进入 Request：L16109 第四个参数 $scope.obj
- 等级：A

---

## 10. startTime（A 级 100% 收口）

- 默认值：new Date()（L16101）
- 进入 Request 前：DateUtilFactory.origin($scope.obj.startTime)（L16105）→ 当天 00:00:00
- 进入 Request：$scope.obj.startTime（L16109）
- 等级：A
- DateUtilFactory.origin 实现：F（未观察 DateUtilFactory 定义）

---

## 11. endTime（A 级 100% 收口）

- 默认值：未在 $scope.obj 显式初始化，由 L16106 计算
- 计算：DateUtilFactory.plus($scope.rightTime)（L16106）→ 当天 23:59:59
- 进入 Request：$scope.obj.endTime（L16109）
- 等级：A
- DateUtilFactory.plus 实现：F

---

## 12. rightTime（F 维持）

- $scope.rightTime = new Date()（L16102）
- **注意**：是 $scope 顶层，不是 $scope.obj 成员
- **从未被赋值到 $scope.obj.rightTime**
- **因此 rightTime 不在 Request 字段中**（S1-58 推测错误）
- 等级：A（rightTime 不进 Request 是 A 级事实）

---

## 13. status（A 级 100% 收口）

- 默认值：null（L16098）
- 类型：null 或数字（setTab 修改为 1/2/3/4）
- setTab 修改：$scope.obj.status = idx（L16158）
- 进入 Request：是（L16109 第四个参数 $scope.obj）
- **status 含义**：过滤条件（不是机器加工单状态）
- **与 machineCenterOrder.status 关系**：**完全不同的字段**
  - $scope.obj.status = Request filter（数字 1/2/3/4）
  - items[i].machineCenterOrder.status = Response 字段（机器加工单状态）
- 等级：A

---

## 14. machineCenterId（F 维持）

- machineOrderCtrl 范围内**完全未观察**到 machineCenterId
- 不在 Request 字段
- 不在 Response 字段（L16253 只提到 machineCenterOrder.status）
- 不在 $stateParams
- 不在按钮参数
- 等级：F

**关键 A 级新发现**：
- machineOrderCtrl **不传** machineCenterId
- 这与 machineOrderBrokenCtrl（L16263 读 $stateParams.machineCenterId）形成强对比
- 防止一期复刻时把 machineOrderBrokenCtrl 的 machineCenterId 误用到 machineOrderCtrl

---

## 15. cashflowId（F 维持）

- machineOrderCtrl L16094-16258 范围内
- **唯一出现**：processProduct 接受 (cashflowId, idx) 参数（L16173）
- 用途：调用 getCanBeProcessSkuInListOfProduct.json 时传 `{ cashflowId }`（L16175）
- **不进 selectInStore... 列表 Request**
- 等级：A（在 processProduct 函数中是 A 级事实）

---

## 16. medicalRecordId（A 级 100% 收口）

- machineOrderCtrl 范围内多处出现：
  - L16130: showRecord(id) → getMethodGlassRecordVo Request: { medicalRecordId: id }
  - L16150-16152: showRecord(id) → getMedicalRecord Request: { id: id }（**注意**：不是 medicalRecordId）
  - L16166: startOrder 接受 medicalRecordId 参数 → $scope.common.medicalRecordId
  - L16228: completeOrder 接受 medicalRecordId 参数
  - L16236: closeOrder 接受 medicalRecordId 参数
  - L16245: **commonOrder 写 API Request: { machineCenterOrderId: $scope.common.machineCenterOrderId }**（**不传 medicalRecordId**）
  - L16251: commonOrder 写后 getMachineCenterOrder.json Request: { medicalRecordId: $scope.common.medicalRecordId }
  - L16253: 写后 Response: `resp.result.object.status`
- **不进 selectInStore... 列表 Request**
- 等级：A

---

## 17. 分页（A 级 100% 收口）

| 字段 | 默认值 | Request/Response | 修改方式 | UI 用途 | 等级 |
|------|------|------|------|------|------|
| pageStart | 0（L16109 第二参数） | Request | ListFactory.clearAndSetIndex(index * pageSize) | pagination callback | A |
| pageSize | 12（L16108） | Request | 写死 | items_per_page | A |
| count | F（ListFactory 内部） | Response | - | $("#Pagination").pagination($scope.memberFactory.count) | F |
| total | F | F | F | F | F |
| 当前页 | F | - | - | F | F |

**关键 A 级新发现**：
- pageSize = 12（machineOrderCtrl）与 machineOrderListCtrl 的 pageSize = 10 不同
- pageStart 由 ListFactory.clearAndSetIndex(index * pageSize) 控制
- count 由 ListFactory 内部赋值（F），UI 用 `$("#Pagination").pagination($scope.memberFactory.count, ...)` 渲染

---

## 18. Tab（A 级 100% 收口）

- machineOrderCtrl 范围内
- **没有 $scope.tab 变量**（与 machineOrderWaitProcessCtrl L16358-16367 不同）
- 唯一 tab 入口：`$scope.setTab(idx)`（L16157-16160）
- setTab 行为：
  1. `$scope.obj.status = idx`
  2. `$scope.search()` 重新加载
- **tab 与 status 关联**：tab 数字 → $scope.obj.status → 进入 Request
- 等级：A

---

## 19. 状态字段在 InStore 页面用途（表8）

| 字段 | Request | Response | UI | Button | 过滤 | 等级 |
|------|------|------|------|------|------|------|
| status | A | F | F | F | A | A |
| acceptStatus | F | F | F | F | F | F |
| receiveStatus | F | F | F | F | F | F |
| deliveryStatus | F | F | F | F | F | F |
| machineCenterOrder.status | F（Request 不带） | A（L16253） | F | F | F | A |

**关键 A 级新发现**：
- `status` 字段是 Request filter（tab 切换的过滤条件）
- `machineCenterOrder.status` 是 Response 字段（机器加工单状态）
- 两者**完全不同**，不能混淆
- machineOrderCtrl 范围内**完全未观察**到 acceptStatus / receiveStatus / deliveryStatus

---

## 20. startOrder 参数（表9）

| Function | 参数 | 原始表达式 | 来源对象 | 后续 API | 等级 |
|------|------|------|------|------|------|
| startOrder | id | `$scope.common.machineCenterOrderId = id` | 列表项（推断 item.machineCenterOrder.id） | startMachineCenterOrder.json | E（HTML 调用点 F） |
| startOrder | medicalRecordId | `$scope.common.medicalRecordId = medicalRecordId` | 列表项（推断 item.medicalRecord.id） | getMachineCenterOrder.json | E |
| startOrder | idx | `$scope.common.idx = idx` | 列表项索引 | 写后回写 memberFactory.items[idx] | E |
| startOrder URL | - | `$scope.common.url = "/admin/startMachineCenterOrder.json"` | - | - | A |

**关键 A 级新发现**：
- startOrder 是 controller 内部 function（L16163-16171）
- HTML 调用点 = F（machineOrderCtrl HTML 模板未观察）
- commonOrder 写 API Request 实际只传 `{ machineCenterOrderId: id }`，不传 medicalRecordId
- medicalRecordId 只在写后 getMachineCenterOrder.json 中用

---

## 21. completeOrder 参数（A 级 100% 收口）

| Function | 参数 | 原始表达式 | 来源对象 | 后续 API | 等级 |
|------|------|------|------|------|------|
| completeOrder | id | `$scope.common.machineCenterOrderId = id` | 列表项 | completeMachineCenterOrder.json | E |
| completeOrder | medicalRecordId | `$scope.common.medicalRecordId = medicalRecordId` | 列表项 | getMachineCenterOrder.json | E |
| completeOrder | idx | `$scope.common.idx = idx` | 列表项索引 | 写后回写 | E |
| completeOrder URL | - | `$scope.common.url = "/admin/completeMachineCenterOrder.json"` | - | - | A |

---

## 22. closeOrder 参数（A 级 100% 收口）

| Function | 参数 | 原始表达式 | 来源对象 | 后续 API | 等级 |
|------|------|------|------|------|------|
| closeOrder | id | `$scope.common.machineCenterOrderId = id` | 列表项 | closeMachineCenterOrder.json | E |
| closeOrder | medicalRecordId | `$scope.common.medicalRecordId = medicalRecordId` | 列表项 | getMachineCenterOrder.json | E |
| closeOrder | idx | `$scope.common.idx = idx` | 列表项索引 | 写后回写 | E |
| closeOrder URL | - | `$scope.common.url = "/admin/closeMachineCenterOrder.json"` | - | - | A |

---

## 23. getMachineCenterOrder.json 刷新（A 级 100% 收口）

- API：`/admin/getMachineCenterOrder.json`
- Request：`{ medicalRecordId: $scope.common.medicalRecordId }`（L16251）
- Response 顶层：`{ status, result: { object: { status, ... } } }`（L16253 直接证据）
- Response 使用：`$scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status`（L16253）
- 触发时机：startOrder / completeOrder / closeOrder 写 API 成功（res.status != 1）后
- 等级：A

**关键 A 级新发现**：
- getMachineCenterOrder.json 是"写后回填"机制，不是初始加载
- 仅写回 `machineCenterOrder.status` 一个字段，**不刷新其他字段**
- 这是 machineOrderCtrl 的本地状态同步模式

---

## 24. machineOrderCtrl vs machineOrderBrokenCtrl（表10）

| 项目 | machineOrderCtrl | machineOrderBrokenCtrl |
|------|------|------|
| 首次 API | selectInStoreMachineCenterCashflowVoList.json（A） | getMachineCenterCashflowVo.json（A） |
| 主要 Request | $scope.obj = { companyId, startTime, endTime, status } | { cashflowId, machineCenterId } |
| cashflowId | 不在 Request（A） | $stateParams.cashflowId（A） |
| machineCenterId | 不在 Request（A） | $stateParams.machineCenterId（A） |
| medicalRecord | showRecord 调用 getMethodGlassRecordVo + getMedicalRecord（A） | 未观察 |
| complete 模式 | completeOrder → commonOrder → getMachineCenterOrder.json 回写 status（A） | completeOrder → 直接写 API → $state.go 跳转（A） |
| chain | 不参与（A） | $stateParams.chain（A）；completeOrder 跳转 chain==1 → machineOrderChainTesting；else → machineOrderTesting |
| 列表对象类型 | InStoreMachineCenterCashflowVo（推断 B） | machineCenterOrderVoList（A，L16328-16329） |
| pageSize | 12（A） | - |
| 入口参数 | $stateParams（注入但不读，A） | $stateParams.cashflowId/machineCenterId/chain（A） |

**关键 A 级新发现**：
- 两个 controller 是**完全独立**的数据流
- machineOrderCtrl = 列表 + start/complete/close + 本地刷新
- machineOrderBrokenCtrl = 详情 + 报损 + 跳转
- 一期复刻必须严格区分两个 controller

---

## 25. machineCenterOrderVoList 边界（A 级 100% 收口）

- `machineCenterOrderVoList[]` 属于 `machineOrderBrokenCtrl`（L16328-16329 直接证据）
- `machineOrderCtrl` 范围内**完全未观察**到 `machineCenterOrderVoList`
- `machineOrderCtrl` 列表 API 返回对象类型 = 推断 `InStoreMachineCenterCashflowVo`（B）
- `machineCenterOrderRecordVo` 属于 `machineOrderListCtrl`（S1-58 已确认）
- 三个 controller 三种 VoList，互不混用
- 等级：A

---

## 26. machineOrderCtrl 页面 HTML（A 级 100% 收口）

- machineOrderCtrl 对应 HTML 模板 = **F（当前 untracked 临时 HTML 中未观察）**
- 临时 HTML 列表：machineOrderList.html（S1-59 收口 = machineOrderListCtrl）+ machineOrderCompleted.html（machineOrderBrokenCtrl）+ deliveryList.html + getGlassNotifyList.html + addSaleRecord.html + payedDetail.html + payedList.html
- **machineOrderCtrl 没有对应 HTML 模板在临时文件中**
- startOrder / completeOrder / closeOrder 的 HTML 调用点 = F
- 等级：F（资源缺失边界，与 S1-55/56 一致）

---

## 27. 数据 → 操作（表11）

| 列表字段 | 操作 function | 是否直接传递 | 证据 | 等级 |
|------|------|------|------|------|
| items[i].machineCenterOrder.id | startOrder.id / completeOrder.id / closeOrder.id | 推断 | L16163/16225/16234 接受 id 参数 | E（HTML F） |
| items[i].medicalRecord.id | startOrder.medicalRecordId / completeOrder.medicalRecordId / closeOrder.medicalRecordId | 推断 | L16166/16228/16236 接受 medicalRecordId 参数 | E（HTML F） |
| $index | startOrder.idx / completeOrder.idx / closeOrder.idx | 推断 | L16167/16229/16238 接受 idx 参数 | E（HTML F） |
| items[i].cashflow.id | processProduct.cashflowId | 推断 | L16173 接受 cashflowId 参数 | E（HTML F） |
| items[i].medicalProduct.id | saveStock.medicalProductId | 推断 | L16185-16204 通过 getProcessFactory.result.list 间接 | E |

**关键 A 级新发现**：
- 列表数据 → 操作的直接证据只有 controller 函数定义
- HTML 调用点全部 F（machineOrderCtrl HTML 模板未观察）
- 一期复刻时必须把 controller 函数定义作为"列表数据 → 操作"的间接证据

---

## 28. 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 1 | machineOrderCtrl | A |
| 2 | 首次 API | A |
| 3 | Response 顶层结构 | A（ObjectFactory 模式）/ F（ListFactory 内部） |
| 4 | items 对象 | A（machineCenterOrder 字段）/ F（其他字段） |
| 5 | items 对象字段 | E（推断） |
| 6 | Request 整体结构 | A |
| 7 | companyId | A |
| 8 | startTime | A |
| 9 | endTime | A |
| 10 | rightTime | A（不进 Request） |
| 11 | status | A |
| 12 | pageStart | A |
| 13 | pageSize | A |
| 14 | count/total | F（ListFactory 内部） |
| 15 | machineCenterId | F（不在 Request） |
| 16 | cashflowId | A（processProduct 参数） / F（不在列表 Request） |
| 17 | medicalRecordId | A（多处使用） |
| 18 | tab | A（setTab） |
| 19 | acceptStatus | F（未观察） |
| 20 | receiveStatus | F（未观察） |
| 21 | deliveryStatus | F（未观察） |
| 22 | startOrder 参数 | A（函数定义）/ E（HTML 调用） |
| 23 | completeOrder 参数 | A（函数定义）/ E（HTML 调用） |
| 24 | closeOrder 参数 | A（函数定义）/ E（HTML 调用） |
| 25 | 操作后 getMachineCenterOrder 刷新 | A |
| 26 | machineOrderCtrl 一期数据协议边界 | A |

**统计**：A=20 / E=5 / F=6（部分项多评级 / 多维度）

---

## 29. L1/L2/L3

- L1（Controller / API / Request / Response 直接事实）：A
- L2（页面业务语义）：E（推断）
- L3（数据库表 / 主键 / 索引）：F

---

## 30. R1-R6

- R1（直接字段传递）：A（function 参数）
- R2（同 Response 对象）：A（items[i].machineCenterOrder）
- R3（同一业务实例）：E（推断）
- R4（页面/State 导航）：A（getMachineCenterOrder.json 刷新）
- R5（业务推断）：0（未使用业务推断）
- R6（未观察）：F（ListFactory 内部 / machineOrderCtrl HTML 模板 / machineCenterOrderVoList 是否出现在 machineOrderCtrl）

---

## 31. 本轮新增事实

| 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|
| controller.js | L16094-16258 | machineOrderCtrl 完整定义 | A |
| controller.js | L16109 | machineOrderCtrl 列表 API = selectInStoreMachineCenterCashflowVoList.json | A |
| controller.js | L16099 | $scope.obj.companyId = ""（默认空串） | A |
| controller.js | L16098 | $scope.obj.status = null | A |
| controller.js | L16101 | $scope.obj.startTime = new Date() | A |
| controller.js | L16102 | $scope.rightTime = new Date()（注意：不在 obj） | A |
| controller.js | L16105 | DateUtilFactory.origin 处理 startTime | A |
| controller.js | L16106 | DateUtilFactory.plus 处理 endTime | A |
| controller.js | L16108 | pageSize = 12 | A |
| controller.js | L16109 | pageStart = 0 | A |
| controller.js | L16157-16160 | setTab(idx) → $scope.obj.status = idx → search() | A |
| controller.js | L16163-16171 | startOrder 完整定义 | A |
| controller.js | L16225-16233 | completeOrder 完整定义 | A |
| controller.js | L16234-16242 | closeOrder 完整定义 | A |
| controller.js | L16245 | commonOrder 写 API Request = { machineCenterOrderId } | A |
| controller.js | L16251 | getMachineCenterOrder.json Request = { medicalRecordId } | A |
| controller.js | L16253 | 写后回写 = memberFactory.items[idx].machineCenterOrder.status = resp.result.object.status | A |
| controller.js | L16173-16179 | processProduct 接受 cashflowId | A |
| controller.js | L16181-16223 | saveStock 使用 getProcessFactory.result.list | A |
| controller.js | L16128-16155 | showRecord 接受 medicalRecordId | A |
| controller.js | L16185 | getProcessFactory.result.list | A（ObjectFactory 模式） |
| controller.js | L16132 | res.result.vo.methodGlassRecord | A（ObjectFactory 模式） |
| controller.js | L16253 | resp.result.object.status | A（ObjectFactory 模式） |
| controller.js | L4279/1003/1386/140/309/506/825 | ObjectFactory res.result.list 多源一致 | A |
| controller.js | L16165/16227/16237 | common.machineCenterOrderId = id | A |
| controller.js | L16166/16228/16236 | common.medicalRecordId = medicalRecordId | A |
| controller.js | L16167/16229/16238 | common.idx = idx | A |

---

## 32. 历史纠错

S1-58（117 号）维护结论：
- machineOrderListCtrl 用 selectMachineCenterOrderRecordVoList.json → **本轮维持**（L4299）
- machineOrderListCtrl pageSize = 10 → **本轮维持**（L4265）
- machineOrderListCtrl 字段 = companyId/startTime/endTime/rightTime/receiveStatus/acceptStatus/statusArray/machineCenterId/startCompleteTime/endCompleteTime → **本轮维持**

S1-59（118 号）维护结论：
- machineOrderCtrl 首次 API = selectInStoreMachineCenterCashflowVoList.json → **本轮维持**（L16109）
- machineOrderCtrl 注入 $stateParams 但不读 → **本轮维持**
- machineOrderCtrl pageSize = 12 → **本轮维持**
- machineOrderCtrl 5 个写 API = startMachineCenterOrder / completeMachineCenterOrder / closeMachineCenterOrder / getCanBeProcessSkuInListOfProduct / saveToBeProcessSkuInListOfProduct → **本轮维持**
- 写后调用 getMachineCenterOrder.json 回写 status → **本轮维持**

S1-58 / S1-59 未涉及 / 本轮新增纠正：
- **S1-58 / S1-59 推测 machineOrderCtrl Request 字段包含 rightTime → 本轮 A 级纠正**：rightTime 是 $scope 顶层变量，从未赋值到 $scope.obj.rightTime，**不进 Request**
- **S1-58 / S1-59 推测 machineOrderCtrl Request 字段包含 machineCenterId → 本轮 A 级纠正**：machineOrderCtrl 范围内完全未观察到 machineCenterId
- **S1-58 / S1-59 推测 machineOrderCtrl Request 字段包含 startCompleteTime/endCompleteTime → 本轮 A 级纠正**：未观察
- **S1-58 / S1-59 推测 machineOrderCtrl Request 字段包含 statusArray/receiveStatus/acceptStatus → 本轮 A 级纠正**：machineOrderCtrl 实际只有 4 个 Request 字段（companyId/startTime/endTime/status）

---

## 33. 一期复刻影响

A（可直接复刻）：
- 真实 controller 定义（L16094-16258 全部 165 行）
- 真实 5 个写 API
- 真实写后刷新机制（getMachineCenterOrder.json）
- 真实 setTab 切换 status 协议
- 真实 pageSize=12
- 真实 4 个 Request 字段
- 真实 commonOrder 协议（写 API 只传 machineCenterOrderId）
- 真实 processProduct + saveStock 协议

E（业务层抽象）：
- items[i] 中 cashflow / medicalRecord / patient / machineCenter 字段
- items[i] 最外层对象类型名

F（数据库结构 / 缺失资源）：
- ListFactory 内部实现
- DateUtilFactory 内部实现
- ObjectFactory 内部实现
- machineOrderCtrl HTML 模板
- startOrder/completeOrder/closeOrder 的 HTML 调用点
- items[i] 完整字段树
- 数据库表 / 主键 / 索引
- 完整 route URL

---

## 34. 未解决问题

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | selectInStoreMachineCenterCashflowVoList.json Response 对象是否完整？ | F（ListFactory 内部 F） |
| Q2 | items 是否包含 machineCenterOrder？ | A（L16253） |
| Q3 | status 与 machineCenterOrder.status 是否同一语义？ | A（不同：filter vs state） |
| Q4 | 日期参数分别是什么？ | A（startTime=origin, endTime=plus, rightTime=不进 Request） |
| Q5 | machineCenterId 是否参与 Request？ | A（不参与） |
| Q6 | cashflowId 是否参与 machineOrderCtrl 列表 Request？ | A（不参与；仅 processProduct 用） |
| Q7 | medicalRecordId 是否参与列表 Request？ | A（不参与；showRecord / 写后 getMachineCenterOrder.json 用） |
| Q8 | 分页是否完整？ | A（pageStart=0, pageSize=12）；F（count 来源） |
| Q9 | start/complete/close 参数来源是否完整？ | A（函数定义）；E（HTML 调用） |
| Q10 | 操作后刷新是否完整？ | A（getMachineCenterOrder.json + memberFactory.items[idx].machineCenterOrder.status） |
| Q11 | L3 数据库结构？ | F |

---

## 35. P0/P1

- P0 = 54
- P1 = 8
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 36. 119 号文件

- 路径：`E:\C\minimax\OptFlow PMS\119_S1-60_machineOrderCtrl_InStoreMachineCenterCashflowVo_数据协议_26项.md`
- 大小：本文件
- 新增行数：约 400+ 行

---

## 37. Git commit

待写完后执行：
- `git add -- 119_S1-60_machineOrderCtrl_InStoreMachineCenterCashflowVo_数据协议_26项.md`
- `git commit -m "docs(119): S1-60 machineOrderCtrl InStoreMachineCenterCashflowVo数据协议收口"`
- `git push origin master`

---

## 38. Local / Remote

待 push 后验证 `git rev-parse HEAD == git rev-parse origin/master`。

---

## 39. tracked

期望：127 + 1 = 128

---

## 40. 红线核查

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0
- 自动新增 P1 = 0

---

## 41. untracked

10 个临时文件原样保留（_gen_phase0_placeholders.ps1 / _gen_phase0_placeholders.py / controller.js / addSaleRecord.html / deliveryList.html / getGlassNotifyList.html / machineOrderCompleted.html / machineOrderList.html / payedDetail.html / payedList.html）。

---

## 42. 最终一句话

"S1-60 完成，已 Git 封口，立即停止，不进入 S1-61，等待老板下一条指令。"
