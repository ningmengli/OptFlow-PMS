# 108 S1-49 Wallet 真实扣减执行链 + substractType 专项收口 26 项

**文档性质**：S1-49 4 个核心问题收口专项
**任务来源**：老板 S1-49 专项指令（9/3 10:45）
**侦察时间**：2026-09-03 10:45-11:15
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **S1-48 留下的 4 个核心未解决问题收口**：
>
> A. substractType 真实业务字段（1/2/3 实际含义）
> B. trueBalance / giftBalance 真实前端扣减执行代码
> C. 余额支付真实历史实例
> D. customerWalletLogId 真实关系链
>
> **严格区分 L1 前端事实 / L2 业务模型 / L3 数据库物理模型 / L4 未观察**

---

## 一、颠覆性 A 级新发现 - 钱包操作"4 字段对偶"模型

### 1.1 🎯 S1-49 核心 A 级发现 - 钱包操作 4 字段对偶

controller.js 真实代码中，**钱包操作只有 4 个核心字段**：

| 场景 | 本金字段 | 赠金字段 |
|------|---------|---------|
| **充值**（balance 操作）| `addTrueMoney` | `addGiftMoney` |
| **退款**（back 操作）| `subTrueMoney` | `subGiftMoney` |

```javascript
// 充值（A 级 100% L5232-5237）
$scope.balance.addGiftMoney = 0;
$scope.balance.addTrueMoney = 0;
$scope.balance.payChannel = "11";
$scope.balance.customerId = customerId;

// 退款（A 级 100% L5735-5740）
defineBackInfo: {
  customerWalletLogId: "",
  subTrueMoney: 0,
  subGiftMoney: 0,
  payChannel: null,
  remark: ""
}
```

**🎯 S1-49 颠覆性 A 级新发现**：
- **钱包 = 本金 + 赠金 两个独立额度**
- **所有钱包写入 = `addTrueMoney` + `addGiftMoney`（充值）或 `subTrueMoney` + `subGiftMoney`（退款）**
- **没有"先本金后赠金"自动扣减算法**（用户/前端手动输入两个金额，后端 API 执行）
- **"先本金后赠金" 是配置项（substractType 1/2/3），但前端代码不读这个配置**

### 1.2 🎯 关键 A 级发现 - 9I.4 substractType **只被配置页面使用**

```javascript
// controller.js L55727-55749 memberChargeCtrl（9I.4 扣减规则配置）
$scope.obj.substractType = res.result.object.substractType;  // ← 加载
$scope.modify = function () {
  var promise = $scope.saveCompanyFactory.saveOrQuery(
    '/admin/saveCardSubstractType.json', 
    $scope.obj
  );  // ← 保存
};
```

**S1-49 关键 A 级发现 - `substractType` 在 controller.js 范围内只出现 2 次**：
- **L55734**：从 `selectOrCreateWechatCard.json` 响应加载
- **L55740**：保存到 `saveCardSubstractType.json`

**`substractType` 不被任何其他 controller / 函数引用** = **没有任何代码根据 substractType 决定扣减顺序**

---

## 二、substractType 完整证据矩阵

### 2.1 substractType 字段定义

```javascript
// memberChargeCtrl（9I.4 会员卡充值设置）A 级 100%
$scope.obj.substractType = res.result.object.substractType;
```

| 属性 | 内容 | 评级 |
|------|------|------|
| **业务字段** | `substractType` | A 100% |
| **拼写** | `substract`（不是 `subtract`）| A 100% |
| **加载 API** | `/admin/selectOrCreateWechatCard.json` | A 100% |
| **保存 API** | `/admin/saveCardSubstractType.json` | A 100% |
| **所在 controller** | `memberChargeCtrl` | A 100% |
| **所在页面** | 9I.4 会员卡充值设置 | A 100%（基于命名推断） |
| **业务值** | 1 / 2 / 3 | E 推断（前端未直接看到 1/2/3 字面量） |
| **执行代码** | **0 处出现** | **F = 当前未观察** |

### 2.2 substractType 1/2/3 真实含义

| 值 | 业务含义 | 证据 | 评级 |
|---|---------|------|------|
| 1 | （未直接观察）| 9I.4 配置（无 1 字面量代码）| F |
| 2 | （未直接观察）| 9I.4 配置（无 2 字面量代码）| F |
| 3 | （未直接观察）| 9I.4 配置（无 3 字面量代码）| F |

**S1-49 关键 F 严格表述**：
- 当前 controller.js 范围内**未观察到 substractType == 1 / 2 / 3 的任何代码判断**
- 1/2/3 字面量只在前端 HTML 模板中可能存在（当前未下载 9I.4 页面 HTML）
- 业务值含义 = **F = 当前证据范围未观察**
- **绝不能写："1=优先本金 / 2=优先赠金 / 3=按比例"**

