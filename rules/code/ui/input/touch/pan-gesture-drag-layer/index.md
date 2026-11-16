# 绑了 PanGesture 的拖拽层（下拉关弹层、侧滑露按钮）

agent 会看到什么：读到旧代码里弹层或列表行用 PanGesture / parallelGesture 跟手拖动（在顶部才下拉关闭、横滑露出操作按钮），产物里是改成 bindSheet 后丢了顶部门禁，或给带收起手势的内容层设 HitTestMode.None

## 规矩

- rule-6218fe14fd94｜带列表的弹窗改成 bindSheet 时，顶部下拉门禁映射到 nestedScroll 和 onWillDismiss｜读到：旧弹窗的 PanGesture 在 onActionStart 记下列表是否在顶部（currentOffset().yOffset <= 0），在顶部才跟手下拉、过阈值才关、否则 animateTo 回弹；或参考模板没有滚动列表、onWillDismiss 无条件 action.dismiss()；写错：新 SheetOptions 照搬无条件 onWillDismiss: (action) => action.dismiss()，删掉 PanGesture 和顶部判断，内部 List 没写 .nestedScroll，也没注册 onWillSpringBackWhenDismiss
- rule-eea6df4edce9｜修侧滑行按钮被内容层拦截时只改按钮热区，不把带收起手势的内容层设成 HitTestMode.None｜读到：修复单要求展开后点操作按钮只触发按钮自身动作；页面代码里 Stack 下层是操作按钮，上层内容卡片靠 translate 平移露出按钮，并同时绑了 .onClick(未展开进详情、已展开收起) 和 .parallelGesture(PanGesture({ direction: PanDirection.Horizontal })).onActionEnd(...)；写错：内容卡片上加了 .hitTestBehavior(展开 ? HitTestMode.None : HitTestMode.Block)，展开后整张卡片连同它上面的横滑和点击收起一起失去命中，右滑关不上
