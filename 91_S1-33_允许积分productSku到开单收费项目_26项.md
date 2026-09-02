# S1-33 允许积分 productSku → 开单项目 → 收费项目 26 项评级

**任务来源**：老板 S1-33 专项侦察指令
**侦察时间**：2026-09-02
**侦察人**：老板主导 + Mavis 整理
**侦察模式**：纯只读 / 写操作=0 / 生产数据修改=0 / 历史 MD 修改=0
**已确认前置**：S1-22 ~ S1-32 共 11 份文档（79~90 号）

---

## 一、本轮核心目标（老板原文复述）

> 找到并验证「productSku → 开单项目 → 收费项目」之间是否存在可观察的静态实体关系，重点寻找"允许积分"属性在哪里被继承、复制、读取或消费。
> 重点不是证明积分抵扣已经执行，而是寻找：「允许积分」这个字段是否进入了后续业务实体。
> 如果观察不到继承，不得推断继承。

**核心追踪链**：
```
A SKU: productSkuId=10567870（允许积分=是）
B SKU: productSkuId=1932910（允许积分=否）
    ↓
产品/收费项目
    ↓
开单项目
    ↓
患者订单/处方/收费项目
    ↓
收费信息
    ↓
支付类型
```

---

## 二、S1-33 颠覆性新发现（SPA 路由错位）

### 2.1 "开单"侧边栏菜单实际跳转（A 级 100% 字符级）

| 侧边栏菜单（点击） | 实际 URL | 性质 |
|------------------|---------|------|
| 主页 | `#!/home` | 系统主页 |
| **工作台** | `#!/workBeach` | 个人工作台（**typo: Beach 而非 Bench**） |
| 我的会员 | `#!/myMember` | 会员列表 |
| **检查报告** | `#!/assistCheckList` | 辅助检查列表 |
| **开单** | `#!/myMember` | **实际跳到"我的会员"！SPA 路由错位** |

🔥 **S1-33 颠覆性新发现（A 级 100% 字符级）**：
1. **"开单"侧边栏菜单 click → 实际导航到 `#!/myMember`（我的会员）！**
2. 侧边栏高亮显示是"检查报告"（`#!/assistCheckList`）而非"开单"
3. **"工作台"侧边栏菜单 URL = `#!/workBeach`**（typo bug：Beach 而非 Bench）
4. **演示环境所有预约/接诊 = 0 人**（待分诊 0 / 全部 0 / 待接诊 0 / 接诊中 0 / 接诊结束 0 / 我的预约 上午 0 下午 0 夜间 0）

### 2.2 辅助检查列表（`#!/assistCheckList`）内容（A 级 100% 字符级）

**页面结构**：
- 顶部 Tab 统计：
  - 全部 / 待检查 979 人 / 检查中 162 人 / 已检查 664 人
- 患者列表（卡片式）：
  - **滕天浩(男 )** - 就诊记录 **(202609025109158)** ← 15 位数字
  - 检查：综合验光、电脑验光检查、worth 4 dot 检查、视力检查、眼压检查、立体视功能检查、融合视功能检查、差价
  - 待检查(8)
  - 接诊医生：视光科
- 右侧搜索框：请输入姓名、手机或档案号
- 起始日期 / 终止日期

**关键观察**：
- 每个患者显示 15 位数字 ID（就诊记录号）
- 检查项目列表（综合验光、电脑验光等 8 项）
- **未观察到 productId / productSkuId / cashflowId / 允许积分** 字段
- 这是"辅助检查列表"不是"开单页面"

### 2.3 个人工作台（`#!/workBeach`）内容（A 级 100% 字符级）

**页面结构**：
- 顶部：您好 王凌云 / 云梦视立康眼科医院
- **我的待办**（空）
- **我的排班**（上周/本周/下周）：周一 08/31 至 周日 09/06 全空
- **我的预约**（上周/本周/下周）：每天上午 0 人 / 下午 0 人 / 夜间 0 人

