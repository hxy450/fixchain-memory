# 源端工具栏行为由 SearchView、ActionBarDrawerToggle 承载时，规格按控件 API 列状态机

审的是：规格
触发（任一种）：
- 读到：menu XML 的 item 用 SearchView 作 actionView、showAsAction 为 collapseActionView|always，代码里有 OnActionExpandListener、setOnQueryTextFocusChangeListener、onQueryTextSubmit、supportInvalidateOptionsMenu；或 ActionBarDrawerToggle 的 setDrawerIndicatorEnabled、syncState；写错的样子：规格把 SearchView 写成几个查询函数，实现映射写「内化等价」「状态直调」；AC 里没有展开/收起、焦点、提交返回值与 ACTION_SEARCH 投递、菜单重建收起、空串不提交
适用范围：规格提取阶段翻译 AppCompat 宿主栏控件（SearchView、ActionBarDrawerToggle、ActionMode）承载的工具栏行为
做法：
- 按控件 API 列出状态机，每个回调一条 AC：SearchView 的 onMenuItemActionExpand / onMenuItemActionCollapse、焦点监听、onQueryTextSubmit 返回 false 时由 SearchView 投递 ACTION_SEARCH、invalidateOptionsMenu 重建菜单时收起；抽屉开关的 setDrawerIndicatorEnabled、syncState
- 不以「内化等价」把控件生命周期折成查询函数；对接点写清页面持有的展开、焦点状态和收起出口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onMenuItemActionExpand / onMenuItemActionCollapse 返回 true 才展开 / 收起，返回 false 抑制：带 SHOW_AS_ACTION_COLLAPSE_ACTION_VIEW 的菜单项展开、收起时回调（出处：android.view.MenuItem.OnActionExpandListener）
- onQueryTextSubmit 返回 true 表示监听者已处理；返回 false 由 SearchView 执行默认动作（发出关联的 intent）：提交返回值决定是否投递 ACTION_SEARCH（出处：android.widget.SearchView.OnQueryTextListener#onQueryTextSubmit）
- expandActionView() 要求菜单项设了 actionView 和 SHOW_AS_ACTION_COLLAPSE_ACTION_VIEW，并回调 onMenuItemActionExpand：展开是菜单项的状态，不是一个布尔开关（出处：android.view.MenuItem#expandActionView）
针对本应用要查的：
- 源端控件状态机的全部回调：源工程里创建该控件的方法全文（初始化 SearchView 或 ActionBarDrawerToggle 的那个方法），以及 menu XML 里该 item 的 showAsAction；逐个列出 setOn…Listener 注册的回调、各回调里的调用和返回值，每条写成一条 AC
未核实：源端用的是 AppCompat 的 SearchView，本机只有框架 android.widget.SearchView 的源码；同名回调的返回值语义按框架源码核对
来源：1 张卡，1 个应用
- case-aa81c21ff3eaca257ba4（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
