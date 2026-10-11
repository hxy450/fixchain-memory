# ImageView tint 着色的渐变装饰层用容器 linearGradient 实现

ID：`lesson-fcd86aeea6209ea0718b` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，迁移以 app:tint 主题色着色的白到透明渐变装饰层时

## 适用情境

源 ImageView 用 tint=?attr/colorBackground 一类主题色给渐变 shape 着色，目标准备改用 SVG 加 fillColor；目标有深色资源目录。

## 原因

fillColor 不会改写 SVG 的 url(#grad) 渐变填充，深色主题下留下亮带。

## 做法

1. 用容器 linearGradient 配主题色资源与对应透明变体（base/dark 各一份）。

## 可选检查

- 写完在深色主题下核对一次装饰层

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5b7b00a1deb25ed0b8d3](../../../store/cases/case-5b7b00a1deb25ed0b8d3/919bf87f71df8c5347bde16fb06fa3396a51d284ab648ce5d123265dfbf05b5e.json) · 结论：recommendation:3
  卡片版本：`919bf87f71df8c5347bde16fb06fa3396a51d284ab648ce5d123265dfbf05b5e`
