# ui/layout

页面几何与层级：按约束定位、尺寸与边距、滚动区域、运行时覆盖层选择分支；通用页面结构（源 XML 节点、gone 容器与工具栏菜单项的逐项落实，AppCompat 下菜单溢出与返回箭头）、视觉修复依据与未声明 supportsRtl 时的容器布局方向留在本级；声明 supportsRtl 时 start/end 边距与自动镜像图标保留逻辑方向

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐（含 Compose Column/Row 的默认对齐），Compose Box 子项在 Stack 中的定位，基线对齐与逐行内距的 Row 组，及ArkUI容器中的子项定位。
- [layers](layers/index.md) — 运行时addView、全屏底层、状态覆盖层与 BottomSheetBehavior 管理的布局内面板：确定视图挂在哪里、如何叠放及几何范围；点击命中与事件时坐标属于ui/interaction。
- [scrolling](scrolling/index.md) — ScrollView/NestedScrollView 与 weight 剩余区列表的滚动范围（固定头部留在外、剩余区空态居中）、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高。，ScrollView 越界回弹的默认值（IF_CONTENT_SCROLLS）；LazyRow 摘要行转可横滑容器，程序滚动到某项的对齐方式（animateScrollToItem → ScrollAlign.START）；GridView/ListView 转 Grid/List 时的越界效果与滚动条初次显示
- [sizing](sizing/index.md) — 宽高、比例、百分比与边距的组合（父尺寸减边距、占剩余空间，由内容定尺寸的父级里的百分比），Compose 修饰符链顺序与 Row 的测量顺序、固有高度，Material 按钮的布局占位与实绘尺寸，px 域整数布局公式与随进度收放的间距，以及随内容定尺寸的图片、背景和描边，以及非 Row/Column/Flex 父级中 layoutWeight 不生效时的显式尺寸；嵌入满高子组件时的剩余高度分配，居中的 wrap_content 子项组不被拉伸。；换容器（Tabs、Grid 槽位改自绘 Row）后子项的主轴尺寸，TableLayout 按内容测量的列宽

## 本级经验

