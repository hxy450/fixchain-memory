# TopAppBar 带 enterAlways 时，目标用 List.onScrollFrameBegin 先改顶栏偏移

审的是：代码
触发（任一种）：
- 读到：val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior(rememberTopAppBarState())，Scaffold 挂 Modifier.nestedScroll(scrollBehavior.nestedScrollConnection)；写错的样子：目标顶栏是固定高度的 Row（.height(56) 或 .height(64)），没有和 List 滚动联动，注释写「enterAlways 降级为固定顶栏」「ArkUI 无折叠联动等价」「同某页决策」
适用范围：Compose enterAlways 折叠顶栏迁成自绘 ArkUI 顶栏 + List 时
做法：
- 顶栏和内容放在同一个 Column；List.onScrollFrameBegin((offset: number, state: ScrollState) => …) 里先把顶栏 heightOffset 在 0…-顶栏高 之间改掉，本帧改了多少就从 offset 里扣掉，返回 { offsetRemain: 剩余量 }，复刻 onPreScroll
- 停止滚动时按 collapsedFraction 0.5 吸附到全展开或全收起；按累计用户滚动量判定 overlappedFraction > 0.01 时容器色 surface → surfaceContainer
- 页面规格、功能规格（HARD 行为等价）和 pitfall 不一致时按更严格的行为实现；「ArkUI 无直接等价」不等于可降级；参考同族页面只复用写法，不继承它的降级决策
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onScrollFrameBegin(event: OnScrollFrameBeginCallback): ListAttribute：List 每帧滚动开始前回调，返回实际要滚的量（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollFrameBegin）
- type OnScrollFrameBeginCallback = (offset: number, state: ScrollState) => OnScrollFrameBeginHandlerResult；offset 单位 vp：offset 和顶栏 vp 高度同单位，可以直接相减（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，OnScrollFrameBeginCallback）
- OnScrollFrameBeginHandlerResult.offsetRemain: number：返回给 List 的实际滚动量，即扣掉顶栏吃掉的部分后的剩余（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，OnScrollFrameBeginHandlerResult.offsetRemain）
- onScrollFrameBegin(event: OnScrollFrameBeginCallback): GridAttribute：同族接口：Grid 的同一回调（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.onScrollFrameBegin）
- onScrollFrameBegin(event: OnScrollFrameBeginCallback): ScrollAttribute：同族接口：Scroll 的同一回调（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.onScrollFrameBegin）
- onScrollFrameBegin(event: OnScrollFrameBeginCallback): WaterFlowAttribute：同族接口：WaterFlow 的同一回调（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.onScrollFrameBegin）
- heightOffset 在 0…-64 之间、本帧有变化时吞掉滚动量；停止按 0.5 吸附；吸附和色变用弹簧曲线：返修后的联动（出处：卡里修好并验证过）
- function springMotion(response?: number, dampingFraction?: number, overlapDuration?: number): ICurve：吸附动画用的弹簧曲线，参数是 response 和 dampingFraction，不是 stiffness（出处：鸿蒙 SDK 的 ets/api/@ohos.curves.d.ts，curves.springMotion）
未核实：卡里环境是 API 24，本机按 API 23 声明核实
来源：1 张卡，1 个应用
- case-6aada7248be5df4c858e（jerboa）：做法第 1 步 ← 诊断、建议 3；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 3、建议 4；取值 7 ← 诊断
