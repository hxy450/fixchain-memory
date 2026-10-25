# ui/dialog

弹窗：V2 页面可用的弹窗载体、源端真弹窗不以页面叠层充当、按源 Dialog 类型选择呈现形态（路由约束不改变弹窗形态）、弹窗内二级选择器的层级、按源布局还原弹窗内容、源 Dialog 用 setView 注入自定义内容时的承载方式，ComponentContent 弹窗回调的取值时机，源端每次调用新建的对话框按调用独立实例，页内对话框的打开触发点；源端委托共享详情弹窗与分享弹层时复用目标共享组件，依附式弹窗的宿主页归属，展开后才加载数据的弹层；页内覆层承载 Activity 级 Dialog 时的挂载层级与按钮行定高；锚定下拉（PopupWindow showAsDropDown、框架 ActionBar 溢出面板，含子菜单箭头与标题头）的弹出容器，同页多个工具面板逐个选择形态；源端应用内分享面板的形态与逐渠道映射，第三方 Helper 按配置对象渲染的弹窗；页内遮罩承载对话框时的无障碍模态（显示期间隐藏背景）；弹窗外观与窗口几何、半模态 bindSheet 见子主题；Compose DropdownMenu、cascade 级联与居中 Popup 菜单的锚点、遮罩与原地切层

[上一级](../index.md)

## 子主题

- [appearance](appearance/index.md) — 弹窗外观与窗口几何：只靠平台默认外观的 AlertDialog 的可见契约与按钮角色槽位，MaterialAlertDialog 按主题代际的卡片外观与遮罩，三方库或 Dialog 主题决定的窗口宽度公式与遮罩、点外关闭、底色圆角，非全屏窗口下 openCustomDialog 的遮罩与状态栏，bindPopup 气泡的整体着色
- [sheets](sheets/index.md) — 半模态 bindSheet：BottomSheetDialogFragment 的高度档与外壳参数，一个页面挂多个弹层的绑定节点，从半模态内打开的二级弹窗（层级与高度上限）与压入页面（SheetMode、targetId），自绘底部弹窗改 bindSheet 时的手势门禁；Compose ModalBottomSheet（skipPartiallyExpanded）的高度档

## 本级经验

- [@ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)
  - 时机：界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）
  - 情境：项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。
- [ComponentContent 构造即执行 builder：构造后才赋值的回调以延迟调用传入](lesson-1c27b6c7cf05c05733d9.lesson.md)
  - 时机：界面实现阶段，用 ComponentContent 加 wrapBuilder 加 openCustomDialog 封装弹窗并接线关闭、确认回调时
  - 情境：关闭回调需要构造后才得到的 content 句柄，只能在 new ComponentContent(...) 之后赋给 args；内容组件以 @Param 接收回调。
- [Compose DropdownMenu、cascade 级联菜单与居中 Popup 菜单按源形态还原：锚定或居中、无变暗遮罩、子菜单在同一菜单内原地切层](lesson-b1006cf9981e5ff9bb2d.lesson.md)
  - 时机：规格映射与界面实现阶段，为 Compose 下拉菜单、级联子菜单、居中操作菜单与偏好行的下拉菜单确定弹出形态时
  - 情境：源端用 Material3 DropdownMenu、me.saket.cascade CascadeDropdownMenu、基于 Popup 的居中级联菜单或 compose-preference 的 DROPDOWN_MENU：菜单放在触发按钮所在 Box 内锚定弹出或屏幕居中弹出，不带变暗遮罩，点外与返回关闭，带 children 的项在同一菜单内切换到子层并有返回 Header；目标用 bindMenu 或自绘层。
- [从组件外的共享函数打开自定义弹窗时，用 wrapBuilder + ComponentContent 交给 openCustomDialog(content)：不在 options.builder 闭包里直接调用全局 @Builder](lesson-a3ac761b0d52a6bccb9f.lesson.md)
  - 时机：界面实现阶段，把路由页改成多个入口复用的自定义弹窗，确定弹窗内容的构建与挂载方式时
  - 情境：ArkTS V2（@ComponentV2）工程中，把 BottomSheetDialog/DialogFragment 一类弹窗迁成 UIContext.getPromptAction().openCustomDialog，并打算从组件外的导出函数（只持有 UIContext）为多个页面统一打开同一个自定义组件。
- [依附式弹窗（AttachPopup）的宿主按锚点视图所在页面确定：提示挂在锚点页、按锚点实测坐标定位，弹出条件包含锚点可见](lesson-29f62d177a17d08b4e4f.lesson.md)
  - 时机：迁移审计与实现阶段，判定依附式弹窗的宿主归属、改写触发它的子页逻辑时
  - 情境：源端弹窗由子 Fragment 触发 show，但 atView 是父 Fragment 标题栏里的按钮，且只在该按钮可见、一次性标记未写入时显示；目标端已有一个画在子页内部、按固定边距定位的同文案浮层。
