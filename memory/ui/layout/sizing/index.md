# ui/layout/sizing

宽高、比例、百分比与边距的组合（父尺寸减边距、占剩余空间，由内容定尺寸的父级里的百分比），Compose 修饰符链顺序与 Row 的测量顺序、固有高度，Material 按钮的布局占位与实绘尺寸，px 域整数布局公式与随进度收放的间距，以及随内容定尺寸的图片、背景和描边，以及非 Row/Column/Flex 父级中 layoutWeight 不生效时的显式尺寸；嵌入满高子组件时的剩余高度分配，居中的 wrap_content 子项组不被拉伸。；换容器（Tabs、Grid 槽位改自绘 Row）后子项的主轴尺寸，TableLayout 按内容测量的列宽

[上一级](../index.md)

## 本级经验

- [Compose Modifier 链里位于背景之前的内距与 inset 放外层，背景、圆角和裁剪放内层](lesson-5c6217b05bb4c266f254.lesson.md)
  - 时机：规格提取与界面实现阶段，描述或翻译同一条 Compose Modifier 链中的 padding、statusBarsPadding 与 background、clip、Surface 形状时
  - 情境：源 Modifier 链中 padding 或窗口 inset 位于 background、clip 或 Surface 包装之前；目标 ArkUI 的 padding 计入组件尺寸，backgroundColor 和 borderRadius 覆盖含 padding 的整个组件。
- [Compose Row 中无 weight 的 fillMaxWidth 子项先占满剩余宽：不换成 layoutWeight(1)，后续兄弟按实得宽度判断是否绘制](lesson-45f77b3088fa69398f9e.lesson.md)
  - 时机：规格提取或页面转换阶段，解释 Compose Row 的可见元素和横向空间分配时
  - 情境：有限宽度的 Row 中，无 weight 子项使用 fillMaxWidth()，后面还有兄弟（按钮、文字）；规格或派工可能用“近乎不可见、按源码保留”描述该兄弟，实现者准备把该子项换成 layoutWeight(1)。
  - 例外：fillMaxWidth 带比例、主轴约束无上限或子项使用 weight 时，按当前分配规则处理，不套“占满剩余宽度”。；后续子项含 requiredWidth/requiredSize、无界 wrapContent 或自定义测量/绘制时，零宽约束仍不足以判断实际是否绘制。
- [LinearLayout 以 gravity=center 摆放的 wrap_content 子项组转成 Row 时保留居中与按内容定宽，不给中间输入框 layoutWeight(1) 拉满](lesson-02b2fcd7d157d97f95c8.lesson.md)
  - 时机：界面实现阶段，把数量步进器（减号、数量框、加号）一类居中的 wrap_content 子项组翻译成 ArkUI Row 时
  - 情境：源端 LinearLayout 设 gravity=center 与固定外边距，子项是 wrap_content 的按钮与 EditText；控件可能叠在带装饰的背景图（票券存根、竖虚线）上。
- [LinearLayout 的 weightSum 与子权重之和不等，或 wrap_content 子项带权重时，不用 layoutWeight 归一化：余量（可用尺寸减各子项自然尺寸）按 w/剩余 weightSum 依次分配，份额耗尽的子项只留自然尺寸，超出 weightSum 的末块被裁](lesson-adad817f2c3c8f1eaa09.lesson.md)
  - 时机：界面实现阶段，把 Android LinearLayout 的 layout_weight/weightSum 分配翻译成 ArkUI 尺寸时；规格提取阶段写权重布局时
  - 情境：源布局声明 weightSum 且与子权重之和不等（如根 weightSum=10 而子权重 4/1/9，列 weightSum=6 而 8 个 wrap_content 子项各权重 1），或 wrap_content 子项带权重、自然尺寸各不相同。
