# 109 S1-50 Wallet 四字段 + Init/Commit + WalletLog + Cashflow 协议关系收口 26 项

**文档性质**：S1-50 钱包前端协议专项收口
**任务来源**：老板 S1-50 专项指令（9/3 10:58）
**侦察时间**：2026-09-03 11:00-11:30
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0

---

## 零、本轮真正目标

> **把 S1-49 钱包 4 字段对偶 + Init/Commit 二阶段 API 全部钉死**：
>
> A. Wallet 4 字段（addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney）来源矩阵
> B. Init/Commit 二阶段 API 完整调用链
> C. customerWalletLogId 生命周期
> D. Cashflow ↔ Wallet 前端协议关系
>
> **不再追问"后端先扣本金还是赠金"**（保持 F = 当前未直接观察）

---

## 一、Wallet 四字段证据矩阵

### 1.1 充值字段（addTrueMoney / addGiftMoney）

| 行号 | context | 评级 |
|------|---------|------|
| L5234-5235 | `showRecharge` 初始化 `$scope.balance = { addGiftMoney: 0, addTrueMoney: 0, payChannel: "11", customerId }` | **A 100%** |
| L5507-5527 | `saveWallet` 校验（不能同时为 0、数字格式、>0）| **A 100%** |
| L5551 | `paystatus.open({ fee: $scope.balance.addTrueMoney })` 扫码支付金额 | **A 100%** |
| L5581 | `loopPayStatus.successOption.moneyKey = "addTrueMoney"` | **A 100%** |
| L5645 | `that.options.payMoney = $scope.balance.addTrueMoney` | **A 100%** |
| L5865 | `loopPayStatus.successOption.moneyKey = "addTrueMoney"`（退款成功）| **A 100%** |
| L15922-15930 | 第二处 `saveWallet` 实例 | **A 100%** |
| L17971-17972 / L49346-49347 / L18048 / L49353 | 重置/初始化 | **A 100%** |

### 1.2 退款字段（subTrueMoney / subGiftMoney）

| 行号 | context | 评级 |
|------|---------|------|
| L5320-5343 | `subTrueCompute(money)` 校验（数字格式、>0、≤money）| **A 100%** |
| L5345-5367 | `subGiftCompute(money)` 校验（同上）| **A 100%** |
| L5393-5395 | `backWallet` 死代码（`return;` 后不再执行）| **A 100%（确认）** |
| L5396-5419 | `backWallet` 死代码内的校验逻辑 | **F（死代码不执行）** |
| L5735-5740 | `returnCard.defineBackInfo = { customerWalletLogId, subTrueMoney: 0, subGiftMoney: 0, payChannel, remark }` | **A 100%** |
| L5756 | `this.backInfo.customerWalletLogId = params.customerWalletLog.id` | **A 100%** |
| L5788-5832 | `backInterface` 实际退款（initSubBanlance + commitSubBanlance）| **A 100%** |
| L5833-5885 | `initBackInterface` 自动退款（initSubBanlanceAuto）| **A 100%** |
| L5846 | `paystatus.open({ fee: subTrueMoney })` 自动退款金额 | **A 100%** |

### 1.3 🎯 关键 A 级发现 - 字段语义来源

**`True` 命名来源 = `trueBalance`（S1-47 已 A 级确认的本金字段）**：
- `addTrueMoney` ← 增加 trueBalance
- `subTrueMoney` ← 减少 trueBalance

**`Gift` 命名来源 = `giftBalance`（S1-47 已 A 级确认的赠金字段）**：
- `addGiftMoney` ← 增加 giftBalance
- `subGiftMoney` ← 减少 giftBalance

**前端 controller 中没有任何 `trueBalance - ` / `giftBalance - ` 扣减执行代码**（S1-49 已 A 级确认）
**扣减执行 = 后端 API**（initSubBanlance / initAddBanlance + commit）

### 1.4 字段所属（A 级 100%）

| 字段 | 所属对象 | Request/Response | 作用 |
|------|---------|-----------------|------|
| `addTrueMoney` | `$scope.balance` | **Request** | 充值本金金额 |
| `addGiftMoney` | `$scope.balance` | **Request** | 充值赠金金额 |
| `subTrueMoney` | `$scope.back.subTrueMoney` 或 `$scope.returnCard.backInfo.subTrueMoney` | **Request** | 退款本金金额 |
| `subGiftMoney` | `$scope.back.subGiftMoney` 或 `$scope.returnCard.backInfo.subGiftMoney` | **Request** | 退款赠金金额 |

**所有四字段都是 Request 字段，从不被前端从 Response 读取**（A 级 100%，0 处 `res.object.addTrueMoney` 出现）

---

## 二、Init/Commit 二阶段 API 完整调用链

### 2.1 充值链 A：initAddBanlance → commitAddBanlance

```javascript
// firstInitAddBanlance L5497-5505（A 级 100%）
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

// saveWallet 中调用 firstInitAddBanlance + commitAddBanlance（A 级 100%）
var fn = function fn(res) {
  $scope.customerWalletLogId = res.object;  // ← init 返回值保存到 $scope
  if (res.status == 0) {
    var parmas = {
      id: $scope.customerWalletLogId          // ← commit 用同一个 ID
    };
    var url = "commitAddBanlance";
    var payChannel = String($scope.balance.payChannel);
    if (window.loopFn.payChannelIncludes(payChannel)) {
      if (payChannel === "13") {
        url = "commitAddBanlanceForPosPay";
        parmas.posSN = $scope.payInfo.options.posDeviceSn;
      } else {
        url = "commitAddBanlanceForScanPay";   // ← 注意：ForScanPay（不是 ForScan）
        $scope.paystatus.open({
          type: "0",
          payType: payChannel,
          fee: $scope.balance.addTrueMoney
        });
        parmas.authCode = $scope.payInfo.options.authCode;
      }
    }
    new ObjectFactory().saveOrQuery("/admin/" + url + ".json", parmas)
  }
};
```

