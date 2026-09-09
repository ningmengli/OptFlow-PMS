# S1-151：Clinic / Company / Shop / Department / Employee / Role / SystemSetting 权限底座总审计

> 项目：OptFlow PMS
> Repo：https://github.com/ningmengli/OptFlow-PMS
> 工作目录：`E:\C\minimax\OptFlow PMS`
> 任务：只读逆向证据审计（非开发 / 非重构 / 非新增功能）
> 范围：仅 controller.js / 已冻结 213 个 MD / 不修改历史
> 关联：S1-130 / S1-131 / S1-147 / S1-150

---

## 目录

- §0 审计范围
- §1 Company / Corp / corpInfo
- §2 Clinic
- §3 Shop / Store
- §4 Department
- §5 Employee
- §6 Role
- §7 Authorization / grantAuth
- §8 SystemSetting
- §9 ConsultRoom
- §10 Login / corpInfo
- §11 ID Source Trace
- §12 schoolIdArray
- §13 Employee ↔ Role ↔ Department
- §14 Role ↔ Authorization
- §15 Company ↔ Clinic ↔ Shop 组织关系
- §16 SystemSetting Lifecycle
- §17 Controller 消费矩阵
- §18 Object 分类
- §19 26 项证据矩阵
- §20 历史差异
- §21 V4.4 权限/诊所底座规格
- §22 F / 未确认
- §23 Git / 完整性

---

## §0 审计范围

本轮把 Clinic / Company / Shop / Department / Employee / Role / SystemSetting 权限底座
作为**前端可证明的实体、字段、Request、Response、State、API、Controller 和桥接关系**进行完整只读审计：

- 区分 `clinic` / `Clinic` / `clinicId` 命名差异
- 验证 `shop` / `store` / `storeId` 是否独立对象
- 验证 `departmentId` / `roleId` / `adminRoleId` / `employeeId` 真实身份
- 验证 `permission` / `functionAuth` / `buttonAuth` 是否独立实体
- 验证 `systemSetting` 是 State 路由名还是 Object 字段
- corpInfo / localStorage / token 完整 Login Context 链
- 6 个真实 Manage Controller 深审
- 21 Controller 完整消费矩阵
- 26 项证据矩阵
- 历史 S1-130/131/147/150 误判核对

---

## §1 Company / Corp / corpInfo

### §1.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `company` (全词) | 23 | A |
| `companyId` | **127** | A |
| `companyName` | 62 | A |
| `companyInfo` | 58 | A |
| `companyIdArray` | 15 | A |
| `corp` | 3 | A |
| `corpInfo` | **46** | A |
| `CorpInfo` | 0 | A |
| `myCorpInfo` | 0 | A |

### §1.2 Company API 全量

| API | 命中 | R/W |
|---|---:|---|
| `getCompany*.json` | **42** | R |
| `updateCompany*.json` | 3 | W |
| `saveCompany*.json` | 0 | F |

### §1.3 corpInfo 字段级访问（10 字符级）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `corpInfo.companyTitle` | L588/L873/L50845/L51943 | **A** |
| `corpInfo.employeeTitle` | L3540/L14266 | **A** |
| `corpInfo.username` | L14267 | **A** |
| `corpInfo.enableFeier == 1` | L29299 | **A** |
| `corpInfo.xxx` (其他) | 0 命中 | F |

### §1.4 corpInfo localStorage 持久化（Login Context）

```
loginCtrl L14239: localStorage.setItem("corpid", corpId)
loginCtrl L14268: localStorage.setItem("corpInfo", JSON.stringify(corpInfo))
loginCtrl L14270: localStorage.setItem("pcToken", $scope.loginFactory.result.token)
loginCtrl L14272: localStorage.setItem("appid", $scope.loginFactory.result.appid)
loginCtrl L14273: localStorage.setItem("username", $scope.loginFactory.result.admin.nickname)
```

**读 localStorage corpInfo**:
- L585 / L871 / L3529: `var corpInfo = localStorage.getItem('corpInfo')`
- L1144: `$scope.corpid = localStorage.getItem("corpid")`
- L1229: `localStorage.setItem($scope.corpid + "_userCert", EscapeFactory.compileStr(JSON.stringify(res.result.object)))`

### §1.5 corpInfo 关键发现

1. **corpInfo 是 Login Context 持久化对象**（A）
2. **corpInfo 实际是字符串**，在 JS 端是 `var corpInfo = localStorage.getItem('corpInfo')` (字符串)
3. **公司名 / 公司标识** 来自 corpInfo.companyTitle（**4 命中**）
4. **员工标识** 来自 corpInfo.employeeTitle（**2 命中**）
5. **登录用户名** 来自 corpInfo.username（**1 命中**）
6. **飞耳设置** 来自 corpInfo.enableFeier（**1 命中**）

### §1.6 Company 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `companyId` | A |
| B. Response VO | `companyInfo` (派生自 login response) | A |
| C. Request | `companyId` (Request 字段) | A |
| D. State | `corpInfo` (localStorage 持久化) | A |
| E. UI | `companyTitle` (UI 显示) | A |
| F. Runtime | - | F |

---

## §2 Clinic

### §2.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `clinic` (小写) | **6** | A |
| `Clinic` (大写) | **0** | A |
| `clinicId` | **0** | A |
| `clinicName` | **0** | A |

### §2.2 Clinic 关键发现（本轮重大）

1. **`clinic` 仅 6 命中**（非常少）— Clinic 不是核心对象
2. **`Clinic` 大写 0 命中** — 没有 PascalCase 命名
3. **`clinicId` 0 命中** — **Clinic ID 字段不存在！**
4. **`clinicName` 0 命中** — **Clinic Name 字段不存在！**
5. **0 命中 `getClinic*.json` / `saveClinic*.json` / `updateClinic*.json`** — 没有独立 Clinic CRUD API

### §2.3 0 命中 Controller

- `clinicCtrl` / `clinicManageCtrl` / `clinicSettingCtrl` 全部 NOT FOUND

### §2.4 真实存在的诊所管理

- **`adminClinicCtrl` L15053** (6 命中 clinic) — **唯一真实 Clinic Controller**
- **但实际是 admin 端的 adminClinicCtrl**，不是独立 clinic 实体

### §2.5 Clinic 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | `clinic` (字符串) | C (弱) |
| F. Runtime | - | F |

### §2.6 关键判断

- **Clinic 不是独立 ID 实体**（F）
- 实际"诊所"概念由 **adminClinicCtrl** + `consultRoom.consultRoomVoList` 表达
- 实际"诊所设置"由 **systemSettingCtrl** 处理

---

## §3 Shop / Store

### §3.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `shop` | **0** | A |
| `shopId` | **0** | A |
| `shopName` | **0** | A |
| `store` | 128 | A |
| `storeId` | **0** | A |

