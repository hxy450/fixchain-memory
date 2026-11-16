# 布局与尺寸

源端有布局 XML（LinearLayout、RelativeLayout、ConstraintLayout、FrameLayout、TableLayout，include / inflate 进来的布局、layout-land 等变体）、android:visibility，或 Compose 的 Row、Column、Box、自定义 Layout 和项目自己的 @Composable 组件，目标端有 Row、Column、Stack、共享 @Component 和 .width、.height、.margin、.padding、显隐条件时

## 子主题

- [线性排列与权重](linear/index.md)（22 条）：源端有 LinearLayout 的 gravity、layout_gravity、layout_weight、weightSum，或 Compose Row / Column 的 weight、verticalAlignment，目标端有 Row、Column 的 alignItems、justifyContent、layoutWeight 时
- [宽高与边距](size/index.md)（53 条）：源端有 layout_width / layout_height、match_parent、wrap_content、layout_margin*、padding*、dp 尺寸，或 Compose 的 padding、size、fillMaxSize、heightIn 修饰，目标端有 .width、.height、.margin、.padding、constraintSize 时
- [叠层与相对定位](stack/index.md)（46 条）：源端有 FrameLayout、RelativeLayout、ConstraintLayout 的叠放和相对规则，或 Compose Box 的 contentAlignment、Modifier.align，目标端有 Stack、.align、.position、zIndex、hitTestBehavior 时

## 触发族

- [源布局里的图文结构](layout-structure/index.md)（8 条）：读到源布局 XML 由 ImageView 加 TextView 的菜单行、带标题条背景和插图的卡片、固定高度标题栏、TabLayout 等组件组成；产物里只剩 Text、缺 Image、卡片数少，或保留了源布局里没有的区块只调尺寸
- [源端控件的显隐：XML 初值和代码里的 setVisibility](source-visibility/index.md)（15 条）：读到布局 XML 里的 android:visibility="gone" / "invisible"，或 Activity、Fragment、Adapter 里按状态、开关、渠道调的 setVisibility(View.GONE / VISIBLE / INVISIBLE)；产物里对应组件的 if 条件、.visibility(...)，或被无条件渲染、被删掉
- [共享组件和子页面的显隐入参](shared-component-visibility-param/index.md)（6 条）：读到源端控件在构造、绘制或宿主 Adapter 绑定时按条件改显隐，目标由共享组件或子页面承载；产物里组件的 @Param / @Prop 入参、默认值和组件内的 .visibility(...) 分支
- [资源限定符目录的覆盖（values-w / sw、layout-land）](qualifier-override/index.md)（5 条）：读到源 res 里同名资源在 values-w<N>dp、values-sw<N>dp 的 dimens.xml 或 layout-land 下另有定义，交回的代码只用了基础值，或方向分支漏了部分属性
- [换外层容器后留下的布局修饰](container-swap/index.md)（2 条）：读到原先在 Column 里靠 .layoutWeight(1)、.justifyContent(...)、.alignItems(...) 撑满和居中的节点；产物里换成 Scroll 或移进 Refresh 后，这些修饰原样留在新容器或根节点上
- [inflate / setContentView 加载的弹窗与页面布局](inflated-layout/index.md)（4 条）：读过的源码里弹窗或二级页由 inflate(R.layout…)、以 Binding 结尾的 ViewBinding 类的 inflate、setContentView 或工具类的 show…Dialog 加载一个布局 XML；交回的目标弹窗或页面是按行为代码、功能描述、通用确认弹窗或 bindSheet 拼出来的
- [项目自定义 Compose 组件和共享组件](shared-composable/index.md)（7 条）：源端调用项目自己的 @Composable 组件（CircleShape、ContentScale.Crop、裁切写在组件定义里，调用点只传尺寸和资源），对应目标的 Image 外观、共享 @Component 的参数和页内副本
- [Compose 自定义 Layout 的测量和摆放](compose-custom-layout/index.md)（3 条）：读到 Compose 自定义 Layout 里按 constraints、Placeable 的宽高算位置（placeRelative、constraints.maxWidth / n、动画进度乘文本宽）；产物里用 Stack 对齐、padding/margin、translate/position 和手写公式重现
- [TableLayout 的列宽](table-layout-columns/index.md)（2 条）：读到原始布局 XML 里 TableLayout 表头单元 wrap_content 带 android:paddingRight，另有 0dp 高、padding 相同的对齐 TableRow；产物里表格列写成 .layoutWeight 比例常量或 columnsTemplate 的 fr，对齐行被删掉
- [Compose FlowRow 的换行排列](compose-flow-row/index.md)（1 条）：读到 Compose 的 FlowRow（Arrangement.SpaceBetween、spacedBy），尤其 FlowRow 里再套 FlowRow 加尾随元素；产物里外层和内层都是 Flex({ wrap: FlexWrap.Wrap }) 加 .flexGrow(1)，或 onMeasureSize / onPlaceChildren 写的自定义布局
