# LazyRow 摘要行转成可横滑容器，不降成普通 Row：少量固定项用 Scroll 包最小满宽的 Row 保留 Arrangement，item 内 AnimatedVisibility 的槽位恒在

ID：`lesson-caa043fb95ff63e321e2` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，把 Compose LazyRow（含只放几个固定 item 的摘要行、信息行）映射为 ArkUI 容器，确定是否可滚动、排列方式与条件项写法时

## 适用情境

源端用 LazyRow(horizontalArrangement = Arrangement.SpaceEvenly 等) 放少量固定 item，每个 item 恒在、显隐由 item 内部的 AnimatedVisibility 或条件控制；窄屏或大字号下内容可能超出行宽；映射表或规格可能把它写成“Row + 若干子项”。

## 例外与边界

- 源端是普通 Row（没有 LazyRow 或 horizontalScroll），超宽时按源端的裁切或压缩处理

## 原因

Lazy 容器本身可滚动，写成普通 Row 后超宽内容被裁切或挤压、无法横滑。Arrangement 只在内容不足一屏时分配空隙；item 内 AnimatedVisibility 隐藏后仍是零宽子项，照样参与 SpaceEvenly 的间隙计算，改成按条件增删子项，间隙数量与各项位置都会变化。

## 做法

1. 规格映射行写明：带方向的可滚动容器（Scroll 或横向 List）、排列方式，以及每个 item 是否恒在、显隐发生在 item 内部。
2. 少量固定项且要保留 Arrangement 时，用 Scroll().scrollable(ScrollDirection.Horizontal) 包 Row，Row 设 constraintSize({ minWidth: '100%' }) 与对应 justifyContent（如 FlexAlign.SpaceEvenly）：内容不足时铺满并分配空隙，超宽时可横滑；条目多或由数据驱动时用 listDirection(Axis.Horizontal) 的 List。交叉轴高度另按内容确定。
3. item 内 AnimatedVisibility 控制的内容：保留各 item 的槽位容器常在，只让槽内内容按条件出现（隐藏时槽位零宽），显隐过渡按源端动画另行实现。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7ced02d9c41ab6f4919a](../../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
