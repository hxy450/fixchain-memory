# 会换位或增删的列表，位置相关值（首尾标记、序号、上移/下移可用态、首尾圆角）在渲染时按当前位置计算，不取 ForEach/Repeat 生成时的闭包 index

## 何时使用

界面实现阶段，把 Compose itemsIndexed 一类按当前 index 计算行参数的列表迁成 ForEach/Repeat，且列表会换位（上移、下移、拖动）、插入或删除条目时（前提：键不含位置；用默认键或自动拼 index 的不用改）

## 适用情境

源端每次重组把当前 index 传给条目（isFirst/isLast、序号、首尾行形状、移动按钮可用态）；目标 ForEach/Repeat 以实例 id 或内容为键（不含位置），在 itemGenerator 中用闭包 index 计算这些值并作为子组件的构造参数。

## 例外与边界

- ForEach 的键里本来就含位置时（没写 keyGenerator 用默认键 index + '__' + JSON.stringify(item)，或 itemGenerator 声明了 index 而 keyGenerator 没声明、框架会自动拼上 index），换位或增删会让位置变了的项重新生成，闭包 index 就是当前位置，已有写法不用按这条改。

## 原因

键不含位置时，换位或增删后同键的项被复用、不重跑生成函数，闭包 index 和由它传入的 @Param 都停在旧位置；Compose 重组总按当前 index 重算，源端没有这个问题。来源中写者已读到“同键复用旧子组件、不重派 @Param”的说明，仍认为换位后闭包会随新 index 重建；修复期改用 Repeat 的 index 后上移仍然无效，按当前位置求值后才正确。 按对象身份 indexOf 求当前位置只在数组元素保持同一实例（原位换位、splice）时成立：列表整表重建为新对象而键不变时，复用行闭包里的 item 已不在新数组中，indexOf 得 -1。

## 做法

1. 位置相关值由依赖当前数组的表达式在渲染时求出（如 this.items.indexOf(item) 与 length 比较），不把生成函数参数里的 index 固化进子组件参数或行样式。列表会整表重建为新对象时，改按唯一 id 在当前数组 findIndex(x => x.id === item.id)，不用对象身份 indexOf。

## 可选检查

- 换位、插入或删除后，核对首尾两项的上移/下移可用态与首尾圆角

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕ForEach 数据变化后某项生成的键值没变时，ForEach 不把数据更新同步给该子组件，子组件仍绑定旧的数组项，构造时传入的参数不重新计算
- 〔适用情境 / 原因〕ForEach 没有提供 keyGenerator 时，默认键值为 index + '__' + JSON.stringify(item)；itemGenerator 声明了 index 而 keyGenerator 没声明 index 时，框架在 keyGenerator 返回值后拼接 index 作为最终键值
