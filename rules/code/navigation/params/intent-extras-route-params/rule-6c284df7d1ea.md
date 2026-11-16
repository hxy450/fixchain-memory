# NavDestination 参数类要导出并由所有 pushPathByName 调用方共用，或接收端按字段读

审的是：代码
触发（任一种）：
- 读到：源端按 Intent extra 一类入口来源参数改变页面行为；参照规矩要求路由参数是声明的参数类实例、接收端 instanceof 判定；写错的样子：参数类没有 export（文件私有），接收端 onReady 里 instanceof 判断；调用页 pushPathByName 推入的是自己另定义的类，来源标志恒为假
适用范围：经 NavPathStack 在多个调用页之间给同一个 NavDestination 传参时
做法：
- 导出参数类，所有 pushPathByName(name, new 参数类(...)) 调用方共用它；或接收端写 const p = ctx.pathInfo.param as 参数类 后按字段读取
- 写完后检索全部 push 该页面的调用点，确认实参能通过接收端的判断
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 推页并传参（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- pathInfo: NavPathInfo；NavPathInfo.param?: unknown：接收端在 onReady 的 NavDestinationContext 里取参数（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationContext.pathInfo；ets/component/navigation.d.ts，NavPathInfo.param）
- 参数改为 as 参数类后按字段读取：修好的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-766f31f27e3feb426eb4（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