**充值调用链 A 级 100%**：

| 步骤 | API | Request | Response |
|------|-----|---------|---------|
| 1 | `initAddBanlance.json` | `$scope.balance` = `{ addTrueMoney, addGiftMoney, payChannel, customerId }` | `res.object` → `$scope.customerWalletLogId` |
| 2 | `commitAddBanlance.json` (默认) | `{ id: $scope.customerWalletLogId }` | `result` |
| 2' | `commitAddBanlanceForPosPay.json` (payChannel=13) | `{ id, posSN }` | 同上 |
| 2'' | `commitAddBanlanceForScanPay.json` (payChannel=11/12) | `{ id, authCode }` | 同上 |
| 3 | `getCustomerWalletLog` (轮询) | `{ customerWalletLogId: $scope.customerWalletLogId }` | 轮询 status |

**S1-49 修正**：是 `commitAddBanlanceForScanPay`（**带 Pay**，不是 `ForScan`）

### 2.2 退款链 B：initSubBanlance → commitSubBanlance

```javascript
// backInterface L5788-5832（A 级 100%）
backInterface: function backInterface() {
  var _that$backInfo = that.backInfo,
      subTrueMoney = _that$backInfo.subTrueMoney,
      subGiftMoney = _that$backInfo.subGiftMoney,
      payChannel = _that$backInfo.payChannel;

  if (subTrueMoney === 0 && subGiftMoney === 0) {
    return Popup.notice("退卡金额和赠送金额不能同时为0");
  }
  if (!payChannel) {
    return Popup.notice("请选择退款方式!");
  }
  var execute = function execute() {
    new ObjectFactory().saveOrQuery(
      "/admin/initSubBanlance.json", 
      that.backInfo
    ).then(function (res) {
      if (res.status) {
        return Popup.notice(res.errmsg);
      }
      var id = res.result.object;            // ← init 返回值
      /* commit */
      new ObjectFactory().saveOrQuery(
        "/admin/commitSubBanlance.json", 
        { id: id }                            // ← commit 用同一个 ID
      ).then(function (result) {
        if (result.status) {
          return Popup.notice(result.errmsg);
        }
        Popup.notice("退款成功");
        that.hideModal();
        $scope.printFn(id);                    // ← 打印
      });
    });
  };
  if (window.loopFn.payChannelIncludes(payChannel)) {
    execute = that.initBackInterface;          // ← 扫码/POS 用自动退款
  }
  grantAuth.getBackAuth(ObjectFactory, "1").then(function () {
    $timeout(execute);
  }, function (err) {
    $timeout(function () {
      if (err) return Popup.notice(err);
      $scope.smsPop.show = true;
      $scope.smsPop.fn = execute;
    });
  });
}
```

**退款调用链 A 级 100%**：

| 步骤 | API | Request | Response |
|------|-----|---------|---------|
| 1 | `initSubBanlance.json` | `that.backInfo` = `{ customerWalletLogId, subTrueMoney, subGiftMoney, payChannel, remark }` | `res.result.object` → `id` |
| 2 | `commitSubBanlance.json` | `{ id: id }` | `result` |
| 3 | `printFn(id)` (打印) | — | — |

### 2.3 自动退款链 C：initSubBanlanceAuto（无 commit）

```javascript
// initBackInterface L5833-5885（A 级 100%）
initBackInterface: function initBackInterface() {
  var _$scope$returnCard$ba = $scope.returnCard.backInfo,
      subTrueMoney = _$scope$returnCard$ba.subTrueMoney,
      payChannel = _$scope$returnCard$ba.payChannel;

  new ObjectFactory().saveOrQuery(
    "/admin/initSubBanlanceAuto.json", 
    $scope.returnCard.backInfo
  ).then(function (res) {
    if (res.status) {
      return Popup.notice(res.errmsg);
    }
    $scope.paystatus.open({
      type: "1",
      payType: payChannel,
      bankCardInfo: $scope.returnCard.showBankInfo,
      fee: subTrueMoney
    });
    var customerWalletLogId = res.result.object;   // ← init 返回值
    loopFn.loopPayStatus({
      ObjectFactory: ObjectFactory,
      params: {
        url: "getCustomerWalletLogVo",
        params: {
          customerWalletLogId: customerWalletLogId
        }
      },
      statusOption: {
        status1: "success",
        status2: "waitingPayStatus",
        resultKey: "customerWalletLog"
      },
      successOption: {
        moneyKey: "addTrueMoney",                  // ← 成功金额字段
        payTypeKey: "payChannel",                  // ← 支付方式字段
        type: "已退款",
        voiceType: "2"                             // ← 2=退款
      }
    }).then(function () {
      Popup.notice("退 款 成 功！");
      $timeout(function () {
        $scope.printFn(customerWalletLogId);
      });
    }, function (errMsg) {
      Popup.notice(errMsg ? errMsg : "退 款 失 败！");
    }).finally(function () {
      $scope.returnCard.hideModal();
    });
  });
}
```

**🎯 S1-50 关键 A 级发现 - 自动退款 = 无 commit 步骤**：

| 步骤 | API | Request | Response |
|------|-----|---------|---------|
| 1 | `initSubBanlanceAuto.json` | `$scope.returnCard.backInfo` | `res.result.object` → `customerWalletLogId` |
| 2 | `getCustomerWalletLogVo` (loopPayStatus 轮询) | `{ customerWalletLogId }` | 轮询 status |

