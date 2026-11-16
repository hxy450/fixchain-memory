# DrawerLayout 抽屉和汉堡工具栏

agent 会看到什么：源端 DrawerLayout 配 ActionBarDrawerToggle 接管 Toolbar 导航图标、NavigationView 抽屉菜单（含基类里的 toggle），对应目标的抽屉基座、汉堡栏和菜单行

## 通用查法

### 抽屉、Toolbar、NavigationView 没写样式时，到主题和库默认样式里查出值再写

审的是：代码
触发（任一种）：
- 读到：Toolbar、ActionBarDrawerToggle 或 NavigationView 没写外观属性（titleTextAppearance、itemIconTint、itemTextColor 等）；写错的样子：目标的汉堡、标题、菜单行用 SymbolGlyph 系统符号或凭印象的 fontSize、fontColor
适用范围：带抽屉的 AppCompat / Material 页面迁成目标端自绘的工具栏和抽屉菜单时
做法：
- 先看布局 XML 里控件的 style 和这些属性，再看应用主题里的 toolbarStyle、drawerArrowStyle、navigationViewStyle 和 colorPrimary、android:textColorPrimary / textColorSecondary
- 没覆写的，到应用依赖版本的 appcompat、material 包内 res/values/values.xml 和 res/layout 里按样式名找到条目，顺着 @dimen/、?attr/ 读到 dp、sp 和颜色
- 写成目标的显式 vp、fp 和颜色，注释写每项出处；库资源不在手边的逐项标待核
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Base.Widget.AppCompat.DrawerArrowToggle 给 barLength、gapBetweenBars、drawableSize；.Common 给 thickness 和 color = ?android:attr/textColorSecondary：抽屉开关三条横条的默认尺寸和颜色定义在这两个样式里（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.DrawerArrowToggle（按应用依赖的版本））
- Base.V7.Widget.AppCompat.Toolbar：contentInsetStart 16dp，contentInsetStartWithNavigation = @dimen/abc_action_bar_content_inset_with_nav：Toolbar 标题起点的默认值，带导航按钮的要再顺 @dimen 读数（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Widget.AppCompat.Toolbar（按应用依赖的版本））
- Widget.Design.NavigationView 不设 itemIconTint、itemTextColor、itemBackground、itemTextAppearance：这些默认外观由 NavigationView 代码和菜单项布局给出，不在样式里（出处：com.google.android.material:material 包内 res/values/values.xml，Widget.Design.NavigationView（按应用依赖的版本））
- 菜单项 minHeight = ?attr/listPreferredItemHeightSmall；菜单文字 textAppearance = TextAppearance.AppCompat.Body2：抽屉行高和文字外观要从菜单项布局顺着读（出处：material 包内 res/layout/design_navigation_item.xml、design_navigation_menu_item.xml）
针对本应用要查的：
- 源端是否覆写了工具栏、抽屉开关和抽屉菜单的样式：源工程布局 XML 里 Toolbar、NavigationView 的 style 和外观属性；res/values*/styles.xml、themes.xml 里应用主题的 toolbarStyle、drawerArrowStyle、navigationViewStyle、colorPrimary；写了就顺着样式取覆盖后的值；都没写就用库的默认样式
- 库默认样式的实际数值：应用依赖版本的 androidx.appcompat、com.google.android.material 包内 res/values/values.xml（按样式名、dimen 名找）和 res/layout 下的菜单项布局；从样式条目顺着 @dimen/、?attr/ 一层层读到 dp、sp 或颜色；例：没改样式时带导航按钮的 Toolbar 标题起点是 72dp（appcompat 1.7.1）
未核实：卡里核对默认值用的是 appcompat 1.7.1、material 1.8.0 / 1.12.0，应用依赖别的版本时默认值可能不同
来源：2 张卡，1 个应用
- case-cee85a6c89d26db1ef48（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 1
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2

## 规矩

- rule-069d4e22288d｜源端基类 toggle 接管导航图标的页面，目标装进抽屉基座的汉堡栏，不自绘返回标题栏｜读到：所继承基类的 onPostCreate 里 new ActionBarDrawerToggle(this, drawerLayout, toolbar, …) 并 toggle.syncState()，而规格或派工写的是「标题栏 + 返回箭头」；写错：页面自绘标题栏，放返回箭头图标、点击 pop() 返回，没有接共享的抽屉基座组件；文件头注释写与抽屉基座的汉堡栏不可共存、按 setDisplayHomeAsUpEnabled(true) 保留自定义标题栏
- rule-758e463bbc3c｜Toolbar 由 ActionBarDrawerToggle 接管导航时，按 AppCompat 默认几何画汉堡和标题｜读到：AppBarLayout 里的 Toolbar 没写 titleTextAppearance / contentInsetStartWithNavigation，代码里 setSupportActionBar + ActionBarDrawerToggle 接管导航图标；写错：汉堡用 SymbolGlyph 系统符号（如 sys.symbol.line_3_horizontal），标题常规字重、起点很靠左（左距 4 左右），工具栏没有投影
- rule-cca241284273｜NavigationView 没写 item 样式时，抽屉行按 Material 默认样式逐项复刻，不只做二值变色｜读到：DrawerLayout 里的 com.google.android.material.navigation.NavigationView 只给 app:menu、app:headerLayout，没写 itemIconTint、itemTextColor、itemBackground、itemTextAppearance；menu 分组带 android:checkableBehavior；写错：目标菜单行只按选中切换 fontColor / fillColor（选中 colorPrimary、未选纯黑），没有选中底色和加粗，未选图标不着灰；组间 Divider 左右内缩、借近名灰色；List 没有顶部留白
- rule-214bcec6f9b9｜共享基座遇到先行页面的页内草稿时，把它当待收敛对象，不当取值来源｜读到：工程里先行页面已有页内等价草稿（如页内抽屉），注释写着它自己的取值，例如「checked → colorPrimary，默认 → 黑」；写错：共享组件照草稿取值（注释写 precedent、沿用某页先例），只剩 fontColor / fillColor 二值切换；和源库默认或自己原先的推导（选中项有底色、未选图标偏灰）不一致时也跟草稿走
- rule-8caa2875feec｜源端导航图标是 DrawerArrowDrawable 时，目标按 position 插值画汉堡↔箭头，不切两张图透明度｜读到：源端用 ActionBarDrawerToggle / DrawerArrowDrawable，onDrawerSlide 里写 position（汉堡到箭头的动画）；写错：导航位用汉堡和返回箭头两张图按 .opacity(...) 交叉淡化，没有和抽屉开合共用的 position，也没有指示器启用态
- rule-07f3acdad758｜源方法里对框架对象的调用逐条落到目标，缺一条在报告列明，不以「AC 已覆盖」代替｜读到：源方法里调了抽屉开关：getDrawerToggle().setDrawerIndicatorEnabled(false)，或重建菜单的方法末尾调 syncState()；写错：目标方法里没有对应调用，注释写「…由 AC 验收覆盖」或只留 FWD-REF 记号；重建菜单的方法末尾缺 syncState，指示器从没被禁用