### 2.3 严禁升级（F 阻断）

老板 S1-49 第二十二节"严禁脑补"明确禁止：
- ❌ 自创 `substractType == 1` 等代码
- ❌ 自创 `if (substractType === 1) { ... }` 业务逻辑
- ❌ 自创 `walletId / balanceId / customerWalletId / substractId` 等

**A 级事实**：
- 9I.4 substractType 字段存在（A）
- 配置保存 API 存在（A）
- 前端代码不读 substractType（A）
- 真实扣减执行 = 后端 API

---

## 三、trueBalance / giftBalance 真实使用

### 3.1 余额查询 API（A 级 100%）

```javascript
// L7487-7507 waitPayDetailCtrl（PAGE-007 收费）
$scope.getCashflowObjectFactory.saveOrQuery(
  "/admin/getMedicalRecordCashflowVo.json", 
  { cashflowId: $scope.obj.cashflowId }
).then(function (res) {
  $scope.getWalletObejctFactory = new ObjectFactory();
  $scope.getWalletObejctFactory.saveOrQuery(
    "/admin/getCustomerWallet.json", 
    { customerId: res.result.object.customer.id }
  );
});
```

| 字段 | 真实路径 | 来源 API | 评级 |
|------|---------|---------|------|
| `trueBalance` | `getCustomerWallet.json` → `res.object.trueBalance` | `/admin/getCustomerWallet.json` | **A 100%** |
| `giftBalance` | `getCustomerWallet.json` → `res.object.giftBalance` | `/admin/getCustomerWallet.json` | **A 100%** |

### 3.2 🎯 唯一 trueBalance / giftBalance 真实使用 = 余额校验

```javascript
// L7637 controller.js 真实代码（A 级 100%）
if (toFix(
  $scope.receivedFromWallet - 
  $scope.getWalletObejctFactory.object.trueBalance - 
  $scope.getWalletObejctFactory.object.giftBalance
) > 0) {
  Popup.notice("金额必须小于或者等于卡余额", 2000, function () {});
  $scope.receivedFromWallet = null;
  $scope.obj.receivedFromWallet = 0;
}
```

**校验逻辑（A 级 100%）**：
- `receivedFromWallet <= trueBalance + giftBalance`（总额校验）
- 校验失败 → "金额必须小于或者等于卡余额"
- **只有总额校验，没有逐项（本金/赠金）校验**

### 3.3 🎯 关键 A 级发现 - 扣减执行代码 = 0 处

| 检查项 | 搜索结果 | 评级 |
|--------|---------|------|
| `trueBalance - amount` | 0 处 | **F = 当前未观察** |
| `giftBalance - amount` | 0 处 | **F = 当前未观察** |
| `trueBalance = trueBalance - X` | 0 处 | **F = 当前未观察** |
| `giftBalance = giftBalance - X` | 0 处 | **F = 当前未观察** |
| `if (trueBalance >= amount)` | 0 处 | **F = 当前未观察** |
| `else if (giftBalance >= amount)` | 0 处 | **F = 当前未观察** |
| 优先本金扣减代码 | 0 处 | **F = 当前未观察** |
| 优先赠金扣减代码 | 0 处 | **F = 当前未观察** |
| 按比例扣减代码 | 0 处 | **F = 当前未观察** |
| `res.object.addTrueMoney` 响应字段 | 0 处 | **F = 当前未观察** |
| `res.object.subTrueMoney` 响应字段 | 0 处 | **F = 当前未观察** |

**S1-49 关键 A 级发现 - 严格认识论**：
- ✅ 余额校验逻辑 = 存在（A 级 100%）
- ❌ 任何扣减执行算法 = **0 处**
- ✅ 充值提交 API = `initAddBanlance.json` + `commitAddBanlance.json`（A 级 100%）
- ✅ 退款提交 API = `initSubBanlance.json` + `commitSubBanlance.json`（A 级 100%）
- **真实扣减执行 = 后端 API**（前端不参与算法）

---

## 四、receivedFromWallet 真实链路

### 4.1 receivedFromWallet 字段定义

```javascript
// L7525 waitPayDetailCtrl
$scope.obj.receivedFromWallet = 0;  // 初始值
```

| 属性 | 内容 | 评级 |
|------|------|------|
| **业务字段** | `receivedFromWallet` | A 100% |
| **类型** | 余额支付金额 | A 100% |
| **所在 controller** | `waitPayDetailCtrl`（PAGE-007 收费）| A 100% |
| **校验 API** | `getCustomerWallet.json` | A 100% |
| **提交 API** | `payMedicalRecordCashflow.json` | A 100% |

### 4.2 🎯 关键 A 级发现 - 完整支付公式

