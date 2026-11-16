# 源端普通确认框、信息框，目标用自带 Back 关闭的弹窗，不手写 Stack 浮层

审的是：代码
触发（任一种）：
- 读到：源端 Compose AlertDialog / Dialog(onDismissRequest = …) 是打开期间不跨路由跳转的普通确认框、信息框；映射参考 P-27 的负向守卫写明普通确认框不需要页面级；写错的样子：以 P-27 为由把它写成 Stack 内 if 条件渲染的 @Builder 遮罩+卡片，没有接管 Back
适用范围：迁 Compose 弹窗、选目标端弹窗机制时
做法：
- 普通确认框、信息框用自带 Back 关闭的弹窗机制：@CustomDialog + CustomDialogController，或 UIContext 的 PromptAction.openCustomDialog(dialogContent, options)
- 确需页面级时，openCustomDialog 的 options 写 levelMode: LevelMode.EMBEDDED，或把弹窗做成 NavDestination().mode(NavDestinationMode.DIALOG)；不另写不接管 Back 的手工浮层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：UIContext 上打开自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- levelMode?: LevelMode，@default LevelMode.OVERLAY：弹窗显示层级，默认在所有页面之上（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.levelMode）
- LevelMode.EMBEDDED = 1（Display within the current page），@since 15：页面级弹窗；文档写明只在 showInSubWindow 为 false 时生效（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，LevelMode.EMBEDDED；ts-methods-custom-dialog-box.md，CustomDialogControllerOptions对象说明）
- mode(value: NavDestinationMode): NavDestinationAttribute；NavDestinationMode.DIALOG = 1：把 NavDestination 设成对话框模式，默认透明，进出栈不影响下层页面的生命周期（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.mode、NavDestinationMode.DIALOG）
- 按下返回键和 ESC 键时会让弹窗退出：CustomDialog 自带 Back 关闭（出处：ts-methods-custom-dialog-box.md，CustomDialogControllerOptions对象说明）
- levelMode?: LevelMode：同族接口：CustomDialogControllerOptions 同样可设页面级（出处：鸿蒙 SDK 的 ets/component/custom_dialog_controller.d.ts，CustomDialogControllerOptions.levelMode）
- levelMode?: LevelMode：同族接口：AlertDialogParam 同样可设页面级（出处：鸿蒙 SDK 的 ets/component/alert_dialog.d.ts，AlertDialogParam.levelMode）
未核实：卡里的修复是给页内浮层补 onBackPressed，改用自带弹窗机制后的 Back 行为卡里没有上机验证；EMBEDDED 弹窗和 NavDestinationMode.DIALOG 页面在 Back 时是否只关弹窗，声明里没写明
来源：1 张卡，1 个应用
- case-0fc468c36c3cf09b06bb（CleanSweep）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
