# 平台格式化器的数字、金额、日期格式化

agent 会看到什么：读到源端用 String.format、NumberFormat / DecimalFormat、getCurrencyInstance、Formatter.formatShortFileSize、DateFormat 格式化数字、金额、文件大小和日期，常不显式传 Locale；产物里写成无参 intl.NumberFormat、toFixed、toLocaleString、手拼串或固定格式，区域、币种、舍入、进位和精度与源端不同

## 通用查法

### 源端平台格式化器没写全 Locale、币种、舍入时，查出默认后在目标显式写出

审的是：代码
触发（任一种）：
- 读到：源端用 String.format、getCurrencyInstance()、DecimalFormat 或 android.text.format.Formatter 格式化数值，没显式传 Locale、币种或舍入；写错的样子：目标写成无参 new intl.NumberFormat()、toLocaleString()、toFixed(N) 或自写函数，源端默认的区域、币种、舍入和进位没写出来
适用范围：源端用 Java / Android 平台格式化器把数值转成文本、迁成 ArkTS 时
做法：
- 在 Android SDK 的 sources 里打开这个格式化方法（如 java.lang.String#format、java.text.NumberFormat#getCurrencyInstance），读出调用处没写的几项：区域、舍入、进制和小数位
- 把读出的默认写成显式参数：new intl.NumberFormat(i18n.System.getAppPreferredLanguage(), options)，不用无参构造；intl 不推导的币种 currency、float 运算和 HALF_UP 舍入在 options 或自写函数里写明
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- String.format 用的区域是 Locale.getDefault(Locale.Category.FORMAT)：源端没传 Locale 时取默认 FORMAT 区域（出处：java.lang.String#format）
- getCurrencyInstance() 等价于 getCurrencyInstance(Locale.getDefault(Locale.Category.FORMAT))：源端币种来自默认 FORMAT 区域，代码里看不到币种（出处：java.text.NumberFormat#getCurrencyInstance）
- %f 对 float 按 Float.toString 的十进制串、用 HALF_UP 舍到精度位：String.format 的舍入规则（出处：java.util.Formatter（'f' 转换））
- constructor(locale: string | Array<string>, options?: NumberOptions)：intl.NumberFormat 按指定区域构造（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，NumberFormat.constructor）
- constructor()：使用当前系统区域创建：无参构造取系统区域，不跟应用语言（出处：js-apis-intl.md，NumberFormat 的 constructor8+）
- static getAppPreferredLanguage(): string：i18n.System 上取应用偏好语言（出处：鸿蒙 SDK 的 ets/api/@ohos.i18n.d.ts，System.getAppPreferredLanguage）
- NumberOptions.currency 须符合 ISO-4217；style 为 "currency" 时必须提供 currency，没有默认值：intl 不按区域推导币种（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，NumberOptions.currency；ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2020.bigint.d.ts，Intl.NumberFormatOptions.currency）
- new intl.NumberFormat(i18n.System.getAppPreferredLanguage())：例：应用语言为德语时，改成这个构造后显示逗号小数点，与源端默认区域一致（出处：卡里修好并验证过）
针对本应用要查的：
- 源端这处格式化实际给了哪些参数：源工程里这次格式化调用和它所在的工具函数：String.format 的格式串、NumberFormat / DecimalFormat 的构造及 setRoundingMode、setGroupingUsed 调用、Formatter 的 flags；写了的照抄；没写的按格式化器源码里读出的默认补齐，逐项写进目标的参数
- 要显示的币种：源工程的价格格式化代码、规格的验收条目或迁移基线（截图、UT 期望值）里价格的显示串；从显示串读出币种（如 $ 对应 USD），写成 ISO-4217 代码；读不出就回报缺口
未核实：DecimalFormat、DateFormat 没传 Locale 时取哪个默认区域，DecimalFormat 的默认舍入方式，族里规矩没有查实，要按源码现查
来源：3 张卡，3 个应用
- case-526d6b56241863d015dd（MifareClassicTool）：做法第 1 步 ← 建议 4
- case-6aa988142168e8fded35（Privacy Friendly 2048）：做法第 2 步 ← 建议 2；取值 8 ← 诊断
- case-a5c3358954b32d8de1a4（Jetsnack）：做法第 2 步 ← 建议 1

## 规矩

