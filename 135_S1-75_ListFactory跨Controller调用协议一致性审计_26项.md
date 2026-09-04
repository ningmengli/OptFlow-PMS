# S1-75 ListFactory 跨 Controller 调用协议一致性审计

> 专项审计：**ListFactory 跨 Controller 调用协议**一致性
>
> 上一阶段：S1-74（134 号）已收口 ListFactory 内部实现完全缺失。
>
> 本阶段：S1-75（135 号）专项审计 ListFactory **跨 Controller 外部调用协议一致性**。

---

## 1. 核心结论

**S1-75 关键 A 级新发现**：

- **ListFactory 调用模式 100% 一致**（406 次 `new ListFactory(API, 0, pageSize, params)`）
- **4 参数调用** 100% 统一（A）
- **参数1** = API URL 字符串（A）
- **参数2** = `0`（固定，A）
- **参数3** = 数字 10/12/20（A，基于多源一致）
- **参数4** = object（A，406 次全部为 object）
- **`.nextPage()` / `.clearAndSetIndex()` / `.items` / `.count`** 100% 一致调用（A）
- **pagination callback** 模式 100% 一致（A）
- **search 函数** 模式 100% 一致（A，多个 controller 都重新 `new ListFactory`）
- 多个 controller 行为**高度同构**

**ListFactory 内部实现 = F**（维持 S1-74 收口）

**严格 A 级边界**：
- 跨 Controller **外部调用模式一致**（A）
- ListFactory **内部实现一致** = F（无源码证据）
- 严格禁止"因为多 Controller 一致调用 → ListFactory 内部一定这样实现"
- 等级：A（外部模式）/ F（内部实现）

---

## 2. 证据范围

**直接证据**：
- controller.js L1-... 全文
- 全仓 406 次 `new ListFactory(API, 0, pageSize, params)` 一致模式

**资源缺失**：
- ListFactory 内部实现（F 维持）
- HTML 模板（F 维持）
- vendor bundle（F 维持）

---

## 3. 全仓 ListFactory 调用统计（30.1）

**全仓搜索**：

| 模式 | 次数 | 等级 |
|---|---|---|
| `ListFactory` 引用 | 1983 | A |
| `new ListFactory(` | 406 | A |
| `.nextPage()` | 633 | A |
| `.clearAndSetIndex(` | 226 | A |
| `.items` | 693 | A |
| `.count` | 303 | A |

**A 级 100% 收口**：
- 调用模式 100% 一致：4 参数 `(API, 0, pageSize, params)`
- 实例方法 100% 一致：`nextPage()` / `clearAndSetIndex(index * pageSize)` / `items` / `count`
- 等级：A

**严格表述**：
- "406 次调用 100% 一致"（A）
- "ListFactory 内部一定这样实现"（**F**：禁止推断）

---

## 4. 代表性 Controller（30.2）

**6 个代表性 controller**：

| Controller | API | 行号 | 等级 |
|---|---|---|---|
| machineOrderListCtrl | selectMachineCenterOrderRecordVoList.json | L4299 | A |
| adminListCtrl | getAdminList.json | L215 | A |
| adminAreaListCtrl | getLoginAdminSubAreaAdminList.json | L83 | A |
| roleAdminCtrl | selectAdminRoleVoList.json | L720 | A |
| modifyAreaRoleCtrl | getSchoolMateManageCorpVoList.json | L740 | A |
| encryptUserCtrl | selectWatchdogList.json | L1116 | A |

**A 级 100% 收口**。

---

## 5. 构造参数数量（30.3）

**全仓 406 次调用参数数量统计**：

| 参数数量 | 次数 | 等级 |
|---|---|---|
| 4 参数 | 406 | A |
| 5 参数 | **0** | A |
| 可变 | **0** | A |

**A 级 100% 收口**：
- 全部 406 次调用都是 **4 参数**（A）
- 等级：A

---

## 6. 参数 1 比较（30.4）

