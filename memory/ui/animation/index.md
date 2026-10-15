# ui/animation

动画：Compose 显隐、内容切换、容器尺寸与列表条目动画到 ArkUI animateTo、TransitionEffect 的落实，帧时钟动画改自驱帧循环时的进度计算、刷新节奏与前后台追平；动画矢量形变见 graphics，页面转场见 navigation/hosts

[上一级](../index.md)

## 本级经验

- [Compose AnimatedVisibility 的 expand/shrink 落为 ArkUI 容器高度过渡，不以淡入或直切代替](lesson-a4e6bcfb28597691c028.lesson.md)
  - 时机：规格提取与界面实现阶段，把 AnimatedVisibility(expandVertically/shrinkVertically 等) 翻译成 ArkUI 时；规格已写“animateTo 高度过渡 / expandVertically 等价”而准备换成其他转场时
  - 情境：源端用 AnimatedVisibility(enter = expandVertically/expandIn…, exit = shrinkVertically/shrinkOut…) 展开、收起内联内容；目标用 if/else 条件渲染、TransitionEffect 与 animateTo 实现；流程允许把视觉差异登记为近似或留给后续核验。
- [Compose animateContentSize 与 AnimatedContent+SizeTransform：尺寸变化放进 animateTo 过渡](lesson-98a6ded89db8f578fd83.lesson.md)
  - 时机：规格提取与界面实现阶段，把 Modifier.animateContentSize 或 AnimatedContent（含 transitionSpec 与 SizeTransform）翻译成 ArkUI 时
  - 情境：源端容器挂 Modifier.animateContentSize，或用 AnimatedContent(targetState) 配 transitionSpec（如上下滑入滑出）与 using SizeTransform 切换内容；目标用 if/else 或键化 ForEach 承载内容，准备直切或只保留滑入滑出。
- [惰性列表条目带 Modifier.animateItem() 时，ArkUI 侧把数据增删放进 animateTo 并给 ListItem 挂转场](lesson-e3401517f6ed9a9a85ee.lesson.md)
  - 时机：界面实现阶段，把带 Modifier.animateItem() 的惰性列表条目翻译成 ArkUI List，或实现条目移除（关闭提示卡、删除项）时
  - 情境：源端 LazyColumn/LazyRow 条目挂 Modifier.animateItem()，条目出现、消失与位置变化都有动画（Compose foundation 1.11.1 源码 LazyItemScope 中 fadeInSpec、placementSpec、fadeOutSpec 均有默认值）；目标用 List + ForEach/LazyForEach；部分移除由持久化写入后经数据流回推触发。
- [把 Compose Animatable 等帧时钟动画改成自驱 ticker 时，进度按“当前帧时间 − 起始时间”计算：后台可停帧，回前台首帧按真实流逝追平，不钳制单次增量](lesson-6d6ba721c81206d45fbe.lesson.md)
  - 时机：计时或动画引擎的规格与实现阶段，把 Animatable.animateTo(tween) 等由帧时钟驱动的进度改写为 setInterval、displaySync 等自驱 ticker，确定刷新周期与退后台、回前台的时间推进时
  - 情境：源端进度由 Compose Animatable.animateTo(tween(duration, LinearEasing)) 一类帧时钟动画驱动，帧时钟随宿主 ON_STOP 暂停；目标没有可直接复用的同语义帧时钟，自写 ticker 复刻进度推进与前后台切换。同一应用可能另有后台 Worker 以固定周期（如 tickerFlow + elapsedRealtime）推进，其周期与补偿方式不属于前台动画。
