# 滚动容器

源端有 ScrollView、NestedScrollView 和写在它外面的顶栏，目标端有 Scroll、它的内容 Column 的高度和 edgeEffect 时

## 触发族

- [滚动容器之外的顶栏和标题栏](scroll-outer-header/index.md)（1 条）：读到纵向 LinearLayout 里写在 ScrollView / NestedScrollView 或列表容器之前的顶栏、标题栏；产物里这些栏进了 Scroll 的内容 Column
- [Scroll 内容区的高度和纵向位置](scroll-content-height/index.md)（8 条）：读到 ScrollView / NestedScrollView 或权重剩余区里的内容、空态和等高列；产物里 Scroll 内容 Column 上的 .height('100%')、.layoutWeight、constraintSize({ minHeight })、justifyContent
- [ScrollView 的越界模式](scroll-overscroll/index.md)（1 条）：读到 <ScrollView> 写了或没写 android:overScrollMode；产物里 Scroll 的 .edgeEffect(...)
- [Compose 滚动容器的滚动条和越界效果](compose-scroll-defaults/index.md)（5 条）：读到 Compose 的 LazyColumn、Modifier.verticalScroll / horizontalScroll（包括 ModalBottomSheet 里的），modifier 上有没有滚动条修饰符、有没有用 LocalOverscrollFactory / overscrollEffect 覆盖越界效果；产物里 List、Scroll 的 .scrollBar(...)、.edgeEffect(...) 写没写、写的什么
- [ScrollView 没写的滚动条外观和进页唤醒](scroll-scrollbar/index.md)（2 条）：读到 HorizontalScrollView / ScrollView 没写 android:scrollbars、fadeScrollbars、scrollbarSize、scrollbarThumb*，外观和进页唤醒（initialAwakenScrollBars）取自平台和 Activity 主题；产物里 Scroll 的 .scrollBar(BarState…) 切换时机、有没有 .scrollBarWidth / .scrollBarColor