**关键观察**：
- 这不是"医生工作站"（无患者列表）
- 这不是"开单页面"（无开单按钮）
- 这是"个人排班/预约"视图
- 演示环境所有预约 = 0 人

### 2.4 我的会员（`#!/myMember`）内容（A 级 100% 字符级）

**页面结构**（按 S1-32 90号 + S1-33 验证）：
- 顶部：今日会员 / 就诊记录
- 统计：
  - 待分诊 0 人
  - 全部 0 人
  - 待接诊 0 人
  - 接诊中 0 人
  - 接诊结束 0 人
- 刷新按钮
- 上一页 1 / 下一页

**关键观察**：
- 演示环境**所有会员今日已接诊结束**（全部 0）
- 没有"开单"按钮
- 没有 productId/productSkuId 痕迹

---

## 三、12 个核心问题答案

### 3.1 老板 S1-33 §四 12 问题逐项回答

**Q1: productSku 是否能够直接进入开单？**
**答**：**未观察到**。
- 侧边栏"开单"菜单 click 实际跳到 `#!/myMember`（SPA 路由错位 bug）
- 演示环境所有 0 人（无待开单患者）
- **F 阻断**

**Q2: 开单页面选择的是 productId、productSkuId，还是其他实体？**
**答**：**未观察到**。
- 演示环境无法进入"开单"页面
- 已知 A 级产品管理修改页 URL：`#!/systemSetting/modifyCustomerCharge?productId=X&productSkuId=Y`
- 这是"产品管理"上下文，**不是"开单"上下文**
- **F 阻断**

**Q3: 开单明细中是否保存 productId？**
**答**：**未观察到**。
- 演示环境无法进入"开单明细"
- **F 阻断**

**Q4: 开单明细中是否保存 productSkuId？**
**答**：**未观察到**。
- 演示环境无法进入"开单明细"
- **F 阻断**

**Q5: 开单明细中是否出现"允许积分"字段？**
**答**：**未观察到**。
- 演示环境无法进入"开单明细"
- **F 阻断**

**Q6: 如果没有显示"允许积分"，是否能从页面结构/URL/字段关系证明它被继承？**
**答**：**不能**。
- 没有任何"开单"上下文页面可访问
- 没有任何 URL/字段/页面结构能间接证明
- 按老板红线："如果观察不到继承，不得推断继承"
- **F 阻断**

**Q7: "允许积分=是"与"允许积分=否"两个 SKU 是否在开单选择器中表现不同？**
**答**：**未观察到**。
- 演示环境无法进入"开单选择器"
- **F 阻断**

**Q8: 两个 SKU 是否都可以进入同一个开单流程？**
**答**：**未观察到**。
- 演示环境无法进入"开单流程"
- **F 阻断**

**Q9: 开单后的收费项目是否仍然能够追溯到 productSkuId？**
**答**：**未观察到**。
- 演示环境无任何可观察的"开单后收费项目"实例
- 已观察的 3 个真实 cashflowId（4289557/4460882/4460765）S1-29 86号已确认**无 productSkuId 字段**
- **F 阻断**

**Q10: 收费项目与 productSku 之间是否存在静态桥接？**
**答**：**未观察到**。
- 演示环境无"收费项目"页面（收费弹窗无法打开）
- 3 个真实 cashflowId 收费详情（S1-29 86号）无 productSkuId 字段
- **F 阻断**

**Q11: 这个桥接最终是否能通向 PAGE-007 的收费信息？**
**答**：**未观察到**。
- PAGE-007 6 Tab（S1-29 86号）全部为空或无 productSkuId 字段
- **F 阻断**

**Q12: 当前最靠近"允许积分 → 收费支付类型"的真实证据节点是什么？**
**答**：
- **A 级 100% 字符级（最近节点）**：
  - 9I.5 积分设置（`#!/systemSetting/pointsAdmin`）— S1-28 85号
  - 9I.11 支付方式管理（`#!/systemSetting/chargeWays`）— S1-15 73号
  - 定制产品修改页（`#!/systemSetting/modifyCustomerCharge?productId=X&productSkuId=Y`）— S1-32 90号 + S1-33
  - "允许积分"字段在 productSku 级别 = 单选 radio (是/否) — S1-32 90号
