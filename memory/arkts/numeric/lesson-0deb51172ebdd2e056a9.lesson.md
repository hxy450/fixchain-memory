# 源端 Float 参与运算或 == 比较时按 float32 复刻：按数值提升定类型，float 步骤 Math.fround，比较不加容差

ID：`lesson-0deb51172ebdd2e056a9` · 版本：4

[本主题](index.md)

## 何时使用

实现阶段把 Kotlin/Java 中含 Float 的算术（含随后 (int) 截断）与 ==/!= 比较（选中判断、是否已存在、删除过滤）翻译成 ArkTS 时；规格提取阶段为这类表达式写数值契约与验收样例时

## 适用情境

源端变量为 Kotlin Float/Java float（f 后缀字面量、(float) 强转、toFloat()、float 字段或返回值），值来自字符串解析、滑杆或计算，随后 (int) 截断或用 == 比较；目标 number 为双精度，写者准备用 Math.abs(a - b) < ε 容差比较、在不同位置各写一套比较，或照写成 double 表达式；规格可能只写了 float→int 收窄（NaN→0、±∞ 饱和、向零截断）。

## 例外与边界

- 源端本身就用容差或先舍入再比较

## 原因

Kotlin/Java 的 float 是 32 位：同一十进制串解析成 float 与解析成 double 的值可能不同，float 运算每步结果都舍入到 float32；目标 number 全程双精度，两侧来源不一致时本应相等的值会被判为不等，截断结果在少数输入上差 1。容差又会把源端判为不同的值当成相同，选中态、是否已存在、删除哪一项随之偏离。表达式里出现 float 不代表每步都是 float：按 Java/Kotlin 数值提升，含 double 操作数的步骤按 double 计算（Kotlin Float.times(Double) 返回 Double），整型子式按整型计算。

## 做法

1. 先按 Java/Kotlin 数值提升给每个子表达式定类型：两侧都是 float（或 float 与整型）的运算、(float) 强转与赋给 float 变量处，把结果用 Math.fround 舍入到 float32；含 double 操作数（不带 f 的小数字面量、Double 变量）的步骤按 double 计算，不 fround；整型子式按整型计算（整数除法截断，如 (float)(7/2) 为 3.0）。
2. 最后的 (int)/toInt() 收窄按 Java 语义：NaN→0，超出 int 范围饱和到 Integer.MIN_VALUE/MAX_VALUE，其余向零截断（Math.trunc，量可能为负时不换成 Math.floor）；规格把“float 运算”与“float→int 收窄”分两行写，不写“正常值 Math.trunc 等价”，验收样例按 float32 逐步计算（Math.fround 或 numpy.float32），至少给一个 float 与 double 截断结果不同的样例；同一公式只实现一处，其余调用复用。
3. == / != 比较：两侧按 Float 语义归一（解析或计算结果用 Math.fround，也可在写入状态时就 fround）后用 ===，不加 ε 容差；同一组值的选中判断、存在判断与删除过滤调用同一个比较函数。
4. 比较发生在集合 contains/indexOf/distinct 或泛型 equals 中时按 Float.equals 语义：按 floatToIntBits 比较，NaN 等于 NaN，0.0f 与 -0.0f 不等（android-36.1 Float.java equals 说明）；目标对 fround 后的值用 Object.is 判等。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:3
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
- [case-ef3b0044666a7d9e867e](../../../store/cases/case-ef3b0044666a7d9e867e/4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2.json) · 结论：recommendation:1, recommendation:3, diagnosis, recommendation:2
  卡片版本：`4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2`
