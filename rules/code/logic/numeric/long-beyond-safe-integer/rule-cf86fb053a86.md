# 源码把 Long.MAX_VALUE 这类 long 常量拼进 SQL 时，目标用字符串字面量拼

审的是：代码
触发（任一种）：
- 读到：Java 源码用字符串拼接把 Long.MAX_VALUE（或别的超出 2^53 的 long 常量）拼进 SQL，例如 CASE … ELSE " + Long.MAX_VALUE + " END 作哨兵；写错的样子：目标声明成 number 常量 9223372036854775807 再拼进 SQL 字符串，实际拼出的是 9223372036854776000
适用范围：安卓的 long 常量迁到 ArkTS 后参与 SQL 或字符串拼接，且绝对值超出 Number.MAX_SAFE_INTEGER 时
做法：
- 先判断常量的绝对值是否大于 Number.MAX_SAFE_INTEGER（9007199254740991）；Long.MAX_VALUE 是 2^63-1，超出
- 超出时声明字符串常量，例如 static readonly LONG_MAX_VALUE_SQL: string = '9223372036854775807'，直接拼进 SQL，中间不经过 number
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Long.MAX_VALUE = 0x7fffffffffffffffL（2^63-1 = 9223372036854775807）：源端拼进 SQL 的精确整数（出处：java.lang.Long#MAX_VALUE）
- Number.MAX_SAFE_INTEGER = 9007199254740991（2^53 − 1）：ArkTS number 能精确表示的最大整数（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，NumberConstructor.MAX_SAFE_INTEGER）
- number 常量 9223372036854775807 拼进字符串得 9223372036854776000，超出 int64，SQLite 存成 REAL，回读为 0：用 number 时哨兵失效的样子（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-bdbb705b26462605b1c3（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
