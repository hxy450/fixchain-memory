# 启动窗按源端实际启动画面映射：未自定义 SplashScreen 时图标取自适应图标前景层、底色取源主题背景，深色目录不留模板黑底

## 何时使用

资源前置与应用身份迁移阶段，为目标启动窗（module.json5 的 startWindowIcon / startWindowBackground）选定图标与底色资源时

## 适用情境

源工程（如 targetSdk 35）未定义 windowSplashScreen* 主题属性，在 Android 12+ 设备上显示系统启动画面；启动器图标是 adaptive-icon（前景层加背景）；主题是没有夜间变体的 Light 系主题，或 AppCompat 等库的 DayNight 主题（窗口背景取库默认的浅、深两态）；目标工程仍是脚手架 startIcon 与 start_window_background（base 白、dark 黑），身份技能只写“复制前景或 ic_launcher”。

## 例外与边界

- 源端用 windowSplashScreen* 属性或 SplashScreen API 自定义了启动画面，按其声明映射

## 原因

这类应用的 Android 12+ 启动画面由系统按主题背景与自适应图标绘制，旧版栅格 launcher 图不会出现，浅色主题也不会随系统深色变黑。把启动窗当作“替换模板图标”，会选到旧版栅格图、保留模板白底，并把“源端无夜间资源”误读成“保留模板夜间黑底”。

## 做法

1. 启动窗图标取自适应图标的前景层（最高密度的前景 PNG 或矢量），不用旧版栅格 launcher 图；底色取源主题的窗口背景色，base 与 dark 目录都写入：源主题无夜间变体时 dark 写同一浅色；DayNight 主题时 base、dark 分别取库默认的浅、深窗口背景（AppCompat DayNight 为 #FAFAFA 与 #303030）。
2. 主题底色来自 AppCompat 等库的默认值时，到库资源或构建产物（如 aapt2 dump）取确切色值；暂时取不到就在资源映射中登记待核项，不记为“模板保留”。
3. 目标启动窗按图片像素居中显示（来源观察），按源端启动画面中图标的显示尺寸（Android 12 规范中无图标底板为 288dp 见方）乘目标屏密度准备像素，不直接拷贝低分辨率栅格图。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 平台资源 android-30、android-34、android-36.1、android-37.0；androidx.appcompat:appcompat 1.1.0、1.8.0；com.google.android.material:material 1.4.0、1.8.0、1.12.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕安卓 12 起，主题没设 windowSplashScreenBackground 时，系统启动画面的底色按主题的 windowBackground 计算。〔成立范围：对象：API 31 及以上设备上的系统启动画面。条件：主题设了 windowSplashScreenBackground 时以它为准；windowBackground 是图片等非纯色 drawable 时怎样计算，SDK 里看不到。依据是平台 attrs.xml 的属性注释，绘制实现在系统界面里、不在 SDK 源码中。最常见的不成立情形：源端用 windowSplashScreen* 属性或 SplashScreen API 自定义了启动画面（本条经验的例外）。〕
- 〔做法第 1 步〕AppCompat 主题在应用没另设时的窗口背景：Theme.AppCompat.Light 与 Theme.AppCompat.DayNight 的浅色态为 #FAFAFA，Theme.AppCompat 与 DayNight 的深色态为 #303030；API 21 起这两个值来自平台 Theme.Material.Light / Theme.Material 的 colorBackground（windowBackground 取 ?attr/colorBackground）。〔成立范围：对象：parent 链落到 Theme.AppCompat(.Light / .DayNight，含 NoActionBar 子主题) 且链上没有覆写 android:windowBackground、android:colorBackground 的主题；DayNight 在 values 与 values-night 分别以 Theme.AppCompat.Light、Theme.AppCompat 为父。版本：appcompat 1.1.0 与 1.8.0 相同，平台资源 android-30、android-34、android-36.1、android-37.0 相同。最常见的不成立情形：主题继承 MaterialComponents 或 Material3（见下一条），或应用自己覆写了 windowBackground。〕
- 〔做法第 1 步〕MaterialComponents 与 Material3 主题覆写了 android:colorBackground，窗口背景随之不同：Theme.MaterialComponents(.Light / .DayNight) 浅色 #FFFFFF、深色 #121212；Theme.Material3(.Light / .Dark / .DayNight) 在 material 1.8.0 为浅色 #FFFBFE、深色 #1C1B1F，在 1.12.0 至 1.14.0 为浅色 #FEF7FF、深色 #141218（Material3 的 windowBackground 取 ?android:attr/colorBackground）。〔成立范围：对象：com.google.android.material 的这两族主题及其 NoActionBar 子主题，链上未再覆写 colorBackground / windowBackground。版本：MaterialComponents 的值在 1.4.0 与 1.14.0 相同；Material3 的值随库版本变，按源工程实际依赖的版本取。例外：Theme.Material3.DynamicColors.* 在 API 31 起改用系统动态配色，背景随设备而变、无法从资源静态确定。最常见的不成立情形：源工程用的是纯 AppCompat 主题（取上一条的值）。〕
- 〔做法第 1 步〕module.json5 里同一 UIAbility 配了 startWindow（增强启动页）时，startWindowIcon 和 startWindowBackground 不生效，启动页图标与底色改由 startWindow 指向的 profile 里的 startWindowAppIcon、startWindowBackgroundColor 等决定。〔成立范围：对象：module.json5 abilities 中同一 UIAbility 的启动页字段（startWindow 从 API 20 起可用）。例外：startWindow 指向的 profile 没配 startWindowBackgroundColor 时，增强配置整体不生效，回到 startWindowIcon / startWindowBackground 的简易启动页。依据是文档说明。最常见的不成立情形：脚手架工程只配了 startWindowIcon / startWindowBackground、没有 startWindow，这两项照常生效。〕
- 〔做法第 3 步〕简易启动页的 startWindowIcon 按图标资源的实际大小在启动页居中显示，不随窗口尺寸缩放。〔成立范围：对象：未配 startWindow 时的 startWindowIcon。对照：增强启动页的 startWindowAppIcon 由系统缩放到完全显示在展示区内。依据是文档说明；「实际大小」按像素还是按屏幕密度换算，文档没写。最常见的不成立情形：配了 startWindow。〕
- 〔做法第 1 步〕应用没有调用 setColorMode 时，resources 的 dark 目录下有深色资源，系统组件在深色模式下自动切成深色；dark 目录下没有任何深色资源时，系统组件在深色模式下保持浅色。〔成立范围：对象：工程 resources 的 dark 限定词目录与系统组件的深浅色。条件：应用调用了 setColorMode 时以接口为准。依据是文档说明；dark 目录里只放与 base 同值的颜色是否也算「有深色资源」，文档没写。最常见的不成立情形：应用在入口调用 setColorMode 固定了浅色。〕
