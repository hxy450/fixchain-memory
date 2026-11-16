# 底部弹层与上拉面板

源端有 BottomSheetDialog / BottomSheetDialogFragment、ModalBottomSheet、BottomSheetBehavior、SlidingUpPanelLayout，目标端有 bindSheet 和 SheetOptions，或 Stack 加 translate 写的面板时

## 触发族

- [bindSheet 的挂载点和 SheetOptions](bindsheet-options/index.md)（4 条）：读到没有关闭按钮和拖拽把手的 BottomSheetDialogFragment，或同一页弹出多个底部弹层；产物里 bindSheet 的 SheetOptions（height、showClose、dragBar、detents）和几个 bindSheet 挂在哪个组件上
- [当前页底部弹层的承载和层级](bottom-sheet-layer/index.md)（4 条）：读到在当前页 show 的底部 Dialog / BottomSheetDialog / PopupWindow，或弹层里点条目直接 startActivity；产物里面板写成 @HMRouter 路由页、插在内容列里的 if 块，以及 SheetOptions 的 mode 和 openBindSheet 的 targetId
- [BottomSheetBehavior 底部面板](bottom-sheet-behavior/index.md)（2 条）：读到 CoordinatorLayout 里 app:layout_behavior 指向 BottomSheetBehavior 的面板（setHideable、STATE_COLLAPSED、behavior_peekHeight，常在 BottomNavigationView 之上）；产物里面板的状态枚举和初值、bindSheet 或 Stack + translate 的写法
- [底部弹层的承载和关闭](bottom-sheet/index.md)（2 条）：源端 BottomSheetDialogFragment 子类弹出排序、选择面板；产物里用 bindSheet 还是页内 Stack 浮层，选中回调里有没有把显示状态置 false
- [SlidingUpPanelLayout 上拉面板](sliding-up-panel/index.md)（1 条）：读到布局 XML 里 SlidingUpPanelLayout（带 umanoPanelHeight）包着历史 RecyclerView 和下拉指示图；产物里指示图是没有 .onClick 的装饰 Image，没有展开收起的 @State、历史 List 和 ListItem 的回填点击
