# ui/layout/safe-area

Scaffold innerPadding 与状态栏避让契约

[上一级](../index.md)

## 本级经验

- [Scaffold 无 topBar 时 innerPadding.top 就是状态栏 inset：子页无 statusBarsPadding 不能推出「不做顶部避让」](lesson-6803500d0f48b0809ff1.lesson.md)
  - 时机：规格提取阶段，为壳页（Scaffold / Tab 宿主）及其子页、页内浮层写「谁避让状态栏」的沉浸式与安全区契约时
  - 情境：Android 子页自身没有 statusBarsPadding，但作为 Material3 Scaffold 的 content 经 modifier.padding(innerPadding).consumeWindowInsets(innerPadding) 嵌入（无 topBar、contentWindowInsets 默认 systemBars）；目标端父容器不为 Tab 内容区加顶部避让，而是把状态栏高度以 @Param statusBarHeight 下发。
  - 例外：Scaffold 有 topBar 或覆写了 contentWindowInsets，此时 innerPadding.top 不再等于状态栏高
- [下发 statusBarHeight 参数时禁止写「本页不使用」；浮层与同 Stack 兄弟层拿同一 inset](lesson-90838f5b7e407e7c2e44.lesson.md)
  - 时机：派工与界面实现阶段，向子页或浮层下发 statusBarHeight 参数、或把 needs_immersive_safearea=false 的浮层挂进宿主页自窗口顶起的 Stack 时
  - 情境：宿主页按沉浸式取真实 statusBarHeight 下发；子页 @Param 已接线；浮层（scrim + 居中卡片，fillMaxSize）与列表、顶栏同挂一个 Stack。
  - 例外：目标父容器已替子页加了顶部避让并有源码位置可引用
