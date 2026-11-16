# Kotlin 字符串的转数和判空函数

agent 会看到什么：读过的 Kotlin 源里对字符串调用 toIntOrNull / toLongOrNull 转数、isBlank / isNotBlank 做筛选；交回的 TS 用 parseInt、正则或 trim 手写了等价

## 规矩

- rule-c4b14602e93a｜toIntOrNull/toLongOrNull 用 /^[+-]?\d+$/ 整串校验加范围检查，不用前缀解析｜读到：Kotlin 源里把外部字符串转数用 toIntOrNull() / toLongOrNull()，失败时 ?: 回落默认值、null 或某个枚举；写错：目标写成 parseInt(value, 10) / Number.parseInt 只判 NaN，带尾随字符的串按前缀被接受；或者在回落分支外加了源码没有的 `<= 0` 之类合法性规则
- rule-9964e3e89e1c｜源码用 isNotBlank/isBlank 筛选时，trim() 只用于判断，返回原串｜读到：Kotlin 源码 `firstOrNull(String::isNotBlank)`、`filter { it.isNotBlank() }` 或 `isBlank()` 只拿来筛选，返回的是原行；写错：目标端返回 `lines[i].trim()` 这类 trim 之后的串，原行首尾的空格丢了
