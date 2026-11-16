# Compose ModalNavigationDrawer 模态抽屉

agent 会看到什么：读到 Compose 源端用 ModalNavigationDrawer（gesturesEnabled、页内菜单图标调 drawerState.open、子组件里 BackHandler(drawerState.isOpen)）；规格写「边缘右滑」「ModalNavigationDrawer → SideBarContainer(Overlay)」，没写打开入口、内置按钮、整区拖拽和抽屉开着时返回先关抽屉

## 规矩

- rule-7e29c916d809｜ModalNavigationDrawer 映射成 SideBarContainer 时，规格写明打开方式和内置按钮｜读到：Compose 的 ModalNavigationDrawer 只经 gesturesEnabled 手势和页内菜单图标的 openDrawer 回调打开；写错：规格的转换决策只写「ModalNavigationDrawer → SideBarContainer(Overlay)」，没写抽屉的打开入口，也没写内置控制按钮保留还是关掉
- rule-62ce884fd09f｜规格写模态抽屉时写成整区拖拽跟手，子组件返回键分支写进 @Entry 页规格｜读到：源码 `ModalNavigationDrawer(gesturesEnabled = true)`；写错：规格写成「抽屉手势从屏幕边缘滑出」「边缘右滑」，转换决策只给 SideBarContainer 或自定义滑出面板，没写开合行为
