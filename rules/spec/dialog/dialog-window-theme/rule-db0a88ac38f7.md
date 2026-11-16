# Theme.*.Dialog 主题的 Activity，规格逐项写库主题定的暗化、宽度、点外关闭和底色圆角

审的是：规格
触发（任一种）：
- 读到：AndroidManifest.xml 里 Activity 的 android:theme 是 Theme.*.Dialog（如 Theme.MaterialComponents.Light.Dialog、Theme.AppCompat.Light.Dialog）；写错的样子：规格只写「Dialog 主题」「居中卡片形态」，没写暗化比例、窗口宽度和 inset、点外是否关闭、窗口底色和圆角，也没标「未知」
适用范围：Dialog 主题 Activity 迁成 Dialog 形态页或弹窗时，规格里写窗口形态的那一节
做法：
- 顺着主题的 parent 链查出 android:backgroundDimAmount、窗口宽度 / inset（windowBackground 的 inset、windowMinWidthMinor）、android:windowCloseOnTouchOutside、窗口底色和圆角，逐项写进规格
- 查不到的项写「未知，需查 appcompat / material 主题默认值」，不留给实现者猜
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <item name="backgroundDimAmount">0.6</item>：平台基础主题的暗化比例，链上没有覆盖时就是 0.6（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme 的 backgroundDimAmount（按应用的 compileSdk 取对应平台））
- Theme.Dialog 的 windowCloseOnTouchOutside 取 @bool/config_closeDialogWhenTouchOutside，值为 true：平台对话框主题默认点外关闭（出处：Android SDK 平台资源 data/res/values/themes.xml，Theme.Dialog；data/res/values/config.xml，config_closeDialogWhenTouchOutside（按应用的 compileSdk 取对应平台））
- Base.V7.Theme.AppCompat.Light.Dialog：android:windowBackground = @drawable/abc_dialog_material_background，android:windowCloseOnTouchOutside = true：appcompat 对话框主题的窗口底和点外关闭（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Theme.AppCompat.Light.Dialog（按应用依赖的版本））
- abc_dialog_material_background：四边 inset 16dp，solid @android:color/white，corners ?attr/dialogCornerRadius（= abc_dialog_corner_radius_material 2dp）：appcompat 对话框窗口的边距、底色和圆角（出处：androidx.appcompat:appcompat 包内 res/drawable-v21/abc_dialog_material_background.xml 和 res/values/values.xml，abc_dialog_corner_radius_material（按应用依赖的版本））
- Theme.MaterialComponents.Light.Dialog → Base.Theme.MaterialComponents.Light.Dialog → … → Platform.MaterialComponents.Light.Dialog（parent Theme.AppCompat.Light.Dialog）：material 的浅色对话框主题最终继承 appcompat 的对话框主题（出处：com.google.android.material:material 包内 res/values/values.xml，Platform.MaterialComponents.Light.Dialog（按应用依赖的版本））
- Theme.MaterialComponents.Light.Dialog 下按 0.6 暗化、95% 宽 + 16 inset、白底、圆角 2、点遮罩关闭：返修按主题得出的值（出处：卡里修好并验证过）
针对本应用要查的：
- 主题链上实际提供每一项的 style：从 manifest 的主题名出发，在依赖库 material / appcompat 包内 res/values/values.xml 和 Android SDK 平台资源 themes*.xml、dimens.xml 里按 style 的 parent 往上找；取链上离主题最近的那一项；值是 @dimen / @drawable / ?attr 引用时再解析到具体值。例：material 1.12.0 + appcompat 1.7.1 下窗口底来自 appcompat 的 abc_dialog_material_background
未核实：窗口宽 95% 出自卡里返修的结果；plain Light.Dialog 链上 windowMinWidthMinor 由哪一层提供没有逐层核到
来源：1 张卡，1 个应用
- case-ac1b65b76f72e7be3fa6（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 6 ← 诊断