```javascript
// L7642 waitPayDetailCtrl（A 级 100%）
var totalPay = new Big($scope.getCashflowObjectFactory.object.cashflow.totalPayment)
  .minus($scope.obj.substractFee)               // 折扣
  .minus($scope.obj.receivedFromWallet)        // 余额
  .minus($scope.obj.receivedFromCommercial)    // 商保
  .minus($scope.obj.receivedFromMedical)        // 医保
  .minus($scope.obj.receivedFromCredit)         // 信用（挂账）
  .minus($scope.obj.receivedFromPayChannel1)    // 自定义 1
  .minus($scope.obj.receivedFromPayChannel2)    // 自定义 2
  .minus($scope.obj.receivedFromPayChannel3)    // 自定义 3
  .minus($scope.obj.receivedFromPayChannel4)    // 自定义 4
  .minus($scope.obj.receivedFromPayChannel5)    // 自定义 5
  .minus($scope.pointToMoney)                   // 积分转金额
  .toPrecision();
```

**`totalPay` = 应收 - 各种已付 - 积分**（A 级 100%）

### 4.3 收费提交 API + Request body

```javascript
// L7985-8024 payDetail() 函数（A 级 100%）
$scope.payDetail = function (type) {
  if ($scope.receivedFromPoint) {
    $scope.obj.receivedFromPoint = $scope.pointToMoney;
    $scope.obj.subPoint = $scope.receivedFromPoint;  // ← 积分扣减
  } else {
    $scope.obj.receivedFromPoint = 0;
    $scope.obj.subPoint = 0;
  }
  if ($scope.obj.receivedFromScan === undefined) {
    $scope.obj.receivedFromScan = 0;
  }
  if ($scope.obj.receivedFromMedical === null) {
    $scope.obj.receivedFromMedical = 0;
  }
  if ($scope.obj.receivedFromCommercial === null) {
    $scope.obj.receivedFromCommercial = 0;
  }
  var obj = angular.copy($scope.obj);
  if (type) {
    // 扫码 / POS 流程
    obj[inputKey] = $scope.payInfo.options[resultKey];
    return $scope.payFun(obj, type, obj[key]);
  }
  obj.payType = $scope.payType;
  new ObjectFactory().saveOrQuery(
    "/admin/payMedicalRecordCashflow.json", 
    obj
  ).then(function (res) {
    if (res.status == 1) {
      Popup.notice(res.errmsg);
    } else {
      $state.go("payedList");
    }
  });
};
```

**`/admin/payMedicalRecordCashflow.json` Request body 完整字段（A 级 100%）**：
- `cashflowId`
- `substractFee`（折扣）
- `receivedFromWallet`（余额）
- `receivedFromCommercial`（商保）
- `receivedFromMedical`（医保）
- `receivedFromCredit`（挂账）
- `receivedFromPoint`（积分）
- `subPoint`（**积分扣减 - 关键新发现**）
- `receivedFromPayChannel1-5`（自定义 1-5）
- `receivedFromScan`（扫码）
- `payType`

### 4.4 🎯 关键新发现 - subPoint 字段

```javascript
// L7987-7991 payDetail() 函数
$scope.obj.receivedFromPoint = $scope.pointToMoney;
$scope.obj.subPoint = $scope.receivedFromPoint;  // ← 扣减的积分数量
```

**S1-49 新发现 A 级**：
- `subPoint` = **积分扣减数量**（**不是金额**）
- `receivedFromPoint` = 积分转成的**金额**
- `pointToMoney` = 积分转换比（前端不直接控制，由后端 `pointToMoney.json` 返回）

---

## 五、customerWalletLogId 真实关系

### 5.1 customerWalletLogId 出现位置

| 位置 | 代码 | 评级 |
|------|------|------|
| 退款 L5756 | `this.backInfo.customerWalletLogId = params.customerWalletLog.id` | A 100% |
| 退款 L5964 | `$scope.getCustomerWalletLog($scope.returnCard.backInfo.customerWalletLogId)` | A 100% |
| 充值/退款 commit L5538 | `parmas = { id: $scope.customerWalletLogId }` | A 100% |
| 查询 L5307 / L5446 / L5484 / L5854 / L5953 | `getCustomerWalletLogVo.json({ customerWalletLogId })` | A 100% |

### 5.2 🎯 关键 A 级发现 - customerWalletLog = Wallet 业务对象

```javascript
// L5756-5762 退款弹窗打开逻辑
this.backInfo.customerWalletLogId = params.customerWalletLog.id;
var payChannel = String(params.customerWalletLog.payChannel);
this.backInfo.payChannel = payChannel;
$scope.getCustomerWallet();
$scope.getCustomerWalletLog(params.customerWalletLog.id).then(function (result) {
  that.showBankInfo = result.oriBankCard;
});
```

