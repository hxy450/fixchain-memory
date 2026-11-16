# 图片、形状与动画

读到布局里 @drawable 的 background / progressDrawable、容器背景加 ImageView 图标、Compose 的 Modifier.shadow / border、共享组件里的 shape，或 AnimatedImageVector、Animator 动画，规格里写图片资源、形状、阴影描边和动画时

## 触发族

- [容器背景加嵌套 ImageView 的元素](background-plus-icon/index.md)（1 条）：读到源布局里一个元素由容器的 android:background 位图加嵌套 ImageView 的 android:src 图标组成；规格的元素→资源表只列了背景图
- [共享组件定义里自带的形状和裁剪](shared-component-shape/index.md)（1 条）：页面源码调用项目自定义的共享 composable，形状和填充（Surface(shape = CircleShape)、ContentScale）写在组件定义里，规格只写尺寸、只在一处写形状，或决策表写成 Image 加容器 .clip
- [Compose 只绘制的修饰符（Modifier.shadow、Modifier.border）的映射](draw-only-modifiers/index.md)（2 条）：读到 Compose 修饰符链里的 Modifier.shadow(elevation: Dp)、Surface 的 elevation、Modifier.border(BorderStroke, shape) 这类只绘制的修饰符；规格的阴影配方把 dp 数直接填进 ShadowOptions，或描边落在没有宽高的 Stack 上、验收没有盒尺寸判据
- [布局里 @drawable 引用的控件外观（progressDrawable、background）](drawable-ref-appearance/index.md)（1 条）：读到布局 XML 里 ProgressBar 的 android:progressDrawable="@drawable/…" 或控件 android:background 引用 @drawable/…；规格里这个控件只写了边距和初值，没有高度、圆角、轨道色和渐变
- [源端动画（AnimatedImageVector 形变、多组 Animator 分支）](source-animations/index.md)（4 条）：读到 Compose 用 AnimatedImageVector.animatedVectorResource 加 rememberAnimatedVectorPainter(icon, atEnd) 做两态形变，或窗口类里定义多组 Animator、触摸回调里 cancel() 主动画改播另一个；规格写「图标态切换即可」，或行为笔记只记主时序、手势分支没有自己的时长
- [Coil 全局 ImageLoader 的图片管线](coil-image-loader/index.md)（1 条）：读到源码用 ImageLoaderFactory.newImageLoader 或 Coil.setImageLoader 建全局 ImageLoader.Builder（placeholder、error、crossfade，components 里只加了部分解码器、另有带 GIF 解码器的 loader 由设置位切换）；规格的图片管线 AC 只写 crossfade，或写「GIF 按帧动画播放，与 Android 一致」
- [Compose 用的 Material Icons 具名图标](compose-material-icons/index.md)（1 条）：读到 Compose 源里 Icon(imageVector = Icons.Outlined.* / Icons.Filled.* / Icons.AutoMirrored.*) 引用 material-icons 库的具名图标，res/drawable 里没有对应文件；规格的转换决策写「Icons.* → SymbolGlyph，按语义映射」「取最近的 symbol」，或给具名图标配了语义近似的 sys.symbol 名
- [位图上的着色（ColorFilter.tint、setColorFilter）](bitmap-tint/index.md)（1 条）：读到源端 ColorFilter.tint(color)、tint 或 setColorFilter 作用在 drawable 位图上，上游页规格写「.fillColor / .colorFilter」；规格的转换决策或验收条目只写「ColorFilter.tint → Image .fillColor」，没写资源格式和「fillColor 仅 SVG」的前提，或把两者列成任选项
