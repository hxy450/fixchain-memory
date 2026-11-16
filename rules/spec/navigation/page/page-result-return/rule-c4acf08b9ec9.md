# 规格里每条回传通道写清载荷类型、生产端出栈调用和消费端触发点

审的是：规格
触发（任一种）：
- 读到：安卓源用 savedStateHandle 回传：子页写结果后 navigateUp()，来源页回来后读取；写错的样子：实现映射只写「NavPathStack param + onResult 回调 / emitter 事件」或「addReturn 后 pop」，没写载荷类型、生产端用哪个出栈调用、消费端在哪个时机读取
适用范围：规格或基础设施阶段，给跨页回传写实现映射时
做法：
- 每条回传通道写三项：载荷类型；生产端出栈调用；消费端触发点
- 走 pushPathByName 的 onPop 时写明生产端必须 pop(result)；走共享通道时写明消费端在 NavDestination.onShown 等回到页面的时机读取
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onPop 仅在 pop、popToName、popToIndex 设置了 result 参数后触发：规格里选 onPop 轨时，生产端的出栈调用必须带 result（出处：ts-basic-components-navigation.md，pushPathByName11+）
- pop(result: Object, animated?: boolean): NavPathInfo | undefined：生产端出栈调用的写法（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pop）
来源：1 张卡，1 个应用
- case-60576c483fb94367a81b（jerboa）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
