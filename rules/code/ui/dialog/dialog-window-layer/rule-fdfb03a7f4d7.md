# 源主题由应用窗口画状态栏底色且目标非全屏时，弹窗期间把 statusBarColor 切成压暗色

审的是：代码
触发（任一种）：
- 读到：源端用 AlertDialog / Dialog 窗口，应用主题是 Theme.Material 及以后（windowDrawsSystemBarBackgrounds=true，statusBarColor=?attr/colorPrimaryDark 且不透明），对话框按 backgroundDimAmount 压暗；写错的样子：openCustomDialog 只写了 maskColor（如按 dim 0.6 得到的 `#99000000`），onWillAppear / onWillDisappear 里没有切主窗口的状态栏底色
适用范围：源对话框是独立窗口、源主题由应用窗口绘制不透明的状态栏底色（平台 attrs.xml 声明：targetSdk ≥ 35 时 statusBarColor 被忽略），目标窗口保持非全屏、用 openCustomDialog 等系统弹窗承载时
做法：
- 弹窗的 onWillAppear 里计数加一，并把主窗口状态栏底色切成「原底色每个通道 × (1 − dim)」：window.getLastWindow(ctx) 后调 setWindowSystemBarProperties({ statusBarColor: '#FF…' })；onWillDisappear 里计数减一，最后一个弹窗关闭时恢复原底色；状态栏图标颜色不改
- 做成共享工具，所有 openCustomDialog 的打开处（共享弹窗工具和各页宿主）统一挂上，不在各页分别处理
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Material、Theme.Material.Light：windowDrawsSystemBarBackgrounds=true，statusBarColor=?attr/colorPrimaryDark，backgroundDimAmount=0.6：源端状态栏底色由应用窗口画，对话框 dim 默认 0.6（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light（按应用的 compileSdk 取对应平台））
- windowDrawsSystemBarBackgrounds 为 true 且窗口不浮动时，系统栏背景透明，由这个窗口在对应区域填 statusBarColor：源对话框窗口的 dim 盖在应用窗口之上，连应用窗口画的状态栏底色一起压暗（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowDrawsSystemBarBackgrounds（按应用的 compileSdk 取对应平台））
- maskRect?: Rectangle —— Mask Region of dialog. The size can't exceed the main window.：弹窗遮罩不超出主窗口；非全屏时状态栏由系统画在主窗口之外，maskColor 压不到（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.maskRect）
- onWillAppear?: () => void；onWillDisappear?: () => void：弹窗开场动画前、关场动画前的回调，挂切换和恢复（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.onWillAppear / onWillDisappear）
- setWindowSystemBarProperties(systemBarProperties: SystemBarProperties): Promise<void>：设置主窗口系统栏属性（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowSystemBarProperties）
- statusBarColor?: string，入参为十六进制 RGB 或 ARGB，如 '#FF00FF00'：状态栏背景色的写法（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.statusBarColor；arkts-apis-window-i.md，SystemBarProperties）
- 按「原底色每个通道 × (1 − dim)」切换后，弹窗打开时状态栏取样与源端对话框打开时一致，图标颜色不变，关闭后恢复：改后的效果（出处：卡里修好并验证过）
针对本应用要查的：
- 源端状态栏底色和对话框 dim 值：源工程 AndroidManifest 里 application / activity 的 android:theme，再到源工程 res/values*/styles.xml 里这个主题的 statusBarColor、colorPrimaryDark、backgroundDimAmount；没覆盖的顺着父主题到 Android SDK 平台资源 themes_material.xml 找；底色取 statusBarColor 解析出的颜色，dim 取 backgroundDimAmount；压暗色 = 每个 RGB 通道 × (1 − dim)，alpha 保持 FF。例：Theme.Material 族没覆盖时 dim 是 0.6
- 源应用的 targetSdk：源工程模块的 Gradle 构建脚本里的 targetSdk（或 targetSdkVersion）；低于 35 时 statusBarColor 生效，本规矩的前提成立；35 及以上时平台声明 statusBarColor 被忽略，要另看源端状态栏实际怎么画
未核实：横屏和三键导航两种情形卡里没有记录复测结果
来源：1 张卡，1 个应用
- case-5056fd5bebd86cb55f92（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 7 ← 诊断
