# Compose Popup 菜单迁成无遮罩、点外和返回键先关的弹层，保留 tonalElevation

审的是：代码
触发（任一种）：
- 读到：Popup(alignment = Alignment.Center, properties 或参数 focusable = true) + Surface(tonalElevation, shadowElevation)，无遮罩；调用方传 tonalElevation（如 6.dp）；写错的样子：目标菜单加了 Column().backgroundColor('#66000000') 灰色遮罩、去掉 tonalElevation 参数；或写成 if (…) 的普通 Stack 子节点，onBackPress 不先关菜单
适用范围：Compose Popup、居中弹出菜单等无遮罩弹层迁成 ArkUI 时
做法：
- 放到系统弹窗层：openCustomDialog 透明全屏容器、maskColor 透明，onWillDismiss 里关菜单（点外和返回键都先关菜单）；或用 bindPopup / bindMenu
- 弹层组件保留 tonalElevation 参数，调用方传入的值（如 6dp）原样传下去
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onWillDismiss?: Callback<DismissDialogAction>；DismissReason.PRESS_BACK = 0、TOUCH_OUTSIDE = 1：交互关闭回调能区分返回键和点外（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，promptAction.BaseDialogOptions.onWillDismiss；ets/component/common.d.ts，DismissReason）
- bindPopup(show: boolean, popup: PopupOptions | CustomPopupOptions): T：同族接口：组件上绑定气泡弹层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindPopup）
- bindMenu(content: Array<MenuElement> | CustomBuilder, options?: MenuOptions): T：同族接口：组件上绑定菜单（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindMenu）
- 链接菜单改为系统弹窗层透明全屏容器（onWillDismiss 关菜单），居中菜单去遮罩并接受 tonalElevation 后与源端一致：修法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK API 24（6.1.1），本机核实用 API 23
来源：1 张卡，1 个应用
- case-79781a308d7df8726820（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 3；取值 4 ← 诊断
