# 网页

源端有 WebView、WebViewClient、WebSettings、loadDataWithBaseURL，目标端有 Web 组件、WebviewController、onLoadIntercept、onErrorReceive 时

## 触发族

- [wrap_content 的 WebView](webview-wrap-content/index.md)（2 条）：读到 android:layout_height="wrap_content" 的 WebView（常在整页 ScrollView 里）；产物里 Scroll 内 Web 的测高（onPageEnd、scrollHeight）和滚动锁定
- [WebView 的链接拦截和单页 H5 状态](webview-url-callback/index.md)（2 条）：读到 WebView 有或没有 setWebViewClient、加载第三方单页 H5；产物里 Web 的 onOverrideUrlLoading、onPageEnd 里按 URL 的判断和 runJavaScript 探测
- [loadDataWithBaseURL 程序装载的正文](webview-load-data/index.md)（2 条）：读到 webView.loadDataWithBaseURL(baseUrl, data, "text/html", "utf-8", historyUrl)，常在数据加载完成的回调里调；产物里 controller.loadData 的参数个数、baseUrl 和清洗，以及调用前有没有等 onControllerAttached
- [WebViewClient 的拦截和出错回调](webview-client-callback/index.md)（2 条）：读到 WebViewClient 的 shouldOverrideUrlLoading、onReceivedError，或参考模板里无参的 .onErrorReceive；产物里 Web 的 .onLoadIntercept、.onErrorReceive 有没有判 isMainFrame()、isRequestGesture()
- [单页 H5 外面的原生返回和标题栏](webview-host-bar/index.md)（1 条）：读到安卓页面在 WebView 上方放原生返回和 Toolbar、加载第三方单页 H5；产物里 Web 上方的返回 / 标题 Row 被删掉，或控制它显隐的 @State 只置 false 不恢复
- [源 WebView 的 WebSettings 设置](webview-settings/index.md)（3 条）：读到源端 WebView 的 getSettings() 上调了或没调 setJavaScriptEnabled、setLoadWithOverviewMode、setUseWideViewPort 等，产物里是 Web 组件上的 javaScriptAccess、zoomAccess、overviewModeAccess、textAutosizing 开关和交给 Web 渲染的 HTML 里的 viewport
