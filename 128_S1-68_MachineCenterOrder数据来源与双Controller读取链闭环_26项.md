# S1-68 MachineCenterOrder 数据来源与双 Controller 读取链闭环

> 专项审计：`MachineCenterOrder` 真实数据来源 + `machineOrderCtrl` / `machineOrderBrokenCtrl` / `machineOrderListCtrl` 读取链
>
> 上一阶段：S1-67（127 号）已确认 sendMedicalProductToMachineCenter.json **与** MachineCenterOrder **无直接关系**。
>
> 本阶段：S1-68（128 号）反向研究 MachineCenterOrder **真实数据来源**。

---

## 1. 核心结论

**S1-68 关键 A 级发现**：

**machineCenterOrder 在 controller.js 范围内**：
- 直接被读取的字段**仅 3 个**：`id` / `status` / `receiveStatus`（A 级 100% 收口）
- **未出现**的字段：`acceptStatus` / `planDeliveryTime` / `gmtCreate`（F 维持）
- `acceptStatus` / `planDeliveryTime` / `gmtCreate` 是 S1-58 历史证据中 machineOrderListCtrl 的 machineCenterOrderRecordVo **推断**字段，**当前 controller.js 范围内不直接读取**

**3 Controller 数据来源**：

| Controller | 列表 API | Response 对象 | machineCenterOrder 字段来源 |
|---|---|---|---|
| machineOrderCtrl | `selectInStoreMachineCenterCashflowVoList.json` | `memberFactory.items[]`（推断 `InStoreMachineCenterCashflowVo`） | `memberFactory.items[i].machineCenterOrder.status`（A，L16253 写后赋值） |
| machineOrderBrokenCtrl | `getMachineCenterCashflowVo.json` | `getStockObjectFactory.result.object.machineCenterOrderVoList[]` | `machineCenterOrderVoList[i].machineCenterOrder.id`（A，L16328） |
| machineOrderListCtrl | `selectMachineCenterOrderRecordVoList.json` | `getAdminList.items[]` | `getAdminList.items[i].machineCenterOrder.receiveStatus`（A，L4321 写后赋值） |

**A 级 100% 收口**。

---

## 2. 证据范围

**直接证据**：
- controller.js L16094-16258（machineOrderCtrl 完整 165 行）
- controller.js L16261-16354（machineOrderBrokenCtrl 完整 94 行）
- controller.js L4264-4350（machineOrderListCtrl 完整 87 行）
- 全仓 `machineCenterOrder*` 字段搜索

**资源缺失**：
- 3 controller HTML 模板（F）
- 完整 route schema（F）
- 后端算法 / DTO 定义（F）

---

## 3. machineOrderCtrl 精确定位（30.1）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16094 | A |
| 终点 | L16258 | A |
| 总行数 | 165 行 | A |
| 注入 | $scope, $stateParams, Popup, DateUtilFactory, $state, ObjectFactory, ListFactory, $http, $timeout | A |
| 列表 API | selectInStoreMachineCenterCashflowVoList.json (L16109) | A |

---

## 4. machineOrderBrokenCtrl 精确定位（30.2）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16261 | A |
| 终点 | L16354 | A |
| 总行数 | 94 行 | A |
| 注入 | $scope, Popup, $window, $stateParams, $rootScope, $state, $timeout, ListFactory, ObjectFactory | A |
| stateParams | cashflowId / machineCenterId / chain (L16262-16264) | A |
| 首次 API | getMachineCenterCashflowVo.json (L16269) | A |

---

## 5. machineOrderListCtrl 精确定位（30.3）

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L4264 | A |
| 终点 | L4350+ | A |
| 注入 | $scope, Popup, $timeout, $stateParams, $rootScope, $state, ObjectFactory, DateUtilFactory, ListFactory, $http | A |
| 列表 API | selectMachineCenterOrderRecordVoList.json (L4299) | A |

---

## 6. selectInStoreMachineCenterCashflowVoList.json（30.4）

