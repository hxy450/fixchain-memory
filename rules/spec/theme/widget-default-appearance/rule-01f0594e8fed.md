# 页面规格列出 TextView 的文本和字号时，同时写明未声明 textColor 时主题给的颜色

审的是：规格
触发（任一种）：
- 读到：源布局的 TextView 有 android:text、android:textSize，没有 android:textColor、android:textAppearance、style；写错的样子：页面规格或映射参考里这个控件只记了文本和字号，没有颜色这一项，也没写颜色来自主题
适用范围：规格提取阶段写页面规格的控件外观时，源控件颜色由主题隐式提供的情形
做法：
- 在这个控件的外观里写一项：「文字颜色：源控件未声明 textColor，取主题默认 textAppearanceSmall 的 ?android:textColorSecondary（AppCompat/Material 浅色 #8A000000、深色 #B3FFFFFF），目标 Text 须显式写 fontColor」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.TextView：<item name="textAppearance">?attr/textAppearanceSmall</item>：TextView 没写 textAppearance/style 时文字外观取主题的 textAppearanceSmall（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.TextView（按应用的 compileSdk 取对应平台））
- secondary_text_default_material_light = #8a000000；secondary_text_default_material_dark = #b3ffffff：AppCompat/Material 默认次要文字色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，secondary_text_default_material_light / secondary_text_default_material_dark（按应用依赖的版本））
- Text.fontColor 默认值 '#e6182431'：规格不写颜色、下游也不写时目标 Text 用的近黑色（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontColor）
针对本应用要查的：
- 应用主题有没有覆盖次要文字色：源工程 AndroidManifest.xml 的 android:theme 指向的主题，在 res/values*/styles.xml 或 themes.xml 里顺 parent 链找 textColorSecondary、textColorTertiary、textViewStyle；没覆盖就在规格里写主题族默认值；有覆盖就写覆盖后的值及其出处
来源：1 张卡，1 个应用
- case-9ec2a14cbd1df18e3620（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、建议 1
