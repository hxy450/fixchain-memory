# 源端是 exitUntilCollapsed 折叠大标题顶栏时，规格不因没有现成组件就写成固定标题栏

审的是：规格
触发（任一种）：
- 读到：Compose 源码顶栏是 LargeFlexibleTopAppBar（或 LargeTopAppBar）加 TopAppBarDefaults.exitUntilCollapsedScrollBehavior(flingAnimationSpec = rememberSplineBasedDecay())，另有 collapse() 动画写 heightOffset；写错的样子：转换决策写「HarmonyOS 无 exitUntilCollapsed 现成件，简化为标题栏滚动渐变」「保底固定标题栏」「设置类页面无需折叠行为」，或 AC 把「固定标题栏 + 变色」定为验收目标
适用范围：规格提取时为 Compose 折叠顶栏写转换决策和验收条目
做法：
- 转换决策写成组合实现：列表的 onScrollFrameBegin（先折叠顶栏、余量再滚动列表，反向先展开）驱动顶栏高度，松手按 fling 和中间态吸附动画收尾，collapse() 用高度动画
- 核实后确实不能等价时，记 PD-* 保持 proposed 进确认表，不在转换决策或 AC 里自行定成降级目标
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onScrollFrameBegin(event: OnScrollFrameBeginCallback): ListAttribute：每帧滚动开始前回调，传入将要滚动的量，返回实际让列表滚动的量（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollFrameBegin）
- OnScrollFrameBeginCallback = (offset: number, state: ScrollState) => OnScrollFrameBeginHandlerResult；offset 单位 vp；返回 { offsetRemain: number }：offset 里先扣掉顶栏要折叠的量，剩下的作 offsetRemain（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，OnScrollFrameBeginCallback、OnScrollFrameBeginHandlerResult.offsetRemain）
- 用 List.onScrollFrameBegin 先折叠后滚动、余量展开，加中间态弹簧吸附和 collapse() 动画后复刻了折叠顶栏：「平台无对等」不成立（出处：卡里修好并验证过）
未核实：卡里环境是 API 24，按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-d9c2b75062eb57796ca2（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
