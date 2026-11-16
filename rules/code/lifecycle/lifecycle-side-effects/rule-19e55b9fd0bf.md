# Fragment 生命周期按覆盖类型建状态机，不只挂 onShown/onHidden

审的是：代码
触发（任一种）：
- 读到：Fragment 里 onActivityCreated → init()（每次视图创建都重建）、onResume、onPause 各有逻辑；页面会被另一个 Fragment 替换、被全屏 Activity 或对话框式 Activity 覆盖；写错的样子：NavDestination 只挂 onShown（注释「onResume 等价」）和 onHidden（注释「onPause 等价」），被替换再返回时视图常驻不重建
适用范围：把 Fragment 生命周期映射到 NavDestination 时（VisibilityChangeReason 声明 @since 21）
做法：
- 按覆盖类型合成：被 Fragment 页替换 → onPause + onDestroyView，返回时重走 onActivityCreated → init 重建视图；被全屏 Activity 页覆盖 → onPause + onStop；对话框式或外部 Activity → 只 onPause；回到前台 → onResume
- 覆盖类型用 uiObserver 的 navDestinationSwitch 里的目标页名、窗口 windowEvent 的焦点变化和 onShown/onHidden 回调的 VisibilityChangeReason 区分；同工程别的页面用过的「onResume → onShown」不是依据，要对照本页源码的全部回调
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute；onHidden 同型：显示、隐藏回调带上变化原因（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown、NavDestinationAttribute.onHidden）
- VisibilityChangeReason：TRANSITION = 0（页面导航）、CONTENT_COVER = 1（bindContentCover）、APP_STATE = 2（前后台）：区分是页面切换、全屏模态还是进后台（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，VisibilityChangeReason）
- on(type: 'navDestinationSwitch', context: UIAbilityContext | UIContext, callback: Callback<NavDestinationSwitchInfo>): void：监听 NavDestination 切换，拿到切到的是哪个页面（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.observer.d.ts，uiObserver.on('navDestinationSwitch')）
- on(type: 'windowEvent', callback: Callback<WindowEventType>): void；WINDOW_ACTIVE = 2、WINDOW_INACTIVE = 3：窗口获焦、失焦，用来识别对话框式或外部 Activity 覆盖（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('windowEvent')、WindowEventType）
- onDestroyView：之前创建的视图已从 Fragment 分离，下次显示时会创建新视图：被替换再返回时源端会重建视图（出处：android.app.Fragment#onDestroyView）
- onHidden(被 Fragment 页覆盖) 标记视图销毁、onShown 走重建，按四类覆盖合成状态机后与源端一致：修好后的写法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自 API 24（HarmonyOS 6.1.1），本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-aebac48fa7acdb86e57e（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 6 ← 诊断
