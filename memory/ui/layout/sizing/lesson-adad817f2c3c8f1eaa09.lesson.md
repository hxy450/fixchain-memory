# LinearLayout 的 weightSum 与子权重和不等或 wrap_content 子项带权重时，按源码逐项分配余量（余量为负也照算），不归一化

ID：`lesson-adad817f2c3c8f1eaa09` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android LinearLayout 的 layout_weight/weightSum 分配翻译成 ArkUI 尺寸时；规格提取阶段写权重布局时

## 适用情境

源布局声明 weightSum 且与子权重之和不等（例：根 weightSum=10 而子权重 4/1/9；一列 weightSum=6 而 8 个 wrap_content 子项各权重 1），或 wrap_content 子项带权重、自然尺寸各不相同，子项自然尺寸之和可能超过可用尺寸（横屏、小屏）。

## 原因

ArkUI layoutWeight 按权重和的比例分配全部空间，等于忽略 weightSum 与子项自然尺寸。LinearLayout 先测各子项自然尺寸，再把余量按 share = (int)(w × 剩余余量 / 剩余 weightSum) 逐项分配并扣减（LinearLayout.java measureHorizontal/measureVertical）：权重累计恰好用完 weightSum 后余量与分母同为 0，后续子项只留自然尺寸；累计超过 weightSum 后余量与分母都为负，后续带权子项仍按公式得到份额。ImageView.onMeasure 对宽高分别 resolveSize，未设 adjustViewBounds 时盒子不会等比收缩，按“夹紧后等比缩小”求自然尺寸会把余量算错。归一化后源端被裁的末块、份额为 0 的子项与留白都会变形。

## 做法

1. 按源码算法逐项计算：余量 = 可用尺寸 − 各子项自然尺寸之和；按子项顺序 share = (int)(w × 剩余余量 / 剩余 weightSum)，每步从余量与 weightSum 中扣减；0dp 子项尺寸 = share，有自然尺寸的子项 = 自然尺寸 + share，结果按 Math.max(0, …) 夹紧；总和超出可用尺寸的末块按剩余空间裁切。算出位置后按容器实测尺寸绝对定位，或用占位补足 weightSum 余下的份额。
2. 带权重的 wrap_content ImageView 的自然尺寸按分轴测量取值：未设 adjustViewBounds 时，只有超出可用空间的那一轴被夹到父级上限，另一轴仍是密度缩放后的固有尺寸（盒子不等比收缩），把它代入 share 公式，不填经验值；写完抽 2–3 个位置（行中心、分隔线）与源端截图的 dp 对比。
3. 子项自然尺寸之和超过可用尺寸时余量为负，LinearLayout 按同一公式给每个带权子项分负份额、逐项扣减：显式算出各框尺寸，不交给 flexGrow/flexShrink 近似（flexGrow 只对应余量为正的情形）。
4. 规格写权重布局时同时写 weightSum 与子权重之和，以及溢出、份额为 0 的子项，不只列各子项权重。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4e7e0e12d7b6b08c08b0](../../../../store/cases/case-4e7e0e12d7b6b08c08b0/01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115`
- [case-85db2e28957bc67387d9](../../../../store/cases/case-85db2e28957bc67387d9/20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3`
