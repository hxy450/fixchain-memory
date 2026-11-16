# 列表项的键和位置相关值

agent 会看到什么：读到 Compose LazyColumn 的 itemsIndexed 传 index、或无 key 的 item { }，交回的代码里 ForEach / Repeat 的键不含位置、行内用闭包 index 或常驻组件保留旧状态

## 规矩

- rule-17838b3398d4｜ForEach/Repeat 的键不含位置时，位置相关值在渲染时按 indexOf 取当前位置｜读到：Compose `itemsIndexed` 每次重组把当前 index 传给 isFirst / isLast / 序号等位置相关参数；写错：ForEach 的键是实例 id + 内容（不含位置），却在 itemGenerator 里把闭包 index（或 Repeat 的 ri.index）写进 isFirst / isLast / 序号和行形状
- rule-ec148e8e0df2｜LazyColumn 无 key 的项按位置标识，目标常驻组件要按位置相关键重建或保存后复位｜读到：LazyColumn / LazyList 里无 key 的 `item { }`（如列表尾部的新增卡），内部状态只 remember(…)，保存回调不自清；写错：目标把它放进常驻的条件 ListItem，状态只在 aboutToAppear 初始化，保存后只追加不复位，上一条输入留在卡里
