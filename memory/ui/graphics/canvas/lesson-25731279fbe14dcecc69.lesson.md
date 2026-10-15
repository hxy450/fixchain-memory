# 源端 SurfaceView 自建线程的 lockCanvas 循环按线程实例迁移：vsync 驱动，只停最新实例，页面隐藏按 surface 失效写结果

ID：`lesson-25731279fbe14dcecc69` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与渲染实现阶段，把源端 SurfaceView 加自建 Thread 的游戏或绘制循环映射为目标帧调度结构，并写重开、返回、切后台与旋转的生命周期契约时

## 适用情境

源端视图继承 SurfaceView，Thread 子类的 run() 中循环 lockCanvas → 绘制 → unlockCanvasAndPost，循环体没有 sleep，速度与节拍按“每帧”计；SurfaceHolder.Callback 的 surfaceCreated 调 thread.start()，surfaceDestroyed 置停止标志并 join；初始化或重开路径可能每次 new 一个线程赋给同一字段。目标准备用 ArkUI Canvas 加定时器或一个全局帧循环句柄实现，并在页面隐藏、销毁时直接停循环。

## 例外与边界

- 源端用 View.invalidate/onDraw 自续帧、没有自建渲染线程：按 invalidate 迁移的经验（lesson-27d9e16a099c2fb437eb）处理
- 循环体内有 Thread.sleep、固定周期的 Handler.postDelayed，或按 delta-time 推进：节拍不跟显示刷新，按源端周期与时间推进方式迁移

## 原因

lockCanvas 受显示刷新节流，循环每个 vsync 推进一次；定时器回调排在 UI 线程任务队列里、不对齐 vsync，实际频率明显低于 1000/周期，按帧计步的速度与节拍整体变慢。源端每次重开 new 一个线程，而停止只经保存最新实例的字段，旧实例可能仍在运行，同时存活的循环数决定弹窗、音效与副作用的次数。页面不可见时 surface 先失效，正在跑的循环下一次 lockCanvas 得到 null，源端不判空就崩溃；已结束的线程再 start() 抛 IllegalThreadStateException，被 SurfaceView 捕获只记日志，新 surface 留空。收敛成单一句柄、隐藏时平滑停帧，都会改掉这些可观察结果。

## 做法

1. 先数实例：列出 Thread 子类的全部构造调用点、保存实例的字段、该字段上的 start 与停止调用、对话框按钮回调；每个线程实例映射为一个目标循环对象（实例字段加各自的帧订阅），停止只作用于字段当前引用的实例，启动新循环时不清理旧实例。规格写出“重开后旧循环是否仍在跑”及其可见结果，按存活实例数核对弹窗与副作用次数。
2. 节拍：源循环无 sleep、每轮 lockCanvas 时，用 @ohos.graphics.displaySync（create → setExpectedFrameRateRange 取源端刷新率 → on('frame') → start/stop）或每帧重投的 UIContext.postFrameCallback 驱动一次迭代，不用 setInterval/setTimeout 代替。查值：本地 SDK ets/api/@ohos.graphics.displaySync.d.ts、ets/component/common.d.ts 的 ExpectedFrameRateRange、ets/api/@ohos.arkui.UIContext.d.ts。
3. 生命周期按运行态拆分写契约：循环在跑时，返回、切后台与会重建 Activity 的旋转都让 surface 失效，源端在下一次迭代拿到 null 画布；源端不判空时这是崩溃路径，按照搬源端缺陷的规则保留或登记差异。循环已结束时回到前台走 surfaceCreated，对已结束线程再 start 的异常只记日志、绘制区为空。去哪里查：Thread 子类 run() 方法体、SurfaceHolder.Callback 两个回调的方法体、AndroidManifest 中该 Activity 的 configChanges。

## 可选检查

- 对节拍有疑问时，在帧回调里计 1–2 秒的迭代次数，与源端同一场景的帧率比较。

来源支持：3 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4a352d41e71bd8f199f0](../../../../store/cases/case-4a352d41e71bd8f199f0/bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d`
- [case-5b4026f2fabf83812ff2](../../../../store/cases/case-5b4026f2fabf83812ff2/43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75`
- [case-d3f1bcc562a64e5f56f7](../../../../store/cases/case-d3f1bcc562a64e5f56f7/5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f.json) · 结论：diagnosis, recommendation:1
  卡片版本：`5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f`
