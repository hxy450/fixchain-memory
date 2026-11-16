# 并排 wrap_content 图片列总宽接近屏宽时，按固有宽比例 layoutWeight 分列，不写固定 width

审的是：代码
触发（任一种）：
- 读到：match_parent 的水平 LinearLayout 里并排放 wrap_content 的子列或 ImageView，宽度由 drawable 固有尺寸加 android:layout_marginStart / layout_marginEnd 决定；写错的样子：各列写成 .width(<固有 dp 值>) 的固定宽度，图片也是固定 width，中间夹 Blank().layoutWeight(1) 对齐
适用范围：源端并排的 wrap_content 图片列，固有宽度与全部水平边距之和接近或超过手机屏宽时
做法：
- 先把各列固有 dp 宽与全部水平 margin 相加，和目标设备可用 vp 宽比较；接近或超出时不写固定 width，按固有宽度比例写 .layoutWeight(<列1固有宽>) / .layoutWeight(<列2固有宽>)，或用百分比分列
- 图片写 .width('100%').aspectRatio(<原图宽>/<原图高>)，高度随分得的宽度缩放；源端左右 margin 改成外层 .padding({ left: …, right: … })，列间 margin 改成 Row({ space: … })
- 不用 Blank().layoutWeight(1) 夹在固定宽度子项之间对齐；只把边距挪位置消除不了固定宽度造成的溢出
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- layoutWeight(value: number | string): T，默认 0：Row / Column / Flex 里按权重分主轴剩余空间，分配时忽略元素本身的尺寸设置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight；ts-universal-attributes-size.md，layoutWeight）
- aspectRatio(value: number): T：组件宽高比，传原图宽 / 高（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.aspectRatio）
- space?: string | number：Row 子项之间的间距，承接源端列间 margin（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowOptions.space；ts-container-row.md，RowOptions对象说明）
- DENSITY_XXHIGH = 480；DENSITY_DEFAULT = DENSITY_MEDIUM = 160：drawable-xxhdpi 的图按 480/160 = 3 倍折算：固有 dp = 像素 ÷ 3（出处：android.util.DisplayMetrics#DENSITY_XXHIGH、DENSITY_DEFAULT）
- Row({ space: <列间距> }) 内两列 .layoutWeight(<列1固有宽>) / .layoutWeight(<列2固有宽>)，图片 .width('100%').aspectRatio(<原图宽>/<原图高>)，外层左右 padding 承接源端边距：修好后的结构，真机上右列不再顶出屏幕（出处：卡里修好并验证过）
针对本应用要查的：
- 每张图的固有 dp 尺寸：源工程 res/drawable-<密度>/ 下的图片文件，读图片头里的像素宽高；像素 ÷ (该密度目录的 dpi / 160)，例：drawable-xxhdpi 除以 3；宽高比直接用像素宽 / 像素高
来源：1 张卡，1 个应用
- case-974fbf4f7e024029e673（android-train-ticket-vest7）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、建议 4；取值 5 ← 诊断