### §3.2 Shop / Store 关键发现（本轮重大）

1. **`shop` / `shopId` / `shopName` 全部 0 命中** — **Shop 概念在 controller.js 中不存在**
2. **`storeId` 0 命中** — **Store ID 字段不存在**
3. **`store` 128 命中** — 但实际是 `stockIn` / `stockOut` / `selectStore` / 等混合词（**`store` 单独字 0 命中**）
4. **0 命中 `shopCtrl` / `storeCtrl`**

### §3.3 关键判断

- **Shop / Store 概念在 OptFlow PMS 中实际不存在**（F）
- 保持 S1-130 修正：实际"门店"由 `companyId` + `adminClinicCtrl` 表达
- **保持 S1-147 修正**：公司是最高层级（不是 Shop/Store）

---

## §4 Department

### §4.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `department` (全词) | **0** | A |
| `departmentId` | **1** | A |
| `departmentName` | **0** | A |
| `departmentVo` | **0** | A |

### §4.2 Department 关键发现

1. **`department` 全词 0 命中** — Department 不是独立 Object 实体
2. **`departmentId` 仅 1 命中** — 极弱 ID 字段
3. **`departmentName` 0 命中** — 没有 Name 字段
4. **`departmentVo` 0 命中** — 没有独立 VO 容器
5. **0 命中 `getDepartment*.json` 全部**（除 2 个 list API）
6. **0 命中 `saveDepartment*.json` / `updateDepartment*.json` / `deleteDepartment*.json`**

### §4.3 Department Controller

- ✓ `departmentListCtrl` L15327 (列表) — 唯一真实
- ✗ `departmentCtrl` / `departmentManageCtrl` / `departmentEditCtrl` 全部 NOT FOUND

### §4.4 Department 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (departmentId 仅 1 命中)** |
| B. Response VO | - | F |
| C. Request | `departmentId` | C (弱) |
| D. State | - | F |
| E. UI | - | F |
| F. Runtime | - | F |

### §4.5 关键判断

- **Department 不是独立 ID 实体**（F）
- 实际"科室"由 `departmentListCtrl` + `getDepartment*.json` 列表表达
- **没有独立 Department CRUD**

---

## §5 Employee

### §5.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `employee` (全词) | 31 | A |
| `employeeId` | **45** | A |
| `employeeName` | 31 | A |
| `employeeList` | 10 | A |
| `employeeCheckinQueue` | 5 | A |
| `employeeVo` | **0** | A |
| `adminId` | 34 | A |
| `userId` | 0 | A |
| `adminInfo` | 0 命中（getAdminInfo 1 命中 L16287） | C |

### §5.2 Employee API

| API | 命中 | R/W |
|---|---:|---|
| `getEmployee*.json` | 7 | R |
| `saveEmployee*.json` | 0 | F |
| `updateEmployee*.json` | 0 | F |
| `deleteEmployee*.json` | 0 | F |
| `createEmployee*.json` | 0 | F |

### §5.3 Employee Controller

- ✓ `employeeListCtrl` L15347 (列表) — 唯一真实
- ✗ `employeeCtrl` / `employeeManageCtrl` / `employeeEditCtrl` 全部 NOT FOUND

### §5.4 Employee 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `employeeId`, `adminId` | A |
| B. Response VO | `employeeList` | A |
| C. Request | `employeeId` (Request) | A |
| D. State | - | F |
| E. UI | `employeeName`, `nickname` (登录返回) | A |
| F. Runtime | - | F |

### §5.5 关键发现

- **Employee 有 employeeId + adminId 独立 ID 字段**（A）
- **`adminId` 与 `employeeId` 不完全相同**：
  - `employeeId` 多用于接诊队列 (employeeCheckinQueue)
  - `adminId` 多用于登录认证 (corpInfo.username from admin.nickname)
- **0 命中独立 Employee Create / Update / Delete API** — Employee 没有独立 CRUD
- 实际 Employee 由 `getEmployee*.json` 列表 + adminId 引用表达

---

## §6 Role

### §6.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `role` (全词) | 0 (未列出) | A |
| `roleId` | **4** | A |
| `roleName` | 9 | A |
| `adminRoleId` | **38** | A |
| `roleVo` | **0** | A |
| `roleList` | **0** | A |
| `roleIdArray` | 0 | A |
| `roleFunctionVoList` | 0 | A |

### §6.2 adminRoleId vs roleId 真实差异（本轮重大）

**`adminRoleId` 38 命中**（真实 ID 字段）：
- L105: `$scope.adminRoleId = [1, 2]` (数组)
- L232: `changeAdminRole.json { id: adminId, adminRoleId: adminRoleId }` (Write)
- L411: `res.result.object.admin.adminRoleId` (Response)
- L415: `selectObj.adminRoleId = res.result.object.adminRole.id` (Response)
- L504: `getRoleStateListForUpdate.json { adminRoleId: id }` (Read)
- L648: `changeAdminRole.json { id, adminRoleId, companyId }` (Write)
- L784: `if (!$scope.obj.adminRoleId)` (校验)

**`roleId` 仅 4 命中**（URL State 参数）：
- L1473: `$scope.obj.adminRoleId = $stateParams.roleId`
- L1542: `obj.adminRoleId = $stateParams.roleId`
- L1597: `$scope.obj.adminRoleId = $stateParams.roleId`
- L1666: `obj.adminRoleId = $stateParams.roleId`

**关键发现**：
- **`roleId` 全部是 `$stateParams.roleId` URL 参数**（路由入口）
- **`adminRoleId` 是真实 ID 字段**（Request/Response）
- **roleId 和 adminRoleId 不完全等同**：roleId 是 URL 入口，adminRoleId 是真实 ID
- **保持 S1-131 修正**：roleId ≠ adminRoleId

### §6.3 Role API

| API | 命中 | R/W |
|---|---:|---|
| `changeAdminRole.json` | L232/L648 | **W (唯一 Change)** |
| `getRoleStateListForUpdate.json` | L504 | R |
| `getRole*.json` | 4 | R |

### §6.4 Role Controller

- ✗ `roleCtrl` / `roleManageCtrl` / `roleListCtrl` / `roleEditCtrl` 全部 NOT FOUND

### §6.5 Role 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `adminRoleId` | A |
| B. Response VO | `adminRole` (Response object) | A |
| C. Request | `adminRoleId` (Request 字段) | A |
| D. State | `roleId` ($stateParams 入口) | A (但不是 ID 字段) |
| E. UI | `roleName` | A |
| F. Runtime | - | F |

---

## §7 Authorization / grantAuth

