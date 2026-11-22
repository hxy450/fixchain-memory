# DecimalFormat、BigDecimal 舍入与 Float 转字符串按源 API 语义复刻：HALF_EVEN，小数点与数字符号取应用偏好语言（Locale.getDefault 跟随应用语言，不是系统区域），Float.toString 的十进制串与“.0”；不用 Math.round、toFixed、无参 intl.NumberFormat 或模板串顶替

## 何时使用

实现阶段把 Kotlin/Android 的数值转文本函数（DecimalFormat 模式串、Float.toBigDecimal().setScale、Float 的 toString 或字符串模板）翻译成 ArkTS 共享工具或页面内函数时；规格提取阶段为这些格式化函数写映射与验收判例时；修改已有共享数值工具时

## 适用情境

源端用 android.icu.text.DecimalFormat 或 java.text.DecimalFormat（"0.#"、"0.00"、",##0.00" 等模式）生成显示文本且未传 Locale，用 Float.toBigDecimal().setScale(n, RoundingMode.HALF_EVEN).toFloat() 舍入，或把 Float 值直接 toString、写进字符串模板或字符串资源参数；应用可单独设置应用语言；目标 number 为双精度，准备用 Math.round(v*10)/10、toFixed(n)、无参 intl.NumberFormat 或模板字符串实现；共享数值工具与页面可能各有一份同名函数。

## 原因

这些源 API 带隐含语义：DecimalFormat 默认 HALF_EVEN，并按 Locale.getDefault() 输出小数点与数字符号，设置了应用语言时它就是应用语言而不是系统区域；Float.toBigDecimal 以 Float.toString 产生的十进制串为起点再舍入；Kotlin/Java 的 Float.toString 对整数值输出“30.0”。Math.round 对半值向正无穷进位，toFixed 按双精度二进制值舍入且固定输出“.”，无参 intl.NumberFormat 取系统区域，JS 数字串对整数值不带“.0”；把 Float 当双精度运算还会暴露 float32 误差。近似实现在多数样例上碰巧一致，只在半值、非英语应用语言与整数值上偏离。String.format("%.Nf") 是另一套规则（HALF_UP），见 Java 标准库兼容函数的经验。

## 做法

1. 按源 API 逐项实现目标函数：DecimalFormat 用 HALF_EVEN，舍入作用在待格式化 double 的 Double.toString 十进制写法上、不按二进制真值（源值是 Float 时先 Math.fround 再取 String(v) 的十进制串做 HALF_EVEN；如 double 0.15 按 "0.#" 得 "0.2"）（源端调用了 setRoundingMode 就照设置），最少与最多小数位取自模式串（"0.#" 为 0～1 位，"0.00" 固定 2 位）；小数点与数字符号按 Locale.getDefault() 语义取应用偏好语言，目标用 new intl.NumberFormat(i18n.System.getAppPreferredLanguage()) 探测，不用无参构造、toLocaleString() 或系统区域，也不固定写“.”。
2. 源值是 Float 时先按 float32 取值（Math.fround），BigDecimal 舍入从该值的 Float.toString 十进制串开始；Float 直接转字符串（toString、字符串模板、资源参数）时按 Float.toString 输出：float32 的最短往返十进制（这是 Android 15 QPR2 起的系统构建和 API 36 上的 FloatToDecimal 实现；更早的系统构建用 FloatingDecimal，规范是小数部分至少一位、之后只取足以与相邻 float 区分的位数，与前者不是同一套规则），整数值保留“.0”，数量级在 [10^-3, 10^7) 之外为 E 记数；短写法：按 1..9 位依次 toPrecision，取首个经 Math.fround(parseFloat(s)) 往返等于原 float32 值的结果（1 位就往返时再取 2 位的 toPrecision，两者都往返的取更接近原值的，一样近取尾数为偶的），整数值补“.0”。
3. 规格为格式化函数写映射时同时写舍入模式、应用语言下的小数点与 Float→String 规则，判例与所声明的舍入一致（HALF_EVEN 下 "0.#" 格式化 15.25 得 "15.2"），不配“四舍五入”式的例子。
4. 修改共享数值工具时对照源码与自己的源码笔记逐个函数核对；同文件里已有实现与源语义不符的函数（笔记写 HALF_EVEN、实现却是 Math.round）一并修正或登记，不只改派工点名的那个。

## 可选检查

- 最小样例："0.#" 下 15.25 → "15.2"；系统语言英语、应用语言德语时 "0.#" 下 12.5 → "12,5"；30f 直接转字符串 → "30.0"

