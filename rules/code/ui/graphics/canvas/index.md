# 自绘画布

源端有自定义 View 或 SurfaceView 的 onDraw、Paint、Canvas.drawText / drawBitmap、invalidate、Typeface，目标端有 Canvas、CanvasRenderingContext2D、fillText、drawImage、帧循环时

## 触发族

- [自绘 View 里的文字度量和 drawText](canvas-text/index.md)（7 条）：读到自定义 View 用 Paint.ascent/descent、getTextBounds 算文字位置，用 canvas.drawText 画字；产物里 Canvas 的 TextMetrics 字段取错、fillText 前没设 direction，或多画了源端没画的文字
- [自绘 View 的尺寸推导和画布单位](canvas-geometry/index.md)（6 条）：读到自定义 View 在 onSizeChanged / onMeasure 的 px 尺寸上按常量和公式推导行高、格高、字号；产物里画布上下文的单位、参照常量、行高常量与容器高度对不上，或几何按值传进 @Builder
- [自绘 View 一次性准备的背景位图和颜色](canvas-prepared-background/index.md)（3 条）：读到自定义 View 在构造、setup() 或 onSizeChanged 里一次性烘焙背景 Bitmap、从主题属性取色；产物里改成每帧重绘却没 clearRect、每帧读实时状态，或只在 aboutToAppear 取一次色
- [自绘 View 改成组件组合](custom-view-to-components/index.md)（2 条）：读到自定义 View 在 onDraw 里用 drawCircle、drawRoundRect 画角标、指示条；产物里改用 Circle、Blank、padding 等组件拼出，尺寸和内边距没按源端绘制公式算
- [View.invalidate 的重绘请求和帧调度](invalidate-frame/index.md)（7 条）：读到自定义 View 在 onDraw 尾部 invalidate() 自续帧、业务层用 invalidate() 请求重绘；产物里另有直调 render() 的入口、用 setInterval 排帧又不清句柄，或请求重绘后立刻把渲染器字段镜像到 @State / @Local
- [setBounds 拉伸的预烘焙位图和取整坐标](setbounds-bitmap/index.md)（3 条）：读到源端把圆角底和文字烘焙进 Bitmap、用 Drawable.setBounds((int)(…)) 把位图拉伸到新边界；产物里改成逐帧 roundRect + fillText 只缩了字号、台账批准的 OffscreenCanvas 缓存没沿用，或坐标没按 (int) 截断
- [构造期解码和预缩放的位图](bitmap-decode-prescale/index.md)（3 条）：读到源端在 View 构造器或 onCreate 里同步 BitmapFactory.decodeResource、按屏宽算出的尺寸 Bitmap.createScaledBitmap 预缩放，再 drawBitmap 原尺寸绘制；产物里每帧 drawImage 缩放、没按密度解码、位图在几何计算前用模块级守护只装一次，或改成 async 启动加输入门控
- [自绘 Paint / Canvas 的绘制分支和坐标](canvas-draw-branch/index.md)（3 条）：源端 Paint / Canvas 的绘制（paint.style、strokeWidth、drawPath、ItemDecoration.onDraw 的 y 换算），对应目标 Canvas 共享绘制分支里的 ctx.lineWidth、按 key 的特判和诊断日志，或 Polyline 的 points 与 position
- [Canvas 上用的注册字体](canvas-registered-font/index.md)（2 条）：读到源端 Typeface.createFromAsset 后 paint.setTypeface、measureText 参与布局；交回的代码 registerFont 后立刻 measureText，或 ctx.font 带引号、多了 bold
- [SurfaceView 自绘和它的渲染线程](surfaceview-render-thread/index.md)（4 条）：读到源端 SurfaceView 配 Thread 子类循环 lockCanvas → 绘制 → unlockCanvasAndPost，或 Choreographer 续帧；交回的帧循环是 setInterval(16)、static 句柄、页隐藏时照跑，或画布下多放了背景 Image
- [drawBitmap 加 Matrix 的位图绘制](drawbitmap-matrix/index.md)（1 条）：读到源端 canvas.drawBitmap(bitmap, matrix, paint)，Matrix.setRectToRect 把位图像素矩形映射到画布；产物里变换矩阵按 PixelMap 的 getImageInfoSync().size 算，绘制却用三参数 ctx.drawImage(pm, 0, 0)
- [onDraw 里向别的类查询的状态和位置](draw-state-query/index.md)（2 条）：读到源端 onDraw 一路先问别的类有没有某个状态、有才取它的位置（public 读方法、经 Matrix 重投影），否则用画布中心；产物里目标类只有 private 字段没有公开读方法，或 Canvas 绘制无条件取 width / 2、height / 2
