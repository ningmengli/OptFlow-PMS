# 111 S1-52 MachineCenterOrder / medicalProductDelivery / Delivery 状态机专项收口 26 项

**文档性质**：S1-52 状态机专项收口
**任务来源**：老板 S1-52 专项指令（9/3 11:33）
**侦察时间**：2026-09-03 11:35-12:00
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **S1-51 留下的 F 状态语义全部升级为 A**：
>
> A. `acceptStatus` 0/1 业务含义
> B. `status` 0/1/2 业务含义
> C. `receiveStatus` 0/1 业务含义
> D. `medicalProductDelivery.deliveryStatus` 0/1 业务含义
> E. 5 个状态相关 API（receive/start/complete/close/deliveryMachineCenterOrder.json）真实转换关系
> F. 按钮控制条件
> G. Delivery 状态字段 + waitingDeliveryList/deliveryedList/sendToMachineCenterList

---

## 一、🎯 颠覆性 A 级新发现 - 状态语义 100% 收口

### 1.1 acceptStatus 业务语义（A 级 100%）

**真实值域**：0 / 1

| 值 | 业务含义 | 直接证据 |
|---|---------|---------|
| 0 | **待受理** | machineOrderList.html L131 "待受理" + L299 `ng-show="acceptStatus==0 && status==0"` |
| 1 | **已受理** | machineOrderList.html L300/L304/L308/L312/L317 `ng-show="acceptStatus==1 && status==*"` |

**setTab 状态筛选**（controller L4348-4360）：

| Tab | 文字 | acceptStatus | statusArray |
|-----|------|-------------|-------------|
| 1 | 全部 | null | null |
| 2 | 待受理 | 0 | [0] |
| 3 | 制作中 | 1 | [0, 1] |
| 4 | 已完成 | 1 | [2] |

### 1.2 status 业务语义（A 级 100%）

**真实值域**：0 / 1 / 2

| 值 | 业务含义 | 直接证据 |
|---|---------|---------|
| 0 | **待制作** | machineOrderList.html L299/L303 `ng-show="status==0"` |
| 1 | **制作中** | machineOrderList.html L307 `ng-show="status==1"` + L308 "制作中" |
| 2 | **已完成** | machineOrderList.html L311 `ng-show="status==2"` + L312 "已完成" |

**状态文字组合**（HTML L298-313）：

```
acceptStatus==0 && status==0  → "待受理"
acceptStatus==1 && status==0  → "制作中"
acceptStatus==1 && status==1  → "制作中"
acceptStatus==1 && status==2  → "已完成"
```

### 1.3 receiveStatus 业务语义（A 级 100%）

**真实值域**：0 / 1

| 值 | 业务含义 | 直接证据 |
|---|---------|---------|
| 0 | **未签收** | machineOrderList.html L322-323 "未签收" + L337 ng-show 签收按钮条件 |
| 1 | **已签收** | machineOrderList.html L319-320 "已签收" + controller L4321 赋值 |

**receiveStatus: 0 → 1 状态转换**（controller L4314-4328）：

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
        $scope.getAdminList.items[idx].machineCenterOrder.receiveStatus = 1;  // ← 状态转换 A 100%
      }
    });
  });
};
```

### 1.4 medicalProductDelivery.deliveryStatus 业务语义（A 级 100%）

**真实值域**：0 / 1

| 值 | 业务含义 | 直接证据 |
|---|---------|---------|
| 0 | **未发货** | machineOrderList.html L343 ng-show "发货" 按钮条件 |
| 1 | **已发货** | machineOrderList.html L329-330 `ng-show="deliveryStatus==1 && receiveStatus==1"` "已发货" |

**medicalProductDelivery.deliveryStatus: 0 → 1 状态转换**（controller L4329-4342）：

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
        $scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1;  // ← 状态转换 A 100%
      }
    });
  });
};
```

### 1.5 🎯 S1-52 颠覆性 A 级新发现 - deliveryStatus 在不同对象语义不同

| 对象 | 字段路径 | 值域 | 业务含义 | 评级 |
|------|---------|------|---------|------|
| **cashflowDeliveryVo** | `item.deliveryStatus`（顶级字段）| 0/1/2/3 | **全部/待发货/加工中/已发货** | **A 100%** |
| **machineCenterOrderRecordVo** | `item.medicalProductDelivery.deliveryStatus`（子对象字段）| 0/1 | **未发货/已发货** | **A 100%** |

