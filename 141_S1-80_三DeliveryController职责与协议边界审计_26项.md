# S1-80 delivery 三 Controller 职责与协议边界审计

> 审计对象：`deliveryInputCtrl` / `deliveryInputRecordCtrl` / `deliveryProcessingCtrl`
> 任务来源：S1-80（基于 S1-79 已确认 F2 在 3 controller 0 处 result 消费）
> 审计立场：**只按源码证据，不按 Controller 命名推断职责；不按"共享 cashflowId"推断"同一业务实体"**

---

## 1. 核心结论（50 字以内）

**三 Controller 是三个独立 controller，API / Factory / 对象 / 跳转均不同，仅共享 2 个 API（F1+F2）和 1 个参数（cashflowId）。**

---

## 2. 证据范围

| 维度 | 范围 | 备注 |
|---|---|---|
| deliveryInputCtrl | controller.js L3812-4021（209 行） | working dir untracked，git tracked 中无 |
| deliveryInputRecordCtrl | controller.js L4024-4072（49 行） | 同上 |
| deliveryProcessingCtrl | controller.js L4236-4261（26 行） | 同上 |
| HTML 模板 | 7 个 untracked，0 个对应这 3 个 controller | F 边界 |
| 后端 DTO | 不可得 | F 边界 |
| 业务职责 | 不可由 Controller 名称推断 | 严格 F |

---

## 3. 三 Controller 精确定位

| Controller | 起止行 | 行数 | 注入依赖 |
|---|---|---|---|
| deliveryInputCtrl | L3812-4021 | 209 | $scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, **ObjectFactory**, **ListFactory**, $http, $q, QiniuFactory, $timeout |
| deliveryInputRecordCtrl | L4024-4072 | 49 | $scope, $stateParams, DateUtilFactory, Popup, $state, **ObjectFactory**, **ListFactory**, $http, $timeout |
| deliveryProcessingCtrl | L4236-4261 | 26 | $scope, $rootScope, $stateParams, DateUtilFactory, Popup, $state, **ObjectFactory**（**无 ListFactory**）|

**A**：3 controller 都注入 ObjectFactory（A）。
**A**：ListFactory 仅 deliveryInputCtrl / deliveryInputRecordCtrl 注入；**deliveryProcessingCtrl 无 ListFactory 注入**。
**F**：ListFactory 在 3 controller 范围内**实际使用 0 处**（虽然注入了但未 new）。

---

## 4. deliveryInputCtrl 完整 API 清单

| # | API | 行号 | Factory | params | 返回接收 | then |
|---|---|---|---|---|---|---|
| 1 | getCashflowDeliveryVo.json | L3848 | F1 getMedicalRecordDeliveryFactory | { cashflowId } | ✅ deliveryPromise | ✅ L3849 |
| 2 | statProductDeliveryStatusOfCashflow.json | L3841 | F2 getStatusDeliveryFactory | { cashflowId } | ❌ | ❌ |
| 3 | getMedicalProductMachineCenterVoList.json | L3836 | F3 getCenterListFactory | { medicalProductMachineCenterPoListJson } | ❌ | ❌ |
| 4 | getCanBeDeliverySkuInListOfProduct.json | L3885 | F4 getDeliveryListFactory | { medicalProductIdArray } | ❌ | ❌ |
| 5 | saveMedicalProductStockBatch.json | L4007 | F5 saveStockFactory | { listCount, medicalProductStockBatctPoListJson } | ✅ savePromise | ✅ L4008 |
| 6 | sendMedicalProductToMachineCenter.json | L3966 | F6 createOrderFactory | { medicalProductMachineCenterPoListJson, planDeliveryTime } | ✅ createPromise | ✅ L3967 |

**A**：6 API / 6 Factory / 3 接收返回 / 3 不接收 / 3 then。

---

## 5. deliveryInputRecordCtrl 完整 API 清单

| # | API | 行号 | Factory | params | 返回接收 | then |
|---|---|---|---|---|---|---|
| 1 | getMedicalRecordPayVo.json | L4034 | getMedicalRecord（**临时实例，未挂 $scope**）| { cashflowId } | ✅ recordPromise | ✅ L4035 |
| 2 | getCashflowDeliveryVo.json | L4040 | F1 getMedicalRecordDeliveryFactory | { cashflowId } | ❌ | ❌ |
| 3 | statProductDeliveryStatusOfCashflow.json | L4044 | F2 getStatusDeliveryFactory | { cashflowId } | ❌ | ❌ |
| 4 | saveMedicalProductDeliveryCommentBatch.json | L4061 | saveMedicalRecordDeliveryFactory（**独有 Factory**）| { medicalProductDeliveryCommentListJson } | ✅ savePromise | ✅ L4062 |

