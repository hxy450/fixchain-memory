# DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN、区域小数点、Float.toString 的十进制串与“.0”，不用 Math.round、toFixed 或模板串顶替

ID：`lesson-ae093dedda604fddf17e` · 版本：1

[本主题](index.md)

## 何时使用

实现阶段把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、Float.toBigDecimal().setScale、Float 的 toString 或字符串模板）翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些格式化函数写映射与验收判例时；修改已有共享数值工具时

## 适用情境

源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00" 等模式）生成显示文本，用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN).toFloat() 舍入，或把 Float 值直接 toString、写进字符串模板或字符串资源参数（如 (value ?: 0).toString()）；目标 number 为双精度，准备用 Math.round(v*10)/10、toFixed(n) 或模板字符串实现；共享数值工具与页面可能各有一份同名函数。

## 原因

这些源 API 带隐含语义：DecimalFormat 默认 HALF_EVEN，并按默认区域输出小数点与数字符号；Float.toBigDecimal 以 Float.toString 产生的十进制串为起点再舍入；Kotlin/Java 的 Float.toString 对整数值输出“30.0”。Math.round 对半值向正无穷进位，toFixed 按双精度二进制值舍入且固定输出“.”，JS 数字串对整数值不带“.0”；把 Float 当双精度运算还会暴露 float32 误差。近似实现在多数样例上碰巧一致，只在半值、非英语区域与整数值上偏离；注释写着 HALF_EVEN 而实现是 Math.round 时构建也不会报错。String.format("%.Nf") 是另一套规则（HALF_UP），见 Java 标准库兼容函数的经验。

## 做法

1. 按源 API 逐项实现目标函数：DecimalFormat 用 HALF_EVEN（源端调用了 setRoundingMode 就照设置），最少与最多小数位取自模式串（"0.#" 为 0～1 位，"0.00" 固定 2 位），小数点与数字符号取当前区域，不固定写“.”。
2. 源值是 Float 时先按 float32 取值（Math.fround），BigDecimal 舍入从该值的 Float.toString 十进制串开始；Float 直接转字符串（toString、字符串模板、资源参数）时按 Float.toString 输出：float32 的最短往返十进制，整数值保留“.0”，数量级在 [10^-3, 10^7) 之外为 E 记数；短写法：按 1..9 位依次 toPrecision，取首个经 Math.fround(parseFloat(s)) 往返等于原 float32 值的结果，整数值补“.0”。
3. 规格为格式化函数写映射时同时写舍入模式、区域小数点与 Float→String 规则，判例与所声明的舍入一致（HALF_EVEN 下 "0.#" 格式化 15.25 得 "15.2"），不配“四舍五入”式的例子。
4. 修改共享数值工具时对照源码与自己的源码笔记逐个函数核对；同文件里已有实现与源语义不符的函数（笔记写 HALF_EVEN、实现却是 Math.round）一并修正或登记，不只改派工点名的那个。

## 可选检查

- 最小样例："0.#" 下 15.25 → "15.2"；德语区域 "0.#" 下 12.5 → "12,5"；30f 直接转字符串 → "30.0"

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-90117ca805576dda1534](../../../store/cases/case-90117ca805576dda1534/d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342`
- [case-f6665a411a857ad38299](../../../store/cases/case-f6665a411a857ad38299/826eb1a43664d156478dc36e30b48aa6653b387802ab134799e435a288bb3754.json) · 结论：recommendation:4
  卡片版本：`826eb1a43664d156478dc36e30b48aa6653b387802ab134799e435a288bb3754`