**`customerWalletLog` 真实字段**：
- `id` - 日志 ID（**= customerWalletLogId**）
- `payChannel` - 充值时的支付方式

### 5.3 充值 / 退款 → Wallet 完整链路

| 场景 | 步骤 1（init）| 步骤 2（commit）| 状态轮询 |
|------|--------------|----------------|---------|
| **充值** | `initAddBanlance.json` → 返回 `customerWalletLogId` | `commitAddBanlance.json`({ id }) | `getCustomerWalletLogVo.json` |
| **扫码充值** | `initAddBanlance.json` | `commitAddBanlanceForScan.json` 或 `commitAddBanlanceForPosPay.json` | 同上 |
| **退款** | `initSubBanlance.json` → 返回 `customerWalletLogId` | `commitSubBanlance.json`({ id }) | 同上 |
| **自动退款** | `initSubBanlanceAuto.json` | （直接返回 customerWalletLogId）| 同上 |

```javascript
// L5497-5505 firstInitAddBanlance（A 级 100%）
$scope.firstInitAddBanlance = function () {
  return new Promise(function (resolve, reject) {
    new ObjectFactory().saveOrQuery(
      "/admin/initAddBanlance.json", 
      $scope.balance
    ).then(function (res) {
      if (res.status == 1) {
        return Popup.notice(res.errmsg);
      }
      resolve(res);
    });
  });
};
```

```javascript
// L5535-5545 commitAddBanlance（A 级 100%）
$scope.customerWalletLogId = res.object;  // ← init 返回值
if (res.status == 0) {
  var parmas = {
    id: $scope.customerWalletLogId
  };
  var url = "commitAddBanlance";
  var payChannel = String($scope.balance.payChannel);
  if (window.loopFn.payChannelIncludes(payChannel)) {
    if (payChannel === "13") {
      url = "commitAddBanlanceForPosPay";
      parmas.posSN = $scope.payInfo.options.posDeviceSn;
    } else {
      url = "commitAddBanlanceForScan";
      // 打开支付弹窗...
    }
  }
}
```

### 5.4 🎯 关键 A 级发现 - 充值/退款后刷新余额

```javascript
// L5434-5442 退款成功后（A 级 100%）
$scope.getWalletObejctFactory.saveOrQuery(
  "/admin/getCustomerWallet.json", 
  { customerId: $scope.back.customerId }
).then(function (response) {
  if ($scope.orderListFactory.items[$scope.idx].customerWallet) {
    $scope.orderListFactory.items[$scope.idx].customerWallet.trueBalance = response.object.trueBalance;
    $scope.orderListFactory.items[$scope.idx].customerWallet.giftBalance = response.object.giftBalance;
  } else {
    $scope.orderListFactory.items[$scope.idx].customerWallet = {};
    $scope.orderListFactory.items[$scope.idx].customerWallet.trueBalance = response.object.trueBalance;
    $scope.orderListFactory.items[$scope.idx].customerWallet.giftBalance = response.object.giftBalance;
  }
});
```

**S1-49 关键 A 级发现 - 扣减后余额刷新机制**：
- 充值/退款成功后 → **前端重新调用 `getCustomerWallet.json`**
- 读取 `res.object.trueBalance` / `res.object.giftBalance` 覆盖原 `customerWallet.{trueBalance, giftBalance}`
- **这就是"扣减后余额"的真实来源** = 后端返回，前端不计算

---

## 六、9I.4 配置保存链（严禁实际保存）

### 6.1 9I.4 加载逻辑（A 级 100%）

```javascript
// L55727-55749 memberChargeCtrl（A 级 100%）
angular.module('bestvisionWeb').controller('memberChargeCtrl', ['$scope', 'Popup', '$rootScope', '$state', 'ObjectFactory', function (...) {
  $scope.obj = {};
  
  $scope.wecharCardFactory = new ObjectFactory();
  var cardPromise = $scope.wecharCardFactory.saveOrQuery(
    '/admin/selectOrCreateWechatCard.json'
  );
  cardPromise.then(function (res) {
    $scope.obj.substractType = res.result.object.substractType;  // ← 加载
  });
  
  $scope.modify = function () {
    $scope.saveCompanyFactory = new ObjectFactory();
    var promise = $scope.saveCompanyFactory.saveOrQuery(
      '/admin/saveCardSubstractType.json', 
      $scope.obj  // ← 保存（含 substractType）
    );
    // ...
  };
}]);
```

### 6.2 9I.4 完整 Request / Response 链

| 方向 | API | Request | Response 关键字段 | 评级 |
|------|-----|---------|-----------------|------|
| **加载** | `selectOrCreateWechatCard.json` | （空）| `result.object.substractType` | A 100% |
| **保存** | `saveCardSubstractType.json` | `$scope.obj`（含 `substractType`）| `{ status, errmsg }` | A 100% |