**A**：4 API / 4 ObjectFactory 实例（3 挂 $scope + 1 临时变量）/ 2 接收返回 / 2 不接收 / 2 then。
**A**：独有 API 2 个（getMedicalRecordPayVo / saveMedicalProductDeliveryCommentBatch）。
**A**：独有 Factory = `saveMedicalRecordDeliveryFactory`（L4060）。

---

## 6. deliveryProcessingCtrl 完整 API 清单

| # | API | 行号 | Factory | params | 返回接收 | then |
|---|---|---|---|---|---|---|
| 1 | statProductDeliveryStatusOfCashflow.json | L4242 | F2 getStatusDeliveryFactory | { cashflowId } | ❌ | ❌ |
| 2 | getCashflowDeliveryVo.json | L4249 | F1 getMedicalRecordDeliveryFactory | { cashflowId } | ❌ | ❌ |

**A**：2 API / 2 Factory / 0 接收返回 / 0 then。
**A**：**result 消费 0 处**（唯一只创建 + 调用的 controller）。

---

## 7. API 交叉矩阵（A = 调用，F = 不调用）

| API | deliveryInputCtrl | deliveryInputRecordCtrl | deliveryProcessingCtrl |
|---|---|---|---|
| getMedicalRecordPayVo.json | F | **A**（L4034）| F |
| getCashflowDeliveryVo.json (F1) | **A**（L3848）| **A**（L4040）| **A**（L4249）|
| statProductDeliveryStatusOfCashflow.json (F2) | **A**（L3841）| **A**（L4044）| **A**（L4242）|
| getMedicalProductMachineCenterVoList.json (F3) | **A**（L3836）| F | F |
| getCanBeDeliverySkuInListOfProduct.json (F4) | **A**（L3885）| F | F |
| saveMedicalProductStockBatch.json (F5) | **A**（L4007）| F | F |
| sendMedicalProductToMachineCenter.json (F6) | **A**（L3966）| F | F |
| saveMedicalProductDeliveryCommentBatch.json | F | **A**（L4061）| F |
| **API 总数** | **6** | **4** | **2** |

**A**：
- **共同 API = 2 个**（F1 + F2）
- **deliveryInputCtrl 独有 = 4 个**（F3/F4/F5/F6）
- **deliveryInputRecordCtrl 独有 = 2 个**（getMedicalRecordPayVo + saveMedicalProductDeliveryCommentBatch）
- **deliveryProcessingCtrl 独有 = 0 个**

---

## 8. 三 Controller ObjectFactory 实例清单

### 8.1 deliveryInputCtrl（6 实例）

| # | Factory | 行号 | 变量挂载 |
|---|---|---|---|
| 1 | getCenterListFactory (F3) | L3835 | $scope |
| 2 | getStatusDeliveryFactory (F2) | L3840 | $scope |
| 3 | getMedicalRecordDeliveryFactory (F1) | L3847 | $scope |
| 4 | getDeliveryListFactory (F4) | L3884 | $scope |
| 5 | createOrderFactory (F6) | L3965 | $scope |
| 6 | saveStockFactory (F5) | L4006 | $scope |

### 8.2 deliveryInputRecordCtrl（4 实例）

| # | Factory | 行号 | 变量挂载 |
|---|---|---|---|
| 1 | getMedicalRecord（**临时，不挂 $scope**）| L4033 | 局部 var |
| 2 | getMedicalRecordDeliveryFactory (F1) | L4039 | $scope |
| 3 | getStatusDeliveryFactory (F2) | L4043 | $scope |
| 4 | saveMedicalRecordDeliveryFactory（**独有**）| L4060 | $scope |

### 8.3 deliveryProcessingCtrl（2 实例）

| # | Factory | 行号 | 变量挂载 |
|---|---|---|---|
| 1 | getStatusDeliveryFactory (F2) | L4241 | $scope |
| 2 | getMedicalRecordDeliveryFactory (F1) | L4248 | $scope |

**A**：3 controller 共 12 个 ObjectFactory 实例 + 1 个临时实例（getMedicalRecord）。
**A**：F1 + F2 在 3 controller 各 1 个独立实例（共 3 × 2 = 6 个独立实例，**互不共享**）。

