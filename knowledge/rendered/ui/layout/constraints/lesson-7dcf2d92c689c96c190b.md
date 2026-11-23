# RelativeLayout 中没有相对规则的子 View 叠放在同一区域：用 Stack 或同一坐标定位，不改成 Column 顺序排列

## 何时使用

界面实现与视觉返修阶段，把 RelativeLayout 或 FrameLayout 内的多个子 View（如两条曲线、图层）翻译成 ArkUI 容器时

## 适用情境

源 item 在固定高度的 RelativeLayout 中放置多个子 View，它们没有 below/above/toEndOf 等相对规则，只有相同的 margin 或对齐，实际重叠绘制在同一区域；目标沿用了上一版的 Column 顺序结构。

## 例外与边界

- 子 View 之间写有 layout_below/above/toStartOf 等相对规则，此时按规则排布
- 改成 Stack 时要保留源端的贴边位置：RelativeLayout 中无规则的子项和 FrameLayout 中不写 layout_gravity 的子项都贴起始边和顶部，而 Stack 不写 alignContent 时子项居中，需写 alignContent: Alignment.TopStart 并保留各子项原有的 margin，或改用 position 给出同一坐标。

## 原因

没有相对规则的 RelativeLayout 子项都相对父容器定位，会叠在一起；改成 Column 后每层各占一份高度，总高翻倍，所在列被拉长、底部内容被裁切。来源中视觉对齐会话读到两个 80dp 曲线同在一个 marginTop=123dp、高 80dp 的 RelativeLayout 里，仍把它们作为 Column 中的两个 80 高区块。

## 做法

1. 逐个检查子 View 是否有相对规则；没有的放进同一个 Stack，或用 position 定位到源端同一坐标。
2. 写完把各子区块高度相加，与源 item 的固定高度对照；超出就说明把叠放写成了顺序排列。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕RelativeLayout 里横向、纵向都没有规则的子 View 按 positionAtEdge 放到起始边（LTR 为左、RTL 为右）和顶部，再按各自 margin 偏移，几个这样的子 View 叠在同一位置
- 〔做法第 1 步〕安卓 FrameLayout 的子项不写 layout_gravity 时按 DEFAULT_CHILD_GRAVITY（Gravity.TOP | Gravity.START）贴左上
- 〔做法第 1 步〕Stack 不写 alignContent 时子组件按 Alignment.Center 居中摆放，和 RelativeLayout、FrameLayout 默认贴左上不同
- 〔做法第 1 步〕position 是相对父组件内容区（父组件尺寸减去 border、padding）的绝对定位；父组件为 Row、Column 或 Flex 时，设了 position 的子组件不占位
- 〔做法第 1 步〕align 设的是组件绘制区域内内容的对齐方式（默认 Alignment.Center），对齐的是组件自身里面的内容
- 〔做法第 1 步〕Stack 中的子元素依次入栈，后一个子元素覆盖前一个子元素
- 〔做法第 1 步〕offset 相对组件原位置偏移，只在绘制时调整位置，布局仍按原位置占位
