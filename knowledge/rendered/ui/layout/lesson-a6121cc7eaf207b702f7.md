# 导航图标与菜单分区按实际生效者实现：DrawerToggle 画汉堡、parentActivityName 默认 Up，showAsAction 按名额宽度分流

## 何时使用

界面实现阶段，转换工具栏菜单 XML、自绘 ActionBar 或标题栏，决定导航图标（返回箭头或汉堡）、图标位与溢出菜单时；自绘框架主题提供的 ActionBar（应用图标、Up 尖角、溢出按钮、横竖屏高度与标题字号）时；同一菜单复用到自绘多选 CAB（ActionMode）时

## 适用情境

源菜单项带图标与 showAsAction=ifRoom/always，或带 checkable=true。也包括 Activity 基于 AppCompat、菜单 XML 写的是 android:showAsAction（常带 tools:ignore="AppCompatResource"）。也包括判断导航图标的输入：Manifest 是否为 Activity 声明 parentActivityName 或 PARENT_ACTIVITY meta-data、代码是否调用 setDisplayHomeAsUpEnabled、基类 onPostCreate 是否以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState；目标套用自带返回箭头的标题栏模板、兄弟页标题栏，或保留自定义 Up 标题栏。除第 1 步①的 DrawerToggle 情形外，自建 Toolbar 不经 setSupportActionBar、直接在自身上设了导航图标（布局 app:navigationIcon 或代码 setNavigationIcon）的，导航图标和点击按 Toolbar 自己的设置与 setNavigationOnClickListener 实现，不套第 1 步的 Up 判定。也包括框架 ActionBar（Theme.Holo 等）带 manifest android:icon、setDisplayHomeAsUpEnabled 与 showAsAction="ifRoom|withText"，目标多个页面各自用 hideTitleBar 自绘标题栏。 也包括同一菜单 XML 在多选 CAB（ActionMode）里复用，部分项未声明 showAsAction；目标自绘工具栏与 CAB 栏，规格只登记了菜单 id 清单与显隐规则。

## 原因

全部放进溢出菜单或只设选中态，会丢掉工具栏图标位与勾选指示；反过来把 ifRoom 项一律上栏，又会在窄屏多出源端放进溢出的图标、挤掉标题——ifRoom 项是否上栏由 ActionMenuPresenter 按按钮名额与宽度预算决定。AppCompat 只读 app: 命名空间的 showAsAction，android:showAsAction 被忽略、所有项进右上 ⋮ 溢出菜单；把这些项做成标题栏图标，会多出源端没有的入口。导航图标同样由实际生效者决定：“只在源端启用 Up 时绘制”只是必要条件——AppCompat 窗口 ActionBar 在 Manifest 有 parentActivityName 时默认启用 Up，不调 setDisplayHomeAsUpEnabled 也显示箭头；基类的 ActionBarDrawerToggle.syncState 又会把同一 Toolbar 的 Up 换成汉堡。把前者读成“没调 setDisplayHomeAsUpEnabled 就不画”，或把后者保留成自定义返回标题栏，都会与源端不同。框架 ActionBar 的 withText 由窗口宽高与横竖屏决定（ActionMenuItemView.shouldAllowTextWithIcon），高度与标题字号另有 values-land 取值。同一菜单复用到 ActionMode 时，未声明 showAsAction 的项缺省值与选项菜单不同；DrawerToggle 管理的导航图标是按抽屉进度插值的同一绘制，不是两张图标切换。

## 做法

