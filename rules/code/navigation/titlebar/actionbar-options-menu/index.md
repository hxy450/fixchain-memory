# 平台 ActionBar 和选项菜单

agent 会看到什么：读到 Activity 用平台主题的 ActionBar（setDisplayHomeAsUpEnabled、onCreateOptionsMenu）、菜单 XML 的 <item> 带 showAsAction 和 android:icon；交回的标题栏各页手绘、动作项放错位置（标题栏图标位或 ⋮ 溢出），或 Menu / MenuItem 只改了颜色

## 通用查法

### 标题栏由平台主题的 ActionBar 绘制时，到 SDK 平台资源查栏高、字号和图标，写成显式值

审的是：代码
触发（任一种）：
- 读到：Activity 的标题栏来自平台主题（如 android:Theme.Holo）的 ActionBar：setDisplayHomeAsUpEnabled、onCreateOptionsMenu，没有自定义 Toolbar 布局；写错的样子：目标标题栏的 .height、标题 fontSize、动作项文字样式是凭记忆写的数；Up、溢出图标用 Polyline、Text('<') 自绘
适用范围：目标端自绘源端平台主题提供的 ActionBar 外观时
做法：
- 按源工程的 compileSdk 打开 Android SDK 平台资源 data/res：values/ 与 values-land/ 的 dimens.xml 查 action_bar_default_height、action_bar_title_text_size，styles_holo.xml 查 TextAppearance.Holo.Widget.ActionBar.* 的字号、字重、大小写
- Up 和溢出图标从同一平台资源复制原图放进 media，写 Image($r('app.media.…'))
- 查出的值写成显式 vp / fp，横竖屏不同的按窗口尺寸切换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- action_bar_default_height 48dip / values-land 40dip；action_bar_title_text_size 18dp / values-land 16dp：例：android-35 平台资源里横竖屏的栏高和标题字号（出处：Android SDK 平台资源 data/res/values*/dimens.xml，action_bar_default_height、action_bar_title_text_size（按应用的 compileSdk 取对应平台））
- TextAppearance.Holo.Widget.ActionBar.Menu：textSize 12sp、textStyle bold：例：android-35 平台资源里动作项文字样式（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，TextAppearance.Holo.Widget.ActionBar.Menu（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- ActionBar 的栏高、标题字号和动作项文字样式：Android SDK 平台资源 data/res 下 values/、values-land/ 的 dimens.xml，values/styles_holo.xml、config.xml（按源工程的 compileSdk 取对应平台）；按资源名找到 dimen、style 的 item，横竖屏各记一个；style 里引用 @bool/、@dimen/ 的再到 config.xml、dimens.xml 解一层
- Up、溢出等图标的原图：同一平台的 data/res 下各密度 drawable 目录；找到主题用的那张图，复制进目标工程的 media 资源
未核实：Up、溢出图标在平台资源里的文件名和对应的主题属性，族里规矩没有查实
来源：1 张卡，1 个应用
- case-5f607109511beae4aec1（Blockinger）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3

## 规矩

