# ui/dialog

弹窗：V2 页面可用的弹窗载体、源端真弹窗不以页面叠层充当、按源 Dialog 类型选择呈现形态（路由约束不改变弹窗形态）、MaterialAlertDialog 的 Material3 卡片外观与统一遮罩、只靠平台默认外观的 AlertDialog 的可见契约与按钮角色槽位、弹窗内二级选择器的层级、按源布局还原弹窗内容、源 Dialog 用 setView 注入自定义内容时的承载方式，ComponentContent 弹窗回调的取值时机，页内对话框的打开触发点；源端委托共享详情弹窗与分享弹层时复用目标共享组件，依附式弹窗的宿主页归属，bindPopup 气泡的整体着色，展开后才加载数据的弹层；页内覆层承载 Activity 级 Dialog 时的挂载层级与按钮行定高；锚定下拉（PopupWindow showAsDropDown）的弹出容器，同页多个工具面板逐个选择形态；半模态 bindSheet 见子主题；源端应用内分享面板的形态与逐渠道映射，第三方 Helper 按配置对象渲染的弹窗；页内遮罩承载对话框时的无障碍模态（显示期间隐藏背景）

[上一级](../index.md)

## 子主题

- [sheets](sheets/index.md) — 半模态 bindSheet：BottomSheetDialogFragment 与 Compose ModalBottomSheet 的高度档与外壳参数，一个页面挂多个弹层的绑定节点，从半模态或页内面板内再打开的二级弹窗的承载层，从弹层内压入页面（SheetMode、targetId），自绘底部弹窗改 bindSheet 时的手势门禁

## 本级经验

- [@ComponentV2 页面不用 CustomDialogController 承载弹窗，改用 openCustomDialog、半模态或状态驱动浮层](lesson-3f3e1ff0a4d0e0299bda.lesson.md)
  - 时机：界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）
  - 情境：项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。
- [ComponentContent 构造即执行 builder：构造后才赋值的回调以延迟调用传入](lesson-1c27b6c7cf05c05733d9.lesson.md)
  - 时机：界面实现阶段，用 ComponentContent 加 wrapBuilder 加 openCustomDialog 封装弹窗并接线关闭、确认回调时
  - 情境：关闭回调需要构造后才得到的 content 句柄，只能在 new ComponentContent(...) 之后赋给 args；内容组件以 @Param 接收回调。
- [MaterialAlertDialogBuilder 对话框转自绘卡片时，卡片宽度、圆角、底色、高度上限与遮罩按源主题代际与 material 库版本取值](lesson-39077e6612d5f97b0731.lesson.md)
  - 时机：界面实现与规格提取阶段，把 MaterialAlertDialogBuilder 对话框转换为 ArkUI 自绘卡片或弹层（含由转换器单独产出、呈现外壳留给后续切片的对话框组件），确定卡片宽度、圆角、底色、最大高度与遮罩时
  - 情境：应用主题继承 Theme.Material3.*（或 MaterialComponents），对话框由 MaterialAlertDialogBuilder 构建；目标用 openCustomDialog、bindSheet 或页内遮罩自绘，工程中有被当作族先例的卡片，可能登记了按 M2 推断的值。也包括对话框组件只负责内容、呈现外壳未定，组件没有自带高度上限。
- [PopupWindow showAsDropDown 自定义下拉按源布局在锚点下方原位还原，不换成原生 Select、系统 Menu 或整页筛选视图](lesson-666a746081ba1e447322.lesson.md)
  - 时机：界面实现阶段，为筛选栏、排序栏等用 PopupWindow 锚定弹出的下拉选项选择 ArkUI 弹出容器、呈现位置与样式时
  - 情境：源端点击筛选项后用 PopupWindow 加载自定义布局（固定宽度、固定行高、箭头图、勾选图标），以 showAsDropDown 锚定在触发器或置顶筛选栏下方原位展开；同页可能另有整屏的“更多筛选”面板；目标有现成的 Select 组件或已写好的整页筛选组件可用。
  - 例外：源端菜单是框架 ActionBar/Toolbar 的溢出菜单（showAsAction=never），而不是 PopupWindow 加载应用布局时，不适用本条，见 lesson-9694dd3b56dc6ce8164b
