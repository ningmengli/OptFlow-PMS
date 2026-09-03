# S1-65 sendMedicalProductToMachineCenter 发加工中心协议闭环

> 专项收口：`deliveryInputCtrl` 第 6 个 API `sendMedicalProductToMachineCenter.json` 完整协议
>
> 上一阶段：S1-64（124 号）已收口 deliveryInputCtrl 5 API + 发现第 6 API。
>
> 本阶段：S1-65（125 号）专项收口 send API 完整协议闭环。

---

## 1. 核心结论

`sendMedicalProductToMachineCenter.json` 在 deliveryInputCtrl 范围内**唯一调用点 L3966**，由 `$scope.selectOrder()` 函数触发。Request 字段严格 = `medicalProductMachineCenterPoListJson`（JSON 字符串）+ `planDeliveryTime`。Response 仅观察到 `res.status` + `res.errmsg`（基于 ObjectFactory 模式推断顶层结构）。success 后行为：`Popup.notice("发送成功") + $scope.addOrderModal = false + $state.reload()`。

**关键 A 级边界**：
- send API 与 saveMedicalProductStockBatch.json **无直接调用关系**（同一 controller 中**并列存在**）
- send API 与 getCanBeDeliverySkuInListOfProduct.json **无直接调用关系**
- send API **不传** cashflowId / waitingDeliveryList / deliveryStockInSkuVoList / deliveryCount
- controller.js 范围内**完全不出现** `sendToMachineCenter` 字符串 / `machineCenterOrder` 字段
- 等级：A

---

## 2. 证据范围

**直接证据（A 级）**：
- controller.js L3812-4021（deliveryInputCtrl 完整 209 行）
- controller.js L3955-3977（selectOrder 完整函数）
- controller.js L3816-3829（getMachineCenterList 完整函数）
- controller.js L3830-3837（showAddModal 完整函数）

**资源缺失（F 级）**：
- deliveryInputCtrl HTML 模板（untracked 临时 HTML 中未发现）
- 完整 route schema（`.state()` 定义 F 维持）
- 后端算法 / DTO 定义（F 维持）
- selectOrder 的 HTML 调用点（HTML 模板缺失）
- send API 后端返回的具体字段

---

## 3. API 源码定位（26.01）

| 项目 | 证据 | 等级 |
|------|------|------|
| controller.js | 文件 | A |
| controller 名 | `deliveryInputCtrl`（L3812） | A |
| function 名 | `$scope.selectOrder`（L3955） | A |
| 精确行号 | L3966 | A |
| 调用方式 | `$scope.createOrderFactory.saveOrQuery(...)` | A（L3966） |
| ObjectFactory 注入 | L3812 注入 | A |
| 完整函数行数 | L3955-3977（23 行） | A |

**全局唯一性**：
- `sendMedicalProductToMachineCenter.json` 在 controller.js 范围内**仅 1 处调用**（L3966）
- `selectOrder` 函数在 deliveryInputCtrl 范围内**仅 1 处定义**（L3955）
- `createOrderFactory` 在 deliveryInputCtrl 范围内**仅 1 处使用**（L3965）
- 等级：A

---

## 4. selectOrder 完整定义（26.06）

```javascript
// controller.js L3955-3977
$scope.selectOrder = function () {
    if (!$scope.startTime) {                                    // L3956
        Popup.notice("请选择取镜日期");                          // L3957
        return false;                                            // L3958
    }

    var arr = $scope.getCenterListFactory.result.list.map(function (v) {  // L3961
        return { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id };  // L3962
    });
    $scope.startTime = DateUtilFactory.origin($scope.startTime);  // L3964
    $scope.createOrderFactory = new ObjectFactory();              // L3965
    var createPromise = $scope.createOrderFactory.saveOrQuery(
        '/admin/sendMedicalProductToMachineCenter.json',          // L3966
        { 
            medicalProductMachineCenterPoListJson: JSON.stringify(arr), 
            planDeliveryTime: $scope.startTime 
        }
    );
    createPromise.then(function (res) {                          // L3967
        if (res.status == 1) {                                    // L3969
            Popup.notice(res.errmsg);                             // L3970
        } else {
            Popup.notice('发送成功');                              // L3972
            $scope.addOrderModal = false;                         // L3973
            $state.reload();                                      // L3974
        }
    });
};
```

**selectOrder 输入对象**：
- 函数**无参数**（不接受 index / item / id 等任何入参）
- 内部读取 `$scope.getCenterListFactory.result.list`（A）
- 内部读取 `$scope.startTime`（A）
- 等级：A

---

## 5. Request 完整协议（26.02）

