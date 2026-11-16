# 源 targetSdk≥31 且没写 windowSplashScreen* 时，启动窗图标取自适应图标前景层

审的是：资源
触发（任一种）：
- 读到：AndroidManifest 的 android:icon 指向 anydpi-v26 下的 <adaptive-icon>（<foreground>、<background>），targetSdkVersion ≥ 31，主题里没有 android:windowSplashScreen* 属性；写错的样子：module.json5 的 startWindowIcon 指向的 startIcon.png 换成了旧版栅格 launcher 图（如方形带底色的 logo），或仍是脚手架图
适用范围：为鸿蒙 UIAbility 的启动窗选图标、源端走 Android 12+ 系统启动画面时
做法：
- startIcon.png 取自适应图标 <foreground> 引用的前景层图（取最高密度的 mipmap，如 mipmap-xxxhdpi 下那张），不用旧版栅格 launcher 图替代
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- windowSplashScreenAnimatedIcon：替换启动窗中央的图标：源端写了它时启动图标以它为准；没写时看下一项（出处：Android SDK 平台资源 data/res/values/attrs.xml，Window 的 windowSplashScreenAnimatedIcon（按应用的 compileSdk 取对应平台））
- targetSdk ≥ 31 在 Android 12+ 上，启动画面由系统按主题背景和自适应图标绘制，旧版栅格 logo 不会出现：源端没写 windowSplashScreen* 时的启动表现（出处：卡里修好并验证过）
- startWindowIcon：当前 UIAbility 启动页面图标资源的索引，如 $media:startIcon；配置了 startWindow 标签时它不生效：目标端启动窗图标的配置位置（出处：module-configuration-file.md，abilities 标签 startWindowIcon）
- 换成前景层图后，冷启连拍两端启动画面一致：修复后的观察（出处：卡里修好并验证过）
针对本应用要查的：
- 启动画面用的是哪张图：源工程 AndroidManifest 的 application / activity 的 android:icon，顺着引用到 drawable-anydpi-v26 或 mipmap-anydpi-v26 的 adaptive-icon XML；读 <foreground android:drawable> 引用的资源名，到各 mipmap-*dpi 目录取最高密度那张
来源：1 张卡，1 个应用
- case-0405ee7ad27947343068（2048）：做法第 1 步 ← 建议 1；取值 2 ← 诊断；取值 4 ← 诊断
