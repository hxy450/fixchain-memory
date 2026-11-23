# ArkWeb 导航拦截按请求属性区分用户导航，loadData 在控制器挂接后调用

## 何时使用

实现阶段，把 WebView.shouldOverrideUrlLoading 与 loadDataWithBaseURL 迁移为 Web 组件、onLoadIntercept 与 controller.loadData 时

## 适用情境

源 shouldOverrideUrlLoading 只处理用户点开的链接，不为程序装载回调；目标 onLoadIntercept 对初始装载同样回调。

## 例外与边界

- 先判 isRequestGesture() 的前提是源端拦截只针对用户点开的链接。安卓 shouldOverrideUrlLoading 除用户点击外，也为网页脚本发起的导航和 HTTP 重定向回调（只是不为应用自己 loadUrl 的装载回调）；源端靠它把这类非点击导航也分发出去时，不能只处理手势请求，其余主框架导航按源端的 URL 规则判断，规则对照打印出的真实 getRequestUrl() 来写。

## 原因

按猜测的 loadData 请求 URL 逐字放行，会把正文自身的导航当外链拦掉，页面停在空白；控制器未挂接时调用 loadData 不会装载，而是抛出 17100001 错误。

## 做法

1. onLoadIntercept 先判 isMainFrame() 且 isRequestGesture()，再分发外链；确需按 URL 判断时先打印真实 getRequestUrl()。
2. 以 onControllerAttached 置位为前提调用 loadData，未挂接时缓存数据、挂接后补发一次。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕安卓 shouldOverrideUrlLoading 不为应用自己用 loadUrl() 发起的导航回调，只报网页发起（如 JavaScript）、用户点击和 HTTP 重定向的导航；POST 请求也不回调
- 〔适用情境 / 做法第 1 步〕onLoadIntercept 在导航触发时回调（包括 iframe 导航）；返回 true 取消此次导航，false 允许，返回 undefined 或 null 按 false
- 〔原因 / 做法第 1 步〕设备上：onLoadIntercept 对 loadData 装载正文时的主框架导航也会回调，回调里的请求 URL 不是传给 loadData 的 baseUrl 原串
- 〔做法第 1 步〕onOverrideUrlLoading 在 URL 将要加载到当前 Web 时回调，返回 true 阻止加载；loadUrl 主动触发的跳转和 POST 请求不触发
- 〔做法第 2 步〕onControllerAttached 在 WebviewController 成功绑定到 Web 组件时回调；在此之前调用 Web 相关接口会抛 js-error
- 〔原因 / 做法第 2 步〕WebviewController 还没关联到 Web 组件时调用 loadData 抛 BusinessError 17100001（The WebviewController must be associated with a Web component.）