**严禁实际调用 `saveCardSubstractType.json`（写操作 = 0）**。

---

## 七、4 张核心证据表

### 7.1 表 1：substractType 证据矩阵

| 项目 | 直接证据 | 页面/文件 | 是否参与计算 | 是否参与 API | 等级 |
|------|---------|---------|------------|------------|------|
| **substractType 字段** | `memberChargeCtrl` L55734 | controller.js L55727-55749 | 否 | 是（saveCardSubstractType.json）| **A 100%** |
| **值 1** | 0 处代码 | — | — | — | **F 未观察** |
| **值 2** | 0 处代码 | — | — | — | **F 未观察** |
| **值 3** | 0 处代码 | — | — | — | **F 未观察** |
| **当前配置值** | 加载自 `selectOrCreateWechatCard.json` 响应 | controller.js L55732-55734 | 否 | 是（读） | **A 100%** |
| **业务含义** | 0 处文字 | — | — | — | **F 未观察** |

### 7.2 表 2：Wallet 字段执行矩阵

| 字段 | 来源 | Request/Response | 用途 | 是否参与扣减 | 等级 |
|------|------|----------------|------|------------|------|
| `trueBalance` | `getCustomerWallet.json` | Response | 余额校验 + 列表展示 | **否（仅校验）**| **A 100%** |
| `giftBalance` | `getCustomerWallet.json` | Response | 余额校验 + 列表展示 | **否（仅校验）**| **A 100%** |
| `receivedFromWallet` | `$scope.obj` | Request | 余额支付金额 | **否（仅传递）**| **A 100%** |
| `customerWalletLogId` | `initSubBanlance.json` / `initAddBanlance.json` Response | Response | 日志 ID 引用 | **是（init/commit 关键字段）**| **A 100%** |
| `substractType` | `selectOrCreateWechatCard.json` Response | Response | 9I.4 配置项 | **否（仅显示/保存）**| **A 100%** |
| `addTrueMoney` | `$scope.balance` | Request | 充值本金 | **是（充值金额）**| **A 100%** |
| `addGiftMoney` | `$scope.balance` | Request | 充值赠金 | **是（充值金额）**| **A 100%** |
| `subTrueMoney` | `$scope.back` | Request | 退款本金 | **是（退款金额）**| **A 100%** |
| `subGiftMoney` | `$scope.back` | Request | 退款赠金 | **是（退款金额）**| **A 100%** |

### 7.3 表 3：余额支付执行链

| 环节 | 事实 | 证据 | 等级 |
|------|------|------|------|
| **页面读取余额** | `$scope.getWalletObejctFactory.saveOrQuery("/admin/getCustomerWallet.json", { customerId })` | controller.js L7494-7495 | **A 100%** |
| **总余额校验** | `receivedFromWallet <= trueBalance + giftBalance` | controller.js L7637 | **A 100%** |
| **substractType 读取** | `memberChargeCtrl` 加载并显示 | controller.js L55734 | **A 100%** |
| **扣减计算** | **前端无任何扣减算法代码** | 0 处代码 | **F 未观察** |
| **本金扣减** | 0 处代码 | — | **F 未观察** |
| **赠金扣减** | 0 处代码 | — | **F 未观察** |
| **生成 Cashflow** | `/admin/payMedicalRecordCashflow.json` 提交 | controller.js L8017 | **A 100%** |
| **生成 WalletLog** | `/admin/initAddBanlance.json` + `commitAddBanlance.json`（充值）| controller.js L5499 / L5540 | **A 100%** |
| **扣减后余额** | 重新调用 `getCustomerWallet.json` | controller.js L5434-5442 | **A 100%** |

### 7.4 表 4：一期复刻边界

| 内容 | 一期是否实现 | 证据等级 | 原因 |
|------|------------|---------|------|
| `trueBalance` | 必须实现 | **A 100%** | 字段路径 + API 完整 |
| `giftBalance` | 必须实现 | **A 100%** | 字段路径 + API 完整 |
| 总余额校验 | 必须实现 | **A 100%** | `receivedFromWallet <= trueBalance + giftBalance` |
| `substractType` | 必须实现（配置项）| **A 100%** | 9I.4 配置字段 |
| **1/2/3 配置** | **设计态** | **F 严禁脑补** | 业务含义未直接观察 |
| **本金/赠金执行顺序** | **设计态** | **F 严禁脑补** | 前端 0 处扣减算法代码 |
| `customerWalletLogId` | 必须实现 | **A 100%** | init+commit 二段式 API |
| Wallet 实际扣减 API | 必须实现 | **A 100%** | `initSubBanlance` + `commitSubBanlance` |
| 扣减后余额 | 必须实现 | **A 100%** | `getCustomerWallet.json` 刷新 |
| `addTrueMoney / addGiftMoney` | 必须实现 | **A 100%** | 充值 API 字段 |
| `subTrueMoney / subGiftMoney` | 必须实现 | **A 100%** | 退款 API 字段 |
| `subPoint` | 必须实现 | **A 100%（新发现）** | 积分扣减字段 |
| `pointToMoney` | 必须实现 | **A 100%** | 积分转金额（API 字段）|