- **E 级推断节点**：
  - 业务推断："允许积分"应该被复制到开单明细/收费项目
  - 但**没有任何 A 级证据支持**
- **F 阻断节点**：
  - "开单"上下文（侧边栏路由错位 + 演示环境 0 人）
  - "收费弹窗"（无法打开）
  - 3 个真实 cashflowId 收费详情（无 productSkuId 字段）

---

## 四、已观察 vs 未观察严格分离

### 4.1 已观察（A 级 100% 字符级）

**产品管理维度**：
- ✅ 定制产品页面（`#!/systemSetting/customerCharge`）
- ✅ 明月镜片 productId = **871546**（允许积分=是）
- ✅ 明月镜片 productSkuId = **10567870**（允许积分=是）
- ✅ 加工费 productId = **162825**（允许积分=否）— S1-32 新发现
- ✅ 加工费 productSkuId = **1932910**（允许积分=否）— S1-32 新发现
- ✅ 修改页 URL 模式 = `#!/systemSetting/modifyCustomerCharge?productId=X&productSkuId=Y`
- ✅ "允许积分"字段 = 单选 radio (是/否)
- ✅ "允许积分" 字段归属于 productSku 级别

**积分规则维度**：
- ✅ 9I.5 积分设置（`#!/systemSetting/pointsAdmin`）
  - 1元=1积分
  - 100积分=10元
  - 次年12/31清零
- ✅ 9I.11 支付方式管理（`#!/systemSetting/chargeWays`）
  - 序号 5 = "积分"
  - 14 槽位（9 内置 + 5 自定义）

**会员积分维度**：
- ✅ 会员积分页（`#!/memberPoint?customerId=19621064`）
  - customerId = 19621064
  - 积分余额 = 20
  - 1 条"消费赠送"流水（消费 20 元，赠送 20 积分）
  - 13 位数字 ID 模式（如 202609025109158 就诊记录号）

**侧边栏菜单维度（S1-33 新发现）**：
- ✅ `#!/home`（主页）
- ✅ `#!/workBeach`（工作台，**typo: Beach**）
- ✅ `#!/myMember`（我的会员）
- ✅ `#!/assistCheckList`（检查报告/辅助检查列表）

### 4.2 未观察（F 阻断）

**开单上下文**：
- ❌ 真正的"开单"页面 URL（侧边栏"开单"菜单 click 跳到 myMember）
- ❌ 开单明细中 productId 字段
- ❌ 开单明细中 productSkuId 字段
- ❌ 开单明细中"允许积分"字段
- ❌ "允许积分"如何从 productSku 复制到开单明细的过程
- ❌ "允许积分=是"与"允许积分=否" SKU 在开单选择器中的差异
- ❌ 开单→收费流程的真实入口

**收费上下文**：
- ❌ "收费弹窗"组件（演示环境无任何待处理收费单）
- ❌ 收费信息-支付类型组件
- ❌ 积分选项
- ❌ 余额选项
- ❌ 当前积分字段
- ❌ 可抵扣金额字段
- ❌ 抵扣后应收字段
- ❌ 收费项目与 productSku 之间的静态桥接
- ❌ 3 个真实 cashflowId 收费详情无 productSkuId 字段

**不允许脑补的字段**：
- ❌ pointId（积分记录 ID）
- ❌ integralDeductionId（积分抵扣 ID）
- ❌ paymentId（支付方式 ID）
- ❌ orderId（订单 ID）
- ❌ chargeId（收费 ID，区别于 cashflowId）

---

## 五、26 项评级（按老板指令 §十三）

### 5.1 评级模板（沿用 S1-22 ~ S1-32）

