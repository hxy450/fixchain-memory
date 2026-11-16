# 装配 Layer 2 或验收 Layer 3 时逐页核对顶部避让，只有底部避让的不算通过

审的是：计划与派工
触发（任一种）：
- 读到：入口壳要在根 Navigation 上写四向 expandSafeArea；写错的样子：派工或装配说明写「各子页面 Layer 3/4 已自处理」，没有逐页核对 NavDestination 页和壳内嵌子页的顶部；验收只要出现 windowBottomPadding 就判 Layer 3 通过
适用范围：入口壳装配 Layer 2 expandSafeArea 的派工，以及 Layer 3 前景避让的验收
做法：
- 装配前逐个列出 NavDestination 页和壳内嵌子页，写明每页顶部用的是 windowTopPadding 还是别的明确避让
- Layer 3 验收要求顶部和底部各有避让，只命中 windowBottomPadding 的页面判为未通过
来源：1 张卡，1 个应用
- case-b4a2f2d65e01a68393e3（AntennaPod）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
