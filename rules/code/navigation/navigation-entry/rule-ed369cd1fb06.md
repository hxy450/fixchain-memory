# pageMap 里填组件前确认它的 build 根是 NavDestination，Tab 内容组件要包一层路由帧

审的是：代码
触发（任一种）：
- 读到：规格写明 Compose NavHost → Navigation(navPathStack) 加各 NavDestination 子页；某些页面既是底部 Tab 的内容组件又是路由目标；写错的样子：navDestination 的 pageMap 构建函数里直接挂 build 根不是 NavDestination 的组件（如直接调用一个 Tab 内容 struct），push 后是空白页
适用范围：路由表收口、往 Navigation 的 navDestination 构建函数里按路由名填组件时
做法：
- 每个 slot 填组件前确认目标 struct 的 build() 根是 NavDestination()；只按 struct 名匹配不够
- Tab 内容组件由路由侧包一层：@Component struct <路由帧> { build() { NavDestination() { <Tab 内容组件>(…) }.onReady((ctx) => { 解析 ctx.pathInfo.param }) } }，pageMap 里挂这个路由帧
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- NavDestination 是 Navigation 子页面的根容器：pageMap 构建出来的每个页面都要以它为根（出处：arkts-navigation-navdestination.md，开头说明）
- navDestination(builder: (name: string, param: unknown) => void): NavigationAttribute：按路由名构建子页的入口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.navDestination）
- 四路改为以 NavDestination 为根的路由帧并在其中解析参数后，push 不再空白：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- pageMap 里每个组件的 build 根：目标工程里每个被 pageMap 引用的 struct 的 build() 方法；看 build() 第一层是不是 NavDestination()；不是的就要包路由帧
来源：1 张卡，1 个应用
- case-2e5a8c9bed405f41a6ce（jerboa）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断；取值 3 ← 诊断
