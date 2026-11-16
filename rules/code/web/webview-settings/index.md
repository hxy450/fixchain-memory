# 源 WebView 的 WebSettings 设置

agent 会看到什么：读到源端 WebView 的 getSettings() 上调了或没调 setJavaScriptEnabled、setLoadWithOverviewMode、setUseWideViewPort 等，产物里是 Web 组件上的 javaScriptAccess、zoomAccess、overviewModeAccess、textAutosizing 开关和交给 Web 渲染的 HTML 里的 viewport

## 通用查法

### WebView 的 WebSettings 逐项查源端值或 Android 默认值，和 ArkWeb 不同的显式写

审的是：代码
触发（任一种）：
- 读到：源端 WebView 的 getSettings() 上调了或没调 setJavaScriptEnabled、setLoadWithOverviewMode、setUseWideViewPort 等；写错的样子：Web 组件只写了 .javaScriptAccess(...)，其余开关沿用 ArkWeb 默认；或交给 Web 的 HTML 没有 viewport meta
适用范围：安卓 WebView 迁成 ArkWeb Web 组件时，影响排版和交互的 WebSettings 各项
做法：
- 在源端拿到 WebView 的那段代码里找 getSettings() 上的每个 set… 调用，读出源端设的值；没调的项到 android.webkit.WebSettings 对应 setter 的注释读默认值
- 到鸿蒙 SDK 的 ets/component/web.d.ts 找 WebAttribute 上的同义开关读默认值，两边不同的在 Web 上显式写（如 .zoomAccess(false)）；源端 setUseWideViewPort(false) 时，交给 Web 的 HTML 每条路径都写 viewport meta
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- javaScriptAccess、zoomAccess、overviewModeAccess、textAutosizing 在 ArkWeb 默认都是 true：源端关着的这几项要显式写（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.javaScriptAccess、WebAttribute.zoomAccess、WebAttribute.overviewModeAccess、WebAttribute.textAutosizing）
- setJavaScriptEnabled、setBuiltInZoomControls、setLoadWithOverviewMode 默认 false；setLayoutAlgorithm 默认 NARROW_COLUMNS：源端没调这些 setter 时的取值（出处：android.webkit.WebSettings#setJavaScriptEnabled、WebSettings#setBuiltInZoomControls、WebSettings#setLoadWithOverviewMode、WebSettings#setLayoutAlgorithm）
- metaViewport(enabled: boolean): WebAttribute，默认 true；2in1 设备不解析 viewport：HTML 里写的 viewport 默认会被解析（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.metaViewport）
- <meta name="viewport" content="width=device-width, initial-scale=1">：带条件的例子：源端 setUseWideViewPort(false)、HTML 本身没有 viewport 时，各路径都注入后正文按设备宽排版（出处：卡里修好并验证过）
针对本应用要查的：
- 源端每项 WebSettings 的实际值：源工程里创建或 findViewById 拿到 WebView 的 Activity / Fragment，按 getSettings() 找 set… 调用；调了的取调用参数，没调的取 WebSettings 对应 setter 注释里的默认值。例：源端没调任何 setter 时，Web 写 .javaScriptAccess(false).zoomAccess(false).overviewModeAccess(false)
未核实：textAutosizing 取什么值卡里没写明；NARROW_COLUMNS 下安卓是否等同于不做文本自动缩放没核实；WebSettings 其余各项与 WebAttribute 的对应和默认值，族里规矩没有查实；卡里的观察出自 HarmonyOS 6.1.1(24)，本机声明按 API 23 核实
来源：2 张卡，2 个应用
- case-60d268b503cb75aa01a2（AntennaPod）：做法第 2 步 ← 建议 4；取值 4 ← 诊断
- case-68e0a1ed3d4f2117efdb（MifareClassicTool）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 3

## 规矩

- rule-c36e3604ae7d｜源 WebView 没改 WebSettings 时，Web 组件逐项显式写出 Android 默认值，不只对齐 JS｜读到：`WebView` 只 findViewById 后 loadUrl，没有任何 `getSettings()` / `WebSettings` 调用；写错：`Web` 组件上 `.javaScriptAccess(false)`、`.zoomAccess(false)`、`.overviewModeAccess(false)`、`.metaViewport(false)`、`.textAutosizing(false)` 缺几项或全缺（如只写了 JS 一项，或只设宽高和 onLoadIntercept）
- rule-8fac5e5fa2aa｜源端靠 WebSettings 按设备宽排版时，产出给 ArkWeb 的 HTML 每条路径都注入 viewport｜读到：源端 WebSettings 有 setUseWideViewPort(false) / setLoadWithOverviewMode(true)，清洗出的 HTML 本身没有 viewport；写错：目标产出给 Web 渲染的 HTML 里，某条路径（含空文案兜底）的 <head> 没有 <meta name="viewport" …>，只有 style 注入或空的 <head></head>
