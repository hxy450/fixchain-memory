# Kotlin 的 Float.toInt() 迁成 Math.trunc，不写成 Math.round

审的是：代码
触发（任一种）：
- 读到：Kotlin 里 fontSize = state.toInt() 或标题文本里 slider 值 .toInt()；写错的样子：目标标题和落库都写成 Math.round(…)
适用范围：页面实现阶段，源码里浮点转整数的每一处
做法：
- 源码的数值转换照原语义映射：Float.toInt() → Math.trunc(x)
- 写完后在源码里搜 toInt / roundToInt，逐处核对目标表达式
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Math.trunc(x: number): number：取整数部分，去掉小数：对应 Kotlin toInt() 的向零截断（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.trunc）
- Math.round(x: number): number：四舍五入到最近整数：不是截断，小数 ≥ .5 时比 toInt() 大 1（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，Math.round）
- Float.toInt() 对应 Math.trunc：卡里返修改成 Math.trunc 后与源端一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-69c1c089176794fbe5db（jerboa）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；取值 3 ← 诊断
