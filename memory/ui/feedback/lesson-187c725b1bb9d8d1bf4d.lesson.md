# 源端单一 SnackbarHost 显示操作结果时，目标用唯一提示宿主按源端排队与时长展示

ID：`lesson-187c725b1bb9d8d1bf4d` · 版本：3

[本主题](index.md)

## 何时使用

页面转换与功能接线阶段，把源端 SnackbarHostState.showSnackbar 的操作结果提示落成 ArkUI 提示宿主、决定排队、替换与显示时长时

## 适用情境

源端页面只有一个 SnackbarHost(hostState)，多个操作结果先后调用 showSnackbar，可能带 actionLabel 或显式 duration；目标准备用多个条件渲染的底部浮层或单槽定时器实现提示。

## 原因

拆成多个互不排斥的浮层会叠在一起；单槽覆盖会丢掉 SnackbarHostState 中排队等待的结果；带动作的提示被按固定秒数自动关闭，动作来不及点。

## 做法

1. 用一个宿主管理当前提示，任何时刻最多一条：源端 showSnackbar 挂起排队时，后续提示入队，当前提示结束（超时、点动作或关闭）后再取下一条；源端调用方显式 dismiss 旧提示，或当前决策批准只保留最新结果时，才改为新提示替换旧提示。
2. 时长按源端调用推导：显式传 duration 时照用；未传时先看 import 的库——androidx.compose.material3 的 showSnackbar 无 actionLabel 默认 Short、有 actionLabel 默认 Indefinite（常驻到点动作、关闭或离页）；androidx.compose.material（M2）的 showSnackbar 未传 duration 一律 Short，带 actionLabel 也不常驻。
3. Short/Long 的毫秒数取所用库版本 SnackbarHost.kt 中 SnackbarDuration.toMillis 的定义（例：material3 1.4.0-alpha17 下 Short 为 4000ms），设备开启无障碍服务时 SnackbarHost 会按 AccessibilityManager.calculateRecommendedTimeoutMillis 延长显示；与评审口径不同时在迁移报告登记差异。

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, recommendation:4
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-2f11f734c53d33bee770](../../../store/cases/case-2f11f734c53d33bee770/df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15`
