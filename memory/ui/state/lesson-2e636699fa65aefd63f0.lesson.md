# 列表条目以同键新对象替换或整表重建时，按渲染器确定新值怎样到达条目：键并入可变字段，或改为可观察实例原位更新

ID：`lesson-2e636699fa65aefd63f0` · 版本：7

[本主题](index.md)

## 何时使用

功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时；为消除重建抖动而稳定 ForEach/Repeat 的键时

## 适用情境

列表条目编辑后以保留 id 的新对象替换（copy、arr[pos] = 新实例、splice），或操作成功后重新请求并整表赋值（id 不变、计数等字段变化）；目标用 ForEach 或 Repeat 渲染，键只含 id 等不变字段，条目字段作为子组件 @Param 传入。源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新、remove+add+notifyItemChanged。也包括为消除重建抖动把键缩成只含页标识而页模型仍是普通对象，以及只由显示内容拼出的键（内容可能完全相同）。

## 例外与边界

- 更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键
- Repeat 开了 virtualScroll：同键新对象会经 updateItem 送进 RepeatItem，builder 直接读 ri.item 即可，保持稳定键

## 原因

ForEach 键值不变时复用已有子组件、不再执行条目构建，子组件拿不到替换后的新对象，界面停在旧值；未开 virtualScroll 的 Repeat 对保留的键只更新 index，RepeatItem.item 仍指向旧对象。@Trace 只追踪同一实例上的属性写入，不能代替键变化。反过来，改键会销毁并重建该行，行内的输入焦点、编辑中文本和动画状态随之丢失。只由显示内容拼出的键在内容重复时互相冲突，ForEach 只渲染其中一个。Compose 不设 key 的 forEach 与 RecyclerView 整表刷新每次都拿到新值，所以源端没有这个问题。

## 做法

1. 先按渲染器判断：ForEach 与未开 virtualScroll 的 Repeat，同键新对象不会到达条目；开了 virtualScroll 的 Repeat 会对同键新对象 updateItem，builder 直接读 ri.item、保持稳定键。
2. 再看行内状态：条目内有输入焦点、编辑中文本或动画时，改为 @ObservedV2 条目、显示字段标 @Trace 并原位赋值，保留只含 id 的键；只有源端本就整行重建（替换对象、重新请求后 setList）且行内没有这类状态时，才把会变且显示的字段并入键，如 `${item.id}:${item.name}:${item.count}`。
3. 写键前列出条目内所有展示字段，并查源端的刷新方式，不把“整表重载”当作会重渲染的依据。
4. 对每个修改动作核一遍：动作 → 数组元素是否换成新对象 → 键是否变化 → 子组件 @Param 绑定的是哪个对象，确认新值能到达条目界面；页面交付自检对每个列表都做这一核对。
5. 为消除抖动稳定键时，同步把条目或页模型改为 @ObservedV2 类、需要显示的字段标 @Trace 并原位赋值，@Builder 与子组件 @Param 链传可观察实例或完整 RepeatItem；在测试断言或注释中写明该实例禁止整体替换。
6. 键要随新实例变化时也可追加实例分量（如按 WeakMap 记录的实例序号）：新实例得到新键而重建该行，同实例 @Trace 原地变更时键不变。
7. 条目内容可能重复时，键包含本次结果中的位置标识（如分组号加序号），再按需加内容字段；结果每次整体重建且条目是普通 class 时，给每次计算分配代次前缀写入键，确保旧行不被复用。

## 可选检查

- 行内状态（如下载完成后的按钮）在设备上不刷新时，检索写入新对象而键不含实例分量的列表

来源支持：6 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-3045f4019d7d543e18ca](../../../store/cases/case-3045f4019d7d543e18ca/c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451`
- [case-5184da257133ebcc7073](../../../store/cases/case-5184da257133ebcc7073/fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9.json) · 结论：diagnosis, recommendation:2
  卡片版本：`fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9`
- [case-69d294e4afbc31f4ab87](../../../store/cases/case-69d294e4afbc31f4ab87/482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db`
- [case-74bcab538b062ee7cac8](../../../store/cases/case-74bcab538b062ee7cac8/b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f`
- [case-b0c0f14a07fefbd87d63](../../../store/cases/case-b0c0f14a07fefbd87d63/062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043`
- [case-c1c7d598a9076a276e6a](../../../store/cases/case-c1c7d598a9076a276e6a/e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824`
