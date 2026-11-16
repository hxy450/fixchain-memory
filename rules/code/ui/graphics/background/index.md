# 背景、渐变与描边

源端有 android:background 引用的 drawable（shape、layer-list、gradient、selector）、CardView 圆角、Compose Brush 渐变或 drawWithContent，目标端有 backgroundColor、backgroundImage、linearGradient、border、borderRadius 时

## 触发族

- [组件自身 Drawable 背景的预览层](drawable-background-preview/index.md)（3 条）：读到源端选中背景后改组件自身的背景 Drawable（setBackground）再 invalidate() 重绘；产物里在 Stack 底部另加背景层，上面仍叠着不透明的占位层或成品静态预览图，测试也没断言占位层 backgroundColor 跟着切换
- [背景和进度条引用的 drawable 层](layered-drawable/index.md)（4 条）：读到 android:background、android:progressDrawable 引用的 @drawable/ layer-list 或 @mipmap/ 位图层；产物里只剩 .backgroundColor(...)、没有出处的 .height(...)，或位图层只留了 FWD-REF 注释
- [android:background 引用的背景图和状态背景](background-drawable/index.md)（5 条）：读到 android:background="@drawable/…" 的位图（整屏背景、带透明边缘或装饰的图）或 style 带来的框架背景选择器；产物里 Image 用了 Cover 裁切、背景图下垫了品牌色、内容压到装饰、按钮只剩透明底加默认压暗
- [没写背景或背景为 @null 的控件](no-background/index.md)（5 条）：读到源控件和它的父容器没写 android:background，或写了 android:background="@null"；产物里对应组件多了 .backgroundColor(...)、.border(...)，或留着组件默认的 padding
- [Compose Brush 线性渐变（Brush.linearGradient / horizontalGradient）](compose-brush-gradient/index.md)（6 条）：读过的 Compose 源码里背景或描边用 Brush.horizontalGradient、Brush.linearGradient（带或不带 start / end、tileMode）；交回的换成了纯色或单色 .border，或 .linearGradient 的方向、色阶位置、repeating 是估的
- [android:background 引用的 shape drawable 与 CardView 圆角](shape-background/index.md)（9 条）：读过的布局里控件的 android:background 引用 @drawable/…（<shape> 的 <solid>、<corners>、<stroke>，或各布局变体不同），列表项或 holder 动态加入的视图根是 CardView 带 app:cardCornerRadius；交回的底色、圆角、描边是猜的或照抄兄弟页，shape 被当成 backgroundImage，border() 冲掉了圆角
- [drawable 里的 <gradient> 渐变（窗口背景、ImageView 着色）](gradient-drawable/index.md)（2 条）：读过的源码里主题的 windowBackground 或 ImageView 的 android:src 是带 <gradient android:startColor / endColor> 的 drawable，可能再用 app:tint 着色；交回的写成单色 backgroundColor、新加的单色颜色键，或用 Image(...).fillColor 给渐变 SVG 着色
- [按选择对象分图片、单色、渐变生成的背景](selection-background/index.md)（2 条）：读到的源方法按选择对象的 url、colors 数量、orientation 分支生成图片、ColorDrawable 或 GradientDrawable；交回的绑定或测试只覆盖 url 一支
- [同一视图上的圆角加描边](corner-and-stroke/index.md)（1 条）：读到同一视图同时带圆角和描边（MaterialButton 的 cornerRadius 加 strokeColor、CardView 的 cardCornerRadius 加描边、OutlinedBox）；交回的代码 .borderRadius 后跟不带 radius 的 .border
- [Compose 用 drawWithContent 写的自定义 Modifier 扩展](compose-draw-modifier/index.md)（2 条）：读到 Compose 组件调用 drawWithContent { drawContent(); drawRect(brush, blendMode = …) } 一类自定义 Modifier 扩展（渐变着色、渐变描边）；交回的代码改成单色 fillColor、兄弟节点单独混合，或描边宽度不是扩展里的默认值
- [主题 ripple 和 selector 提供的按压反馈](pressed-ripple/index.md)（5 条）：读到源控件的按压反馈来自主题的 ripple 或 selector（?attr/selectableItemBackground、listSelector → listChoiceBackgroundIndicator、actionBarItemBackground、colorControlHighlight / highlight_alpha_*）；产物里 .stateStyles({ pressed }) 的底色取值、整块平铺还是径向层或按半径画圆，以及有没有用 normal 写回静止值
- [Compose 的边缘渐隐（fadingEdges / fadingEdge）](compose-fading-edges/index.md)（4 条）：读到 Compose 内容上的 .fadingEdges(scrollState)、verticalGradient / Brush.horizontalGradient 做的 fadingEdge 修饰符（常配 horizontalScroll / verticalScroll、drawWithContent + BlendMode.DstIn）；产物里渐隐遮罩条的 linearGradient 方向和终点色、.mask 还是 blendMode(DST_IN) 覆盖层、遮罩上的 hitTestBehavior 和高度
