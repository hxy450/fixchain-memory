# 窗口避让区的取值和换算

agent 会看到什么：EntryAbility 或页面里用 getWindowAvoidArea / on('avoidAreaChange') 取避让高度（AvoidAreaType、topRect、bottomRect），写进共享模型或 AppStorage 前的 px2vp 换算、getUIContext 的时机和取窗口用的 API

## 规矩

- rule-49524dc97a2d｜TYPE_NAVIGATION_INDICATOR 避让取 bottomRect.height，不取 topRect｜读到：派工或参考写「getWindowAvoidArea(TYPE_SYSTEM / TYPE_NAVIGATION_INDICATOR) 测量写入」，没指定取哪个矩形；已有页面片段里两类避让都读 topRect.height；写错：getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR).topRect.height 被写进 bottomPadding（页面级或全局共享窗口模型），带导航指示条的设备上 bottomPadding 恒为 0
- rule-24c78d1a29f5｜避让区和窗口尺寸写进供 .padding 用的模型前先 px2vp，不把 px 原值当 vp｜读到：UIAbility 里 getWindowAvoidArea(...) 取到 avoidArea.topRect.height / bottomRect.height，或取窗口的 windowRect 宽高，要写进各页 .padding 消费的共享模型；写错：topRect / bottomRect 的原值直接写进共享模型，没有经过 px2vp；注释写成「consumed as vp」，或留着空的换算占位
- rule-20141ab0939b｜onWindowStageCreate 里依赖 UIContext 的步骤，放进 loadContent 成功回调里做｜读到：派工或沉浸式说明要求在 EntryAbility.onWindowStageCreate 里做全屏、系统栏设置，用 getWindowAvoidArea 测避让区换成 vp 写入窗口模型；写错：onWindowStageCreate 中位于 windowStage.loadContent(...) 之前、或在它的回调之外同步执行的代码（含被它同步调用的辅助函数）调用了 mainWindow.getUIContext()，再用它 px2vp 换算避让区或 setKeyboardAvoidMode
- rule-e288ad62e0f9｜页面订阅安全区时从主窗口取窗口对象，不用 window.getLastWindow｜读到：参考或 skill 示例里用 window.getLastWindow(getContext(this)) 设置系统栏属性；工程 EntryAbility 在 windowStage.getMainWindowSync() 得到的主窗口上 on('avoidAreaChange') / getWindowAvoidArea 测量安全区；写错：页面里用 window.getLastWindow(ctx) 取窗口，再在其上 on('avoidAreaChange') 或 getWindowAvoidArea 初始化顶部、底部避让高度
- rule-34f021542baf｜沉浸式底部避让取 TYPE_SYSTEM 与导航条底部高度的较大值，并监听 avoidAreaChange｜读到：源端按 isUsingGestures 区分手势 / 三键导航，规格写「两种导航模式下页面内容均不被导航栏遮挡」；写错：windowBottomPadding = 只取 TYPE_NAVIGATION_INDICATOR 的 bottomRect.height，三键导航时底部避让为 0
- rule-9ffd7ca84908｜源端 WindowInsets.navigationBars 的顶部分量迁成 0，不用窗口顶部安全区｜读到：源端内边距工具把 WindowInsets.navigationBars 的 calculateTopPadding() 加进顶部内边距；写错：目标把这一项写成窗口顶部避让值（如 windowTopPadding），使用它的页面顶部多算一份避让
- rule-a66b2afa8094｜窗口层重算顶部避让值时，除 windowSizeChange 外再挂 avoidAreaChange｜写错：EntryAbility 只挂 windowClass.on('windowSizeChange', …) 重算避让值（如 windowTopPadding），没有 on('avoidAreaChange', …)
