# 多入口共享的目标页参数用一个载荷接口，调用方不用 as Object 或裸值绕过，目标页不收窄解析

审的是：代码
触发（任一种）：
- 写错的样子：某个入口的 pushPathByName 参数写成 `as Object` 强转或裸 number / string，和其他入口传的对象形状不同
- 写错的样子：目标页把 pathInfo.param 解析成 typeof param === 'number' / 'string' 只认一种形状，其他入口传的对象被当成空值
- 读到：巡检报告指出某调用方 pushPathByName 的参数形状和目标页 pathInfo.param 的解析不一致；写错的样子：修复只把这一个调用方的 pushPathByName 参数改成迎合目标页当前的解析（改传裸字符串），其他入口没查
适用范围：一个 NavDestination 目标页被多个入口用 pushPathByName 打开、载荷由不同任务分别写入时
做法：
- 在路由契约文件里给这个目标页定义一个 interface，字段覆盖所有入口的来源字段；每个入口都传这个类型的对象，新入口要新字段时扩展这个接口并同步所有调用方和目标页解析
- 目标页把 pathInfo.param 按这个接口解析，不为某一个入口收窄成 number / string
- 发现形状不一致时，搜目标页名在所有 pushPathByName 调用里的参数，按契约两端一起改，并对照安卓结果处理分支核对每个入口带的来源字段和去向
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：param 声明为 unknown，编译器不检查各入口传的形状是否一致，一致只能靠共享接口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- NavPathInfo.param?: unknown：目标页收到的载荷类型是 unknown，要按共享接口解析（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.param）
- 统一成一个带来源字段的载荷接口，三个入口传同一载荷，目标页按它解析来源并分支：修好后的形态（出处：卡里修好并验证过）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：NavPathStack 按页名入栈并返回 Promise，载荷同样要用共享接口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：NavPathStack 按页名替换栈顶，载荷同样要用共享接口（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
未核实：卡里环境是 API 24（6.1.1），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-914a0da87d6ea90ab419（android-panorama-map-vest7）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 4；取值 3 ← 诊断
