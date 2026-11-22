# 源对话框带目标系统弹窗没有的槽位（setView 注入的复选框等自定义布局、Compose AlertDialog 的 icon）时改用自定义弹窗承载，不写成 AlertDialog.show 的参数，也不自行省略

## 何时使用

界面实现阶段，把 Android AlertDialog/MaterialAlertDialogBuilder 或 Compose AlertDialog 转换为 ArkUI 弹窗、确定弹窗 API 与参数结构时

## 适用情境

源对话框在标题、正文和正负按钮之外还 setView 注入自定义布局（如“不再提示”复选框），确认回调读取其中控件的状态并写偏好；目标准备用 AlertDialog.show 弹出。也包括 Compose AlertDialog 传了 icon = { Icon(...) }，目标准备改用没有图标槽的 showAlertDialog/AlertDialog.show，并以“仅视觉降级”或“与兄弟页同模式”为由省略图标。

## 例外与边界

- 源对话框只有标题、正文与按钮，没有自定义视图或图标：可以映射 AlertDialog.show，但正/负键按角色核对目标槽位位置；项目要求一比一还原平台默认外观时改用自定义弹窗复刻
- 改用自定义弹窗时保留源对话框的关闭方式：点遮罩、按返回键能不能关闭要和源端一致（源端 setCancelable(false) 等）；自定义弹窗的 autoCancel 默认为 true，点遮罩即关闭，返回键等交互关闭要拦时用 onWillDismiss

## 原因

AlertDialog.show 的参数只有标题、副标题、必填的 message、按钮等字段，没有承载自定义组件树的 builder，也没有图标槽；选它就等于删掉源端图标，把自定义视图写进不存在的字段还会让编译解析失败并引发大面积连锁错误。来源转换者写前已判断“自定义内容需 openCustomDialog”，落盘时又凭记忆假定存在带 builder 的参数形态；修复者删掉 builder 以通过编译，复选框及其偏好写入随之丢失。

## 做法

1. 先看源对话框是否调用 setView、加载自定义布局或传入 icon：都没有时才考虑 AlertDialog.show（按钮槽位与外观取舍见例外）；有则用自定义弹窗，在同一个自定义构建里放图标、标题、正文、复选框与按钮，确认回调读取复选状态后再执行源端的偏好写入与后续动作。
2. V1 页面可用 @CustomDialog + CustomDialogController；@ComponentV2 页面用 UIContext.getPromptAction().openCustomDialog 或状态驱动浮层，不用 CustomDialogController 承载 V2 组件。
3. 只能先落简化弹窗时，把丢失的交互或视觉元素（控件、偏好写入、图标）登记为占位与回补点，并在报告中列为与源端的差异；有决策台账时先查台账，未命中就作为决策缺口上报，不以“仅视觉降级”或兄弟页先例自行定案，也不以不存在的参数假装等价。

## 依赖经验

- [@ComponentV2 页面的弹窗不用 CustomDialogController 承载 V2 组件，改用状态驱动浮层、半模态或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md)

来源支持：3 张卡 · 3 次迁移 · 3 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔例外与边界〕应用主题继承 Theme.Material.Light 且没有另设 alertDialogTheme、backgroundDimAmount 时，框架 AlertDialog 用 ThemeOverlay.Material.Dialog.Alert，背后遮罩按 backgroundDimAmount 0.6 变暗
- 〔例外与边界〕平台 ThemeOverlay.Material.BaseDialog 设 windowBackground=@drawable/dialog_background_material、windowIsFloating=true、windowAnimationStyle=@style/Animation.Material.Dialog（进出场 popup_enter_material / popup_exit_material）、windowCloseOnTouchOutside=@bool/config_closeDialogWhenTouchOutside（values 下为 true，即点外部关闭）
- 〔例外与边界〕平台 Material 警告框按钮条从起始边到末端依次是 button3（中性）、占满剩余宽度的 spacer、button2、button1，layoutDirection=locale：从左到右语言下按钮靠右、负键在正键左边
- 〔例外与边界〕AlertController.setupButtons 把正键放在 button1、负键 button2、中性键 button3；某个按钮文案为空时该按钮 setVisibility(View.GONE)
- 〔例外与边界〕平台 TextAppearance.Material.Button 设 textAllCaps=true：Material 主题下警告框按钮文字全大写
- 〔例外与边界〕平台警告框标题 alertTitle 宽 match_parent、textAlignment=viewStart：标题占满宽度并靠起始边对齐
- 〔例外与边界〕平台警告框正文区 contentPanel 设 minHeight=48dp
- 〔例外与边界〕应用主题没有另设 dialogCornerRadius 时，框架 Material 主题的对话框圆角取 dialog_corner_radius = 2dp
- 〔例外与边界〕ArkUI 系统 AlertDialog（带 primaryButton / secondaryButton）显示时 primaryButton 在左侧；系统框固有版式为标题居中、大圆角、按钮文字首字母大写
