# 安全区避让值的派工、前向引用和交付结论

agent 会看到什么：源端子页经 Scaffold innerPadding 拿 inset、WindowModel 契约写明顶底两侧避让、避让值只取 TYPE_NAVIGATION_INDICATOR 一个值，派工写「statusBarHeight 本页不使用」、前向引用只登记一侧，或交付说明写「视觉不受影响」

## 规矩

- rule-a2e19eff847d｜派工向子页下发 statusBarHeight 时，不写「本页不使用」，除非给出父容器已消费的源码位置｜读到：源端子页经 Scaffold 的 content { padding -> … Modifier.padding(padding) … } 拿到 innerPadding；写错：派工说明写「接受 @Param statusBarHeight: number = 0（本页不使用）」或「Android 未做 statusBarsPadding，本页也不加」，没给 Android 父容器已消费这个 inset 的源码位置
- rule-0ff5f5f4943f｜安全区前向引用的登记写明顶、底两侧，解除时两侧都核对，不只兑现写到的一侧｜读到：WindowModel 契约写明前景避让统一读 windowTopPadding / windowBottomPadding；写错：Layer 3 前向引用的登记文本只写一侧（如「列表底部 padding 消费 inset」），或写「顶部避让随基座兑现」；派工照登记只要求接底部
- rule-82a7b20201e0｜各导航模式避让值相同、视觉占用不同时，交付说明标明未验证的模式，不下「视觉不受影响」结论｜读到：避让值只取 getWindowAvoidArea(TYPE_NAVIGATION_INDICATOR).bottomRect.height 一个 px 值，代码不区分三键和手势模式；写错：交付说明写「手势模式仅有微小增量，视觉不受影响」一类没有实测依据的结论，没列出哪些导航模式未验证
- rule-00a4eed341db｜浮层挂在自窗口顶起的 Stack 里时，slot 契约和派工带上与兄弟层相同的 statusBarHeight｜读到：页面规格里同一 Stack 三层：列表首项、顶栏都带 statusBarHeight，浮层是 needs_immersive_safearea=false 的 modal_overlay；写错：slot 契约、覆盖清单和派工词给浮层组件只传回调（如 onDismiss），没有 statusBarHeight
- rule-4d43d6c63fd1｜标题栏避让前向项标已解除前，确认页面里顶部避让值确实用在 padding 上｜读到：前向项登记里有标题栏避让项（暂用系统标题栏，待改 hideTitleBar 加自绘工具栏）；写错：回报、信封或前向项登记里把这项写成已解除，而对应页面文件里顶部避让值没出现在任何 padding 里（只声明或 connect 了窗口模型）