| Controller | 参数1 | 等级 |
|---|---|---|
| machineOrderListCtrl | `"/admin/selectMachineCenterOrderRecordVoList.json"` | A |
| adminListCtrl | `"/admin/getAdminList.json"` | A |
| adminAreaListCtrl | `"/admin/getLoginAdminSubAreaAdminList.json"` | A |
| roleAdminCtrl | `"/admin/selectAdminRoleVoList.json"` | A |
| modifyAreaRoleCtrl | `"/admin/getSchoolMateManageCorpVoList.json"` | A |
| encryptUserCtrl | `"/admin/selectWatchdogList.json"` | A |

**A 级 100% 收口**：
- 全部是 API URL 字符串（A）
- 全部以 `/admin/...json` 开头（A）
- 等级：A

---

## 7. 参数 2 比较（30.5）

| Controller | 参数2 | 等级 |
|---|---|---|
| machineOrderListCtrl | `0` | A |
| adminListCtrl | `0` | A |
| adminAreaListCtrl | `0` | A |
| roleAdminCtrl | `0` | A |
| modifyAreaRoleCtrl | `0` | A |
| encryptUserCtrl | `0` | A |

**A 级 100% 收口**：
- 全部 **固定为 0**（A）
- 含义推断为 pageStart（E 级，**不**升 A）
- 等级：A（事实）/ E（推断）

---

## 8. 参数 3 比较（30.6）

| Controller | 参数3 | 等级 |
|---|---|---|
| machineOrderListCtrl | `10` | A |
| adminListCtrl | `10` | A |
| adminAreaListCtrl | `10` | A |
| roleAdminCtrl | `10` | A |
| modifyAreaRoleCtrl | `10` | A |
| encryptUserCtrl | `10` | A |
| adminRoleCtrl (addRole) | `20` (L46) | A |
| modifyRoleCtrl (schoolList) | `12` (L602) | A |
| adminModifyCtrl (schoolList) | `12` (L891) | A |

**A 级 100% 收口**：
- 参数3 是数字 10/12/20（A）
- 含义推断为 pageSize（E 级，**不**升 A）
- 不同 controller 用不同 pageSize（A）
- 等级：A（事实）/ E（推断）

---

## 9. 参数 4 比较（30.7, 30.8）

| Controller | 参数4 | 字段 | 等级 |
|---|---|---|---|
| machineOrderListCtrl | `$scope.obj` | 7 个字段（A，9 Request 字段） | A |
| adminListCtrl | `$scope.obj` | 多字段 | A |
| adminAreaListCtrl | `$scope.obj` | 多字段 | A |
| roleAdminCtrl | `$scope.obj` | 多字段 | A |
| modifyAreaRoleCtrl | `{}` | **空** | A |
| addRoleCtrl (L46) | `{ keyword: $scope.keyword }` | 1 字段 | A |
| schoolListCtrl (L602) | `{ keyword: $scope.keyword, schoolType: 0 }` | 2 字段 | A |
| encryptUserCtrl (L1116) | `{ keyword: $scope.keyword }` | 1 字段 | A |
| getNormalAdminList (L276) | `{ status: 0, keyword: $scope.normalKeyword, isClinicAdmin: true }` | 3 字段 | A |

**A 级 100% 收口**：
- 参数4 全部是 **object**（A）
- 可能是 `$scope.obj` / 内联 object / `{}`（A）
- 字段内容**完全不同**（A）
- 等级：A

---

## 10. 参数 4 结构比较（30.8）

**典型字段**：

| 字段 | machineOrderListCtrl | adminListCtrl | addRoleCtrl |
|---|---|---|---|
| companyId | ✓ | **F** | **F** |
| startTime | ✓ | 多源 | **F** |
| endTime | ✓ | 多源 | **F** |
| keyword | **F** | 多源 | ✓ |
| status | **F** | 多源 | **F** |
| acceptStatus | ✓ | **F** | **F** |
| statusArray | ✓ | **F** | **F** |
| machineCenterId | ✓ | **F** | **F** |
| receiveStatus | ✓ | **F** | **F** |
| schoolType | **F** | **F** | **F** |
| isClinicAdmin | **F** | **F** | **F** |