- [依附式弹窗（AttachPopup）的宿主按锚点视图所在页面确定：提示挂在锚点页、按锚点实测坐标定位，弹出条件包含锚点可见](lesson-29f62d177a17d08b4e4f.lesson.md)
  - 时机：迁移审计与实现阶段，判定依附式弹窗的宿主归属、改写触发它的子页逻辑时
  - 情境：源端弹窗由子 Fragment 触发 show，但 atView 是父 Fragment 标题栏里的按钮，且只在该按钮可见、一次性标记未写入时显示；目标端已有一个画在子页内部、按固定边距定位的同文案浮层。
- [只靠平台默认外观的 AlertDialog.Builder 对话框迁移前，按实际对话框主题从平台资源写出完整可见契约，按钮按角色核对槽位](lesson-9c4de55af3c1ecd8eaa4.lesson.md)
  - 时机：规格提取阶段为代码中 AlertDialog.Builder 构造的系统对话框写转换决策时，以及界面实现阶段按该决策落地 ArkUI 系统弹窗或自定义弹窗时
  - 情境：源码用 AlertDialog.Builder 内联构造确认框，只设 title、message、setPositiveButton、setNegativeButton（可有 setView），无自定义样式，外观由主题的平台默认警告框决定；目标准备用 ArkUI AlertDialog.show(primaryButton/secondaryButton) 等系统弹窗替代，项目要求与源端逐屏一致。也包括应用主题为 Theme.Holo 等框架主题，多个对话框共用同一平台外观；规格只写了“标题左对齐、负左正右、遮罩、cancelable”几项，各页写者凭记忆或兄弟页先例自绘面板。
  - 例外：项目明确接受目标系统弹窗的固有外观、只要求文案与按键行为一致；此时仍按角色核对按钮槽位；android.preference 偏好页弹出的 DialogPreference/ListPreference 对话框：外观契约同本条，按钮集合、内容布局与提交语义另按偏好框架默认推导，见 lesson-3f95e9d0ad81b3c431e9
- [同页多个工具面板逐个按源端容器类型、锚点与交互步骤实现：形态不同的面板不共用一个弹窗组件](lesson-21db515a505be4845497.lesson.md)
  - 时机：界面实现与对齐阶段，为同页多个工具面板（如阅读页的设置、更多、发弹幕）确定容器、锚点与交互步骤，或准备用一个共享弹窗组件承载多个面板时
  - 情境：源端同页多个工具面板容器各不相同（底部 PopupWindow 面板、锚定在标题栏右上角带箭头的弹出菜单、先编辑再在内容上拖动定位的多步弹层）；目标现有实现用一个固定高度、带拖动条与关闭按钮的 bindSheet 承载全部面板，或准备按类型切换内容合并成一个弹窗。
- [工程约定“路由统一用某框架”时，源端在当前页 show 的弹窗仍叠在宿主页上：路由约束只管页面跳转，不把弹窗改成路由页](lesson-7ef02de8bbc10734c3d2.lesson.md)
  - 时机：规格提取阶段把 Android Dialog/BottomSheet 的呈现方式映射到 ArkUI 承载方式、工程有路由统一约束时；实现阶段按这类规格落地弹窗时
  - 情境：Android 入口经 bottomDialog/Dialog 在当前 Activity 上 show 全宽底部面板（遮罩下仍见宿主页、点背景关闭、不入返回栈）；目标工程有“路由统一使用某路由框架（如 HMRouter）”的约束，且已有同名路由页可复用；规格援引该约束写成“用路由页承载等价弹层”。
  - 例外：规格选用路由页或独立窗口承载，且已确认该机制保留宿主页可见与点背景关闭、并在验收中写明对应检查时（见 how 第 2 步）
