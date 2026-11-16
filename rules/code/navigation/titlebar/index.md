# 标题栏、抽屉与菜单

源端有 Toolbar / ActionBar、onCreateOptionsMenu、setDisplayHomeAsUpEnabled、DrawerLayout、CollapsingToolbarLayout、Compose TopAppBar，目标端有自绘标题栏、NavDestination 的 title / menu、hideTitleBar 时

## 触发族

- [照源端 @Composable 复刻的标题行组件](composable-title-row/index.md)（2 条）：产物里的标题行组件（换上的共享 @Component，或凭截断的读源码回执重写的组件）丢了源端的标题色、maxLines、weight 和尾部 IconButton，或 padding 对不上
- [DrawerLayout 抽屉和汉堡工具栏](drawer-toolbar/index.md)（7 条）：源端 DrawerLayout 配 ActionBarDrawerToggle 接管 Toolbar 导航图标、NavigationView 抽屉菜单（含基类里的 toggle），对应目标的抽屉基座、汉堡栏和菜单行
- [CollapsingToolbarLayout 折叠头部](collapsing-header/index.md)（5 条）：源端 AppBarLayout / CollapsingToolbarLayout 的折叠头部（match_parent 的背景图、?attr/actionBarSize、OnOffsetChangedListener 里按折叠进度给工具栏图标着色），对应目标头部的高度、滚动折叠阈值和图标两态颜色
- [工具栏的高度、标题字号和颜色](toolbar-size-color/index.md)（9 条）：源端 Toolbar / ActionBar 的 ?attr/actionBarSize、标题样式和 AppBarLayout 的 ThemeOverlay；产物里自绘工具栏的 .height、.fontSize、.fontWeight 和标题、图标的颜色
- [标题栏的返回箭头](up-arrow/index.md)（4 条）：源端 Manifest 的 android:parentActivityName、代码里的 setDisplayHomeAsUpEnabled 和窗口 ActionBar 主题；产物里自绘标题栏有没有返回箭头
- [自绘标题栏的顶部避让](titlebar-top-inset/index.md)（8 条）：目标页 hideTitleBar 或全屏布局下自绘标题栏；产物里标题栏的 .height(…) 与 .padding({ top: … })、NavDestination 的 .title(...) 和顶部避让值用在哪
- [平台 ActionBar 和选项菜单](actionbar-options-menu/index.md)（12 条）：读到 Activity 用平台主题的 ActionBar（setDisplayHomeAsUpEnabled、onCreateOptionsMenu）、菜单 XML 的 <item> 带 showAsAction 和 android:icon；交回的标题栏各页手绘、动作项放错位置（标题栏图标位或 ⋮ 溢出），或 Menu / MenuItem 只改了颜色
- [Compose 折叠顶栏（LargeTopAppBar 配 exitUntilCollapsedScrollBehavior）](collapsing-top-app-bar/index.md)（3 条）：读到 Compose 的 LargeTopAppBar / LargeFlexibleTopAppBar 配 TopAppBarDefaults.exitUntilCollapsedScrollBehavior、按 collapsedFraction 插值，产物里是固定高度顶栏、onDidScroll 只变色或 onScrollIndex 两态切换的写法
- [编辑态切换的顶栏和底栏](edit-mode-bars/index.md)（1 条）：读到 Compose Screen 的 TopAppBar 动作在编辑 / 完成间切换、底栏 Composable 按编辑态换成删除或合计结算；产物里没有编辑态的 @State，顶栏只有单一动作，底栏只有一套控件
- [菜单 XML 里的子菜单](menu-xml-submenu/index.md)（1 条）：读到菜单 XML 的 <item> 里内嵌 <menu> 子菜单（SubMenu）；产物里溢出列表这一项行尾有没有子菜单箭头、从溢出打开的子菜单弹层有没有标题头
- [窗口 ActionBar 溢出菜单的面板](overflow-menu-panel/index.md)（2 条）：读到源端窗口 ActionBar 的溢出菜单（菜单有进溢出的项，框架用 PopupWindow 弹出，样式取主题的 actionOverflowMenuStyle、colorPopupBackground）；产物里自绘溢出面板盖不盖住标题栏、底色、点外关闭层和面板挂在哪一层
- [Compose 模态抽屉和 M3 底栏的自绘替代](m3-drawer-navbar/index.md)（2 条）：读到 Compose 的 ModalNavigationDrawer / ModalDrawerSheet（gesturesEnabled、drawerState、TopAppBar 菜单图标调 openDrawer），或参数多取库默认值的 NavigationBar / NavigationBarItem；产物里自绘的 Row 底栏、Stack 滑出面板或 SideBarContainer 的属性链：默认值有没有按 material3 版本核过、手势是否跟手、有没有 showControlButton(false)
- [ActionMode 多选上下文操作栏（CAB）](action-mode-cab/index.md)（3 条）：读到源端 ActionMode.Callback 显示多选 CAB 盖住 Toolbar（onCreateActionMode 里 getMenuInflater().inflate 复用页面菜单、onActionItemClicked 入口统一门控，targetSdk ≥ 35 的 edge-to-edge）；产物里自绘 CAB 栏的菜单项和溢出的填充、批量动作分发函数里的门控、CAB 期间状态栏区的色块和工具栏投影
- [Ionic 的 IonHeader / IonToolbar 顶部工具栏](ionic-toolbar/index.md)（2 条）：读到源页面 IonHeader > IonToolbar 里的 IonTitle（Ionic mode: "ios" 下居中）、IonButtons slot="end" 的图标按钮、有没有 IonBackButton；产物里 NavDestination 的 .title / .menus 自定义槽、hideTitleBar(true) 加页内头部、头部 Row 里标题的 layoutWeight 和居中
