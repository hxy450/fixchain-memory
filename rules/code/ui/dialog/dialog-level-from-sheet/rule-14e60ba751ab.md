# 从 bindSheet 面板里打开的弹窗用 openCustomDialog 窗口级呈现，不放宿主页 Stack 浮层

审的是：代码
触发（任一种）：
- 读到：源端在 BottomSheetDialogFragment 里用 DialogFragment 的 show(getParentFragmentManager(), TAG) 打开另一个对话框（onCreateDialog 里用 MaterialAlertDialogBuilder），跳转按钮先 dismiss() 自身再关闭父面板；写错的样子：目标在宿主页根 Stack 里写 if (…) { 遮罩 + 卡片 } 的页内浮层，而面板是同一页上的 .bindSheet(...)；弹窗打开在面板下层，跳转回调没有同时关闭面板
适用范围：目标端面板由宿主页 bindSheet 承载（默认 SheetMode.OVERLAY），要从面板里再打开一个对话框时
做法：
- 弹窗用 this.getUIContext().getPromptAction().openCustomDialog(new ComponentContent(uiContext, wrapBuilder(<弹窗 builder>), 参数)) 窗口级呈现，叠在面板之上；删掉宿主页 Stack 里的条件浮层
- 按源码在跳转回调里先 closeCustomDialog(同一个 ComponentContent) 关弹窗，再把 bindSheet 的 isShow 置 false 关父面板，然后跳转
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T；SheetOptions.mode 默认 SheetMode.OVERLAY：半模态面板的绑定；默认模式下面板显示在窗口顶层、所有页面之上，与对话框同层（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet、SheetOptions.mode、SheetMode.OVERLAY）
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：PromptAction（UIContext.getPromptAction()）打开自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- closeCustomDialog<T extends Object>(dialogContent: ComponentContent<T>): Promise<void>：用打开时的同一个 ComponentContent 关闭弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.closeCustomDialog）
- BaseDialogOptions.levelMode 默认 LevelMode.OVERLAY（显示在所有页面层级之上）：不传 levelMode 时 openCustomDialog 就是窗口级，能盖住 OVERLAY 模式的面板（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.levelMode、LevelMode.OVERLAY）
- openCustomDialog 窗口级模态叠在面板之上，跳转回调连带关闭面板：返修后弹窗显示在面板上层（出处：卡里修好并验证过）
- updateCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options: promptAction.BaseDialogOptions): Promise<void>：同族接口：更新已打开弹窗的选项（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.updateCustomDialog）
来源：1 张卡，1 个应用
- case-720d51456fccb920411f（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 5 ← 诊断