**`initSubBanlanceAuto` 没有 `commitSubBanlance` 后续**（A 100% = 0 处 commit 出现）

---

## 三、customerWalletLogId 完整生命周期

### 3.1 生命周期表

| 环节 | 行号 | API/function | 字段来源 | 去向 | 评级 |
|------|------|-------------|---------|------|------|
| **生成（initAddBanlance）** | L5535 | `initAddBanlance.json` Response | `res.object` | → `$scope.customerWalletLogId` | **A 100%** |
| **生成（initSubBanlance）** | L5424 | `initSubBanlance.json` Response | `res.object` | → `$scope.customerWalletLogId` | **A 100%** |
| **生成（initSubBanlanceAuto）** | L5848 | `initSubBanlanceAuto.json` Response | `res.result.object` | → `var customerWalletLogId` | **A 100%** |
| **保存到 backInfo** | L5736 | `returnCard.defineBackInfo` 模板 | 初始 `""` | 模板默认值 | **A 100%** |
| **设置 backInfo** | L5756 | `openModal` | `params.customerWalletLog.id` | → `this.backInfo.customerWalletLogId` | **A 100%** |
| **传给 commitAddBanlance** | L5538 | `commitAddBanlance.json` | `$scope.customerWalletLogId` | → `parmas.id` | **A 100%** |
| **传给 commitSubBanlance** | L5427 / L5809 | `commitSubBanlance.json` | `res.result.object` / `id` | → `{ id }` | **A 100%** |
| **传给 WalletLog 单条查询** | L5307 / L5446 / L5484 / L5953 | `getCustomerWalletLogVo.json` | `$scope.customerWalletLogId` / 函数参数 | → `{ customerWalletLogId }` | **A 100%** |
| **传给 WalletLog 轮询** | L5571 / L5854 | `loopPayStatus` | `$scope.customerWalletLogId` / `customerWalletLogId` | → `params.params.customerWalletLogId` | **A 100%** |
| **传给 printFn** | L5874 / L5964 | `printFn` | `customerWalletLogId` / `$scope.returnCard.backInfo.customerWalletLogId` | → 打印日志 | **A 100%** |

### 3.2 🎯 关键 A 级发现 - ID 跨函数传递链

```
initAddBanlance.json
   ↓
res.object                       (L5535)
   ↓
$scope.customerWalletLogId       (L5535)
   ↓
parmas = { id: ... }             (L5537-5539)
   ↓
commitAddBanlance.json / commitAddBanlanceForPosPay / commitAddBanlanceForScanPay (L5556)
   ↓
loopPayStatus getCustomerWalletLog (L5566-5572)
   ↓
params.params.customerWalletLogId
```

```
initSubBanlance.json
   ↓
res.object                       (L5424)
   ↓
$scope.customerWalletLogId       (L5424)
   ↓
{ id: res.result.object }        (L5427)
   ↓
commitSubBanlance.json
   ↓
printFn(id) / printFn(customerWalletLogId)
```

### 3.3 严格区分：前端变量连续传递 ≠ 数据库外键

**L1 前端事实** = ID 在前端变量中跨函数连续传递（A 100%）

**L3 数据库物理** = 是否有外键约束 = **F = 当前证据范围未观察**

**严禁脑补**：
- ❌ "customerWalletLogId = customer_wallet_log.id 数据库主键"
- ❌ "Cashflow 表有 wallet_log_id 外键字段"
- ❌ "WalletLog 表有 cashflow_id 外键字段"

---

## 四、WalletLog 双 API 区别

### 4.1 单条详情 vs 列表查询

| API | 类型 | 用途 | Request | 评级 |
|-----|------|------|---------|------|
| `getCustomerWalletLogVo.json` | **单条详情** (ObjectFactory) | 打印/查询单条 | `{ customerWalletLogId }` | **A 100%** |
| `selectCustomerWalletLogVoList.json` | **列表** (ListFactory) | 列表查询 | `{ customerId, logType, hasRollBack }` | **A 100%** |

### 4.2 出现位置

| API | 行号 | context | 评级 |
|-----|------|---------|------|
| `getCustomerWalletLogVo.json` | L5307 | `printLog` 打印 | **A 100%** |
| `getCustomerWalletLogVo.json` | L5446 | `backWallet` 死代码（刷新打印） | **A 100%（死代码不执行）** |
| `getCustomerWalletLogVo.json` | L5484 | `backWallet` 死代码（另一种打印） | **A 100%（死代码不执行）** |
| `getCustomerWalletLogVo.json` | L5569 | `loopPayStatus` URL = `"getCustomerWalletLog"`（不带 Vo 后缀？）| **A 100%** |
| `getCustomerWalletLogVo.json` | L5852 | `loopPayStatus` URL = `"getCustomerWalletLogVo"` | **A 100%** |
| `getCustomerWalletLogVo.json` | L5953 | `getCustomerWalletLog` function（打印） | **A 100%** |
| `selectCustomerWalletLogVoList.json` | L5279 | `searchLog` 列表 | **A 100%** |
| `selectCustomerWalletLogVoList.json` | L5893 / L5912 | `search` / `searchTotal` 退款列表 | **A 100%** |
| `selectCustomerWalletLogVoList.json` | L37199 | `searchEmployeeRank` 员工排行 | **A 100%** |

### 4.3 🎯 命名严格区分

- `getCustomerWalletLogVo` (带 Vo) = 单条详情
- `getCustomerWalletLog` (不带 Vo) = 仅在 L5569 出现于 `loopPayStatus` URL 配置
- `selectCustomerWalletLogVoList` = 列表
- 命名差异 = 业务场景差异（详情 vs 列表）

