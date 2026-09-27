# 列表条目以新对象替换或整表重建时，ForEach 键要包含会变且需要显示的字段

ID：`lesson-2e636699fa65aefd63f0` · 版本：2

[本主题](index.md)

## 何时使用

功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时

## 适用情境

列表条目编辑（如改名）后以保留 id 的新对象替换，或操作成功后重新请求列表并整表 setList（id 不变、计数等字段变化）；ArkUI 用 ForEach 渲染，并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新。

## 例外与边界

- 更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键

## 原因

ForEach 键值不变时复用已有子组件、不再执行条目构建，子组件拿不到替换后的新对象，界面停在旧值；Compose 不设 key 的 forEach 与 RecyclerView 整表刷新每次都拿到新值，所以源端没有这个问题。来源两例：改名后反馈与持久化都已更新，卡片仍显示旧名，只含 id 的键由早期页面写入、重建时被沿用，写码者读到的状态参考只讲“替换实例会触发刷新”；另一应用里弹层列表的键只含下标、id 与类型标志，写者认为“整表重载”即会重渲染，添加成功后计数停在旧值，而它读到的陷阱清单已写明同 id 新值重建时键须含可变字段。

## 做法

1. 先定更新方式：替换对象或整表重建就把会变且显示的字段并入键，如 `${item.id}:${item.name}:${item.count}`；改为给 @Trace 字段原地赋值则可保留 id 键。
2. 写键前列出条目内所有展示字段，并查源端的刷新方式（替换对象、重新请求后 setList），不把“整表重载”当作会重渲染的依据。
3. 对每个修改动作核一遍：动作 → 数组元素是否换成新对象 → ForEach 键是否变化 → 子组件 @Param 绑定的是哪个对象，确认新值能到达条目界面；页面交付自检对每个 ForEach 都做这一核对。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-3045f4019d7d543e18ca · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`164645926053e77c27ee6b1cc2240fcb8d377e55df9d339500e1ed4989111455`
- case-b0c0f14a07fefbd87d63 · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`1a80fc062e61ff16fb2adf034e5ee3b79b06d59881ec98b101abb3cda5a867af`
