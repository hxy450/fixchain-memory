# ui/effects

渲染效果：elevation 阴影是否投影及写入 ShadowOptions 的 px 换算与共享映射，blur 的单位与边缘，View 体系的图片模糊、LightingColorFilter 乘法压暗与 tint 渐变装饰层，TextView 文字阴影，blendMode 混合着色的离屏范围与预混，渐变描边的双层结构，以及 Compose 渐变端点几何到 linearGradient 角度、stop 周期与镜像平铺的换算；位图着色（colorFilter SRC_IN，fillColor 仅对 SVG 生效），linearGradient 的 angle 方向语义与渐隐遮罩的同色透明终点

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
- [ImageView tint 着色的渐变装饰层用容器 linearGradient 实现](lesson-fcd86aeea6209ea0718b.lesson.md)
  - 时机：界面实现阶段，迁移以 app:tint 主题色着色的白到透明渐变装饰层时
  - 情境：源 ImageView 用 tint=?attr/colorBackground 一类主题色给渐变 shape 着色，目标准备改用 SVG 加 fillColor；目标有深色资源目录。
- [Modifier.blur(dp) 迁到 ArkUI blur 时先确认数值单位，并处理模糊边缘淡出](lesson-6be3938453498c25e9a5.lesson.md)
  - 时机：界面实现阶段，把 Compose Modifier.blur(N.dp) 写成 ArkUI blur 时
  - 情境：源端 blur 半径带 dp，默认 BlurredEdgeTreatment.Rectangle、边缘不淡出；ArkUI blur(value) 的类型注释没有写单位。
- [TextView 的 shadowColor/shadowRadius 映射为 Text.textShadow](lesson-2f1af636a29b131071b3.lesson.md)
  - 时机：界面实现阶段，转换带文字阴影的 TextView 时
  - 情境：源 TextView 设 shadowColor 与 shadowRadius，映射参考把它对应到 .shadow()。
- [elevation 投影写入 ShadowOptions 时按 px 换算，并集中到一个按 elevation 推导的共享函数](lesson-d0aad947e26220fb43fa.lesson.md)
  - 时机：规格提取阶段写阴影配方，以及界面实现、收敛阶段把 Modifier.shadow(elevation) 或 Surface 的 elevation 写成 ArkUI .shadow() 时
  - 情境：源端以 dp 表示阴影高度；目标 ShadowOptions 的 radius/offsetX/offsetY 数值按 px 解释，而 width、padding 等长度属性默认是 vp。工程可能已有共享的 elevation→shadow 映射函数，个别页面也可能用预置 ShadowStyle 或字面值。也包括源视图带 elevation 但 outlineProvider=background 且没有背景，实际不投影。
- [linearGradient 的 angle 按 CSS 语义（0 向上、90 左→右）；渐隐到透明的终点取底色同色 alpha 0，不写 transparent](lesson-aeb0ddcc08dfc64da650.lesson.md)
  - 时机：界面实现与共享组件实现阶段，用 ArkUI linearGradient 写滚动边缘渐隐遮罩条或其他轴向渐变，确定渐变方向（angle/direction）与终点色时
  - 情境：源端用 fadingEdges 一类修饰让横滑行或纵向滚动区的内容在边缘淡出，或有其他轴向渐变；目标改用叠在内容上、从容器底色渐变到透明的 linearGradient 遮罩条，按左右或上下边分别放置，底色常是运行期解析出的 '#AARRGGBB' 主题色。
- [源端图像模糊、乘法压暗与折叠态着色按参数等价实现](lesson-55cac970ada4ca8fd3f1.lesson.md)
  - 时机：界面实现阶段，迁移折叠头部等使用图片模糊、LightingColorFilter 压暗和按折叠状态切换工具栏图标颜色的页面时
  - 情境：源背景图经模糊变换与 LightingColorFilter(mul, 0) 处理，工具栏图标由专门的着色管理类按折叠阈值切换颜色。
- [给位图（png/jpg/webp）着色用 Image.colorFilter（SRC_IN）：fillColor 只对 SVG 图源生效](lesson-1cc509728c131a924efd.lesson.md)
  - 时机：界面实现阶段为源端着色的图片写 ArkUI Image 修饰链、选择染色 API 时；规格提取阶段为 ColorFilter.tint 一类着色写转换决策时
  - 情境：源端 Compose Image 的 colorFilter = ColorFilter.tint(color)（默认 BlendMode.SrcIn），或 ImageView 的 tint、setColorFilter，作用在 drawable 位图上，常见是白色加透明通道、靠着色才在浅色背景上可见的示意图；目标资源仍是同一位图，没有转成 SVG。
  - 例外：目标资源已是 SVG（或改用同色 SVG 资源），此时 fillColor 可用
