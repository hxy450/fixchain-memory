# 源端左右分类双向联动时，右侧用带 Scroller 的分组 List 并接 onScrollIndex

审的是：代码
触发（任一种）：
- 读到：源端 Compose 左侧分类栏 + 右侧分组列表：rememberLazyListState、左侧选中后 animateScrollToItem、按 visibleItemsInfo / derivedStateOf 可见项回写选中态；写错的样子：目标右侧是没有控制器的 Scroll（只渲染选中分组，或用 Repeat 堆全部分组），左侧 onClick 只改 selectedIndex，没有 Scroller、scrollToIndex、onScrollIndex
适用范围：把源端左右双向联动的分类页迁成 ArkUI 时
做法：
- 右侧写成 List({ scroller: this.scroller })，每个一级分类一个 ListItem；左侧 onClick 调 this.scroller.scrollToIndex(index, true)；右侧 .onScrollIndex((start: number) => { 选中索引 = start })
- 改了右侧展示结构（如由只显示选中分组改为显示全部分组）时，确认左侧 onClick 仍会改变右侧可见内容；提交前 grep 目标文件确有 Scroller、scrollToIndex 和 onScrollIndex
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- scrollToIndex(value: number, smooth?: boolean, align?: ScrollAlign, options?: ScrollToIndexOptions)：Scroller 滚到指定索引；smooth 默认 false，List 上 align 默认 ScrollAlign.START；只对 ArcList、Grid、List、WaterFlow 生效（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，Scroller.scrollToIndex）
- onScrollIndex(event: (start: number, end: number, center: number) => void): ListAttribute：List 子组件进出显示区时回调首尾和中间索引（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollIndex）
- (options?: ListOptions): ListAttribute；ListOptions 里 scroller?: Scroller：List 绑定 Scroller 的写法（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListInterface）
- 右侧为带 Scroller 的分组 List，左侧点击 scrollToIndex，onScrollIndex 同步左侧：返修后的写法（出处：卡里修好并验证过）
- onScrollIndex(event: (first: number, last: number) => void): GridAttribute：同族接口：Grid 的可见索引回调（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.onScrollIndex）
- onScrollIndex(event: (first: number, last: number) => void): WaterFlowAttribute：同族接口：WaterFlow 的可见索引回调（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.onScrollIndex）
来源：1 张卡，1 个应用
- case-455133ba2c8a862f7ce2（青商城）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
