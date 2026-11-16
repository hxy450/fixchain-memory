# ListItem 高度随内容且项内有 layoutWeight 时用 ForEach，不换 Repeat

审的是：代码
触发（任一种）：
- 读到：List 里用 LazyForEach(IDataSource) 渲染 ListItem，每项高度由内容决定（分组条数不等、可折叠），项内有 alignSelf(ItemAlign.Stretch) 的贯穿装饰、layoutWeight(1) 的竖线或内容列；写错的样子：改写成 Repeat<T>(items).each(... ListItem ...).key(...).virtualScroll()，首个 ListItem 被撑成接近 List 视口的高度
适用范围：List 每项高度由内容决定、项内有依赖父约束定尺寸的装饰元素，且条数固定、按批加载的列表
做法：
- 写成 List() { ForEach(items, (item) => { ListItem() { … } }, (item) => <稳定 key>) }，让 ListItem 按内容自然高度排列
- 在重构报告里记下这个列表不换 Repeat 的豁免原因：可变高度项、条数固定按批加载
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的调用签名（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- virtualScroll(virtualScrollOptions?: VirtualScrollOptions): RepeatAttribute<T>：Repeat 打开懒加载（按显示区域和预加载区域按需加载子组件）（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.virtualScroll）
- Repeat 懒加载模式不支持与状态管理（V1）配合使用，否则会导致渲染异常：Repeat.virtualScroll 只该出现在 @ComponentV2 组件里（出处：arkts-new-rendering-control-repeat.md，使用限制）
- 去掉 virtualScroll、改项内布局（整条竖线、Stack 加固定内边距）后首个 ListItem 仍是视口高度；改回 ForEach + ListItem 后各项按内容连续排列：返修时真机上的结果（出处：卡里修好并验证过）
针对本应用要查的：
- 列表所在组件用的是状态管理 V1 还是 V2：目标工程里这个页面或组件的 .ets 文件，struct 上的装饰器；@Component（配 @State、@Prop 等）是 V1，@ComponentV2（配 @Local、@Param 等）是 V2；V1 组件里不能用 Repeat 懒加载模式
未核实：返修时项内 Stretch/layoutWeight 与 Repeat 一并改掉，前者单独的贡献没有分离；卡里没核这个页面是 V1 还是 V2 组件，首项被撑高是否与懒加载模式不支持 V1 有关未知
来源：1 张卡，1 个应用
- case-4a7f1aef1c804d227365（记得日历）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
