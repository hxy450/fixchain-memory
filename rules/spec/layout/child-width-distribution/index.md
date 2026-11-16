# 源布局容器里子项的宽度分配（权重、表格列宽）

agent 会看到什么：读到源布局 LinearLayout 写了 android:weightSum 而子项 layout_weight 之和与它不等，或 TableLayout 的单元格是 wrap_content、表体首行另有对齐用的 fake header；规格只列各子项权重、自拟 columnsTemplate 比例列或 layoutWeight，没写权重合计、溢出项和按内容取最大值的列宽

## 规矩

- rule-0613bfc9fc3a｜规格写权重布局时同时写 weightSum 和子权重之和，标出溢出和份额为 0 的项｜读到：源布局 LinearLayout 写了 android:weightSum，和子项 android:layout_weight 之和不等；写错：规格只列各子项权重（如「weight 4 / weight 1 / weight 9」），没写 weightSum、子权重合计，也没写哪块溢出被裁、哪几项份额为 0
- rule-cdc686ba51cb｜TableLayout 带外部表头和对齐用的 fake header 时，规格写按内容取最大值的列宽契约｜读到：源布局 TableLayout 的单元格是 wrap_content 的 TextView（或 Java 里逐个 addView），外部固定表头 TableRow 之外，表体首行另有一行同文案、height=0dp、paddingRight 与表头相同的 fake header；写错：规格写「fake header 删除（Grid 定宽列天然对齐）」，自拟 columnsTemplate('2fr 1fr …') 或 layoutWeight 比例列；或列宽契约里没有 paddingRight
