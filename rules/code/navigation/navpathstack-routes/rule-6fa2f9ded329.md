# onReady 的参数可能是 JSON.parse 出的 DTO 时，不用 instanceof DTO 类判定

审的是：代码
触发（任一种）：
- 读到：源端在 Compose 的 NavHost 导航里把整个 data class 数据对象交给目标页，目标页提交只用它的 id、name 等字段；写错的样子：目标 onReady 里只写 if (param instanceof <DTO 类>) 才赋值，而这个 DTO 在工程里是 JSON.parse(body) as T 得到的普通对象
适用范围：目标页的路由参数可能来自 API / JSON 解析的数据对象，或来自多个生产页时
做法：
- 导出本页自己的参数类（只含提交要用的标量字段，如 id、name），onReady 用 instanceof 这个类收窄，生产端 new 它传入
- 或者对非实例的参数按 id / name 等字段收窄取值，不因 instanceof 不命中就退回默认对象
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- parse(text: string, reviver?: …): any：JSON.parse 返回普通对象，as T 只是编译期断言，运行时不是 T 的实例（出处：鸿蒙 SDK 的 ets/build-tools/ets-loader/node_modules/typescript/lib/lib.es5.d.ts，JSON.parse）
- onReady(callback: Callback<NavDestinationContext>): NavDestinationAttribute；参数在 context.pathInfo.param，类型是 unknown：目标页拿到的参数要自己收窄（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady；ets/component/navigation.d.ts，NavPathInfo.param）
- 改用按 id / name 收窄的辅助函数后，提交带上正确的 id：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 这个 DTO 在目标工程里是怎么产生的：目标工程的网络或数据层里返回这个类型的方法；看是 JSON.parse(...) as T 还是 new T(...)；是前者就不能用 instanceof 判定
来源：1 张卡，1 个应用
- case-2e5a8c9bed405f41a6ce（jerboa）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 3 ← 诊断
