# 启动窗按源端实际启动画面映射：未自定义 SplashScreen 时图标取自适应图标前景层、底色取源主题背景，深色目录不留模板黑底

ID：`lesson-c4af68b3ee1456525e8e` · 版本：3 · 阶段：execute · 主题：[app/resources](index.md)

概要：启动窗图标取自适应前景层，底色取源主题窗口背景

信号：`startWindowIcon`, `startWindowBackground`, `start_window_background`, `windowSplashScreen`, `SplashScreen`, `adaptive-icon`, `DayNight`, `#FAFAFA`, `aapt2`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [应用显示名同时改 AppScope 与入口 label 值](lesson-55f44e2efdc1a49ac387.lesson.md)（共享 1 张卡）
- [推进阶段前核对约定产物与放行门，待接事项落负责方](../../process/handoff-loss/lesson-5754b7be28238f1bdf57.lesson.md)（共享 1 张卡）
- [Material 图标按同变体从可核来源取 pathData](../../ui/graphics/icons/lesson-74d535afb21b2270119e.lesson.md)（共享 1 张卡）
- [app.json5 的 icon 改指分层图标并补齐前景背景](lesson-feec63f65102f5396e51.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0405ee7ad27947343068](../../../../store/cases/case-0405ee7ad27947343068/bf5f2b704057881d8a4286c94e68e8f3cd0fed3b7d69925e72bac0ae69947102.json) · 结论：diagnosis, rec-d7e115ce25, rec-1e4c00a35a, rec-c1218083d1, rec-319e1a8f86
  卡片版本：`bf5f2b704057881d8a4286c94e68e8f3cd0fed3b7d69925e72bac0ae69947102`
- [case-4f7163b95249e9ede2ca](../../../../store/cases/case-4f7163b95249e9ede2ca/8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f.json) · 结论：diagnosis, rec-8fc1e38726
  卡片版本：`8d4d0d18e9bd68c6ddc5554130ad97c38ea483d147b5bdff45d24a790e1ea78f`