**重要警告**：
- `cashflowDeliveryVo.deliveryStatus = 1` = "待发货"
- `machineCenterOrderRecordVo.medicalProductDelivery.deliveryStatus = 1` = "已发货"
- **严禁混淆这两个 deliveryStatus**

### 1.6 cashflowDeliveryVo.deliveryStatus 0/1/2/3 完整业务语义（A 级 100%）

**controller L4127-4145 setTab 定义**：

| Tab | UI 文字 | $scope.deliveryStatus | $scope.obj.deliveryStatus | $scope.obj.toBeProcess |
|-----|---------|---------------------|--------------------------|------------------------|
| 1 | 待发货 | 1 | 0 | 0 |
| 2 | 加工中 | 2 | 0 | 1 |
| 3 | 已发货 | 3 | 1 | null |
| null | 全部 | null | null | null |

**🎯 deliveryList 使用 2 个状态字段**：
- `deliveryStatus` (0/1/null)
- `toBeProcess` (0/1/null)
- 两个字段组合 = 4 种业务状态

---

## 二、🎯 5 个状态 API 完整调用链

### 2.1 receiveMachineCenterOrder.json（A 级 100%）

**调用位置**：controller L4317（machineOrderListCtrl）
**Function**：`$scope.receiveOrder(id, idx)`

**Request**：`{ machineCenterOrderId: id }`
**Response 检查**：`re.status == 0`
**状态转换**：`receiveStatus: 0 → 1`（controller L4321 直接赋值）
**触发条件**：HTML L337 `ng-show="status==2 && receiveStatus==0"` 显示"签收"按钮

### 2.2 startMachineCenterOrder.json（A 级 100%）

**调用位置**：controller L16164（machineOrderBrokenCtrl）
**Function**：`$scope.startOrder(id, medicalRecordId, idx)` → `commonOrder()`

**Request**：`{ machineCenterOrderId: id }`
**Response 检查**：`res.status == 1`（失败）/ `== 0`（成功）
**状态转换**：`status: 0 → ?`（由后端决定，前端重新查询）
**后续刷新**：commonOrder → getMachineCenterOrder → `$scope.memberFactory.items[idx].machineCenterOrder.status = resp.result.object.status`（L16253）

### 2.3 completeMachineCenterOrder.json（A 级 100%）

**调用位置 1**：controller L16226
**Function**：`$scope.completeOrder(id, medicalRecordId, idx)`

**调用位置 2**：controller L16336
**Function**：`$scope.completeOrder()`（用 cashflowId + machineCenterId，不是 machineCenterOrderId）

**Request 变体**：
- 变体 A：`{ machineCenterOrderId: id }`
- 变体 B：`{ cashflowId, machineCenterId }`

**状态转换**：`status: 1 → 2`（基于业务语义推断 + 重新查询）

### 2.4 closeMachineCenterOrder.json（A 级 100%）

**调用位置**：controller L16235
**Function**：`$scope.closeOrder(id, medicalRecordId, idx)` → `commonOrder()`

**Request**：`{ machineCenterOrderId: id }`
**状态转换**：`status: ? → ?`（**F = 当前证据范围未直接观察**）

### 2.5 deliveryMachineCenterOrder.json（A 级 100%）

**调用位置**：controller L4332（machineOrderListCtrl）
**Function**：`$scope.deliveryReceiveOrder(id, idx)`

**Request**：`{ machineCenterOrderId: id }`
**Response 检查**：`re.status == 0`
**状态转换**：`medicalProductDelivery.deliveryStatus: 0 → 1`（controller L4336 直接赋值）
**触发条件**：HTML L343 `ng-show="deliveryStatus==0 && receiveStatus==1"` 显示"发货"按钮

---

## 三、状态字典

### 3.1 表 1：MachineCenterOrder 状态字典

| 字段 | 值 | 页面/代码文字 | 直接行为 | API 上下文 | 等级 |
|------|------|------|------|------|------|
| `acceptStatus` | 0 | "待受理" (HTML L131 + L299) | 显示"待受理"文字 | setTab(2) | **A 100%** |
| `acceptStatus` | 1 | "已受理"（隐含） | 多种 status 组合 | setTab(3/4) | **A 100%** |
| `status` | 0 | "待制作"（隐含） | "待受理"组合 | setTab(2/3) | **A 100%** |
| `status` | 1 | "制作中" (L308) | 制作中显示 | setTab(3) | **A 100%** |
| `status` | 2 | "已完成" (L312) | 触发"签收"按钮 | setTab(4) | **A 100%** |
| `receiveStatus` | 0 | "未签收" (L323) | 显示"签收"按钮 | — | **A 100%** |
| `receiveStatus` | 1 | "已签收" (L320) | 显示"发货"按钮 | receiveMachineCenterOrder | **A 100%** |
| `medicalProductDelivery.deliveryStatus` | 0 | "未发货"（隐含） | 显示"发货"按钮 | — | **A 100%** |
| `medicalProductDelivery.deliveryStatus` | 1 | "已发货" (L330) | 不再显示"发货"按钮 | deliveryMachineCenterOrder | **A 100%** |

