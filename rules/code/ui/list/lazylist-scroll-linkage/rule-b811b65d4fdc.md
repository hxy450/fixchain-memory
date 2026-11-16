# 规格要求侧栏与内容区滚动联动时，内容区用 List＋Scroller 承载全部一级分组

审的是：代码
触发（任一种）：
- 读到：规格或计划写着侧栏与内容区「滚动联动」「列表控制器」（如用 Repeat 和列表控制器表达选择与滚动联动），或写着安卓用 scroll synchronization；写错的样子：内容区是 Scroll 里按 selectedIndex 取出的单个分组，没有 Scroller，也没有点击滚动或滚动回写选中项的回调
适用范围：左侧一级分类、右侧内容区的侧栏分类页，规格或计划提了滚动联动或列表控制器时
做法：
- 内容区写成 List({ scroller: this.contentScroller })，用 Repeat 或 ForEach 遍历全部一级分类，每个一级分组（标题加二级分类网格）是一项；不按选中索引只渲染一个分组
- 点击侧栏第 i 项时调 this.contentScroller.scrollToIndex(i)；内容区滚动时用 List 的 .onScrollIndex((start) => …) 把 start 回写成侧栏选中项
- 写完自查：内容区遍历的是全部一级分类、绑了 Scroller、两向联动回调都在；结构里只有按 selectedIndex 取出的单个分组的，判为未满足「选择与右侧内容同步」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (options?: ListOptions): ListAttribute；ListOptions.scroller?: Scroller：List 的构造，scroller 绑定控制器（一个 Scroller 不能再绑别的滚动组件）（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListInterface、ListOptions.scroller）
- scrollToIndex(value: number, smooth?: boolean, align?: ScrollAlign, options?: ScrollToIndexOptions)：滚到第 value 项；smooth 默认 false，List 上 align 默认 ScrollAlign.START；只对 ArcList、Grid、List、WaterFlow 生效（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，Scroller.scrollToIndex）
- onScrollIndex(event: (start: number, end: number, center: number) => void): ListAttribute：子项进出 List 显示区时回调，start 是首个可见项下标（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollIndex）
- onScrollIndex(event: (first: number, last: number) => void): GridAttribute：同族接口：Grid 的可见项回调（只有 first、last）（出处：鸿蒙 SDK 的 ets/component/grid.d.ts，GridAttribute.onScrollIndex）
- onScrollIndex(event: (first: number, last: number) => void): WaterFlowAttribute：同族接口：WaterFlow 的可见项回调（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.onScrollIndex）
针对本应用要查的：
- 安卓内容区的结构：源工程侧栏分类页的代码里父组件引用的右侧内容子组件；看它是否在同一个滚动列表里遍历全部一级分类；读源码的回执中段被截断时按行号补读到这个子组件为止
未核实：两向联动的回调写法（点击滚动期间 onScrollIndex 回写会抢占选中态）由后续修复处理，这张卡只验证了遍历全部一级分组
来源：1 张卡，1 个应用
- case-722d7aa5f8d4f236bd6f（青商城）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3