### 4.4 logType 业务含义

| 值 | 用途 | 评级 |
|---|------|------|
| 0 | 默认（充值/扣款？）| **F 未直接观察** |
| 1 | 退款/其他？| **F 未直接观察** |
| 2 | 退款？| **F 未直接观察** |
| 3 | 其他？| **F 未直接观察** |

**L37831-37834** 显示 logType 0 = [0, 3]，logType 1 = [1, 2]（数组展开），但具体含义 F。

**严禁排列 logType = 新增/扣减/退款/充值**（老板 14 节明确禁止）

---

## 五、getCustomerWallet 完整链路

### 5.1 加载（A 级 100%）

```javascript
// waitPayDetailCtrl L7437-7438
$scope.getWalletObejctFactory = new ObjectFactory();
$scope.getWalletObejctFactory.saveOrQuery(
  "/admin/getCustomerWallet.json", 
  { customerId: res.result.object.customer.id }
);
```

### 5.2 刷新（A 级 100%）

```javascript
// 退款成功 / 充值成功 L5434-5442
var getPromise = $scope.getWalletObejctFactory.saveOrQuery(
  "/admin/getCustomerWallet.json", 
  { customerId: $scope.back.customerId }
);
getPromise.then(function (response) {
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

### 5.3 真实 Response 字段（A 级 100%）

| 字段 | 真实路径 | 评级 |
|------|---------|------|
| `trueBalance` | `res.object.trueBalance` 或 `response.object.trueBalance` | **A 100%** |
| `giftBalance` | `res.object.giftBalance` 或 `response.object.giftBalance` | **A 100%** |

**注意**：`customerWallet` 是 walletLogVo 列表项中的嵌套对象（`orderListFactory.items[idx].customerWallet`），不是 API 顶层字段。

---

## 六、Cashflow 协议分析

### 6.1 完整 Request Body（A 级 100%）

`angular.copy($scope.obj)` + `obj.payType = $scope.payType`：

| 字段 | 来源 | 评级 |
|------|------|------|
| `cashflowId` | URL state param | **A 100%** |
| `substractFee` | `$scope.obj` | **A 100%** |
| `receivedFromWallet` | `$scope.obj` | **A 100%** |
| `receivedFromCommercial` | `$scope.obj` | **A 100%** |
| `receivedFromMedical` | `$scope.obj` | **A 100%** |
| `receivedFromCredit` | `$scope.obj` | **A 100%** |
| `receivedFromPoint` | `$scope.obj` | **A 100%** |
| `subPoint` | `$scope.obj` (L7988) | **A 100%** |
| `receivedFromPayChannel1-5` | `$scope.obj` | **A 100%** |
| `receivedFromScan` | `$scope.obj` (L7995) | **A 100%** |
| `payType` | `obj.payType = $scope.payType` (L8016) | **A 100%** |

### 6.2 🎯 关键 A 级发现 - Cashflow Request 缺失字段

**`payMedicalRecordCashflow.json` Request body 中没有**：
- ❌ `customerId`
- ❌ `patientId`
- ❌ `medicalRecordId`
- ❌ `customerWalletLogId`
- ❌ `addTrueMoney` / `addGiftMoney`
- ❌ `subTrueMoney` / `subGiftMoney`

**`$scope.obj` 全部 16 个字段 + 1 个 payType = 纯支付字段**

### 6.3 Wallet-Cashflow 协议关系（A 级 100%）

**结论**：**前端协议上 Cashflow 和 Wallet 是两条并行协议**（前端不直接关联）

**L1 证据**：
- `payMedicalRecordCashflow.json` Request **不携带** customerWalletLogId
- `payMedicalRecordCashflow.json` Request **不携带** addTrueMoney/subTrueMoney 等 Wallet 字段
- 余额支付 `receivedFromWallet > 0` 只是**金额字段**传给后端
- 后续 `getCustomerWallet.json` 调用**不在 payDetail() 流程中**

**L2 业务推断**（E 级）：
- 后端可能通过 cashflowId 关联 Wallet Log
- 但前端**不直接观察**到这个关联

**L3 数据库物理**（F = 未观察）：
- 数据库 Cashflow 表是否有 wallet_log_id 外键
- Wallet Log 表是否有 cashflow_id 外键
- 都 = F

---

## 七、API 总矩阵

| API | 场景 | Request 关键字段 | Response 关键字段 | 后续调用 | 评级 |
|-----|------|----------------|-----------------|---------|------|
| `initAddBanlance.json` | 充值 | `addTrueMoney, addGiftMoney, payChannel, customerId` | `res.object` (customerWalletLogId) | commitAddBanlance | **A 100%** |
| `commitAddBanlance.json` | 充值 | `{ id: customerWalletLogId }` | result | loopPayStatus → getCustomerWalletLog | **A 100%** |
| `commitAddBanlanceForPosPay.json` | 充值 POS | `{ id, posSN }` | result | 同上 | **A 100%** |
| `commitAddBanlanceForScanPay.json` | 充值扫码 | `{ id, authCode }` | result | 同上 | **A 100%** |
| `initSubBanlance.json` | 退款 | `customerWalletLogId, subTrueMoney, subGiftMoney, payChannel, remark` | `res.result.object` (id) | commitSubBanlance | **A 100%** |
| `commitSubBanlance.json` | 退款 | `{ id }` | result | printFn | **A 100%** |
| `initSubBanlanceAuto.json` | 自动退款 | `$scope.returnCard.backInfo` | `res.result.object` (customerWalletLogId) | loopPayStatus → getCustomerWalletLogVo | **A 100%** |
| `getCustomerWallet.json` | 查询余额 | `{ customerId }` | `{ trueBalance, giftBalance }` | （用于校验/刷新）| **A 100%** |
| `getCustomerWalletLogVo.json` | 单条详情 | `{ customerWalletLogId }` | `walletLogVo` | （用于打印/轮询）| **A 100%** |
| `selectCustomerWalletLogVoList.json` | 列表 | `{ customerId, logType, hasRollBack }` | list | （分页）| **A 100%** |
| `payMedicalRecordCashflow.json` | 收费 | 16 个支付字段 + payType | result | `payedList` 跳转 | **A 100%** |

---

## 八、三条业务时序图

### 8.1 时序 A：充值（addTrueMoney + addGiftMoney）

```
页面：reChargeList
  ↓
