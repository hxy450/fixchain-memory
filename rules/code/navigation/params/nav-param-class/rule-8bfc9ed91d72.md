# 订阅键取自路由参数时，在 NavDestination.onReady 赋值之后订阅，并确认有生产者

审的是：代码
触发（任一种）：
- 写错的样子：aboutToAppear 里用还没赋值的路由参数作键调 subscribe(...)（参数在 onReady 才赋值），订阅键恒为空串；页面里没有任何发该键事件的生产调用
适用范围：NavDestination 页面按路由参数（如图片地址）订阅事件总线或进度总线时
做法：
- 在 NavDestination().onReady((ctx: NavDestinationContext) => { 从 ctx.pathInfo.param 取参数赋值；之后再 subscribe(键, …) }) 里订阅，不在 aboutToAppear 里
- 确认页面或上游有生产者用同一个键发事件（例如图片改由带进度的下载函数加载），否则订阅永远收不到
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onReady(callback: import('../api/@ohos.base').Callback<NavDestinationContext>): NavDestinationAttribute：NavDestination 将要构建子组件前回调，带 NavDestinationContext（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- NavDestinationContext.pathInfo: NavPathInfo；NavPathInfo.param?: unknown：路由参数从这里取（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationContext.pathInfo；ets/component/navigation.d.ts，NavPathInfo.param）
来源：1 张卡，1 个应用
- case-149fd657e7134bf86261（jerboa）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、诊断