- [按源弹层类型逐个选呈现形态：居中 CustomDialog/AlertDialog（含框架生成的 ListPreference 选项框：无确定钮、留 CANCEL）用居中卡片，底部面板才用 bindSheet，锚定菜单按锚点弹出；形态不同的面板不共用一个弹窗；定长密码框输满即校验](lesson-21db515a505be4845497.lesson.md)
  - 时机：页面接线与界面实现阶段，为源端 DialogHelper 一类函数弹出的确认或输入弹窗选择承载形态与校验触发方式时；对齐同页多个工具面板（如阅读页的设置、更多、发弹幕）的容器、锚点与交互步骤时
  - 情境：源端经 CustomDialog/AlertDialog 加自定义布局弹出居中卡片，卡内可能有定长格子密码框（输满即比对、失败提示），根视图点击关闭；目标公共弹窗封装只有确认/提示类，带输入的弹窗需要在页面内自建。也包括源端同页多个工具面板容器各不相同（底部 PopupWindow 面板、锚定在标题栏右上角带箭头的弹出菜单、先编辑再在内容上拖动定位的多步弹层），目标现有实现用一个固定高度、带拖动条与关闭按钮的 bindSheet 承载全部面板。也包括源端 MaterialAlertDialogBuilder（含 setView 输入、下拉）对话框，工程惯例或规格并列给出 bindSheet/CustomDialog。也包括 AlertDialog.Builder…setView(ListView) 的列表选择框被规格写成 bindSheet 半模态加 List；按钮的上下文菜单被写成锚定 bindPopup 或 bindMenu，丢了长按入口与标题图标。也包括 android.preference.ListPreference 的选项对话框：由框架生成的居中 AlertDialog，代码中看不到 Builder，规格却写成 Select 或 bindSheet。
- [源对话框带目标系统弹窗没有的槽位（setView 注入的复选框等自定义布局、Compose AlertDialog 的 icon）时改用自定义弹窗承载，不写成 AlertDialog.show 的参数，也不自行省略](lesson-18fca50f9c801cb282ec.lesson.md)
  - 时机：界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 或 Compose AlertDialog 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时
  - 情境：源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。也包括 Compose AlertDialog 传了 icon = { Icon(...) }，目标准备改用没有图标槽的 showAlertDialog/AlertDialog.show，并以“仅视觉降级”或“与兄弟页同模式”为由省略图标。
  - 例外：源对话框只有标题、正文与按钮，没有自定义视图或图标：可以映射 AlertDialog.show，但正/负键按角色核对目标槽位位置；项目要求一比一还原平台默认外观时改用自定义弹窗复刻
- [源弹窗按它实际加载的布局 XML、函数全文或依赖库模板逐控件还原并接通配置回调，不以行为代码、相邻弹窗外壳、通用确认弹窗或现成文案代替](lesson-1f366fe4ccdc917ce0fc.lesson.md)
  - 时机：界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时；用自绘弹层替代源端第三方 SDK 或 Helper 弹窗（隐私概要、协议弹窗），确定其内容分区、文案与操作区并接线交互回调时（含收口时重写弹窗正文或操作区）；规格提取阶段为这类库弹窗写验收条目与导航表时
  - 情境：源弹窗由 ViewBinding/inflate 或工具类加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。也包括源确认区是带形状背景、可点击的复合容器（勾选控件＋主文案＋小字号次文案），目标准备复用只收单个文字 label 的主题按钮 builder，或用一个共享弹窗组件承载普通、严格等多个变体。也包括源页通过 PrivacyDialogHelper.showXxx(PrivacyConfig{…}) 一类库调用弹出隐私概要：标题、权限说明条目与图标、勾选两态图、链接色、服务协议与隐私政策链接回调、拒绝回调都在配置对象里，弹窗布局不在页面 XML，页面规格与合成快照没有弹窗节点；依赖库坐标可能只写在 app/build.gradle，工程源码只有 import 与调用，生成期没有实机截图；参考规格可能只在页面结构描述里提到“协议链接”，验收条目没有对应项；目标 WebView 页已存在，协议 URL 提供者可能由后续切片负责。
