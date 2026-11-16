# 规格转写 SwipeToDismissBox 方向时，同时写枚举、手势方向和 offset 符号

审的是：规格
触发（任一种）：
- 读到：源 `SwipeToDismissBox` 写 `enableDismissFromStartToEnd = false`，`currentValue == SwipeToDismissBoxValue.EndToStart` 才算 dismiss，背景 `horizontalAlignment = Alignment.End`；写错的样子：规格里写「EndToStart，即右滑」「右滑滑删过阈值」，或只写枚举名、没写手势方向和 offset 符号
适用范围：规格提取阶段把 Compose SwipeToDismissBox 的方向枚举写成文字描述时
做法：
- 规格里写成「仅 EndToStart：LTR 下手指从右往左滑（左滑），内容 offset 为负，背景从行尾（右侧）露出；StartToEnd 已由 enableDismissFromStartToEnd = false 关掉」
- 落笔前核对源码三处指向同一方向：enableDismissFromStartToEnd 的开关、dismiss 判定用的枚举、背景的 horizontalAlignment
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LTR 下 EndToStart 是手指从右往左、内容向负方向移动；目标按 [-行宽, 0] 实现后，设备上左滑删除与 Android 一致：EndToStart 对应左滑，不是右滑（出处：卡里修好并验证过）
- PanGesture 的 offsetX 从左向右滑动为正，反之为负，单位 vp：规格里写 offset 符号时按这个约定（出处：ts-gesture-common.md，GestureEvent对象说明）
来源：1 张卡，1 个应用
- case-fc6df865cb042aec7af1（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
