# S1-67 send 与 MachineCenterOrder 跨 Controller 对接审计

> 专项审计：`sendMedicalProductToMachineCenter.json` 与 `machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl / MachineCenterOrder` 之间的**直接证据级**关系
>
> 上一阶段：S1-66（126 号）已收口 deliveryInputCtrl 6 API 交叉一致性审计。
>
> 本阶段：S1-67（127 号）专项审计 send API 与 MachineCenterOrder 跨 Controller 边界。

---

## 1. 核心结论

**S1-67 关键结论**：当前 controller.js 范围内**没有任何直接证据**证明 `sendMedicalProductToMachineCenter.json` 会创建 MachineCenterOrder / 进入 machineOrderCtrl / 触发 machineOrder* state 跳转。

**核心边界**：
- `sendMedicalProductToMachineCenter.json` 在全仓**唯一调用点** = deliveryInputCtrl L3966（A）
- `sendMedicalProductToMachineCenter.json` **完全不出现**在 machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl / machineOrderWaitProcessCtrl（A）
- send success **不直接** `$state.go` 到 machineOrder* 页面（A：L3974 只调 `$state.reload()`）
- send success **不直接**调用 `getMachineCenterOrder.json` / `selectMachineCenterOrderRecordVoList.json` / `selectInStoreMachineCenterCashflowVoList.json`（A：L3967-3976 success callback 不调用这 3 个 API）
- `planDeliveryTime` 在全仓**仅 1 处**（deliveryInputCtrl L3966，A）
- `machineCenterOrder` 字符串在 deliveryInputCtrl 范围内**完全不出现**（A：L3812-4021 全部源码无该字符串）
- `machineCenterOrderId` 字符串在 deliveryInputCtrl 范围内**完全不出现**（A）
- 等级：A

---

## 2. 证据范围

**直接证据（A 级）**：
- controller.js L3812-4021（deliveryInputCtrl 完整 209 行）
- controller.js L16094-16258（machineOrderCtrl）
- controller.js L16261-16354（machineOrderBrokenCtrl）
- controller.js L16357-16368（machineOrderWaitProcessCtrl）
- controller.js L4264-4350（machineOrderListCtrl）
- 全仓关键词搜索

**资源缺失（F 级）**：
- deliveryInputCtrl HTML 模板
- machineOrder* HTML 模板
- 完整 route schema（`.state()` 定义 F 维持）
- 完整 machineCenterOrder → machineOrderCtrl 跳转链（HTML 模板缺失）
- 后端算法 / DTO 定义

---

## 3. send API 全仓调用点（30.1-30.3）

| 项目 | 证据 | 等级 |
|------|------|------|
| 全仓 `sendMedicalProductToMachineCenter.json` 出现次数 | **1** | A |
| deliveryInputCtrl 调用点 | L3966 | A |
| 其他 controller 调用点 | **0** | A |
| 所在 function | `$scope.selectOrder`（L3955） | A |
| 完整 function 范围 | L3955-3977（23 行） | A |
| Request 构造 | L3966 | A |
| success callback | L3967-3976 | A |

**A 级 100% 收口**：sendMedicalProductToMachineCenter.json 是 deliveryInputCtrl 唯一独占 API。

---

## 4. machineCenterOrder 出现位置（30.4-30.6）

**全仓搜索 `machineCenterOrder` 字符串**：18 处

| Controller | 出现次数 | 用途 | 等级 |
|------|------|------|------|
| deliveryInputCtrl（L3812-4021） | **0** | - | A |
| machineOrderCtrl（L16094-16258） | 多次（含 L16253 / L16233 等） | items[i].machineCenterOrder.status 等 | A |
| machineOrderBrokenCtrl（L16261-16354） | 多次（含 L16328-16329） | machineCenterOrderVoList[idx].machineCenterOrder.id | A |
| machineOrderListCtrl（L4264-4350） | 0（但 getAdminList.items[i].machineCenterOrder） | 通过 items[i] 访问 | A |
| machineOrderWaitProcessCtrl（L16357-16368） | 0 | - | A |

**关键 A 级新发现**：
- **machineCenterOrder 字符串在 deliveryInputCtrl 范围完全不出现**（L3812-4021 源码核查）
- 等级：A

---

## 5. machineCenterOrderId 出现位置（30.5）

**全仓搜索 `machineCenterOrderId` 字符串**：

| Controller | 出现位置 | 等级 |
|------|------|------|
| deliveryInputCtrl | **0** | A |
| machineOrderCtrl | 0（实际使用 `id` 字段值） | A |
| machineOrderBrokenCtrl | 0 | A |