- [Row 中位于定宽兄弟之后的 wrap_content 多行文字要加 flexShrink(1)（或 layoutWeight(1)）才会在剩余宽度内折行：Row 设了满宽，子项也默认不收缩](lesson-8566839cffc9e9e7fa30.lesson.md)
  - 时机：界面实现阶段，把横向 LinearLayout 中位于固定尺寸兄弟之后的 wrap_content 文字转成 ArkUI Row 子项时
  - 情境：源横向 LinearLayout（常见于 layout-land）中，固定 dp 的 ImageView 之后跟 wrap_content 宽、带左右 padding 的多行 TextView；文本长于剩余宽度时 Android 以 AT_MOST 取行内剩余宽折行。目标 Row 本身可能已设 width('100%')。
- [Row(height(IntrinsicSize.Min)) 先算出固有高度写成显式高度，再让子项按百分比撑满并保留源偏移](lesson-cb1a12afca61db08ed9a.lesson.md)
  - 时机：页面转换阶段，遇到 Row(height(IntrinsicSize.Min)) 且子项 fillMaxHeight、带 padding(top) 等偏移时
  - 情境：源 Row 以固有最小高度定高，高度由最高的子项（如按钮的最小触控尺寸）决定；子项用 fillMaxHeight 并在内部偏移；目标端没有固有尺寸测量，迁移陷阱表提示不定高父级下的百分比子项会撑满。
- [TableLayout 加外部表头与 fake header 行的表格按内容测量列宽：表体每列宽取 fake header（文字＋paddingRight）与各单元格单行自然宽的最大值，不自拟 fr 比例或权重](lesson-6cb9ad45093ce2ca28af.lesson.md)
  - 时机：规格提取与页面转换阶段，把 Android TableLayout 表格（滚动表体外另有固定表头）翻译为 ArkUI 列宽时
  - 情境：源页面在 ScrollView 外放一行固定表头 TableRow，表体 TableLayout 首行是 height=0、文案与 paddingRight 同表头的 fake header 行（注释说明用于对齐外部表头列宽）；单元格是默认 wrap_content 的 TextView 逐行 addView，没有设定列宽；合成 view.xml 会丢掉 padding 与 height；规格可能写“fake header 删除（Grid 定宽列天然对齐）”并自拟 columnsTemplate 或权重。
- [layout_marginStart/End 写成 margin 的 start/end 时同一对象各边都用 LengthMetrics；不需要随语言方向翻转时改用 left/right 数值](lesson-e3077bf60cfc3f34d0a2.lesson.md)
  - 时机：界面实现阶段，把 layout_marginStart/End、paddingStart/End 或 Compose padding(start/end) 一类方向相关边距写成 ArkUI margin/padding 时；维护映射参考的边距示例时
  - 情境：源布局用 marginEnd/marginStart（常与 marginBottom 等写在同一控件上）；映射参考把它对到 .margin({ end }) 并给出纯数字示例。
- [“父尺寸减边距”或“扣除兄弟后的剩余空间”不写成 '100%'：match_parent/0dp 加同轴 margin 改用容器 padding 或 calc，Column 中占剩余高度的内容区用 layoutWeight(1)，等权重兄弟的间距改用 space](lesson-75f4743dff663f50966b.lesson.md)
  - 时机：界面实现阶段，把 match_parent 或两侧约束 0dp 且带同轴 margin 的视图、或带 margin 的等权重兄弟翻译成 ArkUI 尺寸与间距时；按要求调整左右边距时；为 Compose Column 中排在搜索栏、分隔线等固定高度节点之后、占满剩余高度的内容区确定高度时；宿主页在固定标题栏下嵌入根节点为 height('100%') 的面板或弹层组件时
  - 情境：源元素 match_parent（或约束到父两侧的 0dp）同时设 layout_marginHorizontal/Start/End 或 marginTop/Bottom；或水平 LinearLayout 中等权重（0dp + weight）的子项以 marginStart 作间距；目标用 width/height('100%') 或 layoutWeight。也包括 Compose Column 里内容区排在固定高度兄弟之后，靠 fillMaxSize、weight 或 Lazy 列表默认行为占满剩余高度，可能有空结果、加载、结果等多个状态分支。 也包括宿主页 Column 顶部有固定高度标题栏，下方直接放根节点 height('100%')、自带标题行与底部按钮栏的筛选面板；对应 Android 以 MATCH_PARENT 的 PopupWindow showAsDropDown(标题栏) 弹出，只占锚点以下的高度。也包括 wrap_content 加 minWidth 实际占满可用宽，或 RecyclerView 项偏移（ItemDecoration）被写成容器外边距的变体。
