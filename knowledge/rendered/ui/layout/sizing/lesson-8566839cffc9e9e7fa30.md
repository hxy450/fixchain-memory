# Row 中位于定宽兄弟之后的 wrap_content 多行文字要加 flexShrink(1)（或 layoutWeight(1)）才会在剩余宽度内折行：Row 设了满宽，子项也默认不收缩

## 何时使用

界面实现阶段，把横向 LinearLayout 中位于固定尺寸兄弟之后的 wrap_content 文字转成 ArkUI Row 子项时

## 适用情境

源横向 LinearLayout（常见于 layout-land）中，固定 dp 的 ImageView 之后跟 wrap_content 宽、带左右 padding 的多行 TextView；文本长于剩余宽度时 Android 以 AT_MOST 取行内剩余宽折行。目标 Row 本身可能已设 width('100%')。

## 例外与边界

- flexShrink 只在 Row 设了主轴宽度（width 或 size）时生效；Row 没设宽度时按子项尺寸自适应、不会挤压文字，要先让 Row 取得确定宽度，单加 flexShrink(1) 不会折行。
- 源 TextView 是 wrap_content 宽：短文案时文字只占自然宽度。用 layoutWeight(1) 会忽略 Text 自身宽度、占满剩余空间，文字带背景、边框或 Row 设了主轴对齐方式时会改变短文案的显示，这类情况用 flexShrink(1) 保留自然宽度。

## 原因

ArkUI Row 的子项按自然宽度排布、默认不收缩，即使 Row 已限宽，长文本仍单行溢出被裁；竖屏 Column 能折行的结论不能代替横屏 Row。

## 做法

1. 给该 Text 加 .flexShrink(1)（或 layoutWeight(1)、显式剩余宽度），并按每个配置变体分别核对文字的主轴宽度约束；写后按最窄窗口与最长文案估算图片宽 + 边距 + 文字自然宽是否超出。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕应用没有另设 flexShrink 时，父容器是 Row、Column 的子组件默认值为 0（不收缩），父容器是 Flex 时默认值为 1；父容器是 Row、Column 时还要设了主轴尺寸（width/height/size）flexShrink 才生效，未设主轴尺寸时容器按子组件尺寸自适应；用 getInspectorByKey 读未设置 flexShrink 的节点会返回 1
- 〔做法第 1 步〕layoutWeight 默认 0；父容器尺寸确定时，没设或生效值为 0 的子组件先占位，生效值大于 0 的子组件从主轴剩余空间按权重分配尺寸，分配时忽略自身 width/height，但保留 minWidth/minHeight 约束；传小于 0 的值按 0 处理
- 〔适用情境〕横向 LinearLayout 在前面的子项都没有 weight 时，以已占宽度作为 usedWidth 测量后续子项；wrap_content 宽的子项得到 AT_MOST 测量规格，上限是父容器宽度减去已占宽度和内边距，所以长文字在这段剩余宽度内折行
