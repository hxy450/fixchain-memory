# 源端 SurfaceView 自有渲染线程时，规格按运行态写返回、切后台、旋转的结果

审的是：规格
触发（任一种）：
- 读到：Thread 子类 run() 里 canvas = holder.lockCanvas() 后直接 onDraw(canvas) 或 canvas.drawColor，循环体不判空；SurfaceHolder.Callback 的 surfaceCreated 里直接 thread.start()，surfaceDestroyed 里置停止标志再 join；写错的样子：规格或验收条目写「页面隐藏 / 销毁触发停帧、丢弃迟到回调」或「旋转重建 = 重开新局」，不分渲染线程在跑还是已结束
适用范围：规格提取阶段，把 SurfaceView 加自建渲染线程的页面映射为目标页面生命周期契约时
做法：
- 先按源端运行态（渲染线程在跑 / 已结束、对话框是否显示）拆开，再分别写返回、切后台、旋转的结果，不写成平滑停帧
- 线程在跑时：surface 失效后 lockCanvas 返回 null，不判空的绘制空指针，进程崩溃。线程已结束后回前台：surfaceCreated 对已结束线程 start() 抛 IllegalThreadStateException，SurfaceView 捕获只记日志，绘制区变黑、对话框还在
- configChanges 不含 orientation 时，线程已结束后旋转：旧对话框消失，按新窗口尺寸重开当前局；已结束后按返回：逐层关对话框再回上一页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- lockCanvas 在 surface 尚未创建或无法编辑时返回 null：窗口隐藏后循环拿到的是 null 画布（出处：android.view.SurfaceHolder#lockCanvas）
- 一个 Thread 只能 start 一次，已结束的线程不能再启动，否则抛 IllegalThreadStateException：回前台 surfaceCreated 再 start() 的结果（出处：java.lang.Thread#start）
- SurfaceView 调 surfaceCreated 等回调时 catch (Exception ex) 后只 Log.e("Exception configuring surface")：start() 抛的异常不会让进程崩溃，只是新 surface 留空（出处：android.view.SurfaceView#updateSurface）
- 安卓实测：进行中按返回、按 Home 各 4/4 崩溃，进行中旋转崩溃，结束后旋转重开：运行态分支的实测结果（出处：卡里修好并验证过）
针对本应用要查的：
- 源端渲染循环和 surface 回调的写法：源工程 Thread 子类的 run() 方法体、SurfaceHolder.Callback 的 surfaceCreated / surfaceDestroyed 方法体、AndroidManifest 里该 Activity 的 configChanges；看 lockCanvas 后有没有判空、surfaceCreated 是否每次都 start 同一个线程对象、configChanges 是否含 orientation，按结果写各运行态的分支
来源：1 张卡，1 个应用
- case-d3f1bcc562a64e5f56f7（Bubble Shooter）：做法第 1 步 ← 建议 3、建议 1、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3、建议 2、诊断；取值 4 ← 诊断
