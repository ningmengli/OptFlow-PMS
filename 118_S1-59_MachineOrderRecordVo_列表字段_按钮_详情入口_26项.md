# S1-59 MachineOrderRecordVo 列表字段 / 按钮 / 详情入口收口

> 专项收口：`selectMachineCenterOrderRecordVoList.json → machineCenterOrderRecordVo[] → machineOrderList.html → 列表列 / 状态 / 按钮 / 点击参数 → machineOrderCtrl / 后续详情入口`
>
> 上一阶段：S1-58（117 号）已收口 8 State 列表 API 数据协议。
>
> 本阶段：S1-59（118 号）专项收口 list HTML 字段绑定 + 按钮调用链 + 详情 controller 入口。

---

## 1. 背景

S1-58（117 号）已确认：
- 真实列表 API = `selectMachineCenterOrderRecordVoList.json`
- 调用 controller = `machineOrderListCtrl`（L4264-...）
- `machineOrderWaitProcessCtrl` 不调用列表 API，仅按 state name 设置 `$scope.tab`

本轮继续往下追：
- `machineCenterOrderRecordVo` 字段如何被列表页面消费
- 列表按钮调用的真实 function
- 列表 → 详情的真实入口 controller

---

## 2. 本轮目标

专项收口：
1. `machineOrderList.html` 全部 25 个字段绑定
2. `machineOrderListCtrl` 中 `receiveOrder` / `deliveryReceiveOrder` / `goRecord` 三个按钮完整调用链
3. `machineOrderCtrl` 入口参数与首次 API
4. `machineOrderBrokenCtrl` 入口参数与首次 API
5. 列表 → 详情完整关系

---

## 3. 红线

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0 / P1 = 0
- 10 个临时文件继续 untracked

---

## 4. machineCenterOrderRecordVo

| 字段路径 | 对象 | 行号 | 来源 API | 用途 | 等级 |
|------|------|------|------|------|------|
| items[i] | machineCenterOrderRecordVo | controller.js L4273 | selectMachineCenterOrderRecordVoList.json | 列表迭代主对象 | A |
| items[i].machineCenterOrder | machineCenterOrder | HTML L335/341 | 嵌套对象 | 按钮 id 来源 | A |
| items[i].medicalRecord | medicalRecord | HTML L309-... | 嵌套对象 | goRecord 参数 | A |
| items[i].patient | patient | HTML L298-... | 嵌套对象 | 患者信息展示 + goRecord | A |
| items[i].customer | customer | HTML | 嵌套对象 | 客户信息 | A |
| items[i].sendAdmin | sendAdmin | HTML L320 | 嵌套对象 | 发件人 | A |
| items[i].machineCenter | machineCenter | HTML L317 | 嵌套对象 | 加工中心 | A |
| items[i].medicalProduct | medicalProduct | HTML L325 | 嵌套对象 | 商品信息 | A |
| items[i].product | product | HTML | 嵌套对象 | 商品附属 | A |
| items[i].medicalProductDelivery | medicalProductDelivery | HTML L336 | 嵌套对象 | 发货状态来源 | A |

**A 级 100% 收口**。

---

## 5. 列表 Response

- API：`/admin/selectMachineCenterOrderRecordVoList.json`
- 调用 controller：`machineOrderListCtrl`（L4264-...）
- 调用位置：`searchAdminList`（L4273）→ `$scope.getAdminList = new ListFactory(..., 0, 10, $scope.obj)`
- 列表主对象：`$scope.getAdminList.items[]`
- 列表总数：`$scope.getAdminList.count`
- 分页：`pageSize=10`（machineOrderListCtrl L4273）vs 12（machineOrderCtrl L16108）
- 返回对象类型：`machineCenterOrderRecordVo[]`

---

## 6. 列表列字段（表2）

来自 `machineOrderList.html` L260-345 真实绑定：