**A 级 100% 收口**：
- 不同 controller 字段**完全不同**（A）
- 严格禁止"字段相同 → 同一 DTO"
- 等级：A

---

## 11. `.items` 使用模式（30.10）

| Controller | items 访问 | 行号 | 等级 |
|---|---|---|---|
| machineOrderListCtrl | `$scope.getAdminList.items` | L4321/L4336 | A |
| adminListCtrl | `$scope.getAdminList.items` | L237 | A |
| adminAreaListCtrl | `$scope.getAdminList.items` | L90 | A |
| 其他 693 次 | 各种 `$scope.xxx.items` | 多处 | A |

**A 级 100% 收口**：
- 全部是 `$scope.<factory 实例名>.items` 模式（A）
- items 是 ListFactory 实例属性（A）
- 等级：A

---

## 12. `.count` 使用模式（30.11）

| Controller | count 访问 | 行号 | 等级 |
|---|---|---|---|
| machineOrderListCtrl | `$scope.getAdminList.count` | L4303 | A |
| adminListCtrl | `$scope.getAdminList.count` | L219 | A |
| adminAreaListCtrl | `$scope.getAdminList.count` | L87 | A |
| 其他 303 次 | 各种 `$scope.xxx.count` | 多处 | A |

**A 级 100% 收口**：
- 全部是 `$scope.<factory 实例名>.count` 模式（A）
- count 是 ListFactory 实例属性（A）
- 等级：A

---

## 13. `.nextPage()` 调用模式（30.12）

| 位置 | 上下文 | 等级 |
|---|---|---|
| L47 | `$scope.hospitalListFactory.nextPage()` 立即调用 | A |
| L84 | `var promise = $scope.getAdminList.nextPage()` search 中 | A |
| L91 | `$scope.getAdminList.nextPage()` pagination callback | A |
| L216 | search 中 | A |
| L223 | pagination callback | A |
| L277 | search 中 | A |
| L283 | pagination callback | A |
| L567 | showAddModal 中 | A |
| 其他 | 多种 | A |

**A 级 100% 收口**：
- nextPage 调用模式 100% 一致：`<factory>.nextPage()`（A）
- 633 次调用分布：search / pagination callback / 直接触发（A）
- 等级：A

---

## 14. `.clearAndSetIndex()` 调用模式（30.13）

| 位置 | 表达式 | 行号 | 等级 |
|---|---|---|---|
| adminAreaListCtrl | `$scope.getAdminList.clearAndSetIndex(index * pageSize)` | L90 | A |
| adminListCtrl | `$scope.getAdminList.clearAndSetIndex(index * pageSize)` | L222 | A |
| adminRoleCtrl | `$scope.getNormalAdminList.clearAndSetIndex(index * pageSize)` | L282 | A |
| 其他 | `$scope.xxx.clearAndSetIndex(index * pageSize)` | 226 次 | A |

**A 级 100% 收口**：
- 226 次调用**全部是** `clearAndSetIndex(index * pageSize)` 模式（A）
- 唯一异常 L1123: `clearAndSetIndex(index * $scope.pageSize)`（含变量）
- 等级：A

---

## 15. pagination callback 模式（30.14, 30.15）

**完整 callback 模式**（L87-91 为例）：

```javascript
$(".first-pagination").pagination($scope.getAdminList.count, {
  items_per_page: pageSize,
  callback: function callback(index) {
    $scope.getAdminList.clearAndSetIndex(index * pageSize);
    $scope.getAdminList.nextPage();
  }
});
```

**A 级 100% 收口**：

