# ui/graphics/canvas

自绘 View（onDraw、Paint）移植到 ArkUI Canvas：上下文单位域与跨域换算，invalidate 与帧循环，每帧起始画面（清屏），预烘焙位图改每帧绘制时的取值时机与缩放语义，字体串格式与字体就绪，文字基线度量与段落方向

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
- [View.invalidate 迁成唯一的“请求下一帧绘制一次”入口：待决标志合并请求，用 postFrameCallback 调度，只在动画活跃时续帧](lesson-27d9e16a099c2fb437eb.lesson.md)
  - 时机：渲染与动画实现阶段，为 Canvas 自绘视图确定帧循环、invalidate 重绘入口与停止条件时
  - 情境：源端自定义 View 在 onDraw 尾部按动画状态 invalidate()（加 tick）自续帧，业务层也用 invalidate() 请求重绘；目标在 ArkUI Canvas 上全量重绘，需要选下一帧调度 API，并处理同帧多次请求、动画结束停止和页面销毁。
- [把预烘焙位图改为每帧矢量绘制前，保留位图隐含的取值时机与缩放语义：烘焙时读取的状态留快照，setBounds 拉伸的全部属性按比例缩放](lesson-046c8bbb304684669060.lesson.md)
  - 时机：渲染实现阶段，用每帧矢量绘制替代源端预渲染的背景位图或 tile 位图缓存，并准备声称“行为等价”时
  - 情境：源端在 onSizeChanged 等时机把受状态字段控制的元素（如首启说明）和圆角底、数字等烘焙进 Bitmap，onDraw 只贴图，或在出生、合并动画中用 setBounds((int)…) 整体拉伸、按 int 位移绘制；这些状态在位图生成后仍会被其他流程改写；目标改为 Canvas 每帧 roundRect、fillText 等矢量绘制。
- [按 Android px 公式移植自绘 View 时先定画布上下文单位：用 LengthMetricsUnit.PX 构造，让字号、测宽、几何与触点同域，dp 常量与 vp 输入在边界换算](lesson-7083c6ad69ab19ad17dd.lesson.md)
  - 时机：规格提取与渲染实现阶段，创建 CanvasRenderingContext2D，并为字体串、measureText、几何公式、触点坐标、窗口避让值和 dp 常量确定单位域时
  - 情境：源端是 Android 自定义 View：onSizeChanged 给出 int px 尺寸，Paint.setTextSize/measureText 在 px 域推导字号与派生间距，drawable 圆角等常量以 dp 声明；目标用 ArkUI Canvas 逐式移植，规格或已有代码对画布单位的表述不一致（字体串写 px、映射写 vp、触点写 px 域）。
- [移植 Paint.ascent/descent 的文字基线修正前实测选 TextMetrics 字段：与字体 hhea 上下伸吻合的字段才等价，不凭 W3C 字段名或先例推定；源式取整原样保留](lesson-f876887b216b6caf9f39.lesson.md)
  - 时机：渲染实现阶段，把源端 Canvas 文字居中或基线修正（如 (int)((descent+ascent)/2)）移植为 measureText 的 TextMetrics 计算，或决定能否关闭“需实测校正”的字段映射标记时；规格提取阶段写文字基线映射时
  - 情境：源端以 Paint.ascent()/descent()（字体级上/下伸，ascent 为负）计算基线偏移，供数字、标题、说明等文字使用；目标用 CanvasRenderingContext2D.measureText 返回的 fontBoundingBox*、emHeight*、actualBoundingBox* 取等价度量，并注册了自定义字体。
