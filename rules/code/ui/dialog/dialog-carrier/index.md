# 源对话框迁成哪种弹窗承载

agent 会看到什么：读到 AlertDialog.Builder / MaterialAlertDialogBuilder（带不带 setView）、居中的 DialogFragment，或 bindSheet 面板里再弹的对话框；产物里写成 AlertDialog.show、openCustomDialog、bindSheet、bindContentCover 还是页内 Stack 浮层

## 规矩

- rule-6dc351d9f8e6｜规格只写「系统弹窗 1:1」时，落地 AlertDialog 前逐项比对，不符就回报或改自定义弹窗｜读到：规格或映射参考写「AlertDialog → AlertDialog｜直接映射」「系统对话框 1:1」，源端是只设正 / 负键的 AlertDialog.Builder；写错：写成 AlertDialog.show({ primaryButton: 源端正键, secondaryButton: 源端负键 })，注释写「系统弹窗 1:1」
- rule-194005a88105｜对话框带 setView 自定义布局时用自定义弹窗承载，不往 AlertDialog.show 塞 builder｜读到：MaterialAlertDialogBuilder / AlertDialog.Builder 在 setTitle、setMessage 和正负按钮之外还调了 setView(...)（如「不再提示」复选框）；写错：目标写成 AlertDialog.show({ title, builder: () => {…}, primaryButton, secondaryButton })：AlertDialogParam 没有 builder 字段，必填的 message 也没传
- rule-2a2ab9e1124a｜Material 对话框（含 setView）转居中弹窗，底部面板才转 bindSheet｜读到：源码 `new MaterialAlertDialogBuilder(…).setView(…)` 加 `setPositiveButton` / `setNegativeButton` 后 `show()`；页面规格的映射行并列写「bindSheet/CustomDialog」；写错：这个对话框被写成 `bindSheet(…)` 半模态，理由是工程既定模式
- rule-d57008d20834｜还原居中 DialogFragment 的点外关闭时，模态内自绘遮罩加居中卡片，不用 bindSheet(CENTER)｜读到：源端是居中显示、点外部可关闭的 DialogFragment；写错：目标用 bindSheet 配 preferType: SheetType.CENTER 挂在 0 尺寸节点上代替
- rule-73c922493585｜从 bindSheet 内部打开的弹窗用 bindContentCover 承载，不写成页内 Stack 条件浮层｜读到：源端 BottomSheetDialogFragment 内部点击后直接 show() 出居中 DialogFragment，或调工具方法弹窗；写错：目标从 bindSheet 内容的回调打开的弹窗，写成页面根 Stack 里 if 条件渲染的全屏遮罩 Column；头注写「规避全局弹窗跨页覆盖（P-27）」或照本页已有浮层先例
- rule-8fc85c5e85c7｜源 AlertDialog 带 icon 时不用没有图标槽的 showAlertDialog，用自定义对话框保留图标｜读到：Material3 `AlertDialog(icon = { Icon(painterResource(…)) }, …)`；写错：目标改用 getUIContext().showAlertDialog(…)，图标被省略，注释或思考写「视觉降级」「与兄弟页同模式」
- rule-5619f80115a5｜安卓真弹窗不复用 @Local 可见性加 Stack 遮罩的页面叠层，按原类改用真弹窗 API｜读到：安卓端 DialogFragment.show(supportFragmentManager, …)，或 XPopup 的 CenterPopupView / AttachPopupView；写错：目标端把 @Local 的可见性状态置 true 来弹出，在页面树里用 if (this.…) 或 .visibility(…) 条件渲染 Stack + 遮罩组件（常带 .zIndex(…)）
- rule-a96ec3839103｜安卓底部弹窗迁移时用系统半模态 Sheet 承载，不写成 visible 驱动的页面内全屏 Stack｜读到：源弹窗继承 XPopup 的 BottomPopupView 一类底部弹窗基类，或是底部 DialogFragment；映射计划或决策台账写「BottomPopup → showBindSheet / 系统半模态」；写错：目标弹窗是 @Param popupVisible / dialogVisible 驱动的全屏 Stack：自绘半透明遮罩、PanGesture 阈值下拉关闭、宿主传返回信号，在宿主页里内嵌或靠 zIndex 叠加；或仍是 NavDestination 路由页
- rule-d90dbec8e77b｜BottomSheetDialogFragment 迁成弹层，不写成标准 NavDestination 加自绘蒙层｜读到：源类继承 BottomSheetDialogFragment / DialogFragment，在宿主上 show(manager, tag, …) 弹出、选中后回调并 dismiss()；规格 page_type 为 modal_overlay 或 dialog；写错：目标写成没有 .mode(NavDestinationMode.DIALOG) 的 NavDestination 路由页，页内自绘半透明蒙层和底板，关闭用 navPathStack.pop()，对外只暴露路由 Builder 和路由参数
- rule-3bd01aa63828｜调用方接入弹层时对照安卓调用点 show()，用弹层入口，不 pushPathByName｜读到：安卓调用点以 fragment.show(childFragmentManager, tag, …) 弹出这个弹层；写错：目标调用方写 navPathStack.pushPathByName('<弹层路由名>', …) 打开它，因为已转换的组件只暴露了路由页
- rule-554bbd1a8aad｜源端对话框不做成页内 Stack overlay，用 openCustomDialog 等独立弹窗｜读到：源码用 MaterialDialog.Builder、MaterialAlertDialogBuilder 或 AlertDialog.Builder 弹出对话框；写错：目标在页面 build 里用 Stack + 全屏遮罩 Column + 白卡、按 visible 状态显示弹窗组件，没有 openCustomDialog / CustomDialogController，返回键不能先关弹窗
- rule-7955de9b2522｜源端每次 new 的对话框，目标端每次调用新建 ComponentContent，只关闭自身｜读到：方法里每次 `new MaterialDialog.Builder(…)…build().show()`，对话框由局部变量持有；写错：服务里用单例字段持有 `ComponentContent`，每次新调用前先 dismiss 旧句柄，前一个弹窗被静默关闭、回调永不触发
- rule-c11d0311e265｜Preference 或 MaterialDialog 弹窗写成 bindSheet 时，改成居中对话框按库几何｜读到：源端 ListPreference、EditTextPreference 或 MaterialDialog 单选列表，或规格写着「bindSheet 弹层」；写错：目标用 .bindSheet(…, { detents: [SheetSize.MEDIUM, SheetSize.LARGE] }) 承载这些弹层，宽度用自造的比例常量，TextInput 没有 preference_dialog_edittext 的边距