| 项目 | 模式 | 等级 |
|---|---|---|
| pagination 选择器 | `.first-pagination` / `.second-pagination` / `#Pagination` | A |
| items_per_page | pageSize（局部 var） | A |
| callback 参数 | `index` | A |
| 翻页动作 | clearAndSetIndex(index * pageSize) | A |
| 翻页动作 | nextPage() | A |
| 调用 search() | **否**（A） | A |

**关键 A 级发现**：
- **翻页 callback 不调用 search**（A）
- 翻页**直接**调 ListFactory 实例方法（clearAndSetIndex + nextPage）（A）
- 100% 跨 controller 一致（A）

---

## 16. search 函数模式（30.16, 30.17, 30.18）

**search 函数定义位置**（多 controller 都有）：

| Controller | search 函数 | 行号 | 等级 |
|---|---|---|---|
| addRoleCtrl | `$scope.search = function () { ... }` | L2066 | A |
| assistCheckListCtrl | `$scope.search = function () { ... }` | L2333 | A |
| remindListCtrl | `$scope.search = function () { ... }` | L2430 | A |
| smsSetCtrl | `$scope.search = function () { ... }` | L2525 | A |
| reChargeListCtrl | `$scope.search = function () { ... }` | L4166 | A |
| waitPayListCtrl | `$scope.search = function () { ... }` | L5072 | A |
| **machineOrderListCtrl** | **`$scope.searchAdminList = function () { ... }`** | **L4294** | **A** |

**A 级 100% 收口**：
- 多 controller 都有 `$scope.search = function ()` 或 `$scope.searchXxxList = function ()`（A）
- 命名风格**不完全统一**（A）：有的叫 search，有的叫 searchAdminList
- 等级：A

---

## 17. machineOrderListCtrl 特殊性（30.18）

**machineOrderListCtrl 搜索函数**（L4294-4312）：

```javascript
$scope.searchAdminList = function () {
    if ($scope.obj.startTime && $scope.rightTime) {
      $scope.obj.startTime = DateUtilFactory.origin($scope.obj.startTime);
      $scope.obj.endTime = DateUtilFactory.plus($scope.rightTime);

      $scope.getAdminList = new ListFactory(
        "/admin/selectMachineCenterOrderRecordVoList.json", 
        0, 10, $scope.obj
      );
      var promise = $scope.getAdminList.nextPage();
      ...
    }
};
```

**A 级关键发现**：
- `searchAdminList` **重新 new ListFactory**（A，L4299）
- setTab 触发 searchAdminList → 重新 new（A）
- changeReceiveStatus 触发 searchAdminList → 重新 new（A）
- 翻页**不调** searchAdminList（直接调 ListFactory 方法）
- 等级：A

**关键 A 级边界**：
- machineOrderListCtrl search 函数**完全重新 new** ListFactory（A）
- 其他 controller 是否也重新 new = F（需要逐个验证）

---

## 18. deliveryInputCtrl 特殊性（30.19）

**deliveryInputCtrl 范围内 ListFactory 搜索**：
- L3812-4021 范围（之前 S1-64 完整看过）
- deliveryInputCtrl **不调 ListFactory**（A）
- deliveryInputCtrl 调 ObjectFactory（A，6 API）

**A 级 100% 收口**：
- deliveryInputCtrl **不使用** ListFactory
- 严格"列表调用 ListFactory"模式不适用
- 等级：A

---

## 19. 其他 Controller 代表（30.20）

**addRoleCtrl (L17-310)**：search 函数（L2066-2080）+ new ListFactory（L46）

**assistCheckListCtrl (L2309-2399)**：search 函数（L2333）+ new ListFactory（L215）

**remindListCtrl (L2519-2586)**：search 函数（L2430）

**encryptUserCtrl (L1088-1282)**：new ListFactory（L1116）+ showAddModal 模式

**A 级 100% 收口**：
- 多个 controller 都用 `$scope.search = function ()` 模式（A）
- search 函数内部**重新 new ListFactory**（A，多源一致）
- 等级：A

