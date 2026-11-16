# SurfaceView 自有渲染线程的帧循环

agent 会看到什么：源端 Thread 子类在 run() 里 SurfaceHolder.lockCanvas / unlockCanvasAndPost 循环，surfaceCreated / surfaceDestroyed 经实例字段 start、置停止标志再 join，规格里写成「单一帧循环句柄（setInterval ~16ms）」「隐藏即停帧」「行为等价」

## 规矩

- rule-3b4356ffd6c5｜源端 SurfaceView 自有渲染线程时，规格按运行态写返回、切后台、旋转的结果｜读到：Thread 子类 run() 里 canvas = holder.lockCanvas() 后直接 onDraw(canvas) 或 canvas.drawColor，循环体不判空；SurfaceHolder.Callback 的 surfaceCreated 里直接 thread.start()，surfaceDestroyed 里置停止标志再 join；写错：规格或验收条目写「页面隐藏 / 销毁触发停帧、丢弃迟到回调」或「旋转重建 = 重开新局」，不分渲染线程在跑还是已结束
- rule-aa93769976d2｜源端每轮 new 循环线程、停止只经最新实例时，规格按实例映射，不收敛成全局单一帧循环句柄｜读到：初始化或重开方法里 new 一个 Thread 子类赋给同一字段，surfaceCreated / surfaceDestroyed 只经这个字段 start 或置 isRunning = false 再 join，对话框按钮直接 init + start、不先停旧实例；写错：规格把循环写成「单一帧循环句柄」（setInterval / displaySync），startLoop/stopLoop 对应 surfaceCreated/surfaceDestroyed，并写「每局新实例不释放…不可观察差异，行为等价」
- rule-71d04777eb60｜规格写帧循环「与源端等价节流」时，先写源端节拍来源和目标驱动 API，races 和 C7 候选列出 vsync 驱动｜读到：源端帧循环是无 Thread.sleep 的 SurfaceHolder.lockCanvas / unlockCanvasAndPost 忙循环，或分析器缺陷表写「帧率不限、弹速随设备帧率漂移（帧计数时间基准）」；写错：规格的跨栈映射、实现映射、races 节或决策候选写「单一帧循环句柄（setInterval ~16ms）」「16ms≈60fps」「setInterval 16ms 等价节流」，没写源端节拍来自 vsync 还是固定周期，也没把 displaySync / postFrameCallback 列为候选
