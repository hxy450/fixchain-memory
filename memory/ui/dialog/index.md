# ui/dialog

弹窗与半模态：V2 页面可用的弹窗载体、源端真弹窗不以页面叠层充当、sheet 内二级弹窗的层级、从半模态内压入页面时的 SheetMode 与 targetId、按源 Dialog 类型选择呈现形态（路由约束不改变弹窗形态）、弹窗内二级选择器的层级、按源布局还原弹窗内容、源 Dialog 用 setView 注入自定义内容时的承载方式，页内对话框的打开触发点；源端委托共享详情弹窗与分享弹层时复用目标共享组件，依附式弹窗的宿主页归属，自绘底部弹窗改 bindSheet 时的手势门禁（含列表的下拉关闭）；多个独立底部弹层的绑定节点，展开后才加载数据的弹层；页内覆层承载 Activity 级 Dialog 时的挂载层级与按钮行定高；锚定下拉（PopupWindow showAsDropDown）的弹出容器，同页多个工具面板逐个选择形态

[上一级](../index.md)

## 本级经验

- [@ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)
  - 时机：界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）
  - 情境：项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。
- [PopupWindow 以 showAsDropDown 锚定弹出的自定义下拉，用锚点弹出按源布局还原：不换成原生 Select、系统菜单或整页筛选视图](lesson-666a746081ba1e447322.lesson.md)
  - 时机：界面实现阶段，为筛选栏、排序栏等下拉选项选择 ArkUI 弹出容器、呈现位置与菜单样式时
  - 情境：源端点击筛选项后用 PopupWindow 加载自定义布局（固定宽度、固定行高、箭头图、勾选图标），以 showAsDropDown 锚定在触发器或置顶筛选栏下方原位展开；同页可能另有整屏的“更多筛选”面板；目标有现成的 Select 组件或已写好的整页筛选组件可用。
- [从 bindSheet 半模态里打开的弹窗必须叠在 sheet 之上：不用页内浮层，居中点外可关用模态内自绘遮罩](lesson-009212ca2c691b97d76c.lesson.md)
  - 时机：界面实现阶段，为从底部 sheet 内部触发的二级弹窗（定时、新建输入等）选择承载层时
  - 情境：Android 在 BottomSheetDialog 内再 show 居中 DialogFragment（点外可关）；目标底部弹层用 bindSheet；二级弹窗候选有页内 Stack 条件浮层、bindSheet(CENTER)、bindContentCover 与全局自定义弹窗。
- [会从半模态内压入 Navigation 页的弹层用 SheetMode.EMBEDDED 并传宿主 targetId，不照搬选择器模板的 OVERLAY](lesson-97bf3cf56f55715f7e42.lesson.md)
  - 时机：界面实现或弹窗改造阶段，把页面内弹层改成 bindSheet/openBindSheet 系统半模态、确定 SheetMode 与挂载节点时
  - 情境：弹层内条目会通过 Navigation/NavPathStack 压入新页面（如节日详情、订阅详情），要求跳转时不关闭弹层、新页面盖住弹层、返回后弹层仍在；目标用 UIContext.openBindSheet 或基于它的弹窗库（如 showBindSheet），手头参考的是不从弹层内跳页的选择器类半模态模板。
  - 例外：弹层内只有选择或确认、不会打开页面，或产品允许跳转前先关闭弹层
- [依附式弹窗（AttachPopup）的宿主按锚点视图所在页面确定：提示挂在锚点页、按锚点实测坐标定位，弹出条件包含锚点可见](lesson-29f62d177a17d08b4e4f.lesson.md)
  - 时机：迁移审计与实现阶段，判定依附式弹窗的宿主归属、改写触发它的子页逻辑时
  - 情境：源端弹窗由子 Fragment 触发 show，但 atView 是父 Fragment 标题栏里的按钮，且只在该按钮可见、一次性标记未写入时显示；目标端已有一个画在子页内部、按固定边距定位的同文案浮层。
