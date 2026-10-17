# WebView 排版与缩放按源端 WebSettings（未做设置时取 Android WebView 默认值）在 ArkWeb 中显式落实：HTML 声明 viewport，缩放与 JS 逐项对齐

ID：`lesson-65ebab594a9dabe77ac2` · 版本：4

[本主题](index.md)

## 何时使用

规格映射、页面实现与 HTML 产出阶段，把 WebView（含未调用任何 WebSettings 的 WebView）迁移到 ArkWeb、确定 Web 属性时

## 适用情境

源 WebView 通过设置按设备宽排版；目标 HTML 由独立服务产出，可能没有 viewport 声明。也包括源 Activity 只 loadUrl 本地 asset HTML、未修改任何 WebSettings，本地 HTML 没有 viewport meta；写者提出“对齐 Android 默认值”，只落实了 JS 一项。

## 原因

ArkWeb 无 viewport 时按桌面宽排版再整体缩小，正文字极小（默认视口宽度 980px，overviewModeAccess 未调用时默认开启概览模式；HarmonyOS 文档 arkts-basic-components-web-attributes，访问于 2026-10-17）；规格笼统标“行为等价”时，这些设置不会传到 HTML 产出方。源端未做设置时，目标行为就是 Android WebView 的全部默认值：按 WebView 宽度排版（useWideViewPort=false）、没有缩放手势、JS 关闭；ArkWeb 在页面没有 viewport meta 时不按组件宽度排版，zoomAccess 默认为 true。

## 做法

1. 规格逐项写出 WebSettings 与回调触发范围的差异；无一对一属性时给出替代，如 head 注入 width=device-width, initial-scale=1 的 viewport。
2. 每条 HTML 输出路径（含空文案兜底）都在 head 中声明 viewport。
3. 源未修改 WebSettings 时逐项列出影响布局与交互的 Android 默认值，与 ArkWeb 默认值对照并显式设置：JS（ArkWeb 的 javaScriptAccess 未调用时默认允许，与 Android 默认关闭相反，源未开 JS 时写 javaScriptAccess(false)）、缩放手势（Android 默认没有，写 zoomAccess(false)）、useWideViewPort/loadWithOverviewMode、文本自动缩放（ArkWeb 的 overviewModeAccess 与 textAutosizing（API 12 起）未调用时都默认开启，按 Android 默认值显式设置；两者在 PC/2in1 上无效果）（HarmonyOS 文档 arkts-basic-components-web-attributes，访问于 2026-10-17）。
4. 本地 HTML 没有 viewport meta 时，在 rawfile HTML 的 head 补 width=device-width, initial-scale=1，并保持 metaViewport 默认解析，不用 metaViewport(false) 模拟 useWideViewPort=false。

## 可选检查

- 首屏截图对照 Android：居中元素完整可见、正文字号一致，并试一次双指缩放核对缩放默认值

来源支持：3 张卡 · 已知 2 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

## 来源（按需复核）

- [case-60d268b503cb75aa01a2](../../../store/cases/case-60d268b503cb75aa01a2/4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`4c9e9c004967e82833493fa2cf9fa6df0cf9cf14bf3fab9df3ada7255951c08c`
- [case-68e0a1ed3d4f2117efdb](../../../store/cases/case-68e0a1ed3d4f2117efdb/aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:6
  卡片版本：`aaeef50585350b84b245d01b7fa8c65456ad2bf20bc44821d926afd957f81720`
- [case-9174c62c22f8d979372e](../../../store/cases/case-9174c62c22f8d979372e/eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa.json) · 结论：diagnosis, recommendation:2
  卡片版本：`eec4229b6f305745c835a372c2d8c2fb44e5a7937fa2f43696c8ce7707fe1efa`