- [源端 XPopup/DialogFragment 真弹窗（居中、锚点、底部）迁成可关闭的系统弹窗或半模态，不以页面可见性叠层充当](lesson-368c4592e4c7075c1871.lesson.md)
  - 时机：迁移实现、弹窗恢复与宿主接线阶段，为 Android 真弹窗（DialogFragment、XPopup Center/Attach/Bottom 类）确定 ArkUI 承载形态，或为已有弹窗补触发、宿主、去掉路由时
  - 情境：源端通过 DialogFragment、XPopup CenterPopupView/AttachPopupView 等在当前 Activity 上弹出提示、升级、菜单或锚点气泡，点击遮罩或返回即关闭；目标工程里已有以 @Local visible/visibility 或 if 条件渲染的 Stack + 遮罩叠层，或派工只写“接到现有弹窗”“恢复可关闭的页面内弹层”。也包括源弹窗继承 BottomPopupView 一类底部弹窗基类，计划或决策已写明映射到 showBindSheet/系统半模态，而现有实现是 NavDestination 路由页或由 @Param 可见性驱动、内嵌在宿主页的全屏 Stack（自绘遮罩、PanGesture 下拉关闭、返回信号参数）。 也包括 BottomSheetDialogFragment 被写成标准模式的 NavDestination 路由页，在页内自绘蒙层与底板，调用方随之 pushPathByName。也包括源端 BottomSheetDialogFragment 的宿主页在目标中嵌在壳内容区（标题栏、底部导航由外层提供），写者为回避同节点第二个 bindSheet 改用页内浮层。也包括 AlertDialog.Builder 构造、默认可取消的对话框，为满足“每个组件 @ComponentV2 导出”被写成自带蒙层的共享页内浮层，注释称覆盖返回键而实现只接蒙层点击。
  - 例外：项目决策明确采用页内浮层，且浮层已实现遮罩点击、返回键与页面离开关闭并只回调一次
- [源端在当前页 show 的底部弹窗保持叠在宿主页上：“路由统一用某框架”只约束页面跳转，不把弹窗改成路由页](lesson-7ef02de8bbc10734c3d2.lesson.md)
  - 时机：规格提取阶段把 Android Dialog/BottomSheet 的呈现方式映射到 ArkUI 承载方式时；界面实现阶段落实弹窗内的二级日历或选择弹层时
  - 情境：Android 入口经 bottomDialog/Dialog 在当前 Activity 上 show 全宽底部面板（遮罩下仍见宿主页、点背景关闭、不入返回栈），面板内再弹同类底部选择器；目标工程有“路由统一使用 HMRouter/Navigation”的约束，且已有同名路由页可复用。
- [源端应用内分享面板按交互形态复用目标的应用内分享弹层，并逐渠道映射（含发动态等 App 内渠道）；不以系统分享面板整体替代](lesson-b366cf7ae68525577f57.lesson.md)
  - 时机：规格提取、能力核对与功能实现阶段，为源端分享入口选定目标工程已有的分享能力，并把面板的各渠道接到目标入口时；按用户要求更换分享面板时
  - 情境：Android 源端用应用内分享面板（如 ShareUtil.shareImage 加 ShareItem 渠道列表，按 platformName 分发到 QQ 空间、动态、蓝牙等），其中可能有把截图带进 App 内发布页的渠道；目标工程同时有 systemShare 封装（ShareTool、ShareController）和应用内“分享至”Sheet 组件及微信、QQ 图片发送工具；需求要求复用现有能力，规格的依赖接缝可能已写明各渠道与承接页参数，验收条目却只写“分享截图”。
  - 例外：源端本身调用系统分享（Intent.ACTION_SEND、createChooser），或用户已确认改用系统面板并登记了这项 UX 差异
- [源端弹窗展开后才加载数据时，先打开弹层再在弹层内异步加载，带加载中与失败重试](lesson-5f8833721d3c4a11c60a.lesson.md)
  - 时机：界面实现与修复阶段，为需要网络数据的底部弹层或弹窗确定数据加载时机时
  - 情境：源端弹窗的数据请求放在展开回调里（如 Compose 弹窗的 onExpanded 调用 loadXxx），失败可在弹窗内重试；目标准备在页面初始化时预取，或在打开弹层前 await 网络。
- [源端把入口委托给跨页面共享组件（详情弹窗、公共分享弹层）时，目标检索并复用同职责的共享组件，不保留页内副本](lesson-6d3ac9a5c0382377b91e.lesson.md)
  - 时机：功能实现与审计阶段，接线页面中调用源端共享组件（XxxDialog.show、公共分享弹层）的入口，并决定这些入口背后的动作由谁实现时
  - 情境：源端列表项点击或按钮调用跨页面共享的对话框或弹层（带实体键参数），分享走公共底部分享弹层；目标工程已有同名或同职责的共享组件及其宿主接线，当前页面里却有一份自绘副本，副本中的部分动作尚未接通。
  - 例外：源端该入口本身是页面私有实现，没有委托给共享组件
