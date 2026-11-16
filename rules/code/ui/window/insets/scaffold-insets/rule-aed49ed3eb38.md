# 浮层组件挂在自窗口顶起的 Stack 时，接 statusBarHeight 并在根节点 padding top

审的是：代码
触发（任一种）：
- 读到：Compose 浮层 Box(Modifier.fillMaxSize()) 里 scrim + 居中卡片，和列表、顶栏同在一个 Box，整体在 Scaffold innerPadding 之内；写错的样子：浮层组件根 Stack 只有 .width('100%').height('100%')，没有顶部偏移；父页嵌入时只传回调，同一 Stack 的列表首项、顶栏却带了 statusBarHeight
适用范围：宿主页 Stack 从窗口顶起、各层自行避让状态栏时，叠在列表上的浮层组件（@ComponentV2 用 @Param）
做法：
- 浮层组件加 @Param statusBarHeight: number = 0，根节点 .padding({ top: this.statusBarHeight })；父页嵌入时传 this.statusBarHeight，与兄弟层同一个值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @Param：由父到子单向同步；有本地初始值又有外部传入值时，优先用外部传入值：statusBarHeight 由父页传入，父页的值变了会同步过来（出处：arkts-new-param.md，装饰器说明、变量传递）
- 浮层组件补 @Param statusBarHeight、根 Stack padding top、父页传入后，遮罩从状态栏下沿起，与安卓一致：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-049d48a5d4b79983dde3（Jetsnack）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断