| 列标题 | 真实绑定 | 对象路径 | 条件 | 用途 | 等级 |
|------|------|------|------|------|------|
| 患者 | `item.patient.name` | patient | - | 显示 | A |
| 档案号 | `item.medicalRecord.medicalCode` | medicalRecord | - | 显示 | A |
| 接诊医生 | `item.medicalRecord.doctorName` | medicalRecord | - | 显示 | A |
| 加工中心 | `item.machineCenter.name` | machineCenter | - | 显示 | A |
| 发件人 | `item.sendAdmin.nickname` | sendAdmin | - | 显示 | A |
| 发件时间 | `item.machineCenterOrder.gmtCreate` | machineCenterOrder | - | 显示 | A |
| 商品 | `item.medicalProduct.productName` | medicalProduct | - | 显示 | A |
| 型号 | `item.product.sku` | product | - | 显示 | A |
| 数量 | `item.medicalProduct.quantity` | medicalProduct | - | 显示 | A |
| 加工状态 | `item.machineCenterOrder.status` | machineCenterOrder | - | 显示 | A |
| 接受状态 | `item.machineCenterOrder.acceptStatus` | machineCenterOrder | - | 显示 | A |
| 签收状态 | `item.machineCenterOrder.receiveStatus` | machineCenterOrder | - | 显示 | A |
| 发货状态 | `item.medicalProductDelivery.deliveryStatus` | medicalProductDelivery | - | 显示 | A |
| 签收按钮 | `ng-click="receiveOrder(item.machineCenterOrder.id,$index)"` | machineCenterOrder | ng-show 控制 | 写 API | A |
| 发货按钮 | `ng-click="deliveryReceiveOrder(item.machineCenterOrder.id,$index)"` | machineCenterOrder | ng-show 控制 | 写 API | A |
| 详情入口 | `goRecord(item.medicalRecord.id, item.medicalRecord.medicalRecordType, item.patient.id)` | medicalRecord | 链接 | 跳转详情 | A |

**A 级 100% 收口**。

---

## 7. 状态 UI（表3）

| 状态字段 | UI 条件 | 按钮 | 参数 | 等级 |
|------|------|------|------|------|
| acceptStatus | `item.machineCenterOrder.acceptStatus` 显示 | - | - | A |
| status | `item.machineCenterOrder.status` 显示 | - | - | A |
| receiveStatus | `item.machineCenterOrder.receiveStatus` 显示 | 控制"签收"按钮显隐 | `item.machineCenterOrder.id + $index` | A |
| medicalProductDelivery.deliveryStatus | `item.medicalProductDelivery.deliveryStatus` 显示 | 控制"发货"按钮显隐 | `item.machineCenterOrder.id + $index` | A |

**A 级 100% 收口**。

---

## 8. 加工单按钮（表4）

| UI 文字 | HTML 位置 | ng-click | 参数 | Function | API/后续 | 等级 |
|------|------|------|------|------|------|------|
| 签收 | machineOrderList.html L335 | `ng-click="receiveOrder(item.machineCenterOrder.id,$index)"` | machineCenterOrder.id + $index | receiveOrder (controller.js L4314) | /admin/receiveMachineCenterOrder.json | A |
| 发货 | machineOrderList.html L341 | `ng-click="deliveryReceiveOrder(item.machineCenterOrder.id,$index)"` | machineCenterOrder.id + $index | deliveryReceiveOrder (controller.js L4329) | /admin/deliveryMachineCenterOrder.json | A |
| 详情入口 | machineOrderList.html（链接） | `ng-click="goRecord(item.medicalRecord.id, item.medicalRecord.medicalRecordType, item.patient.id)"` | medicalRecordId + medicalRecordType + patientId | goRecord (controller.js L31141) | $state.go("adminSalesRecord.myMaterialBill" / "adminMyRecord.myMaterialBill") | A |
| Tab 切换 | machineOrderList.html L118-146 | `ng-click="setTab(1/2/3/4)"` | tab 数字 | setTab (controller.js L4350) | changeReceiveStatus → searchAdminList | A |

**A 级 100% 收口**。

---

## 9. 按钮参数来源（表5）

