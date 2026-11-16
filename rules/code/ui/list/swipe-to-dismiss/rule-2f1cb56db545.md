# 源端只允许 EndToStart 时，滑删 offset 截在 [-行宽, 0]，落定到 -行宽

审的是：代码
触发（任一种）：
- 读到：源端 `enableDismissFromStartToEnd = false`，`currentValue == SwipeToDismissBoxValue.EndToStart` 才算 dismiss；写错的样子：`PanGesture` 里写 `Math.max(0, Math.min(event.offsetX, rowWidth))` 把 offset 截成正数，落定 `offsetX = rowWidth`，阈值按正 offset 判断
适用范围：用 PanGesture 自定义滑删、还原源端单向 SwipeToDismissBox 时（LTR）
做法：
- onActionUpdate 里 offsetX = Math.min(0, Math.max(event.offsetX, -行宽))，正向拖动截到 0
- onActionEnd 里按 -offsetX >= 阈值 判断：过阈值时 offsetX = -行宽 并删除，否则回到 0
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- GestureEvent.offsetX：相对手指按下时的偏移，单位 vp，从左向右滑动为正，反之为负：左滑（EndToStart）得到负的 offsetX（出处：ts-gesture-common.md，GestureEvent对象说明；鸿蒙 SDK 的 ets/component/gesture.d.ts，GestureEvent.offsetX）
- clamp 改成 [-rowWidth, 0]、阈值按 -offset、落定 -rowWidth 后，设备上左滑删除与 Android 一致，右滑没有反应：改法已上机验证（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-fc6df865cb042aec7af1（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