- [源端每次调用都新建的对话框，目标按调用创建独立弹窗实例并只关闭自身，不收敛为单例句柄](lesson-4d577c6a9451bd996e78.lesson.md)
  - 时机：服务层或页面实现阶段，把源端封装的“请求输入/确认”类对话框方法（每次调用 new Builder()…show()）翻译成目标弹窗时
  - 情境：源端帮助方法每次调用都新建一个对话框并在其回调里交付结果；目标准备在服务单例里保存一个 ComponentContent 或弹窗控制器字段，新调用前先关闭旧弹窗再打开。
- [用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，按钮行先按源取值定高再让分隔线撑满（平台 AlertDialog 的按钮条取平台样式或实测，不默认 48vp）](lesson-0a26e0cfc44a183d3a02.lesson.md)
  - 时机：界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级与卡片、按钮行的高度约束时
  - 情境：源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，布局是固定宽、wrap_content 高的卡片，按钮行内有 layout_height=match_parent 的竖分隔 View；触发按钮位于 Tabs 子页或嵌套组件内。 也包括按钮由 AlertDialog.Builder 的 setPositive/Negative/NeutralButton 生成、源布局里没有按钮行，按钮条外观来自主题的平台对话框样式。
  - 例外：改用 openCustomDialog、bindSheet 等系统弹窗 API 时，全窗遮罩由系统窗口负责，按真弹窗写法处理
- [锚定弹出的下拉（PopupWindow showAsDropDown 自定义下拉、框架 ActionBar 的溢出面板）按源样式与源主题锚定方式还原（Material 溢出面板盖住标题栏），遮罩与面板放同一承载层：不换成原生 Select、系统 Menu 或整页筛选视图](lesson-666a746081ba1e447322.lesson.md)
  - 时机：界面实现阶段，为筛选栏、排序栏等下拉选项选择 ArkUI 弹出容器、呈现位置与菜单样式时；为工具栏溢出菜单（showAsAction=never 或未上栏的项）选择承载方式、锚定位置与外观时；把页内浮层（锚定面板与点外关闭层）搬进共享标题栏等组件时
  - 情境：源端点击筛选项后用 PopupWindow 加载自定义布局（固定宽度、固定行高、箭头图、勾选图标），以 showAsDropDown 锚定在触发器或置顶筛选栏下方原位展开；同页可能另有整屏的“更多筛选”面板；目标有现成的 Select 组件或已写好的整页筛选组件可用。 也包括源 Activity 用框架 ActionBar（Theme.Holo，或 values-v21 的 Theme.Material*），溢出菜单项由平台主题绘制的 ListPopupWindow 面板承载，源码里没有面板样式；目标准备用 ArkUI Menu/bindMenu，任务要求逐屏一致。 也包括溢出面板由共享标题栏组件绘制（组件节点内或 .overlay()），点外关闭的全幅捕获层按组件契约留给宿主页，声明在标题栏之后的兄弟层里。 也包括溢出项带 &lt;menu/&gt; 子菜单（如排序），目标把它做成独立单选面板。
- [页内对话框的可见性状态逐一落实打开触发点：卡片整体点击与卡内关闭按钮分开实现，留给后续任务的触发点要登记](lesson-f0d5a447e645bc253019.lesson.md)
  - 时机：界面转换与页内接线阶段，把源页面中可点击的卡片、按钮及其打开的页内对话框转换为 ArkUI 触发器与可见性状态时
  - 情境：源端 Compose Card 以 Modifier.clickable 打开对话框，卡内另有关闭或忽略按钮；目标以 @Local 可见性标志加 @Builder 覆盖层实现页内对话框，部分处理器以前向占位留给后续切片；页面规格的导航关系表列出“触发 → 对话框”。
- [页内遮罩承载源端对话框时，显示期间把背景内容移出无障碍树：accessibilityLevel('no-hide-descendants')](lesson-96eea0feeae116ef9262.lesson.md)
  - 时机：界面实现阶段，为源端独立窗口对话框选择承载方式，或按项目已有写法用页内 Stack 遮罩加卡片实现对话框时
  - 情境：源端对话框是独立窗口（Compose Dialog/AlertDialog、Android Dialog），读屏焦点限制在对话框内；目标以可见性状态在页面根 Stack 中条件渲染遮罩与卡片，背景页面仍在同一组件树；规格或共享弹窗组件头注可能已指定 openCustomDialog、@CustomDialog 等系统通道，兄弟页已有同款页内遮罩可参照。
  - 例外：使用 openCustomDialog、showAlertDialog、bindSheet 等系统弹窗通道：窗口级模态由系统提供