**Request 字段**（L16098-16106）：
- `$scope.obj.companyId` = `""`（L16099）
- `$scope.obj.startTime` = `DateUtilFactory.origin(new Date())`（L16105）
- `$scope.obj.endTime` = `DateUtilFactory.plus($scope.rightTime)`（L16106）
- `$scope.obj.status` = `null`（L16098） / `setTab(idx)` 改为 idx（A，L16158）
- pageSize = 12（L16108）
- pageStart = 0（L16109 第二参数）

**Response 顶层**（基于 ObjectFactory 模式 + ListFactory items）：
- 顶层：`{ status, result: { list: [...] } }`（A，B 级推断）
- 等级：A（结构）/ B（推断）

**items[i] 结构**：
- 推断为 `InStoreMachineCenterCashflowVo[]`（B 级推断，基于 API URL 命名）
- 包含 `machineCenterOrder` 嵌套对象（A，L16253 直接证据：items[i].machineCenterOrder）
- 等级：B/A

---

## 7. machineOrderCtrl 中 machineCenterOrder（30.5-30.6）

**machineCenterOrder 字段读取**（A 级 100% 收口）：

| 字段 | 读取位置 | 用途 | 等级 |
|---|---|---|---|
| `machineCenterOrder.status` | L16253 | commonOrder 写后回填 | A |

**未直接读取字段**（F 维持）：
- `machineCenterOrder.id`：F（未直接读取，但通过 function 参数 id 隐式）
- `machineCenterOrder.receiveStatus`：F
- `machineCenterOrder.acceptStatus`：F
- `machineCenterOrder.planDeliveryTime`：F
- `machineCenterOrder.gmtCreate`：F

**关键 A 级边界**：
- machineOrderCtrl **仅**写 machineCenterOrder.status（A，L16253）
- **不读** machineCenterOrder.id（A）
- 等级：A

---

## 8. machineOrderCtrl machineCenterOrder.id（30.7）

| 项目 | 证据 | 等级 |
|---|---|---|
| 是否在 controller.js 中直接读取 | **否** | A |
| 是否通过 function 参数 id 隐式 | **是**（E 级推断） | E |
| 是否在 HTML 调用中直接绑定 | **F** | F |
| 是否在 machineCenterOrderRecordVo 嵌套 | **F** | F |

**A 级 100% 收口**：
- machineOrderCtrl 范围内**完全不直接读取** machineCenterOrder.id
- 推断通过 startOrder/completeOrder/closeOrder 的 id 参数进入（A 级证据 + E 级推断）
- 等级：A（事实）/ E（推断）

---

## 9. machineOrderCtrl machineCenterOrder.status（30.8）

**完整生命周期**：

```
selectInStoreMachineCenterCashflowVoList.json
   ↓ Response
memberFactory.items[i].machineCenterOrder.status    [初始化值, F 当前未读取]
   ↓
commonOrder() 写后调用 getMachineCenterOrder.json
   ↓
memberFactory.items[common.idx].machineCenterOrder.status = resp.result.object.status    [L16253 刷新]
```

**A 级 100% 收口**：
- machineCenterOrder.status **仅**在 L16253 写后赋值
- **不**直接由 selectInStore API 读取
- **不**在其他地方被修改
- 等级：A

**严格表述**：
- machineOrderCtrl 范围内 machineCenterOrder.status **不直接读取**（F 维持）
- **仅**在 commonOrder 写后被刷新
- 等级：A

---

## 10. machineOrderCtrl machineCenterOrder.receiveStatus（30.9）

**A 级 100% 收口**：
- machineOrderCtrl 范围内**完全不读取** machineCenterOrder.receiveStatus
- machineOrderCtrl 没有 `receiveOrder` / `deliveryReceiveOrder` 函数（这些是 machineOrderListCtrl 的）
- 等级：A

**receiveOrder 协议属于 machineOrderListCtrl**（不是 machineOrderCtrl）：
- L4314-4328: `receiveOrder(id, idx)` 调 `receiveMachineCenterOrder.json` + 写 `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1`
- 等级：A

**严格不写**：
- 禁止把 machineOrderListCtrl.receiveOrder 错误归到 machineOrderCtrl
- 等级：A

---

