# 被入口 Navigation 压栈的根页 NavDestination 必须实现 onBackPressed 并始终消费

审的是：代码
触发（任一种）：
- 读到：入口用 Navigation 把根页作为 NavDestination 压栈；源端根 Activity 按返回会关 popup、退到后台或退出（OnBackPressedCallback / onBackPressed）；写错的样子：根页 NavDestination 没有 .onBackPressed，或以「接口可能只在较新 API 可用」为由回避
适用范围：根页面本身也在 Navigation 栈里（作为 NavDestination 压栈）时
做法：
- 根页写 .onBackPressed(() => { 先关页内弹层；再调 VM 返回链；都没消费就 context.moveAbilityToBackground()，或按 capture intent 返回取消结果；return true })
- 对接口可用性有疑问时查声明或编译验证，不因猜测回避；检查根页按 Back 后栈深度不变、应用退到后台而不是露出空的 Navigation 外壳
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onBackPressed(callback: () => boolean): NavDestinationAttribute，文档标 10+：低版本就可用，不需要回避（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onBackPressed；ts-basic-components-navdestination.md，onBackPressed）
- 与 Navigation 绑定的导航控制器中存在内容时，此回调生效：根页被压栈后栈里有内容，返回键会走它的 onBackPressed，不拦就被弹出（出处：ts-basic-components-navdestination.md，onBackPressed）
- moveAbilityToBackground(): Promise<void>（@since 12）：把当前 Ability 退到后台（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.moveAbilityToBackground）
- 根页 onBackPressed 先关弹层再走 VM 返回链，否则退到后台，始终返回 true：修好后的写法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK 6.1.1(24)，本机声明按 API 23 核实；capture intent 返回取消结果的具体写法卡里没给
来源：1 张卡，1 个应用
- case-f80e125586e1709cf157（opencamera-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 4 ← 诊断
