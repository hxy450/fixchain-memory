# 源端给位图做 tint 着色时，目标用 Image.colorFilter，不用 fillColor

审的是：代码
触发（任一种）：
- 读到：Compose Image(painter = painterResource(R.drawable.…), colorFilter = ColorFilter.tint(color))，drawable 是 png / jpg / webp 位图；写错的样子：目标 Image 上写 .fillColor(颜色)，图源仍是同一张位图
- 读到：ImageView 带 android:tint / app:tint，或代码里 setColorFilter(color)，src 是 png / jpg / webp 位图；写错的样子：目标 Image 上写 .fillColor(颜色)，图源仍是同一张位图
适用范围：源端对位图着色、目标资源仍是位图（没有换成 SVG）时
做法：
- 写成 .colorFilter(drawing.ColorFilter.createBlendModeColorFilter(color, drawing.BlendMode.SRC_IN))，drawing、common2D 从 @kit.ArkGraphics2D 导入；color 是 common2D.Color，主题色 '#AARRGGBB' 拆成 alpha / red / green / blue 四个 0–255 整数
- 颜色在渲染期按当前主题取值；只有部分条目着色时，不着色的分支不挂滤镜
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute，只对 SVG 图源生效：对 png 等位图不起作用；文档写明 png 改色用 colorFilter（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor；ts-basic-components-image.md，fillColor）
- colorFilter(value: ColorFilter | DrawingColorFilter): ImageAttribute：Image 的颜色滤镜；设了它 renderMode 不生效（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.colorFilter）
- static createBlendModeColorFilter(color: common2D.Color, mode: BlendMode): ColorFilter：用一个颜色和混合模式生成滤镜（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.drawing.d.ts，drawing.ColorFilter.createBlendModeColorFilter）
- BlendMode.SRC_IN = 5：r = s * da：只在原图不透明处留下着色色，等于源端的 SrcIn 着色（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.drawing.d.ts，drawing.BlendMode.SRC_IN）
- common2D.Color：alpha、red、green、blue，各是 0–255 的整数：createBlendModeColorFilter 的颜色参数（出处：鸿蒙 SDK 的 ets/api/@ohos.graphics.common2D.d.ts，common2D.Color）
- tint 不写 tintMode 时是 SRC_IN（Drawable.DEFAULT_TINT_MODE）；ImageView#setColorFilter(int) 假定 SRC_ATOP：源端各写法的混合模式（出处：android.graphics.drawable.Drawable#DEFAULT_TINT_MODE；android.widget.ImageView#setColorFilter(int)）
- fillColor 改为 colorFilter(createBlendModeColorFilter(主题色, SRC_IN)) 后，白色加透明通道的位图在浅色背景上显出着色：用 fillColor 时只剩极淡的白块（出处：卡里修好并验证过）
- colorFilter(filter: ColorFilter | DrawingColorFilter): ImageSpanAttribute：同族接口：ImageSpan 的颜色滤镜（出处：鸿蒙 SDK 的 ets/component/image_span.d.ts，ImageSpanAttribute.colorFilter）
来源：1 张卡，1 个应用
- case-cc44101b075cbccf3dfa（GameOfLife）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 7 ← 诊断