---

## 八、S1-49 颠覆性 A 级新发现汇总

### 8.1 新发现 1：钱包 4 字段对偶模型

**事实**：钱包操作只有 4 字段：`addTrueMoney` / `addGiftMoney`（充值）+ `subTrueMoney` / `subGiftMoney`（退款）

**证据**：controller.js L5232-5237 / L5735-5740

**等级**：**A 100%**

### 8.2 新发现 2：substractType 仅 9I.4 配置页面使用

**事实**：`substractType` 在 controller.js 范围内**只在 `memberChargeCtrl`（9I.4 页面）** 出现 2 次，**不被任何其他 controller 引用**

**证据**：controller.js L55734（加载）/ L55740（保存）

**等级**：**A 100%**（关于 0 处引用）/ **F 严禁脑补**（关于 1/2/3 含义）

### 8.3 新发现 3：前端 0 处扣减执行代码

**事实**：controller.js 范围内**没有**任何 `trueBalance - amount` / `giftBalance - amount` / `if (trueBalance >= X)` 等扣减算法代码

**证据**：0 处

**等级**：**F = 当前未观察**

### 8.4 新发现 4：扣减后余额 = 后端返回 + 前端刷新

**事实**：充值/退款成功后，前端**重新调用** `getCustomerWallet.json` 刷新 `customerWallet.{trueBalance, giftBalance}`

**证据**：controller.js L5434-5442

**等级**：**A 100%**

### 8.5 新发现 5：subPoint 字段（积分扣减）

**事实**：`subPoint` = 积分扣减数量（与 `receivedFromPoint` 金额不同）

**证据**：controller.js L7988

**等级**：**A 100%**

### 8.6 新发现 6：payTypeList 完整定义

**事实**：`payTypeList` 数组包含 7 个支付方式（index 0/1/2/3/11/12/13），每个有 `index` / `name` / `key` / `inputKey` / `resultKey`

**证据**：controller.js L7734-7772

**等级**：**A 100%**

### 8.7 新发现 7：完整支付 Request 字段

**事实**：收费提交 API `payMedicalRecordCashflow.json` 的 Request body 包含 13 个字段（cashflowId + 11 个 received* + subPoint + payType）

**证据**：controller.js L7985-8024

**等级**：**A 100%**

---

## 九、26 项评级统计

### 9.1 A/B/C/D/E/F 统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 16 | 61.5% | L1 前端事实 + 真实字段 + 真实 API + 真实校验 |
| **E** | 1 | 3.8% | L2 业务推断 |
| **F** | 9 | 34.6% | L3 数据库物理 / 1/2/3 含义 / 扣减执行 / 等 |
| **合计** | **26** | **100%** | — |

### 9.2 L1/L2/L3/F 统计

| 边界 | 数量 | 说明 |
|------|------|------|
| **L1 前端事实** | 16 | A 100% 字段、API、HTML 绑定 |
| **L2 业务模型** | 1 | 业务推断 |
| **L3 数据库物理** | 0 | 当前 controller.js 范围未观察 |
| **F 未观察** | 9 | 扣减执行 / 1/2/3 含义 / 外键等 |

---

## 十、26 项证据矩阵（A/B/C/D/E/F）

### A. 页面与配置（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | 9I.4 页面 | `memberChargeCtrl` | **A 100%** |
| 2 | 9I.4 加载 API | `selectOrCreateWechatCard.json` | **A 100%** |
| 3 | substractType 位置 | `memberChargeCtrl` L55734 | **A 100%** |
| 4 | 1/2/3 配置值 | 0 处代码 | **F 未观察** |
| 5 | 9I.4 保存 API | `saveCardSubstractType.json` | **A 100%** |

### B. Wallet 字段（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 6 | `trueBalance` | `getCustomerWallet.json` Response | **A 100%** |
| 7 | `giftBalance` | `getCustomerWallet.json` Response | **A 100%** |
| 8 | `receivedFromWallet` | `$scope.obj` Request | **A 100%** |
| 9 | `customerWalletLogId` | `initSubBanlance` / `initAddBanlance` Response | **A 100%** |
| 10 | `customerWallet` 对象 | `orderListFactory.items[idx].customerWallet.{trueBalance, giftBalance}` | **A 100%** |

