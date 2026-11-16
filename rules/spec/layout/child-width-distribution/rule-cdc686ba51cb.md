# TableLayout 带外部表头和对齐用的 fake header 时，规格写按内容取最大值的列宽契约

审的是：规格
触发（任一种）：
- 读到：源布局 TableLayout 的单元格是 wrap_content 的 TextView（或 Java 里逐个 addView），外部固定表头 TableRow 之外，表体首行另有一行同文案、height=0dp、paddingRight 与表头相同的 fake header；写错的样子：规格写「fake header 删除（Grid 定宽列天然对齐）」，自拟 columnsTemplate('2fr 1fr …') 或 layoutWeight 比例列；或列宽契约里没有 paddingRight
适用范围：规格里写 TableLayout 表格列宽的那一节，源端没有给任何列设定固定宽度、靠 fake header 对齐外部表头时
做法：
- 列宽契约写成：表体每列宽 = max(该列 fake header 的文字宽 + paddingRight, 该列全部单元格的单行自然宽)；外部表头单元按 wrap_content 加 paddingRight 排布；不写 fr 比例或权重
- 各表头单元的 paddingRight、对齐行的 height=0dp 从原始布局 XML 读出写进契约（合成的视图树会丢 padding、height 这类属性）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- // find the maximum width for each column … maxWidths[j] = Math.max(maxWidths[j], widths[j]);：TableLayout 每列宽取该列所有行单元格测量宽的最大值（出处：android.widget.TableLayout#findLargestCells）
针对本应用要查的：
- 各列表头单元的 paddingRight 和对齐行的写法：源工程 res/layout/ 下这个页面的原始布局 XML，外部表头 TableRow 和 TableLayout 首行 TableRow 的各 TextView；读 android:paddingRight（dp）和 android:layout_height；对齐行常带说明用途的注释
来源：1 张卡，1 个应用
- case-29fdf1fe3faadb5933b9（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
