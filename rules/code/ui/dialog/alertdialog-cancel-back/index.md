# 可取消的 AlertDialog 的返回键和取消去向

agent 会看到什么：读到 AlertDialog.Builder 默认可取消或带 setOnCancelListener、源 Activity 的 onBackPressed 先取消打开的对话框；产物里页内 Stack 浮层弹窗只接了蒙层 onClick、NavDestination 没有 .onBackPressed，或改用 openCustomDialog 承载

## 规矩

- rule-d600b9c79610｜可取消的 AlertDialog 用 openCustomDialog 承载，返回键和点外走 onCancel｜读到：AlertDialog.Builder 链没有 setCancelable(false)（默认可取消），或带 setOnCancelListener；写错：目标写成页内 Stack 条件渲染浮层，只接蒙层 .onClick 取消；弹窗打开时按返回直接退出页面或叠弹别的框
- rule-fde262688b60｜自绘层复刻 AlertDialog 时，返回键和点遮罩都走同一个 OnCancelListener 去向｜读到：源端 AlertDialog.Builder 或 Dialog 上 setOnCancelListener(...)，cancel 时写偏好、finish 或进入下一步；写错：目标只在遮罩 onClick 里调 cancel 处理，NavDestination 上没有 .onBackPressed(...)（@Entry 页没有 onBackPress()），返回键不推进 cancel 去向
- rule-51623735472c｜对话框改成页内 Stack 弹层时，宿主 NavDestination 补 onBackPressed 先关弹层｜读到：源端 AlertDialog、ListPreference 对话框或 popup 面板（可被 Back 关闭）；规格映射写 showDialog / CustomDialog / bindSheet / Select；写错：改成 Stack 里按可见状态条件渲染的页内弹层，宿主 NavDestination 上没有 .onBackPressed(...)，或注释写返回由 NavDestination 默认 pop 处理
