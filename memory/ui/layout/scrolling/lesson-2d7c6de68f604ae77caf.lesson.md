# 横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空

ID：`lesson-2d7c6de68f604ae77caf` · 版本：5

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时

## 适用情境

源端横向滚动行（Compose LazyRow、horizontalScroll、可滚动 Tab 行）的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。

## 例外与边界

- 横向滚动容器放在已定高的父槽位里（父级给出确定高度）时，交叉轴随父级即可

## 原因

在已观察的工具链中（target SDK 5.0.0(12) 工程的设备实测），ArkUI 滚动容器的交叉轴不随内容收缩：横向 Scroll/List 不设高度会撑满父级剩余高度，写 height('auto') 也不收缩；行内选中格等百分比子层随之放大，后续项被挤出视口。

## 做法

1. 交叉轴高度取最高子项高度加上下内边距或外边距：单行文本项按字号对应的单行行高加上下 padding 计算（字号与 padding 取当前源样式），已有设备测量值时以测量值为准；把算出的数值写到横向滚动容器的 .height(...)，不以 'auto' 代替。

## 可选检查

- 仅当高度仍有疑问或出现被撑高时，核对当前滚动容器的高度声明与子项尺寸；能上设备时复用dumpLayout核对二者是否一致。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-2018daf21990f553ec22](../../../../store/cases/case-2018daf21990f553ec22/28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`28ef980edd82e29589d8923bf1fff263161ff6975ab9fe8a33e7149e781419c0`
