# DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN，小数点与数字符号取应用偏好语言（Locale.getDefault 跟随应用语言，不是系统区域），Float.toString 的十进制串与“.0”；不用 Math.round、toFixed、无参 intl.NumberFormat 或模板串顶替

## 何时使用

实现阶段把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、Float.toBigDecimal().setScale、Float 的 toString 或字符串模板）翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些格式化函数写映射与验收判例时；修改已有共享数值工具时

## 适用情境

源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）生成显示文本且未传 Locale，用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN).toFloat() 舍入，或把 Float 值直接 toString、写进字符串模板或字符串资源参数；应用可单独设置应用语言；目标 number 为双精度，准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板字符串实现；共享数值工具与页面可能各有一份同名函数。源端构造时传了 Locale 或 DecimalFormatSymbols 的（如 new DecimalFormat(pattern, DecimalFormatSymbols(Locale.US))、NumberFormat.getInstance(Locale.ROOT)），符号按传入的 Locale 取，目标写死对应符号（如“.”）是对的，不改成应用偏好语言；按应用偏好语言取只针对没传 Locale 的调用。

## 原因

这些源 API 带隐含语义：DecimalFormat 默认 HALF_EVEN，并按 Locale.getDefault() 输出小数点与数字符号，设置了应用语言时它就是应用语言而不是系统区域；Float.toBigDecimal 以 Float.toString 产生的十进制串为起点再舍入；Kotlin/Java 的 Float.toString 对整数值输出“30.0”。Math.round 对半值向正无穷进位，toFixed 按双精度二进制值舍入且固定输出“.”，无参 intl.NumberFormat 取系统区域，JS 数字串对整数值不带“.0”；把 Float 当双精度运算还会暴露 float32 误差。近似实现在多数样例上碰巧一致，只在半值、非英语应用语言与整数值上偏离。String.format("%.Nf") 是另一套规则（HALF_UP），见 Java 标准库兼容函数的经验。

## 做法

1. 按源 API 逐项实现目标函数：DecimalFormat 用 HALF_EVEN（源端调用了 setRoundingMode 就照设置），最少与最多小数位取自模式串（"0.#" 为 0～1 位，"0.00" 固定 2 位）；小数点与数字符号按 Locale.getDefault() 语义取应用偏好语言，目标用 new intl.NumberFormat(i18n.System.getAppPreferredLanguage()) 探测，不用无参构造、toLocaleString() 或系统区域，也不固定写“.”。
2. 源值是 Float 时先按 float32 取值（Math.fround），BigDecimal 舍入从该值的 Float.toString 十进制串开始；Float 直接转字符串（toString、字符串模板、资源参数）时按 Float.toString 输出：float32 的最短往返十进制，整数值保留“.0”，数量级在 [10^-3, 10^7) 之外为 E 记数；短写法：按 1..9 位依次 toPrecision，取首个经 Math.fround(parseFloat(s)) 往返等于原 float32 值的结果；首个是 1 位时再看 2 位的 toPrecision，它也往返且比 1 位的更接近原值时取 2 位；整数值补“.0”。
3. 规格为格式化函数写映射时同时写舍入模式、应用语言下的小数点与 Float→String 规则，判例与所声明的舍入一致（HALF_EVEN 下 "0.#" 格式化 15.25 得 "15.2"），不配“四舍五入”式的例子。
4. 修改共享数值工具时对照源码与自己的源码笔记逐个函数核对；同文件里已有实现与源语义不符的函数（笔记写 HALF_EVEN、实现却是 Math.round）一并修正或登记，不只改派工点名的那个。

## 可选检查

- 最小样例："0.#" 下 15.25 → "15.2"；系统语言英语、应用语言德语时 "0.#" 下 12.5 → "12,5"；30f 直接转字符串 → "30.0"

来源支持：4 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；org.jetbrains.kotlin:kotlin-stdlib 2.3.20（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕java.text.DecimalFormat 和 android.icu.text.DecimalFormat 在应用没有另调 setRoundingMode 时都按 HALF_EVEN（中点取偶）舍入
- 〔原因 / 做法第 1 步〕DecimalFormat(String pattern) 没传 Locale 时，小数点、分组符等符号取 Locale.getDefault(Locale.Category.FORMAT)；ICU 版取 ULocale.getDefault(Category.FORMAT)
- 〔原因〕应用没有另设 Locale.setDefault 时，进程的默认 Locale 由框架设成应用 Context 资源配置里的首个 locale：ConfigurationController.updateLocaleListFromAppContext 调 LocaleList.setDefault，后者调 Locale.setDefault，同时设置 DISPLAY 和 FORMAT 两类默认值
- 〔原因 / 做法第 1 步〕系统语言英语、应用语言设为德语时：安卓上未传 Locale 的 DecimalFormat(",##0.00") 输出 0,00；鸿蒙（HarmonyOS 6.1.0，API 23）上无参 new intl.NumberFormat() 格式化同一数值输出 0.00
- 〔原因 / 做法第 1 步〕intl.NumberFormat 的无参构造和 NumberOptions.locale 不写时都用系统当前区域；应用偏好语言决定优先加载哪种语言的资源，文档要求开发者自己把国际化特性的区域设为偏好语言
- 〔做法第 1 步〕NumberOptions 不写时 roundingMode 为 halfExpand（中点远离零），可选 halfEven（API 18 起）；minimumFractionDigits 为 0、maximumFractionDigits 为 3，useGrouping 为 true
- 〔做法第 2 步〕Kotlin 的 Float.toBigDecimal() 等于 BigDecimal(String.valueOf(f))，String.valueOf(float) 又等于 Float.toString(f)：BigDecimal 从 Float.toString 产生的十进制串构造
- 〔做法第 2 步〕android-36.1 的 Float.toString 选能按 IEEE 754 就近舍入后等于原值的十进制数，几乎总是最短的那个（最短长度为 1 位时在 1、2 位里取最接近原值的，等距时取有效数字为偶数的）；格式：十进制指数 e 在 [-3, 0) 写成 0.0…，在 [0, 7) 写定点且至少一位小数（123×10^2 写成 12300.0），其余用科学计数（1.0E23、1.23E-19）；零写成 0.0 或 -0.0；更早版本的安卓源码没有核
