# 滚动容器之外的顶栏和标题栏

agent 会看到什么：读到纵向 LinearLayout 里写在 ScrollView / NestedScrollView 或列表容器之前的顶栏、标题栏；产物里这些栏进了 Scroll 的内容 Column

## 规矩

- rule-a2a17d3a6890｜固定高度标题栏与滚动列表同级时，标题栏放在 Scroll 外的外层 Column 里｜读到：纵向 LinearLayout 下固定高度的标题栏（FrameLayout / Toolbar）与装 RecyclerView 或 ScrollView 的容器同级；规格写「标题栏 + 剩余空间列表」；写错：页面写成 Scroll() { Column() { 标题栏 @Builder … 列表或空态 } }，标题栏进了滚动内容，随列表一起滚走
