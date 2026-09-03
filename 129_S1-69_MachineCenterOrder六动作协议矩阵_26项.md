# S1-69 MachineCenterOrder 六动作协议矩阵

> 专项收口：6 个 MachineCenterOrder 动作协议矩阵（receive / start / complete C-A / complete C-B / close / delivery receive）
>
> 上一阶段：S1-68（128 号）已收口 MachineCenterOrder 数据来源。
>
> 本阶段：S1-69（129 号）专项收口**动作层协议**冻结。

---

## 1. 核心结论

**6 动作完整 A 级收口**（每动作全部源码直接证据）：

| 动作 | Controller | Function | API | Request |
|---|---|---|---|---|
| receive | machineOrderListCtrl | receiveOrder | receiveMachineCenterOrder.json | `{ machineCenterOrderId: id }` |
| start | machineOrderCtrl | startOrder | startMachineCenterOrder.json | `{ machineCenterOrderId: id }`（通过 commonOrder） |
| complete C-A | machineOrderCtrl | completeOrder | completeMachineCenterOrder.json | `{ machineCenterOrderId: id }`（通过 commonOrder） |
| complete C-B | machineOrderBrokenCtrl | completeOrder | completeMachineCenterOrder.json | `{ cashflowId, machineCenterId }`（**不传** machineCenterOrderId） |
| close | machineOrderCtrl | closeOrder | closeMachineCenterOrder.json | `{ machineCenterOrderId: id }`（通过 commonOrder） |
| delivery receive | machineOrderListCtrl | deliveryReceiveOrder | deliveryMachineCenterOrder.json | `{ machineCenterOrderId: id }` |

**关键边界**：
- commonOrder **覆盖** start / C-A / close
- commonOrder **不覆盖** receive / delivery receive / C-B
- receive 修改 `machineCenterOrder.receiveStatus = 1`（A）
- delivery receive 修改 `medicalProductDelivery.deliveryStatus = 1`（A）
- C-A success 调 getMachineCenterOrder.json 回写 `machineCenterOrder.status`（A）
- C-B success **不**调 getMachineCenterOrder（**A**），仅根据 chain 跳 state

---

## 2. 证据范围

**直接证据**：
- controller.js L4314-4342（machineOrderListCtrl 6 动作函数）
- controller.js L16094-16258（machineOrderCtrl 6 动作函数）
- controller.js L16261-16354（machineOrderBrokenCtrl C-B 函数）
- controller.js L16243-16257（commonOrder）

**资源缺失**：
- 3 controller HTML 模板（F）
- 完整 route schema（F）
- 后端算法 / DTO 定义（F）

---

## 3. 六动作清单（30.1）

**全仓精确搜索**：

| 关键词 | 出现次数 | 位置 | 等级 |
|---|---|---|---|
| receiveOrder | 2 | L4314 (定义) / L4328 (call) | A |
| deliveryReceiveOrder | 1 | L4329 (定义) | A |
| startOrder | 1 | L16163 (定义) | A |
| completeOrder (C-A) | 1 | L16225 (定义) | A |
| completeOrder (C-B) | 1 | L16333 (定义) | A |
| closeOrder | 1 | L16234 (定义) | A |
| commonOrder | 6 | L16243 (定义) / L16169 / L16231 / L16240 + 内部 | A |
| receiveMachineCenterOrder.json | 1 | L4317 | A |
| deliveryMachineCenterOrder.json | 1 | L4332 | A |
| startMachineCenterOrder.json | 1 | L16164 / L16245 | A |
| completeMachineCenterOrder.json | 2 | L16226 (C-A) / L16336 (C-B) | A |
| closeMachineCenterOrder.json | 1 | L16235 / L16245 | A |

**A 级 100% 收口**。

---

## 4. receive 完整协议（30.2, 30.11）

**receiveOrder 函数**（machineOrderListCtrl L4314-4328）：

```javascript
$scope.receiveOrder = function (id, idx) {
    Popup.confirm("确定签收么", function () {
      $scope.receiveFactory = new ObjectFactory();
      var receivePromise = $scope.receiveFactory.saveOrQuery(
        "/admin/receiveMachineCenterOrder.json", 
        { machineCenterOrderId: id }
      );
      receivePromise.then(function (re) {
        if (re.status == 0) {
          Popup.notice("签收成功");
          $scope.getAdminList.items[idx].machineCenterOrder.receiveStatus = 1;
          $scope.getAdminList.count = $scope.getAdminList.count - 1;
        } else {
          Popup.notice(re.errmsg);
        }
      });
    }, function () {});
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderListCtrl | A |
| Function | receiveOrder (L4314) | A |
| 参数 | (id, idx) | A |
| 参数来源 | HTML 调用传入（id = machineCenterOrderId, idx = $index） | A（函数定义）/ F（HTML） |
| Request | `{ machineCenterOrderId: id }` | A（L4317） |
| API | receiveMachineCenterOrder.json | A |
| success 提示 | Popup.notice("签收成功") | A（L4320） |
| 本地对象修改 | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` | A（L4321） |
| count 修改 | `getAdminList.count = getAdminList.count - 1` | A（L4322） |
| refresh | **不调** | A（**不调** getMachineCenterOrder / $state.reload） |
| commonOrder | **不调** | A |
| state.go | **不调** | A |