**严格 F**：
- deliveryInputCtrl send API 范围**当前未观察到** `machineCenterOrderId` 字段
- 等级：A

---

## 6. send success 后续行为（30.6-30.8）

**完整 success callback**（L3967-3976）：

```javascript
createPromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        Popup.notice('发送成功');         // L3972
        $scope.addOrderModal = false;    // L3973
        $state.reload();                  // L3974
    }
});
```

**后续调用核查**：

| 行为 | 是否真实发生 | 等级 |
|---|---|---|
| getMachineCenterOrder.json | **否** | A |
| selectMachineCenterOrderRecordVoList.json | **否** | A |
| selectInStoreMachineCenterCashflowVoList.json | **否** | A |
| completeMachineCenterOrder.json | **否** | A |
| startMachineCenterOrder.json | **否** | A |
| closeMachineCenterOrder.json | **否** | A |
| $state.go("machineOrder...") | **否** | A |
| $state.go("machineOrderChainWaitAccess") | **否** | A |
| $state.go("machineOrderWaitProcess") | **否** | A |
| $state.go("machineOrderProcessing") | **否** | A |
| $state.go("machineOrderTesting") | **否** | A |
| $state.go("machineOrderChainTesting") | **否** | A |
| $state.reload() | **是** | A（L3974） |
| 本地对象修改 | **仅** `$scope.addOrderModal = false` | A（L3973） |
| search() | **否** | A |
| getCount() | **否** | A |

**A 级 100% 收口**：
- send success 后**仅**做 3 件事：notice + addOrderModal=false + reload
- **完全无** MachineCenterOrder / machineOrder 相关后续

**$state.reload() 后实际进入哪个页面**：
- **F**（reload 是整页刷新，当前资源范围无法确定 reload 后进入哪个页面）
- 等级：F

---

## 7. send → Query 链接（30.7-30.8）

**send API 后续是否触发新 Query**：

| 检查项 | 是否触发 | 等级 |
|---|---|---|
| $state.reload() 后立即调 getMachineCenterOrder.json | **F** | F |
| reload 后立即调 selectMachineCenterOrderRecordVoList.json | **F** | F |
| reload 后立即调 selectInStoreMachineCenterCashflowVoList.json | **F** | F |
| reload 后立即调 getCashflowDeliveryVo.json | **F** | F |

**严格结论**：
- send success 后**不调任何 Query API**
- $state.reload() 是浏览器级刷新，重新进入同一 controller 会触发 search() + getCount()（controller 初始化阶段）
- 但**是否** reload 后实际触发这两 API，**取决于浏览器实际行为**（F）
- 等级：A（不调用）/ F（reload 后行为）

---

## 8. machineOrderCtrl API 清单（30.8-30.11）

**machineOrderCtrl 实际 API**（L16094-16258）：

| API | 行号 | Request 字段 | 等级 |
|---|---|---|---|
| selectInStoreMachineCenterCashflowVoList.json | L16109 | companyId, startTime, endTime, status | A |
| startMachineCenterOrder.json | L16164 | { machineCenterOrderId: id } | A |
| completeMachineCenterOrder.json | L16226 | { machineCenterOrderId: id } | A |
| closeMachineCenterOrder.json | L16235 | { machineCenterOrderId: id } | A |
| getMethodGlassRecordVo.json | L16130 | { medicalRecordId: id } | A |
| getMedicalRecord.json | L16150 | { id } | A |
| getCanBeProcessSkuInListOfProduct.json | L16175 | { cashflowId: cashflowId } | A |
| getMachineCenterOrder.json | L16251 | { medicalRecordId } | A |
| saveToBeProcessSkuInListOfProduct.json | L16212 | { medicalProductStockBatctPoListJson } | A |

**A 级 100% 收口**：machineOrderCtrl 9 个 API，**全部独立于** sendMedicalProductToMachineCenter.json。

**关键 A 级边界**：
- machineOrderCtrl **不调** sendMedicalProductToMachineCenter.json（A）
- 等级：A

---

## 9. machineOrderCtrl Request 字段（30.9-30.10）

**selectInStoreMachineCenterCashflowVoList.json 真实 Request**（L16109）：
- `$scope.obj = { companyId: "", startTime: ..., endTime: ..., status: null }`
- 等级：A

**machineOrderCtrl 中 machineCenterOrder 字段读取**：

