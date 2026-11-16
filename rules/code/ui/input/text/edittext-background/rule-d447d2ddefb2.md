# 对齐 EditText 时逐项核 TextInput 默认带出的外观，源端没有的显式关闭或覆盖

审的是：代码
触发（任一种）：
- 读到：源 EditText 没写清除按钮、显隐图标，用 android:background="@null" 等去掉了默认装饰，高度按内容或 padding 决定；写错的样子：TextInput 只覆盖了源 XML 写出的属性，没有处理 ArkUI 默认带出的外观：没写 .height()、.showPasswordIcon(false)、.cancelButton(...)、.caretStyle(...)
适用范围：界面实现或 1:1 对齐修复阶段，把 EditText 转换或核对为 ArkUI TextInput 时
做法：
- 每个 TextInput 至少逐项过一遍：默认高度、密码显隐图标、输入时的清除按钮、光标样式；源端没有对应项的，显式写 .height(<源端高度>)、.showPasswordIcon(false)、.cancelButton({ style: CancelButtonStyle.INVISIBLE })、.caretStyle({ width: <源端值>, color: <源端值> }) 关闭或覆盖
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- cancelButton(options: CancelButtonOptions): TextInputAttribute，参数默认 { style: CancelButtonStyle.INPUT }：清除按钮的样式（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.cancelButton）
- CancelButtonStyle：CONSTANT、INVISIBLE、INPUT：INVISIBLE 是不显示清除按钮（出处：鸿蒙 SDK 的 ets/component/search.d.ts，CancelButtonStyle）
- caretStyle(value: CaretStyle): TextInputAttribute：光标宽度和颜色（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretStyle）
- showPasswordIcon(value: boolean): TextInputAttribute，默认 true：密码模式末尾的显隐图标（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.showPasswordIcon）
针对本应用要查的：
- 源端输入框的实际高度和光标外观：源工程布局 XML 里这个 EditText 的 android:layout_height、padding、textSize，以及 android:textCursorDrawable 或它引用的 style；能读出 dp 值的直接写成 vp；高度是 wrap_content 时按 padding 加行高推算，写进 .height()
未核实：TextInput 不调 cancelButton 时是否显示清除按钮、不设高度时的默认高度，卡里没有核实
来源：1 张卡，1 个应用
- case-403ea87fd461ab4a0ad8（企业安全培训）：做法第 1 步 ← 建议 2
