# 收到「近乎不可见、parity 保留」的元素时先分清成因，布局裁剪就用 Visibility.Hidden

审的是：代码
触发（任一种）：
- 读到：规格或派工说某元素「近乎不可见——parity 保留」，源码里它在 Row 中排在不带 weight 的 fillMaxWidth() 兄弟之后；写错的样子：目标按 .opacity(...) 降低透明度或用低对比色把它的 Text 画出来，或给前面的标题 .layoutWeight(1) 让出空间让它显示
适用范围：实现者落地规格里标为「近乎不可见」的源端元素时
做法：
- 先分辨不可见是颜色还是布局裁剪造成的；是布局裁剪就写 .visibility(Visibility.Hidden)，保留槽位、不绘制
- 在注释里写明 Android 的度量推演（哪个子项吃满主轴、这个元素得到 0 约束）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- visibility(value: Visibility): T：组件的显隐（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.visibility）
- Visibility.Hidden：隐藏但参与布局占位；Visibility.None：隐藏且不参与布局、不占位：要保留槽位用 Hidden（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Visibility）
- 改成 Visibility.Hidden 并保留原槽位后，dump 里没有该节点、槽位只有背景色，与 Android dump 一致：降低透明度去画会多出 Android 上没有的元素（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-72a54efb333474d03d1a（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
