# 启动窗按源端实际启动画面映射：未自定义 SplashScreen 时图标取自适应图标前景层、底色取源主题背景，深色目录不留模板黑底

## 何时使用

资源前置与应用身份迁移阶段，为目标启动窗（module.json5 的 startWindowIcon / startWindowBackground）选定图标与底色资源时

## 适用情境

源工程（如 targetSdk 35）未定义 windowSplashScreen* 主题属性，在 Android 12+ 设备上显示系统启动画面；启动器图标是 adaptive-icon（前景层加背景）；主题是没有夜间变体的 Light 系主题，或 AppCompat 等库的 DayNight 主题（窗口背景取库默认的浅、深两态）；目标工程仍是脚手架 startIcon 与 start_window_background（base 白、dark 黑），身份技能只写“复制前景或 ic_launcher”。“源主题”指启动器 Activity 的 android:theme，它没设时才取 application 的主题。#FAFAFA、#303030 只是 AppCompat 一系 DayNight 在主题链没有覆盖 windowBackground 时的默认值：Theme.MaterialComponents.DayNight 一系在 API 21 起默认为日间 #FFFFFF、夜间 #121212，Material3 等其他主题族也按应用依赖的库版本另行解析，不套 AppCompat 的值。

## 例外与边界

- 源端用 windowSplashScreen* 属性或 SplashScreen API 自定义了启动画面，按其声明映射

## 原因

这类应用的 Android 12+ 启动画面由系统按主题背景与自适应图标绘制，旧版栅格 launcher 图不会出现，浅色主题也不会随系统深色变黑。把启动窗当作“替换模板图标”，会选到旧版栅格图、保留模板白底，并把“源端无夜间资源”误读成“保留模板夜间黑底”。

## 做法

1. 启动窗图标取自适应图标的前景层（最高密度的前景 PNG 或矢量），不用旧版栅格 launcher 图；底色取源主题的窗口背景色，base 与 dark 目录都写入：源主题无夜间变体时 dark 写同一浅色；DayNight 主题时 base、dark 分别取库默认的浅、深窗口背景（AppCompat DayNight 为 #FAFAFA 与 #303030）。
2. 主题底色来自 AppCompat 等库的默认值时，到库资源或构建产物（如 aapt2 dump）取确切色值；暂时取不到就在资源映射中登记待核项，不记为“模板保留”。
3. 目标启动窗按图片像素居中显示（来源观察），按源端启动画面中图标的显示尺寸（Android 12 规范中无图标底板为 288dp 见方）乘目标屏密度准备像素，不直接拷贝低分辨率栅格图。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36、android-37.0 的平台资源；android-36.1 的源码；androidx.appcompat:appcompat 1.1.0、1.7.0、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕源端 targetSdk 不低于 31、主题没有写 windowSplashScreen* 属性时，在 Android 12 及以上设备上启动画面由系统按主题窗口背景和自适应图标绘制，旧版栅格 launcher 图（如大尺寸 logo PNG）不会出现
- 〔例外与边界 / 做法第 1 步〕安卓主题属性 windowSplashScreenAnimatedIcon 替换启动窗中央的图标（动画 drawable 会播放动画）；windowSplashScreenBackground 是启动画面背景色，主题没有设置时系统从 windowBackground 计算
- 〔做法第 1 步〕安卓自适应图标的前景、背景两层都按 108×108dp 绘制，只有中央 72×72dp 出现在遮罩视口内，四周各 18dp 留给系统做遮罩和视觉效果
- 〔适用情境 / 做法第 1、2 步〕主题链上没有任何一层覆盖 windowBackground 时：平台 Theme.Material.Light 的 windowBackground 为 ?attr/colorBackground，解析到 background_material_light = material_grey_50 = #fffafafa；appcompat 的 Light 主题在 API 21 起经 Platform.V21.AppCompat.Light 继承 android:Theme.Material.Light.NoActionBar，取到同一个 #fffafafa（appcompat 1.1.0、1.8.0 相同）
- 〔适用情境 / 做法第 1、2 步〕应用主题是 Theme.AppCompat.DayNight 且主题链上没有覆盖 windowBackground 时（appcompat 1.7.0、平台 android-36 资源）：日间为 #fffafafa（Theme.Material.Light 的 background_material_light），夜间为 #ff303030（Theme.Material 的 colorBackground = background_material_dark = material_grey_850）
- 〔何时使用 / 做法第 1 步〕module.json5 abilities 里的 startWindowIcon（启动页面图标资源索引）和 startWindowBackground（启动页面背景颜色资源索引，如 $color:red）都不可缺省，取值不超过 255 字节；同一 UIAbility 配置了 startWindow 标签时这两项都不生效
- 〔做法第 1 步〕简易启动页的 startWindowIcon 用于展示应用图标，不会随窗口尺寸缩放
- 〔原因 / 做法第 1 步〕resources 下深色模式的限定词目录名为 dark：base/element/color.json 与 dark/element/color.json 里定义同名颜色时，深色模式下取 dark 里的值；dark 目录里没有这一项时回落到 base 里的值
