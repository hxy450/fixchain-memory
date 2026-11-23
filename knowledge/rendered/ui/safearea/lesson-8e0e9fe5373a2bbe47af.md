# 页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入口 Ability 已维护的避让状态，不用 window.getLastWindow

## 何时使用

界面实现或巡检修复阶段，为全屏页订阅 avoidAreaChange、调用 getWindowAvoidArea 取顶部与底部避让值并选择窗口对象时（前提：页面由主窗口承载，不是自建子窗口或悬浮窗）

## 适用情境

ArkUI 页面需自行订阅避让区或读取避让值；工程已在 EntryAbility 用主窗口测量安全区并写入共享状态，或有 getMainWindow()、windowStage.getMainWindowSync() 一类主窗口入口；运行时可能出现分享面板、调试浮窗等其他窗口；skill 示例为设置系统栏属性用了 window.getLastWindow(context)。前提是页面由主窗口承载；页面本身由应用自己创建的子窗口或悬浮窗加载（经该窗口的 setUIContent）时，避让区要从承载它的那个窗口取，不换成主窗口。

## 原因

getLastWindow 返回应用最近的窗口，不保证是承载页面的主窗口；全局悬浮窗、模态窗或系统窗口未调用 setSystemAvoidAreaEnabled 时取不到避让区（窗口接口文档 getWindowAvoidArea 一节有此说明）；子窗口与主窗口位置尺寸不一致时避让区为空这一条，现行窗口接口文档和声明文件都没有写，页面拿到 0 避让值，顶部按钮落进状态栏、点不到。来源中写者已收到“复用 EntryAbility 主窗口安全区”的巡检要求，注释也称“订阅与 EntryAbility 相同的窗口事件”，实际却用 getLastWindow；该写法在出现分享或调试子窗后暴露。

## 做法

1. 页面取避让值时优先复用 EntryAbility 已维护的避让状态；需要自行订阅时，用工程现有主窗口入口（如封装的 getMainWindow()，或 windowStage.getMainWindowSync()）取窗口，再 on('avoidAreaChange') 与 getWindowAvoidArea。
2. 注释或报告声称与入口 Ability 订阅同一窗口时，核对两处取窗口的 API 一致；为设置系统栏属性写的 getLastWindow 示例不用于读避让区。

## 可选检查

- 对避让值有疑问时，先打开分享面板或调试浮窗等额外窗口再进入页面，确认顶部按钮仍在状态栏下方且可点

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕window.getLastWindow 取当前应用最上层的窗口，只有没有子窗口时才返回应用主窗口；最上层窗口或主窗口为空或已销毁时以错误码 1300002 失败
- 〔做法第 1 步〕WindowStage.getMainWindowSync 同步取这个 WindowStage 的主窗口；窗口还未创建或已销毁时抛 1300002
- 〔原因 / 做法第 1 步〕getWindowAvoidArea 取当前窗口的避让区；全局悬浮窗、模态窗或系统窗口只有调用 setSystemAvoidAreaEnabled 使能后才能取到；返回值全为 0 表示避让区为空；文档列出的典型用法是在 onWindowStageCreate 中取应用启动时的初始避让区
- 〔做法第 1 步〕on('avoidAreaChange') 监听当前窗口系统避让区变化，全局悬浮窗、模态窗或系统窗口同样要先 setSystemAvoidAreaEnabled；常见触发场景是窗口在全屏、悬浮、分屏之间切换，窗口旋转，折叠状态变化
- 〔做法第 1 步〕AvoidAreaType.TYPE_SYSTEM 包含状态栏和三键导航栏区域（顶部避让取它的 topRect）；TYPE_NAVIGATION_INDICATOR 是底部导航区域
