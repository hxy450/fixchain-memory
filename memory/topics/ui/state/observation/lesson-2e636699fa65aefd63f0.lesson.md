# 列表条目以新对象替换或整表重建时，ForEach/Repeat 键要包含会变且需要显示的字段；要稳定键就改为可观察实例原位更新

ID：`lesson-2e636699fa65aefd63f0` · 版本：7 · 阶段：execute/repair · 主题：[ui/state/observation](index.md)

概要：替换对象时 ForEach 键并入显示字段；稳定键则原位更新

信号：`ForEach`, `Repeat`, `RepeatItem`, `@Param`, `@ObservedV2`, `@Trace`, `setList`, `RecyclerView`, `notifyItemChanged`, `removeAllViews`

## 何时使用

功能实现与页面接线阶段，为可编辑或会重新拉取的列表选定条目更新方式与 ForEach 键时；为消除重建抖动而稳定 ForEach/Repeat 的键时

## 适用情境

列表条目编辑（如改名）后以保留 id 的新对象替换，或操作成功后重新请求列表并整表 setList（id 不变、计数等字段变化）；ArkUI 用 ForEach 渲染，并把条目字段作为子组件的 @Param 传入；源端是 Compose 不设 key 的 forEach 加不可变 copy，或 RecyclerView 整表刷新。也包括分页或 Swiper 的页模型是普通 interface，键原先拼入请求状态与数据导致每次加载都销毁重建（抖动），修复者准备把键缩成只含页标识。也包括 RecyclerView 的 remove+add+notifyItemChanged 被迁成 arr[pos] = 新实例、splice 或整表赋值，行内显示取自条目可变字段（下载态、播放态），注释以“@Trace 字段级刷新”代替键检查。也包括源端 removeAllViews 后逐项 inflate 的结果区改成嵌套 ForEach，键只用显示内容拼接（内容可能完全相同，如多个全零数据块），条目是普通 class，每次计算整体重建。

## 例外与边界

- 更新方式是对 @ObservedV2 条目的 @Trace 字段原地赋值，子组件绑定的仍是同一对象，此时可保留只含 id 的键

## 原因

ForEach 键值不变时复用已有子组件、不再执行条目构建，子组件拿不到替换后的新对象，界面停在旧值；Compose 不设 key 的 forEach 与 RecyclerView 整表刷新每次都拿到新值，所以源端没有这个问题。来源两例：改名后反馈与持久化都已更新，卡片仍显示旧名，只含 id 的键由早期页面写入、重建时被沿用，写码者读到的状态参考只讲“替换实例会触发刷新”；另一应用里弹层列表的键只含下标、id 与类型标志，写者认为“整表重载”即会重渲染，添加成功后计数停在旧值，而它读到的陷阱清单已写明同 id 新值重建时键须含可变字段。另一应用为消除翻页抖动把键缩成只含查询键，页模型仍是普通对象、异步结果以新对象替换，已创建的页节点再也收不到数据，各视图都显示为空；改成 @ObservedV2/@Trace 并原位更新才显示，后来又被改回不可变替换而再次无数据。@Trace 只追踪同一实例上的属性写入，不能代替键变化。只由显示内容拼出的键在内容重复时互相冲突，ForEach 只渲染其中一个；整体重建时内容相同的旧行又会被复用。

## 做法

1. 先定更新方式：替换对象或整表重建就把会变且显示的字段并入键，如 `${item.id}:${item.name}:${item.count}`；改为给 @Trace 字段原地赋值则可保留 id 键。
2. 写键前列出条目内所有展示字段，并查源端的刷新方式（替换对象、重新请求后 setList），不把“整表重载”当作会重渲染的依据。
3. 对每个修改动作核一遍：动作 → 数组元素是否换成新对象 → ForEach 键是否变化 → 子组件 @Param 绑定的是哪个对象，确认新值能到达条目界面；页面交付自检对每个 ForEach 都做这一核对。
4. 为消除抖动稳定键时，同步把条目或页模型改为 @ObservedV2 类、需要显示的字段标 @Trace 并原位赋值，@Builder 与子组件 @Param 链传可观察实例或完整 RepeatItem；在测试断言或注释中写明该实例禁止整体替换。
5. 键要随新实例变化时也可追加实例分量（如按 WeakMap 记录的实例序号）：新实例得到新键而重建该行，同实例 @Trace 原地变更时键不变；接线时把数组元素替换写成新实例的同时核对该列表的键。
6. 条目内容可能重复时，键包含本次结果中的位置标识（如分组号加序号），再按需加内容字段；结果每次整体重建且条目是普通 class 时，给每次计算分配代次前缀写入键，确保旧行不被复用。

## 可选检查

- 行内状态（如下载完成后的按钮）在设备上不刷新时，检索写入新对象而键不含实例分量的列表

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 2 张卡）
- [@Monitor 监听数组路径时，生产方以新数组重新赋值](lesson-0cc7ae4eec0a59086202.lesson.md)（共享 1 张卡）
- [改用 Repeat 虚拟化前逐列表核对项高度来源](../../list/behaviors/lesson-150e48577e599f64ee23.lesson.md)（共享 1 张卡）
- [不补源端没有的元素；框架默认元素须保留](../../../process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md)（共享 1 张卡）
- [判字段是否需 @Trace 前先读其修改方法与显示界面](lesson-4d1c980bbbd20275f5c3.lesson.md)（共享 1 张卡）

来源支持：6 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-3045f4019d7d543e18ca](../../../../../store/cases/case-3045f4019d7d543e18ca/c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451.json) · 结论：diagnosis, rec-0a13d13249, rec-e7064287e1, rec-6e5bbb5c37
  卡片版本：`c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451`
- [case-5184da257133ebcc7073](../../../../../store/cases/case-5184da257133ebcc7073/fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9.json) · 结论：diagnosis, rec-3fc07ddafa
  卡片版本：`fed0f7aa28d6ee296719c0490ea8a5ff6c8212ba348c192ba1d653410ad7b9a9`
- [case-69d294e4afbc31f4ab87](../../../../../store/cases/case-69d294e4afbc31f4ab87/482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db.json) · 结论：diagnosis, rec-1628fd93fc, rec-07ba820ab1
  卡片版本：`482f975670aa8a524ba4731d49a54edcd885b84ce6161a9413dadfa75baff5db`
- [case-74bcab538b062ee7cac8](../../../../../store/cases/case-74bcab538b062ee7cac8/b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f.json) · 结论：diagnosis, rec-d60ef40a49, rec-f0ad4bbfbb
  卡片版本：`b08ad9aa1c7b953bf8cb52b98ed3769cfb39ff95071e66a7245cfb7b0e47101f`
- [case-b0c0f14a07fefbd87d63](../../../../../store/cases/case-b0c0f14a07fefbd87d63/062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043.json) · 结论：diagnosis, rec-114a6a8140, rec-f871cd0d80
  卡片版本：`062128bbb9142f6226678dcce11c36b96b76244588e2d4a2080c8a72c4036043`
- [case-c1c7d598a9076a276e6a](../../../../../store/cases/case-c1c7d598a9076a276e6a/e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824.json) · 结论：diagnosis, rec-1560c26214, rec-7ef8f070fa, rec-defd11ff75
  卡片版本：`e08fcecfcb0ba66ded65b06bfca4e2fae61130f9835525a62f6e684c11cec824`
