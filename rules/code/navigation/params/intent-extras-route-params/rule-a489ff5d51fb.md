# Intent extra 迁成路由参数时，到接收端源码读出实际读取的键和取值再定参数

审的是：代码
触发（任一种）：
- 读到：发起页 startActivity 前 intent.putExtra(KEY, 值)，或启动器类构造器里预置 putExtra；接收端用 getIntent().getBooleanExtra / getStringExtra 或 Fragment.newInstance(...) 取用；写错的样子：目标页路由参数（pushPathByName / router.pushUrl 的 param）的字段和取值按发起端 putExtra、目标侧注释或默认值推断，没对照接收端的 get…Extra 读取
适用范围：把安卓 Intent extra 传参迁成 NavPathStack / router 路由参数，定参数字段、取值和接收端行为时
做法：
- 到接收 Activity / Fragment 的源码，按每个 extra 的 KEY 搜 get…Extra(、getExtras()、arguments，再看创建 Fragment 的 newInstance(...)：读不读、默认值是什么、读到后走哪个分支
- 取值按发起端或启动器构造器 putExtra 写入的值，没写入才用接收端默认值；只有被读取并生效的键写进目标页的参数接口，目标页照读取处的分支实现行为
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getBooleanExtra(String name, boolean defaultValue)：返回之前 putExtra() 放入的值，没有才返回 defaultValue：写入的值优先于读取端默认值；接收端不读的 extra 对界面不起作用（出处：android.content.Intent#getBooleanExtra）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 推页并传参（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- NavPathInfo.param?: unknown：接收端在 onReady 的 NavDestinationContext.pathInfo 里取到的页面参数（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathInfo.param）
针对本应用要查的：
- 接收端读了哪些 extra、默认值和读到后的分支：源工程里 Intent 指向的接收 Activity / Fragment 的 Java 或 Kotlin 文件：按 extra 的 KEY 常量全文搜 get…Extra(、getExtras()、arguments，并看 onCreate 里的 newInstance(...) / setArguments；被读取且读出的值传给了界面或 Fragment 的才算被消费；newInstance(...) 对应参数写成常量的，目标端这个字段取该常量
- 发起端或启动器类实际写入的值：调用点 startActivity 之前的 putExtra，以及启动器类构造器里的 putExtra；写入的值优先；都没写入时才看接收端 get…Extra 的默认值
来源：3 张卡，3 个应用
- case-05f3fb8501654bad9261（AntennaPod）：做法第 2 步 ← 建议 5
- case-72b2ae4850e7ef2a6ce2（记得日历）：做法第 1 步 ← 建议 1
- case-c12a47945c40bc682e71（免费来电多多）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