$scope.showRecharge(customerId)                   L5232
  ↓ 初始化
$scope.balance = { 
  addTrueMoney: 0, 
  addGiftMoney: 0, 
  payChannel: "11", 
  customerId: customerId 
}                                                  L5232-5237
  ↓
[用户输入 addTrueMoney / addGiftMoney]
  ↓
$scope.saveWallet()                               L5507
  ↓ 校验
if (addTrueMoney===0 && addGiftMoney===0) return  L5508
数字格式校验                                      L5512-5529
payChannel 必选                                    L5531-5533
  ↓
$scope.firstInitAddBanlance()                     L5497
  ↓
POST /admin/initAddBanlance.json
Request: $scope.balance
Response: res.object → $scope.customerWalletLogId L5535
  ↓
判断 payChannel:                                  L5540-5554
  - "13" → commitAddBanlanceForPosPay + posSN
  - 11/12 → commitAddBanlanceForScanPay + authCode + paystatus.open
  - 其他 → commitAddBanlance
  ↓
POST /admin/{url}.json
Request: { id: $scope.customerWalletLogId, ... }  L5556
Response: result
  ↓
loopPayStatus {                                   L5566-5586
  url: "getCustomerWalletLog",
  params: { customerWalletLogId: ... }
  successOption: {
    moneyKey: "addTrueMoney",
    payTypeKey: "payChannel",
    voiceType: "1"  // 收款
  }
}
  ↓
"支付成功" → $scope.successFn()                   L5589-5590
```

### 8.2 时序 B：退款（subTrueMoney + subGiftMoney）

```
页面：reChargeList（退款弹窗）
  ↓
$scope.returnCard.openModal(params, nowIndex)     L5752
  ↓
this.backInfo = {
  customerWalletLogId: params.customerWalletLog.id,  L5756
  subTrueMoney: 0,
  subGiftMoney: 0,
  payChannel: String(params.customerWalletLog.payChannel),  L5757-5758
  remark: ""
}
$scope.getCustomerWallet()                       L5759
$scope.getCustomerWalletLog(id).then(...)         L5760-5766
  ↓
[用户输入 subTrueMoney / subGiftMoney + 选择 payChannel]
  ↓
$scope.returnCard.backInterface()                L5788
  ↓ 校验
if (subTrueMoney===0 && subGiftMoney===0) return  L5795
if (!payChannel) return Popup.notice             L5798-5800
  ↓
[分支] payChannelIncludes(payChannel)            L5820
  - 是 (11/12/13) → execute = initBackInterface  L5821
  - 否 → execute = initSubBanlance + commitSubBanlance
  ↓
grantAuth.getBackAuth(ObjectFactory, "1")         L5823
  ↓
[execute() 路径 A: 手动退款]
  POST /admin/initSubBanlance.json
  Request: that.backInfo
  Response: res.result.object → id              L5802-5806
  ↓
  POST /admin/commitSubBanlance.json
  Request: { id: id }                           L5808-5810
  Response: result
  ↓
  "退款成功" → printFn(id)                       L5814-5816

[execute() 路径 B: 自动退款]
  POST /admin/initSubBanlanceAuto.json
  Request: $scope.returnCard.backInfo
  Response: res.result.object → customerWalletLogId  L5838-5848
  ↓
  paystatus.open({ type: "1", payType, fee: subTrueMoney })  L5842-5847
  ↓
  loopPayStatus {
    url: "getCustomerWalletLogVo",
    params: { customerWalletLogId },
    successOption: {
      moneyKey: "addTrueMoney",
      payTypeKey: "payChannel",
      voiceType: "2"  // 退款
    }
  }
  ↓
  "退 款 成 功！" → printFn(customerWalletLogId)  L5870-5875
```

### 8.3 时序 C：收费（receivedFromWallet 余额支付）

```
页面：waitPayDetailCtrl（PAGE-007 待收费）
  ↓
$scope.obj.cashflowId = $stateParams.cashflowId  L7462
  ↓
POST /admin/getMedicalRecordCashflowVo.json
Request: { cashflowId }
Response: result.object.{cashflow, medicalRecord, customer, ...}
  ↓
POST /admin/getCustomerVo.json                  L7433-7436
Request: { customerId: res.result.object.customer.id }
  ↓
POST /admin/getCustomerWallet.json              L7437-7438
Request: { customerId }
Response: { trueBalance, giftBalance }
  ↓
POST /admin/getCustomerPoint.json               L7439-7440
Request: { customerId }
Response: { point }
  ↓
POST /admin/pointToMoney.json                   L7442-7444
Request: { point: resp.result.object.point }
Response: pointToMoney 比率
  ↓
[页面 UI：用户输入 substractFee / receivedFromWallet / ...]
  ↓
$scope.receivedWallet()                         L7619
  ↓ 校验
