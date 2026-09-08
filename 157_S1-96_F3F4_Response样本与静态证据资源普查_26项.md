# S1-96 F3/F4 Response 样本与静态证据资源定向普查

> **任务名**：S1-96｜F3/F4 Response 样本与静态证据资源定向普查（26项）
> **审计范围**：当前仓库全部资源（controller.js / 7 HTML / 视光之家url.txt / 历史 MD / .gitignore / Git 历史）
> **核心目标**：普查是否存在可用于解释 F3/F4 Response 的真实样本；找不到则正式冻结 F
> **本轮承诺**：0 次 API 调用 / 0 次 Write / 0 次生产数据修改 / 0 次历史资源修改

---

## 1. 审计范围

| 范围 | 状态 | 说明 |
|---|---|---|
| controller.js（2194196 bytes） | ✅ 已审 | F3/F4 API 字符串、F3/F4 result.list 消费全文搜索 |
| 7 HTML（addSaleRecord/deliveryList/getGlassNotifyList/machineOrderCompleted/machineOrderList/payedDetail/payedList） | ✅ 已审 | 0 处 F3/F4 API 字符串 |
| 视光之家url.txt | ✅ 已审 | URL 列表（业务页面入口），非 API 文档 |
| .gitignore | ✅ 已审 | 仅忽略 视光之家url.txt |
| 全仓 164 个 .md 文档 | ✅ 已审 | grep 关键词命中，但**全部是历史审计文档中的引用** |
| .git/hooks/*.sample（14 个） | ✅ 已审 | Git 自带 sample hooks，与项目无关 |
| 0 个 .json / .har / .postman / .yaml / .yml / .http / .xml / .swagger / .openapi 文件 | ✅ 已证 | 全仓搜索 0 命中 |
| 0 个 mock / fixture / test / spec / __snapshots__ / api / swagger / openapi / postman / har / network / sample 目录 | ✅ 已证 | 全仓搜索 0 命中 |
| Git 历史（S1-22 ~ S1-95 共 50+ commits） | ✅ 已审 | `git log -S` 检索 API 字符串与关键字段 |

---

## 2. 证据等级

A = 直接源码/文件证据 / B = 多源互证 / C = 局部 / D = 冲突 / E = 业务推断 / F = 当前资源范围未观察/不可得

**本轮明令禁止**：
- "没找到 = 不存在"（必须用 F 标注）
- 字段名 → 业务含义（E 升 A）
- API 名称 → 业务逻辑（E 升 A）
- 用第三方常见 DTO 补样本（D 升 A）

---

## 3. 仓库全文件类型分布（基线）

| 扩展名 | 数量 | 备注 |
|---|---:|---|
| (空扩展名/目录) | 405 | 主要是 .git 内部 + 目录 |
| .md | 164 | 全部历史审计/侦察文档 |
| .html | 7 | 全部 untracked 临时文件 |
| .sample | 14 | 全部在 .git/hooks（Git 自带） |
| .js | 1 | controller.js（唯一） |
| .txt | 1 | 视光之家url.txt（被 .gitignore 排除） |
| .ps1 / .py | 1+1 | _gen_phase0_placeholders（untracked） |
| .gitignore | 1 | 仅含 `视光之家url.txt` |
| **.json** | **0** | **本项目无 .json 资源** |
| **.har / .postman_collection.json / .postman_environment.json** | **0** | 无 HAR/Postman 资源 |
| **.yaml / .yml** | **0** | 无 yaml 资源 |
| **.xml / .http** | **0** | 无 xml/http 资源 |
| **.swagger / .openapi** | **0** | 无 OpenAPI/Swagger 资源 |
| **.ts / .tsx** | **0** | 无 TypeScript 资源 |

---

## 4. 目标 API 关键词扫描

### 4.1 F3 关键词全仓命中

**关键词**：`getMedicalProductMachineCenterVoList` / `medicalProductMachineCenterPoListJson`

| 命中类型 | 命中数 | 是否真证据 |
|---|---:|---|
| controller.js 真实调用 | 2 | ✅ L3836（F3 Request）/ L3966（F6 Request 共用字段名） |
| 历史 MD 引用 | 100+ | ❌ 全部是 S1-22 ~ S1-95 审计文档的引用 |
| F3 真实 Response 样本 | **0** | ❌ **未发现** |
| F3 Swagger/OpenAPI 描述 | **0** | ❌ **未发现** |
| F3 mock/fixture/test | **0** | ❌ **未发现** |

**A 级结论**：
- F3 API 字符串在 controller.js 全局**仅 L3836 一处真实调用**（已穷举）
- F3 真实 Response 样本：**F**（当前仓库资源范围未发现）
- F3 文档/测试/mock：**F**（当前仓库资源范围未发现）

### 4.2 F4 关键词全仓命中

**关键词**：`getCanBeDeliverySkuInListOfProduct` / `medicalProductIdArray` / `deliveryStockInSkuVoList`

| 命中类型 | 命中数 | 是否真证据 |
|---|---:|---|
| controller.js 真实调用 | 2 | ✅ L3885（deliveryInputCtrl / showDeliveryModal）/ L35054（optometryCtrl / concatMedicalProductStock） |
| 历史 MD 引用 | 400+ | ❌ 全部是 S1-22 ~ S1-95 审计文档的引用 |
| F4 真实 Response 样本 | **0** | ❌ **未发现** |
| F4 Swagger/OpenAPI 描述 | **0** | ❌ **未发现** |
| F4 mock/fixture/test | **0** | ❌ **未发现** |

**A 级结论**：
- F4 API 字符串在 controller.js 全局**2 处真实调用**（已穷举）：
  - L3885 `deliveryInputCtrl`（showDeliveryModal）
  - L35054 `optometryCtrl`（concatMedicalProductStock）
- F4 真实 Response 样本：**F**（当前仓库资源范围未发现）
- F4 文档/测试/mock：**F**（当前仓库资源范围未发现）

---

## 5. F3 / F4 真实 Consumer 全集（关键发现）

### 5.1 F3 真实 Consumer

| # | Controller | 文件行号 | 调用 | 消费字段 |
|---|---|---|---|---|
| 1 | deliveryInputCtrl | L3836 | `getCenterListFactory.saveOrQuery('/admin/getMedicalProductMachineCenterVoList.json', { medicalProductMachineCenterPoListJson: JSON.stringify(arr) })` | L3961: `result.list.map(v => { medicalProductId: v.medicalProduct.id, machineCenterId: v.machineCenter.id })` |

**A 级结论**：F3 在 controller.js 全局**仅 1 个真实 Consumer（deliveryInputCtrl）**。

### 5.2 F4 真实 Consumer（**B 级多源互证关键**）

| # | Controller | 文件行号 | 调用 | 消费字段 |
|---|---|---|---|---|
| 1 | deliveryInputCtrl | L3885 | `getDeliveryListFactory.saveOrQuery('/admin/getCanBeDeliverySkuInListOfProduct.json', { medicalProductIdArray: medicalProductIdArray })` | L3985-3991: `result.list[i].medicalProduct.id` / `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` / `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` |
| 2 | optometryCtrl | L35054 | `new ObjectFactory().saveOrQuery("/admin/getCanBeDeliverySkuInListOfProduct.json", { medicalProductIdArray: medicalProductIdArray })` | L35062-35070: `result.list.forEach(medical => { medicalProductId: medical.medicalProduct.id, medicalProductStocks: medical.deliveryStockInSkuVoList.map(delivery => { stockInSkuId: delivery.stockInSku.id, deliveryCount: delivery.deliveryCount }) })` |

**A 级结论**：F4 在 controller.js 全局**2 个真实 Consumer**（deliveryInputCtrl + optometryCtrl）。

### 5.3 deliveryStockInSkuVoList 完整引用（避免 F3 误证）

| 行号 | 上下文 | 实际 API 来源 |
|---|---|---|
| L3988-3992 | deliveryInputCtrl saveStock | F4 (`getCanBeDeliverySkuInListOfProduct.json`) |
| L16188-16194 | optometryCtrl/machineOrderCtrl saveStock | **getCanBeProcessSkuInListOfProduct.json**（加工，非 F4）|
| L35063-35067 | optometryCtrl concatMedicalProductStock | F4 (`getCanBeDeliverySkuInListOfProduct.json`) |

**A 级结论**：F4 实际 Consumer = 2 个（deliveryInputCtrl + optometryCtrl）；L16188 的 deliveryStockInSkuVoList 来自**加工** API（getCanBeProcessSkuInListOfProduct），与 F4 不同源。

---

## 6. F3 Response 字段可证范围（A 级，但极窄）

### 6.1 deliveryInputCtrl 视角（唯一 Consumer）

| 字段路径 | 行号 | 访问类型 | A-F | L1/L2/L3 |
|---|---|---|---|---|
| `result.list[i].medicalProduct.id` | L3962 | 读（map v.medicalProduct.id） | A | L1 |
| `result.list[i].machineCenter.id` | L3962 | 读（map v.machineCenter.id） | A | L1 |

### 6.2 不可证

| 项 | 原因 | 标注 |
|---|---|---|
| F3 Response 完整字段 | 无样本 / 无后端代码 | F |
| v.medicalProduct 是否有 name / code / ... | 无样本 | F |
| v.machineCenter 是否有 name / code / ... | 无样本 | F |
| F3 Response 是否回显 Request | 无后端代码 | F |
| F3 Response 与 Request 是否一一对应 | 无后端代码 | F |
| F3 Response 元素是否包含 medicalProduct / machineCenter 之外字段 | 无样本 | F |

**A 级结论**：
- Controller 视角 F3 Response 可见字段 = **2 个**（`medicalProduct.id` + `machineCenter.id`）
- 是否有其它字段：**F**

### 6.3 与 S1-95 对照
S1-95 已确认 F3 Response Controller 视角仅 2 字段可证；本轮 S1-96 重新普查未发现任何新证据可证更多字段。**F 边界未缩小**。

---

## 7. F4 Response 字段可证范围（B 级多源互证）

### 7.1 deliveryInputCtrl 视角

| 字段路径 | 行号 | 访问类型 | A-F | L1/L2/L3 |
|---|---|---|---|---|
| `result.list[i].medicalProduct.id` | L3998 | 读（push.medicalProductId） | A | L1 |
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | L3991 | 读（push.stockInSkuId） | A | L1 |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | L3991 | 读（push.deliveryCount） | A | L1 |

### 7.2 optometryCtrl 视角

| 字段路径 | 行号 | 访问类型 | A-F | L1/L2/L3 |
|---|---|---|---|---|
| `result.list[i].medicalProduct.id` | L35070 | 读（push.medicalProductId） | A | L1 |
| `result.list[i].deliveryStockInSkuVoList[j].stockInSku.id` | L35065 | 读（map.stockInSkuId） | A | L1 |
| `result.list[i].deliveryStockInSkuVoList[j].deliveryCount` | L35066 | 读（map.deliveryCount） | A | L1 |

### 7.3 B 级多源互证（A 级互证）

| 字段 | deliveryInputCtrl | optometryCtrl | 是否一致 | 互证等级 |
|---|---|---|---|---|
| `result.list[].medicalProduct.id` | ✅ | ✅ | ✅ 一致 | **B**（2 源互证） |
| `result.list[].deliveryStockInSkuVoList[].stockInSku.id` | ✅ | ✅ | ✅ 一致 | **B**（2 源互证） |
| `result.list[].deliveryStockInSkuVoList[].deliveryCount` | ✅ | ✅ | ✅ 一致 | **B**（2 源互证） |

### 7.4 不可证

| 项 | 原因 | 标注 |
|---|---|---|
| F4 Response 完整字段 | 无样本 / 无后端代码 | F |
| medicalProduct 是否有 name / code / ... | 无样本 | F |
| deliveryStockInSkuVoList 元素是否有 stockInSku.id 之外字段 | 无样本 | F |
| F4 Response 是否回显 Request | 无后端代码 | F |
| F4 Response 与 Request 元素数量关系 | 无后端代码 | F |

### 7.5 与 S1-95 / S1-90 对照
- S1-90 已确认 F4 Response 4 字段 A 级（medicalProductId + stockInSkuId + deliveryCount + listCount）— 但 listCount 是 saveStock 的 Request 字段，不是 Response 字段
- S1-95 未单独审计 F4
- **S1-96 新发现**：
  - F4 真实 Consumer = 2 个（deliveryInputCtrl + optometryCtrl）
  - F4 Response 字段结构在 2 个 controller 中**完全一致** → **B 级多源互证**
  - 字段路径比 F3 更确定（3 字段 + 多源互证）

### 7.6 A 级结论
- F4 Response 可见字段（A 级）= 3 个（`medicalProduct.id` / `stockInSku.id` / `deliveryCount`）
- F4 Response 互证（B 级）= 2 个 controller 字段路径完全一致
- F4 是否有其它字段：**F**

---

## 8. mock / fixture / test / Swagger / OpenAPI / Postman / HAR / Network 普查

### 8.1 目录扫描

| 目录名 | 是否存在 | 备注 |
|---|---|---|
| mock / mocks | ❌ | 不存在 |
| fixture / fixtures | ❌ | 不存在 |
| test / tests / spec / specs | ❌ | 不存在 |
| __snapshots__ | ❌ | 不存在 |
| api | ❌ | 不存在 |
| swagger | ❌ | 不存在 |
| openapi | ❌ | 不存在 |
| postman | ❌ | 不存在 |
| har | ❌ | 不存在 |
| network | ❌ | 不存在 |
| sample / example / examples | ❌ | 不存在 |
| docs | ❌ | 不存在 |

**A 级结论**：全仓**0 个** mock/fixture/test/swagger/openapi/postman/har/network/sample/docs 目录。

### 8.2 文件类型扫描

| 类型 | 是否存在 | 命中文件 |
|---|---|---|
| *.json | ❌ | 0 命中 |
| *.har | ❌ | 0 命中 |
| *.postman_collection.json | ❌ | 0 命中 |
| *.postman_environment.json | ❌ | 0 命中 |
| *.swagger / *.openapi | ❌ | 0 命中 |
| *.yaml / *.yml | ❌ | 0 命中 |
| *.http | ❌ | 0 命中 |
| *.xml | ❌ | 0 命中 |
| *.ts / *.tsx | ❌ | 0 命中 |

**A 级结论**：全仓**0 个** API 文档/Network 导出/Postman collection 资源。

### 8.3 controller.js 硬编码 JSON 扫描

| 模式 | 命中数 | 备注 |
|---|---:|---|
| `result.list = [...]`（F3/F4 Response 真实样本） | 0 | 仅 `result.list = []`（空数组初始化） |
| `medicalProduct: {...}`（F3/F4 Response 元素样本） | 0 | 仅有字段访问，无字面对象 |
| `machineCenter: {...}` | 0 | 仅有字段访问，无字面对象 |
| `deliveryStockInSkuVoList: [...]` | 0 | 仅有字段访问，无字面数组 |

**A 级结论**：controller.js 中**0 处 F3/F4 硬编码 Response 样本**。

### 8.4 其它 7 HTML 扫描

| HTML | F3/F4 命中 |
|---|---|
| deliveryList.html | 0（仅有 sendToMachineCenterList 3 处 F1 字段） |
| addSaleRecord.html / getGlassNotifyList.html / machineOrderCompleted.html / machineOrderList.html / payedDetail.html / payedList.html | 0（与 F3/F4 无关） |

**A 级结论**：7 HTML 中**0 处** F3/F4 API / Response 引用。

### 8.5 视光之家url.txt

- 内容：业务页面 URL 列表（就诊流程、预约叫号、患者维护、营销管理、筛查机构、物资管理、数据报表、诊所管理、收费项目维护等）
- **不包含**任何 F3/F4 API 文档、Response 样本、字段定义
- 标注：与本轮 F3/F4 Response 普查**完全无关**

---

## 9. Markdown / 注释 Response 样本

### 9.1 历史 MD 命中统计

| MD 文件 | F3 命中 | F4 命中 |
|---|---:|---:|
| 123_S1-63_ProcessSku_DeliverySku_StockSku_三协议对照_26项.md | 3 | 多 |
| 124_S1-64_deliveryInputCtrl_五API发货流协议闭环_26项.md | 多 | 多 |
| 125_S1-65_sendMedicalProductToMachineCenter_发加工中心协议闭环_26项.md | 多 | 多 |
| 126_S1-66_deliveryInputCtrl_六API交叉一致性审计冻结_26项.md | 多 | 多 |
| 122_S1-62_deliveryStockInSkuVoList_stockInSku_deliveryCount_26项.md | 0 | 53 |
| 150_S1-89_deliveryInputCtrl_六API最小协议与waitingDeliveryList动作链审计_26项.md | 多 | 多 |
| 151_S1-90_F4到F5_库存保存字段级闭合审计_26项.md | 0 | 47 |
| 152_S1-91_F3到F6_machineCenter发送字段级闭合审计_26项.md | 多 | 0 |
| 153_S1-92_deliveryInput_F3F4结果到前端状态字段分层审计_26项.md | 多 | 多 |
| 154_S1-93_F1_waitingDeliveryList到F3F4入口字段级闭合审计_26项.md | 多 | 多 |
| 155_S1-94_objectId运行时改写与F3F4分流规则审计_26项.md | 多 | 0 |
| 156_S1-95_F3_Request_Response字段对应与F6传递审计_26项.md | 多 | 0 |
| 137_审计勘误与当前有效证据基线_20260904.md | 0 | 2 |
| 139_S1-78 / 137_S1-77 / 136_S1-76 / 141_S1-80 / 146_S1-85 | 少量 | 少量 |

### 9.2 关键判定

| 维度 | 评估 | A-F |
|---|---|---|
| 历史 MD 是否提供 F3 真实 Response 样本 | ❌ 全部是 L3836 调用点的引用 + Request 字段记录；无 Response 字段直接来源 | F |
| 历史 MD 是否提供 F4 真实 Response 样本 | ❌ 全部是 L3885 / L35054 调用点的引用 + Request 字段记录；无 Response 字段直接来源 | F |
| 历史 MD 互证 F3/F4 Response 字段 | 仅是审计文档中的字段名引用（如 `v.medicalProduct.id`），不是真实样本 | F |

**A 级结论**：历史 MD **不构成** F3/F4 Response 真实样本，仅是审计文档对源码字段访问的引用。

### 9.3 其它 MD 类别（README / design / docs / note / changelog / issue / TODO）

- 本项目 MD 文件全部为 0_xxx 至 8_xxx 编号的侦察/审计/收口报告（共 60+ 个）
- 包含业务规则、数据模型、变更记录等
- 全部为审计/侦察输出，**不包含** F3/F4 API 后端 schema 或 Response 样本

---

## 10. 其它 API 是否暴露相同对象结构

### 10.1 全 controller.js 字段搜索

| 字段模式 | 命中位置 | 与 F3/F4 关系 |
|---|---|---|
| `res.result.object.machineCenter` | L422-425 | F1 Response（getCashflowDeliveryVo）的另一种结构，**不**是 F3 |
| `resp.result.object.machineCenter.id` | L16443 | getCompanyMachineCenterOfMine / getChainMachineCenterOfMine 响应，**不**是 F3 |
| `res.object.machineCenter.{status,type,name}` | L56912-56914 | /admin/getMachineCenterVo.json 响应，**不**是 F3 |
| `machineCenterOrder.{receiveStatus,status}` | L4321/L16253 | /admin/receiveMachineCenterOrder.json / /admin/getMachineCenterOrder.json 响应，**不**是 F3 |
| `productArr[i].deliveryStockInSkuVoList` | L16188-16194 | getCanBeProcessSkuInListOfProduct.json 响应，**不**是 F4 |
| `result.list[i].stockInSkuVoList[i].stockInSku.{skuCount,skuOutCount,...}` | 多处 | 其它 API（getProductListFactory 等），**不**是 F4 |

### 10.2 A 级结论

- **不存在**与 F3 Response 字段结构（`{ medicalProduct: {id}, machineCenter: {id} }`）完全相同的其它 API Response
- **不存在**与 F4 Response 字段结构（`{ medicalProduct: {id}, deliveryStockInSkuVoList: [{stockInSku: {id}, deliveryCount}] }`）完全相同的其它 API Response
- 其它 API 即使包含 `machineCenter` / `deliveryStockInSkuVoList` 字段，**都不证明它们是 F3/F4 的同源对象**

---

## 11. Git 历史只读检索

### 11.1 git log -S 关键词命中统计

| 关键词 | 命中 commit 数 | 全部为审计 MD？ |
|---|---:|---|
| `getMedicalProductMachineCenterVoList` | 16 | ✅ 全部是 S1-63 ~ S1-95 审计文档 |
| `getCanBeDeliverySkuInListOfProduct` | 14 | ✅ 全部是 S1-62 ~ S1-95 审计文档 |
| `deliveryStockInSkuVoList` | 14 | ✅ 全部是 S1-61 ~ S1-95 审计文档 |
| `medicalProductMachineCenterPoListJson` | 15 | ✅ 全部是 S1-63 ~ S1-95 审计文档 |
| `medicalProductIdArray` | 13 | ✅ 全部是 S1-62 ~ S1-95 审计文档 |

### 11.2 关键判定

| 维度 | 评估 | A-F |
|---|---|---|
| Git 历史中是否曾有真实 Response 样本 commit | ❌ 0 命中（所有 commit 都是审计 MD 引用 controller.js 已存在的字符串） | F |
| Git 历史中是否曾有 mock/fixture/test commit | ❌ 0 命中 | F |
| Git 历史中是否曾有 Swagger/OpenAPI/Postman/HAR commit | ❌ 0 命中 | F |
| 历史是否曾删除过相关 mock / 文档 | ❌ 无 commit 引入过，所以也无 commit 删除过 | F |
| controller.js 中 F3/F4 API 字符串的首次引入 commit | ❌ 无法通过 git log 找到（controller.js 是 untracked，从未通过 git 提交过） | F |

### 11.3 重要限制

- **controller.js 是 untracked 文件**（从 S1-77 开始持续在 untracked 列表）
- `git log -S <api string>` 命中的是**历史 MD 中引用这些字符串的 commit**，**不是** controller.js 中的 API 字符串引入 commit
- controller.js 的 API 字符串**首次可见**就是当前工作目录版本（untracked），无历史快照可比

---

## 12. 敏感信息检查

| 检查项 | 命中 |
|---|---|
| Cookie | 0 |
| token | 0 |
| authorization | 0 |
| password | 0 |
| secret | 0 |
| 手机号 / 患者信息 | 0 |
| 生产数据 | 0 |

**A 级结论**：在 *.sample / *.json / *.txt 中**0 处敏感信息**命中。

---

## 13. 证据资源目录

| 类型 | 是否存在 | 是否包含 F3/F4 API | 是否存在 Response | 可用于建模 |
|---|---|---|---|---|
| **JS（controller.js）** | ✅ | ✅ 包含 L3836 / L3885 / L35054 调用 | ❌ 仅 Request 字段 / 2-3 个 Response 字段访问 | ✅ 字段访问 / ❌ 完整 Response |
| **HTML（7 个）** | ✅ | ❌ 0 命中 F3/F4 API | ❌ | ❌ |
| **JSON 文件** | ❌ | — | — | — |
| **mock 目录/文件** | ❌ | — | — | — |
| **fixture 目录/文件** | ❌ | — | — | — |
| **test 目录/文件** | ❌ | — | — | — |
| **Swagger / OpenAPI** | ❌ | — | — | — |
| **Postman collection** | ❌ | — | — | — |
| **HAR / Network** | ❌ | — | — | — |
| **Markdown（164 个）** | ✅ | ✅ 引用 API 字符串 | ❌ 仅引用 L3836/L3885/L35054，无 Response 样本 | ✅ 调用关系 / ❌ 完整 Response |
| **Git history（50+ commits）** | ✅ | ✅ 审计 MD 中含 API 字符串 | ❌ 无 Response 样本 commit | ✅ 审计时间线 / ❌ Response |
| **视光之家url.txt** | ✅ | ❌ 业务页面 URL，与 F3/F4 无关 | ❌ | ❌ |
| **.gitignore** | ✅ | 仅忽略 视光之家url.txt | — | — |
| **.sample（.git/hooks）** | ✅ | Git 自带 hooks sample | — | — |

---

## 14. F3 F 边界（最终）

| 项 | S1-95 状态 | S1-96 状态 | 是否缩小 F |
|---|---|---|---|
| F3 Request 字段 | A（medicalProductId + machineCenterId） | A（同 S1-95） | ❌ 已 A |
| F3 Response 字段 | A（仅 2 字段：v.medicalProduct.id + v.machineCenter.id） | A（同 S1-95） | ❌ 已 A（窄） |
| F3 Response 完整 schema | F | F | ❌ 未缩 |
| F3 Response 与 Request 值相等 | F | F | ❌ 未缩 |
| F3 Response 与 Request 元素数量关系 | F | F | ❌ 未缩 |
| F3 Response 元素是否同源 | F | F | ❌ 未缩 |
| F3 后端处理逻辑 | F | F | ❌ 未缩 |
| F3 是否回显/查询/匹配/转换 | F | F | ❌ 未缩 |
| F3 真实 Response 样本 | F | F | ❌ 未缩（资源范围内 0 命中） |
| F3 文档/测试/mock | F | F | ❌ 未缩（资源范围内 0 命中） |
| F3 Consumer 全集 | A（仅 deliveryInputCtrl） | A（同 S1-95） | ❌ 已 A |
| F3 真实 F3 → F6 字段链 | A（除 F3 后端节点 = F） | A（同 S1-95） | ❌ 已 A |

**A 级结论**：F3 的 F 边界**未缩小**。当前仓库资源范围内**未发现** F3 真实 Response 样本或文档。

---

## 15. F4 F 边界（最终）

| 项 | S1-90/S1-95 状态 | S1-96 状态 | 是否缩小 F |
|---|---|---|---|
| F4 Request 字段 | A（medicalProductIdArray） | A（同 S1-90） | ❌ 已 A |
| F4 Response 字段 | A（3 字段：medicalProduct.id / stockInSku.id / deliveryCount，单 Consumer） | **A → B**（2 Consumer 互证） | ✅ **缩小 F** |
| F4 Response 完整 schema | F | F | ❌ 未缩 |
| F4 Response 与 Request 值相等 | F | F | ❌ 未缩 |
| F4 Response 与 Request 元素数量关系 | F | F | ❌ 未缩 |
| F4 Response 元素是否同源 | F | F | ❌ 未缩 |
| F4 后端处理逻辑 | F | F | ❌ 未缩 |
| F4 是否回显/查询/匹配/转换 | F | F | ❌ 未缩 |
| F4 真实 Response 样本 | F | F | ❌ 未缩（资源范围内 0 命中） |
| F4 文档/测试/mock | F | F | ❌ 未缩（资源范围内 0 命中） |
| F4 Consumer 全集 | A（仅 deliveryInputCtrl 已知） | **A → 扩展**（2 个 Consumer: deliveryInputCtrl + optometryCtrl） | ✅ **扩展 A** |

### 15.1 F 边界缩小（A 级证据）

| 缩小项 | 缩小前 | 缩小后 |
|---|---|---|
| F4 Response 字段互证 | A（仅 1 Consumer） | **B（2 Consumer 互证）** |
| F4 Consumer 数量 | 1 (deliveryInputCtrl) | **2 (deliveryInputCtrl + optometryCtrl)** |
| F4 Response 字段路径 | 单 Consumer 观察 | **2 Consumer 字段路径完全一致** |

**A 级结论**：F4 通过 S1-96 的多 Consumer 互证，**F 边界部分缩小**：
- F4 Response 3 字段（`medicalProduct.id` / `stockInSku.id` / `deliveryCount`）从 **A 级（单源）** 升级到 **B 级（多源互证）**
- F4 Consumer 全集从 1 扩展到 2
- F4 后端处理 / 完整 schema / Request↔Response 关系 仍保持 F

---

## 16. 26 项矩阵

| # | 维度 | 证据 / 位置 | A-F | L1/L2/L3 | 备注 |
|---|---|---|---|---|---|
| 01 | F3 关键词全局扫描 | controller.js L3836/L3966 + 100+ 历史 MD 引用 | A | L1 | controller.js L3836 = 真调用，MD = 审计引用 |
| 02 | F4 关键词全局扫描 | controller.js L3885/L35054 + 400+ 历史 MD 引用 | A | L1 | controller.js L3885/L35054 = 真调用 |
| 03 | JS 命中 | F3: L3836 (1) / F4: L3885/L35054 (2) | A | L1 | controller.js 全文 |
| 04 | HTML 命中 | 0 | A | L1 | 7 HTML 全文 |
| 05 | JSON 命中 | 0 | A | L1 | 全仓 0 个 .json 文件 |
| 06 | MD 命中 | 100+ / 400+ | A | L1 | 全部审计文档引用 |
| 07 | mock | 0 | A | L1 | 0 目录 + 0 文件 |
| 08 | fixture | 0 | A | L1 | 0 目录 + 0 文件 |
| 09 | test | 0 | A | L1 | 0 目录 + 0 文件 |
| 10 | Swagger/OpenAPI | 0 | A | L1 | 0 文件 + 0 目录 |
| 11 | Postman | 0 | A | L1 | 0 文件 |
| 12 | HAR/Network | 0 | A | L1 | 0 文件 |
| 13 | F3 Response 样本 | 0 | F | L1=F | 当前仓库资源范围未发现 |
| 14 | F4 Response 样本 | 0 | F | L1=F | 当前仓库资源范围未发现 |
| 15 | F3 其它 Consumer | 0 (仅 deliveryInputCtrl) | A | L1 | controller.js 全文 |
| 16 | F4 其它 Consumer | 1 (optometryCtrl L35054) | A | L1 | controller.js 全文，**S1-96 新发现** |
| 17 | F3 medicalProduct 扩展字段 | F | F | L1=F | 仅 .id 可证（A），其它字段 F |
| 18 | F3 machineCenter 扩展字段 | F | F | L1=F | 仅 .id 可证（A），其它字段 F |
| 19 | F4 deliveryStockInSkuVoList 扩展字段 | 0 | A | L1 | Controller 仅读 .stockInSku.id / .deliveryCount |
| 20 | F4 stockInSku 扩展字段 | 0 | A | L1 | Controller 仅读 .id |
| 21 | Git history | 50+ commits 含 API 字符串 | A | L1 | 全部审计 MD，无 Response 样本 commit |
| 22 | 历史删除资源 | 0 | A | L1 | 无删除 commit |
| 23 | Request/Response 值相等 | F | F | L1=F | 无样本可证 |
| 24 | Request/Response 一对一 | F | F | L1=F | 无后端代码可证 |
| 25 | Request/Response 同源 | F | F | L1=F | HTTP 边界隔断 |
| 26 | F3/F4 最终证据边界 | F3 = A（窄）/ F4 = B（多源）/ 完整 schema = F | A/B/F | L1 | 本轮核心成果 |

**统计**：
- **A：18 项**
- **B：1 项**（#26 F4 字段互证）
- **C：0**
- **D：0**
- **E：0**
- **F：7 项**（#13/14/17/18/23/24/25）
- **E/F 升 A：0**

---

## 17. L1/L2/L3

### L1（源码事实，可证）

- F3/F4 API 字符串 + 行号（A）
- F3/F4 Request 字段 + JSON.stringify 位置（A）
- F3/F4 Consumer 全集（A）
- F3 Response Controller 可见字段 = 2 个（A）
- F4 Response Controller 可见字段 = 3 个（A）
- F4 Response 字段 2 Consumer 互证一致（B）
- 全仓 0 个 mock/fixture/test/swagger/postman/har/yaml/yml/json/http 资源（A）
- controller.js 0 处 F3/F4 硬编码 Response 样本（A）
- 0 处敏感信息（A）
- Git history 50+ commits 全部为审计 MD（A）

### L2（业务解释，未证）

- "F3 是加工中心查询接口"：**E**（未证）
- "F4 是可发货 SKU 查询"：**E**（未证）
- "F3 后端会回显 Request"：**E**（未证）
- "F4 后端会回显 Request"：**E**（未证）
- "medicalProductMachineCenterPoListJson 字符串格式 = 后端 JSON"：**E**（未证）
- "machineCenter 字段包含 name"：**E**（未证）
- "stockInSku 字段包含 batchNo/expiresDate"：**E**（虽然 controller.js 其它处访问 stockInSku.batchNo/expiresDate，但**不证明 F4 stockInSku 包含**）

### L3（DB/Entity/DTO/FK）

- L3 = **F**（无后端代码 / 无 schema 样本 / 无 F3/F4 后端实现）

---

## 18. F 边界（最终汇总）

| 项 | 不可证原因 | 标注 |
|---|---|---|
| F3 Response 完整 schema | 无样本 | F |
| F3 Response 与 Request 值相等 | 无样本 / 无后端代码 | F |
| F3 Response 与 Request 元素数量关系 | 无后端代码 | F |
| F3 后端处理逻辑 | 无后端代码 | F |
| F3 是否回显/查询/匹配/转换 | 无后端代码 | F |
| F3 真实 Response 样本 | 仓库 0 命中 | F |
| F4 Response 完整 schema | 无样本 | F |
| F4 Response 与 Request 值相等 | 无样本 / 无后端代码 | F |
| F4 Response 与 Request 元素数量关系 | 无后端代码 | F |
| F4 后端处理逻辑 | 无后端代码 | F |
| F4 是否回显/查询/匹配/转换 | 无后端代码 | F |
| F4 真实 Response 样本 | 仓库 0 命中 | F |
| F3/F4 文档/测试/mock | 仓库 0 命中 | F |
| 其它 API 是否同源 DTO | 字段名相似 ≠ 同源 | F |
| 字段路径 → DB/Entity/DTO 字段 | 无后端代码 | F（L3） |

---

## 19. 红线核查

| 红线 | 状态 | 证据 |
|---|---|---|
| 启动原系统进行 API 调用 = 0 | ✅ | 未启动任何服务 |
| 浏览器访问 API = 0 | ✅ | 未用浏览器 |
| 发送任何 HTTP 请求 = 0 | ✅ | 未发任何网络请求 |
| F3 实际调用 = 0 | ✅ | 仅静态审计 |
| F4 实际调用 = 0 | ✅ | 仅静态审计 |
| F5 实际调用 = 0 | ✅ | 仅静态审计 |
| F6 实际调用 = 0 | ✅ | 仅静态审计 |
| save / submit / send / delivery / receive / charge / refund / recharge / start / complete / close / notify 全部 0 调用 | ✅ | |
| Production mutation = 0 | ✅ | |
| Historical MD = 0 | ✅ | 仅新增 157 |
| controller.js 未改 | ✅ | git status 不显示 M |
| deliveryList.html 未改 | ✅ | SHA256 = `5B79B6F0E423A90188EE420234A9449531E623528C9807800C5780BD61006476`（不变）/ 12720 bytes（不变）|
| 10 untracked 临时文件原样保留 | ✅ | _gen_phase0_placeholders.ps1/.py + controller.js + 7 HTML |
| P0 = 54 冻结 | ✅ | |
| P1 = 8 冻结 | ✅ | |
| git add . / -A / * / -u 全部禁止 | ✅ | 仅 git add -- 157_*.md |
| 文件编号连续 | ✅ | 156 已被 S1-95 占用，本轮使用 157 |

---

## 20. 最终结论

### 20.1 资源普查核心结果（A 级）

| 资源类型 | 命中 | 用途 |
|---|---|---|
| controller.js | 1（2194196 bytes） | F3/F4 Consumer + Request/Response 字段访问 |
| 7 HTML | 7 | 0 处 F3/F4 |
| 164 MD | 164 | 全部为审计/侦察文档，0 处真实 Response 样本 |
| .json / .har / .yaml / .yml / .postman / .swagger / .openapi / .http / .xml | **0** | **当前仓库无 API 文档 / 测试 / 样本资源** |
| mock / fixture / test / swagger / openapi / postman / har / network / sample 目录 | **0** | **不存在** |
| Git history | 50+ commits | 全部审计 MD commit，无源码 commit 引入 F3/F4 API 字符串 |
| 视光之家url.txt | 1 | 业务 URL 列表，与 F3/F4 无关 |
| .gitignore | 1 | 仅忽略 url.txt |

### 20.2 F3 状态（**F 未缩**）

- **Request**：A（medicalProductId + machineCenterId 字段，JSON.stringify，L3836）
- **Response 字段可见**：A（仅 2 字段：`medicalProduct.id` + `machineCenter.id`，1 Consumer）
- **Response 完整 schema**：F
- **后端处理**：F
- **是否回显/查询/匹配/转换**：F
- **真实样本 / 文档 / mock**：F（仓库 0 命中）
- **F 边界**：**未缩小**

### 20.3 F4 状态（**F 部分缩小**）

- **Request**：A（medicalProductIdArray，L3885/L35054）
- **Response 字段可见**：A（3 字段：`medicalProduct.id` / `stockInSku.id` / `deliveryCount`）
- **字段互证**：**B（2 Consumer 完全一致：deliveryInputCtrl + optometryCtrl）** ← **S1-96 新发现**
- **Response 完整 schema**：F
- **后端处理**：F
- **是否回显/查询/匹配/转换**：F
- **真实样本 / 文档 / mock**：F（仓库 0 命中）
- **F 边界**：**部分缩小**（字段互证 B 级 + Consumer 扩展至 2 个）

### 20.4 与 S1-95 对照

| 维度 | S1-95 | S1-96 | 变化 |
|---|---|---|---|
| F3 Consumer 全集 | 1 (deliveryInputCtrl) | 1 (deliveryInputCtrl) | 不变 |
| F3 Response 字段 | 2 字段 A | 2 字段 A | 不变 |
| F3 Response 互证 | 无 | 无 | 不变 |
| F4 Consumer 全集 | 1 (deliveryInputCtrl) | **2 (deliveryInputCtrl + optometryCtrl)** | **扩展** |
| F4 Response 字段 | 3 字段 A | 3 字段 A | 不变 |
| F4 Response 互证 | 无 | **B（2 源互证）** | **升级** |
| 资源普查 | 未做 | **0 个 mock/fixture/test/文档** | 新增 |

### 20.5 严格表述

- "F3 Response 字段 = 2 字段"：**A**（Controller 视角）
- "F3 Response 字段 = 仅这 2 字段"：**D**（无样本可证，禁止升级）
- "F4 Response 字段 = 3 字段"：**A**（Controller 视角）
- "F4 Response 字段 = 仅这 3 字段"：**D**（无样本可证，禁止升级）
- "F4 字段路径在 2 Consumer 完全一致"：**B**（多源互证）
- "F4 字段路径一致 = F4 真实 Response"：**E**（业务推断，未证 — 业务推断不升 A）
- "F3/F4 后端逻辑"：**F**（无后端代码）
- "F3/F4 Request↔Response 关系"：**F**（无样本）

### 20.6 最终边界

```
F3:
  Request  → A
  Response 字段 → A（窄：2 字段，1 Consumer）
  Response 完整 schema → F
  Response ↔ Request 关系 → F
  后端处理 → F
  真实样本 / 文档 → F（当前仓库 0 命中）

F4:
  Request  → A
  Response 字段 → A（3 字段）
  Response 字段互证 → B（2 Consumer：deliveryInputCtrl + optometryCtrl）  ← S1-96 新增
  Response 完整 schema → F
  Response ↔ Request 关系 → F
  后端处理 → F
  真实样本 / 文档 → F（当前仓库 0 命中）
```

### 20.7 不可在本轮升级为 A 的项

- F3/F4 真实 Response 完整字段（F）
- F3/F4 后端处理逻辑（F）
- F3/F4 Request↔Response 值相等（F）
- F3/F4 Request↔Response 数量关系（F）
- F3/F4 Request↔Response 同源（F）
- F3/F4 业务语义（E）
- 其它 API 同源 DTO（F）
- DB/Entity/DTO/FK 字段映射（L3 = F）

---

**审计结束**。