- [多个相互独立的底部弹层不在同一组件上链式 bindSheet：分别挂到不同节点，或用一个 bindSheet 按类型切换内容](lesson-b661a3a6a4c0a1e2a3c9.lesson.md)
  - 时机：界面实现阶段，把源页面并列的多个底部弹窗映射为 ArkUI bindSheet、安排绑定节点时；修复“点击后弹层不出现”时
  - 情境：源页面并列存在两个及以上由各自 visible 状态控制的底部弹窗（如规格选择与优惠券）；目标页面用 @Local 状态加 bindSheet 实现，并把它们写在同一个容器的修饰链上。
- [按源弹层类型逐个选呈现形态：居中 CustomDialog 用居中卡片，底部面板才用 bindSheet，锚定菜单按锚点弹出；形态不同的面板不共用一个弹窗；定长密码框输满即校验](lesson-21db515a505be4845497.lesson.md)
  - 时机：页面接线与界面实现阶段，为源端 DialogHelper 一类函数弹出的确认或输入弹窗选择承载形态与校验触发方式时；对齐同页多个工具面板（如阅读页的设置、更多、发弹幕）的容器、锚点与交互步骤时
  - 情境：源端经 CustomDialog/AlertDialog 加自定义布局弹出居中卡片，卡内可能有定长格子密码框（输满即比对、失败提示），根视图点击关闭；目标公共弹窗封装只有确认/提示类，带输入的弹窗需要在页面内自建。 也包括源端同页多个工具面板容器各不相同（底部 PopupWindow 面板、锚定在标题栏右上角带箭头的弹出菜单、先编辑再在内容上拖动定位的多步弹层），目标现有实现用一个固定高度、带拖动条与关闭按钮的 bindSheet 承载全部面板。
- [源弹窗按它实际加载的布局 XML 与函数全文逐控件还原，不以行为代码、相邻弹窗外壳或通用确认弹窗代替](lesson-1f366fe4ccdc917ce0fc.lesson.md)
  - 时机：界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时
  - 情境：源弹窗由 ViewBinding/inflate 或工具类加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。也包括源确认区是带形状背景、可点击的复合容器（勾选控件＋主文案＋小字号次文案），目标准备复用只收单个文字 label 的主题按钮 builder，或用一个共享弹窗组件承载普通、严格等多个变体。
- [源确认框用 setView 注入复选框等自定义内容时改用自定义弹窗承载，不写成 AlertDialog.show 的 builder 参数](lesson-18fca50f9c801cb282ec.lesson.md)
  - 时机：界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时
  - 情境：源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。
  - 例外：源对话框只有标题、正文与按钮，没有自定义视图，此时直接映射 AlertDialog.show
- [源端 XPopup/DialogFragment 真弹窗（居中、锚点、底部）迁成可关闭的系统弹窗或半模态，不以页面可见性叠层充当](lesson-368c4592e4c7075c1871.lesson.md)
  - 时机：迁移实现、弹窗恢复与宿主接线阶段，为 Android 真弹窗（DialogFragment、XPopup Center/Attach/Bottom 类）确定 ArkUI 承载形态，或为已有弹窗补触发、宿主、去掉路由时
  - 情境：源端通过 DialogFragment、XPopup CenterPopupView/AttachPopupView 等在当前 Activity 上弹出提示、升级、菜单或锚点气泡，点击遮罩或返回即关闭；目标工程里已有以 @Local visible/visibility 或 if 条件渲染的 Stack + 遮罩叠层，或派工只写“接到现有弹窗”“恢复可关闭的页面内弹层”。也包括源弹窗继承 BottomPopupView 一类底部弹窗基类，计划或决策已写明映射到 showBindSheet/系统半模态，而现有实现是 NavDestination 路由页或由 @Param 可见性驱动、内嵌在宿主页的全屏 Stack（自绘遮罩、PanGesture 下拉关闭、返回信号参数）。
  - 例外：项目决策明确采用页内浮层，且浮层已实现遮罩点击、返回键与页面离开关闭并只回调一次
