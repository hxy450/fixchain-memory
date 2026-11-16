# 对话框里的 EditText，规格分开写焦点、软键盘和预填光标，<requestFocus/> 只决定焦点

审的是：规格
触发（任一种）：
- 读到：源端 AlertDialog / DialogFragment 用 setView 承载 EditText，布局里有 <requestFocus/> 或首个可获焦视图；源码和 manifest 都没有 showSoftInput、setSoftInputMode、windowSoftInputMode；写错的样子：规格写「requestFocus → 打开即聚焦并弹软键盘」，验收条目判据写「软键盘弹出」，把焦点和输入法写成一件事
适用范围：规格提取阶段给源端对话框里的输入框写打开时的初始状态时
做法：
- 分三项写：焦点（<requestFocus/> 或首个可获焦视图）；软键盘（只有源码显式请求，即 showSoftInput、setSoftInputMode 为 STATE_VISIBLE / ALWAYS_VISIBLE、DialogPreference / EditTextPreference 的输入法请求，或 STATE_UNSPECIFIED 解析为 adjustResize、或大屏时才自动弹；手机上的普通对话框是 adjustPan，只获焦，点按才弹）；预填光标
- 拿不准软键盘时标「待核」，附 dumpsys input_method 的核验方法，不写成验收条目
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- SOFT_INPUT_STATE_UNSPECIFIED = 0：没有指定状态，系统为了体验可能在窗口获焦时显示或隐藏软键盘：不写 softInputMode 时不等于打开就弹键盘（出处：android.view.WindowManager.LayoutParams#SOFT_INPUT_STATE_UNSPECIFIED）
- SOFT_INPUT_STATE_VISIBLE = 4，SOFT_INPUT_STATE_ALWAYS_VISIBLE = 5：源码显式要求弹键盘时用的两个取值（出处：android.view.WindowManager.LayoutParams#SOFT_INPUT_STATE_VISIBLE / SOFT_INPUT_STATE_ALWAYS_VISIBLE）
- 手机上实测对话框窗口 softInputMode = STATE_UNSPECIFIED | ADJUST_PAN | IS_FORWARD_NAVIGATION，mShowRequested = false，连开 4 次都不弹键盘，点按才弹：只有 <requestFocus/> 的对话框只获焦（出处：卡里修好并验证过）
针对本应用要查的：
- 源端对话框是否显式请求输入法：源工程里对话框类（onCreateDialog / onCreate）和它 inflate 的布局 XML，以及 AndroidManifest 里对应 Activity 的 windowSoftInputMode；搜 showSoftInput、setSoftInputMode、windowSoftInputMode、DialogPreference；都没有就写「只获焦、不弹键盘」
来源：1 张卡，1 个应用
- case-1446bd8a3fc8a14b0a94（Sokoban）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
