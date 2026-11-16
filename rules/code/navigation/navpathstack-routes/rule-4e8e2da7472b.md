# popUpTo 根且 inclusive 的回根导航，目标用 NavPathStack.clear()，不用 pop()

审的是：代码
触发（任一种）：
- 读到：Compose Navigation 回调里 navController.navigate(root) { popUpTo(root) { inclusive = true } }；写错的样子：完成回调里写 this.navPathStack.pop()，只退一层，回到已失效的详情页
适用范围：Compose Navigation 的清栈回根迁成 ArkUI Navigation + NavPathStack 时
做法：
- 根列表是 Navigation 首页时写 this.navPathStack.clear()；根列表是栈里的 NavDestination 时清栈后 pushPath 列表；不用 pop() 代替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- clear(animated?: boolean): void：NavPathStack 清空整个栈，回到 Navigation 首页；animated 默认 true（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.clear）
- pop(animated?: boolean): NavPathInfo | undefined：只弹出栈顶一个 NavDestination，不等于清栈回根（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pop）
- 克隆、删除完成后改成 navPathStack.clear()：修复后的写法（出处：卡里修好并验证过）
- pushPath(info: NavPathInfo, animated?: boolean): void：根列表不是 Navigation 首页时，清栈后用它把列表压回栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPath）
未核实：卡里的环境是 HarmonyOS 6.0.1(21)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-ef4b9ae3acaea9323135（Cofi）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