- rule-cce68d029458｜源端格式化没传 Locale 时，intl.NumberFormat 显式传应用偏好语言，不用无参构造｜读到：源端 new DecimalFormat(",##0.00")、NumberFormat 或 String.format 没有显式传 Locale；写错：目标写 new intl.NumberFormat().format(…)（注释「无参构造 = 系统Locale」）、toLocaleString()，或用 getSystemLanguage / getSystemLocale 取区域
- rule-438d75de819b｜源端 String.format 按 %.Nf 格式化 float 时，目标按 float、HALF_UP、区域小数点写｜读到：`String.format("%.2f", percentage)`，参数是 float（如 (float)a / b * 100f）；写错：目标用 number 直接算再 .toFixed(2) 输出，注释里写着 String.format("%.2f")
- rule-e78df6bfcbb7｜getCurrencyInstance 迁成 intl.NumberFormat 时须显式给 currency｜读到：源端用 NumberFormat.getCurrencyInstance().format(...)，不指定币种、按默认 locale 取；写错：new intl.NumberFormat(locale, { style: 'currency' }) 没有 currency 字段，价格输出不带货币符号
- rule-15575235b9ff｜intl 货币格式与迁移基线显示串不一致时（如 US$ 对 $），按基线可观察字符串定格式｜读到：迁移基线（截图、UT 期望值）里价格显示为 `$4.99` 这种只带 $ 的形式；写错：intl.NumberFormat(…, { style: 'currency', currency: 'USD', currencyDisplay: 'symbol' }) 在目标系统地区输出 US$ 前缀，与基线不一致
- rule-d1aa6abd8a24｜源码用 Formatter.formatShortFileSize 时，目标按千进、>900 升级和短格式小数位实现｜读到：源码调用 Formatter.formatShortFileSize(context, bytes)（或 Formatter.formatFileSize）显示文件大小；写错：目标自写的格式化函数按 1024 进位、单位写成 KB，或升级阈值写成 999.5、1000 之类不是 900 的值，小数位不按量级取
- rule-657bf0fce45e｜源端建议文件名用本地化短日期时间时，目标照源格式生成再做 FAT 合法化｜读到：源码建议文件名用 DateFormat.getDateTimeInstance(SHORT, SHORT, Locale.getDefault()) 格式化；写错：目标文件名写成固定格式（如 yyyy-MM-dd_HH-mm），或直接把含 '/'、':' 的本地化串交给 newFileNames
- rule-403a139ac543｜品类精度和基类不同时，子类 ViewModel 覆写全部高亮文本 getter，用同精度格式化｜写错：子类 ViewModel 没覆写高亮文本 getter，页面的高亮分支直接用基类 getter（内部是 `toFixed(2)` 的通用格式化），而同一字段的静态值已用 `toFixed(3)` 的格式化
- rule-c2786cac601d｜DecimalFormat 或 HALF_EVEN 舍入转文本时，目标照 ICU 语义写，不用 Math.round｜读到：源码 android.icu.text.DecimalFormat("0.#") / DecimalFormat("0.00") 的 .format(...) 生成显示文本；写错：目标写成 Math.round(v * 10) / 10 加模板串、toFixed(2)：舍入成了 HALF_UP，小数点固定为 "."
- rule-b46a44da4f78｜Kotlin Float 的 toString 或模板出文本时，目标照 Float.toString 写，整数带 .0｜读到：Kotlin 里 Float 值 .toString() 或字符串模板 "$value" 生成文本，如 (x?.value ?: 0).toString()；写错：目标写成模板串 `${value}` 或 String(value)，整数值的 Float 显示成 "30" 而不是 "30.0"
- rule-0bc607f69e94｜共享格式工具里已有函数与源码笔记的舍入语义不符时，owner 一并修正，不只补点名的函数｜读到：源码笔记或规格写「DecimalFormat "0.#"，默认 HALF_EVEN」，派工只点名共享工具里的某一个函数；写错：同一工具文件里其他格式函数仍是 Math.round / toFixed 实现，只新增或改了派工点名的那个
- rule-52d17f536b31｜迁移 DecimalFormat 时保留 HALF_EVEN 和当前 locale 符号，不用 toFixed｜读到：源端用 new DecimalFormat("#,###.#") 格式化计数缩写（如千、百万）；写错：目标写成 value.toFixed(...) 或 toLocaleString('en-US', …)：1250 出 1.3K、1200 出 1K，小数点和分组符号固定成英文