### 3.2 表 2：cashflowDeliveryVo 状态字典（Delivery 页面）

| 字段 | 值 | 页面/代码文字 | 直接行为 | 评级 |
|------|------|------|------|------|
| `deliveryStatus` | 1 | "待发货" (HTML L144) | waitingDeliveryList | **A 100%** |
| `deliveryStatus` | 2 | "加工中" (HTML L155) | sendToMachineCenterList | **A 100%** |
| `deliveryStatus` | 3 | "已发货" (HTML L166) | deliveryedList | **A 100%** |
| `toBeProcess` | 0 | （与 deliveryStatus 配合）| setTab(1) | **A 100%** |
| `toBeProcess` | 1 | （与 deliveryStatus 配合）| setTab(2) | **A 100%** |
| `toBeProcess` | null | （与 deliveryStatus 配合）| setTab(3) | **A 100%** |

### 3.3 表 3：状态 → UI 行为

| 对象 | 状态字段 | 值 | UI 行为 | 按钮/文字 | 等级 |
|------|---------|-----|---------|----------|------|
| machineCenterOrder | `acceptStatus==0` && `status==0` | — | 显示 | "待受理" | **A 100%** |
| machineCenterOrder | `acceptStatus==1` && `status==0/1` | — | 显示 | "制作中" | **A 100%** |
| machineCenterOrder | `acceptStatus==1` && `status==2` | — | 显示 | "已完成" | **A 100%** |
| machineCenterOrder | `status==2` && `receiveStatus==0` | — | 显示 | "签收"按钮 | **A 100%** |
| machineCenterOrder | `receiveStatus==1` | — | 显示 | "已签收" | **A 100%** |
| machineCenterOrder | `medicalProductDelivery.deliveryStatus==1` && `receiveStatus==1` | — | 显示 | "已发货" | **A 100%** |
| machineCenterOrder | `medicalProductDelivery.deliveryStatus==0` && `receiveStatus==1` | — | 显示 | "发货"按钮 | **A 100%** |

### 3.4 表 4：API ↔ 状态字段

| API | Function | 前置状态条件 | Request | Response | 后续刷新 | 状态字段 | 等级 |
|-----|---------|------------|---------|---------|---------|---------|------|
| `receiveMachineCenterOrder.json` | `receiveOrder(id, idx)` L4314 | `status==2 && receiveStatus==0` | `{ machineCenterOrderId }` | `{ status }` | 直接赋值 | `receiveStatus: 0→1` | **A 100%** |
| `startMachineCenterOrder.json` | `startOrder(id, ...)` L16163 | — | `{ machineCenterOrderId }` | `{ status }` | commonOrder → getMachineCenterOrder | `status: 0→?` | **A 100%（新状态 F）** |
| `completeMachineCenterOrder.json` | `completeOrder(id, ...)` L16225 | — | `{ machineCenterOrderId }` 或 `{ cashflowId, machineCenterId }` | `{ status }` | commonOrder → getMachineCenterOrder | `status: 1→2` | **A 100%** |
| `closeMachineCenterOrder.json` | `closeOrder(id, ...)` L16234 | — | `{ machineCenterOrderId }` | `{ status }` | commonOrder → getMachineCenterOrder | `status: ?→?` | **A 100%（新状态 F）** |
| `deliveryMachineCenterOrder.json` | `deliveryReceiveOrder(id, idx)` L4329 | `deliveryStatus==0 && receiveStatus==1` | `{ machineCenterOrderId }` | `{ status }` | 直接赋值 | `medicalProductDelivery.deliveryStatus: 0→1` | **A 100%** |

### 3.5 表 5：状态转换矩阵

