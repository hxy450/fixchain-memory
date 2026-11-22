# 源 WebView 未设 WebViewClient 时链接按 Android 默认交给外部浏览器：拦截非本地 URL，用 viewData + entity.system.browsable 拉起，失败再由 Web 自行加载；页内锚点与本地资源放行

## 何时使用

界面实现阶段，把未设置 WebViewClient 的 Android WebView 迁移为 ArkWeb、确定链接点击的导航处理与外链打开写法时；复用其他页面已有的外链打开函数时

## 适用情境

源 Activity 只 findViewById 后 loadUrl 本地 asset HTML，没有 setWebViewClient；HTML 含页内锚点与外部 http(s) 链接；目标拦截外链后用 startAbility 打开，工程其他页面可能照抄同一个外链函数。

## 例外与边界

- 源端设置了 WebViewClient 并覆写 shouldOverrideUrlLoading：按其逻辑实现
- 源端设置了 WebViewClient 但没有覆写 shouldOverrideUrlLoading：默认实现返回 false，链接照常在 WebView 内打开，不按本条把外链交给浏览器
- 应用自己用 loadUrl 发起的加载（含远程 http(s) 首页）在源端不经这一判定、照常在 WebView 里打开；本条只管页面内点击、脚本和重定向发起的导航，拦截时放行应用自己发起的加载

## 原因

Android WebView 没有 WebViewClient 时，跨文档链接交给能处理 BROWSABLE 的外部应用，没有可处理的应用时才由 WebView 自行加载；目标 Web 默认在组件内导航。外链 Want 缺少 browsable 实体，不是拉起默认浏览器的标准写法，被其他页面“对齐”复用后同样带出。来源中帮助页已拦截 http(s) 并交给 viewData Want，但没有 browsable 实体、也没有失败回退，另一页面按“与该页对齐”原样复用。

## 做法

1. 用 onOverrideUrlLoading（或 onLoadIntercept）拦截非本地 URL，以 { action: 'ohos.want.action.viewData', entities: ['entity.system.browsable'], uri } 调 startAbility 打开外部浏览器，失败后再由 Web 自行 loadUrl（拦截回调对这次回退加载的 URL 放行，不在回调里对同一 URL 调 loadUrl 后又返回 true）；页内锚点与本地 rawfile 资源不拦截。
2. 复用已有外链打开函数前，核对 Want 字段是否包含 browsable 实体并符合本页源码的 ACTION_VIEW 语义，不按“与某页对齐”直接复制。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕安卓 WebView 没设 WebViewClient 时，URL 将要加载时默认请 Activity Manager 选合适的处理者打开；设了 WebViewClient 时 shouldOverrideUrlLoading 返回 true 中止当前 WebView 加载、返回 false 照常加载
- 〔做法第 1 步〕onOverrideUrlLoading 在 URL 将要加载进当前 Web 时回调；POST 请求不触发，子框架和非 HTTP(S) 协议也可能触发
- 〔做法第 1 步〕OnOverrideUrlLoadingCallback 返回 true 中止当前 Web 加载该 URL，返回 false 照常加载；声明注明：不应对请求的 URL 调 WebviewController.loadUrl 同时返回 true
- 〔做法第 1、2 步〕要被浏览器类应用匹配，被拉起方在 skills 里声明 actions 含 "ohos.want.action.viewData"、entities 含 "entity.system.browsable"；隐式 Want 带上这两项才与之对应
- 〔做法第 1 步〕UIAbilityContext.startAbility(want) 找不到可拉起的能力时以 BusinessError 16000001（The specified ability does not exist）拒绝
