# 基类用同一 Toolbar 挂 ActionBarDrawerToggle 时，规格写汉堡开抽屉，不写返回箭头

审的是：规格
触发（任一种）：
- 读到：子类 onCreate 调 setSupportActionBar 和 setDisplayHomeAsUpEnabled(true)，所继承的基类在 onPostCreate 里以同一 Toolbar new ActionBarDrawerToggle(...) 并 syncState()；布局根是 DrawerLayout + NavigationView；写错的样子：规格、转换决策或验收条目写「setDisplayHomeAsUpEnabled(true)（返回箭头）」「标题栏 + 返回箭头」「Up 返回箭头可见」，点击结果写返回上一页；没写导航图标最终是汉堡、点击开关抽屉
适用范围：规格提取时写继承抽屉基类的页面的工具栏导航图标、点击结果和对应验收条目
做法：
- 按生命周期顺序合并子类 onCreate 与基类 onPostCreate 对同一 Toolbar 的设置，规格里只写最终生效的那一种：基类以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState() 时写「导航图标为汉堡，点击开关抽屉，页面装配抽屉基座」
- 验收条目照最终形态写（汉堡可见、点击开关抽屉），不只凭子类出现 setDisplayHomeAsUpEnabled(true) 写返回箭头
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onPostCreate 在 onStart 和 onRestoreInstanceState 之后调用，晚于子类 onCreate：基类在这里对 Toolbar 的设置会盖过子类 onCreate 里的设置（出处：android.app.Activity#onPostCreate）
- 子类 setDisplayHomeAsUpEnabled(true) 之后，基类 onPostCreate 以同一 toolbar 构造 ActionBarDrawerToggle 并 syncState()，导航图标被换成汉堡、点击开关抽屉：两处设置合并后实际生效的形态（出处：卡里修好并验证过）
针对本应用要查的：
- 页面继承的基类有没有接管同一 Toolbar 的导航图标：源工程里这个 Activity 的父类（一路往上）的 Java/Kotlin 文件，按 ActionBarDrawerToggle、syncState、onPostCreate 搜；构造 ActionBarDrawerToggle 时传的是同一个 toolbar 并调了 syncState()，就按汉堡写；否则才按子类的 setDisplayHomeAsUpEnabled 写返回箭头
来源：1 张卡，1 个应用
- case-255a399de4580990a70e（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 2 ← 诊断
