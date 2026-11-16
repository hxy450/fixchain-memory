# Activity 的返回键处理（onBackPressed、OnBackPressedDispatcher）

agent 会看到什么：读到 Activity 覆写 onBackPressed() 按标志分支，或用 onBackPressedDispatcher.addCallback 登记回调；交回的返回按钮无条件 pop，或 NavDestination 的 .onBackPressed 写成封闭的固定分支

## 规矩

- rule-adbca6ce5612｜源端返回键按来源标志分支时，返回按钮和 onBackPressed 共用同一分支，不默认 pop｜读到：Activity 里返回按钮点击和 onBackPressed() 按启动来源标志分支：标志为真时执行别的动作（如添加默认项并进入主页），否则 finish()；写错：目标返回按钮无条件 navPathStack.pop()，NavDestination 上没有 .onBackPressed(...)，来源标志分支丢失
- rule-f916a1de9365｜源端用 OnBackPressedDispatcher 时，壳实现可登记的后进先出返回回调栈，宿主先分发｜读到：源端 Activity 通过 onBackPressedDispatcher.addCallback 登记壳层回调，子组件（列表多选、菜单）另行登记 OnBackPressedCallback；写错：壳的 NavDestination .onBackPressed(...) 写成封闭的固定分支（栈判断 → 默认页 → 开抽屉 → 退出），没有子页登记返回回调的入口；嵌入同一子页的其他 NavDestination 宿主也不分发
- rule-e0e24b40f9be｜非 @Entry 子组件的返回拦截要由 @Entry 壳页 onBackPress 转调，不靠自身回调｜读到：源端在非 Activity 根的 Composable 里用 BackHandler / PredictiveBackHandler 按状态条件拦截返回；写错：目标组件不是 @Entry、被 @Entry 壳页直接组合（不在 Navigation 栈内），却只在自身写 onBackPress() 或挂 NavDestination().onBackPressed(...)；壳页没有转调
- rule-447cf95e5121｜源端有 OnBackPressedCallback 时，VM 提供单一返回决策方法，不用注释代替实现｜读到：源端注册了几个 OnBackPressedCallback（handleOnBackPressed，按状态 setEnabled，如锁屏、暂停预览、popup）；规格验收条目写「锁定后按返回仅提示不离开」「按返回恢复预览」；写错：VM 里没有返回决策方法，只写注释「由 Navigation back 拦截承载」；也没有 FWD-REF 或交接到宿主页的 onBackPressed