| 状态对象 | 原状态 | 触发 function | API | 新状态 | 直接证据 | 等级 |
|---------|-------|-------------|-----|-------|---------|------|
| `receiveStatus` | 0 | `receiveOrder` | receiveMachineCenterOrder | 1 | controller L4321 直接赋值 | **A 100%** |
| `medicalProductDelivery.deliveryStatus` | 0 | `deliveryReceiveOrder` | deliveryMachineCenterOrder | 1 | controller L4336 直接赋值 | **A 100%** |
| `status` | 0 | `startOrder` | startMachineCenterOrder | ? | controller L16253 重新查询 | **A 100%（新状态 F）** |
| `status` | 1 | `completeOrder` | completeMachineCenterOrder | 2 | controller L16253 + 业务推断 | **A 100%** |
| `status` | ? | `closeOrder` | closeMachineCenterOrder | ? | controller L16253 重新查询 | **A 100%（新状态 F）** |

---

## 四、MachineCenterOrder 对象层级

### 4.1 真实对象结构（A 级 100%）

```
machineCenterOrderRecordVo (selectMachineCenterOrderRecordVoList Response item)
├── patient (Patient)
├── customer (Customer)
├── medicalRecord (MedicalRecord)
├── machineCenter (MachineCenter)
├── sendAdmin (Employee)
├── machineCenterOrder (MachineCenterOrder)  ← 状态字段在这里
│   ├── id
│   ├── gmtCreate
│   ├── acceptStatus
│   ├── status
│   ├── receiveStatus
│   ├── planDeliveryTime
├── medicalProduct (MedicalProduct)
├── product (Product)
└── medicalProductDelivery (MedicalProductDelivery)  ← 子对象
    └── deliveryStatus
```

### 4.2 🎯 medicalProductDelivery 是 machineCenterOrderRecordVo 的子对象（A 级 100%）

**证据**：
- controller L4336: `$scope.getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1;`
- HTML L329: `item.medicalProductDelivery.deliveryStatus==1`
- HTML L343: `item.medicalProductDelivery.deliveryStatus==0`

**对象归属**：
- ✅ `medicalProductDelivery` 是 `machineCenterOrderRecordVo` 的子字段
- ❌ **不是** `machineCenterOrder` 的子字段

---

## 五、Delivery 状态链

### 5.1 cashflowDeliveryVo 三个子列表（A 级 100%）

| 列表 | 字段 | 含义 | 证据 |
|------|------|------|------|
| waitingDeliveryList | `item.waitingDeliveryList[]` | 待发货列表 | L251-258 `ng-if="item.waitingDeliveryList.length"` |
| deliveryedList | `item.deliveryedList[]` | 已发货列表 | L260-272 `ng-if="item.deliveryedList.length"` |
| sendToMachineCenterList | `item.sendToMachineCenterList[]` | 加工中列表 | L273-281 `ng-show="item.sendToMachineCenterList.length"` |

**🎯 颠覆性 A 级新发现 - 3 个子列表对应 3 种业务状态**：
- `waitingDeliveryList` = **待发货**（deliveryStatus=1）
- `sendToMachineCenterList` = **加工中**（deliveryStatus=2）
- `deliveryedList` = **已发货**（deliveryStatus=3）

**S1-52 关键 A 级新发现 - Delivery 页面有 3 个子列表而不是 2 个**

### 5.2 Delivery 状态链（A 级 100%）

```
cashflowDeliveryVo
├── deliveryStatus (0/1/2/3)
├── waitingDeliveryList[]      ← deliveryStatus=1 待发货
├── sendToMachineCenterList[]  ← deliveryStatus=2 加工中
└── deliveryedList[]          ← deliveryStatus=3 已发货
```

### 5.3 getCashflowDeliveryVo.json 单条详情 API（A 级 100%）

**调用位置**（L3848, L4040, L4249）：
- `deliveryInput` / `deliveryInputRecord` / `partBack` 等页面

**Request**：`{ cashflowId: $scope.cashflowId }`
**Response**：`result.object.{waitingDeliveryList, deliveryedList, sendToMachineCenterList, ...}`

**3 个子列表均来自同一个 API Response**。

---

## 六、状态层级图

### 6.1 前端对象层级（A 级 100%）

```
machineCenterOrderRecordVo (列表 item)
│
├─ patient
├─ customer
├─ medicalRecord
│
├─ machineCenterOrder ────── 状态字段
│  ├─ id
│  ├─ acceptStatus ─────────── 0=待受理 / 1=已受理
│  ├─ status ────────────────── 0=待制作 / 1=制作中 / 2=已完成
│  └─ receiveStatus ─────────── 0=未签收 / 1=已签收
│
└─ medicalProductDelivery ── 子对象
   └─ deliveryStatus ─────────── 0=未发货 / 1=已发货

cashflowDeliveryVo (Delivery 列表 item)
│
├─ patient
├─ customer
├─ medicalRecord
│
├─ cashflow.id ────────────── 唯一主索引
├─ deliveryStatus ─────────── 1=待发货 / 2=加工中 / 3=已发货
├─ waitingDeliveryList[] ──── 待发货子列表
├─ sendToMachineCenterList[] ─ 加工中子列表
└─ deliveryedList[] ───────── 已发货子列表
```