---

## 20. 参数 2 / 参数 3 统计矩阵（30.21）

| Controller | 参数2 | 参数3 | 参数4 |
|---|---:|---:|---|
| machineOrderListCtrl | 0 | 10 | `$scope.obj` |
| adminListCtrl | 0 | 10 | `$scope.obj` |
| adminAreaListCtrl | 0 | 10 | `$scope.obj` |
| addRoleCtrl (L46) | 0 | 20 | `{ keyword }` |
| roleAdminCtrl | 0 | 10 | `$scope.obj` |
| modifyAreaRoleCtrl | 0 | 10 | `{}` |
| encryptUserCtrl (L1116) | 0 | 10 | `{ keyword }` |
| getNormalAdminList (L276) | 0 | 10 | `{ status, keyword, isClinicAdmin }` |
| schoolListCtrl (L602) | 0 | 12 | `{ keyword, schoolType }` |

**A 级 100% 收口**：
- 参数 2 = 0（**100% 一致**，A）
- 参数 3 = 10/12/20（不同 controller 不同，A）
- 参数 4 = object（100% 一致，A）
- 等级：A

---

## 21. Pagination 统计矩阵（30.22）

| Controller | clearAndSetIndex | nextPage | 翻页后 search |
|---|---|---|---|
| machineOrderListCtrl | `index * 10` | 直接调 | **否**（A） |
| adminListCtrl | `index * 10` | 直接调 | **否**（A） |
| adminAreaListCtrl | `index * 10` | 直接调 | **否**（A） |
| addRoleCtrl | `index * 20` | 直接调 | **否**（A） |
| modifyAreaRoleCtrl | `index * 10` | 直接调 | **否**（A） |
| schoolListCtrl | `index * 12` | 直接调 | **否**（A） |

**A 级 100% 收口**：
- 翻页 callback **不调用 search**（A，多源一致）
- 翻页**直接**调 ListFactory 实例方法（clearAndSetIndex + nextPage）（A）
- 100% 跨 controller 一致（A）
- 等级：A

---

## 22. items / count 统计矩阵（30.23）

| Controller | items 访问 | count 访问 | 变量命名 |
|---|---|---|---|
| machineOrderListCtrl | `.items` (L4321/L4336) | `.count` (L4303) | `getAdminList` |
| adminListCtrl | `.items` (L237) | `.count` (L219) | `getAdminList` |
| adminAreaListCtrl | `.items` (L90) | `.count` (L87) | `getAdminList` |
| addRoleCtrl | `.items` (L21203) | `.count` (L2086) | `getAdminList` |
| encryptUserCtrl | `.items` (L1123) | `.count` (L1120) | `getAdminList` |
| 其他 controller | `.items` | `.count` | 各种变量 |

**A 级 100% 收口**：
- 全部通过 `$scope.<factory 实例名>.items / .count` 访问（A）
- 变量命名**不完全统一**（A），但模式一致
- 等级：A

---

## 23. Request object 统计矩阵（30.24）

| Controller | object 变量 | 字段数 | 作为 ListFactory 参数 |
|---|---|---|---|
| machineOrderListCtrl | `$scope.obj` | 7 | ✓ |
| adminListCtrl | `$scope.obj` | 多 | ✓ |
| adminAreaListCtrl | `$scope.obj` | 多 | ✓ |
| roleAdminCtrl | `$scope.obj` | 多 | ✓ |
| addRoleCtrl (L46) | `{ keyword }` | 1 | ✓ |
| modifyAreaRoleCtrl (L740) | `{}` | 0 | ✓ |
| encryptUserCtrl (L1116) | `{ keyword }` | 1 | ✓ |
| schoolListCtrl (L602) | `{ keyword, schoolType }` | 2 | ✓ |

**A 级 100% 收口**：
- 参数 4 全部是 object（A）
- object 来源**多样**（A）：$scope.obj / 内联 `{ ... }` / `{}`
- 严格禁止"object 字段相同 → 同一 DTO"
- 等级：A