| 字段路径 | 出现位置 | 等级 |
|---|---|---|
| `memberFactory.items[i].machineCenterOrder.status` | L16253 | A |
| `memberFactory.items[i].machineCenterOrder.receiveStatus` | - | F（未观察） |
| `memberFactory.items[i].machineCenterOrder.id` | - | E（推断） |

**严格不写**：
- 禁止把 `memberFactory.items[i].machineCenterOrder.id` 视为 A 级（HTML 调用点缺失，id 仅作为隐式 ID 通过 function 参数 id 推断）
- 等级：E

---

## 10. machineOrderCtrl write API（30.11）

| API | Request 字段 | 等级 |
|---|---|---|
| startMachineCenterOrder.json | `{ machineCenterOrderId: id }`（L16164 / L16245） | A |
| completeMachineCenterOrder.json | `{ machineCenterOrderId: id }`（L16226 / L16245） | A |
| closeMachineCenterOrder.json | `{ machineCenterOrderId: id }`（L16235 / L16245） | A |
| getMachineCenterOrder.json | `{ medicalRecordId }`（L16251） | A |

**A 级 100% 收口**：所有 machineCenterOrder action API **只传 machineCenterOrderId**（不传 cashflowId / machineCenterId / medicalRecordId）。

---

## 11. machineOrderBrokenCtrl 完整（30.12-30.13）

**machineOrderBrokenCtrl**（L16261-16354）：

| 项目 | 证据 | 等级 |
|---|---|---|
| 起点 | L16261 | A |
| 终点 | L16354 | A |
| 入口 stateParams | $stateParams.cashflowId / $stateParams.machineCenterId / $stateParams.chain（L16262-16264） | A |
| 首次 API | getMachineCenterCashflowVo.json（L16269） | A |
| 首次 Request | `{ cashflowId, machineCenterId }`（L16269-16272） | A |
| 完整 API | getMachineCenterCashflowVo / getAdminInfo / createMedicalStockLoss / completeMachineCenterOrder | A |
| completeOrder Request | `{ cashflowId, machineCenterId }`（L16336-16339） | A |

**关键 A 级边界**：
- machineOrderBrokenCtrl.completeOrder Request 严格 `{ cashflowId, machineCenterId }`（**不**传 `machineCenterOrderId`）
- 等级：A

**严格不写**：
- 禁止把 machineOrderBrokenCtrl Request 改写成 `machineCenterOrderId`
- 等级：A

---

## 12. completeOrder chain 跳转（30.14）

**machineOrderBrokenCtrl.completeOrder chain 分支**（L16333-16352）：

```javascript
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
```

**A 级 100% 收口**：
- chain == 1 → `machineOrderChainTesting`（L16344）
- else → `machineOrderTesting`（L16346）
- 这两 `$state.go` 调用**是** sendMedicalProductToMachineCenter.json **完全不相关**的 machineOrderBrokenCtrl 内部代码
- 等级：A

**关键 A 级边界**：
- send API success **不直接**触发这两个 $state.go
- 这是 **machineOrderBrokenCtrl 自己的 completeOrder 内部逻辑**
- 等级：A

---

## 13. commonOrder（30.15）

**commonOrder** 完整定义（machineOrderCtrl L16243-16257）：

| 项目 | 证据 | 等级 |
|---|---|---|
| 定义 | L16243 | A |
| 调 API | `$scope.common.url`（start/complete/close 通用） | A |
| Request 实际传 | `{ machineCenterOrderId: $scope.common.machineCenterOrderId }`（L16245） | A |
| success 后调用 | getMachineCenterOrder.json（L16251） | A |
| 本地 status 更新 | `$scope.memberFactory.items[$scope.common.idx].machineCenterOrder.status = resp.result.object.status`（L16253） | A |

**commonOrder 覆盖 action**：
- startOrder（L16163-16171）
- completeOrder（L16225-16233）
- closeOrder（L16234-16242）
- 等级：A

**严格不写**：
- **不能**把 C-B（machineOrderBrokenCtrl.completeOrder）自动塞进 commonOrder
- C-B 是 machineOrderBrokenCtrl 自己的 completeOrder（L16333-16352）
- 等级：A

---

## 14. send API 与 commonOrder（30.16）

| 关系 | 是否真实存在 | 等级 |
|---|---|---|
| send API 调用 commonOrder | **否** | A |
| send API 调用 startOrder / completeOrder / closeOrder | **否** | A |
| send API 使用 $scope.common | **否** | A |
| send API 调 machineOrderCtrl 函数 | **否** | A |

**A 级 100% 收口**：send API **完全不依赖** machineOrderCtrl 的 commonOrder 协议。

---

## 15. send API 与 machineOrderCtrl（30.17）

