# 还原 EditText 光标时读 textCursorDrawable，没写就顺主题查，写成 caretStyle

审的是：代码
触发（任一种）：
- 读到：EditText 写了 android:textCursorDrawable="@drawable/…"，或没写它、光标由所在 Activity 的主题决定；写错的样子：TextInput 的 .caretColor / .caretStyle 照抄别的字段、别的页面或凭记忆写，没核对源 drawable 或主题
适用范围：把安卓 EditText 的光标外观迁成 ArkUI TextInput（TextArea、Search 同理）时
做法：
- 写了 textCursorDrawable 的：打开它引用的 drawable XML，读 <solid android:color>（是 @color/… 再解析到色值）和 <size android:width>
- 没写的：顺着所在 Activity 的主题查 textCursorDrawable、colorControlActivated、colorAccent；借别页的光标前先核对两页主题解析出同一结果
- 写成 .caretStyle({ width: <dp 数值>, color: <颜色> })，只加在源端能查出光标外观的那个字段上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- text_cursor_material：<size android:width="2dp">，android:tint="?attr/colorControlActivated"：例：Material 主题没覆盖 textCursorDrawable 时，默认光标 2dp 宽，颜色取主题的 colorControlActivated（出处：Android SDK 平台资源 data/res/drawable/text_cursor_material.xml（按应用的 compileSdk 取对应平台））
- <item name="colorControlActivated">?attr/colorAccent</item>：Material 主题没覆盖时，colorControlActivated 等于 colorAccent（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 colorControlActivated（按应用的 compileSdk 取对应平台））
- caretStyle(value: CaretStyle): TextInputAttribute；CaretStyle { width?: Length; color?: ResourceColor }：光标的宽度和颜色一起设（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretStyle；ets/component/text_common.d.ts，CaretStyle）
- Length 写 number 时默认单位 vp：width: 2 即 2vp，对应源端 2dp（出处：ts-types.md，Length）
- caretColor(value: ResourceColor): TextInputAttribute，默认 '#007DFF'：不写光标色时用这个默认值（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.caretColor）
针对本应用要查的：
- 光标 drawable 的颜色和宽度：源工程 res/drawable*/ 下与 textCursorDrawable 引用同名的 XML；颜色写成 @color/… 时到 res/values*/colors.xml 按名字找；读 <solid android:color> 的 #RRGGBB / #AARRGGBB 和 <size android:width> 的 dp 数值
- 源输入框所在 Activity 的主题给的光标：源工程 AndroidManifest.xml 里这个 <activity> 的 android:theme（没写看 <application android:theme>），顺着 res/values*/ 下 styles、themes XML 的 parent 链；继承 AppCompat 或 MaterialComponents 的，到依赖库包内 res/values/values.xml 按同名项查；链上离控件最近的一项给出值；没覆盖 textCursorDrawable 时按平台默认光标 drawable 读宽度和 tint，再把 colorControlActivated 解析到颜色
未核实：源 EditText 没写 textCursorDrawable 时两张卡的修法冲突：case-84754321501fb68838ca 去掉显式 caretColor、用鸿蒙默认光标色；case-f6c7146888f4d05c7874 按同一 Activity 的安卓实测写 .caretStyle({ width: 2, color: <主题色> })；不写 caretColor 时鸿蒙默认 '#007DFF'，和安卓主题给的默认光标色是否一致未核实；默认光标由 text_cursor_material 和 colorControlActivated 决定，是按平台资源推出的，卡里没验证；主题继承 AppCompat、MaterialComponents 时由依赖库覆盖的光标项，族里规矩没有查实过
来源：2 张卡，1 个应用
- case-84754321501fb68838ca（企业安全培训）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 2
- case-f6c7146888f4d05c7874（企业安全培训）：做法第 2 步 ← 建议 1、建议 2；做法第 3 步 ← 建议 4
