# org.json 的读取和序列化语义

agent 会看到什么：源码用 org.json 的 JSONObject.getString / getJSONObject / put、JSONArray.toString 读写 JSON；产物里 JSON.parse 后的 as 强转、typeof 守卫和 JSON.stringify 导出

## 通用查法

### 源端用 org.json 读写 JSON 时，按它对应方法的实现写等价的读写工具

审的是：代码
触发（任一种）：
- 读到：源码用 org.json 的 JSONObject.getString / getInt / getJSONObject / getJSONArray 读字段，或 JSONObject.put、JSONArray.toString(n) 导出；写错的样子：目标 JSON.parse 后用 as string、as Record 强转或 typeof 守卫抛错，导出直接 JSON.stringify，JSON null、缺键、数字和 '/' 的处理和源端不同
适用范围：把源端 org.json 的解析和序列化迁成 ArkTS 时
做法：
- 列出源端用到的 org.json 方法，到 Android 框架源码 org.json 包里对应方法看它对 JSON null、缺键、类型不符的处理和序列化时的转义，照写成一个等价的读写工具，各解析、导出都走它
- 对照实际数据里出现 null、数字的字段，用含这些值的样例和源端结果逐字比对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getString 值存在就按需强转、缺键才抛；JSON null 解析为 JSONObject.NULL，toString 返回 "null"：例：源端读 JSON null 得到字符串 "null"（出处：org.json.JSONObject#getString；org.json.JSONTokener#readLiteral）
- put(name, null) 删除已有的 name 映射；JSONStringer 输出字符串时 '/' 前加反斜杠：例：源端导出里没有 null 值的键，'/' 写成 \/（出处：org.json.JSONObject#put；org.json.JSONStringer#string）
针对本应用要查的：
- 实际数据里哪些字段是 null、数字或缺键：目标工程 rawfile 里迁过来的 JSON，或源工程 assets / res/raw 里的同一份、备份导出的样例；按键名搜 ": null 和不带引号的数字值，列出要按源端语义强转或兜底的字段
来源：1 张卡，1 个应用
- case-7e6984a7fa6d5845737b（Cofi）：做法第 1 步 ← 建议 4、建议 1；做法第 2 步 ← 建议 5、建议 4

## 规矩

- rule-355789dc4f73｜源端用 org.json 的 getString 取字段时，目标解析器遇 JSON null 不抛错，只在缺键时失败｜读到：源码用 getString("key") 读字段，实际数据（rawfile、备份 JSON）里该字段有 "key": null 或数字；写错：目标用 `as string` 直取字段，保留真 null（显示成空行）；或写成非字符串即抛错的守卫
- rule-f6300b0c282d｜org.json 的 getJSONObject/getString 改写时补宽松解析、对象校验和 null 取值｜读到：new JSONObject(text).getJSONObject("…") / getString(...)（org.json）；写错：JSON.parse(text) 后 parsed['…'] as Record<string, string> 强转，字段不是对象也不判失败；getString 的 JSON null 取成 null 而不是 "null"
- rule-e1c771d3a7b5｜替代 org.json 序列化时不用 JSON.stringify 直出，put(null) 删键、'/' 转义｜读到：源码对可空字段直接 JSONObject.put(key, value)，导出用 JSONArray.toString(2)；写错：目标 toJson 返回带 null 值键的对象（注释「键保留」），导出用 JSON.stringify(records, null, 2)，'/' 不转义
