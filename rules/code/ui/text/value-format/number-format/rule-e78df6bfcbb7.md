# getCurrencyInstance 迁成 intl.NumberFormat 时须显式给 currency

审的是：代码
触发（任一种）：
- 读到：源端用 NumberFormat.getCurrencyInstance().format(...)，不指定币种、按默认 locale 取；写错的样子：new intl.NumberFormat(locale, { style: 'currency' }) 没有 currency 字段，价格输出不带货币符号
- 读到：派工或巡检单依据源端 getCurrencyInstance() 要求「以系统 locale 对应的默认币种构造格式化器」；写错的样子：删掉 currency 并在摘要里称已随系统语言和地区选择币种；或者另写 `$${…}` 一类手拼字符串和共享格式化器并存
适用范围：把安卓 NumberFormat.getCurrencyInstance() 的价格格式化改写为 ArkTS intl.NumberFormat 时
做法：
- 写成 new intl.NumberFormat(locale, { style: 'currency', currency: 'ISO-4217 代码' })；ArkTS intl 不会像 Java 那样按 locale 推导币种
- 需求要求随系统 locale 选择币种而 SDK 里查不到 region → currency 接口时，保留显式币种或写明映射表，并把无法推导的缺口回报派工者；不用省略参数表示已满足
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(locale: string | Array<string>, options?: NumberOptions)：intl.NumberFormat 的构造（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，NumberFormat.constructor）
- NumberOptions.currency?: string，须符合 ISO-4217（如 "EUR"、"CNY"、"USD"；API 12 起也可用三位数字码）：币种代码，声明里没有按 locale 的默认值（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，NumberOptions.currency）
- NumberOptions.style?: string，取值 "decimal"、"currency"、"percent"、"unit"，默认 "decimal"：数字显示格式（出处：鸿蒙 SDK 的 ets/api/@ohos.intl.d.ts，NumberOptions.style）
- currency 没有默认值；style 为 "currency" 时必须提供 currency：ES Intl 的规定，ArkTS 沿用（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es2020.bigint.d.ts，Intl.NumberFormatOptions.currency）
- getCurrencyInstance() 等价于 getCurrencyInstance(Locale.getDefault(Locale.Category.FORMAT))：源端币种来自默认 FORMAT locale，代码里看不到币种（出处：java.text.NumberFormat#getCurrencyInstance）
针对本应用要查的：
- 要显示的币种：源工程的价格格式化代码、规格的验收条目或迁移基线（截图、UT 期望值）里价格的显示串；从显示串读出币种（如 $ 对应 USD），写成 ISO-4217 代码；读不出就回报缺口
未核实：卡里没记鸿蒙 SDK 版本，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-a5c3358954b32d8de1a4（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2
