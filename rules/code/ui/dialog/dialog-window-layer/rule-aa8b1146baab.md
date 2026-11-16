# Dialog 形态的源端控件迁成自绘弹窗时，补上窗口层的投影、遮罩、圆角和宽度

审的是：代码
触发（任一种）：
- 读到：源端是 Dialog 形态（MaterialDialog、AlertDialog、DialogPreference），对话框主题属 Theme.MaterialComponents.Light.Dialog、Theme.AppCompat 一类；写错的样子：目标 openCustomDialog 的弹窗只做了内容区：没有 shadow 投影，maskColor、圆角、宽度没按源端主题写
适用范围：源端 Dialog 的窗口层外观（投影、背景变暗、圆角、宽度）来自主题和库、项目 res/ 里没有这些值时
做法：
- 从源端生效的对话框主题查出 windowElevation、backgroundDimAmount、圆角和最小宽度，写成弹窗窗口层的常量
- 给弹窗加上窗口投影，遮罩按 backgroundDimAmount 写 maskColor，圆角、宽度按主题值写；源项目 res/ 里没有不等于没有
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog(options: promptAction.CustomDialogOptions): Promise<number>，CustomDialogOptions 里有 shadow?: ShadowOptions | ShadowStyle、cornerRadius?: Dimension | BorderRadiuses、width?: Dimension：用 builder 形式打开自定义弹窗时，投影、圆角、宽度写在选项里（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog；ets/api/@ohos.promptAction.d.ts，CustomDialogOptions）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：ComponentContent 形式只收 BaseDialogOptions，其中没有 shadow、cornerRadius，投影和圆角要画在内容根组件上（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- maskColor?: ResourceColor：BaseDialogOptions 的遮罩颜色（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.maskColor）
- Dialog 窗口带 elevation 投影；返修加了窗口投影常量：源端对话框有窗口投影（出处：卡里修好并验证过）
针对本应用要查的：
- 源端对话框窗口的 windowElevation、backgroundDimAmount、圆角和最小宽度：源工程 AndroidManifest 里 Activity 或应用的主题 → 它的 dialogTheme / alertDialogTheme；再到 Android SDK 平台资源 data/res/values/themes_material.xml，或 androidx.appcompat:appcompat、com.google.android.material:material 包内 res/values/values.xml 里按主题名找；顺着 parent 找到提供 windowElevation、backgroundDimAmount 的那一项并解析 @dimen；例：平台 Theme.Material.Light.BaseDialog 下 windowElevation 是 @dimen/floating_window_z（16dp），Theme.Material 的 backgroundDimAmount 是 0.6；appcompat 1.7.1 的 abc_dialog_corner_radius_material 是 2dp
未核实：卡里的返修把投影写在哪一层（选项还是内容根组件）卡里没写明；卡里环境是 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-e91d2b9a9a156d1023ec（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
