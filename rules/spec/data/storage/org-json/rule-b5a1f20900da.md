# 源端用 org.json 读写时，规格把库语义写进契约，不按字段可空写「null 键保留」

审的是：规格
触发（任一种）：
- 读到：源码 import org.json，序列化对可空字段直接 JSONObject.put(key, value)，反序列化用 getString / getInt / getJSONArray，导出用 JSONArray.toString(n)；写错的样子：规格或映射表写「null 时输出 JSON null（键保留）」「数组或 null、null 直通」「null 字段写 JSON null」，判据要求 null 字段键存在
适用范围：规格提取阶段描述基于 org.json 的序列化、反序列化契约时
做法：
- 契约里写明库语义：put(key, null) 删除键；getString 把 JSON null 转成 "null"、数字转成字符串；getInt 截断小数；getJSONArray 遇到缺键或非数组抛错；toString 把 '/' 转义成 \/
- 不由 Kotlin / Java 字段可空推出「null 值键保留」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- put(name, null) 删除已有的 name 映射：可空字段为 null 时输出里没有这个键（出处：org.json.JSONObject#put）
- getString 按需强转：JSON null 解析为 JSONObject.NULL，其 toString 返回 "null"；数字经 String.valueOf 转字符串；缺键才抛错：读出的是字符串 "null"，不是空值，也不抛错（出处：org.json.JSONObject#getString；org.json.JSON#toString；org.json.JSONTokener#readLiteral）
- getInt 对 Number 取 intValue()、对字符串 (int) Double.parseDouble：小数被截断（出处：org.json.JSONObject#getInt；org.json.JSON#toInteger）
- getJSONArray 在缺键或值不是 JSONArray（含 JSON null）时抛 JSONException：缺键或 null 不会被读成空数组（出处：org.json.JSONObject#getJSONArray）
- JSONStringer 输出字符串时把 '\\' 和 '/' 前面加反斜杠：toString 输出的 '/' 是 \/（出处：org.json.JSONStringer#string）
来源：1 张卡，1 个应用
- case-7e6984a7fa6d5845737b（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
