# 可恢复页面的路由参数要可序列化，接收端按字段识别，不只靠 instanceof

审的是：代码
触发（任一种）：
- 读到：源端 NavHost 路由带参数，进程回收后参数由框架随返回栈恢复；写错的样子：接收页用 `instanceof` 某个参数类判断 NavPathStack 传来的参数；开启 recoverable 后恢复出的参数是同形的普通对象，判断不成立
适用范围：NavDestination 设了 recoverable(true) 的页面接收路由参数时
做法：
- push 的参数只放可序列化的字段（数字、字符串、普通对象），不依赖类实例和回调
- 接收端按字段识别（如 typeof param.id === 'number'），不只用 instanceof 判断类实例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 恢复过程中不可序列化的信息（不可序列化的参数、用户设置的 onPop 等）会被丢弃，无法恢复：恢复出的参数只剩可序列化的字段（出处：ts-basic-components-navigation.md，recoverable）
- 参数识别从 instanceof 改为按 id 字段识别后，恢复的页面能读到参数：修好的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-30dbf63ea8a03d315607（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
