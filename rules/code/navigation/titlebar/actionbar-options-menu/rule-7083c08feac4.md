# 菜单 XML 翻成自绘工具栏时，按 showAsAction 和名额、宽度算上栏集合，不把 ifRoom 写死

审的是：代码
触发（任一种）：
- 读到：res/menu/*.xml 的 <item> 带 app:showAsAction（always / ifRoom / never 或缺省）、android:orderInCategory，页面用 MenuInflater.inflate 填充工具栏菜单；写错的样子：自绘工具栏把分区写死：只渲染 always 图标，ifRoom 与 never 项全塞进溢出列表，没有按可用宽度算动作键数的逻辑
- 读到：源菜单 XML 的 android:showAsAction 有 always、ifRoom、never 混用，源端用窗口 ActionBar；写错的样子：共享标题栏组件的上栏过滤式把 always / ifRoom 全上栏、只把 never 放进溢出
适用范围：把安卓 Toolbar / ActionBar 菜单迁成 ArkUI 自绘工具栏（含各页共用的自绘标题栏）和溢出弹层时
做法：
- 把每项的 showAsAction（缺省也登记）、orderInCategory、<menu/> 子菜单逐项写成数据，如 { id, showAsAction, order, subMenu }；共享标题栏由组件内计算，消费方只传 showAsAction 和 orderInCategory
- 用布局函数按屏幕 dp 和按钮实测宽度算上栏集合（名额、溢出钮预留、半屏宽度预算）：always 必上栏，ifRoom 按顺序在名额和宽度内补位，其余和 never 进溢出；不把 ifRoom 写死成溢出，也不把 always / ifRoom 全上栏
- 横竖屏或窗口宽变化后重算上栏集合；检查：横屏、宽屏下动作键数随宽度变化
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showAsAction 的 flag：never = 0、ifRoom = 1、always = 2、withText = 4、collapseActionView = 8：never 进溢出，ifRoom 有空位才上栏，always 不受上限约束（出处：Android SDK 平台资源 data/res/values/attrs.xml，MenuItem 的 showAsAction（按应用的 compileSdk 取对应平台）；androidx.appcompat:appcompat 包内 res/values/values.xml，showAsAction（按应用依赖的版本））
- getMaxActionButtons：smallestScreenWidthDp > 600 或 (w > 960 且 h > 720) 或 (w > 720 且 h > 960) → 5；w ≥ 500 或 (w > 640 且 h > 480) 或 (w > 480 且 h > 640) → 4；w ≥ 360 → 3；否则 2（w、h 为 screenWidthDp、screenHeightDp）：动作键名额（含溢出钮）随屏宽变，横屏、平板上更多 ifRoom 项上栏（出处：com.android.internal.view.ActionBarPolicy#getMaxActionButtons（框架版，AppCompat 同名类本机只有编译产物））
- 有溢出项或 always + ifRoom 超过上限时先给溢出按钮留一格，再减去 always 项数；ifRoom 按顺序在剩余格数和宽度内上栏：布局函数的分区顺序（出处：android.widget.ActionMenuPresenter#flagActionItems）
- 宽度预算 = widthPixels / 2 − 溢出钮宽：上栏宽度预算，ifRoom 项按顺序扣按钮宽，透支的进溢出（出处：com.android.internal.view.ActionBarPolicy#getEmbeddedMenuWidthLimit；android.widget.ActionMenuPresenter#initForMenu）
- 改成 showAsAction 数据加按实测宽度排布的布局函数后，横屏、宽屏下动作键数与源端一致：数据加布局函数的做法经双机对照（出处：卡里修好并验证过）
- 组件移植 maxActionButtons() / actionFlags() 后，竖屏实机上栏项与安卓一致：共享标题栏修好后的写法（出处：卡里修好并验证过）
未核实：case-ccade488607d58d27d0e 的工程 SDK 是 6.1.1(24)，本机按 API 23 核对
来源：2 张卡，2 个应用
- case-45b40cf92799928188ab（Sokoban）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 5、建议 1、诊断；做法第 3 步 ← 建议 1；取值 6 ← 诊断
- case-ccade488607d58d27d0e（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 5 ← 诊断
