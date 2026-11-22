# Kotlin/Java Float 的运算与比较迁到 ArkTS 时对齐 float32：算术每步 Math.fround 后再按 Java (int) 截断，==/!= 两侧 fround 后用 ===，不自加容差；选中、存在判断与删除共用同一比较

## 何时使用

实现阶段，把 Kotlin/Java 中 Float 的算术（含随后 (int) 截断）与 ==/!= 比较（选项选中判断、列表去重、删除过滤）翻译成 ArkTS 时；规格提取阶段为 float 表达式写数值契约时

## 适用情境

源端用 value.toFloat() == state 一类写法比较 Float（如倍率、刻度选项与当前值），值来自字符串解析或滑杆；目标 number 为双精度，写者担心浮点误差，准备用 Math.abs(a - b) < ε 容差比较，或在不同位置各写一套比较。 也包括 Java 用 (float) 强转与 f 字面量计算比值、透明度、字号后再 (int) 截断，规格只写了 float→int 收窄（NaN→0、±∞ 饱和、向零截断），实现照写成 double 表达式。

## 例外与边界

- 源端本身就用容差或先舍入再比较
- 源端的值是 Double / double（Kotlin 不带 f 后缀的小数字面量、toDouble()，Java double）时不套 Math.fround：它与 number 同为 64 位，按原式计算、直接 === 比较。
- Math.fround 只用于比较和算术；值要显示成文字时仍照源端的格式化（Float.toString 给出能区分这个 float 的最短十进制串），不把 fround 后的 number 直接转字符串显示，在写入状态时就 fround 的，显示处按 Float.toString 的规则格式化。

## 原因

容差会把源端判为不同的值当成相同，选中态、是否已存在、删除哪一项随之偏离；只把 == 换成 === 也不完全等价：Kotlin Float 是 32 位，同一个十进制串解析成 double 与解析成 float 的值可能不同，两侧来源不一致时本应相等的值会被判为不等。double 中间值不按 float32 舍入，截断结果在少数输入上与源端差 1。

## 做法

1. 比较两侧都按 Float 语义归一：解析或计算得到的值用 Math.fround 转成 float32（也可在写入状态时就 fround），再用 ===；不加 ε 容差。
2. 同一组值的选中判断、存在判断与删除过滤调用同一个比较函数。
3. 源式含 (float) 或 f 字面量的算术：每个操作数与每步结果用 Math.fround 舍入到 float32（double 中间值对单精度加减乘除再舍入不产生二次舍入误差），最后按 Java (int) 截断；规格把“float 运算”和“float→int 收窄”分两行写，不写“正常值 Math.trunc 等价”；同一公式只实现一处，其余方法复用。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1、3 步〕Math.fround(x) 返回 x 最接近的单精度（float32）浮点表示，结果仍以 number 存放
- 〔做法第 3 步〕Math.trunc(x) 只去掉 x 的小数部分（向零取整），结果仍是双精度 number，不会收窄到 32 位 int 范围
- 〔适用情境 / 做法第 3 步〕Java int 的取值范围是 Integer.MIN_VALUE（-2147483648，0x80000000）到 Integer.MAX_VALUE（2147483647，0x7fffffff）
- 〔原因 / 做法第 3 步〕源端含 (float) 强转或 f 字面量的算术，用双精度 number 直接计算再截断成整数时，少数输入的结果比 Java 的 float 计算差 1
