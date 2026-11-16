# 给源端默认字色建的颜色键，base 和 dark 照 TextView 默认链取次级文字色，不填主文字色

审的是：资源
触发（任一种）：
- 读到：源 TextView 没写 android:textColor，主题继承 Theme.AppCompat.DayNight.* 或平台 Material 主题，且未覆盖 textAppearanceSmall、textColorTertiary；写错的样子：目标 base/element/color.json 为这些文字新建的键填 #DE000000，dark/element/color.json 填 #FFFFFFFF（主文字色的取值）
适用范围：为未设字色的源 TextView 在目标 element 资源里建颜色键时
不适用的情形：EditText、Button 等控件的默认 textAppearance 不同，要各自解析，不套用这条的取值
做法：
- base/element/color.json 里这个键填 #8A000000，dark/element/color.json 里同名键填 #B3FFFFFF；主题有覆盖时改按覆盖值解析
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- secondary_text_default_material_light = #8a000000；secondary_text_default_material_dark = #b3ffffff：TextView 默认链（textAppearanceSmall → textColorTertiary）最终的颜色（出处：Android SDK 平台资源 data/res/values/colors_material.xml，secondary_text_default_material_light / _dark（按应用的 compileSdk 取对应平台））
- 白底上实测 #757575：核对用的观察值（出处：卡里修好并验证过）
针对本应用要查的：
- 主题是否覆盖次级文字色：源工程 res/values*/styles.xml、themes.xml（含 values-night）里应用主题的 android:textColorTertiary、android:textColorSecondary、android:textAppearanceSmall；有覆盖就按覆盖值分别填 base 和 dark；没有就用上面的默认值
来源：1 张卡，1 个应用
- case-64a967d716ed18688332（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；例外 1 ← 建议 1；取值 2 ← 诊断
