# 浮层挂在自窗口顶起的 Stack 里时，slot 契约和派工带上与兄弟层相同的 statusBarHeight

审的是：计划与派工
触发（任一种）：
- 读到：页面规格里同一 Stack 三层：列表首项、顶栏都带 statusBarHeight，浮层是 needs_immersive_safearea=false 的 modal_overlay；写错的样子：slot 契约、覆盖清单和派工词给浮层组件只传回调（如 onDismiss），没有 statusBarHeight
适用范围：派工和 slot 契约里，浮层组件挂进宿主页从窗口顶起的 Stack 的情形
做法：
- slot 契约和派工词给浮层组件加上 statusBarHeight 参数，取值和同一 Stack 的兄弟层是同一个
来源：1 张卡，1 个应用
- case-049d48a5d4b79983dde3（Jetsnack）：做法第 1 步 ← 建议 3
