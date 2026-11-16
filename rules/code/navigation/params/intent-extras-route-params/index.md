# Intent extra 迁成路由参数

agent 会看到什么：读到发起页 startActivity 前的 putExtra、启动器类构造器预置的 extras、接收端的 get…Extra / Fragment.newInstance 和按来源 extra 分支；产物里 pushPathByName / router.pushUrl 的参数对象、NavDestination 的参数类和 onReady 里对 pathInfo.param 的读取

## 通用查法

### Intent extra 迁成路由参数时，到接收端源码读出实际读取的键和取值再定参数

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

## 规矩

- rule-2b1f84e8d2fe｜迁 startActivity+putExtra 时，逐个 extra 核实接收 Activity 读了才映射成路由参数｜读到：发起页源码在 startActivity(intent) 前有 intent.putExtra(KEY_…, 值)；写错：目标页路由参数里给这个 extra 对应的字段赋了发起页的值，注释写「KEY_… → 接收 Activity」，而接收 Activity 没有用 getBooleanExtra / getStringExtra 等读它，或在创建 Fragment 时写死了这个值
- rule-560a46b4c53b｜调用方 putExtra 而接收方 Activity 从不读取的参数，目标页 onReady 里不新增入页动作｜读到：调用方用 Intent.putExtra("…", true) 启动某个 Activity，但接收方 Activity 里没有用 getIntent().getBooleanExtra / getStringExtra / getExtras() 读这个键；写错：目标页的参数类里新增了同名字段，并在 NavDestination 的 onReady 里读 pathInfo.param 的这个键，为 true 时调用登录、弹窗等入页动作
- rule-980e30b46bd8｜目标页参数字段注明由接收端固定时，发起页不用自身状态覆盖，不赋值或写该固定值｜读到：目标页已转换的参数类里，字段注释写明对应 Fragment.newInstance(...) 的某个参数、由 Activity 固定传值（如「Activity 固定传 false」），默认值就是这个固定值；写错：发起页构造目标页参数时照源端 putExtra 把自身同名状态赋给这个字段，覆盖了默认的固定值
- rule-145b5de1a714｜映射启动器打开页面时，核对构造器写入的默认 extras 与读取端默认值再选清栈或压栈｜读到：源端用启动器类打开页面：构造器里就 putExtra 写入清栈标志（如 clear_back_stack=false），调用处只链式加了要打开的对象再 start()；写错：目标把这类调用接成清栈切页（并持久化最后页）；或按目标侧清栈字段的默认值、注释选了分支，与源端构造器 `putExtra` 写入的值相反
- rule-0920cbf992ab｜安卓目标页由多个入口带不同 extra 启动并按来源分去向时，路由载荷带齐来源字段并实现各分支｜读到：目标 Activity 有多个静态启动方法（如 start(context, …) 和另一个只给某入口用的启动方法），各自 Intent.putExtra 不同的键；选中结果的处理按某个 extra 分支：一支 setResult(RESULT_OK, intent) 回传，另一支 startActivity 下一页后 finish()；写错：目标页只从 pathInfo.param 取一个字段、选中处固定 pop()；调用方 pushPathByName 的 param 里没有来源标志等字段
- rule-376c259dc888｜找不到源码或契约说只传 ID 时，保留页面已声明的来源参数并按来源出动作，不整体删减｜读到：源端打开结果页的静态 start(context, …, 来源常量, …) 带来源类型，结果页的 onClick 方法按来源分支进入编辑页；写错：目标端 router.pushUrl / pushPathByName 的参数只剩媒体 ID；页面路由参数接口里声明的来源字段没人传也没人读；底栏没有按来源出现的「下一步」
- rule-6c284df7d1ea｜NavDestination 参数类要导出并由所有 pushPathByName 调用方共用，或接收端按字段读｜读到：源端按 Intent extra 一类入口来源参数改变页面行为；参照规矩要求路由参数是声明的参数类实例、接收端 instanceof 判定；写错：参数类没有 export（文件私有），接收端 onReady 里 instanceof 判断；调用页 pushPathByName 推入的是自己另定义的类，来源标志恒为假
- rule-7f17fbe3039b｜多入口共享的目标页参数用一个载荷接口，调用方不用 as Object 或裸值绕过，目标页不收窄解析｜写错：某个入口的 pushPathByName 参数写成 `as Object` 强转或裸 number / string，和其他入口传的对象形状不同
- rule-7d14df7f1bb0｜源页从 Intent 或首页缓存拿列表数据时，目标 Param 或共享运行时给出等价来源，不留静态占位｜读到：源 Activity/Fragment 用 `bundle.getSerializable(...)` 取首页数据对象给列表赋值，或从首页缓存读数据（如 15 日列表）再按下标请求详情；写错：目标页面的 Param 只有城市、编码、经纬度等标识，列表初始化为空数组且没有任何赋值来源，或写成几条固定占位；forward-ref 只登记了加载函数
- rule-217f4d14aabb｜同一路由参数被分别当完整 JSON、ID、图片地址时，拆成三个字段或入口解析，不用 startsWith 屏蔽｜读到：调用方把完整的业务 JSON 写进路由参数；页面内又把同一个参数当 ID 拼进请求路径，或直接传给 Image(...) 当图片地址；写错：页面用 startsWith('{') / startsWith('[') 一类判断把 JSON 排除在预览之外，预览恒为占位；参数仍原样当 ID 去请求
- rule-2e60fbf25fd2｜构建修复补建缺失的模型时按规格数据流和上游 DTO 建模，不按一个调用方的字段补最少实现｜读到：规格数据流写着启动参数按已安装实例、用户组件、缓存 JSON 的顺序解析；上游 DTO 里已有预览地址和原始 JSON 两个字段；写错：补建的启动参数模型只有调用方用到的几个 ID 字段，没有承接缓存 JSON 的位置；从详情转模板时丢掉预览地址和原始 JSON；open() 不解析就拿参数原样请求 /{id}