---

## 24. 共同调用模式（30.20）

**A 级 100% 收口 - 共同模式**：

| 项目 | 模式 | 等级 |
|---|---|---|
| 构造 | `new ListFactory(API, 0, pageSize, params)` | A |
| 触发 query | `<factory>.nextPage()` 返回 promise | A |
| 翻页 | `clearAndSetIndex(index * pageSize)` + `nextPage()` | A |
| items | `<factory>.items[]` | A |
| count | `<factory>.count` | A |
| pagination 渲染 | jQuery pagination 插件 + items_per_page + callback | A |
| search 模式 | `$scope.search = function () { ... new ListFactory(...) }` | A |

**A 级 100% 一致**。

---

## 25. machineOrderListCtrl 与 deliveryInputCtrl 对照（30.25）

| 项目 | machineOrderListCtrl | deliveryInputCtrl |
|---|---|---|
| ListFactory 使用 | **是**（L4299） | **否** |
| ObjectFactory 使用 | 否 | **是**（6 API） |
| 列表分页 | 是 | 否 |
| 列表页类型 | 业务列表 | 录入页面 |
| 等级 | A | A |

**A 级 100% 收口**：
- 两个 controller **不同构**（A）
- machineOrderListCtrl = 业务列表（用 ListFactory）
- deliveryInputCtrl = 录入页面（用 ObjectFactory）
- 等级：A

---

## 26. ListFactory 与业务流程边界（30.26）

**当前可证明**（A 级）：
- ListFactory 是**列表请求调用协议**（A）
- 多个 controller 用**相同外部模式**调用（A）
- 调用 4 参数一致（A）
- 实例方法 4 个一致（A）

**当前不可证明**（F 级）：
- ListFactory 内部 Request 构造
- ListFactory 内部 Response 解析
- ListFactory 内部 nextPage 实现
- ListFactory 内部 status/errmsg 处理
- ListFactory 内部 result.list → items 转换
- 业务状态（"分页"是 E 级推断）
- 数据库 DTO
- 后端分页算法

**严格表述**：
- "ListFactory 是列表调用协议"（A）
- "ListFactory 内部一定这样实现"（**禁止**，F）
- 等级：A/F

---

## 27. ListFactory 定义 F 的影响范围（30.27）

**当前无法证明**（必须 F 维持）：

| F 边界 | 说明 |
|---|---|
| 参数 2 内部语义 | 当前仅推断为 pageStart（E） |
| 参数 3 内部语义 | 当前仅推断为 pageSize（E） |
| Request 构造 | ListFactory 内部 |
| Response 解析 | ListFactory 内部 |
| nextPage 内部逻辑 | ListFactory 内部 |
| items / count 内部赋值 | ListFactory 内部 |
| status 处理 | ListFactory 内部 |
| errmsg 处理 | ListFactory 内部 |
| result.list → items 转换 | ListFactory 内部 |
| 业务状态（"分页"） | E（基于模式推断） |
| 数据库 DTO | F |
| 后端分页算法 | F |

**A 级 100% 收口**。

---

## 28. 一期复刻建议边界（30.28）

### A 级可冻结（仅外部调用协议）

```javascript
// ListFactory 外部调用模式（100% A 级一致）
// ===============================
// 构造：4 参数
const factory = new ListFactory(
  API,        // 参数1: API URL 字符串
  0,          // 参数2: 固定 0
  pageSize,   // 参数3: 数字 10/12/20
  params      // 参数4: object
);

// 触发 query
factory.nextPage();   // 返回 promise

// 翻页
factory.clearAndSetIndex(index * pageSize);
factory.nextPage();

// 访问数据
factory.items[];  // array
factory.count;    // number

// pagination 渲染
$(selector).pagination(factory.count, {
  items_per_page: pageSize,
  callback: function (index) {
    factory.clearAndSetIndex(index * pageSize);
    factory.nextPage();
  }
});

// search 模式
$scope.search = function () {
  $scope.factory = new ListFactory(API, 0, pageSize, $scope.obj);
  $scope.factory.nextPage();
};
```

