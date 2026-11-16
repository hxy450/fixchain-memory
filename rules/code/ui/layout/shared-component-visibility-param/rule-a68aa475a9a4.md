# 宿主 Adapter 绑定行时改写行内视图、共享行组件无对应入参时，给组件加默认原行为的入参

审的是：代码
触发（任一种）：
- 读到：宿主 Adapter 绑定行时（`onBindViewHolder` 或它前后的钩子）按条件改写行内视图，如把行内某个按钮 `setVisibility(View.GONE)`；写错的样子：目标宿主照常构造共享行组件，没传任何显隐入参，组件里那个 `Button` 在所有行都显示
适用范围：多个页面复用同一个行组件、只有某个宿主在绑定时改写行内视图的列表
做法：
- 给共享行组件加一个默认保持原行为的布尔入参（默认 true，即照常显示），宿主按源端条件传值：源端在某条件下 GONE 就在该条件下传 false
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View.GONE：不可见，也不占布局空间：源端隐藏后不留空位（出处：android.view.View#GONE）
- Visibility.None：隐藏且不参与布局、不占位；Visibility.Hidden 隐藏但占位：目标端与 View.GONE 对应的是 None，不是 Hidden（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
- 行组件加显隐入参（默认 true），宿主传「无数据或已订阅时为 true」一类的条件：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 宿主改写了哪些行内视图、在什么条件下：源工程里宿主列表 Adapter 的绑定方法及其前后钩子，按 setVisibility、setEnabled、setText 搜；逐项记下被改的视图和条件，每项在行组件上对应一个默认原行为的入参
来源：1 张卡，1 个应用
- case-07655e78d2a5ab769146（AntennaPod）：做法第 1 步 ← 建议 3、诊断；取值 3 ← 诊断
