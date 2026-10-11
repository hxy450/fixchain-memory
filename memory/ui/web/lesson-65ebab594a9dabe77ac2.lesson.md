# 源端靠 WebSettings 控制的排版在 ArkWeb 中显式落实，HTML 声明 viewport

ID：`lesson-65ebab594a9dabe77ac2` · 版本：1

[本主题](index.md)

## 何时使用

规格映射与 HTML 产出阶段，把 WebView 的 useWideViewPort、loadWithOverviewMode 等设置迁移到 ArkWeb 时

## 适用情境

源 WebView 通过设置按设备宽排版；目标 HTML 由独立服务产出，可能没有 viewport 声明。

## 原因

ArkWeb 无 viewport 时按桌面宽排版再整体缩小，正文字极小；规格笼统标“行为等价”时，这些设置不会传到 HTML 产出方。

## 做法

1. 规格逐项写出 WebSettings 与回调触发范围的差异；无一对一属性时给出替代，如 head 注入 width=device-width, initial-scale=1 的 viewport。
2. 每条 HTML 输出路径（含空文案兜底）都在 head 中声明 viewport。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-60d268b503cb75aa01a2](../../../store/cases/case-60d268b503cb75aa01a2/4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c`
