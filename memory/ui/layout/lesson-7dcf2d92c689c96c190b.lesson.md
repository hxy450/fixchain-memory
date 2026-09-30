# RelativeLayout 中没有相对规则的子 View 叠放在同一区域：用 Stack 或同一坐标定位，不改成 Column 顺序排列

ID：`lesson-7dcf2d92c689c96c190b` · 版本：1

[本主题](index.md)

## 何时使用

界面实现与视觉返修阶段，把 RelativeLayout 或 FrameLayout 内的多个子 View（如两条曲线、图层）翻译成 ArkUI 容器时

## 适用情境

源 item 在固定高度的 RelativeLayout 中放置多个子 View，它们没有 below/above/toEndOf 等相对规则，只有相同的 margin 或对齐，实际重叠绘制在同一区域；目标沿用了上一版的 Column 顺序结构。

## 例外与边界

- 子 View 之间写有 layout_below/above/toStartOf 等相对规则，此时按规则排布

## 原因

没有相对规则的 RelativeLayout 子项都相对父容器定位，会叠在一起；改成 Column 后每层各占一份高度，总高翻倍，所在列被拉长、底部内容被裁切。来源中视觉对齐会话读到两个 80dp 曲线同在一个 marginTop=123dp、高 80dp 的 RelativeLayout 里，仍把它们作为 Column 中的两个 80 高区块。

## 做法

1. 逐个检查子 View 是否有相对规则；没有的放进同一个 Stack，或用 position 定位到源端同一坐标。
2. 写完把各子区块高度相加，与源 item 的固定高度对照；超出就说明把叠放写成了顺序排列。

## 来源（按需复核）

- case-55bbad53c11b2d1b95e6 · 结论：diagnosis, recommendation:3
  卡片版本：`b23fae9cfd1d1656d9a5ecb824d2151dfc94d9f78a910b09f2d0b86cf9c6b07c`
