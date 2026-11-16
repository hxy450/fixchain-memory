# 瀑布流迁成 WaterFlow 的列宽和间距

agent 会看到什么：读到 Compose LazyVerticalStaggeredGrid（StaggeredGridCells.Adaptive / Fixed、StaggeredGridItemSpan.FullLine）或 RecyclerView 配 StaggeredGridLayoutManager；产物里 WaterFlow 的 columnsTemplate、FlowItem 修饰链上有没有 .width('100%')、间距写在 padding 还是 margin

## 规矩

- rule-86219e3081d2｜多列 WaterFlow 的每个 FlowItem 都写 .width('100%')，再用 padding 表达间距｜读到：源端多列瀑布流：LazyVerticalStaggeredGrid(StaggeredGridCells.Adaptive(...) / Fixed(...))，或 RecyclerView 配 StaggeredGridLayoutManager；项上带 Modifier.padding(horizontal = ...)，头尾项用 StaggeredGridItemSpan.FullLine；写错：WaterFlow 的 columnsTemplate 在某个断点下是两列及以上，FlowItem() {...} 的修饰链里没有 .width('100%')（只有 .padding(...) / .margin(...)），里面卡片根节点写的是 .width('100%')
