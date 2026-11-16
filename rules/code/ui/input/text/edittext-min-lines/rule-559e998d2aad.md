# 多行 EditText 带 minLines 时，最小高度用源字体实际行距算，内容不足时竖直居中

审的是：代码
触发（任一种）：
- 读到：EditText 带 android:minLines（未声明 android:gravity）；写错的样子：TextArea 的 minHeight 按估算行高（如 4/3 em）算，lineHeight 写裸数字，文字顶对齐
适用范围：源端多行 EditText 迁成 TextArea、内容可能不足 minLines 行时
做法：
- 最小高度 = 上内距 + minLines × 源字体在该字号下的实际行距 + 下内距；行距写成带单位的值（如 lineHeight('21.1vp')），不写裸数字
- 内容不足 minLines 行时按 EditText 默认 gravity center_vertical 竖直居中
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.EditText 的 gravity 是 center_vertical：源端未写 gravity 时内容竖直居中（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.EditText（按应用的 compileSdk 取对应平台））
- lineHeight(value: number | string | Resource): TextAreaAttribute；number 的单位是 fp：裸数字按 fp 解释，源端行距是 dp 时写成 'Nvp'（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.lineHeight）
- 18sp 等宽字体源端行距实测 21.1dp，按 4/3 em 估成 24 偏大：估算行高与实测的差距（出处：卡里修好并验证过）
- lineHeight(value: number | string | Resource): TextInputAttribute：同族接口：TextInput 的行高，number 同样按 fp（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.lineHeight）
针对本应用要查的：
- 源字体在该字号下的实际行距：源工程布局里这个 EditText 的 textSize、fontFamily / typeface；按该字体的字体度量算出行距（或在源端真机上量），换成 vp 写进 lineHeight 和最小高度
未核实：卡里没写 ArkUI 端竖直居中的具体写法
来源：1 张卡，1 个应用
- case-9d195db79dc4cccc7d1a（Sokoban）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；取值 3 ← 诊断
