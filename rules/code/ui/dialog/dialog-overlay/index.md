# 安卓对话框改写成的页内弹层

agent 会看到什么：读到 AlertDialog / Dialog 子类、ListPreference 和 EditTextPreference 这类 DialogPreference 弹出的对话框；产物里是 Stack 里遮罩加卡片的页内弹层或自绘面板

## 通用查法

### 框架对话框的遮罩、宽度、圆角、标题字号，从平台主题资源读出再写显式值

审的是：代码
触发（任一种）：
- 读到：源端用 AlertDialog.Builder 或 DialogPreference 弹出框架对话框，应用主题没改对话框外观；写错的样子：目标弹层的遮罩色、width、borderRadius、标题 fontSize 是手写常数（#66000000、width(300)、borderRadius(24)）或标「待核」
适用范围：用页内遮罩加卡片复刻框架对话框
做法：
- 先在源工程 styles / themes XML 里按应用主题的 parent 和 alertDialogTheme 找 backgroundDimAmount、dialogCornerRadius、windowMinWidthMinor 的覆写，有就取它
- 没覆写就按 compileSdk 到 Android SDK 平台资源顺着引用读：themes_*.xml 的 backgroundDimAmount、dialogCornerRadius → dimens.xml；宽度取 dialog_min_width_minor 减背景 inset；标题取 DialogWindowTitle 继承的 TextAppearance 的字号
- 写成显式值：遮罩 alpha = backgroundDimAmount × 255 转十六进制，宽度写百分比加左右内边距，其余照读出的数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- params.dimAmount 取窗口主题的 backgroundDimAmount（缺省 0.5f）：源端遮罩浓度的出处：窗口主题属性，不是对话框代码里的常数（出处：com.android.internal.policy.PhoneWindow#generateLayout）
- dialogCornerRadius 引用 @dimen/dialog_corner_radius：圆角要从主题属性再跟到 dimens.xml 读数（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material 的 dialogCornerRadius；values/dimens.xml，dialog_corner_radius（按应用的 compileSdk 取对应平台））
- dialog_min_width_minor = 95%（dialog_min_width_major = 65%）：竖屏时对话框窗口宽占屏宽的比例（横屏取 major）（出处：Android SDK 平台资源 data/res/values/dimens.xml，dialog_min_width_minor、dialog_min_width_major（按应用的 compileSdk 取对应平台））
- dialog_background_material：<inset android:inset="16dp">：背景四周内缩 16dp，可见卡宽再减 32dp（出处：Android SDK 平台资源 data/res/drawable/dialog_background_material.xml（按应用的 compileSdk 取对应平台））
- TextAppearance.Material.DialogWindowTitle 继承 TextAppearance.Material.Title：标题样式的解析顺序：字号和字体写在 Title 里（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.DialogWindowTitle（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 应用主题有没有覆写对话框外观：源工程 res/values 下的 styles / themes XML，按应用主题的 parent 链和 backgroundDimAmount、dialogCornerRadius、alertDialogTheme、windowMinWidthMinor 找；有覆写取覆写值；没有就看 parent 落到哪个框架主题，再去平台资源读
- 框架主题下的实际取值：按模块 Gradle 构建脚本里的 compileSdk 取对应平台的 Android SDK 平台资源 data/res/values 下 themes_*.xml、dimens.xml、styles_material.xml；顺着 ?attr 和 @dimen 引用读到数值；例：android-36 平台下 Theme.Material 的 backgroundDimAmount 是 0.6、dialog_corner_radius 是 2dp、标题 20sp sans-serif-medium，Theme.Holo 的 backgroundDimAmount 也是 0.6
未核实：应用主题是 Theme.AppCompat / Theme.MaterialComponents 一族时，对话框外观值在依赖库的 values.xml 里，族里规矩没有查过这一路的解析顺序和取值
来源：2 张卡，2 个应用
- case-20015832edaeb45f53bb（Bubble Shooter）：做法第 3 步 ← 建议 5
- case-dadda7b6820516f5f415（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2

## 规矩

- rule-e7fd2b1c8864｜工程已有平台 AlertDialog 复刻的共享弹窗时，偏好对话框交给它承载，不在页面另起自绘面板｜读到：工程里已有或计划有按平台 AlertDialog 外观复刻的共享弹窗组件，它的用途清单只列了 AlertDialog.Builder 构造的对话框；写错：设置页里为 EditTextPreference / ListPreference 另写一套自绘面板和按钮条（自建 @Component 按钮栏、Stack 覆层面板）
- rule-222d7672cb90｜Activity 级 Dialog 改写成页内覆层时，挂在覆盖整个窗口的宿主根 Stack，不挂在 Tab 子组件｜读到：弹窗是 Dialog 子类，构造时传 getActivity() 或 Activity 创建，样式继承 Theme.Dialog、windowIsFloating=true；写错：Tabs 子页或嵌套组件把根改成 Stack，在里面用 if 条件渲染全幅遮罩覆层；宿主页根 Stack 没挂这个覆层，遮罩盖不到底部 Tab 栏
- rule-12a62d6774ff｜源端会叠放多个对话框时，遮罩由宿主统一画一层，浓度取主题 backgroundDimAmount｜读到：源端先后 show() 两个以上 AlertDialog，或规格要求两层弹窗同时可见；写错：每个弹窗组件的根 Stack 里自带一层全屏半透明遮罩（如复用应用里碰巧有的半透明黑色资源），宿主又把几个实例叠在一起
- rule-4711a61e02b2｜框架 AlertDialog 的遮罩、圆角、标题取平台值（60%、2、20 号 Medium），不套鸿蒙卡片惯例｜读到：源端是框架生成的 AlertDialog（ListPreference 等 DialogPreference），应用主题没改 backgroundDimAmount、dialogCornerRadius 和对话框标题样式；写错：目标遮罩写 #66000000（40%），卡片 .borderRadius(24)，标题 fontSize(18)，报告里把这些标成「框架默认外观估计…待核」
- rule-374143220493｜框架 AlertDialog 落地成页内弹卡时，宽写 '95%' 加左右 16 内边距，不写 width(300)｜读到：源端是框架生成的 AlertDialog（含 ListPreference 选项对话框），没有自定义宽度；写错：页面根 Stack 的遮罩里，弹卡写死 width(300) 一类固定值，或照「约 280–320vp」估值
- rule-ab4a6a80199e｜ListPreference 没把 negativeButtonText 设为 @null 时，弹卡保留 CANCEL｜读到：偏好 XML 里的 ListPreference / DialogPreference 没写 android:negativeButtonText="@null"；写错：目标的偏好弹层（Stack 里的遮罩加卡片）一个按钮都没有，头注或报告写「无确定/取消钮」
