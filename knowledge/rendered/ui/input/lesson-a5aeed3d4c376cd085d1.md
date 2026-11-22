# 金额类输入可含小数时不用 InputType.Number：按源端解析函数选择允许小数点的输入方式

## 何时使用

界面实现阶段，把源端输入弹窗的 EditText 转成 ArkUI TextInput 并确定输入类型时

## 适用情境

源端 EditText 未设数字 inputType（或为 numberDecimal），保存时用 toDoubleOrNull 一类解析允许小数；目标 TextInput 准备用 InputType.Number。源端只收非负整数（inputType 为 number 且不带 numberDecimal、numberSigned，按 toIntOrNull 一类解析）时，InputType.Number 本来就对，不在这条范围。

## 原因

InputType.Number 按纯数字输入处理，小数点无法输入；源端能输入 66.2、22.63 的金额在目标端被截成整数。来源中写者读到 toDoubleOrNull 与无数字限制的 EditText，只参照工程里其他数字输入写法就用了 Number；先加的输入规范化没有解决，最终改为普通文本输入加 onChange 规范化后用户反馈消失。

## 做法

1. 先从源端读输入约束（inputType、maxLength）与解析函数（toDoubleOrNull/toIntOrNull）确定允许字符；可含小数时用支持小数点的类型（如 InputType.NUMBER_DECIMAL，API 11 起提供，只允许数字和一个小数点、不支持负数，源端允许负数时改用 inputFilter）或普通文本加 onChange 规范化（单个小数点、限定小数位、去多余前导零）。

## 可选检查

- 需要确认时，在真机键入 66.2、22.63 一类值确认小数点可输入。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕TextInput 不设 type 时为 InputType.Normal（无特殊限制）；InputType.Number 是纯数字输入模式，不支持负数、小数
- 〔原因〕TextInput 用 InputType.Number 时，即使在 onChange 里规范化输入值，小数点仍然输入不进去
- 〔做法第 1 步〕InputType.NUMBER_DECIMAL（API 11 起）是带小数点的数字输入模式：只允许数字和一个小数点，不支持负数，要负数时文档建议用 inputFilter 设允许负号的规则
