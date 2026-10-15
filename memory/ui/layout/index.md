# ui/layout

页面几何与层级：按约束定位、尺寸与边距、滚动区域、运行时覆盖层选择分支；通用页面结构（源 XML 节点、gone 容器与工具栏菜单项的逐项落实，AppCompat 下菜单溢出与返回箭头）、视觉修复依据与未声明 supportsRtl 时的容器布局方向留在本级；声明 supportsRtl 时 start/end 边距与自动镜像图标保留逻辑方向

[上一级](../index.md)

## 子主题

- [constraints](constraints/index.md) — ConstraintLayout/RelativeLayout的锚点、叠放与默认对齐（含 Compose Column/Row 的默认对齐），Compose Box 子项在 Stack 中的定位，基线对齐与逐行内距的 Row 组，及ArkUI容器中的子项定位。
- [layers](layers/index.md) — 运行时addView、全屏底层、状态覆盖层与 BottomSheetBehavior 管理的布局内面板：确定视图挂在哪里、如何叠放及几何范围；点击命中与事件时坐标属于ui/interaction。；Box 中贴底栏在 Stack 中的锚定，页面级全屏遮罩与一次性动效层的条件挂载。
- [scrolling](scrolling/index.md) — ScrollView/NestedScrollView 与 weight 剩余区列表的滚动范围（固定头部留在外、剩余区空态居中）、LazyRow/横向滚动行的交叉轴尺寸、Lazy 列表 contentPadding 的内容偏移、带高度上限的滚动卡片、连续折叠顶栏与滚动区内跟随等高；可滚动视图（ScrollView、GridView/ListView）越界效果与滚动条的平台默认值（IF_CONTENT_SCROLLS、进页先亮再淡出）；LazyRow 摘要行转可横滑容器，程序滚动到某项的对齐方式（animateScrollToItem → ScrollAlign.START）
- [sizing](sizing/index.md) — 宽高、比例、百分比与边距的组合（父尺寸减边距、占剩余空间，由内容定尺寸的父级里的百分比），Compose 修饰符链顺序与 Row 的测量顺序、固有高度，Material 按钮的布局占位与实绘尺寸，px 域整数布局公式与随进度收放的间距，以及随内容定尺寸的图片、背景和描边，以及非 Row/Column/Flex 父级中 layoutWeight 不生效时的显式尺寸；嵌入满高子组件时的剩余高度分配，居中的 wrap_content 子项组不被拉伸。；换容器（Tabs、Grid 槽位改自绘 Row）后子项的主轴尺寸，TableLayout 按内容测量的列宽

## 本级经验

- [supportsRtl 应用保留逻辑方向：边距用 LengthMetrics 的 start/end，自动镜像图标加 matchTextDirection](lesson-786a04847bf10d364d9d.lesson.md)
  - 时机：规格提取与界面实现阶段，为声明 supportsRtl=true 的源应用转换 start/end 边距与自动镜像图标时
  - 情境：源 Manifest 声明 android:supportsRtl="true"；Compose 用 padding(start/end)、Icons.AutoMirrored.*（或 autoMirrored=true 的矢量），View 用 marginStart/End、paddingStart/End；应用含 RTL 语言资源或可能在 RTL 系统语言下运行；转换者准备写 left/right，把返回箭头等方向性图标转成普通 Image；页面规格可能没有携带 RTL 契约，资源映射可能把自动镜像图标当普通媒体。映射参考的边距示例可能是纯数字 margin({ end: 10 })，含 start/end 键的边距对象写数字会编译报 Type 'number' is not assignable to type 'LengthMetrics'。
  - 例外：源 Manifest 未声明 supportsRtl：布局恒 LTR，按显式固定 LTR 的做法处理
- [截图缺少源码中存在的入口、区块，或列数、背景、文案与源码不同时，先查运行分支与调用链，不按单张截图删改](lesson-815118d5bdb7a05cdc66.lesson.md)
  - 时机：视觉校验与修复阶段，按截图删减其中没有出现的 tab、入口或区块，调整列数、背景，或按文档截图、@Preview 选定空态等文案与图标时
  - 情境：源码布局里存在、且有点击逻辑的入口或区块在截图中缺失，或截图的列数、背景、文案与源码不一致；Fragment/Activity 可能按渠道（getChannel）、会员、开关或运行状态切换可见性与数据；截图可能只来自一种运行变体，也可能来自 docs/assets 或 @Preview 示例。
  - 例外：源码确认该入口已下线（无可达分支、无点击逻辑）时，按源码删除
- [按参考截图补元素前先把它归属到具体组件：当前组件源码没有其绘制逻辑时转查相邻组件，不在 Canvas 里自行补画](lesson-b04dfc0158b66f6544d5.lesson.md)
  - 时机：界面实现或视觉修复阶段，按参考截图补齐无数据空态、提示文案等元素，决定它归属哪个组件时
  - 情境：页面由图表 Canvas 与相邻侧栏、列表等并列组件组成；截图里出现的文案（如“暂无数据”）在正在修改的组件源码中只被赋值、没有绘制或消费逻辑；用户文字可能只列出部分要补的元素。
- [按截图或视觉差异单修改固定尺寸前，先按两端密度把差异折算成 vp，与源布局值、目标当前值三方对照](lesson-8119d8bf0b58e4daac24.lesson.md)
  - 时机：视觉校验与修复阶段，根据双端截图差异撰写尺寸类工单，或决定修改页面固定高度、间距、图片尺寸时
  - 情境：Android 基线截图与目标截图来自不同设备（密度、逻辑宽度不同），差异单写“主内容偏小/上移”一类观感结论；目标页的固定高度、margin 可能已等于源布局 dp 值，并与底栏共享有限纵向空间。
  - 例外：差异涉及自绘组件外层容器的高度、裁剪或折叠范围时，按自绘尺寸与容器同源修改的规则处理