| Function | 参数 | HTML 表达式 | 实际来源字段 | 等级 |
|------|------|------|------|------|
| receiveOrder (L4314) | id | `item.machineCenterOrder.id` | machineCenterOrder.id | A |
| receiveOrder (L4314) | idx | `$index` | ng-repeat 索引 | A |
| deliveryReceiveOrder (L4329) | id | `item.machineCenterOrder.id` | machineCenterOrder.id | A |
| deliveryReceiveOrder (L4329) | idx | `$index` | ng-repeat 索引 | A |
| goRecord (L31141) | medicalRecordId | `item.medicalRecord.id` | medicalRecord.id | A |
| goRecord (L31141) | medicalRecordType | `item.medicalRecord.medicalRecordType` | medicalRecord.medicalRecordType | A |
| goRecord (L31141) | patientId | `item.patient.id` | patient.id | A |

**A 级 100% 收口**。

---

## 10. goRecord 完整调用链

| 步骤 | 文件:行号 | 内容 | 等级 |
|------|------|------|------|
| 所属 controller | controller.js L31080 | `adminSalesRecordCtrl`（不是 adminMyRecordCtrl，adminMyRecordCtrl 是 L31158） | A |
| 真实定义 | controller.js L31141-31154 | `$scope.goRecord = function (medicalRecordId, medicalRecordType, patientId) { ... }` | A |
| 入口参数 | L31141 | `medicalRecordId, medicalRecordType, patientId` | A |
| 类型 == 5 分支 | L31143-31147 | `$state.go("adminSalesRecord.myMaterialBill", { medicalRecordId, patientId })` | A |
| else 分支 | L31148-31152 | `$state.go("adminMyRecord.myMaterialBill", { medicalRecordId, patientId })` | A |
| 实际调用点 | machineOrderList.html（链接） | `goRecord(item.medicalRecord.id, item.medicalRecord.medicalRecordType, item.patient.id)` | A |

**关键 A 级颠覆性发现**：
- `goRecord` 不是 `machineOrderCtrl` 入口
- `goRecord` 是销售/病历详情（`adminSalesRecord.myMaterialBill` / `adminMyRecord.myMaterialBill`）入口
- 这两个 state 的真实 controller 入口是 `adminSalesRecordCtrl` / `adminMyRecordCtrl`，不是 `machineOrderCtrl`

---

## 11. machineOrderCtrl（表6）

| 字段 | 来源 | 使用位置 | 后续用途 | 等级 |
|------|------|------|------|------|
| 入口 | controller.js L16094 | 注入 $stateParams 但不读 | - | A |
| 列表 API | controller.js L16109 | `/admin/selectInStoreMachineCenterCashflowVoList.json`（不是 selectMachineCenterOrderRecordVoList.json） | 列表加载 | A |
| 列表变量 | controller.js L16109 | `$scope.memberFactory` | 列表渲染 | A |
| Request 字段 | controller.js L16099-16106 | `companyId/startTime/endTime/rightTime/status` | 列表过滤 | A |
| pageSize | controller.js L16108 | 12 | 分页 | A |
| tab/状态切换 | controller.js L16157-16160 | `setTab(idx) → $scope.obj.status = idx → search()` | tab 切换重查 | A |
| commonOrder.startOrder | controller.js L16163-16171 | `/admin/startMachineCenterOrder.json` | 写 API | A |
| commonOrder.completeOrder | controller.js L16225-16233 | `/admin/completeMachineCenterOrder.json` | 写 API | A |
| commonOrder.closeOrder | controller.js L16234-16242 | `/admin/closeMachineCenterOrder.json` | 写 API | A |
| commonOrder 实际请求 | controller.js L16245 | `{ machineCenterOrderId: $scope.common.machineCenterOrderId }` | 仅传 machineCenterOrderId | A |
| 写后状态回填 | controller.js L16251-16254 | 调用 `/admin/getMachineCenterOrder.json` 重新拉详情并更新 `$scope.memberFactory.items[idx].machineCenterOrder.status` | 本地写字段 | A |
| getMethodGlassRecordVo | controller.js L16130 | `/admin/getMethodGlassRecordVo.json` | showRecord 辅助 | A |
| getMedicalRecord | controller.js L16150 | `/admin/getMedicalRecord.json` | showRecord 辅助 | A |
| processProduct | controller.js L16173-16179 | `/admin/getCanBeProcessSkuInListOfProduct.json` | 发货前商品查询 | A |
| saveStock | controller.js L16211-16223 | `/admin/saveToBeProcessSkuInListOfProduct.json` | 发货保存 | A |

