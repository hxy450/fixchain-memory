# Compose 模态抽屉和 M3 底栏的自绘替代

agent 会看到什么：读到 Compose 的 ModalNavigationDrawer / ModalDrawerSheet（gesturesEnabled、drawerState、TopAppBar 菜单图标调 openDrawer），或参数多取库默认值的 NavigationBar / NavigationBarItem；产物里自绘的 Row 底栏、Stack 滑出面板或 SideBarContainer 的属性链：默认值有没有按 material3 版本核过、手势是否跟手、有没有 showControlButton(false)

## 规矩

- rule-a85add0ead2d｜源端抽屉没有悬浮切换按钮时，SideBarContainer 写 .showControlButton(false)｜读到：Compose 的 ModalNavigationDrawer 只靠 gesturesEnabled 边缘手势和页内 TopAppBar 菜单图标的 openDrawer 回调打开，没有悬浮的抽屉切换按钮；详情页同一左上角是返回键；写错：SideBarContainer(SideBarContainerType.Overlay) 的属性链只有 .showSideBar / .sideBarWidth / .onChange，没写 .showControlButton(false)，默认内置控制按钮盖在 NavDestination 返回键上
- rule-1e612d089312｜自绘替代 M3 底栏或模态抽屉时，按 material3 版本逐项列默认值并实现｜读到：Compose `NavigationBar` / `NavigationBarItem` 多数参数取库默认值；写错：自定义 Row 底栏的容器色、项间距、指示器尺寸、选中图标/标签色是自定的近似值，没有按 material3 版本核
