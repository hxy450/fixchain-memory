# 组件调用同目录的自定义 Modifier 扩展时，按扩展定义的默认参数和绘制顺序写，环宽不自定

审的是：代码
触发（任一种）：
- 读到：Compose 组件调用同目录文件里的自定义 Modifier 扩展（渐变描边、渐变着色等），调用时没传宽度参数，参数声明里带 Dp 默认值；写错的样子：目标描边宽度不是扩展定义里的默认值，如用 .padding(1) 露出 1vp 的环
适用范围：Compose 组件依赖同目录的 Modifier 扩展函数，迁成 ArkUI 时
做法：
- 写组件前先读扩展定义，取出默认参数和绘制顺序（先 drawContent 再 drawRect 就是内容在下、渐变在上）；写完才读到定义的，回头核对已写组件里的对应值
- 环宽照默认参数的 dp 数值写成 vp；渐变环在圆内侧画一圈同宽的渐变，不用 .padding 露边代替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- color?: EdgeColors | ResourceColor | LocalizedEdgeColors：BorderOptions 的颜色只收纯色，.border 画不了渐变描边（出处：鸿蒙 SDK 的 ets/component/units.d.ts，BorderOptions.color）
针对本应用要查的：
- 扩展的默认参数和绘制顺序：源工程同目录的 Kotlin 文件里该 Modifier 扩展函数的参数声明和函数体；参数声明里的默认值（如 Dp 默认值）照数值搬到目标；函数体里 drawContent 和 drawRect 的先后决定哪层在上
来源：1 张卡，1 个应用
- case-583c797930b89c0d4e63（Jetsnack）：做法第 1 步 ← 建议 2；做法第 2 步 ← 诊断、建议 2
