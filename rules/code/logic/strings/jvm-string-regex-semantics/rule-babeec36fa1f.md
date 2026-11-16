# Kotlin replaceFirst(…, true) 只换首个且忽略大小写，replace 换全部

审的是：代码
触发（任一种）：
- 读到：Kotlin 源码 url.startsWith("http://", true) 后 replaceFirst("http", "https", true)，或 String.replace("www.", "") 一类替换；写错的样子：目标写成 'h' + url.substring(1) 这类结果等于原串的拼接，或用 String.replace('www.', '') 只替换了第一个
适用范围：把 Kotlin 的 String 替换函数移植成 ArkTS 时
做法：
- replaceFirst(old, new, ignoreCase = true) 只换第一个、不分大小写的匹配；前缀已用 startsWith(…, true) 判定时写 'https' + url.substring(4)
- Kotlin String.replace(old, new) 是全部替换，目标写 replaceAll(old, new)
- 写完用源端样例自测，例如 'http://example.com' 应得 'https://example.com'
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- replace(searchValue: string | RegExp, replaceValue: string)：searchValue 是字符串（或不带 g 的正则）时只替换第一个匹配：Kotlin replace 的全部替换不能用它（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，String.replace）
- replaceAll(searchValue: string | RegExp, replaceValue: string): string：替换全部匹配（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2021.string.d.ts，String.replaceAll）
- 修好后写成 'https' + url.substring(4)：前缀判定后只换首个 http（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4b8ebe5007982e666e18（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 3 ← 诊断
