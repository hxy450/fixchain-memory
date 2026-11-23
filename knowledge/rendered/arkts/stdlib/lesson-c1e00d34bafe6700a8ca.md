# Kotlin 严格解析（toIntOrNull、ZonedDateTime.parse、类型化解码）不改写成 parseInt、Date.parse 或 as

## 何时使用

数据层与服务层实现阶段，把外部字符串或 JSON 转成数值、时间或类型化对象的 Kotlin 解析调用改写为 ArkTS 时

## 适用情境

源码用 toIntOrNull/toLongOrNull、ZonedDateTime.parse、Json.decodeFromString 等严格解析，失败时回落默认值、null 或保留旧值；目标侧可选 parseInt、Number、Date.parse 与 as 类型断言，它们接受的输入更宽或不做运行时检查。

## 例外与边界

- toLongOrNull 对应的值可能超过 9007199254740991（2^53 − 1）时（如 64 位 id），整串校验后不要直接 Number()：number 已不能精确表示，范围检查和保存改用 BigInt 或保留原字符串；只有值域确定落在安全整数内（如 Int 范围、分钟数）才用 Number()。

## 原因

只照抄了失败时的回落分支，接受范围却被放宽：parseInt 只解析前缀（'15abc' 得 15），Date.parse 接受 '2024-01-02' 这类纯日期，as 不在运行期检查类型；源函数会拒绝的输入在目标被当成有效值，命中错误分支或覆盖旧值。自加源码没有的合法性规则（如把 0 当非法）同样改变结果。

## 做法

1. 改写前写出源函数接受与拒绝的输入：toIntOrNull/toLongOrNull 要求整串为十进制整数（可带正负号）且在 Int/Long 范围内；ZonedDateTime.parse 要求含 T 与时分，并且必须带偏移（Z 或 ±HH:MM），偏移之后可再跟 [Zone]；只有 [Zone] 没有偏移的串会被拒；kotlinx 解码在字段类型不符时抛错。
2. 整数串先用 ^[+-]?\d+$ 整串校验再 Number() 并检查范围；时间串先按 ISO_ZONED_DATE_TIME 格式校验再转 epoch 毫秒；手写 fromJson 对每个字段 typeof 检查，不符即抛给外层回退。只保留源码已有的回落分支。

## 可选检查

- 对每个解析点用一个源函数会拒绝的反例（如 '15abc'、'2024-01-02'、数字类型的字符串字段）和一个边界合法值（如 '0'）核对结果与源函数一致

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；org.jetbrains.kotlin:kotlin-stdlib 2.2.21。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕ZonedDateTime.parse(text) 按 DateTimeFormatter.ISO_ZONED_DATE_TIME 解析，解析不了抛 DateTimeParseException
- 〔做法第 1、2 步〕ISO_ZONED_DATE_TIME 是 ISO_OFFSET_DATE_TIME 加可选的 [区域 ID]；ISO_OFFSET_DATE_TIME 是日期 + 'T' + HH:mm[:ss[.小数]] 再加必需的偏移；用 STRICT 解析
- 〔做法第 1、2 步〕Kotlin String.toIntOrNull：首字符可为 '+' 或 '-'（只有一个符号字符时返回 null），其他非数字字符返回 null，超出 Int 范围返回 null
- 〔做法第 1、2 步〕Int 的范围是 -2147483648..2147483647（0x80000000..0x7fffffff）
- 〔做法第 2 步〕Number.MAX_SAFE_INTEGER 为 9007199254740991（2^53 − 1），超过它的整数在 number 里不能保证精确表示