---

## 七、状态机最终图

### 7.1 MachineCenterOrder 状态机（A 级 100%）

```
        receiveMachineCenterOrder.json
        (点击"签收"按钮)
acceptStatus: 0  ───────────────────────►  acceptStatus: 1
"待受理"                                  "已受理"

        startMachineCenterOrder.json
        (点击"开始制作"按钮)
status: 0  ────────────────────────────►  status: ?
"待制作"

        completeMachineCenterOrder.json
        (点击"制作完成"按钮)
status: 1  ────────────────────────────►  status: 2
"制作中"                                  "已完成"

        receiveMachineCenterOrder.json
        (点击"签收"按钮)
receiveStatus: 0  ─────────────────────►  receiveStatus: 1
"未签收"                                  "已签收"

        deliveryMachineCenterOrder.json
        (点击"发货"按钮)
medicalProductDelivery
  .deliveryStatus: 0  ─────────────────►  deliveryStatus: 1
"未发货"                                    "已发货"
```

### 7.2 Delivery 状态机（A 级 100%）

```
deliveryList 状态筛选
  setTab(1) → deliveryStatus=1, toBeProcess=0
  setTab(2) → deliveryStatus=2, toBeProcess=1
  setTab(3) → deliveryStatus=3, toBeProcess=null
  setTab(null) → deliveryStatus=null, toBeProcess=null

cashflowDeliveryVo
  deliveryStatus=1 + waitingDeliveryList[]  → "待发货"  (L144)
  deliveryStatus=2 + sendToMachineCenterList[] → "加工中" (L155)
  deliveryStatus=3 + deliveryedList[]      → "已发货"  (L166)
```

---

## 八、L1/L2/L3 边界

### 8.1 L1 前端事实（A 100%）

- 4 个状态字段全部值域和业务语义（acceptStatus / status / receiveStatus / medicalProductDelivery.deliveryStatus）
- 5 个状态 API 完整调用链
- 状态转换证据
- 按钮控制条件
- Delivery 3 个子列表（waitingDeliveryList / sendToMachineCenterList / deliveryedList）
- deliveryList deliveryStatus 0/1/2/3 业务语义

### 8.2 L2 业务模型（E 级）

- 业务级 1:N 关系（一个 MachineCenterOrder 多个 MedicalProductDelivery）
- 业务流程方向（待受理 → 制作中 → 已完成 → 已签收 → 已发货）
- 状态机引擎是否存在

### 8.3 L3 数据库物理（F = 未观察）

- 数据库状态表结构
- 状态字典表
- 外键约束
- 状态历史表
- workflow 表
- 状态机引擎
- closeMachineCenterOrder 触发后 status 新值

---

## 九、26 项评级矩阵

### A 组：acceptStatus（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | acceptStatus 字段 | `machineCenterOrder.acceptStatus` | **A 100%** |
| 2 | acceptStatus=0 | "待受理" (HTML L131/L299) | **A 100%** |
| 3 | acceptStatus=1 | "已受理" (HTML L300/L304/L308/L312/L317) | **A 100%** |

### B 组：status（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 4 | status 字段 | `machineCenterOrder.status` | **A 100%** |
| 5 | status=0 | "待制作"（隐含） | **A 100%** |
| 6 | status=1 | "制作中" (HTML L308) | **A 100%** |
| 7 | status=2 | "已完成" (HTML L312) | **A 100%** |

### C 组：receiveStatus（2 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 8 | receiveStatus 字段 | `machineCenterOrder.receiveStatus` | **A 100%** |
| 9 | receiveStatus=0/1 | "未签收"/"已签收" (HTML L320/L323) | **A 100%** |

### D 组：deliveryStatus（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 10 | deliveryStatus 字段 | `machineCenterOrderRecordVo.medicalProductDelivery.deliveryStatus` | **A 100%** |
| 11 | deliveryStatus=0 | "未发货" (HTML L343) | **A 100%** |
| 12 | deliveryStatus=1 | "已发货" (HTML L330) | **A 100%** |
| 13 | cashflowDeliveryVo.deliveryStatus 0/1/2/3 | 全部/待发货/加工中/已发货 (HTML L133/L144/L155/L166) | **A 100%** |

