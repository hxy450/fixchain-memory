# 规格映射 WebView 时，逐项写 WebSettings 和回调触发范围的 ArkWeb 落点，不标「行为等价」

审的是：规格
触发（任一种）：
- 读到：源端 WebView 用 WebSettings 设 setUseWideViewPort(false)、setLoadWithOverviewMode(true)、cacheMode、mixedContentMode，并有 shouldOverrideUrlLoading；写错的样子：规格映射表里 WebView 那一行只写 loadData 签名和「onLoadIntercept 返回 true 截获」，结论标「行为等价」；没有视口、overview、缓存、混合内容的落点，也没写 onLoadIntercept 会为 loadData 自身导航回调
适用范围：规格提取阶段把安卓 WebView 映射到 ArkWeb Web 组件的那一行或那一节
做法：
- 逐项写 WebSettings 的 ArkWeb 落点；没有 1:1 属性的给替代，如 setUseWideViewPort(false) → HTML head 注入 <meta name="viewport" content="width=device-width, initial-scale=1">
- 写明回调触发范围的差异：shouldOverrideUrlLoading 不为程序装载回调，onLoadIntercept 会为 loadData 自身的主框架导航回调，判据写 isMainFrame()&&isRequestGesture()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setUseWideViewPort(false) 时布局宽度总是 WebView 控件的宽度（CSS 像素）：源端按设备宽排版的来源（出处：android.webkit.WebSettings#setUseWideViewPort）
- setLoadWithOverviewMode：内容宽于控件时缩小到屏宽，默认 false：源端 overview 设置的含义（出处：android.webkit.WebSettings#setLoadWithOverviewMode）
- metaViewport(enabled: boolean): WebAttribute，默认 true；2in1 设备不解析 viewport：ArkWeb 默认解析 HTML 里的 meta viewport，注入 meta 的替代才生效（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.metaViewport）
- HTML 没有 viewport 声明时 ArkWeb 按 980px 桌面宽排版再整体缩小，正文字极小；注入 width=device-width, initial-scale=1 后正常：不写视口落点的后果（出处：卡里修好并验证过）
针对本应用要查的：
- 源端 WebView 设了哪些 WebSettings：源工程里自定义 WebView 子类或宿主 Fragment 的初始化代码，按 getSettings() 后的 set… 调用找；逐个列出设置名和取值，每项在映射里写 ArkWeb 属性或替代写法
来源：1 张卡，1 个应用
- case-60d268b503cb75aa01a2（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 4 ← 诊断