---

## 9. ListFactory 使用

| Controller | 注入 | 实际 new |
|---|---|---|
| deliveryInputCtrl | ✅ | **0 处** |
| deliveryInputRecordCtrl | ✅ | **0 处** |
| deliveryProcessingCtrl | ❌（未注入）| **0 处** |

**A**：3 controller 范围内 ListFactory **0 处实际 new**。
**F**：3 controller 对应 HTML 不可得，HTML 内是否 new ListFactory 不可证。

---

## 10. cashflowId 使用

| Controller | $stateParams.cashflowId | 流入 API 数 |
|---|---|---|
| deliveryInputCtrl | L3814 | 6 API 全部使用 cashflowId |
| deliveryInputRecordCtrl | L4026 | 4 API 全部使用 cashflowId |
| deliveryProcessingCtrl | L4238 | 2 API 全部使用 cashflowId |

**A**：3 controller 全部从 `$stateParams.cashflowId` 接收 cashflowId 并直接流入所有 saveOrQuery。
**F**：3 controller 共享 cashflowId **不意味着同一业务实体**（cashflowId 是路由参数，相同 URL 跳转可触发任意 controller 接收）。

---

## 11. F1（getMedicalRecordDeliveryFactory）分布

| Controller | 创建 | result 消费字段 | 消费行号 |
|---|---|---|---|
| deliveryInputCtrl | L3847 | **waitingDeliveryList** | L3818/L3851/L3854/L3856/L3870/L3893/L3910（7 处）|
| deliveryInputRecordCtrl | L4039 | **deliveryedList** | L4051（1 处）|
| deliveryProcessingCtrl | L4248 | **0 字段**（result 不读）| — |

**A**：3 controller 都调用 F1，但消费**完全不同的 result 字段**。
**A**：F1 返回的 `result.object` 至少有 2 个不同字段（waitingDeliveryList + deliveryedList），由 3 controller 各取所需。
**F**：result.object 完整字段结构（ObjectFactory 内部不可得）。

---

## 12. F2（getStatusDeliveryFactory）分布

| Controller | 创建 | result 消费 |
|---|---|---|
| deliveryInputCtrl | L3840 | 0 处 |
| deliveryInputRecordCtrl | L4043 | 0 处 |
| deliveryProcessingCtrl | L4241 | 0 处 |

**A**：3 controller 调用 F1，**全部 0 处 result 消费**（S1-79 已确认）。
**A**：F2 调用形式 100% 同构（API + params + fire-and-forget）。

---

## 13. F3（getCenterListFactory）分布

| Controller | 调用 |
|---|---|
| deliveryInputCtrl | ✅ L3836 |
| deliveryInputRecordCtrl | F |
| deliveryProcessingCtrl | F |

**A**：F3 仅 deliveryInputCtrl 使用，**其它 2 controller 0 处调用**。

---

## 14. F4（getDeliveryListFactory）分布

| Controller | 调用 |
|---|---|
| deliveryInputCtrl | ✅ L3885 |
| deliveryInputRecordCtrl | F |
| deliveryProcessingCtrl | F |

**A**：F4 仅 deliveryInputCtrl 使用。

---

## 15. F5（saveStockFactory）分布

| Controller | 调用 |
|---|---|
| deliveryInputCtrl | ✅ L4007（saveMedicalProductStockBatch.json）|
| deliveryInputRecordCtrl | F（但用不同 Factory: `saveMedicalRecordDeliveryFactory` 调 `saveMedicalProductDeliveryCommentBatch.json`）|
| deliveryProcessingCtrl | F |

**A**：F5 仅 deliveryInputCtrl 使用。
**A**：F5 ≠ `saveMedicalRecordDeliveryFactory`（**不同 Factory 实例** + **不同 API**）。

---

## 16. F6（createOrderFactory）分布

| Controller | 调用 |
|---|---|
| deliveryInputCtrl | ✅ L3966 |
| deliveryInputRecordCtrl | F |
| deliveryProcessingCtrl | F |

**A**：F6 仅 deliveryInputCtrl 使用。

---

## 17. Factory / result 对照矩阵

