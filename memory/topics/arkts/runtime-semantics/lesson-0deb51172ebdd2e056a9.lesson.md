# Kotlin/Java Float 的运算与比较迁到 ArkTS 时对齐 float32：算术每步 Math.fround 后再按 Java (int) 截断，==/!= 两侧 fround 后用 ===，不自加容差；选中、存在判断与删除共用同一比较

ID：`lesson-0deb51172ebdd2e056a9` · 版本：4 · 阶段：spec/execute · 主题：[arkts/runtime-semantics](index.md)

概要：Float 运算比较按 float32 后用 ===

信号：`Math.fround`, `toFloat()`, `Float`, `(int)`, `Math.trunc`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [集合迭代序、byte 比较与返回码按 Java](../java-stdlib/lesson-1f4747c81f16e9529787.lesson.md)（共享 1 张卡）
- [Java 读行切分格式化日历集中兼容实现](../java-stdlib/lesson-237091b9b04bc4cd340b.lesson.md)（共享 1 张卡）
- [短提示音保留混播与播放中 start 不重启语义](../../app/playback/lesson-5475edc47af05c1c6a5b.lesson.md)（共享 1 张卡）
- [单测预期按源端实现手算，不编造更严的过滤期望](../../process/check-gaming/lesson-5bc9af19bedaecaf627c.lesson.md)（共享 1 张卡）
- [形似 JS 的平台库调用按源语义逐项移植](../java-stdlib/lesson-5e3ba83ebfe5bbdf9278.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, rec-a465057588
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
- [case-e9189514e875ef00f96f](../../../../store/cases/case-e9189514e875ef00f96f/70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b.json) · 结论：rec-b746dfba92
  卡片版本：`70962a835201462f5cdf9dc9d03b341d51dc0e830922cf32d7761f935762ea1b`
- [case-ef3b0044666a7d9e867e](../../../../store/cases/case-ef3b0044666a7d9e867e/4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2.json) · 结论：rec-a96e702769, rec-94188b50a6
  卡片版本：`4aad2db1b9d7709864612c3d70b5be1c0c87bf7b7e230a9128470ccf116d75a2`
