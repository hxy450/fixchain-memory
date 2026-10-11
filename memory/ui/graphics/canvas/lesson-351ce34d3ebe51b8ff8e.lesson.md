# ArkUI Canvas 的内容跨帧保留：把 onDraw 移植为反复调用的 render() 时每帧先清屏，再按源顺序绘制

ID：`lesson-351ce34d3ebe51b8ff8e` · 版本：1

[本主题](index.md)

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

## 来源（按需复核）

- [case-fbf67056e47edb718e10](../../../../store/cases/case-fbf67056e47edb718e10/3867724c72cf631bdaf0429205c052777592fcd050c113561c9e901f642da2c1.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`3867724c72cf631bdaf0429205c052777592fcd050c113561c9e901f642da2c1`
