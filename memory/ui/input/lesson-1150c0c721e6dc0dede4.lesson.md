# 按 EditText 对齐 TextInput 时，未声明 background 的输入框按主题状态背景（editTextBackground 的 9-patch，随聚焦切换并取其内边距）复刻，并显式关闭源端没有的 ArkUI 默认装饰：填充底与圆角、Password 显隐图标、清除按钮，核默认高度

ID：`lesson-1150c0c721e6dc0dede4` · 版本：2

[本主题](index.md)

## 何时使用

界面实现或 1:1 对齐修复阶段，把安卓 EditText（含密码框、数字掩码的验证码框）转换或核对为 ArkUI TextInput，决定要显式覆盖哪些默认外观时；为未声明 background 的 EditText 写 TextInput 外观修饰链时

## 适用情境

源输入框是裸 EditText 或其子类，用 android:password、inputType=textPassword/numberPassword 掩码，没有 TextInputLayout passwordToggleEnabled 或自绘显隐按钮，也没有清除按钮；目标用 TextInput，type 为 InputType.Password 或 Normal。 也包括源 EditText 未声明 background、padding 与高度，外观来自框架主题的 editTextBackground 状态选择器（Holo 为 textfield_default/activated_holo_dark 两张 9-patch，含端头竖线与内容内边距）。

## 例外与边界

- 源端确有可见性切换（passwordToggleEnabled 或自绘眼睛按钮）或清除按钮，此时保留并按源端对齐样式

## 原因

ArkUI 的 Password 输入框默认显示显隐图标（showPasswordIcon 默认 true），源 XML 里不会出现对应属性，只比对源端写出的属性就会漏掉；dumpLayout 的字段 bounds 也看不出这类内部装饰，几何全对不等于外观一致。来源中对齐会话两次读到三个裸 EditText，也已注意到 TextInput 默认高度与源端不同，差异清单仍未列显隐图标；验证只核几何，截图拍了没看，用户随后报告“三个小眼睛”。同一应用的登录页、找回密码页也有同类输入框。TextInput 自带填充底、圆角、内边距与默认高度；只设透明底加 bottom 边框时默认圆角让两端上翘，也没有聚焦态。另一应用的经验摘要写“TextInput 显式覆盖默认填充底为透明+下划线”，写者据此用静态下边框和猜测色近似了状态背景。

## 做法

1. 源 EditText 未声明 background 时外观是主题的状态背景：从本机 SDK 平台资源取 editTextBackground 选择器各状态的 9-patch，随 onFocus/onBlur 切换，padding 取 9-patch 内容区，高度按 wrap_content 结果（内边距 + 文字行高）设置，光标色按 textCursorDrawable；不用 border bottom 加猜测色近似。TextInput 改透明底时同时显式 borderRadius(0)。
2. 源端密码框没有显隐切换时，在 .type(InputType.Password) 旁写 .showPasswordIcon(false)；数字掩码的验证码框同样处理。
3. 对齐 TextInput 时，除源 XML 写出的属性外，逐项核源端没有、ArkUI 却默认带出的外观：默认填充底、圆角与内边距、默认高度、密码显隐图标、输入时的清除按钮（可用 cancelButton 设为 INVISIBLE）、光标样式；源端没有对应项就显式关闭或覆盖。
4. 修一处后在工程内检索 InputType.Password 等同类字段一并处理，不等用户逐页报告。

## 可选检查

- 真机验证输入框时打开截图目视对照（必要时裁剪输入框右端），不只看 dumpLayout 的 bounds。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0ce95f901f7e409784a3](../../../store/cases/case-0ce95f901f7e409784a3/4aa26550cce3a384a4aa9ffe3848cf1c7c967010523cbc09787d6c214d2c67df.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`4aa26550cce3a384a4aa9ffe3848cf1c7c967010523cbc09787d6c214d2c67df`
- [case-403ea87fd461ab4a0ad8](../../../store/cases/case-403ea87fd461ab4a0ad8/396b6254f2aabefa36741250da14adee7db9fc436d214e603f984286e8c606b2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`396b6254f2aabefa36741250da14adee7db9fc436d214e603f984286e8c606b2`
