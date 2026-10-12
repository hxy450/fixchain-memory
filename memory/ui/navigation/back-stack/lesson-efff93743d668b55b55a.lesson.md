# 唯一页面被压在空的 Navigation 首页之上时由根页接管返回键：源端无返回处理就按 Activity 默认退到后台，不出栈露出空白首页

ID：`lesson-efff93743d668b55b55a` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与入口装配阶段，为单 Activity 应用确定根页面的返回语义、搭建 Navigation 入口壳并决定首页放在 Navigation 内容区还是首次 push 时

## 适用情境

安卓启动 Activity 未覆写 onBackPressed，也没有 OnBackPressedDispatcher、BackHandler 或 KEYCODE_BACK 处理（含 Compose NavHost 的起始目的地），返回键走 Activity 默认行为（Android 12+ 对任务根启动 Activity 把任务移到后台，onPause 存档、onResume 读档）；目标按 Navigation + NavDestination 模板，用内容为空的 Navigation 首页在启动时 pushPathByName 压入唯一页面，或启动页已生成为 NavDestination、入口只能首次 push。

## 原因

“空栈时返回退出应用”只对 Navigation 首页成立；唯一页面被压栈后栈深为 1，返回会把它弹出，露出空白首页，应用仍在前台。来源中转换者已推出“返回 = 退出应用”，却误判了栈深，后续切片也没有接返回处理。

## 做法

1. 在根 NavDestination 的 .onBackPressed 中按栈深判断：navPathStack.size() <= 1 时取 UIAbilityContext 调用 moveAbilityToBackground() 并 return true，消费返回、不出栈，存档交给 onBackground/onHidden；栈深大于 1 时不拦截。页面上的对话框打开时先由对话框消费返回。
2. 源端有返回处理时按源端逻辑实现；首屏不必是 NavDestination 时，也可把它作为 Navigation 根内容常驻、不压栈，空栈返回按系统默认处理。
3. 列出所有会把栈收成只剩根页的路径（冷启动首次 push、深链清栈重建、删除或克隆后清栈回根），确认它们都由同一个根页返回处理接管，不只覆盖冷启动。
4. 规格提取时，源端根页没有返回处理、依赖 Activity 默认行为，也要在导航规格写出“栈底返回 = 退到后台（或退出）”的可验收项，不因源码里没有对应代码而省略。

## 可选检查

- 冷启动后按一次返回：应用应退到桌面且进程与局面保留；出现空白页或应用仍在前台，说明返回链路漏接。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-16af2a52e0c933739747](../../../../store/cases/case-16af2a52e0c933739747/546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`546c9b748003d405ec9dbee50d90fd10ccfe93c2fefb64630e76e612cc263901`
- [case-e8db862eb02b52da96d0](../../../../store/cases/case-e8db862eb02b52da96d0/3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3981a32e0ac4329767da495cc56061acd812eecc47c60a18eae0098f1d58831b`