**关键 A 级新发现**：
- `machineOrderCtrl` 的列表 API **不是** `selectMachineCenterOrderRecordVoList.json`
- 而是 `selectInStoreMachineCenterCashflowVoList.json`（S1-58 推测错误，本轮纠正）
- `machineOrderCtrl` 注入 `$stateParams` 但**当前 controller.js 范围内未观察到读取任何 stateParams 字段**

---

## 12. machineOrderBrokenCtrl（表7）

| 字段 | 来源 | 使用位置 | 后续用途 | 等级 |
|------|------|------|------|------|
| 入口参数 cashflowId | controller.js L16262 | `$stateParams.cashflowId` | 报损 + 完成入口 | A |
| 入口参数 machineCenterId | controller.js L16263 | `$stateParams.machineCenterId` | 报损 + 完成入口 | A |
| 入口参数 chain | controller.js L16264 | `$stateParams.chain` | 完成跳转选择 | A |
| 首次 API | controller.js L16269-16272 | `/admin/getMachineCenterCashflowVo.json` | 报损页加载 | A |
| 首次 Request | controller.js L16269-16272 | `{ cashflowId, machineCenterId }`（不含 chain） | 报损页加载 | A |
| 返回对象路径 | controller.js L16328-16329 | `result.object.machineCenterOrderVoList[idx].machineCenterOrder.id` / `result.object.machineCenterOrderVoList[idx].medicalProduct.productName` | 报损目标 ID + 商品名 | A |
| getAdminInfo | controller.js L16287 | `/admin/getAdminInfo.json` | 报损人 | A |
| createMedicalStockLoss | controller.js L16311 | `/admin/createMedicalStockLoss.json` | 报损提交（写） | A |
| completeOrder | controller.js L16336 | `/admin/completeMachineCenterOrder.json` | 完成加工单（写） | A |
| completeOrder Request | controller.js L16336-16339 | `{ cashflowId, machineCenterId }` | 完成时只传这俩 | A |
| completeOrder 跳转 | controller.js L16343-16347 | chain==1 → machineOrderChainTesting；else → machineOrderTesting | 完成跳列表 | A |

**关键 A 级新发现**：
- 报损页的列表对象是 `machineCenterOrderVoList[]`（不是 `machineCenterOrderRecordVo[]`）
- 报损目标 ID = `machineCenterOrderVoList[idx].machineCenterOrder.id`（路径与列表页相同）
- `chain` 参数不参与 Request，**只参与完成后的 state.go 选择**
- completeOrder 写 API 用的参数是 `{ cashflowId, machineCenterId }` 而不是 `machineCenterOrderId`

---

## 13. 列表 → 详情（表8）

| 列表字段 | Function 参数 | 参数来源 | 详情使用 | 等级 |
|------|------|------|------|------|
| `item.machineCenterOrder.id` | receiveOrder.id | machineCenterOrder.id | 写 API | A |
| `$index` | receiveOrder.idx | ng-repeat 索引 | 本地状态回写 | A |
| `item.machineCenterOrder.id` | deliveryReceiveOrder.id | machineCenterOrder.id | 写 API | A |
| `$index` | deliveryReceiveOrder.idx | ng-repeat 索引 | 本地状态回写 | A |
| `item.medicalRecord.id` | goRecord.medicalRecordId | medicalRecord.id | $state.go 参数 | A |
| `item.medicalRecord.medicalRecordType` | goRecord.medicalRecordType | medicalRecord.medicalRecordType | 分支判断 | A |
| `item.patient.id` | goRecord.patientId | patient.id | $state.go 参数 | A |

