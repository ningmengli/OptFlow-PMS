# 234B S1-168 前 ID 类型后端 Schema 证据核验 V2

> **本轮定位**:S1-168 前最终 ID 类型证据核验 V2。
> - 严禁修改任何历史 MD、controller.js、HTML、配置、数据库
> - 本报告**仅基于真实代码证据**逆向核验,不基于 229/233/234 已有结论
> - 证据评级:**A**=直接数据库/Entity / **B**=多源后端 / **C**=API 局部 / **D**=冲突 / **E**=业务推断 / **F**=未观察
> - **关键原则**:"宁可 BLOCK,不要猜"

---

## §0 完整性闸门

- **HEAD**:`1bf472c39812d88ad41c2e8a0570ddf37ab0e8fc`(S1-168 盲测审计后)
- **REMOTE**:同 LOCAL ✓
- **0 号闸门**:4 文件 SHA256 全部 PASS
- **历史 MD(190~234A 共 46 份)未修改** ✓
- **本轮不写代码、不提交 Git** ✓

---

## §1 仓库是否存在后端

### 1.1 完整文件类型清单(排除 .git)

| 扩展名 | 数量 | 性质 |
|---|---:|---|
| `.md` | 242 | 文档 / 审计报告 |
| `.html` | 7 | 前端模板 |
| `.js` | 1 | `controller.js`(前端 AngularJS) |
| `.py` | 1 | `_gen_phase0_placeholders.py`(占位符生成) |
| `.ps1` | 1 | `_gen_phase0_placeholders.ps1`(占位符生成) |
| `.txt` | 1 | `视光之家url.txt`(已 ignored) |

### 1.2 后端文件 = **0 个**

**关键证据:本仓库不存在以下任何后端文件类型**:

| 扩展名 | 数量 | 通常用途 |
|---|---:|---|
| `.java` | **0** | Java 实体 / Service / Controller |
| `.kt` | **0** | Kotlin 源码 |
| `.sql` | **0** | DDL / DML 脚本 |
| `.xml` | **0** | MyBatis Mapper / Spring 配置 |
| `.yml` / `.yaml` | **0** | Spring Boot / 数据库配置 |
| `.ts` / `.tsx` | **0** | TypeScript |
| `.vue` | **0** | Vue 组件 |
| `.properties` | **0** | Java 配置 |
| `.proto` | **0** | Protobuf |

**本仓库 = 纯前端项目**(AngularJS controller.js + HTML 模板 + MD 文档)。

### 1.3 已扫描的关键证据源

| 文件 | 性质 | 关键内容 |
|---|---|---|
| `controller.js` (59K 行) | 前端 JS | ID 用法、parseInt 模式、数字字面量 |
| `04_数据模型.md` (14KB) | 文档 | 60+ 数据库表名(无 ID 类型)|
| `105_S1-46_核心业务编号与数据库模型边界专项侦察_26项.md` (34KB) | 文档 | ID 数值证据 + 数据库主键边界 |
| `210_S1-147_Customer_Patient_CustomerCheckin身份链与MedicalRecord上游边界总审计.md` (47KB) | 文档 | Customer / Patient ID 证据 |
| `214_S1-151_Clinic_Company_Shop_Department_Employee_Role_SystemSetting权限底座总审计.md` (44KB) | 文档 | Company / Employee / ConsultRoom ID 证据 |
| `216_S1-153_Appointment_预约排班_叫号_诊室屏全生命周期总审计.md` (53KB) | 文档 | BigScreen ID 证据 |
| `221_S1-158_诊所管理子模块逐页面API_Object_Write全量审计.md` (46KB) | 文档 | 诊所管理 |
| 7 个 `.html` | 前端模板 | ID 字段绑定(`{{...id}}`)|

### 1.4 跨文档 SQL / Java 证据搜索

