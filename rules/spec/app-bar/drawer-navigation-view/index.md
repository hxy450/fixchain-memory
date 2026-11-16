# DrawerLayout + NavigationView 抽屉页

agent 会看到什么：读到布局根是 DrawerLayout + NavigationView（基类用 ActionBarDrawerToggle 挂 Toolbar、menu 带 checkableBehavior、多处 fitsSystemWindows）；规格把导航图标写成返回箭头、抽屉项只写 checked 同步、安全区只写根节点

## 规矩

- rule-81b0f2c8baa3｜基类用同一 Toolbar 挂 ActionBarDrawerToggle 时，规格写汉堡开抽屉，不写返回箭头｜读到：子类 onCreate 调 setSupportActionBar 和 setDisplayHomeAsUpEnabled(true)，所继承的基类在 onPostCreate 里以同一 Toolbar new ActionBarDrawerToggle(...) 并 syncState()；布局根是 DrawerLayout + NavigationView；写错：规格、转换决策或验收条目写「setDisplayHomeAsUpEnabled(true)（返回箭头）」「标题栏 + 返回箭头」「Up 返回箭头可见」，点击结果写返回上一页；没写导航图标最终是汉堡、点击开关抽屉
- rule-a4ce0f16e4fb｜规格写 NavigationView 转自定义抽屉的映射行时，补上菜单项选中、未选的可见契约｜读到：源 DrawerLayout + NavigationView 没写 item 样式，menu 分组带 checkableBehavior；写错：规格的抽屉映射行或 AC 只写 checked 布尔同步（点击项选中、其余清除），没写菜单项选中、未选的底色、字重、文字与图标着色，组间分隔几何和列表上下留白
- rule-81d9571e2a97｜源布局多处 fitsSystemWindows 时，规格的安全区段逐个子视图写由谁消费｜读到：源布局 DrawerLayout、内容列（CoordinatorLayout 等）、NavigationView 各自写了 android:fitsSystemWindows="true"，NavigationView 带 app:headerLayout；写错：规格的沉浸、安全区段只写根节点的 fitsSystemWindows（如「DrawerLayout(fitsSystemWindows) → SideBarContainer」），没写内容列下移、抽屉头部画到状态栏下并叠 insetForeground
