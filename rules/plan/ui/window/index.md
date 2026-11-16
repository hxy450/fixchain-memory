# 窗口与系统栏

源端有 FEATURE_NO_TITLE、FLAG_FULLSCREEN、ImmersionBar、Scaffold innerPadding、状态栏底色，或者派工、slot 契约、前向引用、交付说明里写到沉浸、安全区避让值（statusBarHeight）、系统栏颜色时

## 触发族

- [UI 清单和派工里的源端系统栏形态](source-system-bars/index.md)（4 条）：源 Activity 只有 FEATURE_NO_TITLE、FLAG_FULLSCREEN 一类窗口写法或主题非全屏，UI 清单和派工却写「各页 needs_immersive_safearea=true」「无标题全屏」，或预写 setWindowSystemBarEnable([]) 隐藏全部系统栏
- [系统栏底色和深色适配的派工](bar-color/index.md)（2 条）：规格或台账要求状态栏底色、交付风险里有系统栏内容色未适配深色，派工限定只改配置文件、禁碰页面文件，或事项只留在交付风险里，没进 decision_gaps、负责切片的派工或账本
- [安全区避让值的派工、前向引用和交付结论](safe-area-avoid/index.md)（5 条）：源端子页经 Scaffold innerPadding 拿 inset、WindowModel 契约写明顶底两侧避让、避让值只取 TYPE_NAVIGATION_INDICATOR 一个值，派工写「statusBarHeight 本页不使用」、前向引用只登记一侧，或交付说明写「视觉不受影响」
