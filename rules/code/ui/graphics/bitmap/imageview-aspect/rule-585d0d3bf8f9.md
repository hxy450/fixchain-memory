# GridView 条目高按内容量出时，GridItem 写固有高加 padding，不用 aspectRatio(1)

审的是：代码
触发（任一种）：
- 读到：GridView 只有 numColumns 和 horizontalSpacing / verticalSpacing，没有固定行高；Adapter.getView 没有 setLayoutParams 固定条目高，条目里是 wrap_content + centerInside 的 ImageView，位图所在密度目录低于设备密度；写错的样子：Grid 只写 columnsTemplate 和 columnsGap / rowsGap，GridItem 不设 height，条目根写 .width('100%').aspectRatio(1) 做成方格
适用范围：把 GridView / ListView 的 Adapter 条目迁成 ArkUI Grid / List 项、条目高由内容决定（getView 未设固定高的 LayoutParams）时
做法：
- 格高 = wrap_content 图片按密度放大后的固有高 + 条目上下 padding（不随列宽等比收缩），写到 GridItem 的 .height('<格高>px')
- 条目内 Image 宽高铺满格子并 .objectFit(ImageFit.Contain)，去掉条目根的 .aspectRatio(1)；条目 padding 和行列间距按源端 px 截断值写成 'Npx'
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- GridView 量子项：宽 makeMeasureSpec(mColumnWidth, EXACTLY)，高 makeMeasureSpec(0, UNSPECIFIED)；getView 没设 LayoutParams 时默认 AbsListView.LayoutParams(MATCH_PARENT, WRAP_CONTENT, 0)：列宽定死，条目高按内容量出，wrap_content 图片只在宽这一轴被夹紧（出处：android.widget.GridView#setupChild；android.widget.AbsListView#generateDefaultLayoutParams）
- 位图固有高 = ((px × 设备 dpi) + (目录 dpi >> 1)) / 目录 dpi（整数除法）：BitmapDrawable 的固有高取 bitmap.getScaledHeight(mTargetDensity)，按这个式子放大（出处：android.graphics.Bitmap#scaleFromDensity；android.graphics.drawable.BitmapDrawable#computeBitmapSize）
- horizontalSpacing / verticalSpacing 用 getDimensionPixelOffset 读出：dp 间距乘密度后截断成整 px（出处：android.widget.GridView#GridView(Context, AttributeSet, int, int)）
- rowsGap(value: Length): GridAttribute，默认 0、单位 vp；Length 的字符串要写成 '10px' 才按 px，不写单位按 vp：源端算出的 px 值要带 px 后缀写（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.rowsGap；ts-types.md，Length）
- objectFit(value: ImageFit): ImageAttribute，默认 ImageFit.Cover：不写就按 Cover 裁切，要显式写 ImageFit.Contain（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.objectFit）
- objectFit(value: ImageFit): ImageSpanAttribute：同族接口：ImageSpan 的图片适配方式（出处：鸿蒙 SDK 的 ets/component/image_span.d.ts，ImageSpanAttribute.objectFit）
- objectFit(value: ImageFit): VideoAttribute：同族接口：Video 的画面适配方式（出处：鸿蒙 SDK 的 ets/component/video.d.ts，VideoAttribute.objectFit）
- GridItem.height 写按上式算出的 px 格高，间距写 trunc(dp × density) px，条目去掉 aspectRatio(1) 改为铺满格子后，格高、行距与安卓参照机一致：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 条目根有没有固定高、条目 padding 多少：源工程 Adapter 的 getView，按 setLayoutParams( 和 setPadding( 找；被注释掉的不算；有固定高就用它；没有就按内容量高，padding 是 px 原值
- 条目里图片的密度目录和像素尺寸：条目布局 XML 里 ImageView 的 android:src 和 layout_width / layout_height、scaleType；源工程 res/drawable-<密度>/ 下该图的像素宽高；目录 dpi 取 ldpi 120、mdpi 160、hdpi 240、xhdpi 320、xxhdpi 480、xxxhdpi 640，按上面的式子算固有高
- 目标设备的 dpi：运行时 @ohos.display 的 getDefaultDisplaySync().densityDPI；代入固有高式子算格高，再加上下 padding
未核实：解码时按密度缩放走的是原生代码，本机没有源码核对它和 scaleFromDensity 的取整是否完全一致
来源：1 张卡，1 个应用
- case-50d5978491b9ba48b899（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 8 ← 诊断
