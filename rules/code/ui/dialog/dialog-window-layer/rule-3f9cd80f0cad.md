# 宿主 openCustomDialog 承载框架对话框时，maskColor 按主题遮罩浓度写

审的是：代码
触发（任一种）：
- 读到：源端框架 AlertDialog 没改窗口 dim，运行期主题有 backgroundDimAmount（Theme.Material.Light 为 0.6）；写错的样子：`openCustomDialog(content, { alignment, autoCancel, onDidDisappear })` 没有 maskColor
适用范围：宿主页用 promptAction / UIContext 的 openCustomDialog 承载复刻的框架对话框时
做法：
- options 里写 maskColor，透明度 = backgroundDimAmount × 255 的黑色（0.6 → '#99000000'）
- 对话框里有输入框时，打开后对它 requestFocus 兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- openCustomDialog<T extends Object>(dialogContent: ComponentContent<T>, options?: promptAction.BaseDialogOptions): Promise<void>：宿主打开自定义对话框（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.openCustomDialog）
- maskColor?: ResourceColor（@since 12），默认 0x33000000：遮罩颜色，不写时比 Android 0.6 浅（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，BaseDialogOptions.maskColor；js-apis-promptAction.md，BaseDialogOptions）
- Theme.Material.Light 的 backgroundDimAmount 是 0.6：源端遮罩浓度（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light 的 backgroundDimAmount（按应用的 compileSdk 取对应平台））
- requestFocus(key: string): void：按组件 id 请求焦点（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，FocusController.requestFocus）
- 打开时设 maskColor '#99000000'、打开后 requestFocus 后与源端一致：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 运行期主题的 backgroundDimAmount：源工程主题定义顺父主题到平台 themes*.xml；读出浓度，乘 255 取整作为黑色的透明度
来源：1 张卡，1 个应用
- case-9d195db79dc4cccc7d1a（Sokoban）：做法第 1 步 ← 诊断、建议 2；做法第 2 步 ← 诊断；取值 5 ← 诊断
