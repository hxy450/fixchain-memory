# 源 WebView 未设 WebViewClient 时外链交给外部浏览器：Want 带 browsable 实体，失败再由 Web 加载

ID：`lesson-42cf412cacabb3c8c281` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把未设置 WebViewClient 的 Android WebView 迁移为 ArkWeb、确定链接点击的导航处理与外链打开写法时；复用其他页面已有的外链打开函数时

## 适用情境

源 Activity 只 findViewById 后 loadUrl 本地 asset HTML，没有 setWebViewClient，公共基类与初始化工具也没有安装 Client；HTML 含页内锚点与外部 http(s) 链接；目标拦截外链后用 startAbility 打开，工程其他页面可能照抄同一个外链函数。

## 例外与边界

- 源端设置了 WebViewClient（含不覆写 shouldOverrideUrlLoading 的默认实例，此时链接在 WebView 内加载），或公共基类、初始化工具装了 Client：按实际实现处理；覆写了 shouldOverrideUrlLoading 的见同主题导航拦截经验

## 原因

Android WebView 没有 WebViewClient 时，跨文档链接交给能处理 BROWSABLE 的外部应用，没有可处理的应用时才由 WebView 自行加载；目标 Web 默认在组件内导航。外链 Want 缺少 browsable 实体，不是拉起默认浏览器的标准写法，被其他页面“对齐”复用后同样带出。

## 做法

1. 用 onOverrideUrlLoading（或 onLoadIntercept）拦截非本地 URL，以 { action: 'ohos.want.action.viewData', entities: ['entity.system.browsable'], uri } 调 startAbility 打开外部浏览器，失败后再由 Web 自行 loadUrl；页内锚点与本地 rawfile 资源不拦截。
2. 复用已有外链打开函数前，核对 Want 字段是否包含 browsable 实体并符合本页源码的 ACTION_VIEW 语义，不按“与某页对齐”直接复制。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-68e0a1ed3d4f2117efdb](../../../store/cases/case-68e0a1ed3d4f2117efdb/aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720.json) · 结论：diagnosis, recommendation:4, recommendation:5
  卡片版本：`aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720`
