# 转换滚动区时只把源滚动容器内的子节点放进 Scroll/List，固定头部留在外面；weight 剩余区里与列表叠放的空态放在有确定高度的区域内居中

## 何时使用

界面实现阶段，把 Android 页面转成 ArkUI 时确定固定区域与 Scroll/List 的包含范围，或借用相邻页面的页面骨架时；以及规格提取阶段书写滚动容器的转换决策时

## 适用情境

源布局根为纵向 LinearLayout 或 RelativeLayout，顶部用户栏、工具栏或横幅位于 NestedScrollView 之前（RelativeLayout 中滚动容器以 layout_below 排在其下），滚动容器承载地图、主按钮、卡片、宫格等主体；目标用 ArkUI Scroll 实现。 也包括源根为纵向 LinearLayout：固定高度标题栏与 layout_height=0dp、layout_weight=1 的列表容器同级，容器内 RecyclerView 与 match_parent、gravity=center 的空态 TextView 叠放、按数据显隐；同工程相邻页面按其自身源码采用整页单一 Scroll，可能被当作骨架照搬。

## 原因

固定头部进了 Scroll 就会随内容滚动；内容不足一屏时 Scroll 还会把整组内容纵向居中，头部被整体下推。视觉修复若只调 padding 偏移，会掩盖层级错误。来源中执行者写首页前的批量读取恰好截掉了源布局的头部与滚动容器开标签，没有补读就把头部与地图、按钮、统计卡一起放进 Scroll；规格只写了“NestedScrollView → Scroll + Column”，没写哪些区域固定；之后的视觉轮只改顶部偏移，直到用户两次反馈顶部栏太靠下才改层级。另一应用首页的横幅是 NestedScrollView 的兄弟、滚动区 layout_below 横幅，生成者读到该层级后仍用 Blank(200) 与横幅一起放进 Scroll，横幅随内容滚动，直到用户要求“火车订票是固定的”才移出。 Scroll 的内容在纵向无界，空态写 height('100%') 没有可解析的基准，源端空态在剩余区居中的语义随之丢失；第三个应用的规格已给出标题栏与 weight=1 列表区同级，生成者仍把标题、列表和空态一起包进单个 Scroll，生成前它读过的相邻页面正好是整页 Scroll。

## 做法

1. 转换前按源布局确认滚动容器开、闭标签之间包含哪些子节点；在它之前的兄弟（RelativeLayout 中被 layout_below 锚定的视图、与 weight 列表区同级的固定标题栏）放在 Scroll/List 外，滚动区用 layoutWeight(1) 或定位占剩余区域，只包裹原滚动区内容；不用 Blank 占位把固定区一起塞进 Scroll。
2. 源端 layout_height=0dp + layout_weight=1 的列表容器映射为 layoutWeight(1) 区域；与列表叠放的 match_parent、gravity=center 空态放在这个有确定高度的区域内（Stack 叠放，或按数据条件渲染并 justifyContent(Center)），不在 Scroll 内容里依赖 height('100%') 居中。
3. 借用相邻页面的骨架（如整页单一 Scroll）前，先核对本页规格的结构描述与属性表是否也是整页滚动。
4. 规格写滚动容器的转换决策时写明滚动范围：哪些区域固定、距顶多少，哪些随滚动；不只写组件映射。
5. 视觉校验发现顶部区块位置偏差时，先查它是否处在滚动容器内（内容不足一屏时最明显），层级错误就改层级，不用 padding 偏移补偿。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Scroll 只支持单个子组件；子组件的布局尺寸超过 Scroll 的尺寸时内容可以滚动，放进 Scroll 的节点都随内容滚动
- 〔做法第 1、2 步〕layoutWeight 只在 Row、Column、Flex 中生效，不写时为 0：父容器尺寸确定时，不设或为 0 的子组件先占位，设了大于 0 的子组件按权重分主轴剩余空间，分配时忽略自身 width/height 但保留 minWidth/minHeight 约束；容器里有子组件设了大于 0 的 layoutWeight 时，所有子组件不再按 flexShrink、flexGrow 布局
- 〔做法第 1 步〕Scroll 的高度超出屏幕显示范围时，可以通过 layoutWeight 让 Scroll 高度适应父容器主轴的剩余空间
