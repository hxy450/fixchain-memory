# 页面和组件的入参

源端有 Intent 的 putExtra / get…Extra、Bundle、Fragment 的 setArguments / newInstance / navArgs，目标端有路由参数对象、NavDestination 取参、子组件的 @Param 时

## 触发族

- [Intent extra 迁成路由参数](intent-extras-route-params/index.md)（12 条）：读到发起页 startActivity 前的 putExtra、启动器类构造器预置的 extras、接收端的 get…Extra / Fragment.newInstance 和按来源 extra 分支；产物里 pushPathByName / router.pushUrl 的参数对象、NavDestination 的参数类和 onReady 里对 pathInfo.param 的读取
- [源 Fragment 入参到目标页面和组件的传递](fragment-arguments/index.md)（3 条）：读到 Fragment 的 newInstance / setArguments / getArguments、requireArguments、navArgs，或宿主调 setter 注入参数；产物里子组件的 @Param / @Event、@Builder 插槽传没传参，以及目标页取参的代码
- [路由参数的有效性判定和错误态](route-param-validation/index.md)（2 条）：产物里页面从路由参数取 id 的默认值和有效性判定（id < 0、id <= 0），以及 build() 里错误态 if 分支和分支外的操作入口
- [打开设置子屏时经 Bundle 传的能力快照](settings-bundle-snapshot/index.md)（2 条）：读到源端打开设置页前用一串 bundle.put…(...) 把尺寸数组、取值范围、能力标志交给设置子屏，子屏各自 bundle.get…(...) 读；产物里构造快照的方法给哪些字段赋了值，子屏读不到某个键时是扩展共享模型、登记占位还是传空数组降级
- [NavDestination 路由参数类的定义、导出和取用](nav-param-class/index.md)（5 条）：产物里 pushPathByName / replacePathByName 传的参数类和接收页 onReady 里对 pathInfo.param 的 instanceof 判定：参数类定义在哪个文件、有没有 export、发送页是不是自建同形类、路由层或页面之间谁 import 谁、字段名是否照源端路由参数（routerLink、;id=），以及 onReady 赋值之前就拿参数去 subscribe
