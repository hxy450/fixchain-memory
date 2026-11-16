# TileMode.Mirror 渐变端点平移时，写回文 stop 加 repeating 并平移面板，不转角度

审的是：代码
触发（任一种）：
- 读到：Brush.linearGradient(colors, start = Offset(o, o), end = Offset(o + d, o + d), tileMode = TileMode.Mirror)，o 由 rememberInfiniteTransition / animateFloat 往复驱动，或 horizontalGradient 的 startX / endX 随滚动偏移；写错的样子：linearGradient 的 angle 被做成 animateTo 往复旋转，colors 只有两色 0 / 1；或登记成「TileMode.Mirror 无对应」的降级
适用范围：Compose 渐变刷用 TileMode.Mirror 镜像平铺、靠平移端点做漂移或视差，译成 ArkUI linearGradient 时
做法：
- colors 写成首尾同色的回文（双色 A、B 写成 A→B→A），再开 repeating: true，就是镜像平铺；登记「无等价 / 降级」之前先试这组写法
- 端点平移改成平移面板：面板比显示区大一个相位周期，用 translate / position 按源端的方向和速度移动（按周期取模），外层容器写 .clip(true)；不把平移换成转角动画
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 双色 Mirror：回文 repeating 渐变面板比显示区大一个相位周期（端点距离的 2 倍），沿对角平移，外层 Stack clip：修好后的写法（一个回文周期含 A→B 和镜像回来的 B→A 两段）（出处：卡里修好并验证过）
- repeating 默认 false：回文 stop 要配 repeating: true 才平铺（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions.repeating）
- translate(value: TranslateOptions): T：平移面板（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.translate）
- clip(value: boolean): T：外层容器裁掉超出显示区的面板（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.clip）
来源：1 张卡，1 个应用
- case-f4f67940ef03672d639c（Jetsnack）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断
