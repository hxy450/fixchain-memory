# .navDestination 直接传 @Builder 方法 this.destination，不再包一层箭头函数

审的是：代码
触发（任一种）：
- 写错的样子：写成 .navDestination((name, param) => this.destination(name, param))，用箭头函数包了一层 @Builder 方法
适用范围：Navigation 宿主用 @Builder 方法做路由映射时
做法：
- 写成 .navDestination(this.destination)，destination 是带 (name: string, param: unknown) 参数的 @Builder 方法
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- navDestination(builder: (name: string, param: unknown) => void): NavigationAttribute：路由映射的签名；箭头包装能过类型检查，但运行时取不到 builder（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.navDestination）
- 箭头包装时设备日志出现 Builder function is empty；改为 .navDestination(this.destination) 后正常：写错时的现象和修好的写法（出处：卡里修好并验证过）
- .navDestination(this.PagesMap)：官方示例同样直接传 @Builder 方法（出处：arkts-navigation-navdestination.md，页面显示类型示例）
未核实：卡里工程的 SDK 是 6.1.1(24)，本机按 API 23 核对
来源：1 张卡，1 个应用
- case-5fcc464cf9b9cd1034f1（android-panorama-map-vest7）：做法第 1 步 ← 建议 2、诊断；取值 2 ← 诊断