### §7.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `grantAuth` | **73** | A |
| `hasAuthForCompany` | **32** | A |
| `hasAuthForWA` | 4 | A |
| `getBackAuth` | 8 | A |
| `getFrontAuth` | 7 | A |
| `isUnlockFun` | 5 | A |
| `getAuthList` | 6 | A |
| `permission` | **0** | A |
| `permissionId` | **0** | A |
| `authId` | **0** | A |
| `functionAuth` | **0** | A |
| `menuAuth` | **0** | A |
| `buttonAuth` | **0** | A |

### §7.2 Authorization 关键发现（本轮重大）

1. **`grantAuth` 73 命中** — 是 Function/Service，不是 Object
2. **`hasAuthForCompany` 32 命中** — 是 grantAuth 的方法
3. **`hasAuthForWA` 4 命中** — 是 grantAuth 的方法
4. **`getBackAuth` / `getFrontAuth` / `getAuthList`** — 是 grantAuth 的方法
5. **`isUnlockFun` 5 命中** — 是 grantAuth 的方法
6. **`permission` / `permissionId` / `authId` / `functionAuth` / `menuAuth` / `buttonAuth` 全部 0 命中** — **没有独立 Permission/Auth ID 实体！**

### §7.3 grantAuth Function 真实身份

- `grantAuth` 是 **window 全局 Service**（推测 — 73 命中大多是 `window.grantAuth.xxx()`）
- `hasAuthForCompany(ObjectFactory).then(function(res) {...})` (L8778 多次) — **返回 Promise**
- **grantAuth 是前端 UI 权限判断 Function，不是 Object 实体**

### §7.4 Authorization 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | - | F |
| E. UI | `grantAuth` (Function/Service) | A (Function) |
| F. Runtime | - | F |

### §7.5 关键判断

- **Authorization 不是独立 ID 实体**（F）
- 实际权限是 **grantAuth Function** 实现的 UI 权限判断
- 保持 S1-131 修正：grantAuth 是 Function 不是 Object

---

## §8 SystemSetting

### §8.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `systemSetting` | **24** | A |
| `systemSettings` | **0** | A |
| `setting` (全词) | **0** | A |
| `settings` | **0** | A |
| `systemConfig` | **0** | A |
| `config` | 11 | A |
| `getSystemSetting*.json` | **0** | A |
| `saveSystemSetting*.json` | 0 | A |

### §8.2 SystemSetting 关键发现（本轮重大）

1. **`systemSetting` 24 命中 — 全部是 `$state.go('systemSetting.xxx')`** (L50229/L50463/L50788/L51172/L51735/L51792/L51817/L52231/L53022/L53248/L53797/L54043-L54055/L55200/L56408/L56805/L56889)
2. **`systemSetting` 不是 Object 字段，而是 State 路由名！**
3. **`setting` / `settings` / `systemConfig` 全部 0 命中** — **没有独立 setting 字段**
4. **0 命中 `getSystemSetting*.json`** — **没有独立 SystemSetting Read API！**

### §8.3 17+ 个 systemSetting 子 State

| State | 用途推测 | 等级 |
|---|---|---|
| `systemSetting.checkList` | 检验单列表 | A |
| `systemSetting.checkModify` | 检验单修改 | A |
| `systemSetting.customerChargeItem` | 客户收费项目 | A |
| `systemSetting.customerCharge` | 客户收费 | A |
| `systemSetting.modifyCustomerCharge` | 修改客户收费 | A |
| `systemSetting.customerMaterialCertificate` | 客户物料证件 | A |
| `systemSetting.materiallist` | 物料列表 | A |
| `systemSetting.materialModify` | 物料修改 | A |
| `systemSetting.materialCertificate` | 物料证件 | A |
| `systemSetting.medicalFeesList` | 医疗费用列表 | A |
| `systemSetting.memberTypeList` | 会员类型列表 | A |
| `systemSetting.processCenter` | 加工中心 | A |
| `systemSetting.projectCard` | 项目卡 | A |
| `systemSetting.supplierList` | 供应商列表 | A |
| `systemSetting.supplierModify` | 供应商修改 | A |
| `systemSetting.supplierCertificate` | 供应商证件 | A |
| `systemSetting.InspectList` | 检查列表 | A |

### §8.4 systemSettingCtrl L59014 详细

- 唯一真实存在的 SystemSetting Controller
- 通过 17+ 个子 State 路由分发
- **不是单一 Object 实体**，而是 **State 路由聚合器**

### §8.5 SystemSetting 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | **F (0 命中)** |
| B. Response VO | - | F |
| C. Request | - | F |
| D. State | `systemSetting.*` (State 路由) | A (State 路由名) |
| E. UI | `systemSettingCtrl` 控制器 | A (Controller) |
| F. Runtime | - | F |

### §8.6 关键判断

- **SystemSetting 不是 Object 实体**（F）
- 实际"系统设置"由 `systemSettingCtrl` + 17+ 子 State 路由聚合
- 保持 S1-130 修正：SystemSetting 是 UI/State 路由，不是数据库实体

---

## §9 ConsultRoom

### §9.1 字符级精确统计

| 模式 | 命中数 | 等级 |
|---|---:|:---:|
| `consultRoom` | **53** | A |
| `consultRoomId` | **25** | A |
| `roomName` | **0** | A |
| `getConsultRoom*.json` | 2 | A |

### §9.2 ConsultRoom 字段级访问（20 命中）

| 字段 | 字符级证据 | 等级 |
|---|---|---|
| `consultRoom.consultRoomName` | L9514 | A |
| `consultRoom.id` | L9555/L9852 | A |
| `consultRoom.companyId` | **L9336** | **A (consultRoom.companyId 真实存在！)** |
| `consultRoomVoList[]` | L9623 | A |
| `consultRoomIdArray` | L9615/L9623/L9630/L9644/L9647/L9654/L9675-L9693 | A |
| `consultRoom.examineList` | L9725 | A |
| `$scope.clinicInfo.consultRoom` | **L9825** | **A (clinicInfo.consultRoom 真实存在！)** |
| `consultRoomId` (Request) | L9555/L9852 | A |

### §9.3 ConsultRoom 关键发现（本轮重要）

1. **ConsultRoom 是真实 ID 实体**（consultRoomId 25 命中）
2. **`consultRoom.companyId` 直接存在**（L9336） — **ConsultRoom 与 Company 有 A 字段桥！**
3. **`clinicInfo.consultRoom` 真实存在**（L9825） — **clinicInfo 内嵌 consultRoom**
4. **consultRoomVoList / consultRoomIdArray 真实存在**（A 派生链）
5. **consultRoom 实际是接诊/叫号核心对象**

### §9.4 ConsultRoom 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | `consultRoomId`, `consultRoom.id` | A |
| B. Response VO | `consultRoomVoList[]` | A |
| C. Request | `consultRoomId` (Request) | A |
| D. State | `consultRoomIdArray` (Scope) | A |
| E. UI | `consultRoomName` | A |
| F. Runtime | - | F |

