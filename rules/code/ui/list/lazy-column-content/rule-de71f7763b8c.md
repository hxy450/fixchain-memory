# 安卓列表按父项分组成卡片、卡内列子项行时，目标按父项 ForEach 出卡片，不把子项拍平

审的是：代码
触发（任一种）：
- 读到：安卓 Compose Screen 的 `LazyColumn` 里每个 item 是一张按父项（如商品）分组的卡片，卡内再列子项（如规格）行；目标数据模型已按父项聚合子项数组；写错的样子：目标页面用嵌套 `ForEach` 把每个子项渲染成独立行，并在每行重复父项标题，没有父项卡片这一层
适用范围：按「对比安卓还原」实现列表页面，安卓端列表项有父子两层时
做法：
- 外层 ForEach 遍历父项，每个父项出一个卡片 @Builder（标题、主图只出一次），卡内用内层 ForEach 遍历它的子项数组出子项行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的调用签名，外层遍历父项、内层遍历子项数组（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 新增按父项分组的卡片，卡内列子项行，替换原来每个子项一行的写法后通过：修复后的列表层级（出处：卡里修好并验证过）
针对本应用要查的：
- 安卓列表项的分组层级：源工程里对应页面的 Compose Screen（.kt）中 LazyColumn 的 items 块和它调用的卡片 Composable；items 遍历的是哪一层对象、卡片里是否再遍历子项，照这个层级写目标的外层和内层 ForEach
来源：1 张卡，1 个应用
- case-38718a95ad1839df7084（青商城）：做法第 1 步 ← 诊断、建议 1；取值 2 ← 诊断
