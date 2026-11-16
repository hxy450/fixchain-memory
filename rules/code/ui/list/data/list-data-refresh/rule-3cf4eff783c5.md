# LazyForEach 要整批换数据时保持数据源对象不变，用 onDataReloaded 通知，不重新赋值

审的是：代码
触发（任一种）：
- 读到：源端用 setAdapter(...) 换一批数据（如排序后换适配器），或延迟后才填充列表数据；写错的样子：目标写 this.数据源 = 新的 IDataSource 实例，整体替换 LazyForEach(this.数据源) 的数据源，排序后行不刷新；或 keyGenerator 只按 index 生成，换数据集后键重复
适用范围：用 LazyForEach 绑定 IDataSource 的列表，需要延迟填充或整批替换数据时
做法：
- 数据源对象只建一次（稳定宿主），换数据时替换它内部的数组，再对每个已注册的 DataChangeListener 调 onDataReloaded()（或对应的 notify* 方法）
- keyGenerator 返回跨数据集唯一的行键（用条目自身的稳定标识，不用 index）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：LazyForEach 的构造：数据源、子项生成、键值生成（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
- onDataReloaded(): void：DataChangeListener 的全量重载通知：键不变的子组件复用，键变的新建（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，DataChangeListener.onDataReloaded）
- 重新赋值第一个参数 dataSource 会导致异常；dataSource 用状态变量时，状态变量改变不会触发 LazyForEach 的 UI 刷新：必须经 DataChangeListener 通知（出处：arkts-rendering-control-lazyforeach.md，使用限制）
- 默认键值 (item: Object, index: number) => { return viewId + '-' + index.toString(); }；键值必须每项唯一：不写 keyGenerator 时键只跟 index 有关，换数据后不刷新（出处：arkts-rendering-control-lazyforeach.md，键值生成规则）
未核实：卡里的行为出自 API 24（6.1.1），本机核对用 API 23 的声明
来源：1 张卡，1 个应用
- case-2f7266880e1702fcb7a2（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断