1. 绘制导航图标前按顺序判定：①Activity 或其基类（常见 BaseActivity.onPostCreate）以同一 Toolbar 构造 ActionBarDrawerToggle 并 syncState() 时，导航图标是汉堡、点击开关抽屉，setDisplayHomeAsUpEnabled 不再决定图标，目标装配抽屉基座的汉堡栏；②否则看主题是否带窗口 ActionBar（NoActionBar + 自建 Toolbar 按 setSupportActionBar 之后的调用判断）；③窗口 ActionBar 页在 Manifest 声明 parentActivityName 或 PARENT_ACTIVITY meta-data 时 AppCompat 默认显示 Up，点 Up 走 onOptionsItemSelected 的 android.R.id.home 分支或回父页；④代码显式 setDisplayHomeAsUpEnabled(true/false) 时以它为准；都没有才不画，返回交给系统返回键与手势。复用模板或兄弟页标题栏前先按当前源核对。
2. 按生效的 showAsAction（AppCompat 读 app:showAsAction，框架 ActionBar 读 android:showAsAction）照 ActionMenuPresenter.flagActionItems 分配：always 项必上栏；ifRoom 项按名额与宽度分配——名额取 ActionBarPolicy.getMaxActionButtons（按当前配置 dp：smallestWidth>600，或宽>960 且高>720，或宽>720 且高>960 为 5；宽≥500，或宽>640 且高>480，或宽>480 且高>640 为 4；宽≥360 为 3；否则 2），有 never 项或 always 与 ifRoom 合计超出名额时先给溢出钮扣一个名额，always 先扣；宽度预算为屏宽一半减溢出钮宽，按菜单顺序逐项扣按钮宽，透支的退回溢出；未上栏的 ifRoom 项与 never/collapseActionView 项按 orderInCategory 进溢出面板；横竖屏或窗口宽变化后重算。判断信号：同一菜单 always 与 ifRoom 合计 3 个以上，或含无图标的 ifRoom 文字项。checkable 项显式开启 selectIcon 等勾选指示。框架 ActionBar 的 withText 项在 screenWidthDp ≥480、或宽 ≥640 且高 ≥480、或横屏时在图标旁显示 TextAppearance.Holo.Widget.ActionBar.Menu 文字（12sp 粗体全大写；出处：框架 ActionMenuItemView.shouldAllowTextWithIcon 与 styles_holo.xml），竖屏窄屏只显示图标。
3. Activity 基于 AppCompat 而菜单写 android:showAsAction 时，该属性被忽略，全部项进右上 ⋮ 溢出菜单，不转成标题栏图标或 NavDestination 图标菜单。
4. 自绘框架 ActionBar 时多页共用一个标题栏组件，各页只传图标、标题、是否 Up 与动作项（showAsAction、orderInCategory），上栏集合由组件按上一步计算：显示该 Activity 或 application 的 manifest android:icon，Up 尖角与溢出按钮用平台原图（如 ic_ab_back_holo_dark_am、ic_menu_moreoverflow_normal_holo_dark），高度、背景与标题字号取平台样式及 values-land 覆盖值，随窗口尺寸切换。
5. 同一菜单复用于 ActionMode（CAB）时分别填充：未声明 showAsAction 的项在选项菜单缺省 never，在 AppCompat StandaloneActionMode 缺省 ifRoom（MenuBuilder.setDefaultShowAsAction），按各自缺省值再走第 2 步的名额与宽度计算，不复制同一张固定清单。自绘 CAB 覆盖工具栏；窗口为 edge-to-edge 时 AppCompat 在 CAB 显示期间给状态栏区绘制 status guard 并盖住工具栏投影，按源 targetSdk 与窗口模式核对后实现。
6. 源端由 ActionBarDrawerToggle 管理导航图标时，图标是 DrawerArrowDrawable：汉堡与返回箭头是同一绘制按 position 插值，position 由 onDrawerSlide 写入抽屉滑动进度（源端调 setDrawerSlideAnimationEnabled(false) 或覆写 onDrawerSlide 时按源端）；setDrawerIndicatorEnabled(false) 改显返回箭头并让点击走返回，syncState() 按抽屉开合重设图标。目标用一个按进度绘制的图标和指示器启用态逐条承接源端这些调用，不用两张图标切透明度，也不以验收描述已覆盖代替缺失的调用。

