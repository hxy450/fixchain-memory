# 复刻平台 AlertDialog 的外观

agent 会看到什么：读到没有自定义样式的 AlertDialog.Builder / MaterialAlertDialogBuilder 或 manifest 里的 supportsRtl；产物里自绘对话框面板的字号字重、宽度和限高、标题与按钮条的对齐和方向，以及各页是否共用一个对话框组件

## 通用查法

### 自绘复刻没有自定义样式的平台对话框时，外观按源主题从平台资源读出再写显式值

审的是：代码
触发（任一种）：
- 读到：源端 AlertDialog.Builder / DialogFragment.onCreateDialog 没有自定义布局和样式；规格只写「按平台默认」或没给数值；写错的样子：自绘面板的 fontSize / fontWeight、宽度、按钮行高是手写常数，注释写「先例」「近似」，或标题写成 FontWeight.Bold
适用范围：用 ArkUI 自绘复刻安卓平台默认对话框的外观时
做法：
- 先定源主题：manifest 的 android:theme 指向的 style 顺着 parent 认出属于框架 Material、Holo 还是别的一族
- 在平台资源里从该主题的 alertDialogTheme / alertDialogStyle 顺到 styles*.xml 里标题、按钮的 TextAppearance，再顺 @dimen/…、@string/… 读出字号字体；宽度比例读 dimens.xml 的 dialog_min_width_minor / major
- 写成显式的 fontSize、fontWeight（sans-serif-medium 写 FontWeight.Medium）、fontColor 和宽度；读不出的回报规格缺项，不照兄弟页先例填
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- TextAppearance.Material.DialogWindowTitle 的 parent 是 TextAppearance.Material.Title；Title 的 textSize = @dimen/text_size_title_material，fontFamily = @string/font_family_title_material：框架 Material 一族的对话框标题外观定义在这条继承链上（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.DialogWindowTitle、TextAppearance.Material.Title（按应用的 compileSdk 取对应平台））
- TextAppearance.Material.Button 的 textSize = @dimen/text_size_button_material，fontFamily = @string/font_family_button_material：框架 Material 一族的按钮文字外观定义处（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.Button（按应用的 compileSdk 取对应平台））
- dialog_min_width_minor、dialog_min_width_major：平台对话框竖屏、横屏的最小宽度比例定义处（出处：Android SDK 平台资源 data/res/values/dimens.xml，dialog_min_width_minor、dialog_min_width_major（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 源主题：源工程 AndroidManifest 里 application / activity 的 android:theme，及它指向的 res/values 下的 style 和 parent 链；认出主题属于框架 Material、Holo 还是别的一族，再到对应平台的资源里找这个主题
- 这个主题下对话框标题、按钮的字号字体和对话框宽度：Android SDK 平台资源 data/res/values/themes*.xml 里源主题的 alertDialogTheme、alertDialogStyle，及其指向的 styles*.xml、dimens*.xml、donottranslate*.xml（按应用的 compileSdk 取对应平台）；顺着 @style/…、@dimen/…、@string/… 一步步解析到值；例：主题是框架 Material 一族时，标题是 TextAppearance.Material.DialogWindowTitle（继承 Title），查出来是 20sp、sans-serif-medium
- 按钮文字色 colorAccent：源工程 res/values 下应用主题的 style，没有覆盖时取 Android SDK 平台资源 data/res/values/themes_material.xml 里对应主题的 colorAccent；顺着 @color/… 或 ?attr/… 解析到色值，写成按钮的 fontColor
未核实：主题 → alertDialogTheme / alertDialogStyle → windowTitleStyle → TextAppearance.*.DialogWindowTitle 这条引用链，族里规矩没有逐级引原文核实，只核实了链尾的样式和尺寸；按钮条高度、分隔线、圆角等其余外观在平台资源里的定义处，族里规矩没有查实
来源：2 张卡，2 个应用
- case-641f7da5b5891df89eeb（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 诊断
- case-ed0c3a60e7342aa867b4（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2

## 规矩

