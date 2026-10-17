# TableLayout 列宽按内容测量：每列取各行（含 fake header）自然宽最大值，stretchColumns 再均分余量，不写等分或权重

ID：`lesson-6cb9ad45093ce2ca28af` · 版本：3 · 阶段：spec/execute · 主题：[ui/layout/intrinsic](index.md)

概要：TableLayout 列宽取各列自然宽最大值不等分

信号：`TableLayout`, `TableRow`, `stretchColumns`, `shrinkColumns`, `columnsTemplate`, `layoutWeight(1)`, `measureText`, `onAreaChange`, `layout_sources`, `paddingRight`

## 何时使用

规格提取与页面转换阶段，把 Android TableLayout 表格（滚动表体外另有固定表头，或带 stretchColumns/shrinkColumns）翻译为 ArkUI 列宽时

## 适用情境

源页面在 ScrollView 外放一行固定表头 TableRow，表体 TableLayout 首行是 height=0、文案与 paddingRight 同表头的 fake header 行（注释说明用于对齐外部表头列宽）；单元格是默认 wrap_content 的 TextView 逐行 addView，没有设定列宽；合成 view.xml 会丢掉 padding 与 height；规格可能写“fake header 删除（Grid 定宽列天然对齐）”并自拟 columnsTemplate 或权重。也包括 TableLayout 写 stretchColumns="*"、shrinkColumns="*"，单元格带左右 padding，写者准备解释成“两列等分”并写两个 layoutWeight(1) 或 50%。

## 原因

TableLayout 的列宽由该列所有行（含零高的 fake header）的自然宽决定，fake header 让表体列宽不小于外部表头，两者因此对齐；stretchColumns 只把剩余宽度在可拉伸列之间均分，列宽仍以自然宽为底。改成固定比例、权重或等分，列宽与内容脱钩，长内容折行或留出大片空白，表头与表体也不再对齐。

## 做法

1. 列宽契约写成：表体每列宽 = 该列 fake header（文字 + paddingRight）与全部单元格单行自然宽中的最大值；外部表头单元按 wrap_content 加 paddingRight 排布；实现按测量结果求各列最大宽后写入。
2. 写规格前打开 meta.json 列出的 layout_sources 原始 XML，核对 padding、height 等合成快照会丢的属性；原始 XML 与规格的近似决策冲突时以源布局为准，并在报告记录冲突。
3. 带 stretchColumns/shrinkColumns 时：先按各列最大自然宽（含单元格 padding）分配，剩余宽度均分给可拉伸列，总宽超出可用宽时才收缩 shrinkColumns 指定的列；用 measureText 或 onAreaChange 取得自然宽后计算列宽，不写成两个 layoutWeight(1) 或 50%。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [多字重字族逐文件 registerFont，入口只注册一次](../../theme/tokens/lesson-046baeb5ffbb10a6abc5.lesson.md)（共享 1 张卡）
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../../theme/sources/lesson-47785524c7f132ea7efe.lesson.md)（共享 1 张卡）
- [按源端实际色值与字号在资源中反查同值键，不按名选键](../../theme/tokens/lesson-4e9507a2a793c5583aa8.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [图标用源端原图，缺失从 drawable 密度目录复制不替代](../../graphics/icons/lesson-943544ce27bf04f9faf8.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-29fdf1fe3faadb5933b9](../../../../../store/cases/case-29fdf1fe3faadb5933b9/7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214.json) · 结论：diagnosis, rec-54d5c54f59, rec-35d099069b
  卡片版本：`7e89a2a29280e57f4b1930d3be3e5cf0ef1d7b50676e2d240862c6794865b214`
- [case-9cfde635e67a08373fe6](../../../../../store/cases/case-9cfde635e67a08373fe6/2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985.json) · 结论：rec-54ca61b050
  卡片版本：`2518eb32a760514e0502b0ebe77fc6cbe0a1431c7916a06f5aaf27ba9bf58985`
