# 编译报 .mask 不支持渐变时，改用 linearGradient 覆盖层加 blendMode(DST_IN)

审的是：代码
触发（任一种）：
- 读到：Compose 内容上用 verticalGradient 做的渐隐修饰符（fadingEdge）；或规格把它映射为 linearGradient 遮罩；写错的样子：写成 .mask({ gradient: [...] })（编译不过），或编译修复时删掉整段渐隐、只留一句 TODO(...)
- 写错的样子：渐变覆盖层写成 .height('100%')，在 List 里取到视口高度，把单项撑满整屏
适用范围：Compose 内容渐隐迁成 ArkUI，或编译修复遇到 SDK 不支持的遮罩写法时
做法：
- 写成 Stack { 内容 ; 覆盖层 }，覆盖层 .linearGradient({ direction: GradientDirection.Bottom, colors: [[不透明色, 渐隐起点], [透明色, 1.0]] }).blendMode(BlendMode.DST_IN)，起止比例取源端 verticalGradient 的停靠点；不要删除渐隐
- 覆盖层高度取内容的实测高度，不写 height('100%')
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- mask(value: ProgressMask): T：CommonMethod.mask 现行重载只收 ProgressMask（形状遮罩已改为 maskShape），没有 gradient 参数（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.mask）
- linearGradient(value: LinearGradientOptions): T；direction 默认 GradientDirection.Bottom：覆盖层的线性渐变（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
- blendMode(value: BlendMode, type?: BlendApplyType): T；type 默认 BlendApplyType.FAST：覆盖层与下方内容的混合方式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blendMode）
- BlendMode.DST_IN = 7，r = d * sa：只保留下方内容与覆盖层不透明部分重叠处；覆盖层不透明处内容保留、透明处内容消失（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BlendMode.DST_IN）
- DST_IN 渐变覆盖层补上了渐隐；覆盖层用 height('100%') 时在 List 内取到视口高度、把首项撑满整屏，改为按内容实测高度后正常：做法和高度取法（出处：卡里修好并验证过）
针对本应用要查的：
- 渐隐的起止比例和方向：源工程 Compose 文件里渐隐修饰符的 verticalGradient 参数；读出颜色停靠点（如从某比例到 1.0），对应写进 linearGradient 的 colors 比例
未核实：卡里没写覆盖层或其容器是否需要 BlendApplyType.OFFSCREEN；卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23
来源：1 张卡，1 个应用
- case-bcc79fa7d3d15ef4a8b2（jerboa）：做法第 1 步 ← 建议 6、诊断；做法第 2 步 ← 建议 6；取值 5 ← 诊断
