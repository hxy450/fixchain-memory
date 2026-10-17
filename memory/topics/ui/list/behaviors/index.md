# ui/list/behaviors

列表容器行为：侧栏与分组列表的滚动联动、组头默认展开、Repeat 虚拟滚动的项高度核对、swipeAction 挂载。

[上一级](../index.md)

## 本级经验

- [分类页右侧用 Scroller 列表双向联动迁滚动保护](lesson-7723af3766fb843a2577.lesson.md) · 阶段：spec/execute/repair · 信号：scrollToIndex, onScrollIndex, Scroller, LazyListState
- [改用 Repeat 虚拟化前逐列表核对项高度来源](lesson-150e48577e599f64ee23.lesson.md) · 阶段：execute/repair · 信号：virtualScroll, Repeat, LazyForEach, alignSelf(Stretch)
- [无组点击监听时组头仍默认切换展开状态](lesson-e01c6f821d631fad5383.lesson.md) · 阶段：execute/repair · 信号：ExpandableListView, BaseExpandableListAdapter, setOnGroupClickListener, expandGroup
- [滑动操作挂在 ListItem 节点而非行 Builder](lesson-feaf8a4a916a022b13a1.lesson.md) · 阶段：execute · 信号：swipeAction, ItemTouchHelper, SwipeActions, ListItem
