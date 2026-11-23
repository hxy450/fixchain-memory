# WebView 排版与缩放按源端 WebSettings（未做设置时取 Android WebView 默认值）在 ArkWeb 中显式落实：HTML 声明 viewport，缩放与 JS 逐项对齐

## 何时使用

规格映射、页面实现与 HTML 产出阶段，把 WebView（含未调用任何 WebSettings 的 WebView）迁移到 ArkWeb、确定 Web 属性时

## 适用情境

源 WebView 通过设置按设备宽排版；目标 HTML 由独立服务产出，可能没有 viewport 声明。也包括源 Activity 只 loadUrl 本地 asset HTML、未修改任何 WebSettings，本地 HTML 没有 viewport meta；写者提出“对齐 Android 默认值”，只落实了 JS 一项。

## 例外与边界

- HTML 已有 viewport meta 的保留原样（包括其中的 width、initial-scale、user-scalable 等），只给没有声明的输出路径补，不要统一覆盖成 width=device-width, initial-scale=1。
- 补的 viewport meta 只在 Web 解析它时起作用：在 2in1 上不管怎么设都不解析；工程改过 User-Agent、其中没有 Mobile 字段时默认也不解析，这时要显式写 metaViewport(true)，“保持默认解析”不够。

## 原因

ArkWeb 无 viewport 时按桌面宽排版再整体缩小，正文字极小；规格笼统标“行为等价”时，这些设置不会传到 HTML 产出方。源端未做设置时，目标行为就是 Android WebView 的全部默认值：按 WebView 宽度排版（useWideViewPort=false）、没有缩放手势、JS 关闭；ArkWeb 在页面没有 viewport meta 时不按组件宽度排版，zoomAccess 默认为 true。

## 做法

1. 规格逐项写出 WebSettings 与回调触发范围的差异；无一对一属性时给出替代，如 head 注入 width=device-width, initial-scale=1 的 viewport。
2. 每条 HTML 输出路径（含空文案兜底）都在 head 中声明 viewport。
3. 源未修改 WebSettings 时逐项列出影响布局与交互的 Android 默认值，与 ArkWeb 默认值对照并显式设置：JS、缩放手势（Android 默认没有，写 zoomAccess(false)）、useWideViewPort/loadWithOverviewMode、总览模式与文本自动缩放（Android 未设置时 setLoadWithOverviewMode 为 false、布局算法为 NARROW_COLUMNS 而不是 TEXT_AUTOSIZING，对应写 overviewModeAccess(false)、textAutosizing(false)）。
4. 本地 HTML 没有 viewport meta 时，在 rawfile HTML 的 head 补 width=device-width, initial-scale=1，并保持 metaViewport 默认解析，不用 metaViewport(false) 模拟 useWideViewPort=false。

## 可选检查

- 首屏截图对照 Android：居中元素完整可见、正文字号一致，并试一次双指缩放核对缩放默认值

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 3、4 步〕安卓 setUseWideViewPort(false) 时布局宽度总是 WebView 控件的宽度（CSS 像素）；为 true 且页面有 viewport meta 时用其中的 width，页面没有该标签或没给 width 时用宽视口（源码注释没写这项的默认值）
- 〔原因 / 做法第 3 步〕应用没有另设 setJavaScriptEnabled 时，安卓 WebView 的 JS 关闭（默认 false）
- 〔原因 / 做法第 3 步〕应用没有另设 setBuiltInZoomControls、setSupportZoom 时，安卓 WebView 的内置缩放（含双指缩放手势）关闭（默认 false），setSupportZoom 为 true
- 〔做法第 3 步〕安卓 setLoadWithOverviewMode 决定是否按总览模式加载（内容宽于控件时缩小到按宽度放下）；应用没有另设它时为 false
- 〔做法第 3 步〕应用没有另设 setLayoutAlgorithm 时，安卓 WebView 的布局算法为 LayoutAlgorithm.NARROW_COLUMNS（已标废弃），不是 TEXT_AUTOSIZING
- 〔原因 / 做法第 3 步〕ArkWeb 的 javaScriptAccess、zoomAccess、overviewModeAccess 应用没有另设时都为 true：允许执行 JS、支持手势缩放、按总览模式加载
- 〔做法第 3、4 步〕ArkWeb 的 textAutosizing（API 12 起）应用没有另设时为 true，生效时把过小的字放大到 16px~32px；生效前提包括设备为手机、平板、穿戴或 TV，Web 视口宽度小于 980px，页面文字量够大，以及前端没有 viewport meta 或 viewport meta 里没有 width 和 initial-scale
- 〔做法第 4 步〕ArkWeb 的 metaViewport 应用没有另设时为 true（解析 viewport meta 并按它布局）；设为 false 时不解析、用默认布局；2in1 设备不管设什么都不解析；User-Agent 不含 Mobile 字段时默认不解析，显式设 true 可覆盖
- 〔原因〕设备上：HTML 没有 viewport 声明时，ArkWeb 按 980px 桌面宽排版再整体缩小，正文字极小
- 〔原因 / 做法第 4 步〕设备上：本地 HTML 没有 viewport meta 时，ArkWeb 不按 Web 组件宽度排版