- [源 manifest 未声明 android:supportsRtl 时布局方向恒为 LTR：有顺序或对齐语义的容器逐个显式 Direction.Ltr](lesson-148a3e67bd557bafd722.lesson.md)
  - 时机：规格提取与界面实现阶段，为带多语言资源的应用确定布局方向契约，新建按钮条、对话框面板等有顺序或起止对齐语义的容器时（含返修中用自绘面板替换系统弹窗）
  - 情境：AndroidManifest 的 &lt;application&gt; 未声明 android:supportsRtl（安卓布局方向恒为 LTR）；应用含 fa 等 RTL 语言资源，或可能在 RTL 系统语言下运行；目标用 Row/Column 等容器实现按钮条、对话框或起始对齐的内容，未设 direction。
  - 例外：源端声明 android:supportsRtl="true"：按源布局的 start/end 语义让容器随语言方向翻转
- [源布局有 layout-land、layout-sw&lt;N&gt;dp 等同名变体时逐控件对照各变体，在承载组件内按对应配置条件分支（ArkUI 没有布局资源限定词）](lesson-c8e645a542254d96997e.lesson.md)
  - 时机：界面实现阶段，合并 layout 与 layout-land 变体，或实现替代带变体 fragment 的共享组件时；计划与派工阶段指派变体实现时
  - 情境：源 res/layout-land/、layout-sw600dp/ 等目录下有同名变体，控件的 background、weight、margin、textSize 或整体结构与默认布局不同；Activity 代码在运行时只对部分控件 setBackgroundResource；布局由另一任务的共享组件承载，派工只写默认结构，变体要求只出现在资源任务或移交登记里。
  - 例外：变体之间只有 values-* 中的尺寸、颜色等值不同而布局结构相同时，按资源值的限定词覆盖规则处理
- [源用 Theme.Holo 等框架主题提供的 ActionBar 时，按 SDK 平台资源写外观契约，并做成多页共享的标题栏组件](lesson-b3372bd24373e70e4485.lesson.md)
  - 时机：规格提取与页面实现阶段，为框架主题（Theme.Holo/Material/DeviceDefault，未用 NoActionBar 或 FEATURE_NO_TITLE）提供的 ActionBar 自绘目标标题栏时
  - 情境：ActionBar 是主题提供的窗口装饰，不在布局 XML 中；页面调用 setDisplayHomeAsUpEnabled、manifest 声明 android:icon、菜单带 showAsAction；目标用 hideTitleBar 自绘标题栏，多个页面需要同一外观并可能并行转换。
  - 例外：源主题为 AppCompat/MaterialComponents 的 ActionBar 或自建 Toolbar 时，取值来自对应依赖库的样式，不取框架平台资源
- [自绘工具栏导航图标按实际生效者判定：DrawerToggle 接管同一 Toolbar 时画汉堡，有 parentActivityName 时默认显示 Up](lesson-a6121cc7eaf207b702f7.lesson.md)
  - 时机：规格提取与界面实现阶段，自绘 ActionBar 代体或标题栏、决定导航图标是返回箭头、汉堡还是不画时；复用模板或兄弟页标题栏时
  - 情境：判断导航图标的输入：Activity 主题是否带窗口 ActionBar；Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data；代码是否调用 setDisplayHomeAsUpEnabled(true/false)，onOptionsItemSelected 是否处理 android.R.id.home；基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState（布局根常为 DrawerLayout + NavigationView）。目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。
  - 例外：主题为 NoActionBar 且自建 Toolbar 时，按 setSupportActionBar 之后对该 Toolbar 的调用（setNavigationIcon、setDisplayHomeAsUpEnabled、DrawerToggle）判断
- [菜单项按生效的 showAsAction 分流到图标位或溢出：AppCompat 只读 app:showAsAction](lesson-43bf296f09f756b24a55.lesson.md)
  - 时机：界面实现阶段，把选项菜单 XML（onCreateOptionsMenu 中 inflate 的 menu）转到自绘标题栏或工具栏，决定哪些项进图标位、哪些进溢出菜单、是否显示文字时
  - 情境：源菜单项带 icon 与 showAsAction=ifRoom/always/never/withText，或带 checkable=true；Activity 可能基于 AppCompat，而菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"）；也可能是框架 ActionBar（Theme.Holo 等），读 android:showAsAction。
  - 例外：菜单项由代码 MenuItem.setShowAsAction 设置时，以代码设置的值为准
- [页面转换按源 XML 初始可见性与全部 setVisibility 决定节点是否渲染：gone 且从未设为可见的不生成，invisible 保留占位](lesson-f1a98587fe72ff68c5a8.lesson.md)
  - 时机：页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构时；迁移标题栏或工具栏图标按钮、结果标题行等并决定是否显示时
  - 情境：源布局含 visibility=gone/invisible 的标题、图标按钮或容器；Activity 对 gone 的图标 findViewById 并绑定点击，全文没有 setVisibility(VISIBLE)，或只改它子控件的文案与可见性、从不让容器本身可见；迁移用的页面快照可能是合成的，把 gone 节点列为可见文本或缺少 visibility 属性；目标工程其他页面已有同类入口的现成写法。
  - 例外：源端在不同状态分支里切换该节点的可见性时，按状态切换的显隐规则逐分支迁移
