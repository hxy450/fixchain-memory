# TableLayout 表格转 ArkUI 时按内容测量列宽：每列宽取该列各行单元格自然宽的最大值，不自拟 fr 比例或权重

ID：`lesson-6cb9ad45093ce2ca28af` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与页面转换阶段，把 Android TableLayout/TableRow 表格（含与滚动区外固定表头对齐的写法）翻译为 ArkUI 列宽时

## 适用情境

源 TableLayout 的单元格为 wrap_content（XML 中声明或代码逐行 addView），未声明 stretchColumns/shrinkColumns/collapseColumns；可能在滚动表体外另有固定表头 TableRow，并在表体首行放一行与表头同文案、同 paddingRight 的对齐行（fake header）；规格可能写“删除对齐行，Grid 定宽列天然对齐”并自拟 columnsTemplate 或权重。

## 例外与边界

- 声明了 android:stretchColumns/shrinkColumns（或 setStretchAllColumns/setShrinkAllColumns）时，自然宽之外的剩余或不足空间按这些列分配；collapseColumns 指定的列不显示
- 单元格带 layout_span 跨列时，该单元不计入单列自然宽

## 原因

TableLayout 先让每个 TableRow 报告各列宽度，再按列取最大值作为列宽（TableLayout.java 中 maxWidths[j] = Math.max(maxWidths[j], widths[j])），列宽随内容变化；改成固定比例或权重，列宽与内容脱钩，长内容折行或留出大片空白。外部表头在另一容器里按自身 wrap_content 排，对齐行只让表体列宽不小于表头；表体内容更宽时源端本身也不对齐。

## 做法

1. 列宽契约写成：表体每列宽 = 该列全部行（含对齐行：文字 + 其 paddingRight）单行自然宽的最大值；外部表头单元按 wrap_content 加 paddingRight 排布。要让外部表头与表体始终等宽时，在报告中注明是有意改进。
2. 实现时用 this.getUIContext().getMeasureUtils().measureText({ textContent, fontSize, ... })（@ohos.arkui.UIContext.d.ts，API 12 起，返回 px，用 px2vp 换算）求各单元自然宽，加上单元左右 padding，按列取最大值写入列宽。
3. TableLayout 测量时会把 TableRow 的 layout_height 改回 WRAP_CONTENT（TableLayout.java），行上写的 height=0 不能单独让该行零高；对齐行在源端是否占高、是否可见，按其单元格自身的尺寸与可见性判断后再决定目标是否渲染。
4. 写规格前读源 res/layout 下的原始 XML，核对 padding、height 等合成快照可能丢的属性；原始 XML 与规格的近似决策冲突时以源布局为准，并在报告记录冲突。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-29fdf1fe3faadb5933b9](../../../../store/cases/case-29fdf1fe3faadb5933b9/7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214`