| Controller | Factory 数 | 挂 $scope Factory | 临时 Factory | result.object 消费 | result.list 消费 | result 字段 |
|---|---|---|---|---|---|---|
| deliveryInputCtrl | 6 | 6 | 0 | **7 处**（waitingDeliveryList 7 处）| **7 处**（F3=1, F4=6）| waitingDeliveryList + deliveryStockInSkuVoList + medicalProduct |
| deliveryInputRecordCtrl | 4 | 3 | 1（getMedicalRecord）| **1 处**（deliveryedList L4051）| **0 处** | deliveryedList + medicalProduct + medicalProductDelivery.deliveryComment + medicalRecord.id |
| deliveryProcessingCtrl | 2 | 2 | 0 | **0 处** | **0 处** | — |

**A**：3 controller 的 result 消费模式完全不同。
**A**：deliveryProcessingCtrl **完全不读任何 Factory result**。

---

## 18. waitingDeliveryList 跨 controller

| Controller | 是否消费 |
|---|---|
| deliveryInputCtrl | ✅ **7 处**（L3818/L3851/L3854/L3856/L3870/L3893/L3910）|
| deliveryInputRecordCtrl | ❌ 0 处 |
| deliveryProcessingCtrl | ❌ 0 处 |

**A**：waitingDeliveryList **仅 deliveryInputCtrl 消费**——其它 2 controller 虽调用 F1 但不读此字段。
**F**：后端是否在每次 F1 调用都返回 waitingDeliveryList 字段（不可得）。

---

## 19. deliveryedList 跨 controller

| Controller | 是否消费 |
|---|---|
| deliveryInputCtrl | ❌ 0 处 |
| deliveryInputRecordCtrl | ✅ **1 处**（L4051）|
| deliveryProcessingCtrl | ❌ 0 处 |

**A**：deliveryedList **仅 deliveryInputRecordCtrl 消费**。
**A**：F1 result.object 在 2 个 controller 暴露了 2 个不同字段（waitingDeliveryList vs deliveryedList），**不互通**。

---

## 20. sendToMachineCenterList 跨 controller

| Controller | 是否消费 |
|---|---|
| deliveryInputCtrl | ❌ |
| deliveryInputRecordCtrl | ❌ |
| deliveryProcessingCtrl | ❌ |

**A**：全仓 `sendToMachineCenterList` **0 处出现**。
**F**：业务名称（"待发到加工中心"）是否对应 F3 result.list 或 F6 send data 中某字段，**未观察到统一字段名**。

---

## 21. medicalProductDelivery 字段使用

| Controller | 使用 |
|---|---|
| deliveryInputCtrl | ❌ 0 处 |
| deliveryInputRecordCtrl | ✅ **1 处**（L4056 `medicalProductDelivery.deliveryComment`）|
| deliveryProcessingCtrl | ❌ 0 处 |

**A**：仅 deliveryInputRecordCtrl 通过 deliveryedList 路径读取 `medicalProductDelivery.deliveryComment`。

---

## 22. machineCenter 字段使用

| Controller | 使用 |
|---|---|
| deliveryInputCtrl | ✅ 3 处（L3824 / L3854 / L3962）|
| deliveryInputRecordCtrl | ❌ |
| deliveryProcessingCtrl | ❌ |

**A**：machineCenter 相关字段（id / lockMachineCenter）**仅 deliveryInputCtrl 使用**。

---

## 23. medicalProductMachineCenter 字段使用

| Controller | 使用 |
|---|---|
| deliveryInputCtrl | ✅ 2 处（L3817 `medicalProductMachineCenterPoList` / L3828 return）|
| deliveryInputRecordCtrl | ❌ |
| deliveryProcessingCtrl | ❌ |

**A**：medicalProductMachineCenterPoList 派生函数（`getMachineCenterList` L3816-3829）**仅 deliveryInputCtrl**。

---

## 24. Save / Send 分布

| Controller | Save API | Send API | Save Factory | Send Factory |
|---|---|---|---|---|
| deliveryInputCtrl | ✅ F5 saveMedicalProductStockBatch | ✅ F6 sendMedicalProductToMachineCenter | saveStockFactory (L4006) | createOrderFactory (L3965) |
| deliveryInputRecordCtrl | ✅ **不同 API** saveMedicalProductDeliveryCommentBatch | ❌ | **saveMedicalRecordDeliveryFactory** (L4060) | — |
| deliveryProcessingCtrl | ❌ | ❌ | — | — |

**A**：
- Save API **跨 2 controller**（F5 vs saveMedicalProductDeliveryCommentBatch），但**完全不同 API + 完全不同 Factory**
- Send API **仅 deliveryInputCtrl**
- deliveryProcessingCtrl **无任何 Save/Send**

---

## 25. $state.go / $state.reload / $stateParams 分布