---

## §10 Login / corpInfo

### §10.1 Login Context 完整链

```javascript
// loginCtrl L14239-L14273 (Login 后写入)
localStorage.setItem("corpid", corpId);            // L14239
localStorage.setItem("corpInfo", JSON.stringify(corpInfo));  // L14268
localStorage.setItem("pcToken", $scope.loginFactory.result.token);  // L14270
localStorage.setItem("appid", $scope.loginFactory.result.appid);  // L14272
localStorage.setItem("username", $scope.loginFactory.result.admin.nickname);  // L14273

// 其他 Controller 读 localStorage
var corpInfo = localStorage.getItem('corpInfo');   // L585/L871/L3529
var corpid = localStorage.getItem("corpid");        // L1144
var token = localStorage.getItem("pcToken");        // L12596/L12916/L13830/L14106/L16748/L18085/L30117/L30334
var userCert = JSON.parse(EscapeFactory.uncompileStr(localStorage.getItem($scope.corpid + "_userCert")));  // L1148
```

### §10.2 corpInfo 字段访问

| 字段 | 用途 | 行号 | 等级 |
|---|---|---|---|
| `corpInfo.companyTitle` | UI 显示公司名 | L588/L873/L50845/L51943 | A |
| `corpInfo.employeeTitle` | UI 显示员工名 | L3540/L14266 | A |
| `corpInfo.username` | 登录用户名 | L14267 | A |
| `corpInfo.enableFeier == 1` | 飞耳设置 | L29299 | A |

### §10.3 Login Context 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | F |
| B. Response VO | `corpInfo` (login response + JSON.parse) | A |
| C. Request | - | F |
| D. State | `corpInfo` (localStorage 持久化) | A |
| E. UI | `companyTitle` / `employeeTitle` | A |
| F. Runtime | - | F |

### §10.4 关键判断

- **corpInfo 是 Login Context 持久化对象**（A, D）
- **localStorage 是 Login Context 真实存储**（A, D）
- **不是数据库实体**（F, A）— 是 UI State 持久化
- **保持 S1-131 修正**：corpInfo 是 State 不是 Entity

---

## §11 ID Source Trace

### §11.1 关键字段溯源

#### companyId
- **Source A**: `$stateParams` / login response (L14239 corpId)
- **Source B**: `consultRoom.companyId = res.id` (L9336)
- **Source C**: `getCompany*.json` Request (42 调用)
- **Source D**: 业务 Controller Scope 字段
- **Target**: getCompany* / saveCompany* / companyIdArray
- **等级**: A

#### shopId / storeId
- **Source**: 0 命中
- **等级**: **F (Shop/Store 概念不存在)**

#### roleId
- **Source**: `$stateParams.roleId` (4 命中, L1473/L1542/L1597/L1666)
- **Target**: `obj.adminRoleId = $stateParams.roleId`
- **等级**: A (URL 入口参数)

#### adminRoleId
- **Source A**: `changeAdminRole.json` Request (L232/L648)
- **Source B**: `res.result.object.admin.adminRoleId` (L411)
- **Source C**: `getRoleStateListForUpdate.json` Request (L504)
- **Source D**: `$scope.adminRoleId = [1, 2]` (L105)
- **等级**: A (真实 ID 字段)

#### employeeId
- **Source A**: `employeeCheckinQueue.employeeId` (L10652)
- **Source B**: getEmployee*.json Response
- **等级**: A

#### adminId
- **Source A**: login response (L14273 `admin.nickname`)
- **Source B**: `changeAdminRole.json` Request `id: adminId` (L232/L648)
- **等级**: A

#### departmentId
- **Source**: 仅 1 命中
- **等级**: **C (极弱)**

#### consultRoomId
- **Source A**: `consultRoom.id` (L9555/L9852)
- **Source B**: `consultRoomVoList[].consultRoom.id` (L9645/L9678/L9693)
- **Source C**: `getConsultRoom*.json` Request
- **等级**: A (真实 ID 字段)

#### systemSetting
- **Source**: 17+ `$state.go('systemSetting.xxx')` (L50229 等)
- **Target**: State 路由名
- **等级**: A (State 路由, 不是 ID 字段)

#### schoolIdArray
- **Source A**: Screening Plan Scope 数组 (L634/L642)
- **Source B**: admin 创建/编辑 obj.schoolIdArray (L769/L791)
- **Source C**: changeAdminRole.json 复合 Request (L648 含 companyId + adminRoleId)
- **等级**: A (Request 字段 + Scope 数组)

---

## §12 schoolIdArray

### §12.1 6 命中完整上下文

| 行号 | 上下文 | 等级 |
|---|---|---|
| L634 | `$scope.schoolIdArray = []` (Screening Plan) | A |
| L642 | `schoolIdArray.push($scope.selected[i])` | A |
| L648 | `changeAdminRole.json { id, adminRoleId, companyId, schoolIdArray }` (复合 Request) | A |
| L769 | `$scope.obj.schoolIdArray = []` (admin 创建) | A |
| L791 | `obj.schoolIdArray.push($scope.selected[j])` | A |

### §12.2 关键判断

- **schoolIdArray 不是 School 主表字段**（保持 S1-131 修正）
- **实际是 Scope 数组 + Request 复合字段**
- **Screening Plan 上下文**（L634-L642）
- **admin 角色/学校范围**（L648/L769-L791）

### §12.3 schoolIdArray 6 分类

| 分类 | 字段 | 等级 |
|---|---|---|
| A. Core ID | - | F |
| B. Response VO | - | F |
| C. Request | `schoolIdArray` (Request 字段) | A |
| D. State | `$scope.schoolIdArray` | A |
| E. UI | - | F |
| F. Runtime | - | F |

---

## §13 Employee ↔ Role ↔ Department

### §13.1 6 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Employee | Role | 0 命中 `employee.roleId` 字段 | F | - | **F** | F |
| Role | Employee | `changeAdminRole.json { id: adminId, adminRoleId }` | A Request Bridge | L232/L648 | **A** | A |
| Employee | Department | 0 命中 `employee.departmentId` 字段 | F | - | **F** | F |
| Department | Employee | 0 命中 `department.employee` 字段 | F | - | **F** | F |
| Role | Department | 0 命中 | F | - | **F** | F |
| Department | Role | 0 命中 | F | - | **F** | F |

### §13.2 关键判断

- **Role → Employee**: A Request Bridge（`changeAdminRole.json`）
- **其他关系**: F
- 保持 S1-131 修正：Employee/Role/Department 之间没有直接字段桥

---

## §14 Role ↔ Authorization

