# Swiper 禁止滑动和容器的触摸拦截

agent 会看到什么：读到 ViewPager2 的 isUserInputEnabled = false、只有一页或拦截触摸；产物里 Swiper、Tabs、Stack 上的 .enabled(false)、disableSwipe、hitTestBehavior

## 规矩

- rule-9ba52307f68b｜ViewPager2 只禁手势滑动时，Swiper 用 disableSwipe(true) 不用 enabled｜读到：ViewPager2 上写了 isUserInputEnabled = false，子页是可交互的 Fragment；写错：对应的 Swiper 上写了 .enabled(false)
- rule-84200806cc94｜源端 ViewPager2 不可滑时，目标不用 Swiper，或显式写 disableSwipe(true)｜读到：源端 ViewPager2 的适配器只有 1 页，或 isUserInputEnabled = false；规格、派工或映射表写 ViewPager2 → Swiper；写错：Swiper(controller){ 单个内容 }.index(0).indicator(false).loop(false)，没有 disableSwipe(true)，还留着 changeIndex 切页
- rule-7aa52f754e82｜承载可交互子页的容器设 enabled 或 hitTestBehavior 时，按作用于整个子树来选取值｜读到：源端 ViewPager2 等容器承载多个可交互的 Fragment，容器本身只限制某个行为（如滑动）；写错：Swiper、Tabs、Stack 等容器上写了 .enabled(false) 或会挡住子节点的 .hitTestBehavior(...)，放进去的子页控件点不动
