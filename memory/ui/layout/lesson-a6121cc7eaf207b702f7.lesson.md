# 工具栏导航图标按实际生效者绘制：基类以 ActionBarDrawerToggle 接管同一 Toolbar 时画汉堡；否则窗口 ActionBar 页在 Manifest 有 parentActivityName 时 AppCompat 默认显示 Up，都没有且未调 setDisplayHomeAsUpEnabled(true) 才不画；菜单项按实际生效的 showAsAction 与可用宽度分流到图标位或溢出菜单（AppCompat 下 android:showAsAction 被忽略），可勾选项开启勾选指示

ID：`lesson-a6121cc7eaf207b702f7` · 版本：5

[本主题](index.md)

## 何时使用

界面实现阶段，转换工具栏菜单 XML、自绘 ActionBar 或标题栏，决定导航图标（返回箭头或汉堡）、图标位与溢出菜单时；自绘框架主题提供的 ActionBar（应用图标、Up 尖角、溢出按钮、横竖屏高度与标题字号）时；同一菜单复用于 ActionMode/CAB、菜单项带子菜单，或规格登记菜单时

## 适用情境

源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。也包括 Activity 基于 AppCompat、菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"）。也包括判断导航图标的输入：Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data、代码是否调用 setDisplayHomeAsUpEnabled、基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState；目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。也包括框架 ActionBar（Theme.Holo 等）带 manifest android:icon、setDisplayHomeAsUpEnabled 与 showAsAction="ifRoom|withText"，目标多个页面各自用 hideTitleBar 自绘标题栏。 也包括菜单 XML 有多项 ifRoom、部分项未声明 showAsAction、项内嵌 <menu/> 子菜单，且同一菜单被 ActionMode 再次 inflate；以及 ActionBarDrawerToggle 管理导航图标时源端调用 setDrawerIndicatorEnabled(false)，或在刷新菜单等处 syncState。

## 原因

全部放进溢出菜单或只设选中态，会丢掉工具栏图标位与勾选指示。反过来，AppCompat 只读 app: 命名空间的 showAsAction，android:showAsAction 被忽略、所有项进右上 ⋮ 溢出菜单；把这些项做成标题栏图标，会多出源端没有的入口。导航图标同样由实际生效者决定：“只在源端启用 Up 时绘制”只是必要条件——AppCompat 窗口 ActionBar 在 Manifest 有 parentActivityName 时默认启用 Up，不调 setDisplayHomeAsUpEnabled 也显示箭头；基类的 ActionBarDrawerToggle.syncState 又会把同一 Toolbar 的 Up 换成汉堡。来源中前者被读成“没调 setDisplayHomeAsUpEnabled 就不画”，后者被保留成自定义返回标题栏。框架 ActionBar 的 withText 由 values-w480dp 控制，高度与标题字号另有 values-land 取值。 ifRoom 既不等于必上栏也不等于溢出：上栏数受 ActionBarPolicy 按窗口宽度给出的上限约束，写死成一种分区只在某一宽度下成立；同一菜单在 ActionMode 中未声明项的缺省是 IF_ROOM，与选项菜单的 NEVER 不同。汉堡与箭头是同一个 DrawerArrowDrawable 按进度插值绘制，两张图切透明度会丢掉与抽屉滑动的联动和指示器启用态。

## 做法

