# DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN，小数点与数字符号取应用偏好语言（Locale.getDefault 跟随应用语言，不是系统区域），Float.toString 的十进制串与“.0”；不用 Math.round、toFixed、无参 intl.NumberFormat 或模板串顶替

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

来源支持：4 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；ICU4J 75.1（样例运行）；kotlin-stdlib 1.3.72、2.4.20（字节码）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕安卓的 java.text.DecimalFormat 把格式化整体交给 android.icu.text.DecimalFormat；ICU 格式化 double 时，舍入位落在居中附近就改用 Double.toString 的最短十进制串判断再进位，即按“写出来的十进制”舍入：HALF_EVEN 下 "0.0" 格式化 0.15 得 "0.2"，"0.00" 格式化 2.675 得 "2.68"，"0.#" 格式化 15.35 得 "15.4"、15.25 得 "15.2"，也可能反向："0.0" 格式化 0.45 得 "0.4"。ArkTS 的 toFixed 按 double 的二进制精确值取最近、恰好居中时取绝对值大的一侧：0.15.toFixed(1) 为 "0.1"，2.675.toFixed(2) 为 "2.67"，15.35.toFixed(1) 为 "15.3"，15.25.toFixed(1) 为 "15.3"，0.45.toFixed(1) 为 "0.5"。〔成立范围：对象：安卓 java.text.DecimalFormat 与 android.icu.text.DecimalFormat 的 format(double)；ArkTS 的 Number.prototype.toFixed。条件：安卓一侧依据 android-36.1 源码（format(double) 委托 icuDecimalFormat；DecimalQuantity_AbstractBCD 的 roundToMagnitude 在居中区调用 convertToAccurateDouble），并用 ICU4J 75.1 跑样例得到上述结果，更早的 Android 版本未逐版核对；toFixed 依据 ECMAScript 规范的算法逐步算出，并对照 arkcompiler_ets_runtime 仓 master 的 NumberHelper::DoubleToFixedString（经 FixedDtoa 按二进制值取舍、余数不小于一半就进位），未在设备上跑。不成立：桌面 JDK 的 java.text.DecimalFormat 不走 ICU（按二进制值舍入，0.15 在 "0.0" 下得 "0.1"），不在本条范围。〕
- 〔做法第 1 步〕@ohos.intl 的 NumberFormat 无参构造用当前系统区域（不是应用偏好语言）；NumberOptions.roundingMode 传 "halfEven" 时与安卓 DecimalFormat 默认的 HALF_EVEN 对应。〔成立范围：对象：intl.NumberFormat 的构造与 format。条件：无参取系统区域依据是文档说明，并对照 OpenHarmony global_i18n 仓 master（NAPI 路径的 NumberFormat 构造在没给区域时取 LocaleConfig::GetEffectiveLocale，读系统区域参数）；roundingMode 选项从 API 18 起才有。未传 roundingMode 时的舍入不在本条范围：声明注释写默认 "halfExpand"，开源实现却只在传了 roundingMode 时才设置、未传时沿用 ICU 数字格式化器默认的 HALF_EVEN，两份依据不一致（已记 device_todo）。不成立：构造时传了 locale（如 i18n.System.getAppPreferredLanguage() 的返回值）时按所传区域取符号。〕
- 〔做法第 2 步〕Kotlin 的 Float.toBigDecimal() 编译后就是 BigDecimal(String.valueOf(f))，起点是 Float.toString 的十进制串（2.675f → "2.675"，setScale(2, HALF_EVEN) 得 2.68）；而把 Float 交给 DecimalFormat.format 时先拓宽成 double，起点是这个 double 的最短串（2.675f 拓宽为 2.674999952316284，"0.00" 下得 "2.67"）。〔成立范围：对象：源端 Float 值经 toBigDecimal().setScale 与经 DecimalFormat 格式化两条路径。条件：toBigDecimal 依据 kotlin-stdlib 1.3.72 与 2.4.20 的字节码（javap），DecimalFormat 一侧依据 ICU4J 75.1 样例。不成立：源端用 BigDecimal(float) 构造（不是 toBigDecimal）时，起点是二进制精确值 2.6749999523162841796875。〕
- 〔原因〕安卓 DecimalFormat（java.text 与 android.icu 两套）没调 setRoundingMode 时舍入模式为 HALF_EVEN；只传模式串构造时，小数点与分组符号取 Locale.getDefault(Locale.Category.FORMAT) 的 DecimalFormatSymbols。〔成立范围：对象：new DecimalFormat(pattern) 构造、未传 DecimalFormatSymbols 或 Locale 的实例。条件：依据 android-36.1 源码。不成立：源端调了 setRoundingMode，或构造时传了指定 Locale 的 DecimalFormatSymbols，按其设置。〕
- 〔适用情境〕安卓进程的默认 Locale 由下发给应用的语言列表设定（handleBindApplication 里 LocaleList.setDefault(config.getLocales())），ConfigurationController 再把它调成应用资源实际选中的那个语言（updateLocaleListFromAppContext 取应用 Context 资源配置的首个语言）；Locale.setDefault 同时设 FORMAT 类别并同步 ICU 默认值；Android 13 起经 LocaleManager 设的应用语言以“应用语言在前、系统语言在后”的并集下发给应用，所以设了应用语言时 Locale.getDefault(FORMAT) 是应用语言。〔成立范围：对象：安卓应用进程内的 Locale.getDefault()。条件：依据 android-36.1 源码与 LocaleManager#setApplicationLocales 的注释，适用于 Android 13+ 的系统级应用语言。不成立：没设应用语言时默认 Locale 不一定是系统首选语言——列表首位语言应用没有对应资源、后面有应用支持的语言（英语总当作支持）时，ResourcesImpl 会把后者排到首位、默认 Locale 随之是它；Android 12 及以下由应用或库自己改 Activity 配置实现的应用内语言，默认 Locale 是否跟着变取决于实现，本条不覆盖。〕
- 〔做法第 2 步〕Float.toString 输出能唯一区分该 float 的最短十进制：数量级 e 满足 -3 ≤ e < 7（即 [10^-3, 10^7)）时写普通小数，整数值带“.0”（30f → "30.0"）；之外用科学记数（1e7f → "1.0E7"，0.0009f → "9.0E-4"）。〔成立范围：对象：java.lang.Float#toString 与 Kotlin 的 Float.toString()。条件：依据 android-36.1 源码的 javadoc（实现为 FloatToDecimal），样例输出用 JDK 21 核对；更早 Android 版本的实现未逐版核对。不成立：Double 走 Double.toString，位数按 double 计。〕