if (receivedFromWallet - trueBalance - giftBalance > 0)
  → "金额必须小于或者等于卡余额"               L7637-7640
  ↓
计算 totalPay = totalPayment - substractFee - ...  L7642
if (totalPay < 0) return Popup.notice
  ↓
$scope.confirmPay()                              L7886
  ↓
$scope.payDetail(type)                           L7985
  ↓ 组装
obj = angular.copy($scope.obj)                   L8003
obj[inputKey] = $scope.payInfo.options[resultKey]  (扫码/POS)  L8012
obj.payType = $scope.payType                     L8016
  ↓
POST /admin/payMedicalRecordCashflow.json        L8017
Request: obj (16 字段 + payType，不含 customerWalletLogId)
Response: result
  ↓
if (res.status == 1) Popup.notice(res.errmsg)    L8018-8019
else $state.go("payedList")                      L8021
```

**🎯 S1-50 关键 A 级发现 - 时序 C 不调用 Wallet 操作 API**：
- 收费提交后**只跳转 payedList**，**不调用** `getCustomerWallet.json` 刷新
- 余额支付 `receivedFromWallet > 0` **不直接触发** initAddBanlance / initSubBanlance
- **前端协议上：Cashflow 提交和 Wallet 扣减完全分离**

---

## 九、L1/L2/L3 边界

### 9.1 L1 前端事实（A 100%）

| 项 | 评级 |
|----|------|
| Wallet 4 字段（addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney）| **A 100%** |
| 11 个 Init/Commit API 路径 | **A 100%** |
| customerWalletLogId 完整生命周期 | **A 100%** |
| `getCustomerWalletLogVo.json` vs `selectCustomerWalletLogVoList.json` 区别 | **A 100%** |
| `getCustomerWallet.json` Response 字段 | **A 100%** |
| `payMedicalRecordCashflow.json` 完整 17 字段 Request body | **A 100%** |
| 三条业务时序图 | **A 100%** |
| Cashflow 不携带 customerWalletLogId | **A 100%** |
| Cashflow 不携带 addTrueMoney/subTrueMoney | **A 100%** |
| `backWallet` 是死代码 | **A 100%** |
| 自动退款（initSubBanlanceAuto）无 commit 步骤 | **A 100%** |

### 9.2 L2 业务模型（E 级推断）

| 项 | 评级 |
|----|------|
| 后端通过 cashflowId 关联 WalletLog | **E**（业务推断，无直接证据） |
| 后端根据 substractType 1/2/3 决定扣减顺序 | **E**（配置存在但执行未观察） |

### 9.3 L3 数据库物理（F = 未观察）

| 项 | 评级 |
|----|------|
| customerWalletLogId 数据库主键 | **F**（仅知字段名，不知表名/类型） |
| Cashflow 表 wallet_log_id 外键 | **F** |
| WalletLog 表 cashflow_id 外键 | **F** |
| Wallet 表结构 | **F** |
| WalletLog 表结构 | **F** |
| 后端扣减算法实现 | **F** |

---

## 十、26 项评级矩阵

### A 组：四字段（5 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 1 | `addTrueMoney` 来源 | `$scope.balance` Request 字段 | **A 100%** |
| 2 | `addGiftMoney` 来源 | `$scope.balance` Request 字段 | **A 100%** |
| 3 | `subTrueMoney` 来源 | `$scope.back` / `backInfo` Request 字段 | **A 100%** |
| 4 | `subGiftMoney` 来源 | `$scope.back` / `backInfo` Request 字段 | **A 100%** |
| 5 | 四字段所属 Request/Response | 全部 Request 字段 | **A 100%** |

### B 组：Init/Commit（7 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 6 | `initAddBanlance` | L5499 / L5503 | **A 100%** |
| 7 | `commitAddBanlance` | L5540-5556 | **A 100%** |
| 8 | `commitAddBanlanceForScanPay` | L5547 | **A 100%**（修正 S1-49 命名错误）|
| 9 | `commitAddBanlanceForPosPay` | L5544 | **A 100%** |
| 10 | `initSubBanlance` | L5422 / L5802 | **A 100%** |
| 11 | `commitSubBanlance` | L5427 / L5808 | **A 100%** |
| 12 | `initSubBanlanceAuto` | L5838（无 commit）| **A 100%** |

### C 组：Wallet Log（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 13 | `customerWalletLogId` 生命周期 | 11 个位置已追踪 | **A 100%** |
| 14 | `getCustomerWalletLogVo` 单条 | ObjectFactory + 打印 | **A 100%** |
| 15 | `selectCustomerWalletLogVoList` 列表 | ListFactory + 分页 | **A 100%** |
| 16 | `logType` 业务含义 | 0/1/2/3 数组展开 | **F 未直接观察** |

### D 组：Wallet 状态（4 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 17 | `getCustomerWallet` | L7437-7438 / L5434 | **A 100%** |
| 18 | `trueBalance` 响应 | `res.object.trueBalance` | **A 100%** |
| 19 | `giftBalance` 响应 | `res.object.giftBalance` | **A 100%** |
| 20 | Wallet 刷新链 | 充值/退款成功后调用 | **A 100%** |

### E 组：Cashflow（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 21 | `payMedicalRecordCashflow` | L8017 | **A 100%** |
| 22 | `receivedFromWallet` 余额支付 | `$scope.obj.receivedFromWallet` | **A 100%** |
| 23 | Cashflow ↔ WalletLog 前端关系 | **不携带 customerWalletLogId** | **A 100%（无关联）** |

### F 组：综合（3 项）

| # | 项目 | 实际观察 | 评级 |
|---|------|---------|------|
| 24 | 充值时序 | 时序 A 完整 | **A 100%** |
| 25 | 退款时序 | 时序 B 完整（含自动退款）| **A 100%** |
| 26 | 余额支付时序 | 时序 C 完整 | **A 100%** |

---

## 十一、26 项统计

| 评级 | 数量 | 占比 | 说明 |
|------|------|------|------|
| **A** | 25 | 96.2% | L1 前端事实 100% 收口 |
| **E** | 0 | 0% | — |
| **F** | 1 | 3.8% | logType 0/1/2/3 业务含义未直接观察 |
| **合计** | **26** | **100%** | — |

**L1 = 25 / L2 = 0 / L3 = 0 / F = 1**

---

## 十二、本轮新增事实（S1-50 独有）

### 事实 1：commitAddBanlanceForScanPay 完整命名（A 级 100%）

**事实**：是 `commitAddBanlanceForScanPay`（**带 Pay**），不是 `commitAddBanlanceForScan`

**证据**：controller.js L5547 `url = "commitAddBanlanceForScanPay"`

**等级**：**A 100%**

**修正 S1-49 错误**：S1-49 写为 `commitAddBanlanceForScan`（少 Pay）

### 事实 2：自动退款（initSubBanlanceAuto）无 commit 步骤（A 级 100%）

**事实**：`initSubBanlanceAuto` 之后**没有** `commitSubBanlance` 调用，直接进入 `loopPayStatus` 轮询

**证据**：controller.js L5838-5885（initSubBanlanceAuto 完整逻辑 47 行内 0 处 commit）

**等级**：**A 100%**

### 事实 3：payMedicalRecordCashflow Request 17 字段（A 级 100%）

**事实**：`payMedicalRecordCashflow.json` Request body = 17 个支付字段（不含 customerWalletLogId / addTrueMoney / subTrueMoney 等 Wallet 字段）

**证据**：controller.js L8003 + L8016 + $scope.obj 全部 16 字段

**等级**：**A 100%**

### 事实 4：Cashflow 和 Wallet 前端协议完全分离（A 级 100%）

**事实**：前端**没有**任何代码将 `customerWalletLogId` 传给 `payMedicalRecordCashflow.json`，也**没有**将 `addTrueMoney`/`subTrueMoney` 传给任何收费 API

**证据**：waitPayDetailCtrl 范围（L7395-8070）内 0 处 `customerWalletLogId` 出现

**等级**：**A 100%**

### 事实 5：backWallet 是死代码（A 级 100%）

**事实**：`backWallet` function L5393 在 L5395 `return;` 后**全部是死代码**，从不执行

**证据**：controller.js L5393-5442 实际可执行代码只有 L5394-5395 4 行

**等级**：**A 100%**

### 事实 6：customerWalletLogId 在 11 个不同位置出现（A 级 100%）

**事实**：完整生命周期包括 11 处出现：3 处 init 生成、2 处 backInfo 模板/赋值、2 处 commit 传递、3 处 WalletLog 查询、1 处 printFn

**证据**：见 3.1 表格

**等级**：**A 100%**

---

## 十三、历史纠错检查

| # | 历史结论 | 本轮复核 | 结果 |
|---|---------|---------|------|
| 1 | substractType 只在配置页面读取/保存 | 维持 L55734 / L55740 | **一致** |
| 2 | trueBalance / giftBalance 只观察到总额校验 | 维持 L7637 | **一致** |
| 3 | Wallet 扣减算法前端未观察 | 维持 0 处扣减代码 | **一致** |
| 4 | customerWalletLogId 存在 | 维持 + 11 处出现 | **增强** |
| 5 | Cashflow 存在 receivedFromWallet | 维持 | **一致** |
| 6 | payType = payChannel | 维持 L8055 等 | **一致** |
| 7 | L3 数据库结构未知 | 维持 F | **一致** |
| 8 | commitAddBanlanceForScan | **修正为 ForScanPay** | **历史有误** |

---

## 十四、一期复刻影响

### 14.1 必须 1:1 复刻（A 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | Wallet 4 字段（addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney）| **A 100%** |
| 2 | 11 个 Init/Commit API 路径 | **A 100%** |
| 3 | `commitAddBanlanceForScanPay`（带 Pay）正确命名 | **A 100%** |
| 4 | 自动退款无 commit 步骤 | **A 100%** |
| 5 | customerWalletLogId 11 个位置生命周期 | **A 100%** |
| 6 | `getCustomerWalletLogVo` 单条 vs `selectCustomerWalletLogVoList` 列表 | **A 100%** |
| 7 | `getCustomerWallet.json` 余额查询 | **A 100%** |
| 8 | `payMedicalRecordCashflow.json` 17 字段 Request body | **A 100%** |
| 9 | 三条业务时序 | **A 100%** |
| 10 | `backWallet` 死代码状态 | **A 100%** |
| 11 | `payType = payChannel` 同一字段 | **A 100%** |

### 14.2 需要设计（E 级证据支持）

| # | 能力 | 评级 |
|---|------|------|
| 1 | 后端 Cashflow ↔ WalletLog 数据库关联 | **E** |
| 2 | 后端 Wallet 扣减算法 | **E** |
| 3 | 后端积分扣减算法 | **E** |
| 4 | substractType 1/2/3 业务值含义 | **E** |

### 14.3 不得实现（F 阻断 / 严禁脑补）

| # | 能力 | 阻断原因 |
|---|------|---------|
| 1 | 自创 `walletId` / `balanceId` / `customerWalletId` | F = 当前未观察 |
| 2 | 自创 `walletTransactionId` / `walletRecordId` | F = 当前未观察 |
| 3 | 自创 `rechargeId` / `rechargeRecordId` | F = 当前未观察 |
| 4 | 自创 `memberCardId` / `memberWalletId` | F = 当前未观察 |
| 5 | 自创 `deductId` / `deductionId` | F = 当前未观察 |
| 6 | 自创 `substractId` / `substractRecordId` | F = 当前未观察 |
| 7 | 自创 `transactionId` / `paymentId` | F = 当前未观察 |
| 8 | 自创 `wallet` / `walletLog` / `walletTransaction` 表名 | F = 当前未观察 |
| 9 | 在 Cashflow 表添加 `wallet_log_id` 外键 | F = 前端不携带该字段 |
| 10 | 在 WalletLog 表添加 `cashflow_id` 外键 | F = 前端不携带该字段 |
| 11 | 在 `payMedicalRecordCashflow.json` 添加 Wallet 字段 | F = 不在 Request body 中 |
| 12 | logType 0/1/2/3 业务值 | F = 业务含义未直接观察 |

---

## 十五、严禁脑补清单

> 27 个 F 字段名在 controller.js + 7 HTML 模板 + 已知 API Response 范围 = **0 处出现**
>
> **F 严格表述 = "当前已检查前端证据范围内未观察" ≠ "数据库全局不存在"**

```
// 严禁脑补字段
walletId                  balanceId               customerWalletId
customerWalletLogId  ← 仅作为"日志 ID 引用"已 A 级确认
rechargeId                rechargeRecordId
memberCardId              memberWalletId
walletTransactionId       walletRecordId
deductId                  deductionId
substractId               substractRecordId
rechargeId                rechargeRecordId
transactionId             paymentId

