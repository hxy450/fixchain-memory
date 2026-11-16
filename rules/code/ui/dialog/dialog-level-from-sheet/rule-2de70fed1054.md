# 需要页面级的弹窗用 LevelMode.EMBEDDED 或 NavDestinationMode.DIALOG

审的是：代码
触发（任一种）：
- 读到：迁移陷阱条目 P-27（弹窗开着时跨路由 push 会盖住新页）；源码里这个弹窗跳转时就 dismiss() 自身和父面板；写错的样子：组件或宿主注释写按 P-27「页级渲染」，弹窗写成宿主页 Stack 里的 if (…) 浮层
适用范围：引用 P-27 一类「弹窗要页面级」的提示决定弹窗呈现层级时；levelMode 从 API 15 起可用（出自声明）
做法：
- 先核对源码：弹窗在跳转时就 dismiss 自身（及父面板）的，不需要页面级，用默认的 openCustomDialog（levelMode 默认 OVERLAY）
- 跳转后弹窗仍要留在原页时，openCustomDialog 的 options 写 levelMode: LevelMode.EMBEDDED，或把弹窗做成 NavDestination 并写 .mode(NavDestinationMode.DIALOG)；不改成页内 Stack 浮层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- enum LevelMode { OVERLAY = 0, EMBEDDED = 1 }，@since 15：OVERLAY 显示在所有页面层级之上，EMBEDDED 显示在当前页面内（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，LevelMode）
- BaseDialogOptions.levelMode?: LevelMode，默认 LevelMode.OVERLAY；levelUniqueId?: number 是路由或导航页里任一节点的 uniqueId：EMBEDDED 时用 levelUniqueId 指定挂在哪个页面（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.levelMode、BaseDialogOptions.levelUniqueId）
- NavDestinationMode.DIALOG = 1；mode(value: NavDestinationMode): NavDestinationAttribute：对话框模式的 NavDestination，默认透明，入栈出栈不影响下层页的生命周期（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationMode.DIALOG、NavDestinationAttribute.mode）
来源：1 张卡，1 个应用
- case-720d51456fccb920411f（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2
