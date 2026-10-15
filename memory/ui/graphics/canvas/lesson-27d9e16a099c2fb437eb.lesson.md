# 源端以 invalidate 自续帧时迁成唯一的下一帧绘制入口：合并请求、postFrameCallback 调度、动画活跃才续帧

ID：`lesson-27d9e16a099c2fb437eb` · 版本：3

[本主题](index.md)

## 何时使用

渲染与动画实现阶段，为 Canvas 自绘视图确定帧循环、invalidate 重绘入口与停止条件时

## 适用情境

源端自定义 View 在 onDraw 尾部按动画状态 invalidate()（加 tick）自续帧，业务层也用 invalidate() 请求重绘，没有自建渲染线程；目标在 ArkUI Canvas 上全量重绘，需要选下一帧调度 API，并处理同帧多次请求、动画结束停止和页面销毁。

## 例外与边界

- 源端为 SurfaceView 加自建 Thread 的 lockCanvas 循环：按线程实例、vsync 驱动与 surface 失效语义迁移（lesson-25731279fbe14dcecc69），不收敛成唯一句柄，页面隐藏也不按本条平滑停帧

## 原因

invalidate 只请求下一帧的一次 onDraw，多次请求会合并。写成定时器却在回调里只复位句柄、不清除，或在渲染尾部每帧新开定时器，旧定时器不会停，数量逐帧增加并在动画结束后继续全量重绘，占满 UI 线程；定时器回调本身也不对齐 vsync，按帧计步的速度会随实际频率变慢。另留一条同步直调 render 的路径，会与自续帧的时序不一致，调用方也会依赖同步绘制的结果。

## 做法

1. 实现一个 invalidate()：已有待决帧就返回；否则置待决标志，经 UIContext.postFrameCallback 在下一 vsync 绘制一次，回调先清标志再绘制。引擎桥、尺寸变化与绘制尾部的续帧都走这个入口，render 不再供外部同步调用；按源 onDraw 的顺序在绘制末尾判断动画是否活跃再 invalidate。
2. 帧调度用帧回调，不用 setInterval/setTimeout 代替：定时器回调不对齐 vsync，实际频率低于 1000/周期，按帧计步的动画整体变慢。定时器只留给源端本就按固定周期 tick 的逻辑（Handler.postDelayed、Timer、带 sleep 的循环），用 setInterval 时以同一句柄 clearInterval。页面销毁时置停止标志，丢弃之后到达的帧回调。
3. 依赖绘制结果的状态（如按钮可用性）在消费时刻直读渲染器字段，不在请求重绘后立刻镜像，以免重绘改为异步后读到旧值。

## 可选检查

- 对帧循环有疑问时，记录动画期间与结束后的待决调度数：任一时刻不超过 1，动画结束后为 0，页面销毁后不再绘制。

来源支持：4 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-4a352d41e71bd8f199f0](../../../../store/cases/case-4a352d41e71bd8f199f0/bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d.json) · 结论：recommendation:1
  卡片版本：`bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d`
- [case-569a68ae79caad45dbb6](../../../../store/cases/case-569a68ae79caad45dbb6/f52b572012bb921778066e276b5ebecd610f8263b432b09bccedfe8de4edeb49.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`f52b572012bb921778066e276b5ebecd610f8263b432b09bccedfe8de4edeb49`
- [case-5b4026f2fabf83812ff2](../../../../store/cases/case-5b4026f2fabf83812ff2/43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75.json) · 结论：recommendation:1
  卡片版本：`43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75`
- [case-d3f1bcc562a64e5f56f7](../../../../store/cases/case-d3f1bcc562a64e5f56f7/5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f.json) · 结论：recommendation:1
  卡片版本：`5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f`
