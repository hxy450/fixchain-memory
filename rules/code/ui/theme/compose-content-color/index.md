# Compose 没写颜色的文本和图标

agent 会看到什么：读到 Compose 的 Text 没传 color、Icon 没写 tint，颜色来自外层 Surface / Scaffold 的 contentColor 或 LocalContentColor，产物里是 Text 的 fontColor、Image 的 fillColor 用了哪个色资源

## 通用查法

### Compose 文本和图标没写颜色时，顺着宿主 contentColor 查出色资源显式写

审的是：代码
触发（任一种）：
- 读到：Compose 的 Text(...) 没传 color、Icon(...) 没写 tint，颜色来自外层 Surface / Scaffold 的 contentColor 或 LocalContentColor；写错的样子：目标 Text 不写 fontColor 或写 sys.color.font_primary，Image 的 .fillColor(...) 照搬相邻页面的 iconPrimary / 品牌色
适用范围：Compose 里不显式设色、靠宿主内容色着色的文本和图标，迁成 ArkUI Text / Image 时
做法：
- 从这个 Text / Icon 往外找最近的 Surface、Scaffold 的 contentColor，或 LocalContentColor 的 provides，读出主题颜色名
- 到目标 color.json 找对应的颜色资源，Text 写 .fontColor($r('app.color.<名>'))、Image 写 .fillColor($r('app.color.<名>'))；源端写了 color / tint 才照它映射，不照搬相邻页面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontColor(value: ResourceColor): TextAttribute：Text 的字色（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontColor）
- Text 的 fontColor 默认值 '#e6182431'：ArkUI Text 不设色时用系统字色，不会继承外层容器的内容色（出处：ts-basic-components-text.md，fontColor）
- fillColor(value: ResourceColor): ImageAttribute；不写时不叠加颜色：图标的内容色写在这里（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
针对本应用要查的：
- 宿主提供的内容色：源工程 Kotlin 里包住这个 Text / Icon 的 Surface、Scaffold 的 contentColor 参数，或 CompositionLocalProvider(LocalContentColor provides …)；读出颜色 token 或主题颜色名
- 内容色对应的目标色资源：目标工程 resources/base/element/color.json；找同名或对应的颜色资源，写 $r('app.color.…')
未核实：外层 Surface 没写 contentColor 时内容色怎么取默认，族里规矩没有查实；图标那张卡没核实宿主 Surface 的 contentColor，修复用次要文字色是对照截图决定的
来源：2 张卡，1 个应用
- case-40b9281a2c93eda1c790（Jetsnack）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3

## 规矩

- rule-b303efd82f59｜Compose 无色文本迁到 ArkUI 时，按宿主 contentColor 映射到应用色资源｜读到：Compose `Text(...)` 没传 `color`，外层是 `Surface`/`Scaffold` 提供的 `contentColor`；写错：目标 `Text` 写成 `fontColor($r('sys.color.font_primary'))`，或照搬别的页面的无色文本写法
- rule-ff38039af79a｜Compose Icon 没写 tint 时，目标沿用宿主内容色，不套 iconPrimary 或品牌色｜读到：Compose 的 Icon(painter = …, contentDescription = …) 没写 tint；写错：对应 Image 上写了 .fillColor(...)，用的是 iconPrimary 或品牌色对应的资源，照搬了相邻页面显式着色的写法
- rule-a2809575e8ad｜LargeFloatingActionButton 图标按 36vp、取容器内容色，不加写死语言的无障碍文案｜读到：Compose 源用 LargeFloatingActionButton，Icon 尺寸 FloatingActionButtonDefaults.LargeIconSize，tint 没写或被注释掉（取默认内容色），contentDescription = null；容器色在 primaryContainer 和 primary 间切换；写错：目标图标写成 SymbolGlyph().fontSize(24)、固定 primary 或其他写死颜色，并加写死中文的 accessibilityText
- rule-8e8e89812a99｜Compose 行组件转 ArkUI 时，Row 间距照源码，继承的内容色逐个显式写｜读到：Compose `Row` 没写 `horizontalArrangement = Arrangement.spacedBy(...)`，间距只靠子项 padding；写错：ArkUI 写成 `Row({ space: … })`，多出源端没有的间距