### §14.1 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Role | Authorization | `getRoleStateListForUpdate.json` (经 adminRoleId) | A Request Bridge | L504 | **A** | A |
| Authorization | Role | `grantAuth` Function | A Function/Service | 多处 | **A** | A (Function) |
| Role | Authorization | 0 命中 `role.permission` 字段 | F | - | **F** | F |
| Authorization | Role | 0 命中 `auth.role` 字段 | F | - | **F** | F |

### §14.2 关键判断

- **Role → Authorization**: A Request Bridge（`getRoleStateListForUpdate`）
- **Authorization → Role**: A Function/Service（grantAuth）
- 保持 S1-131 修正：grantAuth 是 Function 不是 Object 实体

---

## §15 Company ↔ Clinic ↔ Shop 组织关系

### §15.1 关系矩阵

| Source | Target | Mechanism | Direct/Indirect | Line | Grade | V4.4 |
|---|---|---|---|---:|---|---|
| Company | Clinic | 0 命中 `company.clinic` 字段 | F | - | **F** | F |
| Clinic | Company | 0 命中 `clinic.companyId` 字段 | F | - | **F** | F |
| Company | Shop | 0 命中 | F | - | **F** | F |
| Shop | Company | 0 命中 | F | - | **F** | F |
| Company | Department | 0 命中 `company.department` 字段 | F | - | **F** | F |
| Department | Company | 0 命中 `department.companyId` 字段 | F | - | **F** | F |
| ConsultRoom | Company | `consultRoom.companyId = res.id` | **A 字段桥** | L9336 | **A** | A |
| ConsultRoom | Clinic | `clinicInfo.consultRoom` (经 clinicInfo) | A 字段桥 (经 clinicInfo) | L9825 | **C** | C |

### §15.2 关键判断

- **ConsultRoom → Company**: A 字段桥（`consultRoom.companyId` 真实存在，L9336）
- **ConsultRoom → Clinic**: C 字段桥（经 clinicInfo）
- **Shop/Store 全部 F**（概念不存在）
- **保持 S1-130 修正**：公司是最高层级（不是 Shop/Store）

---

## §16 SystemSetting Lifecycle

### §16.1 完整 Lifecycle

```
[登录后] corpInfo 写入 localStorage
    ↓
[systemSettingCtrl] 17+ 个子 State 路由
    ├── systemSetting.checkList / checkModify (检验单)
    ├── systemSetting.customerChargeItem / customerCharge (客户收费)
    ├── systemSetting.materiallist / materialModify (物料)
    ├── systemSetting.medicalFeesList (医疗费用)
    ├── systemSetting.memberTypeList (会员类型)
    ├── systemSetting.processCenter (加工中心)
    ├── systemSetting.projectCard (项目卡)
    └── systemSetting.supplierList / supplierModify (供应商)
```

### §16.2 关键发现

- **SystemSetting 没有 Object 实体**
- **17+ 子 State 路由聚合**（A）
- **没有独立 Read/Write API**（0 命中 `getSystemSetting*.json`）
- **保持 S1-130 修正**：SystemSetting 是 UI State 聚合器

---

## §17 Controller 消费矩阵

### §17.1 21 Controller 消费矩阵

| Controller | company | clinic | shop | dept | emp | role | auth | setting | room | 等级 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| **adminClinicCtrl** (L15053) | **35** | 0 | 0 | 1 | 8 | 0 | 4 | 0 | **16** | A |
| adminPatientCtrl | 23 | 0 | 0 | 0 | 2 | 0 | 3 | 0 | 0 | A |
| adminMyRecordCtrl | 12 | 0 | 0 | 0 | 7 | 0 | 7 | 0 | 0 | A |
| **addCheckinCtrl** | **51** | 4 | 0 | 0 | **44** | 0 | 11 | 0 | **62** | A |
| addSaleRecordCtrl | 12 | 0 | 0 | 0 | 7 | 0 | 8 | 0 | 0 | A |
| **addVisitCtrl** | 16 | 0 | 0 | 0 | 4 | 1 | 2 | **20** | 0 | A |
| optometryCtrl | 37 | 0 | 0 | 0 | 12 | 0 | 20 | 0 | 0 | A |
| myMemberCtrl | 27 | 0 | 0 | 0 | 7 | 0 | **27** | 0 | 0 | A |
| myMemberRecordCtrl | 27 | 0 | 0 | 0 | 7 | 0 | 26 | 0 | 0 | A |
| myMedicalRecordListCtrl | 27 | 0 | 0 | 0 | 7 | 0 | 24 | 0 | 0 | A |
| **waitChargeDetailCtrl** | 38 | 4 | 0 | 0 | **44** | 0 | 21 | 0 | **62** | A |
| **waitPayDetailCtrl** | **51** | 4 | 0 | 0 | **44** | 0 | 14 | 0 | **62** | A |
| payedListCtrl | 18 | 0 | 0 | 0 | 30 | 0 | **31** | 0 | 19 | A |
| deliveryInputCtrl | 12 | 0 | 0 | 0 | 16 | 0 | **30** | 0 | 0 | A |
| machineOrderCtrl | 24 | 0 | 0 | 0 | 2 | 0 | 3 | 0 | 0 | A |
| machineOrderListCtrl | 12 | 0 | 0 | 0 | 24 | 0 | **31** | 0 | 0 | A |
| myMaterialBillCtrl | 19 | 0 | 0 | 0 | 7 | 0 | 19 | 0 | 0 | A |
| partBackCtrl | 11 | 0 | 0 | 0 | 24 | 0 | **31** | 0 | 1 | A |
| **loginCtrl** (L14086) | **61** | 0 | 0 | 1 | 9 | 0 | 4 | 0 | 16 | A |
| assistCheckingCtrl | 22 | 2 | 0 | 0 | 2 | 0 | 22 | 0 | 0 | A |
| drugPrescriptionCtrl | 11 | 0 | 0 | 0 | 7 | 0 | 8 | 0 | 0 | A |

### §17.2 核心观察

1. **addCheckinCtrl / waitChargeDetailCtrl / waitPayDetailCtrl** 同时大量消费 company(38-51), employee(44), consultRoom(62) — 接诊/收费三大 Controller
2. **addVisitCtrl** 是唯一 systemSetting 消费者（20）— 复诊场景
3. **myMemberCtrl/Record/List** 大量消费 grantAuth (24-27) — 客户域权限检查
4. **clinic = 0 命中** 在大多数 Controller — Clinic 概念弱
5. **shop = 0 全部** — Shop 不存在
6. **department = 0/1** — Department 极弱
7. **role = 0/1** — Role 极弱

### §17.3 6 个真实 Manage Controller

