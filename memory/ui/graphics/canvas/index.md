# ui/graphics/canvas

自绘 View（onDraw、Paint）移植到 ArkUI Canvas：上下文单位域与跨域换算，invalidate 自续帧的帧入口，SurfaceView 自建线程循环的实例数、vsync 节拍与 surface 失效，每帧起始画面（清屏），位图按密度解码与预缩放的采样，预烘焙位图改每帧绘制时的取值时机与缩放语义，字体串格式与字体就绪，文字基线度量与段落方向

[上一级](../index.md)

## 本级经验

- [ArkUI Canvas 的内容跨帧保留：把 onDraw 移植为反复调用的 render() 时每帧先清屏，再按源顺序绘制](lesson-351ce34d3ebe51b8ff8e.lesson.md)
  - 时机：渲染实现阶段，把源端 onDraw 改为在同一 ArkUI Canvas 上反复调用的 render()、确定每帧起始画面时，含把一次性烘焙的背景位图改成每帧矢量重绘
  - 情境：源端自定义 View 由 setBackgroundColor 设背景，onDraw 先画背景或 drawBitmap 一张只烘焙一次的透明背景位图（标题、说明等抗锯齿文字只栅格化一次），再叠加动态层；目标用同一个 CanvasRenderingContext2D 多次 render()。
- [Canvas 字体串按注册字族名原样引用、不加源端没有的 bold；字体参与测宽布局时，首次布局前确认字体已就绪](lesson-74295d12b4edc025569f.lesson.md)
  - 时机：规格提取与渲染实现阶段，为源端自定义字体制定 ArkUI Canvas 的 ctx.font 串格式，并安排字体注册与首次 measureText 布局的先后时
  - 情境：源端以 Typeface.createFromAsset 同步装载单一字面（如 Bold）的字体文件并 setTypeface 给 Paint，文本测宽参与布局计算；目标用 font.registerFont 注册字族，在 Canvas 中以 ctx.font 串引用并 measureText。
- [Canvas.drawText 移植为 fillText 时按每串首个强方向字符设置 ctx.direction，不让画布方向随系统语言 inherit](lesson-68717b80482f4bd12825.lesson.md)
  - 时机：规格提取与渲染实现阶段，把安卓 Canvas.drawText 文字迁到 ArkUI fillText、确定文字段落方向时
  - 情境：源端文字经 Canvas.drawText 配默认 new Paint()（未设 bidi）绘制；应用有 fa、ar 等 RTL 资源，或可能在无对应资源、回落英文的 RTL 系统语言下运行；目标 CanvasRenderingContext2D.direction 保持默认 inherit。
- [getTextBounds 取的文字高度按 actualBoundingBox 两项各自 ceil 映射，不用 fontBoundingBox 行框](lesson-d525795f545b1b16e77a.lesson.md)
  - 时机：规格提取阶段写 Paint 文字度量到 TextMetrics 的映射行时；渲染实现阶段按映射计算 Canvas 文字行高、行距或自适应字号时
  - 情境：源端自绘 View 用 Paint.getTextBounds(text, start, end, Rect) 取一段具体字符的墨迹包围盒，再用 rect.height() 定行高或间距（如标签与数值的行距、自适应字号循环）；目标用 CanvasRenderingContext2D.measureText 返回的 TextMetrics 计算。
  - 例外：源端用的是 Paint.ascent()/descent()/getFontMetrics() 的字体级度量：按字体级基线修正实测选字段
- [把预烘焙位图改为每帧矢量绘制前，保留位图隐含的取值时机与缩放语义：烘焙时读取的状态留快照，拉伸的全部属性按比例缩放](lesson-046c8bbb304684669060.lesson.md)
  - 时机：渲染实现阶段，用每帧矢量绘制替代源端预渲染的背景位图或 tile 位图缓存，并准备声称“行为等价”时
  - 情境：源端在 onSizeChanged 等时机把受状态字段控制的元素（如说明文案、提示层）和圆角底、文字等烘焙进 Bitmap，onDraw 只 drawBitmap，或在缩放类动画中用 setBounds((int)…) 整体拉伸位图、按 int 位移绘制；这些状态在位图生成后仍会被其他流程改写；目标改为 Canvas 每帧 roundRect、fillText 等矢量绘制。
  - 例外：只涉及每帧起始画面（是否清屏、透明区文字叠画变粗）：按画布跨帧保留与每帧清屏的规则处理
