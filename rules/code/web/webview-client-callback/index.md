# WebViewClient 的拦截和出错回调

agent 会看到什么：读到 WebViewClient 的 shouldOverrideUrlLoading、onReceivedError，或参考模板里无参的 .onErrorReceive；产物里 Web 的 .onLoadIntercept、.onErrorReceive 有没有判 isMainFrame()、isRequestGesture()

## 规矩

- rule-578149f1c053｜shouldOverrideUrlLoading 迁到 onLoadIntercept 时，先判主框架且手势触发｜读到：`WebViewClient.shouldOverrideUrlLoading` 只处理用户点开的链接（时码或外链），正文用 `loadDataWithBaseURL` 程序装载；写错：Web 的 .onLoadIntercept(...) 只判 isMainFrame()，再按 getRequestUrl() 逐字等于 baseUrl 或 'about:blank' 放行，其余主框架加载一律外开并 return true，正文停在 about:blank
- rule-10b7b07f2321｜Web 的 onErrorReceive 切整页失败态时，只在 isMainFrame() 为真时切｜读到：安卓端经 WebView（外部库承载、错误处理不可见）打开线上 H5；参考模板里是无参的 `.onErrorReceive(() => {})`；写错：Web 组件 .onErrorReceive(() => { … }) 没有事件参数或不判断 isMainFrame，里面直接置加载失败，显示覆盖整个 Web 区域的失败 / 重新加载卡片
