# Compose 的 Dialog、AlertDialog 迁成的弹窗形态

agent 会看到什么：读到源端 Compose Dialog / AlertDialog / ModalBottomSheet 带 onDismissRequest；交回的代码改成 Stack 里 if 渲染的遮罩浮层，没有接管 Back、没隐藏背景无障碍

## 规矩

- rule-846b34bf9ffc｜源端普通确认框、信息框，目标用自带 Back 关闭的弹窗，不手写 Stack 浮层｜读到：源端 Compose AlertDialog / Dialog(onDismissRequest = …) 是打开期间不跨路由跳转的普通确认框、信息框；映射参考 P-27 的负向守卫写明普通确认框不需要页面级；写错：以 P-27 为由把它写成 Stack 内 if 条件渲染的 @Builder 遮罩+卡片，没有接管 Back
- rule-d9c5e192a813｜源对话框是 Dialog 独立窗口时，目标走系统弹窗通道；用页内遮罩就隐藏背景无障碍｜读到：源端 Dialog(onDismissRequest, properties) / AlertDialog；规格把它映射为 @CustomDialog，或共享对话框组件头注要求经 openCustomDialog 打开；写错：目标改成页内 Stack 遮罩加对话框，显示期间背景没有 .accessibilityLevel('no-hide-descendants')，读屏仍能遍历背景；或把规格改写成「页内 Stack overlay」
- rule-c63c3779d5b5｜源端弹窗改成页内 Stack 浮层时，NavDestination 上加 onBackPressed 逐层关闭｜读到：源端 Compose Dialog / AlertDialog / ExposedDropdownMenu / ModalBottomSheet 带 onDismissRequest，关闭只关弹窗、留在当前页；写错：目标改成 Stack 里 if 渲染的遮罩浮层，所在 NavDestination 没有 .onBackPressed（或照搬了别页没处理返回键的覆盖层）
- rule-2b71a727e2fd｜Compose AlertDialog 迁成 openCustomDialog 弹窗层，不用 Stack 子节点模拟｜读到：Compose AlertDialog(onDismissRequest, confirmButton, …) 或 Dialog，含组件内状态控制的子对话框；写错：弹窗写成页面 Stack 或组件 Column 的条件子节点，加 backgroundColor('#66000000') 自绘遮罩