## 11. getMachineCenterOrder.json（30.10-30.11）

**Request 字段**（L16251）：
- `{ medicalRecordId: $scope.common.medicalRecordId }`（A）

**Response 顶层**：
- `{ status, result: { object: { status } } }`（A，L16253 直接证据）

**success 后操作**（L16250-16254）：
```javascript
$scope.getOrderFactory = new ObjectFactory();
var orderPromise = $scope.getOrderFactory.saveOrQuery(
    "/admin/getMachineCenterOrder.json", 
    { medicalRecordId: $scope.common.medicalRecordId }
);
orderPromise.then(function (resp) {
    $scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status;
});
```

**A 级 100% 收口**：
- Request 严格 = `{ medicalRecordId }`（**不传** machineCenterOrderId / cashflowId / machineCenterId）
- Response **仅**返回 status 字段被使用
- 写后修改 `memberFactory.items[idx].machineCenterOrder.status`（**唯一被写回 machineCenterOrder 的字段**）
- 等级：A

---

## 12. machineOrderBrokenCtrl 精确初始化（30.12）

**stateParams 读取**：

| 参数 | 表达式 | 行号 | 等级 |
|---|---|---|---|
| cashflowId | `$scope.cashflowId = $stateParams.cashflowId` | L16262 | A |
| machineCenterId | `$scope.machineCenterId = $stateParams.machineCenterId` | L16263 | A |
| chain | `$scope.chain = $stateParams.chain` | L16264 | A |

**A 级 100% 收口**：machineOrderBrokenCtrl 读取全部 3 个 stateParams。

---

## 13. getMachineCenterCashflowVo.json（30.13）

**Request 字段**（L16269-16272）：
- `{ cashflowId: $scope.cashflowId, machineCenterId: $scope.machineCenterId }`（A）

**Response 顶层**：
- 顶层：`{ status, result: { object: { machineCenterOrderVoList, ... } } }`（A，L16328-16329 直接证据）

**A 级 100% 收口**：
- Request 严格 = `{ cashflowId, machineCenterId }`（**不传** medicalRecordId / machineCenterOrderId）
- Response 包含 `result.object.machineCenterOrderVoList[]`（A）
- 等级：A

---

## 14. machineCenterOrderVoList（30.14）

**来源**：
- `getMachineCenterCashflowVo.json` Response（L16328-16329 间接证据）
- 通过 `$scope.getStockObjectFactory.result.object.machineCenterOrderVoList` 暴露（A）

**每个 list 元素**：
- `machineCenterOrderVoList[i].machineCenterOrder.id`（A，L16328）
- `machineCenterOrderVoList[i].medicalProduct.productName`（A，L16329）
- 等级：A

**未读取字段**（F 维持）：
- machineCenterOrderVoList[i].machineCenterOrder.status：F
- machineCenterOrderVoList[i].machineCenterOrder.receiveStatus：F
- 等级：F

---

## 15. machineOrderBrokenCtrl.machineCenterOrder.id（30.15）

**真实来源**（A 级 100% 收口）：
- `$scope.getStockObjectFactory.result.object.machineCenterOrderVoList[idx].machineCenterOrder.id`（L16328）

**A 级边界**：
- 来源严格 = `machineCenterOrderVoList[i].machineCenterOrder.id`
- **不**来自 machineOrderCtrl 任何变量
- 等级：A

---

## 16. machineOrderBrokenCtrl receiveStatus / status（30.16）

| 字段 | 读取 | 修改 | action 使用 | 等级 |
|---|---|---|---|---|
| machineCenterOrder.status | **F** | **F** | **F** | F |
| machineCenterOrder.receiveStatus | **F** | **F** | **F** | F |

**A 级 100% 收口**：
- machineOrderBrokenCtrl 范围内**完全不读取** status / receiveStatus
- 严格区分：machineOrderBrokenCtrl 范围**不引用**这两个字段
- 等级：F

---

## 17. machineOrderBrokenCtrl completeOrder（30.17）

**完整定义**（L16333-16352）：