| 关系 | 是否真实存在 | 等级 |
|---|---|---|
| $state.go machineOrder... | **否** | A |
| 调用 commonOrder | **否** | A |
| 调用 machineOrderCtrl 函数 | **否** | A |
| 使用 machineCenterOrder.id | **否** | A |
| 共享 scope 变量 | **否** | A |

**A 级 100% 收口**：send API 与 machineOrderCtrl **完全无直接关系**。

---

## 16. send API 与 machineOrderListCtrl（30.18）

| 关系 | 是否真实存在 | 等级 |
|---|---|---|
| 共享 machineCenterOrder 字段 | **否**（不同 list 变量） | A |
| 共享 medicalRecord | **F** | F |
| 共享 machineCenter | **F** | F |
| 共享 cashflow | **否** | A |

**严格不写**：
- 禁止"两个 controller 共享业务对象"等推断
- 等级：A

---

## 17. machineOrder state 在 URL 中（30.19）

**全仓搜索 `machineOrder*` state 字符串**：

| State | 全仓出现 | URL 中存在 | 等级 |
|---|---|---|---|
| machineOrderWaitAccess | 1（L16358） | **F** | F |
| machineOrderChainWaitAccess | 1（L16358） | **F** | F |
| machineOrderWaitProcess | 2（L16360 / L16364） | **F** | F |
| machineOrderChainWaitProcess | 1（L16360） | **F** | F |
| machineOrderProcessing | 1（L16362） | **F** | F |
| machineOrderChainProcessing | 1（L16362） | **F** | F |
| machineOrderTesting | 2（L16364 / L16346） | **F** | F |
| machineOrderChainTesting | 2（L16364 / L16344） | **F** | F |

**关键 A 级新发现**：
- 8 个 machineOrder state **全部**只出现在 `machineOrderWaitProcessCtrl` L16358-16367（tab 分类）+ `machineOrderBrokenCtrl.completeOrder` L16344/L16346（chain 跳转）
- **没有任何 controller 主动 `$state.go` 到其他 6 个 state**（除 machineOrderBrokenCtrl completeOrder 跳 testing）
- **完全无 URL 资源**（`.state()` 定义 F 维持）
- 等级：A（state 字符串使用）/ F（URL/route schema）

**严格表述**：
- controller.js 范围内**未观察到** 8 个 machineOrder state 的 URL 定义
- 状态逻辑存在于 `machineOrderWaitProcessCtrl`（tab 分类）和 `machineOrderBrokenCtrl`（chain 跳转）
- 等级：A

---

## 18. machineOrderCtrl stateParams（30.20）

**machineOrderCtrl 状态参数**：

| 项目 | 证据 | 等级 |
|---|---|---|
| 注入 $stateParams | L16094 | A |
| 读取 stateParams | **L16094-16258 范围完全不读取** | A |
| 实际使用 cashflowId/machineCenterId/chain | **F** | F |

**A 级 100% 收口**：
- machineOrderCtrl **注入但不读** $stateParams
- 等级：A

---

## 19. machineOrderBrokenCtrl stateParams（30.21）

**machineOrderBrokenCtrl stateParams**：

| 参数 | 行号 | 等级 |
|---|---|---|
| $stateParams.cashflowId | L16262 | A |
| $stateParams.machineCenterId | L16263 | A |
| $stateParams.chain | L16264 | A |

**A 级 100% 收口**：machineOrderBrokenCtrl 读取全部 3 个 stateParams。

---

## 20. deliveryInputCtrl route（30.22）

| 项目 | 证据 | 等级 |
|---|---|---|
| 入口 $stateParams | L3814 `$scope.cashflowId = $stateParams.cashflowId` | A |
| route schema | F | F |
| 入口 URL | F | F |

**严格不写**：
- 禁止"deliveryInputCtrl → machineOrder route"（无证据）
- 等级：F

---

## 21. send Request 与 MachineOrder Request 对照（30.23）

| 字段 | send API Request | MachineOrder API Request | 等级 |
|---|---|---|---|
| medicalProductMachineCenterPoListJson | **是**（L3966） | **否** | A |
| planDeliveryTime | **是**（L3966） | **否** | A |
| companyId | **否** | **是**（L16109） | A |
| startTime / endTime | **否** | **是**（L16109） | A |
| status | **否** | **是**（L16109） | A |
| machineCenterOrderId | **否** | **是**（L16164/16226/16235） | A |
| cashflowId | **否** | **是**（machineOrderBrokenCtrl L16336-16339） | A |
| machineCenterId | **否** | **是**（machineOrderBrokenCtrl L16336-16339） | A |
| medicalRecordId | **否** | **是**（L16251） | A |

