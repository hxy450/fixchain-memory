# M3 IconButton 外部 size 小于 48dp 且带圆形背景时，按 48 圆实现、圆心不变

审的是：代码
触发（任一种）：
- 读到：源码 IconButton(… modifier = Modifier….size(x.dp) …)，x < 48；规格写 .width(x).height(x)；写错的样子：Button({ type: ButtonType.Circle }).width(36).height(36)，margin 仍按源码左上角的 16 / 10
- 读到：M3 `IconButton(modifier = Modifier….size(...).background(..., CircleShape))`，外部 `size` 小于 48.dp；写错的样子：目标按钮按字面 size 写 `width`/`height` 和一半大小的 `borderRadius`，背景圆比源端小
适用范围：把 Material3 IconButton 迁成 ArkUI 圆形按钮，外部 modifier 的 size 小于 48dp 并带圆形 background 时
做法：
- 按 minimumInteractiveComponentSize 画 48 的圆：`.width(48).height(48)`（自绘背景的再加 `.borderRadius(24)`），margin 各减 (48 − x) / 2，让圆心仍在原槽位中心（x 为 36 时各减 6）；源码的 x 和偏移常量保留并加注释
- 在交回信封的 low_confidence_uncertain_regions 里列出这处与规格尺寸的差异；核对方法：在源码里搜 IconButton( 出现处的 .size( 数值，逐个和 48 比
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (options: ButtonOptions): ButtonAttribute；ButtonOptions.type?: ButtonType；ButtonType.Circle：圆形按钮的写法（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonInterface、ButtonOptions.type、ButtonType.Circle）
- Button 改为 48、margin 各减 6 保持圆心后，dump 量得 48vp，与安卓一致：修好后的写法（出处：卡里修好并验证过）
- 外部 size 36dp 带圆形背景时，Android 上背景圆实为 48dp；改成 48 圆、margin 各减 6 后与源端一致：双端截图对照确认过（出处：卡里修好并验证过）
未核实：最小 48dp 出自 Compose Material3 库代码，本机没有源码，按卡写
来源：2 张卡，1 个应用
- case-6eec56e15cefd5c659cb（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 2 ← 诊断
- case-d54a9506e30031090325（Jetsnack）：做法第 1 步 ← 建议 5、诊断；取值 3 ← 诊断
