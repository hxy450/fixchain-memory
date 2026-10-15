# 源端未自定义 SplashScreen 时，启动窗按 Android 12+ 系统启动画面取自适应图标与主题窗口背景，dark 不留模板黑底

ID：`lesson-c4af68b3ee1456525e8e` · 版本：6

[本主题](index.md)

## 何时使用

资源前置与应用身份迁移阶段，为目标启动窗（module.json5 的 startWindowIcon / startWindowBackground）选定图标与底色资源时

## 适用情境

源主题未定义 windowSplashScreen* 属性、也未调用 SplashScreen API，在 Android 12+ 设备上显示系统启动画面；启动器图标是 adaptive-icon（前景层加背景）；主题是没有夜间变体的 Light 系主题，或 AppCompat 等库的 DayNight 主题；目标工程仍是脚手架 startIcon 与 start_window_background（base 白、dark 黑），身份技能只写“复制前景或 ic_launcher”。

## 例外与边界

- 源端用 windowSplashScreen* 属性或 SplashScreen API 自定义了启动画面，按其声明映射

## 原因

Android 12+ 的系统启动画面由系统按主题与自适应图标绘制：底色取 windowSplashScreenBackground，未设时由 windowBackground 计算（attrs.xml 注释）；旧版栅格 launcher 图不会出现，浅色主题也不会随系统深色变黑。把启动窗当作“替换模板图标”，会选到旧版栅格图、保留模板白底，并把“源端无夜间资源”误读成“保留模板夜间黑底”。

## 做法

1. 图标用自适应图标，不用旧版栅格 launcher 图，并按源端启动画面实际显示的形态取：只显示前景时取前景层（最高密度 PNG 或矢量）；显示带背景的遮罩图标时，前景与背景两层合成（两层同尺寸，见 adaptive-icon 转分层图标一条）。尺寸按 Android 12+ 规范（developer.android.com Splash screens 的 Splash screen dimensions，2026-10-15 访问）：带图标背景时图标资产 240×240dp、内容在直径 160dp 的圆内；不带图标背景时 288×288dp、内容在直径 192dp 的圆内；圆外的内容被系统遮掉、不可见。准备目标图时保留这张画布和四周留白，只让遮罩后可见的部分显示：圆外本来透明，或目标启动窗已有等价的圆形遮罩时，整张图直接用；圆外有像素时，先按对应直径的圆把圆外置透明再用。背景层与启动底色同色、且遮罩后的可见轮廓一致时，两种形态外观一致，取前景层即可；不同色时在 Android 12+ 设备或模拟器冷启源端 APK 截图确定；无法运行源端时，在资源映射中写明“图标是否带背景未确认”及其对启动窗外观的影响并上报。
2. 底色取源主题的窗口背景色，base 与 dark 目录都写入：windowBackground 是纯色或颜色引用时直接取；是 layer-list 等 drawable 时，系统只从它计算一个启动底色（attrs.xml 的 windowSplashScreenBackground 注释），计算方法本机 SDK 未说明，在 Android 12+ 设备冷启源端截图取色，不把整张闪屏图搬进启动窗。源主题无夜间变体时 dark 写同一浅色；DayNight 主题时 base、dark 分别取库默认的浅、深窗口背景。
3. 库默认色到所用库版本的资源里取：Gradle 缓存中 appcompat（或 Material Components）aar 的 res/values 与 res/values-night（androidx.appcompat 为 background_material_light/background_material_dark，例：appcompat 1.7.0 中主题未覆盖 windowBackground/colorBackground 时为 #FAFAFA 与 #303030，以所用库版本的实际资源为准），或对源 APK 运行 aapt2 dump resources；缺构建输入时上报缺哪个库与版本，不记为“模板保留”。
4. 目标启动窗在来源案例的目标模拟器上按图片原始像素居中显示（卡中观察，未核其他设备与版本）：按所选形态的资产尺寸乘目标屏密度准备像素，不直接拷贝低分辨率栅格图。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0405ee7ad27947343068](../../../store/cases/case-0405ee7ad27947343068/bf5f2b704057881d8a4286c94e68e8f3cd0fed3b7d69925e72bac0ae69947102.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`bf5f2b704057881d8a4286c94e68e8f3cd0fed3b7d69925e72bac0ae69947102`
- [case-4f7163b95249e9ede2ca](../../../store/cases/case-4f7163b95249e9ede2ca/8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f.json) · 结论：diagnosis, recommendation:3
  卡片版本：`8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f`