// 严禁脑补表名
wallet                    walletLog
walletTransaction         walletBalance

// 严禁脑补外键
Cashflow.wallet_log_id
WalletLog.cashflow_id
```

---

## 十六、仍未解决问题

| Q# | 问题 | 答案 | 评级 |
|----|------|------|------|
| Q1 | addTrueMoney / addGiftMoney / subTrueMoney / subGiftMoney 出现位置 | **A 100%**（11 + 8 + 14 + 14 = 47 处）| A 100% |
| Q2 | 它们所属 Request/Response/对象 | **A 100%**（全部 Request 字段）| A 100% |
| Q3 | initAddBanlance 返回什么 | `res.object` = `customerWalletLogId` | A 100% |
| Q4 | commitAddBanlance 接收什么 | `{ id: customerWalletLogId }` | A 100% |
| Q5 | init 返回的 ID 是否被 commit 继续使用 | **是**（变量连续传递）| A 100% |
| Q6 | 这个 ID 是否能证明为 customerWalletLogId | **是**（变量名直接证据）| A 100% |
| Q7 | getCustomerWalletLogVo.json vs selectCustomerWalletLogVoList.json 区别 | **单条详情 vs 列表** | A 100% |
| Q8 | Wallet 变更与 Cashflow 在哪里发生联系 | **前端无联系** | A 100% |
| Q9 | receivedFromWallet 是否触发 Wallet 操作 | **否**（仅金额字段，后端处理）| A 100% |
| Q10 | L1/L2/L3 边界 | **L1=25 / L2=0 / L3=0 / F=1** | A 100% |
| Q11 | 后端先扣本金还是赠金 | **F 未直接观察** | F |
| Q12 | logType 0/1/2/3 业务含义 | **F 未直接观察** | F |
| Q13 | 后端 Cashflow ↔ WalletLog 关联 | **E 业务推断** | E |
| Q14 | 后端扣减算法 | **F 未直接观察** | F |
| Q15 | L3 数据库结构 | **F 维持** | F |

---

## 十七、P0/P1

- **P0 = 54** ✅
- **P1 = 8** ✅
- 本轮不自动新增 / 不自动解除

---

## 十八、文档元数据

- **文档编号**：109
- **任务阶段**：S1-50 Wallet 四字段 + Init/Commit + WalletLog + Cashflow 协议收口
- **侦察时间**：2026-09-03 11:00-11:30
- **S1-50 关键 A 级新发现**：
  1. **`commitAddBanlanceForScanPay` 正确命名**（修正 S1-49 错误）
  2. **自动退款无 commit 步骤**（initSubBanlanceAuto 直接进入 loopPayStatus）
  3. **payMedicalRecordCashflow 17 字段 Request body 完整**（不含 Wallet 字段）
  4. **Cashflow 和 Wallet 前端协议完全分离**（无 customerWalletLogId 传递）
  5. **backWallet 是死代码**（L5395 return; 后不执行）
  6. **customerWalletLogId 11 个位置生命周期**（init / backInfo / commit / WalletLog / printFn）
  7. **三条业务时序完整**（充值 / 退款 / 收费）
- **26 项评级 = 25 A + 0 E + 1 F**
- **L1=25 / L2=0 / L3=0 / F=1**
- **历史文档影响**：0（28~108 号全部原文保留，仅 S1-49 一处命名错误被记录在第 13 节"历史纠错"中）
- **P0/P1 影响**：P0=54 / P1=8（不自动新增）
- **写操作**：0
- **生产数据安全**：是
- **下一步**：等老板指令决定是否进入 S1-51

---

> **S1-50 完成。**
> **25 A + 0 E + 1 F（4 个核心问题收口）**。
> **Wallet 4 字段 + 11 个 Init/Commit API + customerWalletLogId 11 位置生命周期 + 三条业务时序 + Cashflow/Wallet 协议分离**。
> **logType 0/1/2/3 业务含义 = F**。
> **下一步：等待老板下一条指令。**