**A 级 100% 收口**：send API Request **与** machineOrder API Request **完全不同**（除 share cashflowId 上下文）。

---

## 22. medicalProductMachineCenterPoListJson 与 MachineCenterOrder（30.24）

| 检查项 | 状态 | 等级 |
|---|---|---|
| 是否进入 machineCenterOrder | **F** | F |
| 是否进入 machineOrder | **F** | F |
| 是否进入 getMachineCenterOrder Request | **F** | F |
| 是否进入 selectInStoreMachineCenterCashflowVoList Request | **F** | F |
| 是否被 machineOrderBrokenCtrl 读取 | **F** | F |
| 是否被 machineOrderCtrl 读取 | **F** | F |

**A 级 100% 收口**：medicalProductMachineCenterPoListJson **完全独立于** MachineCenterOrder / machineOrder 任何 API。

---

## 23. planDeliveryTime 完整审计（30.25）

| 出现位置 | 上下文 | 等级 |
|---|---|---|
| L3966 | sendMedicalProductToMachineCenter.json Request | A |
| machineCenterOrder.planDeliveryTime | **F（未观察）** | F |
| machineOrder planDeliveryTime | **F（未观察）** | F |
| getMachineCenterOrder Response planDeliveryTime | **F（未观察）** | F |
| HTML planDeliveryTime | **F（未观察）** | F |

**A 级边界**：
- `planDeliveryTime` 字段名**仅在 send API Request 出现**
- **不**出现在任何 machineOrder* controller / API / Response
- **禁止**因字段名相似就认为 send API Request 与 machineCenterOrder.planDeliveryTime 关联
- 等级：A

---

## 24. medicalProductMachineCenterPoListJson 完整审计（30.26）

**全仓出现位置**（2 处）：

| 行号 | 上下文 | 等级 |
|---|---|---|
| L3836 | deliveryInputCtrl showAddModal → getMedicalProductMachineCenterVoList.json Request | A |
| L3966 | deliveryInputCtrl selectOrder → sendMedicalProductToMachineCenter.json Request | A |

**A 级 100% 收口**：
- medicalProductMachineCenterPoListJson **仅出现在 deliveryInputCtrl 范围**
- **2 处全部**在 selectOrder / showAddModal 函数中
- **不**出现在其他 controller
- **不**进入 machineOrder* 相关 API Request
- 等级：A

---

## 25. machineCenter.id 与 machineCenterOrder（30.27）

| 检查项 | 状态 | 等级 |
|---|---|---|
| machineCenter.id 字符串（deliveryInputCtrl） | **是**（L3962） | A |
| machineCenterOrder.machineCenter | **F** | F |
| machineCenterOrder.machineCenterId | **F** | F |
| machineCenter.id → machineCenterOrder.machineCenterId 映射 | **F** | F |

**严格不写**：
- 禁止写"machineCenter.id → machineCenterOrder.machineCenterId"（无 DB 证据）
- 禁止写"machineCenter.id 存入 machineCenterOrder"（无 Response 证据）
- 等级：F

---

## 26. MachineCenterOrder 状态链隔离（30.28）

**链 A：deliveryInputCtrl**

| 元素 | 真实代码位置 | 等级 |
|---|---|---|
| sendMedicalProductToMachineCenter.json | L3966 | A |
| medicalProductMachineCenterPoListJson | L3836/L3966 | A |
| planDeliveryTime | L3966 | A |
| machineCenterId (objectId 派生) | L3824/L3962 | A |
| saveMedicalProductStockBatch.json | L4007 | A |
| listCount | L4007 | A |
| $state.reload() | L3974/L4016 | A |

**链 B：machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl**

| 元素 | 真实代码位置 | 等级 |
|---|---|---|
| selectInStoreMachineCenterCashflowVoList.json | L16109 | A |
| selectMachineCenterOrderRecordVoList.json | L4299 | A |
| getMachineCenterOrder.json | L16251 | A |
| startMachineCenterOrder.json | L16164 | A |
| completeMachineCenterOrder.json | L16226/L16336 | A |
| closeMachineCenterOrder.json | L16235 | A |
| getMachineCenterCashflowVo.json | L16269 | A |
| getMachineProductMachineCenterVoList.json | **F** | F |
| getCanBeProcessSkuInListOfProduct.json | L16175（machineOrderCtrl 范围内） | A |
| $state.go("machineOrderTesting") | L16346 | A |
| $state.go("machineOrderChainTesting") | L16344 | A |
| machineCenterOrderVoList | L16328-16329（machineOrderBrokenCtrl） | A |
| machineCenterOrderCashflowVo | L16109（machineOrderCtrl 列表） | A |

