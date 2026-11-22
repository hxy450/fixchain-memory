# 源端 Activity 对自身 getWindow() 加的标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）随该 Activity 窗口失效；映射到应用共享的 UIAbility 主窗口时按页面可见性成对开关（onShown 开、onHidden 关）

## 何时使用

规格提取与页面实现阶段，把 Activity 的窗口标志映射为鸿蒙窗口 API 并写验收时

## 适用情境

源端某个 Activity 在 onCreate 给 getWindow() 加标志且没有清除代码，靠该 Activity 不可见或 finish 时随窗口失效；目标各页以 Navigation/NavDestination 共用一个主窗口，经 window.getLastWindow 调 setWindowKeepScreenOn 等窗口级 API。页面是 router 管理的 @Entry 页而不是 NavDestination 时，成对的时机换成该页的 onPageShow / onPageHide；该页面对应独立的窗口（单独的 UIAbility 主窗口或子窗口）时，窗口标志随那个窗口失效，不在本条范围内。

## 例外与边界

- 常亮只在该窗口位于前台时生效：整个应用退到后台时平台已不再保持常亮，不需要另在 onBackground 里关；本条要补的是同一窗口内离开该页面（返回、跳到别的页）这一侧。

## 原因

目标主窗口全应用共享，只在 aboutToAppear 打开、从不关闭时，离开该页后效果一直生效（来源中回到主菜单后仍持有常亮锁）；验收只测“进入后生效”时发现不了。

## 做法

1. 规格先写作用范围“该 Activity 可见期间”，映射写成成对开关：NavDestination onShown 设 true、onHidden 设 false（仍受源端读取的偏好约束）；不写“onCreate 时机设 true”。
2. 跨栈基线表的窗口级映射行注明“目标窗口全应用共享，须随页面可见性开关”；设备判据补离开页面一侧（返回主菜单后按系统超时熄屏，可用 hidumper 查本应用窗口锁已释放）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔标题 / 原因〕安卓 WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON 只在加了它的那个窗口对用户可见期间保持屏幕常亮
- 〔适用情境 / 原因〕window.getLastWindow 取当前应用最上层的窗口，没有子窗口时返回应用主窗口
- 〔原因 / 做法第 1 步〕Window.setWindowKeepScreenOn 设置的是该窗口位于前台时设备屏幕是否常亮，不随应用内页面切换自动撤销；文档要求退出导航、视频、游戏等场景后重置为 false，系统检测到不规范使用时可能恢复自动灭屏
- 〔做法第 1 步〕NavDestination 的 onShown 在该页面显示时触发，onHidden 在该页面隐藏时触发；API 21 起回调参数 VisibilityChangeReason 说明触发原因
- 〔原因 / 做法第 2 步〕卡里设备上页面只在 aboutToAppear 里对主窗口设常亮、离开时不传 false，返回上一页后应用仍持有常亮锁（windowLock），而源端的常亮已随该 Activity 不可见失效
