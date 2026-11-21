# SurfaceView 自建线程的 lockCanvas 循环按线程实例迁移：vsync 回调驱动，页面隐藏按 surface 失效写结果

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，openharmony ets 6.1.0.105；文档副本含到 API 26 的内容，超出 SDK 的已注明）；安卓 平台资源 android-34；框架源码 android-36.1；androidx Compose 1.10.3（foundation、ui、ui-unit、ui-graphics，按字节码核）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕SurfaceHolder.lockCanvas()：surface 尚未创建或不能编辑时返回 null
- 〔原因〕Thread.start() 只能调用一次，线程结束后也不能再 start，否则抛 IllegalThreadStateException
- 〔原因〕SurfaceView 调 surfaceCreated 等回调时 catch (Exception) 后只 Log.e("Exception configuring surface")：回调里抛的异常不让进程崩溃，新 surface 留空
- 〔做法第 2 步〕displaySync 从 @kit.ArkGraphics2D 导出；displaySync.create(): DisplaySync（@since 11）
- 〔做法第 2 步〕DisplaySync.setExpectedFrameRateRange(rateRange: ExpectedFrameRateRange)，不调时 min/max/expected 默认都是 60；ExpectedFrameRateRange { min, max, expected } 单位 fps，min ≤ expected ≤ max，取值 [0, 设备最大帧率]
- 〔做法第 2 步〕DisplaySync.on('frame', callback: Callback<IntervalInfo>)；off('frame', callback?) 不传 callback 时移除全部；start() 加入渲染管线启用回调、stop() 移出；IntervalInfo.timestamp、targetTimestamp 单位纳秒
- 〔做法第 2 步〕UIContext.postFrameCallback(frameCallback: FrameCallback)（@since 12）只在下一帧运行一次；FrameCallback 是抽象类，实现 onFrame(frameTimeInNano: number)
- 〔做法第 2 步〕60Hz 模拟器上，每次回调里更新并绘制一帧的 setInterval(16) 实际约 39 次/秒；displaySync 期望 {60, 60, 60} 的 on('frame') 随显示刷新约 60 次/秒回调，与安卓无 sleep 的 lockCanvas 循环同节拍
- 〔做法第 3 步〕onPageShow?() / onPageHide?()：页面每次显示、隐藏时调用，含切前台、切后台；只对 @Entry 装饰的组件生效；NavDestination 另有 NavDestinationAttribute.onShown / onHidden 显示、隐藏回调
- 〔做法第 3 步〕清画布：CanvasRenderer.clearRect(x, y, w, h)（默认单位 vp）；reset() 清空后备缓冲、状态栈、路径和样式（@since 12）
- 〔做法第 3 步〕configChanges 未声明的配置变化发生时 Activity 重启；orientation = 0x0080；targetSdk ≥ 13 时横竖屏切换同时改变 screenSize（0x0400），两者都声明才不重建
- 〔做法第 3 步〕window.on('windowSizeChange', Callback<Size>) 只在窗口尺寸变化时触发，旋转 180° 不触发；display.on('change', Callback<number>) 在屏幕旋转时触发，此时 Display 的 width/height/orientation/rotation 已更新，Window 取到的可能仍是旧宽高
- 〔做法第 3 步〕安卓上 SurfaceView 渲染线程在 lockCanvas 后不判空就绘制时，循环运行中按返回、按 Home，或旋转导致 Activity 重建，都会因拿到 null 画布而崩溃
