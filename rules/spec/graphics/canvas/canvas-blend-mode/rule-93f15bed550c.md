# Compose 同画布 drawRect(blendMode) 着色，规格映射成离屏组内 SRC_IN，不写兄弟节点混合

审的是：规格
触发（任一种）：
- 读到：Compose 源码 Modifier.drawWithContent { drawContent(); drawRect(Brush.linearGradient(…), blendMode = BlendMode.Plus / BlendMode.Darken) } 在同一画布上给已画好的图标、底盘着色；源码注释提示用「layer + srcIn」；写错的样子：规格把渐变层写成图标的独立兄弟节点 Column().blendMode(PLUS / DARKEN, BlendApplyType.OFFSCREEN) 并定为 HARD，把 SRC_IN 蒙版法只列为回退；或映射决策没引用源码里的实现提示
适用范围：规格提取时，为依赖画布已有内容的 Compose 混合绘制确定 ArkUI 映射
做法：
- 先判断混合结果是否依赖画布上已画好的兄弟内容（白底加 PLUS 饱和为白、深底加 DARKEN 取 min 都依赖）；依赖的，映射写成：参与混合的节点（字形和渐变，必要时含底盘）放进同一个 Stack().blendMode(BlendMode.SRC_OVER, BlendApplyType.OFFSCREEN) 离屏组，组内渐变 .blendMode(BlendMode.SRC_IN, BlendApplyType.OFFSCREEN)
- 源码里原作者的实现提示（如 // This should use a layer + srcIn）在映射决策里引用，写明采纳或不采纳的理由
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- blendMode(value: BlendMode, type?: BlendApplyType): T，type 默认 BlendApplyType.FAST：组件内容（含子组件）与下方画布已有内容混合（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blendMode）
- BlendApplyType.OFFSCREEN：按当前组件大小建离屏画布，组件和子组件先画到离屏画布，再按混合模式和下方画布已有内容混合：离屏组的边界就是这个组件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.blendMode、BlendApplyType.OFFSCREEN）
- BlendMode.SRC_IN = 6：r = s * da；BlendMode.SRC_OVER = 4：r = s + (1 - sa) * d：SRC_IN 只依赖目标的 alpha，渐变只留在字形范围内（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BlendMode.SRC_IN、BlendMode.SRC_OVER）
- 独立兄弟节点的 OFFSCREEN 混合目标不含兄弟节点已画的内容，PLUS 层显示成半透明淡色方块；改成同一离屏组内 SRC_IN 后效果对上：为什么不能把同画布叠加映射成兄弟节点混合（出处：卡里修好并验证过）
未核实：深色主题原来的 DARKEN 分支没截图核验；修复后深浅两态都用 SRC_IN，卡里只核了浅色
来源：1 张卡，1 个应用
- case-0e3ff99e6b2aa8afcfff（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3；取值 4 ← 诊断
