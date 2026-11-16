# 布局与尺寸

源布局里有 match_parent 加水平 margin、按计数或密度分支算出的尺寸，或者派工、尺寸工单、交付报告里写到 '100%'、N vp、dp 对照、尺寸契约时

## 触发族

- [match_parent 加水平 margin 的派工交代](percent-width-margin/index.md)（1 条）：源布局里有 match_parent 或两侧约束 0dp 又带水平 margin 的视图，页面转换的派工、检查项或交给转换者的映射参考只写了 match_parent → '100%'、margin → .margin()
- [尺寸问题的工单和拆分交接](size-tickets-handoff/index.md)（4 条）：派修尺寸问题的工单（跨设备截图偏小、两卡等高）或把布局拆给不同执行者（面板与宿主、横屏变体由共享组件承载）时，派工里的源布局 dp 对照、验收条件和尺寸契约
- [小视觉元素尺寸的转述和对齐说法](small-visual-size/index.md)（2 条）：源码里小视觉元素的尺寸由计数分支和密度分支算出，派工、消息或交付报告里只写「改成 N vp」「按 Android 真机密度对应为 N vp」「已按真机对齐」，没有源函数依据或编译、截图对照
- [布局方向镜像（RTL）的全局约定](rtl-mirroring-convention/index.md)（1 条）：ui-manifest 全局约定里有布局方向镜像（RTL）要求，或源清单 android:supportsRtl="true"；写界面的 worker 的派工说明里没有布局方向镜像、start/end 边距这一条
- [限定符布局变体（layout-sw600dp、layout-v21）](qualifier-layout-variants/index.md)（1 条）：ui-graph 回报「layout-sw600dp / layout-v21 未入图」，或源 res 下有 layout-sw600dp/ 等变体目录；决策台账或计划写「仅 1 布局变体随迁」，没点名文件、没归属到页面 spec、slice 或派工，未入图的变体没有步骤接手
- [派工里转述的位图固有尺寸](bitmap-intrinsic-size/index.md)（1 条）：规格映射写位图「固有 px（按密度换算）」、资源迁移回报写了图块取自哪个密度目录（如 drawable-xxxhdpi），派工把它改写成 getWidth / getHeight 一类具体取值 API，丢了换算条件，或用这些位图做几何计算的派工没带来源密度目录
