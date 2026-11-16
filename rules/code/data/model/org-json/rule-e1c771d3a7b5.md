# 替代 org.json 序列化时不用 JSON.stringify 直出，put(null) 删键、'/' 转义

审的是：代码
触发（任一种）：
- 读到：源码对可空字段直接 JSONObject.put(key, value)，导出用 JSONArray.toString(2)；写错的样子：目标 toJson 返回带 null 值键的对象（注释「键保留」），导出用 JSON.stringify(records, null, 2)，'/' 不转义
适用范围：把源端 org.json 序列化（备份导出、共享数据）迁成 ArkTS 时
做法：
- 封装或移植一个 org.json 等价的写工具：put 值为 null 时删键，输出字符串时把 '/' 写成 \/，缩进与 toString(n) 一致；各模型的 toJson 都走它
- 用含 null 值、数字型字符串字段和 '/' 的样例，和源端输出逐字节比对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- JSON.stringify 保留 null 值的键，也不转义 '/'；改走 org.json 等价工具（put(null) 删键、'/' 转义）后输出与源端一致：修复前后的差别（出处：卡里修好并验证过）
- put(name, null) 删除已有的 name 映射：源端 null 字段不出现在输出里（出处：org.json.JSONObject#put）
- JSONStringer 输出字符串时把 '\\' 和 '/' 前面加反斜杠：源端输出里的 '/' 是 \/（出处：org.json.JSONStringer#string）
未核实：卡里的行为在 API 24（6.1.1）上观察
来源：1 张卡，1 个应用
- case-7e6984a7fa6d5845737b（Cofi）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 1 ← 诊断
