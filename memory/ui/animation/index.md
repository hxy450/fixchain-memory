# ui/animation

动画：Compose 显隐、内容切换、容器尺寸与列表条目动画到 ArkUI animateTo、TransitionEffect 的落实，帧时钟动画改自驱帧循环时的进度计算、刷新节奏与前后台追平；View 体系 fade、startAnimation、动画辅助类与 Fragment setCustomAnimations 的显隐与切换过渡（含动画结束才切显隐的顺序）；动画矢量形变见 graphics，Activity 与 NavHost 页面转场见 navigation/hosts

[上一级](../index.md)

## 本级经验

- [Compose 的显隐、内容切换、尺寸与条目位移动画（AnimatedVisibility expand/shrink、AnimatedContent + SizeTransform、animateContentSize、animateItem）逐项落为 ArkUI 动画，不以透明度渐变或直切代替](lesson-a4e6bcfb28597691c028.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose 显隐、内容切换、容器尺寸与列表条目的动画翻译成 ArkUI 时；规格已写“animateTo 高度过渡 / expandVertically 等价”而准备换成其他转场时
  - 情境：源端用 AnimatedVisibility(enter = expandVertically, exit = shrinkVertically)、AnimatedContent(transitionSpec … using SizeTransform)、Modifier.animateContentSize，或 LazyColumn/LazyRow 条目上的 Modifier.animateItem()；目标用 if/else 条件渲染、TransitionEffect 与 animateTo 实现；流程允许把视觉差异登记为近似或留给后续核验。
  - 例外：决策记录以编号批准省略该动画，并写明差异验收
- [View 动画调用（fade、startAnimation、setCustomAnimations）按行为迁移：取源动画资源与时长，动画结束才切显隐](lesson-284e67e299e71fc63095.lesson.md)
  - 时机：实现与接线阶段，为源端用 View 动画完成的行显隐、列表项进入详情、Fragment 切换等状态变化选择 ArkUI 过渡时；规格提取阶段为导航与显隐验收项登记转场契约时
  - 情境：源端在置 VISIBLE/GONE 或 replace Fragment 前后调用自有动画辅助类（淡入淡出、缩放进入详情）、View.startAnimation 或 FragmentTransaction.setCustomAnimations，动画取 res/anim 资源、config_mediumAnimTime 等平台时长或代码常量，常在动画结束回调里才切 visibility；目标用 if 条件渲染与 Navigation/NavDestination，未写 transition、animateTo 或 customTransition。
  - 例外：决策记录以编号批准省略该动画并写明差异验收
- [帧时钟动画（Animatable、ValueAnimator）改自驱 ticker 时，时间分数取“当前帧时间 − 起始时间”再套源端插值：后台停帧、回前台按真实流逝追平，不钳制单次增量](lesson-6d6ba721c81206d45fbe.lesson.md)
  - 时机：计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween)、ValueAnimator/ObjectAnimator 等由帧时钟驱动的进度改写为 setInterval、displaySync、postFrameCallback 等自驱 ticker，确定进度曲线、刷新周期与退后台、回前台的时间推进时
  - 情境：源端进度由 Compose Animatable.animateTo(tween(duration, easing)) 一类帧时钟动画驱动，或由 Android ValueAnimator/ObjectAnimator 逐帧写入绘制用的进度字段；插值曲线可能显式设置，也可能取框架默认。帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。