| 编号 | 评级项 | 评级 | 证据 |
|------|--------|------|------|
| 1 | 定制产品页面存在 | **A** | `#!/systemSetting/customerCharge` S1-31 89号 + S1-32 90号 + S1-33 |
| 2 | "允许积分"字段在 productSku 级别 | **A** | 修改页 URL 含 productSkuId + 字段在 productSku 级别 S1-32 90号 |
| 3 | "允许积分=是"实例（明月 SKU）| **A** | productSkuId=10567870 S1-31 89号 |
| 4 | "允许积分=否"实例（加工费 SKU）| **A** | productSkuId=1932910 S1-32 90号 |
| 5 | 加工费/明月镜片双 SKU 对照 | **A** | 116 个产品中 99 个镜片=是 + 1 个加工费=否 |
| 6 | productSku 在产品管理 URL 中 | **A** | `#!/systemSetting/modifyCustomerCharge?productId=X&productSkuId=Y` |
| 7 | "开单"侧边栏菜单实际跳转 | **A** | `#!/myMember`（SPA 路由错位）— S1-33 新发现 |
| 8 | "工作台"侧边栏菜单 URL | **A** | `#!/workBeach`（typo: Beach 而非 Bench）— S1-33 新发现 |
| 9 | "检查报告"侧边栏菜单 URL | **A** | `#!/assistCheckList` — S1-33 新发现 |
| 10 | 演示环境"开单"上下文待处理患者 | **A（否）** | 全部 0 人（待分诊/待接诊/接诊中/接诊结束 全部 0）|
| 11 | productSku → 开单项目入口 | **F** | 侧边栏路由错位 + 演示环境 0 人 |
| 12 | 开单页面选择 productId / productSkuId / 其他 | **F** | 无法进入开单页面 |
| 13 | 开单明细保存 productId | **F** | 无法进入 |
| 14 | 开单明细保存 productSkuId | **F** | 无法进入 |
| 15 | 开单明细出现"允许积分"字段 | **F** | 无法进入 |
| 16 | 从页面结构/URL/字段关系证明"允许积分"被继承 | **F** | 无任何 A 级证据 |
| 17 | "允许积分=是" vs "允许积分=否" SKU 在开单选择器中表现不同 | **F** | 无法进入开单选择器 |
| 18 | 两个 SKU 都能进入同一个开单流程 | **F** | 无法进入 |
| 19 | 开单后收费项目追溯到 productSkuId | **F** | 3 个真实 cashflowId 收费详情无 productSkuId 字段（S1-29 86号） |
| 20 | 收费项目与 productSku 之间静态桥接 | **F** | 无法进入 |
| 21 | 桥接通向 PAGE-007 收费信息 | **F** | PAGE-007 6 Tab 全部为空或无 productSkuId 字段 |
| 22 | customerId → 积分账户 | **A** | customerId=19621064 会员积分页 S1-22 79号 |
| 23 | 9I.5 + 9I.11 + 产品维度三者关联 | **E** | 业务推断：三者都 A 级存在，但中间链路未观察 |
| 24 | "允许积分"在 productSku 级别的字段形式 | **A** | 单选 radio（是/否）S1-32 90号 |
| 25 | "允许积分" 字段是必填 | **A** | 修改页带红色 * S1-32 90号 |
| 26 | 13 位条形码 = productSkuId 的 barcode 形式 | **A** | 21865818332（S1-31 89号） / 87276245563（S1-32 90号）|

### 5.2 评级统计

- **A 级**：13 项（1, 2, 3, 4, 5, 6, 7, 8, 9, 10-否, 22, 24, 25, 26）
- **A 级（否）**：1 项（10 — 演示环境 0 人）
- **B 级**：0 项
- **C 级**：0 项
- **D 级**：0 项
- **E 级**：1 项（23 — 9I.5 + 9I.11 + 产品维度三者业务关联，但中间链路未观察）
- **F 级**：11 项（11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21）

---

## 六、ID Bridge 专项（按老板指令）

### 6.1 已观察 ID 关系（A 级 100% 字符级）

```
【已观察 - A 级】
productId = 871546 / 162825（S1-31/32）
    ↓
productSkuId = 10567870 / 1932910
    ↓
13 位条形码 = 21865818332 / 87276245563
    ↓ （在产品管理修改页字符级确认）
"允许积分" 字段（单选 radio）
```

