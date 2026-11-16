# 条目以同 id 新对象替换时，ForEach 键要含会变且要显示的字段，不能只取 id

审的是：代码
触发（任一种）：
- 读到：源端 Compose 里 forEach { ... } 不设 key 逐项渲染，修改条目用 data class 的 copy(...) 生成新对象、map 出新列表；写错的样子：目标的修改动作用 new X(同 id, 新值) 替换数组元素，而 ForEach(arr, item => Child({ field: item.field }), item => item.id) 的键只取 id
适用范围：ArkUI 可编辑列表用 ForEach 渲染、子组件经 @Param 接条目字段，修改动作替换整条对象时
做法：
- 保留替换对象的写法时，keyGenerator 返回 id 加上会变且要显示的字段，如 (item) => `${item.id}:${item.name}`
- 或者改成对 @ObservedV2 类里带 @Trace 的字段原地赋值（不换对象），这时可以保留只取 id 的键
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的第三个参数是键生成函数（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 替换数组项后新项生成的 key 没变，ForEach 不把数据更新同步给子组件，子组件仍绑定旧对象：键不变时组件复用、条目不重建（出处：arkts-rendering-control-foreach.md，数据变化不渲染）
- 建议在键值生成函数中使用与 UI 界面相关的数据属性：键里放要显示的字段是文档推荐的做法（出处：arkts-rendering-control-foreach.md，键值生成规则）
- @ObservedV2 类里被 @Trace 装饰的属性变化时，会触发绑定它的 UI 组件刷新：原地赋值 @Trace 字段能刷新的依据（出处：arkts-new-observedV2-and-trace.md，观察变化）
- 键改为 `${item.id}:${item.name}` 后改名在卡片上显示，其他条目不变，重启后一致：返修后的写法（出处：卡里修好并验证过）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的键生成函数（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>：同族接口：Repeat 的键生成函数（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.key）
未核实：原地赋值 @Trace 字段并保留 id 键的写法卡里没有上机验证
来源：1 张卡，1 个应用
- case-3045f4019d7d543e18ca（听音练习）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
