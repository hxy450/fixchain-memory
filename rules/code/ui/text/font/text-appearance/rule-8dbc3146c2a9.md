# EditText 没写 android:textColor 时，按主题解析默认文字色写 fontColor，不沿用硬编码

审的是：代码
触发（任一种）：
- 读到：源布局的 EditText（含它的 style）没有 android:textColor，可能只写了 android:textColorHint；文字色由 Manifest 里 Activity 或 application 的 android:theme 决定；写错的样子：对应 TextInput 的 .fontColor(...) 是目标端原有的硬编码色，或按「同组统一」给几个框写成同一个现值，不是从主题解析出的默认文字色
适用范围：源 EditText 未声明 textColor、文字色来自 Activity 或应用主题时，迁成 ArkUI TextInput 的 fontColor
做法：
- 先确认源 EditText 和它的 style 有没有声明 android:textColor；没有时按控件 style → Activity 主题 → 应用主题找 editTextColor，再顺着 ?android:attr/textColorPrimary 解析到颜色值
- 把解析出的值写进 .fontColor(...)；带透明度的值按背景预合成（例：AppCompat Light 主题、白底时 #DE000000 约为 #212121）。目标端已有的硬编码值和「同组统一」都不当源值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.EditText：textColor = ?attr/editTextColor：平台 EditText 默认样式的文字色取主题的 editTextColor（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.EditText（按应用的 compileSdk 取对应平台））
- Theme.Material：editTextColor = ?attr/textColorPrimary：平台 Material 主题里 editTextColor 指向 textColorPrimary（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 editTextColor（按应用的 compileSdk 取对应平台））
- Base.V7.Widget.AppCompat.EditText：android:textColor = ?attr/editTextColor；Base.V7.Theme.AppCompat.Light：editTextColor = ?android:attr/textColorPrimary：AppCompat 主题下 EditText 的文字色同样落到 textColorPrimary（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Widget.AppCompat.EditText、Base.V7.Theme.AppCompat.Light（按应用依赖的版本））
- Theme.Material.Light：textColorPrimary = @color/text_color_primary，即 colorForeground（@color/black）乘 primaryContentAlpha（0.87），约 #DE000000：浅色 Material 主题的主文字色（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light 的 textColorPrimary；data/res/color/text_color_primary.xml；data/res/values/colors_material.xml，primary_content_alpha_material_light（按应用的 compileSdk 取对应平台））
- primary_text_default_material_light = #de000000：AppCompat 浅色主文字色的默认值（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，primary_text_default_material_light（按应用依赖的版本））
- fontColor(value: ResourceColor): TextInputAttribute：TextInput 的文字色；声明里只写了穿戴设备的默认值，手机上要显式写（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.fontColor）
- fontColor(value: ResourceColor): TextAreaAttribute：同族接口：TextArea 的文字色（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.fontColor）
- fontColor(value: ResourceColor): SearchAttribute：同族接口：Search 的文字色（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.fontColor）
针对本应用要查的：
- 源 EditText 实际生效的文字色：源工程布局 XML 里这个 EditText 的 style 属性 → AndroidManifest.xml 里 activity / application 的 android:theme → 应用 res/values 的 styles、themes 里这个主题的 parent 链 → 所继承的库主题（AppCompat、Material Components）或平台主题；找到第一个提供 editTextColor 或 android:textColorPrimary 的项，顺着 @color/… 或 ?attr/… 解析到颜色值；是 selector 时取默认 item（enabled 状态）的颜色
未核实：白底 #212121 是按 AppCompat Light 默认 textColorPrimary 推算的，卡里没有真机取色复核；平台主题的文字色在运行设备的系统资源里解析，本机只核了 android-36 的定义
来源：1 张卡，1 个应用
- case-784ba4ab52f98f7156b6（企业安全培训）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
