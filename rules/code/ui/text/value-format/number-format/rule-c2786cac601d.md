# DecimalFormat 或 HALF_EVEN 舍入转文本时，目标照 ICU 语义写，不用 Math.round

审的是：代码
触发（任一种）：
- 读到：源码 android.icu.text.DecimalFormat("0.#") / DecimalFormat("0.00") 的 .format(...) 生成显示文本；写错的样子：目标写成 Math.round(v * 10) / 10 加模板串、toFixed(2)：舍入成了 HALF_UP，小数点固定为 "."
- 读到：源码 Float.toBigDecimal().setScale(scale, HALF_EVEN).toFloat()；写错的样子：目标按 double 直接 Math.round(v * 10) / 10，没有 float32 取值和 HALF_EVEN
适用范围：把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、BigDecimal 舍入）翻译成 ArkTS 共享工具或页面内函数时
做法：
- DecimalFormat 模式串照 ICU 语义实现：按模式的小数位数做 HALF_EVEN 舍入（"0.#" 至多 1 位且去尾零，"0.00" 固定 2 位），小数点和数字符号用默认区域的
- Float.toBigDecimal().setScale(n, HALF_EVEN) 先用 Math.fround(v) 取 float32 值，在它的 Float.toString 十进制串上做 HALF_EVEN 舍入
- 自检用例："0.#" 下 15.25→"15.2"，德语区域 12.5→"12,5"
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DecimalFormat 默认舍入模式是 HALF_EVEN（中点取偶）：Math.round 是中点进位，结果不同（出处：android.icu.text.DecimalFormat#setRoundingMode）
- new DecimalFormat(pattern) 用默认区域的符号：小数点随区域变化，德语区域是逗号（出处：android.icu.text.DecimalFormat#DecimalFormat(String)）
- Math.fround(x: number): number 返回最接近的单精度浮点值：模拟 Kotlin Float 的 float32 取值（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.fround）
- 共享数值工具整体重写为 float32 语义、HALF_EVEN、区域小数点、Float.toString 模拟，roundToDecimals 按 BigDecimal 方式实现；页面删掉页内函数统一调用：修好后的做法（出处：卡里修好并验证过）
未核实：Float.toBigDecimal 以 Float.toString 的十进制串为基础出自卡，Kotlin 标准库源码本机没有
来源：1 张卡，1 个应用
- case-90117ca805576dda1534（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 4 ← 诊断
