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
3. 按源端运行态（循环在跑或已结束、对话框是否显示）分别写返回、切后台、旋转的结果：run() 中 lockCanvas 后不判空就绘制时，循环在跑遇 surface 失效即崩溃；已结束的线程在 surfaceCreated 再 start() 只记日志、画面留空。目标在页面隐藏时（@Entry 页面用 onPageHide、onPageShow，Navigation 子页面用 NavDestination 的 onHidden、onShown）让画布失效并通知仍在跑的循环，下一轮走源端拿到 null 画布的路径；页面重新显示时清画布后走 surfaceCreated 的等价路径。这些是对源端结果的复刻，不是额外防护；Activity 重建的其余后果见 lesson-94715d0df4c03a8fb5a5。

## 可选检查

- 源端节拍是否跟 vsync 有疑问时，在帧回调里计 1–2 秒帧数，与源端同场景帧率比较。

来源支持：3 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码；android-36 的平台资源。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕源端每局 new 一个循环线程、重开前不停旧实例时，安卓设备上两个循环同时运行，结算弹窗随存活循环持续叠加（实测叠到 600 个以上）
- 〔原因 / 做法第 2 步〕60Hz 模拟器上 setInterval(16) 驱动的帧循环实际约 39 帧/秒；同场景下安卓无 sleep 的 lockCanvas 循环约 60 帧/秒
- 〔原因 / 做法第 2 步〕setTimeout、setInterval 不是精准定时器，实际延迟可能与预期有误差；回调放进任务队列，等当前代码执行完、下一次事件循环才执行，页面忙时会更晚；应用切到后台时到期定时器不触发，回到前台后按序触发
- 〔做法第 2 步〕@ohos.graphics.displaySync（API 11 起）：displaySync.create() 新建实例；setExpectedFrameRateRange({ min, max, expected }) 设期望帧率范围，单位帧/秒，取值 [0, 设备最大帧率] 且 min ≤ expected ≤ max，超出有效范围抛 401；on('frame', callback) 注册帧回调，callback 收到 IntervalInfo（timestamp、targetTimestamp，纳秒）；start() 后每帧回调一次，回调在 UI 主线程执行；stop() 停止回调但保留期望帧率和已注册的回调，可再 start()；off('frame') 不传 callback 时移除全部回调
- 〔做法第 2 步〕没调用 setExpectedFrameRateRange 时两方说法不同：SDK 声明注释写 min、max、expected 默认都是 60；文档写跟随应用当前运行的帧率（传 (0, 0, 0) 同样跟随）；默认行为以文档为准
- 〔做法第 1 步〕DisplaySync.start() 会把实例关联到 UI 上下文和窗口；在非 UI 页面或异步回调里调用 start() 可能取到错误的 UI 上下文，回调不执行、期望帧率不生效；stop() 解除这一关联
- 〔做法第 2 步〕UIContext.postFrameCallback(frameCallback)（API 12 起）注册的回调只在下一帧渲染时调用一次，回调方法是 FrameCallback.onFrame(frameTimeInNano)；持续按帧驱动要在每次 onFrame 里重新 postFrameCallback
- 〔原因 / 做法第 3 步〕SurfaceHolder.lockCanvas() 在 surface 尚未创建或不能编辑时返回 null；在 surfaceCreated 之前或 surfaceDestroyed 之后反复调用，会被节流到很慢的频率（SurfaceView 的实现：视图不可见、绘制已停止或还没有 surface 时返回 null，并让两次失败调用之间至少隔 100ms）
- 〔原因 / 做法第 3 步〕同一个 Thread 对象只能 start() 一次，线程已启动或已结束时再次调用 start() 抛 IllegalThreadStateException
- 〔原因 / 做法第 3 步〕SurfaceView.updateSurface 里回调 surfaceCreated、surfaceChanged 等时，用 catch (Exception) 捕获异常、只记 Log.e 的 “Exception configuring surface”，不向外抛
- 〔原因 / 做法第 3 步〕源端 run() 中 lockCanvas 后不判空就绘制、渲染循环在跑时，安卓设备上按返回、按 Home 各 4 次均崩溃，旋转（Activity 重建）也崩溃；对局结束、循环已停时旋转按重建重开
- 〔做法第 3 步〕configChanges 没有列出的配置变化发生时 Activity 重启；旋转对应 orientation（0x0080），横竖切换时可用屏幕尺寸 screenSize（0x0400）也随之变化，targetSdk ≥ 13（HONEYCOMB_MR2）时两者都列出才不因旋转重启；例外：targetSdk 低于 13 时 screenSize、smallestScreenSize 的变化不重启，Android 8.0 起 mcc、mnc 变化默认也不重启（要重启得写进 recreateOnConfigChanges）
- 〔做法第 3 步〕onPageShow、onPageHide 只对 @Entry 装饰的 router 页面生效：每次显示（含路由跳转、应用进入前台）、每次隐藏（含路由跳转、应用进入后台）各触发一次；Navigation 子页面用 NavDestination 的 onShown、onHidden（API 10 起），onHidden 在有新页面压栈使它不在栈顶、它作为栈顶页面出栈、或应用切到后台时触发
- 〔做法第 3 步〕display.on('change', callback) 在显示设备改变（如方向改变）时回调，参数是 displayId；Display.rotation 取 0、1、2、3，表示屏幕顺时针旋转 0°、90°、180°、270°