| 搜索模式 | 命中数 |
|---|---:|
| `CREATE TABLE` | 0 |
| `ALTER TABLE` | 0 |
| `PRIMARY KEY` / `FOREIGN KEY` | 0 |
| `BIGINT` | 27(全部在 MD 业务推断段,**E 级**)|
| `@Entity` / `@Id` / `@Table` / `@Column` | 0 |
| `private Long` / `private Integer` / `private String` | 0 |
| `import java.` / `import javax.` | 0 |
| `public class` / `public static` | 0 |
| UUID 字符串字面量 | 0(controller.js 全文) |
| 32 字符十六进制 | 0 |

---

## §2 Company(companyId)

### 2.1 字段名证据(A 级)

**【证据】**:
- 214 S1-151 §1.1:`companyId | **127** | A` 命中
- 214 §1.6:`A. Core ID | companyId | A`
- 214 §11.1:`companyId | Source A: $stateParams / login response (L14239 corpId) ... | 等级: A`
- 105 §6.1:未列 companyId(但列了 `customer.id` / `patient.id` 同类)

**结论**:`companyId` 字段名 A 级确认。

### 2.2 类型证据

**【证据 A】**:
- 214 §1.4 L96-99:`loginCtrl L14239: localStorage.setItem("corpid", corpId)`
- 214 §1.5:「corpInfo 实际是**字符串**,在 JS 端是 `var corpInfo = localStorage.getItem('corpInfo')` (字符串)」
- controller.js L1144-1146:corpid 从 localStorage 读取,用作字符串拼接 key
- controller.js L420:`$scope.object.companyId = res.result.object.company.id;` ← **company.id 派生自 response,具体类型未观察**
- controller.js L36962:`companyId=" + $scope.obj.companyId` ← 字符串拼接(JS 自动转换)

**【证据 E】**:
- 105 §8.1:**company.id 不在表**(只列 cashflow / medicalRecord / patient / customer / medicalProduct / machineCenterOrder / machineCenterId)
- 105 §8.2 严格禁止:"❌ 不能说原系统数据库就是 MySQL BIGINT"

**结论**:
- **companyId 字段名:A 级确认**
- **companyId 是"数值"语义**:**C 级(局部)** — 未在 105 §6.1 数值表中列出,只有 response 字段引用
- **数据库物理类型 / Java POJO 类型**:**F 级(未观察)**
- **数字字面量证据:0** — controller.js 中 companyId 无数字字面量

### 2.3 风险

**HIGH**:如果 S1-168 DDL 写 companyId = BIGINT,**F 级推断**。如果实际是 UUID / String / Long,DDL 错。

---

## §3 Customer(customerId)

### 3.1 字段名证据(A 级)

**【证据】**:
- 214 §1.1:未单独列 customerId(但在 §11.1 列出)
- 105 §6.1 L377:`customer.id | Customer 主键 | 数值 | res.object.customer.id | **A 100%**`
- 101 S1-42 L92:`customerId(仅 PAGE-302)✅ getCustomerVo Customer A 仅在会员卡路由用`
- 101 S1-42 L104-106:数字字面量 `customerId=19621064`(8 位数字)实际出现在 URL
- 101 S1-42 L386:`patientId | Patient 实体 ID | 严禁与 customerId 合并`

**结论**:`customerId` 字段名 A 级确认。

### 3.2 类型证据

**【证据 A】**:
- 105 §6.1 L377:`customer.id` 字段名 + 数值语义 + A 100%
- 101 S1-42 L104:`customerId=19621064`(8 位数字)
- 101 S1-42 L484:"cashflow.id 真实出现在 4 个页面 URL/字段: payedList / payedDetail / 销售详情 / 加工详情"

**【证据 E】**:
- 105 §8.1 L453:`customer.id 类型 | 数值 | BIGINT | A + E`
- 105 §8.2 严格禁止:"❌ 不能说原系统数据库就是 MySQL BIGINT"
- 105 §8.2:"✅ 一期数据库主键 = UUID 或 BIGINT 都可以(属于一期设计方案)"

**【证据 F】**:
- 101 S1-42 L100:**"C. 真实数据库主键/唯一键 = ❌ 不知道 | F | API endpoint 命名中未暴露 4 字段组合作为主键;无法从 endpoint 命名判断"**