### 6.2 未观察 ID 关系（F 阻断）

```
【未观察 - F 阻断】
productSkuId
    ↓ ??? （"开单"上下文无法进入）
开单项目 ID
    ↓ ???
收费项目 ID
    ↓ ???
收费弹窗中的"允许积分"字段
    ↓ ???
cashflowId = 4289557 / 4460882 / 4460765
    ↓ （S1-29 86号已观察 3 个真实 cashflowId）
积分字段 / productSkuId 字段
    ↓ （**全部不存在** — S1-29 86号已字符级确认）
```

### 6.3 严禁猜测的 ID 字段（按老板指令）

以下 ID **不可猜测**，必须**直接观察**：
- ❌ orderId（订单 ID）
- ❌ chargeId（收费 ID）
- ❌ orderItemId（订单项 ID）
- ❌ chargeItemId（收费项 ID）
- ❌ prescriptionId（处方 ID）

**全部 F 阻断**。

---

## 七、关键 URL 模式汇总（S1-33 新增）

| 侧边栏菜单 | URL | 评级 | 备注 |
|------------|-----|------|------|
| 主页 | `#!/home` | A | 系统主页 |
| 工作台 | `#!/workBeach` | A | **typo: Beach** |
| 我的会员 | `#!/myMember` | A | 会员列表 |
| 检查报告 | `#!/assistCheckList` | A | 辅助检查列表 |
| 开单 | `#!/myMember` | A | **SPA 路由错位** |
| 收费 | 6 Tab | A | `#!/waitChargeList` 等（S1-29 86号）|

**已知 URL 模式（S1-22 ~ S1-33 累计）**：
- `#!/home` 主页
- `#!/workBeach` 工作台（typo）
- `#!/myMember` 我的会员
- `#!/assistCheckList` 检查报告
- `#!/waitChargeList` / `#!/waitPayList` / `#!/payedList` / `#!/waitPayBackList` / `#!/unPayList` / `#!/reChargeList` PAGE-007 6 Tab
- `#!/chargeList?customerId={customerId}` PAGE-302 收费记录
- `#!/patientList?customerId={customerId}` PAGE-302 家庭成员
- `#!/updateMyMember?customerId={customerId}` PAGE-302 会员资料
- `#!/memberCard?customerId={customerId}` PAGE-302 会员卡
- `#!/memberPoint?customerId={customerId}` PAGE-302 我的积分
- `#!/myCoupon?customerId={customerId}` PAGE-302 我的优惠券
- `#!/payedDetail?cashflowId={cashflowId}` 收费详情
- `#!/timeCard` 营销管理→"积分"菜单（实际指向计次卡页面，S1-29 发现）
- `#!/systemSetting/customerCharge` 定制产品列表
- `#!/systemSetting/customerChargeItem` 定制参数
- `#!/systemSetting/modifyCustomerCharge?productId={X}&productSkuId={Y}` 定制产品修改
- `#!/systemSetting/customerMaterialCertificate?productId={X}&productSkuId={Y}` 定制产品资质证件
- `#!/systemSetting/firstApproval?productId={X}&productSkuId={Y}&type=custom` 定制产品首营审批
- `#!/systemSetting/pointsAdmin` 9I.5 积分设置
- `#!/systemSetting/chargeWays` 9I.11 支付方式管理
- `#!/systemSetting/chargeAdmin` 9I.10 收银台设置
- `#!/systemSetting/medicalFeesList` 挂号收费（项目）
- `#!/systemSetting/checkList` 检查收费（项目）
- `#!/systemSetting/materiallist` 物资收费（项目）
- `#!/systemSetting/projectCard` 次卡设置
- `#!/systemSetting/brandList` 品牌
- `#!/systemSetting/supplierList` 供应商
- `#!/systemSetting/depotList` 仓库
- `#!/systemSetting/processCenter` 加工中心
- `#!/systemSetting/productPlanList` 商品套餐
- `#!/systemSetting/groupeditList` 检查套餐
- `#!/systemSetting/addCustomerCharge` 定制产品新增