- [弹窗确认区是可点击的复合容器（勾选或图标加多行文案）时，整体转成复合按钮，不用只收单个 label 的按钮 builder](lesson-f7f9b40bf3d0e1b62d1f.lesson.md)
  - 时机：界面实现与收口阶段，转换弹窗里带点击事件、内含勾选控件或图标与多行文本的确认区，或用一个共享弹窗组件承载多个弹窗变体时
  - 情境：源确认区是带形状背景、可点击的 LinearLayout/Shape 容器（勾选控件＋主文案＋小字号次文案）；目标准备复用只收单个文字 label 的主题按钮 builder；或一个共享弹窗组件承载普通、严格等多个变体，只有某个变体有显式勾选状态；源端还可能在勾选后延时再回调。
- [按钮行里有 match_parent 高的竖分隔 View 时，先给按钮行定高再让分隔线撑满，不让未定高行里的 Stretch 子项决定卡片高度](lesson-2a07020daf9a7d8a60a3.lesson.md)
  - 时机：界面实现阶段，转换弹窗或卡片里的按钮行（按钮之间有 layout_height=match_parent 的竖分隔 View），确定行高与卡片高度约束时
  - 情境：源布局卡片为 wrap_content 高，按钮行由 wrap_content 按钮加 padding 构成，按钮之间的竖分隔 View 为 match_parent 高；目标准备给分隔线 alignSelf(ItemAlign.Stretch)，而按钮行本身不设高度，卡片放在覆盖整窗的遮罩容器里。也包括按钮由 AlertDialog.Builder 的 setPositive/Negative/NeutralButton 生成、源布局里没有按钮行，按钮条外观来自主题的平台对话框样式。
  - 例外：行位于 Scroll 等纵向无界容器内、子项要随最高兄弟等高时不按本条（本条针对上层有确定高度的弹窗卡片），按 lesson-cb1a12afca61db08ed9a 处理
- [整体着色的气泡用 bindPopup 的 popupColor，而不是只给内容加背景](lesson-05dc4eb9548bf3fef6ae.lesson.md)
  - 时机：界面实现阶段，把 Balloon、Tooltip 等带箭头的气泡迁移为 bindPopup 自定义 builder 时
  - 情境：源 setBackgroundColor 作用于整个气泡（含箭头），目标的箭头与外框由 popup 容器绘制。
- [源对话框有 setView 自定义布局或 icon 槽时改用自定义弹窗承载，不写进 AlertDialog.show 参数也不省略](lesson-18fca50f9c801cb282ec.lesson.md)
  - 时机：界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 或 Compose AlertDialog 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时
  - 情境：源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。也包括 Compose AlertDialog 传了 icon = { Icon(...) }，目标准备改用没有图标槽的 showAlertDialog/AlertDialog.show，并以“仅视觉降级”或“与兄弟页同模式”为由省略图标。
  - 例外：源对话框只有标题、正文与按钮，没有自定义视图或图标：可以映射 AlertDialog.show，但正/负键按角色核对目标槽位位置；项目要求一比一还原平台默认外观时改用自定义弹窗复刻
- [源弹窗由依赖库按配置对象（如 PrivacyConfig）渲染时，版面取自库模板，配置里的每个回调逐项接到目标控件](lesson-afc5868d6c1a6dec04fa.lesson.md)
  - 时机：界面实现与收口阶段，用自绘弹层替代源端第三方 SDK 或 Helper 渲染的弹窗（隐私概要、协议弹窗），确定分区、文案与操作区并接线回调时（含收口时重写弹窗正文或操作区）；规格提取阶段为会弹出这类库弹窗的页面写验收条目与导航表时
  - 情境：源页通过库调用加配置对象弹窗：标题、权限说明条目与图标、勾选两态图、链接色、服务协议与隐私政策链接回调、同意与拒绝回调都在配置对象里，弹窗布局不在工程 XML，页面规格与合成快照没有弹窗节点；依赖库坐标可能只写在 app/build.gradle，工程源码只有 import 与调用；参考规格可能只在页面结构描述里提到“协议链接”；目标 WebView 页已存在，协议 URL 提供者可能由后续切片负责。
