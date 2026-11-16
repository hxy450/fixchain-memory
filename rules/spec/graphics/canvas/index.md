# 自绘与画布

读到自定义 View 的 onDraw、onSizeChanged、Paint（setTextSize、measureText、getTextBounds、setTypeface）、SurfaceView 渲染线程，或 Compose drawWithContent 里的 blendMode，规格里写画布单位、文字度量、字体和重绘时

## 触发族

- [自绘 View 的单位、尺寸分支和位图缩放](custom-view-units/index.md)（5 条）：读到自定义 View 在 onSizeChanged 的 px 尺寸上推导布局、Paint.setTextSize / measureText 按 px 算，尺寸函数按计数和 DisplayMetrics.density 分支返回 dp，BitmapFactory.decodeResource 加 createScaledBitmap 预缩放再 drawBitmap；规格里画布单位、vp 数值和位图缩放的写法
- [自绘 View 的状态读取和重绘时机](custom-view-refresh/index.md)（2 条）：读到自定义 View 在构造、onSizeChanged、onDraw 里取文案或 firstRun 一类一次性状态，或把画面预渲染成位图缓存；规格写「每帧矢量，行为等价」，或没标哪些内容随配置重建刷新
- [自绘 View 用 Paint 取的文字度量](paint-text-metrics/index.md)（3 条）：源端自绘 View 用 Paint.getTextBounds / rect.height()、Paint.ascent() / descent() 算行高、基线或自适应字号，规格的映射行写的是 TextMetrics 的 actualBoundingBox* / fontBoundingBox* 近似、待实测或契约栏「—」
- [SurfaceView 自有渲染线程的帧循环](surfaceview-render-thread/index.md)（3 条）：源端 Thread 子类在 run() 里 SurfaceHolder.lockCanvas / unlockCanvasAndPost 循环，surfaceCreated / surfaceDestroyed 经实例字段 start、置停止标志再 join，规格里写成「单一帧循环句柄（setInterval ~16ms）」「隐藏即停帧」「行为等价」
- [Typeface.createFromAsset 装的自定义字体用在画布上](canvas-custom-typeface/index.md)（2 条）：源端 Typeface.createFromAsset 装载字体文件后 paint.setTypeface，再 measureText 参与布局，规格里的 Canvas font 串带引号或加了 bold，或只写「rawfile 注册字体 → ctx.font」、没写首次测宽前字体须可用
- [依赖画布已有内容的混合模式（blendMode）](canvas-blend-mode/index.md)（2 条）：读到 Compose drawWithContent 里 drawRect(…, blendMode = BlendMode.Plus / Darken) 在同一画布上着色，或 SDK 文档对 blendMode 的混合基底说得不清；规格把它写成兄弟节点的 .blendMode(…, BlendApplyType.OFFSCREEN) 并定为 HARD
