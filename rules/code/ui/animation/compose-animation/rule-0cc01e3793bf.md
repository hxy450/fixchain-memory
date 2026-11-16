# 源端有尺寸、内容切换或条目位移动画时，目标实现对应动画，不自行省略

审的是：代码
触发（任一种）：
- 读到：Surface(modifier = Modifier.animateContentSize())，或 AnimatedContent 的 transitionSpec 带 .using(SizeTransform(clip = false))；写错的样子：目标只有 TransitionEffect 滑入滑出，容器 height 在切换时跳变，没有 .animation(...) 之类的尺寸动画，也没登记缺口
- 读到：AnimatedContent(targetState = …, transitionSpec = 上下滑入滑出)；写错的样子：目标写成直切的 Text，只登记 FWD-REF 跳过
- 读到：列表项上有 Modifier.animateItem()；写错的样子：ForEach 列表项增删时没有位移动画，只当作 key 状态保持处理
适用范围：源 Compose 的尺寸、内容切换、条目位移动画迁成 ArkUI 时
做法：
- 尺寸动画：容器在内容尺寸变化时做高度过渡（.animation(AnimateParam) 或 animateTo 改尺寸状态）；内容切换：按 key 的 if/else 加 .transition(TransitionEffect.asymmetric(进入, 退出))，方向随源端条件
- 源有 animateItem 时给条目增删做位移动画（卡里修法是 spring 位移补偿）
- 做不到时登记为本流水线后续步骤可执行的明确缺口，不以「视觉细节」为由放弃
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- animation(value: AnimateParam): T：属性动画：其前面的尺寸等属性变化时过渡（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.animation）
- static asymmetric(appear: TransitionEffect, disappear: TransitionEffect): TransitionEffect<"asymmetric">：进入、退出用不同转场（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TransitionEffect.asymmetric）
- static translate(options: TranslateOptions): TransitionEffect<"translate">：上下滑入滑出用的位移转场（出处：鸿蒙 SDK 的 ets/component/common.d.ts，TransitionEffect.translate）
- 卡片加尺寸动画、步骤文本加上下滑切换、编辑页加 spring 位移补偿后与源端一致：修法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23；卡里没写尺寸动画用的是 animation 还是 animateTo
来源：1 张卡，1 个应用
- case-7d5b3583abd06943248f（Cofi）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3；取值 4 ← 诊断
