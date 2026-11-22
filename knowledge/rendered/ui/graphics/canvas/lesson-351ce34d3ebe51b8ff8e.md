# ArkUI Canvas 的内容跨帧保留：把 onDraw 移植为反复调用的 render() 时每帧先清屏，再按源顺序绘制

## 何时使用

渲染实现阶段，把源端 onDraw 改为在同一 ArkUI Canvas 上反复调用的 render()、确定每帧起始画面时，含把一次性烘焙的背景位图改成每帧矢量重绘

## 适用情境

源端自定义 View 由 setBackgroundColor 设背景，onDraw 先画背景或 drawBitmap 一张只烘焙一次的透明背景位图（标题、说明等抗锯齿文字只栅格化一次），再叠加动态层；目标用同一个 CanvasRenderingContext2D 多次 render()。

## 原因

Android 每次绘制都从 View 背景开始，烘焙位图里的文字只栅格化一次；ArkUI 画布上下文的内容跨帧保留，不清屏就在上一帧上叠画，透明区域里重复 fillText 的抗锯齿边缘逐帧累积 alpha，文字越画越粗。只核对不透明色块是否覆盖动态区，发现不了这类累积。

## 做法

1. render() 开头 clearRect(0, 0, ctx.width, ctx.height)（或整幅填背景色），再按源顺序绘制背景层与动态层；View 的 setBackgroundColor 由 Canvas 组件的 backgroundColor 承担。
2. 判断能否省略清屏时按“每帧是否从空白开始”判定，不按“同位置重画”或不透明区域是否覆盖判定。

## 可选检查

- 静止画面连续触发多次 render() 后，静态文字区域截图的边缘像素数应保持不变。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕安卓 View.draw(Canvas) 每次绘制先 drawBackground 画 View 背景，再调 onDraw，所以 onDraw 每帧都从背景开始
- 〔原因 / 做法第 2 步〕ArkUI 同一个 CanvasRenderingContext2D 上已画的内容跨帧保留；每次 render() 不清屏、在透明区域重复 fillText 时，文字的抗锯齿边缘逐帧累积 alpha，文字越来越粗
- 〔做法第 1 步〕CanvasRenderingContext2D 的 width、height 是只读属性，绑定到所关联画布的宽高（未绑定时为 0）
