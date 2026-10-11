# 唯一页面被压在空的 Navigation 首页之上时由根页接管返回键：源端无返回处理就按 Activity 默认退到后台，不出栈露出空白首页

ID：`lesson-efff93743d668b55b55a` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为单 Activity 应用搭建 Navigation 入口壳、决定根页面的返回键行为时

## 适用情境

安卓启动 Activity 未覆写 onBackPressed，也没有 OnBackPressedDispatcher 或 KEYCODE_BACK 处理，返回键走 Activity 默认行为（Android 12+ 对任务根启动 Activity 把任务移到后台，onPause 存档、onResume 读档）；目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面。

## 原因

“空栈时返回退出应用”只对 Navigation 首页成立；唯一页面被压栈后栈深为 1，返回会把它弹出，露出空白首页，应用仍在前台。来源中转换者已推出“返回 = 退出应用”，却误判了栈深，后续切片也没有接返回处理。

## 做法

1. 在根 NavDestination 的 .onBackPressed 中取 UIAbilityContext 调用 moveAbilityToBackground() 并 return true：消费返回、不出栈，存档交给 onBackground/onHidden；页面上的对话框打开时先由对话框消费返回。
2. 源端有返回处理时按源端逻辑实现；首屏不必是 NavDestination 时，也可把它作为 Navigation 根内容常驻、不压栈，空栈返回按系统默认处理。

## 可选检查

- 冷启动后按一次返回：应用应退到桌面且进程与局面保留；出现空白页或应用仍在前台，说明返回链路漏接。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e8db862eb02b52da96d0](../../../../store/cases/case-e8db862eb02b52da96d0/3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b`
