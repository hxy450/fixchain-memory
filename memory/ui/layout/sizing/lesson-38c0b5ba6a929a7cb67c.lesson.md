# 权重行里非权重兄弟要有确定尺寸：未设宽高的网络图片会挤掉 layoutWeight 列，拆槽时保留源端尺寸

ID：`lesson-38c0b5ba6a929a7cb67c` · 版本：2

[本主题](index.md)

## 何时使用

界面实现与槽位接线阶段，把调用方经 Modifier 传给子组件的尺寸、以及 Row{ Column.weight(1); 图片 } 一类权重布局转成 ArkUI 时

## 适用情境

源端图片尺寸由调用方 Modifier（如 Modifier.size(常量)）传给图片子组件；目标把该子组件拆成 @Builder 占位槽由后续接线者填入，被嵌组件本身没有尺寸参数；行内另一列用 layoutWeight(1)。

## 原因

网络 Image 不设尺寸时按图片固有像素测量，可能占满整行，权重列分到零宽，标题等内容不可见；尺寸原本写在调用方 Modifier 上，拆槽或重构时最容易丢，填槽者只看到组件签名。

## 做法

1. 拆 @Builder 占位槽时把源端调用处的宽高写在槽外层容器或槽调用处，并在占位注释写明尺寸；填槽者对照源端调用处的 Modifier.size，被嵌组件没有尺寸参数就在调用处补 width/height。
2. 写完权重布局，逐个检查非权重同级子项是否有确定尺寸。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bcc79fa7d3d15ef4a8b2](../../../../store/cases/case-bcc79fa7d3d15ef4a8b2/e30fc67a72656c26df78d1cef5d67b912bde2f8ee301b7b3fc3f9cff5843baba.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`e30fc67a72656c26df78d1cef5d67b912bde2f8ee301b7b3fc3f9cff5843baba`
