# AlertDialog.Builder 弹出的系统对话框

agent 会看到什么：读过的源码用 AlertDialog.Builder（setTitle、setMessage、setPositiveButton / setNegativeButton、setCancelable、setView）弹系统对话框；交回的规格里这个对话框的可见契约、按钮排位、取消方式、映射形态和弹出次数

## 通用查法

### AlertDialog 外观取平台默认时，顺应用主题到平台对话框样式和布局读出数值

审的是：规格
触发（任一种）：
- 读到：AlertDialog.Builder 只设标题、消息、按钮和 setCancelable，没有自定义布局和样式，外观由应用主题继承的平台主题决定；写错的样子：规格的对话框契约写「按平台默认」「系统对话框 1:1」，或排位、标题、底色、宽度、遮罩的取值凭记忆写，没有平台资源出处
适用范围：为外观全由主题决定的平台 AlertDialog 写规格的可见契约时
做法：
- 从 AndroidManifest 的 android:theme 顺 res/values* 的 parent 链找到继承的平台主题，到平台资源 themes_*.xml 读 alertDialogTheme、alertDialogStyle、backgroundDimAmount
- 顺样式引用往下读：windowTitleStyle → 标题字号颜色，layout → 布局里 buttonPanel（button1 正键、button2 负键）的先后、gravity、weight，windowMinWidthMinor / Major → dimens，windowCloseOnTouchOutside → config.xml
- 每项写成数值并注明资源名和平台版本，写进契约和验收
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- mButtonPositive 取 R.id.button1，mButtonNegative 取 R.id.button2：读布局里的 buttonPanel 时，button1 是正键、button2 是负键（出处：com.android.internal.app.AlertController#setupButtons）
- params.dimAmount 取窗口主题的 backgroundDimAmount（缺省 0.5f）：遮罩浓度来自对话框所在主题（出处：com.android.internal.policy.PhoneWindow#generateLayout）
- Theme.Material.Light：alertDialogTheme = @style/ThemeOverlay.Material.Dialog.Alert，alertDialogStyle = @style/AlertDialog.Material.Light：例：应用主题落到框架 Material 浅色主题时，对话框样式从这里往下读（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light（按应用的 compileSdk 取对应平台））
- Theme.Holo：alertDialogStyle = @style/AlertDialog.Holo（layout = @layout/alert_dialog_holo），backgroundDimAmount = 0.6：例：应用主题继承 Theme.Holo 时的对话框样式、布局和遮罩浓度（出处：Android SDK 平台资源 data/res/values/themes_holo.xml，Theme.Holo；styles_holo.xml，AlertDialog.Holo（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题继承的平台主题和它的对话框样式：源工程 AndroidManifest 的 android:theme 和 res/values*/styles.xml、themes.xml 的 parent 链；再到 Android SDK 平台资源（按 compileSdk）data/res/values 的 themes_*.xml、styles_*.xml 和 data/res/layout 下的对话框布局；读 alertDialogTheme / alertDialogStyle，顺 @style、@layout、@dimen、@drawable、@bool 引用一路解析到具体值
未核实：源端用 androidx.appcompat.app.AlertDialog 时样式取自 AppCompat 库的主题属性，族里规矩没有查实这条链
来源：3 张卡，3 个应用
- case-20015832edaeb45f53bb（Bubble Shooter）：做法第 1 步 ← 建议 1
- case-bee1ccf417ac7e3b453c（2048）：做法第 1 步 ← 建议 1
- case-ed0c3a60e7342aa867b4（Blockinger）：做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1

## 规矩

