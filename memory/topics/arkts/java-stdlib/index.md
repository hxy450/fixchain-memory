# arkts/java-stdlib

Java/Kotlin 标准库调用（集合序、字符串、正则、格式化、日历）与形似 JS API 的语义差异复刻

[上一级](../index.md)

## 本级经验

- [DecimalFormat 按半偶舍入与应用语言复刻](lesson-ae093dedda604fddf17e.lesson.md) · 阶段：spec/execute · 信号：DecimalFormat, BigDecimal, setScale, RoundingMode.HALF_EVEN
- [Java 读行切分格式化日历集中兼容实现](lesson-237091b9b04bc4cd340b.lesson.md) · 阶段：spec/execute · 信号：BufferedReader.readLine, String.split, String.format, SimpleDateFormat
- [位置参数插入用 split/join，不把参数当替换串](lesson-ecbaa1723e2beb9b1aec.lesson.md) · 阶段：execute · 信号：getString, String.format, %1$s, String.replace
- [形似 JS 的平台库调用按源语义逐项移植](lesson-5e3ba83ebfe5bbdf9278.lesson.md) · 阶段：spec/execute · 信号：Pattern, replaceAll, compareToIgnoreCase, List.remove
- [集合迭代序、byte 比较与返回码按 Java](lesson-1f4747c81f16e9529787.lesson.md) · 阶段：spec/execute · 信号：HashSet, HashMap, keySet, toArray