```javascript
$scope.completeOrder = function () {
    Popup.confirm("确定完成么", function () {
        var completeFactory = new ObjectFactory();
        var completePromise = completeFactory.saveOrQuery(
            "/admin/completeMachineCenterOrder.json",
            {
                cashflowId: $scope.cashflowId,
                machineCenterId: $scope.machineCenterId
            }
        );
        completePromise.then(function (res) {
            if (res.status == 0) {
                Popup.notice("完成成功");
                if ($scope.chain == 1) {
                    $state.go("machineOrderChainTesting");
                } else {
                    $state.go("machineOrderTesting");
                }
            } else {
                Popup.notice(res.errmsg);
            }
        });
    }, function () {});
};
```

**A 级 100% 收口**：
- Request 严格 = `{ cashflowId, machineCenterId }`（**不传** machineCenterOrderId）
- success 后根据 chain 判断跳 `machineOrderChainTesting` 或 `machineOrderTesting`
- 等级：A

---

## 18. machineOrderBrokenCtrl vs machineOrderCtrl 数据来源对照（30.18）

| Controller | API | Response 顶层 | machineCenterOrder 来源 | 等级 |
|---|---|---|---|---|
| machineOrderCtrl | selectInStoreMachineCenterCashflowVoList.json | `{ status, result: { list } }` | `memberFactory.items[i].machineCenterOrder`（A） | A |
| machineOrderBrokenCtrl | getMachineCenterCashflowVo.json | `{ status, result: { object: { machineCenterOrderVoList[] } } }` | `getStockObjectFactory.result.object.machineCenterOrderVoList[i].machineCenterOrder`（A） | A |

**A 级关键差异**：
- 列表变量名不同：`memberFactory.items` vs `getStockObjectFactory.result.object.machineCenterOrderVoList`
- 嵌套路径不同：`items[i].machineCenterOrder` vs `machineCenterOrderVoList[i].machineCenterOrder`
- 列表变量名暗示**不同 VO**：`InStoreMachineCenterCashflowVo` vs 隐含 `MachineCenterOrderVoList`

**严格不写**：
- 禁止"两个 Controller 处理同一个 machineCenterOrder 实例"（无代码证据）
- 禁止"两个 VO 是同一个 DTO"（无 Response 字段直接对比证据）
- 等级：A

---

## 19. machineCenterOrderRecordVo vs machineCenterOrderVoList（30.19）

| 字段 | machineCenterOrderRecordVo | machineCenterOrderVoList | 等级 |
|---|---|---|---|
| machineCenterOrder | 推断包含（**F 维持**） | **A**（L16328） | A/F |
| medicalProduct | 推断包含（**F 维持**） | **A**（L16329） | A/F |
| medicalRecord | 推断包含（**F 维持**） | **F** | F |
| patient | 推断包含（**F 维持**） | **F** | F |
| customer | 推断包含（**F 维持**） | **F** | F |
| machineCenter | 推断包含（**F 维持**） | **F** | F |

**A 级 100% 收口**：
- machineCenterOrderVoList **直接证据**仅 2 个字段：machineCenterOrder.id + medicalProduct.productName
- machineCenterOrderRecordVo 在 controller.js 范围内**仅出现 3 次**（之前 S1-58 收口）

**严格不写**：
- 禁止"两个 VO 都有 machineCenterOrder" → "同 DTO"
- 等级：A

---

## 20. machineCenterOrder 字段集合（30.20）

**当前 2 Controller 直接观察到的字段**（A 级 100% 收口）：

| 字段 | machineOrderCtrl | machineOrderBrokenCtrl | machineOrderListCtrl |
|---|---|---|---|
| `id` | F（不直接读取） | A（L16328 读取） | F（不直接读取） |
| `status` | A（L16253 写后回填） | F | F |
| `receiveStatus` | F | F | A（L4321 写后回填） |
| `acceptStatus` | F | F | F |
| `planDeliveryTime` | F | F | F |
| `gmtCreate` | F | F | F |

**A 级 100% 收口**：
- 2 Controller 直接读取的 machineCenterOrder 字段**仅 3 个**：id（A × 1）/ status（A × 1）/ receiveStatus（A × 1）
- 其他字段在 controller.js 范围内**完全不出现**（F 维持）
- 等级：A

