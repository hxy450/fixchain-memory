# ui/animation

动画：Compose 显隐、内容切换、容器尺寸与列表条目动画到 ArkUI animateTo、TransitionEffect 的落实，帧时钟动画改自驱帧循环时的进度计算、刷新节奏与前后台追平；动画矢量形变见 graphics，页面转场见 navigation/hosts

[上一级](../index.md)

## 本级经验

- [Compose 的显隐、内容切换、尺寸与条目位移动画（AnimatedVisibility expand/shrink、AnimatedContent + SizeTransform、animateContentSize、animateItem）逐项落为 ArkUI 动画，不以透明度渐变或直切代替](lesson-a4e6bcfb28597691c028.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Compose 显隐、内容切换、容器尺寸与列表条目的动画翻译成 ArkUI 时；规格已写“animateTo 高度过渡 / expandVertically 等价”而准备换成其他转场时
  - 情境：源端用 AnimatedVisibility(enter = expandVertically, exit = shrinkVertically)、AnimatedContent(transitionSpec … using SizeTransform)、Modifier.animateContentSize，或 LazyColumn/LazyRow 条目上的 Modifier.animateItem()；目标用 if/else 条件渲染、TransitionEffect 与 animateTo 实现；流程允许把视觉差异登记为近似或留给后续核验。
  - 例外：决策记录以编号批准省略该动画，并写明差异验收
- [View 体系的 fade/startAnimation 显隐与自写页面转场按源时长与顺序实现，不折叠成即时显隐或默认路由](lesson-76258c72cc6764d88db3.lesson.md)
  - 时机：实现与接线阶段，翻译源码中伴随动画调用的“置 VISIBLE/GONE”或“进入详情、replace fragment”时；规格提取阶段为导航与显隐验收条目登记转场契约时
  - 情境：源端在显隐处调用 fade(view, show)、startAnimation、ViewPropertyAnimator，或进入详情前调用自写转场助手（列表项缩放、覆盖层淡出）、setCustomAnimations；动画参数在 res/anim、config_*AnimTime 或代码常量中；目标用条件渲染驱动显隐、用 pushPathByName 跳转。
  - 例外：源端为 Compose 动画 API 时按 Compose 显隐与尺寸动画的对应做法处理；决策台账以决策 ID 批准省略该动画
- [把 Compose Animatable 等帧时钟动画改成自驱 ticker 时，进度按“当前帧时间 − 起始时间”计算：后台可停帧，回前台首帧按真实流逝追平，不钳制单次增量](lesson-6d6ba721c81206d45fbe.lesson.md)
  - 时机：计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween) 等由帧时钟驱动的进度改写为 setInterval、displaySync 等自驱 ticker，确定刷新周期与退后台、回前台的时间推进时
  - 情境：源端进度由 Compose Animatable.animateTo(tween(duration, LinearEasing)) 一类帧时钟动画驱动，帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。
