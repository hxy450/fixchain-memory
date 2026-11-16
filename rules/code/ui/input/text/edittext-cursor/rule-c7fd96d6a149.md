# textCursorDrawable 引用 shape 时，caretColor 用其 solid 颜色

审的是：代码
触发（任一种）：
- 读到：EditText 上写了 android:textCursorDrawable="@drawable/…"，引用的是 <shape>，颜色在 <solid android:color>；写错的样子：对应 TextInput 的 .caretColor(...) 是从仓内别的页面照抄的颜色，没有打开 shape 文件核对
适用范围：安卓 EditText 用 textCursorDrawable 引用 shape 自定义光标，迁成 ArkUI TextInput 时的光标色
做法：
- 打开 textCursorDrawable 引用的 shape XML，读 <solid android:color="…"> 的颜色（是 @color/… 时再解析到色值）
- 写成 TextInput(...).caretColor('<该颜色>')，只加在源里写了 textCursorDrawable 的那个字段上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- caretColor(value: ResourceColor): TextInputAttribute：TextInput 的光标色，API 12 起同时决定文本手柄颜色；不写时默认 '#007DFF'（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretColor）
- GradientDrawableSolid 的 color（format="color"）：shape 的 <solid android:color> 就是光标的填充色（出处：Android SDK 平台资源 data/res/values/attrs.xml，GradientDrawableSolid 的 color（按应用的 compileSdk 取对应平台））
- textCursorDrawable 是画在插入光标下面的 drawable（format="reference"）：光标外观完全由它引用的 drawable 决定（出处：Android SDK 平台资源 data/res/values/attrs.xml，textCursorDrawable（按应用的 compileSdk 取对应平台））
- caretColor(value: ResourceColor): TextAreaAttribute：同族接口：TextArea 的光标色（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.caretColor）
- caretColor(value: ResourceColor): RichEditorAttribute：同族接口：RichEditor 的光标色（出处：鸿蒙 SDK 的 ets/component/rich_editor.d.ts，RichEditorAttribute.caretColor）
- 光标色改成 shape 里 solid 的颜色后修好：照抄来的颜色换成源 shape 的颜色（出处：卡里修好并验证过）
针对本应用要查的：
- 光标 shape 的颜色：源工程 res/drawable*/ 下与 textCursorDrawable 引用同名的 XML 的 <solid android:color>；写的是 @color/… 时到 res/values*/colors.xml 按名字找；读出 #RRGGBB 或 #AARRGGBB，原样写进 caretColor
未核实：卡里的验证在鸿蒙 SDK API 22 上，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-84754321501fb68838ca（企业安全培训）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断、建议 2；取值 6 ← 诊断
