# 源端背景是 Brush.horizontalGradient 时，目标写 linearGradient，不换成纯色

审的是：代码
触发（任一种）：
- 读到：Compose 组件用 Modifier.background(Brush.horizontalGradient(colors)) 着色，外层 Surface(color = Color.Transparent)，colors 取自主题调色板里的某个渐变名；写错的样子：目标只写 .backgroundColor($r('app.color.…')) 一个品牌纯色，没有 .linearGradient(...)
适用范围：把 Compose 共享按钮等组件的渐变背景迁成 ArkUI 时
做法：
- 写成 .backgroundColor(Color.Transparent).linearGradient({ direction: GradientDirection.Right, colors: [[c1, 0], [c2, 1]] })，不设 angle；colors 按源端列表顺序
- 源端只给了调色板名时，先解析到具体色序，每个色阶再换成同值的 $r('app.color.*')
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- linearGradient(value: LinearGradientOptions): T：组件背景的线性渐变（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
- LinearGradientOptions：direction 默认 GradientDirection.Bottom，angle 默认 180，colors: Array<[ResourceColor, number]>：不写 direction 是自上而下；colors 每项是 [颜色, 位置]（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions）
- GradientDirection.Right：From left to right：对应 horizontalGradient 的从左到右（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，GradientDirection.Right）
- direction 在 angle 不是 undefined 时不生效；colors 的位置取值 [0, 1.0]，应递增：要用 direction 就别写 angle（出处：ts-universal-attributes-gradient-color.md，LinearGradientOptions 对象说明）
- 背景设透明并加 linearGradient Right 两个色阶后，按钮和源端一致：单一品牌纯色丢了渐变（出处：卡里修好并验证过）
- constructor(options: LinearGradientOptions)（LinearGradientStyle，@since 20）：同族接口：文字着色用的线性渐变样式（出处：鸿蒙 SDK 的 ets/component/text_common.d.ts，LinearGradientStyle.constructor）
针对本应用要查的：
- 调色板里这个渐变名对应的色序：源工程主题 Kotlin 文件里调色板对象的构造，按渐变名找它指向的 listOf(...)，再找各元素的 Color(0x…) 常量；按 listOf 的顺序依次写进 colors，每个元素换成同值的 $r 令牌
未核实：源端多于两个颜色时 Compose 按等分分布、目标位置取 i/(n-1)，未核实
来源：1 张卡，1 个应用
- case-4a0392021e915d5b60d1（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 5 ← 诊断
