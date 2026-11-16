# 派工向子页下发 statusBarHeight 时，不写「本页不使用」，除非给出父容器已消费的源码位置

审的是：计划与派工
触发（任一种）：
- 读到：源端子页经 Scaffold 的 content { padding -> … Modifier.padding(padding) … } 拿到 innerPadding；写错的样子：派工说明写「接受 @Param statusBarHeight: number = 0（本页不使用）」或「Android 未做 statusBarsPadding，本页也不加」，没给 Android 父容器已消费这个 inset 的源码位置
适用范围：派工向子页下发状态栏高度一类参数并说明用法时
做法：
- 派工里不同时写「下发 statusBarHeight」和「本页不使用」；认为不必消费的，写出 Android 侧父容器已消费该 inset 的源码位置（哪个 Composable 的哪个 padding / windowInsetsPadding）
来源：1 张卡，1 个应用
- case-b4d0b2f21cf92275a46b（Jetsnack）：做法第 1 步 ← 建议 3