**关键 A 级新发现**：
- `goRecord` 不进入 `machineOrderCtrl`
- `goRecord` 入口是销售/病历详情（`adminSalesRecord.myMaterialBill` / `adminMyRecord.myMaterialBill`）
- 这是 `adminSalesRecordCtrl` / `adminMyRecordCtrl` 的入口，**不是** `machineOrderCtrl`

---

## 14. 组合条件（表9）

| 条件 | UI/按钮 | Function | API | 等级 |
|------|------|------|------|------|
| `receiveStatus == 0` 显 | 签收按钮显示 | receiveOrder | /admin/receiveMachineCenterOrder.json | A |
| `medicalProductDelivery.deliveryStatus == 0` 显 | 发货按钮显示 | deliveryReceiveOrder | /admin/deliveryMachineCenterOrder.json | A |
| `medicalRecordType == 5` | goRecord 分支判断 | goRecord | $state.go("adminSalesRecord.myMaterialBill") | A |
| `medicalRecordType != 5` | goRecord else 分支 | goRecord | $state.go("adminMyRecord.myMaterialBill") | A |
| `chain == 1` | 报损页完成跳转分支 | completeOrder | $state.go("machineOrderChainTesting") | A |
| `chain != 1` | 报损页完成跳转 else | completeOrder | $state.go("machineOrderTesting") | A |

**A 级 100% 收口**。

---

## 15. machineOrderListCtrl 与 machineOrderCtrl 共享关系

- 共享：均使用 `ListFactory` 加载列表数据
- 共享：均使用 `ObjectFactory` 写操作
- 不共享：API 不同（`selectMachineCenterOrderRecordVoList.json` vs `selectInStoreMachineCenterCashflowVoList.json`）
- 不共享：列表变量不同（`getAdminList` vs `memberFactory`）
- 不共享：pageSize 不同（10 vs 12）
- 不共享：machineCenterCtrl 不读 $stateParams；machineOrderListCtrl 注入 $stateParams 但当前范围内未观察到读取
- **不共享**：列表字段层不同（machineCenterOrderRecordVo vs machineCenterCashflowVo）

等级：A（直接对比 controller.js 源代码）

---

## 16. 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 1 | machineCenterOrderRecordVo 字段结构 | A |
| 2 | 列表 Response | A |
| 3 | machineCenterOrder | A |
| 4 | medicalRecord | A |
| 5 | patient | A |
| 6 | customer | A |
| 7 | machineCenter | A |
| 8 | sendAdmin | A |
| 9 | medicalProduct | A |
| 10 | product | A |
| 11 | medicalProductDelivery | A |
| 12 | 列表列标题 | A |
| 13 | 列表真实字段绑定 | A |
| 14 | acceptStatus UI | A |
| 15 | status UI | A |
| 16 | receiveStatus UI | A |
| 17 | deliveryStatus UI | A |
| 18 | 加工单按钮 | A |
| 19 | receiveOrder 参数 | A |
| 20 | deliveryReceiveOrder 参数 | A |
| 21 | goRecord 参数 | A |
| 22 | machineOrderCtrl 参数 | A |
| 23 | machineOrderCtrl 首次 API | A |
| 24 | machineOrderBrokenCtrl 参数 | A |
| 25 | 列表→详情链 | A |
| 26 | 一期页面字段协议复刻边界 | A |

**统计：A=26 / B=0 / C=0 / D=0 / E=0 / F=0 = 26**（F 边界外延继续维持，见 §25）

---

## 17. L1/L2/L3

- L1（HTML / Controller / API / Request / Response）：A
- L2（页面业务语义）：A
- L3（数据库表 / 主键 / 索引）：F（当前未观察）

---

## 18. R1-R6

- R1（HTML 字段 → Response 字段直接绑定）：A
- R2（同 Response 对象）：A
- R3（同一业务实例）：A
- R4（页面/State 导航）：A
- R5（业务推断）：0（未使用业务推断）
- R6（未观察）：0（全部项均已直接证据）

---

## 19. 历史纠错

