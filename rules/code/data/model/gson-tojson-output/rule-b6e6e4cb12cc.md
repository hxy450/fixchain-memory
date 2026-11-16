# 源端用 Gson 反射写备份 JSON 时，toJson 按 Gson 的键序、布尔写法和 null 省略写出

审的是：代码
触发（任一种）：
- 读到：源端备份或互通 JSON 走 `Gson` 反射序列化（`new Gson().toJson(obj)`），规格或参考里的 JSON 示例标着 `[推断]`；写错的样子：手写的 `toJson` 照抄推断示例：Boolean 字段写成 0/1 数值、null 值写出键、键序不按字段声明顺序，或用 `JSON.stringify` 加全局 `replace` 凑 htmlSafe 转义
适用范围：源端用 Gson 反射序列化、目标端手写 toJson/fromJson 互通同一份 JSON 时
做法：
- 先核对真实序列化器再写：键按字段声明顺序，Boolean 写 true/false，null 值省略键，字符串按 Gson 的 htmlSafe 规则转义
- 需要特殊字符转义时逐字符写出（等价于 Gson 的写出器），不用 JSON.stringify 后全局 replace
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Gson 反射：字段名序、Boolean 为 true/false、null 省略、htmlSafe 转义：手写 toJson 要对齐的四项（出处：卡里修好并验证过）
针对本应用要查的：
- Gson 的版本和 JsonWriter 的转义表：源工程 Gradle 构建脚本里 com.google.code.gson:gson 的版本；Gradle 缓存里对应版本的 jar；对 com.google.gson.stream.JsonWriter 跑 `javap -c -p`，读 htmlSafe 时替换的字符表
来源：1 张卡，1 个应用
- case-5e7f81b1b1ef0753d249（omni-notes-hmos）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 建议 6、诊断；取值 1 ← 建议 6、诊断
