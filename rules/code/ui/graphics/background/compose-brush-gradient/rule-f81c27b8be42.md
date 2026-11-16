# Compose 的 border 用 Brush 渐变时，目标用外层渐变加 padding 加内层实底拼描边环

审的是：代码
触发（任一种）：
- 读到：Compose 源码 Modifier.border(width, Brush.linearGradient(colors), shape)，或封装它的渐变描边 Modifier（可能按状态显隐描边）；写错的样子：目标写成单色 .border({ width: 1, color: 渐变首色 })，注释说「ArkUI border 只收单色，降级取首色」；或边宽和源 Modifier 的值不符
- 写错的样子：外层挂了 .linearGradient(...)，内层没挂 .backgroundColor 实底（组件里定义的内层颜色函数没有调用点），整块被渐变填满
适用范围：把 Compose 的渐变描边翻译成 ArkUI 胶囊、卡片、按钮等组件时
做法：
- 外层容器 .linearGradient({ angle, colors }).padding(边宽) 挂描边色，内层 .backgroundColor(实底) 加圆角，内层内距减去边宽；边宽取源 Modifier 的值（含默认参数），不降级成单色
- 写完 grep 组件里定义的颜色函数是否都有调用点，并逐一确认未选中、选中、按压三种状态下内层都盖住环的内侧
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- linearGradient(value: LinearGradientOptions): T：所有组件通用的线性渐变背景（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
- BorderOptions.color?: EdgeColors | ResourceColor | LocalizedEdgeColors：.border 每条边只收一个颜色，不收渐变（出处：鸿蒙 SDK 的 ets/component/units.d.ts，BorderOptions.color）
- 外层渐变 + padding(2) + 内层实底和圆角，内距减 2dp 环宽后，各状态与源一致：双层描边环的验证结果（出处：卡里修好并验证过）
针对本应用要查的：
- 描边宽度、颜色和显隐条件：源工程里定义这个渐变描边 Modifier 的 Kotlin 文件（按 Modifier 扩展函数名找），看 border(width = …, brush = …) 的默认参数；边宽取默认参数或调用处传的值，颜色取 Brush.linearGradient 的 colors，显隐取调用处的条件
来源：1 张卡，1 个应用
- case-40c445e1fb0a99ce0a72（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
