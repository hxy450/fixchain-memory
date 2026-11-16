# 源 BottomSheet 面板在底栏之上时，目标用布局内 Stack+translate，不用 bindSheet

审的是：代码
触发（任一种）：
- 读到：面板容器带 app:layout_behavior 指向 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；写错的样子：展开态用挂在内容上的 .bindSheet(…, { height: SheetSize.LARGE }) 覆盖全页（含底栏），onDisappear 当作 STATE_HIDDEN 停播
适用范围：源端 BottomSheet 面板嵌在页面布局里、不覆盖底部导航时
做法：
- 面板放在内容区的 Stack 里，peek、展开、收起三态用 .translate({ y: … }) 切换，配手势（如 SwipeGesture）；面板边界止于底栏之上
- 收起不等于停播；返回键先收起面板
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：给组件绑定半模态页面，是独立的模态层，不是布局内的面板（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet；ts-universal-attributes-sheet-transition.md，bindSheet）
- SheetSize.LARGE = 1：高度接近屏幕高：LARGE 会盖住底栏（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetSize.LARGE）
- translate(value: TranslateOptions): T：面板三态的位移（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.translate）
- 布局内 sheet：translate 三态、peek 高度实测、SwipeGesture；返回键先收起面板：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- peek 高度：源布局 XML 里面板容器的 app:behavior_peekHeight，或代码里的 setPeekHeight 调用；dp 数值照搬为 vp，作为收起态露出的高度
来源：1 张卡，1 个应用
- case-590e7a719e7ced6a558d（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 诊断、建议 3；取值 4 ← 诊断
