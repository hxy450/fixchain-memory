# TableLayout 的列宽

agent 会看到什么：读到原始布局 XML 里 TableLayout 表头单元 wrap_content 带 android:paddingRight，另有 0dp 高、padding 相同的对齐 TableRow；产物里表格列写成 .layoutWeight 比例常量或 columnsTemplate 的 fr，对齐行被删掉

## 规矩

- rule-6bc07cb93e16｜TableLayout 列宽随内容时，代码按表头和单元格自然宽取最大值，不写比例权重｜读到：原始布局 XML 里 TableLayout 表头单元 wrap_content 带 android:paddingRight，另有 android:layout_height="0dp"、padding 相同的对齐 TableRow（注释写明对齐外部表头宽度）；写错：代码里表格列写成 .layoutWeight(…) 比例常量或 columnsTemplate('… fr …')，对齐行被删掉，报告援引规格的决策
- rule-ac7b8cafa11b｜TableLayout 的 stretchColumns/shrinkColumns 不是等分，按自然宽加均分余量算列宽｜读到：源布局 `TableLayout` 带 `android:stretchColumns="*"` / `android:shrinkColumns="*"`，单元格有 paddingStart / paddingEnd；写错：目标每行用两个 `.layoutWeight(1)` 或 `.width('50%')` 等分列宽
