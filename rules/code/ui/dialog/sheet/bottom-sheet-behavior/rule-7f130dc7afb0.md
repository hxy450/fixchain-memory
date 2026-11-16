# 翻译 BottomSheetBehavior 时，可见性和 sheet 状态分开，初值和隐藏后都是 COLLAPSED

审的是：代码
触发（任一种）：
- 读到：BottomSheetBehavior（或其子类）setHideable(false)、初始 STATE_COLLAPSED；宿主隐藏面板时 setVisibility(View.GONE) 并 setState(STATE_COLLAPSED)；写错的样子：目标面板状态初值写成 Hidden，隐藏后永久停在 Hidden，或只在 Expanded 时才折叠回 Collapsed
适用范围：把 BottomSheetBehavior 管理的面板迁成 ArkUI 状态机时
做法：
- 容器可见性（VISIBLE / GONE）和 sheet 状态（COLLAPSED / EXPANDED / HIDDEN）分成两个状态存
- sheet 初值取源码或规格的 STATE_COLLAPSED；隐藏容器和 HIDDEN 回调都回到 COLLAPSED，不让 Hidden 成为没有出口的初值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 状态初值改为 Collapsed，隐藏统一回到 Collapsed：修好后的状态机（出处：卡里修好并验证过）
针对本应用要查的：
- 面板初始状态和隐藏后的回落状态：源工程里设置该 BottomSheetBehavior 的 Activity / Fragment 代码（setState、setHideable、setPeekHeight 调用）和布局 XML 里的 app:behavior_* 属性；初值取首次 setState 或 app:behavior_ 属性给的状态；隐藏分支里 setState 的参数就是回落状态
来源：1 张卡，1 个应用
- case-590e7a719e7ced6a558d（AntennaPod）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断
