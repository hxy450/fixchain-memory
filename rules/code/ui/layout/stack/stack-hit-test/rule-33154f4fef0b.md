# 叠在 Scroll/Swiper 上的全屏叠加容器，设 hitTestBehavior Transparent

审的是：代码
触发（任一种）：
- 读到：Compose `Box(fillMaxSize)` 里，在可滚动内容（含轮播）之上叠放悬浮栏；写错的样子：Stack 里叠在 Scroll / Swiper 之上、`.width('100%').height('100%')` 的容器（如 Column + `Blank().layoutWeight(1)`）没有 `.hitTestBehavior(HitTestMode.Transparent)`
适用范围：ArkUI Stack 里叠在可滚动、可滑动兄弟节点上，尺寸铺满内容区的叠加容器
做法：
- 在这个全屏容器上加 .hitTestBehavior(HitTestMode.Transparent)，例：Column() { Blank().layoutWeight(1); 底栏 }.width('100%').height('100%').hitTestBehavior(HitTestMode.Transparent)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hitTestBehavior(value: HitTestMode): T，默认 HitTestMode.Default：默认时本节点和子节点响应触摸测试，被它盖住的兄弟节点收不到（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- HitTestMode.Transparent：本节点和子节点照常响应，同时让被它盖住的其他节点也做触摸测试（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Transparent）
- Stack 中触摸区域重叠时，只有给最上层节点设 HitTestMode.Transparent，下层节点才触发触摸测试：叠加容器要设在最上层那个节点上（出处：ts-universal-attributes-hit-test-behavior.md，触摸测试控制）
- 底栏外包全屏 Column + Blank().layoutWeight(1) + hitTestBehavior(HitTestMode.Transparent) 后，底栏在底部，下层 Scroll 和 Swiper 能滑动：全屏叠加容器加 Transparent 的效果（出处：卡里修好并验证过）
- onTouchIntercept(callback: Callback<TouchEvent, HitTestMode>): T：同族接口：CommonMethod.onTouchIntercept，触摸测试时按事件动态返回 HitTestMode（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouchIntercept）
来源：1 张卡，1 个应用
- case-9b8bac5680e58daada3a（青商城）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
