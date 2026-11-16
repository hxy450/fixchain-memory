# 标题栏、菜单与抽屉

读到源端有菜单 XML（showAsAction）、上下文菜单、ActionBar / Toolbar / TopAppBar、DrawerLayout + NavigationView，规格里写标题栏、Up 箭头、溢出菜单、折叠顶栏和抽屉时

## 触发族

- [菜单项的 android:showAsAction 和溢出菜单](menu-show-as-action/index.md)（5 条）：菜单 XML 的 <item> 用 android:showAsAction（ifRoom、never，带 tools:ignore="AppCompatResource"），溢出项由平台主题的下拉面板承载，规格写成 ActionBar 图标按钮、或只写「Menu + MenuItem」一行
- [DrawerLayout + NavigationView 抽屉页](drawer-navigation-view/index.md)（3 条）：读到布局根是 DrawerLayout + NavigationView（基类用 ActionBarDrawerToggle 挂 Toolbar、menu 带 checkableBehavior、多处 fitsSystemWindows）；规格把导航图标写成返回箭头、抽屉项只写 checked 同步、安全区只写根节点
- [带窗口 ActionBar 的页面的 Up 箭头](actionbar-up-arrow/index.md)（2 条）：读到源 Activity 用带 ActionBar 的 AppCompat 主题、Manifest 有 parentActivityName、onOptionsItemSelected 处理 android.R.id.home；页面规格的导航表写「ActionBar Up（若有）」或只按 setDisplayHomeAsUpEnabled 判断
- [exitUntilCollapsed 折叠大标题顶栏](collapsing-large-top-bar/index.md)（2 条）：读到 Compose 顶栏是 LargeFlexibleTopAppBar / LargeTopAppBar 加 TopAppBarDefaults.exitUntilCollapsedScrollBehavior(...)，另有 collapse() 动画写 heightOffset；转换决策写「无现成件，简化为标题栏滚动渐变」「保底固定标题栏」，或 AC 以固定标题栏为目标
- [上下文菜单（registerForContextMenu、openContextMenu）](context-menu-trigger/index.md)（1 条）：读到源码 registerForContextMenu(view)、点击时 openContextMenu(view)（不带坐标）、onCreateContextMenu 里 setHeaderTitle / setHeaderIcon；规格写「openContextMenu 锚定在按钮上弹出」或「长按/点击 → Menu 弹出列表」，不分点击和长按两种形态，也没写标题和图标
- [Compose ModalNavigationDrawer 模态抽屉](compose-modal-drawer/index.md)（2 条）：读到 Compose 源端用 ModalNavigationDrawer（gesturesEnabled、页内菜单图标调 drawerState.open、子组件里 BackHandler(drawerState.isOpen)）；规格写「边缘右滑」「ModalNavigationDrawer → SideBarContainer(Overlay)」，没写打开入口、内置按钮、整区拖拽和抽屉开着时返回先关抽屉
- [Compose 的下拉菜单和级联菜单](compose-dropdown-cascade-menu/index.md)（2 条）：读到 Compose 源端用 M3 DropdownMenu、CascadeDropdownMenu 或基于 Popup 的菜单，放在触发 IconButton 所在的 Box 里，带 children 的项在同一菜单里切到子层；规格写「两级 Menu / 半模态面板」「ArkUI Menu 不支持嵌套子菜单」「弹出形态差异由 visual 断言容忍」
- [工具栏里的 SearchView 和 ActionBarDrawerToggle](toolbar-search-drawer-toggle/index.md)（1 条）：读到菜单 XML 的 item 用 SearchView 作 actionView（showAsAction 含 collapseActionView）、代码有 OnActionExpandListener、onQueryTextSubmit、supportInvalidateOptionsMenu，或 ActionBarDrawerToggle 的 setDrawerIndicatorEnabled、syncState；规格把它写成几个查询函数或「内化等价」，AC 没有展开收起、焦点、提交和菜单重建