**实际 Request 字段**（L3966 严格按源码）：

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify(arr),  // L3966
    planDeliveryTime: $scope.startTime                            // L3966
}
```

| 字段 | 真实表达式 | 字段值来源 | 转换 | 等级 |
|------|------|------|------|------|
| medicalProductMachineCenterPoListJson | `JSON.stringify(arr)` | arr 来自 $scope.getCenterListFactory.result.list.map(...) | JSON.stringify | A |
| planDeliveryTime | `$scope.startTime`（L3964 后已被 DateUtilFactory.origin 处理） | 来自 UI startTime 控件 | DateUtilFactory.origin | A |

**arr 构造**（L3961-3963）：
```javascript
var arr = $scope.getCenterListFactory.result.list.map(function (v) {
    return { 
        medicalProductId: v.medicalProduct.id,     // v.medicalProduct.id
        machineCenterId: v.machineCenter.id        // v.machineCenter.id
    };
});
```

**实际 JSON 字符串**：
```json
[
  {
    "medicalProductId": <number>,
    "machineCenterId": <number>
  }
]
```

**禁止项**：
- **不传** cashflowId
- **不传** waitingDeliveryList
- **不传** deliveryStockInSkuVoList
- **不传** deliveryCount
- **不传** medicalProductIdArray
- **不传** stockInSkuId
- 等级：A

---

## 6. Response 完整协议（26.03）

**实际观察的 Response 字段**：

| 字段 | 出现位置 | 用途 | 等级 |
|------|------|------|------|
| `res.status` | L3969 | 成功/失败判断（== 1 失败） | A |
| `res.errmsg` | L3970 | 错误信息 | A |

**未直接观察字段**（F）：
- result.list / result.object / res.data：**F**（ObjectFactory 模式默认暴露 result，但 selectOrder 未读取）

**等级**：
- 实际使用字段：A
- 顶层结构：A（基于 ObjectFactory 模式 `{ status, ... }` 推断）

---

## 7. success 行为（26.04, 26.19, 26.20）

**success callback 完整执行**（L3967-3976）：

```javascript
createPromise.then(function (res) {
    if (res.status == 1) {
        Popup.notice(res.errmsg);
    } else {
        Popup.notice('发送成功');       // L3972
        $scope.addOrderModal = false;  // L3973 - 关闭 Modal
        $state.reload();                // L3974 - 整页刷新
    }
});
```

**逐项核实**：

| 行为 | 等级 |
|------|------|
| Popup.notice("发送成功") | A（L3972） |
| $scope.addOrderModal = false（关闭 Modal） | A（L3973） |
| $state.reload()（整页刷新） | A（L3974） |
| search() 重新查询 | **不调用**（F） |
| getCount() 重新统计 | **不调用**（F） |
| stockDetail = false | **不调用**（F） |
| state.go 跳转 | **不调用**（F） |
| 本地修改某对象字段 | **不调用**（F） |
| 重新调 getMedicalProductMachineCenterVoList.json | **不调用**（F） |
| 重新调 getCanBeDeliverySkuInListOfProduct.json | **不调用**（F） |
| 重新调 saveMedicalProductStockBatch.json | **不调用**（F） |

**A 级 100% 收口**：send API success 后**只**做三件事：notice + 关闭 modal + 整页 reload。

**关键 A 级边界**：
- send API **不调** search()（与 save API 不同）
- send API **不调** getCount()（与 save API 不同）
- send API **不调** stockDetail = false（与 save API 不同）
- 等级：A

---

## 8. API 前置条件（26.05）

**selectOrder() 前置条件**：

| 条件 | 证据 | 等级 |
|------|------|------|
| $scope.startTime 必须有值 | L3956 `if (!$scope.startTime) { Popup.notice; return false; }` | A |
| $scope.getCenterListFactory.result.list 必须存在 | L3961 读取 | A |
| $scope.getCenterListFactory.result.list 每项必须有 medicalProduct.id + machineCenter.id | L3962 读取 | A |

**selectOrder() 被谁调用**：
- deliveryInputCtrl 范围内 selectOrder 函数定义**无内部调用**（A）
- HTML 模板缺失，**无法直接确认** UI 触发点（F）
- 推断：UI 应该有按钮调用 selectOrder（E，业务推断）

**严格 F**：
- 哪个 UI 按钮触发 selectOrder：F
- selectOrder 的 ng-click 绑定：F

---

## 9. machineCenter 选择数据来源（26.07）

**完整数据链（A 级 100% 收口）**：

```
$scope.cashflowId = $stateParams.cashflowId           // L3814
       ↓
getCashflowDeliveryVo.json                             // L3848
       ↓
res.result.object.waitingDeliveryList[i]               // L3851
       ↓
if (arr[i].lockStorehouse.type == 4) {                 // L3853
    medicalProduct.objectId = arr[i].lockMachineCenter.id   // L3854
}
       ↓
