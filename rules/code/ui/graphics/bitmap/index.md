# 位图、图标与快照

源端有 ImageView / ImageButton 的 android:src、@drawable 位图、Compose Icons、当图标用的字符，或按内容总高导出长图，目标端有 Image 的宽高和 objectFit、SymbolGlyph、componentSnapshot 时

## 触发族

- [按内容总高导出的长图快照](long-snapshot/index.md)（2 条）：读到按内容总高 Bitmap.createBitmap 后整体 draw(canvas) 导出长图；产物里只做一次 componentSnapshot.createFromBuilder，或测自然高度的副本放在高度受限的容器里
- [没写固定尺寸的密度目录位图](bitmap-intrinsic-size/index.md)（6 条）：读到 ImageView / ImageButton 宽高是 wrap_content，或 TextView 的 drawableLeft / drawableStart 挂位图，图在 drawable-xhdpi 这类密度目录里；产物里 Image 没写宽高、写 16、32 之类经验值，照抄相邻控件或别页模板，或固定正方形再叠 padding
- [固定承载区里的图标按钮](icon-button-slot/index.md)（5 条）：读到工具栏、按钮的 ImageView / ImageButton 放在固定 android:layout_width 的承载区里，或写固定 dp 盒子加 android:scaleType="centerInside"；产物里槽位宽沿用旧值、图标尺寸和点击区写在同一个 Image 上、Image 设成盒子大小再 Contain，或照范式页逐字抄了宽高和 objectFit
- [源布局引用的 @drawable 位图资源](media-reference/index.md)（7 条）：读到源端 android:src、android:background、drawableStart、setImageResource 引用 @drawable/… 位图；产物里少了对应的 Image，换成名字不同的近似图标、SymbolGlyph($r('sys.symbol.…'))、Text('›') 字形或纯色，给替代图加 fillColor，或以 base/media 里没有为由判缺失
- [ImageView 的宽高比、夹紧和条目高](imageview-aspect/index.md)（3 条）：读到 wrap_content 的 ImageView 带或不带 android:adjustViewBounds、被父级或同行兄弟夹紧，或 GridView 条目高由 wrap_content + centerInside 的图撑出；产物里 Image 写固定宽高、按被夹紧的轴等比算另一轴，或 GridItem 写 aspectRatio(1) 做成方格
- [当图标用的字符和 SymbolGlyph 系统符号](symbol-glyph/index.md)（3 条）：读到源端 Text / TextView 里当图标用的字符（emoji、粗体的“-”“+”、'✓'），或派工要求把这类字符换成 SymbolGlyph；产物里写了 SymbolGlyph($r('sys.symbol.…'))，外形和原字符不同，或 .fontColor 沿用了单值
- [Compose 内置的 Icons 矢量图标](compose-material-icons/index.md)（2 条）：读到 Compose 里用 Icons.AutoMirrored.* 这类内置矢量图标（如 Icons.AutoMirrored.Rounded.ArrowBack）；产物里转成的 Image($r('app.media.…')) 有没有 .matchTextDirection(true)
- [BitmapFactory 的解码选项（inSampleSize、inJustDecodeBounds）](bitmapfactory-options/index.md)（1 条）：读到源端 BitmapFactory.Options 先 inJustDecodeBounds 取尺寸、再按 2 的幂设 inSampleSize 降采样解码；产物里 ImageSource.createPixelMap 的 DecodingOptions 写了 sampleSize 还是 desiredSize
- [位图的 tint 着色（android:tint、ColorFilter.tint）](bitmap-tint/index.md)（1 条）：读到 ImageView 的 android:tint / app:tint、代码里 setColorFilter(color)，或 Compose Image 的 colorFilter = ColorFilter.tint(...)，图源是 png / jpg / webp 位图；产物里 Image 上写的是 .fillColor(...) 还是 .colorFilter(drawing.ColorFilter…)
- [按素材固有比例定高的图片（ContentScale.FillWidth、无宽高约束的 img）](image-intrinsic-aspect/index.md)（2 条）：读到 Compose Image / AsyncImage 写 contentScale = ContentScale.FillWidth，或网页模板里没有 width、height 约束的 IonImg / <img>；产物里 Image 用 objectFit(ImageFit.Fill / Contain / Cover) 加 layoutWeight 或固定高代替按素材比例算高
- [按 EXIF 方向旋转的位图](exif-rotate-bitmap/index.md)（2 条）：读到源端 ExifInterface 按整数读 TAG_ORIENTATION（ORIENTATION_ROTATE_90 等）、经 Matrix.postRotate 旋转 Bitmap；产物里对 getImageProperty(image.PropertyKey.ORIENTATION) 的结果做 Number(...) / parseInt(...)，或手写像素平面旋转的下标公式
- [PixelMap 的所有者和释放](pixelmap-release/index.md)（2 条）：读到源端 Bitmap.recycle()、isRecycled、后处理后重新赋值的 bitmap、Bitmap.copy 后交给两处；产物里同一个 PixelMap 被入参、局部变量和调用方各自 release()，或画廊和 Canvas 覆盖层共用一个 PixelMap 没 cloneSync
- [图片加载库的占位图、错误图和淡入](image-loader-placeholder/index.md)（1 条）：读到 Coil 的 ImageLoader.Builder / ImageRequest.Builder、AsyncImage 上的 .placeholder(...)、.error(...)、.crossfade(true)；产物里 Image 的 .alt(...)、加载中的占位和 .contentTransition(...)
