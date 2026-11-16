# 列表会整表重建时，ForEach 条目闭包按唯一字段 findIndex 定位当前行，不用 indexOf(row)

审的是：代码
触发（任一种）：
- 读到：源端 ListActivity.onListItemClick(ListView, View, int position, long id) 或 onItemClick 按 position 从当前数据表取行，加载函数每次 new 一张新表；写错的样子：条目 .onClick 闭包捕获行对象 row，处理函数里用 indexOf(row) 或 ForEach 生成时的 index 到当前数组里定位，再按这个位置取行
适用范围：数据表在 onPageShow、子页返回或增删后整表重建为新对象，且 ForEach 键只由内容或 id 组成（不含实例分量）时
做法：
- 闭包里按行内唯一字段在当前数组里查：const position = this.list.findIndex(f => f.id === row.id)（list、id 换成实际的数组和唯一字段），再交给各分支
- 回调只需要行的某个字段时直接用 row 的那个字段，不到当前数组里求位置
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的条目生成函数拿到的 item、index 是生成那一刻的值（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 非首次渲染时键值已存在就不创建新组件，直接渲染该键值对应的组件：同键行不重跑条目生成，onClick 闭包里的 row 仍是旧对象（出处：arkts-rendering-control-foreach.md，非首次渲染）
- 整表换成新对象后 indexOf(row) 得 -1、list[-1] 为 undefined 而崩溃；改成 findIndex(f => f.唯一字段 === row.唯一字段) 后返回列表再点击不再闪退：按唯一字段查当前表与源端按 position 取当前表等价（出处：卡里修好并验证过）
- onListItemClick(ListView l, View v, int position, long id)：position 是被点视图在列表里的位置：源端按位置从当前数据表取行，不依赖对象身份（出处：android.app.ListActivity#onListItemClick）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的条目生成函数同样捕获生成时的 item、index（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
来源：1 张卡，1 个应用
- case-746bb8fab046be7fe43e（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
