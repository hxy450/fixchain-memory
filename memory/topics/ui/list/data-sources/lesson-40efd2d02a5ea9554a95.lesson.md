# LazyForEach 换数据时不重新赋值数据源对象：保持同一 IDataSource 宿主并通知重载，行键跨数据集唯一

ID：`lesson-40efd2d02a5ea9554a95` · 版本：3 · 阶段：execute/repair · 主题：[ui/list/data-sources](index.md)

概要：LazyForEach 换数据不换源对象，通知重载

信号：`LazyForEach`, `IDataSource`, `DataChangeListener`, `onDataReloaded`, `onDataAdd`, `onDataChange`, `keyGenerator`, `notifyDataSetChanged`, `setAdapter`, `swapAdapter`

## 何时使用

界面实现与返修重写阶段，为 LazyForEach 列表实现整批换数据（换适配器、排序、筛选结果）或延迟填充时

## 适用情境

源端 setAdapter/swapAdapter、排序后 notifyDataSetChanged 等整表刷新；目标 LazyForEach 绑定一个实现 IDataSource 的数据源对象，准备在换数据时写 this.dataSource = new XxxDataSource(...)。

## 例外与边界

- 列表已改用 ForEach 或 Repeat，按它们的键与更新规则处理

## 原因

LazyForEach 经数据源上注册的 DataChangeListener 获知变化；把状态字段换成另一个数据源对象，列表不会按新对象整体重载，排序或换列表后行不刷新（文档明言重新赋值 dataSource 会导致异常，dataSource 为状态变量时其改变不触发 LazyForEach 刷新；HarmonyOS 文档 arkts-rendering-control-lazyforeach，访问于 2026-10-17）。数据集切换后若行键与旧数据集重合，旧行会被复用。

## 做法

1. 数据源对象在组件生命周期内只创建一次；换数据时更新它内部的数组，或让这个稳定宿主改挂新的数据集合，再对已注册的监听调用 onDataReloaded()；单项增删改用 onDataAdd/onDataDelete/onDataChange 一类通知。
2. 源端在多个适配器之间切换时，把各适配器做成宿主内部可替换的数据集，宿主保留并转交已注册的监听。
3. keyGenerator 返回的键在不同数据集之间也唯一（如数据集标识加条目稳定 id），不使用下标。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [派工必读清单覆盖语义来源，提速要求下也保留](../../../process/handoff-loss/lesson-8598e0af342dd5c8ba28.lesson.md)（共享 1 张卡）
- [状态派生值不传 @Builder，改 @Param 子组件](../../state/binding/lesson-8d2979542fa2cd65150c.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-2f7266880e1702fcb7a2](../../../../../store/cases/case-2f7266880e1702fcb7a2/7ad07097b8635ee30e7754d0a13165768bfede48f5dd7b281caa3f66644e0eef.json) · 结论：diagnosis, rec-861162c128
  卡片版本：`7ad07097b8635ee30e7754d0a13165768bfede48f5dd7b281caa3f66644e0eef`
