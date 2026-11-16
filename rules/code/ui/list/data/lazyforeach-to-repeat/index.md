# LazyForEach 列表改写成 Repeat

agent 会看到什么：读到 LazyForEach(IDataSource) 渲染列表或 ListItem；产物里写成 Repeat<T>(…).each(…).virtualScroll()，或 each 里调 @Builder

## 规矩

- rule-648fd48ddd7a｜ListItem 高度随内容且项内有 layoutWeight 时用 ForEach，不换 Repeat｜读到：List 里用 LazyForEach(IDataSource) 渲染 ListItem，每项高度由内容决定（分组条数不等、可折叠），项内有 alignSelf(ItemAlign.Stretch) 的贯穿装饰、layoutWeight(1) 的竖线或内容列；写错：改写成 Repeat<T>(items).each(... ListItem ...).key(...).virtualScroll()，首个 ListItem 被撑成接近 List 视口的高度
- rule-0dfd4db82933｜Repeat 的 each 里拆出 @Builder 或子组件时，传完整 RepeatItem，不传 ri.item｜读到：源列表用 LazyForEach（或要改成 Repeat）渲染会整体切换的数据集（按日期、周、月、分页替换数组）；清单或计划写着「Builder 接完整 RepeatItem」；写错：Repeat<T>(…).each(ri => this.SomeRow(ri.item))（或 this.Section(ri.item, ri.index)），@Builder 按值接收普通对象，常带 .virtualScroll()
