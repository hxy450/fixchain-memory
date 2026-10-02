# ui/effects

渲染效果：elevation 阴影写入 ShadowOptions 的 px 换算与共享映射，blur 的单位与边缘，blendMode 混合着色的离屏范围与预混，渐变描边的双层结构，以及 Compose 渐变端点几何到 linearGradient 角度、stop 周期与镜像平铺的换算

[上一级](../index.md)

## 本级经验

- [Compose Brush 渐变描边用“外层渐变 + 边宽内衬 + 内层实底”实现，不降级成渐变首色](lesson-5d56afe5595bb26eaf2f.lesson.md)
  - 时机：界面实现阶段，把 Compose border(width, Brush) 或项目自定义的渐变描边 Modifier 翻成 ArkUI 组件时
  - 情境：源组件用 Brush.linearGradient 描边（自定义渐变描边扩展等），边宽来自扩展的默认参数，外面可能套 elevation &gt; 0 的 Surface；ArkUI border 只接受单色。
- [Compose 叠在已画内容上的 blendMode 着色：参与混合的底色、字形和渐变放进同一离屏组，或把源算式预混进色标](lesson-3024193e4816229c5370.lesson.md)
  - 时机：规格提取与界面实现阶段，把 drawWithContent { drawContent(); drawRect(brush, blendMode) } 这类图标渐变着色映射成 ArkUI 结构，或在修复阶段改写其混合方式时
  - 情境：源组件先画图标内容，再用渐变矩形以 Plus、Darken 等混合模式叠加着色，可能按深浅主题切换模式；结果依赖画布上已画好的底色（底盘、按钮背景）与字形像素。目标端渐变层、图标、底盘是 Stack 里的兄弟节点，ArkUI 提供 blendMode 与 BlendApplyType。
  - 例外：源端混合只依赖自身 alpha（SRC_IN、DST_IN 一类）时，不需要纳入底色，也不需要预混
- [Compose 渐变按端点几何换算成 ArkUI linearGradient：默认对角按宽高算角度，端点周期按渐变线长缩放 stop，Mirror 用回文 stop](lesson-4ce3a1c186651285f362.lesson.md)
  - 时机：界面实现阶段，把 Brush.linearGradient/horizontalGradient 翻成 ArkUI linearGradient，确定方向角、stop 位置与平铺、平移写法时
  - 情境：源渐变或未指定 start/end（默认从组件左上 (0,0) 到右下 (w,h)），或以端点距离（startX/endX、start/end）定义图案周期并配 TileMode.Mirror 与随滚动、动画的平移；ArkUI linearGradient 只有角度或方向、按组件自身渐变线长取比例的 stop 和 repeating 开关；目标组件可能宽高不等（胶囊、卡片）。
- [Modifier.blur(dp) 迁到 ArkUI blur 时先确认数值单位，并处理模糊边缘淡出](lesson-6be3938453498c25e9a5.lesson.md)
  - 时机：界面实现阶段，把 Compose Modifier.blur(N.dp) 写成 ArkUI blur 时
  - 情境：源端 blur 半径带 dp，默认 BlurredEdgeTreatment.Rectangle、边缘不淡出；ArkUI blur(value) 的类型注释没有写单位。
- [elevation 投影写入 ShadowOptions 时按 px 换算，并集中到一个按 elevation 推导的共享函数](lesson-d0aad947e26220fb43fa.lesson.md)
  - 时机：规格提取阶段写阴影配方，以及界面实现、收敛阶段把 Modifier.shadow(elevation) 或 Surface 的 elevation 写成 ArkUI .shadow() 时
  - 情境：源端以 dp 表示阴影高度；目标 ShadowOptions 的 radius/offsetX/offsetY 数值按 px 解释，而 width、padding 等长度属性默认是 vp。工程可能已有共享的 elevation→shadow 映射函数，个别页面也可能用预置 ShadowStyle 或字面值。
