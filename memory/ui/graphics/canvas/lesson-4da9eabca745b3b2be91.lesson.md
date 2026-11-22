# SurfaceView 自建线程的 lockCanvas 循环按线程实例迁移：vsync 回调驱动，页面隐藏按 surface 失效写结果

ID：`lesson-4da9eabca745b3b2be91` · 版本：1

[本主题](index.md)

## 何时使用

规格提取、架构决策与渲染实现阶段，把源端 SurfaceView 加自建 Thread 的游戏或渲染循环映射为目标帧驱动方式、循环实例结构与页面生命周期契约时

## 适用情境

源端 SurfaceView 子类实现 SurfaceHolder.Callback，Thread 子类的 run() 在 while(isRunning) 里 lockCanvas → 更新 → onDraw → unlockCanvasAndPost，循环体没有 sleep；循环对象在初始化或重开方法里 new 并赋给同一字段，surfaceCreated 里 start()，surfaceDestroyed 里置停止标志再 join；结算弹窗由循环线程 post 到 UI，弹窗按钮直接重开；速度、周期与动画步进按“每帧”计、没有 delta-time。目标在 ArkUI Canvas 上用帧回调实现，页面隐藏与旋转时不销毁重建。

## 例外与边界

- 源循环体内有固定周期等待（Thread.sleep、SystemClock 等待），或节拍由 Handler.postDelayed、Timer 决定：按源端周期迁移节拍，做法第 2 步不适用
- 源端在重开前停止并 join 旧实例、任何时刻只有一个循环在跑：单一循环句柄与按实例迁移的结果相同

## 原因

这类循环的节拍、同时存活的实例数和停止时机都会被用户看到。无 sleep 的 lockCanvas 循环由显示 vsync 节流，按帧计数的速度与周期依赖实际帧率；setInterval/setTimeout 排在 UI 线程任务队列里、不对齐 vsync，实际频率可能明显低于 1000/周期，逻辑整体变慢。停止只经保存最新实例的字段时，重开前未停的旧实例继续运行，弹窗、音效与下压等副作用随存活实例数倍增；收敛成全局唯一句柄，或启动新循环时清掉旧句柄，会抹掉这种并存。页面隐藏、切后台或 Activity 重建时 surface 先失效，lockCanvas 返回 null（SurfaceHolder.lockCanvas 文档：surface 未创建或不可编辑时返回 null），循环体不判空就在绘制处空指针崩溃；线程结束后 surfaceCreated 再 start() 抛 IllegalThreadStateException，SurfaceView 捕获后只记日志（本机 android-36.1 源码 SurfaceView.java 的 “Exception configuring surface”），新 surface 留空。写成“页面隐藏即停帧并丢弃迟到回调”会丢掉这些结果。

## 做法

1. 先数源端循环实例：查 Thread 子类的构造调用点、保存实例的字段的全部赋值、surfaceCreated/surfaceDestroyed 方法体与各对话框按钮回调。每次 new 映射为一个目标循环对象（实例字段＋各自的帧订阅），启动与停止只作用于字段当前引用的最新实例；重开前不停旧实例的，旧对象继续运行，不收敛成全局单一句柄，也不在启动新循环时清掉旧句柄。规格或派工要求单一句柄而源码每轮 new 时，写进 handback 的 decision_gaps 回报规格分歧。
2. 源循环无 sleep、每轮 lockCanvas 时用 vsync 回调驱动：@kit.ArkGraphics2D 的 displaySync.create() → setExpectedFrameRateRange({ min, max, expected }) 取源端刷新率 → on('frame') → start()，停止时 stop() 并 off('frame')；或每帧重投 UIContext.postFrameCallback。不用 setInterval/setTimeout(16) 代替。规格写“与源端等价节流”时同时写出源端节拍来源和目标驱动 API（本地 SDK ets/api/@ohos.graphics.displaySync.d.ts，@since 11）。
3. 按源端运行态（循环在跑或已结束、对话框是否显示）分别写返回、切后台、旋转的结果：run() 中 lockCanvas 后不判空就绘制时，循环在跑遇 surface 失效即崩溃；已结束的线程在 surfaceCreated 再 start() 只记日志、画面留空。目标在页面隐藏时让画布失效并通知仍在跑的循环，下一轮走源端拿到 null 画布的路径；页面重新显示时清画布后走 surfaceCreated 的等价路径。这些是对源端结果的复刻，不是额外防护；Activity 重建的其余后果见 lesson-94715d0df4c03a8fb5a5。

## 可选检查

- 源端节拍是否跟 vsync 有疑问时，在帧回调里计 1–2 秒帧数，与源端同场景帧率比较。

来源支持：3 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4a352d41e71bd8f199f0](../../../../store/cases/case-4a352d41e71bd8f199f0/bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`bfb25822a981031a8ca464a470972396d768323577afd20d17f7b84d67d5cc0d`
- [case-5b4026f2fabf83812ff2](../../../../store/cases/case-5b4026f2fabf83812ff2/43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`43e98074974b2d60bab047b15264b217ca9d4855b956901208c3897b7e047c75`
- [case-d3f1bcc562a64e5f56f7](../../../../store/cases/case-d3f1bcc562a64e5f56f7/5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`5c0afd723a88fe2ebd2bd100b43aeab602cd42264e70eb03e30e4e9cb7ea012f`
