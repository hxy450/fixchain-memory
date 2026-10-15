# 源端覆写 shouldOverrideUrlLoading 时，ArkWeb 拦截只放行宿主发起的装载，脚本跳转、点击与重定向按源逻辑分发

ID：`lesson-f095b7b87fbc8d8ed03d` · 版本：3

[本主题](index.md)

## 何时使用

实现阶段，把覆写了 WebView.shouldOverrideUrlLoading 的导航处理迁移为 Web 组件 onLoadIntercept（或 onOverrideUrlLoading）时

## 适用情境

源端 WebViewClient 覆写 shouldOverrideUrlLoading（如把外链交给浏览器），并用 loadUrl/loadDataWithBaseURL 装载正文；目标 onLoadIntercept 对宿主自己的 loadUrl/loadData 装载同样回调，请求 URL 可能不是 baseUrl 原串。

## 例外与边界

- 源端没有设置 WebViewClient：链接按 Android 默认交给外部应用，见同主题未设 WebViewClient 的链接经验

## 原因

shouldOverrideUrlLoading 不为应用自己用 loadUrl/loadData 发起的装载回调，但页面脚本发起的跳转、用户点击链接与 HTTP 重定向都会回调，也可能为子框架回调（android/webkit/WebViewClient.java 注释）。目标拦截器若不排除宿主装载，正文自身的导航会被当外链拦掉，页面停在空白；只按 isRequestGesture() 放行，又会漏掉源端照常处理的脚本跳转与重定向；按猜测的请求 URL 逐字放行同样不可靠。

## 做法

1. 区分宿主装载与其他导航：onLoadIntercept 也为宿主自己的 loadUrl/loadData 回调，请求 URL 不一定是 baseUrl 原串，不按猜测的 URL 字面放行；需要按 URL 判断时先打印真实 getRequestUrl() 核对。
2. 源端只处理用户点击的链接时，用 isMainFrame() && isRequestGesture() 识别用户导航，其余放行。
3. 源端还处理脚本跳转或重定向（没有按 hasGesture() 门控）时，不只用 isRequestGesture() 过滤：脚本跳转与重定向（isRedirect()）照源处理，宿主装载的识别方式先在真机打印各请求的 getRequestUrl()、isRequestGesture()、isRedirect() 后确定；源端只处理主框架时才用 isMainFrame() 过滤子框架。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-60d268b503cb75aa01a2](../../../store/cases/case-60d268b503cb75aa01a2/4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c.json) · 结论：diagnosis, recommendation:1
  卡片版本：`4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c`
