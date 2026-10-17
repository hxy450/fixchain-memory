# 整体着色的气泡用 bindPopup 的 popupColor，而不是只给内容加背景

ID：`lesson-05dc4eb9548bf3fef6ae` · 版本：2 · 阶段：execute · 主题：[ui/dialog/frame](index.md)

概要：气泡整体着色用 popupColor，不只给内容加背景

信号：`bindPopup`, `popupColor`, `backgroundBlurStyle`, `BlurStyle.NONE`, `setBackgroundColor`, `Balloon`, `Tooltip`

## 何时使用

界面实现阶段，把 Balloon、Tooltip 等带箭头的气泡迁移为 bindPopup 自定义 builder 时

## 适用情境

源 setBackgroundColor 作用于整个气泡（含箭头），目标的箭头与外框由 popup 容器绘制。

## 原因

只给 builder 内容加 backgroundColor 时，箭头与外框沿用默认的透明加模糊底色。

## 做法

1. 把源背景色映射到 popupColor，并设 backgroundBlurStyle: BlurStyle.NONE 与 radius。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [布尔组合条件逐字保留括号并列真值表](../../../process/lossy-transcription/lesson-381ebc5899e92cbd23a2.lesson.md)（共享 1 张卡）
- [占位只登记输入缺值的情况，能实现的当场实现](../../../process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-1907ba587e6b1439f17d](../../../../../store/cases/case-1907ba587e6b1439f17d/3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a.json) · 结论：rec-9df5d76294
  卡片版本：`3b9e23602906ed8c186b14784339e4463fbb6d15d4980a92ce92cd6be7aa805a`
