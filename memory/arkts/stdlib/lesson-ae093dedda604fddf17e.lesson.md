# DecimalFormat、String.format、BigDecimal 舍入生成数值文本时，按源 API 复刻舍入模式与默认 Locale

ID：`lesson-ae093dedda604fddf17e` · 版本：4

[本主题](index.md)

## 何时使用

实现阶段把 DecimalFormat 模式串、String.format("%.Nf")、Float.toBigDecimal().setScale 等数值转文本函数翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些函数写映射与验收判例时；修改已有共享数值工具时

## 适用情境

源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）且未传 Locale，用 String.format("%.2f", f) 输出小数，或用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN) 舍入；应用可能单独设置应用语言；目标准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板串实现；共享数值工具与页面可能各有一份同名函数。

## 例外与边界

- 源端显式传入 Locale 或调用了 setRoundingMode：按显式设置实现

## 原因

这些 API 带隐含语义：DecimalFormat 默认 HALF_EVEN，String.format 的 %f 按 HALF_UP；两者未传 Locale 时按默认 Locale（FORMAT 类别）输出小数点与数字符号，toFixed 固定输出“.”，无参 intl.NumberFormat 取系统区域；Float.toBigDecimal 以 Float.toString 的十进制串为起点再舍入；Math.round 对半值向正无穷进位，toFixed 按双精度二进制值舍入。近似实现在多数样例上碰巧一致，只在半值、非英语语言与 float 值上偏离。默认 Locale 是否等于应用语言取决于源端切换语言的方式。

## 做法

1. 先定源端格式化实际用的 Locale：未传 Locale 时为默认 Locale 的 FORMAT 类别（Locale.getDefault(Locale.Category.FORMAT)，android-36.1 Formatter.java）。查源端切换应用语言的入口——系统应用语言设置（Android 13+ 的 per-app language，android-36.1 ConfigurationController 按应用配置调用 LocaleList.setDefault）或调用了 Locale.setDefault 时，它是应用语言，目标用 new intl.NumberFormat(i18n.System.getAppPreferredLanguage())；自实现切换只改 Activity 的 Resources 配置、没有 Locale.setDefault 时，它仍是系统区域（android-36.1 Resources/ResourcesImpl 不调用 setDefault）。不用无参构造、toLocaleString() 或固定写“.”。
2. DecimalFormat 用 HALF_EVEN（源端调用了 setRoundingMode 就照设置），最少与最多小数位与分组取自模式串（"0.#" 为 0～1 位，"0.00" 固定 2 位）。
3. String.format("%.Nf", float) 先按 float32 取值（Math.fround），再按 HALF_UP 舍入，并按同一 Locale 输出小数点与数字，不直接用 toFixed。
4. Float.toBigDecimal().setScale 从该 Float 的 Float.toString 十进制串开始按指定模式舍入（Float.toString 的规则见“Float 直接转字符串”的经验），不从双精度展开值舍入。
5. 规格为格式化函数写映射时同时写舍入模式与 Locale 来源，判例与所声明的舍入一致（HALF_EVEN 下 "0.#" 格式化 15.25 得 "15.2"），不配“四舍五入”式的例子。
6. 修改共享数值工具时对照源码与源码笔记逐个函数核对；同文件里已有实现与源语义不符的函数（笔记写 HALF_EVEN、实现却是 Math.round）一并修正或登记，不只改派工点名的那个。

## 可选检查

- "0.#" 下 15.25 → "15.2"；系统语言英语、经系统应用语言设置为德语时，"0.#" 下 12.5 → "12,5"

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-526d6b56241863d015dd](../../../store/cases/case-526d6b56241863d015dd/a7f09c67cf6e515e83af0b00787044b5d2bf8375cdc6531388a274c58f8366a6.json) · 结论：recommendation:4
  卡片版本：`a7f09c67cf6e515e83af0b00787044b5d2bf8375cdc6531388a274c58f8366a6`
- [case-6aa988142168e8fded35](../../../store/cases/case-6aa988142168e8fded35/3159baf2c12175612f43a3aca1bbed44e2a10d68446474eb6fbebab749c94f97.json) · 结论：diagnosis, recommendation:3, recommendation:1, recommendation:2
  卡片版本：`3159baf2c12175612f43a3aca1bbed44e2a10d68446474eb6fbebab749c94f97`
- [case-90117ca805576dda1534](../../../store/cases/case-90117ca805576dda1534/d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342`
