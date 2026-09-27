# ui/layout

容器选择、约束与定位（ConstraintLayout、RelativeContainer、Column 等），默认对齐差异、百分比尺寸与 margin、跟随等高、滚动容器的包含范围、运行时挂载层与锚点转换、随滚动折叠的顶栏、全屏底层与状态覆盖层骨架、gone 节点与列表 item 布局，以及视觉修复中固定尺寸的依据

[上一级](../index.md)

## 本级经验

- [ConstraintLayout 中单视图对 parent 居中、兄弟单向悬挂时，用 RelativeContainer 复刻，不用 Column 整组居中](lesson-e607a28fcd91acd2b40f.lesson.md)
  - 时机：规格提取阶段把 ConstraintLayout 约束翻译成容器与定位决策，或页面实现阶段落定容器时
  - 情境：源 ConstraintLayout 中一个子视图以 start/end/top/bottom 四向锚定 parent 自身居中，另一个兄弟只以 constraintTop_toBottomOf 等单向约束挂在它下方，兄弟之间没有双向约束。
  - 例外：兄弟之间有双向约束构成 chain 时，按 chain 语义（chainStyle）另行转换，不适用本条
- [ConstraintLayout 改写成 Column 顺序流前先列出各子项锚点：锚父底、锚兄弟与双 0dp 比例子项都要保留语义](lesson-3fe0026df9abc72ff788.lesson.md)
  - 时机：界面实现阶段，把 ConstraintLayout 转成 Column/Row 顺序流或 Stack 层级，确定锚点边距与比例子项尺寸时
  - 情境：源 ConstraintLayout 中有多个子项 constraintBottom_toBottomOf=parent（含 invisible 仍占位的行）、按钮上方的文字以 constraintBottom_toTopOf 锚在兄弟上、0dp×0dp 加 dimensionRatio 的子项夹在上下锚点之间；目标用 Column 顺序流、layoutWeight、Visibility.Hidden 或父 Stack 的 BottomStart。
- [match_parent/0dp 加同轴 margin 表示“父尺寸减边距”：不写成百分比加 margin，等权重兄弟的间距改用 space](lesson-75f4743dff663f50966b.lesson.md)
  - 时机：界面实现阶段，把 match_parent 或两侧约束 0dp 且带同轴 margin 的视图、或带 margin 的等权重兄弟翻译成 ArkUI 尺寸与间距时；按要求调整左右边距时
  - 情境：源元素 match_parent（或约束到父两侧的 0dp）同时设 layout_marginHorizontal/Start/End 或 marginTop/Bottom；或水平 LinearLayout 中等权重（0dp + weight）的子项以 marginStart 作间距；目标用 width/height('100%') 或 layoutWeight。
- [为已转换页面接线时保留“全屏底层 + 按状态切换的前景层”骨架；地图 SDK 不可用也不把全屏承载改成自绘小卡](lesson-4de4283ec625be7e976c.lesson.md)
  - 时机：功能切片为已转换页面接入 ViewModel、Service 与跳转，决定保留还是重写布局骨架时；巡检修复处理“缺少全屏地图承载”一类发现时
  - 情境：Android 页面以全屏 MapView/导航视图为底层，前景由 ViewModel 布尔状态（如 showRoute）切换两套覆盖层；导航页 FEATURE_NO_TITLE、只承载导航视图；目标地图/导航 SDK 暂不可用，页面转换阶段已写出带全屏占位底图与两态覆盖层的骨架。
- [播放器面等运行时 addView 挂到根部的层，按运行时层级实现，不按 XML 里的占位区域定几何](lesson-c3dcc5a25a0ad59c53c1.lesson.md)
  - 时机：界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时
  - 情境：源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0) 无约束铺满），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。
- [横向滚动容器给交叉轴写数值高度，按内容算出，不写 'auto' 也不留空](lesson-2d7c6de68f604ae77caf.lesson.md)
  - 时机：界面实现阶段，把 Compose 可滚动 Tab 行、LazyRow、horizontalScroll 等按内容定高的横向滚动行翻译成 ArkUI 滚动容器时
  - 情境：源端横向滚动行的高度由子项固有高度决定；目标用 Scroll(ScrollDirection.Horizontal) 或横向 List/Grid 实现，所在父容器在纵向上还有剩余空间。