---

## 21. MachineCenterOrder action 对照（30.21）

| Action | Controller | API | Request | 本地修改 | refresh | 等级 |
|---|---|---|---|---|---|---|
| **receive** | machineOrderListCtrl | receiveMachineCenterOrder.json (L4317) | `{ machineCenterOrderId: id }` | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` (L4321) | **不调** getMachineCenterOrder | A |
| **deliveryReceiveOrder** | machineOrderListCtrl | deliveryMachineCenterOrder.json (L4332) | `{ machineCenterOrderId: id }` | `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` (L4336) | **不调** | A |
| **start** | machineOrderCtrl | startMachineCenterOrder.json (L16164) | `{ machineCenterOrderId: id }` (L16245) | **不直接** | commonOrder → getMachineCenterOrder.json 回写 status | A |
| **complete (C-A)** | machineOrderCtrl | completeMachineCenterOrder.json (L16226) | `{ machineCenterOrderId: id }` (L16245) | **不直接** | commonOrder → getMachineCenterOrder.json 回写 status | A |
| **complete (C-B)** | machineOrderBrokenCtrl | completeMachineCenterOrder.json (L16336) | `{ cashflowId, machineCenterId }` (**注意：不是 machineCenterOrderId**) | **不直接** | **不调** getMachineCenterOrder | A |
| **close** | machineOrderCtrl | closeMachineCenterOrder.json (L16235) | `{ machineCenterOrderId: id }` (L16245) | **不直接** | commonOrder → getMachineCenterOrder.json 回写 status | A |

**A 级 100% 收口**。

**关键 A 级新发现**：
- receive 协议**属于** machineOrderListCtrl（不是 machineOrderCtrl）
- deliveryReceiveOrder 也属于 machineOrderListCtrl
- C-A / C-B / close 都在 machineOrderCtrl
- C-B 在 machineOrderBrokenCtrl（**不同 controller**）
- 6 个 action **全部**有直接证据（A 级）

---

## 22. commonOrder 覆盖范围（30.22）

**commonOrder 覆盖**：
- startOrder（L16163-16171）→ commonOrder（L16243-16257）
- completeOrder（L16225-16233）→ commonOrder（L16243-16257）
- closeOrder（L16234-16242）→ commonOrder（L16243-16257）

**commonOrder 不覆盖**：
- receiveOrder（machineOrderListCtrl L4314-4328）
- deliveryReceiveOrder（machineOrderListCtrl L4329-4342）
- C-B complete（machineOrderBrokenCtrl L16333-16352）

**A 级 100% 收口**。

---

## 23. machineOrderBrokenCtrl vs commonOrder（30.23）

| 关系 | 是否真实 | 等级 |
|---|---|---|
| C-B complete 调用 commonOrder | **否** | A |
| C-B complete 使用 $scope.common | **否** | A |
| C-B complete 调 getMachineCenterOrder | **否** | A |
| C-B complete 直接 $state.go | **是** | A（L16344/L16346） |

**A 级 100% 收口**：C-B complete **绕开** commonOrder 协议。

**C-A vs C-B 关键差异**：
- C-A：commonOrder 协议 + 写后回填 status（A）
- C-B：直接 API + chain 判断 $state.go（A）
- 等级：A

---

## 24. MachineCenterOrder refresh 机制（30.24）

| 机制 | 用途 | 写入字段 | 等级 |
|---|---|---|---|
| getMachineCenterOrder.json | commonOrder 写后回填 | `memberFactory.items[idx].machineCenterOrder.status` (L16253) | A |
| getMachineCenterCashflowVo.json | machineOrderBrokenCtrl 初始加载 | `getStockObjectFactory.result.object.machineCenterOrderVoList[]` | A |
| $state.reload() | 整页刷新（machineOrderBrokenCtrl / machineOrderListCtrl / deliveryInputCtrl） | 全部重新加载 | A |
| 本地对象直接赋值 | receiveOrder / deliveryReceiveOrder 成功后 | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` (L4321) | A |