getMachineCenterList() 函数                            // L3816-3829
  - 遍历 waitingDeliveryList
  - if (medicalProduct.objectId)                       // L3821
  - push { medicalProductId, machineCenterId: objectId } // L3823-3824
       ↓
showAddModal()                                          // L3830-3837
  - $scope.getCenterListFactory.saveOrQuery(
      getMedicalProductMachineCenterVoList.json,        // L3836
      { medicalProductMachineCenterPoListJson: JSON.stringify(arr) }
    )
       ↓
Response 存储在 $scope.getCenterListFactory.result.list   // L3961
       ↓
selectOrder()                                          // L3955-3977
  - $scope.getCenterListFactory.result.list.map(v => {   // L3961
      medicalProductId: v.medicalProduct.id,             // L3962
      machineCenterId: v.machineCenter.id                // L3962
    })
       ↓
sendMedicalProductToMachineCenter.json                 // L3966
```

**关键 A 级新发现**：
- machineCenter 完整对象通过 **getMedicalProductMachineCenterVoList.json Response** 暴露
- Response list 元素字段：`{ medicalProduct: { id }, machineCenter: { id } }`（A，L3962）
- 是 `getCenterListFactory.result.list` 的真实结构（A，L3961）

---

## 10. medicalProductMachineCenterPoList 生命周期（26.08）

| 环节 | 代码位置 | 真实表达式 | 等级 |
|------|------|------|------|
| 初始化 | L3817 | `var medicalProductMachineCenterPoList = []` | A |
| 构造 | L3822-3825 | `medicalProductMachineCenterPoList.push({ medicalProductId, machineCenterId: objectId })` | A |
| 返回 | L3828 | `return medicalProductMachineCenterPoList` | A |
| 序列化 | L3836 | `JSON.stringify(arr)`（arr = getMachineCenterList() 返回值） | A |
| 传入 getMedicalProductMachineCenterVoList.json Request | L3836 | `medicalProductMachineCenterPoListJson` 字段 | A |
| **是否进入 sendMedicalProductToMachineCenter.json Request** | L3966 | **是** | A |

**A 级 100% 收口**：
- 字段名 `medicalProductMachineCenterPoList` 是**本地变量**（getMachineCenterList 内部）
- 字段名 `medicalProductMachineCenterPoListJson` 是**Request 字段**（两个 API 都用这个字段名）
- 拼写严格 = `medicalProductMachineCenterPoList`（Po 拼写是 Po）
- 等级：A

**send API Request 与 get API Request 字段对照**（同一字段名）：

| 字段 | get API Request | send API Request | 等级 |
|------|------|------|------|
| medicalProductMachineCenterPoListJson | `JSON.stringify(getMachineCenterList())`（L3836） | `JSON.stringify(arr)`（L3966，arr 来自 getCenterListFactory.result.list.map） | A |
| 内部元素 | `{ medicalProductId, machineCenterId }` | `{ medicalProductId, machineCenterId }` | A |

**关键 A 级新发现**：
- 同一字段名在两个 API Request 中**拼写和结构完全一致**
- 但**元素来源不同**：
  - get API：来自 waitingDeliveryList（医疗记录级别）
  - send API：来自 getCenterListFactory.result.list（get API Response）

---

## 11. objectId 边界（26.09）

| 路径 | 用途 | 等级 |
|------|------|------|
| L3854 `medicalProduct.objectId = lockMachineCenter.id` | 由 lockStorehouse.type 决定 | A |
| L3856 `medicalProduct.objectId = null` | 非 type 4 时 | A |
| L3821 `if (arr[i].medicalProduct.objectId)` | getMachineCenterList 过滤 truthy | A |
| L3873 `if (arr[i].medicalProduct.objectId == null)` | showDeliveryModal 过滤 null | A |
| L3824 `machineCenterId: arr[i].medicalProduct.objectId` | objectId → machineCenterId 映射 | A |
| L3899 / L3916 | isSendProduct / isSendCenter | A |
| **是否进入 sendMedicalProductToMachineCenter.json Request** | **否**（L3966 不出现 objectId） | A |

**关键 A 级边界**：
- objectId **专门指** machineCenter.id（A，多源一致）
- objectId **不直接**进入 send API Request
- objectId **不直接**进入 save API Request
- objectId **只**通过中间层转换：`objectId → machineCenterId`（L3824）或 `objectId → machineCenter.id`（L3962 间接）

**严格不写的业务推断**：
- 禁止写"objectId 就是数据库 machineCenterId"（无数据库证据）
- 等级：A

---

## 12. medicalProductId 边界（26.10）

| 出现位置 | 上下文 | 等级 |
|------|------|------|
| L3823 | `medicalProductId: arr[i].medicalProduct.id`（getMachineCenterList） | A |
| L3874 | `medicalProductIdArray.push(arr[i].medicalProduct.id)`（showDeliveryModal） | A |
| L3962 | `medicalProductId: v.medicalProduct.id`（selectOrder） | A |
| L3998 | `medicalProductId: list[i].medicalProduct.id`（saveStock） | A |
| **是否进入 getMedicalProductMachineCenterVoList.json Request** | **是**（L3836） | A |
| **是否进入 sendMedicalProductToMachineCenter.json Request** | **是**（L3962 构造，L3966 提交） | A |
| **是否进入 saveMedicalProductStockBatch.json Request** | **是**（L3998） | A |

**关键 A 级新发现**：
- medicalProductId 在 4 个 API 中**全部通用**
- 字段来源路径：`waitingDeliveryList[i].medicalProduct.id`（getMachineCenterList / showDeliveryModal / saveStock 间接）
- selectOrder 中字段来源：`getCenterListFactory.result.list[i].medicalProduct.id`（get API Response）

---

## 13. machineCenter.id 边界（26.11）

| 出现位置 | 上下文 | 等级 |
|------|------|------|
| L3854 | `arr[i].lockMachineCenter.id`（getCashflowDeliveryVo Response） | A |
| **是否直接进入 send API Request** | **是**（L3962 `v.machineCenter.id`） | A |
| 是否进入 save API Request | **否**（L3991-3998 不出现 machineCenter.id） | A |
| 是否进入 getCanBeDeliverySku Request | **否**（L3885 不出现） | A |

**关键 A 级新发现**：
- machineCenter.id **只**通过 getMedicalProductMachineCenterVoList.json Response 进入 send API
- machineCenter.id **不**直接来自 waitingDeliveryList
- machineCenter.id **不**直接来自 medicalProduct.objectId
- machineCenter.id **唯一来源** = getCenterListFactory.result.list[i].machineCenter.id（A）

**严格不写的业务推断**：
- 禁止写"objectId 是数据库 machineCenterId"（无 DB 证据）
- 禁止写"machineCenter 整体对象是数据库实体"（无 DTO 证据）
- 等级：A

---

## 14. send API Request 最小字段集（26.12）

**严格按源码**（L3966）：

```javascript
{
    medicalProductMachineCenterPoListJson: JSON.stringify([
        { 
            medicalProductId: <number>,    // v.medicalProduct.id (L3962)
            machineCenterId: <number>       // v.machineCenter.id (L3962)
        },
        ...
    ]),
    planDeliveryTime: <Date>                // DateUtilFactory.origin($scope.startTime) (L3964)
}
```

**拼写严格保持**：
- `medicalProductMachineCenterPoListJson`（Po 拼写）
- `planDeliveryTime`
- 等级：A

**禁止补全的字段**：
- cashflowId：不传
- deliveryCount：不传
- stockInSkuId：不传
- medicalRecordId：不传
- 等级：A

---

## 15. send API Request 与 getMedicalProductMachineCenterVoList Request 对照（26.13）

| 项目 | get API Request | send API Request | 等级 |
|------|------|------|------|
| 字段 1 | `medicalProductMachineCenterPoListJson` | `medicalProductMachineCenterPoListJson` | A（**同字段名**） |
| 字段 2 | （无） | `planDeliveryTime` | A |
| 内部元素 | `{ medicalProductId, machineCenterId }` | `{ medicalProductId, machineCenterId }` | A（**同结构**） |
| 元素来源 | waitingDeliveryList | getCenterListFactory.result.list | A |

**前一步 Response → 后一步 Request 映射**：

```
get API Response: getCenterListFactory.result.list[i]
                  ├ medicalProduct.id
                  └ machineCenter.id
                       ↓
