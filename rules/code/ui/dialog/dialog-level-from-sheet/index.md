# 半模态面板里再弹出的对话框的呈现层级

agent 会看到什么：读到 BottomSheetDialogFragment 里再 show 一个 DialogFragment，或迁移陷阱 P-27（弹窗开着时跨路由 push 会盖住新页）；产物里这个弹窗写成宿主页 Stack 里的 if 浮层、openCustomDialog，或带 LevelMode.EMBEDDED / NavDestinationMode.DIALOG

## 规矩

- rule-14e60ba751ab｜从 bindSheet 面板里打开的弹窗用 openCustomDialog 窗口级呈现，不放宿主页 Stack 浮层｜读到：源端在 BottomSheetDialogFragment 里用 DialogFragment 的 show(getParentFragmentManager(), TAG) 打开另一个对话框（onCreateDialog 里用 MaterialAlertDialogBuilder），跳转按钮先 dismiss() 自身再关闭父面板；写错：目标在宿主页根 Stack 里写 if (…) { 遮罩 + 卡片 } 的页内浮层，而面板是同一页上的 .bindSheet(...)；弹窗打开在面板下层，跳转回调没有同时关闭面板
- rule-2de70fed1054｜需要页面级的弹窗用 LevelMode.EMBEDDED 或 NavDestinationMode.DIALOG｜读到：迁移陷阱条目 P-27（弹窗开着时跨路由 push 会盖住新页）；源码里这个弹窗跳转时就 dismiss() 自身和父面板；写错：组件或宿主注释写按 P-27「页级渲染」，弹窗写成宿主页 Stack 里的 if (…) 浮层
