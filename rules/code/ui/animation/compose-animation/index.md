# Compose 的尺寸、内容切换和列表项动画

agent 会看到什么：读到 Compose 的 Modifier.animateItem()、animateContentSize()、AnimatedContent 的 transitionSpec / SizeTransform，交回的代码在 ListItem、ForEach 或切换容器上没写对应的 animateTo、transition、animation

## 规矩

- rule-0cc01e3793bf｜源端有尺寸、内容切换或条目位移动画时，目标实现对应动画，不自行省略｜读到：Surface(modifier = Modifier.animateContentSize())，或 AnimatedContent 的 transitionSpec 带 .using(SizeTransform(clip = false))；写错：目标只有 TransitionEffect 滑入滑出，容器 height 在切换时跳变，没有 .animation(...) 之类的尺寸动画，也没登记缺口
- rule-02179e51e296｜列表项带 animateItem() 时，增删用 animateTo 包裹并给 ListItem 加转场｜读到：Compose 列表项上有 Modifier.animateItem()（如 ListItem(modifier = Modifier.animateItem())），或者某一项随持久化状态回推而消失；写错：数据数组直接赋值、没有 animateTo，ListItem 上没有 .transition(...)；由持久化回推的移除写成同步把显示标志置 false
- rule-32716db33ad8｜源 Compose 动画逐帧刷新时，目标用 displaySync 逐帧驱动，不用 500ms setInterval｜读到：源端进度由 Compose `Animatable.animateTo(…, tween(…, LinearEasing))` 逐帧驱动；规格映射行写高频 tick，派工却写 500ms ticker；写错：目标用 `setInterval(…, 500)` 驱动进度环和计时文本
- rule-402e5a30a5fc｜Compose Animatable 改写成自驱计时时，进度按绝对帧时间算，不钳制、不累加增量｜读到：Compose `Animatable(0f)` / `Animatable(Color)` 用 `animateTo(target, tween(durationMillis = …, easing = LinearEasing))` 推进进度；写错：目标逐 tick 累加增量，并用 `Math.min(now - <上次时间>, <若干倍 tick>)` 给单次增量设上限；注释称「后台近似冻结」
- rule-b44373513b13｜源端 expandVertically 或规格写高度过渡时，不用 TransitionEffect.OPACITY 代替｜读到：源 AnimatedVisibility(enter = expandVertically(), exit = shrinkVertically())；或规格写「if/else 条件渲染 + animateTo 高度过渡，等价 expandVertically」；写错：目标条件渲染的块只有 .transition(TransitionEffect.OPACITY.animation(...)) 或 OPACITY.combine(scale({ y: 0 }))，没有高度过渡，切换状态时没有 animateTo，也没登记不确定项
- rule-c08f79f49a3b｜NavHost 自定义转场迁成 customNavContentTransition 加页面绑定，常量要有消费点｜读到：源 NavHost 的 enterTransition / exitTransition / popEnterTransition / popExitTransition 写了 scaleIn、slideIn、scaleOut、slideOut 和 tween 时长；写错：Navigation 上没有 .customNavContentTransition(...)，只定义了一个没人引用的转场常量类，注释写「已知近似」