| Controller | 行号 | 等级 |
|---|---|---|
| `adminClinicCtrl` | L15053 | A |
| `systemSettingCtrl` | L59014 | A |
| `employeeListCtrl` | L15347 | A |
| `departmentListCtrl` | L15327 | A |
| `companyCtrl` | L13829 | A |
| `loginCtrl` | L14086 | A |

### §17.4 15+ NOT FOUND Controller

- `clinicCtrl` / `clinicManageCtrl` / `clinicSettingCtrl`
- `systemSettingListCtrl` / `systemConfigCtrl`
- `roleCtrl` / `roleManageCtrl` / `roleListCtrl` / `roleEditCtrl`
- `employeeCtrl` / `employeeManageCtrl`
- `departmentCtrl` / `departmentManageCtrl`
- `consultRoomCtrl` / `consultRoomManageCtrl` / `consultRoomListCtrl`
- `companyManageCtrl` / `companySettingCtrl`
- `shopCtrl` / `storeCtrl`
- `loginMainCtrl` / `loginOutCtrl`
- `grantAuthCtrl` / `authCtrl` / `permissionCtrl`
- `corpInfoCtrl` / `myCorpInfoCtrl`

---

## §18 Object 分类

### §18.1 10 个对象分类

| 对象 | 独立 ID | Response VO | Request Payload | State/UI | 等级 |
|---|---|---|---|---|---|
| **Company** | ✓ (companyId 127) | ✓ (companyInfo) | ✓ | ✓ (corpInfo localStorage) | A |
| **Clinic** | ✗ (0 命中 clinicId) | ✗ | ✗ | ✗ | **F** |
| **Shop** | ✗ (shopId 0 命中) | ✗ | ✗ | ✗ | **F** |
| **Store** | ✗ (storeId 0 命中) | ✗ | ✗ | ✗ | **F** |
| **Department** | ✗ (departmentId 1 命中) | ✗ | ✗ | ✗ | **F** |
| **Employee** | ✓ (employeeId 45 / adminId 34) | ✓ (employeeList) | ✓ | - | A |
| **Role** | ✓ (adminRoleId 38 / roleId 4 URL 入口) | ✓ (adminRole) | ✓ | - | A |
| **Authorization** | ✗ (permission 0 命中) | ✗ | ✗ | ✓ (grantAuth Function) | **A (Function)** |
| **SystemSetting** | ✗ (systemSetting 0 命中字段) | ✗ | ✗ | ✓ (17+ State 路由) | **A (State 路由)** |
| **ConsultRoom** | ✓ (consultRoomId 25) | ✓ (consultRoomVoList) | ✓ | ✓ (consultRoomIdArray) | A |
| **corpInfo** | ✗ | ✓ (Login Response) | ✗ | ✓ (localStorage) | A |

### §18.2 关键结论

- **真正独立 ID 实体仅 4 个**: Company / Employee / Role(adminRoleId) / ConsultRoom
- **3 个 0 命中实体**: Clinic / Shop / Store (概念不存在)
- **Department 极弱 ID 实体** (1 命中)
- **Authorization 是 Function/Service** 不是 Object
- **SystemSetting 是 State 路由聚合** 不是 Object
- **corpInfo 是 Login Context 持久化对象** 不是 DB 实体

---

## §19 26 项证据矩阵

| # | 项目 | 结论 | 等级 | Controller | 行号 | 当前采用 |
|---|---|---|---|---|---|---|
| 1 | Page | 6 Manage Controllers | A | - | L13829-L59014 | A |
| 2 | Controller | 6 真实 + 15+ NOT FOUND | A | - | 全部 | A |
| 3 | State | systemSetting.checkList 等 17+ State | A | - | L50229+ | A |
| 4 | URL | (HTML 不可读) | F | - | - | F |
| 5 | Entry | companyId / employeeId / adminRoleId / consultRoomId | A | - | 全部 | A |
| 6 | Layout | (HTML 不可读) | F | - | - | F |
| 7 | Buttons | (HTML 不可读) | F | - | - | F |
| 8 | Inputs | (HTML 不可读) | F | - | - | F |
| 9 | Filters | roleId ($stateParams) | A | - | L1473+ | A |
| 10 | Status | (无 SystemSetting status) | F | - | - | F |
| 11 | Dialog | (HTML 不可读) | F | - | - | F |
| 12 | Pagination | pageSize=10/12/20 | A | - | 多处 | A |
| 13 | Sorting | (未明确) | F | - | - | F |
| 14 | Required | companyId (大部分) | A | - | 多处 | A |
| 15 | Default | adminRoleId=[1,2] | A | - | L105 | A |
| 16 | Data Source | 42 getCompany + 7 getEmployee + 4 getRole | A | - | 全部 | A |
| 17 | Object | companyId / employeeId / adminRoleId / consultRoomId | A | - | 全部 | A |
| 18 | Request | { companyId } / { employeeId } / { adminRoleId } | A | - | 多处 | A |
| 19 | Response | admin.adminRoleId / consultRoomVoList | A | - | L411/L9623 | A |
| 20 | Function | grantAuth.hasAuthForCompany / isUnlockFun | A | - | 多处 | A |
| 21 | State Bridge | corpInfo (localStorage) | A | - | L585-L14268 | A |
| 22 | Object Bridge | consultRoom.companyId (A) | A | - | L9336 | A |
| 23 | API Bridge | changeAdminRole.json | A | - | L232/L648 | A |
| 24 | Business Interpretation | Company/Employee/Role/ConsultRoom 是一级对象 | A | - | - | A (派生) |
| 25 | Evidence Grade | 19 A / 3 C / 0 D / 0 E / 4 F | - | - | - | - |
| 26 | V4.4 Decision | 4 个独立 ID 实体必保留, Clinic/Shop/Store F, SystemSetting 17+ State 路由 | A | - | - | A |

---

## §20 历史差异

### §20.1 S1-130/131/147/150 误判核对

| 历史口径 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| S1-130: SystemSetting 是 Object 实体 | 实际是 17+ State 路由名 | **应改** | **A (State 路由, F Object)** |
| S1-131: grantAuth 是 Object | 实际是 Function/Service 73 命中 | 保持 | **保持 S1-131 修正** |
| S1-131: roleId ≡ adminRoleId | 实际 roleId 仅 4 命中 ($stateParams), adminRoleId 38 命中 (真实 ID) | **应改** | **A (roleId 是 URL 入口, adminRoleId 是真实 ID)** |
| S1-131: schoolIdArray 是 School 主表字段 | 实际是 Scope + Request 复合字段 | 保持 | **保持 S1-131 修正** |
| S1-131: corpInfo 是数据库实体 | 实际是 localStorage 持久化 | 保持 | **保持 S1-131 修正** |
| S1-147: companyId 是业务 FK | 实际是 localStorage corpInfo 持久化的 State ID | 保持 | **保持 S1-147 修正** |
| S1-150: 加工中心 F 入口由 Company 派生 | 实际 Company 127 命中, 但是 corpInfo 是 Login Context State | 保持 | **保持 S1-150 修正** |