- [按 Android px 公式移植自绘 View 时先定画布上下文单位：用 LengthMetricsUnit.PX 构造，让字号、测宽、几何与触点同域，dp 常量与 vp 输入在边界换算](lesson-7083c6ad69ab19ad17dd.lesson.md)
  - 时机：规格提取与渲染实现阶段，创建 CanvasRenderingContext2D，并为字体串、measureText、几何公式、触点坐标、窗口避让值和 dp 常量确定单位域时
  - 情境：源端是 Android 自定义 View：onSizeChanged 给出 int px 尺寸，Paint.setTextSize/measureText 在 px 域推导字号与派生间距，drawable 圆角等常量以 dp 声明；目标用 ArkUI Canvas 逐式移植，规格或已有代码对画布单位的表述不一致（字体串写 px、映射写 vp、触点写 px 域）。
- [源端 SurfaceView 自建线程的 lockCanvas 循环按线程实例迁移：vsync 驱动，只停最新实例，页面隐藏按 surface 失效写结果](lesson-25731279fbe14dcecc69.lesson.md)
  - 时机：规格提取与渲染实现阶段，把源端 SurfaceView 加自建 Thread 的游戏或绘制循环映射为目标帧调度结构，并写重开、返回、切后台与旋转的生命周期契约时
  - 情境：源端视图继承 SurfaceView，Thread 子类的 run() 中循环 lockCanvas → 绘制 → unlockCanvasAndPost，循环体没有 sleep，速度与节拍按“每帧”计；SurfaceHolder.Callback 的 surfaceCreated 调 thread.start()，surfaceDestroyed 置停止标志并 join；初始化或重开路径可能每次 new 一个线程赋给同一字段。目标准备用 ArkUI Canvas 加定时器或一个全局帧循环句柄实现，并在页面隐藏、销毁时直接停循环。
  - 例外：源端用 View.invalidate/onDraw 自续帧、没有自建渲染线程：按 invalidate 迁移的经验（lesson-27d9e16a099c2fb437eb）处理；循环体内有 Thread.sleep、固定周期的 Handler.postDelayed，或按 delta-time 推进：节拍不跟显示刷新，按源端周期与时间推进方式迁移
- [源端以 invalidate 自续帧时迁成唯一的下一帧绘制入口：合并请求、postFrameCallback 调度、动画活跃才续帧](lesson-27d9e16a099c2fb437eb.lesson.md)
  - 时机：渲染与动画实现阶段，为 Canvas 自绘视图确定帧循环、invalidate 重绘入口与停止条件时
  - 情境：源端自定义 View 在 onDraw 尾部按动画状态 invalidate()（加 tick）自续帧，业务层也用 invalidate() 请求重绘，没有自建渲染线程；目标在 ArkUI Canvas 上全量重绘，需要选下一帧调度 API，并处理同帧多次请求、动画结束停止和页面销毁。
  - 例外：源端为 SurfaceView 加自建 Thread 的 lockCanvas 循环：按线程实例、vsync 驱动与 surface 失效语义迁移（lesson-25731279fbe14dcecc69），不收敛成唯一句柄，页面隐藏也不按本条平滑停帧
- [源端位图按密度解码、createScaledBitmap 预缩放后原尺寸绘制时，目标在 PixelMap 上按同样采样预缩放，不在 drawImage 时缩放](lesson-ad2107690c0cdb9fd4fc.lesson.md)
  - 时机：规格提取阶段把源端位图的解码、预缩放与绘制方式写成目标画布契约时；渲染实现阶段装载并绘制这些位图时
  - 情境：源端自绘视图用 BitmapFactory.decodeResource 解码（资源只放在某个密度目录时按 设备dpi/目录dpi 缩放并带滤波），再用 Bitmap.createScaledBitmap(src, w, h, filter) 缩到由运行时几何决定的尺寸，onDraw 以 drawBitmap 按位图原尺寸绘制；目标准备在 ArkUI Canvas 的 drawImage 里传 dw/dh 做绘制期缩放。
- [源端用 Paint.ascent/descent 做文字基线修正时，实测选与 hhea 吻合的 TextMetrics 字段，源式取整原样保留](lesson-f876887b216b6caf9f39.lesson.md)
  - 时机：渲染实现阶段，把源端 Canvas 文字居中或基线修正（如 (int)((descent+ascent)/2)）移植为 measureText 的 TextMetrics 计算，或决定能否关闭“需实测校正”的字段映射标记时；规格提取阶段写字体级基线映射时
  - 情境：源端以 Paint.ascent()/descent()（字体级上/下伸，ascent 为负）或 getFontMetrics() 计算基线偏移，供数字、标题、说明等文字使用；目标用 CanvasRenderingContext2D.measureText 返回的 fontBoundingBox*、emHeight*、actualBoundingBox* 取等价度量，并注册了自定义字体。
  - 例外：源端用 Paint.getTextBounds(…, Rect) 或 rect.height() 取一段字符的墨迹包围盒：直接对应 actualBoundingBox*，不做 hhea 实测
