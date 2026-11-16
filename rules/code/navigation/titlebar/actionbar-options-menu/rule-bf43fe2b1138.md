# ForEach 渲染动作项或菜单项时，键要含项身份，不用下标加分类属性

审的是：代码
触发（任一种）：
- 读到：源端菜单项 MenuItem 有 itemId 或标题资源 id，按 showAsAction 和屏幕宽度决定哪些显示在上栏；写错的样子：ForEach 的 keyGenerator 用下标加分类属性拼键（如 `${index}_${item.showAsAction}_…`），不含项身份
适用范围：目标用 ForEach 渲染动作项、菜单项，尤其是显示子集会随宽度、方向变化时
做法：
- ForEach(items, itemGenerator, (item) => 项身份的字符串)：键取命令 id 或标题资源 id，不拼 index 和分类属性
- 改动让列表子集变得可变时（如上栏数随屏宽变），同时回头核对这个列表的键
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的第三个参数生成键（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 不定义 keyGenerator 时默认键是 index + '__' + JSON.stringify(item)：默认键也带下标（出处：arkts-rendering-control-foreach.md，键值生成规则）
- 不建议省略 keyGenerator，也不建议在键值中使用数据项索引 index：下标做键时插入或子集变化会复用错位的组件（出处：arkts-rendering-control-foreach.md，渲染性能降低）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的键生成同样适用（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- 键改成项身份后，上栏子集随宽度变化时不再显示错位的图标：卡里修好的结果（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-db3da49c14f06085f3b8（Sokoban）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 5；取值 5 ← 诊断
