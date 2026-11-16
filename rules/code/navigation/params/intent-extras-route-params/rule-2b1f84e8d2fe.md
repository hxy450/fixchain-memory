# 迁 startActivity+putExtra 时，逐个 extra 核实接收 Activity 读了才映射成路由参数

审的是：代码
触发（任一种）：
- 读到：发起页源码在 startActivity(intent) 前有 intent.putExtra(KEY_…, 值)；写错的样子：目标页路由参数里给这个 extra 对应的字段赋了发起页的值，注释写「KEY_… → 接收 Activity」，而接收 Activity 没有用 getBooleanExtra / getStringExtra 等读它，或在创建 Fragment 时写死了这个值
- 读到：`forward-ref` 占位登记里的「携带参数」说明（按发起端 putExtra 写的）；写错的样子：代码照占位登记的说明给目标页参数赋值，注释只写 putExtra 的 KEY，没写接收端源码依据
适用范围：把安卓跨 Activity 跳转迁成鸿蒙页面路由、决定哪些发起页状态要透传时
做法：
- 逐个 extra 到接收 Activity 核实：有没有被 getIntent().get…Extra(KEY, …) 读取、创建 Fragment 时是否被硬编码覆盖；只有被读取并生效的 extra 才映射成路由参数
- 占位登记里的「携带参数」只当发起端线索，接线时与接收端核对；冲突时以接收端实际语义为准，并在注释里写明依据的接收端源码
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getBooleanExtra(String name, boolean defaultValue)：返回 putExtra() 放进去的值，找不到时返回默认值：extra 只有接收端调用 get…Extra 读取才有作用；接收端不读，发起端 putExtra 的值不影响界面（出处：android.content.Intent#getBooleanExtra）
- putExtra(String name, boolean value)：Add extended data to the intent：putExtra 只描述发起端放了什么（出处：android.content.Intent#putExtra）
针对本应用要查的：
- 接收 Activity 实际读了哪些 extra、给 Fragment 传的是什么：源工程里 new Intent(…, 接收类) 指向的那个 Activity 的 .java / .kt 源文件：按 extra 的 KEY 常量全文搜 get…Extra(、getExtras()，再看 onCreate 里创建 Fragment 的 newInstance(...) 或 setArguments 调用；KEY 被读取且读出的值传给了 Fragment 或界面的，才算被消费；newInstance(...) 对应参数写的是常量的，目标端该字段取这个常量，发起端不透传
未核实：卡里上机所用 SDK 是 API 24（6.1.1）
来源：1 张卡，1 个应用
- case-c12a47945c40bc682e71（免费来电多多）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 3
