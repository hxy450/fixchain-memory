# Compose Box 叠放子项的对齐和定位（contentAlignment、Modifier.align）

agent 会看到什么：读过的 Compose 源码里 Box(contentAlignment = …) 叠放子项，子项用 Modifier.align(Alignment.BottomCenter) 等钉在顶部、底部或角上；交回的 Stack 写了 justifyContent、不存在的 Alignment.CenterStart、子项上的 .align()，或把顶栏底栏塞进全屏 Column 加 Blank，定位只留在注释里

## 规矩

- rule-f9efab66820d｜Stack 的内容对齐用 Stack({ alignContent })，不写即居中，不用 justifyContent｜读到：Compose `Box(contentAlignment = Alignment.Center)` 一类的居中叠放布局，迁成 ArkUI `Stack`；写错：`Stack() {…}` 后面写了 `.justifyContent(FlexAlign.Center)`，编译报 Property 'justifyContent' does not exist on type 'StackAttribute'
- rule-27c15967e7ca｜ArkTS 里出现 Alignment.CenterStart 等 Compose 名时，换成实有枚举并按语义重选接口｜读到：Compose 源码或问题单里用 Compose 的对齐名描述位置，如 `Alignment.CenterStart`；写错：.ets 里写了 `Alignment.CenterStart`（ArkUI 的 Alignment 没有这个成员，编译不过）
- rule-a65830ef2aee｜Box 子项有 Modifier.align 非默认位置时，Stack 子项写 .position 实际定位｜读到：源 Compose Box 里子项写 Modifier.align(Alignment.BottomCenter) 等非左上位置；规格写「底部居中」「Stack 底部对齐」；写错：目标 Stack({ alignContent: Alignment.TopStart }) 里这个子项只有 width / zIndex，没有 .position / .align / .markAnchor，底部定位只留在注释或转换报告里
- rule-f13a6358d56b｜要把 Stack 子项钉到顶或底时，不写子项的 .align()，改用 position 或外包全屏容器｜读到：Compose `Box` 子项上的 `Modifier.align(Alignment.BottomCenter)`，把底栏钉在底部；写错：Stack 子项上写 `.align(Alignment.Top)` / `.align(Alignment.Bottom)`，或把 `.align(Alignment.Bottom)` 写进子项 @Builder 里 Row 的修饰链，想把它定到顶部或底部
- rule-d2cdd36bbf1e｜Box 里各占自身高度的悬浮顶栏、底栏，迁到 Stack 时逐个定位，不合并成全屏 Column｜读到：Compose `Box(fillMaxSize)` 里叠在滚动内容上、只占自身高度的 `Modifier.zIndex` 顶栏和 `Modifier.align(Alignment.BottomCenter)` 底栏；写错：两栏被并进 Stack 里一个 `Column().width('100%').height('100%')`，中间 `Blank().layoutWeight(1)` 撑开
- rule-13cf65848476｜Stack 子项不靠 .align() 定位，改用 alignContent 或 .position｜写错：Stack 子项上写 .align(Alignment.Start / End / Top / Bottom) 想贴到容器边上，结果落在中央或左缘
