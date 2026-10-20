# 导航图标与菜单分区按实际生效者实现：DrawerToggle 画汉堡、parentActivityName 默认 Up，showAsAction 按名额宽度分流

ID：`lesson-a6121cc7eaf207b702f7` · 版本：6

[本主题](index.md)

## 何时使用

界面实现阶段，转换工具栏菜单 XML、自绘 ActionBar 或标题栏，决定导航图标（返回箭头或汉堡）、图标位与溢出菜单时；自绘框架主题提供的 ActionBar（应用图标、Up 尖角、溢出按钮、横竖屏高度与标题字号）时；同一菜单复用到自绘多选 CAB（ActionMode）时

## 适用情境

源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。也包括 Activity 基于 AppCompat、菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"）。也包括判断导航图标的输入：Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data、代码是否调用 setDisplayHomeAsUpEnabled、基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState；目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。也包括框架 ActionBar（Theme.Holo 等）带 manifest android:icon、setDisplayHomeAsUpEnabled 与 showAsAction="ifRoom|withText"，目标多个页面各自用 hideTitleBar 自绘标题栏。 也包括同一菜单 XML 在多选 CAB（ActionMode）里复用，部分项未声明 showAsAction；目标自绘工具栏与 CAB 栏，规格只登记了菜单 id 清单与显隐规则。

## 原因

全部放进溢出菜单或只设选中态，会丢掉工具栏图标位与勾选指示；反过来把 ifRoom 项一律上栏，又会在窄屏多出源端放进溢出的图标、挤掉标题——ifRoom 项是否上栏由 ActionMenuPresenter 按按钮名额与宽度预算决定。AppCompat 只读 app: 命名空间的 showAsAction，android:showAsAction 被忽略、所有项进右上 ⋮ 溢出菜单；把这些项做成标题栏图标，会多出源端没有的入口。导航图标同样由实际生效者决定：“只在源端启用 Up 时绘制”只是必要条件——AppCompat 窗口 ActionBar 在 Manifest 有 parentActivityName 时默认启用 Up，不调 setDisplayHomeAsUpEnabled 也显示箭头；基类的 ActionBarDrawerToggle.syncState 又会把同一 Toolbar 的 Up 换成汉堡。把前者读成“没调 setDisplayHomeAsUpEnabled 就不画”，或把后者保留成自定义返回标题栏，都会与源端不同。框架 ActionBar 的 withText 由 values-w480dp 控制，高度与标题字号另有 values-land 取值。同一菜单复用到 ActionMode 时，未声明 showAsAction 的项缺省值与选项菜单不同；DrawerToggle 管理的导航图标是按抽屉进度插值的同一绘制，不是两张图标切换。

## 做法

