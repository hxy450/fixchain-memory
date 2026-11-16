# 源 WebView 没改 WebSettings 时，Web 组件逐项显式写出 Android 默认值，不只对齐 JS

审的是：代码
触发（任一种）：
- 读到：`WebView` 只 findViewById 后 loadUrl，没有任何 `getSettings()` / `WebSettings` 调用；写错的样子：`Web` 组件上 `.javaScriptAccess(false)`、`.zoomAccess(false)`、`.overviewModeAccess(false)`、`.metaViewport(false)`、`.textAutosizing(false)` 缺几项或全缺（如只写了 JS 一项，或只设宽高和 onLoadIntercept）
适用范围：安卓 WebView 没有修改任何 WebSettings、迁成 ArkWeb Web 组件时，影响布局与交互的那几项设置
做法：
- 逐项对照两边默认值显式写：Web({ src, controller }).javaScriptAccess(false).zoomAccess(false).overviewModeAccess(false)；Android 默认 JS 关、无缩放手势、不按总览模式加载，ArkWeb 这三项默认都是 true
- 文本自动缩放也显式写 .textAutosizing(false)：源端没调 setLayoutAlgorithm 时 Android 默认是 NARROW_COLUMNS 而不是 TEXT_AUTOSIZING，ArkWeb 的 textAutosizing 默认 true
- 再写 .metaViewport(false)：源端没开 setUseWideViewPort 时布局宽度即控件宽度，ArkWeb 这项默认 true
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- javaScriptAccess(javaScriptAccess: boolean): WebAttribute，默认 true：ArkWeb 默认允许执行 JS，Android 默认不允许（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.javaScriptAccess）
- zoomAccess(zoomAccess: boolean): WebAttribute，默认 true：ArkWeb 默认支持手势缩放（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.zoomAccess）
- overviewModeAccess(overviewModeAccess: boolean): WebAttribute，默认 true：ArkWeb 默认按总览模式（把内容缩到屏宽）加载（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.overviewModeAccess）
- textAutosizing(textAutosizing: boolean): WebAttribute，默认 true（@since 12）；metaViewport(enabled: boolean): WebAttribute，默认 true：ArkWeb 默认对小字号文本自动放大、默认解析页面的 meta viewport（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.textAutosizing / WebAttribute.metaViewport）
- setJavaScriptEnabled 默认 false；setBuiltInZoomControls 默认 false；setLoadWithOverviewMode 默认 false：源端没调用时 JS 关闭、没有双指缩放、不按总览模式加载（出处：android.webkit.WebSettings#setJavaScriptEnabled、android.webkit.WebSettings#setBuiltInZoomControls、android.webkit.WebSettings#setLoadWithOverviewMode）
- setLayoutAlgorithm 默认 LayoutAlgorithm.NARROW_COLUMNS：源端没调用时不是 TEXT_AUTOSIZING（出处：android.webkit.WebSettings#setLayoutAlgorithm）
- useWideViewPort 为 false 时布局宽度总是 WebView 控件宽度：源端默认不按 meta viewport 布局，对应 metaViewport(false)（出处：android.webkit.WebSettings#setUseWideViewPort）
- metaViewport、overviewModeAccess、zoomAccess、javaScriptAccess、textAutosizing 五项显式设置：修复后与源端默认一致（出处：卡里修好并验证过）
未核实：卡里的观察出自 HarmonyOS 6.1.1(24)，本机声明按 API 23 核实；case-68e0a1ed3d4f2117efdb 没写明 textAutosizing 取什么值（case-9174c62c22f8d979372e 写 false 并修好）；NARROW_COLUMNS 下安卓是否等同于不做文本自动缩放没核实；生成态在 ArkWeb 默认 overviewModeAccess 下具体怎样缩放显示，卡里没核实
来源：2 张卡，2 个应用
- case-68e0a1ed3d4f2117efdb（MifareClassicTool）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 3
- case-9174c62c22f8d979372e（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2、诊断；取值 8 ← 诊断
