# 点击监听器里的跳转目标

agent 会看到什么：读到源页面的 setOnClickListener、onItemChildClick、onClick* 方法或弹窗配置里的链接回调，函数体里 startActivity / start(url) 到别的页；规格的行为契约、对接点、AC、导航表里写的入口和目标页

## 规矩

- rule-ffcb28e209ea｜页面有可点击入口时，规格逐个写出源码目标页、URL 常量和参数，不写「打开对应业务页」｜读到：源码的点击回调里调起目标：某个 Fragment 的 start(url) 打开 WebView 加载固定 URL，或 start(列表[i]) 打开详情 Fragment、startActivity(Intent)；写错：规格的行为契约只写「打开对应 H5 业务页」「进入对应业务」，没写每个入口的目标页、URL 常量和默认值、所带参数
- rule-1408c1f8b34c｜页面有多个点击入口时，规格按各监听器函数体逐个写「控件→调用→目标页」｜读到：源 Fragment / Activity 里有多个点击入口（`setOnBannerListener`、`onItemChildClick`、clickDelay 等监听器），规格作者只看过声明级的搜索结果，没展开函数体；写错：规格 AC 写「点击X进入Y；源:某Fragment」，Y 却不是该监听器函数体里实际跳转的页面；或几个入口并成一条，补出源码里没有的「列表项→详情」AC 和对接点
- rule-932a7fbeda36｜页面对接点只从该页布局和 Fragment 实际绑定的控件推导，不收共享 ViewModel 里没调用的方法｜读到：Fragment 只给部分控件挂 setOnClickListener；登录 SDK 类、事件类只出现在 import；共享 ViewModel 里有登录等方法，但该页没有调用；写错：规格「对接点」一节把共享 ViewModel 的方法写成该页入口（如「某页: 登录入口消费…」），或 AC 以 ViewModel 方法为源写成该页要有的功能
- rule-21ffa394a237｜源结果页按启动来源出的继续动作，规格逐个列出 onClick* 及其来源分支，写明来源由谁携带｜读到：源结果页读启动方传入的来源类型，某个 onClick* 方法只在特定来源时进入编辑页等跨功能页面；写错：功能契约的范围、AC 和状态交接只写结果保存，没列这个继续动作；路由参数写成只带稳定媒体 ID，没写来源类型由谁携带
- rule-6d4623f34240｜源端弹窗里有跳转回调时，源码理解笔记和 Spec Gap List 记下每个回调和目标｜读到：源端弹窗配置里有打开 WebView 页的链接回调；页面规格的导航表列着到 WebView 页的跳转；写错：源码理解笔记和 Spec Gap List 没记弹窗里的跳转回调，验收条目也没单列协议链接跳转
- rule-7ac02bb45ba3｜SDK 隐私弹窗配置带协议链接回调时，规格逐条写成验收项，并在导航表登记目标页｜读到：源码用 SDK 的隐私弹窗配置对象（如 PrivacyConfig）以回调属性声明行为：同意、拒绝之外还有 goServiceLink / goPrivacyLink 这类协议链接回调，打开 WebView 页；或者参考规格的对话框目录写着隐私概要框含「协议链接」；写错：功能规格的隐私验收只覆盖显示、外部点击不可关闭、同意持久化、拒绝退出、已同意不重复弹出，没有协议入口；页面导航表没有到 WebView 页的去向；「协议链接」只留在页面结构描述里