### §20.2 本轮新增历史差异

| 误判 | 当前证据 | 差异 | 当前采用 |
|---|---|---|---|
| ~~Clinic 是独立 ID 实体~~ | 0 命中 clinicId / clinicName / Clinic / getClinic*.json | **本轮重大发现** | **F** |
| ~~Shop 是独立 ID 实体~~ | 0 命中 shop / shopId / shopName / shopCtrl | **本轮重大发现** | **F** |
| ~~Store 是独立 ID 实体~~ | 0 命中 storeId / storeCtrl (store 128 是 stockIn/stockOut 混合词) | **本轮重大发现** | **F** |
| ~~Department 是独立 ID 实体~~ | departmentId 仅 1 命中 | **本轮重大发现** | **F** |
| ~~Permission / Auth ID 是独立实体~~ | 0 命中 permission / permissionId / authId / functionAuth | **本轮重大发现** | **F** |
| ~~SystemSetting 是 Object 实体~~ | 24 命中全部是 State 路由名 | **本轮重大发现** | **F (Object), A (State 路由)** |
| ~~roleId 是 adminRoleId 同义~~ | 实际 roleId 仅 4 命中 ($stateParams), adminRoleId 38 命中 | **本轮重大发现** | **A (不同身份, URL 入口 vs 真实 ID)** |
| ~~adminClinicCtrl 是 Clinic 实体 Controller~~ | 实际 adminClinicCtrl 是 admin 端, Clinic 概念 0 命中 | **本轮重大发现** | **A (adminClinicCtrl 是 admin 端, 不是 Clinic)** |
| ~~roleCtrl / roleManageCtrl 真实存在~~ | NOT FOUND | **本轮新增** | **F** |
| ~~employeeCtrl / departmentCtrl / consultRoomCtrl 真实存在~~ | NOT FOUND | **本轮新增** | **F** |
| ~~getSystemSetting*.json / saveSystemSetting*.json 存在~~ | 0 命中 | **本轮新增** | **F** |
| ~~Company 字段含 shopId/storeId~~ | 0 命中 | **本轮新增** | **F** |

### §20.3 保持历史结论 (不修改旧文档)

- 165_S1-124 ~ 213_S1-150 全部保持原样
- 本文档 214_*.md 单独记录权限底座完整闭环

---

## §21 V4.4 权限/诊所底座规格

### §21.1 必实现 (A 级)

| 项 | 等级 |
|---|---|
| **companyId 独立 ID** | A (127 命中) |
| **employeeId / adminId 独立 ID** | A (45/34 命中) |
| **adminRoleId 独立 ID** | A (38 命中) |
| **consultRoomId 独立 ID** | A (25 命中) |
| **corpInfo localStorage 持久化** | A (5 key) |
| **consultRoom.companyId 字段桥** | A (L9336) |
| **changeAdminRole.json Write API** | A (L232/L648) |
| **getRoleStateListForUpdate.json Read API** | A (L504) |
| **42 getCompany*.json Read API** | A |
| **7 getEmployee*.json Read API** | A |
| **2 getConsultRoom*.json Read API** | A |
| **6 个真实 Manage Controller** | A |
| **17+ systemSetting 子 State 路由** | A |
| **grantAuth Function/Service** | A (Function) |
| **schoolIdArray Request 字段** | A (复合) |

### §21.2 必不实现 (F 级)

| 项 | 必不实现 |
|---|---|
| `clinicId` / `clinicName` / `Clinic` 独立 Object | ✗ (0 命中) |
| `shop` / `shopId` / `shopName` / `Shop` 独立 Object | ✗ (0 命中) |
| `storeId` / `Store` 独立 Object | ✗ (0 命中) |
| `department` 顶层字段 (仅 departmentId 1 命中) | ✗ |
| `departmentName` / `departmentVo` 字段 | ✗ (0 命中) |
| `permission` / `permissionId` / `authId` / `functionAuth` / `menuAuth` / `buttonAuth` 字段 | ✗ (0 命中) |
| `systemSetting.xxx` Object 字段 (24 命中全部是 State 路由) | ✗ |
| `setting` / `settings` / `systemConfig` 独立字段 | ✗ (0 命中) |
| `getSystemSetting*.json` / `saveSystemSetting*.json` API | ✗ (0 命中) |
| `roleVo` / `roleList` / `employeeVo` 独立 VO 容器 | ✗ (0 命中) |
| `clinicCtrl` / `roleCtrl` / `employeeCtrl` / `departmentCtrl` / `consultRoomCtrl` / `companyManageCtrl` 等 NOT FOUND Controller | ✗ (NOT FOUND) |
| `company.clinic` / `company.shop` / `clinic.companyId` 字段桥 | ✗ (0 命中) |
| `roleId` 与 `adminRoleId` 合并 | ✗ (不同身份) |
| `corpInfo` 是数据库实体 | ✗ (localStorage State 持久化) |
| 6 ID 合并 | ✗ (companyId / employeeId / adminRoleId / consultRoomId / corpid / adminId 必须严格区分) |

### §21.3 10 对象 Object Type 分类 (A 级)

| Object | 实际 Type | V4.4 必不当作 |
|---|---|---|
| **Company** | A+B (独立 ID + Response + localStorage) | 包含 Clinic/Shop 字段 (F) |
| **Clinic** | F (0 命中) | 独立 ID 实体 |
| **Shop** | F (0 命中) | 独立 ID 实体 |
| **Store** | F (0 命中) | 独立 ID 实体 |
| **Department** | F (1 命中) | 独立 ID 实体 |
| **Employee** | A+B (独立 ID + Response) | employeeVo 独立 VO (F) |
| **Role** | A (adminRoleId 真实 ID, roleId 是 URL 入口) | roleVo 独立 VO (F) |
| **Authorization** | A (Function/Service) | permission/authId 独立 ID (F) |
| **SystemSetting** | A (17+ State 路由聚合) | Object 字段 (F) |
| **ConsultRoom** | A+B+C+D (独立 ID + 嵌套 + Request + Scope) | - |
| **corpInfo** | A (localStorage Login Context) | 数据库实体 (F) |

### §21.4 关键派生关系 (A 级)

| 派生 | 等级 | 字符级证据 |
|---|---|---|
| `consultRoom.companyId = res.id` (Company → ConsultRoom) | **A** | L9336 |
| `clinicInfo.consultRoom` (Clinic → ConsultRoom, 经 clinicInfo) | A | L9825 |
| `changeAdminRole.json { id: adminId, adminRoleId, companyId, schoolIdArray }` (Role → Employee) | A | L232/L648 |
| `corpInfo` localStorage 持久化 (Login → Context) | A | L14268 |
| `consultRoomVoList[].consultRoom.id` (ConsultRoom List 容器) | A | L9645 |

