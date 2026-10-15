# 会换位或增删的列表，位置相关值按当前位置计算：ForEach 不取闭包 index，Repeat 在构建表达式里直接读 ri.index

ID：`lesson-09a0bceae55d05616ecc` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose itemsIndexed 一类按当前 index 计算行参数的列表迁成 ForEach/Repeat，且列表会换位（上移、下移、拖动）、插入或删除条目时

## 适用情境

源端每次重组把当前 index 传给条目（isFirst/isLast、序号、首尾行形状、移动按钮可用态）；目标 ForEach/Repeat 以实例 id 或内容为键（不含位置），在 itemGenerator 中用闭包 index 计算这些值并作为子组件的构造参数，或改用 Repeat 后以 RepeatItem.index 传值。

## 例外与边界

- 键本身随位置变化（如以位置拼键），换位即重建、生成函数随之重跑时，不需要另算位置
- 条目显示的内容（不是位置）在对象替换后不刷新：按列表键与对象替换的规则处理

## 原因

ForEach 键不含位置时，换位或增删后同键的项被复用、不重跑生成函数，闭包 index 和由它传入的 @Param 都停在旧位置。Repeat 换位时会更新 RepeatItem.index（SDK previewer 内嵌 stateMgmt 的 RepeatItem.updateIndex）：@ComponentV2 下它是可观察字段，构建中直接读取就会刷新；@Component(V1) 下 index 没有渲染依赖时不更新，只在事件回调里读或先存成局部常量都会停在旧值。Compose 重组总按当前 index 重算，源端没有这个问题。

## 做法

1. ForEach：位置相关值放在属性表达式或子组件 @Param 实参里，按稳定 id 求当前位置（如 this.items.findIndex(x => x.id === item.id)）再与 length 比较，不把生成函数参数里的 index 固化进子组件参数或行样式；数组元素会被替换或有重复值时不用 indexOf(item)。
2. Repeat：在 build 表达式里直接读 ri.index（向子组件传完整 RepeatItem，或在属性链里读），不先存成局部常量、不只在事件回调里读；V1 组件的事件回调需要位置时，按当前数组求位置。按此读取后换位仍过期时，改按稳定 id 求当前位置（同上一步）。

## 可选检查

- 换位、插入或删除后，核对首尾两项的上移/下移可用态与首尾圆角

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-36f0b5f441f81e98f6c6](../../../store/cases/case-36f0b5f441f81e98f6c6/6e2b86cc0863dd4232f59587c36db65173759de237ec7ebf70bc99eac7b8cc1f.json) · 结论：diagnosis, recommendation:3
  卡片版本：`6e2b86cc0863dd4232f59587c36db65173759de237ec7ebf70bc99eac7b8cc1f`
