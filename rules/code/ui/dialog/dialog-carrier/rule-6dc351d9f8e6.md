# 规格只写「系统弹窗 1:1」时，落地 AlertDialog 前逐项比对，不符就回报或改自定义弹窗

审的是：代码
触发（任一种）：
- 读到：规格或映射参考写「AlertDialog → AlertDialog｜直接映射」「系统对话框 1:1」，源端是只设正 / 负键的 AlertDialog.Builder；写错的样子：写成 AlertDialog.show({ primaryButton: 源端正键, secondaryButton: 源端负键 })，注释写「系统弹窗 1:1」
适用范围：按规格落地替代源端平台默认警告框的弹窗时
做法：
- 落地前把源端截图或平台样式与目标系统框逐项比对（按钮顺序、大小写、标题对齐）；有差异就回报规格或改自定义实现，不拿注释里的「1:1」当依据
- 自定义实现写成 uiContext.getPromptAction().openCustomDialog(content, { autoCancel, maskColor, offset, transition })，面板、按钮条照平台资源复刻；负键只关闭，正键关闭后再执行动作
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：PromptAction 上打开自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- autoCancel?: boolean（默认 true）、maskColor?: ResourceColor、transition?: TransitionEffect、offset?: Offset：BaseDialogOptions 里点遮罩关闭、遮罩色、进出场、位置偏移（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions）
- static show(value: AlertDialogParamWithConfirm | AlertDialogParamWithButtons | AlertDialogParamWithOptions)：系统 AlertDialog，自带居中标题、大圆角、首字母大写按钮（出处：鸿蒙 SDK 的 ets/component/alert_dialog.d.ts，AlertDialog.show）
- openCustomDialog 用透明外框、autoCancel、offset.dy =（状态栏高 − 手势条高）/ 2、maskColor 与 transition；负键只关闭，正键关闭后执行：修复后的弹窗（出处：卡里修好并验证过）
- openCustomDialogWithController<T extends Object>(dialogContent: ComponentContent<T>, controller: promptAction.DialogController, options?: promptAction.BaseDialogOptions): Promise<void>：同族接口：带控制器的自定义弹窗（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialogWithController）
- openCustomDialog(options: promptAction.CustomDialogOptions): Promise<number>：同族接口：按 builder 打开自定义弹窗，返回弹窗 id（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
未核实：卡里的行为出自 SDK 6.1.0(23)，与本机同版
来源：1 张卡，1 个应用
- case-bee1ccf417ac7e3b453c（2048）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断；取值 4 ← 诊断
