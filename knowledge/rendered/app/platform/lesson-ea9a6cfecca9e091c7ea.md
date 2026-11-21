# 源端 Activity 对自身 getWindow() 加的标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）随该 Activity 窗口失效；映射到应用共享的 UIAbility 主窗口时按页面可见性成对开关（onShown 开、onHidden 关）

## 何时使用

规格提取与页面实现阶段，把 Activity 的窗口标志映射为鸿蒙窗口 API 并写验收时

## 适用情境

源端某个 Activity 在 onCreate 给 getWindow() 加标志且没有清除代码，靠该 Activity 不可见或 finish 时随窗口失效；目标各页以 Navigation/NavDestination 共用一个主窗口，经 window.getLastWindow 调 setWindowKeepScreenOn 等窗口级 API。

## 原因

目标主窗口全应用共享，只在 aboutToAppear 打开、从不关闭时，离开该页后效果一直生效（来源中回到主菜单后仍持有常亮锁）；验收只测“进入后生效”时发现不了。

## 做法

1. 规格先写作用范围“该 Activity 可见期间”，映射写成成对开关：NavDestination onShown 设 true、onHidden 设 false（仍受源端读取的偏好约束）；不写“onCreate 时机设 true”。
2. 跨栈基线表的窗口级映射行注明“目标窗口全应用共享，须随页面可见性开关”；设备判据补离开页面一侧（返回主菜单后按系统超时熄屏，可用 hidumper 查本应用窗口锁已释放）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕安卓 FLAG_KEEP_SCREEN_ON 是窗口标志，含义是「只要这个窗口对用户可见，就保持屏幕常亮」；Activity 不可见或 finish 后效果随窗口失效，不需要清除代码。〔成立范围：对加在 Activity 自身窗口（getWindow()）上的标志；同一 Activity 内切换 Fragment 不改变窗口可见性，常亮一直生效；含义依据是 javadoc（常亮的实际判定在系统服务里，SDK 源码看不到）；最常见的不成立情形：代码显式 clearFlags 时提前失效。〕
- 〔做法第 1 步〕鸿蒙 Window.setWindowKeepScreenOn 设置的是该窗口位于前台时屏幕是否常亮，是窗口级属性，不随页面切换变化；文档要求只在导航、视频播放、绘画、游戏等必要场景设 true，退出场景后重置为 false，系统检测到不规范使用时可能恢复自动灭屏；异源虚拟屏下不生效。〔成立范围：对调用它的那个 Window 实例（窗口级设置，不区分窗口里显示的是哪一页）；最常见的不成立情形：窗口退到后台时不常亮（只在前台生效），回前台再生效。〕
- 〔适用情境〕window.getLastWindow(ctx) 返回当前应用内层级最高的子窗口；只有没有子窗口、或子窗口未调用 showWindow() 显示时才返回应用主窗口；自由窗口状态下独立子窗不在计算范围内。〔成立范围：对 window.getLastWindow（API 9 起）；最常见的不成立情形：页面显示期间应用另外显示了子窗口时，onShown / onHidden 里经 getLastWindow 设置的常亮或隐私模式落在子窗口上，主窗口没被设置或没被复位。〕
- 〔做法第 1 步〕NavDestination 的 onHidden 在被新页覆盖、出栈和应用切后台时都会触发，onShown 在显示、上层页出栈露出和应用回前台时触发；从 API 21 起，打开或关闭全模态（bindContentCover）也会让 NavDestination 触发 onHidden / onShown，回调参数为 VisibilityChangeReason.CONTENT_COVER。〔成立范围：对 NavDestination；API 21 之前文档没有写明全模态是否触发；被 NavDestinationMode.DIALOG 页覆盖或它出栈时，下层页不触发 onHidden / onShown（只触发 onInactive / onActive）；最常见的不成立情形：Navigation 首页内容不是 NavDestination，收不到这两个回调。〕
- 〔适用情境〕安卓 FLAG_SECURE 让窗口内容不出现在截屏中、不能在非安全显示器上显示；鸿蒙 Window.setWindowPrivacyMode(true) 让窗口内容无法被截屏或录屏，未调用时默认不开启，隐私模式窗口退后台后在多任务卡片中显示为白色蒙层或隐私蒙层；该接口需要 ohos.permission.PRIVACY_WINDOW，没有时抛 201。〔成立范围：对调用它的那个 Window 实例；PRIVACY_WINDOW 在 HarmonyOS 6.1.0（API 23）SDK 的权限定义里是 system_grant、normal，只需在 module.json5 声明；最常见的不成立情形：漏声明权限，调用失败、截屏不受限。〕
