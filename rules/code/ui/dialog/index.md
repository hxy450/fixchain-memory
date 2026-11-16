# 弹窗与浮层

源端有 AlertDialog、DialogFragment、BottomSheetDialog、PopupWindow、XPopup、Toast、Snackbar、上下文菜单，目标端有 openCustomDialog、CustomDialogController、bindSheet、bindPopup、Stack 里的遮罩浮层、showToast 时

## 子主题

- [菜单、气泡与下拉面板](menu/index.md)（24 条）：源端有 PopupWindow 的 showAsDropDown / showAtLocation、registerForContextMenu / onCreateContextMenu、AttachPopupView、Balloon 气泡，目标端有 bindPopup、bindMenu、openMenu 或锚定在控件上的浮层时
- [底部弹层与上拉面板](sheet/index.md)（13 条）：源端有 BottomSheetDialog / BottomSheetDialogFragment、ModalBottomSheet、BottomSheetBehavior、SlidingUpPanelLayout，目标端有 bindSheet 和 SheetOptions，或 Stack 加 translate 写的面板时
- [吐司与提示条](toast/index.md)（20 条）：源端有 Toast.makeText、Snackbar / SnackbarHost，目标端有 promptAction.showToast、统一的 ToastService 门面或自绘的提示条时

## 触发族

- [半模态面板里再弹出的对话框的呈现层级](dialog-level-from-sheet/index.md)（2 条）：读到 BottomSheetDialogFragment 里再 show 一个 DialogFragment，或迁移陷阱 P-27（弹窗开着时跨路由 push 会盖住新页）；产物里这个弹窗写成宿主页 Stack 里的 if 浮层、openCustomDialog，或带 LevelMode.EMBEDDED / NavDestinationMode.DIALOG
- [源对话框迁成哪种弹窗承载](dialog-carrier/index.md)（13 条）：读到 AlertDialog.Builder / MaterialAlertDialogBuilder（带不带 setView）、居中的 DialogFragment，或 bindSheet 面板里再弹的对话框；产物里写成 AlertDialog.show、openCustomDialog、bindSheet、bindContentCover 还是页内 Stack 浮层
- [复刻平台 AlertDialog 的外观](alertdialog-look/index.md)（18 条）：读到没有自定义样式的 AlertDialog.Builder / MaterialAlertDialogBuilder 或 manifest 里的 supportsRtl；产物里自绘对话框面板的字号字重、宽度和限高、标题与按钮条的对齐和方向，以及各页是否共用一个对话框组件
- [自绘弹窗的打开、关闭和触摸穿透](custom-dialog-open-close/index.md)（8 条）：读到 setCancelable / setCanceledOnTouchOutside、循环里逐个 show 的模态窗或会重建的 Activity；产物里遮罩的 onClick 和 HitTestMode.Block、ComponentContent 的关闭回调、方向变化时的关闭路径，以及一次开几个弹窗
- [弹窗组件和宿主之间的接线](dialog-host-wiring/index.md)（4 条）：读到弹窗 show 时带 onDismiss 或结果回调，或多个页面共用同一个详情对话框、底部面板；产物里遮罩、返回键、页面离开的关闭路径和结果回传，以及共享组件的 @Event 在各宿主调用点有没有接上
- [可取消的 AlertDialog 的返回键和取消去向](alertdialog-cancel-back/index.md)（3 条）：读到 AlertDialog.Builder 默认可取消或带 setOnCancelListener、源 Activity 的 onBackPressed 先取消打开的对话框；产物里页内 Stack 浮层弹窗只接了蒙层 onClick、NavDestination 没有 .onBackPressed，或改用 openCustomDialog 承载
- [安卓对话框改写成的页内弹层](dialog-overlay/index.md)（7 条）：读到 AlertDialog / Dialog 子类、ListPreference 和 EditTextPreference 这类 DialogPreference 弹出的对话框；产物里是 Stack 里遮罩加卡片的页内弹层或自绘面板
- [V2 页面里的自定义弹窗](v2-custom-dialog/index.md)（3 条）：@ComponentV2 页面要弹自定义弹窗：产物里的 CustomDialogController、openCustomDialog 的 builder 或 ComponentContent，以及弹窗组件自己 new 的 ViewModel
- [Compose 的 Dialog、AlertDialog 迁成的弹窗形态](compose-dialog-form/index.md)（4 条）：读到源端 Compose Dialog / AlertDialog / ModalBottomSheet 带 onDismissRequest；交回的代码改成 Stack 里 if 渲染的遮罩浮层，没有接管 Back、没隐藏背景无障碍
- [按接口返回数据条件弹出的弹窗](data-gated-popup/index.md)（2 条）：读到源端弹窗函数先判 token 为空 return、再 POST 专用接口、按返回对象和必填字段、当日次数决定是否展示；交回的只判了每日次数，或改调同名内容的列表接口取 items[0] 就弹
- [外部库模板按配置对象弹出的隐私协议弹窗](library-privacy-dialog/index.md)（4 条）：读到源端构造 Config 配置对象（标题、条目及图标、checkImageId / unCheckImageId、linkColor、goServiceLink / goPrivacyLink 回调）交给外部库 Helper 弹窗，工程里没有这个弹窗的 layout；产物里自写的 CustomDialog / openCustomDialog 弹窗
- [对话框窗口层的遮罩、投影、圆角、宽度和位置](dialog-window-layer/index.md)（7 条）：读到源端用 AlertDialog、MaterialDialog、DialogPreference 或 android:theme 为 Theme.*.Dialog 的 Activity 弹出浮动窗口，外观来自主题（backgroundDimAmount、windowElevation、窗口宽度），窗口在系统栏之间居中、压暗应用画的状态栏；产物里 openCustomDialog 的 maskColor、alignment / offset，自绘卡片的 .shadow、.borderRadius、.width 和弹窗期间的 statusBarColor
- [对话框库 Builder 建的对话框（material-dialogs）的形制和排版缺省](dialog-lib-defaults/index.md)（3 条）：读到源端用 material-dialogs 等对话框库的 MaterialDialog.Builder（customView、positiveText）建对话框，项目 res/ 里没有对应布局，库内的 dimen、布局几何和 Builder 缺省（如正文 setLineSpacing）不在源码树里；产物里自绘弹窗的内边距、字号、圆角、按钮栏高度和正文 lineSpacing 有没有出处
- [对话框接口的条目和回调参数](dialog-item-callbacks/index.md)（1 条）：读到 ViewModel 或 presenter 接口的对话框方法带条目列表和多个回调参数（选中某项、清空、onCancel），或 AlertDialog 的 setItems；产物里页面实现用 void 丢弃回调，或用 showAlertDialog 只显示拼起来的条目