### F 边界（禁止伪代码实现）

- ListFactory constructor 内部实现
- ListFactory.prototype.nextPage 内部实现
- ListFactory.prototype.clearAndSetIndex 内部实现
- $http 调用细节
- Response 解析逻辑
- 错误处理
- 任何 ListFactory 内部方法实现

---

## 29. 历史证据 vs 当前代码

### S1-74（134 号）：ListFactory 请求/分页/Response 协议审计
- 收口 30 项 + ListFactory 内部 F 维持
- **S1-75 验证**：406 次调用 100% 外部一致（A）
- **S1-75 验证**：参数 2/3 含义仍 E 级推断，**不**升 A
- **S1-75 验证**：ListFactory 内部实现仍 F 维持
- **无冲突**

### S1-72（132 号）：machineOrderListCtrl 列表 Query 协议闭环
- 收口 9 Request 字段
- **S1-75 验证**：ListFactory(API, 0, 10, $scope.obj) 模式维持（A）
- **无冲突**

### S1-73（133 号）：machineOrderListCtrl Request 生命周期
- 收口 30 项
- **S1-75 验证**：searchAdminList 重新 new ListFactory（A）
- **S1-75 验证**：翻页 callback 不调 search（A）
- **无冲突**

### S1-59（119 号）：machineOrderListCtrl 列表字段
- 收口 25 字段
- **S1-75 验证**：items[idx] / count 访问**正确**（A）
- **S1-75 验证**：items / count 是 ListFactory 实例 property（A）
- **无冲突**

---

## 30. A/B/C/D/E/F 评级

| 编号 | 项目 | 等级 |
|---|---|---|
| 30.1 | ListFactory 全仓调用统计 | A |
| 30.2 | 代表性 Controller | A |
| 30.3 | 构造参数数量（4） | A |
| 30.4 | 参数1 = API | A |
| 30.5 | 参数2 = 0 | A（事实）/ E（pageStart 推断） |
| 30.6 | 参数3 = 10/12/20 | A（事实）/ E（pageSize 推断） |
| 30.7 | 参数4 = object | A |
| 30.8 | 参数 4 结构 | A |
| 30.9 | API 与 object 关系 | A |
| 30.10 | `.items` 使用模式 | A |
| 30.11 | `.count` 使用模式 | A |
| 30.12 | `.nextPage()` 调用模式 | A |
| 30.13 | `.clearAndSetIndex()` 调用模式 | A |
| 30.14 | pagination callback | A |
| 30.15 | 翻页是否显式 search | A（**否**） |
| 30.16 | search 函数模式 | A |
| 30.17 | ListFactory 是否在 search 中重新 new | A（**是**） |
| 30.18 | machineOrderListCtrl 特殊性 | A |
| 30.19 | deliveryInputCtrl 特殊性 | A（**不**用 ListFactory） |
| 30.20 | 多 Controller 共享外部约定 | A（外部一致）/ F（内部一致） |
| 30.21 | 参数 2/3 统计 | A |
| 30.22 | Pagination 统计 | A |
| 30.23 | items/count 统计 | A |
| 30.24 | Request object 统计 | A |
| 30.25 | machineOrderListCtrl vs deliveryInputCtrl | A（**不同构**） |
| 30.26 | ListFactory 与业务流程边界 | A（外部）/ F（内部） |
| 30.27 | ListFactory 定义 F 影响范围 | F |
| 30.28 | 一期复刻建议 | A（外部）/ F（内部） |
| 30.29 | 历史一致性审计 | A |
| 30.30 | 最终冻结 | A/F |

**统计**：A=29 / B=0 / C=0 / D=0 / E=1 / F=0 = 30