**结论**:
- **customerId 字段名:A 级确认**
- **customerId 是"数值"语义**:**A 级**(105 §6.1)
- **customerId = BIGINT**:**E 级**(105 §8.1 一期设计)
- **数据库物理类型 / Java POJO 类型**:**F 级(未观察)**

### 3.3 风险

**HIGH**:DDL 写 customerId = BIGINT 是 E 级推断,不是 A 级事实。

---

## §4 Patient(patientId)

### 4.1 字段名证据(A 级)

**【证据】**:
- 101 S1-42 L98:`patientId ❌(用 MedicalRecord 实体)` — 实际 patientId **不作为业务 ID**,只通过 MedicalRecord 实体存在
- 210 S1-147 §1.3 L124:`id | item.patient.id / res.patient.id | L8250/L11668/L31116 | A`
- 105 §6.1 L375:`patient.id | Patient 主键 | 数值 | res.object.patient.id | **A 100%**`

**结论**:`patientId` 字段名 A 级确认。**但作为业务 ID 实际不用**(用 MedicalRecord)。

### 4.2 类型证据

**【证据 A】**:
- 105 §6.1 L375:`patient.id` 数值语义 A 100%
- controller.js L8423:`$scope.selectedPatientId = 10000;` ← **唯一 patientId 数字字面量**
- controller.js L8213:`$scope.obj.patientId = parseInt($stateParams.patientId)` ← URL state 字符串转 int
- 100 S1-41 L9:`payedDetail cashflowId=4460882`(虽不是 patientId 但说明 URL 数字字面量惯例)

**【证据 E】**:
- 105 §8.1 L452:`patient.id 类型 | 数值 | BIGINT | A + E`

**【证据 F】**:
- 101 S1-42 L100:**"真实数据库主键 = ❌ 不知道 | F"**

**结论**:
- **patientId 字段名:A 级确认**
- **patientId 是"数值"语义**:**A 级**(数字字面量 10000 + parseInt 模式)
- **patientId = BIGINT**:**E 级**(105 §8.1)
- **数据库物理类型 / Java POJO 类型**:**F 级**

### 4.3 风险

**MEDIUM**:有 A 级"数值"证据 + E 级 BIGINT 推断。如果实际是 Long,DDL 正确;如果是 Integer / int,也是 BIGINT 兼容。但如果是 String / UUID,DDL 错。

---

## §5 Employee(employeeId + adminId)

### 5.1 字段名证据(A 级)

**【证据】**:
- 214 §5.1:`employeeId | **45** | A` 命中
- 214 §5.1:`adminId | 34 | A` 命中
- 214 §5.4:`A. Core ID | employeeId, adminId | A`
- 214 §5.5:**"Employee 有 employeeId + adminId 独立 ID 字段(A)。adminId 与 employeeId 不完全相同"**
- 214 §11.1:`employeeId | Source A: employeeCheckinQueue.employeeId (L10652) | Source B: getEmployee*.json Response | A`
- 214 §11.1:`adminId | Source A: login response (L14273 admin.nickname) | Source B: changeAdminRole.json Request id: adminId | A`
- 214 §5.1:userId | 0 命中(C 级弱,无 userId 字段)
- 214 §5.5:**"0 命中独立 Employee Create / Update / Delete API — Employee 没有独立 CRUD"**

**结论**:`employeeId` 和 `adminId` 字段名 A 级确认。**两个独立 ID 字段**。

### 5.2 类型证据

**【证据 A】**:
- 214 §11.1 L105:`$scope.adminRoleId = [1, 2]` ← adminRoleId = 数字字面量数组
- 214 §11.1 L613-616:`adminId | login response + changeAdminRole.json | A` — adminId 派生自 response
- controller.js L1328:`employeeIdFrom: $scope.employeeIdFrom, employeeIdTo: $scope.employeeIdTo` — 都是变量

**【证据 E】**:
- 105 §8.1:未列 employeeId(只列 patient / customer / cashflow / medicalRecord)
- 105 §8.2:**"❌ 不能说原系统数据库就是 MySQL BIGINT"**