- [源端在当前页 show 的底部弹窗保持叠在宿主页上：“路由统一用某框架”只约束页面跳转，不把弹窗改成路由页](lesson-7ef02de8bbc10734c3d2.lesson.md)
  - 时机：规格提取阶段把 Android Dialog/BottomSheet 的呈现方式映射到 ArkUI 承载方式时；界面实现阶段落实弹窗内的二级日历或选择弹层时
  - 情境：Android 入口经 bottomDialog/Dialog 在当前 Activity 上 show 全宽底部面板（遮罩下仍见宿主页、点背景关闭、不入返回栈），面板内再弹同类底部选择器；目标工程有“路由统一使用 HMRouter/Navigation”的约束，且已有同名路由页可复用。
- [源端弹窗展开后才加载数据时，先打开弹层再在弹层内异步加载，带加载中与失败重试](lesson-5f8833721d3c4a11c60a.lesson.md)
  - 时机：界面实现与修复阶段，为需要网络数据的底部弹层或弹窗确定数据加载时机时
  - 情境：源端弹窗的数据请求放在展开回调里（如 Compose 弹窗的 onExpanded 调用 loadXxx），失败可在弹窗内重试；目标准备在页面初始化时预取，或在打开弹层前 await 网络。
- [源端把入口委托给跨页面共享组件（详情弹窗、公共分享弹层）时，目标检索并复用同职责的共享组件，不保留页内副本](lesson-6d3ac9a5c0382377b91e.lesson.md)
  - 时机：功能实现与审计阶段，接线页面中调用源端共享组件（XxxDialog.show、公共分享弹层）的入口，并决定这些入口背后的动作由谁实现时
  - 情境：源端列表项点击或按钮调用跨页面共享的对话框或弹层（带实体键参数），分享走公共底部分享弹层；目标工程已有同名或同职责的共享组件及其宿主接线，当前页面里却有一份自绘副本，副本中的部分动作尚未接通。
  - 例外：源端该入口本身是页面私有实现，没有委托给共享组件
- [用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，按钮行先定高再让分隔线撑满](lesson-0a26e0cfc44a183d3a02.lesson.md)
  - 时机：界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级与卡片、按钮行的高度约束时
  - 情境：源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，布局是固定宽、wrap_content 高的卡片，按钮行内有 layout_height=match_parent 的竖分隔 View；触发按钮位于 Tabs 子页或嵌套组件内。
  - 例外：改用 openCustomDialog、bindSheet 等系统弹窗 API 时，全窗遮罩由系统窗口负责，按真弹窗写法处理
- [自绘底部弹窗改成 bindSheet 时迁移原手势门禁：含列表的面板按手势起点是否在顶部决定下拉关闭，不照搬无列表模板的无条件 dismiss](lesson-f35f4912277e0c9a1b14.lesson.md)
  - 时机：弹窗改造阶段，把页面内自绘底部弹窗替换为系统 bindSheet/showBindSheet、配置 SheetOptions 与内部滚动时
  - 情境：旧的自绘面板含可滚动 List，用 PanGesture 记录手势起点是否在列表顶部，只有在顶部才跟手下拉、达阈值关闭、否则回弹；参考的现有 Sheet 模板是无列表的固定高度选择器，onWillDismiss 无条件关闭。
  - 例外：面板内没有可滚动内容，下拉关闭不需要与列表滚动区分
- [页内对话框的可见性状态逐一落实打开触发点：卡片整体点击与卡内关闭按钮分开实现，留给后续任务的触发点要登记](lesson-f0d5a447e645bc253019.lesson.md)
  - 时机：界面转换与页内接线阶段，把源页面中可点击的卡片、按钮及其打开的页内对话框转换为 ArkUI 触发器与可见性状态时
  - 情境：源端 Compose Card 以 Modifier.clickable 打开对话框，卡内另有关闭或忽略按钮；目标以 @Local 可见性标志加 @Builder 覆盖层实现页内对话框，部分处理器以前向占位留给后续切片；页面规格的导航关系表列出“触发 → 对话框”。
