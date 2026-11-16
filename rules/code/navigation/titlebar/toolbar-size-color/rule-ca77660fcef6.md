# AppBarLayout 带 ThemeOverlay 时，工具栏标题和图标按覆盖取色，不按 DarkActionBar

审的是：代码
触发（任一种）：
- 读到：AppBarLayout / Toolbar 的 android:theme 的 parent 是 ThemeOverlay.AppCompat.Light，没写 titleTextColor，Activity 主题 *.DarkActionBar；写错的样子：标题 fontColor 和汉堡图标写成白色（Color.White 或 #FFFFFF），注释称按 DarkActionBar「推断」
- 读到：Toolbar 的 app:popupTheme 也是 Light 覆盖，AppBarLayout 内含 TabLayout，菜单项 showAsAction="never"；写错的样子：溢出点和 Tab 文字写成白色或半透明白，溢出菜单改用 bindMenu 默认外观
适用范围：迁移 AppBarLayout 内的 Toolbar、TabLayout、溢出菜单，源端用 ThemeOverlay 覆盖主题时
做法：
- 按「控件 style → 祖先 android:theme → Activity 主题」找取色方；DarkActionBar 的 actionBarTheme 只管窗口装饰 ActionBar，不管 setSupportActionBar 的 Toolbar
- Light 覆盖下标题 .fontColor 取 textColorPrimary（#DE000000），导航图标、溢出点取 colorControlNormal（#8A000000），Tab 字也深色；夜间 .Dark 为 #FFFFFFFF、#B3FFFFFF；写显式值，注明取自哪层
- 溢出菜单按 popupTheme 复刻成浅底 PopupMenu 式菜单，不用系统菜单默认外观
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ThemeOverlay.AppCompat.Light 的 parent 是 Base.ThemeOverlay.AppCompat.Light；后者 android:textColorPrimary = @color/abc_primary_text_material_light，colorControlNormal = ?android:attr/textColorSecondary：Light 覆盖下标题色和控件（导航图标、溢出点）色的来源（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，ThemeOverlay.AppCompat.Light、Base.ThemeOverlay.AppCompat.Light（按应用依赖的版本））
- primary_text_default_material_light = #de000000，secondary_text_default_material_light = #8a000000：Light 覆盖下标题色和导航图标色的具体值（abc_primary/secondary_text_material_light 的启用态）（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，primary_text_default_material_light、secondary_text_default_material_light；res/color/abc_primary_text_material_light.xml、abc_secondary_text_material_light.xml（按应用依赖的版本））
- primary_text_default_material_dark = #ffffffff，secondary_text_default_material_dark = #b3ffffff；Base.ThemeOverlay.AppCompat.Dark 的 colorControlNormal 同样是 ?android:attr/textColorSecondary：夜间 .Dark 覆盖下的标题色和导航图标色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.ThemeOverlay.AppCompat.Dark、primary_text_default_material_dark（按应用依赖的版本））
- Base.Theme.AppCompat.Light.DarkActionBar：actionBarTheme = @style/ThemeOverlay.AppCompat.Dark.ActionBar：DarkActionBar 的深色只经 actionBarTheme 给窗口装饰 ActionBar（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Theme.AppCompat.Light.DarkActionBar（按应用依赖的版本））
- Toolbar 标题的 android:textColor = ?android:attr/textColorPrimary：标题跟随主题的 textColorPrimary（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.TextAppearance.AppCompat.Widget.ActionBar.Title（按应用依赖的版本））
- 溢出点图标 abc_ic_menu_overflow_material 的 android:tint = ?attr/colorControlNormal：溢出点跟随主题的 colorControlNormal（出处：androidx.appcompat:appcompat 包内 res/drawable/abc_ic_menu_overflow_material.xml（按应用依赖的版本））
- colorBackgroundFloating = @color/background_floating_material_light = @android:color/white：Light 覆盖下浮层（弹出菜单）的底色（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.ThemeOverlay.AppCompat.Light、background_floating_material_light（按应用依赖的版本））
- 按 AppBarOverlay 解析色重写为深色标题（text_primary）和深色条形汉堡后与源一致：修复后的取色（出处：卡里修好并验证过）
针对本应用要查的：
- 提供工具栏取色的那一层主题：源工程布局 XML 里 Toolbar 的 style、app:popupTheme 和祖先 AppBarLayout 的 android:theme，再到 res/values/styles.xml 与 res/values-night/styles.xml 里该样式的 parent 链；顺着 parent 找到 ThemeOverlay.AppCompat.Light 或 .Dark，按上面的解析值取昼夜两色；样式自己覆盖了 android:textColorPrimary 或 colorControlNormal 的，以样式里的值为准
- Tab 文字的选中、未选中颜色：源工程布局 XML 里 TabLayout 的 app:tabTextColor、app:tabSelectedTextColor、style；没写时看应用依赖的 com.google.android.material:material 包内 res/values/values.xml 里 TabLayout 默认样式的 tabTextColor；顺着颜色引用解析到具体 ARGB，写进目标 Tab 的文字颜色
未核实：取值按本机 appcompat 1.7.1 核实，应用依赖的版本没有记在卡里
来源：2 张卡，1 个应用
- case-255a399de4580990a70e（Privacy Friendly 2048）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；做法第 3 步 ← 建议 4、诊断
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、建议 4；做法第 2 步 ← 建议 1、建议 4；取值 8 ← 诊断
