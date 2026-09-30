# ArkTS intl.NumberFormat 用 style: 'currency' 时必须给 currency 代码，不会像 Java getCurrencyInstance 那样按 locale 推导币种

ID：`lesson-19cedec8ad1bc4b08b2c` · 版本：1

[本主题](index.md)

## 何时使用

实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时

## 适用情境

源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。

## 例外与边界

- 应用需要多币种或按用户地区切换币种时，不能用固定前缀代替格式化器

## 原因

ES Intl 与 @ohos.intl 声明都规定 style 为 currency 时必须提供 ISO-4217 的 currency，没有默认值；省略后当前运行时退化为普通数字（4.99），不是本地货币串。补上 USD 后，在非美区系统语言下又可能显示 US$ 而不是基线的 $。来源中巡检修复者已读到这两处声明，也确认查不到 region→币种接口，仍删掉 currency 来表示“随 locale”，价格从此没有货币符号；返修先补 USD 得到 US$，最后按基线显示改为固定 $ 前缀加两位小数。

## 做法

1. style: 'currency' 时总是显式传 currency（ISO-4217）；需求要求随 locale 选币种而 SDK 没有推导接口时，写明 region→币种映射，或把无法推导的缺口回报给派工者，不以省略参数表示已满足。
2. 金额的最终显示形式（$4.99、US$4.99 等）以当前迁移基线或规格的可观察字符串为准，所有价格入口共用同一个格式化函数；单一币种应用在目标系统语言下拿不到基线形式时，可按基线直接格式化（来源最终采用 $ 前缀加 toFixed(2)）。

## 可选检查

- 无法运行时，用一个样例值（如 499 分）对照基线期望字符串核对格式化结果。

