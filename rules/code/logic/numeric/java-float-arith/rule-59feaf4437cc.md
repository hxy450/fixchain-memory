# 源式按 Java float 运算时，目标每个操作数和每步结果包 Math.fround 再收窄

审的是：代码
触发（任一种）：
- 读到：Java 源表达式有 `(float)` 强转、`60000.0f` 这类 f 后缀字面量或 float 返回类型，结果再 `(int)` 截断；写错的样子：目标写成 double 表达式再截断，如 Math.trunc(a * (60000.0 / b))，没有 Math.fround；同一公式在几个方法里各写一遍
适用范围：把含 Java float 算术、随后 (int) 截断或比较的表达式迁成 ArkTS number 运算时
做法：
- 每个操作数和每步结果都包 Math.fround，例：(int)(255.0f * (1.0f + (float)a / (float)b)) 写成 Math.fround(255 * Math.fround(1 + Math.fround(Math.fround(a) / Math.fround(b))))，再按收窄转 int：NaN→0，≥ Integer.MAX_VALUE 或 ≤ Integer.MIN_VALUE 饱和，其余 Math.trunc
- 同一公式出现在几个方法里时只实现一处，其余调用它
- 规格只写收窄或给的是 double 样例时，仍照源端语义复刻，并在源码理解笔记里登记这处规格差异供回改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Math.fround(x: number): number：取最接近的单精度浮点值（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.fround）
- Math.trunc(x: number): number：向零截断，只用在最后的收窄（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.trunc）
- Integer.MAX_VALUE = 0x7fffffff（2147483647）、Integer.MIN_VALUE = 0x80000000（−2147483648）：收窄时饱和到的两端（出处：java.lang.Integer#MAX_VALUE、java.lang.Integer#MIN_VALUE）
- 每个操作数和每步结果加 Math.fround 后，截断结果与 Java 一致；只用 double 时少数输入差 1：逐步 fround 是上机核对过的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-ef3b0044666a7d9e867e（Blockinger）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3；取值 4 ← 诊断
