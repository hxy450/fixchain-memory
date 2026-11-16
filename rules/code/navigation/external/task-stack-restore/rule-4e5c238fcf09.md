# 路由恢复持久化整个 NavPathStack 并整栈重建，参数用入栈时的原值

审的是：代码
触发（任一种）：
- 读到：规格或台账的 PD 要求进程回收后恢复路由栈；源端用 `TaskStackBuilder.addNextIntentWithParentStack` 组栈；写错的样子：只存最后一个路由、恢复时只 `pushPathByName` 一页，并把恢复页参数写死成续接值；恢复后栈底没有父页，返回会露出空的 `Navigation` 宿主页
适用范围：目标端用单 Navigation + NavPathStack、手动持久化并恢复路由栈时
做法：
- 每次路由变化后持久化整栈：stack.getAllPathName() 的全部名字，加上逐个 stack.getParamByIndex(i) 的参数
- 恢复时按保存的顺序逐个 stack.pushPathByName(name, param, false) 重建，参数用保存的原值；确认栈底有父页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 持久化整栈（getAllPathName / getParamByIndex），恢复时重建整栈并保留入栈时的参数：修好的写法（出处：卡里修好并验证过）
- getAllPathName(): Array<string>：取栈里所有 NavDestination 的名字（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getAllPathName）
- getParamByIndex(index: number): unknown | undefined：按从 0 开始的下标取某页参数（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getParamByIndex）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：按名字入栈一页，恢复时逐页调用（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
来源：1 张卡，1 个应用
- case-a8413b6eae04f3be7d9d（Privacy Friendly 2048）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、建议 4；取值 1 ← 诊断
