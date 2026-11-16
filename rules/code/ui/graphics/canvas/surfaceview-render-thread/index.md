# SurfaceView 自绘和它的渲染线程

agent 会看到什么：读到源端 SurfaceView 配 Thread 子类循环 lockCanvas → 绘制 → unlockCanvasAndPost，或 Choreographer 续帧；交回的帧循环是 setInterval(16)、static 句柄、页隐藏时照跑，或画布下多放了背景 Image

## 规矩

- rule-ae40dd1c59ed｜源端帧循环跟 vsync、逻辑按帧计时，目标用 displaySync 驱动，不用 setInterval(16)｜读到：源端游戏线程 while 循环里没有 Thread.sleep，每轮 SurfaceHolder.lockCanvas() → 更新 → onDraw → unlockCanvasAndPost；速度、周期按「每帧」计（px/帧、N 帧），没有 delta-time；写错：目标帧循环写成 setInterval(…, 16)，帧间隔常量写 16，注释写「16ms 等价节流」
- rule-056de679b860｜源端每轮 new 循环线程时，目标每个实例对应一个循环对象，startLoop 不先清掉旧句柄｜读到：源码初始化方法里 new 一个 Thread 子类赋给同一字段，停止只经这个字段；写错：目标用一个 static 句柄字段承载全局唯一循环，起新循环前先 clearInterval(旧句柄) 再 setInterval 新句柄；页面用两个布尔旗承载结算弹窗
- rule-a95d33cfbe38｜源端渲染线程在页隐藏时会拿到空画布，目标在 onPageHide 让画布失效、onPageShow 重走创建｜读到：Thread 子类 run() 里 lockCanvas() 后直接绘制不判空；surfaceCreated 里直接 thread.start()；configChanges 不含 orientation；写错：目标只在 aboutToDisappear 里停掉帧循环（clearInterval）、丢弃迟到回调，没有 onPageHide 处理（切后台回来循环照跑）；方向变化时无条件关弹窗、重开
- rule-a5c87c586f92｜画布下放背景层前核对源自绘类，默认 Z 序 SurfaceView 不放背景 Image｜读到：源自绘视图类 extends SurfaceView（或 GLSurfaceView），构造器只 getHolder().addCallback(this)，没有 setZOrderOnTop / setFormat，每帧 drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR)；写错：目标 Stack 底层放了 Image(…).objectFit(ImageFit.Fill) 背景层，上面是透明 Canvas，每帧 clearRect 后露出背景图