- [values-sw&lt;N&gt;dp(-land) 覆盖按设备屏幕短边 min(宽,高) 判定再叠加方向，不译成 mediaquery min-width](lesson-51bf52bc666b921ef2e9.lesson.md)
  - 时机：规格提取与界面实现阶段，把源端 sw&lt;N&gt;dp 限定目录（可带 -land/-port）的覆盖值落成运行期分支时
  - 情境：源 res 有 values-sw720dp-land 一类最小宽度限定目录，覆盖尺寸、边距等取值，注释常写“for sw720dp devices (e.g. 10" tablets)”；目标没有对应资源限定词，要在运行期按屏幕配置取值，可用 mediaquery 或 display 查询；规格里写成“横屏 + 最小宽度≥N”。
  - 例外：源限定目录是 values-w&lt;N&gt;dp、values-h&lt;N&gt;dp（当前可用宽高）：按当前窗口宽高取值，不按短边
- [工具栏导航图标按实际生效者绘制：基类以 ActionBarDrawerToggle 接管同一 Toolbar 时画汉堡；否则窗口 ActionBar 页在 Manifest 有 parentActivityName 时 AppCompat 默认显示 Up，都没有且未调 setDisplayHomeAsUpEnabled(true) 才不画；菜单项按实际生效的 showAsAction 分流：always 上栏，ifRoom 只在名额与宽度够时上栏，其余进溢出菜单（AppCompat 下 android:showAsAction 被忽略），可勾选项开启勾选指示](lesson-a6121cc7eaf207b702f7.lesson.md)
  - 时机：界面实现阶段，转换工具栏菜单 XML、自绘 ActionBar 或标题栏，决定导航图标（返回箭头或汉堡）、图标位与溢出菜单时；自绘框架主题提供的 ActionBar（应用图标、Up 尖角、溢出按钮、横竖屏高度与标题字号）时
  - 情境：源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。也包括 Activity 基于 AppCompat、菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"）。也包括判断导航图标的输入：Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data、代码是否调用 setDisplayHomeAsUpEnabled、基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState；目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。也包括框架 ActionBar（Theme.Holo 等）带 manifest android:icon、setDisplayHomeAsUpEnabled 与 showAsAction="ifRoom|withText"，目标多个页面各自用 hideTitleBar 自绘标题栏。
- [源 manifest 未声明 android:supportsRtl 时布局方向恒为 LTR：有顺序或对齐语义的容器逐个显式 Direction.Ltr](lesson-148a3e67bd557bafd722.lesson.md)
  - 时机：规格提取与界面实现阶段，为带多语言资源的应用确定布局方向契约，新建按钮条、对话框面板等有顺序或起止对齐语义的容器时（含返修中用自绘面板替换系统弹窗）
  - 情境：AndroidManifest 的 &lt;application&gt; 未声明 android:supportsRtl（安卓布局方向恒为 LTR）；应用含 fa 等 RTL 语言资源，或可能在 RTL 系统语言下运行；目标用 Row/Column 等容器实现按钮条、对话框或起始对齐的内容，未设 direction。
  - 例外：源端声明 android:supportsRtl="true"：按源布局的 start/end 语义让容器随语言方向翻转
- [源布局有 layout-land 等配置变体时逐控件逐属性对照，并在承载该布局的组件内按方向分支实现（ArkUI 没有布局资源限定词）；运行时 setBackgroundResource 只覆盖被调用的控件，其余控件取各变体 XML 的值](lesson-c8e645a542254d96997e.lesson.md)
  - 时机：界面实现阶段，合并 layout 与 layout-land 变体，或实现替代带变体 fragment 的共享组件时；计划与派工阶段指派变体实现时
  - 情境：源 res/layout-land/ 下有同名变体，控件的 background、weight、margin、textSize 或整体结构与竖屏不同；Activity 代码在运行时只对部分控件 setBackgroundResource；布局由另一任务的共享组件承载，派工只写竖屏结构，横屏要求只出现在资源任务或移交登记里。
- [源应用声明 supportsRtl=true 时保留逻辑方向：start/end 边距写 LengthMetrics 的 start/end，AutoMirrored 图标加 matchTextDirection(true)](lesson-786a04847bf10d364d9d.lesson.md)
  - 时机：规格提取与界面实现阶段，为声明 supportsRtl=true 的源应用转换 start/end 边距与自动镜像图标时
  - 情境：源 Manifest 声明 android:supportsRtl="true"；Compose 用 padding(start/end)、Icons.AutoMirrored.*（或 autoMirrored=true 的矢量），View 用 marginStart/End、paddingStart/End；应用含 RTL 语言资源或可能在 RTL 系统语言下运行；转换者准备写 left/right，把返回箭头等方向性图标转成普通 Image；页面规格可能没有携带 RTL 契约，资源映射可能把自动镜像图标当普通媒体。
  - 例外：源 Manifest 未声明 supportsRtl：布局恒 LTR，按显式固定 LTR 的做法处理
- [视觉修复以源布局与源码分支为准：截图尺寸差先折算成 vp 对照，容器尺寸与自绘组件的绘制尺寸同源修改，截图里缺少的入口先查渠道与开关分支，截图里的元素先对应到所属组件，文档截图与 @Preview 示例不当应用真值](lesson-8119d8bf0b58e4daac24.lesson.md)
  - 时机：视觉校验与修复阶段，根据截图差异撰写工单，决定修改固定尺寸、列数、背景，删减截图中没有出现的入口与区块，或按基线截图选定空态等文案与图标时；按差异单调整包裹自绘组件（Canvas 日历等）的容器高度与折叠范围时；按参考截图补齐无数据空态、决定截图中某段文案归属哪个组件时
  - 情境：依据截图或视觉差异单修改页面尺寸、可见入口、文案或图标；基线可能跨设备密度、渠道或运行状态，也可能来自docs/assets或@Preview。页面含Canvas自绘组件时，外层高度、clip和折叠范围还可能依赖绘制端的行高等尺寸。 也包括按参考截图为无数据状态补边框、图例与“暂无数据”类文案：页面由图表 Canvas 与相邻侧栏列表等并列组件组成，截图里的文案在源图表代码中没有绘制逻辑。
- [页面转换逐项落实源 XML 的 gone 节点（代码只绑点击、没有设为可见的入口也不渲染）、固定尺寸点击容器与 tools:listitem 行布局](lesson-f1a98587fe72ff68c5a8.lesson.md)
  - 时机：页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时；迁移标题栏或工具栏图标按钮并决定是否显示时
  - 情境：源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。 也包括 Activity 对 visibility=gone 的标题栏图标 findViewById 并绑定跳转（如打开搜索页），全文没有 setVisibility(VISIBLE)；目标工程其他页面已有同类入口的现成写法。也包括页面声明并在更新函数中维护某个展示状态（如倍速文本），build 中却没有消费它的组件。也包括 gone 的结果标题行容器：Activity 只改它子控件的文案或可见性，从不让容器本身可见；合成 view.xml 列出了该节点却没有 visibility 属性。