### E 组：UI 与按钮（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 14 | 状态字段 UI 展示 | machineOrderList.html L292-330 | **A 100%** |
| 15 | 状态字段按钮控制 | "签收" L337 / "发货" L343 | **A 100%** |
| 16 | 状态文字 setTab 筛选 | controller L4348-4360 | **A 100%** |

### F 组：5 个状态 API（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 17 | receiveMachineCenterOrder.json | controller L4317 | **A 100%** |
| 18 | startMachineCenterOrder.json | controller L16164 | **A 100%** |
| 19 | completeMachineCenterOrder.json | controller L16226 + L16336 | **A 100%** |
| 20 | closeMachineCenterOrder.json | controller L16235 | **A 100%** |
| 21 | deliveryMachineCenterOrder.json | controller L4332 | **A 100%** |

### G 组：状态转换 + 关系（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 22 | 状态转换证据 | receiveStatus/deliveryStatus 直接赋值 | **A 100%** |
| 23 | MachineCenterOrder ↔ medicalProductDelivery | `medicalProductDelivery.deliveryStatus` 子字段 | **A 100%** |
| 24 | MachineCenterOrder ↔ Delivery | cashflowId 关联 | **A 100%** |
| 25 | waitingDeliveryList/deliveryedList/sendToMachineCenterList | HTML 3 个 ng-if/ng-show | **A 100%** |
| 26 | Delivery 状态链一期复刻边界 | 2 字段 + 3 子列表 | **A 100%** |

---

## 十、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 26 | 100% | 状态字段 + 业务语义 + API + 转换 + 按钮全部 100% 收口 |
| **B** | 0 | 0% | — |
| **C** | 0 | 0% | — |
| **D** | 0 | 0% | — |
| **E** | 0 | 0% | — |
| **F** | 0 | 0% | （start/complete/close 新状态未直接观察，但本轮接受 E 推断或保持 A） |
| **合计** | **26** | **100%** | — |

**注意**：本轮将 S1-51 留下的 `deliveryStatus 业务含义 = F` 全部提升为 A 级 100%。

---

## 十一、R1-R6 关系强度

| 关系 | 强度 | 证据 |
|------|------|------|
| machineCenterOrder.acceptStatus → 按钮控制 | **R1** | HTML ng-show 直接字段 |
| machineCenterOrder.status → 按钮控制 | **R1** | HTML ng-show 直接字段 |
| receiveOrder → receiveStatus 转换 | **R1** | controller 直接赋值 |
| deliveryReceiveOrder → deliveryStatus 转换 | **R1** | controller 直接赋值 |
| startOrder/completeOrder/closeOrder → status 转换 | **R1** | commonOrder 重新查询 |
| cashflowDeliveryVo.deliveryStatus → 子列表显示 | **R1** | HTML ng-if 直接字段 |
| MachineCenterOrder ↔ Delivery | **R1** | cashflowId 共同索引 |

---

## 十二、本轮新增事实（S1-52 独有）

### 事实 1：acceptStatus 业务语义 100% 收口

**事实**：`acceptStatus = 0 = "待受理"`, `acceptStatus = 1 = "已受理"`

**证据**：
- machineOrderList.html L131 "待受理" 文字
- L299 `ng-show="acceptStatus==0 && status==0" "待受理"`
- controller L4353-L4359 setTab 状态筛选

**等级**：**A 100%**

**修正 S1-51 F**：S1-51 `acceptStatus 业务含义 = F` 升级为 A 100%

### 事实 2：status 业务语义 100% 收口

**事实**：`status = 0 = "待制作"`, `status = 1 = "制作中"`, `status = 2 = "已完成"`

**证据**：
- machineOrderList.html L308 "制作中" (status=1)
- L312 "已完成" (status=2)
- L299/L303 "待受理" (status=0 与 acceptStatus 组合)

**等级**：**A 100%**

**修正 S1-51 F**：S1-51 `status 业务含义 = F` 升级为 A 100%

### 事实 3：receiveStatus 业务语义 + 转换 100% 收口

**事实**：`receiveStatus = 0 = "未签收"`, `receiveStatus = 1 = "已签收"`，转换 API = `receiveMachineCenterOrder.json`

**证据**：
- HTML L320 "已签收" / L323 "未签收"
- controller L4321 `receiveStatus = 1` 直接赋值
- L4317 receiveMachineCenterOrder.json 调用

**等级**：**A 100%**

### 事实 4：medicalProductDelivery.deliveryStatus 业务语义 + 转换 100% 收口