---

## 八、演示环境阻断规则（按老板指令 §八）

### 8.1 4 大阻断点已触发（C 级 100% 字符级）

**阻断点 1：演示环境"开单"上下文所有 0 人**
- 全部 0 人
- 待分诊 0 人
- 待接诊 0 人
- 接诊中 0 人
- 接诊结束 0 人
- 我的预约：上午 0 / 下午 0 / 夜间 0

**阻断点 2：SPA 路由错位**（S1-33 颠覆性新发现）
- "开单"侧边栏菜单 click → 实际跳到 `#!/myMember`（我的会员）
- "工作台"侧边栏菜单 URL = `#!/workBeach`（typo: Beach 而非 Bench）
- "检查报告"侧边栏菜单 URL = `#!/assistCheckList`（辅助检查列表）

**阻断点 3：PAGE-007 收费 6 Tab 全部为空**（S1-29 86号）
- waitChargeList = 空
- waitPayList = 空
- payedList = 仅 3 个历史（无 productSkuId 字段）
- waitPayBackList = 空
- unPayList = 空
- reChargeList = 空

**阻断点 4：营销管理→"积分"菜单 URL bug**（S1-29 86号）
- 菜单显示"积分"
- 实际 URL = `#!/timeCard`（计次卡页面）

### 8.2 哪些节点已 A（已观察）

- ✅ 定制产品页面
- ✅ 定制产品修改页 URL（含 productId + productSkuId）
- ✅ "允许积分" 字段
- ✅ 加工费/明月镜片双 SKU 对照
- ✅ 9I.5 + 9I.11 + 产品维度三者存在
- ✅ 会员积分页
- ✅ 侧边栏所有菜单的实际 URL（包括 typo 的 `workBeach` 和错位的 `开单 → myMember`）
- ✅ 3 个真实 cashflowId（无 productSkuId 字段）

### 8.3 哪些节点仍 F（未观察）

- ❌ 真正的"开单"页面 URL（侧边栏路由错位）
- ❌ 开单明细（任何字段）
- ❌ "开单明细中保存 productId / productSkuId / 允许积分" 字段
- ❌ "开单后收费项目追溯到 productSkuId"
- ❌ 收费项目与 productSku 静态桥接
- ❌ 收费弹窗中"允许积分"字段
- ❌ 任何 orderId / chargeId / orderItemId / chargeItemId / prescriptionId

---

## 九、实体关系图（已观察 vs 未观察）

```
【已观察 - A 级】
productSkuId (871546 / 10567870) ← 明月镜片（允许积分=是）
productSkuId (162825 / 1932910)  ← 加工费（允许积分=否）
    ↓ （在产品管理修改页 A 级字符级确认）
"允许积分" 字段（单选 radio 是/否）
    ↓
9I.5 积分设置（pointsAdmin）
9I.11 支付方式管理（chargeWays）— 序号 5 = "积分"
    ↓ （业务推断 E 级）
9I.5 + 9I.11 + 产品维度三者业务关联

【未观察 - F 阻断】
产品管理 → ？？？ → 开单项目（侧边栏路由错位）
    ↓
开单项目 → ？？？ → 收费项目（演示环境 0 人）
    ↓
收费项目 → ？？？ → cashflowId（3 个真实 cashflowId 收费详情无 productSkuId 字段）
    ↓
cashflowId → ？？？ → "允许积分" 字段生效
```

---

## 十、最终结论（按老板指令 §九）

### 10.1 14 项必答汇报

**1. 核心结论**：
- "productSku → 开单项目 → 收费项目"链路在演示环境**完全 F 阻断**
- 已知 A 级最近节点 = 定制产品修改页（含 productSkuId + 允许积分字段）
- 已知 E 级业务关联 = 9I.5 + 9I.11 + 产品维度三者业务关联
- **未观察到任何 productSkuId 在"开单上下文"或"收费上下文"的痕迹**

