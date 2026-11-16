# Compose 路由带 {参数} 占位符时，pushPathByName 首参写固定名，参数只走 param

审的是：代码
触发（任一种）：
- 读到：Compose Navigation 用带 {参数} 占位符的路由模式注册目的地（composable("detail/{id}", arguments = listOf(navArgument("id")…))），另有函数把 id 拼进路由串再 navController.navigate(…)；写错的样子：pushPathByName 的首参是模板字符串或字符串拼接（如 pushPathByName(`detail/${id}`, id)），同一个 id 既拼进名字又作为 param 传
适用范围：把 Compose Navigation 的带参路由迁成 Navigation + NavPathStack 跳转时
做法：
- 目的地名写规格判定组里的固定名常量，参数只经 param：pushPathByName('detail', id)；源端拼路由串的函数只说明要带什么参数，不照搬成目的地名
- 目标页在 NavDestination 的 onReady 回调里从 context.pathInfo.param 取参数
- 写完搜每个 pushPathByName 的首参，出现模板字符串或字符串拼接就改成固定名常量
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：name 是目的地名，param 是给目的地的参数（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- NavDestinationContext.pathInfo: NavPathInfo；NavPathInfo.param?: unknown：目的地页取参数的位置（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationContext.pathInfo；ets/component/navigation.d.ts，NavPathInfo.param）
- onReady(callback: Callback<NavDestinationContext>): NavDestinationAttribute：目的地页拿到 context 的回调（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：同样按名字加 param 入栈，带返回的 Promise（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：按名字加 param 替换栈顶（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
- constructor(name: string, param: unknown, onPop?: Callback<PopInfo>, isEntry?: boolean)：同族接口：NavPathInfo 的构造，配 pushPath 用，name 同样写固定名（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.constructor）
未核实：卡里环境是 HarmonyOS API 21，本机按 API 23 核实
来源：1 张卡，1 个应用
- case-17c8141513c5958bfbac（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 1
