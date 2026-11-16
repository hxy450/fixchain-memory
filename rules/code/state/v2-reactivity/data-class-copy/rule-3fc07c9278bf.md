# 列表行按多个可变字段渲染时，ForEach key 拼入全部会被改写的展示字段

审的是：代码
触发（任一种）：
- 读到：源端列表行组件按多个可变字段分支渲染（隐藏、锁定、置顶、删除、移除、封禁、已读、计数），列表回调用 copy(...) 改这些字段；写错的样子：ForEach / LazyForEach 的 keyGenerator 只拼 id 和部分字段（投票、收藏、已读等），漏掉行内会被后续操作改写的展示字段
适用范围：元素不是 @ObservedV2 / @Trace 行模型、靠 key 变化重建行的 ForEach / LazyForEach 列表
做法：
- 写 key 前列出该行组件实际渲染、且会被后续操作改写的全部字段，keyGenerator 里拼上身份 id 和这些字段；或改用 @ObservedV2 + @Trace 行模型
- 后续接线新增隐藏、锁定、置顶等动作时，同步把新改写的字段拼进 key
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的第三个参数生成键值（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 数组项变更但键值未变时，ForEach 不把数据同步给子组件，组件仍绑定旧数组项：key 不含被改的字段时行不重建（出处：arkts-rendering-control-foreach.md，数据变化不渲染）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的键值生成（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>：同族接口：Repeat 的键值生成（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.key）
来源：1 张卡，1 个应用
- case-ef3f002672e7158de02c（jerboa）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
