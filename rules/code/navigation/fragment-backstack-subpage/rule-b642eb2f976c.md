# 源端 popBackStack() 时，目标把 pop 推迟到下一轮并在根页不出栈

审的是：代码
触发（任一种）：
- 读到：返回分支调 popBackStack()（异步），并按 getBackStackEntryCount() == 1 判断是否回到列表根；写错的样子：同步调 navPathStack.pop()，不判断栈深，会越过列表根
适用范围：把 FragmentManager.popBackStack 迁成 NavPathStack 出栈时
做法：
- 把 pop 排到下一轮再执行；执行前看 navPathStack.size()，已在列表根（栈里没有可出的页）时什么都不做
- 源端按栈深决定的后续动作（如恢复标题栏、发回到上级的事件）放在详情出栈、回到根页之后由根页触发
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- popBackStack 是异步的：只把出栈请求排队，回到事件循环后才执行：源端出栈不是当场生效（出处：android.app.FragmentManager#popBackStack）
- pop(animated?: boolean): NavPathInfo | undefined：目标端出栈，栈为空时返回 undefined（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pop）
- size(): number：当前栈里的页数，用来判断是否已在根（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.size）
- pop 排到下一轮、不越过列表根，上级事件由根页在详情出栈后发出，修好：修好后的写法（出处：卡里修好并验证过）
未核实：「排到下一轮」用哪种调度方式卡里没写
来源：1 张卡，1 个应用
- case-aebac48fa7acdb86e57e（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 4 ← 诊断
