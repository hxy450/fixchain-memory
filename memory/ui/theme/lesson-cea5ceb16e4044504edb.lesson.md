# Compose 组件未显式给的外观（内容色、文本样式、Material3 组件几何与槽位留白、库主题色）按宿主与库默认解析后写成 ArkUI 显式值

ID：`lesson-cea5ceb16e4044504edb` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为未写 tint/color 的 Compose Icon/Text 着色、翻译未传 textStyle 的 BasicTextField、翻译只显式传入部分参数的 Material3 组件（TopAppBar、Slider、Snackbar、LargeFloatingActionButton 等），或迁移 GlanceTheme 等依赖库主题色时

## 适用情境

Compose 的 Icon/Text 未写 tint/color，颜色来自最近宿主 Surface/Scaffold/CompositionLocalProvider 的 LocalContentColor；foundation 的 BasicTextField 不传 textStyle；Material3 组件的 thumb 形状、留隙、容器高度、内距与标题、导航、动作槽留白来自库默认与 MaterialTheme，源码本身没有 padding 修饰符；颜色来自 GlanceTheme 一类依赖库主题，源码与规格里都没有具体色值；目标组件的内置样式与之不同。

## 原因

只记显式参数时，实现者会把目标框架的内置样式当作等价物，或凭不确定的记忆写死几何值并标成“库常量”；无色文本被写成“默认 onSurface”、系统字色或别处显式使用的品牌色；库的内部留白可能是单侧规则（如 TopAppBar 标题起始侧 inset），凭记忆补值时容易写成两侧对称。

## 做法

1. Icon/Text 未写 tint/color 时，沿调用链找最近的 Surface、Scaffold 或 CompositionLocalProvider，取其 contentColor（material3 1.4.0 Surface.kt 中默认为 contentColorFor(color)）对应的资源写进规格与实现；调用链上没有任何宿主时取 LocalContentColor 的默认值（例：material3 1.4.0 的 ContentColor.kt 定义为 Color.Black）。不写“默认 onSurface”或系统字色，也不照搬别处显式使用的 iconPrimary、brand 或其他页面的先例。
2. 源端显式写了 color 与禁用 alpha（如 uiBackground.copy(alpha = if (!enabled) 0.38f else 1f)）时，分别落实为 fontColor 与按状态的 opacity，不用品牌色加 enabled() 代替。
3. foundation BasicTextField 未传 textStyle 时按 TextStyle.Default 落实（例：compose ui-text 1.11.1 的 SpanStyle 默认 DefaultFontSize 14sp、DefaultColor 黑色，系统字体）；bodyLarge 等 M3 排版只用于 M3 TextField/Text。
4. Material3 组件只传部分参数时，几何从对应 material3 版本的 Tokens 与源码取（例：SnackbarTokens、TopAppBar 的标题 inset；LargeFloatingActionButton 的图标槽为 FloatingActionButtonDefaults.LargeIconSize，material3 1.4.0 为 36dp，未写 tint 的图标取容器对应的 on 色），未传入的颜色写明取 MaterialTheme.colorScheme 的哪一项；不直接映射成 ArkUI 内置样式。规格已写入某组件的部分默认值（如容器高度）时，把同一组件的标题 inset 与槽位规则一并写出。
5. 源码没写、由库内部布局提供的留白，按库的布局规则分侧写出：哪一侧有 inset、由哪个槽位撑开；不把单侧 token 扩成对称 padding，TopAppBar 标题槽内的 Row 不自行补末端内距。
6. 思考中带问号或决定不深究的数值，不写成带库出处注释的常量；本机 Gradle 缓存（modules-2 下的 -sources.jar）找不到对应库源码时，在规格或报告里列为缺口，写明需要的库与版本交协调者。
7. 依赖库主题色（如 GlanceTheme.widgetBackground）从库包的 res/values 与 values-night 取回退值（Gradle 缓存中的 aar），不用其他设计体系的基线色代替。

## 可选检查

- 补出库内部留白后有疑问时，用源端 dump 或截图核一次两端元素与屏缘的距离；没有 dump 时在注释写明取自哪条库规则、作用于哪一侧。

来源支持：7 张卡 · 4 次迁移 · 2 个应用

## 来源（按需复核）

- [case-036361d8949e7daf5247](../../../store/cases/case-036361d8949e7daf5247/c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79.json) · 结论：diagnosis, recommendation:5
  卡片版本：`c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79`
- [case-2280cf8a2bf7682ff26b](../../../store/cases/case-2280cf8a2bf7682ff26b/f21f8d2582fa9e731eaa95a1fdc6350d54167eb1f4656c7eda7ea18219ab8682.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f21f8d2582fa9e731eaa95a1fdc6350d54167eb1f4656c7eda7ea18219ab8682`
- [case-40b9281a2c93eda1c790](../../../store/cases/case-40b9281a2c93eda1c790/9cc0a2a0ff4d089d6f237b75d7db454c395cd5dce33dc97c1a03c8f4d14dfa07.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`9cc0a2a0ff4d089d6f237b75d7db454c395cd5dce33dc97c1a03c8f4d14dfa07`
- [case-77c6596fcdf362f9e832](../../../store/cases/case-77c6596fcdf362f9e832/c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a.json) · 结论：recommendation:7
  卡片版本：`c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a`
- [case-7f41c5604c3a5213023b](../../../store/cases/case-7f41c5604c3a5213023b/4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8.json) · 结论：recommendation:2
  卡片版本：`4242659d6c555274f4b22e2a7d309bf85bb1c658b28e7509473a012ac96234c8`
- [case-83dafcc0eaba740bd9c0](../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：recommendation:6
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4, recommendation:6
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
