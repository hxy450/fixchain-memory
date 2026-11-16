# 规格写底栏之上的 BottomSheet 面板时，写明不覆盖底栏、收起不停播，不把 bindSheet 列为等价

审的是：规格
触发（任一种）：
- 读到：面板容器带 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；写错的样子：转换决策写「bindSheet 半模态或 Stack+translateY 手势」两种并列，没写面板边界不覆盖底栏、收起不等于停播
适用范围：规格提取阶段写嵌在布局里的 BottomSheet 面板时
做法：
- 规格写明面板边界止于底栏之上、收起不等于停播；转换决策只列布局内 Stack+translate，不把 bindSheet 列为等价选项
来源：1 张卡，1 个应用
- case-590e7a719e7ced6a558d（AntennaPod）：做法第 1 步 ← 建议 3