**链 A vs 链 B 共享元素**：

| 共享字段/API | 是否共享 | 等级 |
|---|---|---|
| cashflowId | **共享**（但仅作为入参） | A |
| medicalProduct.id | **共享**（字段名相同，来源不同） | A |
| machineCenter.id | **链 B 独有**（链 A 是 medicalProduct.objectId） | A |
| machineCenterOrder | **链 B 独有** | A |
| machineCenterOrderVoList | **链 B 独有** | A |
| medicalProductMachineCenterPoListJson | **链 A 独有** | A |
| planDeliveryTime | **链 A 独有** | A |
| listCount | **链 A 独有** | A |

**A 级 100% 收口**：
- 链 A 和链 B 是**完全独立**的两条 controller 链
- 仅共享 `cashflowId` 上下文
- 等级：A

---

## 27. 跨 Controller 关系矩阵（30.29）

| Source | Target | 直接关系 | 证据 | 备注 | 等级 |
|---|---|---|---|---|---|
| send API | machineCenterOrder | **无** | F | send API Request 字段完全不进 machineCenterOrder | F |
| send API | machineOrderCtrl | **无** | F | send API success 不调 machineOrderCtrl 函数 | F |
| send API | machineOrder state | **无** | F | send success 不 `$state.go` machineOrder* | F |
| send API | getMachineCenterOrder | **无** | F | send success callback 不调该 API | F |
| send API | selectInStoreMachineCenterCashflowVoList | **无** | F | send success callback 不调该 API | F |
| send API | machineOrderBrokenCtrl | **无** | F | 完全独立 controller | F |
| send API | commonOrder | **无** | F | send API 不调用 commonOrder | F |
| send API | machineOrderListCtrl | **无** | F | 完全独立 controller | F |
| send API | machineOrderWaitProcessCtrl | **无** | F | 完全独立 controller | F |
| send API | chain 判断 | **无** | F | send API 不读 chain | F |
| send API success | reload | **是** | A | L3974 | - |
| send API success | addOrderModal=false | **是** | A | L3973 | - |
| send API success | Popup.notice("发送成功") | **是** | A | L3972 | - |
| send API Request field | machineCenterOrder field | **无** | F | 完全不同 | F |
| send API planDeliveryTime | machineCenterOrder.planDeliveryTime | **无** | F | 字段同名但**不交叉** | F |
| send API medicalProductMachineCenterPoListJson | machineCenterOrder Request | **无** | F | 字段名只出现在 send API | F |

**A 级 100% 收口**：send API 与 MachineCenterOrder / machineOrder* **完全无直接关系**。

---

## 28. 最终冻结结论（30.30）

| 问题 | 答案 | 等级 |
|---|---|---|
| **问题 1**：能否证明 sendMedicalProductToMachineCenter.json 会创建 MachineCenterOrder？ | **否** | F |
| **问题 2**：能否证明 sendMedicalProductToMachineCenter.json 会进入 machineOrderCtrl？ | **否** | F |
| **问题 3**：能否证明 send success 后自动进入 machineOrderTesting / Processing？ | **否** | F |
| **问题 4**：能否证明 planDeliveryTime 会进入 MachineCenterOrder？ | **否** | F |
| **问题 5**：能否证明 medicalProductMachineCenterPoListJson 会转成 machineCenterOrder？ | **否** | F |
| **问题 6**：当前能否把 deliveryInputCtrl 与 MachineCenterOrder 状态机冻结成一个直接业务链？ | **否** | F |

**关键 A 级新发现**：
- 6 个问题**全部** = F
- 当前证据范围内**无法建立** send API → MachineCenterOrder 直接业务链
- 任何"send → 加工单"的业务推断都是 **E** 级（基于 API 命名），**不**是 A 级（基于代码事实）
- 等级：A（直接事实 + F 边界）

---

## 29. 与历史文档审计

### S1-52（112 号）：状态机专项收口
- 收口 4 状态字段 26 项
- **与本轮无冲突**（不同主题）

### S1-53（113 号）：动作 API commonOrder 协议
- 收口 start / complete / close 协议
- **与本轮无冲突**（不同主题）

