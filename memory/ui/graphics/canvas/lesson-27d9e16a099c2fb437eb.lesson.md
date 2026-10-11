# View.invalidate 迁成唯一的“请求下一帧绘制一次”入口：待决标志合并请求，用 postFrameCallback 调度，只在动画活跃时续帧

ID：`lesson-27d9e16a099c2fb437eb` · 版本：1

[本主题](index.md)

## 何时使用

渲染与动画实现阶段，为 Canvas 自绘视图确定帧循环、invalidate 重绘入口与停止条件时

## 适用情境

源端自定义 View 在 onDraw 尾部按动画状态 invalidate()（加 tick）自续帧，业务层也用 invalidate() 请求重绘；目标在 ArkUI Canvas 上全量重绘，需要选下一帧调度 API，并处理同帧多次请求、动画结束停止和页面销毁。

## 原因

invalidate 只请求下一帧的一次 onDraw，多次请求会合并。写成定时器却在回调里只复位句柄、不清除，或在渲染尾部每帧新开定时器，旧定时器不会停，数量逐帧增加并在动画结束后继续全量重绘，占满 UI 线程。另留一条同步直调 render 的路径，会与自续帧的时序不一致，调用方也会依赖同步绘制的结果。

## 做法

1. 实现一个 invalidate()：已有待决帧就返回；否则置待决标志，经 UIContext.postFrameCallback 在下一 vsync 绘制一次，回调先清标志再绘制。引擎桥、尺寸变化与绘制尾部的续帧都走这个入口，render 不再供外部同步调用；按源 onDraw 的顺序在绘制末尾判断动画是否活跃再 invalidate。
2. 只能用定时器时用 setTimeout 做一次性调度；用 setInterval 必须以同一句柄 clearInterval。页面销毁时置停止标志，丢弃之后到达的帧回调。
3. 依赖绘制结果的状态（如按钮可用性）在消费时刻直读渲染器字段，不在请求重绘后立刻镜像，以免重绘改为异步后读到旧值。

## 可选检查

- 对帧循环有疑问时，记录动画期间与结束后的待决调度数：任一时刻不超过 1，动画结束后为 0，页面销毁后不再绘制。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-569a68ae79caad45dbb6](../../../../store/cases/case-569a68ae79caad45dbb6/f52b572012bb921778066e276b5ebecd610f8263b432b09bccedfe8de4edeb49.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`f52b572012bb921778066e276b5ebecd610f8263b432b09bccedfe8de4edeb49`
