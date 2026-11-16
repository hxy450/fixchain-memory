# 列表以同 id 新实例替换条目时，Repeat/ForEach 的键要随实例变化，不能只含 id

审的是：代码
触发（任一种）：
- 读到：安卓列表事件处理里 remove(pos) + add(pos, item) + notifyItemChanged(pos)，或整表重载后重新绑定行；写错的样子：Repeat 的 .key(...) 或 ForEach 的 keyGenerator 只含 item.id（或再加选中位、列数等页面状态），数据数组却用 arr[pos] = item、splice(pos, 1, item) 或整表赋值换入同 id 的新实例
- 写错的样子：换入新对象的地方注释写「@Trace 字段级刷新」「原位替换（notifyItemChanged 等价）」，键函数没有实例分量
适用范围：行内显示取自条目对象可变字段（下载态、播放态、已读、计数等）的 Repeat / ForEach 列表
做法：
- 凡以同 id 新实例替换或整表重载，键末尾追加按对象实例发的序号（用 WeakMap<object, number>，首次见到的对象分配新号），新实例→新键→重建该行；同一实例上改 @Trace 字段时键不变
- 不换实例的做法：约定只在原实例上改 @Trace 字段，并把这条约定写在键函数旁供后续切片沿用
- @Trace 只追踪同一实例上的属性写入，不能代替键变化；不用「@Trace 字段级刷新」注释代替对键的核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>：Repeat 的键函数（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.key）
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的第三个参数是键函数（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 替换数组项后新项生成的 key 没变，ForEach 不把数据更新同步给子组件，组件仍绑定旧对象：同 id 新实例替换而键不变时行不刷新的原因（出处：arkts-rendering-control-foreach.md，数据变化不渲染）
- Repeat 根据键值是否发生变化判断数据项是否更新：Repeat 同样按键判断，键不变就当作同一项（出处：arkts-new-rendering-control-repeat.md，键值生成规则）
- @ObservedV2 类里 @Trace 属性的值变化时，刷新绑定该属性的组件：观察的是这个对象上的属性写入，换成另一个对象不在其内（出处：arkts-new-observedV2-and-trace.md，观察变化）
- 键追加实例序号后，下载完成时换入的新实例使该行重建，行按钮由下载变为播放：修好后的行为（出处：卡里修好并验证过）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的键函数（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
来源：1 张卡，1 个应用
- case-c1c7d598a9076a276e6a（AntennaPod）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 6 ← 诊断
