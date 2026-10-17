# Row 中位于定宽兄弟之后的 wrap_content 多行文字要加 flexShrink(1)（或 layoutWeight(1)）才会在剩余宽度内折行：Row 设了满宽，子项也默认不收缩

ID：`lesson-8566839cffc9e9e7fa30` · 版本：2 · 阶段：execute · 主题：[ui/layout/sizing](index.md)

概要：定宽兄弟后的多行 Text 加 flexShrink(1)

信号：`flexShrink(1)`, `layoutWeight(1)`, `layout-land`, `wrap_content`, `LinearLayout`, `width('100%')`

## 何时使用

界面实现阶段，把横向 LinearLayout 中位于固定尺寸兄弟之后的 wrap_content 文字转成 ArkUI Row 子项时

## 适用情境

源横向 LinearLayout（常见于 layout-land）中，固定 dp 的 ImageView 之后跟 wrap_content 宽、带左右 padding 的多行 TextView；文本长于剩余宽度时 Android 以 AT_MOST 取行内剩余宽折行。目标 Row 本身可能已设 width('100%')。

## 原因

ArkUI Row 的子项按自然宽度排布、默认不收缩，即使 Row 已限宽，长文本仍单行溢出被裁；竖屏 Column 能折行的结论不能代替横屏 Row。

## 做法

1. 给该 Text 加 .flexShrink(1)（或 layoutWeight(1)、显式剩余宽度），并按每个配置变体分别核对文字的主轴宽度约束；写后按最窄窗口与最长文案估算图片宽 + 边距 + 文字自然宽是否超出。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e4abf8f80dac25135b2e](../../../../../store/cases/case-e4abf8f80dac25135b2e/acc80a0833a62a53127d689cdb60aa0b50d731fac89421160491d624541b6ad4.json) · 结论：diagnosis, rec-18d89afde9, rec-9c79966011, rec-ca5444a314
  卡片版本：`acc80a0833a62a53127d689cdb60aa0b50d731fac89421160491d624541b6ad4`
