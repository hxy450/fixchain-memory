# ui/dialog/carriers

按源弹层类型选载体：真弹窗不以页面叠层或路由页充当、V2 页面的弹窗 API、锚定下拉与自定义内容。

[上一级](../index.md)

## 本级经验

- [V2 页面弹窗用浮层或 openCustomDialog](lesson-3f3e1ff0a4d0e0299bda.lesson.md) · 阶段：execute · 信号：@ComponentV2, CustomDialogController, @CustomDialog, openCustomDialog
- [setView 注入自定义内容的确认框改用自定义弹窗](lesson-18fca50f9c801cb282ec.lesson.md) · 阶段：execute · 信号：setView, AlertDialog.show, MaterialAlertDialogBuilder, @CustomDialog
- [当前页 show 的底部弹窗叠在宿主页上不改路由页](lesson-7ef02de8bbc10734c3d2.lesson.md) · 阶段：spec/execute · 信号：bottomDialog, BottomSheetDialog, HMRouter, Navigation
- [按源弹层类型选形态：底部面板才用 bindSheet](lesson-21db515a505be4845497.lesson.md) · 阶段：execute · 信号：DialogHelper, CustomDialog, AlertDialog, BottomSheetDialog
- [真弹窗迁成系统弹窗或半模态，不用可见性叠层充当](lesson-368c4592e4c7075c1871.lesson.md) · 阶段：execute/repair · 信号：XPopup, CenterPopupView, AttachPopupView, BottomPopupView
- [锚定下拉用 bindPopup 原位还原，不换 Select](lesson-666a746081ba1e447322.lesson.md) · 阶段：execute · 信号：showAsDropDown, PopupWindow, bindPopup, Select
