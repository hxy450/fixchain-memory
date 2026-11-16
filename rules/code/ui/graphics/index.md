# 图片和图形

源端有 ImageView、@drawable 位图和 shape、自定义 View 的 onDraw / Canvas / Paint、elevation 阴影、模糊，目标端有 Image、Canvas、backgroundColor、linearGradient、border、shadow、blur 时

## 子主题

- [背景、渐变与描边](background/index.md)（48 条）：源端有 android:background 引用的 drawable（shape、layer-list、gradient、selector）、CardView 圆角、Compose Brush 渐变或 drawWithContent，目标端有 backgroundColor、backgroundImage、linearGradient、border、borderRadius 时
- [位图、图标与快照](bitmap/index.md)（37 条）：源端有 ImageView / ImageButton 的 android:src、@drawable 位图、Compose Icons、当图标用的字符，或按内容总高导出长图，目标端有 Image 的宽高和 objectFit、SymbolGlyph、componentSnapshot 时
- [自绘画布](canvas/index.md)（43 条）：源端有自定义 View 或 SurfaceView 的 onDraw、Paint、Canvas.drawText / drawBitmap、invalidate、Typeface，目标端有 Canvas、CanvasRenderingContext2D、fillText、drawImage、帧循环时

## 触发族

- [elevation 高程阴影](elevation-shadow/index.md)（4 条）：源端的 elevation 阴影（Modifier.shadow(elevation = …)、Surface 的 elevation、android:elevation 配 outlineProvider），对应目标组件上的 .shadow(ShadowOptions | ShadowStyle) 和共享的高程映射
- [背景图的模糊变换和 LightingColorFilter 压暗](blur-lighting-filter/index.md)（1 条）：读到源端加载背景图时做模糊变换（BlurTransformation），并 setColorFilter(new LightingColorFilter(mul, add)) 压暗；交回的背景 Image 没有 .blur，只用 Cover 加固定半透明遮罩近似
- [Compose Modifier.blur 的模糊](compose-blur/index.md)（2 条）：读到 Compose Modifier.blur(N.dp)（edgeTreatment 写没写）；产物里组件上的 .blur(…) 半径和外层 .clip
