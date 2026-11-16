# 接收页 onReady 里 instanceof 判定的路由参数类没有 export 时，直接 export 它

审的是：代码
触发（任一种）：
- 写错的样子：NavDestination 页面里 class P { … } 前面没有 export，onReady 里却用 context.pathInfo.param 再 instanceof P 判定
适用范围：ArkTS Navigation 的接收页（NavDestination）用 instanceof 判定路由参数类时
做法：
- 把 onReady 里 instanceof 用的参数类写成 export class P { … }，它就是这个页面对外的参数契约，发送方 import 它来 new
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onReady(callback: import('../api/@ohos.base').Callback<NavDestinationContext>): NavDestinationAttribute：NavDestination 在构建子组件前回调，回调参数里带 pathInfo（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- NavDestination 子页第一次创建时触发 onReady，可以在里面获取此页面对应的参数（示例：context.pathInfo.param as string）：参数在 onReady 里取（出处：arkts-navigation-jump.md，参数获取）
未核实：卡里记的是鸿蒙 SDK API 24，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-9d077ec16cc976090144（real-estate-hmos）：做法第 1 步 ← 建议 2
