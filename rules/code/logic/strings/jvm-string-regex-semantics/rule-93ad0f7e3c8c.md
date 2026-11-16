# 源码用 lineSequence()/lines() 分行时，目标按 \r\n、\n、\r 三种行尾分行

审的是：代码
触发（任一种）：
- 读到：Kotlin 源码对文本调用 `lineSequence()` 或 `lines()`；写错的样子：目标端写成 `split('\n')`，\r\n 的行尾留下 \r、只用 \r 分行的文本不分行
适用范围：把 Kotlin 的按行拆分翻译成 ArkTS 时
做法：
- 写成 text.split(/\r\n|\n|\r/)，正则里 \r\n 放在最前
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- split(separator: string | RegExp, limit?: number): string[]：String.split 接受正则作分隔符（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，String.split）
来源：1 张卡，1 个应用
- case-63ee0b9d164865f45abd（com.nononsenseapps.feeder）：做法第 1 步 ← 建议 2、诊断
