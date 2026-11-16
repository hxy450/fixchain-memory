# Compose Row 里不带 weight 的 fillMaxWidth 子项后还有兄弟时，规格标「源码有、实绘无」

审的是：规格
触发（任一种）：
- 读到：Compose Row { …; Text(modifier = Modifier.fillMaxWidth()…); IconButton { … } }：不带 weight 的 fillMaxWidth() 子项后面还跟着兄弟组件；Column 里不带 weight 的 fillMaxHeight() 子项同理；写错的样子：规格的页面结构、clickable_elements 或合成的 view.xml 把这个兄弟列为可见、可点的元素，转换决策还给它写了映射（.enabled / .opacity / .fontWeight）
适用范围：规格提取阶段从纯 Compose 源码合成页面结构、clickable_elements 和分页规格时
做法：
- 对每个 Row / Column 做一次度量推演：不带 weight 的 fillMaxWidth()（Row）或 fillMaxHeight()（Column）子项先吃满剩余主轴空间，排在它后面的兄弟按 0 约束度量、不绘制
- 这类兄弟在页面结构和 clickable_elements 里标「源码有、实绘无」，不给转换决策
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Row 里不带 weight 的 fillMaxWidth 文本先度量，尾部 IconButton 只剩 0 宽约束、内容被裁掉，Android 上不绘制：声明了不等于画出来；基线 dump 里没有这个节点（出处：卡里修好并验证过）
未核实：兄弟组件的启用态（如 enabled = true 时）是否同样不渲染，卡里只用基线核了默认态，另一态按度量推演认定
来源：1 张卡，1 个应用
- case-72a54efb333474d03d1a（Jetsnack）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 1 ← 诊断
