# 规格写 Compose 修饰符链时写明内距和最小高度的先后，不只平列各项

审的是：规格
触发（任一种）：
- 读到：源码 Modifier.navigationBarsPadding().then(…).heightIn(min = N.dp) 这类内距与 heightIn 串在一条链上；写错的样子：规格只平列「navigationBarsPadding、水平 24dp、minHeight 56dp」，没写先后，看不出最小高度在内距之内还是之外
适用范围：规格提取时描述 Compose 组件尺寸和内距的条目
做法：
- 按修饰符链的顺序写，并写明结论：例如「navigationBarsPadding 在 heightIn 之前，最小高度 N 作用在导航条内距之内，目标端 minHeight = N + 底部避让值」
未核实：修饰符先后的语义出自 Compose 库代码，本机没有源码，按卡写
来源：1 张卡，1 个应用
- case-cfab70f115f2d290e44a（Jetsnack）：做法第 1 步 ← 诊断
