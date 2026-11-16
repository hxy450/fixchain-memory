# Material Icons 的 media 未就绪时，按原名引用并登记占位，不用近似 sys.symbol

审的是：代码
触发（任一种）：
- 读到：Compose 源里 Icons.Filled.Bookmark、Icons.Outlined.MoreVert、Icons.Outlined.Menu 这类具名 Material 图标，目标 media 里还没有对应 SVG；写错的样子：写成 SymbolGlyph($r('sys.symbol.star_fill'))、sys.symbol.ellipsis、sys.symbol.list_bullet 等近似字形，报告自认「视觉近似降级」
适用范围：界面实现阶段，源端 material-icons 库的图标在目标端还没有资源文件时
做法：
- 按原图标名和风格引用 media 资源，如 Image($r('app.media.<风格>_<原名>')).fillColor(<颜色>)，并登记 `resource-pending-asset` 占位交资源阶段补齐
- 不因零资产依赖、编译稳定改用近似 sys.symbol
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute（@since 20）；只对 SVG 图片生效：media 里的 SVG 图标按源端 tint 着色（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 返修把 sys.symbol 逐处换成 Material Icons 原矢量（收藏用 filled/outlined 两枚 bookmark，MoreVert 用 outlined more_vert）：返修后的写法（出处：卡里修好并验证过）
未核实：卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-4f4db97a21303734c63e（jerboa）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 2 ← 诊断
