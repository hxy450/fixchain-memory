# ui/dialog/content

弹窗内容与行为的还原：按源布局逐控件重建、复用共享弹窗组件、打开触发点、展开后加载数据、下拉关闭的手势门禁。

[上一级](../index.md)

## 本级经验

- [ComponentContent 后赋的回调以闭包传入](lesson-1c27b6c7cf05c05733d9.lesson.md) · 阶段：execute/repair · 信号：ComponentContent, wrapBuilder, openCustomDialog, @Param
- [含列表的 bindSheet 按手势起点决定下拉关闭](lesson-f35f4912277e0c9a1b14.lesson.md) · 阶段：execute · 信号：onWillDismiss, onWillSpringBackWhenDismiss, nestedScroll, SELF_FIRST
- [弹窗展开后才加载数据：先开弹层再内部异步加载带重试](lesson-5f8833721d3c4a11c60a.lesson.md) · 阶段：execute/repair · 信号：onExpanded, bindSheet
- [源弹窗按布局或库模板逐控件还原不用通用弹窗](lesson-1f366fe4ccdc917ce0fc.lesson.md) · 阶段：spec/execute · 信号：DialogXxxBinding.inflate, R.layout, android:hint, setContentView
- [源端委托共享弹窗时复用目标共享组件不留副本](lesson-6d3ac9a5c0382377b91e.lesson.md) · 阶段：execute/verify · 信号：XxxDialog.show, onAction, Dialog.show, DialogFragment
- [长按菜单按 onCreateContextMenu 移植](lesson-9975dd1d15f5c73758e8.lesson.md) · 阶段：execute · 信号：registerForContextMenu, onCreateContextMenu, multi_select, android:visible
- [页内对话框可见性状态逐一接通打开触发点](lesson-f0d5a447e645bc253019.lesson.md) · 阶段：execute · 信号：Modifier.clickable, @Local, @Builder, onClick