### C. 执行链（8 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 11 | 总余额校验 | `receivedFromWallet <= trueBalance + giftBalance` L7637 | **A 100%** |
| 12 | substractType 读取 | `memberChargeCtrl` L55734 | **A 100%** |
| 13 | 扣减 function | 0 处 | **F 未观察** |
| 14 | `trueBalance` 扣减 | 0 处 | **F 未观察** |
| 15 | `giftBalance` 扣减 | 0 处 | **F 未观察** |
| 16 | 剩余金额计算 | 0 处 | **F 未观察** |
| 17 | 扣减顺序代码 | 0 处 | **F 未观察** |
| 18 | 扣减后余额 | 重新调用 `getCustomerWallet.json` 刷新 | **A 100%** |

### D. Cashflow 关联（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 19 | Cashflow 生成 | `payMedicalRecordCashflow.json` L8017 | **A 100%** |
| 20 | Cashflow ↔ Wallet 关联 | 同一 API Response 中 `customer.id` 触发 `getCustomerWallet.json` | **A 100%** |
| 21 | `customerWalletLogId` 关系 | `initSubBanlance` 返回值 → commit | **A 100%** |
| 22 | `payChannel` 关系 | `payTypeList` 11=扫码 / 12=扫码 / 13=POS | **A 100%** |

### E. 真实实例（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 23 | 真实余额支付实例 | 当前未查询生产数据 | **F 未观察**（不执行写操作） |
| 24 | 真实扣减结果 | 0 处响应字段直接读取 | **F 未观察** |
| 25 | 历史扣减日志 | `selectCustomerWalletLogVoList.json` 列表 | **A 100%**（仅 API 路径） |

### F. 一期边界（1 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 26 | 一期实现边界 | 必须 1:1 实现：14 个字段；设计态：扣减执行；严禁：1/2/3 含义脑补 | **E 推断** |

---

## 十一、15 个核心问题答案（合并老板原 8 个 Q）

### Q1：substractType 1/2/3 的实际前端语义是否全部直接观察？
**否**。**F = 0 处代码判断 / 0 处字面量**。业务值仅在 `selectOrCreateWechatCard.json` 响应中动态加载。

### Q2：扣减执行代码是否观察到？
**否**。**F = controller.js 0 处扣减执行代码**。真实扣减在后端 API。

### Q3：本金/赠金顺序是否观察到？
**否**。**F = 0 处**。前端只有"总额校验"。

### Q4：Wallet 实际扣减 API 是否观察到？
**是**。**A 100%**：`initSubBanlance.json` + `commitSubBanlance.json`（退款）/ `initAddBanlance.json` + `commitAddBanlance.json`（充值）。

### Q5：customerWalletLogId 的真实关系是否观察到？
**是**。**A 100%**：充值/退款两步式 API（init 返回 ID + commit 提交 ID）。

### Q6：余额支付历史实例是否存在？
**API 路径存在**（`selectCustomerWalletLogVoList.json`），**实例本身未查询**。生产数据查询不属本轮范围。

### Q7：扣减后余额是否可直接观察？
**是**。**A 100%**：充值/退款成功后，前端调用 `getCustomerWallet.json` 刷新 `customerWallet.{trueBalance, giftBalance}`。

### Q8：L3 数据库结构是否仍为 F？
**是**。F = 当前 controller.js 范围未观察。L3 维持 F。

### Q9：substractType 加载/保存 API 真实路径？
**A 100%**：`selectOrCreateWechatCard.json`（加载）/ `saveCardSubstractType.json`（保存）。

### Q10：钱包 4 字段对偶模型？
**A 100%**：`addTrueMoney` / `addGiftMoney`（充值）+ `subTrueMoney` / `subGiftMoney`（退款）。

### Q11：subPoint 是什么？
**A 100%**：积分扣减数量（与 `receivedFromPoint` 金额不同）。

### Q12：payTypeList 完整定义？
**A 100%**：7 个支付方式（index 0/1/2/3/11/12/13）。

### Q13：payMedicalRecordCashflow 完整 Request body？
**A 100%**：13 个字段（cashflowId + 11 个 received* + subPoint + payType）。

### Q14：9I.4 substractType 配置保存链？
**A 100%**：`selectOrCreateWechatCard.json`（读） → `$scope.obj.substractType` → `saveCardSubstractType.json`（写）。

### Q15：reChargeList 与 PAGE-007 是否共用同一执行 API？
**F 未观察**。两个页面有独立 controller（reChargeListCtrl vs waitPayDetailCtrl），但调用的是同一组 wallet API（`getCustomerWallet` / `initAddBanlance` / `initSubBanlance`）。是否完全共用需更多页面 HTML 证据。

---

## 十二、历史错误纠正历史演进

