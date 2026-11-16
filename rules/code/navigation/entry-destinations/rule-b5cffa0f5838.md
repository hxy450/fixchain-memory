# 可见入口的点击处理只有 FWD-REF 注释和 return 时，按源码目标实现跳转

审的是：代码
触发（任一种）：
- 读到：源端点击回调打开固定 URL 的 WebView 页，或带列表索引参数打开详情 Fragment；写错的样子：目标端对应的点击处理函数体只有 `// FWD-REF: …` 注释和 `return;`
适用范围：页面上横幅、图片等可见入口的 onClick 处理
做法：
- 固定 URL 的 WebView 目标：新建一个页面，用 Web({ src: <源端 URL 默认值>, controller: new webview.WebviewController() }) 加载，点击时跳到这个页面
- 带参数的详情目标：新建详情页，点击时把源端传的参数（如列表索引 index）带过去，详情页按它取对应内容
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (value: WebOptions): WebAttribute：Web 组件的构造，WebOptions 里 src 是要加载的地址（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebInterface）
- src: string | Resource；controller: WebController | WebviewController：WebOptions 的两个必填项（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebOptions.src、WebOptions.controller）
- webview.WebviewController：控制 Web 组件的控制器，一个对象只控制一个 Web 组件，方法要在绑定之后调用（出处：鸿蒙 SDK 的 ets/api/@ohos.web.webview.d.ts，webview.WebviewController）
- 新增 WebView 目标页加载源端 URL、详情页带 index 跳转后，入口点击与安卓一致；两页都是小页面，几分钟内完成：修好后的写法（出处：卡里修好并验证过）
未核实：卡里没写跳转用的是 Navigation 还是 router
来源：1 张卡，1 个应用
- case-4042c8947009b8610581（android-train-ticket-vest7）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；取值 4 ← 诊断