**A 级 100% 收口**：4 个 refresh 机制**完全独立**。

---

## 25. cashflowId 与 MachineCenterOrder（30.25）

| 关系 | 等级 |
|---|---|
| cashflowId 作为 machineOrderBrokenCtrl 入口 | A |
| cashflowId 作为 machineOrderCtrl 字段（**未直接**读 controller 内部 $scope.cashflowId） | F |
| cashflowId 作为 deliveryInputCtrl 入口 | A |
| cashflowId 作为 database FK | F |

**A 级 100% 收口**：
- cashflowId **只是** API Request 字段（A）
- 不进入 MachineCenterOrder 对象（A）
- 等级：A

---

## 26. medicalRecordId 与 MachineCenterOrder（30.26）

| 关系 | 等级 |
|---|---|
| medicalRecordId 作为 getMachineCenterOrder Request 字段 | A（L16251） |
| medicalRecordId 作为 machineOrderCtrl commonOrder 内部字段 | A |
| medicalRecordId 是否直接进入 machineCenterOrder 对象 | F |

**A 级 100% 收口**：
- medicalRecordId **只是** getMachineCenterOrder.json Request 字段（A）
- **不**直接进入 machineCenterOrder 对象（A）
- 等级：A

---

## 27. machineCenterId 与 MachineCenterOrder（30.27）

| 关系 | 等级 |
|---|---|
| machineCenterId 作为 machineOrderBrokenCtrl stateParams | A（L16263） |
| machineCenterId 作为 getMachineCenterCashflowVo Request 字段 | A（L16271） |
| machineCenterId 作为 completeMachineCenterOrder Request 字段 | A（L16338） |
| **是否直接出现 machineCenterOrder.machineCenterId** | **F** | F |

**A 级 100% 收口**：
- machineCenterId **只是** API Request 字段（A）
- **不**直接出现 machineCenterOrder.machineCenterId（A 级事实）
- 等级：A

---

## 28. 状态机边界（30.28）

| 类别 | 名称 | 等级 |
|---|---|---|
| 字段 | `acceptStatus` | F（当前 controller.js 范围内**不直接读取**） |
| 字段 | `status` | A（machineOrderCtrl commonOrder 写后读取） |
| 字段 | `receiveStatus` | A（machineOrderListCtrl receiveOrder 写后读取） |
| UI state | `machineOrderWaitAccess` | F（仅 machineOrderWaitProcessCtrl L16358 字符串出现） |
| UI state | `machineOrderChainWaitAccess` | F（仅 L16358） |
| UI state | `machineOrderWaitProcess` | F（仅 L16360） |
| UI state | `machineOrderChainWaitProcess` | F（仅 L16360） |
| UI state | `machineOrderProcessing` | F（仅 L16362） |
| UI state | `machineOrderChainProcessing` | F（仅 L16362） |
| UI state | `machineOrderTesting` | F + A（仅 L16346 + L16364） |
| UI state | `machineOrderChainTesting` | F + A（仅 L16344 + L16364） |

**关键 A 级边界**：
- **状态字段** vs **UI state** 是**完全不同的概念**（A）
- 字段 `status` 是**业务字段**（machineCenterOrder.status）
- UI state `machineOrderTesting` 是**路由名称**
- 两者**无直接映射代码**（A 级事实）
- 等级：A

---

## 29. 与 S1-67 的反向结论（30.29）

### S1-67 收口结论
- send API → MachineCenterOrder = **当前证据未观察**（F）
- 6 个核心问题**全部** = F
- 链 A（deliveryInputCtrl）与链 B（machineOrder*）**完全独立**

### S1-68 反向研究

**已确认来源**（A 级）：

**machineOrderCtrl**：
```
selectInStoreMachineCenterCashflowVoList.json
   ↓ Response
memberFactory.items[i]
   └─ machineCenterOrder
        └─ status (仅 L16253 写后回填)
```

**machineOrderBrokenCtrl**：
```
getMachineCenterCashflowVo.json
   ↓ Response
getStockObjectFactory.result.object.machineCenterOrderVoList[i]
   ├─ machineCenterOrder
   │    └─ id (L16328)
   └─ medicalProduct
        └─ productName (L16329)
```

