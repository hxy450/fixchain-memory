# CoordinatorLayout 里带 BottomSheetBehavior 的常驻面板

agent 会看到什么：读到面板容器带 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；转换决策写「bindSheet 半模态或 Stack+translateY 手势」两种并列，没写面板不覆盖底栏、收起不等于停播

## 规矩

- rule-7ab67c0612ed｜规格写底栏之上的 BottomSheet 面板时，写明不覆盖底栏、收起不停播，不把 bindSheet 列为等价｜读到：面板容器带 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；写错：转换决策写「bindSheet 半模态或 Stack+translateY 手势」两种并列，没写面板边界不覆盖底栏、收起不等于停播