- [源弹窗由独立布局 XML 或弹窗工具函数加载时，按实际布局与函数全文逐控件还原，不以行为代码、相邻弹窗外壳或通用确认弹窗代替](lesson-1f366fe4ccdc917ce0fc.lesson.md)
  - 时机：界面转换与接线阶段，为源端弹窗编写或补建 ArkUI 弹窗内容（包括解接线标记时顺带新建弹窗、补齐流程闭环时新建弹窗、考虑复用通用弹窗）时；规格提取阶段整理页面弹窗清单时
  - 情境：源弹窗由 ViewBinding/inflate 或工具类（如 DialogHelper.showXxx）加载独立布局（DialogXxxBinding.inflate、R.layout.xxx），含标题、关闭图标、专用图标、说明文字、输入框、单个或多个按钮及容器级 margin；目标工程已有“标题 + 确定/取消”的通用确认弹窗或相邻弹窗写法可参照，或只拿到“展示、复制、关闭”一类功能描述。
  - 例外：源弹窗由依赖库按配置对象渲染、工程里没有布局文件时按 lesson-afc5868d6c1a6dec04fa 处理，不适用本条的逐控件对照
- [源端应用内分享面板（自定义渠道列表）按交互形态复用目标的应用内分享弹层并逐渠道映射，不以系统分享面板整体替代](lesson-b366cf7ae68525577f57.lesson.md)
  - 时机：规格提取、能力核对与功能实现阶段，为源端分享入口选定目标工程已有的分享能力，并把面板的各渠道接到目标入口时；按用户要求更换分享面板时
  - 情境：Android 源端用应用内分享面板（如 ShareUtil.shareImage 加 ShareItem 渠道列表，按渠道分发到各社交平台、动态、蓝牙等），其中可能有把截图带进 App 内发布页的渠道；目标工程同时有 systemShare 封装和应用内分享弹层组件及各渠道发送工具；需求要求复用现有能力，规格的依赖接缝可能已写明各渠道与承接页参数，验收条目却只写“分享截图”。
  - 例外：源端本身调用系统分享（Intent.ACTION_SEND、createChooser），或用户已确认改用系统面板并登记了这项 UX 差异
- [源端弹窗展开后才加载数据时，先打开弹层再在弹层内异步加载，带加载中与失败重试](lesson-5f8833721d3c4a11c60a.lesson.md)
  - 时机：界面实现与修复阶段，为需要网络数据的底部弹层或弹窗确定数据加载时机时
  - 情境：源端弹窗的数据请求放在展开回调里（如 Compose 弹窗的 onExpanded 调用 loadXxx），失败可在弹窗内重试；目标准备在页面初始化时预取，或在打开弹层前 await 网络。
- [源端把入口委托给跨页面共享组件（详情弹窗、公共分享弹层）时，目标检索并复用同职责的共享组件，不保留页内副本](lesson-6d3ac9a5c0382377b91e.lesson.md)
  - 时机：功能实现与审计阶段，接线页面中调用源端共享组件（XxxDialog.show、公共分享弹层）的入口，并决定这些入口背后的动作由谁实现时
  - 情境：源端列表项点击或按钮调用跨页面共享的对话框或弹层（带实体键参数），分享走公共底部分享弹层；目标工程已有同名或同职责的共享组件及其宿主接线，当前页面里却有一份自绘副本，副本中的部分动作尚未接通。
  - 例外：源端该入口本身是页面私有实现，没有委托给共享组件；目标共享件尚未就绪：按页内副本登记待收敛项的经验处理
