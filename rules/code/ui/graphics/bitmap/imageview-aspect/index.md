# ImageView 的宽高比、夹紧和条目高

agent 会看到什么：读到 wrap_content 的 ImageView 带或不带 android:adjustViewBounds、被父级或同行兄弟夹紧，或 GridView 条目高由 wrap_content + centerInside 的图撑出；产物里 Image 写固定宽高、按被夹紧的轴等比算另一轴，或 GridItem 写 aspectRatio(1) 做成方格

## 规矩

- rule-83d7b577870c｜ImageView 带 adjustViewBounds 时，Image 用 aspectRatio 跟随位图比例｜读到：ImageView 写了 wrap_content 和 android:adjustViewBounds="true"，可带 app:layout_constrainedWidth="true"、horizontal_bias，宽度受同行兄弟和边距约束；写错：Image 只写了 .layoutWeight(1).objectFit(ImageFit.Contain)，或写了固定的 .width().height()，没有 .aspectRatio(...)
- rule-84ce880ede11｜未设 adjustViewBounds 的 ImageView 一轴被夹紧时，另一轴仍取缩放后的固有尺寸｜读到：布局 XML 里 ImageView 的 layout_width / layout_height 为 wrap_content，没有 android:adjustViewBounds="true"，引用的位图只放在低于设备密度的 drawable-ldpi 这类目录，按密度放大后一轴超过父级；写错：目标里图片框的另一轴按被夹紧的轴等比算，如 .height(列宽 * 位图高 / 位图宽) 或写一个 RATIO 常量
- rule-585d0d3bf8f9｜GridView 条目高按内容量出时，GridItem 写固有高加 padding，不用 aspectRatio(1)｜读到：GridView 只有 numColumns 和 horizontalSpacing / verticalSpacing，没有固定行高；Adapter.getView 没有 setLayoutParams 固定条目高，条目里是 wrap_content + centerInside 的 ImageView，位图所在密度目录低于设备密度；写错：Grid 只写 columnsTemplate 和 columnsGap / rowsGap，GridItem 不设 height，条目根写 .width('100%').aspectRatio(1) 做成方格
