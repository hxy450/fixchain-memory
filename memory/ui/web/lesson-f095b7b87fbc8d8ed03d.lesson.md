# ArkWeb 导航拦截按请求属性区分用户导航，loadData 在控制器挂接后调用

ID：`lesson-f095b7b87fbc8d8ed03d` · 版本：1

[本主题](index.md)

## 何时使用

实现阶段，把 WebView.shouldOverrideUrlLoading 与 loadDataWithBaseURL 迁移为 Web 组件、onLoadIntercept 与 controller.loadData 时

## 适用情境

源 shouldOverrideUrlLoading 只处理用户点开的链接，不为程序装载回调；目标 onLoadIntercept 对初始装载同样回调。

## 原因

按猜测的 loadData 请求 URL 逐字放行，会把正文自身的导航当外链拦掉，页面停在空白；控制器未挂接时调用 loadData 不生效。

## 做法

1. onLoadIntercept 先判 isMainFrame() 且 isRequestGesture()，再分发外链；确需按 URL 判断时先打印真实 getRequestUrl()。
2. 以 onControllerAttached 置位为前提调用 loadData，未挂接时缓存数据、挂接后补发一次。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-60d268b503cb75aa01a2](../../../store/cases/case-60d268b503cb75aa01a2/4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c`