- [源端真弹窗（DialogFragment、AlertDialog、XPopup、BottomSheet）按源类迁成系统弹窗或半模态，不用页面叠层或路由页](lesson-368c4592e4c7075c1871.lesson.md)
  - 时机：迁移实现、弹窗恢复与宿主接线阶段，为 Android 弹窗类（DialogFragment、AlertDialog/MaterialAlertDialogBuilder、XPopup Center/Attach/Bottom、BottomSheetDialog(Fragment)、上下文菜单）确定 ArkUI 承载形态时；规格把弹窗映射为路由页，或工程有“路由统一使用某框架”的约束时；为已有弹窗补触发、宿主、去掉路由时
  - 情境：源端通过 DialogFragment、AlertDialog、XPopup CenterPopupView/AttachPopupView 等在当前 Activity 上弹出提示、升级、菜单或锚点气泡，点击遮罩或返回即关闭；目标工程里已有以 @Local visible/visibility 或 if 条件渲染的 Stack + 遮罩叠层，或派工只写“接到现有弹窗”“恢复可关闭的页面内弹层”。也包括源弹窗继承 BottomPopupView 一类底部弹窗基类，计划已写明映射到 showBindSheet/系统半模态，而现有实现是 NavDestination 路由页或由 @Param 可见性驱动、内嵌在宿主页的全屏 Stack（自绘遮罩、PanGesture 下拉关闭）。也包括 MaterialAlertDialogBuilder 或 AlertDialog（含 setView 输入、下拉、ListView 列表）在规格里与 bindSheet 并列，或因“弹窗里有输入框”被改成半模态；按钮的上下文菜单被写成锚定菜单而丢了长按入口与标题图标。也包括 BottomSheetDialogFragment 被写成标准模式的 NavDestination 路由页，在页内自绘蒙层与底板，调用方随之 pushPathByName。
  - 例外：确需保留页内浮层（项目已定）时，同时交付遮罩点击、返回键与页面离开关闭且只回调一次，显示期间给背景内容 accessibilityLevel('no-hide-descendants')（见 lesson-96eea0feeae116ef9262），并在报告中说明与源端承载的偏离
- [用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，不挂在触发按钮所在的子组件](lesson-0a26e0cfc44a183d3a02.lesson.md)
  - 时机：界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级时
  - 情境：源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，源端 dim 覆盖整个窗口；触发按钮位于 Tabs 子页或嵌套组件内；项目已决定用页内覆层而不是系统弹窗 API。
  - 例外：改用 openCustomDialog、bindSheet 等系统弹窗 API 承载时不适用本条（本条只管页内覆层的挂载层级），承载形态按 lesson-368c4592e4c7075c1871 选择
- [组件外的函数打开弹窗时，把 wrapBuilder 包好的内容建成 ComponentContent 再 openCustomDialog](lesson-a3ac761b0d52a6bccb9f.lesson.md)
  - 时机：界面实现阶段，把路由页改成多个入口复用的自定义弹窗，确定弹窗内容的构建与挂载方式时
  - 情境：ArkTS V2（@ComponentV2）工程中，把 BottomSheetDialog/DialogFragment 一类弹窗迁成 UIContext.getPromptAction().openCustomDialog，并打算从组件外的导出函数（只持有 UIContext）为多个页面统一打开同一个自定义组件。
- [页内对话框的可见性状态逐一落实打开触发点：卡片整体点击与卡内关闭按钮分开实现，留给后续任务的触发点要登记](lesson-f0d5a447e645bc253019.lesson.md)
  - 时机：界面转换与页内接线阶段，把源页面中可点击的卡片、按钮及其打开的页内对话框转换为 ArkUI 触发器与可见性状态时
  - 情境：源端 Compose Card 以 Modifier.clickable 打开对话框，卡内另有关闭或忽略按钮；目标以 @Local 可见性标志加 @Builder 覆盖层实现页内对话框，部分处理器以前向占位留给后续切片；页面规格的导航关系表列出“触发 → 对话框”。
- [页内遮罩承载源端对话框时，显示期间把背景内容移出无障碍树：accessibilityLevel('no-hide-descendants')](lesson-96eea0feeae116ef9262.lesson.md)
  - 时机：界面实现阶段，为源端独立窗口对话框选择承载方式，或按项目已有写法用页内 Stack 遮罩加卡片实现对话框时
  - 情境：源端对话框是独立窗口（Compose Dialog/AlertDialog、Android Dialog），读屏焦点限制在对话框内；目标以可见性状态在页面根 Stack 中条件渲染遮罩与卡片，背景页面仍在同一组件树；规格或共享弹窗组件头注可能已指定 openCustomDialog、@CustomDialog 等系统通道，兄弟页已有同款页内遮罩可参照。
  - 例外：使用 openCustomDialog、showAlertDialog、bindSheet 等系统弹窗通道：窗口级模态由系统提供
