# ui/web

ArkWeb 承载 WebView：WebSettings 默认值、viewport、导航拦截与外链、控制器挂接时序

[上一级](../index.md)

## 本级经验

- [导航拦截按手势判用户点击，挂接后再 loadData](lesson-f095b7b87fbc8d8ed03d.lesson.md) · 阶段：execute · 信号：shouldOverrideUrlLoading, loadDataWithBaseURL, onLoadIntercept, isMainFrame
- [无 WebViewClient 时外链交系统浏览器](lesson-42cf412cacabb3c8c281.lesson.md) · 阶段：execute · 信号：WebViewClient, setWebViewClient, shouldOverrideUrlLoading, onOverrideUrlLoading
- [未设 WebSettings 时按安卓默认逐项显式设](lesson-65ebab594a9dabe77ac2.lesson.md) · 阶段：spec/execute · 信号：WebSettings, javaScriptAccess, zoomAccess, overviewModeAccess
