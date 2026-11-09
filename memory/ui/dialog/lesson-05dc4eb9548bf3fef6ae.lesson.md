# 整体着色的气泡用 bindPopup 的 popupColor，而不是只给内容加背景

ID：`lesson-05dc4eb9548bf3fef6ae` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Balloon、Tooltip 等带箭头的气泡迁移为 bindPopup 自定义 builder 时

## 适用情境

源 setBackgroundColor 作用于整个气泡（含箭头），目标的箭头与外框由 popup 容器绘制。

## 原因

只给 builder 内容加 backgroundColor 不会同时设置气泡容器的箭头与外框颜色。当前官方自定义 Popup 文档区分默认值：API 10 为 #4d4d4d，API 11 起为透明色加模糊填充；源气泡需整体纯色时应显式设置容器色与模糊样式，不把某一版默认外推到全部 SDK。

## 做法

1. 把源背景色映射到 popupColor，并设 backgroundBlurStyle: BlurStyle.NONE 与 radius。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1907ba587e6b1439f17d](../../../store/cases/case-1907ba587e6b1439f17d/3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a.json) · 结论：recommendation:2
  卡片版本：`3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a`
