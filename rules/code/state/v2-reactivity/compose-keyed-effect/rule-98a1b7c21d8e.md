# 把 @Monitor 改成生产方回调时，回调入口比较监听字段上次值，未变就返回

审的是：代码
触发（任一种）：
- 读到：源端视觉效果按目标值变化触发：LaunchedEffect(key)、animateColorAsState(targetValue)、AnimatedContent(targetState)；原目标代码用 @Monitor 只监听运行态和结果字段；写错的样子：删掉 @Monitor 后在每次状态提交（每代 tick）尾部都调页面回调，回调里的 animateTo、getColorSync、getStringSync 没有任何变化判断
- 读到：编译报告里 @Monitor 的 WARN「needs to monitor the state variables that exist」，补丁要求删 @Monitor、改由生产方显式调回调
适用范围：ArkUI V2 里把 @Monitor 监听改成由 ViewModel 显式调用的页面回调时
做法：
- 回调入口记录被监听字段的上次值（如「运行态×结果」组合），与当前值比较，未变化就直接 return
- 或只在真正改写这些字段的路径调用；含 animateTo、资源查询的处理函数不挂在每代 tick 的提交上
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare type MonitorDecorator = (value: string, ...args: string[]) => MethodDecorator：@Monitor 按路径字符串监听若干字段（出处：鸿蒙 SDK 的 ets/component/common.d.ts，MonitorDecorator）
- @Monitor 装饰成员方法，监听的属性发生变化时才触发回调：替换成显式回调时要保留的就是这条变化门控（出处：arkts-new-monitor.md，装饰器说明）
- 回调开头加变化判断后，每代 tick 里回调耗时降到 0，不再每代重放 animateTo：修法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-31dcdb74eb848ff217c8（GameOfLife）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
