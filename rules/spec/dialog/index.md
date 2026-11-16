# 弹窗与提示

读到源端弹 AlertDialog、Dialog、经工具类或 Helper 弹的弹窗、BottomSheetDialogFragment / ModalBottomSheet、BottomSheetBehavior 面板或 Toast，规格里写弹窗清单、底部面板和提示时

## 触发族

- [AlertDialog.Builder 弹出的系统对话框](alert-dialog/index.md)（12 条）：读过的源码用 AlertDialog.Builder（setTitle、setMessage、setPositiveButton / setNegativeButton、setCancelable、setView）弹系统对话框；交回的规格里这个对话框的可见契约、按钮排位、取消方式、映射形态和弹出次数
- [经工具方法弹出的对话框](util-dialog/index.md)（1 条）：读到源页面经工具类的静态方法弹对话框，调用方 lambda 只传了接受回调，主弹窗里的按钮还会再弹确认弹窗；规格的弹窗清单、页面契约或源码理解笔记只登记了确认弹窗或只写「只有接受回调」
- [源码里给用户的 Toast 和通知提示](toast-notification/index.md)（3 条）：源码里有 Toast.makeText（LENGTH_SHORT / LENGTH_LONG 混用、文案带加工）或把接口返回的数据只经 Toast、Notification 交给用户，规格或源码笔记里把它记成统一时长、或没写怎么呈现
- [页面上弹出、布局不在页面 XML 里的弹窗和底部面板](page-popup-dialogs/index.md)（4 条）：读到 Activity 只一句委托辅助类的 show…Dialog、通过 Helper 加配置对象弹出库渲染的弹窗，或在当前页 show 一个 Dialog / BottomSheet；规格只列页面自身的布局，没有弹层结构、源调用锚点和配置字段，或把底部弹层改写成 HMRouter 路由页
- [底部弹层的展开高度（ModalBottomSheet、BottomSheetDialogFragment）](bottom-sheet-height/index.md)（2 条）：读到 ModalBottomSheet(sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true))，或 BottomSheetDialogFragment 的 onShow 里调了名为 setupFullHeight 的方法、或没改 peekHeight 和高度；规格按名字写「全高」「半开/全开」，给 detents LARGE / MEDIUM
- [CoordinatorLayout 里带 BottomSheetBehavior 的常驻面板](persistent-bottom-sheet/index.md)（1 条）：读到面板容器带 BottomSheetBehavior，位于 CoordinatorLayout 内、BottomNavigationView 之上；转换决策写「bindSheet 半模态或 Stack+translateY 手势」两种并列，没写面板不覆盖底栏、收起不等于停播
- [由主题或库决定的对话框窗口外观](dialog-window-theme/index.md)（3 条）：读到 Activity 的 android:theme 是 Theme.*.Dialog，或对话框由 material-dialogs（MaterialDialog.Builder）这类库包装、源码里只有主题名或库名；规格只写「Dialog 主题」「Dialog 形态页」「→ CustomDialog」，没有暗化、窗口宽度、点外关闭、底色圆角的值和出处