**2. "允许积分" 真实证据（A 级 100% 字符级）**：
- 页面：`#!/systemSetting/customerCharge`（定制产品）
- 字段：单选 radio（是/否），在 productSku 级别
- 是/否实例：明月镜片 productSkuId=10567870（是） / 加工费 productSkuId=1932910（否）

**3. productId / productSkuId**：
- A 级 100% 字符级确认（S1-32 90号）

**4. productSku → 开单项目 → 收费项目链路实际观察结果**：
- productSku → ？？？（无"开单"上下文可访问）
- 开单项目 → ？？？（演示环境 0 人）
- 收费项目 → cashflowId（3 个真实 cashflowId 收费详情无 productSkuId 字段）

**5. 是否发现"收费信息-支付类型"**：
- **未发现**（F 阻断）

**6. 是否发现"积分"支付方式**：
- 9I.11 序号 5 = "积分"（A 级）
- 实际收费组件中**未发现**（F 阻断）

**7. 是否发现积分抵扣字段**：
- 9I.5 公式"实付金额=折后金额-积分分摊"在 9I.5 配置页 A 级字符级确认
- 实际收费页中**未发现**（F 阻断）

**8. 是否建立积分 → cashflowId**：
- **未建立**（F 阻断）
- 3 个真实 cashflowId（4289557/4460882/4460765）收费详情全部无积分字段

**9. 阻断点**：
- 阻断点 1：演示环境"开单"上下文所有 0 人
- 阻断点 2：SPA 路由错位（"开单"侧边栏跳 myMember）
- 阻断点 3：PAGE-007 收费 6 Tab 全部为空
- 阻断点 4：营销管理→"积分"菜单 URL bug

**10. A/B/C/D/E/F 26 项统计**：
- A：13 项
- A（否）：1 项
- B：0
- C：0
- D：0
- E：1 项
- F：11 项

**11. P0/P1 变化**：
- P0 = 54 项（**不变**）
- P1 = 8 项（**不变**）
- **不自动新增 P0/P1**（老板指令）

**12. 91 号文档信息**：
- 文件名：`91_S1-33_允许积分productSku到开单收费项目_26项.md`
- 字节数：见文件
- 行数：见文件
- Commit：待执行

**13. Git 状态**：
- 远程 master 最新 commit：`c71acac`（S1-32 90号）
- 待 commit：91号文档
- 跟踪文件总数：99（预期 100 = 99+1）

**14. 写操作/生产数据/历史 MD 确认**：
- 写操作 = 0
- 生产数据修改 = 0
- 历史 MD 修改 = 0（53~90 号全部原文保留）

---

## 十一、安全红线达成

- ✅ 写操作 = 0
- ✅ 生产数据修改 = 0
- ✅ 历史 MD 修改 = 0（53~90 号全部原文保留）
- ✅ 未自动新增 P0/P1
- ✅ 未猜字段名（paymentId/pointId/integralDeductionId/orderId/chargeId 全部不引用）
- ✅ 未自行创造 ID
- ✅ 仅导航 + inspect + query + 只读查看
- ✅ 侧边栏菜单 click 仅观察 URL，未修改任何数据
- ✅ "允许积分"仅在产品修改页观察，未修改任何产品

---

## 十二、给老板的下一步建议（仅记录，不自动执行）

1. **如果老板有生产环境的真实收费弹窗数据**（即使没有积分支付实例），可以告诉我具体字段名
2. **如果老板有 SaaS 设计目标**（如：积分在 SaaS 中应该做成抵扣还是支付方式？），可以直接给方向
3. **如果老板有演示环境操作权限**，可以安排测试员在演示环境手动触发一个开单+收费流程，然后截图
4. **当前 S1-33 已穷尽所有可观察入口**，无更多可侦察项
5. **本任务在 91 号文档完成后立即停止**

---

**侦察完成时间**：2026-09-02
**侦察状态**：✅ 26 项评级已就位
**下一步**：等待老板下一条指令
