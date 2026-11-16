# 开启 setWindowLayoutFullScreen 时逐页核对贴底那一层消费了底部避让

审的是：代码
触发（任一种）：
- 写错的样子：入口在 EntryAbility 里调了 setWindowLayoutFullScreen(true)，但有 NavDestination 页只消费了 windowTopPadding，贴底那一层没有 windowBottomPadding
适用范围：入口收尾阶段，开启全屏布局的一方（入口 Ability 或收口者）
做法：
- 开启前逐页 grep windowTopPadding 和 windowBottomPadding，确认每个 NavDestination 页贴底的那一层都消费了底部避让；只接了顶部的页面补上，或登记移交给负责该页的切片
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>：开启后各页前景伸到系统栏和导航条下，要靠页面自己避让（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen）
- AvoidAreaType.TYPE_NAVIGATION_INDICATOR = 4：底部导航区域，三键导航显示时始终存在：底部避让值的来源（出处：arkts-apis-window-e.md，AvoidAreaType）
来源：1 张卡，1 个应用
- case-4e1ab457a4fa55aaeb29（Privacy Friendly 2048）：做法第 1 步 ← 建议 3
