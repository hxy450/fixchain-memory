# 页面级安全区订阅从承载页面的主窗口取窗口对象：复用工程主窗口入口或入口 Ability 已维护的避让状态，不用 window.getLastWindow

ID：`lesson-8e0e9fe5373a2bbe47af` · 版本：2

[本主题](index.md)

## 何时使用

界面实现或巡检修复阶段，为全屏页订阅 avoidAreaChange、调用 getWindowAvoidArea 取顶部与底部避让值并选择窗口对象时

## 适用情境

ArkUI 页面需自行订阅避让区或读取避让值；工程已在 EntryAbility 用主窗口测量安全区并写入共享状态，或有 getMainWindow()、windowStage.getMainWindowSync() 一类主窗口入口；运行时可能出现分享面板、调试浮窗等其他窗口；skill 示例为设置系统栏属性用了 window.getLastWindow(context)。

## 原因

getLastWindow 返回应用的顶层窗口，有子窗时就是子窗（@ohos.window.d.ts：没有子窗时才返回主窗口）；分享面板、调试浮窗等子窗的避让值可能与主窗口不同（已观察为 0），页面拿到 0 避让值，顶部按钮落进状态栏、点不到。

## 做法

1. 页面取避让值时优先复用 EntryAbility 已维护的避让状态；需要自行订阅时，用工程现有主窗口入口（如封装的 getMainWindow()，或 windowStage.getMainWindowSync()）取窗口，再 on('avoidAreaChange') 与 getWindowAvoidArea。
2. 注释或报告声称与入口 Ability 订阅同一窗口时，核对两处取窗口的 API 一致；为设置系统栏属性写的 getLastWindow 示例不用于读避让区。

## 可选检查

- 对避让值有疑问时，先打开分享面板或调试浮窗等额外窗口再进入页面，确认顶部按钮仍在状态栏下方且可点

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-dfc66c797f37eb94114f](../../../store/cases/case-dfc66c797f37eb94114f/9f98a79dac0d272fe6955fc32778afcddd33077fd3a0dd30a10ac3e6e45f4fd2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`9f98a79dac0d272fe6955fc32778afcddd33077fd3a0dd30a10ac3e6e45f4fd2`