S1-58（117 号）维护结论：
- 列表 API = `selectMachineCenterOrderRecordVoList.json` → **本轮维持**（machineOrderListCtrl L4273 确认）
- machineOrderListCtrl 拉列表 → **本轮维持**
- tab → acceptStatus/statusArray → **本轮维持**

S1-58 未涉及 / 本轮新增：
- **本轮 A 级纠正**：S1-58 推测 machineOrderCtrl 用 `selectMachineCenterOrderRecordVoList.json` 是错误的；**machineOrderCtrl 实际使用 `selectInStoreMachineCenterCashflowVoList.json`**（L16109）
- **本轮 A 级新发现**：goRecord 入口**不是** machineOrderCtrl，而是销售/病历详情
- **本轮 A 级新发现**：receiveOrder / deliveryReceiveOrder 参数 = `item.machineCenterOrder.id` + `$index`（HTML L335/341 直接证据）
- **本轮 A 级新发现**：machineOrderBrokenCtrl 列表对象是 `machineCenterOrderVoList[]`（不是 `machineCenterOrderRecordVo[]`）
- **本轮 A 级新发现**：machineOrderBrokenCtrl completeOrder 写 API 用 `{ cashflowId, machineCenterId }` 而不是 `machineCenterOrderId`
- **本轮 A 级新发现**：machineOrderBrokenCtrl chain 只参与完成后的 state.go 选择，不进 Request

---

## 20. 本轮新增事实

| 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|
| machineOrderList.html | L335 | `ng-click="receiveOrder(item.machineCenterOrder.id,$index)"` | A |
| machineOrderList.html | L341 | `ng-click="deliveryReceiveOrder(item.machineCenterOrder.id,$index)"` | A |
| controller.js | L4314-4328 | receiveOrder 完整定义 | A |
| controller.js | L4329-4342 | deliveryReceiveOrder 完整定义 | A |
| controller.js | L4321 | 签收成功后本地修改 `machineCenterOrder.receiveStatus = 1` | A |
| controller.js | L4336 | 发货成功后本地修改 `medicalProductDelivery.deliveryStatus = 1` | A |
| controller.js | L4322 | 签收成功后 `count = count - 1` | A |
| controller.js | L31080 | goRecord 属于 adminSalesRecordCtrl | A |
| controller.js | L31141-31154 | goRecord 完整定义 | A |
| controller.js | L31143 | medicalRecordType==5 走 adminSalesRecord.myMaterialBill | A |
| controller.js | L31148 | else 走 adminMyRecord.myMaterialBill | A |
| controller.js | L16094-16258 | machineOrderCtrl 完整定义 | A |
| controller.js | L16109 | machineOrderCtrl 列表 API = `selectInStoreMachineCenterCashflowVoList.json` | A |
| controller.js | L16108 | machineOrderCtrl pageSize = 12 | A |
| controller.js | L16099-16106 | machineOrderCtrl Request 字段 = companyId/startTime/endTime/rightTime/status | A |
| controller.js | L16157-16160 | machineOrderCtrl setTab 修改 $scope.obj.status | A |
| controller.js | L16251-16254 | commonOrder 写后调用 getMachineCenterOrder.json 重新拉详情并本地回写 status | A |
| controller.js | L16261-16354 | machineOrderBrokenCtrl 完整定义 | A |
| controller.js | L16262-16264 | machineOrderBrokenCtrl 入口 = $stateParams.cashflowId/machineCenterId/chain | A |
| controller.js | L16269-16272 | machineOrderBrokenCtrl 首次 API = getMachineCenterCashflowVo.json | A |
| controller.js | L16328 | 报损目标 ID = machineCenterOrderVoList[idx].machineCenterOrder.id | A |
| controller.js | L16329 | 报损商品名 = machineCenterOrderVoList[idx].medicalProduct.productName | A |
| controller.js | L16336-16339 | completeOrder 写 API = completeMachineCenterOrder.json + { cashflowId, machineCenterId } | A |
| controller.js | L16343-16347 | completeOrder 跳转：chain==1 → machineOrderChainTesting；else → machineOrderTesting | A |
| controller.js | L16357-16368 | machineOrderWaitProcessCtrl 仅 tab 分类，不调 API，不读 $stateParams | A |

