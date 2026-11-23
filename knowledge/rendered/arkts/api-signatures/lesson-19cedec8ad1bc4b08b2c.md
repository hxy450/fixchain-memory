# ArkTS intl.NumberFormat 用 style: 'currency' 时必须给 currency 代码，不会像 Java getCurrencyInstance 那样按 locale 推导币种

## 何时使用

实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时

## 适用情境

源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。

## 例外与边界

- 应用需要多币种或按用户地区切换币种时，不能用固定前缀代替格式化器
- 基线显示 $ 而 currencyDisplay 默认的 symbol 显示成 US$ 时，先改用 currencyDisplay: 'narrowSymbol'（文档以 USD 为例：symbol 为 -US$12,300.00，narrowSymbol 为 -$12,300.00），保留格式化器的分组和小数规则；它也拿不到基线形式时，才按第 2 步直接格式化。

## 原因

ES Intl 的声明规定 style 为 currency 时必须提供 ISO-4217 的 currency、没有默认值；@ohos.intl 的声明和文档只写 currency 须符合 ISO-4217、需配合 style 为 currency 使用，也没有按区域推导的默认值；省略后当前运行时退化为普通数字（4.99），不是本地货币串。补上 USD 后，在非美区系统语言下又可能显示 US$ 而不是基线的 $。来源中巡检修复者已读到这两处声明，也确认查不到 region→币种接口，仍删掉 currency 来表示“随 locale”，价格从此没有货币符号；返修先补 USD 得到 US$，最后按基线显示改为固定 $ 前缀加两位小数。

## 做法

1. style: 'currency' 时总是显式传 currency（ISO-4217）；需求要求随 locale 选币种而 SDK 没有推导接口时，写明 region→币种映射，或把无法推导的缺口回报给派工者，不以省略参数表示已满足。
2. 金额的最终显示形式（$4.99、US$4.99 等）以当前迁移基线或规格的可观察字符串为准，所有价格入口共用同一个格式化函数；单一币种应用在目标系统语言下拿不到基线形式时，可按基线直接格式化（来源最终采用 $ 前缀加 toFixed(2)）。

## 可选检查

- 无法运行时，用一个样例值（如 499 分）对照基线期望字符串核对格式化结果。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕安卓应用调用 NumberFormat.getCurrencyInstance() 没有传 Locale 时，等价于 getCurrencyInstance(Locale.getDefault(Locale.Category.FORMAT))，币种由当时的 FORMAT 区域决定，代码里看不到币种
- 〔原因 / 做法第 1 步〕@ohos.intl 的 NumberOptions.currency 须符合 ISO-4217（如 EUR、CNY、USD，API 12 起也支持三位数字码如 978），需配合 style 为 currency 使用，声明和文档都没有按区域推导的默认值；ES Intl 的 TypeScript 声明写明 currency 没有默认值，style 为 currency 时必须提供
- 〔做法第 1 步〕应用没有设置 NumberOptions.style 时取 decimal
- 〔做法第 2 步〕应用没有设置 NumberOptions.currencyDisplay 时取 symbol，可选 symbol、narrowSymbol、code、name
- 〔做法第 1 步〕intl.NumberFormat 的无参构造使用当前系统区域创建数字格式化对象
- 〔原因〕intl.NumberFormat 用 style 'currency' 却不给 currency 时，设备上金额显示为普通数字（如 4.99），没有货币符号
- 〔原因 / 做法第 2 步〕currency 设为 'USD'、currencyDisplay 为 'symbol' 时，在卡里当时的系统地区设置下设备上显示为 US$ 前缀，不是 $