- [区分 Material 按钮的布局占位、背景实绘与触控范围：不只凭调用处 size 定背景，也不给内容撑开的容器补最小尺寸](lesson-b73a1ac8908f74856a02.lesson.md)
  - 时机：规格提取或界面实现阶段，确定 Material 按钮及包装容器的尺寸与位置时
  - 情境：源组件含 size/background 与库内部的最小交互尺寸规则（如 IconButton 在调用方 .size(x) 之内再套 minimumInteractiveComponentSize），或只是由内容撑开的 Surface/Box（如图标撑开的圆钮）；ui 快照由源码合成、bounds 为空时，调用处 size 数值最容易被当成实绘尺寸。
  - 例外：当前组件明确关闭或改写了最小交互尺寸，或强约束及修饰符顺序限制了其作用时，不套默认最小尺寸。
- [将图片内容缩放与组件尺寸约束分别落实：wrap_content + adjustViewBounds 的图片按位图像素比确定高度](lesson-624248be2c5f81082268.lesson.md)
  - 时机：界面实现阶段，为图片组件确定宽高约束时；校准阶段处理图片比例、宽度类的不确定占位时
  - 情境：源 ImageView 为 wrap_content + adjustViewBounds（可带 layout_constrainedWidth 与 bias），宽度受同行兄弟和边距约束，高度应随位图固有比例跟随；目标用 Row 内的 Image 承接。
  - 例外：当前父布局或明确的尺寸规则已给出图片盒的宽高，此时只需设置盒内缩放
- [并排 wrap_content 图片列不按固有 dp 写死宽度：按固有宽度比例分列，高度用 aspectRatio](lesson-0618cdf331560d389f0e.lesson.md)
  - 时机：界面实现阶段，把 match_parent 父行中并排的 wrap_content 图片列转换为 ArkUI Row/Column 并确定列宽时；修复“右侧顶满/被遮挡”时
  - 情境：源布局在 match_parent 的水平 LinearLayout 中并排放置 wrap_content 图片列，列宽来自 drawable 固有尺寸与左右、列间 margin，其总和接近或超过常见手机屏宽；目标要在宽度不同的设备上与源截图对齐。
- [把原由 Tabs、Grid 等容器分配槽位的子项搬进自绘 Row/Column 时重新确定主轴尺寸：等分用 layoutWeight(1)，不保留依赖旧容器的 width('100%')](lesson-c572346f0be19acf5579.lesson.md)
  - 时机：公共组件或页面实现阶段，把 Tabs 内置 tabBar、Grid 等由容器分配槽位的子项改写为自绘 Row/Column + ForEach（如自绘底部导航），确定每个子项的主轴尺寸时
  - 情境：源端底栏是水平 LinearLayout，子项由代码以 LayoutParams(0, MATCH_PARENT) 与 weight=1 动态添加，布局 XML 里没有静态子项；目标原先用 Tabs BarMode.Fixed 承载页签、页签 builder 写 width('100%')/height('100%')，新组件把该 builder 原样搬进 Row。
- [把靠 layoutWeight 填满并居中的内容移进 Refresh、Stack 等非 Row/Column/Flex 父级时，改用 height('100%') 等显式尺寸](lesson-1c3d6367be48f70bb001.lesson.md)
  - 时机：界面实现阶段，把已有空态、未登录引导等内容 builder 放进下拉刷新组件或其他封装容器的 content 时，确定内容根节点的高度约束
  - 情境：内容根节点原本在 Column 中用 layoutWeight(1) + justifyContent(Center) 占满剩余空间并居中；新父级是封装了原生 Refresh（或 Stack、Scroll 等）的组件，经 @BuilderParam 注入内容；工程里可能已有同样写法可以照搬。
