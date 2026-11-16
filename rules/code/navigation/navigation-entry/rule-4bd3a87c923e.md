# 入口写 hideNavBar(true) 时，navBar 槽不能承载内容，且要有空栈压入启动页的语句

审的是：代码
触发（任一种）：
- 读到：入口模板是 Navigation(this.navPathStack){ 首页内容 }.navDestination(pageMap).mode(NavigationMode.Stack)，模板里没有 hideNavBar；写错的样子：入口 Navigation 上写了 .hideNavBar(true)，而内容槽里放着启动页或首页内容，或者全文找不到空栈时 pushPathByName 启动页的语句
适用范围：入口页 Navigation 设置 hideNavBar 时
做法：
- 只有确实不用 navBar 槽时才写 .hideNavBar(true)，并同时在 aboutToAppear 里空栈时 pushPathByName 启动页；navBar 槽承载启动或首页内容时去掉 hideNavBar(true)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hideNavBar(value: boolean): NavigationAttribute，默认 false；隐藏的 NavBar 包括标题栏、Navigation 的子组件和工具栏，隐藏后直接显示栈顶页，栈里没有页面时为空：hideNavBar(true) 加空栈就是白屏（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.hideNavBar）
来源：1 张卡，1 个应用
- case-d1b8189b8a745399dc3a（实时公交）：做法第 1 步 ← 建议 2