1. 绘制导航图标前按顺序判定：①Activity 或其基类（常见 BaseActivity.onPostCreate）以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState() 时，导航图标是汉堡、点击开关抽屉，setDisplayHomeAsUpEnabled 不再决定图标，目标装配抽屉基座的汉堡栏；②否则看主题是否带窗口 ActionBar（NoActionBar + 自建 Toolbar 按 setSupportActionBar 之后的调用判断）；③窗口 ActionBar 页在 Manifest 声明 parentActivityName 或 PARENT_ACTIVITY meta-data 时 AppCompat 默认显示 Up，点 Up 走 onOptionsItemSelected 的 android.R.id.home 分支或回父页；④代码显式 setDisplayHomeAsUpEnabled(true/false) 时以它为准；都没有才不画，返回交给系统返回键与手势。复用模板或兄弟页标题栏前先按当前源核对。
2. 按生效的 showAsAction（AppCompat 读 app:showAsAction，框架 ActionBar 读 android:showAsAction）照 ActionMenuPresenter.flagActionItems 分配：always 项必上栏；ifRoom 项按名额与宽度分配——名额取 ActionBarPolicy.getMaxActionButtons（按当前配置 dp：smallestWidth>600，或宽>960 且高>720，或宽>720 且高>960 为 5；宽≥500，或宽>640 且高>480，或宽>480 且高>640 为 4；宽≥360 为 3；否则 2），有 never 项或 always 与 ifRoom 合计超出名额时先给溢出钮扣一个名额，always 先扣；宽度预算为屏宽一半减溢出钮宽，按菜单顺序逐项扣按钮宽，透支的退回溢出；未上栏的 ifRoom 项与 never/collapseActionView 项按 orderInCategory 进溢出面板；横竖屏或窗口宽变化后重算。判断信号：同一菜单 always 与 ifRoom 合计 3 个以上，或含无图标的 ifRoom 文字项。checkable 项显式开启 selectIcon 等勾选指示。框架 ActionBar 的 withText 项只在窗口宽 ≥480dp 时在图标旁显示 TextAppearance.Holo.Widget.ActionBar.Menu 文字（12sp 粗体全大写；出处：框架 values-w480dp/bools.xml 的 config_allowActionMenuItemTextWithIcon 与 styles.xml），竖屏窄屏只显示图标。
3. Activity 基于 AppCompat 而菜单写 android:showAsAction 时，该属性被忽略，全部项进右上 ⋮ 溢出菜单，不转成标题栏图标或 NavDestination 图标菜单。
4. 自绘框架 ActionBar 时多页共用一个标题栏组件，各页只传图标、标题、是否 Up 与动作项（showAsAction、orderInCategory），上栏集合由组件按上一步计算：显示该 Activity 或 application 的 manifest android:icon，Up 尖角与溢出按钮用平台原图（如 ic_ab_back_holo_dark_am、ic_menu_moreoverflow_normal_holo_dark），高度、背景与标题字号取平台样式及 values-land 覆盖值，随窗口尺寸切换。
5. 同一菜单复用于 ActionMode（CAB）时分别填充：未声明 showAsAction 的项在选项菜单缺省 never，在 AppCompat StandaloneActionMode 缺省 ifRoom（MenuBuilder.setDefaultShowAsAction），按各自缺省值再走第 2 步的名额与宽度计算，不复制同一张固定清单。自绘 CAB 覆盖工具栏；窗口为 edge-to-edge 时 AppCompat 在 CAB 显示期间给状态栏区绘制 status guard 并盖住工具栏投影，按源 targetSdk 与窗口模式核对后实现。
6. 源端由 ActionBarDrawerToggle 管理导航图标时，图标是 DrawerArrowDrawable：汉堡与返回箭头是同一绘制按 position 插值，position 由 onDrawerSlide 写入抽屉滑动进度（源端调 setDrawerSlideAnimationEnabled(false) 或覆写 onDrawerSlide 时按源端）；setDrawerIndicatorEnabled(false) 改显返回箭头并让点击走返回，syncState() 按抽屉开合重设图标。目标用一个按进度绘制的图标和指示器启用态逐条承接源端这些调用，不用两张图标切透明度，也不以验收描述已覆盖代替缺失的调用。

来源支持：9 张卡 · 已知 5 次迁移（部分未记录） · 已知 5 个应用（部分未记录）

## 来源（按需复核）

- [case-255a399de4580990a70e](../../../store/cases/case-255a399de4580990a70e/f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f6ed46916e4fffbe8498bb8d8758eba997c05df5680aa0652de88a8b74f512c9`
- [case-45b40cf92799928188ab](../../../store/cases/case-45b40cf92799928188ab/12328be1792ad9e3cfad92aa5777a5997c9da687a70ce34dbad8fa41b8cedfa3.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`12328be1792ad9e3cfad92aa5777a5997c9da687a70ce34dbad8fa41b8cedfa3`
- [case-5f607109511beae4aec1](../../../store/cases/case-5f607109511beae4aec1/8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772.json) · 结论：recommendation:1, recommendation:3, recommendation:4, recommendation:6
  卡片版本：`8828a5ece38c458b890f0fcf43602c5b43fc2c7f01e073d04da1621028806772`
- [case-855df43db43e4ed66f9e](../../../store/cases/case-855df43db43e4ed66f9e/90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58.json) · 结论：diagnosis, recommendation:4
  卡片版本：`90ab1730914da1d421431502024f5fc3fbce0c541761fd4b3ae9ed8a57255a58`
- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:5
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
- [case-aa81c21ff3eaca257ba4](../../../store/cases/case-aa81c21ff3eaca257ba4/186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`186b3ad1798ec3352fd7eec9416a225c17b00304f58ef4f907d2a94f7d32f674`
- [case-ccade488607d58d27d0e](../../../store/cases/case-ccade488607d58d27d0e/3e5c0cc6e46e1b5861d8227f66879604a2e285b2bd4b0862f04103e0ae624e94.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`3e5c0cc6e46e1b5861d8227f66879604a2e285b2bd4b0862f04103e0ae624e94`
- [case-db3da49c14f06085f3b8](../../../store/cases/case-db3da49c14f06085f3b8/c679bb6c86541e5f34f87ce8cdf2a5916c70d1427e62bba1d5228300a4ad8967.json) · 结论：recommendation:5
  卡片版本：`c679bb6c86541e5f34f87ce8cdf2a5916c70d1427e62bba1d5228300a4ad8967`
- [case-ee2085c48fe78dbd3a2f](../../../store/cases/case-ee2085c48fe78dbd3a2f/0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1.json) · 结论：recommendation:4, recommendation:5
  卡片版本：`0d5ffa24bf798f0358ab64f71da008ad0e9a55d64c0c62be2089ad430e3160d1`
