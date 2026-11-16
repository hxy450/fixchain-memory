# List 行自定义滑删的背景不放成 Stack 的 100% 子节点，改用 .background

审的是：代码
触发（任一种）：
- 读到：源 `SwipeToDismissBox` 的 `backgroundContent` 用 `fillMaxWidth().fillMaxHeight()` 铺满行，行高由内容决定；写错的样子：目标 List 行里 `Stack` 的一个子节点 `.width('100%').height('100%')` 作背景层，而 `Stack` 高度是 'auto' 或没定高
适用范围：在 ArkUI List 行里用 Stack + PanGesture 自定义滑删、行高由内容决定时
做法：
- 背景层从 Stack 子节点里拿掉，画在行容器上：Stack() { 行内容.translate({ x: offsetX }) }.background(this.swipeBackground)，swipeBackground 是 @Builder
- 要用 width/height('100%') 子层占满前，先看它的父级有没有确定高度；没有就不用 100% 子层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- background(content: CustomBuilder | ResourceColor, options?: BackgroundOptions): T：给组件加自定义背景，背景画在组件自身上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.background）
- 自定义背景渲染存在一定延迟，不能响应事件：背景里只放视觉内容，删除的点击或拖动不能挂在背景上（出处：ts-universal-attributes-background.md，background）
- Stack 里的 100% 背景子层让 ListItem 和背景 Row 都被撑到整屏高（只剩首行可见）；改成行容器的 .background(builder) 后行高恢复：100% 子节点会向上解析到有确定尺寸的祖先（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-fc6df865cb042aec7af1（Jetsnack）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 3 ← 诊断