1. 绘制导航图标前按顺序判定：①Activity 或其基类（常见 BaseActivity.onPostCreate）以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState() 时，导航图标是汉堡、点击开关抽屉，setDisplayHomeAsUpEnabled 不再决定图标，目标装配抽屉基座的汉堡栏；②否则看主题是否带窗口 ActionBar（NoActionBar + 自建 Toolbar 按 setSupportActionBar 之后的调用判断）；③窗口 ActionBar 页在 Manifest 声明 parentActivityName 或 PARENT_ACTIVITY meta-data 时 AppCompat 默认显示 Up，点 Up 走 onOptionsItemSelected 的 android.R.id.home 分支或回父页；④代码显式 setDisplayHomeAsUpEnabled(true/false) 时以它为准；都没有才不画，返回交给系统返回键与手势。复用模板或兄弟页标题栏前先按当前源核对。抽屉指示器：DrawerArrowDrawable 的进度随 onDrawerSlide 的滑动比例在汉堡与箭头间插值，syncState 按抽屉开合同步进度；setDrawerIndicatorEnabled(false) 时改显示 Up 箭头，点击交源端 Up 处理。这些源调用逐条落实，不以“验收描述已覆盖”代替。
2. 生效的 showAsAction（AppCompat 读 app:showAsAction，框架 ActionBar 读 android:showAsAction）先逐项登记为数据（含缺省值、orderInCategory、子菜单），再按宽度布局：always 必上栏；ifRoom 按 orderInCategory 依序补位，上限取 AppCompat ActionBarPolicy.getMaxActionButtons 按当前窗口宽高（dp）给出的档位，并按 ActionMenuPresenter.flagActionItems 扣除溢出按钮与可用宽度（规则取依赖库源码，旋转或窗口变化时重算）；其余项与 never/collapseActionView 的进溢出。不按某一屏宽的截图把 ifRoom 写死成图标或溢出。checkable 项显式开启 selectIcon 等勾选指示。框架 ActionBar 的 withText 项只在窗口宽 ≥480dp 时在图标旁显示 TextAppearance.Holo.Widget.ActionBar.Menu 文字（12sp 粗体全大写），竖屏窄屏只显示图标。
3. Activity 基于 AppCompat 而菜单写 android:showAsAction 时，该属性被忽略，全部项进右上 ⋮ 溢出菜单，不转成标题栏图标或 NavDestination 图标菜单。
4. 自绘框架 ActionBar 时多页共用一个标题栏组件，各页只传图标、标题、是否 Up 与动作项：显示该 Activity 或 application 的 manifest android:icon，Up 尖角与溢出按钮用平台原图（如 ic_ab_back_holo_dark_am、ic_menu_moreoverflow_normal_holo_dark），高度、背景与标题字号取平台样式及 values-land 覆盖值，随窗口尺寸切换。
5. 同一菜单 XML 复用于 ActionMode/CAB 时分别传缺省：选项菜单里未声明 showAsAction 的项按 NEVER，StandaloneActionMode 按 IF_ROOM（setDefaultShowAsAction）。带 <menu/> 子菜单的项在溢出列表中显示子菜单箭头；由溢出项打开的子菜单带标题头，由动作键直接打开时不带。规格登记菜单时一并写出每项 showAsAction、缺省值与子菜单结构。

来源支持：7 张卡 · 已知 4 次迁移（部分未记录） · 已知 4 个应用（部分未记录）

## 来源（按需复核）

- [case-255a399de4580990a70e](../../../store/cases/case-255a399de4580990a70e/f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9`
- [case-5f607109511beae4aec1](../../../store/cases/case-5f607109511beae4aec1/8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772.json) · 结论：recommendation:1, recommendation:3, recommendation:4, recommendation:6
  卡片版本：`8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772`
- [case-855df43db43e4ed66f9e](../../../store/cases/case-855df43db43e4ed66f9e/90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58.json) · 结论：diagnosis, recommendation:4
  卡片版本：`90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58`
- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:5
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
- [case-aa81c21ff3eaca257ba4](../../../store/cases/case-aa81c21ff3eaca257ba4/186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674`
- [case-ccade488607d58d27d0e](../../../store/cases/case-ccade488607d58d27d0e/3e5c0cc6e46e1b5861d8227f66879604a2e285b2bd4b0862f04103e0ae624e94.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`3e5c0cc6e46e1b5861d8227f66879604a2e285b2bd4b0862f04103e0ae624e94`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:4, recommendation:5
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
