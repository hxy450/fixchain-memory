# ImageView tint 着色的渐变装饰层用容器 linearGradient 实现

## 何时使用

界面实现阶段，迁移以 app:tint 主题色着色的白到透明渐变装饰层时

## 适用情境

源 ImageView 用 tint=?attr/colorBackground 一类主题色给渐变 shape 着色，目标准备改用 SVG 加 fillColor；目标有深色资源目录。

## 例外与边界

- “主题色到其透明变体”的渐变只对应默认着色模式 SRC_IN（结果是主题色乘以原图形的 alpha）；源端另设了 tintMode（如 multiply、screen）时，着色结果还取决于原图形的颜色，要按该模式另算色标

## 原因

fillColor 不会改写 SVG 的 url(#grad) 渐变填充，深色主题下留下亮带。

## 做法

1. 用容器 linearGradient 配主题色资源与对应透明变体（base/dark 各一份）。

## 可选检查

- 写完在深色主题下核对一次装饰层

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕Image 的 fillColor 只对 SVG 图片生效
- 〔原因〕深色主题下，fillColor 不改写 SVG 里 url(#grad) 的渐变填充，白到透明的渐变仍显示为白色亮带
- 〔做法第 1 步〕LinearGradientOptions.colors 每项是 [颜色, 位置]，位置取值 0–1；没写 angle 时为 180，没写 direction 时为 GradientDirection.Bottom（自上而下）
- 〔做法第 1 步〕资源里的八位十六进制颜色值前两位表示透明度，后六位表示颜色值
- 〔做法第 1 步〕颜色模式限定词为 dark 的资源目录在设备处于深色模式时优先匹配，找不到同名资源才回落 base 目录
