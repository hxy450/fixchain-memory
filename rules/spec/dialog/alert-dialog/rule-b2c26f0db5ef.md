# 规格映射弹窗按钮时按角色和视觉位置核对，不把 primaryButton 的参数先后当显示顺序

审的是：规格
触发（任一种）：
- 读到：源端 AlertDialog.Builder 的 setPositiveButton / setNegativeButton 是按钮角色；写错的样子：规格写「AlertDialog.show({primaryButton, secondaryButton})｜文案/顺序保持（正=… 负=…）」，没核对两端系统框各把按钮放在哪一侧
适用范围：规格里把源端系统对话框的正 / 负键映射到目标弹窗按钮槽位时
做法：
- 写「顺序保持」前先查目标系统框把每个参数槽位放在哪一侧（ArkUI AlertDialog 的 primaryButton 在左），再按源端视觉位置（负键左、正键右）决定正 / 负键各放进哪个槽位，或改用自定义弹窗
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ArkUI 系统 AlertDialog 把 primaryButton 放在左侧，按钮首字母大写、标题居中：照搬「正 = primaryButton」时正键显示在左（出处：卡里修好并验证过）
- primaryButton: AlertDialogButtonBaseOptions；secondaryButton: AlertDialogButtonBaseOptions：AlertDialogParamWithButtons 的两个按钮槽位（出处：鸿蒙 SDK 的 ets/component/alert_dialog.d.ts，AlertDialogParamWithButtons.primaryButton）
- 源端按钮条 button2（负键）在 button1（正键）左边，整体靠右：源端的视觉顺序（出处：Android SDK 平台资源 data/res/layout/alert_dialog_button_bar_material.xml（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-bee1ccf417ac7e3b453c（2048）：做法第 1 步 ← 建议 2；取值 1 ← 诊断
