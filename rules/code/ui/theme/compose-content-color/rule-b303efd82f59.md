# Compose 无色文本迁到 ArkUI 时，按宿主 contentColor 映射到应用色资源

审的是：代码
触发（任一种）：
- 读到：Compose `Text(...)` 没传 `color`，外层是 `Surface`/`Scaffold` 提供的 `contentColor`；写错的样子：目标 `Text` 写成 `fontColor($r('sys.color.font_primary'))`，或照搬别的页面的无色文本写法
适用范围：界面实现阶段，把 Compose 里没显式设色的文本迁成 ArkUI Text 时
做法：
- 按宿主 contentColor 解析到的主题颜色，写 `.fontColor($r('app.color.<对应色资源>'))`，不映射到 `sys.color.font_primary`
- 别的页面已有的写法只作参考，照搬前回到本页源码确认是同一个宿主
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fontColor(value: ResourceColor): TextAttribute：Text 的字色（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.fontColor）
- Text 的 fontColor 默认值 '#e6182431'：ArkUI Text 不设色时用系统字色，不会继承外层容器的内容色（出处：ts-basic-components-text.md，fontColor）
针对本应用要查的：
- 宿主 contentColor 对应的目标色资源：先按规格或源工程 Kotlin 里外层 Surface/Scaffold 的 contentColor 找到主题颜色名，再到目标工程 resources/base/element/color.json 里找同名或对应的色资源；用该色资源名写 $r('app.color.…')
来源：1 张卡，1 个应用
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
