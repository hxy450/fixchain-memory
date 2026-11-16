# Kotlin Float 的 toString 或模板出文本时，目标照 Float.toString 写，整数带 .0

审的是：代码
触发（任一种）：
- 读到：Kotlin 里 Float 值 .toString() 或字符串模板 "$value" 生成文本，如 (x?.value ?: 0).toString()；写错的样子：目标写成模板串 `${value}` 或 String(value)，整数值的 Float 显示成 "30" 而不是 "30.0"
适用范围：把 Kotlin Float 转字符串（toString、字符串模板、toBigDecimal 的基础串）翻译成 ArkTS 时
做法：
- 调用一个按 Kotlin Float.toString 规则写的转换函数：先 Math.fround(v) 取 float32 值，取能唯一还原它的最短十进制串；整数值补 .0（30f→"30.0"），指数 < -3 或 ≥ 7 时用 1.0E7 这类科学计数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 选出的十进制数是按 IEEE 754 就近舍入能还原原值的最短那个：float32 值要按单精度取最短串，不能直接用 JS number 的 toString（出处：java.lang.Float#toString(float)）
- 0 ≤ e < 7 且没有小数部分时格式成 12300.0；e < -3 或 e ≥ 7 时用科学计数，如 1.0E23：整数值带 .0，大数和很小的数是科学计数（出处：java.lang.Float#toString(float)）
- Math.fround(x: number): number 返回最接近的单精度浮点值：先取 float32 值再转串（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.fround）
- 编辑卡的初始值改用共享工具里模拟 Float.toString 的函数：修好后 30 显示为 30.0（出处：卡里修好并验证过）
未核实：Kotlin Float.toString 在 JVM/Android 上等同 java.lang.Float.toString，本机只有 Android 框架源码可核
来源：1 张卡，1 个应用
- case-90117ca805576dda1534（Cofi）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