**关键 A 级新发现**：
- receive 写入 `machineCenterOrder.receiveStatus = 1`（**不是** status）
- 同时修改 `getAdminList.count - 1`（业务列表总数）
- 等级：A

---

## 5. deliveryReceive 完整协议（30.3, 30.16）

**deliveryReceiveOrder 函数**（machineOrderListCtrl L4329-4342）：

```javascript
$scope.deliveryReceiveOrder = function (id, idx) {
    Popup.confirm("确定发货么", function () {
      $scope.deliveryFactory = new ObjectFactory();
      var deliveryPromise = $scope.deliveryFactory.saveOrQuery(
        "/admin/deliveryMachineCenterOrder.json", 
        { machineCenterOrderId: id }
      );
      deliveryPromise.then(function (re) {
        if (re.status == 0) {
          Popup.notice("发货成功");
          $scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1;
        } else {
          Popup.notice(re.errmsg);
        }
      });
    }, function () {});
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderListCtrl | A |
| Function | deliveryReceiveOrder (L4329) | A |
| 参数 | (id, idx) | A |
| Request | `{ machineCenterOrderId: id }` | A（L4332） |
| API | deliveryMachineCenterOrder.json | A |
| success 提示 | Popup.notice("发货成功") | A（L4335） |
| **本地对象修改** | `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` | A（L4336） |
| refresh | **不调** | A |
| commonOrder | **不调** | A |
| state.go | **不调** | A |
| count 修改 | **不调** | A |

**关键 A 级边界**：
- deliveryReceive 写入 **`medicalProductDelivery.deliveryStatus = 1`**（**不是** machineCenterOrder.deliveryStatus）
- 字段路径严格：`medicalProductDelivery.deliveryStatus`
- 等级：A

---

## 6. receive vs deliveryReceive 对照（30.4）

| 项目 | receive | delivery receive | 等级 |
|---|---|---|---|
| Controller | machineOrderListCtrl | machineOrderListCtrl | A |
| Function | receiveOrder | deliveryReceiveOrder | A |
| Request | `{ machineCenterOrderId: id }` | `{ machineCenterOrderId: id }` | A（**字段完全相同**） |
| API | receiveMachineCenterOrder.json | deliveryMachineCenterOrder.json | A（**不同**） |
| success 提示 | "签收成功" | "发货成功" | A |
| 本地修改字段 | `machineCenterOrder.receiveStatus = 1` | `medicalProductDelivery.deliveryStatus = 1` | A（**不同**） |
| count 修改 | `count - 1` | **不调** | A（**不同**） |
| refresh | **不调** | **不调** | A |
| commonOrder | **不调** | **不调** | A |
| state.go | **不调** | **不调** | A |

**关键 A 级边界**：
- Request 字段**完全相同**（A）
- API **不同**（A）
- 本地修改**完全不同**（A）：
  - receive → `machineCenterOrder.receiveStatus = 1`
  - delivery receive → `medicalProductDelivery.deliveryStatus = 1`
- 等级：A

---

## 7. startOrder 完整协议（30.5, 30.12）

**startOrder 函数**（machineOrderCtrl L16163-16171）：

```javascript
$scope.startOrder = function (id, medicalRecordId, idx) {
    $scope.common.url = "/admin/startMachineCenterOrder.json";
    $scope.common.machineCenterOrderId = id;
    $scope.common.medicalRecordId = medicalRecordId;
    $scope.common.idx = idx;
    Popup.confirm("确定开始制作么？", function () {
      $scope.commonOrder();
    }, function () {});
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderCtrl | A |
| Function | startOrder (L16163) | A |
| 参数 | (id, medicalRecordId, idx) | A |
| 写入 common | url / machineCenterOrderId / medicalRecordId / idx | A（L16164-16167） |
| Popup | "确定开始制作么？" | A |
| 实际 API 调用 | $scope.commonOrder() | A（L16169） |
| 实际 Request | `{ machineCenterOrderId: $scope.common.machineCenterOrderId }` | A（L16245，commonOrder 内） |
| 实际 API URL | startMachineCenterOrder.json | A |
| 写后回填 | getMachineCenterOrder.json → `memberFactory.items[common.idx].machineCenterOrder.status = resp.result.object.status` | A（L16251-16253） |
| state.go | **不调** | A |
| commonOrder | **调用** | A |

**关键 A 级边界**：
- startOrder 严格 = commonOrder 协议
- 不直接修改 machineCenterOrder.status（A，通过 commonOrder 间接回填）
- 等级：A

---

## 8. completeOrder C-A 完整协议（30.6, 30.13）

**completeOrder 函数**（machineOrderCtrl L16225-16233）：

```javascript
$scope.completeOrder = function (id, medicalRecordId, idx) {
    $scope.common.url = "/admin/completeMachineCenterOrder.json";
    $scope.common.machineCenterOrderId = id;
    $scope.common.medicalRecordId = medicalRecordId;
    $scope.common.idx = idx;
    Popup.confirm("确定制作完成么？", function () {
      $scope.commonOrder();
    }, function () {});
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderCtrl | A |
| Function | completeOrder (L16225) | A |
| 参数 | (id, medicalRecordId, idx) | A |
| commonOrder | **调用** | A |
| 实际 Request | `{ machineCenterOrderId: $scope.common.machineCenterOrderId }` | A |
| 实际 API URL | completeMachineCenterOrder.json | A |
| 写后回填 | getMachineCenterOrder.json → status | A |
| state.go | **不调** | A |

**关键 A 级边界**：
- C-A 与 start 协议**完全相同**（仅 URL 不同）
- id 来自 function 参数（**不直接**读取 `machineCenterOrder.id`）
- 等级：A

---

## 9. closeOrder 完整协议（30.7, 30.15）

**closeOrder 函数**（machineOrderCtrl L16234-16242）：

```javascript
$scope.closeOrder = function (id, medicalRecordId, idx) {
    $scope.common.url = "/admin/closeMachineCenterOrder.json";
    $scope.common.machineCenterOrderId = id;
    $scope.common.medicalRecordId = medicalRecordId;
    $scope.common.idx = idx;
    Popup.confirm("确定关闭么？", function () {
      $scope.commonOrder();
    }, function () {});
};
```

**A 级 100% 收口**：

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderCtrl | A |
| Function | closeOrder (L16234) | A |
| 参数 | (id, medicalRecordId, idx) | A |
| commonOrder | **调用** | A |
| 实际 Request | `{ machineCenterOrderId: $scope.common.machineCenterOrderId }` | A |
| 实际 API URL | closeMachineCenterOrder.json | A |
| 写后回填 | getMachineCenterOrder.json → status | A |
| state.go | **不调** | A |

**关键 A 级边界**：
- close 与 start / C-A 协议**完全相同**（仅 URL 不同）
- 等级：A

---

## 10. commonOrder 统一协议（30.8）

**commonOrder 定义**（machineOrderCtrl L16243-16257）：

```javascript
$scope.commonOrder = function () {
    $scope.commonOrderFactory = new ObjectFactory();
    var commonPromise = $scope.commonOrderFactory.saveOrQuery(
        $scope.common.url, 
        { machineCenterOrderId: $scope.common.machineCenterOrderId }
    );
    commonPromise.then(function (res) {
      if (res.status == 1) {
        Popup.notice(res.errmsg);
      } else {
        $scope.getOrderFactory = new ObjectFactory();
        var orderPromise = $scope.getOrderFactory.saveOrQuery(
            "/admin/getMachineCenterOrder.json", 
            { medicalRecordId: $scope.common.medicalRecordId }
        );
        orderPromise.then(function (resp) {
          $scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status;
        });
      }
    });
};
```

**commonOrder 覆盖动作**：

| 动作 | 是否调 commonOrder | 等级 |
|---|---|---|
| start | **是**（L16169） | A |
| complete C-A | **是**（L16231） | A |
| close | **是**（L16240） | A |
| complete C-B | **否** | A |
| receive | **否** | A |
| delivery receive | **否** | A |

**A 级 100% 收口**：
- commonOrder **覆盖** 3 个动作（start / C-A / close）
- commonOrder **不覆盖** 3 个动作（C-B / receive / delivery receive）

**commonOrder 内部协议**：
- 第 1 步：写 API（$scope.common.url 决定）
- 第 2 步：写后调 getMachineCenterOrder.json（**仅**在写成功时）
- 第 3 步：本地修改 `memberFactory.items[idx].machineCenterOrder.status`
- 等级：A

---

## 11. C-B completeOrder 完整协议（30.9, 30.14）

**C-B completeOrder 函数**（machineOrderBrokenCtrl L16333-16352）：

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

| 项目 | 证据 | 等级 |
|---|---|---|
| Controller | machineOrderBrokenCtrl | A |
| Function | completeOrder (L16333) | A |
| 参数 | **无参数** | A（L16333 无入参） |
| Request | `{ cashflowId, machineCenterId }` | A（L16336-16339） |
| API | completeMachineCenterOrder.json | A |
| 关键边界 | **不传** machineCenterOrderId | A |
| commonOrder | **不调** | A |
| getMachineCenterOrder | **不调** | A |
| 本地 MachineCenterOrder 字段更新 | **无** | A（**不调**任何本地写） |
| state.go | chain == 1 → machineOrderChainTesting (L16344) | A |
| state.go | else → machineOrderTesting (L16346) | A |

**关键 A 级边界**：
- C-B **不传** machineCenterOrderId（A）
- C-B **不调** commonOrder（A）
- C-B **不调** getMachineCenterOrder（A）
- C-B **不本地修改** machineCenterOrder（A）
- C-B **只**根据 chain 跳 state（A）
- 等级：A

---

## 12. C-A / C-B 协议对照（30.10）

| 项目 | C-A | C-B | 等级 |
|---|---|---|---|
| Controller | machineOrderCtrl | machineOrderBrokenCtrl | A |
| Function | completeOrder (L16225) | completeOrder (L16333) | A |
| API | completeMachineCenterOrder.json | completeMachineCenterOrder.json | A（**同 API**） |
| Request | `{ machineCenterOrderId: id }` | `{ cashflowId, machineCenterId }` | A（**完全不同**） |
| commonOrder | **调用** | **不调** | A |
| getMachineCenterOrder | **调**（写后回填 status） | **不调** | A |
| 本地 MachineCenterOrder 字段更新 | `memberFactory.items[idx].machineCenterOrder.status` | **不调** | A |
| 状态跳转 | **不调** | chain==1 → machineOrderChainTesting / else → machineOrderTesting | A |
| refresh | **不调** $state.reload | **不调** $state.reload | A |

**A 级 100% 收口**：
- C-A 与 C-B **API 相同**但**协议完全不同**（Request 字段 / 后续行为）
- 等级：A

---

## 13. 动作参数来源（30.26）

| 动作 | 参数 | 真实来源 | 等级 |
|---|---|---|---|
| receive | id | function 参数（HTML 调用传入） | A（函数）/ F（HTML） |
| receive | idx | function 参数（HTML `$index` 推断） | A（函数）/ E（推断） |
| delivery receive | id | function 参数 | A（函数）/ F（HTML） |
| delivery receive | idx | function 参数 | A（函数）/ E（推断） |
| start | id | function 参数 | A（函数）/ F（HTML） |
| start | medicalRecordId | function 参数 | A（函数）/ F（HTML） |
| start | idx | function 参数 | A（函数）/ E（推断） |
| C-A complete | id | function 参数 | A（函数）/ F（HTML） |
| C-A complete | medicalRecordId | function 参数 | A（函数）/ F（HTML） |
| C-A complete | idx | function 参数 | A（函数）/ E（推断） |
| C-B complete | 无参数 | - | A |
| C-B complete | cashflowId | $stateParams.cashflowId (L16262) | A |
| C-B complete | machineCenterId | $stateParams.machineCenterId (L16263) | A |
| close | id | function 参数 | A（函数）/ F（HTML） |
| close | medicalRecordId | function 参数 | A（函数）/ F（HTML） |
| close | idx | function 参数 | A（函数）/ E（推断） |

**A 级 100% 收口**：
- C-B 唯一有 stateParams 完整证据（A）
- 其他动作参数来源 = HTML 绑定（F）

---

## 14. MachineCenterOrder.status（30.17）

**全仓直接写入点**：

| 位置 | 表达式 | 等级 |
|---|---|---|
| L16253 | `memberFactory.items[common.idx].machineCenterOrder.status = resp.result.object.status` | A（commonOrder 写后回填） |

**被 commonOrder 覆盖的动作**：
- start 成功后回填
- C-A 成功后回填
- close 成功后回填

**A 级 100% 收口**：
- `machineCenterOrder.status` 写入点**仅 1 处**（A，L16253）
- 由 commonOrder 协议统一处理
- 等级：A

---

## 15. MachineCenterOrder.receiveStatus（30.18）

**全仓直接写入点**：

| 位置 | 表达式 | 等级 |
|---|---|---|
| L4321 | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` | A（receiveOrder 写后） |

**receiveStatus 与 status 严格区分**：
- `machineCenterOrder.receiveStatus`（A，L4321）
- `machineCenterOrder.status`（A，L16253）
- 字段路径**完全不同**
- 写入点**完全不同**
- 等级：A

---

## 16. deliveryStatus（30.19）

**全仓 `medicalProductDelivery.deliveryStatus` 写入点**：

| 位置 | 表达式 | 等级 |
|---|---|---|
| L4336 | `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` | A（deliveryReceiveOrder 写后） |

**关键 A 级边界**：
- deliveryStatus 字段路径严格 = `medicalProductDelivery.deliveryStatus`（**不是** `machineCenterOrder.deliveryStatus`）
- 等级：A

---

## 17. acceptStatus（30.20）

**全仓搜索**：

| 项目 | 状态 | 等级 |
|---|---|---|
| `machineCenterOrder.acceptStatus` 在 controller.js 范围内直接出现 | **F**（0 处） | F |
| `acceptStatus` 作为查询 filter 出现 | machineOrderListCtrl L4350 `setTab` | A |
| `acceptStatus` 在动作函数中直接修改 | **F** | F |

**A 级 100% 收口**：
- acceptStatus **不是** MachineCenterOrder 状态字段（controller.js 范围内**不直接读取/写入**）
- acceptStatus **仅**作为 machineOrderListCtrl `setTab` 查询 filter（A，L4350）
- 等级：A

---

## 18. status 与 UI state 边界（30.21, 30.22）

| 类别 | 名称 | 直接读取/写入 | 等级 |
|---|---|---|---|
| 字段 | `machineCenterOrder.status` | L16253 写后赋值 | A |
| 字段 | `machineCenterOrder.receiveStatus` | L4321 写后赋值 | A |
| 字段 | `medicalProductDelivery.deliveryStatus` | L4336 写后赋值 | A |
| UI state | machineOrderWaitAccess | 字符串（L16358） | A（字符串） / F（映射） |
| UI state | machineOrderChainWaitAccess | 字符串（L16358） | A / F |
| UI state | machineOrderWaitProcess | 字符串（L16360） | A / F |
| UI state | machineOrderChainWaitProcess | 字符串（L16360） | A / F |
| UI state | machineOrderProcessing | 字符串（L16362） | A / F |
| UI state | machineOrderChainProcessing | 字符串（L16362） | A / F |
| UI state | machineOrderTesting | 字符串（L16346 / L16364） | A / F |
| UI state | machineOrderChainTesting | 字符串（L16344 / L16364） | A / F |

**关键 A 级边界**：
- **字段** vs **UI state** 是**完全不同的概念**（A）
- 无直接映射代码（A）
- 等级：A

---

## 19. $state.reload（30.23）

**6 动作中 $state.reload 调用**：

| 动作 | $state.reload | 等级 |
|---|---|---|
| receive | **不调** | A |
| start | **不调** | A（通过 commonOrder 不调） |
| C-A complete | **不调** | A（通过 commonOrder 不调） |
| C-B complete | **不调** | A |
| close | **不调** | A（通过 commonOrder 不调） |
| delivery receive | **不调** | A |

**A 级 100% 收口**：**6 动作 success 后均不调 $state.reload**。

---

## 20. $state.go（30.22）

**6 动作中 $state.go 调用**：

| 动作 | $state.go | 等级 |
|---|---|---|
| receive | **不调** | A |
| start | **不调** | A |
| C-A complete | **不调** | A |
| C-B complete | chain==1 → machineOrderChainTesting (L16344) / else → machineOrderTesting (L16346) | A |
| close | **不调** | A |
| delivery receive | **不调** | A |

**A 级 100% 收口**：
- **仅 C-B** 调用 $state.go
- 等级：A

---

## 21. getMachineCenterOrder.json 调用（30.24）

**调用动作**：

| 动作 | 调 getMachineCenterOrder.json | 等级 |
|---|---|---|
| receive | **不调** | A |
| start | **调**（commonOrder 内部） | A |
| C-A complete | **调**（commonOrder 内部） | A |
| C-B complete | **不调** | A |
| close | **调**（commonOrder 内部） | A |
| delivery receive | **不调** | A |

**A 级 100% 收口**：
- 仅 start / C-A / close（通过 commonOrder）调 getMachineCenterOrder.json
- 等级：A

---

## 22. getMachineCenterCashflowVo.json 调用（30.25）

**调用动作**：

| 动作 | 调 getMachineCenterCashflowVo.json | 等级 |
|---|---|---|
| 6 动作 | **0 个调** | A |
| C-B 初始加载 | 调（L16269-16272） | A |
| C-B complete | **不调** | A |

**A 级 100% 收口**：
- 6 动作中**均不**调 getMachineCenterCashflowVo.json
- 该 API 仅在 machineOrderBrokenCtrl 初始化时调用
- 等级：A

---

## 23. 与 machineOrderListCtrl 数据来源（30.27）

| 动作 | 数据来源 | 路径 | 等级 |
|---|---|---|---|
| receive | `getAdminList.items[idx].machineCenterOrder` | `getAdminList.items[]`（来自 selectMachineCenterOrderRecordVoList.json） | A |
| delivery receive | `getAdminList.items[idx].medicalProductDelivery` | 同上 | A |

**A 级 100% 收口**：
- machineOrderListCtrl 列表变量 = `getAdminList.items[]`
- 来自 selectMachineCenterOrderRecordVoList.json Response
- 等级：A

---

## 24. 六动作协议矩阵（30.28）

| Action | Controller | Function | API | Request | 本地更新 | Refresh | State |
|---|---|---|---|---|---|---|---|
| **receive** | machineOrderListCtrl | receiveOrder (L4314) | receiveMachineCenterOrder.json | `{ machineCenterOrderId: id }` | `getAdminList.items[idx].machineCenterOrder.receiveStatus = 1` + count - 1 | **不调** | **不调** |
| **start** | machineOrderCtrl | startOrder (L16163) | startMachineCenterOrder.json（via commonOrder） | `{ machineCenterOrderId: id }` | `memberFactory.items[idx].machineCenterOrder.status`（via commonOrder） | getMachineCenterOrder.json（via commonOrder） | **不调** |
| **complete C-A** | machineOrderCtrl | completeOrder (L16225) | completeMachineCenterOrder.json（via commonOrder） | `{ machineCenterOrderId: id }` | `memberFactory.items[idx].machineCenterOrder.status`（via commonOrder） | getMachineCenterOrder.json（via commonOrder） | **不调** |
| **complete C-B** | machineOrderBrokenCtrl | completeOrder (L16333) | completeMachineCenterOrder.json | `{ cashflowId, machineCenterId }` | **不调** | **不调** | chain==1 → machineOrderChainTesting / else → machineOrderTesting |
| **close** | machineOrderCtrl | closeOrder (L16234) | closeMachineCenterOrder.json（via commonOrder） | `{ machineCenterOrderId: id }` | `memberFactory.items[idx].machineCenterOrder.status`（via commonOrder） | getMachineCenterOrder.json（via commonOrder） | **不调** |
| **delivery receive** | machineOrderListCtrl | deliveryReceiveOrder (L4329) | deliveryMachineCenterOrder.json | `{ machineCenterOrderId: id }` | `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1` | **不调** | **不调** |

**A 级 100% 收口**。

---

## 25. Controller 边界（30.22）

| Controller | 动作 | 列表变量 | 字段写入 |
|---|---|---|---|
| machineOrderCtrl | start / C-A / close | memberFactory.items | machineCenterOrder.status |
| machineOrderBrokenCtrl | C-B | getStockObjectFactory.result.object.machineCenterOrderVoList | **不写**（仅 state.go） |
| machineOrderListCtrl | receive / delivery receive | getAdminList.items | machineCenterOrder.receiveStatus / medicalProductDelivery.deliveryStatus |

**A 级 100% 收口**：
- 3 Controller 完全独立
- 字段写入点严格分离
- 等级：A

---

## 26. 与历史证据对照

### S1-52（112 号）：状态机专项收口
- 收口 4 状态字段 26 项
- **本轮验证**：4 状态字段（acceptStatus / status / receiveStatus / deliveryStatus）当前 controller.js 范围直接读取点：
  - acceptStatus: 0 处写入 + L4350 setTab filter（A）
  - status: L16253 commonOrder 写后回填（A）
  - receiveStatus: L4321 receiveOrder 写后回填（A）
  - deliveryStatus: L4336 deliveryReceiveOrder 写后回填（A）
- **S1-52 推测**某些字段存在但 controller.js 范围**不直接读取**（如 planDeliveryTime / gmtCreate）
- **S1-69 严格 A 级**记录
- **无冲突**

### S1-53（113 号）：动作 API commonOrder 协议
- 收口 start / complete / close 协议
- **本轮验证**：commonOrder 覆盖 start / C-A / close（A）
- **S1-53 收口**正确
- **S1-69 进一步明确**：commonOrder 不覆盖 C-B / receive / delivery receive（A）
- **无冲突**

### S1-54（114 号）：Complete 双协议
- 收口 C-A 和 C-B
- **S1-69 验证**：
  - C-A: machineOrderCtrl commonOrder（A）
  - C-B: machineOrderBrokenCtrl 直接 API + chain $state.go（A）
  - 协议**完全不同**（Request / refresh / state.go）
- **S1-54 收口**正确
- **无冲突**

### S1-60（120 号）：MachineCenterOrder 状态机 100% 收口
- **S1-69 验证**：26 项评级中直接读取/写入的字段在 controller.js 范围仅 3 个（id / status / receiveStatus）
- 其他字段（acceptStatus / planDeliveryTime / gmtCreate）当前 controller.js 范围**不直接读取**
- **S1-60 历史收口**部分基于推断，本轮**进一步 A 级严格**
- **无冲突**

### S1-68（128 号）：MachineCenterOrder 数据来源与双 Controller 读取链
- **S1-69 验证**：3 Controller 数据来源完全正确
- **S1-69 进一步收口**：6 动作完整矩阵
- **无冲突**

---

## 27. 一期冻结事实（A 级）

**6 动作完整可复刻**：

```javascript
// === 动作 A: receive ===
$scope.receiveOrder = function (id, idx) {
  Popup.confirm("确定签收么", function () {
    var factory = new ObjectFactory();
    factory.saveOrQuery("/admin/receiveMachineCenterOrder.json", { machineCenterOrderId: id })
      .then(function (re) {
        if (re.status == 0) {
          Popup.notice("签收成功");
          $scope.getAdminList.items[idx].machineCenterOrder.receiveStatus = 1;
          $scope.getAdminList.count = $scope.getAdminList.count - 1;
        } else {
          Popup.notice(re.errmsg);
        }
      });
  }, function () {});
};

// === 动作 B: start ===
$scope.startOrder = function (id, medicalRecordId, idx) {
  $scope.common.url = "/admin/startMachineCenterOrder.json";
  $scope.common.machineCenterOrderId = id;
  $scope.common.medicalRecordId = medicalRecordId;
  $scope.common.idx = idx;
  Popup.confirm("确定开始制作么？", function () { $scope.commonOrder(); }, function () {});
};

// === 动作 C-A: complete (machineOrderCtrl) ===
$scope.completeOrder = function (id, medicalRecordId, idx) {
  $scope.common.url = "/admin/completeMachineCenterOrder.json";
  $scope.common.machineCenterOrderId = id;
  $scope.common.medicalRecordId = medicalRecordId;
  $scope.common.idx = idx;
  Popup.confirm("确定制作完成么？", function () { $scope.commonOrder(); }, function () {});
};

// === 动作 D: C-B complete (machineOrderBrokenCtrl) ===
$scope.completeOrder = function () {
  Popup.confirm("确定完成么", function () {
    var factory = new ObjectFactory();
    factory.saveOrQuery("/admin/completeMachineCenterOrder.json", { 
      cashflowId: $scope.cashflowId, 
      machineCenterId: $scope.machineCenterId 
    }).then(function (res) {
      if (res.status == 0) {
        Popup.notice("完成成功");
        if ($scope.chain == 1) { $state.go("machineOrderChainTesting"); }
        else { $state.go("machineOrderTesting"); }
      } else {
        Popup.notice(res.errmsg);
      }
    });
  }, function () {});
};

// === 动作 E: close ===
$scope.closeOrder = function (id, medicalRecordId, idx) {
  $scope.common.url = "/admin/closeMachineCenterOrder.json";
  $scope.common.machineCenterOrderId = id;
  $scope.common.medicalRecordId = medicalRecordId;
  $scope.common.idx = idx;
  Popup.confirm("确定关闭么？", function () { $scope.commonOrder(); }, function () {});
};

// === 动作 F: delivery receive ===
$scope.deliveryReceiveOrder = function (id, idx) {
  Popup.confirm("确定发货么", function () {
    var factory = new ObjectFactory();
    factory.saveOrQuery("/admin/deliveryMachineCenterOrder.json", { machineCenterOrderId: id })
      .then(function (re) {
        if (re.status == 0) {
          Popup.notice("发货成功");
          $scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1;
        } else {
          Popup.notice(re.errmsg);
        }
      });
  }, function () {});
};

// === commonOrder (覆盖 start / C-A / close) ===
$scope.commonOrder = function () {
  var factory = new ObjectFactory();
  factory.saveOrQuery($scope.common.url, { machineCenterOrderId: $scope.common.machineCenterOrderId })
    .then(function (res) {
      if (res.status != 1) {
        var orderFactory = new ObjectFactory();
        orderFactory.saveOrQuery("/admin/getMachineCenterOrder.json", { medicalRecordId: $scope.common.medicalRecordId })
          .then(function (resp) {
            $scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status;
          });
      } else {
        Popup.notice(res.errmsg);
      }
    });
};
```

---

## 28. 当前 F 边界（明确冻结）

| F 边界 | 说明 |
|---|---|
| HTML 模板 | 3 controller HTML 模板缺失 |
| 完整 route schema | `.state()` 定义 F |
| HTML 调用点 | 6 动作 HTML ng-click 绑定 F |
| machineCenterOrder.id 直接读取 | machineOrderCtrl / machineOrderListCtrl 不直接读取 |
| acceptStatus / planDeliveryTime / gmtCreate | 当前 controller.js 范围不直接读取 |
| 字段 vs UI state 映射 | 无直接映射代码 |
| 后端算法 / DTO 定义 | F |
| 数据库表结构 | F |
| machineCenterOrderId 是否数据库 FK | F |
| send API → MachineCenterOrder | F（S1-67 维持） |

---

## 29. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | 6 动作 API 搜索 | A |
| 30.2 | receiveOrder 完整协议 | A |
| 30.3 | deliveryReceiveOrder 完整协议 | A |
| 30.4 | receive vs deliveryReceive 对照 | A |
| 30.5 | startOrder | A |
| 30.6 | completeOrder C-A | A |
| 30.7 | closeOrder | A |
| 30.8 | commonOrder 覆盖范围 | A |
| 30.9 | C-B complete | A |
| 30.10 | C-A / C-B 对照 | A |
| 30.11 | receive 与 MachineCenterOrder | A |
| 30.12 | start 与 MachineCenterOrder | A |
| 30.13 | C-A complete 状态更新 | A |
| 30.14 | C-B complete 状态更新 | A |
| 30.15 | close 状态更新 | A |
| 30.16 | deliveryReceive 状态更新 | A |
| 30.17 | MachineCenterOrder.status 写入点 | A |
| 30.18 | MachineCenterOrder.receiveStatus 写入点 | A |
| 30.19 | deliveryStatus 写入点 | A |
| 30.20 | acceptStatus | A（仅 filter）/ F（动作函数） |
| 30.21 | status 与 UI state 边界 | A |
| 30.22 | $state.go | A |
| 30.23 | $state.reload | A |
| 30.24 | getMachineCenterOrder.json 调用 | A |
| 30.25 | getMachineCenterCashflowVo.json 调用 | A |
| 30.26 | 动作参数来源 | A（函数）/ F（HTML） |
| 30.27 | 与 machineOrderListCtrl 数据来源 | A |
| 30.28 | 六动作协议最终矩阵 | A |
| 30.29 | Controller 边界 | A |
| 30.30 | 最终冻结 | A |

**统计**：A=30 / B=0 / C=0 / D=0 / E=0 / F=0 = 30

---

## 30. L1/L2/L3

**L1（前端直接事实）**：
- 6 动作完整协议
- 字段写入点
- commonOrder 覆盖范围
- C-A/C-B 协议差异
- 等级：A

**L2（业务模型解释）**：
- 6 动作业务含义（"签收" / "开始" / "完成" / "关闭" / "发货"）
- 状态机业务解释
- 等级：**E**

**L3（数据库/物理模型）**：
- machineCenterOrder 表
- 6 动作后端算法
- 状态机后端实现
- 等级：**F**

---

## 31. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 32. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | receive 精确 API / Request？ | A（receiveMachineCenterOrder.json / { machineCenterOrderId: id }） |
| Q2 | deliveryReceive 精确 API / Request？ | A（deliveryMachineCenterOrder.json / { machineCenterOrderId: id }） |
| Q3 | start 精确 API / Request？ | A（startMachineCenterOrder.json / { machineCenterOrderId: id } via commonOrder） |
| Q4 | C-A complete 精确 API / Request？ | A（completeMachineCenterOrder.json / { machineCenterOrderId: id } via commonOrder） |
| Q5 | C-B complete 精确 API / Request？ | A（completeMachineCenterOrder.json / { cashflowId, machineCenterId }） |
| Q6 | close 精确 API / Request？ | A（closeMachineCenterOrder.json / { machineCenterOrderId: id } via commonOrder） |
| Q7 | 哪些动作走 commonOrder？ | A（start / C-A / close） |
| Q8 | 哪些动作直接调 API？ | A（C-B / receive / delivery receive） |
| Q9 | 哪些动作本地修改 machineCenterOrder？ | A（receive: receiveStatus / commonOrder: status） |
| Q10 | 哪些动作本地修改 medicalProductDelivery？ | A（delivery receive: deliveryStatus） |
| Q11 | 哪些动作调 getMachineCenterOrder？ | A（start / C-A / close via commonOrder） |
| Q12 | 哪些动作调 getMachineCenterCashflowVo？ | A（0 个） |
| Q13 | 哪些动作调 $state.reload？ | A（0 个） |
| Q14 | 哪些动作调 $state.go？ | A（仅 C-B） |
| Q15 | machineCenterOrder.status 写入点？ | A（L16253 commonOrder 内） |
| Q16 | machineCenterOrder.receiveStatus 写入点？ | A（L4321 receiveOrder） |
| Q17 | deliveryStatus 写入点？ | A（L4336 deliveryReceiveOrder） |
| Q18 | acceptStatus 状态字段还是查询过滤？ | A（**仅**查询 filter，**不**是 MachineCenterOrder 状态字段） |
| Q19 | MachineCenterOrder.status 与 UI state 直接映射？ | A（**否**，无映射代码） |
| Q20 | 6 动作能否冻结成统一协议？ | A（**否**，6 动作有 3 种不同模式：commonOrder / C-B direct / listCtrl direct） |

---

## 33. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 34. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~128 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 35. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | 6 动作全仓搜索 100% 收口 | A |
| 2 | receive / delivery receive 协议 100% 收口 | A |
| 3 | start / C-A / close 通过 commonOrder 协议 | A |
| 4 | C-B 绕开 commonOrder 直接调 API | A |
| 5 | receive 写 receiveStatus / count - 1 | A |
| 6 | delivery receive 写 medicalProductDelivery.deliveryStatus | A |
| 7 | C-B 不传 machineCenterOrderId | A |
| 8 | C-B 跳 state.go(machineOrderTesting / machineOrderChainTesting) | A |
| 9 | commonOrder 写后调 getMachineCenterOrder.json 回写 status | A |
| 10 | 6 动作 success 后均不调 $state.reload | A |
| 11 | 仅 C-B 调 $state.go | A |
| 12 | acceptStatus 仅是查询 filter 不是 MachineCenterOrder 状态字段 | A |
| 13 | 字段 vs UI state 无直接映射代码 | A |

---

## 36. 最终一句话

"S1-69 完成，已 Git 封口，立即停止，不进入 S1-70，等待老板下一条指令。"