- rule-700e04b3a005｜源端系统弹窗只靠平台默认外观时，规格写出可见契约和取值来源，不写「系统组件 1:1」｜读到：源端用 android.app.AlertDialog.Builder 内联构造，只设 setTitle / setMessage / setPositiveButton / setNegativeButton，没有自定义布局或样式；写错：转换决策表写「AlertDialog.show()（primaryButton/secondaryButton）｜系统对话框 1:1」或「行为等价」，只写文案和按键行为
- rule-0387ed0fad22｜AlertDialog 外观来自主题继承的平台样式时，规格从平台资源取值写成数值契约｜读到：AlertDialog.Builder（含 DialogFragment.onCreateDialog 里的）没有自定义样式，应用主题继承 android:Theme.Holo 这类平台主题；写错：契约只写标题对齐、按钮槽位、遮罩和可取消性，或写「按平台默认」「暗底白字」，没有标题字号颜色、分隔线、消息字号、按钮条、窗口背景、宽度和进出场
- rule-b2c26f0db5ef｜规格映射弹窗按钮时按角色和视觉位置核对，不把 primaryButton 的参数先后当显示顺序｜读到：源端 AlertDialog.Builder 的 setPositiveButton / setNegativeButton 是按钮角色；写错：规格写「AlertDialog.show({primaryButton, secondaryButton})｜文案/顺序保持（正=… 负=…）」，没核对两端系统框各把按钮放在哪一侧
- rule-702687fa8102｜平台默认 AlertDialog 的取消契约按返回键和点外部两路分别写，不写「仅返回键可关」｜读到：源端 AlertDialog.Builder(...).show()，没有调用 setCancelable 或 setCanceledOnTouchOutside；写错：取消契约或平台缺省表只写「系统返回键可关闭」，没写点对话框外部这一路
- rule-ccb5509a126e｜规格把 AlertDialog（含列表选择）映射为居中模态对话框，不写 bindSheet｜读到：源码 new AlertDialog.Builder…setTitle(...).setView(ListView).create() 的列表选择对话框；写错：规格的组件映射写“bindSheet 半模态 + List（或 Menu）”，理由写“选择类交互更贴近”
- rule-05ea76d002be｜源端循环里每个命中各弹一窗时，规格把多窗行为写进怪癖清单，AC 写到弹窗个数和确认次数｜读到：源端判定方法双层循环不 break，每个命中元素都落盘统计并 show 一个不可取消的 AlertDialog；写错：规格和 AC 只写「弹一次」，页面状态接口写成布尔，怪癖清单里没有这一条
- rule-17a6cb945858｜源端 MaterialDialog / AlertDialog / Dialog 主题窗口，规格映射为独立弹窗并记按钮｜读到：源码里有 MaterialDialog.Builder、MaterialAlertDialogBuilder、AlertDialog.Builder 构造的确认、单选（setSingleChoiceItems）或 customView 对话框，或 manifest 里 Activity 用 Theme.*.Dialog 主题；写错：规格决策表写「→ bindSheet」「→ 页内弹层（无独立页面）」「Select 弹层」，没读对话框构造就改了形制，也没记 positive / negative / neutral 按钮文案和 cancelable
- rule-46fb5f12be39｜AlertDialog.setView 对话框的可见契约写进遮罩浓度和卡片限高，并写明由宿主哪个参数承载｜读到：源端 android.app.AlertDialog.Builder 的 setView / setTitle / setPositiveButton，没有改窗口 dim；写错：规格的可见契约只写框体、标题、按钮条、宽度，没有遮罩浓度和高度上限，也没写哪几项由宿主的 openCustomDialog 参数承载
- rule-3b7cafb3c2a6｜规格写对话框点外取消时，写明安卓判定：触摸未被框内视图消费且抬起在窗口外｜读到：源端 AlertDialog.Builder…show()、Dialog、DialogFragment 或 ListPreference 没调 setCanceledOnTouchOutside(false) / setCancelable(false)，对话框里有按钮、列表、输入框或可滚动正文；写错：规格的取消契约只写「返回键与点击对话框外部两条取消路径均默认可用」「返回键/点外（cancelable 默认 true）」，没写点外路径的触摸判定
- rule-aeeefc8f579b｜对话框里的 EditText，规格分开写焦点、软键盘和预填光标，<requestFocus/> 只决定焦点｜读到：源端 AlertDialog / DialogFragment 用 setView 承载 EditText，布局里有 <requestFocus/> 或首个可获焦视图；源码和 manifest 都没有 showSoftInput、setSoftInputMode、windowSoftInputMode；写错：规格写「requestFocus → 打开即聚焦并弹软键盘」，验收条目判据写「软键盘弹出」，把焦点和输入法写成一件事
- rule-3d1a6f3ec838｜规格写对话框可见契约时，遮罩写浓度和覆盖范围，显示位置写参照区｜读到：安卓源端用 AlertDialog / Dialog 窗口；源主题由应用窗口画状态栏底色（windowDrawsSystemBarBackgrounds、statusBarColor）；全局约定决定「目标保持非全屏」；写错：规格的弹窗契约只写「载体 openCustomDialog 居中卡片」「遮罩 60% 黑」「弹层由宿主窗口避让兜底」「仅做系统栏默认避让」，没写遮罩是否覆盖应用窗口画的状态栏、导航栏底色，没写居中的参照区，也没写目标侧要做的处理