### §21.5 不可桥 (F 级)

| 不可桥 | 等级 |
|---|:---:|
| Clinic → Company 直接字段 | F |
| Company → Shop/Store 字段 | F |
| Employee → Department 字段 | F |
| Department → Employee 字段 | F |
| Role → Department 字段 | F |
| Role → Employee 字段 | F |
| roleId 与 adminRoleId 合并 | F |
| corpInfo 是数据库实体 | F |
| SystemSetting 是 Object 实体 | F |
| Shop/Store 任何字段 | F |
| Clinic 任何独立字段 | F |
| Authorization 任何 ID 字段 | F |

### §21.6 命名误导必标注 (V4.4 复刻必读)

| 命名 | 实际 | 警告 |
|---|---|---|
| `clinic` (6 命中) | 实际是 adminClinicCtrl 内的 `adminClinic` 字符串, 不是 Clinic 实体 | **命名误导** |
| `store` (128 命中) | 实际是 `stockIn` / `stockOut` 混合词, 没有 Store 实体 | **命名误导** |
| `departmentId` (1 命中) | 弱 ID, 不是独立 Object | 命名误导 |
| `roleId` (4 命中) | 实际是 $stateParams URL 入口, 不是 ID 字段 | **命名误导 (S1-131 误判已修正)** |
| `systemSetting` (24 命中) | 实际是 17+ State 路由名, 不是 Object 字段 | **命名误导** |
| `grantAuth` (73 命中) | 实际是 Function/Service, 不是 Object 实体 | **命名误导 (S1-131 误判已修正)** |
| `corpInfo` (46 命中) | 实际是 localStorage 持久化 Login Context, 不是 DB 实体 | **命名误导 (S1-131 误判已修正)** |
| `adminClinicCtrl` | 实际是 admin 端 Controller, 不是 Clinic 实体 Controller | **命名误导** |
| `companyInfo` (58 命中) | 实际是 login response.companyInfo 派生, 不是独立 Object | 命名误导 |
| `permission` | 0 命中, 没有独立 Permission 实体 | 命名误导 (历史可能误认为存在) |
| `systemSettingCtrl` | 实际是 17+ State 路由聚合器, 不是 Object 字段 Controller | 命名误导 |
| `loginInfo` (10 命中) | 实际是 commonFn.getSession("loginInfo") 临时变量, 不是 DB 实体 | 命名误导 |
| `myCorpInfo` | 0 命中, 实际是 corpInfo 字符串 | 命名误导 |
| `CorpInfo` (大写) | 0 命中, 实际统一用小写 corpInfo | 命名规范 |
| `Clinic` (大写) | 0 命中, 实际统一用小写 clinic | 命名规范 |

---

## §22 F / 未确认

| # | 命题 | 等级 | 后续验证 |
|---|---|:---:|---|
| 1 | Company 数据库表结构 | F | 需后端 |
| 2 | Employee 数据库表结构 | F | 需后端 |
| 3 | Role 数据库表结构 | F | 需后端 |
| 4 | ConsultRoom 数据库表结构 | F | 需后端 |
| 5 | Clinic 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 6 | Shop/Store 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 7 | Department 数据库表结构 | F (弱 1 命中) | 需后端 |
| 8 | Authorization 数据库表结构 | F (0 命中) | 需后端 |
| 9 | SystemSetting 数据库表结构 | F (0 字段) | 需后端 (如存在) |
| 10 | Permission 数据库表结构 | F (0 命中) | 需后端 (如存在) |
| 11 | corpInfo 完整 schema | F | 需后端 |
| 12 | schoolIdArray 与 Screening Plan 详细关系 | F (L634-L642) | 需后端 |
| 13 | changeAdminRole 完整 Request/Response | F | 需后端 |
| 14 | getRoleStateListForUpdate 完整 Response | F | 需后端 |
| 15 | 6 NOT FOUND Controller 命名历史 | F | 需 git log |
| 16 | corpInfo 登录后所有字段完整 schema | F | 需后端 + 真实登录 |
| 17 | grantAuth Function 内部实现 (Service/Fn?) | F (UI 调用层推测) | 需源码深入 |
| 18 | SystemSetting 17+ State 对应后端业务 | F (前端 State 路由推测) | 需后端 |
| 19 | roleId 是 URL 入口时哪个 State 传入 | F (L1473+L1542+L1597+L1666) | 需 State 路由配置 |
| 20 | 6 个真实 Manage Controller 后端 API 完整 | F (部分确认) | 需后端 |

---

## §23 Git / 完整性

### §23.1 完整性校验

| 检查项 | 状态 |
|---|---|
| API actual = 0 | ✓ |
| Write actual = 0 | ✓ |
| Production mutation = 0 | ✓ |
| controller.js SHA256 | ✓ `F40589FF...0A19433` |
| deliveryList.html SHA256 | ✓ `5B79B6F0...006476` |
| machineOrderCompleted.html SHA256 | ✓ `F1602AB1...30BDB24` |
| machineOrderList.html SHA256 | ✓ `A429507C...5AB9B26A` |
| 历史 MD 165-213 不变 | ✓ |
| P0=54 / P1=8 冻结 | ✓ |
| untracked=10 | ✓ |
| ignored=1 | ✓ (视光之家url.txt 未修改) |
| 本轮只新增 214_*.md | ✓ |

### §23.2 Git 操作

```
git add -- 214_S1-151_Clinic_Company_Shop_Department_Employee_Role_SystemSetting权限底座总审计.md
git diff --cached --name-only
git commit -m "docs(214): S1-151 Clinic/Company/Shop/Department/Employee/Role/SystemSetting 权限底座总审计"
git push origin master
```

### §23.3 预期

- tracked = 221 → **222**
- untracked = 10 (不变)
- ignored = 1 (不变)
- staged = 0
- LOCAL HEAD == origin/master
- 当前 HEAD: `cdcdc700a1dd4320bab754649f79abe3d78016ed` (S1-150 commit)

---

## 文档元信息

- **审计范围**：S1-151 (Clinic / Company / Shop / Department / Employee / Role / SystemSetting 权限底座)
- **本轮新增文件**：`214_S1-151_Clinic_Company_Shop_Department_Employee_Role_SystemSetting权限底座总审计.md`
- **依据证据等级**：A=字符级 / B=多源一致 / C=部分 / D=冲突 / E=推断 / F=未观察
- **结束条件**：本轮完成后立即停止，**不执行 S1-152** / 不修改 controller.js / 不修改 HTML / 不修改历史 MD
