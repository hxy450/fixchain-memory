# Navigation 入口和首屏的挂载

agent 会看到什么：入口页的 Navigation(...) { } 内容槽里放了什么、有没有 hideNavBar、navDestination 怎么注册，首屏 NavDestination 怎么压栈和处理返回键

## 规矩

- rule-06f0a8293910｜启动页根是 NavDestination 时，入口空栈时 pushPathByName 压入，不放进 navBar 槽｜读到：规格写「单 Navigation + 各 Activity 映射为 NavDestination」，启动 Activity 靠 onResume、onActivityResult 驱动；写错：启动页写在 Navigation(...) { } 内容槽里、从未进栈，onShown / onResult / onBackPressed 落空
- rule-4bd3a87c923e｜入口写 hideNavBar(true) 时，navBar 槽不能承载内容，且要有空栈压入启动页的语句｜读到：入口模板是 Navigation(this.navPathStack){ 首页内容 }.navDestination(pageMap).mode(NavigationMode.Stack)，模板里没有 hideNavBar；写错：入口 Navigation 上写了 .hideNavBar(true)，而内容槽里放着启动页或首页内容，或者全文找不到空栈时 pushPathByName 启动页的语句
- rule-3e405da72623｜启动页作为首个 NavDestination 压入空 Navigation 时，该页 onBackPressed 退后台｜读到：源端启动页是 NavHost 的 startDestination，没有 BackHandler；写错：空的 Navigation(this.navPathStack) {}，aboutToAppear 里 pushPathByName 启动页，它的 NavDestination 没有 .onBackPressed
- rule-199676fcbc5b｜.navDestination 直接传 @Builder 方法 this.destination，不再包一层箭头函数｜写错：写成 .navDestination((name, param) => this.destination(name, param))，用箭头函数包了一层 @Builder 方法
- rule-ed369cd1fb06｜pageMap 里填组件前确认它的 build 根是 NavDestination，Tab 内容组件要包一层路由帧｜读到：规格写明 Compose NavHost → Navigation(navPathStack) 加各 NavDestination 子页；某些页面既是底部 Tab 的内容组件又是路由目标；写错：navDestination 的 pageMap 构建函数里直接挂 build 根不是 NavDestination 的组件（如直接调用一个 Tab 内容 struct），push 后是空白页
- rule-882496c1926d｜源端起点会在会话内变时，目标起点做成可重算，变了就 clear 后以新起点重压｜读到：源端 NavHost(startDestination = 读偏好或状态的函数) 写在会重组的壳层内容 lambda 里，没有 remember；写错：目标只在 NavPathStack 为空时 pushPathByName 首屏一次、另加布尔守卫，顶级导航器构造时固定首压时的起点名，navigateToTopLevel 只以这个固定起点为 popToName 基准
- rule-b93fedcfcdad｜被入口 Navigation 压栈的根页 NavDestination 必须实现 onBackPressed 并始终消费｜读到：入口用 Navigation 把根页作为 NavDestination 压栈；源端根 Activity 按返回会关 popup、退到后台或退出（OnBackPressedCallback / onBackPressed）；写错：根页 NavDestination 没有 .onBackPressed，或以「接口可能只在较新 API 可用」为由回避
