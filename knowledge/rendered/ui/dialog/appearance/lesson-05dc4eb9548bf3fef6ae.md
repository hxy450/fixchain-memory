# 整体着色的气泡用 bindPopup 的 popupColor，而不是只给内容加背景

## 何时使用

界面实现阶段，把 Balloon、Tooltip 等带箭头、源端背景色作用于整个气泡（含箭头）的气泡迁移为 bindPopup 自定义 builder 时

## 适用情境

源 setBackgroundColor 作用于整个气泡（含箭头），目标的箭头与外框由 popup 容器绘制。

## 原因

只给 builder 内容加 backgroundColor 时，箭头与外框沿用默认的透明加模糊底色。

## 做法

1. 把源背景色映射到 popupColor，并设 backgroundBlurStyle: BlurStyle.NONE 与 radius。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕CustomPopupOptions 没写 popupColor 时气泡底色是透明加 COMPONENT_ULTRA_THICK 模糊；要去掉背景模糊需把 backgroundBlurStyle 设为 BlurStyle.NONE
- 〔原因 / 做法第 1 步〕CustomPopupOptions.backgroundBlurStyle 没写时取 BlurStyle.COMPONENT_ULTRA_THICK；BlurStyle.NONE 表示不模糊
- 〔做法第 1 步〕CustomPopupOptions.radius 没写时气泡圆角为 20vp