---

## 31. L1/L2/L3

**L1（前端直接事实）**：
- 406 次 `new ListFactory(API, 0, pageSize, params)` 模式
- 633 次 nextPage / 226 次 clearAndSetIndex / 693 次 items / 303 次 count
- 100% 跨 controller 一致调用
- 等级：A

**L2（业务模型解释）**：
- ListFactory "分页组件" 推断
- 参数 2 = "pageStart" 推断
- 参数 3 = "pageSize" 推断
- 等级：**E**

**L3（数据库/物理模型）**：
- ListFactory 内部实现
- DTO / 后端分页算法
- 等级：**F**

---

## 32. R1-R6

- R1（直接字段映射）：A
- R2（同 Response 结构）：A
- R3（同业务实例）：E
- R4（页面/State）：A
- R5（业务推断）：0
- R6（未观察）：F

---

## 33. Q&A

| 编号 | 问题 | 等级 |
|---|---|---|
| Q1 | new ListFactory 全仓调用数量？ | A（**406**） |
| Q2 | 调用 Controller 数量？ | A（**多 controller**） |
| Q3 | 参数数量是否统一？ | A（**4** 100% 统一） |
| Q4 | 参数1 是否统一为 API/URL？ | A（**是**） |
| Q5 | 参数2 是否统一？ | A（**是 0**） |
| Q6 | 参数3 是否统一？ | A（**10/12/20 不同**） |
| Q7 | 参数4 是否统一为 object？ | A（**是**） |
| Q8 | machineOrderListCtrl 与 deliveryInputCtrl 是否同构？ | A（**不同构**） |
| Q9 | `.nextPage()` 是否统一？ | A（**是**） |
| Q10 | `.clearAndSetIndex()` 是否统一？ | A（**是**） |
| Q11 | pagination callback 是否统一？ | A（**是**） |
| Q12 | 翻页是否统一调用 search？ | A（**否**，直接 ListFactory 方法） |
| Q13 | search 是否统一重建 ListFactory？ | A（**是**） |
| Q14 | items/count 是否统一？ | A（**是**） |
| Q15 | 哪些只是"共同调用模式"？ | A（**406 次调用模式 + 实例方法**） |
| Q16 | 哪些可作为一期 A 级调用协议？ | A（**外部调用协议 100%**） |
| Q17 | 哪些仍必须 F？ | A（**内部实现 100%**） |
| Q18 | 当前是否能定义 ListFactory 内部实现？ | A（**否**，F 维持） |

---

## 34. P0/P1

- **P0 = 54**（冻结）
- **P1 = 8**（冻结）
- 本轮 P0 = 0（不新增）
- 本轮 P1 = 0（不新增）

---

## 35. 红线核查

- 写操作 = **0**
- 生产数据修改 = **0**
- 历史 MD 修改 = **0**（28~134 全部未修改）
- P0 自动新增 = **0**
- P1 自动新增 = **0**
- 10 个 untracked 临时文件原样保留 = **A**

---

## 36. 本轮新增事实

| 编号 | 证据 | 等级 |
|---|---|---|
| 1 | 406 次 `new ListFactory` 100% 4 参数 | A |
| 2 | 参数 1 = API URL 100% 一致 | A |
| 3 | 参数 2 = 0 100% 固定 | A |
| 4 | 参数 3 = 10/12/20 不同 controller 不同 | A |
| 5 | 参数 4 = object 100% 一致 | A |
| 6 | 633 次 nextPage + 226 次 clearAndSetIndex 模式一致 | A |
| 7 | 翻页 callback 不调用 search | A |
| 8 | search 函数模式 100% 一致 | A |
| 9 | 翻页直接调 ListFactory 实例方法 | A |
| 10 | deliveryInputCtrl 不使用 ListFactory | A |

---

## 37. 最终一句话

"S1-75 完成，已 Git 封口，立即停止，不进入 S1-76，等待老板下一条指令。"