**【证据 F】**:
- controller.js 中 employeeId / adminId 数字字面量:**0** — 全部从 response 派生
- Java POJO 类型:**完全未观察**
- 数据库物理类型:**完全未观察**

**结论**:
- **employeeId 字段名:A 级确认**
- **employeeId 是"数值"语义**:**C 级**(无数字字面量 + 105 §6.1 未列入)
- **employeeId = BIGINT**:**E 级**(同 105 §8.1 一期设计原则推断)
- **数据库物理类型 / Java POJO 类型**:**F 级**
- **employeeId 与 adminId 关系**:**D 级** — 214 §5.5 说"不完全相同",具体关系未明

### 5.3 Employee 关系未观察

- **employeeId 与 adminId 关系**:可能(1)同一字段别名(2)两个独立字段(3)一对多关系(4)其他关系。**完全未观察,不得自行合并。**
- **doctorId / userId 关系**:`userId | 0 命中` = 不存在 userId 字段。`doctorId` 在 233 引入,原系统无此字段,需 S1-168 自行决定命名。

### 5.4 风险

**HIGH**:Employee 字段最复杂,无 Java 实体证据,DDL 写 BIGINT 是 E 级推断。

---

## §6 ConsultRoom(consultRoomId)

### 6.1 字段名证据(A 级)

**【证据】**:
- 214 §11.1 L622-626:`consultRoomId | Source A: consultRoom.id (L9555/L9852) | Source B: consultRoomVoList[].consultRoom.id (L9645/L9678/L9693) | Source C: getConsultRoom*.json Request | A`
- 214 §17:`consultRoom.id | L9555/L9852 | A`
- 216 S1-153 §14.1:`consultRoomVoList[]` 字段
- 216 S1-153 §14.4:`consultRoom.examineList[].examineName (sceneType=2)`
- 216 S1-153 §1.3 L101:`consultRoomScreen 5 命中 — 实际是 consultRoom.screen 内部,不是独立 Object`
- 216 S1-153 §1.3 L153:`appoint.consultRoom / appoint.room / appoint.employee / appoint.doctor 顶层 | F(0 命中)`

**结论**:`consultRoomId` 字段名 A 级确认。

### 6.2 类型证据

**【证据 A】**:
- controller.js L10141:`$scope.clinicInfo.consultRoom.status === 1` ← status 与数字 1 比较
- controller.js L9555 / L10159:`consultRoomId: $scope.clinicInfo.consultRoom.id` ← 派生自 response
- controller.js 中 consultRoom.id 数字字面量:**0**

**【证据 E】**:
- 105 §8.1:未列 consultRoomId
- 105 §8.2:**"❌ 不能说原系统数据库就是 MySQL BIGINT"**

**【证据 F】**:
- consultRoom 数字字面量:**0** — 全部从 response 派生
- Java POJO 类型:**完全未观察**
- 数据库物理类型:**完全未观察**

**结论**:
- **consultRoomId 字段名:A 级确认**
- **consultRoomId 是"数值"语义**:**C 级**(无数字字面量 + 105 §6.1 未列入)
- **consultRoomId = BIGINT**:**E 级**(同 105 §8.1 推断原则)
- **数据库物理类型 / Java POJO 类型**:**F 级**

### 6.3 风险

**HIGH**:DDL 写 BIGINT 是 E 级推断。

---

## §7 BigScreen(bigScreenId)

### 7.1 字段名证据(A 级)

**【证据】**:
- 216 S1-153 §14.1:`bigScreen | 5+ | A` / `bigScreen.id | L9600+ | **A (核心 ID)**`
- 216 S1-153 §14.4:`bigScreen.id | L9600 (item.bigScreen.id / update.bigScreen.id) | **A (核心 ID)**`
- 216 S1-153 §14.5:`**bigScreen 是独立 ID 实体**(A)`
- 214 §11.1:未单独列 bigScreenId
- 216 S1-153 §14.3:5 个 API = `selectConsultRoomVoListOfCompany.json` / `selectBigScreenConfVoListOfCompany.json` / `getBigScreenConfVo.json` / `addBigScreenAndConf.json` / `updateBigScreenAndConf.json`

