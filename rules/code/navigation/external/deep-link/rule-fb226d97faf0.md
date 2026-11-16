# 壳深链分发对每个目标路由用目标页导出的参数类传 query，不统一传无参

审的是：代码
触发（任一种）：
- 读到：源端深链监听（如 AppUrlListener）把 pathname + search 整体交给 history.push，多个目标页各自用 URLSearchParams 读 query；目标页在 NavDestination 的 onReady 里用 instanceof 判断自己导出的参数类；写错的样子：分发器只给本 feature 的路由构造参数类，其余路由一律 pushPathByName('<路由名>', 无参对象)，读 query 的页面拿到空参数（标题为空、日期 NaN 之类）
适用范围：目标端由壳统一解析 want.uri 后用 pushPathByName 分发深链、目标页由其他切片实现时
做法：
- 逐个目标路由打开目标页的参数契约（onReady 里 instanceof 的参数类、源页面读的 query 键）；有参数的页面 import 它导出的参数类，用 query 里的值构造后 pushPathByName('<路由名>', new <参数类>(...))
- 写完逐条列出“路由 → 参数类”对照，确认所有读 query 的页面都拿到参数；只有确实不读参数的路由才传无参
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：按名字压入目标页，param 原样交给目标页（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- NavPathInfo.param?: unknown；目标页从 NavDestinationContext.pathInfo 取到它：目标页 instanceof 判断的就是 push 时传入的这个对象，传无参就判不中（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.param；ets/component/nav_destination.d.ts，NavDestinationContext.pathInfo）
- onReady(callback: import('../api/@ohos.base').Callback<NavDestinationContext>): NavDestinationAttribute：目标页取路由参数的回调（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- import 目标页导出的参数类，用 query 的 title/date 构造后 push，目标页预填正常：按此改后通过收尾验证（出处：卡里修好并验证过）
- pushPathByName(name: string, param: Object, onPop: import('../api/@ohos.base').Callback<PopInfo>, animated?: boolean): void：同族接口：带出栈回调的重载，参数同样要传目标页的参数类（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：返回 Promise 的压栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：替换栈顶（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
针对本应用要查的：
- 源端每个页面从 query 读的键：源工程（Web 框架）里各页面组件读 URLSearchParams 或 location.search 的代码，以及深链监听交给路由的路径；按路由列出键名，对到目标页参数类的字段
未核实：卡里的环境是 HarmonyOS SDK 26.0.0，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-41e4b1f40ee7559e1a92（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
