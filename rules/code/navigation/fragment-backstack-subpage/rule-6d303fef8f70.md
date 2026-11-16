# 源端壳内 hide+add+addToBackStack 压栈的子页，目标在壳状态里维护子回退栈

审的是：代码
触发（任一种）：
- 读到：源端单 Activity 壳在内容区用 FragmentTransaction 的 hide(当前) + add(子 Fragment) + addToBackStack(...) 压栈加载子页，子页期间底部导航和迷你播放条仍在，工具栏随回退栈深度切换上箭头，带导航 tag 时同步底部导航选中；规格 AC 用「标:」点名壳路由的子页加载方法；写错的样子：子页写成 pushPathByName 推到壳外的 NavDestination；返回首分支写 navPathStack.size() > 1 交系统弹栈；壳状态里没有子回退栈字段，壳路由只有清栈切页入口
适用范围：目标端同时有 Navigation + NavDestination 路由和壳内容槽（按 tag 切换），迁移源端单 Activity 内容区压栈子页时
做法：
- 壳状态里加子回退栈：入栈项记上一页的 tag 和参数，另记当前子页参数、上箭头是否显示、底部导航选中 tag；壳路由提供「压栈加载子页」「弹出子页」两个入口，清栈切页入口同时清空子栈
- 返回键和工具栏上箭头先弹子栈，子栈空了再走默认页 / 抽屉 / 退出分支；上箭头按栈深切换；压栈时带了导航 tag 就覆盖底部导航选中
- 规格里每条「标:」指向的目标方法逐条落地或登记缺口；先判定子页期间底栏、迷你播放条是否仍可见，仍可见的子页由壳内容区按 tag 承载，不用 Navigation 路由栈替代
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- addToBackStack(@Nullable String name)：提交后事务被记住，出栈时反向执行：源端子页压在内容区回退栈里，返回时恢复上一页（出处：android.app.FragmentTransaction#addToBackStack）
- hide(Fragment fragment)：只隐藏已加到容器里的 Fragment 的视图：源端上一页保活不销毁，壳的其余部分（底栏、迷你条）不动（出处：android.app.FragmentTransaction#hide）
- 壳状态加子回退栈、当前子页参数、上箭头和选中 tag；壳路由加压栈加载、弹出入口，清栈入口清子栈；壳以保活层渲染回退栈和嵌入子页：返修后的壳结构（出处：卡里修好并验证过）
针对本应用要查的：
- 子页期间哪些壳元素仍可见：源工程壳 Activity 的布局 XML（内容区容器之外的底部导航、播放条等）和压栈加载方法里有没有隐藏它们；加载子页时没隐藏的元素，在目标子页期间也保持显示
来源：1 张卡，1 个应用
- case-05f3fb8501654bad9261（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 1；取值 3 ← 诊断
