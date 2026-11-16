# WebView 的 WebSettings 配置和导航回调

agent 会看到什么：读到源端 WebView 用 WebSettings 设 setUseWideViewPort、setLoadWithOverviewMode、cacheMode、mixedContentMode，并有 shouldOverrideUrlLoading；规格映射表里 WebView 只写 loadData 签名和「onLoadIntercept 截获」，标「行为等价」

## 规矩

- rule-1ea7d2c3621d｜规格映射 WebView 时，逐项写 WebSettings 和回调触发范围的 ArkWeb 落点，不标「行为等价」｜读到：源端 WebView 用 WebSettings 设 setUseWideViewPort(false)、setLoadWithOverviewMode(true)、cacheMode、mixedContentMode，并有 shouldOverrideUrlLoading；写错：规格映射表里 WebView 那一行只写 loadData 签名和「onLoadIntercept 返回 true 截获」，结论标「行为等价」；没有视口、overview、缓存、混合内容的落点，也没写 onLoadIntercept 会为 loadData 自身导航回调
