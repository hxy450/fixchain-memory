# ui/state/observation

共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。

[上一级](../index.md)

## 本级经验

- [@Monitor 监听数组路径时，生产方以新数组重新赋值](lesson-0cc7ae4eec0a59086202.lesson.md) · 阶段：execute · 信号：@Monitor, @Trace, StateFlow.update, .push(
- [Activity 实例字段的会话态按页面实例建服务](lesson-d9143de006714935afe2.lesson.md) · 阶段：spec/execute · 信号：getInstance, new Service()
- [共享状态 key 只用字母数字下划线，禁连字符与点号](lesson-7508ddc52eaf816887f0.lesson.md) · 阶段：spec/execute · 信号：AppStorageV2.connect, PersistenceV2, @ObservedV2, kebab-case
- [判字段是否需 @Trace 前先读其修改方法与显示界面](lesson-4d1c980bbbd20275f5c3.lesson.md) · 阶段：spec · 信号：@Trace, @ObservedV2, data class, copy(
- [拆 ViewModel 单例，跨页状态显式传递而非换 new](lesson-fc724027e2c995632733.lesson.md) · 阶段：execute/repair · 信号：getInstance(), AppStorageV2, @Param, @Monitor
- [换位列表的首尾序号按当前位置渲染时算](lesson-09a0bceae55d05616ecc.lesson.md) · 阶段：execute · 信号：itemsIndexed, ForEach, Repeat, itemGenerator
- [替换对象时 ForEach 键并入显示字段；稳定键则原位更新](lesson-2e636699fa65aefd63f0.lesson.md) · 阶段：execute/repair · 信号：ForEach, Repeat, RepeatItem, @Param
- [未保存检测用改动标志，不对 @Local 数组 ===](lesson-5d6e099ff0c8965f2b3c.lesson.md) · 阶段：execute · 信号：@Local, UIUtils.getTarget, mutableStateOf, canSafelyExit
- [直读 @Trace 字段，不复制为 @Local 快照](lesson-08c38f950b69e991607d.lesson.md) · 阶段：execute · 信号：@ObservedV2, @Trace, @Local, AppStorageV2.connect