**结论**:`bigScreenId` 字段名 A 级确认。

### 7.2 类型证据

**【证据 A】**:
- controller.js L9368:`manageBigScreenId: $scope.screenList.items[this.index].bigScreen.id` ← 派生自 response
- controller.js L9554:`params.bigScreenId = $scope.clinicInfo.bigScreen.id;`
- controller.js L9628:`this.bigScreenId = null;` ← 可空
- controller.js 中 bigScreen.id 数字字面量:**0**

**【证据 E】**:
- 105 §8.1:未列 bigScreenId
- 105 §8.2:**"❌ 不能说原系统数据库就是 MySQL BIGINT"**

**【证据 F】**:
- bigScreen 数字字面量:**0** — 全部从 response 派生
- Java POJO 类型:**完全未观察**
- 数据库物理类型:**完全未观察**

**结论**:
- **bigScreenId 字段名:A 级确认**
- **bigScreenId 是"数值"语义**:**C 级**(无数字字面量 + 105 §6.1 未列入)
- **bigScreenId = BIGINT**:**E 级**(同 105 §8.1 推断原则)
- **数据库物理类型 / Java POJO 类型**:**F 级**

### 7.3 风险

**HIGH**:DDL 写 BIGINT 是 E 级推断。

---

## §8 数据库 Schema / SQL 证据

### 8.1 搜索结果

| 搜索 | 命中 | 说明 |
|---|---:|---|
| `CREATE TABLE` | **0** | 全仓库无 SQL DDL |
| `ALTER TABLE` | **0** | 全仓库无 SQL DML |
| `PRIMARY KEY` / `FOREIGN KEY` | **0** | 全仓库无 SQL 约束 |
| `BIGINT` / `INT` / `VARCHAR` / `UUID` / `BINARY` | 27(全部 E 级业务推断)| 仅在 MD 一期设计章节 |
| SQL 文件(.sql)| **0** | 无 |

### 8.2 §8 关键论断(105 S1-46)

105 §8.2 明确写:
> "❌ 不能说原系统数据库就是 MySQL BIGINT"
> "❌ 不能说原系统是 Oracle(F = 当前未观察)"
> "✅ 一期数据库主键 = UUID 或 BIGINT 都可以(属于一期设计方案)"

**结论**:**本仓库无数据库 Schema / SQL 证据**(F 级)。

### 8.3 业务编号 vs 系统主键(105 §6.2 严禁混淆表)

- 业务编号(`medicalCode` 14 位字符串 / `tradeNo` 19 位字符串)= String
- 系统主键(`id`)= 数值 / BIGINT(推断)
- **严禁混淆**

但**此表内容是设计原则,不是 A 级证据**。

---

## §9 Java Entity / ORM 证据

### 9.1 搜索结果

| 搜索 | 命中 | 说明 |
|---|---:|---|
| `import java.` / `import javax.` | **0** | 无 Java 源码 |
| `@Entity` / `@Id` / `@Table` / `@Column` | **0** | 无 JPA 注解 |
| `private Long` / `private Integer` / `private String` | **0** | 无 Java 字段定义 |
| `public class` / `public static` | **0** | 无 Java 类定义 |
| `private static final` | **0** | 无 Java 常量 |
| `.java` / `.kt` / `.class` | **0** | 无 Java 编译产物 |

### 9.2 ORM / 持久化框架证据

| 搜索 | 命中 | 说明 |
|---|---:|---|
| `@MyBatis` / `@Insert` / `@Select` | **0** | 无 MyBatis 注解 |
| `Mapper` / `Repository` | **0** | 无 Mapper 文件 |
| `EntityManager` / `Session` | **0** | 无 JPA / Hibernate |
| `Mongoose` / `Schema` | **0** | 无 MongoDB |

