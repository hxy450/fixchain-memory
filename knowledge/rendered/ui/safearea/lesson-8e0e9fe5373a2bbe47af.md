# 页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入口 Ability 已维护的避让状态，不用 window.getLastWindow

## 何时使用

界面实现或巡检修复阶段，为全屏页订阅 avoidAreaChange、调用 getWindowAvoidArea 取顶部与底部避让值并选择窗口对象时

## 适用情境

ArkUI 页面需自行订阅避让区或读取避让值；工程已在 EntryAbility 用主窗口测量安全区并写入共享状态，或有 getMainWindow()、windowStage.getMainWindowSync() 一类主窗口入口；运行时可能出现分享面板、调试浮窗等其他窗口；skill 示例为设置系统栏属性用了 window.getLastWindow(context)。

## 原因

getLastWindow 返回应用最近的窗口，不保证是承载页面的主窗口；子窗口与主窗口位置尺寸不一致时避让区为空，全局悬浮窗、模态窗未调用 setSystemAvoidAreaEnabled 时避让区恒为空（窗口接口文档 getWindowAvoidArea 一节有此说明，声明文件没有写子窗口这一条），页面拿到 0 避让值，顶部按钮落进状态栏、点不到。来源中写者已收到“复用 EntryAbility 主窗口安全区”的巡检要求，注释也称“订阅与 EntryAbility 相同的窗口事件”，实际却用 getLastWindow；该写法在出现分享或调试子窗后暴露。

## 做法

1. 页面取避让值时优先复用 EntryAbility 已维护的避让状态；需要自行订阅时，用工程现有主窗口入口（如封装的 getMainWindow()，或 windowStage.getMainWindowSync()）取窗口，再 on('avoidAreaChange') 与 getWindowAvoidArea。
2. 注释或报告声称与入口 Ability 订阅同一窗口时，核对两处取窗口的 API 一致；为设置系统栏属性写的 getLastWindow 示例不用于读避让区。

## 可选检查

- 对避让值有疑问时，先打开分享面板或调试浮窗等额外窗口再进入页面，确认顶部按钮仍在状态栏下方且可点

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕window.getLastWindow(ctx) 返回当前应用内层级最高的子窗口；只有没有子窗口、或子窗口还没调用 showWindow() 显示时，才返回应用主窗口。〔成立范围：对 Promise 与 callback 两种 getLastWindow 成立；自由窗口状态下独立子窗不在计算范围内（依据是文档说明）。最常见的不暴露情形：应用没有已显示的子窗口时返回的就是主窗口，所以问题只在出现子窗口后出现。〕
- 〔原因〕getWindowAvoidArea 和 on('avoidAreaChange') 对子窗口只有在子窗口位置和大小与主窗口一致时才返回计算后的避让区，否则返回空避让区；全局悬浮窗、模态窗和系统窗口要先调用 setSystemAvoidAreaEnabled 使能，否则恒为空；处于自由窗口状态的自由悬浮窗口模式下只有固定态软键盘（TYPE_KEYBOARD）一种避让区。〔成立范围：依据是文档说明（声明文件只写了系统窗口未使能时为空）。主窗口在非自由悬浮窗口模式下、或设备类型为 Phone、Tablet 时返回计算后的避让区；主窗口在非自由窗口状态的悬浮模式下只有 TYPE_SYSTEM 一种。〕
- 〔做法第 1 步〕AvoidArea 里 topRect、bottomRect 等 Rect 的 left、top、width、height 单位是 px；ArkUI 组件尺寸传 number 时按 vp 解释，直接把 height 当 padding 或高度用会放大一个像素密度倍数，要先换算成 vp。〔成立范围：对 getWindowAvoidArea 返回值与 avoidAreaChange 回调里的 AvoidArea 成立；px 单位依据是文档说明（Rect 的声明没写单位），声明文件另有 RectInVP（API 23）类型专门表示 vp 的矩形。不成立：用组件的安全区属性（如 expandSafeArea）交给框架处理避让时，不经过这个数值。〕
- 〔做法第 1 步〕避让区按类型分开取：文档的沉浸式示例取顶部高度用 TYPE_SYSTEM 的 topRect，取底部高度用 TYPE_NAVIGATION_INDICATOR 的 bottomRect；TYPE_NAVIGATION_INDICATOR 表示底部导航区域，三键导航显示时也始终存在。〔成立范围：对 getWindowAvoidArea 与 avoidAreaChange 成立；依据是文档说明和示例。不成立：只读 TYPE_SYSTEM 的 bottomRect 当底部值不可靠，OpenHarmony 文档写它含状态栏和三键导航栏，没有写手势导航条，手势导航下它的 bottomRect 取值文档没写。〕
- 〔做法第 2 步〕setWindowSystemBarProperties 对子窗口调用不生效，只设置主窗口的状态栏属性；getLastWindow 在有已显示子窗口时拿到的是子窗口，在它上面设置系统栏也不会生效。〔成立范围：依据是文档说明（setWindowSystemBarProperties 一节）。主窗口处于非全屏、非最大化或设备处于自由窗口状态时，主窗口上设置同样不生效。〕