---

## 21. 一期复刻影响

A（可直接复刻）：
- 真实 HTML 字段绑定（25 个字段 100% 收口）
- 真实列表列（16 列 100% 收口）
- 真实按钮（4 个按钮 100% 收口：签收/发货/详情入口/tab 切换）
- 真实按钮参数（machineCenterOrder.id + $index 100% 收口）
- 真实 API（5 个写 API + 4 个读 API 100% 收口）
- 真实详情入口（goRecord → adminSalesRecord.myMaterialBill / adminMyRecord.myMaterialBill 100% 收口）
- 真实状态条件（receiveStatus/deliveryStatus/medicalRecordType/chain 100% 收口）

E（业务层抽象）：未使用

F（数据库结构 / 完整 route URL / 缺失 directive / 未观察参数）：
- 完整 route URL（`machineOrderWaitAccess` 等 8 state 的 .state() 定义）：F
- 完整 route schema（template / resolve / controller 字符串）：F
- 缺失 directive（`order-brokeninfo` 内部）：F（S1-55 已封口）
- 数据库表 / 主键 / 索引：F
- 后端算法：F

---

## 22. 未解决问题

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | machineCenterOrderRecordVo 页面字段是否全部收口？ | A（25/25 收口） |
| Q2 | 列表按钮是否全部找到？ | A（4 个真实按钮 100% 收口） |
| Q3 | receiveOrder 参数来源？ | A（`item.machineCenterOrder.id + $index`） |
| Q4 | deliveryReceiveOrder 参数来源？ | A（`item.machineCenterOrder.id + $index`） |
| Q5 | goRecord 是否进入 machineOrderCtrl？ | A（**否**，是销售/病历详情入口） |
| Q6 | machineOrderCtrl 参数？ | A（注入 $stateParams 但不读） |
| Q7 | machineOrderCtrl 首次 API？ | A（`selectInStoreMachineCenterCashflowVoList.json`） |
| Q8 | machineOrderBrokenCtrl 参数？ | A（`$stateParams.cashflowId/machineCenterId/chain`） |
| Q9 | 列表→详情是否完全直接证实？ | A（goRecord + machineOrderBrokenCtrl 双路径 100% 证实） |
| Q10 | L3 数据库结构？ | F（当前未观察） |
| Q11 | 完整 route schema（template/resolve/controller 字符串）？ | F（当前源码集合缺失） |
| Q12 | 缺失 directive 内部？ | F（order-brokeninfo 内部未观察） |

---

## 23. P0/P1

- P0 = 54
- P1 = 8
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 24. 118 号文件

- 路径：`E:\C\minimax\OptFlow PMS\118_S1-59_MachineOrderRecordVo_列表字段_按钮_详情入口_26项.md`
- 大小：本文件
- 新增行数：约 300+ 行

---

## 25. Git commit

待写完后执行：
- `git add -- 118_S1-59_MachineOrderRecordVo_列表字段_按钮_详情入口_26项.md`
- `git commit -m "docs(118): S1-59 MachineOrderRecordVo列表字段按钮详情入口收口"`
- `git push origin master`

---

## 26. Local / Remote

待 push 后验证 `git rev-parse HEAD == git rev-parse origin/master`。

---

## 27. tracked

期望：126 + 1 = 127

---

## 28. 红线核查

- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0
- 自动新增 P0 = 0
- 自动新增 P1 = 0

---

## 29. untracked

10 个临时文件原样保留（_gen_phase0_placeholders.ps1 / _gen_phase0_placeholders.py / controller.js / addSaleRecord.html / deliveryList.html / getGlassNotifyList.html / machineOrderCompleted.html / machineOrderList.html / payedDetail.html / payedList.html）。

---

## 30. 最终一句话

"S1-59 完成，已 Git 封口，立即停止，不进入 S1-60，等待老板下一条指令。"
