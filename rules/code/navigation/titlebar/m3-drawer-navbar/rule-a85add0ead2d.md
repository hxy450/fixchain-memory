# 源端抽屉没有悬浮切换按钮时，SideBarContainer 写 .showControlButton(false)

审的是：代码
触发（任一种）：
- 读到：Compose 的 ModalNavigationDrawer 只靠 gesturesEnabled 边缘手势和页内 TopAppBar 菜单图标的 openDrawer 回调打开，没有悬浮的抽屉切换按钮；详情页同一左上角是返回键；写错的样子：SideBarContainer(SideBarContainerType.Overlay) 的属性链只有 .showSideBar / .sideBarWidth / .onChange，没写 .showControlButton(false)，默认内置控制按钮盖在 NavDestination 返回键上
适用范围：用 ArkUI SideBarContainer 承接源端模态抽屉，并在主内容区放 Navigation / NavDestination 时
做法：
- 先列出源端抽屉的全部打开入口（页内菜单图标回调、边缘手势）；源端没有悬浮切换按钮时，在属性链里显式写 .showControlButton(false)，不依赖默认值
- 保留内置按钮之前，按它的默认位置（距容器左 16vp、上 48vp，24vp 见方）和被包页面同位置的可点控件（NavDestination 返回键、TopAppBar 菜单键）比对是否重叠
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showControlButton(value: boolean): SideBarContainerAttribute，默认值 true：是否显示内置控制按钮；不写就显示（出处：鸿蒙 SDK 的 ets/component/sidebar.d.ts，SideBarContainerAttribute.showControlButton；ts-container-sidebarcontainer.md，showControlButton）
- controlButton(value: ButtonStyle): SideBarContainerAttribute；ButtonStyle.left 默认 16vp、top 默认 48vp，width、height 从 API 10 起默认 24vp：内置控制按钮的位置和大小，用来判断会不会盖住页面左上角的控件（出处：鸿蒙 SDK 的 ets/component/sidebar.d.ts，SideBarContainerAttribute.controlButton；ts-container-sidebarcontainer.md，ButtonStyle对象说明）
- (type?: SideBarContainerType): SideBarContainerAttribute：SideBarContainer 的构造，Overlay 对应模态抽屉的叠放（出处：鸿蒙 SDK 的 ets/component/sidebar.d.ts，SideBarContainerInterface）
- 加上 .showControlButton(false) 后点返回键正常返回，不再打开抽屉：修复只关掉内置按钮，SideBarContainer 包住 Navigation 的结构不变（出处：卡里修好并验证过）
未核实：卡里环境的鸿蒙版本记了 API 12 和 API 24 两种，本机按 API 23 核实
来源：1 张卡，1 个应用
- case-71aa526f07e03994b949（Jetnews）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
