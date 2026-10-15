# WebView 排版与缩放按源端 WebSettings（未设置取 Android 默认值）在 ArkWeb 显式设置并声明 viewport

ID：`lesson-65ebab594a9dabe77ac2` · 版本：4

[本主题](index.md)

## 何时使用

规格映射、页面实现与 HTML 产出阶段，把 WebView（含未调用任何 WebSettings 的 WebView）迁移到 ArkWeb、确定 Web 属性时

## 适用情境

源 WebView 通过设置按设备宽排版，或源 Activity 只 loadUrl 本地 asset HTML、未修改任何 WebSettings；目标 HTML 由独立服务产出或来自 rawfile，可能没有 viewport meta。

## 原因

ArkWeb 无 viewport 时按桌面宽排版再整体缩小，正文字极小；规格笼统标“行为等价”时，这些设置不会传到 HTML 产出方。源端未做设置时，目标行为就是 Android WebView 的全部默认值：按 WebView 宽度排版（useWideViewPort=false）、没有缩放手势、JS 关闭；ArkWeb 在页面没有 viewport meta 时不按组件宽度排版，zoomAccess 默认为 true。

## 做法

1. 规格逐项写出 WebSettings 与回调触发范围的差异；无一对一属性时给出替代，如 head 注入 width=device-width, initial-scale=1 的 viewport。
2. 每条 HTML 输出路径（含空文案兜底）都在 head 中声明 viewport。
3. 源未修改 WebSettings 时逐项对照 Android 默认值（出处为本机 SDK sources/android-36.1 的 android/webkit/WebSettings.java 注释）与 web.d.ts 中 ArkWeb 属性的默认值并显式设置：JS 默认关，写 javaScriptAccess(false)；builtInZoomControls 默认 false、没有缩放手势，写 zoomAccess(false)；loadWithOverviewMode 默认 false，而 overviewModeAccess 默认 true，写 overviewModeAccess(false)；布局算法默认不是 TEXT_AUTOSIZING，而 textAutosizing 默认 true（API 12 起），写 textAutosizing(false)；textZoom 与 textZoomRatio 默认都是 100。
4. useWideViewPort 为 false 时按 WebView 宽排版：本地 HTML 没有 viewport meta 时，在 rawfile HTML 的 head 补 width=device-width, initial-scale=1，并保持 metaViewport 默认解析，不用 metaViewport(false) 模拟。

## 可选检查

- 首屏截图对照 Android：居中元素完整可见、正文字号一致，并试一次双指缩放核对缩放默认值

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-60d268b503cb75aa01a2](../../../store/cases/case-60d268b503cb75aa01a2/4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c.json) · 结论：recommendation:3, recommendation:4, diagnosis
  卡片版本：`4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c`
- [case-68e0a1ed3d4f2117efdb](../../../store/cases/case-68e0a1ed3d4f2117efdb/aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:6
  卡片版本：`aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720`
