# 延后状态栏避让时，自绘标题栏外层也留顶部 inset 钩子，FWD-REF 写明顶部和底部两处

审的是：代码
触发（任一种）：
- 读到：派工写 needs_immersive_safearea=true；源页面用 IonHeader / IonToolbar 自绘顶部工具栏，目标是 NavDestination().hideTitleBar(true) 子页，WindowModel 还没落地；写错的样子：自绘标题栏的头部 Stack 外层没有任何顶部 inset 钩子，唯一的 FWD-REF 放在 Scroll 底部，注释只写底部 safe-area 份额
适用范围：页面转换阶段，安全区基建（WindowModel、全屏布局）没就绪、把自绘标题栏的状态栏避让延后时
做法：
- 在自绘标题栏外包一层 Column，写 .padding({ top: this.safeTopPadding })，safeTopPadding 先用临时 @Local 值 0（或直接引用占位），并标 FWD-REF
- FWD-REF 注释写明两处：标题栏顶部（windowTopPadding）和底部内容（windowBottomPadding），不只在 Scroll 底部放一个只描述底部份额的 marker
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- hideTitleBar(value: boolean): NavDestinationAttribute：隐藏系统标题栏后，顶部是页面自绘的头部，状态栏避让要页面自己做（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.hideTitleBar）
- 沉浸式布局状态下……需要在组件布局时做额外的布局避让：开启全屏布局后，没留顶部避让的头部会落到状态栏下（出处：immersive-window-feature.md，布局避让）
未核实：卡里的环境是 HarmonyOS 26.0.0，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-5955d25895cbd250bbde（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