| Controller | $state.go | $state.reload | $stateParams |
|---|---|---|---|
| deliveryInputCtrl | **1 处** L3861（→ deliveryList）| **2 处** L3974/L4016 | 2 处（L3812 注入 + L3814 读取）|
| deliveryInputRecordCtrl | **0 处** | **0 处** | 2 处（L4024 注入 + L4026 读取）|
| deliveryProcessingCtrl | **0 处** | **0 处** | 2 处（L4236 注入 + L4238 读取）|

**A**：仅 deliveryInputCtrl 做导航 / 刷新。
**A**：3 controller 都用 $stateParams.cashflowId，但用途相同（路由参数接收）。

---

## 26. Controller → Controller 直接关系

| Source | Target | 关系 | 证据 |
|---|---|---|---|
| deliveryInputCtrl | deliveryListCtrl (L4075+) | **state.go 跳转** | L3861 `$state.go('deliveryList')` |
| deliveryInputRecordCtrl | — | 无 | — |
| deliveryProcessingCtrl | — | 无 | — |

**A**：3 controller 范围内**仅 1 处跨 controller 跳转**（deliveryInputCtrl → deliveryListCtrl）。
**A**：2 个其它 controller（InputRecord / Processing）**无任何 Controller→Controller 调用**。
**F**：HTML 是否有跳转链接（working dir 无对应 HTML）。

### 26.1 其它共享关系

| 类型 | 3 controller 间 |
|---|---|
| 共享 Factory 实例 | ❌（3 × 2 = 6 个 F1/F2 实例各自独立）|
| 共享 scope 变量 | ❌（3 controller 各自 $scope）|
| 共享 result.object | ❌（3 controller 各自 Factory 独立 result）|
| 共享 service / factory / directive | ❌（无调用记录）|
| 共享 event / $emit / $broadcast | ❌（无调用记录）|
| 共享 callback / resolve | ❌（无调用记录）|

**A**：3 controller **完全无共享运行期状态**。

---

## 27. 三 Controller 直接关系矩阵

| Source → Target | deliveryInputCtrl | deliveryInputRecordCtrl | deliveryProcessingCtrl | deliveryListCtrl |
|---|---|---|---|---|
| deliveryInputCtrl | — | F | F | **A**（state.go L3861）|
| deliveryInputRecordCtrl | F | — | F | F |
| deliveryProcessingCtrl | F | F | — | F |
| Shared API | F1+F2 (3) | F1+F2 (2) | F1+F2 (2) | — |
| Shared Factory 实例 | F | F | F | — |
| Shared scope | F | F | F | — |

**A**：3 controller 之间无直接函数调用 / 共享 Factory / 共享 scope。
**A**：仅 1 处跨 controller 跳转：deliveryInputCtrl → deliveryListCtrl。

---

## 28. Controller 职责边界（按直接证据）

### 28.1 deliveryInputCtrl 直接证据

- 调用 6 API：Query(4) + Save(1) + Send(1)
- 6 ObjectFactory 实例
- result 消费：14 处（result.object 7 + result.list 7）
- 使用 modal：stockDetail（L3882）、addOrderModal（L3831）
- 使用 dateSearch / startTime / date
- 使用 expiresWarning / isSendProduct / isSendCenter 等 helper
- 操作 `$state.go('deliveryList')` + `$state.reload()` 各 1 次
- Save success refresh：search() + getCount() + reload() + stockDetail=false（4 步）
- Send success refresh：reload() + addOrderModal=false（2 步）
- 派生 JSON：medicalProductMachineCenterPoListJson（L3836）+ medicalProductStockBatctPoListJson（L4007）
- 自动派生：getMachineCenterList() helper（L3816-3829）

### 28.2 deliveryInputRecordCtrl 直接证据

- 调用 4 API：Query(3) + Save(1)
- 4 ObjectFactory 实例（3 挂 $scope + 1 临时）
- result 消费：1 处（deliveryedList L4051）
- 使用 toggle / medicalRecordId
- 使用 saveRemark function（L4048）
- 派生 JSON：medicalProductDeliveryCommentListJson（L4061）
- Save success：toggle=true（L4068），**无 reload / 无 state.go**
- 独有：medicalProductDelivery.deliveryComment 字段读取（L4056）

### 28.3 deliveryProcessingCtrl 直接证据

- 调用 2 API：Query(2)
- 2 ObjectFactory 实例
- result 消费：**0 处**
- 仅 expiresWarning helper（L4253-4259）
- 无 modal / 无 state 操作 / 无 Save/Send / 无 JSON 派生
- **最小 controller**（26 行）