来源支持：4 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1；AOSP libcore android-11.0.0_r1、android-13.0.0_r1、android-14.0.0_r1、android-15.0.0_r1、android-16.0.0_r1（java.lang.Float）；kotlin-stdlib 2.1.0（源码包）；AOSP libcore android-15.0.0_r1 至 r20 逐标签（java.lang.Float）；AOSP build android-15.0.0_r17、r20（build_id.mk）；AOSP external/icu android-8.1.0_r1、9.0.0_r1、11.0.0_r1、14.0.0_r1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕java.text.DecimalFormat 在没有调用 setRoundingMode 时用 RoundingMode.HALF_EVEN；new DecimalFormat(String pattern) 用 Locale.getDefault(Locale.Category.FORMAT) 的数字符号（小数点、分组符）；安卓上 java.text.DecimalFormat 内部委托 android.icu.text.DecimalFormat 做格式化
- 〔原因 / 做法第 1 步〕android.icu.text.DecimalFormat 在没有调用 setRoundingMode 时用 HALF_EVEN（中点取偶）；new DecimalFormat(String pattern) 用默认 FORMAT 区域的 DecimalFormatSymbols（小数点、分组符随区域，德语区域小数点为逗号）
- 〔原因 / 做法第 1 步〕安卓 ICU 数字格式化（android.icu 的这套实现在 AOSP android-9.0.0_r1、11、14 标签与 android-36.1 源码里相同；8.1 的 ICU 里没有这个类，更早的行为未核）给 double 舍入时先按快速近似值算，舍入位落在中点附近的不确定区时改用 Double.toString(n) 的十进制串重算再舍入，所以结果按这个 double 的 Double.toString 写法定、不按它的二进制真值：double 0.15 按 "0.#" 取 "0.15"，是中点，HALF_EVEN 得 "0.2"。Double.toString 的规范是小数部分至少一位、之后只取足以与相邻 double 区分的位数（android-36.1 仍由 FloatingDecimal.toJavaFormatString 实现）
- 〔原因 / 做法第 1 步〕应用没有自己调 Locale.setDefault 时，安卓进程的默认 Locale 由框架按应用资源配置的首选语言设置：绑定应用时 ActivityThread 调 LocaleList.setDefault(config.getLocales())，之后 ConfigurationController.updateLocaleListFromAppContext 把应用 Context 资源配置里的首选 Locale 设为默认；LocaleList.setDefault 内部调 Locale.setDefault(Locale)，DISPLAY、FORMAT 两个类别一起设。配置变化时（改系统语言或应用语言等）ConfigurationController.handleConfigurationChanged 和 ViewRootImpl 的配置回调会再调 updateLocaleListFromAppContext，应用先前自己用 Locale.setDefault 设的值随之被覆盖
- 〔原因 / 做法第 1 步〕安卓设置应用语言为德语、系统语言为英语时，不传 Locale 的 DecimalFormat(",##0.00") 输出逗号小数点（0,00）；鸿蒙在应用偏好语言德语、系统语言英语时，无参构造的 intl.NumberFormat 输出点号（0.00）
- 〔做法第 1 步〕intl（从 @kit.LocalizationKit 导入）的 NumberFormat：constructor()（首段 @since 8）用当前系统区域创建；constructor(locale: string | Array<string>, options?: NumberOptions)（首段 @since 6）按给定区域创建，数组取第一个有效的区域；format(num: number): string。NumberOptions 在应用没有另设时 minimumFractionDigits 为 0、maximumFractionDigits 为 3、useGrouping 为 true；roundingMode?: string（@since 18）可取 ceil、floor、expand、trunc、halfCeil、halfFloor、halfExpand、halfTrunc、halfEven，没有另设时为 halfExpand（中点远离零进位）
- 〔做法第 1 步〕i18n（从 @kit.LocalizationKit 导入）的 static System.getAppPreferredLanguage(): string（首段 @since 9）返回应用偏好语言；System.getSystemLocale() 自 API 20 起废弃，表示的是系统区域
- 〔原因 / 做法第 2 步〕java.lang.Float.toString(float) 有两种实现。FloatToDecimal：在按 IEEE 754 就近舍入能回到原值的十进制里取最短的（最短长度为 1 时在 1 到 2 位里选），再取其中最接近原值的那个（并列取偶数尾数）；数量级在 [10^-3, 10^7) 内用定点写法，没有小数部分时补「.0」（123×10^2 写成 12300.0），之外用科学计数（1.0E23、1.23E-19）。FloatingDecimal.toJavaFormatString：规范写的是小数部分至少一位、之后只取足以与相邻 float 区分的位数，定点与科学计数的分界同为 10^-3 和 10^7。AOSP libcore 的 android-15.0.0_r17（构建号 AP4A.250205）及更早标签是 FloatingDecimal，android-15.0.0_r20（Android 15 QPR2，构建号 BP1A.250305，API 级别仍是 35）起、android-16.0.0_r1 和 android-36.1 源码是 FloatToDecimal：API 36 的设备是后者，API 35 的设备随系统构建两种都有
- 〔原因 / 做法第 2 步〕Kotlin 的 Float.toBigDecimal() 是 BigDecimal(this.toString())（@SinceKotlin 1.2，@InlineOnly：内联进调用方，运行时用的是设备上 java.lang.Float 的 toString，实现随设备的系统版本变），即从 Float.toString 产生的十进制串构造 BigDecimal，Double.toBigDecimal() 同样从 Double.toString 的串构造
- 〔做法第 2 步〕安卓上 Kotlin 的 Float 值 30f 直接转字符串（toString、字符串模板、字符串资源参数）显示 30.0；鸿蒙 ArkTS 模板串对同一数值显示 30
- 〔做法第 2 步〕Math.fround(x: number): number 返回与参数最接近的单精度浮点值（声明在 SDK 自带的 TypeScript lib.es2015.core.d.ts）；number 的 toPrecision(precision?: number): string 声明在 lib.es5.d.ts
