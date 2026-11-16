# BottomSheetBehavior 底部面板

agent 会看到什么：读到 CoordinatorLayout 里 app:layout_behavior 指向 BottomSheetBehavior 的面板（setHideable、STATE_COLLAPSED、behavior_peekHeight，常在 BottomNavigationView 之上）；产物里面板的状态枚举和初值、bindSheet 或 Stack + translate 的写法

## 规矩

- rule-be1637d87fb5｜源 BottomSheet 面板在底栏之上时，目标用布局内 Stack+translate，不用 bindSheet｜读到：面板容器带 app:layout_behavior 指向 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；写错：展开态用挂在内容上的 .bindSheet(…, { height: SheetSize.LARGE }) 覆盖全页（含底栏），onDisappear 当作 STATE_HIDDEN 停播
- rule-7f130dc7afb0｜翻译 BottomSheetBehavior 时，可见性和 sheet 状态分开，初值和隐藏后都是 COLLAPSED｜读到：BottomSheetBehavior（或其子类）setHideable(false)、初始 STATE_COLLAPSED；宿主隐藏面板时 setVisibility(View.GONE) 并 setState(STATE_COLLAPSED)；写错：目标面板状态初值写成 Hidden，隐藏后永久停在 Hidden，或只在 Expanded 时才折叠回 Collapsed