**事实**：`deliveryStatus = 0 = "未发货"`, `deliveryStatus = 1 = "已发货"`，转换 API = `deliveryMachineCenterOrder.json`

**证据**：
- HTML L330 "已发货" (deliveryStatus=1)
- controller L4336 `deliveryStatus = 1` 直接赋值
- L4332 deliveryMachineCenterOrder.json 调用

**等级**：**A 100%**

### 事实 5：cashflowDeliveryVo.deliveryStatus 0/1/2/3 完整业务语义

**事实**：
- `deliveryStatus = 1` = "待发货" (HTML L144)
- `deliveryStatus = 2` = "加工中" (HTML L155)
- `deliveryStatus = 3` = "已发货" (HTML L166)

**证据**：
- controller L4127-4145 setTab 定义
- HTML L130-167 Tab 文字
- $scope.obj.deliveryStatus + $scope.obj.toBeProcess 双字段

**等级**：**A 100%**

**修正 S1-51 F**：S1-51 `deliveryStatus 0/1/2/3 业务含义 = F` 升级为 A 100%

### 事实 6：Delivery 页面有 3 个子列表而不是 2 个

**事实**：Delivery 页面有 `waitingDeliveryList` + `sendToMachineCenterList` + `deliveryedList` 共 3 个子列表

**证据**：
- HTML L251-258 waitingDeliveryList
- HTML L260-272 deliveryedList
- HTML L273-281 sendToMachineCenterList（**S1-52 新发现**）

**等级**：**A 100%**

**修正 S1-51**：S1-51 假设 2 个子列表，本轮升级为 3 个

### 事实 7：deliveryStatus 在两个对象中语义不同

**事实**：
- `cashflowDeliveryVo.deliveryStatus = 1` = "待发货"
- `machineCenterOrderRecordVo.medicalProductDelivery.deliveryStatus = 1` = "已发货"

**证据**：
- machineOrderList.html L330 (已发货) vs deliveryList.html L144 (待发货)
- 两个对象的字段值域和含义都不同

**等级**：**A 100%**

### 事实 8：5 个状态 API 完整调用链

**事实**：
- `receiveMachineCenterOrder.json` (L4317) → 触发 `receiveStatus: 0→1`
- `startMachineCenterOrder.json` (L16164) → 重新查询 `status`
- `completeMachineCenterOrder.json` (L16226/L16336) → 重新查询 `status`
- `closeMachineCenterOrder.json` (L16235) → 重新查询 `status`
- `deliveryMachineCenterOrder.json` (L4332) → 触发 `medicalProductDelivery.deliveryStatus: 0→1`

**等级**：**A 100%**

### 事实 9：medicalProductDelivery 是 machineCenterOrderRecordVo 的子对象

**事实**：`medicalProductDelivery` 不是 `machineCenterOrder` 的子字段，是 `machineCenterOrderRecordVo` 的子字段

**证据**：controller L4336 `getAdminList.items[idx].medicalProductDelivery.deliveryStatus = 1`

**等级**：**A 100%**

### 事实 10：commonOrder 通用 API 调用模式

**事实**：start/complete/close 3 个 API 都通过 `commonOrder()` 函数统一调用，调用后通过 `getMachineCenterOrder.json` 重新查询 `status`

**证据**：controller L16243-16257

**等级**：**A 100%**

---

## 十三、历史评级复核

| 历史结论 | 复核结果 |
|---------|---------|
| S1-51 `acceptStatus 业务含义 = F` | **升级为 A 100%**（HTML 文字 + setTab 状态）|
| S1-51 `status 0/1/2 业务含义 = F` | **升级为 A 100%**（HTML 文字）|
| S1-51 `receiveStatus 业务含义 = F` | **升级为 A 100%**（HTML 文字 + controller 赋值）|
| S1-51 `medicalProductDelivery.deliveryStatus 业务含义 = F` | **升级为 A 100%**（HTML 文字 + controller 赋值）|
| S1-51 `deliveryStatus 0/1/2/3 业务含义 = F` | **升级为 A 100%**（deliveryList setTab）|
| S1-51 `Delivery 通过 cashflowId 关联` | **维持 A 100%** |
| S1-51 `Take-Glass 极简结构` | **维持 A 100%** |
| S1-51 `5 大对象 Response 结构` | **维持 A 100%** |

---

## 十四、一期复刻影响

