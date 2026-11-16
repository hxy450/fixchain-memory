# 根 Navigation 壳与 NavDestination 页的分工

agent 会看到什么：派工、装配说明或跨切片草稿里，根 Navigation 壳上的机制（四向 expandSafeArea、共享转场、路由守卫）要各 NavDestination 页配合，或要按规格的映射写守卫表达式

## 规矩

- rule-3c897eb9bc6f｜装配 Layer 2 或验收 Layer 3 时逐页核对顶部避让，只有底部避让的不算通过｜读到：入口壳要在根 Navigation 上写四向 expandSafeArea；写错：派工或装配说明写「各子页面 Layer 3/4 已自处理」，没有逐页核对 NavDestination 页和壳内嵌子页的顶部；验收只要出现 windowBottomPadding 就判 Layer 3 通过
- rule-cc7260d055b4｜规格机制要页面侧接线时，计划把页面绑定列入写盘额度，派工不写定制或默认二选一｜读到：规格的转场机制要求各 NavDestination 页面绑定共享转场状态；写错：计划只给各页路由注册（pageRegister）额度、限定每页只改几行，派工写「定制转场或 NavDestination 默认」二选一，页面绑定不在写权内
- rule-e7f51693b202｜跨切片草稿的守卫注释写注册校验、表达式却查栈成员时，按规格映射改表达式｜读到：规格把 isIntentAvailable 映射为「路由表命中页注册态校验（NavDestination 注册表）」，验收条目要求目标不可用或路由未命中时不跳转；写错：派工说明的 cross_slice_edits 草稿注释写「isIntentAvailable 等价：pageMap 未注册页不分发」，表达式却是 getAllPathName().indexOf(pageName) < 0 → return false
- rule-9f5a4a1cffdd｜壳分发交给不拥有目标页的切片时，派工列出各目标页参数类和壳契约｜读到：壳规格写“深链参数 {path, title?, date?} → 目标页参数预填”，源端深链监听把 pathname + search 整体交给路由；写错：壳分发的派工输入只有分发方本 feature 的规格，没有列出各目标页的参数类，也没带目标页功能规格里的壳契约（如“壳 push(path + query)”“页面状态全部来自路由参数”）
