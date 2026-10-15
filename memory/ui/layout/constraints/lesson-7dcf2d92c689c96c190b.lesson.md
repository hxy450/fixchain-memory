# RelativeLayout 中没有相对规则的子 View 叠放在同一区域：用 Stack 或同一坐标定位，不改成 Column 顺序排列

ID：`lesson-7dcf2d92c689c96c190b` · 版本：4

[本主题](index.md)

## 何时使用

界面实现与视觉返修阶段，把 RelativeLayout 内的多个子 View（如叠放的曲线、图层）翻译成 ArkUI 容器时

## 适用情境

源 item 在固定高度的 RelativeLayout 中放置多个子 View，它们没有 below/above/toEndOf 等相对规则，只有相同或各自的 margin 与对齐，实际重叠绘制在同一区域；目标沿用了 Column 顺序结构。

## 例外与边界

- 子 View 之间写有 layout_below/above/toStartOf 等相对规则，此时按规则排布

## 原因

没有相对规则的 RelativeLayout 子项都相对父容器定位，会叠在同一区域；改成 Column 后每层各占一份高度，总高增加，所在列被拉长、底部内容被裁切。

## 做法

1. 逐个检查子 View 是否有相对规则；没有的放进同一个 Stack，各自按源 margin 与对齐定位，或用 position 定位到源端同一坐标（坐标取当前子 View 的 layout_marginTop 等属性）。

## 可选检查

- 需要确认时，把各子区块高度与 margin 相加，与源 item 的 layout_height 对照；超出就说明把叠放写成了顺序排列。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-55bbad53c11b2d1b95e6](../../../../store/cases/case-55bbad53c11b2d1b95e6/0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7.json) · 结论：diagnosis, recommendation:3
  卡片版本：`0fc10fb1ff61028dc2a64bc1cea2a5a75c8437eb92967ddc5ada779fa4b263c7`