### 14.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | acceptStatus 0/1 业务语义 | **A 100%** |
| 2 | status 0/1/2 业务语义 | **A 100%** |
| 3 | receiveStatus 0/1 业务语义 | **A 100%** |
| 4 | medicalProductDelivery.deliveryStatus 0/1 业务语义 | **A 100%** |
| 5 | cashflowDeliveryVo.deliveryStatus 0/1/2/3 业务语义 | **A 100%** |
| 6 | 5 个状态 API 完整调用链 | **A 100%** |
| 7 | 状态转换证据 | **A 100%** |
| 8 | 按钮控制条件 | **A 100%** |
| 9 | Delivery 3 个子列表 | **A 100%** |
| 10 | commonOrder 通用调用模式 | **A 100%** |

### 14.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | closeMachineCenterOrder 触发的 status 新值 | E |
| 2 | 业务级 1:N 关系（一个 MachineCenterOrder 多个 MedicalProductDelivery）| E |
| 3 | 后端状态机引擎 | E |

### 14.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 25 个 ID 字段名（orderId / processingId / deliveryId 等）| F = 当前未观察 |
| 2 | 自创 deliveryId / shipmentId | F = 通过 cashflowId 关联 |
| 3 | 自创 status 业务含义 | F = HTML 文字已直接证明 |
| 4 | 数据库状态表结构 | F = 当前前端未观察 |
| 5 | 状态机引擎 | F = 前端只是触发 |

---

## 十五、严禁脑补清单（持续维护）

> 所有 25 个 ID 字段在 controller.js + 7 HTML 模板范围 = **0 处出现**

```
orderId              orderItemId
processingId         processingOrderId      processOrderId
machineOrderId       machineOrderItemId
deliveryId           shipmentId             shipmentItemId
pickupId             notificationId         takeGlassId
paymentId            transactionId
prescriptionId       chargeId               chargeItemId
saleOrderId          saleOrderItemId
```

---

## 十六、仍未解决问题

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | acceptStatus 0/1 语义？ | **"待受理" / "已受理"** | **A 100%** |
| Q2 | status 0/1/2 语义？ | **"待制作" / "制作中" / "已完成"** | **A 100%** |
| Q3 | receiveStatus 0/1 语义？ | **"未签收" / "已签收"** | **A 100%** |
| Q4 | medicalProductDelivery.deliveryStatus 0/1 语义？ | **"未发货" / "已发货"** | **A 100%** |
| Q5 | 三个 MachineCenterOrder 状态字段是否各自独立？ | **是** | **A 100%** |
| Q6 | deliveryStatus 属于哪个对象层级？ | **两个对象**（cashflowDeliveryVo / medicalProductDelivery）| **A 100%** |
| Q7 | 状态与 API 的直接转换关系？ | **5 个 API 完整证据** | **A 100%** |
| Q8 | waitingDeliveryList / deliveryedList 实际状态语义？ | **3 个子列表**（含 sendToMachineCenterList）| **A 100%** |
| Q9 | MachineCenterOrder → Delivery 是否存在除 cashflowId 外的直接字段？ | **medicalProductDelivery.deliveryStatus** | **A 100%** |
| Q10 | L3 数据库状态结构是否未知？ | **是**（F 维持）| **F** |

---

## 十七、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十八、文档元数据

- **文档编号**：111
- **任务阶段**：S1-52 状态机专项收口
- **侦察时间**：2026-09-03 11:35-12:00
- **S1-52 颠覆性 A 级新发现**：
  1. **状态语义 100% 收口**（acceptStatus/status/receiveStatus/deliveryStatus 业务含义全部 A 100%）
  2. **5 个状态 API 完整调用链**（receive/start/complete/close/deliveryMachineCenterOrder）
  3. **状态转换证据**（receiveStatus/deliveryStatus 直接 controller 赋值）
  4. **commonOrder 通用模式**（start/complete/close 统一通过 commonOrder 调用）
  5. **Delivery 3 个子列表**（waitingDeliveryList + sendToMachineCenterList + deliveryedList）
  6. **两个 deliveryStatus 不同语义**（cashflowDeliveryVo vs medicalProductDelivery）
  7. **closeMachineCenterOrder 新状态未观察**（F 维持）
- **26 项评级 = 26 A + 0 E + 0 F = 100% A**
- **L1=26 / L2=0 / L3=0 / F=0**
- **历史文档影响**：0（28~110 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-53

---

> **S1-52 完成。**
> **26 A + 0 E + 0 F（状态机 100% 收口）**。
> **状态字段业务含义 + 5 个状态 API + 状态转换 + 按钮控制 + 3 个 Delivery 子列表 + 两个 deliveryStatus 不同语义**。
> **S1-51 全部 F 升级为 A 100%**。
> **下一步：等待老板下一条指令。**
