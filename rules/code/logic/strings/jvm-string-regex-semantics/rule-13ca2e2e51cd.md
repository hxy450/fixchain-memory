# contains/endsWith/startsWith 没传 ignoreCase 时，目标保持大小写敏感

审的是：代码
触发（任一种）：
- 读到：Kotlin 源码里 `contains("…")`、`endsWith(".ext")`、`startsWith("…")` 没有传 `ignoreCase = true`，前面也没有 `lowercase()`；写错的样子：目标端写成 `s.toLowerCase().indexOf('…') >= 0`、`name.toLowerCase().endsWith('.ext')`，自行加了大小写归一
适用范围：把 Kotlin 源码里的字符串匹配、筛选表达式翻译成 ArkTS 判定时
做法：
- 按源 API 的默认语义写大小写敏感的判定：contains("x") → s.includes('x')，endsWith(".ext") → name.endsWith('.ext')，startsWith("x") → s.startsWith('x')，不加 toLowerCase()
- 只有源码本身调用了 lowercase() 或传了 ignoreCase = true 时，目标端才做大小写归一
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- includes(searchString: string, position?: number): boolean：String.includes，按原样逐字比较子串（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，String.includes）
- endsWith(searchString: string, endPosition?: number): boolean：String.endsWith，按原样逐元素比较结尾（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，String.endsWith）
- startsWith(searchString: string, position?: number): boolean：String.startsWith，按原样逐元素比较开头（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，String.startsWith）
来源：1 张卡，1 个应用
- case-63ee0b9d164865f45abd（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
