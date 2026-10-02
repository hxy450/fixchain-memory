# 按 EditText 对齐 TextInput 时显式关闭源端没有的 ArkUI 默认装饰：Password 的显隐图标、输入时的清除按钮，并核默认高度

ID：`lesson-1150c0c721e6dc0dede4` · 版本：1

[本主题](index.md)

## 何时使用

界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时

## 适用情境

源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。

## 例外与边界

- 源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式

## 原因

ArkUI 的 Password 输入框默认显示显隐图标（showPasswordIcon 默认 true），源 XML 里不会出现对应属性，只比对源端写出的属性就会漏掉；dumpLayout 的字段 bounds 也看不出这类内部装饰，几何全对不等于外观一致。来源中对齐会话两次读到三个裸 EditText，也已注意到 TextInput 默认高度与源端不同，差异清单仍未列显隐图标；验证只核几何，截图拍了没看，用户随后报告“三个小眼睛”。同一应用的登录页、找回密码页也有同类输入框。

## 做法

1. 源端密码框没有显隐切换时，在 .type(InputType.Password) 旁写 .showPasswordIcon(false)；数字掩码的验证码框同样处理。
2. 对齐 TextInput 时，除源 XML 写出的属性外，逐项核源端没有、ArkUI 却默认带出的外观：默认高度、密码显隐图标、输入时的清除按钮（可用 cancelButton 设为 INVISIBLE）、光标样式；源端没有对应项就显式关闭或覆盖。
3. 修一处后在工程内检索 InputType.Password 等同类字段一并处理，不等用户逐页报告。

## 可选检查

- 真机验证输入框时打开截图目视对照（必要时裁剪输入框右端），不只看 dumpLayout 的 bounds。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-403ea87fd461ab4a0ad8](../../../store/cases/case-403ea87fd461ab4a0ad8/396b6254f2aabefa36741250da14adee7db9fc436d214e603f984286e8c606b2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`396b6254f2aabefa36741250da14adee7db9fc436d214e603f984286e8c606b2`