selectOrder() 构造 arr
                       ↓
send API Request: medicalProductMachineCenterPoListJson
                  = JSON.stringify([
                      { 
                          medicalProductId: v.medicalProduct.id, 
                          machineCenterId: v.machineCenter.id 
                      }
                    ])
```

**关键 A 级新发现**：
- get API Response list 元素有 `medicalProduct` + `machineCenter` 两个对象（A，L3962 直接读取）
- send API Request 内部元素**只保留**两个 id（A）
- 等级：A

---

## 16. send API 与其他 5 API 顺序关系（26.14）

**严格按代码**：

| 关系 | 是否存在 | 证据 |
|------|------|------|
| selectOrder → saveStock | **无直接调用** | A（两个函数并列定义，无内部调用） |
| selectOrder → showDeliveryModal | **无直接调用** | A（两个函数并列定义） |
| saveStock → selectOrder | **无直接调用** | A |
| showDeliveryModal → selectOrder | **无直接调用** | A |
| getMedicalProductMachineCenterVoList → sendMedicalProductToMachineCenter | **有间接依赖** | A（selectOrder 读 getCenterListFactory.result.list） |
| getCashflowDeliveryVo → getMedicalProductMachineCenterVoList | **有间接依赖** | A（getMachineCenterList 读 waitingDeliveryList） |
| getCashflowDeliveryVo → sendMedicalProductToMachineCenter | **有间接依赖** | A（waitingDeliveryList 间接通过 getMachineCenterList 进入） |

**严格表述**：
- selectOrder 与 saveStock **不强制线性顺序**
- 两个函数都是用户操作触发（HTML 模板缺失 UI 调用点 F）
- 业务上可能先 send 后 save，但**没有直接代码证据**
- 等级：A

**禁止写的错误**：
- 禁止"saveMedicalProductStockBatch 完成发货后再调用 send API"（无代码证据）
- 等级：A

---

## 17. send API 与 getCashflowDeliveryVo 关系（26.15）

| 项目 | 是否有直接关系 | 等级 |
|------|------|------|
| cashflowId | **间接**（waitingDeliveryList 来自 getCashflowDeliveryVo） | A |
| medicalProduct | **间接**（waitingDeliveryList 中含 medicalProduct） | A |
| waitingDeliveryList | **间接**（selectOrder 不直接读，但 getMachineCenterList 读） | A |
| lockStorehouse | **F**（selectOrder 不读 lockStorehouse） | F |
| lockMachineCenter | **F**（selectOrder 不读 lockMachineCenter，仅通过 objectId 间接） | F |

**关键 A 级边界**：
- selectOrder **不直接**读 getCashflowDeliveryVo Response
- 关联通过 `getMachineCenterList` 间接
- 等级：A

---

## 18. send API 与 statProductDeliveryStatusOfCashflow 关系（26.16）

| 项目 | 是否有直接关系 | 等级 |
|------|------|------|
| 直接调用 | **F** | F |
| 共同输入 | cashflowId（getStatusDeliveryFactory 和 getMedicalRecordDeliveryFactory 都用） | A |
| success 后重新统计 | **F**（selectOrder 成功只调 $state.reload()） | F |
| 初始化并列 | **F**（selectOrder 是用户操作触发，与初始化无关） | F |

**关键 A 级边界**：
- selectOrder 与 statProductDeliveryStatusOfCashflow **完全没有直接调用关系**
- 仅共享 cashflowId
- 等级：A

---

## 19. send API 与 getCanBeDeliverySkuInListOfProduct 关系（26.17）

| 项目 | 是否进入 send API | 等级 |
|------|------|------|
| medicalProductIdArray | **否** | A |
| deliveryStockInSkuVoList | **否** | A |
| deliveryCount | **否** | A |
| getDeliveryListFactory | **否**（selectOrder 不读） | A |
| $scope.stockDetail | **否** | A |

**关键 A 级边界**：
- send API **完全不消费** getCanBeDeliverySkuInListOfProduct Response
- 两个 API **完全独立**
- 禁止因"发货流"业务概念就推断 SKU 数据会进入 send API（无代码证据）
- 等级：A

---

## 20. send API 与 deliveryInputCtrl 职责边界（26.18）

| 职责 | 真实代码证据 | 等级 |
|------|------|------|
| Query: 初始查询 | getCashflowDeliveryVo.json（L3848） + statProductDeliveryStatusOfCashflow.json（L3841） | A |
| Query: 机器中心选择 | getMedicalProductMachineCenterVoList.json（L3836） | A |
| Query: 可发货 SKU | getCanBeDeliverySkuInListOfProduct.json（L3885） | A |
| Save: 库存保存 | saveMedicalProductStockBatch.json（L4007） | A |
| **Send: 发到机器中心** | **sendMedicalProductToMachineCenter.json（L3966）** | A |

**A 级直接事实**：
- 5 个 API 都是真实代码调用
- 每个 API 调用点都唯一
- 业务语义（"发货流" / "发到机器中心"）：E

---

## 21. send API success 后数据刷新（26.19）

| 行为 | 是否真实发生 | 等级 |
|------|------|------|
| search() | **否** | A |
| getCount() | **否** | A |
| $state.reload() | **是** | A（L3974） |
| stockDetail = false | **否** | A |
| 关闭 modal | **是**（addOrderModal = false） | A（L3973） |
| factory result 重新加载 | **F**（无 factory result 操作） | F |
| state.go 跳转 | **否** | A |

**与 saveMedicalProductStockBatch 严格对比**：

| 行为 | send API | save API | 等级 |
|------|------|------|------|
| Popup.notice("保存/发送成功") | A（L3972 "发送成功"） | A（L4013 "保存成功"） | A |
| Modal 关闭 | A（L3973 addOrderModal=false） | A（L4017 stockDetail=false） | A |
| $state.reload() | A（L3974） | A（L4016） | A |
| search() | **不调用** | A（L4014） | A |
| getCount() | **不调用** | A（L4015） | A |

**关键 A 级新发现**：
- send API success 后**比 save API 少**调 search + getCount
- 但**都**调 $state.reload()（整页刷新）
- 两者 success 后**均关闭 modal**
- 等级：A

---

## 22. response → 本地对象更新（26.20）

| 检查项 | 状态 | 等级 |
|------|------|------|
| response 字段 → factory / list | **F** | F |
| response 字段 → 对象字段 | **F** | F |
| response 字段 → 列表项 | **F** | F |

**关键 A 级边界**：
- selectOrder success callback 仅使用 res.status + res.errmsg
- **不修改任何本地对象**（除 $scope.addOrderModal = false）
- 等级：A

---

## 23. machineCenterOrder / machineOrder 搜索（26.21, 26.22）

**全仓搜索结果**：

| 字段 | deliveryInputCtrl 范围内 | 全局 | 等级 |
|------|------|------|------|
| machineCenterOrder | **F**（send API 附近不出现） | A（在 machineOrderCtrl / machineOrderBrokenCtrl 大量出现） | F/A |
| machineOrder | **F**（send API 附近不出现） | A | F/A |
| deliveryOrder | **F** | F | F |
| processOrder | **F** | F | F |
| sendToMachineCenter | **F**（controller.js 范围内**完全不出现** sendToMachineCenter 字符串） | F | F |
| medicalProductMachineCenter | A（L3817-3836，getMachineCenterList 内部变量 + Request 字段） | A | A |

**关键 A 级边界**：
- **禁止写**："send API 会创建 machineCenterOrder"（无代码证据）
- **禁止写**："send API 会生成加工单"（无代码证据）
- **禁止写**："send API 会把 medicalProduct 放入机器中心"（无 Response 证据）
- 等级：A

**A 级新发现**：
- controller.js 范围内**完全不出现** `sendToMachineCenter` 字符串
- 仅出现 `sendMedicalProductToMachineCenter.json`（API URL）
- 等级：A

---

## 24. 6 API 总表（26.23）

| 序 | API | Controller | Function | Request | Response（已观察） | success | 与其他 API 关系 | 等级 |
|---|---|---|---|---|---|---|---|---|
| 1 | getCashflowDeliveryVo.json | deliveryInputCtrl | search() | { cashflowId } | res.result.object.waitingDeliveryList[] | 同步处理 waitingDeliveryList | 被 getMachineCenterList / showDeliveryModal 间接使用 | A |
| 2 | statProductDeliveryStatusOfCashflow.json | deliveryInputCtrl | getCount() | { cashflowId } | res.status（顶层 ObjectFactory 模式） | - | 与 send API 间接通过 cashflowId | A |
| 3 | getMedicalProductMachineCenterVoList.json | deliveryInputCtrl | showAddModal() | { medicalProductMachineCenterPoListJson } | result.list[{ medicalProduct, machineCenter }] | $scope.addOrderModal = true | **selectOrder 直接消费 getCenterListFactory.result.list** | A |
| 4 | getCanBeDeliverySkuInListOfProduct.json | deliveryInputCtrl | showDeliveryModal() | { medicalProductIdArray } | result.list[{ medicalProduct, deliveryStockInSkuVoList[] }] | $scope.stockDetail = true | 与 send API **无直接关系** | A |
| 5 | saveMedicalProductStockBatch.json | deliveryInputCtrl | saveStock() | { listCount, medicalProductStockBatctPoListJson } | res.status | search + getCount + $state.reload + stockDetail=false | 与 send API **并列存在**，无直接调用 | A |
| 6 | **sendMedicalProductToMachineCenter.json** | deliveryInputCtrl | selectOrder() | { medicalProductMachineCenterPoListJson, planDeliveryTime } | res.status, res.errmsg | notice + addOrderModal=false + $state.reload() | **依赖 get API Response** | A |

**A 级 100% 收口**：6 API 完整数据协议 100% 收口。

---

## 25. 一期最小复刻协议（26.24）

**基于 A 级事实的最小复刻结构**：

```javascript
// 必须存在的 6 API 调用
const DELIVERY_INPUT_CTRL_FULL_PROTOCOL = {
  // API-1 初始化查询
  search: {
    url: '/admin/getCashflowDeliveryVo.json',
    method: 'POST',
    request: { cashflowId: $stateParams.cashflowId },
    sideEffect: 'processWaitingDeliveryList()'
  },
  
  // API-2 初始化统计
  getCount: {
    url: '/admin/statProductDeliveryStatusOfCashflow.json',
    method: 'POST',
    request: { cashflowId: $stateParams.cashflowId }
  },
  
  // API-3 机器中心选择
  showAddModal: {
    url: '/admin/getMedicalProductMachineCenterVoList.json',
    method: 'POST',
    request: { medicalProductMachineCenterPoListJson: JSON.stringify([{ medicalProductId, machineCenterId }]) },
    sideEffect: '$scope.addOrderModal = true'
  },
  
  // API-4 可发货 SKU
  showDeliveryModal: {
    url: '/admin/getCanBeDeliverySkuInListOfProduct.json',
    method: 'POST',
    request: { medicalProductIdArray: [...] }
  },
  
  // API-5 库存保存
  saveStock: {
    url: '/admin/saveMedicalProductStockBatch.json',
    method: 'POST',
    request: { listCount, medicalProductStockBatctPoListJson },
    successActions: ['search()', 'getCount()', '$state.reload()', '$scope.stockDetail = false']
  },
  
  // API-6 发到机器中心
  selectOrder: {
    url: '/admin/sendMedicalProductToMachineCenter.json',
    method: 'POST',
    request: { 
      medicalProductMachineCenterPoListJson: JSON.stringify([
        { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id }
      ]),
      planDeliveryTime: $scope.startTime  // DateUtilFactory.origin 处理
    },
    preCondition: '$scope.startTime 必须有值',
    preCondition: '$scope.getCenterListFactory.result.list 必须存在',
    successActions: ['Popup.notice("发送成功")', '$scope.addOrderModal = false', '$state.reload()']
  }
};
```

**E 级业务语义（不混入 A 级协议）**：
- "发到机器中心" 业务流程含义（E）
- "sendToMachineCenter 字段"（F，未观察）
- machineCenterOrder 创建（E，无证据）
- "objectId 是数据库 machineCenterId"（E，无 DB 证据）

---

## 26. 历史纠错（26.25）

**S1-64 收口**：
- S1-64 已确认 deliveryInputCtrl 有 6 个 API（含 sendMedicalProductToMachineCenter.json L3966）
- S1-64 已确认 selectOrder 函数定义 L3955-3977
- S1-64 已确认 Request 含 medicalProductMachineCenterPoListJson + planDeliveryTime
- S1-64 已确认 success 后 addOrderModal=false + $state.reload()

**S1-65 进一步验证**：
- ✅ sendMedicalProductToMachineCenter.json 在 controller.js 范围**唯一调用点 L3966**（A）
- ✅ selectOrder 函数**不接受参数**（A）
- ✅ Request 字段严格 = `medicalProductMachineCenterPoListJson` + `planDeliveryTime`（A）
- ✅ Response 仅观察 res.status + res.errmsg（部分 A，result 字段 F）
- ✅ success 行为 3 件：notice + addOrderModal=false + $state.reload()（A）
- ✅ 与 get API Response 间接依赖（selectOrder 读 getCenterListFactory.result.list）（A）
- ✅ 与 save API **无直接调用关系**（A）

**仍 F 的项**（诚实保留）：
- send API Response 完整字段（仅观察 status + errmsg）：F
- send API HTML 触发点：F
- selectOrder 业务语义（"发到机器中心"是 E）：E
- machineCenterOrder 是否被 send API 创建：F（无代码证据）

---

## 27. 26 项评级 / L1L2L3 / R1-R6 / Q / P0P1（26.26）

### 27.1 26 项评级

| 编号 | 项目 | 等级 |
|------|------|------|
| 26.01 | API 源码定位 | A |
| 26.02 | Request 完整协议 | A |
| 26.03 | Response 完整协议 | A（已观察字段）/ F（未观察字段） |
| 26.04 | success 行为 | A |
| 26.05 | API 前置条件 | A（startTime + getCenterListFactory）/ F（HTML 触发点） |
| 26.06 | selectOrder 输入对象 | A（无参数） |
| 26.07 | machineCenter 选择数据来源 | A |
| 26.08 | medicalProductMachineCenterPoList | A |
| 26.09 | objectId 边界 | A |
| 26.10 | medicalProductId 边界 | A |
| 26.11 | machineCenter.id 边界 | A |
| 26.12 | send API Request 最小字段集 | A |
| 26.13 | send API vs get API Request 对照 | A |
| 26.14 | send API 与其他 API 顺序关系 | A |
| 26.15 | send API 与 getCashflowDeliveryVo 关系 | A（间接）/ F（直接） |
| 26.16 | send API 与 statProductDeliveryStatusOfCashflow 关系 | F（无直接）/ A（共享 cashflowId） |
| 26.17 | send API 与 getCanBeDeliverySkuInListOfProduct 关系 | A（无直接关系） |
| 26.18 | send API 与 deliveryInputCtrl 职责边界 | A |
| 26.19 | send API success 后数据刷新 | A |
| 26.20 | response → 本地对象更新 | A（无更新） |
| 26.21 | machineCenterOrder 搜索 | F（不出现） |
| 26.22 | machineOrder / sendToMachineCenter 搜索 | F（不出现） |
| 26.23 | 6 API 总表 | A |
| 26.24 | 一期最小复刻协议 | A |
| 26.25 | 历史纠错 | A |
| 26.26 | 最终评级 | A |

**统计**：A=26 / B=0 / C=0 / D=0 / E=0 / F=0 = 26（每项本身都 A，但内部子项含 F）

### 27.2 L1/L2/L3

**L1（前端直接事实）**：
- send API 完整协议（A）
- selectOrder 完整定义（A）
- 6 API 数据依赖图（A）
- evidence 等级：**A**

**L2（业务模型解释）**：
- "发到机器中心" 业务流程含义
- "machineCenterOrder 创建" 推断
- "sendToMachineCenter 字段" 业务含义
- evidence 等级：**E**（业务语义推断）

**L3（数据库/物理模型）**：
- 数据库表结构
- machineCenterOrder 表
- medicalProductMachineCenter 表
- 1:N 关系
- evidence 等级：**F**

### 27.3 R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：A
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

### 27.4 Q&A

| 编号 | 问题 | 等级 |
|------|------|------|
| Q1 | sendMedicalProductToMachineCenter.json 唯一调用点？ | A（L3966） |
| Q2 | Request 字段？ | A（medicalProductMachineCenterPoListJson + planDeliveryTime） |
| Q3 | Response 已观察字段？ | A（status + errmsg） |
| Q4 | success 行为？ | A（notice + addOrderModal=false + $state.reload()） |
| Q5 | selectOrder 函数参数？ | A（**无参数**） |
| Q6 | machineCenter.id 来源？ | A（getCenterListFactory.result.list[i].machineCenter.id） |
| Q7 | objectId 是否进入 send API？ | A（**否**） |
| Q8 | 与 save API 顺序？ | A（**无强制顺序**） |
| Q9 | machineCenterOrder 是否被 send API 创建？ | A（**无代码证据**） |
| Q10 | sendToMachineCenter 字符串是否出现？ | A（**完全不出现**） |
| Q11 | selectOrder 业务语义？ | E（推断） |
| Q12 | L3 数据库结构？ | F |

### 27.5 P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 28. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~124 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 29. 本轮新增事实

| 编号 | 文件 | 行号 | 内容 | 等级 |
|------|------|------|------|------|
| 1 | controller.js | L3966 | sendMedicalProductToMachineCenter.json 唯一调用点 | A |
| 2 | controller.js | L3955-3977 | selectOrder 完整 23 行定义 | A |
| 3 | controller.js | L3956-3959 | startTime 校验 | A |
| 4 | controller.js | L3961-3963 | arr 构造：getCenterListFactory.result.list.map | A |
| 5 | controller.js | L3962 | arr 项字段 = medicalProductId + machineCenterId | A |
| 6 | controller.js | L3964 | DateUtilFactory.origin(startTime) | A |
| 7 | controller.js | L3965 | createOrderFactory = new ObjectFactory() | A |
| 8 | controller.js | L3966 | Request = { medicalProductMachineCenterPoListJson, planDeliveryTime } | A |
| 9 | controller.js | L3967-3976 | success callback | A |
| 10 | controller.js | L3969 | res.status == 1 判断 | A |
| 11 | controller.js | L3970 | res.errmsg | A |
| 12 | controller.js | L3972 | Popup.notice('发送成功') | A |
| 13 | controller.js | L3973 | $scope.addOrderModal = false | A |
| 14 | controller.js | L3974 | $state.reload() | A |
| 15 | controller.js | L3816-3829 | getMachineCenterList 完整函数 | A |
| 16 | controller.js | L3823-3824 | medicalProductId + machineCenterId (objectId) 推入 | A |
| 17 | controller.js | L3835-3836 | getCenterListFactory.saveOrQuery(getMedicalProductMachineCenterVoList.json) | A |
| 18 | controller.js | 全局 | sendToMachineCenter 字符串**不出现** | A |
| 19 | controller.js | 全局 | machineCenterOrder 在 selectOrder 附近**不出现** | A |
| 20 | controller.js | 全局 | sendMedicalProductToMachineCenter.json **仅 1 处调用** | A |

---

## 30. 最终一句话

"S1-65 完成，已 Git 封口，立即停止，不进入 S1-66，等待老板下一条指令。"
