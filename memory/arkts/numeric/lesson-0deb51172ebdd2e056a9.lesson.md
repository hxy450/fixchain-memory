# Kotlin/Java Float 的运算与比较迁到 ArkTS 时对齐 float32：算术每步 Math.fround 后再按 Java (int) 截断，==/!= 两侧 fround 后用 ===，不自加容差；选中、存在判断与删除共用同一比较

ID：`lesson-0deb51172ebdd2e056a9` · 版本：3

[本主题](index.md)

## 何时使用

实现阶段，把 Kotlin/Java 中 Float 的算术（含随后 (int) 截断）与 ==/!= 比较（选项选中判断、列表去重、删除过滤）翻译成 ArkTS 时；规格提取阶段为 float 表达式写数值契约时

## 适用情境

源端用 value.toFloat() == state 一类写法比较 Float（如倍率、刻度选项与当前值），值来自字符串解析或滑杆；目标 number 为双精度，写者担心浮点误差，准备用 Math.abs(a - b) < ε 容差比较，或在不同位置各写一套比较。 也包括 Java 用 (float) 强转与 f 字面量计算比值、透明度、字号后再 (int) 截断，规格只写了 float→int 收窄（NaN→0、±∞ 饱和、向零截断），实现照写成 double 表达式。

## 例外与边界

- 源端本身就用容差或先舍入再比较

## 原因

容差会把源端判为不同的值当成相同，选中态、是否已存在、删除哪一项随之偏离；只把 == 换成 === 也不完全等价：Kotlin Float 是 32 位，同一个十进制串解析成 double 与解析成 float 的值可能不同，两侧来源不一致时本应相等的值会被判为不等。double 中间值不按 float32 舍入，截断结果在少数输入上与源端差 1。

## 做法

1. 比较两侧都按 Float 语义归一：解析或计算得到的值用 Math.fround 转成 float32（也可在写入状态时就 fround），再用 ===；不加 ε 容差。
2. 同一组值的选中判断、存在判断与删除过滤调用同一个比较函数。
3. 源式含 (float) 或 f 字面量的算术：每个操作数与每步结果用 Math.fround 舍入到 float32（double 中间值对单精度加减乘除再舍入不产生二次舍入误差），最后按 Java (int) 截断；规格把“float 运算”和“float→int 收窄”分两行写，不写“正常值 Math.trunc 等价”；同一公式只实现一处，其余方法复用。

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:3
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
- [case-e9189514e875ef00f96f](../../../store/cases/case-e9189514e875ef00f96f/70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b.json) · 结论：recommendation:1
  卡片版本：`70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b`
- [case-ef3b0044666a7d9e867e](../../../store/cases/case-ef3b0044666a7d9e867e/4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2.json) · 结论：recommendation:1, recommendation:3
  卡片版本：`4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2`
