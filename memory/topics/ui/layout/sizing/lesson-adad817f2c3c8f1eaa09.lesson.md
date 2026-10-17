# LinearLayout 的 weightSum 与子权重之和不等，或 wrap_content 子项带权重时，不用 layoutWeight 归一化：余量（可用尺寸减各子项自然尺寸）按 w/剩余 weightSum 依次分配，份额耗尽的子项只留自然尺寸，超出 weightSum 的末块被裁

ID：`lesson-adad817f2c3c8f1eaa09` · 版本：3 · 阶段：spec/execute · 主题：[ui/layout/sizing](index.md)

概要：weightSum 与权重和不等时按源算法分余量

信号：`weightSum`, `layout_weight`, `layoutWeight`, `flexGrow`, `flexShrink`, `adjustViewBounds`, `measureVertical`, `LinearLayout`

## 何时使用

界面实现阶段，把 Android LinearLayout 的 layout_weight/weightSum 分配翻译成 ArkUI 尺寸时；规格提取阶段写权重布局时

## 适用情境

源布局声明 weightSum 且与子权重之和不等（如根 weightSum=10 而子权重 4/1/9，列 weightSum=6 而 8 个 wrap_content 子项各权重 1），或 wrap_content 子项带权重、自然尺寸各不相同。 也包括带权重的 wrap_content ImageView 未设 adjustViewBounds、位图按密度放大后宽于父级，各子项自然尺寸之和可能超过可用尺寸（横屏、小屏）。

## 原因

ArkUI layoutWeight 按权重和的比例分配全部空间，等于忽略 weightSum 与子项自然尺寸：源端被裁的末块、份额耗尽的子项与留白都会变形。 flexGrow 只在余量为正时按比例增长：自然尺寸之和超过可用尺寸时，LinearLayout 用同一公式给每个带权子项分负份额、逐项扣减，flexGrow/flexShrink 复现不了；自然尺寸取错（如把未设 adjustViewBounds 的图片高按父宽等比缩小），分出的各框尺寸也跟着错。

## 做法

1. 按 LinearLayout 算法计算：先测各子项自然尺寸，余量按权重依次分配（每次除以剩余 weightSum），weightSum 用尽后的子项只保留自然尺寸，总和超出可用尺寸的末块按剩余空间裁切；可按容器实测尺寸算出位置后绝对定位，或用占位补足 weightSum 余下的份额。 份额逐项计算为 share = (int)(w × 剩余余量 / 剩余 weightSum)（本机 android-36.1 源码 LinearLayout.java 的 measureVertical/measureHorizontal），余量为负时同一公式给出负份额、逐项扣减；不交给 flexGrow/flexShrink，显式算出各子项尺寸。
2. 带权重的 wrap_content 图片固有尺寸超过行能给的空间时，只把超限的那一轴夹紧到父级上限；ImageView 未设 adjustViewBounds 时另一轴保持密度缩放后的固有尺寸（位图在盒内 centerInside/FIT_CENTER 缩小绘制，盒子不等比缩小），以此作为自然尺寸代入余量分配，不填经验值；写完抽 2–3 个位置（行中心、分隔线）与源端截图的 dp 对比。
3. 规格写权重布局时同时写 weightSum 与子权重之和，以及溢出、份额为 0 的子项，不只列各子项权重。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [图标按资源固有 dp 显示，触摸盒放外层不设成盒尺寸](../../graphics/icons/lesson-bdc493f5950835f9bfcc.lesson.md)（共享 2 张卡）
- [fragment 根 padding 只由宿主或组件一方实现](lesson-8a7d25959b954ffb9215.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4e7e0e12d7b6b08c08b0](../../../../../store/cases/case-4e7e0e12d7b6b08c08b0/01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115.json) · 结论：diagnosis, rec-edbb30e710, rec-ceec5167fe, rec-357705e373
  卡片版本：`01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115`
- [case-85db2e28957bc67387d9](../../../../../store/cases/case-85db2e28957bc67387d9/20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3.json) · 结论：diagnosis, rec-fbf9416ed8, rec-c06ce6b931
  卡片版本：`20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3`