- rule-01111c2e0093｜多页共享平台 ActionBar 时建一个共享组件，Up 和溢出用平台原图，不在各页手绘｜读到：多个 Activity 共用 android:Theme.Holo 提供的 ActionBar，各页 setDisplayHomeAsUpEnabled(true)；写错：各页各写一个标题栏 @Builder；Up 用 Text('<')、Polyline 或 Circle 画，标题字号各页不同，没有 manifest 图标
- rule-4d4221f600ae｜菜单项 showAsAction 含 ifRoom/always 且有 icon 时，放标题栏图标位，不进溢出菜单｜读到：菜单 XML 的 <item> 带 android:icon，且 app:showAsAction 或 android:showAsAction 含 ifRoom 或 always；写错：这一项和其余项一起放进溢出按钮 bindMenu 的 Menu 里，标题栏只有返回和溢出图标
- rule-0a373c6bcd5b｜AppCompat 下菜单用 android:showAsAction 时，全部项进右上 ⋮ 溢出菜单，不做成标题栏图标｜读到：菜单 XML 的 <item> 用 android:showAsAction="ifRoom"（常带 tools:ignore="AppCompatResource"），Activity 基于 AppCompat；写错：这些项被做成标题栏右侧的图标按钮，或 NavDestination 的 .menus 图标项
- rule-5af8f667cf55｜showAsAction 带 withText 时文字只在宽屏显示，ActionBar 高度和标题字号随横竖屏切换｜读到：菜单项 android:showAsAction="ifRoom|withText" 且有 android:icon，主题是 android:Theme.Holo；写错：竖屏窄屏也恒显示图标加文字；标题栏 .height(48) 和标题字号写死，没有横屏取值
- rule-7ef566e58560｜规格只给 Menu + MenuItem 而源端是平台主题弹出菜单时，逐项对照外观，对不上改页内浮层｜读到：规格的溢出菜单只写 Menu + MenuItem；源 Activity 主题 parent=android:Theme.Holo，菜单项 android:showAsAction="never"；写错：⋮ 按钮 .bindMenu(builder) 里 Menu + 若干 MenuItem，只改了 contentFontColor 和 backgroundColor（还借用对话框底色），没有面板边线和分隔线；返回键不先关菜单
- rule-6f45389b71ae｜带图标的溢出菜单项转 MenuItem 时，图标字段写 startIcon，不写 startImage｜读到：菜单 XML 的 <item> 带 android:icon，规格要求溢出菜单项带图标；写错：MenuItem({ startImage: …, content: … }) 用了不存在的 startImage 字段
- rule-8a8118bab1ca｜复刻溢出菜单或 PopupMenu 宽度时用 constraintSize 写下限和上限，不写 width(196)｜读到：菜单 XML 的 <item> 带 showAsAction="never"（进溢出菜单）或用 PopupMenu 弹出，标题是 @string/ 字符串资源；框架菜单项布局 abc_popup_menu_item_layout 写着 android:minWidth="196dip"；写错：自绘的菜单弹层或菜单行写成 .width(196)（或别的实测宽度），没有 maxWidth 上限，标题 Text 没有 maxLines(1)
- rule-159a7ea9822e｜源页 ActionBar 由框架主题着色且计划列了共享顶栏时，页面 hideTitleBar(true) 接共享标题栏｜读到：Activity 主题（values-vXX 覆盖优先）的父链到 android:Theme.Material.Light.DarkActionBar 这类带窗口 ActionBar 的框架主题，colorPrimary 指向应用色；计划或公共组件表列了共享顶栏组件；写错：NavDestination 上写 .title(...).menus(...) 用系统标题栏顶替（白底灰圆钮，没有主题底色和标题色），也没登记 `FWD-REF` 或 `HANDOFF` 指向共享件
- rule-7083c08feac4｜菜单 XML 翻成自绘工具栏时，按 showAsAction 和名额、宽度算上栏集合，不把 ifRoom 写死｜读到：res/menu/*.xml 的 <item> 带 app:showAsAction（always / ifRoom / never 或缺省）、android:orderInCategory，页面用 MenuInflater.inflate 填充工具栏菜单；写错：自绘工具栏把分区写死：只渲染 always 图标，ifRoom 与 never 项全塞进溢出列表，没有按可用宽度算动作键数的逻辑
- rule-b5f3158f380e｜实现里简化了源端动态行为时，在文件头注释和回执 risks 写明简化与差异｜读到：源菜单 XML 的 android:showAsAction 有 always、ifRoom、never 混用；写错：简化了源端的 ifRoom 上栏分配（如 always / ifRoom 全上栏），却没在文件头注释和回执 risks 里写明
- rule-bf43fe2b1138｜ForEach 渲染动作项或菜单项时，键要含项身份，不用下标加分类属性｜读到：源端菜单项 MenuItem 有 itemId 或标题资源 id，按 showAsAction 和屏幕宽度决定哪些显示在上栏；写错：ForEach 的 keyGenerator 用下标加分类属性拼键（如 `${index}_${item.showAsAction}_…`），不含项身份
