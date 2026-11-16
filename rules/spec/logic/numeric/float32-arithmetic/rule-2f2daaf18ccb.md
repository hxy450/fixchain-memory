# 源式按 float 运算时，验收样例按 float32 逐步算，并给一个与 double 不同的样例

审的是：规格
触发（任一种）：
- 读到：Java 源表达式有 (float) 强转、f 后缀字面量或 float 返回值，结果随后 (int) 截断或比较；写错的样子：验收样例按实数或 double 心算得出（如把 255×(1/3) 记成 85），没有一个 float 与 double 截断结果不同的样例；样例值落在整数或 .5 边界附近也没按 float32 复核
适用范围：规格提取时给含 Java float 运算的公式写验收样例和判据
做法：
- 样例按源端类型逐步舍入来算：Python 用 struct.pack('f') 或 numpy.float32，JS 用 Math.fround，每个操作数和每步结果都舍入，最后再按 (int) 收窄截断
- 至少给一个 float 与 double 截断结果不同的样例，写明两种算法各得多少
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Math.fround(x: number): number：取最接近的单精度浮点值，JS 里逐步算样例用（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2015.core.d.ts，Math.fround）
来源：1 张卡，1 个应用
- case-ef3b0044666a7d9e867e（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
