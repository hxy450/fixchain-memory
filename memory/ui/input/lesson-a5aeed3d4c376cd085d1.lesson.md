# 数值输入框按源 inputType 与提交时的解析函数选键盘：可负用带符号键盘、可含小数用 NUMBER_DECIMAL

ID：`lesson-a5aeed3d4c376cd085d1` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把源端 EditText（含输入弹窗）的数值输入转成 ArkUI TextInput 并确定 type 与 inputFilter 时

## 适用情境

源端 EditText 为 number、numberSigned、numberDecimal 等数值 inputType，或未设数字 inputType 而保存时用 toDoubleOrNull/toFloat 一类允许小数的函数解析；目标 TextInput 准备一律用 InputType.Number。

## 例外与边界

- inputType 是 textCapCharacters 等 text 类标志：只映射键盘与输入法属性，不加内容过滤

## 原因

InputType.Number 是纯数字输入（text_input.d.ts），小数点与负号都无法输入，源端可输入小数或负值的字段在目标被截成非负整数。源端的接受集合由 number 类 inputType 装的 DigitsKeyListener（signed 允许首位单个符号，decimal 允许小数点）、android:digits、InputFilter 与提交时的解析函数共同决定。设了 inputFilter 后，type 自带的过滤不再生效（text_input.d.ts，API 11 起）。

## 做法

1. 先从源端读接受集合：inputType、android:digits、InputFilter、maxLength 与提交时的解析函数（toIntOrNull/toDoubleOrNull）。
2. 按接受集合选键盘与过滤：只收非负整数 → InputType.Number，需要时加 [0-9] 过滤；可含小数 → InputType.NUMBER_DECIMAL（API 11 起，数字与一个小数点）；可负 → 带 +/- 的键盘（如 InputType.PhoneNumber）加 [0-9+-] 过滤，“只允许首位单个符号”另写在过滤函数或 onWillChange 中（inputFilter 的正则只匹配单个字符，text_input.d.ts）；可负且可含小数时用 InputType.Normal 加过滤。设了 inputFilter 时把允许的字符集完整写进它。
3. 只迁移源端已有的输入期过滤与转换，不因字段是金额等业务含义新增限定小数位、去前导零等规范化；提交时的校验仍放在提交时。

## 可选检查

- 需要确认时，在真机键入带小数点或负号的值（如 66.2、-3）确认可输入，并核对提交时的解析结果。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0852bbd20dbe34883a83](../../../store/cases/case-0852bbd20dbe34883a83/d9d1a92626f1ac8aeda57c3c243bd9f3782939e0e413ec022bb118521c0c3ccc.json) · 结论：recommendation:3, recommendation:1
  卡片版本：`d9d1a92626f1ac8aeda57c3c243bd9f3782939e0e413ec022bb118521c0c3ccc`
- [case-0d37e50dbb1a2e0a9bee](../../../store/cases/case-0d37e50dbb1a2e0a9bee/a72d2163734bf85155f4e46236ac3ab57df7d675bfda616e92a576af577688da.json) · 结论：diagnosis, recommendation:1
  卡片版本：`a72d2163734bf85155f4e46236ac3ab57df7d675bfda616e92a576af577688da`
