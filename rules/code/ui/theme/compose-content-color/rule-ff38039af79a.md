# Compose Icon 没写 tint 时，目标沿用宿主内容色，不套 iconPrimary 或品牌色

审的是：代码
触发（任一种）：
- 读到：Compose 的 Icon(painter = …, contentDescription = …) 没写 tint；写错的样子：对应 Image 上写了 .fillColor(...)，用的是 iconPrimary 或品牌色对应的资源，照搬了相邻页面显式着色的写法
适用范围：把 Compose 里没写 tint 的 Icon 迁成 ArkUI Image 时的颜色
做法：
- 源 Icon 写了 tint 才映射到那个颜色的资源；没写时顺着宿主找内容色，fillColor 用它对应的颜色资源
- 不照搬相邻页面里显式写了 iconPrimary 或品牌色的图标的颜色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(value: ResourceColor): ImageAttribute；不写时不叠加颜色：宿主内容色映射到的颜色资源写在这里（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 没写 tint 的关闭图标、行首图标改成次要文字色后与源端一致：修复者对照截图选的颜色（出处：卡里修好并验证过）
针对本应用要查的：
- 宿主提供的内容色：源工程里包住这个 Icon 的 Surface 或自定义 Surface 的 contentColor 参数，或 CompositionLocalProvider(LocalContentColor provides …)；读出颜色 token，再在目标工程 resources/base/element/color.json 里找对应的颜色资源
未核实：卡里没核实宿主 Surface 的 contentColor，修复用次要文字色是对照截图决定的；卡里记的环境没写鸿蒙 SDK 版本，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-40b9281a2c93eda1c790（Jetsnack）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
