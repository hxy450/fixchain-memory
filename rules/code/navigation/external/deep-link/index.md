# 深链的 intent-filter、navDeepLink 和 want.uri 解析

agent 会看到什么：读到 AndroidManifest 里带 android.intent.action.VIEW / BROWSABLE 和 <data android:scheme> 的 intent-filter、navDeepLink 的 uriPattern 或源端深链路由器；产物里 EntryAbility 的 onCreate / onNewWant 读 want.uri、URI 解析函数和导航栈的深链入口

## 规矩

- rule-f94848910dce｜源端有深链时，EntryAbility 的 onCreate 和 onNewWant 都读 want.uri 投递｜读到：AndroidManifest 的 Activity 带 `<intent-filter>`：`android.intent.action.VIEW`、`android.intent.category.BROWSABLE`、`<data android:scheme=… android:host=…>`；写错：EntryAbility.onCreate 只做初始化，不读 want.uri；没有覆写 onNewWant
- rule-5a61d906f676｜源端有深链路由器时，目标路由文件写 URI 解析函数和子路由表，导航栈提供深链入口｜读到：源导航模块里有把 `Uri` 映射到路由的深链路由器类，和 `const val` 定义的 `scheme://host` 深链常量；配置页说明里列了 Deep link 行；写错：路由文件只有路由表常量和按名查路由的函数，没有深链 scheme 常量和 URI 解析函数；导航栈（NavPathStack 的封装）只有 push、pop、clear，没有处理深链的入口
- rule-37cf6e54f3cb｜解析 want.uri 时按源端 uriPattern 锚定整串，不匹配就清空待处理状态｜读到：源端 Navigation DeepLink 的 uriPattern 写成 https://<host>/<路径>/{参数}，参数有类型（如数字 id）；写错：onCreate/onNewWant 把 want.uri 交给一个不带 ^…$ 的正则（只匹配 host/路径片段、不含 scheme，或带 /i），匹配不上时不清空上一次的待处理 id
- rule-90b1b32986d5｜深链解析器按 manifest 的 scheme 接受前缀，不认源端没有的 scheme｜读到：AndroidManifest 的深链 intent-filter 有 https 与 http 两个 scheme，navDeepLink 的 uriPattern 是域名常量加路径加 {id}；写错：want.uri 的解析器同时接受自拟 scheme 前缀和 `https://` 前缀，没有 `http://` 前缀
- rule-2f6fdf149c84｜深链 scheme 常量来自外部库时先核实值，核不到按 manifest 的 scheme 加冒号做前缀匹配｜读到：源端 getDataString().startsWith(<外部库常量>) 判深链，manifest 的 <data android:scheme=…> 只有 scheme、没有 host；写错：目标端 startsWith(...) 用的深链常量写成 `'<scheme>://'` 形式（预设了 //），注释称「值 per manifest / spec」，库里的实际值没核过
- rule-fb226d97faf0｜壳深链分发对每个目标路由用目标页导出的参数类传 query，不统一传无参｜读到：源端深链监听（如 AppUrlListener）把 pathname + search 整体交给 history.push，多个目标页各自用 URLSearchParams 读 query；目标页在 NavDestination 的 onReady 里用 instanceof 判断自己导出的参数类；写错：分发器只给本 feature 的路由构造参数类，其余路由一律 pushPathByName('<路由名>', 无参对象)，读 query 的页面拿到空参数（标题为空、日期 NaN 之类）
- rule-3e2294571111｜规格公式与已读源表达式不一致时，解析函数照源求值并上报 decision_gaps｜读到：规格写 `: ''` 守卫或要求过滤未注册路径，而读过的源端是 `"?" + x.split("?")[1]` 和只有 `if (x)` 的判断；写错：解析函数里无分隔符分支返回 `''`，或出现源端没有的注册路由表、未注册路径返回 `null`
- rule-eb9e700610ed｜URLSearchParams.get 改成手写解析时，先把 + 换成空格再 URI 解码｜读到：源端 new URLSearchParams(location.search).get(key) 读深链或路由 query 参数；写错：目标手写 split('&') / split('=') 后只做 decodeURIComponent(value)，没有先 replace(/\+/g, ' ')；?title=A+B 得到 'A+B'
- rule-e5c6fe3657da｜深链或路由的 query 解析写成可导出的工具函数，不写成 @Entry 页面的私有方法｜写错：query 取值函数写成 @Entry 页面里的 private 方法，多个深链或路由分支各自调用它或复制一份
