# WebView 的链接拦截和单页 H5 状态

agent 会看到什么：读到 WebView 有或没有 setWebViewClient、加载第三方单页 H5；产物里 Web 的 onOverrideUrlLoading、onPageEnd 里按 URL 的判断和 runJavaScript 探测

## 规矩

- rule-3b3260491f16｜没设 WebViewClient 的 WebView，用 onOverrideUrlLoading 把外链交浏览器｜读到：`WebView` 没有 `setWebViewClient`，页面里有外部 http(s) 链接和页内锚点；写错：`Web` 上没有拦截、链接在 Web 里打开；或拦截后交出的 `Want` 没有 `entities: ['entity.system.browsable']`、`startAbility` 失败只记日志不回退；或页内锚点、本地资源也被拦截
- rule-2b314551173d｜第三方单页 H5 切状态时 URL 可能不变，用 runJavaScript 探测页面标记判状态｜读到：安卓端 WebView 加载第三方单页 H5，H5 内部切换状态时地址栏不一定变化；写错：H5 状态只在 onOverrideUrlLoading / onPageEnd 里按 url.includes(...) 这类 URL 子串判定，没有 runJavaScript 探测页面内容