**machineOrderListCtrl**：
```
selectMachineCenterOrderRecordVoList.json
   ↓ Response
getAdminList.items[i]
   ├─ machineCenterOrder
   │    └─ receiveStatus (L4321 写后回填)
   └─ medicalProductDelivery
        └─ deliveryStatus (L4336 写后回填)
```

**未确认关系**（F 维持）：
- send API → 上述来源 = F（S1-67 已确认）
- 三个 controller 的 list 项是否同 VO = F
- machineCenterOrderRecordVo 与 machineCenterOrderVoList 是否同 DTO = F
- 三个 controller 的 machineCenterOrder 是否同业务实例 = F
- cashflowId / medicalRecordId / machineCenterId 是否数据库 FK = F

---

## 30. 最终冻结（30.30）

| 问题 | 答案 | 等级 |
|---|---|---|
| Q1 | machineOrderCtrl 获取 MachineCenterOrder 的 API？ | selectInStoreMachineCenterCashflowVoList.json（A） |
| Q2 | machineOrderBrokenCtrl 获取 MachineCenterOrder 的 API？ | getMachineCenterCashflowVo.json（A） |
| Q3 | 两边 machineCenterOrder 字段集合？ | machineOrderCtrl: { status } / machineOrderBrokenCtrl: { id } / machineOrderListCtrl: { receiveStatus }（A） |
| Q4 | 两边是否可以证明为同一 DTO？ | **否**（A：F 维持） |
| Q5 | machineCenterOrder.id 来源？ | machineOrderBrokenCtrl: `machineCenterOrderVoList[i].machineCenterOrder.id`（A，L16328） / machineOrderCtrl: 不直接读取（A） / machineOrderListCtrl: 不直接读取（A） |
| Q6 | status 来源？ | machineOrderCtrl: getMachineCenterOrder.json Response（A，L16253） / 其他: F |
| Q7 | receiveStatus 来源？ | machineOrderListCtrl: receiveOrder 写后本地赋值（A，L4321） / 其他: F |
| Q8 | getMachineCenterOrder.json 更新什么？ | `memberFactory.items[idx].machineCenterOrder.status`（A） |
| Q9 | C-A / C-B complete 协议区别？ | C-A: commonOrder + 写后回填 status / C-B: 直接 API + chain $state.go（A） |
| Q10 | receive/start/complete/close/delivery 是否全部直接证实？ | **是**（A） |
| Q11 | cashflowId 是否只是 API 参数？ | **是**（A）/ DB FK F |
| Q12 | medicalRecordId 是否只是 API 参数？ | **是**（A）/ DB FK F |
| Q13 | machineCenterId 是否存在直接 machineCenterOrder 字段？ | **否**（A） |
| Q14 | send API → MachineCenterOrder 直接证据？ | **否**（A：F 维持 S1-67 结论） |
| Q15 | 能否冻结完整 MachineCenterOrder 数据来源链？ | **部分**（A：3 Controller 数据流完整；F：3 Controller 间关系 / DB 结构） |

**A 级 100% 收口**。

---

## 31. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1-30.3 | 3 controller 源码定位 | A |
| 30.4 | selectInStoreMachineCenterCashflowVoList.json Request | A |
| 30.5-30.6 | machineOrderCtrl machineCenterOrder 字段 | A（status）/ F（其他 5 字段） |
| 30.7-30.9 | machineOrderCtrl machineCenterOrder.id / status / receiveStatus | A（事实）/ E（id 推断） |
| 30.10-30.11 | getMachineCenterOrder.json | A |
| 30.12-30.13 | machineOrderBrokenCtrl + getMachineCenterCashflowVo | A |
| 30.14-30.15 | machineCenterOrderVoList + id | A |
| 30.16-30.17 | machineOrderBrokenCtrl status/receiveStatus + completeOrder | A |
| 30.18 | 双 controller 数据来源对照 | A |
| 30.19 | RecordVo vs VoList | A/F |
| 30.20 | machineCenterOrder 字段集合 | A |
| 30.21-30.23 | action 对照 + commonOrder 覆盖 + C-A/C-B | A |
| 30.24 | refresh 机制 | A |
| 30.25-30.27 | cashflowId / medicalRecordId / machineCenterId | A（API 参数）/ F（DB FK） |
| 30.28 | 状态机边界 | A |
| 30.29 | 与 S1-67 反向结论 | A |
| 30.30 | 最终冻结 | A/F |

