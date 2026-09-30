# 横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空

ID：`lesson-2d7c6de68f604ae77caf` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时

## 适用情境

源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。

## 原因

ArkUI 滚动容器的交叉轴不随内容收缩，横向不设高度时会撑满父级剩余高度；工程迁移陷阱表记有同一条，纵向缺宽度同理。来源的 Tab 行写了 .height('auto') 并注释为“自适应内容”，设备实测（API 12 模拟器）Scroll 仍被撑到约 597vp，行内选中格跟着放大，后几项被挤出视口。生成者没读到陷阱表里这一条，只凭另一个组件属性注释中的 auto 字样推断可用。

## 做法

1. 交叉轴高度取最高子项高度加上下内边距或外边距：单行文本项可按字号对应的单行高度加上下 padding 计算，已有设备测量值时以测量值为准。
2. 写完 grep 横向 Scroll/List/Grid 的链式属性，确认有数值 .height()；拿不准时列为设备必验项。

## 可选检查

- 对高度有疑问且能上设备时，用 dumpLayout 看滚动容器的高度是否与子项高度一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-2018daf21990f553ec22](../../../../store/cases/case-2018daf21990f553ec22/28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0.json) · 结论：diagnosis, recommendation:1
  卡片版本：`28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0`
