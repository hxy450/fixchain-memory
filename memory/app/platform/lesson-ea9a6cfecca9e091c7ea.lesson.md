# 源端 Activity 对自身 getWindow() 加的标志（FLAG_KEEP_SCREEN_ON、FLAG_SECURE 等）随该 Activity 窗口失效；映射到应用共享的 UIAbility 主窗口时按页面可见性成对开关（onShown 开、onHidden 关）

ID：`lesson-ea9a6cfecca9e091c7ea` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-42fb1284b2edc857b78b](../../../store/cases/case-42fb1284b2edc857b78b/1ec9ca3305bf0aaf2592d3df82c58adfa8db844dc2f0f12c41ad008281976b71.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`1ec9ca3305bf0aaf2592d3df82c58adfa8db844dc2f0f12c41ad008281976b71`
