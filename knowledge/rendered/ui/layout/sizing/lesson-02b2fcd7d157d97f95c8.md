# LinearLayout 以 gravity=center 摆放的 wrap_content 子项组转成 Row 时保留居中与按内容定宽，不给中间输入框 layoutWeight(1) 拉满

## 何时使用

界面实现阶段，把数量步进器（减号、数量框、加号）一类居中的 wrap_content 子项组翻译成 ArkUI Row 时

## 适用情境

源端 LinearLayout 设 gravity=center 与固定外边距，子项是 wrap_content 的按钮与 EditText；控件可能叠在带装饰的背景图（票券存根、竖虚线）上。

## 例外与边界

- 只针对源端子项都是 wrap_content 的情形；源端中间项本来就是 layout_width=0dp 加 layout_weight，或 match_parent 撑满时，目标给它 layoutWeight(1) 是对的，保留，不改成按内容定宽。

## 原因

给中间输入框 layoutWeight(1) 会把它拉满剩余宽度，两侧按钮被推到容器边缘，可能压住背景装饰；源端的居中与按内容定宽是需要同时保留的两条约束。来源中步进器把居中组改成拉伸，减号正好落在票券竖虚线上。

## 做法

1. Row 用 justifyContent(FlexAlign.Center)，子项按内容定宽（数量框按位数定宽），不给中间项 layoutWeight(1)。
2. 控件叠在装饰背景图上时，先确定装饰在图中的相对位置，再按比例留出安全区。

## 可选检查

- 在选中、未选中与最长数值状态下对照源端截图，确认没有压住装饰。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2 步〕padding 默认 0、单位 vp；设百分比时上下左右内边距都以父容器的 width 为基础值
- 〔适用情境〕安卓 LinearLayout 的 gravity 不写时为 Gravity.START | Gravity.TOP
- 〔做法第 1 步〕Row 的 justifyContent 不设时为 FlexAlign.Start；子组件不设 flexShrink 时默认不压缩，子组件主轴尺寸之和超过容器时，FlexAlign.Center、FlexAlign.End 的起始位置和 FlexAlign.Start 一致
- 〔做法第 1 步〕Row 的 alignItems 不设时为 VerticalAlign.Center
