# Compose 的 Icons.* 图标，规格逐个记原名和风格，转换决策写下载 Material Icons 原矢量

审的是：规格
触发（任一种）：
- 读到：Compose 源里 Icon(imageVector = Icons.Outlined.* / Icons.Filled.* / Icons.AutoMirrored.*) 引用 material-icons 库的具名图标，res/drawable 里没有对应文件；写错的样子：规格的转换决策写「Icons.Outlined.* → SymbolGlyph，按语义映射」「取清单里最近的 symbol」，或给具名图标配了语义近似的 sys.symbol 名（如书签写成星标）
适用范围：源端为 Jetpack Compose、图标来自 material-icons 库时，规格里的图标转换决策
做法：
- 逐个图标记录原名和风格（Outlined / Filled / AutoMirrored），转换决策写成「下载 Material Icons 原矢量为 media SVG，用 Image($r('app.media.<名>')).fillColor(<颜色>) 着色」
- 不把具名 Material 图标改写成语义近似的 sys.symbol
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(color: ResourceColor | ColorContent | ColorMetrics): ImageAttribute（@since 20）；只对 SVG 图片生效：给 media 里的 SVG 图标着色（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 返修下载 Material Icons 原矢量替换全部近似 sys.symbol 后，图标与源端一致：返修后的结果（出处：卡里修好并验证过）
未核实：卡里环境是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-4f4db97a21303734c63e（jerboa）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