- [源端在整数 px 上取整的布局公式：规格写明运算域，实现在 px 域取整、写入布局属性前再换回 vp](lesson-0ef2cd00e1a91491b350.lesson.md)
  - 时机：规格提取阶段，把自定义 Layout、MeasureScope 里的测量与整数几何公式翻成目标契约时；界面实现阶段，用 onAreaChange、measureText 等返回值驱动这类公式时；移植自绘 View 的绘制坐标、setBounds 边界、位移与文字基线修正中的 (int) 强转时
  - 情境：源算法在约束或测量结果（Compose constraints、placeable 宽高等整数 px）上做整数除法、.toInt() 截断或取整；目标布局属性和尺寸回调（onAreaChange）使用 vp 等逻辑单位，回调值通常不是整数，measureText 返回 px。 也包括 Canvas 绘制代码中的 (int) 强转（setBounds 边界、int 位移、文字基线修正），其中的量可能为负。
  - 例外：公式本来作用于 Dp 常量（固定间距、固定尺寸），不涉及 constraints 或 placeable 时，按原单位保留
- [由内容定尺寸的父级（列表行、wrap_content 头部、FIT_CONTENT 半模态）里不写 width/height('100%')：描边背景画在节点自身，行内撑满用 Stretch；源端描边不改尺寸时注意 .border() 计入测量（定尺寸遮罩中的居中弹卡不在此列，宽度按源窗口规则）](lesson-a58ebfe7a4c55b041b14.lesson.md)
  - 时机：界面实现与规格映射阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景，为高度由内容决定的行加铺满的背景层（滑删进度背景等），或把 Compose Modifier.border 这类只绘制、不改测量的修饰符落到 ArkUI 容器上时；把 match_parent 高度翻译到 ListItem、列表行组件、折叠头部背景层或 bindSheet 内容根时；转换将被宿主嵌入的子组件（Fragment 转子组件）、确定根节点及各状态视图的高度约束时
  - 情境：源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。也包括列表行里的 Stack 没有确定高度，准备放一层宽高 100% 的背景子节点；或源 border 画在调用方已定尺寸的盒内侧，目标容器自身不设宽高、尺寸由槽内容决定。也包括源 match_parent 子视图位于 wrap_content 的行、AppBar 或 BottomSheet 容器中，实际随内容或兄弟高度；目标放进 List、ListItem、Scroll 或 FIT_CONTENT 半模态，准备直译为 height('100%')。也包括被宿主嵌入的子组件：源布局根节点与空态容器都是 wrap_content，在宿主 NestedScrollView 的 wrap_content 槽位里按内容取高；目标根 Column 与 loading/empty/error 各分支写 height('100%')，宿主把它放进 Scroll 内未设高度的 Column。
  - 例外：父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用；页面根 Stack 等定尺寸遮罩里的居中弹窗卡片：父级已定尺寸，宽度按源端窗口规则写（框架 AlertDialog 为屏宽 95% 减左右各 16dp），不适用本条，也不从本条取固定 vp 估值
- [网格里跨列数不同的卡片要同行等高时，用实际列宽与留边推导宽卡比例；组件自身的原生宽高比只用于卡内内容缩放](lesson-4fc212d401ac7b2a4218.lesson.md)
  - 时机：列表或首页网格的界面实现阶段，为不同尺寸规格（如 2x2、4x2）的卡片确定外框高度或 aspectRatio 时
  - 情境：源网格按规格分配 span（窄卡占 n 列、宽卡占 2n 列），卡片两侧有固定内边距或网格留边；参考截图里同一行的窄卡与宽卡外框等高；目标用百分比列宽加 aspectRatio 决定卡片高度，手头有组件自身的原生尺寸表（如 334.75×158）。
  - 例外：源端或参考截图里不同规格的卡片本就按各自原生比例显示、不等高
- [随选中进度收放的图标与文本位置：源端为 0 的间距按同一选中条件归零](lesson-c39245065cc26d8c9f64.lesson.md)
  - 时机：界面实现阶段，把源端自定义 Layout 中随动画进度收放的图标、文本位置公式翻成 ArkUI 属性时
  - 情境：源端导航项等按 animationProgress 计算文本宽度（含其两侧间距），未选中时为 0、图标在槽内居中；目标用 Row 居中加 constraintSize、opacity、scale 折叠文本来模拟。
