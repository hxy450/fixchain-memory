# @ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog

## 何时使用

界面实现阶段，为 @ComponentV2 页面选择弹窗承载方式、编写弹窗子组件时（含参照工程内已有弹窗写法时）

## 适用情境

项目要求页面与子组件都用 @ComponentV2、不混用 V1；需要把 Android Dialog/DialogFragment 一类居中或底部弹窗迁成 ArkUI；规格可能写着 CustomDialog、@CustomDialog 或 bindSheet。

## 原因

CustomDialogController 的 builder 约定是 @CustomDialog 组件；把 @ComponentV2 struct 当 builder 传入时，结构体构造语法不会被转译，运行时报 TypeError: class constructor cannot called without 'new'，页面打开或首次状态更新即崩溃或冻结。编译能通过，自检若只查“有没有混用 V1/V2 装饰器”也发现不了。来源中第一位写者没有采用规格给出的可用载体，第二位写者看到这个先例后推断“builder 接受任意组件”并照抄。

## 做法

1. 在 V2 页面里从这些载体中选：页内 @Local 状态驱动的 Stack 条件浮层（遮罩＋卡片，卡片吞点击、遮罩点击关闭）、bindSheet/bindContentCover、UIContext.getPromptAction().openCustomDialog。
2. 写 CustomDialogController 前先核其 builder 约定；“全 V2、不混用”的规则与之冲突时换载体，不要把弹窗 struct 改写成 @ComponentV2 来绕开。
3. 自检时 grep CustomDialogController，逐个确认 builder 组件的装饰器，以及控制器是否在页面字段初始化时就执行构造。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；Android SDK 平台资源 android-34；appcompat 1.1.0、1.7.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕CustomDialogControllerOptions.builder 在声明里是 any；编译工具只在 builder 的初始值是 @CustomDialog 装饰的 struct 时才把它改写成构造弹窗实例的代码，传 @Component 或 @ComponentV2 的 struct 不报编译错，这次 struct 调用原样留在产物里。〔成立范围：对 new CustomDialogController({ builder: X(...) }) 这种在构造参数对象字面量里写 builder 的用法成立，编译工具按 builder 初始值的名字查 @CustomDialog 集合；只有 builder 键没有初始值时才报编译错误 10905335（The builder should be initialized with a @CustomDialog Component.）。另外文档写明控制器只在作为 @CustomDialog 或 @Component struct 的成员变量、并在 @Component struct 内部定义时赋值才有效，没有列 @ComponentV2（依据是文档说明）；状态管理总览给 V2 的替代是 openCustomDialog。〕
- 〔做法第 1 步〕安卓 Dialog 默认可取消：返回键或返回手势调用 cancel()，平台与 AppCompat 的对话框主题把 windowCloseOnTouchOutside 设为 true（点窗口外也取消）；鸿蒙页内用 if 条件渲染的 Stack 浮层收不到返回事件，返回只分发给 router 页面 @Entry 组件的 onBackPress（返回 true 才不做路由返回）或 NavDestination 的 onBackPressed，不处理（返回 false 或不设返回值）时按默认路由逻辑返回上一页。〔成立范围：安卓侧对 android.app.Dialog 及其子类成立：setCancelable(false) 同时关掉返回取消和点外部取消；对话框主题的点外部取消取自平台配置 config_closeDialogWhenTouchOutside（SDK 平台资源里为 true），Theme.Material.Dialog.NoFrame 这类把 windowCloseOnTouchOutside 设为 false 的主题点外部不取消。鸿蒙侧只对页内普通组件做的浮层成立（依据是文档说明：返回回调只列在 @Entry 页面和 NavDestination 上）；openCustomDialog、bindSheet 这类系统弹窗自带点遮罩、侧滑、返回键关闭，可用 onWillDismiss 拦截。〕
- 〔做法第 1 步〕鸿蒙触摸测试会把被点组件的各级祖先一起收进响应链：卡片嵌在带 onClick 的遮罩容器里、自身没有点击手势时，点卡片也会触发遮罩的 onClick；只有卡片自己也绑了同类点击手势时才由子组件优先识别，遮罩的不触发。〔成立范围：依据是文档说明，对父子嵌套（遮罩是卡片的祖先）成立。卡片和遮罩是同一个 Stack 里的兄弟、卡片叠在上层时情形不同：卡片按默认 HitTestMode.Default 命中后阻塞被它遮住的兄弟，遮罩收不到这次点击。卡片设 HitTestMode.Block 时连祖先一起阻塞，遮罩的 onClick 也不触发。遮罩用 priorityGesture 绑点击时父组件优先，规则反过来。〕
- 〔做法第 1 步〕bindSheet 的 isShow 不做双向绑定时，用户拖拽关闭半模态不会把 isShow 改回 false；宿主节点还没挂上组件树就把 isShow 置为 true，半模态不生效。〔成立范围：依据是文档说明，文档点名的是拖拽关闭。isShow 用 $$（API 10 起）或 !!（API 18 起，状态管理 V2 用这种）双向绑定时会随关闭同步。想在页面一显示就弹出，要在宿主的 onAppear 之后再置 true，SheetMode.EMBEDDED 还要求所在页面节点已挂载。离场动效没结束时再次拉起不响应。〕
- 〔做法第 1 步〕UIContext.getPromptAction().openCustomDialog 的两个重载默认外观不同：传 ComponentContent 的重载完全按内容自身样式显示（相当于 customStyle 为 true，没有系统背板）；传 CustomDialogOptions（builder）的重载套系统背板，应用没有另设时背板 backgroundColor 为透明、backgroundBlurStyle 为 COMPONENT_ULTRA_THICK、四角圆角 32vp、宽度最大 400vp。两个重载都默认带 0x33000000 蒙层、isModal 为 true、autoCancel 为 true（点遮罩关闭）。〔成立范围：背板默认值按 API 23 的 SDK 声明；文档写明 backgroundBlurStyle 的默认值从 API 版本 26.0.0 起改为 BlurStyle.NONE。设了非透明 backgroundColor 时要把 backgroundBlurStyle 设为 NONE，否则颜色不符合预期。showInSubWindow 与 isModal 同为 true 时只生效子窗口、没有蒙层。builder 根节点的百分比宽高相对弹窗容器。〕
- 〔做法第 1 步〕bindSheet 在应用没有另设时：preferType 按窗口宽度取（宽度 < 600vp 为底部样式，600–840vp 为居中，≥ 840vp 为跟手），height 为 SheetSize.LARGE（底部样式竖屏时最高到距状态栏 8vp），showClose 为 true（显示关闭图标），backgroundColor 为 Color.White，圆角 32vp。〔成立范围：依据是文档说明。底部样式只显示上方两个圆角（底部两个圆角设了也不生效），设了 detents 时 height 不生效；居中和跟手样式下 LARGE、MEDIUM 无效，显示默认高度 560vp；按内容定高要显式设 SheetSize.FIT_CONTENT。2in1 设备的关闭图标默认没有按钮底板。〕
