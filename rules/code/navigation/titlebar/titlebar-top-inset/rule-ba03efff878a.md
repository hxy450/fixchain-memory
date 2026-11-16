# hideTitleBar 自绘工具栏时，外层容器实际写 padding top 接顶部避让值

审的是：代码
触发（任一种）：
- 读到：源 Activity 用窗口 ActionBar（主题如 Theme.AppCompat.Light.DarkActionBar，Up 返回）；目标开启全屏布局，NavDestination 改 .hideTitleBar(true) 自绘工具栏；写错的样子：包工具栏的外层 Column 只有「避状态栏」之类的注释，没有 .padding({ top: … }) 引用顶部避让值；窗口模型只声明并 connect，成了没被引用的成员
适用范围：目标开启全屏布局、页面隐藏系统标题栏改自绘工具栏时，含兑现标题栏避让前向项
做法：
- 在包工具栏的外层容器上写 .padding({ top: <目标工程提供的顶部避让值> })，工具栏底色铺在这个外层容器上
- 写完在本文件里搜这个顶部避让值，确认至少出现在一处 padding 里
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hideTitleBar(value: boolean): NavDestinationAttribute，默认 false：隐藏 NavDestination 的系统标题栏（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.hideTitleBar）
- padding(value: Padding | Length | LocalizedPadding): T：外层容器内边距，top 放顶部避让值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea；AvoidAreaType.TYPE_SYSTEM = 0；Rect.height 单位 px：目标工程没有现成顶部避让值时的来源：系统避让区 topRect 的高度，按 px 给出（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea、AvoidAreaType.TYPE_SYSTEM；arkts-apis-window-i.md，Rect）
- 外层包裹 Column 加顶部避让 padding 后工具栏不再画进状态栏：卡里最终保留的改法（出处：卡里修好并验证过）
针对本应用要查的：
- 目标工程里顶部避让值叫什么、单位是什么：目标工程里窗口或安全区的模型/工具类，以及已经做过自绘标题栏的页面（先例的外层容器 padding）；照先例外层容器 padding top 引用的那个值写；看它是 px 还是 vp，px 要换成 vp 再给 padding
未核实：工具栏的图标、标题字重和投影细节卡里没核到
来源：1 张卡，1 个应用
- case-f103fbdcad4e6eeb7569（Privacy Friendly 2048）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 4 ← 诊断