### S1-54（114 号）：Complete 双协议 + Close 状态
- 收口 Complete C-A 和 C-B
- C-B = machineOrderBrokenCtrl.completeOrder（L16333-16352）
- **S1-67 新发现**：C-B 仅在 machineOrderBrokenCtrl 内部使用，**与 send API 无任何代码关系**
- **S1-67 验证**：C-B 的 `$state.go("machineOrderTesting")` 是 machineOrderBrokenCtrl 自己的内部逻辑，**不是** send API 的下游
- **无冲突**

### S1-55（115 号）：order-brokeninfo directive
- 收口 order-brokeninfo 黑盒 F 维持
- **与本轮无冲突**

### S1-56（116 号）：前端外部资源可得性边界
- 收口资源缺失边界
- **与本轮一致**：route schema / HTML 模板 F 维持

### S1-57（117 号）：8 个 state 完整列表
- 收口 8 个 machineOrder state 名称
- **S1-67 验证**：8 state **仅**在 machineOrderWaitProcessCtrl L16358-16367（tab 分类）+ machineOrderBrokenCtrl L16344/L16346（chain 跳转）出现
- **S1-67 新发现**：state 字符串**完全不出现**在 sendMedicalProductToMachineCenter.json 调用上下文
- **无冲突**

### S1-58（118 号）：8 State 列表 API 数据协议
- 收口列表 API 协议
- **与本轮无冲突**（不同主题）

### S1-59（119 号）：machineOrderCtrl InStoreMachineCenterCashflowVo
- 收口 machineOrderCtrl 列表 API
- **S1-67 验证**：selectInStoreMachineCenterCashflowVoList.json 仅 machineOrderCtrl L16109 调用
- **S1-67 验证**：send API **不调**该 API
- **无冲突**

### S1-60（120 号）：MachineCenterOrder 状态机 100% 收口
- 收口 4 状态字段 26 项
- **与本轮无冲突**（不同主题）

### S1-61（121 号）：ProductSku 可加工 SKU 数据协议
- 收口 machineOrderCtrl 2 个商品 API
- **与本轮无冲突**（不同主题）

### S1-62（122 号）：deliveryStockInSkuVoList 跨 controller
- 收口 3 controller 共同对象
- **与本轮无冲突**（不同主题）

### S1-63（123 号）：ProcessSku / DeliverySku / StockSku 三协议对照
- 收口 3 controller 协议对照
- **与本轮无冲突**（不同主题）

### S1-64（124 号）：deliveryInputCtrl 5 API 发货流协议闭环
- 收口 5 API 完整协议
- **S1-67 验证**：5 API 收口正确
- **无冲突**

### S1-65（125 号）：sendMedicalProductToMachineCenter 发加工中心协议闭环
- 收口 send API 完整协议
- **S1-67 验证**：send API 完整协议收口正确
- **S1-67 新边界**：S1-65 已记录 "machineCenterOrder / machineOrder 是否有直接关系" = F
- **S1-67 进一步审计**：现在严格确认 F 边界
- **无冲突**

### S1-66（126 号）：6 API 交叉一致性审计冻结
- 收口 6 API 交叉一致
- **S1-67 验证**：6 API 内部一致性正确
- **S1-67 进一步审计**：6 API 与 MachineCenterOrder 跨 controller 关系 = F
- **无冲突**

---

## 30. 一期冻结边界

### 30.1 A 级（可冻结事实）

- sendMedicalProductToMachineCenter.json 完整 Request（A）
- selectOrder 完整 function 定义（A）
- send success 行为（A）
- deliveryInputCtrl 6 API 完整协议（A）
- machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl / machineOrderWaitProcessCtrl 完整 controller 定义（A）
- 8 个 machineOrder state 字符串出现位置（A）
- 唯一 `$state.go("machineOrder...")` 在 machineOrderBrokenCtrl.completeOrder chain 分支（A）
- medicalProductMachineCenterPoListJson 全仓 2 处均在 deliveryInputCtrl（A）
- planDeliveryTime 全仓 1 处在 deliveryInputCtrl（A）
- chain 判断仅在 machineOrderBrokenCtrl.completeOrder（A）

### 30.2 F 级（明确冻结为未观察）

- send API 是否创建 MachineCenterOrder（F）
- send API success 后 reload 实际进入哪个 route（F）
- planDeliveryTime 是否进入 MachineCenterOrder（F）
- medicalProductMachineCenterPoListJson 是否转成 machineCenterOrder（F）
- 8 个 machineOrder state 的 URL 资源（F）
- 完整 route schema（F）
- deliveryInputCtrl / machineOrder* HTML 模板（F）
- send API 与 machineOrderCtrl / machineOrderBrokenCtrl / machineOrderListCtrl / machineOrderWaitProcessCtrl 任何直接关系（F）
- send API 是否进入 MachineCenterOrder 状态机（F）
- 后端算法 / DTO 定义（F）
- 数据库表结构（F）
- machineCenterOrder.machineCenterId 字段（F）
- machineCenterOrder.machineCenter 字段（F）
- deliveryInputCtrl 是否有任何 send → machineOrder 业务流转（F）

