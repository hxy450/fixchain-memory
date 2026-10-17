# 源 WebView 未设 WebViewClient 时链接按 Android 默认交给外部浏览器：拦截非本地 URL，用 viewData + entity.system.browsable 拉起，失败再由 Web 自行加载；页内锚点与本地资源放行

ID：`lesson-42cf412cacabb3c8c281` · 版本：2 · 阶段：execute · 主题：[ui/web](index.md)

概要：无 WebViewClient 时外链交系统浏览器

信号：`WebViewClient`, `setWebViewClient`, `shouldOverrideUrlLoading`, `onOverrideUrlLoading`, `onLoadIntercept`, `ohos.want.action.viewData`, `entity.system.browsable`, `startAbility`, `ACTION_VIEW`, `rawfile`, `loadUrl`

## 何时使用

界面实现阶段，把未设置 WebViewClient 的 Android WebView 迁移为 ArkWeb、确定链接点击的导航处理与外链打开写法时；复用其他页面已有的外链打开函数时

## 适用情境

源 Activity 只 findViewById 后 loadUrl 本地 asset HTML，没有 setWebViewClient；HTML 含页内锚点与外部 http(s) 链接；目标拦截外链后用 startAbility 打开，工程其他页面可能照抄同一个外链函数。

## 例外与边界

- 源端设置了 WebViewClient 并覆写 shouldOverrideUrlLoading：按其逻辑实现

## 原因

Android WebView 没有 WebViewClient 时，跨文档链接交给能处理 BROWSABLE 的外部应用，没有可处理的应用时才由 WebView 自行加载；目标 Web 默认在组件内导航。外链 Want 缺少 browsable 实体，不是拉起默认浏览器的标准写法，被其他页面“对齐”复用后同样带出。来源中帮助页已拦截 http(s) 并交给 viewData Want，但没有 browsable 实体、也没有失败回退，另一页面按“与该页对齐”原样复用。

## 做法

1. 用 onOverrideUrlLoading（或 onLoadIntercept）拦截非本地 URL，以 { action: 'ohos.want.action.viewData', entities: ['entity.system.browsable'], uri } 调 startAbility 打开外部浏览器，失败后再由 Web 自行 loadUrl；页内锚点与本地 rawfile 资源不拦截。
2. 复用已有外链打开函数前，核对 Want 字段是否包含 browsable 实体并符合本页源码的 ACTION_VIEW 语义，不按“与某页对齐”直接复制。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [未设 WebSettings 时按安卓默认逐项显式设](lesson-65ebab594a9dabe77ac2.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-68e0a1ed3d4f2117efdb](../../../../store/cases/case-68e0a1ed3d4f2117efdb/aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720.json) · 结论：diagnosis, rec-0686e4747c, rec-d67789c77d
  卡片版本：`aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720`
