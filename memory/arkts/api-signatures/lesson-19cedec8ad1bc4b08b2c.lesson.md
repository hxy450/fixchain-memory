# 改写 getCurrencyInstance() 为 intl.NumberFormat 时显式传 currency 代码，不靠 locale 推导币种

ID：`lesson-19cedec8ad1bc4b08b2c` · 版本：2

[本主题](index.md)

## 何时使用

实现或修复阶段，把 Android NumberFormat.getCurrencyInstance() 的价格格式化改写为 @kit.LocalizationKit 的 intl.NumberFormat，并确定币种来源与显示形式时

## 适用情境

源端用不带币种参数的 NumberFormat.getCurrencyInstance() 按默认 locale 格式化金额；目标用 intl.NumberFormat(locale, { style: 'currency', ... })；任务或巡检要求“随系统 locale 选择币种”，而 SDK 声明里查不到 region→currency 的接口。

## 例外与边界

- 应用需要多币种或按用户地区切换币种时，不能用固定符号拼接代替格式化器

## 原因

Java 的 getCurrencyInstance() 按 locale 推导币种；ES Intl 规定 style 为 currency 时必须给 currency（缺省抛 TypeError），@ohos.intl.d.ts 则把 currency 声明为可选、不写缺省行为，已观察到的运行时省略后退化为不带货币符号的普通数字。同一 ISO 币种在不同系统地区下的显示形式也不同（如 $ 与 US$），只看格式化器配置定不了最终字符串。

## 做法

1. style: 'currency' 时总是显式传 currency（ISO-4217）；需求要求随 locale 选币种而 SDK 没有推导接口时，写明 region→币种映射，或把无法推导的缺口回报给派工者，不以省略参数表示已满足。
2. 金额的最终显示形式以当前迁移基线或规格的可观察字符串为准，所有价格入口共用同一个格式化函数；单一币种应用在目标系统地区下得不到基线形式时，在该函数内按基线字符串定形。

## 可选检查

- 无法运行时，用一个样例金额对照基线期望字符串核对格式化结果，样例写明币种与 locale。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-a5c3358954b32d8de1a4](../../../store/cases/case-a5c3358954b32d8de1a4/7b21adbce08b927dc204f4850fa661029b29fca5233c7b7034838e100c1e6aa0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`7b21adbce08b927dc204f4850fa661029b29fca5233c7b7034838e100c1e6aa0`
