# Compose 的 fillMaxSize、heightIn、matchContentSize 尺寸修饰

agent 会看到什么：读过的 Compose 源码里节点用 Modifier.fillMaxSize() 占剩余高度、heightIn(max) 紧接 verticalScroll、matchContentSize 让描边贴合内容；交回的写成 height('100%')、另加 100% 覆盖层，或 constraintSize 挂在了外层 Column 上

## 规矩

- rule-16d900738148｜排在固定高度兄弟之后、占剩余高度的内容区写 layoutWeight(1)，不写 100% 高｜读到：Compose Column 里内容区排在搜索栏、分隔线这类固定高度节点之后，用 Modifier.fillMaxSize() 或 LazyColumn 占满剩余高度；写错：内容区（或它的各个状态分支容器）写成 .height('100%')；或规划过的 layoutWeight(1) 包裹层没写出来，状态分支直接挂在根 Column 下
- rule-d2954c85f224｜heightIn(max) 紧接 verticalScroll 时，高度上限挂在 Scroll 上｜读到：Compose 同一 Modifier 链里 `heightIn(max = …)` 紧接 `verticalScroll(rememberScrollState())`，圆角、背景也在这个节点上；写错：目标拆成外层卡片 `Column` + `Scroll` + 内容 `Column` 后，`.constraintSize({ maxHeight: … })` 挂在外层 `Column` 上，`Scroll` 只写了 `width('100%')`；转换报告的理由是「Column 会 wrap，Scroll 不会」
- rule-c7d9f59f4667｜源端靠 matchContentSize 贴合内容的描边或指示器，画在内容节点自身，不用 100% 覆盖层｜读到：Compose 选中指示器或背景层用 Modifier.fillMaxSize()、tabIndicatorOffset(matchContentSize = true) 加 .border(...) 贴合选中项内容；写错：目标在没有定尺寸的 Stack/Row 里另放一层 .width('100%').height('100%') 的覆盖层画描边或背景
- rule-8ed9885740e5｜只绘制不改测量的修饰符落成包装组件时，遮罩层按实测内容尺寸定数值，不写 '100%'｜读到：Compose 里 Modifier.fadingEdges、Modifier.border 这类只绘制、不参与测量的修饰符，挂在由内容定高的 LazyRow 等节点上；写错：目标用不设尺寸的 Stack 包 @BuilderParam 内容，叠在上面的遮罩条写 .height('100%') 或 .width('100%')，包装层被撑到页面高
- rule-80f3a0d028c1｜源码注释说明用于撑齐宽度的零高 Text 不能跳过，目标给列设 constraintSize 的 minWidth｜读到：Compose 里带注释（如 invisible Text … aligns width）的不可见对齐子项：Text("00000", Modifier.height(0.dp))；写错：目标里省略了这个对齐子项，或照搬成 .height(0) 的 Text，列上也没有 minWidth，列宽随内容变化