- rule-acea0a69721b｜规格只写「按平台默认」没给数值时，对话框外观从平台资源取，不凭记忆或兄弟页先例填｜读到：源端是没有自定义样式的 AlertDialog.Builder；规格的弹窗契约只写「按平台默认」，没有数值；写错：自绘对话框面板写 .width('85%') 加 constraintSize({ maxWidth: 320 })、标题 .fontSize(20)、按钮行 .height(48)、圆角描边框，注释写「先例」或「近似」；或把已写对的平台值（如 22 的标题字号）改成兄弟页的值
- rule-d3f48f432631｜复刻框架 Material AlertDialog 时，标题和按钮的字号字重按主题取，不按印象写 Bold｜读到：源端 android.app.AlertDialog.Builder 只设 setTitle / setMessage / setPositiveButton / setNegativeButton，没有自定义布局或样式，应用主题是框架 Material 一族；写错：目标的标题写成 .fontWeight(FontWeight.Bold)，或字号、字重与计划值不一致；按钮字号字重是估的
- rule-a4a173b39b28｜Column 卡片里复刻左对齐标题、靠右按钮条时，子项设 width('100%') 再用 Start / End｜读到：源端 AlertDialog.Builder 的平台默认外观（标题、正文左对齐，按钮条靠右），或规格、派工写明「标题左对齐、按钮右排」；写错：Column 里的标题、正文 Text 只加了 .textAlign(TextAlign.Start)，按钮 Row 只加了 .justifyContent(FlexAlign.End)，都没设 width('100%')，父 Column 也没设 .alignItems(HorizontalAlign.Start)
- rule-413fcf411647｜未声明 supportsRtl 时，自绘对话框的面板和按钮条都加 .direction(Direction.Ltr)｜读到：manifest 的 `<application>` 没有 `android:supportsRtl`；源端确认框是 Material `AlertDialog`，按钮在右侧按 [负键][正键] 排；写错：复刻对话框的面板 `Column` 和按钮条 `Row` 都没写 `.direction(`，依赖默认 `Direction.Auto`，阿拉伯语系统下按钮镜像到左侧
- rule-92298595ffe3｜MaterialAlertDialog 转成的弹窗自带限高：卡片和内容 Scroll 都写 constraintSize｜读到：源对话框是 DialogFragment + MaterialAlertDialogBuilder.setView(ScrollView …)，高度由 AlertDialog 框架自动封顶；写错：弹窗组件的卡片只有 width('100%') 和不带 maxHeight 的 constraintSize，内容 Scroll 用 .layoutWeight(1)，注释写高度边界由宿主承担；改成窗口级弹窗后卡片撑满全窗、标题被压
- rule-f721bd9cb5ef｜多个源对话框共用同一平台 AlertDialog 外观时，实现一个共享对话框组件，各页只传内容｜读到：源端多处 AlertDialog.Builder / DialogFragment.onCreateDialog，都没有自定义样式，外观来自同一份平台 AlertDialog；写错：每个页面各自用 Stack 浮层加 Column 面板手绘对话框，标题、宽度、字号、按钮行各写各的
- rule-90c5316db98b｜自绘弹窗面板的容器和标题、消息、按钮条各区都要落底色，声明的颜色常量都要被引用｜读到：规格或派工给了对话框面板底色（如源端默认 AlertDialog 的深色面板）；写错：面板 Column 没有 .backgroundColor(...)，只有标题区上了色，消息区和按钮条透明；或者声明了面板底色常量却没被引用
- rule-2e75962f44c0｜M3 主题的 Material 对话框转卡片时，圆角 28、底色取主题值、宽度窗宽减 48vp｜读到：源码用 `MaterialAlertDialogBuilder`（setView、单选列表或消息），应用主题沿 styles.xml 的 parent 链继承 `Theme.Material3.*`；写错：对话框卡片写成 `borderRadius(4)`、`width('85%')` 或不设宽度，`backgroundColor` 用的是工程先例 token 而不是主题 colorSurfaceContainerHigh 解析出的颜色
- rule-7819db626115｜弹层和手写遮罩都显式设 maskColor，统一引用源主题推出的遮罩色｜读到：源端用 `MaterialAlertDialogBuilder` 或 `BottomSheetDialog` 弹出，主题 parent 链是 `Theme.Material3.*` 或主题里设了 `android:backgroundDimAmount`；写错：openCustomDialog 的 options 里没有 maskColor、bindSheet 的 SheetOptions 里没有 maskColor，或页内 Stack 手写遮罩用的颜色和弹层不是同一个 token
- rule-b4da356121e8｜源主题推出的弹窗取值与工程先例冲突时按源主题写，不复制登记为 UNC 的近似值｜读到：读过的工程先例文件里弹窗卡片的注释写「弹窗族先例」「同款」，或它的取值出自登记为 `UNC`、「需真机校对」的近似推断；写错：新写的弹窗卡片照抄先例的 borderRadius、backgroundColor、width、maxHeight，注释写「沿 … 弹窗家族语言」「`UNC` 定值」，与源主题推出的值不同
- rule-5fab2fb6429a｜弹窗按钮只照源码设了文案的 positive / negative / neutral 渲染，不补 Cancel｜读到：MaterialDialog.Builder 只调了 positiveText(...)，或 MaterialAlertDialogBuilder 只 setPositiveButton(...)、没有 setNegativeButton(...)；写错：目标弹窗的按钮行多出源码没有的取消 Button / Text 按钮
- rule-4b5e37bdbdfd｜AlertDialog 按钮条按框架布局落位成右簇，按钮带框架的 inset 和内距｜读到：框架 AlertDialog 的 setPositiveButton / setNegativeButton（按钮条布局 alert_dialog_button_bar_material）；写错：按钮条 Row 写成 [negative][Blank()][positive]，取消键被推到左边缘；或按钮写成无内距的 Text
- rule-8e325a72d1a3｜AlertDialog 按钮的 minHeight 不是渲染高度，不写成 .height(48)｜读到：对话框按钮样式 Widget.Material.Button.ButtonBar.AlertDialog 的 minHeight 是 @dimen/alert_dialog_button_bar_height（48dip）；写错：目标按钮写成 .height(48)，没有水平内距和 minWidth
- rule-8b76047b4c42｜复刻对话框时内容组件自己设卡片和内容区的最大高度，超高时框内滚动｜读到：源端框架对话框里的 EditText 或内容行数没有上限（超高时由窗口收束、内容框内滚动）；写错：目标卡片和 `TextArea` 都没有最大高度（没有 constraintSize({ maxHeight })），注释写「内容超出后内部滚动」，报告把越屏列为真机核对项
- rule-81232736c0ed｜AlertDialog 有标题且有消息或列表时，标题下补 8vp 间隔，自定义视图框不加｜读到：源对话框由 AlertDialog.Builder 生成（setTitle 加 setMessage / setItems / setAdapter），平台 alert_dialog_title_material.xml 里 id=titleDividerNoCustom 的 Space 写着 android:visibility="gone"、高 @dimen/dialog_title_divider_material；写错：openCustomDialog 自绘卡片的标题 Text 和消息或列表之间没有间隔，注释或登记写「Material 无标题分隔线」
- rule-25926ea04722｜setView 对话框的标题与内容间距按 AlertController.setupView 定，不凭记忆加垫片｜读到：对话框布局里 visibility="gone" 的 Space（Material 的 titleDividerNoCustom，contentPanel 里的 textSpacerNoTitle、textSpacerNoButtons），对话框用 setView 注入自定义视图；写错：目标在标题和自定义内容之间、内容下方加了垫片（如 .padding({ top: 18, bottom: 8 })）
- rule-959a6cb53f26｜复刻 AlertDialog 内容区时写上 contentPanel 的最小高 48dp｜读到：平台 alert_dialog_material.xml 里 id=contentPanel 写着 android:minHeight="48dp"；写错：自绘对话框的消息或列表区域没有 .constraintSize({ minHeight: 48 })，内容短时区域被压扁