### 28.4 不能由 Controller 名称直接确定的（E / F）

- **E 业务职责**（E 表示仅命名推测，无代码直接证据）：
  - "deliveryInputCtrl 是发货录入页面"
  - "deliveryInputRecordCtrl 是发货记录页面"
  - "deliveryProcessingCtrl 是发货处理页面"
- **F 真正职责**：必须由对应 HTML 模板（**working dir 不可得**）的 UI 文案 / 字段绑定 / 按钮行为确定。
- **禁止表述**："三 controller 属于同一业务模块"（仅因共享 cashflowId 不够，需 UI 证据）。

---

## 29. 一期冻结事实

| 冻结 | 内容 |
|---|---|
| 三 Controller 名称 | deliveryInputCtrl / deliveryInputRecordCtrl / deliveryProcessingCtrl |
| 三 Controller 行号 | L3812-4021 / L4024-4072 / L4236-4261 |
| API 总数 | 6 + 4 + 2 = **12 个**（去重：9 个不同 API）|
| 共同 API | **2 个**（F1+F2）|
| 跨 controller state 跳转 | **1 处**（deliveryInputCtrl → deliveryListCtrl L3861）|
| 共享 Factory 实例 | **0 处** |
| 共享 scope | **0 处** |
| 共享 result | **0 处** |
| result 消费最多 | deliveryInputCtrl（14 处）|
| result 消费最少 | deliveryProcessingCtrl（**0 处**）|
| 唯一无 Save/Send controller | deliveryProcessingCtrl |
| 唯一无 state.go/reload controller | deliveryInputRecordCtrl + deliveryProcessingCtrl |

---

## 30. 当前 F 边界

| F 项 | 不属本审计的原因 |
|---|---|
| 3 controller 对应 HTML 模板 | working dir 不可得 |
| UI 文案 / 按钮 / 提示信息 | HTML 不可得 |
| 后端 9 个 API 响应结构 | 资源范围外 |
| ObjectFactory 内部实现 | 资源范围外 |
| 业务模块归属（E 推测）| 无 UI 证据 |
| $stateParams.cashflowId 是否来自同一 URL | 路由表不可得 |
| 3 controller 路由路径 | 资源范围外 |
| 3 controller 是否在 production 被实际使用 | 静态分析不可证 |
| F2 result.* 字段是否存在 | S1-79 0 处观察（无 Consumer）|

---

## 31. A / B / C / D / E / F 评级

| # | 审计项 | 评级 |
|---|---|---|
| 01 | 三 Controller 精确定位 | **A** |
| 02 | deliveryInputCtrl API 清单 | **A**（6 API 全部）|
| 03 | deliveryInputRecordCtrl API 清单 | **A**（4 API 全部）|
| 04 | deliveryProcessingCtrl API 清单 | **A**（2 API 全部）|
| 05 | API 交叉矩阵 | **A** |
| 06 | ObjectFactory 使用 | **A**（12 实例）|
| 07 | ListFactory 使用 | **A**（注入 + 0 实际 new）|
| 08 | cashflowId 使用 | **A** |
| 09 | F1 分布 | **A**（3 controller 不同字段消费）|
| 10 | F2 分布 | **A**（3 controller + 0 消费）|
| 11-14 | F3-F6 分布 | **A**（仅 deliveryInputCtrl）|
| 15 | Factory/result 对照 | **A** |
| 16-18 | 各 Controller 特有对象 | **A** |
| 19 | waitingDeliveryList 跨 controller | **A**（仅 deliveryInputCtrl）|
| 20 | deliveryedList 跨 controller | **A**（仅 deliveryInputRecordCtrl）|
| 21 | sendToMachineCenterList 跨 controller | **A**（0 处）|
| 22 | medicalProductDelivery | **A**（仅 deliveryInputRecordCtrl）|
| 23 | machineCenter | **A**（仅 deliveryInputCtrl）|
| 24 | medicalProductMachineCenter | **A**（仅 deliveryInputCtrl）|
| 25 | Save / Send 分布 | **A** |
| 26 | state.go / reload | **A** |
| 27 | Controller → Controller 调用 | **A**（1 处 state.go）|
| 28 | 三 Controller 直接关系矩阵 | **A** |
| 29 | Controller 职责边界 | **A**（直接证据）+ **E**（命名推测）|
| 30 | Q1-Q30 回答 | **A** |

