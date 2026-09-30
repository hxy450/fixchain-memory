# 金额类输入可含小数时不用 InputType.Number：按源端解析函数选择允许小数点的输入方式

ID：`lesson-a5aeed3d4c376cd085d1` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把源端输入弹窗的 EditText 转成 ArkUI TextInput 并确定输入类型时

## 适用情境

源端 EditText 未设数字 inputType（或为 numberDecimal），保存时用 toDoubleOrNull 一类解析允许小数；目标 TextInput 准备用 InputType.Number。

## 原因

InputType.Number 按纯数字输入处理，小数点无法输入；源端能输入 66.2、22.63 的金额在目标端被截成整数。来源中写者读到 toDoubleOrNull 与无数字限制的 EditText，只参照工程里其他数字输入写法就用了 Number；先加的输入规范化没有解决，最终改为普通文本输入加 onChange 规范化后用户反馈消失。

## 做法

1. 先从源端读输入约束（inputType、maxLength）与解析函数（toDoubleOrNull/toIntOrNull）确定允许字符；可含小数时用支持小数点的类型（如 InputType.NUMBER_DECIMAL，按当前 SDK 核对可用性）或普通文本加 onChange 规范化（单个小数点、限定小数位、去多余前导零）。

## 可选检查

- 需要确认时，在真机键入 66.2、22.63 一类值确认小数点可输入。

## 来源（按需复核）

- [case-0d37e50dbb1a2e0a9bee](../../../store/cases/case-0d37e50dbb1a2e0a9bee/a72d2163734bf85155f4e46236ac3ab57df7d675bfda616e92a576af577688da.json) · 结论：diagnosis, recommendation:1
  卡片版本：`a72d2163734bf85155f4e46236ac3ab57df7d675bfda616e92a576af577688da`
