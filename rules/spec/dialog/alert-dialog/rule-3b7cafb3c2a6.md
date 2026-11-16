# 规格写对话框点外取消时，写明安卓判定：触摸未被框内视图消费且抬起在窗口外

审的是：规格
触发（任一种）：
- 读到：源端 AlertDialog.Builder…show()、Dialog、DialogFragment 或 ListPreference 没调 setCanceledOnTouchOutside(false) / setCancelable(false)，对话框里有按钮、列表、输入框或可滚动正文；写错的样子：规格的取消契约只写「返回键与点击对话框外部两条取消路径均默认可用」「返回键/点外（cancelable 默认 true）」，没写点外路径的触摸判定
适用范围：规格阶段为源端没关点外取消的对话框写取消契约时
做法：
- 点外取消一项写出判定：只有这次触摸没被对话框窗口内的视图消费（按钮、列表、输入框、可滚动正文、按钮条都会消费按下），且抬起落在窗口外，才取消；按在这些控件上拖到外部松手不取消；按在标题等不消费触摸的位置拖出去、或直接点外部，才取消
- 依据写框架源码：Dialog#dispatchTouchEvent 先交窗口视图、未消费才进 onTouchEvent，再由 Window#shouldCloseOnTouch 判 ACTION_UP 是否在窗口外；返回键路径另写一项，不受这个条件影响
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- if (mWindow.superDispatchTouchEvent(ev)) { return true; } return onTouchEvent(ev);：触摸先交对话框窗口里的视图，被消费了就不再判点外（出处：android.app.Dialog#dispatchTouchEvent）
- mCancelable && mShowing && mWindow.shouldCloseOnTouch(mContext, event) 时 cancel()：没被视图消费的触摸才走到点外取消（出处：android.app.Dialog#onTouchEvent）
- isOutside = ACTION_UP 且越出窗口（含 getScaledWindowTouchSlop 余量），或 ACTION_OUTSIDE：按抬起点判在不在窗口外（出处：android.view.Window#shouldCloseOnTouch、Window#isOutOfBounds）
来源：1 张卡，1 个应用
- case-96bad1fc979bd25d24d3（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断
