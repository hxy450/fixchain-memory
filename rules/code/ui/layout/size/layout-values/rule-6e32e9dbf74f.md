# 列表单元格按 RecyclerView item 布局逐项落尺寸和角标，不用自绘圆或文字色块替代

审的是：代码
触发（任一种）：
- 读到：`RecyclerView` 的 item 布局 XML 写了 `layout_height`、`layout_margin`、各 `TextView` 的 `android:textSize`，以及做今日、状态角标的 `ImageView`；写错的样子：目标单元格的高度、边距、字号与 item 布局不一致；选中或今日用 `Circle()` 自绘，状态角标用文字色块，没有对应的 `Image`
适用范围：界面实现阶段把 RecyclerView item 布局落成 ArkUI 列表或网格单元格时
做法：
- 逐项照搬 item 布局：layout_height 的 dp 数值 → .height(n)（vp）、layout_margin → .margin，textSize 的 sp 数值 → .fontSize(n)（fp）
- item 布局里用 ImageView 画的角标，目标端用 Image($r('app.media.…')) 放同一张图，不改成自绘圆形或文字色块
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- vp：屏幕密度相关像素，数值不带单位时默认 vp；fp：字体像素，随系统字体大小变化：dp 数值对应 vp，sp 数值对应 fp（出处：ts-pixel-units.md，基本像素单位）
针对本应用要查的：
- item 布局里引用的尺寸值：源工程 res/values 下的 dimens.xml，按 layout_height、layout_margin、textSize 引用的 @dimen 名字找；读出 dp / sp 数值，照数填进 height、margin、fontSize
来源：1 张卡，1 个应用
- case-5b1c11815476c648a9dc（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断