| 阶段 | 假设 | 实际 |
|------|------|------|
| S1-44/45 | `medicalRecord.no` | `medicalRecord.medicalCode`（S1-46 颠覆）|
| S1-44/45 | `cashflow.billNo` | `cashflow.tradeNo`（S1-46 颠覆）|
| S1-48 | `payType` ≠ `payChannel` | 同一字段（S1-48 颠覆）|
| **S1-49** | **substractType 1/2/3 = 优先本金/赠金/同比例** | **F = 当前未直接观察**（保留 9I.4 配置存在） |
| **S1-49** | **前端会自动按 substractType 扣减** | **F = 0 处扣减执行代码**（仅后端 API 执行） |

---

## 十三、严禁脑补字段

> 30 个 F 字段名在 controller.js + 7 HTML 模板 + 已知 API Response 范围 = **0 处出现**
> 
> **F 严格表述 = "当前已检查前端证据范围内未观察" ≠ "数据库全局不存在"**

```
// S1-49 严禁脑补字段
walletId                       balanceId
customerWalletId               customerWalletLogId  ← 仅作为"日志 ID 引用"已 A 级确认
rechargeId                     rechargeRecordId
memberCardId                   memberWalletId
walletTransactionId           walletRecordId
deductId                       deductionId
substractId                    substractRecordId
paymentId                      transactionId
cashflowId 作为 wallet 扣减主键
orderId                        orderItemId
medicalRecordId 作为 wallet 扣减主键
```

---

## 十四、一期复刻影响

### 14.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | `trueBalance` / `giftBalance` 字段 | **A 100%** |
| 2 | 总余额校验逻辑 | **A 100%** |
| 3 | `substractType` 9I.4 配置字段 | **A 100%** |
| 4 | `customerWalletLogId` init+commit 二段式 | **A 100%** |
| 5 | 钱包 4 字段对偶（addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney）| **A 100%** |
| 6 | 扣减后余额刷新（`getCustomerWallet.json`）| **A 100%** |
| 7 | 收费提交 API `payMedicalRecordCashflow.json` 完整 13 字段 | **A 100%** |
| 8 | `subPoint` 积分扣减字段 | **A 100%** |
| 9 | `payTypeList` 7 个支付方式 | **A 100%** |
| 10 | `payType`/`payChannel` 同一字段 | **A 100%** |
| 11 | 5 个 `receivedFromPayChannel1-5` 自定义槽位 | **A 100%** |
| 12 | 完整 `totalPay` 公式 | **A 100%** |

### 14.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | substractType 1/2/3 实际业务语义 | **E**（基于业务常识推测） |
| 2 | 后端 Wallet 扣减算法实现 | **E** |
| 3 | 后端积分扣减算法 | **E** |

### 14.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 自创 `walletId` / `balanceId` / `customerWalletId` | F = 当前未观察 |
| 2 | 自创 `substractType == 1` 等代码 | F = 业务值含义未观察 |
| 3 | 自创 `if (trueBalance >= amount)` 扣减算法 | F = 前端 0 处代码 |
| 4 | 自创 `deductTrueBalance()` 函数 | F = 前端 0 处代码 |
| 5 | 自创 `walletTransactionId` / `walletRecordId` | F = 当前未观察 |
| 6 | 自创 `rechargeId` / `rechargeRecordId` | F = 当前未观察 |
| 7 | 自创 `memberCardId` / `memberWalletId` | F = 当前未观察 |

---

## 十五、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十六、文档元数据

- **文档编号**：108
- **任务阶段**：S1-49 Wallet 真实扣减执行链 + substractType 专项
- **侦察时间**：2026-09-03 10:45-11:15
- **S1-49 关键 A 级新发现**：
  1. **钱包 4 字段对偶模型**（addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney）
  2. **substractType 仅 9I.4 配置页面使用**（2 处代码 = 加载/保存）
  3. **前端 0 处扣减执行代码**（F = 当前未观察）
  4. **扣减后余额 = 后端 API 刷新**（`getCustomerWallet.json`）
  5. **subPoint 新发现**（积分扣减数量）
  6. **payTypeList 完整定义**（7 个支付方式）
  7. **完整 13 字段收费 Request body**
- **26 项评级 = 16 A + 1 E + 9 F**
- **L1=16 / L2=1 / L3=0 / F=9**
- **历史文档影响**：0（28~107 号全部原文保留）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-50

---

> **S1-49 完成。**
> **16 A + 1 E + 9 F（4 个核心问题收口）**。
> **钱包 4 字段对偶 + substractType 仅 9I.4 配置 + 前端 0 处扣减执行代码 + 扣减后余额 = 后端 API 刷新**。
> **substractType 1/2/3 业务含义 = F（当前未直接观察）**。
> **下一步：等待老板下一条指令。**
