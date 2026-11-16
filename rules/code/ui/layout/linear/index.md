# 线性排列与权重

源端有 LinearLayout 的 gravity、layout_gravity、layout_weight、weightSum，或 Compose Row / Column 的 weight、verticalAlignment，目标端有 Row、Column 的 alignItems、justifyContent、layoutWeight 时

## 触发族

- [LinearLayout 的 gravity 和子项对齐](linear-gravity/index.md)（5 条）：读到 LinearLayout（或 ConstraintLayout、Compose Column）写了或没写 android:gravity、layout_gravity；产物里 Row / Column 的 alignItems、justifyContent 和子项的 layoutWeight
- [LinearLayout 的权重子项（layout_weight、weightSum）](linear-weight/index.md)（4 条）：读到 LinearLayout 子项带 android:layout_weight（XML 里或代码的 LayoutParams 里），可能还有 android:weightSum；产物里这些子项的 .layoutWeight、.flexGrow、.width('100%') 或算出来的显式尺寸
- [横向行里 wrap_content 子项的宽度](row-wrap-content-width/index.md)（2 条）：读到横向 LinearLayout 里 wrap_content 的文字或图片列，和定宽兄弟并排、总宽接近或超过屏宽；产物里 Row 子项写成固定 .width、没有 .flexShrink 或按比例的 layoutWeight
- [兄弟间距用的单侧外边距](sibling-margin/index.md)（2 条）：读到 LinearLayout 子项只在一侧写 android:layout_marginStart / layout_marginEnd / layout_marginRight 当兄弟间距；产物里每项两侧对称的 .margin(...)，或 layoutWeight 项上带 .margin
- [Compose 行容器的高度和垂直对齐](compose-row-height-align/index.md)（3 条）：读到 Compose Row（没写 verticalAlignment，或 Modifier.height(IntrinsicSize.Min)）和按内容定高的横向滚动行（ScrollableTabRow、horizontalScroll）；产物里 Row / Scroll 的 alignItems 和 height
- [Compose Row 子项的 weight、fillMaxWidth 和基线对齐](compose-row-weight/index.md)（4 条）：源端 Compose Row 里子项的 Modifier.weight、fillMaxWidth、wrapContentWidth、alignBy(LastBaseline)，对应目标 Row / Flex 子项上的 layoutWeight、textAlign、ItemAlign.Baseline 和可见性
- [Ionic 内容区的纵向排布（IonContent）](ionic-content-flow/index.md)（1 条）：读到 IonContent 里依次排着 IonChip、Swiper、IonButton 等，源上没有 flex-grow、height: 100% 或 ion-padding；产物里外层 Column、Swiper、Image 上的 .layoutWeight(1)、height('100%') 和内容 Column 的水平 .padding
- [按 layout_weight 分高、带大内边距的 ImageView](weighted-imageview-padding/index.md)（1 条）：读到纵向 LinearLayout 里 ImageView 写 android:layout_height="0dp" 加 android:layout_weight，同时带 android:padding；产物里是不是写成 Image(...).layoutWeight(...).padding(...)
