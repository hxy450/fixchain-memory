# 未声明 windowSoftInputMode 且含 EditText 时，验收写首屏焦点分支和键盘避让模式

审的是：规格
触发（任一种）：
- 读到：manifest 里该 activity 没有 android:windowSoftInputMode；EditText 前面只有可能为空的 ListView 或没有常驻可获焦视图；源码没有 requestFocus / showSoftInput；写错的样子：规格只在 Manifest 事实行写“无 windowSoftInputMode（默认弹出）”；验收里没有首屏谁获焦、是否自动弹键盘，也没指派实现
- 读到：AndroidManifest 的 <activity> 没有 android:windowSoftInputMode，布局含 EditText 和 ListView / ScrollView / RecyclerView（或继承 ListActivity / PreferenceActivity）；写错的样子：Manifest 事实写「按系统缺省」，没写实际避让方式和 KeyboardAvoidMode 目标值
适用范围：源 Activity 未声明 windowSoftInputMode、首屏布局含 EditText 时的页面验收
做法：
- 验收写一条“首屏焦点与软键盘”：按布局顺序找第一个可获焦视图（EditText 可获焦；AdapterView 只在 adapter 有数据时可获焦），逐个数据分支写谁获焦、是否自动弹键盘、从子页返回不重复
- 另写一条“调整方式”：含可滚动视图时缺省是 adjustResize，目标写 KeyboardAvoidMode.RESIZE；没有时是 adjustPan，对应缺省的 OFFSET
- 两条都写成带目标值的验收条目，指派给 EntryAbility 或该页实现者
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- windowSoftInputMode 的 stateUnspecified 是缺省：由系统决定：未声明时软键盘是否弹出由系统按情形决定，不能写成无条件的“默认弹出”（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowSoftInputMode 的 stateUnspecified（按应用的 compileSdk 取对应平台））
- adjustUnspecified：the system will automatically select between resize and pan modes, depending on whether the content of the window has any layout views that can scroll their contents：未声明时的缺省：窗口里有可滚动视图时选 resize，否则 pan（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowSoftInputMode 的 adjustUnspecified（按应用的 compileSdk 取对应平台））
- mScrollContainers 里有任一个 isShown() 时取 SOFT_INPUT_ADJUST_RESIZE，否则取 SOFT_INPUT_ADJUST_PAN：框架里自动选模式的那段判断（出处：android.view.ViewRootImpl#performTraversals）
- AdapterView 在 adapter 为空或条数为 0 时把自己设为不可获焦：列表空时首个可获焦视图会落到后面的 EditText（出处：android.widget.AdapterView#checkFocus）
- KeyboardAvoidMode.OFFSET = 0（the layout moves up）、RESIZE = 1（the layout is resized）：adjustPan 对应 OFFSET，adjustResize 对应 RESIZE（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，KeyboardAvoidMode）
- setKeyboardAvoidMode(value: KeyboardAvoidMode): void，Default mode: KeyboardAvoidMode.OFFSET：目标窗口不设时就是 OFFSET（整页上推）（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.setKeyboardAvoidMode）
- 安卓清数据冷启动：列表为空时 EditText 获焦并弹出软键盘；有记录时 ListView 获焦、不弹：未声明 windowSoftInputMode 时首屏焦点随数据分支变化（出处：卡里修好并验证过）
针对本应用要查的：
- 首屏每个数据分支下第一个可获焦视图：源工程的布局 XML（按视图顺序）和对应 Activity 的 onCreate 里 setAdapter / setListAdapter 的数据来源；AdapterView 有数据时它先获焦，没数据时跳过；看 EditText 之前还有没有其他常驻可获焦视图（android:focusable 未关闭的按钮、输入框等）
- 源 Activity 的窗口里有没有可显示的可滚动视图：源工程 AndroidManifest.xml 里该 activity 的属性，它 setContentView 的布局 XML（连同 include），以及 Activity 的父类；有 ListView、ScrollView、RecyclerView 等或继承 ListActivity / PreferenceActivity → adjustResize → 目标写 RESIZE；都没有 → adjustPan → OFFSET
来源：2 张卡，1 个应用
- case-1b03af761b99c891e236（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1；取值 7 ← 诊断
- case-c96bdbf4d2e0fb58e797（Blockinger）：做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1、建议 2
