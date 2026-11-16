# 安卓目标页由多个入口带不同 extra 启动并按来源分去向时，路由载荷带齐来源字段并实现各分支

审的是：代码
触发（任一种）：
- 读到：目标 Activity 有多个静态启动方法（如 start(context, …) 和另一个只给某入口用的启动方法），各自 Intent.putExtra 不同的键；选中结果的处理按某个 extra 分支：一支 setResult(RESULT_OK, intent) 回传，另一支 startActivity 下一页后 finish()；写错的样子：目标页只从 pathInfo.param 取一个字段、选中处固定 pop()；调用方 pushPathByName 的 param 里没有来源标志等字段
适用范围：安卓一个 Activity 被多个入口以不同 Intent extra 启动、结果去向随来源而变，迁成 Navigation 下的 NavDestination 页时
做法：
- 把目标 Activity 的全部启动方法和各自的 extra 列成表，载荷接口逐项带上这些字段（来源标志、类型、关键词）；每个入口都用 pushPathByName(页名, 载荷) 传这个接口的对象，按自己的源端启动方法填值
- 目标页从 NavDestinationContext.pathInfo.param 解析全部来源字段，在选中处逐个实现分支：源端 startActivity 下一页再 finish() 的那支写成 pathStack.pop() 后 pathStack.pushPathByName(下一页名, 参数)；源端 setResult 回传的那支照原回传逻辑做完再 pop()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 按页名入栈，param 是目标页收到的载荷（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- pathInfo: NavPathInfo；NavPathInfo.param?: unknown：目标页在 NavDestinationContext.pathInfo.param 里取到入口传的载荷，类型是 unknown，要按载荷接口解析（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationContext.pathInfo；ets/component/navigation.d.ts，NavPathInfo.param）
- pop(animated?: boolean): NavPathInfo | undefined：NavPathStack 弹出栈顶页（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pop）
- 来源要求跳下一页时，先 pop() 当前页再 pushPathByName 下一页：对应源端 startActivity 下一页后 finish() 的分支（出处：卡里修好并验证过）
- constructor(name: string, param: unknown, onPop?: import('../api/@ohos.base').Callback<PopInfo>, isEntry?: boolean)：同族接口：NavPathInfo 的构造，用 pushPath / pushDestination 入栈时载荷同样放在 param（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.constructor）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：NavPathStack 按页名入栈并返回 Promise（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- setResult(int resultCode, Intent data)：源端回传分支：把结果交回启动它的调用方（出处：android.app.Activity#setResult）
针对本应用要查的：
- 目标页有哪些启动入口、各带哪些 extra、结果处理按哪个 extra 分支：源工程里目标 Activity 的 Kotlin/Java 文件：伴生对象或静态方法里的 Intent.putExtra，选中处理里的 if/when 分支；再搜调用这些启动方法的 Activity/Fragment；每个启动方法记下它放的键和值，每个分支记下条件和去向（setResult 回传或跳哪一页），逐项对到载荷字段和目标页分支
未核实：卡里环境是 API 24（6.1.1），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-914a0da87d6ea90ab419（android-panorama-map-vest7）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 4 ← 诊断
