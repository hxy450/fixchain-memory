# 源用 clickable 或 Card onClick 时，目标用 stateStyles 补按压态

审的是：代码
触发（任一种）：
- 读到：Compose 外层 `Modifier.toggleable(enabled = …, role = Role.Switch)` 或 `Modifier.clickable` 用默认涟漪；写错的样子：目标只有 `.onClick(...)`，没有 `stateStyles` 的 pressed 态，按下没有反馈
- 读到：Compose 源码 Modifier.clickable(onClick, role = Role.Button) 或 Card(onClick = …)，没有关掉默认 indication；写错的样子：目标组件只挂 .onClick(...)，没有 .stateStyles({ pressed: … })
适用范围：源端可点击 / 可切换组件用默认按压涟漪，迁成 ArkUI 组件时的按压反馈
做法：
- 可点击或可切换（源 enabled 为真）时，在 .onClick(...) 之外写 .stateStyles({ normal: { .backgroundColor(<底色>) }, pressed: { .backgroundColor(<底色叠按压层>) } })，补上源端自带的按压状态层
- 源端 toggleable 不可切换（enabled 为假）时不挂 onClick，也不显示按压态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stateStyles(value: StateStyles): T：按组件状态切换样式，StateStyles 里有 normal、pressed、disabled 等（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.stateStyles）
- StateStyles.pressed?: any：按下状态的样式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，StateStyles.pressed）
- clicked 和 pressed 同时用在一个组件上时，只有后注册的生效：按压叠层只写 pressed，不再同时写 clicked（出处：ts-universal-attributes-polymorphic-style.md，pressed和clicked状态说明）
- 可切换状态下加 10% 按压叠层：修复时的做法，复审通过（出处：卡里修好并验证过）
针对本应用要查的：
- 按压状态层的颜色和不透明度：源工程 Compose 主题里这个组件的内容色（MaterialTheme.colorScheme 的对应角色），以及应用依赖的 androidx.compose.material3 版本里的按压状态层定义；取内容色叠加按压层的不透明度，写进 pressed 里的 backgroundColor
未核实：Material 3 默认按压层不透明度是 10%，本机没有 Compose 源码可核；按压层的具体颜色也没在本机来源里核实；一张卡（case-5a84af0e2f5c593b9f0c）的行为出自鸿蒙 SDK API 24，本机核实用的是 API 23
来源：2 张卡，1 个应用
- case-5a84af0e2f5c593b9f0c（Cofi）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 4 ← 诊断
- case-7ced02d9c41ab6f4919a（Cofi）：做法第 1 步 ← 建议 5、诊断
