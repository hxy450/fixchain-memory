# 源式有 (float) 强转或 f 字面量再截断时，规格映射把 float 运算和收窄分两行

审的是：规格
触发（任一种）：
- 读到：Java 源表达式出现 (float) 强转、60000.0f 这类 f 后缀字面量或 float 字段、返回值，结果随后 (int) 截断或参与比较；写错的样子：规格的实现映射只写「(int) float→int 收窄 → Math.trunc + 显式饱和」或「正常值 Math.trunc 等价」，公式去掉了 f，没写每步按 float32 舍入
适用范围：规格提取时，把含 Java float 运算的算术表达式翻译成目标数值契约的那几行映射
做法：
- 实现映射分两行：「float 运算」一行写明每个操作数和每步 + − × ÷ 的结果都用 Math.fround 舍入到 float32；「float→int 收窄」一行再写 NaN→0、±∞ 饱和、向零截断；不写「正常值 Math.trunc 等价」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Math.fround(x: number): number：取最接近的单精度浮点值，用来逐步复刻 float32 舍入（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.fround）
- Math.trunc(x: number): number：去掉小数部分，即向零截断，只用于收窄那一步（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.trunc）
- Integer.MAX_VALUE = 0x7fffffff（2147483647）、Integer.MIN_VALUE = 0x80000000（−2147483648）：±∞ 和超范围值饱和到的两端（出处：java.lang.Integer#MAX_VALUE、java.lang.Integer#MIN_VALUE）
来源：1 张卡，1 个应用
- case-ef3b0044666a7d9e867e（Blockinger）：做法第 1 步 ← 建议 1
