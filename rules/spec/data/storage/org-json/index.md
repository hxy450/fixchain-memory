# 源码用 org.json 读写 JSON

agent 会看到什么：源码 import org.json，用 new JSONObject(...)、getString / getInt / getJSONObject / getJSONArray、put、toString 解析或导出，或在循环里边解析边 insert，规格写成 JSON.parse 纯语言构造、「null 键保留」或「解析先于写库」

## 通用查法

### 源端用 org.json 读写时，规格按 org.json 源码逐个方法查缺键、null 和类型处理，写进契约

审的是：规格
触发（任一种）：
- 读到：源码 import org.json，用 new JSONObject(...)、getString / getInt / getJSONObject / getJSONArray、put、toString 读写 JSON；写错的样子：规格或映射表写「JSON.parse + 显式 class」「纯语言构造」「null 字段写 JSON null（键保留）」，没写源库对缺键、JSON null、类型不符和数字的处理，AC 也没覆盖
适用范围：规格提取阶段描述基于 org.json 的解析、序列化契约和对应 AC 时
做法：
- 列出源码实际用到的每个 org.json 方法，逐个在 Android 框架的 org.json 源码里读它对缺键、JSON null、类型不符和小数的处理
- 契约照源库写：缺键抛错还是取默认、JSON null 读成什么、数字是否截断、put(key, null) 是否删键、输出怎么转义；不从字段可空或 JSON.parse 的行为去推
- 宽松语法、类型校验失败、null 取值各写一条失败或取值 AC
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- put(name, null) 删除已有的 name 映射：例：可空字段为 null 时输出里没有这个键（出处：org.json.JSONObject#put）
- getString 遇 JSON null 得到 JSONObject.NULL 的 toString，即字符串 "null"：例：读出的是字符串 "null"，不是空值，也不抛错（出处：org.json.JSONObject#getString；org.json.JSONObject#NULL）
- JSONTokener 是宽松解析，解析成功不代表输入是合法 JSON：例：源端能解析、JSON.parse 会拒绝的输入（出处：org.json.JSONTokener（类注释））
针对本应用要查的：
- 源码用到的每个 org.json 方法的实际语义：Android SDK 源码包里 org/json/ 下的 JSONObject.java、JSONArray.java、JSON.java、JSONTokener.java（按应用的 compileSdk 取对应版本），按方法名找；读方法体和 @throws：缺键是抛 JSONException 还是返回默认值，值经 JSON.toString、JSON.toInteger 等怎么转换，遇 JSONObject.NULL 怎么处理
未核实：族里规矩只查过 put、getString、getInt、getJSONObject、getJSONArray、JSONTokener 和 JSONStringer，其他方法要按查法现查
来源：2 张卡，2 个应用
- case-7e6984a7fa6d5845737b（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
- case-ce5d3e2da2846b40767d（MifareClassicTool）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2

## 规矩

- rule-faa148429442｜源端用 org.json 解析时，规格逐项写宽松语法、取值类型校验和 null 转换并各写 AC｜读到：源码 new JSONObject(...) 后 getJSONObject("…") / getString(...)（org.json）；写错：映射写「org.json.JSONObject → JSON.parse + 显式 class」并标「纯语言构造」；AC 只列非法 JSON、缺字段、空对象，没有宽松语法、getJSONObject 的类型校验和 getString 对 null 的取值
- rule-b5a1f20900da｜源端用 org.json 读写时，规格把库语义写进契约，不按字段可空写「null 键保留」｜读到：源码 import org.json，序列化对可空字段直接 JSONObject.put(key, value)，反序列化用 getString / getInt / getJSONArray，导出用 JSONArray.toString(n)；写错：规格或映射表写「null 时输出 JSON null（键保留）」「数组或 null、null 直通」「null 字段写 JSON null」，判据要求 null 字段键存在
- rule-48b04e994993｜规格写导入、恢复流程时按源循环里解析和写库的先后写中止语义｜读到：源码恢复流程在 for 循环里逐条 getJSONObject → 解析 → insert → getJSONArray(子项) → insertAll；写错：规格写「解析先于任何 DB 写入，不产生部分导入」或称「源端解析在循环外先行」
