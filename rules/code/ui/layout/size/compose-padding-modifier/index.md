# Compose 的 padding 和系统栏内距修饰符

agent 会看到什么：读到 Compose 的 Modifier.padding(...)（horizontal、start / end）、statusBarsPadding / navigationBarsPadding 及它们在 heightIn、background 前后的顺序；产物里 padding、margin、constraintSize 落在哪个组件、用什么方向

## 规矩

- rule-053b24481f66｜statusBarsPadding 在 background 之前时，不在带背景的同一组件上加顶部 padding｜读到：Compose 链 heightIn(min = …).statusBarsPadding() 之后才有 .background(...)，状态栏内距在背景之前、不涂色；写错：同一个带 .backgroundColor(...) 的组件上写 .padding({ top: 状态栏高度 }) 和 .constraintSize({ minHeight: … })，状态栏区被涂成背景色
- rule-2bd76183bebf｜Compose 内距修饰符在 heightIn(min) 之前时，minHeight 要加上这段内距｜读到：Row(modifier = Modifier.navigationBarsPadding().then(…).heightIn(min = N.dp))：navigationBarsPadding() 在 heightIn 之前，最小高度作用在内距之内；写错：.constraintSize({ minHeight: N }).padding({ bottom: 导航条避让值 })，minHeight 没加上底部 padding，内容区不足 N
- rule-8734732ddd67｜源端每行各自 padding(horizontal) 时逐行复制，不提到外层，也不自行补内距｜读到：Compose 里每个子 Row 各自 Modifier.padding(horizontal = …)，分隔线在行外全宽；写错：目标把各行和分隔线包进一个 .padding({ start, end, top }) 的 Column，分隔线跟着缩进、顶部多出一段
- rule-464fb5fc734a｜源端 Start/End 边距时目标写 start/end 的 LengthMetrics，不转 left/right｜读到：源布局 XML 里有 android:paddingStart / paddingEnd / layout_marginStart / layout_marginEnd，或 layout_gravity="start|end"；写错：对应组件写成 .padding({ left, right }) / .margin({ right }) 这类物理键
- rule-004ce241bd20｜Compose 链里 padding 在 background/shape 之前时，内距放外层，背景和圆角放内层组件｜读到：Compose Modifier 链里 .padding(...)、statusBarsPadding()、navigationBarsPadding() 写在 .background(...)、.clip(...) 之前；写错：同一组件上同时写 .padding(...) 和 .backgroundColor(...) / .borderRadius(...)
- rule-f83602f464ef｜库组件内部给的单侧 inset，目标按侧写 padding({ start })，不扩成两侧对称｜读到：源是 Compose Material3 TopAppBar（或 IconButton、Scaffold 等库组件），title 槽里的 Row / Text / IconButton 只有 weight、align，没有 Modifier.padding；写错：目标端 title Row 上写 .padding({ left: 16, right: 16 }) 这类两侧对称留白，常量注释却写的是起始侧的 TopAppBarTitleInset
- rule-75cb2307afdb｜Compose 占满父宽且背景外带水平 padding 时，不在同一节点写 '100%' 宽加左右 margin｜读到：Compose 容器修饰链在 clip / background 之前有 padding(horizontal = N.dp)，自身 fillMaxWidth 或被 fillMaxWidth 的子项撑满；写错：同一节点写 .width('100%') 加 .margin({ left: N, right: N })，卡片右移、右侧贴边或被裁