**结论**:**本仓库无 Java Entity / ORM 证据**(F 级)。

---

## §10 API / Frontend 证据

### 10.1 API endpoint 命名(无类型信息)

| ID 字段 | API 端点 | 行号 |
|---|---|---|
| `cashflowId` | payedDetail.html `ui-sref="payedDetail({cashflowId:item.cashflow.id})"` | L116 |
| `cashflowId` | deliveryList.html | L253/L261/L268/L274 |
| `cashflowId` | machineOrderCompleted.html URL = `#!/machineOrderCompleted?cashflowId=4372377&machineCenterId=4335` | 100 S1-41 L33 |
| `cashflowId` | URL 数字字面量 4460882 / 4372377 | 100 S1-41 L9-10 |
| `patientId` | controller.js `parseInt($stateParams.patientId)` | L8213 |
| `patientId` | controller.js 数字字面量 10000 | L8423 |
| `adminId` | controller.js `changeAdminRole.json { id: adminId }` | L232/L648 |
| `adminRoleId` | controller.js 数字字面量 `[1, 2]` | L105 |
| `consultRoomId` | controller.js `params.consultRoomId = $scope.consultRoom.id` | L9555 |
| `bigScreenId` | controller.js `params.bigScreenId = $scope.clinicInfo.bigScreen.id` | L9554 |
| `companyId` | controller.js L420 `$scope.object.companyId = res.result.object.company.id` | L420 |
| `customerId` | controller.js L4395 `customerId: $scope.refundFeeInfo.customer.id` | L4395 |
| `employeeId` | controller.js L8564 `employeeId: $scope.obj.employeeId` | L8564 |

**结论**:所有 ID 字段名在 API / Frontend 端有 A 级证据。**但 API endpoint 命名约定本身不携带类型信息**。

### 10.2 JS 端类型行为

| 行为 | 证据 | 含义 |
|---|---|---|
| `parseInt()` | controller.js L8213 patientId | URL state 字符串 → int |
| 数字字面量 10000 | controller.js L8423 selectedPatientId | ID 数字字面量 |
| 数字字面量 `[1, 2]` | controller.js L105 adminRoleId | ID 数组 |
| 字符串拼接 | controller.js L1146 `localStorage.getItem($scope.corpid + "_userCert")` | corpid 行为像 number 或 string(JS 自动转换) |
| 数字字面量 4460882 | URL `#!/payedDetail?cashflowId=4460882` | 7 位数字 |

**关键洞察**:所有 ID 在 JS 端**都行为像 number(可参与数学运算 / 字符串拼接无异常)**。但这是 **JS 端行为,不是后端类型**。

---

## §11 三层类型一致性矩阵

| 实体 | 字段 | 第一层(数据库物理)| 第二层(Java POJO)| 第三层(API/前端)|
|---|---|---|---|---|
| Company | companyId | **F 未观察** | **F 未观察** | C:数字行为 + 字符串拼接 |
| Customer | customerId | **F 未观察** | **F 未观察** | **A 100% 数值**(105 §6.1)|
| Patient | patientId | **F 未观察** | **F 未观察** | **A 100% 数值**(数字字面量 10000 + parseInt + 105 §6.1)|
| Employee | employeeId | **F 未观察** | **F 未观察** | C:变量传递(无数字字面量)|
| Employee | adminId | **F 未观察** | **F 未观察** | A:数字数组 [1, 2] |
| ConsultRoom | consultRoomId | **F 未观察** | **F 未观察** | C:变量传递(无数字字面量)|
| BigScreen | bigScreenId | **F 未观察** | **F 未观察** | C:变量传递(无数字字面量)|

**结论**:
- 第三层(API/前端)有部分 A 级证据(patient / customer / cashflow / medicalRecord / medicalProduct / machineCenterOrder / machineCenterId)
- **第一层 + 第二层全部 F 未观察**
- 三层**不能建立一致性**——前端的"数值"行为不能反推后端 Java 类型

---

## §12 冲突与已识别问题

### 12.1 冲突

