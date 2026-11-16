# Compose SwipeToDismissBox 的列表行滑删

agent 会看到什么：读到源端 SwipeToDismissBox / rememberSwipeToDismissBoxState（滑动方向、positionalThreshold、backgroundContent）；产物里 List 行用 PanGesture 加 translate 手写的滑删、阈值和背景层

## 规矩

- rule-2f1cb56db545｜源端只允许 EndToStart 时，滑删 offset 截在 [-行宽, 0]，落定到 -行宽｜读到：源端 `enableDismissFromStartToEnd = false`，`currentValue == SwipeToDismissBoxValue.EndToStart` 才算 dismiss；写错：`PanGesture` 里写 `Math.max(0, Math.min(event.offsetX, rowWidth))` 把 offset 截成正数，落定 `offsetX = rowWidth`，阈值按正 offset 判断
- rule-da017eccbe58｜源用 SwipeToDismissBox 默认阈值时，按依赖版本查默认值实现，不写 50% 近似｜读到：rememberSwipeToDismissBoxState(confirmValueChange = …) 没传 positionalThreshold，SwipeToDismissBox 用默认阈值；写错：代码里写死一个比例阈值（如 0.5、注释「positionalThreshold 默认 50% 近似」），没有速度阈值，也没有登记待核
- rule-c33d5046af0b｜List 行自定义滑删的背景不放成 Stack 的 100% 子节点，改用 .background｜读到：源 `SwipeToDismissBox` 的 `backgroundContent` 用 `fillMaxWidth().fillMaxHeight()` 铺满行，行高由内容决定；写错：目标 List 行里 `Stack` 的一个子节点 `.width('100%').height('100%')` 作背景层，而 `Stack` 高度是 'auto' 或没定高