来源支持：9 张卡 · 已知 5 次迁移（部分未记录） · 已知 5 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 的平台资源；源码 android-36.1；androidx.appcompat:appcompat 1.1.0、1.7.1、1.8.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Activity.onCreate 中 manifest 为该 Activity 声明了 parentActivityName 时，把窗口 ActionBar 的默认 Up 设为开启（setDefaultDisplayHomeAsUpEnabled(true)），代码不调 setDisplayHomeAsUpEnabled 也显示返回箭头
- 〔做法第 1 步〕setDefaultDisplayHomeAsUpEnabled 只在没有显式设过 Up 时生效，代码显式调用 setDisplayHomeAsUpEnabled(true/false) 时以显式值为准
- 〔做法第 1 步〕appcompat 的 Base.V7.Theme.AppCompat 设 windowActionBar = true，Theme.AppCompat.NoActionBar 设 windowActionBar = false：主题是否带窗口 ActionBar 看 parent 链落到哪一支（1.7.1）
- 〔做法第 1 步〕应用主题没有另设 homeAsUpIndicator 时，AppCompat 主题默认 homeAsUpIndicator 为 @drawable/abc_ic_ab_back_material；平台 Theme.Material 的 android:homeAsUpIndicator 为 ic_ab_back_material，Theme.Holo 为 ic_ab_back_holo_dark
- 〔做法第 1 步〕AppCompat Toolbar 的导航按钮样式 Base.Widget.AppCompat.Toolbar.Button.Navigation 的 android:minWidth 为 56dp（API 21 起经平台 Widget.Material.Toolbar.Button.Navigation，同为 56dp）
- 〔原因 / 做法第 2 步〕showAsAction 标志：never = 0（进溢出）、ifRoom = 1（系统判定有空位才上栏）、always = 2（不受系统上栏上限约束）、withText = 4、collapseActionView = 8
- 〔原因 / 做法第 3 步〕appcompat 包的 declare-styleable MenuItem 里声明的是不带 android: 前缀的 showAsAction（菜单 XML 里的 app:showAsAction），平台的 MenuItem 声明的是 android:showAsAction
- 〔原因 / 做法第 2 步〕上栏名额 getMaxActionButtons（含溢出钮，单位 dp）：smallestScreenWidthDp > 600 或（宽 > 960 且高 > 720）或（宽 > 720 且高 > 960）为 5；宽 ≥ 500 或（宽 > 640 且高 > 480）或（宽 > 480 且高 > 640）为 4；宽 ≥ 360 为 3；否则 2，宽高取当前方向的 screenWidthDp、screenHeightDp
- 〔做法第 2 步〕flagActionItems：保留溢出钮且（有 never 项或 always 与 ifRoom 合计超过名额）时先减一个名额，再减去 always 项数，ifRoom 项按顺序用剩下的名额
- 〔做法第 2 步〕上栏宽度预算为 widthPixels / 2，保留溢出钮时再减去溢出钮的测量宽
- 〔做法第 2 步〕框架动作项遵守 withText 的条件：screenWidthDp ≥ 480，或宽 ≥ 640 且高 ≥ 480，或当前为横屏
- 〔做法第 2 步〕TextAppearance.Holo.Widget.ActionBar.Menu：textSize 12sp、textStyle bold、textAllCaps 取 config_actionMenuItemAllCaps（true）
- 〔做法第 4 步〕Theme.Holo 的 actionBarStyle 为 Widget.Holo.ActionBar、actionBarSize 为 @dimen/action_bar_default_height（Theme.Holo.Light 的 actionBarStyle 为 Widget.Holo.Light.ActionBar.Solid）
- 〔做法第 4 步〕Widget.Holo.ActionBar 的 background 是 @drawable/ab_transparent_dark_holo（drawable，不是纯色），标题样式为 TextAppearance.Holo.Widget.ActionBar.Title
- 〔做法第 4 步〕action_bar_default_height：values 48dip、values-land 40dip、values-sw600dp 56dip；action_bar_title_text_size：values 18dp、values-land 16dp、values-sw600dp 18dp
- 〔做法第 2 步〕MenuItem 的 selected 默认 false；selectIcon 默认 false（不显示勾），true 显示默认对勾，也可传自定义图标
- 〔做法第 5 步〕MenuBuilder 的缺省 showAsAction 是 SHOW_AS_ACTION_NEVER；StandaloneActionMode 与 WindowDecorActionBar 的 ActionMode 菜单把缺省设为 SHOW_AS_ACTION_IF_ROOM；MenuInflater 读不到 showAsAction 时得 -1，不调 setShowAsAction，沿用所填充菜单的缺省值
- 〔做法第 5 步〕appcompat 1.8.0 的 status guard 颜色 abc_decor_view_status_guard 为 #ff000000、abc_decor_view_status_guard_light 为 #ffffffff（1.1.0 包内没有这两个资源）
- 〔做法第 5 步〕框架 DecorView 的 status guard 在窗口设了 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR 时用 decor_view_status_guard_light，否则用 decor_view_status_guard
- 〔做法第 5 步〕targetSdk 为 35（VANILLA_ICE_CREAM）及以上的应用默认强制 edge-to-edge，windowOptOutEdgeToEdgeEnforcement（默认 false）设 true 可退出；targetSdk 36（BAKLAVA）及以上时该属性被忽略
- 〔做法第 6 步〕SideBarContainer 的 onChange 在侧栏显示状态变化完成时回调