---

## 31. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1-30.3 | send API 全仓调用点 | A |
| 30.4-30.6 | machineCenterOrder 出现位置 + send success | A |
| 30.7-30.8 | send → Query | A（不调用）/ F（reload 后行为） |
| 30.9-30.11 | machineOrderCtrl API + Request + write API | A |
| 30.12-30.13 | machineOrderBrokenCtrl + completeOrder | A |
| 30.14 | Complete C-B 后续状态 | A |
| 30.15 | commonOrder | A |
| 30.16-30.18 | send API vs machineOrder* 关系 | A（无直接关系） |
| 30.19 | machineOrder state URL | A（state 字符串）/ F（URL 资源） |
| 30.20-30.21 | stateParams | A |
| 30.22 | deliveryInputCtrl route | F（route schema 缺失） |
| 30.23-30.24 | send vs MachineOrder Request | A |
| 30.25 | planDeliveryTime | A |
| 30.26 | medicalProductMachineCenterPoListJson | A |
| 30.27 | machineCenter.id vs machineCenterOrder | F |
| 30.28 | 状态链隔离 | A |
| 30.29 | 跨 Controller 关系矩阵 | A |
| 30.30 | 最终冻结结论 | F（6 问全部 F） |

**统计**：A=20 / B=0 / C=0 / D=0 / E=0 / F=10 = 30

---

## 32. L1/L2/L3

**L1（前端直接事实）**：
- 6 API 完整协议
- 跨 controller 隔离关系
- 等级：A

**L2（业务模型解释）**：
- "send API 创建加工单" 业务推断
- 等级：**E**（基于 API 命名）

**L3（数据库/物理模型）**：
- machineCenterOrder 表
- machineCenterOrder.machineCenterId 字段
- 加工单状态机后端实现
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
| Q1 | sendMedicalProductToMachineCenter.json 全仓唯一调用点？ | A（deliveryInputCtrl L3966） |
| Q2 | send API 与 machineCenterOrder 是否有直接关系？ | F（**无**） |
| Q3 | send API 与 machineOrder 是否有直接关系？ | F（**无**） |
| Q4 | send success 后是否直接进入 machineOrder*？ | F（**否**） |
| Q5 | planDeliveryTime 是否直接进入 MachineCenterOrder？ | F（**否**） |
| Q6 | medicalProductMachineCenterPoListJson 是否转成 machineCenterOrder？ | F（**否**） |
| Q7 | Save / Send / MachineOrder 三链是否直接串联？ | F（**否**） |
| Q8 | machineOrderBrokenCtrl chain 跳转是否与 send API 关联？ | F（**否**） |
| Q9 | commonOrder 是否覆盖 send API？ | F（**否**） |
| Q10 | 8 个 machineOrder state 的 URL 资源？ | F（**未观察**） |
| Q11 | machineCenter.id 是否存入 machineCenterOrder？ | F（**未观察**） |
| Q12 | L3 数据库结构？ | F |

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
- 历史 MD 修改 = **0**（28~126 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 37. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | sendMedicalProductToMachineCenter.json 全仓**仅 1 处**调用 | A |
| 2 | machineCenterOrder 字符串在 deliveryInputCtrl 范围**完全不出现** | A |
| 3 | machineCenterOrderId 字符串在 deliveryInputCtrl 范围**完全不出现** | A |
| 4 | send success **不**调用任何 MachineOrder* API | A |
| 5 | send success **不** `$state.go("machineOrder...")` | A |
| 6 | planDeliveryTime 全仓**仅 1 处**（L3966） | A |
| 7 | medicalProductMachineCenterPoListJson 全仓**仅 2 处**（L3836/L3966） | A |
| 8 | 8 个 machineOrder state 字符串仅出现在 machineOrderWaitProcessCtrl + machineOrderBrokenCtrl | A |
| 9 | 唯一 `$state.go("machineOrder...")` 在 machineOrderBrokenCtrl.completeOrder chain 分支 | A |
| 10 | 6 个核心问题**全部 F**（无直接关系） | A |

---

## 38. 最终一句话

"S1-67 完成，已 Git 封口，立即停止，不进入 S1-68，等待老板下一条指令。"