- [源端 exitUntilCollapsed 连续折叠顶栏按滚动偏移算折叠比例插值，不用首个可见行索引做两态切换](lesson-67ab02abe6ec76f4129e.lesson.md)
  - 时机：界面转换阶段，把 LargeTopAppBar/LargeFlexibleTopAppBar 配合 exitUntilCollapsedScrollBehavior 的顶栏落成 ArkUI 时
  - 情境：源端顶栏由 collapsedFraction 驱动高度、标题、背景色与阴影；目标页用 List 或 Scroll 承载内容。
- [源端“右列 match_parent 跟随左卡等高”在 Scroll 内用实测高度传递实现，不用估算常量](lesson-8334433bea644f2a89ae.lesson.md)
  - 时机：界面实现与验证期修复阶段，为并排卡片确定跟随等高约束，而整行位于 Scroll 等纵向无界容器中时
  - 情境：Android 水平行里右列 height=match_parent 随左侧 wrap_content 卡片等高；整行在 NestedScrollView（ArkUI Scroll）中；目标在 Scroll 内用纵向 layoutWeight 或 height('100%') 会被撑高失控。
- [源端默认起始对齐和贴顶要显式写出：ArkUI Column 交叉轴默认居中，Scroll 内不满一屏的内容默认居中](lesson-08b9064f678f1635e647.lesson.md)
  - 时机：界面实现阶段，把纵向 LinearLayout、带 constraintStart/Top 的 ConstraintLayout 或 ScrollView/NestedScrollView 转成 ArkUI Column 与 Scroll 时
  - 情境：源纵向 LinearLayout 没写 gravity（子项默认贴起始边），或 wrap_content 子项以 constraintStart_toStartOf=parent 靠起始边、卡片以 constraintTop_toTopOf=parent 贴顶；目标 Column 宽度撑满，子项为固定或内容宽度；滚动页内容常不满一屏。
- [视觉修复前把截图尺寸差折算成 vp，与源布局值和目标当前值对照；目标已等于源值时不放大固定尺寸](lesson-8119d8bf0b58e4daac24.lesson.md)
  - 时机：视觉校验与修复阶段，根据双端截图差异撰写尺寸类工单，并决定是否修改页面固定高度、间距时
  - 情境：源端基线截图与目标截图来自不同设备或屏幕密度，并排对比显示目标主内容“偏小”或“偏上”；目标页的主要区块已按源布局 dp 字面值写入固定高度与 marginTop，并与底部 Tab 共享有限的纵向空间。
- [贴合内容的描边、选中背景画在由内容定尺寸的节点自身，不用 width/height('100%') 覆盖层](lesson-a58ebfe7a4c55b041b14.lesson.md)
  - 时机：界面实现阶段，翻译用 fillMaxSize()、matchContentSize 贴合内容的选中指示器、描边或背景时
  - 情境：源端指示器或背景层以 fillMaxSize、matchContentSize 贴合某个由内容定尺寸的格子；目标准备在 Stack/Row 里叠一层 width/height('100%') 的节点来画描边或背景。
  - 例外：父节点有确定的宽高（显式数值，或已被外层约束定死）时，百分比层按该尺寸解析，可以使用
- [转换 NestedScrollView/ScrollView 时只把源滚动容器内的子节点放进 Scroll，位于其前的固定头部留在 Scroll 外](lesson-46a0d7f239efac925d33.lesson.md)
  - 时机：界面实现阶段，把 Android 页面转成 ArkUI 时确定固定区域与 Scroll 的包含范围；以及规格提取阶段书写滚动容器的转换决策时
  - 情境：源布局根为纵向 LinearLayout，顶部用户栏或工具栏在 NestedScrollView 之前、以固定 marginTop 定位，其下 layout_weight=1 的滚动容器承载地图、主按钮、卡片等主体；目标用 ArkUI Scroll 实现。
- [页面转换逐项落实源 XML 的 gone 节点、固定尺寸点击容器与 tools:listitem 行布局](lesson-f1a98587fe72ff68c5a8.lesson.md)
  - 时机：页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时
  - 情境：源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。
