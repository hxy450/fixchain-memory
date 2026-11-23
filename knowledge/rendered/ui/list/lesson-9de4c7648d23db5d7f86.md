# 多 viewType 列表按每类 holder 的根布局与运行时挂入的子视图定卡片外观：某一类专属的背景、圆角、描边不写进各类共用的 Builder

## 何时使用

界面实现阶段，为含普通项、推广项等多种 ViewHolder 的列表或网格确定卡片背景、描边与圆角，或参照兄弟页面的卡片实现时；规格准备阶段为列表页登记 item 布局时

## 适用情境

Android 列表同时有多类 holder：普通项的外观来自 holder 运行时 addView/inflate 的组件根视图（如 CardView 的 cardCornerRadius），推广项另有带圆角描边的背景 drawable；目标准备用一个共用 Builder 渲染各类卡片，或照搬兄弟页面已有的“白底 + 描边 + 圆角”卡片。

## 例外与边界

- 普通项外观来自 androidx 的 CardView 时，圆角之外还有两样默认行为要一起保留：API 21 起子视图按卡片圆角轮廓裁剪（目标端 borderRadius 要配 clip(true)，否则铺满卡片的图片会露出直角）；没另设 cardElevation 时卡片带 2dp 阴影。

## 原因

只看到一类 item 布局里的背景就套给所有分支，会把该类的圆角与描边带到其他项上；普通项真正的外观藏在 holder 动态加入的视图里，不打开它就拿不到圆角真值。兄弟页面的卡片 Builder 也是迁移产物，其数值不能当源端真值。

## 做法

1. 逐类核对 item 根布局和 holder 的绑定代码；holder 把动态视图放进内容容器时，继续打开该视图的布局取背景与圆角（如 cardCornerRadius 对应的 dimen 真值）。
2. 只属于某一类的背景 drawable 只用在该类分支；共用 Builder 按 holder 类型取外观参数，不写死一套。参照兄弟页面的卡片实现时只借结构，圆角、描边、底色逐项回到本页源码核对。
3. 规格准备阶段，列表页的布局清单（如 layout_sources、recycler_item_layouts）包含各类 item 布局及其动态 inflate 的预览布局，不只登记某一类。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 androidx.cardview:cardview 1.0.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕应用和主题没有另设 cardCornerRadius（也没改 cardViewStyle）时，CardView 取 Base.CardView 样式里的 cardview_default_radius，即 2dp（androidx.cardview 1.0.0）
- 〔做法第 2 步〕border() 里缺省 radius 时，写在它前面的 borderRadius 不保证生效，要把 borderRadius 写在 border 之后或把 radius 写进 border；border 的宽度、圆角默认都是 0
- 〔做法第 2 步〕borderRadius 默认 0，单位 vp，百分比按组件宽度计算；四个角里某个半径超过宽高较小值的一半时，按各值比例绘制异形圆角
- 〔做法第 2 步〕只设 borderRadius 不会裁剪子组件，子组件可以超出圆角；要配 clip(true) 子组件才按当前组件边缘轮廓（含圆角）裁剪
