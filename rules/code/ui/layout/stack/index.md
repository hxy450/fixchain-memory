# 叠层与相对定位

源端有 FrameLayout、RelativeLayout、ConstraintLayout 的叠放和相对规则，或 Compose Box 的 contentAlignment、Modifier.align，目标端有 Stack、.align、.position、zIndex、hitTestBehavior 时

## 触发族

- [Stack 上层的点击命中](stack-hit-test/index.md)（7 条）：读到 FrameLayout 里较晚声明、本身不可点击的 match_parent 容器或进度环叠在按钮上；产物里 Stack 上层子节点没写 .hitTestBehavior(HitTestMode.Transparent)，onClick 只挂在底层
- [FrameLayout 里的头像与角标](avatar-badge/index.md)（3 条）：读到固定尺寸 FrameLayout 里铺满的头像 ImageView、layout_gravity="end|bottom" 的角标、按步距重叠的头像；产物里 Stack 中角标的 .align / position、头像的 .border，以及从旧 ArkTS 片段照搬的写法
- [RelativeLayout 子项的相对规则、贴边和叠放](relative-layout-children/index.md)（12 条）：读到 RelativeLayout（或 FrameLayout）的子 View 带 layout_alignParent*、layout_below、layout_centerVertical、CENTER_IN_PARENT、父容器 android:gravity，或没有任何相对规则；产物里对应的 Column / Row 顺序排列、Row+Blank、Stack 子项上的 .align、Stack 的 alignContent、.position 和 zIndex
- [ConstraintLayout 子项的约束和锚点](constraint-anchors/index.md)（7 条）：读到 ConstraintLayout 子项的 app:layout_constraint*_to*Of="parent" 或指向兄弟、0dp 加 dimensionRatio；产物里换成了 Stack 加 .align()、带 Blank() 的 Row、百分比 position、整组居中的 Column 或照抄 margin 的顺序流
- [Compose Box 叠放子项的对齐和定位（contentAlignment、Modifier.align）](box-align/index.md)（6 条）：读过的 Compose 源码里 Box(contentAlignment = …) 叠放子项，子项用 Modifier.align(Alignment.BottomCenter) 等钉在顶部、底部或角上；交回的 Stack 写了 justifyContent、不存在的 Alignment.CenterStart、子项上的 .align()，或把顶栏底栏塞进全屏 Column 加 Blank，定位只留在注释里
- [Stack 上叠加的覆盖层和全屏遮罩](stack-overlay-hit-test/index.md)（7 条）：读到参考实现里原生地图 XComponent 铺在最底层、上面叠 ArkUI 控件，或同仓页面在无 padding 的根 Stack 里条件渲染全屏遮罩，产物里是覆盖层有没有 .hitTestBehavior(...)，以及挂在带 padding 容器上的 .overlay(...)
- [按朝向在代码里重排的 RelativeLayout 子控件](rotation-relayout/index.md)（2 条）：读到源 Activity 按界面方向和系统朝向（getRotation、onConfigurationChanged）在代码里用 RelativeLayout.LayoutParams / setMargins 逐控件重排、按导航栏间隙加边距；产物里布局控制器产出的逐控件摆位和 margin 字段，以及按钮层固定百分比的 .position
- [布局里的 start / end 方向和 RTL 镜像](rtl-start-end/index.md)（2 条）：读到布局 XML 里同一控件或三方容器带 android:layout_gravity="bottom|end" 和 android:layout_marginEnd；产物里 Alignment.BottomEnd、HorizontalAlign.End 配 .margin({ right })，或容器内部子项整体镜像、整体不镜像