| 冲突 | 来源 A | 来源 B | 解决 |
|---|---|---|---|
| **现金流主键类型** | 105 §6.1 L368:"cashflow.id 数值 A 100%" | 105 §8.1 L448:"原系统事实 数值,一期设计 BIGINT" | **不冲突**——前者是"数值语义",后者是"数据库类型推断" |
| **patientId 业务存在性** | 101 §7.3:"patientId ❌ 用 MedicalRecord 实体" | 233 API-016 显式 patientId 字段 | **D 级冲突** — 233 与原系统不一致,233 自创 |
| **Employee ID 关系** | 214 §5.5:"employeeId + adminId 独立" | 233 用 employeeId 单字段 | **D 级冲突** — 233 简化 Employee 模型 |

### 12.2 233 自创模型 vs 原系统事实

| 233 模型 | 原系统事实 | 评级 |
|---|---|---|
| `employeeId` 单字段 | `employeeId` + `adminId` 双字段 | **D 冲突** |
| `patientId` 业务主键 | `patientId` 实际用 MedicalRecord 替代 | **D 冲突** |
| `consultRoomId` | `consultRoom.id` 同义 | A 一致 |
| `bigScreenId` | `bigScreen.id` 同义 | A 一致 |
| `companyId` | `companyId` 同义 | A 一致(但类型 F)|
| `customerId` | `customerId` 同义 | A 一致 |

### 12.3 关键警告

105 §8.2 写:
> ❌ "不能原系统数据库就是 MySQL BIGINT"
> ❌ "不能原系统是 Oracle(F = 当前未观察)"
> ✅ "一期数据库主键 = UUID 或 BIGINT 都可以(属于一期设计方案)"

105 §7.3 L700 写:
> "一期 1:1 复刻必须严格按 12.1-12.3 节执行:业务实体命名 + URL 参数 + 字段显示名直接采用;**25 个 F 阻断 ID 严禁脑补**;数据库主键独立设计(UUID/BIGINT)"

---

## §13 最终可信类型

### 13.1 6 个实体的最终可信类型

| 实体 | 字段 | 第一层(数据库)| 第二层(Java)| 第三层(API)| 综合判定 |
|---|---|---|---|---|---|
| Company | companyId | F | F | C(字符串拼接 + 变量)| **F 未验证** |
| Customer | customerId | F | F | **A 数值** | **C 数值语义**(类型 F)|
| Patient | patientId | F | F | **A 数值** | **C 数值语义**(类型 F)|
| Employee | employeeId | F | F | C(变量)| **F 未验证** |
| Employee | adminId | F | F | A(数字数组)| **C 数值语义**(类型 F)|
| ConsultRoom | consultRoomId | F | F | C(变量)| **F 未验证** |
| BigScreen | bigScreenId | F | F | C(变量)| **F 未验证** |

### 13.2 4 个 ID 类型已确认(105 §6.1 数值表中)

- `cashflow.id` = 数值(A 100%) — **E 级 BIGINT 推断**
- `medicalRecord.id` = 数值(A 100%) — **E 级 BIGINT 推断**
- `patient.id` = 数值(A 100%) — **E 级 BIGINT 推断**
- `customer.id` = 数值(A 100%) — **E 级 BIGINT 推断**

但这些是**前端 API 响应字段**的字符特征(A 级),**不是数据库物理类型**(F 级)。

### 13.3 自检:**234A 报告的修正**

234A 报告写:
> "6 个 ID 全部是数值类型,A 级证据 95%+"

**本 V2 审计修正**:
- 234A 的"数值"是**前端 API 响应字段的字符特征** — A 级
- 234A 的"BIGINT/Long 推断"是 **E 级**,不是 A 级
- 234A 表格里"Patient patientId = 数值 A + E"应改为 **"C 数值语义(类型 F)"**
- **234A 报告"long(BIGINT 推断)"** — 应当**改为"待 DDL 前确认"**

### 13.4 一句话结论

