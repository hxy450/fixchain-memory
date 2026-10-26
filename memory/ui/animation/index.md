# ui/animation

动画：Compose 显隐、内容切换、容器尺寸与列表条目动画到 ArkUI animateTo、TransitionEffect 的落实，帧时钟动画改自驱帧循环时的进度计算、刷新节奏与前后台追平；View 体系 fade、startAnimation、动画辅助类与 Fragment setCustomAnimations 的显隐与切换过渡（含动画结束才切显隐的顺序）；条件块改常驻折叠容器时的节点归属，两层共享元素转场到 geometryTransition 的配对；动画矢量形变见 graphics，Activity 与 NavHost 页面转场见 navigation/hosts

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
- [sharedBounds 包住 sharedElement 的两层共享转场，每端只挂一个 geometryTransition（外层容器），不逐层各配一对](lesson-cf45ff2e03a84ab1a0a4.lesson.md)
  - 时机：界面实现与规格提取阶段，把 Compose SharedTransitionLayout 内的 sharedBounds/sharedElement 落为 ArkUI geometryTransition，确定每端挂几个配对键、挂在哪个节点时
  - 情境：源端在 SharedTransitionLayout 内用 sharedBounds("${id}-bounds") 包住带 sharedElement(id) 的内容，两层 key 不同，列表卡与同页详情浮层两端各有这两层；目标用同页条件浮层加 geometryTransition 做展开和收起，规格页面结构一节可能把源端两层 key 原样列出。
- [帧时钟动画（Animatable、ValueAnimator）改自驱 ticker 时，时间分数取“当前帧时间 − 起始时间”再套源端插值：后台停帧、回前台按真实流逝追平，不钳制单次增量](lesson-6d6ba721c81206d45fbe.lesson.md)
  - 时机：计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween)、ValueAnimator/ObjectAnimator 等由帧时钟驱动的进度改写为 setInterval、displaySync、postFrameCallback 等自驱 ticker，确定进度曲线、刷新周期与退后台、回前台的时间推进时
  - 情境：源端进度由 Compose Animatable.animateTo(tween(duration, easing)) 一类帧时钟动画驱动，或由 Android ValueAnimator/ObjectAnimator 逐帧写入绘制用的进度字段；插值曲线可能显式设置，也可能取框架默认。帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。
- [把 AnimatedVisibility 等条件块改成常驻折叠容器时，只把源 lambda 内的节点放进容器，lambda 外的兄弟留在容器外常驻](lesson-fef54f39225a043ac692.lesson.md)
  - 时机：界面实现阶段，把源端条件显隐块（AnimatedVisibility、if 块）转写为显式宽/高 0↔内容加 clip(true) 的常驻折叠容器，决定哪些兄弟节点放进容器、展开尺寸怎样确定时
  - 情境：源端同一行里既有常驻节点，又有只包住其中一部分兄弟的 AnimatedVisibility 或条件块；目标用常驻容器配显式宽/高 0↔内容、clip(true) 实现显隐，展开尺寸按容器内节点手算成常量。