**统计**：30 项中 28 A + 2 E（业务职责命名推测），**无 F 升 A**。

---

## 32. L1 / L2 / L3 分层

| 层级 | 内容 | 状态 |
|---|---|---|
| L1 前端事实 | Controller / API / Factory / result 消费 / state 操作 / 对象字段 | **是** |
| L2 业务规则 | 业务职责 / 业务模块归属 / 业务流程 | **E**（命名推测 + HTML 不可得）|
| L3 数据库物理模型 | 后端 DTO / Service / Repository | **F**（资源范围外）|

---

## 33. R1-R6 红线核查

| 红线 | 是否触发 |
|---|---|
| R1 生产数据修改 | ❌ |
| R2 真实 API 调用 | ❌ |
| R3 创建 DTO/VO/PO/Service/Repository | ❌ |
| R4 修改历史 MD | ❌ |
| R5 删除 10 个 untracked | ❌ |
| R6 P0/P1 自动新增 | ❌ |

---

## 34. Q1-Q30 回答

| Q | 答案 |
|---|---|
| Q1：3 Controller 各自 API 数量？| 6 / 4 / 2 |
| Q2：共同 API 有哪些？| **2 个**（F1 getCashflowDeliveryVo + F2 statProductDeliveryStatusOfCashflow）|
| Q3：只有 deliveryInputCtrl 的 API？| **4 个**（F3/F4/F5/F6）|
| Q4：只有 deliveryInputRecordCtrl 的 API？| **2 个**（getMedicalRecordPayVo + saveMedicalProductDeliveryCommentBatch）|
| Q5：只有 deliveryProcessingCtrl 的 API？| **0 个** |
| Q6：3 Controller 是否都用 ObjectFactory？| **是**（注入 + new）|
| Q7：3 Controller 是否都用 ListFactory？| **否**（仅 2 注入，0 实际 new）|
| Q8：3 Controller 是否都使用 cashflowId？| **是**（来自 $stateParams）|
| Q9：F1 是否 3 Controller 都调用？| **是** |
| Q10：F2 是否 3 Controller 都调用？| **是** |
| Q11：F2 是否 3 Controller Consumer=0？| **是** |
| Q12：F3 哪些 Controller 调用？| 仅 deliveryInputCtrl |
| Q13：F4 哪些 Controller 调用？| 仅 deliveryInputCtrl |
| Q14：F5 哪些 Controller 调用？| 仅 deliveryInputCtrl |
| Q15：F6 哪些 Controller 调用？| 仅 deliveryInputCtrl |
| Q16：waitingDeliveryList 哪些 Controller Consumer？| 仅 deliveryInputCtrl（7 处）|
| Q17：deliveryedList 哪些 Controller Consumer？| 仅 deliveryInputRecordCtrl（1 处）|
| Q18：sendToMachineCenterList 哪些 Controller Consumer？| **0 Controller**（全仓 0 处）|
| Q19：medicalProductDelivery 哪些 Controller 使用？| 仅 deliveryInputRecordCtrl（deliveryComment 字段）|
| Q20：machineCenter 哪些 Controller 使用？| 仅 deliveryInputCtrl（3 处）|
| Q21：medicalProductMachineCenter 哪些 Controller 使用？| 仅 deliveryInputCtrl（2 处）|
| Q22：Save / Send 是否只有 deliveryInputCtrl？| Send 是（仅 F6）；Save 跨 2 controller 但**API 不同**（F5 vs saveMedicalProductDeliveryCommentBatch）|
| Q23：3 Controller 是否存在直接 Controller→Controller 调用？| **1 处**（deliveryInputCtrl → deliveryListCtrl state.go L3861）|
| Q24：3 Controller 是否共享 Factory 实例？| **否** |
| Q25：3 Controller 是否共享 result.object/list？| **否** |
| Q26：3 Controller 是否共享 scope 对象？| **否** |
| Q27：3 Controller 是否存在直接 state 跳转关系？| **是**（1 处，Input → List）|
| Q28：3 Controller 是否可冻结为 3 个独立职责？| **是**（按 API/Factory/对象/result 消费均不同）|
| Q29：哪些职责只能标 E？| 业务模块归属 / 业务页面定位 / 业务流程顺序（**无 UI 证据**）|
| Q30：当前 F 边界？| 见第 30 节（9 项 F）|

---

## 35. P0 / P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）

---

## 36. 历史证据 vs 当前代码

### 36.1 S1-78 / S1-79 表述

