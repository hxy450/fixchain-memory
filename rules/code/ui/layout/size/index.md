# 宽高与边距

源端有 layout_width / layout_height、match_parent、wrap_content、layout_margin*、padding*、dp 尺寸，或 Compose 的 padding、size、fillMaxSize、heightIn 修饰，目标端有 .width、.height、.margin、.padding、constraintSize 时

## 触发族

- [随内容高的父容器里的 height('100%')](wrap-parent-full-height/index.md)（3 条）：读到 NestedScrollView、wrap_content 的槽位或弹层根、被嵌入的 Fragment 布局根里按内容取高的子树；产物里 Scroll、bindSheet 内容或子组件 build() 根和各状态分支上的 .height('100%')、依赖父高的 .layoutWeight
- [wrap_content 行里 match_parent 高的子项](row-match-parent-height/index.md)（2 条）：读到 wrap_content 高的行容器（列表项、弹窗按钮行）里 android:layout_height="match_parent" 的子控件或竖分隔线；产物里这个子项的 .height('100%')、.alignSelf(ItemAlign.Stretch) 和 Row 的高度
- [match_parent 子项转成 '100%' 的写法](match-parent-percent/index.md)（4 条）：读到列表项、网格项或 FrameLayout 叠层里 layout_width / layout_height="match_parent" 的子项，常带同轴的 android:layout_margin；产物里 .width('100%') / .height('100%') 漏写，或和同轴的 .margin 叠写
- [按钮和图片的显式宽高](explicit-size/index.md)（2 条）：读到按钮或 ImageView 的 android:layout_width / layout_height（固定 dp、@dimen 或 48dp 加 android:padding）；产物里 Image / Button 链上的 .width / .height 数值、padding 是否另加、有没有第二组异常大的尺寸
- [布局 XML 上的外边距、内边距和尺寸](margin-padding/index.md)（12 条）：读到布局 XML 元素（含容器自身）上的 android:layout_margin*、android:padding*、match_parent 加 margin、带 padding 的 ImageView、锚在兄弟控件上方的 marginBottom；产物里对应组件修饰链上的 .margin / .padding / .width / .height 漏写、数值不同、叠成两份或没扣边距
- [源布局写定的尺寸、字号和颜色](layout-values/index.md)（10 条）：读到源布局（含 <include> 的布局、RecyclerView 的 item 布局）里控件的 layout_height、margin、padding、textSize、textColor、background 或 @dimen/、@color/ 引用，交回的代码给组件写了 .height、.margin、.fontSize、.fontColor 等常数，或视觉修复改了这些数
- [Compose 的 fillMaxSize、heightIn、matchContentSize 尺寸修饰](compose-size-modifier/index.md)（5 条）：读过的 Compose 源码里节点用 Modifier.fillMaxSize() 占剩余高度、heightIn(max) 紧接 verticalScroll、matchContentSize 让描边贴合内容；交回的写成 height('100%')、另加 100% 覆盖层，或 constraintSize 挂在了外层 Column 上
- [Compose 未定尺寸的 Surface / Box 的尺寸与描边](compose-box-size/index.md)（2 条）：读过的 Compose 源码里 Surface / Box 只加 clickable、clip、border、background，有没有 Modifier.size 决定它的尺寸；交回的按钮自加了 16 或套了 40、48vp，或在尺寸由内容决定的 Stack / Column 上直接写 .border(...)
- [Compose 的 padding 和系统栏内距修饰符](compose-padding-modifier/index.md)（7 条）：读到 Compose 的 Modifier.padding(...)（horizontal、start / end）、statusBarsPadding / navigationBarsPadding 及它们在 heightIn、background 前后的顺序；产物里 padding、margin、constraintSize 落在哪个组件、用什么方向
- [M3 IconButton 的最小触控尺寸](m3-iconbutton-min-size/index.md)（1 条）：读到 M3 IconButton 外部 Modifier.size(...) 小于 48.dp（可带 CircleShape 背景）；产物里按字面尺寸写的 Button 宽高、borderRadius 和 margin
- [dp 尺寸在目标端的单位](dp-vp-unit/index.md)（4 条）：读到源端以 dp 给出的尺寸（布局 XML 的 1dp、vector drawable 的 android:width / height）或在 dp 列宽内折行的 TextView；产物里写成 'px' 字符串、按密度除过的数，或对本按 vp 解析的宽度又做了 vp2px
- [wrap_content 容器按子项定宽](wrap-content-width/index.md)（1 条）：读到 wrap_content 宽的纵向 LinearLayout，或 PopupWindow#setWidth(WRAP_CONTENT) 的弹层，子项里 match_parent 和固定 dp 宽混排；产物里容器宽是不是 Math.max(各子项宽) + padding，有没有把 match_parent 子项自己测出的宽也算进去
