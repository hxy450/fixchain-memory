# 列表条目以新对象替换或整表重建时，ForEach/Repeat 键要包含会变且需要显示的字段；要稳定键就改为可观察实例原位更新

ID：`lesson-2e636699fa65aefd63f0` · 版本：3

[本主题](index.md)

## 何时使用

功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时；为消除重建抖动而稳定 ForEach/Repeat 的键时

## 适用情境

列表条目编辑（如改名）后以保留 id 的新对象替换，或操作成功后重新请求列表并整表 setList（id 不变、计数等字段变化）；ArkUI 用 ForEach 渲染，并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新。也包括分页或 Swiper 的页模型是普通 interface，键原先拼入请求状态与数据导致每次加载都销毁重建（抖动），修复者准备把键缩成只含页标识。

## 例外与边界

- 更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键

## 原因

ForEach 键值不变时复用已有子组件、不再执行条目构建，子组件拿不到替换后的新对象，界面停在旧值；Compose 不设 key 的 forEach 与 RecyclerView 整表刷新每次都拿到新值，所以源端没有这个问题。来源两例：改名后反馈与持久化都已更新，卡片仍显示旧名，只含 id 的键由早期页面写入、重建时被沿用，写码者读到的状态参考只讲“替换实例会触发刷新”；另一应用里弹层列表的键只含下标、id 与类型标志，写者认为“整表重载”即会重渲染，添加成功后计数停在旧值，而它读到的陷阱清单已写明同 id 新值重建时键须含可变字段。另一应用为消除翻页抖动把键缩成只含查询键，页模型仍是普通对象、异步结果以新对象替换，已创建的页节点再也收不到数据，各视图都显示为空；改成 @ObservedV2/@Trace 并原位更新才显示，后来又被改回不可变替换而再次无数据。

## 做法

1. 先定更新方式：替换对象或整表重建就把会变且显示的字段并入键，如 `${item.id}:${item.name}:${item.count}`；改为给 @Trace 字段原地赋值则可保留 id 键。
2. 写键前列出条目内所有展示字段，并查源端的刷新方式（替换对象、重新请求后 setList），不把“整表重载”当作会重渲染的依据。
3. 对每个修改动作核一遍：动作 → 数组元素是否换成新对象 → ForEach 键是否变化 → 子组件 @Param 绑定的是哪个对象，确认新值能到达条目界面；页面交付自检对每个 ForEach 都做这一核对。
4. 为消除抖动稳定键时，同步把条目或页模型改为 @ObservedV2 类、需要显示的字段标 @Trace 并原位赋值，@Builder 与子组件 @Param 链传可观察实例或完整 RepeatItem；在测试断言或注释中写明该实例禁止整体替换。

## 来源（按需复核）

- [case-3045f4019d7d543e18ca](../../../store/cases/case-3045f4019d7d543e18ca/c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451`
- [case-69d294e4afbc31f4ab87](../../../store/cases/case-69d294e4afbc31f4ab87/482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db`
- [case-b0c0f14a07fefbd87d63](../../../store/cases/case-b0c0f14a07fefbd87d63/062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043`
