# 源端按末项可见状态触底加载时，用 onScrollIndex 做上升沿，不用 onReachEnd 替代

审的是：代码
触发（任一种）：
- 读到：源端 derivedStateOf { 最后可见项下标 == totalItems - 1 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；写错的样子：目标 List 上只写 .onReachEnd(() => this.loadMore())，或只在 onReachEnd 里补一个重试态判断，没有末项可见判定和上升沿
适用范围：把 Compose 状态派生的触底追加加载迁成 ArkUI List 时
做法：
- 在 .onScrollIndex((start, end) => …) 里用 end 和当前总项数（含头尾项）算条件 total > 0 && end === total - 1 && !重试态，条件由假变真时触发一次加载
- 数据或重试态变化时（如 @Monitor 监听）用最近一次的 end 复核条件；条件变假时复位，下次由假变真再触发
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onScrollIndex(event: (start: number, end: number, center: number) => void): ListAttribute：显示区域首尾子组件下标变化时回调，end 是最后一个可见子组件的下标（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollIndex）
- 列表初始化时会触发一次；首尾子组件下标变化时触发；ListItemGroup 整体占一个下标：首屏就能判定；总项数要按 List 的直接子项数（含头尾项）算（出处：ts-container-list.md，onScrollIndex）
- onReachEnd(event: () => void): ListAttribute：滚动到末尾的事件，不能单独替代末项可见状态（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onReachEnd）
- 上升沿控制器：onScrollIndex(end, 总项数, 重试态, load) 接入，数据或状态变化时用 @Monitor 调 update / reset：修复后首屏未满、追加后仍未满、重试态清除后都会继续加载（出处：卡里修好并验证过）
- onScrollIndex(event: (first: number, last: number) => void): GridAttribute：同族接口：Grid 的首尾下标回调（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.onScrollIndex）
- onScrollIndex(event: (first: number, last: number) => void): WaterFlowAttribute：同族接口：WaterFlow 的首尾下标回调，初始化时触发一次（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.onScrollIndex）
来源：1 张卡，1 个应用
- case-c9f6d4fc935ada70c215（jerboa）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
