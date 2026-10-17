# DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN，小数点与数字符号取应用偏好语言（Locale.getDefault 跟随应用语言，不是系统区域），Float.toString 的十进制串与“.0”；不用 Math.round、toFixed、无参 intl.NumberFormat 或模板串顶替

ID：`lesson-ae093dedda604fddf17e` · 版本：3 · 阶段：spec/execute · 主题：[arkts/java-stdlib](index.md)

概要：DecimalFormat 按半偶舍入与应用语言复刻

信号：`DecimalFormat`, `BigDecimal`, `setScale`, `RoundingMode.HALF_EVEN`, `Float.toString`, `Math.round`, `toFixed`, `intl.NumberFormat`, `getAppPreferredLanguage`, `Locale.getDefault`, `toPrecision`, `Math.fround`

## 何时使用

实现阶段把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、Float.toBigDecimal().setScale、Float 的 toString 或字符串模板）翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些格式化函数写映射与验收判例时；修改已有共享数值工具时

## 适用情境

源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）生成显示文本且未传 Locale，用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN).toFloat() 舍入，或把 Float 值直接 toString、写进字符串模板或字符串资源参数；应用可单独设置应用语言；目标 number 为双精度，准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板字符串实现；共享数值工具与页面可能各有一份同名函数。

## 原因

这些源 API 带隐含语义：DecimalFormat 默认 HALF_EVEN，并按 Locale.getDefault() 输出小数点与数字符号，设置了应用语言时它就是应用语言而不是系统区域；Float.toBigDecimal 以 Float.toString 产生的十进制串为起点再舍入；Kotlin/Java 的 Float.toString 对整数值输出“30.0”。Math.round 对半值向正无穷进位，toFixed 按双精度二进制值舍入且固定输出“.”，无参 intl.NumberFormat 取系统区域，JS 数字串对整数值不带“.0”；把 Float 当双精度运算还会暴露 float32 误差。近似实现在多数样例上碰巧一致，只在半值、非英语应用语言与整数值上偏离。String.format("%.Nf") 是另一套规则（HALF_UP），见 Java 标准库兼容函数的经验。

## 做法

1. 按源 API 逐项实现目标函数：DecimalFormat 用 HALF_EVEN（源端调用了 setRoundingMode 就照设置），最少与最多小数位取自模式串（"0.#" 为 0～1 位，"0.00" 固定 2 位）；小数点与数字符号按 Locale.getDefault() 语义取应用偏好语言，目标用 new intl.NumberFormat(i18n.System.getAppPreferredLanguage()) 探测，不用无参构造、toLocaleString() 或系统区域，也不固定写“.”。
2. 源值是 Float 时先按 float32 取值（Math.fround），BigDecimal 舍入从该值的 Float.toString 十进制串开始；Float 直接转字符串（toString、字符串模板、资源参数）时按 Float.toString 输出：float32 的最短往返十进制，整数值保留“.0”，数量级在 [10^-3, 10^7) 之外为 E 记数；短写法：按 1..9 位依次 toPrecision，取首个经 Math.fround(parseFloat(s)) 往返等于原 float32 值的结果，整数值补“.0”。
3. 规格为格式化函数写映射时同时写舍入模式、应用语言下的小数点与 Float→String 规则，判例与所声明的舍入一致（HALF_EVEN 下 "0.#" 格式化 15.25 得 "15.2"），不配“四舍五入”式的例子。
4. 修改共享数值工具时对照源码与自己的源码笔记逐个函数核对；同文件里已有实现与源语义不符的函数（笔记写 HALF_EVEN、实现却是 Math.round）一并修正或登记，不只改派工点名的那个。

## 可选检查

- 最小样例："0.#" 下 15.25 → "15.2"；系统语言英语、应用语言德语时 "0.#" 下 12.5 → "12,5"；30f 直接转字符串 → "30.0"

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [页内先写共享件副本时登记待收敛并回收](../../process/deferred-fulfillment/lesson-447ba5818e4e203272e8.lesson.md)（共享 2 张卡）
- [验收条目实读源码段落，照抄比较符并给边界样例](../../process/enumeration-gaps/lesson-08854573a81a9fa03746.lesson.md)（共享 1 张卡）
- [remember 按首次或 key 变才求值](../../ui/state/lifecycle/lesson-3b4a96141329db62a6af.lesson.md)（共享 1 张卡）
- [内联被调组件时按调用点实参整链代入公式](../../process/inferred-not-traced/lesson-4428ce765fcef294b004.lesson.md)（共享 1 张卡）
- [跨文件补实现的功能登记带负责方与验证的移交项](../../process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md)（共享 1 张卡）

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-6aa988142168e8fded35](../../../../store/cases/case-6aa988142168e8fded35/3159baf2c12175612f43a3aca1bbed44e2a10d68446474eb6fbebab749c94f97.json) · 结论：diagnosis, rec-d56b98c67e
  卡片版本：`3159baf2c12175612f43a3aca1bbed44e2a10d68446474eb6fbebab749c94f97`
- [case-90117ca805576dda1534](../../../../store/cases/case-90117ca805576dda1534/d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342.json) · 结论：diagnosis, rec-dcb679cd12, rec-c87ba96b15, rec-f17105847d
  卡片版本：`d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342`
- [case-f6665a411a857ad38299](../../../../store/cases/case-f6665a411a857ad38299/826eb1a43664d156478dc36e30b48aa6653b387802ab134799e435a288bb3754.json) · 结论：rec-8fe96e8198
  卡片版本：`826eb1a43664d156478dc36e30b48aa6653b387802ab134799e435a288bb3754`
