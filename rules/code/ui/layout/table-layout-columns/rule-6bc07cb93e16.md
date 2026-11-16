# TableLayout 列宽随内容时，代码按表头和单元格自然宽取最大值，不写比例权重

审的是：代码
触发（任一种）：
- 读到：原始布局 XML 里 TableLayout 表头单元 wrap_content 带 android:paddingRight，另有 android:layout_height="0dp"、padding 相同的对齐 TableRow（注释写明对齐外部表头宽度）；写错的样子：代码里表格列写成 .layoutWeight(…) 比例常量或 columnsTemplate('… fr …')，对齐行被删掉，报告援引规格的决策
适用范围：把源端没有固定列宽、靠 fake header 对齐外部表头的 TableLayout 迁成 ArkUI 表格时
做法：
- 外部表头每个单元按内容宽排布，加上源 paddingRight（源 dp 数值写成 vp 的右内边距）
- 表体每列写显式 .width(该列宽)，列宽 = max(fake header 该列文字宽 + paddingRight, 该列全部单元格单行自然宽)
- 源布局的 paddingRight、height=0 对齐行与规格里的比例决策冲突时，按源布局写，并在转换报告里记下这处冲突
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- maxWidths[j] = Math.max(maxWidths[j], widths[j]);：源端每列宽是该列所有行单元格测量宽的最大值（出处：android.widget.TableLayout#findLargestCells）
针对本应用要查的：
- 各列表头单元的 paddingRight：源工程 res/layout/ 下这个页面的原始布局 XML，外部表头 TableRow 里的各 TextView；读 android:paddingRight 的 dp 数值，写成同数值的 vp
未核实：卡里记的鸿蒙 SDK 是 6.1.1(24)，本机核实用的是 API 23；本条未用到鸿蒙接口的具体签名
来源：1 张卡，1 个应用
- case-29fdf1fe3faadb5933b9（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2
