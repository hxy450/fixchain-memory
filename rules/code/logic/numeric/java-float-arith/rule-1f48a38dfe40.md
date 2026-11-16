# 源式里有 (int) 截断时，目标用 Math.trunc 原样保留，不留浮点

审的是：代码
触发（任一种）：
- 读到：Java 源式里有 `(int)` 强转或 `Math.floor` 等取整，如 `(int) ((descent() + ascent()) / 2)`；写错的样子：目标写成不取整的浮点表达式，没有 `Math.trunc(` 或对应的取整
适用范围：把安卓 Java 里带取整的数值式（坐标、偏移、尺寸）移植到 ArkTS 时
做法：
- Java 的 `(int) expr` 向零截断，写成 `Math.trunc(expr)`；源式是 floor 的写 `Math.floor(expr)`；取整放在源式里同一个位置，不因视觉验收看不出亚像素差而省掉
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- trunc(x: number): number：去掉小数部分取整数部分，即向零截断，对应 Java 的 (int) 强转（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.trunc）
- floor(x: number): number：取不大于参数的最大整数；负数时与 trunc 不同，不能拿来替 (int)（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Math.floor）
- Math.trunc((m.emHeightDescent - m.emHeightAscent) / 2)：基线偏移保留截断后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-5e1beaa11de7eb15fa6e（2048）：做法第 1 步 ← 建议 3；取值 3 ← 诊断