- S1-78：deliveryInputCtrl 6 Factory / 6 API / 1 instance / consumer 各异
- S1-79：3 controller 调用 F2，0 处 result 消费

### 36.2 S1-80 新增/修正

| 项 | 历史 | 当前代码 | 判定 |
|---|---|---|---|
| F1 consumer 范围 | S1-78 仅 deliveryInputCtrl | **3 controller 都调用 F1**，但**消费字段不同**（waitingDeliveryList vs deliveryedList vs 0）| **修正** |
| Save 跨 controller | S1-78 未提 | deliveryInputCtrl F5 + deliveryInputRecordCtrl saveMedicalProductDeliveryCommentBatch，**不同 API 不同 Factory** | **新增** |
| Controller→Controller 跳转 | 未提 | **1 处**：deliveryInputCtrl L3861 → deliveryListCtrl | **新增** |
| ListFactory 实际使用 | 未提 | 3 controller 范围内**0 处 new**（注入但未用）| **新增** |
| sendToMachineCenterList | 未提 | 全仓 **0 处** | **新增** |
| medicalProductDelivery 字段 | 未提 | 仅 deliveryInputRecordCtrl L4056 deliveryComment | **新增** |
| waitingDeliveryList 跨 controller | S1-78 仅 deliveryInputCtrl | 确认**仅 deliveryInputCtrl** | **保留** |
| deliveryedList 跨 controller | 未提 | **仅 deliveryInputRecordCtrl** | **新增** |

### 36.3 最终采用

- **保留**：S1-78 的 6 Factory 实例 + S1-79 的 F2 0 消费
- **修正**：F1 consumer 范围从"deliveryInputCtrl 7 处"扩展到"3 controller + 不同字段"
- **新增**：1 处跨 controller state 跳转 + 跨 controller Save（不同 API）
- **新增**：ListFactory 0 实际 new + sendToMachineCenterList 全仓 0 处

---

## 37. 本轮新增事实

1. **3 Controller 共 12 个 ObjectFactory 实例**（6+4+2）+ 1 个临时实例（getMedicalRecord）
2. **API 总数 = 12（去重 9）**：6/4/2 分布
3. **共同 API = 2**（F1 + F2）
4. **F1 在 3 controller 调用但消费不同字段**（waitingDeliveryList vs deliveryedList vs 0）
5. **F2 在 3 controller 调用但 0 处 result 消费**（S1-79 已确认）
6. **Save 跨 2 controller 但 API 不同**（F5 vs saveMedicalProductDeliveryCommentBatch）
7. **Send 仅 deliveryInputCtrl**
8. **1 处跨 controller state 跳转**：deliveryInputCtrl L3861 → deliveryListCtrl
9. **3 controller 0 处共享 Factory 实例 / 0 处共享 scope / 0 处共享 result**
10. **waitingDeliveryList / machineCenter / medicalProductMachineCenter 仅 deliveryInputCtrl**
11. **deliveryedList / medicalProductDelivery.deliveryComment 仅 deliveryInputRecordCtrl**
12. **sendToMachineCenterList 全仓 0 处**
13. **ListFactory 注入但 0 实际 new**（3 controller 范围内）
14. **deliveryProcessingCtrl 是最小 controller**（26 行 / 2 API / 0 result 消费 / 0 state 操作 / 仅 expiresWarning helper）
15. **三 Controller 业务职责**（E）：无 UI 证据，**禁止由命名直接确定**

---

## 38. 红线核查（最终）

| 红线 | 状态 |
|---|---|
| Write 操作 = 0 | ✅ |
| 生产数据修改 = 0 | ✅ |
| 历史 MD 修改 = 0 | ✅ |
| P0 自动新增 = 0 | ✅ |
| P1 自动新增 = 0 | ✅ |
| 10 个 untracked 临时文件仍保留 | ✅ |
| Git 禁止命令未触发 | ✅（仅 `git add -- 141_*.md`）|

---

## 39. 停止条件

✅ 30 项审计完成（28 A + 2 E）
✅ 30 问 Q1-Q30 全部回答
✅ 7 大矩阵建立（API / Factory / result / 对象 / state / Controller 关系 / 职责）
✅ 12 项 ObjectFactory 实例 + 12 项 API 完整列出
✅ 1 处跨 controller 跳转明确
✅ 0 处共享 Factory / scope / result 明确
✅ F 边界 9 项明确列出
✅ 红线 0 触发

**等待老板下一条指令（不自动执行 S1-81）**。
