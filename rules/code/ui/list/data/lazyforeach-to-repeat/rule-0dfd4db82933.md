# Repeat 的 each 里拆出 @Builder 或子组件时，传完整 RepeatItem，不传 ri.item

审的是：代码
触发（任一种）：
- 读到：源列表用 LazyForEach（或要改成 Repeat）渲染会整体切换的数据集（按日期、周、月、分页替换数组）；清单或计划写着「Builder 接完整 RepeatItem」；写错的样子：Repeat<T>(…).each(ri => this.SomeRow(ri.item))（或 this.Section(ri.item, ri.index)），@Builder 按值接收普通对象，常带 .virtualScroll()
适用范围：ArkUI 列表用 Repeat（尤其 virtualScroll）渲染、条目经 @Builder 或子组件渲染时
做法：
- each 回调写成 .each((ri: RepeatItem<T>) => { this.SomeRow(ri) })，@Builder 参数声明为 RepeatItem<T>，在内部读 ri.item / ri.index
- 列表很短、不需要懒加载时，可改用 ForEach 并在注释里写明理由（短列表豁免）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- each(itemGenerator: (repeatItem: RepeatItem<T>) => void): RepeatAttribute<T>：each 回调拿到的是 RepeatItem，item 是其中的数据（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.each）
- 只传 RepeatItem.item 或 RepeatItem.index 时参数值的改变不会引起 @Builder 内 UI 刷新；要将 RepeatItem 整体传参：按值传入 @Builder 的旧对象不随复用节点更新（出处：arkts-new-rendering-control-repeat.md，与@Builder混用时状态变量未刷新）
- template(type: string, itemBuilder: RepeatItemBuilder<T>, templateOptions?: TemplateOptions): RepeatAttribute<T>：同族接口：template 的 itemBuilder 同样接 RepeatItem，拆 Builder 时同样整体传（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.template）
- Repeat + virtualScroll + 按值传 item 时，非空→非空切换后保留旧条目并追加新条目；改为 ForEach + 传 item 后刷新正常：上机看到的现象和修好的写法（出处：卡里修好并验证过）
未核实：保留 virtualScroll、改传完整 RepeatItem 能否消除旧条目，卡里没上机验证；上机验证过的是改成 ForEach
来源：1 张卡，1 个应用
- case-69d294e4afbc31f4ab87（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
