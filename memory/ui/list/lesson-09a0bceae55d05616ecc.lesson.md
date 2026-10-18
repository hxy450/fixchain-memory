# 会换位或增删的列表，位置相关值（首尾标记、序号、上移/下移可用态、首尾圆角）在渲染时按当前位置计算，不取 ForEach/Repeat 生成时的闭包 index

ID：`lesson-09a0bceae55d05616ecc` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose itemsIndexed 一类按当前 index 计算行参数的列表迁成 ForEach/Repeat，且列表会换位（上移、下移、拖动）、插入或删除条目时

## 适用情境

源端每次重组把当前 index 传给条目（isFirst/isLast、序号、首尾行形状、移动按钮可用态）；目标 ForEach/Repeat 以实例 id 或内容为键（不含位置），在 itemGenerator 中用闭包 index 计算这些值并作为子组件的构造参数。

## 原因

键不含位置时，换位或增删后同键的项被复用、不重跑生成函数，闭包 index 和由它传入的 @Param 都停在旧位置；Compose 重组总按当前 index 重算，源端没有这个问题。来源中写者已读到“同键复用旧子组件、不重派 @Param”的说明，仍认为换位后闭包会随新 index 重建；修复期改用 Repeat 的 index 后上移仍然无效，按当前位置求值后才正确。 按对象身份 indexOf 求当前位置只在数组元素保持同一实例（原位换位、splice）时成立：列表整表重建为新对象而键不变时，复用行闭包里的 item 已不在新数组中，indexOf 得 -1。

## 做法

1. 位置相关值由依赖当前数组的表达式在渲染时求出（如 this.items.indexOf(item) 与 length 比较），不把生成函数参数里的 index 固化进子组件参数或行样式。列表会整表重建为新对象时，改按唯一 id 在当前数组 findIndex(x => x.id === item.id)，不用对象身份 indexOf。

## 可选检查

- 换位、插入或删除后，核对首尾两项的上移/下移可用态与首尾圆角

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-36f0b5f441f81e98f6c6](../../../store/cases/case-36f0b5f441f81e98f6c6/6e2b86cc0863dd4232f59587c36db65173759de237ec7ebf70bc99eac7b8cc1f.json) · 结论：diagnosis, recommendation:3
  卡片版本：`6e2b86cc0863dd4232f59587c36db65173759de237ec7ebf70bc99eac7b8cc1f`
- [case-746bb8fab046be7fe43e](../../../store/cases/case-746bb8fab046be7fe43e/ed7f4051e6d4742dbfd6f6dcd6a8047e202656c3a05d028ba230fc3217dffea4.json) · 结论：recommendation:5
  卡片版本：`ed7f4051e6d4742dbfd6f6dcd6a8047e202656c3a05d028ba230fc3217dffea4`