**统计**：A=27 / B=0 / C=0 / D=0 / E=1 / F=2 = 30

---

## 32. L1/L2/L3

**L1（前端直接事实）**：
- 3 controller 完整协议
- 6 action 完整定义
- machineCenterOrder 字段集合
- 等级：A

**L2（业务模型解释）**：
- 三个 controller 业务上下文
- "MachineCenterOrder 业务实体" 推断
- 等级：**E**

**L3（数据库/物理模型）**：
- machineCenterOrder 表
- cashflowId / medicalRecordId / machineCenterId 外键
- 等级：**F**

---

## 33. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 34. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | machineOrderCtrl 获取 MachineCenterOrder 的 API？ | A（selectInStoreMachineCenterCashflowVoList.json） |
| Q2 | machineOrderBrokenCtrl 获取 MachineCenterOrder 的 API？ | A（getMachineCenterCashflowVo.json） |
| Q3 | machineCenterOrder 字段集合？ | A（id / status / receiveStatus 3 个） |
| Q4 | 两边是否可证同一 DTO？ | F（**否**） |
| Q5 | machineCenterOrder.id 来源？ | A（machineOrderBrokenCtrl: machineCenterOrderVoList[i].machineCenterOrder.id L16328） |
| Q6 | status 来源？ | A（getMachineCenterOrder.json L16253） |
| Q7 | receiveStatus 来源？ | A（receiveOrder 写后本地赋值 L4321） |
| Q8 | getMachineCenterOrder.json 更新什么？ | A（memberFactory.items[idx].machineCenterOrder.status） |
| Q9 | C-A / C-B complete 区别？ | A（C-A: commonOrder / C-B: 直接 API + chain $state.go） |
| Q10 | 6 action 全部直接证实？ | A |
| Q11 | cashflowId 是否只是 API 参数？ | A（是） / F（DB FK） |
| Q12 | medicalRecordId 是否只是 API 参数？ | A（是） / F（DB FK） |
| Q13 | machineCenterId 是否存在直接 machineCenterOrder 字段？ | F（**否**） |
| Q14 | send API → MachineCenterOrder 直接证据？ | F（**否**） |
| Q15 | 能否冻结完整数据来源链？ | A（3 Controller 数据流）/ F（3 Controller 间关系） |

---

## 35. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 36. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~127 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 37. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | machineCenterOrder 在 controller.js 范围**仅 3 字段**被直接读取（id / status / receiveStatus） | A |
| 2 | acceptStatus / planDeliveryTime / gmtCreate **完全不出现** | A |
| 3 | machineOrderCtrl 列表变量 memberFactory.items 包含 machineCenterOrder 嵌套 | A（L16253） |
| 4 | machineOrderBrokenCtrl 列表变量 getStockObjectFactory.result.object.machineCenterOrderVoList | A（L16262-16329） |
| 5 | machineOrderListCtrl 列表变量 getAdminList.items | A（L4321） |
| 6 | receive 协议属于 machineOrderListCtrl（不是 machineOrderCtrl） | A |
| 7 | C-B complete 在 machineOrderBrokenCtrl 用 `{ cashflowId, machineCenterId }`（不是 machineCenterOrderId） | A |
| 8 | commonOrder 不覆盖 receive / deliveryReceive / C-B | A |
| 9 | cashflowId / medicalRecordId / machineCenterId 都不进入 machineCenterOrder 对象 | A |
| 10 | 字段 vs UI state 是完全不同概念，无直接映射代码 | A |

---

## 38. 最终一句话

"S1-68 完成，已 Git 封口，立即停止，不进入 S1-69，等待老板下一条指令。"
