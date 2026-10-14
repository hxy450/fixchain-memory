# ui/canvas

Canvas自绘：绘制单位、离屏位图、帧驱动、着色、画布状态

[上一级](../index.md)

## 本级经验

- [Paint级透明度映射为画布状态时，画完复位到已知默认值](lesson-5511f322875beff3e87a.lesson.md)
  - 时机：界面实现阶段，把Android逐次绘制所用Paint的透明度或颜色滤镜映射为ArkUI CanvasRenderingContext2D共享状态时
  - 情境：源端每次drawBitmap用独立Paint设透明度（如淡出），其他图层用默认Paint不透明绘制；目标用globalAlpha等共享上下文状态，同一画布还要连续绘制不应受影响的图层。
- [对角ColorMatrix着色用逐像素乘法实现，不依赖合成模式](lesson-374cf4b3b855e9d518ab.lesson.md)
  - 时机：绘制实现阶段，把Android ColorMatrixColorFilter逐通道着色迁移到ArkUI Canvas时
  - 情境：源端用4×5对角ColorMatrix（R×r、G×g、B×b、A×a）给带明暗渐变的灰度模板着色；目标是ArkUI Canvas/OffscreenCanvas，候选中出现globalCompositeOperation混合模式（如multiply）。
- [按帧推进的自绘动画用逐帧回调驱动，不用固定间隔定时器](lesson-57669a007c3ccaf939d3.lesson.md)
  - 时机：规格提取、派工与实现阶段，为源端自绘渲染循环确定目标帧驱动方式时
  - 情境：源端渲染线程在任务队列非空时不休眠、按合成节奏逐帧推进；各动画按帧计步（每帧位移、透明度或步数），个别任务另带毫秒节流；目标为ArkUI Canvas单UI线程绘制。
- [离屏位图按源端显示尺寸生成，不自行加超采样](lesson-7654c8d2dcaf4a7ccd17.lesson.md)
  - 时机：界面实现与渲染功能实现阶段，为Canvas自绘的离屏位图（着色精灵、网格整图等）确定生成分辨率时
  - 情境：源端把资源位图缩放到格子像素尺寸、按画布宽度生成整图后1:1绘制；目标用OffscreenCanvas离屏生成位图，并在帧循环中逐帧drawImage。
- [移植像素语义的自绘画布时显式使用PX单位](lesson-435581ac467471b486aa.lesson.md)
  - 时机：界面实现阶段，把Android自绘View（SurfaceView/Canvas）的测量、取整、位图缩放、逐帧位移和触摸换算移植到ArkUI Canvas/OffscreenCanvas时
  - 情境：源端测量、整除取整、位图缩放和每帧±N位移都以物理像素计；目标Canvas上下文与OffscreenCanvas默认单位为vp，组件尺寸与触摸坐标也以vp给出。