> **6 个 ID 字段名 A 级确认。第三层(API/前端)有"数值"语义证据(A / C 级)。第一层(数据库物理类型)+ 第二层(Java POJO 类型)全部 F 未观察,本仓库无后端 Java / SQL 证据。233 / 234A 报告的"BIGINT/Long"是 E 级推断,严禁作为 DDL 事实。**

---

## §14 S1-168 是否允许启动

### 14.1 PASS 条件(必须全部满足)

1. **第一层证据 ≥ A 级** — 数据库物理类型确认 ❌ F 级
2. **第二层证据 ≥ A 级** — Java POJO 类型确认 ❌ F 级
3. **6 个 ID 全部 F 已关闭** ❌ 4 个 F(Company / Employee / ConsultRoom / BigScreen)
4. **三层一致** ❌ 第一层 + 第二层未观察
5. **无 D 级冲突** ❌ 233 vs 原系统有 2 处冲突(Employee 双 ID / patientId 业务主键)
6. **105 §8.2 严禁脑补** ❌ 234A 已脑补 BIGINT

### 14.2 最终判断

# **【BLOCK】**

**S1-168 DDL 草案在当前证据下不允许启动。**

### 14.3 BLOCK 阻塞项清单

1. **BLOCK-1**:6 个 ID 的数据库物理类型未观察(F 级)
2. **BLOCK-2**:6 个 ID 的 Java POJO 类型(Long / Integer / int / String / UUID)未观察(F 级)
3. **BLOCK-3**:Employee 双 ID 关系(employeeId vs adminId)未观察(D 级冲突)
4. **BLOCK-4**:patientId 业务主键存在性(101 §7.3 vs 233 API-016)D 级冲突
5. **BLOCK-5**:doctorId / userId 是否存在的命名决策 — 原系统 0 命中 userId,233 自创 doctorId 命名需明确

### 14.4 解除 BLOCK 的条件

| 条件 | 来源 |
|---|---|
| 提供 6 个 ID 的 Java 实体源码 / 反编译类 | 后端 Java 项目 |
| 提供 6 个 ID 的数据库 DDL | DBA Schema dump |
| 提供 Employee / Admin 关系定义 | 后端实体 + 关系图 |
| 解决 233 vs 原系统的 2 处 D 级冲突 | 业务决策 |

**S1-167B(后端实体补充)前置 → S1-168(DDL)**。

---

## §15 报告自评

| 维度 | 分数 | 理由 |
|---|:-:|---|
| 后端 Schema 搜索 | 95/100 | 全仓库递归搜索 .java / .sql / .xml / .yml / .ts / .vue,0 命中 |
| 三层证据区分 | 90/100 | 严格区分数据库 / Java POJO / API 端 |
| 评级纪律 | 95/100 | A/B/C/D/E/F 严格应用,233 推断的 BIGINT 降级为 E |
| 拒绝脑补 | 90/100 | 在 105 §8.2 严禁的语境下严格拒绝 DDL 推断 |
| 综合 | **92/100** | |

---

## §16 一句话最终判断

> **6 个复用实体 ID 字段名 A 级确认(在 controller.js / MD 中)。第三层(API/前端)有"数值"语义证据(部分 A 级)。但本仓库不存在后端 Java 实体、SQL Schema、ORM 映射(0 命中 .java / .sql / .xml / .yml 文件)。第一层(数据库物理类型)+ 第二层(Java POJO 类型)全部 F 级未观察。234A 报告的"BIGINT/Long"推断属 E 级业务推断,严禁作为 DDL 事实。S1-168 DDL 草案在当前证据下应 BLOCK,需先 S1-167B 补充后端实体 / SQL 证据。**

---

## §17 Git

本轮**不提交 Git**(按老板指示"Git commit / Git push 严禁")。报告已写入磁盘但未 commit。

- 文件:`E:\C\minimax\OptFlow PMS\234B_S1-168_ID类型后端Schema证据核验.md`
- 字节:待 commit 前确认
- HEAD 不变:`1bf472c39812d88ad41c2e8a0570ddf37ab0e8fc`
- 7 个历史 MD 全部 SHA256 锁定
