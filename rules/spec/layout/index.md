# 布局与尺寸

读到源布局的 LinearLayout、ConstraintLayout、NestedScrollView、TableLayout、代码里循环 addView 搭的视图，或 Compose 的 Column、Modifier 链、自定义 Layout，规格里写容器映射、对齐、权重和尺寸时

## 触发族

- [Compose 修饰符链里的内距、背景和尺寸](compose-modifier-chain/index.md)（5 条）：读过的 Compose 源码里 Modifier 链上 padding / statusBarsPadding / navigationBarsPadding 与 background、heightIn、size 有先后，或 LazyRow 的 contentPadding、M3 IconButton 外层 .size(x)；交回的规格把这些平列，或把修饰符字面当实绘尺寸
- [Compose 自定义 Layout 在 constraints 上的 Int 整除](compose-layout-int-division/index.md)（2 条）：源端 Compose 自定义 Layout / MeasureScope 在 constraints.maxWidth、placeable 宽高上做 Int 整除或 .toInt() 截断，规格里把这条公式写成 vp 域、或只给整数宽的用例
- [排在固定高度兄弟之后的填满内容区](fill-remaining-content/index.md)（1 条）：读到 Compose Column 里排在搜索栏、分隔线之后、用 fillMaxSize 或 LazyColumn 占满的内容区；规格把它写成「全屏」「全屏居中」
- [源布局容器（NestedScrollView、LinearLayout）的滚动范围和默认对齐](container-scroll-align/index.md)（2 条）：读到源布局里顶部栏在 NestedScrollView 之前、滚动容器只包下方内容，或纵向 LinearLayout 没写 android:gravity、子项默认贴起始边；规格只写「NestedScrollView → Scroll + Column」「左上角」「左对齐」，没写哪些栏固定、Column 的 alignItems / alignSelf
- [源布局容器里子项的宽度分配（权重、表格列宽）](child-width-distribution/index.md)（2 条）：读到源布局 LinearLayout 写了 android:weightSum 而子项 layout_weight 之和与它不等，或 TableLayout 的单元格是 wrap_content、表体首行另有对齐用的 fake header；规格只列各子项权重、自拟 columnsTemplate 比例列或 layoutWeight，没写权重合计、溢出项和按内容取最大值的列宽
- [代码里循环 new 再 addView 搭出的视图](code-built-views/index.md)（2 条）：读到源码在循环里 new TextView 或自定义 View、逐个 addView 进容器（单个符号加大字号画的圆点指示器、只构造不刷新的一层格子）；规格写成「Html.fromHtml("&#8226;") → Text('•')」这类字符加字号的硬映射，或只按绘制方法写可见状态
- [ConstraintLayout 里四向锚 parent 的单视图和挂在它下面的兄弟](constraint-center-anchor/index.md)（1 条）：读到源布局 ConstraintLayout 里一个子视图 start/end/top/bottom 都锚定 parent，兄弟视图只有 constraintTop_toBottomOf 指向它、兄弟之间没有反向约束；规格把根布局写成「N 个子元素的垂直居中链」「ConstraintLayout（居中约束链）→ Column」
